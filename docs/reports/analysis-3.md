# Report: analysis level 3 (Series)

Course `analysis` (topic 1.10, strand pure), level 3, from `## Level 3` of `docs/briefs/analysis.md`. Ids, names, objectives and the skill `an-series` are as in course.json.

## Files written (app/content/courses/analysis/)
| file | screens / items | quiz | canvases |
|---|---|---|---|
| l11-partial-sums.json | 12 | 4 | plane with a table widget bound to its dots, plane with an ε-band and a frames control, table, bars, console |
| l12-convergence-tests.json | 12 | 4 | plane with two rows of partial sums and a frames control, plane of ratios, plane `riemann` under y = 1/x², flawed-line table, console, bars |
| l13-absolute-conditional.json | 11 | 4 | plane zigzag with a frames control, place, table, plane, console |
| l14-rearranging.json | 12 | 4 | plane of rearranged sums with a frames control, plane with a table bound to its dots, console |
| review-3.json | 9 items, difficulty 2 to 4 | | numeric, choice |
| homework-3.json | 9 items, difficulty 3 to 5 (four at 5) | | 3 order, 1 expression, 2 numeric, 1 flawed-line tap, 1 multi, 1 code (d5), 1 longform (d5) |

The longform rubric is 2+2+2+1+2+1 = 10, with a full model answer. The generators are gen_l11.py to gen_l14.py, gen_review3.py, gen_homework3.py and common.py in the scratchpad folder analysis-3.

Lesson shapes:
- **l11:** table hook, expression, explore, generalise, order, choice, two ladders, order, trap, code, transfer.
- **l12:** explore (says this level proves what `taylor` used), choice ×2, order, choice ×2, order, ladder table, rectangles problem, flawed-line trap, code, transfer.
- **l13:** explore, place (four facts with their reasons), order, ladder numeric, generalise, choice, order, classify table, trap, code, transfer.
- **l14:** explore, choice, ladder table, generalise, choice ×3, order, trap, Dirichlet problem, code, transfer.

Edge cases:
- **l11:** finitely many terms changed (quiz).
- **l12:** L = 1 (quiz), and p > 1.
- **l13:** ∑(−1)^n, in the classify table and the quiz.
- **l14:** a rearrangement that diverges to +∞ (quiz).

## Validator
0 errors. Warnings on these files: l13 screens[1] and screens[7], "problem screen without a canvas before the ladder ends".

## Playthrough (--local-cdn pkgs --mobile; --why while developing)
- l11: ok, 16 checks, quiz 4/4.
- l12: ok, 16 checks, quiz 4/4.
- l13: ok, 15 checks, quiz 4/4.
- l14: ok, 16 checks, quiz 4/4.
- review-3: recorded 9 of 9.
- homework-3: 9 of 9 right, 44 of 44 marks.

Every code solution passes in Pyodide, and every starter (a body of `...`) fails its tests.

Layout faults fixed:
- **l12 hook:** the vline label collided with the y = 1 label, so vline labels are now empty.
- **l12 rectangles:** the curve label is moved out of the tall rectangle.
- **l12 Merton bars:** crowded 0.000 value labels are removed.
- **l13 place:** a long KaTeX chip overflowed at 390 px and is shortened. Checked with a scratch scroll-and-capture script, peek.mjs.
- **l14 hook:** the ln 2 label touched the axis title, so y now starts at 0.5.
- **l14 wording:** "≈" replaces "=" where a decimal is rounded.

## Numbers (each by two routes: exact Fraction or float sum, and a closed form or second method)

**l11**
- S_1 to S_4 are 1/2, 2/3, 3/4, 4/5, matching 1 − 1/(n+1). S_10 = 10/11 ≈ 0.9091.
- The ε-band gives N = 4, 10, 20, 25 for ε = 0.25, 0.1, 0.05, 0.04, and N = 100 at ε = 0.01.
- S_1024 ≥ 6 by grouping. The true value is 7.509176, by sum and by ln 1024 + γ + 1/2048.
- first_exceeding: 4, 11, 31, 83 and 12367 for t = 2, 3, 4, 5, 10. The first four also hold with Fractions. Extra tests: t = 1 gives 2, 1.5 gives 3, 0 gives 1.
- Dividend model: the price is £100, by summing 3,000 terms and by 5/(0.08 − 0.03).
- The first ten years are worth £37.75, by summation and by 100(1 − (1.03/1.08)^10), with (1.03/1.08)^10 = 0.6225.
- The wrong answers are £50, £57.32 and £46.30, each worked out directly.
- Quiz: 15.25; a tail of 1/5; a_n = 1/(n(n−1)) with sum 2.

**l12**
- The hook series ∑ 1/(2^n + n) tends to 0.697277.
- ∑ n/2^n = 2, by S − S/2 = 1 and by sum. S_10 = 509/256.
- The ratio-test example uses r = 3/4 with N = 3.
- The ratios of n!/n^n are 0.385543 at n = 10 and 0.369711 at n = 100, by two formulas. The limit is 1/e = 0.367879 and the sum is 1.879854.
- sum_with_bounds(10) = (1.549768, 1.640677, 1.649768), by float and Fraction. Both bounds trap π²/6 for n < 200.
- Merton weights at λT = 2: the tail after n = 10 is 8.3082e-6, both as 1 − ∑ and as a direct sum. So the price error is at most £0.00083, and w_10 = 3.82e-5.
- Quiz: ∑ n^(−1.1) lies between 10 and 11, and ∑ 1/(n² + n) = 1.

**l13**
- S_10 = 0.645635 and ln 2 = 0.693147, so the error is 0.047512. Fraction against a 60-digit Decimal and the float sum agree. The bound is 1/11 = 0.0909.
- ∑ (−1)^(n+1)/n² = π²/12 = 0.822467.
- terms_needed with Fractions: 1/1000 gives 1000, 1/10 gives 10, 3/1000 gives 333, 1/2 gives 2.
- actual_needed: 0.1, 0.05, 0.01, 0.002, 0.001, 0.0005 give 5, 10, 50, 250, 500, 1000. Exact and float agree, and the errors decrease strictly up to n = 3000.
- At n = 500 the error is 0.000999000002; at n = 499 it is 0.001000999998. The Pyodide test passes.
- Trap: S_40 = 2.001576.
- Transfer: the net is £692.65 and the amount traded is £7,485.47, by sum and by H_n ≈ ln n + γ. A 1% cost is £74.85 after 1,000 trades and £143.93 after 10^6.
- Quiz: 1/36 against a true error of 0.016144, and n = 31.

**l14**
- Two-up-one-down totals: 0.8333 after 3 terms, 0.9801 after 12, 1.0152 after 30, 1.0273 after 60, 1.0372 after 300 and 1.0395 after 3,000.
- The limit is (3/2) ln 2 = 1.039721, by the L + L/2 argument and by 9,000 terms. From the third term on, the totals stay below 1.2 (maximum 1.1762).
- Greedy, T = 3/2: the twelve terms and totals match the brief exactly, in Fractions. After 2,000 terms the total is 1.4995174.
- Greedy, T = 0: the eight terms match the brief.
- The positive terms of ∑ (−1)^(n+1)/n² sum to π²/8 = 1.2337.

**review-3**
- ∑ 2/(n(n+2)) = 3/2, and ∑ n²/3^n = 3/2.
- The Leibniz series needs n = 50; at n = 49 the bound is 1/99 = 0.0101.
- Greedy towards T = 1: the second term is 1/3, because the rule compares with ≤.
- ∑ (−1)^(n+1)/2^n = 1/3.
- The midpoint estimate is 1.644973 against π²/6, off by 3.9e-5.
- Grouping needs 2^18 = 262,144 terms to reach 10.

**homework-3**
- ∑_{n≥1} 3^n/n! = e³ − 1 = 19.085537.
- S_n of ∑ 2/(k(k+2)) is 3/2 − 1/(n+1) − 1/(n+2), checked at n = 1 and 2 and in Fractions.
- The tail bound needs m = 3334.
- Greedy towards T = −1: the first five terms are −1/2, −1/4, −1/6, −1/8, 1. After 2,000 terms the total is −0.9958228, by Fraction and float.
- Longform: S_20 = 0.668771, the bound is 1/21 = 0.047619 and the true error is 0.024376.

Main-session spot check (a third route, CPython): ∑ 1/(2^n + n) = 0.697277, S_10 of ∑ n/2^n = 509/256, the l13 error 0.047512, the n = 499 and 500 errors, e³ − 1 = 19.085537 and S_1024 = 7.509176 all agree.

## Proof steps and their widgets
| proof | steps graded by |
|---|---|
| Terms of a convergent series tend to 0 (l11) | order (2 distractors); choice for "both S_n and S_(n−1) tend to S" |
| Term test on n/(n+1) | choice |
| Harmonic series by grouping | numeric (≥ 6), then order |
| Brackets in 1 − 1 + 1 − … (trap) | choice |
| Comparison test (l12) | choice (why increasing), choice (why bounded), order with `same`, choice (contrapositive for divergence) |
| Ratio test | choice (why r and N exist), order; homework: flawed-line tap (the sup of the ratios is 1) |
| Integral test | choice on the Riemann picture |
| Comparing below a divergent series (trap) | flawed-line tap |
| Alternating series test (l13) | place (four facts with reasons, two decoys), order with `same`, numeric bound; whole proof in the homework longform |
| Absolute implies convergent | choice (triangle inequality), order (Cauchy proof); homework order (comparison with a_n + abs(a_n)) |
| Greedy rearrangement (l14) | choice ×3 (both halves diverge, every crossing happens, the overshoot shrinks), then order |
| Both halves of a conditional series diverge | homework order, difficulty 5 |

## Proposed course.json changes
None.

## Conventions
- S_n notation as in levels 1 and 2, with n ≥ N.
- Code uses exact Fractions with compare "equal" where exact; otherwise isclose with abs 1e-9.
- No random seeds are used.
- Money is in £.
- The proofs rely only on level 2 results, each named: monotone convergence, the limit laws, Cauchy implies convergent, convergent implies bounded.

## Engine limits
Five bullets in `docs/BACKLOG-INBOX.md` under "Raised later (analysis level 3):":
- The validator rejects a table cell's `wrong[]` ids as byKey keys.
- A place chip with long KaTeX does not wrap at 390 px.
- `riemann` has no `colour`.
- vline and hline labels collide near the top of the plot.
- playthrough --mobile screenshots show only the viewport.

The main session saved this report from the agent's returned text, because the harness refuses report-file writes from subagents.
