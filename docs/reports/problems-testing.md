# Problem sets: testing (brief `docs/briefs/chained.md`)

Files: `app/content/courses/testing/problems-4.json`. Numbers: `docs/reports/problems-testing-numbers.py` (exits 0, 309 checks). Levels 1 to 3 have no set yet.

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
