# Answer check, topic 3.2, measure-prob level 4

Independent recomputation of every graded widget in `courses/measure-prob/` `l14-radon-nikodym`, `l15-likelihood-ratios`, `l16-girsanov-on-a-tree`, `l17-risk-neutral-rigorous`, `review-4` and `homework-4`. Neither the author's scripts nor `docs/reports/measure-prob-4.md` were used. Scripts are in the scratchpad folder `ac-mp4`.

**Method.**
- Exact arithmetic (`fractions`) and SciPy/NumPy for every number: the die weights (0.6, 0.6, 0.6, 1.2, 1.2, 1.8), `E_P[Z]` = 1, `E_Q[face]` = 4.2 (25.2 / 6; covariance 0.7), `Q(even)` = 0.6 and `Q({5, 6})` = 0.5, and the inverse weights 5/3, 5/6, 5/9; the one-step tree (S0 = £100, u = 1.2, d = 0.8, r = 5%, q = 5/8, call £11.9048, p = 0.7 weights 0.892857 and 1.25, kernel 0.850 and 1.190) and the two-step tree (weights 0.797194, 1.116071, 1.5625; call 15.5896; put 6.2925; unweighted 19.5556; parity 9.2971 against 100 - 100/1.05^2).
- l15: the tail 1 - Phi(4) = 3.1671e-5, the relative error per draw `sqrt(e^(theta^2) Phibar(a + theta) / p^2 - 1)` at theta = 0, 2, 4, 4.1, 4.12, 5, 6 (177.69, 7.26, 2.124, 2.1148, 2.1145, 2.665, 5.635), the minimisers by `minimize_scalar` (2.2159, 3.1548, 4.1197, 5.0972), and the seed-21 NumPy values with `default_rng(21)`: estimate 3.184972646057774e-05, standard error 6.729730145004383e-07, 4,994 draws above 4, weights summing to 0.31849726, plain maximum 3.61 (no tail day), inverted weights about 4.19e11 per 100,000 days. The `is_tail(2, 2.2, 5000, 8)` test value 0.022735909434736756 rebuilt in a second implementation.
- l16: the walk canvas replayed in Node from `walk.js` (seed 74, 300 paths, 20 steps, `K.rngFor`, one uniform and one Gaussian draw per step): plain average 4.05, weighted average -0.06 at q = 0.5 and 7.90 at q = 0.7, mean weight 0.999; the table of `E[ln Z_n]` and `Var(ln Z_n)` at n = 100 and 10,000 (-0.061263, 0.122450 and -0.061250, 0.122499); the 4-step fair running maximum 19/16; all four tree weights and prices.
- l17: q for three trees, the arbitrage gains, the discounted prices (114.29, 76.19, 130.61, 87.07, 58.05), the root averages under q and p (100 and 102.857), the trinomial martingale set, the Black-Scholes call 100 Phi(0.35) - 100 e^-0.05 Phi(0.15) = 10.45058 (digital 0.532325), the real-drift slip 15.526 and the undiscounted slip 10.986.
- review and homework: every key, slip and stated number, and for h-is the threshold 6 / sqrt 3 = 3.4641 (tail 2.6600e-4, best shift 3.6005, relative error 1.9636 against 61.305), for h-code all ten tests by brute force under both routes.
- Code: each solution and starter run in CPython with a copy of the `code.js` compare rules (`equal`, `isclose` with its `tol`, `fraction`, `raises`, `setup`; `prelude` first). Five code items, 51 hidden tests and 10 examples.
- Expressions: the four expression widgets run through the real `grade.js` `exprEqual` (CortexJS 0.30.2, with `\exp` rewriting from item 501, implicit products from 502): 69 cases, 51 equivalent learner forms (`\exp(...)`, `\frac`, `0.5`, reordered, reciprocal, products of exponentials) all pass and 18 non-equivalent forms (the named slips and neighbours) all fail.
- Order items checked against `order.js`: `same` makes the lines in a group interchangeable among their places. Each proof's dependency graph was written out and every valid order compared with the accepted set.
- Tables: ids checked against `table.js` (zero-based `r{row}c{col}`, column 0 the label). Lattice `bind` ids (`values.n2_2` = UU, `n2_1` = UD or DU, `n2_0` = DD) checked against the labels on the `l17` lattice.
- Numeric widgets, all: `answer`, `tol`, the number in `accept`, `wrong` bands (no overlaps with the answer band or each other), `feedback.correct`, `byKey` and `explain` agree. A script compared `answer` with `accept` for every numeric widget (no mismatch); the rest was read line by line.
- Choice keys: no second correct option in any choice item; key length against the longest distractor (limit 1.5). There are no multi widgets in these files.
- Text scans: literal backslash-n (none; the hits are LaTeX `\ne` and `\not`), exclamation marks (none; the hits are `\!` in LaTeX), em-dashes and en-dashes (none), sentence length, and numbers shared with a lesson (answers and prompt numbers of every review and homework item searched in the four lessons).

**Summary.** 83 widgets checked (82 graded plus one longform; table widgets counted once). Every key, tolerance and `wrong` value is right; one slip description does not match its value (item 4). Errors: 1. Warnings: 7. Notes: 8. The worst finding is item 1: the `l17` s9 table gives the share's drift under `P` as 12% on the tree, but with p = 0.7 on u = 1.2 and d = 0.8 it is 8% a step.

## Widgets checked

Key column: the keyed answer. Mine: my value. OK means the key, its tolerance, every `wrong` value and every stated number in the screen's prose, hints and explanation agree with my recomputation, and (reviews and homework) the numbers are not repeated from a lesson. See the numbered list for the exceptions.

| File | Screen or item | Key | Mine | Verdict |
|---|---|---|---|---|
| l14 | s0 table | 0.6, 0.6, 0.6, 1.2, 1.2, 1.8 (abs 0.01) | same; slips 1.67, 0.83, 0.56 are the inverses | OK |
| l14 | s1 numeric | 1 (abs 0.005) | 6 / 6 = 1; slip 6 right | OK |
| l14 | s2 choice | a | a only; d would force Q = P | OK |
| l14 | s3 table | 0.6, 0.5 | 3.6 / 6 = 0.6, 3 / 6 = 0.5; slips 0.5, 0.33 right | OK |
| l14 | s4 expression | `e^{\theta x-\theta^2/2}` | same; 15 learner forms pass, 7 wrong forms fail; `nocorrection` and `inverted` right | OK |
| l14 | s5 choice | a | a only; P << Q holds so d is false; dP/dQ = 2 on [0, 1] | OK |
| l14 | s6 choice | a | a only; 5/3, 5/6, 5/9 right | OK |
| l14 | s7 numeric | 4.2 (abs 0.02) | 25.2 / 6 = 4.2; slips 3.5, 25.2 right; covariance 0.7 | OK |
| l14 | s8 code | 10 tests | solution 10/10, examples 2/2, starter 0/10; 21/5, 3/5, 3/10, 102/5, 3 rechecked | OK |
| l14 | s9 table | 0.8929, 1.25, 11.9 | 0.892857, 1.25, 11.9048; slips 1.12, 0.8, 13.33; kernel 0.850 and 1.190 | OK |
| l14 | q-normal numeric | 0.5 | 0.5; slips 0, 0.125 | OK |
| l14 | q-reverse numeric | 2 | 1 / 0.5 = 2; slip 0.5 | OK |
| l14 | q-edge choice | a | a only, if P gives the face chance | OK; Note 13 |
| l14 | q-state numeric | 0.8 | 0.4 / 0.5 = 0.8; q = 0.6 right; slips 1.25, 0.4 | OK |
| l15 | s0 numeric | 0.3167 (abs 0.01) | 0.31671; slip 3.167 | OK |
| l15 | s1 slider | 4.1 (tol 0.5) | minimum 4.1197 (2.1145); 177.7, 7.26, 2.12 at 4, 2.66 at 5, 5.63 at 6 all right; bands 0 to 2.5 and 5.5 to 6 clear of 3.6 to 4.6 | OK |
| l15 | s2 numeric | 0.8681 (abs 0.001) | 125/144 = 0.868056; slips 1.152, 0.019 | OK |
| l15 | s3 choice | a | a only; at theta = 4 half the draws exceed 4 | OK |
| l15 | s4 expression | `e^{-\theta x+\theta^2/2}` | same; 11 learner forms pass, 5 wrong forms fail; e^-8 = 0.000335 | OK |
| l15 | s5 numeric | 2.1 (abs 0.1) | 2.113; slip 47.3 (47.33); slip 212.4 is the per-draw error 2.124 as a percentage | OK key; Warning 4 |
| l15 | s6 numeric | 3.185 (abs 0.02) | 3.18497; 4,994 above 4 and 0.3185 right; slips 49,940 and 0.3185 | OK |
| l15 | s7 code | 9 tests | solution 9/9, examples 2/2, starter 0/9; (3.18497e-05, 6.7297e-07), 0.0227359 and the four best shifts reproduce | OK |
| l15 | s8 numeric | 333 (abs 4) | (1.8258 / 0.1)^2 = 333.4; slips 73,980 (73,984), 18.3 | OK; Note 9 |
| l15 | q-plain numeric | 13.5 | 13.499; slip 135 | OK |
| l15 | q-weight numeric | 0.0183 | e^-4 = 0.018316; slips 54.6, 0.00248 | OK |
| l15 | q-edge numeric | 1 | e^0 = 1; slip 0 | OK |
| l15 | q-inverted choice | a | a only; 4.19e11 matches "about 4e11" | OK |
| l16 | s0 numeric | 0 (abs 0.6) | canvas replay -0.06; slips 4 (4.05), 10 | OK |
| l16 | s1 numeric | 8 (abs 1) | 20(2(0.7) - 1) = 8; canvas replay 7.90; slips 4, 14; -4, 0, 4, 8 right | OK |
| l16 | s2 table | 0.8333, 1.25, 1 | 5/6, 5/4, 0.6(5/6) + 0.4(5/4) = 1; slips 1.2, 0.8 | OK |
| l16 | s3 numeric | 0.8681 (abs 0.001) | (5/6)^2 (5/4) = 125/144; slips 1.152, 1.0417 (25/24) | OK |
| l16 | s4 order | m1 to m4, same m2/m3 | proof valid; m2 and m3 both need only m1; d1, d2 false | OK; Note 14 |
| l16 | s5 choice | a | a only; options b, c, d give Z_n, Z_n, Z_n / Z_N at X = 1 | OK |
| l16 | s6 expression | `e^{-\theta w-\theta^2 t/2}` | same; 12 learner forms pass, 5 wrong forms fail; table values -0.06126, 0.12245 and -0.06125, 0.12250 reproduce | OK |
| l16 | s7 choice | a | a only; 5/6-only weight averages 0.9; the 2/3 step has mean 0 but is not a reweighting | OK |
| l16 | s8 code | 10 tests | solution 10/10, examples 2/2, starter 0/10; 125/144, 125/64, 0, 1, 19/16, 8/5 reproduce | OK |
| l16 | s9 table | 0.7972, 1.1161, 1.5625, 15.59 | 0.797194, 1.116071, 1.5625; 15.5896; slip 19.56 | OK |
| l16 | q-down numeric | 1.25 | 0.5 / 0.4 = 1.25; slip 1 (average 0.9) | OK |
| l16 | q-edge choice | a | a only; at q = 1 down weight is 0, Q << P holds, P << Q fails | OK |
| l16 | q-drift numeric | 0.1 | 2(0.55) - 1 = 0.1; slips 0.2, 0.55 | OK |
| l16 | q-path numeric | 0.9453 (abs 0.0005) | (0.55/0.6)^2 (0.45/0.4) = 0.945313; slips 1.0579, 0.8403 | OK |
| l17 | s0 table | 114.29, 102.86 | 114.2857, 102.857; slips 108.84, 117.55 and 100.00 | OK |
| l17 | s1 choice | a | a only; b, c, d false | OK; Note 11 |
| l17 | s2 numeric | 1.0417 (abs 0.0005) | 0.25 / 0.24 = 1.041667; slips 0.625, -0.0417; gain £1 to £25 | OK |
| l17 | s3 order | a1 to a4 | proof valid and forced in order; d1 (P-martingale) and d2 false | OK |
| l17 | s4 numeric | 6.29 (abs 0.01) | 6.9375 / 1.1025 = 6.2925; slips 6.61, 4.46; parity 9.30 | OK |
| l17 | s5 choice | a | a only (product rule); b, c, d each name the slip they describe | OK key; Warning 3 |
| l17 | s6 numeric | 15.59 (abs 0.01) | 15.5896; slips 19.56, 16.37; gap £3.97 | OK |
| l17 | s7 numeric | 10 (abs 0.05) | 20q_u with q_u in (0, 1/2): supremum 10, not attained; slips 20, 6.67 | OK key; Warning 2 |
| l17 | s8 code | 12 tests | solution 12/12, examples 2/2, starter 0/12; 5/8, 3/5, 250/21, 6875/441, 925/147, 400/441 reproduce | OK |
| l17 | s9 choice | a | a only; table row "Drift of the share" is wrong | OK key; Error 1 |
| l17 | q-q numeric | 0.4667 | 0.07 / 0.15 = 0.466667; slip 0.5333 | OK |
| l17 | q-arb choice | a | a only; sure gain £1 to £25 | OK |
| l17 | q-bs numeric | 10.4506 (abs 0.002) | 10.45058; 63.6831 - 53.2325; slips 15.53 (15.526), 10.99 (10.986) | OK |
| l17 | q-incomplete choice | a | a only | OK |
| review | r-weights numeric | 22.5 | Z = (1/2, 1, 2); 2.5 + 5 + 15; slip 17.5 | OK |
| review | r-is numeric | 0.0025 (abs 0.0001) | e^-6 = 0.002479; slips 403.4, 2.75e-05 | OK |
| review | r-girs numeric | 0.9183 | (0.5/0.55)^2 (0.5/0.45) = 0.918274; slips 1.089, 0.8264 | OK |
| review | r-q numeric | 0.52 | 0.13 / 0.25 = 0.52; slip 0.48 | OK |
| review | r-ac choice | a | P << Q, not Q << P; dP/dQ = (3/2, 3/2, 0); b, c, d false | OK; Note 16 |
| review | r-n numeric | 17182 (abs 100) | 42.956 / 0.0025 = 17,182.4; 6.554; slip 131 | OK |
| review | r-arb choice | a | a only; q = 14/13 = 1.0769; gain at least £1 | OK |
| review | r-twostep part 1 numeric | 1.44 | 1.2^2 = 1.44; slip 0.6944 | OK key; Warning 5 |
| review | r-twostep part 2 numeric | 7.27 (abs 0.01) | 7.56 / 1.0404 = 7.2664; slips 5.05, 7.41 | OK key; Warning 5 |
| homework | h-expect part 1 numeric | 4 | 0.4 / 0.1 = 4; slip 0.25 | OK |
| homework | h-expect part 2 numeric | 3 | 0.1 + 0.4 + 0.9 + 1.6 = 3; slip 2 | OK |
| homework | h-expect part 3 numeric | 10 | 0.1 + 0.8 + 2.7 + 6.4 = 10; slip 5; variance 1 | OK |
| homework | h-is part 1 numeric | 26.6 (abs 0.05) | 26.6003; slip 2275 (2275.01) | OK |
| homework | h-is part 2 numeric | 3.6 (abs 0.1) | 3.6005; slip 3.4641; bands clear | OK |
| homework | h-is part 3 numeric | 386 (abs 5) | (1.9636 / 0.1)^2 = 385.6; slip 375,836 | OK key; Warning 8 |
| homework | h-density part 1 expression | `e^{\theta w-\theta^2 t/2}` | same; 9 learner forms pass, 5 wrong forms fail | OK |
| homework | h-density part 2 numeric | 1.1205 (abs 0.0005) | e^0.11375 = 1.120472; slips 0.7896, 1.1912 | OK key; Warning 7 |
| homework | h-tree part 1 numeric | 2.0408 | (0.5/0.35)^2 = 2.040816; slip 0.49 | OK |
| homework | h-tree part 2 numeric | 4.31 | 4.75 / 1.1025 = 4.3084; slips 2.11, 4.52 | OK |
| homework | h-tree part 3 numeric | 4.31 | 0.25 (19) / 1.1025 = 4.31 at p = 0.8; slip 0.69 (0.6893) | OK |
| homework | h-tri part 1 numeric | 15 | 30 q_d with q_d in (0, 1/2): 15; slip 30 | OK |
| homework | h-tri part 2 numeric | 0.2 | 6 / 30 = 0.2; slip 6 | OK |
| homework | h-tri part 3 numeric | 6 | 30 (0.2) = 6; parity 6 - 6 = 0; slip 18 | OK |
| homework | h-arb part 1 numeric | 1.1538 | 15/13 = 1.153846; slip -0.1538 | OK |
| homework | h-arb part 2 numeric | 2 | 110 - 108 = 2; slip 15 | OK |
| homework | h-order order | c1 to c5 | proof valid and forced in order; e1, e2 false | OK; Note 12 |
| homework | h-code code | 10 tests | solution 10/10, examples 2/2, starter 0/10; all ten pairs match brute force (35/16, 9/16, 9/4, 1/4, 2, 7/5, 3/10, 43/25, 1, 11/8) | OK; Note 16 |
| homework | h-long longform | 5 rubric points, 10 marks | 2 + 2 + 2 + 2 + 2 = 10; model correct (q, Z_2, 0.3906, 0.4688, 0.1406, 102.86, 15.59, 19.56) | OK; Warning 6 |

## Mismatches

Errors

1. **Error. `l17-risk-neutral-rigorous.json` screens[9] (`The interview question`), canvas table row "Drift of the share": the `P` cell says $12\%$.** The table is headed "for our tree" (up chance 0.7, u = 1.2, d = 0.8). Its one-step mean return is 0.7(1.2) + 0.3(0.8) - 1 = 8%, and the discounted price drifts 8% less 5%, about 2.9% (the screen 0 root, £102.86 against £100). The 12% belongs to the continuous-time model of screen 5, not to this tree. Fix: change the cell `"$12\\%$"` to `"$8\\%$"` (so the row reads $8\%$ and $r = 5\%$). The `why` of option c ("$p = 0.7$ gives a drift above $r$") is then also right, and no other text on the screen uses 12%.

Warnings

2. **Warning. `l17-risk-neutral-rigorous.json` screens[7] (`An incomplete market`), question "What is the largest price any martingale measure allows?"** Every `q` must be positive, so $q_u < \tfrac12$ and the price $20q_u$ stays strictly below 10 and never reaches it; there is no largest price, only a supremum. The explanation already says "strictly between £0 and £10", and `homework-4` `h-tri` phrases the same fact correctly ("anything strictly between £0 and what?"). Fix: question "The call struck at £100 costs $20q_u$. Every martingale measure prices it below what number?" Key 10, tolerance, `accept` ("10: q_u must stay below 1/2") and feedback unchanged.
3. **Warning. `l17-risk-neutral-rigorous.json` screens[5] (`The same fact in continuous time`), the key is visibly longer than the distractors.** Key `a` is 54 characters; the distractors are 25, 19 and 20, a ratio of 2.16 against the 1.5 limit. Fix: key `a` "No $dt$ term: only $\\sigma e^{-rt}S_t\\,d\\tilde W_t$ is left" (about 48 characters), and lengthen the distractors to `b` "$(\\mu - r)e^{-rt}S_t\\,dt$, the excess return", `c` "$r\\,e^{-rt}S_t\\,dt$, the share's drift under $Q$", `d` "$-r\\,e^{-rt}S_t\\,dt$, the discount's own drift" (about 40 to 45 each, ratio about 1.15). The `why` texts and the explanation are unchanged.
4. **Warning. `l15-likelihood-ratios.json` screens[5] (`How good is one run?`), `wrong` `perdraw` (212.4) and `byKey.perdraw`.** The value 212.4 is the per-draw relative error 2.124 written as a percentage (212%); the text says "You gave the per-draw error 2.12 as if it were a percentage". A learner who types 2.12, the per-draw ratio itself, lands inside the key band 2.1 +/- 0.1 and is marked right, because the run's percentage error (6.73e-7 / 3.185e-5 = 2.113%) and the per-draw ratio (2.12) differ by a factor of exactly $100/\sqrt{10{,}000}$ = 1. So the named slip is never caught as written, and the text misdescribes the value that is. Fix: `byKey.perdraw` becomes "You gave the per-draw error as a percentage, 212%. The run averages 10,000 draws, so divide by $\\sqrt{10{,}000} = 100$ to get the error of the whole run, 2.1%." Optionally narrow the key to `tol` abs 0.05 (2.05 to 2.15 still holds 2.113 and 2.12); the coincidence cannot be removed without changing the threshold or the draw count (for example 40,000 draws give 1.06%).
5. **Warning. `review-4.json` `r-twostep` repeats the `l14` quiz `q-state` setup.** The tree u = 1.1, d = 0.9, r = 2%, p = 0.5, q = 0.6 is that quiz's tree, and `q-state` already states the up weight 1.2 that part 1 squares to 1.44. DECISIONS "Fresh numbers in reviews and homework" bars this. Fix, checked by an exact tree: S0 = £100, u = 1.3, d = 0.7, r = 3% a step, p = 0.45, so q = 0.55; the call struck at £100 pays £69 on UU (S = 169) and 0 elsewhere. Part 1: $Z_2$ on UU = $(0.55/0.45)^2$ = 1.4938 (`inverted` $(0.45/0.55)^2$ = 0.6694; the explanation's per-step weight 1.2222). Part 2: $0.2025 \times 1.4938 \times 69 / 1.0609$ = £19.67, since the weighted sum 20.8725 equals $q^2 \times 69$ = 0.3025 x 69 (`real` slip $0.2025 \times 69/1.0609$ = 13.17; `onedisc` slip 20.8725 / 1.03 = 20.26). Update `accept`, `feedback` and `explain` text to match ("Only UU is in the money: $130 \times 1.3 = 169$").
6. **Warning. `homework-4.json` `h-long` repeats the lesson numbers.** The whole item is the trees tree with p = 0.7: $Z_2$ = 0.7972, 1.1161, 1.5625, the discounted prices, the root 102.86, the call £15.59 and £19.56 are all keyed or worked in `l16` s9, `l17` s0 and s6. The shared course numbers may appear in lessons only. Fix, checked by an exact tree: S0 = £100, u = 1.25, d = 0.75, r = 4% a step, real up chance p = 0.65. Part 1: q = (1.04 - 0.75)/0.5 = 0.58; one-step weights 0.58/0.65 = 0.8923 and 0.42/0.35 = 1.2; $Z_2$ = 0.7962 (UU), 1.0708 (UD or DU), 1.4400 (DD); check 0.4225(0.7962) + 0.455(1.0708) + 0.1225(1.44) = 0.3364 + 0.4872 + 0.1764 = 1; the `Q`-chances 0.3364, 0.4872, 0.1764. Part 2: discounted prices £100; £120.19, £72.12; £144.46, £86.68, £52.01; under `Q` 0.58(144.46) + 0.42(86.68) = 120.19, 0.58(86.68) + 0.42(52.01) = 72.12 and 0.58(120.19) + 0.42(72.12) = 100; under `P` the root 0.65(120.19) + 0.35(72.12) = 103.37, not 100. Part 4: only UU pays £56.25 (S = 156.25), so $0.3364 \times 56.25/1.0816$ = £17.49 and, weighted, $0.4225 \times 0.7962 \times 56.25/1.0816$ = £17.49; weighting by $p^2$ alone gives $0.4225 \times 56.25/1.0816$ = £21.97. Update the prompt, `model` and the rubric numbers (the rubric item 2 "102.86" becomes 103.37; item 4 "£15.59" becomes £17.49). Part 3 and Part 5 text need no number changes.
7. **Warning. `homework-4.json` `h-density` part 2 repeats the `l16` s6 numbers.** It takes $\theta = 0.35$, $T = 1$ and the term $-0.06125$, which is the limit mean $-\theta^2/2$ in the `l16` s6 table. Fix: $\theta = 0.4$, $T = 1$, $\tilde W_T = 1$. Then the exponent is $0.4 - 0.08 = 0.32$ and $\tfrac{dP}{dQ} = e^{0.32}$ = 1.3771 (key 1.3771, abs 0.0005); `dqdp` slip $e^{-0.4 - 0.08} = e^{-0.48}$ = 0.6188; `nocorrection` slip $e^{0.4}$ = 1.4918. Update `accept` ("e^0.32 = 1.3771"), the feedback texts ("The exponent is $0.4 \\times 1 - 0.4^2/2$", "$-0.4 - 0.08$", "$-\\theta^2T/2 = -0.08$") and the explanation ("$0.4 - 0.08 = 0.32$").
8. **Warning. `homework-4.json` `h-is` part 3 explanation states "$(61.3/0.10)^2 = 375{,}836$".** From 61.3 the square is 375,769 (613^2); 375,836 comes from the unrounded error 61.3055. A learner who checks the line gets a different number. The `wrong` value 375836 (tol 500) and the answer 386 (tol 5) both hold. Fix: write "$(61.3/0.10)^2 \\approx 375{,}800$, about 970 times as many" in the explanation, and the same in `feedback.correct` ("against about 375,800 for plain sampling"); keep the `wrong` value 375836. The "about 970 times" holds (375,836 / 386 = 974).

Notes

9. **Note. `l15-likelihood-ratios.json` screens[8] explanation and `wrong` `plain` (73980).** The text writes "$(27.2/0.10)^2 = 73{,}980$"; from 27.2 the square is 73,984, and 73,980 comes from the unrounded 27.1992. Fix: "$(27.2/0.10)^2 \\approx 74{,}000$" in the explanation and "73,980" kept only as the `wrong` value; the "222 times fewer" holds either way.
10. **Note. `l15-likelihood-ratios.json` summary idea 3.** "Best $\\theta$ sits near the threshold: 4.12 for $a = 4$. On seed 21 it gives 3.185 per 100,000 days" reads as if the seed-21 run used 4.12; it used $\\theta = 4$. Fix: "On seed 21 with $\\theta = 4$ it gives 3.185 per 100,000 days with a 2.1% standard error."
11. **Note. `l17-risk-neutral-rigorous.json` screens[1] explanation: "Shreve II, section 5.4, proves it for finite markets".** Shreve II section 5.4 states the fundamental theorems for the Brownian (continuous-time) model; the finite-market statement is the binomial and finite-state material of Shreve I (and Harrison and Pliska, as the prose says). Fix: "Harrison and Pliska prove it for finite markets; Shreve II, section 5.4, gives the Brownian version." The summary note citing Shreve II 5.4 is fine as further reading.
12. **Note. `homework-4.json` `h-order`: the proof divides by $Z_n$ without saying $Z_n > 0$.** The prose says only "$Z_n$ is the density of $Q$ on $\mathcal F_n$". If $Q$ is merely absolutely continuous, $Z_n$ can be 0 and $Y$ is undefined there. Fix: "Let $Z_n$ be the density of $Q$ on $\mathcal F_n$, with $Q$ equivalent to $P$ so that $Z_n > 0$, and let $Y = \dots$". Nothing else changes.
13. **Note. `l14-radon-nikodym.json` quiz `q-edge`: "A weight $Z$ is 0 on one face of a die".** Option a ("$P \not\ll Q$") needs $P$ to give that face chance; if $P$ gave it none, $Z$ there is arbitrary and $P$ and $Q$ could still be equivalent. Fix: "A weight $Z = \\tfrac{dQ}{dP}$ is 0 on one face of a fair die and positive elsewhere."
14. **Note. `l16-girsanov-on-a-tree.json` screens[4] (order): a valid but odd order is marked wrong.** `m3` ($E_P[z \mid \mathcal F_n] = 1$) is a free-standing lemma, so `m3, m1, m2, m4` is a valid proof, but `same` [[m2, m3]] accepts `m3` only in slots 2 and 3. The explanation already says "both need only the first". Fix if wanted: start `m3` with "Then" so it follows `m2`, and drop `same`, giving the single order m1, m2, m3, m4 (the explanation's last sentence goes). Leaving it as it is costs nothing but a rare rejected order.
15. **Note. Sentences of exactly 20 words.** The voice rule is under 20. Counting maths as one word: `l14` s9 prose, `l15` s6 prose and s8 prose, `l16` s7 option b `why`, `l16` s8 `feedback.correct`, `l17` s1 explanation, `l17` s3 line a2, `l17` s3 `feedback.correct`, `l17` s9 `feedback.correct`, `homework-4` h-arb part 2 explanation and the `h-long` model Part 3. Fix if wanted: split each at its comma.
16. **Note. Setups that echo a lesson without repeating a keyed answer.** `review-4` `r-ac` is the `l14` s8 hidden-test pair with the roles swapped (P = (1/3, 1/3, 1/3) and Q = (1/2, 1/2, 0) there; P = (1/2, 1/2, 0) and Q = (1/3, 1/3, 1/3) here, with weights (3/2, 3/2, 0) in both). `homework-4` `h-code` uses the `l16` s8 prelude (p = 3/5, q = 1/2 and 11/20, `S`, `runmax`) with different functions and numbers. None repeats a visible answer. Fix if wanted: `r-ac` with P = (1/4, 3/4, 0) and Q = (1/2, 1/4, 1/4), and `h-code` with p = 2/5 and q = 1/2.

## Checks with nothing found

- Every numeric `wrong` band lies outside its answer band and outside every other wrong band; table `byKey` ids match their rows and columns in all six tables (zero-based, column 0 the label) and the `l16` s9 `bind` ids match the lattice.
- No choice item has two correct options; every distractor has a `why`. Choice-key length ratios (key over longest distractor): `l14` 1.00, 0.73, 0.42, 1.12; `l15` 1.00, 1.29; `l16` 1.00, 1.07, 1.36; `l17` 1.12, 1.43, 0.77, 1.25 (and 2.16 in item 3); review 0.71 and 1.01. All within 1.5 except item 3.
- Order keys: `l16` s4, `l17` s3 and `homework-4` `h-order` are valid proofs and their distractors are false as the `why` texts say. `l17` s3 and `h-order` are chains with one valid order each, so the missing `same` groups are right.
- Theorem statements: Radon-Nikodym (Q << P gives a weight; the weight is >= 0 with mean 1), chain rule and inverse weight (needs equivalence, said), importance sampling `E_P[f] = E_Q[f dP/dQ]` (normals are equivalent), Girsanov on a tree (Z_n is a P-martingale with mean 1, Q-drift 2q - 1, the weight is 0 at q = 1 so equivalence fails), Bayes' rule for conditional expectations (`E_Q[X | F_n] = E_P[Z_N X | F_n] / Z_n`), the continuous limit (mean -theta^2/2, variance theta^2, `dQ/dP = exp(-theta B_T - theta^2 T/2)`), the easy direction of the fundamental theorem (an equivalent martingale measure, a martingale transform, `E_Q[V~_N] = 0`, equivalence back to P; the finite market makes every expectation exist), and the incomplete trinomial market (q_u = q_d, q_m = 1 - 2q_u > 0). The hypotheses stated in each are the ones used (item 12 aside).
- Canvas data: the die bars (0.1, 0.2, 0.3), the uniform pair, the Gaussian pair and weight, the `l15` caption formula (equal to my relative error), the `l16` walk overlay formulas (`p` and `q` are the P up and down chances), the `l16` s5 tree weights (0.8333, 1.25, 0.6944, 1.0417, 1.5625), the `l17` lattice labels and the P and Q mean curves (100 e^{0.07 t} against 100).
- All five code items: each solution passes all its tests and examples; each starter fails every one (0 of 51 hidden tests, 10 + 9 + 10 + 12 + 10, and 0 of 10 examples). Stated counts in `how` and `feedback.correct` (10, 9, 10, 12, 10) match.
- Longform rubric (`h-long`): five points of 2 make 10; each is checkable; the model answer is correct in all five parts (the arithmetic is checked above).
- Fresh numbers: `r-weights`, `r-is`, `r-girs`, `r-q`, `r-ac`, `r-n`, `r-arb`, `h-expect`, `h-is`, `h-tree`, `h-tri`, `h-arb`, `h-order` and `h-code` share no keyed answer with a lesson. The repeats are items 5, 6 and 7 (and the setups in item 16).
- Stale-value check: for every numeric widget `answer`, `accept`, `feedback.correct`, the explanation and the console or hint numbers agree (the earlier slip, an old value in `answer` against a new `accept`, does not occur).
- No literal backslash-n in any prose field (the hits are `\ne`, `\not`); no exclamation marks; no em-dashes or en-dashes; no explanation over three sentences.
