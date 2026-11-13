# Problem sets: linear-maps, levels 1 to 4 (brief `docs/briefs/chained.md`)

Files: `app/content/courses/linear-maps/problems-1.json`, `problems-2.json`, `problems-3.json` (3 problems each, 40 minutes each). Numbers: `docs/reports/problems-linear-maps-numbers.py` (exit 0, 202 checks, 0 failures; it also reads every stored key back from the JSON, 37 of 37 typed parts).

## Sets

| set | item | parts (numeric / expression / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-hedge-baskets | 5 (2 / 2 / 1) | l2, l4 (subspace test, dimension, coordinates, dim of a sum) | 5 |
| problems-1 | p-hedge-curves | 5 (2 / 2 / 1) | l3, l4 (dependence lemma, span, extending to a basis, coordinates) | 4 |
| problems-1 | p-scenario-space | 5 (0 / 4 / 1) | l1, l2, l3, l4 (odd operations, zero, inverse, subspace, coordinates) | 4 |
| problems-2 | p-curve-report | 5 (1 / 4 / 0) | l5, l6, l7, l8 | 5 |
| problems-2 | p-futures-exposure | 4 (0 / 4 / 0) | l8, l9 | 4 |
| problems-2 | p-slope-adjusted | 4 (1 / 2 / 1) | l5, l6, l7, l9 | 3 |
| problems-3 | p-currency-duals | 5 (0 / 5 / 0) | l10, l11 | 4 |
| problems-3 | p-index-beta | 4 (3 / 1 / 0) | l11, l12, l13 | 4 |
| problems-3 | p-two-signal-fit | 4 (1 / 3 / 0) | l13, l14 | 5 |

Typed parts: level 1 12 of 15, level 2 12 of 13, level 3 13 of 13. The four choice parts are judgements: which extra rule keeps a subspace, which polynomial fails to extend a list to a basis, which scenario set is a subspace under the new operations, which argument proves a null space is zero.

Chains. L1: rule $w_1 = 2w_4$, $\dim U = 2$, coordinates $(2, 5)$, the basket $(4, -3, -3, 2)$ in $U \cap W$, $\dim(U + W) = 3$; $p_1 = p_2 + 3p_3$, span of dimension 2, $k = -1$, $2 + x$ fails, coordinates $(-1, 5, -3)$; $\mathbf{u} \oplus \mathbf{v} = (6, 50)$, zero $(3, 40)$, inverse $(2, 50)$, subspace $s = 40$, coordinates $(1, 2)$. L2: $T(t^3) = (8, 12)$, the $2 \times 4$ matrix, nullity 2, $p_0 = 3t - 1$, then $2t^2 - 5t + 7$; $[T\mathbf{b}_2]_{\mathcal{B}} = (4, 2)$, $[T]_{\mathcal{B}}$, its inverse, $T^{-1}(11, 13) = (3, 4)$; $T(3x^2 + x)$, null space zero, rank 3, $p = x^2 + 2x + 5$. L3: $\varphi_1 = x - 4y$, $\varphi_2 = 5y - x$, $T'\psi = 11x + 12y$, dual coordinates $(67, 56)$, representer $(\tfrac{11}{2}, 12)$; covariance 2, correlation 0.784, residual $(1, 2, -2, 0, -1)$, share 0.615; $\mathbf{f}_2$, $P_U\mathbf{v} = (3, 1, 2, 5)$, loadings $(-1, 2)$, distance 3.873. Each later part restates the value it uses.

Judgement calls a reader may question:
- `p-scenario-space` gives the operations ($\mathbb{R}^2$ with origin moved to a base case). l1 uses the positive reals with $xy$ and $x^{\lambda}$; this is a different space and setting, chosen so the same axioms work without reusing it.
- `p-curve-report` part 3 states that the first two columns are independent, so the part tests rank-nullity, not the rank.
- `p-futures-exposure` part 3 gives the determinant 6 to say why $T$ is invertible; the $2 \times 2$ inverse formula is from `vectors`.
- `p-currency-duals` part 5 (a representing vector under a weighted inner product) is computed from the l11 definition; the Riesz theorem is not named.
- Matrix answers are typed as `[[a, b], [c, d]]`, which each question names; grade-all grades the plain form as an accept entry.

## Checks

1. Numbers script: exit 0 (202 checks). Each key twice (sympy exact, then numpy solve, lstsq, QR, polyfit, a grid search for the least distance, or direct substitution); every `wrong` value shown to differ from its key, and the slip values recomputed.
2. Validator: 0 errors, no warnings on these files (three `[O2-explain-answer]`, one `[key-length]` and one `[wrong-band]` were fixed).
3. Playthrough `--problems linear-maps/problems-<n> --local-cdn <pkgs>`: all three green on desktop and with `--mobile`, rerun after the last edit to sets 2 and 3. Shots at 440 px read: no overflow; the inline matrix in `p-futures-exposure` prose sets cleanly.
4. Voice scan 35 on the course folder: 0 explanations over three sentences, 0 sentences over 35 words.
5. `grade-all.mjs --local-cdn` on the three files: 41 widgets, 0 failures.

## Freshness

`fresh-check --file` on each set: 0 hits. `--cross-numbers` advisories, judged: `p-index-beta` against `exams/mock-superday-research` (26, 6.5, 2.5: a boosting MSE item, a coincidence); `p-currency-duals` against l10 and `topic-1.10` for $\varphi_j(\mathbf{v}_k) = 1$ (the definition of a dual basis, stock).

Own-course reuse (the lesson of today's reads). For each problem I grepped its matrices, key vectors, polynomials, distinctive numbers and setting nouns first in `courses/linear-maps/`, then all of `app/content/`, and compared every matrix with every matrix in the content (pmatrix text and canvas `rows`: 264 in the course, 3,085 in all) for equality, a scalar multiple or the transpose. The first draft failed this, and I changed it:
- `p-currency-duals` had l8's quiz and homework-3's map $T(x, y) = (x + 2y, 3y)$ and review-3's basis $(2, 1), (1, 1)$; a second try used $(4, 1), (3, 1)$ and $\begin{pmatrix}1&-1\\2&1\end{pmatrix}$, which are `vectors/review-3` and `vectors/homework-2` matrices. Now $(5, 1), (4, 1)$ and $T(x, y) = (2x - y, x + 3y)$: no matrix match anywhere.
- `p-futures-exposure` had $\mathbf{A} = \begin{pmatrix}5&-2\\1&2\end{pmatrix}$ (equal to `eigen/homework-1`) and basis matrix $\begin{pmatrix}1&1\\1&2\end{pmatrix}$ (four eigen, algebra and elimination lessons). Now $\mathbf{A} = \begin{pmatrix}1&2\\-1&4\end{pmatrix}$, $\mathbf{P} = \begin{pmatrix}1&2\\1&3\end{pmatrix}$: no match.
- `p-two-signal-fit` ended on $\sqrt{12} \approx 3.464$ with the slip $\sqrt{24} \approx 4.899$, the distance and slip of a homework-3 item. Now $\mathbf{v} = (4, 2, 5, 3)$, distance $\sqrt{15} \approx 3.873$, slip $\sqrt{27}$.
- `p-slope-adjusted` part 1 asked $T(x^2) = x^2 - 2x$, the $q_1$ of homework-1 item 9; it now asks $T(3x^2 + x)$.

Result per problem after the changes (course folder / rest of content):
- `p-hedge-baskets`: no matrix, vector or rule shared; "cash-neutral" in `least-squares/l1` (a word only).
- `p-hedge-curves`: no polynomial, vector or matrix shared in the course; $x - 2x^2$ and $1 + x^2$ occur in calculus courses as unrelated functions.
- `p-scenario-space`: no vector or matrix shared in the course; $(3, 40)$ and $(2, 50)$ occur once each elsewhere in unrelated items; "base case" is a common phrase (l17).
- `p-curve-report`: map, matrix, polynomials not found anywhere; $(8, 12)$ appears in l5 as an intermediate $4(2, 3)$, a coincidence.
- `p-futures-exposure`: no matrix match; single vectors $(2, 3)$, $(4, 2)$ occur in lessons in other roles.
- `p-slope-adjusted`: $p - p'$, $3x^2 - 5x - 1$ not found; $x^2 + 2x + 5$ once in `complex/l1` (a quadratic with no real roots), a coincidence. Its matrix (not shown) has no match.
- `p-currency-duals`: basis, map, functionals and answers not found; the weight matrix $\operatorname{diag}(2, 1)$ is generic and appears in several courses, but the item writes it as $2u_1w_1 + u_2w_2$, which is found nowhere.
- `p-index-beta`: both return vectors, the residual and $\sqrt{6.5}$ not found; 0.784 and 0.615 occur in unrelated items.
- `p-two-signal-fit`: signals, returns, projection, residual and 3.873 not found; $\sqrt{15}$ and $\sqrt{27}$ occur elsewhere as unrelated surds.

## Backlog

Two bullets appended to `docs/BACKLOG-INBOX.md` under "Raised later (problems linear-maps):".

## Level 4 (`problems-4.json`, Operators)

File: `app/content/courses/linear-maps/problems-4.json` (3 problems, 15 parts, 40 minutes). Numbers: the level-4 block of `docs/reports/problems-linear-maps-numbers.py` (whole script exit 0, 0 failures; 90 `L4` lines, keys of all 15 parts read back from the JSON).

| set | item | parts (numeric / expression / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-footbridge-modes | 5 (2 / 3 / 0) | l15 (Axler 5.19 method over $\mathbb{C}$), l16 (real eigenvalues, perpendicular eigenvectors with the conjugate), l17 (decomposition $\sum \lambda\mathbf{q}\mathbf{q}^*$) | 5 |
| problems-4 | p-spring-linkage | 5 (2 / 3 / 0) | l16 (perpendicular eigenvectors), l17 (orthonormal eigenbasis, solving by the spectral sum) | 4 |
| problems-4 | p-curvature-operator | 5 (1 / 4 / 0) | l18 (kernels of powers, too few eigenvectors), l19 (block sizes from $d_k$, multiplicities, powers of $J_2$) | 4 |

Typed parts 15 of 15; no choice part. Every numeric part states its form ("a whole number", "two whole numbers, separated by a comma", "an exact fraction or a decimal to 3 places").

Chains. $\mathbf{S} = \begin{pmatrix}6&2+i\\2-i&2\end{pmatrix}$, $\mathbf{v} = (1, 0)$: $(a, b) = (8, -7)$, roots 1 and 7, $\mathbf{w} = (\mathbf{S} - \mathbf{I})\mathbf{v} = (5, 2 - i)$, $\mathbf{u} = (-2 - i, 5)$ from $\langle \mathbf{u}, \mathbf{w} \rangle = 0$, share $\tfrac{35}{36} \approx 0.972$ of $S_{11}$. $\mathbf{K} = \begin{pmatrix}4&-2&2\\-2&5&0\\2&0&3\end{pmatrix}$: $\lambda = 4$ on $(1, 2, 2)$, $(2, 1, -2)$ for 1, $(2, -2, 1)$ by perpendicularity, its eigenvalue 7, $\mathbf{x} = \mathbf{K}^{-1}(28, 0, 0) = (15, 6, -10)$ by the spectral sum. $Tp = p + p''$ on $\mathcal{P}_3$: $T(x^3) \mapsto (0, 6, 0, 1)$, $d = (2, 4)$, blocks 2, 2, multiplicities $(4, 2)$, $T^t(x^3) = x^3 + 6tx$. Each later part restates the value it uses.

Slips with lines (each `wrong` value checked in the script): $(2 + i)(2 - i)$ taken as 3, sign of $b$, roots with signs flipped, the other factor $(\mathbf{S} - 7\mathbf{I})\mathbf{v}$, the inner product without the conjugate ($(-2 + i, 5)$, not an eigenvector), $\tfrac56$ without the eigenvalue, $\tfrac78$ (share of the trace), $\tfrac{35}{6}$ (power, not share); entry or trace read as $\lambda$, a vector in the plane that is not an eigenvector, cross-product sign and scale, $\mathbf{K}\mathbf{F}$ instead of $\mathbf{K}^{-1}\mathbf{F}$, unit vectors left unnormalised; $p'$ for $p''$, one derivative factor, $d = (1, 2)$ (one chain), $(4, 4)$, blocks 3, 1 (whose $d_2$ is 3), multiplicities swapped, $T(x^3)$ for every $t$.

Judgement calls a reader may question:
- `p-footbridge-modes` part 5 uses $\mathbf{S} = 7\mathbf{q}_1\mathbf{q}_1^* + \mathbf{q}_2\mathbf{q}_2^*$ for a Hermitian matrix. l17 proves the real theorem; the question states the decomposition, and it follows here from l16 (two perpendicular unit eigenvectors are a basis of $\mathbb{C}^2$).
- `p-spring-linkage` part 5 gives the formula $\mathbf{x} = \sum \langle \mathbf{F}, \mathbf{q}_i \rangle\mathbf{q}_i/\lambda_i$; a learner may solve $\mathbf{K}\mathbf{x} = \mathbf{F}$ by elimination instead, which is a valid second route, not working back from a printed target.
- `p-spring-linkage` part 3 can be done by a cross product (from `vectors`) or by two equations; both are in the feedback.
- `p-curvature-operator` part 3 is a numeric set with a repeated value, `[2, 2]`, typed "2, 2" as AUTHORING section 3 allows.

## Level 4 checks

1. Numbers script: exit 0. Route 1 exact (sympy: `solve`, `nullspace`, `rank`, `jordan_form`, `LUsolve`, complex conjugates), route 2 another method (numpy `lstsq`, `eigvalsh`, `eigh`, `solve`, `matrix_rank` of powers, repeated application of $T$ for $t = 1$ to 6, the matrix power). Every `wrong` value rebuilt from its slip and shown to differ from the key; the 3-place bands of part 5 take 0.972 and $\tfrac{35}{36}$ and hold each slip.
2. Validator: 0 errors; no warning on `problems-4.json` (three `[O2-explain-answer]` fixed by stating the key in the explanation).
3. Playthrough `--problems linear-maps/problems-4 --local-cdn <pkgs>`: green on desktop and with `--mobile` (3 problems, 15 parts, 18 typed slips routed). Shots at 440 px read: the $3 \times 3$ matrices in the prose and the feedback set cleanly, no overflow.
4. Voice scan 35 on the course folder: 0 and 0.
5. `grade-all.mjs --file problems-4.json --local-cdn`: 15 widgets, 0 failures.

## Level 4 freshness

`fresh-check --file`: 0 hits; 2 advisories, the basis $(1, x, x^2, x^3)$ shared with l4 and l5 (stock).

Reuse (DECISIONS AB, and the `reuse` findings of `review-problems-linear-maps-1-3.md`, which were lesson-hook settings retold). I read l15 to l19, `review-4` and `homework-4` first and listed their settings: AR(2) companion matrices and cycles, principal portfolios from a covariance, equicorrelated assets, the hump-shaped response of a Jordan block, the shift on $\mathcal{P}_2$, rotations, weighted adjoints, Hermitian $2 \times 2$ examples, power iteration by deflation. None is used: the settings are a footbridge's two sensors, a spring linkage, and the operator $p \mapsto p + p''$. A first idea, differentiation on $\operatorname{span}(e^{2x}, xe^{2x}, x^2e^{2x}, e^{-x})$, was dropped: its single chain and $d = (1, 2, 3)$ retell the shift chain of l18 and l19.

Matrices: a scratch scan (`SCRATCH/author-linear-maps/matrices.py`) compared $\mathbf{S}$, $\mathbf{S} - \mathbf{I}$, $\mathbf{S} - 7\mathbf{I}$, $\mathbf{K}$, $\mathbf{K} - \mathbf{I}$, $[T]$, $[T] - \mathbf{I}$ and the Jordan form with every `pmatrix` and canvas `rows` matrix in `app/content`, up to a scalar, the transpose and any reordering of rows and columns: 0 matches (the scan finds l17's matrix and l16's and review-4's Hermitian matrices when asked, so it reads complex entries).

Grep per problem (course folder, then `app/content`):
- `p-footbridge-modes`: "accelerometer", "footbridge" nowhere; "vibration sensor" only in `stat-learning` (clustering), so the item says accelerometers. $(8, -7)$, $(5, 2 - i)$, $\tfrac{35}{36}$ not in the course.
- `p-spring-linkage`: "spring", "linkage", "stiffness matrix" not in the course (stiffness appears in `numerics` as stiff equations). $(1, 2, 2)$ is l12's vector $\mathbf{u}$ in a Cauchy-Schwarz example, a single vector in another role; $(2, 1, -2)$, $(2, -2, 1)$, $(15, 6, -10)$ not found.
- `p-curvature-operator`: $p + p''$, $x^3 + 6x$ not found; $\mathcal{P}_3$ is common (l6, l8 differentiate it into $\mathcal{P}_2$, `problems-2` reports a curve). $(2, 4)$ and $(4, 2)$ occur as unrelated small pairs.

Backlog: one bullet under "Raised later (problems linear-maps level 4):".
