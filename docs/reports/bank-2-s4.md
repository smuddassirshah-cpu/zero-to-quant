# Bank part 2, session 4 (author B): partial hand-in

Brief: `docs/briefs/bank-2.md`. Written: `app/content/bank/statistics-4.json` (15), `finance-4.json` (15), `behavioural-8.json` (8), 38 items, one commit per file. Not written: `coding-4.json` (12), which waits for engine requirement B2-E1. Number script: `docs/reports/bank-2-s4-numbers.py` (standard library only, plain `python3`). House style copied from `docs/reports/bank-2-s1.md` and `bank-2-s3.md` (question line, rubric time lines, spoken-item feedback, per cent keys as fractions with `unit: "%"`, unrounded keys stored to at most d + 2 places).

## Acceptance (section 7)

| Step | Result |
| --- | --- |
| 1. Validator | `0 errors, 4663 warnings`, the same count with the three files removed (the baseline today); 0 warnings name the three files, the 20-word advisory `[O2-long-sentence]` included. |
| 2. Numbers | `python3 docs/reports/bank-2-s4-numbers.py`: `745 checks, 0 failed`, exit 0. A planted wrong key (0.5662 for 0.5642) and a planted wrong slip (5.88 for 5.86) fail it with 5 checks. |
| 3. Playthrough | `--bank statistics-4 --bank finance-4 --bank behavioural-8 --local-cdn <pkgs>`: `bank total: 38 of 38 items passed in 3 files`, `All passed.` With `--mobile`: 38 of 38, `All passed.`; the 440 px result screenshots read cleanly (B2-E3 still open: no phone pass of the deal itself). `--routes-only` with and without `--mobile`: `All passed.`, `#bank 208 drawable of 352 in 32 files (144 locked)`. |
| 4. Freshness | `fresh-check.mjs --bank <file>`: 0 hits, each file; `--min-run 10`: 0 each. `--min-run 10 --min-share 0`: 1 hit (below), rewritten; now 0 on all three. The nine part 2 files written so far are in the comparison set; I also read their ids and set-ups by hand (below). |
| 5. Voice | `voice-scan.py 35 --summary` on the bank folder: explanations over three sentences 0, sentences over 35 words 0 (a 37-word file description and a 49-word model sentence were cut first). |
| 6. Wrong answers route | Scratch script (not committed) loading `js/engine/grade.js` and typing each key and `wrong` value into `ZQ.grade.numGrade` (per cent items as "1.2166%"): 91 cases, 24 keys right, 49 wrong ids each routed to their own id with a `byKey` line, 18 distractors each with a `why`, 0 bad. |
| 7. Counts | Below; they match sections 2, 3 and 5. |

### Freshness

- `statistics-4` `gv-models-ewma-after-a-shock` against `exams/stage-2` parts[1].items[8] (run 11, share 0.37: "yesterday's volatility estimate was ... a day, and today's return"). Same stock one-step EWMA update with decay 0.94; numbers differ (1% and 3% against 0.011 and -0.028) and the exam asks 5 places. Prose rewritten; the brief's template kept.
- Against part 2 by hand: `rg-inference-overall-f` (F from R² with 3 predictors) is near `statistics-1` `rg-inference-t-from-r-squared` (t from R² with one predictor) but asks a different statistic with degrees of freedom; `fi-bonds-duration-and-convexity` extends `finance-1` `fi-bonds-duration-move` (duration only) with the convexity term; `reasoning-aloud-correct-me-politely` (gambler's fallacy) is unlike `behavioural-6` `reasoning-aloud-five-losses-running` (luck against error); `digital-option-from-two-calls` (call spread) is unlike `finance-2` `digital-option-at-the-money` (Black-Scholes). All kept.

## Counts

| File | Items | D2 | D3 | D4 | D5 | numeric | choice | longform | with `requires` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| statistics-4 | 15 | 4 | 5 | 5 | 1 | 12 | 3 | 0 | 6 |
| finance-4 | 15 | 4 | 4 | 6 | 1 | 12 | 3 | 0 | 7 |
| behavioural-8 | 8 | 0 | 4 | 3 | 1 | 0 | 0 | 8 | 4 |

Families: one item for each of the 15 statistics and 15 finance families of section 5; behavioural `star-story` 3, `why-us`, `reasoning-aloud`, `final-round`, `after-rejection`, `project-account` 1 each, as section 3. With `coding-4` (D2 1, D3 7, D4 4; 6 code, 3 numeric, 3 choice) the session totals of section 2 follow: D2 9, D3 20, D4 18, D5 3; numeric 27, choice 9, longform 8.

## Each number and its two routes

Every check is an `ok`, `two`, `numeric`, `choice` or `stated` line in the script, in item order. `numeric()` asserts the key, its rounding as asked, each slip inside its own band and as rounded, no band touching the key or another slip, no band over half its value, and a `byKey` line per id.

| Item | Route A | Route B |
| --- | --- | --- |
| es-estimators-error-of-the-vol | σ/√(2n) | exact sd of s by the c4 constant (0.1205), and 40,000 seeded samples, tolerance 0.002 |
| es-mle-best-precision-rate | Fraction n/(p(1-p)) = 625 | Fisher information summed over all 101 binomial outcomes; the sample proportion's variance by enumeration (the "smallest" claim) |
| es-intervals-two-desk-gap | Fraction | pooled-form float |
| es-bayes-three-from-three | Fraction 4/5 | midpoint integral of p⁴ over p³ |
| sm-nonpar-shuffled-labels | the 10 splits | all 120 orderings |
| ht-setup-one-or-two-sided | `NormalDist` | `erf`; cut-offs 1.645 and 1.96 by `inv_cdf` |
| ht-multiple-better-of-two | 1/√π | integral of 2zφ(z)Φ(z); 400,000 seeded pairs, tolerance 0.005 |
| power-half-the-effect | Fraction 150 × 4 | count-up on the power function at half the effect |
| rg-fit-next-year-return | Fraction | fitted line on 400,000 seeded pairs, tolerance 0.1 points |
| rg-inference-overall-f | Fraction 40/7 | sums of squares of a real 44-point fit with 3 predictors built to R² 0.3 (Gaussian elimination) |
| rg-diagnostics-most-leverage | 1/n + (x - x̄)²/Sxx | diagonal of the hat matrix |
| rg-multiple-dummy-and-slope | the model | the D = 1 line, 7 + 3.5x |
| gv-models-ewma-after-a-shock | update formula | EWMA as a weighted sum over a 3,000-day flat history |
| gv-forecast-long-run-vol | ω/(1 - α - β) | iterating the variance forecast 5,000 steps |
| co-spurious-two-walks | slope over its usual error | t from the correlation, r√(n-2)/√(1-r²); seed 20261111 |
| fi-interest-one-year-forward-rate | Fraction | a pound compounded in floats |
| fi-bonds-duration-and-convexity | Fraction | a price curve built with D 8 and C 80, checked by finite differences |
| fi-equity-combine-two-sharpes | √(0.36 + 0.64) | search over 100,001 weights (the "highest" claim); best weight ∝ Sharpe over vol |
| fi-forwards-implied-rate | 2 ln 1.02 | bisection on 100e^(r/2) = 102 |
| digital-option-from-two-calls | Fraction | float |
| op-strategies-protective-put-floor | closed form | scan of the expiry value |
| op-parity-exercise-before-dividend | parity: 10 against 8.80 | the dividend rule 2.00 - 0.80 |
| gamma-pnl-hedger-trades | N(d1) | finite difference of Black-Scholes |
| op-greeks-put-delta-from-call | parity | finite difference of a Black-Scholes put at call delta 0.62 |
| tp-multistep-lookback-two-step | path enumeration | backward induction on (price, running high) |
| ms-book-opening-auction | the four limit prices | a price scan in steps of 0.01 |
| ms-orders-immediate-or-cancel | level sum | share-by-share fill |
| ms-costs-participation-time | Fraction | hour-by-hour loop |
| option-estimate-straddle-implied-move | the 0.8 rule | exact Black-Scholes solve by bisection (10.03%, inside the band) |
| tp-bs-delta-and-finishing-chance | Φ(d1 - σ√T) | 400,000 seeded risk-neutral finishes, tolerance 0.002 |

Behavioural: model length (151 to 172 words), rubric 2, 2, 2, 2, 1, 1, the `question` line, no `prose`, pace 120 where "two minutes" appears, part 1's feedback lines, distinct `question` lines, no backtest story. Figures in the models are checked too: 1/32 and 2 of 64 sequences (coin), 6 and 14 expected flips for two and three heads (by formula and by solving the chain), 3.1 against 4.6 as about a third less, three Fridays of twenty sheets.

## Differences from section 5

Answers that differ from the brief: **0 keys; 3 slips, 1 question form.**

- `gv-forecast-long-run-vol`: the slip "0.02 (gave the variance times 100: 0.0225; band 0.001)" does not follow: 0.0225 lies outside 0.02 ± 0.001, and at the asked 1 place it reads 0.0, so no band can route it. Replaced by `one-minus-beta`, 0.6% ($\sqrt{0.0000045/0.12} = 0.612\%$). The annualised slip 23.8 stands.
- `fi-forwards-implied-rate`: the slip 4.04 "compounded twice a year" does not follow: twice-yearly compounding gives 4.00%, the simple slip. 4.04% is $1.02^2 - 1$, the annual effective rate; the slip is `annual-effective` with that text.
- `sm-nonpar-shuffled-labels`: 0.05 "counted ordered pairs" does not follow as named: counting ordered pairs throughout gives 2/20 = 0.1. 0.05 is 20 ordered pairs over one order of {8, 9}; the `byKey` text says so. Value kept.
- `es-mle-best-precision-rate`: asked "as a decimal", not "to 2 decimal places". At 2 places the variance slip 0.0016 reads 0.00, so its band could not route it and `[wrong-band]` fires; the brief's bands (0.0005 and 0.0001) fit "as a decimal".
- Added slip on the other side of the key (rule 8): `fi-bonds` sign (+7.6%).
- Tolerances: whole keys take 0 (`tp-multistep-lookback-two-step` 16; brief 0.005). Per cent keys are fractions with `unit: "%"`, bands the brief's divided by 100.
- Stored precision: `ht-multiple` 0.5642, `rg-inference` 5.7143, `gv-models` 0.012166, `fi-interest` 0.050097, `fi-forwards` 0.039605.
- Simulated figures (section 6): my seed gives 88.0% beyond 1.96 in levels and 5.0% after differencing (planner 88.5% and 5.1%); mine are in the item. The script also shows 77.2% at 100 steps, so the "longer sample is worse" `why` holds.
- Wording: `gamma-pnl-hedger-trades` names the call (three months, at the money, 20%, zero rates, share 100 to 101) in the prose, so the 0.52 and 0.56 of the explanation belong to the item; `op-parity-exercise-before-dividend` names share £60 and strike £50, so the £10 and £8.80 do.
- No item swapped; no family changed. No `[verify]` item in this session.

## Open questions

- `coding-4.json` waits for B2-E1 to B2-E5.
- `[bank-family]` (B2-E5) and `numbers_lib.Bank` (B2-E4) are not built; families were checked by hand and the script reads the JSON itself.
- B2-E3: the phone pass of step 3 is still empty for `--bank`.

## Coding file

`app/content/bank/coding-4.json`, 12 items, written after engine pass AB-2 (ENGINE-BACKLOG 920 to 925), in the house style of `coding-3` (`docs/reports/bank-2-s3.md`, "Coding file"). Checks are in `docs/reports/bank-2-s4-numbers.py` (sections "coding helpers" and "coding-4"), run with the scratchpad venv Python and `g++ -std=c++20`.

| Step | Result |
| --- | --- |
| 1. Validator | `0 errors, 4856 warnings`, the baseline without the file; 0 warnings name `coding-4` (no `[bank-code]`, `[bank-family]`, `[O2-long-sentence]`). |
| 2. Numbers | `venv/bin/python docs/reports/bank-2-s4-numbers.py`: `1189 checks, 0 failed`, exit 0, about 20 s (two slow near-misses run to their 5 s limit). |
| 3. Playthrough | `--bank coding-4 --local-cdn <pkgs>`: 12 of 12, 6 starters fail first. `--mobile`: 24 of 24 at 1280 and 440 px. `--why`: 12 of 12. All passed. |
| 4. Freshness | `fresh-check.mjs --bank coding-4`: 0 hits, exit 0; `--min-run 10` and `--min-share 0`: 0 hits, no advisory. By hand: `at-recursion` style nested lists appear in `algo-think` (`homework-2` `h-flatten`, `l5` nested folders), but no task weights by depth; `ci-live-median` is a running median, not windows of three; `ci-hold-limit` is a knapsack. No task repeated. |
| 5. Voice | `voice-scan.py 35 --summary` on the bank folder: 0 and 0. |

Counts: D2 1, D3 7, D4 4 (4 with `requires`); 6 code, 3 numeric, 3 choice; families as section 3 (`pf-idioms`, `pf-classes`, `at-search`, `ds-arrays`, `ds-pointers`, `ds-trees`, `gd-dp`, `gd-traversal`, `edge-case-list`, `simulation-rules`, `bit-lowest`, `defined-vs-undefined`, one each). Session totals as above.

### Each code task: tests, twin and near-misses

| Item | Twin | Near-misses run, and the first test each fails |
| --- | --- | --- |
| pf-idioms-count-above-mean | the mean as a `Fraction` | at or above the mean (3): `[4, 4, 4]`; no guard: `[]` |
| ds-arrays-local-peaks | window maximum is the middle and occurs once | at least (`[1, 3, 4]`): the brief's list; ends included: same, and `[9, 1, 9]` |
| ds-pointers-median-of-three | each window sorted | middle element (`[1, 4, 2]`); one window short: `[5, 1, 4, 2, 8]`, `[1, 2, 3]` |
| simulation-rules-settle-day | list of business days ahead, indexed | add the lag then skip (8): `(4, 2, {7})`; skip weekends then add the holiday count: `(4, 1, {5})`, a holiday on a Saturday |
| at-search-smallest-n | `math.isqrt` then adjust | float square root: one row short at 999,999,998,765,257,142 (it is right at $10^{18}$ itself); counting up: right on the 7 small tests, past 5 s at $10^{18}$ |
| gd-dp-dice-total-ways | inclusion-exclusion, and every face tuple for up to 4 dice | plain recursion: right on the 7 small tests, past 5 s on 40 dice to 140 |

Edge cases: empty and one-element lists, ties and plateaus, negatives, a trade on a weekend, a holiday week, lag 0, a 100,000-long list for each list task, $10^{18}$, and 40 dice (a 31-digit count, exact in Python).

### Reading items

Each runs its own lines: `pf-classes-shared-class-list` prints 2 (a class with a list per object gives 1; appending to a copy gives 0); `ds-trees-heap-trace` prints 6, also worked by hand with `sorted`; `bit-lowest-and-count` prints 7 (bit index 2 gives 5, highest bit 32 gives 35); `edge-case-list-median-test` runs `median` on each option against `statistics.median`; `gd-traversal-depth-first-order` runs the search, a breadth-first queue and a stack of pushes (the three orders of the key and two distractors); `defined-vs-undefined-wraparound` is checked by constant evaluation: `0u - 1 == 4294967295u` compiles, and `constexpr int y = INT_MAX + 1;` is rejected.

### Differences from section 5

Answers that differ from the brief: **0 keys; 1 trap value restated; 1 task renamed.**

- `at-search-smallest-n`: the function is `rows_needed(target)`, set as rows of a coin triangle, because `smallest_n` is already a function name in `counting-chance/homework-3` and `analysis/l6-epsilon-and-n` (other tasks). The float trap is right at $10^{18}$ itself, so a hidden test at $T(1{,}414{,}213{,}561) + 1$ catches it; a test with a negative target was added.
- `simulation-rules-settle-day`: the brief's trap "`trade_day + lag` then skipping forward gives 8 for the first" does not follow: it gives 7 on `(3, 2, set())`, which is right. It gives 8 on `(4, 2, {7})` (key 9), which the explanation now states.
- `pf-classes-shared-class-list`: the brief's slip 0 has no slip named; it is "appended to a copy".
- No item swapped; no family changed.
