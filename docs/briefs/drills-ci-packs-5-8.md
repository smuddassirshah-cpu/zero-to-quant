# Brief: Phase 4 drill packs 5 to 8 (pack `ci`, 60 drills; PLAN 2d item D and 2a "Drill packs 5 to 8"; `docs/briefs/interview-plan.md` "Drill packs")

Everything in `docs/briefs/drills-ci-packs.md` holds (and through it `docs/briefs/drills-1.8.md`): files, fields, difficulty mix, pace, two stdin drills a pack, `tags` with `"pack-<n>"` first, `planted` required, true `notes`, checks 1 to 6. Python only; the C++ variants of packs 6 to 8 are not part of this task. This brief adds the packs and four rules from the reviews of packs 1 to 4.

## Packs (one agent each, 15 drills)

| Pack | Patterns | Ideas to cover |
| --- | --- | --- |
| 5 | `graphs` | grid flood fill and island counts, shortest path in an unweighted grid with walls, multi-source breadth-first search, cycle detection and topological order of a dependency list, union-find for connected groups and redundant links, Dijkstra on a small weighted graph, bipartite check, cloning or rebuilding a graph from an edge list |
| 6 | `dp-1d` | climbing and tiling counts, best non-adjacent sum on a line and on a ring, coin change (fewest coins, number of ways), longest increasing run by patience sorting, decoding counts, word break, best time to trade with a cooldown or a fee, maximum subarray and maximum product subarray |
| 7 | `dp-2d`, `backtracking` | grid paths with blocked cells, edit distance, longest common subsequence, 0/1 knapsack and partition into equal sums, palindromic substrings, subsets, permutations and combinations with duplicates, placing queens, a word search on a grid, splitting a string into valid parts |
| 8 | `intervals`, `greedy`, `bits`, `simulation` | merging and inserting intervals, fewest rooms or arrows, jump reachability and fewest jumps, a refuelling circuit, task scheduling with a gap, single number and counting bits, subsets by bit mask, spiral and rotation of a matrix, a robot or order-book simulation run step by step |

## Rules added from the reviews of packs 1 to 4

- **Constraints, machine-readable (ENGINE-BACKLOG 866, AUTHORING section 5).** Every drill carries the `constraints` object shape beside its prose constraints, and every example and hidden test satisfies it; the validator now checks this. A test outside the stated constraints was found three times in packs 1 to 4.
- **Fresh data.** Two readers recalled 26 drills of packs 1 to 4 as carrying a coding site's sample data. Write every example and test input yourself; never reuse a well-known sample (`[2, 7, 11, 15]`, `"leetcode"`, the 3 by 3 spiral of 1 to 9). A classic problem needs a changed return value or constraint that changes the code, and the `how` says what changed.
- **No drill repeats** a `coding-int` or `trees` lesson task, a `dsa-` drill, a `ci-` drill of packs 1 to 4, or a `contests` task under a new story: read the index rows of those packs for your patterns first.
- **The large hidden test** at difficulty 4 and 5 is sized from a measurement in Pyodide, not CPython: the obvious method must exceed the drill page's time limit there and the target method must pass with at least a factor of five to spare; record both timings in the report.

Checks, names: `docs/reports/drills-ci-<n>-check.py`, `docs/reports/drills-ci-<n>.md`, inbox heading `Raised later (drills ci <n>):`. Do not edit engine files, `course.json`, lessons, or other agents' drills. Do not commit `manifest.json`. Commit in your worktree every five drills with "drills ci pack <n>" in the message; never push.
