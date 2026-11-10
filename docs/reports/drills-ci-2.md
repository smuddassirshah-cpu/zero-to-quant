# Drills pack `ci`, pack 2 (two-pointers, windows)

Brief: `docs/briefs/drills-ci-packs.md`, row "Pack 2", on top of `docs/briefs/drills-1.8.md`. 15 Python drills, `"pack": "ci"`, `"course": "coding-int"`, skills `ci-patterns` and `ci-timed`, tags `["pack-2", ("stdin",) <slug>]`, rows appended to `app/content/drills/index.json`.

| id | pattern | difficulty | pace (s) | stdin | hidden tests | planted |
| --- | --- | --- | --- | --- | --- | --- |
| `ci-reference-split` | two-pointers | 2 | 900 | no | 12 | 3 |
| `ci-late-fills-merge` | two-pointers | 2 | 1020 | no | 12 | 3 |
| `ci-two-desk-matches` | two-pointers | 3 | 1260 | no | 13 | 3 |
| `ci-widest-banner` | two-pointers | 3 | 1200 | no | 13 | 3 |
| `ci-van-pairs` | two-pointers | 3 | 1320 | yes | 13 | 3 |
| `ci-three-leg-nets` | two-pointers | 4 | 1860 | no | 13 | 3 |
| `ci-frame-triples` | two-pointers | 4 | 1800 | no | 13 | 3 |
| `ci-excused-outages` | windows | 2 | 960 | yes | 14 | 3 |
| `ci-capped-repeats` | windows | 3 | 1200 | no | 13 | 3 |
| `ci-rota-swaps` | windows | 3 | 1440 | no | 14 | 3 |
| `ci-basket-cover` | windows | 4 | 2100 | no | 14 | 3 |
| `ci-ends-to-target` | windows | 4 | 1980 | no | 14 | 3 |
| `ci-paired-signals` | windows | 4 | 2040 | no | 14 | 3 |
| `ci-exact-venue-runs` | windows | 5 | 2520 | no | 14 | 3 |
| `ci-hop-score` | windows | 5 | 2580 | no | 14 | 3 |

Mix: three at 2, five at 3, five at 4, two at 5; two stdin drills. Ideas of the row: pair search across two sorted lists with repeated sizes, opposite pointers on heights, a greedy pairing after a sort (two-pointers); distinct triples to a target and counting triangle triples (triple search); stable partition in place; merging from the back with a tie rule; shrinking windows with a count map (capped repeats, basket cover with multiplicity, most-common-letter window); at most k of something (excused outages, and exactly k venues as at most k minus at most k - 1); the inverted window (longest middle stretch for end removals); deque maximum over a time window (signal pairs) and over a fixed window of DP totals (hop score). At 4 and 5, `how` names the obvious method and the step to the target one.

## Checks

1. `docs/reports/drills-ci-2-check.py` (scratchpad venv Python): exit 0, 15 drills, 0 errors. Per case it runs the model and an independent method (brute force on small inputs; on large ones a stable sort, `Counter`, tallest-first index sweep, binary search on the number of van pairs, value-pair hash for triples, numpy `searchsorted`, bisect on prefix sums, occurrence lists, a fixed-length window under binary search on the length, a prefix and suffix map, a sparse table, sorted first-occurrence lists, a heap with lazy deletion). It checks the starter fails; every planted solution fails a test and finishes all tests inside 2.5 s; each slow method in `SLOW` (the obvious one, 13 of them) runs past 5 s on one hidden test in CPython; and the mix. Model time over all tests: under 0.25 s in CPython and under 0.45 s in Pyodide 0.27.7 (timed in node).
2. `node tools/validate.mjs`: 0 errors. The only warnings on these files are "pace over 30 minutes" on the six drills paced 1,800 to 2,580 s, which the brief allows (900 to 2,700).
3. `node tools/playthrough.mjs --drill <15 ids> --local-cdn <pkgs>`: 15 of 15 ok, All passed; with `--mobile`: All passed. Screenshots at 440 px and desktop read cleanly; the lambda calls of the in-place drills wrap but stay inside the card.
4. Voice: `voice-scan.py 35` on the 15 files: 0 sentences over 35 words, 0 explanations over three sentences; no em-dashes; the only `!` are `!=` in code.
5. This report and the inbox bullets.
6. `node tools/planted-check.mjs --drill <15 ids> --require --local-cdn <pkgs>`: 15 drills, 45 planted solutions, 0 failures.

## Planted solutions

First pass: 3 planted solutions passed every hidden test, and one more was caught only by running out of time. Tests added (never a weaker slip): `solve_excused_outages('4 1\n UUUU \n')` (raw second line, spaces counted as down days), `longest_after_swaps('BAAA', 1)` (only the start letter of each stretch), `solve_excused_outages('4 2\nDDDU\n')` (restart the window at today) and `longest_capped_run(['a', 'b', 'b', 'c'], 1)` (lowering the new id's count).

The first draft had one "right idea, wrong complexity" planted solution per drill. Those timed out in the browser, and planted-check then failed the model on 13 drills: after a timeout the drill page restarts Python, and the playthrough's next Submit goes in before Python is ready, so it reads the timed-out run's results again (shown by a scratch copy of the tool that waits for ready: 0 failures). The slow methods moved to `SLOW` in the check script, timed there, and each was replaced in `planted` by a fast wrong solution. Engine bullet raised.

## Freshness

`node tools/fresh-check.mjs --drill <id>`: 0 hits for all 15. At `--min-run 8 --min-share 0` the hits are the shared constraint line ("is too slow. All the tests in a run share one 5-second limit in the browser") against `dsa-` and sibling `ci-` drills: stock phrasing, kept. Taught setups avoided by design: `max_sliding_window` and `longest_within_limit` (coding-int l3), `shortest_at_least` and `window_median` (coding-int homework-1), `longest_k_distinct`, `has_pair_with_difference` (ds homework-2), `two_sum_sorted` (ds l5), `merge` and `merge_logs` (algo-think l12), `partition` (algo-think l13), `find_anagrams` (coding-int l6), and the pack's `dsa-` and `oa-` drills of these two patterns (pairs within a budget, closest pair, pairs within d, subsequence, rain water, budget stretch, clean runs, alarm windows, varied windows, product windows).

`app/content/manifest.json` was rewritten by the validator and is left out of the commit.

Counts as authored; see `docs/reviews/review-drills-ci-1-2.md`, Fix pass, for later changes. `ci-zero-quads` is now difficulty 3 and `ci-mean-stretches` 4 (see the delta fix pass).

Counts as authored; `ci-reference-split` was `ci-cancelled-to-back`, and `ci-widest-banner` now returns `[area, width]` with 14 tests and 4 planted. See `docs/reviews/review-delta-session-z.md`, Fix pass.
