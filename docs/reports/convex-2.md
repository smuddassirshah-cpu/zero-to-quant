# convex level 2 (Linear programmes): report

## Files (app/content/courses/convex/)

| file | screens or items | quiz | canvases and widgets |
|---|---|---|---|
| l5-linear-programmes.json | 9 screens | 4 | desk pentagon `plane` with draggable P and a live "outside: which limit" caption; `place` sentences to lines; vector `expression`s; venue `table`; hedge region with a wrong-answer patch that flips it |
| l6-corners.json | 10 screens | 3 | iso-profit line driven by a graded `slider`; vertex `table` widget (10 pairs); `tap-regions` on vertices; simplex walk and vertex proof as `order` with distractors |
| l7-lp-in-code.json | 9 screens | 3 | `console` (wrapped) for `linprog` output; status `table` widget; `code` (four HiGHS functions) |
| l8-lp-duality.json | 10 screens | 3 | dual region in $(y_1, y_2)$ as a clipped polygon with a draggable offer; weak duality `order`; trap with a wrong-option patch showing the transposed region; `code` (dual and gap) |
| review-2.json | 10 items, `pass` 0.8 | | difficulty 2 to 4, all four lessons and one level 1 recall (convexity of an LP's region) |
| homework-2.json | 8 items | | difficulty 3 to 5 (two at 5); `order` weak duality for the min form; `code` cash-flow matching as `performance: "code"` (the objective "Write ..." makes the level rule-matched); `longform` "do nothing" with a 10-point rubric |

## Gates

- Validator: 0 errors; no warnings on level 2 files.
- Voice scan on the course folder: 0 over 20 words (0 at 19 too) and 0 explanations over three sentences.
- Numbers: `docs/reports/convex-L2-numbers.py` exits 0: 128 of 128 `numbers_lib` checks, 0 two-route failures; it runs the 3 code widgets in CPython (solutions pass all tests, starters none).
- Playthrough with `--local-cdn`: every lesson, review-2 and homework-2 green on desktop, `--mobile` and `--tablet` in one run; l7 replayed after wrapping its consoles. Screenshots read; fixes: vertex label positions, hedge labels no longer show the answer, consoles wrapped.

## Runtime

HiGHS runs in Pyodide: l4 (level 1), l7, l8 and homework-2 code all pass their hidden tests in the playthrough, including the duals (`ineqlin.marginals`, `eqlin`, `upper`). No value differed between Pyodide's SciPy and CPython's 1.18.1 at the tolerances used (absolute $10^{-6}$ for solver values, $10^{-8}$ for the duality gap, plans rounded to 6 places). SciPy load time: not measurable with the current playthrough (no per-item timing; inbox bullet raised in level 1); the lessons with SciPy took 36 to 37 s across three widths against 36 s for l5 without it, so the local load is a few seconds. Each `how` says "a few seconds from cache, longer on a first visit".

## Numbers and sources

All computed twice in the script: exact vertex enumeration (fractions) against HiGHS, closed forms against `linprog` duals. Reproduced from the brief: the pentagon and profits 0, 300, 420, 480, 400; slacks $(0, 0, 1)$; marginals $(-30, -10, 0)$; infeasible pairs $(5, 5)$, $(10, 0)$, $(0, 18)$, $(6, 0)$; tie 600; walk 300, 420, 480 with edge rates $+60$, $-20$, $-60$; venue $(4000, 3000, 3000)$, 3,150p, duals 0.40, 0.10, 0.15; hedge $(3, 2)$ £6k, corners £12k and £9k, reversed rows £0; swapped row $(5, \tfrac{13}{3})$, £473.33k; $2x + y \le 14$ redundant; 9.5%, status 2 and 3; dual corners 720, 480, 600; 420 and 580; cash-flow lots $(\tfrac{13}{14}, \tfrac{10}{7}, 0, 2)$, cost $\tfrac{2804}{7}$, factors $(0.96, 0.897143, 0.85)$, 4% bond worth 95.83.

**Brief error.** "Change the profit of A to £90k and the optimum jumps to $(5, 3)$ with £510k" is wrong: at £90k, $(4, 6)$ earns 600 and $(5, 3)$ 570, so $(4, 6)$ stays optimal ($(4, 6)$ is optimal for A's profit from £40k to £120k). I used £150k: $(5, 3)$ earns £870k against 840 at $(4, 6)$, and the dual of that case is $(0, 40, 30)$ at 870; `solve_desk` and `check_duality` test it. Homework item `h2-range` asks for the £120k threshold.

Added: P at $(2, 5)$ £320k; margin row $2x + 4y \le 36$; long-short 12.5% at $(-0.5, 0.5, 1)$ against 11% with default bounds; equality-only point $(6, 4)$; 19 risk units give $(4.5, 5.5)$ and £490k; review figures (600, 6 vertices after $y \le 8$, offer 560, venue £28.50, 0.40p); homework hedge £7,200 at $(2.4, 3.2)$, 460 at £70k/£30k, cover prices $(0.3, 0.4)$, 500 rows for the minimax tracker, a second dedication case (cost 270.714286).

## Notes

- Scratchpad: this session's `19ed1109...` folder, subfolder `convex-2` (the brief's `a8ff8d32...` paths are stale).
- No `course.json` change proposed.
- Inbox: 2 bullets under "Raised later (convex level 2)".
