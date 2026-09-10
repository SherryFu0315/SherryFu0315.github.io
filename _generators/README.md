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

## Changing the words

The `.html` files are generated. Editing them directly works until the next
build, which overwrites the lot. Edit the source instead:

| To change | Edit |
|---|---|
| Any sentence on a page — headlines, paragraphs, buttons, questions | `_generators/words.py` |
| A study's title, authors, status, description, image | `_generators/projects.py` |
| The publications list, the credits page | `publications/index.html`, `credits/index.html` — these two are hand-written and safe to edit directly |

Then double-click **Preview site.command** in the main folder. It rebuilds and
opens the site in a browser, and if something is wrong it says which file and
which line.

`words.py` holds 147 sentences, grouped by page, each with a comment saying
where it appears. It was extracted from the templates in one pass that was
verified to leave every generated page byte-identical, so it is a pure
relocation of the text — no wording was changed in the move.

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

`works.json` is the parsed reference lists of 13 pieces of work — 752 distinct
works, 29 of them reached by more than one study. `extract_refs.py` pulls the
reference block out of each `.docx`; the published book chapter came from its
PDF instead, where indentation varies per page, so entries are split on the
"Surname, A." citation pattern rather than on indent. A parsing pass then turned
five different citation styles into structured records with a shared matching
key. It is committed, so the map rebuilds without needing the manuscripts.

Two studies are deliberately absent: EduBot and the robotic-surgery work have no
manuscript to read a reference list from.

### Unfinished: the second hop

First-order coupling is thin — two of these studies rarely cite the *same* paper,
because they sit in different literatures. But they do rest on the same
foundations. `resolve_oa.py` looks each cited work up on OpenAlex and pulls that
work's own reference list; `secondorder.py` then finds the ancestors several
studies share.

From the 155 works resolved so far (21%), the difference is large:

| | first order | second order (21% sample) |
|---|---|---|
| distinct works | 752 | 8,298 |
| shared by 2+ studies | 32 | 1,351 |
| shared by 3+ studies | — | 537 |
| *Detecting AI Errors* ↔ the JMIS paper | 6 | 610 |

First-order coupling links 32 pairs of studies; second-order coupling links all
10 of the studies resolved so far to each other.

**This run is incomplete** — 171 of 752 works. To carry on, double-click
**Finish the citation map.command** in the main folder any time after the
allowance resets. It checks first and says how long is left rather than
half-running, picks up from the cache, and stops on its own before the day's
budget is gone.

The allowance is **1000 requests a day, per IP, resetting at midnight UTC**, and
it is not raised by identifying yourself — `OA_MAILTO` buys a much better rate
per second, nothing more. Finishing needs about 640 lookups plus roughly 120
batched calls for the ancestors' titles, so one clean day is enough.

`OA_MAILTO` is read from `_generators/.oa_mailto`, which git ignores: the
address goes to OpenAlex, not into a public repository.

Or by hand:

```bash
cd ~/Documents/website/_generators
OA_MAILTO=you@example.com python3 resolve_oa.py   # resumable
OA_MAILTO=you@example.com python3 secondorder.py  # -> secondorder.json
```

`oa_cache/` is gitignored (hundreds of tiny files) and is the resume point, so
re-running only fetches what is still missing. What remains is about 640 lookups
for the works plus roughly 120 batched calls for ancestor metadata — one day's
allowance, with room to spare.

`OA_MAILTO` puts the request in OpenAlex's "polite pool", which is their
documented way of identifying a caller. It buys a much better per-second rate;
it does not raise the daily cap. Without it the anonymous pool throttles to
roughly one request every four seconds, which the script falls back to on its
own.

Two things to keep in mind if this is ever rewritten:

- A 429 is a transient failure, never an answer. The first version cached
  rate-limited lookups as "no such work", which is why it reported a 14% match
  rate against a real rate of about 90%. `get()` now returns `_error` for 429/503
  and `resolve()` refuses to cache those.
- Semantic Scholar is not a substitute. Publishers elide the `references` field
  for exactly the closed-access IS journals this work cites.
- A 429 whose `Retry-After` is most of a day is not a blip either. It is the
  daily allowance running out, and the first version simply slept on it — which
  from the outside is indistinguishable from a hung process. Anything over five
  minutes now ends the run with a message saying when it resets.
- A rejected request costs the same as a served one. The first version retried a
  429 six times per lookup, so once the budget got tight it spent what was left
  learning the same thing six times over — 41 works resolved out of a thousand
  requests. It now watches `X-RateLimit-Remaining` on every answer and stops
  with 25 to spare, which is what makes tomorrow's run start from a clean point.
