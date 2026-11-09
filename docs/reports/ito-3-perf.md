# ito level 3: performance task (perf retrofit)

- File `app/content/courses/ito/homework-3.json`, item `h-derive-black`, index 7 (8 of 8), appended. Nothing converted or changed.
- Kind `derivation`, difficulty 5, skills `it-pricing`, `it-calculus`, no tags.
- Objective: l9 "Derive the Black-Scholes equation by hedging away the noise." New setting: a European claim on the forward price $F_t = S_te^{r(T_F - t)}$ (the forward price of ito l8 screen 10, level 2; the prompt defines it), hedged with shares and cash. Product: $V_t + \tfrac12\sigma^2F^2V_{FF} - rV = 0$, holding $e^{r(T_F - t)}V_F$ shares.
- Rubric: assumptions 2, Itô for $F$ and $V$ 2, hedge with drift cancelling and no arbitrage 3 (`required`), equation 2, check 1. The model justifies each line and gives two checks.
- Gates: (1) `cd app && node tools/validate.mjs`: 0 errors. (2) `VOICE_BASE=app/content/courses/ito python3 docs/reviews/voice-scan.py 35`: 0 and 0. (3) `python3 docs/reports/ito-3-perf-numbers.py`: exit 0, 56 checks in the venv (sympy plus seeded numerics and a discrete hedge under two drifts). (4) `node tools/playthrough.mjs --set ito/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed. A scratch script (`scratchpad/ito-perf/model-shot.mjs`) found 0 sideways display equations and 0 inline overflow at 440 px, after two inline splits.
- Freshness grep: forward price, T_F, delivery, F_T, V_F, Black, e^{0.06}. `fresh-check.mjs --file`: no hit on item 7.
- Backlog: 1 bullet.
- Overlapping screens: ito l9 screen 2 orders the hedge argument on the share. New: the forward as the variable, Itô for $F$, the ratio $e^{r(T_F - t)}V_F$ and no first-derivative term.
