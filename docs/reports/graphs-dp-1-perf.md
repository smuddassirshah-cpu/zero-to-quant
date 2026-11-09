# graphs-dp level 1: performance task

`homework-1.json`, `h-split-desks`, item 9 of 9 (added). Kind `code` (Python).

Matched objective: l2-level-by-level "Implement breadth-first search with a queue."

Task: split desks into two groups across every conflict, the first desk of each linked set in group 0, `None` on an odd loop. The course never two-colours a graph.

Tests: 12 hidden, 1 example. Nine planted slips each first fail the value test byKey names: one-way storage (2), no clash check or `False` (3), first set only (4), lone desks dropped (5), given order (6), non-parent clash (7), edge greedy (8), recursion on the 3,000 chain (10). List and stack variants pass; in Pyodide (scratch `solution` swap) the list queue passes and recursion fails test 10.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/graphs-dp python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/graphs-dp-1-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set graphs-dp/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed.

Freshness grep: bipart, colour, two groups, conflict, `split_desks`; `fresh-check --file`: 0 hits.

Overlapping screens: l2-level-by-level screens[4] (`bfs`, `deque`) and [5], l3-going-deep screens[7] and [8] (`count_components`), l1-nodes-and-edges screens[6]; new: parity groups, the clash test, the first-desk rule, `None`.
