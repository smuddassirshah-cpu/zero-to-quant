# Problem sets: regression (brief `docs/briefs/chained.md`)

Files: `app/content/courses/regression/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-regression-numbers.py` (exit 0, 1,109 checks, 0 failures). Commits: ef70780 (level 1), 9a0efce (level 2), b4564cb (levels 1 and 2: stored keys to 4 places), 30e8865 (level 3), then this report.

Read first: every screen and quiz of l1 to l12, review-1 to 3, homework-1 to 3 and `exams/topic-1.6.json`, for settings to avoid (market and stock returns, slippage and impact against order size, hedge ratios, bond spreads, pairs trades, momentum signals, the market maker of l9).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-gas-demand | 5 (5 / 0) | l1, l2, l3 | 3 |
| problems-1 | p-car-prices | 4 (4 / 0) | l2, l4 | 4 |
| problems-1 | p-smudged-shift | 5 (5 / 0) | l1, l2, l3, l4 | 5 |
| problems-1 | p-stopping-distances | 5 (4 / 1) | l1, l2, l3, l4 | 4 |
| problems-2 | p-sunny-cones | 4 (4 / 0) | l5, l6 | 3 |
| problems-2 | p-freight-summary | 4 (4 / 0) | l5, l6, l7 | 4 |
| problems-2 | p-raw-intercept | 4 (4 / 0) | l5, l6, l8 | 5 |
| problems-2 | p-grocer-beta | 5 (4 / 1) | l5, l6, l8 | 4 |
| problems-3 | p-power-price | 4 (4 / 0) | l9, l10 (and l2) | 4 |
| problems-3 | p-solar-output | 5 (5 / 0) | l9, l12 (and l7) | 5 |
| problems-3 | p-overlap-signal | 5 (4 / 1) | l11, l12 | 5 |
| problems-3 | p-bond-fund-weeks | 5 (4 / 1) | l9, l11 | 4 |

Typed parts: level 1 18 of 19, level 2 16 of 17, level 3 17 of 19. Each choice part is a judgement: what an arched residual plot says, whether a beta is below 1, whether an overlap-corrected $t$ is significant, which standard errors to report.

Chains. Level 1: $r, s_x, s_y$ to slope, intercept, a cold-day forecast, its residual and that residual in leftover sds; car ages to $S_{xx}$, slope, the slope's rise when the oldest car's price is corrected, and the corrected slope; a smudged record recovered from $\bar y = a + b\bar x$, then its residual, SSE and $R^2 = \tfrac{10}{11}$; Highway Code stopping distances to slope, intercept, a residual, $R^2 = 0.985$ and the curve verdict. Level 2: $s$, SE, $t = 1.6$, then $t = 3.2$ on four times the days; a spilt summary rebuilt from $R^2$ and $n$ ($F$, $t$, SE, interval); a raw-return intercept turned into alpha, its SE, $t$ and the 205 months needed; a beta's $s$, SE, $t$ against 1, interval and verdict. Level 3: omitted-variable slope to $\delta$, $r$, VIF and the 313 days that undo it; a two-slope solve, SSE, $s^2$ on 21 df and adjusted $R^2$; $s$, SE, naive $t = 3.5$, overlap-honest $t = 1.90$ and verdict; a two-factor prediction, its residual, Durbin-Watson, $\hat\rho$ and the HAC choice. Each later part restates the value it uses, and its `wrong` list holds the value the commonest slip in the part before gives (`carried`, or the named slip).

Judgement calls a reader may question: `p-sunny-cones` part 4 assumes the slope and $s$ repeat on 72 days, said in the question. `p-freight-summary` part 1 restates $F = \mathrm{ESS}/s^2$ (l7) so $F$ follows from $R^2$ and $n$; the $R^2$ form of $F$ is level 3. `p-overlap-signal` part 4 restates the overlap factor from homework-3 (h = 10, naive $t$ 3.2); here $h = 5$ and the naive $t$ is built from SSE and $(\mathbf X^T\mathbf X)^{-1}$, so the setting is new and only the taught tool is shared. `p-power-price` part 2 uses $b = r\,s_y/s_x$ from l2.

Form and units. Every numeric part names its form ("Give your answer to n decimal places." or "Give a whole number."). Parts with a natural unit carry `unit` (GWh, £, m, hours, cones, months, days, %, MWh); per cent keys are fractions. Where a part restates a rounded value the key is what that value gives and the band takes the exact route too (SE $0.85/3.16$ and $0.85/\sqrt{10}$; interval from 0.269 and from statsmodels' exact SE; honest $t$ via 1.84, 1.844 and exact; $\hat\rho$ from 0.22). The script checks those.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (1,109 checks in all) |
| validator | 0 errors; no warning on the file | same | same |
| playthrough `--local-cdn` | green (19 parts) | green (17 parts) | green (19 parts) |
| playthrough `--mobile` | green; 440 px shots read, no layout fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

Method 2 in the script: NumPy fits on the raw data; statsmodels OLS on synthetic data built to have each problem's exact summary figures (means, sds, $r$, SSE, $S_{xx}$, the centred moment matrix); SciPy $t$ quantiles; statsmodels VIF and Durbin-Watson; a fixed-seed simulation of overlapping 5-day sums (sd of the naive $t$ within 0.15 of $\sqrt{3.4}$).

## Fresh-check

At the gate: 0 hits on all three sets. Advisories: $S_{xx} = 40$ (l3, other sums), $\mathrm{SSE}/(n-2)$, $F = \mathrm{ESS}/s^2$, $(e_t - e_{t-1})^2$ and the overlap factor (l5, l7, l11, l12, homework-3: taught formulas); 23, 53, 73 with `mock-oa-trader-3` (a number sequence); 0.975, 48, 95 with homework-2 `Judging a manager` (stock levels; 48 is my degrees of freedom, not months); 42, 0.85, 95 with `topic-2.2` (a GARCH VaR item). At `--min-run 8 --min-share 0`: 16, 34 and 26 hits, all form sentences or stock questions ("what is the upper end of the 95% interval"). The settings (gas demand, used cars, a courier's smudged log, stopping distances, an ice-cream kiosk, a freight index, a fund's raw-return fit, a supermarket's beta, power against gas and carbon, a solar farm, overlapping 5-day returns, a bond fund's weeks) are new to the course.

## Engine limits

Three bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems regression)": the per-cent decimal slip cannot be a `wrong` entry, a multi-word unit typed after the number is refused, and the Accepted line prints the stored key's full decimals. None blocked a problem.
