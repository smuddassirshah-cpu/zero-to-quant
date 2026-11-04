# Answer check, pdes level 3 (3.2)

Independent recomputation of every keyed answer, tolerance, slip value, stated number and code test in `app/content/courses/pdes/` for `l9-black-scholes-to-heat`, `l10-formula-from-the-kernel`, `l11-feynman-kac`, `l12-four-decimal-pricer`, `review-3` and `homework-3`. Each value was worked from the question text alone. The author's scripts and `docs/reports/pdes-3.md` were not read. Scripts are in the scratchpad folder `ac-pdes3` (`calc1.py`, `vasicek.py`, `fd.py`, `fd2.py`, `fd3.py`, `simp.py`, `walk.cjs`, `mc.py`, `code_check.py`, `expr.cjs`, `scan.py`, `reuse.py` and the smaller files named below).

Second routes used:

- SciPy `quad` of the heat-kernel integral for every heat value (u(0, 0.02) = 0.111107 and price 10.450584; the c = 1 kernel 0.071030 and price 6.680959; u(0.2, 0.02) = 0.347148; u(0.2, 0.0005) = 0.259081; the put by the kernel over y < 0, 5.573526; the call at S = 110, 17.662954). Black-Scholes closed form for every price quoted (with `scipy.stats.norm`).
- The engine's own Simpson readout (400 intervals on [0, 5], `plane.js` `simpson`) replicated in `simp.py` for the l10 caption: 10.45059 at c = 2, 6.68096 at c = 1, 17.66206 at x0 = 0.0953.
- The l11 walk canvas replicated from `walk.js` (mulberry32 seed 3, run 0, 2,000 paths, 50 steps, `exp(-r*T)*max(exp(x)-K,0)` overlay): mean 10.32502, standard error 0.32559, so the readout is £10.33 with £0.33. Runs 1 to 4 give 10.398, 10.038, 10.647, 10.379.
- Seeded NumPy runs for every Monte Carlo figure (seed 11: 10.453355, 0.046462; digital 0.531975; real drift 12% 15.534329; undiscounted 10.989309; seed 5: 1.500126 and 2.501607; a million draws at 8% drift with seed 11: 12.473527).
- Vasicek: affine closed form (0.789581, and 0.880706 for the homework bond), deterministic-rate price (0.789215, 0.880498), Crank-Nicolson solve of the bond PDE on a 1,600 by 2,000 grid (0.7895815, 0.8807062), and `default_rng(21)` with 500 steps and 20,000 paths (mean 0.789530, standard error 0.000171; all 200 running means of the chart agree to 5e-7). The homework simulation reproduces with `default_rng(7)`, 300 steps and 200,000 paths (0.880800, 0.0000428).
- My own finite-difference code (`fd.py`, written from the equations, `scipy.linalg.solve_banded` for the tridiagonal solves): explicit scheme, Crank-Nicolson, Rannacher start, Richardson, boundary shifts, odd grids, S grid, put, second-difference gamma. A dense `np.linalg.solve` at 400 by 80 agrees with the author's Thomas test value to 1e-14.
- Every code solution run in CPython with NumPy under the engine's rules (prelude, solution, `isclose` with the item's `abs`, `raises` by class name). Starters run the same way.
- Every expression widget graded by the repo's own `grade.js` (`exprEqual`) with Compute Engine 0.30.2 from the scratchpad `pkgs`: the key, 12 to 14 forms a learner would type per widget (fraction, `\frac`, `\cdot`, `\left(` brackets, `\frac12`, decimals, expanded forms, implicit products such as `\sigma^2(T-t)`) and six differing forms per widget including every `wrong` expression. All 4 widgets: 0 failures.
- A structural scan of all 76 widgets (`scan.py`): wrong values inside the answer tolerance, answer inside a wrong tolerance, wrong values overlapping each other, `byKey` keys naming nothing, wrong ids without feedback text, choice and multi correct counts, order ids against lines, table cell ids against `byKey`, literal backslash-n in every string, option lengths. A grep of every numeric key and slip against the twelve pdes lessons and both earlier level sets (`reuse.py`).

**Summary.** All 76 widgets were recomputed (40 numeric, 12 choice, 4 expression, 6 order, 6 code with 41 hidden tests and 6 examples, 3 multi, 3 table with 12 editable cells, 1 slider, 1 longform; 79 slip entries). Every key is right, every tolerance holds my value, no slip lies inside an answer tolerance and no two slips overlap. Every code solution passes all its tests and every starter fails them (the homework starter passes only the visible `bs_put` example, no hidden test). Every figure the author reports for the finite-difference lesson reproduces: the explicit prices at 110, 100, 96 and 90 steps, the boundary shifts 4e-11 (±1.5) and -3.2e-6 (±0.5), the error ratios 3.99, 3.97, 3.94, 3.88, the odd-grid error order h^2 with a larger constant, the walk readout, and the Richardson error 7.6e-6. Three items need a fix (errors 1 to 3): a false "30% multiplies by 2.25", a false subtraction behind the l10 call at S = 110, and a feedback line that double counts the odd-grid error. Fourteen items need a decision or a small edit (warnings 4 to 17), mostly repeats of lesson numbers in the homework and a hidden test that is fragile in floating point. Twelve are notes (18 to 29).

## Widgets checked

Numeric rows give the key and tolerance, then my value and my value for each named slip. `ok` means my value lies inside the key's tolerance and each slip value lies inside its stated value's tolerance. Slips not shown are 0 or the quoted number.

| File | Screen or item | Key | My value | Verdict |
|---|---|---|---|---|
| l9 | screen[0] | choice back | data sit at t = T, so solve backwards; fwd and either false | ok; key 58 against 46 and 38 (warning 16) |
| l9 | screen[1] | expression sigma^2 (T-t)/2 | V_t = -cV_tau, coefficient sigma^2/(2c) = 1; CE: 13 typed forms equal; `forward` sigma^2 t/2 and `no-half` sigma^2 (T-t) differ | ok |
| l9 | screen[2] | order c1..c4; d1, d2 | V_S = (K/S) v_x, V_SS = (K/S^2)(v_xx - v_x); chain is strict; d1, d2 false as `why` says | ok |
| l9 | screen[3] | expression 2r/sigma^2 | 0.10/0.04 = 2.5; CE: 12 forms equal (`2r\sigma^{-2}`, `\frac{r}{\sigma^2/2}`, ...); `no-two`, `inverted` and 3 more differ | ok |
| l9 | screen[4] | numeric 1.5, abs 0.001 | k - 1 = 1.5 (slips: dropped 2.5; only-chain -1) | ok |
| l9 | screen[5] | expression -(k-1)/2 | 2 alpha + (k-1) = 0; CE: 14 forms equal; `sign`, `no-half` and 4 more differ | ok |
| l9 | screen[6] | expression -(k+1)^2/4 | beta = alpha^2 + (k-1) alpha - k = -(k+1)^2/4; k = 2.5 gives -3.0625; CE: 12 forms equal; `no-k`, `sign` and 4 more differ | ok |
| l9 | screen[7] | numeric 10.4506, abs 0.0006 | 100 e^(-0.06125) x 0.111107 = 10.450584 (quad and closed form; slips: no-factor 11.110691; wrong-sign 11.812494); canvas dot 0.1111 | ok; accept text (note 18) |
| l9 | screen[8] | numeric 7.9656, abs 0.001 | 100(2 Phi(0.1) - 1) = 7.965567; B has sigma^2 T = 0.04 as well (slips: double 15.931135; half 3.982784) | ok |
| l9 | screen[9] | code: heat_params, to_heat, price_from_u; 7 tests + example | solution 8/8; starter 0/8; (2.5, -0.75, -3.0625), (0.96, 0.02, -0.9604), 0.095310, 10.450584, 24.496059 | ok |
| l9 | screen[10] | multi a, b | sigma^2 T: a 0.16 x 0.25 = 0.04, b 0.01 x 4 = 0.04; c 0.08, d 0.02 | ok |
| l9 | quiz[0] q-tau | numeric 0.09, abs 0.0006 | 0.5 x 0.09 x 2 = 0.09 (slips: no-half 0.18; one-year 0.045) | ok |
| l9 | quiz[1] q-coeff | numeric -0.04, abs 0.0006 | k = 0.96, k - 1 = -0.04 (slips: dropped 0.96; k-plus 1.96); alpha 0.02 | ok |
| l9 | quiz[2] q-beta | numeric -0.9604, abs 0.0006 | -(1.96)^2/4 = -0.9604 (slips: no-k -0.0004; half-k -0.2304) | ok |
| l9 | quiz[3] q-backward | choice ill | tau = sigma^2 t/2 gives u_tau = -u_xx, backward heat | ok; key 78 against 51 and 25 (warning 16) |
| l10 | screen[0] | numeric 10.4506, abs 0.0006 | Simpson readout 10.45059 (area 0.111107); slip area 0.1111 | ok |
| l10 | screen[1] | order l1..l4; d1, d2 | -(y-x-2a tau)^2/(4 tau) + a x + a^2 tau expands back to a y - (y-x)^2/(4 tau); mean x + 2a tau, variance 2 tau; d1, d2 false | ok |
| l10 | screen[2] | table 0.35, 0.6771, 0.15, 0.5659 | arguments 0.2a = 0.35, 0.15; I(1.75) = 0.677056, I(0.75) = 0.565949 (abs 0.002 and 0.0008) | ok; explain subtraction (note 19) |
| l10 | screen[3] | order t1..t5; same t3, t4, t5; d1, d2 | alpha + a1 = 1, beta + a1^2 = 0, alpha + a2 = 0, beta + a2^2 = -k all hold; t3, t4, t5 are independent after t2 | ok |
| l10 | screen[4] | numeric 17.66, abs 0.015 | 17.662954 (slips: same-x 10.45 vs 10.450584; no-disc 14.08 vs 14.0806 exact, 14.088 from rounded Phi) | key ok; explain arithmetic (error 2) |
| l10 | screen[5] | slider c = 2, tol 0.1; wrong 0.8 to 1.2 | canvas price at c = 2: 10.4506; c = 1: 6.6810 (6.680959); 36.07% low; c = 1.9 reads 10.0962, c = 2.1 reads 10.8018 | key ok; tolerance too wide (warning 5) |
| l10 | screen[6] | numeric 0.2572, abs 0.004 | e^0.35 - e^0.15 = 0.257233 (slips: wide 0.347148); at tau = 0.0005 the area is 0.259081 (0.2591 quoted); payoff 22.1403 | ok |
| l10 | screen[7] | numeric 5.5735, abs 0.0006 | 10.450584 - 100 + 95.122942 = 5.573526 (kernel over y < 0 also 5.573526; slip undiscounted 10.4506) | ok |
| l10 | screen[8] | code: call_via_kernel, bs_call; 7 tests + example | solution 8/8; starter 0/8; kernel 10.450583 (key 10.450584, diff 1.4e-6 of 5e-5), 17.662953, 1.766906 | ok |
| l10 | screen[9] | numeric 2661.6, abs 1 | 5000 e^-0.05 x 0.559618 = 2661.624 (slips: no-disc 2798.088; hedge 3184.153) | ok; accept text (note 20) |
| l10 | quiz[0] q-arg | numeric 0.85, abs 0.006 | (0.1 + 0.07)/0.2 = 0.85 (slips: no-shift 0.5; no-root 4.25) | ok |
| l10 | quiz[1] q-width | numeric 0.4, abs 0.006 | sqrt(0.16) = 0.4 (slips: tau 0.2828; variance 0.16) | ok |
| l10 | quiz[2] q-put | numeric 2.7859, abs 0.0006 | 17.662954 - 110 + 95.122942 = 2.785896 (slip undiscounted 7.66295) | ok |
| l10 | quiz[3] q-d2 | choice exercise | Phi(d2) is the risk-neutral exercise chance | ok |
| l11 | screen[0] | choice settle | canvas run 0: 10.32502, standard error 0.32559; five runs lie within 1.3 standard errors of 10.4506 on both sides | ok; key 70 against 43 and 32 (warning 16) |
| l11 | screen[1] | numeric 1.5, abs 0.001 | x^2 + t = 1.5 (slips: no-noise 1; t-only 0.5); seeded 1.500126, 0.005003 | ok |
| l11 | screen[2] | order f1..f5; d1, d2 | dM = e^-rs (V_t + mu V_x + sigma^2 V_xx / 2 - rV) ds + ...; strict chain | ok |
| l11 | screen[3] | choice bs | mu = rS, sigma(S) = sigma S | ok |
| l11 | screen[4] | numeric 0.33, abs 0.01 | 0.046462 x sqrt(50) = 0.3285 (slips: linear 2.325; inverse 0.006576) | ok |
| l11 | screen[5] | choice rn | real 12% on the seed-11 draws 15.534329; exact 15.526075; 48.6% above 10.4506 (quoted 49%); forward 105.1271 | ok; key 78 against 60 and 50 (warning 16) |
| l11 | screen[6] | numeric 10.9864, abs 0.002 | 10.450584 e^0.05 = 10.986396; sample 10.989309 (quoted 10.9893) | ok |
| l11 | screen[7] | numeric 2.1, abs 0.1 | (0.7895815 - 0.7892149)/0.000171 = 2.143 (slip mc-gap 0.301) | ok |
| l11 | screen[8] | numeric 4.8771, abs 0.0006 | 100 - 100 e^-0.05 = 4.877058 (slips: undisc 5.1271; vol 10.4506); vol adds 5.573526 | ok |
| l11 | screen[9] | code: mc_price, heat_mc, vasicek_bond_mc; 7 tests + example | solution 8/8; starter 0/8; 10.453354512, 0.046461812; 0.531975056, 0.001493436; 1.500125868, 0.005003376; 2.501606655, 0.012430746; 0.7892149; MC within 4 standard errors, standard error 0.000171 | ok |
| l11 | screen[10] | numeric 20, abs 0 | 100^10 = 10^20 (slips: ten 10; one-asset 2) | ok |
| l11 | quiz[0] q-cube | numeric 2.5, abs 0.001 | x^3 + 3xt = 2.5 (slips: no-noise 1; cross 1.5) | ok |
| l11 | quiz[1] q-digital | numeric 0.354, abs 0.002 | d2 = -0.32655, Phi 0.372004, price 0.353861 (slip undisc 0.372004) | ok |
| l11 | quiz[2] q-drift | choice wrong | expected payoff 15.526 at 12% drift | ok; key 72 against 53 and 52 |
| l11 | quiz[3] q-sigma0 | choice ode | only first derivatives remain | ok; key 64 against 33 and 40 (warning 16) |
| l12 | screen[0] | table 0.4545, 0.5, 0.5208, 0.5556 (abs 0.0006) | lambda = 50/n; explicit prices 10.448014, 10.429838, -31.994641, -1,446,997.83 (quoted 10.4480, 10.4298, -31.99, -1,446,998) | ok |
| l12 | screen[1] | numeric -1.083, abs 0.002 | 1 - 4 lambda s^2 = -1.082819 at lambda = 0.520833 (-1.0827 at 0.5208); s^2 = 0.999753 (slips: no-four 0.4792; sign 1.083) | ok; hint digit (note 21) |
| l12 | screen[2] | order g1..g5; d1, d2 | g = (1 - 2 lambda s^2)/(1 + 2 lambda s^2); lambda = 200 gives g = -0.995012 | ok |
| l12 | screen[3] | table 496.6, 126.1, 32.5 (abs 1.0, 0.6, 0.4) | errors 496.649, 126.127, 32.516 (x 1e-6); ratios 3.988, 3.969, 3.938, 3.879; prices 10.4427214, 10.4486123, 10.4500869, 10.4504574, 10.4505511 | ok; hint 496.7 (note 22) |
| l12 | screen[4] | numeric 10.4506, abs 6e-5 | Richardson 100/200 = 10.450575955 (error -7.6e-6); 200/400 = 10.450578461 (slips: no-third 10.454503; average 10.445667) | ok |
| l12 | screen[5] | choice ok | 1,600 error 3.25e-5; 800 error 1.26e-4; ratios about 4 | ok; key 84 against 93 and 56 |
| l12 | screen[6] | choice kink | lambda = 200, g = -0.99501; 400 x 4 price 10.008549 (44 pence low); second differences reproduce the canvas points to 5e-6, minimum -0.21585 at S = 99.50; Rannacher 10.449247; 1,600 x 50 plain error -0.030808 | ok; key 100 against 56, 29, 42 (warning 16) |
| l12 | screen[7] | numeric 2.4, abs 0.1 | 101 intervals: 10.469412, error +0.018829; 100 intervals: -0.007862; ratio 2.395 (slips: same 1; smaller 0.418); 201 intervals +0.004752 | key ok; `same` text (error 3) |
| l12 | screen[8] | code: cn_heat_price; 6 tests + example | solution 7/7; starter 0/7; 10.448612308, 10.450086923, 17.662832764, 10.008549, 10.449247 (Rannacher), 10.450551057 | ok; explain (warning 14) |
| l12 | screen[9] | code: richardson, price_to_4dp, explicit_heat_price; 9 tests + example | solution 10/10; starter 0/10; 10.450575955; explicit 10.448014224 and 10.429838421; ValueError at 96 | ok; warnings 6, 7, 15 |
| l12 | screen[10] | multi tol, seq, bnd | three required items; the two distractors are correct as wrong | ok; keys 63, 61, 70 against 33 and 37 (warning 16) |
| l12 | quiz[0] q-order | numeric 2, abs 0.1 | 496.649/126.127 = 3.938 (slip one 1) | ok |
| l12 | quiz[1] q-steps | numeric 400, abs 0 | 0.02 / (0.01^2/2) = 400 (slips: linear 200; hundred 100) | ok |
| l12 | quiz[2] q-boundary | numeric -3.2, abs 0.15 | L = 0.5: 10.448609113 - 10.448612308 = -3.195e-6; L = 1.5: +3.9e-11 (slip abs 3.2) | ok |
| l12 | quiz[3] q-rannacher | choice implicit | two implicit half steps, factor 1/(1 + 4 lambda s^2) = 0.0025 at lambda = 100 | ok; key 102 against 62 and 55 (warning 16) |
| review-3 | item[0] r-k | numeric 0.8889, abs 0.0006 | 0.08/0.09 = 0.888889 (slips: no-two 0.4444; inverted 1.125) | ok |
| review-3 | item[1] r-beta | numeric -0.892, abs 0.0006 | -(1.888889)^2/4 = -0.891975 (slips: no-k -0.003086; half-k -0.197531); alpha 0.0556 | ok |
| review-3 | item[2] r-sd | numeric 0.2121, abs 0.0006 | sqrt(0.045) = 0.212132 (slips: tau 0.15; variance 0.045) | ok; explain quotes a lesson number (note 24) |
| review-3 | item[3] r-put | numeric 6.2715, abs 0.0006 | 7.760257 - 100 + 98.511194 = 6.271451 (slip undiscounted 7.7603) | ok |
| review-3 | item[4] r-drift | numeric 12.475, abs 0.004 | 12.474510 (8% drift, e^-0.05); undiscounted 13.114092; slips price 10.4506 | ok; accept text (note 23) |
| review-3 | item[5] r-se | numeric 0.104, abs 0.002 | 14.70/sqrt(20000) = 0.103945 (slips: no-root 0.000735; n-root 2.0789) | ok |
| review-3 | item[6] r-agree | choice yes | error 4e-5 < 5e-5 | key ok; conflicts with the lesson (warning 8) |
| review-3 | item[7] r-rich | numeric 7.7603, abs 6e-5 | CN 200 7.7576434, 400 7.7596032; formula 7.7602567; Richardson 7.7602565 (slips: no-third 7.761563; average 7.758623) | ok |
| review-3 | item[8] r-decay | numeric 1.0966, abs 0.0006 | 0.25 (2 pi/3)^2 = 1.096623 (slips: no-square 0.523599; no-d 4.386491) | ok; repeats review-2 (warning 12) |
| homework-3 | item[0] h-put-4dp | code: price_put_4dp; 5 tests + example | solution 6/6; starter 1/6 (the visible `bs_put` example only); CN puts 200: 5.571402, 400: 5.572991; Richardson 5.573521 against 5.573526; second option 6.507626280 against 6.507626240 | ok; warning 11 |
| homework-3 | item[1] h-chain | order c1..c5; d1, d2 | alpha, beta, k as in l9; c3 needs c1 and c2 | key ok; c1 and c2 swap rejected (warning 4) |
| homework-3 | item[2] h-r0-sigma | numeric 13.33, abs 0.02 | sqrt(0.04/2.25) = 0.133333 (slips: inverse 30; time 8.889) | key ok; `inverse` text false (error 1); repeats l9 (warning 9) |
| homework-3 | item[3] h-drift-sim | multi ok, anti | 12%: 15.526075; no discount 10.986396; 12% with e^-0.12: 14.476416 | ok; repeats l11 (warning 10) |
| homework-3 | item[4] h-vasicek | numeric 0.8807, abs 6e-5 | B = 1.136603, A = -0.092933, price 0.880706; CN solve 0.8807062 (slips: no-noise 0.880498; flat 0.913931) | ok; simulation unreproducible as written (note 26) |
| homework-3 | item[5] h-explicit | numeric 446, rel 0.01 | lambda = 0.666667, |g| = 1.662556, ^12 = 445.98 (slip one-step 1.66) | ok |
| homework-3 | item[6] h-sequence | numeric 1600, abs 0 | errors 6.535e-4, 1.635e-4, 4.10e-5 at 400, 800, 1,600; crossing at 1,446.06 (slips: exact 1446; eight 800) | ok; cost sentence (warning 17) |
| homework-3 | item[7] h-colleague | longform, 5 rubric lines of 2 points | rubric sums to 10; lambda 200, g -0.9950, second difference -0.21585, 10.4492, 0.0308, sequence and Richardson all recompute | numbers ok; repeats l12 wholesale (warning 13) |

## Mismatches

### Errors

1. **`homework-3.json`, item `h-r0-sigma`, `feedback.byKey.inverse`: "30% multiplies by 2.25" is false.** The slip value 30% is the course's 20% times 1.5 (its square root), not 2.25; 20% x 2.25 is 45%. The rest of the line is right. Fix: "30% multiplies 20% by 1.5. Volatility enters through $\sigma^2T$, so 2.25 times the time divides it by $\sqrt{2.25} = 1.5$." (If warning 9 is taken, rewrite this line with the new slip 24%.)

2. **`l10-formula-from-the-kernel.json`, screen 4: the subtraction that gives 17.66 does not give it.** The hint and `accept` use the four-place values printed in the prose: $110 \times 0.7958 = 87.54$ and $95.1229 \times 0.7345 = 69.87$. The explain then says "$87.54 - 69.87 = 17.66$", but 87.54 - 69.87 = 17.67 (17.670 from the printed values). The exact figure is 87.5330 - 69.8700 = 17.6630, so the printed Phi values carry the error. The key 17.66 with tolerance 0.015 accepts 17.670 (0.010 away), so grading is unaffected, but a learner who follows the printed numbers and checks the explain finds a false sum. Fix: in `explain.text` write "$87.54 - 69.87 = 17.67$ with the four-place values, and the exact figure is £17.6630, so the answer is 17.66 to the cent." Change `accept` to "£17.66 (£17.67 from the rounded values): $110 \times 0.7958 - 95.1229 \times 0.7345$." (Or print $\Phi(0.8266) = 0.79575$ and $\Phi(0.6266) = 0.73452$, which give 87.533 and 69.870 and 17.663.)

3. **`l12-four-decimal-pricer.json`, screen 7, `feedback.byKey.same`: the interpolation does not "add £0.0188 on top".** The text says "The interpolation adds £0.0188 on top of a scheme that already has £0.0079". The 101-interval error is £0.0188 in total (price 10.469412, formula 10.450584), scheme error and interpolation together; a sum of the two would be 0.0267. The pure interpolation term $\tfrac18h^2u_{xx}$ is about £0.0173 (h = 2/101, u_xx = 3.750 at x = 0, factor 94.06), and the scheme error moves with the position of the kink in its cell, so the two do not add. Fix: "Ratio 1 would mean no extra error. The 101-interval error is £0.0188 in all, against £0.0079 for 100 intervals. With the strike between two nodes, interpolation alone accounts for about £0.017 of it."

### Warnings

4. **`homework-3.json`, item `h-chain`, order: a valid order is rejected.** Line c1 ($\tau$, so $V_t = -\tfrac12\sigma^2V_\tau$) and line c2 ($x = \ln(S/K)$ and $V = Kv$ with the chain rule) do not depend on each other; c3 needs both. A learner who takes the logarithm first is marked wrong. Fix: add `"same": [["c1", "c2"]]`. The other lines are a strict chain (c3 needs c1 and c2, c4 needs c3, c5 needs the $\alpha$ of c4). The lesson orders in l9 (screen 2), l10, l11 and l12 are strict or already carry `same` where needed.

5. **`l10-formula-from-the-kernel.json`, screen 5, slider: `tol` 0.1 equals one step.** The canvas price reads 10.0962 at $c = 1.9$ and 10.8018 at $c = 2.1$, against the target 10.4506 the question says to match. Both pass. The wrong band 0.8 to 1.2 is clear of the answer. Fix: `tol` 0.05 (only $c = 2.0$ passes at step 0.1).

6. **`l12-four-decimal-pricer.json`, screen 9: the hidden test at 100 steps is fragile in floating point.** With `h = x[1] - x[0]` from `np.linspace` the 100-step ratio is 0.49999999999999917 and a plain `lam > 0.5` passes. With `h = 2 * L / nx`, which is just as natural, it is 0.5000000000000001 and `lam > 0.5` raises `ValueError`, so a correct solution fails `explicit_heat_price(100, 100, 0.05, 0.2, 1, 100, 100)`. The solution's `+ 1e-12` guard is not stated anywhere. Fix: add to the prose and to the `explicit_heat_price` docstring "Allow rounding error: raise only when `lam > 0.5 + 1e-9`."

7. **`l12-four-decimal-pricer.json`, screen 9: the promise "within 5e-5" holds only for small total variance, and the tests cannot tell a real solution from `return bs_call(...), 400`.** (a) The (200, 400) Richardson rule meets 5e-5 for $\sigma^2T \le 0.05$ (errors -5.1e-6 at 0.04, -2.9e-5 at 0.05) but not beyond: $r = 4\%$, $\sigma = 20\%$, $T = 1.5$ ($\sigma^2T = 0.06$) gives -9.2e-5, and $\sigma = 30\%$, $T = 1$ gives -6.9e-4. The hidden tests use $\sigma^2T$ 0.0156 and 0.015. The prose and docstring promise the tolerance without the limit. (b) `bs_call` is in the prelude, so `return bs_call(S, K, r, sigma, T), 400` passes all three `price_to_4dp` tests. The same holds for `bs_put` in the homework item `h-put-4dp` (5 tests, all compare with `bs_put` or the literal 5.5735). Fix (a): add "for total variance $\sigma^2T$ up to 0.05" to the prose. Fix (b): replace the comparisons with literals (`price_to_4dp(100, 100, 0.03, 0.25, 0.5)[0]` against 7.760257 and `price_to_4dp(120, 120, 0.04, 0.2, 0.75)[0]` against 10.054162, each with `tol` {abs 5e-5}) and keep `bs_call` out of the prelude, giving it to the learner only as a function to write in an earlier lesson. (A test cannot stop a call to a function that is loaded, so removing the oracle from the namespace is the only complete fix.) For `h-put-4dp` use the literal 5.5735 test already there and a second literal for the 120 option, the put 6.507626 (from the formula), and drop `bs_put` from the prelude.

8. **`review-3.json`, item `r-agree`: the answer "yes" conflicts with the lesson.** l12 screen 5 says four-decimal agreement is "a test over a halving sequence, not a single number", and marks "one grid within the tolerance proves the pricer is right" as false. This item scores the single-grid claim "Yes: the error is 4e-5" as right and "It cannot be said from one grid" as wrong, though the question reads "as the course defines it". A learner who took the lesson literally picks `unknown`. Fix: reword the question to "Is its error within the course's tolerance of $5 \times 10^{-5}$?" and the option `unknown` to "That cannot be said without the formula's value". The key and numbers stay.

9. **`homework-3.json`, item `h-r0-sigma`, repeats `l9-black-scholes-to-heat.json` screen 8.** The prose price £7.9656 and the option ($\sigma = 20\%$, $T = 1$, $r = 0$, $S = K$) are the lesson's edge case (DECISIONS "Fresh numbers in reviews and homework"). Fix with $\sigma = 16\%$ for one year: $100(2\Phi(0.08) - 1) = $ £6.3763 (6.376274 by quadrature and by the closed form), the other option $T = 2.25$: `answer` 10.67 (0.0256/2.25 = 0.011378, $\sigma = 0.106667$) with `tol.abs` 0.02; `wrong` `inverse` 24 (16% x 1.5, tol 0.1) and `time` 7.11 (16%/2.25 = 7.111, tol 0.02). Text for `inverse`: "24% multiplies 16% by 1.5. Volatility enters through $\sigma^2T$, so 2.25 times the time divides it by $\sqrt{2.25} = 1.5$." None of 6.3763, 10.67, 24 or 7.11 occurs in the course.

10. **`homework-3.json`, item `h-drift-sim`, repeats `l11-feynman-kac.json` figures.** The `why` and the explain quote £15.5261 (l11 screens 5, quiz) and £10.9864 (l11 screen 6, summary). Fix: real drift $m = 9\%$ gives $e^{-0.05}(100e^{0.09}\Phi(0.55) - 100\Phi(0.35)) = $ £13.1997 (13.199658); replace `nodisc` by "$m = 5\%$, factor $e^{-0.06}$" with the limit $10.4506e^{-0.01} = $ £10.3466 (10.346599) and the text "Discounting at the wrong rate leaves the limit at £10.3466"; replace `real-disc` by "$m = 9\%$, factor $e^{-0.09}$" with limit £12.6821 (12.682092). The key set ("ok" and "anti") is unchanged. Update the explain with the three new figures. None of 13.1997, 10.3466 or 12.6821 occurs in the course.

11. **`homework-3.json`, item `h-chain`, `explain` repeats the lesson option.** "For our option $k = 2.5$, $\alpha = -0.75$ and $\beta = -3.0625$" is `l9` screens 3 to 6 and the summary. Fix: use $r = 2\%$, $\sigma = 25\%$: $k = 0.64$, $\alpha = 0.18$, $\beta = -0.6724$ ($-(1.64)^2/4$). Also, `h-put-4dp` tests the literal 5.5735 (the l10 screen 7 key); see warning 7(b) for the replacement tests.

12. **`review-3.json`, item `r-decay`, repeats `review-2.json` item `r-lambda-len4`.** $L = 3$, $k = 2$ gives $(2\pi/3)^2 = 4.3865$, which is review-2's key and this item's slip `no-d`. Fix: $L = 4$, $k = 3$, $D = 0.5$: `answer` 2.7758 ($0.5 \times (3\pi/4)^2 = 2.775826$); `no-square` 1.1781 ($0.5 \times 3\pi/4$); `no-d` 5.5517 ($(3\pi/4)^2$); the explain value $e^{-2.7758} = 0.0623$ (0.062298). Update the prose, `accept` and `byKey` text. None of these numbers occurs in the course.

13. **`homework-3.json`, item `h-colleague`, repeats `l12-four-decimal-pricer.json` wholesale.** The prompt, model and rubric use the lesson's colleague, option and numbers: 400 by 4, £10.0085, $-0.9950$, £10.4492, £0.0308, the five prices 10.4427214 to 10.4505511, 10.4505836 and 10.4505760 (screens 3, 4, 6, 7, quiz). Fix: keep the story, change the option to $S = K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 0.5$ ($\tau = 0.01$, the formula is £6.8887286). All values below were computed with `nt = nx/5` and checked against a second implementation (`alt2.py`): 400 by 4 returns £6.5728 (£0.3160 low); $\Delta x = 0.005$ and $\Delta\tau = 0.0025$, so $\lambda = 100$ and the top mode has $g = -0.9900$ (1% a step); the second differences go negative beside the strike, down to $-0.277$; Rannacher gives £6.8837. Sequence on 100, 200, 400, 800 and 1,600 intervals: 6.8760493, 6.8855674, 6.8879388, 6.8885312, 6.8886792; errors (formula minus price) 1.27e-2, 3.16e-3, 7.90e-4, 1.97e-4, 4.93e-5, ratios 4.01, 4.00, 4.00, 4.00; only the 1,600 grid is below 5e-5 (4.93e-5, a thin margin). Richardson on 100 and 200 gives 6.8887402 (error +1.2e-5). Plain Crank-Nicolson on 1,600 with 50 steps is £0.0185 off. Update the rubric lines with these numbers (the line structure and the 2-point weights stay). None of these numbers occurs in the course.

14. **`l12-four-decimal-pricer.json`, screen 8, `explain`: the S-grid check supports nothing.** "An independent check on an $S$ grid to £300 (600 intervals, 200 steps) gives £10.449972" reproduces (plain Crank-Nicolson in $S$ gives 10.449972; with Rannacher 10.449959), but it differs from the formula by 6.1e-4 and from the Rannacher £10.4492 by 7.2e-4, so it agrees with neither to four decimals and the sentence reads as a confirmation. Fix: "A direct Crank-Nicolson solve on an $S$ grid to £300 (600 intervals, 200 steps) gives £10.4500, within 7e-4 of the formula, so the two codes agree to three decimals."

15. **`l12-four-decimal-pricer.json`, screen 9, `explain`: "extrapolation works less well" understates it and gives a wrong reason.** At $S = 110$ ($x_0 = 0.0953$ is not a node) Richardson on 200 and 400 intervals has error -1.2e-3, ten times the plain 400-interval error (-1.2e-4); the errors on the grids 100, 200, 400, 800 are 7.3e-3, 3.2e-3, -1.2e-4, 3.0e-5 (ratios 2.3, -26, -4.0), with no steady $h^2$ constant because the position of $x_0$ inside its cell changes with every halving. On two odd grids (201 and 401, strike always at a cell midpoint) Richardson works (7.4e-6). Fix: "If $x_0$ is not a node, the position of $x_0$ in its cell changes with each halving, so the interpolation error has no fixed $h^2$ constant and Richardson can make the price worse (error $-1.2 \times 10^{-3}$ at $S = 110$). The tests use $S = K$."

16. **Choice keys visibly longer than their distractors** (characters without `$`; key against each distractor; mean ratio over distractors, ratio to the longest in brackets): l9 `q-backward` 78 against 51, 25 (2.05, 1.53); l11 screen 0 70 against 43, 32 (1.87, 1.63); l11 `q-sigma0` 64 against 33, 40 (1.75, 1.60); l12 screen 6 100 against 56, 29, 42 (2.36, 1.79); l12 `q-rannacher` 102 against 62, 55 (1.74, 1.65); l12 screen 10 (multi) correct 63, 61, 70 against 33, 37 (2.0, 1.89); homework `h-drift-sim` (multi) correct `anti` 54 against 26, 18, 26 (2.31, 2.08). Suggested keys (distractors lengthened to match):
    - l9 `q-backward`: key "It is the backward heat equation, which has no stable solution" (62); distractors "Nothing: the sign only changes which way the heat flows" (55) and "It still has a drift term left over from the change" (51).
    - l11 screen 0: key "It settles near £10.45, within a few standard errors" (51); distractors "It settles on £10.4506 exactly in every batch of paths" (54) and "It keeps wandering with no limit as paths are added" (51).
    - l11 `q-sigma0`: key "An ordinary differential equation, with first derivatives only" (60); distractors "Still a heat equation, with the diffusion constant set to 0" (59) and "Ill-posed, because there is no diffusion term left in it" (55).
    - l12 screen 6: key "The top mode's factor is $-0.9950$, so the kink's high modes flip sign and barely damp" (83); distractors "The closed form is wrong, because a call's gamma can go negative" (62), "The strike is not on the grid, so interpolation spoils the price" (63), "Crank-Nicolson is unstable for large steps, so errors grow" (56). Drop "($\lambda = 200$)" from the key and keep it in the explain.
    - l12 `q-rannacher`: key "Two implicit half steps damp the kink's high modes, then Crank-Nicolson resumes" (76); distractors "It takes explicit half steps first, to keep the start accurate for longer" (72) and "It smooths the payoff with a normal bump before the pricing begins" (65).
    - l12 screen 10: lengthen the two distractors to about 55 ("The price on the finest grid only, with no coarser grids shown" and "The language and library the pricer happens to be written in").
    - `h-drift-sim`: shorten `anti` to "$m = 5\%$, factor $e^{-0.05}$, antithetic $\pm z$" (42) or lengthen the other options.

17. **`homework-3.json`, item `h-sequence`, `explain`: "at a quarter of the cost" is not supported.** The Richardson price from 200 and 400 intervals costs $200 \times 40 + 400 \times 80 = 40{,}000$ node-steps; the 1,600 grid costs $1600 \times 320 = 512{,}000$, so the ratio is 0.078, about a thirteenth. In time steps alone it is $120/320$ = 0.375. No reading gives a quarter. Fix: "Richardson on 200 and 400 intervals reaches $2 \times 10^{-7}$ for 40,000 node-steps, against 512,000 for the 1,600 grid, which only reaches $4 \times 10^{-5}$."

### Notes

18. **`l9-black-scholes-to-heat.json` screen 7, `accept`: "$100e^{-3.0625 \times 0.02} \times 0.1111$" is 10.4497.** With the rounded 0.1111 the product is 94.0588 x 0.1111 = 10.4496, outside the key's tolerance 0.0006. The hint step uses 0.111107 (right). Fix: "$\times 0.111107$".

19. **`l10-formula-from-the-kernel.json` screen 2, `explain`: "0.6771 - 0.5659 = 0.1111".** With the printed values it is 0.1112; the unrounded values give 0.677056 - 0.565949 = 0.111107. Fix: "$0.67706 - 0.56595 = 0.11111$".

20. **`l10-formula-from-the-kernel.json` screen 9, `accept`: "£2,661.62: $5000 \times e^{-0.05} \times 0.5596$".** With 0.5596 the product is 2661.54; the exact $\Phi(d_2) = 0.559618$ gives 2661.62. Fix: "$\times 0.559618$". Grading is unaffected (tolerance 1).

21. **`l12-four-decimal-pricer.json` screen 1: the hint step gives $-1.0827$, the feedback $-1.0828$.** $4 \times 0.5208 \times 0.99975 = 2.0827$ uses the rounded $\lambda$; the exact $\lambda = 0.520833$ gives $-1.0828$. Also the explain's "$(-1.0828)^{96} \approx 2000$" is 2,077 exactly. Fix: write $\lambda = 0.52083$ in the hint (2.0828) and "about 2,100" in the explain.

22. **`l12-four-decimal-pricer.json` screen 3, hint step: "10.4505836 - 10.4500869 = 0.0004967, which is 496.7".** The key and feedback say 496.6 (unrounded 496.649). Tolerance 1.0 accepts both. Fix: "which is 496.6 to 496.7, depending on rounding".

23. **`review-3.json` item `r-drift`, `accept`: "$0.9512(108.329 \times 0.6915 - 61.791)$" is 12.478, not 12.475.** The exact value is $0.951229 \times (108.3287 \times 0.691462 - 61.7911) = 12.4745$, which the feedback and explain give. Fix the accept text to the unrounded factors. (The key 12.475 with tolerance 0.004 is right.)

24. **`review-3.json` item `r-sd`, `explain`: "the trap that prices our call at £6.6810"** quotes l10's number. Fix: "Using variance $\tau$ instead is the trap of lesson 10."

25. **Error sign is not consistent in l12.** Screen 3 defines error as formula minus price (positive: 7862.2, 496.6). Screen 4's feedback ("an error of $-7.6 \times 10^{-6}$"), screen 7 ("$-\text{£}0.0079$ for 100 intervals") and `r-rich` ("$-2 \times 10^{-7}$") use price minus formula, and `h-colleague` rubric line 4 does not say which. Fix: keep screen 3 as it is ("error = formula minus price" is its table header meaning) and say the direction in words elsewhere: "the extrapolated price is $7.6 \times 10^{-6}$ below the formula" in screen 4, "£0.0079 below" and "£0.0188 above" in screen 7, and "$2 \times 10^{-7}$ below" in `r-rich`.

26. **Simulation figures that cannot be reproduced as written.** `h-vasicek` explain "a seeded simulation gives 0.880800, standard error 0.000043": reproduces with `default_rng(7)`, 300 steps, 200,000 paths (0.8808004, 0.0000428). `r-drift` explain "a million draws give 12.4735": reproduces with `default_rng(11)` (12.473527). l11 screen 7 states `default_rng(21)` and 20,000 paths: it also needs 500 steps (all 200 chart values reproduce). Fix: add the missing seed, path count and step count to each sentence.

27. **The error ratio "about 4 per halving" holds only on these grids (l12 screen 3, `q-order`, homework `h-sequence`).** Beyond 1,600 intervals the ratios fall: 3.77, 3.59, 3.32 for 3,200, 6,400 and 12,800 intervals (errors 8.6e-6, 2.4e-6, 7.2e-7). For larger total variance the ratio is already below 4 on the course range: $r = 4\%$, $\sigma = 20\%$, $T = 1.5$ gives 3.69, 3.47, 3.16, 2.82. The claims in the lessons are right for the stated option ($\sigma^2T = 0.04$) and for the homework option (4.005, 3.999, 3.996, 3.991). Fix: add "for this option" to the explain of screen 3 and to `q-order`.

28. **`homework-3.json` `h-explicit`, explain: "would reach about 0.4".** $446 \times 10^{-3} = 0.446$. Fix: "about 0.45".

29. **Engine items 501 to 503, literal backslash-n, repeats of lesson numbers (already listed).** None of the four expression keys contains `\exp` or an integer symbol, so items 501 and 503 are not reached; item 502 (a letter before a bracket) is exercised by `\sigma^2(T-t)`, `(k+1)^2`, `(1-k)/2` and `2r\sigma^{-2}`, and all grade as products. A scan of every string in the six files found no literal backslash-n (the one hit in l12 screen 9 is the LaTeX `\ne` in "$S \ne K$"). The homework longform `model` has real blank lines. No em-dash or exclamation mark occurs. Cross-references (`ito` 6, 9, 11, `trees` 10, `multivar` 4, `numerics` 14, 15, 17, `odes` 18) match the course maps; the `numerics` and `odes` lessons are not yet authored, so those numbers cannot be checked against text.

## Commands to reproduce

Run from the scratchpad folder `ac-pdes3` (needs `pip install --target pylib scipy sympy mpmath numpy`): `python3 calc1.py` (closed forms and kernel integrals), `python3 vasicek.py`, `python3 fd.py`, `python3 fd2.py`, `python3 fd3.py`, `python3 simp.py`, `node walk.cjs`, `python3 mc.py`, `python3 code_check.py` (all code widgets; or `l12a l12b h3` for one), `node expr.cjs`, `python3 scan.py`, `python3 reuse.py`, `python3 order.py`, `python3 alt.py`, `python3 alt2.py`, `python3 fix_nums.py`, `python3 fix2.py`, `python3 lamfloat.py`, `python3 hvas2.py`, `python3 dense.py`.

## Fix pass

Every corrected number was recomputed by two routes (scratchpad `fix-pdes3/nums*.py`: closed form and SciPy `quad`; banded and dense-LU finite-difference solvers; seeded NumPy). No finding was disputed.

1. Fixed. `h-r0-sigma` `inverse` now reads "24% multiplies 16% by 1.5" (see 9).
2. Fixed. l10 screen 4: hint kept, `accept` gives £17.66 (£17.67 from rounded values), explain says 87.54 - 69.87 = 17.67 with the exact £17.6630 (87.5330 - 69.8700).
3. Fixed. l12 screen 7 `same`: £0.0188 in all against £0.0079, interpolation alone about £0.017 (0.01729 recomputed).
4. Fixed. `h-chain` has `same: [["c1","c2"]]`.
5. Fixed. l10 slider `tol` 0.05; the slider grades `|v - 2| <= tol + 1e-9`, step 0.1, so only 2.0 passes (1.9 reads 10.0962, 2.1 reads 10.8018).
6. Fixed. The prompt and docstring state `np.linspace(-L, L, nx + 1)` (h = 2L/nx) and the guard `lam > 0.5 + 1e-9`; the solution uses 1e-9. Run in CPython with both `h = x[1] - x[0]` and `h = 2 * L / nx`: 9 of 9 tests either way; starter 0 of 9.
7. Fixed. (a) "for total variance up to 0.05" in the prose and docstring. (b) `bs_call` removed from the l12 screen 9 prelude and `bs_put` from `h-put-4dp`; tests compare literals (7.760257, 10.054162; homework 4.7752, 6.507626, 4.768697, each with 5e-5, Richardson errors 1.8e-7, 4e-8, 2.7e-8, 4e-8, 4.2e-7). The homework option is now r = 6%, sigma = 20%, T = 0.75 (put 4.7751999 by formula and by kernel), so the lesson option is gone from the item as well.
8. Fixed. `r-agree` question and `unknown` option reworded; key unchanged.
9. Fixed. `h-r0-sigma`: sigma = 16%, call £6.3763 (6.376274 by closed form and quadrature); answer 10.67 (abs 0.02); `inverse` 24, `time` 7.11.
10. Fixed. `h-drift-sim`: m = 9% gives £13.1997; wrong discount e^-0.06 gives £10.3466; m = 9% with e^-0.09 gives £12.6821. Prose said four simulations for five options; now five. Option texts lengthened to similar size (also fixes 16 here).
11. Fixed. `h-chain` explain uses r = 2%, sigma = 25%: k = 0.64, alpha = 0.18, beta = -0.6724. `h-put-4dp` literal replaced (see 7).
12. Fixed. `r-decay`: L = 4, k = 3, D = 0.5: 2.7758; `no-square` 1.1781; `no-d` 5.5517; e^-2.7758 = 0.0623.
13. Fixed. `h-colleague` option S = K = 100, r = 5%, sigma = 20%, T = 0.5: formula 6.8887286, 400 by 4 gives 6.5728 (0.3160 low), lambda = 100, g = -0.9900, second differences down to -0.277 (both solvers), Rannacher 6.8837, sequence 6.8760493, 6.8855674, 6.8879388, 6.8885312, 6.8886792 (errors 1.27e-2 to 4.93e-5), Richardson 100/200 6.8887402, 1,600 by 50 is £0.0185 off. Rubric weights unchanged. Dense solver checked 100 to 800 intervals; the 1,600 value agrees with the answer check's independent run.
14. Fixed. l12 screen 8 explain: S-grid solve gives £10.4500, £0.0006 below the formula (6.1e-4 recomputed), with no claim of four-decimal agreement.
15. Fixed. l12 screen 9 explain: off the node extrapolation can fail; at S = 110 it lands £0.0012 below the formula (-1.22e-3 recomputed).
16. Fixed. l9 `q-backward`, l11 screen 0 and `q-sigma0`, l12 screen 6, `q-rannacher` and screen 10, `h-drift-sim` options lengthened or shortened as suggested (kink key lost "(lambda = 200)", which moved into the explain).
17. Fixed. `h-sequence` explain: 40,000 against 512,000 node-steps (ratio 0.078).
18. Fixed. l9 screen 7 `accept` uses 0.111107.
19. Fixed. l10 screen 2 explain: 0.67706 - 0.56595 = 0.11111.
20. Fixed. l10 screen 9 `accept`, hint and explain use 0.559618 and 0.53232 (2661.62).
21. Fixed. l12 screen 1 hint uses lambda = 0.52083 (2.0828); explain says about 2,100 (2,077 exact).
22. Fixed. l12 screen 3 hint: "496.6 to 496.7, depending on rounding".
23. Fixed. `r-drift` `accept` uses 0.951229, 108.3287, 0.691462, 61.7911 (12.4745).
24. Fixed. `r-sd` explain: "the trap of lesson 10".
25. Fixed. Direction in words: l12 screen 4 ("below the formula"), screen 7 ("above", "below"), `r-rich` ("below it"), `h-colleague` ("above the formula"). Screen 3 keeps formula minus price.
26. Fixed. `default_rng(21)`, 500 steps, 20,000 paths (l11 screen 7); `default_rng(7)`, 300 steps, 200,000 paths (`h-vasicek`); `default_rng(11)` (`r-drift`).
27. Fixed. "for this option" in l12 screen 3 explain, `q-order` explain and `accept`.
28. Fixed. `h-explicit` explain: about 0.45.
29. No defect; no edit. The scan found nothing to change.

Also split five sentences over 20 words that the edits created; voice scan is 0 and 0.

### Changed keys

- l9 `q-backward` (options text)
- l10 screen 5 slider (`tol` 0.1 to 0.05)
- l11 screen 0 (options text)
- l11 `q-sigma0` (options text)
- l12 screen 6 (options text)
- l12 screen 9 (hidden tests 4 and 5 now literals, prelude without `bs_call`, solution guard 1e-9)
- l12 screen 10 (options text)
- l12 `q-rannacher` (options text)
- review-3 `r-agree` (question, `unknown` option)
- review-3 `r-decay` (key 2.7758, `wrong` 1.1781 and 5.5517)
- homework-3 `h-put-4dp` (example, all five tests, option numbers, prelude without `bs_put`)
- homework-3 `h-chain` (`same` group c1, c2)
- homework-3 `h-r0-sigma` (key 10.67, `wrong` 24 and 7.11)
- homework-3 `h-drift-sim` (options text and numbers)
- homework-3 `h-colleague` (prompt, model and rubric numbers)

Results: validator 0 errors; playthrough of l9 to l12, review-3 and homework-3 passes plain and with `--mobile --tablet`; voice scan 0 and 0.
