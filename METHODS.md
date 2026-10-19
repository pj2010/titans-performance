# Methodology / statistical definitions

## Periods

- **Chronological marker:** November 18, 2022 (Todd Downing DUI arrest; the preceding game was Tennessee's November 17 win over Green Bay).
- **Equal calendar windows:** December 18, 2018–November 17, 2022 and November 18, 2022–October 19, 2026. Calendar endpoints establish inclusion, while the visible game range shows the first and last completed games.
- **Matched game count:** last N eligible pre-marker games vs. first N post-marker games, where N is the smaller total. At this cutoff, N = 61. The sampled post-marker window therefore ends before October 19, 2026.
- **Regular season only:** Preseason, byes, pending games and postseason are excluded from the game-result comparison.
- **Partial seasons:** December 2018 and split 2022 rows and 2026 through Week 6 are explicitly marked.

## Calculation definitions

- `games`: number of completed regular-season games in the comparison sample.
- `wins`, `losses`, `ties`: counts of scored game outcomes.
- `winPct`: `(wins + 0.5 * ties) / games * 100`.
- `winsPer17`: `(wins + 0.5 * ties) / games * 17`.
- `pointsForPerGame`: sum of Tennessee's final points / games.
- `pointsAgainstPerGame`: sum of opponents' final points / games.
- `marginPerGame`: `(pointsFor − pointsAgainst) / games`.
- `divisionRecord`: record against IND, JAX, HOU.
- `oneScore`: games decided by 8 points or fewer, including ties.
- `home/away`: whether Tennessee was home or away in the score record.
- `longestLossStreak`: maximum consecutive losses in chronologically ordered comparison games; sequences are cut at the sample boundaries, not automatically at calendar-season boundaries.
- `lossesBy9`: losses by 9 points or more.
- `seasonBreakdown`: games grouped by season and before/after period. A 17-slot grid is used for visual consistency, and blank slots represent games outside the displayed segment, not future scheduled games.

## Game dates

Source fields are season, week, month and day, without an explicit year in `GameDate`. January–March games are assigned to `Season + 1`, other months to `Season`. Regular-season games are validated against the cutoff. Only rows where Tennessee appears as home/away and `Week` is exactly `WEEK N` are counted.

## Source correction

One score was not yet marked final in the upload:

| Game | Uploaded status | Official confirmation | Treatment |
|---|---|---|---|
| 2026 Week 6, TEN at IND, Oct 18 | TBD, no score | [NFL Game Center: TEN 26, IND 20](https://www.nfl.com/games/titans-at-colts-2026-reg-6) | Included in normalized game results; play file coverage missing |

Source attribution for all other game scores: user-uploaded `2010-2026_scores.csv`. The upload's provenance and independent verification of each individual historical score are outside the scope of the automated checks.

## Play-level data

The supplied play files have 16 fields including team, week, possession, play outcome and descriptions. Records are matched to games by `(season, week, away, home)`. In 2026, only five Tennessee regular-season games have play rows, while six completed results are in the score dataset.

Exploratory counts use exact `PlayOutcome` label patterns:

- Tagged runs: `<signed integer> Yard Run` while Tennessee has possession.
- Tagged passes: `<signed integer> Yard Pass`, `Pass Incomplete`, or `Interception` while Tennessee has possession.
- Tagged sacks allowed: `Yard Sack` or `Sack` while Tennessee has possession.
- Tagged sacks made: same tags while the opponent has possession.

These are **not official passing attempts, rushing attempts, sacks, offensive yards, EPA, success rate or drive efficiency**, because play outcomes such as touchdowns, penalties and special-teams plays can be coded differently. The interface limits these signals to the Analyst section, reports play-file coverage and discloses the definitions.

## Titles and postseason

Postseason appearances and records were identified from postseason rows of the source score file. AFC South titles in 2020 and 2021 are maintained as season metadata. They are contextual and are not recalculated when the regular-season sample count changes.

## Interpretation limitations

This descriptive analysis is not causal. The teams' personnel, leadership, schedules and opponents changed during the compared periods. Statistical differences do not establish that the November 18, 2022 incident caused subsequent outcomes. The dates are a reproducible split for exploratory comparison. More rigorous attribution would require additional covariate data and an explicit identification strategy.
