# Problem sets 0.3 (b): second-reader findings

Read at commit 4ee6a57. A full second read of three sets. Pattern: `review-problems-0.2-b.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not give what the learner needs, or refuses a sensible entry in the stated form; `minor` = weak part, loose chain, loose `wrong` entry, wording, freshness or tooling.

## A. Second read: exp-log 1 to 3

Scope: `app/content/courses/exp-log/problems-1.json` to `problems-3.json`: 12 problems, 48 parts (44 numeric, 3 expression, 1 choice).

Method. The author's two scripts were run first. Every part was then solved from its text before its key was read (`problems-0.3-b-scripts/questions.py` prints the questions alone), by hand, and again in `mine.py`: sympy or mpmath for the exact value, then a second route (stepping the story month by month, bisection on the curve, counting halvings, a loop over doublings). Every `wrong` value was rebuilt from the slip its feedback line names and compared inside that entry's own band; every band was tested against the value the feedback prints, sensible roundings in the stated form and the value carried from the rounded earlier part, and against its neighbours for overlap. Every part was then put through the engine's own graders in node (`grade-check.mjs`: `parseNum`, `within`, `matchWrong` as `numeric.js` calls them, `exprEqual` and `normExpr` as `expression.js` does, with the local Compute Engine): the key, each `accept` form, each `wrong` entry on its own key, and 425 typed strings of my own (other orders, `\exp`, `e^{\frac{11t}{200}}`, a letter and `=` in front, fractions and mixed numbers, a Unicode minus, currency signs, thousands commas, a % sign, a decimal in a % box, roundings one step either side). The 13 lessons with their quizzes, the three reviews, three homeworks, four Fluency sets and the exp-log items of `topic-0.3` and `stage-0` were read item by item (`problems-0.2-b-scripts/skim.py`), and each setting and number was searched across the Stage 0 courses and the exams (`fresh-grep.py`).

Tool results.

| check | result |
|---|---|
| author's number script | 1170 checks, 0 failures |
| author's grade script (`--local-cdn`) | 677 checks, 0 failures |
| `mine.py` (reader's own answers and slips) | 44 numeric parts, 840 checks, 0 failures, 8 notes (findings 2, 6, 9 and loose bands) |
| `grade-check.mjs` (engine graders) | 48 parts, 425 typed rows, 822 checks, 0 failures, 2 rows held to be faults (findings 6, 7) |
| `proposed.py` (numbers of the fixes below, freshness of 11%) | 35 checks, 0 failures |
| validator | 0 errors; 0 warnings on the three files |
| playthrough `--problems`, three sets, `--local-cdn` | green |
| the same with `--mobile` | green |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --file`, gate | 0 hits on each set |
| `fresh-check.mjs --min-run 8 --min-share 0` | only the form sentence "give your answer in pounds to the nearest pound" |
| `fresh-grep.py` and the reader's own reading | one reuse worth a change (finding 12) and notes under Freshness |

Result. No `answer`, `accept` line, `why` or explanation states a wrong value, and every stated number agrees with mine. Every key and `accept` form grades correct; each of the 139 numeric and 9 expression `wrong` entries grades wrong and lands on its own key; no two bands overlap. Every numeric part states its form. Expression answers take either order, `\times`, brackets, `N=`, `U=` and `A=` in front, `1500\cdot2^{n+1}`, `3000\cdot4^{n/2}`, `2000(1+0.3)^n`, `\left(\tfrac{13}{10}\right)^n`, `2400\exp(0.055t)`, `2400(e^{0.055})^t`, `\tfrac{2400}{e^{-0.055t}}` and `e^{\frac{11t}{200}}`, and refuse `3000\cdot2n`, `2000e^{0.3n}`, `2400\cdot1.0565^t` and `2400e^{0.055}t`. Numeric fields take `£7,624`, `4,243`, `−5.5`, `-5 1/2`, `25%` and `56.25%`; a decimal in a % box lands on the `decimal` line. A letter in front (`k=2.5`) or a unit word behind (`6 cm`) leaves Check disabled, which is the known engine limit (inbox, 0.2 a and 0.3 a), not a mis-mark. One feedback line states a false rule (finding 1). Two parts do not give the learner what they need (findings 2, 3).

Loose but harmless bands, no change asked: savings 3 takes 37.82 (key 37.808 ± 0.015), deposit 3 takes 0.2396, weekly 4 takes 0.0250.

Claims checked beyond the keys: $2^{2.5} \approx 5.66$ and $4243 \div 750 \approx 5.66$; $0.75^4 = 31.64\%$ and the 3-year loss 57.81%; $640 \to 800 \to 1000$; $4^{5.5} = 2^{11} = 2048$ and $4^{0.25} = \sqrt2$; the prose rule $2^k \ge N$ gives 11, 16 and 19, and ceiling halving agrees; $2^{40} = 1{,}099{,}511{,}627{,}776$; $2^{49} < 10^{15} < 2^{50}$; $\log 1.25$, $\log 1.08$, $\log 25$, $\log 1.3$ to the places printed; balances 47,018 and 50,780, users 46,596 and 60,575; $72 \div 5.5$, $\tfrac{\ln 2}{\ln 1.055}$; $e^{0.043} = 1.04394$; $\ln 1.125 = 0.1178$; three weeks at 2.52% take £41.76 to £45.00; $9^{1/8} - 1 = 31.61\%$; the tripling time is exactly 4 years; $\sqrt{15 \times 135} = 45$; $1.004^{12}$, $e^{0.048}$, $e^{0.2395}$, $6000 \times 1.004^{60} = 7623.84$.

### Findings

1. `wrong` | `exp-log/problems-1.json` | `p-yeast-culture` part 1 | `feedback.byKey.added`.
   "Adding $2^n$ barely changes 3,000." That is false after the first few hours: $2^{12} = 4096$ more than doubles it, and the rule is asked for every $n$.
   Fix: "After one hour that gives 3,002 cells, not 6,000. Doubling multiplies the whole culture: $3000 \times 2^n$."

2. `unclear` | `exp-log/problems-3.json` | `p-weekly-target` parts 3, 4, 5 | key off the value the question names.
   Part 3 says "Using Friday's close of £41.76". That gives $\ln\tfrac{45}{41.76} = 0.074724$, so 0.0747. The key is 0.074783, the `accept` line leads with 0.0748, and `correct` works from Monday's £40.00 instead. A learner who does as told types 0.0747, is marked right, and part 4 then says "that 0.0748". The brief: a part that names a rounded value has the answer that value gives. Part 5's key, 0.025241, is likewise $e^{0.0748/3} - 1$, not the $e^{0.0249} - 1 = 0.025213$ its question names; 2.52 passes by 0.9 of a hundredth of a point.
   Fix (numbers in `proposed.py`).
   - Part 3: `answer` 0.074724, `tol` 0.0001 (takes 0.0747 and 0.0748, refuses 0.0746 and 0.0749), `accept` "0.0747 (0.0748 is also accepted)". `correct` "$\ln \tfrac{45}{41.76} \approx 0.0747$." `explain` "The log return needed is ln of the target over Friday's close: $\ln \tfrac{45}{41.76} \approx 0.0747$. Check from Monday: $\ln \tfrac{45}{40} \approx 0.1178$, and the week supplied 0.043, leaving 0.0748. The two agree to rounding." `inverted` value $-0.0747$, line "That is $\ln \tfrac{41.76}{45}$, a fall. The price must rise, so the log return is positive."
   - Part 4: question "The trader hopes to earn that 0.0747 in three equal weekly log returns. Using 0.0747, what must each week's log return be? Give 4 decimal places." `answer` 0.0249, `tol` 0.0001. `wrong`: `cube-root` 0.4212 "You took the cube root of 0.0747. Log returns add, so divide by 3."; `times-three` 0.2241 "You multiplied by 3. The three weeks share the 0.0747 between them."; `carried` 0.0259 "That shares out 0.0776, the simple return. The log return needed is 0.0747." `correct` "Log returns add, so each week needs $0.0747 \div 3 = 0.0249$." `generic` "Not quite. Three equal log returns add up to 0.0747." `explain` "Three weekly log returns $\ell$ add to $3\ell$. So $3\ell = 0.0747$ and $\ell = 0.0249$. Simple returns would not split this way, because they compound."
   - Part 5: `answer` 0.025213 (tol unchanged; takes 2.52 and 2.521, refuses 2.51 and 2.53).

3. `unclear` | `exp-log/problems-3.json` | `p-monthly-deposit` part 3 | the step is not taught.
   The part needs "a continuous rate is a log return per year". No lesson of the level says so: l11 never names a continuous rate, and l9, l10, l12 and l13 never name a log return. It follows in one line from $\ln(e^{x}) = x$ (l10), but the learner is not shown the line before being marked on it.
   Fix: question "Growing at a continuous rate $r$ for $t$ years multiplies by $e^{rt}$, so the log return is $\ln(e^{rt}) = rt$. The continuous rate is 4.79% a year. What is the log return of Leo's deposit over the 5 years? Give 4 decimal places." Key and feedback unchanged.

4. `minor` | `exp-log/problems-2.json` | `p-forty-doublings` parts 3, 4 | loose chain.
   Part 3's result, $m = 1.10$, is used nowhere: part 4 goes back to part 1's 12.0412.
   Fix: part 4 question "Using $2^{40} \approx 1.10 \times 10^{12}$ from part 3 and $\log 2 \approx 0.30103$, how many further doublings first take the £$2^{40}$ above £$10^{15}$? Give a whole number." Key 10 and the `wrong` values stand. `correct` "The money must grow by a factor of $\tfrac{10^{15}}{1.10 \times 10^{12}} \approx 909$. $\tfrac{\log 909}{\log 2} \approx \tfrac{2.9586}{0.30103} \approx 9.83$, so 10 more doublings." `generic` "Not quite. Find the factor still needed, then count its doublings with $\tfrac{\log x}{\log 2}$." `rounded-down` "Nine more doublings multiply by 512, short of the 909 needed. A tenth is needed." `tenfold-steps` "About 3 is the gap in tenfold steps, $\log 909 \approx 2.96$. Each doubling is only 0.30103 of a step, so divide: 9.83." `explain` "The factor still needed is $\tfrac{10^{15}}{1.10 \times 10^{12}} \approx 909$. By the change of base rule that is $\log_2 909 = \tfrac{2.9586}{0.30103} \approx 9.83$ doublings. Ten is the first whole number of doublings to pass it."

5. `minor` | `exp-log/problems-2.json` | `p-drawdown-recovery` part 4 (also `p-forty-doublings` parts 2 and 4) | a natural slip gives the key.
   Three of the set's five "whole number" parts are right by plain rounding to the nearest: 12.0412 to 12, 9.83 to 10, 5.80 to 6. Only `p-fault-search` 3 (18.32 to 19) and `p-app-users` 4 (12.27 to 13) test the direction. The last part of the difficulty 5 problem should.
   Fix: grow at 11% a month, so that $n \approx 4.28$ and the answer is 5 (11% is used nowhere in the course or its exams).
   - Prose "... then grows 11% a month."
   - Part 3: question "Recovering needs the factor $1.5625 = 1.25^2$ from part 2, and $n$ months at 11% multiply by $1.11^n$. Using $\log 1.25 \approx 0.09691$ and $\log 1.11 \approx 0.04532$, solve $1.11^n = 1.25^2$. Give $n$ to 2 decimal places." `answer` 4.2764, `tol` 0.006, `accept` "4.28". `wrong`: `no-power` 2.14; `inverted` 0.23; `simple` 5.11 "That shares 56.25% out as 11% a month with no compounding. Each month's 11% grows on the last, so it takes less time."; `carried` 3.22 (line unchanged); `divided-numbers` 1.41 "You divided 1.5625 by 1.11. The power $n$ comes down only after taking logs." `inverted` line with "$\log 1.11$". `correct` "$n \log 1.11 = 2 \log 1.25$, so $n \approx \tfrac{2 \times 0.09691}{0.04532} \approx 4.28$ months." `explain` "Taking logs, $\log(1.11^n) = \log(1.25^2)$, and the power law gives $n \log 1.11 = 2 \log 1.25$. So $n = \tfrac{2 \times 0.09691}{0.04532} = \tfrac{0.19382}{0.04532} \approx 4.28$."
   - Part 4: question "Using $n \approx 4.28$, after how many whole months of growth is the strategy first back above £50,000? Give a whole number." `answer` 5. `wrong`: `rounded-down` 4 "After 4 months it holds $32{,}000 \times 1.11^4 \approx 48{,}578$ pounds, still below £50,000."; `with-falls` 7 "7 counts the two months of falls as well. The question asks for months of growth only." `correct` "After 4 months it holds about £48,578, still short. After 5 months it holds about £53,922, so 5 months." `generic` "Not quite. 4.28 months is not a whole month, and after 4 months it has not yet recovered." `explain` "The strategy reaches £50,000 at about 4.28 months, between months 4 and 5. At month 4 it holds $32{,}000 \times 1.11^4 \approx 48{,}578$ pounds, and at month 5 about 53,922 pounds. So 5 whole months of growth bring it back."

6. `minor` | `exp-log/problems-1.json` | `p-rare-coin` part 4 | band.
   $1397.54 \pm 1.5$ takes £1,399, which no rounding of the answer or of the explanation's working gives.
   Fix: `tol` `{"abs": 1}`. It still takes 1397, 1398, 1397.5 (from $1250 \times 1.118$) and 1397.54.

7. `minor` | `exp-log/problems-3.json` | `p-weekly-target` part 5 and `p-monthly-deposit` part 2 | `wrong` `decimal` bands too broad.
   Each `decimal` band is $\pm 0.005$ of a point wide where the answer is under 5%. In weekly 5 a learner who retypes the log return as 0.0249, or types the `simple-split` slip as 0.0259, lands on `decimal` and is told "Type the percentage, 2.52". In deposit 2 the `quoted` and `factor-rate` slips typed as 0.048 and 0.0491 are told "Type the percentage, 4.79". Each hands over the answer to a learner who did not have it.
   Fix: `"tol": {"abs": 5e-07}` on both `decimal` entries (takes 0.0252 and 0.02521; 0.0479 and 0.04793).

8. `minor` | `exp-log/problems-2.json` | `p-app-users` part 3 | `wrong` `simple` not what its line says.
   83.33 is $25 \div 0.3$. Its line says "as if each month added a fixed amount", but a fixed 600 users a month reaches 50,000 at $n = 80$.
   Fix: value 80, line "That adds a fixed 600 users a month: $2000 + 600n = 50{,}000$ at $n = 80$. The rise compounds, so it is far quicker."

9. `minor` | `exp-log/problems-3.json` | `p-savings-doubling` part 4 | `wrong` `years` value.
   Keyed 2606.2; the slip gives $2400e^{0.055 \times 1.5} = 2606.40$ (2606.44 by doublings). The $\pm 1$ band hides it.
   Fix: value 2606.4.

10. `minor` | `exp-log/problems-2.json` | `p-app-users` part 2 | one lesson of the level, and a repeated screen.
    Part 1 is level 1's l2; parts 2 to 4 are all l8. The choice part is l8's own generalise question ("What is the first move for $3 \times 2^x = 48$?") with new numbers, and its `join` option is l8's trap. The report's "l7" rests on one closing sentence.
    Fix: make part 2 the l7 judgement. Question "Using $U = 2000 \times 1.3^n$, the app reaches 50,000 users when $1.3^n = 25$, so $n = \log_{1.3} 25$. Which is equal to $\log_{1.3} 25$?" Options: `ratio` "$\dfrac{\log 25}{\log 1.3}$" (correct); `quotient` "$\log \dfrac{25}{1.3}$", why "That is the log of a quotient, about 1.284. Change of base divides one log by the other."; `difference` "$\log 25 - \log 1.3$", why "Subtracting logs gives $\log \tfrac{25}{1.3} \approx 1.284$. Change of base divides the logs."; `numbers` "$\dfrac{25}{1.3}$", why "That divides the numbers and gives about 19.23, but $1.3^{19.23}$ is far above 25." `correct` "Change of base: $\log_{1.3} 25 = \tfrac{\log 25}{\log 1.3}$, in any one base." `generic` "Not quite. Measure 25 in steps of 1.3: divide its log by the log of one step." `explain` "Dividing $2000 \times 1.3^n = 50{,}000$ by 2,000 gives $1.3^n = 25$. So $n$ is the log of 25 to base 1.3. The change of base rule writes it as $\tfrac{\log 25}{\log 1.3}$." Part 3's question becomes "Using $n = \tfrac{\log 25}{\log 1.3}$, find $n$. Give 2 decimal places."

11. `minor` | `exp-log/problems-1.json` | `p-curve-point` part 4 | wording.
    "is the mirror image of $y = 4^x$" does not say in which line; only the explanation does.
    Fix: "is the mirror image of $y = 4^x$ in the y-axis."

12. `minor` | `exp-log/problems-3.json` | `p-log-chart-line` part 1 | freshness.
    The part is l13's transfer screen ("a straight line from £100,000.00 in 2016 to £400,000.00 in 2026. What continuous yearly growth rate ... Give a percentage to two decimal places") and its quiz item 3 (£30.00 to £120.00 over 4 years) a third time, ending in the same year. The gate reads word runs and missed it. Parts 2 to 4 carry the problem on, so only the dates need to move.
    Fix: prose "... from £15 at the start of 2017 to £135 at the start of 2025."; part 3 "... at the start of 2021, 4 years in?".

### Sets against their levels

- Ideas taught. Level 1 uses no log; halving and doubling steps come from l4's equal-step law, and $1.25^{3/2}$ is l3's $a^{m/n}$. Level 2 uses the l7 ruler, change of base and l8's three moves. Level 3 uses l9 to l13 only, save the step of finding 3.
- Reading load. Prose is one to three short sentences a problem; the longest question sentence is 23 words (curve point part 3). Fit for the level.
- Lessons. Every lesson of each level is drawn on. Every problem draws on two or more lessons of its level except `p-app-users` (finding 10).
- Difficulty. One 5 a set: `p-rare-coin`, `p-drawdown-recovery`, `p-log-chart-line`.
- Chain. Every part's result is used later or is the final result, except forty doublings part 3 (finding 4). Every later part restates the value it needs.
- Typed parts: 47 of 48. The one choice is a judgement.
- Within set 2, `p-drawdown-recovery` and `p-app-users` end on the same two steps (solve $a^n = b$, then the first whole month). Findings 5 and 10 make them differ.

### Freshness

One change is asked (finding 12). Notes, no change asked:

- `p-curve-point` part 4: `review-1` item 4 asks the height of $y = 0.25^x$ at $x = -1$, the same curve, and l4's fourth screen mirrors $2^x$ to $0.5^x$ at height 8. New base and a new height here.
- `p-yeast-culture` part 3: l3's trap screen is $2^{1/2}$ against the midpoint 1.5; the `halfway` slip is that trap times 3,000.
- `p-yeast-culture` setting: `functions/problems-3` `p-two-cultures` has a lab culture that "doubles each hour", $N = 200 \times 2^t$; `review-2` item 3 has a colony tripling every hour. Other course, other level.
- `p-laptop-value`: l2 quiz item 2 is a van losing 15% a year for 2 years, and l2's trap is "ten falls of 10% make 100%". Same ideas, new numbers, and the chain goes on to the 2-year factor.
- `p-rare-coin`: l3's transfer finds a yearly factor from £10,000.00 to £12,100.00 over two years. The report weighed it; agreed.
- `p-weekly-target`: `ratio/l5-rise-or-fall` has "A share closed at £40.00 on Monday. By Friday ...". `homework-3` item 2 opens a share at £45.00. Other questions.
- `p-monthly-deposit`: `review-3` item 1 also invests £6,000.00 (8 years at 3.5%). The report lists "6,000 at 3.5%" as not reused; the deposit is the same.
- Exams: no exp-log item of `topic-0.3` or `stage-0` shares a setting or a number with the sets.

### Counts

`wrong` 1 (finding 1). `unclear` 2 (findings 2, 3). `minor` 9 (findings 4 to 12).

### Verdict by set

- `problems-1`: one false feedback sentence (1), one band (6), one wording (11). Fix and pass.
- `problems-2`: no wrong value or claim. Four minor items (4, 5, 8, 10), two of them re-keys. Fix and pass.
- `problems-3`: no wrong value or claim. Two unclear parts (2, 3) and three minor (7, 9, 12). Fix and pass.

## Engine

Raised in `docs/BACKLOG-INBOX.md` under `Raised later (review problems 0.3 b):`.

- Validator: on a `unit: "%"` part, warn when the `decimal` entry's band, read as typed decimals, holds another `wrong` value or a retyped given value (finding 7).
- Validator or author script: on a "first whole number above" part, warn when rounding the stated earlier value to the nearest whole number gives the key (finding 5).
