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

## Recheck

Recheck of fix pass ce71820, 2026-11-05. All numbers recomputed with independent code (scratchpad scripts, not the repo's), then compared with the content.

### 1. Widgets rechecked

Key, tolerance, slips, feedback and prose agree for all of these, with two prose mismatches listed below.

- l13: s0 choice (ratio 1.9901, £7.97 to £15.85); s9 table (S, vol, T merged; rule, exact, error 0.43%, 0.31%, 0.36%) and its code tests; q-ratio (0.2887 rule, 0.2891 at 20% vol, tol 0.01 accepts both).
- l14: s2 labels; s4 theta (-0.015714 with 0.0198, -0.015752 exact; key -0.0158, tol 0.0005 accepts both; slips -3.96 and -0.0314); s5 straddle sign table (0 means about zero); s8 desk theta (-632.45 exact, -632.54 from -15.94; key -632, tol 2; slips -159,400 and -316); recall-prefix screens carry no figures.
- l15: s1 (0.53233, key 0.5323, tol 0.0005; reversed slip -0.5323 reachable; width-10 value 0.5325 now falls inside tolerance, width-20 0.5330 as stated); s8 (1,064,650; tol 5,000 accepts 1.06m and 1,065,000, rejects no-discount 1,119,235 and d1 slip 1,211,544).
- l16: q0 wording; s4 (0.0813 and flat 0.1072 correct; see mismatch 2).
- l17: s3 (7.97/sqrt3 = 4.601, key 4.6 tol 0.1 accepts 4.616; slip 3.98); s5 and its explain; s7 up-and-out (vanilla call S 90, K 100, 20%, 1 year, r 0 is 3.5891, slip 3.59 tol 0.05); s8; s9 tests 6 to 9 (expects 7.9656, 4.6687, 4.8887, tolerances 0.37 and 0.21 are four standard errors); quiz.
- l18: s1 (net 0.0238 rounded gamma, 0.02394 exact, full revaluation 0.02342; key 0.024 tol 0.001; slips 0.0397, -0.0239); s5 (10.3434 - 7.9656 = 2.3778; vega x 6 = 2.38; constant gamma 2.739); s8 (-47,556, vega shortcut -47,634).
- review-4: r-digital at 95 (d2 0.4065, Phi 0.6578, price 0.6257, put 0.3255); r-smile 24/20/17; r-rank (all five rows hold, including Asian put under European at r = 0 and American put equal at r = 0); r-breakeven (£40, 35%: 0.8819; slip 14); r-upout 80/85/90; r-parts-gamma (theta -0.01975, breakeven 0.7874, P&L 261.2, full revaluation 254.9 up and 270.6 down; tol 7 accepts 255, rejects 271; no-half 522).
- homework-4: item 3 d2 -0.6195, Phi 0.2678; item 1 gap noise (my run: standard error 0.006 at 6,000 paths, gap 0.0013).
- topic-1.7: e-bs-hedge (d1 0.5383, d2 0.3615, price 9.015 exact or 9.010 from the table, hedge 1,409.6; d1 and d2 tol 0.005 accept 0.538 and 0.36 and reject the sigma slip 0.3807; digital 0.63161 exact, 0.63165 from the table, tol 0.0008 accepts 0.632 and 0.631, rejects 0.6412, 0.6943, 0.3535); e-american-put (5.873, 5.248, 4.567, order holds).

Mismatches found:

1. l17 s5 option text and explain: "about £7.97 on a tree" and "about £7.97 on an 800-step tree" are wrong at two places. The CRR 800-step tree (same as `check_l4.py`) gives 7.9631 for both puts, which rounds to 7.96. The fix replaced a correct 7.96 with 7.97. Recommend "£7.96 on an 800-step tree (7.9656 exact)". At 5% the tree gives 6.0894 and 5.5710, gap 0.518, so "dearer by £0.52" and "£6.09 against £5.57" hold.
2. l16 s4 explain: vega x 0.002 is 12.916 x 0.002 = 0.02583, which rounds to 0.0258, not 0.0259. Then 0.1072 - 0.0258 = 0.0814, not 0.0813. Unrounded, 0.10715 - 0.02583 = 0.08132, so the answer 0.0813 is right. Recommend "takes 0.0258 off the flat-vol chance: 0.10715 - 0.02583 = 0.08132, so about 8.13%".

Minor: l13 q-ratio explain says "Black-Scholes gives 0.2891" without "at 20% vol"; the accept line has it. Optional.

### 2. Asian call, S = K = 100, 20%, 1 year, r = 0, n fixings at t = i/n

Method: exact lognormal moments of the discrete geometric average give the control's closed-form price. Then Monte Carlo with exact GBM steps, antithetic pairs and a fitted control-variate coefficient.

| Fixings | Geometric control (exact) | Arithmetic Asian call | Standard error | Paths |
|---|---|---|---|---|
| 12 | 4.7190 | 4.8888 | 0.00005 | 10,000,000 |
| 52 | 4.4981 | 4.6685 | 0.00004 | 10,000,000 |
| 252 | 4.4456 | 4.6160 | 0.00007 | 4,000,000 |

- 252 daily: stated 4.62 is right at two places (4.6160). "three-million-path simulation, standard error 0.0001" is consistent.
- 12 monthly: stated 4.89 is right at two places (4.8888). The test `expect` 4.8887 is within 0.0001 and fine.
- 52 weekly: 4.6685 plus or minus 0.00004. The stated 4.6687 is 0.0002 high, about 5 standard errors on my run, so at four places it is not right. At two places both give 4.67. Recommend 4.6685 in the explain and the `how` line and test 6 `expect`, or round to 4.67. The 0.21 tolerance makes the test indifferent. The fix agent's 4.6684 agrees with mine, and the checker's 4.6687 (a moment-matching value) is the outlier.

### 3. Old values

Grepped `courses/trees/` and `exams/topic-1.7.json` for 4.63, 4.90, 4.6779, 4.8977, 0.4400, 0.4626, 0.5112, 5.325, unscaled, 7.96, "Average so far", "small shortfall", -0.6193, 0.9449, 0.94, £6.09, "four decimal", "list the four paths", "formula 4", "by formula", the old smile vols and 44p. None remain as replaced. Hits that are legitimate: l15 quiz digital put at 105 (0.4400 and 0.5112, a different, correct problem), homework-4 £0.94 (100 x 15%, another problem), l17 "£6.09 against £5.57" (correct), 4.63 inside a data array in l18. The one value that should change is mismatch 1 (the new 7.97).

### 4. Layout

`node tools/playthrough.mjs --lesson trees/l13-rules-of-thumb --shots ... --mobile --local-cdn ...`: 14 checks, quiz 4/4, all passed. Screen 9 at 440 px: four columns (S, vol, T / Rule / Exact / Error) fit with margin, all rows and headers fully visible, nothing clipped.

### 5. Voice

`VOICE_BASE=app/content/courses/trees/ python3 docs/reviews/voice-scan.py --summary`: 0 explanations over three sentences. The full scan lists no hits in l13 to l18, review-4 or homework-4 (its 14 long sentences are in homework-1 to homework-3).
