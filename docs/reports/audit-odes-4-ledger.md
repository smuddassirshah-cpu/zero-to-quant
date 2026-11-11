# Claim ledger: odes level 4 (blind concept audit, round 1)

Written before reading any earlier review or author report. Scope: `l14-laplace-transform`, `l15-solving-with-laplace`, `l16-euler-method`, `l17-runge-kutta`, `l18-four-decimal-places`, `review-4`, `homework-4` (performance tasks `h-match-4dp` and `h-monthly-note` included). No `fluency-*` or `problems-*` file belongs to a level 4 lesson.

"script" means a check in `docs/reports/odes-L4-concepts.py` (251 checks pass; 10 checks tied to findings fail until the fix pass). "Pyodide" means the widget code was also run in Pyodide 0.27.7 (NumPy 2.0.2, SciPy 1.14.1) from the local package folder.

Sources: BD = Boyce and DiPrima, *Elementary Differential Equations and Boundary Value Problems* (ch. 6 the Laplace transform, ch. 8 numerical methods); Schiff = *The Laplace Transform: Theory and Applications*; HNW = Hairer, Nørsett and Wanner, *Solving Ordinary Differential Equations I* (I.7 Euler, II.1 to II.4 Runge-Kutta); HW = Hairer and Wanner, *Solving Ordinary Differential Equations II* (IV.2 stability functions); LeVeque = *Finite Difference Methods for Ordinary and Partial Differential Equations* (ch. 5 to 7); BF = Burden and Faires, *Numerical Analysis* (1.2 rounding, 5.2 Euler, 5.4 Runge-Kutta); Hull = *Options, Futures and Other Derivatives* (ch. 4 continuous compounding); BM = Brigo and Mercurio, *Interest Rate Models* (3.2.1 Vasicek); SciPy = `scipy.integrate.solve_ivp` reference.

Files are in `app/content/courses/odes/`. A path such as `s3.hints` means `screens[3].hints[0..2]`; `q1` means `quiz[1]`; `i4` means `items[4]`.

## l14-laplace-transform

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l14 | s0.prose | Money due at time t is worth e^{-st} today at continuous rate s; the value of £1 a year for ever is the area under that curve | correct | Hull 4.2 (continuous compounding); integral of the discounted flow |
| l14 | s0.widget.answer, hints, feedback.correct, explain | The area at 4% is 1/0.04 = 25 | correct | script (quad) |
| l14 | s0.widget.wrong[percent], feedback.byKey.percent | 0.25 is 1/4: the rate entered as 4, not 0.04 | correct | 1/4 = 0.25 |
| l14 | s0.explain | A higher rate shrinks the area | correct | 1/s is decreasing for s > 0 |
| l14 | s1.prose | Definition: F(s) = integral from 0 to infinity of e^{-st} f(t) dt, written L{f} | correct | BD 6.1 definition 6.1.1 (real s) |
| l14 | s1.widget.answer, accept, feedback.correct | L{1} = 1/s for s > 0 | correct | BD 6.1 example 1; script |
| l14 | s1.hints | Integral to b is (1/s)(1 - e^{-sb}); let b go to infinity | correct | direct integration |
| l14 | s1.widget.wrong[rate], feedback.byKey.rate | s is the rate; the area is its reciprocal | correct | follows |
| l14 | s1.explain | A perpetuity at rate s is worth 1/s; every present value at a continuous rate is a Laplace transform | correct | Hull 4.2; true of a flow f(t) valued over [0, infinity), which is the lesson's setting |
| l14 | s2.prose | e^{-st} e^{at} = e^{-(s-a)t}, the same curve with rate s - a | correct | exponent law |
| l14 | s2.options[a], feedback.correct, hints | L{e^{at}} = 1/(s - a), for s > a only | correct | BD 6.1 example 2; script |
| l14 | s2.options[b].why | 1/(s + a) adds the rates; a is subtracted | correct | exponent is -(s - a)t |
| l14 | s2.options[c].why, feedback.byKey.c | The formula fails at s <= a: the curve never falls and the area keeps growing | correct | script (600-year and 6000-year areas) |
| l14 | s2.options[d].why | e^{a}/s moves a t-dependent factor out of the integral | correct | e^{at} is not constant in t |
| l14 | s2.explain | At s <= a the area grows without bound | correct | integrand does not decay; script |
| l14 | s3.prose | Parts with u = t, dv = e^{-st} dt: boundary term 0 at both ends, leaving (1/s) times the integral of e^{-st} | correct | BD 6.1; for s > 0, t e^{-st} tends to 0 |
| l14 | s3.widget.answer, hints, explain | L{t} = 1/s^2 = 0.25 at s = 2; the shaded area is the same | correct | script (quad) |
| l14 | s3.widget.wrong, feedback.byKey | 0.5 is 1/s; 4 is s^2 | correct | arithmetic |
| l14 | s4.prose | Two rounds of parts give L{t^2} = 2/s^3; sines and cosines also take two rounds | correct | BD 6.1 examples 5 to 7 |
| l14 | s4.widget.rows, hints, explain | L{sin 3t} = 3/(s^2+9), L{cos 2t} = s/(s^2+4); at s = 1 the values are 2, 0.3, 0.2 | correct | BD table 6.2.1; script (quad) |
| l14 | s4.prose, explain | The signed area of e^{-t} sin 3t is L{sin 3t}(1) = 0.3 | correct | definition at s = 1; script |
| l14 | s4.feedback.byKey.r1c2, r2c2 | s on top is the cosine's transform; b on top is the sine's | correct | BD table 6.2.1 |
| l14 | s5.prose | £5 a year growing at 2% is worth L{5e^{0.02t}}(r) = 5/(r - 0.02), £125 at 6%: the Gordon growth model | correct | continuous-time Gordon growth, c/(r - g); script |
| l14 | s5.options[c], hints, feedback.correct | At r = 1% the integrand is 5e^{0.01t}: no finite value | correct | script (area grows tenfold from 600 to 900 years) |
| l14 | s5.options[a].why, feedback.byKey.a | -£500 trusts 1/(s - a) where the integral does not exist; it holds only for s > a | correct | BD 6.1 |
| l14 | s5.options[b].why | £500 drops the sign of r - g; the formula does not apply when r <= g | correct | follows |
| l14 | s5.options[d], why, feedback.byKey.d | L{5} L{e^{0.02t}} at 0.01 is -£50,000; the transform of a product is not the product of transforms | correct | (5/0.01)(1/(-0.01)) = -50,000; script (t e^{-t} counterexample); BD 6.6 (products of transforms invert to convolutions) |
| l14 | s5.explain | L{e^{at}} exists only for s > a; a negative price is the formula used outside that range | correct | BD 6.1 |
| l14 | s6.canvas.state.caption | e^{t^2 - st} is lowest at t = s/2, then climbs for ever | correct | derivative of t^2 - st is 2t - s; script |
| l14 | s6.options[a], hints, feedback.correct | e^{t^2} has no transform at any s: t^2 - st = t(t - s) > 0 once t > s | correct | BD 6.1 (not of exponential order); script |
| l14 | s6.options[b].why | e^{5t} has transform 1/(s - 5) for s > 5 | correct | table |
| l14 | s6.options[c].why | t^10 has transform 10!/s^11 for s > 0 | correct | BD table; script (quad) |
| l14 | s6.options[d].why | sin(t^2) stays in [-1, 1], so e^{-st} makes it integrable for every s > 0 | correct | comparison with e^{-st}; script |
| l14 | s6.explain | "Any function growing no faster than some e^{at} has a transform" | imprecise | BD theorem 6.1.2 needs piecewise continuity on every [0, A] as well as exponential order; 1/t is below e^{t} for t >= 1 and has no transform (script). Finding 6 |
| l14 | s7.widget.lines s1 to s4 | L{f'} = [e^{-st} f]_0^inf + s times the integral of e^{-st} f = sF(s) - f(0), given e^{-st} f(t) tends to 0 | correct | BD theorem 6.2.1; the decay condition is on the line; script (two functions) |
| l14 | s7.widget.lines d1, why, feedback.byKey.d1 | The lower limit is subtracted, so the bracket is 0 - f(0) | correct | fundamental theorem of calculus |
| l14 | s7.explain | Parts moves the derivative onto e^{-st}, which brings out s; applied twice, L{f''} = s^2 F - s f(0) - f'(0) | correct | BD corollary 6.2.2; script |
| l14 | s8.prose | Transforms add: L{af + bg} = aF + bG | correct | linearity of the integral; script |
| l14 | s8.prose, canvas rows | Shift rule L{e^{at} f(t)} = F(s - a) | correct | BD theorem 6.3.2; script |
| l14 | s8.canvas rows | Table: 1, e^{at}, t^n, sin bt, cos bt with ranges s > 0 or s > a | correct | BD table 6.2.1 |
| l14 | s8.widget.answer, accept, hints, explain | L{e^{-t} cos 2t} = (s+1)/((s+1)^2+4) = (s+1)/(s^2+2s+5) | correct | script (quad at two s) |
| l14 | s8.widget.wrong[sign], feedback.byKey.sign | (s-1)/((s-1)^2+4) shifts the wrong way; with a = -1, s - a = s + 1 | correct | script (differs at s = 0.5 and 2) |
| l14 | s9.prose | The integral is cut at T = 50 and summed by the trapezium rule on n strips | correct | composite trapezium rule (BF 4.4) |
| l14 | s9.widget.solution | h (sum of g - half the end values) is the trapezium sum; pv_growing raises when r <= g | correct | script: 9 tests and 2 examples pass, starter fails all 9; Pyodide |
| l14 | s9.canvas lines[1] | laplace_numeric(t, 2) prints 0.24999999479166676 | wrong | true under NumPy 2.5 on a desktop; the app's Pyodide (NumPy 2.0.2) prints 0.24999999479166674. Finding 3 |
| l14 | s9.canvas lines[3], lines[5] | pv_growing(5, 0.02, 0.06) prints 125.00000000000001; the 1% case raises ValueError | correct | script; Pyodide |
| l14 | s9.hints | Trapezium sum is h times all the values less half of the two end values | correct | BF 4.4 |
| l14 | s9.feedback.correct | The trapezium values sit within 1e-7 of 0.5, 0.25 and 0.3 | correct | script: errors 1.0e-8, 5.2e-9, 1.6e-8 |
| l14 | s9.explain | 200,000 strips are accurate to about 1e-8; the cut at T = 50 costs below 1e-18 | correct | error (h^2/12)(g'(T) - g'(0)); tails at most e^{-50} times 2602 = 5.0e-19; script |
| l14 | s9.how | Tolerances 1e-6 (1e-5 for t^2), prices by relative 1e-9, two cases raise | correct | read from the test list |
| l14 | s10.prose | A constant hazard rate 2% gives default-time density 0.02 e^{-0.02t} | correct | exponential law of a constant hazard (Hull 24.1) |
| l14 | s10.prose, widget.answer, hints, explain | Value 100 L{0.02 e^{-0.02t}}(0.04) = 100 times 0.02/0.06 = £33.33 | correct | script (quad and Monte Carlo, 2 million draws) |
| l14 | s10.prose | The moment generating function is this transform read at -s | correct | M(u) = E[e^{u tau}] = F(-u) for a density on [0, infinity); script |
| l14 | s10.widget.wrong, feedback.byKey | 50 is 0.02/0.04 (the density's own decay left out); 100 is undiscounted | correct | arithmetic |
| l14 | s10.explain | Discounting and default add their rates | correct | e^{-0.04t} e^{-0.02t} = e^{-0.06t} |
| l14 | summary.ideas, formula, trap | PV at rate s is a transform; table from definition and parts; L{f'} = sF - f(0); 1/(s - a) at s <= a means nothing | correct | rows above |
| l14 | q0 | L{e^{3t}}(5) = 0.5; 0.125 uses 1/(s + a) | correct | script |
| l14 | q1 options, feedback, explain | L{f''} = s(sF - f(0)) - f'(0); the three distractors drop, unscale or swap the starting values | correct | BD corollary 6.2.2 |
| l14 | q2 | L{sin 3t}(4) = 3/25 = 0.12; 0.16 is the cosine's | correct | script |
| l14 | q3 options, explain | The integral of e^{-st} e^{2t} exists exactly when s > 2, and is then 1/(s - 2) | correct | script |

## l15-solving-with-laplace

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l15 | s0.prose, states s0 to s4 | y' + 2y = 4, y(0) = 0: sY + 2Y = 4/s, Y = 4/(s(s+2)) = 2/s - 2/(s+2), y = 2 - 2e^{-2t} | correct | BD 6.2; script (ODE solver and transform of the answer) |
| l15 | s0.states.s0.ops[1].why | Integrating both sides needs the unknown y itself | correct | the integral of 2y is unknown |
| l15 | s0.states.s2.ops[1].why | There is no product rule for inverting; split into a sum first | correct | BD 6.6 (a product inverts to a convolution) |
| l15 | s0.hints, feedback, explain | Cover-up gives 2/s - 2/(s+2); the answer follows the slope field | correct | residues 4/2 and 4/(-2) |
| l15 | s1.prose | The Laplace method: transform, solve the algebra, split by partial fractions, invert by the table | correct | BD 6.2 |
| l15 | s1.widget.answer, hints, explain | y(1) = 2 - 2e^{-2} = 1.7293; the curve leaves 0 with slope 4 and levels off at 2 | correct | script; y'(0) = 4 - 0 |
| l15 | s1.widget.wrong[one], feedback.byKey.one | 1.2642 is 2 - 2e^{-1}; the pole at -2 gives e^{-2t} | correct | script |
| l15 | s2.prose | r' = 0.5(0.04 - r), r(0) = 0.06 transforms to sR - 0.06 = 0.02/s - 0.5R | correct | derivative rule and L{0.02} = 0.02/s |
| l15 | s2.widget.answer, accept, hints | R = (0.06s + 0.02)/(s(s + 0.5)) = 0.04/s + 0.02/(s + 0.5) | correct | script (quad at two s) |
| l15 | s2.widget.wrong[no-start], feedback.byKey | 0.02/(s(s+0.5)) drops r(0) and solves from a zero rate | correct | script |
| l15 | s2.explain | r = 0.04 + 0.02 e^{-0.5t}, lesson 5's theta + (r0 - theta)e^{-kappa t} | correct | script (ODE solver) |
| l15 | s3.prose | y'' + 3y' + 2y = 2 from rest gives Y = 2/(s(s+1)(s+2)) | correct | s^2 + 3s + 2 = (s+1)(s+2) |
| l15 | s3.prose | Cover-up: hide a pole's factor and put s equal to the pole | correct | Heaviside cover-up for distinct linear factors (BD 6.2, example 1) |
| l15 | s3.widget.rows, hints, feedback | Residues 1, -2, 1 at 0, -1, -2 | correct | script (roots and derivative form) |
| l15 | s3.explain | y = 1 - 2e^{-t} + e^{-2t}; y(1) = 0.399576 | correct | script (ODE solver) |
| l15 | s4.prose | y'' + 2y' + 5y = 0, y(0) = 1, y'(0) = 0 gives (s^2+2s+5)Y = s + 2, Y = (s+2)/((s+1)^2+4) | correct | s^2 Y - s + 2(sY - 1) + 5Y = 0 |
| l15 | s4.canvas.state.caption | Real part -1 sets the decay; imaginary part 2 sets the (angular) frequency | correct | BD 3.3 |
| l15 | s4.widget.answer, accept, hints, feedback.correct | y = e^{-t}(cos 2t + (1/2) sin 2t) | correct | script (ODE solver; transform at s = 0.3) |
| l15 | s4.widget.wrong, feedback.byKey | cos-only drops the leftover 1; full-sine forgets b = 2 on top | correct | 1 = (1/2) times 2 |
| l15 | s4.explain | y(1) = 0.014164; the poles -1 +/- 2i are the eigenvalues of lesson 12's test: decay e^{-t}, frequency 2 | correct | script; the poles are the roots of the characteristic polynomial |
| l15 | s5.prose, options[a], hints, explain | Dropping every starting term gives (s^2+2s+5)Y = 0, so Y = 0 and y = 0, the problem from rest | correct | script (solver from rest stays at 0) |
| l15 | s5.options[b].why, feedback.byKey.b | The true answer needs -s y(0) - y'(0) - 2y(0) | correct | derivative rules |
| l15 | s5.options[c].why | e^{-t} cos 2t keeps part of the starting value | correct | Y = (s+1)/((s+1)^2+4) keeps s + 1 of s + 2 |
| l15 | s5.options[d].why | (1/2)e^{-t} sin 2t is the solution from y(0) = 0, y'(0) = 1 | correct | script (ODE solver) |
| l15 | s6.prose, answer, hints, explain | 1/(s+1)^2 inverts to t e^{-t}: the shift of 1/s^2; lesson 7's (c1 + c2 t)e^{rt} | correct | BD 6.3; script |
| l15 | s6.widget.wrong, feedback.byKey | e^{-t} inverts 1/(s+1); e^{-2t} squares the exponential | correct | table |
| l15 | s7.prose | Four steps: transform with the two derivative rules, solve for Y, split one piece per pole, invert | correct | BD 6.2 |
| l15 | s7.options, feedback, explain | Step 1 brings in the starting values, so no constants are left to fit; that is why the method suits initial value problems | correct | BD 6.2 |
| l15 | s8.prose | For distinct poles p_k of num/den the residue is num(p_k)/den'(p_k) and y(t) = sum of res_k e^{p_k t} | imprecise | true for a proper fraction (deg num < deg den), the unstated hypothesis; for s/(s+1) the formula returns -e^{-t} and misses the constant 1 (script). Finding 7 |
| l15 | s8.prose | Coefficient lists run from the highest power, as in np.roots | correct | NumPy reference |
| l15 | s8.widget.solution | np.roots, np.polyval, np.polyder give poles and residues; the real part of the sum is returned | correct | script: 7 tests and 1 example pass, starter fails all 7; Pyodide |
| l15 | s8.canvas lines | residues prints (array([-2., -1., 0.]), array([1., -2., 1.])); inverse_laplace prints 0.39957640089372803 | correct | Pyodide prints exactly these lines |
| l15 | s8.tests[3] | Residue of (s+2)/(s^2+2s+5) at -1 + 2i is 0.5 - 0.25i | correct | (1 + 2i)/(4i) = 0.5 - 0.25i |
| l15 | s8.how | y(1) within 1e-9 of the closed forms, poles and residues within 1e-6 | correct | read from the test list |
| l15 | s8.explain | The derivative form of cover-up works for any distinct poles; a complex pair's terms are conjugates, so imaginary parts cancel | correct | limit of (s - p) num/den at a simple pole; script (real coefficients) |
| l15 | s9.prose, answer, hints, explain | A flow r(t) discounted at a flat 5% is worth R(0.05) = 0.04/0.05 + 0.02/0.55 = 0.8364 | correct | script (quad) |
| l15 | s9.widget.wrong, feedback.byKey | 0.8 values only the long-run 4% | correct | 0.04/0.05 |
| l15 | s9.prose, explain | Some option prices have closed-form transforms in maturity and are inverted numerically; Fourier inversion is the sister method | correct | Geman and Yor (1993) Asian options; Carr (1998) randomisation; Carr and Madan (1999) |
| l15 | summary | Each pole p gives e^{pt}; a complex pair rings at its imaginary part; a double pole brings a factor t; dropping starting terms solves from rest | correct | rows above |
| l15 | q0 options, explain | y' - 3y = 0, y(0) = 2: sY - 2 - 3Y = 0, Y = 2/(s - 3), y = 2e^{3t}; the distractors flip a sign or transform 3y as 3/s | correct | script |
| l15 | q1 | Residue of 1/((s-1)(s+2)) at 1 is 1/3; -1/3 is the residue at -2 | correct | script |
| l15 | q2 options, explain | Poles -2 +/- 3i: frequency 3 inside the envelope e^{-2t}; a complex pair always oscillates, only real poles creep | correct | BD 3.3; for a non-zero residue |
| l15 | q3 | 3/(s + 2) inverts to 3e^{-2t} | correct | table with a = -2 |

## l16-euler-method

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l16 | s0.prose, rows, hints, feedback | Euler on y' = y, h = 0.5: 1, 1.5, 2.25; each step adds h times the slope at the start | correct | BD 8.1; script |
| l16 | s0.explain | e = 2.718282; two steps fall short by 0.47 | correct | script |
| l16 | s1.prose | Euler's method: y_{n+1} = y_n + h f(t_n, y_n) | correct | BD 8.1; HNW I.7 |
| l16 | s1.answer, hints, explain | On y' = y each step multiplies by 1 + h; h = 0.25 gives 1.25^4 = 2.4414; the gap falls from 0.47 to 0.28 | correct | script |
| l16 | s1.widget.wrong[half], feedback | 2.25 is the h = 0.5 value | correct | script |
| l16 | s2.prose, explain | Euler on y' = 0.05y with h = 1/12 is monthly compounding; the continuous rate is the limit as the step shrinks | correct | (1 + r/m)^m tends to e^r (Hull 4.2) |
| l16 | s2.answer, hints | (1 + 0.05/12)^12 = 1.051162 against e^{0.05} = 1.051271 | correct | script |
| l16 | s2.widget.wrong, feedback.byKey | 1.051271 is the continuous answer; 1.05 is one annual step | correct | arithmetic |
| l16 | s3.prose | Errors at t = 1: 0.124539 (h = 0.1), 0.064984 (0.05), 0.013468 (0.01) | correct | script |
| l16 | s3.answer, hints, feedback | Halving h from 0.1 to 0.05 cuts the error by 1.92, close to 2 | correct | script |
| l16 | s3.widget.wrong, feedback.byKey | 4 would mean error proportional to h^2; 0.52 is the reciprocal | correct | definition of order |
| l16 | s3.explain | The error is proportional to h; each step errs by about (h^2/2)y'' and there are 1/h steps | correct | BD 8.1 (local truncation error); HNW I.7 theorem 7.5; script (one-step error over h^2 is 0.5017) |
| l16 | s3.explain | The four points have a fitted slope of 0.964: first order | correct | script: 0.96391 (0.9993 for h = 0.001, 0.0005) |
| l16 | s4.prose | Quarterly Euler on r' = 0.5(0.04 - r) adds 0.125(0.04 - r) a step; r(1) = 5.2131% exactly | correct | script |
| l16 | s4.answer, hints, feedback, explain | Four steps: 5.75%, 5.5313%, 5.3398%, 5.1724% | correct | script |
| l16 | s4.widget.wrong, feedback.byKey | 5% is one annual step; 5.2131% is the closed form, which Euler undershoots | correct | script |
| l16 | s4.explain | Monthly steps give 5.2001%: three times as many steps, about a third of the error | correct | script: error ratio 0.318 |
| l16 | s5.prose | Euler with h = 0.1 on x' = y, y' = -x sends (x, y) to (x + 0.1y, y - 0.1x); the true orbit is the unit circle | correct | x^2 + y^2 is conserved by the flow |
| l16 | s5.hints, explain | One step multiplies x^2 + y^2 by 1 + h^2, so the radius grows by sqrt(1.01) a step | correct | (x + hy)^2 + (y - hx)^2 = (1 + h^2)(x^2 + y^2) |
| l16 | s5.answer, question | After 63 steps, one turn, the radius is 1.3681 | correct | script; 63 atan(0.1) = 6.279 against 2 pi = 6.283 |
| l16 | s5.widget.wrong, feedback.byKey | 1 is the true orbit; 1.8717 is 1.01^63, the squared radius | correct | script |
| l16 | s5.explain, feedback.byKey.circle | Each tangent step leaves the circle on its outside | correct | the tangent line lies outside a circle |
| l16 | s5.canvas points | The 64 drawn points are Euler's path, ending at (1.3681, 0.0056) | correct | script |
| l16 | s6.prose, series | y' = -10y with h = 0.25: Euler multiplies by 1 - 10h = -1.5; true values 0.0821, 0.0067, 0.0006 | correct | script |
| l16 | s6.answer, hints, explain | After four steps Euler gives 5.0625 against e^{-10} = 0.0000454; each step overshoots zero and lands further away | correct | script |
| l16 | s6.widget.wrong, feedback.byKey | 0 expects decay; -5.0625 has the sign wrong | correct | (-1.5)^4 > 0 |
| l16 | s7.prose | On y' = -lambda y the steps shrink only if abs(1 - h lambda) < 1, so h < 2/lambda | correct | BD 8.6; LeVeque 7.2 (lambda > 0, h > 0) |
| l16 | s7.prose | This is lesson 12's discrete test; for an eigenvalue mu = -lambda < 0 the factor reads 1 + h mu | correct | modulus of the multiplier below 1 (odes l12, "Continuous against discrete") |
| l16 | s7.prose | At h = 0.05 the factor is 0.5; at h = 0.1 it is 0 (lambda = 10) | correct | script |
| l16 | s7.prose | Beside slower rates in a system, a fast rate makes it stiff | correct | HW IV.1; numerics l12 |
| l16 | s7.question, widget.answer, feedback.correct | "The largest stable h" for y' = -10y is 0.2 | imprecise | by the screen's own test the stable steps are h < 0.2; at h = 0.2 the factor is -1 and nothing shrinks (script). The key is the limit, not a stable step. Finding 5 |
| l16 | s7.hints, explain | abs(1 - 10h) crosses 1 at h = 0.2; below it every step shrinks, above it every step grows | correct | script (h = 0.1999 decays, 0.2001 grows) |
| l16 | s7.widget.wrong[one], feedback.byKey.one, explain | At h = 0.1 the factor is 0, still stable: one step lands on 0 exactly | correct | 1 - 10(0.1) = 0 |
| l16 | s8.prose, widget.solution | One `euler` serves numbers and systems by keeping y as an array with one row per step | correct | script: 8 tests and 1 example pass, starter fails all 8; Pyodide |
| l16 | s8.canvas lines[2] | `y[-1]` prints 2.5937424601000023 | wrong | the taught loop gives 2.5937424601 in CPython and Pyodide; 2.5937424601000023 is `1.1**10`. Finding 3 |
| l16 | s8.canvas lines[4] | observed_order([0.01, 0.0025], [0.1, 0.05]) prints 2.0 | wrong | np.polyfit returns 1.9999999999999998 (NumPy 2.5) and 1.9999999999999987 (Pyodide). Finding 3 |
| l16 | s8.widget observed_order | The order is the slope of log(error) against log(h) by a straight-line fit | correct | BF 5.2; LeVeque appendix A.6 |
| l16 | s8.how, feedback.correct | 8 tests; fitted order within 1e-6 of 0.963913; 1.1^10, 1.368117, flipping signs | correct | script; Pyodide gives 0.9639130568583 |
| l16 | s8.explain | np.shape(y0) is () for a number and (2,) for a pair, so the same loop handles both | correct | NumPy reference; script |
| l16 | s9.prose | L' = 0.06L - 12,000 from £100,000; the bank's monthly schedule (0.5% interest, £1,000 off) is Euler with h = 1/12 | correct | L + (1/12)(0.06L - 12,000) = 1.005L - 1,000; script |
| l16 | s9.prose | The continuous formula gives £93,816.35 after a year | correct | L = 200,000 - 100,000 e^{0.06t}; script (ODE solver) |
| l16 | s9.answer, hints, feedback | The gap L - 200,000 is multiplied by 1.005 a month; L_12 = £93,832.22, £15.87 above the formula | correct | script |
| l16 | s9.widget.wrong, feedback.byKey, explain | The monthly schedule compounds less often; the £15.87 is Euler's first-order error | correct | (1.005)^12 < e^{0.06} |
| l16 | summary | Euler is compounding on y' = ry; global error proportional to h; stable on y' = -lambda y only for h < 2/lambda, past which the steps flip sign and grow | correct | rows above |
| l16 | q0 | One Euler step on y' = t + y from (0, 1), h = 0.1, gives 1.1; 1.1222 uses the slope at the end | correct | 1.01/0.9 = 1.1222 (backward Euler); script |
| l16 | q1 options, explain | At the equilibrium r = 4% the slope is 0, so Euler stays there exactly, whatever h | correct | f = 0 gives y_{n+1} = y_n; script |
| l16 | q2 question, answer | "The largest stable Euler step" for y' = -50y is 0.04 | imprecise | as s7: the stable steps are h < 0.04. Finding 5 |
| l16 | q2 feedback.byKey.half, explain | At h = 0.02 the factor is 0, still stable; stability needs abs(1 - 50h) < 1 | correct | script |
| l16 | q3 options, explain | Error 0.027 at h = 0.02 becomes about 0.0135 at h = 0.01 (true value 0.013468); 0.0068 would be second order | correct | script |

## l17-runge-kutta

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l17 | s0.prose, answer, hints | Midpoint step: half an Euler step, read the slope there, use it for the whole step; on y' = y from 1 with h = 0.1 it gives 1.105 | correct | HNW II.1 (Runge's midpoint rule); script |
| l17 | s0.widget.wrong, feedback.byKey | 1.1 is Euler; 1.05 is where the half step lands | correct | arithmetic |
| l17 | s0.explain | Ten such steps give 2.714081: error 0.004201 against Euler's 0.124539 | correct | script; measured order 2.00 |
| l17 | s1.prose | RK4: k1 = f(t, y), k2 = f(t + h/2, y + (h/2)k1), k3 = f(t + h/2, y + (h/2)k2), k4 = f(t + h, y + h k3); step with (1/6)(k1 + 2k2 + 2k3 + k4) | correct | HNW II.1 table 1.2 (the classical Runge-Kutta method); BD 8.3 |
| l17 | s1.answer, hints, explain | On y' = y one step multiplies by 1 + h + h^2/2 + h^3/6 + h^4/24; h = 0.5 gives 1.6484375, squared 2.7173, within 0.001 of e | correct | HW IV.2 (stability function of a 4-stage order-4 method); script |
| l17 | s1.explain | Four slopes a step buy a great deal | correct | error 9.4e-4 against Euler's 0.47; script |
| l17 | s2.rows, hints, feedback | k1 to k4 are 1, 1.05, 1.0525, 1.10525 and y1 = 1.1051708 | correct | script |
| l17 | s2.feedback.byKey | k3 is read at y + (h/2)k2; k4 takes a full step with k3; weights 1, 2, 2, 1 over 6 | correct | definition |
| l17 | s2.explain | y1 = 1.1051708333 is the Taylor series of e^h to h^4 at h = 0.1 | correct | script (equal to 1e-15) |
| l17 | s3.prose | Ten RK4 steps reach 2.7182797, error 2.084e-6; twenty err by 1.358e-7 | correct | script |
| l17 | s3.answer, hints, feedback, explain | The ratio is 15.35, close to 2^4 = 16; the RK4 points fall with slope 4: fourth order | correct | script (fitted order 3.97); HNW II.3 |
| l17 | s3.canvas points | The eight points are log10 of Euler's and RK4's errors | correct | script |
| l17 | s3.widget.wrong, feedback.byKey | 2 is first order; 16 is the ideal, the measured ratio is 15.35 | correct | script |
| l17 | s4.prose | RK4 costs four evaluations of f a step, Euler one | correct | four stages |
| l17 | s4.prose, explain | Euler needs 100,000 steps for an error of 1.36e-5; ten RK4 steps (40 evaluations) err by 2.08e-6 | correct | script |
| l17 | s4.answer, wrong, feedback | 100,000/40 = 2,500 times fewer evaluations; 10,000 compares steps | correct | arithmetic |
| l17 | s4.explain | Order beats cost per step | correct | for a smooth problem at this accuracy; script |
| l17 | s4.canvas points | Cost chart: Euler at 10 to 100,000 evaluations, RK4 at 4 to 80 | correct | script |
| l17 | s5.prose | Euler's 63 steps of 0.1 on the centre reach radius 1.3681 | correct | script |
| l17 | s5.options[a], feedback, explain | RK4's 63 steps reach radius 0.9999996; its factor per step has modulus 1 - 6.9e-9 | correct | abs(R(ih))^2 = 1 - h^6/72 + h^8/576; script (0.99999956) |
| l17 | s5.options[b], [c], [d].why | RK4 is not exact here; its small error shrinks this orbit and does not grow it | correct | modulus below 1 for h = 0.1; script |
| l17 | s5.canvas points | The RK4 path drawn ends at (0.9999, -0.0168) | correct | script |
| l17 | s6.prose | With k3 built from k1 the step runs and gives 2.71613 at t = 1 with h = 0.1 | correct | script |
| l17 | s6.prose, canvas lines[7] | Its measured order over h = 0.1 to 0.0125 is 1.98 (1.979) | correct | script: 1.9788 |
| l17 | s6.widget.answer, hints, feedback | The line that breaks fourth order is line 4, where k3 uses k1 | correct | comparison with the definition |
| l17 | s6.feedback.byKey | Lines 3, 5 and 6 are right | correct | definition |
| l17 | s6.explain | With k1 the step matches Taylor only to h^2, so the order falls to about 2 | correct | factor 1 + h + h^2/2 + h^3/12; script (linear and nonlinear test) |
| l17 | s6.explain | Code that runs and looks close can still be wrong: measure its order | correct | LeVeque appendix A.6 (order verification) |
| l17 | s7.prose | On y' = -lambda y one RK4 step multiplies by R(z) = 1 - z + z^2/2 - z^3/6 + z^4/24 with z = h lambda | correct | HW IV.2; script (step equals R to 1e-13) |
| l17 | s7.prose | R(2.5) = 0.6484, R(3) = 1.375; abs(R) = 1 at z = 2.7853 | correct | script (root 2.78529; abs(R) < 1 on the whole of (0, 2.7853)); HW IV.2 figure 2.1 |
| l17 | s7.prose | `numerics` writes z = h lambda < 0 for y' = lambda y and places the limit at -2.7853 | correct | numerics l12 text read |
| l17 | s7.question, answer, feedback.correct | "The largest stable h" for y' = -10y with RK4 is 0.2785 | imprecise | the stable steps are h < 0.27853. Finding 5 |
| l17 | s7.widget.wrong, feedback.byKey | 0.2 is Euler's limit 2/lambda | correct | l16 |
| l17 | s7.explain | About 1.4 times Euler's limit; on a linear equation each RK4 step is exactly this polynomial, so the limit is exact | correct | script (h = 0.278 decays, 0.279 grows) |
| l17 | s8.prose | A method of order p has error about C h^p at a fixed time; halving h divides the error by 2^p | correct | HNW II.3 theorem 3.4 (for small h and a smooth right side) |
| l17 | s8.prose | Euler is order 1 with one evaluation a step; RK4 is order 4 with four; each has a stability limit on h lambda | correct | HNW II.1; HW IV.2 |
| l17 | s8.answer, hints, wrong | Error divided by 8 on halving means p = 3; 8 is the factor, not the order | correct | 2^3 = 8 |
| l17 | s9.prose, tests[4..6] | Seven RK4 steps on the oscillator reach 0.014164 within 5e-5; five do not | correct | script: errors 4.1e-5 (7 steps), 7.1e-5 (6), 1.3e-4 (5) |
| l17 | s9.widget.solution | rk4_step from the four slopes; rk4 with the same shape as euler | correct | script: 9 tests and 1 example pass, starter fails all 9; Pyodide |
| l17 | s9.canvas lines[1] | rk4_step(y' = y, h = 0.1) prints 1.1051708333333332 | correct | script; Pyodide |
| l17 | s9.canvas lines[3] | rk4(...)[1][-1] prints 2.7182797441351627 | wrong | the taught code gives 2.718279744135166 in CPython and Pyodide. Finding 3 |
| l17 | s9.tests[8] | One RK4 step on y' = -10y with h = 0.3 gives 1.375 | correct | R(3); script |
| l17 | s9.how | Tolerances 1e-9, 1e-10 for one step, 1e-12 for the integral of t^3 | correct | read from the test list |
| l17 | s9.explain | RK4 is exact for y' = t^3 because its weights are Simpson's rule | correct | for y' = f(t) the step is (h/6)(f0 + 4 f_mid + f1); Simpson is exact for cubics; script |
| l17 | s9.explain; hw i5.how | Euler would need about 16,000 steps on the oscillator for 5e-5 | correct | script: 16,019 by matrix powers |
| l17 | s10.prose | solve_ivp uses an adaptive RK45 pair by default | correct | SciPy: method='RK45', Dormand-Prince 5(4); script |
| l17 | s10.prose | It shrinks the step until each step's error estimate meets rtol and atol | correct | SciPy: local error kept below atol + rtol abs(y) |
| l17 | s10.prose | numerics lesson 11 builds that control | correct | numerics l11 text read (step-size controller from an error estimate) |
| l17 | s10.canvas lines[3] | `sol.y[0, -1]` prints 0.014164048945... | wrong | solve_ivp returns 0.0141640489531 (SciPy 1.18 and Pyodide's 1.14); 0.014164048945 is the closed form. Finding 2 |
| l17 | s10.canvas lines[5] | The closed form prints 0.014164048945404822 | correct | Python float (NumPy prints ...40483, the same number to 17 digits) |
| l17 | s10.widget.solution, how | oscillator_ivp passes 4 tests within 1e-8 of the closed form | correct | script; Pyodide |
| l17 | s10.explain | With rtol = 1e-10 the adaptive step keeps the error near 1e-11 | correct | script: 2.6e-12 to 1.05e-11 at t = 0.5, 1, 2, 3 |
| l17 | s10.explain | Testing against the closed form, not another solve_ivp run, is what makes the check mean something | correct | an independent reference is needed for validation (LeVeque appendix A.6) |
| l17 | s11.prose | x' = -40(x - theta): h lambda must stay under 2 for Euler and 2.7853 for RK4 | correct | rows above with lambda = 40 |
| l17 | s11.answer, hints, feedback | Fewest stable RK4 steps over the year: n > 40/2.7853 = 14.36, so 15; 14 steps give z = 2.857 | correct | script (14 steps a year grow, 15 decay) |
| l17 | s11.widget.wrong[euler], feedback, explain | 20 uses Euler's limit; Euler needs more than 20 | correct | abs(1 - 40/20) = 1 |
| l17 | s11.explain | A production pricer weighs order, cost per step and stability together | correct | statement of practice |
| l17 | summary | RK4 weights 1, 2, 2, 1; matches Taylor to h^4 on y' = y; error about C h^4; stable on y' = -lambda y only for h lambda < 2.7853; a slip is exposed only by the measured order | correct | rows above |
| l17 | q0 | One RK4 step on y' = -y, h = 0.1: 0.9048375; a linear equation is multiplied by the Taylor factor | correct | script |
| l17 | q1 | One midpoint step on y' = y, h = 0.2: 1.22; 1.2 is Euler | correct | script |
| l17 | q2 options, explain | Error 3.2e-6 at h becomes about 2e-7 at h/2; dividing by 4 or 2 is second or first order | correct | 3.2e-6/16 |
| l17 | q3 options[a], explain | RK4 on y' = -10y with h = 0.3 multiplies by 1.375 a step, so it grows; h lambda = 3 is past 2.7853 | correct | script |
| l17 | q3 options[1].why | Order is about small h | correct | HNW II.3 |
| l17 | q3 options[2].why, feedback.correct | "RK4's is R(-3) = 1.375" | imprecise | with the R(z) of screens[7] (z = h lambda = 3) the factor is R(3); R(-3) = 16.375 (script). R(-3) = 1.375 only in the numerics convention. Finding 4 |
| l17 | q3 options[3].why | Linear means the factor is an exact polynomial, not that it equals e^{-3} | correct | R(3) = 1.375 against e^{-3} = 0.0498 |

## l18-four-decimal-places

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l18 | s0.prose | With no noise, a five-year zero paying £100 is worth 100 e^{-I(5)}, I(5) the integral of r over [0, 5] | correct | deterministic short rate: P = exp(-integral of r) (BM 1.1) |
| l18 | s0.answer, hints, explain | I(5) = 0.236717; price £78.92 (£78.9215) | correct | script (quad) |
| l18 | s0.widget.wrong, feedback.byKey, explain | £81.87 discounts at 4% throughout, £74.08 at 6%; the price lies between | correct | script |
| l18 | s1.prose | I(T) = theta T + (r0 - theta)(1 - e^{-kappa T})/kappa | correct | integral of theta + (r0 - theta)e^{-kappa t}; script |
| l18 | s1.answer, hints, wrong | (1 - e^{-2.5})/0.5 = 1.835830; 0.917915 forgets to divide by kappa | correct | script |
| l18 | s1.explain | I(5) = 0.2 + 0.02 times 1.835830; D = 0.789215 | correct | script |
| l18 | s2.prose | The system (r, I)' = (kappa(theta - r), r) from (0.06, 0); Euler's I adds h times each r_n | correct | I' = r; script (caption formula equals Euler on the system) |
| l18 | s2.answer, feedback | Euler with 10 steps gives D = 0.788402, below the exact value | correct | script |
| l18 | s2.explain | 100 steps give 0.789134, 1,000 give 0.789207; the error falls tenfold per tenfold n: first order | correct | script |
| l18 | s3.prose | "Matching to four decimal places means abs(D_num - D) < 5e-5: then the printed 0.7892 agrees" | wrong | the band is a standard definition (BF 1.2), but the consequence is false: 0.789255 is 4e-5 from 0.789215 and prints 0.7893; 0.789151 prints 0.7892 and is outside the band (script). Finding 1 |
| l18 | s3.answer, hints, feedback, explain | The smallest n with Euler error below 5e-5 is 163: 50.02e-6 at 162, 49.71e-6 at 163 | correct | script: 163 is the smallest of all n, and every n from 163 to 399 stays inside |
| l18 | s3.hints[1] | The error is about 8.1e-3/n | correct | script: n times error = 8.10e-3 at n = 200 |
| l18 | s3.widget.wrong, feedback.byKey | At 100 steps the error is 81e-6 | correct | script |
| l18 | s4.canvas rows | RK4 with 1, 2, 4, 8 steps: 0.807298, 0.789608, 0.789229, 0.789216; errors 18083, 393, 13.9, 0.67 (times 1e-6) | correct | script |
| l18 | s4.answer, hints, feedback | Four steps is the first of the sequence inside the band | correct | script |
| l18 | s4.explain | Four steps are inside by a factor of 3.6; ten steps err by 2.6e-7; Euler needed 163 for what RK4 does in 4 | correct | script; 4 is also the smallest of all n (3 steps err by 5.3e-5) |
| l18 | s5.prose, canvas points | Euler errors: 0.00062 (2 steps), 0.00196 (4), then 1015.1, 508.2, 253.7 (times 1e-6) | correct | script |
| l18 | s5.options[a], hints, feedback, explain | One step size proves nothing; from 4 steps on each doubling halves the error; the 2-step error is small by cancellation | correct | script |
| l18 | s5.options[1].why | With 2 steps the rate overshoots below 4% and the errors in I cancel | correct | r1 = 3.5%; script |
| l18 | s5.options[2].why | With 2 steps h kappa = 1.25, factor -0.25 inside (-1, 1): stable, just coarse | correct | 1 - 1.25 |
| l18 | s5.options[3].why | First order once h is small | correct | script |
| l18 | s6.prose, canvas rows | Monthly Euler (n = 60) gives D = 0.789080, £78.9080 against £78.9215 | correct | script |
| l18 | s6.options[a], hints | D is off by 1.35e-4, outside the band | correct | script |
| l18 | s6.options[1].why, feedback.byKey.b | Four decimals is a statement about D; on £100 a 5p gap is 5e-4 in D, ten times the band | correct | 0.05/100 |
| l18 | s6.options[2].why, explain | Euler's error is proportional to h; it takes 163 steps, not 60 | correct | s3 |
| l18 | s6.options[3].why | h kappa = 0.0417, far inside Euler's limit of 2: accuracy, not stability | correct | 0.5/12 |
| l18 | s6.feedback.correct, explain | 0.789080 prints 0.7891 against 0.7892: the fourth decimal is wrong | correct | script; true of this value |
| l18 | s7.prose | With noise sigma the price gains a factor e^{Var(I)/2}, because e^{-I} is convex; here e^{4.643 sigma^2} | correct | I is Gaussian, so E[e^{-I}] = exp(-E[I] + Var(I)/2) (BM 3.2.1, with the drift taken as the pricing drift); Var(I)/sigma^2 = 9.2864; script |
| l18 | s7.prose, answer, hints | D = 0.789581, price £78.9581, £0.0367 above £78.9215 | correct | script: closed form and Monte Carlo (800,000 antithetic paths, exact OU steps: mean within 4 standard errors of 0.789581 and more than 6 above 0.789215) |
| l18 | s7.widget.wrong, feedback.byKey | Noise raises the price: averaging a convex function over paths lifts it | correct | Jensen's inequality |
| l18 | s7.explain | The no-noise system gives the expected rate path, not the expected discount factor; the gap is convexity | correct | E[r(t)] solves the drift equation; script (Monte Carlo mean of r(5)) |
| l18 | s8.lines s1 to s4, feedback, explain | Check: closed form first, doubling runs, stop when two successive runs agree within 5e-5 and the last is within 5e-5 of D, report n, value, tolerance | correct | LeVeque appendix A.6; consistent with s5 |
| l18 | s8.lines d1, why, feedback.byKey.d1 | Stopping at the first n within 5e-5 of D trusts one lucky grid | correct | s5 |
| l18 | s8.explain | Homework 4 codes exactly this | correct | hw i5 `match_to_4dp` reads so |
| l18 | s9.prose, widget.solution | `steps_to_4dp` doubles n from 1 until the method's D is within 5e-5 of the closed form | misleading | this is the rule s8 tells the learner to leave out (line d1), coded on the next screen with no word that it is only the search. Finding 8 |
| l18 | s9.widget.solution, prelude | vasicek_rhs, discount_exact, discount_rk4 are right; the prelude's discount_euler is Euler on the system | correct | script: 9 tests and 1 example pass, starter fails all 9; Pyodide |
| l18 | s9.canvas lines | 0.7892149197923242, 0.7892288673245939, 4 | correct | Pyodide prints exactly these |
| l18 | s9.feedback.correct, explain | In the doubling sequence RK4 meets the band at 4 and Euler at 256; Euler's true minimum is 163 but the sequence jumps from 128 to 256 | correct | script |
| l18 | s9.how | Tolerances 1e-9 and 1e-12; band check and step counts exact; hidden prelude | correct | read from the test list |
| l18 | s10.prose | The tests compare with the closed form, never with another solve_ivp run; its output changes slightly between SciPy versions | correct | tests read; last digits differ between SciPy 1.14 and 1.18 by 1e-16 |
| l18 | s10.canvas lines, explain | discount_ivp minus discount_exact is 1.78e-12; agreement to about 2e-12 in the browser's SciPy as on a desktop | correct | script: 1.7796e-12 (SciPy 1.18); Pyodide: 1.7797e-12 |
| l18 | s10.widget.solution, how | discount_ivp passes 4 tests within 1e-8 | correct | script; Pyodide |
| l18 | s11.canvas lines | Validation log: 0.789608 (3.9e-4), 0.789229 (1.4e-5), 0.789216 (6.7e-7), agree: yes | correct | script |
| l18 | s11.options, hints, feedback | Validate first on a case with a closed form, to a stated tolerance, with a doubling check | correct | statement of practice (benchmarking against an analytic case) |
| l18 | s11.options[1..3].why | A small step can hide a slip; two pricers can share a bug or a coarse grid; pence is the monthly-Euler trap | correct | l17 s6; l18 s6 |
| l18 | s11.explain | Every numerical pricer is first checked against a closed form; only then does it price anything that has none | correct | a norm of model validation, stated as the desk habit |
| l18 | summary.ideas | Four decimals means the band on D; Euler needs 163 steps, RK4 4; trust a method only after a doubling sequence converges and matches a closed form | correct | rows above |
| l18 | summary.trap | Monthly Euler prices within 2p, yet misses the fourth decimal of D | correct | 1.35p; 0.7891 against 0.7892 |
| l18 | q0 | With r0 = theta = 5%, D = e^{-0.25} = 0.7788; 0.75 is simple interest | correct | script |
| l18 | q1 options, feedback, explain | Only 0.789180 is within 5e-5 of 0.789215 (3.5e-5); the others miss by 8.1e-5, 1.35e-4, 7.5e-5 | correct | script |
| l18 | q2 | Error 8.1e-5 at 100 steps reaches 4e-5 at about 200; 142 assumes h^2 | correct | script (202.5 and 142.3) |
| l18 | q3 options, explain | 1.4e-5 at 4 steps becomes about 9e-7 at 8; the true figure is 6.7e-7 | correct | script |

## review-4

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| review-4 | i0 | L{t^3}(2) = 3!/2^4 = 0.375; 0.0625 drops the 3! | correct | script |
| review-4 | i1 | £2 a year growing at 3%, discounted at 5%, is worth 2/0.02 = £100; it exists because 0.05 > 0.03; 25 adds the rates | correct | script |
| review-4 | i2 | Y = 3/(s(s+3)) = 1/s - 1/(s+3), y = 1 - e^{-3t}; 3e^{-3t} inverts one factor only | correct | script (ODE solver) |
| review-4 | i3 | Y = (s+3)/((s+1)(s+2)): residues 2 and -1, y(1) = 2e^{-1} - e^{-2} = 0.6004; 0.8711 has the sign wrong | correct | script |
| review-4 | i4 | Euler on y' = -2y, h = 0.25: y_2 = 0.25 against e^{-1} = 0.3679 | correct | script |
| review-4 | i5.prose | A = [[-2, 1], [1, -2]] has eigenvalues -1 and -3; Euler multiplies each eigenvector by 1 + h lambda a step | correct | script; (I + hA)v = (1 + h lambda)v |
| review-4 | i5.question, answer | "The largest stable h" is 2/3 | imprecise | the stable steps are h < 2/3; at h = 2/3 the fast mode has factor -1 (script). Finding 5 |
| review-4 | i5.feedback, explain | Both abs(1 - h) < 1 and abs(1 - 3h) < 1 must hold; the fastest eigenvalue limits the step, the slowest sets the half-life | correct | script (h = 0.66 decays, 0.67 grows) |
| review-4 | i6 | RK4 error 4.8e-5 at 10 steps predicts 3e-6 at 20; 24 and 12 are first and second order | correct | 48/16 |
| review-4 | i7.prose | RK4 on y' = -lambda y is stable for h lambda < 2.7853 | correct | l17 s7; script |
| review-4 | i7.question, answer | "The largest stable h" for y' = -25y is 0.1114 | imprecise | the stable steps are h < 0.11141. Finding 5 |
| review-4 | i7.wrong, explain | Euler's limit is 2/25 = 0.08 | correct | arithmetic |
| review-4 | i8 | Monthly Euler misses by 1.35e-4; scaling n by 1.35/0.5 gives 162, the exact count is 163; 99 scales by a square root | correct | script |
| review-4 | i9 options, feedback, explain | The safe rule: two successive runs agree within 5e-5 and the last is within 5e-5 of the closed form; one run can be lucky; 5p is 5e-4; 100 Euler steps miss by 8.1e-5 | correct | l18 s5, s6, s8; script |

## homework-4

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-4 | i0 | L{t e^{-2t}}(1) = 1/(1+2)^2 = 0.1111; 1 forgets the shift | correct | script |
| homework-4 | i1.lines s1 to s5 | y'' - y = 0, y(0) = 0, y'(0) = 2: s^2 Y - 2 - Y = 0, Y = 2/((s-1)(s+1)) = 1/(s-1) - 1/(s+1), y = e^t - e^{-t} = 2 sinh t | correct | script (ODE solver) |
| homework-4 | i1.lines d1, why, feedback | s^2 Y - Y = 0 drops the starting values, which here are the whole solution | correct | l15 s5 |
| homework-4 | i2 | Y = (2s+3)/(s^2+2s+5) inverts to e^{-t}(2 cos 2t + (1/2) sin 2t); the no-half option forgets b = 2 | correct | 2s + 3 = 2(s+1) + 1; script |
| homework-4 | i3.prose | Eigenvalues -1 and -20: one factor reverts in weeks, the other in years | correct | half-lives ln 2/20 = 1.8 weeks and ln 2 = 0.69 years (time constant one year); script |
| homework-4 | i3.question, answer | "The largest stable Euler step" is 0.1 | imprecise | the stable steps are h < 0.1. Finding 5 |
| homework-4 | i3.feedback, explain | Each factor needs abs(1 + h lambda) < 1; the fast one forces h < 0.1, the slow one would allow 2; numerics lesson 12 calls this gap stiffness | correct | script; numerics l12 read |
| homework-4 | i4 | Fourth order predicts 2.084e-6/16 = 1.30e-7 for 20 steps; the true error is 1.358e-7, ratio 15.35; 10.42 halves it | correct | script |
| homework-4 | i5.prose, solution | `match_to_4dp` doubles n from 1 and returns the first (n, value) within tol of the previous run and of the closed form; the bond as (r, D)' = (0.5(0.04 - r), -rD) | correct | D' = -rD gives D = e^{-I}; script: 7 tests and 1 example pass, starter fails all 7; Pyodide |
| homework-4 | i5.how, feedback.correct | The bond needs 8 steps, the oscillator 16; a planted wrong closed form returns None | correct | script |
| homework-4 | i5.explain | "So it stops one doubling after RK4 first meets the band" | imprecise | true of the three tests (first in band at 4, 8, 8; stops at 8, 16, 16). Not a consequence: when the run before is within tol of the first run in the band the check stops there (script counterexample). Finding 9 |
| homework-4 | i5.explain | A wrong closed form never matches, and the cap returns None instead of looping for ever | correct | script |
| homework-4 | i6.model para 1 | Four decimals is abs(D_num - D) < 5e-5; monthly Euler errs by 1.35e-4, 2.7 times the band; prints 0.7891 against 0.7892 | correct | script |
| homework-4 | i6.model para 2 | The prices differ by 1.35p; 5p on £100 is 5e-4 in D, ten times the band; "within 5p" is a far weaker claim | correct | script |
| homework-4 | i6.model para 3 | Euler is first order: error about C h; about 162 steps, exact count 163 | correct | script |
| homework-4 | i6.model para 4, 5 | RK4's 4 steps err by 1.4e-5 and give 0.789229; the 4-step and 8-step runs agree within 5e-5; stop only on two agreeing runs and the closed form | correct | script: the two runs differ by 1.3e-5 |
| homework-4 | i6.rubric | Six rows: the band on D, the monthly error, why 5p is the wrong test, first order and about 163 steps, the fix, the note | correct | each row is a claim of the model answer above |
| homework-4 | i7.options, explain | £1 growing at 2% at 5% is worth 1/0.03; growth at 6% beats 5%; the default claim is £33.33; e^{t^2} beats every rate | correct | script |
| homework-4 | i7.feedback.correct | "The first and the third exist" | imprecise | a `multi` shuffles by default (AUTHORING), so the place words name the wrong options for most learners. Finding 10 |
