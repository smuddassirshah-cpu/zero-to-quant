# integrals level 2: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/integrals/homework-2.json`, item `h-derive-window`, index 9 (item 10 of 10; the homework had 9, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skills `in-ftc`, `in-apply`.
- Matched objective: l5 "Derive the fundamental theorem from the accumulation function." It is the only L2 objective that starts with derive, prove, write, build or code (l6 "Explain" is not matched in Stage 1).
- Task: (a) prove $A'(x) = f(x)$ for continuous $f$, both signs of $h$, saying where continuity is used; (b) $G(x) = \int_x^{2x} f$ gives $G'(x) = 2f(2x) - f(x)$; (c) for the normal density, the window $[x, 2x]$ holds the most chance at $x^* = \sqrt{2\ln 2/3} \approx 0.680$, shown to be a maximum.
- Rubric 2, 3, 2, 2, 1; rows 2 to 5 `required` (8 points): (a)'s squeeze, (b), the point and the maximum. `rubric-passes.mjs`: the only minimal pass is rows 2 to 5; only row 1 (the strip and its bounds, a step of (a)) can be left out. Rows accept the min and max squeeze or an $\varepsilon$ band, a split at any fixed point, and the sign of $G'$ or $G'' < 0$. The only hypothesis stated, continuity, is used in both places the model names.
- Overlapping screens: l5 screens 2, 3 and 6 (the strip, rise over run, the squeeze for $h > 0$ put in order), l5 screen 7 and quiz 1 (a fixed lower limit; $\int_1^x e^{t^2}$), l7 screen 8 (the second form, which is not asked), `h-long-ftc` (a) (the same proof written out, with $h < 0$ in a sentence), `h-ftc-chain` (upper limit $x^3$), `r-ftc-cos`. New: a moving lower limit, the window derivative $2f(2x) - f(x)$, the $h < 0$ case written out, and an optimisation on a function with no antiderivative formula.
- Freshness grep (course folder, every hit read): `e^{-t^2}`, `e^{-x^2}`, `int_x^`, `{2x}`, `lower limit`, `ln 2`, `varphi`, `window`; `fresh-check.mjs --file` 1 hit, on `items[6]` (`h-ev-triangle` against limits-thm l5), present at the base commit; 0 on the new item at `--min-run 8 --min-share 0`.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "integrals/L2: has a performance task, remove from perf-pending". Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/integrals python3 docs/reviews/voice-scan.py 35`: 1 and 3, all present at the base commit, none in the new item (see `integrals-1-perf.md`).
3. `<venv>/bin/python -I docs/reports/integrals-2-perf-numbers.py`: exit 0, 124 checks. Sympy: $A' = f$, $G = A(2x) - A(x)$, the Leibniz rule for a general $f$, the factorisation, the single root, $G''(x^*) = -6x^*\varphi(2x^*)$. Scipy: the squeeze bounds on four functions with both signs of $h$, `quad` against the normal cdf, `minimize_scalar` and a grid for the maximiser, sign checks.
4. `node tools/playthrough.mjs --set integrals/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed, 2 longform marked by the button. Model shot at 440 px: one display scrolled (the split of $G$); split with `aligned`, now 7 displays and none scroll, no page errors.

No backlog bullets. No course.json change.
