# alpha level 4: performance task

- `homework-4.json` item 9 of 9, `h-neutral-book`, appended (nothing converted). Kind `code`, difficulty 5, pace 1200 s.
- Objective (l13): "Build a dollar-neutral long-short portfolio from a signal." Preferred to l16's longform note: auto-graded, and tests catch neutrality, gross and look-ahead.
- Product: `split_book(signal, gross)` (distance from each date's median, each side scaled to `gross/2`, cash on an empty side) and `split_pnl` (positions earn the next day).
- 12 tests, 1 example, no timing test. 15 planted bugs each fail first at their byKey test (1 neutrality and gross, 2 weights, 3 missing signal, 4 empty side, 7 look-ahead spy, 8 dates, 9 NaN return).

Overlapping screens: l13 screens 3, 8, 9, 10 lay out rank weights at ±0.5 and next-day holding. New: median centring with per-side scaling, £ gross, empty-side cash, dated £ P&L. `fresh-check.mjs --file`: 0 hits. Grep: median, dollar-neutral, each side, gross, split_.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/alpha python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/alpha-4-perf-numbers.py`: exit 0; two routes agree; starter fails 12 of 12.
4. `node tools/playthrough.mjs --set alpha/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: All passed.

Backlog: 0 bullets.
