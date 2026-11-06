# linear-maps level 4 (Operators): report

Author: content agent, worktree `worktree-agent-a402571da00abd115`. Brief: `## Level 4` of `docs/briefs/linear-maps.md`.

## Files written

| File | Screens | Quiz / items | Skills |
|---|---|---|---|
| `l15-eigenvalues-exist.json` | 12 | 5 | lx-spectral |
| `l16-self-adjoint.json` | 12 | 4 | lx-spectral, lx-inner |
| `l17-spectral-theorem.json` | 12 | 5 | lx-spectral |
| `l18-generalised-eigenvectors.json` | 11 | 4 | lx-jordan |
| `l19-jordan-form.json` | 11 | 5 | lx-jordan |
| `review-4.json` | | 8 (difficulty 2 to 4, `pass: 0.8`) | all three |
| `homework-4.json` | | 8 (difficulty 3 to 5, two at 5) | all three |

Ids, titles, objectives and skills are copied from `course.json` (the l19 objective keeps its typographic apostrophe). Homework-4 ends with the exit-line longform "Prove the spectral theorem for real symmetric matrices without notes", marked `"performance": "derivation"` (the objectives start with "Prove", so the verb rule matches; one task in the level). Its 10-point rubric covers induction and base case (1), the real eigenvalue with its reason (2), normalisation (1), the complement's dimension (1), invariance by symmetry (2, `required`), the restriction (1), assembling the basis (1) and the converse (1). The homework also has an `order` item (invariant complements of a self-adjoint operator) and the difficulty-5 `code` item `spectral_by_deflation`.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; no warning names a level 4 file.
2. Voice scan, `VOICE_BASE=app/content/courses/linear-maps python3 docs/reviews/voice-scan.py`: level 4 files 0 sentences over 20 words and 0 explanations over three sentences. The folder as a whole reports 9 and 0; all 9 are in older levels, not edited: `homework-1` items 3 prose and 8 model, `l13` screen 8 prose, `l14` screen 8 prose, `l4` screen 10 prose, `l5` screen 5 prose and screen 10 explain, `l8` screen 9 `how`, `l9` screen 10 prose.
3. `python3 docs/reports/linear-maps-L4-numbers.py`: 242 of 242 checks, exit 0. It imports `app/tools/numbers_lib.py`, recomputes every value with exact fractions or complex arithmetic, calls `lv.check_wrongs()` then `lv.report()`.
4. Playthrough with `--local-cdn` (scratchpad `pkgs`): all 5 lessons, the review and the homework green on desktop, with `--mobile` (440) and with `--tablet` (1032, 1376). Code widgets were also run in CPython: every solution passes every test and example, every starter fails at least one.

## Playthrough per file

All "ok": l15 17 checks, quiz 5/5; l16 16 checks, 4/4; l17 17 checks, 5/5; l18 15 checks, 4/4; l19 16 checks, 5/5; review-4 8 of 8; homework-4 8 of 8, 36 of 36 marks, longform marked by the button. Screenshots looked at (desktop and 440): layout faults fixed were a skewed basis grid and a basis arrow lying on the image arrow (see backlog), an edge-on plane in l17 (camera moved to az 0, el 15), and a tall complex-map on the phone (panel height 200).

## Proofs and the widget that grades each step

- l15, Axler 5.19: `order` of 7 lines plus a distractor (factor over R) on the derive screen; `choice` for why the list is dependent (generalise screen), why $p$ is not constant (quiz 1), why some factor is not injective (quiz 2); the line that fails over R (`choice`, trap); finite dimension (`choice`, quiz 3); degree 1 when $\mathbf v$ is an eigenvector (`numeric`, quiz 4).
- l16, real eigenvalues (Axler 7.12): `choice` for $\langle \mathbf v, \lambda\mathbf v\rangle = \bar\lambda\langle\mathbf v,\mathbf v\rangle$, `order` of 5 lines with a distractor that drops the conjugate. Orthogonal eigenvectors: `order` of 4 lines with a distractor. Spot the flaw: `table` canvas with `tap: "rows"` and `tap-regions` (the line that writes $\mu$ for $\bar\mu$ without citing the first theorem). Which step uses $T = T^*$: `choice` (quiz).
- l17, spectral theorem (Axler 7.29): real eigenvector `choice` (generalise); 9-line `order` with an "invertible" distractor (derive); the same skeleton as `place` in assign mode, six reasons to six lines plus two spare reasons; the invariance step's property `choice` with distractors "invertible" and "eigenvalues real" (quiz 1); restriction self-adjoint `choice` (quiz 2); spot the flaw for $\mathbf N$ as a `pair` of a tappable table and a `vectors` canvas showing $\mathbf N(0, 1) = (1, 3)$ off its line.
- l18: kernels of powers grow, two-line `order` with a distractor; Axler 8.2, 6-line `order` with a distractor; settling by $k = \dim V$ `choice` (generalise); the key step `choice` (quiz 1). Axler 8.22 is stated with a sentence that the proof is in Axler and not examined.
- l19: existence not examined; the chain-independence core is a 5-line `order` with an "apply $N^m$" distractor.
- Homework: invariant complement `order`; the full spectral proof `longform` with rubric.

## Numbers and their sources

All are checked in the script at the JSON path where they are stated. The main ones: $\mathbf A\mathbf v = (2, 1)$, $\mathbf A^2\mathbf v = (5, 4)$, $(a, b) = (4, -3)$, $(\mathbf A - \mathbf I)\mathbf v = (1, 1)$, $\mathbf A(1,1) = (3, 3)$; rotation $(0, 1)$, $(-1, 0)$, $z^2 + 1$, $(i, 1)$, $\mathbf R(i, 1) = (-1, i)$; AR(2) eigenvalues $0.5 \pm 0.5i$, modulus 0.7071, angle $\pi/4$, period 8, zero crossings at 3, 7, 11, 15 and $x_8 = 0.0625$ (compute and report: the recursion gives 1, 1, 0.5, 0, -0.25, -0.25, -0.125, 0, 0.0625, ..., 0.00390625 at $t = 16$); annihilating polynomials `[1, -4, 3]`, `[1, -3]`, `[1, 0, 1]`, `[1, -6, 11, -6]`. l16: $(6, 3)$, $(-2, 4)$, inner products 0 and 1, $45°$, eigenvalues 3 and $-2$, Hermitian 1 and 3, weighted pair 1 and 2, adjoint $\begin{pmatrix}0&0.5\\2&0\end{pmatrix}$, covariance 0 with variances 8 and 4; quiz Hermitian 3 and $-1$. l17: $(4,4,4)$, $\mathbf A(1, 2, -3) = (1, 2, -3)$, inner product 1 ($60°$), $\mathbf f = (0.5, 0.5, -1)$, $\mathbf Q^T\mathbf A\mathbf Q = \operatorname{diag}(4, 1, 1)$ (checked exactly on unnormalised columns), $\tfrac12$ in the trap, $\mathbf N(0,1) = (1, 3)$, equicorrelated eigenvalues $1 + 2\rho$ and $1 - \rho$ for $\rho = 0.5, -0.5, -0.6$ (2, 0.5, 0.5; 0, 1.5, 1.5; -0.2, 1.6, 1.6), equal-weight variance $2/3 \approx 0.6667 = (3 + 6 \times 0.5)/9$. l18: $\mathbf N\mathbf e_2 = \mathbf e_1$, $\mathbf N^2 = 0$, $d_k$ for $\mathbf A_3$ (1, 2, 2 and 1), the shift (1, 2, 3, chain $x^2 \to 2x + 1 \to 2$), $2\mathbf I$ (2, 2), $\mathbf M$ (2, 3, 4, 4); the hump $t \cdot 0.9^{t-1}$ checked against the top-right entry of $\mathbf A^t$ for all 21 values: 1, 3.2805, peak 3.8742 at 9 and 10, 2.7017 at 20. l19: $d_k$ of $\mathbf M$, $\mathbf K$ and the third matrix, each rebuilt as $\mathbf P\mathbf J\mathbf P^{-1}$ with $\det \mathbf P = 1$; block sizes [3, 1], [2, 2], [2, 1, 1], [2], [3], [1, 1], [2]; the four frame captions; $J_3(1)$ in the chain basis via $\mathbf B^{-1}\mathbf S\mathbf B$; $\pm 10^{-5}$. Review: $(5, -6)$, $\mathbf C^2\mathbf v = (-2, 0)$, Hermitian 1 and 4, blocks 4 and 1, modulus $\sqrt{0.72} \approx 0.8485$ and $0.72^4 \approx 0.2687$. Homework: blocks 4, 2, 1 from $(3, 5, 6, 7, \dots)$, blocks 3, 2 against 4, 1, $z^2 - 7z + 10$, hump peak 2.048 at 4 and 5, weighted adjoint entry 6 and $2/3$.

`check_wrongs` "check by hand" lines, all read and correct: l15 `coords` (6 is the sum of (3, 3)), `eighth` (0.125 is $|x_6|$); l16 `swap` (root of the wrong factoring), `off` (two off-diagonal 1s), `diag` (the diagonal 1); l17 `twelve`, `ninth` ($3/9$), `other` ($1.5/3$); l18 `grow`; l19 `same`, `dk`, `eps`.

## Seeds and tolerances (homework code item)

`spectral_by_deflation` is tested on the equicorrelated matrix ($\rho = 0.5$, 500 iterations, seed 0; eigenvalues `[2.0, 0.5, 0.5]` after rounding to 6) and on $\mathbf S = \mathbf X\mathbf X^T$ with `X = np.random.default_rng(3).standard_normal((4, 4))` (eigenvalues about 21.7787, 6.3191, 1.1407, 0.0986, distinct; 1000 iterations, seed 1). The stated tolerance is `np.allclose(..., atol=1e-6)`; CPython reaches errors near 1e-14 for the eigenvalues, $\mathbf S\mathbf Q - \mathbf Q\boldsymbol\Lambda$ and $\mathbf Q^T\mathbf Q - \mathbf I$, and the Pyodide playthrough passes.

## Deviations from the brief

- `vectors` with `state.matrix` draws the image grid, $\mathbf b_1$, $\mathbf b_2$ and the unit square with no way to hide them; $\mathbf b_1$ then lies on the image arrow (for $\mathbf A\mathbf e_1$, $\mathbf R\mathbf v$, $\mathbf R^2\mathbf v$). Image arrows are written by `derive` formulas on plain vectors instead (l15 screens 3 and 6, l16, l18 screen 0). Backlog bullet raised.
- l15: the $(a, b)$ expression sits on the explore screen, with sliders for $a$ and $b$; the eigenvalue $i$ expression is quiz item 1, the $(i, 1)$ expression a ladder screen.
- l17: the hook's table became the explore screen's `table` widget for $\mathbf A(1, 2, -3)$, with sliders driving $\mathbf u$.
- l18: the shift chain uses a `table` (the brief allowed it) rather than `manipulate`.
- The optional `plane` for the chain is not used.

## course.json

No change proposed.
