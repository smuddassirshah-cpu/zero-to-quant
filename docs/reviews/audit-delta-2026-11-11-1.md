# Concept audit, delta batch 1 of 11 November 2026

Blind delta audit of content added or changed after each course closed: puzzles, game-theory, brainteasers, coding-int, research-int, systems, ito (levels 2 and 3) and measure-prob (levels 1 to 3). Scope is the changed items only, read from `git diff <close> HEAD` with each whole item and its lesson context. Twenty-seven files, 28 items (24 new, 4 edited).

- Ledger: `docs/reports/audit-delta-2026-11-11-1-ledger.md` (349 rows).
- Script: `docs/reports/delta-2026-11-11-1-concepts.py` (85 checks; exits 1 because three checks fail on findings C1, R1 and R2 below; it exits 0 once they are fixed).
- Finding pattern: `N. file | JSON path | severity | serious or minor | problem | evidence and basis | exact fix`.

Code items were run, not only read. The three Python tasks ran their hidden tests under Python 3 against the solution and the starter, and against an independent second implementation. The C++ ring was compiled with g++ 13 against its twelve hidden tests, stressed with two threads across the counter wrap, and run under ThreadSanitizer with no report.

## puzzles

No findings. The Kelly derivation (`homework-4.json` `items[9]`) holds line by line: hypotheses, the strong-law step, concavity, existence and uniqueness of the maximum, the numbers, the zero of $g$ at 0.513 and the long-shot example. The two review items and all four slip values are right, and no slip is right under another method.

## game-theory

1. `review-2.json` | `items[9].prose` | imprecise | minor | "Each round of deletion removes every guess above the current bound." Read as written, a round removes nothing, since no surviving guess is above the current bound. The round removes the guesses above half of it. | The key, feedback and explain all use the bound $100 \times 0.5^k$ after round $k$ (Osborne, *An Introduction to Game Theory*, sec. 12.2, iterated elimination). Only the prose misstates the step. | Replace the prose with: "Guesses run from 0 to 100, and the target is half the average. The bound starts at 100. Each round of deletion removes every guess above half the current bound, and that half becomes the new bound."

The street-carts task passes: the solution passes its nine hidden tests, the starter fails all nine, and tables and best replies agree with an exact-fraction version on 300 random streets. The mixed value in `review-1.json` was recomputed (no pure equilibrium, $q = \tfrac25$, value 2.2, Ben 1.5). The edit to `hw1-say-it` is layout only.

## brainteasers

No findings. Every one of the 304 placements of an L-tetromino on the 6 by 10 board is 2 and 2 on the chessboard and 3 and 1 on column stripes and on row stripes. The hats plan passes its tests; an exhaustive search over every plan at $n = 3$ and $n = 4$ confirms that no plan beats $\lfloor n/2 \rfloor$, so the equality tests are sound. Breadth-first search gives 6 steps for the jugs and 8 when the 7 is filled first.

## coding-int

1. `homework-3.json` | `items[8].feedback.byKey.test-6` | wrong | minor | "Test 6 asks for three moves that must be refused." The test holds four refused moves. | `tests[5]` calls `mv('/a', '/b')`, `mv('/a', '/a/k/l')`, `mv('/', '/z')` and `mv('/a/f', '/b/g')`, and expects `False` four times. The script check fails on this count. | "Test 6 asks for four moves that must be refused. Check every refusal before you make any folder for `dst`."

2. `homework-4.json` | `items[8].widget.rubric[3].text` | imprecise | minor | The required row demands that you "said why `target - x` is looked up before `x` is counted". That reason belongs to the one-pass plan only. A correct plan that counts every value first, then adds $c_v c_{t-v}$ and $c_v(c_v - 1)/2$, has no such order, yet cannot tick a required row. | The model's own follow-up 2 uses the count-first formula, and the script confirms it equals brute force on 500 random lists. A required row should name the property, not one plan's way of getting it. | "Tick only if both: the typed code is correct (it gives 5 on the example), and while typing you said why no position pairs with itself and no pair is counted twice. In the model's plan, that is why `target - x` is looked up before `x` is counted"

3. `homework-4.json` | `items[8].widget.model` (Plan A and Cost) | imprecise | minor | "Each step is a constant-time dict look-up, so time is $O(n)$" states an average-case bound as if it were a guarantee. An interviewer's next question is the worst case. | A hash table look-up is $O(1)$ on average and $O(n)$ in the worst case (CLRS, sec. 11.2). The course says "on average" for amortised steps elsewhere. | In Plan A replace "Each step is a constant-time dict look-up, so time is $O(n)$;" with "Each step is a dict look-up, constant time on average, so time is $O(n)$ on average;". In **Cost** replace the sentence with "One pass of dict steps, each constant time on average: $O(n)$ time and $O(n)$ memory."

The `NotesDrive` solution passes its ten hidden tests and the starter fails all ten. A flat-dictionary version written for this audit passes the nine rule tests and agrees with the solution on a 4,000-step random case, so the rules admit one reading. `size` costs the same with 2,000 and 64,000 files stored. The pair-count model code, the two-pointer run rule and the many-target formula all equal brute force.

## research-int

1. `homework-2.json` | `items[8].widget.model` (How many) | imprecise | minor | "so a stricter bar is $0.51 \times 1.73 = 0.88$". The arithmetic is right, but 0.88 is the lower bar, easier to clear than 1.73. A learner reads "stricter" as harder to pass and carries the scaling the wrong way. | The Marchenko-Pastur edge scales with the noise variance $\sigma^2$: $\sigma^2(1 + \sqrt{p/n})^2$ (Laloux, Cizeau, Bouchaud and Potters, 1999). With $\sigma^2 = 0.51 < 1$ the bar falls. The conclusion (three components) is unchanged. | Replace "so a stricter bar is $0.51 \times 1.73 = 0.88$. The fourth still misses it." with "so a lower bar, scaled to that noise, is $0.51 \times 1.73 = 0.88$. The fourth misses even that."

2. `homework-4.json` | `items[8].prose` | misleading | minor | The task interpolates between the quotes on either side of `t` and holds the first price backwards in time. Both read a quote that arrives after `t`. The item frames this as how long a quote "can be trusted" and never says the answer is not knowable at `t`. | In the solution, the value at second 4 changes when the quote at second 10 changes (script check). The level's own interpolation lesson warns, in its summary, never to feed a linear fill to a model as if known at the time; the task drops that warning. Look-ahead is the standard backtest fault (López de Prado, *Advances in Financial Machine Learning*, sec. 11.4). Minor because the lesson states the rule. | Replace "A desk asks for tens of thousands of seconds at a time." with "A desk asks for tens of thousands of seconds at a time, to mark past trades. The fill reads the quote after `t`, so it is never an input a live model could have had."

3. `homework-2.json` | `items[8].widget.model` (follow-up 2) | imprecise | minor | "Only if the stocks had similar volatilities" gives one condition as the only one. Covariance is also the right choice when variance in return units is the object, as in a risk model. | Jolliffe, *Principal Component Analysis*, sec. 3.3: covariance suits variables in the same units whose variances carry meaning. Statistical risk models take components of the return covariance (Connor and Korajczyk, 1988). | Replace "(2) Only if the stocks had similar volatilities. Otherwise the most volatile names take over the first components, so correlations are the safer default for returns." with "(2) Yes if the job is risk in return units, where a volatile stock should count for more. To find common structure, no, unless volatilities are similar: the most volatile names take over the first components."

Checked and correct: $p = 0.025$, power 0.61, the "four times in ten" for twenty tries, 7.84 years, and the Benjamini-Hochberg claim (a best $p$ of 0.025 passes only with ten or more versions under 0.05). The noise edge 1.73 was checked by Monte Carlo: over 300 draws of pure noise the largest eigenvalue averages 1.67 and never passes 1.79, and with three planted factors exactly three eigenvalues clear the edge in 100 runs of 100. `quote_at` passes its ten tests, the starter fails, and an independent version agrees. The determinant is 26.

## systems

1. `homework-4.json` | `items[6].explain.text` (with `items[6].feedback.correct`) | imprecise | minor | The feedback tells the learner to check their loads and stores against the explain, since the tests cannot. The explain gives only the `tail_` pair. The `head_` pair, which stops the producer overwriting a tick still being read, is absent, so half the memory orders have nothing to be checked against. | The solution uses both pairs: the consumer stores `head_` with release and the producer loads it with acquire (Williams, *C++ Concurrency in Action*, sec. 5.3). A learner who loads `head_` relaxed in `try_push` passes every test and finds no line in the explain that says otherwise. | Replace the explain with: "The unsigned difference `tail_ - head_` is the count even after a wrap, and the slot is the counter masked with $N - 1$, which stays in order because $N$ divides $2^{32}$. The producer stores `tail_` with release after writing the slot, and the consumer loads it with acquire before reading, so a tick is never read half-written. The consumer's release store of `head_` and the producer's acquire load of it do the same for a freed slot, so no tick is overwritten before it is read."

The ring itself is sound. It has no data race and no undefined behaviour: each slot access is ordered by a release and acquire pair, ThreadSanitizer reports nothing, and 2,000,000 ticks cross the counter wrap in order under two threads. The counters are 64 bytes apart and the object makes no heap allocation. `size` is safe because the specification gives it to the consumer only. The two-bit counter figure (36%, 18 ms) matches the stationary law of the four-state chain, 0.3621, and a simulation. All four review keys and their slips are right.

## ito

No findings. The Black equation derivation (`homework-3.json` `items[7]`) is valid at every step: $dF$ by Itô, the hedge $\Delta = e^{r(T_F - t)}V_F$, the cancellation of $\mu$, the no-arbitrage step and both checks. The script confirms that the Black-76 call solves the equation and that the stated hedge replicates it under a real-world drift of 11%. In `homework-2.json` the edit to `h-why-not-chain` is layout only. Making the hypotheses row and the Taylor row of `h-derive-ito` required, and the worked check optional, demands nothing false: the hypotheses (adapted, integrable, $C^{1,2}$) and the local-martingale caution are all stated.

## measure-prob

1. `homework-3.json` | `items[8].rubric[3].text` | imprecise | minor | The required row credits the chance $\tfrac12$ only "by the tower property". The symmetry of the two colours gives $\tfrac12$ at once and is a complete argument, which the row would not credit. | The urn starts with one ball of each colour and the rule treats the colours alike, so $P(D_{n+1} = 1) = P(D_{n+1} = 0) = \tfrac12$. The prompt asks only to "find the chance". | "Finds that draw $n + 1$ is red with chance $\tfrac12$, with a reason: $E[D_{n+1}] = E[M_n] = \tfrac12$ by the tower property, or the symmetry of the two colours."

The three proofs hold. Continuity from above states its finiteness hypothesis and names the subtraction that needs it. Monotone convergence has its hypotheses checked, and the means of the simple functions match exact fractions for $n = 1$ to 8. The urn is a martingale on every atom up to $n = 8$ by exact enumeration, and no step assumes independence.

## New-text rule

No new or changed learner text cites a lesson by number. The two lesson references in `ito/homework-2.json` `items[8].model` predate the close and are outside this delta.

## Summary

| course | ledger rows | wrong | imprecise | misleading | unverified | serious | minor | overlap: mine only / earlier only / both |
|---|---|---|---|---|---|---|---|---|
| puzzles | 42 | 0 | 0 | 0 | 0 | 0 | 0 | pending |
| game-theory | 28 | 0 | 1 | 0 | 0 | 0 | 1 | pending |
| brainteasers | 31 | 0 | 0 | 0 | 0 | 0 | 0 | pending |
| coding-int | 46 | 1 | 2 | 0 | 0 | 0 | 3 | pending |
| research-int | 55 | 0 | 2 | 1 | 0 | 0 | 3 | pending |
| systems | 69 | 0 | 1 | 0 | 0 | 0 | 1 | pending |
| ito | 31 | 0 | 0 | 0 | 0 | 0 | 0 | pending |
| measure-prob | 47 | 0 | 1 | 0 | 0 | 0 | 1 | pending |
| total | 349 | 1 | 7 | 1 | 0 | 0 | 9 | pending |

## Overlap with earlier reads

Pending: filled after the blind commit.

## Gate results

Pending: filled after the blind commit.
