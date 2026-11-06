# numerics levels 1 to 3: second-reader findings

Scope: every lesson, review and homework file of `numerics` L1 to L3 (l1 to l12, review-1 to review-3, homework-1 to homework-3), against `docs/briefs/numerics.md` (L1 to L3), `docs/AUTHORING.md` and the reports `docs/reports/numerics-L1.md`, `-L2.md`, `-L3.md`.
Method: the three author scripts were run first. They read the lesson JSON only to run the code widgets, so prose, wrong-option values and `why` texts were checked here directly. Every stated number was recomputed independently (mpmath at 30 to 50 digits for floating-point errors, roots, Black-Scholes and the CIR closed form; `Fraction` for variances; SciPy `CubicSpline`, `BarycentricInterpolator`, `leggauss`, `solve_ivp` 1.18.1; NumPy 2.5.3), every code widget was rerun in a separate harness (solution passes, starter fails), and numeric tolerances were scanned for overlaps. Scripts are in the scratchpad folder `review-numerics` (`c_l2.py`, `c_l6.py`, `c_l11.py`, `codecheck.py`, `dump.py`).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak or misleading explanation, or teaching issue; note = small inconsistency or style.

Brief corrections claimed in the reports, checked:
- l8 straight-line forwards 4.075% (just below 5 years) and 4.20% (just above): correct, 3.95 + 5 × 0.025 and 3.95 + 5 × 0.05.
- l11 adaptive controller end error 2.4e-8 with the extrapolated value kept: correct (2.37e-8 from the lesson's own `adaptive_rk4` solution).
- l11 first step 0.069 and smallest step 0.0022: not correct for the lesson. The lesson's solution takes its first accepted step at 0.0701 and the smallest at 0.00207, which are the brief's 0.070 and 0.0021. The author's script uses a different scale in the step update (|y| after acceptance instead of the trial's |y_{h/2}|). Either way the smallest step is the last one, clipped to land on t = 0.95. See the l11 error below.
- l3 residual (0, −0.0001), corrected from the brief's +0.0001: correct.

## Level 1

- app/content/courses/numerics/l2-cancellation.json | screens[3] feedback.correct | error | "$8.27 \times 10^{-8}$: about seven of 16 digits are lost." A relative error of 8.27e-8 leaves 7.1 correct digits, so about nine of 16 are lost (mpmath: 8.269e-8). | "$8.27 \times 10^{-8}$: only about seven of 16 digits survive."
- app/content/courses/numerics/l2-cancellation.json | screens[1] option `none` why | error | "at $b = 10^5$ about seven are already lost": the measured relative error there is 10^-6.47, so about 6.5 digits are left and 9.5 lost. | "Digits go long before the last step: at $b = 10^5$ only about six correct digits are left."
- app/content/courses/numerics/l2-cancellation.json | screens[1] option `eight` why | error | "That is the total over the whole range": the error climbs from 10^-14.4 to 10^-0.6, about 14 digits in total; eight is the number of steps in k. | "Eight counts the steps in $k$. The whole range costs about 14 digits, two a step."
- app/content/courses/numerics/l2-cancellation.json | quiz q-book-variance (prose, explain, option `onepass` why) | error | With marks near £1bn moving "by a few thousand pounds a day" the variance is near 10^7, and the one-pass formula keeps 3 to 4 digits: 100 seeded runs of 250 days (iid moves, sd £3,000) gave a worst relative error of 2.6e-4 and never a negative value. The explain's "keeps almost nothing of a variance near $10^7$. It can even come out negative" and the why's "the spread is lost" are false. The author's own report changed homework-1's scenario for exactly this reason. | Prose: "A hedged book's daily mark-to-market sits near £1bn and moves by only a few pounds a day." Explain: replace "a variance near $10^7$" with "a variance near 10". The `onepass` and `float32` whys are then true as written.
- app/content/courses/numerics/homework-1.json | h1-expm1-kappa explain | error | "The seven digits lost to `exp(1e-10) - 1`": nine are lost, seven survive (as in l2 screens[3]). | "The nine digits lost to `exp(1e-10) - 1` were the algorithm's fault, which is why `expm1` exists."
- app/content/courses/numerics/review-1.json | r1-bump wrong `noroot` | error | Value 0.0089 matches no slip, so its why "You forgot the square root" never fires. Following the generic ("Multiply ε by 100, take the root, double it") without the root gives 2 × 2.22e-14 = 4.44e-14, that is 4.44e-7 in units of 10^-7. | `noroot` value 4.44e-7 with tol `{ "rel": 0.02 }`, or drop the entry.
- app/content/courses/numerics/l2-cancellation.json | screens[2] prose | warning | "$\sqrt{b^2 - 4}$ is within $10^{-8}$ of $b = 10^8$, and each carries an absolute error near $10^{-8}$": the gap is 2e-8, and b = 10^8 (and b² − 4) are stored exactly. Only the square root is rounded, by up to 7.45e-9, half the gap of 1.49e-8; that gives the 7.450581e-9 = 2^-27 result. | "$\sqrt{b^2 - 4}$ is within $2 \times 10^{-8}$ of $b = 10^8$. $b$ is exact, but the stored root can be off by $7.5 \times 10^{-9}$. Subtracting them keeps that error but shrinks the answer to $2 \times 10^{-8}$."
- app/content/courses/numerics/l2-cancellation.json | screens[3] wrong `abs` (0.0827) why | warning | "You stopped before multiplying by $10^8$" gives 8.27e-8, not 0.0827; the value is 8.27e-8 times 10^6. | "You multiplied by $10^6$, not $10^8$."
- app/content/courses/numerics/l4-stability.json | quiz q-lauchli-1e7 options `exact` and `garbage` whys | warning | "Squaring κ still costs about 14 digits" and "At 0.02 a couple of digits survive" describe the bound as the outcome. Measured: the normal equations return (1, 1) with errors −4.9e-15 and 5.1e-15, one digit lost, because this b has zero residual. | `exact`: "The bound $\kappa^2 u \approx 0.02$ allows 14 lost digits. NumPy loses about one here, but nothing promises all 16." `garbage`: "That needs $\kappa^2 u$ near 1. At 0.02 even the worst case keeps a couple of digits."
- app/content/courses/numerics/review-1.json | r1-float32-notional explain | warning | "Pennies added one at a time are rounded to a sixteenth of a pound": a penny is below half the £0.0625 gap, so adding one to £1,000,000 in float32 changes nothing. The penny vanishes. | "A penny is under half a gap, so adding one there changes nothing."
- app/content/courses/numerics/homework-1.json | h1-hex wrong `nobias` (value 0) | warning | No `byKey` entry (the only such gap in L1 to L3), and no slip gives 0: forgetting the bias gives 1.25 × 2^1026. | Drop the `nobias` wrong entry.
- app/content/courses/numerics/l2-cancellation.json | screens[6] hints[1] and option `tiny` why | note | The hint says "only about three digits of their difference are real", the why says "Only four digits of the price difference survive". The estimate 0.6324 against 0.636831 (error 4.4e-3) has two correct digits. | Hint: "...so only about two digits of their difference are real." Why: "Only about two digits of the price difference survive, so delta is 0.6324."
- app/content/courses/numerics/l4-stability.json | quiz q-lauchli-1e7 option `nan` text | note | "`nan`, as at ε = 10^-8" holds in the app's Pyodide NumPy 2.0.2 (AUTHORING section 3), but desktop NumPy raises `LinAlgError` there (checked, NumPy 2.5.3). | "`nan` or an error, as at $\epsilon = 10^{-8}$"
- app/content/courses/numerics/l4-stability.json | screens[2] hints[2] | note | "Its sum is accurate to $u$ in relative terms": a sum of about 60 positive terms is good to a few u, not u. | "Its sum is accurate to a few $u$ in relative terms, and $1/x$ has $\kappa = 1$."
- app/content/courses/numerics/homework-1.json | h1-book-variance model, **Fix** paragraph | note | "the one-pass formula gave 0 half the time. Otherwise it swung between −263 and 263" is seed-specific and not reproducible from the text: a rerun (Python `random`, seed 7, sd £3, 250 days, 200 years) gave 0 in 73 years and −257 to 257 otherwise. | "the one-pass formula often gave exactly 0. Otherwise it swung by a few hundred either way."

## Level 2

- app/content/courses/numerics/l5-bisection-and-newton.json | screens[0] option `secant` why and explain | error | "It needs one more step" and "The secant method needs step 5 or 6": the secant errors are 3.16e-10 at step 5 and 2.37e-16 at step 6, so it reaches 12 digits at step 6, two steps after Newton's step 4. | Why: "It is fast, but each step multiplies the digits by about 1.6, not 2. It needs two more steps." Explain: "The secant method needs step 6".
- app/content/courses/numerics/l6-safe-root-finder.json | screens[4] wrong `w33` | error | Value 33 with why "That treats the width as 1": from width 1 the bracket needs $2^k > 10^{10}$, so 34 halvings ($2^{33} = 8.6 \times 10^9$ is too few). The misconception never fires. | `w33` value 34 (id may stay or become `w34`, with the `byKey` key renamed to match).
- app/content/courses/numerics/l6-safe-root-finder.json | screens[3] order lines t4 and t5 | warning | "the stopping rule caps the Newton steps between bisections": no rule does that. A run of Newton steps that stays inside the bracket triggers no bisection, so the bisection count alone does not prove the method ends. The solution ends through `maxit`, the xtol step test or `ftol`. | t4: "Every bisection halves it, and the cap `maxit` ends any long run of Newton steps." t5: "So the method ends: by xtol after at most $\lceil \log_2(\text{width}/\text{xtol}) \rceil$ bisections, or at the cap."
- app/content/courses/numerics/review-2.json | r2-safeguard | warning | The solver "has bracket [0.1, 0.9] and is at σ = 0.3", with 0.3 inside the bracket. In l6's algorithm the bracket is first updated with f(0.3), so the midpoint is that of [0.3, 0.9] (for the 75 put f(0.3) < 0), which is 0.6. As written, a learner who follows l6 gets 0.6 and is marked wrong. | Prose: "A safeguarded Newton solver has just evaluated $f$ at $\sigma = 0.3$, and its bracket is now $[0.3, 0.9]$. The Newton step would land at 2.53." Option `ok`: "Bisect: move to 0.6, the middle of the bracket". feedback.correct: "Bisect, to 0.6." Explain: "The Newton step leaves $[0.3, 0.9]$, so the solver bisects to 0.6."
- app/content/courses/numerics/l8-splines.json | quiz q-natural option `third` why | warning | "That is the not-a-knot idea": not-a-knot makes the third derivative continuous at the second and second-last knots. A zero third derivative at the ends makes the end pieces parabolas, another condition. | "Zero third derivative makes each end piece a parabola. Natural ends set $M_1 = M_n = 0$ instead."
- app/content/courses/numerics/l5-bisection-and-newton.json | screens[6] explain | note | "Newton reached 7 correct digits in 3 steps": the third iterate 6.1932282681% has relative error 7.1e-12, about 11 digits. | "Newton reached about 11 correct digits in 3 steps."
- app/content/courses/numerics/l5-bisection-and-newton.json | screens[9] prose | note | "Bisection on $[0, 0.2]$ needs 31." counts halvings, but screen 8's explain counts two more calls for the ends (33 evaluations, ratio 4.1). | "Bisection on $[0, 0.2]$ needs 31 halvings, one evaluation each, after checking the ends."
- app/content/courses/numerics/review-2.json | r2-efficiency explain | note | "When $f'$ is cheap, Newton wins back the lead" clashes with homework-2 h2-efficiency ("Even with a cheap derivative the secant method's 1.618 edges ahead"). Newton wins only when $2^{1/(1 + c)} > 1.618$, that is when $f'$ costs under 0.44 of $f$. | "Newton wins back the lead only when $f'$ costs under about 0.44 of $f$."
- app/content/courses/numerics/l7-interpolation.json | screens[3] explain | note | "The other factors of the error are the same for both node sets": $f^{(n+1)}(\xi)$ depends on ξ, which depends on the nodes. | "The derivative factor has the same bound for both node sets."

## Level 3

- app/content/courses/numerics/l11-step-size.json | screens[4] explain | error | "The steps shrink from 0.069 to 0.0022 as the curve steepens." The lesson's own `adaptive_rk4` solution (screens[7]) takes its first accepted step at 0.0701 and its smallest controller-chosen step at 0.0043. The 0.0021 is the last step, clipped to land on t = 0.95, not a response to steepness. The author's figures come from a controller variant in `numerics-L3-numbers.py` that scales by |y| after acceptance. The canvas dots (s1 at 0.06864) come from that variant too. | "$39 \times 12 = 468$, as the steps shrink from 0.070 to 0.0043. The last is cut to 0.0021 to land on 0.95. Fixed-step RK4 needs about 400 steps, 1,600 evaluations, for $7 \times 10^{-8}$." Regenerate the dots from the screens[7] solution, and change the script's checks to 0.070 and 0.0043.
- app/content/courses/numerics/l9-quadrature.json | screens[0] explain and wrong `n2`, screens[1] canvas row and hint | note | The trapezium error at n = 2 is 0.035649, which rounds to 0.0356, not 0.0357 (the ratio stays 3.99). | Replace 0.0357 with 0.0356 in all five places.
- app/content/courses/numerics/l9-quadrature.json | screens[6] hints[2] | note | The split Simpson error at n = 128 is 1.9248e-6. | "$1.93 \times 10^{-6}$" to "$1.92 \times 10^{-6}$".
- app/content/courses/numerics/l11-step-size.json | quiz q-floor feedback.correct | note | The prose puts the flattening "at about $10^{-14}$", the feedback "near $10^{-15}$". | "Rounding sets a floor near $10^{-14}$."
- app/content/courses/numerics/l12-stiff-equations.json | summary.trap | note | "rings between 4% and 8%": the path dips to 3.9891%. | "...rings between about 4% and 8%."
- app/content/courses/numerics/homework-3.json | h3-trap-n explain | note | "Simpson would reach it at $n = 32$" assumes Simpson also starts from 0.02 at n = 8. | "Simpson, from the same starting error, would reach it at $n = 32$, which is why order matters more than effort."
- app/content/courses/numerics/course.json | levels[2].requires `odes/L4` | note | odes L4 (Euler and Runge-Kutta) is not written yet, so numerics L3 stays locked. l11 screens[0] says "`odes` showed these orders" and l12 assumes Euler's method from it. Neither can be checked until odes L4 lands. | No change now; recheck l11 and l12 against odes L4 when it is written.

## Checked and correct

Level 1: the 52 halvings and $2^{-52}$; the toy format's 32 numbers and gaps; the bit grids of −6.5 (`0xC01A...`) and 100.25 (`0x4059 1...`); `decode(0.1)` = (0, −4, 0.6000000000000001); the spacings 1.42e-14 and 1.16e-10; $2^{53}$; eps/tiny ≈ 10^292; float32 gap 0.001953125 and 20,000.009765625; 256 ns; $e^{710}$ = 2.234e308. The textbook root 2^-27 = 7.450581e-9 (25.5%); expm1 error 8.269e-8; one-pass 0.0 and 29.33; the forward and central difference tables; h* = 2.98e-8 and 7.03e-7; the call £10.450584, delta 0.636831, gamma 0.0187620, vega 37.52; the bumped deltas and gammas; log(1 + 1e-12) = 1.000089e-12. σ = 2.00005 and 4.999875e-5, κ = 40,002.00007; 28,285; Hilbert 1.5258e10; the 60 put £0.01129 and vega 0.5882 (1.70 and 8.5 vol points, ratio 63.8). The series 6.147561828914626e-9 (198.3%), largest term 4.31e7 and 16.3 decades; the Läuchli determinant, κ = 1.414e8 and 16.3 digits; the yield design κ 2.98e4, 8.88e8 and 13.3. Review and homework: 0.01 = 1.28 × 2^-7; 30^30/30! = 7.76e11 against e^-30 = 9.36e-14; 2^24; (48ε)^(1/4) = 3.21e-4; naive float32 pennies £9,865.22.

Level 2: Newton, secant and bisection error sequences; orders 1.98, 2.00, 1.50, 1.67; C 0.3333, 0.3529, 0.3535 and 0.353553; the bond yield 6.1932283% and Newton's iterates; 31 and 40 halvings; the eleven quotes, V(0.2) and vega columns, 2,724, 18.14 and −218; 2.53 from 0.3 and 0.482 from 0.5; the implied vols against the test list to 1e-10; the bounds £5.3950 and £9.5426. Runge errors on both node sets (20,001 and 200,001 points), p10(0.95) = 1.9236, Lebesgue 29.90 and 2.42, node products and ratio 126, the alternating-error swing 0.0292 near strike 76.6. The spline M values, the tridiagonal rows and right sides, 3.9114% and 4.5297%, forwards 4.0273% and 5.2010%, degree-7 readings including −2.58%, the bump responses 5.51, 6.42, −2.67 and 3.25 bp, and the prices £85.5169 and £85.4704.

Level 3: the trapezium and Simpson tables, the 0.00895 prediction, Richardson = S8 = 1.7182841547, the kink and split error sequences, the Gauss split and unsplit errors, the tail 2.5036e-13, the [K, 200/300/400] truncations, the polynomial payoff 10/3. CIR γ, B(5), A(5) and £79.1020; the Euler and RK4 error tables; C, h = 0.0773, n = 65 (error 8.19e-9), Richardson −1.10e-6 against −9.84e-7; 38 accepted, 1 rejected, 468 evaluations, end error 2.4e-8; fixed RK4 at 400 steps 7.05e-8. The two-speed model's exact r(1), the Euler caption formula and its values, the implicit Euler and trapezoidal paths, factors at z = −2.5, solve_ivp counts 1,172, 422 and 226 (SciPy 1.18.1). Homework: the spread £4.410495, digital £0.532325 and forward £4.877058.

Grading: every code solution passes its hidden tests and every starter fails at least one (independent harness, CPython; l3 and l4 starters pass one source-text test each). No numeric answer and wrong value overlap within tolerance in L1 to L3. Voice: `voice-scan.py` on the course gives 0 sentences over 20 words and 0 explanations over three sentences; no em-dashes, exclamation marks, American spellings or dollar amounts found. Teaching order follows each brief; the hooks name the secant method (l5) and the bump model (l2) one screen before defining them, which is acceptable for a predict-first hook.

## Process note

The three author scripts read the lesson JSON only to run code widgets. All nine errors above sit in prose, `why` texts and wrong values, which no script checked. This is the third second read this session with the same finding class. Under SESSION PROTOCOL 6 it should become a rule before the next wave: for example, each numbers script asserts every figure it checks against the JSON text that states it, and a validator rule flags a numeric `wrong` entry whose `byKey` text has no number matching its value.

## Counts

- errors: 9
- warnings: 8
- notes: 14
- Author scripts: `python3 -I docs/reports/numerics-L1-numbers.py` exit 0, `numerics-L2-numbers.py` exit 0, `numerics-L3-numbers.py` exit 0.
- Validator: 0 errors.

## Fix pass

Every changed value was recomputed twice (author scripts extended with mpmath references, plus a second ad hoc check); the l11 figures come from the lesson's own `adaptive_rk4`.

Level 1
- l2 screens[3] feedback.correct: fixed ("only about seven of 16 digits survive"; 8.27e-8 gives 7.08 digits left).
- l2 screens[1] `none` why: fixed (about six correct digits left at b = 10^5; measured 10^-6.47).
- l2 screens[1] `eight` why: fixed (14 digits over the range).
- l2 q-book-variance: fixed (prose "a few pounds a day", explain "variance near 10"; one-pass is wrong in most seeded runs there, and under 1e-3 at £3,000 moves, so the old text was false).
- homework-1 h1-expm1-kappa: fixed (nine digits lost).
- review-1 r1-bump `noroot`: fixed (value 4.44e-7, rel 0.02; the old 0.0089 matched no slip).
- l2 screens[2] prose: fixed (gap 2e-8, b exact, root off by up to 7.5e-9).
- l2 screens[3] `abs` why: fixed ("multiplied by 10^6, not 10^8").
- l4 q-lauchli-1e7 `exact` and `garbage` whys: fixed (NumPy loses about one digit here, bound allows 14).
- review-1 r1-float32-notional explain: fixed (a penny changes nothing).
- homework-1 h1-hex `nobias`: fixed by dropping the entry.
- l2 screens[6] hint and `tiny` why: fixed (two digits).
- l4 `nan` option text: fixed ("`nan` or an error").
- l4 screens[2] hints[2]: fixed ("a few u").
- homework-1 h1-book-variance model: fixed (seed-neutral wording).

Level 2
- l5 screens[0] `secant` why and explain: fixed (two more steps, step 6; errors 3.16e-10 and 2.37e-16 in mpmath).
- l6 screens[4] `w33`: fixed (renamed `w34`, value 34, byKey key renamed; 2^33 = 8.6e9 is too few from width 1).
- l6 order lines t4 and t5: fixed as suggested.
- review-2 r2-safeguard: fixed (bracket [0.3, 0.9], bisect to 0.6; graded option text and feedback changed, option id `ok` unchanged).
- l8 q-natural `third` why: fixed.
- l5 screens[6] explain: fixed (about 11 digits; relative error 7.1e-12).
- l5 screens[9] prose: fixed (31 halvings after checking the ends).
- review-2 r2-efficiency explain: fixed (under about 0.44 of f; 1/log2(1.618) - 1 = 0.4405).
- l7 screens[3] explain: fixed.

Level 3
- l11 screens[4] explain: fixed (0.070, 0.0043, last step cut to 0.0021; lesson controller gives first 0.07010, smallest controller step 0.004341, last 0.002067, 38 accepted, 1 rejected, 468 evaluations, end error 2.37e-8). Dots s0 to s38 on screens[4] and [7] regenerated from that run. Script `numerics-L3-numbers.py` now uses the lesson's controller and checks 0.070, 0.0043, 0.0021 and the dots.
- l9 0.0357 to 0.0356 in all five places: fixed (script tolerance table updated; 0.035649).
- l9 screens[6] hints[2]: fixed (1.92e-6; script row changed from 1.93e-6 and a rounding check added, the old 0.5% tolerance had hidden it).
- l11 q-floor feedback: fixed (near 10^-14).
- l12 summary.trap: fixed ("about 4% and 8%").
- homework-3 h3-trap-n explain: fixed.
- course.json levels[2].requires `odes/L4`: deferred (no change allowed; recheck l11 and l12 when odes L4 lands).

Process note (SESSION PROTOCOL 6 rule for scripts asserting figures against the JSON text): deferred to the orchestrator as an engine item. Disputed: none.

Graded answers changed: none by value. Wrong-option values changed: review-1 r1-bump `noroot` 0.0089 to 4.44e-7; l6 `w33` 33 to `w34` 34; homework-1 h1-hex `nobias` removed. review-2 r2-safeguard correct option text now "0.6" (id `ok` unchanged).

Gates: `node tools/validate.mjs` 0 errors; `python3 -I docs/reports/numerics-L1-numbers.py`, `-L2-`, `-L3-` all exit 0; playthrough `--lesson` for l2, l4, l5, l6, l7, l8, l9, l11, l12 and `--set` for homework-1, homework-3, review-1, review-2, desktop and mobile, all "All passed."
