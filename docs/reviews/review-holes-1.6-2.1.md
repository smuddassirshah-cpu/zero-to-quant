# Syllabus holes 1.6 and 2.1: second-reader findings

Read at commit 77d4c90. A full second read of content written in session AB and not read before. Patterns: `review-holes-0.1-0.2.md`, `review-problems-1.5-a.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not give what the learner needs, or refuses or mis-marks a sensible entry; `minor` = weak part, loose chain, loose `wrong` entry, wording, freshness, tagging, coverage or tooling.

Scope.

- Exams: the four new items of `app/content/exams/topic-1.6.json` (`s-uniform-moments`, `s-chi-order-mix`, `s-pool-rates`, `s-pareto-losses`; seven graded parts) and the five of `topic-2.1.json` (`e-spline-slope`, `e-street-inside`, `e-kmeans-spreads`, `e-unit-gradient`, `e-report-which`), and the five items `topic-2.1` dropped.
- Skills: `ht-theory`, `ht-likelihood` and `sl-flexible`, on every lesson, review, homework, problem and exam item of level 4 of `testing` and `stat-learning`.
- Problem sets: `testing/problems-4.json` (4 problems, 20 parts) and `stat-learning/problems-4.json` (4 problems, 19 parts), against `docs/briefs/chained.md`.
- Fluency: all eight new sets, 29 families (testing l13, l15, l17, l18: 16; stat-learning l15 to l18: 13), 20 draws a family, 580 draws.

Method. The six authors' scripts were run first. Every graded key and every `wrong` value was then worked by hand from the item's text and again in `review-holes-1.6-2.1-scripts/mine.py`, with no import from the authors' scripts and by another route where one exists (SciPy's `chisquare`, `chi2_contingency`, Poisson and binomial pmfs, a Gamma integral for the unbiased rate estimator, a finite difference for each gradient and each Fisher information, a literal k-means loop and a search over every split). Every fluency draw was recomputed from its prompt text alone (`fluency-read.py`: regex on the sentence the learner reads, never the draw's `vars` or `lets`). Every typed part then went through the engine's own grader in node (`grade-probe.mjs`, `fluency-probe.mjs`: `numGrade` of `app/js/engine/grade.js`): the answer, each `wrong` entry on its own key, and strings of my own for what a right learner would type (fractions for decimals, more places, a letter and `=` in front, a true minus sign, the unit or % the prompt names, a thousands comma) and what a learner one step short would type (one place short, the value from rounded logs or rounded expected counts, the question's own intermediate). The theory was checked from first principles, not from the lessons: each Fisher information by a numerical second derivative, the Cramér-Rao regularity of each model, each sufficiency claim by factorisation and a counter-example where one exists, Wilks' count as free parameters removed, each chi-squared count, the margin as a distance, k-means as assign then mean, linkage rules, layer parameter counts, ReLU as a hinge.

Tool results.

| check | result |
|---|---|
| authors' number scripts (scratchpad venv) | `exam-1.6-holes` 90 of 90; `exam-2.1-holes` 72 of 72; `problems-testing` 309 checks, 0 failures; `problems-stat-learning` 286, 0; `fluency-testing` 11,974, 0; `fluency-stat-learning` 7,800, 0; all exit 0 |
| `mine.py` (reader's own keys, slips and claims) | 356 checks, 0 failures; one check confirms a false claim (finding 10) |
| `fluency-read.py` (580 draws from the prompt text) | 5,354 checks, 0 failures, 65 notes read (findings 16, 17) |
| `grade-probe.mjs` (engine grader, problems and exam items) | 528 checks over 44 parts, 0 failures, 11 rows held to be faults (findings 5, 8, 11) |
| `fluency-probe.mjs` (engine grader, every draw) | 3,274 checks, 0 failures, 18 classes of row against the reader (findings 16 to 20) |
| `shares.py` (200 draws of six families; the exam and problem parts with logs) | shares quoted in findings 1, 16, 17, 19, 23 |
| `proposed.py` (numbers of the fixes below) | 37 checks pass |
| `try-fixes.py` (the fluency fixes of findings 16 to 19 and 22 on copies, 200 draws each) | all pass |
| `skills.py` (every skill tag of the two levels and exams) | 0 unknown tags |
| validator | 0 errors; no warning on any file or item in scope (the warnings on the two exams are on older items: `s-welch`, `s-overlap-hac`, `s-vol-annual`, `e-rf-variance`); `manifest.json` unchanged |
| playthrough `--problems` both sets, `--exam topic-1.6` and `topic-2.1`, `--local-cdn` | all passed, desktop and `--mobile` |
| voice scan 35, `stat-learning`, `exams` | 0 and 0 each; `testing` 1 over 35 words, in `homework-3.json` (not in scope) |
| `fresh-check.mjs --file` both sets; `--exam` both | 0 hits; 6 advisories on `testing/problems-4` (shared formulas) read. Four reuses the tool missed are findings 3, 9 and 13 |

Result. Every graded key agrees with mine: all 39 problem parts, all 12 graded exam parts and all 580 fluency draws. Every `wrong` value is the slip its line describes and lands on its own key. None of the ten `wrong` findings of `review-stat-learning-4.md` recurs: no `wrong` value disagrees with its own feedback, no claim about scikit-learn or runtimes is made, no accuracy is split into bias and variance, the spline counts follow the level's rule (a cubic piece has 4 coefficients and each interior knot adds 1).

There are three `wrong` findings, all of them sentences, not keys: a feedback line that tells a learner with the right method that they used Pearson's statistic (1), a rule about sufficiency that is false as stated (2), and an explanation that says a gradient step lowers a loss which it more than doubles (10). Five are `unclear`, and all five mark a sensible entry wrong (11, 16 to 19).

The judgement asked for on `topic-2.1` is finding 4: two lessons lost their only exam item, `stat-learning` l10 and `ensembles` l7.

Claims checked beyond the keys: $(n - 1)/\sum x_i$ is unbiased for an exponential rate with variance $\lambda^2/(n - 2)$ (Gamma integral, $n = 40$); $E[X_1 \mid T]$ is $T/12$ by the binomial law of $X_1$ given $T$; the six expected counts of the bakery table and $G = 7.242$; $P(\chi^2_2 \ge x) = e^{-x/2}$; the 5% cut-offs 3.841, 5.991 and 11.07; $-2\ln\Lambda$ for one Poisson mean and for two pooled rates by `logpmf`; the Pareto density integrates to 1 and its MLE by numerical maximisation; the settled k-means split in `e-kmeans-spreads` and `p-order-sizes` is the best split of all; the unit in each network item is on; $1{,}182$ is the first $n$ with $t \ge 3$.

## A. Exam items and skill tags

1. `wrong` | `exams/topic-1.6.json` | `s-pool-rates` | `widget.rows[0][0].wrong` `pearson` and `feedback.byKey.pearson`.
   The item asks for 2 decimal places. A learner who uses the right formula with $\ln 1.2 = 0.182$ and $\ln 0.8 = -0.223$ gets $2(16.38 - 13.38) = 6.00$ exactly, which sits on the `pearson` entry (6.0 ± 0.001). They are told "You found Pearson's $X^2$", which they did not. Logs to 2 places give 6.00 too; 4 places give 6.042, which is accepted (`shares.py`).
   Fix: `question` "Fill in $-2\\ln\\Lambda$, to 2 decimal places, and the degrees of freedom of its $\\chi^2$ limit. Keep 5 decimal places in each logarithm." `byKey.pearson` "6.00 is Pearson's $X^2$, $\\tfrac{15^2}{75} + \\tfrac{15^2}{75}$. Logarithms rounded to 3 places give it too. With 5 places, $-2\\ln\\Lambda = 6.04$."

2. `wrong` | `exams/topic-1.6.json` | `s-pareto-losses` | `parts[0].widget.options[2].why`.
   "The maximum is sufficient when the support moves with the parameter, as for a uniform." False as a rule. For a shifted exponential on $x > \theta$ the minimum is sufficient and the maximum is not (`mine.py`: two samples with one maximum have a likelihood ratio that moves with $\theta$). For the uniform on $(-\theta, \theta)$ of this exam's own `s-uniform-moments` it is $\max |x_i|$.
   Fix: "The largest value is sufficient for a uniform on $(0, \\theta)$, whose upper end is the parameter. Here the support, $x > 1$, is fixed."

3. `minor` | `exams/topic-1.6.json` | `s-pareto-losses` | freshness against `courses/estimation/homework-2.json` `hw2-pareto-tail`.
   The exam covers `estimation` as well as `testing`. Homework 2 of `estimation` opens "A desk records every loss above £1m. In £m, it models each such loss $X$ as Pareto, with density $f(x) = \alpha x^{-\alpha - 1}$", and its part (a) derives $\hat\alpha = n/\sum \ln x_i$ with the second-derivative check. The exam item has the same desk, threshold, density and estimate; its part 2 is that derivation with numbers. The author's check ran against `testing` only ("a Pareto model ... appear nowhere in the course"). `fresh-check --exam topic-1.6` reports nothing.
   Fix, every key kept (`proposed.py`): use the density $\theta x^{\theta - 1}$ on $(0, 1)$, which no file of `estimation`, `testing`, `regression` or the stage exams holds; "recovery rate" is unused there too.
   - `title` "Recovery rates: summary, estimate, floor". `prose` "Recovery rates on defaulted loans, as fractions $x$ between 0 and 1, follow the density $f(x \\mid \\theta) = \\theta x^{\\theta - 1}$, so $\\ln f = \\ln\\theta + (\\theta - 1)\\ln x$. A desk has 80 independent recoveries with $\\sum \\ln x_i = -32$."
   - Part 1: options unchanged but for `c.why` "The largest value is sufficient for a uniform on $(0, \\theta)$, whose upper end is the parameter. Here the support, $0 < x < 1$, is fixed." `feedback.correct` "The joint density is $\\theta^n \\exp\\big((\\theta - 1)\\sum\\ln x_i\\big)$, a function of $\\theta$ and $\\sum \\ln x_i$ only." `explain` "$\\prod \\theta x_i^{\\theta - 1} = \\theta^n \\big(\\prod x_i\\big)^{\\theta - 1} = \\theta^n e^{(\\theta - 1)\\sum\\ln x_i}$. The data meet $\\theta$ only through $\\sum \\ln x_i$, so by the factorisation theorem it is sufficient. The product $\\prod x_i$ carries the same information."
   - Part 2: answer 2.5; `wrong` `upside-down` 0.4, `exponent` 3.5, and a new `sign` $-2.5$. `feedback.correct` "$\\tfrac{n}{\\theta} + \\sum\\ln x_i = 0$ gives $\\hat\\theta = \\tfrac{80}{32} = 2.5$." `generic` "Not quite right. Differentiate $n\\ln\\theta + (\\theta - 1)\\sum\\ln x_i$ in $\\theta$ and set it to 0." `byKey.exponent` "You set $\\theta - 1 = 2.5$. The power drops out on differentiating: the slope is $\\tfrac{n}{\\theta} + \\sum\\ln x_i$." `byKey.sign` "You lost a sign. $\\sum \\ln x_i = -32$ is negative, so $\\hat\\theta = -\\tfrac{n}{\\sum\\ln x_i}$ is positive." `explain` "The log-likelihood is $\\ell(\\theta) = 80\\ln\\theta - 32(\\theta - 1)$. Its slope $\\tfrac{80}{\\theta} - 32$ is 0 at $\\theta = 2.5$, and $\\ell'' = -\\tfrac{80}{\\theta^2} < 0$, so it is a peak. So $\\hat\\theta = 2.5$."
   - Part 3: $\alpha$ to $\theta$ throughout, "from the 80 recoveries", "The support $0 < x < 1$ does not move with $\\theta$"; key 0.078125 and all three `wrong` values unchanged.

4. `minor` (coverage) | `exams/topic-2.1.json` | the five replaced items.
   Three of the five drops leave their lessons examined: `e-leak-rows` (leakage keeps `e-lookahead-lines` and three more), `e-ridge-shrink` (ridge stays in `e-code-ridge-inter` and `e-bias-var-table`), `e-walk-first-test` (walk-forward folds stay in `e-code-purged-roll`, `e-boost-recipe`, `e-code-honest-report`). Two do not.
   - `e-odds-update` was the only item that reads a logistic coefficient as odds, the stated objective of `stat-learning` l10. Level 3 of `stat-learning` now has `e-precision-recall` (l12), `e-kelly-wrong` (l13) and two items on an honest hit rate (l14); "odds" appears only in two Kelly items and "logistic" only as a model name in two others. l10 has no item.
   - `e-oob-overlap` was the only item on out-of-bag error, which is the whole of `ensembles` l7. No item of the exam now holds "out-of-bag" or "OOB". `en-bagging` keeps two items, as the author's script checks, but neither is on l7.
   Fix: put `e-odds-update` (difficulty 3, key 21.5%, `proposed.py`) back in place of `e-report-which` (difficulty 3). The ramp stays 6, 15, 6, 3. `e-report-which` asks "choose on validation, report the test score", which `e-code-honest-report` and `e-best-of-n` already examine, and which review-4 `r-gamma-tie`, homework-4 `h-pick-learner` and two of the four problems of `problems-4` drill (finding 13). Level 4 keeps four items on l15 to l18. For l7, either put `e-oob-overlap` back in place of `e-importance-claims` or `e-rf-variance` (both difficulty 3 on `en-bagging`), or record the gap in `KNOWN_ISSUES.md`.
   `topic-1.6` dropped `s-summary-dw` only: Durbin-Watson stays in `s-residual-plots`, so nothing is lost there.

5. `minor` | `exams/topic-2.1.json` | `e-spline-slope` and `e-kmeans-spreads` | `widget.placeholder`.
   The placeholders read "bp a year" and "bp squared". A learner who types the placeholder's words after the number, "2.5 bp a year" or "91 bp squared", is stopped: the field does not read them and will not submit ("2.5 bp" and "91 bp^2" pass). "2.5 basis points" is stopped too. This is finding 9 of the pattern review again.
   Fix: `placeholder` "a number" on both. See finding 8 and Engine.

6. `minor` | skill tags | `courses/testing/review-4.json` `r-chi-23`, `exams/topic-1.6.json` `s-chi-order-mix`.
   The re-tagging is honest. Every item under `ht-theory` is on moments, sufficiency, Rao-Blackwell, information or the Cramér-Rao bound (l13 to l16; eleven review and homework items, and `h-analyst` with both new skills; `p-disk-failures`, `p-website-signups`; `s-uniform-moments`, `s-pareto-losses`). Every item under `ht-likelihood` is a likelihood ratio, Neyman-Pearson or chi-squared item. Every item under `sl-flexible` is on margins, clusters, networks or splines, and each second tag is earned (`sl-classify` on the four margin items, `sl-linear` on the spline items and on `p-one-unit`, whose last part reads the unit as a hinge). l19 and its items rightly stay on `sl-setup` and `sl-tradeoff`. No item is left on a placeholder.
   One tag is loose: `ht-pvalue` sits on `r-chi-23` ("What is $X^2$?") and on `s-chi-order-mix`, which ask for a statistic and a cut-off decision; a p-value appears only in each explanation. `h-gof-code` and `p-bakery-loaves` do ask for one.
   Fix (optional): drop `ht-pvalue` from `r-chi-23`; keep it on `s-chi-order-mix`, whose second part is the test decision.

Notes, no change asked. `s-uniform-moments` accepts 0.599 (central moment), "0.6 ticks" and `3/5`. `s-pareto-losses` part 3 accepts 0.0781, 0.078125 and `5/64` and refuses 0.078. `e-unit-gradient` and the problems take a true minus sign. `e-street-inside`: $(0, 0)$ has value exactly 1 and is rightly outside "strictly inside". `e-report-which`: the key is not the longest option by the validator's rule.

## B. `testing/problems-4.json`

The chained rules hold. Each later part restates the value it needs; each rounded part names its places; each band takes the value its own feedback prints (also from the unrounded value, `grade-probe.mjs`); 18 of 20 parts are typed; difficulties 3, 4, 4, 5; l13 to l18 each appear and each problem draws on two or more lessons; each `carried` entry is the answer that follows from the slip named in the part before. Percentages typed for the efficiencies and the p-value ("95%", "8.33%", "2.81%") are accepted.

7. `minor` | `p-website-signups` | `parts[0].widget.options[2].why` and `feedback.byKey.largest`.
   "The largest count is the uniform's sufficient statistic." True only for a uniform on $(0, \theta)$; see finding 2.
   Fix, both places: "The largest value is sufficient for a uniform on $(0, \\theta)$. Poisson probabilities depend on the data through the total."

8. `minor` | both problem sets | a unit typed after the number.
   "0.4 failures a day" and "0.4 a day" (`p-disk-failures` part 1, whose question says "in failures a day"), "3.8 a night" (`p-night-admissions` part 1), "4.5 sign-ups" (`p-website-signups` part 2) and "7 h" (`stat-learning` `p-one-unit` part 1) do not parse: the field shows its help line and will not submit. "50 hours", "28 loaves", "20 nights", "38.4 bp" and "7 hours" pass. Nothing is marked wrong.
   Fix: none in content for the multi-word units; add `"unit": "h"` to `p-one-unit` part 1. See Engine (already raised by the pattern review).

9. `minor` | `p-disk-failures` part 5 and `p-bakery-loaves` | freshness.
   Part 5 is l16 screen 6 with a new $n$: the same estimator $\tfrac{n - 1}{\sum x_i}$, the same variance $\tfrac{\lambda^2}{n - 2}$, the same question ("what is its efficiency"), there with $n = 10$ and here with 40. `fresh-check` lists it as an advisory only. `p-bakery-loaves` is a 2 by 3 table of 200 tested for independence, as review-4 `r-chi-23` is; the numbers and story differ, so no change is asked there.
   Fix (optional, low priority): keep part 5 and add nothing, or turn it round so it is not the lesson's question: "The estimator $\\tfrac{n - 1}{\\sum x_i}$ is unbiased, with variance $\\tfrac{\\lambda^2}{n - 2}$, against the bound $\\tfrac{\\lambda^2}{n}$ of part 4. How many gaps make its efficiency at least 0.99?" Key 200 (from $\\tfrac{n - 2}{n} \\ge 0.99$); `wrong` 198 (the 2 taken off again after solving) and 0.95 (the efficiency at 40) (`proposed.py`).

## C. `stat-learning/problems-4.json`

Keys, restated values, forms and coverage hold: l15 (`p-spam-filter`), l16 (`p-order-sizes`, k-means only), l17 (`p-one-unit`, `p-renewals`), l18 (`p-order-sizes` part 4, `p-one-unit` part 5), l19; 16 of 19 parts typed; difficulties 3, 4, 5, 4.

10. `wrong` | `p-one-unit` | `parts[3].explain` (and the story of part 5).
    "The slope is negative, so raising $w_1$ lowers the loss. A step of 0.01 against it moves $w_1$ from 0.5 to 0.98." The step does the opposite. At $w_1 = 0.98$ the prediction is $2(7.84 - 1) + 1 = 14.68$ hours against a target of 10, and the loss is 10.95, up from 4.5 (`mine.py`, `proposed.py`). The row is fitted at $w_1 = 0.6875$; any $\eta$ above 0.0078 raises the loss. A learner is told that a step against the slope lowered the loss when it more than doubled it. The graded keys (0.98, knot 1.020) are right.
    Fix, text only, keys kept: `parts[3].explain` "The slope is negative, so a small rise in $w_1$ lowers the loss. This step is too long: at $w_1 = 0.98$ the prediction is 14.68 hours and the loss 10.95, up from 4.5. That is why $\\eta$ is kept small."
    Fuller fix, if a step that works is wanted (`proposed.py`): $\eta = 0.002$ in part 4. New $w_1 = 0.596$, prediction 8.536, loss 1.07. Part 4: answer 0.596, `uphill` 0.404, `no-rate` 48.5, `carried` 0.518. Part 5 ("with $w_1 = 0.596$ from part 4"): answer 1.678, `old-knot` 2, `sign` $-1.678$, `carried` 1.931; explanation "... so one step moved the bend from 20 km to about 16.8 km."

11. `unclear` | `p-order-sizes` | parts 1 and 2 | a % sign.
    The prose gives the sizes "as % of daily volume" and part 4 speaks of "an order of 20% of volume". A learner who answers part 1 with "18%" or part 2 with "22%" is marked wrong with the generic line "Send each order to the nearer centre, then average each group": the grader reads a typed % as a hundredth, 0.18 (`grade-probe.mjs`).
    Fix: add to `parts[0].widget.wrong` `{ "id": "percent-sign", "value": 0.18, "tol": { "abs": 0 } }` and to `parts[1].widget.wrong` `{ "id": "percent-sign", "value": 0.22, "tol": { "abs": 0 } }`, each with `byKey` `"percent-sign": "That is the right centre. Type the number alone, with no % sign."` Or reword the prose to "six order sizes, in lots" and part 4 to "an order of 20 lots".

12. `minor` | `p-order-sizes` | `parts[2].widget.wrong` `carried`.
    The entry is 91, the inertia of the settled groups about centres 3 and 18. No slip in part 2 leads there. The slip part 2 names, `no-reassign` (6 kept in group 2, centres 3 and 18), gives $1 + 1 + 144 + 0 + 16 + 64 = 226$, which gets the generic line.
    Fix: add `{ "id": "not-settled", "value": 226, "tol": { "abs": 0 } }` with `byKey` `"not-settled": "You left 6 in the second group, with centres 3 and 18. After the loop settles the groups are 2, 4, 6 and 18, 22, 26."` Keep `carried`.

13. `minor` | `p-spam-filter` parts 4 and 5, `p-renewals` parts 2 and 3 | the same two steps twice, and both from homework-4.
    Both problems end "a tie on validation goes to the simpler learner" (with the same `why` lines: "A tie goes to the simpler, more explainable model", "Choosing on the test rows uses them up") and then "what is the $t$ statistic of its hit rate against the base rate", with the same three slips. That pair is homework-4 `h-pick-learner` ("Two learners tie at 0.61 on validation, and the tie goes to the simpler ... $t$-statistic of its test accuracy against the base rate"), and the $t$ statistic is also review-4 `r-t-edge`, l19 and two screens of l14. In `p-spam-filter` neither part uses an earlier answer, so the chain stops at part 3. `fresh-check` reports nothing.
    Fix: replace `p-spam-filter` part 4 (the choice) with a typed part that continues the chain, and keep part 5 as the l19 step. Part 4 `question` "Refitted with a smaller $C$, the filter has $w = (0.9, -1.2)$ and $b = 0.3$: the same centre line. Using the margin 0.4 from part 1, what is the margin now? Give 3 decimal places." Answer 0.667, band 0.0005; `wrong` `gave-norm` 1.5, `street-width` 1.333, `unchanged` 0.4 ("That is the old margin. The new $\\lVert w \\rVert$ is 1.5."); `explain` "$\\lVert w \\rVert = \\sqrt{0.81 + 1.44} = 1.5$, so the margin is $\\tfrac{1}{1.5} \\approx 0.667$. A smaller $C$ charges less for intrusions, so the street widens, here by a factor of $\\tfrac{5}{3}$." (`proposed.py`.) The set then has 17 of 19 parts typed.

14. `minor` | `p-spam-filter` `prose`, and `fluency-l15-widest-street.json` family `margin` `prompt` | a hypothesis.
    "The margin is $1/\lVert w \rVert$" holds only when the weights are scaled so the edges are $w \cdot x + b = \pm 1$. The exam item `e-street-inside` says so; these two do not, and the same line with doubled weights has half the "margin".
    Fix: `p-spam-filter` `prose` "... It has $w = (1.5, -2)$ and $b = 0.5$, scaled so the street's edges are $w \\cdot x + b = \\pm 1$, and a positive decision value means spam." Family `margin` `prompt` "A fitted linear SVM has $w = ({w1}, {w2})$ and $b = {b}$, with edges at $w \\cdot x + b = \\pm 1$. What is its margin, the distance from the centre line to either edge? Give 4 decimal places."

15. `minor` | `p-renewals` | `parts[1].explain`.
    "It varies less on new rows than one with 129" is stated as a fact. A parameter count is a guide to variance, not a law (a heavily penalised network can vary less than an unpenalised line).
    Fix: "With equal validation scores, the learner with 7 parameters wins. As a rule it varies less on new rows than one with 129, and it is easier to explain. The test rows then give it one honest score."

## D. Fluency sets

All 580 answers agree with mine from the prompt text; every `wrong` value is the slip its line names; an entry is dropped only where it would sit on the answer or on another entry; every solution prints the answer at the rounding asked. Shapes can exist: the k-means draws have no tie and leave 2 to 4 shares with the second centre; every unit in `slope-first-weight` is on; every $2 \times 2$ table adds up. The theory lines are right: $I(p) = \tfrac{1}{p(1 - p)}$, $I(\lambda) = \tfrac{1}{\lambda}$ (Poisson) and $\tfrac{1}{\lambda^2}$ (exponential), $I(\sigma) = \tfrac{2}{\sigma^2}$ with the mean known, Wilks' count as parameters fixed, $(r - 1)(c - 1)$, average linkage of a pair as the mean of the two distances.

16. `unclear` | `testing/fluency-l18-counts-against-expectations.json` | family `two-by-two` | `widget.tol` and `prompt`.
    "Give 3 decimal places" with a band of 0.0005. l18 teaches $X^2$ cell by cell (no shortcut formula), and a learner who keeps the four expected counts to 2 decimal places lands outside the band in 180 of 200 draws; kept to 1 place, 193. The family's own solution prints the first expected count to 2 places and the gap to 3; the value those printed numbers give is outside the band in 65 of 200 draws (`shares.py`: 7.2053 against the key 7.2059). The pattern rule is "the tolerance accepts the value the part's own feedback prints".
    Fix: `prompt` ends "Give 2 decimal places."; `widget.tol` and both `wrong` `tol` `{ "abs": 0.05 }`; `accept` "${key:dp2}$, within 0.05"; solution "... gives $X^2 \\approx {key:dp2}$, on 1 degree of freedom." With that band no draw of 200 is refused for expected counts kept to 2 places, and no `wrong` entry comes within 0.4 of the answer (`try-fixes.py`).

17. `unclear` | `testing/fluency-l17-ratio-of-likelihoods.json` | family `poisson-ratio-test` | `widget.tol` and `prompt`.
    The same fault. The statistic is a small difference of two large terms ($\sum x_i$ runs to 350), so a logarithm kept to 4 places leaves the band of 0.0005 in 188 of 200 draws and one kept to 5 places in 90; a ratio $\hat\lambda/\lambda_0$ kept to 4 places in 117. The largest miss with 4 places is 0.03.
    Fix: `prompt` ends "Give 2 decimal places."; `widget.tol` and both `wrong` `tol` `{ "abs": 0.05 }`; `accept` "${key:dp2}$, within 0.05"; solution "$\\approx {key:dp2}$". No draw of 200 is then refused for a 4-place logarithm, and the nearest `wrong` entry is 0.10 away (`try-fixes.py`). The same family in `problems-4` (`p-night-admissions` part 2) takes a 4-place logarithm as it stands.

18. `unclear` | `testing/fluency-l15-sharpness-of-the-peak.json` | family `volatility-se` | a % sign.
    "$\sigma = 3\%$ a month. What is the standard error of $\hat\sigma$ ..., in percentage points?" A learner who types "0.4009%" is marked wrong in every draw, with no line: the grader reads the % as a hundredth. "0.4009 percentage points" will not submit.
    Fix: add to `wrong` `{ "id": "percent-sign", "value": "{sig/sqrt(2*n)/100}", "tol": { "abs": 5e-05 }, "line": "Type the number alone. The answer is already in percentage points, so a % sign divides it by 100." }`. Tried on 200 draws: the entry is clear of the answer and of both other entries in all of them.

19. `unclear` | `stat-learning/fluency-l16-groups-nobody-labelled.json` | family `assign-and-update` | a % sign.
    In 63 of 200 draws the values are volatilities "12, 13, 20, 30 and 34%". "28.00%" is then marked wrong with no line. In the daily-volume draws "21.00 million shares" will not submit; "25.60 bp" passes.
    Fix: add to `wrong` `{ "id": "percent-sign", "value": "{(KEY)/100}", "tol": { "abs": 0.005 }, "line": "Type the number alone, with no % sign after it." }`, where `KEY` is the family's `key` expression written out in full, as `try-fixes.py` builds it. Tried on 200 draws: clear of the answer and both other entries in all of them.

20. `minor` | `testing/fluency-l13-matching-moments.json` `exponential-rate`, `fluency-l15-sharpness-of-the-peak.json` `exponential-se` | a unit typed after the number.
    The prompts name the unit ("rate $\lambda$ per day", "$\hat\lambda = 2.5$ per second"). "0.132 per day" and "0.132 a day" will not submit, in every draw. Nothing is marked wrong.
    Fix: none in content; see Engine.

21. `minor` | `testing/fluency-l17-ratio-of-likelihoods.json` | family `wilks-df` | `prompt`.
    "The null hypothesis fixes {r} of them at given values, leaving {free} free. How many degrees of freedom ...?" The answer is the number the sentence has just printed, so the draw asks only which of two printed numbers to copy.
    Fix: `prompt` "A model for {what} has {p} parameters. Under the null hypothesis {free} of them stay free and the rest are fixed at given values. How many degrees of freedom has the $\\chi^2$ limit of $-2\\ln\\Lambda$?" The solution already reads "${p} - {free} = {r}$", and both `wrong` lines still fit.

22. `minor` | `stat-learning/fluency-l18-bending-the-line.json` | family `slope-in-a-region` | `prompt`.
    "A linear spline has slope 3 on $x$, knots at 4 and 19, and hinge coefficients ..." "Slope 3 on $x$" is not a phrase the lesson uses and can be read as the slope everywhere.
    Fix: "A linear spline has slope {b} left of its first knot, knots at {k1} and {k2}, and hinge coefficients ${d1}$ and ${d2}$. What is its slope {where}?" (drawn in `try-fixes.py`).

23. `minor` | `stat-learning/fluency-l16-groups-nobody-labelled.json` | family `linkage-distance` | `prompt`.
    "Give 3 decimal places" where the answer has at most 2 in 161 of 200 draws; and in the single and complete draws, two thirds of the family, the answer is the smaller or the larger of the two numbers printed.
    Fix: `prompt` ends "Give the exact value." A fuller fix, for the author: give the third share's distances to a group of three under average linkage, so every draw has a sum to do.

Notes, no change asked. `uniform-moment`: the moment estimate is below the largest draw in 14 of 200 draws (1, 2, 5 and 13 give 10.5); l13 teaches this as the method's flaw, and the `largest` line names the likelihood answer. `wilks-df`, `independence-df` and `coefficient-count` repeat a prompt within 20 draws (19, 17 and 17 distinct). `bernoulli-information` takes a thousands comma. `two-log-likelihoods` gives $n$, which is not needed. `decision-value` solutions print "$-8 +4$", which renders correctly.

## Engine

- A numeric field with no `%` unit reads a typed % as a hundredth and marks the entry wrong with the generic line, also where the prompt gives its values in per cent or percentage points. Three places: findings 11, 18, 19. Either ignore a trailing % when the part's `unit` is not `%` and the prompt or `placeholder` holds "%" or "percentage points", or say so in the help line.
- A number followed by unit words does not parse ("0.4 a day", "0.132 per day", "2.5 bp a year", "91 bp squared", "21 million shares", "7 h"): findings 5, 8, 20, 19. Already raised by the pattern review (its finding 9); this read adds "per" and "a" phrases and two placeholders that invite the words.
- `fresh-check.mjs --exam topic-1.6` reports no hit for `s-pareto-losses` against `estimation/homework-2` `hw2-pareto-tail`, also in the triage run (`--min-run 8 --min-share 0`, 20 hits, none of them this pair). The two share the desk, the £1m threshold, the density and the estimate (finding 3), but no run of eight words, and the tool does not read a `longform` item's `model`. It also cannot see a task repeated with new numbers (findings 9, 13). A shared-formula advisory across the exam's courses, as `--file` gives for a problem set, would have caught the density.
- Validator rule candidates from classes seen three times here: (a) a numeric part or family whose prompt asks for $k$ decimal places with a band of half a unit in that place, where the prompt holds `\ln` or "$X^2$" (findings 1, 16, 17): warn, since rounded intermediates leave the band; (b) a numeric part with no `unit` whose prose or prompt gives values with "%" (11, 18, 19): ask for a `percent-sign` entry; (c) a topic exam that loses the only item whose text names a lesson's key term (finding 4) is a `census` matter, not a validator one.

All four are appended to `docs/BACKLOG-INBOX.md` under "Raised later (review holes 1.6 and 2.1)", with the lesson-coverage check of finding 4 as a fifth bullet.

## Counts

| group | wrong | unclear | minor |
|---|---|---|---|
| A. exam items and skill tags (findings 1 to 6) | 2 | 0 | 4 |
| B. `testing/problems-4` (7 to 9; 8 also touches `stat-learning/problems-4`) | 0 | 0 | 3 |
| C. `stat-learning/problems-4` (10 to 15) | 1 | 1 | 4 |
| D. Fluency sets (16 to 23) | 0 | 4 | 4 |
| total (23 findings) | 3 | 5 | 15 |

Finding classes seen three times or more:

- A band at the asked rounding that a sensible working route leaves (logs or expected counts rounded on the way): findings 1, 16, 17.
- A % sign typed after a value the prompt gives in per cent, marked wrong with no line: 11, 18, 19.
- A unit typed after the number that the field will not read: 5, 8, 20 (and 19), the pattern review's finding 9 again.
- A story or task reused that `fresh-check` does not report: 3, 9, 13.
- A general statement without its hypothesis: 2, 7, 14, 15 (the class of `review-stat-learning-4.md`; here two are in `testing`).

## Fix pass

Fix agent, Sonnet. Targeted edits only, to the named files. No disputes: every corrected number was recomputed by two routes (see the number scripts) and agrees with the reader. 21 fixed, 2 deferred, 0 disputed. The three `wrong` findings are 1 (the Pearson line), 2 (the sufficiency rule) and 10 (the gradient step).

A. Exam items and skill tags

1. `s-pool-rates`: fixed. `question` asks for 5-place logarithms; `byKey.pearson` reads "6.00 is Pearson's $X^2$ ... With 5 places, $-2\ln\Lambda = 6.04$." Key 6.0406, band 0.005 and the `pearson` entry unchanged. Checked: logs to 5 places give 6.0408 and to 4 places 6.0420, both inside the band; logs to 3 places give 6.0 exactly, which is Pearson's value (2 x 15^2/75 = 6.0), outside the band.
2. `s-pareto-losses` option c: fixed, inside the item rewrite of finding 3: "The largest value is sufficient for a uniform on $(0, \theta)$, whose upper end is the parameter. Here the support, $0 < x < 1$, is fixed." Basis: the factorisation theorem. For $U(0, \theta)$ the joint density is $\theta^{-n}\mathbf 1\{\max x_i < \theta\}$, so the data meet $\theta$ through the maximum; for a fixed support they meet it through $\sum \ln x_i$ only (the item's first part).
3. `s-pareto-losses` freshness: fixed as proposed. Recovery rates on defaulted loans, density $\theta x^{\theta - 1}$ on $(0, 1)$, $n = 80$, $\sum\ln x_i = -32$. Keys kept (option a, 2.5, 0.078125). Part 2 `wrong`: `upside-down` 0.4, `exponent` 3.5 (was 1.5: it is now $\theta - 1 = 2.5$), new `sign` $-2.5$. Part 3 `wrong` id `alpha-not-squared` renamed `theta-not-squared`, value 0.03125 as before. Every text line, `accept` and `explain` rewritten from $\alpha$ to $\theta$; item id unchanged. Recomputed: $\hat\theta = -n/\sum\ln x_i$ by algebra and by numerical maximisation; $I(\theta) = 1/\theta^2$ by a numerical second derivative; the bound 6.25/80 by $I$, and the simulated variance of the MLE (Beta(2.5, 1) draws) is near it.
4. `topic-2.1` coverage: fixed for `stat-learning` l10, deferred for `ensembles` l7. `e-odds-update` is back (the author's original item, key 21.5%, band 0.0015, `unit` "%", difficulty 3) in the place of `e-report-which`. Recomputed: odds $0.1111 \times e^{0.9} = 0.2733$, probability 0.21462; and on the log-odds scale $\operatorname{logit}(0.1) + 0.9$ through the logistic function, 0.21462. Every skill is still examined (sl-setup by `e-gap-reading`, `e-code-ridge-inter`, `e-code-honest-report`; sl-tradeoff by `e-gap-reading`, `e-bias-var-table`, `e-explain-note`; sl-classify gains the item). Level 4 keeps `e-street-inside` (l15), `e-kmeans-spreads` (l16), `e-unit-gradient` (l17), `e-spline-slope` (l18). The ramp stays 6, 15, 6, 3 (30 items). `node tools/test-exam-minutes.mjs`: all passed. Deferred: the `ensembles` l7 gap (no out-of-bag item). Putting `e-oob-overlap` back means giving up `e-importance-claims` or `e-rf-variance`, a lesson-coverage choice, and the alternative is a line in `KNOWN_ISSUES.md`, a file outside this pass. For the main session to decide.
5. `e-spline-slope`, `e-kmeans-spreads`: fixed, `placeholder` "a number" on both.
6. `ht-pvalue` on `r-chi-23`: deferred. It is optional and the item is in `courses/testing/review-4.json`, not a file named for this pass.

B. `testing/problems-4.json`

7. `p-website-signups` part 1: fixed, both places: "The largest value is sufficient for a uniform on $(0, \theta)$. Poisson probabilities depend on the data through the total."
8. A unit typed after the number: fixed where content can: `p-one-unit` part 1 gets `"unit": "h"` (the field then reads "7 h"; checked in the engine grader). The multi-word units ("a day", "sign-ups", "a night") are an engine matter, already in the inbox: deferred.
9. `p-disk-failures` part 5: fixed, turned round as proposed: "How many gaps make its efficiency at least 0.99?" Key 200 (whole number, band 0), `wrong` `numerator` 198, `efficiency-now` 0.95. Recomputed: $(n - 2)/n \ge 0.99$ gives $n \ge 200$ by algebra and by a search over $n$; 198/200 = 0.99 exactly and 199 gaps fall short; a simulation at $n = 200$ gives an efficiency near 0.99; 38/40 = 0.95 at $n = 40$.

C. `stat-learning/problems-4.json`

10. `p-one-unit`: fixed with the fuller fix. I chose a step that lowers the loss, because level 4's chain and the lesson (l17) teach that a step against the slope lowers the loss; keeping 0.01 would turn the part into a lesson about overshoot that the lesson does not draw. $\eta = 0.002$: new $w_1 = 0.5 + 0.096 = 0.596$; prediction $2 \times (0.596 \times 8 - 1) + 1 = 8.536$; loss $\tfrac12 \times 1.464^2 = 1.0716$, down from 4.5 (also by forward evaluation in code; the old step gives 14.68 and 10.95, and the largest step that does not raise the loss is 0.0078). Part 4: answer 0.596 (3 decimal places), `uphill` 0.404, `no-rate` 48.5, `carried` 0.518. Part 5: answer 1.678, `old-knot` 2, `sign` $-1.678$, `carried` 1.931 ($1/0.518$); explanation "from 20 km to about 16.8 km". Part 4 `explain` now says the step takes the prediction from 7 to 8.536 hours and the loss from 4.5 to about 1.07.
11. `p-order-sizes` parts 1 and 2: fixed. New `wrong` `percent-sign` 0.18 and 0.22 (band 0), each with the line "That is the right centre. Type the number alone, with no % sign." Checked in the engine grader: "18%" now lands on `percent-sign` with a line.
12. `p-order-sizes` part 3: fixed. New `wrong` `not-settled` 226 with the line proposed; `carried` 91 kept. Recomputed: $1 + 1 + 144 + 0 + 16 + 64 = 226$ and $1 + 1 + 9 + 0 + 16 + 64 = 91$.
13. `p-spam-filter` part 4: fixed as proposed. Typed, "Refitted with a smaller $C$ ... what is the margin now? Give 3 decimal places." Key 0.667 (band 0.0005), `gave-norm` 1.5, `street-width` 1.333, `unchanged` 0.4. Recomputed: $\lVert w\rVert = \sqrt{0.81 + 1.44} = 1.5$; the refit is 0.6 times the old $(w, b)$, the same centre line; margin by geometry from a point on the new edge; growth factor 5/3. The set now has 17 of 19 parts typed.
14. `p-spam-filter` `prose` and family `margin`: fixed, both say the edges are $w \cdot x + b = \pm 1$.
15. `p-renewals` part 2 `explain`: fixed, "As a rule it varies less ...".

D. Fluency sets

16. `two-by-two`: fixed. 2 decimal places, band and both `wrong` bands 0.05, `accept` "${key:dp2}$, within 0.05", solution prints `{key:dp2}`. I added the sentence "Keep at least 2 decimal places in each expected count.": with that, none of 200 draws is refused for expected counts kept to 2 or 3 places or for the solution's own printed figures (a working at 1 place is outside the band in some draws and is not promised). No `wrong` entry is within twice the band of the answer.
17. `poisson-ratio-test`: fixed. 2 decimal places, bands 0.05, `accept` and solution at `dp2`, and "Keep at least 4 decimal places in any logarithm." None of 200 draws is refused for a log or a ratio kept to 4 or 5 places (3 places is refused in some draws, which is why the sentence is there). No `wrong` entry within twice the band.
18. `volatility-se`: fixed. `percent-sign` entry as proposed; on 200 draws it is clear of the answer and both other entries.
19. `assign-and-update`: fixed. `percent-sign` entry with the family's `key` written out in full; clear in 200 draws.
20. `exponential-rate`, `exponential-se` units: deferred, engine (already in the inbox).
21. `wilks-df`: fixed with the proposed prompt (the answer is no longer printed). `wrong` lines still fit. Checked on 200 draws: the prompt prints the free count and never "fixes".
22. `slope-in-a-region`: fixed, "has slope {b} left of its first knot".
23. `linkage-distance`: fixed, "Give the exact value." (the fuller fix is for the author).

Number scripts, all exit 0 with the scratchpad venv: `exam-1.6-holes-numbers.py` 99 of 99; `exam-2.1-holes-numbers.py` 82 of 82; `problems-testing-numbers.py` 307 checks, 0 failures; `problems-stat-learning-numbers.py` 331, 0; `fluency-testing-numbers.py` 12,174 (2,200 are the new band, % and prompt checks over 200 draws a family), 0; `fluency-stat-learning-numbers.py` 8,000 (800 new), 0.

Reader's scripts rerun. `mine.py`: the only differences are the changed items (`disk` 5, `orders` 1 to 3, `unit` 4 and 5, `pareto` 2 and 3: 14 lines, each the new key or the new `wrong` id of this pass), and it stops at `e-report-which`, which is out. `fluency-read.py` (a copy with the prompt patterns of the new `wilks-df` and `slope-in-a-region` prompts, run on 580 fresh draws): 5,474 checks, 0 failures, 3 notes (the uniform-moment note, not asked), against 65 notes before: the band notes of findings 16 and 17 are gone. `fluency-probe.mjs` (engine grader, every draw): 3,237 checks, 0 failures; the classes left are the multi-word units (engine) and a typed % now marked wrong with the `percent-sign` line. `grade-probe.mjs`: 541 checks; its 13 failures are rows holding the old keys of the changed parts (`p-disk-failures` 5, `p-one-unit` 4 and 5); "7 h" is read, "18%" and "22%" get their line, and the unit-word rows left are the engine matter.

Gates (from `app/`, local CDN): validator 0 errors, 4,857 warnings, none new on these files (the warnings on the two exams are on older items, as the reader noted); `test-exam-minutes.mjs` all passed (56 exams); `test-fluency.mjs --unit-only` 290 of 290, and each changed set 304 or 308 of the same with `--local-cdn`; playthrough `--exam topic-1.6`, `--exam topic-2.1`, `--problems testing/problems-4`, `--problems stat-learning/problems-4`, and `--fluency` for the six changed sets, all passed, with and without `--mobile`; voice scan 35: `exams` 0 and 0, `stat-learning` 0 and 0, `testing` 0 explanations and 1 sentence over 35 words, in `homework-3.json` (not in scope, as before).

Changed graded answers, tolerances, forms and exam items (for the main session):

- `topic-1.6` `s-pareto-losses`: story and notation changed (Pareto losses to recovery rates, $\alpha$ to $\theta$). Part 2 `wrong` `exponent` 1.5 to 3.5, new `sign` $-2.5$. Part 3 `wrong` id `alpha-not-squared` to `theta-not-squared`. Keys 2.5, 0.078125 and option a unchanged.
- `topic-1.6` `s-pool-rates`: question text and `pearson` line only; key, bands and `wrong` unchanged.
- `topic-2.1`: `e-report-which` (choice) out, `e-odds-update` (numeric, key 0.215 as a fraction, band 0.0015, `unit` "%", `wrong` 0.246 and 0.273) in, same position and difficulty; `e-spline-slope` and `e-kmeans-spreads` placeholders only.
- `stat-learning/problems-4` `p-one-unit`: part 1 `unit` "h"; part 4 $\eta$ 0.01 to 0.002, answer 0.98 to 0.596, `uphill` 0.02 to 0.404, `carried` 0.59 to 0.518; part 5 answer 1.02 to 1.678, `sign` $-1.02$ to $-1.678$, `carried` 1.695 to 1.931.
- `p-order-sizes`: new `wrong` `percent-sign` 0.18 (part 1) and 0.22 (part 2), `not-settled` 226 (part 3). Keys unchanged.
- `p-spam-filter` part 4: a choice replaced by a numeric part (key 0.667, band 0.0005, `wrong` 1.5, 1.333, 0.4).
- `testing/problems-4` `p-disk-failures` part 5: key 0.95 (band 0.0005) to 200 (whole number, band 0); `wrong` `inverted`, `n-minus-one`, `carried` replaced by 198 and 0.95.
- Fluency `two-by-two` and `poisson-ratio-test`: places 3 to 2, key band and `wrong` bands 0.0005 to 0.05, a "keep at least" sentence added; keys unchanged. `volatility-se` and `assign-and-update`: new `wrong` `percent-sign`. Prompt-only: `wilks-df`, `margin`, `slope-in-a-region`, `linkage-distance` (answers and `wrong` values unchanged).
