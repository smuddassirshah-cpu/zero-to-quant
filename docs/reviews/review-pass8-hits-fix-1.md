# Fix pass 1 of review-pass8-hits (group 1)

Sets: `arma/problems-3`, `coint/problems-1`, `elimination/problems-1`, `estimation/problems-3`, `fin-ml/problems-3`, `garch/problems-1`, `garch/problems-2`, `garch/problems-3`, `numerics/problems-1`. Every replacement applied as the reader wrote it; no key changed. The group has no `reuse` verdict in list B (its list B hits are all `stands`).

## Findings

1. coint/problems-1 `items[2].parts[3].explain.text` | fixed: "so $n = 1{,}105$ days," added after 1,104.4 (recomputed 1,104.40 and 1,105)
5. arma/problems-3 `items[2].parts[2].question` | fixed: "Read the normal tail from software or a table." (band unchanged)
6. arma/problems-3 `items[2].parts[3].question` | fixed: "Read the tail from software or a table, as in part 3." (band unchanged)
7. fin-ml/problems-3 `items[1].parts[1].question` | fixed: quantiles sentence added
8. fin-ml/problems-3 `items[1].parts[3].question` | fixed: "Read $\Phi$ from software or a normal table."
9. fin-ml/problems-3 `items[2].parts[3].question` | fixed: same sentence
10. garch/problems-1 `items[0].parts[1]` | fixed: question sentence added; `tol.abs` 0.0006 to 0.0025 (band [0.1895, 0.1945])
11. estimation/problems-3 `items[1].parts[1].wrong[3]` | fixed: tol 0.005 to 0.00005
12. garch/problems-2 `items[1].parts[0].wrong[3]` | fixed: tol 0.005 to 0.00005
13. garch/problems-2 `items[1].parts[2].wrong[3]` | fixed: tol 0.005 to 0.0005
14. garch/problems-2 `items[1].parts[4].wrong[3]` | fixed: tol 0.005 to 0.0005
15. garch/problems-2 `items[2].parts[2].wrong[2]` | fixed: tol 0.00005 to 0.000002
16. garch/problems-3 `items[0].parts[1].wrong[2]` | fixed: tol 0.005 to 0.000005
17. garch/problems-3 `items[3].parts[0].wrong[3]` | fixed: tol 0.005 to 0.0005
18. garch/problems-3 `items[3].parts[2].wrong[3]` | fixed: tol 0.005 to 0.0005
19. numerics/problems-1 `items[2].parts[1].wrong[1]` | fixed: tol 0.005 to 0.0005
21. elimination/problems-1 `items[1].parts[1].question` | fixed: stray backslash before the apostrophe removed

Counts: 17 fixed, 0 disputed, 0 deferred. Graded keys changed: none. Bands changed: finding 10 (key band widened to take table readings 19.0, 19.2, 19.4) and the nine `wrong` tolerances above, narrowed.

## Gates

- Validator: 0 errors; none of the pass 8 warnings for the fixed parts is printed.
- Voice scan 35: 0 and 0 for arma, coint, elimination, estimation, fin-ml, garch, numerics.
- Number scripts (`problems-<course>-numbers.py`, readers, delta and fluency scripts of the seven courses): all exit 0; no script edit was needed because they check slip values, not the `wrong` tolerances, and the key band checks still hold. The perf scripts of the courses were not run (coint-1-perf exceeds two minutes and checks other files).
- `fresh-check.mjs --file`: 0 hits on all nine sets.
- `grade-all.mjs --file`: 0 failures on all nine sets.
- `playthrough.mjs --problems`, with and without `--mobile`: All passed on all nine sets.
