# -*- coding: utf-8 -*-
"""
Resolve each work Xinyu Fu cites to an OpenAlex record, and pull that record's own
reference list. That second hop is what makes the sky deep: her papers cite ~600
works, and those works in turn rest on a shared foundation that first-order
coupling cannot see.

    python3 resolve_oa.py            # resumable; caches every lookup to oa_cache/

No API key is needed. Nothing personal is sent — only the bibliographic strings that
already appear in the manuscripts' reference lists.
"""
import json, os, re, sys, threading, time, unicodedata, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'oa_cache')
os.makedirs(CACHE, exist_ok=True)

API = 'https://api.openalex.org/works'
SELECT = 'id,display_name,publication_year,authorships,referenced_works,cited_by_count,primary_location'
UA = 'xinyufu-website-citation-map/1.0'

# OpenAlex runs two pools. The anonymous one is throttled hard and unpredictably
# — a fresh request can come back 429 with a 36-second Retry-After — so at its
# pace this run takes hours. Identifying yourself with a contact address puts you
# in the "polite pool", which is the documented way to ask for a real rate. It is
# opt-in on purpose: set OA_MAILTO before running.
#
#     OA_MAILTO=you@example.edu python3 resolve_oa.py
#
MAILTO = os.environ.get('OA_MAILTO', '').strip()
POLITE = ('&mailto=' + urllib.parse.quote(MAILTO)) if MAILTO else ''
MIN_GAP = 0.12 if MAILTO else 4.0     # seconds between requests


def strip(s):
    s = unicodedata.normalize('NFKD', s or '')
    return ''.join(c for c in s if not unicodedata.combining(c))


def norm_title(s):
    return re.sub(r'[^a-z0-9 ]', ' ', strip(s).lower()).strip()


def toks(s):
    STOP = set('a an the of on in at to for from with and or but as by is are be'.split())
    return set(w for w in norm_title(s).split() if w not in STOP and len(w) > 2)


def sim(a, b):
    ta, tb = toks(a), toks(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


_throttle = threading.Semaphore(1)
_last = [0.0]

# OpenAlex meters a fixed number of requests per day. When that runs out it still
# answers 429, but with a Retry-After of most of a day rather than a few seconds.
# The first version could not tell the two apart and simply slept on it — which
# looked exactly like a hung process. A long Retry-After is not something to wait
# out; it is the end of the run, and the only thing to do is say so and stop.
BURST_MAX = 300.0                     # seconds; longer than this is the daily cap
STOP_AT   = 25                        # leave this much of the day's budget unspent
_exhausted = threading.Event()
_remaining = [None]                   # what OpenAlex last said was left for today


def _note_budget(headers):
    """Every answer carries the day's remaining budget. Watching it is the
    difference between a run that stops with a clean resume point and one that
    spends its last hundred requests on retries and stops mid-lookup."""
    try:
        n = int(headers.get('X-RateLimit-Remaining'))
    except (TypeError, ValueError):
        return
    _remaining[0] = n
    if n <= STOP_AT:
        _exhausted.set()


def get(url, tries=6):
    """Returns the decoded body, or {'_error': ...}. A 429 is a transient failure,
    never an answer — the caller must not cache it as 'no such work'."""
    for i in range(tries):
        if _exhausted.is_set():
            return {'_error': 'daily quota exhausted'}
        with _throttle:
            wait = MIN_GAP - (time.time() - _last[0])
            if wait > 0:
                time.sleep(wait)
            _last[0] = time.time()
        try:
            req = urllib.request.Request(url + POLITE,
                                         headers={'User-Agent': UA,
                                                  'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=40) as r:
                _note_budget(r.headers)
                return json.loads(r.read().decode('utf8'))
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                _note_budget(e.headers)
                back = float(e.headers.get('Retry-After') or 0) or min(60, 4 * (i + 1) ** 2)
                if back > BURST_MAX:
                    _exhausted.set()
                    return {'_error': 'daily quota exhausted; resets in %d h %d min'
                                      % (back // 3600, (back % 3600) // 60)}
                if i >= 1:
                    # a rejected request still costs one. Two are enough to learn
                    # that the pace is wrong; a third just spends the budget.
                    return {'_error': 'rate limited'}
                time.sleep(back)
                continue
            return {'_error': 'http %d' % e.code}
        except Exception as e:
            if i == tries - 1:
                return {'_error': str(e)}
            time.sleep(2.0 * (i + 1))
    return {'_error': 'rate-limited'}


def cache_path(key):
    safe = re.sub(r'[^a-z0-9]+', '_', key.lower())[:120]
    return os.path.join(CACHE, safe + '.json')


def resolve(w):
    """Find the OpenAlex record for one cited work. Conservative: an unmatched work
    is better than a wrong one, because a wrong match imports someone else's
    reference list into the graph."""
    cp = cache_path(w['key'])
    if os.path.exists(cp):
        try:
            return json.load(open(cp, encoding='utf8'))
        except Exception:
            pass

    title = (w.get('title') or '').strip()
    out = {'key': w['key'], 'matched': False}
    if len(norm_title(title)) < 12:
        json.dump(out, open(cp, 'w')); return out

    q = urllib.parse.quote(norm_title(title)[:220])
    data = get('%s?filter=title.search:%s&per-page=5&select=%s' % (API, q, SELECT))
    if data.get('_error'):
        return {'key': w['key'], 'matched': False, 'error': data['_error']}  # NOT cached
    results = data.get('results') or []
    if not results:
        data = get('%s?search=%s&per-page=5&select=%s' % (API, q, SELECT))
        if data.get('_error'):
            return {'key': w['key'], 'matched': False, 'error': data['_error']}
        results = data.get('results') or []

    want_year = w.get('year') or 0
    want_a1 = strip((w['authors'][0] if w.get('authors') else '')).lower()

    best, best_s = None, 0.0
    for r in results:
        s = sim(title, r.get('display_name') or '')
        yr = r.get('publication_year') or 0
        names = [strip((a.get('author') or {}).get('display_name') or '').lower()
                 for a in (r.get('authorships') or [])]
        a1_ok = any(want_a1 and want_a1 in n for n in names[:6])
        yr_ok = bool(want_year) and abs(yr - want_year) <= 2

        # a title alone must be near-identical; with author or year agreement, relax it
        ok = (s >= 0.85) or (s >= 0.62 and (a1_ok or yr_ok)) or (s >= 0.5 and a1_ok and yr_ok)
        if ok and s > best_s:
            best, best_s = r, s

    if best:
        out = {'key': w['key'], 'matched': True,
               'oa': best['id'].rsplit('/', 1)[-1],
               'title': best.get('display_name'),
               'year': best.get('publication_year'),
               'cites': best.get('cited_by_count') or 0,
               'refs': [x.rsplit('/', 1)[-1] for x in (best.get('referenced_works') or [])],
               'sim': round(best_s, 3)}
    json.dump(out, open(cp, 'w'))
    return out


if __name__ == '__main__':
    works = json.load(open(os.path.join(HERE, 'works.json'), encoding='utf8'))
    print('resolving %d cited works against OpenAlex...' % len(works))
    done = []
    if MAILTO:
        print('polite pool, identifying as %s' % MAILTO)
    else:
        print('anonymous pool — %.1fs between requests; set OA_MAILTO to go faster'
              % MIN_GAP)
    with ThreadPoolExecutor(max_workers=3 if MAILTO else 1) as ex:
        for i, r in enumerate(ex.map(resolve, works), 1):
            done.append(r)
            if i % 25 == 0:
                m = sum(1 for x in done if x.get('matched'))
                left = ('' if _remaining[0] is None
                        else '   budget left today: %d' % _remaining[0])
                print('  %4d/%d  matched %d (%.0f%%)%s'
                      % (i, len(works), m, 100.0 * m / i, left))
                sys.stdout.flush()

    json.dump(done, open(os.path.join(HERE, 'oa_level1.json'), 'w'), indent=1)
    err = [x for x in done if x.get('error')]
    if err:
        print('%d lookups did not complete (not cached) — re-run to finish them' % len(err))
        quota = [x for x in err if 'quota' in x['error']]
        if quota:
            print('   ' + sorted(quota, key=lambda x: x['error'])[-1]['error'])
        elif _remaining[0] is not None and _remaining[0] <= STOP_AT:
            print('   stopped with %d requests left of today\'s allowance, on'
                  ' purpose — run again after it resets at midnight UTC'
                  % _remaining[0])
    m = [x for x in done if x.get('matched')]
    nrefs = sum(len(x['refs']) for x in m)
    print()
    print('matched %d/%d (%.0f%%)' % (len(m), len(done), 100.0 * len(m) / max(1, len(done))))
    print('second-hop references pulled: %d' % nrefs)
    with_refs = sum(1 for x in m if x['refs'])
    print('matched works that expose a reference list: %d' % with_refs)
