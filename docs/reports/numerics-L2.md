# numerics level 2 (Equations and curves): report

Author: content agent, 5 Nov 2026. Brief: `docs/briefs/numerics.md` section "Level 2".

## Files

| File | Screens or items | Canvases and widgets of note |
|---|---|---|
| `l5-bisection-and-newton.json` | 10 screens, quiz 4 | race table hook, secant chord explore (two points riding the curve, derived crossing), order tables for Newton (1.98, 2.00) and secant (1.50, 1.67), log10 plot of e(k+1) against e(k), `order` derivation of e(k+1) ≈ f''/(2f') e(k)² with a distractor, bond yield and 31 halvings, efficiency trap, code `bisect` + `secant` + `newton` + `observed_order`, 5,000-bond transfer |
| `l6-safe-root-finder.json` | 10 screens, quiz 4 | eleven-quote table (tap the two failing puts), 75 put price curve with a dragged start, tangent and live next iterate, safeguard rule on a number-line, `order` termination argument, 36-bisection cap, rounding trap (0.2124 against 0.2103), no-arbitrage edge case, code `safe_newton`, code `implied_vols` (vectorised, prelude supplies `bs_price` and `bs_vega`), market-maker transfer |
| `l7-interpolation.json` | 9 screens, quiz 3 | barycentric interpolant as one curve formula with `sum`, stepped by a `frames` control over n with the nodes; Chebyshev version; node-product curves with `prod`; Lebesgue constant; more-points trap; x³ edge case; code `lagrange_eval` + `max_interp_error`; vol-smile wiggle transfer |
| `l8-splines.json` | 10 screens, quiz 3 | three curves hook (straight lines, degree 7), live natural spline from eight draggable quotes (`derive` with `let` and `solve(A, rhs)` writing `params.M1..M8` and `y1..y8`, seven piece functions), tridiagonal row on a `matrix`, forward rates, bump trap read from the live caption, straight-line edge case, code `natural_spline_M` + `spline_eval` + `zero_price`, curve-scheme transfer |
| `review-2.json` | 10 items, difficulty 2 to 4 | all four lessons plus one item recalling l3 (wing conditioning, `r2-wing-cond`, tagged `nm-stability` too) |
| `homework-2.json` | 8 items, difficulty 3 to 5 | performance task `h2-ytm-book` (`performance: "code"`, difficulty 5, 6 tests against 1 example, starter fails); `order` derivation of the spline row; longform smile polynomial (10-point rubric, full model) |

Performance task: the l6 objective starts with "Build", so the level matches the verb rule. The task is the homework code item, `ytm_book`. The validator passes it and the set playthrough reports "1 performance starter fail".

## Gates (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; no warning on any level 2 file.
2. `VOICE_BASE=app/content/courses/numerics/ python3 docs/reviews/voice-scan.py`: 0 sentences over 20 words, 0 explanations over three sentences, across levels 1 and 2.
3. `python3 docs/reports/numerics-L2-numbers.py`: exits 0. Every code widget's solution passes its tests in CPython, and every starter fails at least one.
4. Playthrough with `--local-cdn`: all six files pass without flags and with `--mobile --tablet`. Lessons have 14, 14, 12 and 12 checks, with quizzes all right. Review 10 of 10; homework 8 of 8 (37 of 37 marks), the performance starter fails, and the longform is marked by the button. The `--why` shot of the l8 trap shows the live spline redrawn through the bumped quote, with the caption at 4.5622%.

SciPy: no hidden test imports SciPy. `brentq` and `CubicSpline` are named in prose, and their values are precomputed in the tests, so no load time applies. The brief asked to avoid SciPy where a test can.

## Numbers and their sources

Each figure was computed in CPython, then recomputed in the numbers script by a second route. Hand loops were checked against `scipy.optimize`, and mpmath at 40 digits was used for the Black-Scholes prices and roots. Hand barycentric sums were checked against `BarycentricInterpolator` and `np.polyfit`, and a hand tridiagonal solve against `CubicSpline`.

- l5: bisection midpoint errors 0.0858, 0.164, 0.0392, 0.0233; 40 halvings for 10^-12 from width 1; Newton errors 0.0858, 0.00245, 2.12e-6, 1.59e-12; secant 0.0809, 0.0142, 4.21e-4, 2.12e-6, 3.16e-10; first chord 4/3; orders 1.98, 2.00 (Newton), 1.50, 1.67 (secant); phi 1.618, √2 1.414; C = 1/(2√2) = 0.353553, measured 0.3333, 0.3529, 0.3535; bond yield 6.193228% (6.1932283%); Newton from 5%: 6.15487%, 6.193188%, 6.1932283%; 31 halvings on [0, 0.2]; 31/8 ≈ 3.9; call counts of the model solution 42 (bisection), 9 (secant), 6 (Newton).
- l6: quotes £0.0766, 0.0794, 0.1154, 0.2448, 0.6958, 2.5121, 0.6182, 0.0872, 0.0093, 0.0012, 0.0003; plain Newton from 0.2 jumps to 2,724 (75 put) and to 18.14 then −218 (80 put); the 85 put steps to 0.89; vega at 0.2 is 0.000028 (75 put) and 0.0044 (80 put); from 0.3 the next 75 put iterate is 2.53, from 0.5 it is 0.482, root 0.4806; safe solver 9 iterations with 1 bisection for the 75 and 80 puts, 2 to 8 with none for the rest; 36 bisections cap for [0.0001, 5] to 10^-10; 125 call: recovered 0.2124, smile 0.2103, vega 0.0218, 0.00005/0.0218 = 0.0023; bounds £5.3950 (95 call) and £9.5426 (110 put); x³ − 2x + 2 root −1.769292, plain Newton from 0 cycles 0, 1, 0; brentq agrees with the safe solver to 10^-10 on all eleven quotes.
- l7: maximum errors on a 20,001-point grid, equal spacing 0.4384, 1.0452, 1.9157, 59.82 (n = 4, 8, 10, 20); Chebyshev 0.4600, 0.2047, 0.1322, 0.0177; p10(0.95) = 1.9236, f(0.95) = 0.0424; Lebesgue constants 29.9 and 2.42 for 11 nodes; node product 0.00845 at 0.95 against 0.0000671 at 0.05 (ratio 126), Chebyshev product at most 2^-9 = 0.00195; vol wiggle 0.0292 (2.92 vol points) near strikes 76.6 and 123.4.
- l8: straight lines 3.925% and 4.475%; degree 7 gives 3.9103%, 5.1921% and −2.58% at 25 years; natural spline 3.9114% and 4.5297%; M (per cent per year squared) 0.1372, 0.0510, 0.0033, 0.0107, −0.0047, −0.0041; 5-year row diagonal 8, right side 0.15; spline forwards 4.0273% (4 years) and 5.2010% (15); straight-line forward 4.075% just below 5 years and 4.20% just above (the brief said 4.07% and 4.21%; the exact values are 3.95 + 5 × 0.025 and 3.95 + 5 × 0.05); zero-coupon price £85.5169 (spline) and £85.4704 (lines); a 10 bp bump at 5 years moves the spline 5.51 bp at 4 years, 6.42 at 6, −2.67 at 8.5 and +3.25 at 15 (4.5297% to 4.5622%).
- Review and homework: 30 halvings for 10^-9; wing vol 0.46 vol points per £0.0001 at vega 0.0218; forward 5%; 29 halvings for [0.0001, 5] to 10^-8; Newton efficiency 2^(2/3) = 1.587; M2 = −2 for (0, 0), (1, 2), (3, 2); 2.5 vol points per £0.0005 tick at vega 0.02; order 1.5 from 10^-2, 10^-3, 3.16e-5; zero-coupon yield (100/60)^(1/10) − 1 = 0.0524097791.

Pyodide against CPython: no stated value differed. Code tolerances: roots 1e-12 (l5) and 1e-9 or 1e-10 (l6, homework), implied vols 1e-6 against brentq, interpolation errors 1e-4, spline M 1e-10 and rates 1e-8, price £0.0001. Two timing cases ask for under 1 s on 1,000 strikes or 1,000 bonds; both passed in Pyodide in the playthrough.

## Choices that differ from the brief

- The l5 log-log picture plots log10 values on linear axes, as in level 1 (Backlog, level 1).
- The l5 explore is the secant chord, not Newton's tangent, which `taylor` l3 already drags.
- The ytm rule: yields are sought on [0, 1], so a price above the sum of the cash flows, which needs a negative yield, returns NaN for review. This is stated in the item.

## Proposed course.json change

None.

## Seeds and conventions

Homework timing case: `np.random.default_rng(3)`, 1,000 bonds with maturities 1 to 30, coupons 0 to 8% and yields 0.5% to 12%. Smile `σ(K) = 0.20 − 0.40 ln(K/100) + 2.0 ln²(K/100)`, one month, S = 100, r = 5%. Rates in per cent on canvases and as decimals in code. Generators are in the scratchpad folder `numerics-L2`.
