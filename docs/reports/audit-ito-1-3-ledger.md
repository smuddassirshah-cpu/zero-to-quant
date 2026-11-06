# Claim ledger: ito L1 to L3 (concept audit, blind)

Auditor: Fable, 6 Nov 2026. Scope: `app/content/courses/ito/` lessons l1 to l12, review-1 to review-3, homework-1 to homework-3. Verdicts: correct, wrong, imprecise, misleading, unverified. Basis: a named source (Shreve = *Stochastic Calculus for Finance II*; KS = Karatzas and Shreve, *Brownian Motion and Stochastic Calculus*; Øksendal = *Stochastic Differential Equations*, 6th ed.; Williams = *Probability with Martingales*; Hull = *Options, Futures and Other Derivatives*; C&B = Casella and Berger), a short derivation, or `sim: <script>:<check>` naming an assert in `docs/reports/ito-L<n>-concepts.py`. File names are relative to `app/content/courses/ito/`.

## Level 1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1-walk-to-bm.json | screens[0].widget.answer, explain.text | 16 independent steps of ±1/4 have endpoint variance 16 × 1/16 = 1 | correct | Var of a sum of independent terms adds (C&B Thm 4.5.6); sim: L1:scaled_walk_var |
| l1-walk-to-bm.json | screens[0].feedback.byKey.sizes | "Variances add, and one step's variance is (1/4)²" | correct | same |
| l1-walk-to-bm.json | screens[1].widget.options[0] | spread of the endpoint stays the same as n grows; most paths within 2 of 0 | correct | Var = n × 1/n = 1 for every n; P(|N(0,1)| < 2) = 0.954 |
| l1-walk-to-bm.json | screens[1].widget.options[1].why | the unscaled walk grows like √n; scaling by 1/√n cancels it | correct | Var(S_n) = n (Shreve 3.2.1) |
| l1-walk-to-bm.json | screens[1].widget.options[3].why, explain.text | paths get rougher, not smoother, as n grows; the limit is a random continuous curve | correct | Donsker / Shreve 3.2.5; continuity of the limit: KS 2.4 |
| l1-walk-to-bm.json | screens[2].prose, explain.text | Var(cS_n) = c²n, c = 1/√n; any other power sends the variance to 0 or ∞ | correct | Var(cX) = c²Var(X); n^{1-2a} → 0 or ∞ unless a = 1/2 |
| l1-walk-to-bm.json | screens[3].explain.text | by time t the walk has nt steps of variance 1/n, so Var(W_t) = t; sd √t | correct | Shreve 3.2.2 (scaled random walk) |
| l1-walk-to-bm.json | screens[4].prose, explain.text | by the CLT W_1 ~ N(0, 1); P(W_1 > 1) = 1 − Φ(1) = 0.1587 | correct | Shreve 3.2.3 (CLT for the scaled walk); Φ(1) = 0.8413 |
| l1-walk-to-bm.json | screens[4].feedback.byKey.two | 0.3173 is the two-sided chance | correct | 2(1 − Φ(1)) = 0.3173 |
| l1-walk-to-bm.json | screens[5].widget.options[0], explain.text | steps of 1/n give endpoint variance 1/n → 0: a flat line at 0, by the law of large numbers | correct | Var = n × 1/n² = 1/n; WLLN (C&B 5.5.2) |
| l1-walk-to-bm.json | screens[5].widget.options[3].why | blowing up needs steps bigger than 1/√n | correct | Var n^{1-2a} → ∞ iff a < 1/2 |
| l1-walk-to-bm.json | screens[6].prose, explain.text | biased coin p = 1/2 + μ√Δt/2 gives step mean μΔt and limit μt + W_t | correct | step mean (2p−1)√Δt = μΔt; step variance Δt(1 − μ²Δt) → Δt; Shreve 3.2 scaled walk with drift; sim: L1:biased_walk_moments |
| l1-walk-to-bm.json | screens[6].explain.text | "the spread is still about 1, as p barely moves from 1/2" | correct | variance per step Δt(1 − μ²Δt) |
| l1-walk-to-bm.json | screens[7].prose, explain.text | W_t ~ N(0, t), sd √t; spread grows like √t; W_4 ~ N(0, 4); Shreve 3.2 builds BM from scaled walks | correct | Shreve Def 3.3.1 and section 3.2 |
| l1-walk-to-bm.json | screens[8].widget.solution, explain.text | code: cumsum of ±1 over √n is the scaled walk; sample variance (ddof = 1) of W_1 on 10,000 walks is within one se (0.014) of 1 | correct | se of a sample variance of N(0,1) ≈ √(2/n) = 0.0141; sim: L1:scaled_walk_code |
| l1-walk-to-bm.json | screens[9].prose, explain.text | 10-day VaR = √10 × 1-day VaR when daily moves are independent with equal variance (and the same shape) | correct | sd of a sum of 10 iid terms is √10 sd; Hull ch. 22 (time-horizon rule) |
| l1-walk-to-bm.json | screens[9].explain.text | the rule fails under positive autocorrelation (true figure larger) and under fat tails (the 99% point is no fixed number of sds) | correct | AR(1) variance of a 10-day sum exceeds 10σ² for φ > 0 (derivation in sim: L1:var_scaling_autocorr); heavy-tail quantile ratio ≠ √10 (sim: L1:var_scaling_fat_tails) |
| l1-walk-to-bm.json | summary.ideas[1], summary.formula | S_{⌊nt⌋}/√n → W_t in distribution; scale c/√n gives cW_t | correct | Donsker's theorem (KS 2.4.20); Shreve 3.2 |
| l1-walk-to-bm.json | quiz[0] | 900 steps of ±1/30 have sd 1 | correct | 900/900 = 1 |
| l1-walk-to-bm.json | quiz[1].explain.text | P(W_4 > 2) = 1 − Φ(1); a level of √t at time t is one sd away, so the chance is the same at every t | correct | W_t/√t ~ N(0, 1) |
| l1-walk-to-bm.json | quiz[2] | scaling by n^{-0.4} gives variance n^{0.2} → ∞; a power below −0.5 gives 0 | correct | n × n^{-0.8} |
| l1-walk-to-bm.json | quiz[3] | √10 understates 10-day risk under positive autocorrelation; negative autocorrelation makes it overstate; the level of volatility does not matter | correct | Var(sum) = 10σ² + 2σ²Σ(10−k)ρ_k; sim: L1:var_scaling_autocorr |
| l2-normal-increments.json | screens[0].explain.text | Var(W_3 − W_1) = 2; an increment over length t − s has variance t − s, independent of where the path stood | correct | Shreve Def 3.3.1 (ii) and (iii) |
| l2-normal-increments.json | screens[1].widget.options[0], explain.text | Corr(W_1, W_t) = 1/√t, falling with t | correct | min(1, t)/(1 × √t); sim: L1:cov_min |
| l2-normal-increments.json | screens[1].widget.options[2].why | independence holds for increments, not for values | correct | Shreve 3.3.1 |
| l2-normal-increments.json | screens[2].prose, explain.text | W_1 and W_3 − W_1 are independent increments; Cov(W_1, W_3) = 1; Cov(W_s, W_t) = min(s, t) | correct | Shreve Thm 3.3.2 (eq. 3.3.3 region); derivation screens[4] |
| l2-normal-increments.json | screens[3].explain.text | Corr(W_s, W_t) = √(s/t) for s < t; 1/√3 = 0.5774 | correct | s/(√s√t) |
| l2-normal-increments.json | screens[3].feedback.byKey.rest | 0.8165 = √(2/3) is the share of W_3's sd from the later increment | correct | √((t−s)/t) |
| l2-normal-increments.json | screens[4].widget.lines a1 to a5 | derivation of Cov = min(s, t): split, bilinearity, Var(W_s) = s, independence kills the cross term | correct | Shreve 3.3.2; bilinearity of covariance (C&B 4.5) |
| l2-normal-increments.json | screens[4].widget.lines[5].why (d1) | W_s and W_t are not independent | correct | Cov = s ≠ 0 |
| l2-normal-increments.json | screens[4].widget.lines[6].why (d2) | Cov(W_s, W_t − W_s) = 0, not t − s | correct | independence of increments |
| l2-normal-increments.json | screens[5].explain.text | Var(2W_1 − W_2) = 2, by increments or by 4 + 2 − 4 | correct | 2W_1 − W_2 = W_1 − (W_2 − W_1), two independent N(0,1); sim: L1:var_linear_combos |
| l2-normal-increments.json | screens[5].feedback.byKey.half | the cross term is 2ab Cov = −4 | correct | a = 2, b = −1, Cov = 1 |
| l2-normal-increments.json | screens[6].explain.text | two independent days of sd 1 have sd √2; adding sds is right only in lockstep | correct | Var adds; perfect correlation gives (σ_1 + σ_2)² |
| l2-normal-increments.json | screens[7].explain.text | sd of ΔW/Δt is 1/√Δt, growing without bound; "so no slope exists anywhere"; paths continuous everywhere and differentiable nowhere | imprecise | the sd argument shows the difference quotient at a fixed t diverges in probability (no derivative at any fixed time a.s.); nowhere differentiability of almost every path is the Paley, Wiener and Zygmund theorem (KS Thm 2.9.18; Shreve 3.3 remarks). Conclusion true, the "so" overreaches |
| l2-normal-increments.json | screens[8].prose | the four defining properties: W_0 = 0, W_t − W_s ~ N(0, t − s), independent increments over disjoint intervals, continuous paths | correct | Shreve Def 3.3.1 |
| l2-normal-increments.json | screens[8].widget.options, explain.text | X_t = √t Z has N(0, t) marginals, X_0 = 0, continuous paths, but increments are not independent; Cov(X_1, X_2) = √2 | correct | X_2 − X_1 = (√2 − 1)Z; Cov = √1·√2; sim: L1:sqrt_t_Z_not_bm |
| l2-normal-increments.json | screens[9].widget.solution, explain.text | code: cumsum of N(0, T/n) steps; np.cov divides by n − 1; the sample covariance at (0.3, 0.7) over 10,000 paths has se about 0.0055 | correct | Var of sample cov of bivariate normal = (σ_x²σ_y² + c²)/n = (0.21 + 0.09)/10⁴, sd 0.0055; sim: L1:cov_min |
| l2-normal-increments.json | screens[10].explain.text | Corr(5-day, 10-day P&L) = √(5/10) for any σ | correct | min(5,10)σ²/(√5σ√10σ) |
| l2-normal-increments.json | summary.ideas[2] | paths continuous but nowhere differentiable | correct | KS Thm 2.9.18 |
| l2-normal-increments.json | quiz[0] | Var(W_5 − W_2) = 3, independent of everything up to time 2 | correct | Shreve 3.3.1 |
| l2-normal-increments.json | quiz[1] | Var(W_1 + W_2) = 5 | correct | 1 + 2 + 2·1; sim: L1:var_linear_combos |
| l2-normal-increments.json | quiz[2] | Cov(W_2, W_5) = 2 | correct | min(2, 5) |
| l2-normal-increments.json | quiz[3].explain.text | 2W_{t/4} is a Brownian motion; cW_{t/c²} is a BM for any c > 0; W_{2t}, √2W_t, W_t + t are not | correct | Brownian scaling (KS 2.9 Lemma 9.4; Øksendal Ex. 2.12); each failing candidate has Var ≠ t or mean ≠ 0; sim: L1:brownian_scaling |
| l3-quadratic-variation.json | screens[0] | sum of four squared increments of the reference path is 0.6639 | correct | arithmetic on the stated increments; sim: L1:reference_path_qv |
| l3-quadratic-variation.json | screens[1].widget.options[0], explain.text | Σ(ΔW)² settles near T = 1 as the grid refines; Σ|ΔW| keeps growing (51.36 at the finest grid) | correct | Shreve Thm 3.4.3; total variation infinite (Shreve 3.4.2 remark, KS 2.9.9); sim: L1:reference_path_qv |
| l3-quadratic-variation.json | screens[1].widget.options[1].why | Σ|ΔW| is the path's length | correct | first variation definition (Shreve 3.4.1) |
| l3-quadratic-variation.json | screens[2].widget.solution, tests | code: np.diff of the coarse grid, squared and summed; a straight line 0 to 1 in 100 steps has 0.01 | correct | Σ(1/100)² × 100 = 0.01; sim: L1:reference_path_qv |
| l3-quadratic-variation.json | screens[3].explain.text | each abs increment is about √(2Δt/π), so m of them add to about √(2m/π) = 51.06 at m = 4,096; four times the steps doubles the length | correct | E abs N(0, Δt) = √(2Δt/π) (C&B Ex. 2.3), m√(2/(πm)) = √(2m/π); sim: L1:total_variation_growth |
| l3-quadratic-variation.json | screens[4].widget.lines b1, b2, b3, b5 | E[(ΔW)²] = Δt; E[(ΔW)⁴] = 3Δt²; Var[(ΔW)²] = 2Δt²; the sum has mean T and variance 2TΔt → 0 | correct | Shreve proof of Thm 3.4.3; E[Z⁴] = 3; sim: L1:qv_moments |
| l3-quadratic-variation.json | screens[4].widget.lines[4].why (d1) | (ΔW)² is first order in Δt, not second | correct | E(ΔW)² = Δt |
| l3-quadratic-variation.json | screens[4].widget.lines[5].why (d2) | Var of the square is not the square of the variance; it is 3Δt² − Δt² | correct | fourth moment |
| l3-quadratic-variation.json | screens[4].explain.text | "so the sum converges to T" (mode unstated; it is mean-square, hence in probability) | correct | Shreve 3.4.3 proves L² convergence; a learner does not carry a wrong habit from the unstated mode |
| l3-quadratic-variation.json | screens[5].explain.text | sd of the sum at m = 4,096 is √(2/4096) = 0.0221; at m = 16 it is 0.354 | correct | √(2TΔt) |
| l3-quadratic-variation.json | screens[6].explain.text | for smooth f, (Δf)² ≈ f'²Δt² is second order; a Brownian step has size √Δt so its square is first order | correct | Taylor; Shreve 3.4 |
| l3-quadratic-variation.json | screens[7].explain.text | f = t² on [0,1] with m steps has Σ(Δf)² = 1,333,300/10⁸ ≈ 4/(3m) → 0: a smooth path has quadratic variation 0 | correct | Σ_{k<m}(2k+1)² = m(4m²−1)/3; Shreve 3.4.1 (f with continuous derivative has zero quadratic variation); sim: L1:smooth_qv |
| l3-quadratic-variation.json | screens[8].prose, explain.text | Σ|ΔW Δt| is about √Δt and Σ(Δt)² = TΔt, both → 0; table dW·dW = dt, dW·dt = 0, dt·dt = 0 | correct | Shreve 3.4.3 remarks (eqs 3.4.10 to 3.4.11); Σ|ΔW|Δt ≈ T√(2Δt/π); sim: L1:cross_variation_terms |
| l3-quadratic-variation.json | screens[9].prose, explain.text | [σW]_T = σ²T; 0.3W over [0, 2] has QV 0.18; QV reads σ² off a single path | correct | each square scales by σ²; realised variance (Shreve 3.4 remark on volatility) |
| l3-quadratic-variation.json | screens[10].explain.text | σ̂ = √(Σr²/T) with T = 0.5 for 126 trading days (252-day year) is realised volatility | correct | QV of σW over T is σ²T; 252-day convention stated as "half a year" |
| l3-quadratic-variation.json | screens[10].feedback.byKey.daily | 0.0127 is a daily volatility; annual divides by T in years | correct | √(0.02036/126) = 0.0127 |
| l3-quadratic-variation.json | summary.ideas, formula, trap | QV = T, mean T, variance 2TΔt; path infinitely long; multiplication table; (ΔW)² is first order | correct | as above |
| l3-quadratic-variation.json | quiz[0] | [2W]_3 = 12 | correct | 4 × 3 |
| l3-quadratic-variation.json | quiz[1].explain.text | Σ(ΔW)³ → 0: each cube has mean 0 and variance 15Δt³, sum variance 15TΔt² → 0; Σ|ΔW| → ∞; ΣΔW telescopes | correct | E[Z⁶] = 15; sim: L1:cubic_variation |
| l3-quadratic-variation.json | quiz[2] | Var Σ(ΔW)² over [0,2], Δt = 0.02 is 0.08 | correct | 2TΔt |
| l3-quadratic-variation.json | quiz[3] | (3dW + 2dt)² = 9dt | correct | table |
| l4-gbm.json | screens[0].explain.text | ln S_t = ln 100 + 0.06t + 0.2W_t; a path with W_1 = 0 is the median path | correct | ln S_1 is normal with median at W_1 = 0, exp is increasing |
| l4-gbm.json | screens[1].explain.text | median of S_1 is 100e^{μ−σ²/2}; falls from 107.79 (σ = 10%) to 90.48 (60%); mean fixed at 100e^μ = 108.33; the gap σ²/2 is the volatility drag | correct | lognormal median e^m, mean e^{m+v/2} (C&B Ex. 2.3.x, lognormal); 100e^{0.075} = 107.79, 100e^{−0.1} = 90.48; sim: L1:gbm_moments |
| l4-gbm.json | screens[2].prose, explain.text | GBM S_t = S_0 exp((μ − σ²/2)t + σW_t); E[S_1] = 100e^{0.08}; the −σ²/2 makes μ the mean growth rate | correct | Shreve 3.2.7 / 4.4.9; E e^X = e^{m+v/2}; sim: L1:gbm_moments |
| l4-gbm.json | screens[3].explain.text | P(S_1 < 100) = Φ(−0.3) = 0.3821; general P(S_T < K) = Φ((ln(K/S_0) − (μ − σ²/2)T)/(σ√T)) | correct | ln S_T normal; sim: L1:gbm_prob_below |
| l4-gbm.json | screens[4].explain.text | at σ = 60%, log drift −0.10, P(S_1 < 100) = Φ(0.1667) = 0.5662; the mean still rises to 108.33; positive μ says nothing about the typical path when σ is large | correct | same formula; sim: L1:gbm_prob_below |
| l4-gbm.json | screens[5].explain.text | σ = 0 gives S_t = S_0e^{μt}; mean = median; the gap e^{σ²t/2} exists only because of the noise | correct | mean/median ratio e^{σ²t/2} |
| l4-gbm.json | screens[6].prose, explain.text | exact log step S exp((μ − σ²/2)Δt + σ√Δt Z); Euler S(1 + μΔt + σ√Δt Z); Z = −6 with Δt = 1 gives 31.98 vs −12; the two differ by order σ²Δt; only the log step is exact at any Δt | correct | exact step has the law of S_{t+Δt} given S_t (Shreve 3.2.7); expansion of exp differs from Euler by σ²Δt(Z² − 1)/2 + O(Δt^{3/2}); sim: L1:euler_vs_exact |
| l4-gbm.json | screens[7].widget.lines c1 to c5 | E[S_t] = S_0e^{μt} via mgf E e^{σW_t} = e^{σ²t/2}; median via monotone exp | correct | normal mgf; quantiles commute with increasing maps |
| l4-gbm.json | screens[7].widget.lines[5].why (d1) | E e^X > e^{E X} for random X (Jensen) | correct | Jensen (Williams 6.6); strict for non-degenerate X |
| l4-gbm.json | screens[7].widget.lines[6].why (d2) | exp stretches the upper tail, so mean > median | correct | lognormal |
| l4-gbm.json | screens[8].widget.solution, explain.text | code: cumulative exact log steps; prob_below as the closed form; realised vol 0.1994 on the seed-4 path by sample sd × √252 | correct | 252-day annualisation is the stated convention; sim: L1:gbm_prob_below |
| l4-gbm.json | screens[9].prose, explain.text | se of the sample mean of S_1 over 10,000 paths is about £0.22 | correct | sd(S_1) = 21.88, /100 = 0.219; sim: L1:gbm_moments |
| l4-gbm.json | screens[10].widget.options, explain.text | £108.33 is the mean, £106.18 the median, the mode is 100e^{0.06−0.04} = 102.02, 38% chance of a loss | correct | lognormal mode e^{m−v} |
| l4-gbm.json | summary.ideas, formula, trap | GBM, drag, exact simulation, P(S_T < K) formula; 57% lose at σ = 60% | correct | as above |
| l4-gbm.json | quiz[0], quiz[1] | median of S_2 is 50e^{0.11} = 55.81; E[S_2] = 50e^{0.2} = 61.07 whatever σ | correct | formulas above |
| l4-gbm.json | quiz[2].widget.options, explain.text | the exact log step keeps prices positive; Euler and additive updates can go negative | correct | exp > 0 |
| l4-gbm.json | quiz[2].explain.text | "For small steps all three agree to first order." | wrong | the additive update S + μΔt + σ√Δt Z moves S by pounds, not by a proportion: its noise term differs from the GBM step's SσΔW by the factor S, so it disagrees at order √Δt whenever S ≠ 1 (it is arithmetic Brownian motion, a different model). Only the Euler and exact steps agree to first order. sim: L1:additive_update_not_first_order (EXPECTED_FAIL) |
| l4-gbm.json | quiz[3] | median flat when μ = σ²/2 = 4.5%; the mean still grows at 4.5%; half gain and half lose but the gains are bigger | correct | median formula; E[S_1] = S_0e^{0.045} |
| review-1.json | items[0].explain.text | E[W_t⁴] = 3t² (W_t = √t Z, E Z⁴ = 3, by parts E Z⁴ = 3E Z²) | correct | normal moments (C&B 2.3); sim: L1:w_fourth_moment |
| review-1.json | items[1].explain.text | 25-day VaR = 5 × 1-day; holds only if days are independent and the tails keep their shape | correct | as l1 screens[9] |
| review-1.json | items[2].explain.text | Var(W_1 + W_2 + W_3) = 14 by increments or by 6 + 2(1 + 1 + 2) | correct | sim: L1:var_linear_combos |
| review-1.json | items[3] | Corr(W_4, W_9) = 2/3 | correct | √(4/9) |
| review-1.json | items[4].prose | "X_t is a martingale if E[X_t | path up to s] = X_s for every s < t" (recap "from markov") | imprecise | drops E|X_t| < ∞ and adaptedness (Shreve Def 2.3.5; Williams 10.3). Recap of a definition made elsewhere; the full statement belongs in l8, see L2 rows |
| review-1.json | items[4].widget.options, explain.text | W_t² − t is a martingale; W_t² drifts up by t − s; W_t + 2t drifts; abs W_t has mean √(2t/π) rising with t so it is not a martingale | correct | Shreve Thm 3.3.4 (W is a martingale); W² − t by expanding (W_s + D)² with D independent of F_s, the explain's own derivation; E abs W_t = √(2t/π); a martingale has constant mean; sim: L1:martingale_conditional_means |
| review-1.json | items[5] | sd of Σ(ΔW)² over [0, 0.5] with Δt = 0.01 is 0.1; halving Δt shrinks the sd by √2 | correct | √(2TΔt) |
| review-1.json | items[6].explain.text | P(S_1 > 120) = 1 − Φ(0.6116) = 0.2704 | correct | formula; sim: L1:gbm_prob_below |
| review-1.json | items[7].explain.text | E[S_1²] = 10⁴e^{0.2}; Var(S_1) = 478.92; sd 21.88; general Var(S_t) = S_0²e^{2μt}(e^{σ²t} − 1) | correct | lognormal second moment e^{2m+2v}; sim: L1:gbm_moments |
| review-1.json | items[7].feedback.byKey.normal | treating S_1 as 100 × 0.2W_1 gives sd 20 | correct | linearisation |
| review-1.json | items[8].explain.text | Var(∫_0^2 W dt) = ∫∫min(s,t) = T³/3 = 8/3; A is normal with mean 0; averaging is why an Asian option is cheaper than a plain one | correct | Fubini with Cov(W_s, W_t) = min(s, t) (Shreve Thm 3.3.2); Gaussian integral of a Gaussian process; Asian cheaper because the average has lower variance than the terminal (Hull 26.3); sim: L1:integrated_bm_var |
| homework-1.json | items[0].widget.solution, explain.text | code: QV at m steps over many paths; sd ≈ √(2/m); sum converges to T in mean square | correct | Shreve 3.4.3; sim: L1:qv_moments |
| homework-1.json | items[1].prose, explain.text | X_t = W_0 + (W_1 − W_0)t + (B_t − tB_1) is pinned at both ends; Var(B_t − tB_1) = t − 2t² + t² = t(1 − t), largest at 1/2 | correct | Brownian bridge (Shreve 4.7.1 and 4.7.2); sim: L1:bridge_variance |
| homework-1.json | items[2].widget.lines e1 to e6 | Var(∫_0^T W dt) = T³/3 by swapping E and the integral and using E[W_sW_t] = min(s,t) | correct | Fubini (integrand is integrable); sim: L1:integrated_bm_var |
| homework-1.json | items[2].widget.lines[6].why (x1), [7].why (x2) | variance does not pass through the integral; E[W_sW_t] ≠ 0 for s ≠ t | correct | covariances count; min(s,t) > 0 |
| homework-1.json | items[3].widget.options, explain.text | W_t³ − 3tW_t, e^{W_t − t/2}, W_t² − t are martingales; W_t³, tW_t, e^{W_t} are not | correct | Shreve Thm 3.6.1 (exponential martingale), Hermite polynomials h_3; conditional expansions with D ⊥ F_s; sim: L1:martingale_conditional_means |
| homework-1.json | items[3].widget.options[4].why | E[tW_t | F_s] = tW_s ≠ sW_s | correct | martingale property of W |
| homework-1.json | items[4].explain.text | P(W_1 > 0, W_2 > 0) = 3/8: the wedge X > 0, Y > −X spans 135° and the density of (X, Y) is rotation-invariant | correct | iid N(0,1) pair is rotationally symmetric; also 1/4 + arcsin(1/√2)/(2π) = 3/8 (Sheppard); sim: L1:both_positive |
| homework-1.json | items[5].explain.text | E[W_s²W_t²] = 3s² + s(t − s) = 2s² + st | correct | expand with D ⊥ W_s, E W_s³D = 0; sim: L1:mixed_fourth_moment |
| homework-1.json | items[6].explain.text | X_4 = 0.5·4 + W_4 ~ N(2, 4), P(X_4 < 0) = Φ(−1); the chance of being down is Φ(−0.5√t), falling with t | correct | mean 0.5t, sd √t |
| homework-1.json | items[7].explain.text | σ̂ = √(Σr²/T) = 0.24; the drift adds about μ²T²/63 to Σr² | correct | Σ(mΔt + σ√Δt Z)² = σ²T + m²T²/n + cross term of mean 0 |
| homework-1.json | items[8].model section 1 | arithmetic BM price goes negative with chance Φ(−S_0/(σ√t)) > 0; moves in pounds not percentages | correct | P(S_0 + σW_t < 0) |
| homework-1.json | items[8].model section 2 | GBM log returns over disjoint periods are independent N((μ − σ²/2)Δt, σ²Δt); price lognormal | correct | Shreve 3.2.7 |
| homework-1.json | items[8].model section 3, rubric[2], rubric[3] | drag, mean 108.33, median 106.18; 57% lose at σ = 60% | correct | as l4 |
| homework-1.json | items[8].model section 4 | realised variance Σr² estimates σ²T; 0.1994 on the seeded year | correct | as l3 |
| homework-1.json | items[8].model section 5 | fat tails (October 1987 over 20 sd), volatility clustering, jumps, skew and leverage are departures from GBM | correct | Hull ch. 20 (volatility smiles) and ch. 23; 19 October 1987: −22.6% against a daily sd near 1% |
| homework-1.json | items[8].model section 6 | GBM gives closed forms and exact simulation; desks patch it with a volatility surface | correct | Hull 20 |
