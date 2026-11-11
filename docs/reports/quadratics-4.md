# quadratics level 4: Algebraic fractions and polynomials (author report)

Brief: `docs/briefs/gap-quadratics.md`, section `## Level 4`. Written in the agent worktree, one commit per file.

## Files

| File | Screens | Quiz / items | Skills | Canvases |
|---|---|---|---|---|
| `l14-roots-that-stay.json` | 10 | 4 | quad-solve | plane (tilted squares, a slider-grown square, the root plot, the $\sqrt{t}$ curve), table, number-line |
| `l15-fractions-with-letters.json` | 11 | 4 | quad-factor | table, plane (point slider on two coinciding curves, a hole at $(-2, -1)$, the trap curve) |
| `l16-adding-and-solving.json` | 10 | 4 | quad-factor, quad-solve | plane (stops slider finding $p = -0.6$, the no-solution pair), table |
| `l17-dividing-polynomials.json` | 11 | 4 | quad-factor, quad-solve | plane (table cells bound to points, a $k$ slider), pair of `area` grids run backwards |
| `l18-circles-on-a-grid.json` | 11 | 4 | quad-square, quad-graph | plane: squares on the sides, a draggable lattice point with a derive caption, implicit circles, drag-point centre, tangent with right angle, a slider on the constant |
| `l19-line-meets-curve.json` | 11 | 4 | quad-solve, quad-graph | plane: the $k$ slider with the discriminant $200 - 4k^2$ in the caption (the central picture), a parabola slider, the break-even curve and a fixed-cost slider |
| `review-4.json` | | 10 items, `pass` 0.8, difficulty 2 to 4 | quad-solve, quad-factor, quad-square, quad-graph | |
| `homework-4.json` | | 8 items (one with 3 parts), difficulty 3 to 5, three at 5 | | one `longform` (10-point rubric, full model), one `order` proof, one `expression` cubic |

Each lesson follows hook, explore, name, ladder, trap, edge case, derive (an `order` screen with a distractor line in every lesson), transfer, summary, quiz. Every rule carries its conditions: $\sqrt{ab} = \sqrt{a}\sqrt{b}$ for $a, b \ge 0$; which surds simplify (a square factor above 1 inside); cancelling needs $B, C \ne 0$ and the excluded values are listed; rejected roots are checked in the original; the factor theorem is stated "exactly when ... in both directions"; tangency is a zero discriminant; a circle needs $13 - c > 0$.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors overall and no warning on any level-4 file.
2. `VOICE_BASE=app/content/courses/quadratics/ python3 docs/reviews/voice-scan.py 35`: explanations over three sentences 0, sentences over 35 words 0. No exclamation marks or dashes in the eight files.
3. `python3 docs/reports/quadratics-L4-numbers.py`: 462 of 462 checks pass, exit 0 (41 "check by hand" byKey lines read: each names the slip's own numbers, none states a false value).
4. Playthrough: every lesson, the review and the homework green without `--mobile` (one run per file during authoring, `--local-cdn`) and with `--mobile` (one run of all eight). Screenshots looked at for every lesson; fixes made: explore grid step, pair of area grids (labels unreadable side by side, now stacked with `size: [6, 2]`), function labels moved off points and off the plot edge (l16, l19), circle label (l19).

Also: `node docs/reports/quadratics-L4-grade.mjs --local-cdn <pkgs>`: 12 expression widgets, 6 numeric sets, 198 checks, 0 failures.

## Expression forms and what the grader does

The probe (`docs/reports/quadratics-L4-grade.mjs`) found `form: "simplified"` unusable on rational expressions: it refuses true simplest forms ($\tfrac{x + 8}{(x - 1)(x + 2)}$, $1 - \tfrac{3}{x}$) and accepts the uncancelled $\tfrac{x^2 + 5x + 6}{x^2 + 3x + 2}$ for $\tfrac{x + 3}{x + 1}$. So no level-4 item uses `simplified`. Forms used:

- `fraction` (l15 hook $\tfrac{7}{10}$): `0.7`, $\tfrac{42}{60}$ and the prompt $\tfrac{84}{120}$ return `form`.
- `expanded` for "type the top over this bottom" (l16 $2x + 1$, $x + 8$; review $5x - 2$): the unexpanded $3(x + 2) - 2(x - 1)$ returns `form`; $x + 1 + x$ passes.
- `factorised` (l15 $2(x + 2)$, $x(x + 2)$): the retyped product or quotient of fractions and the expanded $2x + 4$ return `form` (byKey says "a number times one bracket").
- `factorised-fully` (l17 $(x - 1)(x - 2)(x + 3)$, $(x - 1)^2(x + 2)$; review, homework cubics): a half-factorised form and the expanded cubic return `form`; any order of brackets and $(x - 1)(x - 1)(x + 2)$ pass.
- no form, an answer with no retype risk (l15 "type the top": $x - 3$; the prompt's $x^2 - 9$ is not equal).
- an equation (l18 tangent $3x + 4y = 26$): `y = -0.75x + 6.5`, `4y = 26 - 3x` and `y - 2 = -\frac{3}{4}(x - 6)` pass; the bare right side $-\tfrac{3}{4}x + \tfrac{13}{2}$ is refused (an equation never matches an expression).
- numeric sets with `unordered` for every "give both" (roots, break-even prices, $k = \pm 10$): `\pm 4`, `x = 2 or x = -0.6`, `-3/5, 2` pass; one value returns `count`.

l14 never asks for a simplified surd in a free box (ENGINE-BACKLOG 670): parts go through `table` cells and `numeric` ($a$ in $a\sqrt{2}$), and the full forms through `choice`.

## Numbers

Every number is in `docs/reports/quadratics-L4-numbers.py`, each computed twice (largest square factor against squaring back; synthetic division against evaluation and exact expansion; completing the square against substituting a point; the discriminant two ways; shoelace areas against box minus corners; brute-force lattice counts; exact Fraction identities at five rational points) and then found at its path. The brief's planner list is all confirmed. "Compute and report" values: l15 division example $\tfrac{x^2 + x}{x - 2} \div \tfrac{x + 1}{x^2 - 4} = x(x + 2)$; l16 quadratic denominator $\tfrac{2}{x^2 - 1} + \tfrac{1}{x + 1} = \tfrac{1}{x - 1}$ (excluding $x = \pm 1$).

## Conventions

- Money in £; prices in the transfer screens: £600 twice at £2 and £3 (l16), £80 to £84 (l15), the l13 subscription $p(500 - 10p)$ with cost $100p + F$ (l19), the £1,000 investment returning £400, £480 and £576 (l17).
- Volatility: daily 1%, 252 trading days, $\sqrt{252} = 6\sqrt{7} \approx 15.87\%$ (l14); risk $\sqrt{x^2 + y^2}$ for independent equal-volatility positions, stated in the screen (l18).
- No seeds or datasets.

## Deviations from the brief

- l14 tilted squares are drawn on a `plane` (polygons, `equal: true`, grid step 1): the `grid` canvas has cells, not lattice polygons. Backlog bullet.
- l17 shows division as the level-1 grid run backwards (a stacked `pair` of `area` grids, $252 \div 12$ above, $f(x) \div (x - 1)$ below), not the long-division layout.

## Proposed `course.json` change

None. (The optional `quad-rational` skill was not present, so l14 to l17 use the course's existing skills as the brief lists.)

## Fluency families for later (`docs/briefs/fluency.md`)

Simplify $\sqrt{n}$ to $a\sqrt{b}$ (asked as $a$ until ENGINE-BACKLOG 670 gives a surd form); simplify a quadratic over a quadratic (asked as the top over a given bottom); add two fractions with linear bottoms (the top, `expanded`); $f(a)$ and the remainder; centre and radius from an expanded circle (table cells); the $k$ for tangency of $y = mx + k$ to a parabola or circle.

## Backlog

Seven bullets under `Raised later (quadratics L4):` in `docs/BACKLOG-INBOX.md`.
