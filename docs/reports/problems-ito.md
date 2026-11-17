# Problem sets: ito levels 1 to 3 (brief `docs/briefs/wave-c-author-ag.md`, `docs/briefs/chained-prompts.md`, `docs/briefs/chained.md`)

Files: `app/content/courses/ito/problems-1.json` to `problems-3.json`. Level 4 has its own author. Numbers: `docs/reports/problems-ito-numbers.py` (956 of 956 checks, exit 0). Commits: `074c470a` (level 1, with the script), `d72d1fbf` (level 2), `223fd3ab` (level 3).

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
| problems-3 | p-digital-measures | 4 (4 / 0) | l10, l11 | 4 |
| problems-3 | p-one-touch | 4 (4 / 0) | l10, l11, l12 | 4 |

Every lesson of each level appears; every problem draws on two or more. Skills: level 1 `it-bm`, `it-calculus`; level 2 `it-calculus`, `it-martingale`; level 3 `it-pricing`, `it-martingale`, all from the level's lessons. Typed parts 12/12, 11/12, 11/12. The two choice parts are judgements (which integral a weighted sum of squared moves tends to; which root fits the note's boundary conditions). Each later part restates the value it uses. Every part that needs $\Phi$ names software or a normal table.

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
| p-digital-measures | l11 S8 (digital call at the money): here a digital put, priced under $Q$ and against a junior's $P$ price via the shift $\theta\sqrt T$. | l10 q-theta; l11 q-digital (chance given). | r-weight; r-digital (chance given). | h-girsanov-ratio: average weight on an event; here the $z$ shift and the £ cost of using $P$. | e-tree-price: a tree, not a lognormal digital. |
| p-one-touch | l12 S1 (driftless touch of 1), S3 (shift table): here a driftless log price under $Q$ found from $r = \tfrac12\sigma^2$, then a no-touch by parity, daily. | l12 q-touch, q-shift. | r-touch, r-shift (shifted level given). | h-touch-shift (shifted level and $\Phi$ given). | e-daily-touch: the shifted touch chance; here the $Q$ drift, parity to a no-touch and discounting. |

No problem walks through several items in a row, and none retells a lesson screen: each joins two or three lessons in a chain the course does not run.
