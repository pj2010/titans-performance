# Quality-assurance and release report

Release snapshot: October 19, 2026. Test environment: Node.js 22, Python, Chromium via Playwright, loaded from embedded standalone HTML content. Font-network requests were removed **for the offline screenshot/interaction test**; the distributed website uses Google Fonts with system fallbacks.

## Verified programmatically

- [x] 125 unique completed regular-season games within the date windows.
- [x] Records: 61 games / 40–21 before, 64 games / 13–51 after.
- [x] Normalized score sums: before 1,547 for and 1,358 against; after 1,089 for and 1,608 against.
- [x] Tennessee 2026 Week 6 correction included once, with official source reference.
- [x] 124 of 125 included games matched to uploaded play-level files.
- [x] No duplicate selected game keys found.
- [x] Game margin and one-score indicators reconcile with final scores.
- [x] Game-count comparison produces 61 vs. 61 selected games.
- [x] Cumulative plotted wins reconcile with headline win counts.
- [x] Per-season matrices include each game exactly once.
- [x] Automated Node assertions pass (`node --test tests/validation.test.mjs`).

## Browser interactions tested in Chromium

- [x] JavaScript completes without uncaught page errors in tested paths.
- [x] All 125 game squares render at 1440, 768, 390 and 375 CSS pixel widths.
- [x] Switching to equal games displays a 61-game post sample.
- [x] Selecting a game reveals the correct opponent, score, date and context.
- [x] Analyst mode reveals additional analytical content.
- [x] Division filter dims nonmatching games; reset restores all.
- [x] Cumulative graph switches into winning-percentage mode.
- [x] Season selection visually emphasizes the selected season.
- [x] No document-wide horizontal overflow at tested widths.
- [x] Desktop and mobile screenshot reviews performed.

## Design evaluation

Three directions assessed conceptually (not three separately coded prototypes): Swiss Research, Experimental Editorial Atlas, and Ownership Briefing. The production site implements the Experimental Editorial Atlas, using executive reading order and Swiss chart discipline. It avoids repeated cards, gradients, decorative objects and framework-specific widgets. The game chronology is the signature component.

## Known limitations / checks not performed

- Historical score values were checked for internal consistency, **not** independently cross-checked one-by-one against every NFL game center.
- Automated WCAG auditing and a full screen-reader evaluation were **not** performed. Keyboard controls and labels were implemented and some were exercised in-browser.
- Automated deployment to GitHub Pages was **not** performed; a live public URL does not yet exist.
- Real-device Safari / iPhone touch behavior was **not** independently tested. Mobile viewports were simulated in Chromium.
- Native browser print-to-PDF and Web Share behavior were implemented but have not been independently exercised across all browsers.
- Proprietary fonts were not embedded or redistributed; design uses open Google Fonts where network access is available.
- Exploratory play-tag signals are source-label counts, **not official NFL efficiency metrics**.
- Browser tests used the standalone embedded edition; modular entrypoint was checked for source integrity but full cross-browser regression remains recommended after publication.

## Release conclusion

The project is a functional **release candidate**, with a verified score-based analysis, passing calculation tests and exercised primary browser interactions. Treat independent score verification, mobile Safari review, screen-reader testing and live deployment as remaining production-hardening activities—not as completed checks.
