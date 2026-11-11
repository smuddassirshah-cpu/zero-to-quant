# Problem sets: series (brief `docs/briefs/chained.md`)

Files: `app/content/courses/series/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-series-numbers.py` (exits 0, 1465 checks, 0 failures). Engine graders: `docs/reports/problems-series-grade.mjs --local-cdn <pkgs>`, run from the repo root (547 checks, 0 failures).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-theatre-rows | 4 (4 / 0) | l1, l2 | 3 |
| problems-1 | p-pendulum-swings | 4 (3 / 1) | l1, l3 (l2 as the slip) | 4 |
| problems-1 | p-daily-tablet | 4 (4 / 0) | l3, l4 | 5 |
| problems-1 | p-shop-orders | 5 (4 / 1) | l1, l2, l3 | 4 |
| problems-2 | p-tin-display | 4 (4 / 0) | l5, l6 | 3 |
| problems-2 | p-app-users | 4 (4 / 0) | l5, l7 | 4 |
| problems-2 | p-bouncing-ball | 4 (4 / 0) | l7, l8 | 4 |
| problems-2 | p-two-repayment-plans | 5 (5 / 0) | l6, l7, l8 | 5 |
| problems-3 | p-pizza-toppings | 4 (4 / 0) | l9, l10 | 3 |
| problems-3 | p-bracket-estimate | 5 (5 / 0) | l10, l11, l12 | 4 |
| problems-3 | p-gym-membership | 4 (4 / 0) | l10, l12, l13 | 5 |
| problems-3 | p-powers-of-eleven | 4 (4 / 0) | l9, l11, l12 | 4 |

12 problems, 51 parts. Typed parts: level 1 15 of 17, level 2 17 of 17, level 3 17 of 17. The two choice parts are judgements: which rule fits all three swings, and which model month 3's record supports. Every lesson of each level appears in at least one problem and every problem draws on at least two. Nothing runs ahead of its level: level 1 has no sums and no logarithms (first months and swings are found by stepping on), level 2 solves "first day past" by trying powers, and level 3 gives the annuity formula of l13 in the part that uses it.

Chains. Level 1: the next row, $u_n$, the back row, then the first row with half its seats; the ratio, $u_n$, swing 6, then the first swing under 40 cm from swing 6; $u_3$, the level 400, the gap formula, then the first tablet above 395 mg from the gaps; $d$, $r$, the month 3 test, $u_n$, then the first month over 1,000. Level 2: the bottom row, the display, the terms of a sigma, then the stand from both; day 6, the 6-day total by the shift, $S_n$, then the first day past 100,000; 9 rises, the 10th landing, all rises, the whole distance; plan A's $S_n$, its month, plan B forever, plan B by month 21, then what B still owes. Level 3: $\binom{11}{4}$, symmetry for 4 or 7 toppings, Pascal's rule with a 12th topping, the row sum; the $x^2$ number, three terms, the estimate, the $x^3$ number, the improved estimate; a three-term $1.005^{12}$, its discount factor, the stream's value, the saving; $11^4$, $11^5$ from row 5, $1.1^5$, the linear estimate's shortfall. Two parts are second branches joined later (`p-bracket-estimate` 4, used by 5; `p-bouncing-ball` 2, whose working part 4 reuses), as review 1.3 c allowed.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures (1465 checks for the three sets) | same | same |
| engine grade script | 0 failures (547 checks, 168 typed strings) | same | same |
| validator | 0 errors, no warning on the file (total 4145) | same | same |
| playthrough `--local-cdn` | green (17 parts) | green (17 parts) | green (17 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault of ours | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |
| `fresh-check --file` gate | 0 hits | 0 hits | 0 hits |

The numbers script computes each answer twice (fractions, `math.comb` and closed forms; then the story walked term by term, `itertools.combinations` counts, the bracket expanded by repeated multiplication, a long partial sum for each sum to infinity) and rebuilds every `wrong` value from its named slip. It checks the key inside its band, the asked rounding and every rounded route the explanation prints accepted (19.84 from 7.42 and 19.85 from 7.4244; 1781 and 1782 from $0.9^{21} \approx 0.1094$ or 0.109; 1161, 1162 and 1161.89; 0.80795, 0.80796 and the true 0.80798), the figure `feedback.correct` prints last accepted, each `wrong` outside the key's band with a `byKey` line and no overlap, expression keys, accept forms and slips against sympy, and a stated form on every numeric part. The grade script ran the answers, accept forms, wrong forms and typed strings through `grade.js`, including `£1,781`, `1,456`, `u_n=3n+15`, `S_n=2\cdot3^n-2`, `160\left(\frac{2}{5}\right)^{n-1}`, and the refusal of 0.809, 1.0617 and the calculator values where a three-term estimate is asked.

## Review faults avoided (1.3 c, 0.2 a)

- Every numeric part names its form; integer parts say "Give a whole number"; `accept` always starts with a number, never "Any form".
- Bands take the explanation's own printed route (listed above); `wrong` bands for slips a learner rounds are widened to the asked rounding (171.43, 222.22, 105.26, 94.19, 12.5 at $\pm 0.5$), and no band is wider than its slip needs.
- Each later part restates the value it needs; no part says "using part n" without the value. Last parts ask for the result the problem is about.
- Three-term parts carry a `calculator` slip, so the true power is told apart from the estimate with its own line.
- Expression answers are LaTeX (`\cdot`, `^{...}`, `\frac`); no thousands comma is asked in an expression field.
- Natural slips that reach the key: none. The arithmetic model in `p-pendulum-swings` 4 and the $0.9^n$ slip both give 7, which has one line true for both.

## Freshness

Gate clean on all three. Triage (`--min-run 8 --min-share 0`): sets 1 and 2 no hits; set 3 only stock phrasing ("give your answer to # decimal places", "the general term, what is the number in front of").

Read by hand against the 13 lessons, their quizzes, three reviews, three homeworks, six Fluency sets and `topic-0.3`:
- Settings not used elsewhere in the course: theatre rows, a pendulum, a daily tablet, a shop's lost records, a tin display, a messaging app, a bouncing ball, two plans to repay a friend, pizza toppings, $(1 - 3x)^7$, a gym membership, powers of 11.
- A first draft used $(1 - 4x)^5$ for three terms; that is the l12 derive screen's $(1 - 2x)^5$ with one constant changed, so it became $(1 - 3x)^7$ and $0.97^7$ (l12 quiz has $0.97^6$ by $1 + nx$, a different power and method).
- Shapes that recur, judged acceptable: a geometric ratio from two non-adjacent terms (`homework-1` $u_2, u_5$; `topic-0.3` 3rd and 6th) is here months 2 and 4 with an arithmetic rival and a month-3 test, the idea of `review-1` `r-two-readings` taken further; "first term past a target" (l2 savings pot, `review-1`, `homework-2` `h-pass-1000`) appears with new stories and numbers; a recurrence's fixed point and gap (l4, `homework-1` `h-gap-proof`) is used on a dose, not a loan or account; a stream of payments valued with $\tfrac{C}{r}(1 - (1 + r)^{-n})$ (l13, `review-3` pension, `homework-3` loan) is monthly at 0.5% and compared with a lump sum.
- No quiz, review, homework or exam number is reused (checked: 5050, 1275, 10100, 1090, 5465, 6.25, 255, 1533, 0.3125, 126, 216 in $(3x - 2)^4$, 1.1048, 17852.97, 1792, 240, 443.21, 2373.96, 1.02^10, 1.03^8, 0.98^4, 0.97^6).

## Engine limits

Two bullets to `docs/BACKLOG-INBOX.md` under "Raised later (problems series):": a plain-text power with a bracketed exponent (`80*0.9^(n-1)`) grades wrong (fix pass of 0.3 c: the bracketed-base spellings are now `accept` forms in pendulum 2, tablet 3 and shop 4, so the text fallback passes them); the feedback bar and raw-LaTeX Accepted line met again.
