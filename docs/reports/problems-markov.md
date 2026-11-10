# Problem sets: markov (brief `docs/briefs/chained.md`)

Files: `app/content/courses/markov/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-markov-numbers.py` (exits 0). The course writes distributions as row vectors, $\boldsymbol{\pi}_{k} = \boldsymbol{\pi}_0\mathbf{P}^k$, with rows of $\mathbf{P}$ adding to 1; every set follows that.

Every numeric part ends with a form sentence ("Give a decimal to 2 places.", "Give a fraction, or a decimal to 4 places."), its `tol` accepts that rounding, and the numbers script checks that the value printed in `feedback.correct` is accepted by the part's own `tol`. Where a part hands the learner a rounded value (3.33 months, 6.67 minutes), the script also checks that the answer from the rounded value is accepted.

## Level 1

File: `problems-1.json` ("Problems: chains, paths and regimes", 45 minutes).

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-thin-book | 4 (4 / 0) | l2, l4 | 3 |
| problems-1 | p-two-losses | 4 (4 / 0) | l1, l2, l3 | 4 |
| problems-1 | p-margin-calls | 4 (3 / 1) | l1, l3 | 4 |
| problems-1 | p-carry-pause | 5 (5 / 0) | l2, l4 | 5 |

Typed parts 16 of 17. Every lesson appears in at least one problem, and every problem draws on two or more.

Chains. p-thin-book: a matrix estimated from transition counts ($\hat p_{TT} = 0.7$), a two-step chance from it (0.535), the mean Thin spell (3.33 minutes), then the long-run Thin share from the spell lengths ($\tfrac13$, which the record's 20 of 60 moves confirms). p-two-losses: a rule that stops a trader after two losses in a row, written as a chain with an absorbing stop; one path (0.0216), stopped by trade 2 (0.18), by trade 3 (0.306, cumulative absorption), then the stop on trade 4 exactly (0.1098). p-margin-calls: a first return within two days (0.65, against $(\mathbf{P}^2)_{MH} = 0.6$ as a `wrong` value), ever back ($\tfrac57$), $f_H = \tfrac{34}{35}$, then the judgement that every account is liquidated in the end because only X is closed. p-carry-pause: a stressed spell (3.33 months), the calm share ($\tfrac67$ from run lengths, as l4 teaches), the long-run P&L of a carry trade (£1.43m a month), the expected month after stress (−£4.7m), then a rule that trades only after calm months (£2.1m a month). Each later part restates the value it needs, and its `wrong` list holds the value from the commonest slip before it (0.535 in place of 0.7; 0.65 in place of $\tfrac57$; a stressed spell of 1.43 months).

Level 1 teaches no $\boldsymbol{\pi}\mathbf{P} = \boldsymbol{\pi}$ (that is l5), so the long-run shares come from mean run lengths, as in l4, and the hitting chances from the return argument of l3 and homework-1.

Checks (level 1):

| check | result |
|---|---|
| numbers script | 361 checks, 0 failures |
| validator | 0 errors, 0 warnings on the file |
| playthrough `--local-cdn` | green (4 problems, 17 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault |
| voice scan 35 (course folder) | 0 and 0 |

Fresh-check: 0 hits at the gate. At triage settings (`--min-run 8 --min-share 0`) one hit, "give a decimal to # places using # how many", against `counting-chance/problems-3.json` items[2], share 0.06: the form sentence, stock phrasing. The settings are new to the course: no lesson, review or homework uses a Deep and Thin order book, a two-loss stop, margin calls or a paused carry trade. The bull and bear numbers, the A, B, Default ratings and the weather chain of the lessons are not reused.

## Level 2

File: `problems-2.json` ("Problems: long runs and absorption", 50 minutes). Level 2 writes $P$ and $\pi$ without bold, as its lessons do.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-2 | p-band-days | 5 (4 / 1) | l5, l6 | 3 |
| problems-2 | p-strategy-trial | 4 (4 / 0) | l5, l6, l8 | 4 |
| problems-2 | p-rfq-rounds | 5 (4 / 1) | l7, l8 | 4 |
| problems-2 | p-merger-arb | 5 (5 / 0) | l7, l8 | 5 |

Typed parts 17 of 19 (one `expression`). Every lesson appears in at least two problems, and every problem draws on two or more.

Chains. p-band-days: a two-step chance on a three-state band chain (0.14), the ratio $\pi_B = 0.2\pi_I$ from one column of $\pi P = \pi$, the normalised $\pi_I = \tfrac{20}{29}$, the judgement that the chain is irreducible and aperiodic so $\pi$ attracts every start, then a mean-reversion rule's long-run P&L ($\tfrac{7}{29} \approx$ £0.24k a day). p-strategy-trial: a reducible chain (Test, a live class On and Off, Shut); On in two weeks (0.42), the On share of the live class (0.8), the chance of ever going live (0.6), then the start-dependent limit $0.6 \times 0.8 = 0.48$. Part 3 does not use part 2; both feed part 4. p-rfq-rounds: a request for quote with re-quotes; $h_C = 0.2 + 0.5q$ as an expression, $q = 0.6$, expected rounds $t_Q = 1.75$, the trade chance under a tighter quote ($\tfrac{56}{85} \approx 0.6588$), then the judgement that the old quote earns more per request (£30 against £26.35). p-merger-arb: completion from Review (0.625) and from Announced (0.575), expected months to resolution (3.5), the share's expected value at resolution (£8.30), then the break-even price after holding costs (£8.23). Each later part restates the value it needs, and its `wrong` list holds the value from the commonest slip before it (the dropped $0.5\pi_B$ gives $\pi_I = 0.7407$; 4.5 months gives £8.21).

Checks (level 2):

| check | result |
|---|---|
| numbers script | 788 checks with levels 1 and 2, 0 failures |
| validator | 0 errors, 0 warnings on the file |
| playthrough `--local-cdn` | green (4 problems, 19 parts) |
| playthrough `--mobile` | green; 440 px shots read, the matrix canvas fits |
| voice scan 35 (course folder) | 0 and 0 |

Fresh-check: 0 hits at the gate. At triage settings three hits, all against `problems-1.json` and all form sentences or "using # from part # what is the chance" (shares 0.06 or less): stock phrasing. No lesson, review or homework uses a price band, a strategy trial, a request for quote or a takeover; the order queue, the loan ratings and the fair walks of l7 and l8 are not reused.

## Level 3

File: `problems-3.json` ("Problems: walks, ruin and barriers", 50 minutes). Notation as l9 to l12: $S_n$, $P_i$, $D_i$, $r = \tfrac{1-p}{p}$, $\Phi$.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-3 | p-maker-edge | 4 (4 / 0) | l9, l12 | 3 |
| problems-3 | p-barrier-note | 5 (4 / 1) | l9, l11, l12 | 5 |
| problems-3 | p-stake-size | 4 (4 / 0) | l9, l10 | 4 |
| problems-3 | p-pairs-exit | 5 (4 / 1) | l9, l10 | 4 |

Typed parts 16 of 18. Every lesson appears in at least one problem (l11 in one, the others in two or more), and every problem draws on two or more.

Chains. p-maker-edge: a ±£2 walk with $p = 0.55$; one trade's variance (3.96), the 400-trade standard deviation (£39.80), the normal chance of being down ($\Phi(-2.01) \approx 0.022$; the exact binomial 0.0199 also passes), then the trades needed for a 1% tail with $z = 2.33$ (538; `tol` 2 also takes 536 from $z = 2.326$). p-barrier-note: a binomial price model with a knock-out barrier at $-3$; paths ending at $-4$ (495), touching paths ending at $-2$ by reflection (the same 495), the touch chance ($\tfrac{1588}{4096} \approx 0.3877$, checked by listing all 4,096 paths), the note's fair price (£61.23), then the judgement that drift breaks reflection and calls for simulation. p-stake-size: one trade's edge (−£4), the chance of £600 to £1,000 at £100 stakes (0.5026) and at £200 stakes (0.5515), then the expected profit of the bolder plan (−£48.51). p-pairs-exit: target first ($\tfrac58$), expected days (15), expected ticks at exit (0, a fair walk), the expected P&L after financing (−£600), then the choice of exits by expected days ($+2$, $-6$: −£480). Each later part restates the value it needs; the `wrong` lists hold the slip from the part before (a variance of 4 gives £40 and $n = 543$; $i \times N = 40$ days gives −£1,600).

Level 3 teaches $D_i = i(N - i)$ for fair walks only, so the unfair walk in p-stake-size asks for chances and an expected profit read from the two ends, never a duration.

Checks (level 3):

| check | result |
|---|---|
| numbers script | 1,137 checks with levels 1 to 3, 0 failures |
| validator | 0 errors, 0 warnings on the file |
| playthrough `--local-cdn` | green (4 problems, 18 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault |
| voice scan 35 (course folder) | 0 and 0 |

Fresh-check: 0 hits at the gate. At triage settings six hits. Five are form sentences shared with problems-1 and problems-2. One, "log price is a fair walk in steps of", is against `l12-price-paths` screens[5]: the binomial price model is the lesson's own, but the note, the barrier at $-3$, 12 days and the questions are new. An earlier wording of p-maker-edge part 3 matched `l9` quiz[2] ("is close to normal, about what is the chance"); the question was reworded and the hit is gone. That part asks the same kind of question as l9's 52% strategy (a normal tail for a walk's P&L), with a new walk (±£2 at 0.55), and the item goes on to the variance and the trades for a 1% tail.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems markov)": the playthrough still shoots only part 1 (met again, as for conditional), and fresh-check triage is dominated by the required form sentences. Neither blocked a problem.

## Level 4

File: `problems-4.json` ("Problems: balance, networks, sampling and arrivals", 50 minutes). Numbers: the section "level 4 (problems-4.json)" at the end of `docs/reports/problems-markov-numbers.py`, added after the level 3 section; the earlier sections are unchanged. Notation as l13 to l16: $\pi_iP_{ij} = \pi_jP_{ji}$, $\pi_i = \tfrac{\deg(i)}{2|E|}$, $q_{ij}$ and $\min\left(1, \tfrac{w_jq_{ji}}{w_iq_{ij}}\right)$, rates $\lambda$.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-supplier-survey | 5 (4 / 1) | l14, l15 | 3 |
| problems-4 | p-taxi-rank | 5 (5 / 0) | l13, l16 | 4 |
| problems-4 | p-payment-audits | 5 (5 / 0) | l14, l16 | 4 |
| problems-4 | p-regime-sampler | 5 (5 / 0) | l13, l15 | 5 |

Typed parts 19 of 20. Every lesson appears in two problems, and every problem draws on two.

Chains. p-supplier-survey: a walk on a five-firm network (degrees 4, 2, 2, 1, 1); the share at a leaf (0.1), the walk's estimate of the late-payer rate (0.2 against a true 0.4), the judgement that $\min(1, \tfrac{\deg(i)}{\deg(j)})$ makes the target uniform, the chance a leaf stays (0.75), then the share of repeated records in the corrected walk (0.4). p-taxi-rank: merged Poisson streams give the chance an arrival is a taxi (0.6), balance gives the ratio 1.5, the empty share is $\tfrac{8}{65}$, passengers lost an hour (11.82), then the loss with a fourth space (7.28). p-payment-audits: a six-bank network with 7 links; $\pi_D = \tfrac{3}{14}$, the return time to F (14 hops), thinned audits at F ($\tfrac87$ a day), no audit in a day ($e^{-8/7} \approx 0.3189$), then the fewest hours for a 0.9 chance of one (17). p-regime-sampler: Metropolis-Hastings with an unequal proposal; $P_{LM} = 0.75$, $P_{MH} = 0.6$, $P_{ML} = 0.3$ from detailed balance, the rejection share (0.1), then the share a plain Metropolis rule gives Mid ($\tfrac{50}{77} \approx 0.6494$ against 0.5). Each later part restates the value it needs, and its `wrong` list holds the value from the slip before it (the uniform share $\tfrac16$ carries into $\tfrac86$ and $e^{-8/6}$; the inverted ratio into $\tfrac{27}{65}$ and 36.85).

The taxi rank is watched at arrivals, so it is a discrete chain with up chance $\tfrac{2.4}{4}$, as l16's merge rule gives; passengers arrive whatever the rank holds, so the share who find it empty is $\pi_0$. The script checks this by simulating the rank in continuous time. The audits pick a message at random from many in flight, so each lands on F with chance $\pi_F$ independently, the condition for thinning.

Checks (level 4):

| check | result |
|---|---|
| numbers script | 1,485 checks with levels 1 to 4, 0 failures |
| validator | 0 errors, 0 warnings on the file (no `[answer-form]`) |
| playthrough `--local-cdn` | green (4 problems, 20 parts) |
| playthrough `--mobile` | green; every part shot at 440 px and read, no fault |
| voice scan 35 (course folder) | 0 and 0 |

The script found one stated number wrong in a draft: the chance of an audit at F within 16 hours is 0.8983, not 0.8984; the feedback and explanation were corrected before commit.

Fresh-check (`--file`): 0 hits at the gate. At triage settings 31 hits: 24 are the form sentences ("give an exact fraction, or a decimal to # places"), 7 are "arrive as a Poisson process at # a minute" or "an hour" against l16, l22, review-4, review-5, homework-4, limits-thm review-2 and the topic exam. Stock phrasing. No lesson, review or homework uses a taxi rank, a supply-network survey, payment audits or a volatility-regime sampler; the knight, the venues, the dealer network, the hit-rate grid, the order queue and the 3 and 2 buy and sell rates are not reused.

## Level 5

File: `problems-5.json` ("Problems: martingales and stopping", 50 minutes). Numbers: the section "level 5 (problems-5.json)" at the end of the numbers script, after the level 4 section. Notation as l17 to l22: $S_n$, $T$, $r = \tfrac{q}{p}$, $E[S_T]$, $S_t - \lambda t\,E[Y]$, the casino rule $\sum \tfrac{1}{P(\text{prefix})}$.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-5 | p-cash-machine | 5 (5 / 0) | l17, l22 | 3 |
| problems-5 | p-signal-trial | 5 (5 / 0) | l17, l18, l19 | 4 |
| problems-5 | p-two-loss-cut | 5 (4 / 1) | l19, l20, l21 | 4 |
| problems-5 | p-capped-close | 5 (4 / 1) | l18, l19, l20 | 5 |

Typed parts 18 of 20. Every lesson appears in at least one problem (l21 and l22 in one, the others in two or three), and every problem draws on two or more.

Chains. p-cash-machine: compound Poisson withdrawals at 12 an hour; $E[Y] = £45$, the martingale forecast of the 4-hour total after £1,000 in hour 1 (£2,620), $E[Y^2] = 2{,}950$, the standard deviation of hours 2 to 4 (£325.88), then the cash for mean plus two standard deviations (£2,272). p-signal-trial: a losing signal in £2,000 steps between +£4,000 and −£6,000; the drift (−£200 a day), $r = \tfrac{11}{9}$, the target chance ($\tfrac{24381}{51001} \approx 0.4780$), the expected length (6.10 days), then the expected P&L at the end (−£1,219.51, which the rounded route −£1,220 also passes). p-two-loss-cut: a strategy with an edge of £60 a day cut after LL; the casino wait ($\tfrac{130}{9}$ days), the judgement that Wald's identity applies (stopping time, finite $E[T]$, bounded steps), the expected total (£866.67), then the total under an LWL rule (£1,152.38). p-capped-close: a fair walk closed at +1 or day 4; the chance of +1 (0.625), the average loss when it misses (−£1,666.67), $E[T] = 2.375$, the standard deviation at the close from $S_n^2 - n$ (£1,541.10), then the judgement that dropping the cap fails all three conditions. Each later part restates the value it needs, and its `wrong` list holds the value from the slip before it ($r = \tfrac{9}{11}$ gives 0.7141; $\tfrac{1}{0.09}$ days gives £666.67; $\operatorname{Var}(Y)$ in place of $E[Y^2]$ gives £182.48 and then £1,984.97).

The script checks each martingale answer against a second route: first-step equations solved with numpy for the ruin chance, the duration and the two pattern waits; all 16 paths of the capped walk listed for its chance, mean loss, $E[T]$ and $E[S_T^2]$; seeded simulations of the trial, the cut and the 3-hour withdrawal total; and the random-sum variance formula for the compound total.

Checks (level 5):

| check | result |
|---|---|
| numbers script | 1,807 checks with levels 1 to 5, 0 failures |
| validator | 0 errors, 0 warnings on the file (no `[answer-form]`) |
| playthrough `--local-cdn` | green (4 problems, 20 parts) |
| playthrough `--mobile` | green; every part shot at 440 px and read |
| voice scan 35 (course folder) | 0 and 0 |

Shots: the prose "reaches +£4,000" and "+£1,000" broke between "+" and "£" at 440 px; the prose now says "£4,000 up" and "£1,000 up" (inbox bullet). The validator's `[shown-arithmetic]` rule caught "$60 \times 19.206 \approx 1152.38$" (it is 1,152.36); the factor is now printed as 19.2063.

Fresh-check (`--file`): 0 hits at the gate. At triage settings 22 hits: 14 are form sentences; the rest are "as a Poisson process at # an hour" (problems-4, the topic exam), "what is the standard deviation of the P&L" (l9, l18, review-3, random-vars problems-3), "starts # above the stop and # below the target" (l19 screen 11, a fair £1,000 strategy from 4 and 2) and "makes or loses # a day with equal chance" (homework-5, a fair £500 strategy closed at ±£5,000). Stock phrasing. p-capped-close uses l20's idea of a time cap, with a cap of 4 days in place of 100 bets and new questions (the closing day and the spread at the close); no lesson, review or homework uses a cash machine, a losing signal trial or an LL or LWL cut.

## Engine limits (levels 4 and 5)

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems markov levels 4 and 5)": a leading "+" before "£" breaks at the line end at 440 px, and fresh-check triage is still dominated by the form sentences (met again). The playthrough now shoots every part at 440 px, so the earlier part-1-only bullet no longer applies to these sets.
