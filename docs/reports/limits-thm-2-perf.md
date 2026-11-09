# limits-thm level 2: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/limits-thm/homework-2.json`, item `h-prove-cycles-exponential`, index 8 (item 9 of 9; the homework had 8, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `dl-continuous`.
- Matched objective: l6 "Derive the uniform variance and the exponential survival function." It is the only objective of the level that starts with derive (l5 read, find; l7 standardise, use; l8 model, find).
- Task: a venue matching in cycles of $\tfrac1n$ s, with fill chance $\tfrac{\lambda}{n}$ per cycle (the same in every cycle, cycles independent, $n > \lambda$). (a) $P(T_n > t) = (1 - \tfrac{\lambda}{n})^{\lfloor nt \rfloor}$. (b) The limit $e^{-\lambda t}$ by a squeeze on the whole part, checked against the density's tail. (c) $\lambda = 0.5$, $t = 4$: 0.1285 at 0.1 s and 0.1347 at 0.01 s, both below $e^{-2} = 0.1353$, because $\ln(1 - x) < -x$. (d) $\operatorname{Var}(U(a, b))$ straight from the density, then mean 0.03 s and sd 0.0289 s on $[-0.02, 0.08]$.
- Rubric 2, 3, 1, 1, 3. Rows 1, 2, 3 and 5 are `required` (9 points), one for each of (a) to (d). `rubric-passes.mjs`: the only minimal pass is rows 1, 2, 3, 5. Only row 4 (why the values lie below the limit) can be left out.
- Overlapping screens: l6 screen 2 (the variance of $U(0, w)$, ordered) and screen 8 (the $[a, b]$ formula, stated by shifting); l6 screens 3 and 4, `h-exp-survival` and `h-long-exponential` (a) (the survival function as a tail integral); l3 screen 7 (the limit $(1 - \lambda/n)^n \to e^{-\lambda}$, used here as a given fact). New: the exponential survival reached as the limit of a discrete cycle model, with the squeeze for $\lfloor nt \rfloor$; the size and sign of the finite-$n$ error; the uniform variance derived on $[a, b]$ with $a < 0$, with no shift.
- Freshness grep (course folder, every hit read): `cycle`, `lfloor`, `whole part`, `0.95^`, `e^{-2}`, `audit`, `-0.02`, `0.08`, `a^2 + ab`, `b^3`. None of them is the same setup. `fresh-check.mjs --file content/courses/limits-thm/homework-2.json`: 1 advisory hit, on the existing `h-lognormal-var` (shared constants 99, 2.326, 0.01 with l7), and none on the new item.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors. Expected warning "limits-thm/L2: has a performance task, remove from perf-pending". Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/limits-thm python3 docs/reviews/voice-scan.py 35`: 0 and 0. The L1 commit split the folder's one 36-word sentence, in `h-long-exponential` of this file.
3. `<venv>/bin/python -I docs/reports/limits-thm-2-perf-numbers.py`: exit 0, 64 checks. Exact rationals for (a) and the powers. sympy for the limit, the tail integral and the uniform moments. Grids for the squeeze and for $\ln(1 - x) < -x$. Seeded simulations of the cycle model at $n = 10$ and $100$, the exponential and $D$. Passing tick sets listed.
4. `node tools/playthrough.mjs --set limits-thm/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed. A 356 px KaTeX column check and its shot (scratch `eqcheck.mjs`) found displays that ran wide. Four were split with `aligned`, and all 7 now fit.

No backlog bullets. No course.json change.
