# Concept audit: integrals levels 1 to 3, round 3

Blind read at commit `73990629` (round 2 fix pass merged). Scope: lessons l1 to l13, review-1 to -3, homework-1 to -3, problems-1 to -3, fluency l6, l7, l9, l10. Sources: Stewart, *Calculus* (8e) chapters 4.9, 5, 6.1, 6.5, 7.1, 7.7, 7.8, 8.5; Spivak, *Calculus* (4e) chapters 13, 14, 19; Apostol, *Calculus* I (2e) chapters 1, 2, 5, 10.23. Stage 1, so the full ledger.

- Ledger: `docs/reports/audit-integrals-1-3-r3-ledger.md`, 3245 rows: correct 3231, wrong 2, imprecise 12, misleading 0, unverified 0.
- Concepts script: `docs/reports/integrals-L1-3-concepts-r3.py`, 6430 checks.
- Code-widget sweep: `docs/reports/integrals-L1-3-test-line-sweep-r3.mjs`, 45 submissions.

## Verdict

No mathematical error, no wrong key, no wrong slip value and no accept figure that its own tolerance refuses. The round 2 class (a printed figure that is not what it claims) does not recur: all 163 numeric keys and 420 slip values were recomputed from the mistake each line names, and every figure an accept line prints as the answer was graded against its own band.

Four findings remain, all minor. Two are `wrong` as stated, but neither is mathematics: each is a "last lesson" pointer that names the wrong lesson. Two are `imprecise` wording.

| severity | serious | minor |
|---|---|---|
| wrong | 0 | 2 |
| imprecise | 0 | 2 |
| misleading | 0 | 0 |

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `l4-accumulating-a-rate.json` | `screens[7].explain.text` | wrong, minor | The line ends "the same squeeze as last lesson". The lesson before l4 is l3 (the definite integral as signed area), which has no squeeze. The squeeze of the area between $L_n$ and $R_n$ is in l2, `screens[7]`. | Lesson order in `course.json`: l1, l2, l3, l4. l2 `screens[7].widget.lines[4]`: "$L_n \le A \le R_n$ and both tend to $\tfrac13$ ... the area is squeezed". l3 has no line with a squeeze. The mathematics of the l4 line is correct. Script: `C l4 screens[7].explain`. | Replace the last sentence. Paste: `Each piece's change is trapped between its lowest and highest rate times $\Delta t$. Added up, the total change sits between two Riemann sums. Both converge to the integral, so the change equals it: the same squeeze as in lesson 2.`

2. `l7-evaluating.json` | `screens[8].prose` | wrong, minor | "Last lesson, for a continuous $f$, $A(x) = \int_a^x f(t)\,dt$ had $A' = f$." The lesson before l7 is l6 (antiderivatives), which never mentions $A(x)$. $A' = f$ is proved in l5. | Lesson order: l5, l6, l7. l5 `screens[6]` and `screens[7]` prove and state $A'(x) = f(x)$; l6 has no accumulation function. The mathematics of the line is correct, and the hypotheses are stated. Script: `C l7 screens[8].prose`. | Paste: `Why does $F(b) - F(a)$ work? In lesson 5, for a continuous $f$, $A(x) = \int_a^x f(t)\,dt$ had $A' = f$. Let $F$ be any antiderivative of $f$ on $[a, b]$.`

3. `l10-undo-product.json` | `quiz[3].feedback.byKey.no-integral` | imprecise, minor | "You evaluated $x\ln x$ alone. Subtract the $-x$ part between the limits too." The antiderivative is $x\ln x - x$. The missing piece $\big[-x\big]_1^e = -(e - 1)$ is added; or $\big[x\big]_1^e$ is subtracted. Read literally, subtracting the $-x$ part gives $e + (e - 1) \approx 4.437$, not 1. | $\big[x\ln x\big]_1^e = e$ (the slip value 2.7183, correct) and $e - (e - 1) = 1$. The sister lines say it unambiguously: l10 `screens[4]` "Subtract the $\int v\,du$ part, $\tfrac{x^2}{4}$", l10 `quiz[2]` "The antiderivative is $(x - 1)e^x$, not $x\,e^x$". Script: `C l10 quiz[3] byKey no-integral`. | Paste: `You evaluated $x\ln x$ alone. The antiderivative is $x\ln x - x$, so take off $\big[x\big]_1^e = e - 1$ as well.`

4. Eleven accept lines, listed below | `widget.accept` | imprecise, minor | Each line ends "accepted as $x \pm t$" or "or $x \pm t$", with $x$ the key rounded. The widget accepts `answer` $\pm$ `tol` around the unrounded key. So the printed band is shifted by up to 0.4 of its half-width, and its far edge is refused. The printed $x$ itself is accepted in all eleven, so this is not the round 2 defect. No learner who rounds as the question asks is refused. | `js/engine/grade.js` `within(value, answer, tol)`. Worst case, problems-3 `items[2].parts[2]`: key 0.00166875, tol 0.00005, accepted set $[0.00161875, 0.00171875]$, printed band $[0.00165, 0.00175]$: 0.00173 is promised and refused. Others: 6.6672 against "$6.667 \pm 0.0005$" (accepted up to 6.66717); $-5.326$ against "$-5.33 \pm 0.005$" (accepted from $-5.3283$). The pattern is the house example in `docs/AUTHORING.md` line 128 ("or 0.1667 ± 0.0005"), so the root is the authoring rule; an inbox bullet is raised. Script: section B, eleven `KNOWN B` lines. | Reword each to name the tolerance, not a band round the rounded figure. Paste-ready lines:
   - problems-1 `items[2].parts[3]`: `Any form equal to $-\tfrac{16}{3}$, or a decimal within 0.005 of it, such as $-5.33$`
   - problems-1 `items[2].parts[4]`: `Any form equal to $\tfrac{7}{3}$, or a decimal within 0.005 of it, such as $2.33$`
   - problems-2 `items[0].parts[3]`: `Any form equal to $\tfrac{20}{3}$, or a decimal within 0.0005 of it, such as $6.667$`
   - problems-2 `items[1].parts[3]`: `$2\ln 4 \approx 2.77$, or any decimal within 0.005 of $2\ln 4$`
   - problems-2 `items[2].parts[1]`: `Any form equal to $\tfrac{125}{24}$, or a decimal within 0.0005 of it, such as $5.208$`
   - problems-2 `items[2].parts[2]`: `Any form equal to $\tfrac{19}{6}$, or a decimal within 0.0005 of it, such as $3.167$`
   - problems-3 `items[0].parts[3]`: `$\sqrt{99} \approx 9.95$, or any decimal within 0.005 of $\sqrt{99}$`
   - problems-3 `items[2].parts[1]`: `$-0.0452$, or any decimal within 0.00005 of $-0.045229$`
   - problems-3 `items[2].parts[2]`: `$0.0017$, or any decimal within 0.00005 of $0.001669$`
   - problems-3 `items[3].parts[1]`: `$4(1 - e^{-2}) \approx 3.459$, or any decimal within 0.0005 of $4(1 - e^{-2})$`
   - problems-3 `items[3].parts[2]`: `$1 - e^{-2} \approx 0.865$, or any decimal within 0.0005 of $1 - e^{-2}$`

   Basis for each: the band the widget applies.

   Earlier ruling, read after the blind pass: `review-delta-problems-1.3-ab.md` finding 1 raised this class. It fixed the three lines whose refused end sits at the asked precision ("13.84 is accepted too" and its two sisters, which I checked hold) and ruled "No edit" for the five "accepted as" lines, because their refused ends have more places than the part asks for. The same reasoning covers the six "Any form equal to ..., or $x \pm t$" lines. So no fix is needed under that ruling, and the paste-ready lines above are for use only if it is reopened. I list the finding because the line is still not the band, and because the pattern is the example in `docs/AUTHORING.md`.

## Watch list, checked and clean

- **Fundamental theorem hypotheses.** l5 `screens[7]` and the summary state "for any continuous $f$". l7 `screens[2]` states "$f$ continuous on $[a, b]$ and $F' = f$ there". l7 `screens[6]`, homework-2 `items[8]` part (d): the rule is refused across the blow-up of $\tfrac{1}{x^2}$ at 0, with the right reason. The proofs (l5 `screens[6]`, l7 `screens[8]`, homework-2 `items[8]` and `items[9]`) use the extreme value theorem, continuity and "zero derivative on an interval means constant" where they are needed.
- **Signed area.** Area is $\int |f|$ throughout; every "area" slip and "signed" slip has the right value.
- **Substitution and parts.** l9 `screens[7]` gives the definite rule with $g'$ continuous and $f$ continuous on the range of $g$. l9 `screens[5]` says the direct substitution needs the inside's derivative "up to a constant". homework-3 `items[9]` derives parts with continuous derivatives and says where each is used.
- **Improper integrals.** Always "integrate to $b$, then let $b \to \infty$". The $p$-test is stated as "exactly when $p > 1$" with the boundary shown. Every limit in the long-form models carries a bound.
- **Numerical rule errors.** "For a smooth $f$, one whose second derivative stays bounded, its error shrinks like $h^2$" (l12 `screens[6]`). Exact for lines. The sign claims (overshoot for $x^2$, $x^3$, $\tfrac1x$; low for $e^{-x^2}$ on $[0, 1]$) hold. The predictions in problems-3 match what the rule really gives: error 0.0293 at $n = 8$ and 0.0073 at $n = 16$ for the signal; 0.00172 at $n = 8$ for $\ln x$.
- **Jensen-type claims.** Stated only for the case that holds: "Because this payoff bends inside the range of prices" (l13 `screens[5]`), "in general is not $g(E[X])$" (summary), convex $100e^{-x}$ and concave $\ln x$ in problems-3 with the inequality the right way round. Monte Carlo agrees.
- **Tails and support.** Every density integrates to 1 on its stated support. problems-3 `items[0]`: tail $\tfrac{1}{1 + m^2}$, median 1, 1% size $\sqrt{99}$. problems-3 `items[1]`: Gamma(2, 1), median 1.678. l12 `screens[8]` says returns are "roughly normal".
- **Conventions.** Actual/365 accrual for sterling (l4). Continuous compounding is said each time. Log return against simple return (l9 `screens[8]`).

## Code widgets

Swept with `docs/reports/integrals-L1-3-test-line-sweep-r3.mjs` through `tools/code-runner.mjs`: the page's own harness and worker grader, Pyodide 0.27.7 from the local CDN. No timing-dependent line.

| widget | line | natural codings submitted | fail test N first |
|---|---|---|---|
| l12 `screens[3]` trapezium | test-1 | starter; `range(n - 1)`; `range(n + 1)`; `range(1, n)` | 4 of 4 |
| | test-3 | guard `n < 2`; ends added inside the inside-point loop; ends added only when `n > 1` | 3 of 3 |
| | test-6 | `left = i * h`; point list from 0; `f(i * h)` and `f((i + 1) * h)` | 3 of 3 |
| l12 `screens[8]` phi, prob_within | test-1 | starter; `/ (2 * pi)`; `sqrt(2) * pi`; no constant | 4 of 4 |
| | test-4 | 0 to `z`; `phi()`; `phi(z)`; starter body | 4 of 4 |
| | error | missing bracket | 1 of 1 |
| homework-3 `items[4]` n_needed | test-1 | starter; one strip short; left rectangles | 3 of 3 |
| | test-3 | returns the $n$ before; doubles after the check; steps by 1 | 3 of 3 |
| | test-4 | starts at 2; doubles before testing; always one doubling | 3 of 3 |
| | test-8 | $T_{2n}$ against $T_n$; estimate against the one before | 2 of 2 |
| | error | missing colon | 1 of 1 |

Every line holds. The obvious wrong programs are all refused: left rectangles, midpoint rule, Jo's short point list, `h = b / n`, Simpson weights; the wrong exponent, a hard-coded `n`, a closed form by `math.erf`; relative error, signed error, successive estimates. A correct each-point-once trapezium passes.

Two notes, neither a finding. `while error > tol` (non-strict) passes all eight tests of `n_needed`; it differs from the specified `< tol` only when a float error equals `tol` exactly. `2 * trapezium(phi, 0, z, n)` is refused at test 4: it is the rule with $2n$ strips, and the question fixes $n$ strips on $[-z, z]$, so the line "Integrate `phi` from `-z` to `z`" is the right advice.

## Empirical checks (concepts script, section D)

Seeded, `numpy.random.default_rng(20261126)`.

| claim | check | result |
|---|---|---|
| l12: 95% of days within $\pm 1.96$ | 4,000,000 normals, s.e. 0.00011 | within 0.0006 of 0.95 |
| l1: chance of 0 to 1 s.d. is 0.3413 | same draws, s.e. 0.00024 | pass |
| l7, l13: uniform call and put worth £2.50, £5 when it pays | 4,000,000 uniforms | pass |
| l13, homework-2, homework-3: triangular call £1.67, struck at 104 £0.36 | sum of two uniforms | pass |
| review-3: call struck at 105 worth £0.625 | 4,000,000 uniforms | pass |
| problems-3: $P(X > 2) = 3e^{-2}$, $E[X] = 2$, $E[100e^{-X}] = 25 > 13.53$ | 4,000,000 gamma draws | pass |
| problems-3: tail 0.2, median 1, 1% size $\sqrt{99}$ | inverse-cdf sample and quadrature | pass |
| problems-3: typical compounded path shrinks, mean stays 1 | 400,000 ten-year paths | median 0.64, mean 1.00 |
| l12: trapezium error quarters on doubling | six integrands, $n = 16$ to 256 | ratios in $[3.9, 4.1]$ |
| l1, l2: left below, right above a rising curve, for every $n$ | $n = 1$ to 399 | pass |
| homework-2: best window $x = 0.680$ | numerical maximisation of $\Phi(2x) - \Phi(x)$ | 0.6798 |
| l9: $\int S'/S$ depends only on the end prices | a path with nine wiggles | pass |

Fluency: 960 items (60 seeded draws for each of 16 families) rederived from the prompt text with SymPy. Every key is an antiderivative of its integrand or equals the definite integral; every wrong form is wrong; every numeric slip equals its named mistake; every accept figure is inside its band.

## Overlap with earlier reads

Read only after the ledger and the findings above were written: `docs/reviews/audit-integrals-1-3.md` (round 1, addendum and fix pass), `docs/reviews/audit-integrals-1-3-r2.md` (round 2 and its fix pass), both ledgers for the three lines of findings 1 to 3, and `review-delta-problems-1.3-ab.md` finding 1. Conceptual findings only.

| | count | which |
|---|---|---|
| this audit only | 3 | findings 1, 2, 3 |
| earlier reads only | 29 | round 1 findings 1 to 14 (14), round 2 findings 1 to 7 and 9 to 11 (10; its finding 8 is round 1's 7 again), and the five conceptual findings of the older reviews that round 1 lists. All are fixed in the text read here. I met each fixed wording in the blind read and verified it: for example "the area below the axis ... outweighs the area above", "the signed integral of $f - b$, not the area", "Half of ln 0.5 is −0.34657", "£0.625 exactly", "spreads prices wider", "$-3981.285$", the hypotheses on l9 `screens[7]` |
| both | 1 | finding 4: `review-delta-problems-1.3-ab.md` finding 1, the same defect, already ruled "no edit" for these lines |

Notes.

- Findings 1 and 2 are rows that an earlier ledger marks `correct` where it has them (round 2 ledger line 1849 for l7 `screens[8].prose`). Finding 3's line is marked `correct` in both earlier ledgers (round 1 line 2909, round 2 line 3041). None of the three came from a fix pass: all three lines predate round 1.
- New `wrong` that no earlier read found: **2**, findings 1 and 2, both minor. Both are lesson pointers, not mathematics, figures, keys or slips. Whether a wrong pointer counts against the convergence rule is for the main session to rule. On the content that the rule was written for (definitions, theorems, methods, conventions, graded answers, printed figures), this round found no new `wrong`.

## Engine notes sent to the inbox

Two bullets under "Raised later (audit integrals):" in `docs/BACKLOG-INBOX.md`: a validator warning on relative lesson pointers ("last lesson", "next lesson"), which no tool can check against `course.json` as they stand; and the "$x \pm t$" accept pattern, whose example in `docs/AUTHORING.md` prints a band the widget does not apply.

## Tool runs

| run | result |
|---|---|
| `node tools/validate.mjs` | 0 errors |
| `node tools/run-number-scripts.mjs --only integrals` (venv Python) | 5 of 5 passed |
| `node tools/grade-all.mjs --file` (26 files) `--code --local-cdn` | 409 widgets, 3 Python code widgets, 0 failures |
| `docs/reports/integrals-L1-3-concepts-r3.py` | exit 1: 6430 checks, 14 fail, and all 14 are findings 1 to 4 (1 + 1 + 1 + 11). With `--allow-known`: exit 0 |
| `docs/reports/integrals-L1-3-test-line-sweep-r3.mjs <pkgs>` | exit 0 |

The venv has newer NumPy, SciPy and SymPy than CI's pins. No figure depends on the version. No playthrough was run, as the common rules say.

## Fix pass

Opus fixer, on `claude/sleepy-heisenberg-bhwkqw` at `0ea4d7b4`. No key, tolerance, slip value or hidden test changed.

1. **Fixed.** l4 `screens[7].explain` now ends "the same squeeze as in lesson 2." Basis: `course.json` level 1 order is l1, l2, l3, l4; l2 `screens[7]` line d5 is the squeeze $L_n \le A \le R_n$; l3 has no squeeze, sandwich or bound between sums (searched).
2. **Fixed.** l7 `screens[8].prose` now reads "In lesson 5, for a continuous $f$, ...". Basis: level 2 order is l5, l6, l7; l5 `screens[6]` proves and `screens[7]` states $\frac{d}{dx}\int_a^x f = f$ for continuous $f$; l6 has no $A(x)$ (searched).
3. **Fixed.** l10 `quiz[3]` `byKey.no-integral` now reads "You evaluated $x\ln x$ alone. The antiderivative is $x\ln x - x$, so take off $\big[x\big]_1^e = e - 1$ as well." Basis: $\big[x\ln x\big]_1^e = e$ (the slip 2.7183), and $e - (e - 1) = 1$, the key; subtracting "the $-x$ part" literally gives $2e - 1 \approx 4.437$.
4. **Fixed differently.** The eleven lines now state the grader's own band: "a decimal within $t$ of" the exact value (written as the fraction, $2\ln 4$, $\sqrt{99}$, $4(1 - e^{-2})$, $1 - e^{-2}$), plus the rounded figure as an example. Two differ from the paste: problems-3 `items[2].parts[1]` names the exact value $(1.5\ln 1.5 - 1.5) - (0.5\ln 0.5 - 0.5)$, and `parts[2]` names $0.0267 / 16 = 0.00166875$, because the pasted centres $-0.045229$ and $0.001669$ are rounded, so their far band edges ($-0.045279$, $0.001719$) are refused. Basis: `grade.js` `within` accepts $|v - \text{answer}| \le t + 10^{-9}$, and every key equals its named exact value to $10^{-12}$. Probe through the real `numGrade` (`scratchpad/fix-int13r3/probe.mjs`): for all eleven, the example figure and exact $\pm 0.999999t$ are accepted and exact $\pm 1.02t$ refused. This reopens the "no edit" ruling of `review-delta-problems-1.3-ab.md` finding 1 for these lines, as the orchestrator asked; the `docs/AUTHORING.md` example is engine-side and left to the inbox bullet.

Script: `docs/reports/integrals-L1-3-concepts-r3.py` exits 0 without `--allow-known` (6419 checks; the eleven band checks no longer match, and section B gains a check that each "within $t$ of" line states the widget's own `tol.abs`). No check re-pointed.

| gate | result |
|---|---|
| `node tools/validate.mjs` | 0 errors |
| `voice-scan.py 35` on the six edited files | 0 and 0 |
| concepts scripts r1, r2, r3 | exit 0 each (r3 without `--allow-known`) |
| test-line sweeps r1, 2, r2, r3 | exit 0 each |
| `run-number-scripts.mjs --only integrals` | 5 of 5 passed |
| `grade-all.mjs --code --file` (six files) | 90 widgets, 0 failures |
| playthrough l4, l7, l10, problems-1 to -3, desktop and `--mobile` | all passed |

## Fix-pass read

Fresh reader, blind to this file until the rows below were fixed. Read `git show 3eb0f5ec -- app/content/courses` (six files, 14 changed strings) at `cf2bfdbe`. Script: `docs/reports/integrals-L1-3-r3-fixread.mjs` (run from the repo root; loads the real `app/js/engine/grade.js` and calls `numGrade`, which is what `widgets/numeric.js` `grade()` calls); exit 0.

| # | file | JSON path | claim | verdict | basis |
|---|---|---|---|---|---|
| 1 | l4-accumulating-a-rate | `screens[7].explain.text` | "the same squeeze as in lesson 2" | correct | `course.json` level 1 order l1, l2, l3, l4, so lesson 2 is l2-thinner, which traps the area ($L_n \le A \le R_n$) between sums that converge and calls it the squeeze; l3 has no squeeze (searched), so the old "last lesson" was false. The app numbers lessons course-wide (`screens/course.js` line 111, `screens/today.js` line 202), so the learner sees l2 as "Lesson 2". |
| 2 | l7-evaluating | `screens[8].prose` | "In lesson 5, for a continuous $f$, $A(x) = \int_a^x f(t)\,dt$ had $A' = f$" | correct | Level 2 order l5, l6, l7; l5-area-undoes-slope proves "$A'(x) = f(x)$ for any continuous $f$" with a fixed start $a$. Course-wide count makes it "Lesson 5". The rest of the derivation ($F - A$ has zero derivative, $C = F(a)$) is unchanged and still follows. |
| 3 | l10-undo-product | `quiz[3].feedback.byKey.no-integral` | "You evaluated $x\ln x$ alone. The antiderivative is $x\ln x - x$, so take off $[x]_1^e = e - 1$ as well." | correct | $[x\ln x]_1^e = e \cdot 1 - 0 = e \approx 2.7183$, the slip value; $[x]_1^e = e - 1$; $e - (e - 1) = 1$, the key. Second way: midpoint sum of $\ln x$ on $[1, e]$ with $2 \times 10^6$ strips gives 1.0000000000. Typed 2.7183 and 2.718 route to `no-integral`, 1 grades correct, 0 routes to `top-only`. |
| 4 | problems-1 | `items[2].parts[3].widget.accept` | $-\tfrac{16}{3}$, decimal within 0.005, such as $-5.33$ | correct | $\tfrac{8}{3} - 8 = -5.3333$; `tol.abs` 0.005; $-5.33$ is 0.0033 off; `-16/3` accepted. |
| 5 | problems-1 | `items[2].parts[4].widget.accept` | $\tfrac{7}{3}$, within 0.005, such as $2.33$ | correct | $-3 - (-\tfrac{16}{3}) = 2.3333$; tol 0.005; 2.33 is 0.0033 off; `7/3` accepted. |
| 6 | problems-2 | `items[0].parts[3].widget.accept` | $\tfrac{20}{3}$, within 0.0005, such as $6.667$ | correct | $\tfrac{8}{3} - 12 + 16 = 6.66667$; tol 0.0005; 6.667 is 0.00033 off; `20/3` accepted. |
| 7 | problems-2 | `items[1].parts[3].widget.accept` | $2\ln 4 \approx 2.77$, or any decimal within 0.005 of $2\ln 4$ | correct | $16e^{-0.5t} = 4$ gives $t = 2\ln 4 = 2.772589$; tol 0.005; 2.77 is 0.0026 off. |
| 8 | problems-2 | `items[2].parts[1].widget.accept` | $\tfrac{125}{24}$, within 0.0005, such as $5.208$ | correct | $[\tfrac{x^2}{2} + 3x - \tfrac{2x^3}{3}]_{-1}^{1.5} = 3.375 + \tfrac{11}{6} = 5.208333$; tol 0.0005; 5.208 is 0.00033 off; `125/24` accepted. |
| 9 | problems-2 | `items[2].parts[2].widget.accept` | $\tfrac{19}{6}$, within 0.0005, such as $3.167$ | correct | $[\tfrac{2x^3}{3} - \tfrac{x^2}{2} - 3x]_{-2}^{-1} = \tfrac{11}{6} + \tfrac{4}{3} = 3.166667$; tol 0.0005; 3.167 is 0.00033 off; `19/6` accepted. |
| 10 | problems-3 | `items[0].parts[3].widget.accept` | $\sqrt{99} \approx 9.95$, or any decimal within 0.005 of $\sqrt{99}$ | correct | $1 + q^2 = 100$, $q = \sqrt{99} = 9.949874$; tol 0.005; 9.95 is 0.00013 off; the `drop-one` band (10 ± 0.001) is 0.05 away. |
| 11 | problems-3 | `items[2].parts[1].widget.accept` | $-0.0452$, or within 0.00005 of $(1.5\ln 1.5 - 1.5) - (0.5\ln 0.5 - 0.5)$ | correct | The expression is $-0.04522875$, equal to the key to $10^{-12}$; tol 0.00005; $-0.0452$ is 0.000029 off. |
| 12 | problems-3 | `items[2].parts[2].widget.accept` | $0.0017$, or within 0.00005 of $0.0267 / 16 = 0.00166875$ | correct | $0.0267 / 16 = 0.00166875$ exactly, the key; tol 0.00005; 0.0017 is 0.000031 off. The only terminating centre, so the only one with decimals on the band edge: 0.00171875 and 0.00161875 are both accepted, as "within" promises. The unrounded route ($0.026692 / 16 = 0.001668$) is accepted too. |
| 13 | problems-3 | `items[3].parts[1].widget.accept` | $4(1 - e^{-2}) \approx 3.459$, or within 0.0005 of $4(1 - e^{-2})$ | correct | $[-4e^{-t^2/8}]_0^4 = 4 - 4e^{-2} = 3.458659$; tol 0.0005; 3.459 is 0.00034 off. |
| 14 | problems-3 | `items[3].parts[2].widget.accept` | $1 - e^{-2} \approx 0.865$, or within 0.0005 of $1 - e^{-2}$ | correct | $3.458659 / 4 = 0.864665$; tol 0.0005; 0.865 is 0.00034 off. |

Counts: 14 rows; 14 correct, 0 wrong, 0 imprecise, 0 misleading, 0 unverified.

Rows 4 to 14, the promise against the grader. `within` accepts $|v - \text{answer}| \le t + 10^{-9}$. For each item the script recomputes the exact value from the question (not from the stored key), then checks: key equals it to $10^{-12}$; the stated $t$ is the item's `tol.abs`; the example figure grades correct; decimals at exact $\pm (t - 2 \times 10^{-9})$ and $\pm 0.5t$ grade correct and at exact $\pm (t + 2 \times 10^{-9})$ and $\pm 2t$ are refused; a sweep of 4,000 random seven-place decimals across exact $\pm 3t$ agrees with $|x - \text{exact}| \le t$ every time; and no `wrong[]` band reaches the promised band. All pass for all eleven. Ten centres are irrational or recurring, so no typed decimal can sit on an edge; row 12 covers the eleventh.

One note, not a finding and not from this diff: the numeric field parses only decimals, fractions and mixed numbers, so `2ln4`, `sqrt(99)` and `4(1-e^-2)` cannot be submitted at all (`parseNum` returns NaN, so the field is not ready). Rows 7, 10, 13 and 14 name the closed form only as the centre of the decimal band, and each question asks for a decimal, so nothing promised is refused. "Any form equal to" in rows 4 to 6, 8 and 9 is older wording and holds for fractions and mixed numbers.
