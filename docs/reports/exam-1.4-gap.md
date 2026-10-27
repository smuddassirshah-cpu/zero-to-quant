# Topic 1.4 exam: gap extension for eigen level 4

File: `app/content/exams/topic-1.4.json` (id `topic-1.4`, 60 minutes, pass 0.7, header unchanged).
Generator and checks: scratchpad folder `exam-1.4` (`code_items.py` holds the code items' preludes, starters, solutions, wrong versions and test specs; `chk.py` builds the expected values from the reference solutions and grades solution, starter and wrong versions with `harness.py`, a CPython copy of the app's `__zq_cmp`; `gen.py` builds the four items and appends them; `verify.py` recomputes every stated number by a second route; `final_chk.py` re-grades the code items as written in the exam file; `lint.py` checks voice).

## What changed

Four items appended after `a-minvar-long`. The 26 existing items are byte-for-byte unchanged and in their old order: `gen.py` asserts that the new file starts with the text of the pre-extension version (commit `42dbeff`) up to the end of its last item.

| # | id | d | skills | widget | rests on (eigen L4, `docs/reports/eigen-4.md`) |
|---|---|---|---|---|---|
| 27 | `a-expm-spreads` | 3 | eg-diag, eg-eigen | numeric | l14 screens 2 to 4, homework `h-expat` |
| 28 | `a-chol-conditional` | 3 | eg-pd | table (5 cells) | l15 screens 1, 3 and 4, `h-chol3`; l16 screens 2, 6 and 8, `h-cond` |
| 29 | `a-code-normal-eq` | 4 | ls-fit, eg-pd | code (7 tests, bans `lstsq` and `pinv`) | l17 (normal equations against the pseudoinverse), `pinv_svd`, `h-code-lstsq`; topic exam `a-beta` |
| 30 | `a-code-pca-changes` | 4 | eg-pca | code (8 tests) | l11, l12 (`eigh` order, the sign rule), l16 (covariance) |

Ramp after the extension, 30 items: difficulty 2 has 5 (17%), 3 has 15 (50%), 4 has 7 (23%), 5 has 3 (10%), against 20/50/20/10 ± 10.

## Coverage of the gaps-plan bullet

All five asks are covered, in four items:
- $e^{\mathbf{A}t}\mathbf{u}_0$ for a $2 \times 2$ system: `a-expm-spreads`.
- A Cholesky factor by hand: `a-chol-conditional`, cells $L_{11}$, $L_{21}$, $L_{22}$.
- A conditional mean of a bivariate normal: `a-chol-conditional`, cells $E[Y \mid X = -5.8]$ and the conditional sd.
- A normal-equations code item that bans `lstsq`: `a-code-normal-eq` (it bans `pinv` too).
- A PCA code item: `a-code-pca-changes`.

Why two asks share one item: `validate.mjs` caps a topic exam at 30 items and the exam held 26. The pair is a natural one: the factor's first column turns $X = x$ into $Z_1 = (x - \mu_X)/L_{11}$, so the conditional mean is $\mu_Y + L_{21}Z_1$ and the conditional sd is $L_{22}$. Each part is its own cell with its own feedback line.

The pseudoinverse route was not chosen for the code item because l17 (`pinv_svd`) and homework 4 (`h-code-lstsq`) already set it; the normal equations with a multi-stock right-hand side are new.

## Code items (CPython NumPy 2.5.3 with `harness.py`; Pyodide 0.27.7, NumPy 2.0.2, in the playthrough)

| item | tests | solution | starter | wrong versions (each fails; first failing test) |
|---|---|---|---|---|
| `a-code-normal-eq` | 7 | 7/7 | 0/7 (stops with an error) | no column of ones (1), result transposed (1), `np.linalg.lstsq` (5), `np.linalg.pinv` (5), each factor fitted on its own (2), centred factors so intercepts become means (1) |
| `a-code-pca-changes` | 8 | 8/8 | 0/8 | PCA on levels (1), eigenvalues left ascending (1), first column of `eigh` for PC1 (5), no sign rule (5), correlation not covariance (2), no centring (1), loadings from levels only (6) |

The ban is enforced by tests 5 and 7 of `a-code-normal-eq`: each is a value check joined with `'lstsq' not in __learner_source__ and 'pinv' not in __learner_source__`, so the starter fails them too and a correct `lstsq` or `pinv` answer passes 5 of 7 and fails. Neither the starter nor the solution contains either word.

Tolerances: matrices and vectors are rounded to 6 places in the call and compared with `isclose` at an absolute 1e-6 (2e-6 on the seeded cases), so a last-digit rounding difference between NumPy builds cannot fail a correct answer. The data come from hidden preludes: `make_factors(seed, n, k, m)` and `make_curve(seed, n)`, both `np.random.default_rng`. Seeds 17, 29 and 5 (factors) and 41 and 58 (curves) are not used by the eigen lessons. Starters are wrapped to 36 characters so they fit the editor at 390 px.

## Numbers computed twice

First route in `gen.py` and `chk.py`; second in `verify.py` (33 checks, all pass).

- `a-expm-spreads`: $\mathbf{A} = \begin{pmatrix}-3&1\\2&-2\end{pmatrix}$ has eigenvalues $-1$ with $(1, 2)$ and $-4$ with $(1, -1)$ (`np.linalg.eig`; exact check by hand); $\mathbf{u}_0 = (3, 0) = 1(1, 2) + 2(1, -1)$. $u_2(0.5) = 2e^{-0.5} - 2e^{-2} = 1.2131 - 0.2707 = 0.942391$, stated 0.9424 (eigen route; second route a 60-term Taylor series of $e^{0.5\mathbf{A}}$). $u_1(0.5) = 0.877201$ (not stated). Wrong values: $t = 1$ gives 0.6991 (Taylor series of $e^{\mathbf{A}}$), one Euler step $(\mathbf{I} + 0.5\mathbf{A})\mathbf{u}_0 = (-1.5, 3)$ gives 3, the entrywise exponential gives $3e = 8.1548$, and the eigenvector slip $(1, 1)$ gives $2e^{-0.5} + 2e^{-2} = 1.4837$.
- `a-chol-conditional`: $\boldsymbol{\Sigma} = \begin{pmatrix}9&6\\6&8\end{pmatrix}$, $\boldsymbol{\mu} = (0.2, 0.1)$, $x = -5.8$. $\mathbf{L} = \begin{pmatrix}3&0\\2&2\end{pmatrix}$ (`np.linalg.cholesky`; exact fractions $6/3 = 2$, $8 - 4 = 4$). $Z_1 = -6/3 = -2$, $E[Y \mid X = -5.8] = 0.1 + 2(-2) = -3.9$ (Cholesky route; regression route $0.1 + \tfrac{6}{9}(-6)$ in exact fractions; Monte Carlo fit on 400,000 draws within 0.03). Conditional sd $L_{22} = 2 = \sqrt{8 - 36/9}$ (exact; Monte Carlo residual sd within 0.01). Named slips in the feedback: $\sqrt{8} = 2.8284$, $\Sigma_{21} = 6$, correlation $6/(3\sqrt8) = 0.7071$, variance 4.
- `a-code-normal-eq`: expected matrices from `np.linalg.solve` on the normal equations; second route QR ($\mathbf{R}_1\mathbf{B} = \mathbf{Q}^T\mathbf{R}$) agrees to 1.5e-6 on all four value cases. The one-factor case reproduces `a-beta`'s $\hat\alpha = -0.3$, $\hat\beta = 1.3$; the planted case returns its built-in intercepts $(0.1, -0.05)$ and betas $\begin{pmatrix}1&0.5\\-0.2&2\end{pmatrix}$ exactly.
- `a-code-pca-changes`: expected shares and loadings from `eigvalsh`/`eigh` of `np.cov` of the changes; second route the SVD of the centred changes agrees to 1.5e-6 on all five value cases. The four-day example by hand: changes $(1, 2)$, $(-1, -1)$, $(2, 1)$; covariance $\begin{pmatrix}7/3&11/6\\11/6&7/3\end{pmatrix}$; eigenvalues $25/6$ and $1/2$; shares $25/28 = 0.892857$ and $3/28 = 0.107143$; PC1 $(1, 1)/\sqrt2 = (0.707107, 0.707107)$. PC1 shares of the seeded curves: 0.850 (seed 41) and 0.821 (seed 58), so the feedback says "over 80%".

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors overall, no message for `topic-1.4.json` (350 warnings elsewhere in the repository). Earlier in the run the whole tree showed 19 errors, all in `topic-1.5.json` (another agent's file, in progress).
- Voice lint (`lint.py`) on the four items: no `!`, no em-dash or en-dash, no sentence of 20 words or more, explanations of at most three sentences, no American spellings, prose under 60 words.
- `node tools/playthrough.mjs --exam topic-1.4 --local-cdn <pkgs> --shots ... --mobile --why`: `ok topic-1.4 30 items, scored 30 of 30, passed` (45.1 s and 47.1 s on two runs, the second after the starters were rewrapped). No console errors.
- Screenshots of items 27 to 30, at desktop and 390 px, were inspected. The display matrices, the five-row table and the code panels fit. One fault was fixed: the first starters' docstrings and comments ran past the editor's edge at 390 px, so both starters were rewrapped to 36 characters.

## Notes

- The orchestrator's WIP commit `364fd44` landed while this work was in flight and already holds a draft of the four items. The final file differs from it only in the two rewrapped starters and solutions. A later WIP commit, `1080aa1`, holds the final file as it stands.
- The exam header (`minutes: 60`) was not changed, as the task was append-only; see the backlog bullet on timing.

## Engine notes (also in `docs/BACKLOG-INBOX.md`)

Five bullets under "Raised later (exam topic-1.4 gap extension):": the 30-item cap, table cell `wrong[]` keys rejected by the validator, the substring-based `lstsq` ban, the code editor's visible width on a phone, and the 60-minute allowance for 30 items with three code items.

## Proposed course.json change

None.
