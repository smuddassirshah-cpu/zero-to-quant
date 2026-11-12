# Claim ledger: limits-thm level 4 (blind concept audit, round 1)

Scope: `l14-joint-densities`, `l15-new-variables`, `l16-adding-densities`, `l17-smallest-and-largest`, `l18-gamma-beta`, `l19-generating-functions`, `review-4`, `homework-4`, `problems-4`. No `fluency-*.json` in the course has a lesson in l14 to l19.

Stage 1, full ledger. Every row was judged by hand. Paths: `sN` is `screens[N]`, `qN` is `quiz[N]`, `iN` is `items[N]`, `pN` is `parts[N]`. "script" means a check in `docs/reports/limits-thm-L4-concepts.py` (exact sympy integration, scipy closed form, or Monte Carlo with 400,000 draws). C&B is Casella and Berger, *Statistical Inference*, 2nd edition. Theorem numbers are given where I am sure of them and section numbers otherwise. F-numbers point to findings in `docs/reviews/audit-limits-thm-4.md`.

Conventions found: Gamma is written with shape $a$ and rate $\lambda$ throughout (l16, l18, review, problems), and the scale $1/\lambda$ is named once in l18 s3 as what libraries ask for. That matches SciPy (`scale`) and NumPy (`scale`). No SciPy or NumPy call appears in learner code. Exponential is by rate everywhere; `random.expovariate(rate)` in l17 s9 takes a rate, which is consistent.

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l14 | s0.prose | Independent default times at rates 1 and 2 have joint density $2e^{-x-2y}$ (canvas heat) | correct | product of exponential densities; script integrates to 1 |
| l14 | s0.key, canvas | "A first" is the triangle above the diagonal, $y > x$ | correct | polygon (0,0),(0,3.3),(3.3,3.3) lies above $y = x$ |
| l14 | s0.wrong swapped | Region below the diagonal has B first | correct | $y < x$ |
| l14 | s0.explain | Surface is highest near the origin | correct | $2e^{-x-2y}$ decreasing in both |
| l14 | s1.prose | Probability of a region is the volume under the surface | correct | C&B section 4.1 |
| l14 | s1.key | $P(A \text{ first}) = 1/3$ | correct | script: sympy exact, MC |
| l14 | s1.hints | Inner integral $e^{-x}e^{-2x}$, outer $\int e^{-3x} = 1/3$ | correct | derivation |
| l14 | s1.wrong half | 0.5 holds for equal rates | correct | symmetry |
| l14 | s1.wrong other | 0.6667 is P(B first) | correct | $1 - 1/3$ |
| l14 | s1.explain | Definition of a joint density | correct | C&B section 4.1 |
| l14 | s1.explain | "agrees with the rule $1/(1+2)$ for the faster clock to lose" | misleading | "lose" can mean default first, which is B at 2/3. F22 |
| l14 | s2.caption | $P(X \le a, Y \le b) = (1 - e^{-a})(1 - e^{-2b})$ | correct | product of marginal CDFs |
| l14 | s2.key | Rectangle volume is the product of the two single chances | correct | independence |
| l14 | s2.wrong sum | Sum is 1.4968, above 1 | correct | script |
| l14 | s2.wrong small | Equal to the smaller would mean $Y \le 1$ certain given $X \le 1$ | correct | $P(A \cap B) = P(A)$ iff $A \subset B$ a.s. |
| l14 | s2.wrong avg | An average lies between the two; the joint is below both | correct | $P(A \cap B) \le \min$ |
| l14 | s2.explain | $0.6321 \times 0.8647 = 0.5466$; density factors so chances multiply | correct | script; C&B Lemma 4.2.7 |
| l14 | s3.prose | Marginal $f_X(x) = \int f(x,y)\,dy$ | correct | C&B section 4.1 |
| l14 | s3.key | $f_X(x) = e^{-x}$ | correct | script |
| l14 | s3.wrong kept2 | The 2 belongs to $2e^{-2y}$, which integrates to 1 | correct | derivation |
| l14 | s3.wrong left-y | A marginal has no $y$ | correct | definition |
| l14 | s3.explain | Continuous version of summing a table's row | correct | analogy to discrete marginal |
| l14 | s4.prose | $f = 2$ on $0 \le y \le x \le 1$ has volume $\tfrac12 \times 2 = 1$ | correct | area of triangle |
| l14 | s4.key | $f_X(x) = 2x$ | correct | script |
| l14 | s4.wrong whole | 2 comes from integrating $y$ over $[0,1]$ | correct | $\int_0^1 2\,dy = 2$ |
| l14 | s4.wrong half | $x$ is the slice length without height 2 | correct | derivation |
| l14 | s4.explain | $f_Y(y) = 2(1 - y)$; $\int_0^1 2x = 1$ | correct | script |
| l14 | s5.key | $P(X + Y \le 1) = 1/2$ | correct | script exact |
| l14 | s5.hints | Shaded triangle base 1, height 1/2, area 1/4 | correct | vertices (0,0),(1,0),(.5,.5) |
| l14 | s5.wrong area | 0.25 is the area without height 2 | correct | derivation |
| l14 | s5.wrong all | 1 is the whole volume | correct | |
| l14 | s5.explain | With a flat density a probability is a share of area | correct | uniform on a region |
| l14 | s6.prose | Conditional density $f(y \mid x) = f(x,y)/f_X(x) = 1/x$ on $[0,x]$ | correct | C&B section 4.2 |
| l14 | s6.key | $E[Y \mid X = x] = x/2$ | correct | script |
| l14 | s6.wrong x | $x$ is the top of the slice | correct | |
| l14 | s6.wrong inv | $1/x$ is the conditional density's height | correct | |
| l14 | s7.key | Flat density on a triangle is dependent | correct | support not a product set |
| l14 | s7.wrong const | A constant splits only on a rectangle | correct | C&B Lemma 4.2.7 with indicator |
| l14 | s7.wrong range | Slices at 0.2 and 0.9 differ in length | correct | |
| l14 | s7.wrong marg | Every marginal depends on one variable; independence is joint = product | correct | definition |
| l14 | s7.hint | Product of marginals is $4x(1-y)$ | correct | script marginals |
| l14 | s7.explain | "independent only if its support is a rectangle and it factors on it" | correct | standard wording (Blitzstein and Hwang 7.1); a rectangle here means a product of intervals, sides may be infinite |
| l14 | s8.lines | $E[X] = 2/3$, $E[Y] = 1/3$, $E[XY] = 1/4$, Cov $= 1/36$ | correct | script exact |
| l14 | s8.explain | Non-zero covariance implies dependence | correct | contrapositive of independent implies uncorrelated |
| l14 | s9.prose | Region, marginal and conditional formulas | correct | C&B 4.1, 4.2 |
| l14 | s9.key | Independence is $f = f_Xf_Y$ at every point | correct | C&B section 4.2 (almost everywhere) |
| l14 | s9.wrong cov | Zero covariance says no straight-line link only | correct | C&B section 4.5 |
| l14 | s9.wrong flat | Triangle is the counterexample | correct | |
| l14 | s9.wrong mean | Equal conditional means at two points prove nothing | correct | |
| l14 | s9.explain | Fails as soon as the support is not a rectangle; a marginal says nothing about dependence | correct | |
| l14 | s10.key | Bivariate normal with $\rho = 0$ and the exponential pair are independent | correct | densities factor |
| l14 | s10.wrong sq | $X \sim U(-1,1)$, $Y = X^2$: covariance 0 and dependent | correct | script MC; $E[X^3] = 0$ |
| l14 | s10.wrong tri | Covariance 1/36, support not a rectangle | correct | |
| l14 | s10.explain | Uncorrelated implies independent for jointly normal variables | correct | C&B section 4.5; "jointly" is stated |
| l14 | s10.explain | "It fails for ... any other pair that is not jointly normal" | wrong | independent exponentials, or any two Bernoulli variables, are counterexamples. script. F1 |
| l14 | s11.prose | $1 + (2x-1)(2y-1)$ is a density on the unit square with uniform marginals | correct | script; FGM copula with $\theta = 1$ |
| l14 | s11.key | $P = 5/16 = 0.3125$ | correct | script exact |
| l14 | s11.wrong indep | 0.25 is the independent answer | correct | |
| l14 | s11.wrong half | 0.5 is one loan's chance | correct | uniform marginal |
| l14 | s11.explain | Dependence raises joint default by a quarter (0.3125 against 0.25) | correct | ratio 1.25 |
| l14 | s11.explain | Ignoring positive dependence understates joint tail risk | correct | follows from the item; standard credit result |
| l14 | summary.ideas | Volume, marginal, conditional, independence needs rectangular support | correct | as above |
| l14 | summary.trap | "zero covariance is not independence either, except for jointly normal pairs" | imprecise | not the only exception (two-valued variables). Folded into F1 |
| l14 | q0 | $f_X(0.5) = 1$ for $x + y$; slip 0.5 is the $x$ part | correct | script |
| l14 | q1 | $4xy$ is the only factorising density; the other three are valid densities that do not factor | correct | script |
| l14 | q2 | $E[Y \mid X = 0.5] = 0.25$; slip 0.5 is the slice end | correct | |
| l14 | q3 | $P(A \text{ first}) = 1/4$ at rates 1 and 3; slips 0.75 (B first), 0.5 (equal rates) | correct | $\lambda_A/(\lambda_A + \lambda_B)$ |
| l14 | q3.explain | General rule $\lambda_A/(\lambda_A + \lambda_B)$ | correct | Ross, *Introduction to Probability Models* 5.2.3; needs independence, stated in the prose |
| l15 | s0.prose | $-\tfrac12 \ln 0.5 = 0.3466$; half the draws have $u > 0.5$ | correct | script |
| l15 | s0.key | Density piles near 0 with a right tail | correct | Exp(2) |
| l15 | s0.wrong flat, bell, far | Each description of the map is right | correct | $g$ steep near 0, flat near 1 |
| l15 | s1.question | "The bars centre near 0.5" | misleading | 0.5 is the mean; the median is 0.35 and the mode is 0. F21 |
| l15 | s1.key | Rate 2 gives mean 0.5; slip 0.5 is the mean | correct | $1/\lambda$ |
| l15 | s1.explain | $-\tfrac12 \ln U$ is exponential with rate 2 | correct | script KS test |
| l15 | s2.lines | CDF method steps; inequality flips on multiplying by $-2$; $P(U \ge c) = 1 - c$ | correct | C&B Thm 2.1.3; valid for $y \ge 0$ |
| l15 | s2.explain | Density is the slope of the CDF | correct | |
| l15 | s3.prose | $f_Y(y) = f_X(x)\lvert dx/dy \rvert$ "with $g$ monotone" | imprecise | needs strictly monotone and differentiable (C&B Thm 2.1.5). Folded into F2 |
| l15 | s3.key | $2e^{-2y}$ | correct | script |
| l15 | s3.wrong nofac | $e^{-2y}$ is $f_U \cdot x$ | correct | $x = e^{-2y}$ |
| l15 | s3.wrong neg | Sign kept; a density is never negative | correct | |
| l15 | s3.wrong inv | "$\tfrac12 e^{-2y}$: you used $dy/dx$ upside down" | wrong | $\lvert dy/dx \rvert = e^{2y}/2$, not the option. script. F5 |
| l15 | s3.explain | Where $y$ is stretched the density thins by that factor | correct | |
| l15 | s4.prose | Lognormal density $f_X(\ln s)/s$ | correct | C&B 3.3 |
| l15 | s4.key | $f_S(2) = 0.1569$ | correct | script, MC |
| l15 | s4.wrong nofac, wayround | 0.3138 is $\varphi(\ln 2)$; 0.6276 multiplies by $s$ | correct | script |
| l15 | s5.prose | If $U$ is uniform, $F^{-1}(U)$ has CDF $F$; exponential inverse | correct | C&B Thm 2.1.10; $F$ continuous and strictly increasing here |
| l15 | s5.code | `exp_sample` solution passes all six tests; taught method is the inverse CDF | correct | script runs the tests |
| l15 | s5.tests | $P(Y > 1) = 0.1353$ at rate 2; mean 50 at rate 0.02 | correct | $e^{-2}$ |
| l15 | s5.explain | Mean of 100,000 draws within a percent of $1/\text{rate}$ | correct | se is 0.32% of the mean |
| l15 | s5.explain | Any invertible CDF gives a sampler | correct | |
| l15 | s6.prose | $Y = Z^2$: two branches, each with $1/(2\sqrt y)$ | correct | C&B Thm 2.1.8 |
| l15 | s6.key | $f_Y(1) = \varphi(1) = 0.2420$ | correct | script; chi-square(1) pdf |
| l15 | s6.wrong one, nofac | 0.1210 is one branch; 0.4839 is $2\varphi(1)$ without the factor | correct | script |
| l15 | s6.explain | Chi-square with one degree of freedom; unbounded at 0 with area 1 | correct | |
| l15 | s7.key | $Y = 3X$ has density 1/3 on $[0,3]$ | correct | |
| l15 | s7.wrong one, three, short | Areas 3, 9 and 1/3 | correct | arithmetic |
| l15 | s7.explain | A candidate that does not integrate to 1 has lost a factor | correct | necessary check, stated as a check |
| l15 | s8.lines | Box and Muller: $u_1 = e^{-r^2/2}$, Jacobian $re^{-r^2/2}/(2\pi)$, divide by $r$, factor | correct | Box and Muller (1958); C&B section 5.6 |
| l15 | s8.lines jac | "a triangular determinant" for a diagonal one | correct | diagonal is a special case |
| l15 | s8.explain | $X$, $Y$ independent $N(0,1)$ | correct | script runs the sampler tests |
| l15 | s9.code | `box_muller` passes seven tests; `1 - rng.random()` keeps the log finite | correct | script; `random()` is in $[0,1)$ |
| l15 | s9.explain | Mean, variance, 95% share, pair correlation as $N(0,1)$; no rejection step | correct | tests |
| l15 | s10.key | $P(\text{payoff} = 0) = \Phi(0.5) = 0.6915$ | correct | script, MC |
| l15 | s10.wrong tail, zero | 0.3085 is in the money; 0 confuses a point of $S$ with the atom | correct | |
| l15 | s10.explain | "A non-constant monotone $g$ keeps a density" | wrong | the screen's own $g = \max(s - 105, 0)$ is non-constant and monotone and has an atom. script. F2 |
| l15 | s10.explain | A $g$ constant on an interval leaves an atom there | correct | |
| l15 | s11.prose | Constant hazard 2% gives $T = -\ln(1-U)/0.02$ | correct | inverse CDF |
| l15 | s11.key | $100(1 - e^{-0.1}) = 9.516$ | correct | script; linearity of expectation needs no independence |
| l15 | s11.wrong linear, prob | 10 is rate times time times names; 0.0952 is one name | correct | |
| l15 | s11.feedback.correct | "$100 \times 0.0952 = 9.516$" | imprecise | the product shown is 9.52. F20 |
| l15 | s11.explain | Monte Carlo engines start from uniforms and transform them | correct | Devroye, *Non-Uniform Random Variate Generation*, ch. II; inversion is one of several methods, and the text says "any distribution with an invertible CDF" |
| l15 | summary.ideas[0] | "For monotone $g$" | imprecise | strictly monotone. Folded into F2 |
| l15 | summary.ideas[1,2], formula, trap | Branches, atoms, Jacobian, one branch halves the $Z^2$ density | correct | |
| l15 | q0 | Height 1/2 for $Y = 2X$; slips have areas 2 and 4 | correct | |
| l15 | q1 | $-\ln(0.1)/0.5 = 4.605$; slip 0.2107 is the 10th percentile | correct | script |
| l15 | q2 | $P(Z^2 \le 1) = 0.6827$; slips 0.3413 (one branch), 0.8413 ($\Phi(1)$) | correct | script |
| l15 | q3 | $E[R^2] = 2$; $-2\ln U_1$ has mean 2 | correct | |
| l16 | s0.key | Sum of two uniforms is triangular with peak at 1 | correct | convolution of two $U(0,1)$ densities (C&B Thm 5.2.9); script MC |
| l16 | s0.wrong | Flat, bell, ends: each rebuttal is right | correct | |
| l16 | s1.prose | "Flip $Y$'s density, slide it so it is centred on $t$" | wrong | $f_Y(t - x)$ covers $[t-1, t]$; its centre is $t - \tfrac12$. The canvas draws $[t-1,t]$. F6 |
| l16 | s1.key | Overlap 0.5 at $t = 1.5$ | correct | $[0.5, 1]$ |
| l16 | s1.wrong one, zero | 1 is the overlap at $t = 1$; 0 would mean 1.5 is unreachable | correct | |
| l16 | s2.key | $P(U_1 + U_2 \le 1.5) = 0.875$ | correct | script MC |
| l16 | s2.wrong unif, tail | 0.75 is the uniform-on-$[0,2]$ answer; 0.125 is the tail | correct | |
| l16 | s3.prose | Convolution formula for independent $X$, $Y$ | correct | C&B Thm 5.2.9 |
| l16 | s3.key, options | Integrand non-zero on $[0.5, 1]$; three wrong ranges explained | correct | supports |
| l16 | s3.explain | Limits $[0,t]$ for $t \le 1$, $[t-1,1]$ for $t \ge 1$ | correct | |
| l16 | s4.lines | Two Exp($\lambda$): $\lambda^2te^{-\lambda t}$ | correct | script sympy |
| l16 | s4.explain | Not exponential; starts at 0 | correct | Gamma(2) |
| l16 | s5.prose | $P(T > t) = e^{-2t}(1 + 2t)$ | correct | script sympy |
| l16 | s5.key | $3e^{-2} = 0.4060$ | correct | script, MC |
| l16 | s5.wrong single, mid | $e^{-2}$ is the first trade; $2e^{-2}$ drops the 1 | correct | |
| l16 | s5.explain | This is the Gamma with $a = 2$ | correct | |
| l16 | s6.prose | Discrete convolution sum | correct | independence is carried from s3; two dice |
| l16 | s6.code | `convolve_pmf` passes six tests; dice, coins, Binomial(3, 0.3) | correct | script |
| l16 | s6.explain | The binomial is a repeated convolution of Bernoulli trials | correct | |
| l16 | s7.key | Density of the sum at 0.5 is 0.5, not the product 1 | correct | script MC |
| l16 | s7.wrong prod | "only counts the case where both fills are at 0.5, and ignores every other way to add to 0.5" | wrong | (0.5, 0.5) adds to 1; it is not a way to add to 0.5. F7 |
| l16 | s7.wrong sum, quarter | Sum of densities is not the density of a sum; 0.25 is a region's probability | correct | |
| l16 | s7.explain | The product uses the same $t$ for both; it is twice too big | correct | |
| l16 | s8.prose | Sum of independent normals is normal; means and variances add | correct | C&B Thm 4.2.14 |
| l16 | s8.prose | The two strategies are not said to be independent | imprecise | key 0.1587 needs it. F12 |
| l16 | s8.key | $1 - \Phi(1) = 0.1587$ | correct | script |
| l16 | s8.wrong sd, half | 0.2375 uses sd 7; 0.5 is the chance of beating the mean | correct | script |
| l16 | s9.key | $0.8\,\Phi(0) + 0.2\,\Phi(1) = 0.5683$ | correct | script, MC |
| l16 | s9.wrong never, always | 0.5 ignores the drop; 0.8413 always applies it | correct | |
| l16 | s9.explain | Discrete plus continuous: $f_{X+D}(t) = \sum_d P(D = d)f_X(t - d)$ | correct | law of total probability; independence stated |
| l16 | s10.prose | Desks A and B are not said to be independent | imprecise | key needs it. F12 |
| l16 | s10.key | $\tfrac12(e^{-1} - e^{-3}) = 0.1590$ | correct | script exact, MC under independence |
| l16 | s10.wrong ignore, worst | $e^{-2}$ if A makes 0; $e^{-1}$ if A always loses £1k | correct | |
| l16 | s10.explain | Noise lifts the chance above $e^{-2}$ because $e^{-x}$ is convex | correct | Jensen |
| l16 | summary | Convolution, limits, triangle, $\lambda^2te^{-\lambda t}$, discrete sum, mixture | correct | |
| l16 | summary.trap | "Variances of normals add, not standard deviations" | correct | ideas[2] on the same card says "independent normals" |
| l16 | q0 | 0.125; slip 0.25 is uniform on $[0,2]$ | correct | |
| l16 | q1 | 4/36; slips 1/36 (one pair), 1/6 (total 7) | correct | |
| l16 | q2 | $\sqrt{13} = 3.606$; slips 5 (sds added), 13 (variance) | correct | |
| l16 | q3 | $2e^{-2} = 0.2707$; slips $e^{-4}$ (product), $e^{-2}$ (one density) | correct | script |
| l17 | s0.prose | Hazard 2% a year gives mean wait 50 years | correct | $1/\lambda$ |
| l17 | s0.key, options | Mean first default about 10 years; 25 is two issuers, 5 is ten issuers | correct | $50/n$; script MC |
| l17 | s1.key | $P(\min > t) = e^{-0.1t}$ | correct | independence |
| l17 | s1.wrong one, cdf, five | One issuer; the CDF; chances multiply, not add | correct | |
| l17 | s1.explain | Minimum of independent exponentials is exponential with the rates added | correct | Ross 5.2.3; script KS |
| l17 | s2.key | $1 - e^{-0.1} = 0.0952$ | correct | script |
| l17 | s2.wrong single, five | 0.0198 one issuer; 0.0990 is five times that (union bound) | correct | script |
| l17 | s3.key | $0.9^5 = 0.5905$; slips 0.9 and 0.4095 | correct | script |
| l17 | s4.prose | $P(\max \le t) = F(t)^n$, $P(\min > t) = (1 - F(t))^n$, $f_{\max} = nF^{n-1}f$ for $n$ independent draws with CDF $F$ | correct | C&B Thm 5.4.4; iid is stated |
| l17 | s4.key | $5 \times 0.9^4 = 3.2805$; slips 0.5905 (CDF), 4.5 (power 1) | correct | script |
| l17 | s5.lines | Counting argument: $f_{(k)}(x) = n\binom{n-1}{k-1}x^{k-1}(1-x)^{n-k}$ | correct | C&B Thm 5.4.4 |
| l17 | s5.explain | $k = n$ gives $nx^{n-1}$ | correct | |
| l17 | s6.key | $20 \times 0.3 \times 0.7^3 = 2.058$ | correct | script; KS against Beta(2,4) |
| l17 | s6.wrong half, nocount | 1.029 uses $\binom52$; 0.1029 has no count | correct | script |
| l17 | s6.explain | Mean $k/(n+1)$; draws cut $[0,1]$ into $n+1$ gaps of equal mean | correct | C&B Ex 5.4.5; exchangeable spacings |
| l17 | s7.prose | Skill-free $t$-ratios roughly $N(0,1)$, independent (caption) | correct | stated as an approximation |
| l17 | s7.key | Mean best of 20 is about 1.9 (1.8675) | correct | script quadrature and MC |
| l17 | s7.wrong three | One in 740; about one trial in 40 with twenty tries | correct | script: 741 and 1 in 37.6 |
| l17 | s7.wrong zero, one | Best of twenty almost never below 1 | correct | $\Phi(1)^{20} = 0.032$ |
| l17 | s7.explain | Integrand $z \cdot 20\varphi(z)\Phi(z)^{19}$ | correct | density of the maximum |
| l17 | s8.key | $1 - e^{-1} = 0.6321$ | correct | script |
| l17 | s8.wrong maxcdf | 0.0002 is $0.1813^5$, the maximum's CDF | correct | script |
| l17 | s8.wrong five | "0.9063 is $5 \times 0.1813$" | imprecise | $5 \times 0.1813 = 0.9065$; the slip value is $5 \times 0.18127$. F20 |
| l17 | s8.explain | $1 - (1 - F)^n$, not $F^n$, not $nF$ | correct | |
| l17 | s9.prose | Exact answer $1 - e^{-(\lambda_1 + \dots + \lambda_n)T}$ | correct | independent exponentials |
| l17 | s9.code | `first_default_mc` passes six tests; `expovariate` takes a rate | correct | script; Python docs for `random.expovariate(lambd)` |
| l17 | s9.explain | Error shrinks like $1/\sqrt{\text{trials}}$; 200,000 draws | correct | $40{,}000 \times 5$ |
| l17 | s10.prose | "For continuous variables a tie has probability 0" | imprecise | needs independent draws (or a joint density); $X$ and $Y = X$ tie always. F13 |
| l17 | s10.key | $P(\max = 3) = 5/36$; slip 1/36 is both dice 3 | correct | grid count |
| l17 | s10.wrong cdf | "0.25 is $P(\max \le 3)$. That includes totals of 1 and 2" | wrong | the quantity is the maximum, not a total. F8 |
| l17 | s10.explain | Discrete: subtract two CDF values | correct | |
| l17 | s11.key | $1 - \Phi(2.1)^{20} = 0.3027$ | correct | script, MC |
| l17 | s11.accept, feedback | "$1 - 0.9821^{20} = 0.3027$" | imprecise | the digits shown give 0.3032. F20 |
| l17 | s11.wrong single | 0.0179 is one strategy | correct | script |
| l17 | s11.wrong times | "0.3573 is $20 \times 0.0179$" | imprecise | $20 \times 0.0179 = 0.358$. F20 |
| l17 | s11.explain | Benchmark for a chosen-best strategy is the distribution of the maximum | correct | multiple-testing argument; Bailey and López de Prado (2014) use the same expected-maximum benchmark |
| l17 | summary.ideas[0] | $F(t)^n$ and $(1 - F(t))^n$ with no mention of independent draws | imprecise | hypothesis dropped on the summary card. F13 |
| l17 | summary.ideas[1,2], formula, trap | Rates add; order-statistic density; mean $k/(n+1)$; 1.87 | correct | |
| l17 | q0 | $e^{-3} = 0.0498$; slips $e^{-0.5}$, $e^{-6}$ | correct | script |
| l17 | q1 | $0.5^4 = 0.0625$; slips 0.5, 0.25 | correct | |
| l17 | q2 | $3/10$; slip $3/9$ | correct | |
| l17 | q3 | $\Phi(1.5)^{20} = 0.2509$; slips 0.9332, 0.7491; "three times in four" | correct | script |
| l18 | s0.prose | "Trades arrive at 2 a minute, so each gap is exponential" | imprecise | true for Poisson arrivals, not for a rate alone. F16 |
| l18 | s0.key | Bars peak near 1, below the mean 1.5 | correct | mode $(a-1)/\lambda$; script |
| l18 | s0.wrong | Zero, mean, three: rebuttals right | correct | |
| l18 | s0.explain | Density $4t^2e^{-2t}$, peak at $t = 1$ | correct | script sympy |
| l18 | s1.key | Var$(T) = 0.75$; slips 0.25, 2.25 | correct | script MC |
| l18 | s1.explain | Mean $a/\lambda$, variance $a/\lambda^2$; sd 0.87 | correct | C&B 3.3 |
| l18 | s2.prose | $T > 2$ exactly when fewer than 3 arrivals in 2 minutes | correct | Poisson and Gamma duality; C&B section 3.3 |
| l18 | s2.key | $13e^{-4} = 0.2381$; slips $e^{-4}$, 0.4335 (includes $N = 3$) | correct | script |
| l18 | s3.prose | Gamma density with shape $a$, rate $\lambda$; $\Gamma(n) = (n-1)!$; $\Gamma(\tfrac12) = \sqrt\pi$ | correct | C&B 3.3; script |
| l18 | s3.prose | Libraries often ask for the scale $1/\lambda$ | correct | `scipy.stats.gamma(a, scale=)`, `numpy.random.Generator.gamma(shape, scale)` |
| l18 | s3.key, options | Shape 3, scale 0.5; scale 2 gives mean 6 | correct | script |
| l18 | s3.explain | Density 0.5413 at $t = 1$; check the mean to detect rate against scale | correct | script |
| l18 | s4.prose | Sum of $n$ independent squared standard normals is chi-square, Gamma($n/2$, rate $\tfrac12$) | correct | C&B Lemma 5.3.2; script |
| l18 | s4.question | "Six independent standardised returns" are treated as standard normal | imprecise | variance 2 per term needs normality (kurtosis 3). F17 |
| l18 | s4.key | Var$(V) = 12$; slips 6 (mean), 2 (one term) | correct | script |
| l18 | s5.prose | $t = Z/\sqrt{V/n}$ has the $t$ distribution | imprecise | needs $Z$ independent of $V$ (C&B Def 5.3.4). script shows a dependent pair that fails. F11 |
| l18 | s5.key | Ratio $0.1019/0.0455 = 2.24$; slip 0.446 is the inverse | correct | script |
| l18 | s5.explain | Estimated sd fattens tails; gap closes as $n$ grows | correct | $t_n \to N(0,1)$ |
| l18 | s6.prose | Normal two-tail at 2.3 is 0.021; $t_5$ 5% two-sided cut-off 2.57 | correct | script |
| l18 | s6.key | Not significant: $t_5$ two-tail at 2.3 is 0.0698 | correct | script, MC with six normal returns |
| l18 | s6.wrong small | "The $t$ is exact for normal data at any size" | correct | C&B Thm 5.3.1; the condition "normal data" is stated |
| l18 | s6.explain | With 30 observations the gap is much smaller | correct | $t_{29}$ cut-off 2.045 against 1.96 |
| l18 | s7.prose | Beta density, mean $a/(a+b)$, Beta(1,1) uniform, $k$th of $n$ uniforms is Beta($k$, $n-k+1$) | correct | C&B Ex 5.4.5 |
| l18 | s7.key | Mean 1/3; slips 0.4 ($k/n$), 0.5 (Beta(2,2)) | correct | |
| l18 | s8.prose | Beta(0.5, 0.5) density $1/(\pi\sqrt{x(1-x)})$; mean 1/2 and least dense at 1/2 | correct | $B(\tfrac12,\tfrac12) = \pi$ |
| l18 | s8.key | $P(X \le 0.25) = 1/3$; CDF $\tfrac2\pi\arcsin\sqrt x$ | correct | script exact |
| l18 | s8.wrong unif, half | 0.25 uniform; 0.5 is below the mean | correct | |
| l18 | s8.explain | Arcsine law is the share of time "a fair random walk" spends positive | imprecise | it is the limit for a long walk (Feller vol. 1, III.4). F15 |
| l18 | s9.lines | Beta(2,2) prior, 14 of 20: posterior Beta(16, 8) | correct | script kernel; C&B section 7.2.3 |
| l18 | s9.explain | Conjugacy: wins add to $a$, losses to $b$ | correct | |
| l18 | s10.prose | Posterior mean 0.667 lies between 0.5 and 0.70 | correct | |
| l18 | s10.key | About 95% posterior chance that $p > 0.5$ (0.9534) | correct | script; a posterior statement, so the reading is valid |
| l18 | s10.wrong raw, mean, flip | Each rebuttal right | correct | |
| l18 | s10.explain | Posterior sd 0.094 | correct | script |
| l18 | summary.ideas[1] | "A sum of $n$ squared standard normals is chi-square"; $Z/\sqrt{V/n}$ | imprecise | independence dropped twice. F11 |
| l18 | summary other | Gamma mean and variance, rate against scale, Beta update, trap on normal critical values | correct | |
| l18 | q0 | Mean wait for the fifth order 1.25; slips 0.25, 20 | correct | Poisson process is stated here |
| l18 | q1 | $\sqrt{20} = 4.472$; slips 20, 10 | correct | |
| l18 | q2 | $t_5$ has more mass beyond $\pm 2$; a little lower at the centre | correct | script |
| l18 | q3 | Beta(4, 2), mean 2/3; slips 0.75, 0.5 | correct | |
| l19 | s0.key | $M'(0) = 3.5$; slips 21, 1 | correct | script sympy |
| l19 | s1.key | $M''(0) = 91/6$; slips 3.5, 12.25; variance 35/12 | correct | script |
| l19 | s2.lines | Series, expectation term by term, $M^{(k)}(0) = E[X^k]$ | correct | C&B Thm 2.3.7; needs the MGF finite near 0, stated on the next screen and in the summary |
| l19 | s3.prose | For independent $X$, $Y$: $M_{X+Y} = M_XM_Y$ | correct | C&B Thm 4.2.12; stated as sufficient |
| l19 | s3.prose | An MGF finite near 0 pins down the distribution | correct | C&B Thm 2.3.11 |
| l19 | s3.key | $(0.7 + 0.3e^t)^3$ | correct | script |
| l19 | s3.wrong sum, scaled | Sum is 3 at $t = 0$; $0.7 + 0.3e^{3t}$ is one trade paying 3 | correct | |
| l19 | s4.prose | Poisson MGF $e^{\lambda(e^t - 1)}$ | correct | derivation: $\sum_k e^{tk}e^{-\lambda}\lambda^k/k! = e^{\lambda(e^t-1)}$; script uses it for $M''(0)$ |
| l19 | s4.key | Poisson(3.5) at 3 is 0.2158 | correct | script, MC |
| l19 | s4.wrong add, none | 0.306 is $0.1804 + 0.1255$; 0.0302 is $e^{-3.5}$ | correct | script |
| l19 | s5.prose | Normal MGF; $E[S_1] = 100M_X(1)$ | correct | C&B section 2.3 |
| l19 | s5.key | £105.13; slips £103.05, £107.25 | correct | script, MC |
| l19 | s5.explain | The lognormal has no MGF for $t > 0$ | correct | C&B section 2.3; $e^{te^x}$ outgrows the normal tail for any $t > 0$ |
| l19 | s6.key, options | Product $(0.5 + 0.5e^t)^2$; sum is 2 at 0; $0.5 + 0.5e^{2t}$ is $2X$ | correct | |
| l19 | s6.explain | "The product rule needs independence. For dependent variables $E[e^{tX}e^{tY}]$ does not split." | wrong | independence is sufficient, not necessary. script builds a dependent pair on $\{1,2,3\}^2$ with $M_{X+Y} = M_XM_Y$ for every $t$. F3 |
| l19 | s7.prose | Coin MGF $\cosh t$, normal $e^{t^2/2}$; Cauchy has none; lognormal none for $t > 0$ | correct | C&B 2.3 |
| l19 | s7.key | Agree to $t^2$, split at $t^4$: $E[X^4]$ is 1 and 3 | correct | script series |
| l19 | s7.wrong exist | A bounded variable has an MGF everywhere | correct | |
| l19 | s7.explain | Matching two moments does not match a distribution; the whole MGF does | correct | both MGFs are finite everywhere |
| l19 | s8.prose | "$X_i$ independent with mean $\mu$ and sd $\sigma$" | imprecise | the first line uses identical distribution too. F18 |
| l19 | s8.lines | $[M_Y(t/\sqrt n)]^n$, Taylor, substitute, limit, identify with the stated provisos | correct | C&B Thm 5.5.14; Curtiss (1942) for MGF convergence |
| l19 | s8.explain | Proper theorem needs only finite variance and uses characteristic functions | correct | C&B Thm 5.5.15 (iid) |
| l19 | s9.prose | Chernoff: $P(S \ge a) \le e^{-ta}M(t)^n$ for every $t > 0$ | correct | Markov on $e^{tS}$ |
| l19 | s9.code | Both functions pass nine tests; grid includes $t = 0$ so the bound is at most 1 | correct | script; bound holds on a grid of $(n, a)$ |
| l19 | s9.explain | Best $t$ about 0.31; bound 0.0104 is six times the exact 0.00176 | correct | $\operatorname{artanh}(0.3) = 0.3095$; script |
| l19 | s10.table | Chebyshev 0.1111, $e^{-a^2/2n} = 0.0111$, best $t$ 0.0104, normal 0.00135, exact 0.00176 | correct | script |
| l19 | s10.key | Only the Chernoff bound and the exact sum prove the limit | correct | a bound or exact figure below 0.015 |
| l19 | s10.wrong clt, cheb | An estimate below the truth proves nothing; Chebyshev too loose | correct | |
| l19 | s10.explain | Chebyshev 63 times the truth | correct | script |
| l19 | summary.ideas[0,1] | Moments, uniqueness when finite near 0, product for independent variables | correct | sufficient direction only |
| l19 | summary.ideas[2], formula | "$\min_t e^{-ta}M(t)^n$" with no $t > 0$ | imprecise | over all $t$ it is not a bound: script gives 0.0104 against a true 0.998 at $a = -30$. F14 |
| l19 | summary.formula.note | Exponential MGF $\lambda/(\lambda - t)$ for $t < \lambda$ | correct | |
| l19 | summary.trap | $M_{X+Y}$ is a product when $X$, $Y$ are independent; Cauchy has no MGF | correct | sufficient direction |
| l19 | q0 | Mean 3; slips 0.6, 5 | correct | |
| l19 | q1 | Variance 13; slips 5, 25 | correct | |
| l19 | q2 | Cauchy has no MGF near 0; geometric finite below $-\ln(1-p)$ | correct | script |
| l19 | q2.explain | Cauchy has no mean; tails like $1/x^2$ | correct | |
| l19 | q3 | $E[N^2] = 6$; slips 2, 4 | correct | script |
| review-4 | i0 r-marginal | $3x$ on the triangle is a density; $P(X \le 0.5) = 0.125$; slip 0.375 integrates $y$ to 1 | correct | script exact |
| review-4 | i1 r-transform | $f_Y(0.16) = 1.25$; slips 1, 0.8 | correct | script; one branch only since $X \ge 0$ |
| review-4 | i2 r-sum-uniform | 0.32; slips 0.4, 0.64 | correct | script MC |
| review-4 | i3 r-max-exp | $(1 - e^{-1.5})^5 = 0.2830$; slips 0.7769, 0.717 | correct | script |
| review-4 | i4 r-best10 key | $1 - \Phi(2)^{10} = 0.2056$; slips 0.0228, 0.2275 | correct | script, MC |
| review-4 | i4 r-best10 explain | "One in five fund pitches this good is luck" | wrong | 0.2056 is P(best $\ge 2$ given no skill), not P(luck given a pitch this good); in the item's model that share is 1. F4 |
| review-4 | i5 r-gamma-tail | $4e^{-3} = 0.1991$; slips $e^{-3}$, $3e^{-3}$; Poisson(3) check | correct | script |
| review-4 | i6 r-beta-post | Beta(8, 4); options Beta(7,3), Beta(4,8), Beta(11,4) | correct | conjugacy |
| review-4 | i7 r-mgf-mean | $M'(0) = 0.5$; slips 2 (rate), 1 ($M(0)$) | correct | script |
| review-4 | i8 r-poisson-sum | Poisson(5); exponents add; an MGF identifies the distribution | correct | finite for all $t$ |
| homework-4 | i0 h-marginal | $8xy$ is a density on the triangle; $P(X \le 0.5) = 1/16$; slip 0.25 from $2x$ | correct | script |
| homework-4 | i1 h-condexp | $E[Y \mid X = x] = 2x/3$; slips $x/2$, $x$ | correct | script |
| homework-4 | i2 h-chi-derive | CDF method for $Z^2$ | correct | C&B section 2.1 |
| homework-4 | i3 h-jacobian | $\lvert J \rvert = u$; $f_{U,V} = ue^{-u}$; key 0.2707; slips $e^{-2}$, $4e^{-2}$ | correct | script; C&B section 4.3 |
| homework-4 | i3 explain | $U$ is Gamma(2, 1), $V$ uniform, independent | correct | script MC |
| homework-4 | i4 h-convolve | $e^{-1} - e^{-2} = 0.2325$; slips $e^{-2}$, 0 | correct | script MC |
| homework-4 | i5 h-first-default prose | Who is first is independent of when the first default comes | correct | Ross 5.2.3; script MC |
| homework-4 | i5 key | $0.5 \times 0.2592 = 0.1296$; slips 0.2592, 0.5 | correct | script |
| homework-4 | i6 h-order-code | Solution passes seven tests; index $k - 1$ | correct | script |
| homework-4 | i6 explain | "within about 0.001 ... since the sd of the mean is $0.18/\sqrt{20000}$" | imprecise | 0.18 is the sd for $n = 5$, $k = 2$ only; other tested cases range 0.08 to 0.29. F19 |
| homework-4 | i7 h-beta-two-batches | Beta(14, 10), mean 0.5833; slips 0.6875, 0.5; order of batches does not matter | correct | |
| homework-4 | i8 h-binomial-mgf | $(1 - p + pe^t)^n$; slips as in l19 s3 | correct | |
| homework-4 | i9 h-poisson-third | $E[N^3] = 22$; $M''$, $M'''$ as written; slips 8, 6 | correct | script sympy, MC |
| homework-4 | i10 model part 1 | 0.0047, 0.208, median best 2.20, mean about 2.25 | correct | script |
| homework-4 | i10 model part 2 | $\Phi(c)^{50} = 0.99$ gives 3.54; dividing the level by 50 gives the same to two places | correct | script: Šidák 3.539, Bonferroni 3.540 |
| homework-4 | i10 model part 3 | $t_{29}$: 0.0073, 0.31, median 2.32, cut-off about 4.0 | correct | script; 30 normal returns give 29 degrees of freedom |
| homework-4 | i10 model part 4 | Not significant; assumptions independence and normality; positive correlation lowers the effective number of tries | correct | one-sided reading used throughout; two-sided gives the same verdict |
| homework-4 | i10 rubric | Six rubric lines match the model | correct | |
| problems-4 | i0 prose | $e^{-y}$ on $0 < x < y$ is a density | correct | script |
| problems-4 | i0 p0 | $f_X = e^{-x}$; slips $e^{-y}$, $1 - e^{-x}$ (limits 0 to $x$), 1 | correct | script |
| problems-4 | i0 p1 | $E[Y \mid X = 0.5] = 1.5$; slips 2 ($E[Y]$), 0.25, 1 | correct | script MC |
| problems-4 | i0 p2 | Dependent: the slice moves with $x$; wedge support | correct | |
| problems-4 | i0 p3 | $f_{X,G} = e^{-x}e^{-g}$; $P(G > 2) = e^{-2}$; slips $3e^{-2}$, $1 - e^{-2}$, $e^{-1}$ | correct | script |
| problems-4 | i0 p4 | $P(Y > 3) = 4e^{-3}$; slips $e^{-3}$, 0.8009, $3e^{-3}$ | correct | script |
| problems-4 | i1 p0 | Different rates: $f_T = e^{-t/2} - e^{-t}$, not a Gamma; slips product, sum, equal-rate Gamma | correct | script sympy; hypoexponential |
| problems-4 | i1 p1 | $2e^{-5} - e^{-10} = 0.0134$; slips $e^{-5}$, 0.9866, $6e^{-5}$; one in 74 | correct | script, MC |
| problems-4 | i1 p2 | $M_T(s) = 1/((1-s)(1-2s))$ for $s < 0.5$; slips sum, $1/(1 - 0.5s)$, single | correct | script |
| problems-4 | i1 p3 | Minimiser $s = 0.3807$ from $20s^2 - 26s + 7 = 0$; slips 0.9193, 0.4, 0.9 | correct | script numeric minimiser |
| problems-4 | i1 p4 | Bound 0.1503; slips 0.1526, 0.0222, 0.0134; about 11 times the exact value | correct | script |
| problems-4 | i2 p0 | $0.8^4 = 0.4096$; slips 0.8, 0.9984 (worst), 0.5904 | correct | script |
| problems-4 | i2 p1 | $E[\text{best}] = 0.8$; slips 0.5, 0.2, 0.75 | correct | script MC |
| problems-4 | i2 p2 | $4t^3$ is Beta(4, 1); $B(4,1) = 1/4$ | correct | |
| problems-4 | i2 p3 | Beta(3, 2) mean 0.6; slips 0.75, 0.4, 0.5 | correct | script MC |
| problems-4 | i2 p4 key | $P(X_{(3)} > 0.5) = 11/16$; slips 5/16, 15/16, 0.5 | correct | script, Beta(3,2) tail |
| problems-4 | i2 p4 explain | "$X_{(3)} > 0.5$ exactly when at most 1 of the 4 quotes is below 0.5" | wrong | the event is at most 2 below (at least 2 above). The numbers agree only by symmetry at 0.5; script separates the rules at 0.6. F9 |
| problems-4 | i3 p0 | $M_D(s) = (1 - 2s)^{-2}$; slips added, one | correct | script quadrature |
| problems-4 | i3 p0 wrong power | "$(1-2s)^{-1/8}$: you multiplied the exponent by $\tfrac12$ again" | wrong | $-\tfrac12 \times \tfrac12 = -\tfrac14$; $-\tfrac18$ is $-\tfrac12 \div 4$. F10 |
| problems-4 | i3 p1 | Var$(D) = 8$; $M' = 4(1-2s)^{-3}$, $M'' = 24(1-2s)^{-4}$; slips 24, 2, 2.83 | correct | script |
| problems-4 | i3 p2 | Gamma shape 2, rate 1/2 (chi-square 4); wrong options' MGFs | correct | Gamma MGF $(\lambda/(\lambda - s))^a$ |
| problems-4 | i3 p3 | $P(D > 8) = 5e^{-4} = 0.0916$; slips $e^{-4}$, $13e^{-4}$, $9e^{-8}$ | correct | script, MC |
| problems-4 | i3 p4 | Smallest whole $d$ is 10; tails 0.0611 and 0.0404; normal fit gives 9 | correct | script; chi-square(4) 95% point 9.488 |

Verdict counts are in the audit file.
