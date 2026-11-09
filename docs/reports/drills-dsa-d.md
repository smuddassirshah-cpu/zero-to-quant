# Drills pack `dsa`, sub-pack D (graphs, dp, greedy, backtracking)

Brief: `docs/briefs/drills-1.8.md`, sub-pack D. 15 Python drills, `"pack": "dsa"`, rows appended to `app/content/drills/index.json`.

| id | pattern | difficulty | pace (s) | stdin | hidden tests | course |
| --- | --- | --- | --- | --- | --- | --- |
| `dsa-lift-buttons` | graphs | 1 | 720 | yes | 12 | graphs-dp |
| `dsa-spare-cables` | graphs | 1 | 720 | no | 12 | graphs-dp |
| `dsa-climb-limit` | graphs | 2 | 960 | no | 12 | graphs-dp |
| `dsa-upstream-stations` | graphs | 2 | 900 | no | 12 | graphs-dp |
| `dsa-forced-order` | graphs | 3 | 1260 | no | 12 | graphs-dp |
| `dsa-footpath-slabs` | dp | 1 | 600 | no | 12 | graphs-dp |
| `dsa-stamp-gaps` | dp | 1 | 660 | no | 12 | graphs-dp |
| `dsa-shift-pay` | dp | 2 | 960 | yes | 12 | graphs-dp |
| `dsa-feed-passes` | dp | 3 | 1380 | yes | 12 | graphs-dp |
| `dsa-free-desk-square` | dp | 3 | 1200 | no | 12 | graphs-dp |
| `dsa-kiosk-change` | greedy | 1 | 600 | no | 12 | algo-think |
| `dsa-loop-depots` | greedy | 2 | 1020 | no | 12 | algo-think |
| `dsa-ticker-batches` | greedy | 2 | 900 | no | 12 | algo-think |
| `dsa-split-prices` | backtracking | 2 | 1080 | no | 12 | graphs-dp |
| `dsa-server-loads` | backtracking | 3 | 1500 | no | 12 | graphs-dp |

Mix: five at 1, six at 2, four at 3; three stdin drills (`solve_<slug>(text)`, parsed with `split()`, tests with trailing newlines, blank lines, extra spaces and values wrapped over lines). Ideas covered: one-dimensional BFS on floors, components with a cable count, grid BFS with a one-way climb rule, reverse reachability, topological order (is it unique), DP for ways (2-by-n paving), coins (unmakeable totals), best sum (no three days in a row), passes over sparse days, one two-dimensional table (largest free square), three greedy drills each with a proof line as `notes[0]`, and two subsets searches with pruning. Skills: `gd-graphs`, `gd-traversal`, `gd-paths`, `gd-dp`, `gd-backtrack` (graphs-dp lessons) and `at-greedy` (algo-think l14). Every drill has 2 examples with a `note`, 12 hidden tests (smallest input, a tie or duplicate, a boundary case, and two or three large inputs built inside the `call`) and three `notes` lines.

## Checks

1. `docs/reports/drills-dsa-d-check.py` (scratchpad venv Python): exit 0, 15 drills, 0 errors. For each case it runs the model solution and an independent method: brute force on small inputs (Bellman-Ford style relaxation, union-find, a forward search from every station, every permutation, a real cell-by-cell tiling, every working-day mask, plain recursion over passes, every square, every change choice as a state set, every start depot, every cut set, every cut-point combination, every assignment); on the large ones a different algorithm (layered sets, Dijkstra, SciPy breadth-first order on reversed pipes, DFS post-order plus a Hamiltonian-path test, the Jacobsthal closed form, a big-integer bitset, a rest-day DP, a calendar-day table and a forward three-pointer DP, NumPy 2-D prefix sums with a binary search, prefix-sum argmin, a difference array of spanned cuts, a memoised suffix enumeration, binary search with subset DP). Nine small values are also worked by hand in the script and checked. It also checks the starter fails at least one test (7 to 12 per drill), the difficulty and stdin mix, and that no case uses `setup`.
2. `node tools/validate.mjs`: 0 errors, no warning on any file of this sub-pack.
3. `node tools/playthrough.mjs --drill <15 ids> --local-cdn <pkgs>`: 15 of 15 ok, All passed; again with `--mobile`: 15 of 15 ok, All passed (12 of 12 tests with the model solution, starter fails, on every drill).
4. Voice: `voice-scan.py 35` on the 15 files: 0 sentences over 35 words, 0 explanations over three sentences; no exclamation marks or em-dashes in prose (the only `!` are `!=` in test calls).

Slow methods were timed natively: the split search without the remaining-length check takes 12 s on `'1' * 45` in CPython, and the unpruned job assignment takes 1.1 s at 10 jobs, so about 18 s at 12. Every model solution's slowest case runs under 0.6 s in CPython.

## Freshness

Before writing, I listed every code widget in `graphs-dp`, `ds`, `algo-think` and `coding-int`, and every graph or DP code task in the topic and mock exams, and grepped for each planned setup. Rejected at planning, because a lesson or exam already sets them: islands and components counts (`graphs-dp` l3, l4), Kahn order and batch rounds (l5, homework-1), maze steps and spread days (homework-1, 2), climbing stairs and fewest coins (l13), grid paths (l12, l16), knapsack (l14, homework-4), stock trading with a fee (homework-3, topic 1.8), non-conflicting set (topic 2.4 `largest_clear_set`), fewest vans (topic 2.4), greedy coins and meetings (`algo-think` l14), longest rising subsequence (`oa-rising-run`), and subset sum, combination sum, permutations and queens (l10, l11, homework-3).

`node tools/fresh-check.mjs --drill <id>` at the gate: 0 hits for all 15, code names included. At `--min-run 8 --min-share 0` (run on `footpath-slabs`, `climb-limit`, `kiosk-change`) the hits are the shared constraint line ("too slow. Each test has its own 5-second limit in the browser") against sibling drills, and, for `climb-limit`, "from the top-left cell to the bottom-right" against `graphs-dp` l16, review-4, homework-4 and topic 1.8. That is stock phrasing for a grid route, so I kept it.

Judged close but kept: `dsa-footpath-slabs` against `graphs-dp` l13 `stairs` (both one-dimensional ways DP; here the step is modelling two kinds of 2-unit block, so the recurrence is `f(n-1) + 2 f(n-2)` and the answer is taken modulo); `dsa-stamp-gaps` against l13 `min_coins` (same table shape, but a count of unmakeable totals over a range, not one fewest-coins answer); `dsa-climb-limit` against homework-2 `maze_steps` (both grid BFS; the one-way climb rule makes the edges directed and is the point of the drill); `dsa-upstream-stations` against review-1 `has_path` (one pair there; here all sources at once, by reversing the edges); `dsa-kiosk-change` against `algo-think` l14 "Change for 87p" (that makes an amount from coins; this keeps a till over a queue).

## Engine limits

None new. The two known limits (the drill page ignores `setup`; `__learner_source__` is undefined) shaped the tests: every large input is built in the `call`. No bullets added to `docs/BACKLOG-INBOX.md`.

`app/content/manifest.json` was rewritten by the validator and is left out of the commit, so the merge regenerates it.
