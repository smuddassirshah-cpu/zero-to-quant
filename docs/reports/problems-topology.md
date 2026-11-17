# Problem sets: topology, levels 1 to 3 (briefs `docs/briefs/chained.md`, `docs/briefs/wave-c-author-ag.md`)

Files: `app/content/courses/topology/problems-1.json`, `problems-2.json`, `problems-3.json`: 4 problems each, 16, 16 and 17 parts. Numbers: `docs/reports/problems-topology-numbers.py` (exit 0, 754 checks plus 236 numbers_lib checks, 0 failures). Commits: f93c3b73 (level 1), b5694a36 (level 2), 3ddae607 (level 3), then this report.

Read first: every screen and quiz of l1 to l13, review-1 to 3, homework-1 to 3, and the 13 items of `exams/topic-3.4.json` that carry a `tg-` skill (no other exam carries one). Proof-heavy rule (brief rule 6): no part grades a typed proof; each tests the idea by a number (a count of open sets, boundary points, cut points, homeomorphisms, zeros), an expression (a $\delta$ in $\varepsilon$, an inverse) or one judgement choice. No part prints its own target: each later part restates only the earlier part's value.

## Sets

| set | item | parts (numeric / expression / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-plotter-zone | 4 (3 / 1 / 0) | l1, l2, l3, l4 | 5 |
| problems-1 | p-cubic-band | 4 (4 / 0 / 0) | l2, l3, l4 | 4 |
| problems-1 | p-diagonal-sphere | 4 (4 / 0 / 0) | l1, l2 | 3 |
| problems-1 | p-reciprocal-room | 4 (3 / 1 / 0) | l2, l4 | 4 |
| problems-2 | p-four-point-line | 4 (4 / 0 / 0) | l5, l6, l7, l8 | 5 |
| problems-2 | p-bond-yield-map | 4 (3 / 1 / 0) | l7, l8 | 3 |
| problems-2 | p-gapped-domain | 4 (4 / 0 / 0) | l6, l8 | 4 |
| problems-2 | p-right-rays | 4 (3 / 0 / 1) | l5, l7, l8 | 4 |
| problems-3 | p-quadratic-iteration | 5 (5 / 0 / 0) | l10, l12, l13 (l11) | 5 |
| problems-3 | p-input-output | 4 (4 / 0 / 0) | l11, l12 | 4 |
| problems-3 | p-dyadic-points | 4 (3 / 0 / 1) | l9, l11 | 4 |
| problems-3 | p-cube-delta | 4 (3 / 1 / 0) | l9, l10 | 3 |

Typed parts: 16 of 16, 15 of 16, 16 of 17. The two choice parts are judgements (connected but not Hausdorff for right rays; which of $K$, $K'$ is compact and complete).

Chains. L1: $\delta = \tfrac{2\varepsilon}{3}$, $r = \tfrac83$, $s = \tfrac{8}{3\sqrt5} = 1.1926$, $d_2(y, \partial U) = \tfrac{4}{\sqrt{10}} = 1.2649$; $h = x^3 - 27x$, length 6, $|\partial A| = 4$, 1 interior point missed by $h^{-1}((0, 54))$, $r = 3\sqrt3 - 3 = 2.1962$; $p^* = \tfrac{\ln 2}{\ln(20/13)} = 1.6090$, 4 of 6 values of $p$, $s = 0.0808$, $t = 0.0571$; $f^{-1}(V)$ length $\tfrac{4}{15}$, $\delta = 0.1$, $\delta(\varepsilon) = \tfrac{\varepsilon}{2(2+\varepsilon)}$, limit 0.5. L2: 8 open sets, $|\tau_Y| = 6$, 2 cut points, 1 homeomorphism; $y = \tfrac{100}{P} - 1$, £95.2381, $y = \tfrac{3}{97} = 0.0309$, 2 components; 4 open sets, 3 components, 2 zeros, length 5; closure end 5, interior end 10, 3 homeomorphisms. L3: $M = 1.5$, $q = \tfrac23$, $n = 37$, $x^* = 1$, rate $\tfrac13$; $d_\infty$ gap 1.1, $d_1$ ratio 0.8, $n = 98$, $x_1^* = \tfrac{1.9}{0.23} = 8.2609$; 7 points, 8 members, $N = 7$; 2 compact sets, length 9, $\delta = \tfrac{\varepsilon}{12}$, $x = 5.7685$.

Each later part restates the value it uses. Every non-whole numeric part names its form; money parts say "in pounds" or "in £m". No percentage part (yields are asked as decimals).

## Closest course material, per problem

Format: closest lesson screen; quiz item; review item; homework item; exam item. Each with how the problem differs.

**p-plotter-zone.** l2 screens[4] (largest $B_2$ round $(0.3, 0.4)$ in $B_1(0, 1)$): ours shrinks a ball of a weighted metric $2|\Delta_1| + |\Delta_2|$ by its constant $\sqrt5$. l1 `q-rn-constant`: that asks the $d_1$/$d_2$ constant; ours finds a weighted constant and uses it on a radius from a preimage. `r1-delta-max`: a $\delta$ only; ours turns the $\delta$ into a ball inside $f^{-1}((-\infty, 12))$ and chains on. `h1-delta-three-metrics`: three $\delta$ in standard metrics; ours one weighted metric, then the boundary distance. `e-half-disc`: names a boundary set; ours measures the distance to a boundary line.

**p-cubic-band.** l4 screens[0] (preimage of $(1, 4)$ under $x^2$): ours a cubic with a touching point and a half-open band. l4 `q-closed-preimage`: one preimage; ours counts boundary points and the interior point an open preimage misses. `r1-boundary-line`: the boundary of $[0, 1) \cup (1, 2)$ as a choice; ours a computed preimage, by count. `h1-punctured-plus-point`: closure facts in the plane; ours on the line, numeric. `e-preimage-quadratic` ($x^2 - 4x$, $V = (-3, 5)$): ours a cubic, then interior versus preimage and a radius.

**p-diagonal-sphere.** l1 screens[3] (slide $p$, area at $p = 4$): ours solves for the $p$ that puts a point on the sphere. l1 `q-d3`: a $d_3$ value; ours inverts $d_p$. `r1-room-taxi`: room in $B_1$; ours room in $B_2$, then a square in the disc. `h1-star-area`: an area at $p = 0.5$; ours nesting in $p$. Exam: `e-two-function-metrics` is the nearest (two distances); ours plane metrics and balls.

**p-reciprocal-room.** l4 screens[1] (preimage $(-c, c)$ of $(-1, 4)$ under $x^2$): ours a lopsided preimage of $\tfrac1x$. l4 `q-one-open-preimage`: a judgement; ours computes $\delta$ and $\delta(\varepsilon)$. `r1-delta-max`: a linear $\delta$; ours non-linear, with its limit at the edge of $X$. `h1-bounded-metric`: a ball $(-c, c)$ of a metric; ours a preimage. `e-preimage-quadratic`: a preimage only; ours the $\delta$ read from it.

**p-four-point-line.** l6 screens[0] (pieces $\{a\}, \{a, b\}, \{c\}, \{c, d\}$, tap unions): ours another basis, then subspace, cut points and homeomorphisms. l6 `q-basis-count` (5 sets): ours 8, and the chain goes on. `r2-basis-count` (4 sets): same task, other basis; ours continues. `h2-relabellings` (bijections carrying $\tau$ to $\tau'$): ours finds the self-homeomorphisms from cut points. `e-four-point-topology`: chooses a topology; ours builds one.

**p-bond-yield-map.** l7 screens[10] (the $\tanh$ calibrator) and l8 screens[11] (returns 4% to 9%): ours a price-yield homeomorphism and a removed point. l8 `q-image-connected`: a choice; ours numeric ends. `r2-f-value`: one value of l7's map; ours an inverse formula. `h2-radial-inverse`: a 2D inverse; ours 1D, then components. `e-homeomorphic-pairs`: pairs of intervals; ours counts components after removing a point.

**p-gapped-domain.** l6 screens[7] ($[0, 0.5)$ open in $[0, 1]$) and l8 screens[3] (disconnected subsets): ours counts open sets, components, forced zeros and forced values. l6 `q-relative-interval`: one set; ours five. `r2-disconnected-domain` ($f$ on $[0, 1] \cup [2, 3]$ misses 0.5): ours three components, a count of zeros and the length of the forced values. `h2-subspace-split` ($[0, 1) \cup \{2\}$): ours three pieces and the IVT on each. `e-connected-subsets`: a multi-select; ours numeric.

**p-right-rays.** l5 screens[7] (cofinite topology not Hausdorff): ours the right-ray topology, with closure, interior and homeomorphisms. l5 `q-hausdorff-finite`: finite spaces; ours infinite. `r2-hausdorff`: a multi-select of known spaces; ours derives the property. `h2-cofinite-exercise`: another non-Hausdorff topology; ours computes closure and interior ends and counts homeomorphisms. `e-homeomorphic-pairs`: the usual topology; ours shows $-x$ fails in $\tau$.

**p-quadratic-iteration.** l13 screens[1] to [5] ($\cos$ on $[0, 1]$, $q = \sin 1$, count 87, true rate $\sin x^*$): the same standard task (the course's exit skill), with $g = \tfrac{x^2 + 5}{6}$, the image found by compactness (l10), and a second root outside $X$. l13 `q-golden` and l12 `q-apriori-bound`: one value each. `r3-apriori` and `r3-constant`: one value each. `h3-use-it` ($\tfrac{1}{1 + x}$: count, iterates, true error, fixed point): ours adds the compact image, the root outside $X$ and the true rate, with no iterate table. `e-plane-contraction`: a plane map in $d_\infty$; ours 1D with the local rate.

**p-input-output.** l12 screens[6] ($\mathbf{A} = \begin{pmatrix} 0.6 & 0.6 \\ 0 & 0.3 \end{pmatrix}$, row and column constants, fixed point): a first draft asked the row sum, then the column sum, and fresh-check flagged it `retold`; it now uses a witness pair (the $d_\infty$ gap grows to 1.1, the $d_1$ ratio is 0.8), an a priori count and a Leontief fixed point. l12 `q-apriori-bound`: one bound; ours a count with a metric-mixing slip. `r3-apriori`: one count. `h3-report-code`: code; ours by hand. `e-plane-contraction`: $d_\infty$ only; ours shows why $d_1$ is the right metric.

**p-dyadic-points.** l9 screens[8] ($\{0\} \cup \{\tfrac1n\}$, why a finite subcover exists): ours counts a subcover for a given cover, then a Cauchy tail, then removes 0. l11 `q-arctan-tail`: a tail in another metric; ours the dyadic tail. `r3-compact-which`: a choice naming $\{0\} \cup \{\tfrac1n\}$; ours counts. `h3-arctan-tail`: a tail count; ours links it to the cover. `e-compact-subsets` and `e-log-metric`: membership choices; ours numeric.

**p-cube-delta.** l10 screens[5] ($\delta = \varepsilon^2$ for $\sqrt x$): ours $\delta = \tfrac{\varepsilon}{12}$ for $x^3$, then where a fixed $\delta$ fails. l10 `q-delta-sqrt` and l9 `q-which-compact`: one value or choice. `r3-image` ($x^2$ on $[-1, 2]$): the same interval with another function; ours the length of the image and then a $\delta$ (fresh-check finds no function-with-interval hit). `h3-distance-positive`: an order proof; ours numeric. `e-max-on-circle`: an extreme value; ours uniform continuity.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| validator | 0 errors, no warning on the file | same | same |
| voice scan 35 (`VOICE_BASE` the course folder) | 0 and 0 | 0 and 0 | 0 and 0 |
| fresh-check `--file` (and `--files` on all three) | 0 hits, 1 advisory | 0 hits | 0 hits, 1 advisory |
| numbers script | exit 0 | exit 0 | exit 0 |
| grade-all `--local-cdn` | 0 failures (16 widgets) | 0 failures (16) | 0 failures (17) |
| playthrough `--why` | green, 41 slips routed | green, 30 slips routed | green |
| playthrough `--mobile` | green; 440 px shots read | green; shots read | green; shots read |

The number script: route 1 is exact (sympy maxima, inequalities, solve, limits, fractions, matrix solve); route 2 is independent (direction scans for metric constants, bisection on ball radii, grid scans of preimages and boundaries, brute force over every subset, subspace and bijection of the four-point space, iterating each map, random pairs for the $d_1$ constant). It checks every key, every `wrong` value against its rebuilt slip and outside the band, byKey lines present, the key printed in `correct` and `explain` at the asked places, expression forms by sympy and at sample points, and the one correct option. It caught one draft error: $p^*$ was first written 1.6091 (it is 1.60904, so 1.6090).

Fresh-check during drafting: `p-cubic-band` first used $x^3 - 3x$ on $(0, 2]$, a function with its interval in `analysis` l17 and `limits` l17 (reported as errors); moved to $x^3 - 27x$ on $(0, 54]$. One `retold` slip line in `p-four-point-line` (the empty union, as in l6 quiz[1]) was rewritten. The two advisories are definitions (the $d_p$ formula of l1, the a priori bound of l12). Own greps: plotter, Leontief, input-output, zero-coupon and right rays appear nowhere in `app/content/`; $(0.65, 0.65)$, $(2.5, 0.5)$, $x^3 - 27x$, $2^{-n}$ and the matrix of `p-input-output` appear nowhere in the course folder.

Layout: the 440 px shots showed the first level 2 item's prose and its part 2 question running off the right edge, from a long one-span list of eight open sets; the playthrough stayed green. The lists are now split into one span per set, and the reshot pages fit.

Judgement calls a reader may question:
- `p-quadratic-iteration` is the course's exit task (show an iteration converges, bound its error), so it shares l13's steps; the compact image, the excluded root and the 5-part chain are new.
- `p-bond-yield-map` has difficulty 3 and is the only quant setting in level 2; `p-input-output` is the quant setting of level 3.
- `p-cube-delta` shares the interval $[-1, 2]$ with `r3-image` (another function).
