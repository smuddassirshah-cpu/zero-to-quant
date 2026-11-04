# Answer check, topic 3.2, measure-prob level 3

Independent recomputation of every graded widget in `courses/measure-prob/` `l9-information`, `l10-condexp-projection`, `l11-filtrations`, `l12-martingales-defined`, `l13-stopping-times`, `review-3` and `homework-3`. Neither the author's scripts nor `docs/reports/measure-prob-3.md` were used. Scripts are in the scratchpad folder `ac-mp3`.

**Method.**
- Exact arithmetic (`fractions`, SymPy linear systems, NumPy) for every number: atom and event counts; the three-point projection and its error; the random-vars l15 joint table (`E[Y | X]` = -0.8, 0.2, 1.0; `E[Y]` = 0.24; `E[XY]` = 0.46; `Var(Y)` = 2.2624; row variances 1.76, 1.96, 1.8; `Var(E[Y | X])` = 0.3904; `E[Var(Y | X)]` = 1.872), checked cell by cell against `random-vars` l15 and l17; the Longstaff-Schwartz least-squares line; the lookback maxima; the Doob trees; the 3/5 and 3/4 drifts; the discounted-price averages; the gambler's-ruin numbers (probability and `E[T]` for eight start/end/chance triples, by a linear solve, not the closed form); the exact distribution of the maximum of 10 steps (11 bars, mean 1067/512, `E|S_10|` = 2.4609); `E[max]` for 0, 2, 4 and 10 steps; the capped biased-walk mean 6043193/9765625.
- Markov level 5 fair-walk numbers, recomputed by a 200-step absorbing-chain recursion: reach 10 from 3 with chance 0.3 (0.299977 by step 200, 3/10 in the limit), `E[T]` = 21, still going after 50 steps 0.085183 (0.0852), after 200 steps 0.0000458459 (0.0000458). They are not stated in these seven files; they agree with the walk numbers that are.
- Walk canvas: the real `walk.js` draw order (seed 18, 300 paths, 200 steps, `K.rngFor`, one uniform and one Gaussian draw per step) replayed in Node. Start 3, ends 0 and 10: 90 hit the top, 210 the bottom, none unfinished, average of `S_T` exactly 3.00 (matches the `l13` s0 explanation). Start 0, ends -3 and 1: 225 up, 75 down, none unfinished.
- Code: each solution and starter run in CPython with a copy of the `code.js` compare rules (`fraction` needs a `Fraction`, `equal` is `==` after `tolist()`, `prelude` first). Six code items, 61 hidden tests.
- Order items checked against `order.js`: the `same` groups make the lines in a group interchangeable among their places, so any order outside those slot patterns is rejected. Each proof's dependency graph was written out and every valid order compared with the accepted set.
- Grid, tap-region and table ids checked against `grid.js` (one-based `r{row}c{col}` on a grid) and `table.js` (zero-based `r{row}c{col}`, column 0 the label). Numeric `wrong` bands checked against the answer band and each other (no overlaps). Choice and multi options checked for a second correct option. Key length against the longest distractor (limit 1.5). Sliders: `wrong` checks run before the answer-off check, as in `sliders.js`.
- Text scans: literal backslash-n, exclamation marks, em-dashes and en-dashes (none found; the only `\n` hits are the LaTeX `\ne` in `l13` s6 and quiz q-fixed), sentence length.

**Summary.** 92 widgets checked (91 graded plus one longform). All keys are right except one wrong-value slip. Errors: 3. Warnings: 8. Notes: 6. The worst finding is item 1: `l10` s10 offers 7.74 as the "positive slope" slip, but a positive slope gives £1.68 (or £109.68), so the feedback names a slip the number does not make.

## Widgets checked

Key column: the keyed answer. Mine: my value. OK means the key, its tolerance, every `wrong` value and every stated number in the screen's prose, hints and explanation agree with my recomputation, and (reviews and homework) the numbers are not repeated from a lesson. See the numbered list for the exceptions.

| File | Screen or item | Key | Mine | Verdict |
|---|---|---|---|---|
| l9 | s0 tap-regions | r1c1 to r1c4 | HHH, HHT, HTH, HTT; `two-heads` set is "at least two heads" | OK |
| l9 | s1 multi | a, d | a, d only (b and c split a group) | OK |
| l9 | s2 numeric | 4 (abs 0) | 4; 2, 8, 3 (values of `S_2`) match | OK |
| l9 | s3 table | 4, 16, 8, 256 | 4, 2^4 = 16, 8, 2^8 = 256; byKey r0c1, r0c2, r1c1, r1c2 match | OK |
| l9 | s4 multi | a, b | `S_2` and the match indicator; c and d change inside an atom | OK |
| l9 | s5 choice | a | a only; sizes 1, 3, 3, 1, 16 events | OK |
| l9 | s6 numeric | 8 (abs 0) | 2^3 = 8; 16, 3, 4 match | OK |
| l9 | s7 choice | a | a only (d is a false reason) | OK |
| l9 | s8 code | 11 tests | solution 11/11, examples 2/2, starter 0/11 | OK |
| l9 | s9 table | 120, 100 | UD 100, 120, 96 gives 120; DU 100, 80, 96 gives 100 | OK; Warning 5 (payoff undefined) |
| l9 | s10 choice | a | a only; payoffs £20 and £0 hold only for `max(M - 100, 0)` | OK key; Warning 5 |
| l9 | q-trivial choice | a | a only | OK |
| l9 | q-events5 numeric | 65536 | 2^16 = 65536; 16, 32, 2^32 = 4294967296 match | OK |
| l9 | q-tails choice | a | a only (HH gives 0, HT gives 1) | OK |
| l9 | q-s4 numeric | 32 | 2^5 = 32; 5, 16, 65536 match | OK; Note 17 (id) |
| l10 | s0 sliders | a = 2, b = 5 (tol 0.1) | (2, 2, 5), error 2/3; `mean` and `x` slips match | OK |
| l10 | s1 numeric | 1.3333 (abs 0.001) | 4/3; 4, 2, 3 match | OK |
| l10 | s2 table | -0.8, 0.2, 1.0 | -0.8, 0.2, 1.0; table equals random-vars l15 | OK |
| l10 | s3 table | 0.24, 0.46, 0.46 | 0.24, 0.46, 0.46; E[X] = 0.1 so 0.024 is the independence slip | OK |
| l10 | s4 table | 0.3904, 1.872 | 0.3904, 1.872; 0.448 - 0.0576; sum 2.2624 | OK |
| l10 | s5 choice | a | a only | OK |
| l10 | s6 order | t1 to t6, same t2/t3, t4/t5 | proof valid; t2 can also follow t4 or t5 | Warning 6 |
| l10 | s7 choice | a | a only; 8/3 and 2/3 right | OK |
| l10 | s8 multi | a, b | a, b only | OK |
| l10 | s9 code | 10 tests | solution 10/10, examples 2/2, starter 0/10 | OK |
| l10 | s10 numeric | 10.32 (abs 0.01) | slope -135/250 = -0.54, line 60 - 0.54x, 10.32; slips 6, 12 right | OK key; Error 1 (`slope` 7.74) |
| l10 | q-four numeric | 7 | 7; 5, 6, 3 | OK |
| l10 | q-split numeric | 4 | 10 - 6 = 4; 16, 0.6, 6 | OK |
| l10 | q-known choice | a | a only | OK |
| l10 | q-tower choice | a | a only | OK |
| l11 | s0 table | 1, 2, 4, 8 | 1, 2, 4, 8 | OK |
| l11 | s1 multi | a, b, c | a, b, c; d and e look ahead | OK |
| l11 | s2 choice | a | a only | OK |
| l11 | s3 choice | a | a only | OK |
| l11 | s4 table | 0, 1, 1, 0, 0, 4 | H = (0, 1, 1, 0), gain 0, look-ahead 4; byKey r3c1, r4c1, r5c1 match | OK |
| l11 | s5 numeric | 10 (abs 0) | 10; 0, 5, 1 | OK |
| l11 | s6 multi | a, b, c | a, b, c; d false | OK |
| l11 | s7 code | 10 tests | solution 10/10, examples 2/2, starter 0/10 | OK |
| l11 | s8 numeric | 250 | 250; 0, 1, 125 | OK |
| l11 | q-pred choice | a | a only | OK |
| l11 | q-dip numeric | 1 | H = (0, 1, 1, 0, 1), gain 1; slip -1 is "hold after H" (exact), 3 is the unsigned sum, 0 | OK |
| l11 | q-first choice | a | a only | OK |
| l11 | q-min choice | a | a only; true at n = 1 as well | OK |
| l12 | s0 table | 0.5, 0.75, 0.25, 1, 0.5, 0.5, 0 | same; byKey r0c1, r1c1, r2c1 match | OK |
| l12 | s1 choice | a | a only | OK |
| l12 | s2 order | a1 to a4 | single valid order; d1 and d2 false | OK |
| l12 | s3 order | b1 to b4 | valid; b1 first is needed for the conditional expectation | OK |
| l12 | s4 choice | a | a only | OK |
| l12 | s5 numeric | 0.2 (abs 0.001) | 2(0.6) - 1 = 0.2; 0.6, 0.4, 1.2 | OK |
| l12 | s6 choice | a | a only; both one-step checks hold, X3 given (1, 0) is 1; means 0 at each time | OK |
| l12 | s7 code | 10 tests | solution 10/10, examples 2/2, starter 0/10; 81/125 = 0.648 | OK |
| l12 | s8 numeric | 102.86 (abs 0.01) | 102.857; q = 0.625; 100, 108, 95.24 | OK |
| l12 | q-const choice | a | a only | OK |
| l12 | q-doob numeric | 2 | 1 + 1 = 2; 1.5, 1, 3 | OK |
| l12 | q-mean choice | a | a only | OK |
| l12 | q-drift numeric | 0.5 | 0.5; 0.75, 0.25, 1.5 | OK |
| l13 | s0 numeric | 3 (abs 0.5) | 3.00 exactly (90 of 300 hit 10); 5, 10, 0.3 | OK |
| l13 | s1 multi | a, b, c, d | a, b, c, d; e and f look ahead | OK |
| l13 | s2 order | s1 to s4, same s2/s3 | valid; s3 needs only s1 so the swap is right; x1 is false | OK |
| l13 | s3 order | o1, o2, o3 | valid; o1 and o2 are independent and can swap | Warning 7 |
| l13 | s4 choice | a | a only; bound 100 right | OK key; Warning 11 (feedback) |
| l13 | s5 numeric | 21 (abs 0) | 100(3/10) - 9 = 21 = 3 x 7; 30, 9, 39 | OK |
| l13 | s6 choice | a | a only; P(depth beyond k) is 1/(k+1), so the sup has infinite mean | OK; Note 12 |
| l13 | s7 numeric | 2.084 (abs 0.005) | 1067/512 = 2.083984; 11 bars right (252, 210, 210, 120, 120, 45, 45, 10, 10, 1, 1 over 1024); 2.4609 = E abs S_10; 0, 10 | OK |
| l13 | s8 code | 10 tests | solution 10/10, examples 2/2, starter 0/10; 6043193/9765625, 19/16, 1067/512 reproduce | OK; Note 13 |
| l13 | s9 table | 0.75, 3, 0.5938 | 3/4; 3 x 1 = 3; 19/16 x 0.5 = 0.59375 (for the maximum including the buying price) | OK key; Warning 4 |
| l13 | q-ruin numeric | 0.3333 | 4/12; 0.5, 0.6667, 0.4 | OK |
| l13 | q-time numeric | 32 | 4 x 8 = 32; 48, 12, 16 | OK |
| l13 | q-which choice | a | a only | OK |
| l13 | q-fixed choice | a | a only | OK |
| review | r-event choice | a | a only; why b and c right | OK; Note 14 (repeat of l9) |
| review | r-die numeric | 2.6667 (abs 0.0005) | 8/3 = 2.666667; 35/12 = 2.9167, 0.25 | OK |
| review | r-tower numeric | 6 | 6; 12, 8 | OK |
| review | r-pred multi | a, b | a, b only | OK |
| review | r-gain numeric | 2 | positions (0, 1, 1, 1, 1), gain 2; 0, 5, 3; 32 paths | OK |
| review | r-cube choice | a | `S^3 - 3nS` a martingale (symbolic); `S^3 + 3S`, `S^2 + 1` right | OK, key long (1.36 of 11 chars) |
| review | r-doob numeric | 2.4 | 1 + 1.4 = 2.4; 2.1, 3, 2; 0.7(2.4) + 0.3(1.4) = 2.1 | OK; Note 14 |
| review | r-stop multi | a, b | a, b only | OK; Note 14 |
| review | r-ruin table | 0.4, 54 | 6/15 = 0.4; 225(0.4) - 36 = 54 (linear solve agrees) | OK |
| review | r-agree numeric | 6 | 6; 2, 8, 3; 2 atoms, 4 events | OK |
| homework | h-atoms part 1 numeric | 4 | 4 values 0 to 3; 8, 16 | OK |
| homework | h-atoms part 2 numeric | 6 | 3 paths x 2 = 6; 3, 12 | OK |
| homework | h-atoms part 3 choice | a | a only | OK, key 1.25 |
| homework | h-proj table | 16.6667, 35.7143, 23.8095 | 50/3, 250/7, 500/21 = 23.809524 (also 1000 - 976.19) | OK |
| homework | h-gains part 1 numeric | 2 | (0, 0, 2, 2, 0, 2), gain 2; 0, 4 | OK |
| homework | h-gains part 2 numeric | 12 | 6 x 2 = 12; 6, 2 | OK |
| homework | h-gains part 3 choice | a | a only | OK |
| homework | h-class multi | a, b | a, b only | OK |
| homework | h-mart multi | a, b, d | a, b, d; mean 1/3, variance 8/9, E[(1/2)^X] = 1; c drifts by 2S/3 | OK; Note 15 |
| homework | h-code | 9 tests | solution 9/9, example 1/1, starter 0/9; all nine pairs match a linear solve | OK; Warnings 9 and 10 |
| homework | h-wald order | w1 to w6, same w2/w3/w4 | proof valid; many valid orders rejected; v2 is valid; theorem needs identical distribution | Error 2, Error 3, Warning 8 |
| homework | h-long longform | 6 rubric points, 10 marks | 2 + 1 + 2 + 2 + 1 + 2 = 10; model correct | OK |

## Mismatches

Errors

1. **Error. `l10-condexp-projection.json` screens[10] (`Regression as a projection`), `wrong` `slope` (7.74) and `byKey.slope`.** The text says "You used a positive slope." With slope +0.54 through the means the line gives 6 + 0.54(92 - 100) = 1.68, and with intercept 60 it gives 60 + 0.54(92) = 109.68. Nothing gives 7.74 (it is 0.75 times the key). A learner who makes the slip is not told so, and a learner who types 7.74 gets feedback for a slip they did not make. Fix: set `value` to 1.68 (tol abs 0.01) and keep the text "You used a positive slope. The line falls from £12 to £1, so its slope is $-0.54$." The other two slips are right (6 is the mean, 12 the nearest path at 90).
2. **Error. `homework-3.json` items[6] `h-wald`, distractor `v2` ("Dominated convergence applies because $T \wedge n \le T$.") is a valid line.** The item assumes $E[T] < \infty$, so $T$ is an integrable dominator for $T \wedge n$ and $E[T \wedge n] \to E[T]$ by dominated convergence; the line could replace `w3`. The `why` says "You dominated the time" as if that were an error, so a learner who builds a correct proof with it is marked wrong. Fix: replace the text with a false line, "Dominated convergence applies to the sum because each $|X_k| \le 1$." and the `why` with "You assumed bounded steps. The $X_k$ need not be bounded; the dominating variable is $\sum_{k \le T}|X_k|$, with mean $E|X|\,E[T]$." Update `byKey.v2` to "You used a line that assumes bounded steps."
3. **Error. `homework-3.json` items[6] `h-wald`, the hypotheses are too weak for the proof.** The prose says "independent with mean $\mu$ and $E|X_k| < \infty$", but `w4` and the explanation use $E|X|\,E[T]$ for $E\sum_{k \le T}|X_k|$, which needs the $|X_k|$ to share one mean (or a common bound on $E|X_k|$). Independent, non-identical steps can break the identity: with $X_k = \pm 3^k$ fairly and $T$ the first $k$ with $X_k = +3^k$ (so $E[T] = 2$), $\sum_{k \le T} X_k$ has no mean. Fix: "Let $X_1, X_2, \dots$ be independent and identically distributed with mean $\mu$ and $E|X_1| < \infty$", and write $E|X_1|$ in `w4` and in the explanation if the author prefers one name for it.

Warnings

4. **Warning. `l13-stopping-times.json` screens[9] third cell ("Profit per share the backtest reports"): the key 0.5938 needs the buying price to count as a candidate for the best close.** "Sells each share at the best close of 4 days" reads as the maximum of the four closes $S_1, \dots, S_4$, whose mean is exactly 1 step, so £0.50 (all 16 paths enumerated: 19/16 less 3/16 for the three paths that stay below the start). The key $19/16 \times 0.50$ is $E[\max(S_0, \dots, S_4)]$. A careful learner answering £0.50 fails, and the hint and `byKey.r2c1` say 19/16. Fix: write "sells each share at the best price over the 4 days, counting the buying price, with fair £0.50 daily steps" in the prose, and "the best of the buying price and four closes" in the hint; nothing else changes.
5. **Warning. `l9-information.json` screens[9] and [10]: the lookback payoff is never defined.** Screen 9 says "pays on the running maximum, starting from $S_0$"; screen 10 then says it "takes the values £20 and £0". Those hold only for a fixed-strike call, $\max(M - 100, 0)$; the usual floating-strike payoff $M - S_2$ gives £24 and £4. Fix: in screen 9 write "A lookback call pays $\max(M - 100, 0)$, where $M$ is the running maximum, starting from $S_0$." (the keys 120 and 100 and screen 10's £20 and £0 then follow).
6. **Warning. `l10-condexp-projection.json` screens[6] (order, tower property): a valid alternative is marked wrong.** `t2` ($Z$ is $\mathcal H$-measurable) depends on none of `t3`, `t4`, `t5`; only `t6` needs it. So `t1, t3, t4, t5, t2, t6` and `t1, t3, t4, t2, t5, t6` are valid proofs, but the groups [t2, t3] and [t4, t5] accept `t2` only in slots 2 and 3. Fix: fold `t2` into `t1`, which already says "it is $\mathcal H$-measurable": make `t1` "We show that $Z$ is $E[Y \mid \mathcal H]$: it is $\mathcal H$-measurable, by the definition of $E[X \mid \mathcal H]$, and it matches $Y$ on every event of $\mathcal H$.", drop `t2`, and keep `same` [[t4, t5]]. The prose "Two lines are flawed" is unchanged; update the hints ("State the goal, take $A$, chain the two properties").
7. **Warning. `l13-stopping-times.json` screens[3] (order, bounded optional stopping): a valid alternative is marked wrong.** `o1` ($T \wedge N = T$, so $M_T = M_{T \wedge N}$) and `o2` ($E[M_{T \wedge N}] = E[M_0]$) are independent; `o3` needs both. So `o2, o1, o3` is valid. Fix: add `"same": [["o1", "o2"]]` and, in the prose, "Two lines may swap, and two lines are flawed." (screen 2 uses the same wording style).
8. **Warning. `homework-3.json` items[6] `h-wald` (order): most valid proof orders are marked wrong.** The real constraints are `w1` before `w2`, `w4` before `w5`, and `w6` last; `w3` can sit anywhere before `w6`. The key fixes `w1` first and `w5` fifth, with only [w2, w3, w4] interchangeable. Rejected valid orders include `w4, w5, w1, w2, w3, w6` and `w1, w4, w5, w2, w3, w6`. The `same` rule cannot express chains, so merge them: `W12` = "$Y_n = \sum_{k \le n}(X_k - \mu)$ is a martingale, since $X_{n+1} - \mu$ is independent of $\mathcal F_n$ with mean 0; so for the bounded stopping time $T \wedge n$, optional stopping gives $E[\sum_{k \le T \wedge n} X_k] = \mu\,E[T \wedge n]$"; `W3` = `w3`; `W45` = `w4` and `w5` joined ("... so dominated convergence gives ..."). Then `answer` is W12, W3, W45, w6 with `same` [[W12, W3, W45]]; the two flawed lines stay.
9. **Warning. `homework-3.json` items[5] `h-code`, `how`: "both are bounded up to the stop" is false for the second martingale.** $(q/p)^{S_n}$ is bounded by $\max((q/p)^N, 1)$ up to the stop, but $S_{T \wedge n} - (2p - 1)(T \wedge n)$ is not bounded. It is dominated by $N + T$, and $E[T] < \infty$ for a walk between two ends (shown by $E[T \wedge n] \le N^2$ for the fair walk, and the same holds for any $p$). Fix: "The first martingale is bounded up to the stop; the second is dominated by $N + T$, and $E[T]$ is finite between two ends."
10. **Warning. `homework-3.json` items[5] `h-code` repeats the lesson's walk numbers.** The visible example `exit_stats(3, 10, half)` is the `l13` answer (3/10 and 21), and the hidden test `exit_stats(4, 12, half)` is `l13` quiz `q-ruin` and `q-time` (1/3 and 32). DECISIONS "Fresh numbers in reviews and homework" bars this. Fix: example `exit_stats(2, 8, half)` expecting `(Fraction(1, 4), Fraction(12))`, and test 2 `exit_stats(5, 9, half)` expecting `(Fraction(5, 9), Fraction(20))` (both checked by a linear solve). The biased tests are fresh and stay; the `how` count of 9 is unchanged.
11. **Warning. `l13-stopping-times.json` screens[4] option `b` and `byKey.b`: "nothing to dominate it" overstates.** $T \wedge n \le T$, so $T$ dominates it as soon as $E[T] < \infty$; the point is that this integrability is what is being found, so using it here is circular. As the line stands a reader can object that $T$ is the dominator. Fix: `byKey.b` becomes "The only bound on $T \wedge n$ is $T$, and $E[T] < \infty$ is what we are finding. It increases to $T$, which is monotone convergence." and the `why` of `b` gets the same last sentence.

Notes

12. **Note. `l13-stopping-times.json` screens[6] canvas.** The walk is drawn for 200 steps with a cap, so the caption reads "282 of 300 paths hit" (18 are still below +1 at step 200) beside prose saying $S_T = 1$ always. Fix: add "Here 200 steps are drawn, so a few walks are still below 1." to the explanation, or raise `steps` to 600.
13. **Note. `l13-stopping-times.json` screens[8] console.** It shows `stopped_mean(10, hit2)` as `0`; the solution returns `Fraction(0, 1)`, which the console elsewhere prints with its `repr`. Fix: show `Fraction(0, 1)`.
14. **Note. Review and homework items that echo a lesson's setup.** `review-3` `r-event` asks for "the first two tosses differ", the complement of the keyed indicator in `l9` s4; `r-doob` uses chance 0.7, the real chance of `l12` s8; `r-stop` repeats the 5-above-start and last-day-above-start rules of `l13` s1 and `q-which`; `h-wald` totals 21, the answer of `l13` s5. None repeats a keyed answer exactly. Fix if wanted: `r-event` key "The first two tosses are both heads" (the atom HH, in $\mathcal F_2$; options b to d stay false), `r-doob` chance 0.8 (key 1 + 2(0.8) = 2.6, `mean` 2.4, `fair` 2), `r-stop` thresholds $\pm 4$.
15. **Note. Multi items whose distractors are visibly shorter than the keys.** `homework-3` `h-mart` (keys 48, 25 and 12 characters against the one distractor of 11), `l11` s1 (keys up to 41 against distractors of 24 and 25), `l11` s6 (keys up to 60 against 36), `l9` s1 (key 42 against 19 and 18). Choice items are within the 1.5 limit: worst `review-3` `r-cube` 1.36 (15 against 11 characters), `l13` s4 1.33, `l13` quiz `q-which` 1.19, `l13` quiz `q-fixed` 1.26. Fix if wanted: lengthen the single `h-mart` distractor to "$S_n^2 - n$, the fair-walk square" or shorten the keys.
16. **Note. `l13-stopping-times.json` screens[6] and quiz.** `l13` s6 explanation ("Add a floor, or cap the time, and the theorem applies again") is right for a floor at any finite level, but a floor alone gives $E[S_T] = 0$ with $P(\text{hit } 1) < 1$, so $S_T = 1$ no longer holds. Fix: "Add a floor, and the walk may stop at the floor instead; cap the time, and $E[S_{T \wedge N}] = 0$."
17. **Note. `l9-information.json` quiz `q-s4` `wrong` id `sixtyfour` holds 65536.** The value is $2^{16}$, the id says 64. The id is never shown. Fix: rename to `paths16`.

## Checks with nothing found

- Every numeric `wrong` band lies outside its answer band and outside every other wrong band; table byKey ids match their rows and columns in all tables (zero-based) and grid ids in `l9` s0 match the one-based grid.
- No choice item has two correct options; every distractor in every choice and multi widget has a `why`; each multi has exactly its true statements. In `l11` s6 the true statements are the three keyed; in `l13` s1 the four first-time and fixed-time rules.
- Order keys: `l10` s6, `l12` s2, `l12` s3 and `l13` s2 are valid; their distractor lines (`d1`, `d2`, `a`-prefixed, `e1`, `e2`, `x1`, `y1`, `y2`, `v1`) are false as their `why` texts say. Alternatives found are items 6, 7 and 8.
- Theorem statements: tower property (chain through $E[X\mathbf 1_A]$, $A \in \mathcal H \subset \mathcal G$), taking out what is known (bounded $\mathcal G$-measurable factor), the martingale transform (bounded predictable $H$), the stopped martingale (predictable $H_k = \mathbf 1_{T \ge k}$ against the flawed $\mathbf 1_{T > k}$), bounded optional stopping, the optional stopping extension (finite almost surely plus $|S_{T \wedge n}| \le 10$, monotone for $E[T \wedge n]$, dominated for $E[S^2_{T \wedge n}]$), the failure at $+1$ (infinite mean of the running depth, `E[T]` infinite), the look-ahead trap (a last visit and a highest point are not stopping times; $E[M] = 1067/512$), Wald's identity (item 3), and the Doob martingale (integrable `X`).
- Canvas data: the 8 outcome grids (counts, `S_2`, `S_3`, shaded atoms), the two-step lookback tree, the 1, 2, 4, 8 collapse frames, the 7 Doob values on the tree, the 11 bars of the maximum and the `series` lines (0 to 10, and zeros) are all right.
- All six code items: each solution passes all its tests and examples; each starter fails every test and example (0 of 61 hidden tests, 0 of 11 examples). Stated counts in `how` and `feedback.correct` (11, 10, 10, 10, 10, 9) match.
- No literal backslash-n in any prose field (the hits are `\ne`); no exclamation marks; no em-dashes or en-dashes; no explanation over three sentences; no sentence over 20 words by a rough count.
- Fresh numbers: `r-die`, `r-tower`, `r-pred`, `r-gain`, `r-cube`, `r-ruin`, `r-agree`, `h-atoms`, `h-proj`, `h-gains`, `h-class` and `h-mart` share no number or answer with a lesson. The repeats are items 10 and 14.
- Longform rubric (`h-long`): six points of 2, 1, 2, 2, 1 and 2 make 10; each is checkable; the model answer is correct in all three parts (the walk bound $E[T \wedge n] \le N^2 - k^2$, $E[T] = k(N - k)$, the failure and the remedy).
- Markov level 5 numbers, recomputed independently: 3/10, `E[T]` = 21, 0.0852 and 0.0000458 (see Method).

## Fix pass

Every number below was recomputed before it was written: the slip 6 + 0.54(92 - 100) = 1.68 and 60 + 0.54(92) = 109.68; exit chance and `E[T]` for (2, 8) = 1/4 and 12, and (5, 9) = 5/9 and 20, by the closed form and by an exact Gaussian solve of the linear system; the die until a 5 or 6, `E[T]` = 3, total 3 x 3.5 = 10.5 and V = 3.5 + (4/6)V = 10.5; and the chance-0.8 Doob values 1 + 2(0.8) = 2.6, 0.8(2.6) + 0.2(1.6) = 2.4. Validator 0 errors. Playthrough (default, and `--mobile --tablet`) green for l9, l10, l11, l13, review-3 and homework-3 with the local CDN; screenshots of l10 s6, l13 s9 and homework item 7 read at 440 wide. `h-code` solution passes 10 of 10 (9 tests plus the example) and the starter 0 of 10. Voice scan 0 sentences over 20 words and 0 explanations over three sentences.

1. Fixed. `slope` wrong value is now 1.68 (tol abs 0.01); the feedback text "positive slope" was already right for it.
2. Fixed. `v2` is now "Dominated convergence applies to the sum because each $|X_k| \le 1$." with the reviewer's `why`, and `byKey.v2` names the bounded-steps line.
3. Fixed. Prose now says independent and identically distributed, with the filtration $\sigma(X_1, \dots, X_n)$; `w4` and the explanation use $E|X_1|$.
4. Fixed. Prose says "best price over 4 days, counting the buying price"; the hint says "the best of the buying price and four closes"; feedback and explanation say "best price". Key 0.5938 unchanged. The line "Daily steps are fair, £0.50." was split off for sentence length.
5. Fixed. Screen 9 prose defines the call payoff $\max(M - 100, 0)$ with $M$ the running maximum from $S_0$.
6. Fixed as the review proposes: `t2` folded into `t1`, `t2` removed, answer t1, t3, t4, t5, t6, `same` [[t4, t5]], hint updated.
7. Fixed. `same` [[o1, o2]] added and the prose reads "Two lines may swap, and two lines are flawed."
8. Fixed. Lines merged and renamed within the item only: `w1` now carries the old `w1` and `w2`, `w4` the old `w4` and `w5`; `w2` and `w5` removed. Answer w1, w3, w4, w6 with `same` [[w1, w3, w4]]. Exactly the valid orders are accepted: `w6` last, the three blocks in any order, each block internally in its proven order.
9. Fixed. `how` now says the first martingale is bounded up to the stop, the second is dominated by $N + T$, and $E[T]$ is finite between two ends.
10. Fixed, and wider than the review: the visible example and hidden test 1 both repeated the `l13` answer (3/10, 21), so both now use `exit_stats(2, 8, half)` = (1/4, 12); hidden test 2 is `exit_stats(5, 9, half)` = (5/9, 20). Biased tests unchanged; count stays 9 hidden tests.
11. Fixed. `byKey.b` and the `why` of `b` now say the only bound on $T \wedge n$ is $T$, and $E[T] < \infty$ is what is being found.
12. Fixed. Prose now says the picture draws 200 steps so a few walks are still below 1 (the caption "282 of 300" is canvas-generated).
13. Fixed. Console shows `Fraction(0, 1)`.
14. Fixed, all three. `r-event` key is "The first two tosses are both heads" (atom HH, options b to d unchanged and still false); `r-doob` chance 0.8, key 2.6, `mean` slip 2.4, `fair` 2, `all` 3; `r-stop` thresholds $\pm 4$, and option `d` now uses "below its start" (still a look-ahead rule). `h-wald` die changed to "until the first 5 or 6", total 10.5, so it no longer totals 21.
15. Fixed, wider than the review, by lengthening distractors and shortening one key; no key changed. `h-mart` option c is "$S_n^2 - n$, the fair-walk square"; `l9` s1 key is "Something happens: all of $\Omega$" and its distractors are lengthened; `l11` s1 distractors and the `l11` s6 false statement are lengthened. Choice-item ratios were already within 1.5.
16. Fixed. `l13` s6 explanation now reads "Add a floor, and the walk may stop at the floor instead; cap the time, and $E[S_{T \wedge N}] = 0$." (`h-long` part 3 model answer has the same loose phrase "either restores $E[S_T] = 0$"; it reads correctly as the stopped mean and is left, not a finding.)
17. Fixed. `wrong` id `sixtyfour` renamed `paths16` in the `wrong` list and in `byKey`.

Counts: 17 findings, 17 fixed, 0 disputed, 0 deferred.

Changed keys (file, widget id; key, tolerance, options, numbers, order groups or `wrong` values changed):
- `l9-information` s1 multi: option texts (keys a, d unchanged).
- `l9-information` `q-s4` numeric: `wrong` id `sixtyfour` to `paths16` (value 65536 unchanged).
- `l10-condexp-projection` s6 order: lines, answer (t2 removed) and `same`.
- `l10-condexp-projection` s10 numeric: `wrong` `slope` 7.74 to 1.68.
- `l11-filtrations` s1 multi: distractor texts. s6 multi: distractor text.
- `l13-stopping-times` s3 order: `same` added. s4 choice: option `b` `why`.
- `review-3` `r-event` choice: key text. `r-doob` numeric: answer 2.4 to 2.6, accept, `wrong` `mean` 2.1 to 2.4. `r-stop` multi: option texts (thresholds, option d).
- `homework-3` `h-mart` multi: option c text. `h-code` code: example and hidden tests 1 and 2 (numbers). `h-wald` order: lines, answer, `same`, distractor `v2`.

## Recheck

Commit 32cd2a8 confirmed in `git log`. Each value recomputed by hand and by script (`rc-mp3/chk.py`: exact linear solve of the walk equations, CPython). Homework playthrough with the local CDN green (12 items, 8 of 8 right, 38 of 38 marks), so the `h-code` solution also passes in Pyodide.

- `l9` s1 multi: keys a (first toss H) and d (all of Omega) decided, b and c undecided; meaning kept, no distractor correct, keys now shorter than b and c. OK.
- `l9` `q-s4` `paths16`: id rename only, value 65536 = 2^16 unchanged, `byKey` renamed in step. OK.
- `l10` s6 order: t1, t3, t4, t5, t6 with `same` [[t4, t5]]. t4 and t5 both need only A and the defining properties, so either order is valid; no other swap is. d1 and d2 truly invalid. OK.
- `l10` s10 `slope`: 6 + 0.54(92 - 100) = 1.68, which is the positive-slope slip; distinct from 6, 12 and the key 10.32 (slope -135/250 = -0.54). OK.
- `l11` s1 and s6 options: d and e (s1) still not adapted, d (s6) still false; meaning kept, keys not longer. OK.
- `l13` s3 order: o1 and o2 can swap (o2 stands alone as a statement about T and N), o3 must be last; y1 and y2 invalid. OK.
- `l13` s4 option b `why`: matches the `byKey` b text, key a unchanged. OK.
- `review-3` `r-event`: key "first two tosses are both heads" = atom HH in F_2; b, c, d each split an atom (HTT/HTH, HHH/HHT, third toss). OK.
- `review-3` `r-doob`: M_1 = 1 + 2(0.8) = 2.6 (key). `mean` 2.4 = 3(0.8) = M_0 matches its text; `fair` 1 + 2(0.5) = 2; `all` 3. Check 0.8(2.6) + 0.2(1.6) = 2.4. All four distinct. OK.
- `review-3` `r-stop`: a (+4 or -4) and b are stopping times; c (day before) and d (last day below start) look ahead; keys shorter than c and d. OK.
- `homework-3` `h-mart`: c drifts, E[S_{n+1}^2 - (n+1) | F_n] = S_n^2 - n + 2S_n/3, so not a martingale; a, b (variance 1 - 1/9 = 8/9) and d (2/3 * 1/2 + 1/3 * 2 = 1) are. OK.
- `homework-3` `h-code`: (2, 8, 1/2) = (1/4, 12) and (5, 9, 1/2) = (5/9, 20) by closed form and by exact Gaussian solve; all 9 tests plus the example match the independent solve; solution passes 10 of 10, starter passes 0 of 10 in CPython; app playthrough green. OK.
- `homework-3` `h-wald` order: answer w1, w3, w4, w6 with `same` [[w1, w3, w4]]; each of w1, w3, w4 is self-contained, w6 needs all three, so exactly the six orders with w6 last are valid and the engine accepts exactly those (it permutes places within a group). v1 (optional stopping on an unbounded T) and v2 (assumes |X_k| <= 1) are invalid. Prose states i.i.d., the filtration and E[T] < infinity. OK.
- `homework-3` `h-wald` die: until a 5 or 6, p = 1/3, E[T] = 3, total 3 x 3.5 = 10.5; V = 3.5 + (2/3)V gives 10.5. OK.
- Fresh numbers: 2.6, 1.68, 10.5, (2, 8), (5, 9) and chance 0.8 appear in no other measure-prob lesson (the 3/10 and 21 of `l13` are not reused). The 1/4 exit chance for (2, 8) also appears as an unrelated stop-and-target chance in `l13` s? (3/4 and 1/4); different context, not a repeat of a stated problem.

New mismatches: none.
