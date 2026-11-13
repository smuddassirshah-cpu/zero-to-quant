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

## Level 2: `problems-2.json` (Green's theorem, 50 minutes)

| Item | Parts | Kinds | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| `p-rectangle-edges` | 4 | expression, numeric, numeric, numeric | l5 (scalar curl), l6 (circulation by Green, then edge by edge) | 4 |
| `p-cycloid-arch` | 5 | expression, numeric, expression, numeric, numeric | l7 (area as $-\oint y\,dx$), l6 (choosing $P$ with $-P_y = y$ for the moment) | 5 |
| `p-triangle-flux` | 4 | expression, numeric, numeric, numeric | l5 (divergence), l8 (outward flux by the divergence form, then edge by edge) | 4 |
| `p-quadrilateral-plot` | 4 | numeric x 4 | l7 (edge formula, shoelace area), l8 (flux), l6 and l5 (constant divergence and curl times area) | 3 |

17 parts, all typed. Every lesson appears; each item draws on at least two. Skills `vk-fields`, `vk-theorems`, `vk-line`.

Reuse grep, each hit judged:
- `[0, 3]` in l11 and review-3: a box side in 3D, not this rectangle. `(1, 3)` in review-2 (a point for a Laplacian), homework-1, review-1: single points. `(4, 0)` and `(0, 2)`: l7 and homework-2 use the quadrilateral $(0,0), (4,0), (4,3), (1,4)$ and the triangle $(0,0), (2,0), (0,2)$ (homework-2 h9). Our triangle is $(0,0), (4,0), (0,2)$ and our quadrilateral $(0,0), (5,1), (4,5), (1,3)$: no shared shape or number set. I first drew the triangle $(0,0), (2,0), (0,2)$, found it in homework-2 h9, and moved it.
- `5\pi` in homework-2, l8, review-3 and `3\pi` in l7, l8, l10, l11, review-2: other integrals (annuli, the cardioid $\tfrac{3\pi}{2}$, spheres). Our pair is the cycloid arch, $3\pi$ and $\tfrac{5\pi}{2}$; "cycloid", $t - \sin t$ and $1 - \cos t$ appear in no course file.
- `4x` in l4: the term $4xy$ of a different expression. The fields $(y^3 - 4y, xy^2 + 2x)$, $(x^2 + y, 2xy)$ and $(2x - 4y, x + y)$ appear in no course file.
- `fresh-check --cross-numbers`: 0 hits, 15 advisories, all on `p-quadrilateral-plot` sharing three small whole numbers (from 21, 23, 28, 29, 42, 70, 84) with items in brainteasers, equations, markov, mental, testing and functions files. Other courses, unrelated settings: coincidence, not reuse.

Checks: validator 0 errors, no warning on the file (two `[wrong-band]` warnings on fractional slips in whole-number parts went when I replaced those slips, and two long questions were split); voice scan 0 and 0; `grade-all --file`: 17 widgets, 0 failures; playthrough desktop (`--why`) and `--mobile` green; screenshots at 440 px read, no layout fault; number script exit 0.

## Level 3: `problems-3.json` (surfaces and space, 55 minutes)

| Item | Parts | Kinds | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| `p-saddle-roof` | 4 | expression (vector), expression, numeric, numeric | l9 (graph parametrisation, normal, $dS$, area), l10 (upward flux) | 3 |
| `p-open-tank` | 4 | expression, numeric, numeric, numeric | l11 (flux out of a closed box), l10 (flux through one face) | 4 |
| `p-slanted-ellipse` | 5 | expression (vector) x 2, expression, numeric, numeric | l12 (circulation by Stokes), l9 (the plane piece and its normal), l10 (flux of the curl) | 4 |
| `p-can-curl` | 5 | expression (vector), numeric x 4 | l12 (Stokes on the base disc), l11 (closed surface, $\nabla \cdot (\nabla \times \mathbf F) = 0$), l10 (flux through the lid) | 5 |

18 parts, all typed. Every lesson appears; each item draws on at least two. Skills `vk-surface`, `vk-theorems`.

Reuse grep, each hit judged:
- `[0, 2] \times [0, 1] \times [0, 3]` is the box of l11's code screen ("Both sides by machine"). My first tank used that box; I moved it to $[0, 4] \times [0, 1] \times [0, 2]$ with the field $(xz, y^2, 3z)$, which appear nowhere in the course.
- `z = xy` in homework-1 and l4: the term $f_z = xy$ of a potential, not a surface. `saddle` in l5: the flow of $\nabla(x^2 - y^2)$. Our saddle surface over $x^2 + y^2 \le 3$ is new.
- `x^2 + y^2 \le 4` in homework-3, l11, l12: discs under other surfaces (a cylinder of height 3, a paraboloid). The ellipse cut by $z = 2 - x$ and the field $(-yz, xz, xy + 3y)$ are new. The text `2 - x` elsewhere is only part of $y^2 - x^2$ or of `x1 * y2 - x2 * y1` in code.
- The can: fresh-check listed the shared formula $x^2 + y^2 = 9$ with my own `problems-1` bead circle, so I resized the can to $x^2 + y^2 = 16$. `16\pi` and `32\pi` then occur in review-3 (the flux of $(x, y, z)$ out of a sphere of radius 2, and its slip $16\pi$) and l11, review-1: single multiples of $\pi$ in unrelated settings. `14\pi` (homework-2, an annulus integral) and `18\pi` (review-1, a work) likewise.
- `lid` occurs in l9 to l12 and homework-3 as the word for closing a surface; our tank and can are new stories ("tank" and "can" are in no course file).
- `fresh-check --cross-numbers` after the changes: 0 hits, 0 advisories.

Checks: validator 0 errors, no warning on the file (one `[O2-explain-answer]` and one long question fixed); voice scan 0 and 0; `grade-all --file`: 18 widgets, 0 failures; playthrough desktop (`--why`) and `--mobile` green; screenshots at 440 px read, no layout fault; number script exit 0 (748 checks over the three sets).

## Number script

`problems-vector-calc-numbers.py` checks each numeric key two ways: sympy on the hand-derived integrand or region, and scipy `quad`, `dblquad` or `tplquad` on the field along the parametrised curve or surface, with derivatives by central differences (never the hand formula). Every `wrong` value is recomputed from its named slip, shown outside the key band and clear of the other slips, and has a `byKey` line. Expression keys, accepted forms and wrong forms are compared with the sympy truth at random points. Key figures printed in feedback and explain are checked as text, and `numbers_lib.Level.check_wrongs` runs on each set.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under `Raised later (problems vector-calc):` (the explain-answer check misses exact forms; small whole numbers drive cross-course advisories).
