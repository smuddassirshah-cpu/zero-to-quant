# Answer check: trees level 4 (l13 to l18, review-4, homework-4)

Date 2026-11-05. Scope: `app/content/courses/trees/` l13-rules-of-thumb, l14-greeks-by-shape, l15-digitals, l16-the-smile, l17-which-is-cheaper, l18-gamma-and-hedging, review-4, homework-4.

Widgets checked: 109 (l13 to l18: 14 each = 84; review-4: 13 including parts; homework-4: 12 including parts, one long-form). Table cells, order keys, sketch and drag-point targets, and 8 code items (66 hidden tests in all: 8+7+10+10+9+8 in lessons, 7+8 in homework) are included.

Method: every number recomputed from the question text with my own code (own Black-Scholes, Greeks, Reiner-Rubinstein barrier, Goldman-Sosin-Gatto lookback integral, CRR tree with 800 steps, Monte Carlo with geometric control variate for Asians, my own daily hedging loop, reconstruction of paths N and F). The authors' check scripts were not read or run. Code items: the model solution was run against the hidden tests, then the starter.

Result: all keys are right. Every `wrong[]` slip value matches the mistake its feedback names. Every choice, multi, order and table key agrees with its explanation. All model solutions pass all hidden tests and every starter fails every test (0 of n). The only disagreements are in stated prose figures that are not keys, listed below; none changes a key or makes a tolerance accept a wrong answer or reject a right one.

## Mismatches (stated figures)

| file | path | stated | my value | method |
|---|---|---|---|---|
| l17-which-is-cheaper | screens/3 `accept`, screens/8 `explain`, quiz context | daily-fixing Asian "formula 4.63" | 4.616 (4.62) | 252 fixings, r=0, Monte Carlo 3M paths with geometric control variate, SE 0.0001 |
| l17-which-is-cheaper | screens/9 prose, `explain`, test 6 `expect` | 52-fixing Asian "4.6779 by formula" | 4.6687 | same method, SE 0.0001 |
| l17-which-is-cheaper | screens/3 `explain`, screens/9 test 9 `expect` | 12 closes "4.90" and "4.8977" | 4.8887 (4.89) | same method; the 0.614 of the vol is right (4.8887/7.9656 = 0.6137) |
| homework-4 | items/3/parts/0 `explain` | d2 = -0.6193 | -0.6195 | (ln(100/110) - 0.0162)/0.18; the key 0.2678 is unaffected |

The l17 differences are 0.009 to 0.014 and look like a moment-matching approximation labelled "formula". Hidden-test tolerances (0.21) hide them. Suggest "about 4.62", "about 4.67", "about 4.89", or relabel as approximate.

## Notes

1. l18 screens/5 `accept`: "10.34 - 7.97 = 2.3778" does not hold with the rounded prices shown (2.37). The key 2.38 is the exact gap (2.3778) and 2.37 passes under tol 0.02. Say "from unrounded prices".
2. l18 screens/1: the question gives 0.0099 and -0.0158, so 0.0099 x 4 - 0.0158 = 0.0238 and 0.0396 for gamma. The explain says 0.0397 and 0.0239 (from unrounded gamma). Key 0.024 (tol 0.001) and slips (0.0397 +-0.0005 accepts 0.0396; -0.0239 +-0.001) are fine. Full revaluation 0.0234 is accepted.
3. l14 screens/4: with the stated gamma 0.0198 the result is -0.0157; the key -0.0158 comes from exact gamma. Tol 0.0005 accepts both. The explain states both correctly.
4. l14 screens/8: key -632 (tol 2) accepts -632.54 (from the stated -15.94) and -632.45 (exact).
5. l13 quiz q-ratio: the question gives no vol, but "Black-Scholes 0.2891" holds only at 20% (0.2894 at 25%). Key 0.29 (tol 0.01) is fine at any vol from 10% to 30%.
6. l14 screens/5 table: the straddle delta is keyed "zero". The true value is 0.04 (3 months) to 0.08 (1 year), "about 0"; the `explain` and feedback say "about 0", and "0", "~0" and "flat" are accepted. The calendar delta 0.0084 is fine.
7. l15 screens/1 slip `unscaled-width` (5.325, tol 0.01): value is right (5.3251 for the 95/105 spread) but the question never mentions a 95/105 spread, so the slip is only reachable by a learner who imagines it. Consider a different slip or a prompt mention.
8. l15 screens/8: key 1,064,650 (tol 200). A learner who rounds the price to 0.5323 gets 1,064,600 (accepted), but one who types 1,060,000 ("about £1.06m", as the feedback phrases it) is rejected. Consider tol 5,000.
9. review-4 items/7/parts/2: key 261 (tol 5). The `accept` cites full revaluation £255 (254.85 up, 270.61 down), which is 6 away and rejected. Fine if intended; otherwise widen to 7.
10. homework-4 items/1 `explain`: "a small shortfall from hedging daily" at 18% (mean -0.7927 against -0.7943) is a gain of 0.0016, under one standard error (0.0063). It is noise, not a shortfall.
11. l16 density canvases (screens 1 to 5, not keyed): sampled points differ from d2C/dK2 by up to 2e-5 at the ends (140: 0.001268 against 0.001239). Not a key.
12. l14 screens/0 sketch: the ramp wrong-band (0.11) contains the true curve (max gap 0.095), so the correct answer must be tested before the ramp. The correct band (0.05) excludes the ramp, so a ramp is not accepted as correct. Fine as written if the engine checks correct first.

## Verified without mismatch (sample of key figures)

- l13: 7.9656, 15.8519 (ratio 1.99), 3.9878, 3.188, 39.695, 0.7935, 10.4506, 10.4385, 5.91/4.29/2.15, 6.9084 (straddle), 12.55x for doubled spot at fixed strike, 1.86.
- l14: delta 0.5398, gamma 0.019848, peak 94.18 (0.02076), ratio 6.58, vega 0.397, theta -0.015752, calendar [0.0084, -0.0292, 0.0841, 0.0232], gamma ratio 15.95, vega 2.51, desk theta -632.45, breakeven move 1.26.
- l15: 0.532325, 0.4189, 0.5417 (excess 0.0094), 3166 and 188 shares, £1,064,650, 0.5112, d1 slip 0.6058, no-discount 1,119,235.
- l16: 8.13% against 4.62% (ratio 1.762), 10.72% (10.715), 7.90% against 4.16%, 0.0794, 0.5396, 0.9224 premium, flat -0.9614; all ten test values to 6 places.
- l17: payoffs 12, 1.5, 21, 0; lookback 14.984; knock-in 1.4982, knock-out 6.4674; American put 6.0894 (800 steps) against 5.5735, premium 0.5164; up-and-out vanilla 3.59; seed-17 simulation 8.02 and 4.69.
- l18: years A and B 2.0682 and -2.4305 exact, 2.0795 and -2.4412 gamma sum; fall 10.56% and 21.55%; realised vol 26.6% and 12.7%; paths N and F 4.82, 0.38, -4.21, -1.06 (reconstructed); -47,556; 1,588 (exact 1,586); 0.9449; flat path -7.9656 and -7.6064; [100, 105] test -5.6647 and -3.7214.
- review-4: 3.1895, 0.4400, -0.01975, 261.1, 0.5396, 0.7874, order and table keys.
- homework-4: all rule_with_rate test triples, 2.3778, -0.7943, -1.9759, 0.2678, 0.3402, 0.2059, knock-out at 99 0.9646 (stated 0.96), lookback 14.98, 16.2917 rule against 16.2377, 2.7153 and 2.7017, 1,351.75, long-form -1.9870, -1.98.
