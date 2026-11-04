# Answer check, topic 3.2 ito level 2 (4 November 2026)

Independent recomputation of every keyed answer, stated number, feedback value, code test and rubric point in `app/content/courses/ito/` `l5-integrating-noise.json`, `l6-ito-lemma.json`, `l7-solving-gbm.json`, `l8-fair-games.json`, `review-2.json` and `homework-2.json`. Each value was worked from the question text and the engine source; the file explanations and `docs/reports/ito-2.md` were used only as the thing to compare against (the report was read for the lesson 4 cross-reference only). Scripts are in the scratchpad folder `ac-ito2` (`/tmp/claude-0/-home-user-zero-to-quant/5858d7c4-7372-5116-9f86-cb52e41f112f/scratchpad/ac-ito2/`):

- `l5.py`, `l6.py`, `l7.py`, `misc.py`, `chk4.py`, `fixvals.py`: CPython with NumPy, SciPy and SymPy (the sandbox lacked them, installed to `pylib`). They rebuild the seed-3 reference path and the seed-4 GBM year from the stated seeds, reproduce every caption number and every hidden code test (solutions copied verbatim), and recompute every closed form (Itô drifts by SymPy, moments, Φ values, barrier odds, forward) with `math` and `scipy.stats.norm`.
- `scan.py`: for every numeric field, whether a wrong value lies inside the answer's tolerance or another wrong value's, and whether each `byKey` key names a `wrong` id or option; for every choice and multi, the correct count and option lengths; for every order, that `answer` plus `distractors` equal the line ids.
- `expr.mjs`: the real `app/js/engine/grade.js` `exprEqual` with the Compute Engine, run on 18 forms of the l6 key and 12 forms of the homework key.
- `walk.mjs`: the engine's own seeded `walk` generator (mulberry32 and Box-Muller, copied from `sim.js` and `walk.js`) for the three walk canvases that carry a claim.

**Summary.** All 79 widgets recompute: 48 numeric fields (124 wrong values), 12 choice, 1 multi, 5 order, 2 expression, 1 table (8 cells), 1 drag-point, 8 code items (50 hidden tests) and 1 longform rubric. No keyed answer is wrong. Every choice and multi has exactly the keyed correct options and no distractor is also correct. Every code solution passes all its tests and examples, and every starter fails every test (each starter returns `None` or `[]`). Every seeded number reproduces: reference path sums at 4, 16, 64, 256 and 4,096 steps (l5), `W_1 = 0.9996243` and `S_1 = 129.683264`, Euler 129.690755 and the gaps 0.8196, 0.7520, 0.1109, 0.0075 (l7), the seed-6 simulation 12,210.23 with standard error 16.10 (l6), the euler_error sets 0.1533, 0.0744, 0.0391 and 0.32, 0.16, 0.0784 (l7), and the seed-3 martingale changes 0.9981, -0.0019, 0.6480, -0.0005, 0.0032 (l8). No wrong value falls inside any answer's tolerance, no two wrong values overlap, and no `byKey` key names nothing. There is 1 error, 7 warnings and 10 notes. The error is an l7 `wrong` value that no natural slip produces, and the next warning is a second l7 feedback line that misnames its slip. No key changes.

## Mismatches

1. **Error.** `l7-solving-gbm.json` `screens[4]` (P(S_1 > 130)), `wrong` id `plain`, value 0.1087, and its `byKey` line. The feedback says "You used the drift 0.08 in the mean of ln S_1". That slip gives z = (0.262364 - 0.08)/0.2 = 0.9118 and P = 0.1809. No natural slip reproduces 0.1087 (it needs z = 1.2335, an implied mean of 0.0157; I searched means 0 to 0.12, sigmas 0.04 to 0.28 and the three bases ln 1.3, ln(130/108.33), ln(130/110.52)). A learner who makes the stated slip types 0.1809 and gets only the generic line. Fix: set `value` to 0.1809 with `tol` `{ "abs": 0.0005 }`; the other wrong values (0.8442, 0.0668) stay clear of it.
2. **Warning.** `l7-solving-gbm.json` `screens[3]` (z-score of ln 130), `wrong` id `plain`, value 1.3118. The feedback says "You used the drift 0.08, not 0.06". With 0.08 the z-score is (0.262364 - 0.08)/0.2 = 0.9118. The value 1.3118 is ln 1.3 / 0.2, which uses no drift at all (centre at £100, the median of the path at W = 0). Fix: either set `value` to 0.9118 (matches the text), or keep 1.3118 and write "You left the drift out of the mean of ln S_1: ln 1.3 / 0.2 centres the curve at £100." The explanation line is unaffected.
3. **Warning.** `l8-fair-games.json` `screens[2]` (table), cell `r3c1` (answer 3.6945, `tol` abs 0.001). The question names no precision for this column. A learner who computes $\tfrac12e^2 = 3.69$ or 3.7 is marked wrong (3.69 is 0.0045 outside; the accepted range is 3.6935 to 3.6955). Fix: add "Give the last row to 4 decimal places" to the prose, or use `"tol": { "abs": 0.005 }` (3.69 then passes, 3.7 does not, which is also sensible), and say "3.69" in the `accept` line.
4. **Warning.** `homework-2.json` `items[0]` (`ito_vs_strat`) reuses the level's own numbers (DECISIONS "Fresh numbers in reviews and homework"). Test 1 and the example are seed 3 at n = 16, 256, 4,096, whose rows are -0.148729, -0.339218, -0.355507, mid 0.146693, mid minus left 0.5022 and squared sum 1.0044: the values lesson 5 states in its caption, screens and code tests. Test 2 (seed 5, 1,000 steps: left -0.492121, mid 0.001737) is lesson 5's own hidden test path. Fix: use a new seed and grid, for example seed 11 with `ns = [8, 64, 512]`, which gives `[[0.039673, 0.229561, 0.189888, 0.379776], [-0.09729, 0.229561, 0.326851, 0.653702], [-0.235422, 0.229561, 0.464983, 0.929965]]` (my values from the solution), and seed 12 for test 2 (recompute); update the example, `explain` and `how`. The identity test (`mid - left = half the squared sum`) can stay at any seed.
5. **Warning.** `homework-2.json` `items[1]` (`apply_ito`): tests 1 and 2 and the example are the lesson's own cases: $S^2$ at £100 with $\mu = 0.08$, $\sigma = 0.2$ giving 2000 (lesson 6 screen 4 and its code example `ito_drift(0, 200, 2, 8, 20)`), and $\ln S$ giving 0.06 and 0.2 (lesson 6 screen 6). The `explain` repeats both. Fix: change the GBM parameters, for example $S^2$ with $\mu = 0.05$, $\sigma = 0.3$ at $(0, 50)$ giving `[475.0, 1500.0]` (and a second point, say $(1, 40)$ giving `[304.0, 960.0]`), and $\ln S$ giving `[0.005, 0.3]` at every price. Tests 3 to 5 are fresh.
6. **Warning.** Choice key visibly longer than its distractors (the correct text is about 1.5 times the longest wrong one, so length gives it away): `l5-integrating-noise.json` `screens[5]` (116 characters against 80, 69, 57), `l7-solving-gbm.json` `screens[6]` (117 against 72, 67, 57) and `l8-fair-games.json` `screens[8]` (107 against 81, 75, 59). Fix: shorten each key or lengthen the distractors to within about 20%. Suggested: l5 key "It is the midpoint sum, which looks ahead: the left sum is lower by about $\tfrac12$" (82); l7 key "The squared noise terms sum to about $\sigma^2T$, which supplies $-\tfrac12\sigma^2T$" (83); l8 key "A martingale fixes the forecast, not the path; single paths can rise" (68).
7. **Warning.** `l8-fair-games.json` `quiz[3]` (stop at +£4 or -£1), `wrong` id `quarter`, `byKey` line: "$\tfrac14$ is $1/4$." names no slip. The value 0.25 is near over far (1/4). Fix: "$\tfrac14$ is the near distance over the far one, 1 over 4. Divide by the total distance, 5: $p = 1/5$." (`screens[7]` `ratio` is worded correctly.)
8. **Warning.** `l6-ito-lemma.json` `screens[7]` (the 0.0199 gap) gives the learner no $\sigma$, $\mu$ or $T$: the prose says only "our seeded GBM year". The key (0.02) needs $\sigma = 20\%$, $T = 1$, which the options reveal ("$\sigma^2T = 0.04$"). Fix: add "($\sigma = 20\%$, $T = 1$)" to the prose so the question can be answered before the options are read.
9. **Note.** `l5-integrating-noise.json` `screens[0]`: the `accept` and `explain` lines say the products 0, 0.2675, -0.2745, -0.1782 "add to -0.1853". Those rounded figures add to -0.1852 (the unrounded products add to -0.185297; from the table's own four-place inputs the sum is -0.18523). The tolerance 0.0005 accepts both. Fix: "which add to -0.1853 (-0.1852 from the rounded products)", or show the products to five places.
10. **Note.** `l6-ito-lemma.json` `screens[7]` `explain` ("Our path gives $0.2799 - 0.2599 = 0.0199$") and `homework-2.json` `items[7]` rubric point 3: the displayed numbers subtract to 0.0200. The true gap, 0.019935 (seed 4, 252 returns; 0.2798601 and 0.2599249), rounds to 0.0199. Fix: "$0.27986 - 0.25992 = 0.0199$" in both, or "a gap of about 0.02 (0.0199 unrounded)". Rubric point 3 should accept 0.0199 or 0.02.
11. **Note.** `l5-integrating-noise.json` `screens[2]` `feedback.generic`: "on every fourth quarter-step grid the left sum is -0.185297" is garbled. The example is `ito_sum(W[::1024])`, the four-step grid. Fix: "Check the example: on the four-step grid `W[::1024]` the left sum is -0.185297."
12. **Note.** `l5-integrating-noise.json` `screens[9]` `how` says each test lands "within 0.04 of the exact second moment", but tests 1 to 3 expect 0.5 while the exact values are 0.495 ($n = 100$), 0.49 ($n = 50$) and 0.4975 ($n = 200$); only test 4 uses its exact 0.45. All pass (my seeded results 0.4788, 0.4851, 0.4835, 0.4404; the midpoint answer 0.75 and a mean of the sums fail). Fix: expect 0.495, 0.49 and 0.4975 (keep tol 0.04), or reword `how` to "within 0.04 of 0.5".
13. **Note.** `l8-fair-games.json` `screens[7]` prose ("the stopping time is bounded in practice") and `explain` ("No stopping rule, however clever, turns a fair game into a favourable one"). The first is not true (the game can last any number of rounds) and the second is false for unbounded rules (doubling strategies win a fixed sum with probability 1 at the cost of unbounded exposure). The key 0.3 is right because the stopped bankroll stays within -£3 and +£7. The lesson summary correctly says "bounded". Fix: prose "The bankroll is a martingale and the stopped bankroll stays between -£3 and +£7, so the final bankroll has mean equal to the start"; explain "No bounded stopping rule ...".
14. **Note.** `l6-ito-lemma.json` `screens[2]` (derivation order): `same` is `[["e2","e3"]]`, and the prompt says "the two middle lines may swap". Logically e2 (the first-order substitution) is independent of e3 and e4 and may sit anywhere between e1 and e5, so e1, e3, e4, e2, e5 is a valid derivation that the grader marks wrong. Fix: say "Lines 2 and 3 may swap" in the prompt (the key is then exact), or give `same` the group `["e2","e3","e4"]` only if e4 stays after e3 (it cannot, so prefer the reworded prompt).
15. **Note.** `l6-ito-lemma.json` `screens[4]` `feedback.correct`: "matching the lognormal moment $e^{2m + 2s^2}$ from lesson 4 of level 1". Lesson 4 gives the mean $e^{m + v/2}$ and the normal moment generating function $e^{\sigma^2t/2}$, not the second moment, and `review-1.json` `r-gbm-var` reaches 12,214.03 only inside a variance. Fix: "matching the lognormal moment $e^{km + k^2s^2/2}$ at $k = 2$, from the moment generating function of level 1". This is also a recall note: 12,214.03 is the answer of lesson 6 screen 4 and the first term of `review-1` `r-gbm-var`.
16. **Note.** `review-2.json` `items[6]` (P(S_1 < 80)) uses the lesson 7 share ($S_0 = £100$, $\mu = 8\%$, $\sigma = 20\%$) with a new threshold, and `homework-2.json` `items[4]` keys $e^{2W_t - 2t}$, the same martingale as the correct option of `review-2` `items[7]`. The answers differ from every lesson answer (0.0784 against 0.1558), so this passes the "fresh numbers" rule; the second is a repeat between review and homework. Fix if wanted: use $e^{3W_t - 4.5t}$ in the homework multi (the wrong forms follow by changing the correction), or $\mu = 6\%$ and $\sigma = 25\%$ in `r-prob-low`.
17. **Note.** Grader gap P32-expr-exp (recorded once): a typed `\exp(w)` form of the l6 `screens[6]` key is rejected. I ran 18 forms through the real `exprEqual`: `\frac{e^w}{2}`, `e^w/2`, `0.5e^w`, `\frac12 e^w`, `e^w\cdot\frac12` and `\frac{1}{2e^{-w}}` pass; `\frac12\exp(w)`, `\exp(w)/2` and `\frac12\exp\left(w\right)` fail; `e^w`, `0` and `\frac12e^x` fail as intended. The homework `\mu - r` key accepts `\mu-r`, `-r+\mu`, `(\mu-r)`, `-(r-\mu)` and `\left(\mu-r\right)`, and rejects `\mu+r`, `\mu`, `r-\mu`; the text form `mu-r` is covered by `accept`.
18. **Note.** Sample-based grading margins that pass but are thin: `l7` `screens[9]` test 3 asks for a ratio between 3.4 and 4.6 and the seed-3 ratio is 3.895; `l8` `screens[9]` last test asks for $|\bar{W^3}| < 0.04$ and the seed-3 value is 0.0032 (about 3.3 standard errors of slack); `l6` `screens[9]` last test passes with $|\text{sim} - \text{formula}| = 0.05$ standard errors on seed 3. None is a defect.

## Items checked

My value is the one I computed; "ok" means the key, every wrong value and the quoted explanation numbers reproduce, and the number is the same to the stated precision.

| File | Screen or item | Key | My value | Verdict |
|---|---|---|---|---|
| l5 | screens[0] | -0.1853 (wrong 0.4787, 0.1467, 0.7202) | -0.185297 (rounded table: -0.18523; right 0.47867, mid 0.14672, abs 0.72020) | ok, note 9 |
| l5 | screens[1] | choice `gap` | caption sums at m = 4, 16, 64, 256, 4,096: left -0.1853, -0.1487, -0.2967, -0.3392, -0.3555; mid 0.1467; right 0.4787, 0.4421, 0.5901, 0.6326, 0.6489 | ok |
| l5 | screens[2] | code, 8 tests | -0.355507, 0.146693, 0.648893, -0.185297, 0.442115, [-0.5, 0.125, 0.75], -0.492121, [0.001737, 0.495595] | ok, starter fails, note 11 |
| l5 | screens[3] | order c1 to c5, drop x1, x2 | derivation sound | ok |
| l5 | screens[4] | -0.3533 (wrong 0.1467, -0.3555, -0.7066) | -0.353307; 0.5 x 1.0044 - 0.5 check 0.0022 | ok |
| l5 | screens[5] | choice `gap` | gap 0.5022 (about 0.5) | ok, note on length (warning 6) |
| l5 | screens[6] | choice `half` | means 0 and 0.5 | ok |
| l5 | screens[7] | 0.5 (wrong 0.3333, 1, 0.25) | 0.5 | ok |
| l5 | screens[8] | 0.3333 (wrong 0.5, 0.5774, 0.25) | 0.333333; sd 0.57735 | ok |
| l5 | screens[9] | code, 4 tests | 0.4788 (se 0.0124), 0.4851, 0.4835, 0.4404 against 0.495, 0.49, 0.4975, 0.45 | ok, starter fails, note 12 |
| l5 | screens[10] | 0.5022 (wrong 1.0044, 0.5, 0.0022) | 0.5022; 1.0044; 0.0022 | ok |
| l5 | quiz[0] | -1 (wrong 5, 2) | -1; 5; 2 | ok |
| l5 | quiz[1] | 0.98 (wrong -0.02, 1.96) | 0.98; -0.02; 1.96 | ok |
| l5 | quiz[2] | 2 (wrong 1, 4, 0.5) | 2 | ok |
| l5 | quiz[3] | 36 (wrong 6, 9, 12) | 36 | ok |
| l6 | screens[0] | 1.0044 (wrong 0.2934, 0.711, 0) | 0.2934 + 0.7110 = 1.0044 | ok |
| l6 | screens[1] | choice `add` | end values 0.293, -0.711, 0.289 | ok |
| l6 | screens[2] | order e1 to e5 (same e2, e3) | lemma derivation sound | ok, note 14 |
| l6 | screens[3] | 2000 (wrong 1600, 400, 1800) | 1600 + 400 = 2000 | ok |
| l6 | screens[4] | 12214.03 (wrong 11735.11, 10408.11) | 12214.0276; 11735.1087; 10408.1077; lognormal route 12214.0276 | ok, note 15 |
| l6 | screens[5] | 0.06 (wrong 0.08, 0.04, 0.1) | 0.06 | ok |
| l6 | screens[6] | expression `\frac{1}{2}e^{w}` | SymPy: dt coefficient e^w / 2 | ok, note 17 |
| l6 | screens[7] | choice `half` (0.02) | gap 0.019935 (seed 4); sum 0.27986, ln 0.25992; canvas arrays agree | ok, warning 8, note 10 |
| l6 | screens[8] | choice `lin` | f_xx 0, 2, -1/S^2, -S^(-3/2)/4 | ok |
| l6 | screens[9] | code, 8 tests | 2000, 0.06, 6, 11.5, 12214.0276, 12210.23, 16.10, True (seed 3: 4464.35 against 4465.10, se 14.44) | ok, starter fails |
| l6 | screens[10] | 0.0149 (wrong 3.7524, 0.0298, 0) | Gamma 0.01876202; 3.7524; 0.014890; 0.029780 | ok |
| l6 | quiz[0] | 24 (wrong 0, 48, 32) | 6 w^2 = 24; E W^4 = 3 t^2 | ok |
| l6 | quiz[1] | 0.055 (wrong 0.1, 0.01) | 0.055 | ok |
| l6 | quiz[2] | 4465.1 (wrong 3729.6) | 4465.096; 3729.562 | ok |
| l6 | quiz[3] | 4 (wrong 1, 0) | 4 | ok |
| l7 | screens[0] | 129.68 (wrong 132.3, 106.18, 108.33) | 129.6833; 132.3030; 106.1837; 108.3287 | ok |
| l7 | screens[1] | choice `close` | Euler 130.50, 130.44, 129.79, 129.69; gaps 0.8196, 0.7520, 0.1109, 0.0075; guess gap 2.6198 | ok |
| l7 | screens[2] | order g1 to g5, drop x1, x2 | sound | ok |
| l7 | screens[3] | 1.0118 (wrong 1.3118, 1.5, 5.0591) | 1.011821; 1.311821; 1.5; 5.059107 | ok for key; wrong `plain` feedback mismatched, warning 2 |
| l7 | screens[4] | 0.1558 (wrong 0.8442, 0.1087, 0.0668) | 0.155812; 0.844188; 0.066807; the stated slip gives 0.1809 | ok for key; `plain` error 1 |
| l7 | screens[5] | 0.0202 as % (wrong 0.0408, 0, 0.2) | e^0.02 - 1 = 0.020201; e^0.04 - 1 = 0.040811; 110.517 against 108.329 | ok |
| l7 | screens[6] | choice `qv` | ln(1+y) expansion | ok, warning 6 |
| l7 | screens[7] | 0.0433 (wrong 0.04, 0.09, 0.01) | 13/300 = 0.043333; sd 0.208167 | ok |
| l7 | screens[8] | code, 8 tests | 129.683264, 129.690755, [100, 99.2106, 99.0237], [100, 99.2058, 99.0112], 253, [100, 102.5, 105.0625], [100, 102.5315, 105.1271], 59.5623 | ok, starter fails |
| l7 | screens[9] | code, 4 tests | [0.1533, 0.0744, 0.0391], [0.32, 0.16, 0.0784], ratio 3.895, 2 | ok, starter fails (returns []) |
| l7 | screens[10] | 0.0359 (wrong 0.018, 0.9641, 0) | Phi(-1.8) = 0.035930 | ok |
| l7 | quiz[0] | 0.11 (wrong 0.2, 0.02) | 0.11 | ok |
| l7 | quiz[1] | 0.4243 (wrong 0.6, 0.18) | 0.424264 | ok |
| l7 | quiz[2] | 61.38 (wrong 64.2) | 61.3763; 64.2013 | ok |
| l7 | quiz[3] | 0.0942 as % (wrong 0.1972, 0.09) | 0.094174; 0.197217 | ok |
| l8 | screens[0] | drag-point (1, 0.8), tol 0.2 and 0.12 | E[W_1 given W_0.5 = 0.8] = 0.8; zero and trend regions (y -0.2 to 0.2; 1.4 to 1.9, trend 1.6) clear of the target | ok |
| l8 | screens[1] | choice `zero` | flat only at mu = 0; seed-8 mean path rises with mu = 0.005 (0.33 at step 100) | ok |
| l8 | screens[2] | table: 1, 6, 0, 3.6945; no, no, yes, no | SymPy drifts 1, 6 (at w = 2), 0, 3.694528; byKey r0c1 to r3c2 all name editable cells | ok, warning 3 |
| l8 | screens[3] | order m1 to m5, drop x1, x2 | f_t = -theta^2 f / 2, f_x, f_xx; dZ = theta Z dW | ok |
| l8 | screens[4] | 1.284 (wrong 1, 1.1331, 1.6487) | 1.284025; 1.133148; 1.648721 | ok |
| l8 | screens[5] | 2.5 (wrong 1, 0, 1.5) | 2.5 | ok |
| l8 | screens[6] | 3.0 (wrong 8, 5, 13) | 3 | ok |
| l8 | screens[7] | 0.3 (wrong 0.7, 0.5, 0.4286) | 0.3; 3/7 = 0.428571; seed-5 coin walk: 11 of 40 hit +7 | ok, note 13 |
| l8 | screens[8] | choice `avg` | seed-21 bold path ends at 1.86, mean end 0.13 | ok, warning 6 |
| l8 | screens[9] | code, 8 tests | 0.9981, -0.0019, 0.6480, -0.0005, 0.9977, 1.0009, True, True (W3 0.0032) | ok, starter fails |
| l8 | screens[10] | 105.13 (wrong 108.33, 100, 105) | 105.1271; 108.3287 | ok |
| l8 | quiz[0] | -3 (wrong -4, 1, 0) | -3 | ok |
| l8 | quiz[1] | 6 (wrong 4, 2, 3) | 6 | ok |
| l8 | quiz[2] | 2.7183 (wrong 1.6487, 1) | 2.718282; 1.648721 | ok |
| l8 | quiz[3] | 0.2 (wrong 0.8, 0.5, 0.25) | 0.2 | ok, warning 7 |
| review-2 | items[0] r-left-sum | -0.25 (wrong 1.25, 0.5) | -0.25; right 1.25; mid 0.5 | ok |
| review-2 | items[1] r-iso-det | 39 (wrong 110.25, 6.245, 10.5) | 39; 110.25; 6.244998; 10.5 | ok |
| review-2 | items[2] r-drift-expt | -8 (wrong -9, -10, 8) | -9 + 1 = -8 (SymPy) | ok |
| review-2 | items[3] r-es2 | 8166.6 (wrong 7435.7) | 8166.562; 7435.739 | ok |
| review-2 | items[4] r-dlns | choice `right` | mu - sigma^2/2 | ok |
| review-2 | items[5] r-solve | 175.62 (wrong 182.79) | 175.6191; 182.7862 | ok |
| review-2 | items[6] r-prob-low | 0.0784 (wrong 0.0648, 0.1587) | 0.078429 (z -1.41572); 0.064795; 0.158655 | ok, note 16 |
| review-2 | items[7] r-which-mart | choice `right` e^(2W - 2t) | SymPy drifts for the four options: 0, +Z, 2Z, -1.5Z | ok, note 16 |
| review-2 | items[8] r-disc | 7.0 (wrong 12, 5, 17) | 7 | ok |
| review-2 | items[9] r-stop | 0.25 (wrong 0.75, 0.5, 0.3333) | 0.25 | ok |
| homework-2 | items[0] h-ito-vs-strat | code, 5 tests | rows match; identity row 0 | ok, starter fails, warning 4 |
| homework-2 | items[1] h-apply-ito | code, 5 tests | [2000, 4000], [500, 1000]; [0.06, 0.2]; [6, 12], [-3, 3]; [4, 0]; [] | ok, starter fails, warning 5 |
| homework-2 | items[2] part 0 | order o1 to o5, drop x1, x2 | c = p mu + p(p-1) sigma^2 / 2 | ok |
| homework-2 | items[2] part 1 | 1433329 (wrong 1271249, 1323130) | 1433329.41; 1271249.15; 1323129.81; lognormal route e^0.36 | ok |
| homework-2 | items[3] h-iso-w2 | 1.0 (wrong 0.3333, 0.5, 3) | integral of 3 t^2 = 1 | ok |
| homework-2 | items[4] h-which-mart | multi quart, expo, cos | SymPy drifts 0, 0, 0 for the three; 2, -1/2 of the process, 6 W^2 - 6 t for the three wrong | ok, note 16 |
| homework-2 | items[5] h-discount | expression `\mu - r` | -r + mu | ok, note 17 |
| homework-2 | items[6] h-cond-cube | 20 (wrong 8, 12, 14) | 8 + 6 x 2 = 20; 14 = 8 + 6 x 1 | ok |
| homework-2 | items[7] h-why-not-chain | longform rubric 2+2+2+2+2 = 10 | model: 0.27986, 0.25992, gap 0.019935, 2 and 8 points, median growth 0 at 8% and 40%, half the paths below the start | ok (every point checkable, correct), note 10 |
| **Total** | **79 widgets** | 48 numeric fields with 124 wrong values, 12 choice, 1 multi, 5 order, 2 expression, 1 table (8 cells), 1 drag-point, 8 code items (50 hidden tests), 1 longform | | 1 error, 7 warnings, 10 notes, 0 wrong keys |

## Fix pass

Targeted edits to the six level 2 files only. Scripts in the scratchpad folder `fix-ito2` (`calc.py` for the new numbers, `apply.py` for the edits). New seeded values were computed twice: the solution run with NumPy, and an independent pure-Python loop that uses the identities left = (W_n^2 - sum of squared steps)/2 and mid = W_n^2/2 (agreement to 1e-15). Closed forms (Phi values, slip values) came from `math.erf` and a numerical integral of the normal density (agreement to 1e-11).

1. Fixed. l7 `screens[4]` `plain` is now 0.1809 with `tol` abs 0.0005 (slip z 0.9118, 1 - Phi = 0.180931). The other wrong values are clear of it.
2. Fixed. l7 `screens[3]` `plain` is now 0.9118 (z of the drift-0.08 slip), so the feedback text is true as written.
3. Fixed. l8 `screens[2]` cell `r3c1` `tol` abs 0.005 (3.69 passes, 3.7 does not) and the prose says "Give the last row to at least 2 decimal places."
4. Fixed. `homework-2` `h-ito-vs-strat` uses seed 11 with `ns = [8, 64, 512]` (rows as in the finding, confirmed by both routes), seed 12 with `[10, 100, 1000]` for test 2 (new rows, both routes), seed 4 for the identity test; example, `how` and `explain` updated.
5. Fixed. `homework-2` `h-apply-ito`: $S^2$ with $\mu = 0.05$, $\sigma = 0.3$ at (0, 50) and (1, 40) gives `[[475, 1500], [304, 960]]`; $\ln S$ gives `[0.005, 0.3]` at every price; example and `explain` updated. Tests 3 to 5 unchanged.
6. Fixed. Keys shortened to the finding's wording: l5 `screens[5]` `gap` (116 to 82 characters), l7 `screens[6]` `qv` (117 to 83), l8 `screens[8]` `avg` (107 to 68). Meaning unchanged.
7. Fixed. l8 `quiz[3]` `quarter` feedback now names the slip (near over far, 1 over 4) and gives 1/5.
8. Fixed. l6 `screens[7]` prose now states $\sigma = 20\%$, $T = 1$.
9. Fixed. l5 `screens[0]` `accept` and `explain` state $-0.1853$ with "$-0.1852$ from the rounded products".
10. Fixed. l6 `screens[7]` `explain` now reads $0.27986 - 0.25992 = 0.0199$; `homework-2` `h-why-not-chain` rubric point 3 uses 0.27986 and 0.25992 and accepts 0.0199 or about 0.02.
11. Fixed. l5 `screens[2]` `feedback.generic` now says "on the four-step grid `W[::1024]` the left sum is -0.185297".
12. Fixed. l5 `screens[9]` tests 1 to 3 now expect the exact 0.495, 0.49 and 0.4975 (tol 0.04 kept); the seeded results 0.4788, 0.4851 and 0.4835 stay inside.
13. Fixed. l8 `screens[7]` prose now says the stopped bankroll stays between -£3 and +£7; `explain` says "No bounded stopping rule".
14. Fixed. l6 `screens[2]` prompt now names the two lines that may swap (first-order substitution and the squaring of $dX$), which matches `same` `[e2, e3]` exactly.
15. Fixed. l6 `screens[4]` `feedback.correct` now cites $e^{km + k^2s^2/2}$ at $k = 2$ from the moment generating function of level 1.
16. Fixed. `homework-2` `h-which-mart` now keys $e^{3W_t - 4.5t}$ (correction $\tfrac12\theta^2 = 4.5$; the wrong options are unchanged and still wrong); `explain` updated. Also `review-2` `r-prob-low` moved to $\mu = 6\%$, $\sigma = 25\%$ so it no longer reuses lesson 7's share: mean of $\ln S_1$ is $0.06 - 0.03125 = 0.02875$, z = -1.0076, P = 0.1568 (0.156829 by erf and by numerical integral); wrong `plain` (drift 0.06 in the log, z = -1.1326) 0.1287; wrong `price` ($\Phi(-0.8)$) 0.2119.
17. Left (P32-expr-exp), as instructed: an engine pass fixes the grader.
18. Disputed. Every sample-based test runs on a fixed seed, so the results are deterministic and cannot flake; the margins quoted (ratio 3.895 inside 3.4 to 4.6, $|\bar{W^3}|$ 0.0032 under 0.04, 0.05 standard errors) are checked in Pyodide on each playthrough and a wrong solution (midpoint, mean of sums) still fails the tests that target it.

### Changed keys

- `l5-integrating-noise.json` `screens[5]` (`gap`): option text only (key shortened).
- `l5-integrating-noise.json` `screens[9]` (code): `expect` of tests 1 to 3 (0.5 to 0.495, 0.49, 0.4975).
- `l6-ito-lemma.json` `screens[2]` (order): prompt wording only; `same` and `answer` unchanged.
- `l7-solving-gbm.json` `screens[3]` (z-score): `wrong` `plain` 1.3118 to 0.9118.
- `l7-solving-gbm.json` `screens[4]` (P(S_1 > 130)): `wrong` `plain` 0.1087 to 0.1809, `tol` 0.0008 to 0.0005.
- `l7-solving-gbm.json` `screens[6]` (`qv`): option text only (key shortened).
- `l8-fair-games.json` `screens[2]` (table): cell `r3c1` `tol` abs 0.001 to 0.005; prose adds precision.
- `l8-fair-games.json` `screens[8]` (`avg`): option text only (key shortened).
- `review-2.json` `r-prob-low`: numbers, key 0.0784 to 0.1568, `wrong` `plain` 0.0648 to 0.1287, `wrong` `price` 0.1587 to 0.2119.
- `homework-2.json` `h-ito-vs-strat`: seeds, grids, example and `expect` of tests 1, 2 and 5; test 3 seed.
- `homework-2.json` `h-apply-ito`: GBM parameters and points in example and tests 1 and 2, with new `expect`.
- `homework-2.json` `h-which-mart`: correct option `expo` text $e^{2W_t - 2t}$ to $e^{3W_t - 4.5t}$.

Results: `node tools/validate.mjs` 0 errors; playthrough of all six files with `--local-cdn`, with and without `--mobile`, all passed; changed code items (l5 `screens[2]` and `screens[9]`, `h-ito-vs-strat`, `h-apply-ito`) solution passes all tests and starter fails all in Pyodide. Voice scan: 0 explanations over three sentences; 2 sentences over 20 words, both in level 1 files (`homework-1.json` `items.8.model`, `l2-normal-increments.json` `screens.8.prose`), none in level 2 and not touched here.
