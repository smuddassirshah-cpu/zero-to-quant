# Report: measure-prob level 2, "Integration" (topic 3.2)

Brief: `docs/briefs/measure-prob.md`, `## Level 2`, with the brief-check corrections applied: R11 (the moving spike and the typewriter are `plane` `steps` lists with `index`, entries for n = 1 to 20 and 1 to 15), and the stale facts (analysis L1 to L4, markov L5 and ito L1 written; analysis l20 not written; the planner's scripts are gone, so every number was recomputed). Ids, names, objectives and skill (`mt-integral`) as in `course.json`.

## Files written (`app/content/courses/measure-prob/`)

| File | Screens | Quiz | Canvases and widgets |
|---|---|---|---|
| `l5-lebesgue-integral.json` | 11 | 4 | `plane` (bands $\varphi_n$ with a control on n and a `sum()` caption; layer-cake area), `bars`, `console`, `code` (`dyadic_mean`, `simple_mean`), `choice` derive (no `order` proof in this lesson) |
| `l6-monotone-convergence.json` | 9 | 4 | `plane` (cap with density), `bars`, `series`, `order` (MCT proof), `choice` derive (Fatou), `code` (`tail_sum_mean`, `years_to_reach`), `table` |
| `l7-dominated-convergence.json` | 10 | 4 | `plane` with `steps` + `index` (spike), `plane` (payoff, bump), `order` (DCT from Fatou), `table`, NumPy `code` (`pathwise_delta`, `digital_pathwise`) |
| `l8-modes-of-convergence.json` | 11 | 4 | `plane` `steps` + `index` (typewriter, spike), `distribution`, `series` (tree), `table` (yes/no chart), `multi`, `order` (Chebyshev), `code` (`typewriter`, `hits`, `prob_nonzero`) |
| `review-2.json` | 10 items, difficulty 2 to 4 | | l5 three, l6 three (one `parts`), l7 two plus one shared, l8 two |
| `homework-2.json` | 9 items, difficulty 3 to 5 | | `parts` (tranche, Fatou counterexample, `nU^n`), numeric, `order` (Fatou from MCT), `expression`, `table`, `code` d5, `longform` d5 (rubric 10) |

## Validator, playthrough, voice

- `node tools/validate.mjs`: 0 errors. Warnings in the whole repo went from 557 (with an early draft of l5) to 548, the figure before this level: none of the six files has a warning.
- Playthrough with `--local-cdn`, desktop and `--mobile` (390 px, no sideways scroll): l5 15 checks, l6 13, l7 14, l8 15, every quiz 4 of 4; `review-2` 10 of 10 recorded; `homework-2` 9 of 9 items, 41 of 41 marks, parts checks ok. All passed in both modes. Screenshots looked at (hook, ladder, trap, code, transfer, tables at 390 px).
- Voice (`docs/reviews/voice-scan.py`, whole course folder): 0 sentences over 20 words, 0 explanations over three sentences. No `!`, no em-dash.
- Code: `scratchpad/measure-prob-2/codecheck.py` (CPython, with `prelude`): every solution passes all its tests (11, 10, 8, 13 and 9) and every starter passes none. The app's playthrough runs the same solutions in Pyodide.
- NumPy: the l7 code screen (import, 100,000 draws, 8 tests) took 1.1 s on the local CDN once the page had been open 6 s; over jsDelivr the first import adds the package download. Every NumPy `how` says the first run loads NumPy.

## Lesson size: which rungs moved

- l5 (11 screens): hook is a single numeric ($E[\varphi_1]$) then an explore; the linearity and monotonicity rung is one `choice` derive on monotonicity; the edge case (zero except on a null set, equal almost surely) is the Dirichlet screen; the St Petersburg truncation and the trap are separate screens.
- l6 (9): the dividend ladder rung is the transfer screen (a two-cell table: £40 and 78 years); the tail-sum rung is a `problem`, not a `ladder`, because the validator wants a ladder to keep the canvas kind; the infinite-limit edge case has its own screen.
- l7 (10): the call rung is a two-cell table (E[Y] = 1 and delta 0.6368); the digital is split into a ladder (the pathwise derivative is 0) and the trap (the true delta 0.0188); the bounded-convergence edge case stays a screen; the transfer asks for the number of standard errors.
- l8 (11): the typewriter in mean square is a numeric ($\tfrac1{64}$), the spike a two-cell table; the reflection $-Z$ is a `problem` (its distribution function) followed by the trap; the edge case (convergence in distribution to a constant) moved to the quiz; the chart is a four by three yes/no table, then a `multi` on the implications.

## Proof steps and the widget that grades each

- l5: monotonicity passes to the supremum, `choice` (derive).
- l6: monotone convergence, `order` with `same` on the first two lines and two distractors ("$X_n = X$ for large $n$", continuity from above); Fatou from it, `choice` (why monotone convergence applies to $Y_n = \inf_{k \ge n} X_k$).
- l7: dominated convergence from Fatou, `order` with two distractors ("apply monotone convergence", "cancel $E[Y]$ even if infinite").
- l8: mean square implies in probability (Chebyshev), `order` with two distractors (an equality, a jump to almost sure).
- homework: Fatou from monotone convergence, `order` with `same` and two distractors; the dominated convergence proof, the pathwise delta and the digital's failure, `longform` (rubric 10).

## Numbers and two routes

| Value | Route 1 | Route 2 |
|---|---|---|
| $E[\varphi_n]$: 0.1464, 0.2317, 0.2794, 0.3052, 0.3188, 0.3259, $\tfrac13$; gaps 0.187, 0.102, 0.054, 0.028, 0.0145, 0.0074; 0.279370 at n = 3, 0.325917 at n = 6, 0.0019 at n = 8 | the band sum $\sum_k \tfrac{k}{2^n}(\sqrt{(k+1)/2^n} - \sqrt{k/2^n})$ | SciPy `quad` of $\lfloor 2^n x^2 \rfloor / 2^n$ with breakpoints at the band edges (agree to 6 places); closed form $\tfrac12(1 - 1/\sqrt2)$ at n = 1 |
| £5.50, £13, £7 | exact `Fraction` sum | decimal sum |
| layer cake $\tfrac13$, $\tfrac12$ ($(1+t)^{-3}$), 0.2 (from 4 of $(1+t)^{-2}$) | antiderivative | SciPy `quad` |
| St Petersburg $m + 1$ (11 at m = 10), £20.9073 for the £1m cap | exact `Fraction` series ($19 + 10^6/2^{19} = 171273/8192$) | floating sum to k = 80 and the closed form |
| tranche £1.3534m ($10e^{-2}$); mean £8m tranche 10 to 25: £1.9405m and $P(L > 25) = 0.0439$ | closed form | SciPy `quad` (the second also by integrating $\min((l - 10)^+, 15)$ against the density) |
| capped holding time 0.7869, 1.2642, 1.7293, 1.9865, limit 2 | $2(1 - e^{-n/2})$ | SciPy `quad` of $\min(x, n)$ against the density |
| tail sums 5, 4, 2, 3 ($1.5^K$) | geometric series | summed 500 terms |
| dividend £40, partial sum £39.0085 at n = 78 (£38.9603 at 77), 77.82; £60 and year 63 ($S_{63} = 57.057$, 62.60); year 15 at half | closed form $d/(r-g)$, $\ln$ solution | accumulation loop in floating point |
| $E[U^9] = 0.1$, $E[U^{19}] = 0.05$, $E[nU^n] = 0.95$ | $1/(n+1)$ | SciPy `quad` |
| $d_1 = 0.35$, $\Phi(0.35) = 0.636831$, $\Phi(0.15) = 0.559618$, call £10.4506, call delta, digital delta 0.018762 and $\varphi(0.15) = 0.394479$ | closed form with `math.erf` | SciPy `norm`; central finite differences of the Black-Scholes price (0.6368306512 and 0.0187620173) |
| pathwise call delta 0.635956, standard error 0.001822 (seed 7, 100,000) | CPython NumPy 2.5.3 | the same tests pass in Pyodide (NumPy 2.0.2) at relative 1e-6, in the playthrough |
| LR digital 0.018679 (se 0.000088), LR call 0.631907 (se 0.004577) on seed 7; z-score 0.94 | NumPy | the same, in Pyodide; z from the two printed values (0.9400) |
| K = 110 call delta 0.44965 (seed 11, 50,000: 0.45055, se 0.00264); K = 110 digital delta 0.017989 (seed 13, 200,000: 0.018001, se 0.000063, 0.18 se) | closed form | simulation within three se |
| typewriter: 4 hits to N = 15 (n = 1, 2, 5, 10), 10 to N = 1,023, 4 for $\omega = 0.7$ (n = 1, 3, 6, 13); $\tfrac18$ at n = 10, $\tfrac1{64}$ at n = 100 | block construction | brute force over n; the plane entries were asserted against the definition at four points for n = 1 to 15 |
| $P(|{-Z} - Z| > 1) = 0.6171$ ($2(1 - 0.691462)$), $\Phi(1) = 0.8413$ | $\Phi$ by `erf` | SciPy `norm` |
| CRR prices 10.2534, 10.3513, 10.4107, 10.4306, 10.4406, 10.4466, 10.4486 at 10, 20, 50, 100, 200, 500, 1,000 steps; gaps 0.0200 and 0.0040, factor 5 | binomial sum with log-gamma weights | backward induction; Black-Scholes 10.4506 |
| Chebyshev 0.16 and 0.25 | arithmetic | arithmetic |

Walk and bars simulations are not used for any typed number. The bump in l7's digital screen is drawn from the delta (height times width 0.018762), not simulated.

## Departures from the brief

- Lesson size as above; the brief's more than twelve tasks per lesson do not fit, so the moved rungs are listed.
- l7 hook asks a two-cell table (the value at $U = 0.3$ is 0, the mean is 1) instead of "the two numbers"; the call delta screen asks $E[Y] = 1$ as well as the delta, because the delta alone is a table lookup.
- l7's digital screens use an illustrative bump in the quantile space of the scenarios (area about 0.0188), not a simulated difference quotient.
- l5 hook has $E[\varphi_1]$ first and the slider after it, as the brief says, on two screens.
- The brief's analysis l19 triangle is not cited by name: l7 and l8 say "the spike of the last lesson" and l5 states the one fact it takes from analysis l20 (the Dirichlet function has no Riemann integral) in one sentence.
- l8 uses a transposed chart (modes as rows) so that four columns fit at 390 px.
- No expression answer uses `\exp` (P32-expr-exp is open): the E[min(X, n)] formula is a numeric, and the homework expression item is the geometric partial sum.

## course.json

No edit. For the mapping agent: level 2 inherits level 1 (`measure-prob/L1`) and uses the rationals having chance 0 and continuity from below (level 1). It quotes numbers from `trees` l9 and l10 (Φ(0.35), Φ(0.15), the CRR prices; one reader should confirm `trees` is in the closure of `ito/L1`) and mentions `limits-thm` l11 and `analysis` l20 in one sentence each (no dependence on their content). Proposed, as the brief check says: `"requires": ["measure-prob/L1"]` explicitly, and optionally `"trees/l10-black-scholes"`. `analysis/l19-uniform-convergence` is not needed.

## Inbox

Three bullets under "Raised later (topic 3.2 levels, 4 Nov), measure-prob level 2": a `table` cell's `wrong[]` id is not a valid `byKey` key although AUTHORING says it is [Should]; `plane` `steps` drops `at` values at the range ends silently [Could]; a long `plane` x title prints over a `derive` caption [Could]. No [Must].
