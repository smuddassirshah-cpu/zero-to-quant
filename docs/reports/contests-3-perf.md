# contests level 3: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/contests/homework-3.json`, item `hw3-due-order`, index 8 (item 9 of 9; nothing converted, the homework had 8).
- Kind `derivation` (longform, empty box, no tags), difficulty 5, skill `cn-patterns`.
- Objective matched: l10 "Prove a greedy choice with an exchange argument." It is the only verb-rule match in L3 (l9 Solve, l11 Enumerate, l12 Apply).
- Task: problem L, one machine, every job ready at 09:00, minimise the worst lateness; the greedy runs jobs in due order. Prove it by exchange (first difference, swap, feasible, no worse, repeat), then name an assumption the proof needs and break the greedy without it. Model: ready times (A 0/5/7, B 5/1/6: 4 against 0; the never-wait rule fails on a second pair, 3 against 0) and total lateness (8 against 5).
- Rubric 1, 3, 2, 2, 2; rows 2 to 5 required (exchange, feasibility, repeat, assumption). `rubric-passes.mjs`: minimal pass rows 2, 3, 4, 5; only row 1 can be left out.
- Fresh: l10 screens 2 and 9 and `hw3-exchange` lay out the exchange for interval scheduling (a set, first meeting swapped), `hw3-writeup` for alert stabbing. New: an order rather than a set, the first-difference swap with the block bound, closing gaps, the ready-time and total-lateness conditions. Grep terms: `deadline`, `lateness`, `due`, `knapsack`, `exchange`, `greedy`, `swap`, `penalty`, `sorted by`. `fresh-check.mjs --file` homework-3: 0 hits.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "contests/L3: has a performance task, remove from perf-pending".
2. `VOICE_BASE=app/content/courses/contests python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/contests-3-perf-numbers.py`: exit 0, 4,779,275 checks, 24 s. Every multiset of 1 to 5 jobs, times 1 to 3, due 0 to 8 (201,375 instances): greedy under every tie order equals the optimum by all orders and by a bitmask DP. Idle never helps (n up to 3, gaps 0 to 3). The swap is replayed on every best order for n up to 4 (152,920 swaps, at most n - 1). Counterexamples by orders and by a start-time grid. Rubric tick sets.
4. `node tools/playthrough.mjs --set contests/homework-3 --local-cdn <pkgs>` with the regenerated manifest, with and without `--mobile`: All passed (2 longform marked by the button). The display equation measures 168 px in KaTeX, inside the 356 px card.

One backlog bullet. No course.json change.
