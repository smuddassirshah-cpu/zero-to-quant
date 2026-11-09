# opt-dash level 4: performance task

`homework-4.json`, `h4-weekend-explain`, item 8 of 8. Kind `code` (Python, standard library).

Objective: l14 "Explain a day's P&L with the Greeks and measure the residual", the only L4 match.

Task: `explain_day(book, S0, S1, r, days, q)`: a book's four terms, explained, actual and residual, from vols in points and calendar days; `bs_price` and `bs_greeks` are loaded.

Tests: 12 hidden, 1 example. Twelve planted bugs fail first at a byKey test: no ½ (2), vega times points (3), theta times days, one day, 252 days (4), residual sign, unshortened T, old vol (5), qty ignored, end-of-period Greeks (1), mean vol move on summed Greeks (6), q dropped (8).

Overlapping screens: l14 screens 6, 10, 11 (one option), l13's units screen, `h4-book` (summed Greeks, one move). New: per-position revaluation, per-option vol moves, units in code, a weekend.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/opt-dash python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python -I docs/reports/opt-dash-4-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set opt-dash/homework-4 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed, starter fails.

Freshness: `fresh-check --file` 0 hits; grep `explain_day`, `weekend`, `vol points`, `per point`, `365`, `residual`, `pnl_explain`.
