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
- Playthrough of the in-scope files only, with `--local-cdn`: 12 lessons, 6 sets, 3 problem sets and the fluency set. Desktop: all passed, exit 0. `--mobile`: all passed, exit 0.

## Overlap with earlier reads

Read after the WIP commit `87bb8ab2`: the round 1 audit `docs/reviews/audit-markov-1-3.md` with its Fix pass, Fix-pass read and Follow-up, its ledger `docs/reports/audit-markov-1-3-ledger.md`, `docs/reviews/review-1.5.md` (section "markov"), `docs/reviews/review-problems-1.5-c.md` (markov sets 1 to 3) and `docs/reviews/review-perf-retrofit-8.md` (markov `hw-absorb-code`).

Earlier conceptual findings in this scope: 21. Round 1 audit, 16 (2 wrong, 12 imprecise, 2 misleading). Fix-pass read, 1 (l4 `screens[10].feedback.byKey.total`). `review-1.5.md`, 2 (l2 "half again the A route"; l12 "a 6.5% fall on day 71"). `review-problems-1.5-c.md`, 2 (`p-rfq-rounds` prose; `p-merger-arb` part 5). All 21 were fixed before this read, so none could be found again. I read each fixed text blind, and each is a `correct` row in my ledger (rows 7, 10, 25, 42, 44, 64, 85, 91, 108, 110, 114, 139, 148, 165, 181, 207, 219 and 236; row 192 holds for round 1's hypothesis and is finding 5 for another).

| | count |
|---|---|
| Conceptual findings, this read only | 8 |
| Conceptual findings, earlier reads only (all already fixed) | 21 |
| Found by both | 0 |

Each finding of this read against the earlier reads, stated plainly:

1. Finding 1 (`wrong`, l2 `quiz[0].feedback.byKey.squared`): **no earlier read found it.** The round 1 ledger has one row for l2 `q[0]` (key and slip values, `correct`) and does not judge the feedback line. This is the one new `wrong` for the convergence rule.
2. Finding 2 (imprecise, l2 `quiz[3]` option `entry` and `screens[8]` `cubed`): no earlier read found it. Round 1 rows for `q[3]` and `s[8]` are `correct`.
3. Finding 3 (imprecise, l12 "prices"): no earlier read found it. It is the class of round 1 finding 3 (problems-3 "fair price"), in another file. Round 1 and the fix-pass read both judged l12's one-touch number sound because the walk is a fair bet; I agree, and the key is unchanged. Neither read the `screens[6]` sentence "prices a walk with drift" or asked that the hypothesis be said.
4. Finding 4 (imprecise, l5 `screens[4]`): no earlier read found it (round 1 row `correct`).
5. Finding 5 (imprecise, l11 `screens[3]` formula): related to round 1 finding 10, which fixed the same sentence for the other missing hypothesis (k ≤ m). The fix-pass read saw the m > 0 point and passed it ("The lesson's levels are all above the start"). Screen 9 of the same lesson and problems-3 use a level below the start, so I keep it. Counted as this read only.
6. Finding 6 (imprecise, l11 `screens[9].feedback.correct`): no earlier read found it.
7. Finding 7 (imprecise, l10 "thousands of bets"): round 1 saw the phrase and judged it `correct` ("mean 1,904 bets, loosely thousands"). The two reads differ on a matter of wording; the fix costs nothing and states the computed figure.
8. Finding 8 (imprecise, l12 `screens[3]`): no earlier read found it (round 1 row `correct`).

New `wrong` that no earlier read found: 1 (finding 1, minor). New findings of any severity that no earlier read found: 8, all minor.

## Inbox

- Concept lint (validator or script): list every content string that contains "fair price" or "prices" next to a probability, so a reader can check that the model is a fair bet (risk-neutral) or that the text says "expected pay-out". Seen in markov l12 (finding 3).

## Fix pass

Fixer: Opus fix pass. Each basis was worked out without the auditor's text. No graded key, `wrong[]` value or hidden test changed.

1. **Fixed with different text.** l2 `quiz[0].feedback.byKey.squared`: "You squared 0.2, which matches no path: after a step to bull, the next step uses row bull. Add the routes bear, bull, bull and bear, bear, bull." The added clause says why 0.04 is no path. Basis: the two paths from bear to bull are 0.2 × 0.9 = 0.18 and 0.8 × 0.2 = 0.16, and 0.2² would need a bear-to-bull step from bull (Chapman–Kolmogorov, Norris 1.1). The script check for this finding now reads the content string instead of a fixed false claim, so it passes; two checks were added for finding 2 (1,539 checks).
2. **Fixed with different text.** l2 `quiz[3]` option `entry` `why`: "Entry by entry gives one route on the diagonal and no route off it. The matrix product adds every route through the middle." `screens[8].feedback.byKey.cubed`: "You cubed 0.01, which matches no path: once in D the loan stays, so A, D, D, D has chance 0.01. Multiply the matrices instead." The new `cubed` line names what the real path's chance is (0.01, not 0.01³). Basis: a route is (P²)_im (P³)_mj; the entrywise term (P²)_ij (P³)_ij equals the m = i route when i = j and no route when i ≠ j (checked on a random 3-state chain); 0.01³ = 10⁻⁶ would need three A-to-D steps.
3. **Fixed with different text.** l12. `screens[6].explain`: "Set the 0.5 to 0.55 and the code finds the touch chance with drift, where reflection fails." `screens[9].explain`: "The touch chance is $0.1316 + 0.1316 = 0.2632$; here 10 of 40 paths touched. The walk is a fair bet with no interest, so the fair price is the expected pay-out: £26.32. Desks price with the up-chance that makes the walk fair, whatever its real drift." I did not use the audit's "is the price only when the walk is a fair bet", which states the hypothesis as necessary; mine states it as the reason here. The volatility sentence was dropped to keep three sentences. Sibling: `screens[9].hints[0]` (nudge) now reads "With a fair walk and no interest, the price is £100 times the chance of touching $+5$ within 20 steps." `summary.ideas[1]` and `quiz[3].prose` as the audit proposed. The key £26.32 still follows: the item says fair walk and ignore interest. Basis: for an additive ±1 step with r = 0 the replicating up-chance is (S − (S − 1))/((S + 1) − (S − 1)) = 1/2 whatever the real p (Shreve, *Stochastic Calculus for Finance I*, 1.1, risk-neutral probabilities), so price = expectation under the fair walk.
4. **Fixed with different text.** l5 `screens[4].explain`: "So $\pi = (0, 1)$: Default is the only closed class, and it takes all the long-run mass." (avoids the double "so"). Basis: a stationary distribution of a finite chain puts no mass on transient states (Norris 1.7); Performing is transient, so all mass is on the one closed class.
5. **Fixed.** l11 `screens[3].explain`, as proposed. Basis: enumeration of all ±1 paths for n ≤ 10: the formula matches for every m > 0 (and m = 0) with k ≤ m and n + k even, and fails for m < 0, for example n = 4, m = −2, k = −4 gives 1 path against C(4, 2) = 6.
6. **Fixed.** l11 `screens[9].feedback.correct`, as proposed. Basis: exact binomial: P(S₂₀ ≤ −4) = 0.2517, P(S₂₀ < −4) = 0.1316; touch chance by dynamic programme 0.3833, 1.52 times 0.2517, so "half as much again" stands.
7. **Fixed with different text.** l10 `screens[4].explain`: "A 2-point edge cuts the chance from 0.5 to under 0.12, because the average game lasts about 1,900 bets." `screens[5]` option `small` `why`: "You expected small bets to smooth out the edge. Over about 1,900 bets on average the edge compounds: 0.1192 against 0.49." `summary.trap`: "A small edge is not harmless. A 49% bet, played about 1,900 times on average, turns a 50% chance into under 12%." Shorter than the audit's to keep sentences under 20 words, with "on average" kept since the length is random. Basis: (I − Q)t = 1 solved for N = 100, p = 0.49 gives t₅₀ = 1,904.13, equal to (i − N·P_i)/(q − p) with P_i = 0.11917.
8. **Fixed.** l12 `screens[3].explain`, as proposed. Basis: the CLT is a limit statement and says nothing at n = 1; with a normal daily return, mean 0.05% and sd 15.81%/√250 = 1.00%, Φ(−0.05) = 0.480.

Totals: 8 fixed (5 with different text), 0 disputed, 0 not applied. Sibling fix: l12 `screens[9].hints[0]`.

Gates: concepts-r2 exit 0 (1,539 checks), concepts, problems, fluency and markov-2-perf scripts exit 0; validator 0 errors (manifest unchanged); voice scan 35: 0 and 0; playthrough of l2, l5, l10, l11 and l12, desktop and `--mobile`, all passed.

## Fix-pass read

Commit read: `ac8f1d97`, `app/content/courses/markov/` only (l2, l5, l10, l11, l12; 15 changed strings, 16 sentence rows). Read blind: no audit, report, concepts script or review file opened. Each string was judged in its screen as it now stands. Script: `docs/reports/markov-L1-3-fixread-r2.py` (42 checks, exit 0); it recomputes every number below by a second route and runs the voice gate on the changed strings.

| # | File | JSON path | Claim | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | l2-transition-matrix | screens[8].feedback.byKey.cubed | 0.01 cubed matches no path; A, D, D, D has chance 0.01 | correct | Enumerated the seven 3-step paths A to D from the item's matrix: chances 0.000045, 0.00765, 0.0081, 0.0081, 0.009, 0.009, 0.01, sum 0.051895. None is 0.000001. A, D, D, D is 0.01 x 1 x 1. Slip value 1e-06 is 0.01 cubed. |
| 2 | l2-transition-matrix | quiz[q-two-step].feedback.byKey.squared | 0.2 squared matches no path; the routes are bear, bull, bull and bear, bear, bull | correct | Two-step paths from bear: 0.18, 0.02, 0.16, 0.64; none is 0.04. After a step to bull the row is (0.9, 0.1), so 0.2 cannot be used twice. 0.18 + 0.16 = 0.34, the key. Agrees with the `one-path` and `other` lines. |
| 3 | l2-transition-matrix | quiz[q-chapman].options[entry].why | Entrywise product gives one route on the diagonal, none off it | correct | (P^2 P^3)_ij sums P^2_ik P^3_kj over k. The entrywise value P^2_ij P^3_ij equals the k = i term when i = j; for i not j no k gives it. Checked on both lesson matrices. |
| 4 | l5-where-it-settles | screens[4].explain.text | Default is the only closed class, and it takes all the long-run mass | correct | Finite chain: mass leaves transient states and stays in closed classes (Norris, Markov Chains, 1.5 and 1.8). One closed class here, so pi = (0, 1). With two absorbing states the mass splits (0.4 and 0.6 in a test chain), so "only" carries the hypothesis. "Closed class" is defined in l3. 0.97^100 = 0.0476. |
| 5 | l10-gamblers-ruin | screens[4].explain.text | 2-point edge cuts 0.5 to under 0.12, because the average game lasts about 1,900 bets | correct | P_50 = 0.11917. Duration i/(q-p) - (N/(q-p))P_i = 2500 - 5000 x 0.11917 = 1904.1; a linear solve of D_j = 1 + pD_{j+1} + qD_{j-1} gives the same (Feller vol. I, XIV.3). 0.51 - 0.49 is 2 points. |
| 6 | l10-gamblers-ruin | screens[5].options[small].why | Over about 1,900 bets on average the edge compounds | correct | Same item setting (£1 bets, £50 to £100, p = 0.49); 1904.1 as row 5. 0.1192 against 0.49 matches the canvas. |
| 7 | l10-gamblers-ruin | summary.trap | A 49% bet, played about 1,900 times on average, turns 50% into under 12% | correct | Row 5. Agrees with summary idea 2 and the screen. |
| 8 | l11-reflection | screens[3].explain.text | For m > 0 and k <= m, paths to (n, k) touching m number C(n, (n + 2m - k)/2) | correct | Enumerated all walks for n <= 10, every m > 0 and k <= m of the right parity: all match (the count is 0 when the index passes n). k = m gives every path to (n, m). The condition is needed: for m = -1, k = -2, n = 4 the true count is 4, the formula gives 6. Feller vol. I, III.1. |
| 9 | l11-reflection | screens[9].feedback.correct | 0.38 is half as much again as the 0.25 chance of ending at or beyond the limit | correct | P(S_20 <= -4) = 0.25172, which includes ending exactly at the limit, so "at or beyond" is the right wording. Touch chance by exact recursion 0.38331; ratio 1.523. Agrees with the `generic` and `end-only` lines. |
| 10 | l12-price-paths | screens[3].explain.text | If one day's return is normal too, one day is close to a coin flip, 0.48 | correct | Daily mean 0.05%, sd 15.81/sqrt(250) = 1.0%, z = -0.05, Phi = 0.4801. The new condition is needed, since the prose says daily returns need not be normal. |
| 11 | l12-price-paths | screens[6].explain.text | Set 0.5 to 0.55 and the code finds the touch chance with drift, where reflection fails | correct | The solution's `rng.random() < 0.55` steps up with chance 0.55. Exact touch chance (n = 20, m = 5) 0.410 against the reflection sum 0.504. "Finds" means "estimates", as the first sentence's standard error says. se = 0.0034. |
| 12 | l12-price-paths | screens[9].hints[0].text | With a fair walk and no interest, the price is £100 times the touch chance | correct | Price in unit steps, r = 0: risk-neutral q = (0 - (-1))/(1 - (-1)) = 1/2, the item's own walk (Hull, Binomial trees; Shreve vol. I, 1.2). Both hypotheses are stated. |
| 13 | l12-price-paths | screens[9].explain.text, sentences 1 and 2 | Touch chance 0.2632; fair bet with no interest, so the fair price is the expected pay-out, £26.32 | correct | P(S_20 >= 6) = 0.13159; exact recursion gives 0.26318 = 2 x 0.13159; £100 x 0.26318 = £26.32, the key. In this complete model with the price a martingale the replication price equals the expected pay-out. Hypotheses stated. |
| 14 | l12-price-paths | screens[9].explain.text, sentence 3 | Desks price with the up-chance that makes the walk fair, whatever its real drift | imprecise | See finding 1. True when "the walk" is the price and interest is nil. In the lesson's own binomial model the walk is the log price, and the pricing up-chance does not make that walk fair. |
| 15 | l12-price-paths | summary.ideas[1] | Reflection or simulation gives the chance of a barrier event | correct | Chance, not price, which matches the screens. The fair-steps limit on reflection is stated on screens[6] and in q-drift-reflect. |
| 16 | l12-price-paths | quiz[q-drift-reflect].prose | A colleague finds a barrier chance with P(S_n >= m) + P(S_n > m) at p = 0.55 | correct | Wording change only; the item's key (reflected path has a different probability) holds: 0.410 against 0.504 for n = 20, m = 5. |

Counts: 16 rows. correct 15, imprecise 1, wrong 0, misleading 0, unverified 0.

Voice on the changed strings: no exclamation marks, no em-dashes, longest sentence 26 words, no explanation over three sentences, no lesson numbers, British spelling. No slip line names a value other than its slip's.

### Finding

1. l12-price-paths.json | screens[9].explain.text, third sentence | imprecise | serious | "Desks price with the up-chance that makes the walk fair, whatever its real drift" is true only if "the walk" is the price itself and interest is nil. This screen models the price as a unit-step walk, so there it holds. But the lesson's own binomial model, and its summary, make the walk the log price ("multiplies by $u$ or $d = 1/u$, so the log price is a simple walk"). A learner will read the sentence as "price with a fair log walk", or "keep the equal chance". That is not the pricing rule. | Hull, Binomial trees: $p = (e^{r\Delta t} - d)/(u - d)$. With no interest and $d = 1/u$ this is $1/(1 + u)$, below one half: 0.4975 for $u = 1.01$, 0.4545 for $u = 1.2$. For the lesson's $u = 1.25$, $d = 0.8$ model it is $0.2/0.45 = 0.444$, not the 0.5 the lesson uses. Under that chance the price is a fair bet ($qu + (1-q)d = 1$) and the log walk drifts down. Shreve vol. I, 1.2 states the same: the discounted price, not the log price, is the martingale. Script checks `l12 multiplicative tree`. The dropped hypotheses are "the price" and "after interest". Tagged serious because it leaves a wrong pricing rule in the one model the lesson names; the size of the error is small for small steps. | Replace the third sentence with: "Desks price with the up-chance that makes the price itself a fair bet after interest, whatever its real drift." (19 words; the first two sentences stay.)

## Follow-up (fix-pass read)

One row changed, `l12-price-paths.json` `screens[9].explain.text`, third sentence.

- Old: "Desks price with the up-chance that makes the walk fair, whatever its real drift."
- New: "With no interest, desks price with the up-chance that makes the price itself a fair bet, whatever its real drift."

Basis: Hull, Binomial trees, and Shreve vol. I, 1.2: the pricing chance makes the discounted price, not the log price, a martingale; with no interest that is q = (1 − d)/(u − d), 4/9 for u = 1.25, d = 0.8 (qu + (1 − q)d = 1), and 1/2 for this screen's unit-step price walk. The reader's "after interest" was not used, since the lesson only says "Ignore interest"; the condition is stated instead, and "fair bet" is already the screen's own term.

Siblings checked, no change: `screens[9].hints[0]` and `screens[9].explain.text` sentence 2 speak of the item's walk, which is the price itself, with no interest, so both hold; `screens[6]`, `summary.ideas[1]` and `quiz[q-drift-reflect]` state chances, not prices. Key £26.32 recomputed twice: 2 × P(S_20 ≥ 6) = 2 × 0.131588 and an absorbing-barrier recursion 0.263176, × £100 = £26.32. Gates: six scripts exit 0, validator 0 errors, voice scan 0 and 0, playthrough green with and without `--mobile`.
