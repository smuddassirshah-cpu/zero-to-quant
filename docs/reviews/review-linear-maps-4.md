# linear-maps level 4 (Operators): second-reader findings

Scope: `l15-eigenvalues-exist`, `l16-self-adjoint`, `l17-spectral-theorem`, `l18-generalised-eigenvectors`, `l19-jordan-form`, `review-4`, `homework-4` in `app/content/courses/linear-maps/`, against `## Level 4` of `docs/briefs/linear-maps.md` and `docs/reports/linear-maps-4.md`.

Method: every file flattened and read in full. Every number, wrong-option value and code test recomputed in a scratch script (NumPy, exact fractions, complex arithmetic): products, eigenvalues, kernel dimensions of every power, Jordan sizes, the AR(2) recursion, the hump, the equicorrelated eigenvalues, the weighted adjoints. All three code solutions and starters were run in CPython against their hidden tests, and the homework deflation tests with their seeds. Each `why` and `byKey` was re-derived from the slip it names.

Severity: wrong = false statement or wrong maths; misleading = true answer but a gap, a `why` that names no real slip, or grading that marks a valid proof wrong; voice; layout.

## Tool results

- `python3 docs/reports/linear-maps-L4-numbers.py`: 242 of 242 checks passed, exit 0. Its 12 "check by hand" lines were read; all are correct except `l15` `eighth` (finding 4).
- Stated numbers the script does not check (all recomputed here and correct unless a finding says otherwise): homework `items[3]` (the two $d$ sequences and blocks 3, 2 against 4, 1); review `items[7]` (inner product $0/\sqrt{12}$); `l18` `screens[10].canvas.params.series[1]` (only $0.9^{20}$ is checked; all 21 values match); `l16` `screens[1]` captions ($90°$, $45°$, asserted but not expected at the path); `l17` `screens[0].explain.canvas` (the 1.6 arrow, finding 15); `l19` `screens[0].hints[1]` (a count of entries, finding 2); `l15` `screens[11].prose` (the shrink per step, finding 3). The script checks `l15` `quiz[2].widget.options[1].why` for "(1, 1)", which is true, but the inference drawn from it is false (finding 1).
- `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, 2276 warnings; no warning names a level 4 file.
- `VOICE_BASE=app/content/courses/linear-maps python3 docs/reviews/voice-scan.py`: 9 sentences over 20 words and 0 explanations over three sentences in the folder; all 9 are in levels 1 to 3. Level 4: 0 and 0. No `!`, no em-dash, no American spellings ("center" is a table `align` keyword).
- Code: `annihilating_poly`, `spectral`, `gen_eigenspace_dims`, `jordan_block_sizes` and `spectral_by_deflation` solutions pass every test; each starter fails at least one, and the first failing test matches its `byKey.test-N` (keys are 1-based, `code.js` line 543).

## Findings

1. **wrong.** `l15-eigenvalues-exist.json` `quiz[2].widget.options[1].why`, `quiz[2].widget.options[2].why`, `quiz[2].feedback.byKey.first`.
   Problem: both counterexamples say $\mathbf{A} - \mathbf{I}$ is "injective on $\mathbf{v}$" because it sends $(1, 0)$ to $(1, 1) \ne \mathbf{0}$. Injectivity is a property of the map, and $\mathbf{A} - \mathbf{I}$ is not injective. So for this $\mathbf{A}$ both factors fail, which is what the distractor "Both must fail" claims; the counterexample supports the distractor.
   Evidence: $\mathbf{A} - \mathbf{I} = \begin{pmatrix}1&1\\1&1\end{pmatrix}$ has rank 1 and kills $(1, -1)$. A working counterexample: $\mathbf{v} = (1, 1)$ gives $\mathbf{A}^2\mathbf{v} - 8\mathbf{A}\mathbf{v} + 15\mathbf{v} = (9, 9) - (24, 24) + (15, 15) = \mathbf{0}$, so $p(z) = (z - 3)(z - 5)$; $\mathbf{A} - 5\mathbf{I}$ has rank 2 (injective), $(\mathbf{A} - 3\mathbf{I})(\mathbf{A} - 5\mathbf{I})(1, 1) = \mathbf{0}$.
   Fix:
   - `options[1].why`: "Only one need fail. For $\mathbf{A}$ and $\mathbf{v} = (1, 1)$, $(\mathbf{A} - 3\mathbf{I})(\mathbf{A} - 5\mathbf{I})\mathbf{v} = \mathbf{0}$, yet $\mathbf{A} - 5\mathbf{I}$ is injective."
   - `options[2].why`: "In $(\mathbf{A} - 3\mathbf{I})(\mathbf{A} - 5\mathbf{I})(1, 1) = \mathbf{0}$, the first factor applied is $\mathbf{A} - 5\mathbf{I}$. It is injective; $\mathbf{A} - 3\mathbf{I}$ fails."
   - `byKey.first`: "You assumed the first factor applied fails. In $(\mathbf{A} - 3\mathbf{I})(\mathbf{A} - 5\mathbf{I})(1, 1) = \mathbf{0}$, $\mathbf{A} - 5\mathbf{I}$ is injective."
   - Script line 164: expect `"5\\mathbf{I}"` in `options[1].why` instead of `"(1, 1)"`.

2. **wrong.** `l19-jordan-form.json` `screens[0].hints[1].text`.
   Problem: "$(\mathbf{M} - 2\mathbf{I})^2$ has one non-zero entry".
   Evidence: $(\mathbf{M} - 2\mathbf{I})^2 = \begin{pmatrix}0&0&1&-1\\0&0&0&0\\0&0&0&0\\0&0&0&0\end{pmatrix}$: two non-zero entries in one row, rank 1.
   Fix: "$(\mathbf{M} - 2\mathbf{I})^2$ has one non-zero row; $(\mathbf{K} - 2\mathbf{I})^2 = \mathbf{0}$."

3. **wrong.** `l15-eigenvalues-exist.json` `screens[11].prose`.
   Problem: "Each step turns the state by $\tfrac{\pi}{4}$ and shrinks it by $\sqrt{0.5}$." In standard coordinates $\mathbf{C}$ is not a scaled rotation; the state $(x_t, x_{t-1})$ grows at the first step. The turn and shrink hold for the eigen-coordinate only.
   Evidence: $\|(x_0, x_{-1})\| = 1$, $\|(x_1, x_0)\| = \|(1, 1)\| = 1.4142$, $\|(x_2, x_1)\| = 1.1180$. $\mathbf{C}^8 = 0.0625\,\mathbf{I}$ exactly, so the per-cycle statement and $x_8 = 0.0625$ stand.
   Fix: "Each step multiplies the state's eigen-coordinate by $0.5 + 0.5i$: a turn of $\tfrac{\pi}{4}$ and a shrink by $\sqrt{0.5} \approx 0.7071$."

4. **misleading.** `l15-eigenvalues-exist.json` `screens[11].widget.wrong[2]` (`eighth`, 0.125) and `feedback.byKey.eighth`.
   Problem: the why says "$x_6 = -0.125$ is two steps early", but a learner who reads $x_6$ enters $-0.125$, which falls in no `wrong` and gets the generic line. 0.125 itself matches no named slip (it is $1/8$, one over the period).
   Evidence: series value at $t = 6$ is $-0.125$; $|{-0.125} - 0.0625| > 0.0005$ and $|{-0.125} - 0.125| > 0.001$.
   Fix: set `wrong[2].value` to `-0.125` (tol 0.001) and keep the why; update script line 122 to `xs[6]`.

5. **misleading (grading).** `l17-spectral-theorem.json` `screens[7].widget`.
   Problem: s4 ($\dim U = n - 1$) and s5 ($U$ is invariant) are independent: neither uses the other. The order s1, s2, s3, s5, s4, s6, ... is a valid proof and is marked wrong.
   Evidence: s5 uses only $\mathbf{q}_1$ and symmetry; s4 uses only l14. Both are needed before s7, not before each other.
   Fix: add `"same": [["s4", "s5"]]` to the widget.

6. **misleading (grading).** `l18-generalised-eigenvectors.json` `screens[8]`.
   Problem: e2 (the free inclusion) can stand after e5, just before e6; that valid order is marked wrong, and `same` cannot express a line against a block. The prose does not say where the free inclusion goes; only the nudge hint does.
   Evidence: e3 to e5 never use e2; e6 needs both.
   Fix: `screens[8].prose`: append "Give the free inclusion first."

7. **misleading (hypothesis).** `l17-spectral-theorem.json` `screens[6].explain.text`, `screens[7].widget.lines[2]` (s3); `homework-4.json` `items[7].model` step 2.
   Problem: "not injective over $\mathbb{C}$, so its rank is below $n$. Rank-nullity over $\mathbb{R}$ then gives a real kernel vector" silently uses that a real matrix has the same rank over $\mathbb{R}$ and $\mathbb{C}$. That is the only reason the eigenvector can be taken real, and it is the point the brief asked this `choice` to grade.
   Evidence: rank by elimination uses only field operations on the entries, so a real matrix row-reduces identically over both fields.
   Fix:
   - `l17` `screens[6].explain.text`, replace the first sentence: "Its rank is below $n$ over $\mathbb{C}$, and elimination on a real matrix gives the same rank over $\mathbb{R}$."
   - `homework-4` `items[7].model` step 2, after "so its rank is below $n$.": "Elimination uses only real numbers, so the rank over $\mathbb{R}$ is the same."

8. **misleading (gap in the exit proof).** `homework-4.json` `items[7].model` (*Step*, item 6); `l17-spectral-theorem.json` `screens[7].prose` and `screens[7].widget.lines[6]` (s7).
   Problem: the model claims to induct "for any self-adjoint operator on a real inner product space", but steps 1 and 2 are written for a matrix $\mathbf{A}$ on $\mathbb{R}^n$ (complexify, rank). Step 6 then applies the hypothesis to the operator $T = \mathbf{A}|_U$, so the step for operators is never proved. The missing line is the orthonormal basis that turns $T$ into a symmetric matrix. l17 hides the same gap by assuming both forms at $n - 1$.
   Evidence: Axler 7.9 (matrix of $T^*$ in an orthonormal basis is the transpose) and l13 (an orthonormal basis of $U$ exists) close it in one line.
   Fix:
   - `homework-4` `items[7].model`, after "*Step.* Let $n > 1$ and assume the claim in dimension $n - 1$.": "Pick an orthonormal basis (l13). In it the operator has a symmetric matrix $\mathbf{A}$ (Axler 7.9), so it is enough to treat $\mathbf{A}$ on $\mathbb{R}^n$."
   - `l17` `screens[7].prose`: "Assume it for symmetric matrices of size $n - 1$. Each line carries its reason."
   - `l17` s7 text: "Applied to $\mathbf{A}|_U$ in an orthonormal basis of $U$, the hypothesis gives an orthonormal eigenbasis $\mathbf{q}_2, \dots, \mathbf{q}_n$ of $U$."

9. **misleading.** `l18-generalised-eigenvectors.json` `screens[4].feedback.byKey.grow` (wrong value 3 for $d_3$).
   Problem: "Kernels stop growing once two are equal" does not apply here: $d_1 = 1 \ne d_2 = 2$, and $d_2 = d_3$ is what the learner is computing. The second sentence leans on $\dim G = $ algebraic multiplicity, stated only in the summary. Neither names the slip.
   Evidence: $(\mathbf{A}_3 - 2\mathbf{I})^2 = (\mathbf{A}_3 - 2\mathbf{I})^3 = \begin{pmatrix}0&0&0\\0&0&1\\0&0&1\end{pmatrix}$, rank 1 both.
   Fix: "You assumed each power adds a dimension. $(\mathbf{A}_3 - 2\mathbf{I})^3$ still has rank 1, the same as its square."

10. **misleading.** `l17-spectral-theorem.json` `screens[2].widget.wrong[1]` (`minus`, $-1$) and `feedback.byKey.minus`.
    Problem: no natural slip gives $-1$ for $\langle (1, -1, 0), (1, 0, -1) \rangle$, and the why states the rule, not an action. The common slip is multiplying the non-zero entries in turn.
    Evidence: $1 \cdot 1 + (-1)(-1) = 2$ (non-zero entries paired in order); correct pairing $1 + 0 + 0 = 1$.
    Fix: `wrong[1]` id `pairs`, value 2; byKey `pairs`: "You paired the non-zero entries in turn, $1 \cdot 1 + (-1)(-1)$. Pair by position: $1 \cdot 1 + (-1) \cdot 0 + 0 \cdot (-1) = 1$."

11. **misleading (unproved general claim).** `l15-eigenvalues-exist.json` `screens[9].explain.text`.
    Problem: "The characteristic polynomial is a multiple of every such $p$" is Cayley-Hamilton plus minimality, proved nowhere in the course. "Never smaller" is ambiguous.
    Evidence: true (the $\mathbf{v}$-annihilator divides the minimal polynomial, which divides the characteristic one), but it breaks "derive rather than state".
    Fix: replace that sentence with "Its degree is never above $n$, since $n + 1$ vectors are dependent."

12. **misleading.** `l15-eigenvalues-exist.json` `screens[1].feedback.byKey.signs`.
    Problem: "You gave the coefficients of $z^2 - 4z + 3$" cites a polynomial the learner first meets on the next screen.
    Evidence: $z^2 - 4z + 3$ first appears in `screens[2].prose`.
    Fix: "You moved the terms across: $\mathbf{A}^2\mathbf{v} - 4\mathbf{A}\mathbf{v} + 3\mathbf{v} = \mathbf{0}$ has $-4$ and 3. The question asks for $a, b$ in $\mathbf{A}^2\mathbf{v} = a\mathbf{A}\mathbf{v} + b\mathbf{v}$."

13. **misleading (hypothesis).** `l18-generalised-eigenvectors.json` `screens[7].prose`.
    Problem: Axler 8.22 is stated with $T$ undefined (the screen has introduced only $N$) and without "finite-dimensional". The brief asked for one screen of reasoning; there is none.
    Fix: replace the 8.22 sentence with "Now let $T \in \mathcal{L}(V)$, with $V$ complex and finite-dimensional, and distinct eigenvalues $\lambda_1, \dots, \lambda_m$. Then $V = G(\lambda_1, T) \oplus \cdots \oplus G(\lambda_m, T)$ (Axler 8.22). Each $G(\lambda_j, T)$ is invariant, and on it $T$ has the single eigenvalue $\lambda_j$."

14. **misleading.** `l15-eigenvalues-exist.json` `quiz[3].question`.
    Problem: "Which hypothesis of the theorem does this space break?" has two answers: $\mathcal{P}(\mathbb{R})$ is infinite-dimensional and real. Only the "Only" in option `cx` rescues the key.
    Fix: "Which broken hypothesis is to blame for the missing eigenvalue?"

15. **layout.** `l17-spectral-theorem.json` `screens[0].explain.canvas.vectors.aq`.
    Problem: $\mathbf{A}\mathbf{q}$ is drawn at $(1.6, 1.6, 1.6)$, outside the $[-1.5, 1.5]$ box. It is at 0.4 of its length while $\mathbf{q}$ is at 0.8, so it looks like $2\mathbf{q}$, not $4\mathbf{q}$.
    Fix: `aq.v` `[1.2, 1.2, 1.2]`, and add `explain.canvas.caption`: "$\mathbf{q}$ at 0.8 of its length; $\mathbf{A}\mathbf{q} = 4\mathbf{q}$ at 0.3 of its length."

16. **layout.** `l17-spectral-theorem.json` `screens[1].canvas.params.params`.
    Problem: `a = 1, b = 2` disagree with the controls' `start` 0.5 and 0.3; $(1, 2, -3)$ lies outside the box. The controls drive the params on load (`player.js` line 244), so the learner never sees it, but the two sources disagree.
    Fix: `params.params` `{ "a": 0.5, "b": 0.3 }`.

## Checked with no finding

- Ladder ramp: difficulties climb 1 to 3 in every lesson. Each has one `trap` with a `byKey` that names the misconception: l15 real eigenvalue, l16 real means symmetric, l17 always orthogonal, l18 repeat means missing, l19 same polynomial and eigenvectors. Each has an edge case: $\mathcal{P}(\mathbb{R})$ and degree 1; weighted inner product; diagonal and $1 \times 1$; nilpotent; the identity.
- Every proof follows its brief widget plan (`order` with distractor, the `choice` steps, `place` recall, `tap-regions` spot-the-flaw). Every other `order` has one valid order only.
- Homework rubric sums to 10, with `required` on invariance; review covers the six named topics. Small report slip: it gives the review difficulty as "2 to 4", but the items run 2 to 3 (within the brief).
- No engine change needed.
