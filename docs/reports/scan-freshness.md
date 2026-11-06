# Scan: exam freshness (ENGINE-BACKLOG 588)

Tool: `node tools/fresh-check.mjs --all-exams` on the current tree. Hits are one per target item and source file. Nothing was fixed. The 8-gram rule produces all hits; no pair reached the 0.5 shingle score. Mock variants (mock-oa-sig, -sig-2, -sig-3, mock-oa-trader, -trader-2, -trader-3) share items with each other by design, so read those rows as expected.

Total: 1756 hits on 555 items in 44 exam files.

## Hits per exam

| Exam | Hits | Items hit |
|---|---|---|
| topic-1.4 | 141 | 24 |
| stage-1 | 107 | 26 |
| mock-oa-trader-2 | 98 | 28 |
| mock-oa-trader | 96 | 27 |
| topic-1.3 | 95 | 24 |
| mock-oa-trader-3 | 91 | 27 |
| mock-oa-sig-3 | 75 | 17 |
| mock-oa-sig | 75 | 17 |
| mock-oa-sig-2 | 74 | 17 |
| stage-0 | 74 | 25 |
| topic-1.7 | 61 | 20 |
| topic-1.10 | 56 | 18 |
| topic-1.11 | 54 | 12 |
| topic-1.5 | 53 | 15 |
| mock-superday-trader | 50 | 12 |
| topic-3.4 | 43 | 19 |
| topic-3.3 | 41 | 14 |
| topic-1.6 | 38 | 18 |
| topic-2.2 | 37 | 10 |
| topic-3.5 | 37 | 5 |
| topic-0.7 | 32 | 13 |
| topic-2.5 | 29 | 12 |
| topic-3.2 | 29 | 14 |
| topic-0.3 | 26 | 13 |
| topic-2.3 | 22 | 12 |
| topic-0.6 | 21 | 12 |
| topic-1.2 | 20 | 10 |
| topic-2.1 | 20 | 7 |
| topic-3.1 | 19 | 13 |
| topic-2.6 | 18 | 12 |
| topic-0.2 | 17 | 8 |
| mock-oa-quant-data | 15 | 6 |
| topic-1.1 | 15 | 10 |
| topic-0.1 | 12 | 5 |
| mock-trade-sample | 11 | 1 |
| topic-0.4 | 11 | 6 |
| mock-sample-parts | 9 | 3 |
| mock-superday-research | 8 | 5 |
| topic-1.8 | 7 | 4 |
| topic-1.9 | 7 | 5 |
| mock-interleave-sample | 5 | 3 |
| topic-2.4 | 5 | 4 |
| mock-sample-data | 1 | 1 |
| mock-sample | 1 | 1 |

## Top hits outside the mock-to-mock pairs (by 5-shingle score)

| Target | Source | Score | Shared 8-gram |
|---|---|---|---|
| mock-sample-parts.json:items[0] | py-found/homework-sample-parts-late.json:items[3] | 1 | xs # three follow ups on the list |
| mock-sample-parts.json:items[0] | py-found/homework-sample-parts.json:items[0] | 1 | xs # three follow ups on the list |
| topic-0.6.json:items[4] | proof/review-1.json:items[5] | 0.63 | consider exists x in mathbb z # x |
| topic-3.3.json:items[2] | bank/brainteasers-1.json:items[2] | 0.63 | # what is the smaller angle between the |
| mock-sample-parts.json:items[0] | py-found/review-sample-parts.json:items[1] | 0.62 | xs # three follow ups on the list |
| topic-1.5.json:items[12] | random-vars/l10-scaling-and-adding.json:quiz[2] | 0.58 | x and y are independent with operatorname var |
| stage-0.json:parts[1].items[7] | trig/review-2.json:items[6] | 0.57 | the unit circle what is cos tfrac # |
| mock-oa-trader-2.json:parts[1].items[1] | conditional/l14-independent-trials.json:quiz[0] | 0.5 | a fair coin is tossed # times what |
| mock-oa-trader-3.json:parts[1].items[1] | conditional/l14-independent-trials.json:quiz[0] | 0.5 | a fair coin is tossed # times what |
| mock-oa-trader.json:parts[1].items[1] | conditional/l14-independent-trials.json:quiz[0] | 0.5 | a fair coin is tossed # times what |
| topic-1.3.json:items[4] | limits/review-3.json:items[2] | 0.5 | x # what is f x simplify the |
| topic-1.4.json:items[7] | eigen/homework-1.json:items[2] | 0.46 | mathbf a begin pmatrix # end pmatrix write |
| stage-0.json:parts[1].items[9] | trig/l11-every-angle.json:quiz[2] | 0.44 | x # for # circ le x le |
| mock-oa-sig-2.json:parts[0].items[3] | puzzles/l4-indicator-tricks.json:quiz[0] | 0.41 | place where two heads stand side by side |
| mock-oa-sig-3.json:parts[0].items[3] | puzzles/l4-indicator-tricks.json:quiz[0] | 0.41 | place where two heads stand side by side |
| mock-oa-sig.json:parts[0].items[3] | puzzles/l4-indicator-tricks.json:quiz[0] | 0.41 | place where two heads stand side by side |
| topic-0.2.json:items[2] | functions/homework-2.json:items[1] | 0.4 | a line passes through # and # what |
| topic-0.2.json:items[2] | functions/l6-how-steep.json:quiz[0] | 0.4 | a line passes through # and # what |
| topic-0.2.json:items[2] | functions/review-2.json:items[1] | 0.4 | a line passes through # and # what |
| stage-1.json:parts[3].items[11] | vector-calc/l6-green.json:quiz[3] | 0.38 | what is oint c x # y dx |
| stage-0.json:parts[1].items[9] | trig/review-3.json:items[5] | 0.36 | x # for # circ le x le |
| topic-1.2.json:items[9] | sql/l10-matching-rows.json:screens[1] | 0.36 | select t id s name from trades as |
| topic-1.2.json:items[9] | sql/l11-no-match.json:quiz[0] | 0.36 | select t id s name from trades as |
| mock-oa-sig-2.json:parts[0].items[14] | exams/topic-1.5.json:items[23] | 0.33 | game lasts you start with # and bet |
| mock-oa-sig-3.json:parts[0].items[14] | exams/topic-1.5.json:items[23] | 0.33 | game lasts you start with # and bet |

## Reading the list

Most hits are a lesson sentence reused in an exam item (a stem such as "what is the smallest n that works for"), not a copied setup. Review the ones with a score of 0.15 or more first. Calibration: the pre-fix 0.6 item [6] hits `proof/l3-if-then` screens[5]; the pre-fix 1.10 item [12] hits `analysis/l20` screens[3]; the pre-fix 1.10 item [13] (integrand changed only, setup shared with `analysis/homework-5` h-two-limits) is not caught, because it shares fewer than eight tokens.
