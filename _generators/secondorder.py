# -*- coding: utf-8 -*-
"""
Second-order citation structure.

First-order coupling (do two of my papers cite the same work?) turned out to be
thin: 25 shared works out of 608. That is honest but it under-states how connected
the work is, because two literatures can rest on the same foundations without ever
citing the same paper directly.

So: take every work Xinyu Fu cites, look at what THAT work cites, and ask which
ancestors recur. Those ancestors are the deep sky.

    python3 secondorder.py        # needs oa_level1.json from resolve_oa.py
"""
import json, os, sys, time, urllib.request
from collections import Counter, defaultdict
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
API = 'https://api.openalex.org/works'
UA = 'xinyufu-website-citation-map/1.0'
META = os.path.join(HERE, 'oa_level2_meta.json')


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA,
                                                       'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode('utf8'))
        except Exception:
            if i == tries - 1:
                return {}
            time.sleep(1.2 * (i + 1))
    return {}


def load():
    works = json.load(open(os.path.join(HERE, 'works.json'), encoding='utf8'))
    lvl1 = {r['key']: r for r in json.load(open(os.path.join(HERE, 'oa_level1.json'),
                                               encoding='utf8'))}
    return works, lvl1


def main():
    works, lvl1 = load()
    matched = [w for w in works if lvl1.get(w['key'], {}).get('matched')]
    print('cited works: %d, resolved on OpenAlex: %d (%.0f%%)'
          % (len(works), len(matched), 100.0 * len(matched) / len(works)))

    # ---- ancestors: level-2 id -> which of her studies reach it, and via how many
    #      of her level-1 works
    reach = defaultdict(set)        # oa2 -> {study ids}
    via = Counter()                 # oa2 -> number of level-1 works citing it
    anc_by_study = defaultdict(set)  # study -> {oa2}
    for w in matched:
        refs = lvl1[w['key']]['refs']
        if not refs:
            continue
        for oa2 in refs:
            via[oa2] += 1
            for s in w['cited_by']:
                reach[oa2].add(s)
                anc_by_study[s].add(oa2)

    print('distinct ancestor works (level 2): %d' % len(via))
    print('ancestors reached by 2+ of her studies: %d'
          % sum(1 for k, v in reach.items() if len(v) > 1))
    print('ancestors reached by 3+ of her studies: %d'
          % sum(1 for k, v in reach.items() if len(v) > 2))

    # ---- second-order coupling between her studies
    print()
    print('second-order coupling (shared ancestors between studies):')
    pairs = {}
    ids = sorted(anc_by_study)
    for a, b in combinations(ids, 2):
        n = len(anc_by_study[a] & anc_by_study[b])
        if n:
            pairs[(a, b)] = n
    for (a, b), n in sorted(pairs.items(), key=lambda kv: -kv[1]):
        print('  %-14s %-14s %5d' % (a, b, n))
    linked = set()
    for a, b in pairs:
        linked.add(a); linked.add(b)
    print('studies connected: %d of %d' % (len(linked), len(ids)))

    # ---- fetch metadata for the ancestors worth naming
    hubs = [k for k, v in reach.items() if len(v) >= 2]
    hubs.sort(key=lambda k: (-len(reach[k]), -via[k]))
    print()
    print('fetching metadata for %d shared ancestors...' % len(hubs))
    meta = {}
    if os.path.exists(META):
        meta = json.load(open(META, encoding='utf8'))
    todo = [h for h in hubs if h not in meta]
    SEL = 'id,display_name,publication_year,authorships,cited_by_count,primary_location'
    for i in range(0, len(todo), 50):
        chunk = todo[i:i + 50]
        url = '%s?filter=openalex_id:%s&per-page=50&select=%s' % (API, '|'.join(chunk), SEL)
        for r in (get(url).get('results') or []):
            oid = r['id'].rsplit('/', 1)[-1]
            auth = [(a.get('author') or {}).get('display_name') or ''
                    for a in (r.get('authorships') or [])]
            surn = [a.split()[-1] for a in auth if a]
            loc = (r.get('primary_location') or {}).get('source') or {}
            meta[oid] = {'t': r.get('display_name') or '',
                         'y': r.get('publication_year') or 0,
                         'a': surn[:6],
                         'c': r.get('cited_by_count') or 0,
                         'v': loc.get('display_name') or ''}
        json.dump(meta, open(META, 'w'))
        print('  %d/%d' % (min(i + 50, len(todo)), len(todo)))
        sys.stdout.flush()

    out = {
        'ancestors': [
            {'oa': k, 'by': sorted(reach[k]), 'via': via[k],
             **({'m': meta[k]} if k in meta else {})}
            for k in hubs
        ],
        'coupling2': {'%s|%s' % k: v for k, v in pairs.items()},
        'stats': {'level1_total': len(works), 'level1_matched': len(matched),
                  'level2_total': len(via),
                  'level2_shared2': sum(1 for k, v in reach.items() if len(v) > 1),
                  'level2_shared3': sum(1 for k, v in reach.items() if len(v) > 2)},
    }
    json.dump(out, open(os.path.join(HERE, 'secondorder.json'), 'w'), indent=1)
    print()
    print('wrote secondorder.json — %d named ancestors' % len(hubs))

    named = [a for a in out['ancestors'] if 'm' in a]
    print()
    print('the works the most of her studies rest on:')
    for a in named[:22]:
        m = a['m']
        print('  %d studies · via %-3d refs · %s (%s) — %s'
              % (len(a['by']), a['via'], (m['a'][0] if m['a'] else '?'), m['y'], m['t'][:64]))


if __name__ == '__main__':
    main()
