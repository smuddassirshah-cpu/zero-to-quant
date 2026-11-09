# graphs-dp level 3: performance task

`homework-3.json`, `h-fee-trades`, item 9 of 9. Kind `code` (Python).

Matched objective: l13-climbing-stairs "Write a recurrence and fill a table from the bottom up.".

Task: the best profit from trading one share with a fee per round trip, ending flat. The course's tables have one state (stairs, coins); this needs two a day, and greedy fails.

Tests: 11 hidden, 1 example. Five planted slips pass the example and first fail their byKey test: one round trip only (2), the rise-by-rise greedy (3), the table skipping day 0 (4) or the last day (5), `prices[0]` on an empty list (7). The daily greedy, a fee on both legs and a free first share fail the example. An O(n^2) table and a memoised recursion pass in CPython and Pyodide.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/graphs-dp python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/graphs-dp-3-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set graphs-dp/homework-3 --local-cdn <pkgs>`, also `--mobile`: All passed.

Freshness grep: fee, buy, sell, cooldown, round trip, `trade_with_fee`; `fresh-check --file`: 0 hits.

Overlapping screens: l13-climbing-stairs screens[2], [3], [7] (the recipe) and [9] (`min_coins`); new: two states, the fee, ending flat.
