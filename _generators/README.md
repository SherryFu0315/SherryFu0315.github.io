# Generators

The site is static HTML committed to this repo — GitHub Pages serves it directly
(`.nojekyll`, no build step on their side). These scripts are what *writes* that HTML.

```bash
cd _generators
python3 build.py          # -> index.html, research/index.html
python3 build_universe.py # -> universe/index.html
python3 build_pages.py    # -> join/index.html, teaching/index.html
```

`projects.py` is the single source of truth for every study: title, authors,
status, image, links, and its cell in the two-axis map. Edit it, re-run the three
builds, commit the regenerated HTML.

`publications/index.html` and `credits/index.html` are hand-edited, not generated.

Requires system Python 3 (`/usr/bin/python3`) — the Homebrew 3.14 on this machine
has a broken `pyexpat` and cannot parse XML.

## Previewing locally

Absolute paths (`/assets/...`) need a server, so opening the files directly will
not style correctly:

```bash
python3 -m http.server 8731 --directory ~/Documents/website
# then http://localhost:8731/
```

## The literature map

`universe/index.html` holds two arrangements of the same stars. The two-axis one
comes from `projects.py` and `constellations.py`. The literature one comes from
`works.json`, laid out by `citelayout.py`.

The public label is deliberately not "citation sky": read quickly, that names the
wrong thing — the author's own citation count — when the map is about the
opposite, how small a part of a field any one body of work is.

`works.json` is the parsed reference lists of twelve manuscripts — 640 references,
608 distinct works, 25 of them cited by more than one study. It was built by
`extract_refs.py` (pulls the reference block out of each `.docx`) followed by a
pass that parsed the five different citation styles into structured records. It is
committed, so the map rebuilds without needing the manuscripts.

### Unfinished: the second hop

First-order coupling is thin — two of these studies rarely cite the *same* paper,
because they sit in different literatures. But they do rest on the same
foundations. `resolve_oa.py` looks each cited work up on OpenAlex and pulls that
work's own reference list; `secondorder.py` then finds the ancestors several
studies share.

From the 85 works resolved so far (14%), the difference is large:

| | first order | second order (14% sample) |
|---|---|---|
| distinct works | 608 | 4,504 |
| shared by 2+ studies | 25 | 1,087 |
| *Detecting AI Errors* ↔ the JMIS paper | 6 | 610 |

**This run is incomplete.** OpenAlex's anonymous pool allows 1000 requests a day
and the first attempt exhausted it. To finish:

```bash
cd ~/Documents/website/_generators
python3 resolve_oa.py     # resumable — oa_cache/ holds every completed lookup
python3 secondorder.py    # -> secondorder.json
```

`oa_cache/` is gitignored (hundreds of tiny files) and is the resume point, so
re-running only fetches what is still missing. Budget roughly 550 requests.

Two things to keep in mind if this is ever rewritten:

- A 429 is a transient failure, never an answer. The first version cached
  rate-limited lookups as "no such work", which is why it reported a 14% match
  rate against a real rate of about 90%. `get()` now returns `_error` for 429/503
  and `resolve()` refuses to cache those.
- Semantic Scholar is not a substitute. Publishers elide the `references` field
  for exactly the closed-access IS journals this work cites.
