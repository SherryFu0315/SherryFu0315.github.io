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
