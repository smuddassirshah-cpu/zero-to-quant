# Report: measure-prob level 3, "Information and martingales" (topic 3.2)

Brief: `docs/briefs/measure-prob.md`, `## Level 3`, with the brief-check corrections applied: R12 (the l12 hook writes node values from a `table`, each cell `bind: "values.<path>"`, root `values.root`, decimals asked in the prose and the `tol`) and R13 (no walk stopping rule: the look-ahead trap is a `bars` canvas with the exact distribution and `showMean`, the previous screen is the barrier-stopped `walk`, and `max_mean(N)` is the code screen). Stale facts: `markov` level 5 is written, so the numbers come from `markov` l17 (the forecaster), l19 (3 of 10, E[T] = 21, the trader) and l20; `ito` l8 is not written, so nothing is quoted from it. Ids, names, objectives and skills are those of `course.json`. The planner's scripts are gone, so every number was recomputed.

## Files written (`app/content/courses/measure-prob/`)

| File | Screens | Quiz | Canvases and widgets |
|---|---|---|---|
| `l9-information.json` | 11 | 4 | `grid` (eight outcomes, `frames` slider through times 0 to 3, `shade` atoms), `tap-regions`, `multi`, `table`, `numeric`, `console`, `code` (`atoms`, `n_events`, `is_measurable`), `tree` (two-step lookback) |
| `l10-condexp-projection.json` | 11 | 4 | `space` (X, the plane, sliders on a and b, residual), `grid` (random-vars l15 table), `sliders`, `table`, `order` (tower property), `choice` (with `canvas` patches on the trap), `multi`, `code` (`cond_exp`, `mse`), `scatter` (Longstaff-Schwartz) |
| `l11-filtrations.json` | 10 | 4 | `tree` (`frames` with `collapse` and `labels`), `series`, `bars`, `multi`, `choice`, `table`, `numeric`, `code` (`gains`, `is_predictable`) |
| `l12-martingales-defined.json` | 9 | 4 | `tree` (table cells bound to `values`, explicit `nodes` for the trap), two `order` proofs, `choice`, `numeric`, `code` (`is_martingale`, `doob`) |
| `l13-stopping-times.json` | 10 | 4 | `walk` (sliders on both ends, `sq`-style `expr` overlay, `showStopped`), `bars` (`showMean`), two `order` proofs, `multi`, `choice`, `numeric`, `table`, `code` (`stopped_mean`, `max_mean`) |
| `review-3.json` | 10 items, difficulty 2 to 4 | | two items for each of the five lessons |
| `homework-3.json` | 8 items, difficulty 3 to 5 | | `parts` (atoms, gains), `table`, two `multi`, `code` d4, `order` d5 (Wald), `longform` d5 (rubric 10) |

Build scripts, number scripts and audits are in the scratchpad folder `measure-prob-3` (`l9.py` to `l13.py`, `review3.py`, `homework3.py`, `post.py`, `nums.py`, `nums2.py`, `nums3.py`, `audit.py`, `pycheck.mjs`, `seeds.mjs`).

## Validator, playthrough, voice

- `node tools/validate.mjs`: 0 errors. Warnings in the repository stayed at 546 (the figure before this level): none of the seven files has a warning.
- Playthrough with `--local-cdn`, desktop and `--mobile` (390 px, no sideways scroll): l9 15 checks, l10 15, l11 13, l12 13, l13 14, each quiz 4 of 4; `review-3` 10 of 10 recorded; `homework-3` 8 of 8 items, 38 of 38 marks, parts checks ok. All passed in both modes. Screenshots looked at: hooks, trap screens (including the wrong-answer Why sheet on the `space` trap), the walk and bars screens, tables at 390 px and homework items. Fixes made from them: the l9 slider frames now carry group numbers in the cells (eight singleton atoms repeat colours), the trap's `space` canvas hides the answer vector until an option or the explanation shows it, the l12 trap tree hides its probabilities and uses Unicode level labels, the l13 `sq` panel uses a fixed range and a plain chip.
- Voice (`docs/reviews/voice-scan.py`, whole course folder): 0 sentences over 20 words, 0 explanations over three sentences. No `!`, no em-dash or en-dash.
- Code: every solution passes all its hidden tests and examples and every starter passes none, in CPython and in Pyodide 0.27.7 (`pycheck.mjs`, local copy of the package): l9 13 of 13 (starter 0), l10 12, l11 12, l12 12, l13 12, homework 10. No NumPy or SciPy is used, so no first-run load note is needed; the slowest test is under 0.3 s (`stopped_mean` at 2^10 paths).
- Audit (`audit.py`): no choice key more than 1.3 times its longest distractor in plain text, and at most 1.36 times with the LaTeX source counted; no literal backslash-n; every numeric `wrong` has its own `byKey` line and lies outside the answer band; table `byKey` ids are zero-based `r{row}c{col}` and were checked row by row.

## Lesson size: which rungs moved

- l9 (11 screens): the edge case (the trivial sigma-algebra, only constants are measurable) is a quiz item; the "multi: decided at time 1" is its own screen after the hook; the generalise screen of the shape is folded into the ladder's measurability screen.
- l10 (11): the orthogonality check and the Pythagoras split are two table screens; the "taking out what is known" rung is a `choice` on the market table; the edge case (trivial, full and independent) is a `multi`.
- l11 (10): the ladder rung "natural filtration against a larger one" is a `choice` before the gains table; the edge case (deterministic process, trivial F_0) is its own `multi` screen.
- l12 (9): the brief's `choice` for why $H_{n+1}$ comes out is folded into the reason lines and the distractors of the transform `order`; integrability and the constant martingale are the first quiz item (and the explanation of the definition), not a screen.
- l13 (10, the dense one): steps (2) and (3) of the brief are two short `order` screens, not one, because six lines plus distractors was too long; the separate "P(hit 10) = 3/10" numeric is gone (the hook's average and the prose of the unbounded screen carry it); the edge case $T = n$ and $T = 0$ is the fourth quiz item; the `choice` "which theorem handles which term" and the numeric $E[T] = 21$ are consecutive screens.

## Proof steps and the widget that grades each

- l10: tower property, `order` with `same` on (t2, t3) and (t4, t5) and two distractors ("$E[X \mid \mathcal{G}] = E[X \mid \mathcal{H}]$ because $\mathcal{H} \subset \mathcal{G}$", "use $A \in \mathcal{G}$ for every $A$").
- l12: $S_n^2 - n$ is a martingale, `order` with two distractors (an unconditional mean, and $E[X_{n+1}^2 \mid \mathcal{F}_n] = 0$); martingale transform, `order` with two distractors (independence assumed, $H_{n+1}$ treated as adapted).
- l13: stopped process, `order` with `same` on (s2, s3) and one distractor ($\{T > k\}$ is predictable); bounded optional stopping, `order` with two distractors (every stopping time, and $M_T = M_N$); theorem for each limit term, `choice` (monotone for $E[T \wedge n]$, dominated for $E[S^2_{T \wedge n}]$); where it fails, `choice`.
- homework: Wald's identity, `order` (difficulty 5) with `same` on (w2, w3, w4) and two distractors; the optional stopping proof with the ruin chance and duration, and the failing hypothesis, `longform` (rubric 10: 2, 1, 2, 2, 1, 2).

## Numbers and two routes

| Value | Route 1 | Route 2 |
|---|---|---|
| 16 and 256 events of F_2, F_3 (atoms 4, 8); sizes 1, 3, 3, 1 and 16 events of σ(S_3); σ(S_2) 3 atoms, 8 events (sizes 2, 4, 2 on three tosses) | $2^{2^n}$ and atoms from `itertools` | closure by enumerating every union of atoms (`sigma_size`) |
| £96 on UD and DU, maxima £120 and £100 | $100 \times 1.2 \times 0.8$ | path lists in Python |
| 65,536, 32, 6 outcomes, quiz and review sizes | $2^{16}$, $2^5$, $8 - 2$ | enumeration |
| (2, 2, 5), error 2/3, mean error 8/3, residual (1, -1, 0) | atom averages | grid minimisation over a and b in steps of 0.05, which found (2.0, 5.0) and 0.6667 |
| $E[X\mathbf{1}_A] = 4/3$ and $5/3$ | $(3 + 1)/3$ | exact `Fraction` |
| $E[Y \mid X] = -0.8, 0.2, 1.0$; $E[Y] = 0.24$; $E[XY] = 0.46 = E[X E[Y \mid X]]$ | exact `Fraction` over the nine cells | NumPy on the table (-0.8, 0.2, 1.0; 0.24; 0.46) |
| Var(Y) 2.2624 = 0.3904 + 1.872 (row variances 1.76, 1.96, 1.8) | exact `Fraction` | NumPy variance, and the sum checked |
| Longstaff-Schwartz fit 10.32 at 92 (slope -0.54, intercept 60) | hand: $\bar S = 100$, $\bar C = 6$, $-135/250$ | `numpy.linalg.lstsq` |
| Momentum gains 0 and look-ahead 4 on HHTH; look-ahead mean 10 over 10 tosses; momentum mean 0 over 16 paths | enumeration | closed form ($X_k^2 = 1$) |
| Doob values 1/2, 3/4, 1/4, 1, 1/2, 1/2, 0 | backward recursion with `Fraction` | each is the average of its children (checked by `is_martingale`) |
| Martingale checks (S, S² − n, S² not, S − n/5 at p = 3/5, S not at 0.6) | `Fraction` at every node | SymPy one-step conditional expectation |
| Trap process: E[X2 given X1] = ±1, E[X3 given X2] = 2, 0, -2, E[X3 given X1 = 1, X2 = 0] = 1 | exact enumeration | by hand from the tree |
| £114.29, £76.19, £100.00 under q = 0.625, £102.86 under 0.7, £108 undiscounted | $120/1.05$, $80/1.05$ | float arithmetic and $q = (1.05 - 0.8)/0.4$ |
| Drift 0.2 at p = 3/5 and 0.5 at 3/4 | $2p - 1$ | one-step SymPy check |
| Distribution of the maximum 63/256, 105/512 (twice), 15/128 (twice), 45/1024 (twice), 5/512 (twice), 1/1024 (twice); mean 1067/512 = 2.0840; N = 2 gives 3/4, N = 4 gives 19/16 | enumeration of $2^{10}$ paths | reflection principle $P(M = m) = P(S_{10} = m) + P(S_{10} = m + 1)$, and the tail sum $\sum_m P(M \ge m)$ |
| Ruin 3/10 and E[T] = 21 from 3 of 10; 6/15 = 0.4 and 54 from 6 of 15; 4/12 and 32 from 4 of 12; 3/4 and 3 for ends -3 and +1 | $k/N$ and $k(N - k)$ | linear system solved with NumPy (and SymPy for the biased case) |
| $E[S_T^2] = 100 \times 0.3 = 30$, $30 - 9 = 21$ | arithmetic | the same linear solve |
| `stopped_mean` at p = 3/5 for the first hit of +1 capped at 10: 6043193/9765625 | enumeration of the 1024 paths in the solution | backward dynamic programme, and Wald: $0.2\,E[T \wedge 10]$ (equal) |
| `stopped_mean(10, five, 3/5) = 1` | enumeration | $5 \times 0.2$ |
| `exit_stats` values (3/5: 41553/58025 and 48291/2321; 243/275 and 211/11; 1/3: 15/511 and 5727/511; 2/3: 64/85 and 1026/85; 9/10: 729/820 and 131/41) | the two optional-stopping equations | SymPy linear solve of the exact hitting and duration equations (all equal) |
| Die until a 6: 3.5 × 6 = 21 | Wald | NumPy simulation, 200,000 runs, mean 21.005 |
| Review and homework: 8/3 (die), 6, 2 (trend gains on HHHHT), 5 (look-ahead), 2.4, cube martingale, 16/6/4 (atoms), 50/3, 250/7, 500/21 (projection; also $E[X^2] - E[Y^2] = 1000 - 976.19$), 2 and 12 (gains on HTTHTH) | exact `Fraction` | independent formulas (variance split, SymPy for $S_n^3 - 3nS_n$ and the biased-walk martingales) |
| Walk counts in l13 hook (seed 18): 90 of 300 hit 10, average of S_T 3.00; trader screen 225 of 300 hit +1 | the engine's own stream, ported to Node (`seeds.mjs`, which reproduced the seed 5 figure 76 of 300 and mean 2.53 first) | the playthrough screenshot shows "90 hit the top, 210 the bottom (of 300)" and "mean 3" |

The l13 hook's numeric asks where the average settles (3, tolerance 0.5): the engine's seeded value, not a typed canvas count.

## Departures from the brief

- Lesson size as above. The l11 `frames` hook uses `collapse` and `labels` on the tree rather than `dim`, so the visible ends are the atoms.
- l9 uses the `grid` throughout (hook, ladder, trap) and the `tree` only for the lookback transfer; the brief's tree-and-grid hook became the grid alone.
- l10's ladder rung 1 is two screens (the three conditional means; then $E[Y]$, $E[XY]$ and $E[X\,E[Y \mid X]]$), because a three-cell table with a fourth quantity was too dense.
- l11's gains table also asks the look-ahead gain (4) next to the momentum gain (0), and the trap asks the expected 10 over 10 tosses; the `byKey` line names the backtest.
- l13's transfer is a three-cell table (target chance 3/4 and expected trades 3 for ends -3 and +1, and the best-of-4-days backtest, £0.5938) in place of the markov l19 trader (the same trader would repeat markov numbers).
- `stopped_mean` takes a third argument `p` (default 1/2) so the tests are not all 0: a fair-walk-only function would pass by returning 0.
- The brief's homework asked for an `order` of the tower property or Wald; the tower is a lesson screen (l10), so the homework `order` is Wald (difficulty 5). The code item is `exit_stats` (two optional-stopping equations, biased and fair) rather than `doob` on a lookback payoff, which l12 already codes.
- The brief's phrase about "`expression` answers key in the `e^{...}` form" does not arise: no `expression` widget is used (every formula answer was a number or a table), so engine items 501 and 502 are not exercised here.
- Review: 10 items, not the 12 AUTHORING section 11 wants for a level others require (the validator caps reviews at 10). See the inbox.

## course.json

No edit. For the mapping agent, the brief check's proposal stands: add `"random-vars/l17-variance-given-information"` (the variance split in l10) and `"least-squares/l5-dropping-a-perpendicular"` (the projection in l10) to level 3's `requires`, beside `measure-prob/L2`, `markov/L5` and `ito/L2`. Further prerequisites the level leans on, all inside those closures: `random-vars` l15 (the joint table, reused with its numbers), `markov` l17, l19 and l20 (the forecaster, the ruin chance 3/10, E[T] = 21 and the failure at +1), and `trees` l3 and l5 (the tree with $u = 1.2$, $d = 0.8$, $q = 0.625$).

## Inbox

Six bullets under "Raised later (topic 3.2 levels, 4 Nov), measure-prob level 3": one [Should] (review cap of 10 against the 12 that test-out wants for a required level), five [Could] (`tree` `levelLabels` print KaTeX source; `walk` `sq` overlay is centred on the start; `walk` overlay chip prints raw TeX; `grid` `shade` repeats colours beyond six sets; `tree` single-child links print "1"). No [Must]. The planner's inbox bullet "Raised later (brief measure-prob)" (walk stopping rule) is not needed by this level, as R13 says; the main session can withdraw it.
