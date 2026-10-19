# Tennessee Titans | Performance Study

A static interactive data-journalism website comparing the Tennessee Titans' regular-season performance on either side of November 18, 2022. **Analysis cutoff: October 19, 2026.**

## Open and share

### Quickest option: standalone HTML

Open `titans_performance_standalone.html` (included in the release ZIP root) in a modern browser. The game data, CSS and JavaScript are embedded. It runs without a server, login, or API. An internet connection is optional for the web fonts; fallback fonts remain available offline. Downloads in the standalone edition are generated from embedded data.

You can send the HTML file as an attachment, but some messaging apps block HTML attachments. For the easiest phone experience, publish the website and send a normal link.

### GitHub Pages (recommended)

1. Create a public GitHub repository, for example `titans-performance-study`.
2. Upload the **contents of the `titans_performance/` directory** to the repository root, including `index.html`, `scripts/`, `styles/`, and `data/`.
3. Open **Settings → Pages** and select **Deploy from a branch**, using `main` and `/ (root)`.
4. Save and wait for GitHub to show the publication URL (usually `https://YOUR-USERNAME.github.io/titans-performance-study/`).
5. Visit the link on desktop and mobile, test the date-sample toggle, select a game and view Analyst mode.

The built-in share control copies or shares the current URL, including comparison mode, highlighted season and selected game. The site is static and does not collect analytics.

### Local modular development

```bash
cd titans_performance
python -m http.server 8000
```

Then visit `http://localhost:8000/`. Alternatively, open `index.html` directly in a modern browser; the files are local ES modules, so a local server is more reliable for development.

## Features

- Executive briefing and Analyst detail view
- Equal calendar windows and matched game-count comparison
- All 125 eligible regular-season results plotted individually
- Hover, click, focus, and touch-friendly game inspection
- Losing-streak, one-score, division, home and away filters
- Linked interactive cumulative-win chart and winning-percentage mode
- Eight game-result comparison metrics, per-season win/loss strips
- Exploratory tagged-play analysis with explicit coverage warning
- PDF via browser print, JSON and CSV downloads
- Deep links to selected views through query parameters
- WCAG-oriented keyboard, focus and reduced-motion support

## Source files

These user-uploaded source files are consumed by the reproducible build script:

- `2010-2026_scores.csv`
- `2018_plays.csv` through `2026_plays.csv`

The raw files are **not** redistributed in this release, since they include league-wide data and descriptions. The included `data/games.json` and `data/games.csv` contain only the game-level fields used by the site; data volumes are compact. See `METHODS.md` for the exact field definitions.

To rebuild from the originals (Python and pandas required):

```bash
python scripts/build_data.py --input /path/to/uploaded/csvs --output data
python scripts/bundle_standalone.py
node --test tests/validation.test.mjs
```

The build script automatically updates `scripts/data.js` when an adjacent `scripts/` directory exists, so the website and source data remain synchronized. Rebundle the standalone HTML after rebuilding.

## Known scope boundaries

- The source scores CSV had the October 18, 2026 Tennessee win at Indianapolis listed as `TBD`. Only this result was supplemented, with a link to the [NFL game center](https://www.nfl.com/games/titans-at-colts-2026-reg-6). Final: TEN 26, IND 20.
- The uploaded 2026 play file ends at Week 5. The Week 6 outcome appears in all final-score analyses but not play-level signals.
- PBP-derived run/pass/sack values are **outcome-tag counts, not official NFL totals**. Plays coded as a touchdown, penalty, or other terminal label may not be counted as passes or runs.
- Playoff appearance and AFC South title figures are season-level context, excluded from regular-season game records. Division title metadata uses 2020/2021 season outcomes.
- The event date is a **chronological marker**, not evidence of causality.
- This is an independent study, unaffiliated with the Tennessee Titans or NFL. No logos or trademarked graphics are embedded.

## Files

- `index.html`: modular entry page
- `styles/`: type, layout, print rules
- `scripts/app.js`: interface state, charts, filters, exports
- `scripts/calculations.mjs`: reusable metric calculations
- `scripts/data.js`: embedded production dataset module
- `scripts/build_data.py`: raw CSV normalization and validation
- `scripts/bundle_standalone.py`: generate one portable HTML file
- `data/games.csv` and `.json`: normalized games
- `data/validation.json`: provenance, corrections, coverage and summary
- `tests/validation.test.mjs`: data assertions
- `METHODS.md`: definitions and comparison boundaries
- `QA_REPORT.md`: implemented and tested behavior versus limitations

## Design

Design direction selected: **Experimental Editorial Atlas**, moderated by Swiss statistical grids and executive clarity. Fonts: Newsreader, Instrument Sans, IBM Plex Mono (Google Fonts with system fallbacks). Colors are reserved for meaning. No external UI framework or JavaScript visualization library is required.
