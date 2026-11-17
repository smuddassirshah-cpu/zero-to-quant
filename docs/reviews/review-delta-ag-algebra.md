# Delta read AG, algebra problem sets 1 to 3: the four re-authored problems and the fix-pass parts

Counts: `wrong` 0, `misleading` 3 (findings 2, 3, 4), `other` 2 (findings 1, 5), `reuse` 0, `re-author` 0, `continuity` 0, `voice` 0. No key, `wrong` value or printed number is mistaken. Two fixes change a key (findings 1 and 2); the fixer updates the author's and the reader's scripts for them.

Scope, commit range `c408e210..397320c3` on `app/content/courses/algebra/problems-1.json`, `-2`, `-3`, read at `0abcd8fe`:

- re-authored: `p-pixel-scrambler` (set 1), `p-server-moves` (set 2), `p-units-133` and `p-affine-five` (set 3);
- fix-pass parts on kept problems: `p-probe-stride` part 1 and the lines of findings 3 and 4 (part 2 `question`, `byKey.all`, part 3 `question`); `p-fixing-five` $\sigma$ in parts 3 and 4, part 1 `explain` and `options[3].why` (findings 6 and 7).

Brief: `docs/briefs/delta-read-af.md` with the session AG additions (exam items found by skill id; `problems-4.json` as a reuse source; proof-heavy checks; pass 8 rules by hand). No browser, no content or engine edit.

## Method

- Each part was solved from its text before its key was read, then again in `docs/reports/delta-review-delta-ag-algebra-numbers.py`, which imports no earlier script. Routes: matrix powers entry by entry and the inverse by a search of all $7^4$ matrices; permutations as dicts composed right to left, the sign by inversions; the 108 units modulo 133 listed and cubed one by one; the 20 affine maps as tables of values, composed and conjugated in full; $S_5$ listed for the two cosets.
- Claims read for their hypotheses, terms against the level's lessons: order and "$g^k = e$ exactly when the order divides $k$" (l4 s2), invertible matrices as a group (l2 s3), $\sigma^{-1}$ of a cycle (l8 s1), sign of a product (l9 s9), conjugate and normal (l11 s2, s3), a kernel is normal (l11 s7), first isomorphism theorem and "one coset per value" (l12 s2), the one-step test with non-empty (l5 s2).
- Reuse: l1 to l17, `review-1` to `-4`, `homework-1` to `-4`, `problems-4.json` and the 17 items of `exams/topic-3.4.json` that carry an `ag-` skill were searched for each problem's story, numbers, groups and steps (`taught.py` greps and reading of the hits). No other exam or bank file carries an `ag-` skill (the one other grep hit, `courses/complex/homework-1.json`, is the word "lag-polynomial").
- Each fix text was applied to a copy of `app` and `docs` in the scratch folder (`delta-review-delta-ag-algebra/copy`, `applyfix.py`) and run there; the worktree content was never edited.

## Tool results

| check | result |
|---|---|
| author's script `problems-algebra-numbers.py` | 541 of 541, exit 0 |
| reader's script `problems-algebra-numbers-read.py` | 266 checks, 0 FINDING lines, exit 0 |
| level 4 scripts (reuse source) | 177 of 177; 172 checks, 0 FINDING lines |
| `delta-review-delta-ag-algebra-numbers.py` | 219 checks, 0 failed, 5 FINDING lines, exit 0; on the fixed copy 221 checks, 0 failed, 5 `resolved` |
| validator | 0 errors, 4566 warnings, none on the three sets (no pass 8 warning); same on the fixed copy |
| voice scan 35, course folder | 0 and 0; same on the fixed copy |
| `fresh-check --file`, three sets | 0 hits each; 0 hits on the fixed sets 2 and 3 |
| `grade-all --file`, three sets | 12, 14 and 11 widgets, 0 failures; 0 failures on the fixed sets 2 and 3 |

Pass 8 rules by hand: every numeric part in scope is a whole number or a residue with `abs` 0 and states its form; no rounding, no percentage, no table value, no `wrong` band wider than its value, no `\'`. Each `feedback.correct` ends on its key.

## Verdict per item

| set | item | numbers | claims and terms | reuse | finding |
|---|---|---|---|---|---|
| 1 | `p-pixel-scrambler` | clean | clean, nothing after level 1 | clean, two likenesses below | none |
| 1 | `p-probe-stride` parts 1 to 3 | clean | clean | clean (finding 3 of the review applied as written) | none |
| 2 | `p-server-moves` | clean | part 3 wording | clean | 4 |
| 2 | `p-fixing-five` | clean | clean (findings 6 and 7 applied as written) | clean | none |
| 3 | `p-units-133` | clean | one example line | clean, one likeness below | 1, 5 |
| 3 | `p-affine-five` | clean | part 2 "So", part 3 printed target | clean | 2, 3 |

## Findings

`N. file | JSON path | class | problem | evidence | exact fix`

1. `algebra/problems-3.json` | `items[0].parts[1]` (`p-units-133` part 2), `.parts[2].question`, `.parts[2].feedback.correct` | other | the key equals the first number the part invites.
   Evidence. "Using $|\ker\rho| = 6$ from part 1, how many $x \in G$ have $x^3 \equiv 1 \pmod{19}$?" The first step is $108/6 = 18$, the number of cosets and the size of the image. The key is $3 \cdot 6 = 18$ as well. A learner who divides and stops, never looking for a cube root, is marked right. No other part in scope has this.
   Fix: ask for the units whose reduction has order 3. Key 12; the old route gets its own line.
   - `parts[1].question`: "Using $|\ker\rho| = 6$ from part 1, how many $x \in G$ have $\rho(x)$ of order 3 in $\mathbb{Z}_{19}^{\times}$? Give a whole number."
   - `parts[1].widget.answer`: 12. `wrong`: `roots-only` 2, `with-kernel` 18, `one-coset` 6, `seven-each` 14 (all `abs` 0).
   - `feedback.correct`: "$G$ splits into $108/6 = 18$ cosets of $\ker\rho$, one per value, so $\rho$ is onto. The residues of order 3 modulo 19 are 7 and 11, so the count is $2 \cdot 6 = 12$."
   - `feedback.generic`: "Not quite. Find the residues $y$ of order 3 modulo 19, then count the units $x$ that reduce to each."
   - `byKey.roots-only`: "2 counts the residues $y$ modulo 19. Each of them is the value of a whole coset of $\ker\rho$, which holds 6 units."
   - `byKey.with-kernel`: "18 is the number of cosets, and it is also the count with $\ker\rho$ included. Only the cosets over 7 and 11 qualify, since 1 has order 1."
   - `byKey.one-coset`: "7 is not the only residue of order 3 modulo 19. Also $11 \equiv 7^2$, and $11^3 \equiv 7^6 \equiv 1$."
   - `byKey.seven-each`: "Seven numbers below 133 reduce to each $y$. One of the seven is a multiple of 7, so it is not a unit."
   - `explain.text`: "The order of $\rho(x)$ depends only on $y = \rho(x)$. Since $7^3 = 343 = 18 \cdot 19 + 1$, the residues 7 and $7^2 \equiv 11$ have order 3, and no other does. By the first isomorphism theorem each value of $\rho$ is taken on one coset of 6 units, giving 12."
   - `parts[2].question`: "Reduce modulo 7 as well: $x \bmod 7$ is a homomorphism onto $\mathbb{Z}_7^{\times}$, and only $x = 1$ lies in both kernels. Part 2's 12 units and the 6 of $\ker\rho$ are the 18 with $x^3 \equiv 1 \pmod{19}$. How many $x \in G$ have $x^3 \equiv 1 \pmod{133}$? Give a whole number."
   - `parts[2].feedback.correct`: "Modulo 7, $x^3 \equiv 1$ for $x \equiv 1, 2, 4$. Each of those 3 cosets of $\ker\rho$ meets each residue modulo 7 once, so $3 \cdot 3 = 9$."
   Recomputed: 12 units reduce to 7 or 11; $2 \cdot 7 = 14$; $12 + 6 = 18$; part 3's key 9 and its slips 18 and 3 stand. A squares version ($x^2 \equiv 1$) was rejected: `homework-4` item 6 counts the roots of $x^2 - 1$ in $\mathbb{Z}_{15}$.

2. `algebra/problems-3.json` | `items[2].parts[2]` (`p-affine-five` part 3), `.parts[3].question` | misleading | the question prints its own key.
   Evidence. "Using $\operatorname{ord}(fT) = 4$ from part 2, $f^4$ lies in $T$. Work out $f^4$. What is the order of $f$ itself in $G$?" Key 4. Retyping the printed 4 passes without computing $f^4$; the only other candidate is 20. This is the brief's "working backwards from a printed target".
   Fix: grade the computation, the constant of $f^4$. Key 0.
   - `parts[2].question`: "Using $\operatorname{ord}(fT) = 4$ from part 2, $f^4$ lies in $T$, so $f^4(x) = x + c$. Work out $c$. Give a residue from 0 to 4."
   - `widget.answer`: 0. `wrong`: `added-four` 2, `kept` 3 (both `abs` 0).
   - `feedback.correct`: "$f^4(x) = 16x + 3(8 + 4 + 2 + 1) = 16x + 45 \equiv x$, so $c = 0$ and $f^4 = e$. No smaller power is $e$, since $f^k = e$ forces $(fT)^k = T$. So $\operatorname{ord}(f) = 4$."
   - `feedback.generic`: unchanged.
   - `byKey.added-four`: "2 is $4 \cdot 3 = 12$ reduced. Each step also doubles the constant so far, so the constants run 3, 9, 21, 45."
   - `byKey.kept`: "3 is the constant of $f$ itself. Each step doubles the constant so far and adds 3: 3, 9, 21, 45."
   - `explain.text`: "Iterating gives $f^k(x) = 2^kx + 3(2^k - 1)$. At $k = 4$ that is $16x + 45 \equiv x$, so $c = 0$. The order of $f$ is a multiple of $\operatorname{ord}(fT) = 4$ and $f^4 = e$, so it is 4."
   - `parts[3].question`: "Part 3 found $f^4 = e$, so $f$ has order 4, the same as its multiplier. The same holds for every $f$ with $a \ne 1$. How many elements of $G$ have order 4? Give a whole number."
   Recomputed: the constants of $f, f^2, f^3, f^4$ are 3, 9, 21, 45; $12 \bmod 5 = 2$. Part 4's key 10 and slips stand.

3. `algebra/problems-3.json` | `items[2].parts[1].question` (`p-affine-five` part 2) | misleading | "So $T$ is normal" rests on one conjugate.
   Evidence. Part 1 conjugates one translation by one map. Part 2 opens "So $T$ is normal". Normality needs every conjugate (`review-3` item 3: "Normality asks about conjugates by every $g$"). $T$ is normal because it is a kernel (l11 s7), as part 1's `explain` says.
   Fix, `question`: "Being a kernel, $T$ is normal, and by the first isomorphism theorem $G/T \cong \mathbb{Z}_5^{\times}$. Let $f(x) = 2x + 3$. What is the order of the coset $fT$ in $G/T$? Give a whole number."

4. `algebra/problems-2.json` | `items[0].parts[2].question` (`p-server-moves` part 3) | misleading | "the server it started from" has no answer on the story's own clock.
   Evidence. The jobs start on Monday; after Tuesday they sit at $\tau$. "The host repeats Tuesday's migration every night. After how few nights is every job back on the server it started from?" Counted from Monday, the state after $k$ more nights is $\xi^k\tau$, never the identity (script, $k$ to 24). The key 6 is the order of $\xi$ run alone.
   Fix, `question`: "Using $\xi = (1\,6\,7)(2\,3\,8)(4\,5)$ from part 2, suppose the host runs $\xi$ alone, night after night. After how few nights is every job back on the server it held before the first of them? Give a whole number."
   Key 6 and the slips 18, 8, 3 stand.

5. `algebra/problems-3.json` | `items[0].parts[2].feedback.byKey.mod-19-only` (`p-units-133` part 3) | other | the example is not one of the 18.
   Evidence. "18 is the count modulo 19 alone. Modulo 7 many of them fail: $3^3 = 27 \equiv 6$, for example." The unit 3 has $3^3 = 27 \equiv 8 \pmod{19}$, so it is not among the 18.
   Fix: "18 is the count modulo 19 alone. Modulo 7 most of them fail: 45 is one of the 18, and $45 \equiv 3$ has $3^3 = 27 \equiv 6$."
   Recomputed: $45 = 2 \cdot 19 + 7$, $45 = 6 \cdot 7 + 3$, $\gcd(45, 133) = 1$; 9 of the 18 fail.

## Reuse, per problem

- **`p-pixel-scrambler`: clean.** Closest lesson screen: l2 s3 ("every real $2 \times 2$ matrix under matrix multiplication ... we keep only the invertible matrices"), a group check, no order and no modulus. Closest quiz, review, homework: `review-1` item 4 ($7^{-1} \bmod 40$ by Euclid), `homework-1` item 5 (order of 2 in $\mathbb{Z}_{11}^{\times}$): other groups, other routes. Closest exam item: `e-units-mod-17`, whose `explain` has "$2^4 \equiv -1$ gives $\operatorname{ord}(2) = 8$"; part 2 here has "$\mathbf{M}^4 \equiv -\mathbf{I}$" and key 8. It is one line of deduction with the same 4 and 8, in another group, and the exam asks for the order of a residue from its powers; neither of the exam's two questions is walked. In $SL_2(\mathbb{Z}_7)$ a power equal to $-\mathbf{I}$ that is not already so over $\mathbb{Z}$ forces order 8, so the pair cannot be moved without a new modulus. Ruled a likeness.
  Collision with `problems-4` `p-cipher-29` (item 0): both take a $2 \times 2$ matrix modulo a prime acting on pairs and end by applying its inverse to a column and reading the second entry ("which pixel does one step ... send to $(3, 1)$? Give its second coordinate" against "A pair arrives as $\mathbf{c} = (23, 12)$. What is its second plaintext symbol?"). The routes to the inverse differ in kind: here $\mathbf{M}^{-1} = \mathbf{M}^7 = -\mathbf{M}^3$ from the order, a level 1 idea; there $(\det\mathbf{K})^{-1}\operatorname{adj}\mathbf{K}$ in the ring $M_2(\mathbb{Z}_{29})$, with a unit test first. Stories, moduli and matrices differ, and three levels lie between. Ruled clean: one shared last step, the standard task of undoing a linear map. The main session may rule otherwise; if so the part to move is the scrambler's part 4, not the cipher.
  Level 1 only: matrices come from `linear-maps` (a requirement of level 1) and l1, l2; the order step uses l4 s2 alone; no Lagrange, coset or subgroup is named (script).
- **`p-server-moves`: clean.** Closest screens: l8 s1 ("You followed the arrows backwards. That is $\sigma^{-1}$"), l9 s9 ("$\operatorname{sgn}(\sigma\tau) = \operatorname{sgn}\sigma\operatorname{sgn}\tau$"), l8 s8 (order as an lcm, the `product` slip). Closest review and homework: `review-2` items 5 and 6, `homework-2` item 5. Closest exam item: `e-product-table` ("In $S_5$ take $\sigma = (1\,3\,5)(2\,4)$ and $\tau = (1\,5)(2\,3\,4)$ ... Fill in $\sigma\tau(k)$", explain "Both factors are odd and the product is even, as signs multiply"). The problem solves $\xi\sigma = \tau$ for the unknown factor, finds the sign before the permutation and counts even powers: none of these is asked in the course. Part 3 is the standard order task on its own cycle type. No server or migration story with a permutation in `app/content` (`markov` l2 and `eigen` l3 use "migrate" for populations).
- **`p-units-133`: clean.** Closest screens: l12 s0 to s2 ($3x$ on $\mathbb{Z}_{12}$, "Each row is a coset $x + K$ ... and it goes to one value"), l10 s3 ($x \mapsto x \bmod n$). Closest review and homework: `review-3` item 5, `homework-3` item 8 rubric ($x \mapsto x \bmod 4$ on $\mathbb{Z}_{12}$, additive). Closest exam item: `e-squares-mod-11` (kernel and image of squaring on $\mathbb{Z}_{11}^{\times}$). Here the map is reduction between unit groups, the kernel is found by listing, and the count comes from two kernels that meet in 1: no item does that. Likeness: `homework-4` item 6 counts the roots of $x^2 - 1$ in $\mathbb{Z}_{15}$ by squaring every residue; part 3 counts cube roots of 1 modulo 133 by cosets. Same family, other exponent, modulus, method and level. 133 and $\mathbb{Z}_{19}^{\times}$ occur in no other file of the course or the exam.
- **`p-affine-five`: clean.** Closest screens: l11 s3 (conjugates in $D_4$ from a table), l11 s4 (order of $1 + \langle 4 \rangle$), l11 s7 (a conjugate of a kernel element stays in the kernel). Closest review and homework: `review-3` items 3 and 4, `homework-3` item 2. Closest exam items: `e-normal-in-s4`, `e-order-three-s6` (a count by order in $S_6$, by cycle type). The group of maps $ax + b$, its multiplier map and the lift of an order from the quotient occur nowhere in `app/content`. Part 2 is the standard coset-order task in a new quotient. No collision with `problems-4`.
- **`p-probe-stride` part 1: clean.** It now asks for the first return, the standard order task (`review-1` item 5, order of 18 in $\mathbb{Z}_{30}$), with its own modulus; l4 s0's question ("how many seats does a walk from 0 visit, counting 0") is gone. All five texts of finding 3 and both of finding 4 match the review word for word.
- **`p-fixing-five`: clean.** $\sigma = (1\,5\,3\,2)$ in both questions; not the inverse or a relabelling of `e-product-table`'s $(1\,3\,5)(2\,4)$ (other cycle type). Both texts of finding 7 match the review.

## Verified with no finding

- `p-pixel-scrambler`: $\mathbf{M}^2$, $\mathbf{M}^3$, $\mathbf{M}^4$ with every printed entry (41, 112, 56, 153; 11, 30, 15, 41); order 8 by walking the powers, and $\mathbf{M}^k \equiv \mathbf{I}$ exactly when $8 \mid k$ to $k = 60$; the inverse is unique and is $\begin{pmatrix}3&5\\6&1\end{pmatrix}$; the pixel sent to $(3, 1)$ is $(0, 5)$ alone; slips 1, 2; 4, 7; 4, 1; 6, 2 each rebuilt. The adjugate gives part 3 directly; that is a second right route, not a flaw.
- `p-server-moves`: $\xi = \tau\sigma^{-1} = (1\,6\,7)(2\,3\,8)(4\,5)$, the only solution; signs by inversions $-1, +1, -1$; slips 8 and 2; order 6, slips 18, 8, 3; even powers $k = 2, 4, 6$, and they are $\langle \xi^2 \rangle$. Part 1's options cannot be told apart by wording: two say "Odd".
- `p-units-133`: 108 units; reduction is multiplicative and onto $\mathbb{Z}_{19}^{\times}$; kernel $\{1, 20, 39, 58, 96, 115\}$; cube roots of 1 are 1, 7, 11 modulo 19 and 1, 2, 4 modulo 7; 18 and 9 by direct count; each coset of $\ker\rho$ meets each non-zero residue modulo 7 once.
- `p-affine-five`: 20 maps, closed, with the composition rule of the prose; $T$ is normal (all 100 conjugates); $hth^{-1} = x + 2$, $h^{-1}th = x + 3$; $G/T$ has 4 cosets of 5, one per multiplier; $f^4 = e$ with constant 45; the order of every map with $a \ne 1$ is the order of $a$; 10 maps of order 4, 5 of order 2.
- `p-probe-stride` parts 1 to 4 and `p-fixing-five` parts 2 to 5: keys and slips by walking the probe and by listing $S_5$; both cosets are the full sets the part states; $\{e, (1\,2), (2\,3)\}$ is not closed.
- Skills of every item are carried by a lesson of its level. Chains: each later part in scope restates the value it uses.

## Engine

1. A numeric key printed in the same part's question (finding 2: "Using $\operatorname{ord}(fT) = 4$ ... What is the order of $f$") could be a validator warning for problem sets: the key, at the asked form, appears as a stated value after "=" in that part's `question`. Raised in `docs/BACKLOG-INBOX.md` under `Raised later (review-delta-ag-algebra):`.
