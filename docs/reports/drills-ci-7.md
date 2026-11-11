# Drills pack `ci`, pack 7 (two-dimensional DP and backtracking)

Brief: `docs/briefs/drills-ci-packs-5-8.md`, row "Pack 7", on top of `docs/briefs/drills-ci-packs.md` and `docs/briefs/drills-1.8.md`. 15 Python drills, `"pack": "ci"`, `"course": "coding-int"`, pattern `dp` or `backtracking` (the vocabulary has no `dp-2d`, so the two-dimensional tables carry the tag `dp-2d`), skills `ci-patterns` and `ci-timed`, tags `["pack-7", ("stdin",) ("dp-2d",) <slug>]`, rows appended to `app/content/drills/index.json`. Every drill carries `constraints` objects (ENGINE-BACKLOG 866) beside the prose.

| id | idea | pattern | difficulty | pace (s) | stdin | hidden tests | planted |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ci-drop-point-routes` | grid routes with blocked cells, through at least one drop point | dp | 2 | 1020 | no | 14 | 3 |
| `ci-spaced-picks` | subsets with a minimum gap, in list order | backtracking | 2 | 960 | no | 12 | 3 |
| `ci-long-mirrors` | palindromic substrings of length at least `k` | dp | 2 | 960 | no | 13 | 3 |
| `ci-tolerant-common` | longest common subsequence, match within a tolerance | dp | 3 | 1440 | no | 13 | 3 |
| `ci-priced-edits` | edit distance with three prices | dp | 3 | 1500 | yes | 12 | 3 |
| `ci-hold-limit` | 0/1 knapsack with a crate limit | dp | 3 | 1440 | no | 12 | 3 |
| `ci-pillar-queens` | `q` queens on a board with pillars | backtracking | 3 | 1380 | no | 14 | 3 |
| `ci-invoice-matches` | combinations with duplicates, at most `k` items | backtracking | 3 | 1320 | no | 12 | 3 |
| `ci-trace-count` | word traces on a grid, revisits allowed, counted | dp | 4 | 1980 | no | 13 | 3 + slow |
| `ci-mirror-pieces` | splitting a string into fewest palindromes | dp | 4 | 2040 | yes | 14 | 4 + 2 slow |
| `ci-three-feed-common` | longest common subsequence of three strings | dp | 4 | 1800 | no | 15 | 3 + slow |
| `ci-even-desks` | partition into two equal-size groups, closest sums | dp | 4 | 2040 | no | 12 | 2 + slow |
| `ci-merged-tape` | ways a string interleaves two others | dp | 4 | 1980 | no | 15 | 3 + slow |
| `ci-light-cargo` | 0/1 knapsack indexed by value, huge weights | dp | 5 | 2520 | no | 12 | 3 + slow |
| `ci-smooth-orderings` | permutations with duplicates under a neighbour rule, counted | backtracking | 5 | 2700 | no | 14 | 3 + 2 slow |

Mix: three at 2, five at 3, five at 4, two at 5; two stdin drills (`ci-priced-edits`, `ci-mirror-pieces`). Every idea of the row is covered: grid paths with blocked cells (drop-point routes), edit distance (priced edits), longest common subsequence (tolerant common, three-feed common), 0/1 knapsack and partition into equal sums (hold limit, light cargo, even desks), palindromic substrings (long mirrors), subsets (spaced picks), permutations and combinations with duplicates (smooth orderings, invoice matches), placing queens (pillar queens), a word search on a grid (trace count), splitting a string into valid parts (mirror pieces). No problem of pack 6 is used (no climbing, tiling, coin change, decoding, word break, trading or maximum subarray).

Output order: the three drills that return lists fix it in the brief. `ci-spaced-picks` and `ci-invoice-matches` give each choice ascending and the choices in Python's order for lists, so exactly one answer is right; every other drill returns a number or a string of numbers.

## Pyodide timings, difficulty 4 and 5

Measured by `drills-ci-7-check.py --pyodide <pkgs>`: Pyodide 0.27.7 under node, all hidden tests in one run, as the drill page runs them against its 5 s limit, at Pyodide's default recursion limit of 1,000. "Stopped" means the run was cut off at the 12 s cap (a test that started before the cap finishes first), so the true time is longer.

| id | target (model) | obvious method | obvious method is |
| --- | --- | --- | --- |
| `ci-trace-count` | 0.07 s | over 12 s (stopped) | follow every trace square by square |
| `ci-mirror-pieces` | 0.11 s | over 12 s (stopped) | try every mirrored first piece and recurse, unremembered |
| `ci-three-feed-common` | 0.10 s | over 12 s (stopped) | recurse on the three ends, unremembered |
| `ci-even-desks` | 0.03 s | over 12 s (stopped) | every choice of `m` traders (`combinations`) |
| `ci-merged-tape` | 0.02 s | over 12 s (stopped) | recurse on which feed gave the next letter, unremembered |
| `ci-light-cargo` | 0.04 s | over 15 s (stopped) | the knapsack table over weight |
| `ci-smooth-orderings` | 0.04 s | over 12 s (stopped) | build each distinct sequence one at a time |

Every target is under 0.2 s, more than a factor of 25 inside the limit, and each of these seven models is iterative, so none reaches the recursion limit. Every obvious method passes 5 s. It is the last `planted` entry of each of these seven drills (listed in `SLOW_PLANTED`), and `how` names it, the step to the target, and what changed from the classic. Two orderings were set for the timing: in `ci-light-cargo` the 1,500,000 kg test comes before any test with a cap near $10^9$, so the weight table runs out of time before it could ask for 8 GB; in `ci-merged-tape` a 30 + 30 letter test comes before the 300 + 300 one, because the unremembered recursion 600 frames deep ended the Pyodide process with no output (inbox bullet).

## Checks

1. `docs/reports/drills-ci-7-check.py` (scratchpad venv Python): exit 0, "15 drills, 0 errors", "stated numbers recomputed: 40". Per drill it runs the model and an independent method on every example and test (brute force on small inputs: every route, subset, set of cuts, set of squares, arrangement and choice of positions, and a Dijkstra over strings for edits; on large inputs a different algorithm: a flag state, a table by length, memoised recursion from the front, a dict of (count, weight) states, a table filled from the end, sets of totals, a Pareto list, orders divided by the shuffles of equal sizes). It reads every call's arguments and checks them against the `constraints` objects and the prose limits (rectangular boards, `q` at most `n`, even counts, stdin text that parses with its totals), so the generated tests the validator skips are checked too. It checks the starter fails, each wrong plant fails a test inside 2.5 s, each slow plant runs past 5 s in CPython, the mix, tags, paces and `how`, and recomputes the 40 numbers stated in briefs, notes and `how` (each brief's worked answer is also the first example's `expect`).
2. `node tools/validate.mjs`: 0 errors; no `[no-constraints]` warning on these files. The only warnings on them are "pace over 30 minutes" on the seven drills paced 1,800 s or more, which the brief allows.
3. `node tools/playthrough.mjs --drill <15 ids> --local-cdn <pkgs>`: All passed; with `--mobile`: All passed. Shots at 440 px (`ci-priced-edits`, `ci-light-cargo`) read cleanly.
4. Voice: `voice-scan.py 35` on the 15 files: 0 sentences over 35 words, 0 explanations over three sentences; no em-dashes; the only `!` are `!=` in code (a factorial sign in `ci-smooth-orderings` was written out as "11 factorial").
5. This report and the inbox bullets.
6. `node tools/planted-check.mjs --drill <id> --require --local-cdn <pkgs>`, in three runs of five: 15 drills, 50 planted solutions, 0 failures.

## Planted solutions that passed at first, and the tests added

- `ci-mirror-pieces` planted[0] (cut off the longest mirrored start) failed only the large random test. Added `'2\naabba\nabbcb\n'` (2 and 3 pieces; the greedy says 3 and 4), found by a search over short strings.
- `ci-three-feed-common` planted[0] (one longest common subsequence of the first two, then the third) passed every hidden test. Added `('xyx', 'xxyzy', 'xxxxz')` (answer 2; the plant says 1), found by a random search.
- `ci-merged-tape` planted[1] (no length check) failed only the 300 + 299 letter test. Added `('ab', 'c', 'acbb')` (answer 0; the plant says 1).
- `ci-smooth-orderings` planted[3] (each distinct sequence built one at a time) finished in 4.8 s in CPython with 10 orders. The limit became 11 orders and one large test has 11 different sizes, $39{,}916{,}800$ sequences.

## Freshness

`node tools/fresh-check.mjs --drill <id>`: 0 hits for all 15. Taught setups avoided by design: `count_paths` and `min_path_cost` (graphs-dp l16), so the grid drill counts routes through a drop point; `lcs_length` and `edit_distance` (l15), so the drills add a tolerance, prices or a third string; `knapsack` (l14) and `unbounded_knapsack` (homework-4), so the knapsacks add a crate limit or index by value; `n_queens` (l11), so the board has pillars and fewer guards than rows; `subsets`, `permutations` (l10), `combos` (l11) and `combination_sum` (homework-3), so the drills add a gap, a cap on `k` items or a neighbour rule; `longest_palindrome` (coding-int l6), so the palindrome drills count long stretches and cut into fewest pieces; `ci-board-words` (pack 4), so the grid word drill counts traces with revisits; `dsa-split-prices`, `dsa-free-desk-square` and `dsa-server-loads`; contests l11 (meet in the middle, a tour over subsets), so no drill asks for the best subset under a limit. Every example and test input was written for these drills. Each `how` ends with a sentence saying what changed from the classic and why it changes the code.

`app/content/manifest.json` was rewritten by the validator and is not committed.

## Fix pass (second read of pack 7)

- Recursion depth. On the drill page Python stops silently about 450 to 500 frames deep (about 200 to 250 calls with a generator in each). The tests a top-down solution has to pass now stay under about 300 frames: `ci-merged-tape` at most 150 + 150 letters (tape 300), `ci-mirror-pieces` tapes of at most 150 letters, `ci-priced-edits` codes of at most 150, `ci-tolerant-common` feeds of at most 150 ticks. A search of my own found two more: `ci-long-mirrors` (a top-down `is_palindrome(i, j)` goes n / 2 calls deep, 500 on the old 1,000-letter test) now at most 300 letters, and `ci-drop-point-routes` (a generator in each call went 400 calls deep on a 200 by 200 floor) now at most 80 by 80. The other nine drills recurse at most 150 calls deep.
- Confirmed in Chromium (`planted-check` on a scratch copy, my own solutions as `planted`): a top-down `@lru_cache` solution and a dict-memo solution pass every test of the four drills, and `@lru_cache` solutions pass `ci-drop-point-routes`, `ci-three-feed-common`, `ci-hold-limit`, `ci-trace-count` and `ci-light-cargo`. `drills-ci-7-check.py` now runs the same style of solutions at a limit of 340 frames.
- Pyodide timings after resizing (`drills-ci-7-check.py --pyodide`): model `ci-merged-tape` 0.016 s, `ci-mirror-pieces` 0.015 s, `ci-three-feed-common` 0.094 s, `ci-smooth-orderings` 0.057 s. The ruled-out method (the last-but-one or last slow plant) is still cut off at 12 s on all four. In `planted-check` the two new slow plants (the cut-off search of `ci-mirror-pieces`, the formula-then-walk of `ci-smooth-orderings`) fail on the time limit.
- `ci-merged-tape` has 15 tests, not the 16 the review's finding 10 counts: the validator allows at most 15, so the 300 by 299 length-mismatch test (now 150 by 149) was dropped; tests[3] and [7] still catch a missing length check.
