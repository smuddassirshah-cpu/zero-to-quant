# Claim ledger: numerics level 4 (blind concept audit) and delta read of four code widgets

Written before reading any earlier review or author report. "script" means a check in `docs/reports/numerics-L4-concepts.py` (244 checks pass, 8 `EXPECTED_FAIL`, exit 0). Sources: MM = Morton and Mayers, *Numerical Solution of Partial Differential Equations*; TR = Tavella and Randall, *Pricing Financial Instruments: The Finite Difference Method*; Wilmott = *Paul Wilmott on Quantitative Finance*, finite-difference chapters; Hull = *Options, Futures and Other Derivatives*; G = Glasserman, *Monte Carlo Methods in Financial Engineering*; Higham = *Accuracy and Stability of Numerical Algorithms*; TB = Trefethen and Bau; NR = Press et al., *Numerical Recipes*; BGK = Broadie, Glasserman and Kou (1997); GC = Giles and Carter (2006). Files are in `app/content/courses/numerics/`.

## Part A

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l13 | screens[0].prose, question, widget.answer | An explicit central-difference update at the ring reads the three nodes 98, 100, 102 on the known row | correct | MM 2.2 (explicit scheme stencil) |
| l13 | screens[0].widget.wrong, feedback.byKey.same-level | Reading the ring's own level is the implicit scheme | correct | MM 2.8 |
| l13 | screens[0].feedback.byKey r2c3, r2c5, r1c4, r3c2, r3c6, order | Slips: unknown level, later level, two steps out, order | correct | follows from the stencil |
| l13 | screens[0].hints, feedback.correct, explain | V_SS and V_S at 100 need 98 and 102; known values 0, 0, 2; new value is a weighted sum of three known numbers | correct | derivation |
| l13 | screens[1].prose, captions | Explicit grid M=100, N=500 against Black-Scholes; grid values 0.2050, 2.7481, 6.8775, 10.4428; formula 0.3618, 2.7737, 6.8887, 10.4506 | correct | script (own march, SciPy banded solver) |
| l13 | screens[1].widget, feedback, hints | Grid price at tau = 1 is 10.4428; slip 10.4506 is the formula | correct | script |
| l13 | screens[1].explain | Error -0.0078; the kink is smoothed within the first few steps | correct | script; diffusion smooths non-smooth data, MM 2.7 |
| l13 | screens[2].prose | Black-Scholes equation in time to expiry, V_tau = half sigma^2 S^2 V_SS + r S V_S - r V, payoff (S-K)+ | correct | Hull 15.6 with tau = T - t; Wilmott ch. 5 |
| l13 | screens[2].prose | Call edges V(0) = 0 and V(Smax) = Smax - K e^(-r tau) | correct | Hull 21.8; TR ch. 4 |
| l13 | screens[2].widget.options[0] | Second difference (V_{j+1} - 2V_j + V_{j-1}) / dS^2 stands in for V_SS | correct | MM 2.2 |
| l13 | screens[2].widget.options[1..3].why | Wrong options: slope formula, one first difference, wrong divisor | correct | derivation |
| l13 | screens[2].hints, feedback.generic | V_SS is the rate of change of slope; difference of the two one-sided slopes over dS | correct | derivation |
| l13 | screens[2].feedback.correct | The second difference is exact for quadratics | correct | Taylor: error term has V''''; exact for cubics too, so the claim holds |
| l13 | screens[2].explain | Central V_S and a forward step in tau give an explicit update that needs only the known row | correct | MM 2.2 |
| l13 | screens[3].prose | a_j = half dt (sigma^2 j^2 - r j), b_j = -dt (sigma^2 j^2 + r), c_j = half dt (sigma^2 j^2 + r j) with S_j = j dS | correct | derivation from the PDE; Wilmott explicit scheme; differs from Hull 21.8 only by Hull discounting at the new level |
| l13 | screens[3].widget.rows, hints, feedback, explain | a_50 = 0.0975, 1 + b_50 = 0.7999, c_50 = 0.1025, V_50 = 0.2050; weights sum to 1 - r dt = 0.9999 | correct | script |
| l13 | screens[3].feedback.generic | Keep the half in a and c; centre weight is 1 + b | correct | derivation |
| l13 | screens[4].prose, widget, hints | M=200, N=1,700 gives 10.4487; error -0.0019; slips -0.0078, -0.0039, +0.0019 | correct | script |
| l13 | screens[4].feedback.byKey.half | Halving the old error is what a first-order method would give | correct | order definition |
| l13 | screens[4].explain | "Halving dS quartered the error, so the dS^2 term dominates" | imprecise | script: N also rose 3.4 times, so the time error fell 3.4 times too; a ratio of 4.2 cannot separate the terms. The conclusion is true (space -0.0099, time +0.0021 at M=100) but the inference is not. Finding 7 |
| l13 | screens[4].explain | The error is largest near the strike | correct | script |
| l13 | screens[5].prose | Centre weight 1 + b_j is non-negative only if dt (sigma^2 j^2 + r) <= 1 | correct | algebra |
| l13 | screens[5].prose | Taking j = M as a safe bound gives dt <= 1 / (sigma^2 M^2 + r) | correct | sufficient condition by the maximum principle, MM 2.11; stated as "a safe bound" |
| l13 | screens[5] captions | N=250: 4.5e30; N=300: 379,169; N=330: 10.4439 with 7.5e14 near the top; N=500: largest value 104.88 at Smax | correct | script |
| l13 | screens[5].widget, hints, feedback | Smallest N the bound allows at M=100 is 401; slips 400 and 5 | correct | script |
| l13 | screens[5].feedback.byKey.down | N = 400 gives dt = 0.0025, just over the bound | correct | 0.0025 > 1/400.05 |
| l13 | screens[5].feedback.byKey.no-square | The weight grows like j^2 | correct | b_j |
| l13 | screens[5].explain | The blow-up starts at the top of the grid, where sigma^2 j^2 is largest | correct | script (largest value at S > 180 for N=330) |
| l13 | screens[6].prose, options, hints, explain | M=200 needs N >= 1,601; with N=500 the price is about 4.1e277; halving dS means quartering dt | correct | script |
| l13 | screens[6].widget.options[0].why, feedback.byKey.better | The safe step shrinks like 1/M^2 | correct | bound |
| l13 | screens[6].widget.options[1].why | Halving dS changes every weight | correct | a, b, c depend on j |
| l13 | screens[6].widget.options[3].why | NumPy only warns on overflow and carries on | correct | NumPy floating-point error handling default is warn; same in Pyodide NumPy 2.0.2 |
| l13 | screens[7].prose | Safe while dt <= 1/(sigma^2 M^2 + r), about dS^2 / (sigma^2 Smax^2) | correct | algebra; "safe while" is the sufficient direction |
| l13 | screens[7].prose | This is stiffness: the grid's fastest modes decay at rates like sigma^2 S^2 / dS^2 and the explicit step must keep up | correct | MM 2.7 (Fourier modes); largest eigenvalue of the second difference is 4/dS^2 times half sigma^2 S^2 |
| l13 | screens[7].widget.options, feedback | M=300 needs N >= 3,601, nine times as many; slips 1,201, 401, 694 | correct | script |
| l13 | screens[7].explain | Work is M times N, so tripling M costs 27 times | correct | 3 times 9 |
| l13 | screens[8].widget.solution | explicit_bs: vectorised update from the old row, edges reset, np.interp at S0 | correct | script: equals own march to 1e-10; 7 hidden tests and the example pass; starter fails all 7 |
| l13 | screens[8].widget.solution | stable(M, N, sigma, r, T) returns T/N <= 1/(sigma^2 M^2 + r) | correct | matches the stated bound |
| l13 | screens[8].widget.tests, examples, how | Expected 10.442791444, 17.65725084, 10.416091888; K=0 returns 100; N=300 above 1e5; stable flags | correct | script |
| l13 | screens[8].hints, feedback | Slice update; top edge Smax - K e^(-r (n+1) dt); first step V_50 = 0.2050 | correct | script |
| l13 | screens[8].explain | NumPy builds the right side from the old row first | correct | NumPy evaluates the right side before assignment |
| l13 | screens[8].explain | The share (K = 0) is linear in S, so the grid returns it exactly | correct | a(j-1) + (1+b) j + c(j+1) = j; script 1e-9 |
| l13 | screens[9] correct option, explain | The European check measures the error of these settings (about 0.008); quote the barrier with that allowance or refine | correct | script: down-and-out H=90 on the same explicit grid errs by -0.0052 against the closed form, the same size |
| l13 | screens[9].widget.options[1..3].why | Same differences and steps; a dS^2 error under a penny is expected; one node can look right while the top has exploded | correct | script (N=330) |
| l13 | screens[9].feedback, hints | The European is the grid's calibration check | correct | TR ch. 5 (validation against closed forms) |
| l13 | summary.ideas[0] | Each explicit step is a weighted sum of three known nodes | correct | scheme |
| l13 | summary.ideas[1] | The error is mostly dS^2: -0.0078 and -0.0019 | correct | script: space -0.0099 and -0.0025, time +0.0021 and +0.0006 |
| l13 | summary.ideas[2] | The explicit step is safe "only while" dt <= 1/(sigma^2 M^2 + r) | imprecise | script: step matrix has spectral radius <= 1 from N = 359 at M=100 (bound 401; frozen-coefficient von Neumann 393). Sufficient, near sharp, not necessary. MM 2.11. Finding 6 |
| l13 | summary.formula, note, trap | Explicit update and bound; refine S and the time step shrinks with its square; refining S alone explodes | correct | script (M=200, N=500) |
| l13 | quiz[0] all | M=50 needs N >= 101; slips 100 and 401; halving M quarters the steps | correct | script |
| l13 | quiz[1] options, explain | N=330 price 10.4439 is not usable: unstable, growth spreads from the top and would reach S=100 | correct | script: same step, twice the march, the value at 100 exceeds 1e3 |
| l13 | quiz[1].widget.options[2].why | The blow-up is the scheme amplifying noise, not an edge effect | correct | spectral radius 1.17 at N=330 |
| l13 | quiz[2] all | explicit_bs with K=0 returns 100; slips 10.4428 and 95.1229 | correct | script |
| l13 | quiz[2].explain | A forward is linear too; its only error, 2.4e-4, comes from the time step | correct | script (forward payoff with exact edges: 2.4e-4) |
| l14 | screens[0].prose | Each scheme multiplies a mode of frequency omega by a factor per step; a factor outside [-1, 1] grows | correct | von Neumann analysis, MM 2.7 |
| l14 | screens[0].prose | nu = sigma^2 S^2 dt / (2 dS^2); the level's bound sigma^2 j^2 dt <= 1 is nu <= 1/2 | correct | algebra; MM 2.7 |
| l14 | screens[0].canvas functions | Factors 1 - 4 nu sin^2(omega/2), 1/(1 + 4 nu sin^2), (1 - 2 nu sin^2)/(1 + 2 nu sin^2) | correct | MM 2.7, 2.10 (frozen coefficient, diffusion term) |
| l14 | screens[0].widget, feedback | Largest nu for the explicit factor to stay in [-1, 1] is 0.5; slips 1 and 0.25 | correct | 1 - 4 nu >= -1 |
| l14 | screens[0].explain | Implicit factor in (0, 1]; Crank-Nicolson in (-1, 1] and tends to -1 as nu grows | correct | algebra |
| l14 | screens[1].prose | Theta-scheme (I - theta dt L) V^{n+1} = (I + (1 - theta) dt L) V^n; 0 explicit, 1 implicit, 1/2 Crank-Nicolson | correct | MM 2.10; TR ch. 3 |
| l14 | screens[1] options, hints, feedback | At nu = 20: Crank-Nicolson -39/41 = -0.951, implicit 0.012, explicit -79 | correct | arithmetic |
| l14 | screens[1].explain | Sharpest modes flip sign each step and shrink only 5% a step; trapezoidal ringing | correct | 1 - 0.951; Crank-Nicolson is the trapezium rule in time, A-stable not L-stable (Hairer and Wanner IV.3) |
| l14 | screens[2] all | With theta > 0 the ring's equation holds three unknowns on the new level; M - 1 equations; tridiagonal matrix | correct | MM 2.8 |
| l14 | screens[3].prose | Thomas clears the one entry below each pivot, then substitutes back | correct | MM 2.9; Higham 9.5 |
| l14 | screens[3].widget states | Pivots 2, 3/2, 4/3, 5/4; right sides 1, 1/2, 1/3, 5/4; x = (1, 1, 1, 1) | correct | script (np.linalg.solve) and hand elimination |
| l14 | screens[3].widget.states.s0.ops[1].why | No swap needed: each pivot is the largest entry in its column; a swap would break the tridiagonal shape | correct | Higham 9.5 (pivoting widens the band) |
| l14 | screens[3].widget.states.s1.ops[1].why | Finish the forward sweep before substituting back | correct | algorithm |
| l14 | screens[3].explain | The sweep costs "about 3M operations" | imprecise | script: the lesson's own solution does 8 arithmetic operations a row (3 multiplies, 2 divides, 3 subtracts); MM 2.9 and Higham count 5n multiplications and divisions. Finding 8 |
| l14 | screens[3].explain | Pivots never approach 0, so no swap; a dense solver costs about M^3/3 | correct | Higham 9.5; TB lecture 20 (n^3/3 multiplications) |
| l14 | screens[4].widget.lines s1 to s5 | Thomas steps: keep row 1; m_k = a_k / b'_{k-1}; update b'_k and d'_k; x_n = d'_n / b'_n; back substitute | correct | MM 2.9; NR 2.4 |
| l14 | screens[4].widget.lines[5].why, feedback.byKey.d1 | A diagonally dominant tridiagonal matrix keeps its pivots away from 0, so Thomas never swaps | correct | Higham theorem 9.12 and 9.5 |
| l14 | screens[4].explain | Diagonal 1 + theta dt (sigma^2 j^2 + r) beats the off-diagonals | correct | off-diagonal sum is theta dt sigma^2 j^2 for j >= 2 and 0.05 theta dt at j = 1 |
| l14 | screens[4].hints, feedback | Forward before back; multiplier before the updates | correct | algorithm |
| l14 | screens[5] table | Implicit errors -0.0519, -0.0309, -0.0204; Crank-Nicolson -0.00950, -0.00980, -0.00987, -0.00246, -0.000616 | correct | script |
| l14 | screens[5] correct option, feedback | Implicit O(dt + dS^2), Crank-Nicolson O(dt^2 + dS^2) | correct | MM 2.10; for a kinked payoff the price keeps second order at fixed dt/dS (GC; script ratio 4.0), gamma does not, which screens[6] shows |
| l14 | screens[5].widget.options[1..3].why | Crank-Nicolson's column barely moves with N; the implicit column moves | correct | table |
| l14 | screens[5].hints, explain | Space error about -0.0099; implicit remainders -0.042, -0.021, -0.0105 halve; doubling M and N divides the Crank-Nicolson error by 4.0 | correct | script |
| l14 | screens[6].prose | Crank-Nicolson is second order and stable at any step | correct | MM 2.10 |
| l14 | screens[6].prose | M=400, N=10 gives nu = 80 at the strike | correct | script |
| l14 | screens[6] captions, options | CN: 10.2767, gamma 1.2526; implicit: 10.3457, gamma 0.01957; two implicit steps then CN: 10.4324, gamma 0.01904; formula gamma 0.018762 | correct | script |
| l14 | screens[6].widget.options[1].why | At nu = 80 the sharpest modes have factor -0.988, so the kink rings | correct | -159/161; GC |
| l14 | screens[6].widget.options[2].why | Implicit leaves gamma 4% high and the price 0.105 short | correct | script |
| l14 | screens[6].widget.options[3].why | With two implicit steps gamma is within 1.5% | correct | 0.01904 / 0.018762 = 1.0148 |
| l14 | screens[6].feedback.byKey.cn | Stable only means the ringing does not grow | correct | definition of stability against L-stability |
| l14 | screens[6].explain | Gamma 67 times too big; two implicit Euler steps first kill the sharp modes; this is the idea behind Rannacher's start | correct | Rannacher (1984); GC (the published start-up uses half steps; "the idea behind" is accurate) |
| l14 | screens[7].prose | dt L multiplies a mode by about -z, z = 4 nu sin^2(omega/2); explicit 1 - z, implicit 1/(1+z); CN (1 + z/2) V^{n+1} = (1 - z/2) V^n | correct | MM 2.10 |
| l14 | screens[7].widget, feedback | CN factor (1 - z/2)/(1 + z/2); slips: average of the two factors, inverted ratio | correct | algebra |
| l14 | screens[7].explain | Below 1 in size for every z > 0; tends to -1; explicit and implicit O(dt + dS^2), CN O(dt^2 + dS^2) | correct | MM 2.10 |
| l14 | screens[8].prose | Plain loops are fine: the work is "only about 3n steps" | imprecise | as screens[3].explain. Finding 8 |
| l14 | screens[8].widget.solution | thomas: forward elimination storing c' and d', back substitution, returns an array | correct | script: 5 hidden tests and the example pass against np.linalg.solve; starter fails all 5 |
| l14 | screens[8].widget.starter docstring | a below, b on, c above; a[0] and c[-1] not used | correct | solution reads c[-1] only into an unused entry |
| l14 | screens[8].hints | m = b[k] - a[k] cp[k-1]; cp[k] = c[k]/m; dp[k] = (d[k] - a[k] dp[k-1])/m; x[k] = dp[k] - cp[k] x[k+1] | correct | NR 2.4 |
| l14 | screens[8].feedback.correct | "in about 3n steps" | imprecise | Finding 8 |
| l14 | screens[8].explain | Back sweep needs one multiply and one subtract a row | correct | solution |
| l14 | screens[8].explain | For M = 400 "about 1,200 operations", against 21 million dense | imprecise | 3,186 operations counted at n = 399; 21 million is M^3/3. Finding 8 |
| l14 | screens[9].prose | Each step builds (I + (1 - theta) dt L) V^n, adds the top edge's term, calls thomas; first implicit_start steps use theta = 1 | correct | solution; script equals own march |
| l14 | screens[9].widget.solution, tests | theta_bs values 10.398663728, 10.440710244, 10.442791444, 10.276726325, 10.432399088, 17.64630937 | correct | script: 6 tests and example pass; starter fails all 6 |
| l14 | screens[9].hints | System diagonals -theta dt alpha, 1 - theta dt beta, -theta dt gamma; add theta dt gamma_{M-1} V_M^{n+1} to the last right side | correct | derivation |
| l14 | screens[9].explain | With theta = 0 the system is the identity; the known top edge moves to the right side; the bottom edge is 0 | correct | derivation |
| l14 | screens[10] all | 1.2526 / 0.018762 = 66.8; slips 1.2338 and 0.015; price off by only 0.17 | correct | script |
| l14 | screens[10].explain | Production pricers start with a few implicit steps; gamma, not price, is the test that catches ringing | correct | GC; TR ch. 4 |
| l14 | summary.ideas[0] | Theta-scheme, a tridiagonal system per step, by Thomas "in about 3M operations" | imprecise | Finding 8 |
| l14 | summary.ideas[1] | Explicit needs nu <= 1/2; implicit stable but first order in time; CN stable and O(dt^2 + dS^2) | correct | MM 2.10 |
| l14 | summary.ideas[2], formula, trap | CN factor tends to -1 for large nu so a kink rings; a few implicit steps fix it; unconditionally stable is not smooth | correct | GC; Rannacher |
| l14 | quiz[0] all | 0.00246 / 0.000616 = 4.0, second order in both steps; slips 0.25 and 2 | correct | script |
| l14 | quiz[1].prose | M=100, N=500: nu <= 0.4 at every node; prices 10.4428, 10.4386, 10.4407 | correct | script |
| l14 | quiz[1].widget.options[0].text | "With nu <= 1/2 every factor is close to the others" | imprecise | at nu = 0.4 and omega = pi the factors are -0.6, 0.385, 0.111. The schemes agree because each time error is small (dt = 0.002), as options[1].why says. Finding 9 |
| l14 | quiz[1].widget.options[1].why, [2].why | The schemes differ only through their time error; all three sit about 0.01 below the formula | correct | script (-0.0078, -0.0120, -0.0099) |
| l14 | quiz[1].explain | At small nu the factors nearly coincide on the modes that matter; shared dS^2 error about -0.01 | correct | smooth modes have small z; script |
| l14 | quiz[2] all | CN factor at nu = 80 is -159/161 = -0.9876; slips 0.9876, 0.0031; shrinks 1.2% a step; 88% left after ten | correct | script |
| l15 | screens[0].prose, canvas | 50 steps of the risk-neutral log price: drift 0.0006, sd 0.028284 a step | correct | (r - sigma^2/2)/50 and sigma sqrt(1/50) |
| l15 | screens[0].widget, feedback, explain | SE with 2,000 paths about 0.33 = 14.72/sqrt(2,000); slips 10.45 and 14.72; halving it needs four times the paths | correct | G 1.1 |
| l15 | screens[1].prose | Discounted payoffs have exact sd s = 14.7194 | correct | script (quadrature of E[Y^2]) |
| l15 | screens[1].prose | Standard error of a mean of n independent payoffs is s / sqrt(n) | correct | G 1.1 |
| l15 | screens[1].widget.rows, explain | 1.472, 0.465, 0.147, 0.0465; ten times the cost buys 3.16 | correct | script |
| l15 | screens[2].prose | SE = s n^(-1/2) is a straight line on log axes | correct | algebra |
| l15 | screens[2].prose | "This holds whatever the payoff" and whatever the number of shares | imprecise | needs a finite variance (G 1.1: square-integrable payoff). Finding 11 |
| l15 | screens[2].widget, feedback, explain | Slope -1/2; slips +0.5 and -1; the rate does not depend on dimension | correct | G 1.1 |
| l15 | screens[3] all | n = (s / 0.01)^2 = 2,166,609 with unrounded s; slips 1,472 and 147,194; each extra digit costs 100 times | correct | script |
| l15 | screens[4] all | 100,000 paths give 0.0465, not 0.0147; a tenfold cut needs 100 times the paths | correct | arithmetic |
| l15 | screens[5].prose, table | Seed 0: 10.4362, SE 0.0465, -0.31 SE; seed 1: 10.3578, 0.0464, -2.00 SE | correct | script (default_rng stream is stable across NumPy 2.0.2 and 2.5) |
| l15 | screens[5].prose | A 95% interval is the estimate plus or minus 1.96 SE | correct | CLT, G 1.1 and appendix A |
| l15 | screens[5].widget, feedback | Lower end 10.3450; slips 10.3896 and 10.2538 | correct | script |
| l15 | screens[5].explain | Seed 1's interval just misses; a 95% interval misses in one run in 20 | correct | script: 4.9% of 20,000 runs miss at n = 2,000 |
| l15 | screens[6].prose | Down-and-out call H=90 watched continuously is worth 8.6655 | correct | script (Reiner-Rubinstein form, Hull 26.9) |
| l15 | screens[6].prose | "Broadie-Glasserman closed form" with shifted barrier H e^(-0.5826 sigma sqrt(dt)) | imprecise | the result is Broadie, Glasserman and Kou (1997); formula and sign are right (G 6.4, beta = 0.5826). Finding 13 |
| l15 | screens[6] table | Simulated 9.572, 9.152, 8.936 (SE 0.033); shifted 9.580, 9.174, 8.914 | correct | script: own simulations 9.572 (2,000,000 paths), 9.174, 8.936; a 16-million-path run gives 9.581 (SE 0.004) for monthly |
| l15 | screens[6] correct option | With 20 million paths the monthly estimate settles near 9.58 with a band ten times narrower | correct | script; SE falls by sqrt(100) |
| l15 | screens[6].widget.options[1..3].why, feedback, hints | Monitoring is a bias no number of paths removes; the monthly option is a different, dearer contract | correct | G 6.4; script (gap is more than 6 SE) |
| l15 | screens[6].explain | Only more dates shrink the gap; the shifted closed form agrees | correct | BGK |
| l15 | screens[7].prose | Trapezium grid with n points in d dimensions has h like n^(-1/d) and errs like n^(-2/d); behind Monte Carlo once d > 4 | correct | G 1.1 |
| l15 | screens[7] options, explain | d = 12 gives n^(-1/6); a tenfold cut needs a million times the points; Monte Carlo needs 100 times | correct | arithmetic |
| l15 | screens[7].prose | An Asian with 12 fixings is a 12-dimensional integral | correct | G 1.1 |
| l15 | screens[8].widget.solution | mc_call: one draw of n normals, exact terminal price, discounted payoffs, ddof = 1, ValueError for n < 2 | correct | script: 7 tests and example pass; starter fails all 7; exact lognormal sampling is unbiased (G 3.2) |
| l15 | screens[8].widget.solution | paths_for_error = ceil((s / target)^2) | correct | algebra |
| l15 | screens[8].widget.tests, canvas | 10.4361628282, 0.0465140620; 10.3577576442; 14.46696108; 2,166,608; 314,789 | correct | script |
| l15 | screens[8].explain, hints | One call fixes the stream; with n = 1 the spread divides by n - 1 = 0; the count rounds up | correct | NumPy |
| l15 | screens[9] all | 50,000 paths at 0.04 need 800,000 for 0.01; slips 200,000 and 500,000 | correct | arithmetic |
| l15 | summary.ideas[0], formula, note, trap | SE = s / sqrt(n); 100,000 paths give 0.0465; ten times the paths gives 3.16 times the accuracy | correct | script |
| l15 | summary.ideas[1] | "a grid loses once d > 4" | imprecise | true for the second-order trapezium grid of screens[7]; a fourth-order rule ties at d = 8. Finding 12 |
| l15 | summary.ideas[2] | Paths cut noise, not bias: monthly barrier stays near 9.58 against 8.6655 | correct | script |
| l15 | quiz[0] all | One path: refuse; ddof = 1 divides by 0; ddof = 0 would claim zero spread | correct | definition of the sample sd |
| l15 | quiz[1] all | 0.30 to 0.05 needs 36 times the paths: 90,000; slips 15,000 and 6,124 | correct | arithmetic |
| l15 | quiz[2] all | d = 8: grid n^(-1/4) against n^(-1/2); they tie only at d = 4 | correct | G 1.1 |
| l16 | screens[0].prose, canvas | Plain, antithetic and control estimators on the same draws; control uses b = 0.6736 and mean 100 | correct | script |
| l16 | screens[0].widget.options[1].why | Per draw the antithetic variance is a quarter of plain, from two payoffs; the control's is a seventh | correct | script: 54.06/216.66 and 31.48/216.66 |
| l16 | screens[0].explain | Control band about sqrt(6.9) = 2.6 times narrower; antithetics help less | correct | script |
| l16 | screens[1].prose | X = e^(-rT) S_T has mean exactly S_0 | correct | risk-neutral martingale, G 4.1.1 |
| l16 | screens[1].prose | Averaging Y - b(X - 100) is "still unbiased, for any b" | imprecise | true for a fixed b; screens[5] and the code then fit b on the same paths, which adds an O(1/n) bias (script: -0.84 at n = 10, -0.19 at n = 40). G 4.1.3. Finding 4 |
| l16 | screens[1] table | Var(Y) 216.66, Var(X) 408.11, Cov 274.91, E[X] 100 | correct | script |
| l16 | screens[1].widget, feedback, explain | b* = Cov / Var(X) = 0.6736; slips 1.4845, 1.2688; regression slope; seed 0 gives 0.67307 | correct | G 4.1.1; script |
| l16 | screens[2].widget.lines[0] | Var(Y - bX) = Var(Y) - 2b Cov + b^2 Var(X), "since variance is bilinear" | imprecise | the expansion is right; the reason is that covariance is bilinear (variance is quadratic). Finding 5 |
| l16 | screens[2].widget.lines[1..4] | Derivative, minimum at Cov/Var(X), residual Var(Y) - Cov^2/Var(X) = Var(Y)(1 - rho^2) | correct | G 4.1.1 |
| l16 | screens[2].widget.lines[5].why | At b = 1 the variance is 74.95, more than twice 31.48 | correct | script |
| l16 | screens[2].feedback.byKey.d1 | The call moves about 0.64 per 1 of share at the money | correct | delta N(0.35) = 0.637 |
| l16 | screens[2].explain, feedback.correct | Residual 216.66 (1 - 0.92450^2) = 31.48; the control removes the part of Y that moves with X | correct | script |
| l16 | screens[3] all | Paths needed scale with variance per path; factor 1/(1 - rho^2); 5.3 at 0.9, 50 at 0.99; slips 1/(1 - rho) and 1 - rho^2 | correct | G 4.1.1 |
| l16 | screens[3].explain | A control is worth having only if it is highly correlated | correct | G 4.1.1 (the sign of rho does not matter; the put quiz covers negative rho) |
| l16 | screens[4] all | rho = 0.92450 gives 6.88; about 315,000 paths; slips 13.25 and 0.855; one more multiply per path | correct | script |
| l16 | screens[5].prose, table | Seed 0: plain 10.4362 (0.046514); control 10.4484 (0.017764), b = 0.67307 | correct | script |
| l16 | screens[5].widget, feedback | Observed factor 6.86; slips 2.62 and 0.146 | correct | script |
| l16 | screens[5].explain | Estimating b from the paths costs almost nothing at this size; control price 0.12 SE from the formula | correct | script: bias about -8/n, so -8e-5 at n = 100,000 against SE 0.0178 |
| l16 | screens[6].prose | Pair correlation -0.501; pair-mean variance half Var(Y)(1 + rho) = 54.06; two independent paths 108.33 | correct | script; G 4.2 |
| l16 | screens[6].widget, feedback | Efficiency 2.0 at equal cost; slips 0.5 and 1.41; compare variances at equal cost | correct | G 4.2 |
| l16 | screens[6].explain | Seed 0, 50,000 pairs: 10.4721, SE 0.0329; pairs with a fitted control leave a pair variance of 3.78 | correct | script |
| l16 | screens[7].prose | Arithmetic Asian has no formula; the geometric has, since the log of a geometric mean is normal; closed form 5.9402; rho = 0.9996 | correct | Kemna and Vorst (1990); G 4.1.2 example; script |
| l16 | screens[7] table, widget, explain | Plain 6.1722 (0.0269); control 6.1561 (0.00075), 6.1558 (0.00074); factor about 1,281; plain within 1 SE | correct | script |
| l16 | screens[8] table, options, explain | Straddle 16.0241; variance 175.1; pair correlation +0.645; pair variance 144.0; efficiency 0.61 | correct | script |
| l16 | screens[8].feedback.correct | Antithetics are sure to help a payoff that is monotone in z | correct | G 4.2 (monotone payoff gives negative covariance) |
| l16 | screens[8].feedback.byKey.better | They help only when the payoff moves in opposite ways at z and -z | correct | Cov(f(Z), f(-Z)) < 0 is the condition, G 4.2 |
| l16 | screens[9].widget.solution | mc_control: b from np.cov over np.var(ddof=1), adjusted payoffs y - b(x - S0), SE from their sd | correct | standard practice, G 4.1.3; script: 7 tests and example pass; starter fails all 7 |
| l16 | screens[9].widget.solution | mc_antithetic: n // 2 pairs, one average a pair, SE over pairs, ValueError under two pairs | correct | G 4.2 (pairs are the i.i.d. units) |
| l16 | screens[9].widget.tests, canvas | 10.4483678008, 0.0177639559, 0.6730735597; 10.4721465633, 0.0329335968; vrf(0.9245) = 6.8823 | correct | script |
| l16 | screens[9].explain | "Count the error over pairs, not payoffs, or it comes out too small" | wrong | script: for this call the SE over 100,000 payoffs is 0.0466, larger than 0.0329 over pairs, because the pair correlation is -0.501. It is too small only when the pairs are positively correlated. G 4.2. Finding 1 |
| l16 | screens[10].widget.starter | geometric_asian_call: mean log S0 + (r - sigma^2/2) mean(t), variance sigma^2/m^2 times the sum of min(t_i, t_j) | correct | Kemna and Vorst; script: simulated control mean agrees within 3 SE |
| l16 | screens[10].widget.solution, tests | asian_geometric_cv; SE below 0.002; within 3 SE of 6.156 for seeds 0 and 1 | correct | script: 5 tests and example pass; starter fails 4 (the fifth tests the supplied function) |
| l16 | screens[10].explain | "The control's mean 5.9402 is exact, so no bias enters" | imprecise | no bias from the mean; b fitted on the same paths leaves an O(1/n) bias. Finding 4 |
| l16 | screens[11].prose | A control with rho = 0.9995, "as a European is for a barrier" | imprecise | script: for the course's own H = 90 down-and-out call the European payoff has rho = 0.96 (monthly) and 0.93 (daily), a factor of 14 and 8. Finding 2 |
| l16 | screens[11].widget, feedback | Factor 1,000, so 36,000 s become 36 s; slips 18 and 0.01 | correct | arithmetic |
| l16 | screens[11].explain | "A European for a barrier and the geometric for the arithmetic Asian are the standard pairs" | imprecise | the Asian pair is standard (G 4.1.2); the European tracks a barrier far less well. Finding 2 |
| l16 | summary.ideas[0], [1], formula, note | Control estimator, b*, residual Var(Y)(1 - rho^2); 6.88 and about 1,300; the control must have a known mean | correct | G 4.1.1; script |
| l16 | summary.ideas[2] | Antithetic pairs halve the call's variance, but hurt a straddle | correct | script (for the at-the-money straddle of the lesson) |
| l16 | summary.trap | "for a payoff that rises on both sides they increase the variance" | imprecise | script: abs(S_T - 70) rises on both sides of 70 and has pair correlation -0.92. The sign of Cov(f(Z), f(-Z)) decides. Finding 3 |
| l16 | quiz[0] all | rho = 0.9: 5.26; slips 10 and 0.81 | correct | arithmetic |
| l16 | quiz[1] all | Using Y as its own control needs E[Y], the unknown price; a control needs a known mean | correct | G 4.1.1 |
| l16 | quiz[1].widget.options[2].why | The bias from an estimated b is tiny | correct | script; G 4.1.3 |
| l16 | quiz[2] all | For a put b* is negative; half-year 95 put gives -0.292 | correct | script |
| l17 | screens[0] console, table, explain | bs 10.450583572185565; cn 10.449919918096366; gl 10.450583572185309; mc (10.448367800848034, 0.017763955941256515); crr 10.446585136446535; errors -0.000664, -0.0022, -0.0040, -2.6e-13 | correct | script (the last digits may differ under Pyodide NumPy 2.0.2; the lesson rounds them) |
| l17 | screens[1] tokens | Crank-Nicolson: discretisation O(dS^2 + dt^2) | correct | MM 2.10 |
| l17 | screens[1] tokens | Gauss-Legendre: the cut at z = 8 plus a rule error that falls faster than any power | correct | TB and Trefethen, *Approximation Theory and Approximation Practice* ch. 19 (geometric convergence for analytic integrands) |
| l17 | screens[1] tokens | Monte Carlo: statistical, s / sqrt(n), a band | correct | G 1.1 |
| l17 | screens[1] tokens | Tree: order 1/n with an even-odd zigzag | correct | Diener and Diener (2004); Hull 21.3; script |
| l17 | screens[1].hints, explain | Tree error halves with the steps, the grid's quarters; Monte Carlo alone has a random error | correct | script |
| l17 | screens[2] table, widget, feedback | Errors -2.65e-3, -6.64e-4, -1.66e-4, -4.15e-5; slips -8.3 and +4.15 | correct | script |
| l17 | screens[2].explain | "A bound comes from that pattern" | imprecise | refinement gives an estimate (a third of the last change, Richardson), not a bound. NR 17.3; Higham 1.2 on the difference. Finding 10 |
| l17 | screens[3] all | Seed 1: 10.4275, SE 0.0177, -1.30 SE; seed 0 at -0.12 SE; both inside 1.96 | correct | script |
| l17 | screens[4] all | Tree errors -0.0040, -0.0020, +0.0018, -0.0010; even below, odd above; halve with the steps | correct | script |
| l17 | screens[5] table, widget, explain | Put: 5.170209; CN 5.169608; GL 5.170208971851; MC 5.1672 (0.0181), -0.17 SE; tree 5.170502 | correct | script |
| l17 | screens[6] table | Smax = 300, N = 200: errors -0.00151, +0.00091, -0.00131 at M = 390, 400, 420 | correct | script |
| l17 | screens[6] correct option, hints | At M = 400 the strike lies between nodes, so the start values misplace the kink | correct | TR ch. 4 (grid alignment); script |
| l17 | screens[6].widget.options[1..3].why | Rounding about 1e-13; same Smax in the other rows; CN stable at every step | correct | script |
| l17 | screens[6].explain | K and S0 sit a third of the way between nodes; the smeared kink and the interpolation each add about +0.0012 | correct | script: kink alone +0.00118; interpolation half gamma h^2 (1/3)(2/3) = +0.00117 |
| l17 | screens[7] all | Agreement to a penny is not a test; a penny is about 15 times the grid's error; check each error against its own prediction | correct | 0.01 / 0.00066 |
| l17 | screens[8].prose | Put edges V(0) = K e^(-r tau), V(Smax) = 0; put quadrature from -8 to z* | correct | Hull 21.8 |
| l17 | screens[8].widget.starter docstring | "quad" is Gauss-Legendre "from the kink to z = 8" | imprecise | true for the call; the put runs from -8 to the kink, as the prose and solution say. Finding 14 |
| l17 | screens[8].widget.solution | cn_price with both edges, gl_price split at the kink, mc_price with the share as control, three_prices with ValueError | correct | script: 9 tests and example pass; starter fails all 9; cn_price equals own march |
| l17 | screens[8].hints, explain | For a put the bottom edge enters the first equation with theta dt alpha_1 K e^(-r tau); b is negative for the put | correct | derivation; script |
| l17 | screens[9] options | Note lines: grid with error and rate; Monte Carlo 10.4484 plus or minus 0.035 at 95%, halving with four times the paths; where each fails | correct | 1.96 times 0.0178 |
| l17 | screens[9].widget.options[3..4].why, explain | Six decimals or a penny test hide the real errors | correct | script |
| l17 | summary all | Three prices with errors; grid quarters, quadrature vanishes with the nodes, Monte Carlo is a band; tree O(1/n) with a zigzag; off-node strike flips the error | correct | script |
| l17 | quiz[0] all | Quote 10.45 plus or minus 0.035 at 95% | correct | arithmetic |
| l17 | quiz[1] all | A 10-share basket: only Monte Carlo; 100 nodes a side is 1e20 nodes; 32^10 nodes | correct | G 1.1 |
| l17 | quiz[2] all | Even and odd trees zigzag, about 2/n away; the average of 1,000 and 1,001 errs near -1e-4 | correct | script |
| review-4 | items[0] all | M = 150 needs N >= 901; slips 900 and 7; 2.25 times 401 | correct | script |
| review-4 | items[1] all | Error at dS = 0.5 about -0.00049; M=400, N=6,401 gives -0.00045 | correct | script |
| review-4 | items[2] all | CN at nu = 50: factor -99/101 = -0.980; alternates and loses 2% a step; gamma shows it first | correct | arithmetic; l14 |
| review-4 | items[2].widget.options[1].why | CN's factor stays inside (-1, 1) for every nu | correct | for omega > 0; equals 1 only at omega = 0 |
| review-4 | items[3] options | Thomas work grows like M | correct | MM 2.9 |
| review-4 | items[3].feedback.correct, explain | "About 3M operations a step"; an implicit step costs little more than an explicit one | imprecise | 8M operations, 5M multiplications and divisions. Finding 8 |
| review-4 | items[4] all | 0.12 to 0.03 needs 640,000 paths; slips 160,000 and 80,000 | correct | arithmetic |
| review-4 | items[5] all | Ten times the paths shrink the band around 9.15 by sqrt(10); gap of about 0.49 stays | correct | script |
| review-4 | items[5].explain | "The Broadie-Glasserman shift" predicts 9.174 | imprecise | Broadie, Glasserman and Kou. Finding 13 |
| review-4 | items[6] all | rho = 0.95 gives 10.26; slips 20 and 0.9025; half again from 6.88 | correct | arithmetic |
| review-4 | items[7] all | Pairs hurt the straddle; put, call and digital are monotone in z | correct | script (put and digital pair correlations negative) |
| review-4 | items[8] all | z* = -0.15; with the kink inside, 32 nodes err by about 0.12; the cut at 8 is the truncation | correct | script |
| review-4 | items[8].explain | Gauss-Legendre is exact for polynomials, so it is fast on smooth integrands | correct | exact to degree 2n - 1, NR 4.6 |
| review-4 | items[9] all | Implicit Euler factor 1/(1 - h lambda) = 1/41 = 0.0244 at h lambda = -40; slips -39 and 0.0256; theta = 1 on a grid | correct | Hairer and Wanner IV.3 |
| homework-4 | items[0] all | 1 + b_80 = 0.4879; slips -0.5121 and 0.488; 0.2158 at j = 99; 0.0198 at N = 400; negative near the top below N = 393 | correct | script |
| homework-4 | items[1].widget.lines o1 to o5 | Weights sum to 1 - r dt; a_j, c_j > 0 for j >= 2 and a_1 multiplies V_0 = 0; non-negative weights give a weighted average; the maximum cannot grow; 1 + b_j >= 0 gives the bound | correct | maximum principle, MM 2.11 (a sufficient condition, stated as such) |
| homework-4 | items[1].widget.lines[5].why, feedback.byKey.d1 | The sum below 1 is not enough: a negative weight amplifies alternating errors | correct | script (N = 300) |
| homework-4 | items[2] all | Theta factor (1 - (1 - theta) z)/(1 + theta z); in (-1, 1] for theta >= 1/2; limit -(1 - theta)/theta | correct | script |
| homework-4 | items[3] all | rho = 0.98: 39,600 paths, a factor of 25.3; slips 20,000 and 960,400 | correct | arithmetic |
| homework-4 | items[4].prose | "Broadie and Glasserman" correct a barrier checked every dt | imprecise | Broadie, Glasserman and Kou. Finding 13 |
| homework-4 | items[4] widget, feedback, explain | Shifted daily barrier 89.34; slips 90.66 and 87.02; a lower barrier knocks out fewer paths, so the daily option is dearer | correct | script; BGK |
| homework-4 | items[5] all | n-node Gauss-Legendre is exact to degree 2n - 1; 32 nodes give 63; slips 32 and 64 | correct | NR 4.6 |
| homework-4 | items[6].widget.starter docstring | Grid: double M and N until two prices differ by under tol, report the last difference over 3 | correct | Richardson for a second-order method: error of the finer price is about a third of the change |
| homework-4 | items[6].widget.starter docstring | Quadrature: report the last difference; Monte Carlo: double paths until SE < tol | correct | the difference bounds the finer rule's error from above when convergence is fast; G 1.1 |
| homework-4 | items[6].widget.solution, tests | price_report: all 10 tests and the example pass; starter fails all 10 | correct | script |
| homework-4 | items[6].explain | Put: grid stops at M = 320 with error -9.4e-4, matching its estimate; quadrature at 16 nodes; Monte Carlo at 2,560,000 paths, SE 0.0036 | correct | script |
| homework-4 | items[7].prompt | "Say why the Monte Carlo figure is a band and the others are bounds" | imprecise | the deterministic figures are error estimates. Finding 10 |
| homework-4 | items[7].model, grid | 10.449920, error -6.6e-4, O(dS^2 + dt^2), refinement ratios of 4, doubling costs four times and quarters the error, strike on a node | correct | script |
| homework-4 | items[7].model, grid | "Its sign and size are predictable, so it is a bound" | imprecise | Finding 10 |
| homework-4 | items[7].model, quadrature | 32 nodes on [z*, 8], error -2.6e-13, kink at an end point, the cut at 8 is what is left, needs a known density | correct | script: the cut loses about 3e-13 |
| homework-4 | items[7].model, Monte Carlo | 10.4484, SE 0.0178, s cut from 14.72 to 5.61 (factor 6.88), plus or minus 0.035, seed 1 lands 1.30 SE below, four times the paths halves it | correct | script |
| homework-4 | items[7].model, why a band | Grid and quadrature errors are deterministic and repeatable; the Monte Carlo error is random | correct | G 1.1 |
| homework-4 | items[7].model, before going live | Check grid gamma against 0.018762 at the production step count; N = 10 gave 1.2526 | correct | script |
| homework-4 | items[7].rubric[0..3], [5] | Rubric lines restate the prices, orders, measurements and one live check | correct | as the model |
| homework-4 | items[7].rubric[4] | "the others are bounds: random against deterministic error" | imprecise | Finding 10 |

## Delta

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l5 | screens[8].widget.starter docstring (bisect) | Halve [lo, hi] until hi - lo < tol, or until no double lies between the ends | correct | script: tol = 1e-17, 0 and -1 all stop within one float gap of the root in under 60 calls; a root at 1e-300 with tol 0 stops too |
| l5 | screens[8].widget.starter docstring (bisect) | If f is zero at an end, return that end | correct | script (both ends, and the par bond at yield 0) |
| l5 | screens[8].widget.starter docstring (bisect) | Raise ValueError if f(lo) and f(hi) have the same sign: compare signs, not a product | correct | script: values near 1e-200 of either sign raise; a product would underflow to 0 |
| l5 | screens[8].widget.solution (bisect) | Returns the midpoint of the last bracket, so the error is at most tol / 2; an exact zero at a midpoint is still found | correct | script; NR 9.1 |
| l5 | screens[8].widget.solution (bisect) | Sound for any pair of ends that bracket a root | imprecise | script: bisect(f, 2.0, 1.0, 1e-12) returns 1.5 after 2 calls, with no error, because the loop test hi - lo >= tol is false at once. Finding 15 (delta) |
| l5 | screens[8].widget.tests, how | 15 hidden tests pass on the solution and fail on the starter; 40 to 44 calls; tol = 1e-17 stops within 200 calls | correct | script |
| l5 | screens[8].hints[0], explain | A product of tiny values can underflow to 0; bisection uses 42 calls, secant 9, Newton 6 | correct | script |
| l6 | screens[7].prose, starter docstring (safe_newton) | Newton when the step stays inside the bracket and is at most half the step before last, else bisect; start at the midpoint | correct | NR 9.4 (rtsafe uses the same step-before-last test); solution matches |
| l6 | screens[7].prose, docstring | Return early once abs(f(x)) <= ftol, which bounds the residual, not the error; ftol = 0 stops on the step alone | correct | script: (x-1)^9 stops near 1.046 with the default ftol and reaches 1 with ftol = 0 |
| l6 | screens[7].docstring | Zero at an end returns that end; ValueError without a sign change; RuntimeError after maxit | correct | script (ends, 1e-200 values, a 20-step cap on a wide bracket) |
| l6 | screens[7].widget.solution | Zero slope: the sentinel lo - 1.0 forces a bisection | correct | script; with the ends given as (hi, lo) the sentinel can fall inside the bracket, which is still a valid safeguarded point and the root is reached |
| l6 | screens[7].widget.solution | Tolerance below one float gap: xtol = 1e-17 with ftol = 0 stops within a float gap of the root; xtol = 0 ends in RuntimeError | correct | script; matches the documented cap |
| l6 | screens[7].widget.solution | Robust on random smooth functions and wide brackets | correct | script: 3,000 random problems solved to 1e-8, at most 23 calls of f |
| l6 | screens[7].widget.tests, how | 9 hidden tests pass on the solution, fail on the starter; at most 60 calls | correct | script |
| l6 | screens[7].explain | Sign comparison with f(lo) handles rising and falling f; plain Newton from 0 cycles between 0 and 1 on x^3 - 2x + 2; a zero slope costs one bisection | correct | script |
| l6 | screens[8].prose (implied_vols) | A mask chooses Newton or midpoint strike by strike; a second mask leaves a strike alone once its step is below tol | correct | solution |
| l6 | screens[8].prose | brentq agrees with the result to 1e-10; Brent mixes bisection, secant and inverse quadratic steps | correct | script (worst gap below 1e-10); NR 9.3 |
| l6 | screens[8].widget.starter docstring | Implied vols for a whole smile, "NaN where none exists"; bracket [1e-4, 5], start 0.2 | correct | script: a call quoted below its bound gives NaN alone and beside a good quote; 300 random smiles with 10% impossible quotes all return NaN there and 1e-6 accuracy elsewhere |
| l6 | screens[8].widget.solution | Deep in and out of the money strikes, T from one day to ten years, vols 2% to 300% | correct | script: 9,849 recoverable quotes, worst error 1.2e-11 |
| l6 | screens[8].widget.solution | Behaviour at the iteration cap | misleading | script: with maxit = 3, five of the eleven strikes come back as ordinary numbers up to 0.155 from the root; safe_newton on the previous screen raises RuntimeError in the same case. Finding 16 (delta) |
| l6 | screens[8].widget.tests, how | 4 hidden tests pass on the solution, fail on the starter; 1,000 strikes under a second | correct | script |
| l6 | screens[8].hints, explain | Price rises with sigma, so move lo where f < 0; the 75 and 80 puts take the midpoint first | correct | script |
| l10 | screens[7].prose | Call is e^(-rT) times the integral of (S_T(z) - K) phi(z) over [z*, 8], z* = (ln(K/S0) - (r - sigma^2/2)T)/(sigma sqrt(T)); the put integrates K - S_T over [-8, z*] | correct | Hull 15 appendix (risk-neutral expectation); script |
| l10 | screens[7].widget.starter docstrings | Clip the kink z* to [-zmax, zmax] | correct | script: kink below -8 (one-week call at 50) and above +8 both handled; clipped side integrates to 0 |
| l10 | screens[7].widget.solution | gl_integrate maps leggauss nodes to [a, b]; exact on x^2 and x^5 - x; e^x to 1e-14 | correct | script; NR 4.6 |
| l10 | screens[7].widget.solution | Deep in and out of the money strikes | correct | script: strikes 20 to 1,000, four (T, sigma) pairs, 64 nodes: worst error 1.2e-11 against Black-Scholes |
| l10 | screens[7].widget.tests, how | 8 hidden tests pass on the solution, fail on the starter | correct | script |
| l10 | screens[7].explain | Splitting at z* leaves a smooth integrand, so 16 nodes reach 1e-8; parity checks both; the far call's piece [z*, 8] is short and smooth | correct | script (z* = 3.32 at K = 200) |
| homework-2 | items[6].prose | Solve every bond at once by a safeguarded Newton on [0, 1], starting at c | correct | solution; it starts a zero-coupon bond at 0.05 rather than 0, which changes no result |
| homework-2 | items[6].prose, docstring | A price above the sum of the cash flows needs a negative yield: return NaN; NaN where no yield in [0, 1] fits | correct | script: both ends of the bracket, and 5,000 random bonds with 10% bad prices |
| homework-2 | items[6].widget.solution | Yields 0 to 95%, maturities 1 to 50, coupons 0 to 15% | correct | script: worst error below 1e-9 |
| homework-2 | items[6].widget.solution | Behaviour at the iteration cap | misleading | script: with maxit = 2, 199 of 200 bonds come back as unconverged numbers. Finding 17 (delta) |
| homework-2 | items[6].widget.tests, how | 6 hidden tests pass on the solution, fail on the starter | correct | script |
| homework-2 | items[6].explain | The bracket test f(0) >= 0 >= f(1) sends impossible prices to NaN before the loop; one pass moves every unsolved bond | correct | solution |
