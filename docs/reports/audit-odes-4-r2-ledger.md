# Claim ledger: odes level 4, round 2 (blind)

Scope: `l14` to `l18`, `review-4`, `homework-4` in `app/content/courses/odes/`. Stage 1, full depth. Every row was read and judged by hand; none is generated.

Basis keys:
- **BD** = Boyce and DiPrima, *Elementary Differential Equations and Boundary Value Problems*: ch. 6 (6.1 definition and existence, Theorem 6.1.2; 6.2 derivative rule, Theorem 6.2.1 and its corollary; 6.3 shift), ch. 8 (8.1 Euler and its error, 8.3 Runge-Kutta, 8.5 and 8.6 stability and stiffness).
- **HNW** = Hairer, Nørsett and Wanner, *Solving Ordinary Differential Equations I*, II.1 (order conditions, classical RK4), II.3 (global error of order p).
- **HW2** = Hairer and Wanner, *Solving Ordinary Differential Equations II*, IV.2 (stability function; explicit Euler interval (-2, 0); RK4 real interval (-2.785, 0)).
- **BM** = Brigo and Mercurio, *Interest Rate Models*, 3.2.1 (Vasicek: mean of r, integrated rate normal, bond price).
- **CB** = Casella and Berger, *Statistical Inference*, 2.3 (moment generating function).
- **C** = a check in `docs/reports/odes-L4-concepts-r2.py` (CPython 3.13, NumPy 2.2.6, SciPy 1.14.1). "D:" = short derivation here.

Verdict counts are at the foot.

## l14-laplace-transform

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l14 | s0.prose | £1 a year for ever at rate s is worth the area under e^{-st} | correct | D: PV of a continuous flow c(t) is ∫ c e^{-st} dt |
| l14 | s0.widget | £25 at 4%, tol 0.01; slip 0.25 is 1/4 | correct | D: 1/0.04 = 25; C |
| l14 | s0.hints, feedback | ∫ e^{-0.04t} dt = 1/0.04; "rates enter as decimals" | correct | D |
| l14 | s0.explain | a higher rate shrinks the area | correct | D: 1/s falls in s |
| l14 | s1.prose | F(s) = ∫_0^∞ e^{-st} f(t) dt is the Laplace transform | correct | BD 6.1 |
| l14 | s1.widget | L{1} = 1/s; slip s | correct | BD 6.1 example |
| l14 | s1.hints[1..2] | ∫_0^b e^{-st} dt = (1 - e^{-sb})/s; limit 1/s for every s > 0 | correct | D |
| l14 | s1.explain | a perpetuity at rate s is worth 1/s; every PV at a continuous rate is a transform | correct | D, of the cash-flow rate |
| l14 | s2.prose | e^{-st} e^{at} = e^{-(s-a)t}; canvas fixes s = 6% | correct | D; canvas expr exp((a-0.06)x) |
| l14 | s2.options a | L{e^{at}} = 1/(s-a) for s > a | correct | BD 6.1 |
| l14 | s2.options b, c, d whys | sign slip; region dropped; e^{at} is not a constant | correct | D |
| l14 | s2.feedback.c, explain | at s ≤ a the curve never falls and the area is unbounded | correct | D: integrand ≥ 1 |
| l14 | s3.prose | parts with u = t: boundary term 0 at both ends, leaves (1/s)∫ e^{-st} dt | correct | D: [-t e^{-st}/s] vanishes at 0 and ∞ for s > 0 |
| l14 | s3.widget | L{t}(2) = 0.25; slips 0.5 (1/s) and 4 (s²) | correct | D |
| l14 | s3.explain | shaded area equals 0.25 | correct | D: tail beyond 60 negligible |
| l14 | s4.prose | L{t²} = 2/s³ by two rounds of parts; sine and cosine take two rounds | correct | BD 6.1 |
| l14 | s4.prose | signed area of e^{-t} sin 3t is L{sin 3t}(1) | correct | definition |
| l14 | s4.widget rows | 2, 0.3, 0.2 from 2/s³, 3/(s²+9), s/(s²+4) at s = 1 | correct | BD Table 6.2.1; C |
| l14 | s4.feedback r1c2, r2c2 | sine has b on top, cosine has s on top | correct | BD Table 6.2.1 |
| l14 | s5.prose | growing dividend 5/(r - 0.02) = £125 at 6%: Gordon growth | correct | D; continuous-time Gordon, C |
| l14 | s5.options a, b | formula used where the integral diverges; r ≤ g | correct | region of convergence s > a |
| l14 | s5.options d | L{5}·L{e^{0.02t}} at 1% is -£50,000; product of transforms is not the transform of a product | correct | C: 500 × (-100); BD 6.6 (product ↔ convolution) |
| l14 | s5.feedback, explain | at 1% the area has no limit; a negative price is the formula outside its range | correct | D |
| l14 | s6.caption | e^{t²-st} is lowest at t = s/2 then climbs | correct | D: derivative of t² - st |
| l14 | s6.options a | e^{t²} has no transform at any s | correct | BD 6.1 (not of exponential order); D: t² - st > 0 for t > s |
| l14 | s6.options b | e^{5t}: 1/(s-5) for s > 5 | correct | BD 6.1 |
| l14 | s6.options c | t^{10}: 10!/s^{11} for s > 0 | correct | C (numeric transform at s = 2) |
| l14 | s6.options d | sin(t²) is bounded so the integral exists for every s > 0 | correct | D: comparison with e^{-st} |
| l14 | s6.explain | piecewise continuous and of exponential order implies a transform exists | correct | BD Theorem 6.1.2 |
| l14 | s7.lines s1 to s4 | L{f'} = [e^{-st}f]_0^∞ + s∫e^{-st}f = sF - f(0), with e^{-st}f → 0 stated | correct | BD Theorem 6.2.1; hypothesis is on the line |
| l14 | s7.lines d1, feedback | bracket is upper minus lower | correct | D |
| l14 | s7 key | order s1, s2, s3, s4 is the only valid order | correct | each line starts with "=" from the one before |
| l14 | s7.explain | L{f''} = s²F - s f(0) - f'(0) | correct | BD corollary to 6.2.1 |
| l14 | s8.prose | linearity; shift rule L{e^{at}f} = F(s - a) | correct | BD 6.1, 6.3 |
| l14 | s8.canvas rows | table with regions s > 0, s > a | correct | BD Table 6.2.1 |
| l14 | s8.widget | L{e^{-t} cos 2t} = (s+1)/((s+1)²+4); accept expanded form; sign slip | correct | C (numeric transform); (s+1)²+4 = s²+2s+5 |
| l14 | s9.prose | trapezium rule on [0, 50], n strips; guard r ≤ g | correct | method sound for decaying integrands |
| l14 | s9.console | 0.249999994791666...; 125.00000000000001; ValueError text | correct | C: run, every digit |
| l14 | s9.solution | h(Σg - (g0+gn)/2) is the trapezium sum | correct | D |
| l14 | s9.tests, how | 9 tests; tolerances as stated; starter fails | correct | C |
| l14 | s9.feedback.correct | values within 1e-7 of 0.5, 0.25, 0.3 | correct | C: worst 1.6e-8 |
| l14 | s9.explain | accuracy about 1e-8; cut at T = 50 below 1e-18 | correct | C: Euler-Maclaurin h²/12·g'(0); tails ≤ 5e-19 |
| l14 | s10.prose | constant hazard 2% gives density 0.02e^{-0.02t} | correct | D: exponential default time |
| l14 | s10.prose | value is 100·L{density}(0.04) | correct | D: E[100 e^{-0.04τ}] |
| l14 | s10.prose | the MGF is this transform read at -s | correct | CB 2.3: M(θ) = E e^{θT} = L{f}(-θ) |
| l14 | s10.widget | £33.33; slips 50 and 100 | correct | C |
| l14 | s10.feedback, explain | discounting and default add their rates | correct | D: 0.02/(0.04+0.02) |
| l14 | summary.ideas | PV is a transform; table from definition and parts; derivative rule carries starting values | correct | BD 6.1, 6.2 |
| l14 | summary.trap | 1/(s-a) at s ≤ a is meaningless | correct | region of convergence |
| l14 | quiz q-exp | 1/(5-3) = 0.5; slip 0.125 | correct | C |
| l14 | quiz q-second | options and whys for L{f''} | correct | BD corollary to 6.2.1 |
| l14 | quiz q-sine | 3/25 = 0.12; slip 0.16 | correct | C |
| l14 | quiz q-exist | exists exactly for s > 2; whys | correct | D |

## l15-solving-with-laplace

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l15 | s0.prose, states | y' + 2y = 4, y(0) = 0: sY + 2Y = 4/s, Y = 4/(s(s+2)) = 2/s - 2/(s+2), y = 2 - 2e^{-2t} | correct | D: check y' + 2y = 4e^{-2t} + 4 - 4e^{-2t} = 4 |
| l15 | s0.ops rejects | integrating needs y; no product rule for inverting | correct | BD 6.6: product inverts to a convolution |
| l15 | s0.explain | the answer follows the slope field of 4 - 2y | correct | D |
| l15 | s1.prose | the four steps named the Laplace method | correct | BD 6.2 |
| l15 | s1.widget | y(1) = 1.7293; slip 1.2642 = 2 - 2e^{-1} | correct | C |
| l15 | s1.feedback.one | pole at -2 gives e^{-2t} | correct | D |
| l15 | s1.explain | leaves 0 with slope 4, levels at 2 | correct | D: y'(0) = 4, limit 2 |
| l15 | s2.prose | sR - 0.06 = 0.02/s - 0.5R | correct | D |
| l15 | s2.widget | R = (0.06s+0.02)/(s(s+0.5)); accept split form; slip drops r(0) | correct | D; C |
| l15 | s2.feedback.no-start | dropping r(0) solves from a zero rate | correct | D: inverts to 0.04(1 - e^{-0.5t}) |
| l15 | s2.explain | 0.04/s + 0.02/(s+0.5), r = 0.04 + 0.02e^{-0.5t} = θ + (r0-θ)e^{-κt} | correct | C; BM 3.2.1 with σ = 0 |
| l15 | s3.prose | (s²+3s+2)Y = 2/s from rest; poles 0, -1, -2; cover-up rule | correct | D; BD 6.2 |
| l15 | s3.widget | residues 1, -2, 1 | correct | C |
| l15 | s3.explain | y = 1 - 2e^{-t} + e^{-2t}, y(1) = 0.399576 | correct | C |
| l15 | s4.prose | y'' + 2y' + 5y = 0, y(0) = 1, y'(0) = 0 gives (s²+2s+5)Y = s + 2 | correct | D: s²Y - s + 2(sY - 1) + 5Y = 0 |
| l15 | s4.widget | y = e^{-t}(cos 2t + ½ sin 2t); slips cos-only, full-sine | correct | C (solves the equation and both starting values) |
| l15 | s4.caption | real part sets decay, imaginary part sets (angular) frequency | correct | BD 3.3 |
| l15 | s4.explain | y(1) = 0.014164; poles are the eigenvalues | correct | C; D: characteristic roots -1 ± 2i |
| l15 | s5.prose, key | L{y''} = s²Y and L{y'} = sY give Y = 0, y = 0 | correct | D |
| l15 | s5.options b | true answer needs -s y(0) - y'(0) - 2y(0) | correct | D |
| l15 | s5.options c | e^{-t} cos 2t still carries a starting value | correct | D: it has y(0) = 1 |
| l15 | s5.options d | ½e^{-t} sin 2t is the solution from y(0) = 0, y'(0) = 1 | correct | C |
| l15 | s5.explain | dropping the terms solves from rest; here starting values are all the motion | correct | D: homogeneous equation |
| l15 | s6 | 1/(s+1)² inverts to t e^{-t}; slips e^{-t}, e^{-2t}; double root gives (c1 + c2 t)e^{rt} | correct | BD 6.3, 3.4 |
| l15 | s7.prose | the four steps with both derivative rules | correct | BD 6.2 |
| l15 | s7.options | starting values enter at the transform; no constants left to fit | correct | BD 6.2 |
| l15 | s8.prose | simple poles, deg num < deg den: residue num(p)/den'(p), y = Σ res e^{pt} | correct | Heaviside expansion; hypotheses stated |
| l15 | s8.console | (array([-2., -1., 0.]), array([ 1., -2., 1.])); 0.39957640089372803 | correct | C: run, every digit |
| l15 | s8.tests, how | 7 tests; complex residue 0.5 - 0.25j; Vasicek 0.0521306 | correct | C; D: (1+2i)/(4i) |
| l15 | s8.explain | conjugate pair: imaginary parts cancel | correct | real coefficients |
| l15 | s9.prose | PV of r(t) on £1 at flat 5% is R(0.05) | correct | definition |
| l15 | s9.prose, explain | some option prices have closed-form transforms in maturity, inverted numerically | correct | Geman and Yor (1993) Asian options; Carr and Madan (1999) for the Fourier sister |
| l15 | s9.widget | £0.8364; slip 0.8 | correct | C |
| l15 | summary | steps; no constants; pole p gives e^{pt}; complex pair rings; double pole brings t | correct | BD 6.2, 6.3 |
| l15 | summary.trap, formula.note | dropping the terms solves from rest | correct | D |
| l15 | quiz q-sign | Y = 2/(s-3); the three slips | correct | D: option d from sY - 2 - 3/s = 0 |
| l15 | quiz q-cover | 1/3 at s = 1; -1/3 is the residue at -2 | correct | C |
| l15 | quiz q-poles | -2 ± 3i: envelope e^{-2t}, frequency 3; whys | correct | BD 3.3 |
| l15 | quiz q-invert | 3/(s+2) inverts to 3e^{-2t} | correct | BD Table 6.2.1 |

## l16-euler-method

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l16 | s0 | y' = y, h = 0.5: 1 → 1.5 → 2.25; short of e by 0.47 | correct | C |
| l16 | s1.prose | Euler: y_{n+1} = y_n + h f(t_n, y_n) | correct | BD 8.1 |
| l16 | s1.widget, explain | 1.25⁴ = 2.4414; gap 0.47 → 0.28 | correct | C |
| l16 | s2 | h = 1/12 on y' = 0.05y is monthly compounding; 1.051162 against 1.051271 | correct | C; D: (1 + r/m)^m → e^r |
| l16 | s2.feedback | monthly falls short of continuous; one annual step gives 1.05 | correct | D |
| l16 | s3.prose | errors 0.124539, 0.064984, 0.013468 | correct | C |
| l16 | s3.canvas | four points are the errors at 0.1, 0.05, 0.025, 0.0125; reference slope 1 | correct | C |
| l16 | s3.widget | ratio 1.92; slips 4 and 0.52 | correct | C |
| l16 | s3.explain | local error about h²y''/2, 1/h steps, so error ∝ h; fitted slope 0.964; first order | correct | BD 8.1 (local and global truncation error); C |
| l16 | s4.prose | exact r(1) = 5.2131%; each quarterly step adds 0.125(0.04 - r) | correct | C |
| l16 | s4.widget, hints | 5.75%, 5.5313%, 5.3398%, 5.1724%; slips 5% and exact | correct | C |
| l16 | s4.feedback.exact | Euler's four steps undershoot | correct | C: 5.1724 < 5.2131 |
| l16 | s4.explain | monthly 5.2001%, about a third of the error | correct | C: ratio 0.32 |
| l16 | s5.prose | Euler map (x + 0.1y, y - 0.1x); true orbit is the unit circle; Euler spirals out | correct | D: x² + y² conserved by the flow |
| l16 | s5.canvas points | 64 points | correct | C: equal to the taught `euler` to 4 dp |
| l16 | s5.widget | radius (√1.01)^63 = 1.3681; slips 1 and 1.8717; "one turn" | correct | C: 63·atan(0.1) = 6.279 |
| l16 | s5.explain | one step multiplies x² + y² by 1 + h²; each step leaves the circle outside | correct | D: (x+hy)² + (y-hx)² |
| l16 | s6 | y' = -10y, h = 0.25: factor -1.5; 5.0625 at t = 1; true series; e^{-10} = 0.0000454 | correct | C |
| l16 | s6.explain | each step overshoots zero and lands further away | correct | D: factor -1.5 |
| l16 | s7.prose | stable iff abs(1 - hλ) < 1, so h < 2/λ; factor 1 + hμ for eigenvalue μ | correct | HW2 IV.2; BD 8.5 |
| l16 | s7.prose | "At h = 0.05 the factor is 0.5; at h = 0.1 it is 0", stated under the general λ | imprecise | true only for λ = 10, which the sentence does not say; finding 3 |
| l16 | s7.prose | a fast rate beside slower ones makes a system stiff | correct | HW2 IV.1; BD 8.6 |
| l16 | s7.widget | h < 0.2; slip 0.1 | correct | D |
| l16 | s7.feedback.one, explain | factor 0 at h = 0.1 is still stable; below 0.2 errors shrink, above they grow | correct | D |
| l16 | s8.console | 2.5937424601; 2.0 | correct | C: run, every digit |
| l16 | s8.solution | one array row per step; np.shape(y0) handles numbers and vectors | correct | C |
| l16 | s8.tests, how | 8 tests; fitted order 0.963913; starter fails | correct | C |
| l16 | s8.explain | fitted 0.964 is first order | correct | C |
| l16 | s9.prose | loan L' = 0.06L - 12,000; monthly schedule is Euler with h = 1/12; formula £93,816.35 | correct | C |
| l16 | s9.widget | £93,832.22; slip is the continuous value | correct | C |
| l16 | s9.caption, explain | curves differ by under £16; £15.87 is Euler's first-order error | correct | C |
| l16 | summary.ideas | tangent step; on y' = ry it is compounding; error ∝ h; stable only for h < 2/λ, past it signs flip and grow | correct | BD 8.1; HW2 IV.2 |
| l16 | summary.trap | a step past 2/λ blows up with alternating signs | correct | D: factor < -1 |
| l16 | quiz q-step | y1 = 1.1; slip 1.1222 uses the end slope | correct | C: 1.01/0.9 |
| l16 | quiz q-equilibrium | Euler is exact at an equilibrium for any step | correct | D: f = 0 |
| l16 | quiz q-stable | h < 0.04; at 0.02 the factor is 0 | correct | D |
| l16 | quiz q-order | 0.027 → about 0.0135; true 0.013468 | correct | C |

## l17-runge-kutta

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l17 | s0 | midpoint step 1 + 0.1 × 1.05 = 1.105; slips 1.1, 1.05 | correct | HNW II.1 (explicit midpoint) |
| l17 | s0.explain | ten steps 2.714081, error 0.004201 against 0.124539 | correct | C |
| l17 | s1.prose | k1 to k4 and weights (1, 2, 2, 1)/6 | correct | HNW II.1 "the" Runge-Kutta method; BD 8.3 |
| l17 | s1.widget, hints | factor 1 + h + h²/2 + h³/6 + h⁴/24; 1.6484375² = 2.7173; within 0.001 of e | correct | C |
| l17 | s2 | k = 1, 1.05, 1.0525, 1.10525; y1 = 1.1051708(333) | correct | C |
| l17 | s2.explain | equals the Taylor series of e^h to h⁴ | correct | D |
| l17 | s3.prose | 2.7182797; errors 2.084e-6 and 1.358e-7 | correct | C |
| l17 | s3.canvas | eight log10 points; reference slopes 1 and 4 | correct | C |
| l17 | s3.widget | ratio 15.35, tol 0.08; slips 2 and 16 | correct | C; 16 is rejected as the ideal, not the measured, with a why |
| l17 | s3.explain | fourth order | correct | HNW II.1, II.3 |
| l17 | s4.prose | 4 evaluations a step against 1; Euler needs 100,000 steps for 1.36e-5; RK4 better in ten | correct | C |
| l17 | s4.canvas | cost points | correct | C |
| l17 | s4.widget, explain | 100,000/40 = 2,500; slip 10,000; order beats cost per step | correct | D |
| l17 | s5.canvas points | 64 RK4 points | correct | C: equal to the taught `rk4` to 4 dp |
| l17 | s5.caption | "Orange: Euler's 63 steps" | wrong | Euler's path has `colour: 3`, which the plane canvas draws from `--s3`, green (#1BAF7A); orange is slot 2. Finding 1; C |
| l17 | s5.caption | "Blue: RK4's 63 steps" | correct | `colour: 1` is `--s1`, blue |
| l17 | s5.options a | radius 0.9999996 after 63 steps | correct | C: modulus of R(0.1i) = 1 - 6.9e-9 |
| l17 | s5.options b, c, d | not Euler's 1.3681; not exact; shrinks, does not grow | correct | D: abs(R(ih))² = 1 - h⁶/72 + h⁸/576 |
| l17 | s6.console | slipped step; order 1.979 | correct | C |
| l17 | s6.prose | 2.71613 at t = 1; measured order 1.98 | correct | C |
| l17 | s6 key | line 4 (k3 built from k1) | correct | lines count from the `def` |
| l17 | s6.explain | with k1 the step matches Taylor only to h², order about 2 | correct | HNW II.1 order conditions: Σ b a c = 1/12, not 1/6; C |
| l17 | s7.prose | R(z) = 1 - z + z²/2 - z³/6 + z⁴/24 with z = hλ; R(2.5) = 0.6484; R(3) = 1.375; abs(R) = 1 at 2.7853 | correct | HW2 IV.2; C (bisection) |
| l17 | s7.prose | `numerics` uses z < 0 and places the limit at -2.7853 | correct | sign convention only |
| l17 | s7.widget, explain | h < 0.2785 for λ = 10; about 1.4 times Euler's; exact on a linear equation | correct | C: abs(R) < 1 on all of (0, 2.7853) |
| l17 | s8.prose | order p: error about Ch^p; halving divides by 2^p; Euler 1, RK4 4; each has a limit on hλ | correct | HNW II.3; HW2 IV.2 |
| l17 | s8.widget | factor 8 means p = 3 | correct | D |
| l17 | s9.prose | seven steps within 5e-5 of 0.014164; five steps not | correct | C (hidden tests 5 and 6) |
| l17 | s9.console | 1.1051708333333332; 2.718279744135166 | correct | C: run, every digit |
| l17 | s9.tests, how | 9 tests; t³ exact; 0.9999995630469712; R(3) = 1.375; starter fails | correct | C |
| l17 | s9.explain | exact for y' = t³ because the weights are Simpson's rule | correct | D: f independent of y reduces RK4 to Simpson |
| l17 | s9.explain | Euler would need about 16,000 steps | correct | C: error 5e-5 crossed between 15,000 and 17,000; D: error ≈ 0.80h |
| l17 | s10.prose | `solve_ivp` defaults to an adaptive RK45 pair controlled by rtol and atol | correct | SciPy reference, `solve_ivp` (method "RK45", Dormand-Prince) |
| l17 | s10.console | 0.0141640489531...; 0.01416404894540483 | correct | C: run with SciPy 1.14.1 |
| l17 | s10.tests, how | 4 tests within 1e-8 | correct | C |
| l17 | s10.explain | error near 1e-11; test against the closed form | correct | C: 7.7e-12 |
| l17 | s11.prose | hλ under 2 for Euler, 2.7853 for RK4 | correct | HW2 IV.2 |
| l17 | s11.widget | 15 steps; slips 20 and 14 (z = 2.857) | correct | C |
| l17 | s11.explain | Euler needs more than 20 | correct | D: 40/n < 2 |
| l17 | summary | weights; Taylor to h⁴ on y' = y; error about Ch⁴; stable only for hλ < 2.7853 | correct | as above |
| l17 | summary.trap | a slip still runs; only the measured order exposes it | correct | C (s6) |
| l17 | quiz q-step | 0.9048375; slip 0.9 | correct | C |
| l17 | quiz q-mid | 1.22; slip 1.2 | correct | D |
| l17 | quiz q-ratio | 3.2e-6/16 = 2e-7; whys | correct | D |
| l17 | quiz q-unstable | factor 1.375 at hλ = 3; whys (Euler's is -2; linear is not exact) | correct | C |

## l18-four-decimal-places

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l18 | s0.prose | price 100e^{-I(5)}, I the area under r | correct | BM 3.2.1 with σ = 0: D = exp(-∫r) |
| l18 | s0.widget | £78.92; slips 81.87 (4% flat) and 74.08 (6% flat) | correct | C |
| l18 | s0.explain | I(5) = 0.236717; price between the two flat-rate prices | correct | C |
| l18 | s1.prose | I(T) = θT + (r0-θ)(1 - e^{-κT})/κ | correct | D: integrate θ + (r0-θ)e^{-κt} |
| l18 | s1.widget | 1.835830; slip 0.917915 | correct | C |
| l18 | s1.explain | D = 0.789215, price £78.9215 | correct | C |
| l18 | s2.prose | system (r, I)' = (κ(θ-r), r) from (0.06, 0); Euler's I adds h·r_n | correct | D |
| l18 | s2.caption | D_n = exp(-(0.2 + 0.04(1 - (1 - 2.5/n)^n))) | correct | C: equals Euler on the system for all seven stops |
| l18 | s2.widget, explain | 0.788402, 0.789134, 0.789207; tenfold error per tenfold n | correct | C |
| l18 | s3.prose | four decimals means abs(D_num - D) < 5e-5; 0.789255 is inside and prints 0.7893 | correct | convention stated on the screen; D: 4.0e-5 |
| l18 | s3.widget | smallest n is 163; 50.02 at 162, 49.71 at 163 | correct | C: also the minimum over all n |
| l18 | s3.hints, feedback | error about 8.1e-3/n; 81e-6 at 100 | correct | C |
| l18 | s4.canvas rows | RK4 D_n and errors for n = 1, 2, 4, 8 | correct | C |
| l18 | s4.widget | 4 is the first in 1, 2, 4, 8 inside the band | correct | C |
| l18 | s4.explain | 3.6 times inside the band; ten steps 2.6e-7; "Euler needed 163 for what RK4 does in 4" | correct | C: n = 3 errs by 52.8e-6, so 4 is also the true minimum |
| l18 | s5.prose, canvas | Euler errors 618.0, 1964.6, 1015.1, 508.2, 253.7 (×1e-6) | correct | C |
| l18 | s5.options b | two steps are lucky: r overshoots below 4% and the errors in I cancel | correct | C: r_1 = 3.5%; D: +0.0215 and -0.0207 |
| l18 | s5.options c | hκ = 1.25, factor -0.25, stable | correct | D |
| l18 | s5.options d, explain | from 4 steps on each doubling halves the error | correct | C: ratios 1.94, 2.00, 2.00 |
| l18 | s5.options a | one step size proves nothing; double until two runs agree | correct | standard convergence testing (HNW II.4 uses the same idea for error estimates) |
| l18 | s6.prose, table | monthly Euler D = 0.789080, £78.9080; prices within 5p | correct | C: 1.35p |
| l18 | s6.options a, b, c, d | off by 1.35e-4; 5p is 5e-4 in D; 163 steps; hκ = 0.0417 | correct | C |
| l18 | s6.feedback.correct, explain | "prints as 0.7891 against 0.7892, so the fourth decimal is wrong" | imprecise | the lesson's own test is the band (s3 says printed digits can differ inside it); finding 2 |
| l18 | s6.feedback.b | 5p on £100 is ten times the band | correct | D |
| l18 | s7.prose | noisy price gains e^{½Var(I)}, "because e^{-I} is convex" | imprecise | the exact factor needs I normal; convexity gives only the direction (Jensen). Finding 4 |
| l18 | s7.prose | ½Var(I) = 4.643σ²; D = 0.789581; £78.9581 | correct | BM 3.2.1 variance of ∫r; C, with a Monte Carlo of 200,000 paths |
| l18 | s7.widget | £0.0367 higher; slip negative | correct | C |
| l18 | s7.explain | the no-noise system gives the expected rate path, not the expected discount factor | correct | BM 3.2.1: E r(t) = θ + (r0-θ)e^{-κt}; Jensen |
| l18 | s8.lines, key | closed form, doubling runs, two-part stop, report; d1 trusts one grid | correct | the stop rule needs D, so the closed form must come first |
| l18 | s9.prose | `steps_to_4dp` is only the search; the full check also needs two runs to agree | correct | consistent with s8 and the homework |
| l18 | s9.console | 0.7892149197923242; 0.7892288673245939; 4 | correct | C: run, every digit |
| l18 | s9.prelude | `discount_euler` uses the old r in I (tuple assignment) | correct | C: matches the s2 caption |
| l18 | s9.tests, how | 9 tests; Euler 256, RK4 4; RK4 with 50 steps within 1e-9; starter fails | correct | C |
| l18 | s9.explain | doubling overshoots: 128 fails, 256 passes, true minimum 163 | correct | C |
| l18 | s10.prose | compare with the closed form; output varies slightly by SciPy version | correct | C |
| l18 | s10.console | 1.78e-12 | correct | C: SciPy 1.14.1 |
| l18 | s10.tests, how, explain | 4 tests within 1e-8; agreement about 2e-12 | correct | C |
| l18 | s11.console | RK4 log: 3.9e-04, 1.4e-05, 6.7e-07, agree, pass | correct | C |
| l18 | s11.options | validate on a closed-form case first; whys | correct | model validation practice; consistent with s5, s6 and l17 s6 |
| l18 | summary.ideas | band is about D; Euler 163, RK4 4; trust after a doubling sequence converges and matches | correct | C |
| l18 | summary.formula | D and I(T); 0.789215 | correct | C |
| l18 | summary.trap | monthly Euler is within 2p yet misses | correct | C: 1.35p |
| l18 | quiz q-flat | e^{-0.25} = 0.7788; slip 0.75 | correct | C |
| l18 | quiz q-band | only 0.789180 is inside; errors 8.1e-5, 1.35e-4, 7.5e-5 | correct | C |
| l18 | quiz q-steps | about 200, tol 10; slip 142 | correct | D: 8.1e-3/n = 4e-5 gives 202 |
| l18 | quiz q-rk4 | about 9e-7; true 6.7e-7 | correct | C |

## review-4

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| rev | r-t-cubed | 3!/2⁴ = 0.375; slip 0.0625 | correct | C |
| rev | r-growing | 2/(0.05-0.03) = £100; slip 25; exists because 0.05 > 0.03 | correct | D |
| rev | r-invert | 3/(s(s+3)) inverts to 1 - e^{-3t}; slip 3e^{-3t} | correct | D: residues 1 and -1 |
| rev | r-residues | y = 2e^{-t} - e^{-2t}; y(1) = 0.6004; slip 0.8711 | correct | C |
| rev | r-euler-two | 0.5² = 0.25 against e^{-1} = 0.3679 | correct | D |
| rev | r-system-step | eigenvalues -1, -3; h < 2/3; fastest limits the step, slowest sets the half-life | correct | C (eigenvalues); HW2 IV.2 |
| rev | r-rk4-predict | 48/16 = 3; slips 24, 12 | correct | D |
| rev | r-rk4-limit | 2.7853/25 = 0.1114; slip 0.08 | correct | D |
| rev | r-monthly | 60 × 2.7 = 162, tol 3 admits the exact 163; slip 99 | correct | C |
| rev | r-converged | two agreeing runs and the closed form; whys | correct | consistent with l18 s8 |

## homework-4

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| hw | h-shifted-ramp | L{t e^{-2t}}(1) = 1/9; slip 1 | correct | BD 6.3 |
| hw | h-solve-order | y'' - y = 0, y(0) = 0, y'(0) = 2: Y = 2/(s²-1) = 1/(s-1) - 1/(s+1), y = 2 sinh t | correct | D: y'' = y, y(0) = 0, y'(0) = 2 |
| hw | h-solve-order key | only one valid order; d1 drops the starting values | correct | each line follows from the one before |
| hw | h-complex-invert | (2s+3)/(s²+2s+5) inverts to e^{-t}(2cos 2t + ½ sin 2t); slip | correct | D: 2(s+1) + ½·2 over (s+1)² + 4 |
| hw | h-stiff-system | eigenvalues -1, -20: h < 0.1; slow factor alone would allow 2; "weeks" and "years" | correct | HW2 IV.2; D: time constants 1/20 year and 1 year |
| hw | h-rk4-predict | 20.84/16 = 1.30; true 1.358, ratio 15.35; slip 10.42 | correct | C |
| hw | h-match-4dp.prose | bond as (r, D)' = (0.5(0.04-r), -rD); rule needs both gaps under tol | correct | D: D' = -rD |
| hw | h-match-4dp.tests, how | 7 tests; bond 8, oscillator 16, exp 16, planted form None; starter fails | correct | C |
| hw | h-match-4dp.how | Euler would need about 16,000 on the oscillator | correct | C |
| hw | h-match-4dp.explain | stops one doubling after RK4 first meets the band | correct | C: first inside at 4, 8, 8; stops at 8, 16, 16 |
| hw | h-monthly-note.model | band; error 1.35e-4 is 2.7 bands; 1.35p; 5p is ten bands | correct | C |
| hw | h-monthly-note.model | first order; about 162, exact 163; RK4's 4 steps err by 1.4e-5; 4- and 8-step runs agree | correct | C (the lesson's (r, I) system) |
| hw | h-monthly-note.rubric | six lines match the model | correct | read against the model |
| hw | h-which-exist | a and c exist; b diverges; e^{t²} beats every rate; 1/0.03 and £33.33 | correct | region of convergence; C |

## Counts

Rows: 244. correct 240, wrong 1, imprecise 3, misleading 0, unverified 0.
