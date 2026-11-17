# Problem sets: ito levels 1 to 3 (brief `docs/briefs/wave-c-author-ag.md`, `docs/briefs/chained-prompts.md`, `docs/briefs/chained.md`)

Files: `app/content/courses/ito/problems-1.json` to `problems-3.json`. Level 4 has its own author. Numbers: `docs/reports/problems-ito-numbers.py` (988 of 988 checks after the fix pass, exit 0). Commits: `074c470a` (level 1, with the script), `d72d1fbf` (level 2), `223fd3ab` (level 3).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-maker-tally | 4 (4 / 0) | l1, l3 | 4 |
| problems-1 | p-quarter-rally | 4 (4 / 0) | l2, l4 | 4 |
| problems-1 | p-realised-then-risk | 4 (4 / 0) | l3, l4 | 5 |
| problems-2 | p-cable-inverse | 4 (4 / 0) | l6, l7, l8 | 5 |
| problems-2 | p-cube-path | 4 (3 / 1) | l5, l6 (l3 table) | 4 |
| problems-2 | p-results-vol | 4 (4 / 0) | l5, l7 | 4 |
| problems-3 | p-touch-note | 4 (3 / 1) | l9, l12 | 5 |
| problems-3 | p-twin-shares | 4 (4 / 0) | l9, l10, l11 | 4 |
| problems-3 | p-bridge-closes | 4 (3 / 1) | l10, l11, l12 | 4 |

Every lesson of each level appears; every problem draws on two or more. Skills: level 1 `it-bm`, `it-calculus`; level 2 `it-calculus`, `it-martingale`; level 3 `it-pricing`, `it-martingale`, all from the level's lessons. Typed parts 12/12, 11/12, 10/12. The three choice parts are judgements (which integral a weighted sum of squared moves tends to; which root fits the note's boundary conditions; why the drift drops out between two closes). Each later part restates the value it uses. Every part that needs $\Phi$ names software or a normal table.

## Checks

1. Number script: 956 of 956, exit 0. Method 1 is closed form (fractions, sympy). Method 2: the binomial law of the 625 trades and a path simulation for the squared-move sum; Monte Carlo of GBM and of the integral $\int\sigma(t)\,dW$ on a grid; `quad` of the normal density; sympy differentiation for both Itô parts; `brentq` and the first-passage Laplace transform for the touch note; a bridge-corrected fine-grid and a daily simulation for the one-touch. Every `wrong` is rebuilt from its slip, every printed decimal is either in the stem or in a `shown` check at its printed places, and the rounded routes (0.3377, 0.6196, 0.6422, 0.006805) stay inside their key bands.
2. Validator: 0 errors; no warnings on these files.
3. Voice scan 35 on the course folder: 0 and 0 (8,553 sentences).
4. `fresh-check --files` on the three sets: 0 hits. Advisories, judged fine: $\int_0^1 W_t^2\,dW_t$ is named in homework-2 `h-iso-w2` (that item asks its variance by the isometry; p-cube-path builds the left sum on a path and expands the cube); $\int_0^1 W_t\,dt$ is named in homework-4 (a variance there; a limit of a weighted sum here); p-quarter-rally and p-cube-path share the times 0.25 and 0.75 with each other only.
5. `grade-all --file`: 12, 12 and 12 widgets, 0 failures each.
6. Playthrough `--problems ito/problems-<n> --local-cdn <pkgs>`: green for all three, desktop and `--mobile`. Part shots at 440 px read; one fault found and fixed (the coarse path's values as one comma list in one maths span overflowed the page; split into separate spans).

During authoring the checker found my own sets retelling each other (one table-source sentence used in six parts, two "chance of ending above" slip lines, two "no drag" lines) and two slip lines equal to the course's ("You used $\mu$ as the log drift", l4 S4 and r-gbm-above; "You moved the barrier towards the share", l12 Q3 and r-shift). All were rewritten.

## Closest material to each problem

| problem | lesson screen | quiz | review | homework | exam |
|---|---|---|---|---|---|
| p-maker-tally | l1 S7 (biased coin, drift of the mean path): there the drift is read off a slider; here the edge per trade, the pathwise sum of squares and a week's loss chance. | l1 q-fine-walk: sd of a fair fine walk; here a biased walk and its quadratic variation. | r-var-horizon: sd scales by $\sqrt{t}$ for VaR; here only one step of the chain. | h-drift-below: $P(X_4 < 0)$ for $0.5t + W_t$ given; here the drift and $\sigma$ are built from trades first. | e-qv-drift: QV of $3W - 2t$; here QV of a walk, exact on every path. |
| p-quarter-rally | l4 S4 ($P(S_1 < 100)$ from the start): here conditioned on a rally at 0.25, with only 0.75 of noise left. | l4 q-median, q-mean: from $t = 0$; here restarted at $S_{0.25}$. | r-gbm-above: from the start, no conditioning. | none conditions GBM on an earlier value. | e-var-two-times: a variance of a combination; here independent increments restart a forecast. |
| p-realised-then-risk | l3 transfer and S6 (sd $\sqrt{2T\Delta t}$ of the sum for $W$): here scaled by $\sigma^4$ and divided by $T$, then carried into a loss chance at a stressed $\sigma$. | l3 q-qv-var: variance of the sum for $W$; here for $\hat\sigma^2$. | r-qv-sd: same. | h-realised-vol: estimates $\sigma$ only; here also its error and the effect on $P(S_1 < 60)$. | none. |
| p-cable-inverse | l6 S6 ($d(\ln S)$ coefficient): here $f = 1/x$, a reciprocal exchange rate. | l6 q-ln-s; l8 q-exp-mean. | r-dlns (which line is $d\ln S$); r-which-mart. | h-moment-order ($E[S^p]$ order); h-discount ($\mu - r$ for $e^{-rt}S$): here $p = -1$ by Itô directly, then the product of means $e^{\sigma^2T}$ and the martingale condition. | e-pick-martingales: classify listed processes; here a drift solved for. |
| p-cube-path | l5 S1, S4 ($\sum W_k\Delta W_k$, squaring the path): here $W^2$ against $dW$ and the cube's expansion. | l5 q-left-small: the $W\,dW$ left sum on a three-step path. | r-left-sum: same task as the quiz. | h-iso-w2: variance of $\int W^2\,dW$; here its left sum and the source of the $3W\,dt$ term. | e-moment-and-isometry: moments and an isometry, not a sum on a path. |
| p-results-vol | l7 S8 ($\sigma(t) = 0.1 + 0.2t$, variance of $\ln S_1$): here a step in $\sigma$ at a results date, the term volatility, the median and a loss chance. | l5 q-det: constant integrand. | r-iso-det: $\int(2 + t)\,dW$ variance only. | none. | none. |
| p-touch-note | l9 S5 (forward checked in the equation): here $V = S^a$ solved for $a$, roots chosen by boundary conditions, a hedge. | l9 q-vt: $V_t$ from the equation. | r-pde-vt: same. | h-pde-check: a numerical residual. | e-theta-from-pde: theta from given Greeks; e-cubed-claim prices $S_T^m$ by expectation, not by the PDE with a barrier. |
| p-twin-shares | l9 S0 (slide $\Delta$ until a share hedges an option): here one share hedges another, then the noiseless book fixes the second drift. | l10 q-theta ($\theta$ from $\mu$, $r$, $\sigma$): here $\theta$ is never asked; it is implied by no arbitrage across two shares. | r-qmean ($E_Q[S_1]$ of one share): here the $Q$ mean of a ratio of two shares, which is not a martingale. | homework-3 h-derive-black (option on a forward, longform): one asset; here two on one $W$. | e-pick-martingales (classify processes): here a drift of $S_B/S_A$ is computed and priced. |
| p-bridge-closes | l12 S1 (touch chance of $W$ by reflection) and S6 (knock-out pricer): here reflection gives the touch chance between two known closes, and the path is weighted by survival. | l12 q-touch (touch chance from the start). | r-shift and r-parity (daily against continuous): here no shift and no parity; a per-path correction. | homework-3 h-barrier-report (four pricers of one knock-out): no bridge weight. | e-daily-touch and s3-touch (shifted barrier, touch chance from the start): here the chance between two closes, conditioned on both. |

No problem walks through several items in a row, and none retells a lesson screen: each joins two or three lessons in a chain the course does not run.

## Level 4

File: `app/content/courses/ito/problems-4.json` ("Problems: stochastic calculus at interview", 45 minutes). Numbers: `docs/reports/problems-ito-4-numbers.py` (325 of 325 checks, exit 0, after the session AF fix pass); `problems-ito-numbers.py` is untouched.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-band-wait | 5 (5 / 0) | l13, l14 | 5 |
| problems-4 | p-two-date-product | 4 (4 / 0) | l15, l16 | 4 |
| problems-4 | p-dividend-hedge | 4 (3 / 1) | l16, l17 | 4 |

Every lesson of the level appears; every problem draws on two. Skills `it-martingale`, `it-bm`, `it-calculus`, `it-pricing`, all from the level's lessons. Typed parts 12 of 13; the choice part is a judgement (which $dt$ coefficient the hedged book has once dividends are paid). The dividend yield is stated in the stem as a cash flow ($q\Delta S\,dt$), so the derivation needs only the steps of l17.

Chains. p-band-wait (re-authored in session AF, review finding 1): $E[X_\tau^3] = 75{,}000$ from $X_\tau^3 = 2{,}500X_\tau$ for $X = 30 + 2W$ stopped at 0 or 50; $c = 12$ and the stopped cubic martingale give $E[\tau X_\tau] = 4{,}000$; $A = E[\tau\,\mathbf 1_{\{X_\tau = 50\}}] = 80$; the result pair $E[\tau \mid X_\tau = 50] = 80/0.6 \approx 133.33$ and $E[\tau \mid X_\tau = 0] = (150 - 80)/0.4 = 175$ minutes. $P = \tfrac35$ and $E[\tau] = 150$ are given, so no part asks for $c$, $P$ or $E[\tau]$ alone; part 2 states the optional-stopping condition. p-two-date-product: $\text{Cov}(\ln S_1, \ln S_2) = 0.09$, the variance 0.45 of the sum, $E_Q[S_1S_2/100] = 25e^{0.18}$, the price $25e^{0.12} \approx 28.19$. p-dividend-hedge: the book's $dt$ coefficient, the bracket $r - q$, $V_t = qV \approx 2.3643$ for the prepaid share, the forward price $120e^{0.01875} \approx 122.27$.

Checks:
1. Number script: 325 of 325, exit 0 (session AF fix pass). Method 2: sympy differentiation for the drift tests and the dividend equation; the symmetric gambler's-ruin chain on the 1-pip grid $0, \ldots, 50$ from 30, solved as linear systems (exact for $P$, $E[\tau]$ and $E[\tau\,\mathbf 1_{\{X_\tau = 50\}}]$, each step lasting $1/\sigma^2$), and the closed forms $(50^2 - 30^2)/12$ and $(50^2 - 20^2)/12$; Monte Carlo of $S_1S_2$ under $Q$ (2,000,000 paths) and the split $E[S_1^2]e^{r}$; `brentq` for the forward price. Reader's script `problems-ito-4-numbers-read.py`: 299 of 299, 0 FINDING lines.
2. Validator: 0 errors; no warnings on this file (three `[wrong-band]` warnings on the new problem's slips were fixed by widening them to the asked rounding).
3. Voice scan 35 on the course folder: 0 and 0 (8,767 sentences).
4. `fresh-check --file` (and `--pairs`): 0 hits. Own greps of 75{,}000, 48{,}000, 4{,}000, 133.33, 175, "pips", "central bank", $30 + 2W_t$, 29.93, 28.19, 122.27, 2.3643, 118.21 and the stories: no match in the course or its exams (133.333 is an unrelated slip in l3; "central bank" appears only in other courses). The trade-exit story (take-profit and stop-loss) was rejected: l14 and review-4 use it.
5. `grade-all --file`: 13 widgets, 0 failures.
6. Playthrough `--problems ito/problems-4 --local-cdn <pkgs>`: green, desktop and `--mobile`. Part shots at 440 px read; no layout faults.

Closest material to each problem (screens numbered from 1):

| problem | lesson screen | quiz | review | homework | exam |
|---|---|---|---|---|---|
| p-band-wait | l14 S3, S7 ($P = b/(a + b)$, $E[\tau] = ab/\sigma^2$, start at 0): here both are given and the problem starts off-centre, uses $X_\tau^3 = 2{,}500X_\tau$ and the stopped cubic martingale, then conditions on the exit edge; l13 S1 ($W^3 - ctW$, $c = 3$): here $c = 12$ is one step inside part 2. | l14 q-ratio, q-sigma (chance, $ab/\sigma^2$): neither is asked. | r-exit-sigma ($ab/\sigma^2$): $E[\tau]$ is given, not asked. | h-stopping, h-exit-drift (derive $P$ and $E[\tau]$): no conditional time. | e-exit-drift (drifting exit, $P$ and $E[\tau]$), e-sixth-repair (martingale repair): no conditioning on the exit level. |
| p-two-date-product | l15 S5 ($\text{Var}(W_2 + W_3)$ by $\min(s, t)$) and l16 S4, S5 (power payoff $S_T^2$): here the covariance of two log prices feeds a lognormal mean of a product at two dates. | l15 q-const; l16 q-cube ($S_T^3$). | r-sqrt ($\sqrt{S_T}$): one date only. | h-moments ($E[W_2^4W_3^2]$): moments of $W$, not a price. | e-cubed-claim ($S_T^m$ at one date). |
| p-dividend-hedge | l17 S2 to S5 (the no-dividend derivation and where $\mu$ goes) and S8 (forward check): here a dividend term changes the coefficient to $r - q$, then a prepaid share and a forward price follow from it. | l17 q-vt ($V_t$ from given Greeks); l16 q-fwd2 ($100e^{0.1}$, no dividends). | r-mu (what the price depends on). | h-derivation, h-aloud-unknown-drift (the derivation aloud, no dividends). | e-theta-from-pde (theta from given Greeks). |

No problem walks through several items in a row, and none retells a lesson screen. No engine limit bent a part; no inbox bullets.
## Re-author and fix pass (session AF, `docs/briefs/reauthor-fix-af.md`)

Review `docs/reviews/review-problems-ito-1-3.md`. Re-authored: `p-digital-measures` as `p-twin-shares`, `p-one-touch` as `p-bridge-closes`. Findings 1 to 8 and 10 applied exactly as the reader wrote them, numbers recomputed first; finding 9 fell with `p-one-touch`.

- `p-twin-shares`: two shares on one $W$; hedge one with the other (£600), the noiseless book fixes $\mu_B = 12.5\%$, the drift rate of $R = S_B/S_A$ under $P$ (0.84%), then under $Q$ ($-2.16\%$) to price a note on $R$ (£64.99). The trap: a ratio of two prices that drift at $r$ is not a martingale.
- `p-bridge-closes`: a four-day up-and-out call simulated on daily closes; why the drift drops out between two known closes (the change-of-measure weight depends on end values only), the reflection touch chance between closes (0.4942), the path's survival chance (0.3837) and its corrected payoff (£3.60).
- Fresh-check `--files` on the three sets: 0 hits. New advisories, judged fine: `p-twin-shares` shares 45 and 0.25 with `p-quarter-rally` (a price and a time there, a price and a price of risk here) and 400 and 0.25 with l1 S3. By grep: 0.0084 sits in l11 as a tree error, £112.75 in l10 as a mean, 0.3632 (a `p-maker-tally` slip, $\Phi(-0.35)$) in l9 as a put delta and among path values; no story or chain is shared.
- Gates: validator 0 errors, no warning on the three sets (the two `[table-source]` warnings are gone); voice scan 35, 0 and 0; `grade-all --file` 0 failures on each; author script 988 of 988; reader script 320 checks, 0 FINDING lines (its digital and one-touch checks removed, the maker and touch-note checks retargeted); playthrough green with and without `--mobile` for all three sets, part shots at 440 px read.

Delta fix pass (session AG, `docs/reviews/review-delta-ag-ito.md`): bands widened on `p-bridge-closes` parts 2 and 3, `p-touch-note` part 3, `p-twin-shares` part 4; the reader lines applied to `p-bridge-closes` part 2 and `p-twin-shares` part 2. No key changed; all scripts exit 0.
