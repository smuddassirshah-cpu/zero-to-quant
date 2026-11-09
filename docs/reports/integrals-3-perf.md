# integrals level 3: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/integrals/homework-3.json`, item `h-derive-parts-tail`, index 9 (item 10 of 10; the homework had 9, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `in-techniques`.
- Matched objective: l10 "Derive integration by parts from the product rule". It is the only L3 objective that starts with derive, prove, write, build or code (l11 "Show", l12 "Approximate ... in code" start with other verbs).
- Task: (a) the definite parts formula from the product rule, saying where each assumption is used; (b) $\int_1^\infty \frac{\ln x}{x^3}\,dx = \tfrac14$, worked on $[1, b]$ with every limit justified.
- Rubric 3, 1, 3, 2, 1; rows 1, 3, 4, 5 `required` (9 points): (a), the finite-range result, the limit, the value. `rubric-passes.mjs`: the only minimal pass is rows 1, 3, 4, 5; only row 2 (why the split helps) can be left out. Rows accept parts with $u = \ln x$ or the substitution $x = e^s$ (new limits 0 and $\ln b$) then parts, and for the limit a bound ($\ln b \le b - 1$ by comparing $\tfrac1t \le 1$), exponentials beating powers, or L'Hôpital. The only hypothesis, continuous derivatives, is used where the model says.
- Overlapping screens: l10 screen 8 (the same derivation, indefinite, put in order), l10 screens 2 to 6 (parts on $x\cos x$, $x\ln x$, $\ln x$, $x^2e^x$), l11 screens 1, 2 and 6 ($\int_1^b$ then $b \to \infty$; $x^{-3}$), l9 screen 7 (new limits), `h-parts-log`, `h-log-tail` ($\frac{\ln x}{x}$ diverges), `h-long-duration` and `h-ramp-perpetuity` ($b\,e^{-rb} \to 0$), `r-parts-infinite`, `r-sub-infinite`. New: the definite form with $[uv]_a^b$ and the use of each assumption, a log over a power on an infinite range, the bound on $\ln b$ by comparing integrands, and two routes to one closed form.
- Freshness grep (course folder, every hit read): `ln x}{x`, `x^{-3}`, `x^3}`, `e^{-2s}`, `e^{-2x}`, `x = e^`, `pital`, `b - 1`, `ln b`; `fresh-check.mjs --file` 1 hit, the code name `trapezium` on `items[4]`, present at the base commit; 0 on the new item at `--min-run 8 --min-share 0`.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "integrals/L3: has a performance task, remove from perf-pending". Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/integrals python3 docs/reviews/voice-scan.py 35`: 1 and 3, all present at the base commit, none in the new item (see `integrals-1-perf.md`).
3. `<venv>/bin/python -I docs/reports/integrals-3-perf-numbers.py`: exit 0, 130 checks. Sympy: the product rule, the closed form on $[1, b]$ by integration and by differentiation back, both limits, the improper value, the substitution to $s\,e^{-2s}$ and its closed form equal at $B = \ln b$. Scipy: `quad` on $[1, b]$, $[0, B]$ and $[1, \infty)$, the parts formula on four pairs, the bounds on grids.
4. `node tools/playthrough.mjs --set integrals/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed. Model shot at 1280 and 440 px: 9 display equations, none scroll sideways, no page errors.

No backlog bullets. No course.json change.
