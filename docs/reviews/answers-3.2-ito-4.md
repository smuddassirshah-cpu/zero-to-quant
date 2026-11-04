# Answer check, topic 3.2 ito level 4 (4 November 2026)

Independent recomputation of every keyed answer, stated number, feedback value, code test and rubric point in `app/content/courses/ito/` `l13-martingale-or-not.json`, `l14-hitting-and-exit.json`, `l15-moments-quickly.json`, `l16-pricing-in-a-minute.json`, `l17-derivation-aloud.json`, `review-4.json` and `homework-4.json`. Each value was worked from the question text; the file explanations were used only as the thing to compare against, and `docs/reports/ito-4.md` was not read. Scripts are in the scratchpad folder `ac-ito4` (`/tmp/claude-0/-home-user-zero-to-quant/5858d7c4-7372-5116-9f86-cb52e41f112f/scratchpad/ac-ito4/`):

- `calc4.py`, `calc5.py`: CPython with NumPy, SciPy and SymPy (installed to `pylib`). SymPy drifts $f_t + \tfrac12 f_{xx}$ for every process of lesson 13, closed forms for the exit probability and time (with Wald), the moment and isometry integrals by `scipy.integrate.quad` and `dblquad`, the digital, forward, power, put and Black-Scholes terms, and every `wrong` value.
- `code.py`: runs every code widget (7 widgets, 52 hidden tests, 11 examples). The solution is exec'd with the widget `prelude`, each `call` is evaluated, and `isclose` and `equal` are applied to lists elementwise. The starter is run the same way.
- `sim4.py`: the exit simulator of l14 and `homework-4` re-run on 300,000 paths, against the formula and against the shifted-barrier formula (barriers moved by $0.5826\,\sigma\sqrt{\Delta t}$). `walk4.mjs`: the engine's seeded `walk` generator (copied from `canvas/walk.js` and `sim.js`) for the hit counts on the l14 canvases.
- `expr4.mjs`: the real `app/js/engine/grade.js` `exprEqual` with the Compute Engine, run on the three expression keys with 7, 11 and 11 equivalent forms (`\exp`, a letter before a bracket, `\frac12`, `*`, `\cdot`, reordered terms, factored forms) and 5, 5 and 5 wrong forms.
- `scan.py`: for every numeric field whether a wrong value sits inside the answer's tolerance or another wrong value's, whether each `byKey` key names a `wrong` id, cell or option and each `wrong` id has a line, for every choice the correct count and option lengths, for every order that `answer` plus `distractors` equal the line ids and whether `same` is set. `count4.py`: widget count. `dups.py`: for every keyed or wrong number of 4 or more digits, the course, exam and bank files outside this level that contain it (1,655 files), then read by hand. `fresh4.py`: replacement numbers proposed below, with a grep of `courses`, `exams` and `bank` for each.

**Summary.** All 91 widgets recompute: 74 numeric fields (50 numeric items and 24 numeric table cells, with 125 `wrong` values in all), 4 text cells, 1 slider, 14 choice, 6 order, 3 expression, 1 tap-regions, 7 code (52 hidden tests, 11 examples) and 1 longform rubric (7 lines, 2 + 2 + 2 + 1 + 1 + 1 + 1 = 10 points). No keyed answer is wrong and no tolerance is mis-set: no `wrong` value falls inside any answer's tolerance or another wrong value's. Every choice has exactly one correct option and no distractor is also correct; the longest key against the longest distractor is 1.13 (l17 `screens[9]`), so no choice key is visibly longer. Every code solution passes every test and example (CPython with NumPy, every seeded value reproduces to the stated digits, the three statistical `equal` tests are True) and every starter fails the tests (all return `None`). The three expression keys grade every equivalent form as right and every wrong form as wrong, including `\exp`, `s(2s+t)` and `S_0^n e^{...}` with a letter before the bracket. The seeded canvases agree (l14 `screens[0]`: 128 of 190 exits are upward, 0.674 against 2/3). Every `pace` is plausible; the one `timed` is 75 seconds under the sum of the paces. No literal backslash-n sits in any prose field (the only `\n` text is `\neq` in l13, l16 and l17), and no exclamation mark or dash other than factorials. There are 2 errors, 13 warnings and 17 notes. The worst is a feedback line in l14 `screens[7]` that tells the learner to compute $(1 - e)/(e^{-1} - e)$, which is the answer to the previous screen, for a problem whose exponent is $e^2$. No key changes.

## Mismatches

1. **Error.** `l14-hitting-and-exit.json` `screens[7]` (the $a = 1$, $b = 2$ exit), `feedback.generic` and `feedback.byKey.r0c1` use the wrong exponent. Here $2\mu b = 2 \times 0.5 \times 2 = 2$, so the numerator is $1 - e^2$. The generic line reads "$P = (1 - e^{1})/(e^{-1} - e^{1})$", which is the $b = 1$ value 0.7311, and `r0c1` says "With $b = 2$ it is $e^{2\mu b} = e$, so $P = 0.9100$". The key 0.91 and the hint ($e^2 = 7.3891$) are right. Fix `generic`: "Not quite right. $P = (1 - e^{2})/(e^{-1} - e^{2})$, then $E[\\tau] = (aP - b(1 - P))/\\mu$." Fix `r0c1`: "$P = (1 - e)/(e^{-1} - e) = 0.7311$ is for $b = 1$. With $b = 2$ the exponent is $2\\mu b = 2$, so $P = (1 - e^2)/(e^{-1} - e^2) = 6.3891/7.0210 = 0.9100$."
2. **Error.** `homework-4.json` `items[0]` (`h-stopping`), `"same": [["o3", "o4"]]` and the prose sentence "The last two correct lines may swap". Line `o4` ends "$E[\\tau] = E[W_\\tau^2] = Pa^2 + (1 - P)b^2 = ab$", and the step to $ab$ needs $P = b/(a + b)$, which only `o3` states. The order `o1, o2, o4, o3` is therefore marked right although `o4` uses a chance not yet derived. The other direction is also fixed: `o3` needs `o2` (its "bounded convergence" needs $\tau$ finite). Fix: delete `same` and the sentence in `prose`, so the key is the chain `o1, o2, o3, o4`.
3. **Warning.** `l15-moments-quickly.json` `quiz[3]` (`q-ito`), `wrong` id `one`, value 1, feedback "You used $E[W_t^2] = 1$. At time $t$ the variance is $t$". With $E[W_t^2] = 1$ the integral is $\int_0^2 1\,dt = 2$, which is the key, so the slip named cannot give 1. The value 1 is $\tfrac12\int_0^2 t\,dt$. Fix: change the value to 2.6667 (tolerance abs 0.0005) and the line to "You used $E[W_t^2] = t^2$, giving $\\int_0^2 t^2\\,dt = 8/3$. The variance of $W_t$ is $t$, so square the integrand's size, not the time." 2.6667 is clear of 4 and of the key.
4. **Warning.** `homework-4.json` `items[3]` (`h-hermite`), `parts[1]`, `wrong` id `half`, value 7.5, feedback "You solved $3a + b = 0$ and halved". Solving $3a + b = 0$ gives $b = 30$, and halving gives 15, the key. The value 7.5 solves $\tfrac32a + 2b = 0$ (the $\tfrac12 f_{xx}$ term of $a\,tx^3$ halved again). Fix the line: "You halved the $\\tfrac12f_{xx}$ term of $a\\,tx^3$ a second time, solving $\\tfrac32a + 2b = 0$. That term is already $3atx$, so $2b = 30$."
5. **Warning.** `l14-hitting-and-exit.json` `screens[4]` (`P` expression), `byKey.flipped`: "That is the probability of reaching $-b$ first with the drift reversed". The wrong form is $P(-\mu)$, the chance of reaching $+a$ first when the drift is reversed: at $\mu = 0.5$, $a = 1$, $b = 2$ it is 0.3348, and the chance of $-b$ first with the reversed drift is 0.6652. Fix: "You flipped the sign of $\\mu$ throughout. That is the chance of reaching $+a$ first when the drift is reversed (0.3348 for $\\mu = 0.5$, $a = 1$, $b = 2$)."
6. **Warning.** `l14-hitting-and-exit.json` `screens[4]` `explain.text`: "The curve is flat near $\mu = 0$ at $b/(a + b)$, and a small positive drift lifts it fast." The two halves contradict each other, and the curve is not flat: for $a = 1$, $b = 2$ the slope at $\mu = 0$ is $ab/(a + b) = 2/3$ (0.6667 by central difference), and $P(0.1) = 0.7307$. Fix: "The curve crosses $\\mu = 0$ at $b/(a + b)$ with slope $ab/(a + b)$ (2/3 here): a small positive drift lifts it at once."
7. **Warning.** `l15-moments-quickly.json` `screens[6]`, `byKey.drop-cross` (value $s^2 + st$): "missing one $s^2$. $E[W_s^4] = 3s^2$, not $s^2$". With $E[W_s^4] = s^2$ the total would be $s^2 + s(t - s) = st$, which is the `independent` wrong form. The form $s^2 + st$ comes from $E[W_s^4] = 2s^2$, or from $E[W_s^2]E[W_t^2] + \text{Cov}^2$ with the covariance counted once. Fix: "You gave $s^2 + st$, missing one $s^2$. That follows from $E[W_s^4] = 2s^2$; the fourth moment of a normal is $3s^2$."
8. **Warning.** `l14-hitting-and-exit.json` `screens[9]`, `byKey.swapped` (value 0.5714): "the near distance over the total". Here $a = 2$ is the far barrier (the take-profit) and $b = 1.5$ the near one, so $a/(a + b)$ is the far distance over the total, and 0.5714 is the chance of the stop-loss first. Fix: "You used $a/(a + b) = 0.5714$, the far distance over the total. That is the chance of the stop-loss first."
9. **Warning.** `homework-4.json` `items[1]` (`h-exit-report`), `explain.text`: "the chance gap is within noise". On seed 7 the chance gap is 0.0200 against a standard error of 0.0077 (2.6 standard errors, outside noise), and the discretisation bias is real: 300,000 paths give 0.5932 against the formula's 0.5808, a gap of +0.012. Test 2 (seed 3) has a gap of 1.7 standard errors, which is why the hidden test asks for three. Fix: "The gap shrinks as $\\Delta t$ does. The chance gap is smaller (about +0.012 on a long run at $\\Delta t = 0.01$) and sits within about three standard errors at 4,000 paths."
10. **Warning.** `review-4.json` `items[6]` (`r-dig110`) repeats the pdes level 3 quiz item `pdes/l11-feynman-kac.json` `q-digital`: same market ($S = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$), same strike 110, same $d_2 = -0.3266$, $\Phi(d_2) = 0.3720$, same wrong value 0.372 (the no-discount slip), same answer 0.354 (0.3539). DECISIONS "Duplicates (6 Nov)". Fix: a fresh contract, for example $S = 60$, $K = 64$, $r = 4\%$, $\sigma = 30\%$, $T = 2$: $d_2 = (\ln(60/64) + (0.04 - 0.045) \times 2)/(0.3\sqrt2) = -0.1757$, $\Phi(d_2) = 0.4303$, price $e^{-0.08} \times 0.4303 = 0.3972$ (`no-discount` 0.4303, `d1` $e^{-0.08}\Phi(0.2486) = 0.5522$). None of 0.3972, 0.4303 or 0.5522 is in any course, exam or bank file (`fresh4.py`, grep).
11. **Warning.** `review-4.json` `items[6]` and `items[7]` repeat lesson numbers of the same course (DECISIONS "Fresh numbers in reviews and homework"). `r-dig110` is the strike-110 digital of `l16` `screens[8]` test 1 (0.3539) and `r-sqrt` ($\sqrt{S_T}$, 9.7045) is `l16` `screens[8]` test 3 (`power_price(100, 0.05, 0.2, 1, 0.5)`), in the same market. Fix for `r-sqrt` (a fresh answer; $S = 100$, $r = 4\%$, $\sigma = 30\%$, $T = 2$): price $10e^{-0.08 + 0.5(0.04 - 0.045) \times 2 + 0.125 \times 0.09 \times 2} = 10e^{-0.0625} = 9.3941$; `jensen` $e^{-0.08}\sqrt{100e^{0.08}} = 9.6079$; `no-discount` $10e^{0.0175} = 10.1765$. The convexity line in `explain` becomes $\tfrac12n(n - 1)\sigma^2T = -0.0225$ (here $\tfrac12 \times \tfrac12 \times (-\tfrac12) \times 0.09 \times 2$). No file holds 9.3941 or 10.1765.
12. **Warning.** `l16-pricing-in-a-minute.json` `screens[4]` repeats `review-3.json` `items` `r-power` of the same course: same market, same claim $S_T^2$, same answer 10,941.74 and the same wrong value 11,502.74 (no discount). The newer item takes fresh numbers. Fix: $S_0 = 80$, $r = 4\%$, $\sigma = 25\%$, $T = 1.5$: price $6400e^{(0.04 + 0.0625) \times 1.5} = 6400e^{0.15375} = 7463.68$; `jensen` $6400e^{0.06} = 6795.75$; `no-discount` $6400e^{0.21375} = 7925.20$; `spot` 6400. The convexity factor in `explain` is $e^{\sigma^2T} = e^{0.09375} = 1.0983$. (Avoid $S_0 = 50$, $T = 2$: its Jensen value 2654.59 is the `l16` test value for $S = 50$, $T = 0.5$.)
13. **Warning.** `l16-pricing-in-a-minute.json` `screens[0]` and `screens[1]` repeat items of other levels. `screens[0]` (digital call at 100, 0.5323, wrong 0.5596) is the digital of `ito/l11-prices-as-expectations.json` (answer 0.5323, accept "$e^{-0.05}\Phi(0.15) = 0.951229 \times 0.559618$") and is quoted in `pdes/l10` and `pdes/l11`. `screens[1]` (forward at 100, 4.8771) is the answer of `pdes/l11-feynman-kac.json` (accept "$e^{-0.05}(105.1271 - 100)$, or $100 - 100e^{-0.05}$") and of `cpp-pricing/l12`. Fix: strike the digital at 105 in `screens[0]`, `screens[2]` and `screens[9]`: $d_2 = -0.0940$, $Q$-chance 0.4626 (`no-discount`), call 0.4400, put 0.5112, pair 0.9512; `real-drift` ($\mu = 12\%$, $\Phi(0.2561)$ discounted) 0.5717; the junior's pair becomes 0.4400 and 0.5600 (sum 1.0000), still 0.0488 short. Strike the forward at 90 in `screens[1]`: $Ke^{-rT} = 85.6106$, value $100 - 85.6106 = 14.3894$ (`free`, `forward-price` 105.1271 and `simple` 5 stay). No item repeats 14.3894, 0.4400 or 0.5112 with these inputs (the digits occur only in unrelated ensembles, backtest and conditional files). Update the `explain` and `feedback` lines that quote 0.5323, 0.4189 and 0.5596.
14. **Warning.** `l17-derivation-aloud.json` `screens[6]` repeats `l9-bs-pde.json` `screens[1]`: the same option and the same four terms ($\Theta = -6.4140$, $rS\Delta = 3.1842$, $\tfrac12\sigma^2S^2\Gamma = 3.7524$, $rV = 0.5225$, sum 0), also the model answer of `homework-3`. Fix: a new market, for example $S = 90$, $K = 100$, $r = 3\%$, $\sigma = 30\%$, $T = 1$: $V = 7.9761$, $\Delta = 0.4597$, $\Gamma = 0.014700$, $\varphi(d_1) = 0.396905$, $\Phi(d_2) = 0.344136$, and the terms $\Theta = -6.3601$, $rS\Delta = 1.2412$, $\tfrac12\sigma^2S^2\Gamma = 5.3582$, $rV = 0.2393$, sum 0 (recomputed; no file holds -6.3601 or 5.3582). Update the prose inputs, the hints, the `byKey` lines (for $\Theta$: $-5.3582 - 1.0019$), `feedback.correct` ("$-6.3601 + 1.2412 + 5.3582 - 0.2393 = 0.0000$ from rounded terms") and the `explain` and `bars` canvas labels.
15. **Warning.** `l13-martingale-or-not.json` repeats martingale items of level 2. `screens[4]` ($e^{3W_t + ct}$, $c = -4.5$) is the option $e^{3W_t - 4.5t}$ of `homework-2.json` `h-which-mart`, with the same explanation, and the rows $e^{2W_t - 2t}$ and $W_t^3 - 3tW_t$ of `screens[2]` are the key of `review-2.json` (`right`, $e^{2W_t - 2t}$) and an option of `homework-1.json`. Fix `screens[4]`: take $a = 5$, so $c = -12.5$ (wrong values `sign` 12.5, `no-square` -2.5, `no-half` -25; the table row "$e^{3x + ct}$" becomes "$e^{5x + ct}$", $f_x$ is $5f$, and the `explain` keeps the general $e^{aW_t - \tfrac12a^2t}$). Fix `screens[2]`: replace the row $e^{2W_t - 2t}$ with $e^{4W_t - 8t}$ (drift $-8f + \tfrac12 \times 16f = 0$, key still 0 and "yes"). `screens[3]` ($W_t^4 - 6tW_t^2 + 3t^2$) is also an option of `homework-2.json`, but it is the only quartic martingale, so only its framing can change: leave it, or ask for the constant in $W_t^4 - 6tW_t^2 + c\,t^2$ (drift $(2c - 6)t$, $c = 3$).
16. **Note.** `l14-hitting-and-exit.json` `screens[8]`, prose "with 5,000 paths the gap is about 0.02" and `explain` "Halving $\Delta t$ roughly halves the gap in $\sqrt{\Delta t}$ terms". On seed 1 the gap is 0.0212, one standard error (0.0107) under the long-run bias: 300,000 paths give $E[\tau] = 0.9548$, a gap of +0.0306 (the shifted barrier formula gives 0.956), and $P = 0.7350$ against 0.7311. The explanation is garbled: the gap scales as $\sqrt{\Delta t}$, so quartering $\Delta t$ halves it. Fix: "the long-run gap is about 0.03 (this seed shows 0.021, within one standard error)" and "The gap falls like $\\sqrt{\\Delta t}$: quartering the step halves it."
17. **Note.** `l14-hitting-and-exit.json` `screens[9]` `explain.text`: "costs of a few pence a trade can erase it". The edge is £0.1509 a trade, so a few pence leave most of it. Fix: "costs of about fifteen pence a trade erase it."
18. **Note.** `review-4.json` `timed`: `seconds` 600 against paces of 60, 60, 75, 90, 60, 90, 90, 90 and 60, a sum of 675. The clock does not lock (`lockAtZero` false) but starts 75 seconds short of the stated paces. Fix: `"seconds": 720` (or 675, or lower the three 90 paces to 75).
19. **Note.** Order lines with a free pair and no `same`, so a valid order is marked wrong (the ito-3 note 15 pattern). `l14` `screens[1]`: `a4` ($W^2 - t$ is a martingale too) can precede `a2` or `a3`; `same` cannot express a line that moves two places, so say in the prompt "Finish the chance before the time". `l15` `screens[1]`: `b1` and `b2` swap (the expansion needs only $D$, defined in the prose); fix `"same": [["b1", "b2"], ["b3", "b4"]]`.
20. **Note.** `l13-martingale-or-not.json` `screens[2]` (table): the `wrong` ids `no-half`, `no-ft` (cell `r0c1`) and `whole-fxx` (cell `r3c1`) have no `byKey` line, so a learner who makes exactly those slips gets `generic`, and the cell lines `r0c1` and `r3c1` (which name the slips) are never reached. Fix: add `no-half` "You used the whole $f_{xx} = 2$: $1 + 2 = 3$. Itô carries half of it.", `no-ft` "You left out $f_t = 1$.", `whole-fxx` "You left out the half: $f_{xx} = 12x^2 = 48$."
21. **Note.** `l13-martingale-or-not.json` `screens[5]`, `byKey.drift-only`: "$3W\,dt \times 2 = 6$". The drift at $W = 2$ is $3W = 6$ for one unit of time ($W_s$ stays at 2 in mean), not "$\times 2$". Fix: "You kept only the drift: $3W = 6$ over one unit of time. The forecast is today's 8 plus that 6." The line also describes the correct answer 14 as "8 plus 6"; say "so you gave the gain alone".
22. **Note.** `l13-martingale-or-not.json` `screens[8]` `explain.text`: "Central differences give $f_t + \tfrac12f_{xx}$ to about $10^{-6}$ here". The errors on the six tests are 1.4e-7, 1e-8, 2e-8, 1e-8, 5e-8 and 2e-8. Fix: "to about $10^{-7}$".
23. **Note.** `l16-pricing-in-a-minute.json` `screens[0]`, `wrong` id `real-drift`, value 0.6578 and the line "$\Phi(0.5) = 0.6915$, then discounted". $0.691462 \times 0.951229 = 0.65774$, so the value is 0.6577. The tolerance 0.0005 covers both. Fix: 0.6577.
24. **Note.** `l16-pricing-in-a-minute.json` `screens[8]` `feedback.correct`: "within 1.6 standard errors". $(10948.7709 - 10941.7428)/4.5605 = 1.54$. Fix: "within 1.5 standard errors".
25. **Note.** `l16-pricing-in-a-minute.json` `screens[9]` `explain.text`: "£48.80 on £1,000 of notional". $1000 \times 0.048771 = 48.77$ (48.80 comes from the rounded 0.0488). Fix: "£48.77".
26. **Note.** `l17-derivation-aloud.json` `quiz[1]` (`q-put`), `accept`/`feedback.correct`: "$0.5338 + 2.7518 - 3.9576 = -0.6721$". The sum of the rounded terms is $-0.6720$; the unrounded terms give $-0.67208$, and from the printed $V$, $\Delta$ and $\Gamma$ a learner gets $-0.6718$ (inside the tolerance 0.0005). Fix: "$= -0.6721$ from unrounded terms ($-0.6720$ from the rounded ones)".
27. **Note.** `l17-derivation-aloud.json` `screens[8]` canvas table, row "$S = 120$, $K = 105$, $\sigma = 30\%$": the test uses $r = 4\%$ and $T = 0.5$ too. Fix: "$S = 120$, $K = 105$, $r = 4\%$, $\sigma = 30\%$, $T = 0.5$".
28. **Note.** Displayed rounded terms reproduce the key to one unit in the fourth place, not exactly: `l14` `screens[5]` `r1c1`: $(0.7311 - 0.2689)/0.5 = 0.9244$ (key 0.9242); `l14` `screens[7]` `feedback.correct`: $(0.9100 - 2 \times 0.0900)/0.5 = 1.4600$ (key 1.4598; `byKey.r1c1` already says "from unrounded values"); `homework-4` `items[4]` `parts[1]`: $(1.2916 - 0.3473)/0.2 = 4.7215$ (key 4.7214, `explain` says $0.9443/0.2 = 4.7214$). All are inside the tolerance 0.0005. Fix: add "from unrounded values" to the two other lines.
29. **Note.** `homework-4.json` `items[4]` `parts[0]`, `wrong` id `no-drift`, value 0.625: it equals $b/(a + b) = 2.5/4$ and also the exponent $k = 2\mu/\sigma^2 = 0.625$ quoted in `generic`, so a learner who answers with $k$ meets the no-drift line. Fix: $\sigma = 0.7$ (then $k = 0.8163$, $P = 0.9046$, $E[\tau] = 5.5924$, `driftless` $ab/\sigma^2 = 7.6531$; `no-drift` 0.625 and `no-sigma` 0.792 (with $k = 2\mu = 0.4$) and 3.75 stay), and update the prose, the two `accept` lines and the `explain` text ($E[X_\tau] = 1.1185$).
30. **Note.** `l15-moments-quickly.json` `screens[3]` ($\operatorname{Var}\int_0^1 W_t\,dt = \tfrac13$) repeats the structure and the $T = 1$ value of `ito/homework-1.json` `h-var-integral-proof` ("At $T = 1$ that is $\tfrac13$") and of `ito/review-1.json` `r-var-integral` (the same variance at $T = 2$, 2.6667). Fix: take $T = 2.5$ in the prose, the canvas and the hints: $\int_0^{2.5} (2.5 - t)^2\,dt = 5.2083$; `isometry-dt` $\int_0^{2.5} t\,dt = 3.125$; `whole` 2.5 (the variance of $W_{2.5}$). $T = 1.5$ would make the `isometry-dt` slip equal the key (both 1.125), so avoid it. No file holds 5.2083.
31. **Note.** `review-4.json` `items[1]` (`r-expconst`, $e^{-2W_t + ct}$, $c = -2$) repeats the $a^2 = 4$ case of `review-2.json` (key $e^{2W_t - 2t}$) and the row of `l13` `screens[2]`. Fix: $e^{-3W_t + ct}$ ($c = -4.5$ repeats `l13` `screens[4]`), so use $e^{1.5W_t + ct}$: $c = -1.125$, wrong values $1.125$, $-0.75$, $-2.25$.
32. **Note.** Hidden-test and lesson numbers that coincide with other items, left for the author to judge: `l17` `screens[7]` (forward $S = 80$, $K = 90$, $r = 3\%$, half a year, $V = -8.6601$) is `l16` `screens[8]` test 0's third value; `l16` `screens[8]` test 6 (`[10.4534, 0.0465]`, seed 11, 100,000 draws) is the run of `l10`, `l11` and `homework-3`. A test inside a code widget is not shown as an item, so this is a note.

## Items checked

My value is the one I computed; "ok" means the key, every wrong value and the quoted explanation numbers reproduce to the stated precision (stated otherwise in the verdict).

| File | Screen or item | Key | My value | Verdict |
|---|---|---|---|---|
| l13 | screens[0] | slider 3, tol 0.15 (wrong 1.2 to 1.8, 5.7 to 6.0) | drift $(3 - c)x$ vanishes at c = 3; c = 1.5 halves $f_{xx}$ twice, c = 6 uses all of it | ok |
| l13 | screens[1] | order a1 to a5, drop x1, x2 | chain sound; x1 and x2 flawed | ok |
| l13 | screens[2] | table 2, 0, 0, 24 and no, yes, yes, no | 2, 0, 0, 24 (SymPy); wrong 3 (whole $f_{xx}$), 1, 48 | ok for keys; note 20 |
| l13 | screens[3] | 6 (wrong 12, 3) | drift $(6 - a)(x^2 + t)$, a = 6; $E[W^4] = 3t^2$ | ok; warning 15 |
| l13 | screens[4] | -4.5 (wrong 4.5, -1.5, -9) | $c + \tfrac12 \times 9 = 0$ | ok; warning 15 |
| l13 | screens[5] | 14 (wrong 8, 0, 6) | $E[(2 + Z)^3] = 14.0000$ by quadrature | ok; note 21 |
| l13 | screens[6] | choice `integral` | $d(tW - \int W) = t\,dW$; the others leave drift $W - t$, $W$ and $2W$ | ok |
| l13 | screens[7] | -1.5 (wrong -0.75, 1.5) | nonzero root of $0.75c + c^2/2$ is $-1.5$ | ok |
| l13 | screens[8] | code, 9 tests, 2 examples | drifts 6, 2, 0, 0, 0, 2 within 1.4e-7; seed 4: [0.9955, 0.0074] and [-0.0766, 0.0614]; $e^W$ test True | ok, starter fails; note 22 |
| l13 | screens[9] | 2.7183 (wrong 1, 7.3891, 0.3679) | $e = 2.71828$, $e^2 = 7.38906$, $e^{-1} = 0.36788$ | ok |
| l13 | quiz[0] | 11 (wrong 9, 2) | $9 + 2$ | ok |
| l13 | quiz[1] | 2 (wrong -2, 4) | $c - 2 = 0$ (SymPy) | ok |
| l13 | quiz[2] | 27 (wrong 9, 81) | $3t^2$ at 3 | ok |
| l13 | quiz[3] | choice `forecast` | $E[W_t^3 \mid W_s] = W_s^3 + 3(t - s)W_s$; no distractor correct | ok |
| l14 | screens[0] | choice `twothirds` | 2/3; engine seed 6: 128 up, 62 down of 190 exits (0.674) | ok |
| l14 | screens[1] | order a1 to a5, drop x1, x2 | $P = b/(a + b)$, $E[\tau] = ab$ | ok; note 19 |
| l14 | screens[2] | table 0.6, 6 | 3/5, 2 x 3 | ok |
| l14 | screens[3] | choice `infinite` | $E[\tau] = \infty$; others false | ok |
| l14 | screens[4] | expression $(1 - e^{2\mu b})/(e^{-2\mu a} - e^{2\mu b})$ | key right; 6 equivalent forms pass (`\exp`, reordered, `e^{2b\mu}`, multiplied through); 5 wrong forms fail | ok; warnings 5, 6 |
| l14 | screens[5] | table 0.7311, 0.9242 | 0.731059, 0.924234 | ok; note 28 |
| l14 | screens[6] | 1.5 (wrong 6, 3) | $6/4$ | ok |
| l14 | screens[7] | table 0.91, 1.4598 | 0.909969, 1.459817 | ok for keys; error 1; note 28 |
| l14 | screens[8] | code, 9 tests, 2 examples | formula cases 0.6/6, 0.6/1.5, 0.7311/0.9242, 0.91/1.4598, 0.2689/0.9242, 0.4251/0.9173; seed 1 [0.7464, 0.9454, 0.0062, 0.0107]; seed 2 [0.6683, 2.1916, 0.0074, 0.0309]; gap test True | ok, starter fails; note 16 |
| l14 | screens[9] | 0.4717 (wrong 0.4286, 0.5, 0.5714) | 0.471678; edge £0.1509; $\mu/\sigma \times \sqrt{252} = 0.79$ | ok; warning 8, note 17 |
| l14 | quiz[0] | 0.2 (wrong 0.8, 0.5) | 1/5 | ok |
| l14 | quiz[1] | 0.25 (wrong 1, 0.5, 4) | $1/4$ | ok |
| l14 | quiz[2] | 0.7788 (wrong 0.3679, 0.6065) | $e^{-0.25} = 0.778801$; $e^{-1}$; $e^{-0.5}$ | ok |
| l14 | quiz[3] | choice `inf` | infinite | ok |
| l15 | screens[0] | table 3, 15 | $24/8$, $720/48$ (quadrature 3.0000, 15.0000) | ok |
| l15 | screens[1] | order b1 to b5, `same` b3, b4 | $E[W_1^2W_2^2] = 4.0000$ by `dblquad` | ok; note 19 |
| l15 | screens[2] | 2.6667 (wrong 4, 2) | $8/3$ | ok |
| l15 | screens[3] | 0.3333 (wrong 0.5, 1) | $\int_0^1 (1 - t)^2 = 1/3$ | ok; note 30 |
| l15 | screens[4] | 9 (wrong 5, 11) | $2 + 3 + 2 \times 2$ | ok |
| l15 | screens[5] | 6 (wrong 0, 3) | $E[W_1W_2^3] = 6.0000$ by `dblquad` | ok |
| l15 | screens[6] | expression $2s^2 + st$ | 11 equivalent forms pass (`s(2s+t)`, `2*s^2+s*t`, `\left(...\right)`, `s\cdot t`); 5 wrong forms fail; 14 at (2, 3) by `dblquad` | ok; warning 7 |
| l15 | screens[7] | code, 10 tests, 2 examples | 12, 15, 5; 0s; 105, 120; 2.6667, 0.3333, 8, 3; seeds 5 and 3 [12.0189, 0.0876], [14.7659, 0.2134]; 3-se test True | ok, starter fails |
| l15 | screens[8] | table 120, 2, 5, 7.3891, 2.3333 | 120, 2, 5, 7.38906, 2.33333 | ok |
| l15 | quiz[0] | 75 (wrong 25, 15) | $3 \times 25$ | ok |
| l15 | quiz[1] | 0 (wrong 5.6569, 15) | $2^{2.5} = 5.65685$ | ok |
| l15 | quiz[2] | 12 (wrong 6, 36) | $4 \times 3$ | ok |
| l15 | quiz[3] | 2 (wrong 4, 1) | $\int_0^2 t\,dt = 2$ | ok for key; warning 3 |
| l16 | screens[0] | 0.5323 (wrong 0.5596, 0.6578, 0.5) | 0.532325; 0.559618; 0.65774 | ok; note 23, warning 13 |
| l16 | screens[1] | 4.8771 (wrong 0, 105.1271, 5) | 4.877058; 105.12711 | ok; warning 13 |
| l16 | screens[2] | 0.4189 (wrong 0.4404, 0.4677) | 0.418905; 0.440382; 0.467675 | ok |
| l16 | screens[3] | order p1 to p5, drop x1, x2 | exponent $2r + \sigma^2$, price $S_0^2e^{(r + \sigma^2)T}$ | ok |
| l16 | screens[4] | 10941.74 (wrong 10512.71, 11502.74, 10000) | 10941.7428; 10512.71; 11502.738; $e^{\sigma^2T} = 1.0408$ | ok; warning 12 |
| l16 | screens[5] | table 53.2325, 10.4506 | 53.23248, 10.45058; 63.68307; sums 116.9156 | ok (the call 10.4506 recaps l9 by design) |
| l16 | screens[6] | 0.9512 (wrong 1, 0.95, 1.0513) | $e^{-0.05} = 0.951229$ | ok |
| l16 | screens[7] | expression $S_0^ne^{n(r - \sigma^2/2)T + n^2\sigma^2T/2}$ | 11 equivalent forms pass (`\exp`, $\tfrac{n(n-1)}{2}$, $(S_0e^{rT})^ne^{...}$); 5 wrong forms fail (including the discounted form) | ok |
| l16 | screens[8] | code, 8 tests, 2 examples | forward 4.8771, 9.6332, -8.6601; digitals 0.5323, 0.3539, 0.6676; powers 100, 10941.7428, 1246076.7306, 9.7045, 2654.5914; seed 16 [10948.7709, 4.5605]; seed 11 [10.4534, 0.0465]; 3-se test True | ok, starter fails; notes 24, 32 |
| l16 | screens[9] | 0.0488 (wrong 0, 0.9512, 0.05) | 0.048771 | ok; note 25 |
| l16 | quiz[0] | 110.5171 (wrong 110, 105.1271) | 110.51709 | ok |
| l16 | quiz[1] | 4.4091 (wrong 4.6352, 4.3806) | 4.409110; 4.635170; 4.380573 | ok |
| l16 | quiz[2] | choice `fwd` | only the linear payoff is free of $\sigma$ | ok |
| l16 | quiz[3] | 1246076.73 (wrong 1105170.92, 1309964.45) | 1246076.7306; 1105170.918; 1309964.4507 | ok |
| l17 | screens[0] | tap l3, l4, l6 | silence, missing $\tfrac12\sigma^2S^2V_{SS}$, "earns $r$" with no reason; line numbers match the console | ok |
| l17 | screens[1] | order s1 to s5, drop x1, x2 | chain sound; the five minutes split as 1 + 2 + 1 + 1 | ok |
| l17 | screens[2] | choice `mine` | $\Phi(d_1) = 0.6368$ against $\Phi(d_2) = 0.5596$ | ok |
| l17 | screens[3] | choice `noise` | no noise, so any other return is arbitrage | ok |
| l17 | screens[4] | choice `cancel` | $-\mu SV_S + \Delta\mu S = 0$ at $\Delta = V_S$ | ok |
| l17 | screens[5] | choice `split` | $\sigma(t, S)$ keeps the argument; random $\sigma$ needs a second hedge | ok |
| l17 | screens[6] | table -6.4140, 3.1842, 3.7524, 0.5225, 0 | -6.41403, 3.18415, 3.75240, 0.52253, sum 2e-16; rounded sum 0.0001 | ok for keys; warning 14 |
| l17 | screens[7] | -2.6598 (wrong 2.6598, -2.7, 0) | -2.659802; $V = -8.660075$; residual 0 | ok |
| l17 | screens[8] | code, 6 tests, 1 example | terms at three markets [-10.2092, 3.8241, 7.1973, 0.8121] and [-3.7535, 1.2128, 2.8207, 0.28]; residuals 2e-16 | ok, starter fails; note 27 |
| l17 | screens[9] | choice `same` | same equation, payoff $\max(K - S, 0)$ | ok |
| l17 | quiz[0] | -3.28 (wrong -1.28, 3.28) | $0.32 - 1.6 - 2.0$ | ok |
| l17 | quiz[1] | -0.6721 (wrong -3.4238, -6.414, 0.6721) | put 10.675325, $\Delta$ -0.550352, $\Gamma$ 0.019788; -0.67208 (also direct formula, -0.672078); -3.42384 | ok; note 26 |
| l17 | quiz[2] | choice `rebal` | delta fixed over $dt$, reset after | ok |
| l17 | quiz[3] | 5.625 (wrong 11.25, 18.75) | $450 \times 0.0125$ | ok |
| review-4 | r-drift | 6 (wrong 4.5, 1.5) | $1.5 + 4.5$ | ok |
| review-4 | r-expconst | -2 (wrong 2, -4) | $c + 2 = 0$ (SymPy) | ok; note 31 |
| review-4 | r-exit-sigma | 12 (wrong 3, 4, 0.75) | $3/0.25$ | ok |
| review-4 | r-ever | 0.6703 (wrong 0.4066, 0.5488) | $e^{-0.4} = 0.670320$; $e^{-0.9}$; $e^{-0.6}$ | ok |
| review-4 | r-s2t2 | 14 (wrong 6, 18) | $2 \times 4 + 2 \times 3$ (`dblquad` 14.0000) | ok |
| review-4 | r-timeavg | 9 (wrong 4.5, 27) | $\int_0^3 (3 - t)^2 = 9$ | ok |
| review-4 | r-dig110 | 0.3539 (wrong 0.372, 0.4277) | 0.353861; $\Phi(d_2) = 0.372004$; $e^{-0.05}\Phi(d_1) = 0.427718$ | ok for key; warnings 10, 11 |
| review-4 | r-sqrt | 9.7045 (wrong 9.7531, 10.202) | 9.704455; 9.753099; 10.202013 | ok for key; warning 11 |
| review-4 | r-mu | choice `notmu` | price depends on $r$, $\sigma$, $K$, $T$ | ok |
| homework-4 | items[0] h-stopping | order o1 to o4, `same` o3, o4 | chain o1, o2, o3, o4; $o_4$ needs $P$ | error 2 |
| homework-4 | items[1] h-exit-report | code, 5 tests, 1 example | seed 7 [0.5808, 1.5065, 0.6008, 1.6599, 0.0077, 0.0214, 0.02, 0.1535]; seed 3 and seed 5 rows; sign and 3-se tests True | ok, starter fails; warning 9 |
| homework-4 | items[2] h-quick-prices | code, 5 tests, 1 example | [2.1895, 0.7583, 0.2367, 1617.0906]; [5.7586, 0.4207, 0.4932, 18934.359]; [2.2166, 0.3696, 0.6008, 9367.263]; pair sum 0.9139311853 (= $e^{-0.09}$); 1.0941742837 | ok, starter fails; fresh numbers |
| homework-4 | items[3] h-hermite, part 1 | -10 (wrong 10, -5) | $a + 10 = 0$ (SymPy drift $(a + 10)W^3 + (3a + 2b)tW$) | ok |
| homework-4 | items[3] h-hermite, part 2 | 15 (wrong 7.5, -15, 30) | $2b = 30$ | ok for key; warning 4 |
| homework-4 | items[3] h-hermite, part 3 | -30 (wrong 30, 0) | $3a\,tW = -30$ | ok |
| homework-4 | items[4] h-exit-drift, part 1 | 0.8611 (wrong 0.625, 0.792) | 0.861070; 0.625; 0.792028 | ok; note 29 |
| homework-4 | items[4] h-exit-drift, part 2 | 4.7214 (wrong 5.8594, 3.75) | 4.721390; 5.859375; 3.75; $E[X_\tau] = 0.944278$ | ok; note 28 |
| homework-4 | items[4] h-exit-drift, part 3 | choice `missed` | discrete steps miss crossings; others false | ok |
| homework-4 | items[5] h-moments, part 1 | 132 (wrong 36, 12) | $120 + 12$ | ok |
| homework-4 | items[5] h-moments, part 2 | 21.3333 (wrong 8, 64) | $64/3 = 21.33333$ | ok |
| homework-4 | items[5] h-moments, part 3 | 0.5 (wrong 1, 0.3333) | $\int_0^1 t\,dt$ | ok |
| homework-4 | items[6] h-derivation | longform, `pace` 300, rubric 2, 2, 2, 1, 1, 1, 1 | points sum to 10; model answer algebra checked (book $-(V_t + \tfrac12\sigma^2S^2V_{SS})dt = r(-V + SV_S)dt$; forward residual 0); the five-minute split 1, 2, 1, 1 matches the rubric | ok |

## Fix pass

Files: the seven level 4 files only. Every new number was computed twice (closed form and a second route: quadrature or a finite-difference boundary-value solve) and grepped against `courses`, `exams` and `bank`. Scripts in `.../scratchpad/fix-ito4/`. Validator 0 errors; playthrough of all seven files passes plain and with `--mobile --tablet`; screenshots of l13 screens 2 to 4, l15 screen 3 and l16 screen 4 checked at 440 and 1032; voice scan 0 and 0 for level 4 files. No code widget changed, so no code solution or starter changed.

1. Error, l14 s7: fixed. `generic`, `r0c1` and `correct` now use the exponent 2 (6.3891/7.0212 = 0.9100; the review's 7.0210 is 7.0212 on recomputation).
2. Error, homework-4 h-stopping: fixed. `same` and the "may swap" sentence deleted; only o1, o2, o3, o4 is accepted.
3. Warning, l15 quiz[3] `one`: fixed. Value 2.6667 (tolerance kept at the widget's 0.01), line names the $t^2$ slip.
4. Warning, homework-4 h-hermite part 2 `half`: fixed (line as proposed).
5. Warning, l14 s4 `flipped`: fixed (0.3348 recomputed).
6. Warning, l14 s4 explain: fixed (slope $ab/(a+b) = 2/3$).
7. Warning, l15 s6 `drop-cross`: fixed.
8. Warning, l14 s9 `swapped`: fixed.
9. Warning, homework-4 h-exit-report explain: fixed, shortened to three sentences.
10. Warning, review-4 r-dig110: fixed. $S_0 = 60$, $K = 64$, $r = 4\%$, $\sigma = 30\%$, $T = 2$: 0.3972 (quadrature agrees), wrong 0.4303 and 0.5522.
11. Warning, review-4 r-sqrt: fixed. $S_0 = 100$, $r = 4\%$, $\sigma = 30\%$, $T = 2$: 9.3941 (quadrature agrees), wrong 9.6079 and 10.1765. The l16 test value remains only in hidden tests.
12. Warning, l16 s4: fixed. $S_0 = 80$, $r = 4\%$, $\sigma = 25\%$, $T = 1.5$: 7,463.68, wrong 6,795.75, 7,925.20, 6,400.
13. Warning, l16 s0, s1: disputed. The brief (`docs/briefs/ito.md`, l16) fixes the shared option (S = K = 100, r = 5%, sigma = 20%, T = 1) with digital 0.5323 and forward 4.8771 "match them exactly"; a lesson may reuse it (DECISIONS). The 0.6578 slip value is fixed to 0.6577 (note 23).
14. Warning, l17 s6: disputed on the same ground. The brief fixes this check at the shared option (Theta -6.4140, rS Delta 3.1842, 3.7524, 0.5225), and l17 s8 says "at the shared option". The duplicate in `homework-3` is outside this level.
15. Warning, l13 repeats: fixed. s2 row now $e^{4W_t - 8t}$ (bars label too, drift 0, "yes"); s4 now $a = 5$, $c = -12.5$ (wrong 12.5, -2.5, -25); s3 reframed to ask the constant $c$ in $W_t^4 - 6tW_t^2 + c\,t^2$ (key 3, wrong 6 and 1.5), so the quartic is no longer a repeat of `homework-2`.
16. Note, l14 s8: fixed. Prose and explain say the long-run gap is about 0.03 and that quartering the step halves it.
17. Note, l14 s9 explain: fixed ("about fifteen pence").
18. Note, review-4 `timed`: fixed, 720 seconds.
19. Note, order free pairs: fixed. l14 s1 question says "Finish the chance before the time"; l15 s1 `same` is [[b1, b2], [b3, b4]].
20. Note, l13 s2 unreachable cell lines: fixed differently. The proposed `byKey` ids are rejected by the validator ("the widget cannot return the key"; table `byKey` takes cell keys only), so the table `wrong` entries on cells r0c1 and r3c1 were removed. A wrong 3, 1 or 48 now returns the cell key and shows the existing lines, which name those slips. Engine gap: table `wrong` ids cannot carry `byKey` lines (reported to `docs/BACKLOG-INBOX.md`).
21. Note, l13 s5 `drift-only`: fixed.
22. Note, l13 s8 explain: fixed, $10^{-7}$.
23. Note, l16 s0 `real-drift`: fixed, 0.6577.
24. Note, l16 s8 correct: fixed, 1.5 standard errors.
25. Note, l16 s9 explain: fixed, £48.77.
26. Note, l17 q-put: fixed ("from unrounded terms, -0.6720 from the rounded ones").
27. Note, l17 s8 canvas row: fixed ($r = 4\%$, $T = 0.5$ added).
28. Note, rounded terms: fixed. "from unrounded values" added to l14 s5 `r1c1`, l14 s7 `correct` and homework-4 h-exit-drift part 2 (`accept`).
29. Note, homework-4 h-exit-drift: fixed with $\sigma = 0.7$: $k = 0.8163$, $P = 0.9046$ (finite-difference solve 0.9042 at a grid offset), $E[\tau] = 5.5924$, driftless 7.6531, $E[X_\tau] = 1.1185$; `no-drift` 0.625, `no-sigma` 0.792 and 3.75 stay.
30. Note, l15 s3: fixed with $T = 2.5$: 5.2083, `isometry-dt` 3.125, `whole` 2.5. Canvas, hints, feedback, explain and the summary trap updated ($T^3/3$, not $T^2/2$); the explain now says the variance exceeds the endpoint's because $T > \sqrt3$.
31. Note, review-4 r-expconst: fixed. $e^{1.5W_t + ct}$: -1.125, wrong 1.125, -0.75 (added `no-square`), -2.25.
32. Note, hidden-test coincidences (l17 s7 forward, l16 test 6 seed 11 run): disputed. Test values inside code widgets are not shown as items, and the l16 seed-11 run recaps l10 and l11 by design; l17 s7 is a forward check for the lesson's own PDE and uses fresh inputs from `l16`'s hidden test only in its third value.

### Changed keys

- `l13-martingale-or-not` screens[2] table: row 2 label $e^{4W_t - 8t}$ (key unchanged 0, "yes"); `wrong` removed on cells r0c1 and r3c1.
- `l13-martingale-or-not` screens[3] numeric: key 6 to 3; `wrong` 12 to 6 (id `no-two`), 3 to 1.5.
- `l13-martingale-or-not` screens[4] numeric: key -4.5 to -12.5; `wrong` 4.5 to 12.5, -1.5 to -2.5, -9 to -25.
- `l14-hitting-and-exit` screens[1] order: prompt only (no key change).
- `l15-moments-quickly` screens[1] order: `same` [[b1, b2], [b3, b4]].
- `l15-moments-quickly` screens[3] numeric: key 0.3333 to 5.2083; `wrong` 0.5 to 3.125, 1 to 2.5.
- `l15-moments-quickly` quiz[3] `q-ito`: `wrong` `one` 1 to 2.6667.
- `l16-pricing-in-a-minute` screens[0]: `wrong` `real-drift` 0.6578 to 0.6577.
- `l16-pricing-in-a-minute` screens[4] numeric: key 10941.74 to 7463.68; `wrong` 10512.71 to 6795.75, 11502.74 to 7925.2, 10000 to 6400.
- `review-4` r-expconst: key -2 to -1.125; `wrong` 2 to 1.125, -4 to -2.25, added -0.75.
- `review-4` r-dig110: key 0.3539 to 0.3972; `wrong` 0.372 to 0.4303, 0.4277 to 0.5522.
- `review-4` r-sqrt: key 9.7045 to 9.3941; `wrong` 9.7531 to 9.6079, 10.202 to 10.1765.
- `homework-4` h-stopping order: `same` removed.
- `homework-4` h-exit-drift part 1: key 0.8611 to 0.9046 (no-drift, no-sigma unchanged); part 2: key 4.7214 to 5.5924, `wrong` `driftless` 5.8594 to 7.6531.
- `homework-4` h-hermite part 2: feedback only (values unchanged).
