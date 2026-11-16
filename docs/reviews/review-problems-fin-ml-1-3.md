# Problem sets 2.1, fin-ml levels 1 to 3: second-reader findings

Scope: `app/content/courses/fin-ml/problems-1.json`, `-2`, `-3`: 12 problems, 55 parts (51 numeric, 4 choice), 107 `wrong` entries. Rules: `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md` (Author rules, Reader). Pattern: `review-problems-analysis-1-3.md`.

Method. The author's script was run first. The learner-facing text of l1 to l12, `review-1` to `-3` and `homework-1` to `-3` was printed (`taught.py` in the scratch folder) and read for what each level teaches, its conventions and its settings. Every part was solved by hand from its text, then again in `docs/reports/problems-fin-ml-numbers-read.py`, which imports nothing from the author's script and types every table, window, close and date from the prose. Second routes: exact fractions against floats; the 400 bond windows counted one by one against $409/10$; the fractional weights by the recursion and by $(-1)^k\binom{d}{k}$; `np.convolve(..., mode='same')` and `rolling(4, center=True)` run on a spike; the calendar by `datetime`; pandas for the two rolling z-scores; Kelly by brute maximisation of the log growth; $2\Phi(z) - 1$ against `erf`. Every one of the 107 `wrong` values was rebuilt from the slip its line names, worked both from unrounded values and from the rounded values the part itself states, and each number printed in a feedback or `explain` string was checked. `grade-probe.mjs` puts 102 typed strings through the engine's own `numGrade`. `proposed.py` computes the numbers of every fix below.

Severities: `wrong` = a learner is marked wrongly or told a false number; `misleading` = a line says something loose or untrue, or a slip misses its own feedback; `reuse`; `voice`; `continuity`.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-fin-ml-numbers.py` 598 of 598, exit 0 |
| reader's script | `problems-fin-ml-numbers-read.py` 811 of 821, exit 1: the 10 failing checks are findings 2, 3, 6, 7, 8 and 9 and stay failing until fixed. The copper checks are typed at the present threshold 0.6; the fixer of finding 1 retypes them at 0.55 |
| `review-problems-fin-ml-1-3-scripts/grade-probe.mjs` | 102 rows, 0 failures, 4 FINDING rows (findings 6 to 9), exit 0 |
| `review-problems-fin-ml-1-3-scripts/proposed.py` | ok, exit 0 |
| validator | 0 errors, 4546 warnings, none on the three files; `manifest.json` restored |
| `grade-all.mjs --file`, three sets | 20, 18 and 17 widgets, 0 failures |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --file`, three sets | 0 hits each |
| skills | every `skills` id is carried by a lesson of its level |
| browser | not run (reader rule) |

Result. All 51 typed keys and the 4 choice keys agree with mine. Coverage holds: every lesson of each level is drawn on, typed parts are 51 of 55, each set has a difficulty 5, and nothing beyond the level is needed (the one new call, `np.convolve`, is explained in the part and behaves as it says). One key band takes a slip (finding 7). Three slips miss their own feedback when worked from the values the part prints (6, 8, 9). Four lines are loose or false (2, 3, 4, 9). One problem shares a number pair with `review-1` (1).

## A. `problems-1`

1. `fin-ml/problems-1.json` | `items[1].parts[2]` to `parts[4]` (`p-copper-breakout`) | `reuse` | same base rate and threshold as `review-1`.
   Evidence: `review-1` item 3 reads "Out of 120 primary calls, 50 paid. The secondary model, at threshold 0.6, takes 40 calls", with explain "The primary alone pays $50/120 = 41.7\%$". Here 5 of 12 pay, base rate $5/12 = 0.4167$, and "The desk acts when $p \ge 0.6$". `fresh-check` does not see it (41.7% against 0.4167). The table is new; only the pair repeats.
   Fix: move the threshold to 0.55 (trade 3, $p = 0.58$, is now taken). Numbers in `proposed.py`.
   - `parts[2]`: question "The desk acts when $p \ge 0.55$. What is the precision? Give a decimal to 4 places." `answer` 0.5714, tol 0.0001. `wrong`: `recall` 0.8 (unchanged), `share-taken` 0.5833. `correct`: "Trades 1, 2, 3, 6, 8, 10 and 12 are taken, and 1, 2, 6 and 10 pay: $4/7 = 0.5714$." `recall`: "That is $4/5$, the share of paying calls kept: recall. Precision divides by the 7 trades taken." `share-taken`: "That is $7/12$, the share of trades taken. Of those 7, four paid." `explain`: "Seven trades have $p \ge 0.55$, and four of them have meta-label 1. Precision is $4/7 = 0.5714$, against the base rate of 0.4167."
   - `parts[3]`: question "Using the 5 paying calls from part 1, what is the recall at $p \ge 0.55$? Give a decimal." Key 0.8 and the `price-up` entry stand (trade 5, $p = 0.47$, stays out). `wrong` `precision` value 0.5714; its line: "That is $4/7$, the precision. Recall divides by the 5 calls that paid."
   - `parts[4]`: question "Using precision $\tfrac47$ and recall $\tfrac45$, what is the F1 score? Give a decimal to 4 places." `answer` 0.6667, tol 0.0001 (the decimal route $2 \times 0.5714 \times 0.8/1.3714 = 0.6666$ is inside). `wrong`: `mean` 0.6857, `product` 0.4571. `correct`: "$\frac{2 \times \frac47 \times \frac45}{\frac47 + \frac45} = \frac{32/35}{48/35} = \tfrac23 = 0.6667$." `explain`: "With $P = \tfrac47$ and $R = \tfrac45$, F1 is $\tfrac{32/35}{48/35} = \tfrac{2}{3} = 0.6667$. The filter lifts precision from 0.4167 to 0.5714 and keeps four winners in five."
   None of 0.5714, 0.5833, 0.6857, 0.4571 occurs in the level 1 files.

No other finding on `problems-1`. Checked claims: the 4-day return is exactly 2.0%; £61.90 is under both £61.952 and £61.95; the silver weights are $\tfrac{11}{18}, \tfrac{13}{30}, \tfrac{7}{18}, \tfrac{11}{24}, \tfrac23$ and sum to $\tfrac{307}{120}$; the 400 bond windows cover days 2 to 410 and their uniqueness sums to $\tfrac{409}{10}$ exactly; 57% and 60.5% of 400 are whole rows.

## B. `problems-2`

2. `fin-ml/problems-2.json` | `items[0].parts[1].explain.text` (`p-gold-frac-weights`) | `misleading` | "Each weight is a little over half the one before, so they fade slowly."
   Evidence: the ratios $w_k/w_{k-1}$ are 0.35 ($k = 1$, in size), 0.325, 0.55, 0.6625. Only $w_3$ is "a little over half" of its neighbour, and part 1 has just had the learner use 0.325.
   Fix, the whole `explain`: "The factor is $1.65/3 = 0.55$, and $-0.11375 \times 0.55 = -0.0626$. The factor $(k - 1 - d)/k$ climbs towards 1 as $k$ grows, so the weights fade slowly."

3. `fin-ml/problems-2.json` | `items[1].parts[3].widget.options[0].text` and `.explain.text` (`p-retail-relative-volume`) | `misleading` | "squashing the rest near 0" and "leaves the others evenly spaced".
   Evidence: with the mean 1.17 and sd 0.5729, Raven's z is $-0.93$ and Avocet's $-0.61$: not near 0. What Plover does is put all six others below the mean. The ranks of the others are 1, 2, 3, 4, 5.5, 5.5: the tie of part 2 makes them uneven.
   Fix: option text "Plover's 2.40 lifts the mean and sd, so the other six all score below 0". Last sentence of `explain`: "Plover alone has $z = 2.15$; the rank gives it 1 and spreads the others from 0 to 0.75."

4. `fin-ml/problems-2.json` | `items[2].parts[2].explain.text` (`p-q3-earnings-join`) | `misleading` | "The leak gives Coral its 11% five days early".
   Evidence: the row is Friday 24 October and the first honest row is Thursday 30 October (part 1's explain): 6 calendar days, 4 trading days. Five is the gap to the publication day, which the problem says is not usable. Part 4 then counts 22 early rows.
   Fix, first sentence: "On 24 October the leak shows Coral's 11% four trading days before its first honest row, and its rank moves from 0.6 to 1, the top."

5. `fin-ml/problems-2.json` | `items[2].parts[1].widget.wrong[1].id` and `feedback.byKey` (`p-q3-earnings-join`) | `continuity` | the slip id is `dee-early`.
   Evidence: Dee was the river name the report says was dropped; the company is Jasper. Not shown to a learner, but it is the last trace of the reused names.
   Fix: rename the id to `jasper-early` in `wrong[]`, in `byKey` and in the author's script.

6. `fin-ml/problems-2.json` | `items[3].parts[1].widget.wrong[1]` (`p-shipping-z`, `no-mean`) | `misleading` | the slip misses its line from the unrounded sd.
   Evidence: $25/2.0817 = 12.01$; the band is $12.02 \pm 0.005$, from the rounded 2.08. The probe grades `12.01` wrong with no key. The key itself takes both routes.
   Fix: `value` 12.015, `tol` 0.006 (takes 12.0096, 12.01, 12.0192, 12.02).

Checked: 30 September 2025 is a Tuesday and every weekday in the table is right; 21 weekdays from 1 to 29 October; `mode='same'` with 4 weights reaches 1 day ahead and 2 back, as pandas' centred window of 4 does, and `mode='valid'` returns the part 4 value; the weights sum to 0.474.

## C. `problems-3`

7. `fin-ml/problems-3.json` | `items[2].parts[3].widget` (`p-futures-net-psr`) | `wrong` | the key band takes the `normal` slip.
   Evidence: the `normal` line says "That uses the normal error 0.0366". From that printed value $0.038/0.0366 = 1.038$ and $\Phi = 0.8504$, typed 0.850. The key band is $0.848 \pm 0.002$, and the probe grades `0.850` right. The slip's own band, $0.851 \pm 0.0005$, takes only the unrounded route.
   Fix: key `tol` 0.0015 (still takes 0.8478, 0.8479, 0.8485 and a typed 0.847 to 0.849). `normal`: `value` 0.8505, `tol` 0.0006 (takes 0.850 and 0.851; lower edge 0.8499 is above the key's 0.8495). Its line: "That uses the normal error 0.0366, which gives about 0.850. Skew and kurtosis widen it to 0.0370."

8. `fin-ml/problems-3.json` | `items[2].parts[2].widget.wrong[1]` (`p-futures-net-psr`, `annual`) | `misleading` | the slip misses its line from the value the line names.
   Evidence: "You put the annual 0.60 into the formula." With 0.60 the result is $\sqrt{1.72/749} = 0.04792$, typed 0.0479; the band $0.048 \pm 0.00006$ takes only the unrounded 0.6032 route (0.04800). The probe grades `0.0479` wrong with no key.
   Fix: `value` 0.04795, `tol` 0.00007 (takes 0.04792, 0.0479, 0.0480, 0.04800).

9. `fin-ml/problems-3.json` | `items[3].parts[2]` (`p-calibrated-kelly`) | `misleading` | the working is for a stake the question does not give, and the `even-payout` slip misses its line.
   Evidence: the question fixes the stake at 0.176. Then $1 + 1.8 \times 0.176 = 1.3168$, and the terms are $0.44\ln 1.3168 = 0.1211$ and $0.56\ln 0.824 = -0.1084$. The lines print 1.316, 0.1208 and 0.1081, which belong to the unrounded 0.17556. Both give 0.0127, so the key is safe. For the slip, $0.44\ln 1.176 + 0.56\ln 0.824 = -0.0371$; the band $-0.0369 \pm 0.00006$ takes only the unrounded route, and the probe grades `-0.0371` wrong with no key.
   Fix: `correct`: "$0.44\ln(1.3168) + 0.56\ln(0.824) = 0.1211 - 0.1084 = 0.0127$." `explain`, first sentence: "A win lifts capital to 1.317 times and a loss cuts it to 0.824 times." `even-payout`: `value` $-0.0370$, `tol` 0.00015 (takes $-0.0371$ and $-0.0369$). Part 4 needs no change: from the stated stakes the share is 0.873, inside $0.875 \pm 0.003$, and its line already says "Unrounded".

Checked: the four stated sizes 0.48, 0.38, $-0.21$, $-0.13$; 1.3 units rounded against 1.25 raw; $\Phi^{-1}(0.8) = 0.842$ and $\Phi^{-1}(0.926) = 1.450$; the DSR key takes every route through the stated rounded values (0.9543 to 0.9550); the Kelly formula is the argmax of the log growth at both chances; doubling the raw Kelly gives negative growth, as the option says.

## Reuse read, no finding

Each is the level's standard task with its own numbers; listed so the main session can rule.
- `p-calibrated-kelly` tells the story of l9 screen 8 ("trades scored 0.6 win only 55% of the time") and `review-3` item 8 a third time, here at a 1.80 payout with 0.47 and 0.44.
- `p-five-day-sizing` parts 2 and 3 have the frame of `homework-3` item 3 (five days, a £m book, from flat, bp a side, cost in pounds); positions, book and cost differ.
- `p-trial-log-dsr` part 1 uses the device of `review-3` item 7 (a log with reruns); models and counts differ.
- `p-bond-sign-model` shares average uniqueness 0.1 with `review-1` item 8, and its 57% sits near l4's 57.1%; the roles differ.
- `p-index-fund-day` shares $h = 4$ and $\sqrt 4$ with `homework-1` item 1.

## Chain and bands

Each later part restates the value it uses. Three parts open a second strand and do not use the part before (`p-index-fund-day` part 3, `p-bond-sign-model` part 2, `p-q3-earnings-join` part 4); each feeds the last part or is the result. No `wrong` band meets its key band except as finding 7. `p-bond-sign-model` part 5 measures the edge with the error at $p = 0.605$, as the part says; the error at the null 0.57 would give 0.45.

## Engine

- `fresh-check.mjs` does not match a rate written as a decimal or fraction in one file and as a per cent in another ($5/12 = 0.4167$ here, $50/120 = 41.7\%$ in `review-1`), with the threshold 0.6 beside both (finding 1).
- No tool checks that a `wrong` value is reached from the rounded values the part's own lines print; findings 6 to 9 are all this class, and finding 7 lets the slip into the key band. The reader's `slip()` check is a pattern: each slip worked from stated and from unrounded inputs must land in its band.

## Fix pass

1. fixed (reuse). Copper threshold moved to 0.55; every number recomputed ($4/7 = 0.5714$, share taken $7/12 = 0.5833$, recall 0.8 unchanged, F1 $= 2/3 = 0.6667$, mean 0.6857, product 0.4571). Keys: part 3 0.5714, part 4 0.8, part 5 0.6667, all tol as before. `wrong`: part 3 `recall` 0.8, `share-taken` 0.5833; part 4 `precision` 0.5714, `price-up` 0.75; part 5 `mean` 0.6857, `product` 0.4571.
2. fixed. Gold part 2 `explain` now says the factor $(k - 1 - d)/k$ climbs towards 1.
3. fixed. Retail option text and `explain` reworded (all six others score below 0; ranks spread from 0 to 0.75).
4. fixed. Earnings part 3 `explain` now says four trading days before the first honest row.
5. fixed. Slip id `dee-early` renamed `jasper-early` in `wrong[]`, `byKey` and both scripts.
6. fixed. Shipping part 2 `no-mean` value 12.015, tol 0.006 (key 12.02, tol 0.005 unchanged; 12.0096 to 12.0192 and 12.02 taken).
7. fixed. Futures part 4 key 0.848, tol 0.0015 (band 0.8465 to 0.8495); `normal` 0.8505, tol 0.0006 (band 0.8499 to 0.8511, so a typed 0.850 is refused by the key and routed to `normal`); line now says "which gives about 0.850".
8. fixed. Futures part 3 `annual` value 0.04795, tol 0.00007 (takes 0.04792, 0.0479, 0.0480, 0.04800).
9. fixed by re-authoring (ruled reuse by the main session, a retold story). `p-calibrated-kelly` replaced by `p-power-spread-cap` (power-forward spread, win pays £0.80 per £1, $p = 0.70$, stake cap 0.20, no calibration story). Folds in the old slip `even-payout` and the 1.316 working, as stakes are now stated exactly. Parts, keys and `wrong` values (all recomputed in both scripts):
   - part 1 Kelly $0.70 - 0.30/0.8 = 0.325$, tol 0.0005; `even-odds` 0.4 ($2p - 1$), `times-b` 0.46 ($0.70 - 0.30 \times 0.8$), tol 0.0005.
   - part 2 growth at 0.325: $0.70\ln 1.26 + 0.30\ln 0.675 = 0.1618 - 0.1179 = 0.0439$ (unrounded 0.04387), tol 0.00006; `even-payout` 0.0791 (win as $\ln 1.325$), `swapped` $-0.2058$ (weights 0.30 and 0.70), tol 0.00006.
   - part 3 growth at 0.20: $0.70\ln 1.16 + 0.30\ln 0.8 = 0.1039 - 0.0669 = 0.0370$ (unrounded 0.03695), tol 0.00006; `uncapped` 0.0439, `even-payout` 0.0607 ($\ln 1.2$ for a win), tol 0.00006.
   - part 4 share kept, key 0.843, tol 0.003 (takes 0.8424 unrounded, 0.8428 from 0.0370/0.0439, 0.8434, 0.8405); `inverse` 1.187, `stake-ratio` 0.615 ($0.20/0.325$), tol 0.003.
   - part 5 choice, key `sizing` (the cap sits at sizing, after calibration and before costs, l12's order); three other options each routed.
   Numbers appear nowhere else in `app/content` as a Kelly setting; `fresh-check` 0 hits.
Judged, no finding: the other four reuse likenesses stand (main session ruling).

Gates. Author's `problems-fin-ml-numbers.py` 596 of 596, exit 0; reader's `problems-fin-ml-numbers-read.py` 823 of 823, exit 0 (copper typed at 0.55; Kelly section rewritten). `fresh-check` 0 hits on each of the three sets. Validator 0 errors (manifest restored). Voice scan 35: 0 and 0. `grade-all.mjs --file` 0 failures on each set. `playthrough.mjs --problems fin-ml/problems-1|2|3` with and without `--mobile`: All passed.
