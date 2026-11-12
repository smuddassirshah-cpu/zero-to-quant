# Problem sets: testing (brief `docs/briefs/chained.md`)

Files: `app/content/courses/testing/problems-1.json` to `problems-4.json`. Numbers: `docs/reports/problems-testing-numbers.py` (exits 0, 1,019 checks over the four sets; the level 4 part is unchanged).

## Levels 1 to 3 (`problems-1.json`, `problems-2.json`, `problems-3.json`)

Lessons read first: l1 to l12, with the quizzes, reviews 1 to 3 and homework 1 to 3 (settings listed to stay clear of them). Settings new to the course: cereal boxes, phone batteries, a wine taster, pizza deliveries; fertiliser trials, tyre brands, running shoes, a blood screen; a gene screen, fund managers under BH, checkout pages, a field of biomarkers.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-cereal-boxes | 5 (3 / 2) | l1, l2, l3 | 3 |
| problems-1 | p-phone-battery | 5 (4 / 1) | l1, l3, l4 | 5 |
| problems-1 | p-wine-taster | 4 (4 / 0) | l1, l3 | 4 |
| problems-1 | p-pizza-delivery | 4 (3 / 1) | l2, l3, l4 | 4 |
| problems-2 | p-fertiliser-trials | 5 (4 / 1) | l5, l6 | 4 |
| problems-2 | p-tyre-brands | 4 (3 / 1) | l7, l8 | 3 |
| problems-2 | p-running-shoes | 5 (4 / 1) | l6, l8 | 5 |
| problems-2 | p-blood-screen | 5 (4 / 1) | l5, l7 | 4 |
| problems-3 | p-gene-screen | 5 (4 / 1) | l9, l10 | 5 |
| problems-3 | p-fund-managers | 3 (3 / 0) | l10, l11 | 3 |
| problems-3 | p-checkout-designs | 5 (4 / 1) | l9, l10 | 3 |
| problems-3 | p-biomarker-field | 5 (3 / 2) | l9, l10, l12 | 4 |

Typed parts: 14 of 18, 15 of 19, 14 of 18 (after the fix pass below). Each choice part is a judgement: which hypotheses, which test and cut-off, which plan, what a p-value or a flag means, which next step is honest, what Bonferroni and BH promise. Every lesson of each level appears, and every problem draws on two or more.

Chains. Every non-final part's result is used by a later part, restated in that part's question. Examples: the standard error 3 g, $z = -2.3$, p = 0.0107 against $\alpha = 0.01$; $\bar x = 18$, $s = 2$, $t = -2.121$, the cut-off 1.895, then the smallest advert rejected, 19.34 hours; the tails 13, 79 and 299 of 4096 to the smallest rejecting count, 10; the centre 2.25, power 0.7274, the either-rule 0.9257 against one 72-plot trial at 0.9379; $\alpha = 0.0359$, $\beta = 0.3446$, 483 flags, a share of 0.27; the Bonferroni 0.00125, its family chance 0.0488, then 2 against BH's 5 (rank 4 fails, rank 5 passes); 17.29 and 1.026 false finds, shares 0.490 and 0.079. Each `carried` entry is the answer from the commonest slip of the part before, where the learner could reach it with the values given; where that slip needs a $\Phi$ value the part does not give, no `carried` entry is written (it could not fire).

Form and bands. Every non-whole numeric part names its form ("Give n decimal places.", "Give a decimal.", "Give the nearest whole number.", "Round up to a whole runner."). Where a part gives a rounded $\Phi$, the key is what that value gives, and the band also takes the unrounded route where they differ (tyres part 3 band 0.0001 takes 0.0117 and 0.0118; the screen's 483 from rounded and unrounded rates; the shares at 2 places). The $t$ of the phones keeps a band of 0.001 so a 3-place standard error (0.707) still lands. A rounding tie (8.645 at 2 places) has its `wrong` band set to take both neighbours. All answers that are chances are fractions, so a typed "1.07%" reads as 0.0107 and is right; no key is in per cent units, so no `percent-sign` entry is needed. Single-letter units typed after the number are read through the widget's `unit` (`g` for the cereal standard error, `s` for the shoe differences); multi-letter units (hours, minutes, mm) are dropped by the field.

Checks. Numbers script 0 failures, two routes a part (exact fractions or sympy against SciPy, statsmodels `multipletests`, `ttest_1samp`, `ttest_rel`, `ttest_ind_from_stats`, enumeration of all 4096 sequences, seeded simulation of null families, brute search over $n$); each `wrong` value matched to its slip, outside the key's band and clear of the others. Validator 0 errors and 0 warnings on the three files (first drafts had key-length, long-sentence and explain-answer advisories, all rewritten). Playthrough `--local-cdn` green for each set (18, 19, 17 parts), and with `--mobile` green; the 440 px shots of every part were read, no layout fault. Voice scan 35 on the course folder: 0 explanations over three sentences; the one long sentence is the old one in `homework-3.json`.

Fresh-check (`--file`, then `--min-run 8 --min-share 0` for triage): 0 hits on each set. Advisories are shared constants only: the levels 0.05 and 0.01, the cut-offs 1.645 and 1.96, $1 - 0.95^2 = 0.0975$ (given, not asked, in the fertiliser plan), 6.18 from the power formula, $P(|Z| > 2) = 0.0455$ from l12, one p-value (0.004) shared with `homework-2` `h-abstract` in another story, and stock phrasing ("what is the chance of at least one false"). A first draft of `problems-3` item 4 was the `homework-3` `h-vendor` setting with new numbers (best of 200 signals, the Bonferroni bar and the rule of thumb); it was replaced by the biomarker field before commit.

Notes for the reader. `p-fertiliser-trials` part 5 states the either rule's $\alpha$ from independence, an idea l9 names later. `p-gene-screen` part 5 asks what Bonferroni and BH promise, the l10 idea of FWER against FDR, but about two lists side by side rather than one. The running-shoes sample size uses the level's normal formula $n = 6.18(\sigma/\delta)^2$ with the sd of a difference.


## Level 4: `problems-4.json` (estimation theory and likelihood tests)

Lessons read first: l13 matching moments, l14 sufficiency and Rao-Blackwell, l15 Fisher information, l16 the Cramér-Rao bound, l17 likelihood ratios and Wilks, l18 chi-squared tests. Settings new to the course: gaps between disk failures in a data centre, a website's hourly sign-ups, a bakery's loaves by kind of day, a hospital ward's night admissions.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-disk-failures | 5 (5 / 0) | l13, l15, l16 | 3 |
| problems-4 | p-website-signups | 5 (4 / 1) | l14, l15, l16 | 4 |
| problems-4 | p-bakery-loaves | 5 (4 / 1) | l17, l18 | 4 |
| problems-4 | p-night-admissions | 5 (5 / 0) | l13, l15, l17 | 5 |

Typed parts 18 of 20. The two choice parts are judgements: which statistic is sufficient, and the conclusion at 5% with the Wilks count of degrees of freedom. Every lesson of the level appears in at least one problem, and every problem draws on at least two.

Chains. Moment estimate $\hat\lambda = 0.4$, the information 250 in 40 gaps, the standard error 0.0632, the bound $\tfrac{1}{250}$, and the efficiency 0.95 of the unbiased $\tfrac{n - 1}{\sum x_i}$. The sufficient total, the Rao-Blackwell estimate $\tfrac{54}{12} = 4.5$, its variance 0.375, the efficiency $\tfrac{1}{12}$ of the first hour alone, and the 50 hours a standard error of 0.3 needs. An expected count 28, $X^2 = \tfrac{50}{7} \approx 7.143$, 2 degrees of freedom, p = 0.0281 from $e^{-x/2}$, then $G = 7.242$ against the same $\chi^2_2$. The MLE 3.8, $-2\ln\Lambda = 1.966$, the standard error 0.6164 from $I = \tfrac{1}{\lambda}$, $z = 1.298$, and the 20 nights the likelihood-ratio statistic needs to pass 3.841. Each later part restates the value it uses, and its `wrong` list holds the value that follows from the commonest slip in the part before (`carried`).

Form. Every non-whole numeric part says "Give a decimal." or "Give n decimal places.", so `[answer-form]` is silent. Keys are stored rounded to the places asked, with a band of half a unit; where a part tells the learner to use a rounded value (0.6164 in part 4 of the admissions, 7.143 in part 4 of the loaves) the key is what that value gives, and the script checks the unrounded value gives the same figure.

The script caught one of my slips while drafting: the carried slip in part 5 of the disk failures is 15.01 from the printed 0.0632, not 15.02 from the unrounded standard error.

## Checks

| check | problems-4 |
|---|---|
| numbers script | 0 failures (309 checks; two routes a part: sympy against SciPy's `chi2_contingency`, a numeric score root, integration or summation of the score's variance, seeded simulation, brute search over $n$) |
| validator | 0 errors, 0 warnings on the file (three `O2-long-sentence` advisories on first draft, rewritten) |
| playthrough `--local-cdn` | green (20 parts) |
| playthrough `--mobile` | green; 440 px shots of every part read, no fault |
| voice scan 35 (course folder) | 0 and 0 on the file (the folder's one long sentence is in `homework-3.json`) |

## Fresh-check

`node tools/fresh-check.mjs --file content/courses/testing/problems-4.json`: 0 hits, 6 advisory shared formulas. Each is a formula the level teaches and the part restates so a slip does not sink the chain: $I(\lambda) = \tfrac{1}{\lambda^2}$ and $\tfrac{1}{\lambda}$ (l15 quiz), the l16 estimator $\tfrac{n - 1}{\sum x_i}$ with variance $\tfrac{\lambda^2}{n - 2}$, $G = 2\sum O\ln\tfrac{O}{E}$ (l18 screen 3) and the Poisson $-2\ln\Lambda$ (l17 screen 4). No setup, story or number is reused: the l16 screen uses $n = 10$ and $\lambda = 2$; the l17 screen 50 minutes, 120 trades and $\lambda_0 = 2$.

## Engine limits

One bullet in `docs/BACKLOG-INBOX.md` under "Raised later (fluency and problems testing 4)". None blocked a problem.

## Fix pass (review-problems-1.6-b, problems-1 to 3)

`p-gene-screen`, `p-checkout-designs` and `p-biomarker-field` were re-authored with a new task structure and new numbers, because each reworked a lesson or exam task (finding 9). Genes: 60 tests at 10%, the Bonferroni bar, its count, BH past a failing rank, then the smallest $q$ that keeps rank 5 (new step). Checkout pages: 18 pages, expected launches and their cost at £4,000 a launch, the Bonferroni bar and the chance of any useless launch under it. Biomarkers: a table of four bars, the per-null chance that keeps expected false finds at 1, the lowest bar that meets it, the real finds and false share there, and why a false share is not a chance of any false find. The other minor findings are small edits listed in `docs/reviews/review-problems-1.6-b.md`. Numbers script: 1,120 checks, 0 failures, a stale-value check on each re-authored item. Fresh-check: 0 hits and no advisory on `problems-3`.
