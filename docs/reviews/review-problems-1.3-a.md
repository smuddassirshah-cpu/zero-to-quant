# Problem sets 1.3 (a): second-reader findings

Read at commit 1794fd8. A full second read of six sets. Pattern: section A of `review-problems-1.5-c.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not give what the learner needs, or refuses a sensible rounding in the stated form; `minor` = weak part, loose `wrong` entry, wording, freshness or tooling.

## A. Second read: limits and integrals, sets 1 to 3

Scope: `app/content/courses/limits/problems-1.json` to `problems-3.json` and `app/content/courses/integrals/problems-1.json` to `problems-3.json`: 23 problems, 95 parts (44 limits, 51 integrals; 76 numeric, 12 expression, 7 choice).

Method. Both authors' scripts run first: `problems-limits-numbers.py` 668 checks, 0 failures; `problems-integrals-numbers.py` 765 of 765. Every part was then solved from its text before its answer was read, by hand, and again in `problems-1.3-a-scripts/mine.py`: sympy for the exact value, then a second route (mpmath quadrature, a numeric limit, a central difference, a brute-force scan over whole numbers or a grid). Every `wrong` value was re-derived from the slip its feedback line names and compared inside that entry's own band. Every part was then put through the engine's own graders in node (`grade-check.mjs`: `parseNum`, the `%` unit, `within`, `numSetGrade`, `exprEqual`, `exprEqualUpToConstant`, `shapeFactorised`, with the local Compute Engine): the answer, each `accept` form, each `wrong` entry, and 95 typed strings of my own (fractions, roundings in the stated form, other correct forms of each expression, near misses). The lessons of each level were searched and the passages read for each idea a set leans on (`taught.py`): one-sided limits (limits l1), the squeeze on $\tfrac{\sin x}{x}$ (l4), corners (l8), negative powers (l7), $E[g(X)] \ne g(E[X])$ and densities (integrals l13), the gap rule and the sum of squares (l2), midpoint sums (l1), reversed limits (l3), "shrinks like $h^2$" (l12), $\int e^{kt}$ and $\ln$ (l6).

Tool results.

| check | result |
|---|---|
| authors' number scripts | 668 and 765 checks, 0 failures |
| `mine.py` (reader's own answers and slips) | 95 parts, 313 checks, 0 failures |
| `grade-check.mjs` (engine graders) | 720 checks, 0 failures, 4 rows the reader holds to be content faults (findings 1 to 4) |
| `proposed.py` (numbers of the fixes below) | all hold |
| validator | 0 errors; 0 warnings on the six files |
| playthrough `--problems`, six sets, `--local-cdn` | green (14, 16, 14, 15, 18, 18 parts) |
| the same with `--mobile` | green |
| voice scan 35, both course folders | 0 and 0 |
| `fresh-check.mjs --file`, gate | 0 hits on each set |
| the same at `--min-run 8 --min-share 0` | limits 13, 0, 1; integrals 2, 14, 5: form sentences, stock phrases, bar the l2 hit judged in finding 7 |

Result. No `answer`, `accept`, feedback line or explanation states a wrong value of the quantity asked, and no claim in the 95 parts is false. Every stated number agrees with my own. No expression answer carries a plain-text function name: all are LaTeX (`\sin`, `\ln`, `e^{...}`), and every answer and `accept` form grades correct while every `wrong[].tex` grades wrong. Antiderivative parts take `+ C`, a different constant ($16 - 16e^{-0.5t}$) and an equal form ($\tfrac{x^2}{1 + x^2}$ for $-\tfrac{1}{1 + x^2}$). `form: "factorised"` on `p-research-price` part 3 takes $-(50 - p)(3p - 50)$ and returns the form line for the expanded cubic. The `%` unit on `p-relative-strength` part 3 takes 2 and 2%.

Claims checked beyond the keys: the wiggle bound $|p(t) - 50| \le \tfrac{4}{t}$ at six times; $4q - 8$ is the tangent to $0.5q^2$ at 4; $(\ln R)' = 0.02$; the explicit pool curve $y = k^5 x^{-4}$ gives the same slopes $-64$ and $-2$ as the implicit route; both densities integrate to 1; $P(X > m) = \tfrac{1}{1 + m^2}$ for every $m \ge 0$; the true trapezium errors (ln: 0.0267 at $n = 2$ and 0.00173 at $n = 8$ against the predicted 0.0017; signal: 0.491, 0.119, 0.029, 0.0073 against the predicted 0.49, 0.12, 0.031, 0.0077, so $n = 16$ is the true first $n$ under 0.01 as well as the predicted one); both Jensen directions ($E[100e^{-X}] = 25 > 100e^{-2}$, $E[\ln X] < \ln E[X]$).

### Findings

1. `unclear` | `limits/problems-2.json` | `p-perpetuity-slope` | part 2.
   "Give your answer to the nearest whole number", `tol` 0.5 on $-2040.82$. The part is about a price in pounds. A learner who keeps $P(0.049)$ to the penny has $102.04$ and $\tfrac{2.04}{-0.001} = -2040$, a whole number, and is refused (0.82 off). Only the generic line, shown after the miss, says to keep 4 places.
   Fix: question "Shrink the move: the yield falls from 0.05 to 0.049. Keep $P(0.049)$ to 4 decimal places. What is the average rate of change now? Give your answer to the nearest whole number." Answer `tol` `{ "abs": 1 }`; `sign` `tol` `{ "abs": 1 }`. `accept` "$-2041$, the exact value being $-2040.82$ to 2 places". The band $-2041.82$ to $-2039.82$ still refuses both `wrong` values.

2. `unclear` | `integrals/problems-3.json` | `p-signal-average` | part 4.
   `tol` 0.0005 on 2.96746. The explanation's own printed working, $2(1.2131 + 0.2707)$, is 2.9676, which rounds to 2.968, and 2.968 is refused. A learner who keeps 4 places, as the explanation does, is marked wrong.
   Fix: answer `tol` `{ "abs": 0.001 }`; `accept` "$2.967 \pm 0.001$"; last sentence of `explain` "Then $T_2 = 2(1.21306 + 0.27067) \approx 2.967$." The three `wrong` values (3.509, 1.484, 3.713) stay far outside.

3. `unclear` | `integrals/problems-3.json` | `p-log-return` | part 1.
   The same fault. `tol` 0.00005 on $-0.07192$; the explanation prints $0.5 \times (-0.3466 + 0 + 0.2027)$, which is $-0.07195$ and rounds to $-0.0720$, refused.
   Fix: answer `tol` `{ "abs": 0.0001 }`; `accept` "$-0.0719 \pm 0.0001$"; last sentence of `explain` "That is $0.5 \times (-0.34657 + 0 + 0.20273) \approx -0.0719$." The `wrong` values ($-0.1438$, $-0.0323$, $-0.1733$) stay outside. Part 3's "out by about 0.0267" stands.

4. `minor` | `integrals/problems-2.json` | `p-turnover-decay` | part 3.
   `tol` 0.005 on 13.8346. With $e^{-2} \approx 0.1353$, $16 - 16 \times 0.1353 = 13.8352$, which rounds to 13.84 and is refused. The feedback's own route ($16 - 2.17$) is accepted, so this is the weaker case of findings 2 and 3.
   Fix: answer `tol` `{ "abs": 0.01 }`; `accept` "$13.83 \pm 0.01$". The `wrong` values ($-2.17$, 3.46, 1.08) stay outside.

5. `minor` | `limits/problems-3.json` | `p-relative-strength` | part 3.
   The field carries the unit `%`, so a typed 0.02 is read as 0.0002 and refused. That learner did the division right, and the `correct` line itself prints "$= 0.02$". They get the generic line "Divide the rate of change by the ratio itself", which they have done.
   Fix: add to `wrong` `{ "id": "decimal", "value": 0.0002, "tol": { "abs": 0.00001 } }` and to `byKey` `"decimal": "That is the growth rate as a decimal. The answer is wanted in per cent: $0.02 = 2\\%$, so type 2."` It is clear of the answer and of `raw` (0.0004).

6. `minor` | `integrals/problems-2.json`, `problems-3.json` | five `accept` lines.
   "Any form equal to $2\ln 4$" (and $\sqrt{99}$, $3e^{-2}$, $4(1 - e^{-2})$, $1 - e^{-2}$) on numeric parts. The numeric field takes numbers and fractions only: `parseNum` returns NaN for `2ln4`, `sqrt(99)` and `3e^-2`. The line promises a form the field cannot take. (The fraction lines, "Any form equal to $\tfrac{20}{3}$", are true.)
   Fix: `p-turnover-decay` part 4 "$2\ln 4 \approx 2.77$, accepted as $2.77 \pm 0.005$"; `p-order-size-tail` part 4 "$\sqrt{99} \approx 9.95$, accepted as $9.95 \pm 0.005$"; `p-time-to-fill` part 2 "$3e^{-2} \approx 0.406$, accepted as $0.406 \pm 0.0005$"; `p-signal-average` part 2 "$4(1 - e^{-2}) \approx 3.459$, accepted as $3.459 \pm 0.0005$"; part 3 "$1 - e^{-2} \approx 0.865$, accepted as $0.865 \pm 0.0005$".

7. `minor` | `integrals/problems-1.json` | `p-falling-parabola` | freshness.
   `homework-1` item `h-derive-falling-area` is the same curve and the same derivation: $f(x) = 9 - x^2$, the limit of right sums with the sum of squares stated, $R_n \le A \le L_n$, and the gap $|f(b) - f(a)| \cdot \tfrac{b - a}{n}$ as the finish. Only the interval differs ($[1, 3]$ there, $[0, 3]$ here). Part 3 is also l2's first question on a new curve ("smallest $n$ that makes the gap ... or less"). The brief bars a setup from the course's homework.
   Ruling: change the curve; the chain stands. Fix (all in `proposed.py`): $f(x) = 12 - 3x^2$ on $[0, 2]$.
   - Part 1: $n = 4$ strips, each 0.5 wide. Heights 11.25, 9, 5.25, 0, sum 25.5. $R_4 = 12.75$. `left-ends` 18.75, `no-width` 25.5.
   - Part 2: gap $12 \times \tfrac{2}{4} = 6$, $L_4 = 18.75$. `subtracted` 6.75; `no-length` 15.75 (gap $12 \times \tfrac{1}{4}$).
   - Part 3: gap $12 \times \tfrac{2}{n} = \tfrac{24}{n}$; answer 240. `no-length` 120 (from $\tfrac{12}{n}$), `strict` 241.
   - Part 4: $\Delta x = \tfrac{2}{n}$, $x_k = \tfrac{2k}{n}$. Answer `16-\frac{12}{n}-\frac{4}{n^2}`; `accept` `\frac{16n^2-12n-4}{n^2}`, `24-\frac{4(n+1)(2n+1)}{n^2}`. `left-ends` `16+\frac{12}{n}-\frac{4}{n^2}`; `nine` (rename `once`) `12-\frac{4(n+1)(2n+1)}{n^2}`; `no-width` `12n-\frac{2(n+1)(2n+1)}{n}`. At $n = 4$ it gives 12.75.
   - Part 5: area 16. `no-squares` 24 (the $2 \times 12$ box; the part above the curve takes 8), `stopped` 12.75, `once` 4.

8. `minor` | `limits/problems-3.json` | `p-relative-strength` | freshness.
   `review-3` item `r-log-return-product` opens "A price follows $P(t) = 40e^{0.06t}(1 + 0.02t)$" and asks $\tfrac{d}{dt}\ln P(t)$. This problem opens $P(t) = 40e^{0.06t}$ and ends on the same log-derivative idea. The question asked (a ratio to an index, by the quotient rule) is new; the numbers are the review's.
   Fix: $P(t) = 30e^{0.07t}$ and $I(t) = 1500e^{0.05t}$; $R(0) = 0.02$ as now. Part 1: $P'(0) = 2.1$; `no-chain` 30, `no-forty` (rename `no-thirty`) 0.07. Part 2: $I'(0) = 1500 \times 0.05 = 75$, $R'(0) = \tfrac{2.1 \times 1500 - 30 \times 75}{1500^2} = \tfrac{900}{2{,}250{,}000} = 0.0004$; `swapped` $-0.0004$, `no-square` 0.6, `rates` 0.028, `no-chain` 0.019 (top $45{,}000 - 2250$). Part 3: 2% a year as now; `added` 0.12, `raw` 0.0004, `share-only` 0.07; the index grows at 5%, the gap is $0.07 - 0.05$.

9. `minor` | `integrals/problems-3.json` | `p-time-to-fill` | part 1, freshness.
   The topic exam `topic-1.3` item `c-parts` is "Find $\int x e^{-x}\,dx$ by parts".
   Ruling: stands. It is the first integral by parts any course sets, the exam item is that one step, and the density, tail, mean and curved payoff of parts 2 to 5 appear nowhere else. No edit.

10. `minor` | `limits/problems-2.json` | `p-inventory-penalty` | part 2.
    The correct option is 87 characters against 67, 57 and 57, and the only one that names two slopes. Advisory rule 586.
    Fix: correct option text "$C$ is continuous, with a corner: slope 4 from the left, 3 from the right" (72 characters).

11. `minor` | `limits/problems-2.json` | `p-inventory-penalty` | part 1.
    "For $h < 0$ the first piece applies on both sides of the quotient." A quotient has a top and a bottom, not sides; the sentence means both terms of the top.
    Fix: "For $h < 0$ the first piece gives both $C(4 + h)$ and $C(4)$. Simplify $\dfrac{C(4 + h) - C(4)}{h}$ for such $h$."

12. `minor` | tooling, `app/tools/numbers_lib.py` or `validate.mjs` | band of half a unit.
    Findings 2 to 4 share one cause: a part asks for $k$ places, the answer is irrational, and `tol` is exactly $0.5 \times 10^{-k}$, so any working kept to 4 figures can land one unit out. `review-problems-1.5-c.md` finding 1 is the same class; with these it has been seen three times (protocol 6).
    Fix (engine item, not content): an advisory `[tight-band]` when a numeric question says "decimal to $k$ places" (or "to $k$ decimal places"), the stored answer has more than $k + 2$ decimal digits and `tol.abs` is at most $0.5 \times 10^{-k}$; suggest $10^{-k}$. And a line in `docs/briefs/chained.md`: the tolerance accepts the value the explanation's own printed figures give.

### Per problem

- Chains. Every problem has a real chain and its last part asks for the result the problem is about. Seven parts use no earlier answer and feed a later one: `p-rational-features` 3, `p-session-volume` 4, `p-desk-session` 3, `p-line-and-parabola` 3, `p-etf-units` 2, `p-time-to-fill` 4, `p-signal-average` 4. All acceptable: each is a second result that the last part joins to the first, and the last part restates both. `p-perpetuity-slope` is three independent slopes joined by a judgement; acceptable for the same reason. No dead end.
- Later parts restate what they need: yes, in every item. The rounded hand-offs (3.459 into the average, 0.0267 and 0.49 into the error predictions, $-0.05\pi$ into the product rule) each give an answer inside the part's band; `p-gas-season` part 3 also takes $-28.75$ and $-28.76$ from the 3-place $-0.157$.
- Answer form. Every numeric part with a non-whole answer names its form. 30 parts with a whole-number answer do not say "whole number"; none refuses a sensible entry.
- `wrong` entries: every one differs from its answer and from its neighbours, and every one is the value its named slip gives (215 entries: the 186 numeric ones re-derived in `mine.py`, the 29 `wrong[].tex` forms by hand). Carried slips are present where a learner would carry one (the dropped fee, $a = \tfrac{1}{2}$, the cross term, $n'(20) = 60$, $y = 800$, old-power and times-$k$ antiderivatives, $x$ limits kept after a substitution).
- `p-print-wiggle` part 1 asks how far $p(20)$ "can be" from £50 "at most". $p(20)$ is one number (£50.18); the lead-in "Since $\sin t$ lies between $-1$ and 1" makes the bound the plain reading. No edit.
- `p-gas-season`: $D$ is monthly demand, so its rate is strictly "million therms a month, per month". The part's wording reads naturally. No edit.

Clean problems (15 of 23): limits set 1 `p-broker-schedule`, `p-rational-features`, `p-fit-the-constants`, `p-print-wiggle`; set 2 `p-session-volume`, `p-fund-session`; set 3 `p-research-price`, `p-weighted-pool`, `p-gas-season`; integrals set 1 `p-subscriptions`, `p-desk-session`; set 2 `p-area-function`, `p-line-and-parabola`, `p-etf-units`; set 3 `p-order-size-tail` (bar its `accept` line, finding 6).

### Per set

- Lessons. Every lesson of each level is drawn on (limits l1 to l4, l5 to l8, l9 to l12; integrals l1 to l4, l5 to l8, l9 to l13), and each problem draws on at least two. Limits l1 is the thinnest: it enters through one-sided limits and the idea of closing in (`p-broker-schedule`, `p-print-wiggle` part 3, `p-rational-features` part 4), not through a table or graph. Nothing is used before its level. Limits level 1 asks no slope; level 2 uses a derivative only as a slope (no estimate of a change, no optimisation: `p-fund-session` part 4 is handed the parabola's symmetry); `p-research-price` part 4 asks where the slope is 0, not for a best price. Integrals level 1 uses no antiderivative ($\tfrac{b^3}{3}$ is handed over as a limit of right sums). `p-weighted-pool` part 1 joins l12's implicit step to l11's $(\ln u)' = \tfrac{u'}{u}$; l12 itself has no logarithm, and the question supplies the log form. "Median" is not a level 3 word and is defined in the question.
- Difficulty. One 5 in each set (`p-fit-the-constants`, `p-inventory-penalty`, `p-weighted-pool`, `p-desk-session`, `p-etf-units`, `p-time-to-fill`), and each earns it. Typed parts 88 of 95 (limits 12 of 14, 13 of 16, 14 of 14; integrals 15 of 15, 18 of 18, 16 of 18). Each of the 7 choice parts is a judgement.
- Voice. British spelling, no exclamation marks, no em-dashes, £ for money, explanations of at most three sentences (my own count in `forms.py` and `voice-scan.py 35`: 0 and 0). No option, `why` or feedback line names an option by place.

### Counts

| tag | limits | integrals | tooling | total |
|---|---|---|---|---|
| `wrong` | 0 | 0 | 0 | 0 |
| `unclear` | 1 | 2 | 0 | 3 |
| `minor` | 4 | 4 | 1 | 9 |

### Verdict by set

| set | verdict |
|---|---|
| limits `problems-1` | clean; no edit |
| limits `problems-2` | sound; findings 1, 10, 11 |
| limits `problems-3` | sound; findings 5, 8 |
| integrals `problems-1` | sound; finding 7 (new curve for `p-falling-parabola`) |
| integrals `problems-2` | sound; findings 4, 6 |
| integrals `problems-3` | sound; findings 2, 3, 6; finding 9 stands |

One fix pass on Sonnet covers all of it. Findings 7 and 8 change graded answers, so a delta reader should recompute those two items after the pass; the rest change bands and text only.

### Scripts (`docs/reviews/problems-1.3-a-scripts/`)

| file | what it does | run |
|---|---|---|
| `mine.py` | the reader's own answer and named-slip value for every numeric part, two methods each | `<venv>/bin/python`, exit 0 |
| `grade-check.mjs` | the engine's graders on every answer, `accept`, `wrong` and 95 typed strings; `--accept-lines` for finding 6 | `node ... --local-cdn <pkgs>`, exit 0, 4 FINDING rows |
| `proposed.py` | the numbers of every fix above, twice | `<venv>/bin/python`, exit 0 |
| `taught.py` | per lesson, counts of each idea a set leans on | `python3` |
| `forms.py` | form sentences, explanation length, voice, typed share, option length | `python3` |
| `fresh-grep.py` | each setup's formula and nouns across the course and the exams | `python3` |
| `dump.py`, `exprs.py` | compact dumps for reading | `python3` |

All run from the repo root.


## Fix pass

Edits are targeted JSON field edits (the files round-trip byte-identical, so the diff touches only the fields below). Every changed number was computed twice (sympy exact, then numeric or enumeration) in `docs/reports/problems-limits-numbers.py` and `docs/reports/problems-integrals-numbers.py`, both updated and exit 0 (limits 1253 checks, 0 failures; integrals 1064 of 1064; sets 4 and 5 untouched). The pins in those scripts check the new band exactly, so a reverted fix fails.

1. Fixed. `p-perpetuity-slope` part 2: question now says to keep $P(0.049)$ to 4 places; `tol` and `sign` `tol` abs 1. The penny route -2040 and the 4-place route -2041 are both inside the band of -2040.82; both `wrong` values (2040.82, 2) are outside.
2. Fixed. `p-signal-average` part 4: `tol` 0.001, `accept` "$2.967 \pm 0.001$", explain ends "$2(1.21306 + 0.27067) \approx 2.967$". 2.968 and 2.9676 are now accepted; wrongs (3.509, 1.484, 3.713) outside.
3. Fixed. `p-log-return` part 1: `tol` 0.0001, `accept` "$-0.0719 \pm 0.0001$", explain uses -0.34657 and 0.20273. -0.0720 and -0.07195 accepted; wrongs outside.
4. Fixed. `p-turnover-decay` part 3: `tol` 0.01, `accept` "$13.83 \pm 0.01$". 13.84 and 13.8352 accepted; wrongs (-2.17, 3.46, 1.08) outside.
5. Fixed. `p-relative-strength` part 3: `wrong` `decimal` 0.0002 (tol 0.00001) with its `byKey` line; clear of the answer and of `raw`.
6. Fixed. Five `accept` lines now promise only number forms ("$2\ln 4 \approx 2.77$, accepted as $2.77 \pm 0.005$" and the four like it: `p-order-size-tail` 4, `p-time-to-fill` 2, `p-signal-average` 2 and 3).
7. Fixed. `p-falling-parabola` on $f(x) = 12 - 3x^2$ over $[0, 2]$, all five parts, recomputed here: heights 11.25, 9, 5.25, 0; $R_4 = 12.75$, $L_4 = 18.75$, gap 6; $n = 240$; $R_n = 16 - \tfrac{12}{n} - \tfrac{4}{n^2}$ (symbolic sum, the $24 - \tfrac{4(n+1)(2n+1)}{n^2}$ form, and at $n = 4$); area 16 by limit and by antiderivative. Slip `nine` renamed `once` in parts 4 and 5. Fresh-check 0 hits; the curve appears nowhere else in the course.
8. Fixed. `p-relative-strength` on $P = 30e^{0.07t}$, $I = 1500e^{0.05t}$: $P'(0) = 2.1$, $I'(0) = 75$, $R'(0) = \tfrac{900}{2{,}250{,}000} = 0.0004$ (sympy and a central difference), growth 2%. Slip `no-forty` renamed `no-thirty`. No hit elsewhere in limits or the exams.
9. No edit, as ruled (the part-1 by-parts step stands).
10. Fixed. `p-inventory-penalty` part 2 correct option: "$C$ is continuous, with a corner: slope 4 from the left, 3 from the right" (72 characters against 67, 57, 57).
11. Fixed. `p-inventory-penalty` part 1 question reworded as proposed.
12. Not content. The reader had not added it, so one `[tight-band]` bullet is added to `docs/BACKLOG-INBOX.md` under `Raised later (review problems 1.3 a):`, noting the `docs/briefs/chained.md` line (no brief edited).

Gates: validator 0 errors; `fresh-check.mjs --file` 0 hits on all five changed sets; playthrough `--problems` with `--local-cdn`, with and without `--mobile`, green for limits 2, limits 3, integrals 1, 2, 3; voice scan 35 on both course folders 0 and 0; the tables in `docs/reports/problems-limits.md` and `-integrals.md` updated where an item changed (setting text only; parts, lessons and difficulty unchanged).

Graded values changed (a delta reader recomputes exactly this list; `tol` is abs):

- limits `problems-2` `p-perpetuity-slope` part 2: answer -2040.82 unchanged; `tol` 0.5 to 1; `wrong` `sign` 2040.82 `tol` 0.5 to 1.
- limits `problems-3` `p-relative-strength` (new setting):
  - part 1: answer 2.4 to 2.1; `no-chain` 40 to 30; `no-forty` 0.06 renamed `no-thirty` 0.07.
  - part 2: answer 0.0004 unchanged; `no-square` 0.8 to 0.6; `rates` 0.03 to 0.028; `no-chain` 0.0192 to 0.019; `swapped` -0.0004 unchanged.
  - part 3: answer 0.02 (%) unchanged; `added` 0.1 to 0.12; `share-only` 0.06 to 0.07; `raw` 0.0004 unchanged; new `decimal` 0.0002 (tol 0.00001).
- integrals `problems-1` `p-falling-parabola` (new curve):
  - part 1: answer 15.625 to 12.75; `left-ends` 20.125 to 18.75; `no-width` 31.25 to 25.5.
  - part 2: answer 20.125 to 18.75; `subtracted` 11.125 to 6.75; `no-length` 17.125 to 15.75.
  - part 3: answer 270 to 240; `no-length` 90 to 120; `strict` 271 to 241.
  - part 4: answer `18-\frac{27}{2n}-\frac{9}{2n^2}` to `16-\frac{12}{n}-\frac{4}{n^2}`; accept to `\frac{16n^2-12n-4}{n^2}` and `24-\frac{4(n+1)(2n+1)}{n^2}`; `left-ends` to `16+\frac{12}{n}-\frac{4}{n^2}`; `nine` renamed `once` `12-\frac{4(n+1)(2n+1)}{n^2}`; `no-width` to `12n-\frac{2(n+1)(2n+1)}{n}`.
  - part 5: answer 18 to 16; `no-squares` 27 to 24; `stopped` 15.625 to 12.75; `nine` 0 renamed `once` 4.
- integrals `problems-2` `p-turnover-decay` part 3: answer 13.8346 unchanged; `tol` 0.005 to 0.01.
- integrals `problems-3` `p-signal-average` part 4: answer 2.96746 unchanged; `tol` 0.0005 to 0.001. `p-log-return` part 1: answer -0.07192 unchanged; `tol` 0.00005 to 0.0001.
- Accept text only, no value change: `p-turnover-decay` part 4, `p-order-size-tail` part 4, `p-time-to-fill` part 2, `p-signal-average` parts 2 and 3; and the `p-inventory-penalty` option and question wording.
