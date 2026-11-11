# Problem sets: exp-log (brief `docs/briefs/chained.md`)

Files: `app/content/courses/exp-log/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-exp-log-numbers.py` (exits 0, 1170 checks, 0 failures).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-yeast-culture | 4 (4 / 0) | l1, l3, l4 | 3 |
| problems-1 | p-laptop-value | 4 (4 / 0) | l2, l4 | 4 |
| problems-1 | p-rare-coin | 4 (4 / 0) | l2, l3 | 5 |
| problems-1 | p-curve-point | 4 (4 / 0) | l1, l3, l4 | 4 |
| problems-2 | p-fault-search | 3 (3 / 0) | l5, l6 | 3 |
| problems-2 | p-forty-doublings | 4 (4 / 0) | l5, l6, l7 | 4 |
| problems-2 | p-drawdown-recovery | 4 (4 / 0) | l6, l7, l8 (and l2) | 5 |
| problems-2 | p-app-users | 4 (3 / 1) | l2, l7, l8 | 4 |
| problems-3 | p-savings-doubling | 4 (4 / 0) | l9, l10, l12 (and l3) | 3 |
| problems-3 | p-weekly-target | 5 (5 / 0) | l10, l11 | 4 |
| problems-3 | p-log-chart-line | 4 (4 / 0) | l10, l12, l13 | 5 |
| problems-3 | p-monthly-deposit | 4 (4 / 0) | l9, l10, l11 | 4 |

Typed parts: level 1 16 of 16, level 2 14 of 15, level 3 17 of 17. The one choice part (app users, part 2) is a judgement: the first move before taking logs. Every lesson of each level appears in at least one problem and every problem draws on at least two. Level 1 uses no logarithm: counts are found step by step, and halving or doubling steps come from the l4 law $a^{x+h} = a^x a^h$.

Chains. Level 1: a rule, then a negative and a half power of it, then the factor between those two times as $2^k$; a yearly factor, 2 years, 4 years by the 2-year factor, then the total loss (68.36%, not 100%); a 2-year factor, its square root, the rate, then 18 months as $1.25^{3/2}$; the base from $(3, 64)$, the doubling step, where the curve reaches 2,048, then the mirror curve. Level 2: halvings of a batch, a day by the product law, a week trapped between 18 and 19; $\log 2^{40}$, the power of ten, the leading figure, further doublings to £$10^{16}$ by change of base (13.15, so 14); two falls, the gain back (56.25%), $1.11^n = 1.25^2$ by the power law (4.28), the whole month (5); a rule, the change-of-base form of $\log_{1.3} 25$, the solve, the whole month. Level 3: a continuous balance, its doubling time, three doublings, then 1.5 doublings at half the time; a week of log returns, Friday's close, the log return still needed ($\ln \tfrac{45}{41.76} = 0.0747$), split over three weeks (0.0249), back to a simple return (2.52%); a log-chart gradient, its doubling time, the price 4 years in, its height on the chart; a monthly factor, the matching continuous rate, a 5-year log return (the bridge $\ln e^{rt} = rt$ is stated in the part), the balance.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures (1170 checks for the three sets) | same | same |
| validator | 0 errors, no warning on the file (total 4144, as before) | same | same |
| playthrough `--local-cdn` | green (16 parts) | green (15 parts) | green (17 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |
| `fresh-check --file` gate | 0 hits | 0 hits | 0 hits |

Census: "Problem sets 48 (items 185)".

The script recomputes each answer twice (fractions or sympy, then a step-by-step walk, a bisection on an exponential series, a halving loop or a brute search), rebuilds every `wrong` value from its named slip, and checks: the key inside its band; the value at the asked rounding, the figure printed last in `feedback.correct` and each rounded route the explanation prints (for example $\ln\tfrac{45}{41.76} = 0.0747$ beside $0.1178 - 0.043 = 0.0748$) accepted; every `wrong` outside the key's band, not overlapping another, with a `byKey` line; for each % part the decimal slip and the per cent figure of `accept`; no "Any form" line; expression keys, accept forms and slips against sympy. Besides the script, every answer, accept form, wrong form and 138 typed strings went through the engine's graders in node (`docs/reports/problems-exp-log-grade.mjs --local-cdn <pkgs>`, run from the repo root: `grade.js` with the local Compute Engine): 677 checks, 0 failures, including `2400\exp(0.055t)`, `2000\left(\tfrac{13}{10}\right)^n`, `£7,624`, `25%` and the refusal of 27.46, 2.53 and 4.80 in % fields.

## Review faults avoided (1.3 a, b, c)

- Bands take sensible roundings and the explanation's own working: 4242 and 4243 (half past twelve, from $\sqrt2 \approx 1.414$ or 1.4142); 1397 and 1398 (coin, from $1.118^3$); 37.80 and 37.81; 6787 and 6788 (direct route and $2^{1.5}$ route); 7623.68 and 7623.84 and 7624; 5.80 from both the given 5-place logs and full precision.
- Every numeric part names its form; every `accept` gives a number, never "Any form equal to".
- Each % part has a `decimal` slip; `over100` only where a `wrong` value is above 1.
- `wrong` bands checked against each other and the key; no band wider than its own slip needs (one entry dropped where a 4.5 band met the 4 slip).
- Last parts ask for the result the problem is about; each later part restates the value it needs; no part is a dead end (each result feeds the next part, as listed under Chains).
- Expression answers are LaTeX with `e^{...}`, no plain `ln(`. The exponent forms were tested through the grader.

## Freshness

Gate clean on all three. Triage (`--min-run 8 --min-share 0`): only the form sentence "give your answer in pounds to the nearest pound", shared with other sets.

Read by hand against the course's 13 lessons, quizzes, three reviews, three homeworks, four Fluency sets and `topic-0.3`:
- Settings not used elsewhere in the course: yeast culture, laptop, rare coin, a curve through $(3, 64)$, a fault search, £1 doubled 40 times, a drawdown and recovery, app users, Mia's continuous account, a weekly log-return target, a £15 to £135 chart line, a monthly-paid deposit.
- Shapes that recur, judged acceptable: a factor from two values with a root (coin) is l3's transfer idea, but here the values lie in the past and present and the item goes on to a $\tfrac32$ power; `topic-0.3` `e-years-to-target` depreciates a car, so the laptop asks the total loss as a percentage instead of a first whole year; "first whole month above a target" (app users, recovery) is the l8 and `review-2` technique with new stories and a log law first; a log-chart gradient (chart line part 1) is `l13` `q-slope-rate`'s skill with other numbers, then three further steps.
- No quiz, review or homework number is reused (checked: 1,024, 10,000, 12,100, 5,000 at 4%, £27, 2,500 at 6%, 1.09, the 10%/20%/30% up-down moves, 4,000 at 6%, 6,000 at 3.5%, £64 to £80).

## Engine limits

Two bullets to `docs/BACKLOG-INBOX.md` under "Raised later (problems exp-log):": the Accepted line prints `accept` forms as raw LaTeX source; the fixed feedback bar covers the last part's input at 440 px.
