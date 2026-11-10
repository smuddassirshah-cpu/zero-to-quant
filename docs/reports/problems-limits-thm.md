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
