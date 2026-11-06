# topology level 1 (Metric spaces revisited): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l1-many-distances.json` | 12 screens | 4 |
| `l2-open-balls.json` | 12 screens | 4 |
| `l3-closure-interior-boundary.json` | 11 screens | 3 |
| `l4-continuity-by-open-sets.json` | 11 screens | 3 |
| `review-1.json` | 9 items (difficulty 2 to 4, `pass` 0.8, every lesson) | |
| `homework-1.json` | 9 items (difficulty 3 to 5, three at 5) | |

The performance task (the verb rule matches "Prove" in l2 and l4) is `h1-equivalent-metrics-proof`, a `derivation` longform with a 10-point rubric (2, 3, 2, 3).

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; no warnings on level 1 files except "a problem screen without a canvas before the ladder ends" on the two proof-only ladder screens of l2 (order widgets need no canvas).
2. `VOICE_BASE=app/content/courses/topology python3 docs/reviews/voice-scan.py`: 0 sentences over 20 words, 0 explanations over three sentences.
3. `python3 docs/reports/topology-L1-numbers.py`: exits 0, 177 of 177 checks; `check_wrongs` passes every numeric wrong value. Its "check by hand" lines were read: each byKey names the slip without restating the wrong value (for example "the outer power is $1/p = 2$").
4. Playthrough with `--local-cdn`: every lesson, the review and the homework pass at desktop, with `--mobile`, and with `--tablet`. Screenshots at 440 px were read for the hooks of l1 to l4, the $d_p$ family, the 3D balls and the calibration plot; the only fault found (the frame label "octahedron" clipped at 440 px) was fixed by the labels d₁, d₂, d∞.

## Proof steps and their widgets

- l1: the chain $d_\infty \le d_2 \le d_1 \le 2d_\infty$: `order` with a `same` group of three and one distractor (a single example as proof).
- l2: the radius $r - d$: `expression`; balls are open: `order` with the brief's two distractors ($s = r$, $s = d(x, y)$); equivalent metrics: `order` with a dropped-constant distractor; unions open: `order` with a "smallest radius" distractor; finite intersection radius: `expression` `\min(r_1, r_2)`; infinite intersection: `choice`.
- l3: $(\overline{A})^c = (A^c)^\circ$: `order` with a wrong-negation distractor; smallest closed set: `order`; closure by sequences: `order` with an "$a_n = x$" distractor.
- l4: both directions of the preimage theorem: two `order` screens (distractor "$f(U)$ open"); closed sets: `order` with an image-complement distractor; the three $\delta$s: one vector `expression` $(\varepsilon, \tfrac\varepsilon2, \tfrac{\varepsilon}{\sqrt2})$.
- homework: finite intersections by `order`; $\delta$ for $3x - 4y$ as a vector `expression`; the whole equivalent-metrics proof as the `longform`.

## Numbers and sources

Every value below is recomputed in `docs/reports/topology-L1-numbers.py` by two routes and checked at its JSON path.

- Hook distances of the eight points (1, 1, 1, 1, 1.4, 2, 0.9, 1.2 in $d_1$): direct sums, and the on-diamond set found by filter.
- $d_p$ areas 2, 3.1416, 3.5333, 3.7081, 4 and $\tfrac23$ at $p = 0.5$: gamma formula, a 200,000-strip midpoint sum and a Monte Carlo count.
- $(0, 0)$ to $(2, 1)$: $\sqrt5 \approx 2.2361$, 3, 2; the chain checked on a grid of pairs.
- $\tfrac{1}{\sqrt2} \approx 0.7071$ (disc in diamond, and square in disc): closed form, a search along the edge and bisection.
- $P = (0.5, 0.5, 0.5)$: 1.5, 0.8660, 0.5; volumes $\tfrac43$, $4.1888$, 8 (the sphere by Monte Carlo).
- $d_{0.5}$: 4 against 2; $d_3((0,0),(1,1)) = 2^{1/3} \approx 1.2599$.
- Code: $A = (3, 0)$, $B = (2, 2)$: 3 against 2.8284 ($d_2$), 3 against 2 ($d_\infty$), 3 against 4 ($d_1$).
- Rebalancing: $d_1 = 0.30$ (£600,000), $d_\infty = 0.15$ (£300,000), $d_2 = \sqrt{0.03} \approx 0.1732$, in fractions and in floats.
- l2 fits 0.5, 0.3, 0.6 and $\tfrac{0.3}{\sqrt2} \approx 0.2121$: closed form and a bisection over each ball's rim; trap 0.1 and $(1.8, 0)$; desk room £0.6m and £0.3m.
- l3: distances 0.5, 0.2, 0.3 from the probe points to $A$; correlation lower ends $-0.5$ and $-\tfrac19 \approx -0.1111$ by closed form and bisection; eigenvalues 0, 1.5, 1.5.
- l4: $C(0.2) = £7.9656$; the accepted interval $(0.199860, 0.200364)$ by bisection on $C$ and by Newton on $\Phi$; the constants 1, 2, $\sqrt2$ for $x + y$ by random search.
- Review: $\sqrt{10} \approx 3.1623$, 4, 3; radius 1; room 0.3; constant 3 for $2x - y$ in $d_\infty$.
- Homework: constants 7, 4, 5 for $3x - 4y$ by random search; $\tfrac{0.7}{\sqrt2} \approx 0.4950$ by the four edge distances and a dense rim search; star area $\tfrac23 \approx 0.6667$; the bounded metric's $c = 1$ by bisection; `ball_area` with 20,000 strips gives 2.0, 3.1415928, 3.5332781, 3.7081506 (within $2 \times 10^{-6}$ of the gamma formula), and $4\sqrt{0.75} \approx 3.4641$ with one strip; $\max d_1/d_2$ and $\max d_2/d_\infty$ on $\mathbb{R}^4$ approach 2.

## Other notes

- The `analysis` lessons l15, l22 and l23 exist; their notation was matched and l22 is recalled in one screen (l1 screen 3).
- Pyodide first load: a cold start of Pyodide 0.27.7 from the local package took 1.7 s in Node, plus about 12 MB to fetch on first use; each `how` says "about 4 s once".
- Code screens: l1 `dist`/`nearest` (10 tests) and homework `ball_area` (7 tests). The number script runs both in CPython: the solution passes, the starter fails.
- No `course.json` change proposed.
- Backlog: 3 bullets under "Raised later (topology level 1)".
