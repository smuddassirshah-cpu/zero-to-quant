# graphs-dp level 2: performance task

`homework-2.json`, `h-cheapest-count`, item 9 of 9. Kind `code` (Python).

Matched objective: l7-dijkstra "Implement Dijkstra’s algorithm with a heap."

Task: the cheapest fee from `src` to `dst` and the number of routes that cost it, `(None, 0)` when unreachable. The course never counts cheapest routes.

Tests: 11 hidden, 1 example. Eight planted slips first fail their byKey value test: counting arrivals or re-pushing a tie (2), no reset on a cheaper cost or fixing a venue when first reached (3), a stale entry expanded again (5), two-way links or `inf` (7), a `KeyError` on an unseen `dst` (8). A list-scan Dijkstra passes, in CPython and in Pyodide (scratch `solution` swap). Listing every route fails only the ladder (358,584,264,000 routes), by time.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/graphs-dp python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/graphs-dp-2-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set graphs-dp/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed.

Freshness grep: routes, ties, count, cheapest, `count_cheapest`; `fresh-check --file`: 0 hits.

Overlapping screens: l7-dijkstra screens[4] (`dijkstra`, stale skip), [5] (recording on pop) and [9] (`slowest_arrival`); new: the route count, ties, resetting on a cheaper cost.
