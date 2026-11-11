# Fluency sets: stat-learning (brief `docs/briefs/fluency.md`)

Levels 1 to 3 have no sets yet.

## Level 4 (sets for l15, l16, l17, l18)

### Lessons chosen

- `l15-widest-street`: the margin $\tfrac{1}{\lVert w \rVert}$, a decision value $w \cdot x + b$ and a point's distance $\tfrac{|w \cdot x + b|}{\lVert w \rVert}$, as screens 2 and 3 and quiz 1 work them.
- `l16-groups-nobody-labelled`: one assign and update step of k-means in one dimension, a group's sum of squares about its centre, and a merged group's distance under single, complete and average linkage.
- `l17-a-small-network`: a forward pass through two ReLU units, the parameter count $ab + b$ a layer, the slope $\partial L/\partial w_1 = (\hat y - y)\,w_2\,x$ and one gradient step.
- `l18-bending-the-line`: a one-knot linear spline's value, a two-knot spline's slope in a region, and the coefficient count ($K + 4$ cubic, knots $+ 2$ linear).

Considered and left out: `l19-which-learner` (choosing a learner is a judgement; its one formula, $t$ against a base rate, is drilled in the problem set instead). Kernels, $C$ and $\gamma$ in l15, the elbow in l16 and the scikit-learn fits are ideas or code, not hand calculations. The spline count leaves out `SplineTransformer`'s own column rule ($n_{\text{knots}} + \text{degree} - 1$, review finding 31), since the lesson teaches the count by interior knots.

### Sets

Four sets, 13 families. Decimal keys are asked to the places the lessons use (4 for a margin, 2 for a distance, 3 for a linkage height), with half a unit of tolerance; exact keys ask for "the exact value".

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l15-widest-street | margin | 189 | none (numeric) | gave-norm, street-width |
|  | decision-value | 199 | none | no-intercept, one-term |
|  | distance | 200 | none | no-norm, squared-norm |
| fluency-l16-groups-nobody-labelled | assign-and-update | 200 | none | all-shares, kept-centre |
|  | group-inertia | 200 | none | unsquared, averaged |
|  | linkage-distance | 185 | none | nearest, farthest, averaged (each `when` it is not the linkage asked) |
| fluency-l17-a-small-network | forward-pass | 200 | none | no-relu, no-output-bias |
|  | parameter-count | 186 | none | no-biases, units |
|  | slope-first-weight | 178 | none | slope-for-w2, dropped-w2 |
|  | one-step | 189 | none | uphill, no-rate |
| fluency-l18-bending-the-line | hinge-value | 200 | none | ignored-hinge (`when` past the knot), hinge-on-left (`when` before it), no-intercept |
|  | slope-in-a-region | 200 | none | coefficient-only, skipped-knot |
|  | coefficient-count | 79 | none | no-constant, knots-only |

Draw shapes: the k-means family draws the smallest value and four gaps, so the five values come sorted, and keeps only draws where no value is equidistant from the two centres (the lesson's tie rule is never needed) and each centre wins two or more. The forward pass keeps draws where one hidden unit is off and one on, so the ReLU always matters (284 of 484 draws rejected, under the 80% limit). The inertia family draws three gaps about a whole-number centre and sets the fourth, so the sum of squares is a whole number.

### Checks

1. `docs/reports/fluency-stat-learning-numbers.py` (new; 200 draws a family, shared checker `fluency_check.py`). Each key is rebuilt by a route of its own: the margin as the distance to a point placed on the edge; a point's distance by projection onto the line in NumPy; the k-means step by scikit-learn's `KMeans` run one iteration from the stated centres; inertia from `KMeans`; linkage heights from SciPy's `linkage`; the forward pass in NumPy; the slope by sympy's derivative, checked by a central finite difference; spline values and slopes from a sympy `Piecewise`; the coefficient count as the rank of a truncated-power basis on 400 points. Result: 7,800 checks over 13 families, 0 failures, exit 0. On its first run it caught three faults, each fixed by a `where`: two slips that coincided on some draws (decision value with $w_2 x_2 = b$, forward pass, hinge value), and a working step that printed $-\eta \times -9$.
2. From `app/`: validator 0 errors and no warning naming any of the four files; `node tools/test-fluency.mjs --local-cdn <pkgs> --set` green for each (304, 304, 308 and 304 checks).
3. `node tools/playthrough.mjs --fluency stat-learning/<set> --local-cdn <pkgs>`, with and without `--mobile`: green for all four; the 440 px shot of the two-unit network fits its prompt on three lines.
4. `VOICE_BASE=app/content/courses/stat-learning/ python3 docs/reviews/voice-scan.py 35`: 0 and 0.
5. I read 20 drawn items of every family (`fluency-sample.mjs --n 20`). Fixed while reading: "1 interior knots" (the count now starts at 2), a linkage pair that merged while a third share sat closer than they could be to each other (distances now 0.30 or more), a working sentence starting in lower case, "durations" for shares, and a `+ -3` in a working step. No `1x`, `+-`, `x^1`, `0x`, double minus or unreduced fraction, and no prompt that gives the answer away.
6. Engine limits: none new for this course, so nothing is added to `docs/BACKLOG-INBOX.md`. The one limit met this session (a picked phrase cannot hold a drawn number) is raised under the testing heading.
