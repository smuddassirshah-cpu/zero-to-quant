# Drills pack `ci`, pack 5 (graphs)

Brief: `docs/briefs/drills-ci-packs-5-8.md`, row "Pack 5", on top of `docs/briefs/drills-ci-packs.md` and `docs/briefs/drills-1.8.md`. 15 Python drills, `"pack": "ci"`, `"course": "coding-int"`, `"pattern": "graphs"`, skills `ci-patterns` and `ci-timed`, tags `["pack-5", ("stdin",) <slug>]`, rows appended to `app/content/drills/index.json`. Every drill carries `constraints` objects (ENGINE-BACKLOG 866) beside the prose.

| id | idea | difficulty | pace (s) | stdin | hidden tests | planted |
| --- | --- | --- | --- | --- | --- | --- |
| `ci-flood-reach` | flood fill, downhill or level steps | 2 | 960 | no | 13 | 3 |
| `ci-loop-cables` | union-find, every redundant link | 2 | 900 | no | 12 | 3 |
| `ci-line-from-pairs` | rebuild a path graph from an edge list | 2 | 1020 | no | 12 | 3 |
| `ci-checkpoint-route` | grid shortest path with walls, through a checkpoint | 3 | 1380 | yes | 13 | 3 |
| `ci-stuck-jobs` | cycle detection: jobs on or behind a cycle | 3 | 1260 | no | 13 | 3 |
| `ci-two-shift-rota` | bipartite check, largest side per group | 3 | 1320 | no | 13 | 3 |
| `ci-cheapest-route` | Dijkstra on a small graph, tie rules | 3 | 1500 | no | 13 | 3 |
| `ci-island-shapes` | island shapes, those seen once | 3 | 1320 | no | 13 | 3 |
| `ci-wall-break-route` | grid shortest path, one wall knocked through | 4 | 1980 | no | 14 | 2 + slow |
| `ci-nearest-depot` | multi-source BFS, two firms, ties | 4 | 1920 | no | 13 | 2 + slow |
| `ci-reclaimed-land` | union-find islands as land is added | 4 | 1920 | no | 14 | 2 + slow |
| `ci-ferry-timetable` | Dijkstra with timetabled departures | 4 | 2100 | yes | 13 | 2 + slow |
| `ci-first-circular-rule` | topological order: first rule making a cycle | 4 | 2040 | no | 13 | 2 + slow |
| `ci-half-fare-route` | Dijkstra over (town, voucher used) | 5 | 2580 | no | 13 | 2 + slow |
| `ci-safest-walk` | multi-source BFS then a max-min walk | 5 | 2700 | no | 14 | 2 + slow |

Mix: three at 2, five at 3, five at 4, two at 5; two stdin drills. Every idea of the row is covered: flood fill and island counts (flood reach, island shapes, reclaimed land), shortest path in a grid with walls (checkpoint route, wall break), multi-source search (nearest depot, safest walk), cycle detection and topological order (stuck jobs, first circular rule), union-find for groups and redundant links (loop cables, reclaimed land), Dijkstra (cheapest route, ferry timetable, half-fare route), bipartite check (two-shift rota), rebuilding a graph from an edge list (line from pairs).

## Pyodide timings, difficulty 4 and 5

Measured by `drills-ci-5-check.py --pyodide <pkgs>`: Pyodide 0.27.7 under node (V8, Chromium's engine), all hidden tests in one run, as the drill page runs them against its 5 s limit. "Stopped" means the run was cut off at the 12 s cap, so the true time is longer.

| id | target (model) | obvious method | obvious method is |
| --- | --- | --- | --- |
| `ci-wall-break-route` | 0.62 s | over 12 s (stopped) | knock each wall in turn and search again |
| `ci-nearest-depot` | 0.51 s | over 23 s (stopped) | one search per depot |
| `ci-reclaimed-land` | 0.47 s | over 12 s (stopped) | flood-fill the new cell's island after each fill |
| `ci-ferry-timetable` | 0.67 s | over 12 s (stopped) | relax every crossing until nothing changes |
| `ci-first-circular-rule` | 0.27 s | over 36 s (stopped) | search from `b` for `a` before each rule |
| `ci-half-fare-route` | 0.12 s | over 12 s (stopped) | a fresh Dijkstra with the voucher on each road |
| `ci-safest-walk` | 0.60 s | over 24 s (stopped) | every cell against every camera, then each level from the top |

Every target is under 1 s, a factor of five inside the limit; every obvious method passes 5 s. The obvious method is the last `planted` entry of each of these seven drills (the planted-check stale-result fault is fixed, so a timed-out plant no longer spoils the next submit), and `how` names it and the step to the target.

## Checks

1. `docs/reports/drills-ci-5-check.py` (scratchpad venv Python): exit 0, "15 drills, 0 errors" (64 s; with `--pyodide`, also the timings above). Per drill it runs the model and an independent method on every example and test (brute force on small inputs: every 2-colouring, every simple path, every permutation, a sweep until nothing changes, each wall or voucher in turn, minute-by-minute ferry simulation; on large inputs a different algorithm: parity union-find, Kosaraju, union by rank, a state search, frontier sets, SPFA, colour DFS with a binary search, two Dijkstras with both road directions, numpy covers with a binary search). It reads every call's actual arguments and checks them against the `constraints` objects and the prose limits, so the large generated tests the validator skips are checked too. It checks the starter fails, each wrong plant fails a test inside 2.5 s, each slow plant runs past 5 s in CPython, the mix, tags, paces and `how`.
2. `node tools/validate.mjs`: 0 errors; no `[no-constraints]` warning on these files. The only warnings are "pace over 30 minutes" on the seven drills paced 1,800 s or more, which the brief allows.
3. `node tools/playthrough.mjs --drill <15 ids> --local-cdn <pkgs>`: All passed; with `--mobile`: All passed. Shots at 440 px (ferry timetable, safest walk) read cleanly.
4. Voice: `voice-scan.py 35` on the 15 files: 0 sentences over 35 words, 0 explanations over three sentences; no em-dashes; the only `!` are `!=` in code.
5. This report and the inbox bullets.
6. `node tools/planted-check.mjs --drill <15 ids> --require --local-cdn <pkgs>`: 15 drills, 45 planted solutions, 0 failures.

## Planted solutions that passed at first, and the tests added

- `ci-wall-break-route` planted[0] (one seen mark per cell, whatever the knock state) passed every test. A random search found `['#.#E', 'S.##']` (answer 4; the plant says -1), now a hidden test.
- `ci-reclaimed-land` planted[0] (a repeated fill restarts the cell as a new group) passed. Added `largest_after_each(1, 3, [[0, 0], [0, 1], [0, 0]])`, where the repeated cell is not its group's root.
- `ci-safest-walk` planted[1] (the start cell's cover left out) passed. Added `safest_walk(['.......', '.#####.', 'G......'])`, where the start cell is the bottleneck.
- The check script also caught two tests outside the stated constraints while drafting (a £4,000 toll and a £1,999,990 toll); both were brought inside.

## Freshness

`node tools/fresh-check.mjs --drill <id>`: 0 hits for all 15, after one fix: the helper `has_loop` in the first-circular-rule model matched a `ds` lesson widget and was renamed `prefix_loops`. Taught setups avoided by design: `count_islands`, `count_loss_regions` (graphs-dp l4) and `capture_regions` (coding-int l9), so the island drill counts shapes seen once; `days_to_spread` (homework-1), so the multi-source drills compare two firms or take a max-min walk; `split_desks` (homework-1), so the rota asks for the largest day shift; `topo_sort` and `run_order` with smallest-name ties (l5), `batch_rounds` and `dsa-forced-order`, so the topological drills ask for stuck jobs and the first rule that makes a loop; `slowest_arrival`, `cheapest_within`, `count_cheapest` (l7, homework-2), so the Dijkstra drills settle ties, wait for sailings or spend a voucher; `dsa-spare-cables` (a count of moves), so loop cables lists every spare cable; `maze_steps`, `shortest_hops`, `dsa-climb-limit`, so the grid drills add a checkpoint or one knocked-through wall. Every example and test input was written for these drills. Nine drills grow from a known problem; each `how` ends with a sentence saying what changed and why it changes the code.

Worked numbers in the briefs and notes (the example answers 6, `[3, 4, 6]`, `['Bury', 'Hertford', 'Ware', 'Ely']`, `'11'`, `[1, 2, 3]`, 3, `[0, 1, 4]`, 1, 2, `[1, 1]`, `[1, 1, 2, 4]`, `'7'`, 4, 6, 1) are the `expect` of each drill's first example, and the check script recomputes each one with the independent method.

`app/content/manifest.json` was rewritten by the validator and is not committed.
