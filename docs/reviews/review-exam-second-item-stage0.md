# Review: exam second item, stage0 (topic-0.3, topic-0.2, topic-0.4)

Second read of the eight new items in `docs/reports/exam-second-item-stage0.md` (commits eacef006, da46fb40, ce330b65). No content edited, no browser.

- Author's script `docs/reports/exam-second-item-stage0-numbers.py`: 149 of 149, exit 0.
- Reader's script `docs/reports/exam-second-item-stage0-numbers-read.py`: 148 checks, exit 0, 4 `FINDING` lines (findings 1 to 4 below). Other routes than the author's: enumeration of pairs and triples, bisection for the ratio and the rates, a grid scan for the roots, Pascal rows built by multiplying by $(1 + x)$, a keyboard map. Lines marked `fix` recompute every number of the fixes below.
- Validator 0 errors. Voice scan on `app/content/exams`: 0 and 0. `grade-all.mjs --file`: 0 failures on each exam (30, 25 and 16 widgets; the report's "21" for `topic-0.4` is the item count, not the widget count).
- `fresh-check.mjs --file` on `topic-0.3`: 0 hits; no advisory names a new item.

## Structure

| check | topic-0.3 | topic-0.2 | topic-0.4 |
|---|---|---|---|
| items | 26 to 30 (5 in, 1 out) | 30 (2 in, 2 out) | 20 to 21 (1 in) |
| minutes | 60 x 30/26 = 69.2, so 70 | 75, count unchanged | 60 x 21/20 = 63, so 65 |
| ramp d2/d3/d4/d5 | 6/15/6/3 | 6/15/6/3 | 4/11/4/2 |
| listed pairs, auto items now | all 8 on 2 | fn-transform 2, quad-model 2 | tm-typing 2 |
| lowest skill of the exam | 2 | 2 | 2 |

Pairs recounted from the exam before the change (82f9d534) and every review of the topic's courses: the same 8, 2 and 1. `e-spread-model` is longform on the item, so `quad-model` did hold one auto item.

Removals, each skill of the removed item counted over auto items after the swap:

| removed | skills | auto items left |
|---|---|---|
| topic-0.3 `e-sigma-odd` | seq-sums | 2: `e-weekly-savings`, `e-loan-payment` |
| topic-0.2 `e-two-roots` | quad-solve, quad-factor | quad-solve 4: `e-two-desks`, `e-two-rates`, `e-fg-equation`, `e-tangent-line`; quad-factor 2: `e-factorise`, `e-odd-squares` |
| topic-0.2 `e-formula` | quad-solve | 4, as above |

All three removals hold. Note: quad-factor and seq-sums now sit on exactly two auto items, so neither can lose another.

## Skill tags, item by item

| item | tags | verdict |
|---|---|---|
| `e-desk-meetings` | ct-comb | tests it; cannot be passed without it |
| `e-rebate-third` | seq-converge, seq-geom | needs both: the ratio comes only from $S_\infty$, the answer only from a term |
| `e-double-angle-roots` | tr-identities, tr-equations | **fails the two-skill rule** (finding 1) |
| `e-parallelogram-midpoint` | vc-arrows, vc-geometry | needs both, thinly: the only vc-geometry step is the midpoint of BC (taught in `counting/l12`, screens[4]); the sum, end minus start and the length are vc-arrows |
| `e-coefficients-in-step` | seq-arith, seq-binomial | needs both: the coefficients need $\binom{n}{k}$, the condition needs equal differences; $n = 2$ and 7 are the only values up to 199 |
| `e-read-the-change` | fn-transform | tests it; only option a matches the dashed curve on a grid of 65 points |
| `e-two-rates` | quad-model, quad-solve | needs both: forming $(1 + r)(1 + 2r) = 1.1872$, then the formula |
| `e-left-hand-commands` | tm-typing | tests it; the keyboard map gives `cat`, `sed`, `wc` and the three stray keys P, H, U |

## Reuse, item by item

| item | closest exam item | closest lesson screen | closest review | closest homework | closest problem-set item | rule |
|---|---|---|---|---|---|---|
| `e-desk-meetings` | `e-tech-pick` (2 tech of 4 from 12, a chance) | `counting/l4` screens[1] ("Every pair fills exactly two of them ... $12 \div 2 = 6$ pairs") | `counting/review-1` `r-team-of-four` (4 of 9 analysts) | `counting/homework-1` `h-correlations` ("one number for each pair of different stocks") | `counting/problems-1` `p-five-a-side` parts 1 and 2 | **reuse** (finding 3) |
| `e-rebate-third` | `e-perpetuity-now` (sum of a stream) | `series/l8` screens[3] ($6 + 2 + \tfrac23 + \dots$, find $S_\infty$) | `series/review-2` `r-impact` ("Each later minute adds 60% of the previous minute's move, forever") | `series/homework-2` `h-recurring` | `series/problems-2` `p-bouncing-ball` | clean: no item of the course goes from the total back to the ratio |
| `e-double-angle-roots` | `e-double-angle-solve` ($\cos 3x = \tfrac12$) | `trig/l11` screens[8] ($2\sin^2 x - \sin x - 1 = 0$) | `trig/review-3` `r3-cos-quadratic` | `trig/homework-3` `h3-phase-crossing` | `trig/problems-3` `p-quadratic-in-sine` | clean on reuse; see finding 1 |
| `e-parallelogram-midpoint` | `e-vector-ratio` (X on AB, $1 : 2$) | `counting/l10` screens[5] and [6] | `counting/review-3` `r-diagonal` ("OABC is a parallelogram with $\overrightarrow{OA} = \mathbf{a}$ and $\overrightarrow{OC} = \mathbf{c}$") | `counting/homework-3` `h-diagonals` (same sentence, a proof) | `counting/problems-3` `p-sail-ring` | **reuse** of a number set (finding 2); the figure sentence is shared with the review and the homework, the task is not |
| `e-coefficients-in-step` | `e-binomial-cube` (find $a$ from one coefficient) | `series/l9` screens[6] (row 7 printed) | `series/review-3` `r3-row-eight` (row 7 printed) | `series/homework-3` `hw3-x-five` | `series/problems-3` `p-powers-of-eleven` | clean: 7, 21, 35 is Pascal's row, no item asks for coefficients in step |
| `e-read-the-change` | `e-shifted-peak` (apply $f(x + 3) - 2$ to a point) | `functions/l15` screens[0] ($g(x) = 2f(x)$ on a hill) | `functions/review-4` `r4-two-moves` ("highest point of $y = 2f(x - 4)$") | `functions/homework-4` `h4-squash-lift` | `functions/problems-4` `p-fountain-jet` part 2 | clean: those apply a rule, this reads one from two curves, on a new function |
| `e-two-rates` | `e-floor-area` (rectangle, 96 m²) | `quadratics/l1` screens[8] (£2,000 at $r$ for two years) | `quadratics/review-2` `r2-return` | `quadratics/homework-2` `hw2-return` | `quadratics/problems-3` `p-bike-hire` | **reuse**, low (finding 4) |
| `e-left-hand-commands` | `e-typing-speed` (characters in three minutes) | `terminal/l1` screens[3] ("Tap every key the left index finger presses") | `terminal/review-1` `r-right-index` | `terminal/homework-1` `h-return-index` (index-finger keys of `return`) | none on tm-typing | clean: sorts whole words by hand, no shared word |

## Findings

1. `app/content/exams/topic-0.3.json` | `items[18]` (`e-double-angle-roots`) `.prose`, `.widget`, `.feedback`, `.explain` | high, misleading (tag) | The item is tagged tr-identities and tr-equations under rule b, but it can be answered with tr-equations alone. | Equal sines: $2x = x + 360^\circ k$ gives 0°; $2x = 180^\circ - x + 360^\circ k$ gives 60°, 180°, 300°. That is the whole key, with no identity. The course teaches the route: `trig/homework-3` `h3-phase-crossing` prints "Equal sines need equal angles, or angles adding to $\pi$, up to whole turns". The script's grid scan and this route agree on [0, 60, 180, 300]. | Change the equation so no angle pairing works. Keep id, title, skills, difficulty, pace, question, tol, placeholder, label.
   - `prose`: `Solve $\sin 2x = \sqrt{3}\cos x$ for $0^\circ \le x < 360^\circ$.`
   - `widget.answers`: `[60, 90, 120, 270]`; `widget.accept`: `60, 90, 120 and 270, in any order`
   - `widget.wrong`: `[{"id": "cos-pair", "value": "60, 90, 270, 300"}, {"id": "cos-root", "value": "30, 90, 270, 330"}]`
   - `feedback.correct`: `$\cos x(2\sin x - \sqrt{3}) = 0$, so $\cos x = 0$ or $\sin x = \tfrac{\sqrt{3}}{2}$: 90°, 270°, 60° and 120°.`
   - `feedback.generic`: unchanged.
   - `feedback.byKey.count`: `There are four solutions. Dividing by $\cos x$ loses the angles where $\cos x = 0$, which are 90° and 270°.`
   - `feedback.byKey.cos-pair`: `You took $360^\circ - 60^\circ$, as for cosine. Sine is $\tfrac{\sqrt{3}}{2}$ at 60° and at $180^\circ - 60^\circ = 120^\circ$.`
   - `feedback.byKey.cos-root`: `You solved $\cos x = \tfrac{\sqrt{3}}{2}$. The factor left after taking out $\cos x$ is $2\sin x - \sqrt{3}$.` (delete `sine-pair` and `sin-half`)
   - `explain.text`: `The identity $\sin 2x = 2\sin x\cos x$ turns the equation into $2\sin x\cos x - \sqrt{3}\cos x = 0$, which is $\cos x(2\sin x - \sqrt{3}) = 0$. So $\cos x = 0$, giving 90° and 270°, or $\sin x = \tfrac{\sqrt{3}}{2}$, giving 60° and 120°. Dividing by $\cos x$ instead would lose 90° and 270°.`
   - Recomputed: grid roots of $\sin 2x - \sqrt{3}\cos x$ on $[0^\circ, 360^\circ)$ are 60, 90, 120, 270; 300, 30 and 330 are not roots; two roots survive division by $\cos x$. No hit for $\sqrt{3}\cos x$ against $\sin 2x$ in `trig`, `stage-0`, the topic exams or the mocks.

2. `app/content/exams/topic-0.3.json` | `items[21]` (`e-parallelogram-midpoint`) `.prose`, `.widget`, `.feedback`, `.explain` | medium, reuse (number set) | The two vectors are the pair of a lesson of the same course, and one slip is that lesson's answer. | New: "$\overrightarrow{OA} = (4, 1)$ and $\overrightarrow{OC} = (1, 3)$". `counting/l10-adding-arrows` screens[5]: "Here $\mathbf{u} = \begin{pmatrix} 4 \\ 1 \end{pmatrix}$, $\mathbf{v} = \begin{pmatrix} 1 \\ 3 \end{pmatrix}$ ... Drag the head of $\mathbf{w}$ so that $\mathbf{w} = \mathbf{u} - \mathbf{v}$"; screens[6] uses them again. The `b-minus` slip starts from that same $\mathbf{u} - \mathbf{v} = (3, -2)$. | Use $(-4, 2)$ and $(3, 5)$ (no hit as a pair in `counting`, `stage-0`, the topic exams or the mocks; avoids $\sqrt{17}$ of `l11` screens[1] and $\sqrt{52}$ of `e-two-u-minus-v`).
   - `prose`: `OABC is a parallelogram, with its corners in that order. O is the origin, $\overrightarrow{OA} = (-4, 2)$ and $\overrightarrow{OC} = (3, 5)$. M is the midpoint of BC.`
   - `widget.answer`: `6.403124`; `widget.accept`: `6.40 (exactly $\sqrt{41}$)`
   - `widget.wrong` values: `b-minus` 2.24 ($\sqrt5$: B taken as $(-7, -3)$, M as $(-2, 1)$, so $(2, -1)$), `om` 6.08 ($\sqrt{37}$), `no-root` 41; tolerances unchanged.
   - `feedback.correct`: `B is $(-1, 7)$ and M is $(1, 6)$, so $\overrightarrow{AM} = (5, 4)$ and its length is $\sqrt{41} \approx 6.40$.`
   - `feedback.byKey.no-root`: `That is the square of the length. Take the square root of 41.` (`b-minus`, `om`, `generic` unchanged)
   - `explain.text`: `Opposite sides match, so $\overrightarrow{OB} = (-4, 2) + (3, 5) = (-1, 7)$. M is halfway from B to C, at $(1, 6)$, so $\overrightarrow{AM} = (1 + 4, 6 - 2) = (5, 4)$. Its length is $\sqrt{25 + 16} = \sqrt{41} \approx 6.40$.`
   - Recomputed with complex numbers: key 6.403124; bands 6.40, 2.24, 6.08, 41 at 0.005 do not touch.

3. `app/content/exams/topic-0.3.json` | `items[5]` (`e-desk-meetings`) whole item | medium, reuse (story) | The task is the round-robin count of the course's problem set with 9 in place of 8, and its `ordered` slip is that item's part 2. | New: "pairs 9 desks so that every desk meets every other desk exactly once. How many meetings are there?" (36; slip 72). `counting/problems-1` `p-five-a-side`: "A five-a-side football league has 8 teams. In a season every team plays every other team twice" with part 1 "How many different pairs of teams are there?" (28) and part 2 $P(8, 2) = 56$. Also outside the brief's scope but the same numbers: `counting-chance/review-2` `r-pairs`, 9 traders shaking hands, $\binom92 = 36$. | Replace the story and the count; keep id, skills, difficulty, pace, tol, placeholder.
   - `title`: `Corners on a circle`
   - `prose`: `Ten points are marked on a circle. A triangle is drawn by joining three of them.`
   - `question`: `How many different triangles can be drawn?`
   - `widget.answer`: `120`; `label`: `Triangles`; `accept`: `120`
   - `widget.wrong`: `ordered` 720, `third` 240, `pairs` 45, each `tol.abs` 0.
   - `feedback.correct`: `Each triangle is a choice of 3 points from 10: $\binom{10}{3} = 120$.`
   - `feedback.generic`: `A triangle is a set of three points, and the order of the three does not matter. Count the sets.`
   - `feedback.byKey.ordered`: `You counted each triangle 6 times, once for every order of its corners. Divide by $3! = 6$.`
   - `feedback.byKey.third`: `You divided the 720 ordered picks by 3. Three corners can be listed in $3! = 6$ orders, so divide by 6.`
   - `feedback.byKey.pairs`: `That is $\binom{10}{2}$, the number of lines joining two points. A triangle needs three corners.`
   - `explain.text`: `Each triangle picks 3 of the 10 points, and the order of the three does not matter. There are $10 \times 9 \times 8 = 720$ ordered picks, and each triangle appears $3! = 6$ times. So there are $\binom{10}{3} = \tfrac{720}{6} = 120$ triangles.`
   - Recomputed by enumeration: 120 sets of three, 720 ordered, 720/3 = 240, 45 pairs. No "points on a circle" or $\binom{10}{3}$ in `counting`, `series`, `stage-0`, the topic exams or the mocks ($\binom93 = 84$ was avoided: it is part 4 of `p-five-a-side`).

4. `app/content/exams/topic-0.2.json` | `items[22]` (`e-two-rates`) `.prose`, `.widget`, `.feedback`, `.explain` | low, reuse (story and key) | A two-year growth whose rate is 6% with the negative root rejected is already the course's homework; the `one-rate` slip is that homework's method. | New: "£10,000 grows to £11,872 over the two years ... What is $r$, as a percentage?" (6%). `quadratics/homework-2` `hw2-return`: "A fund grows from £5,000.00 to £5,618.00 over two years, at the same return each year. What is the yearly return, as a percentage?" with "$1 + r = \pm 1.06$; the negative root is impossible. So $r = 6\%$". The equation differs ($r$ then $2r$ needs the formula), so only the numbers move. | £25,000 to £31,320, rate 8%.
   - `prose`: replace `£10,000 grows to £11,872` by `£25,000 grows to £31,320`.
   - `widget.answer`: `0.08`; `accept`: `8% (from $2r^2 + 3r - 0.2528 = 0$)`
   - `widget.wrong` values: `simple` 0.0843, `one-rate` 0.1193, `other-root` -1.58; tolerances unchanged.
   - `feedback.correct`: `$(1 + r)(1 + 2r) = 1.2528$ gives $2r^2 + 3r - 0.2528 = 0$, so $r = 0.08$, or 8%.`
   - `feedback.generic`: replace `£10,000` by `£25,000` and `1.1872` by `1.2528`.
   - `feedback.byKey.simple`: replace `$3r = 0.1872$` by `$3r = 0.2528$`; `byKey.other-root`: replace `−156%` by `−158%`; `one-rate` unchanged.
   - `explain.text`: `Each year multiplies the balance, so $25{,}000(1 + r)(1 + 2r) = 31{,}320$, which expands to $2r^2 + 3r - 0.2528 = 0$. The formula gives $r = \tfrac{-3 \pm \sqrt{11.0224}}{4} = \tfrac{-3 \pm 3.32}{4}$. The positive root is $r = 0.08$, so the bond pays 8% and then 16%.`
   - Recomputed by bisection: roots 0.08 and -1.58; $9 + 8 \times 0.2528 = 11.0224 = 3.32^2$; $25{,}000 \times 1.08 \times 1.16 = 31{,}320$; slips $0.2528 / 3 = 0.08427$ and $\sqrt{1.2528} - 1 = 0.11929$. No hit for 31,320, 1.2528 or 11.0224 in the content.

## Checked and clean

- Keys and slips: all eight keys, every `wrong` value and every printed number agree on both scripts. No rounding tie; every band takes its printed value (2.69, 2.88, 6%) and refuses each slip; slips do not overlap.
- Units and form: `e-two-rates` carries unit "%" with `over100`; `e-parallelogram-midpoint` states two decimal places; `e-rebate-third` asks for pounds and prints £2.88; the set item names degrees and commas. No tail or table value is used.
- `e-read-the-change`: both curves stay inside the window; option c shares the lowest point and crosses at $2 \pm \sqrt2$; option d's lowest height is $-1$; option b sits at $x = -2$. Each `why` says so.
- `e-coefficients-in-step`: $n^2 - 9n + 14 = (n - 2)(n - 7)$; 7, 21, 35 rise by 14; $(1 + x)^2$ has no $x^3$ term.
- `e-left-hand-commands`: columns Y H N, U above J and P above the semicolon match `terminal/l1`.
- Voice: British spelling, no exclamation marks, no em-dashes, explanations of two or three sentences, £ for money.

Totals: 4 findings (1 high, 2 medium, 1 low), all with exact, recomputed fixes. After the fixes the author's script needs the new values for items 1 to 4.

## Fix pass

1. Fixed: `e-double-angle-roots` now $\sin 2x = \sqrt{3}\cos x$ (roots 60, 90, 120, 270; slips "60, 90, 270, 300" and "30, 90, 270, 330"), as written; recomputed by grid scan and by factorising. Id kept (the review gives none). Grep of `trig`, `counting`, `quadratics`, exams: no hit for the equation.
2. Fixed: `e-parallelogram-midpoint` now $(-4, 2)$ and $(3, 5)$, key $\sqrt{41} = 6.403124$, slips 2.24, 6.08, 41, as written; recomputed with complex numbers and exact fractions. No hit for the pair in the four folders.
3. Fixed: `e-desk-meetings` now ten points on a circle, triangles, key 120, slips 720, 240, 45, as written; id kept, title "Corners on a circle". The grep finds only `counting/l4` using $\binom{10}{3}$ as a leave-out illustration (a number coincidence, no shared story or task), so not deferred.
4. Fixed: `e-two-rates` now £25,000 to £31,320, key 8%, slips 8.43%, 11.93%, -158%, as written; roots 0.08 and -1.58 by bisection, $9 + 8 \times 0.2528 = 11.0224 = 3.32^2$. No hit for 31,320 or 1.2528.

Deferred 0, disputed 0. `topic-0.4` has no finding, untouched. Both scripts exit 0 (152 and 147 checks, no FINDING); item table in `docs/reports/exam-second-item-stage0.md` updated. Validator 0 errors; voice scan 0 and 0; `grade-all.mjs --file` 0 failures on topic-0.3 (30 widgets) and topic-0.2 (25); playthrough green with and without `--mobile` on both. Graded answers changed: 4 (the keys of the four items).
