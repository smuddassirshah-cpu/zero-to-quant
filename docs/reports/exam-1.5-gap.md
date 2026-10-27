# Topic 1.5 exam: gap extension (random-vars L5, limits-thm L4, markov L4)

File: `app/content/exams/topic-1.5.json`. The 24 existing items are unchanged and in their order; six items are appended (diff is additions only).
Generator and checks: `/tmp/claude-0/-home-user-zero-to-quant/1109e7e7-f61f-52ac-bff8-468d8cf2fae8/scratchpad/exam-1.5/` (`gen.py` appends the items with assertions, `verify.py` recomputes every number by a second route, `lint.py` checks voice, `shots/` holds desktop and 390 px screenshots).

## Why six items for thirteen asks

`validate.mjs` caps a topic exam at 30 items and the exam had 24. The thirteen asks of the gaps plan are therefore packed into six items, five of them multi-part `table` items, each part a separate graded cell. Every ask is covered; none is left out.

## Shape after the extension

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 5 | 17% | 20% |
| 3 | 14 | 47% | 50% |
| 4 | 8 | 27% | 20% |
| 5 | 3 | 10% | 10% |

| # | id | d | widget | asks covered | rests on |
|---|---|---|---|---|---|
| 25 | e-trade-counts | 4 | table, 2 cells | multinomial covariance; law of total variance | random-vars l20, l17 (and l18) |
| 26 | e-share-count | 3 | choice | Jensen "which is larger" | random-vars l19 |
| 27 | e-beta-pair | 4 | table, 2 cells | order statistic; Beta posterior | limits-thm l17, l18 |
| 28 | e-reversible-sampler | 4 | table, 2 cells, graph canvas | detailed-balance stationary distribution; Metropolis acceptance | markov l13, l15 |
| 29 | e-order-split | 3 | table, 2 cells | Poisson process split | markov l16 |
| 30 | e-default-pair | 5 | table, 4 cells | joint density with a marginal; transformation; convolution; MGF identification; the Stat 110 final-level multi-part problem | limits-thm l14, l15, l16, l19 (Gamma from l18) |

Skills used: rv-variance, rv-condexp, rv-linearity, rv-expect, dl-continuous, rv-joint, mc-longrun, mc-chains, dl-discrete. No new skills were needed (the gap levels added none).

The MGF part asks for $M_Y(0.5) = 4$ for $Y = X + G$; the explanation names it as the Gamma(2, 1) MGF. It tests recognising the MGF of the sum rather than naming a family by text (a free-text "Gamma(2, 1)" cell would grade spelling).

## Numbers, each computed twice

First route in `gen.py` (exact fractions or closed forms, asserted); second in `verify.py`.

- Item 25: $\mathrm{Cov}(U, D \mid N = 10) = -10(0.5)(0.3) = -1.5$; second route, exact enumeration of the multinomial pmf, $-3/2$. $\mathrm{Var}(N) = 500 - 400 = 100$; $\mathrm{Var}(U) = 20(0.25) + 0.25(100) = 30$; second routes, the exact mixture pmf (30) and 2,000,000 simulated days (29.955).
- Item 26: $A = \tfrac12(12.5 + 8) = 10.25$, $B = 1000/102.5 = 9.756$; recomputed directly.
- Item 27: $0.8^5 = 0.32768$ (simulation 0.3280); posterior Beta(9, 5), mean $9/14 = 0.642857$ (grid posterior 0.642857).
- Item 28: detailed balance weights 1, 2, 1.2, $\pi = (5/21, 10/21, 2/7)$, $\pi_2 = 0.2857$; eigenvector of $P^\top$ gives (0.2381, 0.4762, 0.2857). Acceptance $\min(1, 0.6) = 0.6$; a 400,000-step Metropolis run accepts 1 to 2 at 0.5974 and occupies (0.237, 0.477, 0.286). Slip values used in the feedback text: uniform 0.3333, flipped ratios 0.3571, the chain's own 0.3.
- Item 29: buy rate 3 an hour, $e^{-1} = 0.3679$ (simulation 0.3678); $E[\text{buys} \mid 6\ \text{sells}] = 1$ (simulation 1.0001). Slip values: $e^{-4} = 0.0183$, $e^{-3} = 0.0498$, ratio answer 2.
- Item 30: $P(X > 1) = e^{-1} = 0.3679$, $P(G > 0.5) = e^{-0.5} = 0.6065$, $f_Y(2) = 2e^{-2} = 0.2707$, $M_Y(0.5) = 4$; second routes, a 2-D grid integration of $e^{-y}$ on $0 < x < y$ (0.3675, 0.6060, 0.2704, 3.998, grid error about 0.001) and 2,000,000 simulated pairs $(E_1, E_1 + E_2)$ (0.3677, 0.6060, 0.267 by a histogram bin, 3.993). Slip values: $P(Y > 1) = 2e^{-1} = 0.7358$, $P(Y > 0.5) = 0.9098$, $e^{-2} = 0.1353$, one-exponential MGF 2.

No code items were added.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors (350 warnings, none on this file).
- Voice lint on the new items: no `!`, no em-dash, no sentence of 20 words or more (KaTeX counted as one word), explanations at most three sentences, no American spellings.
- `node tools/playthrough.mjs --exam topic-1.5 --local-cdn <pkgs>`: 30 items, scored 30 of 30, passed (run with `--shots --mobile --why`, then again alone after the last edit).
- Screenshots of items 25 to 30 inspected at desktop and 390 px. Fix made: the long part label "(b) posterior mean of $p$" wrapped badly on a phone and became "(b) $E[p \mid \text{data}]$". The three-state graph fits at 390 px; the self-loop labels sit clear of the nodes.

## Engine notes (also in `docs/BACKLOG-INBOX.md`)

Two bullets under "Raised later (exam topic-1.5 gap extension)": the 30-item cap that forced packing, and the table cell `wrong[]` keys the validator still rejects (feedback keyed on `r{i}c1` instead).

## Proposed course.json change

None.
