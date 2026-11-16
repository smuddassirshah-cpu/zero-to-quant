# Delta read AF, arma problem sets 1 to 3: the re-authored problems and the parts the fix pass changed

Counts: `wrong` 0, `misleading` 0, `reuse` 2, `re-author` 0, `continuity` 1, `voice` 0, `other` 1. No key, `wrong` value or band is mistaken. Three numbered findings, all small, each with tested text; finding 1 counts once under `reuse` and once under `continuity`. The three hardest checks of the brief hold: the `p-airport-anomaly` statistics agree with each other, and the renumbered `p-etf-flows` and `p-inflation-arma` are consistent from stem to last part.

Scope, from `docs/reviews/review-problems-arma-1-3.md` and its `## Fix pass`, and a JSON-path diff of the three sets between `e9cc28a5` (before the pass) and `4746c6a7`:

- re-authored: `problems-2` `p-trust-discount`, `p-satellite-stocks`; `problems-3` `p-swap-spread-hold` (whole items);
- renumbered: `p-airport-anomaly` (prose, parts 1 to 5), `p-etf-flows` (prose, parts 1 to 4), `p-inflation-arma` (prose, parts 2 to 4), `p-dual-listing` (parts 1, 3, 4, 5);
- lines only: `p-ppp-screen` part 5, `p-gdp-trend` part 1, `p-gold-drift` part 1, `p-peg-fridays` parts 1 to 3, `p-smoothed-fund` part 2.

The diff shows no change outside those paths, and nothing at the top level of any set. Mock exams: none carries a `ts-` skill or a time-series item (grep for AR(1), ARMA, half-life, autocorrelation, Dickey, Ljung), so the exams in scope are `topic-2.2.json` and `stage-2.json`.

Method. Each part in scope was solved from its text before its key was read, then again in `docs/reports/delta-review-delta-af-arma-numbers.py`, which imports no earlier script. Routes: damped sums of squared weights for each AR(1) variance; a seeded Dickey-Fuller regression on 365 days (400 paths) for the size of the airport $t$; the variance of a day's change for the airport residual variance; Durbin-Levinson for the four regression rows of `p-trust-discount`; a fixed-point recursion for its mean; a seeded simulation of 400,000 weeks for the satellite ACF; the model run forward with future shocks at 0 for the inflation forecasts, and brute search for its horizon; statsmodels psi weights for both ARMA(1, 1) problems; a day-by-day product and a sum of 20 shock variances for the swap spread; the loss chance at every hold from 1 to 1,999 days for "never below". Bands: every key takes each typed form of the stated places, refuses each `wrong` value, and no two bands of a part meet. No browser; no content or engine file edited.

## Tool results

| check | result |
|---|---|
| author's script `problems-arma-numbers.py` | 605 checks, 0 failures, exit 0 |
| first reader's script `problems-arma-numbers-read.py` | 473 checks, 0 failing, exit 0 |
| `delta-review-delta-af-arma-numbers.py` | 417 checks, exit 0, 4 FINDING lines (two for finding 1, one each for findings 2 and 3); 0 FINDING lines once the fixes are in |
| validator | 0 errors, 4589 warnings; three on the sets, all recorded by the fix pass (`[key-length]` on `p-ppp-screen` part 5, `[O2-long-sentence]` twice on `p-dual-listing`); `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check --file`, three sets | 0 hits; 4, 1 and 7 advisories, read (stock constants, the ARMA(1, 1) equation, 0.05 and 0.08 against l7 screens[10]) |
| `grade-all --file`, three sets | 0 failures (18, 16, 17 widgets) |
| trial copy with the three fixes below | my script 0 FINDING lines; `fresh-check` 0 hits on sets 2 and 3 (0 and 7 advisories, none new); `grade-all` 0 failures; voice 0 and 0; validator 0 errors, the same three warnings; content restored with `git checkout` |

## Verdict per item

| item | numbers | closest items | reuse verdict |
|---|---|---|---|
| `p-trust-discount` | clean; one row inconsistent (finding 1) | l8 screens[1] (regress on the last $k$ days, newest coefficient; series B rows), screens[4] ("What AR order does the PACF point to?", PACF 0.609, 0.25, 0.043, −0.075), screens[7] (stray bar); l7 quiz[0] and review-2 items[4] ($c/(1 - \phi)$); review-2 items[5] (forecast from `const`); homework-2 items[3]; topic-2.2 items[8]; stage-2 parts[1].items[4] | part 1 `reuse`, number level (finding 1). Parts 2 to 4 `clean`: no item takes an AR(2) mean, a two-lag forecast or the gap between two fits' forecasts. |
| `p-satellite-stocks` | clean | l5 screens[11] (bid-ask bounce on a walk); l7 screens[9] ($\rho_k = \phi^k$); l9 quiz[3] (booked P&L with a booking error); homework-2 items[1]; topic-2.2 items[5]; stage-2 parts[1].items[1] | `clean` chain: no item adds white error to a stationary series or takes $\phi$ from a ratio of lags. One slip line `reuse` (finding 2). |
| `p-swap-spread-hold` | clean; one printed tail off the key's rounding (finding 3) | l12 screens[2], [4], quiz[2] (half-life, days to a fraction), screens[11] (half-lives of 4, 13 and 110 days against a 20-day funding limit); l11 screens[6], [11]; l7 screens[11]; review-3 items[4], [6]; homework-3 items[7]; topic-2.2 items[15], [16] | `clean`. The 12-day half-life against a 20-day hold is near l12 screens[11]'s 13 days against 20, but that screen sorts spreads and computes nothing. No slip line of l12 or l11 is retold: "That is a straight line from 9 bp down to 0 over 24 days" against "You took 20% of the starting gap off each day. The decay is geometric". No $\phi = 0.915$, no sd 2.4. |
| `p-airport-anomaly` | clean | as the second read | `clean`; finding 3's line replaced as written |
| `p-etf-flows` | clean | stage-2 parts[1].items[4] (0.45, 0.2025, 0.7975) | `clean`: none of 0.45, 0.2025, 0.7975 is left; 0.44, 0.1936, 51.06, 725.76, 26.94 are in no item |
| `p-inflation-arma` | clean | stage-2 parts[1].items[5] ($0.35\varepsilon_{t-1}$) | `clean`: no 0.35 left; 0.472, 0.222, 0.4320, 0.1820 are in no item |
| `p-dual-listing` | clean | homework-3 items[2]; l10 screens[2]; `p-peg-fridays` ($0.88^5$) | `clean`: part 3 is at 7 days, neither $0.88^5$ nor 0.5277 is left, the three part 1 lines are the review's |
| line fixes (`p-ppp-screen`, `p-gdp-trend`, `p-gold-drift`, `p-peg-fridays`, `p-smoothed-fund`) | clean | as the second read | `clean`: each line is the review's text, word for word |

## Findings

1. `reuse` and `continuity` | `arma/problems-2.json` | `p-trust-discount` | `items[1].prose`, `parts[0].widget.options[0].text`, `options[1].text`, `options[1].why`, `options[2].why`, `parts[0].explain.text`.
   Reuse. Part 1 is the task of l8 screens[1] and screens[4] on almost the lesson's numbers. The lesson regresses series B on its last $k$ days for $k = 1$ to 4 and reads the newest coefficients 0.615, 0.252, 0.041, −0.074 (screens[4]: "Its PACF is 0.609, 0.25, then 0.043, −0.075 ... What AR order does the PACF point to?", key 2, band ±0.088). The problem regresses on the last $k$ weeks for $k = 1$ to 4 and reads 0.80, 0.24, 0.05, −0.08 (key AR(2), band ±0.086). To two places the lesson's tail is 0.25, 0.04, −0.07; the problem's is 0.24, 0.05, −0.08, same signs, each 0.01 away. The trap is the problem's own, and so are parts 2 to 4, so the verdict is number-level reuse, not a re-author. `fresh-check` reads no canvas table and gave 0 hits.
   Continuity. The four-lag row cannot follow from the three-lag row. With a newest coefficient of −0.08, Durbin-Levinson gives week 2 as $0.21 + 0.08 \times 0.21 = 0.227$; the prose prints 0.20. The other six coefficients of the two rows agree to 0.005.
   Fix (one change cures both; parts 2 to 4 use only the one-lag and two-lag fits and are untouched). Rows rebuilt by Durbin-Levinson from 0.61 and 0.24 with PACF −0.06 at lag 3 and 0.07 at lag 4: three lags 0.6244, 0.2766, −0.06; four lags 0.6286, 0.2572, −0.1037, 0.07. The trap survives: −0.10 is outside ±0.086, and −0.06 and 0.07 are inside.
   - `prose`: "... Two lags give constant 1.38 and coefficients 0.61 and 0.24. Three lags give 0.62, 0.28 and −0.06. Four lags give 0.63, 0.26, −0.10 and 0.07. The PACF band for 520 weeks is ±0.086."
   - `options[0].text` (`two`): "AR(2): the newest coefficients run 0.80, 0.24, −0.06, 0.07, and only the first two clear the band"
   - `options[1].text` (`three`): "AR(3): in the four-lag fit, week 3's coefficient of −0.10 is outside the band"
   - `options[1].why`: "The PACF at lag 3 is the last coefficient of the three-lag fit, −0.06. A coefficient in the middle of a longer fit is not a partial autocorrelation."
   - `options[2].why` (`four`): "Its last coefficient, 0.07, is inside the band. Week 4 adds no new memory."
   - `explain.text`: "Reading the last coefficient of each fit gives the PACF: 0.80, 0.24, −0.06 and 0.07. Only the first two lie outside ±0.086. The proposal is the two-lag fit, an AR(2)."
   The minus signs are U+2212, as in the file. If the main session rules the likeness a standard task and keeps the numbers, the smaller fix is "0.20" to "0.23" in the prose alone. Left open either way: the two-lag coefficients 0.61 and 0.24 stand beside the lesson's PACF "0.609, 0.25" in another role; changing them would move three keys, and I do not ask for it.

2. `reuse` | `arma/problems-2.json` | `p-satellite-stocks` | `items[3].parts[1].feedback.byKey.no-error`.
   Set: "That is the true stock's $\phi$. The errors add variance but no covariance, so the estimates' value is lower." l9 quiz[3], `half` `why` (true P&L plus a booking error): "That would need the errors to be the whole P&L. The true P&L adds variance but no covariance." The same six words on the same idea, a series seen with error.
   Fix: "That is the true stock's $\phi$. The error lifts the variance to 48.25 and leaves the covariance at 30.6, so the estimates' value is lower."

3. `other` | `arma/problems-3.json` | `p-swap-spread-hold` | `items[2].parts[2].feedback.correct`, `parts[2].explain.text`, `parts[3].explain.text`.
   The key 0.139485 rounds to 0.139, and so does the value from the restated 2.83 and 5.69: $6.17/5.69 = 1.084$, tail 0.1391. The feedback prints "1.08 sds" and "$P(Z > 1.08) = 0.140$", the table value at the rounded $z$. The band (±0.0008) takes 0.139 and 0.140, so nobody is marked wrong; a learner who typed 0.139 from a calculator is told 0.140. The second read fixed the same pattern in `p-airport-anomaly` part 5 by printing the third place of $z$.
   Fix, `parts[2].feedback.correct`: "Correct. 9 bp is $(9 - 2.83)/5.69 = 1.084$ sds above the forecast, and $P(Z > 1.084) = 0.139$."
   Fix, `parts[2].explain.text`: "The loss line sits $6.17/5.69 = 1.084$ sds above the forecast. The upper tail beyond it is 0.139, about one trade in seven. Most of the gap is expected to close, but a day-20 sd of 5.69 bp leaves real risk."
   Fix, `parts[3].explain.text`: "Far ahead the forecast is the mean and the sd is the long-run 6 bp. A loss then needs the spread 9 bp above the mean, $9/6 = 1.5$ sds, with chance 0.067. A longer hold lowers the risk from 0.139 at 20 days, but never below 0.067."
   Band and `wrong` values stand ($P(Z > 1.08) = 0.1401$ stays inside the band for a table user).

## Verified with no finding

- `p-airport-anomaly`, the stem statistics. $S_{xy}/S_{xx} = -0.23$; $s^2/S_{xx} = \tfrac{1}{900}$, se $\tfrac{1}{30}$, $t = -6.90$. $S_{xx}/364 = 7.912$ against part 4's 7.8605, 0.7% apart. An AR(1) with $\phi = 0.77$ and variance 7.8605 has changes of variance $2 \times 7.8605 \times 0.23 = 3.616$, and the regression leaves $3.616 - 0.23^2 \times 7.8605 = 3.200$, the stated $s^2$ exactly. $\hat\gamma\sqrt{n}/\sqrt{1 - \hat\phi^2} = -6.88$. On 400 seeded samples of 365 days the regression's $t$ runs from −8.00 to −6.10 (5% to 95%, median −6.98), with −6.90 inside. `no-sqrt` −207.0, `s-not-s2` −9.2286, `sign` 6.9 rebuilt. Part 3 carries −6.90 in all six places and no −4.55. Part 5: 0.03726; the band takes 0.037 and 0.038, `shock-sd` takes 0.003, `no-square` takes 0.090; 14 days a year and about one day hold.
- `p-etf-flows`. $79{,}200/180{,}000 = 0.44$; $(0.44, 0.24)$ is a possible pair of autocorrelations and $\phi = 0.44$ is stationary. $Q(2) = 51.0564$, `box-pierce` 50.24, `no-n-k` 10148.48, $\chi^2_2$ point 5.99. $0.44^2 = 0.1936$, band 0.139, gap 0.0464 printed as 0.05. $\sigma = \sqrt{900 \times 0.8064} = 26.9399$, `no-square` 22.4499, `variance` 725.76, "about 10%" is 10.2%. Every later part uses the new 0.44.
- `p-inflation-arma`. $\phi = 0.82$ stationary, $\theta = -0.20$ invertible, no common factor. Shock 0.12; forecasts 0.472 and 0.43204 by recursion and by psi weights; `no-ma` 0.496, `theta-sign` 0.52, `ma-again` 0.40804, `from-xn` 0.45172. First horizon 9 by search (gaps 0.0553 and 0.0454), 10 for the AR(1) start, 7.51 and 0.225 as printed. The part is in "% a month" and asks a decimal, as before the pass; no "%" unit is set, and none was before.
- `p-dual-listing`. BIC gap 14.3799, AIC slip 19.0. Psi weights: day 1 1.13, day 7 0.524777, day 8 0.461803; $0.88^7 = 0.408676$. Half the shock at 7.3783 days, $5.42 + 1 + 0.96$; day 7 is above one half and day 8 below, as part 4 needs.
- `p-trust-discount`, parts 2 to 4. Mean 9.2 from both fits and as the recursion's fixed point; the one-lag slope 0.80 is the $\rho_1 = 0.61/0.76 = 0.803$ the two-lag fit implies. Forecast 11.94 two ways, `swap` 12.495, `no-constant` 10.56. Gap 0.50, `narrowing` 0.56, the two-lag narrowing 0.06, "nearly nine tenths" is 89%. Band $1.96/\sqrt{520} = 0.086$.
- `p-satellite-stocks`. 48.25; 0.634197; 0.389476 (0.389 also from the restated 0.634); cube root 0.86878, fourth root 0.899876, $0.40^{1/4} = 0.795271$. The simulation gives the variance, lags 1 and 4 and the ratio estimate within 0.01. The sample values 0.61 and 0.40 are within two standard errors of 0.634 and 0.389 on 520 weeks. Claim "the error scales every lag by the same $36/48.25$": true for white, independent error.
- `p-swap-spread-hold`. Gap 2.834822 by 20 daily steps of $\phi = 0.5^{1/12}$; sd 5.694589 from 20 damped shock variances; loss chance 0.139485; floor 0.066807. Each `wrong` value rebuilt, and each takes the value a learner gets from the restated 2.83 and 5.69. "Never below 0.067": the loss chance is $P\big(Z > 1.5\sqrt{(1 - a)/(1 + a)}\big)$ with $a = \phi^h$, which falls at every longer hold and tends to 0.0668.
- Chain: each later part of the three new problems restates the value it takes, and the last part is the result. Coverage as the author's report states (l8 by `p-trust-discount`, l12 by `p-dual-listing` and `p-swap-spread-hold`).
- Fix pass applied as written: findings 3, 4, 5, 6, 9, 10, 12, 15 and 16, each replacement compared with the review's text by JSON path. `p-peg-fridays` part 3: $17.73 \times (1 - 0.5277^2) = 12.79$, inside the band.
- Voice: nothing to report.

## Notes, not findings

- `p-trust-discount` and `p-satellite-stocks` both use 520 weeks, in one set. Different tasks; no number follows from it but the band.
- `p-etf-flows` part 3 prints the gap $0.24 - 0.1936 = 0.0464$ as "0.05 away". Correct to two places.

## Engine

1. `fresh-check.mjs` reads no canvas table: the regression rows of l8 screens[1] (`canvas.params.params.C2`) and the PACF run in screens[4]'s prose are not held against a set's stem (finding 1). A run of three numbers that match a lesson's run to within 0.01, in order and sign, could be an advisory.
2. No rule checks a table of nested-regression coefficients for consistency, nor any printed normal tail against the rounding of its own key (finding 3: key 0.139485, feedback 0.140). A validator candidate: a `feedback.correct` that prints the answer to the stated places should print `round(key)`.

Inbox bullets: `docs/BACKLOG-INBOX.md`, `Raised later (delta read AF arma):`.

## Fix pass

1. Fixed: `p-trust-discount` rows rebuilt as written (three lags 0.62, 0.28, −0.06; four lags 0.63, 0.26, −0.10, 0.07), options and explain updated. Recomputed by Durbin-Levinson: 0.6244, 0.2766, −0.06; 0.6286, 0.2572, −0.1037, 0.07. No key, band or `wrong` value moves (keys of parts 2 to 4 use only the one-lag and two-lag fits; part 1 key stays `two`).
2. Fixed: `p-satellite-stocks` `no-error` line now "The error lifts the variance to 48.25 and leaves the covariance at 30.6, so the estimates' value is lower."
3. Fixed: `p-swap-spread-hold` parts 3 and 4 print 1.084 and 0.139 (6.17/5.69 = 1.08436, tail 0.13910). Band and `wrong` values unchanged.

Scripts: `problems-arma-numbers.py` updated (newest PACF run, −0.10 clears the band, z 1.084 to 0.0005); it, the reader's script, the delta script (0 FINDING lines) and the five other arma scripts exit 0.

Gates: validator 0 errors; voice scan 35 0 and 0; `fresh-check` sets 2 and 3 0 hits (0 and 7 advisories, none new); `grade-all` sets 2 and 3 0 failures; playthrough sets 2 and 3 with and without `--mobile` all passed.
