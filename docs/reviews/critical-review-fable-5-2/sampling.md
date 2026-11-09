# Sampling list: critical review, 9 Nov 2026

Reviewed at HEAD 7078fac (census: 1,214 lessons, 279 levels, 49 exams, 35 drills, 200 bank items).

## Read as a learner (rendered with `scripts/render.py`, answers checked by hand)

Lessons, whole or nearly whole (12 of 1,214, 1.0%):
number-sense/l1-what-a-fraction-measures, equations/l3-opening-brackets, first-python/l1-calculator (Stage 0);
limits/l2-computing-limits, markov/l13-balanced-flows, micro/l9-both-sides (Stage 1);
stat-learning/l4-nearest-neighbours (Stage 2);
ito/l4-gbm, mm-games/l13-full-game, coding-int/l3-window-maximum, research-int/l11-framing-the-question, recruiting/l12-reasoning-aloud (Stage 3 and interview).

Sets: conditional/homework-2 (10 items, including the performance task `h-two-filters`; every number recomputed).

Lesson titles only: puzzles, mm-games, mental-pressure, brainteasers, game-theory, recruiting, mental.

## Sat or attempted

- `mock-oa-sig`: all 17 items attempted blind (`render.py --blind`); 17 of 17 keys agree with my working.
- `topic-1.5`: items 0 to 25 attempted blind; all keys agree (items 26 to 29 read, not worked).
- `mock-superday-trader`: structure and the first probability items read and recomputed; `mock-superday-research`: papers 1 to 3 read, four items worked.
- `mock-video`, `mock-oa-code` (pool drills `oa-rain-water`, `oa-critical-path`), `stage-0` (stems of papers 1 and 2), bank `behavioural-1`, `market-making-2`: read.
- Playthrough with `--local-cdn`: `topic-1.5` 30 of 30, `stage-0` 52 of 52, `mock-oa-sig` 17 of 17, `mock-superday-trader` 24 of 24, `mock-oa-code` (see log line in the review), all green.

## Screens looked at

Fresh-profile walk (`scripts/walk.mjs`) at 1280 and 440 px: setup, Today, Learn, Prepare, Review, You, two course maps, five exam start or lock cards, bank, drill list, one drill, one homework. Lesson screenshots at both widths from the playthrough for 7 lessons (number-sense l1, equations l3, functions l6, trig l4, first-python l1, conditional l8, mm-games l6, ito l4); about 14 opened and judged. The ones cited are in `shots/`.

## Tools run

`census.mjs`, `closure.mjs --role` (trader, researcher, developer, strats, derivatives), `readiness-sums.mjs` (OK), `fresh-check.mjs --all-exams` (23 hits, 7 in sample files), counts scripted inline (minutes, widget and canvas mix, set sizes).

## Not done (limits of this review)

- No complete route was read end to end. The trader route is 432 lessons; I read its first lesson and one lesson in each of six of its courses.
- Stage 2 is one lesson. No lesson of puzzles, brainteasers, game-theory, mental-pressure or systems was read; they were judged through mock items and titles.
- `validate.mjs` was not run (it rewrites `manifest.json`; this is a read-only review). `rubric-passes.mjs` and `perf-reports.mjs` were not run.
- No drill was solved in the browser. Explanation-sheet screenshots were taken for five lessons only (the `--why` run was too slow).
