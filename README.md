# Word Alive Bible app

Word Alive Bible Version (WABV): a 66-book Bible reading app with search, bookmarks, highlights, daylight/sepia/night themes and cross references. *Faithful to the Word. Alive in English.*

Single-file web app (vanilla JS, no framework), installable as a PWA. Draft text, under review.

## Layout
- `src/app.html`: app template (placeholders `/*DATA*/`, `/*REFS*/`, `/*HERO*/`, `/*MARK*/`, `/*FAV*/`, `/*ICON*/`)
- `data/bible.json`: WABV text, 66 books
- `data/refs.json`: cross references parsed from each book's Appendix B (authored references only)
- `appendix-b/`: source Appendix B exports per book
- `img/`: hero, mark and icons
- `deploy/`: manifest, service worker, icons for eobibles.com
- `tools/`: `parse_refs.py`, `flatten_refs.py`, `build.py`, `make_deploy.py`

## Build
```
python3 tools/parse_refs.py && python3 tools/flatten_refs.py
mkdir -p dist && python3 tools/build.py      # dist/WordAliveBible.html
python3 tools/make_deploy.py                 # dist/WordAliveBible-deploy.zip
```
Bump the cache name in `deploy/sw.js` on each release.

## Status
- Cross references cover 60 of 66 books. **Missing Appendix B tables: Joel, Jonah, Nahum, Habakkuk, Zephaniah, Malachi.**
- Planned: footnotes, BCLS word studies, reading plans, Play Store and App Store wrappers.
