# vectors level 3: performance task (perf retrofit)

- `app/content/courses/vectors/homework-3.json`, item `h-bond-curve`, index 9 (10 of 10), appended; nothing converted (9 items, cap 12). Kind `code` (Python, NumPy), difficulty 5, `la-inverse`, `la-product`, pace 1200.
- Matched objective (l12): "Build, multiply and invert matrices in NumPy, and prefer solving to inverting." (l9 "Write a system ... as $\mathbf{A}\mathbf{x} = \mathbf{b}$" also matches; l12's product is code, so it proves the level better.)
- Task: from a stub, `curve_from_bonds(bonds, prices, targets)` builds the cash-flow matrix of annual-coupon bonds, solves for the discount factors, prices new bonds by one product, refuses (`ValueError`) when the prices do not fix the curve or a target runs past it, and forms no inverse.
- Tests: 12 hidden against 1 example, seven bond sets. Fourteen planted slips each fail at least one (listed in the numbers script); `det == 0` fails test 9, where rounding leaves the determinant near $10^{-13}$. Two other correct routes pass.
- Overlapping screens: l12 screens[0] (`A @ x`), [3] (`solve`), [7] (build, check, solve), [8] (`three_way_hedge`), [9] (`safe_hedge`, rank refusal); l9 screens[2], [3], [6]; l4 screens[2], [7] (value as a dot product); l11 screens[4], [5]; homework-3 `h-min-var`; review-3 `r-solve-inv`. New: the bond setting, the matrix built from a schedule, curves fixed with no one-year bond, square sets that fix nothing, padded target rows.

## Gates

1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors (expected "vectors/L3: has a performance task, remove from perf-pending").
2. Voice, `VOICE_BASE=app/content/courses/vectors python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/vectors-3-perf-numbers.py`: exit 0, 85 checks.
4. Playthrough, `node tools/playthrough.mjs --set vectors/homework-3 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed (10 of 10, 1 performance starter fail); shots read at 1280 and 440 px, no sideways display, no older item needed `aligned`.

Freshness grep: bond, coupon, discount factor, `curve_from_bonds`, `cash_flow_rows`, maturity. `fresh-check --file`: 0 hits (one shared-numbers advisory on older items[8]). Backlog: 1 bullet.
