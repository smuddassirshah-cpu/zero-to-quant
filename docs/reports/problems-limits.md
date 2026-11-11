# Problem sets: limits (brief `docs/briefs/chained.md`)

Files: `app/content/courses/limits/problems-1.json` to `problems-5.json`. Numbers: `docs/reports/problems-limits-numbers.py` (exits 0).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-broker-schedule | 3 (3 / 0) | l1, l3, l4 | 3 |
| problems-1 | p-rational-features | 4 (3 / 1) | l1, l2, l3, l4 | 4 |
| problems-1 | p-fit-the-constants | 4 (3 / 1) | l2, l3, l4 | 5 |
| problems-1 | p-print-wiggle | 3 (3 / 0) | l1, l4 | 4 |
| problems-2 | p-session-volume | 4 (4 / 0) | l5, l6, l7 | 3 |
| problems-2 | p-fund-session | 4 (3 / 1) | l7, l8 | 4 |
| problems-2 | p-inventory-penalty | 4 (3 / 1) | l6, l7, l8 (and l3) | 5 |
| problems-2 | p-perpetuity-slope | 4 (3 / 1) | l5, l7, l8 | 4 |
| problems-3 | p-relative-strength | 3 (3 / 0) | l9, l10, l11 | 3 |
| problems-3 | p-research-price | 4 (4 / 0) | l9, l10 (and l8) | 4 |
| problems-3 | p-weighted-pool | 4 (4 / 0) | l10, l11, l12 (and l5) | 5 |
| problems-3 | p-gas-season | 3 (3 / 0) | l9, l10, l11 | 4 |
| problems-4 | p-spread-quote | 5 (5 / 0) | l13, l14, l15 | 4 |
| problems-4 | p-signal-decay | 4 (4 / 0) | l13, l14, l16 | 3 |
| problems-4 | p-barbell-hedge | 4 (4 / 0) | l13, l15 | 4 |
| problems-4 | p-level-annuity | 5 (5 / 0) | l15, l16 (and l9) | 5 |
| problems-5 | p-camera-pan | 4 (4 / 0) | l17, l18, l19 | 5 |
| problems-5 | p-app-adoption | 5 (5 / 0) | l17, l18, l20 (and l13) | 4 |
| problems-5 | p-impact-curve | 4 (3 / 1) | l18, l19, l20 | 4 |

Typed parts: level 1 12 of 14, level 2 13 of 16, level 3 14 of 14, level 4 18 of 18, level 5 12 of 13. Every lesson of the level appears in at least one problem, and every problem draws on at least two.

Level 1 chains. p-broker-schedule: a one-sided limit at the join, the constant that removes the jump, then what large orders pay per £1 thousand. p-rational-features: the limit at the hole by cancelling, the kind of break at the other zero of the bottom, the far-out level, then the first whole $x$ inside 0.01 of that level (the definition of a limit at work). p-fit-the-constants runs backwards: the far-out level fixes $a$, a finite limit at 2 fixes $b$, the other zero of the bottom is an asymptote, and the value that repairs the hole is $\tfrac{7}{3}$. p-print-wiggle bounds a $\tfrac{\sin t}{t}$ wiggle, squeezes it to the limit, then finds when the bound keeps the price within a penny. Each later part restates the value it uses; the slip that follows from the commonest slip in the part before has its own `wrong` (the dropped fee in the commission, $a = \tfrac{1}{2}$ in the constants).

Level 2 chains. p-session-volume: a secant over a window, the difference quotient at $t = 2$, its limit, then the power rule to find when trading reaches a rate. p-fund-session: $V'(t)$ by the power rule, its zeros, the sign of the slope graph between them, then the slope graph's lowest point, the fastest fall. p-inventory-penalty: a one-sided difference quotient at the join, the corner of a draft schedule, then the slope and intercept that make the join smooth (the tangent $4q - 8$). p-perpetuity-slope: two secants that shrink towards the tangent of $\tfrac{5}{r}$, the tangent by the power rule, then why the secants are steeper. The $\tfrac{dP}{dr}$ notation of l8 carries the last two parts; no part uses a derivative to estimate a change (that is level 4).

Level 3 chains. p-relative-strength: $P'(0)$ by the chain rule on $e^{0.06t}$, the ratio's slope by the quotient rule, then its growth rate, 2% a year, checked by $(\ln R)' = \tfrac{R'}{R}$. p-research-price: the subscribers' slope by the chain rule, the revenue's slope by the product rule at £20, $R'(p)$ factorised, then the flat price $\tfrac{50}{3}$. p-weighted-pool: implicit differentiation of $0.8\ln x + 0.2\ln y$ for the pool's price, the holdings after a trade, the new price, then the trader's average price as a secant between the two tangents. p-gas-season: $s'(t)$ by the chain rule on a cosine, its value on 1 April, then the product rule for demand. Level 3 has no choice part: each step is a rule applied, not a judgement between rules.

Level 4 chains. p-spread-quote: a market maker's revenue $\tfrac{900s}{(2+s)^2}$, its slope by the quotient rule, the best half-spread $s = 2$ by the sign of $R'$, the revenue there, then a cap at 1 penny that moves the best value to the end, and the tangent estimate of what raising the cap to 1.25 pence adds (8.33, true 6.51). p-signal-decay: L’Hôpital on $\tfrac{N(t)}{t}$ at the start (57) and far out ($\tfrac{\infty}{\infty}$, $-3$), then the best stopping day 19 and the net profit there. p-barbell-hedge: a long 2- and 8-year, short 5-year book of zero-coupon bonds, $V'(u)$ by the chain rule, a zero sensitivity at today's yields, $V''(0) = 900$ so today is a minimum, then the true gain on a 1-point rise, £42.81, where the flat tangent predicts nothing. p-level-annuity: the 0/0 value of $\tfrac{1 - e^{-10r}}{r}$ at 0, $A'(r)$ by the quotient rule, L’Hôpital again for $A'(0) = -50$, the tangent estimate at 2% and the true value, which lies above it.

Level 5 chains. p-camera-pan: $\tfrac{d}{dx}\arctan\tfrac{x}{30}$, the turning rate at $x = 40$ by the chain rule in time, the average rate $\tfrac{\pi}{6}$ over the pass, then the mean value theorem's point $x = 15.7$ m (not the midpoint, the l17 trap). p-app-adoption: a logistic user count given through $N' = \tfrac{N(1000 - N)}{1000}$; the rate at 200 thousand, $N''$ by differentiating that equation in time, the inflection at 500 thousand, the top rate 250, then the mean value bound: at least 3.2 months from 100 to 900 thousand (the true time is $\ln 81$). p-impact-curve: the slope of $2\arctan\tfrac{q}{500}$, the price's rate while buying 200 shares a minute, the bend for buys (the one choice part, a judgement from the sign of $p''$), then the inverse's slope at £1 of impact, 324.61 shares a pound, with the l19 trap (taking $p'$ at the price, not the order) as a slip. Level 5 has three problems: each lesson appears in two of them.

Level 1 teaches no derivative, so no part asks for a slope; the squeeze uses only $-1 \le \sin t \le 1$ from l4.

## Checks

| check | problems-1 | problems-2 | problems-3 | problems-4 | problems-5 |
|---|---|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures | 0 failures | 0 failures (1242 checks in all) |
| validator | 0 errors, 0 warnings on the file | same | same | same | same |
| playthrough `--local-cdn` | green (14 parts) | green (16 parts) | green (14 parts) | green (18 parts) | green (13 parts) |
| playthrough `--mobile` | green; 440 px shots of every part read, no fault | same | same | green; shots read, no fault | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 | 0 and 0 | 0 and 0 |

Census after the three sets: "Problem sets 25 (items 100)". After sets 4 and 5 (in this worktree): "Problem sets 33 (items 130)".

## Fresh-check

problems-1: 0 hits at the gate. At triage settings (`--min-run 8 --min-share 0`) 20 hits, all the form sentence "Give an exact fraction, or a decimal to 4 places" shared with other courses' problem sets. Stock phrasing. The settings (a commission schedule with a parameter, $\tfrac{2x^2 - 2x - 12}{x^2 - 9}$, fitting $a$ and $b$, a $\tfrac{4\sin t}{t}$ wiggle after a print) are new to the course; joining two pieces is l3's idea, met here with a fee and a far-out question.

problems-2: 0 hits at the gate and 0 at triage settings. Secants of a perpetuity, a smooth inventory-penalty join and a fund's value over a session are new settings; l6 used a broker's cost and a hedging cost, not a two-piece penalty.

problems-3: 0 hits at the gate. At triage settings one hit, "give your answer in pounds to # decimal places" against `markov/problems-2.json` items[3], share 0.1: stock phrasing. l9's transfer is shares times price and its quiz a price to earnings ratio; here the ratio is a share against its index, the product a price against demand. l12's transfer is a variance kept fixed; the weighted pool is new. l11's transfer discounts £1,000; no set item discounts.

problems-4 and problems-5: 0 hits at the gate. At triage settings 2 hits, both the stock sentence "Find ... Write it as one fraction. Using ... from part" shared between these two sets. No lesson, quiz, review or homework of the course uses a quote's half-spread, a fading signal's stopping day, a duration-matched barbell, a continuous annuity, a turning camera, an app's logistic growth or an arctan impact curve. l15 used a coupon bond and FX; l16's transfer is compounding; l17's transfer a delta bound; l19's transfers vega and a normal quantile; l20's a log utility.

## Rounding and tolerances

Where a part follows a value that a learner may round, the tolerance takes the rounded routes: p-gas-season part 3 states $s'(3) = -0.05\pi$ exactly, and its band of 0.02 accepts $5 + 215 \times (-0.157) = -28.755$ as well as $-28.77$ (checked in the script). p-perpetuity-slope part 2 asks for the nearest whole number and its band of 0.5 takes both $-2041$ and the exact $-2040.82$.

Sets 4 and 5: p-barbell-hedge part 4 asks the nearest pound; its band of 0.5 takes 42.81 and 43, and leaves out 45, the curvature estimate that level 4 does not teach (checked). The printed terms carry 5 places so that they add to the printed 0.04281. p-spread-quote part 5 takes 8.33 from the rounded slope 33.33 (band 0.006). p-camera-pan part 4 asks 1 place; its band of 0.05 takes 15.68 and 15.7. p-impact-curve part 4 asks the nearest share; its band of 0.5 takes 324.61 and 325.

## Engine limits

None raised, for sets 1 to 5: no bullet added to `docs/BACKLOG-INBOX.md`. Every part fitted the numeric, expression (with `answers` sets and `form: "factorised"`) and choice widgets as documented.
