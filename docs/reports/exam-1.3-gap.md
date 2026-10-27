# Topic 1.3 exam: gap-level extension

File: `app/content/exams/topic-1.3.json` (id `topic-1.3`, 60 minutes, pass 0.7, unchanged).
Generator and checks: scratchpad `exam-1.3/` (`gen.py` appends the items to a backed-up copy of the original, `topic-1.3.orig.json`; `nums.py` gives the closed forms; `verify.py` recomputes every value by a numerical route; `lint.py` checks voice).

## What changed

Three items appended after the existing 27. No existing item, id, order or header field changed (checked by script: the first 27 items and every top-level field equal the backup).

The validator caps a topic exam at 30 items (`20 to 30 items`), so the twelve requested items could not each be their own item. Each gap level got one four-part `table` item instead, so every requested topic is covered as one graded part.

| # | id | d | skills | parts (one table cell each) | rests on |
|---|---|---|---|---|---|
| 28 | `c-rates-and-bends` | 4 | lm-derivative, lm-chain, lm-optimise | MVT bound; related rate ($\sigma = \sqrt v$); $\frac{d}{dx}\arctan(x^2)$; inflection of $x^4 - 6x^2$ read beside its graph | limits l17, l18, l19, l20 |
| 29 | `c-four-integrals` | 4 | in-techniques, in-apply | partial fractions; trig substitution; $\int_0^1 x^{-p}\,dx$; volume by shells | integrals l14, l15, l16, l17 |
| 30 | `c-change-and-constrain` | 5 | mv-integrals, mv-lagrange, mv-optimise | Jacobian change of variables; triple integral; three-asset Lagrange; extreme on a closed disc | multivar l17, l18, l19, l20 |

Ramp after the change (30 items): difficulty 2: 5 (17%), 3: 14 (47%), 4: 7 (23%), 5: 4 (13%); all within the ramp's ±10%.

Each item has a `byKey` line per cell (`r0c1` to `r3c1`, the keys the table returns) naming the likely slip, a `feedback.correct`, a `generic`, and a three-sentence explanation. Item 28 has a `plane` canvas of $h(x) = x^4 - 6x^2$ (`maxHeight` 220) and an `explain.canvas` marking the inflections at $x = \pm 1$.

## Coverage and departures

- All twelve requested topics are covered, one table cell each.
- Departure: the curve sketch is not a tap item. One widget per item means "tap the inflection points" cannot sit in a multi-part table, so the part asks for the inflection's $x > 0$ with the curve drawn above. A tap item would need a 31st item, which the validator refuses.
- A table item is marked right or wrong as a whole in the exam, so these three are harder than their parts; they sit at difficulty 4, 4 and 5 for that reason.

## Validator

`node tools/validate.mjs`: 0 errors, 350 warnings repository-wide, none naming `topic-1.3.json`.

## Playthrough

`node tools/playthrough.mjs --exam topic-1.3 --local-cdn <scratchpad>/pkgs --shots <scratchpad>/exam-1.3/shots --why --mobile`: `ok topic-1.3 30 items, scored 30 of 30, passed`. All passed, no console errors.

Screenshots inspected (desktop and 390 px) for items 28 to 30 and the result page: the prose lists, KaTeX in the row labels, the plane of $h$ and the table all render and fit. On a phone the table of item 28 sits below the graph and needs a scroll; the canvas is capped at 220 px to keep that short. No layout faults found.

## Numbers stated, and their sources

Route 1 is the closed form by hand, evaluated with exact fractions (`nums.py`). Route 2 is independent (`verify.py`, 21 checks, all pass): central differences, Simpson or midpoint quadrature after a substitution that removes the singularity, a direct grid over the region, Monte Carlo, a one-dimensional brute-force search, and a dense grid plus boundary sweep.

**c-rates-and-bends**
- MVT: $f(5) \le 4 + 3 \times 4 = 16$ (slips: 19 with a run of 5, 12 without $f(1)$). Route 2: random paths with slope at most 3 never beat 16.
- $\sigma' = 0.003 / (2 \times 0.3) = 0.005$ a day (slip 0.01). Route 2: central difference 0.005000.
- $g'(2) = \frac{2 \cdot 2}{1 + 16} = \frac{4}{17} = 0.2353$ (slips $\frac{1}{17} = 0.0588$, $0.8$). Route 2: 0.235294.
- $h'' = 12x^2 - 12$: inflection at $x = 1$, $h(1) = -5$; stationary at $\sqrt3 = 1.7321$, $h(\sqrt3) = -9$. Route 2: sign changes of finite differences at 0.999 and 1.732, one inflection on $x > 0$.

**c-four-integrals**
- $\int_2^4 \frac{dx}{x^2 - 1} = \frac12\ln\frac95 = 0.2939$ (0.293893; slip 0.5878). Route 2: Simpson 0.293893.
- $\int_0^1 \frac{x^2}{\sqrt{1 - x^2}}dx = \frac\pi4 = 0.7854$ (kept limits $\frac12 - \frac{\sin 2}{4} = 0.2727$). Route 2: Simpson after $x = 1 - s^2$, 0.785398.
- $\int_0^1 x^{-2/3}dx = \frac{1}{1 - 2/3} = 3$ (slip $-3$). Route 2: Simpson after $x = t^3$ gives 3; midpoint 2.98 approaching.
- Shells: $2\pi\int_0^2 x^2(2 - x)\,dx = \frac{8\pi}{3} = 8.3776$ (no $2\pi$: 1.3333; discs about the $x$-axis $\frac{16\pi}{15} = 3.3510$). Route 2: midpoint shells 8.377580 and washers in $y$ 8.377580; discs 3.351032.

**c-change-and-constrain**
- $|J| = \frac12$: $\frac12 \cdot \frac83 \cdot 2 = \frac83 = 2.6667$ (no $J$: 5.3333; $|J| = 2$: 10.6667). Route 2: direct grid in $x, y$, 2.671.
- $\iiint_E z\,dV = \int_0^1 z\frac{(1 - z)^2}{2}dz = \frac{1}{24} = 0.0417$ (slips $\frac1{12}$, volume $\frac16$). Route 2: midpoint 0.0416667; Monte Carlo (seed 11, 400,000 points) 0.041657.
- Lagrange: $w_i = \lambda + \mu r_i$ with $\lambda = -\frac5{12}$, $\mu = \frac{25}{2}$; $\mathbf w = (\frac1{12}, \frac13, \frac7{12})$, $w_3 = 0.5833$; variance 0.018333, volatility 13.54%. Route 2: brute force along the constraint line, $w_3 = 0.583333$, $w_1 = 0.083333$, volatility 0.135401.
- Disc: interior $(0, 1)$ gives $-1$; edge $f = 8 - y^2 - 2y$ peaks at $y = -1$: $f(\pm\sqrt3, -1) = 9$; axis points give 8, 8 and 0. Route 2: grid plus boundary sweep, maximum 9.000000 at $(-1.73204, -1.00002)$.

## Voice

`lint.py`: no exclamation marks or dashes (a KaTeX `\!` was removed), every sentence under 20 words outside maths, each explanation three sentences. British spelling, no money in these items.

## Backlog

Three bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (exam topic-1.3 gap extension):": the 30-item cap, all-or-nothing marks for multi-part table items, and no compound item for a tap part.

## Proposed course.json change

None.
