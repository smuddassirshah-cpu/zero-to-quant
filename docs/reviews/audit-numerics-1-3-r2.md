# Concept audit, round 2: numerics, levels 1 to 3

Second blind concept audit (brief: `docs/briefs/concept-audit.md`) of `app/content/courses/numerics/` levels 1 to 3: l1 to l12, review-1 to review-3, homework-1 to homework-3. Level 4 is out of scope. Claim ledger: `docs/reports/audit-numerics-1-3-r2-ledger.md` (244 rows: correct 229, imprecise 10, wrong 3, misleading 2, unverified 0). Experiments: `docs/reports/numerics-L1-concepts-r2.py`, `numerics-L2-concepts-r2.py`, `numerics-L3-concepts-r2.py` (175 checks pass, 12 are `EXPECTED_FAIL`). Every code task's solution was run against its hidden tests (17 tasks, all pass) and every starter was checked to fail.

The ledger and the findings below were written and committed before any earlier review, audit, ledger, round-1 script or author report for this course was opened.

Findings are `N. file | JSON path | severity | problem | evidence and basis | exact fix`. Severities: `wrong`, `imprecise`, `misleading`. Each is tagged `serious` (a learner would carry away a wrong definition, theorem, method, convention or graded answer, or code that teaches a wrong method) or `minor`. There are 13 findings: 2 `wrong` (1 serious, 1 minor), 9 `imprecise` (all minor), 2 `misleading` (both minor). No graded key is wrong. One key (finding 8) is right only under a count the lesson's own code contradicts. No `wrong[]` value or wrong option is correct under a valid alternative method, apart from that one.

## Level 1

1. l1-floating-point.json | quiz[0].explain.text (second and third sentences) | imprecise, minor | "20,000.01 is stored as 20,000.009765625, wrong in the third decimal. A level quoted to hundredths needs float64." The stored error is 0.00023, in the fourth decimal. Every hundredth near 20,000 survives a float32 round trip, because the gap 0.00195 is under half a hundredth. So the stated reason for float64 is false. The real damage is to differences. | `numerics-L1-concepts-r2.py` `l1:quiz0_float32_cannot_hold_a_level_to_hundredths` is `EXPECTED_FAIL`: all 100 hundredths from 20,000.00 round back correctly. `fix1:float32_one_hundredth_move_is_2.3_per_cent_off` confirms the replacement numbers. Goldberg (1991) sec. 1.2 (relative error and ulps). | quiz[0].explain.text: "Between $2^{14}$ and $2^{15}$ float32's gap is $2^{14-23} = 0.001953125$. So 20,000.01 is stored as 20,000.009765625, off by 0.00023. The level still rounds to its hundredth, but a one-hundredth move comes out as 0.009765625, wrong by 2.3%: returns need float64."
2. l3-conditioning.json | screens[4].explain.text (third sentence); quiz[0].prose (second sentence) | imprecise, minor | "The correlation matrix, whose $\kappa$ is $\tfrac{1 + r}{1 - r}$." The eigenvalues are $1 + r$ and $1 - r$, so the ratio as written is below 1 when $r$ is negative. A condition number is never below 1. The quiz's own slip feedback says "the largest eigenvalue goes on top", which the formula does only for $r \ge 0$. | Trefethen and Bau lecture 12 ($\kappa = \sigma_{\max}/\sigma_{\min} \ge 1$). `l3:corr_kappa_formula_for_negative_r` is `EXPECTED_FAIL`: at $r = -0.95$ NumPy gives 39, the formula 0.0256. The checks at $r = 0.95$, 0.99 and 0.3 pass. | screens[4].explain.text, third sentence: "The same count holds when you solve with `regression`'s correlation matrix, whose $\kappa$ is $\tfrac{1 + |r|}{1 - |r|}$." quiz[0].prose, second sentence: "The `regression` course gave the condition number of $\begin{bmatrix}1 & r\\ r & 1\end{bmatrix}$ as $\tfrac{1 + r}{1 - r}$ for $r \ge 0$."
3. l3-conditioning.json | quiz[3].explain.text (third sentence); screens[9].explain.text (second sentence) | wrong, minor | "The same £0.05 on the 60 put would move it 8.5 points." The put is worth £0.0113. An error of $+£0.05$ moves its implied vol by 4.1 points, and $-£0.05$ makes the price negative, so no vol exists. The rule $\Delta\sigma \approx \Delta V/\text{vega}$ is first order and is used here with an error over four times the price. On screens[9] the same rule is stretched less far: £0.01 is 89% of the price, and the true moves are $+1.3$ and $-3.3$ points against the 1.70 the screen states as fact. The graded key 1.7 is the rule the prose gives, so it stands. | `l3:quiz3_0.05_on_the_60_put_moves_vol_8.5_points` is `EXPECTED_FAIL` (brentq on the Black-Scholes put: $+4.1$ points; $0.0113 - 0.05 < 0$). `l3:put60_price_vega_first_order` prints the true moves for £0.01. Hull ch. 19 (vega is a local sensitivity). | quiz[3].explain.text: "$0.05 / 37.52 = 0.00133$, or 0.133 vol points. At the money the vol is well conditioned in absolute terms. On the 60 put, worth £0.0113, an error of £0.05 swamps the price: the vol moves by whole points." screens[9].explain.text: "$0.01 / 0.588 = 0.017$, which is 1.70 vol points against 0.027 at the money. That is a first-order estimate: £0.01 is most of this price, and the true moves are 1.3 points up and 3.3 down. Either way a wing quote is ill-conditioned in absolute terms."
4. l4-stability.json | quiz[1].widget.options[1].why | imprecise, minor | "That is forward accuracy. An ill-conditioned problem rules it out for any algorithm." False for "any algorithm". Subtracting two close doubles is as ill-conditioned as a problem gets, and l2 quiz[1] has just taught that the machine returns it exactly. What ill-conditioning limits is the promise of a backward stable method, and of any method fed inexact data. | Sterbenz's lemma (Higham ASNA Thm 2.5); Trefethen and Bau Thm 15.1 (forward error of a backward stable algorithm is $O(\kappa u)$). `l4:quiz1_ill_conditioning_rules_out_forward_accuracy_for_any_algorithm` is `EXPECTED_FAIL`: $x - y$ with $\kappa = 2.2 \times 10^{12}$ is exact. | quiz[1].widget.options[1].why: "That is forward accuracy. On an ill-conditioned problem even a backward stable algorithm cannot promise it: its error can reach $\kappa u$."
5. l2-cancellation.json | screens[9].hints[1].text | imprecise, minor | "Rounding error in the numerator grows like $\epsilon V / h^2$." The numerator $V(S + h) - 2V(S) + V(S - h)$ carries a rounding error of about $4\epsilon V$ whatever $h$ is. The estimate, numerator over $h^2$, is what grows like $\epsilon V/h^2$. homework-1 items[6] states it correctly. | Burden and Faires 4.1 (rounding in difference formulas); `l2:gamma_bumps`. | screens[9].hints[1].text: "Rounding error in the estimate grows like $\epsilon V / h^2$, faster than for delta."

## Level 2

6. l5-bisection-and-newton.json; l6-safe-root-finder.json | l5 screens[8].widget.solution (`bisect`), starter docstring, tests, how; l6 screens[7].widget.solution (`safe_newton`), starter docstring, tests, how | wrong, serious | Both solvers test the bracket with `if flo * fhi > 0`. Two defects follow. (a) A root exactly at `lo` passes the test, because the product is 0. The loop then treats `flo = 0` as "not positive" and moves `lo` off the root, so the solver converges to the other end and returns it with no error. A bond priced at the sum of its cash flows has yield 0, the lower end of the lesson's own bracket $[0, 0.2]$: `bisect` returns 20%. `safe_newton(lambda x: -x, lambda x: -1.0, 0.0, 1.0)` returns 1.0, where $f = -1$. (b) The product underflows: two positive values near $10^{-200}$ multiply to 0.0, so the missing sign change is not refused. Both docstrings promise "Raise ValueError" without a sign change, and l6 is titled "A root finder you can trust". A learner copies a bracket test that returns a non-root silently, in the one lesson whose point is that this cannot happen. | Press et al., *Numerical Recipes* 9.1 and 9.4: `rtbis` and `rtsafe` compare signs (`fl > 0 && fh > 0 || fl < 0 && fh < 0`) and `rtsafe` returns the end when $f$ is zero there. `numerics-L2-concepts-r2.py`: `l5:bisect_root_at_lower_end_is_found_or_refused`, `l6:safe_newton_root_at_lower_end_is_found_or_refused` and `l5/l6:same_sign_values_that_underflow_are_refused` are `EXPECTED_FAIL`. `fix:proposed_bisect_and_newton_pass_the_hidden_tests`, `fix:proposed_safe_newton_passes_the_hidden_tests` and `fix:proposed_code_handles_end_roots_and_underflow` pass for the code below. homework-2's `ytm_book` tests with `>=` and `<=` and does find a zero yield (`hw2:ytm_book_zero_yield_and_nan`). | Replace the functions, extend the docstrings, add one hidden test each and update the test counts. See "Fix 6" below for the paste-ready text.
7. l5-bisection-and-newton.json | screens[8].widget.solution (`newton`), starter | misleading, minor | The taught Newton stepper is `while True:` with no iteration cap. On $x^3 - 2x + 2$ from 0, the cycle the next lesson shows, it never returns, and in the app it hangs the Python worker. The lesson's last screen says a bad start "can send Newton anywhere", yet its code has no stop. A learner takes away an uncapped loop as the reference Newton. | `l5:taught_newton_loop_ends_on_x^3-2x+2_from_0` is `EXPECTED_FAIL` (10,000 steps of 1, 0, 1, 0). `fix:proposed_newton_raises_on_the_cycle` passes. Numerical Recipes 9.4 (`rtnewt` has `JMAX` and throws). | See "Fix 7" below.
8. l5-bisection-and-newton.json | screens[9].prose (third sentence), canvas.params.rows[1], widget.answer, widget.wrong[0], hints[2], feedback, explain.text | imprecise, minor | "Bisection on $[0, 0.2]$ needs 31 halvings, one evaluation each, after checking the ends", tabled as 31 evaluations per bond and keyed as $31/8 = 3.875 \pm 0.13$. The lesson's own `bisect` makes 33 calls on this bond, and screens[8] has just taught the count "twice to start and once per halving". A learner who counts as taught enters $33/8 = 4.125$ and is marked wrong. | `l5:s9_bisection_costs_31_evaluations_per_bond` is `EXPECTED_FAIL`: the solution returns `f_calls = 33`. | screens[9].prose, third sentence: "Bisection on $[0, 0.2]$ needs 2 evaluations to check the ends and 31 halvings: 33 evaluations." canvas.params.rows[1]: `["Bisection", "33", "yes"]`. widget.answer: `4.125`. widget.wrong[0].value: `8.25`. hints[2].text: "$33 / 8 \approx 4.1$." feedback.correct: "About 4.1 times cheaper: 33 against 8." feedback.generic: "Not quite right. Compare 33 with 8 evaluations, not with 4 iterations." explain.text, first sentence: "$33 / 8 \approx 4.1$, so Newton is about 4 times cheaper per bond."
9. l6-safe-root-finder.json | screens[7].widget.solution (`if abs(fx) < ftol`, default `ftol=1e-12`), widget.how (last sentence) | misleading, minor | The default call stops as soon as the residual is below $10^{-12}$. On $(x - 1)^9$ it returns 1.046, and on $10^{-9}(x^2 - 2)$ it stops $2 \times 10^{-6}$ short of the root. Level 1 taught that a small residual is a small error only when the problem is well conditioned (l3 screens[5]); here the taught solver stops on a residual by default and the lesson never says so. The hidden test has to pass `ftol=0.0` to dodge it, with no explanation. | `l6:safe_newton_default_call_reaches_the_ninefold_root_to_1e-9` is `EXPECTED_FAIL` (returns 1.0463). Higham ASNA 7.1 (residual against error); Numerical Recipes 9.4 (`rtsafe` stops on the step alone). | widget.how, last sentence replaced by two: "Last, (x − 1)⁹ on [0, 3] must reach 1 with ftol=0, which needs the halving rule. With the default ftol the same call stops at 1.046: a small residual is not a small error." screens[7].prose, add at the end: "Return early when $|f(x)|$ is below `ftol`; that test is safe only where the slope is not tiny, and `ftol=0` turns it off."
10. l6-safe-root-finder.json; course.json | screens[9].explain.text (first sentence); course.json lessonNames.l6-safe-root-finder | imprecise, minor | "The bracketed solver cannot fail on a valid quote, so every NaN points at the data." `implied_vols` also returns NaN for a valid quote whose vol lies outside the bracket $[0.0001, 5]$, and `safe_newton` can raise at `maxit`. The course map still calls the lesson "A root finder that never fails", although the lesson's own title is now "A root finder you can trust". | `l6:s9_bracketed_solver_cannot_fail_on_a_valid_quote` is `EXPECTED_FAIL`: a call priced at a vol of 6 comes back NaN. | screens[9].explain.text, first sentence: "The bracketed solver finds every vol between 0.0001 and 5, so here every NaN points at the data." course.json lessonNames.l6-safe-root-finder: "A root finder you can trust" (for the main session; auditors and content agents do not edit `course.json`).
11. l7-interpolation.json | screens[8].hints[0].text | imprecise, minor | "Alternating signs: the worst case for equal spacing." The worst error pattern at a point $x$ has the signs of the Lagrange basis values $\ell_k(x)$. Those alternate except across the interval that holds $x$. Alternating signs give 0.0292 at the worst strike; the true worst pattern gives 0.0299 there. The screen's explain line, "near the Lebesgue bound", is right. | Trefethen ATAP ch. 15 (Lebesgue function $\sum_k |\ell_k(x)|$). `l7:alternating_quote_errors` prints both values. | screens[8].hints[0].text: "The errors are equally spaced data with alternating signs: close to the worst case for equal spacing."
12. l8-splines.json | screens[2].explain.text (third sentence); summary.ideas[1]; screens[7].prose | imprecise, minor | "A tridiagonal system ... solved in $O(n)$ steps" and "so it costs $O(n)$". The lesson's own solution fills a dense matrix and calls `np.linalg.solve`, which is $O(n^3)$. The stated cost belongs to a banded solve that the code never shows. For eight quotes it does not matter, but the claim and the code disagree. | Burden and Faires 6.6 (Crout factorisation for tridiagonal systems, $O(n)$); the solution in screens[7]. | screens[2].explain.text, third sentence: "Six such rows make a tridiagonal system for $M_2$ to $M_7$, which a banded solver handles in $O(n)$ steps." summary.ideas[1]: "Its second derivatives solve one tridiagonal system, $O(n)$ work with a banded solver, and it never shows Runge's swings." screens[7].prose, add at the end: "For eight quotes a dense `np.linalg.solve` is fine; `scipy.linalg.solve_banded` gives the $O(n)$ cost on long curves."

## Level 3

13. l9-quadrature.json | screens[9].widget.options[2].why | imprecise, minor | "The trapezium rule has the same kink problem and a lower order." A kink does not lower the trapezium rule's order: it stays second order, with an erratic constant. With the kink inside, Simpson is second order too, so on this integrand the two rules have the same order. At $n = 128$ the trapezium error is $4.5 \times 10^{-4}$ and Simpson's is $6.4 \times 10^{-3}$. The option is still a wrong choice, but for a different reason. | `numerics-L3-concepts-r2.py` `l9:s9_trapezium_has_a_lower_order_than_simpson_with_the_kink_inside` is `EXPECTED_FAIL`: fitted slopes over $n = 16$ to 4096 are $-2.10$ (trapezium) and $-2.01$ (Simpson). `l9:trapezium_keeps_order_2_through_a_kink` passes on $|x - 1/\pi|$. Derivation: the panel that holds the kink adds a local error of order $h^2$, the size of the trapezium rule's own global error, so its order is unchanged. | screens[9].widget.options[2].why: "With a kink inside, both rules are erratic and second order. Only the split restores Simpson's fourth order."

## Fix 6: bracket test in `bisect` and `safe_newton`

l5 screens[8].widget.solution, replace `bisect` by:

```python
def bisect(f, lo, hi, tol):
    flo, fhi = f(lo), f(hi)
    calls = 2
    if flo == 0:
        return lo, calls
    if fhi == 0:
        return hi, calls
    if (flo > 0) == (fhi > 0):
        raise ValueError('no sign change')
    while hi - lo >= tol:
        mid = (lo + hi) / 2
        fm = f(mid)
        calls += 1
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2, calls
```

l5 screens[8].widget.starter, `bisect` docstring: `"""Halve [lo, hi] until hi - lo < tol. Return (root, f_calls).` / `If f is zero at an end, return that end. Raise ValueError if f(lo)` / `and f(hi) have the same sign."""`. New hidden test: call `bisect(lambda x: -x, 0.0, 1.0, 1e-9)[0]`, expect `0.0`, compare `isclose`, tol.abs `1e-9`. widget.how: "Submit runs 12 hidden tests." and add "A root at an end of the bracket must be returned."

l6 screens[7].widget.solution, replace the first three lines of the body (`flo, fhi = ...` to the `raise`) by the lines below, and change `if abs(fx) < ftol:` to `if abs(fx) <= ftol:` so an exact zero returns when `ftol=0`:

```python
    flo, fhi = f(lo), f(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if (flo > 0) == (fhi > 0):
        raise ValueError('no sign change')
```

l6 screens[7].widget.starter docstring, first line: `"""Root of f in [lo, hi]. If f is zero at an end, return that end.` New hidden test: call `safe_newton(lambda x: -x, lambda x: -1.0, 0.0, 1.0)`, expect `0.0`, compare `isclose`, tol.abs `1e-9`. widget.how: "Submit runs 8 hidden tests" and add "A root at an end of the bracket must be returned." The full replacement function is `FIX_SAFE` in `numerics-L2-concepts-r2.py`; it passes the seven current tests and the new one.

## Fix 7: iteration cap in `newton`

l5 screens[8].widget.solution, replace `newton` by:

```python
def newton(f, df, x0, tol, maxit=50):
    x, calls = x0, 0
    for _ in range(maxit):
        fx = f(x)
        calls += 1
        step = fx / df(x)
        x -= step
        if abs(step) < tol:
            return x, calls
    raise RuntimeError('no convergence')
```

l5 screens[8].widget.starter: `def newton(f, df, x0, tol, maxit=50):` with docstring `"""Newton steps until |step| < tol. Return (root, f_calls),` / `counting calls of f only. Raise RuntimeError after maxit steps."""`. Optional hidden test: call `newton(lambda x: x ** 3 - 2 * x + 2, lambda x: 3 * x * x - 2, 0.0, 1e-12)`, expect `RuntimeError`, compare `raises`.

## Noted, not conceptual

- l1-floating-point.json screens[9].prose: "Today that is about $1.7 \times 10^{18}$" was true in 2023 to 2024. It is now $1.79 \times 10^{18}$, still between $2^{60}$ and $2^{61}$, so the answer stands. Suggested: "about $1.8 \times 10^{18}$".
- l1-floating-point.json quiz[3].explain.text: "about half of $u$, as the rounding model promises". The model promises at most $u$. Suggested: "inside the bound $u = 1.11 \times 10^{-16}$".
- l8-splines.json screens[0].explain.text: "level 2's wiggles again" sits inside level 2. Suggested: "the last lesson's wiggles again".
- l6-safe-root-finder.json screens[8]: the vectorised `implied_vols` uses the bracket rule only. It has no halving rule and returns silently at `maxit`, unlike `safe_newton`. It is correct on every test and on 1,000 exact quotes (`l6:thousand_strikes_recovered`), so this is a difference to be aware of, not an error.

## Checked and clean

Conventions are stated once and kept: machine epsilon is $2^{-52}$, the gap above 1, and the unit roundoff is $u = 2^{-53}$; the rounding model carries its range (between `tiny` and `max`). The sample variance divides by $n - 1$. Zero rates are continuously compounded and the forward is $z + tz'$. Chebyshev nodes are the extreme points $\cos(k\pi/n)$, and the bounds quoted ($2^{1-n}$ for the node product, 2.42 for the Lebesgue constant at $n = 10$) are the ones for that set.

Theorems carry their hypotheses: the digits-lost rule is called a rule of thumb, and "loses about $\log_{10}\kappa(\mathbf A)$" is tied to a close fit wherever QR is compared with the normal equations; Newton's order 2 needs $f'(r) \ne 0$, with the double-root case named; bisection is certain "for a continuous $f$ with a sign change"; Runge's growth is claimed "for this $f$" and "for some smooth functions"; Simpson's $h^4$ needs four continuous derivatives; Gauss speed needs smoothness; local order $p + 1$ against global order $p$; stiffness is defined by stability, not accuracy, setting the step; unconditional stability is separated from accuracy and from L-stability.

Every empirical claim was rerun independently, with these results among others. The secant order tends to 1.618 in 3,000-digit arithmetic. Random matrices confirm $\kappa(\mathbf A^T\mathbf A) = \kappa(\mathbf A)^2$ and $\kappa(\mathbf R) = \kappa(\mathbf A)$. Twenty thousand random right-hand sides never exceed the $\kappa$ bound. Trefethen and Bau's degree-14 fit gives 0.99999998 by QR and $-0.16$ by the normal equations on this machine, as the screen says of a desktop NumPy. Gauss-Legendre is exact to degree $2n - 1$ and not $2n$ for $n = 1$ to 8. Monte Carlo error falls with slope $-0.5$ over 300 replications per sample size, and a CRR tree with slope $-1$. The implicit Euler and trapezoidal factors are at most 1 at 40,000 random points of the left half-plane. `solve_ivp` reproduces 1,172, 422 and 226 evaluations in SciPy 1.18.1. The fastest rate of a Black-Scholes grid quadruples when $\Delta S$ halves.

## Overlap with the earlier reads

Read after the ledger, scripts and findings above were committed (`9329a8f0`, `634a2e69`): `docs/reviews/review-numerics-1-3.md` (second reader, 31 findings, fix pass `1bc2a38b`) and `docs/reviews/audit-numerics-1-3.md` (round-1 concept audit, 22 findings, fix pass `6dce011e`). Both fix passes were applied before this read, so this audit read the content after them. The round-1 audit counted 11 of the review's 31 findings as conceptual; this table adds a twelfth, the review's note on l5 screens[9] (31 against 33 evaluations), because it is the same convention as finding 8 here.

| Conceptual findings | Count | Which |
|---|---|---|
| Found by this audit only | 12 | findings 1 to 7 and 9 to 13 |
| Found by the earlier reads only | 32 | round-1 audit findings 1 to 22 (its finding 12 shared with the review) and 10 review-only findings; all were fixed before this read |
| Found by both | 1 | finding 8: the review saw that 31 counts halvings while screens[8] counts 33 calls, and its fix pass reworded one sentence; the table, the key and the feedback still say 31 |

Two near overlaps are counted as this audit only, because the earlier read judged the text sound. Round-1 finding 4 rewrote the l3 screens[4] sentence about $\tfrac{1 + r}{1 - r}$ for another reason (it is the normal-equations figure) and left the sign condition out (finding 2 here). Round 1's "Noted" list called l6 screens[9] true as it stands and retitled the lesson; finding 10 here shows the sentence fails outside the bracket and that `course.json` still carries the old name. The second reader's "checked and correct" list passes the 8.5 vol points of finding 3 as arithmetic.

Whether each finding sits in text or code a fix pass wrote (`git show` of each path before and after `1bc2a38b` and `6dce011e`):

| Finding | In fix-pass text or code | Detail |
|---|---|---|
| 1, 3, 4, 5, 7, 11, 12, 13 | no | original author text or code, untouched by both fix passes |
| 2 | partly, round-1 fix pass | the screens[4] sentence is round-1 fix text ("correlation matrix, whose $\kappa$ is ..."); the quiz[0] prose is original |
| 6 | partly, round-1 fix pass | the round-1 fix pass rewrote `safe_newton` and kept the original line `if flo * fhi > 0`; it added `RuntimeError` and the title "you can trust", which make the silent wrong return stand out more. `bisect` in l5 is original |
| 8 | yes, second reader's fix pass | the sentence "31 halvings, one evaluation each, after checking the ends" is that pass's text; the table and key are original |
| 9 | yes, round-1 fix pass | the default `ftol=1e-12` is original; the hidden test with `ftol=0.0` and the `how` sentence that mentions it without explanation are round-1 fix text |
| 10 | partly, round-1 fix pass | screens[9] is original; the stale `course.json` name is an omission of the round-1 retitling |

So 4 of the 13 findings touch what the round-1 fix pass wrote or left behind (2, 6, 9, 10), 1 sits in the second reader's fix text (8), and 8 are in original text that two earlier reads passed. The one serious finding (6) is in code that all three earlier passes ran: the author, the second reader and the round-1 auditor and fixer each executed `bisect` and `safe_newton`, always on brackets with a strict sign change.

All other fix-pass text was read blind with the rest and then reread against the list of 78 strings changed by `6dce011e`. No further defect was found in it: the `rtsafe` halving rule is implemented as Numerical Recipes states it, the nine-fold root does need it, and the reworded Runge, Simpson-panel, close-fit and variance-conditioning passages hold.

## Gate results

- Validator (from `app/`): `0 errors, 4115 warnings`; `git status` clean afterwards.
- Round-2 concept scripts: `numerics-L1-concepts-r2.py` exit 0 (68 checks passed, 4 `EXPECTED_FAIL`); `numerics-L2-concepts-r2.py` exit 0 (58 passed, 7 `EXPECTED_FAIL`); `numerics-L3-concepts-r2.py` exit 0 (49 passed, 1 `EXPECTED_FAIL`). Each `EXPECTED_FAIL` prints the corrected assert. NumPy 2.5.3, SciPy 1.18.1, Python 3.13.
- Author number scripts (from `app/`): `numerics-L1-numbers.py` exit 0, `numerics-L2-numbers.py` exit 0, `numerics-L3-numbers.py` exit 0 (each "all checks passed").
- Code tasks: 17 solutions pass all their hidden tests and all 17 starters fail (inside the concept scripts). The replacement code of fixes 6 and 7 passes the current hidden tests and the proposed new ones.
- No content file, engine file or `course.json` was changed. Playthrough was not run: nothing playable changed.
