# Report: pdes level 1, "The heat equation" (topic 3.2)

Brief: `docs/briefs/pdes.md`, `## Level 1`, with the brief check `docs/reviews/review-briefs-3.2.md` (R14 and the stale facts) applied. Ids, names, objectives and skill (`pe-heat`) as in `app/content/courses/pdes/course.json`.

## Files written

| File | Screens / items | Quiz | Canvases |
|---|---|---|---|
| `l1-equations-in-two-variables.json` | 11 screens | 4 | `space` (Black-Scholes surface, heat surface), `table`, `plane`, `space` |
| `l2-heat-equation.json` | 11 screens | 4 | `pair` (`walk` + `bars` sim), `bars`, `walk`, `plane` |
| `l3-heat-kernel.json` | 11 screens | 4 | `plane` (kernel, `area`), `walk` (normal) |
| `l4-boundary-conditions.json` | 11 screens | 4 | `plane` (series), `table`, `plane` |
| `review-1.json` | 9 items, difficulty 2 to 4 | | all four lessons |
| `homework-1.json` | 7 items, difficulty 3 to 5 (three at 5) | | code d5, two `order`/`multi`, longform |

## Validator, playthrough, voice

- `node tools/validate.mjs`: 0 errors (warnings in my files: point hints without a highlight, ladder canvases that change kind).
- Playthrough with `--local-cdn`: l1 to l4 each ok (15 checks, quiz 4/4), `--set pdes/review-1` ok (9 of 9), `--set pdes/homework-1` ok (7 of 7, 35 of 35 marks). Run both without and with `--mobile` (the second with `--shots`); screenshots in `scratchpad/pdes-1/shots-*` at 1280 and 390 px.
- Voice scan: 0 sentences over 20 words, 0 explanations over three sentences.
- Code: every solution passes its tests and no starter passes its suite, in CPython (`scratchpad/pdes-1/codecheck.py`) and the solutions in Pyodide through the playthrough. The l2 starter passes 2 of 7 (length and sum tests), so it fails the suite as a whole.
- NumPy load time measured with a local copy: 1.2 s for the first Run examples on l2 (Pyodide already up). `how` says "a second or two".

## Departures from the brief (brief check items)

- R14: l3 uses `area` from 0 to 8 over the kernel alone (`normpdf(xc, y, ...)`, a hidden-free visible function), which reads 0.841345; the caption uses `fixed(values.A, 4)`.
- Lesson size: every lesson is 11 screens. Rungs that moved to the quiz or the review: l1, the order-of-an-equation rung is one screen and the beam-equation order is a quiz item; Tricomi at $x = -1$ is a ladder screen and its twin ($x - 2$ at $x = 1$) a quiz item; $(1-t)\sin x$ is a quiz item, as is the transport value $u(5, 1)$ with speed 3. l2: $\varphi(1) = 0.2420$, the third row of the stencil (3 steps, 0.375), the factor-2 edge and the $\Delta x = \Delta t$ diffusion are quiz items; the variance 2Dt is one ladder screen. l3: the total-heat screen stays; peak, width, backward factor and $\Phi(\sqrt2)$ are quiz. l4: the energy value $E(0.1)$, the maximum principle, the BS condition count and the put at half a year are quiz items. The review holds the data multi item and the insulated average from l4.
- l1 hook asks a choice about the price at £100, not a numeric reading of $u_t$ and $u_{xx}$; the heat surface caption computes $u_t$ and $u_{xx}$ by finite differences from the two bold slices, and the question is where they agree.
- l3 hook is a graded `slider` widget (peak halves at $t = 4$) rather than a target peak of 0.1.
- l4 hook asks the middle value at $t \to \infty$ (35), with the slider capped at $t = 3$ (39.12 there). The explicit-scheme code screen refuses $\lambda > \tfrac12$ as the brief asks.
- Homework has seven items, not eight to twelve as the review of the brief suggested: one `longform`, one `code` (d5), one `order` (drift derivation), `multi`, numeric items.
- Parameter names: `tc` and `xc` instead of `t0` and `x0`; `m` instead of `n` (see the inbox bullets).

## course.json and prerequisites

- No change proposed. The brief names "all of `odes` and `ito` level 3", while `requires` lists `odes/L4` and `ito/L3`. Per the brief check this reaches odes l2, l6, l7, l10, l16, l18, multivar, limits-thm l7, quadratics l8 and trees l10, so nothing is missing. l1 to l4 stand alone: they cite `ito` l1 and l2 and the odes edge cases by name only, and l2 states the walk facts it uses.

## Numbers and their two sources

Route A is a closed form (by hand or SymPy 1.14); route B is quadrature, a finite-difference run, the playthrough or the Pyodide test (`scratchpad/pdes-1/chk_nums.py`, `chk3.py`, `chk4.py`, `chk5.py`).

| Number | A | B |
|---|---|---|
| $u(\tfrac\pi2, 1) = e^{-1} = 0.367879$, $u_t = u_{xx} = -0.367879$ | SymPy | central differences, $h = 10^{-4}$ and the caption |
| residuals $3e^{-t}\sin 2x$, $-t\sin x$ ($-1$ at $(\tfrac\pi2,1)$) | SymPy | `heat_residual` tests in the browser |
| transport $u(3,1) = e^{-1}$; $u(5,1)$ with speed 3 $= e^{-4} = 0.0183$ | formula | evaluated numerically |
| discriminants 0, 16, $-4$, $-4x$, 4 | by hand | `classify` tests |
| call £10.4506, £6.8887 at $t = 0.5$, £1.1785 at $t = 0.98$ | `S Phi(d1) - K e^{-r tau} Phi(d2)` | put-call check, put(100,1) = £5.5735 (trees l10) |
| stencil rows $[\tfrac12,\tfrac12]$, $[\tfrac14,\tfrac12,\tfrac14]$; 3 steps: $\tfrac38$ | by hand | NumPy slice update |
| $D = 1$, wrong 2, $c = 2$, variance 4 at $t = 2$ | by hand | walk canvas bands ($\sqrt2$ and 2) |
| $P(S_{100}=0) = 0.079589$, normal 0.079788 | $\binom{100}{50}2^{-100}$ | 100 iterated averaging steps, variance exactly 100 |
| $\varphi(1) = 0.241971$ | $e^{-1/2}/\sqrt{2\pi}$ | kernel with $D = \tfrac12$ |
| $\sigma = 20\%$: $D = 0.02$, variance 0.04, sd 0.1 at 3 months | by hand | walk band at the stop line |
| kernel peak 0.282095 (t=1), 0.141047 (t=4) | $1/\sqrt{4\pi Dt}$ | NumPy |
| $\Phi(1) = 0.841345$ for the step | normal cdf | trapezium 0.841344; Simpson over $[0, 8]$ 0.841345 (R14) |
| bump $1/\sqrt5 = 0.447214$, $x=1$: 0.366148 | closed form | `quad` and `heat_line` |
| total heat $\sqrt\pi = 1.772454$ | closed form | `quad` over $\pm50$ |
| $\sqrt2 = 1.414214$; $e^{10} = 22026.47$; $e^{-10} = 4.54\times10^{-5}$; $e^8 = 2980.96$; $e^9 = 8103.08$ | exp | `math.exp` |
| $\Phi(1) - \Phi(-1) = 0.682689$ | normal cdf | `quad` |
| $E(0.1) = 0.069456$ | $\tfrac12 e^{-0.2\pi^2}$ | `quad` of $u^2$ |
| long-run middle 35; $t = 3$: 39.12; series at $t = 0$ near 100 | $20 + 30x/\pi$ | 400-term series |
| insulated series equals $x$ at $t = 0$ | Fourier cosine series | 2,000 terms |
| put at $S=0$: £95.1229; half year £97.5310; call boundary at 300: £202.4690 | $Ke^{-r\tau}$ | `math.exp` |
| perturbation 2,202.65 and $4.54\times10^{-6}$ | $0.1e^{\pm10}$ | `math.exp` |
| 29 at $x = 0.3$ (Dirichlet), 0.5 (Neumann, max error $4\times10^{-14}$) | line / average | 20,000-step runs, 0.15 s in CPython |
| unstable step: centre $-0.2$ then 0.76 ($\lambda = 0.6$), 0.36 ($\lambda = 0.4$) | by hand | NumPy |
| $2/\sqrt6 = 0.8165$, $0.5774$ ($D = \tfrac12$ bump) | formula | `heat_line_profile` |

## `space` screens

l1 screen 1 is the call surface ($S$ 60 to 140, $t$ 0 to 0.98, `normcdf` inline, `n: 30`, `shade: "height"`) with a bold slice curve and a point `on: "s"`, both bound to a `tc` slider; l1 screen 2 is $e^{-t}\sin x$ with two bold slices and a point bound to `xc` and `tc`. No plane cuts a surface. At 390 px both fit the column with the sliders below; the caption sits under the picture. The other `space` uses are static (rotation by drag works, no control needed).

## Engine notes

Five bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (topic 3.2 levels, 4 Nov)" (pdes level 1): digit-bearing parameter names in the validator, `bars` sim params in a `pair`, table width at 390 px, early screenshots of a filling histogram, starters not run. No [Must].
