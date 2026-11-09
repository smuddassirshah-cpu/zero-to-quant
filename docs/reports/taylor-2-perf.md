# taylor level 2: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/taylor/homework-2.json`, item `h2-prove-perpetuity-series`, index 9 (item 10 of 10; the homework had 9, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skills `ty-taylor`, `ty-finance`.
- Matched objective: l7 "Derive the Maclaurin series of $e^x$, $\sin x$ and $\ln(1 + x)$". l5 "Build a quadratic approximation..." and l6 "Build a Taylor polynomial of any order..." also match (verb build, so `code`); l7's derive was chosen because its product, a series with its general term proved for every $k$, is the level's whole method and the course has no Python strand.
- Task: a £5 perpetuity, $P(y) = 5/y$, at $y_0 = 5\%$. (a) $P^{(k)} = (-1)^k k!\,5\,y^{-(k+1)}$ by induction and $f(h) = 100\sum(-20h)^k$; (b) $D = 20$, $C = 800$ read off the coefficients; (c) the second-order rule's exact error $-100u^3/(1 + u)$, $u = 20h$, shrinking like $h^3$; (d) $\pm 1\%$: rule £84.00 against £83.33 (67p high), £124.00 against £125.00 (£1.00 low); optional: the series works only for $|h| < 0.05$.
- Rubric 3, 2, 2, 2, 1. Rows 1 to 4 `required`, one per part (a) to (d), worded by result; row 5 is the part marked "Optional, one more point:". `rubric-passes.mjs --item content/courses/taylor/homework-2.json#h2-prove-perpetuity-series`: one minimal pass, rows 1 to 4 (9 points); only row 5 can be left out.
- Overlapping screens: l7 screens[4] ($\tfrac{1}{1 - x}$ coefficients) and [6] (a pattern proved for every $k$, for $\ln(1 + x)$); l8 screens[4], [5] and [7] (the second-order rule at $\pm 1\%$); homework-2 `h2-zero-coupon` (duration, convexity and $\pm 1\%$ estimates for a zero). New parts: a perpetuity, which no lesson uses; $D$ and $C$ read from series coefficients; the rule's error in closed form; where the series fails although the price exists.
- Freshness grep (course folder, every hit read): `perpetuit`, `5/y`, `for ever`, `geometric`, `1/(1 - x)`, `ratio`, `convexity`, `1%`. Hits are the screens above. `fresh-check.mjs --file content/courses/taylor/homework-2.json --min-run 10`: 0 hits; `--exam topic-1.3`: 0 hits.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors. Expected warning "taylor/L2: has a performance task, remove from perf-pending"; none on the new item. Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/taylor python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python -I docs/reports/taylor-2-perf-numbers.py`: exit 0, 91 checks. Route 1 sympy (`diff` to order 12, the induction step, `series` coefficients, the error and its $h^3$ limit); route 2 exact `Fraction` repricing, float finite differences and partial sums. Passing tick sets listed.
4. `node tools/playthrough.mjs --set taylor/homework-2 --local-cdn <pkgs>`: All passed. With `--mobile`: the new item passes; the run fails on the older item `h2-zero-coupon`, three displays wider than the column at 440 px (`P'(y) = -1000(1 + y)^{-11} \quad ...`, `P''(y) = ...`, `D = -\frac{P'}{P} = ...`). Not edited; fix: split each with `aligned`.

No backlog bullets. No course.json change.
