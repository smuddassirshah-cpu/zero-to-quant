# Concept audit: odes chained problem sets 1 to 4 (blind)

Scope: `app/content/courses/odes/problems-1.json` to `problems-4.json` at commit 5fce6b73: 12 problems, 55 parts. Brief: `docs/briefs/concept-audit.md`, "Auditor brief (binding)", full ledger (Stage 1 to 3 depth). Lessons were opened only to check a convention (l1 compounding, l9 damping ratio and overshoot, l2 and l4 constant solutions, l18 the RK4 limit).

Method. Every equation was typed from the item's prose into `docs/reports/odes-problems-concepts.py`. Each solution was found twice: symbolically with sympy (`dsolve`, `residue`, `laplace_transform`, eigenvalues, the Jacobian) and numerically with scipy `solve_ivp` (DOP853, rtol 1e-11). Every key, every slip value and every number printed in feedback or an explanation is recomputed from the mistake its line names. Euler and RK4 were run as written, on the scalar equation and on the two-compartment system at n = 51, 52, 71, 72 and 73. The script reads the keys from the content files. Versions: sympy 1.14.0, SciPy 1.18.1 (newer than CI's pins; no figure depends on the version).

## Result

No key, tolerance, slip value or printed number is wrong: 169 checks, exit 0. Chained parts all restate the value carried forward, and each slip chain (for example $A = 7$, $0.2$, $\tfrac18$ into part 5 of `p-lending-members`) gives the slip value stated. The watch list came out as follows.

- Existence and uniqueness: not used in these sets; no claim to check.
- Separable step (`p-lending-members`): dividing by $(m - 2)(6 - m)$ drops the constant solutions $m = 2$ and $m = 6$. The item fixes $m(0) = 2.5$, so nothing is lost and nothing false is said; l2 teaches the point. Ledger row correct.
- Characteristic equation: complex (`p-hedge-overshoot`, `p-cash-buffer`) and repeated (`p-tracking-gap`) cases are right, with the $(c_1 + c_2t)e^{rt}$ form and the one-crossing remark.
- Resonance: both trial solutions state why no extra $t$ is needed (0 and $\pm i$ are not roots).
- Stability: `p-liquidity-arbitrage` says "for the linearised system" and the point is hyperbolic, so the type carries over; a nonlinear run agrees on both the inward spiral and the turn time. One local-to-global slip of reasoning in `p-lending-members` (finding 2).
- Units and time scales: all consistent (months, years, days, weeks, hours, seconds). One compounding convention left unstated (finding 1).

## Findings

1. `odes/problems-1.json` | `items[2].prose` (`p-rising-pension`; keys of parts 1, 3 and 4 depend on it) | imprecise | minor | "Payments start at £2,000 a year and rise by 2% a year, compounded continuously, and the fund earns 4% a year." The word "continuously" attaches to the payments only. The keys $0.04B$ and £27,042 need the fund's 4% to be a continuous rate too. | l1 teaches the difference: yearly 5% has slope $\ln(1.05)B$, "a little short of $0.05B$", and l1's loan says "6% a year, continuously". A learner who reads the fund's 4% as yearly gets $B' = \ln(1.04)B + 2000e^{0.02t}$ and $B(10) \approx$ £26,934, marked wrong on the generic line (script check F1). Basis: Boyce and DiPrima 2.3, compound interest. | `prose`: "A saver pays into a pension continuously. Payments start at £2,000 a year and rise by 2% a year. The fund earns 4% a year. Both rates are compounded continuously. $B(t)$ is the fund in pounds after $t$ years, with $B(0) = 0$."

2. `odes/problems-1.json` | `items[0].parts[1].explain.text` (`p-lending-members` part 2) | imprecise | minor | "Membership that starts at 2.5 therefore heads for 6." The "therefore" follows two sentences about a small gap near an equilibrium. A start at 2.5 is 3.5 away from 6, so the linear test does not give its fate; the right answer is reached by the wrong reasoning. | The linearisation $u' = f'(m^*)u$ is local (Strogatz 2.4). What sends 2.5 to 6 is the sign of $f$ on the whole interval: $f(m) = -(m - 2)(m - 6) > 0$ for $2 < m < 6$ (Strogatz 2.2; script check P1.2). The earlier review's finding 2 fixed "obeys" to "nearly obeys" in the first sentence; this is the last sentence. | Replace the last sentence: "Between 2 and 6, $f(m) > 0$, so membership that starts at 2.5 rises all the way to 6."

3. `odes/problems-3.json` | `items[0].parts[2].feedback.correct` and `items[0].parts[2].explain.text` (`p-yield-gaps` part 3) | imprecise | minor | "every path runs into the origin without turning" and "neither turns ... So the gaps close without oscillating". Paths into a node do bend, and in this very item both gaps overshoot zero before they close. A learner reads "closes without turning" as a monotone approach. | With $\mathbf{x}(t) = -e^{-t}(1, 3) + 5e^{-5t}(1, 1)$: $y = 0$ at $t = \tfrac14\ln\tfrac53 \approx 0.13$ weeks and $x = 0$ at $t = \tfrac14\ln 5 \approx 0.40$ weeks. The path leaves $(4, 2)$ heading down and left, crosses both axes and comes in from the third quadrant along $(1, 3)$ (script check F3). The lessons l10 to l13 do not use "turning" as a term for spiralling. Basis: Strogatz 5.2 (a node has no rotation; a sum of two real exponentials has at most one zero). `p-tracking-gap` part 4 already says "cross once" with care. | `feedback.correct`: "Two real negative eigenvalues: every path runs into the origin without spiralling. It is a stable node." `explain.text`: "Both modes $e^{-t}$ and $e^{-5t}$ decay, and neither spirals, since the eigenvalues are real. So the gaps close without oscillating, though each may cross zero once: a stable node. In trace and determinant terms, $\tau < 0$, $\Delta > 0$ and $\tau^2 - 4\Delta = 16 > 0$."

4. `odes/problems-4.json` | `items[2].parts[0].feedback.byKey.signs` (`p-dose-simulator` part 1) | imprecise | minor | "Both amounts decay, so both eigenvalues are negative". The blood amount does not simply decay: it is fed by the gut and rises first. The eigenvalues are negative because both modes decay. | For a tablet, $b(0) = 0$ and $b(t) = \tfrac{6g_0}{5.5}(e^{-0.5t} - e^{-6t})$, which rises until $t = \tfrac{\ln 12}{5.5} \approx 0.45$ hours and then falls (script check F4). Basis: Boyce and DiPrima 7.5; the part's own `explain` speaks of modes. | `byKey.signs`: "Each diagonal entry is a loss rate with a minus sign, so both modes decay: $-6$ and $-0.5$."

No finding needs a screen rewritten.

## Counts

| severity | count | serious | minor | findings |
|---|---|---|---|---|
| wrong | 0 | 0 | 0 | |
| imprecise | 4 | 0 | 4 | 1, 2, 3, 4 |
| misleading | 0 | 0 | 0 | |

Ledger: `docs/reports/audit-odes-problems-1-4-ledger.md`, 410 rows: correct 405, imprecise 5 (finding 3 covers two rows), wrong 0, misleading 0, unverified 0.

## Overlap with the earlier reads

Read after the ledger and findings were written: `docs/reviews/review-problems-odes-1-3.md`, `docs/reviews/review-problems-odes-4.md`, `docs/reports/problems-odes.md`, `docs/reports/problems-odes-4.md`. No earlier `audit-*` file covers these sets. Only conceptual findings are counted (the earlier reuse, voice and continuity findings are outside this brief).

| found by | count | which |
|---|---|---|
| this audit only | 4 | 1, 2, 3, 4 |
| earlier reads only | 4 | review 1-3 findings 1 ($dq$ for $dm$), 2 (linear law stated as exact), 3 (critical damping "promises" no crossing); review-4 finding 2 (RK4 limit stated for any $\lambda$). All four are fixed in the text audited here. |
| both | 0 | Finding 2 here is in the same `explain` as review 1-3 finding 2 but is a different defect. |

New `wrong`: 0.

## Checks run

- `cd app && node tools/validate.mjs`: 0 errors, 4615 warnings.
- `node tools/run-number-scripts.mjs --only odes`: 9 of 436 scripts, 9 passed, 0 new failures.
- `node tools/grade-all.mjs --file content/courses/odes/problems-N.json --local-cdn <pkgs>` for N = 1 to 4: 13, 13, 14 and 15 widgets checked, 0 failures each.
- `python docs/reports/odes-problems-concepts.py`: 169 checks, 0 failed, exit 0. The checks named F1, F3 and F4 state the facts behind findings 1, 3 and 4, so they pass before and after a fix.
- No playthrough, as the brief sets.

## Engine

No new engine limit. Nothing added to `docs/BACKLOG-INBOX.md`.
