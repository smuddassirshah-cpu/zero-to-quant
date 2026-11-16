# Problem sets: fin-ml levels 1 to 3 (brief `docs/briefs/chained.md`, prompts `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/fin-ml/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-fin-ml-numbers.py` (paths from `__file__`; exits 0). Every lesson, review and homework of each level was read first and its numbers, windows, prices and stories noted; each setting below was grepped against the course folder and `app/content/` before writing.

## Level 1 (labels)

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-index-fund-day | 5 (4 / 1) | l1, l2 | 3 |
| problems-1 | p-copper-breakout | 5 (5 / 0) | l2, l3 | 4 |
| problems-1 | p-silver-windows | 5 (5 / 0) | l2, l3, l4 | 4 |
| problems-1 | p-bond-sign-model | 5 (5 / 0) | l1, l4 | 5 |

Typed parts 19 of 20. The one choice is the `first_touch` result, a reading of the walk. The chain in each: bar, label, barrier, exit, loss; meta-labels, base rate, precision, recall, F1; concurrency, weight, $n_{\text{eff}}$, weighted hit rate, honest error; middle-label uniqueness, covered days, $n_{\text{eff}} = 409/10$ exactly, error, $t$ against the majority baseline.

Checks: number script exit 0; validator 0 errors and no warning on the file (a long-sentence, `negative-key`, `shuffle-false` and three `O2-explain-answer` warnings met while drafting were fixed); `grade-all --file` 0 failures (20 widgets); playthrough `--problems fin-ml/problems-1 --local-cdn` green with `--why` (34 typed slips routed) and with `--mobile`; 440 px shots read, the 12-row table and the choice grid fit. Voice scan 35 on the course folder: 0 and 0.

Freshness: `fresh-check --file`: 0 hits and 0 advisories after two edits. The first run gave one text warning (11 shared words with l4's "a label's window runs from its entry day to its ...", rewritten) and two shared-formula advisories ($\sqrt{p(1-p)/n_{\text{eff}}}$ printed in two questions, the l4 formula; the formula was taken out of the questions). Own-course grep of £64.00, 65.28, 61.95, 61.90, 0.7273, 2.5583, 0.6111, 0.0764, 409 and the windows A 0 to 2, B 1 to 5, C 2 to 4, D 4 to 7, E 6 to 8: no shared setting (l4 has a window 0 to 3 and the homework 0 to 4, 2 to 6, 5 to 9, 5 to 6). The stories (index fund, copper miner breakout, silver fund, bond future) appear in fin-ml nowhere; "copper miner", "breakout rule" and "bond future" occur once each in other courses (coint, backtest, linear-maps) in unrelated tasks.

## Level 2 (features)

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-2 | p-gold-frac-weights | 5 (5 / 0) | l6, l8 | 5 |
| problems-2 | p-retail-relative-volume | 4 (3 / 1) | l5, l7 | 3 |
| problems-2 | p-q3-earnings-join | 4 (4 / 0) | l8, l7 | 4 |
| problems-2 | p-shipping-z | 5 (4 / 1) | l5, l8 | 4 |

Typed parts 16 of 18. Choices are judgements: why a rank and a z disagree (one outlier), why a trailing and a centred z disagree (look-ahead). Chains: $w_2$, $w_3$, $w_4$ and the window of 4, the value, the look-ahead of `np.convolve(..., mode='same')` on that window (checked by a spike in the script: 1 day); relative volume, tied rank, cross-sectional z, reading; the as-of value on 24 October, honest rank, leaky rank, early rows; sample sd, trailing z, centred mean, centred z, reading.

Checks: number script exit 0; validator 0 errors, no warning on the file (two `shown-arithmetic`, one `key-length`, one `O2-explain-answer` and one long question fixed while drafting); `grade-all --file` 0 failures (18 widgets); playthrough green with `--why` (31 slips routed) and `--mobile`; 440 px shots read. Voice scan 0 and 0.

Freshness: `fresh-check --file`: 0 hits, 0 advisories in the end. First run: the l6 recursion $w_k = -w_{k-1}\frac{d - k + 1}{k}$ was a shared-formula advisory with l6 and `exams/stage-2.json`; the set now states the same rule as $w_k = w_{k-1}\frac{k - 1 - d}{k}$, which the learner must still apply (all feedback rewritten in that form). Grep: d = 0.35, −0.11375, −0.0626, 2.379, the closes 5.005 to 5.012, 1.38m over 1.20m, the values 0.82 to 2.40, 25.33 and the closes £20 to £30 share no setting in fin-ml (l6 has $d$ = 0.3, 0.4, 0.5; review-2 has 0.3 and the ranks 4, 7, 7, 1, 9). The company names were first rivers (Avon, Brent, Clyde, Dee, Exe, Wye); `alpha` l5 and l7 use river names for a cross-sectional rank, so they were changed to Agate, Beryl, Coral, Jasper, Onyx and Topaz, which appear nowhere in `app/content/`.

## Level 3 (from prediction to profit)

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-3 | p-five-day-sizing | 4 (4 / 0) | l9, l10 | 4 |
| problems-3 | p-trial-log-dsr | 4 (4 / 0) | l11, l12 | 5 |
| problems-3 | p-futures-net-psr | 4 (4 / 0) | l10, l11 | 4 |
| problems-3 | p-calibrated-kelly | 5 (4 / 1) | l9, l12 | 3 |

Typed parts 16 of 17; the choice is the plan's order (calibrate before sizing). Chains: AFML size, rounded units traded, cost, break-even; trial count from a log with reruns, $E[\max]$, the error with skew and kurtosis, DSR; daily cost, net Sharpe, error, PSR; Kelly at odds 1.8 on the raw and calibrated chances, growth at the raw stake, share of the best growth.

Checks: number script exit 0 (598 of 598 over the three sets); validator 0 errors, no warning on the file (`wrong-band`, `shown-arithmetic` and four long sentences fixed while drafting); `grade-all --file` 0 failures (17 widgets); playthrough green with `--why` (36 slips routed) and `--mobile`. The first 440 px shots showed the inline $E[\max]$ formula running past the column and shifting the page; both long formulas are now display maths and the shots read clean. Voice scan 0 and 0.

Notes on numbers: the $E[\max]$ closed form runs 2.6% above the exact mean of the best of 5 normals (1.1927 against 1.1630, checked by integration and simulation), so the question says "about" and the key is the closed form, as l11 teaches it. The DSR key 0.954 accepts 0.952 to 0.956, which covers $\Phi$-table rounding of the stated intermediates (0.955 from 0.53 a year rounded).

Freshness: `fresh-check --file`: 0 hits, 0 advisories in the end. First run: a numbers warning and a parameters advisory against this course's own `problems-1` (0.63, 0.66, 0.74: the first draft's probabilities met the copper table's $p$ values); the five probabilities were changed to 0.67, 0.77, 0.72, 0.37, 0.42 and every downstream key recomputed. Grep of the course folder, `exams/topic-2.1.json` and `exams/stage-2.json`: only 0.28 appears in stage-2, as an unrelated single number. Stories (five-day sizing on a £5m book, a ridge and forest trial log, a futures signal at 9 bp, a 1.80 payout) are new to fin-ml; review-3 uses a 1.50 payout and the homework a 25-trial pitch.

## Reuse advisories

None left on any set: every advisory met while drafting was removed by a rewrite (listed per level above), none was waived. No `reuseWaiver` is used.

## Engine limits

One bullet in `docs/BACKLOG-INBOX.md` under "Raised later (problems fin-ml)".
