# Engine pass 9b: hits of the new tags not yet judged

At the pass 9b HEAD. Every remaining hit of today's new tags that `docs/reviews/review-pass9-hits.md` has not judged (its items for `[rounding-tie]`, `[working-band]` and `[key-in-question]` are left out). Columns: tag | file (under `app/content/`) | item | part or field | message.

## [carry-band] (13)

- [carry-band] | exp-log/problems-3.json | p-savings-doubling | items[0].parts[3].wrong[0] | the question carries a rounded value "from part k" (relative error 0.021% against the stored key) and wrong "halfway-pounds" (10800) has a band of +-1, narrower than the 2.3 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | exp-log/problems-3.json | p-savings-doubling | items[0].parts[3].wrong[1] | the question carries a rounded value "from part k" (relative error 0.021% against the stored key) and wrong "midpoint" (7200) has a band of +-1, narrower than the 1.5 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | markov/problems-1.json | p-thin-book | items[0].parts[3].wrong[1] | the question carries a rounded value "from part k" (relative error 0.099% against the stored key) and wrong "swapped" (0.6667) has a band of +-0.0005, narrower than the 0.00066 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | markov/problems-1.json | p-carry-pause | items[3].parts[1].wrong[0] | the question carries a rounded value "from part k" (relative error 0.099% against the stored key) and wrong "stay-ratio" (0.5758) has a band of +-0.0005, narrower than the 0.00057 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | markov/problems-1.json | p-carry-pause | items[3].parts[1].wrong[1] | the question carries a rounded value "from part k" (relative error 0.099% against the stored key) and wrong "used-stay" (0.9333) has a band of +-0.0005, narrower than the 0.00092 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | estimation/problems-3.json | p-three-month-fund | items[1].parts[3].wrong[2] | the question carries a rounded value "from part k" (relative error 0.082% against the stored key) and wrong "same" (1) has a band of +-0.0005, narrower than the 0.00082 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | validation/problems-1.json | p-rent-seeds | items[3].parts[1].wrong[0] | the question carries a rounded value "from part k" (relative error 0.075% against the stored key) and wrong "worst" (0.8926) has a band of +-0.0005, narrower than the 0.00067 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | validation/problems-1.json | p-rent-seeds | items[3].parts[1].wrong[1] | the question carries a rounded value "from part k" (relative error 0.075% against the stored key) and wrong "carried" (0.7731) has a band of +-0.0005, narrower than the 0.00058 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | validation/problems-1.json | p-rent-seeds | items[3].parts[1] | the question carries 0.0468 from part 1, but part 1's feedback.correct prints $0.81 \times 0.0577$, which comes to 0.046737, 0.0467 at the 4 decimal places carried: a learner who carries the printed working is refused or lands outside the band
- [carry-band] | arma/problems-1.json | p-gold-drift | items[3].parts[1].wrong[0] | the question carries a rounded value "from part k" (relative error 0.099% against the stored key) and wrong "no-sqrt" (20.661) has a band of +-0.01, narrower than the 0.02 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | garch/problems-1.json | p-stale-alarm | items[0].parts[2].wrong[1] | the question carries a rounded value "from part k" (relative error 0.014% against the stored key) and wrong "percent" (7111.11) has a band of +-0.6, narrower than the 0.96 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | numerics/problems-2.json | p-vol-curve-extension | items[1].parts[4].wrong[0] | the question carries a rounded value "from part k" (relative error 0.0004% against the stored key) and wrong "peak" (20.472136) has a band of +-0.00006, narrower than the 0.000081 a slip worked from the unrounded carry (or the printed one) moves by: widen it
- [carry-band] | stat-models/problems-2.json | p-two-looks | items[2].parts[2].wrong[0] | the question carries a rounded value "from part k" (relative error 0.39% against the stored key) and wrong "independent" (0.0417) has a band of +-0.0001, narrower than the 0.00016 a slip worked from the unrounded carry (or the printed one) moves by: widen it

## [band-edge] (10)

- [band-edge] | ratio/problems-2.json | p-fund-six-months | items[3].parts[3] | the key 0.024699 rounds to 0.0247 at the 2 decimal places asked, but its band +-0.0001 reaches 0.0246, the next rounding, by a float margin: narrow the band to take the key's rounding only, or widen it on purpose to a full step
- [band-edge] | trig/problems-1.json | p-lake-markers | items[2].parts[2] | the key 47.16 rounds to 47.2 at the 1 decimal place asked, but its band +-0.06 reaches 47.1, the next rounding, by a float margin: narrow the band to take the key's rounding only, or widen it on purpose to a full step
- [band-edge] | analysis/problems-3.json | p-cube-root-greedy | items[2].parts[1] | the key 0.2062995 rounds to 0.2063 at the 4 decimal places asked, but its band +-0.0001 reaches 0.2062, the next rounding, by a float margin: narrow the band to take the key's rounding only, or widen it on purpose to a full step
- [band-edge] | analysis/problems-3.json | p-cube-root-greedy | items[2].parts[3] | the key 0.2697002 rounds to 0.2697 at the 4 decimal places asked, but its band +-0.0001 reaches 0.2698, the next rounding, by a float margin: narrow the band to take the key's rounding only, or widen it on purpose to a full step
- [band-edge] | vector-calc/problems-2.json | p-cycloid-arch | items[1].parts[3] | the key 7.854 rounds to 7.85 at the 2 decimal places asked, but its band +-0.006 reaches 7.86, the next rounding, by a float margin: narrow the band to take the key's rounding only, or widen it on purpose to a full step
- [band-edge] | arma/problems-3.json | p-smoothed-fund | items[0].parts[2] | the key 0.04704 rounds to 0.047 at the 2 decimal places asked, but its band +-0.00006 reaches 0.0471, the next rounding, by a float margin: narrow the band to take the key's rounding only, or widen it on purpose to a full step
- [band-edge] | arma/problems-3.json | p-inflation-arma | items[1].parts[2] | the key 0.43204 rounds to 0.432 at the 4 decimal places asked, but its band +-0.00006 reaches 0.4321, the next rounding, by a float margin: narrow the band to take the key's rounding only, or widen it on purpose to a full step
- [band-edge] | garch/problems-1.json | p-eight-day-window | items[2].parts[0] | the key 0.016726 rounds to 0.01673 at the 3 decimal places asked, but its band +-0.000006 reaches 0.01672, the next rounding, by a float margin: narrow the band to take the key's rounding only, or widen it on purpose to a full step
- [band-edge] | numerics/problems-3.json | p-rate-path-euler | items[2].parts[2] | the key 0.852054 rounds to 0.85205 at the 5 decimal places asked, but its band +-0.000006 reaches 0.85206, the next rounding, by a float margin: narrow the band to take the key's rounding only, or widen it on purpose to a full step
- [band-edge] | pdes/problems-2.json | p-tent-rod | items[0].parts[0] | the key 0.24674 rounds to 0.2467 at the 4 decimal places asked, but its band +-0.00006 reaches 0.2468, the next rounding, by a float margin: narrow the band to take the key's rounding only, or widen it on purpose to a full step

## [later-key] (10)

- [later-key] | counting/problems-1.json | p-tulip-bed | items[0].parts[0].feedback.byKey.divide-four | the line prints 1680, the answer of part 3, which part 1's question does not print: a learner who reads the line learns a later part's result; reword it without the figure
- [later-key] | counting/problems-1.json | p-ice-cream-van | items[3].parts[0].feedback.byKey.ordered | the line prints 2184, the answer of part 2, which part 1's question does not print: a learner who reads the line learns a later part's result; reword it without the figure
- [later-key] | proof/problems-2.json | p-jobs-servers | items[1].parts[0].feedback.byKey.functions | the line prints 1296, the answer of part 2, which part 1's question does not print: a learner who reads the line learns a later part's result; reword it without the figure
- [later-key] | markov/problems-1.json | p-carry-pause | items[3].parts[1].feedback.byKey.used-stay | the line prints 1.4286, the answer of part 3, which part 2's question does not print: a learner who reads the line learns a later part's result; reword it without the figure
- [later-key] | validation/problems-3.json | p-fund-flows | items[0].parts[0].feedback.byKey.train | the line prints 1.7795, the answer of part 2, which part 1's question does not print: a learner who reads the line learns a later part's result; reword it without the figure
- [later-key] | ensembles/problems-1.json | p-opening-gaps | items[3].parts[1].feedback.byKey.other | the line prints 0.163, the answer of part 3, which part 2's question does not print: a learner who reads the line learns a later part's result; reword it without the figure
- [later-key] | arma/problems-2.json | p-etf-flows | items[0].parts[1].feedback.byKey.box-pierce | the line prints 0.1936, the answer of part 3, which part 2's question does not print: a learner who reads the line learns a later part's result; reword it without the figure
- [later-key] | numerics/problems-4.json | p-grid-node-budget | items[2].parts[0].feedback.generic | the line prints 276, the answer of part 3, which part 1's question does not print: a learner who reads the line learns a later part's result; reword it without the figure
- [later-key] | convex/problems-4.json | p-curve-fit-backtrack | items[0].parts[2].feedback.byKey.below-inverse | the line prints 0.03125, the answer of part 4, which part 3's question does not print: a learner who reads the line learns a later part's result; reword it without the figure
- [later-key] | topology/problems-3.json | p-coin-paths | items[2].parts[0].feedback.byKey.two-days | the line prints 0.125, the answer of part 2, which part 1's question does not print: a learner who reads the line learns a later part's result; reword it without the figure

## [no-chain] (7)

- [no-chain] | equations/problems-1.json | p-food-van | items[1] | no part after the first cites an earlier part ("from part 2", "using the 0.34 of part 1") or states an earlier part's key: the 4 parts are separate questions, not a chain (docs/briefs/chained.md); restate the value each later part needs
- [no-chain] | proof/problems-1.json | p-fund-thresholds | items[2] | no part after the first cites an earlier part ("from part 2", "using the 0.34 of part 1") or states an earlier part's key: the 4 parts are separate questions, not a chain (docs/briefs/chained.md); restate the value each later part needs
- [no-chain] | proof/problems-3.json | p-six-nine-lots | items[2] | no part after the first cites an earlier part ("from part 2", "using the 0.34 of part 1") or states an earlier part's key: the 4 parts are separate questions, not a chain (docs/briefs/chained.md); restate the value each later part needs
- [no-chain] | ensembles/problems-2.json | p-ipo-forest | items[1] | no part after the first cites an earlier part ("from part 2", "using the 0.34 of part 1") or states an earlier part's key: the 4 parts are separate questions, not a chain (docs/briefs/chained.md); restate the value each later part needs
- [no-chain] | ensembles/problems-2.json | p-imbalance-stumps | items[3] | no part after the first cites an earlier part ("from part 2", "using the 0.34 of part 1") or states an earlier part's key: the 5 parts are separate questions, not a chain (docs/briefs/chained.md); restate the value each later part needs
- [no-chain] | ensembles/problems-3.json | p-surprise-drift | items[3] | no part after the first cites an earlier part ("from part 2", "using the 0.34 of part 1") or states an earlier part's key: the 5 parts are separate questions, not a chain (docs/briefs/chained.md); restate the value each later part needs
- [no-chain] | topology/problems-2.json | p-right-rays | items[3] | no part after the first cites an earlier part ("from part 2", "using the 0.34 of part 1") or states an earlier part's key: the 4 parts are separate questions, not a chain (docs/briefs/chained.md); restate the value each later part needs

## [slip-in-key-band] (2)

- [slip-in-key-band] | number-sense/problems-2.json | p-golf-card | items[1].parts[2].wrong[0] | wrong "unrounded" (0.277778) rounds to 0.278 at the 3 decimal places asked, which is inside the key 0.278 band +-0.0001: a learner who makes this slip and rounds as asked is marked right, so its line cannot fire; separate the slip from the key or narrow the key's band
- [slip-in-key-band] | number-sense/problems-2.json | p-taxi-split | items[2].parts[1].wrong[0] | wrong "unrounded" (2.8333) rounds to 2.83 at the 2 decimal places asked, which is inside the key 2.83 band +-0.0005: a learner who makes this slip and rounds as asked is marked right, so its line cannot fire; separate the slip from the key or narrow the key's band

## [shown-arithmetic] (2)

- [shown-arithmetic] | testing/homework-4.json | h-np-normal | items[6].feedback.correct | "\Phi\big(\tfrac{0.5 - 0.411}{1/4}\big) = \Phi(0.355)": the left side works out to 0.356, not 0.355; recompute from the numbers as printed, or print the unrounded inputs
- [shown-arithmetic] | fin-ml/l11-deflated-sharpe.json | screens[10] | screens[10].widget.accept | "\Phi((0.1323 - 0.0976)/0.0464) = \Phi(0.747)": the left side works out to 0.7478448, not 0.747; recompute from the numbers as printed, or print the unrounded inputs

## [doubled-word] (10)

- [doubled-word] | courses/exp-log/problems-2.json |  | items.1.parts.1.explain.text | "million million"
- [doubled-word] | courses/garch/l7-garch11.json |  | screens.7.prose | "in in"
- [doubled-word] | courses/least-squares/l11-fitting-a-line.json |  | screens.8.feedback.correct | "squares squares"
- [doubled-word] | courses/number-sense/l14-very-big-very-small.json |  | quiz.4.prose | "million million"
- [doubled-word] | courses/number-sense/l14-very-big-very-small.json |  | quiz.4.feedback.byKey.million | "million million"
- [doubled-word] | courses/number-sense/l14-very-big-very-small.json |  | quiz.4.explain.text | "million million"
- [doubled-word] | courses/numerics/l1-floating-point.json |  | summary.ideas.1 | "doubles doubles"
- [doubled-word] | courses/puzzles/l12-ants.json |  | screens.3.question | "fly fly"
- [doubled-word] | courses/pytest/l9-logic-apart.json |  | screens.8.feedback.correct | "returns returns"
- [doubled-word] | courses/stat-models/l3-poisson-regression.json |  | screens.5.widget.options.2.why | "as as"

Total: 54
