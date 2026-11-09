# Drills pack `dsa`, sub-pack B (two-pointers, windows, stacks-queues, binary-search)

Brief: `docs/briefs/drills-1.8.md`, sub-pack B. 15 Python drills, `"pack": "dsa"`, rows appended to `app/content/drills/index.json`.

| id | pattern | difficulty | pace (s) | stdin | hidden tests | course |
| --- | --- | --- | --- | --- | --- | --- |
| `dsa-fills-in-order` | two-pointers | 1 | 540 | no | 12 | ds |
| `dsa-cheap-pairs` | two-pointers | 2 | 900 | no | 12 | ds |
| `dsa-near-trades` | two-pointers | 2 | 1080 | yes | 12 | ds |
| `dsa-closest-hedge` | two-pointers | 3 | 1200 | no | 12 | ds |
| `dsa-sensor-alarm` | windows | 1 | 780 | yes | 12 | ds |
| `dsa-varied-windows` | windows | 1 | 720 | no | 12 | ds |
| `dsa-budget-stretch` | windows | 2 | 900 | no | 12 | ds |
| `dsa-oncall-rota` | windows | 2 | 960 | no | 12 | ds |
| `dsa-bracket-partners` | stacks-queues | 1 | 660 | no | 12 | ds |
| `dsa-net-tape` | stacks-queues | 2 | 1080 | no | 12 | ds |
| `dsa-ticket-desk` | stacks-queues | 3 | 1500 | yes | 12 | ds |
| `dsa-depth-block` | stacks-queues | 3 | 1500 | no | 12 | ds |
| `dsa-missing-seq` | binary-search | 1 | 600 | no | 12 | algo-think |
| `dsa-price-peak` | binary-search | 2 | 900 | no | 12 | algo-think |
| `dsa-kiosk-spacing` | binary-search | 3 | 1500 | no | 12 | algo-think |

Mix: five at 1, six at 2, four at 3; three stdin drills (`solve_<slug>(text)`, parsed with `split()`, tests with trailing newlines, blank lines and extra spaces). Skills come from the `ds` lessons (`ds-pointers`, `ds-arrays`, `ds-hashing`, `ds-stacks`, `ds-lists`) and `algo-think` lessons (`at-search`, `at-complexity`). Every drill has 2 examples with a `note`, 12 hidden tests (empty or smallest input, a tie or duplicate, a negative or boundary case, two large inputs that a quadratic or scan-per-query method cannot finish in 5 s) and three `notes` lines.

## Checks

1. `docs/reports/drills-dsa-b-check.py` (scratchpad venv Python): exit 0, 15 drills, 0 errors. For each case it runs the model solution and an independent method: brute force on small inputs; on the large ones a different algorithm (bisect counting, prefix sums, a difference array of spoiled window starts, depth matching, right-to-left jump links, numpy threshold runs, an iterator scan, unit-lot simulation, set difference, `index(max)`, a downward scan from the even split). One case (`net_tape([10**9, -1, -10**9])`) is worked by hand in a comment. It also checks the starter fails at least one test, the difficulty and stdin mix, and that no case uses `setup`.
2. `node tools/validate.mjs`: 0 errors, no warning on any `dsa-` file in this sub-pack.
3. `node tools/playthrough.mjs --drill <15 ids> --local-cdn <pkgs>`: 15 of 15 ok, All passed; again with `--mobile`: 15 of 15 ok, All passed.
4. Voice: `voice-scan.py 35` on the 15 files: 0 sentences over 35 words, 0 explanations over three sentences; no exclamation marks or em-dashes in prose (the only `!` are `!=` in code).

## Freshness

`node tools/fresh-check.mjs --drill <id>` at the gate: 0 hits for all 15. At `--min-run 8 --min-share 0` the only hits are the shared constraint lines ("is the target. Checking every pair is too slow. Each test has its own 5-second limit"), against sibling drills and `ci-` drills, and one phrase "the length of the longest run of" against `ds` homework-1 and l6: stock phrasing, kept.

Replaced before hand-back. The first draft repeated taught setups, though the prose gate was clean: merging two sorted lists (`algo-think` l12 `merge_logs`), best fixed-window sum (`ds` l6 `max_window_sum`), at most k distinct (`ds` homework-2 `longest_k_distinct`), balanced brackets (`ds` l9 `is_balanced`), days until a higher close (`ds` l10 `days_until_higher`), first index at least x (`algo-think` l9 `first_at_least`, a code-name hit), counts between two prices (`algo-think` review-3), and the shipping capacity search (`algo-think` homework-3 `min_capacity`; `days_needed` was a code-name hit). Their eight replacements are `fills-in-order`, `varied-windows`, `oncall-rota`, `bracket-partners`, `net-tape`, `missing-seq`, `price-peak` and `kiosk-spacing`.

Judged close but kept: `dsa-cheap-pairs` (count of pairs with sum at most a budget, against `ds` l5 `two_sum_sorted`, which finds one exact pair); `dsa-near-trades` (count of pairs within d, against `ds` homework-2 `has_pair_with_difference`, which asks whether one pair is exactly d apart); `dsa-sensor-alarm` (count of windows clearing an average, parsed from text, against `ds` l6's maximum window sum). In each the question and the counting step differ, so I judged the pattern shared and the setup new.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (drills dsa b)": the drill page ignores a case's `setup`, and `__learner_source__` is not defined there. The validator flags neither.

`app/content/manifest.json` was rewritten by the validator and is left out of the commit, so the merge regenerates it.
