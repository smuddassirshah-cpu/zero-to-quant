# Drills pack `ci`, pack 4 (trees, heaps-tries)

Brief: `docs/briefs/drills-ci-packs.md`, row "Pack 4", on top of `docs/briefs/drills-1.8.md`. 15 Python drills, `"pack": "ci"`, `"course": "coding-int"`, skills `ci-patterns` and `ci-timed`, tags `["pack-4", ("stdin",) <slug>]`, rows appended to `app/content/drills/index.json`.

| id | pattern | difficulty | pace (s) | stdin | hidden tests | planted | tree encoding in the brief |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ci-right-edge-view` | trees | 2 | 960 | no | 12 | 3 | nested tuple `(value, left, right)`, `None` empty |
| `ci-read-preorder` | trees | 2 | 1020 | no | 12 | 3 | preorder text with `#`, returned as nested tuple |
| `ci-busiest-links` | heaps-tries | 2 | 900 | no | 11 | 3 | (none) |
| `ci-first-misplaced` | trees | 3 | 1260 | no | 13 | 3 | nested tuple `(price, left, right)` |
| `ci-rebuild-from-orders` | trees | 3 | 1380 | no | 12 | 3 | preorder and inorder lists, returned as nested tuple |
| `ci-level-totals` | trees | 3 | 1320 | yes | 11 | 3 | parent numbers on line 2, `-1` for the root |
| `ci-no-repeat-rota` | heaps-tries | 3 | 1320 | no | 13 | 3 | (none) |
| `ci-stock-by-prefix` | heaps-tries | 3 | 1440 | no | 12 | 3 | (trie) |
| `ci-downward-path-sums` | trees | 4 | 1980 | no | 13 | 3 | `parent` list, `-1` root, parent may outnumber child |
| `ci-best-route-value` | trees | 4 | 1920 | no | 13 | 3 | `parent` list |
| `ci-handoff-distances` | trees | 4 | 2100 | no | 12 | 3 | `parent` list |
| `ci-cheapest-pairs` | heaps-tries | 4 | 1860 | no | 13 | 3 | (none) |
| `ci-funded-projects` | heaps-tries | 4 | 1800 | no | 13 | 3 | (none) |
| `ci-live-median` | heaps-tries | 5 | 2640 | yes | 12 | 3 | (none) |
| `ci-board-words` | heaps-tries | 5 | 2700 | no | 12 | 3 | (trie) |

Mix: three at 2, five at 3, five at 4, two at 5; two stdin drills. Ideas of the row: lowest common ancestor (handoff distances, many queries, binary lifting); path sums (downward runs to a target with a prefix count; best bending route); serialise and rebuild (preorder text with markers; preorder plus inorder); level views (right-hand view; heaviest level from stdin); validate with bounds (first misplaced level in preorder); k-way merge (k cheapest two-leg trades as merged sorted runs); running median with two heaps (with cancellations, lazy deletion); top k by frequency (undirected links, name tie rule); prefix lookups (stock under a prefix with replacing sets) and word search with a trie. Plus a heap greedy (rota with no double shift) and a two-heap greedy (projects from a growing pot). Nested tuples keep a height of at most 400; the deep trees of the difficulty-4 drills use a `parent` list so a chain of 100,000 can be tested without recursion.

## Checks

1. `docs/reports/drills-ci-4-check.py` (scratchpad venv Python; optional drill ids check a subset): exit 0, 15 drills, 0 errors. Per case it runs the model and an independent method (brute force on small inputs; on large ones an iterative parser, the stack rebuild, a memoised climb, a count-array scan for the rota, a hash of all prefixes, subarray sums or Kadane along a chain, an O(n h) walk-up, an Euler tour with a sparse table, a threshold search with numpy `searchsorted`, a sorted list, one search per word). It checks the starter fails; every planted solution fails a test and finishes all tests inside 2.5 s; each slow method in `SLOW` (the obvious method of all seven drills at 4 and 5) runs past 5 s on one hidden test in CPython; `how` at 4 and 5 names the obvious method and the step; and the mix. Model time over all hidden tests in Pyodide 0.27.7 (node): 0.03 to 1.02 s per drill.
2. `node tools/validate.mjs`: 0 errors. The only warnings on these files are "pace over 30 minutes" on the six drills paced 1,800 s or more, which the brief allows.
3. `node tools/playthrough.mjs --drill <15 ids> --local-cdn <pkgs>`: 15 of 15 ok, All passed; with `--mobile`: All passed. Screenshots at 440 px and desktop (level totals, handoff distances, live median) read cleanly.
4. Voice: `voice-scan.py 35` on the 15 files: 0 sentences over 35 words, 0 explanations over three sentences; no em-dashes; the only `!` are `!=` in code.
5. This report and the inbox bullets.
6. `node tools/planted-check.mjs --drill <15 ids> --require --local-cdn <pkgs>`: 15 drills, 45 planted solutions, 0 failures.

## Planted solutions

No planted solution passed every hidden test on the first run, so no test was added for that reason. Two tests were fixed as drafting faults found by the check script: a `ci-handoff-distances` tree with a node that was its own parent (the climb never ended), and duplicate words in the large `ci-board-words` list, which the brief says are distinct. All planted solutions are fast and wrong, per the known `planted-check` timeout fault; the slow methods live in `SLOW`.

One near miss is stated openly: for `ci-live-median` a sorted list with `insort` and `del` (not the obvious method, which re-sorts) takes 1.7 s per large test in CPython, so `SLOW` holds only the re-sort. Timed in Pyodide it takes 6.15 s over the hidden tests, past the shared 5 s limit, while the model takes 0.96 s.

## Freshness

`node tools/fresh-check.mjs --drill <id>`: 0 hits for all 15. Taught setups avoided by design: `running_median` (ds homework-4) and `window_median` (coding-int homework-1), so the median drill adds cancellations; `kth_largest_stream`, `top_k_frequent` (coding-int l4), so the frequency drill counts undirected links; `count_prefix`, `top_completions` (coding-int l2), so the prefix drill sums replaceable counts; `validate_bst` (ds l15), so the bounds drill reports the first misplaced level; `merge_k` (ds homework-4, algo-think homework-3), so the k-way merge is over implicit runs; `level_order`, `max_root_to_leaf`. Also the pack's `dsa-` and `oa-` drills of these patterns (single-pair manager, nearest BST level, shallowest leaf, swapped levels, nearest strikes, print queue, tightest window across venues, short codes, stick merge cost).

`app/content/manifest.json` was rewritten by the validator and is committed with the drills.
