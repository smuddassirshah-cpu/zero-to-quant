# Answer check, topic 3.2, measure-prob level 2

Independent recomputation of every graded widget in `courses/measure-prob/` `l5-lebesgue-integral`, `l6-monotone-convergence`, `l7-dominated-convergence`, `l8-modes-of-convergence`, `review-2` and `homework-2`. Neither the author's scripts nor `docs/reports/measure-prob-2.md` were used. Scripts are in the scratchpad folder `ac-mp2`.

**Method.**
- Closed forms and direct sums for every integral and limit: dyadic means of `U^2` (all six means and gaps), capped St Petersburg means (direct sum to 200 terms), geometric series, tail integrals with SciPy `quad`, the dividend partial sums (all 100 plotted values regenerated and compared, 78 and 63 years by search), tranche integrals, and `sup_n n U^n` by brute force near `U = 1`.
- Black-Scholes numbers: `d1 = 0.35`, `d2 = 0.15`, `Phi(d1) = 0.636831`, `Phi(d2) = 0.559618`, `phi(d2) = 0.394479`, digital delta 0.018762, price 0.5323. The call delta, the digital delta, the likelihood-ratio and pathwise estimates were rerun with NumPy `default_rng(7)` and match the quoted values to every digit. The binomial tree prices at 10, 20, 50, 100, 200, 500 and 1000 steps were recomputed from the CRR recursion and match the plotted series; Black-Scholes is 10.450584.
- Typewriter and spike: every `steps` frame (the 15 typewriter blocks, the 20 spike frames, the six digital bumps) compared with the definitions; the chart of modes (12 cells) and the `h-modes` chart (12 cells) derived cell by cell.
- Code: each solution and each starter run in CPython with a copy of the `code.js` compare rules (`fraction` needs a `Fraction`, `isclose` honours `tol`, `raises` accepts subclasses, `prelude` first). Six code items, 62 hidden tests. Starters return `None`, so every starter fails every test and example. Alternatives were also run: plain `sum` without a `Fraction(0)` start, closed-form partial sums, `ddof=0` standard errors.
- Expression grading: the real `grade.js` `exprEqual` with Compute Engine 0.30.2 on 24 forms for `h-geom` (including `a(1-x^n)` with a letter before a bracket, `\left( \right)`, `\cdot`, `a(x^n-1)/(x-1)`, `\frac{a-ax^n}{1-x}`).
- Table byKey ids checked against `table.js` (zero-based `r{row}c{col}`, column 0 is the label). Numeric `wrong` bands checked against the answer band and each other. Choice and multi options checked for a second correct option. Key length against the longest distractor (limit 1.5). Order keys checked against the `same` rule in `order.js` (lines interchangeable among their places).
- Text scans: literal backslash-n, exclamation marks, em-dashes and en-dashes (none found), sentence length (rough count).

**Summary.** 82 widgets checked (81 graded plus one longform). All 82 keys are right. Errors: 2 (one distractor that is also a valid reason, one `wrong` text that names the wrong factor). Warnings: 13. Notes: 9. The worst finding is item 1: in `l7` screen 1 option d ("because $E[X_n] = 1$ for every $n$") is a valid proof that no integrable $Y$ exists, so a learner who picks it is marked wrong for a correct argument.

## Widgets checked

Key column: the keyed answer. Mine: my value. OK means the key, its tolerance, every `wrong` value and every stated number in the screen's prose, hints and explanation agree with my recomputation, and the numbers are not repeated from a lesson (reviews and homework). See the numbered list for the exceptions.

| File | Screen or item | Key | Mine | Verdict |
|---|---|---|---|---|
| l5 | s0 numeric | 0.1464 (abs 0.0005) | 0.146447; slips 0.5, 0.2929, 0.3333 match | OK |
| l5 | s1 numeric | 0.3333 (abs 0.002) | 1/3; means 0.1464, 0.2317, 0.2794, 0.3052, 0.3188, 0.3259; gaps 0.1869 to 0.0074; slip 0.3259 is E of phi_6 | OK |
| l5 | s2 choice | a | a only | OK |
| l5 | s3 numeric | 5.5 | 5.5; 25/3 = 8.33, 25, 7 (swap) match | OK |
| l5 | s4 choice | a | a only (Q has chance 0) | OK |
| l5 | s5 numeric | 0.3333 | 1 - 2/3 = 1/3; 0.5, 0.6667 match | OK |
| l5 | s6 numeric | 11 | m + 1 = 11 (direct sum 11) | OK |
| l5 | s7 choice | a | a only (mean infinite) | OK |
| l5 | s8 choice | a | a only | OK |
| l5 | s9 code | 11 tests | solution 11/11, examples 2/2, starter 0/11 | OK; Warning 4 (explanation) |
| l5 | s10 numeric | 1.3534 | 10 e^-2 = 1.353353; 0.1353, 2.7067, 10 match | OK |
| l5 | q-bet numeric | 13 | 13; 110/3 = 36.67, 110 | OK |
| l5 | q-tail numeric | 0.5 | 1/2; slip 1 is the exponent -2 integral | OK |
| l5 | q-heavy choice | a | a only; ln(1 + t) diverges | OK |
| l5 | q-null numeric | 3 | 3 | OK |
| l6 | s0 numeric | 2 (abs 0.01) | 2; caption 0.7869, 1.2642, 1.7293, 1.9865 | OK |
| l6 | s1 choice | a | a only | OK |
| l6 | s2 numeric | 5 | 5; 4, 0.2, 1.25 match; 10 bars match | OK |
| l6 | s3 order | m1 to m6, same m1/m2 | proof valid; other valid orders exist | Warning 6 |
| l6 | s4 choice | a | a only; Y_n increases to liminf | OK |
| l6 | s5 choice | a | a only | OK, key long (1.66), item 14 |
| l6 | s6 choice | a | a only; E[1/(nU)] infinite | OK, key long (1.75), item 14 |
| l6 | s7 code | 10 tests | solution 10/10, examples 2/2, starter 0/10; closed form also passes | OK |
| l6 | s8 table | 40, 78 | 40 and 77.82 so 78 (39.008 at 78, 38.960 at 77); 100 plotted values equal; r0c1, r1c1 right | OK |
| l6 | q-tail numeric | 2 | 2; slip 1 | OK |
| l6 | q-which choice | a | a only | OK |
| l6 | q-sum numeric | 0.5 | 1/2; 0.3333; 1.5 | OK |
| l6 | q-inf choice | a | a only | OK |
| l7 | s0 table | 0, 1 | X_20(0.3) = 0; E = 1; first n with 1/n < 0.3 is 4; 20 spike frames match | OK |
| l7 | s1 choice | a | a is right, and d is also a valid reason | Error 1 |
| l7 | s2 numeric | 0.1 | 1/10; 0.1111 (1/9), 0.9 | OK |
| l7 | s3 order | p1 to p5 | proof valid; p3 and p4 can swap | Warning 5; Note 20 |
| l7 | s4 table | 1, 0.6368 | E[Y] = 1; Phi(0.35) = 0.636831; digital figures 0.5596, 0.5323 right | OK; Note 24 |
| l7 | s5 numeric | 0 (tol 0) | 0 | Warning 15 (canvas and prose) |
| l7 | s6 numeric | 0.0188 (abs 5e-5) | 0.018762; slips 0.3945, 0.0197 (0.019724), 0 match | OK; Warning 15 |
| l7 | s7 choice | a | a only | OK, key long (1.73), item 14; Note 17 |
| l7 | s8 code | 8 tests | solution 8/8, examples 2/2, starter 0/8; seed 7 values 0.635956, 0.001822 reproduce | OK; Warning 8 |
| l7 | s9 numeric | 0.94 (abs 0.05) | 0.940 to 0.943; 213 pathwise | OK key; Error 2 (slip `big`) |
| l7 | q-hyp choice | a | a only | OK, key long (1.60), item 14 |
| l7 | q-digital choice | a | a only | OK (key 1.50, at the limit) |
| l7 | q-u19 numeric | 0.05 | 1/20; 0.0526, 0.95 | OK |
| l7 | q-quad choice | a | a only; E[X_n] = 1/n, E[sup] = 2 | OK |
| l8 | s0 numeric | 4 | n = 1, 2, 5, 10; 15 frames match | OK |
| l8 | s1 choice | a | a only | OK |
| l8 | s2 numeric | 0.0156 (abs 1e-4) | 1/64 = 0.015625; 0.01, 0.5, 1 match | OK |
| l8 | s3 table | 0.05, 20 | 1/20; 400/20 = 20 | OK |
| l8 | s4 numeric | 0.8413 | Phi(1) = 0.841345; 0.1587 | OK |
| l8 | s5 order | c1 to c5 | valid | OK; Note 19 |
| l8 | s6 table | 12 cells (no, yes, no / yes, yes, no / yes, no, no / yes, yes, yes) | same, derived cell by cell; 12 byKey texts right | OK |
| l8 | s7 multi | i1, i2, i3 | same; i4 to i7 each false | OK |
| l8 | s8 choice | a | a only; P(|Z| > 0.5) = 0.617075 | OK, key long (1.58), item 14 |
| l8 | s9 code | 13 tests | solution 13/13, examples 2/2, starter 0/13; hits 4 and 10 | OK |
| l8 | s10 numeric | 5 | 0.0200/0.0040 = 5; tree prices match; sqrt 5 = 2.24, 25, 0.2 | OK |
| l8 | q-const choice | a | a only | OK, key long (2.56), item 14 |
| l8 | q-zn numeric | 0.01 | 0.01; 0.1, 1 | OK |
| l8 | q-tree choice | a | a only | OK |
| l8 | q-cheb numeric | 0.16 | 0.04/0.25 = 0.16; 0.04, 0.08 | OK |
| review | r-simple numeric | 7 | 7; 20, 60 | OK |
| review | r-layer numeric | 0.2 | 1/5; 1, 0.04, 0.8 | OK |
| review | r-heavy numeric | 3 | 0.75/0.25 = 3; 0.75, 1.5 | OK |
| review | r-tail numeric | 4 | 4; 3, 0.25 | OK |
| review | r-div part 1 numeric | 60 | 3/0.05 = 60; 42.86, 150 | OK |
| review | r-div part 2 numeric | 63 | 62.60 so 63 (56.91 at 62, 57.06 at 63) | OK key; Warning 3 (explanation sign) |
| review | r-which choice | a | a only | Warning 9 (repeat), key long (2.08), item 14 |
| review | r-dom numeric | 3 | 2 * 3/2 = 3; 1.5, 2 | OK |
| review | r-delta choice | a | a only | Warning 10 (repeat), key long (2.65), item 14 |
| review | r-mode choice | a | a only; E[X_n^2] = 1 | Warning 11 (repeat), key 1.46 |
| review | r-cheb numeric | 0.25 | 0.0025/0.01 = 0.25; 0.0025, 0.025 | OK |
| homework | h-tranche part 1 numeric | 0.0439 | e^-3.125 = 0.043937; 0.2865 | OK |
| homework | h-tranche part 2 numeric | 1.9405 | 1.940543; 15, 2.292 | OK key; Note 16 |
| homework | h-sp numeric | 20.9073 | 19 + 10^6/2^19 = 20.907349 (direct sum agrees); 19, 21, 10^6 | OK |
| homework | h-fatou part 1 numeric | 0 | 0 | Warning 12 (repeat) |
| homework | h-fatou part 2 numeric | 1 | 1 | Warning 12 (repeat) |
| homework | h-fatou part 3 choice | a | a only | OK, key long (1.71), item 14; Warning 12 |
| homework | h-order | f1 to f5, same f2/f3 | valid; f2 can also follow f4 | Warning 7 |
| homework | h-geom expression | a(1-x^n)/(1-x) | 13 equivalent forms graded right, 4 wrong forms graded wrong | OK |
| homework | h-modes table | 12 cells (yes, yes, no / yes, yes, no / yes, no, no / yes, yes, yes) | same | OK; Note 21 |
| homework | h-nu part 1 numeric | 0.95 | 19/20; 1, 0.05 | OK; Note 22 |
| homework | h-nu part 2 numeric | 1 | 1 | OK |
| homework | h-nu part 3 choice | a | a only; sup is 3.487, 36.60, 367.7 at delta 0.1, 0.01, 0.001 against 1/(e delta) = 3.68, 36.8, 367.9 | OK, key long (2.41), item 14 |
| homework | h-code | 9 tests | solution 9/9, example 1/1, starter 0/9; digital 0.0186793, SE 8.8037e-5, call 0.631907, SE 0.0045772 | OK; Warnings 8 and 13 |
| homework | h-long longform | 7 rubric points, 10 marks | sum 10; model correct except the constant in part 3 | OK; Warning 15 |

## Mismatches

Errors

1. **Error. `l7-dominated-convergence.json` screens[1] (`Why can no integrable $Y$ dominate the spike?`), option `d` is also a correct answer.** "Because $E[X_n] = 1$ for every $n$" is a valid proof: if an integrable $Y$ dominated the spike, dominated convergence would give $E[X_n] \to E[0] = 0$, but every mean is 1. The author's own `byKey.d` says "That is true but it is the symptom." A learner who picks d gives a correct argument and is marked wrong. Fix: replace the text of `d` with a false statement, for example "Because the heights $n$ are unbounded, and an unbounded variable has no finite mean." with `why`: "You treated unboundedness as the obstacle. An unbounded variable can have a finite mean. The trouble is the size of $\sup_n X_n$ against its chance." Replace `byKey.d` with "Unbounded variables can still be integrable. Look at the largest value any $X_n$ takes at a given $U$."
2. **Error. `l7-dominated-convergence.json` screens[9], `wrong` `big` (94) and `byKey.big`.** The text says "You scaled by 1,000." The value 94 is 0.94 times 100: the gap 0.000083 over 0.000088 is 0.94, so a 1,000 scale would give 940. No slip of 1,000 gives 94. Fix: "You scaled by 100. The ratio of two small numbers is near 1." (or keep the text and change the value to 940, tol 5).

Warnings

3. **Warning. `review-2.json` items[4] `r-div` part 2, `explain`: "$n \ge \ln 0.05 / \ln(1.07/1.02) = 62.6$".** $\ln 0.05 = -2.9957$ and $\ln(1.07/1.02) = 0.04785$, so the quotient is $-62.6$, not $62.6$. The key 63 and the 62.6 are right. Fix: "$n \ge \ln 20 / \ln(1.07/1.02) = 62.6$" (the lesson's hint for the same step in `l6` writes $\ln 40 / \ln(1.08/1.03) = 77.82$, which is correct). The `generic` text "Solve $(1.02/1.07)^n \le 0.05$" is fine.
4. **Warning. `l5-lebesgue-integral.json` screens[9] `explain`: "The gap to $\tfrac13$ is 0.0539 at $n = 3$".** $\tfrac13 - 0.279370 = 0.053963$, which is 0.0540 to four places (the hint on screen 1 gives 0.054). The value 0.0074 at $n = 6$ is right. Fix: write 0.0540.
5. **Warning. `l7-dominated-convergence.json` screens[3] (order, Fatou proof): a valid alternative order is marked wrong.** Line `p3` (cancel to get the liminf bound) needs only `p2`. Line `p4` (Fatou for $Y - X_n$, with its own cancellation) needs only `p1` and `p2`. So `p1, p2, p4, p3, p5` is a valid proof. Fix: add `"same": [["p3", "p4"]]`.
6. **Warning. `l6-monotone-convergence.json` screens[3] (order, proof of monotone convergence): valid alternatives are marked wrong, and `m6` points at "line one".** `m1` (L exists and $L \le E[X]$) depends on none of `m2` to `m5`, so it may sit anywhere before `m6`, not only first or second. `m4` and `m5` also swap: `m5` proves $E[\varphi\mathbf 1_{E_n}] \to E[\varphi]$ from `m3` alone, and `m6` needs both. The `same` group covers only `m1`/`m2`. The words "With line one" in `m6` are wrong when the learner puts `m2` first, which `same` allows. Fix: move the content of `m1` into `m6` ("$L = \lim E[X_n]$ exists because the means rise and stay below $E[X]$, so $L \le E[X]$; ... $L \ge E[X]$. Hence $L = E[X]$") and drop `m1`; then the lines are `m2` to `m6` with `"same": [["m4", "m5"]]`, and the prose says "Two lines are flawed." (unchanged). Minimal alternative: keep `m1`, reword `m6` to "With the bound $L \le E[X]$", and add `"same": [["m4", "m5"]]`; the loose position of `m1` then stays a known gap.
7. **Warning. `homework-2.json` items[3] `h-order`: a valid alternative order is marked wrong.** `f2` (monotone convergence on $Y_n$) is independent of `f3` and `f4`; `f5` needs `f2` and `f4`. So `f1, f3, f4, f2, f5` is valid, and the `same` group `f2`/`f3` accepts only `f1, f3, f2, f4, f5`. Fix: merge `f3` and `f4` into one line ("For every $k \ge n$, $Y_n \le X_k$, so $E[Y_n] \le E[X_k]$. Taking the infimum over $k \ge n$: $E[Y_n] \le \inf_{k \ge n} E[X_k]$.") and keep `"same": [["f2", "f34"]]` with the prose "The line using monotone convergence and the line bounding $E[Y_n]$ by later means may swap." unchanged.
8. **Warning. The standard error is graded to 1e-6 relative but the prompt never says which one.** `homework-2.json` items[7] `h-code` (tests 2 and 4) and `l7-dominated-convergence.json` screens[8] (test 2) compare the standard error with `rel 1e-6`. The sample standard deviation `x.std(ddof=1)/sqrt(n)` passes; the population form `x.std()/sqrt(n)` gives 8.80369e-05 against 8.80373e-05 and fails (verified). In `l7` the `point` hint states `ddof=1`; `h-code` has no hints and says only "its standard error". Fix: add "(the sample standard deviation, `ddof=1`, divided by $\sqrt n$)" to the `h-code` question and to the `l7` s8 prompt, or loosen the two SE tests to `rel 1e-4`.
9. **Warning. `review-2.json` items[5] `r-which` repeats the lesson's spike and its answer.** $X_n = n\mathbf 1_{\{U < 1/n\}}$ with $E[X_n] = 1$ is the spike of `l7` s0 and `l6` quiz `q-which` option b, with the same key. DECISIONS "Fresh numbers in reviews and homework" bars this. Fix: use $X_n = 3n\mathbf 1_{\{U < 1/n\}}$ and $E[X_n] = 3$; in option b's `why` write "it is $3n$, then 0"; in option d's `why` write "the limit of the means would be 0, not 3". Keys unchanged ($\sup_n X_n \approx 3/U$, infinite mean).
10. **Warning. `review-2.json` items[7] `r-delta` repeats the lesson's digital and its delta 0.0188.** The same scenario, exact delta and 100,000 paths appear in `l7` s5 to s8; `byKey`/`why` d also quotes 0.0188. Fix: change the exact delta to a fresh digital: $S_0 = 100$, $K = 105$, $r = 3\%$, $\sigma = 25\%$, $T = 0.5$ has exact delta $e^{-rT}\varphi(d_2)/(S_0\sigma\sqrt T) = 0.02138$ ($d_2 = -0.2795$; recomputed twice). Write "The exact delta is 0.0214" in the prose and "a different seed would give 0.0214" in option d's `why`.
11. **Warning. `review-2.json` items[8] `r-mode` uses the lesson's variable.** $X_n = n\mathbf 1_{\{U < 1/n^2\}}$ is `l7` quiz `q-quad` (there the question is the mean; here the modes). Fix: use $X_n = 2n\mathbf 1_{\{U < 1/n^2\}}$: $P(X_n \ne 0) = 1/n^2$ and $E[X_n^2] = 4$ for every $n$. In option b's `why` write "$E[X_n^2] = 4n^2 \cdot \tfrac1{n^2} = 4$", in the `feedback.correct` "with $E[X_n^2] = 4$", and in the explanation "But $E[X_n^2] = 4$". Keys unchanged. (Do not use $\sqrt n\,\mathbf 1_{\{U < 1/n\}}$: it is `h-modes` column B.)
12. **Warning. `homework-2.json` items[2] `h-fatou` repeats the lesson's spike and both answers.** $X_n = n\mathbf 1_{\{U < 1/n\}}$ gives 0 and 1, as in `l7` s0. Fix: use $X_n = 3n\mathbf 1_{\{U < 1/n\}}$: part 1 stays 0 (change `wrong` `one` to 3), part 2 becomes 3 (its `accept` and `explain` become "$3n \cdot \tfrac1n = 3$"), part 3 reads "$0 < 3$".
13. **Warning. `homework-2.json` items[7] `h-code` reproduces the lesson's printed output.** Its first example and test are the digital with seed 7, $K = 100$, which gives 0.018679 and 0.000088, the numbers in the `l7` s9 console; the `correct` feedback says "near 0.0188". Fix: move the examples and tests to $S_0 = 100$, $K = 105$, $r = 0.03$, $\sigma = 0.25$, $T = 0.5$, $n = 100000$, seed 21. Recomputed: digital estimate 0.021320863378961503, SE 0.00010402382624449808, exact delta 0.021379762050349284 (0.57 SE away); call estimate 0.45659000268962846, SE 0.003819911396832423, exact delta $\Phi(d_1) = 0.45907764450186667$ (0.65 SE away). Change the test "SE greater than 0.0018" to "greater than 0.0035" (the pathwise call SE here is 0.00183), and the explanation to "0.0038 against 0.0018". Rerun all 9 tests before shipping.
14. **Warning. Choice keys visibly longer than their distractors** (key characters against the longest distractor, limit 1.5 as in `answers-3.2-measure-prob-1`). Worst first: `review-2` `r-delta` (135 against 51, 2.65); `l8` quiz `q-const` (115 against 45, 2.56); `homework-2` `h-nu` part 3 (111 against 46, 2.41); `review-2` `r-which` (125 against 60, 2.08); `homework-2` `h-fatou` part 3 (116 against 68, 1.71); `l6` s6 (84 against 48, 1.75); `l7` s7 (97 against 56, 1.73); `l6` s5 (88 against 53, 1.66); `l7` quiz `q-hyp` (64 against 40, 1.60); `l8` s8 (87 against 55, 1.58). Fix: shorten each key to its claim and keep the reason in `feedback.correct`/`explain`, or lengthen the distractors. Suggested keys: `r-delta` "The pathwise estimator is biased: a step has derivative 0 almost surely."; `q-const` "$X_n \to c$ in probability."; `h-nu` "No integrable $Y$ dominates: $\sup_n nU^n$ has an infinite mean."; `r-which` "Neither theorem applies: $X_n$ is not monotone and $\sup_n X_n$ is not integrable."; `h-fatou` "The inequality can be strict: $0 < 3$ (or $0 < 1$)."; `l6` s6 "$\infty$, because $E[X_n] = \tfrac1n\int_0^1 \tfrac{du}{u}$ diverges."; `l7` s7 "The constant 5 is integrable, so it dominates (bounded convergence)."; `l6` s5 "$E[X] = \infty$: the means rise without bound."; `q-hyp` "One $Y$ with $|X_n| \le Y$ and $E[Y] < \infty$."; `l8` s8 "No: $|X_n - Z| = 2|Z|$ never shrinks." Within the limit but watch: `l7` quiz `q-digital` (33 against 22, exactly 1.50), `l6` s4 (1.48), `r-mode` (1.46).
15. **Warning. The digital's difference quotient is written as $1/h$, but the quoted mean 0.0188 is the discounted one.** `l7` s5 prose ("The difference quotient over a bump $h$ is $\tfrac1h$") and `homework-2` `h-long` model, part 3 ("the quotient is $\tfrac1h$ ... its mean stays near $c = 0.0188$"). With the undiscounted payoff $\mathbf 1_{\{S_T > K\}}$ the constant is $\varphi(d_2)/(S_0\sigma\sqrt T) = 0.019724$; 0.018762 needs the factor $e^{-rT} = 0.951229$ ($0.019724 \times 0.951229 = 0.018762$). The canvas on s5 and s6 draws heights as 0.018762 divided by the width, so it is the discounted quotient. Also the bump areas on the canvas are the limit value for every $k$, but the true areas at the wider bumps are 0.0162, 0.0177, 0.0183, 0.0185, 0.0187 and 0.0187 for $k = 1$ to 6 (the caption says "area about 0.0188"). Fix: in `l7` s5 write "The discounted quotient over a bump $h$ is $e^{-rT}/h$ on the few paths ..." and in the caption "area tends to 0.0188"; in `h-long` part 3 write "the discounted quotient is $e^{-rT}/h$ ... its mean stays near $c = 0.0188$".

Notes

16. **Note. `homework-2.json` items[0] `h-tranche` part 2 `explain`: "$8(0.2865 - 0.0439) = 1.9405$".** With the four-place operands the product is 1.9408; the exact value is 1.94054. Fix: "$8(0.28650 - 0.04394) = 1.9405$".
17. **Note. `l7-dominated-convergence.json` screens[7] canvas.** The prose bound is 5 but the canvas draws a line labelled "Y = 1" (id `five`) over $U^n$. Fix: set the line to y = 5, label "Y = 5" (the axis then needs `y` up to 5.5) or relabel it "$U^n \le 1$, a tighter bound than 5".
18. **Note. `l8-modes-of-convergence.json` summary ideas[1].** "Almost surely and mean square each imply in probability (Chebyshev)" reads as though Chebyshev proves both; it proves only the mean-square arrow. Fix: "Almost surely implies in probability, and mean square does by Chebyshev; in probability implies in distribution."
19. **Note. `l8` s5 order, lines `c1` and `c2`.** `c2` could precede `c1`, since its own reason ("on the event the left side exceeds $\varepsilon^2$") uses the equivalence that `c1` states. The hint order agrees with the key. No change needed; add `"same": [["c1", "c2"]]` only if both are to be accepted.
20. **Note. `l7` s3 line `p1`.** The proof uses $E[X]$ and Fatou for $Y \pm X$ without saying $|X| \le Y$ almost surely, which follows from $|X_n| \le Y$ and $X_n \to X$ ($h$-long's model does say it). Fix: end `p1` with "so also $|X| \le Y$ almost surely".
21. **Note. `homework-2.json` items[5] `h-modes`: 5 of the 12 table cells have no `byKey` text** (`r0c1`, `r1c1`, `r2c1`, `r3c1`, `r3c2`: column A everywhere and B in distribution). A wrong entry there shows only the generic line. Add lines only if wanted (A: "$1/n \to 0$ in every mode").
22. **Note. `homework-2.json` items[6] `h-nu` part 1 reuses a lesson integral.** $\int_0^1 u^{19}\,du = \tfrac1{20}$ is the answer to `l7` quiz `q-u19`, and the `wrong` `five` value (0.05) equals that answer. Fix: use $n = 24$ (key $24/25 = 0.96$, `wrong` `five` 0.04, text "You gave $1 - 0.96$"; part 1 `accept` becomes "$24\int_0^1 u^{24}\,du = \tfrac{24}{25}$").
23. **Note. Sentences of exactly 20 words by a rough count** (formulas counted as one word) in `l6` s2 `correct`, `l7` s4 `explain`, `l7` s8 `correct`, `l7` s9 prose, `l8` s9 `explain`, `l8` s10 prose, `l8` summary ideas[0] and `h-geom` prose. The limit is under 20. Split each at its comma.
24. **Note. `l7` s4 prose quotes six-place normal values** ($\Phi(0.35) = 0.636831$, $\Phi(0.15) = 0.559618$) "from trees l10", which prints them to four places (0.6368, 0.5596). The six-place values are right; only the attribution is loose. Fix: "From trees l10, $\Phi(0.35) = 0.6368$ and $\Phi(0.15) = 0.5596$." The delta key and its tolerance (0.0005) need only four places.

## Checks with nothing found

- Every numeric `wrong` band lies outside its answer band and outside every other wrong band; no byKey names an id that does not exist; every numeric `wrong` has a byKey text. Table byKey ids are zero-based and match their rows and columns in all six tables (only `h-modes` has cells without text, item 21).
- No choice item has two correct options except `l7` s1 (item 1); every distractor in every choice and multi widget has a `why`; the one multi (`l8` s7) has exactly the three true implications.
- Order keys: `l8` s5 has no other valid order (item 19 aside); the `d1`, `d2` and `x1`, `x2` distractor lines are false as their `why` texts say; every `answer` is a valid proof.
- All six code items: each solution passes all its tests and examples; each starter fails every test and example (0 of 62). Stated counts in `how` (11, 10, 8, 13, 9) match. The plain `sum` without a `Fraction(0)` start, a closed-form partial sum and a `True`/`False` typewriter also pass.
- The `h-geom` expression key accepts the 13 equivalent forms tried (including the letter before a bracket) and rejects $a/(1-x)$, $a(1-x^n)/(x-1)$, $a(1-x^{n+1})/(1-x)$ and $a(1-x^{n-1})/(1-x)$. The `inf` slip is $a/(1-x)$.
- Theorem statements: monotone convergence (increasing, non-negative, infinite limit allowed, fails downwards without $E[X_1] < \infty$), Fatou (from the running infimum), dominated convergence (one integrable $Y$, bounded convergence on a probability space), Chebyshev, the chain a.s. and mean square to probability to distribution, and the three counterexamples (typewriter, spike, reflection) are all stated correctly. `q-const` (distribution to a constant implies probability) is right.
- Canvas data: all 15 typewriter frames, all 20 spike frames, the six digital bumps (widths 0.2 halving, area 0.018762), the dividend series (100 values), the tree series (7 values and the 10.4506 line), the bars (0.8^k, $m + 1$) and the layer-cake curves.
- No literal backslash-n in any prose field; no exclamation marks; no em-dashes or en-dashes.
- Fresh numbers: `r-simple`, `r-layer`, `r-heavy`, `r-tail`, `r-div`, `r-dom`, `r-cheb`, `h-tranche`, `h-sp`, `h-modes` and `h-geom` share no number or answer with a lesson. The repeats are items 9 to 13 and 22.
- Longform rubric (`h-long`): seven points of 1, 2, 1, 2, 1, 2 and 1 make 10; each is checkable; the model answer is correct (Fatou twice with the finite cancel, Lipschitz bound $e^{-rT}M$ with $E[Y] = 1$, the digital's spike of height $1/h$, and the likelihood-ratio remedy), except the constant in part 3 (item 15).

## Fix pass

All 24 findings fixed, none disputed. Every changed number was recomputed twice by independent routes (closed form and finite difference of the price, plus the lognormal-density route for the digital delta; NumPy reruns for the seed values). Validator 0 errors; playthrough of the four lessons, `review-2` and `homework-2` passes with and without `--mobile` (Pyodide, local CDN); voice scan 0 and 0. The `h-code` solution passes 9 of 9 tests and its example in CPython, the starter 0 of 9 and 0 of 1, and a `ddof=0` variant fails 2 (the two standard-error tests).

1. Error, l7 s1 option d: fixed. Option d is now the false "unbounded means no finite mean"; its `why` and `byKey.d` rewritten; the explanation notes that `E[X_n] = 1` is the symptom.
2. Error, l7 s9 `big`: fixed. The feedback now says "You scaled by 100" (94 = 100 x 0.94); value 94 kept.
3. Warning, r-div explanation: fixed, now `\ln 20 / \ln(1.07/1.02) = 62.6`.
4. Warning, l5 s9 explain: fixed, 0.0540.
5. Warning, l7 s3 order: fixed, `same` [[p3, p4]], prose says the two cancelling lines may swap. Also note 20 (p1 now ends "so also $|X| \le Y$ almost surely").
6. Warning, l6 s3 order: fixed by the main route. `m1` merged into `m6` and dropped; lines m2 to m6, `same` [[m4, m5]]; prose and step hint reworded. Verified `m6` no longer says "line one".
7. Warning, h-order: fixed. `f3` and `f4` merged into `f34`; answer f1, f2, f34, f5; `same` [[f2, f34]].
8. Warning, standard-error convention: fixed. `h-code` question and l7 s8 prompt state `ddof=1`; tests kept (the `ddof=0` form fails the two SE tests, as intended).
9. Warning, r-which: fixed. Now $X_n = 3n\mathbf 1_{\{U<1/n\}}$, mean 3; options b and d `why` and the correct feedback updated; key unchanged.
10. Warning, r-delta: fixed. Fresh digital S0 = 100, K = 105, r = 3%, sigma = 25%, T = 0.5, exact delta 0.021380 = 0.0214 (closed form, finite difference 0.0213798, density route 0.0213798). Option d now quotes 0.0214; the quotient in the explanation is discounted.
11. Warning, r-mode: fixed. Now $X_n = 2n\mathbf 1_{\{U<1/n^2\}}$ with $E[X_n^2] = 4$ in option b, feedback and explanation; key unchanged.
12. Warning, h-fatou: fixed. Spike $3n\mathbf 1_{\{U<1/n\}}$: part 1 key 0 (`wrong` `one` now 3), part 2 key 3, part 3 "$0 < 3$".
13. Warning, h-code numbers: fixed. Examples and tests moved to S0 = 100, K = 105, r = 0.03, sigma = 0.25, T = 0.5, n = 100000, seed 21: digital 0.021320863378961503 (SE 0.00010402382624449808), call 0.45659000268962846 (SE 0.003819911396832423); exact 0.021379762050349284 and 0.45907764450186667 (the 3-SE tests hold, 0.57 and 0.65 SE); strike-115 digital test (n = 200000, seed 13) 0.0161998 against exact 0.0162189; call-SE test now "> 0.0035"; explanation "0.0038 against 0.0018"; feedback "near 0.0214". Pathwise call SE for these inputs 0.0018307 (second route).
14. Warning, key lengths: fixed for all 10 (ratios now 0.56 to 1.46: r-delta 1.41, q-const 0.60, h-nu 1.39, r-which 1.37, h-fatou 0.56, l6 s6 1.44, l7 s7 1.21, l6 s5 0.87, q-hyp 1.18, l8 s8 0.67). Reasons moved into `feedback.correct` or kept in the explanation. `r-mode` is now 1.46 and l6 s4 1.48, within limit.
15. Warning, discounted quotient: fixed. l7 s5 prose "discounted quotient ... $e^{-rT}/h$", caption and explanation "tends to 0.0188"; `h-long` model part 3 and rubric point 6 use $e^{-rT}/h$ and "mean stays near $e^{-rT}c' = 0.0188$".
16. Note, h-tranche explain: fixed, $8(0.28650 - 0.04394)$.
17. Note, l7 s7 canvas: fixed, line at y = 5 labelled "Y = 5", axis to 5.5.
18. Note, l8 summary ideas[1]: fixed ("and mean square does by Chebyshev"). Idea 0 also split (note 23).
19. Note, l8 s5: fixed, `same` [[c1, c2]], prose and step hint updated.
20. Note, l7 s3 `p1`: fixed (with item 5).
21. Note, h-modes: fixed, `byKey` lines added for `r0c1`, `r1c1`, `r2c1`, `r3c1`, `r3c2`.
22. Note, h-nu part 1: fixed. n = 24: key 0.96, `wrong` `five` 0.04 ("You gave $1 - 0.96$"), question, label, accept and explanation updated.
23. Note, 20-word sentences: fixed in l6 s2, l7 s4, l7 s8, l7 s9, l8 s9, l8 s10, l8 summary ideas[0] and `h-geom`; voice scan reports 0 over 20 words.
24. Note, l7 s4 attribution: fixed, "$\Phi(0.35) = 0.6368$ and $\Phi(0.15) = 0.5596$".

### Changed keys

20 widgets changed a key, tolerance, options, numbers, order groups or `wrong` values:

- `l6-monotone-convergence` s3 order (line `m1` removed, answer m2 to m6, `same` m4/m5), s5 option a text, s6 option a text.
- `l7-dominated-convergence` s1 option d text and `why`; s3 order (`same` p3/p4, `p1` text); s7 option a text; quiz `q-hyp` option a text. (s9 `big`: feedback text only, value 94 unchanged.)
- `l8-modes-of-convergence` s5 order (`same` c1/c2); s8 option a text; quiz `q-const` option a text.
- `review-2` `r-which` (spike 3n: option a text, b and d `why`); `r-delta` (option a and d text, exact delta 0.0214); `r-mode` (2n spike, E[X^2] = 4 in b `why`).
- `homework-2` `h-fatou` part 1 (`wrong` `one` 1 to 3), part 2 (answer 1 to 3), part 3 (option a text); `h-order` (lines f3 and f4 merged into f34, answer, `same`); `h-nu` part 1 (answer 0.95 to 0.96, `wrong` `five` 0.05 to 0.04), part 3 (option a text); `h-code` (all examples and tests).
