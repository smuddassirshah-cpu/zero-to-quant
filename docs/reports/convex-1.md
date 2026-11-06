# convex level 1 (Convexity): report

## Files (app/content/courses/convex/)

| file | screens or items | quiz | canvases and widgets |
|---|---|---|---|
| l1-convex-sets.json | 10 screens | 4 | plane discs and ellipse with draggable A, B and derived Q; pair plane + space simplex; capped triangle; risk ellipse; code |
| l2-convex-functions.json | 10 screens | 4 | plane chords riding $x^2$ and $x^3$; tangent on $e^x$; space bowl with a slider widget on $b$; space trap surface; code (NumPy) |
| l3-local-is-global.json | 10 screens | 4 | plane hidden field + trajectory (ball rolling), tap-regions, contour, code |
| l4-recognising-convex-problems.json | 9 screens | 4 | table with `tap: "rows"`, contours, epigraph `order`, code (SciPy `linprog`) |
| review-1.json | 10 items, `pass` 0.8 | | difficulty 2 to 4, all four lessons |
| homework-1.json | 9 items | | difficulty 3 to 5 (two at 5), `order` derivation, `code` item (numerical Hessian), `longform` performance task |

Performance task: `h1-colleague-qp`, `performance: "derivation"` (lesson objectives start with "Prove", so the level is rule-matched).

## Gates

- Validator: 0 errors; no warnings on level 1 files.
- Voice scan (`VOICE_BASE=app/content/courses/convex/`): 0 over 20 words and 0 explanations over three sentences (also 0 at 19).
- Numbers: `docs/reports/convex-L1-numbers.py` exits 0: 177 of 177 `numbers_lib` checks, 0 two-route failures; it also runs all 5 code widgets in CPython (solutions pass every test, starters pass none).
- Playthrough with `--local-cdn` (session pkgs folder): every lesson, review-1 and homework-1 green on desktop, and again with `--mobile --tablet` (440, 1032, 1376). Screenshots read at all widths; fixes made: pair unstacked, generalise labels removed, trap camera turned, `maxHeight: 330` on every plane, space and pair canvas.

## Numbers and sources

Every value is computed twice in the script (fractions or closed forms against NumPy, SciPy HiGHS or SLSQP, RK4, a 2,000,000-draw simulation for Jensen). The planner's figures all reproduced: midpoint 1.5; $(0.30, 0.24, 0.46)$; cap corners and 9.5%; 30%, 40%, 25%; 25% pair and 24% midpoint; 15.364%; gap 2, $-1$, $-4$; $2 \pm b$; $-2$, 6; $4 \pm \sqrt{13}$ (0.3944, 7.6056); $-0.2$, 2.2; 2.828 and 4; $-1.3008$, $-3.5139$, 1.1309, $-1.0702$, 0.1699; basin ends $-1.30084$ and 1.130901. Added: relaxed 25% optimum 9.51% at $(0.017, 0.465, 0.519)$ (SLSQP against KKT bisection), 18.03%, £565.69 against £800, Jensen gap 0.2231, cap $\tfrac49$ for a 9% floor, 8.6% under a 40% cap, 22.33% at the 9% optimum.

## l3 trajectory

Hidden `field` P = $-f'$, Q = $-f'^2$; `trajectory` `length: 3`, `step: 0.003` (1,000 RK4 steps). The default step (length/200) drifted off the curve for starts near $\pm 2$ ($y$ error up to 2); at 0.003 the RK4 path stays on the curve and ends within $10^{-6}$ of 1.1309 or $-1.3008$ (checked in the script). The $x^2$ screen uses length 6, step 0.006.

## Runtime

`linprog(method="highs")` runs in Pyodide (l4 code screen green), so the level 2 check passes. `res.multipliers` was not used.

## Notes for the main session

- The brief's scratchpad paths (`a8ff8d32...`) are stale; I used this session's scratchpad (`19ed1109...`), subfolder `convex-1`.
- LEVEL-BRIEF says do not commit; the orchestrator said commit per level, which I followed.
- Review has 10 items (the brief's maximum); AUTHORING section 11 suggests 12 or more for a level others require, for fresh test-out papers.
- No `course.json` change proposed.
- Inbox: 4 bullets under "Raised later (convex level 1)".
