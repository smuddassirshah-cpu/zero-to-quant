# Problem sets: multivar (brief `docs/briefs/chained.md`)

Files: `app/content/courses/multivar/problems-1.json` ("Problems: functions of two variables", 30 minutes), `problems-2.json` ("Problems: gradients", 35 minutes), `problems-3.json` ("Problems: optimisation", 40 minutes), `problems-4.json` ("Problems: multiple integrals", 45 minutes), `problems-5.json` ("Problems: changing variables and many constraints", 50 minutes). Numbers: `docs/reports/problems-multivar-numbers.py` (exits 0, 718 checks). The JSON was written from generators in the scratchpad (`multivar-problems/gen.py` for sets 1 to 3, `gen45.py` with `items45.py` for sets 4 and 5), not committed.

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-stretched-bowl | 4 (4 / 0) | l1, l2, l4 | 3 |
| problems-1 | p-mixed-both-ways | 5 (5 / 0) | l2, l3 | 4 |
| problems-1 | p-dollar-holding | 5 (5 / 0) | l2, l3, l4 | 5 |
| problems-2 | p-slopes-around | 5 (5 / 0) | l5, l6 | 3 |
| problems-2 | p-two-book-risk | 5 (5 / 0) | l5, l7 | 4 |
| problems-2 | p-fit-descent | 5 (5 / 0) | l5, l8 | 5 |
| problems-3 | p-two-level-points | 5 (4 / 1) | l9, l10 | 4 |
| problems-3 | p-capital-limit | 5 (4 / 1) | l9, l10, l11 | 4 |
| problems-3 | p-min-variance-pair | 5 (5 / 0) | l11, l12 | 5 |
| problems-4 | p-weighted-rectangle | 4 (4 / 0) | l13, l14 | 3 |
| problems-4 | p-corner-sprinkler | 5 (5 / 0) | l14, l15 | 4 |
| problems-4 | p-drone-landing | 5 (5 / 0) | l15, l16 | 5 |
| problems-5 | p-three-strategies | 5 (4 / 1) | l19, l20 | 5 |
| problems-5 | p-dome-tent | 5 (5 / 0) | l17, l18 (polar from l15) | 4 |
| problems-5 | p-triangle-field | 5 (5 / 0) | l17, l20 (inner limits from l14) | 3 |

Typed parts: level 1 14 of 14, level 2 15 of 15, level 3 13 of 15, level 4 14 of 14, level 5 14 of 15. Expression parts: 6, 6, 4, 6 and 4 (pairs are graded entry by entry; `form: "expanded"` on the variance quadratic so the prose's bracketed form fails). Every lesson of each level appears in at least one problem, and every problem draws on at least two.

Level 1: p-stretched-bowl finds a contour level, the partials, the $\Delta y$ that keeps $f$ on the contour (chain rule with $\frac{df}{dt} = 0$), then the exact change. p-mixed-both-ways finds $f_x$, $f_{xy}$, $f_{yx}$ the other way, then predicts $f_x(2, 1.1)$ from the mixed partial. p-dollar-holding values a dollar holding in pounds: $V_P$, $V_X$, the daily rate of $V$, $V_{PX}$, then the drift of the sterling delta ($V_{PP} = 0$).

Level 2: p-slopes-around runs gradient, steepest slope, a directional derivative, the contour arrow and the angle for half the steepest slope. p-two-book-risk takes $\sigma = \sqrt{x^2 + y^2}$ for two uncorrelated books: gradient, tangent plane, estimate, its error, then the predicted error for half the move. p-fit-descent takes a gradient, a step, the per-step factor, the step-size limit and the steps to reach 0.01.

Level 3: p-two-level-points solves for stationary points, $D$, a saddle, a pit and its height. p-capital-limit finds the free peak, classifies it, then the Lagrange point on a capital limit, $\lambda$ and the estimate for more capital. p-min-variance-pair expands $\sigma_p^2$, finds $w^*$, $\sigma_p$, $\lambda = 2\sigma_p^2$, then the variance at a budget of 1.02.

Level 4: p-weighted-rectangle finds the slice $\int_0^1 xy^2\,dx$, the constant $c = \tfrac34$, the inner integral over $0 \le y \le 2x$, then $P(Y \le 2X) = 0.4$. p-corner-sprinkler sets up the strip limit $\sqrt{9 - x^2}$, switches to polar ($9r - r^3$), integrates to 20.25 and $\tfrac{81\pi}{8} \approx 31.81$ litres, then the radius holding half the water, $a = \sqrt{9 - 9/\sqrt2} \approx 1.62$. p-drone-landing finds $\int e^{-x^2/8}\,dx = \sqrt{8\pi}$, squares it to $8\pi$, takes $c = \tfrac{1}{8\pi}$, then in polar $P(R \le 2) = 1 - e^{-1/2} \approx 0.3935$ and the 90% radius $\sqrt{8\ln 10} \approx 4.29$.

Level 5: p-three-strategies solves the budget-only Lagrange system ($\lambda = \tfrac43$, $z = -\tfrac16$), judges that the best allowed point is on the boundary, solves the edge $z = 0$ with two multipliers ($x = \tfrac34$), then compares edges and corners (2.125). p-dome-tent takes the stretch $x = 2u$ ($|J| = 2$), the roof in $u, v$, the volume $2\pi$, $\iiint z\,dV = \tfrac{4\pi}{3}$ and the mean air height $\tfrac23$ m. p-triangle-field takes the stretch onto a triangle ($|J| = 8$), the total yield $\tfrac{32}{15}$, the average $\tfrac{8}{15}$, the largest value on the closed field $\tfrac{64}{27}$ (slanted edge), then the share 0.225.

In sets 4 and 5 every part uses a value from an earlier part, except p-corner-sprinkler part 2 and p-triangle-field part 4, which start a new step on the same setting; the last part of each combines them. Each later part restates the value it uses. `wrong` lists carry the slip of the part before where one exists: the both-variables $f_x$ carried into $f_{xy}$; $V_X = -80{,}000$ carried into the rate; slopes of $x^2 + y^2$ carried into the plane and its estimate; the gradient without its 2 carried into the step; $D$ slips carried into $D(0, 0)$; $\lambda = -4$ into the estimate; the no-correlation quadratic into $w^*$; $\lambda = \sigma_p^2$ into the last part.

Sets 4 and 5 carry the slip of the part before as `carried` entries too: $c = \tfrac43$ into the inner integral and the chance; the inner integral 18 (no $r$) into the litres; $\sqrt\pi$ into $8\pi$ and $c$; $\lambda = \tfrac53$ and $\lambda = 2$ into $z$; $\tfrac{4}{15}$ (no $|J|$) into the average. Expression answers use LaTeX only (`\sqrt{...}`, `\pi`), never plain-text function names. Every numeric part with a non-integer key states its form. Tolerances accept the value the feedback prints and, where a part asks for an estimate, the exact value too ($-0.0303$ in p-stretched-bowl part 3, 10.78, 0.0029, 51.875).

## Checks

| check | problems-1 | problems-2 | problems-3 | problems-4 | problems-5 |
|---|---|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures | 0 failures | 0 failures (718 checks in all) |
| validator | 0 errors, 0 warnings on the file | same | same | same | same |
| playthrough `--local-cdn` | green (14 parts) | green (15 parts) | green (15 parts) | green (14 parts) | green (15 parts) |
| playthrough `--mobile --local-cdn` | green; 440 px part shots read, no fault | same | same | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 | 0 and 0 | 0 and 0 |

## Fresh-check

At the gate all three sets have 0 hits. At triage settings (`--min-run 8 --min-share 0`): problems-1 has one, "at what rate is # changing in pounds per day" (review-1 item 8, share 0.07), stock phrasing on a different setting (a currency-converted holding against a bond book). problems-2 has one, "how steep is the steepest climb from P" (l5 screens[3], share 0.08), the lesson's own term on a new function and point. problems-3 had six: four are the classification option list and form sentences, and two are the "asset A has volatility # and asset B #" opening shared with l12 and homework-3 (shares 0.09 and 0.11), with new volatilities and correlation (30%, 20%, 0.25). The l12 sentence "you put a fraction of your money in A" was reworded.

Sets 4 and 5: 0 hits at the gate. At triage settings problems-4 has one, "give your answer to # decimal places using the" (limits-thm problems-4, share 0.06), and problems-5 has 18, all the form sentence "give an exact fraction or a decimal to # places" shared with other courses' problem sets (shares 0.05 to 0.08). These are the brief's required form wording, not reused settings. No setting or number of sets 1 to 3, the level 4 and 5 lessons, review-4, review-5, homework-4 or homework-5 is reused: the nearest are the quarter disc (review-4 has $xy$ on radius 2; here a depth on radius 3) and the stretch onto an ellipse (l17 has $x = 2u$, $y = 3v$ on the unit disc; here a tent roof).

## Commits

The numbers script and this report cover all five sets; sets 1 to 3 were committed with level 3, and the extension for sets 4 and 5 with level 5. Each level was committed after their set passed the validator, the playthroughs, the voice scan and the script's checks for that level.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems multivar):": point sets in `answers` (level 3) and the raw LaTeX `accept` forms in the after-grading line (levels 4 and 5).
