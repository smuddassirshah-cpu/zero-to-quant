# Concept audit, round 2: integrals levels 1 to 3

Blind read at commit `83aadaaa` by a fresh auditor (name `integrals-1-3-r2`). Scope: lessons l1 to l13, review-1 to -3, homework-1 to -3, problems-1 to -3, and the fluency files for l6, l7, l9 and l10. Sources: Spivak, *Calculus* (ch. 13, 14, 19); Stewart, *Calculus* (5.1 to 5.5, 6.1, 6.5, 7.1, 7.7, 7.8); Apostol, *Calculus* I; Casella and Berger (2.2, 4.7) for the density screens.

Files written:

- Ledger: `docs/reports/audit-integrals-1-3-r2-ledger.md`, 4,085 rows: correct 4,069, wrong 2, imprecise 13, misleading 1, unverified 0. The 16 rows that are not `correct` belong to the 11 findings below.
- Concepts script: `docs/reports/integrals-L1-3-concepts-r2.py`, 71 checks. It exits 1 at this commit: two checks fail because the content is wrong (findings 1 and 2). The other 69 pass.
- Code sweep: `docs/reports/integrals-L1-3-test-line-sweep-r2.mjs` (`node <script> <app dir> <pkgs>`), run through `app/tools/code-runner.mjs` under the page's Pyodide 0.27.7. Results in the section "Code widgets".

## What was checked

Every graded key, every `wrong[]` value and every number printed in a hint, feedback line or explanation was recomputed, by sympy or `scipy.integrate` and a second time by hand or by a Riemann or trapezium routine. The fundamental theorem is stated with its hypotheses each time it is stated (l5 screens[7], l7 screens[2], l7 summary, homework-2 items[8] and [9]). Signed area and area are kept apart throughout (l3, l7 quiz, l8, review-2). Improper integrals are defined as limits and the p-test is right at the boundary (l11). "No elementary formula" is the wording used in the body text wherever the claim is made (l5 quiz, l9 screens[5], l12 screens[0] and [8], review-2, homework-2, homework-3); only the l12 title shortens it to "no formula", which screen 0 corrects at once. The trapezium error order $h^2$ carries its smoothness condition (l12 screens[6]) and the script confirms the factors 4 and 9 on three integrands. Density and expectation items were also checked by Monte Carlo with 4 million draws.

No `wrong[]` value lies inside its key's tolerance (162 single-key numeric widgets in the lessons, reviews, homework and problems; mechanical scan in the script). No wrong option is correct under an alternative valid method.

## Findings

1. problems-3.json | `items[2].parts[0].feedback.byKey.sign` | wrong, minor | The line says "ln 0.5 is −0.34657 and ln 1.5 is 0.20273". Those are the halves. | $\ln 0.5 = -0.69315$ and $\ln 1.5 = 0.40547$ (script check fails). The halved values are what the trapezium bracket holds, as the part's own explanation shows. The conclusion of the line is right; the two stated values are false. | Replace the line with: `Half of ln 0.5 is −0.34657 and half of ln 1.5 is 0.20273, so the negative end outweighs. A positive 0.0719 takes 0.34657 − 0.20273, the wrong way round.`

2. review-3.json | `items[8].widget.accept` with `items[8].widget.tol` | wrong, minor | The accepted-answer line reads "£0.63, exactly 0.625", and the correct feedback says "About £0.63". The tolerance is 0.001 around 0.625, so 0.63 is marked wrong. The question states no precision, and every other money answer in the level is in pence. | `within()` in `app/js/engine/grade.js`: $|0.63 - 0.625| = 0.005 > 0.001$ (script check fails). The line states as accepted a form the grader rejects. | Set `"tol": {"abs": 0.006}`. The slips 0, 2.5 and 12.5 stay outside it. Keep the accept text.

3. l13-average-as-integral.json | `screens[8].explain.text` | misleading, serious | "Fatter tails, as in the uniform model, make the option worth more." The uniform is not the fatter-tailed shape, and tail shape is not why the call is worth more. | Kurtosis: uniform 1.8, triangle 2.4 (Monte Carlo in the script; exact values $\tfrac95$ and $\tfrac{12}{5}$). The uniform is the thinner-tailed of the two in the standard sense. The call is worth more because the uniform on the same range has the wider spread: standard deviation 5.77 against 4.08. For a symmetric density an at-the-money call is worth $\tfrac12 E|X - 100|$, a measure of spread. At equal standard deviation the script prices the uniform at 1.767 and the triangle at 1.667, so the thinner-tailed shape is still worth more. A learner would carry "fat tails" away as a name for wide spread, and the rule "fatter tails raise the at-the-money option" away as general. Both are wrong habits for an options desk. | Replace the last two sentences with: `The triangle moves weight from the far prices to the middle, where the call pays little. The wider spread of the uniform model makes the option worth more.`

4. l13-average-as-integral.json | `screens[5].explain.text` and `summary.ideas[2]` | imprecise, minor | "For a bent payoff, $E[g(X)]$ and $g(E[X])$ differ" and "which is not $g(E[X])$" are stated without condition. They are equal whenever $g$ is a straight line on the range of $X$. | Counter-example in the script: a call struck at £80 with $X$ uniform on [£90, £110] has $E[(X - 80)^+] = 20 = (E[X] - 80)^+$. Jensen's inequality is strict only when the bend lies inside the support (Casella and Berger 4.7.7). problems-3 already writes "differ in general". | screens[5] last sentence: `When the payoff bends inside the range of prices, $E[g(X)]$ and $g(E[X])$ differ.` summary.ideas[2]: `An expected payoff is $E[g(X)] = \int g(x)\,f(x)\,dx$, which in general is not $g(E[X])$.`

5. problems-3.json | `items[1].parts[4].widget.options[1].why` | imprecise, minor | "No one wait gives $E[g(X)]$ for a curved $g$." One wait always does, by the intermediate value theorem. What fails is any fixed summary of the waits. | Here $100e^{-x^*} = 25$ at $x^* = \ln 4 \approx 1.386$ minutes (script). The option is still wrong: the median wait solves $(m + 1)e^{-m} = \tfrac12$, $m \approx 1.678$, and gives £18.67. | Replace the why with: `You swapped the mean for another single wait. The median wait, about 1.68 minutes, gives £18.67, not £25. For a curved $g$ you need the whole density.`

6. l10-undo-product.json | `quiz[1].widget.options[1].why`; `screens[3].widget.options[0].why`; `screens[3].feedback.byKey.a` | imprecise, minor | The other split is called "harder than the old one" and "harder than the integral you began with". For $x^3\ln x$ it brings back three times the same integral and solves. For $x\ln x$ the needed $v = \int \ln x\,dx$ is not a harder integral; it needs parts itself. | With $u = x^3$, $v = x\ln x - x$: $\int v\,du = 3\int x^3\ln x\,dx - 3\int x^3\,dx$ (sympy check in the script). homework-3 items[9] says of the same split "solving for it works but takes longer". The choice of $u = \ln x$ is still the right key. | quiz[1] options[1].why: `Then $v = \int \ln x\,dx = x\ln x - x$, and the new integral brings back $x^3\ln x$ three times over. It can be solved, but it takes far longer.` screens[3] options[0].why: `With $u = x$ you need $v = \int \ln x\,dx$ before you can start. That integral needs parts itself.` screens[3] feedback.byKey.a: `You chose $u = x$. Then $v$ is $\int \ln x\,dx$, which needs parts itself before you can start.`

7. l4-accumulating-a-rate.json | `screens[6].widget.options[2].why` and `summary.ideas[2]` | imprecise, minor | "There $A$ stops climbing: it is at a peak or a dip" and "peaks where the rate crosses zero" drop the direction of the crossing. | A rate that touches zero without changing sign, $r = (T - 1)^2$, gives neither. A crossing from below gives a low: review-1 items[8] has exactly that, with the low at the crossing. l5's summary states the direction ("from positive to negative"). | options[2].why: `There $A$ is flat for an instant, not climbing. Often it is at a peak or a dip.` summary.ideas[2]: `The running total climbs fastest where the rate is largest and peaks where the rate crosses zero from above.`

8. l4-accumulating-a-rate.json | `screens[8].hints[1].text` and `hints[2].text` | imprecise, minor | Hint 2 tells the learner to form $60 \times 1{,}232.88$; hint 3 then prints £73,972.60. The printed product is £73,972.80. | $60 \times 1232.88 = 73{,}972.80$; the £73,972.60 comes from the unrounded rate $\tfrac{450{,}000}{365}$. Likewise $30 \times 1095.89 = 32{,}876.70$ against the printed £32,876.71. The key and tolerance (£1) are fine. | hints[1].text: `Use the unrounded daily rates: $30 \times \tfrac{400{,}000}{365}$ and $60 \times \tfrac{450{,}000}{365}$.`

9. l10-undo-product.json | `screens[9].explain.text` | imprecise, minor | "At 2 it is $-4400e^{-0.1} \approx -3981.28$; at 0 it is $-4000$. The difference is about 18.715." From the printed figures the difference is 18.72. | $-4400e^{-0.1} = -3981.2846$; $4000 - 3981.28 = 18.72$, $4000 - 3981.285 = 18.715$. | Print `\approx -3981.285` in place of `\approx -3981.28`.

10. homework-3.json | `items[4].feedback.byKey.test-3` (with `test-8`) | imprecise, minor | The test-8 line names the mistake "compare with the estimate before". Only the codings that return the coarser $n$ reach test 8. The equally natural coding that returns the finer $n$ fails test 3 first with 128, and is told "Stop only when the error is below tol", although it stops too late. | Sweep under the page's Pyodide: coarser-$n$ coding fails test 8; finer-$n$ coding fails test 3 (returns 128, expected 64); the $|T_{2n} - T_n|/3$ coding fails test 4. Moving test 8 forward does not help: the finer-$n$ coding passes test 8. The test-3 line is true of its test, so only its advice needs widening. | test-3: `Test 3 expects 64: the error is 0.000163 at $n = 32$ and 0.000041 at $n = 64$. Return the first $n$ whose own error against exact is below tol, neither the one before nor the one after.` (Keep the code formatting of `exact` and `tol` as in the file.)

11. l9-undo-chain.json | `screens[7].prose` | imprecise, minor | The substitution rule with new limits is derived and stated with no hypotheses. | It needs $g'$ continuous on $[a, b]$ and $f$ continuous on the values $g$ takes (Stewart 5.5 theorem 6; Spivak ch. 19 theorem 2). The derivation's own lines use both: line 1 needs $f$ to have an antiderivative, line 3 applies the fundamental theorem to $f(g(x))\,g'(x)$. l7 and homework-3 items[9] state such conditions; this screen does not. | Replace the last sentence of the prose with: `Here $u = g(x)$ is the inside. Take $g'$ continuous on $[a, b]$ and $f$ continuous on the values $g$ takes.`

Counts: wrong 2 (both minor), imprecise 8 (all minor), misleading 1 (serious). Serious 1, minor 10.

## Code widgets

All three Python widgets were swept through `app/tools/code-runner.mjs` (the page's harness and worker grader, Pyodide 0.27.7, wasm32). `grade-all.mjs --code` on the three: solutions pass, starters fail, every listed mutant fails its named test first. No line is timing dependent.

| widget | byKey line | codings submitted (first failing test) | verdict |
|---|---|---|---|
| l12 screens[3] `trapezium` | test-1 "exactly $n$ strips" | `range(n - 1)` (1), `range(n + 1)` (1), `range(1, n)` (1) | correct |
| | test-3 "with `n = 1` the loop must still run once" | points form returning 0 when `n == 1` (3); loop to `n - 1` plus last strip only if `n > 1` (3) | correct |
| | test-6 "build each edge from `a`" | `left = i * h` (6); points list from 0 (6); `h = b / n` (5, no line: generic) | correct |
| | error | a `NameError` inside the function reports as test-1, not `error`; `error` is the load stage only. The line is true of that stage | correct |
| l12 screens[8] `phi`, `prob_within` | test-1 "check the square root and the $2\pi$" | no square root (1); `sqrt(2) * pi` (1); `sqrt(pi)` (1) | correct |
| | test-4 "from `-z` to `z`, pass `phi` itself" | `trapezium(phi, 0, z, n)` (4); `phi(z)` passed (4); limits `z, -z` (4); `2 * trapezium(phi, 0, z, n)` (4: right mathematics on a different grid, the line tells the learner what the test wants) | correct |
| homework-3 items[4] `n_needed` | test-1 "exactly `n` strips of width `h`" | `range(n - 1)` (1); `h = (b - a) / (n + 1)` (1) | correct |
| | test-4 "start at `n = 1`, test before doubling" | start at 2 (4); double before testing (4) | correct |
| | test-3 "stop only when the error is below `tol`" | return `n // 2` (3); halve the error before comparing (3); relative error (3); `n += 1` search (3); successive estimates returning the finer `n` (3, misdescribed) | finding 10 |
| | test-8 "compare with `exact`, not the estimate before" | coarser-`n` while loop (8); finer-`n` (3); $|T_{2n} - T_n|/3$ returning $2n$ (4) | finding 10 |

Wrong programs against the hidden tests: left Riemann, midpoint and un-halved sums fail l12 test 1; a `prob_within` that ignores `n` fails test 6; a closed-form `erf` fails test 4; signed error without `abs` fails homework-3 test 6. One program passes that differs from the stated rule only at exact equality (`> tol` in place of `>= tol`); no test sits on the boundary and no learner would be misled, so it is not a finding.

## Runs

- Validator (`cd app && node tools/validate.mjs`): 0 errors, 4,616 warnings.
- Number scripts (`node tools/run-number-scripts.mjs --only integrals`, venv Python first on PATH): 5 of 436 scripts, 5 passed, 0 new failures.
- `node tools/grade-all.mjs --file <each of the 26 files> --code --local-cdn <pkgs>`: 409 widgets and 16 fluency templates checked, 3 Python code widgets run, 0 failures.
- `docs/reports/integrals-L1-3-concepts-r2.py`: 71 checks, 2 failing (findings 1 and 2), exit 1. It exits 0 once those two are fixed.
- No playthrough, as the common rules set.

## Overlap with earlier reads

Read only after the ledger and the findings above were written: `docs/reviews/audit-integrals-1-3.md` (round 1, with its addendum and fix pass), its ledger, `review-1.3.md` (integrals sections), `review-problems-1.3-a.md`, `review-delta-problems-1.3-ab.md` and `review-perf-retrofit-10.md` (the three integrals derivation items). Conceptual findings only; voice, rendering and freshness notes are not counted.

| | count | which |
|---|---|---|
| this audit only | 10 | findings 1, 2, 3, 4, 5, 6, 7, 9, 10, 11 |
| earlier reads only | 18 | round 1 findings 1 to 6 and 8 to 14 (13), and the five conceptual findings of the older reviews that round 1 lists. All are fixed in the text read here, and I confirmed each fixed wording in the blind read, so none could be found again |
| both | 1 | finding 8: round 1 finding 7 found the printed products of rounded figures on l4 `screens[8]`. Its fix pass rewrote the explanation; the same two products remain across `hints[1]` and `hints[2]` |

Notes on the "this audit only" row:

- Finding 6 (the other split called "harder") was seen by round 1 and passed as "fair wording" in its notes; `review-perf-retrofit-10.md` IN3-2 fixed the same claim in the homework-3 model. I keep it as an `imprecise`, since the level now says two different things about one split.
- Finding 10: the round 1 fix pass (item 9) records that the finer-$n$ coding first fails test 3, but left the test-3 line as it was.
- Findings 1 and 2 are rows that round 1's ledger marks `correct`. Finding 1's line was added by the commit "negative-key pass part 2", before round 1's commit. Finding 2 is of the class that `review-delta-problems-1.3-ab.md` finding 1 raised in the problems files; this instance is in review-3.

New `wrong` that no earlier read found: 2 (findings 1 and 2, both minor) over three levels. The convergence rule allows at most one, so the course does not close on this round. A fix-pass read was not found in the round 1 file.

## Engine note sent to the inbox

One bullet under "Raised later (audit integrals):" in `docs/BACKLOG-INBOX.md`: a numeric `accept` line that prints a form its own `tol` refuses (finding 2), with a proposed `grade-all.mjs` check.

## Fix pass

Opus fixer, from commit `9228cd2d`. Each basis is my own recomputation (venv Python: scipy, a closed form or a sweep under the page's Pyodide), not the auditor's text.

1. fixed. $\ln 0.5 = -0.693147$, $\ln 1.5 = 0.405465$; halves $-0.346574$ and $0.202733$; $0.5 \times (0.34657 - 0.20273) = 0.07192$. The line now says "Half of ln 0.5 ... half of ln 1.5" and "comes from 0.5 × (0.34657 − 0.20273)"; the slip value 0.0719 is unchanged.
2. fixed differently. The question states no precision and 0.625 is exact, so 0.63 is not a correct answer to a stated precision; tolerance not widened. The question now says "Give 3 decimal places." (as items[0], [3] and [4] of the set do), the accept line prints "£0.625 exactly" and the correct feedback "£0.625". Key 0.625 and tol 0.001 unchanged: $\tfrac{1}{20}\int_{105}^{110}(x - 105)\,dx = 0.625$ by quad and by hand ($12.5/20$). Concepts-r2 check re-pointed: it read "£0.63" from the old accept text and now reads the figure the accept line prints.
3. fixed (own wording). Kurtosis uniform 1.8, symmetric triangle 2.4 (scipy); sd 5.774 against 4.082; calls 2.5 and 5/3. Last two sentences now: "The triangle moves weight from the far prices to the middle, where the call pays little. The uniform model spreads prices wider, so its option is worth more."
4. fixed differently on screens[5]. The proposed "When the payoff bends inside the range, they differ" is itself too broad: $g(x) = (x - 100)^3$ bends inside $[90, 110]$ yet $E[g(X)] = g(E[X]) = 0$ for the symmetric uniform. Now: "Because this payoff bends inside the range of prices, ..." (true for this convex call with its kink at 100 inside the support, strict Jensen). summary.ideas[2]: "which in general is not $g(E[X])$", as proposed. Counter-example confirmed: strike 80 on $U[90, 110]$ gives 20 both ways.
5. fixed (own wording). Median of Gamma(2, 1) solves $(1 + m)e^{-m} = \tfrac12$: $m = 1.67835$ (brentq and `stats.gamma(2).median()`), $100e^{-m} = 18.668$; the wait $\ln 4$ gives 25 exactly. why: "The median, about 1.68 minutes, gives about £18.67, not £25. The one wait that gives £25 can only be found from $E[g(X)]$, so the whole density is needed."
6. fixed. Parts with $u = x^3$, $v = x\ln x - x$: $I = x^4\ln x - x^4 - 3I + \tfrac34 x^4$, so $4I = x^4\ln x - \tfrac14 x^4$, the same as $u = \ln x$ gives. quiz[1] options[1].why ends "It can be solved, but it takes longer" (homework-3's wording, not "far longer"); screens[3] options[0].why and feedback.byKey.a as proposed. Also screens[3] options[2].why ("without a harder integral" to "without a second use of parts"), the same claim in a fourth place.
7. fixed. $r = (T - 1)^2 \ge 0$ gives $A$ increasing with no extremum at $T = 1$; a sign change from negative to positive gives a minimum. options[2].why as proposed; summary.ideas[2] says "crosses zero from positive to negative" (l5's own phrase) in place of "from above". screens[5] feedback.correct ("The P&L peaks where the rate crosses zero") left: it describes that screen's rate, which falls through zero.
8. fixed. $30 \times 400{,}000/365 = 32{,}876.712$, $60 \times 450{,}000/365 = 73{,}972.603$, matching hint 3 and the key 106,849.32; the rounded products are 32,876.70 and 73,972.80. hints[1] now uses the unrounded daily rates. Key and tol unchanged.
9. fixed. $-4400e^{-0.1} = -3981.28464$ and $\int_0^2 10t\,e^{-0.05t}\,dt = 18.71536$ by quad; the explain prints $-3981.285$.
10. fixed. Error $1/(6n^2)$: $1.628 \times 10^{-4}$ at 32, $4.07 \times 10^{-5}$ at 64. test-3 line as proposed. Codings of its mistake under the page's Pyodide (`code-runner.mjs`), first failing test: `return n // 2` (3), keep the last $n$ still above tol (3), double after the check passes (3), successive estimates returning the finer $n$ (3); solution passes. Three added to `mutants` with `test: 3` (`n // 2`, double after, finer $n$). No test, key or solution changed.
11. fixed. Stewart 5.5 theorem 6: $g'$ continuous on $[a, b]$ and $f$ continuous on the range of $g$; the order lines use both (F exists by the FTC part 1 for continuous $f$; FTC part 2 needs $f(g(x))g'(x)$ continuous). Sentence added to the prose as proposed.

Gates: validator 0 errors; voice-scan 35 on the seven files 0 and 0; `integrals-L1-3-concepts-r2.py` 71 checks, 0 failing, exit 0; `integrals-L1-3-concepts.py` 360 pass, 0 fail; the three test-line sweeps exit 0 with the keys recorded above; number scripts (integrals) 5 of 5 pass; `grade-all.mjs --code --file` on the seven files 0 failures; playthrough of l4, l9, l10, l13, review-3, homework-3 and problems-3 green desktop and `--mobile`.
