# Delta read: fix passes of the syllabus holes 0.1 and 0.2, and 1.6 and 2.1

Scope: every entry of the two "changed graded answers" lists, read as the files stand at commit 4cc694b.

- Fix pass 0.1 and 0.2 (9cabc98): `number-sense/problems-4`, `quadratics/problems-4`, `exams/topic-0.1`, `exams/topic-0.2`, seven Fluency families. Record: `review-holes-0.1-0.2.md`, "Fix pass".
- Fix pass 1.6 and 2.1 (8e62748): `testing/problems-4`, `stat-learning/problems-4`, `exams/topic-1.6`, `exams/topic-2.1`, eight Fluency families. Record: `review-holes-1.6-2.1.md`, "Fix pass".

Method. Each listed item was read whole. `recompute.py` recomputes every changed answer, band and `wrong` value by two routes of my own (whole-number search and prime forms, sympy, fractions, a forward pass of the network with a central-difference slope, k-means stepped to its fixed point, the gamma moments of the disk estimator, a grid search and numerical integrals for the recovery density) and searches each re-authored item for numbers of its old version. `grade.mjs` runs the engine's own graders (`numGrade`, and `exprGrade` with the local Compute Engine) on every answer, `accept` form and `wrong` entry of the changed parts and on some 340 typed strings: other right forms, the answer one step short, the value the feedback prints, a typed % or unit. `fluency.py` reads 200 engine draws of each of the 14 changed families (`draw.sh`), checks each key by my own formula, then measures the two widened bands against the workings their prompts promise and against wrong methods; `poisson-ratio-test` is also run over all 2,530 parameter sets it can draw, and `two-by-two` over 30,000 tables of my own. `fluency-grade.mjs` puts the draws through the engine's graders. `fresh.py`, `find.py` and `context.py` search the content for each re-authored item's words, numbers and formulae; I read what they pointed at. `proposed.py` computes the numbers of every fix proposed below, twice.

Scripts: `docs/reviews/review-delta-holes-scripts/`, run from the repo root: `recompute.py`, `proposed.py`, `fluency.py <draws>` (scratchpad venv Python); `grade.mjs --local-cdn <pkgs> [--show]`; `fluency-grade.mjs <draws> --local-cdn <pkgs>`; `draw.sh <out> [seed] [n]`; `fresh.py`; `find.py '<glob>' '<regex>'`; `context.py <file> '<regex>'`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = a statement reads two ways; `minor` = otherwise.

## Tool results

- `recompute.py`: 332 checks, 0 failures; 1 FINDING row left failing (finding 1).
- `grade.mjs`: 572 checks, 0 failures; 17 FINDING rows (findings 4, 6 and 8). Every answer and `accept` form grades correct; every `wrong` entry lands on its own id and has a line.
- `fluency.py`: 6,809 checks, 0 failures, 1 note (finding 10). `fluency-grade.mjs`: 4,989 checks, 0 failures. `proposed.py`: 10 of 10.
- Authors' scripts, scratchpad venv, all exit 0: `exam-0.1-holes` 101 of 101; `exam-0.2-holes` 57 of 57; `exam-1.6-holes` 99 of 99; `exam-2.1-holes` 82 of 82; `problems-number-sense` 286, 0 failures; `problems-quadratics` 874, 0; `problems-testing` 307, 0; `problems-stat-learning` 331, 0; `fluency-number-sense` 55,829 of 55,829; `fluency-quadratics` 57,931 of 57,931; `fluency-testing` 12,174, 0; `fluency-stat-learning` 8,000, 0. All twelve passed with finding 1 in the file: no script reads the `generic` line.
- `node tools/validate.mjs`: 0 errors, 4,857 warnings; none on a changed item (the seven on the four exams are on older items). `manifest.json` unchanged.
- `fresh-check.mjs`: 0 hits on the four sets and the four exams; advisories as the fix passes report. It does not see findings 4 and 5.
- `voice-scan.py 35`: 0 and 0 on `exams`, `number-sense`, `quadratics`, `stat-learning`; `testing` 1 sentence, in `homework-3.json`, out of scope.
- No browser run, as asked.

## Findings

1. `wrong` | `courses/number-sense/problems-4.json` | `p-hall-tiles` `parts[1].feedback.generic`.
   "Not quite. Count the factors of 108 from its primes." 108 is the HCF of the old hall (finding 7 of the first read replaced it by 120). The question two lines above says "divides 120". A learner with any unlisted wrong count is sent to the wrong number.
   Fix: "Not quite. Count the factors of 120 from its primes."

2. `wrong` | `courses/testing/fluency-l18-counts-against-expectations.json` | family `two-by-two` | band 0.05 at 2 places.
   The promise holds: with expected counts kept to 2 places the worst error is 0.0171 in 200 draws and 0.0223 in 30,000 tables; with every term rounded to 2 places as well, 0.0280. The solution's printed figures are never refused. Counts kept to 1 place are refused in 65 of 200 draws, which the prompt does not promise.
   The band is no longer tight enough for two wrong methods. Dividing each squared gap by the observed count is marked right in 72 of 200 draws (33.8% of tables; 0.7% under the old band 0.0005). The statistic $G = 2\sum O\ln\tfrac{O}{E}$, which the same lesson teaches (l18 `screens[3]`), is marked right in 119 of 200 (59.9%; 3.7% before). A tighter band does not cure it: at 0.03, the tightest the promise allows, the shares are 27.0% and 50.9%. The other nine methods tried, and both `wrong` entries, are refused in every draw.
   Fix: keep the band and draw only tables where the two slips are clear of it, each with its own line (0.11 = both bands and the rounding). Add to `let`:
   `"obs": "(a*d - b*c)^2/(a + b + c + d)^2*(1/a + 1/b + 1/c + 1/d)"`,
   `"g": "2*(a*ln(a*(a + b + c + d)/((a + b)*(a + c))) + b*ln(b*(a + b + c + d)/((a + b)*(b + d))) + c*ln(c*(a + b + c + d)/((c + d)*(a + c))) + d*ln(d*(a + b + c + d)/((c + d)*(b + d))))"`;
   to `where`: `"abs(key - obs) > 0.11"`, `"abs(key - g) > 0.11"`; to `wrong`:
   `{"id": "over-observed", "value": "{obs}", "tol": {"abs": 0.05}, "line": "You divided each squared gap by the observed count. Divide by the expected count."}`,
   `{"id": "likelihood-ratio", "value": "{g}", "tol": {"abs": 0.05}, "line": "That is $G$, the likelihood-ratio statistic. Pearson's $X^2$ divides each squared gap by its expected count."}`.
   The first clause keeps 55.0% of tables, both together 25.6% (`fluency.py`); run `test-fluency.mjs` on the set after the change. Check for the table 62, 68, 16, 56: $X^2 = 12.68$, `obs` 15.49 (`proposed.py`).

3. `minor` | `courses/testing/fluency-l17-ratio-of-likelihoods.json` | family `poisson-ratio-test` | band 0.05 at 2 places.
   The promise holds over every set the family can draw: a logarithm kept to 4 places is never refused (worst error 0.0379 of 2,530 sets, inside the bound $2 \times 350 \times 0.00005 + 0.005 = 0.04$). 3 places is refused in half the sets, as the fix pass says.
   Two things the fix pass did not see. (a) The score statistic $\tfrac{(\sum x_i - n\lambda_0)^2}{n\lambda_0}$ is marked right in 64 of 200 draws and 839 of 2,530 sets (33%); the Wald form in 563 (22%). The prompt prints the formula wanted, so this is less likely than finding 2. (b) A learner who rounds the ratio to 4 places and then its logarithm to 4 places is refused in 4 of 2,530 sets (worst error 0.0615); a truncated logarithm in 27.
   Fix: (a) add to `where` `"abs(key - dv^2/(n*lam0)) > 0.11"`, which keeps 1,299 of 2,530 sets and clears the Wald form in every one. (b) end the prompt "Keep the ratio as a fraction and at least 4 decimal places in any logarithm."

4. `minor` | `exams/topic-2.1.json` | `e-odds-update` | freshness against `courses/stat-learning/homework-3.json` `h-odds3`; and the grader.
   The restored item is homework 3 with two numbers changed. Homework: "A default model has coefficient 0.40 on leverage. A loan has default probability 0.10. Its leverage rises by 3 turns". Exam: coefficient 0.45 on leverage, default probability 10%, two more turns. Same model, same feature, same starting probability, same odds 0.111 in both `accept` lines. `fresh-check --exam` reports nothing. This is the class of finding 3 of the first read (`s-pareto-losses`), which was rewritten.
   The grader: "0.215" and "0.2146" in the % field are read as 0.215% and get the generic line (`grade.mjs`).
   Fix, same idea and difficulty, new story (no file of `stat-learning` or the exam has a fill model, $e^{-1.2}$ or "ticks away"; `proposed.py`):
   - `prose` "A logistic model for whether a resting order fills has a coefficient of $-0.6$ on its distance from the best price, in log-odds per tick. An order 1 tick away fills with probability 40%. Nothing else changes."
   - `question` "What is the fill probability 3 ticks away? Give a percentage to one decimal place."
   - `widget`: `answer` 0.167, `tol` 0.0015, `unit` "%", `label` "Fill probability", `accept` "16.7%: odds $0.667 \\times e^{-1.2} = 0.201$"; `wrong` `prob-times` 0.120 (band 0.002), `odds-as-prob` 0.201 (0.002), `sign` 0.689 (0.002), `decimal` 0.00167 (0.00002).
   - `feedback.correct` "The odds fall from 0.667 to 0.201, a probability of 16.7%." `generic` "The coefficient acts on the log-odds, so two more ticks multiply the odds by $e^{-1.2}$." `byKey.prob-times` "You multiplied the probability by $e^{-1.2}$. The coefficient multiplies the odds, not the probability." `odds-as-prob` "You stopped at the odds, 0.201. Convert them: probability is odds over one plus odds." `sign` "You multiplied the odds by $e^{1.2}$. The coefficient is negative, so the odds fall." `decimal` "That is the probability as a fraction of 1. Type it as a percentage: 16.7."
   - `explain` "At 1 tick the odds are $0.40/0.60 = 0.667$. Two more ticks multiply them by $e^{-0.6 \\times 2} = 0.301$, which gives 0.201. The probability is $0.201/1.201 = 16.7\\%$."
   Exact value 0.16722; the rounded figures give 0.1672, inside the band.

5. `minor` | `exams/topic-0.2.json` | `e-diameter-ends` | freshness against `courses/quadratics/l18-circles-on-a-grid.json` `screens[3]`.
   The fix pass moved the item off the 6-8-10 triangle of `p-park-pond` and onto 5-12-13. That is the lesson's own distance question: "How far is $(-2, 1)$ from $(3, 13)$?", answer 13, `wrong` `no-root` 169, feedback "$\sqrt{5^2 + 12^2} = \sqrt{169} = 13$". The exam's radius step is that line, digit for digit. The points and the task (an equation) differ, so the item still tests something.
   Fix, the 8-15-17 triangle, which no file of `quadratics` or the exam holds (`find.py`; `proposed.py`):
   - `prose` "The points $A(-7, -9)$ and $B(9, 21)$ are the two ends of a diameter of a circle. Its centre is $C(1, 6)$."
   - `answer` `(x-1)^2+(y-6)^2=289`; `accept` `["x^2+y^2-2x-12y-252=0"]`; `wrong` `signs` `(x+1)^2+(y+6)^2=289`, `radius-not-squared` `(x-1)^2+(y-6)^2=17`, `full-diameter` `(x-1)^2+(y-6)^2=1156`.
   - `feedback.correct` "The radius is the distance from $C$ to $A$: $\\sqrt{8^2 + 15^2} = 17$. So the equation is $(x - 1)^2 + (y - 6)^2 = 289$." `byKey.radius-not-squared` "The right side is $r^2$. With $r = 17$ that is 289." `full-diameter` "You used the whole distance between the ends, 34, as the radius. The radius runs from the centre to the edge, so it is half of that."
   - `explain` "From $C(1, 6)$ to $A(-7, -9)$ is 8 across and 15 down, so $r = \\sqrt{8^2 + 15^2} = \\sqrt{289} = 17$. The ends are $\\sqrt{16^2 + 30^2} = 34$ apart, which is $2r$. The circle is $(x - 1)^2 + (y - 6)^2 = 17^2$."
   The grader as it stands is sound: 15 right forms pass (sides swapped, $13^2$, multiplied out in four ways, both sides doubled, spaces, `\left`); the equation with no right side, $= r^2$, $= 26$, a wrong centre and a bare 13 or 169 are refused; each slip lands on its line. Only the square-root form $\sqrt{(x-1)^2+(y-6)^2} = 13$ is refused, which is fair.

6. `unclear` | `courses/testing/problems-4.json` | `p-disk-failures` `parts[4].question`.
   "How many gaps make its efficiency at least 0.99?" Every $n \ge 200$ does. The key is the smallest, which the question does not ask for, and its own "at least" invites a bound: "≥200", ">=200", "n ≥ 200" and "at least 200" are not read, so the field will not submit (`grade.mjs`, 5 rows). "200", "200 gaps" and "n = 200" pass; 198 and 0.95 land on their lines.
   Fix: "... against the bound $\\tfrac{\\lambda^2}{n}$ of part 4. What is the smallest number of gaps that makes its efficiency at least 0.99? Give a whole number."
   The numbers are right: the estimator is unbiased with variance $\tfrac{\lambda^2}{n - 2}$ (gamma moments, and by integration at $n = 5$); $\tfrac{n-2}{n} \ge 0.99$ first holds at 200; $\tfrac{198}{200} = 0.99$ exactly.

7. `minor` | `courses/number-sense/problems-4.json` | `p-lawn-pond` `parts[2]`.
   $134.37 \div 15 = 8.96$, so rounding to the nearest whole number gives 9 as well. The part is about rounding up and cannot tell it from plain rounding; `rounded-down` 8 needs a learner to truncate 8.96. (The old item had 3.99, the same weakness.)
   Fix (optional): tins of 12 m². "Sealant comes in tins that each cover 12 m². ..." Answer 12 ($134.37 \div 12 \approx 11.20$; 11 tins cover 132 m², 12 cover 144 m²). `rounded-down` 11, `whole-courtyard` 13 ($154 \div 12 = 12.83$). Drop `circumference-carried`: $138.29 \div 12 = 11.52$ also gives 12. `correct` "$134.37 \\div 12 \\approx 11.20$, so 11 tins are too few. 12 tins cover $12 \\times 12 = 144$ m²."

8. `minor` | units in the question's own words | `number-sense/problems-4` `p-cycle-commute` parts 4 and 5; `quadratics/problems-4` `p-windy-ride` part 3; `exams/topic-0.1` `e-pit-area`, `e-plan-hall`.
   The `unit` fields work: "120 cm", "21.6 m²", "45 m", "20 km/h", "5.56 m/s", "89.375 m³", "7 h", "199 m²" all pass. But each of these questions names its unit in words, and the words are not read: "20 km an hour", "8 km an hour", "5.56 metres a second", "199 square metres", "234 square metres" stop the field (`grade.mjs`, with "m^2", "m2", "m^3", "cubic metres": 11 rows). Same engine class the fix pass deferred (finding 9 there), now with the question's own wording as the trigger. No content fix; it strengthens the inbox row. No new engine class was found, so nothing was added to the inbox.

9. `minor` | `courses/quadratics/problems-4.json` | `p-windy-ride` `parts[3]`.
   The new part is sound: only an expression equal to $9v$ passes ("9v", "9*v", "v9", "(9v)", "9 v"); 144 and 9 land on their lines; the whole fraction in five spellings lands on `whole`. Two small points. (a) `whole` also takes the question typed back ($\tfrac{9}{v-2} \div \tfrac{16}{v}$) and the flipped product not yet multiplied, and tells both "That is the whole fraction, and it is right". (b) "72", the top with $v = 8$ from part 3 put in, gets the generic line.
   Fix (optional): `byKey.whole` "That is the whole ratio. Type only the top of the single fraction over $16(v - 2)$." New `wrong` `{"id": "number", "tex": "72"}` with "You put $v = 8$ in. Keep the letter here; part 5 puts the number in."
   Chain: part 4 restates both times, part 5 restates the ratio and uses it; holds.

10. `minor` | `courses/testing/fluency-l17-ratio-of-likelihoods.json` | family `wilks-df` `prompt`.
    38 of 200 draws read "Under the null hypothesis 1 of them stay free". The answer is no longer printed, as the fix pass says.
    Fix: "A model for {what} has {p} parameters. The null hypothesis leaves {free} free and fixes the rest at given values. How many degrees of freedom has the $\\chi^2$ limit of $-2\\ln\\Lambda$?"

## The parts named in the brief

- `p-windy-ride` part 4 (key $9v$): right; finding 9. Part 1 `whole` lands for the bottom as $v(v-2)$ or $v^2 - 2v$ and for the top uncollected.
- `e-diameter-ends`: right ($A$ and $B$ are on the circle, $C$ is their midpoint, $r^2 = 169$, the `accept` form is the key multiplied out); finding 5 on freshness.
- `p-one-unit` parts 4 and 5 ($\eta = 0.002$): right. By a forward pass, $w_1 = 0.596$ gives a prediction of 8.536 and a loss of 1.0716, down from 4.5. The slope $-48$ agrees by the chain rule and a central difference. The old step 0.01 gave a loss of 10.95; the largest step that does not raise the loss is $\tfrac{6}{768} = 0.0078$. `uphill` 0.404, `no-rate` 48.5, `carried` 0.518 ($-9$ is part 3's `slope-for-v`); knot $\tfrac{1}{0.596} = 1.678$, `old-knot` 2, `sign` $-1.678$, `carried` $\tfrac{1}{0.518} = 1.931$; 20 km to 16.8 km. No 0.98, 1.02, 1.695 or 0.59 is left. Notes: part 3's `sign` slip carried (0.404) lands on `uphill`, whose line still fits; `dropped-x` and part 3's own `carried` give 0.512 and 0.532, generic. In part 5, "16.78" (km, not tens of km) gets the generic line.
- `p-disk-failures` part 5: right; finding 6.
- `p-spam-filter` part 4: right. $\lVert w \rVert = 1.5$, margin $\tfrac{2}{3}$; the refit is 0.6 times the old $(w, b)$, so the centre line is the same; $0.4 \times \tfrac{5}{3}$ agrees. 0.667, 0.6667, 0.6666 and 2/3 pass; 0.67 and 0.666 are refused; 1.5, 1.333 and 0.4 land on their lines. 17 of 19 parts are typed. Note: its result is not used by part 5, as before the pass.
- `s-pareto-losses`: right. The density integrates to 1; $\hat\theta = 2.5$ by calculus and a grid search; $I = \tfrac{1}{\theta^2}$ by the second derivative and the squared score at three values of $\theta$; bound 0.078125; the mean of $\ln x$ at 2.5 is $-0.4$, the data given. Option c's line is true. No $\alpha$, Pareto, £ or 1.5 is left. Fresh: no other file of `testing`, `estimation`, `regression` or the stage exam holds the density or "recover".
- `two-by-two` and `poisson-ratio-test`: the solution's rounding lands inside the band in every draw; the band lets wrong methods through. Findings 2 and 3.

## Original findings: closed or not

Closed as the fix passes say (each checked in the file and by script): 0.1 and 0.2 findings 1 to 4, 6 to 16, 18 to 21; 1.6 and 2.1 findings 1 to 3, 5, 7, 9 to 19, 21 to 23. Finding 7 of 0.1 and 0.2 left the stale 108 (finding 1 here). Finding 5 (skill names) was proposed only; the main session has since made it (cd55747): `ns-powers` and `quad-graph` read alike in both course files and both exams.

Still open, deferred by the passes:
- Engine: units with a caret or in words (0.1 and 0.2 finding 9; finding 8 here). Multi-word units "a day", "sign-ups" (1.6 and 2.1 findings 8 and 20).
- Engine: the uneven verdict of `form: "simplified"` (0.1 and 0.2 finding 17). Measured on 40 draws a family: a top with its common factor out is refused when the bracket's coefficient is above 1 (15 of 15) and passes when it is 1, such as $3(x - 4)$ (15 of 15). The prompts now say "with no brackets", so the second case contradicts the prompt.
- `ht-pvalue` on `testing/review-4` `r-chi-23` (1.6 and 2.1 finding 6): still there; optional.
- `ensembles` l7 has no exam item (1.6 and 2.1 finding 4): below.
- `linkage-distance`: the fuller fix "is for the author" (finding 23).

## Ruling asked for: `ensembles` l7 and `e-oob-overlap`

Accept the gap and record it in `KNOWN_ISSUES.md`. Do not put `e-oob-overlap` back.

- It is not fresh. It is l7 `screens[8]` with the numbers changed: a forest on the sign of the next 10 days' return, an out-of-bag score (0.767 there, 0.71 here) against a walk-forward score near a half (0.495, 0.52), and the same key, that neighbouring days share the label.
- What it tests is examined already: overlapping labels and the purge in `e-code-purged-roll` and `e-boost-recipe`. Out-of-bag scoring itself is practised in three items of `homework-2`.
- `e-importance-claims` cannot give way: it is the exam's only `en-interpret` item and its only item on l8.
- `e-rf-variance` adds least of the two and is the one that would give way: `en-bagging` would keep two items and `en-trees` keeps `e-gini-node` and `e-code-gbm-stop`. But it is the only item on why a forest works (l5 and l6), and it is typed. The swap would trade an l7 gap for an l5 and l6 gap, and a number for a choice.
- If l7 must be examined, write a new typed item (for instance the expected number of trees that leave a given row out) and let it replace `e-rf-variance`.

## Verified clean

- `p-hall-tiles` numbers: HCF 120, 16 sides, 15 tiles, 21.6 m², and all nine `wrong` values. `p-lawn-pond`: 19.63 (3.14 and 22/7 inside the band), 134.37, 9, and all seven `wrong` values; no word of its story is elsewhere in the course. `p-meshing-gears` part 4: 45 m.
- `e-pit-area` `rounded-radius` 201 (3.14 and 22/7 too), `e-feed-updates` `six-fifty` 369,000, `e-five-counts` has one solution.
- `p-order-sizes`: 18, 22, 40, 226, 91 by stepping k-means; "18%" and "22 %" land on `percent-sign`.
- `s-pool-rates`: 6.0406; logarithms to 5 and 4 places inside the band, 3 and 2 places give 6.00, which is Pearson's value.
- `volatility-se`, `assign-and-update`: `percent-sign` is the key over 100 and clear of every other band in 200 draws; a typed % lands on it. `conjugate-bottom` 55 pairs, all 1 or more. `other-number`: the given number is never the HCF. `count-factors`: `no-plus-one` only when an index is above 1. `table-mean`, `quotient`, `add-tops`, `subtract-tops`, `slope-in-a-region`, `linkage-distance`: prompts as stated.
- `topic-2.1`: 30 items, ramp 6, 15, 6, 3.

## Counts

10 findings: 2 `wrong` (1, 2), 1 `unclear` (6), 7 `minor`. No changed key, band or `wrong` value is wrong.

## Fix pass

Findings 1 to 7, 9 and 10 applied; 8 deferred (engine). `e-oob-overlap` not restored, as ruled. Each number recomputed by a second route in the author scripts named below (sympy and Fractions against floats and brute force); the reader's `proposed.py` agrees (10 of 10).

1. Fixed. `number-sense/problems-4.json` `p-hall-tiles` part 2 `feedback.generic`: "factors of 108" now "factors of 120". `problems-number-sense-numbers.py` now fails if 108 appears anywhere in the item, and asserts the generic line names 120 (the stale-number check that would have caught it).
2. Fixed. `testing/fluency-l18-counts-against-expectations.json` `two-by-two`: `let` gains `obs` and `g`; `where` gains `abs(key - obs) > 0.11`, `abs(key - g) > 0.11` and a third clause `abs(g - obs) > 0.11` (found by the reader's grade run: in 3 of 200 draws the `likelihood-ratio` value lay within 0.05 of `over-observed`, so G was given the wrong line); `wrong` gains `over-observed` and `likelihood-ratio`. Band 0.05 unchanged. Disputed in part: with the proposed clauses the validator rejects 82% of draws (limit 80%), so the draw ranges of `a`, `b`, `c`, `d` are widened from 15..70 to 10..70 and the `key <= 20` clause to `key <= 25` (26.8% of tables kept, my own simulation). Table 62, 68, 16, 56 gives $X^2$ = 12.68 and `obs` 15.49. Proof in `fluency-testing-numbers.py` over 200 draws: the right working (exact, expected counts to 2 and 3 places, the printed figures) is accepted in every draw; `over-observed`, `likelihood-ratio`, `no-divide` and `one-cell` are refused in every draw; both slips are more than 0.11 from the key and from each other.
3. Fixed. `fluency-l17-ratio-of-likelihoods.json` `poisson-ratio-test`: `where` gains `abs(key - dv^2/(n*lam0)) > 0.11`; prompt now ends "Keep the ratio as a fraction and at least 4 decimal places in any logarithm."; extra `wrong` `score-form` (let `score`) so a learner who types the score statistic gets its own line. Proof in the script over 200 draws: right working (exact, logarithm to 4 and 5 places) accepted every draw; score, Wald ($dv^2/s$), `not-doubled` and `no-mean-term` refused every draw. The script's ratio-rounded-to-4-places check is dropped, since the prompt no longer promises it.
4. Fixed as proposed. `exams/topic-2.1.json` `e-odds-update` is the resting-order fill item: key 0.167 (band 0.0015, %), `wrong` `prob-times` 0.120, `odds-as-prob` 0.201, `sign` 0.689 (each 0.002), new `decimal` 0.00167; new prose, question, accept, feedback (correct, generic, four `byKey`) and explain. Two departures: `decimal` band 0.0005 not 0.00002 (the validator's wrong-band warning), and the prose split into three short sentences (O2-long-sentence warning); both leave no new validator warning. Exact value 0.16722, by odds times $e^{-1.2}$ and by the logistic of the log-odds. `exam-2.1-holes-numbers.py` also fails if any figure or word of the leverage version remains.
5. Fixed as proposed. `exams/topic-0.2.json` `e-diameter-ends`: $A(-7, -9)$, $B(9, 21)$, centre $C(1, 6)$; key `(x-1)^2+(y-6)^2=289`; `accept` `x^2+y^2-2x-12y-252=0`; `wrong` `signs` `(x+1)^2+(y+6)^2=289`, `radius-not-squared` `...=17`, `full-diameter` `...=1156`; feedback correct, two `byKey` lines and explain rewritten (8, 15, 17, 34, 16, 30). Radius 17 two ways (distance to $A$, half of $AB$ = 34); lattice-point check of the accept form. `exam-0.2-holes-numbers.py` fails if 169, 676, 13, 26, -132 remain.
6. Fixed. `testing/problems-4.json` `p-disk-failures` part 5: "What is the smallest number of gaps that makes its efficiency at least 0.99?" The proposed "Give a whole number" is left out because the validator then reads 0 decimal places and warns on the 0.95 slip band; the field's placeholder already says "whole number". 200 is the smallest $n$ with $(n-2)/n \ge 0.99$ by algebra and by search; the script asserts both and the wording.
7. Fixed. `number-sense/problems-4.json` `p-lawn-pond` part 3: tins of 12 m². Key 12 ($134.37 \div 12 = 11.20$; 11 tins cover 132, 12 cover 144); `rounded-down` 11; `whole-courtyard` 13 ($154 \div 12 = 12.83$); `circumference-carried` removed ($138.29 \div 12 = 11.52$ also gives 12). Question, accept, correct, generic, two `byKey` and explain updated. Rounding to the nearest gives 11, so the part now separates rounding up from rounding.
8. Deferred (engine: units in words or with a caret; already in the inbox). No content change.
9. Fixed. `quadratics/problems-4.json` `p-windy-ride` part 4: `byKey.whole` "That is the whole ratio. Type only the top of the single fraction over $16(v - 2)$."; new `wrong` `number` (tex 72 = $9 \times 8$, part 3's speed) with its line.
10. Fixed. `fluency-l17-ratio-of-likelihoods.json` `wilks-df` prompt as proposed ("The null hypothesis leaves {free} free and fixes the rest at given values."); the script's prompt check updated to it and to the absence of "stay free".

Graded answers, bands, `where` clauses and items changed (complete list):
- `p-lawn-pond` part 3: answer 9 to 12; `rounded-down` 8 to 11; `whole-courtyard` 11 to 13; `circumference-carried` (10) removed.
- `p-windy-ride` part 4: new `wrong` `number` (72); `byKey.whole` text.
- `p-disk-failures` part 5: question wording only; answer 200 unchanged.
- `p-hall-tiles` part 2: `generic` text only.
- `e-odds-update`: whole item (answer 0.215 to 0.167; wrong 0.246 and 0.273 to 0.120 and 0.201; new `sign` 0.689 and `decimal` 0.00167).
- `e-diameter-ends`: answer 169 to 289 form; `accept` -132 to -252; the three `wrong` values.
- `two-by-two`: `let` `obs`, `g`; `where` three clauses added and `key <= 20` to `key <= 25`; vars `a` to `d` from 15..70 to 10..70; `wrong` `over-observed`, `likelihood-ratio`.
- `poisson-ratio-test`: `let` `score`; `where` one clause; `wrong` `score-form`; prompt tail.
- `wilks-df`: prompt only.

Gates (worktree, scratchpad venv Python, `--local-cdn` scratchpad `pkgs`):
- Author scripts all exit 0: `exam-0.1-holes` 101, `exam-0.2-holes` 60, `exam-1.6-holes` 99, `exam-2.1-holes` 93, `problems-number-sense` 285, `problems-quadratics` 882, `problems-testing` 309, `problems-stat-learning` 331, `fluency-number-sense` 55,829, `fluency-quadratics` 57,931, `fluency-testing` 12,774 (including 4,840 extra checks: the 200-draw proofs), `fluency-stat-learning` 8,000.
- Reader's scripts: `recompute.py` finding row now passes (0 findings left; its 10 failures are its own old keys for the items changed above); `proposed.py` 10 of 10; `fluency-grade.mjs` 5,589 checks, 0 failures (3 failures before the third `where` clause); `fluency.py` reports no failure other than its stale expectations (key at most 20, old poisson prompt wording); `grade.mjs` rows for finding 6 no longer fail; its remaining failures use the old typed strings of the re-authored items and the FINDING rows are finding 8.
- `node tools/validate.mjs`: 0 errors, 4,857 warnings (as before; none on the changed items). `manifest.json` not committed.
- `test-fluency.mjs` on both changed sets 308 of 308; `test-exam-minutes.mjs` all 56 pass.
- Playthrough green, with and without `--mobile`: `--exam topic-0.2`, `--exam topic-2.1`, `--problems number-sense/problems-4`, `quadratics/problems-4`, `testing/problems-4`, `--fluency testing/fluency-l17-ratio-of-likelihoods` and `fluency-l18-counts-against-expectations`.
- Voice scan 35: 0 and 0 on `number-sense`, `quadratics` and `exams`; `testing` 1 sentence in `homework-3.json`, out of scope.
