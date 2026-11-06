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

## Run length and share (follow-up to 588)

Each n-gram hit is now extended to the longest token run the two texts share (`run`, text capped at 30 tokens) and `share` is run over the target item token count. Gate with `--min-run n` (default 8) and `--min-share x` (default 0). Counts below are on the current tree, one hit per target item and source file; the 0.5 Jaccard rule added no hits.

| Setting | Hits | Items hit |
|---|---|---|
| run >= 8 | 1756 | 555 |
| run >= 10 | 841 | 337 |
| run >= 12 | 492 | 235 |
| run >= 15 | 291 | 158 |
| run >= 20 | 154 | 90 |
| share >= 0.3 | 653 | 259 |
| share >= 0.5 | 296 | 147 |

### Per exam (hits)

| Exam | run>=8 | >=10 | >=12 | >=15 | >=20 | share>=0.3 | share>=0.5 |
|---|---|---|---|---|---|---|---|
| mock-oa-sig-2 | 74 | 59 | 42 | 38 | 32 | 59 | 37 |
| mock-oa-sig-3 | 75 | 59 | 42 | 38 | 32 | 59 | 38 |
| mock-oa-sig | 75 | 59 | 42 | 38 | 32 | 59 | 38 |
| mock-oa-trader-2 | 98 | 55 | 37 | 28 | 12 | 69 | 32 |
| mock-oa-trader | 96 | 70 | 37 | 31 | 15 | 71 | 40 |
| mock-superday-trader | 50 | 39 | 37 | 9 | 1 | 10 | 1 |
| mock-oa-trader-3 | 91 | 55 | 35 | 29 | 13 | 60 | 32 |
| topic-1.10 | 56 | 34 | 22 | 6 | 2 | 2 | 0 |
| topic-1.4 | 141 | 43 | 19 | 10 | 3 | 26 | 3 |
| topic-3.3 | 41 | 26 | 17 | 5 | 0 | 3 | 2 |
| topic-3.4 | 43 | 17 | 13 | 5 | 1 | 2 | 0 |
| topic-1.7 | 61 | 29 | 12 | 7 | 0 | 2 | 0 |
| topic-2.5 | 29 | 16 | 12 | 1 | 0 | 1 | 0 |
| mock-trade-sample | 11 | 11 | 11 | 2 | 1 | 1 | 0 |
| topic-1.11 | 54 | 18 | 11 | 3 | 1 | 3 | 2 |
| topic-0.6 | 21 | 13 | 10 | 5 | 1 | 2 | 1 |
| topic-1.6 | 38 | 17 | 10 | 4 | 0 | 3 | 0 |
| stage-0 | 74 | 31 | 9 | 6 | 1 | 39 | 32 |
| topic-1.3 | 95 | 23 | 9 | 4 | 0 | 14 | 1 |
| topic-1.5 | 53 | 13 | 9 | 4 | 0 | 14 | 4 |
| mock-sample-parts | 9 | 6 | 6 | 3 | 3 | 7 | 6 |
| stage-1 | 107 | 35 | 6 | 1 | 0 | 67 | 5 |
| topic-1.2 | 20 | 10 | 6 | 4 | 2 | 8 | 2 |
| topic-2.6 | 18 | 9 | 6 | 1 | 0 | 4 | 0 |
| topic-3.2 | 29 | 7 | 5 | 3 | 0 | 4 | 0 |
| topic-0.1 | 12 | 4 | 4 | 0 | 0 | 8 | 6 |
| topic-0.3 | 26 | 7 | 4 | 1 | 1 | 19 | 10 |
| mock-superday-research | 8 | 5 | 3 | 0 | 0 | 1 | 0 |
| topic-2.2 | 37 | 5 | 3 | 0 | 0 | 1 | 0 |
| mock-oa-quant-data | 15 | 6 | 2 | 2 | 0 | 4 | 0 |
| topic-2.3 | 22 | 8 | 2 | 1 | 0 | 0 | 0 |
| topic-3.5 | 37 | 4 | 2 | 1 | 0 | 3 | 0 |
| mock-interleave-sample | 5 | 2 | 1 | 0 | 0 | 0 | 0 |
| mock-sample | 1 | 1 | 1 | 0 | 0 | 1 | 0 |
| topic-0.7 | 32 | 17 | 1 | 0 | 0 | 0 | 0 |
| topic-1.8 | 7 | 3 | 1 | 1 | 1 | 1 | 0 |
| topic-1.9 | 7 | 3 | 1 | 0 | 0 | 0 | 0 |
| topic-2.4 | 5 | 1 | 1 | 0 | 0 | 1 | 0 |
| topic-3.1 | 19 | 5 | 1 | 0 | 0 | 2 | 0 |
| mock-sample-data | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| topic-0.2 | 17 | 9 | 0 | 0 | 0 | 14 | 4 |
| topic-0.4 | 11 | 1 | 0 | 0 | 0 | 5 | 0 |
| topic-1.1 | 15 | 2 | 0 | 0 | 0 | 3 | 0 |
| topic-2.1 | 20 | 3 | 0 | 0 | 0 | 0 | 0 |

### Known cases

| Case | run | share | Caught at |
|---|---|---|---|
| 0.6 item [6] vs proof l3 screens[5] | 13 | 0.30 | run >= 12 (not 15); share >= 0.3 |
| 1.10 item [12] vs analysis l20 screens[3] | 10 | 0.14 | run >= 10 only; no share setting |
| 1.10 item [13] vs analysis homework-5 h-two-limits | none | none | no setting |

Item [13] only changes the integrand: it shares fewer than 8 consecutive tokens with homework-5 and its shingles score near 0, so no run, share or Jaccard setting catches it without flooding the list. A word-level tool cannot see an integrand-only change; that needs the second reader.

### Recommended default gate

Gate on `--min-run 12`: 492 hits on 235 items today, still a lot, but it keeps the verbatim copy (0.6 [6]) and drops stock stems. Use `--min-run 10` (841 hits on 337 items) to catch [12]-style cases too; the extra hits are mostly stems and need a read. `--min-share 0.3` (653 hits) adds nothing on the known cases and is better as a sort key. The tool default stays 8 for the scan; authors pass 12 for a hard gate.
