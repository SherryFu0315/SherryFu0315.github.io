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

First-order coupling is thin. Two of these studies rarely cite the *same* paper,
because they sit in different literatures. But they do rest on the same
foundations. `resolve_oa.py` looks each cited work up on OpenAlex and pulls that
work's own reference list; `secondorder.py` then finds the ancestors several
studies share.

From the 308 works resolved so far (41%), the difference is large:

| | first order | second order (41% resolved) |
|---|---|---|
| distinct works | 752 | 17,448 |
| shared by 2+ studies | 32 | 2,399 |
| shared by 3+ studies | 9 | 889 |
| study pairs linked | 32 of 78 | 78 of 78 |
| *Detecting AI Errors* and the JMIS paper | 6 | 610 |

**This run is incomplete**: 308 of 752 works. Every study now has part of its
reference list resolved, from 10% to 95%, but none of the low ones is
done. To carry on, double-click **Finish the citation map.command** in the main
folder once a day. It checks first and says how long is left rather than
half-running, picks up from the cache, and stops on its own before the day's
credits are gone. When it is done it rebuilds the
research map, prints the works the map names so a wrong record can be caught,
and asks before publishing: type y to put the update on the website, or press
return to keep it on this computer. It only ever publishes the data files and
the map page, and not at all while the site's own source files have edits.

OpenAlex meters **credits**, not requests: 1000 a day for free, refilled about
once a day (the `X-RateLimit-Reset` header on any response says exactly when).
What a request costs depends on its kind, measured September 2026 from
`X-RateLimit-Credits-Used`:

| request | credits |
|---|---|
| title search (`search=` or `filter=title.search:`) | 10 |
| lookup by OpenAlex ID or DOI, up to 50 in one request | 1 |

`works.json` holds only authors, year, title and venue, with no DOIs, so every
lookup here is a title search: 10 credits, or 20 when the first query finds
nothing and the fallback runs. The last full run averaged about eleven credits
a work, so a day covers roughly ninety works, and the 409 still to do need
about 5 more days. The ancestors' names are cheap by comparison, fifty
to a credit.

Because a day only covers part of the list, `resolve_oa.py` takes works from
each study in turn rather than in file order. `works.json` is grouped by study,
and walking it top to bottom spent the first days on four papers and left nine
with nothing.

`OA_MAILTO` is read from `_generators/.oa_mailto`, which git ignores: the
address goes to OpenAlex, not into a public repository. It puts requests in
OpenAlex's "polite pool", their documented way of identifying a caller, which
buys a much better rate per second. It does not add credits.

Or by hand:

```bash
cd ~/Documents/website/_generators
OA_MAILTO=you@example.com python3 resolve_oa.py   # resumable
OA_MAILTO=you@example.com python3 secondorder.py  # -> secondorder.json
```

`oa_cache/` is gitignored (hundreds of tiny files) and is the resume point, so
re-running only fetches what is still missing. Without `OA_MAILTO` the
anonymous pool throttles to roughly one request every four seconds, which the
script falls back to on its own.

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
- A search is not a lookup. OpenAlex prices by credit, and a title search costs
  ten times a lookup by ID. The first run under that pricing spent a whole day
  on about ninety works and then reported the day as done. Read
  `X-RateLimit-Credits-Used` on a response before assuming what anything costs;
  the double-click script's own "is there budget today?" check used to be a
  title search, and spent 10 credits just to ask.

## The haze: one step back

`deepsky.py` turns `secondorder.json` into the pale haze behind the halos in
the literature view. It draws a work only when at least three studies reach
it, each through a different paper of their own. A work two studies reach only
through one paper they both cite is left out, because the gold star already
shows that link. It never moves a study and never reads the coupling weights.
Every number in its copy is computed at build time, and without usable
OpenAlex data the page is byte-identical to the one without the layer.

```bash
cd ~/Documents/website/_generators
python3 -B deepsky.py     # what would be drawn and named, without building
```

Two lists near the top are for correcting OpenAlex by hand. `DEEP_DENY` keeps a
record from ever being named. `DEEP_YEAR` fixes a year where OpenAlex dates a
paper by when it first appeared online rather than by its volume, which is how
the reference lists date it.
