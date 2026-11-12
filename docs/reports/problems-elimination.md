# Problem sets: elimination (brief `docs/briefs/chained.md`)

Files: `app/content/courses/elimination/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-elimination-numbers.py` (exit 0, 1,201 checks, 0 failures). Commits: 98bdb4d (level 1), 7a604fb (level 2), 6849433 (level 3), then this report.

Read first: every screen and quiz of l1 to l12, review-1 to 3, homework-1 to 3 and both Fluency sets, for settings to avoid: the share, bond and call payoff replication of l1, the delta, gamma and vega desk of l2 to l4 and homework-1, the small-pivot rounding pair, the singular rows $(1, 2, 1)$, $(2, 4, 3)$, $(3, 6, 5)$ of l4, hedging exposures and stock betas (l5, l6, l8, review-2), the SMB factor (l7), shocks to returns and portfolio P&Ls (l9, l10), the riskless pair (l11), and bond, stock, fund, call, put and bet replication (l12, review-3, homework-3). One draft collided with l4: a roaster whose bags were l4's singular rows with a $k$; it was rebuilt on new rows before writing.

Answer kinds. Vectors and matrices are typed whole in one `expression` widget (AUTHORING section 3), as `(a, b, c)` or, for a matrix, row by row; every matrix part says "Type it row by row, as `[[a, b, c], [d, e, f], [g, h, i]]`." and lists that form in `accept`. A matrix that a part must use is shown as a display after the sentence, not inline (inline it broke the line on a phone; see the inbox).

## Sets

| set | item | parts (numeric / expression / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-florist-prices | 5 (4 / 1 / 0) | l1, l2 | 3 |
| problems-1 | p-three-lines | 4 (0 / 4 / 0) | l1, l2, l3 | 4 |
| problems-1 | p-courier-rounds | 5 (1 / 4 / 0) | l2, l3, l4 | 4 |
| problems-1 | p-roaster-beans | 5 (2 / 2 / 1) | l1, l2, l4 | 5 |
| problems-2 | p-burning-ethanol | 4 (2 / 2 / 0) | l4, l6, l8 | 3 |
| problems-2 | p-tilted-gantry | 4 (2 / 2 / 0) | l5, l6, l7 | 4 |
| problems-2 | p-futures-packages | 5 (2 / 3 / 0) | l5, l6, l7, l8 | 5 |
| problems-2 | p-coin-hopper | 4 (1 / 2 / 1) | l6, l8 | 4 |
| problems-3 | p-vinyl-cutter | 4 (3 / 1 / 0) | l9, l11 | 3 |
| problems-3 | p-deformed-part | 5 (5 / 0 / 0) | l9, l10 | 4 |
| problems-3 | p-draw-bet | 5 (4 / 1 / 0) | l10, l11, l12 | 5 |

Typed parts: level 1 18 of 19, level 2 16 of 17, level 3 14 of 14. The two choice parts are judgements: what three costs fix when elimination breaks down (`p-roaster-beans` 3), and how many whole, non-negative coin counts lie on a solution line (`p-coin-hopper` 4).

Chains. Level 1: half of row 1 off row 3, the lily, the tulip, the rose, then a new bouquet; $\mathbf{L}$ from the multipliers, $\mathbf{c}$, Monday's hours, then Tuesday's by adding the extra order's hours; the one swap $\mathbf{P}$, $\mathbf{L}$ of $\mathbf{PA}$, $\mathbf{c}$ from $\mathbf{Pb}$, the minutes per drop, a new round; row 3 with $k$, the $k$ at which no swap helps, what the costs then fix, the price of B after the swap at $k = 4$, the price list. Level 2: rank 3, nullspace dimension 1, the special solution, the balance $(1, 3, 2, 3)$; the dependent tilt $k = -4$, the relation $\mathbf{m}_3 = -2\mathbf{m}_1 + 2\mathbf{m}_2$, the reachable $c$, then a setting with motor 3 at one turn; rank 2, the special solution, the reachable $c$, a particular solution, then 2 butterflies; rank 2, the coin swap $(5, -8, 3)$, one way to pay £3.70, then how many ways. Level 3: area 50, the flat $k = 6$, the image line, the input sent to zero; $\det \mathbf{D} = 13$ by cofactors, the third pivot $\tfrac{13}{6}$ as a check, the volume 195, $\det \mathbf{D}' = -26$ by row rules, the volume 5070; $\det \mathbf{P} = -1000$, one redundant bet, the copy $(1, -1, 1)$, its price £3.30, £15 from 50 pairs. Each later part restates the value it uses, and its `wrong` list holds the value the commonest slip before it gives (`carried`, `triple`, `sign`, `no-sign`, `diagonal`, `scale-ignored`).

Judgement calls a reader may question:
- Branches joined later, as review 1.3 c accepted: `p-coin-hopper` part 3 (one way to pay) does not use part 2 (the swap); part 4 needs both. `p-futures-packages` part 3 uses part 1's rank, not part 2's special solution; part 5 joins them. `p-vinyl-cutter` part 4 uses part 3's factor $(x + 2y)$ and part 2's $k$.
- `p-roaster-beans` part 4 rests on part 3's conclusion (at $k = 2$ the costs cannot fix A and B, so the roaster moves to $k = 4$), not on a number.
- `p-three-lines` part 4 uses linearity, $\mathbf{A}(\mathbf{x} + \mathbf{y}) = \mathbf{A}\mathbf{x} + \mathbf{A}\mathbf{y}$, from the vectors course (a `requires` of level 1). A learner who solves Tuesday's whole order with the factors gets the same $(4, 4, 3)$.
- `p-burning-ethanol` uses atom counts given in the prose; no chemistry beyond counting is needed. Its rank part needs a row swap (l4).
- `p-draw-bet` part 2 asks "bets minus rank", so "how many are redundant" has one answer; the prices imply state prices 0.45, 0.33 and 0.25, which sum to 1.03, a bookmaker's margin (checked in the script, not stated to the learner).

Form. Every numeric part names its form ("Give a whole number", "Give the price in pounds", "Give an exact fraction, or a decimal to 3 places", cm² and cm³). Money carries `unit` "£", time "minutes". `p-deformed-part` part 2 has `accept` "13/6, or 2.167 to 3 places", key 2.1667, tol 0.001.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (1,201 checks in all) |
| validator | 0 errors; no warning on the file (total unchanged at 4,857) | same | same |
| playthrough `--local-cdn` | green (19 parts) | green (17 parts) | green (14 parts) |
| playthrough `--mobile` | green; 440 px shots read, no layout fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

The numbers script, beyond keys and `wrong` values (each rebuilt from its named slip, outside the key's band, no two bands overlapping): `arith` evaluates every chain $a = b = c$ of plain arithmetic in every learner-facing string (feedback, `byKey`, explain, option `why`, tuples included) and fails a false step; `vocab` fails any printed number that is neither a given of the item nor a value the script computed for it. A self-test plants one fault of each kind and expects both to fire. It caught one slip while writing: the `upside-down` row of `p-florist-prices` part 1 was $-11$, and is $-11.5$.

Extra check: `tools/grade-regression.mjs` on a scratch copy holding only these three files (`--content`): all 91 keys and `accept` forms grade correct, and all 87 `wrong` entries grade wrong and land on their own key through the real grader, the row with $k$ included.

## Fresh-check

At the gate: 0 hits on all three sets. One advisory on level 1: `p-florist-prices` shares the formula $2y + z = 7$ with l2 quiz 3 (a triangular system $x + y + z = 6$, $2y + z = 7$, $3z = 9$). Judged a coincidence: one two-term row in a different system, story and answer; kept. At `--min-run 8 --min-share 0`: 10, 0 and 15 hits, all form sentences ("type it row by row as", "give an exact fraction or a decimal to # places"), the letters of the matrix template, and "a home win, a draw or an away win" in counting-chance l11 (another course). One phrase hit led to a change: `p-draw-bet` part 5 first asked "What riskless profit do you lock in today?", as review-3 item 8 does; it now asks how much cash the trade brings in, with nothing owed after the match. The settings (a florist, a food plant's lines, a courier's rounds, a coffee roaster, burning ethanol, a printer gantry, futures packages, a parking machine's coins, a vinyl cutter, a modelling program, a betting exchange) are new to the course.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems elimination)". None blocked a problem.
