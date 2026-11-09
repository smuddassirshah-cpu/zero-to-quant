# opt-dash level 3: performance task

`homework-3.json`, `h-black-iv`, item 8 of 8 (added; cap 12). Kind `code` (Python, standard library).

Objective: l9 "Implement a robust implied volatility solver." Chosen over l12 (a plot) because hidden tests can grade a solver.

Task: `black_iv(price, F, K, D, T, kind)` solves in forward terms with no pricer loaded, returns NaN at or outside the discounted no-arbitrage bounds or for a NaN price, and must solve penny quotes and vols to 300%. The lesson's solver has its pricer loaded and raises.

Tests: 13 hidden, 2 examples; vols within absolute 1e-8. Eleven planted bugs each fail, first at their named test, among them plain Newton from 0.2 (diverges on the 9p put), discounting omitted, put-call parity sign, raising instead of NaN, undiscounted bounds.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; only perf-pending warnings.
2. `VOICE_BASE=app/content/courses/opt-dash python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python -I docs/reports/opt-dash-3-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set opt-dash/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed, starter fails. Shots clean.

Freshness grep: `black_iv`, `black_price`, `forward terms`, `100.4`, `146,935`, `nan`.

Overlapping screens: l9-iv-solver screens[2] (Newton's method), [4] (a step off the chart, penny quote), [5] (no volatility fits, no-arbitrage bounds), [6] (five steps and done), [7] (the safe solver, bracket plus Newton) and [8] (the solver in code with the pricer loaded), [9] (every quote in the chain); new parts: `black_iv` in forward terms with no pricer loaded, NaN at or outside the discounted no-arbitrage bounds or for a NaN price (the lesson's solver raises), penny quotes and vols to 300%, put-call parity sign and discounting.
