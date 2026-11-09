# algo-think level 2: performance task

`homework-2.json`, `h-split-feed`, item 10 of 10 (added). Kind `code` (Python).

Matched objective: l5-calls-itself "Write a recursive function with a correct base case.".

Task: every split of a spaceless feed into listed tickers (word break). New to the course.

Tests: 12 hidden, 1 example, each sorted. Ten planted slips fail: base case `[]` (1, 2), stop when the rest is a ticker (6), cut never reaches the end (7), first split only (1), longest ticker only (4), duplicates in `listed` (5), shared default list (2), reversed tickers (1), `listed` sorted in place (12), empty feed gives `[]` (2). Brute force over cuts passes: slowest case 0.25 s in Pyodide 0.27.7 (Node).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/algo-think python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/algo-think-2-perf-numbers.py`: exit 0, failures 0.
4. `node tools/playthrough.mjs --set algo-think/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed; no wide display.

Freshness grep: ticker, spaces, split, `startswith`, `split_feed`; `fresh-check --file`: no hit on the new item.

Overlapping screens: l5-calls-itself screens[5] (`sum_list`, `power`) and [9] (`total_pnl`), homework-2 `h-flatten`; new: string cuts, a base case that returns `[[]]`, several branches each kept, duplicate tickers.
