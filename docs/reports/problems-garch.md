# Problem sets: garch levels 1 to 3 (brief `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/garch/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-garch-numbers.py` (exits 0). Scratch generators: `<scratchpad>/author-garch/gen<n>.py`.

## Level 1 (Clustering: l1 to l4)

| item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|
| p-stale-alarm (re-authored in the fix pass) | 4 (4 / 0) | l1, l3 (and l4's annualising) | 4 |
| p-stale-prices-scaling | 4 (4 / 0) | l2, l4 | 4 |
| p-eight-day-window | 4 (4 / 0) | l4, l3 | 3 |
| p-big-day-indicator | 4 (4 / 0) | l1, l2 | 5 |

16 parts, all typed. Every lesson appears, every problem draws on two or more. Skills: `gv-clustering`, plus `gv-forecast` where l4 is drawn on.

Chains: P1 the alarm level from an annualised calm screen, then the chance a storm day crosses it, then that chance against the normal 0.27%, then the raw kurtosis of storm days in screen sds. P2 band, then the weekly variance of a sum with lag-1 covariances, then the annual one, then the ratio to the $\sqrt{252}$ figure. P3 mean square, then the sample sd from it, then annualised, then excess kurtosis with $\tfrac78 s^2$. P4 conditional chance, then the indicator's lag-1 autocorrelation, then $LM = (n-1)R^2$, then the smallest count of 75 that rejects.

### Gates (level 1)

- Validator: 0 errors; no warning on `problems-1.json`.
- Voice scan 35 on the course folder: 0 and 0.
- Number script: exit 0 (250 direct checks, 103 numbers_lib checks for level 1).
- `fresh-check --file`: 0 hits after one fix (a `retold` error: the byKey line "Excess kurtosis subtracts the normal's 3." matched the l3 quiz and review wording; reworded in P1 and P3).
- `grade-all --file`: 0 failures (16 numeric widgets).
- Playthrough `--problems garch/problems-1 --local-cdn <pkgs>`: green with `--why` (40 typed slips routed) and with `--mobile`. Part shots at 440 px read: no overflow.

### Closest course material, and why each problem is not a walk through it (level 1)

- **p-stale-alarm** (replaces p-two-regime-tails, ruled re-author). Closest: lesson l1 screen 7 (rolling vol annualised), screen 11 (a 250-day sd that lags a storm, position sizing); l3 screen 0, screen 9 and review-1 item 6 (days beyond 3 sds against the normal's 0.0027); l3 screen 10 (scaling leaves kurtosis alone); review-1 item 7 (clustering and the kurtosis of the shocks); homework-1 item 3 (tail counts); exam `e-mixed-window`. No screen holds a calm sd fixed into a storm and asks how often its 3-sd line is crossed; the l1 screen 11 story sizes positions, this one counts alarms. No mixture, no regime chain, no spell length, no share of days, no big-day-after-big-day table. Verdict: clean.
- **p-stale-prices-scaling.** Closest: l4 screen 10 (order the $\sqrt{252}$ derivation, covariances dropped), l4 screen 8 (annualise 1% daily), l2 quiz 0 (band for 1,000 days). The lesson drops the covariance terms; this problem keeps one lag and counts neighbouring pairs (8 for a week, 502 for a year), a calculation no screen makes. Its setting (thin trading, positive lag-1 ACF) is new to the course. Verdict: clean.
- **p-eight-day-window.** Closest: l4 screen 3 (zero-mean against sample sd on B's 5 days, a table read), l3 screen 2 (kurtosis of eight returns $0, \pm 2$), review-1 item 2 and l3 quiz 0 (kurtosis of 10 and 4 symmetric values). Here the data are eight uneven returns with a non-zero mean; the sample sd is built from the mean square of part 1 through $\tfrac{n}{n-1}(\overline{r^2} - \bar r^2)$, which no screen uses, and the kurtosis divides by $\tfrac78 s^2$. Verdict: clean.
- **p-big-day-indicator.** Closest: l1 screen 4 (table of next-day shares after big moves in B, 27.8% against 4.5%), l2 screen 7 and quiz 2 (ARCH-LM, $LM = (n - q)R^2$), review-1 item 5 (LM with 10 lags). Part 1 is a conditional share from counts, which l1 reads off a table; parts 2 to 4 turn it into an indicator autocorrelation, an LM statistic and an inverted threshold count, a chain no screen follows. Verdict: clean.

Fix pass grep for p-stale-alarm (course folder and exams): 14.5, 2.74, 19.2, 71.1, 0.9134, 2.299, 83.82 and the nouns cocoa, crop, alarm: hits only inside canvas data arrays (71.11, 92.74) and one exam of another course ("alarm", topic-2.1). Original grep (course folder, lessons, reviews and homework): 15.36, 4.54, 2.93% weekly, 21.20, 22.38, 28.33, 59.96 and the nouns Quiet, Turbulent, copper, crude, stale: 0 hits. 0.99, 0.96, 0.936, 1.673, 1.785 and 1,500 appear only inside canvas data arrays or as other quantities (a 99% VaR, day 1,500 of a crash): different roles.

## Level 2 (Models: l5 to l8)

| item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|
| p-two-filters-one-score | 4 (4 / 0) | l5, l7 | 4 |
| p-weekly-gas-arch | 5 (5 / 0) | l6, l8 (and l4's annualising) | 4 |
| p-silver-moment-fit | 4 (4 / 0) | l7, l8 | 5 |
| p-crash-then-quiet | 4 (4 / 0) | l5, l6 | 4 |

17 parts, all typed. Every lesson appears twice. Skills: `gv-models`, plus `gv-forecast` where l8's long run is drawn on.

Chains: P1 EWMA day 2, EWMA day 3 from it, GARCH day 3 from the same start, then day 3's log-likelihood difference from parts 2 and 3. P2 ARCH unconditional weekly variance, annualised with 52, the expected variance two weeks after a 12% fall, a GARCH $\omega$ that keeps the same level, then that GARCH's next-week variance. P3 persistence from the ratio of two squared-return ACF values, its half-life, the targeted $\omega$, then tomorrow's volatility. P4 EWMA after a fall, ARCH against it, EWMA after a quiet day, then the count of quiet days until the EWMA drops below ARCH's quiet-day level.

Every variance part has a `decimal` slip (the value over $10^4$), as the lessons do, which also clears the validator's `[percent-form]` advisory on "in %²" questions.

### Gates (level 2)

- Validator: 0 errors; no warning on `problems-2.json` (a first draft drew `[percent-form]`, `[wrong-band]`, `[shown-arithmetic]` and `[O2-explain-answer]` advisories; all fixed).
- Voice scan 35: 0 and 0.
- Number script: exit 0 (levels 1 and 2: 540 direct checks; 107 numbers_lib checks for level 2).
- `fresh-check --file`: 0 hits.
- `grade-all --file`: 0 failures (17 numeric widgets).
- Playthrough `--problems garch/problems-2`: green with `--why` and with `--mobile`. Part shots at 440 px read: no overflow.

### Closest course material, and why each problem is not a walk through it (level 2)

- **p-two-filters-one-score.** Closest: l5 screen 3 (EWMA five days by hand, $\lambda = 0.94$), l7 screen 3 (B's GARCH five storm days by hand), l7 screen 4 and review-2 item 6 (one day's log-likelihood score). The lessons run one model each and score a day under one variance; here two models run from one start and the same day is scored under both, with the difference split into its log and surprise terms. A first-draft explain line ("It moves 8% of the gap") paraphrased l5's "moves 6% of the way" and review-2 item 0; rewritten. Verdict: clean.
- **p-weekly-gas-arch.** Closest: l6 screen 3 and quiz 0 (ARCH unconditional variance), l6 screen 11 (ARCH variance after a 9% earnings fall), l8 screen 2 (annualise $V_L$ with 252). Weekly data annualised with 52, the expected variance two steps out, and a GARCH matched to ARCH's level by solving for $\omega$ are steps no screen takes. A first-draft explain ("At the level ... repeats itself") echoed l6 screen 3's "At the level nothing changes"; rewritten from stationarity. Verdict: clean.
- **p-silver-moment-fit.** Closest: l8 screen 8 (variance targeting in code, B's 1.0585), l7 screen 11 and quiz 2 and l8 quiz 3 (half-life from a given persistence), l7 screen 2 (GARCH in $r^2$ is an ARMA(1,1)). Estimating the persistence from the ratio of two squared-return ACF values, a moment fit, is new to the course; the targeting step is done by hand rather than by optimiser. Verdict: clean.
- **p-crash-then-quiet.** Closest: l5 screen 10 (EWMA the day after an 8% fall, margin desk), l6 screen 11 (ARCH after a 9% fall), l5 screen 8 (edge cases of $\lambda$). The comparison of the two models on one fall, the EWMA decaying towards a quiet day's square, and the count of days until it crosses ARCH's quiet level are new. Verdict: clean.

Own-course grep: 1.8248, 1.6988, 1.6537, 1.7735, 9.23, 21.91, 25.74, 0.7385, 25.40, 16.98, 0.1156, 4.4524, 2.9495, 2.8145, 0.9125 and the nouns shipping, natural gas, silver, broker: 0 hits in lessons, reviews or homework. 0.92, 1.44, 2.89 and 0.45 appear only as other quantities (a fitted $\hat\beta = 0.9235$, 11.44%, a forecast 1.4464%, a slider value).

## Level 3 (Using forecasts: l9 to l12)

Authored in a second session after a container restart stopped the first agent; levels 1 and 2 were not replayed. Generator: `<scratchpad>/author-garch/gen3.py`.

| item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|
| p-forecasts-to-parameters | 4 (4 / 0) | l9, l10 | 5 |
| p-bank-index-flat-var | 4 (4 / 0) | l12, l10 (and l7's one-step recursion) | 4 |
| p-recalibrate-short-var | 4 (4 / 0) | l11, l10 | 5 |
| p-monthly-sleeve (re-authored in the fix pass) | 4 (4 / 0) | l9, l12 | 5 |

16 parts, all typed. l9 and l12 appear twice, l10 three times, l11 once. Skills: `gv-forecast` (l9, l12) and `gv-risk` (l10, l11, l12), as `course.json` gives them.

Chains: P1 persistence from the ratio of two forecast changes, $V_L$ from the first change and $1 - \phi$, the day-30 vol, then the VaR the model expects to report that day. P2 tomorrow's GARCH vol, the target weight, the fund's VaR (equal to $z \times 11\%/\sqrt{252}$ of capital whatever the forecast), then the VaR on a calm night where the cap binds. P3 Kupiec at $p = 0.025$, the constant factor $c$ that turns the observed breach rate into the 1.96 quantile, the recalibrated VaR, then the recalibrated 97.5% ES. P4 the month's variance as a geometric sum of daily forecasts, the monthly weight from it, the second month's variance by the monthly factor $\phi^{21}$, then the index bought over three monthly resets (a telescoping sum).

### Gates (level 3)

- Validator: 0 errors; no warning on `problems-3.json` (first drafts drew `[O2-explain-answer]`, `[wrong-band]` on a `decimal` slip and two `[O2-long-sentence]` advisories; all fixed).
- Voice scan 35 on the course folder: 0 and 0.
- Number script: exit 0 (levels 1 to 3: 802 direct checks; 120 numbers_lib checks for level 3). Method 2 per part: a linear solve for $\phi$ and $V_L$, the variance recursion stepped forward, `binom.logpmf` for Kupiec, `brentq` for $c$, the normal tail integrated for ES, a brute day search, and the daily weight changes summed.
- `fresh-check --file`: 0 hits. One `retold` error on a first draft (P1 part 3 byKey "The forecast is the long run plus what is left of the gap." matched l9 screen 2) and one `rate` error (1.7550% against problems-2's 0.0175 with 0.92) were fixed by rewording and by new GARCH parameters. Three advisories remain: $z = 2.3263$ with 99 (the standard quantile, as l10 screen 2) and the h-step formula of l9 screen 2, stated as taught.
- `grade-all --file`: 0 failures (16 numeric widgets).
- Playthrough `--problems garch/problems-3`: green with `--why` and with `--mobile`. Part shots at 440 px read: no overflow.

### Closest course material, and why each problem is not a walk through it (level 3)

- **p-forecasts-to-parameters.** Closest: l9 screen 2 and review-3 item 0 (an h-step forecast from a given $V_L$ and $\phi$), l10 screen 2 and homework-3 item 1 (a VaR from a given vol), and problems-2 P3 (persistence from a ratio of two ACF values). Every course screen is handed the parameters; here they are hidden and backed out from three printed forecasts, a step no screen takes. Problems-2 P3 also infers $\phi$ from a ratio, but of squared-return ACF values, then goes to a half-life and $\omega$; this chain goes to $V_L$, a far forecast and a forecast VaR. A first draft repeated l9's sentence on the forecast's form; rewritten. Verdict: clean.
- **p-bank-index-flat-var.** Closest: l12 screen 2 and review-3 item 3 (weight from a daily forecast with a cap), homework-3 item 6 (cap binds, fund vol $1.5 \times 6\%$), l10 screen 1 (VaR in proportion to the forecast), l7 screen 2 (one GARCH step). No screen takes the VaR of a volatility-targeted position; the result that it does not depend on the forecast until the cap binds is new. Target and cap (11%, 1.25) differ from l12 (10%, 2), review-3 (8%, 2) and homework-3 (12%, 1.5); a first draft used share B's own $\omega, \alpha, \beta$ and was refitted. Verdict: clean.
- **p-recalibrate-short-var.** Closest: l11 screen 4 (Kupiec for 41 in 2,520 at 1%), homework-3 item 4 (Kupiec for 9 in 250), review-3 item 6, l10 screen 7 (99% ES), l10 screen 9 (a short's tail). Part 1 is the l11 task at a new rate (2.5%) with its own wording (a first draft echoed homework-3 item 4's "The log-likelihoods are ... at ... and ... at ..." and l11 screen 0's "expected ... and counted"; both rewritten). Parts 2 to 4, inverting the breach rate into a scale factor and recalibrating VaR and ES at 97.5%, are steps no screen takes. Verdict: clean.
- **p-index-fund-back-in** (ruled re-author in the second read; replaced by p-monthly-sleeve, below). Closest: l9 screen 2 and review-3 item 0 (h-step forecast), l12 screen 4 and review-3 item 8 (turnover from listed weights), l12 screen 1 (the forecast below which a cap binds), problems-2 P4 and review-3 item 9 (days until a decaying quantity crosses a level, half-life). Here the weights follow the forecast curve, the units bought telescope to one difference, and the crossing day is where the forecast-sized weight meets its cap; no screen links the term structure to sizing. Persistence 0.977 replaced a draft's 0.978, the mean of l7's 20 fits. Verdict: clean.

- **p-monthly-sleeve** (replaces p-index-fund-back-in). Closest: l9 screen 4 and quiz 1 (a horizon vol from a table of daily variances), l9 screen 6 and screen 11 (250 and 63 summed forecasts, by code), l9 screen 2, quiz 0, review-3 item 0 and exam `e-vol-ahead` (one h-step forecast); l12 screen 2, quiz 0 and review-3 item 3 (a weight from tomorrow's forecast with a cap); l12 screen 4 and review-3 item 8 (turnover and its cost). Here the 21 forecasts are summed in closed form, the weight is set once a month from that sum against a monthly target, the month-to-month persistence is $\phi^{21}$, and the weight's rise over three resets telescopes (the one step the review let stand). No cap, no turnover cost, no crossing day, no single h-step vol, no 4.0 %² start and no horizon of 20. Verdict: clean.

Fix pass grep for p-monthly-sleeve (course folder and exams): 0.81, 0.965, 2.56, 43.35, 29.47, 0.3946, 0.189, 26.34, 17.01 and the nouns pension, airline, sleeve: hits only inside canvas data arrays, l1's "2.56 times" (a ratio of block sds) and l9's day-1,999 0.965% (another role). `fresh-check` advisory: exam `e-breach-days` shares 21, 1.75 and 42 (its table's days and a return), a coincidence.

Own-course grep (lessons, reviews, homework, sets 1 and 2): 0.66298, 0.7172, 0.5144, 133,474, 3.0675, 1.7514, 0.3956, 209,367, 4.168, 76,945, 91,770, 2.3376, 0.4410, 1.6731, 2.7994, 0.0861, 0.977, 0.04101 and the nouns dollar-yen, water utility, bank index, mid-cap: 0 hits. 1.1379 and 139 appear only in canvas data arrays.

## Fix pass (session AF, after `docs/reviews/review-problems-garch-1-3.md`)

Two problems re-authored (p-two-regime-tails as p-stale-alarm, p-index-fund-back-in as p-monthly-sleeve); the reader's 25 other findings applied as written, with one sentence split for the voice rule (finding 22). Keys changed: problems-1 P3 part 3 (0.28336, tol 0.00011); problems-2 P1 part 3 (1.65365), P3 part 4 (0.022687), P4 parts 3 and 4 (2.81, 27); problems-3 P2 part 4 (218090.63), P3 parts 3 and 4 (tol 5). Line by line in the review's `## Fix pass`.

Gates: validator 0 errors, no warning on the three files; voice scan 35 on the course folder 0 and 0; `problems-garch-numbers.py` exit 0 (835 direct, 419 numbers_lib); `problems-garch-numbers-read.py` exit 0 (556 checks, 0 FINDING lines; its checks of the two replaced problems removed); `fresh-check --file` 0 hits on all three sets (4 advisories on problems-3); `grade-all --file` 0 failures (16, 17, 16 widgets); playthrough `--problems garch/problems-<n>` green on all three with and without `--mobile`; 440 px part shots of the two new problems read, no overflow.
