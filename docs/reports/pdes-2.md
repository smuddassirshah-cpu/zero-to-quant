# Report: pdes level 2, "Separation and Fourier series" (topic 3.2)

Brief: `docs/briefs/pdes.md`, `## Level 2`, with the brief check `docs/reviews/review-briefs-3.2.md` applied (R15, R16, R17 and the stale facts for pdes). Ids, names, objectives and skills (`pe-fourier`; l8 also `pe-heat`) as in `app/content/courses/pdes/course.json`. The level stands alone: `odes` and `numerics` are cited by lesson id only, `ito` is not used.

## Files written

| File | Screens / items | Quiz | Canvases |
|---|---|---|---|
| `l5-separation-of-variables.json` | 11 screens | 4 | `plane` (modes, `slopeField` with a dragged start, phase-plane `field` with `trajectory`, curves) |
| `l6-fourier-series.json` | 11 screens | 4 | `plane` (`steps`, partial sums by `sum`, `area`), `series` |
| `l7-when-fourier-converges.json` | 11 screens | 4 | `plane` (zoom on the jump, log-log, `area`) |
| `l8-heat-on-a-rod.json` | 11 screens | 4 | `plane`, `series` (live scheme), `walk` |
| `review-2.json` | 9 items, difficulty 2 to 4 | | all four lessons, plus the level 1 kernel (`r-kernel-peak`) |
| `homework-2.json` | 8 items, difficulty 3 to 5 (three at 5) | | `code` d5, `order` d4, `multi`, five `numeric`, one `longform` |

Every lesson has one `trap`, one edge case, a `code` screen with hidden tests, a `generalise` screen with a task and a quant `transfer`. First lesson (l5) opens with the one-sentence note that traders and researchers may skip the course.

## Validator, playthrough, voice

- `node tools/validate.mjs`: 0 errors, no warnings in my files (every point hint has a highlight, no ladder changes canvas kind: the two kind changes, series and walk, are `problem` and `transfer` screens).
- Playthrough with `--local-cdn`: l5, l6, l7, l8 each ok (15 checks, quiz 4 of 4), `--set pdes/review-2` ok (9 of 9), `--set pdes/homework-2` ok (8 of 8, 39 of 39 marks). Each run again with `--mobile` (screenshots at 1280 and 390 px in `scratchpad/pdes-2/shots-*`): all ok. I looked at the screenshots and fixed the hook labels, the live scheme's y range and the tail-bound area.
- Voice scan (`VOICE_BASE=.../courses/pdes`): 0 sentences over 20 words and 0 explanations over three sentences in my files. (The scan's one remaining sentence is `l4-boundary-conditions` screens[4] explain, level 1.)
- Code: every solution passes its hidden tests in CPython (`codecheck.py`) and in Pyodide through the playthrough; every starter passes 0 of its tests (CPython, 0 of 7, 8, 7, 9 and 7). The starters were not run in Pyodide (the playthrough does not run them); they return `None`, which fails identically.
- Expression grader: tested directly in the browser (`ZQ.grade.exprEqual`) for the five authored answers, 14 accepted rearrangements and 14 wrong forms (the `wrong[]` entries and near misses): all as intended (`check_expr.mjs`).
- NumPy load: first Run examples on l5 took 1.1 s with the local CDN; every `how` says "a second or two".

## Brief check items applied

- R15: the l5 phase-plane trajectory is `{ id: "T", in: "F", from: [0, 1], length: 3.1416 }`; the caption reads `values.TEndX` and shows −0.682 at λ = 2. The slider on λ starts at 2 and runs to 5.5 (0.5 would also be safe); I used 2 so that λ = 1, which also returns X to 0, is out of range and the graded answer 4 is the only one.
- R16: l8 asks the stability limit as an `expression` in `h` and `D` (`\frac{h^2}{2D}`; `\frac{h^{2}}{2\cdot D}` and three more rearrangements pass), and the L = π, N = 10, D = 1 follow-up as a `numeric` quiz item (0.049348). No answer holds `D` or `N` beside a letter. The tail bound is `\frac{1}{N}` (a lone `N`).
- R17: l8 uses the 9 by 9 array literal in a `derive` `let`, with `series.u.values` set to `w` (`vecmat(u0,matpow(A,n))`, written without spaces so the voice scan reads it as one token); no matrix builder is mentioned. The 100- and 200-interval figures are in `code` screens, explain text and the homework.
- Stale facts: no old scratchpad paths used; all numbers recomputed here (below).

## Screens that moved (lesson size)

Each lesson has 11 screens, within the 8 to 12 rule. Rungs that did not get a screen of their own:

- l5: the superposition rung (fit $3\sin x + \sin 3x$ term by term) is the hook itself. The rod of length L numeric values (2.4674, 9.8696, 22.2066) are the `q-lambda2` quiz item and `review-2`. The $\lambda = 0$ case of "$\lambda \le 0$" is in the screen's explanation.
- l6: the $f = x$ coefficients ($b_3 = \tfrac23$) and Leibniz's series ($\pi/4$) are quiz items; the finite-sine-sum edge case and the $2\pi$ divisor trap are quiz items; the even-function rung uses $|x|$ and the constant-term trap its own screen; the complex form is one `expression` screen ($c_2 = i/2$ for $f = x$; $c_1 = -i$ and the square wave's $-2i/\pi$ are in the explanation).
- l7: the midpoint rule is the `generalise` screen. The Gibbs share, the log-log slopes, the $|x|$ error, the tail bound, Parseval (`order`), the trap, the edge ($f = x$ at $\pi$), the code and the transfer each have a screen. The odd-terms sum $\pi^2/8$ and the peak place $\pi/(2M)$ for $M = 100$ are quiz items.
- l8 (the dense one): moved to the quiz, the centre at $t = 1$ with the gap 0.005238 (46.8399 to 46.8346) and the stability step 0.049348; moved into explanation text, the $N = 100$ eigenvalues ($-0.999918$, $-3.998684$, $-8.993340$) with the stiff solve 46.834596, the nonzero-ends centre 65.4425 and the explicit 200-interval 65.4410; the corridor check by images. The screen asks instead, for the grid, the $N = 10$ eigenvalue at $k = 3$ ($-8.3532$, where the continuum has $-9$), and for the ends, $b_2 = 9.5493$. The nonzero-ends centre is also homework item `h-centre-nonzero`. The corridor screen uses the first term only.

## Departures from the brief

- l5 time factor: the screen writes $T' = -\lambda T$ with $D = 1$ stated (separation gives $T' = -\lambda D\,T$); `eigenvalues(L, N, D)` returns the decay rates $D(k\pi/L)^2$.
- l6 transfer: the table gives the two sums (90 and 24, from the unrounded prices; the rounded prices give 89.9987 and 23.9716) and asks for the mean, $a_1$ and $b_2$ by the division. Summing twelve terms by hand is not the lesson.
- l7 transfer: the brief says a Fourier pricer "converges slowly for digitals and fast for calls". The truncation error of the series does not fall like $1/N^2$ for a kink: the $|x|$ error at 0 is 0.2976, 0.0635 and 0.0064 for $k \le 1$, 9 and 99, about $1/N$ (the tail bound screen says the same). The screen therefore compares the size of the first dropped coefficient, $1/k$ against $1/k^2$ (200 terms against 2,000 for 100 times smaller), which is true.
- l8 nine-point scheme: 46.5197 against the series' 47.4487 is not a grid error alone. The exact nine-point semi-discrete value is 47.4357 (0.0130 below the series), and the rest of the gap is Euler's large steps. The explanation says so.
- l8 rod_explicit rule: the step count is $\lceil t/(\lambda\Delta x^2)\rceil$, steps of $t/n$, so the actual $\lambda$ is just under the stated one. With it the centre is 46.7979 (50 intervals) and 46.8254 (100) at $\lambda = 0.4$, matching the brief's figures; 46.8323 at 200.
- l8 corridor `walk` canvas: 300 seeded paths (seed 5) show "85 hit the top, 98 the bottom (of 300)", so 183 of 300 touch (61%), the in-app sample of the daily-monitored 0.60. My custom `hitsLabel` is ignored when both barriers are set (inbox).
- Homework has 8 items (the brief asks for 6 to 12); review has 9.

## Prerequisites beyond `course.json`

`course.json` level 2 has no `requires`, so it inherits level 1 (`odes/L4`, `ito/L3`), which reaches odes l2, l6, l7, l10, l16, trig l13, complex level 1 (l3-euler named, stated again in l6) and, through odes level 3, eigen level 2. Cited by id: `odes` l2, l7, l10, l16; `eigen` l5-perpendicular-eigenvectors; `trig` l13; `complex` l3 (stated in l6 as a pointer) and l13 ("if you have met it", a forward pointer, not a prerequisite). No change to `requires` is needed. Proposed change to `course.json`: none.

## Euler's formula

Stated in l6 screen 8 ($e^{ikx} = \cos kx + i\sin kx$, with the story in `complex` lesson 3), because that lesson is not written; only $c_k = (a_k - ib_k)/2$ is used.

## Numbers and their two sources

Route A is a closed form (by hand or the formula); route B is quadrature (`scipy.integrate.quad`), `solve_ivp` shooting, a matrix exponential, an explicit or stiff scheme, the Pyodide test or the playthrough. Scripts: `scratchpad/pdes-2/nums.py`, `nums2.py`, `nums3.py`, `nums4.py`, `verify.py`, `codecheck.py`, `check_expr.mjs`.

| Number | A | B |
|---|---|---|
| $u(\tfrac\pi2, 0.5) = 3e^{-0.5} - e^{-4.5} = 1.808483$ | formula | explicit scheme, 200 intervals, ceil rule: 1.80847; hook point on the canvas |
| $X(\pi) = \sin(\sqrt\lambda\pi)/\sqrt\lambda$: 1.125280 ($\lambda = 0.5$), $-0.681582$ (2), 2.649732 (0.1) | formula | `solve_ivp` RK45 1e-11; caption $-0.682$ in the app |
| $L = 2$: 2.467401, 9.869604, 22.206610 | $(k\pi/L)^2$ | shooting by `brentq` on `solve_ivp`: same to 1e-12; code test |
| half-lives 0.0770 and 0.6931; $e^{-4.5}/e^{-0.5} = 0.0183$; 0.006105 | $\ln 2/9$, $\ln 2$ | `brentq` on $e^{-9t} = \tfrac12$ and $e^{-t} = \tfrac12$ |
| $1 + e^{-1} = 1.367879$ | formula | direct evaluation |
| squared error $2\pi - 8b + \pi b^2$: 1.424778 ($b = 1$), 1.190227 at $4/\pi$ | expansion | `quad` over the jump (4e-16), and the caption's Simpson integral in the app (1.4248) |
| $b_k$: 1.273240, 0, 0.424413, 0.254648; $x$: 2, $-1$, $\tfrac23$, $-\tfrac12$; $|x|$: $a_0 = \pi$, $a_1 = -1.273240$, $a_3 = -0.141471$ | $4/(k\pi)$, $2(-1)^{k+1}/k$, $-4/(\pi k^2)$ | `quad`; code tests (trapezium, M = 2000) |
| partial sums at $\pi/2$: 1.273240, 0.848826, 1.103474 | $\tfrac4\pi(1 - \tfrac13 + \tfrac15)$ | direct sums; code test |
| $c_1 = -i$, $c_2 = \tfrac{i}{2}$, square wave $c_1 = -\tfrac{2i}{\pi}$ | $(a_k - ib_k)/2$ | `quad` of $f\cos$ and $f\sin$: $0$, $-1$; $0.5$; $-0.6366$ |
| orthogonality: 0 and $\pi$ | by hand | `quad`: $-3\times10^{-18}$, 3.141593 |
| gas prices (12 values), mean 60, $a_1 = 15$, $b_2 = 4$; sums 90 and 24 | model | NumPy: 60, 15.0, 4.0; sums 90.0 and 24.0 (rounded prices 89.9987, 23.9716) |
| Gibbs: peaks 1.182328, 1.179814, 1.179013; limit 1.178980; 8.949% | $\tfrac2\pi\mathrm{Si}(\pi)$ | grid maximum (200,001 points) for $M = 5, 10, 50$; `quad` of $\sin x/x$; code tests |
| $|x|$ error at 0: 0.297557, 0.063453, 0.006366 | tail $\pi/2 - \tfrac4\pi\sum k^{-2}$ | partial sums from `quad`-computed $a_k$ (same to 1e-15) |
| tail $\sum_{k>10}k^{-2} = 0.095166 < 0.1$; $\pi^2/6 = 1.644934$ | $\int_N^\infty x^{-2}$; Euler | direct sum to $2\times10^6$ (1.6449336); Parseval by `quad` ($6.579736 = 2\pi^2/3$) |
| odd-$k$ sum $\pi^2/8 = 1.2337$; $\sum_{odd}k^{-4} = \pi^4/96 = 1.014678$; $\sum k^{-4} = \pi^4/90 = 1.082323$ | Parseval | direct sums (1.014678, 1.082323); `quad` energies |
| rod: centre 46.834628, 46.839865, gap 0.005238; $t = 0.1$: 99.911187, 115.207478, four terms 99.9070 (0.0042); $t_{50} = 0.934523$, $\ln(8/\pi) = 0.934712$ | series | method of lines `expm` and BDF/Radau: 46.834596 at $N = 100$; `brentq` root; code tests |
| nonzero ends: $b_1 = 82.760570$, $b_2 = 9.549297$, $u(\tfrac\pi2, 1) = 65.442508$; one term 65.4459 | $(2/\pi)\ldots/k$ | `quad` coefficients; explicit 200 intervals 65.4410 |
| $N = 10$: $-0.9918$, $-3.8701$, $-8.3532$; $N = 100$: $-0.999918$, $-3.998684$, $-8.993340$ | $-\tfrac{4}{\Delta x^2}\sin^2\tfrac{k\Delta x}{2}$ | `eigvalsh` of the tridiagonal matrix |
| top-mode factors $-0.5608$, $-0.9511$, $-1.3413$; centres 46.5197 and 1,160.98; semi-discrete 47.4357 | $1 - 4\lambda\sin^2\tfrac{9\pi}{20}$ | matrix power, an explicit loop, `expm`; the canvas caption reads 46.5197 and 1160.9807 |
| stable step $h^2/(2D)$: 0.049348 ($h = \pi/10$), 0.024674 ($h = \pi/20$, $D = 0.5$) | formula | direct |
| `rod_explicit`: 46.7979, 46.8254, 46.8323; 2,534 steps | ceil rule | CPython loop and Pyodide code test |
| corridor 0.370777, £37.08; ±0.3 with $\sigma = 25\%$: 0.540358, £54.04 | series | method of images (both to 1e-16); one-term 0.37073 and 0.54055 |
| daily-monitored survival 0.3995 | Monte Carlo, 20,000 paths, 252 steps, `default_rng(5)` | seeds 1 and 11: 0.402, 0.405 (standard error 0.0035) |
| 1.0320 = $32/\pi^3$ ($x(2 - x)$, $L = 2$, $b_1$); $u(0.5, 0.5) = 0.393918$, $u(1, 0.5) = 0.556788$ | series | `quad` coefficient; code test |

## Canvases on a phone

- The phase-plane `field` with `trajectory` fits the 390 px column, the caption sits under it, and the slider is below. At λ = 2 the orbit stays inside the frame as R15 asked.
- The live `series` scheme (9 values, `matpow` up to 30) responds without lag. With y fixed at ±150, λ = 0.6 draws a zigzag that leaves the frame, which reads as blow-up; the caption shows 1160.9807.
- The log-log `plane`, the zoom on the jump and the table (three columns, long cells wrap) fit at 390 px; the code editor clips long docstring lines, as noted before.

## Engine notes

Two bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (topic 3.2 levels, 4 Nov), pdes level 2": a `walk` `hitsLabel` with two barriers, and the voice scan reading `derive` `let` strings as prose. No [Must].
