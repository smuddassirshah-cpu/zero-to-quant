# Claim ledger: delta audit, 26 Nov 2026, batch 3

Eleven closed courses, the content changed between each course's close and `e69cac72`. One row per added or changed claim. "script" is `docs/reports/audit-delta-2026-11-26-3-concepts.py` (exit 0). All eleven courses are Stage 1 to 3, so the ledger is full depth.


## algo-think

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l6-call-stack.json | screens (choice "loop").explain.text | A list holds 50,000 items with ease; the default recursion limit stops the call stack far short of 50,000 frames | correct | Python docs, `sys.getrecursionlimit` (default 1,000); the old wording ("cannot hold") was false once the limit is raised, as the `limit` option on the same screen says |
| l9-halving.json | screens[3].feedback.byKey.test-12 (a) | Test 12 allows at most 45 reads, and this miss (777777 in a million evens) takes all 20 passes | correct | tests[11] reads `big.looks <= 45`; script: 20 passes |
| l9-halving.json | screens[3].feedback.byKey.test-12 (b) | A search testing `==`, then `<`, then `>` reads `xs[mid]` up to three times a pass: 50 reads here | correct | script: 2 reads on a right move, 3 on a left move, 50 in all |
| l9-halving.json | screens[3].feedback.byKey.test-12 (c) | Its answer is right all the same; reading once into a variable passes | correct | script: returns -1; the one-read search uses 20 reads |

## coding-int

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-2.json | items (longform, three-minute talk).prompt | The statement to explain is that of the lesson "Simulating the rules" | correct | `course.json` names `l8-simulating-the-rules` so; script |
| homework-2.json | items (matching events).prose | The event format is that of the lesson "A matching engine" | correct | `course.json` names `l10-matching-engine` so; script |
| review-2.json | items (bot rules).prose | The bot is that of the lesson "Simulating the rules"; its four rules are unchanged | correct | same; the rules match the lesson statement quoted in homework-2 |

## conditional

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l3-shrinking.json | screens[1].feedback.byKey.r1c1 | (1, 1) adds to 2, not 8 | correct | addition; script reads the line |
| l3-shrinking.json | screens[1].feedback.byKey.r2c2 | (2, 2) adds to 4, not 8 | correct | addition; script reads the line |
| l3-shrinking.json | screens[1].feedback.byKey.r3c3 | (3, 3) adds to 6, not 8 | correct | addition; script reads the line |
| l3-shrinking.json | screens[1].feedback.byKey.r1c5 | (1, 5) adds to 6, not 8 | correct | addition; script reads the line |
| l3-shrinking.json | screens[1].feedback.byKey.r5c5 | (5, 5) adds to 10, not 8 | correct | addition; script reads the line |
| l3-shrinking.json | screens[1].feedback.byKey.r6c6 | (6, 6) adds to 12, not 8 | correct | addition; script reads the line |
| l3-shrinking.json | screens[6].canvas.params.keep | The filter keeps a roll when `d1 == 5 \|\| d2 == 5`, the event "at least one 5" | correct | matches the caption and the 11-cell cross; enumeration in script |
| l3-shrinking.json | screens[6].canvas.params.event | Among kept rolls the event "total 10" has exact share 1/11 | correct | only (5, 5) of the 11 kept outcomes totals 10; enumeration and Monte Carlo (600,000 rolls) in script |
| l3-shrinking.json | screens[6].explain.text (a) | 11 of 36 outcomes contain a 5, so about 1000 x 11/36 = 305.6 rolls survive | correct | enumeration; Monte Carlo in script |
| l3-shrinking.json | screens[6].explain.text (b) | Rolling 1,000 shows the share of total 10 among kept rolls settling near 1/11 | correct | law of large numbers; the seeded canvas (mulberry32, seed 4226) keeps 308 of 1,000 with 28 totals of 10, 28/308 = 1/11; script |
| l3-shrinking.json | screens[6].explain.text (c) | "1/11, the shrunk space": the number is named as the space | imprecise | 1/11 is the chance of a total of 10 inside the shrunk space of 11 outcomes, not the space; finding 1 |
| l3-shrinking.json | screens[7].widget.options[right].canvas.caption | After the news three equally likely outcomes are left, each 1/3 | correct | P(outcome \| at least one up) = (1/4)/(3/4); enumeration in script |

## ds

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l4-frequencies.json | screens (anagram choice).options[loop].why (a) | Each `.count` scans a whole string, so the loop is O(n^2) | correct | n characters, each with two O(n) scans; CLRS ch. 3 counting |
| l4-frequencies.json | screens (anagram choice).options[loop].why (b) | Without a length check it is wrong too: `ab` and `abc` pass, because letters only in `b` are never checked | correct | script: the loop returns True on (ab, abc), and agrees with the sorted check on every equal-length pair over {a, b, c} up to length 5, so the added condition is exactly what the old line lacked (the question fixes both lengths at n) |

## ito

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l5-integrating-noise.json | screens[0].widget.wrong[sign] | Slip value 0.1853: minus the key (key -0.1853) | correct | script: value, and band clear of the key and of every other slip |
| l5-integrating-noise.json | screens[0].feedback.byKey | The products 0, 0.2675, -0.2745 and -0.1782 add to -0.1853; a positive value books the net loss as a gain | imprecise | the four quoted products add to -0.1852; -0.1853 is the unrounded sum, as the explain on the same screen says in brackets; finding 2 |
| l5-integrating-noise.json | screens[4].widget.wrong[sign] | Slip value 0.3533: minus the key (key -0.3533) | correct | script: value, and band clear of the key and of every other slip |
| l5-integrating-noise.json | screens[4].feedback.byKey | W1^2 = 0.2934 < 1, so (0.2934 - 1)/2 is negative; 0.3533 is (1 - 0.2934)/2 | correct | arithmetic; script |
| l5-integrating-noise.json | quiz[0] q-left-small.widget.wrong[sign] | Slip value 1: minus the key (key -1) | correct | script: value, and band clear of the key and of every other slip |
| l5-integrating-noise.json | quiz[0] q-left-small.feedback.byKey | Products 0, 2 and -3 add to -1, the last move being a fall from 3; a positive 1 takes 3 - 2 | correct | arithmetic; script |
| l8-fair-games.json | quiz[0] q-drift-w4.widget.wrong[sign] | Slip value 3: minus the key (key -3) | correct | script: value, and band clear of the key and of every other slip |
| l8-fair-games.json | quiz[0] q-drift-w4.feedback.byKey | The dt coefficient of W^2 - 4t is 1 - 4 < 0; a positive 3 takes 4 - 1 | correct | Ito's lemma, f_t + f_xx/2 = -4 + 1 (Shreve II, 4.4); Monte Carlo of E[W_1^2 - 4] in script |
| l9-bs-pde.json | quiz[3] q-put.widget.wrong[sign] | Slip value 1.6579: minus the key (key -1.6579) | correct | script: value, and band clear of the key and of every other slip |
| l9-bs-pde.json | quiz[3] q-put.feedback.byKey | Theta = rV - (1/2)sigma^2 S^2 Gamma - rS Delta = 0.2787 - 3.7524 + 1.8158; the gamma term outweighs the others | correct | Black-Scholes PDE solved for theta (Hull ch. 19); script recomputes V, Delta, Gamma and theta two ways |
| review-2.json | items[0] r-left-sum.widget.wrong[sign] | Slip value 0.25: minus the key (key -0.25) | correct | script: value, and band clear of the key and of every other slip |
| review-2.json | items[0] r-left-sum.feedback.byKey | The last product 1.5 x (-0.5) = -0.75 outweighs the 0.5 before it; a positive 0.25 takes 0.75 - 0.5 | correct | arithmetic; script |

## limits-thm

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l19-generating-functions.json | explain/why (Cauchy line) (a) | A Cauchy's density decays like 1/x^2 | correct | f(x) = 1/(pi(1 + x^2)); script: x^2 f(x) -> 1/pi, while the tail P(X > x) goes like 1/(pi x), so the old word "tails" was wrong and the new one is right |
| l19-generating-functions.json | explain/why (Cauchy line) (b) | That decay is far too slow to offset e^{tx}, so no MGF (and no mean) | correct | Casella and Berger 2.3 (ex. 2.2.4 and MGF existence); script: the truncated integral grows without bound |

## mental-pressure

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-3.json | items[5] h-last-five-guesses.widget.wrong[sign] | Slip value 1.6667: minus the key (key -1.6667) | correct | script: value, and band clear of the key and of every other slip |
| homework-3.json | items[5] h-last-five-guesses.feedback.byKey | Each guess among three is worth 1/3 - 2/3 = -1/3, five make -5/3; the positive value reads as if guessing helped | correct | expected value; Monte Carlo of one guess in script |
| l13-negative-marking.json | screens[2].widget.wrong[sign] | Slip value 0.6: minus the key (key -0.6) | correct | script: value, and band clear of the key and of every other slip |
| l13-negative-marking.json | screens[2].feedback.byKey | 1/5 x 1 + 4/5 x (-1) = 0.2 - 0.8; a positive 0.6 takes 0.8 - 0.2 | correct | arithmetic; script |
| l13-negative-marking.json | screens[7].widget.wrong[sign] | Slip value 0.3333: minus the key (key -0.3333) | correct | script: value, and band clear of the key and of every other slip |
| l13-negative-marking.json | screens[7].feedback.byKey | (2 - k)/k at k = 3 is -1/3, a loss; a positive value takes (k - 2)/k | correct | arithmetic; script |
| l13-negative-marking.json | quiz[1] q-half-penalty.widget.wrong[sign] | Slip value 0.125: minus the key (key -0.125) | correct | script: value, and band clear of the key and of every other slip |
| l13-negative-marking.json | quiz[1] q-half-penalty.feedback.byKey | 1/4 - 3/8 < 0 because the penalty outweighs the chance of a mark; 0.125 takes 3/8 - 1/4 | correct | arithmetic; script |
| l6-percent-of-percent.json | screens[0].widget.wrong[sign] | Slip value 0.01 (+1%): minus the key (key -0.01 (-1%)) | correct | script: value, and band clear of the key and of every other slip |
| l6-percent-of-percent.json | screens[0].feedback.byKey | £110 falls 10% to £99, below the £100 start; +1% books the loss as a gain | correct | arithmetic; script |
| l6-percent-of-percent.json | screens[1].widget.wrong[sign] | Slip value 0.04 (+4%): minus the key (key -0.04 (-4%)) | correct | script: value, and band clear of the key and of every other slip |
| l6-percent-of-percent.json | screens[1].feedback.byKey | £120 falls 20% to £96, below the £100 start; +4% books the loss as a gain | correct | arithmetic; script |
| l9-eighty-in-eight.json | quiz[2] q-blind-guess.widget.wrong[sign] | Slip value 0.5: minus the key (key -0.5) | correct | script: value, and band clear of the key and of every other slip |
| l9-eighty-in-eight.json | quiz[2] q-blind-guess.feedback.byKey | Right earns 1/4 and wrong costs 3/4, so 1/4 - 3/4 < 0; 0.5 takes 3/4 - 1/4 | correct | arithmetic; script |
| review-2.json | items[1] r-up-down-30.widget.wrong[sign] | Slip value 0.09 (+9%): minus the key (key -0.09 (-9%)) | correct | script: value, and band clear of the key and of every other slip |
| review-2.json | items[1] r-up-down-30.feedback.byKey | 1.3 x 0.7 = 0.91 < 1, so the net change is -9% | correct | arithmetic; script |

## numerics

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-2.json | items[3] h2-spline-m.widget.wrong[sign] | Slip value 2: minus the key (key -2) | correct | script: value, and band clear of the key and of every other slip |
| homework-2.json | items[3] h2-spline-m.feedback.byKey | The right side is 6(0 - 2) = -12 because the slopes fall, and -12/6 = -2 | correct | natural-spline row 2(h1 + h2)M2 = 6(slope difference), Burden and Faires 3.5; script |
| l11-step-size.json | screens[3].widget.wrong[sign] | Slip value 1.1: minus the key (key -1.1) | correct | script: value, and band clear of the key and of every other slip |
| l11-step-size.json | screens[3].feedback.byKey | y10 - y20 = 1.81294125 - 1.81295781 < 0, so the estimated error is negative | correct | Richardson estimate (y_h - y_{h/2})/(2^p - 1), Hairer, Norsett and Wanner II.4; script |
| l12-stiff-equations.json | screens[0].widget.wrong[exact].tol | Band of the `exact` slip tightened from 0.0002 to 0.00002 (0.002 of a per cent) | correct | script: 5.2253%, 5.23% and the h = 0.02 value 5.2222% now sit in separate bands; before, the old band swallowed both neighbours |
| l12-stiff-equations.json | screens[0].widget.wrong[exact-rounded] | Slip value 0.0523: the exact 5.2253% rounded to two places | correct | script solves the system exactly (5.2253%) and by Euler (8.2393% at h = 0.04, 5.2222% at h = 0.02) |
| l12-stiff-equations.json | screens[0].feedback.byKey.exact-rounded | That is the exact value, rounded; Euler at 0.04 is far off | correct | same; 8.24% against 5.23% |
| l8-splines.json | screens[2].widget.wrong | Slip value 0.0015: key over 100 (rates as decimals) (key 0.15) | correct | script: value, and band clear of the key and of every other slip |
| l8-splines.json | screens[2].feedback.byKey | 0.0015 is 0.15% written as a decimal; the field wants the number of per cent | correct | script: the row with rates 0.0405, 0.0395, 0.0390 gives 0.0015 |
| review-4.json | items[1] r4-predict-ds.widget.wrong[sign] | Slip value 0.00049: minus the key (key -0.00049) | correct | script: value, and band clear of the key and of every other slip |
| review-4.json | items[1] r4-predict-ds.feedback.byKey | The error -0.0078 is negative and dividing by 16 keeps the sign | correct | second-order error scales with the square of the step; script |

## pdes

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-1.json | items[4] h-unstable.widget.wrong[sign] | Slip value 0.24: minus the key (key -0.24) | correct | script: value, and band clear of the key and of every other slip |
| homework-1.json | items[4] h-unstable.feedback.byKey | After one step the spike is -0.2 and its neighbour 0.6, so the middle is 0.6 + 0.6(-0.2 - 1.2) = -0.24 | correct | explicit scheme applied twice in script |
| homework-3.json | items[2] h-r0-sigma.widget.wrong | Slip value 0.1067: key over 100 (key 10.67) | correct | script: value, and band clear of the key and of every other slip |
| homework-3.json | items[2] h-r0-sigma.feedback.byKey | 0.1067 is 10.67% written as a decimal | correct | arithmetic; script |
| l8-heat-on-a-rod.json | screens[3].widget.wrong[sign] | Slip value 8.3532: minus the key (key -8.3532) | correct | script: value, and band clear of the key and of every other slip |
| l8-heat-on-a-rod.json | screens[3].feedback.byKey | Every eigenvalue of the matrix is negative because the formula starts with -4/dx^2; the positive value drops that minus | correct | eigenvalues of the second-difference matrix (LeVeque, Finite Difference Methods, 2.10); script: all nine eigenvalues negative, the third is -8.3532 |
| l8-heat-on-a-rod.json | screens[5].widget.wrong[sign] | Slip value 1.3413: minus the key (key -1.3413) | correct | script: value, and band clear of the key and of every other slip |
| l8-heat-on-a-rod.json | screens[5].feedback.byKey | The factor is 1 - 4 lambda sin^2(81 deg) = 1 - 2.3413, negative, so the mode flips each step | correct | von Neumann factor (LeVeque 9.6); script |
| l9-black-scholes-to-heat.json | quiz[1] q-coeff.widget.wrong[sign] | Slip value 0.04: minus the key (key -0.04) | correct | script: value, and band clear of the key and of every other slip |
| l9-black-scholes-to-heat.json | quiz[1] q-coeff.feedback.byKey | k - 1 = 0.96 - 1 < 0 because k is just under 1; 0.04 takes 1 - 0.96 | correct | k = 2r/sigma^2 (Wilmott, Howison and Dewynne 5.4); script |
| l9-black-scholes-to-heat.json | quiz[2] q-beta.widget.wrong[sign] | Slip value 0.9604: minus the key (key -0.9604) | correct | script: value, and band clear of the key and of every other slip |
| l9-black-scholes-to-heat.json | quiz[2] q-beta.feedback.byKey | beta = -(k + 1)^2/4 starts with a minus: -3.8416/4 | correct | same source; script |
| review-3.json | items[1] r-beta.widget.wrong[sign] | Slip value 0.892: minus the key (key -0.892) | correct | script: value, and band clear of the key and of every other slip |
| review-3.json | items[1] r-beta.feedback.byKey | beta = -(k + 1)^2/4 = -3.5679/4 | correct | same; script |
| homework-1.json | items[5] h-derive-lazy-walk.prompt (a) | Setting: steps right p, left q, stays r = 1 - p - q; u(x, t) the chance of standing at x; data dx = 0.1, dt = 0.004, p = 0.45, q = 0.35 | correct | well posed; r = 0.2; the lazy walk has no parity gap, so u is one smooth profile |
| homework-1.json | items[5] h-derive-lazy-walk.prompt (b) | Optional point: the update u(x, t + dt) = p u(x - dx, t) + q u(x + dx, t) + r u(x, t); the right step comes from the left neighbour | correct | total probability over the last move (Lawler, Random Walk and the Heat Equation, 2.1); script iterates it and recovers the exact moments |
| homework-1.json | items[5] h-derive-lazy-walk.model, Hypotheses | u smooth with u_tt and u_xxx bounded; steps shrink with r fixed and r < 1 | correct | exactly what the two Lagrange remainders below use |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 1 | The three ways in are separate and the move is independent of the position, so the update holds; swapping the neighbours flips the sign of the drift | correct | law of total probability; with p and q swapped the first-order term is +(p - q)dx u_x |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 2 | u(x, t + dt) = u + dt u_t + R_t with \|R_t\| <= dt^2 max\|u_tt\| / 2 | correct | Taylor's theorem with Lagrange remainder (Rudin, Principles, 5.15) |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 3 (a) | u(x -+ dx) = u -+ dx u_x + dx^2 u_xx / 2 + R with \|R\| <= dx^3 max\|u_xxx\| / 6 | correct | same theorem |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 3 (b) | Weighted sum: (p + q + r)u - (p - q)dx u_x + (p + q)dx^2 u_xx / 2 + pR- + qR+; the u_x terms cancel only when p = q | correct | direct expansion: p(-dx u_x) + q(+dx u_x) |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 4 | u_t + R_t/dt = -(p - q)dx/dt u_x + (p + q)dx^2/(2dt) u_xx + (pR- + qR+)/dt | correct | subtract u, divide by dt |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 5 (a) | c = (p - q)dx/dt, D = (p + q)dx^2/(2dt) = (1 - r)dx^2/(2dt); with D, c fixed, dt = (1 - r)dx^2/(2D) and p - q = c(1 - r)dx/(2D) | correct | algebra; script checks both identities on the data |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 5 (b) | A fixed bias would make c grow like 1/dx; dt shrinking like dx would send D to 0 | correct | c = (p - q) dx/dt with dt ~ dx^2; D ~ dx^2/dt ~ dx |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 6 (a) | \|R_t/dt\| <= dt max\|u_tt\| / 2; \|(pR- + qR+)/dt\| <= D dx max\|u_xxx\| / 3, using (p + q)dx^2/dt = 2D | correct | (p + q)dx^3/(6dt) = 2D dx/6 |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 6 (b) | The bound is not sharp: with p - q of order dx the space remainder over dt is of order dx^2 | correct | third-order terms combine to -(p - q)dx^3 u_xxx/6 = O(dx^4), fourth-order term is O(dx^4); script: the residual of the update on the kernel falls fourfold when dx halves |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 7 | Limit u_t + c u_x = D u_xx; staying put scales D by 1 - r; r = 0, p = q = 1/2 gives the fair walk D = dx^2/(2dt) | correct | drift-diffusion (Fokker-Planck) limit of a biased walk (Lawler 2.1; Gardiner, Stochastic Methods, 3.8) |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 8 (a) | D = 0.8 x 0.01/0.008 = 1 and c = 0.1 x 0.1/0.004 = 2.5 | correct | script |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 8 (b) | The solution from a point at 0 is the heat kernel moved by ct: mean ct = 2.5, variance 2Dt = 2 at t = 1 | correct | substituting y = x - ct removes c u_x; script: finite-difference residual of N(ct, 2Dt) in the equation is below 1e-5 |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 8 (c) | 250 independent steps, each mean 0.01, mean square 0.008, variance 0.0079; the walk has mean 2.5 and variance 1.975 | correct | script: exact by formula, exact by iterating the update, and Monte Carlo (40,000 walks) |
| homework-1.json | items[5] h-derive-lazy-walk.model, step 8 (d) | The variance gap n(p - q)^2 dx^2 = c^2 dt t = 0.025 vanishes as dt -> 0 with c fixed | correct | script; n m1^2 = (t/dt)(c dt)^2 |
| homework-1.json | items[5] h-derive-lazy-walk.rubric[0] | 1 point, optional: the update and the reason (three separate ways in; right step from the left neighbour) | correct | matches model step 1 and the optional line of the prompt |
| homework-1.json | items[5] h-derive-lazy-walk.rubric[1] | 3 points: time to first order, space to second, p + q + r = 1 cancels u, and the equation with c and D | correct | matches steps 2 to 4 and 7 |
| homework-1.json | items[5] h-derive-lazy-walk.rubric[2] | 4 points: dt like dx^2 and p - q like dx; time remainder over dt at most a multiple of dt; space remainder (over dt) at most a multiple of dx, with dx^2 also accepted | correct | matches steps 5 and 6; "over dt" is carried from the sentence before, and the row reads true either way |
| homework-1.json | items[5] h-derive-lazy-walk.rubric[3] | 2 points: D = 1, c = 2.5, mean 2.5 = ct, variance 1.975 is 0.025 below 2Dt = 2 | correct | matches step 8; rubric totals 10 |

## random-vars

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-4.json | items[7] h-three-regimes.widget.wrong[sign] | Slip value 85: minus the key (key -85) | correct | script: value, and band clear of the key and of every other slip |
| homework-4.json | items[7] h-three-regimes.feedback.byKey | 200 - 60 - 225: the crisis term outweighs the 140 from the other days; +£85 books the daily loss as a gain | correct | law of total expectation; script |
| l14-independent-rvs.json | quiz[1] q-exy.widget.wrong[sign] | Slip value 6: minus the key (key -6) | correct | script: value, and band clear of the key and of every other slip |
| l14-independent-rvs.json | quiz[1] q-exy.feedback.byKey | E[Y] = -3, so 2 x (-3) = -6 | correct | E[XY] = E[X]E[Y] under independence (Casella and Berger 4.2.10); Monte Carlo in script |
| l19-convex-bets.json | screens[10].widget.wrong | Slip value 0.0006: key over 10,000 (returns as decimals) (key 6) | correct | script: value, and band clear of the key and of every other slip |
| l19-convex-bets.json | screens[10].feedback.byKey | 0.0006 is the bound with returns as decimals; times 10,000 gives 6 %^2 | correct | 0.02 x 0.03 = 0.0006; one per cent squared is 1e-4; script |
| l6-fair-price.json | quiz[1] q-double-six.widget.wrong[sign] | Slip value 2.4444: minus the key (key -2.4444) | correct | script: value, and band clear of the key and of every other slip |
| l6-fair-price.json | quiz[1] q-double-six.feedback.byKey | The £3 ticket returns about £0.56 on average, so 0.56 - 3 < 0; 2.44 takes 3 - 0.56 | correct | arithmetic; script |
| review-4.json | items[4] r-cond-mean.widget.wrong | Slip value 0.005: key over 100 (key 0.5) | correct | script: value, and band clear of the key and of every other slip |
| review-4.json | items[4] r-cond-mean.feedback.byKey | 0.005 is 0.5% written as a decimal | correct | arithmetic; script |

## research-int

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-1.json | items[0].parts[0].widget.wrong[sign] | Slip value 0.28: minus the key (key -0.28) | correct | script: value, and band clear of the key and of every other slip |
| homework-1.json | items[0].parts[0].feedback.byKey | Centre 0.36 and "width" 0.64, so the smallest c is 0.36 - 0.64 < 0 | imprecise | numbers right (PSD edge checked in script), but 0.64 is the half-width; the range [-0.28, 1] is 1.28 wide and the item's own lines say half-width; finding 3 |
| homework-1.json | items[0].parts[1].widget.wrong[sign] | Slip value 0.3324: minus the key (key -0.3324) | correct | script: value, and band clear of the key and of every other slip |
| homework-1.json | items[0].parts[1].feedback.byKey | The "width" 0.5724 exceeds the centre 0.24, so 0.24 - 0.5724 < 0 | imprecise | same: 0.5724 is the half-width; finding 3 |
| homework-1.json | items[0].parts[2].widget.wrong[sign] | Slip value 0.3333: minus the key (key -0.3333) | correct | script: value, and band clear of the key and of every other slip |
| homework-1.json | items[0].parts[2].feedback.byKey | 1 + 3 rho >= 0 gives rho >= -1/3 | correct | equicorrelation matrix eigenvalue 1 + (n - 1)rho (Horn and Johnson 1.2 example; Meucci 3.3); eigenvalues in script |
| l10-weak-signals.json | screens[7].widget.wrong[sign] | Slip value 1: minus the key (key -1) | correct | script: value, and band clear of the key and of every other slip |
| l10-weak-signals.json | screens[7].feedback.byKey | Selling yesterday's position and buying today's is two trades, 6 bp, so 5 - 6 < 0 | correct | arithmetic; script |
| l11-framing-the-question.json | screens[8].widget.wrong[sign] | Slip value 0.18: minus the key (key -0.18) | correct | script: value, and band clear of the key and of every other slip |
| l11-framing-the-question.json | screens[8].feedback.byKey | Gross edge 0.32 bp less cost 0.5 bp is below zero | correct | 0.52 x 8 - 0.48 x 8 = 0.32; script |
| l2-correlation-limits.json | screens[4].widget.wrong[sign] | Slip value 0.5: minus the key (key -0.5) | correct | script: value, and band clear of the key and of every other slip |
| l2-correlation-limits.json | screens[4].feedback.byKey | 1 + 2 rho >= 0 gives rho >= -1/2 | correct | as above; eigenvalues in script |
| l2-correlation-limits.json | screens[5].widget.wrong[sign] | Slip value 0.5: minus the key (key -0.5) | correct | script: value, and band clear of the key and of every other slip |
| l2-correlation-limits.json | screens[5].feedback.byKey | Centre 0.25 and "width" 0.75, so the lowest c is 0.25 - 0.75 | imprecise | same: 0.75 is the half-width, the word used by the hint, the generic line and the `product` line of this screen; finding 3 |
| l2-correlation-limits.json | screens[8].widget.wrong[sign] | Slip value 0.25: minus the key (key -0.25) | correct | script: value, and band clear of the key and of every other slip |
| l2-correlation-limits.json | screens[8].feedback.byKey | 1 + 4 rho >= 0 gives rho >= -1/4 | correct | as above; eigenvalues in script |
| l2-correlation-limits.json | quiz[2] q-equicorr-six.widget.wrong[sign] | Slip value 0.2: minus the key (key -0.2) | correct | script: value, and band clear of the key and of every other slip |
| l2-correlation-limits.json | quiz[2] q-equicorr-six.feedback.byKey | 1 + 5 rho >= 0 gives rho >= -0.2 | correct | as above; eigenvalues in script |
| l6-bias-variance-aloud.json | screens[8].widget.wrong | Slip value 0.0008: key over 10,000 (returns as decimals) (key 8) | correct | script: value, and band clear of the key and of every other slip |
| l6-bias-variance-aloud.json | screens[8].feedback.byKey | 0.0008 is the MSE with returns as decimals; times 10,000 gives 8 %^2 | correct | MSE = bias^2 + variance (Hastie, Tibshirani and Friedman 7.3); script, with Monte Carlo |
| l7-ridge-against-lasso.json | quiz[1] q-ridge-one.widget.wrong[sign] | Slip value 0.2667: minus the key (key -0.2667) | correct | script: value, and band clear of the key and of every other slip |
| l7-ridge-against-lasso.json | quiz[1] q-ridge-one.feedback.byKey | Ridge multiplies -0.4 by 2/3 and keeps its sign | correct | orthonormal-design ridge b/(1 + lambda) (Hastie, Tibshirani and Friedman 3.4, table 3.4); script |
| review-3.json | items[0] r3-mse-four.widget.wrong | Slip value 0.0000045: key over 10,000 (returns as decimals) (key 0.045) | correct | script: value, and band clear of the key and of every other slip |
| review-3.json | items[0] r3-mse-four.feedback.byKey | 0.0000045 is the MSE with returns as decimals; times 10,000 gives 0.045 %^2 | correct | script |

## Counts

| course | rows | correct | wrong | imprecise | misleading | unverified |
|---|---|---|---|---|---|---|
| algo-think | 4 | 4 | 0 | 0 | 0 | 0 |
| coding-int | 3 | 3 | 0 | 0 | 0 | 0 |
| conditional | 12 | 11 | 0 | 1 | 0 | 0 |
| ds | 2 | 2 | 0 | 0 | 0 | 0 |
| ito | 12 | 11 | 0 | 1 | 0 | 0 |
| limits-thm | 2 | 2 | 0 | 0 | 0 | 0 |
| mental-pressure | 16 | 16 | 0 | 0 | 0 | 0 |
| numerics | 11 | 11 | 0 | 0 | 0 | 0 |
| pdes | 35 | 35 | 0 | 0 | 0 | 0 |
| random-vars | 10 | 10 | 0 | 0 | 0 | 0 |
| research-int | 24 | 21 | 0 | 3 | 0 | 0 |
| total | 131 | 126 | 0 | 5 | 0 | 0 |
