# Answer check, 4 November 2026: mock-superday-research

**Summary.** 18 items checked (S1 to S4, M1 to M6, C1, C2, K1, K2; S1, S4, M5 and C1 have 3 parts each, so 28 keyed answers), plus paper timing, pass rules, draw filter and voice. Wrong keys: 0. Mismatches: 1 voice, 1 note. Duplicates against courses, exams, drills and bank: 0.

Method: every key recomputed in Python (NumPy, SciPy, `Fraction`s, grids, simulation) in the scratchpad folder `answers-mock-research`: `nums.py` (numeric and choice items, cases), `code.py` (hidden tests, starters, wrong solutions), `exact.py` (exact `Fraction` expected values of every code test), `np_test.py`. I read neither `docs/briefs/mocks-scripts/` nor the author report.

## Items

| Item | Key | My computation | Verdict |
| --- | --- | --- | --- |
| S1 p1 | 0.7 | $\sqrt{0.35 \times 1.4} = 0.7$; wrongs 0.49 ($r^2$), 0.875 (mean of slopes) match feedback | ok |
| S1 p2 | 0.5 | 0.35/0.7 = 0.5 and 0.7/1.4 = 0.5; wrongs 2.0 (flipped), 0.35 (slope) match | ok |
| S1 p3 | same slope, SE about 30% smaller | Simulated 40 rows then duplicated: slope identical, SE ratio 0.69798 = $\sqrt{38/78}$; distractors: 50% (halved), unchanged, slope halves: all wrong, `why` fit | ok |
| S2 | -0.1913 | $ab + \sqrt{(1-a^2)(1-b^2)} = -0.5400 + 0.3487 = -0.19129$; grid on determinant of the 3x3 matrix gives -0.19129 (min -0.88871). Wrongs -0.54, 0.191, -0.889 match | ok |
| S3 | 135 | `det` of $3I + 0.5J$ = 135.0; eigenvalues 3, 3, 3, 5. Wrongs 81, 625, 15 match | ok |
| S4 p1 | 0.4596 | $1 - 0.95^{12} = 0.459640$; wrongs 0.6, 0.05, 0.5404 match | ok |
| S4 p2 | 0.00417 | 0.05/12 = 0.0041667; wrongs 0.05, 0.6 match | ok |
| S4 p3 | not significant, above 0.0042 | 0.006 > 0.004167; distractors wrong, `why` fit | ok |
| M1 | 1.3333 | 100/75 = 1.33333; numeric minimiser of the penalised sum gives 1.333333; wrongs 2.0, 1.0, 0.0769 (2/26) match | ok |
| M2 | 2.5 | Per-coordinate minimiser of $\tfrac12(b-c)^2 + \lvert b \rvert$ gives 2, 0, -0.5, 0, sum 2.5; wrongs 5.6 (sum of ols) and 3.4 (2 + 0.2 + 0.5 + 0.7, no floor) match | ok |
| M4 | 0.7945 | `eigvalsh` gives 5.5616 and 1.4384; 5.5616/7 = 0.79451; wrongs 4/7 = 0.5714, 0.5 match | ok |
| M3 | scaler saw the test rows | No number. Distractors wrong (scaling does not change OLS $R^2$; a later test set is honest; simplicity does not inflate a score). Lengths 52 vs 49, 57, 50: key not longest | ok |
| M5 p1 | 1.5 | 0.25 + 0.25 + 1; wrongs 1.75, 0.5 match | ok |
| M5 p2 | 1.68 | 0.04 + 0.64 + 1; wrongs 1.84, 0.68 match | ok |
| M5 p3 | more data or stronger penalty | Bias is 0.04 of 1.68; distractor `why` lines fit; key not longest | ok |
| M6 | 6.5 | Residuals -5, -3, 2, 6. Split sums of squares 40.67, 10, 26, so {1,3}/{8,12}. Stump values -4 and 4, half is -2 and 2; errors -3, -1, 0, 4; 26/4 = 6.5. Wrongs 18.5 (before) and 2.5 (rate 1) recomputed and match | ok on key; explain too long (mismatch 1) |
| C1 p1 | code | Own solution passes 8 of 8 and the reference 8 of 8. Exact `Fraction` normal equations give every expected pair (test 5 is exactly [1.7, -170000002.9]). Starter returns `None`: 0 of 8. Textbook-sums solution (no centring) fails test 5 and no other. A solution with no validation fails 6, 7, 8 | ok |
| C1 p2 | code | Own and reference pass 13 of 13; expected values exact (test 3 slope 2.6153846..., test 4 [0.2, 5.0]). Part 2 starter (the part 1 solution) passes 8 and fails the 5 new tests. Wrongs: ignoring weights fails 10, 11, 13; weights squared fails 10, 11; no weights length check fails 13 only; textbook sums fail 5 only. None passes | ok |
| C1 p3 | $1/\sigma_i^2$ | Standard result. Distractors wrong, `why` fit, key not longest | ok |
| C2 | code | Reference and my prefix-sum solution pass 10 of 10 in under 1 s. Exact integer prefix sums with `Fraction` slopes: test 8 total 1.007939393939394 (key matches), test 9 2.0, test 10 150001; all small tests match brute `Fraction` windows. Starter fails all 10. Naive $O(nw)$ recompute passes tests 1 to 7 and times out on 8, 9, 10 at 15 s. Missing `None` handling fails test 6. Partial windows fail 9 of 10. Float running sums and a NumPy float `cumsum` solution pass (test 9 gives 2.00000000000006; test 8 off by 6e-14), as the brief says; the tolerances are fair | ok |
| K1 | rubric 10 | SE $\sqrt{0.25/1000} = 0.015811$; $z = 1.4546$; two-sided $p = 0.1458$; coin plus 2 SE is 0.5316, "53%" fine. Rubric points 2+1+2+2+2+1 = 10; model (164 words) hits every line; scorable | ok |
| K2 | rubric 10 | $t = 1.2647$ (1.27); $R^2 = 0.16\%$; Fisher interval -0.0220 to 0.1017 (-0.02 to 0.10). Rubric 1+2+2+2+1+2 = 10; model (137 words) hits every line; scorable | ok |

## Structure

- Paper timing: stats 45 min (fixed pace 420+300+240+480 = 1,440 s), ml 30 min (210+210+270+270+420+360 = 1,740 s), coding 45 min (1,500+1,200 = 2,700 s), case 45 min (1,200+1,500 = 2,700 s). Total 165 min, 18 items, 2 `longform`. All agree with the brief.
- Pass rules: 0.6, 0.65, 0.5, 0.5, scoring right 1, wrong 0, blank 0; two checks `story-aloud` and `no-lookup`. All agree with the brief.
- Draw: one entry, `bank/probability`, 16 tags, difficulty 3 to 5, `n` 4. It matches 30 items across `probability-1` to `-4` (brief: 30); every one has `research` in `role` and a numeric or choice widget; 16 families, so four distinct families are available. Drawn pace (90 to 180 s each) is within the paper's slack.
- Counts of parts: S1, S4, M5, C1 have 3 parts each, as the brief says.
- `models` is 173 characters (under 200). Firm names appear only in `models`. The description has no firm name and no exclamation mark.
- Duplicates (DECISIONS "Duplicates"): grepped `app/content/` (courses, exams, drills, bank) for the figures of every item (523 of 1,000, correlation 0.04, slopes 0.35 and 1.4, 0.9 and -0.6, the 3.5/0.5 matrix, rows (4, 2) and (2, 3), $S_{xx} = 50$, targets 1, 3, 8, 12, bias and variance pairs, 12 signals, ridge penalty 25, code names). Hits were all coincidences in other contexts (chart data, other formulas): none is the same item.
- Voice: no em-dashes, no exclamation marks (the four `!` are `!=` in code), British spelling. `docs/reviews/voice-scan.py` on a folder holding the file: 0 sentences over 20 words. The only long sentence is `models` (27 words), which the brief sets and which is a label.

## Mismatches

1. `m6-boosting-round`, `explain.text`: four sentences (mean and residuals; split gives 10; the other splits 40.7 and 26; stump adds ±2 and the mean square is 26/4). The rule allows three. Fix: join the second and third, for example "Splitting after the second point leaves a residual sum of squares of 10, against 40.7 and 26 for the other splits."
2. Note, no fix required: `k1-open-case-framing` carries the tag `open-case-hit-rate`, not a tag matching its id (brief names only the id). Leave as is unless the manifest or skill chart expects family-first tags equal to the id.

## Notes

- The per-part starter check (starters fail) is by my own run, not the playthrough, as the inbox bullet already records.
- Wrong keys: none.
