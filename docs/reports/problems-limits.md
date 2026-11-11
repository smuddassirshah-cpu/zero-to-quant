# Problem sets: limits (brief `docs/briefs/chained.md`)

Files: `app/content/courses/limits/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-limits-numbers.py` (exits 0).

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

Typed parts: level 1 12 of 14, level 2 13 of 16, level 3 14 of 14. Every lesson of the level appears in at least one problem, and every problem draws on at least two.

Level 1 chains. p-broker-schedule: a one-sided limit at the join, the constant that removes the jump, then what large orders pay per £1 thousand. p-rational-features: the limit at the hole by cancelling, the kind of break at the other zero of the bottom, the far-out level, then the first whole $x$ inside 0.01 of that level (the definition of a limit at work). p-fit-the-constants runs backwards: the far-out level fixes $a$, a finite limit at 2 fixes $b$, the other zero of the bottom is an asymptote, and the value that repairs the hole is $\tfrac{7}{3}$. p-print-wiggle bounds a $\tfrac{\sin t}{t}$ wiggle, squeezes it to the limit, then finds when the bound keeps the price within a penny. Each later part restates the value it uses; the slip that follows from the commonest slip in the part before has its own `wrong` (the dropped fee in the commission, $a = \tfrac{1}{2}$ in the constants).

Level 2 chains. p-session-volume: a secant over a window, the difference quotient at $t = 2$, its limit, then the power rule to find when trading reaches a rate. p-fund-session: $V'(t)$ by the power rule, its zeros, the sign of the slope graph between them, then the slope graph's lowest point, the fastest fall. p-inventory-penalty: a one-sided difference quotient at the join, the corner of a draft schedule, then the slope and intercept that make the join smooth (the tangent $4q - 8$). p-perpetuity-slope: two secants that shrink towards the tangent of $\tfrac{5}{r}$, the tangent by the power rule, then why the secants are steeper. The $\tfrac{dP}{dr}$ notation of l8 carries the last two parts; no part uses a derivative to estimate a change (that is level 4).

Level 3 chains. p-relative-strength: $P'(0)$ by the chain rule on $e^{0.06t}$, the ratio's slope by the quotient rule, then its growth rate, 2% a year, checked by $(\ln R)' = \tfrac{R'}{R}$. p-research-price: the subscribers' slope by the chain rule, the revenue's slope by the product rule at £20, $R'(p)$ factorised, then the flat price $\tfrac{50}{3}$. p-weighted-pool: implicit differentiation of $0.8\ln x + 0.2\ln y$ for the pool's price, the holdings after a trade, the new price, then the trader's average price as a secant between the two tangents. p-gas-season: $s'(t)$ by the chain rule on a cosine, its value on 1 April, then the product rule for demand. Level 3 has no choice part: each step is a rule applied, not a judgement between rules.

Level 1 teaches no derivative, so no part asks for a slope; the squeeze uses only $-1 \le \sin t \le 1$ from l4.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (668 checks in all) |
| validator | 0 errors, 0 warnings on the file | same | same |
| playthrough `--local-cdn` | green (14 parts) | green (16 parts) | green (14 parts) |
| playthrough `--mobile` | green; 440 px shots of every part read, no fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

Census after the three sets: "Problem sets 25 (items 100)".

## Fresh-check

problems-1: 0 hits at the gate. At triage settings (`--min-run 8 --min-share 0`) 20 hits, all the form sentence "Give an exact fraction, or a decimal to 4 places" shared with other courses' problem sets. Stock phrasing. The settings (a commission schedule with a parameter, $\tfrac{2x^2 - 2x - 12}{x^2 - 9}$, fitting $a$ and $b$, a $\tfrac{4\sin t}{t}$ wiggle after a print) are new to the course; joining two pieces is l3's idea, met here with a fee and a far-out question.

problems-2: 0 hits at the gate and 0 at triage settings. Secants of a perpetuity, a smooth inventory-penalty join and a fund's value over a session are new settings; l6 used a broker's cost and a hedging cost, not a two-piece penalty.

problems-3: 0 hits at the gate. At triage settings one hit, "give your answer in pounds to # decimal places" against `markov/problems-2.json` items[3], share 0.1: stock phrasing. l9's transfer is shares times price and its quiz a price to earnings ratio; here the ratio is a share against its index, the product a price against demand. l12's transfer is a variance kept fixed; the weighted pool is new. l11's transfer discounts £1,000; no set item discounts.

## Rounding and tolerances

Where a part follows a value that a learner may round, the tolerance takes the rounded routes: p-gas-season part 3 states $s'(3) = -0.05\pi$ exactly, and its band of 0.02 accepts $5 + 215 \times (-0.157) = -28.755$ as well as $-28.77$ (checked in the script). p-perpetuity-slope part 2 asks for the nearest whole number and its band of 0.5 takes both $-2041$ and the exact $-2040.82$.

## Engine limits

None raised: no bullet added to `docs/BACKLOG-INBOX.md`. Every part fitted the numeric, expression (with `answers` sets and `form: "factorised"`) and choice widgets as documented.
