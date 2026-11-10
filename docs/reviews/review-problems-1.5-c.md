# Problem sets 1.5 (c): second-reader findings and fix-pass delta

Read at commit b97e71b. Section A is a full second read of six sets. Section B is a delta read of the fix pass recorded in `review-problems-1.5-b.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways or does not give what the learner needs; `minor` = weak part, loose `wrong` entry, wording, freshness or tooling.

## A. Second read: markov and limits-thm, sets 1 to 3

Scope: `app/content/courses/markov/problems-1.json` to `problems-3.json` and `app/content/courses/limits-thm/problems-1.json` to `problems-3.json`: 24 problems, 112 parts (54 markov, 58 limits-thm; 103 numeric, 1 expression, 8 choice).

Method. Both authors' scripts run first: `problems-markov-numbers.py` 1,137 checks, 0 failures; `problems-limits-thm-numbers.py` 1,181 checks, 0 failures. Every part was then solved from its text before its answer was read, by hand in exact fractions, with an independent Python pass (scipy `norm`, `binom`, `poisson`, `hypergeom`; `numpy` for $(I - Q)^{-1}R$, $(I - Q)^{-1}\mathbf{1}$ and matrix powers; all 4,096 paths of the barrier walk listed; a 2,000,000-month simulation of the carry rule). Every `wrong` value was re-derived from the slip its line names. Each numeric part was tested against `grade.js within` with the value its feedback prints and with the value its own "Using ..." route gives. `numeric.js` read (fractions accepted) and `expression.js` (equivalence, not string match). Lessons opened or searched for what each level teaches: run lengths and long-run share (markov l4), $f_i$ and transience (l3), $(I - Q)^{-1}R$ (l8), $D_i = i(N - i)$ and $P_i$ with $r$ (l10), $\Phi$ for a walk (l9, l12); the 5% rule and finite-population factor (limits-thm l4), VaR (l5, l7), log drift and drag (l8), hazard rate (l6), $t$-ratio and standard error (l12), continuity correction and $np(1 - p) \ge 10$ (l13).

Result. No `answer`, `accept` text, feedback or explanation states a wrong value of the quantity asked. Every stated number agrees with my own. Row-vector convention holds throughout markov ($\pi P = \pi$ read by columns, rows of $P$ sum to 1), and every stationary and hitting answer is that of the stated matrix. Every normal-table value supplied in limits-thm is right to the digits shown ($\Phi(0.06)$, $\Phi(0.11)$, $\Phi(0.15)$, $\Phi(0.69)$, $\Phi(1.55)$, $\Phi(1.61)$, $\Phi(1.8)$, $\Phi(2)$, $\Phi(2.63)$; 1.645, 1.96, 2.326). The continuity correction is asked for exactly where l13 teaches it (binomial counts: `p-maker-days` 3, `p-direction-calls` 2 and 4) and not for sums of P&L or averages. The stated-form fault of review (a) does not recur: every non-whole numeric part names its form and its `tol` accepts that rounding.

Exact-value claims checked: exact binomial tail for the maker 0.0199; hypergeometric clean run 0.2139 and exact smallest $n = 146$; exact $\text{Bin}(250, 0.0228)$ tail 0.0626 and $\text{Pois}(5.7)$ 0.0648; exact $\text{Bin}(400, 0.5)$ tail 0.0605 and 227 as the first cut-off under 0.0043; unrounded $z = 0.6938$ gives 0.2439. All hold.

### Findings

1. `unclear` | `markov/problems-3.json` | `p-maker-edge` | part 3.
   "Roughly what is the chance ... Give a decimal to 2 places." The answer is 0.0222, so 2 places is one significant figure, and the part gives no table value, where part 4 gives its $z$ and every limits-thm part gives its $\Phi$. A learner with only the 95% rule gets 0.025 and types 0.03, which is outside the band (0.0172 to 0.0272). Feedback prints 3 places ("$\approx 0.022$") under a 2-place question.
   Fix: question "From part 2, her P&L after 400 trades has mean £80 and standard deviation £39.80. Treat it as normal and use $\Phi(2.01) = 0.9778$. What is the chance her P&L after 400 trades is below zero? Give a decimal to 3 places." `tol` `{ "abs": 0.0025 }` on the answer and on the three `wrong` entries. That still takes 0.020 (exact binomial), 0.021 (with a correction), 0.022 and 0.023 ($\Phi(-2)$).

2. `unclear` | `markov/problems-2.json` | `p-rfq-rounds` | prose.
   "After a Counter the dealer re-quotes with chance 0.5; otherwise the client trades with chance 0.2 or walks with chance 0.3." "Otherwise" reads as given no re-quote, where the chances would be 0.4 and 0.6. Only the matrix canvas settles it.
   Fix: "After a Counter the dealer re-quotes with chance 0.5, the client trades with chance 0.2 and the client walks with chance 0.3."

3. `minor` | `limits-thm/problems-2.json` | `p-default-drag` | parts 4 and 5, `no-drag`.
   The named slip is "used the drift 0.04 alone". That gives $z = \tfrac{0 - 0.04}{0.35} \approx -0.11$ and $P(S_1 > 40) = \Phi(0.11) = 0.5438$, the very value the question supplies "as needed". The stored value is 0.4553 (between $1 - \Phi(0.11) = 0.4562$ and $1 - \Phi(0.1143) = 0.4546$), which needs a sign slip as well. So the learner who makes the named slip types 0.5438 and gets only the generic line, and the byKey text says "$z \approx 0.11$" where the slip gives $-0.11$. Part 5 carries it: 0.4331 is $0.9512 \times 0.4553$.
   Fix: part 4 `no-drag` value 0.5438, `tol` 0.0005, text "You used the drift 0.04 alone, so $z \approx -0.11$ and the chance is $\Phi(0.11)$. The log drift is $0.04 - 0.06125$." Part 5 `no-drag` value 0.5173 ($0.9512 \times 0.5438$), `tol` 0.0005. Update the numbers script's derivation to match.

4. `minor` | `markov/problems-2.json` | `p-merger-arb` | part 5.
   "What is the highest price today at which buying has a positive expected profit?" At £8.23 the expected profit is 0, and no highest price with a positive profit exists.
   Fix: "What is the break-even price today: the price at which buying has an expected profit of 0?" `feedback` and `explain` stand.

5. `minor` | `markov/problems-2.json` | `p-rfq-rounds` | parts 3 and 5.
   Part 3 ($t_Q = 1.75$) uses no earlier result and feeds no later part; the chain runs 1, 2, 4, 5 around it.
   Fix: tie it in through part 5's `rounds` option. `why`: "It does end sooner, about 1.53 rounds against part 3's 1.75, but rounds cost nothing here. Compare $q$ times the margin." (New $t_Q = \tfrac{1.3}{0.85} \approx 1.53$, checked by $(I - Q)^{-1}\mathbf{1}$.)

6. `minor` | `markov/problems-3.json` | `p-maker-edge` | freshness.
   Part 3 is the same question as l9's quiz `q-down` (mean and sd given, "close to normal", chance of being down, 2 places), and part 4 is the same question as `homework-3` `h-trades-needed` (trades until the mean is $z$ sds above zero). The story is the course's 52% strategy with new numbers (±£2 at 0.55, 400 trades, $z = 2.01$ and 2.33 against 1.27 and 2).
   Ruling: different enough to stand. No number is shared, the lesson never asks the variance, sd, tail and trade count as one chain, and the level's other three problems are new settings. Fix 1 above also moves the wording of part 3 away from `q-down`. No further edit.

7. `minor` | `limits-thm/problems-1.json` | `p-block-calls` | part 2.
   The prose says she stops at the first taker; part 2 then treats "her first four calls" as a hand of 4, which she makes only if the first three miss.
   Fix: "Part 1 followed one path call by call. Now suppose she rang four clients whatever they said, and treat those four as a hand of 4 of the 10 clients, every hand equally likely."

8. `minor` | `limits-thm/problems-3.json` | `p-maker-days` | part 2, `phi`.
   "That is $\Phi(2)$, the chance the day is above $-2$ sds in the mirror." Hard to follow.
   Fix: "That is $\Phi(2)$, the chance the day is not a loss. A loss is the lower tail: $1 - 0.9772$."

9. `minor` | engine, `app/tools/validate.mjs` line 1592 | `[answer-form]`.
   The rule's pattern (`decimal place|significant figure|fraction|nearest|per cent|%`) does not match the form sentences these sets use: "Give a decimal to 2 places", "Give the exact value", "Give the exact decimal", "Give a decimal." on a terminating answer. The validator now prints 57 false advisory warnings on these six files (markov 13, 14, 8; limits-thm 11, 5, 6) and 137 over the 17 problem sets of topic 1.5, so both reports' "0 warnings on the file" no longer reproduces. No part is missing its form.
   Fix (engine item, not content): widen the pattern to `decimal place|decimal to \d+ places?|\d+ places|exact (value|decimal|fraction)|whole number|significant figure|fraction|nearest|per cent|%`, and skip the rule when the answer has at most 4 decimal digits and the question says "Give a decimal".

### Per problem

- Chains. `p-strategy-trial`: part 3 does not use part 2. Acceptable: parts 2 and 3 are two independent results that part 4 multiplies, both restated there, and the brief's aim (the last part needs the earlier answers) is met. `p-default-drag` has the same shape (parts 1 and 2 feed part 3; parts 1 and 4 feed part 5). `p-stake-size` part 1 (−£4) is restated in part 2 but not used in its sum; `p-direction-calls` part 5 and `p-rejected-orders` part 3 turn to a new case of the same setting. All acceptable; only `p-rfq-rounds` part 3 is a dead end (finding 5).
- Later parts restate what they need: yes, in every item. The rounded hand-offs (3.33, 6.67, 0.0788, 0.0754, 0.9512, 41.63, 0.4761, 0.5515) each give an answer inside the part's `tol`.
- `wrong` entries: every one differs from its answer and from its neighbours, and matches its named slip, bar finding 3.
- `p-maker-edge` part 4: `tol` 2 on 538 is right. $z = 2.33$ gives 537.5, and the unrounded $z = 2.326$ gives 536; all of 536 to 538 put the normal tail under 1%.

Clean problems (18 of 24): markov set 1 `p-thin-book`, `p-two-losses`, `p-margin-calls`, `p-carry-pause`; set 2 `p-band-days`, `p-strategy-trial`; set 3 `p-barrier-note`, `p-stake-size`, `p-pairs-exit`; limits-thm set 1 `p-dropped-ticks`, `p-fund-record`, `p-settlement-checks`; set 2 `p-quote-life`, `p-digital-share`, `p-bounded-pnl`; set 3 `p-direction-calls`, `p-rejected-orders`, `p-fund-months`.

### Per set

- Lessons. Every lesson of each level is drawn on (markov l1 to l4, l5 to l8, l9 to l12; limits-thm l1 to l4, l5 to l8, l9 to l13). Each problem draws on two lessons. Two are thin: `p-stake-size` and `p-pairs-exit` are l10 problems whose only l9 content is one step's mean. Nothing is used before its level: level 1 markov gets long-run shares from run lengths (l4), not $\pi P = \pi$.
- Difficulty. One 5 in each set (`p-carry-pause`, `p-merger-arb`, `p-barrier-note`, `p-dropped-ticks`, `p-bounded-pnl`, `p-direction-calls`), and each earns it. `p-merger-arb` is the easiest of the six 5s but its five-step chain is fair. Typed parts 104 of 112.
- Voice. British spelling, no exclamation marks, no em-dashes, £ for money, explanations of at most three sentences (my own count and `voice-scan.py 35`: 0 and 0). Finding 8 is the one line that reads badly.

### Counts (A)

| tag | count |
|---|---|
| `wrong` | 0 |
| `unclear` | 2 |
| `minor` | 7 |

Finding class note (protocol 6): a `wrong` entry that does not follow from its named slip (finding 3 here, B1 below) was also met in review (a), findings 1 and 13. The number scripts check that a `wrong` value differs from the answer, not that it follows from the slip; ask authors to derive each `wrong` value in the script from the slip's own formula.

## B. Delta read: fix pass of review (b)

Diff read: `git diff 80cd3e6 3886822` on `conditional/problems-4.json`, `problems-5.json` and `random-vars/problems-1.json` to `problems-3.json` (169 lines added). The files at b97e71b equal those at 3886822. Each of the six items was read whole as it stands and the changed answer recomputed by a second method.

| item, part | key now | my value | verdict |
|---|---|---|---|
| `p-doubling-desk` 3 | −22.55, `tol` 0.01 | exact $-20q/(1 - q)$ with $q = (31/32)^{20}$: −22.5486; summed round by round over the 20 quitting rounds: −22.5486; from the rounded 0.5299: −22.5441 | closed |
| `p-doubling-desk` 1 | 0, nearest penny | $\tfrac{31}{32} - \tfrac{31}{32} = 0$ | closed |
| `p-signal-streak` 5 | 0.0582, `tol` 0.0005 | exact $2(0.5 + 0.1 \times \tfrac{256}{881}) - 1 = 0.05812$; from 0.5291: 0.0582 | closed |
| `p-two-houses` 4 | 32 funds, `tol` 0 | $10s - 2 = 4.4$, $s = 0.64$, 32 of 50 | closed |
| `p-tightest-quote` 4 | 10, `tol` 0 | $0.6^9 = 0.01008$, $0.6^{10} = 0.00605$ | closed |
| `p-token-draw` 5 | 43.50, `tol` 0.005 | $38 + 15(\tfrac{70}{210} + \tfrac{7}{210}) = 43.50$; also $38 + 15(E[G] - P(G \ge 1)) = 38 + 15(1.2 - \tfrac{5}{6})$ | closed |
| `p-token-draw` 4 | $\tfrac13$, wording | 70 of 210 hands | closed |
| `p-fund-hedge` 1 | 0.8 typed in %, stored 0.008 | $-0.4 + 1.2 = 0.8$ | closed |

Agreement of the unchanged text. `p-doubling-desk`: −22.54 (the route from 0.5299) and −22.56 are both inside the band, the three slips (−31, −20, −10.598) are outside it, and part 4's "about 470 quitters at −£22.55" balances the 530 at £20. `p-signal-streak`: part 4's 0.5291, "down from 0.1" and the slips 0.1, 0.2, 0.5291 all agree. `p-two-houses`: the new slips are right (40 survivors give 6%, 25 give 3%, 0.64 is the share), and parts 1 to 3 are untouched and consistent. `p-tightest-quote`: slips 9, 21 ($0.8^n \le 0.01$) and 6 ($0.4^n \le 0.01$) are right, and the explanation ties back to part 2 through $\tfrac{98}{125}$ at $n = 3$. `p-token-draw`: slips 38, 43, 53 and 5.5 are right. `p-fund-hedge`: parts 2 to 5 still use $E[A] = 0.8$, and 2.16, 1.68, $\tfrac{7}{12}$ and 1.425 all recompute.

Within the level. `p-tightest-quote` 4 (the CDF of a minimum for $n$ dealers, then powers of 0.6 by trial) stays inside random-vars level 1 and earns the set's 5. `p-token-draw` 5 (a bonus as two indicators, $J_2 + J_3$) is linearity of expectation with indicators, the level's own tool. `p-two-houses` 4 is one linear equation in a weighted average. `p-signal-streak` 5 gives the Kelly rule in the question. `p-doubling-desk` 3 is total expectation with the split given. All five are within what their level teaches.

### Findings

1. `minor` | `random-vars/problems-2.json` | `p-token-draw` | part 5.
   (a) The `carried` value 43.7245 mixes the with-replacement 0.3483 for $G \ge 2$ with the exact $\tfrac{1}{30}$ for $G = 3$. A learner who carries the binomial slip uses it for both: $38 + 15(0.3483 + 0.0837) = 44.48$. (b) The question opens "Using $E[V] = £38$ and $P(G \ge 2) = \tfrac13$" but also needs $P(G = 3)$, which no part has asked for.
   Fix: `carried` value 44.48, text "You used the with-replacement chances 0.3483 and 0.0837. Counting hands gives $\tfrac13$ and $\tfrac{1}{30}$, so the price is £43.50." Question opening: "Using $E[V] = £38$, $P(G \ge 2) = \tfrac13$ and the 7 hands with three gold tokens, what is the fair price to play, in pounds?"

2. `minor` | `random-vars/problems-3.json` | `p-fund-hedge` | parts 1 and 4.
   Part 1 has `unit: "%"` with `placeholder: "decimal"`, which invites 0.008 beside a % sign. Part 4's `carried` line still says "the answer is 0.583" under a 4-place question.
   Fix: placeholder "for example 1.5"; "the answer is 0.5833".

3. `minor` | `conditional/problems-5.json` | `p-two-houses` | part 4.
   The new text uses typographic apostrophes ("S’s", "R’s") where the rest of the file uses straight ones.
   Fix: straight apostrophes in the question, `generic` and `r-count` lines.

Tooling note: the fix pass reports "no warning on these five files". At b97e71b the validator prints 40 `[answer-form]` warnings on them (conditional 13 and 6; random-vars 9, 4, 8). All are the pattern fault of finding A9, not missing form sentences.

### Counts (B)

| tag | count |
|---|---|
| `wrong` | 0 |
| `unclear` | 0 |
| `minor` | 3 |

Status: **closed**. All six changed answers recompute, the surrounding text agrees with them, and the hardened parts sit within their levels. Nothing returns to the fixer; the three minor items can ride with the fix pass for section A.
