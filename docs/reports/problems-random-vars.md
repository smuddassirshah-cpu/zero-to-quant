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
