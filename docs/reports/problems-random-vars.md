# Problem sets: random-vars (brief `docs/briefs/chained.md`)

Files: `app/content/courses/random-vars/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-random-vars-numbers.py` (exits 0, 639 checks).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-spinner-product | 4 (4 / 0) | l1, l2, l3, l4 | 3 |
| problems-1 | p-bond-defaults | 5 (4 / 1) | l1, l2, l3, l4 | 4 |
| problems-1 | p-straddle-days | 4 (4 / 0) | l2, l3, l4 | 4 |
| problems-1 | p-tightest-quote | 4 (4 / 0) | l1, l2, l3 | 5 |
| problems-2 | p-phone-cover | 4 (4 / 0) | l5, l6, l7 | 3 |
| problems-2 | p-reversal-days | 5 (4 / 1) | l5, l6, l7, l8 | 4 |
| problems-2 | p-month-options | 4 (4 / 0) | l5, l6, l7 | 4 |
| problems-2 | p-token-draw | 5 (5 / 0) | l5, l6, l7, l8 | 5 |
| problems-3 | p-quote-trades | 4 (4 / 0) | l9, l10 | 3 |
| problems-3 | p-fund-hedge | 5 (5 / 0) | l9, l10, l11, l12 | 4 |
| problems-3 | p-two-funds | 5 (4 / 1) | l9, l10, l12 | 4 |
| problems-3 | p-clustered-fills | 4 (4 / 0) | l9, l10, l11 | 5 |

Typed parts: level 1 16 of 17, level 2 17 of 18, level 3 17 of 18. Every lesson of each level appears in at least one problem, and every problem draws on at least two. Choice parts are judgements only (the VaR after selling a bond, whether dependence moves a mean, which holding has the best mean per sd).

Chains. Level 1 teaches no expectation, so its chains run outcome count, pmf, CDF, transform, then a tail chance or decision: a product of two spins to the payoff $\max(M - 6, 0)$; four bonds to a 95% VaR that sits just past $F_L(25) = 0.9477$, then the VaR after selling a bond; a straddle $|X|$ to a two-day total; the tightest of three quotes to the number of dealers that makes a one-tick quote 90% likely. Level 2 runs distribution, mean, fair price, decision: phone cover with an excess that applies only to claims; reversals counted by dependent indicators, then a break-even gain; a call and put tied by $C - Q = S - 40$; tokens drawn without replacement to a fair price with a bonus. Level 3 runs distribution, mean, variance, then a decision that uses them: trades needed for the sd to fall to 10% of the mean; a joint table to a hedge that leaves $\operatorname{Var}(A)(1 - \rho^2)$; a minimum-variance mix and its mean per sd; clustered fills that cap a book at 5 orders where independence would allow 11. Each later part restates the value it uses, and its `wrong` list holds the value that follows from the commonest slip in the part before.

The script caught two of my slips while drafting (the shrinking-chance sum 1.4369, not 1.4417, and the 20-day P&L slip $-12.96$); both are fixed in the files.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (639 checks in all) |
| validator | 0 errors, 0 warnings on the file | same | same |
| playthrough `--local-cdn` | green (17 parts) | green (18 parts) | green (18 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

## Fresh-check

At the gate, `node tools/fresh-check.mjs --file content/courses/random-vars/problems-<n>.json` gives 0 hits for all three sets. At triage settings (`--min-run 8 --min-share 0`): problems-1 has two hits, "outcomes let # be the product of the two numbers" against `measure-prob/review-1` items[2] (share 0.16) and "give a decimal using # from part # what is" against `conditional/problems-2` (share 0.07); problems-2 has one, "independently from day to day over # trading days" against `exams/topic-1.5` e-winning-days (a binomial count, share 0.05); problems-3 has one, "has mean # and variance # and is independent of" against `arma/l7` (share 0.07). All stock phrasing: the setups (spinner products, bond VaR, reversals, phone cover, token bonus, hedge table, clustered fills) are new to the course.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems random-vars)". None blocked a problem.

## Level 4: `problems-4.json` (two variables at once)

Lessons read first: l13 joint tables, l14 independent variables, l15 given information, l16 averaging averages. Settings new to the course: a courier's vans and late parcels, two independent bus routes seen only through their total, an insurer's young and older drivers, a script that retries a download.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-courier-vans | 5 (4 / 1) | l13, l14, l15, l16 | 3 |
| problems-4 | p-late-buses | 5 (4 / 1) | l13, l14, l15 | 4 |
| problems-4 | p-young-drivers | 5 (5 / 0) | l13, l15, l16 | 4 |
| problems-4 | p-file-retry | 5 (5 / 0, one `expression`) | l15, l16 | 5 |

Typed parts 18 of 20; the two choice parts are judgements (are the vans and parcels independent; does the total move route 2's chances). Chains: margin, conditional row, independence test, conditional mean, refund bill by total expectation; product cells, $P(S = 2)$, $E[X \mid S = 2]$, then $E[Y \mid S = 2] = 2 - 1.6087$ by linearity; a reversed conditional, the young mean, the book mean, the loss on a young policy and the older drivers' cross-subsidy (£120, checked both as $0.2 \times 480 / 0.8$ and as $620 - 500$); first-step analysis $m = 2 + \dots$, $m = 4.2$, $E[T \mid \text{fail}] = 7.4$, a backup for retries (3.4929 s) and the backup speed a 3-second target needs (1.8 s). Each later part restates the value it uses, and its `wrong` list holds the value the commonest slip in the part before gives (`carried`).

Form. Every non-whole numeric part says "Give your answer to n decimal places.", "Give a fraction, or a decimal to 4 places." or "to the nearest penny", so the new `[answer-form]` rule is silent on the file (the house sentence "Give a decimal to 4 places" does not satisfy it; see the inbox). Where a part tells the learner to use a rounded value the key is what that value gives (0.3913 from $2 - 1.6087$; 3.4929 from $m_B = 2.7857$, exact 3.492857).

Numbers. The script now loads `problems-4` and checks each part twice: exact fractions, then a second route (100 equally likely tickets drawn from each table, a 100 by 10 grid of the two routes, the column totals for the book mean, Wald's $E[N]E[\text{try}] = 2 \times 2.1$ and a series over the failures for $m$, a series over the backup's errors for $m_B$), sympy for the `expression` key, accept list and slips, and `form_checks` on every numeric part. 1,038 checks in all sets, 0 failures.

| check | problems-4 |
|---|---|
| numbers script | exit 0 (1,038 checks over sets 1 to 4) |
| validator | 0 errors, 0 warnings on the file |
| playthrough `--local-cdn` | green (20 parts) |
| playthrough `--mobile` | green; 440 px shots read (all 20 parts), no layout fault |
| voice scan 35 (course folder) | 0 and 0 |

Fresh-check: 0 hits at the gate. At `--min-run 8 --min-share 0` five hits, all the form sentence "give a fraction or a decimal to # places" (share 0.05), shared with other problem sets. Stock phrasing.
