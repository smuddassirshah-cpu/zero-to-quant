# opt-dash level 4 (Greeks and the dashboard): report

The four lessons were written by an earlier agent that was stopped before validating, playing or reporting them. This pass checked them, fixed what it found, and wrote `review-4` and `homework-4`.

## Files (app/content/courses/opt-dash/)

| File | Screens / items | Quiz | Code screens | Canvases |
|---|---|---|---|---|
| `l13-computing-greeks.json` | 11 screens (explore hook, problem, table, code, ladder on the plane, trap, code, tree table, derive (order), code, transfer) | 4 | `bs_greeks`, `fd_greeks`, `best_bump` | payoff (value curve, tangent, a "years left" control), table, plane (chord with an `h` control; digits-right against $\log_{10} h$), console |
| `l14-greek-profiles.json` | 12 screens (hook, explore, problem, series, code, two bars ladders, trap, hedged plane, code, derive (order), transfer) | 3 | `greek_profile` + `plot_greek_profiles` (matplotlib), `pnl_explain` + `explain_vs_reval` | plane (delta, gamma, vega profiles with a T control), series, bars, table, console |
| `l15-arbitrage-checks.json` | 11 screens (scatter hook, two payoff problems, code, table ladder, chain table, trap, calendar plane, code, generalise, transfer) | 3 | `vertical_violations` + `butterfly_violations`, `calendar_violations` | scatter, payoff, table, plane, console |
| `l16-assembling.json` | 11 screens (console hook, order, code, one-expiry table, generalise, trap, code, multi, yfinance, Deribit, transfer) | 3 | `dashboard`, `results_note` | console, table |
| `review-4.json` (new) | 9 items, difficulty 2 to 4: four from l13 and l14, two from l15, three on l16 or the whole level | | | table |
| `homework-4.json` (new) | 7 items, difficulty 3 to 5 (one at 5) | | `book_greeks` (d5), `cross_gamma` (d4) | 1 `order` (hedged P&L from the Taylor expansion and the Black-Scholes equation), 1 `longform` (10-point rubric, full model note), 2 numeric, 1 choice |

Skills: l13 and l14 `od-greeks`; l15 `od-surface`; l16 `od-greeks`, `od-surface`, `od-data`. Builders and checks are in `/tmp/claude-0/-home-user-zero-to-quant/3e0ee4d9-5633-56bc-b89e-00d7263b2d42/scratchpad/opt-dash-4/`: `br4.py` and `bh4.py` (review and homework), `edit_lessons.py` (the lesson fixes), `c13.py` to `c16b.py` and `nums4.py` (number checks), `runtests.py` (runs every code widget's hidden tests on its solution and its starter in CPython) and `voice.py` (sentence length and punctuation).

## Validator

`node tools/validate.mjs`: 0 errors overall. My six files have 0 errors and 0 warnings. Before this pass the lessons had 0 errors and 31 warnings (point hints without a highlight, and an order screen with no canvas); both are fixed.

## Playthrough (`--local-cdn .../3e0ee4d9-.../scratchpad/pkgs`)

- l13-computing-greeks: ok, 15 checks, quiz 4/4
- l14-greek-profiles: ok, 15 checks, quiz 3/3
- l15-arbitrage-checks: ok, 14 checks, quiz 3/3
- l16-assembling: ok, 14 checks, quiz 3/3
- review-4: ok, recorded 9 of 9
- homework-4: ok, marked 7 of 7, 33 of 33 marks

Every lesson was played twice: once as left by the earlier agent, once after the edits (l14 a third time after the last fix). In CPython every code widget's solution passes all its tests, and every starter fails at least one (l13 `bs_greeks` starter passes 6 of 15, `fd_greeks` 1 of 8; l15 3 of 10 and 3 of 8; l16 `results_note` 1 of 10; `book_greeks` 1 of 11; the rest 0). The matplotlib screen (l14 s4) was checked only in Pyodide, because this sandbox's CPython has no matplotlib.

Screenshots were checked by eye. They are in `.../opt-dash-4/shots`, `shots2` and `shots4`. Fixes from them: l14's hedged-P&L curve label was clipped at the right edge. A `labelAt` move put it on the curve, so the label was dropped (the y axis already names it). Homework `book_greeks`: a console result line and the starter's `def` line ran past the code column, so both are wrapped under about 54 characters.

## Fixes to the existing lessons

- Numbers: l13 s4's caption measured the chord's error against 0.636831, so it showed 0.000344 at $h = £2$; the true error is 0.0003434. The reference is now 0.63683065, and the hint and accept read 0.000343. l13 trap explanation: the best gamma bump was given as "near £0.003". The balance formula $(48\varepsilon V/V'''')^{1/4}$ gives 0.0067 ($V'''' = -2.76 \times 10^{-5}$), and a fine scan finds the smallest error at about 0.0076. It now says near £0.007. l14 trap hint: delta after a £10 fall is 0.4298, not "towards 0.45". l14 hook option: the one-month delta is 0.839 at £95 and 0.228 at £105, so "close to 1 below £90 and close to 0 above £110" (0.973 and 0.061) replaces £95 and £105.
- Voice: about 30 sentences over 20 words in prose, feedback, explanations, options and summaries were split or shortened. The remaining long sentences are the test lists in `how` lines, as in level 3.
- Hints: every `point` hint now highlights the canvas element it names (tangent spot, table rows, console lines, legs, points). l16's step-order screen has a console canvas showing `sorted(dashboard(...))`; the alphabetical keys do not give away the order.
- l16 s8 nudge "the trap on the last screen but two" now says "the trap about the vendor's vols".

## Function signatures

These are as in the brief, with earlier levels loaded in the preludes (l16's prelude holds every earlier function, as levels 1 to 3 wrote them). Departures:

- `best_bump(pricer, S, sigma, T, hs, true_gamma)`: there is a sixth argument, because the closure `pricer(S, sigma, T)` hides $K$ and $r$, so the function cannot compute the closed-form gamma itself.
- `greek_profile(..., kind="call")`: there is an extra keyword argument, and the brief's call still works.
- `node_iv(surface, K, T, F_of_T)`: a helper loaded in l15 and l16. It reads one node's smile at a strike.
- Homework: `book_greeks(positions, surface, S, r, q, dS=0.0, dsigma=0.0, dt=0.0)` takes positions as dicts with `K`, `T`, `kind` and `qty`. It reads each vol from the planted surface $(0.22 - 0.045e^{-T/0.3}, -0.08, 0.10)$ in $m$, with $F = Se^{(r-q)T}$. It returns the four summed Greeks plus `explain`. `cross_gamma(pricer, S, sigma, T, h_S=0.01, h_sigma=0.0001)` is the four-corner central difference.

## Seeds and data

`make_chain()`, seed 2320, exactly as in the brief. `clean_quotes` keeps 102 of 130 quotes (15 zero bids, 2 crossed, 2 stale, 9 wide). The dashboard takes $q$ per expiry from the implied forwards. $S = 100$, $r = 5\%$. Hand examples use $S = K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$, $q = 0$. The Monte Carlo homework item uses `mc_price` with seeds 1 to 4 (NumPy PCG64, the same stream in Pyodide). CPython: NumPy 2.5.3, pandas 3.0.5. Pyodide 0.27.7 (browser) agreed with CPython on every tested value. The dashboard's hidden tests were computed in CPython, and they pass in the browser.

Load time (browser playthrough, whole lesson): l13 19 to 21 s (pure Python); l14 23 to 27 s (NumPy and matplotlib on screen 4, `budget: 60000`); l15 22 to 25 s (pandas); l16 23 s (NumPy and pandas, the dashboard screen has `budget: 20000`). Homework 7 s (pure Python).

## Numbers stated, with sources (CPython, then Pyodide through the tests and the playthrough)

l13: the call is £10.4506. $d_1 = 0.35$, $d_2 = 0.15$. Delta 0.636831, gamma 0.018762, vega 37.524 (0.3752 per point), theta −6.4140 a year (−0.0176 a day), rho 53.2325. With $q = 1\%$, delta is 0.6118. Chord error 0.0003434 at $h = 2$ and 0.0000860 at $h = 1$ (ratio 3.99), and 8.6e-9 at 0.01. Gamma digits right, by $\log_{10} h$ from 1 to −7: 3.635, 5.639, 7.639, 9.572, 7.806, 6.865, 5.433, 2.015, 0.137. Gamma is 0.028422 at $10^{-6}$ and −0.7105 at $10^{-7}$. The 500-step tree prices the call at 10.4466; its step-1 nodes are 99.1096 and 100.8984 with values 9.8743 and 11.0134. Its delta is 0.63677 and its step-2 gamma 0.018794. A £0.01 bump of the tree gives gamma 3.3546, and its bumped vega is 37.505. The put's delta is −0.3632. Book vega: 5,000 × 0.3752 × 1.5 = £2,814.30 (per unit £281,430; one point £1,876). The one-month £150 call has delta 2.2e-12.

l14: one-month deltas at £90, 95, 100, 105, 110 are 0.973, 0.839, 0.540, 0.228, 0.061. Gamma at £100 is 0.018762 (1 year), 0.062693 (0.1) and 0.140875 (0.02). Vega per point at 0.25 years is 0.1964 (linear guess 0.0938). Week-51 deltas are 0.99994, 0.5194 and 0.00035. Explain for +£2, +1 point, one day: terms 1.2737, 0.0375, 0.3752, −0.0176; explained 1.6689, actual 1.6610, residual −0.0078. For +£10: gamma term 0.9381, explained 7.6641, actual 7.5095, residual −0.1546 (19.7 times the £2 day's). For −£10, vol flat: explained −5.4478, actual −5.3737. The hedged break-even move is £1.369; with $r = 0$ it would be $\sigma S\sqrt{dt}$ = £1.047. Vanna is −0.28143, so the cross term is −0.0056. Short three-month straddle: gamma −0.0786, vega −0.393 per point, theta +4.39p a day.

l15: the six-month call mids (cleaning dropped the £105 call) and the planted £100 mid 8.475 (6.975 + 1.50). The 90/100/110 butterfly costs −0.50. The vertical cap is $5e^{-0.025}$ = 4.8765. Unequal weight $\tfrac23$ gives a chord of 7.6083 and a failure of 1.7333; the planted frame also shows 0.035 at £85. Raw butterfly failures by expiry are 1, 2, 0, 1, 0 (£75 0.170, £75 0.145, £85 0.310, £85 0.035), against middle spreads 1.51, 1.53, 0.94 and 1.06. There are 0 fitted failures and 0 calendar failures. Desk A's forward vol is 8.2%. Quiz: 0.20, and 10.70 against 9.5123.

l16: the forward at one year is 104.12 with $q$ 0.96%. Pricer grid: tree within 0.009843, Monte Carlo within 0.733 standard errors, American put premium up to 1.043843. The one-month smile is (0.1857, −0.0789, 0.0835). ATM vols run from 0.185362 to 0.219176. The three-month £100 call has vol 0.2018, delta 0.5580 and gamma 0.0390. Explain: 1.3636, actual 1.3556, residual −0.0080. A one-expiry chain keeps 21 of 26 quotes. The one-month £75 call mid is 25.325: plain Newton jumps to 3190 and then hits zero vega; the safe solver gives 0.4865 at the implied $q$ (0.4963 at $q = 1\%$). Deribit: 0.0425 × 64,000 = 2,720.

Review: 300 × 27.36 × 0.02 = £164.15 (six-month vega 27.3587). Central delta from 11.0967 and 9.8232 is 0.63675, against the one-sided 0.6461. The one-year put has theta −1.6579. For −£3, +2 points, one day: explained 1.9199, actual 1.9302, residual 0.0104. The gamma ratio between three months and one year is 2.094. Uneven chord 9.0333, gap 0.3667. Total variance is 0.005208 at one month and 0.004817 at two. 0.031 × 58,000 = 1,798.

Homework: the ten-option book has delta −5.0941, gamma 0.1726, vega −141.7206 and theta 5.9318. Its explain is −11.2439 for (+2, +0.01, 1/365) and 23.3924 for (−5, +0.03, 1/365). The one-month £70 put has vol 0.4412 and vega 0.1766; at a flat 20% its vega would be 3.5e-8. Bumped vanna is −0.28143029 for both call and put, against −0.28143026 closed form. Short straddle, +£5: terms −0.6946, −0.9822, +0.0439; explained −1.6329, actual −1.5732. Monte Carlo delta with fresh seeds is −0.2961 (seeds 1, 2) and −1.1549 (seeds 3, 4); with a common seed it is 0.6359. One price's standard error is 0.0328. The lowest six-month vol is 18.38%.

## Departures from the brief

- `best_bump` has a sixth argument, `true_gamma` (reason above).
- l14's edge cases: the zero move is a quiz item. The move to the strike at expiry is not taught on its own, because expiry-day Greeks are NaN (l13).
- Homework `order` item: l13 and l14 already derive the bump errors and the four-term explain, and l16 orders the dashboard's steps. So the homework derives the hedged P&L $\tfrac12\Gamma(dS^2 - \sigma^2S^2dt)$ instead. That is the brief's Taylor expansion carried one step further.
- No `course.json` change is proposed.
