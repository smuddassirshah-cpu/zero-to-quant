# Review: triage of the same-course reuse hits of engine pass AF part 1

Reader of `docs/reports/same-course-reuse-af-hits.md`. No content, engine file or waiver was changed. Both texts of every hit were read in full in the content files, with every matched sentence pair behind the hit (the report shows only the strongest pair of each).

The file lists 94 hits (90 `retold`, 4 `rate`). All 94 have a verdict line below. At this HEAD 93 fire. The 94th, `ensembles/problems-3.json` `p-futures-study` against `l12-trees-on-returns.json:screens[3]`, is closed: its sentence ("Start from the first test row and step back past the gap of 2.") is not in the set at HEAD and the check does not fire. It is counted as `stands` and needs no waiver.

## Verdicts

- `stands`: a false match, or a likeness the rule allows (a given, a definition, a standard instruction or a fact in its only natural words; a standard task in its own setting and numbers). The reason is written for `app/tools/same-course-waivers.json`.
- `reword`: a feedback, explain, why or stem line told again from a lesson, review, homework item or other set. Exact replacements follow the line. Every key, number and `wrong` value is unchanged, and each printed number was recomputed.
- `re-author`: the problem (or the named parts) walks a taught screen or item, or shares a number set. It goes to an author; no replacement is given.

## Count

| course | stands | reword | re-author | total |
|---|---|---|---|---|
| analysis | 1 | 1 |  | 2 |
| complex | 1 | 1 |  | 2 |
| conditional | 1 | 3 | 2 | 6 |
| counting | 1 |  |  | 1 |
| eigen | 1 |  |  | 1 |
| elimination | 1 |  |  | 1 |
| ensembles | 1 | 6 |  | 7 |
| equations | 6 |  |  | 6 |
| exp-log | 1 |  | 2 | 3 |
| fin-ml | 2 |  |  | 2 |
| functions |  | 1 |  | 1 |
| integrals | 4 | 1 |  | 5 |
| least-squares | 3 |  |  | 3 |
| limits | 1 |  |  | 1 |
| limits-thm | 2 | 1 |  | 3 |
| markov | 2 | 1 | 1 | 4 |
| number-sense | 1 |  |  | 1 |
| proof | 1 |  |  | 1 |
| quadratics |  | 1 |  | 1 |
| ratio | 3 | 1 |  | 4 |
| regression | 2 |  |  | 2 |
| stat-learning | 3 | 2 | 5 | 10 |
| taylor | 2 | 1 |  | 3 |
| testing | 6 | 3 |  | 9 |
| trig | 1 | 3 |  | 4 |
| validation |  | 1 | 1 | 2 |
| vector-calc | 3 |  |  | 3 |
| vectors | 1 | 5 |  | 6 |
| **all** | **51** | **32** | **11** | **94** |

Of the reword lines 5 need no edit of their own (the other side of a pair is reworded), and of the re-author lines 3 repeat an item already listed. So a fixer edits 21 sets (47 strings, three of them held in two fields), and an author takes 8 items in 7 sets.

Sets with a re-author verdict: `conditional/problems-3` (`p-losing-week`), `conditional/problems-4` (`p-dated-coins`), `exp-log/problems-1` (`p-rare-coin`, numbers shared with `exp-log/problems-2` `p-drawdown-recovery`), `markov/problems-5` (`p-capped-close`), `stat-learning/problems-2` (`p-futures-lasso`, `p-built-ridge`), `stat-learning/problems-4` (`p-renewals` part 2), `validation/problems-1` (`p-arrears-grid` parts 4 and 5).

## Check of the replacements

All 47 replacements were applied in the worktree (50 fields in 21 sets) and `node tools/fresh-check.mjs --file <set>` was run on each edited set: 15 sets exit clean, and no `retold` or `rate` error is left on a reworded string. A full rescan without waivers falls from 93 hits to 62.
The 13 error lines left in the other 6 sets (`integrals/problems-1`, `ratio/problems-3`, `stat-learning/problems-1`, `taylor/problems-1`, `testing/problems-1`, `trig/problems-2`) are all `stands` lines below; one of them is the rule line of `p-subscriptions`, now reported against `l3-signed-area.json:screens[4]` in place of `quiz[1]`. The content was then restored with `git checkout`; the numbers the replacements print were recomputed from each part's answer and `wrong` values.

## Waivers

A waiver is keyed by file, item and kind, so it also covers any later `retold` hit on the item. Where an item has both a `stands` line and a `reword` or `re-author` line (`integrals/problems-1` `p-subscriptions`, `testing/problems-1` `p-cereal-boxes`), apply the rewording first and waive after. The 50 `stands` lines that fire fall on 35 items.

## Hits by set

One line per hit: set | item and part (as the hits file numbers it) | field of the strongest pair | verdict | source | reason. Replacements are indented under their line: field, then the old text, then the new text.

### analysis/problems-1.json

- `analysis/problems-1.json` | `p-diagonal-fraction` (items[2], part 1) | parts[0].feedback.byKey.diagonal | **reword** | `l5-counting-infinite-sets.json:quiz[3]` | the feedback tells the quiz lines again (the copied diagonal digits; the rule changes each one)
  - `items[2].parts[0].feedback.byKey.diagonal`
    - old: `You copied the diagonal digits $7, 8, 5, 5, 8$. The rule changes each one: 5 where the digit is not 5, and 4 where it is.`
    - new: `$7, 8, 5, 5, 8$ are the list's own digits, read down the diagonal. Each digit of $x$ must differ from them: 5 where the list has no 5, and 4 where it has.`
  - `items[2].parts[0].feedback.correct (first sentence)`
    - old: `The diagonal digits are $7, 8, 5, 5, 8$, so $x$ starts $0.55445$.`
    - new: `Down the diagonal the list reads $7, 8, 5, 5, 8$, so $x$ starts $0.55445$.`

### analysis/problems-4.json

- `analysis/problems-4.json` | `p-bump-series` (items[2], part 4) | parts[3].widget.options[0].text | **stands** | `l19-uniform-convergence.json:screens[9]` | stands: the theorem (a uniform limit of continuous functions is continuous) in its only natural words, as an option and its feedback

### complex/problems-1.json

- `complex/problems-1.json` | `p-four-lamps` (items[2], part 1) | parts[1].feedback.correct | **reword** | `problems-2.json:items[2]` | the feedback of parts 1 and 2 is the feedback of `problems-2` `p-log-branches` parts 1 and 2 line for line (8 sentences); six lines of part 2 reworded here, `problems-2` untouched
  - `items[2].parts[1].feedback.correct`
    - old: `$c$ is in the second quadrant. Its reference angle, the acute angle to the real axis, is $\tfrac{\pi}{3}$, so $\operatorname{Arg} c = \pi - \tfrac{\pi}{3} = \tfrac{2\pi}{3}$.`
    - new: `$c$ lies in the second quadrant, at the acute angle $\tfrac{\pi}{3}$ to the negative real axis. So $\operatorname{Arg} c = \pi - \tfrac{\pi}{3} = \tfrac{2\pi}{3}$.`
  - `items[2].parts[1].feedback.generic`
    - old: `Not quite. Plot $c$ first: its real part is negative and its imaginary part positive.`
    - new: `Not quite. Plot $c$ first: it sits left of the imaginary axis and above the real axis.`
  - `items[2].parts[1].feedback.byKey.arctan`
    - old: `That is $\arctan(-\sqrt3)$, which points into the fourth quadrant. $c$ has a negative real part, so it lies in the second quadrant.`
    - new: `$\arctan(-\sqrt3)$ lands below the real axis, on the right. $c$ has a negative real part, so it lies in the second quadrant.`
  - `items[2].parts[1].feedback.byKey.reference`
    - old: `That is the reference angle. $c$ is in the second quadrant, so the argument is $\pi - \tfrac{\pi}{3}$.`
    - new: `That is the reference angle. Measure from the positive real axis instead: $\pi - \tfrac{\pi}{3}$.`
  - `items[2].parts[1].feedback.byKey.swapped`
    - old: `You used the real part over the imaginary part, which gives a reference angle of $\tfrac{\pi}{6}$. The tangent is $\sqrt3$, so the reference angle is $\tfrac{\pi}{3}$.`
    - new: `$\tfrac{5\pi}{6}$ comes from the ratio upside down, $\tfrac{1}{\sqrt3}$, an acute angle of $\tfrac{\pi}{6}$. Imaginary over real has size $\sqrt3$, an acute angle of $\tfrac{\pi}{3}$.`
  - `items[2].parts[1].explain.text (second sentence)`
    - old: `With the real part negative and the imaginary part positive, $\operatorname{Arg} c = \tfrac{2\pi}{3}$.`
    - new: `$c$ is up and to the left of 0, so $\operatorname{Arg} c = \pi - \tfrac{\pi}{3} = \tfrac{2\pi}{3}$.`

### complex/problems-2.json

- `complex/problems-2.json` | `p-mesh-map` (items[0], part 3) | parts[2].feedback.generic | **stands** | `l6-complex-differentiability.json:screens[4]` | stands: the taught fact that the stretch is the modulus of the derivative, said in two fields; own function and point

### conditional/problems-2.json

- `conditional/problems-2.json` | `p-bad-ticks` (items[3], part 3) | parts[2].feedback.byKey.skipped-a | **reword** | `problems-5.json:items[0]` | the same diagnosis pair for the same slip as `problems-5` `p-warning-screen`
  - `items[3].parts[2].feedback.byKey.skipped-a`
    - old: `You started from the 2% base rate. After A's flag the starting chance is 0.3265.`
    - new: `You started from the 2% base rate. Filter B only sees prints that A flagged, and 0.3265 of those are errors.`

### conditional/problems-3.json

- `conditional/problems-3.json` | `p-losing-week` (items[1], part 3) | parts[2].feedback.byKey.still | **re-author** | `l16-conditional-independence.json:quiz[2]` | the whole item walks the lesson in other nouns. It must not walk `l16-conditional-independence.json:screens[7]` and `screens[8]` (an event with two independent causes, "or both"; the event happens; then one cause is confirmed and the other falls back) nor `quiz[2]` (a fund loses on a bad call or a crash). Part 4's explain line "Conditioning on a shared effect can make independent causes dependent, as it does here." is `quiz[2]`'s explain word for word

### conditional/problems-4.json

- `conditional/problems-4.json` | `p-two-strategies` (items[1], part 2) | parts[1].feedback.byKey.own | **stands** | `homework-4.json:items[0]` | stands: false match, "That is the chance B wins" against a Monty Hall line; nothing shared
- `conditional/problems-4.json` | `p-dated-coins` (items[3], part 1) | parts[0].question | **re-author** | `l19-bertrands-box.json:screens[5]` | the setting is the lesson's boxes of gold and silver coins. It must not walk `l19-bertrands-box.json:screens[5]` (a fourth box, a gold coin drawn, "the chance the other coin is gold"), `screens[7]` (someone looks inside and reports at least one gold coin), nor `l21-tuesday-boy.json:screens[4]` to `screens[8]` (a detail with $k$ equally likely values and its limit as $k$ grows); `homework-4.json:items[2]` already varies the boxes

### conditional/problems-5.json

- `conditional/problems-5.json` | `p-warning-screen` (items[0], part 3) | parts[2].feedback.byKey.slip | **reword** | `problems-2.json:items[3]` | no edit here: cleared by the replacement in `conditional/problems-2.json` `p-bad-ticks`
- `conditional/problems-5.json` | `p-doubling-desk` (items[3], part 1) | prose | **reword** | `review-5.json:items[5]` | the stem sentence is the rule sentence of `review-5.json:items[5]` (and of `l22-gamblers-fallacy.json:screens[9]`), and part 1 asks their question in their words. Part 1 repeats the lesson's computation as a first step, which stands as a standard task; parts 2 to 4 (survivors and quitters) are its own
  - `items[3].prose`
    - old: `In a round a trader stakes £1, doubles after each loss, and stops at the first win or after five losses in a row.`
    - new: `A round opens with a £1 stake, and every losing bet doubles the next stake. The round is over at the first winning bet, or once five bets running have lost.`
  - `items[3].parts[0].question`
    - old: `What is the expected profit of one round, in pounds? Give your answer to the nearest penny.`
    - new: `On average, how much does one round make, in pounds? Give your answer to the nearest penny.`

### counting/problems-3.json

- `counting/problems-3.json` | `p-grain-merchant` (items[2], part 4) | parts[3].feedback.generic | **stands** | `l13-portfolio-vector.json:quiz[2]` | stands: the angle recipe (dot product over both magnitudes, then the inverse cosine) as a standard instruction; own vectors

### eigen/problems-3.json

- `eigen/problems-3.json` | `p-branch-sales` (items[0], part 1) | parts[0].question | **stands** | `homework-3.json:items[1]` | stands: false match on "the off-diagonal entry"; own matrix

### elimination/problems-2.json

- `elimination/problems-2.json` | `p-burning-ethanol` (items[0], part 3) | parts[2].question | **stands** | `l6-inputs-to-zero.json:quiz[0]` | stands: "the special solution" is the term of art; own matrix and setting

### ensembles/problems-1.json

- `ensembles/problems-1.json` | `p-spoof-alerts` (items[0], part 1) | parts[2].question | **reword** | `l2-good-split.json:screens[0]` | one feedback line of `screens[11]` ("The gain is how far it fell from ..."); the other three matched sentences are a given, the standard question and a stock slip
  - `items[0].parts[3].feedback.byKey.child`
    - old: `0.289 is what the split leaves. The gain is how far it fell from 0.42.`
    - new: `0.289 is what the split leaves. Take it from the root's 0.42.`
- `ensembles/problems-1.json` | `p-opening-gaps` (items[3], part 2) | parts[1].feedback.byKey.child | **reword** | `l2-good-split.json:screens[11]` | the `child` and `unweighted` feedback lines of parts 2 to 4 follow `screens[11]`'s byKey lines
  - `items[3].parts[1].feedback.byKey.child`
    - old: `0.267 is the weighted impurity left after the split. The gain is its drop from 0.48.`
    - new: `0.267 is the Gini of the two sides, weighted by size. The gain is what the split took off the parent's 0.48.`
  - `items[3].parts[2].feedback.byKey.child`
    - old: `0.317 is the weighted impurity left after the split. Subtract it from 0.48.`
    - new: `0.317 is the Gini of the two sides, weighted by size. Subtract it from 0.48.`
  - `items[3].parts[3].feedback.byKey.child`
    - old: `0.551 is the weighted entropy left after the split. The gain is its drop from 0.971.`
    - new: `0.551 is the entropy of the two sides, weighted by size. Take it from the root's 0.971.`
  - `items[3].parts[1].feedback.byKey.unweighted`
    - old: `You averaged the two sides equally. The right side holds 6 of the 10 mornings.`
    - new: `You gave both sides the same weight. The right side holds 6 of the 10 mornings.`
  - `items[3].parts[2].feedback.byKey.unweighted`
    - old: `You averaged the two sides equally. Weight them by 6 and 4 mornings.`
    - new: `You gave both sides the same weight. Weight them by 6 and 4 mornings.`

### ensembles/problems-2.json

- `ensembles/problems-2.json` | `p-ipo-forest` (items[1], part 1) | parts[0].feedback.byKey.one | **reword** | `l6-random-forest.json:screens[5]` | the `one` feedback line is `screens[5]`'s byKey.one with the fraction changed
  - `items[1].parts[0].feedback.byKey.one`
    - old: `$\tfrac{1}{10}$ is the chance with one feature on offer. Three are on offer.`
    - new: `$\tfrac{1}{10}$ would be right if a split drew a single feature. Here each split draws three of the 10.`

### ensembles/problems-3.json

- `ensembles/problems-3.json` | `p-callable-bonds` (items[1], part 1) | parts[0].feedback.byKey.rate | **reword** | `homework-3.json:items[4]` | the diagnosis pair of `homework-3.json:items[4]` byKey.p
  - `items[1].parts[0].feedback.byKey.rate`
    - old: `0.25 is the base rate itself. Boosting works on the log-odds scale.`
    - new: `0.25 is the base rate itself. $F_0$ is its log-odds, $\ln\tfrac{0.25}{0.75}$.`
- `ensembles/problems-3.json` | `p-callable-bonds` (items[1], part 2) | parts[1].feedback.byKey.p | **reword** | `review-3.json:items[4]` | the feedback line of `review-3.json:items[4]` byKey.p; "The tree fits minus the slope." beside it is the taught rule and stays
  - `items[1].parts[1].feedback.byKey.p`
    - old: `0.25 is the bond's current probability, not how far it is from the outcome.`
    - new: `0.25 is $p$ itself. The target is the gap $y - p$, and a called bond has $y = 1$.`
- `ensembles/problems-3.json` | `p-callable-bonds` (items[1], part 5) | parts[4].explain.text | **reword** | `l9-fixing-mistakes.json:screens[8]` | the explain sentence of `screens[8]`
  - `items[1].parts[4].explain.text (last sentence)`
    - old: `Summing on the log-odds scale keeps $p$ between 0 and 1 however many trees follow.`
    - new: `The logistic curve turns any total log-odds, however many trees add to it, into a probability strictly between 0 and 1.`
- `ensembles/problems-3.json` | `p-futures-study` (items[2], part 1) | none at HEAD | **stands** | `l12-trees-on-returns.json:screens[3]` | stands: closed, the sentence "Start from the first test row and step back past the gap of 2." is not in the set at HEAD and the check does not fire; no waiver needed

### equations/problems-3.json

- `equations/problems-3.json` | `p-bakery-stock` (items[0], part 2) | parts[1].feedback.correct | **stands** | `l11-one-twist.json:quiz[3]` | stands: the rule that dividing by a negative reverses the sign, in its only natural words, said in three fields; own inequality
- `equations/problems-3.json` | `p-bakery-stock` (items[0], part 2) | parts[1].feedback.correct | **stands** | `l12-trapped.json:screens[8]` | stands: the rule that dividing by a negative reverses the sign, in its only natural words, said in three fields; own inequality
- `equations/problems-3.json` | `p-bakery-stock` (items[0], part 2) | parts[1].feedback.correct | **stands** | `review-3.json:items[1]` | stands: the rule that dividing by a negative reverses the sign, in its only natural words, said in three fields; own inequality
- `equations/problems-3.json` | `p-van-value` (items[2], part 3) | parts[2].feedback.correct | **stands** | `l11-one-twist.json:quiz[3]` | stands: the rule that dividing by a negative reverses the sign, in its only natural words, said in three fields; own inequality
- `equations/problems-3.json` | `p-van-value` (items[2], part 3) | parts[2].feedback.correct | **stands** | `l12-trapped.json:screens[8]` | stands: the rule that dividing by a negative reverses the sign, in its only natural words, said in three fields; own inequality
- `equations/problems-3.json` | `p-van-value` (items[2], part 3) | parts[2].feedback.correct | **stands** | `review-3.json:items[1]` | stands: the rule that dividing by a negative reverses the sign, in its only natural words, said in three fields; own inequality

### exp-log/problems-1.json

- `exp-log/problems-1.json` | `p-laptop-value` (items[1], part 2) | parts[1].feedback.correct | **stands** | `problems-2.json:items[2]` (rate) | stands: 0.75 squared is 0.5625, a two-year decay factor, against a 56.25% gain; different quantities, a chance match
- `exp-log/problems-1.json` | `p-rare-coin` (items[2], part 1) | parts[0].feedback.byKey.rise | **re-author** | `problems-2.json:items[2]` (rate) | a shared number set, not a line: 640 to 1,000 here and 32,000 to 50,000 in `problems-2` `p-drawdown-recovery` are the same ratio, so both items turn on the factor $1.5625 = 1.25^2$ (and 0.64). Renumber this item, the simpler of the two: it must not use a two-period factor of 1.5625 or 0.64, nor the yearly factor 1.25

### exp-log/problems-2.json

- `exp-log/problems-2.json` | `p-drawdown-recovery` (items[2], part 2) | parts[1].feedback.correct | **re-author** | `problems-1.json:items[2]` (rate) | no edit here: cleared when `exp-log/problems-1.json` `p-rare-coin` is renumbered (the shared factor $1.5625 = 1.25^2$)

### fin-ml/problems-3.json

- `fin-ml/problems-3.json` | `p-power-spread-cap` (items[3], part 1) | parts[0].question | **stands** | `l9-probability-to-position.json:screens[3]` | stands: the standard Kelly question in its own payout and probability; parts 2 to 5 are its own
- `fin-ml/problems-3.json` | `p-power-spread-cap` (items[3], part 1) | parts[0].question | **stands** | `review-3.json:items[1]` | stands: the standard Kelly question in its own payout and probability; parts 2 to 5 are its own

### functions/problems-4.json

- `functions/problems-4.json` | `p-photo-mount` (items[0], part 1) | parts[0].feedback.byKey.order | **reword** | `l16-machine-after-machine.json:screens[2]` | the `order` feedback line is `screens[2]`'s byKey.swap in other letters
  - `items[0].parts[0].feedback.byKey.order`
    - old: `That is $e(m(12)) = 1.5 \times 16$: you mounted first. In $m(e(12))$ the inner machine $e$ acts first.`
    - new: `That is $e(m(12)) = 1.5 \times 16$: you mounted first. The shop enlarges before it mounts, so start with $e(12) = 18$.`

### integrals/problems-1.json

- `integrals/problems-1.json` | `p-subscriptions` (items[1], part 4) | parts[3].feedback.correct | **stands** | `homework-1.json:items[4]` | stands: the rule that reversing the limits flips the sign, in its only natural words, said in two fields
- `integrals/problems-1.json` | `p-subscriptions` (items[1], part 4) | parts[3].feedback.correct | **reword** | `l3-signed-area.json:quiz[1]` | the explain sentence paraphrases `quiz[1]`'s explain. After the reword the hit still fires on the rule line alone, which stands: the rule that reversing the limits flips the sign, in its only natural words, said in two fields
  - `items[1].parts[3].explain.text (first sentence)`
    - old: `Running from 5 down to 0 makes every width $\Delta t$ negative.`
    - new: `Each strip now has width $-\Delta t$, because $t$ steps from 5 back to 0.`
- `integrals/problems-1.json` | `p-subscriptions` (items[1], part 4) | parts[3].feedback.byKey.no-flip | **stands** | `l7-evaluating.json:screens[5]` | stands: the rule that reversing the limits flips the sign, in its only natural words, said in two fields

### integrals/problems-2.json

- `integrals/problems-2.json` | `p-area-function` (items[0], part 3) | parts[2].feedback.correct | **stands** | `l6-working-backwards.json:quiz[0]` | stands: the reverse power rule and its stock slip (dividing by the old power) as standard instructions; own polynomial
- `integrals/problems-2.json` | `p-line-and-parabola` (items[2], part 2) | parts[1].feedback.generic | **stands** | `l8-between-curves.json:screens[4]` | stands: top minus bottom between the crossings, the standard instruction; own curves

### least-squares/problems-2.json

- `least-squares/problems-2.json` | `p-dye-mix` (items[3], part 3) | parts[2].feedback.generic | **stands** | `homework-1.json:items[5]` | stands: the definition of an entry of Q^T b (a column of Q dotted with b), said in two fields; own vectors
- `least-squares/problems-2.json` | `p-dye-mix` (items[3], part 3) | parts[2].feedback.generic | **stands** | `l10-normal-equations.json:screens[0]` | stands: the definition of an entry of Q^T b (a column of Q dotted with b), said in two fields; own vectors
- `least-squares/problems-2.json` | `p-dye-mix` (items[3], part 3) | parts[2].feedback.generic | **stands** | `review-1.json:items[2]` | stands: the definition of an entry of Q^T b (a column of Q dotted with b), said in two fields; own vectors

### limits-thm/problems-1.json

- `limits-thm/problems-1.json` | `p-dropped-ticks` (items[0], part 5) | parts[4].feedback.correct | **stands** | `l2-first-success.json:screens[7]` | stands: false match on "the mean wait is"; own alarm setting
- `limits-thm/problems-1.json` | `p-settlement-checks` (items[3], part 2) | parts[1].feedback.byKey.binomial | **stands** | `review-1.json:items[7]` | stands: the finite population factor $(N - n)/(N - 1)$ stated as the standard fact; own numbers

### limits-thm/problems-2.json

- `limits-thm/problems-2.json` | `p-digital-share` (items[1], part 1) | parts[0].explain.text | **reword** | `l8-lognormal.json:screens[2]` | the first two explain sentences follow `screens[2]`'s explain ("Half of ... lies below", "The median passes straight through the exponential")
  - `items[1].parts[0].explain.text (first two sentences)`
    - old: `Half of $Z$ lies below 0, so half of $S_1$ lies below $80e^{0.015}$. The median passes straight through the exponential: $80e^{0.015} \approx \text{£}81.21$.`
    - new: `$Z$ is below 0 exactly half the time, and $S_1$ rises with $Z$. So the median of $S_1$ is its value at $Z = 0$: $80e^{0.015} \approx \text{£}81.21$.`

### limits/problems-5.json

- `limits/problems-5.json` | `p-camera-pan` (items[0], part 1) | parts[0].feedback.generic | **stands** | `l19-running-backwards.json:screens[7]` | stands: the arctan chain-rule formula in words; own function

### markov/problems-1.json

- `markov/problems-1.json` | `p-carry-pause` (items[3], part 1) | parts[0].feedback.byKey.used-stay | **reword** | `problems-2.json:items[3]` | the same diagnosis pair as `problems-2` `p-merger-arb` byKey.over-stay
  - `items[3].parts[0].feedback.byKey.used-stay`
    - old: `You divided by the chance of staying, 0.7. Divide by the chance of leaving, 0.3.`
    - new: `0.7 is the chance a stressed month is followed by another. A spell ends each month with chance 0.3, so its mean length is $\tfrac{1}{0.3}$ months.`

### markov/problems-3.json

- `markov/problems-3.json` | `p-barrier-note` (items[1], part 1) | parts[0].feedback.byKey.end-minus-two | **stands** | `l8-which-end.json:screens[7]` | stands: false match: the shared words are "That is" and "ending at"

### markov/problems-5.json

- `markov/problems-5.json` | `p-signal-trial` (items[1], part 2) | parts[1].question | **stands** | `review-5.json:items[1]` | stands: the standard question for the exponential martingale; own walk and stakes
- `markov/problems-5.json` | `p-capped-close` (items[3], part 2) | parts[1].explain.text | **re-author** | `l20-when-stopping-fails.json:quiz[0]` | parts 1, 2 and 5 walk the lesson with 100 bets cut to 4 days. It must not walk `l20-when-stopping-fails.json:screens[4]` (cap the time, stop when up 1 or at the cap, the failing chance by the reflection count $\binom{n}{n/2}/2^n$, the average loss on failing from $E[S_T] = 0$), `quiz[0]` (a fair strategy stopped when up or after $n$ trades, "whichever comes first") nor `quiz[3]` (no cap: the walk reaches $+1$ with chance 1). Parts 3 and 4 ($E[T]$ and the sd from $S_n^2 - n$) are its own and may stay

### number-sense/problems-3.json

- `number-sense/problems-3.json` | `p-comet-probe` (items[2], part 2) | parts[1].explain.text | **stands** | `l13-estimate-first.json:quiz[0]` | stands: "the first significant figure" is the term of art; own number

### proof/problems-3.json

- `proof/problems-3.json` | `p-even-test-contra` (items[3], part 1) | parts[0].widget.options[1].text | **stands** | `problems-2.json:items[0]` | stands: false match on "is a multiple of"

### quadratics/problems-3.json

- `quadratics/problems-3.json` | `p-bike-hire` (items[1], part 4) | parts[3].explain.text | **reword** | `review-3.json:items[9]` | the last explain sentence is `review-3.json:items[9]`'s closing line with the pounds changed; part 4 itself is the standard task in its own numbers
  - `items[1].parts[3].explain.text (last sentence)`
    - old: `The cost raised the best price by £4, half of £8.`
    - new: `Without the cost the best price was £15, so the £8 cost moves it up by only £4.`

### ratio/problems-1.json

- `ratio/problems-1.json` | `p-pension-split` (items[0], part 1) | parts[0].feedback.correct | **stands** | `l1-out-of-a-hundred.json:screens[9]` (rate) | stands: a single common fraction, 3/8 (DECISIONS session AC)

### ratio/problems-3.json

- `ratio/problems-3.json` | `p-print-run` (items[1], part 1) | parts[0].feedback.byKey.direct | **reword** | `l11-direct-or-inverse.json:quiz[1]` | the `direct` feedback pair is `quiz[1]`'s byKey.direct with presses for servers
  - `items[1].parts[0].feedback.byKey.direct`
    - old: `You scaled the time up with the presses. More presses finish sooner: this is inverse proportion.`
    - new: `30 hours is twice the time for twice the presses. Twice the presses share the same work in half the time: this is inverse proportion.`
- `ratio/problems-3.json` | `p-coffee-suppliers` (items[2], part 3) | parts[2].feedback.byKey.multiplied | **stands** | `l13-currencies.json:screens[0]` | stands: restates the given rate ("each pound buys €1.20") and concludes the opposite operation
- `ratio/problems-3.json` | `p-coffee-suppliers` (items[2], part 3) | parts[2].feedback.byKey.multiplied | **stands** | `review-3.json:items[1]` | stands: restates the given rate ("each pound buys €1.20") and concludes the opposite operation

### regression/problems-2.json

- `regression/problems-2.json` | `p-grocer-beta` (items[3], part 1) | parts[0].question | **stands** | `problems-3.json:items[2]` | stands: the standard question for $s$ and the standard divisor hint; own data, and the chain differs after the $t$ statistic

### regression/problems-3.json

- `regression/problems-3.json` | `p-overlap-signal` (items[2], part 1) | parts[0].question | **stands** | `problems-2.json:items[3]` | stands: the standard question for $s$ and the standard divisor hint; own data, and the chain differs after the $t$ statistic

### stat-learning/problems-1.json

- `stat-learning/problems-1.json` | `p-ferry-passengers` (items[0], part 5) | parts[4].widget.options[1].why, parts[4].feedback.byKey.polynomial | **stands** | `l2-training-error-lies.json:screens[7]` | stands: one four-word diagnosis ("You chose by training error.") held in `why` and `byKey`; the reason after it is its own
- `stat-learning/problems-1.json` | `p-ferry-passengers` (items[0], part 5) | parts[4].widget.options[1].why, parts[4].feedback.byKey.polynomial | **stands** | `review-4.json:items[5]` | stands: one four-word diagnosis ("You chose by training error.") held in `why` and `byKey`; the reason after it is its own
- `stat-learning/problems-1.json` | `p-loaves-k` (items[1], part 3) | parts[2].feedback.byKey.no-noise | **reword** | `l3-bias-variance.json:quiz[1]` | the `no-noise` feedback pair is `quiz[1]`'s byKey.nonoise
  - `items[1].parts[2].feedback.byKey.no-noise`
    - old: `That is bias squared plus variance alone. Add the noise variance, 4.`
    - new: `You left out the noise. Each day's sales scatter about 20 with variance 4, whatever the forecast, so add 4.`
- `stat-learning/problems-1.json` | `p-broker-clients` (items[2], part 4) | parts[4].feedback.generic | **reword** | `problems-2.json:items[0]` | four feedback lines of parts 4 and 5 are those of `problems-2` `p-ice-cream-van` parts 3 and 4 with clients for days
  - `items[2].parts[4].feedback.generic`
    - old: `Not quite. Forecast 5.5 for each held-out client, square the misses, then average.`
    - new: `Not quite. All three held-out clients get the forecast 5.5, and the test MSE is the mean of their three squared errors.`
  - `items[2].parts[3].feedback.byKey.sum and items[2].parts[4].feedback.byKey.sum`
    - old: `That is the sum of the squared misses. Divide by the 3 clients.`
    - new: `You added the squared misses but did not average them. Divide by the 3 clients.`
  - `items[2].parts[4].feedback.byKey.test-mean`
    - old: `You used the held-out clients' own mean. It was not known when the forecasts were made; the baseline is the training mean, 5.5.`
    - new: `1.722 comes from the mean of the three held-out commissions. That was not known when the forecasts were made; the baseline is the training mean, 5.5.`
- `stat-learning/problems-1.json` | `p-heat-demand` (items[3], part 1) | parts[0].feedback.correct | **stands** | `l2-training-error-lies.json:quiz[1]` | stands: choose the lowest test MSE, the standard instruction; own table, and parts 2 to 5 are its own

### stat-learning/problems-2.json

- `stat-learning/problems-2.json` | `p-futures-lasso` (items[2], part 1) | parts[0].feedback.generic | **re-author** | `review-2.json:items[3]` | the item is a tour of taught screens in new coefficients. It must not walk `review-2.json:items[3]` (five uncorrelated z-scored OLS coefficients, `Lasso(alpha=0.15)`, count the survivors: same alpha, same count of features, same key 3), `l8-setting-to-zero.json:screens[1]` (one coefficient after the penalty) and `screens[8]` (the smallest alpha that empties the model), nor `l9-scale-first.json:screens[2]` (standardise with the training mean and sd). Copied feedback lines to drop: "A coefficient survives when its size is above $\alpha = 0.15$.", "You expected ridge's behaviour.", "The penalty always pulls towards 0.", "You added the sizes. The model is empty once $\alpha$ reaches the largest one.", "Subtract the training mean, then divide by the training standard deviation."
- `stat-learning/problems-2.json` | `p-futures-lasso` (items[2], part 2) | parts[2].feedback.byKey.sum | **re-author** | `l8-setting-to-zero.json:screens[1]` | same item as the line above, one re-authoring
- `stat-learning/problems-2.json` | `p-futures-lasso` (items[2], part 4) | parts[3].feedback.generic | **re-author** | `l9-scale-first.json:screens[2]` | same item as the two lines above, one re-authoring
- `stat-learning/problems-2.json` | `p-built-ridge` (items[3], part 1) | prose | **re-author** | `homework-2.json:items[4]` | the stem is `homework-2.json:items[4]` sentence by sentence, and the task is its task. It must not walk that item: "a market we built", uncorrelated z-scored features with true coefficients and a noise variance, OLS estimates on $n$ rows, "expected test MSE is the noise plus the sum of squared coefficient errors", ridge shrinking by $n/(n + \lambda)$

### stat-learning/problems-4.json

- `stat-learning/problems-4.json` | `p-renewals` (items[3], part 2) | parts[1].widget.options[1].why, parts[1].feedback.byKey.network | **re-author** | `l19-which-learner.json:quiz[1]` | part 2 only. It must not walk `l19-which-learner.json:quiz[1]` (logistic regression ties on validation with a more flexible learner, an RBF SVM in the field, and the tie goes to the simpler). Its `why` line follows the quiz's explain ("the extra flexibility bought nothing", "the tie goes to"). Parts 1, 3 and 4 may stay; part 3 asks `screens[4]`'s standard question in its own numbers

### taylor/problems-1.json

- `taylor/problems-1.json` | `p-newton-cubic` (items[1], part 3) | parts[2].widget.options[3].why | **stands** | `l8-convexity.json:quiz[3]` | stands: the convexity fact (a curve that bends up lies above its tangent) in its natural words; own function
- `taylor/problems-1.json` | `p-loss-limit` (items[2], part 1) | parts[0].feedback.byKey.par | **reword** | `problems-2.json:items[2]` | four feedback lines of part 1 are those of `problems-2` `p-eight-coupon` part 1 with the rate changed
  - `items[2].parts[0].feedback.byKey.par`
    - old: `A bond is at par only when its coupon rate equals its yield. A 3% coupon at a 4% yield prices below £100.`
    - new: `£100 would need the coupon rate to match the yield. A 3% coupon at a 4% yield prices below £100.`
  - `items[2].parts[0].feedback.byKey.no-discount`
    - old: `You added the cash flows without discounting them. Each £$c_t$ is worth $c_t/1.04^t$ today.`
    - new: `£112 is the four payments at face value. Each £$c_t$ is worth $c_t/1.04^t$ today.`
  - `items[2].parts[0].feedback.byKey.face-only`
    - old: `You discounted only the final £103. The three earlier coupons are worth $3/1.04 + 3/1.04^2 + 3/1.04^3$ as well.`
    - new: `£88.04 is the last payment alone, $103/1.04^4$. The three earlier coupons are worth $3/1.04 + 3/1.04^2 + 3/1.04^3$ as well.`

### taylor/problems-3.json

- `taylor/problems-3.json` | `p-doubling-coefficients` (items[0], part 2) | parts[1].feedback.byKey.radius | **stands** | `homework-3.json:items[7]` | stands: false match on "the ratio tends to"

### testing/problems-1.json

- `testing/problems-1.json` | `p-cereal-boxes` (items[0], part 1) | parts[0].widget.options[2].why, parts[0].feedback.byKey.swapped | **reword** | `l1-could-be-luck.json:screens[6]` | the `swapped` line is `screens[6]`'s option text ("must fix ... one value so that surprise can be measured")
  - `items[0].parts[0].widget.options[2].why and items[0].parts[0].feedback.byKey.swapped`
    - old: `A null must fix one value of $\mu$, so that surprise can be measured. The officer's suspicion goes in $H_1$.`
    - new: `This pair is the wrong way round. The test asks how odd 743.1 g would be if $\mu$ were exactly 750, so $\mu = 750$ is the null.`
- `testing/problems-1.json` | `p-cereal-boxes` (items[0], part 5) | parts[4].widget.options[2].why, parts[4].feedback.byKey.accept | **stands** | `l3-p-value.json:screens[4]` | stands: the maxim that failing to reject is not proof, one sentence held in `why` and `byKey`
- `testing/problems-1.json` | `p-phone-battery` (items[1], part 2) | parts[2].feedback.byKey.root-seven | **reword** | `problems-2.json:items[2]` | the feedback of parts 2 and 3 follows `problems-2` `p-running-shoes` parts 2 and 3 line for line
  - `items[1].parts[2].feedback.byKey.root-seven`
    - old: `You divided $s$ by $\sqrt 7$. The curve has 7 degrees of freedom, but the standard error uses $\sqrt n = \sqrt 8$.`
    - new: `You divided $s$ by $\sqrt 7$. The 7 only picks which $t$ curve to read. The standard error is $\tfrac{2}{\sqrt 8}$.`
  - `items[1].parts[1].feedback.generic`
    - old: `Not quite. Square each deviation from 18, add them, divide by 7, then take the square root.`
    - new: `Not quite. The eight squared deviations from 18 add to 28. Divide by 7, then take the root.`
  - `items[1].parts[2].feedback.byKey.over-s`
    - old: `You divided by $s$ itself. The mean of 8 phones has standard error $\tfrac{s}{\sqrt 8}$.`
    - new: `You divided by $s$ itself. Averaging 8 phones shrinks the spread, so divide by $\tfrac{s}{\sqrt 8}$.`
- `testing/problems-1.json` | `p-pizza-delivery` (items[3], part 3) | parts[2].feedback.byKey.over-s | **stands** | `l15-sharpness-of-the-peak.json:quiz[0]` | stands: false match on "the standard error is"
- `testing/problems-1.json` | `p-pizza-delivery` (items[3], part 4) | parts[3].widget.options[3].why, parts[3].feedback.byKey.accept | **stands** | `l3-p-value.json:screens[4]` | stands: the maxim that failing to reject is not proof, one sentence held in `why` and `byKey`

### testing/problems-3.json

- `testing/problems-3.json` | `p-fund-managers` (items[1], part 2) | parts[1].feedback.generic | **stands** | `l3-p-value.json:screens[8]` | stands: "the upper tail beyond" is the standard phrase for a one-sided p-value
- `testing/problems-3.json` | `p-fund-managers` (items[1], part 3) | parts[2].feedback.byKey.bonferroni | **stands** | `homework-3.json:items[2]` | stands: the BH rule (the largest rank under its bar) in its usual words; own p-values and bars
- `testing/problems-3.json` | `p-fund-managers` (items[1], part 3) | parts[2].feedback.byKey.bonferroni | **stands** | `l10-correcting.json:quiz[0]` | stands: the BH rule (the largest rank under its bar) in its usual words; own p-values and bars

### testing/problems-4.json

- `testing/problems-4.json` | `p-bakery-loaves` (items[2], part 5) | parts[4].widget.options[2].why, parts[4].feedback.byKey.five-df | **reword** | `l17-ratio-of-likelihoods.json:quiz[0]` | the `five-df` line borrows `quiz[0]`'s hint ("count the parameters the null removes"); $5 - 3 = 2$ is the table's own count and stays
  - `items[2].parts[4].widget.options[2].why and items[2].parts[4].feedback.byKey.five-df`
    - old: `Five is the number of free shares in the full model. Wilks counts the parameters the null removes: $5 - 3 = 2$.`
    - new: `Five is the number of free shares in the full model. Independence still leaves 3 of them free, so the statistic has $5 - 3 = 2$ degrees of freedom.`

### trig/problems-2.json

- `trig/problems-2.json` | `p-water-wheel` (items[0], part 4) | parts[3].feedback.correct | **stands** | `l11-every-angle.json:screens[10]` | stands: the mirror in the vertical axis is the standard description of $180^\circ - x$; own wheel
- `trig/problems-2.json` | `p-two-buoys` (items[1], part 1) | parts[0].feedback.generic | **reword** | `l9-stretching-a-wave.json:screens[8]` | the generic hint and the first explain sentence are the prose sentence of `screens[8]`
  - `items[1].parts[0].feedback.generic`
    - old: `Not quite. One wave is drawn while the angle runs from 0 to $2\pi$.`
    - new: `Not quite. Find how long the angle $\tfrac{\pi t}{5}$ takes to grow by $2\pi$.`
  - `items[1].parts[0].explain.text (first two sentences)`
    - old: `One wave is drawn while the angle $\tfrac{\pi t}{5}$ runs from 0 to $2\pi$. That happens while $t$ runs from 0 to 10.`
    - new: `The angle $\tfrac{\pi t}{5}$ must grow by $2\pi$ for one full wave. That takes $t$ from 0 to 10.`
- `trig/problems-2.json` | `p-observation-wheel` (items[2], part 1) | parts[0].feedback.byKey.diameter | **reword** | `problems-3.json:items[2]` | the same diagnosis pair as `problems-3` `p-daylight-model` byKey.range. Both items fit $a$, $b$, $c$ in that order, which stands as the standard modelling task
  - `items[2].parts[0].feedback.byKey.diameter`
    - old: `That is the whole swing from bottom to top. The amplitude is the swing either side of the hub: half of 50.`
    - new: `50 m is the diameter, the full climb from boarding to the top. The amplitude is the radius, half of 50.`

### trig/problems-3.json

- `trig/problems-3.json` | `p-daylight-model` (items[2], part 1) | parts[0].feedback.byKey.range | **reword** | `problems-2.json:items[2]` | no edit here: cleared by the replacement in `trig/problems-2.json` `p-observation-wheel`

### validation/problems-1.json

- `validation/problems-1.json` | `p-arrears-grid` (items[2], part 2) | parts[3].question | **re-author** | `l4-nested.json:screens[11]` | parts 4 and 5 only. They must not walk `l4-nested.json:screens[11]` (the grid's best CV MSE against the nested score, "by what percentage of the nested score does the best number flatter the model", then what the model card reports). Part 2's line "You left out the 4 refits, one per outer fold." is `quiz[3]`'s; parts 1 to 3 may stay

### validation/problems-2.json

- `validation/problems-2.json` | `p-forward-label` (items[1], part 3) | parts[2].question | **reword** | `homework-2.json:items[2]` | the feedback of part 3 follows `homework-2.json:items[2]` line for line; the count itself is the standard task in its own numbers, and the question sentence stays
  - `items[1].parts[2].feedback.generic`
    - old: `Not quite. Remove the block, 14 rows on each side, then the 29-row embargo.`
    - new: `Not quite. Start from 1,260 and take off the 140-row block, both purges of 14 and the embargo of 29.`
  - `items[1].parts[2].feedback.byKey.block-only`
    - old: `1,120 removes only the test block. The overlapping labels and the embargo go too.`
    - new: `1,120 is $1260 - 140$, the test block alone. The overlapping labels and the embargo go too.`
  - `items[1].parts[2].feedback.byKey.horizon`
    - old: `You purged 15 rows a side. A 15-day label overlaps on 14.`
    - new: `1,061 purges the full horizon, 15 rows, on each side. A 15-day label overlaps on 14.`

### vector-calc/problems-3.json

- `vector-calc/problems-3.json` | `p-open-tank` (items[1], part 2) | parts[1].feedback.generic | **stands** | `l11-divergence-theorem.json:screens[1]` | stands: "use the divergence theorem" is the standard instruction; own field and box
- `vector-calc/problems-3.json` | `p-open-tank` (items[1], part 2) | parts[1].feedback.generic | **stands** | `l12-stokes.json:screens[10]` | stands: "use the divergence theorem" is the standard instruction; own field and box
- `vector-calc/problems-3.json` | `p-open-tank` (items[1], part 2) | parts[1].feedback.generic | **stands** | `review-3.json:items[3]` | stands: "use the divergence theorem" is the standard instruction; own field and box

### vectors/problems-1.json

- `vectors/problems-1.json` | `p-charging-robot` (items[0], part 3) | parts[2].feedback.generic | **stands** | `l3-lengths-angles.json:screens[4]` | stands: the angle recipe (dot product over both lengths, then the inverse cosine) as a standard instruction; own vectors

### vectors/problems-2.json

- `vectors/problems-2.json` | `p-italic-letters` (items[0], part 3) | parts[2].feedback.byKey.entrywise | **reword** | `problems-3.json:items[2]` | the `entrywise` pair is shared word for word with `problems-3` `p-colour-sensor` and `p-engraver-dial`
  - `items[0].parts[2].feedback.byKey.entrywise`
    - old: `You multiplied matching entries. Each entry of a product is a row of $\mathbf{D}$ dotted with a column of $\mathbf{S}$.`
    - new: `That is the entry-by-entry product, which is not the matrix product. Work along a row of $\mathbf{D}$ and down a column of $\mathbf{S}$.`
- `vectors/problems-2.json` | `p-italic-letters` (items[0], part 3) | parts[2].feedback.byKey.entrywise | **reword** | `l8-identity-transpose.json:screens[4]` | no further edit: cleared by the same replacement; the explain sentence left is the definition of a product entry

### vectors/problems-3.json

- `vectors/problems-3.json` | `p-goat-feed` (items[0], part 3) | parts[2].feedback.byKey.no-divide | **reword** | `l10-undoing.json:screens[6]` | the `no-divide` line is `screens[6]`'s `why` with the determinant put in
  - `items[0].parts[2].feedback.byKey.no-divide`
    - old: `You swapped and negated but did not divide by $\det\mathbf{A} = 0.1$. Dividing multiplies each entry by 10.`
    - new: `The entries sit in the right places, but the factor $\tfrac{1}{\det\mathbf{A}} = \tfrac{1}{0.1}$ is missing. Multiply every entry by 10.`
- `vectors/problems-3.json` | `p-colour-sensor` (items[2], part 1) | parts[0].feedback.byKey.entrywise | **reword** | `problems-2.json:items[0]` | no edit here: cleared by the replacement in `vectors/problems-2.json` `p-italic-letters`
- `vectors/problems-3.json` | `p-engraver-dial` (items[3], part 1) | parts[0].feedback.byKey.entrywise | **reword** | `problems-2.json:items[0]` | no edit here: cleared by the replacement in `vectors/problems-2.json` `p-italic-letters`

## The detector

On this evidence the `retold` kind is too loose on short lines and not too tight. Of the 93 hits that fire, 50 stand (54%) and 43 are reuse (46%): 32 reword lines and 11 re-author lines. The true hits are worth having: cloned feedback blocks between two sets of a course (`complex`, `taylor`, `testing`, `vectors`, `stat-learning`) and seven items that walk a taught screen. Weight does not separate the two groups. A standing recipe line scores 6.5 (`counting/problems-3` `p-grain-merchant`) and a retold lesson line 2.3 (`ratio/problems-3` `p-print-run`). The kind of sentence separates them.

Commonest false-positive patterns (the same bullets are in `docs/BACKLOG-INBOX.md` under `Raised later (triage AF hits):`):

- One sentence counted as two, about half of the stands. The same string sits in `widget.options[].why` and `feedback.byKey` of a choice part, or one rule is said in `correct`, `generic` and `explain`, and each copy pairs with the same single source sentence. Count distinct pairs.
- A rule or recipe in its only words, about half of the stands and overlapping the first. "Dividing by $-18$ reverses the sign", "reversing the limits flips the sign", "use the divergence theorem". These are stock inside one course and rare across the app, so the app-wide stock list misses them. Learn stock per course.
- A match made by the masking alone, 7 hits. With numbers, maths and rare nouns masked, the skeleton left is "That is ..., the ... ending at ..." or "the standard error is". Ask for three informative words in common.

Also raised: the error line shows one pair of a hit where a fixer needs all of them; a waiver has no source field, so it hides later hits on its item; the `rate` kind found one real shared number set (`exp-log`) that the `numbers` kind missed, and two chance matches; the hits file holds one hit that does not fire at HEAD.

## Fix pass

Fixer: Sonnet, from the triage above. Replacements applied exactly as written, mechanically (`apply.mjs` from the reader's scratch, read first): all 47 old strings were found, each once (the three held in two fields matched in both), and every file re-parsed as JSON. No key, number or `wrong` value changed, so no graded answer changed. Nothing deferred.

Reword hits (33 lines, 32 hits; the `p-italic-letters` line appears twice):
- analysis/problems-1 `p-diagonal-fraction`: fixed (2 strings)
- complex/problems-1 `p-four-lamps`: fixed (6 strings)
- conditional/problems-2 `p-bad-ticks`: fixed
- conditional/problems-5 `p-warning-screen`: fixed (cleared by the `p-bad-ticks` replacement, no edit of its own)
- conditional/problems-5 `p-doubling-desk`: fixed (2 strings)
- ensembles/problems-1 `p-spoof-alerts` and `p-opening-gaps`: fixed (6 strings across both)
- ensembles/problems-2 `p-ipo-forest`: fixed
- ensembles/problems-3 `p-callable-bonds` parts 1, 2, 5: fixed (3 strings)
- functions/problems-4 `p-photo-mount`: fixed
- integrals/problems-1 `p-subscriptions`: fixed (waived afterwards for its `stands` line)
- limits-thm/problems-2 `p-digital-share`: fixed
- markov/problems-1 `p-carry-pause`: fixed
- quadratics/problems-3 `p-bike-hire`: fixed
- ratio/problems-3 `p-print-run`: fixed
- stat-learning/problems-1 `p-loaves-k`, `p-broker-clients`: fixed (4 strings)
- taylor/problems-1 `p-loss-limit`: fixed (3 strings)
- testing/problems-1 `p-cereal-boxes`, `p-phone-battery`: fixed (6 strings; the first waived afterwards)
- testing/problems-4 `p-bakery-loaves`: fixed
- trig/problems-2 `p-two-buoys`, `p-observation-wheel`: fixed (3 strings)
- trig/problems-3 `p-daylight-model`: fixed (cleared by the `p-observation-wheel` replacement, no edit of its own)
- validation/problems-2 `p-forward-label`: fixed (3 strings)
- vectors/problems-2 `p-italic-letters` (both lines): fixed (one `entrywise` string)
- vectors/problems-3 `p-goat-feed`: fixed (`no-divide`); `p-colour-sensor`, `p-engraver-dial`: cleared by the `vectors/problems-2` `entrywise` replacement, no edit of their own

Waivers: 35 entries added to `app/tools/same-course-waivers.json` (status "stands", the reader's reason), one per item and kind. The 36th `stands` item, `ensembles/problems-3` `p-futures-study`, no longer fires and has none. The 11 `re-author` hits are untouched and unwaived.

Errors left in `node tools/same-course-reuse.mjs --all`: 11, exactly the `re-author` hits: `conditional/problems-3` `p-losing-week`; `conditional/problems-4` `p-dated-coins`; `exp-log/problems-1` `p-rare-coin` and `exp-log/problems-2` `p-drawdown-recovery` (shared numbers); `markov/problems-5` `p-capped-close`; `stat-learning/problems-2` `p-futures-lasso` (parts 1, 2, 4) and `p-built-ridge`; `stat-learning/problems-4` `p-renewals`; `validation/problems-1` `p-arrears-grid`.

Gates: validator 0 errors; voice scan 35 on the 16 edited courses 0 over-long explanations and 0 long sentences in every edited file (one over-35 line, `testing/homework-3.json`, is not an edited file and predates this pass); `grade-all.mjs --file` 0 failures on all 21 sets; `test-fresh-check.mjs`, `test-fresh-check-same-course-ae.mjs`, `test-fresh-check-retold-af.mjs` pass.
`playthrough.mjs --problems` with and without `--mobile` on all 21 edited sets: All passed (the first mobile run of `ensembles/problems-3` and the first runs of `vectors/problems-3` hit my own shell timeout, not a content failure; rerun with a longer limit, all passed). Number scripts of the 16 edited courses (`docs/reports/problems-<course>-numbers*.py`, through `run-number-scripts.mjs --only`): all pass, 0 new failures.
