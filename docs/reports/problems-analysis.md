# Problem sets: analysis levels 1 to 3 (brief `docs/briefs/chained.md`)

Files: `app/content/courses/analysis/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-analysis-numbers.py` (517 of 517 checks, exits 0).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-cube-root-twenty | 5 (4 / 1) | l1, l3 (and l4) | 5 |
| problems-1 | p-climbing-fractions | 5 (4 / 1) | l2, l4 | 4 |
| problems-1 | p-diagonal-fraction | 5 (4 / 1) | l5, l4 | 4 |
| problems-2 | p-sum-law-band | 5 (5 / 0) | l6, l7 | 4 |
| problems-2 | p-root-recursion | 5 (4 / 1) | l8, l6 | 5 |
| problems-2 | p-two-strands-cauchy | 5 (4 / 1) | l9, l10 | 4 |
| problems-3 | p-telescoping-tail | 5 (4 / 1) | l11, l12 | 4 |
| problems-3 | p-alternating-quarters | 5 (4 / 1) | l12, l13 | 5 |
| problems-3 | p-cube-root-greedy | 5 (4 / 1) | l12, l13, l14 | 4 |

Typed parts: 12 of 15 in each set. Every lesson of each level appears, every problem draws on two or more. Choice parts are judgements only (what a contradiction shows, which property, which test, what follows).

## Checks

1. Number script: 517 of 517, exit 0. Each numeric key is computed exactly (fractions, sympy) and by a brute search, float or mpmath run; every `wrong` value is recomputed from its named slip and shown outside the band; expression keys, accept forms and slips are tested by sympy; `numbers_lib.check_wrongs` on each set.
2. Validator: 0 errors; warnings 4522 before and after (no new warning on these files; `[key-length]`, `[tight-band]` and long-sentence warnings met while drafting were fixed).
3. Playthrough `--problems analysis/problems-<n> --local-cdn <pkgs>`: green on desktop and with `--mobile` for all three. Part screenshots at 440 px read: no overflow, fractions and sums wrap cleanly.
4. Voice scan 35 on the course folder: 0 and 0.
5. `grade-all --file` each set: 0 failures (45 widgets).

## Freshness

`fresh-check --file ... --cross-numbers`: 0 hard hits. Advisories, judged: set 1 shares the taught formula $s + \tfrac1n \in S$ with l3 (the proof step itself). Set 2: 21, 0.5714, 0.3333 with `conditional/problems-1` (coincidence: $\tfrac47$, $\tfrac13$); $|b_n - 2|$ and $|a_{n+1} - a_n|$ notation with l7 and l10. Set 3: powers of 2 (64, 256, 1024, 4096) with systems and other courses (coincidence); $|S - S_n| \le a_{n+1}$, the taught theorem.

Own-course grep (key numbers and setting of each problem, own folder first, then `app/content/`), after two rewrites:

- p-cube-root-twenty ($x^3 < 20$, 21/8, $-979$, 29.546875, 1.912109375, 16, $5q^3 = 2k^3$): 0 in analysis. First draft (cube root of 10, bisect [2, 3], left end after 3 halvings = 2.125) matched `review-1` r-bisect-sqrt3 in answer and question sentence; rewritten.
- p-climbing-fractions ($\tfrac{5n-4}{n+1}$, $\tfrac{9}{n+1}$, $\tfrac9\varepsilon - 1$, 2250): 0 in analysis. First draft used gap $\tfrac{7}{n+1}$ and threshold $\tfrac7\varepsilon$, as `exams/topic-1.10` does for $2 - \tfrac{7}{n+4}$; rewritten.
- p-diagonal-fraction (0.70329, 0.18096, 0.42571, 0.96053, 0.33418, 0.55445, 100001, 55446): 0 anywhere for the list and $x$. A draft $x = 0.5445$ matched the topic exam's diagonal slip; replaced before writing.
- p-sum-law-band ($\tfrac{6n+1}{2n+5}$, $\tfrac{2n-2}{n+1}$, 138, 80, 109, 0.09914): 0 in analysis.
- p-root-recursion ($\sqrt{4a_n + 21}$, $a_1 = 1$, $\sqrt{41}$, 6000, 14): 0 in analysis. The planned $\sqrt{3a_n + 10}$ is the topic exam's recursion; replaced before writing.
- p-two-strands-cauchy ($(-1)^n(2 - \tfrac3n)$, 3.071, 6): 0 anywhere.
- p-telescoping-tail ($\tfrac{1}{(n+1)(n+3)}$, $n^2 + 4n + 7$, 998): 0 anywhere; $\tfrac5{12}$ is common elsewhere (other courses, unrelated).
- p-telescoping-tail is review-3's $\tfrac{2}{n(n+2)}$ series with the index moved by one and halved; kept on the reader's judgement (second read of problems analysis 1 to 3, close cousin, sum, tail and comparison parts new).
- p-alternating-quarters ($(-1)^{n+1}\tfrac{n}{4^n}$, $\tfrac5{1024}$, $\tfrac{327}{2048}$): 0 in analysis. $\sum \tfrac{n}{3^n}$ (taylor homework-3) was avoided.
- p-cube-root-greedy ($\sum \tfrac{(-1)^{n+1}}{\sqrt[3]{n}}$, $T = 0.2$, 0.2063, $-0.4237$, 0.2697): only l3's $\sqrt[3]5$ shares the symbol. $\sum \tfrac{(-1)^{n+1}}{\sqrt n}$ (l13, l14, review-3) was avoided.

Hits outside analysis (2.625, 15.45, 2250, 6.403, 0.2063 and the like) are single numbers in unrelated settings.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems analysis)".

# Problem sets: analysis levels 4 and 5 (brief `docs/briefs/chained.md`, prompts `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/analysis/problems-4.json`, `problems-5.json`. Numbers: the same script, `docs/reports/problems-analysis-numbers.py`, extended (section "Levels 4 and 5"). The `reuse` findings of `docs/reviews/review-problems-analysis-1-3.md` (same interval and count as a review screen; same limits, band and asks as a lesson) were read first: every setting below was grepped against the course folder and the topic exam before writing, and three drafts were changed (listed under Freshness).

## Level 4 (continuity and the derivative)

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-cubic-bracket | 5 (5 / 0) | l18, l15, l16 | 4 |
| problems-4 | p-quartic-roots | 5 (4 / 1) | l17, l18, l16 | 3 |
| problems-4 | p-bump-series | 5 (4 / 1) | l19, l15 (l18 for the peak) | 5 |

Typed parts 13 of 15 (one numeric set, two `expression`). Choice parts are judgements: what Rolle's theorem allows, what uniform convergence gives. Skills: `an-continuity`, `an-reals`, `an-calculus`, `an-sequences`, all carried by l15 to l19.

Chains. p-cubic-bracket: mean value point $c = \tfrac{2}{\sqrt3}$, then the slope bound $K = 18$ (the chord slope 10 of part 1 is a slip), then $\delta = 0.0005$ for $\varepsilon = 0.009$, then 12 halvings of $[0, 2]$, then $|f(m)| \le \tfrac{9}{2048}$ at the last midpoint. p-quartic-roots: zeros 0 and 2 of $h'$, maximum 12 at the end point (the critical-only slip 3 has a line), minimum $-13$, Rolle caps the roots at three, the sign changes give exactly 3. p-bump-series: peak $\tfrac{1}{k^2}$, $M_k = \tfrac{1}{ek^2}$, $N = 37$ from the M-test tail $\tfrac{1}{eN}$, uniform limit continuous, then the $\tfrac{\varepsilon}{3}$ proof at 0 with $\delta = \tfrac{1}{3700}$.

Claims checked in the script beyond the keys: the real 12-halving midpoint obeys the bound; $h$ has roots near $-0.63$, 0.63, 2.76 only; the true tail after 37 terms is below 0.01 near its peak; $|S(x) - S(0)| < 0.02$ inside the window; $S_{37}(x) \le 37x$.

### Freshness, level 4

Own-course grep of each problem's key numbers, formulas and nouns (course folder, then `app/content`):

- p-cubic-bracket ($x^3 + 6x - 13$, $[0, 2]$, 10, 18, 0.009, 0.0005, 12, $\tfrac{9}{2048}$, 1.155): 0 in analysis for the function, 0.009, $\tfrac{9}{2048}$ and 1.155; 0.0005 occurs only as a `tol`. Drafts: $x^3 + 4x - 7$ was dropped because `exams/stage-1` has $x^3 + 4x$ on $[1, 4]$; $[1, 2]$ was dropped because l16 and review-4 bisect on it. The halvings ask is l16's standard task with new numbers.
- p-quartic-roots ($x^4 - 8x^2 + 3$, $[-1, 3]$, 12, $-13$, 3 roots): 0 in analysis ($x^4$ only in homework-4's $x^4(1 - x)$). The count 3 matches l16's quiz ($x^3 - x$ on $[-2, 2]$, 3 roots) in answer only: that item reads the roots off; here Rolle bounds them. Judged acceptable.
- p-bump-series ($x e^{-k^2x}$, $\tfrac{1}{ek^2}$, 37, $\tfrac{1}{3700}$): 0 in analysis; $e^{-k^2}$ occurs only in `pdes` heat kernels. Draft: $x^2 e^{-kx}$ was dropped because its $k = 1$ peak $4e^{-2} \approx 0.5413$ is `limits/homework-4`'s answer. `fresh-check` advisory: the tail $\sum_{k > N} \tfrac{1}{k^2}$ with l19 (the M-test screen), a taught formula.

`fresh-check --file problems-4.json --cross-numbers`: 0 hits, 1 advisory (above).

## Checks, level 4

1. Number script: exit 0 (every key two ways, every `wrong` from its slip and outside the band, stated figures, set shape).
2. Validator: 0 errors, no warning on the file (one `[shown-arithmetic]` and two long-sentence warnings met while drafting were fixed).
3. Playthrough `--problems analysis/problems-4 --local-cdn <pkgs>`: green, and green with `--mobile`. Part shots at 440 px read: no overflow.
4. Voice scan 35, course folder: 0 and 0.
5. `grade-all --file problems-4.json`: 0 failures (15 widgets).

## Level 5 (integration and metric spaces)

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-5 | p-root-sums | 5 (5 / 0) | l20, l21 | 3 |
| problems-5 | p-diamond-ball | 5 (4 / 1) | l22, l23 | 4 |
| problems-5 | p-accumulated-cubic | 5 (4 / 1) | l21, l24, l23 | 5 |

Typed parts 13 of 15 (one numeric set, two `expression`). Choice parts are judgements: in which metrics the set is open, why a supremum on $[0, 5)$ is no contradiction. Skills: `an-calculus`, `an-metric`, `an-continuity`, all carried by l20 to l24.

Chains. p-root-sums: $U_4 \approx 6.1463$ for $\sqrt{x}$ on $[0, 4]$, the telescoped gap $\tfrac8n$, the integral $\tfrac{16}{3}$ by part two, $U_4 - \tfrac{16}{3} \approx 0.8129$ inside the gap 2, then $n = 401$ for a gap below 0.02. p-diamond-ball: $d_1(0, p) = 0.7$ at $p = (0.2, -0.5)$, the room 0.3 by the triangle inequality, then the disc radius $\tfrac{0.3}{\sqrt2} \approx 0.2121$ from $d_1 \le \sqrt2\,d_2$ and the square radius 0.15 from $d_1 \le 2\,d_\infty$, so $U$ is open in all three. p-accumulated-cubic: $F(x) = \tfrac{x^3}{3} - 2x^2 + 3x$ by part two, critical points 1 and 3 by part one, maximum $\tfrac{20}{3}$ at the end point of the compact $[0, 5]$ (the critical-only slip $\tfrac43$ has a line), $[0, 5)$ not closed so not compact, then $n = 2667$ from $|F(5) - F(x_n)| \le \tfrac8n$.

Claims checked in the script beyond the keys: $L_4 < \tfrac{16}{3} < U_4$; the disc radius equals the distance from $p$ to the edge $y_1 - y_2 = 1$; the square's corner $(0.35, -0.65)$ lies on the edge of $U$; $|f| \le 8$ on $[0, 5]$ with the maximum at 5; no point of $[0, 5)$ reaches $\tfrac{20}{3}$; the true gap at $n = 2667$ is below 0.003.

### Freshness, level 5

- p-root-sums ($\sqrt{x}$ on $[0, 4]$, 6.1463, $\tfrac8n$, $\tfrac{16}{3}$, 0.8129, 401): 0 in analysis for the setting and the figures; 401 occurs in l7 (a sum-law index, unrelated). $\sqrt{x}$ appears in review-5 on $[0, 1]$ for uniform continuity, a different task. The sums and the gap are l20's standard tasks on a new function and interval.
- p-diamond-ball ($U = \{|y_1| + |y_2| < 1\}$, $(0.2, -0.5)$, 0.7, 0.3, 0.2121, 0.15, $(0.35, -0.65)$): the diamond is l22's taxicab unit ball (a definition screen), and the ask "largest $r$ with a ball inside" is l23's, there for the disc and square at $(0.6, 0.7)$ and review-5's disc at $(0.3, 0.4)$. Here the set is the diamond, the point and every number are new, and parts 3 and 4 use the comparison of metrics, which no screen does. Judged the same standard task in its own setting. `fresh-check` advisories: the $d_\infty$ formula with l22's quiz (a definition), and ten single-number triples (0.2, 0.35, 0.65, 0.15, 0.3, 0.7) with other courses, coincidence.
- p-accumulated-cubic ($t^2 - 4t + 3$ on $[0, 5]$, $\tfrac{x(x - 3)^2}{3}$, $\tfrac{20}{3}$, 2667, $5 - \tfrac1n$): 0 in analysis. $x^2 - 4x + 3$ occurs in l18 as the mean value $g$ for $x^2$ on $[1, 3]$, a different role (here it is integrated); kept, and listed for the reader. l24's portfolio screen (supremum 0.08 not attained on strictly positive weights) is the same idea in another setting.

`fresh-check --file problems-5.json --cross-numbers`: 0 hits, 24 advisories (above).

## Checks, level 5

1. Number script: exit 0, 1003 of 1003 checks for levels 1 to 5 (levels 4 and 5 add set shape and numeric-set checks).
2. Validator: 0 errors, no warning on the file.
3. Playthrough `--problems analysis/problems-5 --local-cdn <pkgs>`: green, and green with `--mobile`. Part shots at 440 px read: no overflow.
4. Voice scan 35, course folder: 0 and 0.
5. `grade-all --file problems-5.json`: 0 failures (15 widgets).

## Engine limits, levels 4 and 5

One bullet in `docs/BACKLOG-INBOX.md` under "Raised later (problems analysis):" (levels 4 and 5).
