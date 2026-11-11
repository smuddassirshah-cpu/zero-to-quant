# Concept audit, delta batch 1 of 11 November 2026

Blind delta audit of content added or changed after each course closed: puzzles, game-theory, brainteasers, coding-int, research-int, systems, ito (levels 2 and 3) and measure-prob (levels 1 to 3). Scope is the changed items only, read from `git diff <close> HEAD` with each whole item and its lesson context. Twenty-seven files, 29 items (25 new, 4 edited).

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
| puzzles | 42 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 0 / 0 |
| game-theory | 28 | 0 | 1 | 0 | 0 | 0 | 1 | 1 / 0 / 0 |
| brainteasers | 31 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 3 / 0 |
| coding-int | 46 | 1 | 2 | 0 | 0 | 0 | 3 | 3 / 1 / 0 |
| research-int | 55 | 0 | 2 | 1 | 0 | 0 | 3 | 3 / 3 / 0 |
| systems | 69 | 0 | 1 | 0 | 0 | 0 | 1 | 1 / 5 / 0 |
| ito | 31 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 1 / 0 |
| measure-prob | 47 | 0 | 1 | 0 | 0 | 0 | 1 | 1 / 1 / 0 |
| total | 349 | 1 | 7 | 1 | 0 | 0 | 9 | 9 / 14 / 0 |

## Overlap with earlier reads

Filled after the blind commit (`b1009863`). Earlier reads of this delta content, found by `grep -l` of the item ids in `docs/reviews/`:

- `review-perf-retrofit-1.md`: brainteasers `hw9-l-pieces-6x10` and `hw9-circle-hats`; research-int `h2-pca-aloud` and `h4-quote-at`; coding-int `h3-notes-drive` and `h4-pairs-aloud`.
- `review-perf-retrofit-2.md`: systems `h1-branch-aloud`, `h3-process-aloud`, `h4-spsc-ring`; measure-prob `h-build-space`, `h-build-integral`, `h-prove-urn`; puzzles `hw4-kelly-draw`.
- `review-perf-retrofit-3.md`: ito `h-derive-black`.
- `review-perf-retrofit-5.md`: game-theory `hw1-street-carts`.
- `review-perf-pilots.md`: ito `h-derive-ito` and research-int `h1-signal-aloud`. Its findings were fixed before those courses closed, so they are outside this delta and are not counted. The delta edits to both items (required flags, an optional point) and the two layout edits have no earlier read.
- Review top-up items (the ten new review items in this batch): no earlier read exists. No file in `docs/reviews/` names any of them; only the author report `docs/reports/review-topup.md` and its number script do.

Counted as conceptual: a finding about a definition, a claim, a method, a hypothesis or a stated reason. Not counted: rubric weights and required flags, missing hidden tests, feedback that gives the answer away, freshness against lesson screens, report wording and typography. Every earlier finding had its fix applied before this read, so "both" can only be a fault that survived a fix; there is none.

| course | this audit only | earlier read only | both | earlier conceptual findings (all fixed before this read) |
|---|---|---|---|---|
| puzzles | 0 | 0 | 0 | none; retrofit 2 read the Kelly task clean. Review items: no earlier read |
| game-theory | 1 | 0 | 0 | none; retrofit 5 read the street-carts task clean. My finding is on a review item with no earlier read |
| brainteasers | 0 | 3 | 0 | BZ1-1 (the piece as defined admitted the I piece), BZ2-2 (bound asserted without its reason), BZ2-3 ($n = 2$ sight line) |
| coding-int | 3 | 1 | 0 | CI4-1 ($O(1)$ memory for sort and two pointers) |
| research-int | 3 | 3 | 0 | RI2-2 (standardised returns), RI2-3 (same-day share against forecast), RI2-5 (loadings in the equicorrelation case) |
| systems | 1 | 5 | 0 | SY4-2 (wrong reason for the wrap), SY3-1 (wait overstated), SY3-4 (kernel copy stated without exception), SY3-5 (tagged TLB entries), SY4-4 (own line against different lines) |
| ito | 0 | 1 | 0 | IT3-3 (the zero-cost book with cash) |
| measure-prob | 1 | 1 | 0 | MP1-2 (some finite $\mu(A_m)$ is enough) |
| total | 9 | 14 | 0 | |

Three of the nine findings sit in text that an earlier read's fix wrote, which is the pattern the fix-pass read exists for:

- research-int 1 ("a stricter bar") is the wording of RI2-4's fix.
- coding-int 2 (the required row tied to the look-up order) is the wording of CI4-2's fix.
- systems 1 follows from SY4-1's fix, which sent the learner to the explain for the memory orders without extending the explain to the `head_` pair.

The other six (game-theory 1, coding-int 1 and 3, research-int 2 and 3, measure-prob 1) were in the authored text and were missed by the earlier read, or had no earlier read. I agree with every earlier conceptual fix as it now stands in the content.

## Gate results

Run from `app/` on the worktree at the blind commit, 11 November 2026.

- Validator: `node tools/validate.mjs` gives 0 errors (4,138 warnings, none new for these items; `perf-optional-row` warnings 0). `content/manifest.json` unchanged.
- Concepts script: `python3 docs/reports/delta-2026-11-11-1-concepts.py` runs 85 checks and exits 1. The three failing checks are findings coding-int 1, research-int 1 and research-int 2, and stay failing until those are fixed. No check was skipped: g++ 13 and ThreadSanitizer were both available.
- Committed number scripts, all exit 0: `puzzles-4`, `game-theory-1`, `brainteasers-1`, `brainteasers-2`, `coding-int-3`, `coding-int-4`, `research-int-1`, `research-int-2`, `research-int-4`, `systems-1`, `systems-3`, `systems-4`, `ito-2`, `ito-3`, `measure-prob-1`, `measure-prob-2`, `measure-prob-3` (each `-perf-numbers.py`), and `review-topup-numbers.py` ("all 13 keys recomputed twice"). `ito-2` and `puzzles-4` report that sympy is missing and run their numeric checks only.
- Voice: `python3 docs/reviews/voice-scan.py 35 --summary` on each of the eight course folders gives 0 sentences over 35 words and 0 explanations over three sentences. Every proposed fix above was counted by hand against the same limits.
- Playthrough, each of the 27 changed sets, desktop and `--mobile`, with `--local-cdn`: 52 of 54 runs end "All passed", code items included (the `NotesDrive`, `quote_at`, street-carts and hats solutions under Pyodide, and the ring under clang). The two that do not are `research-int/review-1`, desktop and mobile: the set itself plays (10 of 10 recorded) but its `(timed)` and `(timed parts)` checks throw `page.waitForFunction: Timeout 20000ms exceeded`. That failure is recorded in KNOWN_ISSUES (session Y) as present before and after the top-up item, and is already in the inbox; it is a harness or engine fault, not a content fault of this delta. It is restated as one inbox bullet under `Raised later (audit delta 2026-11-11):`.
- Unverified claims: none. Two claims rest on the item's own stated figures and not on measurement: the 5 ns cost of a wrong guess and the 0.2 µs, 2 µs and 1 µs costs in the systems tasks are given as round figures in the prompts, and were checked only for the arithmetic built on them.

## Fix pass

Opus fixer, 11 November 2026, content commit `c82c4904`. Nine findings: 9 fixed, 0 disputed, 0 not applied. Each basis below was established independently of the auditor's evidence; where my wording differs from the proposed fix, the reason is given.

- **game-theory 1** (`review-2.json` `items[9].prose`): fixed. Basis: half the average of guesses in $[0, B]$ is at most $B/2$, so a round deletes guesses above $B/2$; $100/2^6 = 1.5625$ and $100/2^7 = 0.78125$, so the key 7 stands. Prose now states the starting bound 100 and the halving step. Key unchanged.
- **coding-int 1** (`homework-3.json` `items[8].feedback.byKey.test-6`): fixed, "three" to "four". Basis: counted `tests[5]` myself; `mv('/a','/b')` (dst exists), `mv('/a','/a/k/l')` (inside src), `mv('/','/z')` (src is root), `mv('/a/f','/b/g')` (dst exists), four `False`. Test unchanged.
- **coding-int 2** (`homework-4.json` `items[8].widget.rubric[3].text`): fixed. **Required rubric row changed**: it now asks why no position pairs with itself and no pair is counted twice, and names the look-up order as the one-pass dict's reason. Basis: the count-first plan ($c_v c_{t-v}$ for $v < t - v$, $c_v(c_v - 1)/2$ for $v = t - v$) is correct and has no look-up order, so the old row failed a correct plan. Kept required (it carries the code, the item's core), points and flags unchanged; no prompt change needed.
- **coding-int 3** (`homework-4.json` `items[8].widget.model`, Plan A and Cost): fixed, "constant time on average" and "$O(n)$ on average". Basis: hash-table look-up is $O(1)$ expected, $O(n)$ worst case (CLRS sec. 11.2; CPython dict is open addressing with the same bounds).
- **research-int 1** (`homework-2.json` `items[8].widget.model`, How many): fixed, "a lower bar, scaled to that noise". Basis: the Marchenko-Pastur edge is $\sigma^2(1 + \sqrt{p/n})^2$; recomputed $(50 - 26.1)/47 = 0.509$, $(1 + \sqrt{0.1})^2 = 1.732$, product 0.88 below 1.73, and 0.85 below both.
- **research-int 3** (`homework-2.json` `items[8].widget.model`, follow-up 2): fixed, own wording: "Yes if the job is risk in return units ... To find structure shared across stocks, only if their volatilities are similar." Basis: covariance PCA is the standard statistical risk model (Connor and Korajczyk 1988); correlation PCA is preferred when scales differ and structure is the aim (Jolliffe sec. 2.3).
- **research-int 2** (`homework-4.json` `items[8].prose`): fixed, own wording. Basis: in the solution the interpolated value and the backward hold both read a quote at a second after `t`, so they are marks for past trades, not live inputs. My sentence names the two cases ("between quotes and before the first") instead of "the fill reads the quote after `t`", which is false at a quoted second and in the forward hold. Tests unchanged.
- **systems 1** (`homework-4.json` `items[6].explain.text`): fixed, own wording, three sentences. Basis: the item's solution stores `head_` with release in `try_pop` and `drain` and loads it with acquire in `try_push`; without that pair the consumer's read of a slot and the producer's next write to it are unordered, a data race (Williams, sec. 5.3; the standard SPSC argument). The first two old sentences were merged so the explain stays at three.
- **measure-prob 1** (`homework-3.json` `items[8].rubric[3].text`): fixed. **Required rubric row changed**: it credits any valid reason, naming the tower property ($P(D_{n+1} = 1) = E[M_n] = \tfrac12$) and colour symmetry. Basis: the start and the rule are invariant under swapping colours, so red and blue next are equally likely. Points and required flag unchanged.

Keys, keyed option text and hidden tests: none changed. Script: the check on line 280 of `docs/reports/delta-2026-11-11-1-concepts.py` encoded the old text ("three moves", count 3); it now requires "four moves" and count 4.

Gates (from `app/`): validator 0 errors (4,140 warnings, none on these seven items; manifest unchanged). Concepts script 85 checks, 0 failed, exit 0. Perf-number scripts of the five courses (coding-int 1, 3, 4; game-theory 1; research-int 1, 2, 4; systems 1, 3, 4; measure-prob 1, 2, 3) and `review-topup-numbers.py` exit 0. Voice scan 35 on the five courses: 0 and 0. Playthrough of the seven changed sets, desktop and `--mobile` with `--local-cdn`: 14 of 14 "All passed".

## Fix-pass read

Blind read of `git diff c82c4904~1 c82c4904 -- app/content/courses` (7 files, 8 changed lines) by a fresh reader who has not seen the audit, its ledger, its script or the earlier reviews. Each changed string was read inside its whole item.

### Ledger

| # | course | file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|---|---|
| 1 | coding-int | homework-3.json | `items[8].feedback.byKey.test-6` | Test 6 asks for four moves that must be refused | correct | Run: `tests[5]` holds four `mv` calls (`/a`→`/b` dst exists, `/a`→`/a/k/l` dst inside src, `/`→`/z` src is root, `/a/f`→`/b/g` dst exists); the solution returns `False` four times. |
| 2 | coding-int | homework-3.json | `items[8].feedback.byKey.test-6` | Check every refusal before making any folder for `dst` | correct | `ls /a` must stay `['f']` after the refused `/a`→`/a/k/l`; making `/a/k` first would break it. Matches the solution's order. |
| 3 | coding-int | homework-4.json | `items[8].widget.model` (Plan A) | A dict look-up is constant time on average, so the pass is $O(n)$ on average | correct | Python wiki TimeComplexity: dict get and set are $O(1)$ average, $O(n)$ amortised worst case; CLRS ch. 11 (hashing, expected time). Worst case is $O(n^2)$, so "on average" is the right qualifier. |
| 4 | coding-int | homework-4.json | `items[8].widget.model` (Cost) | One pass of dict steps: $O(n)$ time on average, $O(n)$ memory | correct | As row 3; memory is at most $n$ keys. The unqualified $O(n)$ in `rubric[2]`, `explain` and follow-up 2 is the usual shorthand and does not contradict it. |
| 5 | coding-int | homework-4.json | `items[8].widget.rubric[3]` | Required: code correct, and you said why no position pairs with itself and no pair is counted twice | correct | Checked three correct plans against brute force on 2,000 random lists: one-pass dict (earlier partners only), counts then $c_v c_{t-v}$ for $v < t - v$ plus $c_v(c_v-1)/2$, sort and two pointers with runs. Each has its own reason for both halves, so each can tick. Wrong plans fail the "code is correct" half. |
| 6 | coding-int | homework-4.json | `items[8].widget.rubric[3]` | In a one-pass dict the reason is that `target - x` is looked up before `x` is counted | correct | Look-up first means only earlier positions are seen: no self-pair when $2x$ is the target, and each pair is counted once at its later position. Agrees with the model and the explain. |
| 7 | game-theory | review-2.json | `items[9].prose` | The bound starts at 100 | correct | Guesses run 0 to 100. |
| 8 | game-theory | review-2.json | `items[9].prose` | Each round removes every guess above half the current bound, and that half is the new bound | correct | If all guesses are at most $B$, the average is at most $B$ and the target at most $B/2$, so guesses above $B/2$ are dominated (Osborne, *An Introduction to Game Theory*, ch. 12; Nagel 1995). Solved: $100/2^6 = 1.5625$, $100/2^7 = 0.78125$, so key 7 holds; the slip 6 and its feedback, the generic line and the explain agree. |
| 9 | measure-prob | homework-3.json | `items[8].rubric[3]` | $P(D_{n+1} = 1) = E[M_n] = \tfrac12$ by the tower property | correct | $E[D_{n+1}] = E[E[D_{n+1} \mid \mathcal{F}_n]] = E[M_n]$, and $E[M_n] = M_0 = \tfrac12$ for a martingale (Williams, *Probability with Martingales*, 9.7 and 10.3). Same as the model's Consequences. |
| 10 | measure-prob | homework-3.json | `items[8].rubric[3]` | The symmetry of the two colours is also a valid reason | correct | The urn starts one red, one blue, and the rule treats the colours alike, so swapping labels keeps the law. Red and blue at draw $n + 1$ are then equally likely and sum to 1. The equal start that this needs is in the prompt. |
| 11 | research-int | homework-2.json | `items[8].widget.model` (How many) | A lower bar, scaled to the residual noise, is $0.51 \times 1.73 = 0.88$ | correct | Recomputed: $50 - 26.1 = 23.9$, $23.9/47 = 0.509$, $(1 + \sqrt{0.1})^2 = 1.732$, product 0.88. It is below 1.73, so "lower" is right. Marchenko-Pastur edge $\sigma^2(1 + \sqrt{q})^2$ (Bouchaud and Potters, *Theory of Financial Risk*, ch. 9; Laloux et al. 1999). With $q = 47/500$ it is 0.87, same verdict. |
| 12 | research-int | homework-2.json | `items[8].widget.model` (How many) | The fourth, 0.85, misses even that | correct | $0.85 < 0.88$ (and $< 0.87$). Three stay as structure, $23 - 3 = 20$ noise, as the rubric and explain say. |
| 13 | research-int | homework-2.json | `items[8].widget.model` (follow-up 2) | Covariance PCA: yes if the job is risk in return units, where a volatile stock should count for more | correct | Jolliffe, *Principal Component Analysis*, 2.3 and 3.3: covariance PCA suits variables in one unit whose variances matter; statistical risk models work on covariances. |
| 14 | research-int | homework-2.json | `items[8].widget.model` (follow-up 2) | To find shared structure, only if volatilities are similar; otherwise the volatile names take over, so correlations are the safer default | correct | Jolliffe 3.3: with unequal variances the leading covariance components track the high-variance variables. Agrees with "When they mislead" in the same model. |
| 15 | research-int | homework-4.json | `items[8].prose` | The desk asks for many seconds at a time, to mark past trades | correct | A stated use; consistent with the rules, which need quotes on both sides of `t`. |
| 16 | research-int | homework-4.json | `items[8].prose` | Between quotes and before the first, the answer reads a quote that arrives after `t`, so a live model could not have known it | correct | Checked against the solution: the interpolation branch reads `xs[i] > t`, the gap test reads it too, and the `i == 0` branch holds `ys[0]` with `xs[0] > t`. The exact-hit and after-the-last branches read only quotes at or before `t`, and the sentence rightly leaves them out. All 10 hidden tests pass on the solution. |
| 17 | systems | homework-4.json | `items[6].explain.text` (sentence 1) | Unsigned subtraction is exact modulo $2^{32}$, so `tail_ - head_` is the count after a wrap | correct | C++ [basic.fundamental]: unsigned arithmetic is modulo $2^n$; the count is at most $N < 2^{32}$. Test 8 starts both counters at 4,294,967,291 and expects the right count. The prose fixes the width at 32 bits. |
| 18 | systems | homework-4.json | `items[6].explain.text` (sentence 1) | "the slot mask $N - 1$ stays in order because $N$ divides $2^{32}$" | imprecise | The mask is a constant; what stays in order across the wrap is the slot index, the counter masked with $N - 1$. The reason given is right: $N \mid 2^{32}$ makes $(c \bmod 2^{32}) \bmod N = c \bmod N$. See finding 1. |
| 19 | systems | homework-4.json | `items[6].explain.text` (sentence 2) | Producer stores `tail_` with release after writing the slot; consumer loads it with acquire before reading; so no tick is read half-written | correct | Solution lines: `buf_[t & (N - 1)] = v;` then `tail_.store(t + 1, release)`; `tail_.load(acquire)` in `try_pop` and `drain` before the slot read. Release then acquire on one atomic gives happens-before for the slot write (cppreference `std::memory_order`, Release-Acquire ordering; Williams, *C++ Concurrency in Action*, 5.3.3). |
| 20 | systems | homework-4.json | `items[6].explain.text` (sentence 3) | Consumer stores `head_` with release after reading the slot; producer loads it with acquire before writing; so no slot is overwritten while it is read | correct | Solution lines: `out = buf_[h & (N - 1)];` then `head_.store(h + 1, release)` (and `h + n` in `drain`); `head_.load(acquire)` in `try_push` before the full test and the write. The read happens-before the reuse of that slot, so there is no data race on `buf_` (same sources; Williams ch. 7 for the single-producer single-consumer queue). The relaxed loads are each thread's own counter, which only it writes, so the explain's silence on them is not an error. |

Verdict counts: 20 rows; 19 `correct`, 0 `wrong`, 1 `imprecise`, 0 `misleading`, 0 `unverified`.

Voice: British spelling, no exclamation marks, no em-dashes and no lesson cited by number in any changed string. `voice-scan.py 35` reports 0 sentences over 35 words and 0 explanations over three sentences in all five courses.

### Findings

1. app/content/courses/systems/homework-4.json | `items[6].explain.text` | imprecise | minor | The first sentence now says "the slot mask $N - 1$ stays in order". A constant mask has no order. The thing that stays in order across the wrap is the slot index, the counter masked with $N - 1$. | In the solution the slot is `t & (N - 1)` and `h & (N - 1)`. Because $N$ divides $2^{32}$, the wrapped counter and the true count agree modulo $N$, so the index still steps 0, 1, ..., $N - 1$, 0 through the wrap. The learner's understanding of the method is unchanged, hence minor. | Replace the first sentence of the explain with: "Unsigned subtraction is exact modulo $2^{32}$, so `tail_ - head_` is the count after a wrap, and the slot, the counter masked with $N - 1$, stays in order because $N$ divides $2^{32}$." (About 31 words by the voice scan's count; the explain stays at three sentences.)

No `wrong` rows, so nothing here counts towards the convergence rule.

### What was run

- Hidden tests of coding-int homework-3 `items[8]` and research-int homework-4 `items[8]` on their solutions in CPython: 10 of 10 pass in each. Test 6 of the first returns four `False` values.
- coding-int homework-4 `items[8]`: the model code gives 5 on the example; three correct plans agree with brute force on 2,000 random lists; $200{,}000 \times 199{,}999 / 2 = 19{,}999{,}900{,}000$.
- Numbers in research-int homework-2 `items[8]` and game-theory review-2 `items[9]` recomputed in Python.
- `voice-scan.py 35 --summary` on the five courses: 0 and 0 each. `node tools/validate.mjs`: 0 errors.
- Not run: the systems C++ solution was read line by line, not compiled, and no playthrough was run (no content changed in this read).
