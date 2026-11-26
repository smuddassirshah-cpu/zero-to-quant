# Blind concept audit: numerics problems-1 to problems-4

Commit 65be5221, branch `worktree-agent-a0cd8519580a7df14`. Scope: `app/content/courses/numerics/problems-1.json` to `problems-4.json` (13 items, 59 parts: 58 numeric, 1 choice). Stage 2, full ledger. No file has a code widget or a hint field, so there are no `test-N` lines to sweep.

Ledger: `docs/reports/audit-numerics-problems-1-4-ledger.md`, 451 rows: 449 correct, 2 imprecise, 0 wrong, 0 misleading, 0 unverified.
Script: `docs/reports/numerics-problems-concepts.py`, 601 checks, 2 failing (the two findings below), exit 1.

## What was checked

- Every key, every slip value against the mistake its feedback names, and every figure printed in prose, feedback and explanations, recomputed independently (IEEE doubles and float32 through NumPy, mpmath at 50 digits for the Newton errors and the moment integrals, SciPy for the normal CDF, the spline and the banded solves).
- Chaining: every "from part k" names the right part and carries the figure that part prints; where a part prints a rounded figure, the rounded route also lands inside the key's band (checked for P1 items 0 to 2, P2 item 2, P3 items 0 and 1, P4 item 0).
- Per cent keys are fractions (0.000596 for 0.060%, 0.088963 for 8.90%), as `docs/AUTHORING.md` requires.
- Floating point: float32 gap $2^{-24}$ in $[0.5, 1)$ against epsilon $2^{-23}$; double $u = 2^{-53}$ against $\epsilon = 2^{-52}$, with the slip lines the right way round; Sterbenz holds for the two factors (run in float32); the forward recurrence does return a negative $I_{18}$ in doubles ($-0.0295$ against a true 0.0501); recursive and pairwise summation obey $nu$ and $u\log_2 n$ on a cancelling sum of $2^{18}$ values (Higham s.4.2).
- Roots: Newton's order 2 is stated "near the root" with the constant $f''/2f'$; the three "real" Newton errors ($5.1 \times 10^{-4}$, $2.0 \times 10^{-7}$, $3.2 \times 10^{-14}$) reproduce at 50 digits; the safeguarded steps agree with the l6 `safe_newton` rule (the step from 0.75 is under half the step before last, so it is kept); a frozen slope is order 1 (run).
- Splines and interpolation: the extension is $C^2$ but not natural; the natural spline through the three quotes has $S''(2) = -4.2$, so it changes $p$, and it rises all the way to 3 years (SciPy). The three-point error formula carries $3!$; a $Q$ with $Q''' = \pm 0.0006$ moves the crossing by 1.96 to 1.97 days.
- Quadrature and ODEs: trapezium, Richardson (weights 4 and 1 for $h^2$, 2 and 1 for $h$), two-node Gauss-Legendre, three-node error below $10^{-6}$; the Bernoulli exact path solves the ODE; explicit Euler at $h\lambda = -3$ is outside $|1 + h\lambda| \le 1$; Euler's 4, 8 and 16 step values and the true error at 5,850 steps (below $10^{-5}$).
- Level 4: the implicit matrix and right side follow from the l13 and l14 coefficients with the put's edges; the grid errors $-0.0219$ (explicit, $M = 69$, $N = 322$), $-0.00137$ (explicit, $M = 276$, $N = 5{,}142$) and $-0.0015$ (Crank-Nicolson, $M = 276$, $N = 100$, two implicit steps first) reproduce; the control-variate variance and the unbiasedness of a fixed $b$ (Monte Carlo, 4,000 runs of 2,000 paths); the antithetic digital's $\rho = -0.25$ and pair variance 138.24 (4 million pairs).

## Findings

1. `problems-4.json` | `items[0].parts[0].explain.text` | imprecise, minor | "The step is 1.145 times the longest the explicit bound allows here" uses a bound the course does not call the explicit bound. | l13 defines the bound as $\Delta\tau \le 1/(\sigma^2M^2 + r)$ with $j = M$, and item `p-grid-node-budget` of this same set uses it with $M$. Here $M = 4$, so that bound is $1/4.04 = 0.2475$ and the step of 0.5 is 2.02 times it. The figure 1.145 is $\Delta\tau(\sigma^2j^2 + r)$ at $j = 3$, the weight condition at the top interior node only. A learner who checks the sentence with the course's formula gets 2.02. | Replace the second sentence of the explanation with: "At $j = 3$, the top interior node, the step is 1.145 times the longest that keeps this weight non-negative, so the checker steps implicitly." (Basis: l13 screen "The centre weight $1 + b_j$ stays non-negative only if $\Delta\tau(\sigma^2j^2 + r) \le 1$"; $0.5 \times 2.29 = 1.145$.)

2. `problems-2.json` | `items[0].parts[1].widget.wrong[accepted]` | imprecise, minor | The slip line says "That is $f(1.1395)$", but the slip value 60.1142 is $f(1.139535)$ and its band of 0.006 excludes $f(1.1395) = 60.1032$. | Part 2's question carries "The landing point 1.1395 from part 1", so a learner who makes this slip with the carried figure types 60.10 and gets the generic line. $f' \approx 316$ there, so the 4 dp rounding moves $f$ by 0.011. | Set the slip to `"value": 60.1087, "tol": { "abs": 0.012 }` (covers 60.1032 and 60.1142; the key $-33.90625$ and the other slips are far outside).

No finding is `wrong` and none is serious.

## Notes that are not findings

- P1 `p-moment-recurrence` part 2 asks "how large can the error in the computed $I_{18}$ be" and keys the part of it that comes from $I_0$ alone; the explanation says later roundings add more, which is enough.
- P4 `p-hand-implicit-put` part 4 keys 9.960978 from the carried 4 dp figures; the exact solve gives 9.9607. Both are 9.96 at the asked 2 places.
- P1 `p-netting-sum` part 2, slip `no-kappa` (0.004657, band 0.0005): a learner who rounds to the asked 2 places types 0.00 and misses the line. Cosmetic.

## Checks run

- `cd app && node tools/validate.mjs`: 0 errors (4,615 warnings, repository-wide).
- `node tools/run-number-scripts.mjs --only numerics` (venv Python first on PATH): 8 of 436 scripts, 8 passed.
- `node tools/grade-all.mjs --file content/courses/numerics/problems-N.json --local-cdn <pkgs>` for N = 1 to 4: 13, 15, 14 and 18 widgets, 0 failures each.
- `docs/reports/numerics-problems-concepts.py`: 601 checks, 2 failed (findings 1 and 2), exit 1. Venv NumPy and SciPy are newer than CI's pins; no figure depends on the version.
- No playthrough, as the common rules set.

## Overlap with the earlier reads

Read after the ledger and findings were written: `docs/reviews/review-problems-numerics-1-3.md`, `review-problems-numerics-4.md`, `review-delta-af-numerics.md` and `docs/reports/problems-numerics.md`.

| conceptual findings | count |
|---|---|
| this audit only | 2 (both imprecise, minor; new `wrong`: 0) |
| earlier reads only | 10 (`wrong` 2, `misleading` 8), all fixed before commit 65be5221, so none was there to find |
| both | 0 |

Finding 1's sentence was written by the first reader's fix (`review-problems-numerics-4` finding 5, a reuse replacement, checked there against the bound at $j = 3$). Finding 2 is the class of `review-problems-numerics-1-3` finding 8 and `review-delta-af-numerics` finding 2 (a slip value built from the unrounded figure), on a part neither read flagged. The earlier fixes hold: each one's text was a ledger row here and recomputes.

Inbox: one bullet under "Raised later (audit numerics)" in `docs/BACKLOG-INBOX.md` (slip values against carried figures).

## Fix pass

Opus fixer, from commit bea50a86. Figures recomputed in `scratchpad/fix-num-ps/check.py` (exact fractions and mpmath Horner).

1. Fixed differently. Basis: l13 sets the bound with $j = M$, which here gives $0.5 \times (0.25 \times 16 + 0.04) = 2.02$; the weight condition at $j = 3$ gives $0.5 \times 2.29 = 1.145$, that is $0.5 / (1/2.29)$. The sentence now reads "The step is 1.145 times the longest that keeps the $j = 3$ weight non-negative, so the checker steps implicitly." The auditor's wording ran to 25 words and raised an O2 warning, so it was shortened.
2. Fixed differently. Basis: $f(1.1395) = 60.10318$ and $f(1.1395349) = 60.11420$, each by exact fractions and by Horner at 30 digits. The slip now centres on the value its line names, `"value": 60.1032, "tol": { "abs": 0.012 }`, so it fires for 60.1032, the unrounded 60.1142 and the 2 dp entries 60.10 and 60.11. The key $-33.90625$ and the slips 20 and 33.90625 are far outside the band.

Scripts: `docs/reports/numerics-problems-concepts.py` finding check 1 encoded the old sentence and is re-pointed (docstring says so); 603 checks, 0 failed, exit 0. `docs/reports/delta-review-delta-af-numerics-numbers.py` line "finding 5 applied" matched the old sentence and is re-pointed to the new one; 265 checks, 0 failed.

Gates: validator 0 errors (4,615 warnings, none new); voice scan 35 on both files 0 and 0; `run-number-scripts --only numerics` 8 of 8 passed; `grade-all --file` problems-2 (15 widgets) and problems-4 (18 widgets) 0 failures; playthrough `--problems numerics/problems-2` and `problems-4`, desktop and `--mobile`, all passed. No key, hidden test or solution changed; one slip value and band changed.

## Fix-pass read

Fresh reader, blind to the audit above until these rows were written. Diff read: the content lines of commit 750c7515 under `app/content/courses` (two changed lines). Numbers recomputed with exact fractions and again with `decimal` Horner evaluation.

| # | file | JSON path | claim | verdict | basis |
|---|------|-----------|-------|---------|-------|
| 1 | problems-4.json | `p-hand-implicit-put` parts[0].explain.text, sentence 2 | "The step is 1.145 times the longest that keeps the $j = 3$ weight non-negative, so the checker steps implicitly." | correct | l13 screen 5: centre weight $1 + b_j = 1 - \Delta\tau(\sigma^2j^2 + r) \ge 0$ iff $\Delta\tau \le 1/(\sigma^2j^2 + r)$. At $j = 3$: $\sigma^2j^2 + r = 0.25 \times 9 + 0.04 = 2.29$, longest step $1/2.29 = 0.43668$, and $0.5 \times 2.29 = 1.145$. The old wording ("the explicit bound") was false: l13's bound is taken at $j = M = 4$ (nodes 0 to 40, $\Delta S = 10$), where $0.5 \times (0.25 \times 16 + 0.04) = 2.02$. A negative weight at an interior node also breaks the $j = M$ bound, so "steps implicitly" follows. |
| 2 | problems-4.json | same text, sentences 1 and 3 (unchanged, read in context) | $-0.145$; implicit diagonal $1 + 1.145 = 2.145$, last matrix entry | correct | $1 - 1.145 = -0.145$; matrix entry (3,3) in the prose is 2.145. The 1.145 at entry (1,1) is the $j = 1$ diagonal $1 + 0.5 \times 0.29$, a coincidence that does not clash with the sentence. |
| 3 | problems-2.json | `p-project-irr` parts[1].widget.wrong[0].value | `accepted` slip value 60.1032 = $f(1.1395)$ | correct | Exact: $f(2279/2000) = 9616509239/160000000 = 60.10318274375$. Horner in decimal gives 60.103182743750. It matches the byKey line "That is $f(1.1395)$" and the question's carried value 1.1395. |
| 4 | problems-2.json | `p-project-irr` parts[1].widget.wrong[0].tol | band 0.012, that is [60.0912, 60.1152] | correct | Catches the carried form 60.1032 (typed 60.10, 60.1, 60.103) and the unrounded form $f(49/43) = 4779500/79507 = 60.11420$ (typed 60.11, 60.114, 60.1142; offset 0.0110, margin 0.0010). Does not catch the key $-33.90625$, `endpoint` 20 or `sign` 33.90625, and no other route lands in the band: $f(1.14) = 60.2612$ and the part 1 sign slip gives $f(-0.1395) = -103.54$, both of which fall to the generic line. The old pair (60.1142, 0.006) had a floor of 60.1082 and missed the carried 60.1032 and a typed 60.10. |

Counts: 4 rows; correct 4, wrong 0, imprecise 0, misleading 0, unverified 0. No fix needed.

Note, outside the diff and not a finding: a learner who rounds part 1 to 2 decimal places and evaluates $f(1.14) = 60.26$ gets the generic line. The question carries 1.1395, so the band rightly stops short of it.
