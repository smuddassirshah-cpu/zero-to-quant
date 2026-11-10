# Problem sets: limits-thm (brief `docs/briefs/chained.md`)

Files: `app/content/courses/limits-thm/problems-1.json` (level 1). Numbers: `docs/reports/problems-limits-thm-numbers.py`, run with the scratchpad venv; it exits 0.

The script checks each numeric part by two methods (exact or closed form, then scipy.stats, an enumeration of hands, paths or calls, or the pmf summed term by term). It checks that the key is the value at the rounding the question asks for, and that every `wrong` value matches its slip outside the key's band. It also reads the number printed last in `feedback.correct` and checks that the part's own tolerance accepts it. Stated numbers in the explanations are checked too.

Every numeric part states its form in one sentence ("Give a decimal to 4 places", "Give 1 decimal place", "Give a whole number", "Give an exact fraction, or a decimal to 4 places"). Where a part tells the learner to use a rounded value (0.0788, 0.0754), the key is what that rounded value gives. The script also checks that the unrounded route lands in the same band.

## Level 1

File: `problems-1.json` ("Problems: named discrete distributions", 45 minutes).

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-dropped-ticks | 5 (5 / 0) | l1, l2, l3 | 5 |
| problems-1 | p-block-calls | 5 (4 / 1) | l2, l4 | 4 |
| problems-1 | p-fund-record | 5 (5 / 0) | l1, l2 | 3 |
| problems-1 | p-settlement-checks | 5 (4 / 1) | l1, l3, l4 | 4 |

Typed parts 18 of 20. Every lesson appears in at least two problems, and every problem draws on at least two. The two choice parts are judgements: whether calls down a short list are memoryless, and whether the binomial's sample size is safe beyond the 5% rule.

Chains. p-dropped-ticks: the exact $0.996^{400} \approx 0.2012$ justifies $\text{Pois}(1.6)$, which gives an alarm chance of 0.0788. That chance makes a 30-minute session quiet with chance 0.0852 and a mean wait of 12.7 minutes. The last part finds the threshold, 6 drops, that stretches the wait past an hour (42 minutes at 5, 166 at 6). p-block-calls: a first taker on call 3 ($\tfrac{7}{40}$), no taker in four calls as a hypergeometric hand ($\tfrac{1}{6}$), the colleague's geometric 0.2401, the fifth call after four misses (0.5), then the judgement that the list is not memoryless. p-fund-record: $P(T = 3)$ for a lag-wait $T \sim \text{Geo}(0.35)$, $P(T > 6) \approx 0.0754$, the same value again given six good months, $P(X = 12) = 0.0754^2$ in the binomial view, then $P(X \ge 10) \approx 0.1513$ for the brochure. p-settlement-checks: the mean 1.5, the variance with the finite-population factor (1.4193), the binomial clean-run chance 0.2181 (exact 0.2139, Poisson 0.2231), the binomial sample size 152, then the judgement that 152 is safe (the exact answer is 146).

Each later part restates the value it uses. Its `wrong` list holds the value that follows from the commonest slip before it: $P(X \ge 3) = 0.2166$ for the alarm gives 0.0007 and 4.6 in parts 3 and 4; the list's $\tfrac{1}{6}$ appears as a slip under the geometric model.

Level 1 teaches no normal approximation, so no part needs a table value.

### Checks, level 1

| check | result |
|---|---|
| numbers script | 0 failures (389 checks) |
| validator | 0 errors, 0 warnings on the file |
| playthrough `--local-cdn` | green (4 problems, 20 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault in the file |
| voice scan 35 (course folder) | 0 and 0 |

### Fresh-check, level 1

`node tools/fresh-check.mjs --file content/courses/limits-thm/problems-1.json`: 0 hits at the gate. At triage settings (`--min-run 8 --min-share 0`) one hit: "give a decimal to # places let # be the" against `counting-chance/problems-2` items[3], share 0.04. Stock phrasing. The settings are new to the course: no lesson, review or homework uses a dropped-tick feed, a client call list, a fund's monthly record against cash or settlement checks. The lessons use trades, limit orders, backtests, loans, large orders, bugs, margin calls, invoices and cards.

## Level 2

File: `problems-2.json` ("Problems: continuous distributions", 45 minutes).

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-2 | p-quote-life | 5 (5 / 0) | l5, l6 | 3 |
| problems-2 | p-digital-share | 5 (5 / 0) | l7, l8 | 4 |
| problems-2 | p-bounded-pnl | 5 (5 / 0) | l5, l7 | 5 |
| problems-2 | p-default-drag | 5 (5 / 0) | l6, l7, l8 | 4 |

Typed parts 20 of 20. Every lesson appears in two problems, and every problem draws on at least two. Every normal value a part needs is given in the part: $\Phi(0.15) = 0.5596$, $\Phi(0.69) = 0.7549$, $\Phi(0.06) = 0.5239$ with $\Phi(0.11) = 0.5438$ beside it (the value the no-drag slip reaches for), and the cut-offs 1.645 and 2.326 as tail areas. Where the table route rounds $z$ (p-digital-share part 4, p-default-drag parts 4 and 5), the key is the table answer and the tolerance also takes the unrounded answer (0.2439 against 0.2451; 0.4758 against 0.4761; 0.4526 against 0.4529).

Chains. p-quote-life: $c = \tfrac29$ makes the triangle a density, the tail beyond 2 seconds is $\tfrac19$, the mean is 1, an exponential with that mean gives $e^{-2} \approx 0.1353$, and the triangle's $P(T > 2.5 \mid T > 2) = 0.25$ shows it is not memoryless (the exponential gives 0.6065). p-digital-share: median £81.21 and mean £84.95, the chance of ending below the mean ($\Phi(0.15) = 0.5596$), the digital's chance 0.2451, then the 95% VaR of £30.42 from the 5% price £49.58. p-bounded-pnl: a triangular P&L's tail 0.125 and variance 6, its 95% VaR £4.10k against the matched normal's £4.03k, then the 99% gap of £0.55k (5.70 against 5.15). p-default-drag: survival $e^{-0.05} \approx 0.9512$, the mean £41.63 given survival, the unconditional mean £39.60 (below today's £40), the chance a survivor ends up (0.4761), then the chance the holder ends up, 0.4529.

### Checks, level 2

| check | result |
|---|---|
| numbers script | 0 failures (788 checks with level 1); seeded simulations check the lognormal median, mean, 5% price, the default-adjusted mean and chance |
| validator | 0 errors, 0 warnings on the file |
| playthrough `--local-cdn` | green (4 problems, 20 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault in the file |
| voice scan 35 (course folder) | 0 and 0 |

### Fresh-check, level 2

0 hits at the gate. At triage settings five hits, shares 0.10 or less. Two are this course's own form sentences ("give an exact fraction or a decimal to # places") against problems-1. "What is # the chance of losing more than # k" (l7 screens[3]) and "with # drift # and volatility # a year what is" (`exams/topic-3.2` items[6]) are stock phrasing with other numbers. "The share ends the year below its expected price" (l8 screens[9]) is the same question on a new share (£80, 6%, 30% against £100, 5%, 20%), asked as one step of a longer chain; kept, because the chain then prices a digital and a VaR on the same share. The settings (a triangular quote life, a bounded triangular P&L, a share with a default hazard) are new to the course.

The validator's `[wrong-band]` rule reads the first "n decimal places" in a question, else "to the nearest 0.01", as the rounding of the answer. The first draft of p-digital-share part 4 asked for $z$ "to 2 decimal places" and the answer "to 4 places", which the rule does not read. $z$ is now asked "to the nearest 0.01" and the answer in "4 decimal places", which the rule reads first.

Slips that need a $\Phi$ value the part does not give (the no-drag routes in p-digital-share part 4 and p-default-drag parts 4 and 5) have bands wide enough for both a calculator's unrounded $z$ and a table's $z$ to 2 places; the script checks both routes.

## Level 3

File: `problems-3.json` ("Problems: limit theorems", 50 minutes).

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-3 | p-maker-days | 4 (3 / 1) | l9, l11, l13 | 4 |
| problems-3 | p-direction-calls | 5 (5 / 0) | l12, l13 | 5 |
| problems-3 | p-rejected-orders | 4 (4 / 0) | l9, l10, l11 | 3 |
| problems-3 | p-fund-months | 5 (5 / 0) | l10, l11, l12 | 4 |

Typed parts 17 of 18. Every lesson of the level appears in at least one problem (l9, l10, l12 and l13 in two, l11 in three), and every problem draws on at least two. The one choice part is a judgement: Poisson or normal for a rare count. Every normal value is given in its part ($\Phi(2)$, $\Phi(1.61)$, $\Phi(1.55)$, $\Phi(2.63)$, $\Phi(1.8)$, and 1.96 as a two-tailed cut-off).

Chains. p-maker-days: the day's sd £180 from 900 trades (variances add), a losing day with chance 0.0228 by the central limit theorem, losing days in a year as $\text{Bin}(250, 0.0228)$ with the corrected normal estimate 0.0537 of 10 or more, then the judgement that the Poisson (0.0648) beats the normal against the exact 0.0626 at $np(1-p) \approx 5.6$. p-direction-calls: the no-skill sd 10, the corrected tail 0.0606 at 216 right calls, the best of 12 signals (0.5277), the cut-off 227 that holds 12 signals to a 0.05 chance (the exact binomial agrees), then the 625 calls a true 54% signal needs for $t = 2$. p-rejected-orders: Markov's $\tfrac13$, Chebyshev's $\tfrac{1}{36}$ for the same tail, 320 days for an average within 1 by Chebyshev, then 62 by the normal. p-fund-months: the standard error 0.6667, $t = 1.80$, Chebyshev's 0.3086 on a fluke that large, the normal's 0.0718, then the 45 months a true edge of that size needs.

Each later part restates the value it uses, and its `wrong` list holds the value that follows from the commonest slip before it (the sd added as £5,400 gives 0.4734 for a losing day; 0.0548 without the correction gives 0.4915 for the best of 12; $\tfrac{4}{36}$ for the standard error gives $t = 10.8$).

### Checks, level 3

| check | result |
|---|---|
| numbers script | 0 failures (1,181 checks with levels 1 and 2); exact binomial sums in fractions, seeded simulations of the day's sd, the best of 12 and the two-tailed chance |
| validator | 0 errors, 0 warnings on the file |
| playthrough `--local-cdn` | green (4 problems, 18 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault in the file |
| voice scan 35 (course folder) | 0 and 0 |

### Fresh-check, level 3

0 hits at the gate. At triage settings four hits, shares 0.07 or less: three are this course's own form sentences against problems-1 and problems-2, and "part # what is the chance at least one" (`conditional/problems-3` items[3]) is stock phrasing. The settings are new: no lesson, review or homework of the course uses a market maker's 900 trades, a vendor's direction calls tested 12 at a time, a broker's rejected orders, or a 36-month fund record. l12 counts 20 backtests at $|t| > 2$; p-direction-calls asks for the cut-off that controls 12, a new question.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems limits-thm)". The playthrough still shoots only part 1 of a set, and the done page still says "Well done." (both already raised under problems conditional); not repeated.
