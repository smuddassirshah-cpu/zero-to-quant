# Fluency sets: eigen (brief `docs/briefs/fluency.md`, second wave, agent 2, topic 1.4)

One of the eight topic 1.4 sets. Chosen lesson:

- `l2-characteristic`: the characteristic polynomial, both eigenvalues of a $2 \times 2$, and an eigenvector from one row of $\mathbf{A} - \lambda\mathbf{I}$ are the course's one rote procedure.

Considered and left out: `l1-directions-that-stay` (the idea), `l3-eigenbasis` (the answer is $\mathbf{P}$, $\mathbf{D}$ or a matrix power, a whole matrix), `l4-where-it-settles` (a steady state is procedural, but the topic has eight sets and l2 is the root technique; a candidate for a later wave), `l5` to `l17` (spectral theorem, definiteness, SVD, PCA, Cholesky and the rest: judgements, matrix answers or NumPy code).

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l2-characteristic | characteristic-polynomial | 198 | `expanded` | sign-of-sum, added-bc |
| | both-eigenvalues | 176 | none (numeric set, unordered) | diagonal-entries, signs-flipped |
| | eigenvector | 181 | none (numeric) | sign-slip, upside-down |

`expanded` stops $(a - \lambda)(d - \lambda) - bc$ passing for "Expand". The eigenvalue family builds $\mathbf{A}$ from two distinct whole eigenvalues $l_1 < l_2$ with diagonal $l_1 + t$ and $l_2 - t$ and off-diagonal product $t(l_2 - l_1 - t)$, so every draw has whole roots and $b, c \ne 0$ (the diagonal slip can never be right). The eigenvector family draws $a$, $b$, $\lambda$ and builds the second row so that $\lambda$ is an eigenvalue, giving $v = (\lambda - a)/b$ in many fractions rather than mostly $\pm 1$. The slips are the lesson's: reading the diagonal, flipping the root signs, the sign of the middle coefficient, $ad + bc$.

## Checks

1. `docs/reports/fluency-eigen-numbers.py` (sympy, 200 draws a family): the matrix rebuilt from the vars, then `charpoly`, `eigenvals` and the `nullspace` of $\mathbf{A} - \lambda\mathbf{I}$ (with $\mathbf{A}\mathbf{v} = \lambda\mathbf{v}$ checked). 1,766 checks, 0 failures, exit 0.
2. Validator 0 errors, no warning on this file. `test-fluency.mjs --local-cdn`: 305/305.
3. Playthrough `--fluency --local-cdn`, with and without `--mobile`: green.
4. `voice-scan.py 35` on `app/content/courses/eigen`: 0 and 0.
5. I read 20 drawn items of every family and scanned 200 a family: the scan found "$2+0$" in a diagonal sum and "$\mathbf{A} - 1\mathbf{I}$"; both fixed (non-zero diagonal; "with $\lambda = 1$"). Final scan clean; no prompt gives the answer away.

## Engine limits

`test-fluency` grades the `\lambda` keys correctly, but I did not confirm that the on-screen maths keyboard offers $\lambda$ (the widget has no Greek option of its own); raised as a check in `docs/BACKLOG-INBOX.md` under `Raised later (fluency vectors elimination eigen least-squares):`.
