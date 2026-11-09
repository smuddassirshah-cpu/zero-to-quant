# measure-prob level 2: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/measure-prob/homework-2.json`, item `h-build-integral`, index 9 (item 10 of 10; nothing converted, the homework had 9 items).
- Kind `derivation` (longform, empty box, no tags), difficulty 5, skill `mt-integral`.
- Objective matched: l5 "Build expectation as a Lebesgue integral from simple functions." It is the only rule-matched objective in the level. l6 to l8 begin "Use" or "Tell".
- Task: for $X = \sqrt U$, build $E[X]$ from simple functions. The model takes dyadic bands $\varphi_n = \lfloor 2^nX \rfloor/2^n$ (band chances $(2k+1)/4^n$), proves they are simple, below $X$, increasing and convergent, and finds $E[\varphi_n] = (N-1)(4N+1)/(6N^2)$. It uses the supremum definition plus monotone convergence (hypotheses checked) to get $2/3$, with a layer-cake check. Then $E[Y]$ for $Y = 2\sqrt U - 1$ comes out as $5/12 - 1/12 = 1/3$.
- Rubric 2, 2, 2, 3, 1. Row 4 (the limit is $E[X]$) is `required`. Row 3 accepts any exact simple-function mean.
- Fresh: the lessons use $U^2$ (l5 bands and code), exponential losses, $2^K$, $nU^n$ and $1/\sqrt U$ only as a dominating bound (l7). Grep terms: `sqrt U`, `sqrt{U}`, `tfrac23`, `2k+1`, `floor`.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "measure-prob/L2: has a performance task, remove from perf-pending".
2. `VOICE_BASE=app/content/courses/measure-prob python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/measure-prob-2-perf-numbers.py` (venv with sympy): exit 0, 25,187 checks. Band sum against closed form and midpoint sums. Exact-grid checks of every property of $\varphi_n$ using `isqrt`. Shortfall $(3N+1)/(6N^2)$. $Y^\pm$ by layer cake, by antiderivative and by sympy.
4. `node tools/playthrough.mjs --set measure-prob/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed (2 longform marked by the button). A scratch KaTeX render of the model and rubric in the 356 px card column showed all four display equations fit. All are split with `aligned` where needed. The marked 440 px shot agrees.

No backlog bullets. No course.json change.

Overlapping screens: l5-lebesgue-integral screens[0] and [1] (dyadic bands $\varphi_n$ for $X = U^2$), [2] (simple functions and their integral), [5] (the layer-cake formula), [8] (monotonicity passes to the supremum), [9] (`dyadic_mean(n)` in code); new parts: $X = \sqrt U$ with band chances $(2k+1)/4^n$ proved simple, below $X$, increasing and convergent, $E[\varphi_n] = (N-1)(4N+1)/(6N^2)$, monotone convergence with its hypotheses checked to reach $2/3$, and $E[Y]$ for $Y = 2\sqrt U - 1$.
