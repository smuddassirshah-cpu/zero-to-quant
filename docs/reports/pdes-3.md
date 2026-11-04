# Report: pdes level 3, "Pricing equations" (topic 3.2)

Brief: `docs/briefs/pdes.md`, `## Level 3`, with the brief check `docs/reviews/review-briefs-3.2.md` applied (R14, R18, R19 and the stale facts for pdes). Ids, names, objectives and skills (`pe-bs`, `pe-heat`, `pe-fk`, `pe-fd`) as in `app/content/courses/pdes/course.json`. `ito` l9 and l11 (written) were read for notation and numbers; `numerics` is unwritten, so the level stands alone on the schemes it uses (the explicit scheme and Crank-Nicolson each have a derivation screen).

## Files written

| File | Screens / items | Quiz | Canvases |
|---|---|---|---|
| `l9-black-scholes-to-heat.json` | 11 screens | 4 | `plane` (call curves with a time slider; the heat solution $u(x,\tau)$ with a slider and a point on the curve) |
| `l10-formula-from-the-kernel.json` | 10 screens | 4 | `plane` with `area` (kernel times start, price in a `derive` caption) |
| `l11-feynman-kac.json` | 11 screens | 4 | `walk` (log price, 2,000 paths, `showStopped`), `plane`, `series` (Vasicek running mean) |
| `l12-four-decimal-pricer.json` | 11 screens | 4 | `plane` (factor curve, log-log errors, gamma polylines), `table` widgets |
| `review-3.json` | 9 items, difficulty 2 to 4 | | all four lessons, plus the level 2 decay rate (`r-decay`) |
| `homework-3.json` | 8 items, difficulty 3 to 5 (two at 5) | | `code` d5, `order` d4, `multi`, four `numeric`, one `longform` |

Every lesson has a trap, an edge case, a `code` screen with hidden tests, a `generalise` screen with a task and a quant `transfer`. l9 opens with the sentence that the course serves derivatives pricing and desk quant roles and may be skipped on the trading or research track.

## Validator, playthrough, voice

- `node tools/validate.mjs`: 0 errors, no warnings in my files (checked by file name).
- Playthrough with `--local-cdn`, desktop and `--mobile` (screenshots at 1280 and 390 px in `scratchpad/pdes-3/shots-*`): l9 (15 checks, quiz 4/4), l10 (14 checks), l11 (15), l12 (15), `--set pdes/review-3` (9 of 9), `--set pdes/homework-3` (8 of 8, 37 of 37 marks): all ok, with and without `--mobile`. I looked at the hook, trap, table, code and walk screens on both widths.
- Voice scan (`VOICE_BASE=.../courses/pdes`): 0 sentences over 20 words, 0 explanations over three sentences.
- Code: every solution passes its tests and every starter passes 0 of them in CPython (`codecheck.py`), and every solution passes in Pyodide through the playthrough. The slowest CPython test is 0.25 s (1,600 intervals by 320 steps with the pure-Python Thomas solver); in Pyodide the 1,600-by-320 case passes inside the 20 s `budget` I gave it. NumPy first load was about a second with the local CDN, as in levels 1 and 2. Pyodide's NumPy 2.0.2 reproduced every seeded value (10.453355 with standard error 0.046462 on `default_rng(11)`, 1.500126 with 0.005003 on `default_rng(5)`, the digital 0.531975, and the cube 2.501607) to $10^{-6}$, so the tests use that tolerance.
- Expression answers: `\frac{\sigma^2(T-t)}{2}`, `\frac{2r}{\sigma^2}`, `-\frac{k-1}{2}` and `-\frac{(k+1)^2}{4}` (R18) with the usual rearrangements in `accept`; none uses `\exp` or an integer-only symbol, so level 3 does not depend on P32-expr-int. The playthrough accepted all four.

## Brief check items applied

- R14: l10 integrates from 0 to 5 with the integrand written for $y > 0$ only (`max(0, sign(x))` times kernel times $e^{1.75y} - e^{0.75y}$); the canvas reads 0.1111 and £10.4506 through `fixed(..., 4)`.
- R18: the chain-rule results are one `order` screen with distractors (the dropped $-v_x$ is the trap), the coefficient of $v_x$ is a `numeric` screen (1.5; the slips are 2.5 and $-1$), and $\tau$, $k$, $\alpha$, $\beta$ are `expression` screens. The coefficient $-k = -2.5$ of $v$ is named in an explanation.
- R19: the Feynman-Kac `walk` is the log-price walk of the call. The Vasicek bond is a `code` screen and a `series` of the running mean (200 points from the author's own NumPy run, `default_rng(21)`) with `hlines` at 0.789581 and 0.789215. No overlay is claimed for it.
- Stale facts: no scratchpad paths of the old brief used; `numerics` cited by lesson id only; `ito` l9 and l11 are read as written.

## Lesson size: rungs that moved

All lessons are 10 or 11 screens. l12 was dense, so:

- l12: the far-boundary check (moving $\pm1$ to $\pm0.5$ or $\pm1.5$) is the quiz item `q-boundary`; the Rannacher start is the quiz item `q-rannacher`, the trap's explanation and a code test; the S-grid cross-check (£10.449972) is in the code screen's explanation; the explicit-step count is `q-steps`; the log-log slope is read in the table screen and the order is `q-order`. The explicit scheme's price table is the hook, and the factor at 96 steps the next screen. The three function groups of the brief are two code screens (`cn_heat_price`; then `richardson`, `price_to_4dp` and `explicit_heat_price`).
- l9: $r = 0$ edge case is one screen; the Black-Scholes-to-heat code screen has three functions; the $-k$ coefficient and the backward-time slip are quiz items.
- l11: the heat-case $x^2$ is a ladder screen, $x^3$ is a quiz item; the digital call with strike 110 and the $\sigma = 0$ ODE are quiz items; $d_2$ for the digital in l10 is a quiz item.
- l10: the put via the kernel is the `generalise` screen (checked by parity, not by a second integral); the digital price and $\Phi(d_1)$ as the hedge are the transfer and a quiz item.

## Departures from the brief

- l9 hook uses a `plane` of the call curves, not a `space`: l1 already has the surface, and the slider-bound `space` has known limits. The heat solution $u(x, \tau)$ is a second `plane`.
- l10 trap is a `slider` bound to the kernel variance factor $c$ (answer 2, the £6.6810 slip is a range around $c = 1$ and shows in the caption), not a `numeric` with 6.6810 as a `wrong` key. The caption reads £6.6810 at $c = 1$.
- l10 edge case: the learner reads $u$ at $\tau = 0.0005$ (0.2591) and answers $u_0(0.2) = 0.2572$ with tolerance 0.004.
- l11 hook asks a `choice` about the running mean, not a number: each reseed gives a different mean. The canvas first shows £10.33 with standard error £0.33 (seed 3, 2,000 paths); its draws are the engine's, not NumPy's, so no number in the prose comes from it. The exact value it converges to is £10.4506.
- l11 trap is a `choice` whose wrong option carries a canvas patch (`mu` 0.002, the real drift in the log step). The 15.5343 and 15.5261 figures are in the explanations.
- l12 boundary figures: the brief says moving the far boundary changes the error "by about $6 \times 10^{-6}$". At the same spacing and the same step it changes the price by $4 \times 10^{-11}$ for $\pm1.5$ and by $-3.2 \times 10^{-6}$ for $\pm0.5$ (Thomas and dense solves agree); I used those. The brief's "4.01 per halving" is not reproduced either: the ratios are 3.99, 3.97, 3.94 and 3.88 (log-log slope 1.98).
- l12 interpolation edge: with 101 intervals the price is £10.4694 (error £0.0188), 2.4 times the 100-interval error. That is not a first-order error as the brief says: it is an $h^2$ term with a larger constant (201 intervals give £0.0048). The screen asks the ratio and says so.
- l12 `price_to_4dp` is tested only at $S = K$: Richardson works only when the strike is a node (for $S = 110$ on 400 by 80 the error is $-1.2 \times 10^{-4}$, and extrapolating makes it $-1.2 \times 10^{-3}$).
- l12 explicit-scheme `explicit_heat_price` refuses $\lambda > \tfrac12 + 10^{-12}$ (floating point makes 100 steps give 0.49999999999999917).
- Homework has 8 items (the brief asks for 6 to 12) and review 9. The longform item is the colleague's £10.0085 pricer; the code item is `price_put_4dp` with `cn_solve`, `thomas`, `heat_params` and `bs_put` in a hidden prelude.
- The table screens use `byKey` on cell ids, not `wrong` ids on cells (validator limit, inbox).

## Prerequisites beyond `course.json`

`course.json` level 3 requires `pdes/L2` and `numerics/L4`. Cited by id, not needed to understand a screen: `ito` l6, l9, l11; `trees` l10; `multivar` l4; `odes` level 1 and l18; `numerics` l14, l15, l17. No change to `requires` is needed. Proposed `course.json` change: none.

## Numbers and their two sources

Route A is a closed form or SymPy 1.14; route B is quadrature, a second scheme, a dense solver or the playthrough. Scripts: `scratchpad/pdes-3/nums1.py` to `nums10.py`, `fd.py`, `vas.py`, `codecheck.py`.

| Number | A | B |
|---|---|---|
| call £10.4506 (10.450584), $d_1 = 0.35$, $d_2 = 0.15$, $\Phi$ 0.6368 and 0.5596 | formula | kernel quadrature 10.450584 (SciPy `quad`), Crank-Nicolson, Simpson as the canvas 10.450585 |
| $k = 2.5$, $\alpha = -0.75$, $\beta = -3.0625$, $\tau_{end} = 0.02$ | by hand | SymPy: $Ke^{\alpha x + \beta\tau}u$ solves Black-Scholes for three heat solutions (residual 0) |
| $u(0, 0.02) = 0.111107$ | price/$(Ke^{\beta\tau})$ | lemma $0.677056 - 0.565949$; quadrature |
| $I(1.75) = 0.677056$, $I(0.75) = 0.565949$ | lemma | `quad` |
| £17.6630 at $S = 110$ ($d$ = 0.8266, 0.6266) | formula | kernel (trapezium, 20,001 points) 17.662953 |
| put £5.5735 | parity | kernel over $y < 0$ 5.573526 |
| wrong kernel variance $\tau$: £6.6810 (6.680959) | lemma with $c = 1$ | Simpson as the canvas 6.680964 |
| $r = 0$: £7.9656 for both options, £15.9311 and £3.9828 slips | formula | $100(2\Phi(0.1) - 1)$ |
| digital £0.5323; 500 digitals £2,661.62 | $e^{-rT}\Phi(d_2)$ | kernel; MC 0.5320 with 0.0015 |
| $u_0(0.2) = 0.2572$; $u(0.2, 0.0005) = 0.2591$; $u(0.2, 0.02) = 0.3471$ | $e^{0.35} - e^{0.15}$ | lemma; Simpson |
| MC call 10.453355, 0.046462; 2,000 paths: standard error 0.33 | `default_rng(11)` | scaling $0.0465\sqrt{50} = 0.3288$ |
| heat $x^2$: 1.5001, 0.0050; $x^3$: 2.5016, 0.0124 | $x^2 + t$, $x^3 + 3xt$ | `default_rng(5)`, Pyodide test |
| real drift 15.5343 (exact 15.5261); undiscounted 10.9893 (10.9864) | closed form | seeded draws |
| real drift 8%: 12.4745 | closed form | million draws 12.4735 |
| Vasicek 0.789581, MC 0.789530 (0.000171), no noise 0.789215, 2.14 standard errors | closed form | Crank-Nicolson PDE 0.789581 (boundary from the closed form), 0.789581 again with $P_{rr} = 0$ boundaries for the homework case; MC |
| homework Vasicek 0.880706; no noise 0.880482 | closed form | PDE 0.880706 and 0.880706 (400 and 800 nodes); MC 0.880800 (0.000043) |
| explicit prices 10.4480, 10.4298, $-31.99$, $-1,446,998$; $\lambda$ 0.4545 to 0.5556 | Python loop | `numpy` explicit scheme in the app test |
| factors $-1.0828$ (96), $-1.2217$ (90), $-0.9995$ (100), $-0.8177$ (110) | $1 - 4\lambda\sin^2$ | `eigvalsh` of the explicit matrix ($-1.082819$) |
| CN prices 10.4427214, 10.4486123, 10.4500869, 10.4504574, 10.4505511 vs 10.4505836 | Thomas | dense solve at 200 and 400 by 80; S-grid CN 10.449972 |
| errors ×10⁶ 7862.2, 1971.3, 496.6, 126.1, 32.5; ratios 3.99, 3.97, 3.94, 3.88 | subtraction | same |
| Richardson 10.4505760 (100 and 200), 10.4505785 (200 and 400) | formula | both from the table prices |
| CN 400 by 4: 10.0085, $g = -0.9950$ ($\lambda = 200$); 1,600 by 50: error 0.0308; Rannacher 10.4492 | CN loop | formula for $g$; dense solve |
| gamma of 400 by 4: minimum $-0.2159$, 16 negative nodes; Rannacher minimum 0.0096 | second differences | exact gamma |
| odd grid 101: 10.4694 (error 0.018829), 201: 10.4553; 100: error $-0.007862$ | CN | ratio 2.395 |
| boundary shifts $4 \times 10^{-11}$ and $-3.2 \times 10^{-6}$ | Thomas | dense solve |
| review: $k = 0.8889$, $\beta = -0.8920$, sd 0.2121, put 6.2715, 12.4745, 0.104, Richardson 7.7603 (7.7602565), $c = 1.0966$ | by hand | scripts above |
| homework: put Richardson 5.5735209 (6.5076263 for the second); explicit top mode $1.6626^{12} = 446$; sequence 1,600; $\sigma = 13.33\%$; 14.48 | by hand | CN put solver; direct powers |

Pyodide against CPython: no value differed, so the seeded tests use the CPython values at $10^{-6}$.

## Engine notes

Three bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (topic 3.2 levels, 4 Nov), pdes level 3" (table cell `wrong` ids and the validator, the `walk` overlay and running-mean panels filling the screen, log-log x title position). No [Must].
