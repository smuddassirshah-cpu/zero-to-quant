# Triage: band warnings and self-grade notes (session AB)

Scope: every `[tight-band]` and `[wide-wrong-band]` warning of `node tools/validate.mjs` and every authored answer that `node tools/grade-regression.mjs` notes as not grading correct itself, at commit `4d3459d`. Counts seen: 149, 36, 257 (tight-band, wide-wrong-band, self-grade notes). The self-grade count has moved from the 198 of session AA; a grader pass is running on another branch, so the count is tied to this commit.

Method: `triage-bands-ab-scripts/` opens each item and grades probe answers with the real grader (`js/engine/grade.js` and the numeric and expression widgets, loaded as `grade-regression.mjs` loads them, Compute Engine from the local `pkgs`). Probes: the answer as stored; the answer rounded as asked; one unit either side; the figure the text prints; every other `wrong[]` value; 0. For pile 3 each fluency family is drawn 40 times with `js/engine/gen.js` and the realised answer, accept forms and wrong values are graded. A verdict comes from the probe where it settles the case, and from a hand reading of the item otherwise (tables `P1` and `P2` in `classify.mjs`). Every proposed fix is applied to a copy of the widget and graded again. No content or engine file was edited.

Verdicts: `content fault` (a right answer in the form asked is marked wrong, or a wrong one right); `harmless` (the rule fires, no sensible answer is misgraded); `tool limit` (the rule or tool misreads the item).

## Summary

| Pile | Entries | content fault | harmless | tool limit |
|---|---|---|---|---|
| 1. `[tight-band]` | 149 | 8 | 81 | 60 |
| 2. `[wide-wrong-band]` | 36 | 0 | 34 | 2 |
| 3. `grade-regression` self-grade notes | 257 | 0 | 0 | 257 |
| Total | 442 | 8 | 115 | 319 |

By class:

| Class | Verdict | Pile | Entries | What it is |
|---|---|---|---|---|
| H1 | harmless | 1 | 68 | half-unit band: the answer rounded as asked is accepted and the item's printed working lands on it |
| H2 | harmless | 1 | 13 | the explanation prints fewer places than the question asks; the form asked is accepted |
| H3 | harmless | 2 | 32 | a small slip value with an absolute band: only that slip, rounded as asked, falls inside |
| H4 | harmless | 2 | 2 | a deliberate catch-all band (any huge number, any small positive number) |
| T1 | tool limit | 1 | 24 | the printed figure is one of the item's own wrong[] values (a slip the text names) |
| T2 | tool limit | 1 | 20 | the printed figure is the value before a whole-number round-up or round-down |
| T3 | tool limit | 1 | 3 | the printed figure is followed by \ldots: it is the unrounded working |
| T4 | tool limit | 1 | 10 | the last "=" or "\approx" belongs to another quantity (a step, a check, the exact value beside an estimate) |
| T5 | tool limit | 1 | 1 | a "{,}" thousands separator is read as the end of the number |
| T6 | tool limit | 1 | 2 | "whole number" in the prose describes the thing picked, not the form of the answer |
| T7 | tool limit | 2 | 2 | the band counted is the grader's float slack (1e-9 absolute, 1e-12 relative), not the authored tol |
| T8 | tool limit | 3 | 256 | a fluency family template ("{key}") is graded as if it were the answer |
| T9 | tool limit | 3 | 1 | a carried value ("{{carry.name}}") is graded as if it were the answer |
| F1 | content fault | 1 | 6 | right answer marked wrong: the item's own printed figure is refused |
| F2 | content fault | 1 | 2 | right answer marked wrong: a working with rounded figures lands one unit out |

Content faults: 8 entries on 7 items, all in pile 1 and all "right answer marked wrong". By course or exam: conditional 1, regression 1, cpp-pricing 2, alpha 1, exams/stage-3 2. No wrong answer is marked right anywhere in the three piles.

## Content faults, with the fix

- `conditional/review-5.json` `items[4].widget` (r-low-prior): explain.text prints 0.46, refused; no form is asked (placeholder "fraction or decimal"); the explanation gives $\tfrac{6}{13} \approx 0.46$. Fix: `"tol": {"abs":0.005}` (was `{"abs":0.0005}`); with it the grader takes 0.46, 6/13, 0.4615, 0.462 and the 2 wrong values keep their own lines.
- `regression/l5-how-sure.json` `quiz[3].widget` (q-month-sd): feedback.correct prints 0.25, refused; no form is asked; the feedback gives $6 / 23.66 = 0.25$. Fix: `"tol": {"abs":0.005}` (was `{"abs":0.003}`); with it the grader takes 0.25, 0.254, 0.2535 and the 2 wrong values keep their own lines.
- `cpp-pricing/l6-binomial-cpp.json` `quiz[1].widget` (q-one-step): explain.text prints 11.9, refused; asked "in pounds"; the explanation and the accept line both give £11.90. Fix: `"tol": {"abs":0.005}` (was `{"abs":0.001}`); with it the grader takes 11.90, 11.9, 11.9048 and the 2 wrong values keep their own lines.
- `cpp-pricing/review-2.json` `items[1].widget` (r-one-step-put): explain.text prints 3.92, refused; asked "in pounds"; the whole of feedback.correct is "£3.92.". Fix: `"tol": {"abs":0.005}` (was `{"abs":0.001}`); with it the grader takes 3.92, 3.9216 and the 2 wrong values keep their own lines.
- `alpha/l7-ranks-and-z.json` `quiz[3].widget` (q4): feedback.correct prints 2.47, refused; no form is asked; feedback.correct and explain.text both end "= 2.47". Fix: `"tol": {"abs":0.005}` (was `{"abs":0.002}`); with it the grader takes 2.47, 2.475, 2.4749 and the wrong value keeps its own line.
- `exams/stage-3.json` `parts[2].items[7].parts[0].widget` (r-t-bar): 2.75 accepted, 2.76 and 2.74 refused; two places asked, no working printed; a standard error kept to three places (3.1/sqrt(360) = 0.163) gives 0.45/0.163 = 2.76. Fix: `"tol": {"abs":0.01}` (was `{"abs":0.005}`); with it the grader takes 2.76, 2.75 and the 2 wrong values keep their own lines.
- `exams/stage-3.json` `parts[2].items[11].widget` (r-best-of-twenty): 0.23 accepted, 0.24 and 0.22 refused; two places asked and the answer 0.225156 sits on the rounding edge; tables at z = 2.24 give 1 - 0.9875^20 = 0.2224, so 0.22; the explanation's own 1 - 0.775 = 0.225 also rounds either way. Fix: `"tol": {"abs":0.006}` (was `{"abs":0.005}`); with it the grader takes 0.22, 0.23, 0.225 and the 2 wrong values keep their own lines.

## Entries

One line per entry: pile, file, path, item id (or family), verdict and class, evidence. A fix is given only for a content fault.

### alpha (3)

- P1 `review-1.json` `items[8].widget` (r-trail) | tool limit T2 | explain.text prints 26.7, then rounds to the whole number 27, which is accepted
- P1 `l7-ranks-and-z.json` `quiz[3].widget` (q4) | content fault F1 | feedback.correct prints 2.47, refused; no form is asked; feedback.correct and explain.text both end "= 2.47" | fix: `"tol": {"abs":0.005}` (was `{"abs":0.002}`); with it the grader takes 2.47, 2.475, 2.4749 and the wrong value keeps its own line
- P1 `l7-ranks-and-z.json` `quiz[3].widget` (q4) | content fault F1 | explain.text prints 2.47, refused; no form is asked; feedback.correct and explain.text both end "= 2.47" | fix: `"tol": {"abs":0.005}` (was `{"abs":0.002}`); with it the grader takes 2.47, 2.475, 2.4749 and the wrong value keeps its own line

### analysis (6)

- P1 `l4-archimedes.json` `quiz[2].widget` (q-third-half) | harmless H2 | feedback.correct prints 0.4286, refused; a fraction is asked; 3/7 accepted
- P1 `homework-1.json` `items[2].widget` (h-root-eps-num) | tool limit T1 | feedback.correct prints 100, the wrong value "equal"; the answer 101 is accepted
- P1 `homework-1.json` `items[2].widget` (h-root-eps-num) | tool limit T1 | explain.text prints 100, the wrong value "equal"; the answer 101 is accepted
- P1 `l12-convergence-tests.json` `quiz[1].widget` (q-n-over-2n) | tool limit T4 | explain.text prints 1.9883, refused; 1.9883 is the check value S_10
- P1 `review-3.json` `items[7].widget` (r-integral-mid) | tool limit T4 | feedback.correct prints 1.64493, refused; 1.64493 is pi^2/6, set beside the estimate 1.64497
- P1 `review-3.json` `items[7].widget` (r-integral-mid) | tool limit T4 | explain.text prints 1.644934, refused; 1.64493 is pi^2/6, set beside the estimate 1.64497

### backtest (2)

- P2 `l12-benchmark.json` `screens[3].widget.wrong[0]` (l12-benchmark) | harmless H3 | slip "daily" 0.0165 has band [-0.0035, 0.0365] %; the answer 4.17 grades correct and the other slip keeps its own line; a typed 0 gets this line
- P2 `review-3.json` `items[3].widget.wrong[0]` (r-alpha) | harmless H3 | slip "daily" 0.012 has band [-0.008, 0.032] %; the answer 3.024 grades correct and the other slip keeps its own line; a typed 0 gets this line; the answer typed as a decimal in the per cent field (0.03024) lands in this band and is told "that is alpha per day"; it is marked wrong either way

### bank (1)

- P1 `probability-2.json` `items[8].widget` (duels-weaker-shoots-first) | harmless H2 | explain.text prints 0.52, refused; four places or a fraction asked; 0.5172 and 15/29 accepted

### brainteasers (1)

- P2 `review-2.json` `items[2].widget.wrong[1]` (r3-twelve-prisoners) | harmless H3 | slip "random" 0.0002 has band [0, 0.0004]; the answer 0.3468 grades correct and the other slip keeps its own line; a typed 0 gets this line

### complex (3)

- P3 `fluency-l2-points-in-a-plane.json` `families[2].widget` (principal-argument) | tool limit T8 | template "\\frac{{{p:c}\\pi}}{{{q}}}"; 40 draws of family "principal-argument": every realised answer grades correct, as do 40 accept forms; none of 36 wrong values grades correct
- P3 `fluency-l2-points-in-a-plane.json` `families[1].widget` (distance) | tool limit T8 | template "{r}"; 40 draws of family "distance": every realised answer grades correct, and the answer rounded as asked (40); none of 120 wrong values grades correct
- P3 `fluency-l2-points-in-a-plane.json` `families[0].widget` (modulus) | tool limit T8 | template "{r}"; 40 draws of family "modulus": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct

### conditional (7)

- P1 `review-5.json` `items[4].widget` (r-low-prior) | content fault F1 | explain.text prints 0.46, refused; no form is asked (placeholder "fraction or decimal"); the explanation gives $\tfrac{6}{13} \approx 0.46$ | fix: `"tol": {"abs":0.005}` (was `{"abs":0.0005}`); with it the grader takes 0.46, 6/13, 0.4615, 0.462 and the 2 wrong values keep their own lines
- P2 `homework-3.json` `items[1].widget.wrong[1]` (h-no-losing-month) | harmless H3 | slip "all" 5e-7 has band [0, 0.000001]; the answer 0.01384 grades correct and the other slip keeps its own line; a typed 0 gets this line
- P2 `l23-prosecutors-fallacy.json` `screens[2].widget.wrong[0]` (l23-prosecutors-fallacy) | harmless H3 | slip "swap" 0.000001 has band [5e-7, 0.0000015]; the answer 0.8333 grades correct and the other 2 slips keep their own lines
- P2 `problems-2.json` `items[3].parts[4].widget.wrong[0]` (p-bad-ticks) | harmless H3 | slip "over-all" 0.0004 has band [0.0002, 0.0006]; the answer 0.0286 grades correct and the other 2 slips keep their own lines
- P3 `fluency-l7-turning-around.json` `families[2].widget` (every-positive-path) | tool limit T8 | template "{key}"; 40 draws of family "every-positive-path": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-turning-around.json` `families[1].widget` (from-rates) | tool limit T8 | template "{key}"; 40 draws of family "from-rates": every realised answer grades correct, and the answer rounded as asked (40); none of 120 wrong values grades correct
- P3 `fluency-l7-turning-around.json` `families[0].widget` (from-counts) | tool limit T8 | template "{key}"; 40 draws of family "from-counts": every realised answer grades correct; none of 80 wrong values grades correct

### counting (7)

- P3 `fluency-l3-choosing-in-order.json` `families[0].widget` (evaluate-p) | tool limit T8 | template "{key}"; 40 draws of family "evaluate-p": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l4-choosing-without-order.json` `families[1].widget` (evaluate-binomial) | tool limit T8 | template "{key}"; 40 draws of family "evaluate-binomial": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l4-choosing-without-order.json` `families[0].widget` (pairs) | tool limit T8 | template "{key}"; 40 draws of family "pairs": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-choosing-in-order.json` `families[2].widget` (factorial-quotient) | tool limit T8 | template "{key}"; 40 draws of family "factorial-quotient": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l4-choosing-without-order.json` `families[3].widget` (up-down-patterns) | tool limit T8 | template "{key}"; 40 draws of family "up-down-patterns": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-choosing-in-order.json` `families[1].widget` (awards) | tool limit T8 | template "{key}"; 40 draws of family "awards": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l4-choosing-without-order.json` `families[2].widget` (committee) | tool limit T8 | template "{key}"; 40 draws of family "committee": every realised answer grades correct; none of 80 wrong values grades correct

### counting-chance (8)

- P1 `review-2.json` `items[7].widget` (r-flush) | harmless H2 | explain.text prints 0.0005, refused; a fraction is asked; 33/66640 accepted
- P1 `l9-double-counting.json` `quiz[1].widget` (q-two-or-five) | tool limit T6 | the rule rounds 0.6 to 1; no rounding is asked; the answer 0.6 is accepted
- P1 `l9-double-counting.json` `quiz[2].widget` (q-two-three-five) | tool limit T6 | the rule rounds 0.7333 to 1; no rounding is asked; 0.7333 and 11/15 are accepted
- P2 `l11-axioms.json` `screens[10].widget.wrong[2]` (l11-axioms) | harmless H3 | slip "all" 1e-27 has band [-9.999999e-21, 1.0000001e-20]; the answer 0.02 grades correct and the other 2 slips keep their own lines; a typed 0 gets this line
- P2 `problems-2.json` `items[3].parts[1].widget.wrong[0]` (p-feed-audit) | harmless H3 | slip "no-others" 0.0000702 has band [0.0000202, 0.0001202]; the answer 0.021052 grades correct and the other slip keeps its own line
- P3 `fluency-l7-replacement.json` `families[2].widget` (three-without) | tool limit T8 | template "{key}"; 40 draws of family "three-without": every realised answer grades correct; none of 78 wrong values grades correct
- P3 `fluency-l7-replacement.json` `families[1].widget` (two-with) | tool limit T8 | template "{key}"; 40 draws of family "two-with": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-replacement.json` `families[0].widget` (two-without) | tool limit T8 | template "{key}"; 40 draws of family "two-without": every realised answer grades correct; none of 80 wrong values grades correct

### cpp-pricing (3)

- P1 `l6-binomial-cpp.json` `quiz[1].widget` (q-one-step) | content fault F1 | explain.text prints 11.9, refused; asked "in pounds"; the explanation and the accept line both give £11.90 | fix: `"tol": {"abs":0.005}` (was `{"abs":0.001}`); with it the grader takes 11.90, 11.9, 11.9048 and the 2 wrong values keep their own lines
- P1 `review-2.json` `items[1].widget` (r-one-step-put) | content fault F1 | explain.text prints 3.92, refused; asked "in pounds"; the whole of feedback.correct is "£3.92." | fix: `"tol": {"abs":0.005}` (was `{"abs":0.001}`); with it the grader takes 3.92, 3.9216 and the 2 wrong values keep their own lines
- P1 `homework-2.json` `items[6].widget` (h-bisection-steps) | tool limit T2 | explain.text prints 28.9, then rounds to the whole number 29, which is accepted

### eigen (3)

- P2 `l16-correlated-normals.json` `screens[4].widget.wrong[2]` (l16-correlated-normals) | harmless H3 | slip "half" 0.0001 has band [-0.0009, 0.0011]; the answer 0.0212 grades correct and the other 2 slips keep their own lines; a typed 0 gets this line
- P3 `fluency-l2-characteristic.json` `families[2].widget` (eigenvector) | tool limit T8 | template "{key}"; 40 draws of family "eigenvector": every realised answer grades correct; none of 73 wrong values grades correct
- P3 `fluency-l2-characteristic.json` `families[1].widget` (both-eigenvalues) | tool limit T8 | template ["{l1}","{l2}"]; 40 draws of family "both-eigenvalues": every realised answer grades correct; none of 80 wrong values grades correct

### elimination (3)

- P3 `fluency-l10-computing-dets.json` `families[0].widget` (cofactors-row-one) | tool limit T8 | template "{key}"; 40 draws of family "cofactors-row-one": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l10-computing-dets.json` `families[2].widget` (pivots-and-swaps) | tool limit T8 | template "{key}"; 40 draws of family "pivots-and-swaps": every realised answer grades correct; none of 66 wrong values grades correct
- P3 `fluency-l10-computing-dets.json` `families[1].widget` (row-operations) | tool limit T8 | template "{key}"; 40 draws of family "row-operations": every realised answer grades correct; none of 120 wrong values grades correct

### ensembles (2)

- P1 `homework-2.json` `items[1].widget` (hw-how-many-trees) | tool limit T2 | explain.text prints 161.8, then rounds to the whole number 162, which is accepted
- P2 `homework-2.json` `items[0].widget.wrong[0]` (hw-no-oob) | harmless H3 | slip "miss" 0.045 has band [-0.005, 0.095]; the answer 10.2 grades correct and the other slip keeps its own line; a typed 0 gets this line

### equations (14)

- P1 `review-2.json` `items[9].widget` (rv-newsletter) | tool limit T1 | feedback.correct prints 78.125, the wrong value "unrounded"; the answer 79 is accepted
- P1 `review-2.json` `items[9].widget` (rv-newsletter) | tool limit T1 | explain.text prints 78.125, the wrong value "unrounded"; the answer 79 is accepted
- P1 `homework-2.json` `items[3].widget` (hw-exit-price) | tool limit T1 | explain.text prints 3.864, the wrong value "unrounded"; the answer 3.87 is accepted
- P1 `homework-2.json` `items[4].widget` (hw-commission-budget) | tool limit T1 | explain.text prints 313.78, the wrong value "unrounded"; the answer 314 is accepted
- P1 `problems-2.json` `items[0].parts[3].widget` (p-climbing-wall) | tool limit T3 | feedback.correct prints 7.2857, refused; asked for whole pence; 7.28 accepted
- P1 `problems-2.json` `items[0].parts[3].widget` (p-climbing-wall) | tool limit T3 | explain.text prints 7.2857, refused; asked for whole pence; 7.28 accepted
- P3 `fluency-l6-undoing-in-reverse.json` `families[0].widget` (multiply-then-add) | tool limit T8 | template "{x0}"; 40 draws of family "multiply-then-add": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l8-clearing-fractions.json` `families[0].widget` (two-fractions-sum) | tool limit T8 | template "{x0}"; 40 draws of family "two-fractions-sum": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l4-putting-brackets-back.json` `families[1].widget` (highest-common-factor) | tool limit T8 | template "{h}({p:c}{v}{q:+})"; 40 draws of family "highest-common-factor": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-unknowns-both-sides.json` `families[1].widget` (brackets-both-sides) | tool limit T8 | template "{x0}"; 40 draws of family "brackets-both-sides": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l4-putting-brackets-back.json` `families[0].widget` (common-factor) | tool limit T8 | template "{h}({p:c}{v}{q:+})"; 40 draws of family "common-factor": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-unknowns-both-sides.json` `families[0].widget` (bracket-one-side) | tool limit T8 | template "{x0}"; 40 draws of family "bracket-one-side": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-undoing-in-reverse.json` `families[1].widget` (divide-then-add) | tool limit T8 | template "{x0}"; 40 draws of family "divide-then-add": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l8-clearing-fractions.json` `families[1].widget` (whole-tops) | tool limit T8 | template "{x0}"; 40 draws of family "whole-tops": every realised answer grades correct; none of 80 wrong values grades correct

### estimation (5)

- P3 `fluency-l10-catching-the-truth.json` `families[1].widget` (half-width-from-s) | tool limit T8 | template "{key}"; 40 draws of family "half-width-from-s": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l10-catching-the-truth.json` `families[0].widget` (interval-from-se) | tool limit T8 | template ["{lo}","{hi}"]; 40 draws of family "interval-from-se": every realised answer grades correct; none of 63 wrong values grades correct
- P3 `fluency-l9-how-precise.json` `families[2].widget` (data-needed) | tool limit T8 | template "{key}"; 40 draws of family "data-needed": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l9-how-precise.json` `families[1].widget` (se-of-proportion) | tool limit T8 | template "{key}"; 40 draws of family "se-of-proportion": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l9-how-precise.json` `families[0].widget` (se-of-mean) | tool limit T8 | template "{key}"; 40 draws of family "se-of-mean": every realised answer grades correct; none of 80 wrong values grades correct

### exp-log (14)

- P1 `l8-solving-for-the-power.json` `quiz[2].widget` (q-halvings) | tool limit T2 | explain.text prints 7.97, then rounds to the whole number 8, which is accepted
- P2 `l8-solving-for-the-power.json` `screens[2].widget.wrong[1]` (l8-solving-for-the-power) | harmless H3 | slip "mult" 0.0084 has band [0.0034, 0.0134]; the answer 4.93 grades correct and the other 2 slips keep their own lines
- P3 `fluency-l10-natural-log.json` `families[1].widget` (continuous-growth) | tool limit T8 | template "{round(years, 6)}"; 40 draws of family "continuous-growth": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l3-strange-powers.json` `families[1].widget` (fractional-power) | tool limit T8 | template "{key}"; 40 draws of family "fractional-power": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l8-solving-for-the-power.json` `families[2].widget` (power-alone-first) | tool limit T8 | template "{n}"; 40 draws of family "power-alone-first": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-strange-powers.json` `families[0].widget` (negative-power) | tool limit T8 | template "{key}"; 40 draws of family "negative-power": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l8-solving-for-the-power.json` `families[1].widget` (power-to-3-sf) | tool limit T8 | template "{round(r, 6)}"; 40 draws of family "power-to-3-sf": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l10-natural-log.json` `families[3].widget` (any-base-as-e) | tool limit T8 | template "{round(lb, 8)}"; 40 draws of family "any-base-as-e": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l3-strange-powers.json` `families[3].widget` (power-of-a-power) | tool limit T8 | template "{key}"; 40 draws of family "power-of-a-power": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-products-into-sums.json` `families[3].widget` (combine-a-difference) | tool limit T8 | template "{n}"; 40 draws of family "combine-a-difference": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l10-natural-log.json` `families[2].widget` (ln-from-two-values) | tool limit T8 | template "{key}"; 40 draws of family "ln-from-two-values": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l3-strange-powers.json` `families[2].widget` (laws-then-evaluate) | tool limit T8 | template "{key}"; 40 draws of family "laws-then-evaluate": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-products-into-sums.json` `families[2].widget` (combine-a-sum) | tool limit T8 | template "{n}"; 40 draws of family "combine-a-sum": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l8-solving-for-the-power.json` `families[3].widget` (money-target) | tool limit T8 | template "{round(r, 6)}"; 40 draws of family "money-target": every realised answer grades correct; none of 80 wrong values grades correct

### first-python (1)

- P1 `l9-packaging-steps.json` `quiz[3].widget` (q-cost) | tool limit T1 | explain.text prints 120, the wrong value "no-fee"; the answer 121.5 is accepted

### functions (1)

- P3 `fluency-l8-line-through-two-points.json` `families[0].widget` (gradient) | tool limit T8 | template "{m}"; 40 draws of family "gradient": every realised answer grades correct; none of 80 wrong values grades correct

### integrals (32)

- P1 `problems-1.json` `items[2].parts[3].widget` (p-desk-session) | harmless H1 | 2 places asked; -5.33 accepted, -5.32 and -5.34 refused
- P1 `problems-1.json` `items[2].parts[4].widget` (p-desk-session) | harmless H1 | 2 places asked; 2.33 accepted, 2.34 and 2.32 refused
- P1 `problems-2.json` `items[0].parts[3].widget` (p-area-function) | harmless H1 | 3 places asked; 6.667 accepted, 6.668 and 6.666 refused
- P1 `problems-2.json` `items[1].parts[3].widget` (p-turnover-decay) | harmless H1 | 2 places asked; 2.77 accepted, 2.78 and 2.76 refused
- P1 `problems-2.json` `items[2].parts[1].widget` (p-line-and-parabola) | harmless H1 | 3 places asked; 5.208 accepted, 5.209 and 5.207 refused
- P1 `problems-2.json` `items[2].parts[2].widget` (p-line-and-parabola) | harmless H1 | 3 places asked; 3.167 accepted, 3.168 and 3.166 refused
- P1 `problems-3.json` `items[0].parts[3].widget` (p-order-size-tail) | harmless H1 | 2 places asked; 9.95 accepted, 9.96 and 9.94 refused
- P1 `problems-3.json` `items[1].parts[1].widget` (p-time-to-fill) | harmless H1 | 3 places asked; 0.406 accepted, 0.407 and 0.405 refused
- P1 `problems-3.json` `items[2].parts[1].widget` (p-log-return) | harmless H1 | 4 places asked; -0.0452 accepted, -0.0451 and -0.0453 refused
- P1 `problems-3.json` `items[2].parts[2].widget` (p-log-return) | harmless H1 | 4 places asked; 0.0017 accepted, 0.0018 and 0.0016 refused
- P1 `problems-3.json` `items[3].parts[1].widget` (p-signal-average) | harmless H1 | 3 places asked; 3.459 accepted, 3.46 and 3.458 refused
- P1 `problems-3.json` `items[3].parts[2].widget` (p-signal-average) | harmless H1 | 3 places asked; 0.865 accepted, 0.866 and 0.864 refused
- P1 `problems-4.json` `items[0].parts[2].widget` (p-impact-kernel) | harmless H1 | 3 places asked; 0.811 accepted, 0.812 and 0.81 refused
- P1 `problems-4.json` `items[0].parts[3].widget` (p-impact-kernel) | harmless H1 | 3 places asked; 1.386 accepted, 1.387 and 1.385 refused
- P1 `problems-4.json` `items[0].parts[4].widget` (p-impact-kernel) | harmless H1 | 3 places asked; 0.585 accepted, 0.586 and 0.584 refused
- P1 `problems-4.json` `items[1].parts[0].widget` (p-flared-mouth) | harmless H1 | 3 places asked; 6.283 accepted, 6.284 and 6.282 refused
- P1 `problems-4.json` `items[1].parts[1].widget` (p-flared-mouth) | harmless H1 | 3 places asked; 1.645 accepted, 1.646 and 1.644 refused
- P1 `problems-4.json` `items[1].parts[2].widget` (p-flared-mouth) | harmless H1 | 3 places asked; 4.935 accepted, 4.936 and 4.934 refused
- P1 `problems-4.json` `items[1].parts[3].widget` (p-flared-mouth) | harmless H1 | 3 places asked; 0.707 accepted, 0.708 and 0.706 refused
- P1 `problems-4.json` `items[2].parts[1].widget` (p-dish-and-spindle) | harmless H1 | 3 places asked; 2.048 accepted, 2.049 and 2.047 refused
- P1 `problems-4.json` `items[2].parts[3].widget` (p-dish-and-spindle) | harmless H1 | 0 places asked; 15 accepted, 16 and 14 refused
- P1 `problems-4.json` `items[3].parts[0].widget` (p-rubber-seal) | harmless H1 | 3 places asked; 1.571 accepted, 1.572 and 1.57 refused
- P1 `problems-4.json` `items[3].parts[2].widget` (p-rubber-seal) | harmless H1 | 2 places asked; 59.22 accepted, 59.23 and 59.21 refused
- P1 `problems-4.json` `items[3].parts[4].widget` (p-rubber-seal) | harmless H1 | 2 places asked; 5.07 accepted, 5.08 and 5.06 refused
- P3 `fluency-l7-evaluating.json` `families[0].widget` (power) | tool limit T8 | template "{ans}"; 40 draws of family "power": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l14-splitting-fractions.json` `families[2].widget` (split-between-limits) | tool limit T8 | template "{ans}"; 40 draws of family "split-between-limits": every realised answer grades correct, and the answer rounded as asked (40); none of 74 wrong values grades correct
- P3 `fluency-l6-working-backwards.json` `families[3].widget` (fix-constant) | tool limit T8 | template "{ans}"; 40 draws of family "fix-constant": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-evaluating.json` `families[3].widget` (exponential) | tool limit T8 | template "{ans}"; 40 draws of family "exponential": every realised answer grades correct, and the answer rounded as asked (40); none of 89 wrong values grades correct
- P3 `fluency-l9-undo-chain.json` `families[3].widget` (definite-power) | tool limit T8 | template "{ans}"; 40 draws of family "definite-power": every realised answer grades correct; none of 40 wrong values grades correct
- P3 `fluency-l7-evaluating.json` `families[2].widget` (reciprocal-square) | tool limit T8 | template "{ans}"; 40 draws of family "reciprocal-square": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l14-splitting-fractions.json` `families[0].widget` (cover-up) | tool limit T8 | template "{ca}"; 40 draws of family "cover-up": every realised answer grades correct; none of 67 wrong values grades correct
- P3 `fluency-l7-evaluating.json` `families[1].widget` (quadratic) | tool limit T8 | template "{ans}"; 40 draws of family "quadratic": every realised answer grades correct; none of 80 wrong values grades correct

### ito (1)

- P2 `l11-prices-as-expectations.json` `quiz[1].widget.wrong[0]` (q-se) | harmless H3 | slip "over-n" 0.0001 has band [0.00005, 0.00015]; the answer 0.02 grades correct and the other slip keeps its own line

### least-squares (2)

- P3 `fluency-l11-fitting-a-line.json` `families[2].widget` (intercept-from-means) | tool limit T8 | template "{key}"; 40 draws of family "intercept-from-means": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l11-fitting-a-line.json` `families[0].widget` (slope-from-points) | tool limit T8 | template "{key}"; 40 draws of family "slope-from-points": every realised answer grades correct; none of 80 wrong values grades correct

### limits (17)

- P1 `l6-first-principles.json` `quiz[0].widget` (q-quotient-value) | tool limit T1 | explain.text prints 8, the wrong value "limit"; the answer 8.1 is accepted
- P1 `problems-1.json` `items[1].parts[3].widget` (p-rational-features) | tool limit T1 | explain.text prints 197, the wrong value "boundary"; the answer 198 is accepted
- P1 `problems-3.json` `items[1].parts[3].widget` (p-research-price) | harmless H1 | 2 places asked; 16.67 accepted, 16.68 and 16.66 refused
- P1 `problems-5.json` `items[0].parts[3].widget` (p-camera-pan) | harmless H1 | 1 place asked; 15.7 accepted, 15.8 and 15.6 refused
- P1 `problems-5.json` `items[2].parts[3].widget` (p-impact-curve) | harmless H1 | 0 places asked; 325 accepted, 326 and 324 refused
- P3 `fluency-l12-implicit.json` `families[2].widget` (product-term) | tool limit T8 | template "{-top/bot}"; 40 draws of family "product-term": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l13-peaks-and-troughs.json` `families[3].widget` (closed-interval-maximum) | tool limit T8 | template "{ans}"; 40 draws of family "closed-interval-maximum": every realised answer grades correct; none of 95 wrong values grades correct
- P3 `fluency-l12-implicit.json` `families[1].widget` (extra-y-term) | tool limit T8 | template "{-top/bot}"; 40 draws of family "extra-y-term": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l13-peaks-and-troughs.json` `families[2].widget` (minimum-value) | tool limit T8 | template "{fmn}"; 40 draws of family "minimum-value": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l2-computing-limits.json` `families[2].widget` (difference-quotient) | tool limit T8 | template "{r}"; 40 draws of family "difference-quotient": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-power-rule.json` `families[3].widget` (slope-at-a-point) | tool limit T8 | template "{r}"; 40 draws of family "slope-at-a-point": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l12-implicit.json` `families[0].widget` (ellipse) | tool limit T8 | template "{s}"; 40 draws of family "ellipse": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l13-peaks-and-troughs.json` `families[1].widget` (local-minimum) | tool limit T8 | template "{mn}"; 40 draws of family "local-minimum": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l2-computing-limits.json` `families[1].widget` (cancel-two-quadratics) | tool limit T8 | template "{top/bot}"; 40 draws of family "cancel-two-quadratics": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l9-products-quotients.json` `families[2].widget` (product-at-a-point) | tool limit T8 | template "{s}"; 40 draws of family "product-at-a-point": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l13-peaks-and-troughs.json` `families[0].widget` (local-maximum) | tool limit T8 | template "{mx}"; 40 draws of family "local-maximum": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l2-computing-limits.json` `families[0].widget` (cancel-linear-bottom) | tool limit T8 | template "{r}"; 40 draws of family "cancel-linear-bottom": every realised answer grades correct; none of 120 wrong values grades correct

### limits-thm (12)

- P1 `homework-3.json` `items[0].widget` (h-rolls-needed) | tool limit T2 | feedback.correct prints 1166.7, then rounds to the whole number 1167, which is accepted
- P1 `homework-3.json` `items[0].widget` (h-rolls-needed) | tool limit T2 | explain.text prints 1166.7, then rounds to the whole number 1167, which is accepted
- P1 `problems-1.json` `items[0].parts[0].widget` (p-dropped-ticks) | tool limit T1 | explain.text prints 0.2019, the wrong value "poisson"; the answer 0.2012 is accepted
- P1 `problems-3.json` `items[3].parts[4].widget` (p-fund-months) | tool limit T2 | explain.text prints 44.4, then rounds to the whole number 45, which is accepted
- P2 `l3-rare-events.json` `screens[1].widget.wrong[2]` (l3-rare-events) | harmless H3 | slip "all" 1.024e-7 has band [2.4e-9, 2.024e-7]; the answer 0.1074 grades correct and the other 2 slips keep their own lines
- P2 `l17-smallest-and-largest.json` `screens[8].widget.wrong[0]` (l17-smallest-and-largest) | harmless H3 | slip "maxcdf" 0.0002 has band [0.0001, 0.0003]; the answer 0.6321 grades correct and the other slip keeps its own line
- P3 `fluency-l1-counting-successes.json` `families[1].widget` (binomial-variance) | tool limit T8 | template "{key}"; 40 draws of family "binomial-variance": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-bell-curve.json` `families[2].widget` (within-band) | tool limit T8 | template "{key}"; 40 draws of family "within-band": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l1-counting-successes.json` `families[0].widget` (exactly-k) | tool limit T8 | template "{key}"; 40 draws of family "exactly-k": every realised answer grades correct, and the answer rounded as asked (40); none of 69 wrong values grades correct
- P3 `fluency-l7-bell-curve.json` `families[1].widget` (normal-probability) | tool limit T8 | template "{key}"; 40 draws of family "normal-probability": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-bell-curve.json` `families[0].widget` (standardise) | tool limit T8 | template "{z}"; 40 draws of family "standardise": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l1-counting-successes.json` `families[2].widget` (none-succeed) | tool limit T8 | template "{key}"; 40 draws of family "none-succeed": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct

### markov (6)

- P2 `l2-transition-matrix.json` `screens[8].widget.wrong[3]` (l2-transition-matrix) | harmless H3 | slip "cubed" 0.000001 has band [5e-7, 0.0000015]; the answer 0.0519 grades correct and the other 3 slips keep their own lines
- P2 `review-3.json` `items[5].widget.wrong[1]` (r-return-zero) | harmless H3 | slip "one-path" 0.001 has band [0.0005, 0.0015]; the answer 0.2461 grades correct and the other 2 slips keep their own lines
- P2 `problems-2.json` `items[0].parts[0].widget.wrong[0]` (p-band-days) | harmless H3 | slip "squared" 0.01 has band [0.005, 0.015]; the answer 0.14 grades correct and the other 2 slips keep their own lines
- P3 `fluency-l2-transition-matrix.json` `families[1].widget` (three-state-two-step) | tool limit T8 | template "{key}"; 40 draws of family "three-state-two-step": every realised answer grades correct; none of 78 wrong values grades correct
- P3 `fluency-l2-transition-matrix.json` `families[0].widget` (two-state-two-step) | tool limit T8 | template "{key}"; 40 draws of family "two-state-two-step": every realised answer grades correct; none of 79 wrong values grades correct
- P3 `fluency-l2-transition-matrix.json` `families[2].widget` (distribution-forward) | tool limit T8 | template "{key}"; 40 draws of family "distribution-forward": every realised answer grades correct; none of 80 wrong values grades correct

### measure-prob (3)

- P1 `l3-measures.json` `quiz[1].widget` (q-union) | tool limit T1 | explain.text prints 1.985, the wrong value "indep"; the answer 2 is accepted
- P1 `review-2.json` `items[4].parts[1].widget` (r-div) | tool limit T2 | explain.text prints 62.6, then rounds to the whole number 63, which is accepted
- P2 `l1-why-measure.json` `screens[1].widget.wrong[0]` (l1-why-measure) | harmless H4 | slip "tiny" 0.001 has band [0.0005, 0.0015]; the answer 0 grades correct; the answer is 0 exactly; the band catches a small positive number

### mental (2)

- P1 `l2-round-and-adjust.json` `quiz[0].widget` (q1) | tool limit T1 | explain.text prints 96, the wrong value "no-fix"; the answer 95 is accepted
- P1 `l7-near-round.json` `quiz[2].widget` (q-hedge) | tool limit T4 | explain.text prints 6400, refused; 6400 is the round number before the 1% is taken off

### mental-pressure (9)

- P1 `review-1.json` `items[4].widget` (r-mix-score) | tool limit T2 | feedback.correct prints 34.3, then rounds to the whole number 34, which is accepted
- P1 `review-1.json` `items[4].widget` (r-mix-score) | tool limit T2 | explain.text prints 34.3, then rounds to the whole number 34, which is accepted
- P1 `l7-estimating-products.json` `screens[2].widget` (l7-estimating-products) | harmless H1 | 2 places asked; 0.16 accepted, 0.17 and 0.15 refused
- P1 `l8-square-roots.json` `screens[0].widget` (l8-square-roots) | harmless H1 | 1 place asked; 7.1 accepted, 7.2 and 7 refused
- P1 `l8-square-roots.json` `screens[11].widget` (l8-square-roots) | harmless H1 | 2 places asked; 1.26 accepted, 1.27 and 1.25 refused
- P1 `l8-square-roots.json` `quiz[0].widget` (q-root-80) | harmless H1 | 1 place asked; 8.9 accepted, 9 and 8.8 refused
- P1 `l8-square-roots.json` `quiz[3].widget` (q-root-1000) | harmless H1 | 1 place asked; 31.6 accepted, 31.7 and 31.5 refused
- P1 `homework-2.json` `items[4].widget` (h-gap-13-17) | harmless H1 | 4 places asked; 0.0028 accepted, 0.0029 and 0.0027 refused
- P1 `homework-2.json` `items[6].widget` (h-monthly-vol) | harmless H1 | 1 place asked; 5.8 accepted, 5.9 and 5.7 refused

### micro (4)

- P1 `l2-walking-the-book.json` `quiz[1].widget` (q-sell) | tool limit T5 | explain.text prints 49, refused; the text prints 49{,}988 (the total), read as 49
- P1 `l10-inventory.json` `quiz[0].widget` (q-skew-ask) | tool limit T4 | feedback.correct prints 796, refused; 796 is the skewed centre; the ask is 3p above it
- P1 `review-3.json` `items[1].widget` (r-skew-bid) | tool limit T4 | feedback.correct prints 1202, refused; 1202 is the skewed centre; the bid is 3p below it
- P1 `homework-3.json` `items[2].widget` (h-limit-ask) | tool limit T1 | feedback.correct prints 1991, the wrong value "mid"; the answer 1995 is accepted

### mm-games (7)

- P1 `l3-how-wide.json` `quiz[0].widget` (q-three-nine-twelve) | harmless H2 | explain.text prints 0.48, refused; four places or a fraction asked; 0.4815 and 13/27 accepted
- P1 `review-1.json` `items[2].widget` (r-abs-diff) | harmless H2 | explain.text prints 1.94, refused; four places or a fraction asked; 1.9444 and 35/18 accepted
- P1 `review-1.json` `items[5].widget` (r-eight-thirteen) | harmless H2 | explain.text prints 0.68, refused; four places or a fraction asked; 0.6759 and 73/108 accepted
- P1 `homework-1.json` `items[6].widget` (h-distinct-faces) | harmless H2 | explain.text prints 2.53, refused; four places or a fraction asked; 2.5278 and 91/36 accepted
- P1 `homework-3.json` `items[7].widget` (h-mock-fair-1) | harmless H2 | explain.text prints 21.96, refused; four places asked; 21.9608 accepted
- P1 `l17-options-on-a-game.json` `quiz[2].widget` (q-strad8) | harmless H2 | explain.text prints 2.11, refused; four places asked; 2.1111 accepted
- P3 `l11-hedging.json` `screens[5].widget` (l11-hedging) | tool limit T9 | the answer is "{{carry.sum.position}}", filled from an earlier screen; with the carried value set to -2, 0, 3 the same number grades correct and its neighbour does not

### momentum-rep (1)

- P2 `l3-main-table.json` `screens[2].widget.wrong[1]` (l3-main-table) | harmless H3 | slip "root" 0.0094 has band [0.0044, 0.0144]; the answer 2.73 grades correct and the other slip keeps its own line

### multivar (8)

- P1 `l7-tangent-planes.json` `quiz[0].widget` (q-plane-est) | tool limit T1 | explain.text prints 4.82, the wrong value "exact"; the answer 4.8 is accepted
- P1 `review-2.json` `items[2].widget` (r-plane-est) | tool limit T1 | explain.text prints 1.701, the wrong value "exact"; the answer 1.7 is accepted
- P3 `fluency-l1-two-inputs.json` `families[2].widget` (point-on-a-contour) | tool limit T8 | template "{key}"; 40 draws of family "point-on-a-contour": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l2-slicing.json` `families[3].widget` (log-at-a-point) | tool limit T8 | template "{key}"; 40 draws of family "log-at-a-point": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l1-two-inputs.json` `families[1].widget` (walk-along-a-contour) | tool limit T8 | template "{r}"; 40 draws of family "walk-along-a-contour": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l1-two-inputs.json` `families[0].widget` (contour-through-a-point) | tool limit T8 | template "{key}"; 40 draws of family "contour-through-a-point": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l2-slicing.json` `families[1].widget` (partial-y-at-a-point) | tool limit T8 | template "{key}"; 40 draws of family "partial-y-at-a-point": every realised answer grades correct; none of 78 wrong values grades correct
- P3 `fluency-l3-second-partials.json` `families[1].widget` (bend-at-a-point) | tool limit T8 | template "{key}"; 40 draws of family "bend-at-a-point": every realised answer grades correct; none of 80 wrong values grades correct

### number-sense (38)

- P1 `l7-fractions-to-decimals.json` `quiz[3].widget` (q-split-profit) | tool limit T1 | feedback.correct prints 33.333, the wrong value "unrounded"; the answer 33.33 is accepted
- P1 `l7-fractions-to-decimals.json` `quiz[3].widget` (q-split-profit) | tool limit T1 | explain.text prints 33.333, the wrong value "unrounded"; the answer 33.33 is accepted
- P1 `review-2.json` `items[4].widget` (rv-fee-split) | tool limit T1 | feedback.correct prints 2.857, the wrong value "unrounded"; the answer 2.86 is accepted
- P1 `review-2.json` `items[4].widget` (rv-fee-split) | tool limit T1 | explain.text prints 2.857142, the wrong value "unrounded"; the answer 2.86 is accepted
- P1 `homework-2.json` `items[1].widget` (hw-seven-twelfths) | tool limit T3 | feedback.correct prints 0.58333, refused; asked for 3 places; 0.583 accepted
- P1 `homework-2.json` `items[7].widget` (hw-fill-average) | tool limit T1 | feedback.correct prints 20.15666, the wrong value "unrounded"; the answer 20.16 is accepted
- P1 `homework-2.json` `items[7].widget` (hw-fill-average) | tool limit T1 | explain.text prints 20.15666, the wrong value "unrounded"; the answer 20.16 is accepted
- P3 `fluency-l12-which-first.json` `families[1].widget` (powers-next) | tool limit T8 | template "{key}"; 40 draws of family "powers-next": every realised answer grades correct; none of 74 wrong values grades correct
- P3 `fluency-l15-building-blocks.json` `families[1].widget` (count-from-primes) | tool limit T8 | template "{key}"; 40 draws of family "count-from-primes": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l16-shared-factors.json` `families[2].widget` (other-number) | tool limit T8 | template "{n}"; 40 draws of family "other-number": every realised answer grades correct; none of 78 wrong values grades correct
- P3 `fluency-l17-around-and-inside.json` `families[3].widget` (l-shape-area) | tool limit T8 | template "{key}"; 40 draws of family "l-shape-area": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l18-circles-and-units.json` `families[3].widget` (area-units) | tool limit T8 | template "{key}"; 40 draws of family "area-units": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l19-one-number-for-many.json` `families[3].widget` (table-mean) | tool limit T8 | template "{key}"; 40 draws of family "table-mean": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l5-how-many-halves.json` `families[1].widget` (fraction-by-fraction) | tool limit T8 | template "{key:frac}"; 40 draws of family "fraction-by-fraction": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l9-negative-times-negative.json` `families[1].widget` (divide-two) | tool limit T8 | template "{q}"; 40 draws of family "divide-two": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l12-which-first.json` `families[0].widget` (times-before-plus) | tool limit T8 | template "{key}"; 40 draws of family "times-before-plus": every realised answer grades correct; none of 56 wrong values grades correct
- P3 `fluency-l15-building-blocks.json` `families[0].widget` (largest-prime) | tool limit T8 | template "{lp}"; 40 draws of family "largest-prime": every realised answer grades correct; none of 50 wrong values grades correct
- P3 `fluency-l16-shared-factors.json` `families[1].widget` (lcm) | tool limit T8 | template "{l}"; 40 draws of family "lcm": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l17-around-and-inside.json` `families[2].widget` (trapezium-area) | tool limit T8 | template "{key}"; 40 draws of family "trapezium-area": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l18-circles-and-units.json` `families[2].widget` (speed-units) | tool limit T8 | template "{key}"; 40 draws of family "speed-units": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l19-one-number-for-many.json` `families[2].widget` (range) | tool limit T8 | template "{key}"; 40 draws of family "range": every realised answer grades correct; none of 76 wrong values grades correct
- P3 `fluency-l5-how-many-halves.json` `families[0].widget` (whole-by-fraction) | tool limit T8 | template "{key:frac}"; 40 draws of family "whole-by-fraction": every realised answer grades correct; none of 67 wrong values grades correct
- P3 `fluency-l9-negative-times-negative.json` `families[0].widget` (multiply-two) | tool limit T8 | template "{key}"; 40 draws of family "multiply-two": every realised answer grades correct; none of 54 wrong values grades correct
- P3 `fluency-l12-which-first.json` `families[3].widget` (left-to-right) | tool limit T8 | template "{key}"; 40 draws of family "left-to-right": every realised answer grades correct; none of 63 wrong values grades correct
- P3 `fluency-l16-shared-factors.json` `families[0].widget` (hcf) | tool limit T8 | template "{g}"; 40 draws of family "hcf": every realised answer grades correct; none of 69 wrong values grades correct
- P3 `fluency-l17-around-and-inside.json` `families[1].widget` (parallelogram-area) | tool limit T8 | template "{key}"; 40 draws of family "parallelogram-area": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l18-circles-and-units.json` `families[1].widget` (circle-area) | tool limit T8 | template "{area}"; 40 draws of family "circle-area": every realised answer grades correct, and the answer rounded as asked (40); none of 64 wrong values grades correct
- P3 `fluency-l19-one-number-for-many.json` `families[1].widget` (median) | tool limit T8 | template "{s3}"; 40 draws of family "median": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-adding-pieces.json` `families[1].widget` (subtract-unlike) | tool limit T8 | template "{s:frac}"; 40 draws of family "subtract-unlike": every realised answer grades correct; none of 52 wrong values grades correct
- P3 `fluency-l8-below-zero.json` `families[1].widget` (subtract-signed) | tool limit T8 | template "{key}"; 40 draws of family "subtract-signed": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l12-which-first.json` `families[2].widget` (brackets-first) | tool limit T8 | template "{key}"; 40 draws of family "brackets-first": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l15-building-blocks.json` `families[2].widget` (count-factors) | tool limit T8 | template "{key}"; 40 draws of family "count-factors": every realised answer grades correct; none of 71 wrong values grades correct
- P3 `fluency-l17-around-and-inside.json` `families[0].widget` (triangle-area) | tool limit T8 | template "{key}"; 40 draws of family "triangle-area": every realised answer grades correct; none of 77 wrong values grades correct
- P3 `fluency-l18-circles-and-units.json` `families[0].widget` (circumference) | tool limit T8 | template "{circ}"; 40 draws of family "circumference": every realised answer grades correct, and the answer rounded as asked (40); none of 77 wrong values grades correct
- P3 `fluency-l19-one-number-for-many.json` `families[0].widget` (mean) | tool limit T8 | template "{m}"; 40 draws of family "mean": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-adding-pieces.json` `families[0].widget` (add-unlike) | tool limit T8 | template "{s:frac}"; 40 draws of family "add-unlike": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l8-below-zero.json` `families[0].widget` (add-signed) | tool limit T8 | template "{key}"; 40 draws of family "add-signed": every realised answer grades correct; none of 70 wrong values grades correct
- P3 `fluency-l9-negative-times-negative.json` `families[2].widget` (multiply-three) | tool limit T8 | template "{key}"; 40 draws of family "multiply-three": every realised answer grades correct; none of 80 wrong values grades correct

### numerics (2)

- P1 `l13-finite-differences.json` `quiz[0].widget` (q-limit-50) | tool limit T2 | explain.text prints 100.05, then rounds to the whole number 101, which is accepted
- P2 `l16-control-variates.json` `screens[11].widget.wrong[1]` (l16-control-variates) | harmless H3 | slip "hours" 0.01 has band [0.005, 0.015]; the answer 36 grades correct and the other slip keeps its own line

### odes (3)

- P3 `fluency-l2-separable.json` `families[3].widget` (discount) | tool limit T8 | template "{key}"; 40 draws of family "discount": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-characteristic-equation.json` `families[0].widget` (real-roots) | tool limit T8 | template ["{r1}","{r2}"]; 40 draws of family "real-roots": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-integrating-factor.json` `families[2].widget` (savings-balance) | tool limit T8 | template "{key}"; 40 draws of family "savings-balance": every realised answer grades correct; none of 80 wrong values grades correct

### opt-dash (1)

- P2 `l16-assembling.json` `screens[9].widget.wrong[1]` (l16-assembling) | harmless H3 | slip "divide" 6.6e-7 has band [-3.4e-7, 0.00000166]; the answer 2720 grades correct and the other slip keeps its own line; a typed 0 gets this line

### pdes (2)

- P1 `homework-2.json` `items[5].widget` (h-step-count) | tool limit T2 | feedback.correct prints 2533.03, then rounds to the whole number 2534, which is accepted
- P2 `l9-black-scholes-to-heat.json` `quiz[2].widget.wrong[0]` (q-beta) | harmless H3 | slip "no-k" -0.0004 has band [-0.0006, -0.0002]; the answer -0.9604 grades correct and the other slip keeps its own line

### plotting (1)

- P1 `review-2.json` `items[6].widget` (r7) | tool limit T4 | explain.text prints 0.99, refused; 0.99 is one up-and-down pair; the answer is two pairs

### puzzles (5)

- P1 `l2-every-coupon.json` `quiz[0].widget` (q-suits) | harmless H2 | explain.text prints 8.33, refused; four places asked; 8.3333 accepted
- P1 `l4-indicator-tricks.json` `quiz[2].widget` (q-three-dice) | harmless H2 | explain.text prints 2.53, refused; four places asked; 2.5278 accepted
- P1 `review-1.json` `items[2].widget` (r1-months) | harmless H2 | explain.text prints 37.24, refused; four places asked; 37.2385 accepted
- P2 `homework-1.json` `items[8].widget.wrong[1]` (hw1-triples) | harmless H3 | slip "one-day" 0.0004 has band [-0.0001, 0.0009]; the answer 0.1471 grades correct and the other slip keeps its own line; a typed 0 gets this line
- P2 `l9-bayes-in-a-minute.json` `screens[4].widget.wrong[0]` (l9-bayes-in-a-minute) | harmless H3 | slip "base" 0.001 has band [0.0005, 0.0015]; the answer 0.5062 grades correct and the other slip keeps its own line

### pytest (1)

- P2 `l4-floats-in-tests.json` `quiz[1].widget.wrong[1]` (q-rel-gap) | tool limit T7 | slip "floor" 1e-12 has band [9e-13, 1.1e-12]; the answer 0.00025 grades correct and the other slip keeps its own line; a typed 0 gets this line; authored tol 1e-13 is a tenth of the value 1e-12

### quadratics (30)

- P1 `problems-2.json` `items[1].parts[2].widget` (p-bus-chase) | harmless H1 | 2 places asked; 1.27 accepted, 1.28 and 1.26 refused
- P1 `problems-2.json` `items[2].parts[2].widget` (p-can-stack) | harmless H1 | 2 places asked; 13.65 accepted, 13.66 and 13.64 refused
- P3 `fluency-l14-roots-that-stay.json` `families[2].widget` (conjugate-bottom) | tool limit T8 | template "{key}"; 40 draws of family "conjugate-bottom": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l16-adding-and-solving.json` `families[0].widget` (add-tops) | tool limit T8 | template "{poly(v; m, c0)}"; 40 draws of family "add-tops": every realised answer grades correct; none of 120 wrong values grades correct
- P3 `fluency-l17-dividing-polynomials.json` `families[0].widget` (remainder) | tool limit T8 | template "{key}"; 40 draws of family "remainder": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l2-product-and-sum.json` `families[0].widget` (factorise-monic) | tool limit T8 | template "({v}{p:+})({v}{q:+})"; 40 draws of family "factorise-monic": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-leading-coefficient.json` `families[1].widget` (split-product) | tool limit T8 | template "{ac}"; 40 draws of family "split-product": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l4-difference-of-squares.json` `families[2].widget` (mental-difference) | tool limit T8 | template "{ans}"; 40 draws of family "mental-difference": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-completing-the-square.json` `families[2].widget` (square-form) | tool limit T8 | template "({v}{h:+})^2{k:+}"; 40 draws of family "square-form": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-the-formula.json` `families[2].widget` (decimal-roots) | tool limit T8 | template ["{lo}","{hi}"]; 40 draws of family "decimal-roots": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l14-roots-that-stay.json` `families[1].widget` (collect-surds) | tool limit T8 | template "{key}"; 40 draws of family "collect-surds": every realised answer grades correct; none of 59 wrong values grades correct
- P3 `fluency-l15-fractions-with-letters.json` `families[2].widget` (divide-and-cancel) | tool limit T8 | template "{v}({v}{b:+})"; 40 draws of family "divide-and-cancel": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l16-adding-and-solving.json` `families[3].widget` (reject-root) | tool limit T8 | template "{b}"; 40 draws of family "reject-root": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l17-dividing-polynomials.json` `families[3].widget` (factorise-cubic) | tool limit T8 | template "({v}{nr:+})({v}{ns:+})({v}{nu:+})"; 40 draws of family "factorise-cubic": every realised answer grades correct; none of 72 wrong values grades correct
- P3 `fluency-l3-leading-coefficient.json` `families[0].widget` (factorise-non-monic) | tool limit T8 | template "({p}{v}{q:+})({v}{s:+})"; 40 draws of family "factorise-non-monic": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l4-difference-of-squares.json` `families[1].widget` (number-minus-square) | tool limit T8 | template "({q}+{p:c}{v})({q}-{p:c}{v})"; 40 draws of family "number-minus-square": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-completing-the-square.json` `families[1].widget` (solve-by-square) | tool limit T8 | template ["{lo}","{hi}"]; 40 draws of family "solve-by-square": every realised answer grades correct; none of 73 wrong values grades correct
- P3 `fluency-l7-the-formula.json` `families[1].widget` (rational-roots) | tool limit T8 | template ["{lo}","{hi}"]; 40 draws of family "rational-roots": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l14-roots-that-stay.json` `families[0].widget` (simplest-surd) | tool limit T8 | template "{k}"; 40 draws of family "simplest-surd": every realised answer grades correct; none of 66 wrong values grades correct
- P3 `fluency-l15-fractions-with-letters.json` `families[1].widget` (multiply-and-cancel) | tool limit T8 | template "{k}({v}{a:+})"; 40 draws of family "multiply-and-cancel": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l16-adding-and-solving.json` `families[2].widget` (solve-two-roots) | tool limit T8 | template ["{r}","{s}"]; 40 draws of family "solve-two-roots": every realised answer grades correct; none of 40 wrong values grades correct
- P3 `fluency-l4-difference-of-squares.json` `families[0].widget` (square-minus-number) | tool limit T8 | template "({p:c}{v}+{q})({p:c}{v}-{q})"; 40 draws of family "square-minus-number": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-completing-the-square.json` `families[0].widget` (find-the-constant) | tool limit T8 | template "{k}"; 40 draws of family "find-the-constant": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-the-formula.json` `families[0].widget` (discriminant) | tool limit T8 | template "{d}"; 40 draws of family "discriminant": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l16-adding-and-solving.json` `families[1].widget` (subtract-tops) | tool limit T8 | template "{poly(v; m, c0)}"; 40 draws of family "subtract-tops": every realised answer grades correct; none of 120 wrong values grades correct
- P3 `fluency-l17-dividing-polynomials.json` `families[1].widget` (find-k) | tool limit T8 | template "{k}"; 40 draws of family "find-k": every realised answer grades correct; none of 76 wrong values grades correct
- P3 `fluency-l2-product-and-sum.json` `families[1].widget` (perfect-square) | tool limit T8 | template "({v}{p:+})^2"; 40 draws of family "perfect-square": every realised answer grades correct, as do 40 accept forms; none of 80 wrong values grades correct
- P3 `fluency-l3-leading-coefficient.json` `families[2].widget` (common-factor-first) | tool limit T8 | template "{k}({p:c}{v}{q:+})({v}{s:+})"; 40 draws of family "common-factor-first": every realised answer grades correct; none of 79 wrong values grades correct
- P3 `fluency-l4-difference-of-squares.json` `families[3].widget` (common-factor-first) | tool limit T8 | template "{k}({p:c}{v}+{q})({p:c}{v}-{q})"; 40 draws of family "common-factor-first": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-completing-the-square.json` `families[3].widget` (largest-value) | tool limit T8 | template "{top}"; 40 draws of family "largest-value": every realised answer grades correct; none of 80 wrong values grades correct

### random-vars (8)

- P1 `homework-2.json` `items[1].widget` (h-squares-game) | harmless H2 | explain.text prints 0.17, refused; three places asked; 0.167 accepted
- P1 `homework-3.json` `items[5].widget` (h3-how-many) | tool limit T2 | explain.text prints 12.9, then rounds to the whole number 13, which is accepted
- P1 `problems-3.json` `items[0].parts[3].widget` (p-quote-trades) | tool limit T2 | feedback.correct prints 486.8, then rounds to the whole number 487, which is accepted
- P2 `review-2.json` `items[4].widget.wrong[0]` (r-square) | harmless H3 | slip "sq-mean" 0.01 has band [0.005, 0.015]; the answer 1.1 grades correct and the other slip keeps its own line
- P2 `l20-many-categories.json` `screens[4].widget.wrong[1]` (l20-many-categories) | harmless H3 | slip "oneorder" 0.00002 has band [0.00001, 0.00003]; the answer 0.0638 grades correct and the other slip keeps its own line
- P3 `fluency-l9-measuring-spread.json` `families[2].widget` (standard-deviation) | tool limit T8 | template "{key}"; 40 draws of family "standard-deviation": every realised answer grades correct; none of 78 wrong values grades correct
- P3 `fluency-l9-measuring-spread.json` `families[1].widget` (three-value-variance) | tool limit T8 | template "{key}"; 40 draws of family "three-value-variance": every realised answer grades correct; none of 79 wrong values grades correct
- P3 `fluency-l9-measuring-spread.json` `families[0].widget` (two-outcome-variance) | tool limit T8 | template "{key}"; 40 draws of family "two-outcome-variance": every realised answer grades correct; none of 77 wrong values grades correct

### ratio (14)

- P2 `l13-currencies.json` `quiz[1].widget.wrong[1]` (q-yen-pence) | harmless H3 | slip "pounds" 0.0053 has band [0.0003, 0.0103]; the answer 0.53 grades correct and the other slip keeps its own line
- P3 `fluency-l4-multipliers.json` `families[1].widget` (apply-multiplier) | tool limit T8 | template "{key}"; 40 draws of family "apply-multiplier": every realised answer grades correct; none of 84 wrong values grades correct
- P3 `fluency-l6-before-the-discount.json` `families[1].widget` (undo-a-rise) | tool limit T8 | template "{orig}"; 40 draws of family "undo-a-rise": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l9-sharing.json` `families[2].widget` (three-way) | tool limit T8 | template "{key}"; 40 draws of family "three-way": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l4-multipliers.json` `families[0].widget` (write-multiplier) | tool limit T8 | template "{key}"; 40 draws of family "write-multiplier": every realised answer grades correct; none of 89 wrong values grades correct
- P3 `fluency-l6-before-the-discount.json` `families[0].widget` (undo-a-discount) | tool limit T8 | template "{orig}"; 40 draws of family "undo-a-discount": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l9-sharing.json` `families[1].widget` (from-one-share) | tool limit T8 | template "{key}"; 40 draws of family "from-one-share": every realised answer grades correct; none of 59 wrong values grades correct
- P3 `fluency-l2-building-percentages.json` `families[1].widget` (half-percent) | tool limit T8 | template "{key}"; 40 draws of family "half-percent": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l5-rise-or-fall.json` `families[1].widget` (daily-return) | tool limit T8 | template "{key}"; 40 draws of family "daily-return": every realised answer grades correct; none of 68 wrong values grades correct
- P3 `fluency-l9-sharing.json` `families[0].widget` (share-a-total) | tool limit T8 | template "{key}"; 40 draws of family "share-a-total": every realised answer grades correct; none of 93 wrong values grades correct
- P3 `fluency-l2-building-percentages.json` `families[0].widget` (whole-percent) | tool limit T8 | template "{key}"; 40 draws of family "whole-percent": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l5-rise-or-fall.json` `families[0].widget` (percentage-change) | tool limit T8 | template "{key}"; 40 draws of family "percentage-change": every realised answer grades correct; none of 119 wrong values grades correct
- P3 `fluency-l6-before-the-discount.json` `families[2].widget` (vat-inside) | tool limit T8 | template "{vat}"; 40 draws of family "vat-inside": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l9-sharing.json` `families[3].widget` (from-a-difference) | tool limit T8 | template "{key}"; 40 draws of family "from-a-difference": every realised answer grades correct; none of 109 wrong values grades correct

### regression (5)

- P1 `l5-how-sure.json` `quiz[3].widget` (q-month-sd) | content fault F1 | feedback.correct prints 0.25, refused; no form is asked; the feedback gives $6 / 23.66 = 0.25$ | fix: `"tol": {"abs":0.005}` (was `{"abs":0.003}`); with it the grader takes 0.25, 0.254, 0.2535 and the 2 wrong values keep their own lines
- P2 `l3-how-much-explained.json` `screens[8].widget.wrong[1]` (l3-how-much-explained) | harmless H3 | slip "sq" 0.0001 has band [0.00005, 0.00015]; the answer 0.1 grades correct and the other slip keeps its own line
- P3 `fluency-l2-slope-formula.json` `families[2].widget` (slope-from-r) | tool limit T8 | template "{key}"; 40 draws of family "slope-from-r": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l2-slope-formula.json` `families[1].widget` (intercept) | tool limit T8 | template "{key}"; 40 draws of family "intercept": every realised answer grades correct; none of 79 wrong values grades correct
- P3 `fluency-l2-slope-formula.json` `families[0].widget` (slope-from-sums) | tool limit T8 | template "{key}"; 40 draws of family "slope-from-sums": every realised answer grades correct; none of 80 wrong values grades correct

### series (21)

- P1 `l12-small-x.json` `quiz[3].widget` (q-three-terms) | tool limit T4 | explain.text prints 1.26677, refused; 1.26677 is the exact value set beside the three-term estimate 1.2652
- P1 `problems-1.json` `items[1].parts[2].widget` (p-pendulum-swings) | harmless H1 | 1 place asked; 47.2 accepted, 47.3 and 47.1 refused
- P1 `problems-2.json` `items[2].parts[0].widget` (p-bouncing-ball) | harmless H1 | 2 places asked; 7.42 accepted, 7.43 and 7.41 refused
- P3 `fluency-l11-powers-of-a-bracket.json` `families[1].widget` (ax-plus-b) | tool limit T8 | template "{key}"; 40 draws of family "ax-plus-b": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l2-any-term.json` `families[2].widget` (difference-from-two-terms) | tool limit T8 | template "{d}"; 40 draws of family "difference-from-two-terms": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-shifted-copy.json` `families[0].widget` (first-n-terms) | tool limit T8 | template "{sum}"; 40 draws of family "first-n-terms": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l8-adding-forever.json` `families[1].widget` (from-a-and-r) | tool limit T8 | template "{sum}"; 40 draws of family "from-a-and-r": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l11-powers-of-a-bracket.json` `families[0].widget` (x-plus-b) | tool limit T8 | template "{key}"; 40 draws of family "x-plus-b": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-multiplying-each-time.json` `families[1].widget` (common-ratio) | tool limit T8 | template "{r}"; 40 draws of family "common-ratio": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-gauss.json` `families[2].widget` (up-to-last-term) | tool limit T8 | template "{sum}"; 40 draws of family "up-to-last-term": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l8-adding-forever.json` `families[0].widget` (from-the-terms) | tool limit T8 | template "{sum}"; 40 draws of family "from-the-terms": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l2-any-term.json` `families[0].widget` (term-from-list) | tool limit T8 | template "{u}"; 40 draws of family "term-from-list": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-multiplying-each-time.json` `families[0].widget` (geometric-term) | tool limit T8 | template "{u}"; 40 draws of family "geometric-term": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-gauss.json` `families[1].widget` (first-n-terms) | tool limit T8 | template "{sum}"; 40 draws of family "first-n-terms": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-shifted-copy.json` `families[2].widget` (sigma-powers) | tool limit T8 | template "{sum}"; 40 draws of family "sigma-powers": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l8-adding-forever.json` `families[3].widget` (recurring-decimal) | tool limit T8 | template "{key:frac}"; 40 draws of family "recurring-decimal": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l11-powers-of-a-bracket.json` `families[2].widget` (term-with-no-x) | tool limit T8 | template "{key}"; 40 draws of family "term-with-no-x": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l2-any-term.json` `families[3].widget` (which-term) | tool limit T8 | template "{m}"; 40 draws of family "which-term": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-gauss.json` `families[0].widget` (one-to-n) | tool limit T8 | template "{sum}"; 40 draws of family "one-to-n": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-shifted-copy.json` `families[1].widget` (up-to-last-term) | tool limit T8 | template "{sum}"; 40 draws of family "up-to-last-term": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l8-adding-forever.json` `families[2].widget` (perpetual-bond) | tool limit T8 | template "{val}"; 40 draws of family "perpetual-bond": every realised answer grades correct; none of 80 wrong values grades correct

### stat-learning (14)

- P2 `l8-setting-to-zero.json` `screens[8].widget.wrong[0]` (l8-setting-to-zero) | harmless H4 | slip "inf" 1000000 has band [1000, 1999000]; the answer 0.6 grades correct and the other 2 slips keep their own lines; catches any huge number as "infinity"; the answer 0.6 and the slips 1.55 and 0.05 are far below 1000
- P3 `fluency-l16-groups-nobody-labelled.json` `families[0].widget` (assign-and-update) | tool limit T8 | template "{key}"; 40 draws of family "assign-and-update": every realised answer grades correct, and the answer rounded as asked (40); none of 120 wrong values grades correct
- P3 `fluency-l17-a-small-network.json` `families[1].widget` (parameter-count) | tool limit T8 | template "{key}"; 40 draws of family "parameter-count": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l18-bending-the-line.json` `families[1].widget` (slope-in-a-region) | tool limit T8 | template "{key}"; 40 draws of family "slope-in-a-region": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l15-widest-street.json` `families[2].widget` (distance) | tool limit T8 | template "{key}"; 40 draws of family "distance": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l17-a-small-network.json` `families[0].widget` (forward-pass) | tool limit T8 | template "{key}"; 40 draws of family "forward-pass": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l18-bending-the-line.json` `families[0].widget` (hinge-value) | tool limit T8 | template "{key}"; 40 draws of family "hinge-value": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l15-widest-street.json` `families[1].widget` (decision-value) | tool limit T8 | template "{key}"; 40 draws of family "decision-value": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l16-groups-nobody-labelled.json` `families[2].widget` (linkage-distance) | tool limit T8 | template "{key}"; 40 draws of family "linkage-distance": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l17-a-small-network.json` `families[3].widget` (one-step) | tool limit T8 | template "{key}"; 40 draws of family "one-step": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l15-widest-street.json` `families[0].widget` (margin) | tool limit T8 | template "{key}"; 40 draws of family "margin": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l16-groups-nobody-labelled.json` `families[1].widget` (group-inertia) | tool limit T8 | template "{key}"; 40 draws of family "group-inertia": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l17-a-small-network.json` `families[2].widget` (slope-first-weight) | tool limit T8 | template "{key}"; 40 draws of family "slope-first-weight": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l18-bending-the-line.json` `families[2].widget` (coefficient-count) | tool limit T8 | template "{key}"; 40 draws of family "coefficient-count": every realised answer grades correct; none of 80 wrong values grades correct

### stat-models (1)

- P1 `review-2.json` `items[3].widget` (r2-n) | tool limit T2 | explain.text prints 392.4, then rounds to the whole number 393, which is accepted

### systems (1)

- P1 `l14-messages-on-the-wire.json` `quiz[3].widget` (q-frames) | tool limit T2 | explain.text prints 58.3, then rounds to the whole number 58, which is accepted

### taylor (8)

- P1 `l3-newton.json` `quiz[0].widget` (q-root-five) | tool limit T4 | explain.text prints 2.2361, refused; 2.2361 is the root, the answer is the first Newton step
- P1 `l3-newton.json` `quiz[2].widget` (q-cube-nine) | tool limit T4 | explain.text prints 2.0801, refused; 2.0801 is the root, the answer is the first Newton step
- P1 `problems-2.json` `items[3].parts[3].widget` (p-log-two) | harmless H1 | 4 places asked; 0.0417 accepted, 0.0418 and 0.0416 refused
- P3 `fluency-l1-tangent-approx.json` `families[2].widget` (estimate-a-root) | tool limit T8 | template "{key}"; 40 draws of family "estimate-a-root": every realised answer grades correct, and the answer rounded as asked (40); none of 120 wrong values grades correct
- P3 `fluency-l1-tangent-approx.json` `families[1].widget` (estimate-a-power) | tool limit T8 | template "{key}"; 40 draws of family "estimate-a-power": every realised answer grades correct; none of 120 wrong values grades correct
- P3 `fluency-l6-matching-derivatives.json` `families[2].widget` (centred-cubic) | tool limit T8 | template "{key}"; 40 draws of family "centred-cubic": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l6-matching-derivatives.json` `families[1].widget` (trig-coefficient) | tool limit T8 | template "{r}"; 40 draws of family "trig-coefficient": every realised answer grades correct; none of 120 wrong values grades correct
- P3 `fluency-l6-matching-derivatives.json` `families[0].widget` (exponential-coefficient) | tool limit T8 | template "{r}"; 40 draws of family "exponential-coefficient": every realised answer grades correct; none of 80 wrong values grades correct

### testing (22)

- P1 `homework-2.json` `items[1].widget` (h-n-strict) | tool limit T2 | feedback.correct prints 208.3, then rounds to the whole number 209, which is accepted
- P1 `homework-2.json` `items[1].widget` (h-n-strict) | tool limit T2 | explain.text prints 208.3, then rounds to the whole number 209, which is accepted
- P3 `fluency-l13-matching-moments.json` `families[1].widget` (gamma-shape) | tool limit T8 | template "{key}"; 40 draws of family "gamma-shape": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l15-sharpness-of-the-peak.json` `families[1].widget` (poisson-se) | tool limit T8 | template "{key}"; 40 draws of family "poisson-se": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l17-ratio-of-likelihoods.json` `families[1].widget` (two-log-likelihoods) | tool limit T8 | template "{key}"; 40 draws of family "two-log-likelihoods": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l18-counts-against-expectations.json` `families[1].widget` (goodness-of-fit) | tool limit T8 | template "{key}"; 40 draws of family "goodness-of-fit": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l2-measuring-surprise.json` `families[1].widget` (z-null-nonzero) | tool limit T8 | template "{key}"; 40 draws of family "z-null-nonzero": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l13-matching-moments.json` `families[0].widget` (exponential-rate) | tool limit T8 | template "{key}"; 40 draws of family "exponential-rate": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l15-sharpness-of-the-peak.json` `families[0].widget` (bernoulli-information) | tool limit T8 | template "{key}"; 40 draws of family "bernoulli-information": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l17-ratio-of-likelihoods.json` `families[0].widget` (binomial-ratio) | tool limit T8 | template "{key}"; 40 draws of family "binomial-ratio": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l18-counts-against-expectations.json` `families[0].widget` (expected-cell) | tool limit T8 | template "{key}"; 40 draws of family "expected-cell": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l2-measuring-surprise.json` `families[0].widget` (z-null-zero) | tool limit T8 | template "{key}"; 40 draws of family "z-null-zero": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l13-matching-moments.json` `families[3].widget` (uniform-moment) | tool limit T8 | template "{key}"; 40 draws of family "uniform-moment": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l15-sharpness-of-the-peak.json` `families[3].widget` (volatility-se) | tool limit T8 | template "{key}"; 40 draws of family "volatility-se": every realised answer grades correct, and the answer rounded as asked (40); none of 120 wrong values grades correct
- P3 `fluency-l17-ratio-of-likelihoods.json` `families[3].widget` (poisson-ratio-test) | tool limit T8 | template "{key}"; 40 draws of family "poisson-ratio-test": every realised answer grades correct, and the answer rounded as asked (40); none of 120 wrong values grades correct
- P3 `fluency-l18-counts-against-expectations.json` `families[3].widget` (independence-df) | tool limit T8 | template "{key}"; 40 draws of family "independence-df": every realised answer grades correct; none of 78 wrong values grades correct
- P3 `fluency-l4-t-test.json` `families[1].widget` (sharpe-t) | tool limit T8 | template "{key}"; 40 draws of family "sharpe-t": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l13-matching-moments.json` `families[2].widget` (gamma-rate) | tool limit T8 | template "{key}"; 40 draws of family "gamma-rate": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l15-sharpness-of-the-peak.json` `families[2].widget` (exponential-se) | tool limit T8 | template "{key}"; 40 draws of family "exponential-se": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l17-ratio-of-likelihoods.json` `families[2].widget` (wilks-df) | tool limit T8 | template "{r}"; 40 draws of family "wilks-df": every realised answer grades correct; none of 77 wrong values grades correct
- P3 `fluency-l18-counts-against-expectations.json` `families[2].widget` (two-by-two) | tool limit T8 | template "{key}"; 40 draws of family "two-by-two": every realised answer grades correct, and the answer rounded as asked (40); none of 160 wrong values grades correct
- P3 `fluency-l4-t-test.json` `families[0].widget` (t-statistic) | tool limit T8 | template "{key}"; 40 draws of family "t-statistic": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct

### trig (18)

- P2 `problems-2.json` `items[0].parts[1].widget.wrong[0]` (p-water-wheel) | harmless H3 | slip "wrong-way" 0.0393 has band [-0.0107, 0.0893]; the answer 128.92 grades correct and the other slip keeps its own line; a typed 0 gets this line
- P2 `problems-2.json` `items[1].parts[0].widget.wrong[1]` (p-two-buoys) | harmless H3 | slip "b-itself" 0.628 has band [0.128, 1.128]; the answer 10 grades correct and the other 2 slips keep their own lines
- P3 `fluency-l1-squares-on-sides.json` `families[2].widget` (hypotenuse-2-dp) | tool limit T8 | template "{round(c, 6)}"; 40 draws of family "hypotenuse-2-dp": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l3-sides-and-angles.json` `families[2].widget` (height-with-tan) | tool limit T8 | template "{key}"; 40 draws of family "height-with-tan": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l4-exact-values.json` `families[3].widget` (combine-values) | tool limit T8 | template "{poly(r; kt, kr)}"; 40 draws of family "combine-values": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-arc-length.json` `families[2].widget` (radians-to-degrees) | tool limit T8 | template "{deg}"; 40 draws of family "radians-to-degrees": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l1-squares-on-sides.json` `families[1].widget` (short-side-whole) | tool limit T8 | template "{b}"; 40 draws of family "short-side-whole": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-sides-and-angles.json` `families[1].widget` (hypotenuse-from-side) | tool limit T8 | template "{round(key, 6)}"; 40 draws of family "hypotenuse-from-side": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l4-exact-values.json` `families[2].widget` (forty-five-triangle) | tool limit T8 | template "{poly(r; (1 - e)*c/2, e*c)}"; 40 draws of family "forty-five-triangle": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l1-squares-on-sides.json` `families[0].widget` (hypotenuse-whole) | tool limit T8 | template "{c}"; 40 draws of family "hypotenuse-whole": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-sides-and-angles.json` `families[0].widget` (side-from-hypotenuse) | tool limit T8 | template "{key}"; 40 draws of family "side-from-hypotenuse": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l4-exact-values.json` `families[1].widget` (height-with-tan) | tool limit T8 | template "{poly(r; tk, 0)}"; 40 draws of family "height-with-tan": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-arc-length.json` `families[1].widget` (degrees-to-radians-exact) | tool limit T8 | template "\\frac{{{p:c}\\pi}}{{{q}}}"; 40 draws of family "degrees-to-radians-exact": every realised answer grades correct, as do 40 accept forms; none of 80 wrong values grades correct
- P3 `fluency-l7-arc-length.json` `families[4].widget` (arc-length) | tool limit T8 | template "{round(s, 6)}"; 40 draws of family "arc-length": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l1-squares-on-sides.json` `families[3].widget` (short-side-2-dp) | tool limit T8 | template "{round(b, 6)}"; 40 draws of family "short-side-2-dp": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct
- P3 `fluency-l4-exact-values.json` `families[0].widget` (side-from-hypotenuse) | tool limit T8 | template "{poly(r; c*tp, c*rp)}"; 40 draws of family "side-from-hypotenuse": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-arc-length.json` `families[0].widget` (degrees-to-radians) | tool limit T8 | template "{k}"; 40 draws of family "degrees-to-radians": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l7-arc-length.json` `families[3].widget` (radians-to-degrees-1-dp) | tool limit T8 | template "{round(deg, 6)}"; 40 draws of family "radians-to-degrees-1-dp": every realised answer grades correct, and the answer rounded as asked (40); none of 80 wrong values grades correct

### validation (1)

- P1 `l4-nested.json` `quiz[3].widget` (q4) | tool limit T1 | explain.text prints 2000, the wrong value "norefit"; the answer 2010 is accepted

### vector-calc (1)

- P3 `fluency-l5-divergence-and-curl.json` `families[2].widget` (at-a-point) | tool limit T8 | template "{key}"; 40 draws of family "at-a-point": every realised answer grades correct; none of 56 wrong values grades correct

### vectors (5)

- P3 `fluency-l3-lengths-angles.json` `families[2].widget` (cosine-of-angle) | tool limit T8 | template "{key}"; 40 draws of family "cosine-of-angle": every realised answer grades correct; none of 74 wrong values grades correct
- P3 `fluency-l7-one-after-another.json` `families[0].widget` (one-entry) | tool limit T8 | template "{key}"; 40 draws of family "one-entry": every realised answer grades correct; none of 59 wrong values grades correct
- P3 `fluency-l10-undoing.json` `families[0].widget` (determinant) | tool limit T8 | template "{key}"; 40 draws of family "determinant": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-lengths-angles.json` `families[0].widget` (length) | tool limit T8 | template "{len}"; 40 draws of family "length": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-lengths-angles.json` `families[3].widget` (projection-multiple) | tool limit T8 | template "{key}"; 40 draws of family "projection-multiple": every realised answer grades correct; none of 80 wrong values grades correct

### tools/fixtures (not content) (13)

- P3 `fluency-l1-letters-for-numbers.json` `families[3].widget` (log-significant) | tool limit T8 | template "{x:sf3}"; 40 draws of family "log-significant": every realised answer grades correct; none of 40 wrong values grades correct
- P3 `fluency-l1-letters-for-numbers.json` `families[7].widget` (fractional-coefficient) | tool limit T8 | template "{r / m}"; 40 draws of family "fractional-coefficient": every realised answer grades correct; none of 34 wrong values grades correct
- P3 `fluency-l3-opening-brackets.json` `families[6].widget` (complete-the-square) | tool limit T8 | template "{a:c}({v}{h:+})^2{q:+}"; 40 draws of family "complete-the-square": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l1-letters-for-numbers.json` `families[6].widget` (falling-product) | tool limit T8 | template "{fact(n) / fact(n - r)}"; 40 draws of family "falling-product": every realised answer grades correct; none of 40 wrong values grades correct
- P3 `fluency-l3-opening-brackets.json` `families[1].widget` (factorise-common) | tool limit T8 | template "{a}({v}{b:+})"; 40 draws of family "factorise-common": every realised answer grades correct; none of 40 wrong values grades correct
- P3 `fluency-l3-opening-brackets.json` `families[5].widget` (factorise-fully) | tool limit T8 | template "{k}({v}{p:+})({v}{q:+})"; 40 draws of family "factorise-fully": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l1-letters-for-numbers.json` `families[1].widget` (exact-angle) | tool limit T8 | template "\\frac{{{p:c}\\pi}}{{{q}}}"; 40 draws of family "exact-angle": every realised answer grades correct; none of 40 wrong values grades correct
- P3 `fluency-l1-letters-for-numbers.json` `families[5].widget` (divide-reject) | tool limit T8 | template "{r:dp3}"; 40 draws of family "divide-reject": every realised answer grades correct, and the answer rounded as asked (40); none of 39 wrong values grades correct
- P3 `fluency-l3-opening-brackets.json` `families[4].widget` (add-fractions) | tool limit T8 | template "{total}"; 40 draws of family "add-fractions": every realised answer grades correct; none of 40 wrong values grades correct
- P3 `fluency-l1-letters-for-numbers.json` `families[0].widget` (fraction-lowest) | tool limit T8 | template "\\frac{{{p}}}{{{q}}}"; 40 draws of family "fraction-lowest": every realised answer grades correct; none of 40 wrong values grades correct
- P3 `fluency-l1-letters-for-numbers.json` `families[4].widget` (height-with-sine) | tool limit T8 | template "{ht:dp2}"; 40 draws of family "height-with-sine": every realised answer grades correct, and the answer rounded as asked (40); none of 39 wrong values grades correct
- P3 `fluency-l3-opening-brackets.json` `families[3].widget` (evaluate-linear) | tool limit T8 | template "{r}"; 40 draws of family "evaluate-linear": every realised answer grades correct; none of 80 wrong values grades correct
- P3 `fluency-l3-opening-brackets.json` `families[7].widget` (roots-numeric) | tool limit T8 | template ["{r}","{s}"]; 40 draws of family "roots-numeric": every realised answer grades correct; none of 40 wrong values grades correct

### exams/mock-oa-sig (1)

- P2 `mock-oa-sig.json` `parts[0].items[8].widget.wrong[1]` (q09-bayes) | harmless H3 | slip "base" 0.01 has band [0.005, 0.015]; the answer 0.161017 grades correct and the other slip keeps its own line

### exams/stage-3 (8)

- P1 `stage-3.json` `parts[0].items[11].parts[1].widget` (a-informed-buyer) | harmless H1 | 2 places asked; 63.53 accepted, 63.54 and 63.52 refused
- P1 `stage-3.json` `parts[0].items[11].parts[2].widget` (a-informed-buyer) | harmless H1 | 2 places asked; -8.53 accepted, -8.52 and -8.54 refused
- P1 `stage-3.json` `parts[2].items[6].widget` (r-turnover-cost) | harmless H1 | 2 places asked; 0.79 accepted, 0.8 and 0.78 refused
- P1 `stage-3.json` `parts[2].items[7].parts[0].widget` (r-t-bar) | content fault F2 | 2.75 accepted, 2.76 and 2.74 refused; two places asked, no working printed; a standard error kept to three places (3.1/sqrt(360) = 0.163) gives 0.45/0.163 = 2.76 | fix: `"tol": {"abs":0.01}` (was `{"abs":0.005}`); with it the grader takes 2.76, 2.75 and the 2 wrong values keep their own lines
- P1 `stage-3.json` `parts[2].items[8].parts[1].widget` (r-small-share) | harmless H1 | 2 places asked; 1.07 accepted, 1.08 and 1.06 refused
- P1 `stage-3.json` `parts[2].items[11].widget` (r-best-of-twenty) | content fault F2 | 0.23 accepted, 0.24 and 0.22 refused; two places asked and the answer 0.225156 sits on the rounding edge; tables at z = 2.24 give 1 - 0.9875^20 = 0.2224, so 0.22; the explanation's own 1 - 0.775 = 0.225 also rounds either way | fix: `"tol": {"abs":0.006}` (was `{"abs":0.005}`); with it the grader takes 0.22, 0.23, 0.225 and the 2 wrong values keep their own lines
- P1 `stage-3.json` `parts[2].items[14].parts[0].widget` (r-oos-power) | harmless H1 | 2 places asked; 1.41 accepted, 1.42 and 1.4 refused
- P1 `stage-3.json` `parts[2].items[14].parts[1].widget` (r-oos-power) | harmless H1 | 2 places asked; 0.28 accepted, 0.29 and 0.27 refused

### exams/topic-0.2 (1)

- P1 `topic-0.2.json` `items[22].widget` (e-formula) | harmless H1 | 2 places asked; 2.77 accepted, 2.78 and 2.76 refused

### exams/topic-0.3 (2)

- P1 `topic-0.3.json` `items[8].widget` (e-truss-angle) | harmless H1 | 1 place asked; 44.4 accepted, 44.5 and 44.3 refused
- P1 `topic-0.3.json` `items[16].widget` (e-tech-pick) | harmless H1 | 3 places asked; 0.424 accepted, 0.425 and 0.423 refused

### exams/topic-1.10 (4)

- P1 `topic-1.10.json` `items[2].widget` (e-telescope-gap-three) | harmless H1 | 4 places asked; 0.6111 accepted, 0.6112 and 0.611 refused
- P1 `topic-1.10.json` `items[13].widget` (e-ftc-both-limits) | harmless H1 | 4 places asked; -0.0154 accepted, -0.0153 and -0.0155 refused
- P1 `topic-1.10.json` `items[24].parts[1].widget` (e-hedge-residual) | harmless H1 | 2 places asked; 2.61 accepted, 2.62 and 2.6 refused
- P1 `topic-1.10.json` `items[26].parts[1].widget` (e-chain-response) | harmless H1 | 3 places asked; 2.662 accepted, 2.663 and 2.661 refused

### exams/topic-1.11 (1)

- P1 `topic-1.11.json` `items[20].widget` (e-euler-by-hand) | harmless H1 | 3 places asked; 1.547 accepted, 1.548 and 1.546 refused

### exams/topic-2.3 (1)

- P2 `topic-2.3.json` `items[26].widget.wrong[0]` (e-bump-size) | harmless H3 | slip "square-root" 0.0000015 has band [5e-7, 0.0000025]; the answer 0.0012 grades correct

### exams/topic-2.5 (4)

- P1 `topic-2.5.json` `items[21].parts[2].widget` (e-projection-kkt) | tool limit T1 | explain.text prints 1.68, the wrong value "predicted"; the answer 1.682 is accepted
- P1 `topic-2.5.json` `items[27].parts[0].widget` (e-solver-certificate) | tool limit T1 | explain.text prints 12, the wrong value "optimum"; the answer 11.996667 is accepted
- P2 `topic-2.5.json` `items[3].widget.wrong[0]` (e-double-gap) | tool limit T7 | slip "at-one" 2.220446049e-16 has band [2.218225603e-16, 2.222666495e-16]; the answer 4.656612873e-10 grades correct and the other 2 slips keep their own lines; a typed 0 gets this line; authored tol is 0.1% of the value 2.2e-16
- P2 `topic-2.5.json` `items[14].widget.wrong[1]` (e-log-condition) | harmless H3 | slip "inverse" 0.0198 has band [0.0098, 0.0298]; the answer 50.4983 grades correct and the other slip keeps its own line

### exams/topic-2.6 (2)

- P1 `topic-2.6.json` `items[8].widget` (e-orders-per-arm) | tool limit T2 | feedback.correct prints 317.9, then rounds to the whole number 318, which is accepted
- P1 `topic-2.6.json` `items[8].widget` (e-orders-per-arm) | tool limit T2 | explain.text prints 317.9, then rounds to the whole number 318, which is accepted

### exams/topic-3.1 (12)

- P1 `topic-3.1.json` `items[0].widget` (e-monthly-from-annual) | harmless H1 | 2 places asked; 1.07 accepted, 1.08 and 1.06 refused
- P1 `topic-3.1.json` `items[8].widget` (e-lowest-match) | harmless H1 | 2 places asked; 0.22 accepted, 0.23 and 0.21 refused
- P1 `topic-3.1.json` `items[9].parts[0].widget` (e-capital-split) | harmless H1 | 2 places asked; 0.73 accepted, 0.74 and 0.72 refused
- P1 `topic-3.1.json` `items[15].widget` (e-bounce-share) | harmless H1 | 1 place asked; 19.5 accepted, 19.6 and 19.4 refused
- P1 `topic-3.1.json` `items[16].widget` (e-gap-in-se) | harmless H1 | 2 places asked; 0.78 accepted, 0.79 and 0.77 refused
- P1 `topic-3.1.json` `items[18].parts[0].widget` (e-convergence-pooled) | harmless H1 | 1 place asked; 60.8 accepted, 60.9 and 60.7 refused
- P1 `topic-3.1.json` `items[21].widget` (e-nw-hand) | harmless H1 | 2 places asked; 2.16 accepted, 2.17 and 2.15 refused
- P1 `topic-3.1.json` `items[23].parts[0].widget` (e-after-pub) | harmless H1 | 1 place asked; 36.4 accepted, 36.5 and 36.3 refused
- P1 `topic-3.1.json` `items[23].parts[1].widget` (e-after-pub) | harmless H1 | 2 places asked; -1.14 accepted, -1.13 and -1.15 refused
- P1 `topic-3.1.json` `items[24].parts[0].widget` (e-break-even-net) | harmless H1 | 2 places asked; 0.72 accepted, 0.73 and 0.71 refused
- P1 `topic-3.1.json` `items[24].parts[1].widget` (e-break-even-net) | harmless H1 | 2 places asked; 0.57 accepted, 0.58 and 0.56 refused
- P1 `topic-3.1.json` `items[27].parts[0].widget` (e-skip-event) | harmless H1 | 2 places asked; 0.37 accepted, 0.38 and 0.36 refused

### exams/topic-3.4 (3)

- P1 `topic-3.4.json` `items[16].parts[0].widget` (e-two-function-metrics) | harmless H1 | 4 places asked; 0.3849 accepted, 0.385 and 0.3848 refused
- P1 `topic-3.4.json` `items[28].parts[0].widget` (e-plane-contraction) | harmless H1 | 4 places asked; 0.3333 accepted, 0.3334 and 0.3332 refused
- P1 `topic-3.4.json` `items[28].parts[2].widget` (e-plane-contraction) | harmless H1 | 4 places asked; 1.9678 accepted, 1.9679 and 1.9677 refused

## Rule changes proposed

Counts are entries of this triage. Each change is for an engine agent; none was made here.

`[tight-band]`, printed-figure check (77 entries: 6 faults, 13 harmless, 58 tool limit):

1. Fire only when the printed figure is the stored answer rounded to fewer places (`2.47` against `2.4749`, `0.46` against `0.4615`) and is not one of the item's `wrong[]` values. This test keeps all 6 faults and drops classes T1 (24), T2 (20), T3 (3) and T4 (10), where the figure is a slip, a pre-rounding value or another quantity. If that test is not wanted, three narrow skips remove 47 of those 57: a figure equal to a `wrong[]` value; a whole-number answer with `tol.abs` of 0.5 or less; a figure followed by `\ldots`.
2. Where the question asks for k places (or a fraction) and the figure has fewer than k, report it under a separate advisory on the explanation text, not as a band fault (class H2, 13). The band is right; the text is rounded more coarsely than the form it asks for.
3. Read `49{,}988` as 49,988 (class T5, 1).

`[tight-band]`, rounded-as-asked check (2 entries, both tool limit):

4. Take "whole number" as a rounding only from the question, or from prose only in "nearest whole number" or "Give a whole number" (class T6, 2). "A whole number from 1 to 100 is picked" is not a form.

`[tight-band]`, half-unit check (70 entries: 2 faults, 68 harmless):

5. Fire only when the stored answer lies within 0.1 of a unit of a rounding edge (0.225156 at 2 places, 2.754242 at 2 places). That keeps both faults (class F2) and cuts the 70 to 11. Away from an edge a working with rounded figures still rounds to the stored answer, which is what the 68 of class H1 show.

`[wide-wrong-band]` (36 entries: 0 faults, 34 harmless, 2 tool limit):

6. Fire only when the wrong band reaches the answer band or another `wrong[]` value, the two cases in which it can take a right answer's line or another slip's line. None of the 36 does either. A small slip with an absolute band a little wider than itself (class H3, 32) is the normal way to catch the slip rounded as asked.
7. Measure the band from the authored `tol`, not from `tol` plus the grader's float slack (class T7, 2). Engine note from the same two items: the slack (1e-9 absolute, 1e-12 relative in `grade.js within`) is wider than a wrong value of 1e-12 or 2.2e-16, so a typed 0 gets that slip's line.

`grade-regression.mjs` self-grade note (257 entries, all tool limit):

8. Leave out of the "do not grade correct themselves" count any answer that holds a template: `{...}` in a `fluency-*.json` family (class T8, 256, of which 13 are fixtures under `tools/fixtures/fluency`) and `{{carry...}}` (class T9, 1). With those out the count is 0. Better, draw each family as `fluency-selfgrade.mjs` does here and grade the realised answers: 10,240 draws, none refused, none of 20,198 wrong values graded correct.
9. Do not walk `tools/fixtures` when `--content` is the app folder, or report fixtures apart from content.
