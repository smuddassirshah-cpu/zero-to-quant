# Problem sets: odes, levels 1 to 3 (brief `docs/briefs/chained.md`)

Files: `app/content/courses/odes/problems-1.json`, `problems-2.json`, `problems-3.json`: 3 problems each, 13, 13 and 14 parts. Numbers: `docs/reports/problems-odes-numbers.py` (547 checks, 0 failures, exit 0). Commits: ef0ce7e (level 1), 661305a (level 2), 790f307 (level 3), then one commit with this report and the inbox bullets. Level 4 (`problems-4.json`) belongs to another agent and is not touched.

Read first: the math of every lesson l1 to l13, review-1 to 3, homework-1 to 3 and the three Fluency sets (l2, l3, l7), dumped and searched before each problem was written. The course's own settings are Newton cooling, continuous compounding, a loan, a savings account, logistic growth to 10,000, the Vasicek drift, a market maker's inventory (l6), a trading venue's market share (l4), predator and prey, competing species and a pendulum. The sets use a lending platform's membership, a moving policy target, a rising pension, a desk's hedge, a fund's cash buffer, a tracking gap, two bond yields, liquidity providers and arbitrage firms, and a trend signal.

## Sets

| set | item | parts (numeric / expression / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-lending-members | 5 (4 / 0 / 1) | l2, l4 | 4 |
| problems-1 | p-moving-target | 4 (2 / 2 / 0) | l3, l5 | 5 |
| problems-1 | p-rising-pension | 4 (1 / 3 / 0) | l1, l3 | 3 |
| problems-2 | p-hedge-overshoot | 5 (4 / 1 / 0) | l6, l7, l8, l9 | 5 |
| problems-2 | p-cash-buffer | 4 (3 / 1 / 0) | l6, l7, l8 | 4 |
| problems-2 | p-tracking-gap | 4 (4 / 0 / 0) | l6, l7, l9 | 3 |
| problems-3 | p-yield-gaps | 5 (4 / 0 / 1) | l10, l11, l12 | 4 |
| problems-3 | p-liquidity-arbitrage | 5 (2 / 2 / 1) | l11, l12, l13 | 5 |
| problems-3 | p-trend-signal | 4 (3 / 1 / 0) | l10, l11, l12 | 3 |

Typed parts: level 1 12 of 13, level 2 13 of 13, level 3 12 of 14. The three choice parts are judgements: which equilibrium is stable, and which kind of equilibrium (node, spiral, saddle, centre) the eigenvalues give. Skills: `de-first` (level 1), `de-second` (level 2), `de-systems` (level 3), each the level's own lesson skill.

Chains. Level 1: equilibria 2 and 6, $f'(6) = -4$ stable, $k = 4$, $A = \tfrac17$, $t = \tfrac{\ln 21}{4} = 0.761$; $\mu = e^{1.25t}$, $r = 2.52 + 0.6t + 2.48e^{-1.25t}$, half-life 0.5545, lowest at 1.314 years where $r = \theta = 3.79$; $B' = 0.04B + 2000e^{0.02t}$, $\mu = e^{-0.04t}$, $B = 100000(e^{0.04t} - e^{0.02t})$, $B(10) = £27{,}042$. Level 2: roots $-2 \pm 5i$, $x_p = 2$, $c_2 = -0.8$, first peak $\tfrac{\pi}{5} = 0.6283$, overshoot $e^{-2\pi/5} = 28.46\%$; roots $-2 \pm i$, $B = 1.25$, $c_2 = -3.75$, $x(\tfrac{\pi}{2}) = 1.088$; critical $b = 10$, root $-5$, $c_2 = 6$, $x(0.5) = 0.4104$. Level 3: $\Delta = 5$, eigenvalues $-1, -5$, stable node, $c_1 = -1$, $y/x \to 3$; equilibrium $(2, 4)$, $\mathbf{J} = \begin{pmatrix}-2&-2\\4&0\end{pmatrix}$, $\tau^2 - 4\Delta = -28$, stable spiral, turn $\tfrac{2\pi}{\sqrt7} = 2.375$; $\mathbf{A} = \begin{pmatrix}0&1\\5&-4\end{pmatrix}$, $\Delta = -5$, eigenvalues $1, -5$, $s'(0) = -5$. Every later part restates the value it uses, and where a slip carries, the next part's `wrong` list holds the carried value (for example `p-lending-members` part 5 holds the times from $A = 7$, $k = 1$, $A = 0.2$ and $A = \tfrac18$).

Judgement calls a reader may question:
- `p-moving-target` part 4 uses part 2's $r(t)$, not part 3's half-life; the explain links the two (the trough is 2.37 half-lives in). Integration by parts is a prerequisite (integrals L3), not a level 1 lesson.
- `p-lending-members` part 3 gives the partial fractions and asks only for $k$; level 1's logistic screen does the same split.
- `p-hedge-overshoot` part 4 states $x'(t) = 11.6e^{-2t}\sin 5t$ so the part tests the reading of the peak, not the product rule again.
- `p-liquidity-arbitrage` part 5 gives the eigenvalues $-1 \pm i\sqrt7$ and asks for the turn time; the `centre` slip ($2\pi/\sqrt\Delta$) is l13's centre formula misapplied.
- Matrix parts accept a typed `[[a, b], [c, d]]`; the playthrough deals every matrix `wrong[].tex` in that form and each reaches its key.

Form. Every non-whole numeric part names its form; the overshoot carries `unit: "%"` with key 0.28461 (the fraction); the fund value carries `unit: "£"`. Each negative key has a wrong entry at its absolute value (validator `negative-key`).

## Reuse (grep of `app/content/courses/odes/` per problem, and `app/content/` for each story)

- Changed while authoring: `p-lending-members` was first a trading venue's depth; l4 screens use a trading venue's market share with equilibria, so the setting moved to a lending platform. `p-cash-buffer` was first a market maker's inventory, which is l6's story. `p-hedge-overshoot` first had roots $-2 \pm 3i$, which l15 names as poles; it now has $-2 \pm 5i$. `p-liquidity-arbitrage` first had the equilibrium $(2, 3)$, which is l13's swapped-coordinates distractor for $(3, 2)$; it now has $(2, 4)$. `p-yield-gaps` first had $\begin{pmatrix}0&-3\\1&-4\end{pmatrix}$, the transpose of review-3's $\begin{pmatrix}0&1\\-3&-4\end{pmatrix}$; it now has $\begin{pmatrix}-7&2\\-6&1\end{pmatrix}$, and its start $(4, 2)$ avoids l10's $(5, 2)$.
- Remaining hits, judged fine: $e^{0.02t}$ in l14 (a Laplace transform of $5e^{0.02t}$; only the 2% rate is shared); review-3 has $\begin{pmatrix}0&1\\-4&-3\end{pmatrix}$ as a wrong form, not the same matrix as `p-trend-signal`'s $\begin{pmatrix}0&1\\5&-4\end{pmatrix}$; l10 has $(1, -5)$ as an image vector, `p-trend-signal` names $(1, -5)$ only as an eigenvector in its explain; eigenvalue pairs such as $-1, -5$ and roots such as $1, -5$ are the standard task with this item's own matrix. Fluency families (`y' = ky`, `B' = rB + d`, characteristic roots from integers) share task shapes, not instances.
- Stories in other courses: "pension" (series review-3, an annuity value), "hedging rule" (testing homework-2 and review-2, a paired test), "liquidity providers" (micro l8, a flash crash), "trend-following" (garch l12, a remark). Different tasks; no shared numbers. `tools/fresh-check.mjs` has no problem-set mode, so these greps stand in for it.

## Checks

1. `docs/reports/problems-odes-numbers.py` (run with the scratchpad venv): exit 0, 547 checks (198, 197, 152). Route 1 sympy (`dsolve`, `solve`, `eigenvals`, `jacobian`, `limit`, symbolic by-parts), route 2 `solve_ivp` on each equation, `numpy.roots` and `linalg`, `brentq`, finite differences, and the linearised flow over one period. Every key, accept form and wrong value is recomputed from its named slip; each wrong lies outside the key band, no two wrong bands overlap, each has a `byKey` line, and printed numbers in feedback and explains are checked.
2. Validator from `app/`: 0 errors, no warnings on the three files.
3. `node tools/playthrough.mjs --problems odes/problems-<n> --local-cdn <pkgs>`, with and without `--mobile`: green for all three sets. Screenshots (`--shots`, 440 px) looked at for each set: no layout faults.
4. `VOICE_BASE=app/content/courses/odes python3 docs/reviews/voice-scan.py 35`: 0 and 0.
5. `node tools/grade-all.mjs --file <set> --local-cdn <pkgs>`: 0 failures on each set (13, 13 and 14 widgets).

Engine limits: two bullets in `docs/BACKLOG-INBOX.md` under `Raised later (problems odes):`.
