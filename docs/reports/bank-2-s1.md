# Bank part 2, session 1 (author A): partial hand-in

Brief: `docs/briefs/bank-2.md`. Written: `app/content/bank/statistics-1.json` (15), `finance-1.json` (15), `behavioural-5.json` (8), 38 items. Not written: `coding-1.json` (12), which waits for engine requirement B2-E1. Number script: `docs/reports/bank-2-s1-numbers.py` (standard library only, runs under plain `python3`).

## Acceptance (section 7)

| Step | Result |
| --- | --- |
| 1. Validator | `0 errors, 4664 warnings` (the baseline before this session); 0 warnings name the three files. |
| 2. Numbers | `python3 docs/reports/bank-2-s1-numbers.py`: `704 checks, 0 failed`, exit 0. A planted wrong key and a planted wrong slip each fail it. |
| 3. Playthrough | `--bank statistics-1 --bank finance-1 --bank behavioural-5 --local-cdn <pkgs>`: `bank total: 38 of 38 items passed in 3 files`, `All passed.` The same with `--mobile`: 38 of 38, `All passed.` (`--mobile` changes nothing for `--bank` until B2-E3.) `--routes-only` with and without `--mobile`: `All passed.`, `#bank 141 drawable of 238 in 23 files (97 locked)`. |
| 4. Freshness | `fresh-check.mjs --bank <file>`: 0 hits, exit 0, for each file. `--min-run 10`: 0 hits each. `--min-run 10 --min-share 0`: 3 hits on `finance-1`, all rewritten (below); now 0 on all three. |
| 5. Voice | `voice-scan.py 35 --summary` on the bank folder: explanations over three sentences 0, sentences over 35 words 0. (One 36-word file `description` in `behavioural-5` was cut.) The validator's 20-word advisory `[O2-long-sentence]` is also silent on the three files. |
| 6. Wrong answers route | In a real page, every key and every `wrong` value was typed into the engine's `ZQ.grade.numGrade` (per cent items as the learner types them, "6.18%"), and each distractor checked against the choice rule: 90 cases, 28 keys right, 56 wrong ids each resolved to their own id and `byKey` line, 6 distractors each with a `why`. `ZQ.test.answerWrong()` cannot pick a named slip (inbox bullet). |
| 7. Counts | Below; they match sections 2, 3 and 5. |

### Freshness hits (`--min-run 10 --min-share 0`)

- `finance-1` `op-parity-price-the-put` against `options/homework-3` items[0] (run 13) and `exams/stage-1` (run 10): stock parity phrasing, different numbers and no dividend; rewritten anyway.
- `finance-1` `greek-signs-calendar-spread` against `opt-dash/l14-greek-profiles` quiz[2] (run 15): that item is a short straddle, not a calendar; the shared run was the question line plus the "Gamma negative, vega ..." option wording. Question rewritten and options reworded to "Negative gamma, positive vega, positive theta".

## Counts

| File | Items | D2 | D3 | D4 | D5 | numeric | choice | longform | with `requires` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| statistics-1 | 15 | 2 | 7 | 5 | 1 | 15 | 0 | 0 | 6 |
| finance-1 | 15 | 6 | 6 | 2 | 1 | 13 | 2 | 0 | 3 |
| behavioural-5 | 8 | 0 | 5 | 3 | 0 | 0 | 0 | 8 | 3 |

Families: one item for each of the 15 statistics families and 15 finance families of section 5; behavioural `star-story` 3, `why-us`, `reasoning-aloud`, `project-account`, `cv-lines`, `video-answer` 1 each. With `coding-1` (D2 4, D3 6, D4 2; 6 code, 5 numeric or choice, 1 choice) the session totals of section 2 follow: D2 12, D3 25, D4 11, D5 2.

## Each number and its two routes

Every check is an `ok(...)` or `two(...)` line in the script, in item order; `numeric()` asserts the key, its rounding as asked, every slip inside its own band, no band touching the key or another slip, and a `byKey` line per id; `stated()` asserts each printed figure.

| Item | Route A | Route B |
| --- | --- | --- |
| es-mle-waits-between-trades | Fraction 6/30 | grid search of the log-likelihood |
| es-biasvar-four-closes | Fraction 34/3 | pairwise-difference form; `statistics.variance` |
| es-intervals-halve-the-width | Fraction 64 (2.94/1.47)² | solve for s, then search n |
| es-bayes-seven-in-ten | Fraction 9/14 | midpoint integral of the Beta(9, 5) density |
| ht-pvalue-thirteen-of-sixteen | Fraction sum of binomials | enumeration of all 65,536 sequences; normal slip by `NormalDist` and `erfc` |
| power-one-sided-shift | `NormalDist` and `erf` | seeded simulation of 20,000 tests, tolerance 0.01 |
| multiple-testing-how-many-tests | floor(0.05/p) | count m up; p at z = 3.2 recomputed |
| two-regressions-two-slopes | Fraction r² = 1/4 | seeded 200,000-point sample with both slopes, tolerance 0.005 |
| rg-inference-t-from-r-squared | closed form | 102 constructed points with R² exactly 0.2, least squares t |
| rg-multiple-left-out-factor | Fraction 1.5 - 0.8 | seeded 200,000-point regression, tolerance 0.02 |
| ts-models-ar1-long-run-variance | Fraction 16/0.64 | sum of squared MA weights |
| ts-acf-ma1-first-lag | Fraction 12/25 | seeded 300,000-step series, tolerance 0.01 |
| sample-size-for-signal-sharpe-years | (2/0.7)² | bisection on 0.7√T = 2 |
| correlation-bounds-highest-third | closed form, top and floor | grid search on the 3 x 3 determinant (also the "highest" claim) |
| es-estimators-median-standard-error | 0.2√(π/2) and 1/(2f(0)√n) | seeded 20,000 medians of 100, tolerance 0.005 |
| fi-interest-monthly-to-annual | Fraction (201/200)¹² - 1 | month-by-month loop; continuous slip by `exp` and series |
| fi-bonds-duration-move | Fraction -7 x 25/10,000 | finite difference of a duration-7 price |
| fi-forwards-six-month-fair | 80e^0.025 | limit of fine compounding |
| fi-equity-growing-dividend | Fraction 3/0.05 | sum of 5,000 discounted dividends |
| op-parity-price-the-put | parity | Black-Scholes put at the call's implied vol |
| op-strategies-bull-spread-breakeven | Fraction | scan of the expiry payoff |
| op-greeks-second-order-estimate | Fraction | the quadratic summed in 2,000 steps (definitional estimate) |
| tp-riskneutral-one-step-with-rate | risk-neutral Fraction | replication with shares and a loan |
| tp-multistep-american-put-two-step | Fraction backward induction | every exercise policy valued by path enumeration |
| ms-book-sweep-four-hundred | Fraction level fill | share-by-share loop |
| ms-costs-effective-spread | Fraction | float |
| ms-orders-stop-through-a-gap | a toy matching rule | (definition; see `[verify]`) |
| greek-signs-calendar-spread | Black-Scholes closed-form Greeks | finite differences of the Black-Scholes price |
| gv-risk-one-day-var | Fraction with 2.326 | `NormalDist.inv_cdf(0.99)`, within the rounding of 2.326 |
| option-estimate-short-dated-call | Fraction 0.4 rule | Black-Scholes by `NormalDist` and by `erf` |

Behavioural: the script checks model length (146 to 172 words), rubric 2, 2, 2, 2, 1, 1, the `question` line, no `prose`, pace 120 where "two minutes" appears and 90 where "ninety seconds" appears, and distinct `question` lines.

## Differences from section 5

Answers that differ from the brief: **0 keys; 1 slip.**

- `rg-inference-t-from-r-squared`: the brief's slip "2.5 (used R²/(1 - R²) without the root)" does not follow: that route gives 0.25 x 100 = 25. The slip is `no-root` at 25 ("You gave t²"). The other slip, 4.5, is √20 = 4.47 at 1 decimal place.
- `greek-signs-calendar-spread`: the brief's distractors were "the patterns a long call, a short call and a long straddle give", but a long straddle has the long call's signs. The third distractor is the reversed calendar (positive gamma, negative vega, negative theta). Figures -0.0200, +19.77, +4.00 reproduced.
- Stored precision: where the unrounded key with the brief's half-unit band trips `[tight-band]` (more than d + 2 decimals), the key is stored to d + 2 places: `es-biasvar` 11.3333, `sample-size-for-signal` 8.163, `tp-riskneutral` 7.1429, `tp-multistep` 2.551, `fi-interest` 0.061678. Bands are the brief's.
- Tolerances: `rg-multiple-left-out-factor` 0.05 (half a unit of 1 decimal place) for the brief's 0.005; `ts-models-ar1-long-run-variance` 0 for a whole key.
- `fi-interest` and `fi-bonds` use `unit: "%"`, so the key is the fraction (0.061678, -0.0175) and the bands are 0.00004 and 0.00005.
- No item swapped; no family changed.

## The `[verify]` item

`ms-orders-stop-through-a-gap`: no lesson in `micro` mentions stop or stop-limit orders (`grep` of `content/courses` finds no "stop-limit"), so the lesson cannot confirm the wording. The item uses the standard definitions: a sell stop triggers on a trade at or below its price and becomes a market order; a stop-limit becomes a limit order at its limit. The prose names both orders and their prices, so the question stands on its own; it is D2 with no `requires`. A second reader should confirm it is fair as interview knowledge outside the courses.

## House style for sessions 2 to 4 (copy exactly)

- **`question` line of a spoken item:** `Answer aloud, then type it: <three to six words, lower case, ending in a full stop>.` Name the prompt, not the skill: "the risk that failed.", "the unpopular decision.", "a bet with unknown odds.".
- **Rubric time lines:** a time appears only where the prompt states one ("Questions in a stated order, short enough for two minutes", pace 120; "Under 250 words, which fits ninety seconds spoken", pace 90). Otherwise the last line is "Under 300 words, told in order, with no filler", which can be ticked from the text.
- **`feedback` of a spoken item:** `"correct": "Compare your answer with the model and tick the rubric."`, `"generic": "Open the model answer and mark each rubric line."` (part 1's lines).
- **Code `how` wording (for B2-E1, not yet written):** "Submit runs N hidden tests. Each result must equal the expected whole number." for an `equal` integer result, "... must equal the expected fraction exactly." for `compare: "fraction"`, and "... must equal the expected value." otherwise, with N the real test count (eight per task, inside rule 12's six to ten). Session 1 has no code item yet, so this is a proposal for the orchestrator to fix in "Changes after session 1".
- **Per cent keys:** `unit: "%"`, key as a fraction, `accept` leading with the per cent figure ("6.17%: ..."), `placeholder: "a percentage"`.
- **Choice options of Greek signs:** "Negative gamma, positive vega, positive theta" word order; "Gamma negative, ..." matches `opt-dash`.

## Open questions

- `coding-1.json` waits for B2-E1 to B2-E5.
- `[bank-family]` (B2-E5) is not built; the families were checked by hand against section 3.
- `numbers_lib.Bank` (B2-E4) is not built; the script reads the JSON itself.
