# opt-dash level 2: performance task

`homework-2.json`, `h-asian-cv`, item 8 of 8 (added; cap 12). Kind `code` (Python, numpy).

Objective: l7 "Implement a Monte Carlo pricer with a variance reduction trick." Chosen over l5 because the lessons already code `bs_price` in full.

Task: `asian_cv(...)` prices an arithmetic Asian call with $X = e^{-rT}A$ as control; the learner derives $E[X]$ (a sum of discounted forwards). The lessons code only a European control on $S_T$; the Asian appears only as a plain-path ticket question. One stated draw call makes values exact.

Tests: 10 hidden, 2 examples; seeded values within relative 1e-5, a one-fixing and an unbiasedness check, and an error under half the plain error. Eleven planted bugs fail, among them payoff undiscounted, wrong or undiscounted control mean, today in the average, independent fixings, raw-payoff error.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; only perf-pending warnings.
2. `VOICE_BASE=app/content/courses/opt-dash python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python -I docs/reports/opt-dash-2-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set opt-dash/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed, starter fails. Shots clean.

Freshness grep: `asian_cv`, `Asian`, `n_fix`, `fixing`, `control variate`, `6.156`.

Overlapping screens: l7-mc-pricer screens[2] (the standard error), [3] (antithetic pairs), [4] (`mc_price` in code), [5] (a control variate on the discounted share price, a European control) and [9] (an Asian call on a trade ticket, by plain paths); new parts: `asian_cv` with $X = e^{-rT}A$ as the control, the learner deriving $E[X]$ as a sum of discounted forwards, fixings drawn along one path, a one-fixing check, and an error under half the plain error.
