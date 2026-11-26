# Delta audit 2026-11-26, batch 4: conditional, limits-thm, markov, random-vars (problem sets)

Blind delta audit at `b2fa22b4` of the content changed since each course closed (bases: conditional `ba403924`, limits-thm `5ad2c837`, markov `a4f8fb2a`, random-vars `d71e3bdf`). Scope is the ten problem-set files in `delta-batch4.tsv`; every added or changed string and value is a ledger row, read in the context of its whole problem. Two problems are new in full (`conditional/problems-3` `p-two-papers`, `conditional/problems-4` `p-dark-fills`) and were read whole. Ledger: `docs/reports/audit-delta-2026-11-26-4-ledger.md`. Script: `docs/reports/audit-delta-2026-11-26-4-concepts.py`.

Not in scope, noted only: `conditional/l3-shrinking.json` also changed since `ba403924` (61 lines) and is not in this batch's list.

## Counts per course

| course | files | rows | correct | wrong | imprecise | misleading | serious | minor |
|---|---|---|---|---|---|---|---|---|
| conditional | problems-2, -3, -4, -5 | 53 | 52 | 0 | 1 | 0 | 0 | 1 |
| limits-thm | problems-2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| markov | problems-1, -3 | 9 | 8 | 1 | 0 | 0 | 0 | 1 |
| random-vars | problems-2, -3, -5 | 9 | 8 | 0 | 1 | 0 | 0 | 1 |
| total | 10 | 75 | 72 | 1 | 2 | 0 | 0 | 3 |

No row is `unverified`. No graded key, tolerance or slip value is wrong; all three findings are feedback or explanation wording.

## Findings

1. `app/content/courses/markov/problems-1.json` | carry-trade problem (prose "A carry trade makes £3m in a calm month"), part 4 `feedback.byKey.sign` | **wrong, minor** | The line says "A positive 4.7 drops the minus sign of the stressed-month loss." That named mistake does not give the slip's value. | Dropping the minus on the stressed-month loss gives $0.3 \times 3 + 0.7 \times 8 = 0.9 + 5.6 = 6.5$. The slip 4.7 is the key $-4.7$ with the sign of the whole sum dropped. The first sentence of the line (0.9, −5.6, sum below zero) is right. | Replace the line with: "0.3 × 3 is 0.9 and 0.7 × (−8) is −5.6, so the sum is −4.7. A positive 4.7 drops the minus sign of the total: the month loses money on average."

2. `app/content/courses/conditional/problems-4.json` | `p-dark-fills` part 5 `explain.text`, first sentence | **imprecise, minor** | "A fill drawn at random is 3 times as likely to come from a large order, one per fill." Read as written it contradicts part 1. | A drawn fill comes from a large order with chance $\tfrac23$ against $\tfrac13$, so it is 2 times as likely to come from a large order. The 3 is the likelihood ratio per order: one given large order is 3 times as likely as one given small order to supply the drawn fill. The keyed option and the feedback use "favours 3 to 1" and "likelihood ratio", which are right. | Replace the first sentence with: "A large order is 3 times as likely as a small one to supply the drawn fill, one chance per fill." The other two sentences stand.

3. `app/content/courses/random-vars/problems-5.json` | `p-startup-rounds` part 1 `feedback.byKey.sign` | **imprecise, minor** | "A positive 0.0527 takes 0.5108 − 0.4055, the wrong way round." The subtraction named gives 0.1053, twice the slip. | $0.5108 - 0.4055 = 0.1053$; the slip is half of it, $\tfrac12 \times 0.1053 = 0.0527$. The first sentence is right. | Replace the second sentence with: "A positive 0.0527 is half of 0.5108 − 0.4055, the wrong way round."

## Checked and found correct (the points most likely to hide an error)

- `p-two-papers`: both within-group joint tables are valid (cells 0.17, 0.03, 0.38, 0.42 and 0.07, 0.13, 0.48, 0.32); the pooled product $0.2 \times 0.55 = 0.11$ holds exactly; the explain's "weighted 0.4 and 0.6, the two shifts offset exactly" is right because the maths pass rate is the same in both groups, so the weights among maths passers equal the group shares. Every slip gives its named mistake's value, including the carried `unweighted` 0.21 in part 3. Monte Carlo, 4,000,000 applicants: pooled P(coding given maths) 0.550.
- `p-dark-fills`: size-biased sampling gives $\tfrac23$; the dark news on a drawn fill has likelihood ratio 1; a yes has ratio $0.488 / 0.2 = 2.44$; the `double` slip 0.8299 is odds $2 \times 2.44$. The prose now says "thousands of client orders", which makes the ratio of realised counts match the ratio of expectations. Monte Carlo, 2,000,000 orders: 0.667, 0.667, 0.619.
- limits-thm: $\Phi(0.2) = 0.5793$ and the `no-centre` slip is $\Phi(0.06/0.3)$; the reworded median argument (monotone map of $Z$) is the correct one.
- markov/problems-3: the three `sign` slips and lines are right, and £551.49 is the exact expected wealth ($P_3 = 0.551490$).
- random-vars/problems-3: the three `decimal` slips are the keys divided by $10^4$, and their 2% bands touch no key or other slip.

## Overlap with earlier reads

Read after the ledger and findings were written: `docs/reviews/review-delta-af-1.md` (with its fix pass), `review-reuse-af-hits-reauthor-conditional.md`, `review-pass9-hits.md`. Their findings on this content (the many-orders assumption in `p-dark-fills`, the re-authoring of `p-two-papers`, the `no-centre` slip) are already applied in the text audited here and none remains open.

| | count |
|---|---|
| conceptual findings by this audit only | 3 (1 wrong, 2 imprecise) |
| by an earlier read only, still open | 0 |
| by both | 0 |

New `wrong` no earlier read found: 1 (markov, minor); 0 in conditional, limits-thm and random-vars.

## Runs

- Validator: 0 errors.
- `run-number-scripts --only`: conditional 4 of 4, limits-thm 5 of 5, markov 5 of 5, random-vars 3 of 3 passed.
- `grade-all --file` on each of the ten files: 0 failures each.
- `audit-delta-2026-11-26-4-concepts.py` (venv Python, NumPy and SciPy newer than CI's pins; no figure depends on the version): 53 checks, exit 0. The three findings are prose and are printed as notes, not asserted.
- No playthrough (auditor rule 7). No code widgets in the changed content. No engine limits met, so no inbox bullet.
