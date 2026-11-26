# Concept audit, round 2: markov levels 4 and 5

Blind read of `app/content/courses/markov` at `668f3e02`: l13 to l16, review-4, homework-4, problems-4 (level 4) and l17 to l22, review-5, homework-5, problems-5 (level 5). Stage 1, full ledger. The ledger and the findings below were written before any earlier review, audit or author report for this course was opened.

- Ledger: `docs/reports/audit-markov-4-5-r2-ledger.md`, 217 rows: 206 correct, 1 wrong, 10 imprecise, 0 misleading, 0 unverified.
- Script: `docs/reports/markov-L4-5-concepts-r2.py`, 71 checks. It exits 1 on one failing check, which is finding 1. The other 70 pass. NOTE lines print the evidence for the imprecise findings.

Sources: Norris, *Markov Chains* (N); Levin, Peres and Wilmer (LPW); Williams, *Probability with Martingales* (W); Grimmett and Stirzaker (GS); Durrett (D).

## What was checked hardest

- Optional stopping: the three cases in l19 match W 10.10 (a), (c), (b). Every use names a case that does hold. The +1 stop, the floor, the cap and doubling were recomputed exactly.
- Wald's identity: see finding 2.
- Detailed balance: stated as sufficient, not necessary (l13 screens 7 to 9), with the cycle and the one-way arrow as counterexamples. Recomputed.
- Reversal: `P*_ji = pi_i P_ij / pi_j` in homework-4, checked by a 400,000-step simulation (0.799 against 0.8).
- Convergence: l14 and review-4 separate "pi exists", "time shares converge" and "P^k converges". The periodic square was recomputed.
- MCMC: burn-in (half-life 4.69 steps), move share (0.7876), accuracy at 100,000 steps (median 0.0029), the move-only record, and the homework sampling sds (0.0039 and 0.0050) all agree with the text.
- Poisson: thinning independence, inspection paradox, conditional uniformity and the negative-binomial item were simulated.
- Pattern waits: every stated wait was recomputed by an exact first-step solve, ABRACADABRA included.
- Slips: every `wrong[]` value whose feedback names a mistake was recomputed. One feedback line misnames its value (finding 6). All slip bands are clear of their keys.

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `l22-arrivals-fair-game` | `screens[8].explain.text` | **wrong**, minor | "The mean is $50 \times 0.2 = 10$ lots: $t$ lots a minute." The rate is not $t$ lots a minute. | The mean rate is $\lambda E[Y] = 5 \times 0.2 = 1$ lot a minute, so the mean after $t$ minutes is $t$ lots (GS 6.13, compound Poisson mean). The next sentence, "Inventory minus $t$", is right and shows the intent. A wording slip, but false as stated. | Replace the first sentence with: "The mean is $50 \times 0.2 = 10$ lots: one lot a minute, so $t$ lots after $t$ minutes."

2. `l19-optional-stopping` | `screens[7].prose`, `summary.ideas[2]` | **imprecise**, serious | Wald's identity is stated for "independent steps with mean $\mu$, and a stopping time $T$ with finite mean". That is not enough. | D 4.8 and GS 10.2 need identically distributed steps with a finite mean (or bounded steps, which is condition (2) for $S_n - n\mu$). The course's own doubling game is the counterexample: the stakes $\pm 2^{n-1}$ are independent with mean 0, $E[T] = 2$, yet $E[S_T] = 1$ (script NOTE). Problems-5 `p-two-loss-cut` part 3 states the conditions correctly, so only this screen and the summary need the fix. | Prose: "Optional stopping also handles sums. Take independent steps with the same distribution and a finite mean $\mu$, and a stopping time $T$ with finite mean. Then **Wald's identity** says $E[S_T] = \mu\,E[T]$. For bounded steps it comes from stopping the martingale $S_n - n\mu$ under condition (2). The bars show the number of rolls until a die shows 6." Summary idea 3: "Wald's identity, $E[S_T] = \mu E[T]$, is optional stopping for sums of independent steps with the same distribution."

3. `l20-when-stopping-fails` | `screens[7].question`, `screens[7].widget.options[1]` | **imprecise**, minor | Single choice "which condition of optional stopping fails?" keys "the steps are not bounded". Conditions (1) and (3) fail too, and the rejected option begins "$T$ is not bounded", which is true. | With unlimited doubling $T$ has no cap, and the bankroll before the win is $-(2^k - 1)$, unbounded below (W 10.10). The key is the informative answer, but the question as worded has more than one true answer. Screen 3 of the same lesson asks the parallel question as "select all". | Question: "With unlimited money, conditions (1) and (3) fail at once: $T$ has no cap and the losses have no floor. Why does condition (2) fail too?" Option `time`, `why`: "True, and that is why condition (1) fails. But condition (2) allows unbounded $T$ when $E[T]$ is finite, and here $E[T] = 2$. Look at the steps." Same text for `feedback.byKey.time`.

4. `l19-optional-stopping` | `screens[9].explain.text` | **imprecise**, minor | "these games averaged £11.75, and 23 of 200 reached £100". If every game had stopped, 23 of 200 at £100 would average £11.50. | The chart ends at bet 8,000. A game is still running then with chance 0.0054, so 1.09 such games are expected in 200 (script, exact). The engine averages unfinished games at their last value, which is how 11.75 arises. The text gives two figures that do not agree without that fact. | Replace the first sentence with: "The plain walk loses 0.02 a bet, so its stopped mean falls: 23 of 200 games reached £100, and the average was £11.75. It sits above £11.50 because two games were still running when the chart ended at bet 8,000." The count of two is from the engine replay in `docs/reviews/perf-retrofit-8-scripts/l19_walk_sim.mjs`, read after the blind pass.

5. `l20-when-stopping-fails` | `screens[2].explain.text` | **imprecise**, minor | "At $L = 99$ the batch shows only about 40, because the mean comes from rare games lasting thousands of bets." The chart cannot show those games at all. | The canvas has `steps: 1000`, so the caption averages $\min(T, 1000)$, whose exact mean is 49.4 (script). Fresh batches centre on 49, not on 99, however often the learner presses New paths. | Replace the second sentence with: "At $L = 99$ the batch shows only about 40. The chart stops at 1,000 bets, and the mean of 99 comes from rare games lasting thousands of bets."

6. `l21-waiting-for-patterns` | `quiz[3].feedback.byKey.hh` | **imprecise**, minor | Slip value 4.4444 with feedback "You used $0.6^2$, the chance of HH." That mistake gives $1/0.36 = 2.7778$. | 4.4444 is the full HH wait, $1/0.36 + 1/0.6$ (script, first-step solve). The feedback names a different computation from the one its band catches. | "That is the wait for HH, $\tfrac{1}{0.36} + \tfrac{1}{0.6}$. The pattern is HT, with chance $0.6 \times 0.4$ and no overlap."

7. `l14-walks-on-networks` | `screens[6].explain.text` | **imprecise**, minor | "so there are 168 legal moves from square to square". | 168 is $|E|$, the number of unordered pairs of squares a knight's move apart. Ordered moves, "from square to square", number 336 (script). | "That is $2|E|$ for the knight's graph, so 168 pairs of squares are a knight's move apart."

8. `l14-walks-on-networks` | `screens[10].explain.text` | **imprecise**, minor | "Each edge adds its weight to both ends, so the strengths add to $2|E|$." | With weights the strengths add to twice the total weight (LPW 9.1). They add to $2|E|$ only when every weight is 1. Screen 5 of the lesson says it correctly. | "Each edge adds its weight to both ends, so the strengths add to twice the total weight, which is $2|E|$ when every weight is 1."

9. `l14-walks-on-networks` | `screens[4].explain.text` | **imprecise**, minor | "In general the mean return time to a state is $1/\pi_i$." | N Thm 1.7.7 is for an irreducible chain. The lesson's own quiz has a network in two pieces with two stationary distributions, where "$1/\pi_i$" has no single meaning. | "On a connected network the mean return time to a state is $1/\pi_i$."

10. `l16-arrivals` | `quiz[2].prose` | **imprecise**, minor | The feedback and explanation say the hour's count "is still Poisson", but the prose never says the orders form a Poisson process. | The key, 90, needs only linearity. The Poisson claim needs a Poisson process with a changing rate (GS 6.13). | Prose: "A venue's orders arrive as a Poisson process whose rate changes. The rate is 4 a minute for the first 10 minutes after the open, then 1 a minute for the next 50 minutes."

## Counts

| Severity | Serious | Minor | Total |
|---|---|---|---|
| wrong | 0 | 1 | 1 |
| imprecise | 1 | 8 | 9 |
| misleading | 0 | 0 | 0 |

Finding 2 covers two ledger rows, so 10 ledger rows are imprecise.

## Checked and left as correct

- l19 `screens[5].feedback.byKey.flip` says $r = p/q$ "gives the chance of going broke". That holds only because the start is the midpoint, 5 of 10. It is true as stated for this item.
- l19 `screens[4]` and l22 `screens[4]` take "$E[T]$ is finite" as given. It is true (a geometric bound; a Gamma time).
- l15 `screens[6]` states the ergodic theorem for "an irreducible chain". The course only has finite chains, where that is enough (N Thm 1.10.2).
- l13 `screens[1]` "filmed and run backwards, it looks the same" is said of a chain already at its stationary split.

## Runs

- `cd app && node tools/validate.mjs`: 0 errors, 4,609 warnings.
- `cd app && node tools/run-number-scripts.mjs --only markov` (venv Python first on PATH): 5 of 436 scripts, 5 passed, 0 new failures.
- `python docs/reports/markov-L4-5-concepts-r2.py`: exit 1, one failing check (finding 1), 70 passing.
- No playthrough, as instructed.

## Overlap with earlier reads

Read after the ledger and findings were written: `docs/reviews/audit-markov-4-5.md` (round 1 audit, its fix pass, fix-pass read and follow-up), its ledger, `review-problems-1.5-d.md` and `review-perf-retrofit-8.md` as cited there.

| | count |
|---|---|
| Conceptual findings by this audit only | 8 (1 wrong, 7 imprecise): findings 1, 2, 3, 6, 7, 8, 9, 10 |
| By earlier reads only | 22 (round 1 audit 13, its fix-pass read 2, earlier reviews 7), all fixed in the text audited |
| By both | 2 (imprecise): findings 4 and 5 |
| New `wrong` that no earlier read named | 1 (finding 1, minor) |

Notes on the overlap.

- Findings 4 and 5 were named by round 1 as an engine limit in `docs/BACKLOG-INBOX.md` (the stopped-walk canvas counts unfinished paths without saying so), with both screens cited. Round 1 raised no content finding and its ledger marks l20 `screens[2].explain` correct. This audit asks for the one-clause content fix as well, since the engine item is not yet built.
- Finding 2: the round 1 ledger marks l19 `screens[7].prose` correct, citing Grimmett and Stirzaker Lemma 10.2.9 "(iid steps)". The screen does not say the steps are identically distributed, and the next lesson's doubling game meets the stated hypotheses and breaks the identity. This audit holds the row imprecise.
- Finding 9: the round 1 ledger marks l14 `screens[4].explain` correct because every network on the screen is connected. This audit objects only to "In general".
- Finding 1 sits in l22 `screens[8].explain`, which no earlier read lists.
- All 22 earlier findings were re-read in their fixed form as ordinary ledger rows. Each is correct as it now stands (l13 birth-death condition, l15 rejection at the ends and burn-in wording, l16 "running for a long while" and the stated rate, l17 zero-rate caveat and slip `five`, l21 fair odds, l22 Random sums in place of Wald, review-4 slips, homework-4 feedback).

## Inbox

One bullet added to `docs/BACKLOG-INBOX.md` under "Raised later (audit markov):": a further slip whose feedback names a different computation (l21 `quiz[3]` `hh`), as evidence for the slip-recompute check already requested there. The existing stopped-walk bullet covers findings 4 and 5.

## Fix pass

Opus fixer, content commit `edc8ef32` (course folder only; six lesson files). No key, slip value, tolerance or hidden test changed. Scratch replay: `scratchpad/fix-mk45r2/l20s2.mjs` (not committed).

| # | Status | Fixer's basis |
|---|---|---|
| 1 | fixed differently | Compound Poisson mean is $\lambda t E[Y]$ (GS 6.13); $\lambda E[Y] = 5 \times 0.2 = 1$ lot a minute, so 10 lots in 10 minutes and the next sentence's "minus $t$" stays right. Text: "10 lots, a drift of $5 \times 0.2 = 1$ lot a minute." |
| 2 | fixed differently | Durrett Thm 4.8.6 (Wald): i.i.d. steps with $E\lvert X_1\rvert < \infty$ and a stopping time with $E[T] < \infty$. Own check of the counterexample: stakes $\pm 2^{n-1}$ are independent, mean 0, $E[T] = 2$, yet $S_T = -(2^{T-1} - 1) + 2^{T-1} = 1$ on every path; they fail "one shared distribution" (and bounded steps), so l20 stays consistent. Prose now says "independent steps that all share one distribution with finite mean $\mu$, and a stopping time $T$ with finite mean", and "for bounded steps it is condition (2) applied to $S_n - n\mu$"; summary idea 3 names both hypotheses. The die example meets both (i.i.d., bounded, geometric $T$). Problems-5 `p-two-loss-cut` already gives the bounded-step form. |
| 3 | fixed differently | Unlimited doubling: $T$ geometric (no cap, (1) fails), stopped bankroll $-(2^k - 1)$ before the win (no floor, (3) fails), stakes unbounded ((2) fails) (W 10.10). Question now grants (1) and (3) and asks why (2) fails; the `time` option becomes the false inference "$T$ is not bounded, so condition (2) cannot apply", so only `steps` is true. Key unchanged. |
| 4 | fixed | Engine replay (`perf-retrofit-8-scripts/l19_walk_sim.mjs`, rerun): up 23, down 175, open 2, mean 11.75; $2300 + 50 = 2350$ over 200. Text names the two unfinished games. |
| 5 | fixed | Own replay of seed 2, run 0, $L = 99$: average length 40.0 (so "about 40" is this batch); exact $E[\min(T, 1000)] = 49.42$ by forward recursion, $P(T > 1000) = 0.025$. Text now says the chart stops at 1,000 bets. |
| 6 | fixed | Biased coin, $p = 0.6$: HH wait $= 1/p + 1/p^2 = 1.6667 + 2.7778 = 4.4444$; $1/0.36$ alone is 2.7778. Feedback now names the HH wait. |
| 7 | fixed | 8 by 8 knight's graph: degree sum 336 (ordered moves), so $\lvert E\rvert = 168$ unordered pairs (handshake lemma). |
| 8 | fixed | Handshake lemma with weights: $\sum_i w(i) = 2 \sum_e w_e$ (LPW 9.1); equals $2\lvert E\rvert$ only for unit weights. Split into two sentences. |
| 9 | fixed | Kac / Norris Thm 1.7.7 needs irreducibility; a finite connected network gives an irreducible, positive recurrent walk. Text: "On any connected network ...". |
| 10 | fixed | The count of a Poisson process with rate $\lambda(t)$ over $[0, 60]$ is Poisson with mean $\int \lambda = 90$ (GS 6.13); the prose now states the process, so the feedback's "still Poisson" has its hypothesis. |

Gates on the six edited files: validator 0 errors; `voice-scan.py 35` 0 and 0; `markov-L4-5-concepts-r2.py` exit 0 (finding 1's check now passes; the NOTE lines keyed on old text no longer print, no re-pointing needed), `markov-L4-5-concepts.py` exit 0, `markov-L4-5-fixread.py` exit 0; `run-number-scripts.mjs --only markov` 5 of 5 passed; `grade-all.mjs --file` 0 failures on each; playthrough desktop and `--mobile` all passed on each.

## Fix-pass read

Reader: fresh Fable reader, blind to this audit, the markov reviews and the markov report scripts until the rows below were written. Diff read: `git show edc8ef32 -- app/content/courses` (markov l14, l16, l19, l20, l21, l22; 14 changed lines). Script: `docs/reports/markov-L4-5-fixread-r2.py` (exit 0, 39 checks). It replays the walk canvas (mulberry32, seed × 7919, one uniform and one Box-Muller normal per step) for every batch figure, and computes the exact capped laws beside them.

Sources: Williams, *Probability with Martingales*, §10.10 (Doob's optional stopping theorem: (i) $T$ bounded; (ii) $X$ bounded and $T$ a.s. finite; (iii) $E[T] < \infty$ and $|X_n - X_{n-1}| \le K$). The lesson's (1), (2), (3) are Williams (i), (iii), (ii). Durrett, *Probability: Theory and Examples* (5th ed.), Thm 4.8.5 ($E[N] < \infty$ and $E(|X_{n+1} - X_n| \mid \mathcal F_n) \le B$ on $\{N > n\}$) and Thm 4.8.6 with Thm 2.6.2 (Wald's equation: i.i.d. steps, $E|X_1| < \infty$, stopping time $N$ with $E[N] < \infty$, then $E[S_N] = E[X_1]E[N]$).

| # | File | JSON path | Claim | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | l14 | screens[4].explain.text | On any connected network the mean return time to state $i$ is $1/\pi_i$ | correct | Kac's formula for an irreducible finite chain (Norris, *Markov Chains*, Thm 1.7.7; Levin, Peres and Wilmer, Prop. 1.19). No aperiodicity needed. Script: first-step solve on the venue graph gives $\tfrac83, 4, 4, 8$; also holds on a bipartite path and a weighted triangle. |
| 2 | l14 | screens[6].explain.text | 336 is $2\lvert E\rvert$, so 168 pairs of squares are a knight's move apart | correct | Handshake lemma. Script enumerates the board: degree classes 4, 8, 20, 16, 16 squares, 168 unordered pairs. The new wording removes the old ambiguity between 168 pairs and 336 directed moves. |
| 3 | l14 | screens[10].explain.text | Each edge adds its weight to both ends, so the strengths add to twice the total weight | correct | Derivation: $\sum_v s_v = \sum_{(u,v,w)} 2w$. Script on the weighted test triangle: 12 = 2 × 6. |
| 4 | l14 | screens[10].explain.text | With every weight 1 that is $2\lvert E\rvert$ | correct | Special case of row 3. |
| 5 | l16 | quiz[2].prose | Orders arrive as a Poisson process whose rate changes: 4 a minute for 10 minutes, then 1 a minute for 50 | correct | Inhomogeneous Poisson process (Ross, *Introduction to Probability Models*, §5.4.1): the count is Poisson with mean $\int \lambda = 90$. The stated model now supports the feedback line "the count is Poisson". Script: mean 90.00, variance 90.0. |
| 6 | l19 | screens[7].prose | Independent steps sharing one distribution with finite mean $\mu$, and a stopping time $T$ with finite mean, give $E[S_T] = \mu E[T]$ | correct | Exactly Durrett Thm 2.6.2 / 4.8.6: i.i.d., $E\lvert X_1\rvert < \infty$, $E[N] < \infty$. No bounded-step or finite-variance condition is needed, and none is claimed. Script: die total 21.00; a non-stopping time (the roll before the first 6) gives 15, not 17.5. |
| 7 | l19 | screens[7].prose | For bounded steps it is condition (2) applied to the martingale $S_n - n\mu$ | correct | $S_n - n\mu$ has increments $X_n - \mu$, bounded when the steps are; with $E[T] < \infty$ this is Williams 10.10(iii). The restriction "for bounded steps" is right: for unbounded i.i.d. steps the proof needs Durrett Thm 4.8.5, not the lesson's (2). The die has bounded steps. |
| 8 | l19 | screens[9].explain.text | 23 of 200 games reached £100, and two still running at bet 8,000 bring the average to £11.75 | correct | Engine replay, seed 6: 23 hit £100, 175 hit £0, 2 unfinished at £4 and £46; $(2300 + 50)/200 = 11.75$. Exact: $P(\text{running at } 8000) = 0.0054$, mean at stop 12.07. |
| 9 | l19 | summary.ideas[2] | Wald's identity needs independent steps with one shared distribution and finite mean, and a stopping time with finite mean | correct | Same hypotheses as row 6. "Needs" reads as the stated hypotheses; they are sufficient, not minimal (a common mean with bounded $E\lvert X_k\rvert$ also works), which no learner is harmed by. |
| 10 | l20 | screens[2].explain.text | At $L = 99$ this batch shows only about 40, since the chart stops at 1,000 bets and the mean of 99 comes from rare games lasting thousands | correct | Engine replay, seed 2, 300 paths: capped average 39.98 (6 unfinished). `tauMean` counts an unfinished game as 1,000. Exact: $E[\min(T, 1000)] = 49.4$ and $P(T > 1000) = 0.025$, so 2.5% of games carry half of the 99. Both stated causes hold. |
| 11 | l20 | screens[7].question | With unlimited money $T$ has no cap and the losses have no floor, so conditions (1) and (3) fail | correct | $T$ is geometric, so unbounded: (1) fails. The stopped bankroll reaches $-(2^n - 1)$ with chance $2^{-n}$, so it is unbounded below: (3) fails although $T < \infty$ a.s. (Williams 10.10(i), (ii)). |
| 12 | l20 | screens[7].widget.options[steps] (key) | Condition (2) fails because the steps are not bounded: the last stake has infinite mean | correct | Step $n$ is $\pm 2^{n-1}$, so no $K$ exists: Williams 10.10(iii) fails. Durrett's weaker Thm 4.8.5 fails too, since the conditional step size on $\{T > n\}$ is $2^n$. $E[2^{T-1}] = \sum \tfrac12 = \infty$. The conclusion fails as it must: $E[M_T] = 1 \ne 0$. Single keyed answer. |
| 13 | l20 | screens[7].widget.options[time].text | "$T$ is not bounded, so condition (2) cannot apply" is a wrong reason | correct | False as an answer to "why": (2) asks for $E[T] < \infty$, not bounded $T$, and $E[T] = 2$. Note: its premise and its conclusion are each true; only the "so" is false. The stem's "why" makes that the thing graded, so the key stays unique. |
| 14 | l20 | screens[7].widget.options[time].why | Unbounded $T$ breaks condition (1) only. Condition (2) allows it when $E[T]$ is finite, and here $E[T] = 2$ | correct | (2) and (3) put no bound on $T$ (Williams 10.10(ii), (iii)). $\sum k 2^{-k} = 2$. |
| 15 | l20 | screens[7].widget.options[mean], [mart] | "$E[T]$ is infinite" and "The bankroll is not a martingale" are false | correct | $E[T] = 2$. Stakes are fixed by past flips and bounded at each fixed $n$, so the bankroll is a martingale transform (Williams 10.7); script: $E[M_n] = 0$ at $n = 1, 5, 12$. |
| 16 | l20 | screens[7].feedback.byKey.time | Unbounded $T$ breaks condition (1) only. Condition (2) allows it when $E[T]$ is finite | correct | As row 14. |
| 17 | l21 | quiz[3].feedback.byKey.hh | 4.4444 is the wait for HH, $\tfrac{1}{0.6} + \tfrac{1}{0.36}$ | correct | HH overlaps itself at lengths 1 and 2, so the wait is $1/p + 1/p^2 = 4.4444$ (Williams §10.11, the ABRACADABRA argument; Li 1980). Simulation agrees. The old line gave $0.6^2$, whose reciprocal is 2.78, not the slip value. |
| 18 | l21 | quiz[3].feedback.byKey.hh | HT has chance $0.6 \times 0.4$ and no overlap | correct | No proper prefix of HT is a suffix, so the wait is $1/(pq) = 4.1667$; check $1/p + 1/q$. Simulation agrees. |
| 19 | l22 | screens[8].explain.text | The mean is $50 \times 0.2 = 10$ lots, a drift of $5 \times 0.2 = 1$ lot a minute | correct | Compound Poisson mean $\lambda t E[Y]$ (Ross §5.4.2); $\lambda E[Y] = 5 \times 0.2 = 1$ a minute, which matches "inventory minus $t$" in the next sentence. Simulation: mean 10.01, sd 7.07. |

Counts: 19 rows. correct 19, wrong 0, imprecise 0, misleading 0, unverified 0.

Wald and optional stopping, checked against the sources. l19 now states Wald with Durrett's exact hypotheses (i.i.d., finite mean, stopping time with finite mean) and limits the "condition (2)" derivation to bounded steps, which is where the lesson's (2) applies. l20's doubling game is consistent with them: its steps are neither bounded (Williams 10.10(iii)) nor conditionally bounded in mean (Durrett Thm 4.8.5), and they are not identically distributed, so Wald does not apply either. The reworded screens[7] has one keyed answer, `steps`, and each other option is false as an answer to the question asked.

Fixes: none needed. One optional tightening, not a finding (row 13): the `time` option's two clauses are each true and only the inference is false. If the author wants an option that is false outright, paste `"text": "Condition (2) needs $T$ to be bounded, and it is not"`; the `why` and `byKey.time` lines stand unchanged.
