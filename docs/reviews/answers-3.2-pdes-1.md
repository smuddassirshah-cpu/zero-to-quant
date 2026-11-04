# Answer check, pdes level 1 (3.2)

Independent recomputation of every keyed answer, tolerance, slip value, stated number and code test in `app/content/courses/pdes/` for `l1-equations-in-two-variables`, `l2-heat-equation`, `l3-heat-kernel`, `l4-boundary-conditions`, `review-1` and `homework-1`. Each value was worked from the question text alone. The author's scripts and `docs/reports/pdes-1.md` were not read. Scripts are in the scratchpad folder `ac-pdes1` (`calc.py`, `code_check.py`, `scan.py`, `gen.py`).

Second routes used:

- SymPy: residuals of every candidate solution in l1 (six candidates, transport with speeds 2 and 3), the heat kernel, the bump formula `e^{-x^2/(1+4t)}/sqrt(1+4t)`, the general Gaussian `a/sqrt(a^2+2Dt)`, the step solution `erf(x/sqrt(4Dt))/2`, the drift change of variable `u(x-ct,t)`, and `u_t/u` for the kernel.
- SciPy quadrature of the heat kernel against the step, the bump and the Gaussian start (l3, review and homework values), and of the energy `E(t)` in l4.
- Exact binomial rows for the walk (variance after 400 steps is 4.000000, `P(S_100 = 0) = 0.0795892`), and a finite-difference rod (Dirichlet, 200 intervals) against the l4 Fourier series (they agree to 1e-5 at the middle).
- Black-Scholes closed form with a finite-difference check of the PDE residual (below 4e-6), for the £10.45, £1.18, £6.89 and put and call boundary values.
- The l4 explicit scheme run in CPython for 20,000 steps (Dirichlet index 15 gives 29.000000000, Neumann deviation 3.9e-14, slowest-mode factor 1.9e-14).
- Every code solution run in CPython with NumPy under the engine's rules (prelude first, then the solution, `setup` in the shared namespace, `isclose` with the item's `rel` and `abs`, `raises` by class name). Starters run the same way.
- A structural scan of all 76 widgets: wrong values inside the answer tolerance, answer inside a wrong tolerance, wrong values overlapping each other, `byKey` keys naming nothing, wrong ids without feedback text, choice and multi correct counts, order ids against lines, table cell ids against `byKey`.

**Summary.** All 76 widgets recompute (41 numeric, 19 choice, 3 table with 15 editable cells, 5 code with 36 hidden tests, 3 order, 2 multi, 1 expression, 1 slider, 1 longform; 89 slip values). Every key is right. Every code solution passes all its tests and examples, and every starter fails its item (the l2 starter passes 2 of 7 trivial tests, which still fails the item). No choice or multi distractor is also correct, and no `same` group is unsafe. Three feedback or content defects need a fix (errors 1 to 3), five items need a decision or a small edit (warnings 4 to 8), and eight are notes (9 to 16). No stated number in prose or an explanation is wrong, except that the l4 screen 0 slider cannot show the 35 its explanation quotes (warning 4).

## Widgets checked

Numeric rows give the key and tolerance, then my value and my value for each named slip. `ok` means my value lies inside the key's tolerance and each slip value lies inside its stated value's tolerance.

| File | Screen or item | Key | My value | Verdict |
|---|---|---|---|---|
| l1 | screen[0] | a: price falls, slice bends more | V(100): 10.4506 at t=0, 1.1785 at t=0.98; kink sharpens; caption 10.45 and 1.18 match | ok |
| l1 | screen[1] | all: every point | u_t - u_xx = 0 symbolically; both -0.367879 at (pi/2, 1) | ok |
| l1 | screen[2] | numeric 3 tol {"abs": 0} | 3 (slips: first 1; added 4) | ok |
| l1 | screen[3] | a: e^{-4t} sin 2x | residuals (sympy): a 0, b 3e^-t sin2x, c 2e^-2t sin2x, d -3e^-4t sin x | ok |
| l1 | screen[4] | numeric 0.3679 tol {"abs": 0.0005} | 0.367879 (slips: unmoved 0.00012341; speed 0.0183156) | ok |
| l1 | screen[5] | table: 0 parabolic, 16 hyperbolic, -4 elliptic; byKey r1c1, r1c2, r2c1 | 0 parabolic, 16 hyperbolic, -4 elliptic; byKey texts match the cells | ok |
| l1 | screen[6] | lin: linear | Linear (V, V_S, V_SS appear to the first power with S-dependent coefficients) | ok; key longest option (note 12) |
| l1 | screen[7] | hyp: hyperbolic | disc -4x = +4 at x=-1: hyperbolic; elliptic x>0 | ok |
| l1 | screen[8] | code: classify, heat_residual; 10 tests | solution passes 10/10 and the example; starter passes 0/10; 1.386870 = 3e^-0.2 sin 0.6 = 1.3868705 (inside 1e-5); -1, 4, 0 verified by hand | ok |
| l1 | screen[9] | par: parabolic | 4 - 4 = 0: parabolic | ok |
| l1 | screen[10] | smooth: smooth, one condition at expiry | V(100, tau=0.5) = 6.8887 (prose 6.89); no corner; parabolic with A = S^2 sigma^2/2, B = C = 0 | ok; key longest option (note 12) |
| l1 | quiz[0] q-residual | numeric -1 tol {"abs": 0.001} | -1 (slips: only-tc 0; reversed 1) | ok |
| l1 | quiz[1] q-transport | numeric 0.0183 tol {"abs": 0.0005} | 0.0183156 (slips: speed2 0.367879) | ok |
| l1 | quiz[2] q-tricomi | hyp: hyperbolic | C = -1, disc = 4: hyperbolic | ok |
| l1 | quiz[3] q-order | o4: linear, order 4 | order 4, linear | ok |
| l2 | screen[0] | numeric 2 tol {"abs": 0.05} | 2 (slips: linear 4; three 3) | ok; wrong "three" feedback does not describe the slip (note 9) |
| l2 | screen[1] | table: 0.5, 0.5 / 0.25, 0.5, 0.25 | binomial rows 1/2,1/2 and 1/4,1/2,1/4 | ok |
| l2 | screen[2] | order a1..a6; same [a2, a3]; distractors d1, d2 | a1..a6 reproduces u_t = dx^2/(2dt) u_xx; a2 and a3 independent (a4 needs a3 only); d1 false (the dx^2 terms add), d2 gives D = dx/2 -> 0 | ok |
| l2 | screen[3] | numeric 1 tol {"abs": 0.001} | 1 (slips: forgot-half 2; dx2 0.01; speed 20) | ok |
| l2 | screen[4] | numeric 4 tol {"abs": 0.01} | 4 (slips: steps 400; sizes 40; dt 2) | ok |
| l2 | screen[5] | expr: -1/(2t) + x^2/(4Dt^2) | sympy: u_t/u = (x^2 - 2Dt)/(4Dt^2), equal to the key; kernel residual 0; wrong sign and nolog differ from the key and match their slips | ok (note 14) |
| l2 | screen[6] | numeric 0.0796 tol {"abs": 0.0003} | 0.0795892 (slips: density 0.0398942) | ok |
| l2 | screen[7] | numeric 2 tol {"abs": 0.005} | 2 (slips: bias 0.1; speed 20; q 11) | ok |
| l2 | screen[8] | code: diffusion_coefficient, walk_density; 7 tests | solution passes 7/7; starter passes 2/7 (sum 1 and length), so the item fails; centre 0.079589, variance 30 verified | ok |
| l2 | screen[9] | numeric 2 tol {"abs": 0.001} | 2 (slips: forgot-half 4; dx2 0.04) | ok |
| l2 | screen[10] | numeric 0.1 tol {"abs": 0.0005} | 0.1 (slips: sigma-t 0.05; variance 0.01) | ok |
| l2 | quiz[0] q-phi | numeric 0.242 tol {"abs": 0.0005} | 0.241971 (slips: peak 0.398942; cdf 0.841345) | ok |
| l2 | quiz[1] q-three-steps | numeric 0.375 tol {"abs": 0.001} | 0.375 (slips: two-step 0.25; corner 0.125) | ok |
| l2 | quiz[2] q-even | even: only even sites, cell 2 wide | 0.0796 = 2 x 0.0399; parity argument right; distractors wrong as stated | ok; key longer than distractors (note 12) |
| l2 | quiz[3] q-d-small | numeric 0.005 tol {"abs": 0.0001} | 0.005 (slips: forgot-half 0.01; dx 0.5) | ok |
| l3 | screen[0] | slider t = 4, tol 0.15, wrong [1.7, 2.4] | peak 1/sqrt(4 pi t): 0.282095 at t=1, 0.141047 at t=4 (equals hline 0.141047); t=2 gives 0.1995 so the wrong range is the doubling slip | key ok; feedback wording wrong (error 3) |
| l3 | screen[1] | numeric 0.5 tol {"abs": 0.001} | 0.5 (slips: whole 1; zero 0) | ok |
| l3 | screen[2] | numeric 4 tol {"abs": 0.001} | 4 (slips: no-two 2.82843; variance 16; t 8) | ok |
| l3 | screen[3] | numeric 0.8413 tol {"abs": 0.0005} | 0.841345 (slips: jump 0.5; two-sided 0.682689) | ok |
| l3 | screen[4] | numeric 0.4472 tol {"abs": 0.0005} | 0.447214 (slips: unchanged 1; no-root 0.2) | ok |
| l3 | screen[5] | numeric 1.7725 tol {"abs": 0.0005} | 1.77245 (slips: peak 0.333333; kernel-area 1) | ok |
| l3 | screen[6] | sqrt2 | sqrt(2) = 1.414214; 2, 4, 1/2 wrong | ok |
| l3 | screen[7] | numeric 22026.47 tol {"rel": 0.001} | 22026.5 (slips: forwards 4.53999e-05; exponent 10) | ok; wrong tol rel 1e-7 too tight (warning 8) |
| l3 | screen[8] | code: kernel, heat_line; 7 tests | solution passes 7/7; starter 0/7. Quadrature (scipy quad): step(1,.5) 0.841345, bump(0,1) 0.447214, bump(1,1) 0.366148, step(0,2) 0.5, kernel(1,.5,.5) 0.207554, ONE 1 | ok |
| l3 | screen[9] | avg: weighted average, normal weights | kernel is a N(x0, 2Dt) density of area 1 | ok; key about twice distractor length (note 12) |
| l3 | screen[10] | numeric 0.6827 tol {"abs": 0.0005} | 0.682689 (slips: two-sd 0.9545; one-side 0.341345; cdf 0.841345) | ok |
| l3 | quiz[0] q-peak | numeric 0.2821 tol {"abs": 0.0005} | 0.282095 (slips: t1 0.398942; no-root 0.159155) | ok |
| l3 | quiz[1] q-width | numeric 0.7071 tol {"abs": 0.0005} | 0.707107 (slips: variance 0.5; dt 0.25) | ok |
| l3 | quiz[2] q-back | numeric 8103 tol {"rel": 0.001} | 8103.08 (slips: forwards 0.00012341; three 3) | ok; wrong tol rel 1e-5 too tight (warning 8) |
| l3 | quiz[3] q-step-d | numeric 0.9214 tol {"abs": 0.0005} | 0.92135 (slips: no-scale 0.97725; half 0.5) | ok |
| l4 | screen[0] | numeric 35 tol {"abs": 0.5} | 35 (slips: start 100; left 20; right 50) | warning 4: limit 35 ok, readout at slider max is 39.12 |
| l4 | screen[1] | neu: u_x = 0 | no flux = zero slope | ok |
| l4 | screen[2] | numeric 0.5 tol {"abs": 0.01} | 0.5 (slips: right 1; zero 0) | ok |
| l4 | screen[3] | order e1..e6; distractors d1, d2 | energy argument sound in this order; d1 false (E falls), d2 false (needs w = 0 at ends) | ok |
| l4 | screen[4] | table: wave 2, 2; BS 1, 2 | wave: u_tt and u_xx: 2 and 2; BS: V_t and V_SS: 1 and 2 | ok |
| l4 | screen[5] | numeric 95.1229 tol {"abs": 0.001} | 95.1229 (slips: undiscounted 100; zero 0) | ok |
| l4 | screen[6] | terminal: payoff is a terminal condition | amplification 0.1 e^10 = 2202.65 (label), shrink 0.1 e^-10 = 4.54e-6 (explain) | ok; key about 2.3 times distractor length (note 12) |
| l4 | screen[7] | smooth: smoothed at once | series 400/(pi k) e^{-k^2 t} sin kx is the exact solution for u0 = 100, ends 0 (checked by quadrature of coefficients); smooth for t > 0 | ok; key longer (note 12) |
| l4 | screen[8] | code: explicit_step, run; 6 tests | solution passes 6/6; starter 0/6. [0,.4,.2,.4,0]; neumann [.5,.25,0]; index 15 -> 29.000000000 after 20,000 steps (closed form 20 + 30(0.3)); neumann deviation 3.9e-14 (< 1e-9); lam 0.6 raises | ok |
| l4 | screen[9] | fwd: forward from u0, both ends held at 0 | Hadamard: forward is well-posed; back unstable; no ends non-unique; two times over-determined | ok |
| l4 | screen[10] | dir0: V = 0 at 80 and 130 | knock-out value 0 at both barriers; payoff at 130 would be 30 | ok |
| l4 | quiz[0] q-energy | numeric 0.0695 tol {"abs": 5e-05} | 0.0694556 (slips: half 0.5; no-half 0.138911) | ok; key off true value by 4.4e-5 of 5e-5 (note 15) |
| l4 | quiz[1] q-max | between: stays between 20 and 50 | maximum principle | ok |
| l4 | quiz[2] q-bs-count | numeric 3 tol {"abs": 0} | 3 (slips: two 2; four 4) | ok |
| l4 | quiz[3] q-put-half | numeric 97.531 tol {"abs": 0.0005} | 97.531 (slips: year 95.1229; strike 100) | ok |
| review-1 | item[0] r-classify | hyp: hyperbolic | 16 - 12 = 4 > 0 | ok |
| review-1 | item[1] r-decay-rate | numeric 9 tol {"abs": 0} | 9 (slips: freq 3; six 6) | ok |
| review-1 | item[2] r-d-walk | numeric 1.5 tol {"abs": 0.001} | 1.5 (slips: forgot-half 3; dx2 0.09) | ok |
| review-1 | item[3] r-sd-time | numeric 2.4495 tol {"abs": 0.0005} | 2.44949 (slips: variance 6; dt 3) | ok |
| review-1 | item[4] r-width-later | numeric 1.5 tol {"abs": 0.001} | 1.5 (slips: times-t 4.5; same 0.5) | ok |
| review-1 | item[5] r-step-neg | numeric 0.1587 tol {"abs": 0.0005} | 0.158655 (slips: wrong-side 0.841345; zero 0) | ok; repeats l3 s3 (warning 5) |
| review-1 | item[6] r-data | multi: init + ends | initial profile and one condition at each end; final profile and midpoint are not sufficient | ok |
| review-1 | item[7] r-insulated-avg | numeric 1 tol {"abs": 0.01} | 1 (slips: two 2; half 0.5) | ok |
| review-1 | item[8] r-back | numeric 2981 tol {"rel": 0.001} | 2980.96 (slips: forwards 0.000335463; exponent 8) | ok; wrong tol rel 1e-5 too tight (warning 8) |
| homework-1 | item[0] h-profile | code: heat_line_profile; 6 tests | solution passes 6/6; starter 0/6. Values [0.158655, 0.5, 0.691462, 0.841345] = Phi(-1, 0, 0.5, 1); bump D=.5 gives 1/sqrt(3) = 0.57735; total heat sqrt(pi) = 1.772454 | ok; tests repeat l3 cases (note 11) |
| homework-1 | item[1] h-drift | order s1..s5; same [s2, s3]; d1, d2 | sympy: v_t + c v_x - D v_xx = 0 for v = u(x - ct, t); d1 has the wrong sign, d2 is false | ok |
| homework-1 | item[2] h-gauss-general | numeric 0.8165 tol {"abs": 0.0005} | 0.816497 (slips: no-root 0.666667; half 0.707107) | wrong "half": value 0.7071 is 2/sqrt(8) (4Dt for 2Dt), but its feedback says a=1 (1/sqrt(3) = 0.5774); error 1 |
| homework-1 | item[3] h-wellposed | multi: fwd, transport, bs | forward heat, transport with u(x,0) and BS from expiry are well-posed; back and two-time are not | ok; repeats l4 s9 (warning 7) |
| homework-1 | item[4] h-unstable | numeric 0.76 tol {"abs": 0.001} | 0.76 (slips: stable 0.36; one-step -0.2) | ok; uses l4 s8 starting vector (note 10) |
| homework-1 | item[5] h-far-boundary | numeric 202.469 tol {"abs": 0.001} | 202.469 (slips: undiscounted 200; payoff-only 300) | ok; reuses l4 q-put-half 97.5310 (warning 6) |
| homework-1 | item[6] h-colleague | longform, 5 rubric lines of 2 points | D = 0.02; sd 0.2 and 0.4; variances 0.04 and 0.16; dx = 0.02 for dt = 0.01 (0.0004/0.02 = 0.02); lambda <= 1/2; rubric sums to 10 | values ok; model string defect (error 2); note 17 |

## Mismatches

### Errors

1. **`homework-1.json`, item `h-gauss-general`, `feedback.byKey.half` states the wrong slip.** The text says "0.7071 is the value for $a = 1$". For $a = 1$, $D = \tfrac12$, $t = 2$ the formula gives $1/\sqrt{3} = 0.5774$. The value 0.7071 is $2/\sqrt{8}$, from using $4Dt = 4$ in place of $2Dt = 2$. The clause "so the bump is wider and decays less" does not follow either. Key 0.8165 and `no-root` 0.6667 are right. Fix: replace the text with "0.7071 is $2/\\sqrt{8}$: you used $4Dt = 4$ in place of $2Dt = 2$. The kernel's variance is $2Dt$."

2. **`homework-1.json`, item `h-colleague`, `model` holds literal backslash-n sequences, not line breaks.** The string has 0 real newlines and 8 two-character `\n` sequences (the file text reads `\\n\\n`). `prose()` splits on real blank lines, so the model answer renders as one block with the characters `\n\n` visible between the five sections. Fix: in the `model` string replace the four `\\n\\n` (as written in the file) with `\n\n`.

3. **`l3-heat-kernel.json`, screen 0, slider `wrong` `half-t`: the feedback names the wrong slip.** The range 1.7 to 2.4 is the learner who doubles $t$ (the peak at $t = 2$ is 0.1995, not 0.141). Halving $t$ to 0.5 makes the peak rise to 0.399. The text "You halved $t$ to get half the height" is false. Fix: "You doubled $t$ to halve the height. The peak depends on $1/\\sqrt{t}$, so $t$ must quadruple." Optionally rename the id `double-t`, in `wrong` and `byKey` together.

### Warnings

4. **`l4-boundary-conditions.json`, screen 0: the slider never reaches the answer.** Key 35 (the limit) is right, but at the slider maximum $t = 3$ the middle label reads 39.12 (the $k = 1$ mode is still $82.76e^{-3} = 4.12$ high). The explain canvas also sets $t = 3$ beside the text "At the middle it is $20 + 30 \times \tfrac12 = 35$". A learner who reads the label and types 39.1 gets only the generic feedback. Fix: set the control `max` to 6 (the label then reads 35.21) and the explain canvas `params.t` to 6. A `max` of 8 reads 35.03.

5. **`review-1.json`, item `r-step-neg`, repeats `l3-heat-kernel.json` screen 3.** Both use $D = 1$, $t = 0.5$, $|x| = 1$ (width 1), so the answer is $\Phi(\mp 1)$ and the slip value 0.8413 is the lesson's key (DECISIONS "Fresh numbers in reviews and homework"). Fix: use $D = 1$, $t = 1$ (width $\sqrt{2}$), $x = -1$. Prose "$u(x, t) = \Phi(x/\sqrt{2Dt}) = \Phi(x/\sqrt{2})$"; question "What is $u(-1, 1)$? Give 4 decimal places."; `answer` 0.2398 (exact 0.239750), `accept` "0.2398: $\\Phi(-1/\\sqrt{2}) = 1 - 0.7602$"; `wrong` `wrong-side` 0.7602 (exact 0.760250), `zero` 0, and a new `no-scale` 0.1587 ($\\Phi(-1)$, forgot to divide by the width). Update the `byKey` texts and `explain` to match.

6. **`homework-1.json`, item `h-far-boundary`, reuses `l4-boundary-conditions.json` quiz `q-put-half`.** Both discount a £100 strike at 5% for half a year, so $100e^{-0.025} = 97.5310$ is the lesson's answer and appears inside this item's working. Fix: strike £120, $r = 4\%$, $T - t = 0.75$, grid stops at $S = 300$. Boundary value $300 - 120e^{-0.03} = 183.5465$ (strike discounted 116.4535). `answer` 183.5465 with `tol.abs` 0.001; `wrong` `undiscounted` 180, `payoff-only` 300. Update the prose ("strike £120, $r = 4\%$", "with 0.75 years to run"), `accept`, feedback and explain.

7. **`homework-1.json`, item `h-wellposed`, repeats three options of `l4-boundary-conditions.json` screen 9.** The correct "Heat on $[0, \\pi]$ from a given $u_0$ ..." and the distractors "run backwards from a measured profile" and "profile given at both $t = 0$ and $t = 1$" are the lesson's options, with the same `why` lines. The item then tests recall. Fix: keep the transport and Black-Scholes options. Replace `fwd` with "Heat on $[0, 1]$ from a given $u_0$, with both ends insulated" (correct). Replace `back` with "$u_t = -u_{xx}$ on $[0, 1]$ solved forwards from $u_0$ with both ends held at 0" (heat with the sign flipped, unstable: modes grow like $e^{k^2\\pi^2 t}$). Replace `two` with "Heat on $[0, 1]$ from $u_0$ with the temperature at both ends and also at the midpoint for all $t$" (over-determined: most data have no solution). Write fresh `why` lines.

8. **Slip tolerances too tight on three "forwards factor" wrongs.** `l3-heat-kernel.json` screen 7 (`forwards`, value 4.54e-05, `rel` 1e-7; true $e^{-10} = 4.539993\\times 10^{-5}$), `l3-heat-kernel.json` quiz `q-back` (`forwards` 0.000123, `rel` 1e-5; true 0.00012341) and `review-1.json` `r-back` (`forwards` 0.000335, `rel` 1e-5; true 0.00033546). A learner who types the calculator output (4.539993e-05, 0.00012341, 0.00033546) misses the slip and gets the generic line. Only the three-figure value matches. Fix: set each of the three `tol` to `{"rel": 0.01}`. The answers (22026.47, 8103 and 2981, at `rel` 0.001) are fine and do not overlap.

### Notes

9. **`l2-heat-equation.json`, screen 0, `wrong` `three`:** the value 3 is the growth in $n$ from 25 to 100 as a multiple of 25, but the feedback says "a gap of 75", which would give 75. Fix: "You took the rise from 25 to 100 as 3 times 25. Spread depends on the ratio of the step counts, through its square root."

10. **`homework-1.json`, `h-unstable`:** starts from the vector $[0, 0, 1, 0, 0]$ that `l4-boundary-conditions.json` screen 8 uses as its example, and its slip 0.36 is the $\lambda = 0.4$ continuation of that example. Key 0.76 (steps $[0, 0.6, -0.2, 0.6, 0]$ then $[0, -0.24, 0.76, -0.24, 0]$) and the slips (0.36, $-0.2$) are right. A fresh start such as $[0, 1, 0, 0, 0]$ would remove the overlap.

11. **`homework-1.json`, `h-profile` tests:** three hidden cases (step at 1 with $t = 0.5$; bump at 0 and at 1 with $t = 1$) are the l3 screen 8 cases. Values verified (0.841345, 0.447214, 0.366148). Acceptable for a vectorising exercise, but a case with new numbers (for example bump at 2, $t = 0.5$, which is $e^{-4/3}/\\sqrt{3}$) would stop the item testing recall.

12. **Choice keys visibly longer than their distractors** (key length against mean distractor length, characters without `$`): `l1` screen 6 (71 against 42), `l1` screen 10 (81 against 51), `l2` quiz `q-even` (75 against 49), `l3` screen 9 (82 against 41), `l4` screen 6 (108 against 48) and `l4` screen 7 (72 against 42). Suggested keys, with distractors trimmed or padded to match:
    - `l1` screen 6: "Linear: $S$ only weights the terms; $V$ never multiplies itself".
    - `l1` screen 10: "Smooth despite the kink, with one condition at expiry".
    - `l2` `q-even`: "Only even sites are reachable, so each carries a cell 2 wide".
    - `l3` screen 9: "A weighted average of $u_0$ with normal weights at $x_0$".
    - `l4` screen 6: "The payoff is a terminal condition, so forwards is ill-posed".
    - `l4` screen 7: "It is smoothed at once and smooth for every $t > 0$".

13. **`l3-heat-kernel.json`, screen 1, canvas readout:** the area runs `from 0 to 8` while the kernel is centred at $x_0$ up to 3 with width up to 2, so it under-reads by up to 0.006 (at $x_0 = 3$, $t = 2$ it shows 0.9270, true $\Phi(1.5) = 0.9332$). The key (0.5 at $x_0 = 0$) is exact to 4 places. Fix: `to: 30`.

14. **P32-expr-exp (known gap, recorded once).** Level 1 has one expression widget, `l2-heat-equation.json` screen 5. Its key, $-\tfrac{1}{2t} + \tfrac{x^2}{4Dt^2}$, contains no `exp`, so the gap does not reach it. SymPy confirms the forms a learner would type equal the key: `x^2/(4Dt^2)-1/(2t)` (listed), `(x^2-2Dt)/(4Dt^2)`, `\frac{x^2-2Dt}{4Dt^2}` and `x^2/(4*D*t^2)-1/(2*t)`. The two `wrong` expressions differ from the key and match their slips.

15. **`l4-boundary-conditions.json`, `q-energy`:** key 0.0695 with `tol.abs` 5e-05 sits 4.4e-05 from the true 0.069456, so 0.0694 is refused and a hand calculation that gives 0.06945 sits on the edge. Fix: `answer` 0.06946 and `tol.abs` 0.00006, which accepts 0.0694 and 0.0695 and keeps `no-half` (0.1389) clear.

16. **`homework-1.json`, `h-colleague` rubric:** the prompt asks the learner to say how the steps should be chosen ($\Delta x = \sigma\sqrt{\Delta t}$, for example 0.02 for $\Delta t = 0.01$), but no rubric line awards it; only the clause "$\Delta t$ must shrink like $\Delta x^2$" in line 2 touches it. The five lines sum to 10 and every number in the model answer is right ($D = 0.02$, standard deviations 0.2 and 0.4, variances 0.04 and 0.16, $\lambda \le \tfrac12$). Fix: reword rubric line 2 to include "and chooses $\Delta x = \sigma\sqrt{\Delta t}$".

## Fix pass

Every changed number was recomputed by two routes (closed form and a loop or Simpson quadrature, scratchpad `fix-pdes1`). Validator 0 errors; voice scan 0 and 0; playthrough of all four lessons, review-1 and homework-1 passes with and without `--mobile`; screenshots of l4 screen 0 (readout 35.2 at the slider end) and homework item 7 checked.

1. Fixed: `h-gauss-general` `half` feedback now says 0.7071 is $2/\sqrt{8}$ ($4Dt$ for $2Dt$). Value unchanged and right.
2. Fixed: `h-colleague` model holds real blank lines (8 literal `\n` replaced). A scan of every string in the four lessons, review-1 and homework-1 found no other literal `\n`; the only other hit is LaTeX `\ne` in review-1 r-classify, which is intended.
3. Fixed: l3 screen 0 `half-t` renamed `double-t` (in `wrong` and `byKey`); feedback now names the doubling slip. Range 1.7 to 2.4 unchanged (t = 2 gives peak 0.1995).
4. Fixed: l4 screen 0 slider `max` 3 to 6 and the explain canvas `t` to 6; the label reads 35.2 (35.205 computed), inside the key tolerance 0.5.
5. Fixed: `r-step-neg` now $D = 1$, $t = 1$, $x = -1$: answer 0.2398 ($\Phi(-1/\sqrt2)$ = 0.239750 by erf and by quadrature); `wrong-side` 0.7602; `zero` 0; new `no-scale` 0.1587.
6. Fixed: `h-far-boundary` strike £120, $r = 4\%$, $T - t = 0.75$ (t = 0.25): answer 183.5465 (300 - 116.4535, by direct and series exponential); `undiscounted` 180; `payoff-only` 300.
7. Fixed: `h-wellposed` options replaced as proposed (insulated heat on [0, 1], sign-flipped heat, midpoint over-determined), fresh `why` lines, explain reworded.
8. Fixed: `forwards` tol set to `{"rel": 0.01}` in l3 screen 7, l3 `q-back`, review-1 `r-back`.
9. Fixed: l2 screen 0 `three` feedback names the "3 times 25" slip.
10. Fixed: `h-unstable` starts from $[0, 1, 0, 0, 0]$; middle entry after two steps is -0.24 (loop and by hand); `stable` ($\lambda = 0.4$) 0.16; `one-step` 0.6. Explain reworded (value below the start minimum 0).
11. Fixed: `h-profile` tests now use new cases: step at $[-2, -0.5, 0.5, 1.5]$ with $t = 1$ (0.07865, 0.361837, 0.638163, 0.855578, by erf and Simpson) and bump at $[1, 2]$ with $t = 0.5$ (0.41369, 0.152188). Solution passes, starter fails.
12. Fixed: choice keys shortened as suggested and distractors adjusted to similar length in l1 screens 6 and 10, l2 `q-even`, l3 screen 9, l4 screens 6 and 7.
13. Fixed: l3 screen 1 area `to` 8 to 30.
14. No change needed (P32-expr-exp, as instructed).
15. Fixed: `q-energy` answer 0.06946, `tol.abs` 6e-05 (true 0.0694556).
16. Fixed: `h-colleague` rubric line 2 adds "and chooses $\Delta x = \sigma\sqrt{\Delta t}$"; still sums to 10.

Also: one 21-word sentence in l4 screen 4's explanation was split so the voice scan reads 0 over-long sentences (pre-existing).

Disputed: none. Deferred: none.

### Changed keys

- `homework-1.json` `h-far-boundary`: answer 202.469 to 183.5465, `undiscounted` 200 to 180, numbers in prose.
- `homework-1.json` `h-unstable`: answer 0.76 to -0.24, `stable` 0.36 to 0.16, `one-step` -0.2 to 0.6, start vector.
- `homework-1.json` `h-wellposed`: options `fwd`, `back`, `two` replaced (correct set unchanged).
- `homework-1.json` `h-profile`: hidden tests 1 and 2 (calls and expected values).
- `review-1.json` `r-step-neg`: answer 0.1587 to 0.2398, `wrong-side` 0.8413 to 0.7602, new `no-scale` 0.1587, numbers.
- `review-1.json` `r-back`: `forwards` tol.
- `l3-heat-kernel.json` screen 0 slider: `wrong` id `half-t` to `double-t`.
- `l3-heat-kernel.json` screen 7: `forwards` tol.
- `l3-heat-kernel.json` `q-back`: `forwards` tol.
- `l4-boundary-conditions.json` screen 0 slider: control range max 3 to 6.
- `l4-boundary-conditions.json` `q-energy`: answer 0.0695 to 0.06946, tol.abs 5e-05 to 6e-05.
- Option text only (keys unchanged): l1 screens 6 and 10, l2 `q-even`, l3 screen 9, l4 screens 6 and 7.
