# Problem sets: integrals (brief `docs/briefs/chained.md`)

Files: `app/content/courses/integrals/problems-1.json` ("Problems: accumulating", 35 minutes), `problems-2.json` ("Problems: the fundamental theorem", 40 minutes), `problems-3.json` ("Problems: techniques", 45 minutes). Numbers: `docs/reports/problems-integrals-numbers.py` (exits 0, 765 checks). The JSON was written from a generator in the scratchpad (`integrals-problems/gen.py`), not committed.

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-falling-parabola | 5 (5 / 0) | l1, l2 | 4 |
| problems-1 | p-subscriptions | 5 (5 / 0) | l3, l4 | 3 |
| problems-1 | p-desk-session | 5 (5 / 0) | l1, l2, l3, l4 | 5 |
| problems-2 | p-area-function | 5 (5 / 0) | l5, l6, l7 | 4 |
| problems-2 | p-turnover-decay | 4 (4 / 0) | l6, l7 | 3 |
| problems-2 | p-line-and-parabola | 4 (4 / 0) | l7, l8 | 4 |
| problems-2 | p-etf-units | 5 (5 / 0) | l5, l6, l7, l8 | 5 |
| problems-3 | p-order-size-tail | 4 (4 / 0) | l9, l11 | 4 |
| problems-3 | p-time-to-fill | 5 (4 / 1) | l10, l11, l13 | 5 |
| problems-3 | p-log-return | 4 (3 / 1) | l10, l12, l13 | 4 |
| problems-3 | p-signal-average | 5 (5 / 0) | l9, l12, l13 | 3 |

Typed parts: level 1 15 of 15, level 2 18 of 18, level 3 16 of 18. Expression parts: 1, 3 and 3 (antiderivatives use `upToConstant`; LaTeX only in `accept`). Every lesson of each level appears in at least one problem, and every problem draws on at least two.

Level 1 teaches no antiderivatives, so its exact values come from limits of right sums (with the sum of squares stated), triangles and the split, reversal and constant rules of l3. p-falling-parabola runs $R_6$, the gap rule to $L_6$, the $n$ for a 0.1 band, $R_n$ in closed form, then its limit 18. p-subscriptions finds the peak of a running total, its value, the net change, the reversed integral and the week the total returns to zero. p-desk-session goes midpoint estimate, exact net P&L, time and size of the low, then the last hour by the split rule.

Level 2: p-area-function reads $A'$, the local maximum, the antiderivative and $A(2)$, then finds the end value 12 beats the local maximum. p-turnover-decay fixes $+C$ from $T(0) = 0$ and solves $T(t) = 12$ with a logarithm. p-line-and-parabola finds crossings, the enclosed area, a piece past a crossing, then the total that one integral would undercount. p-etf-units uses $G' = f - 9$, $G(x)$, two values and the area between rate curves.

Level 3: p-order-size-tail substitutes, takes an improper tail, then the median and the 1% size. p-time-to-fill uses parts for $\int x e^{-x}$, a tail, the mean, an expected value of a curved payoff, and the judgement $E[g(X)] \ne g(E[X])$. p-log-return compares the trapezium rule with parts for $E[\ln X]$, predicts the $n = 8$ error, and ends on Jensen's gap. p-signal-average substitutes, averages, runs $T_2$ and predicts the strips needed.

Each later part restates the value it uses; `wrong` lists carry the slip of the part before where one exists (the $\tfrac{9}{n}$ gap carried into part 3 and the "count the 9 once" limit of 0 in p-falling-parabola; old-power and times-$k$ antiderivatives carried into evaluations; $x$ limits kept after a substitution carried into the average).

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (765 checks in all) |
| validator | 0 errors, 0 warnings on the file | same | same |
| playthrough `--local-cdn` | green (15 parts) | green (18 parts) | green (18 parts) |
| playthrough `--mobile --local-cdn` | green; 440 px part shots read, no fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

## Fresh-check

At the gate all three sets have 0 hits. At triage settings (`--min-run 8 --min-share 0`): problems-1 has two, "what is the smallest # that makes the gap" (l2 screens[0], share 0.09) and "in terms of # using # from part" (markov problems-2), both stock phrasing on a new curve. problems-2 has 21, all the form sentence "give an exact fraction or a decimal to # places" and "using # from part". problems-3 has five: four form sentences and "the chance the order is still unfilled after # minutes" against limits-thm l2 (share 0.05), a different model (a geometric count there, a density here). An earlier draft of p-etf-units used a fund against a steady benchmark; the triage matched l8's transfer screen, so the setting became ETF creations against redemptions.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems integrals):". Neither blocked a problem.
