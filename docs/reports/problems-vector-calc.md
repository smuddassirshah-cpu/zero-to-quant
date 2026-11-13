# Problem sets: vector-calc

Chained problem sets for `vector-calc` (brief `docs/briefs/chained.md`, prompts `docs/briefs/chained-prompts.md`, Author). Number script: `docs/reports/problems-vector-calc-numbers.py` (run with `<scratchpad>/venv/bin/python`; exit 0).

## Level 1: `problems-1.json` (fields and line integrals, 45 minutes)

| Item | Parts | Kinds | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| `p-bead-semicircle` | 5 | numeric, expression, numeric, numeric, numeric | l1 (field value and size), l2 (scalar integral along the semicircle), l3 (work) | 3 |
| `p-two-routes-cubic` | 5 | expression, numeric, numeric, numeric, choice | l2 (parametrised curve), l3 (work on two routes, a loop), l4 (no potential) | 4 |
| `p-cubic-potential` | 4 | expression (vector), expression, expression, numeric | l1 (field value, read as a gradient), l4 (test, potential), l3 (work) | 4 |
| `p-ellipse-family` | 5 | numeric, expression, expression, numeric, expression | l4 (the $k$ that makes it conservative, potential), l3 (circulation on an ellipse), l2 (parametrised ellipse) | 5 |

19 parts, 18 typed (95%), 1 choice (a judgement: what a non-zero loop work says). Every lesson appears; each item draws on at least two. Skills `vk-fields`, `vk-line` (the level's lessons).

Reuse grep (course folder, then `app/content/` for the stories), each hit judged:
- `x + 2y` in homework-3, l4, l8, review-1, review-3: other fields (`(x + 2y, ...)` components in different fields); our field $(2x - y, x + 2y)$ appears nowhere. Not reuse.
- `xy^2` in l1 (a wrong form of the potential $x^2y$), l5, review-2: different objects. Our potentials $x^3 + xy^2$ and $xy^2 + 3xy$ appear nowhere in the course.
- `t^3` in l3, l4, homework-2: $[t^3]_0^1$ in working, $16t^3$, the folium $\tfrac{3t}{1+t^3}$. The cubic route $(t, t^3)$ is not used. Not reuse.
- `6\pi` and 18.85 in l7 (an ellipse area). We moved the level 1 ellipse to $(2\cos t, 5\sin t)$, circulation $20\pi$, so no figure is shared. `\sqrt5` in l2, l9 ($|(1, 2)|$, other settings).
- `(1, 3)` in homework-1, review-1, review-2 (points in other fields); `(2, 3)` in l1 (the point $\mathbf F(2, 3)$ of a different field). Single points, different fields and tasks.
- `semicircle` in l6 (Green's theorem on a half disc), `wire` in homework-1, l9 to l12; our story is a bead on a semicircle, and "bead" is in no file of `app/content/`.
- Across `app/content/`: $f = x^3 + xy^2 + y$ in multivar review-1 (partial derivatives, another course, another function); $3x^2 + y^2$ in multivar l8 (a bowl for gradient descent) and complex problems-2; `2x - y,` in linear-maps problems-3 (a linear map). Other courses, other tasks. Not reuse.
- `fresh-check --file ... --cross-numbers`: 0 hits.

Checks: validator 0 errors, no warning on the file; voice scan 0 and 0; `grade-all --file`: 19 widgets, 0 failures; playthrough desktop (`--why`, 39 slips routed) and `--mobile`: green; screenshots at 440 px read, no layout fault; number script exit 0.
