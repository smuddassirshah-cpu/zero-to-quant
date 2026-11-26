# Claim ledger: vectors L1 to L3 (concept audit, blind, round 1)

Scope: `app/content/courses/vectors/` l1 to l12, review-1 to review-3, homework-1 to homework-3, problems-1 to problems-3, fluency-l3, fluency-l5, fluency-l7, fluency-l10, at commit 397dd192. One row per definition, result, method step, convention, always/never/every/only claim, code-behaviour claim, and the reasoning in each explain, why, hint and feedback line (lines on one screen that state the same step share a row). Verdicts: correct, wrong, imprecise, misleading, unverified.

Paths are JSON paths inside the named file; `s3` abbreviates `screens[3]`, `q1` `quiz[1]`, `i4` `items[4]`, `p2` `parts[2]`, `o` `widget.options`, `w` `widget.wrong`, `fb` `feedback`, `ex` `explain`, `h` `hints`, `fam` `families`. `sim: <name>` points at a check in `docs/reports/vectors-L1-3-concepts.py`; `sweep` at `docs/reports/vectors-L1-3-concepts-sweep.mjs` (the page's Pyodide 0.27.7, NumPy 2.0.2). Sources: Strang, *Introduction to Linear Algebra* (5th ed.), cited as Strang with section; Axler, *Linear Algebra Done Right* (3rd ed.), cited as Axler; Anton, *Elementary Linear Algebra* (11th ed.), cited as Anton; Higham, *Accuracy and Stability of Numerical Algorithms* (2nd ed.); Golub and Van Loan, *Matrix Computations* (4th ed.); Hull, *Options, Futures and Other Derivatives* (ch. 4, 19); Grinold and Kahn, *Active Portfolio Management* (ch. 2, 3). `F<n>` is finding n in `docs/reviews/audit-vectors-1-3.md`.

## Level 1

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l1-mixing | s0 prose, fb, ex | a u + b v stretches each arrow and joins tip to tail; 1u + 2v = (4, 5) | correct | Strang 1.1 (linear combinations); arithmetic |
| l1-mixing | s0 fb.r0c1 | swapped weights a = 2, b = 1 land on (5, 4) | correct | 2(2,1) + (1,2) = (5,4) |
| l1-mixing | s1 widget, ex, fb.P/Q/S | every multiple a u lies on one line through the origin; P = 3u, Q = -2u, S = 0.5u | correct | Strang 1.1; sim L1:span |
| l1-mixing | s1 fb.positive-only, fb.R, fb.T | a negative a turns u round; R, T off the line (second coordinate half the first) | correct | definition of scalar multiple |
| l1-mixing | s2 prose | definition: linear combination, weight; coordinates combine place by place | correct | Strang 1.1; Axler 2.A |
| l1-mixing | s2 o, h, ex | 3u - v = (5, 1); slips (7,5), (1,-1), (5,-1) as described | correct | arithmetic for each slip |
| l1-mixing | s3 h, fb, ex | matching coordinates gives 2a + b = 7, a + 2b = 8; a = 2, b = 3 | correct | sim L1:weights |
| l1-mixing | s4 prose, o, ex | T = (1,-1) is outside the angle between u and v; a negative weight reaches it: u - v | correct | arithmetic; (−1, 1) and (3, 3) for the wrong options |
| l1-mixing | s5 o, h, fb, ex | w = 2u, so every mix is (a + 2b)u; T off the line: no pair; infinitely many pairs only for points on the line | correct | Strang 1.1; sim L1:span |
| l1-mixing | s6 prose, fb | two arrows reach every point of the plane unless one is a multiple of the other; then parallel; definition of span | correct | Strang 1.3 (independence in the plane); Axler 2.A; sim L1:span (zero vector included as a multiple) |
| l1-mixing | s6 o, ex | (1,2),(2,1) and (1,0),(0,-3) span; (1,2),(-2,-4) and (3,6),(1,2) do not; a negative multiple counts | correct | sim L1:span |
| l1-mixing | s7 lines, ex | a = (2x - y)/3, b = (2y - x)/3; every (x, y) gives exactly one pair | correct | sim L1:weights; det = 3 |
| l1-mixing | s8 prose, h, fb, ex | factor exposures combine linearly; a = 0.6, b = 0.4; adding the equations gives a + b = 1 | correct | sim L1:weights; Grinold and Kahn ch. 3 (exposures are linear in holdings) |
| l1-mixing | summary | ideas, formula, trap | correct | restates rows above |
| l1-mixing | q0 | 2u - 3v = (-4, 11); slips (-4,5), (-1,5), (8,5) | correct | arithmetic |
| l1-mixing | q1 | (1,-2),(-3,6) parallel; (1,1),(1,-1) at right angles so not parallel; swapped coordinates are not a multiple | correct | sim L1:span |
| l1-mixing | q2, q3 | a = 2, b = -1; mixes of (1,2), (-2,-4) lie on y = 2x, only (3,6) reachable | correct | arithmetic; sim L1:span |
| l2-lining-up | s0 widget, ex | score 3 v1 + v2 negative exactly when the angle exceeds 90 degrees; counterexamples (2,-1), (1,0), (-0.5,3) | correct | sim L1:sign; Strang 1.2 |
| l2-lining-up | s0 ex | pointing along u gives the biggest score for its length; (-1, 3) is at right angles | correct | Cauchy-Schwarz with equality case, Axler 6.15; sim L1:cs |
| l2-lining-up | s1 prose | definition: dot product u1 v1 + u2 v2 | correct | Strang 1.2; Axler 6.2 |
| l2-lining-up | s1 w, fb, ex | -1; slips 11, 13, 12, 1; "a little more than a right angle apart" | correct | arithmetic; angle 93.4 degrees |
| l2-lining-up | s2 ex | zero dot product between non-zero arrows means perpendicular | correct | Strang 1.2; Axler 6.11 (orthogonal; the zero vector is excluded by "non-zero") |
| l2-lining-up | s3, q2, review-1 i4 | set the dot product to 0 and solve: k = 2, 2, 4; slips sign and flip | correct | arithmetic |
| l2-lining-up | s4 widget, fb, ex | sign follows the angle to u, not the quadrant; key q, r, t | correct | sim L1:sign |
| l2-lining-up | s5 o, fb, ex | the dot product is one number, not an arrow; 2; slips (6,-4), 10, (5,3) | correct | definition |
| l2-lining-up | s6 prose | n-coordinate dot product; positive within 90, zero at 90, negative beyond | correct | Strang 1.2; sim L1:sign (for non-zero arrows, as q1 states) |
| l2-lining-up | s6 w, ex | (1,2,3).(4,-5,6) = 12; slips 32, 11 | correct | arithmetic |
| l2-lining-up | s7 lines, ex | proof that u.(v + w) = u.v + u.w from the definition; "why the exposure of a book plus a hedge is the sum" | correct | Axler 6.7 (additivity); sim L1:dist |
| l2-lining-up | s8 prose, w, fb, ex | factor exposure w.beta = 1.8; slips 9.8, 1, 2.5; 1% factor rise makes about £18,000 | correct | sim L1:expo; 1.8m x 1% |
| l2-lining-up | summary | ideas, formula note (zero between two non-zero arrows means perpendicular), trap | correct | rows above |
| l2-lining-up | q0, q1, q3 | 4 (slips 16, 11); negative dot product means more than 90 degrees for non-zero arrows; -0.3 net short | correct | sim L1:sign, L1:expo |
| l3-lengths-angles | s0 widget, fb, ex | length by Pythagoras: 5; v.v is the squared length | correct | Strang 1.2 |
| l3-lengths-angles | s1 o, ex | all arrows with v.v = 25 are 5 long, heads on a circle; definition of length as sqrt(v.v) | correct | Axler 6.8 (norm) |
| l3-lengths-angles | s2 prose, fb, ex | dividing by the length gives a unit vector in the same direction: (0.6, -0.8) | correct | Strang 1.2; (needs a non-zero arrow, which the example is) |
| l3-lengths-angles | s3 o, h, ex | the ratio u.v / (the two lengths multiplied) is cos of the angle; sin, tan and radians ruled out by test values | correct | Strang 1.2 (cosine formula); sim L1:angle |
| l3-lengths-angles | s4 w, fb, ex | 45 degrees; slips 0.7071, 5, 0.7854 | correct | sim L1:angle |
| l3-lengths-angles | s4 prose, s8 lines[3], summary.formula | cos formula stated with no condition | imprecise | needs non-zero u and v, and gives the angle in [0, 180]; neither is said. Axler 6.B; sim L1:angle. F8 |
| l3-lengths-angles | s5 widget, h, fb, ex | foot of the perpendicular is (4, 2) = 2v; u - 2v perpendicular to v; multiple u.v / v.v | correct | Strang 4.2; sim L1:proj |
| l3-lengths-angles | s5 prose | "which the counting course wrote as beta m" | correct | counting l13-portfolio-vector uses beta m with (r - beta m).m = 0 |
| l3-lengths-angles | s6 prose, w, fb, ex | projection of u onto v is k v, k = u.v / v.v = 1.2; length 6; slips 30, 6, 0.8333 | correct | Strang 4.2; Axler 6.55; sim L1:proj |
| l3-lengths-angles | s7 o, fb | (3,0) + (0,4) is 5 long; lengths add only when the arrows point the same way | correct | sim L1:tri |
| l3-lengths-angles | s7 ex, summary.trap, q3 ex | triangle inequality "with equality only when the arrows point the same way" | imprecise | equality also when one arrow is zero; Axler 6.18 (equality iff one is a non-negative multiple of the other); sim L1:tri. F9 |
| l3-lengths-angles | s8 lines | proof of the cosine formula from the cosine rule on the triangle u, v, u - v | correct | Anton 3.2 (theorem 3.2.2); sim L1:angle |
| l3-lengths-angles | s8 ex | since cos is at most 1, u.v is at most the product of the lengths | correct | Cauchy-Schwarz, Axler 6.15; sim L1:cs |
| l3-lengths-angles | s9 prose, h, ex | correlation of A and B is the cosine of the angle between the demeaned vectors; 0.495; "the same number a spreadsheet's correlation function gives" | correct | Pearson r = a.b / (the two lengths multiplied) for centred a, b; sim L1:corr |
| l3-lengths-angles | s9 w, fb | slips raw 0.6197, dot 7, beta 0.7 | correct | sim L1:corr |
| l3-lengths-angles | s10 prose, h, ex | beta is the projection coefficient of b onto a: a.b / a.a = 0.7; it is the slope of the regression line of B on A | correct | OLS slope = Cov/Var; sim L1:corr (np.polyfit) |
| l3-lengths-angles | s10 w, fb | slips corr 0.495, 7, other-way 0.35 (A's beta to B), length 2.2136 | correct | sim L1:corr |
| l3-lengths-angles | summary.ideas | length, unit vector, cosine and correlation, projection and beta | correct | rows above |
| l3-lengths-angles | q0, q1, q2 | 13; (0,-1); 135 degrees; slips as named | correct | arithmetic; sim L1:angle |
| l3-lengths-angles | q3 o | v = 2u so the lengths add; a direct route is never longer than the detour | correct | sim L1:tri |
| l4-portfolio-return | s0 w, h, fb, ex | return on the whole is total gain over total money: 4.8%; slips average 2.67%, sum 8%, no sign 6.4% | correct | sim L1:port |
| l4-portfolio-return | s1 widget, ex | A's weight 0.5 gives 5.5%; return rises with the weight in the best asset | correct | 0.09k + 0.01 = 0.055 |
| l4-portfolio-return | s2 prose | definition: R_p = w.r, weights dotted with returns | correct | Grinold and Kahn ch. 2; sim L1:port (simple returns, start-of-period weights) |
| l4-portfolio-return | s2, s3, s4, s6 w/o, fb, ex | 1.1%, 1.15%, 3.2%, 3.8%; slips as named; weights must add to 1; a short has a negative weight and loses on a rise | correct | sim L1:port |
| l4-portfolio-return | s5 prose, w, fb, ex | borrowing is cash at -0.5, costing its rate: 4.3%; rescaling to 0.6/0.4 gives 3.2% and is wrong because return is on own money | correct | sim L1:port (pounds: 430 on 10,000) |
| l4-portfolio-return | s7 prose, o, ex | n-asset formula with weights summing to 1; identical returns give that return whatever the weights | correct | 0.03 x sum of weights |
| l4-portfolio-return | s8 lines, ex | derivation: asset i gets V w_i, gains V w_i r_i, total over V is w.r; "return is gain over starting value" | correct | this fixes the convention as simple returns; sim L1:port shows the identity fails for log returns |
| l4-portfolio-return | s9 prose, w, fb, ex | P&L is holdings dotted with price changes: 1,915; slips 1,275 and 1.6 | correct | sim L1:pnl |
| l4-portfolio-return | summary | ideas, formula note, trap | correct | rows above |
| l4-portfolio-return | q0 to q3 | -1%; C's weight -0.2 (short); 10.5% with leverage; P&L £40 | correct | sim L1:port, L1:pnl |
| review-1 | i0 to i4 | (7,3); a = 3, b = 2; parallel pair; dot 7 (slips 23, 2), "positive so less than 90 degrees apart"; k = 4 | correct | arithmetic; sim L1:span, L1:sign |
| review-1 | i5 | angle 126.87 degrees; slips 53.13, -0.6 | correct | sim L1:angle |
| review-1 | i6 | projection of (4,2) onto (1,3) is (1,3); slips (10,30), (2,1) is v onto u, (0.32,0.95) is the unit vector; leftover (3,-1) perpendicular | correct | sim L1:proj |
| review-1 | i7, i9 | R_p = 0.7%; P&L 160 | correct | sim L1:pnl; arithmetic |
| review-1 | i8 ex | positions perpendicular to the betas, so a market move leaves the book flat, to first order | correct | sim L1:expo; linear factor model |
| fluency-l3 | fam0 | length from Pythagorean triples; slips squared length, sum of sizes | correct | grade-all (2 seeds); wrong values never equal the key |
| fluency-l3 | fam1 | unit vector; slips divide by v.v, sign dropped (only when a coordinate is negative) | correct | grade-all |
| fluency-l3 | fam2 | cosine; `where` excludes 0 and plus or minus 1; slips dot only, divide by u.u "gives a projection coefficient" (only when the lengths differ) | correct | dot/uu is the coefficient of v on u; grade-all |
| fluency-l3 | fam3 | projection multiple; `where` keeps the three slips distinct from the key | correct | uv/vv against vv/uv and uv/uu; grade-all |
| homework-1 | i0, i1, i2 | a = 2, b = 3; u.v = 5t - 2 (slips 5t - 1, t^2 - t + 6); t = 0.4 | correct | arithmetic |
| homework-1 | i3 | correlation -0.6455 as the cosine of the demeaned series; slips raw -0.0845, -5, -0.5, sign | correct | sim L1:corr |
| homework-1 | i4 | beta -0.5; slips -0.8333 (X's beta to Y), -1.5811, corr; "Y tends to move half as far as X, the other way" | correct | sim L1:corr |
| homework-1 | i5 | short-funded leverage: w = (1.5, -0.5), 7%; slips 11%, 3.5% (on gross £40,000), 2% | correct | sim L1:port |
| homework-1 | i6 | P&L 142; slips -218, -1.09 | correct | sim L1:pnl |
| homework-1 | i7 lines, ex | proof of k = u.v / v.v from (u - k v).v = 0, dividing by v.v which is positive because v is not zero; with v the demeaned market k is the beta | correct | Axler 6.14 (orthogonal decomposition); sim L1:proj |
| homework-1 | i8 model, rubric | weights 0.75, 0.25; return 4.4% by exposures and by funds, equal because the dot product spreads over sums; two parallel funds reach only y = 0.2x, on-line targets in infinitely many ways | correct | sim L1:weights, L1:dist, L1:span |
| problems-1 | i0 p0 to p3 | (2,3); dot 42 = 6 x 7; angle 58 degrees, unchanged by stretching; straight line 2.18 m shorter; no-cross slip "squared lengths add like that only at right angles" | correct | sim L1:p1, L1:angle |
| problems-1 | i1 p0 to p3 | active weights add to 0; active return a.r = -0.55% = w.r - b.r; length 0.1871; angle 130 degrees; slips as named | correct | Grinold and Kahn ch. 4 (active return); sim L1:p1 |
| problems-1 | i2 p0 to p4 | unit vector (0.6, 0.8); dotting with a unit vector gives the component: -4; crosswind 7 by Pythagoras; 24 km/h; 60 minutes | correct | Strang 1.2; sim L1:p1 |
| problems-1 | i3 p0 to p3 | scenario returns by dot product; hedge h = 0.11 makes w' perpendicular to c; -1.46%; average scenario -0.73% by linearity; "the hedge roughly halves it" | correct | sim L1:p1 |

## Level 2

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l5-acting-on-a-vector | s0 widget, ex | x1 = 2, x2 = 1 reach T; the pair is a recipe | correct | arithmetic |
| l5-acting-on-a-vector | s1 prose | definition: matrix, Ax = x1 a1 + x2 a2 (combination of the columns) | correct | Strang 1.3, 2.1 (column picture) |
| l5-acting-on-a-vector | s1, s4, s5 widgets, fb | (3,-1); (-3,1) with slips rows (-1,3) and plus (1,3); (2,3,-3) | correct | sim L2:views |
| l5-acting-on-a-vector | s2 o, ex | A e1 is column 1; e2 picks out column 2 | correct | sim L2:views |
| l5-acting-on-a-vector | s3 prose, w, fb, ex | each entry of Ax is a row dotted with x; 24; slips 11, 16, 22 | correct | Strang 2.1 (row picture); sim L2:views |
| l5-acting-on-a-vector | s5 ex | an m by n matrix takes n entries to m entries | correct | sim L2:views |
| l5-acting-on-a-vector | s6 widget, fb, ex | the amounts scale the columns, not the rows; P = (4,2), Q = (2,3) from rows, R = (2,2) from the diagonal | correct | arithmetic |
| l5-acting-on-a-vector | s7 lines, fb, ex | derivation that the column view and the row view agree | correct | Strang 2.1; sim L2:views |
| l5-acting-on-a-vector | s8 prose, fb, ex | factor model: returns are loadings times factor moves; 1.4, 1.65, 2.45; column j is each asset's move on a 1% day of factor j; utility gains when rates fall | correct | Grinold and Kahn ch. 3; sim L2:views |
| l5-acting-on-a-vector | summary, q0 to q3 | (8,1); 3 entries; 1.5%; 11 with slips 10, 5, 7 | correct | sim L2:views |
| l6-moving-the-plane | s0 widget, fb, ex | A sends e1 to column 1 and e2 to column 2; every unit square becomes the same parallelogram | correct | Strang 8.1 (linear transformations); linearity |
| l6-moving-the-plane | s1 prose, o, ex | R turns anticlockwise; the quarter turn is [[0,-1],[1,0]]; [[0,1],[-1,0]] is clockwise; -I is a half turn | correct | Anton 4.9 (rotation matrix, positive angle anticlockwise); sim L2:maps |
| l6-moving-the-plane | s2 prose, o, ex | "moving the plane by a matrix is a linear transformation"; e1 to (cos, sin), e2 to (-sin, cos); R(theta) | correct | Anton 4.9; sim L2:maps |
| l6-moving-the-plane | s3 prose, fb, ex | shear [[1,k],[0,1]]: each point slides by k times its height; x-axis fixed; height never changes | correct | Anton 4.9; arithmetic |
| l6-moving-the-plane | s4 o, ex | diagonal matrix: each axis only scaled; a minus sign flips | correct | columns read off |
| l6-moving-the-plane | s5 o, ex | [[0,1],[1,0]] reflects in y = x; a quarter turn has a minus sign; reflection in the x-axis keeps e1 | correct | sim L2:maps |
| l6-moving-the-plane | s6 o, ex | N = [[1,2],[2,4]] flattens the plane onto y = 2x; area 0; no matrix can undo it | correct | sim L2:maps; rank 1 |
| l6-moving-the-plane | s7 widget, fb, ex | images are columns: M e2 = (2,1); a shear with k = 2 | correct | columns read off |
| l6-moving-the-plane | s8 prose, o, ex | A(x, y) = x A e1 + y A e2, so a matrix is fixed by two arrows; reflection in the x-axis | correct | linearity, Axler 3.5 |
| l6-moving-the-plane | s9 prose, fb, ex | m = (s + b)/2, d = s - b as one matrix [[0.5,0.5],[1,-1]]; 3% and -1% give 1% and 4% | correct | columns from unit inputs; arithmetic |
| l6-moving-the-plane | summary, q0 to q3 | half turn -I; shear sends (1,1) to (3,1); columns (0,2), (-1,0); spread -2% | correct | sim L2:maps |
| l7-one-after-another | s0 widget, fb, ex | shear then quarter turn: e1 to (0,1), e2 to (-1,1); (1,1) and (-1,0) explained | correct | sim L2:order |
| l7-one-after-another | s1 o, h, ex | the two orders give the same shape only when k = 0 or theta is 0 or 180 degrees; a half turn only reverses arrows | correct | RS = SR iff k sin(theta) = 0; sim L2:order on every slider setting |
| l7-one-after-another | s2 prose, fb, ex | doing S then R is the product RS; the matrix next to x acts first; column j of RS is R times column j of S | correct | Strang 2.4; sim L2:order |
| l7-one-after-another | s3 prose, w, fb, ex | entry (i, j) is row i of A dotted with column j of B; 7; slips 6, 13 (BA), 9 | correct | Strang 2.4; sim L2:order |
| l7-one-after-another | s4 o, ex | (m x n)(n x p) gives m x p; inner sizes must match | correct | sim L2:order |
| l7-one-after-another | s5 o, fb, ex | reflect then turn is RF = reflection in y = x; FR sends P to (-1,-2); the first move sits on the right | correct | sim L2:order |
| l7-one-after-another | s6 prose, o, ex | R(theta)R(theta) = R(2 theta) gives the double-angle formulas; check at 30 degrees | correct | sim L2:maps |
| l7-one-after-another | s7 prose, lines, ex | why row times column: column j of AB is A b_j | correct | Strang 2.4 |
| l7-one-after-another | s8 prose, w, fb, ex | chained sensitivities L(Mz) = (LM)z; -1.7 as the sum over two paths; slips -0.1 (ML), -0.9, -1.3, 1.7 | correct | sim L2:order |
| l7-one-after-another | summary | AB applies B first; in general AB is not BA; formula note "the columns of the first must match the rows of the second" | correct | Strang 2.4 (counts of columns and rows) |
| l7-one-after-another | q0 to q3 | AB swaps the columns of A, BA its rows; TS; 2x3 times 2x3 undefined; sin 60 = 0.866 | correct | arithmetic; sim L2:maps |
| l8-identity-transpose | s0 widget, ex | R^4 = I | correct | sim L2:maps |
| l8-identity-transpose | s1 prose, o, ex | definition of the identity; AI = A and IA = A when the sizes fit; one identity per size; a 2x3 A needs the 3x3 identity on its right | correct | Strang 2.4 |
| l8-identity-transpose | s2 widget, fb, ex | definition of the transpose (D^T)_ij = d_ji; a 2x3 becomes 3x2 | correct | Strang 2.7 |
| l8-identity-transpose | s3 prose, o, ex | a vector is a column; u^T v is the dot product, a 1x1 matrix; u v^T is 2x2 | correct | Strang 2.7; sim L2:transpose |
| l8-identity-transpose | s4, s5 widgets, o, fb, ex | B^T A^T = [[7,3],[2,1]] = (AB)^T; A^T B^T = [[1,3],[2,7]]; BA = [[1,2],[3,7]] | correct | sim L2:transpose |
| l8-identity-transpose | s6 lines, fb, ex | entry proof of (AB)^T = B^T A^T | correct | Strang 2.7; Anton 1.4 (theorem 1.4.8) |
| l8-identity-transpose | s7 prose, w, fb, ex | covariance matrix entry (i, j) is Cov(R_i, R_j); symmetric because Cov(R_2, R_1) = Cov(R_1, R_2); 0.3 would be the correlation; every covariance matrix is symmetric | correct | definition of covariance; sim L2:var |
| l8-identity-transpose | s8 prose, w, h, fb, ex | portfolio variance w^T Sigma w = 0.01888 with the covariance counted twice; volatility 13.74%, below the 16% weighted average; slips 0.016, 0.01744, 0.16 | correct | Markowitz (1952); sim L2:var (2,000,000 draws separate the key from both slips) |
| l8-identity-transpose | summary | ideas, formula, trap | correct | rows above |
| l8-identity-transpose | q0, q1 | A^T of a 2x3 is 3x2; (ABC)^T = C^T B^T A^T | correct | sim L2:transpose |
| l8-identity-transpose | q2 | volatility 13.74%; below the average "because the two assets are not perfectly correlated" | correct | sim L2:var (long-only mixes, rho below 1) |
| l8-identity-transpose | q3 o, ex | A^T A is always symmetric; A^2, A + I, A^T need not be; "covariance matrices are built this way from centred data" | correct | Strang 2.7; sim L2:transpose (sample covariance is X^T X over n - 1 for centred X) |
| review-2 | i0 to i2 | (0,2); clockwise quarter turn is R(-90); entry (2,1) = 2 with slips 11, -3, -2 | correct | arithmetic; sim L2:maps |
| review-2 | i3, i4, i5 | airline -3.5% (slips -3.8, 1.3, 3.3); shear x = 3.5; DM = [[0,2],[1,0]], MD is the other order | correct | sim L2:views; arithmetic |
| review-2 | i6, i7 | A^T A of a 3x2 is 2x2; (A^T B)^T = B^T A | correct | sim L2:transpose |
| review-2 | i8 | volatility 15.37%; slips 16.77%, 18.06%, variance; "well below the 22.5% average" | correct | sim L2:var |
| fluency-l5 | fam0, fam1 | Ax by columns; slips combined rows, diagonal only, amounts swapped, added columns; `where` keeps each slip off the key | correct | grade-all; b != c and x2 != 0 make the rows slip differ |
| fluency-l7 | fam0, fam1 | one entry and one column of AB; slips BA entry, transposed entry (only off the diagonal), BA column, combined rows | correct | grade-all; `where` clauses checked |
| homework-2 | i0, i1, i2 | factor returns -1.9, 0, -2.35; matrix from images; S(k)S(k) = S(2k) | correct | sim L2:views; arithmetic |
| homework-2 | i3 lines, ex | angle-addition formula from R(alpha)R(beta) = R(alpha + beta) | correct | sim L2:maps |
| homework-2 | i4 | volatility 12.27%; slips 12.73%, 13.17%, 14.4%; "volatilities do not average; variances combine through Sigma" | correct | sim L2:var |
| homework-2 | i5, i6, i7 | R(15)^6 = R(90), entry -1 (slips 1, -0.2588, -1.5529); N flattens onto y = -2x; u^T v = -1 and (u v^T)_23 = 8 | correct | sim L2:maps, L2:transpose |
| homework-2 | i8 model, rubric | Sigma for two assets; w^T Sigma w expands to the two-asset variance formula, cross terms equal because Sigma is symmetric; 0.01888; with rho = -0.3 variance 0.01312, volatility 11.45% | correct | sim L2:var |
| problems-2 | i0 p0 to p3 | slant S = [[1,0.25],[0,1]]; S(2,8) = (4,8); slant then widen is DS = [[1.5,0.375],[0,1]]; x = 6, the other order gives 5 | correct | sim L2:p2 |
| problems-2 | i1 p0 to p3 | R with cos 0.8, sin 0.6; R^T R = I because the columns are unit and perpendicular; m = R^T g = (10,-5); step angle 126.9 = 90 + theta | correct | Strang 4.4 (orthogonal matrices); sim L2:p2 |
| problems-2 | i2 p0 to p4 | exposures B^T w = (1.105, 0.2); x = 0.605; hedged (0.5, 0.04875); variance e^T F e = 0.00376, unhedged 0.01910; cut 80.3%; slips as named | correct | Grinold and Kahn ch. 3 (factor risk b^T F b); sim L2:p2 |
| problems-2 | i3 p0 to p4 | Qx = (23.6, 6.4, 4.4); cost 54.88; c = Q^T p because p^T(Qx) = (Q^T p)^T x; (0.85, 1.74); 77.30; Qp and p^T Q^T undefined | correct | sim L2:p2, L2:transpose |

## Level 3

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l9-one-matrix-equation | s0 widget, fb.swapped, fb.P, ex | both equations hold only at the crossing (2, 3); at (3, 2), 2x - y = 4 | correct | sim L3:sing (one solution) |
| l9-one-matrix-equation | s0 fb.one-line | "That point sits on one line only" for the region x 3.7 to 5.3, y -0.3 to 1.3 | wrong | of the nine snap points in the region six are on neither line, among them the untouched start (4, 0.5): x + y = 4.5, 2x - y = 7.5. F11 |
| l9-one-matrix-equation | s1 prose, o, ex | column picture: x a1 + y a2 = b with a1 = (1,2), a2 = (1,-1); same numbers as the crossing | correct | Strang 2.1 |
| l9-one-matrix-equation | s2 prose, widget, fb, ex | definition: coefficient matrix A, x, b; each row is one equation, each column one unknown | correct | Strang 2.1; Anton 1.1 |
| l9-one-matrix-equation | s3, s4 widgets, o, fb, ex | A and b for 3x + 2y = 12, x - 4y = 2; move unknowns to the left; a missing unknown is a 0; the zero is why the line is upright | correct | arithmetic |
| l9-one-matrix-equation | s5 o, fb, ex | a matrix with each equation down a column encodes a different system: row 1 gives 4x + 2y = 9 | correct | arithmetic |
| l9-one-matrix-equation | s6 prose, o, ex | m equations in n unknowns give an m by n matrix; constants stay in b | correct | Anton 1.1 |
| l9-one-matrix-equation | s7 lines, ex | Ax = rows times x = x a1 + y a2; solving asks which combination of the columns gives b | correct | Strang 2.1 |
| l9-one-matrix-equation | s8 prose, o, fb, ex | greeks add across positions, so each target is one equation; rows are targets, columns are options | correct | Hull ch. 19 (portfolio greeks are sums of position greeks) |
| l9-one-matrix-equation | summary, q0 to q3 | -1; A for x = 3y + 1, y = 2; second entry 17 (slips 11, 7); row (-3, 1) with 0 | correct | arithmetic |
| l10-undoing | s0 widget, fb, ex | undoing diag(2,3) is diag(1/2,1/3); u = (3,2); u on T goes to (12,18) | correct | arithmetic |
| l10-undoing | s1 o, fb, ex | the quarter turn is undone by [[0,1],[-1,0]]; rotation by theta is undone by rotation by -theta; a stretch by k by 1/k; half turn and reflection ruled out | correct | sim L2:maps |
| l10-undoing | s2 prose, fb, ex | if B undoes A then BA = I; example with (3,-1) | correct | arithmetic |
| l10-undoing | s3 prose | definition: the inverse undoes A, with A^-1 A = I | correct | Strang 2.5 (for square A the same matrix also gives A A^-1 = I, which the course never states: see homework-3 i2) |
| l10-undoing | s3 w, fb, ex | swap the diagonal and negate the rest gives (ad - bc) I: 2I; definition of the determinant ad - bc | correct | Anton 1.4 (theorem 1.4.5); sim L3:inv |
| l10-undoing | s4, s6 widgets, o, fb, ex | recipes: [[1,-0.5],[-2,1.5]]; (1/5)[[4,-3],[-1,2]]; slips no-det (gives 5I), swap-bc, wrong-moves, plus (11) | correct | sim L3:inv |
| l10-undoing | s5 prose, o, h, fb, ex | (RS)^-1 = S^-1 R^-1; R^-1 S^-1 sends (-1,2) to (2,0.5); in general (AB)^-1 = B^-1 A^-1 | correct | Strang 2.5; sim L3:inv |
| l10-undoing | s7 prose, summary.formula, summary.ideas[1] | the 2 by 2 inverse rule, stated with no condition on ad - bc | imprecise | holds only when ad - bc is not 0; the condition arrives in l11 s7. Anton 1.4.5. F7 |
| l10-undoing | s7 o, ex | inverse of diag(2,4); slips negate, no-swap, no-det | correct | arithmetic |
| l10-undoing | s8 lines, fb, ex | Ax = b gives x = A^-1 b by multiplying on the left, associativity, A^-1 A = I, Ix = x | correct | Strang 2.5 |
| l10-undoing | s9, s10 widgets, h, fb, ex | det 0.10, A^-1 = [[3,-2.5],[-2,5]]; 225 and 350; new target (0,60) gives -150 and 300; one inverse answers every new target | correct | sim L3:inv |
| l10-undoing | summary.ideas[0], [2], trap; q0, q1, q2 | inverse of [[5,2],[2,1]]; -0.2 (slips -2, 0.2, -0.1429); first entry -1 (slips -29, 13, 1) | correct | sim L3:inv; arithmetic |
| l10-undoing | q3 prose, o, ex | "first rotates by 30 degrees and then stretches everything by 3"; key: shrink then rotate back; option same-order marked wrong: "the stretch came last, so it comes off first" | wrong | a stretch of everything by 3 is 3I, which commutes with every matrix, so "rotate by -30, then shrink by 1/3" also undoes it; Strang 2.4 (cI commutes); sim L3:q3 (failing). F1 |
| l10-undoing | q3 o negate, repeat | -3 flips the picture as well; rotating by 30 again turns further | correct | sim L3:q3 |
| l11-no-inverse | s0 widget, fb, ex | at k = 2 the columns (2,2), (1,1) point the same way; the square flattens; past k = 2 the shape is mirror-imaged | correct | sim L3:det |
| l11-no-inverse | s1 o, ex | the area of the image of the unit square is the absolute value of ad - bc; the determinant is the factor by which A scales every area | correct | Strang 5.1, 5.3; sim L3:det (square and triangle) |
| l11-no-inverse | s2 prose, o, h, ex | a negative determinant means the plane is flipped: A e2 sits clockwise from A e1; sign is orientation, size is area | correct | Strang 5.1; sim L3:det (signed shoelace area) |
| l11-no-inverse | s3 w, fb, ex | area 5 for [[1,3],[2,1]], mirror image; slips -5, 7, 1 | correct | sim L3:det |
| l11-no-inverse | s4, s5 o, fb, ex | det 0: parallel lines give no solution; the same line gives infinitely many; b decides, never exactly one | correct | Strang 2.2 (singular cases); sim L3:sing |
| l11-no-inverse | s6 o, fb, ex | no zero entries does not guarantee an inverse; what matters is dependence between the columns; [[2,1],[1,2]] has det 3 | correct | sim L3:det |
| l11-no-inverse | s7 prose | det = 0 collapses the plane onto a line, different points land on one spot, so nothing can undo it; singular; det A = 0 iff A^-1 does not exist | correct | Strang 2.5, 5.1; sim L3:det (for the zero matrix the collapse is onto a point, a harmless special case) |
| l11-no-inverse | s7 w, fb, ex; q2; review-3 i5 | k = 4, 2, 4; slips plus and zero; columns become multiples | correct | sim L3:det |
| l11-no-inverse | s8 prose, lines, ex | columns "lie on one line", written as column 2 = t x column 1; then ad - bc = tac - tac = 0 | imprecise | a zero first column with a non-zero second lies on one line with no such t (the determinant is still 0); sim L3:det. F10 |
| l11-no-inverse | s9 o, fb, ex | proportional greeks: every mix has vega = 0.4 x delta; (200,150) unreachable; (200,80) reachable in many ways; 400 of P gives vega 80 | correct | sim L3:sing |
| l11-no-inverse | s9 h[2] | "The target needs 150 = 0.4 x 200 = 80" | imprecise | reads as the false chain 150 = 80; the meaning is that the line gives vega 80 where the target asks 150. F12 |
| l11-no-inverse | s10 prose | minimum-variance weights are usually proportional to Sigma^-1 1 | correct | Merton (1972); Lagrange condition 2 Sigma w = lambda 1; sim L3:minvar |
| l11-no-inverse | s10 o, h, fb, ex | perfectly correlated classes: det Sigma = 0, every fully invested mix has variance 0.0625, so no unique minimum; a singular covariance matrix means some mix has zero variance (long one, short the other) | correct | sim L3:minvar; Sigma w = 0 for a null vector w |
| l11-no-inverse | summary; q0, q1, q3 | area 11; [[2,5],[4,10]] singular, the swap matrix undoes itself; x + y = 2, 3x + 3y = 6 has infinitely many | correct | sim L3:det, L3:sing |
| l12-numpy-matrices | s0 prose, tests, ex | `@` is the matrix product; `A @ x` gives the greeks | correct | NumPy reference (matmul); sweep: solution passes, starter fails test 1 |
| l12-numpy-matrices | s0 fb.test-1 | names `A @ x` for the first failing test | correct | sweep: `A * x`, `x @ A`, `A.T @ x`, `A.sum(axis=1)` all fail test 1 first |
| l12-numpy-matrices | s1 canvas, w, fb, ex | `np.linalg.det` prints 5.000000000000001; elimination in floating point leaves an error near 1e-15; never test with `==`, use `np.allclose` | correct | sweep P1 (page) and sim L3:numpy (desktop); LAPACK getrf, Higham ch. 9 |
| l12-numpy-matrices | s2 prose, ex | `np.linalg.inv`, `np.eye`; `np.allclose` allows 1e-8 + 1e-5 times the size of y per entry | correct | NumPy reference (allclose: atol 1e-8, rtol 1e-5 on the second argument); sim L3:numpy |
| l12-numpy-matrices | s2 fb.test-2 | the candidate without the division gives 5I, so False | correct | describes its test; sweep: `return True` fails test 2 first |
| l12-numpy-matrices | s2 fb.test-3 | "With == the rounding error in np.linalg.inv can break the test" | wrong | under the page's Pyodide (and desktop NumPy 2.5) inv([[2,3],[1,4]]) @ A is exactly I: three `==` codings pass tests 1 to 5 and first fail test 6, which has no line; sweep, sim L3:numpy (failing). F2 |
| l12-numpy-matrices | s2 tests | the hidden tests fix `is_inverse` | misleading | sweep: a diagonal-only check `np.allclose(np.diag(B @ A), 1)` and a round-to-integer check pass all six tests. F4 |
| l12-numpy-matrices | s3 prose, tests, fb, ex | `np.linalg.solve(A, b)` solves without forming the inverse; needs a square A with a non-zero determinant | correct | NumPy reference (gesv); sweep: `A @ b`, `solve(A.T, b)`, `b / A` and `solve(b, A)` fail test 1 first |
| l12-numpy-matrices | s4 canvas, o, fb, ex | `*` is elementwise with broadcasting across each row: [[112.5, 87.5],[45, 105]]; x^T A = (182.5, 161.25) | correct | sweep P2, P3; sim L3:numpy |
| l12-numpy-matrices | s5 canvas | Hilbert 10 by 10: residuals 4.4e-16 for solve and 5.2e-05 for inv | correct | sweep P4 reproduces both figures on the page's NumPy; desktop NumPy 2.5 gives 4.4e-16 and 9.7e-05 (version dependent, the lesson says "one run") |
| l12-numpy-matrices | s5 o[0] | solve is more accurate because "it eliminates on b directly, so rounding has fewer steps to grow" | imprecise | the gap is conditioning, not step count: inv costs 3 times the arithmetic but the residual is 1e11 times larger, and on well-conditioned matrices both are at rounding level; Higham 14.1; sim L3:numpy. F5 |
| l12-numpy-matrices | s5 o inv-exact, same, inv-fast; ex | no computed inverse is exact; in exact arithmetic the two agree; inv does about three times the arithmetic for one right-hand side; use inv only when the matrix itself is needed | correct | 2n^3 against (2/3)n^3 flops, Golub and Van Loan 3.2; Higham 14.1 |
| l12-numpy-matrices | s6 prose, o | `A.T`, `np.linalg.det`, solve then check; `x @ A` is x^T A; `solve(A, x)` answers the reverse question | correct | NumPy reference; sim L3:numpy |
| l12-numpy-matrices | s7 lines, ex | build, rank, solve, multiply back, compare; rank 2 means one solution; a small residual does not prove x accurate when A is nearly singular: check `np.linalg.cond` | correct | Higham 7.1 (forward error bounded by condition number times backward error); sim L3:numpy (Hilbert) |
| l12-numpy-matrices | s8 tests, fb.test-1, fb.test-3, ex | 3 by 3 hedge (200, 300, 100); pure vega (-250, 500, 0); large answers (2500, -1000, -1500) are right | correct | sim L3:numpy; sweep: `A @ b`, `solve(A.T, b)` fail test 1; a clip to plus or minus 1000 first fails test 3 |
| l12-numpy-matrices | s9 prose | T = P + Q makes the columns dependent; desktop NumPy raises `LinAlgError`; this browser's NumPy returns nan; `matrix_rank` counts the independent columns: 2 | correct | sweep P7, P12 (page: nan, rank 2); sim L3:numpy (desktop raises; NumPy 2.5) |
| l12-numpy-matrices | s9 fb.test-1, test-3, test-4 | no check fails test 1; the proportional options are rank 1; a solvable hedge must still return | correct | sweep: starter and a `ValueError` coding fail test 1 (for the second the line's "no error was raised" is loose), always-raise fails test 4; test 3 line describes its test |
| l12-numpy-matrices | s9 fb.test-6, ex | the desk matrix scaled by 1e-4 has determinant about 2e-16 and still solves; a cut-off on the determinant misfires because the determinant scales with the entries; a healthy four-asset daily covariance matrix has a determinant near 1e-16 | correct | det(sA) = s^n det A; sweep P16 and three cut-off codings fail test 6 first; sim L3:scale (1,000-day samples, volatility near 1%: median within a factor 10 of 1e-16) |
| l12-numpy-matrices | s9 tests, fb.correct | "Singular hedges now fail loudly everywhere" for any program that passes | misleading | sweep: `if np.linalg.det(A) == 0`, a nan check after solve, and a residual check pass all six tests, yet miss a singular matrix whose computed determinant is not 0, such as [[0.04, 0.06], [0.06, 0.09]] (page: solve returns 7.2e16, -4.8e16). F3 |
| l12-numpy-matrices | summary | `@` against `*`; solve beats inv on arithmetic and rounding; `np.allclose`; test the rank, not the determinant's size | correct | rows above |
| l12-numpy-matrices | q0, q1 | `A @ x` = [3, 7]; `(A @ B).T` = `B.T @ A.T` | correct | sim L3:numpy, L2:transpose |
| l12-numpy-matrices | q2 o, ex | det 0, infinitely many solutions ((1,0) and (-1,1)); desktop raises, the browser returns nan | correct | sweep P5; sim L3:numpy, L3:sing |
| l12-numpy-matrices | q3 o, ex | rounding leaves errors near 1e-16; `==` compares entry by entry and is too strict; tolerance about 1e-5 for entries near 1 | correct | sim L3:numpy |
| review-3 | i0 to i3 | A and b; row (0,2,0); inverse [[1,-3],[-1,4]]; x = 3, y = 1 | correct | sim L3:inv; arithmetic |
| review-3 | i4 o, ex | (ABC)^-1 = C^-1 B^-1 A^-1; matrices cannot be divided | correct | Strang 2.5; sim L3:inv |
| review-3 | i6, i7, i8 | coincident lines; `A @ x` = [2,7], `A * x`, `x @ A`, `A.T @ x` values; 50 and 300 | correct | sim L3:sing, L3:numpy, L3:inv |
| review-3 | i9 o, ex | for one solve of a large system write `np.linalg.solve`; inv costs about three times the arithmetic and more rounding; `*` and `/` are elementwise | correct | Higham 14.1; Golub and Van Loan 3.2 |
| fluency-l10 | fam0 | determinant; slips ad + bc, ad alone | correct | grade-all; entries non-zero so both slips differ from the key |
| fluency-l10 | fam1 wrong not-divided, added-bc | column of the inverse; slips no division (only when det is not 1), divided by ad + bc | correct | grade-all; `where` keeps them apart |
| fluency-l10 | fam1 wrong not-swapped line | "the top-left of the inverse is d over the determinant", also shown when column 2 is asked | imprecise | for column 2 the slipped entry is the bottom-right, a over the determinant; the line points at an entry outside the asked column. F13 |
| fluency-l10 | fam2 | solve by x = A^-1 b; slips A b, (y, x) | correct | grade-all; integer d from the chosen determinant |
| homework-3 | i0, i1, i3 | 3 by 3 A and b; inverse of [[6,4],[2,3]]; k = 4 from k^2 - 16 | correct | arithmetic; sim L3:det |
| homework-3 | i2 lines, ex | proof that B^-1 A^-1 is (AB)^-1 by (AB)(B^-1 A^-1) = I, using B B^-1 = I and A A^-1 = I | imprecise | the course defines the inverse by A^-1 A = I only ("undoes A") and never says the same matrix works on the right; the proof checks the other-sided product. True for square matrices (Strang 2.5 note 2; Axler 3.69). F6 |
| homework-3 | i4 | a change in the target needs A^-1 times the change: (-25, 50) | correct | linearity; sim L3:inv |
| homework-3 | i5 | det Sigma = 0.0027 = the two variances multiplied by (1 - rho^2); falls to 0 as rho goes to plus or minus 1 | correct | sim L3:det |
| homework-3 | i6 o, ex | det -3: has an inverse, triples areas, flips; the inverse has determinant -1/3 | correct | sim L3:det (det of a product) |
| homework-3 | i7 prose | fully invested minimum-variance weights are Sigma^-1 1 over 1^T Sigma^-1 1; solve, then scale; raise on rank; daily covariances and their determinants are tiny | correct | Merton (1972); sim L3:minvar (no fully invested rival beats it on 200 random matrices) |
| homework-3 | i7 tests, fb.test-1, test-6, test-7, test-8, ex | expected weights; uncorrelated weights go as 1 over variance; correlation 1 is singular; det 0.0036 - 0.0036; the healthy 4 by 4 has determinant about 8e-16 and rank 4 | correct | sim L3:minvar; sweep: no-normalise fails test 1, no check fails 6, `det == 0` and a nan check fail 7, three cut-offs fail 8 |
| homework-3 | i8 model, rubric | singular greeks matrix; reachable targets are the line vega = 0.4 x delta, each reached by infinitely many mixes; (200,80) by (500,0) and (200,200); (200,100) by none; with Q, det 0.08, p = 437.5, q = 100 | correct | sim L3:sing, L3:inv |
| homework-3 | i9 prose, solution, ex | a bond's price is its cash flows times the discount factors, so C d = p; with one bond per year the prices fix d exactly when C has full rank; the browser returns nan for an exactly singular matrix and rounding can hide a singular one | correct | Hull 4.5 (bootstrapping); sim L3:bonds; sweep P13, P14 |
| homework-3 | i9 fb.test-3 to test-12 | each line names its test's case: no one-year bond, out-of-order bonds, one bond, two one-year bonds, three three-year bonds (determinant tiny but not 0), a late target, two prices for three years, an inverse in the source | correct | sweep: sequential bootstrap fails 3, sorting bonds without prices fails 5, no checks fails 8, `det == 0` and a nan check fail 9, no maturity check fails 10, `inv` fails 12 |
| homework-3 | i9 fb.test-1, test-2 | test 1: "a bond's row holds its coupon in every year"; test 2: pad the targets' rows | imprecise | tests 1 and 2 call the same function, so target code that raises (unpadded rows) fails test 1 and gets the bond-row line; sweep (matmul shape error on test 1). F14 |
| problems-3 | i0 p0 to p3 | A by nutrient; det 0.1; A^-1 = [[7,-1],[-4,2]]; (30, 40); slips transposed (-90, 70), no-divide, times-det | correct | sim L3:p3 |
| problems-3 | i1 p0 to p4 | k = 2 singular; `matrix_rank` prints 1, rank 0 only for the zero matrix; (60,18) unreachable since blue is a quarter of red; (60,15) with p = 3 needs q = 3; k = 5 gives (4, 2) | correct | sim L3:p3, L3:sing; sweep P12 |
| problems-3 | i2 p0 to p4 | C = DM; a matrix scales areas by the size of its determinant, 0.8 = det D x det M; C^-1; (120, 80); undo the gain first: (DM)^-1 = M^-1 D^-1, and the two orders differ here | correct | sim L3:p3, L3:det, L3:inv |
| problems-3 | i3 p0 to p4 | C_k = B_k A; det = 2 - k = det B_k x det A; singular at k = 2; C_1^-1 = [[2,-3],[-5,8]]; (19,12) came from (2,1); slips as named | correct | sim L3:p3 |
