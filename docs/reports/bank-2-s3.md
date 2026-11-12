# Bank part 2, session 3 (author B): partial hand-in

Brief: `docs/briefs/bank-2.md`. Written: `app/content/bank/statistics-3.json` (15), `finance-3.json` (15), `behavioural-7.json` (8), 38 items. Not written: `coding-3.json` (12), which waits for engine requirement B2-E1. Number script: `docs/reports/bank-2-s3-numbers.py` (standard library only, plain `python3`). House style copied from `docs/reports/bank-2-s1.md` (question line, rubric time lines, spoken-item feedback, per cent keys as fractions with `unit: "%"`).

## Acceptance (section 7)

| Step | Result |
| --- | --- |
| 1. Validator | `0 errors, 4664 warnings`, the baseline before this session; 0 warnings name the three files (no `[tight-band]`, `[wide-wrong-band]`, `[wrong-band]`, `[answer-form]`, `[key-length]`, `[shown-arithmetic]`, and the 20-word advisory `[O2-long-sentence]` is silent too). |
| 2. Numbers | `python3 docs/reports/bank-2-s3-numbers.py`: `790 checks, 0 failed`, exit 0. A planted wrong key and a planted wrong slip each fail it. |
| 3. Playthrough | `--bank statistics-3 --bank finance-3 --bank behavioural-7 --local-cdn <pkgs>`: `bank total: 38 of 38 items passed in 3 files`, `All passed.` With `--mobile`: 38 of 38, `All passed.` (B2-E3 is still open: `bankPlay` never resizes, so `--mobile` adds no phone pass for `--bank`.) `--routes-only` with and without `--mobile`: `All passed.` |
| 4. Freshness | `fresh-check.mjs --bank <file>`: 0 hits, exit 0, each file; `--min-run 10`: 0 each. `--min-run 10 --min-share 0`: 3 hits, all rewritten (below); now 0 on all three. Session 1's files are in the comparison set (the finance-1 hit shows it). |
| 5. Voice | `voice-scan.py 35 --summary` on the bank folder: explanations over three sentences 0, sentences over 35 words 0. |
| 6. Wrong answers route | A scratch script (not committed) loads `js/engine/grade.js` and types each key and each `wrong` value into `ZQ.grade.numGrade` (per cent items as "14.286%"): 95 cases, 27 keys right, 59 wrong ids each resolved to their own id with a `byKey` line, 9 distractors each with a `why`. |
| 7. Counts | Below; they match sections 2, 3 and 5. |

### Freshness hits (`--min-run 10 --min-share 0`)

- `finance-3` `op-strategies-one-by-two-breakeven` against `bank/finance-1` items[5] (run 12, the break-even question line): stock phrasing, different trade; rewritten to "Where above 110 does the position break even at expiry, in pounds?".
- `behavioural-7` `video-answer-competed-and-lost` against `behavioural-2` items[3] and `behavioural-4` items[5] (run 11, "you have thirty seconds to prepare and two minutes to answer"): stock video-format wording; rewritten to "You get thirty seconds to think, then two minutes to record."

## Counts

| File | Items | D2 | D3 | D4 | D5 | numeric | choice | longform | with `requires` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| statistics-3 | 15 | 1 | 8 | 4 | 2 | 13 | 2 | 0 | 6 |
| finance-3 | 15 | 1 | 10 | 4 | 0 | 14 | 1 | 0 | 4 |
| behavioural-7 | 8 | 0 | 5 | 3 | 0 | 0 | 0 | 8 | 3 |

Families: one item for each of the 15 statistics families of section 5; finance `fi-bonds`, `fi-forwards` and `tp-bs` two each, the other nine one each; behavioural `star-story` 3, `why-us`, `reasoning-aloud`, `video-answer`, `return-offer`, `cv-lines` 1 each. All match section 3. With `coding-3` (D2 3, D3 5, D4 4; 6 code, 3 numeric, 3 choice) the session totals of section 2 follow: D2 5, D3 28, D4 15, D5 2; numeric 30, choice 6.

## Each number and its two routes

Every check is an `ok`, `two`, `numeric`, `choice` or `stated` line in the script, in item order. `numeric()` asserts the key, its rounding as asked, each slip inside its own band (and as rounded), no band touching the key or another slip, no band over half its value, and a `byKey` line per id.

| Item | Route A | Route B |
| --- | --- | --- |
| es-estimators-pool-two-estimates | Fraction 1/(1/4 + 1/12) | grid search over the weight (also the "smallest" claim) |
| estimator-bias-divide-by-n | Fraction 4/5 x 10 | 200,000 seeded samples of five, tolerance 0.05 |
| es-intervals-wider-confidence | Fraction centre and half-width | solve for the standard error first |
| es-bayes-arrivals-per-day | conjugate gamma 15/6 | midpoint integral of prior times likelihood |
| ht-setup-die-sixty-rolls | Fraction sum of (O - E)^2/E | sum O^2/E - n; the 5% point 11.07 by closed-form survival and by integral |
| weak-signal-daily-edge | Fraction | float; 1,600 days by count-up |
| ht-errors-sample-for-power | ceiling of the formula | count-up on exact two-sided power (0.7995 at 196, the "smallest" claim) |
| ht-multiple-share-false | Fraction 2/14 | 20,000 seeded runs of 200 null tests, tolerance 0.002 |
| rg-fit-correlation-from-sums | -sqrt(0.75) | least squares on four built points with TSS 200, RSS 50 |
| rg-inference-new-observation | 2 sqrt(1 + 1/25) | 40,000 seeded fits and new points, tolerance 0.02 |
| rg-diagnostics-fanning-residuals | 4,000 seeded fits (seed 20261111) | exact conditional variances on fresh designs (sandwich), tolerance 0.002 |
| rg-multiple-partial-out | residual on residual | 2 x 2 normal equations; each distractor recipe shown to miss |
| ts-forecast-half-life | ln 0.5/ln 0.75 | bisection |
| ts-acf-noise-band | 1.96/sqrt(400) | 4,000 seeded white-noise series, tolerance 0.004 |
| equicorrelation-many-assets-vol | Fraction formula | full 25 x 25 double sum |
| fi-interest-loan-payment | annuity formula | bisection on the year-by-year balance |
| fi-bonds-three-year-coupon | Fraction sum | backward loop |
| fi-bonds-pound-per-basis-point | Fraction | finite difference of a duration-4.5 price |
| fi-forwards-geared-loss | Fraction balance sheet | gearing identity |
| fi-forwards-currency-forward | Fraction covered parity | float round trip |
| op-payoff-short-strangle-loss | Fraction | payoff function |
| op-strategies-one-by-two-breakeven | closed form | scan of the expiry payoff |
| op-parity-implied-forward | Fraction parity | spot by parity, then grown |
| op-greeks-vol-move-pnl | Fraction | repricing a linear-in-vol value |
| tp-bs-at-the-money-delta | N(0.2) | finite difference of Black-Scholes; erf |
| tp-riskneutral-analyst-view | risk-neutral Fraction | replication with shares and cash |
| tp-multistep-monthly-up-factor | exp | power series |
| ms-book-who-gets-filled | priority sort | share-by-share matching loop |
| ms-costs-shortfall-with-unfilled | Fraction | paper portfolio against the real one |
| tp-bs-vega-rule | S N'(d1) sqrt(T) | finite difference in vol; the 0.4 rule inside the band |

Behavioural: model length (154 to 168 words), rubric 2, 2, 2, 2, 1, 1, the `question` line, no `prose`, pace 120 where "two minutes" appears, part 1's feedback lines, distinct `question` lines, at most one backtest story (none here).

## Differences from section 5

Answers that differ from the brief: **0 keys; 2 slips renamed, values kept.**

- `op-strategies-one-by-two-breakeven`: the brief's slip 115 "halved the fall" does not follow (halving the fall gives 130). 115 is what you get when the payoff falls two for one above 110, forgetting the long call; the slip is `two-for-one` with that text.
- `op-greeks-vol-move-pnl`: the brief's slip 18 "one contract of one option" does not follow (one option gives 0.36). 18 is 50 contracts of one option each, the multiplier left out; the slip is `no-multiplier`. A third slip `one-contract` (36, one contract of 100 options) was added.
- `weak-signal-daily-edge`: asked to 2 decimal places, not 1, so the no-root slip 0.05 is printed at the asked places; at 1 place it is an exact rounding half and needed the brief's special band.
- Added slips on the other side of the key (rule 8): `es-estimators` total precision 1/3, `ht-errors` rounded down 196, `rg-fit` root of 50/200 (-0.5), `fi-forwards-geared-loss` sign (+24%).
- Tolerances: whole keys take 0 (`es-estimators` 3, `estimator-bias` 8; brief 0.005). Per cent keys (`ht-multiple`, `equicorrelation`, `fi-forwards-geared-loss`) are fractions with `unit: "%"`, bands 0.0005, 0.0005 and 0.00005.
- Stored precision: unrounded keys are stored to at most d + 2 places (`ts-forecast-half-life` 2.409) so `[tight-band]` stays silent; bands are the brief's.
- Simulated figures (section 6): my seeds give 0.500, 0.057 and 0.063 for the fanning residuals (noise sd 0.2x, 50 points, 4,000 samples) and 1.981 and 2.888 for partialling out (20,000 points, true coefficient 2); these are in the items. The planner's 0.497, 0.152, 0.163, 2.006 and 1.51 are not.
- No item swapped; no family changed. No `[verify]` item in this session.

## Open questions

- `coding-3.json` waits for B2-E1 to B2-E5.
- `[bank-family]` (B2-E5) and `numbers_lib.Bank` (B2-E4) are not built; families were checked by hand and the script reads the JSON itself.
- B2-E3: the phone pass of step 3 is still empty for `--bank`.

## Coding file

`app/content/bank/coding-3.json`, 12 items, written after engine pass AB-2 (ENGINE-BACKLOG 920 to 925). Checks are in `docs/reports/bank-2-s3-numbers.py` (section "coding helpers" and "coding-3"), run with the scratchpad venv Python (NumPy for the broadcast item, `g++ -std=c++20` for the C++ item).

| Step | Result |
| --- | --- |
| 1. Validator | `0 errors, 4856 warnings`, the baseline without the file; 0 warnings name `coding-3` (no `[bank-code]`, `[bank-family]`, `[O2-long-sentence]`). |
| 2. Numbers | `venv/bin/python docs/reports/bank-2-s3-numbers.py`: `1245 checks, 0 failed`, exit 0, about 10 s. |
| 3. Playthrough | `--bank coding-3 --local-cdn <pkgs>`: 12 of 12, 6 starters fail first. `--mobile`: 24 of 24 at 1280 and 440 px. `--why`: 12 of 12, 18 slip lines shown. All passed. |
| 4. Freshness | `fresh-check.mjs --bank coding-3`: 0 hits, exit 0; `--min-run 10`: 0 hits. Advisories: `at-search-stuck-loop` shares the stock binary-search lines with `algo-think/l9-halving` screen 8 and `review-3` item 1 (that screen asks which loop test goes with `lo = mid + 1`; this item is the `lo = mid` fault): kept. `np-broadcast-column-plus-row` shares `a = np.array ... b = np.array ... print(a + b)` with `numpy-pandas/l1-not-lists` screen 3 (two 1-D arrays of unequal length, an error): stock phrasing, kept. No function name matches a drill or lesson. |
| 5. Voice | `voice-scan.py 35 --summary` on the bank folder: 0 and 0 (a 36-word file description was cut first). |

Counts: D2 3, D3 5, D4 4 (4 with `requires`); 6 code, 3 numeric, 3 choice; families as section 3. Session totals with the three earlier files: D2 5, D3 28, D4 15, D5 2; numeric 30, choice 6, code 6, longform 8, as section 2.

House style for the code items (copied from AB-2): `language: "python"`, two examples that are also hidden tests, 8 to 10 hidden tests, `compare: "equal"`, the `how` line "Submit runs N hidden tests. Each result must equal the expected whole number." (or "... the expected value." for a list result), feedback "Every hidden test passed." and a generic line that points to the method.

### Each code task: tests, twin and near-misses

The script runs `solution` on every case (each under 1 s in CPython), the untouched starter on every test (it fails), a brute-force twin that shares no code with the model on every case, and each near-miss.

| Item | Twin | Near-misses run, and the first test each fails |
| --- | --- | --- |
| pf-idioms-trend-direction | set of signs of every difference | first against last: `[1, 1, 2]`; non-strict: `[1, 1, 2]` |
| at-sort-largest-gap | values popped off a heap | gaps in input order (12): `[10, 3, 8, 20]`; max less min (17): same |
| at-greedy-orders-to-fill | every subset by size (small), heap of the largest (large) | input order (3): the 450 case; total strictly above target: the 750 case and `([300], 300)` |
| at-search-count-in-range | `Counter` over the whole numbers of the range | no guard for hi below lo (-5): `(9, 2)`; linear scan: right on the 7 small tests, past 5 s on 1,000 calls over 1,000,000 values |
| simulation-rules-clip-position | one share at a time | reject a breaching order whole (`[6, 0, 0, 3]`); clip the long side only: `[-4, -4, 9, 9]` |
| at-recursion-depth-weighted-sum | bracket depth read off `repr` | plain sum (10, 9); top list at depth 0 (13) |

Edge cases in the hidden tests: empty and one-element lists, ties (`[3, 3]`, `[4, 4, 4]`, `[2, 2, 2]`), negatives, a target equal to a total, `hi` below `lo`, limit 0, a 100,000-long input for each list task, and a list nested 200 deep (under the 300-call limit for a solution that puts a generator in each call).

### Reading items

Each runs its own lines: `pf-idioms-stable-ties` prints `['c', 'b', 'a']` (slips by sorting on `(number, letter)`, on the letter, and not at all); `at-search-stuck-loop` is traced with a step cap and sticks at lo 2, hi 3 (with `lo <= hi` it sticks too; `lo = mid + 1` ends at 3); `ds-stacks-push-pop-trace` prints 14 (a deque popped from the front gives 10); `gd-dp-table-size` prints 70; `np-broadcast-column-plus-row` prints 324 in NumPy and by a double loop; `virtual-dispatch-missing-virtual` is compiled and run with g++ (prints B, and D once `virtual` is added).

### Differences from section 5

Answers that differ from the brief: **0 keys; 1 slip replaced.**

- `np-broadcast-column-plus-row`: the brief's slip 312 ("counted a once per row: 12 + 300") does not follow from any reading of the code. Replaced by 418 (each sum repeated by its own length, $3 \times 6 + 4 \times 100$) and 66 (paired by position, as `zip` would). 106 kept.
- Third slips added (rule 8): `ds-stacks-push-pop-trace` 12 (only the first two pops), `gd-dp-table-size` 17 (added 7 and 10).
- `at-search-count-in-range`: the brief's large case (one call on 1,000,000 values) passes with a linear scan inside the 5 s limit, so it cannot enforce $O(\log n)$. Added a test of 1,000 calls on the same list (6,000), which a linear scan cannot finish.
- No item swapped; no family changed.
