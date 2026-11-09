# estimation level 2: performance task

- `homework-2.json` item `hw2-pareto-tail`, index 8 (9 of 9; appended, nothing converted). Kind `derivation`, difficulty 5.
- Matched objective: l6 "Derive the maximum likelihood estimate for a coin and for a normal mean." (with "Check that a stationary point is a maximum, and check the boundaries.").
- Task: Pareto losses above a known £1m threshold. (a) $\hat\alpha = n/\sum\ln x_i$, $\ell'' < 0$, both ends. (b) $\ln X$ exponential, $E[1/S] = \alpha/(n-1)$, bias, unbiased multiple. (c) 1.85, 1.54, tail chances 0.014 and 0.029. Optional: every loss at £1m.
- Rubric 2, 2, 3, 2, 1; rows 1 to 4 `required`. `rubric-passes.mjs`: minimal pass rows 1 to 4 (9 points); only row 5 (optional part) can be left out.
- Overlapping screens: l6 screens 2 to 4, 7, 10; l7 screens 3, 7; `hw2-poisson-order`, `hw2-longform`; l3 bias of $\hat v$. New: Pareto law, change to an exponential, exact bias via $E[1/S]$, the tail chance.
- Freshness grep, hits read: `Pareto`, `tail index`, `threshold`, `loss`, `1/S`, `1.85`, `1.54`, `n}{n - 1}`, `second derivative`. `fresh-check.mjs --file`: no hit on the item.

Gates:
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, expected perf-pending warning; manifest restored.
2. Voice, `VOICE_BASE=app/content/courses/estimation python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/estimation-2-perf-numbers.py`: exit 0, 66 checks (sympy, quadrature, seeded bias simulation).
4. Playthrough, `node tools/playthrough.mjs --set estimation/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed; 440 px model shot: no display scrolls.

Backlog: 1 bullet. No course.json change.
