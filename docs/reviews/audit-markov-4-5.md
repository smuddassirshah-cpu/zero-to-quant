# Concept audit: markov (topic 1.6), levels 4 and 5, round 1

Scope: `app/content/courses/markov/` l13 to l16, review-4, homework-4 (with its performance task `items[9]`), problems-4, l17 to l22, review-5, homework-5 (with its performance task `items[10]`), problems-5. These levels have no separate second read on record, so this audit stands in for it and was read at full Stage 1 depth. Blind read: no earlier review, audit, ledger, concepts script or author report for this course was opened until the ledger, the findings below and the script were committed (commit `c73c432e` on this branch). Ledger: `docs/reports/audit-markov-4-5-ledger.md` (291 hand-judged rows: 276 correct, 10 imprecise, 1 misleading, 4 wrong, 0 unverified). Script: `docs/reports/markov-L4-5-concepts.py` (112 checks: exact fractions and linear solves for every chain, ruin and pattern result, and seeded Monte Carlo for every empirical claim).

Method. Every graded key and every slip value was recomputed. Each theorem was checked against its hypotheses as the screen states them: optional stopping against Williams 10.10, Wald's identity, the ergodic theorem, detailed balance, the Poisson characterisations. Every optional-stopping answer was checked against an independent first-step linear solve, and every pattern wait against an exact solve of the prefix automaton (ABRACADABRA included, in fractions). Poisson thinning, superposition, memorylessness, the inspection paradox, the uniform arrival time, compound Poisson moments, the Wald examples and the burn-in and acceptance claims of the Metropolis lesson each have a Monte Carlo or exact matrix check sized to separate the claim from its negation.

Overall: the two levels are sound. Optional stopping is stated with all three standard conditions and each use names the condition it relies on. Convergence claims keep irreducibility and aperiodicity apart. Detailed balance is taught as sufficient and not necessary. No graded key is wrong. The findings are four wrong slip or option lines, one loosely justified use of Wald's identity, and eight smaller points of precision.

Format: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

## Level 4

1. l13-balanced-flows.json | screens[6].prose; summary.ideas[1]; homework-4.json items[1].widget.options[0].text | imprecise, minor | "Every such chain on a finite set of states is reversible, with π_{i+1} = π_i P_{i,i+1}/P_{i+1,i}" has no condition on the down chances. With a step up that cannot be undone the formula divides by zero, and screen 9 of the same lesson says a one-way arrow rules out reversibility. In homework-4 item 2 a line chain with a one-way step fits both the keyed option 1 and the unkeyed option 5. | Script NOTE F1: the line chain with P_01 = 0.5, P_10 = 0 has π = (0, 0.5, 0.5). Levin, Peres and Wilmer 2.5 define birth-death chains with every down chance positive before stating reversibility. | l13 screens[6].prose, last sentence: "When every step up can be undone by a step down, such a chain on a finite set of states is reversible, with $$\pi_{i+1} = \pi_i\,\frac{P_{i,i+1}}{P_{i+1,i}}.$$" l13 summary.ideas[1], last sentence: "Birth-death chains on a finite set of states are always reversible, when every step up can be undone." homework-4 items[1].widget.options[0].text: "A chain on a line of states that moves only to a neighbouring state, or stays, and can step both ways between neighbours".

2. l14-walks-on-networks.json | screens[11].explain.text | misleading, minor | "One dealer carries a third of the flow, a single point of failure. That is an argument for a central counterparty." A central counterparty is itself a hub by design: it stands between every pair. The case for it is netting and mutualised default resources, not the removal of a hub. The sentence teaches the opposite of what the degree count shows. | Hull, *Options, Futures and Other Derivatives*, chapter on OTC markets and central clearing: a CCP concentrates counterparty risk in one well-capitalised node. | Replace the explain with: "The degrees are 4, 2, 3, 2 and 1, adding to 12, so D1 sees $\tfrac13$ of all quote flow. If D1 fails, D5 is cut off and every other route gets longer. Regulators map networks like this to find the firms that matter most."

3. l15-sampling-by-chain.json | screens[1].widget.options[2].why | wrong, minor | "Flat steps are rejections, which are common near the peak." In this chain rejections are rarest at the peak. | Script check F3 (failing): stay chances along the grid are 0.500, 0.256, 0.197, 0.130, 0.099 (at 0.60), 0.146, 0.500. The canvas matrix on the same screen shows them. | "A converged chain keeps moving. Flat steps are rejections, and here they are most common at the two ends of the grid."

4. l15-sampling-by-chain.json | screens[2].feedback.correct; screens[2].explain.text (last sentence); homework-4.json items[8].model (point 4) | imprecise, minor | "After about 18 steps the start is forgotten" and "After that the chain behaves as if it began at the posterior". The chain is never exactly at the posterior after a fixed number of steps, and at the stated burn-in it is not yet close. A learner carries away burn-in as a switch. The homework model repeats "a chain needs about 20 steps to forget its start" and then reports a residual bias of 0.0004 after dropping 20 steps. | Script NOTE F4: at k = 18 the bar is 0.0586 against the target 0.0420; total variation distance from the posterior is 0.069 at k = 18, 0.051 at k = 20 and 0.003 at k = 40. It halves about every five steps. Levin, Peres and Wilmer 4.5 (distance to stationarity decays geometrically, never reaching 0); Geyer, *Handbook of MCMC* 1.11. | screens[2].feedback.correct: "After about 18 steps most of the start's pull has gone." screens[2].explain.text, replace the last sentence with: "The start's pull never vanishes exactly, but here it halves about every five steps, so a longer burn-in leaves less of it." homework-4 items[8].model point 4, replace "a chain needs about 20 steps to forget its start" with "a chain needs about 20 steps to lose most of the pull of its start".

5. l16-arrivals.json | screens[8].prose | imprecise, minor | "Run the clock backwards: the time since the last trade is also exponential, mean 0.5." At a fixed time t the time since the last trade is min(Exp(λ), t), because the process started at 0. It is exponential only for a process that has run a long time. The key (1 minute) is the long-run value. | Script NOTE F5: at t = 0.5 minutes the mean age is 0.317, matching (1 − e^{−λt})/λ, and the covering gap averages 0.82; at t = 10 they are 0.50 and 1.00. Grimmett and Stirzaker 10.3 (age and excess life). | Add a first sentence to the prose: "Trading has been running for a long while."

6. l16-arrivals.json | quiz[1].prose; quiz[1].widget.wrong (at-least-one 0.9817, empty 0.1353) | imprecise, minor | The item gives no rate, and the key 0.2 needs none. The two slips "at least one trade in 2 minutes" and "e^{-2}" are 1 − e^{-4} and e^{-2} only at 2 a minute. | Script NOTE F6. | quiz[1].prose: "Trades arrive as a Poisson process at 2 a minute. Exactly one trade arrived in a quiet 10-minute stretch." Add to quiz[1].explain.text: "The rate plays no part."

7. review-4.json | items[6].widget.wrong[1] (third, 0.3333); items[6].feedback.byKey.third | wrong, minor | "You averaged the three states equally" is attached to 0.3333. The equal-weight average of the move chances 1/2, 3/4, 1/4 is 1/2, which is already the slip "half". No slip named in the feedback gives 1/3. | Script check F7 (failing): equal-weight average 0.5000. | Replace the slip with one a learner can reach: `{"id": "walls-only", "value": 0.6429, "tol": {"abs": 0.001}}` and feedback.byKey.walls-only: "You counted only the proposals that fall off the ends. A proposal to a lighter value can be rejected too." Basis: move chances 1/2, 1, 1/2 weighted by (1, 2, 4)/7 give 4.5/7. Change feedback.byKey.half to: "You took the proposal chance as the move chance, or averaged the three states equally. Weight each state's own move chance by its share."

8. homework-4.json | items[2].feedback.byKey.half; items[2].feedback.byKey.forward | wrong, minor | The slip 0.5 is explained as "You treated the chain as reversible". Treating the chain as reversible gives P(A yesterday given B today) = P_BA = 0.2, which is the other slip, "forward". | Script check F8 (failing). Norris Theorem 1.9.1: the reversed chain has P*_BA = π_A P_AB / π_B; under reversibility P* = P. | feedback.byKey.half: "You split the chance evenly between A and C, the two venues that lead to B. Weight each by its flow into B: 0.8 from A against 0.2 from C." feedback.byKey.forward: "That is the chance of going from B to A, which would be right only for a reversible chain. Yesterday's state given today's uses $P_{AB}$, A to B."

9. review-4.json | items[7].widget.wrong[0] (one-minute, 0.0558); items[7].widget.wrong[2] (sum, 0.0222) | wrong, minor | Neither value is what its feedback describes. "You used one minute: means 3 and 2" gives e^{-3}(3²/2) × e^{-2}(2) = 0.0606. "You added the two chances" gives 0.04462 + 0.07326 = 0.1179. A learner who makes either slip gets the generic line. | Script checks F9 (two failing). | Set `"value": 0.0606` for one-minute and `"value": 0.1179` for sum. Tolerances of 0.001 keep both clear of the key 0.00327 and of "merged" 0.0076.

## Level 5

10. l17-fair-bets.json | screens[4].explain.text | imprecise, minor | "Under this chance every price on the tree is a fair game. Pricing with Trees (topic 1.7) calls it the risk-neutral chance." The risk-neutral chance makes the discounted price a martingale. It equals 4/9 here only at a zero interest rate, which the screen does not say. A learner meets p = (e^{rΔt} − d)/(u − d) later and finds the two definitions disagree. | Hull, *Options, Futures and Other Derivatives*, ch. 13 (binomial trees); Shreve I, 1.1 and 2.4 (discounted price is a martingale under the risk-neutral measure). | Replace the last sentence with: "With interest rates at zero it is the risk-neutral chance of Pricing with Trees (topic 1.7); with a rate, the discounted price is the fair game."

11. l17-fair-bets.json | quiz[3].feedback.byKey.five | imprecise, minor | "You may have dropped the chances" does not lead to 5. Dropping the chances gives 3 + 1 + x = 2, so x = −2; an equal average gives 2. The value 5 solves 0.2x = 1. | Script NOTE F11. | "You solved $0.2x = 1$. The known moves give $1.5 + 0.3 = 1.8$, so $0.2x$ has to supply only the last 0.2."

12. l21-waiting-for-patterns.json | screens[7].prose | imprecise, minor | "Gamblers now bet on letters at odds of 26 to 1." A fair bet on a letter with chance 1/26 returns £26 for £1, which is odds of 25 to 1. Odds of 26 to 1 return £27 and would give 27^11 + 27^4 + 27. The answer on the screen uses the 26-for-1 return, so only the wording is off, in a course for traders who quote odds. | Script NOTE F12. Williams 10.11: each gambler's stake is multiplied by 26 on a win. | "A monkey types one of 26 capital letters at random each second. How long until ABRACADABRA appears? Gamblers now bet on letters at fair odds: a winning £1 bet returns £26."

13. l22-arrivals-fair-game.json | screens[6].prose; screens[6].explain.text | imprecise, serious | "Wald's identity from Optional stopping gives E[S_10] = E[N_10]E[Y]" and "The count is a stopping-time sum of independent sizes, so Wald applies." By the definition taught in l19 (a rule that decides at each step from the first n steps only), N_10 is not a stopping time for the sizes: it is fixed by the arrival clock, independently of them. The result is right, and it follows from independence by conditioning on the count, the random-sum rule the next screen cites. A learner who answers "because N is a stopping time" has the wrong hypothesis, and may next apply Wald to a count that depends on the sizes in a way that looks ahead. | Grimmett and Stirzaker 3.7 (random sums, N independent of the summands) against 10.2 (Wald's equation for stopping times). Script: compound Poisson Monte Carlo confirms the mean 4,200 and variance 1,340,000; the numbers are not in doubt. | screens[6].prose: "Over 10 minutes the count $N_{10}$ is Poisson with mean $\lambda t = 20$. The count is independent of the sizes, so Random sums gives $E[S_{10}] = E[N_{10}]\,E[Y]$. So $S_t - \lambda t\,E[Y]$ is a martingale too." screens[6].explain.text: "$E[S_{10}] = 20 \times 210 = 4{,}200$ shares. Given the count, the total is that many independent sizes, so averaging over the count gives $E[N]\,E[Y]$. Subtracting $\lambda t E[Y] = 420t$ makes the volume a fair game."

## Counts

13 findings: 4 wrong (3, 7, 8, 9), 8 imprecise (1, 4, 5, 6, 10, 11, 12, 13), 1 misleading (2). Serious 1 (finding 13), minor 12. No graded key is affected. All four `wrong` findings are single lines: one option reason and three slip lines.

Checked and found correct, so a fixer need not revisit: the three optional-stopping conditions and every use of them (l19, l20, l21 screen 4, l22 screen 4, homework-5 items 5 and 10); "detailed balance is stronger than stationarity" with its two counterexamples; time averages need irreducibility only, P^k needs aperiodicity as well (l14 screen 8, l15 screen 6, review-4 item 5); rejected Metropolis steps are counted; the Hastings ratio and both biased samplers in problems-4; thinning independence, superposition, the uniform arrival time and the inspection paradox by Monte Carlo; every pattern wait, ABRACADABRA included, by exact solve; compound Poisson variance λt E[Y²]; "premiums must exceed λE[Y] or ruin is certain".

## Checks run

- `node tools/validate.mjs`: 0 errors.
- `node tools/run-number-scripts.mjs --only markov`: 5 of 5 scripts passed, 0 new failures.
- `node tools/grade-all.mjs --file` on all 16 files: 203 widgets, 0 failures. With `--code` on the 11 files that hold code: 12 Python widgets run, 0 failures.
- `docs/reports/markov-L4-5-concepts.py`: 112 checks, 5 failing, exit 1. The five are findings 3, 7, 8 and 9 (two checks); the script exits 0 once those lines are fixed.
- No playthrough, by the session's instruction.

## Overlap with earlier reads

Read after the blind commit `c73c432e`. Earlier reads that judged the content of these files: `review-problems-1.5-d.md` (problems-4 and problems-5, with its fix pass) and `review-perf-retrofit-8.md` (homework-4 `h-mh-network`, homework-5 `h-build-lazy-martingales`, and through them l19, l20 and `h-long-take-profit`). The lessons l13 to l22, review-4, review-5 and the other homework items had no earlier read. The reuse reads (`review-reuse-af-hits*.md`, `review-delta-af-1.md`, `review-delta-ae-1.md`) and the band read (`review-pass9-hits.md`) judged freshness and tolerances, not concepts, and are not counted. The author reports `docs/reports/markov-4.md`, `markov-5.md`, `markov-4-perf.md`, `markov-5-perf.md` and `problems-markov.md` were opened only for this table.

Conceptual findings of the earlier reads, all fixed before this audit and so not open to rediscovery:

| earlier finding | file | status in the text audited |
|---|---|---|
| review-problems-1.5-d 1 (`wrong`): an option marked wrong also made the target uniform | problems-4 items[0].parts[2] | fixed; the replacement option (accept with 1/deg(i), H rises to 16/26) is confirmed by the script |
| review-problems-1.5-d 2 (`wrong`): lost passengers called a Poisson stream | problems-4 items[1].parts[3].explain | fixed; "a long-run rate, not a Poisson stream" is a ledger row, correct |
| review-problems-1.5-d 3 (`unclear`): "extra room only helps when taxis outrun passengers" | problems-4 items[1].parts[4].explain | fixed; ledger row correct |
| review-problems-1.5-d 4 (`unclear`): "biases towards the regime that proposes least" | problems-4 items[3].parts[4].explain | fixed; ledger row correct |
| review-perf-retrofit-8 L19-1: condition (3) of optional stopping stated without "T finite with chance 1" | l19 screens[2], screens[3], summary; l20 screens[3]; homework-5 `h-long-take-profit` | fixed; all five strings carry the condition and are ledger rows, correct |
| review-perf-retrofit-8 MK5-1: rubric row 3 asked no reason for a finite mean | homework-5 items[10].rubric[2] | fixed; ledger row correct |
| review-perf-retrofit-8 MK5-2: required row named only condition (3) though (2) also holds | homework-5 items[10].rubric[3], model | fixed; the condition (2) bound (steps at most 1 − θ, E[T] ≤ 5/0.00243) is confirmed |

| | count |
|---|---|
| Conceptual findings by this audit only | 13 (4 wrong, 8 imprecise, 1 misleading) |
| By the earlier reads only | 7 (2 wrong, 2 unclear, 3 Should), all already fixed |
| By both | 0 |

All 13 are in text no earlier read had judged: the lessons, review-4, and homework-4 items 2, 3 and 9 (index 1, 2 and 8), a file that `review-perf-retrofit-8` opened only for its last item. Neither earlier read saw a `wrong` that is still in the text. New `wrong` findings for the convergence rule: 4 across two levels (findings 3, 7, 8, 9), each a single option or slip line and none a key, definition or theorem. That is above one per three levels, so the rule calls for a second blind round after the fix pass.

## Fix pass

Opus fixer, on `cab9929d`. Each basis below is my own derivation or check, made before reading the auditor's suggested wording as a source. Scratch checks in the fixer's scratchpad `fix-mk45/` (Metropolis matrix powers, network distances, Poisson age simulation).

| # | status | basis |
|---|---|---|
| 1 | fixed differently in basis | The cut between {0..i} and {i+1..n} carries zero net flow at stationarity, so balance holds for any finite birth-death chain; but the ratio formula needs $P_{i+1,i} > 0$ (Levin, Peres and Wilmer 2.5 take every down chance positive). The auditor's evidence chain (one-way step, $\pi = (0, 0.5, 0.5)$) still satisfies balance, so this is a formula-hypothesis fix, not a reversibility fix. l13 screens[6] and summary, homework-4 items[1] option `bd` now carry the "can be undone" condition. |
| 2 | fixed differently | A CCP is a hub by design (Hull, OTC markets and clearing), so a single-point-of-failure argument does not lead to it. The auditor's replacement "every other route gets longer" is false: without D1, D2 to D3 and D3 to D4 stay 1 hop and D2 to D4 stays 2 hops via D3; only D5 is cut off. New text says only that. |
| 3 | fixed | Diagonal of the canvas matrix: 0.500, 0.256, 0.197, 0.130, 0.0995, 0.146, 0.500; rejections are rarest at 0.60 and commonest at both ends. |
| 4 | fixed | My matrix powers: TV distance 0.069 at k = 18, 0.0027 at k = 40; second eigenvalue 0.863, so the distance halves every 4.7 steps and never reaches 0. l15 screens[2] feedback and explain, homework-4 items[8] model point 4 reworded. |
| 5 | fixed | Age at a fixed time t is min(Exp(λ), t), mean (1 − e^{−λt})/λ: 0.316 at t = 0.5 by formula and by simulation, 0.50 at t = 10. Prose now says trading has run a long while. |
| 6 | fixed | 0.9817 = 1 − e^{−4} and 0.1353 = e^{−2} hold only at 2 a minute; the rate is now stated, and the explain notes it plays no part. |
| 7 | fixed differently (slip changed) | π = (1, 2, 4)/7, move chances 1/2, 3/4, 1/4: key 3/7; equal-weight average 1/2 (already `half`). Replaced `third` 0.3333 with `stay` 0.5714 (tol 0.002): 1 − 3/7, and again as Σπ_i P_ii = (0.5 + 0.5 + 3)/7 = 4/7. `half` feedback now also names equal averaging. Clear of key 0.4286, `half` 0.5, `accept-top` 0.75. |
| 8 | fixed | Bayes with uniform π: P(A yesterday given B) = P_AB = 0.8; the reversible reading gives P_BA = 0.2 (`forward`); 0.5 is an even split over the two predecessors A and C. Feedback for `half` and `forward` swapped to these mistakes; values unchanged. |
| 9 | fixed (slip values changed) | `one-minute`: e^{−3}·9/2 × e^{−2}·2 = 9e^{−5} = 0.0606, two ways. `sum`: 0.04462 + 0.07326 = 0.1179, by hand and by SciPy. Set to 0.0606 and 0.1179, tol 0.001; clear of key 0.00327 and `merged` 0.0076. |
| 10 | fixed | Risk-neutral p = (e^{rΔt} − d)/(u − d) = 0.2/0.45 = 4/9 only at r = 0 (Shreve I, 1.1); explain now says so and that with a rate the discounted price is the fair game. |
| 11 | fixed | 0.2 × 5 = 1, and no named route (dropping chances gives −2, equal average gives 2) reaches 5; feedback now names the equation solved and the 0.2 still needed. |
| 12 | fixed | A fair bet on chance 1/26 must return R with R/26 = 1, so R = 26 for a £1 stake: a net 25, odds of 25 to 1, and the wait 26^11 + 26^4 + 26 already uses the 26 return; prose now says "fair odds: a winning £1 bet returns £26". |
| 13 | fixed | N_10 is set by the arrival clock, independent of the sizes, so E[S | N = n] = nE[Y] and the tower rule gives E[N]E[Y] (Grimmett and Stirzaker, conditional expectation and random sums); it is not a stopping time of the sizes in l19's sense. Prose cites Random sums (random-vars l18) and gives independent increments as the martingale reason; explain conditions on the count. |

Keys and hidden tests: none changed. Slip values changed: review-4 items[6] `third` 0.3333 replaced by `stay` 0.5714; review-4 items[7] `one-minute` 0.0558 to 0.0606 and `sum` 0.0222 to 0.1179.

Concepts script: three checks encoded the old defects and were re-pointed to the fixed text (F3, F7, F8; stated in its docstring). The F9 checks were already right and now pass. 112 checks, 0 failing, exit 0.

Gates on the nine edited files: validator 0 errors; voice scan 35 gives 0 and 0; `markov-L4-5-concepts.py` exit 0; `run-number-scripts.mjs --only markov` 5 of 5 passed; `grade-all.mjs --file` 0 failures on each; playthrough desktop and `--mobile` all passed (18 runs).

## Fix-pass read

Fresh reader, blind to the audit above and to the earlier reviews. Scope: the content strings changed by commit `35ecf9f8` (`git show 35ecf9f8 -- app/content/courses`), read at `321d59f8`. Script: `docs/reports/markov-L4-5-fixread.py` (exit 0, 55 checks; two of them document the imprecise rows). Sources: Norris, *Markov Chains*; Levin, Peres and Wilmer, *Markov Chains and Mixing Times* (LPW); Williams, *Probability with Martingales*; Grimmett and Stirzaker, *Probability and Random Processes* (GS); Shreve, *Stochastic Calculus for Finance I*.

### Ledger

| # | file | JSON path | claim | verdict | basis |
|---|---|---|---|---|---|
| 1 | homework-4 | items[1].widget.options[0].text | A chain on a line that moves only to a neighbour or stays, and can step both ways between neighbours, must be reversible | correct | Both-way positive steps make the chain irreducible; $\pi_{i+1} = \pi_i P_{i,i+1}/P_{i+1,i}$ solves detailed balance (LPW 2.5; Norris 1.9). Script: 2,000 random birth-death chains, all balanced. |
| 2 | homework-4 | items[2].feedback.byKey.forward | $P_{BA}$ "would be right only for a reversible chain" | imprecise (minor) | $P(X_t = A \mid X_{t+1} = B) = \pi_AP_{AB}/\pi_B$ equals $P_{BA}$ exactly when the A-B flows balance. That one pair can balance in a chain that is not reversible. Script: four-state chain, A linked only to B while B, C, D circulate; pair balanced, chain not reversible, backward chance 0.2 = $P_{BA}$. "Only" is false as stated; "if" would be true. |
| 3 | homework-4 | items[2].feedback.byKey.half | 0.5 splits evenly between A and C; weight by flows $\tfrac13 \times 0.8$ and $\tfrac13 \times 0.2$ | correct | Bayes: $0.8/3 \div (0.8/3 + 0.2/3) = 0.8$. Simulated 0.7992 on 1,000,000 steps, clear of 0.5 and 0.2. |
| 4 | homework-4 | items[8].model | The chain needs about 20 steps to lose most of the pull of its start | correct | Second eigenvalue 0.8626; total-variation distance from 0.40 is 0.051 at step 20, from 0.958 at step 0. |
| 5 | l13 | screens[6].prose | When every step up can be undone by a step down, a birth-death chain on a finite set is reversible, with the ratio formula | correct | The hypothesis gives $P_{i+1,i} > 0$ wherever $P_{i,i+1} > 0$, so the recursion defines a $\pi$ in detailed balance (LPW 2.5, Prop. 2.8 setting; Norris 1.9). Non-neighbour pairs balance at 0 = 0. Walker 0 to 5 checked: $\pi_{i+1} = 6\pi_i$. |
| 6 | l13 | summary.ideas[1] | Same statement in the summary | correct | As row 5. Finite state space keeps $\pi$ normalisable. |
| 7 | l14 | screens[11].explain.text | If D1 fails, D5 is cut off from every other dealer | correct | Edge list: D5's only link is D1. Removing D1 leaves D2, D3, D4 connected and D5 isolated (script). |
| 8 | l14 | screens[11].explain.text | Degree counts show which firms a network leans on most | correct | Stationary share is degree over $2\lvert E\rvert$ (LPW 1.4, 9.1); stated as a reading of the counts, not a theorem. |
| 9 | l15 | screens[1].widget.options[2].why | Flat steps are rejections, "and here they are most common at the two ends of the grid" | imprecise (minor) | Per visit the claim holds: $P_{ii}$ = 0.5, 0.256, 0.197, 0.130, 0.100, 0.146, 0.5. As a share of all flat steps in a long run, $\pi_iP_{ii}$ = 0.021, 0.022, 0.028, 0.025, 0.021, 0.028, 0.068: the low end 0.40 has fewer flat steps than 0.50 or 0.65. "Most common at the two ends" reads as the count, which is false at 0.40. |
| 10 | l15 | screens[2].feedback.correct | After about 18 steps most of the start's pull has gone | correct | Excess chance at 0.40 is 0.017 at step 18, from 0.958; total-variation distance 0.069. |
| 11 | l15 | screens[2].explain.text | The pull never vanishes exactly, but here it halves about every five steps | correct | Half-life $\ln 0.5/\ln 0.8626 = 4.69$ steps; five-step total-variation ratios 0.486, 0.479, 0.478, 0.478 (LPW 12.2, relaxation time). Distance stays positive at every finite step. |
| 12 | l16 | screens[8].prose | Trading has run for a long while; the time since the last trade is exponential, mean 0.5 | correct | Age at time $t$ is $\min(\text{Exp}(\lambda), t)$, exponential in the limit (GS 10.3 on current and excess life; Norris 2.4). Simulated at $t = 30$, 400,000 runs: wait ahead 0.5017, time since 0.4995, covering gap 1.0012, against 0.5 for a typical gap. |
| 13 | l16 | quiz[1].prose | Poisson at 2 a minute; exactly one trade in a quiet 10-minute stretch | correct | Setup now states the rate that the slips 0.9817 = $1 - e^{-4}$ and 0.1353 = $e^{-2}$ rely on. "Quiet" is apt: one trade against a mean of 20. |
| 14 | l16 | quiz[1].explain.text | Given one arrival its time is uniform; the rate plays no part | correct | $P(N_2 = 1)P(N_8 = 0)/P(N_{10} = 1) = 0.2$ for every $\lambda$ (Norris Thm 2.4.6; GS 6.12). Exact at three rates, simulated 0.2005 and 0.2006 on over 800,000 conditioned windows. |
| 15 | l17 | screens[4].explain.text | With interest rates at zero, $p = \tfrac49$ is the risk-neutral chance | correct | $\tilde p = (1 + r - d)/(u - d)$ with $r = 0$, $u = 1.25$, $d = 0.8$ gives $\tfrac49$ (Shreve I, 1.1 to 1.2). |
| 16 | l17 | screens[4].explain.text | With a rate, the discounted price is the fair game | correct | Shreve I, Thm 2.4.4. Check at $r = 5\%$: $\tilde p = \tfrac59$, discounted mean 100. |
| 17 | l17 | quiz[3].feedback.byKey.five | 5 solves $0.2x = 1$; known moves give 1.8, so $0.2x$ supplies 0.2 | correct | $1/0.2 = 5$; $1.5 + 0.3 = 1.8$; $2 - 1.8 = 0.2$; key $x = 1$. Slip 5 and slip 2 are clear of the key band 1 ± 0.001. |
| 18 | l21 | screens[7].prose | Fair odds: a winning £1 bet returns £26 | correct | Chance $\tfrac1{26}$ times return 26 is the stake, so expected profit is zero. This is 25 to 1 in bookmaker's terms, and it is the payout the martingale argument needs (Williams, E10.6; Li 1980). Wait $26^{11} + 26^4 + 26$ recomputed; rule simulated on ABA over three letters: 30.10 against 30, not 27. |
| 19 | l22 | screens[6].prose | The count is independent of the sizes, so Random sums gives $E[S_{10}] = E[N_{10}]E[Y]$ | correct | $E[S \mid N] = N\,E[Y]$ needs exactly that independence, plus finite means (GS 3.7, Thm 4). Simulated 4,195.7 against 4,200 (se 12). Dropping independence breaks it: counting trades before the first 500 lot gives $E[S] = 550$ against $E[N]E[Y] = 841$. Note: the lesson cited is titled "Sums of a random number of terms"; "Random sums" is the short name this lesson already used. |
| 20 | l22 | screens[6].prose | Each later stretch adds volume independent of the past, so $S_t - \lambda tE[Y]$ is a martingale | correct | A compound Poisson process has independent, stationary increments with mean $\lambda sE[Y]$ (GS 6.12; Norris 2.4). Simulated increment over 5 minutes, less 2,100: mean −0.9 after a low past and 0.0 after a high past (se about 5). |
| 21 | l22 | screens[6].explain.text | Given the count, the total is that many independent sizes; averaging over the count gives $E[N]E[Y]$ | correct | Tower rule. Wald's identity is no longer cited here, which is right: its hypotheses are a stopping time (or $\{T \ge n\}$ independent of $Y_n$), $E[T] < \infty$ and $E\lvert Y\rvert < \infty$ (GS 10.2, Lemma 9; Williams 10.10). An independent count meets the general form, but conditioning is the direct argument. |
| 22 | review-4 | items[6].widget.wrong[1] | Slip "stay" = 0.5714 ± 0.002 | correct | Two ways: $1 - \tfrac37 = \tfrac47$; and $\tfrac17 \cdot \tfrac12 + \tfrac27 \cdot \tfrac14 + \tfrac47 \cdot \tfrac34 = \tfrac47 = 0.5714$. Bands: key 0.4286, 0.5, 0.5714, 0.75, each ± 0.002, all disjoint. Key simulated 0.4288 on 2,000,000 steps. |
| 23 | review-4 | items[6].feedback.byKey.stay | That is the share of steps that stay put, $\tfrac47$ | correct | As row 22. |
| 24 | review-4 | items[6].feedback.byKey.half | 0.5 is the proposal chance, or the three move chances averaged equally | correct | Two ways: proposal chance $\tfrac12$; $(\tfrac12 + \tfrac34 + \tfrac14)/3 = \tfrac12$. |
| 25 | review-4 | items[7].widget.wrong[0] | Slip "one-minute" = 0.0606 ± 0.001 | correct | Two ways: $e^{-3}\tfrac{9}{2} \times e^{-2} \cdot 2 = 0.2240 \times 0.2707$; and $9e^{-5} = 0.06064$. Matches its feedback (means 3 and 2). |
| 26 | review-4 | items[7].widget.wrong[2] | Slip "sum" = 0.1179 ± 0.001 | correct | Two ways: $0.04462 + 0.07326$; and $18e^{-6} + 4e^{-4} = 0.11788$. Bands: key 0.00327 ± 0.0001, 0.0076 ± 0.0005, 0.0606 ± 0.001, 0.1179 ± 0.001, all disjoint. The compound slip (one minute and added, 0.4947) lands in no band. Key simulated 0.00325 on 4,000,000 windows. |

### Counts

26 rows: 24 correct, 0 wrong, 2 imprecise (both minor), 0 misleading, 0 unverified. Nothing here counts towards the convergence rule.

### Fixes (paste-ready)

R1. homework-4.json | items[2].feedback.byKey.forward | imprecise, minor. Replace the string with:

`"That is the chance of going from B to A. It would be right if the flows between A and B balanced, and here they do not. Yesterday's state given today's uses $P_{AB}$, A to B."`

Basis: $\pi_AP_{AB}/\pi_B = P_{BA}$ if and only if $\pi_AP_{AB} = \pi_BP_{BA}$, a condition on the one pair (LPW 1.6, time reversal).

R2. l15-sampling-by-chain.json | screens[1].widget.options[2].why | imprecise, minor. Replace the string with:

`"A converged chain keeps moving. Flat steps are rejections, and here a step is most likely to be rejected at the two ends of the grid."`

Basis: $P_{ii}$ is 0.5 at both ends and at most 0.256 elsewhere; the count of flat steps, $\pi_iP_{ii}$, is not largest at 0.40.

### Checks run

`docs/reports/markov-L4-5-fixread.py`: exit 0. It rebuilds the Metropolis chains from the content JSON, recomputes each changed slip two ways, tests band separation, and simulates rows 3, 12, 14, 18, 19, 20, 22 and 26. No content was edited, so the validator and playthrough were not rerun.
