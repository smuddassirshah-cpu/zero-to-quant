# opt-dash level 3: performance task

`homework-3.json`, `h-black-iv`, item 8 of 8 (added; cap 12). Kind `code` (Python, standard library).

Objective: l9 "Implement a robust implied volatility solver." Chosen over l12 ("Build and plot a surface") because a solver's robustness can be graded by hidden tests; a plot cannot.

Task: `black_iv(price, F, K, D, T, kind)` solves in forward terms with no pricer loaded, returns NaN at or outside the discounted no-arbitrage bounds or for a NaN price, and must solve penny quotes and vols to 300%. The lesson's solver works in $S$, $r$, $q$ with `bs_price` and `bs_vega` loaded and raises instead.

Tests: 13 hidden, 2 examples; vols within absolute 1e-8. Eleven planted bugs each fail, first at their named test: plain Newton from 0.2 (diverges on the 9p put), discounting omitted, put-call parity sign, call formula for puts, call bounds for puts, no bounds check, raising instead of NaN, search capped at 2, undiscounted bounds, NaN price slipping through, non-strict bounds.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; only perf-pending warnings.
2. `VOICE_BASE=app/content/courses/opt-dash python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python -I docs/reports/opt-dash-3-perf-numbers.py`: exit 0 (route 2 is SciPy `brentq` and `ndtr`).
4. `node tools/playthrough.mjs --set opt-dash/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed, starter fails. Shots clean.

Freshness grep: `black_iv`, `black_price`, `forward terms`, `discount factor $D$`, `100.4`, `101.2`, `146,935`, `300%`, `nan`.
