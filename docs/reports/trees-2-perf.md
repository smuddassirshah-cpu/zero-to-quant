# trees level 2: performance task

- File `app/content/courses/trees/homework-2.json`, item `h-perf-any-payoff`, index 7, kind `code`.
- Matched objective: l8 "Write a binomial pricer in Python and test it against hand calculations."
- Task: from a stub, `tree_value_delta(S, r, sigma, T, n, payoff, american)`: any payoff, European or American, the first step's delta, `ValueError` unless $d < e^{r\Delta t} < u$.
- 10 tests, 1 example. Twenty planted slips each fail a test (no discount, three wrong $q$, $n$ leaves, $T/(n + 1)$, a step short, no early exercise). The starter fails all 10.
- Overlapping screens: l8 screens 1, 2, 3, 5, 8; l7 screens 1, 2, 5, 7; l5 screen 8; homework-2 `h-code-region`; homework-1 `h-code-pricer`. New: no helpers, any payoff on $n$ steps, a capped call exercised early, delta after the max, the check with $e^{r\Delta t}$, a put exercised today.
- Gates: (1) validator `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors. (2) voice `VOICE_BASE=app/content/courses/trees python3 docs/reviews/voice-scan.py 35`: 0 and 0. (3) numbers script `venv/bin/python -I docs/reports/trees-2-perf-numbers.py`: 99 checks, 0 failures. (4) playthrough `node tools/playthrough.mjs --set trees/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed.
- Freshness grep: `tree_value_delta`, capped, strangle, delta. `fresh-check --file`: 0 hits.
