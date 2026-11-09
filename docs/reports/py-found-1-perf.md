# py-found level 1: performance task

- `homework-1.json` item 10 of 10, `h-overnight-gaps`, appended (cap 12, nothing converted). Kind `code`, difficulty 4, pace 900 s, skills `pf-idioms`, `pf-types`.
- Matched objective (l4): "Write list comprehensions, with and without a condition". The only verb-rule objective in the level.
- Product: `overnight_gaps(days, limit)` from a one-line stub. It returns `(gaps, flagged)`: every open against the previous close (a comprehension without a condition), and the dates gapping more than `limit` either way (one with a condition).
- Tests: 10 hidden, 1 example. Twelve planted slips each fail: same-day close, divide by the open, previous open, no `abs`, flag the day before, `range(len(days))` wrap to `days[-1]`, a dropped last gap, `>=` (test 5, zero gap at limit 0), per cent, `days[0]` on an empty list (test 9), print not return, a loop with `.append` (test 10). Starter fails 10 of 10.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; the expected "py-found/L1: has a performance task, remove from perf-pending" warning.
2. `VOICE_BASE=app/content/courses/py-found python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script `python3 -I docs/reports/py-found-1-perf-numbers.py`: exit 0, 0 failures. Route A the solution, route B an index loop, route C exact fractions for every gap.
4. Playthrough `node tools/playthrough.mjs --set py-found/homework-1 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed, performance starter fails. Shots at 1280 and 440 px read cleanly.

Freshness: `fresh-check.mjs --file` no hit on item 10. Grep: overnight, gap, open, `abs(`, `zip(`, `days[1:]`.

- Overlapping screens: l3 screen 7 (`daily_returns`, `zip(closes, closes[1:])`), l4 screens 2 to 4 (a filter comprehension, `losing_days`), review-1 `r-up-days` and homework-1 `h-k-day-returns`, `h-csv-best-worst` (the later day owns the move). New: two fields of neighbouring records, a two-way flag through `abs` and `limit`, both lists returned.

Backlog: 0 bullets.
