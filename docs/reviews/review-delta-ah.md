# Delta read AH: two re-authored problems and four thinly checked keys

Counts: `wrong` 0, `misleading` 0, `weak` 2 (findings 1, 2), `voice` 0. No key, band, slip value or printed number is mistaken, and neither fix changes a key or a graded answer.

Scope, read at `96151ea6` (session head `claude/session-ah-engine-pass-1nzn58`):

- `topology/problems-2` `p-signal-bands`, all four parts (re-authored in `41e1087c`);
- `pdes/problems-3` `p-grid-budget`, all four parts (parts 1 and 2 re-authored in `96151ea6`);
- `algebra/problems-3` `p-units-133` part 2 and `p-affine-five` part 3; `pdes/problems-3` `p-log-contract` part 4; `measure-prob/problems-2` `p-settlement-fails` part 5.

No browser, no content or engine edit.

## Method

- Each part was solved from its question before its key, feedback or explanation was read, then again in `docs/reviews/review-delta-ah-scripts/check.py`. That script uses the standard library only and imports no other script: 301 checks, 0 failed, exit 0.
- Routes. Topology: the two tests of part 1 on interval pieces; a jump scan of $|h|$ and of $h$ at every quarter point; the image $|A|$ of each set, merged; the lemma "connected exactly when $|A|$ is" by brute force over all 31 non-empty subsets of a five-point model; the two counterexample paths on a grid. Grid: my own Crank-Nicolson solver (Thomas algorithm, zero left edge, far-field heat solution on the right), Fractions for $C$ and every slip. Algebra: all 108 units and all 20 affine maps by brute force. Log contract: the tail by `erfc` and by midpoint quadrature of the density. Settlement: Fractions for the series.
- Bands were rebuilt from each widget's `answer` and `tol` and fed the rounded key, the truncated key, the figure the printed working gives, and both neighbours at the asked places.

## Tool results

| check | result |
|---|---|
| `run-number-scripts --only topology` | 6 scripts, 6 passed, 0 new failures |
| `run-number-scripts --only pdes` | 4 scripts, 4 passed, 0 new failures |
| `run-number-scripts --only algebra` | 9 scripts, 9 passed, 0 new failures |
| `run-number-scripts --only measure-prob` | 8 scripts, 8 passed, 0 new failures |
| `grade-all --file` topology `problems-2` | 16 widgets, 0 failures |
| `grade-all --file` pdes `problems-3` | 12 widgets, 0 failures |
| `grade-all --file` algebra `problems-3` | 11 widgets, 0 failures |
| `grade-all --file` measure-prob `problems-2` | 19 widgets, 0 failures |
| `fresh-check --file`, the four files | 0 hits each; pdes `problems-3` has 7 advisories (see item 2 below) |
| voice scan 35, the four course folders | 0 and 0 each |
| `review-delta-ah-scripts/check.py` | 301 checks, 0 failed |

## Findings

Format: `N. severity | file | problem, part | text at fault | exact replacement`.

1. weak | `app/content/courses/pdes/problems-3.json` | `p-grid-budget`, part 3, `question` | "Part 2 predicts a shortfall of $557.28 \times 10^{-6}$ for the 400 run, before rounding."
   Part 2 tells the learner to use $C = 22.29$, and its own working prints $22.29 \times 0.000025$, which is $557.25 \times 10^{-6}$. The figure 557.28 comes from the unrounded $C = 22.2912$, which no part shows. "Before rounding" reads as "before rounding to 557", so a learner who kept two places sees a number that is not theirs.
   Replacement, that sentence only: "With $C = 22.2912$ kept unrounded, part 2's shortfall for the 400 run is $557.28 \times 10^{-6}$."
   No key, band or slip changes. Part 2's band (557.28, `abs` 0.5) already takes 557, 557.25 and 557.28.

2. weak | `app/content/courses/pdes/problems-3.json` | `p-log-contract`, part 4, `question` | "$\ln(S_T/S_0)$ is normal with mean $-0.0288$, minus part 3's log return, and variance $2\tau = 0.1176$."
   "Mean $-0.0288$, minus part 3's log return" can be read as a subtraction, giving a mean of $-0.0576$ and a chance of 0.4333, outside the band.
   Replacement, that sentence only: "So in that pricing walk, from $x = 0$, $\ln(S_T/S_0)$ is normal with mean $-0.0288$ and variance $2\tau = 0.1176$. The mean is part 3's log return with its sign changed."
   No key changes.

## Answers to the questions asked

### 1. `p-signal-bands` (topology, set 2)

- **Keys, all confirmed.** Part 1: 2 (only $(-2, 2)$ and $(-3, -1) \cup (1, 3)$ pass both tests; slips 4 and 3 are the open count and the symmetric count). Part 2: 3 (slip 1 is the usual count). Part 3: 4 (slip 1 is the usual count, slip 5 adds $[-4, -3] \cup [1, 2]$). Part 4: `size-four`.
- **"A set is in $\tau$ exactly when $U = \{x : |x| \in W\}$, $W$ open in $[0, \infty)$": true.** Given $U$, take $W = U \cap [0, \infty)$, open in the subspace. Given $W$, the set is the preimage of $W$ under the continuous $|x|$, and it is symmetric.
- **"Continuous into $\tau$ exactly when $|h|$ is": true, for any domain.** $h^{-1}(U) = |h|^{-1}(W)$, and $W$ runs over all open sets of $[0, \infty)$. Edge cases tested: $\lfloor t \rfloor$ at 0, where the size falls from 1 to 0; $s(t)$, whose size is constant; $t + s(t)$, whose size is $1 + |t|$ on both sides.
- **"Connected exactly when $|A|$ is an interval or a point": true for every non-empty $A$.** $\tau_A$ is the pullback of the subspace topology of $|A|$ under the onto map $x \mapsto |x|$. A split of $|A|$ pulls back to a split of $A$. A split of $A$ by $A \cap \{|x| \in W_1\}$ and $A \cap \{|x| \in W_2\}$ gives $W_1 \cap |A|$ and $W_2 \cap |A|$, which are disjoint: a shared size $r$ would put a point of $A$ in both pieces. Edge cases tested: a set whose two halves share a size ($\{-2, 2\}$), halves that meet at one size ($[-3, -2] \cup [1, 2]$, sizes $[1, 3]$), a set that straddles 0, a punctured set ($(-1, 0) \cup (0, 1)$, sizes $(0, 1)$), and the brute force on the finite model.
- **Part 4.** Each `why` is true: both counterexample paths have ends $-3$ and 5 and size $3 + 2t$; the first never reads 0, the second reads $-4$ at $t = \tfrac12$ and never 4.
- **Answerable from the level.** Topology axioms (l5), subspace topology (l6), continuity by preimages (l4), connectedness, intervals and the intermediate value theorem (l8) are all taught before the set. $\lfloor t \rfloor$ is used in `analysis` and in topology `review-1`. The characterisation each part needs is stated in its own question.
- **Walk.** It no longer walks l5 screens[0], l8 screens[0], [1], [10], `h2-five-families`, `q-connected-count` or `r2-preimage-sierpinski`: the space is not finite, and the deciding step (pull everything back through $|x|$) is in no lesson, review or homework item of the course. The course folder has no symmetric-set or $|x|$-pullback topology (grep). l8 "Which sets fall apart?" also counts connected subsets of $\mathbb{R}$, but in the usual topology, which is this part's planted slip. `fresh-check`: 0 hits.

### 2. `p-grid-budget` (pdes, set 3)

- **Printed runs.** My solver returns 12.9963192 on 200 intervals and 12.9975576 on 300, as printed.
- **Keys, all confirmed.** Gap $0.0012384$; $h_{200}^2 - h_{300}^2 = \tfrac{1}{18000}$; $C = 22.2912$ exactly. Part 2: $22.2912 \times 25 = 557.28$ (with 22.29: 557.25). Part 3: $557.28 \div 2.25 = 247.68$. Part 4: $2.25^2 = 5.0625$.
- **Slips, all confirmed.** 89.1648, 0.37152, 12.384; 139.3125, 990.6667 (both with $C = 22.29$; with 22.2912 they are 139.32 and 990.72, inside the slip bands); 110.08, 371.52; 2.25, 1.5.
- **Bands.** Part 1 takes 22.29 (rounded and truncated agree), refuses 22.28 and 22.30. Part 2 takes 557, 557.25 and 557.28, refuses 556 and 558. Part 3 takes 247.68, refuses 247.67 and 247.69. Part 4 takes 5.06 (rounded and truncated agree) and 5.0625, refuses 5.05 and 5.07. No slip, at its stored, exact, rounded or truncated value, falls in the key band of any of the four parts, and each slip band takes its own figure.
- **Printed keys.** No part prints its own key. Parts 2, 3 and 4 restate earlier keys only.
- **Explain sentences.** Against the closed form 12.99855638, to which the runs rise (2,400 intervals: 12.9985393): the 400 run's gap is $564.36 \times 10^{-6}$, 1.27% above 557.28 ("about 1% higher" holds); the 600 run sits $253.13 \times 10^{-6}$ below ("about 253" holds); the observed order from 400 to 600 is 1.9775 ("a little under 2" holds). $2.25 \div 5.0625 = 0.444$, so "under half" holds.
- **Walk.** The opening no longer walks `numerics/problems-3` `p-rate-path-euler`. That problem reads an order from three halved runs, then divides a gap by $2^p - 1$, then extrapolates. This one assumes order 2, fits a constant from two runs whose ratio is not 2, and predicts a grid it has not run. No sentence, slip id or slip line is shared. pdes `homework-3` and l12 use Richardson as $V_h + (V_h - V_{2h})/3$ on halved grids; fitting $C$ from 200 and 300 is not that step.
- **Shared numbers 120 and 300: coincidence, no finding.** `h-far-boundary` has a strike of £120 and a grid that stops at $S = 300$; here 300 is a count of intervals, the rate, expiry and volatility differ, and the task (a boundary value) is unrelated. The strike £120 was in this problem before the re-author. `c-sql-having` is a SQL table whose quantities include 120, 300 and 400 and a price of 1.25; `fresh-check` lists it as an advisory on four shared numbers, and nothing else links the two.

### 3. Thinly checked keys

| item | key | confirmed by | band and slips | explanation |
|---|---|---|---|---|
| `algebra/problems-3` `p-units-133` part 2 | 12 | brute force over the 108 units: 12 have $x \bmod 19$ of order 3; the residues are 7 and 11 | exact; slips 2, 18, 6, 14 are the values their lines name (18 units have $x^3 \equiv 1 \pmod{19}$; 7 numbers below 133 reduce to each residue, one a multiple of 7) | true; $7^3 = 343 = 18 \cdot 19 + 1$, $7^2 \equiv 11$ |
| `algebra/problems-3` `p-affine-five` part 3 | 0 | composing $2x + 3$ four times modulo 5 gives the identity, and no earlier power does | exact; slips 2 ($12 \bmod 5$) and 3 | true; constants 3, 9, 21, 45; part 4's 10 and "order equals the multiplier's order for $a \ne 1$" also hold over all 20 maps |
| `pdes/problems-3` `p-log-contract` part 4 | 0.466535 | mean $(k - 1)\tau = -0.0288$ exactly, variance 0.1176, $z = 0.083983$, tail 0.4665352 by `erfc` and by quadrature; equals $\Phi(d_2)$ | takes 0.4665 (rounded, truncated and the printed $1 - 0.5335$); refuses 0.4664, 0.4666, 0.5335, 0.5 | true; $\sqrt{0.1176} = 0.34293$, $0.0288 \div 0.34293 = 0.0840$, $\Phi(0.0840) = 0.5335$; wording, finding 2 |
| `measure-prob/problems-2` `p-settlement-fails` part 5 | `inf` | terms $0.64(k + 1)\,1.2^k$ by Fractions: they grow, so the sum is infinite | choice; distractors 16 and $6^{0.5} \approx 2.45$ are as stated, and "the slip of part 1" is that part's `jensen` slip | true; the closed form $\tfrac{16}{(5 - s)^2}$ needs $0.2s < 1$ |

## For the fixer

Both findings are one-sentence replacements in question text, in one file. After applying: validator, voice scan 35 on `pdes`, `grade-all --file` on `pdes/problems-3`, and the pdes number scripts (the author's script may match on the old sentences). Nothing here needs a ruling.
