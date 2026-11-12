# Negative-key pass (session AC, task 5)

Content pass for the validator rule `[negative-key]`: 240 widgets listed, 237 given a `wrong[]` entry holding the absolute value of the key, 3 left.

## Counts

- Added: 237 (`wrong[]` entry plus a `feedback.byKey` line each). Id `sign`, or `sign2` (18 items) where `sign` was already used for another value.
- Left: 3.
- Validator: 0 errors; `[negative-key]` count 3 (exactly the items left).
- `grade-all.mjs --local-cdn` over all 191 edited files: every key grades right and every new value grades wrong and routes to its own line. One failure, `markov/l20-when-stopping-fails` screens[5], is one of the ten known pre-existing `wrong-misrouted` cases and is not touched.
- Voice: `voice-scan.py` works per course, so the new feedback lines were checked by script instead: longest sentence 26 words (gate 35), no exclamation marks, no dashes.
- Diff shape: each file shows only added lines apart from the trailing comma on the previous last `wrong` entry and the previous last `byKey` line (unavoidable in JSON).
- New entries copy the `tol` of an existing neighbour whose tolerance equals the widget's own; where none matched they copy the last neighbour's. One such copy overlapped the key (trees/review-4 items[7].parts[0], 0.05 against 0.0005) and was set by hand to the widget's own band.

## Left

1. `sql/l8-daily-volume.json` quiz[3] (key -0.0138): an existing entry, `flipped` 0.014 with `abs` 0.0002, already sits on the absolute value (0.0138 is on its edge). The rule fires on the exact value. No entry added; `flipped` is the sign-flip line, so routing is right.
2. `complex/l13-fourier-pricing.json` screens[10] (key -0.0425): the question asks for the drift correction $\lambda\kappa$, but the explanation says "$-\lambda\kappa \approx +0.0425$ is added to the drift". The sign-dropped value is arguably the amount actually added, so the key or the wording needs a decision from the author. Not edited.
3. `fin-ml/l1-fixed-horizon.json` screens[11] (key -0.00095): the existing `hit` entry (0.001 with `abs` 5e-05) takes 0.00095 on its edge, so a new `sign` entry placed after it is misrouted to `hit`, and placed before it overlaps `hit` (validator warning, rule 581). Fixing it needs `hit`'s band narrowed, which this pass does not do. Left.

## Sign-dropped value that is a second plausible answer

- `limits-thm/l7-bell-curve.json` screens[9] (key -0.02741, "What is r?"): the absolute value 2.74% is the VaR, the quantity the prompt introduces one sentence earlier. Added as `sign2` with a line saying that 2.74% is the VaR and the question asks for r. Worth an author glance: the wording could make a learner who gives the VaR feel misjudged.
- `complex/l13-fourier-pricing` (item 2 above) is the one case where the absolute value may be a correct reading.
- Items where the sign-dropped value was also a stated quantity in the item, with feedback saying so: functions/l1-machines screens[3] (5 is f(1)), vectors/l2-lining-up (1 is the other order of subtraction), stat-learning items (positive growth), research-int/l2 (positive 0.5 is a valid but not smallest correlation), trees/review-4 and trees/l14 (theta magnitude). None is a second right answer as worded.

## Notes for the next author

- Wording such as "drawdown", "VaR" and "distance" can legitimately be quoted as positive numbers elsewhere in the course. In this pass the key is always negative and the question asks for the signed quantity, so the positive value is treated as a slip. Items where the prompt says "use a negative number for a loss" (markets/l12, homework-3, exams topic-1.7) are the cleanest cases.
- Fluency templates were not touched.
