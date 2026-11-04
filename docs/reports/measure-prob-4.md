# Report: measure-prob level 4, "Changing measure" (topic 3.2)

Brief: `docs/briefs/measure-prob.md` `## Level 4`, with the brief-check corrections: `ito` l10 and l11 are written (read, notation matched: `Z_T = e^{-\theta W_T - \theta^2T/2}`, `\tilde W = W + \theta t`); `estimation` l5 and `trees` l3, l5 read; `\exp` and letter-before-bracket now grade, so keys use `e^{...}`; `--mobile` is 440 wide and `--tablet` adds 1032 and 1376. Ids, names, objectives and skills are those of `course.json`. The planner's scripts are gone; every number was recomputed.

## Files (`app/content/courses/measure-prob/`)

| File | Screens | Quiz | Canvases and widgets |
|---|---|---|---|
| `l14-radon-nikodym.json` | 10 | 4 | `bars` (groups, factors), `plane` (two normals with theta control, step densities), `tree`, `console`; `table`, `numeric`, `choice`, `expression`, `code` (`rn_derivative`, `expect_q`, `prob_q`) |
| `l15-likelihood-ratios.json` | 9 | 4 | `plane` (tail area, theta control, derive caption with the relative error), `console`, `table`; `slider` (graded), `numeric`, `choice`, `expression`, `code` (`is_tail`, `best_theta`, NumPy) |
| `l16-girsanov-on-a-tree.json` | 10 | 4 | `walk` (weight and weighted-position overlays, `qn` control, `showStopped`), `tree`, `table`, `graph` lattice (cells bound to node values); `order` (proof), `choice`, `expression`, `code` (`girsanov_weight`, `q_mean_via_p`) |
| `l17-risk-neutral-rigorous.json` | 10 | 4 | `graph` lattice (discounted prices as labels), `plane`, `tree` (trinomial), `table`; `order` (proof), `choice`, `numeric`, `code` (`risk_neutral_q`, `tree_price`, `is_discounted_martingale`) |
| `review-4.json` | 8 items, difficulty 2 to 4 | | two per lesson, one two-part item (l16 and l17) |
| `homework-4.json` | 9 items, difficulty 3 to 5 | | six `parts` items, `order` (d4), `code` (d5), `longform` (d5, rubric 10) |

Build scripts, number scripts and checks: scratchpad `measure-prob-4` (`l14.py` to `l17.py`, `review4.py`, `homework4.py`, `nums1.py` to `nums4.py`, `pycheck.mjs`, `exprtest.cjs`, `seeds16.mjs`).

## Validator, playthrough, voice

- `node tools/validate.mjs`: 0 errors; no warning in any of the six files.
- Playthrough with `--local-cdn`: each lesson, `review-4` and `homework-4` pass; the final desktop, `--mobile` and `--tablet` results are in the hand-back.
- Voice scan: 0 sentences over 20 words, 0 explanations over three sentences.
- Code (`pycheck.mjs`, Pyodide 0.27.7, NumPy 2.0.2): every solution passes all tests and examples, every starter passes none: l14 12 of 12, l15 11, l16 12, l17 14, homework 12. The NumPy-seeded values in l15 match the CPython 2.5.3 references to relative 1e-6. NumPy load in the playthrough is inside the code widget's extra budget; l15 ran in 18 s in all.
- Expression grading (`exprtest.cjs`, the engine's `exprEqual`): for the three expression answers, 25 equivalent forms pass (including `\exp(...)`, `\exp\left(...\right)`, `e^{\theta(x-\theta/2)}`, reordered and fraction forms) and 11 wrong forms fail. Greek `\theta` and `w`, `t` are free symbols.

## Lesson size: which rungs moved

- l14 (10): `Q << P` is the name screen (choice); the numeric `E_P[X e^{\theta X - \theta^2/2}] = \theta` and `dP/dQ = 2` are quiz items; the edge case (Z = 0 on a face) is a quiz item; the brief's ladder rung (1) asks Q(even) and Q(faces 5, 6), and `E_Q[face] = 4.2` moved to the trap (so the trap's number is not shown earlier).
- l15 (9): the likelihood ratio 125/144 is a ladder screen before the name; the derived weight is one `expression` screen; "the estimator at theta 4" is a numeric (relative standard error 2.1%) plus the code screen; choosing theta is the graded slider in the explore screen (answer 4.1, tolerance 0.5, wrong ranges 0 to 2.5 and 5.5 to 6); theta = 0 is a quiz item.
- l16 (10, dense): step weights (table), HHT (the name screen, a numeric `generalise`), martingale proof (`order`), Bayes rule (`choice`), continuous limit (`expression`), trap (`choice`), code, transfer. The numeric 0.9 (up-only weights) is in the trap's distractor and quiz item `q-down`; `q = p` and `q = 1` are quiz item `q-edge`.
- l17 (10, dense): the arbitrage choice and the trinomial "range" choice are quiz items (`q-arb`, `q-incomplete`); the continuous call 10.4506 is quiz item `q-bs`; rung (3) prices the put (6.29, trees l5) so the call 15.59 is the trap's answer, not shown earlier.

## Proof steps and the widget that grades each

- l16 `order`: `Z_n` is a `P`-martingale with mean 1 (4 lines, `same` on the two middle lines, 2 distractors: a fair toss assumed, an average under Q).
- l17 `order`: easy direction of the fundamental theorem (4 lines, a strict chain, 2 distractors: the wrong measure, Q taken as P). Written as a direct argument (zero Q-chance, then equivalence), not a contradiction, so that no valid alternative order exists.
- l16 `choice`: Bayes' rule; l16 `expression`: the continuous limit; l17 `choice`: the continuous drift.
- Homework: Bayes' rule for conditional expectations, `order` (5 lines, strict chain, 2 distractors); the whole two-step argument, `longform` (rubric 2, 2, 2, 2, 2).

## Numbers and two routes

| Value | Route 1 | Route 2 |
|---|---|---|
| Z = 0.6, 0.6, 0.6, 1.2, 1.2, 1.8; E_P[Z] = 1; Q(even) 0.6; Q(5,6) 0.5; E_Q[face] 4.2 = 21/5; E_Q[face^2] 20.4; product of means 3.5 | `Fraction` of `Q/P` | `E_P[ZX]` against the direct `Q` sums |
| E_P[X Z] = 0.5 at theta 0.5 | closed form | SciPy quadrature (0.5000000000000002) |
| Z_up 0.8929, Z_down 1.25, price 11.9048 (kernel 0.8503, 1.1905) | `Fraction` | `q * 20 / 1.05` |
| 1 - Phi(4) = 3.16712e-5 (3.167 per 100,000, 0.3167 per 10,000) | `math.erfc` | mpmath, SciPy |
| relative error per draw 177.689, 7.2596, 3.0559, 2.1239, 2.6649 at theta 0, 2, 3, 4, 5; 5.635 at 6; 3.655 at 5.5 | closed form with `erfc` | SciPy quadrature of the second moment (agrees to 1e-12) |
| best theta 3.1548, 4.1197, 5.0972, 2.2159; minimum 2.1145; below 2.3 on 3.596 to 4.644 | golden section | SciPy bounded minimiser and a 2001-point grid (one turning point) |
| seed 21: estimate 3.184973e-5, standard error 6.72973e-7 (2.11%), 4,994 of 10,000 above 4, weights sum 0.318497, plain run 0 hits, inverted weights 4.19e11 per 100,000 | CPython NumPy 2.5.3 | Pyodide NumPy 2.0.2 (same to 1e-6) |
| 125/144 = 0.8681 (HHT) | `Fraction` | direct 0.5^3 / (0.6^2 x 0.4); path enumeration |
| 1.152, 1.0417 (distractors) | 144/125; (5/6)(5/4) | arithmetic |
| plain draws for 10% at £3m: 73,980 (p = 0.0013499); importance sampling 333.4 (per-draw 1.8258 at theta 3.1548) | closed form | `erfc` and SciPy |
| Walk (seed 74, p 0.6, 20 steps, 300 paths): plain 4.05, mean weight 1.00, weighted average -0.06 at q 0.5; 2.00 at 0.55; 6.03 at 0.65; 7.90 at 0.7 | the engine's stream ported to Node (`seeds16.mjs`) | the playthrough screenshot: "Plain average 4.05, mean weight 1.00, weighted average -0.06" |
| E_Q[S_20] = 20(2q - 1); E_P[Z_20^2] = 2.2624 (standard error of the mean weight 0.065); sd of weighted mean at q 0.5, 0.7, 0.3: 0.52, 0.93, 22 | exact binomial sums | closed form (q^2/p + (1-q)^2/(1-p))^n |
| E_P[ln Z_n] = -0.0612625 (n 100), -0.0612501 (n 10,000); variance 0.12245, 0.12250 | binomial sum | mpmath 30 digits (limits -0.06125, 0.1225) |
| `q_mean_via_p`: f = 1 gives 1; S_10 gives 0 at q 1/2 and 1 at 11/20; running maximum n = 4 gives 19/16; heads count at q 2/5 gives 8/5 | enumeration of Z_n f | direct Q enumeration |
| Two-step weights 625/784 = 0.7972, 125/112 = 1.1161, 25/16 = 1.5625; E_P[Z_2] = 1; price 6875/441 = 15.5896 (also E_P[Z_2 payoff]/1.05^2); real chance 19.5556 | `Fraction` | float, and `q^2 x 44 / 1.05^2` |
| Discounted prices 100; 114.2857, 76.1905; 130.6122, 87.0748, 58.0499; root under p = 0.7: 102.857 | arithmetic | `Fraction` (800/7 at the up node) |
| q = 25/24 = 1.0417 for u = 1.04; q = 0.4667, 0.52, 1.0769, 1.1538 | `Fraction` | float |
| put 925/147 = 6.2925; parity 15.5896 - 6.2925 = 9.2971 = 100 - 100/1.1025 | `Fraction` | float |
| trinomial: q_u = q_d, range (0, 10) for the £120/£100/£80 call; (0, 15) for the £130/£100/£70 put; call at £6 gives q_u = 0.2, put 6 | the mean condition | parity with r = 0 |
| call 10.4506 = 63.6831 - 53.2325 | rounded Phi | closed form 10.450584 (mpmath and SciPy) |
| Review: E_Q 22.5 (E_P 17.5), e^{-6} = 0.0024788, n = 17,182, Z_THH = 1000/1089 = 0.9183, q = 0.52, 7.2664 (2100/289), 5.05 real | `Fraction` | float and closed form |
| Homework: Z(4) = 4, E_Q 3, E_Q[X^2] 10; 26.600 per 100,000, best theta 3.6005, per-draw 1.9636, n = 386 (plain 375,836); dP/dQ 1.12047; DD weight 2.0408, put 4.3084 (1900/441), real 2.1111; q = 15/13 | `Fraction` and closed forms | mpmath, SciPy, enumeration |
| `bayes_cond` values 11/8, 35/16, 9/16, 9/4, 1/4, 2, 7/5, 3/10, 43/25 | direct Q enumeration | Bayes route `E_P[Z_n f | F_k] / Z_k` (the two agree at every node) |

## Departures from the brief

- l14: see "rungs moved" (E_Q[face] in the trap, Q(5,6) in the ladder). The hook asks for the weight on all six faces in one table.
- l15: the trap asks the estimate per 100,000 days from the given count and weight sum (answer 3.185, wrong entries 49,940 for the raw share and 0.3185 for the undivided sum), not the share 0.5; the inverted-weight slip (4.19e11) is a quiz choice. The transfer is the £3m tail (73,980 plain draws against 333), with the ito price in its explanation.
- l16: the control on `qn` runs 0.4 to 0.7 (brief: 0.3 to 0.7) because the weighted mean is too noisy at 0.3 (inbox). The hook hides the weighted-average panel until the answer is checked.
- l17: the easy direction is written forward (no contradiction); rung (3) is the put, not the call. The continuous screen is a `choice`; the numeric call is a quiz item.
- Reading list: Williams chapter 14 (l14), Shreve I chapter 3 (l14 summary), Shreve II chapter 1.6 (l15), 5.2 (l16) and 5.4 (l17).
- The first screen of l14 states that topic 3.2 is optional and serves desk quant and derivatives pricing roles.

## course.json

No edit. Prerequisites beyond `requires` (`measure-prob/L3`, `ito/L3`): `estimation` l5-which-fits (the likelihood ratio, l15), as the brief check proposed; `trees` l3 and l5 (the tree, q = 0.625, prices 11.90 and 15.59) are inside the `ito/L3` closure. Proposed `requires`: `["measure-prob/L3", "ito/L3", "estimation/l5-which-fits"]`.

## Inbox

Four bullets under "Raised later (topic 3.2 levels, 4 Nov), measure-prob level 4": one [Should] (validator does not accept `byKey` ids from table cell `wrong` entries), three [Could]. No [Must].
