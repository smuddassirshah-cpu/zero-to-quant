# Drills, pack `ci`, pack 1 (hashing, prefix sums)

Brief: `docs/briefs/drills-ci-packs.md`, row "Pack 1", on top of `docs/briefs/drills-1.8.md`. Fifteen Python drills in `app/content/drills/`, each with a row appended to `drills/index.json`. All carry `"pack": "ci"`, `"course": "coding-int"`, skills `ci-patterns` and `ci-timed` (plus `ci-strings` on the two stdin drills), `tags` starting `"pack-1"`, and three `planted` wrong solutions (two on `ci-code-classes`).

## Drills

| id | pattern | idea | difficulty | pace (s) | stdin | hidden tests |
| --- | --- | --- | --- | --- | --- | --- |
| `ci-code-classes` | hashing | group by a computed key (sorted even and odd letters) | 2 | 900 | no | 11 |
| `ci-steady-climbs` | hashing | count pairs by an equal key, `p[i] - i` | 2 | 900 | no | 11 |
| `ci-row-column-matches` | hashing | rows as tuple keys, columns looked up | 2 | 1050 | no | 11 |
| `ci-peak-stretch` | hashing | frequency with first positions, shortest span at the peak | 3 | 1200 | no | 12 |
| `ci-serial-runs` | hashing | longest run by set lookups, ties to the lower start | 3 | 1200 | no | 12 |
| `ci-mean-stretches` | prefix-sums | prefix map of `x - target` (mean exactly target) | 3 | 1350 | no | 12 |
| `ci-best-block` | prefix-sums | two-dimensional prefix sums, best `s` by `s` block | 3 | 1350 | no | 13 |
| `ci-unique-counts` | hashing | frequency buckets, fewest removals for distinct counts | 3 | 1500 | yes | 14 |
| `ci-zero-quads` | hashing | counting by complement, meet in the middle over four lists | 4 | 1800 | no | 12 |
| `ci-even-vowels` | prefix-sums | prefix parity mask, first position of each pattern | 4 | 1800 | no | 14 |
| `ci-others-product` | prefix-sums | products without division on a grid, modulo 12345 | 4 | 1800 | no | 12 |
| `ci-equal-three` | prefix-sums | prefix map keyed on two count differences | 4 | 1800 | yes | 13 |
| `ci-camera-cover` | prefix-sums | two-dimensional difference array, cells covered at least `m` times | 4 | 1800 | no | 12 |
| `ci-target-blocks` | prefix-sums | submatrices with sum target: fix two rows, prefix map on columns | 5 | 2400 | no | 12 |
| `ci-trim-to-multiple` | prefix-sums | shortest stretch to remove so the rest divides by `p` | 5 | 2700 | no | 13 |

Split 3 / 5 / 5 / 2 at difficulties 2 / 3 / 4 / 5; two stdin drills. At 4 and 5 the `how` line names the step from the obvious method to the target one, and the obvious method is planted and times out on the large tests (CPython: over 5 s on one test; Pyodide: past the drill's shared 5 s). Large `others_product_grid` tests return a digest through a `lambda` call (`[len(g), g[0][:4], g[-1][-4:], sum]`), as `dsa-staff-per-hour` does, so the file stays at 6 KB.

Not repeated from the ten existing `ci-` drills or the `dsa` hashing and prefix drills: no pair gap, divisible pairs, digit-sum pairs, first missing positive, longest sum `k`, balanced 0/1 run, equal-sum cuts, rectangle queries, majority, k-th repeat, shape groups or winning stretch. `coding-int` l17 (`count_subarrays_divisible_by_k`, `longest_zero_sum_subarray`) and l18 (`product_except_self`) are lesson setups, so the plain versions were not used: products without division is a grid modulo a composite number (no inverse exists), and the prefix-map count is "mean exactly target".

## Planted solutions

44 in all. On the first full run 41 failed a hidden test and 3 passed every test; a second run caught a fourth (`ci-zero-quads`, timing). Each got a new or larger test, never a weaker plant:
- `ci-best-block` "adds up each block afresh": passed the 300 by 300, `s = 150` test in under 5 s. Added a 500 by 500, `s = 167` test and raised `R, C` to 500.
- `ci-target-blocks` "every rectangle with a prefix table": 100 by 100 ran inside 5 s. Large tests moved to 60 by 400 (constraint `R` at most 60, `C` at most 400).
- `ci-unique-counts` "splits on single spaces": the double-space test gave the right count by chance. Added `"2\nA  B\n"`.
- `ci-zero-quads` "fixes three, looks up the fourth": 400 per list ran near 5 s in CPython on one run. Lists raised to 500 (cubic now 8 s on its first large test).

## Checks

1. `docs/reports/drills-ci-1-check.py` (venv Python): exit 0. Model and an independent method agree with every `expect` (true brute force on small inputs: swap-reachable sets, all pairs, all stretches, all keep vectors, cell painting; numpy or sorting on large ones); each brief's worked example recomputed, with hand sums; starter fails; model under 1 s a test in CPython; every planted solution fails a test (wrong, error, or over 5 s).
2. `node tools/validate.mjs`: 0 errors. Warnings on these files: only `pace ... over 30 minutes` for the two difficulty-5 drills (2400, 2700), which the brief's 900 to 2700 range allows.
3. Playthrough `--drill` x15 `--local-cdn`: all passed, and again with `--mobile`. Shots looked at (440 and desktop): no overflow; the stdin input lines are written as separate paragraphs because the drill brief renders no lists.
4. Voice: `voice-scan.py 35` on a copy of the 15 files: 0 over three sentences, 0 over 35 words of 497 sentences (24 over 20). No exclamation marks or dashes.
5. Fresh: `node tools/fresh-check.mjs --drill <id>`: 0 hits for all 15 (not triaged at looser settings).
6. `node tools/planted-check.mjs --drill <id> --require --local-cdn <pkgs>`: **red for 11 of 15, a tool race, not the content.** After a planted solution times out the worker restarts, and the next Submit fires while the drill still says "Restarting Python", so `go('submit')` does nothing and `drillSubmit` reads the previous run's results; the model is then reported at 9 of 12 and similar. The four drills with no timing plant are green. On a copy of `app/` in the scratchpad with `drillReady` awaited before each planted and model submit in `plantedOne` (two lines), all 15 are green: 44 planted solutions, 0 failures. Repo engine files are not edited.

## Open

- Check 6 needs the `plantedOne` fix (inbox bullet) before it can go green in the repo.
