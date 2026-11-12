# Concept audit, round 2: markov levels 1 to 3

Auditor: blind Fable reader, round 2. Scope: `app/content/courses/markov/` files `l1-only-now` to `l12-price-paths`, `review-1` to `review-3`, `homework-1` to `homework-3` (with the performance task `hw-absorb-code`), `problems-1` to `problems-3` and `fluency-l2-transition-matrix`. Levels 4 and 5 are out of scope. The course is Stage 1, so the ledger has full depth.

Blind rule: the ledger, the findings below and the concepts script were written and committed (commit message "WIP: markov L1-3 round 2 ledger and findings") before any earlier audit, review, ledger, concepts script, author report, git history or diff of the course folder was opened. The overlap section was filled afterwards.

Ledger: `docs/reports/audit-markov-1-3-r2-ledger.md` (240 rows: correct 231, wrong 1, imprecise 8, misleading 0, unverified 0).

Script: `docs/reports/markov-L1-3-concepts-r2.py`, run from the repo root: 1,537 checks, 1 failed, exit 1. The one failing check is finding 1 and fails on purpose; it stays failing until the content is fixed. With finding 1 fixed the script exits 0.

What the script does. It recomputes every numeric key, every `wrong[]` value and every table cell with exact fractions (matrix powers, stationary vectors, the absorption systems `(I - Q)t = 1` and `(I - Q)h = r`). It checks the ruin formula and `D_i = i(N - i)` against the linear systems, and the reflection rule against full enumeration and an exact dynamic programme. It rebuilds the engine's seeded generator (mulberry32, `app/js/engine/sim.js` and `canvas/walk.js`) and reproduces every seeded figure quoted in text: l9 seeds 43 and 61, l10 seeds 11, 6, 28 and 8, l12 seeds 32, 781 and 10, and the 9.995 of homework-2. It runs the six code solutions against their hidden tests (each starter fails) and reproduces the three console values of l5.

## Findings

Pattern: `N. file | JSON path | severity | serious or minor | problem | evidence and basis | exact fix`.

1. `l2-transition-matrix.json` | `quiz[0].feedback.byKey.squared` | wrong | minor | "You squared 0.2. That keeps one path and drops the route that stays in bear first." Squaring 0.2 keeps no path. | From bear to bull in two periods the paths are bear, bull, bull with chance 0.2 × 0.9 = 0.18 and bear, bear, bull with chance 0.8 × 0.2 = 0.16. The square, 0.04, is the chance of neither (script check, fails on purpose). The lesson's own trap (`screens[6].explain`, `summary.trap`) says an off-diagonal square "matches no path", and `screens[3].feedback.byKey.squared` says so for the same slip. Basis: Chapman–Kolmogorov, Norris 1.1. | `quiz[0].feedback.byKey.squared`: "You squared 0.2, which matches no path. Add the two routes: bear, bull, bull and bear, bear, bull."

2. `l2-transition-matrix.json` | `quiz[3].widget.options[3].why` (id `entry`) and `screens[8].feedback.byKey.cubed` | imprecise | minor | Same class as finding 1, in two more lines. "Entry by entry keeps one route through the middle" is true on the diagonal only. "You cubed the entry 0.01, which keeps the impossible path D, D, D from A" says a path is kept where none is. | A route from i to j is (P²)_im (P³)_mj for one middle state m. The entrywise product (P²)_ij (P³)_ij equals the route through m = i when i = j, and no route term when i ≠ j (script, weather chain). The cube 0.01³ is the chance of no path from A. | `quiz[3].widget.options[3].why`: "Entry by entry matches a route only on the diagonal, and none off it. The matrix product adds every route." `screens[8].feedback.byKey.cubed`: "You cubed the entry 0.01, which matches no path at all. Multiply the matrices instead."

3. `l12-price-paths.json` | `screens[6].explain.text`, `screens[9].explain.text`, `summary.ideas[1]`, `quiz[3].prose` | imprecise | minor | "Price" is used for pay-out times the modelled touch chance without the condition that makes it a price. Screen 6 then says the same code "prices a walk with drift". | In `screens[9]` the answer £26.32 is right, because the modelled walk is a fair additive walk and interest is ignored: the walk is itself a fair bet, so the expected pay-out is the replication price. That hypothesis is not stated. With p = 0.55 the expected pay-out of the same one-touch is £41.03, but its price stays £26.32 (script). A learner would carry away "price = pay-out × real-world chance, drift included". `problems-3` `items[1].parts[3].explain` already says it correctly ("A desk would not price with the 0.5: it uses the up-chance that makes the share itself a fair bet"). Basis: Shreve, *Stochastic Calculus for Finance I*, 1.1 to 1.2. | `screens[6].explain.text`, second sentence: "Change the 0.5 to 0.55 and the same code gives the touch chance for a walk with drift, where reflection no longer applies." `screens[9].explain.text`, third sentence, in place of "Drift breaks the symmetry reflection needs, so desks use formulas with drift or simulation.": "Pay-out times chance is the price only when the walk is a fair bet, so with drift desks price with the fair up-chance, by formula or simulation." `summary.ideas[1]`: "The binomial model multiplies by $u$ or $d = 1/u$, so the log price is a simple walk; reflection or simulation gives the chance of a barrier event." `quiz[3].prose`: "A walk steps up with probability $p = 0.55$. A colleague finds a barrier chance with $P(S_n \ge m) + P(S_n > m)$."

4. `l5-where-it-settles.json` | `screens[4].explain.text` | imprecise | minor | "an absorbing state takes all the long-run mass" reads as a rule. It holds only when that state is the chain's one closed class. | In gambler's ruin (l3 `screens[5]`, l8) two absorbing states share the mass, and in l6 `screens[5]` a closed class keeps half of it. Here Default is the only closed class, which is why π = (0, 1). Basis: Norris 1.7; l6 `summary.ideas[1]` states the rule correctly. | Second sentence of `screens[4].explain.text`: "So $\pi = (0, 1)$: Default is the only closed class, so it takes all the long-run mass."

5. `l11-reflection.json` | `screens[3].explain.text` | imprecise | minor | The count formula is given "for an end at or below the level, $k \le m$". It also needs the level to be above the start. | For a level below the start the formula miscounts: n = 4, m = −2, k = −4 has 1 path, all of which touch −2, and the formula gives C(4, 2) = 6 (script). Screen 9 and problems-3 use a level below the start, correctly, by turning the rule upside down, so the hypothesis matters in this course. Basis: Feller vol. 1, III.1. | In `screens[3].explain.text` replace "For an end at or below the level, $k \le m$:" with "For a level above the start, $m > 0$, and an end at or below it, $k \le m$:".

6. `l11-reflection.json` | `screens[9].feedback.correct` | imprecise | minor | "the 0.25 chance of ending beyond the limit": 0.2517 is the chance of ending at or beyond it. | P(S_20 ≤ −4) = 0.2517 and P(S_20 < −4) = 0.1316 (script). Strict against non-strict is the whole point of this lesson's rule, so the word matters here. | `screens[9].feedback.correct`: "About 0.38, half as much again as the 0.25 chance of ending at or beyond the limit."

7. `l10-gamblers-ruin.json` | `screens[4].explain.text`, `screens[5].widget.options[0].why`, `summary.trap` | imprecise | minor | "the game lasts thousands of bets", "Over thousands of bets", "repeated thousands of times". The expected length is about 1,900 bets. | For p = 0.49, i = 50, N = 100 the expected duration is (i − N P_i)/(q − p) = (50 − 11.917)/0.02 = 1,904 bets, and the linear system agrees (script). Basis: Feller vol. 1, XIV.3, equation (3.4). | `screens[4].explain.text`, second sentence: "A 2-point edge per bet cuts the chance from 0.5 to under 0.12, because the game lasts about 1,900 bets on average." `screens[5].widget.options[0].why`: "You expected small bets to smooth out the edge. Over about 1,900 bets the edge compounds: 0.1192 against 0.49." `summary.trap`: "A small edge is not harmless. A 49% bet repeated about 1,900 times turns a 50% chance into under 12%."

8. `l12-price-paths.json` | `screens[3].explain.text` (and the slip `daily`, 0.48) | imprecise | minor | "One day alone is close to a coin flip: $\Phi(-0.05) \approx 0.48$" uses a normal daily return on the screen that opens "Daily returns need not be normal". | The central limit theorem says nothing for n = 1; the 0.48 holds if one day's return is itself normal. Basis: Lindeberg–Lévy theorem is a statement about large n. | Last sentence of `screens[3].explain.text`: "If one day's return is normal too, one day is close to a coin flip: $\Phi(-0.05) \approx 0.48$."

Totals: 8 findings. By severity: wrong 1, imprecise 7, misleading 0. By tag: serious 0, minor 8.

## Checked and found sound

These are the classes the brief asked for by name. Each was read line by line; none gave a finding beyond those above.

- Row against column convention: stated at first use (l2 `screens[0]`), used the same way throughout, and the column form is contrasted correctly (l2 `screens[7]`, `quiz[2]`; l5 `screens[5]`).
- Unique stationary distribution and convergence: l6 states the theorem for a finite chain that is irreducible and aperiodic, keeps "irreducible alone gives a unique π as a share of time" apart from convergence, and says a single closed class still gives one π. The two-state formula carries a + b > 0.
- Transient and recurrent: the "can reach a state that cannot reach back" test is given its finite-chain hypothesis for the converse (l3 `screens[8]`, `summary.ideas[1]`).
- Absorption equations: `t` and `h` range over the transient states with the right boundary values; the infinite case and the "both ends worth 1" trap are right.
- Gambler's ruin, fair and unfair, the limit N to infinity (p ≤ 1/2 against p > 1/2) and bold play.
- Reflection: non-strict then strict, parity used correctly in every item, fair steps required, the drifted case handled by dynamic programming or the tilted formula.
- Independence: variance results use independence as a sufficient condition, and l9 `screens[6].explain` says "uncorrelated steps would be enough". No line states it as necessary.
- Seeded figures and console values: all reproduced digit for digit.
- Real-world facts: the stylised facts of returns (Cont 2001), GARCH, the single-zero roulette wheel. None left unverified.

## Gates

- Validator, from `app/`: `node tools/validate.mjs`: 0 errors, 5,023 warnings (repository-wide). `app/content/manifest.json` restored afterwards.
- `docs/reports/problems-markov-numbers.py`: exit 0 (1,815 checks, 0 failures).
- `docs/reports/fluency-markov-numbers.py`: exit 0 (1,788 checks over 3 families, 0 failures).
- `docs/reports/markov-2-perf-numbers.py`: exit 0 (0 failures).
- `docs/reports/markov-L1-3-concepts-r2.py`: exit 1 (1,537 checks, 1 failed on purpose: finding 1).
- Playthrough of the in-scope files only, with `--local-cdn`: 12 lessons, 6 sets, 3 problem sets and the fluency set. Desktop: all passed, exit 0. `--mobile`: see the overlap section's closing note.

## Overlap with earlier reads

To be filled after the WIP commit.

## Inbox

- Concept lint (validator or script): list every content string that contains "fair price" or "prices" next to a probability, so a reader can check that the model is a fair bet (risk-neutral) or that the text says "expected pay-out". Seen in markov l12 (finding 3).
