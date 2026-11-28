# gpt level 4: performance task

`homework-4.json`, `h-scaling-fitter`, item 1 of 6. Kind `code` (Python).

Matched objective: l15-power-laws "Fit a power law by least squares in log space and read its exponent." (also l16 "Choose a model size and token count for a fixed compute budget.", and l13 and l14, whose objectives start with "Derive").

Task: from a stub starter, `fit_scaling(runs)` fits $L = E + A/N^{\alpha} + B/D^{\beta}$ to a list of `[N, D, L]` runs, with $\alpha$ and $\beta$ on a 0.01 grid from 0.10 to 0.60 and $E$, $A$, $B$ by linear least squares for each pair; `best_split(p, C)` returns the compute-optimal `(N, D)` for $C = 6ND$ in closed form. NumPy only: the brief allowed a single-variable fit with a floor if the full fit was too slow without SciPy; the grid plus least squares fits the full law in well under a second, so no SciPy import (and its load time) is needed.

Tests: 8 hidden, 2 examples. Two noise-free sets of 12 planted runs (exponents 0.35 and 0.32, and Chinchilla's 0.34 and 0.28) must return their exponents exactly and their constants to $10^{-6}$; Chinchilla's published law gives the split at $5.76 \times 10^{23}$ exactly (about 93 tokens per parameter); a split from a fitted set; a set with 0.3% noise must land its exponents within 0.03 (the number script measures 0.37 and 0.35 against 0.35 and 0.32) and its split within a factor of 1.5 (measured 1.07); the split spends the whole budget. Mutants: the data's exponent used for the model (test 4), no floor column (test 1), 20 tokens per parameter (test 4), a grid of 0.05 (test 1).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/gpt/ python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 explanations over three sentences.
3. Numbers script: `node tools/run-number-scripts.mjs --python <venv> --only gpt-L4`: passed (strict coverage).
4. Playthrough: `node tools/playthrough.mjs --set gpt/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails; `grade-all.mjs --file ... --code`: 0 failures (solution, starter, mutants).

Overlapping screens: l15-power-laws screens[5] (`fit_power_law`) and l16-a-fixed-budget screens[5] (`chinchilla_loss`, `optimal_split`). New here: two variables and a floor, fitting the exponents by search rather than reading a slope, and the split in closed form from fitted constants.
