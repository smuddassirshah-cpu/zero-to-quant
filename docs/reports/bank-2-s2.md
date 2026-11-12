# Bank part 2, session 2: partial hand-in

Brief: `docs/briefs/bank-2.md`. Written: `app/content/bank/statistics-2.json` (15), `finance-2.json` (15), `behavioural-6.json` (8), 38 items. Not written: `coding-2.json` (12), which waits for engine requirement B2-E1. Number script: `docs/reports/bank-2-s2-numbers.py` (standard library only, plain `python3`). House style copied from `docs/reports/bank-2-s1.md`. Written after session 3 (`docs/reports/bank-2-s3.md`) by the same author.

## Acceptance (section 7)

| Step | Result |
| --- | --- |
| 1. Validator | `0 errors, 4664 warnings`, the baseline; 0 warnings name the three files (no `[tight-band]`, `[wide-wrong-band]`, `[wrong-band]`, `[answer-form]`, `[key-length]`, `[shown-arithmetic]`; `[O2-long-sentence]` silent). |
| 2. Numbers | `python3 docs/reports/bank-2-s2-numbers.py`: `749 checks, 0 failed`, exit 0. A planted wrong slip fails it. |
| 3. Playthrough | `--bank statistics-2 --bank finance-2 --bank behavioural-6 --local-cdn <pkgs>`: `bank total: 38 of 38 items passed in 3 files`, `All passed.` With `--mobile`: 38 of 38, `All passed.` (B2-E3 still open, so `--mobile` adds no phone pass for `--bank`.) `--routes-only` with and without `--mobile`: `All passed.`, `#bank 187 drawable of 314 in 29 files (127 locked)`. |
| 4. Freshness | `fresh-check.mjs --bank <file>`: 0 hits, exit 0, each file; `--min-run 10`: 0 each. `--min-run 10 --min-share 0`: 5 hits, all rewritten (below); now 0 on all three. |
| 5. Voice | `voice-scan.py 35 --summary` on the bank folder: explanations over three sentences 0, sentences over 35 words 0 (two file `description` lines of 37 and 38 words were cut). |
| 6. Wrong answers route | Scratch script through `ZQ.grade.numGrade` as in session 3: 90 cases, 26 keys right, 52 wrong ids each resolved to their own id with a `byKey` line, 12 distractors each with a `why`. |
| 7. Counts | Below; they match sections 2, 3 and 5. |

### Freshness hits (`--min-run 10 --min-share 0`)

- `statistics-2` `es-mle-two-coins-ratio` against `exams/mock-oa-sig` parts[0].items[16] (run 10, "a coin is either fair or lands heads with chance"): a different problem (a gambler's posterior); prose rewritten.
- `finance-2` `fi-bonds-zero-coupon-yield` against `exp-log/homework-3` items[0] (run 10): that item prices a bond from a continuous yield; prose rewritten.
- `finance-2` `fi-forwards-rich-forward` against `markets/homework-3` items[2] and `markets/review-3` items[2] (run 10 on the question line, share 0.22): the same setup family (a rich one-year forward, riskless profit at delivery; homework-3 also has a dividend). Numbers differ (200, 4, 3% simple, 205 against 100, 2, 5% yearly, 104), so the item stands; the question line was reworded. A second reader should judge whether the template is too close.
- `finance-2` `ms-book-weighted-mid` against `micro/homework-2` items[8] (run 10, "the best bid is ... the best ask"): stock book wording; rewritten.

## Counts

| File | Items | D2 | D3 | D4 | D5 | numeric | choice | longform | with `requires` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| statistics-2 | 15 | 4 | 5 | 5 | 1 | 12 | 3 | 0 | 6 |
| finance-2 | 15 | 5 | 3 | 7 | 0 | 14 | 1 | 0 | 7 |
| behavioural-6 | 8 | 0 | 4 | 3 | 1 | 0 | 0 | 8 | 4 |

Families match section 3 (statistics `ht-pvalue` 2, the other 13 one each; finance `fi-forwards` and `op-strategies` 2 each, the other 11 one each; behavioural `star-story` 3, `why-us`, `reasoning-aloud`, `final-round`, `after-rejection`, `project-account` 1 each). With `coding-2` (D2 3, D3 7, D4 1, D5 1; 6 code, 2 numeric, 4 choice) the session totals of section 2 follow: D2 12, D3 19, D4 16, D5 3; numeric 28, choice 8.

## Each number and its two routes

Same helpers as session 3. Route B per item:

| Item | Route A | Route B |
| --- | --- | --- |
| es-mle-two-coins-ratio | Fraction | enumeration of all 32 sequences |
| shrinkage-mse-best-multiplier | Fraction 9/12 | grid search of the error (also "smallest") |
| es-intervals-poll-margin | binomial formula | 20,000 seeded polls, tolerance 0.05 points |
| es-bayes-prior-and-sample | precision weights | midpoint integral of prior times likelihood |
| ht-setup-ten-paired-days | formula | ten built differences with mean 1.2, sd 1.5 |
| ht-pvalue-z-two-and-a-half | `NormalDist` | `erfc` |
| ht-pvalue-bigger-sample | root-n scaling | z recomputed from mean, sd and n |
| ht-errors-equal-error-cutoff | symmetry, c = 1.5 | bisection on the two error curves; `erfc` |
| rg-fit-point-at-the-mean | least squares | normal equations; slope 2.5 at four heights of the new point |
| rg-multiple-useless-predictor | 2,000 seeded fits (seed 2): 1,362 and 0 | exact P(abs t < 1) on 47 df = 0.678, tolerance three binomial sds |
| collinear-features-inflation-factor | Fraction 1/0.19 | inverse of the correlation matrix |
| ts-forecast-two-steps-ahead | Fraction | iterated forecast |
| ts-acf-two-day-variance-ratio | 1 + rho | 400,000-step seeded MA(1), tolerance 0.01 |
| measurement-error-noisy-regressor | Fraction 5/8 | 200,000-point seeded regression, tolerance 0.01 |
| dl-clt-mean-of-hundred | `NormalDist` | `erfc` |
| fi-interest-three-payments-pv | annuity formula | sum of discounted payments |
| fi-bonds-zero-coupon-yield | root | bisection on the price |
| fi-forwards-rich-forward | Fraction fair value | cash-flow ledger of the arbitrage |
| fi-forwards-futures-daily-loss | product | point-by-point sum |
| op-strategies-covered-call-at-fifty | formula | ledger |
| op-strategies-butterfly-best-case | Fraction | payoff scan |
| op-parity-call-under-its-floor | Fraction | worst case over expiry prices |
| gamma-pnl-break-even-move | closed form | bisection |
| digital-option-at-the-money | N(d2) | tight call spread of Black-Scholes; 400,000 seeded paths, tolerance 0.003 |
| tp-multistep-two-step-call | risk-neutral Fraction | replication by backward induction |
| ms-book-weighted-mid | Fraction | mid shifted by size share |
| ms-costs-impact-four-times-size | ratio | fitted constant |
| ms-mm-spread-less-drift | Fraction | loop |
| gv-risk-two-desks | sqrt 3 | 400,000 seeded correlated P&Ls, 1% quantile, tolerance 0.02 |
| exotic-ranking-basket-or-calls | 400,000 seeded paths (8.06) | one-dimensional integral with a closed-form inner price (8.050) |

Behavioural: as session 3 (models 156 to 174 words). The figures in two models are checked: five losses at 45% each is 1.8%, and a run of five somewhere in 40 trades is 0.326 by an exact chain and by 100,000 seeded games ("about one game in three"); a hit rate over 250 days has standard error 3.2 points, so 53% is one standard error above 50%.

## Differences from section 5

Answers that differ from the brief: **0 keys; 1 slip value, 1 printed figure.**

- `gamma-pnl-break-even-move`: the brief's slip 1.125 "no square root" does not follow: stopping at the squared move gives $2 \times 0.045/0.04 = 2.25$ (1.125 is $\theta/\Gamma$, both the half and the root left out). The `no-root` slip is 2.25 (band 0.05, which holds 2.2 and 2.3); `no-half` is 1.1 (1.06 rounded).
- `exotic-ranking-basket-or-calls`: the planner's settings for "9.95 against 8.13" are not given. Mine are vol 25%, one year, zero rate, correlation 0.3: the half calls cost 9.95 (closed form) and the basket call 8.05 (exact integral; simulation 8.06). The option text states the conclusion only.
- `rg-multiple-useless-predictor`: my seed gives 1,362 of 2,000 (the planner's 1,371); the exact chance is 0.678.
- Tolerances: the 4-place keys (`ht-errors-equal-error-cutoff` 0.0668, `dl-clt-mean-of-hundred` 0.0228, `digital-option-at-the-money` 0.4701) use half a unit, 0.00005, not the brief's 0.0005, with their slips at the same band (`cutoff-at-three` 0.0013 at 0.00006, so it holds 0.00135). Whole keys take 0. Per cent keys (`es-bayes-prior-and-sample`, `fi-bonds-zero-coupon-yield`) are fractions with `unit: "%"`.
- `tp-multistep-two-step-call`: the `even-chances` slip is stored as 5.625 with band 0.005, so both 5.62 and 5.63 meet it.
- `es-intervals-poll-margin`: the `no-multiplier` slip (2.449, asked to 1 place) has band 0.05 so 2.4 and 2.45 both meet it.
- No item swapped; no family changed. No `[verify]` item in this session.

## Open questions

- `coding-2.json` waits for B2-E1 to B2-E5 (it holds the hardest code item, `gd-dp-walk-above-zero`).
- `fi-forwards-rich-forward` shares a setup family with two `markets` items (above).
- B2-E3, B2-E4 and B2-E5 are still open, as in session 3.

## Coding file

Written after engine pass AB-2: `app/content/bank/coding-2.json`, 12 items. Number checks: the coding section of `docs/reports/bank-2-s2-numbers.py`, which imports `docs/reports/bank_2_code_check.py` (session 1's runner). House style as session 1's "Coding file" section.

| Step | Result |
| --- | --- |
| 1. Validator | `0 errors, 4857 warnings`, the baseline; no warning names `coding-2`. |
| 2. Numbers | `<scratchpad>/venv/bin/python docs/reports/bank-2-s2-numbers.py`: `1119 checks, 0 failed`, exit 0 (749 before), about 26 s. A planted wrong expect (16,795 for 16,796) fails it three ways. The script's voice check now ignores Python's `!=`. |
| 3. Playthrough | `--bank coding-2 --local-cdn <pkgs>`: 12 of 12, 6 starters fail first, `All passed.`; `--mobile --why`: 24 of 24 at 1280 and 440 px, 16 slip lines shown at each width. `--routes-only`: `All passed.` |
| 4. Freshness | `fresh-check.mjs --bank coding-2`: 0 hits; one stem advisory, then at `--min-run 8 --min-share 0` one hit, against `coding-int/review-4` items[2] (a multi that asks which inputs are edge cases of `second_largest`; run 9, share 0.27). The task differs (choose tests, not write the function); the prose was rewritten and the hit is gone at every setting. |
| 5. Voice | 0 and 0 on the bank folder. |
| 6. Wrong answers route | `--why`: 4 `wrong` ids and 12 distractors, each shows its own line. |

Counts: D2 3, D3 7, D4 1, D5 1; 6 code, 2 numeric, 4 choice; two with `requires`. Families: `pf-idioms` 2, `pf-collections` 2, `pf-functions`, `at-recursion`, `ds-arrays`, `ds-hashing`, `ds-pointers`, `gd-dp`, `edge-case-list`, `copy-vs-move` 1 each (section 3). Session 2 now totals D2 12, D3 19, D4 16, D5 3; numeric 28, choice 8, code 6, longform 8.

| Item | Route B (brute force) | Near-misses run, and the tests they fail |
| --- | --- | --- |
| pf-idioms-argmax-last | `max` over the reversed list | `xs.index(max(xs))` gives 1; strict `>`; `max` over indices (each 1, 5 to 8) |
| edge-case-list-second-largest | `sorted(set(xs))` with a length check | `sorted(xs)[-2]` gives 5 and 2 (1 to 3, 5, 7, 8); distinct, no guard (2, 3, 5); guarded, repeats kept (1, 3, 7, 8) |
| ds-pointers-merge-ticks | stable sort on the time alone | `sorted(a + b)`; two pointers with `<`; `heapq.merge` on whole tuples (each 1, 5, 8) |
| ds-arrays-round-trips | `accumulate` positions | every zero position gives 4 and 2 (1, 2, 7); crossings counted too (4) |
| pf-collections-top-symbols | `Counter` and `heapq.nsmallest` | stable sort by total alone; `most_common` (each 1, 2, 4, 7); reverse on (total, symbol) (1, 2, 4, 7, 8) |
| gd-dp-walk-above-zero | depth-first count to n = 22, ballot formula above | all $2^n$ paths listed, and depth-first pruned at -1: both out of time at n = 60 (8, 9); the floor left out (2 to 9); unreachable ends kept (2 to 5) |

Reasoning items run their own lines: `max(d, key=d.get)` is "to" (the later tie "be" and the last key "not" checked); the lambdas give 36, and binding i early gives 33; an instrumented `f` makes 13 calls (6 that add, 7 that return 1); the snippet prints `14 0`. `ds-hashing-list-membership` runs its own lines on 2,000 ids of a type that counts `==`: $n(n-1)/2$ comparisons for the list, a tuple and a re-sorted list, none for the set; $0 + 1 + \dots + 19{,}999 = 199{,}990{,}000$ two ways. The C++ item compiles its lines with `g++ -std=c++20` and prints sizes 3 and 4 with separate storage; the Python lines give one list of 4.

**Differences from section 5: 0 keys; 3 items.**

- `pf-collections-top-symbols`: real tickers (`VOD`, `BP`, `AZN`, `HSBA`) replaced by invented ones (`TUV`, `FGH`, `BCD`, `MNO`) in the same pattern, rule 2. The answers read `["BCD", "FGH"]` and `["BCD", "FGH", "TUV"]`; the trap still gives the first-appearance order.
- `gd-dp-walk-above-zero`: the hidden tests add n = 60 (Catalan 30 at 0, $\binom{60}{30}$ in all) and the prose says n reaches 60. In CPython, listing all $2^{22}$ paths ran inside the 5 s limit and a pruned depth-first count passes n = 22 easily, so n = 22 alone does not force the table method. n = 22 stays as a test.
- `ds-hashing-list-membership`: the brief's dedupe loop is in `contests/l2-limits-to-complexity` (a step-count question), so the snippet counts repeats with `if x in seen`, as the brief's wording has it. The timing figures were dropped for a comparison count the script reproduces.
- Also: `second_largest` prose reworded for freshness (above).

**Freshness by hand:** none of the six function names occurs in a drill or a course code item; `lambda x: x + i`, `"to be or not"`, `n // 3`, `auto w = v` and `sum(g)` occur nowhere else in content.
