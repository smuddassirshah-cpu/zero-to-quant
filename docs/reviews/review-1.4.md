# Topic 1.4 second-reader findings

Format: location | severity | what is wrong | correction. Paths are relative to the repository root.

Counts (error / warning / note): vectors 2 / 8 / 9; elimination 3 / 2 / 8; least-squares 2 / 3 / 10; eigen 2 / 7 / 21; exam 0 / 3 / 0. Total 80.

Check scripts in this folder: check_vectors.py, check_elimination.py, check_ls.py, check_eigen.py, check_exam.py (numbers); style.py (sentence length, "!", spelling, "$"); structure.py (explain length, wrong values without byKey feedback); dump.py (readable dumps in dumps/).

## app/content/courses/vectors

### l2-lining-up.json
- screens[6] (generalise), numeric wrong `pair-sum` | error | Value 15 does not match its feedback "You added all six numbers": 1 + 2 + 3 + 4 + (−5) + 6 = 11. A learner who makes that slip gets the generic line. | Set `value: 11`.
- screens[4] (problem), hint `point` | warning | "Two of the five give a positive answer: p and s" names the two arrows to leave out, so the point rung hands over the answer by elimination. | "Work out 2x + y for p and q first; the sign decides."

### l3-lengths-angles.json
- summary.trap | note | Plain-text "|u + v|" and "|u| + |v|" with no KaTeX or bold vectors; 21 words. | "Lengths do not add: $|\mathbf{u} + \mathbf{v}| \le |\mathbf{u}| + |\mathbf{v}|$, equal only when the arrows point the same way."

### l4-portfolio-return.json
- screens[7] (generalise), explain | warning | "This is why weights must add to 1: a portfolio of identical assets returns what each asset returns." The logic is backwards: weights add to 1 because they are shares of your money; the identical-asset result follows from that. | "Because the weights add to 1, a portfolio of identical assets returns what each asset returns."

### l8-identity-transpose.json
- screens[5] (trap) | warning | The trap is spent before it starts. Screen 4's explain already says "Transposing the product reversed the order of the factors", and the hint step gives the answer. The learner is asked a question they were just told the answer to. | Move the reversal statement out of screen 4's explain (end it at "matches $(\mathbf{AB})^T$ entry for entry"), or put the trap before the ladder computation.
- screens[5] (trap), explain | warning | "Think of socks and shoes: to undo them, reverse the order." That is the analogy for inverses. Transposing undoes nothing, and screen 6 gives the real reason: the row and column trade places. | Drop the sentence, or say "The row of $\mathbf{A}$ and the column of $\mathbf{B}$ trade places, so the factors swap."

### l9-one-matrix-equation.json
- quiz q-untidy, option `sign` why | note | "You kept +3y on the right-hand side's sign" is garbled. | "You moved $3y$ across without changing its sign: $x - 3y = 1$."
- screens[7] (derive), hint `step` | note | Sentence of 21 words. | Split after "rows times $\mathbf{x}$".
- objectives (and course.json lessonObjectives for l8, l9) | note | Non-bold $A$ and $B$ for matrices ("$A\mathbf{x} = \mathbf{b}$", "$(AB)^T = B^T A^T$"), against the house rule of bold capitals. | Use `\mathbf{A}`, `\mathbf{B}`.

### l10-undoing.json
- screens[1] (explore), option `half` why | note | "From $\mathbf{R}\mathbf{u}$ it lands a quarter turn past the far side" is unclear. | "It sends $\mathbf{R}\mathbf{u}$ to $-\mathbf{R}\mathbf{u}$, a quarter turn clockwise of $\mathbf{u}$, not $\mathbf{u}$ itself."
- screens[4] (ladder), feedback r1c1 | note | "$-4$ shared by 2" reads oddly. | "$-4$ divided by 2".
- summary.ideas[0] | note | 23 words in one sentence. | Split at the colon.

### l11-no-inverse.json
- screens[10] (transfer), explain | warning | "A singular covariance matrix means two assets carry the same risk" is false in general. Correlation −1 also makes Σ singular, and with n assets the cause can be any linear combination. The general fact is that some portfolio has zero variance. | "A singular covariance matrix means some mix of the assets has zero variance: here, long one class and short the other."
- screens[10] (transfer), prose | note | Writes $\Sigma$ without bold; l8 and hw-2 use `\boldsymbol{\Sigma}`. | Use `\boldsymbol{\Sigma}` throughout.
- screens[8] (derive), explain | note | "The converse holds too" is asserted with no argument, against "derive rather than state". | Either add the one-line converse argument, or drop the claim.

### l12-numpy-matrices.json
- screens[7] (derive), explain | error | "The final `np.allclose` catches a wrong matrix or a near-singular one." The second half is false. `solve` is backward stable, so the residual is tiny even when A is nearly singular. Screen 5 of this lesson proves it: on the Hilbert matrix `solve` leaves residual 4.4e-16 while x is off by 2.4e-5 (cond ≈ 1.6e13). | "The final `np.allclose` catches a wrong matrix. A small residual does not prove x is accurate when A is nearly singular: check `np.linalg.cond(A)`."
- screens[9] (transfer), line l2 of screens[7], summary.ideas[2] | warning | The lesson teaches "test the determinant before trusting solve", with the threshold |det A| < 1e-12. A determinant threshold depends on scale. A 4-asset covariance matrix of daily returns (variances 1e-4) has det 1e-16 and would be refused although it is perfectly conditioned. Elimination l11 later teaches the opposite ("small is not singular"). The two courses contradict each other. | Use `np.linalg.matrix_rank(A) < n` or `np.linalg.cond(A) > 1e12` as the test, and keep det for the exactly singular toy cases.
- quiz q-allclose, explain | warning | "`np.allclose` accepts differences around $10^{-8}$ and below" is wrong. The default test is |a − b| ≤ 1e-8 + 1e-5·|b|, so for identity entries of 1 it accepts about 1e-5. | "accepts differences of about $10^{-5}$ relative to the values compared (atol 1e-8, rtol 1e-5)".

### homework-3.json
- h-min-var, prose and tests | warning | The same scale-dependent |det Σ| < 1e-12 test, now applied to covariance matrices, where it is wrong in practice (see l12). | Test `np.linalg.matrix_rank(S) < len(S)` or the condition number.

## app/content/courses/elimination

### l1-one-pivot-at-a-time.json
- screens[7] (generalise), explain | note | "Only the pivot row has zeros to the left of its pivot." Rows below it have them too once earlier columns are cleared. The point is that row 1 does not. | "Rows above the pivot row still have entries in the cleared columns; the pivot row does not, so subtracting it keeps those columns clear."

### l2-back-substitution.json
- screens[6] (ladder), numeric wrong `noDiv` (value 3.5, tol 0.6) | error | Counting products only gives 0 + 1 + 2 = 3, the same value as `perrow` (3). The `perrow` entry is matched first, so the `noDiv` line can only fire on 4, which encodes no misconception. | Delete `noDiv`, and widen `perrow`'s line: "3 counts one per row, or the products without the divisions: each row needs both."

### l4-zero-pivot.json
- screens[6] (generalise), explain and quiz q-why-pivot, explain | warning | "rounding errors are never magnified by a step" and "Rounding errors then stay the size they started" overclaim. Partial pivoting bounds the multipliers by 1, but entries can still grow (worst case by 2^(n−1)). It makes elimination stable in practice, not error-free. | "Every multiplier is at most 1 in size, so no single step can blow up the errors the way 10,000 did."
- screens[8] (transfer), prose | note | "In the Black–Scholes model, calls with the same expiry have vega a fixed multiple of gamma" holds only with one volatility for both strikes. Under a real smile the ratio differs slightly, so the system is nearly singular rather than exactly. | Add "priced at the same volatility".

### l9-area-scale.json
- whole lesson | warning | It re-teaches vectors l10 and l11 (det as area scale, sign as flip, det = 0 means no inverse, the no-zero-entries trap) as if new, and bolds "determinant" as a new term. Learners who did vectors meet the same hook twice. | Open with "You met $ad - bc$ in Vectors and Matrices" and spend the screens on what is new: the product rule, the sum trap and $k^n$.

### l11-squashed.json
- screens[8] (transfer), explain | error | The JSON has `$\\\\mathbf{w}` (a double backslash), so KaTeX draws a line break followed by italic "mathbfw". | `$\\mathbf{w} = (3000, -2000)$` in the JSON.
- screens[8] (transfer), explain | note | Sentence of 21 words ("An optimiser that inverts..."). | Split at the colon.

### l3-factorisation.json
- screens[4] (trap), canvas | note | The ids are swapped: id `A` is labelled U and id `U` is labelled A, so a highlight on `A-r1` lands on U. | Swap the ids to match the labels.

### l5-everything-reachable.json
- quiz q-sum-reachable, explain | note | Four sentences, over the three-sentence limit for an explanation. | Merge the last two: "It is closed under scaling too, which is why it is always a line, a plane or more through the origin."

### l6-inputs-to-zero.json, l8-real-directions.json, l10-computing-dets.json
- l6 summary.ideas[2] (21 words), l8 screens[10] prose (23 words), l10 summary.ideas[2] (22 words, three clauses joined by semicolons) | note | Over the 20-word limit. | Split each.

### homework-2.json
- hw-full-analysis, model | note | The model is numbered 1 to 7, but the prompt asks parts (1) to (6). Its 5 and 6 are the prompt's (5), and its 7 is (6). | Renumber the model to match the prompt.

### homework-3.json
- h-arb, numeric wrong `whole-copy` (value −97.6) | error | The feedback says "Two funds are copied by 1 bond and 1 stock". The slip it targets is selling one fund against the full copy: 101.20 − 199 = −97.80. Since the tolerance is 0.01, −97.8 never matches. | Set `value: -97.8`.
- h-long-covariance, model | note | Uses `\top` for transpose; the rest of the topic uses `^T`. | `\mathbf{w}^T`.

## app/content/courses/least-squares

### l1-perpendicular.json
- quiz q-factor-neutral | note | "dollar-neutral" in a course that works in £. | "cash-neutral" (or "money-neutral").
- screens[9] (transfer), explain | note | Four sentences, over the three-sentence limit. | Merge the last two: "A book neutral to several factors is orthogonal to each loading vector, so it lies in the orthogonal complement of their span."

### l2-four-subspaces.json, l3-orthonormal.json, homework-1.json, review-1.json
- matrices throughout | note | These files typeset matrices with `bmatrix`; every other file in the topic uses `pmatrix`. The learner sees square brackets in four files and round ones elsewhere. | Switch to `pmatrix`.

### l5-dropping-a-perpendicular.json
- whole lesson | warning | It re-teaches projection onto a line, p = (a·b / a·a) a, and beta as a projection. Vectors l3 and least-squares l4 already teach both, with the same "divided by |a| instead of |a|²" trap. A learner meets this hook a third time. | Cut the overlap: open from "you have projected onto a line; now project onto a plane", and spend the screens on the error being perpendicular to the whole column space.
- summary.ideas[0] | note | 22 words. | Split after "foot of the perpendicular".

### l6-projection-matrix.json
- screens[7] (generalise), explain | error | "$\mathbf{p} = (5, 2, -1) = 3(1, 1, 1) - 1(0, 1, 2)$" is false: that combination is (3, 2, 1). | "$\mathbf{p} = (5, 2, -1) = 5(1, 1, 1) - 3(0, 1, 2)$".
- screens[4], option `shrink` (5.81, 7.74) | warning | The why ("Projection never shortens a vector that is already on the line") names no slip that produces 5.81 and 7.74. A distractor with no traceable mistake teaches nothing. | Replace it with a value from a real slip, such as forgetting to divide by a·a, and say so in the why.

### l7-error-perpendicular.json
- quiz q-resid-sum, prose | note | 21 words. | "A regression on an intercept and the market leaves residuals 0.3, −0.1, r and 0.2 (in %)."

### l8-qr.json
- quiz q-r-shape, explain | note | "upper triangular with positive diagonal" contradicts screen 9, which says NumPy's R may have negative diagonal entries. | "upper triangular; Gram-Schmidt gives a positive diagonal, though NumPy may flip signs."

### l9-line-misses.json
- summary.trap | note | 22 words. | "Solving two equations and ignoring the third fits two points exactly. It misses the third badly: a sum of 9 against 1.5."

### l10-normal-equations.json
- objectives | note | Non-bold $A$ for a matrix. | `\mathbf{A}`.

### l11-fitting-a-line.json
- screens[0] (explore), hint `point` | warning | "Try a slope of 1 with an intercept near 2" is the answer (β = 1, α = 2), handed over at the second rung. | "Start with the slope: how much does y rise per step in x, on average?"

### l12-beta-by-hand.json
- screens[8] (transfer), prose | note | "α̂ = 0.13 and β̂ = 1.28, both in per cent a day." Beta is a ratio of returns and has no unit. | "α̂ = 0.13% a day and β̂ = 1.28."

### homework-2.json
- h-long-regression, model | note | Several sentences over 20 words, for example the one beginning "For example". | Split them.

### homework-3.json
- h-residual-facts, prose | error | `$\hat y = \hat\alpha + \hat\betax$`: `\betax` is an undefined control sequence, so KaTeX shows an error in place of the formula. | `$\hat y = \hat\alpha + \hat\beta x$`.

## app/content/courses/eigen

### course.json
- lessonObjectives for l2 and l9 | note | Non-bold matrices: "$\det(A - \lambda I) = 0$", "$A = U\Sigma V^T$". | `\mathbf{A}`, `\mathbf{I}`, `\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T`.

### l1 to l4, l9 to l12 (objectives)
- objectives[1] and [2] | note | The second objective (and the third in l9 to l12) has no full stop, unlike the first. l2 and l9 also use non-bold matrices. | Add full stops; bold the matrices.

### l4-where-it-settles.json
- screens[8] (transfer), prose | note | "the markov course" in lower case. | "the Markov chains course".
- summary.ideas[0] | note | "the largest eigenvalue" should be "the eigenvalue of largest size": a −0.9 beats a 0.5. | "keeps the part along the eigenvector whose eigenvalue is largest in size".
- screens[6] (generalise), explain | note | Four sentences. | Merge the last two: "For a Markov matrix the entries of x₂ add to 0, so c₁ is fixed by the total and the start cannot matter."
- quiz q-speed, wrong `keep`, `trace`, `six` | warning | Three wrong values are listed but none has `byKey` feedback, so a learner who types 0.7, 1.3 or 0.6 gets only the generic line. | Add, for example, keep: "0.7 is the chance of staying in state 1, not an eigenvalue"; trace: "1.3 is the sum of both eigenvalues; one is 1"; six: "0.6 is an entry; the shrink factor is λ₂ = 0.3".

### l6-bowls.json
- screens[3] (problem), explain | note | "the second pivot is $c - b^2/a$" uses a, b and c without defining them, and b was the slider on screen 1. | "For $\begin{pmatrix}a&b\\b&c\end{pmatrix}$, the second pivot is $c - b^2/a$."
- screens[6] (trap), prose | note | "Every entry of T is positive, so xᵀTx = x² + 4xy + y²": the "so" makes the form follow from positivity. | "Every entry of T is positive. Its form is xᵀTx = x² + 4xy + y²."
- screens[6] (trap), option `zero` why | note | "You subtracted 2 once, not 4" is garbled: the value 0 comes from a cross term of 2xy. | "You used 2xy, counting the off-diagonal 2 once. It counts twice: 4xy = −4, so the value is 1 − 4 + 1 = −2."
- quiz q-pivot, wrong `full` and `det` | warning | Two wrong values without `byKey` feedback. | full: "You subtracted all of row 1; the multiplier is 2/4 = 1/2." det: "8 is det A, the product of the pivots 4 and 2."

### l7-covariance-psd.json
- screens[1] (explore), prose | warning | "short £$100k$ of B" renders as "£100k", which every reader takes as £100,000. Here k is a slider from 0 to 2. | "short $k \times$ £100 of B".
- screens[6] (trap), prose | warning | The prose states "The implied correlation is 1.2". Every learner knows a correlation cannot exceed 1, so the trap is answered before it starts, and the PSD test is never needed. | Give the matrix without naming the correlation, for example "a colleague's spreadsheet reports this covariance matrix". Let the learner find the −0.4 variance.
- quiz q-fifty-fifty, explain | note | "the mix is quieter than A alone": at 0.75 it is quieter than B (variance 1) too, which is the stronger point. | "the mix is quieter than either asset alone".
- whole lesson against l11 and l12 | note | l7 divides by n; l11, l12 and the homeworks divide by n − 1. Screen 2 says the choice only rescales Σ, so this is consistent, but a learner moving to l11 sees a different formula. | In l11 screen 1, add "(l7 divided by n; NumPy and most libraries divide by n − 1)".
- summary.trap | note | 22 words. | "Symmetric with positive variances is not enough. A correlation of 1.2 gives (1, −1) the variance −0.4."

### l8-ellipses.json
- screens[8] (generalise), prose | note | "a **confidence region** of a bivariate normal": a confidence region is for a parameter. xᵀΣ⁻¹x = c is a probability contour (an equal-density ellipse) of a mean-zero normal. | "is a **probability contour** of a mean-zero bivariate normal: the region inside holds a fixed share of the outcomes."

### l9-rotate-stretch-rotate.json
- screens[7] (trap), prose | warning | The prose gives the eigenvalues of SᵀS (2.618 and 0.382) before the question. The misconception, that eigenvalues of S are its stretches, is defused before the learner can commit to it. What is left is taking a square root. | Drop the SᵀS sentence from the prose. Show the ellipse and ask for the longest stretch; put SᵀS in the hint step.
- screens[11] (transfer), prose and explain | warning | Wrong quant context. "She measures damage by the length of the P&L vector", and the "worst shock" gives P&L (2.83, 0): desk 1 makes £2.83k. That is a gain, not damage. A risk manager adds desk P&Ls; the Euclidean length is not a loss measure. | Ask for "the shock that moves the desks' P&L furthest, by length". Note that −v₁ gives (−2.83, 0), a £2.83k loss for desk 1. Or reframe it as the largest combined move.
- notation, whole lesson | note | Σ is the singular-value matrix here, but the covariance matrix in l7, l8 and l11. l11 renames to S, so the learner meets three conventions in four lessons. | Add one line on screen 3: "Σ here is the stretch matrix, not a covariance."

### l10-biggest-pieces.json
- screens[1] (explore), explain | error | "The third piece is twenty times smaller than the second." σ₂ = 9 and σ₃ = 0.9, a ratio of 10; the entries scale by the same 10. | "The third piece is ten times smaller than the second."
- screens[9] (transfer), and homework-3 h-factor | warning | Wrong quant reading. For the correlation matrix of five banks it reports that one factor "keeps 94.8% of the energy" (11.56/12.2). The quant figure is the variance share, 3.4/5 = 68%. That is exactly the `sigma` distractor, dismissed here as "dividing the σs". In l11 and review-3 the learner is taught that PC1's share is λ₁/Σλ, which for this matrix is 68%. The topic now gives two contradictory "shares" for the same matrix. | Add one sentence: "This is the share of the matrix's squared entries; as a share of variance, PCA in l11 gives 3.4/5 = 68%." Or move the energy example to a data matrix rather than a correlation matrix.
- screens[2] (problem), prose | note | "energy" is named but never linked to the standard term, so a learner cannot look it up. | Add "(the squared Frobenius norm)".
- screens[5] (trap), prose | note | 25 words. | "A colleague builds a rank-1 approximation of A another way. She keeps its first row and column and sets the rest to zero."

### l11-principal-components.json
- screens[4] (problem), feedback | note | Singular values are written σᵢ in a lesson where Σ is the covariance and σ usually means a volatility. "Variance is σᵢ²/(n − 1)" reads like a statement about standard deviations. | Write the singular values as sᵢ, to match the S in X = USVᵀ.

### l12-yield-curve.json
- screens[8] (transfer), explain | note | "its PC2 exposure is +£64": that uses the full-precision loadings (63.5). The table shows 2-decimal loadings, which give £63, and homework-3 h-long-hedge reports 63 for the same book. | "+£63" (from the table), to match the homework.

### review-2.json
- r-zero-eigenvalue, explain | note | 23 words in the last sentence. | "That ties the three ETFs together. One is a combination of the other two, as when one tracks the sum of two others."

### homework-2.json
- hw-risk-analysis, model part 5 | note | 21 words. | "It is the least risky direction, but not riskless. Zero variance would need an eigenvalue of 0."

### homework-3.json
- h-spread, explain | error | "The spread carries only the small component, which is why pairs trades are low-risk." On these numbers Var(A − B) = 4 equals Var(A) = 4. With correlation 0.5 the spread is no quieter than either stock, so the conclusion is false. | "The spread carries only the small component. It is quieter than either stock only when the correlation is above 0.5; here it is not."
- h-long-hedge, model part (d) | note | One sentence of 74 words, built from clauses joined by semicolons. | Make it a list of four risks, one sentence each.
- h-long-hedge, model part (c) | note | "Both are positive: short positions that gain when yields rise..." is 22 words. | Split after "positive".

## app/content/exams

### topic-1.4.json
- a-hedge-lstsq | warning | The exit criterion is "least squares … written in NumPy from the matrix operations". The only least-squares code item calls `np.linalg.lstsq`, so the exam never checks that the learner can build it from AᵀA or QR. | Add a test that bans `lstsq`, or a second item: solve the normal equations with `np.linalg.solve(X.T @ X, X.T @ y)`, or use `np.linalg.qr`.
- whole exam | warning | The other exit criterion, PCA written in NumPy, is not tested. a-pca-share only reads a share from `eigh` output. | Add a short code item: demean, covariance, `eigh`, sort descending and return the shares. It can reuse l12's yield data or fresh data.
- whole exam, against the 18.06 final | warning | It has 26 items and is light where 18.06 finals are heavy. It has one item each on the SVD, diagonalisation, elimination and QR. It has none on the projection matrix P = A(AᵀA)⁻¹Aᵀ, the four subspaces, or du/dt = Au. A 70% pass here is a weaker bar than the curriculum's "18.06 final at 70%". | Add items on P (idempotent, rank), on the four subspaces' dimensions, and a second SVD item (a rank-k error). Or state the exam is a gate, with an 18.06 past paper as the exit.
