# Problem set odes level 4 (Transforms and numerical solution): second-reader findings

Scope: `app/content/courses/odes/problems-4.json`: 3 problems, 15 parts (4 `expression`, 11 numeric of which 1 is a set, 0 choice), 32 `wrong` entries. Rules: `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md` (Author, Reader). Pattern: `review-problems-analysis-1-3.md`. Levels 1 to 3 of the course are another agent's and were not read as sets.

Method. The author's script was run first. Every part was then solved by hand from its text and again in `docs/reports/problems-odes-4-numbers-read.py`, which imports nothing from the author's script. Laplace: each transform by sympy `laplace_transform` and by the defining integral at 50 digits; each inverse by `inverse_laplace_transform`, by `residue` and `apart`, and by putting the answer back into its equation and starting values; the two carried slips of `p-skydiver-check` part 2 inverted as well. Euler and Runge-Kutta: my own steppers, once in exact fractions (17.64, the four slopes, 48.4512, 16.1504 are exact) and once in 50-digit mpmath against the closed form (errors 1.4857, 0.003917, 0.000207, 0.0000119), with RK4 cross-checked by its stability polynomial $v_n = 49(1 - R(-0.2h)^n)$. Stability: $|1 - 6h| < 1$ solved exactly; the RK4 edge as the real root of $R(z) = 1$ (2.785294) and $|R| < 1$ scanned on the whole interval; the fewest stable step counts found by the spectral radius of the step matrix of the two-equation system itself for $n = 1$ to 399 (Euler 73, RK4 52; $n = 72$ on the edge, RK4 at 51 grows). Every `wrong` value was rebuilt from the slip its line names and every band shown clear of the key band. Each typed part went through the engine's graders (`review-problems-linear-maps-4-scripts/grade-probe.mjs` with `review-problems-odes-4-scripts/rows.json`, 140 strings of my own). Reuse: l14 to l18, `review-4`, `homework-4` and `exams/topic-1.11.json` were read for their equations, transforms, step sizes and stories; key numbers grepped in the course, stories across `app/content`.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-odes-4-numbers.py` exit 0, 0 failures |
| reader's script | `problems-odes-4-numbers-read.py` 154 checks, 0 failures, exit 0; 2 CLAIM lines hold (finding 1) |
| `grade-probe.mjs` (engine graders, 15 typed parts) | 224 checks, 140 reader rows, 0 failures, exit 0; 3 rows held to be an engine limit (Engine 1) |
| `proposed.py` (numbers of the fix of finding 1) | 40 checks, 0 failures, exit 0; the replaced set through `grade-probe.mjs` (`rows-proposed.json`) 209 checks, 0 failures; `grade-all --file` on it 0 failures; voice 0 and 0 |
| validator | 0 errors; no warning names `odes/problems-4` |
| `grade-all.mjs --file` | 15 widgets, 0 failures |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --file` (same-course mode) | 0 hits, 0 advisories; it does not see finding 1 (Engine 2) |

Every key, every `wrong` value, every Laplace transform and inverse, every Euler and RK4 step and every error figure is right. No finding of severity wrong. One reuse finding that renumbers a problem, one low finding.

## Findings

1. `problems-4.json` | `items[0]` (`p-test-rig`, all five parts) | reuse | The problem is l15 `screens[3]`'s worked example with $s$ shifted by 2 and the transform times four. DECISIONS session AC rules that a number times four and a series with the index shifted count as reuse and are renumbered. | l15: $y'' + 3y' + 2y = 2$, $y(0) = y'(0) = 0$, $Y = \dfrac{2}{s(s + 1)(s + 2)}$, residues 1, $-2$, 1, $y = 1 - 2e^{-t} + e^{-2t}$, and "At $t = 1$ that is 0.399576". Here $Y = \dfrac{8}{(s + 2)(s + 3)(s + 4)} = 4\,Y_{\text{l15}}(s + 2)$: poles $-2, -3, -4$ are l15's $0, -1, -2$ shifted, residues 4, $-8$, 4 are l15's times four, and $y = 4e^{-2t}(1 - 2e^{-t} + e^{-2t})$ is $4e^{-2t}$ times l15's solution. The `at-one` slip 0.2163 is $4e^{-2} \times 0.399576$. Any three equally spaced poles from a zero start give residues in the ratio $1 : -2 : 1$, so the fix needs unequal gaps. | Replace the item by `docs/reviews/review-problems-odes-4-scripts/proposed-p-test-rig.json` (the whole item, exact text; same id, story, skills and left side $y'' + 6y' + 8y$; forcing $24e^{-8t}$). Keys: part 1 $\dfrac{24}{s + 8}$ (slips $\dfrac{24}{s - 8}$, $\dfrac{1}{s + 8}$); part 2 $\dfrac{24}{(s + 2)(s + 4)(s + 8)}$ (slips $\dfrac{24}{(s - 8)(s + 2)(s + 4)}$, $\dfrac{24}{(s + 8)(s - 2)(s - 4)}$); part 3 the residue at $s = -4$, $\dfrac{24}{(-2)(4)} = -3$ (slips 3 and 2; the others are 2 at $-2$ and 1 at $-8$, sum 0); part 4 $y = 2e^{-2t} - 3e^{-4t} + e^{-8t}$ (slips $2e^{2t} - 3e^{4t} + e^{8t}$, and $+3$ in the middle with $y(0) = 6$); part 5, with $u = e^{-2t}$, $y = 2u - 3u^2 + u^4$ and $\tfrac{dy}{du} = 2(u - 1)(2u^2 + 2u - 1)$ printed in the question, the peak $\tfrac{6\sqrt3 - 9}{4} = 0.3481$ at $u = \tfrac{\sqrt3 - 1}{2} = 0.3660$, $t = \tfrac12\ln(1 + \sqrt3) = 0.5025$, tolerance 0.0005, "to 3 decimal places" (slips 0.366 the $u$, 0.5025 the time, 0.2161 $= y(1)$). $y = u(1 - u)^2(u + 2) \ge 0$, so the "no overshoot" line stays true. Nothing in `app/content` has $6y' + 8y$ or these three poles; `exams/topic-1.11` item 17 has an unforced $y'' + 10y' + 16y$ with an $e^{-8t}$ term, a single shared exponent. The author's script needs the new keys and slips; `proposed.py` holds them.

2. `problems-4.json` | `items[2].parts[3].question` | misleading (low) | The RK4 rule is stated for any $\lambda$: "RK4 on $y' = \lambda y$ is stable when $h|\lambda| < 2.7853$." It holds on the negative real axis only: for $\lambda > 0$ the solution grows, and for complex $\lambda$ the region is not a disc of radius 2.7853. `review-4` item 7 states it with the sign built in ($y' = -\lambda y$, $h\lambda < 2.7853$). | The real edge is the root of $R(z) = 1$, $z = -2.785294$. Inside the disc $|z| < 2.7853$ the rule fails off that axis: $R(1) = 2.7083$ and $|R(0.2 + 2i)| = 1.0073$, both above 1. | Question becomes: "For a real negative $\lambda$, RK4 on $y' = \lambda y$ is stable when $h|\lambda| < 2.7853$. Using $\lambda = -6$, below what step $h$, in hours, is RK4 stable? Give your answer to 4 decimal places." Key 0.4642 unchanged.

## Read and held to stand

- `p-skydiver-check` is a comparison chain: part 3 restates part 2's 16.1543, part 5 restates part 4's error 0.0039. Parts 3 and 4 can be worked without the earlier keys, but each needs them to mean anything, and the last part is the result. Drawn on l15, l16, l17, l18. Stands.
- `p-skydiver-check` part 5 asks for a prediction from the order, as `review-4` item 6 and l18 `quiz[3]` do with other numbers ($48 \times 10^{-6}$, $1.4 \times 10^{-5}$). The true errors give the same $n = 4$, and RK4 at $n = 4$ does print 16.1543.
- `p-dose-simulator` is the task of `review-4` items 5 and 7, `homework-4` item 3 and l17 `screens[11]` with its own system and numbers (theirs: eigenvalues $-1, -3$; 25; $-1, -20$; $40/n$). Same standard task, own setting. Stands. Part 1 is level-3 work used as a first step.
- Stories: "skydiver", "gut", "dose", "air drag" occur nowhere else; "tablet" and "drug" in `series/problems-1` (a daily tablet as a geometric series, another topic); "test rig" in `brainteasers` l9 (egg drop). 2.7853 is RK4's stock limit, in l17 and `review-4`.
- Bands: 16.154 and 16.15 are refused in part 2 and 16.150 in part 4, as "4 decimal places" says; 0.333 is refused for $\tfrac13$, as "4 places" says; `0.25 cm` and `1/4` are accepted.
- Level cover: l14 and l15 (item 1), l15 to l18 (item 2), l16 and l17 (item 3). Skills are the level's (`de-first` is l18's). Difficulty 4, 5, 4.

## Engine

1. `numeric` drops a lone letter and `=` but not the question's own left side: `v(2) = 16.1543`, `h < 1/3` and `h < 0.4642` are refused on the generic line ("below what step $h$" invites the inequality).
2. `fresh-check --file` in same-course mode gave 0 hits and 0 advisories on a problem whose transform is a lesson's shifted and scaled (finding 1). A rational function's pole gaps and residue ratios are unchanged by a shift and a scale; nothing compares them.

Inbox: two bullets under `Raised later (review problems odes 4):`.
