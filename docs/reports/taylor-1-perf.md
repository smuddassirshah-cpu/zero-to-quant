# taylor level 1: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/taylor/homework-1.json`, item `h-prove-newton-error`, index 9 (item 10 of 10; the homework had 9, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skills `ty-linear`, `ty-converge`.
- Matched objective: l3 "Derive the update $x_{n+1} = x_n - f(x_n)/f'(x_n)$ from the tangent line" (the only L1 objective the verb rule matches).
- Task: (a) the update from the tangent, and when it is defined; (b) prove $e_{n+1} = \tfrac{f''(c)}{2f'(x_n)}e_n^2$ from the exact tangent error (given as a fact: l2's rule made exact); (c) for $e^x - 3$ on $[1, 1.2]$, $|e_{n+1}| \le \tfrac12 e^{0.2}e_n^2 \approx 0.611e_n^2$ and $e_{n+1} \ge 0$; (d) $x_1 = 3/e \approx 1.103638$, $e_1 \approx 0.005026 < 0.00594$, $x_2 \approx 1.0986249$, $e_2 \approx 1.26 \times 10^{-5} < 1.54 \times 10^{-5}$; optional: the guesses stay in $[\ln 3, 1.2]$.
- Rubric 2, 3, 2, 2, 1. Rows 1 to 4 `required`, one per part (a) to (d), each worded by its result; row 5 is the part the prompt marks "Optional, one more point:". `rubric-passes.mjs --item content/courses/taylor/homework-1.json#h-prove-newton-error`: one minimal pass, rows 1 to 4 (9 points); only row 5 can be left out.
- Overlapping screens: l3 screens[3] (derive the update, put in order) and [2] (correct places grow as you step); l2 screens[8] and [4] (error about $\tfrac12 f''(a)h^2$) and [5] (its sign from $f''$); homework-1 `h-babylonian` (the update for $x^2 - c$). New parts: the exact error recurrence, a bound on a stated interval checked step by step, the sign of every later error, and the invariant interval, all on $e^x - 3$, which no lesson uses.
- Freshness grep (course folder, every hit read): `e^x - 3`, `ln 3`, `3/e`, `e_{n+1}`, `f(x_n)/f`, `tangent error`, `doubles`, `[1, 1.2]`. Hits only on l3's objective and its derive feedback. `fresh-check.mjs --file content/courses/taylor/homework-1.json` (also `--min-run 10`): 0 hits; `--exam topic-1.3`: 0 hits.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors. Expected warning "taylor/L1: has a performance task, remove from perf-pending". No warning on the new item. Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/taylor python3 docs/reviews/voice-scan.py 35`: 0 and 0 (one 43-word rubric sentence was split to get there).
3. `<venv>/bin/python -I docs/reports/taylor-1-perf-numbers.py`: exit 0, 77 checks. Route 1 sympy (tangent by `series`, the identity solved symbolically, $x_1 = 3/e$, the limit $\tfrac12$ and the step map's series $h^2/2$); route 2 mpmath at 40 digits and floats, $c$ solved from the exact remainder on six starts, grids for the bound, sign and invariant interval. Passing tick sets listed.
4. `node tools/playthrough.mjs --set taylor/homework-1 --local-cdn <pkgs>`: All passed (2 longform marked by the button). With `--mobile`: the new item passes, but the run fails on the older item `h-long-bond`, three displays wider than the column at 440 px (`P(0.05) = \frac{6}{1.05} + ...`, `P(0.07) = ...`, `y_1 = 0.05 - \frac{1.7232}{-277.43} ...`). Not edited, as the brief directs; fix: split each with `aligned`.

One backlog bullet. No course.json change.
