# opt-dash level 2: performance task

`homework-2.json`, `h-asian-cv`, item 8 of 8 (added; cap 12). Kind `code` (Python, numpy).

Objective: l7 "Implement a Monte Carlo pricer with a variance reduction trick." Chosen over l5 (Black-Scholes pricer) because the lessons already code `bs_price` in full, and a pricer with a control and its error is the larger product.

Task: `asian_cv(...)` prices an arithmetic Asian call with $X = e^{-rT}A$ as control; the learner derives $E[X]$ (a sum of discounted forwards). The lessons code only a European control on $S_T$; the Asian appears only as a plain-path ticket question. Normals are drawn in one stated call so tests can expect exact values.

Tests: 10 hidden, 2 examples; seeded values within relative 1e-5, one fixing against Black-Scholes, unbiased against a 4,000,000-path reference, error under half the plain error. Eleven planted bugs fail: payoff undiscounted, control mean of $S_T$, control mean undiscounted, today in the average, independent fixings, raw-payoff error, $b = 1$, $S_T$ control, yield left out twice, no ValueError. A `ddof` mismatch inside $b$ alone passes, by design.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; only perf-pending warnings.
2. `VOICE_BASE=app/content/courses/opt-dash python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python -I docs/reports/opt-dash-2-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set opt-dash/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed, starter fails. Shots clean.

Freshness grep: `asian_cv`, `Asian`, `n_fix`, `fixing`, `control variate`, `standard_normal((`, `6.156`, `97.74`.
