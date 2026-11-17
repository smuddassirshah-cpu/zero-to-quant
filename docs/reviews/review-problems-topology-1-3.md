# Problem sets 3.4, topology levels 1 to 3: second-reader findings

Scope: `app/content/courses/topology/problems-1.json`, `-2`, `-3`: 12 problems, 49 parts (41 numeric, 6 `expression`, 2 choice), 103 `wrong` entries. Rules: `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md` (Reader, Author rules, Session AE additions), `docs/briefs/wave-c-author-ag.md` rules 1 to 6, `docs/briefs/wave-c-reader-ag.md` rules 1 to 5. No content edited; no browser.

## Verdict per problem

`clean` = a new chain on the level's skills. `reuse` = one sentence or step taken from the course, exact fix below. `re-author` = the problem walks several items in a row or retells a screen; the list says what not to walk, and no replacement text is given.

| set | problem | closest lesson screen | closest quiz, review, homework | closest exam item | verdict |
|---|---|---|---|---|---|
| 1 | `p-plotter-zone` | l4 screens[6] ($x + y$, a $\delta$ in three metrics); l2 screens[4] (largest $B_2$ in $B_1$) | `r1-delta-max`; `h1-delta-three-metrics`; `h1-disc-in-diamond` (distance to the edge $x + y = 1$) | `e-half-disc` | clean: the weighted metric changes every step and parts 2 and 3 join them |
| 1 | `p-cubic-band` | l4 screens[1] (preimage of $(-1, 4)$ under $x^2$); l3 screens[2] ($(0, 1] \cup \{2\}$) | `q-closed-preimage`; `r1-boundary-line`; `h1-punctured-plus-point` | `e-preimage-quadratic` ($x^2 - 4x$, $V = (-3, 5)$) | clean: a touching point and the interior point an open preimage misses are new |
| 1 | `p-diagonal-sphere` | l1 screens[3] (slide $p$); l1 screens[8] ($(0.6, 0.6)$ outside the diamond) | `q-disc-not-diamond` ($(0.6, 0.6)$); `q-square-in-diamond`; `r1-room-taxi` | `e-two-function-metrics` | clean: solving for $p$ and counting $p$ are new; note the diagonal point is 0.05 from l1's |
| 1 | `p-reciprocal-room` | l4 screens[1] | `q-one-open-preimage`; `r1-delta-max`; `h1-bounded-metric` | `e-preimage-quadratic` | clean |
| 2 | `p-four-point-line` | l6 screens[0] (pieces on $\{a, b, c, d\}$); l6 screens[5]; l7 screens[7] | `q-basis-count`; `r2-basis-count`; `h2-relabellings` (answer 1) | `e-four-point-topology` | reuse: part 1's question is the quiz and review sentence (finding 3) |
| 2 | `p-bond-yield-map` | l8 screens[11] (returns form $[4\%, 9\%]$, so 7% is attained, which weight gives it); l7 screens[2] (which map is the inverse) | `q-image-connected`; `r2-tell-apart`; `q-circle-line` | `e-homeomorphic-pairs` | re-author (finding 6) |
| 2 | `p-gapped-domain` | l8 screens[3]; l6 screens[7] | `h2-subspace-split` ($[0, 1) \cup \{2\}$); `r2-disconnected-domain`; `q-image-connected` | `e-connected-subsets` | clean: the counts of forced zeros and forced values are new; two wording faults (findings 4, 5) |
| 2 | `p-right-rays` | l5 screens[7] (cofinite, not Hausdorff) | `q-hausdorff-finite`; `r2-hausdorff`; `h2-cofinite-exercise` | `e-homeomorphic-pairs` | clean; definitions missing (finding 7) |
| 3 | `p-quadratic-iteration` | l13 screens[1], [3], [4], [5] | `q-golden`; `r3-apriori`, `r3-constant`; `h3-use-it` | `e-plane-contraction` | re-author (finding 8) |
| 3 | `p-input-output` | l12 screens[6] | `q-apriori-bound`; `r3-apriori`; `h3-report-code` | `e-plane-contraction` | re-author (finding 9) |
| 3 | `p-dyadic-points` | l9 screens[8]; l6 screens[4]; l11 screens[1] | `q-arctan-tail`; `r3-compact-which`; `h3-arctan-tail` | `e-compact-subsets`, `e-log-metric` | re-author (finding 10) |
| 3 | `p-cube-delta` | l10 screens[5] ($\delta = \varepsilon^2$ for $\sqrt x$) | `q-which-compact`; `r3-image` ($x^2$ on $[-1, 2]$); `r1-delta-max` | `e-max-on-circle` | reuse: part 3's sentence (finding 11); part 4 off the chain (finding 12) |

Re-author: 4 of 12 (`p-bond-yield-map`, `p-quadratic-iteration`, `p-input-output`, `p-dyadic-points`). Three sit in level 3, where the lessons already compute what the problems compute.

## Method

The author's script was run first. Every screen and quiz of l1 to l13, `review-1` to `-3`, `homework-1` to `-3` and the 13 `tg-` items of `exams/topic-3.4.json` (no other exam carries a `tg-` skill) were read as learner text (`review-problems-topology-1-3-scripts/taught.py`), and the screens named in the table in full. Each part was solved by hand from its text and again in `docs/reports/problems-topology-numbers-read.py`, which imports nothing from the author's script and uses the standard library only: direction scans for the metric constants, grid scans for the preimage and its boundary, bisection for every root and radius, brute force over the unions, subspaces and 24 bijections of the four-point space, loops for every "smallest $n$", plain iteration of both maps, 40,000 random pairs for the $d_1$ constant. Each of the 103 `wrong` values was rebuilt from the slip its line names. Every typed part then went through the engine's graders in node (`grade-probe.mjs`: the key at the asked places, a true minus sign, each `accept` form, each `wrong` entry on its own key, 77 strings of my own). Each claim was read for its hypotheses: $\mathcal{B}$ is a basis (covers $X$; $\{a, b, c\} \cap \{c, d\} = \{c\}$ is a piece); the right rays form a topology; $P$ is a bijection onto $(0, \infty)$; $g$ and $T$ map their sets into themselves ($g([0, 2]) = [\tfrac56, 1.5]$; $T$ sends the corners of $[0, 10] \times [0, 6]$ to points between $(1, 2)$ and $(9.6, 5.8)$); each closed set is in a complete space; each $V_n$ holds one point of $K$.

## Tool results

| check | result |
|---|---|
| author's script | `problems-topology-numbers.py` exit 0, every `numbers_lib` block passing |
| `problems-topology-numbers-read.py` | 771 checks, exit 0, 2 FINDING lines (findings 1 and 10), 2 NOTE lines |
| `grade-probe.mjs` | 278 checks, 77 reader rows, 0 failures |
| validator | 0 errors, 4567 warnings, none on the three files; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --files` (three sets) `--pairs` | 0 hits, 2 advisories (the $d_p$ formula of l1; the a priori bound of l12 screens[5], see finding 8) |
| `grade-all.mjs --file`, three sets | 16, 16 and 17 widgets, 0 failures |
| browser | not run (reader rule) |

Result. All 47 typed keys and both choice keys agree with mine, and so does every `wrong` value and every number printed in a feedback or explanation string ($1.14 \times 10^{-6}$, $7.6 \times 10^{-7}$, 36.33, 0.00109, 0.00098, 97.84, the two logarithms of $p^*$). No learner is marked wrongly: no `wrong`-tagged finding. No key or slip sits on a rounding tie, no slip band meets a key band, no percentage part exists, and every 4-place rounding is taken. Every "always" and "never" holds, and each theorem is used with its hypotheses met. The faults are of three kinds: retold course material (findings 3, 6, 8, 9, 10, 11), a part passable from its own stem (findings 4, 10), and terms the level does not define (findings 2, 4, 7).

Severities: wrong, misleading, reuse, voice, continuity.

## A. All three sets

1. `problems-1.json`, `problems-2.json`, `problems-3.json` | 13 strings in `feedback` and `explain` | voice | lesson references are written as code spans.
   Evidence: `` `l4` `` in `items[0].parts[1].explain` of set 1, and 12 more (5 in set 1, 3 in set 2, 5 in set 3). The course's lessons write the same course's lessons bare ("by l2", "(l9)") and keep code spans for another course (`` `analysis` l22 ``). No other problem set in the app uses the form.
   Fix: in each of the 13 places replace `` `lN` `` with `lN` (no backticks).

## B. `problems-1`

No finding beyond 1. Two notes, no change asked:
- `p-plotter-zone` `items[0].parts[3].explain`: "The nearest point is ..., above part 3's floor of 1.1926" says a point is above a floor. Optional rewording: "The nearest point is $y + 0.4(3, 1) = (3.7, 0.9)$. Its distance is $0.4\sqrt{10} = \tfrac{4}{\sqrt{10}} \approx 1.2649$, above part 3's floor of 1.1926." (first sentence kept).
- A slip worked from a 4-place restated value lands on the edge of its band (`multiplied` 5.9629 against 5.9628, `times-root` 0.1143 against 0.1142). The engine takes both, so nothing fails; 5.96292 typed in full falls to the generic line.

## C. `problems-2`

2. `problems-2.json` | `items[0].parts[3].question`, `.feedback.correct`, `.feedback.generic`, `.explain` (`p-four-point-line`) | continuity | "cut point" is not a term of level 2.
   Evidence: l7 screens[5] calls it "removing a point"; the words "cut point" first occur in `review-3` feedback. Part 4 opens "Using the 2 cut points $b$ and $c$ from part 3".
   Fix, question: "Using part 3, removing $b$ or $c$ disconnects $X$, and removing $a$ or $d$ does not. Call $b$ and $c$ the cut points. How many bijections $h : X \to X$ are homeomorphisms of $(X, \tau)$ onto itself?"

3. `problems-2.json` | `items[0].parts[0].question` (`p-four-point-line`) | reuse | the question is the sentence of l6 quiz `q-basis-count` and of `r2-basis-count`.
   Course: "How many open sets does it generate, $\varnothing$ included?" (both). Problem: "How many open sets does $\mathcal{B}$ generate, $\varnothing$ included?"
   Fix: "Count the sets of $\tau$, the empty set among them."

4. `problems-2.json` | `items[2].parts[1].question` (`p-gapped-domain`) | misleading | the part is passed from its stem, and "component" is defined by l8 for a finite space only.
   Evidence: the stem names "$[0, 1)$, $(1, 2]$ and $\{4\}$" as open with open complements, then asks how many components $Y$ has; the key 3 is the count of the sets just listed. l8 screens[10] defines a component as "the intersection of the clopen sets holding $x$" "on a finite space"; the problem's own definition comes only in the explanation.
   Fix, question: "Using part 1, four of the five sets are open in $Y$. A component of $Y$ is a largest connected subset. How many components does $Y$ have?" Feedback and explanation stand.

5. `problems-2.json` | `items[2].parts[3].question` (`p-gapped-domain`) | misleading | "the image of each contains $[-1, 2]$, $[-3, 1]$ and $\{5\}$" reads as each image holding all three.
   Fix: "Using the 3 components from part 2: $f([0, 1))$ contains $[-1, 2]$, $f((1, 2])$ contains $[-3, 1]$ and $f(\{4\}) = \{5\}$. What is the total length of the set of values that every such $f$ must take?"

6. `problems-2.json` | `items[1]` (`p-bond-yield-map`) | reuse | re-author: parts 2 and 3 retell l8 screens[11] in other nouns and numbers, and parts 1 and 4 are each one lesson step.
   Course, l8 screens[11]: "Long-only portfolios form the triangle of l6, which is connected. Expected return is continuous, so the attainable returns form an interval: $[4\%, 9\%]$. So 7% is attainable." then "What weight on the 9% asset gives 7%?"
   Problem, parts 2 and 3: "the yields from 2% to 5% form the connected set $[0.02, 0.05]$, so their prices form an interval", then "a price of £97 lies inside it. Which yield gives it?" The same three steps in the same order: a connected set of inputs, an interval of outputs, one value inside solved for its input. Part 1 is l7 screens[2] (name the inverse of a homeomorphism); part 4 is l7 screens[5] with `q-circle-line` (remove a point, count the pieces).
   Also: part 2 restates the inverse of part 1 and does not use it; part 4 asks for "components" of an infinite set (see finding 4); the difficulty is 3 and each part is one line.
   Not to walk: l8 screens[11]; l7 screens[2], [3], [5]; `q-image-connected`; `q-circle-line`; `r2-tell-apart`.

7. `problems-2.json` | `items[3].parts[0].question`, `items[3].parts[1].question` (`p-right-rays`) | misleading | closure and interior are asked in a space with no balls, and the course defines both by balls.
   Evidence: l3 screens[0] and [1]: a closure point is one where "every ball round it, however small, meets $A$"; "an **interior point** of $A$ has some ball inside $A$". Level 2 never restates either for a topology. l3 screens[5] proves "$\overline{A}$ is the smallest closed set holding $A$", which is what part 1 needs; the matching fact for interiors is not in the course. The stems give neither.
   Fix, part 1 question: "The closed sets are $\varnothing$, $\mathbb{R}$ and the rays $(-\infty, t]$. As in l3, the closure of a set is the smallest closed set holding it. The closure of $A = (1, 2) \cup \{5\}$ is $(-\infty, c]$. What is $c$?"
   Fix, part 2 question: "Using that the closed sets are left rays, so the open sets are right rays: the interior of a set is the largest open set inside it. The interior of $B = [3, 8] \cup (10, \infty)$ is a right ray. What is its left end?"

## D. `problems-3`

8. `problems-3.json` | `items[0]` (`p-quadratic-iteration`) | reuse | re-author: the five parts are `h3-use-it` and l13 screens[1] to [5] with another $g$.
   Course, `h3-use-it`: "$g(x) = \tfrac{1}{1 + x}$ on $[0.5, 1]$. It maps $[0.5, 1]$ into $[0.5, \tfrac23]$, and $|g'(x)| \le \tfrac49$ there, so $q = \tfrac49$", then the a priori count for $10^{-6}$, then "the true rate is $|g'(x^*)|$", then the fixed point from a quadratic with the root outside the interval as its slip ("1.618034 is the golden ratio, outside $[0.5, 1]$"). l13 screens[1], [3], [4], [5] run the same order for $\cos$: into itself, "$|g'(x)|$ is largest at the right end", the count 87, "near $x^*$ the true rate is the slope there".
   Problem: the image $[\tfrac56, 1.5]$ inside $X$; $q$ as the largest $|g'|$, at the right end; the count for $10^{-6}$; the fixed point from $x^2 - 6x + 5 = 0$ with the slip "5 ... lies outside $X$"; the rate $|g'(x^*)|$. Part 3's stem, "What is the smallest $n$ with $\tfrac{q^n}{1 - q}\,d(x_1, x_0) < 10^{-6}$?", is l12 screens[5] word for word (the fresh-check advisory), and its slip `q-half` gives 21, that screen's answer.
   The author's report calls this the course's exit task. That is so, and it is why a problem on l13 cannot run the lesson's five steps in the lesson's order.
   Not to walk: l13 screens[1], [3], [4], [5]; `h3-use-it`; l12 screens[5]; `q-golden`; `r3-apriori`; `r3-constant`.

9. `problems-3.json` | `items[1]` (`p-input-output`) | reuse | re-author: l12 screens[6] with the first column of its matrix changed.
   Course, l12 screens[6]: "$T(\mathbf{x}) = \mathbf{A}\mathbf{x} + \mathbf{b}$ on $\mathbb{R}^2$ with $\mathbf{A} = \begin{pmatrix} 0.6 & 0.6 \\ 0 & 0.3 \end{pmatrix}$ ... Not a contraction in $d_\infty$, but one in $d_1$", constant 0.9 from the column $0.6 + 0.3$, then "$x^*$, first coordinate".
   Problem: $\mathbf{A} = \begin{pmatrix} 0.5 & 0.6 \\ 0.2 & 0.3 \end{pmatrix}$, the same second column, the same $q = 0.9$ from the same sum, no contraction in $d_\infty$ but one in $d_1$, then the first coordinate of $\mathbf{x}^*$. Part 3's question, "What is the smallest $n$ whose a priori bound is below 0.001?", is `r3-apriori` word for word, tolerance included.
   The witness pair of parts 1 and 2 is new and sound, and can be kept in a new chain.
   Not to walk: l12 screens[6] (no matrix sharing a row or column with it, no $q = 0.9$); `r3-apriori`; `q-apriori-bound`; `e-plane-contraction` (constant, a priori count, first coordinate of the fixed point, in that order).

10. `problems-3.json` | `items[2]` (`p-dyadic-points`) | misleading and reuse | re-author: part 3 prints its own answer, and parts 1, 2 and 4 retell l9 screens[8].
   Printed target, `items[2].parts[2].question`: "Using part 1, all but 7 points of $K$ crowd into $U$. ... What is the smallest $N$ with $\sup_{m, n \ge N} |x_m - x_n| < 0.01$?" The key is 7. The reader's script prints this as a FINDING.
   Course, l9 screens[8]: "$K = \{0\} \cup \{1, \tfrac12, \tfrac13, \dots\}$ ... The member $U_0$ holding 0 holds all but finitely many $\tfrac1n$; one more member for each of those finishes." Problem: $K = \{0\} \cup \{2^{-n}\}$, "$U$ is needed for 0, and each of the 7 points outside $U$ needs its own $V_n$", and in part 4 "because $U$ swallows the tail". The same set with $2^{-n}$ for $\tfrac1n$ and the same two steps. Part 3 is the tail count of `q-arctan-tail` and `h3-arctan-tail` ("the smallest $N$ with tail width below"); part 4 is l11 screens[1] ($\tfrac1n$ Cauchy in $(0, 1]$ with its limit missing) and `r3-compact-which`.
   Not to walk: l9 screens[8]; l6 screens[4]; l11 screens[1]; `q-arctan-tail`; `h3-arctan-tail`; `r3-compact-which`. No part may restate a number that is its own key.

11. `problems-3.json` | `items[3].parts[2].question` (`p-cube-delta`) | reuse | the instruction is `r1-delta-max`'s sentence.
   Course: "Give the largest $\delta$ of the form $c\,\varepsilon$ that this bound guarantees." Problem: "give the largest $\delta = c\,\varepsilon$ this bound guarantees on all of $K$."
   Fix: "Using part 2, $f$ is continuous on the compact $K$. Since $|x^3 - y^3| = |x - y|\,|x^2 + xy + y^2|$, one $\delta$ serves every point of $K$. Give it in terms of $\varepsilon$, from the largest value of the second factor on $K$."
   Note, no change asked: part 2 shares the interval $[-1, 2]$ and the task with `r3-image` ($x^2$ there, $x^3$ here). The author declared it; the image, the slips and the next step differ.

12. `problems-3.json` | `items[3].parts[3]` (`p-cube-delta`) | continuity | part 4 restates $\delta = \tfrac{\varepsilon}{12}$ and then uses $\delta = 0.01$, which comes from nowhere.
   Fix: use part 3's own $\delta$ at $\varepsilon = 1$. Recomputed in the reader's script: $(x + \tfrac1{12})^3 - x^3 = \tfrac{x^2}{4} + \tfrac{x}{48} + \tfrac{1}{1728}$, root 1.958189, and $x + \tfrac1{12} = 2.041522$; the slope-only slip $\tfrac{x^2}{4} = 1$ gives 2.
   - question: "Using $\delta = \tfrac{\varepsilon}{12}$ from part 3, $\varepsilon = 1$ gives $\delta = \tfrac{1}{12}$ on $K$. On $[0, \infty)$, which is not compact, that $\delta$ fails. What is the smallest $x \ge 0$ with $(x + \tfrac{1}{12})^3 - x^3 \ge 1$? Give 4 decimal places."
   - `answer`: 1.958188652174248, `tol` 0.0001; `wrong`: `slope-only` value 2, `tol` 0.0001.
   - `feedback.correct`: "$(x + \tfrac{1}{12})^3 - x^3 = \tfrac{x^2}{4} + \tfrac{x}{48} + \tfrac{1}{1728}$. Setting it to 1 and solving the quadratic gives $x \approx 1.9582$."
   - `feedback.generic`: "Not quite. Expand $(x + \tfrac{1}{12})^3 - x^3$ and solve the quadratic for $x$."
   - `byKey.slope-only`: "You used only $3x^2 \cdot \tfrac{1}{12} = 1$, the slope term, which gives 2. The terms $\tfrac{x}{48}$ and $\tfrac{1}{1728}$ also count, which moves the root a little lower."
   - `explain`: "The pair $x \approx 1.9582$ and $x + \tfrac{1}{12} \approx 2.0415$ reaches just past the end of $K$, where part 3's $\delta$ was safe. Further out the gap only grows, and any other $\delta$ fails in the same way. The root of $\tfrac{x^2}{4} + \tfrac{x}{48} + \tfrac{1}{1728} = 1$ is $x \approx 1.9582$."
   The fixer adds the new key and slip to `problems-topology-numbers.py`; the reader's script already checks the root.

## Checks that found nothing

- Chain: every later part opens with "Using"; each lesson of each level is drawn on (l1 to l4; l5 to l8; l9 to l13); nothing beyond the level is needed apart from the terms of findings 2, 4 and 7.
- Skills: every `skills` id of each item is carried by a lesson of its level.
- Bands: each key at its asked places is taken, each of the 103 slips reaches its own line, 3-place roundings of 4-place keys are refused as the stems ask, `3/97`, `8/3`, `4/15` and `190/23` are taken, a lower-case `p` and `\epsilon` are taken in the expressions.
- Claims: $d_w \le \sqrt5\,d_2$ is sharp along $(2, 1)$; $h - 54 = (x + 3)^2(x - 6)$; $-3$ is an interior point of $A$ and the only one off $h^{-1}((0, 54))$; the left room $\tfrac{\varepsilon}{2(2 + \varepsilon)}$ binds for every $\varepsilon$, also past $\varepsilon = 2$; the identity is the only homeomorphism of the four-point space; $e^x$ is not onto and $-x$ is not continuous in the right-ray topology; 2 zeros and the values $[-3, 2] \cup \{5\}$ are forced and no more; no pair beats 0.9 in $d_1$ and $(0, 1)$, $(0, 0)$ reaches it.

## Engine

- `fresh-check` passes a stem that is another item's stem word for word when the surrounding numbers differ: "What is the smallest $n$ whose a priori bound is below 0.001?" (`r3-apriori` and `p-input-output` part 3) and "How many open sets does ... generate, $\varnothing$ included?" (`q-basis-count`, `r2-basis-count`, `p-four-point-line` part 1).
- `fresh-check` does not report a 2 by 2 matrix that shares a whole column with a course matrix and gives the same key from it (l12 screens[6] and `p-input-output`: column $(0.6, 0.3)$, $q = 0.9$).
- No rule finds a whole-number key printed in the part's own stem (`p-dyadic-points` part 3: "all but 7 points", key 7).
- No rule finds a lesson id in a code span (`` `l4` ``) in set text.

Inbox: four bullets under `Raised later (review problems topology):` in `docs/BACKLOG-INBOX.md`.

## Fix pass

Author agent (re-author and fix, brief `docs/briefs/reauthor-fix-af.md`). Every corrected number recomputed first, in `docs/reports/problems-topology-numbers.py`.

1. Lesson references as code spans: fixed in the 8 places left after re-authoring (5 in set 1, 1 in set 2, 2 in set 3; the other 5 sat in re-authored problems). Written in words ("the connectedness lesson", "the closure lesson"), as the session asked, rather than bare `lN`.
2. `p-four-point-line` part 4 "cut point": fixed, the reader's question exactly.
3. `p-four-point-line` part 1 question: fixed, the reader's text exactly.
4. `p-gapped-domain` part 2: fixed, the reader's question exactly; feedback and explanation stand.
5. `p-gapped-domain` part 4: fixed, the reader's question exactly.
6. `p-bond-yield-map`: re-authored as `p-signal-bands` (a price signal into $\{\text{sell}, \text{hold}, \text{buy}\}$: 5 sets with open preimage, 7 topologies making it continuous, 6 connected subsets, the hold argument as a choice). Walks none of l8 screens[11], l7 screens[2], [3], [5], `q-image-connected`, `q-circle-line`, `r2-tell-apart`.
7. `p-right-rays` parts 1 and 2: fixed, the reader's questions, with "As in l3" written "As in the closure lesson".
8. `p-quadratic-iteration`: re-authored as `p-kernel-equation` ($T(f)(x) = 1 + \tfrac{x}{2}\int_0^1 t f(t)\,dt$ on $C[0, 1]$: $q = \tfrac14$, $f^* = 1 + \tfrac{3}{10}x$, one step's error $\tfrac{1}{20}$, a posteriori bound over error $\tfrac53$). No a priori count, no into-itself image, no root outside the set, no true rate.
9. `p-input-output`: re-authored as `p-trapping-interval` ($T(x) = 0.2e^x$ on $[-r, r]$: $q = 0.2e^r$, the invariance line, smallest $r = 0.2711$, $x^* = 0.2592$). No matrix, no $q = 0.9$, no a priori count. The witness pair was not kept.
10. `p-dyadic-points`: re-authored as `p-coin-paths` (paths with $d = 2^{-k}$: 8 balls of radius 0.1, gap $\tfrac18$, 2 paths scoring $\tfrac58$, limit score $\tfrac23$). No set $\{0\} \cup \{x_n\}$, no tail count, no part prints its key.
11. `p-cube-delta` part 3: fixed, the reader's question exactly.
12. `p-cube-delta` part 4: fixed, the reader's replacement exactly (key 1.958188652174248, slip `slope-only` 2); added to the author's script, and the reader's check of the old key retargeted to the new one.

Notes under B: the optional rewording of `p-plotter-zone` part 4's explanation was not applied, since it would end the text on 1.1926, not the key, which `[working-band]` reads. Disputed: none. Deferred: none.

Reader's script: the checks of the four re-authored problems are removed (they no longer exist; a delta reader checks the new ones), cube part 4 now checks the fixed key; 541 checks, 0 FINDING lines, exit 0.

Gates: validator 0 errors, no warning on the three files; voice scan 35, 0 and 0; `fresh-check --file` 0 hits on each set (set 1 keeps its $d_p$ advisory); author's script 748 checks, 0 failures, numbers_lib 77, 66, 94 passing; `grade-all --file` 0 failures (16, 16, 16 widgets); playthrough `--problems` with `--why` and with `--mobile` green for all three sets, 440 px shots read.
