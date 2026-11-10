# Concept audit: ito, level 4 (stochastic calculus at interview)

Blind concept audit (brief: `docs/briefs/concept-audit.md`) of `app/content/courses/ito/` level 4: l13-martingale-or-not, l14-hitting-and-exit, l15-moments-quickly, l16-pricing-in-a-minute, l17-derivation-aloud, review-4 and homework-4. Stage 3, so the full ledger. Every screen, quiz item, hint, explain, why, feedback, slip, rubric line and model answer was read in full. Every code widget's solution was run in CPython 3.13 (NumPy 2.5.3, SciPy 1.18.1) against its hidden tests: 7 widgets, 52 hidden tests, 52 pass, and every starter fails all of its tests. Every printed or stated output of those widgets was recomputed.

Claim ledger: `docs/reports/audit-ito-4-ledger.md` (1,209 rows: correct 1,190, wrong 2, imprecise 16, misleading 1, unverified 0). Experiments: `docs/reports/ito-L4-concepts.py` (134 checks: 128 pass, 6 `EXPECTED_FAIL`, exit 0). The script uses exact symbolic checks where it can (drifts, the exit ODEs, two-time moments, the Black-Scholes equation) and Monte Carlo for the empirical claims (the discretisation gaps of the exit simulations, the time-integral and Itô-integral variances, a stopped exponential martingale).

Findings are `N. file | JSON path | severity | problem | evidence and basis | exact fix`. Severities: `wrong` (false as stated), `imprecise` (true only under an unstated hypothesis or convention), `misleading` (true, but teaches a wrong habit). Each is tagged `serious` (a learner would carry away a wrong definition, theorem, method, convention or graded answer) or `minor`.

**Result: 16 findings: 1 `wrong`, 14 `imprecise`, 1 `misleading`. 3 are serious, 13 minor.** No graded key, slip value, formula in a summary, code solution or model answer is wrong. The one `wrong` is a symmetry rule stated backwards in l15. The two other serious findings are one sentence, used in two files, that states optional stopping with a condition that is not sufficient in general. Every fix below was applied to an in-memory copy: each old string occurs exactly once in its field, each new sentence is under 35 words, and no fix changes a graded key.

What the level gets right, checked and worth keeping: the local-versus-true martingale caveat is stated ("tame" $f_x$, with the integrability condition, in the l13 derive line and summary); the two-barrier derivation in the homework passes to the limit with bounded and monotone convergence; the single-barrier trap is correct ($\tau$ finite almost surely, $E[\tau] = \infty$); the drifted exit formula, its $\mu \to 0$ limit and its slope are exact; $\Phi(d_2)$ is called a $Q$-chance and delta is kept apart from it; the spoken model answer for an unknown adapted drift states integrability of $\mu_t$ and the $\int(\mu_t - r)^2\,dt$ caveat.

## l13-martingale-or-not

1. l13-martingale-or-not.json | screens[0].explain.text | imprecise, minor | "a process with zero drift is a martingale" is stated flat on the first screen. Zero drift gives a local martingale; the lesson's own derive line and summary add the condition ("if $f_x$ is tame"). | Shreve Thm 4.3.1(iv) needs $E\int_0^t f_x^2\,ds < \infty$; KS section 3.2. The summary of this lesson says "without it, zero drift is not enough", so the first screen contradicts the summary as worded. | Replace `The drift $(3 - c)x$ vanishes at $c = 3$, and a process with zero drift is a martingale.` with `The drift $(3 - c)x$ vanishes at $c = 3$. With zero drift and a tame noise term, as here, the process is a martingale.`

## l14-hitting-and-exit

2. l14-hitting-and-exit.json | screens[1].feedback.byKey.x1 | imprecise, serious | "Optional stopping needs a bounded stopped value or a finite mean time." A finite mean time is sufficient for $W$ and for $W^2 - t$ (Wald's identities), not for a martingale in general. The very next screens stop the exponential martingale $e^{-2\mu X_t}$, where a learner would reuse the rule. | KS Thm 1.3.22 (bounded times or a uniformly integrable stopped process), KS Prob. 2.7.19 (Wald for Brownian motion). The Markov course states the discrete rule correctly: "finite mean with bounded steps". Counter-example: $M_t = e^{2W_t - 2t}$, $\tau$ = first time $W_t = t - 1$. Then $E[\tau] = 1$ and $M_\tau = e^{-2}$ on every path, so $E[M_\tau] = e^{-2} \ne 1$. Simulated: mean time 1.03, $E[M_\tau] = 0.135$; `l14.s1.x1` is `EXPECTED_FAIL`. | Replace `Optional stopping needs a bounded stopped value or a finite mean time.` with `Optional stopping needs a bounded stopped process. For $W$ and $W^2 - t$ a finite mean time is also enough.`

3. l14-hitting-and-exit.json | screens[3].explain.text | imprecise, minor | "Their wait has no finite mean, so $E[W_\tau]$ is not 0." The "so" is not valid: an infinite mean wait removes the guarantee, it does not force a nonzero mean. | $\tau$ = first zero of $W$ after time 1 has $E[\tau] = \infty$ and $W_\tau = 0$. Here $E[W_\tau] = 1$ because $W_\tau = 1$ on every path. | Replace `Their wait has no finite mean, so $E[W_\tau]$ is not 0.` with `Their wait has no finite mean, so the rule gives no guarantee, and here $E[W_\tau] = 1$.`

4. l14-hitting-and-exit.json | quiz[2].question | imprecise, minor | "A price has drift $-0.5$ and volatility 2. What is the chance it ever reaches $+1$" gives no start point. The key $e^{-0.25}$ needs a start at 0. The matching review item says "starting at 0". | $P(\sup_t X_t \ge a) = e^{-2|\mu|a/\sigma^2}$ with $a$ the distance from the start (KS 3.5.C). | Replace `A price has drift $-0.5$ and volatility 2.` with `A price starts at 0 with drift $-0.5$ and volatility 2.`

## l15-moments-quickly

5. l15-moments-quickly.json | screens[5].prose and screens[5].explain.text | wrong, serious | The prose says "A product across two times can still be odd in total and nonzero." The example $W_1W_2^3$ has total power 4, which is even, as the screen's own feedback says. A two-time product with odd total power always has mean 0. The explain then says "Zero by symmetry applies only to a single odd power", which is too narrow: $E[W_1W_2^2] = 0$ by the same symmetry. A learner keeps a false rule and would expand a moment that is zero at sight, or expect it to be nonzero. | $(W_s, W_t)$ and $(-W_s, -W_t)$ have the same law, so $E[W_s^pW_t^q] = (-1)^{p+q}E[W_s^pW_t^q]$, which is 0 when $p + q$ is odd (Isserlis). Exact computation of all 15 moments with $p + q$ odd, $p, q \le 5$: all zero. `l15.s5 prose` is `EXPECTED_FAIL`. | In `screens[5].prose` replace `A product across two times can still be odd in total and nonzero.` with `A product across two times can be nonzero when each power is odd, provided the total power is even.` In `screens[5].explain.text` replace `Zero by symmetry applies only to a single odd power, such as $E[W_2^3] = 0$.` with `Zero by symmetry needs an odd total power, as in $E[W_2^3]$ or $E[W_1W_2^2]$.`

6. l15-moments-quickly.json | summary.ideas[2] | imprecise, minor | The summary gives the isometry as $\int f^2\,dt$ only. Quiz item q-ito then asks for $\text{Var}\int_0^2 W_t\,dW_t$, which needs $E[f^2]$ inside. The random form appears only in that item's explain. | Shreve Thm 4.3.1(vi): $E[(\int H\,dW)^2] = E\int H^2\,dt$. Simulated $\text{Var}\int_0^2 W\,dW = 2.0$. | Replace `follow the isometry $\int f^2\,dt$. A $dt$` with `follow the isometry $\int f^2\,dt$, with $E[f^2]$ inside when $f$ is random. A $dt$`

## l16-pricing-in-a-minute

7. l16-pricing-in-a-minute.json | screens[1].prose | imprecise, minor | The forward value $S_0 - Ke^{-rT}$ and $E_Q[S_T] = S_0e^{rT}$ hold for a share that pays no dividends. No lesson in the course says so; only two homework prompts do. An interviewer will ask. | Hull 5.5 to 5.7: with a yield $q$ the value is $S_0e^{-qT} - Ke^{-rT}$. | Replace `Next, a forward struck at 100: it pays $S_T - 100$ at $T$.` with `Next, a forward struck at 100 on our share, which pays no dividends. It pays $S_T - 100$ at $T$.`

8. l16-pricing-in-a-minute.json | screens[8].feedback.correct | imprecise, minor | "within 1.5 standard errors": the gap is $(10{,}948.77 - 10{,}941.74)/4.56 = 1.54$ standard errors. | Solution run on seed 16; `l16.s8 feedback` is `EXPECTED_FAIL` ($z = 1.541$). | Replace `, within 1.5 standard errors.` with `, about 1.5 standard errors away.`

9. l16-pricing-in-a-minute.json | screens[9].feedback.correct | imprecise, minor | "the junior forgot to discount the put." The junior's 0.4677 is $1 - 0.5323$. A put that was merely undiscounted would be $\Phi(-d_2) = 0.4404$. The slip is taking the complement to 1, which the screen itself teaches. | $e^{-rT}\Phi(-d_2) = 0.4189$, $\Phi(-d_2) = 0.4404$, $1 - 0.5323 = 0.4677$. `l16.s9 feedback` is `EXPECTED_FAIL`. | Replace `the junior forgot to discount the put.` with `the junior took the put as 1 less the call, not $e^{-rT}$ less the call.`

10. l16-pricing-in-a-minute.json | quiz[2].explain.text | imprecise, minor | "Every nonlinear payoff does" (depend on $\sigma$). True for the price as a function of the share price, but not at one given share price. | With $F = S_0e^{rT}$ the payoff $\sqrt{S_T/F}\,\ln(S_T/F)$ has price 0 at $S_0$ for every $\sigma$ (the integrand is odd after completing the square). Quadrature at $\sigma$ = 0.1, 0.2, 0.4, 0.8: all below $10^{-8}$. `l16.quiz2 explain` is `EXPECTED_FAIL`. | Replace `Every nonlinear payoff does.` with `The digital, the square and the call all carry $\sigma$.`

## l17-derivation-aloud

11. l17-derivation-aloud.json | screens[0].feedback.byKey.l7 | misleading, minor | The candidate's line 6 drops the gamma term, and line 7 checks the result with a forward. The feedback calls the forward "the right quick test". A forward has $V_{SS} = 0$, so it satisfies the flawed equation as well. The check cannot catch the lesson's headline error, and the learner is not told. | $V = S - Ke^{-r(T-t)}$ gives $V_t + rSV_S - rV = 0$ with or without the gamma term; the call leaves a residual of $-3.75$ in the flawed equation. Both in `l17.s0` checks. | Replace `A forward is the right quick test.` with `A forward is a fair quick test of the interest terms. It cannot catch a dropped gamma term, because its $V_{SS}$ is zero.`

## review-4

12. review-4.json | items[6].explain.text | imprecise, minor | "A strike above today's price makes finishing above it less likely than a coin flip". The comparison that decides it is the strike against the $Q$-median $S_0e^{(r - \sigma^2/2)T}$, not against $S_0$. Here the strike 64 is even below the forward, 65.00. | $Q(S_T > K) = \Phi(d_2) > \tfrac12$ exactly when $K < S_0e^{(r - \sigma^2/2)T}$. In the course market ($S_0 = 100$, $r = 5\%$, $\sigma = 20\%$) a strike of 102 gives 0.52. `review.r-dig110 explain` is `EXPECTED_FAIL`. | Replace `A strike above today's price makes finishing above it less likely than a coin flip, here 0.4303.` with `The strike 64 is above the $Q$-median $S_0e^{(r - \sigma^2/2)T} = 59.40$, so finishing above it is less likely than a coin flip, here 0.4303.`

13. review-4.json | items[8].widget.options[0].text, items[8].feedback.correct, items[8].explain.text | imprecise, minor | The marked answer to "what does the option's price depend on?" lists $r$, $\sigma$, the strike and the time, and the explain says "$r$ and $\sigma$ only". Today's share price is missing. The point of the item (not $\mu$) is right. | Hull 15.8: $c = c(S_0, K, T, r, \sigma)$. | In `options[0].text` replace `$r$, $\sigma$, the strike and the time, but not $\mu$` with `today's share price, $r$, $\sigma$, the strike and the time, but not $\mu$`. In `feedback.correct` replace `The price depends on $r$, $\sigma$, $K$ and $T$.` with `The price depends on $S$, $r$, $\sigma$, $K$ and $T$.` In `explain.text` replace `so price depends on $r$ and $\sigma$ only.` with `so $\mu$ never enters the price.`

## homework-4

14. homework-4.json | items[0].feedback.byKey.x1 | imprecise, serious | The same sentence as finding 2: "Optional stopping needs a bounded stopped value or a finite mean time." The item is titled "Optional stopping with its conditions", so the condition should be the right one. | As finding 2. | Replace `Optional stopping needs a bounded stopped value or a finite mean time.` with `Optional stopping needs a bounded stopped process. For $W$ and $W^2 - t$ a finite mean time is also enough.`

15. homework-4.json | items[0].widget.lines[4].why | imprecise, minor | "It fails for a stopping time with infinite mean". It can fail; it need not. The lesson says "can break the rule". | $\tau$ = first zero of $W$ after time 1: $E[\tau] = \infty$, $E[W_\tau] = 0$. | Replace `It fails for a stopping time with infinite mean, such as the hit of a single barrier.` with `It can fail when the stopped process is unbounded, as for the hit of a single barrier.`

16. homework-4.json | items[0].explain.text | imprecise, minor | "A single barrier fails both, which is why $E[\tau] = \infty$ there." One of the two conditions is "$E[\tau]$ finite", so the sentence explains an infinite mean by the mean being infinite. | The direction that holds: $E[W_\tau] = 1 \ne 0$, so by Wald $E[\tau]$ cannot be finite (Shreve Rem. 3.6.4). | Replace `A single barrier fails both, which is why $E[\tau] = \infty$ there.` with `A single barrier meets neither: the stopped path is unbounded below, and $E[\tau]$ is infinite.`

## Checked and left alone

- l14 screens[3], correct option "$E[\tau] = \infty$, so the rule's conditions fail": right for Brownian motion, where both sufficient conditions the lesson names fail. Finding 2 keeps it consistent.
- l14 screens[8] and homework h-exit-report: "long-run gap about 0.03" (simulated 0.031, se 0.004, 40,000 paths) and "chance gap about +0.012" (simulated 0.012, se 0.001, 150,000 paths) both hold, and the $0.5826\,\sigma\sqrt{\Delta t}$ barrier shift predicts both.
- l14 screens[9]: the Sharpe ratio "near 0.8 a year" uses 252 trading days, the usual convention; it is not stated on the screen.
- l17 screens[5] and the homework model answers: "$\sigma(t, S)$ changes nothing" means the hedge argument and the equation, with $\sigma(t, S)$ inside. The explain says so.
- homework h-aloud model: holding cash $C = V - \Delta S$ at all times presumes the result it derives, as the standard argument does. The zero-cost, self-financing reading in the model is sound.
- Lessons are cited by number in learner text (l13 screens[7], l14 screens[1] and screens[4], l16 screens[5], homework h-derivation). That is a voice matter, not a concept finding.

## Overlap with the earlier review

Filled after the ledger and findings were committed.

## Runs

Filled after the checks were run.
