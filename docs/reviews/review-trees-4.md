# Trees level 4 and topic-1.7 changed exam items: second-reader findings

Scope: `app/content/courses/trees/` l13 to l18, review-4, homework-4; exam items e-atm-rule, e-greek-signs, e-bs-hedge, e-american-put in `app/content/exams/topic-1.7.json`.
Method: every exam key recomputed (scipy, two routes); lesson numbers spot-checked (about 120 values, all agree with the stated figures); grading code read (`widgets/numeric.js`); playthrough with `--mobile --tablet`, local CDN, screenshots at 440, 1032, 1376 kept outside the repo; voice scan and grep for em-dashes, exclamation marks, American spellings.
Format: `path | location | finding | proposed fix`.

## Counts

0 errors, 8 warnings, 9 notes. No wrong answer key; no correct form graded wrong in the four exam items beyond the rounding cases below. Voice: new trees files 0 sentences over 20 words and 0 explanations over three sentences (the 14 over-20 hits in the trees scan are all old levels). Exam copy: 2 sentences over 20 words, both in changed items. No em-dashes, no exclamation marks, no American spellings in new files.

## Errors

None. Exam keys recomputed: 15.00, 1.00, 8.66; short-put signs, gamma peak 94.18, P&L -316.80; d1 0.5383, d2 0.3615, call 9.015, hedge 1,409.6, digital 0.6316 and its slips 0.6412, 0.6943, 0.3535; American 5.873, European 5.248, Asian 4.567. All match.

## Warnings

- `app/content/manifest.json` (merged tree) | `--set trees/review-4`, `homework-4` | The committed manifest was stale: the first run failed "the set has no items" and homework timed out. After `node tools/validate.mjs` rewrote it, review-4 (9 of 9) and homework-4 (8 of 8, 38 of 38 marks, parts checks) pass. | Commit the regenerated manifest with the level, or the playthrough and app fail for level 4.
- `l13-rules-of-thumb.json` | screen 9 (code), canvas `table` | Confirmed clip at 440: the table has six columns (S, sigma, T, Rule, Exact, Error) and "Error" is cut off at the right edge (`trees_l13-rules-of-thumb-lesson-09-problem-440.png`). It is not the l14 grid, which was transposed to four columns and fits. 1032 and 1376 are fine. | Drop the T column or shorten headers ("Rule", "BS", "Err"), or let the table scroll sideways.
- `l16-the-smile.json` | screen 4 `explain.text` | "The skew's slope subtracts vega x sigma' from the flat-vol chance": sigma' is -0.002, so subtracting it would add 0.0259 (giving 0.1331). The chance below K is the flat chance plus vega x sigma'. | "The skew's slope takes vega x 0.002 = 0.0259 off the flat-vol chance: 0.1072 - 0.0259 = 0.0813."
- `l17-which-is-cheaper.json` | screen 7 prose and wrong key `vanilla` 3.59 | The prose gives no vol, expiry or rate, yet 3.59 needs 20%, one year, r = 0. No learner can reach it. | Add "Take 20% vol, one year, r = 0", or drop the wrong key (the answer 0 does not depend on it).
- `review-4.json` | r-breakeven, r-upout, r-smile, r-digital, r-rank | Five of nine items reuse lesson inputs verbatim: £50 at 30% breakeven 0.94 is l18 q-breakeven; up-and-out 90/95/100 is l17 screen 7; vols 22/20/18 is l16 q-read; the digital at 105 (0.4400) is given in l15 q-put105; the rank table is l17 screen 4 with one row swapped. Learners can answer from memory. | Change the numbers (£40 at 35%; up-and-out 80/85/90; vols 24/20/17; digital at 95), keep the structure.
- `l14-greeks-by-shape.json`, `l18-gamma-and-hedging.json` | l14 screens 2, 6, 7, quiz q-falls, q-gamma-time, q-straddle-theta; l18 screen 1, quiz q-breakeven | Overlap with opt-dash l14 (gamma peak against expiry, vega goes as root T, straddle signs, break-even move, derived in opt-dash l14 screen 8). The brief asked for no repetition. The new content (vega and theta from gamma, sign grid, calendar, pin) is good. | Fold l14 screens 2 and 6 into one that links to opt-dash l14; give l18 screen 1 a move and gamma not used there.
- `topic-1.7.json` | e-bs-hedge part 1, d1 and d2 cells (tol 0.001) | The question gives no decimals. A learner who rounds to 0.54 and 0.36 is marked wrong with only the generic hint. | tol 0.005 on both (the sigma-denominator slip, 0.3807, stays outside).
- `topic-1.7.json` | e-bs-hedge part 3 prose (26 words); e-american-put part 2 question (37 words) | Voice. The second also opens "List the four paths of the tree.", an instruction a choice widget cannot take. | "In the market the 70-strike puts trade at an implied volatility of 29%. The 80-strike puts trade at 25%. Expiry is the same." and "Rank today's values, dearest first, for puts struck at £52.00: American, European, and an Asian on the average of the two step prices." Move "list the paths" to the explanation.

## Notes

- `topic-1.7.json` e-bs-hedge part 2 | "four decimal places", key 0.6316 tol 0.0008: 0.632 passes, 0.63 fails with the generic line. | Say "to three decimal places" or widen to 0.0016.
- `l14` screen 4 (theta per day) | Key -0.0158 comes from the exact gamma (-0.01575); the accept line and the stated gamma 0.0198 give -0.0157. | Accept line "-£0.0157 to -£0.0158".
- `l18` screen 1 | "Gamma earns 0.0397" while 0.0099 x 4 = 0.0396; net 0.0239 against 0.0238. Within tol. | "about 0.0397 with exact gamma".
- `l17` screens 3 and 8 | "formula 4.63" for the daily Asian is a moment-matching approximation; a 252-fixing simulation (40,000 paths) gives 4.60. | Say "approximation 4.63" or quote 4.60.
- `l17` screen 5 | "£7.96 on a tree" for the American put against the European 7.9656 (7.97 elsewhere). | "about £7.97".
- `l15` screen 1 wrong key `unscaled-width` 5.325 | Needs a 95/105 spread the screen never asked for; feedback is hard to follow. | Drop it, or key the reversed subtraction.
- Layout, minor | l14 screen 4: the "0.000" tick meets the x-axis ticks; l14 screen 2: "strike 130 / strike 100" labels touch; l17 screens 3 and 9: "strike 100" touches "Average so far". All readable at 440. | Shift or shorten the labels.
- `l16` screen 0 | "Which market charges more for crash protection, the 70 put?" reads oddly. | "Which market charges more for the 70 put, crash protection?"
- `l13` screen 0 | Only the correct option carries numbers (£7.97 to £15.85) and it is the longest. | Move the numbers to the explanation.
- Schema | `course.json` level 4 `requires` lacks `opt-dash/L3` (the author proposed it; l16 and l18 lean on opt-dash l10 and l14). Skills valid, ids unique, ramp sound (lessons 1 to 3, review 2 to 4, homework 3 to 5, exam positions unchanged). | Add `opt-dash/L3` when `course.json` is next touched.

## Checks that passed

- Layout at 440, 1032, 1376 for every canvas and table screen in l13 to l18: no clipped columns other than l13 screen 9, no text under the bottom bar; the l14 sign grid scrolls above the Check bar.
- `--exam topic-1.7` with `--mobile --tablet`: 37 items, 30 of 30.
- Per-cent keys: none in the four exam items (all answers in pounds); the numeric widget divides by 100 only for a `%` unit.
- Wrong answers in the four exam items: every listed slip has its own `byKey` line and tolerances do not overlap the keys (nearest gap 0.0096 on the digital). Unlisted slips fall back to the generic line.
- Pedagogy: objectives met, each lesson has a hook, trap, edge case, follow-up and interviewer-voiced transfer; feedback names the slip.
- Lesson numbers spot-checked (another agent recomputes keys): l13, l14 greeks and calendar, l15 table and pin delta, l16 chances and risk reversal, l17 knock-in 1.4982, l18 price gaps, review-4 and homework-4 including the KO at 99 (0.9646) and the £320 case (1,351.7).
