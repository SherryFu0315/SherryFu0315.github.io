# -*- coding: utf-8 -*-
"""
One step back from the literature view: works that several of my studies reach
through the papers they cite.

Presence only. Nothing here moves a study or a work, and secondorder.json's
coupling2 weights are never read: they count the same shared first-order paper
over and over, and they grow with how far each reference list has been traced,
so a heavier pair would mostly mean a better-traced one.

    python3 -B deepsky.py      # dry run: what would be drawn and named (-B keeps
                               # .pyc files out of the repo)

build() returns None when there is nothing honest to draw, and the map is then
byte-identical to the one without this layer.
"""
import datetime, html, json, math, os, re, unicodedata
from collections import Counter, defaultdict
from itertools import combinations

from citelayout import _h
import words as T

HERE = os.path.dirname(os.path.abspath(__file__))

K_MIN, N_MAX = 3, 1500      # draw works reached by >= K studies; K rises while more than N_MAX qualify
T_PAIR = 3                  # pair floor: works two studies reach through different papers
NOTE_CAP, HOVER_CAP = 6, 12
STAR_CLEAR, LAM, SQ = 12.0, 0.55, 0.88   # 0.88 is the halos' own vertical squash

# OpenAlex id -> why. Still drawn, never named. Read the build log's note and
# hover lines after each OpenAlex run; anything wrong goes here.
DEEP_DENY = {}

# OpenAlex id -> year. OpenAlex dates a paper by when it first appeared online; my
# reference lists date it by volume, often a year later. Named works whose two
# years differ are corrected here so a tooltip agrees with my own dots.
DEEP_YEAR = {
    'W2526781987': 2017,    # Frey & Osborne, Technological Forecasting and Social Change 114
    'W2944727737': 2020,    # Lindebaum et al., Academy of Management Review 45(1)
}

# Records that are not works: front matter, series, journals filed as papers.
GENERIC = re.compile(r'^(glossary|index|introduction|preface|foreword|editorial|editor s comments?|front matter|'
                     r'back matter|book reviews?|reviews?|references|contents|erratum|corrigendum|correction|'
                     r'retraction|announcements?|call for papers|abstracts?|bibliography|about the authors|acknowledg)\b')
SERIES = re.compile(r'^(advances in|annual review of|handbook of|proceedings|journal of)\b')
PERIOD = re.compile(r'\b(review|journal|quarterly|magazine|proceedings|letters|bulletin|annals|transactions|'
                    r'newsletter|gazette)s?$')
# Venues that stand in for a work rather than publish it (book reviews, preprint servers).
BAD_VENUE = re.compile(r'choice reviews|book review|reviews online|contemporary sociology|ssrn|arxiv|'
                       r'research papers in economics|repository|working paper|preprint')
INST = {'university', 'institute', 'association', 'organization', 'organisation', 'staff', 'anonymous', 'unknown',
        'editor', 'editors', 'team', 'group', 'committee', 'consortium', 'collaboration'}
SURNAME = re.compile(r"^[^\W\d_](?:[^\W\d_]|['’\-])+$")
PARTICLE = {'von', 'van', 'de', 'der', 'den', 'del', 'della', 'da', 'di', 'du', 'le', 'la', 'ter', 'ten', 'vom', 'zu',
            'dos', 'das', 'el', 'al'}
STOP = set('a an the of and in on for to with by at from as is are its'.split())


def _fold(s):
    s = unicodedata.normalize('NFKD', s or '')
    return ''.join(c for c in s if not unicodedata.combining(c)).lower()


def _nv(s):                     # venue or title, normalised for comparison
    s = ' '.join(re.sub(r'[^a-z0-9 ]', ' ', _fold(s).replace('&', ' and ')).split())
    return s[4:] if s.startswith('the ') else s


def _tkey(t):                   # dedupe key: no punctuation, chapter number or stopwords
    s = re.sub(r'^\s*\d+\s+', '', re.sub(r'[^a-z0-9 ]', ' ', _fold(t)))
    return ' '.join(w for w in s.split() if w not in STOP)


def _k(by):
    """Independent reach: how many studies can each be matched to a DIFFERENT
    first-order paper that cites the work. A work two studies reach only through
    one paper they both cite scores 1, because that link is already a gold star."""
    match = {}

    def aug(s, seen):
        for w in by[s]:
            if w not in seen:
                seen.add(w)
                if w not in match or aug(match[w], seen):
                    match[w] = s
                    return True
        return False
    return sum(1 for s in sorted(by) if aug(s, set()))


def _who(au):                   # the existing tooltip convention, escaped
    au = [html.escape(a) for a in au if a]
    if not au:
        return ''
    return au[0] if len(au) == 1 else (au[0] + ' &amp; ' + au[1] if len(au) == 2 else au[0] + ' et al.')


def _short(t):                  # up to the colon, or just past a question mark
    t = t.split(':')[0]
    q = t.find('?')
    return (t[:q + 1] if q > 0 else t).strip()


def _clean(t):
    return re.sub(r'\s+([”’"\)\]\?\.,:;])', r'\1', ' '.join((t or '').split()))


def build(cworks, sxy, wxy, cpairs, ids, year=None):
    """Everything the page needs for the layer, or None for today's map."""
    try:
        so = json.load(open(os.path.join(HERE, 'secondorder.json'), encoding='utf8'))
        l1 = {r['key']: r for r in json.load(open(os.path.join(HERE, 'oa_level1.json'), encoding='utf8'))}
        anc = so['ancestors']
    except (OSError, ValueError, KeyError, TypeError) as e:
        print('deep sky off: %r' % (e,))
        return None
    year = year or datetime.date.today().year
    idset = set(ids)
    widx = {w['key']: i for i, w in enumerate(cworks)}

    def traced(k):              # one definition everywhere: resolved AND has a reference list
        r = l1.get(k, {})
        return bool(r.get('matched') and r.get('refs'))

    tr = {s: [0, 0] for s in ids}
    paths = defaultdict(lambda: defaultdict(set))       # ancestor -> study -> first-order keys
    cyear = defaultdict(list)
    for w in cworks:
        for s in w['cited_by']:
            if s in tr:
                tr[s][1] += 1
                tr[s][0] += traced(w['key'])
        if traced(w['key']):
            for x in l1[w['key']]['refs']:
                cyear[x].append(l1[w['key']].get('year') or w.get('year') or 0)
                for s in w['cited_by']:
                    if s in idset:
                        paths[x][s].add(w['key'])
    n_traced = sum(traced(w['key']) for w in cworks)
    # still going while any lookup has not happened yet; the copy says so only then
    ongoing = any(r.get('error') for r in l1.values()) or any(w['key'] not in l1 for w in cworks)
    if not n_traced or not anc:
        print('deep sky off: nothing traced yet')
        return None

    venues = ({_nv(w.get('venue')) for w in cworks} | {_nv(a['m'].get('v')) for a in anc if a.get('m')}) - {''}

    def is_work(m):
        t = _nv(m.get('t'))
        return (bool(t) and t != _nv(m.get('v')) and t not in venues and not GENERIC.match(t)
                and not SERIES.match(t) and not (not m.get('a') and PERIOD.search(t)))

    # verified works only: a record OpenAlex could not describe is not drawn or counted
    real = [a for a in anc if a.get('m') and is_work(a['m'])]
    groups, byk = [], defaultdict(list)
    for a in real:
        byk[_tkey(a['m']['t'])].append(a)
    for L in byk.values():      # the same work under several records: same title, years chained within 1
        L.sort(key=lambda a: a['m'].get('y') or 0)
        cur = [L[0]]
        for a in L[1:]:
            if (a['m'].get('y') or 0) - (cur[-1]['m'].get('y') or 0) <= 1:
                cur.append(a)
            else:
                groups.append(cur)
                cur = [a]
        groups.append(cur)

    def canon(g):
        return min(g, key=lambda a: (not a['m'].get('a'), -(a['m'].get('c') or 0), a['oa']))

    fo_oa = {l1[w['key']]['oa']: w['key'] for w in cworks
             if l1.get(w['key'], {}).get('matched') and l1[w['key']].get('oa')}
    wt = [(w['key'], set(_tkey(w['title']).split()), w.get('year') or 0) for w in cworks]

    def twin(g):                # a work I cite directly already has a dot on the map
        for a in g:
            if a['oa'] in fo_oa:
                return fo_oa[a['oa']]
        best = None
        for a in g:
            A, y = set(_tkey(a['m']['t']).split()), a['m'].get('y') or 0
            if len(A) < 2:
                continue
            for key, B, wy in wt:
                if B and abs(y - wy) <= 2:
                    j = len(A & B) / float(len(A | B))
                    if j >= 0.8 and (best is None or j > best[0]):
                        best = (j, key)
        return best[1] if best else None

    deep, dk, pairs = [], {}, Counter()
    for g in groups:
        by = defaultdict(set)
        for a in g:
            for s, ks in paths[a['oa']].items():
                by[s] |= ks
        for x, y in combinations(sorted(by), 2):        # a yes/no floor per pair, never a weight
            if any(p != q for p in by[x] for q in by[y]):
                pairs[x, y] += 1
        k = _k(by)
        if k < 2:
            continue
        via, fk = set().union(*by.values()), twin(g)
        if fk:
            i = widx[fk]
            if k > dk.get(i, {}).get('k', 0):
                dk[i] = {'k': k, 'w': sorted(widx[x] for x in via), 'g': g}
            continue
        deep.append(dict(g=g, k=k, S=sorted(s for s in by if s in sxy), via=via, oa=canon(g)['oa']))

    K = K_MIN
    while sum(d['k'] >= K for d in deep) > N_MAX:
        K += 1
    drawn = sorted((d for d in deep if d['k'] >= K and len(d['S']) >= 2), key=lambda d: d['oa'])
    if not drawn:
        print('deep sky off: no work reaches %d studies yet' % K)
        return None

    # ---- naming: only what passes every check gets a name
    myv = {}
    for w in cworks:
        v = _nv(w.get('venue'))
        if v and not BAD_VENUE.search(v):
            myv.setdefault(v, w['venue'])

    def my_venue(v):            # spelled the way my own reference lists spell it
        v = _nv(v)
        if not v or BAD_VENUE.search(v):
            return None
        if v in myv:
            return myv[v]
        return next((myv[m] for m in myv if v.startswith(m + ' ')), None)

    lost = {_fold(a.split()[-1]) for w in cworks for a in w['authors']
            if len(a.split()) > 1 and _fold(a.split()[0]) in PARTICLE}
    fa = defaultdict(set)
    for a in anc:
        if a.get('m') and a['m'].get('a'):
            fa[_tkey(a['m']['t'])].add(_fold(a['m']['a'][0]))

    def why_not(g):
        c = canon(g)
        m = c['m']
        t, y = _clean(m.get('t')), m.get('y') or 0
        au = [x for x in m.get('a') or [] if x]
        if c['oa'] in DEEP_DENY:
            return 'deny'
        if not (t and y and au):
            return 'incomplete'
        if not SURNAME.match(au[0]) or _fold(au[0]) in INST or au[0] == (au[1:2] or [''])[0]:
            return 'author'
        if any(_fold(x) in lost for x in au[:2]):
            return 'particle'
        if len({_fold(a['m']['a'][0]) for a in g if a['m'].get('a')}) > 1 or len(fa[_tkey(t)]) > 1:
            return 'author conflict'
        cy = [x for a in g for x in cyear[a['oa']] if x]
        if not 1900 <= y <= year or (cy and y > min(cy) + 1):
            return 'year'
        if len(_tkey(t).split()) < 2 or re.match(r'^\s*\d', t):
            return 'title'
        L = [ch for ch in t if ch.isalpha()]
        if sum(ch.isupper() for ch in L) > 0.6 * max(1, len(L)):
            return 'capitals'
        return None if my_venue(m.get('v')) else 'venue'

    pool = []
    for d in deep:
        if why_not(d['g']) is None:
            m = canon(d['g'])['m']
            pool.append(dict(src='deep', id=d['oa'], k=d['k'], via=len(d['via']), cites=m.get('c') or 0,
                             t=_clean(m['t']), a=_who(m['a']), yr=DEEP_YEAR.get(d['oa'], m['y']),
                             v=my_venue(m['v'])))
    for i, v in dk.items():     # a work I cite is named from my own record, never OpenAlex's
        w = cworks[i]
        pool.append(dict(src='fo', id=w['key'], k=v['k'], via=len(v['w']),
                         cites=max(a['m'].get('c') or 0 for a in v['g']), t=w['title'],
                         a=_who(w['authors']), yr=w['year'], v=w.get('venue') or ''))
    pool.sort(key=lambda c: (-c['k'], -c['via'], -c['cites'], c['id']))
    note, hov, K_NAMED, held = [], [], 0, 0
    if pool:
        kmax = pool[0]['k']
        note = [c for c in pool if c['k'] >= kmax - 1]
        if len(note) > NOTE_CAP:
            note = [c for c in pool if c['k'] == kmax][:NOTE_CAP]
        K_NAMED = min(c['k'] for c in note)
        held = sum(1 for a in anc if not (a.get('m') and is_work(a['m'])) and _k(paths[a['oa']]) >= K_NAMED)
        hov = [c for c in pool if c['src'] == 'deep' and c['k'] >= max(5, kmax - 3, K)][:HOVER_CAP]

    # ---- placement: inside the spread of the studies that reach it; position never encodes strength
    stars, wp = list(sxy.values()), list(wxy.values())

    def dstar(p):
        return min(math.hypot(p[0] - q[0], p[1] - q[1]) for q in stars)

    def far(p):                 # room for a hover target: clear of stars and of my own works
        return dstar(p) >= 18 and min(math.hypot(p[0] - q[0], p[1] - q[1]) for q in wp) >= 8

    def place(d, tries=4, ok=None):
        P = [sxy[s] for s in d['S']]
        n = float(len(P))
        cx, cy = sum(p[0] for p in P) / n, sum(p[1] for p in P) / n
        spread = math.sqrt(sum((p[0] - cx) ** 2 + (p[1] - cy) ** 2 for p in P) / n)
        p = (cx, cy)
        for i in range(tries):
            key = d['oa'] if i == 0 else '%s#%d' % (d['oa'], i)
            a, r = 2 * math.pi * _h(key, 'da'), LAM * spread * math.sqrt(_h(key, 'dr'))
            p = (cx + r * math.cos(a), cy + SQ * r * math.sin(a))
            if dstar(p) >= STAR_CLEAR and (ok is None or ok(p)):
                return p
        if ok is not None:
            return None
        q = min(stars, key=lambda s: math.hypot(p[0] - s[0], p[1] - s[1]))
        dd = math.hypot(p[0] - q[0], p[1] - q[1])
        u = ((p[0] - q[0]) / dd, (p[1] - q[1]) / dd) if dd else (1.0, 0.0)
        return (q[0] + u[0] * STAR_CLEAR, q[1] + u[1] * STAR_CLEAR)   # deterministic push out

    hid, named, pts = {c['id']: c for c in hov}, [], []
    for d in drawn:
        c = hid.get(d['oa'])
        p = place(d, 16, far) if c else None
        if p:
            named.append(dict(x=int(round(p[0])), y=int(round(p[1])), t=c['t'], a=c['a'], yr=c['yr'],
                              v=c['v'], k=c['k'], w=sorted(widx[x] for x in d['via'])))
        else:                   # includes a named candidate with no clear spot: drawn, unnamed
            p = place(d)
            pts.append((int(round(p[0])), int(round(p[1]))))
    allp = pts + [(n['x'], n['y']) for n in named]
    M = 10                      # room for the haze's soft edge
    x0, y0 = min(x for x, _ in allp) - M, min(y for _, y in allp) - M
    x1, y1 = max(x for x, _ in allp) + M, max(y for _, y in allp) + M

    names = ['<i>%s</i> (%s, %s)' % (html.escape(_short(c['t'])), c['a'], c['yr']) for c in note]
    pct = [100.0 * a / b for a, b in tr.values() if b]
    n = len(ids)
    tok = {'__N_TRACED__': n_traced, '__N_PAIRS1__': len(cpairs), '__N_PAIRS__': n * (n - 1) // 2,
           '__N_PAIRS2__': sum(v >= T_PAIR for v in pairs.values()), '__T_PAIR__': T_PAIR,
           '__K_DRAW__': K, '__K_NAMED__': K_NAMED,
           '__TRACED_MIN__': int(round(min(pct))), '__TRACED_MAX__': int(round(max(pct))),
           '__DEEP_NAMED__': ((', '.join(names[:-1]) + ' ' + T.MAP_DEEP_LIST_AND + ' ' + names[-1])
                              if len(names) > 1 else ''.join(names))}
    log = ('deep sky: K_DRAW=%d, %d drawn (%d named on hover), study pairs %d at the first step, %d at %d+ '
           'one step back, traced %d/%d (%d%%..%d%%)\n  note:  %s\n  hover: %s\n  held back (unverified, '
           'reach >= %d): %d' % (
               K, len(allp), len(named), len(cpairs), tok['__N_PAIRS2__'], T_PAIR, n_traced, len(cworks),
               tok['__TRACED_MIN__'], tok['__TRACED_MAX__'],
               '; '.join('%s %s (%d%s)' % (html.unescape(c['a']), c['yr'], c['k'], ', mine' if c['src'] == 'fo'
                                            else '') for c in note),
               '; '.join('%s %s (%d)' % (html.unescape(x['a']), x['yr'], x['k']) for x in named),
               K_NAMED, held))
    return dict(js={'b': [x0, y0, x1 - x0, y1 - y0], 'p': [v for x, y in pts for v in (x - x0, y - y0)]},
                named=named, dk={i: {'k': v['k'], 'w': v['w']} for i, v in dk.items()}, tr=tr,
                tok={k: str(v) for k, v in tok.items()}, note=note, held=held, log=log, ongoing=ongoing)


if __name__ == '__main__':      # dry run
    import sys
    sys.dont_write_bytecode = True
    import citelayout as CL
    from projects import PROJECTS
    works = json.load(open(os.path.join(HERE, 'works.json'), encoding='utf8'))
    cited = {c for w in works for c in w['cited_by']}
    studies = [p for p in PROJECTS if p['id'] in cited]
    sxy, wxy, works, _ = CL.layout(studies, works, box=(CL.W, CL.H))
    r = build(works, sxy, wxy, CL.coupling(studies, works), [p['id'] for p in studies])
    print(r['log'] if r else "deep sky off: today's map")
