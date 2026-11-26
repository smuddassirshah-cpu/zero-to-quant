# Blind concept audit: pdes problems-1 to problems-3

Scope: `app/content/courses/pdes/problems-1.json`, `problems-2.json`, `problems-3.json` at commit bea50a86 (10 problems, 42 chained parts; no hints, `why` lines or code widgets in these files). Stage 3, full ledger. Read blind: no earlier review, audit or author report was opened until the ledger and the findings below were written.

Ledger: `docs/reports/audit-pdes-problems-1-3-ledger.md`, 313 rows: 307 correct, 6 imprecise, 0 wrong, 0 misleading, 0 unverified. The six imprecise rows belong to the two findings below.

Script: `docs/reports/pdes-problems-concepts.py`, 369 checks, exit 0. It recomputes every key, every slip value and every stated intermediate number from the problem data alone, checks that each answer typed to the asked rounding (and from the carried rounded inputs) is accepted, and that every slip is clear of its key. Closed forms by sympy (step solution, drifted kernel, trial solutions, Fourier coefficients), finite differences by NumPy (explicit rod runs, fine-grid tent, an own Crank-Nicolson pricer that reproduces £12.9963192 and £12.9975576 to seven decimals), Monte Carlo and exact binomials for the walk and Feynman-Kac claims.

## What was checked and holds

- Heat equation set (problems-1): $D = \Delta x^2/(2\Delta t)$, kernel variance $2Dt$, the step solution $30 + 60\Phi(x/\sqrt{2Dt})$, the $\sqrt t$ motion of a level, steady lines with held ends, the bound $\lambda \le \tfrac12$ (75 steps; 74 give 0.5068), the three explicit steps, and convergence of the grid to the line at $\lambda = \tfrac12$.
- Separation and Fourier set (problems-2): $\lambda_k = (k\pi/L)^2$, $b_1 = 48/\pi^2$, $b_3 = -0.5404$, the two-term centre value against a fine-grid run, $b_k$ for $e^x$ by quadrature for $k = 1$ to 6, the midpoint $\cosh\pi$ at the jump, $\sum 1/(1+k^2) = (\pi\coth\pi - 1)/2$ against a direct sum, and the grid mode factor against a run of the scheme.
- Pricing set (problems-3): the lesson 10 lemma by quadrature, $C = K(2\Phi(\sqrt{\tau/2}) - 1)$ against Black-Scholes at $r = 0$, the implied volatility 17.38% (reprices to £9.598), the log contract $e^{-rT}(x + (r - \tfrac12\sigma^2)T)$ three ways (formula, antithetic Euler Monte Carlo $-27.97$, explicit solve of the scaled equation $-27.95$), $\Phi(d_2) = 0.4665$ against Monte Carlo 0.4664, signs and the $\tau = \tfrac12\sigma^2(T - t)$ clock, the Crank-Nicolson constants, the "about 1% higher" and "about $253 \times 10^{-6}$" remarks (own runs: 1.1% to 1.3%, and 253.1; observed order 1.98), and the $1/\sqrt n$ comparison.
- Every chained part uses the carried value, and the carried rounded value lands inside the tolerance in every part.

## Findings

1. problems-1.json | items/3 (`p-drift-walk`) /prose, and parts/2/question and explain | imprecise, minor (tagged serious while blind; lowered after the overlap read, see below) | The prose models the walk with $q = 0.6$ by $u_t + cu_x = Du_{xx}$ "with $D = \Delta x^2/(2\Delta t) = 1.25$". That value is right only to leading order (or as $q \to \tfrac12$). This walk's variance per step is $4q(1-q)\Delta x^2 = 0.0024$, so its variance per unit time is 2.4, not $2D = 2.5$: its diffusion coefficient is 1.2. A learner carries away that a bias leaves the spread of a walk unchanged. Part 3's chance, 0.0899, is the model's; the walk the prose describes gives 0.077. | Evidence: exact binomial and Monte Carlo in the script (variance at $t = 0.32$: 0.7680 against the model's 0.8; $P(\text{below }2) = 0.0774$ against 0.0899). Derivation: $\operatorname{Var}(\text{step}) = \Delta x^2 - ((2q-1)\Delta x)^2$; equivalently, carrying the Taylor expansion of $u(x, t + \Delta t) = q\,u(x - \Delta x, t) + (1-q)\,u(x + \Delta x, t)$ consistently to second order gives $D = \Delta x^2/(2\Delta t) - c^2\Delta t/2 = 1.25 - 0.05 = 1.2$. The same set's own check in `p-tick-spread` part 2 ("600 steps of variance 0.16 each") fails if a learner tries it here. The questions say "the model", so every key is right as worded and no key changes. The source is lesson 2's rule for the biased coin, outside this audit's scope. | Fix: append to the prose of `p-drift-walk`: "The model keeps the leading terms only. The walk's own variance grows at $4q(1-q)\Delta x^2/\Delta t = 2.4$ a unit of time, a little under $2D = 2.5$." Optionally append to parts/2/explain/text: "The walk itself has variance $2.4t = 0.768$ here, so its own chance is a little lower." (Exact binomial 0.0774; a normal with variance 0.768 gives 0.0855.)

2. problems-1.json | items/0 (`p-tick-spread`) /prose and parts/0 (question, slip `no-half`) | imprecise, minor | The item asks for "the diffusion coefficient $D$" of "the heat equation" without writing the equation. The key 0.8 assumes the course form $u_t = Du_{xx}$. Under the equally standard form $u_t = \tfrac12\sigma^2u_{xx}$ (variance $\sigma^2t$) the coefficient is $\Delta x^2/\Delta t = 1.6$, which is the `no-half` slip. Every other problem in the set writes its equation. | Basis: Strauss 2.4 writes $u_t = ku_{xx}$; Shreve and most finance texts write the half. Part 2 does fix the convention ("variance $2Dt$"), but only after part 1 is graded. | Fix: in the prose replace "We model the spread of its moves with the heat equation." with "We model the spread of its moves with the heat equation $u_t = Du_{xx}$."

No `wrong` and no `misleading` finding.

## Notes that are not findings

- `p-tick-spread` part 3: the kernel gives 0.1258; the lattice walk itself gives 0.1308 (exact binomial, moves come in steps of 0.8 pence after an even count). The item asks for the model's chance, so the key stands.
- `p-grid-modes` part 4: the carried 0.298 gives 1.06% and the unrounded factor 1.13%. Both type as 1.1 and both are inside the tolerance.
- `p-grid-budget` part 3: the "limit" of the grids is the closed form to about $10^{-10}$ (lesson 12 quiz); a Richardson guess from 1,200 and 2,400 intervals sits $1.2 \times 10^{-6}$ under it because the order is 1.98, not 2. The content's 253 is measured against the true limit and is right.

## Checks run

- Validator (`node tools/validate.mjs`): 0 errors.
- Number scripts (`node tools/run-number-scripts.mjs --only pdes`, venv Python, newer than CI's pins; no figure depends on a version): 4 of 4 passed.
- `node tools/grade-all.mjs --file` on each file with the local CDN: 17, 13 and 12 widgets, 0 failures.
- `docs/reports/pdes-problems-concepts.py`: 369 checks, exit 0.
- No playthrough (auditor rules).

## Overlap with earlier reads

Opened only after the ledger and the findings above were written: `docs/reviews/review-problems-pdes-1-3.md` (second read and fix pass), `docs/reviews/review-delta-ag-pdes.md` (delta read of the re-authored level 3 and fix pass), `docs/reports/problems-pdes.md`, and the pdes lines of `audit-pdes-1-3.md`, `audit-delta-2026-11-26-3.md` and `concept-audit-log.md` (the delta audit excluded the problem sets). Conceptual and numerical findings only; reuse, continuity and engine findings are not counted.

| | count | which |
|---|---|---|
| this audit only | 1 | finding 2 (`p-tick-spread`: equation form not stated) |
| both | 1 | finding 1 (`p-drift-walk`: the model's $2Dt$ against the walk's $2.4t$) = review-problems finding 5 and review-delta-ag finding 5 |
| earlier reads only | 7 | review-problems 1 (wrong, $50e^{-0.015}$), 2, 3, 4 (carried rounding); review-delta-ag 1 (risk-neutral chance), 2 (order-2 predictions printed as facts), 7 (band edge) |

New `wrong` from this audit: 0.

All seven earlier-only findings were fixed or made moot by re-authoring before this read, so they were not present to find; the ledger rows for the fixed text (2.2057 and 2.2056, "risk-neutral chance", "a prediction from the two coarser runs", the 0.4665 band) are `correct`. On finding 1: the earlier fix passes reworded the prose and parts 3 and 4 to "the model", which makes each sentence true, and `homework-1` `h-derive-lazy-walk` states the gap ($c^2\Delta t\,t$ below $2Dt$). What is left is that this item gives $D = 1.25$ for a walk whose own coefficient is 1.2 and never says so. Blind, I tagged that serious; given the deliberate wording and the homework, the residual is minor, and the one-sentence fix above closes it. `p-grid-budget` has been re-authored again since `review-delta-ag-pdes` (its keys are now 22.29, 557.28, 247.68 and 5.0625), so its twelve part rows here are a first concept read of that text: all correct.

## Fix pass

Opus fixer, from ba3359b4. Both findings re-derived before editing; no key, slip or test changed.

1. Fixed (`p-drift-walk` prose and part 3 explain, the auditor's sentences). Basis: a step is $+0.05$ with chance 0.6 and $-0.05$ with chance 0.4, so its mean is 0.01 and its variance $0.0025 - 0.0001 = 0.0024$. That is $2.4$ a unit of time ($D_{\text{walk}} = 1.2$, not 1.25). Exact Bin(320, 0.6) at $t = 0.32$: variance 0.7680, $P(\text{below } 2) = 0.0774$; a normal with variance 0.768 gives 0.0855; the model gives 0.0899. So "a little lower" holds both ways. Keys stay the model's, as worded.
2. Fixed (`p-tick-spread` prose now names $u_t = Du_{xx}$). Basis: the course defines $D$ as the coefficient in $u_t = Du_{xx}$ (lesson 2 summary, $D = \Delta x^2/(2\Delta t)$, variance $2Dt$), which gives 0.8. In the diffusion-process convention $u_t = \tfrac12\sigma^2u_{xx}$ the name "diffusion coefficient" usually goes to $\sigma^2 = \Delta x^2/\Delta t = 1.6$ (the `no-half` slip), so naming the equation removes the ambiguity. Its feedback text stays right under the stated form.

Gates: validator 0 errors; voice scan 35 on problems-1 0 and 0; `pdes-problems-concepts.py` 369 checks, exit 0 (no check encodes the edited text); number scripts `--only pdes` 4 of 4; `grade-all.mjs --file problems-1.json` 17 widgets, 0 failures; playthrough `--problems pdes/problems-1` green desktop and `--mobile`.
