# topology levels 1 and 2: second-reader findings

Scope: `l1-many-distances` to `l8-connectedness`, `review-1`, `review-2`, `homework-1`, `homework-2` in `app/content/courses/topology/`.

Method: every file flattened and read in full. Stated numbers and wrong-option values recomputed in a scratch script (gamma formula against a 400,000-strip midpoint sum, bisection for the calibration ends, the four edge distances, brute force over all families on 0 to 3 points for topology, connected and homeomorphism-class counts, the midpoint `ball_area` errors). Every code widget run in CPython: each solution passes all hidden tests and examples, each starter fails (l1 10 tests, l5 11, l6 10, l7 10, l8 8, homework-1 7, homework-2 4; slowest case 4 ms). Each distractor's `why` and `byKey` line re-derived from the learner action it names.

Checks run:

- `python3 docs/reports/topology-L1-numbers.py`: exit 0, 177 of 177 checks.
- `python3 docs/reports/topology-L2-numbers.py`: exit 0, 141 of 141 checks.
- Not checked by those scripts: the chain in finding 8 (the script checks the constants 1, 2 and $\sqrt2$ one by one, not the chain); the four edge distances listed in homework-1 item 2 and its `other-edge` line (finding 19: the script checks only the minimum); the "within $10^{-6}$" claim (finding 20: the script asserts $2 \times 10^{-6}$); and the prose claims in findings 9, 11 and 14.
- `node tools/validate.mjs`: 0 errors. Level 1 and 2 warnings are only "a problem screen without a canvas before the ladder ends" (l2 s6, s7; l3 s5, s6; l4 s5, s6; l7 s5; l8 s5, s7), all proof-only `order` screens. No `[table-slip-key]` warning on any topology file. No O2 warning on level 1 or 2 files.
- `VOICE_BASE=app/content/courses/topology python3 docs/reviews/voice-scan.py`: 0 sentences over 20 words, 0 explanations over three sentences.
- No em-dash, exclamation mark or listed American spelling in level 1 or 2 prose (`center` occurs only as `"align": "center"`).

Every other stated number recomputes: the eight hook distances; areas 2, 3.1416, 3.5333, 3.7081, 4 and $\tfrac23$; 2.2361, 3, 2; 0.7071; 1.5, 0.8660, 0.5 and the volumes; 4 for $d_{0.5}$; 1.2599; 2.8284; 0.30, 0.15, 0.1732, £600,000, £300,000; 0.5, 0.3, 0.6, 0.2121; $-0.5$, $-\tfrac13$, $-0.1111$; £7.9656, 0.199860, 0.200364; 1, 1, 4, 29 (and 355 as stated); 9 generated sets, the subbasis topology, the Sierpiński subspace, 5 and 4 generated sets; 0.4082, 0.8165; 0.7071, 0.8944, 0.4472, 0.2236; $f(0.5) = 1$, $f(0.75) = 3$, $f(-0.9) = -9$, $f(-0.75) = -3$, $g(\pm 3) = \pm 0.75$, $-0.4286$; 3 and 9 classes; 0.5493, $-1.4722$, 0.7616; 1, 1, 3, 19 connected; 0.6 and both 7% portfolios; 0.75 and 0.48; exactly 1 relabelling; $\tfrac{0.7}{\sqrt2} \approx 0.4950$, 0.6364; constants 7, 4, 5 and 3; $c = 1$ and 0.3333 for the bounded metric; `ball_area` 2.0, 3.1415928, 3.5332781, 3.7081506 and 3.4641.

Severity: wrong = a false statement or number; misleading = true but liable to teach the wrong thing, or a claim missing its hypothesis; voice = style rule or grammar; layout = presentation.

Counts: 3 wrong, 14 misleading, 3 voice, 1 layout (21 findings).

## Findings

1. **l1-many-distances.json**, `screens[2].prose` | misleading
   - Problem: the axiom recall says a metric "is zero only for equal points". That is only $d(x, y) = 0 \Rightarrow x = y$; it drops $d(x, x) = 0$.
   - Fix: replace "is zero only for equal points" with "is zero exactly when the points are equal".

2. **l1-many-distances.json**, `screens[11].explain.text` | voice
   - Problem: "can change answer with the metric" is ungrammatical.
   - Fix: "Matching today's market to its nearest day in history can change its answer with the metric, as `nearest` showed."

3. **l2-open-balls.json**, `screens[7].feedback.byKey.sum` | voice
   - Problem: "which fits in neither for sure" reads as "certainly fits in neither", which is false (a small $r_1 + r_2$ can fit).
   - Fix: "Adding radii gives a bigger ball, which need not fit in either set."

4. **l2-open-balls.json**, `quiz[3]` | misleading
   - Problem: the quiz names two distances $d_1 = d(x_1, y)$ and $d_2 = d(x_2, y)$. In this lesson and l1, $d_1$ and $d_2$ are the taxicab and Euclidean metrics. The key $\min(r_1 - d_1, r_2 - d_2)$ then reads as a statement about those metrics.
   - Fix: write $e_1 = d(x_1, y)$ and $e_2 = d(x_2, y)$ in `quiz[3].prose`, and $e_1$, $e_2$, $e_k$ in `widget.options[0].text`, `widget.options[2].text` and `explain.text`.

5. **l3-closure-interior-boundary.json**, `screens[8].widget.options[2]` (`rim`) | misleading
   - Problem: in the discrete metric every $y \ne x$ is at distance exactly 1. So "$\{x\}$ together with the points at distance exactly 1" is $X$, the same set as option `all`. The choice offers one wrong set under two names.
   - Fix: replace the option with text "$X$, because every $y \ne x$ is a limit of points of $B(x, 1)$" and why "A sequence in $B(x, 1) = \{x\}$ is constant at $x$, so its only limit is $x$."

6. **l3-closure-interior-boundary.json**, `screens[10].question` | misleading
   - Problem: "Which set of $\rho$ gives an invertible matrix" has the answer $\mathbb{R} \setminus \{-0.5, 1\}$. At $\rho = 2$ the eigenvalues are 5, $-1$ and $-1$: the matrix is invertible but not a valid correlation matrix. The key $(-0.5, 1)$ is right only among valid $\rho$.
   - Fix: "Which valid $\rho$ give an invertible matrix, and what is that set to the valid set?"

7. **l4-continuity-by-open-sets.json**, `screens[5].widget.lines[4].why` | misleading
   - Problem: the example "$x^2$ maps $(-\infty, 0]$ and $[0, \infty)$ to the same set" uses two sets that are not complements of each other (they share 0). So it does not test the line $f(V^c) = (f(V))^c$.
   - Fix: "Images do not respect complements: $x^2$ sends $V = (0, \infty)$ to $(0, \infty)$, but $V^c = (-\infty, 0]$ to $[0, \infty)$."

8. **l4-continuity-by-open-sets.json**, `screens[6].prose` | wrong
   - Problem: the chain $|f(p) - f(q)| \le d_1(p, q) \le 2d_\infty(p, q) \le \sqrt2\, d_2(p, q)$ is false at its last link. It would need $\sqrt2\, d_\infty \le d_2$.
   - Evidence: $p - q = (1, 0)$ gives $2d_\infty = 2$ and $\sqrt2\, d_2 \approx 1.4142$. The brief carried the same chain.
   - Fix: "Take $f(x, y) = x + y$ from $\mathbb{R}^2$ to $\mathbb{R}$. Then $|f(p) - f(q)| \le d_1(p, q)$, and l1 gives $d_1 \le 2d_\infty$ and $d_1 \le \sqrt2\, d_2$." The answer $(\varepsilon, \tfrac{\varepsilon}{2}, \tfrac{\varepsilon}{\sqrt2})$ stays right.

9. **l5-topologies.json**, `screens[5].widget.lines[4].why` and `screens[5].feedback.byKey.d1` | misleading
   - Problem: both say that with $r = d(x, y)$ "the midpoint of $x$ and $y$ lies in both" balls. A general metric space has no midpoint. In the discrete metric $B(x, 1) = \{x\}$ and $B(y, 1) = \{y\}$ are disjoint, so the line is flawed because it can fail, not because it always does.
   - Fix: why "The balls may overlap: in $\mathbb{R}$, $B(0, 1)$ and $B(1, 1)$ share $(0, 1)$."; byKey "You used the whole distance. The balls can then overlap, as $B(0, 1)$ and $B(1, 1)$ do in $\mathbb{R}$."

10. **l5-topologies.json**, `screens[7].widget.options[1]` (`fin`) | misleading
    - Problem: the option says "Finite sets are not open" and its why opens "True". But $\varnothing$ is finite and open in the cofinite topology.
    - Fix: option text "Non-empty finite sets are not open."

11. **l7-homeomorphisms.json**, `screens[1].prose` | misleading
    - Problem: "Both are continuous away from 0, and both fix 0" is given as the reason the radial map is a homeomorphism. Fixing 0 does not give continuity at 0.
    - Fix: replace that sentence with "Both are continuous away from 0 by their formulas. At 0 they are too, since $d_2(0, P') = d_\infty(0, P)$ and $d_\infty \le d_2 \le \sqrt2\, d_\infty$."

12. **l7-homeomorphisms.json**, `screens[3].prose` | voice
    - Problem: "An expression grader samples only positive inputs" talks to the learner about the app's grader, a note meant for authors (shared rules).
    - Fix: "For $y \ge 0$, $\tfrac{y}{1 + |y|}$ and $\tfrac{y}{1 + y}$ agree. A negative input tells them apart."

13. **l7-homeomorphisms.json**, `screens[9].widget.how` | misleading
    - Problem: "Five test are_homeomorphic: ... and two three-point chains. Two more pair a chain with ..., and spaces of different sizes" reads as seven `are_homeomorphic` tests. There are five.
    - Fix: "Five test are_homeomorphic: the two Sierpiński spaces, Sierpiński against discrete, two three-point chains, a chain against $\{\varnothing, \{a\}, \{b, c\}, X\}$, and spaces of different sizes."

14. **l8-connectedness.json**, `screens[6].explain.text` | misleading
    - Problem: "Together with the last proofs, the connected subsets of $\mathbb{R}$ are exactly the intervals." The lesson proves only that $[a, b]$ is connected. Open, half-open intervals and rays need one more step (a union of connected sets through a common point, which homework-2 item 0 proves).
    - Fix: replace the second sentence with "Every interval is a union of closed intervals through one point, so it is connected (homework 2 proves that step). So the connected subsets of $\mathbb{R}$ are exactly the intervals."

15. **l8-connectedness.json**, `quiz[0].feedback.byKey.one` | misleading
    - Problem: "The Sierpiński spaces are connected too: $\{b\}$ is not open there." In the Sierpiński space $\{\varnothing, \{b\}, X\}$, $\{b\}$ is open.
    - Fix: "The Sierpiński spaces are connected too: each has only one open singleton."

16. **review-1.json**, `items[1].explain.text` | misleading
    - Problem: "A larger diamond has corner $(r, 0)$ outside the disc." The corner $(r, 0)$ is not in the open diamond $B_1(0, r)$, so it proves nothing.
    - Fix: second sentence "For $r > 1$ the diamond holds $(1, 0)$, which is outside the open disc, so $r = 1$."

17. **review-1.json**, `items[6].widget.options[2].why` | misleading
    - Problem: "$\{0\}$ is $f(V)$ inside $V$, an image." But $f(V) = \lfloor(-0.5, 0.5)\rfloor = \{-1, 0\}$, since $\lfloor -0.3 \rfloor = -1$. The line is hard to parse and names a wrong set.
    - Fix: "You found the values of $f$ that lie in $V$, which is image thinking. The preimage is every $x$ with $\lfloor x \rfloor \in V$."

18. **review-2.json**, `items[6].explain.text` | misleading
    - Problem: "The other three have too few open sets." The cofinite topology on $\mathbb{Z}$ has infinitely many open sets; the reason is that they all meet.
    - Fix: second sentence "In the other three, any two non-empty open sets meet."

19. **homework-1.json**, `items[2].explain.text` and `items[2].feedback.byKey.other-edge` | wrong
    - Problem: the explanation lists the four edge distances from $(0.2, 0.1)$ as $\tfrac{0.7}{\sqrt2}$, $\tfrac{0.9}{\sqrt2}$, $\tfrac{0.9}{\sqrt2}$, $\tfrac{1.3}{\sqrt2}$. The byKey line says $\tfrac{0.9}{\sqrt2}$ is the distance to "$-x + y = 1$ or $x - y = 1$".
    - Evidence: $|-0.2 + 0.1 - 1| = 1.1$, so the edge $-x + y = 1$ is $\tfrac{1.1}{\sqrt2} \approx 0.7778$ away. Only $x - y = 1$ gives $\tfrac{0.9}{\sqrt2} \approx 0.6364$. The four are 0.4950, 0.6364, 0.7778 and 0.9192.
    - Fix: explain "From $(0.2, 0.1)$ the distances are $\tfrac{0.7}{\sqrt2}$, $\tfrac{0.9}{\sqrt2}$, $\tfrac{1.1}{\sqrt2}$ and $\tfrac{1.3}{\sqrt2}$."; byKey "$\tfrac{0.9}{\sqrt2}$ is the distance to $x - y = 1$. The edge $x + y = 1$ is nearer."

20. **homework-1.json**, `items[7].explain.text` | wrong
    - Problem: "Each lies within $10^{-6}$ of the gamma formula."
    - Evidence: at 20,000 strips the errors are 0, $1.2 \times 10^{-7}$, $6.1 \times 10^{-7}$ and $1.21 \times 10^{-6}$ for $p$ = 1 to 4. The author's script asserts $2 \times 10^{-6}$.
    - Fix: "Each lies within $2 \times 10^{-6}$ of the gamma formula."

21. **All level 1 and 2 files**, `choice` widgets | layout
    - Problem: 55 of the 59 `choice` widgets put the correct option first and have no `shuffle` (`choice.js` shuffles only on `shuffle: true`). A learner soon learns that the first option is right.
    - The 55: l1 `quiz[0]`; l2 `screens[3]`, `[8]`, `[9]`, `[10]`, `quiz[2]`, `quiz[3]`; l3 `screens[3]`, `[8]`, `[10]`, `quiz[0]`, `[1]`, `[2]`; l4 `screens[2]`, `[7]`, `[8]`, `[9]`, `quiz[1]`, `[2]`; l5 `screens[2]`, `[6]`, `[7]`, `[8]`, `[11]`, `quiz[0]`, `[2]`; l6 `screens[1]`, `[3]`, `[4]`, `[7]`, `[8]`, `quiz[0]`, `[2]`; l7 `screens[2]`, `[8]`, `quiz[0]`, `[1]`; l8 `screens[1]`, `[2]`, `[6]`, `[8]`, `[9]`, `quiz[1]`, `[2]`; review-1 `items[4]`, `[5]`, `[6]`, `[8]`; review-2 `items[0]`, `[2]`, `[3]`, `[4]`, `[5]`, `[8]`; homework-2 `items[3]`.
    - None of them has ordered options.
    - Fix: add `"shuffle": true` to each.
    - Engine note: this is app-wide (3,373 of 6,605 lesson `choice` widgets have the key first and no shuffle), so a validator warning (key at index 0, no `shuffle`, options not ordered) would catch it before the next wave.

## Not findings

- Brief deviations that keep the teaching intact: the l2 hook grades the three fits in a `table` rather than a slider with `tol`; the l7 letters screen labels the junctions rather than tapping them (the report says so).
- l7 `screens[8]` draws $h(t_6)$ at $x = 0.9862$ ($\cos\tfrac16 = 0.98614$); this is only a canvas coordinate and is not visible at plot scale.
- The reader did not run the playthrough; the author reports green at desktop, `--mobile` and `--tablet`.

## Fix pass

1. fixed: "is zero exactly when the points are equal".
2. fixed: "can change its answer with the metric".
3. fixed: "which need not fit in either set".
4. fixed: `e_1`, `e_2`, `e_k` in the prose, options 0 and 2 and the explanation of l2 `quiz[3]`.
5. fixed: option `rim` now reads "$X$, because every $y \ne x$ is a limit of points of $B(x, 1)$", with the reviewer's why.
6. fixed: "Which valid $\rho$ give an invertible matrix, and what is that set to the valid set?".
7. fixed: the line now uses $V = (0, \infty)$ and $V^c = (-\infty, 0]$; $x^2$ sends them to $(0, \infty)$ and $[0, \infty)$, which are not complements.
8. fixed: l4 prose now says $|f(p) - f(q)| \le d_1$, $d_1 \le 2d_\infty$, $d_1 \le \sqrt2\, d_2$. Recomputed: at $(1, 0)$, $d_1 = 1$, $2d_\infty = 2$, $\sqrt2\, d_2 = 1.4142$, and the old link $2d_\infty \le \sqrt2\, d_2$ fails (2 > 1.4142). The $\delta$ values $\varepsilon$, $\tfrac{\varepsilon}{2}$, $\tfrac{\varepsilon}{\sqrt2}$ stand. One-line note added to `docs/briefs/topology.md` under the l4 bullet.
9. fixed: line `d1` why and byKey `d1` reworded with $B(0, 1)$ and $B(1, 1)$ sharing $(0, 1)$ in $\mathbb{R}$.
10. fixed: "Non-empty finite sets are not open."
11. fixed: continuity at 0 now argued from $d_2(0, P') = d_\infty(0, P)$ and $d_\infty \le d_2 \le \sqrt2\, d_\infty$ (checked at seven points in the L2 script).
12. fixed: "For $y \ge 0$, ... agree. A negative input tells them apart."
13. fixed: five `are_homeomorphic` tests listed; the sentence was trimmed ("two chains", "different sizes") to stay at 19 words, since the reviewer's wording is 22. The script counts exactly five such tests.
14. fixed: second sentence replaced as suggested.
15. fixed: "each has only one open singleton".
16. fixed: "For $r > 1$ the diamond holds $(1, 0)$, which is outside the open disc, so $r = 1$."
17. fixed: the image option's why now names the preimage as every $x$ with $\lfloor x \rfloor \in V$. Recomputed $f((-0.5, 0.5)) = \{-1, 0\}$.
18. fixed: "In the other three, any two non-empty open sets meet."
19. fixed: explain and byKey `other-edge` corrected. Recomputed from $(0.2, 0.1)$: $x + y = 1$ gives 0.7, $x - y = 1$ gives 0.9, $-x + y = 1$ gives 1.1, $-x - y = 1$ gives 1.3, each over $\sqrt2$: 0.4950, 0.6364, 0.7778, 0.9192. The graded answer 0.495 is unchanged.
20. fixed: "within $2 \times 10^{-6}$". Recomputed at 20,000 strips: the largest error (p = 4) is between $10^{-6}$ and $2 \times 10^{-6}$.
21. fixed for the 55 named `choice` widgets (`"shuffle": true`; l1 1, l2 6, l3 6, l4 6, l5 7, l6 7, l7 4, l8 7, review-1 4, review-2 6, homework-2 1). Deferred to the engine: the validator warning for key-first unshuffled choices.

Counts: 21 fixed, 0 disputed, 0 deferred findings (the engine warning in 21 is the one deferred part). Graded answers changed: 0.

Number scripts: both now check the l4 chain as an inequality at 53 points including (1, 0) and that the old link fails there, all four homework-1 item 2 edge distances with the text and byKey, the p = 1 to 4 errors against $2 \times 10^{-6}$ (and above $10^{-6}$), plus the review-1, l7, l8 and review-2 claims. `topology-L1-numbers.py` 184 of 184 and `topology-L2-numbers.py` 141 of 141, both exit 0.

Gates: `validate.mjs` 0 errors; voice scan 0 and 0; playthrough with `--local-cdn` green for l1 to l8, review-1, review-2, homework-1 and homework-2, desktop and `--mobile` (24 of 24 runs).
