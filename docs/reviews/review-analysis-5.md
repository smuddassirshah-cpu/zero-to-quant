# analysis level 5: second-reader findings

Scope: every file of `analysis` L5 in `app/content/courses/analysis/` (l20-riemann-integral, l21-fundamental-theorem-proved, l22-metric-spaces, l23-open-and-closed, l24-compactness, review-5, homework-5), against `docs/briefs/analysis.md` (preamble and Level 5), `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md`. The author's report `docs/reports/analysis-5.md` is not in this checkout (commit b53eaaa); the numbers script `docs/reports/analysis-L5-numbers.py` is. No earlier `docs/reviews/review-analysis*.md` exists, so no prior finding classes were carried over.
Method: ran the author's script (`python3 -I docs/reports/analysis-L5-numbers.py`); flattened every file to path = value text and read all of it; recomputed every stated number, distractor value, radius, distance and cover count independently (exact `Fraction` upper and lower sums, a brute-force 600-point-per-piece grid for the turning-point sums, closed forms with `math`); re-derived each distractor from its `why`/`byKey`; checked every definition and theorem statement for its hypotheses and every `order` widget for both a valid answer order and genuinely flawed distractors; checked byKey keys against option and wrong ids; ran every code widget's solution and starter against its examples and hidden tests in local CPython (own harness mirroring `equal`/`isclose`); scanned voice (`docs/reviews/voice-scan.py` with `VOICE_BASE=app/content/courses/analysis`, em-dash, `!`, American spellings, `$` money).
Scratch scripts (not committed): `/tmp/claude-0/-home-user-zero-to-quant/19ed1109-1b3b-5efa-bf90-8d56ce34a33f/scratchpad/review-an5/` (`flat.py`, `recompute.py`, `codecheck.py`, `keys.py`).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, mis-diagnosing distractor, missing hypothesis or teaching issue; note = style. Old strings are quoted as they appear in the JSON source (backslashes doubled).

## What the author's script does not check

- It checks 136 stated values at their JSON paths (much stronger than a hard-coded list) and 66 wrong-value bands, all passing. It does not open code `tests[].expect` values (for example homework-5 items[7]'s $\tfrac{616}{81}$, $\tfrac{38}{27}$, $\tfrac{3}{32}$): I recomputed all of them (correct).
- Numbers it leaves unchecked, all recomputed by hand and correct: l20 hints $\tfrac{30}{16}$, $\tfrac{14}{16}$, $U_{10} = 0.385$ in prose; l21 screens[1] $M = 4$ and width 0.4, screens[10] $\tfrac1\delta - 1$; l22 gaps 3 and 4, the detour $7 > 5$, quiz[1] $\sqrt2 \le 2$; l23 screens[2] hint 0.9220, screens[3] 0.4; l24 screens[10] $\tfrac{1}{\sqrt2}$, quiz[3] values 1 and 0; review-5 items[1] $\tfrac12$; homework-5 items[2] $\tfrac2x$, $\tfrac3x$, items[6] $d(1, 0) = 1$, $d(0, 1) = 2$, $d(0, \pi) = 0$, items[7] $\tfrac29$ and $\tfrac14$.
- It does not check the per cent semantics of `wrong[]` values under `unit: "%"` (l21 screens[11], below), qualitative claims and quantifiers ("only", "two things"), missing hypotheses (nonempty $K$), or whether an `order` widget's answer order is the only valid one (two are not, below).

## l20 bound (author's change from the brief)

- Verified. The brief's "$U - L < \varepsilon(b - a)$" (δ chosen for tolerance ε) and the author's "δ chosen for tolerance $\tfrac{\varepsilon}{b - a}$, so $U - L < \varepsilon$" are both correct proofs. The author's form matches the stated criterion ($U - L < \varepsilon$) directly and is used consistently in l20 screens[9], quiz[0] and homework-5 items[9]. With $b - a = 1$ the numbers are unchanged: $\delta = 0.005$, $n = 201$ against the exact 101 (recomputed with `Fraction`). No change needed.

## l20 (the Riemann integral defined)

- app/content/courses/analysis/l20-riemann-integral.json | quiz[1] explain | note | "$U \le \tfrac2n$" assumes $n$ equal pieces, but the quiz speaks of any partition and never names $n$. | Replace "Only the one or two pieces touching $\\tfrac12$ have top 1, so $U \\le \\tfrac2n$." with "With $n$ equal pieces, only the one or two touching $\\tfrac12$ have top 1, so $U \\le \\tfrac2n$."

## l21 (the fundamental theorem proved)

- app/content/courses/analysis/l21-fundamental-theorem-proved.json | screens[4] order (part one) | error | Lines p1 (the identity for the quotient minus $f(c)$) and p2 ("Let $\varepsilon > 0$. Continuity at $c$ gives $\delta$") are independent: p3 uses both, so p2, p1, p3, p4 is a valid proof graded wrong. | After `"distractors": ["d1"]` (line about 435) add `"same": [["p1", "p2"]]`, and in the prose replace "One line is flawed." with "One line is flawed, and two lines may come in either order."
- app/content/courses/analysis/l21-fundamental-theorem-proved.json | screens[8] order (part two) | error | t2 (telescope) and t3 (mean value theorem on each piece) are independent; t4 needs both. t1, t3, t2, t4, t5 is valid and graded wrong. | After `"distractors": ["d1"]` (line about 790) add `"same": [["t2", "t3"]]`, and in the prose replace "One line is flawed." with "One line is flawed, and two lines may come in either order."
- app/content/courses/analysis/l21-fundamental-theorem-proved.json | quiz[2] explain | warning | "Only a jump in $f$ makes a corner in $F$" is an unqualified general rule and false: $f = 0$ for $t < 0$ and $1 + \sin(1/t)$ for $t > 0$ has no one-sided limit at 0, yet $F$ has one-sided slopes 0 and 1 there (the average of $\sin(1/t)$ over $[0, h]$ is $O(h)$). | Replace "Only a jump in $f$ makes a corner in $F$." with "A jump in $f$, as in screen 7, does make a corner in $F$."
- app/content/courses/analysis/l21-fundamental-theorem-proved.json | screens[11] wrong `integral` (0.175) | warning | With `unit: "%"` the learner types per cent and the engine divides by 100. A learner who gives the integral types 0.175 (graded as 0.00175) and gets the generic line; the stored 0.175 fires only on 17.5, which the byKey text does not describe. | Change the `integral` entry's `"value": 0.175,` to `"value": 0.00175,` with `"tol": { "abs": 5e-06 }`, and keep byKey "You gave the integral itself, 0.175. The forward rate is its slope."
- app/content/courses/analysis/l21-fundamental-theorem-proved.json | screens[2] option `ok` text | note | The correct option uses $s$, which the question writes only as $\sup\{\dots\}$; $s$ is named a screen later. | Replace "The integrand is at most $s$ in size over a length $|h|$." with "Call that supremum $s$. The integrand is at most $s$ in size over a length $|h|$."
- app/content/courses/analysis/l21-fundamental-theorem-proved.json | screens[3] prose | note | "$s(h)$ is the largest $|f(t) - f(c)|$": $f$ need not attain it ($f$ is only continuous at $c$); screen 2 rightly says supremum. | Replace "where $s(h)$ is the largest $|f(t) - f(c)|$ for" with "where $s(h)$ is the supremum of $|f(t) - f(c)|$ for".
- app/content/courses/analysis/l21-fundamental-theorem-proved.json | screens[3] option `integ` why | note | "At a jump, $s(h)$ stays at the jump's size" holds only when $f(c)$ equals one side's limit; in general $s(h)$ stays at least the gap from $f(c)$ to the farther side. | Replace "At a jump, $s(h)$ stays at the jump's size." with "At a jump, $s(h)$ never falls below half the jump's size."

## l22 (distance in general)

- app/content/courses/analysis/l22-metric-spaces.json | screens[11] explain | note | "standardised return vectors" is ambiguous: with population z-scores over 3 days the distance is $\sqrt{6(1 - \rho)}$; $\sqrt{2(1 - \rho)}$ needs vectors scaled to length 1. | Replace "the straight-line distance between standardised return vectors" with "the straight-line distance between return vectors scaled to length 1".

## l23 (open and closed sets)

- app/content/courses/analysis/l23-open-and-closed.json | screens[10] option `open` why | warning | "Only finite intersections stay open" is false as stated: an infinite intersection can be open ($\bigcap_n (0, 1) = (0, 1)$). What fails is the guarantee. | Replace "Only finite intersections stay open." with "Only finite intersections are sure to stay open."
- app/content/courses/analysis/l23-open-and-closed.json | screens[0] explain | note | "inside $(0, 1)$ because both are open" gives the wrong reason; $(0.8, 1) \subseteq (0, 1)$ because $0.8 > 0$ and both leave out 1. | Replace "inside $(0, 1)$ because both are open." with "inside $(0, 1)$, since $0.8 > 0$ and 1 is left out of both."
- app/content/courses/analysis/l23-open-and-closed.json | quiz[3] explain | note | "the minimum can be 0": of infinitely many radii there may be no minimum; it is the infimum. | Replace "With infinitely many sets the minimum can be 0" with "With infinitely many sets the infimum of the radii can be 0".

## l24 (compactness)

- app/content/courses/analysis/l24-compactness.json | screens[1] prose | warning | "Two things can go wrong: the terms run away, or the limit falls outside $K$" is stated for any metric space, but quiz[0] (and the summary note) shows a third failure: $\mathbb{N}$ with the discrete metric is bounded and closed, and $1, 2, 3, \dots$ neither runs away nor has a limit outside. | Replace "Two things can go wrong: the terms run away, or the limit falls outside $K$." with "In $\\mathbb{R}$, two things can go wrong: the terms run away, or the limit falls outside $K$."
- app/content/courses/analysis/l24-compactness.json | screens[6] prose and summary.ideas[2] | warning | Both state the extreme value theorem on a compact $K$ without "nonempty": for $K = \varnothing$, $\sup f(K)$ is not defined and line e3 cannot pick $y_n$. In l17 the interval $[a, b]$ was nonempty automatically. | In screens[6] prose replace "Prove: a continuous $f: K \\to \\mathbb{R}$ is bounded above" with "Prove: for nonempty $K$, a continuous $f: K \\to \\mathbb{R}$ is bounded above"; in summary.ideas[2] replace "On a compact set a continuous function is bounded, attains its extremes" with "On a nonempty compact set a continuous function is bounded, attains its extremes".

## review-5

- No findings. All nine items recompute ($\tfrac{9}{16}$, $\tfrac1{16}$, $\tfrac98$; $U(f, P) = U(x, P) \ge \tfrac12$; $3x^2\ln(x^3)$; 0.5, 3.5, $-1$; 6 against 4; 0.5, 0.6, 0.25; $\delta = 0.01$, 0.3162), every distractor matches its why, and `pass` is 0.8.

## homework-5

- app/content/courses/analysis/homework-5.json | items[4] explain | note | "$f(K)$ is closed and bounded, so it holds its sup" needs $K$ nonempty, as for l24 screens[6]. | Replace "With $Y = \\mathbb{R}$ this gives" with "With $Y = \\mathbb{R}$ and $K$ nonempty this gives".

## Levels 1 to 4 voice (for the fix pass)

`voice-scan.py` reports 28 sentences over 20 words, all in levels 1 to 4 (word count in brackets); L5 has none. Shorten each below 21 words (split at a colon or semicolon where one exists).

- homework-1.json | items.7.prompt (22); items.7.rubric.3.text (24)
- homework-3.json | items.7.widget.how (40); items.8.model (23)
- homework-4.json | items.6.widget.how (22); items.8.model (22)
- l10-cauchy.json | summary.ideas.1 (21)
- l11-partial-sums.json | objectives.0 (22); screens.10.widget.how (21)
- l12-convergence-tests.json | screens.0.prose (21); screens.10.widget.how (30)
- l13-absolute-conditional.json | screens.9.widget.how (27); summary.trap (22)
- l14-rearranging.json | screens.3.prose (21); screens.5.widget.options.0.text (21); screens.9.prose (23); screens.10.widget.how (48); screens.11.prose (21); quiz.0.prose (26)
- l16-intermediate-value.json | screens.10.widget.how (26)
- l17-extreme-value.json | screens.3.prose (30)
- l19-uniform-convergence.json | summary.ideas.1 (25); summary.trap (21)
- l3-completeness.json | screens.10.widget.how (24)
- l5-counting-infinite-sets.json | screens.5.prose (22)
- l6-epsilon-and-n.json | screens.9.prose (23)
- l8-bounded-and-monotone.json | summary.ideas.1 (22)
- review-3.json | items.4.prose (24)

## Automated checks (no finding)

- Every other stated number recomputes exactly: $U_4 = \tfrac{15}{32}$, $L_4 = \tfrac{7}{32}$, $U_n = \tfrac{(n+1)(2n+1)}{6n^2}$ and $U_n - L_n = \tfrac1n$ for $n \le 59$, $U_{10} = \tfrac{77}{200}$, $L_{10} = \tfrac{57}{200}$, two pieces 0.625 and 0.125, $n = 101$ and 201, $\tfrac1x$: $\tfrac{319}{420} = 0.75952$, $\tfrac{533}{840} = 0.63452$, gap $\tfrac18$, $\tfrac{319}{105}$, $\ln 2 = 0.6931$; Asian gap £0.04 and $\tfrac{1}{6250} = 0.00016$; $x$ on $[0, 1]$ with 5 pieces 0.6 and 0.4; strip quotients 2.40333 and 2.26503, $F(1.5) = 1.125$, $F(1.6) - F(1.2) = 0.78933$; forward 4%, average 3.5%, integral 0.175, $e^{-0.175} = 0.83946$; 5, 7, 4; $\tfrac14$, $\tfrac16$; $\max(x - x^3) = 0.38490$ at 0.57735; correlations 0.5, 0.5, $-0.5$ and $\sqrt{2(1 - \rho)} = 1, 1, 1.7321$; $1 - \sqrt{0.85} = 0.078046$; 0.3; covers 101 and 1001; $x$ on $[0, 2]$ with 8 pieces $\tfrac94$, $\tfrac74$, $U_n - L_n = \tfrac4n$ for $n \le 39$; $\tfrac{0.03}{6} = 0.005$; turning-point sums $\tfrac{25}{108}, \tfrac{2}{27}$; $\tfrac{7}{32}, \tfrac{3}{32}$; $\tfrac{38}{27}, \tfrac{4}{27}$; $(6, -6)$; $\pm\tfrac{616}{81}$ (brute-force grid agrees).
- No `wrong[]` value lies inside its answer tolerance (the author's 66 bands plus my own pass, slider ranges in l23 screens[0] included). Every byKey key matches an option or wrong id (l22 screens[1]'s `sq`, `circ` are canvas polygon ids, as tap-regions expects).
- Theorem statements: integrability defined for bounded $f$; part one needs $f$ integrable and continuous at $c$; part two needs $G' = f$ on all of $[a, b]$ and $f$ integrable; uniform continuity on $[a, b]$ by Bolzano-Weierstrass; compactness defined in a metric space; Heine-Borel stated for $\mathbb{R}$ only (with $\mathbb{R}^n$ named, never claimed for general spaces, and the discrete $\mathbb{N}$ counterexample given). All correct apart from the nonempty warning.
- Order widgets: l20 screens[8] and [9], l22 screens[8] (with its `same` group), l23 screens[6] and [7], l24 screens[4] and [6], homework-5 items[3] and [4] each have one valid order and distractors that are genuinely wrong (circular, false or a non sequitur). The two exceptions are the l21 errors above.
- All 3 code widgets: the solution passes every example and hidden test (11, 14 and 10 cases); the starter fails every one (local CPython).
- Voice: 0 explanations over three sentences, 0 L5 sentences over 20 words (13,529 scanned course-wide, 28 long ones all in L1 to L4, listed above); no em-dash, en-dash or `!`; no American spellings ("center" appears only as the canvas `align` value); `£` for money; no `$` money. The longform rubric sums to 10.
- Teaching order: each lesson follows its brief (hook, ladder, trap, edge case, transfer); homework has 10 items, difficulty 3 to 5 with two at 5, two `order` items, `numeric` and `expression` items, a `code` item and a `longform` item.

## Counts

- Errors: 2 (l21 part one and part two `order` widgets each grade a valid order wrong).
- Warnings: 5 (l21 "only a jump"; l21 `integral` per cent value; l23 "only finite intersections"; l24 "two things can go wrong"; l24 nonempty $K$).
- Notes: 8.
- Author's script: `analysis-L5-numbers.py` exit 0 (136 of 136 checks, 66 wrong-value bands).

## Fix pass

All 15 L5 findings applied by targeted edits (2 errors, 5 warnings, 8 notes); none disputed, none deferred. The 28 long sentences of levels 1 to 4 each shortened by splitting or trimming, with no number changes.

- l21 errors fixed (2): part one `order` gets `"same": [["p1", "p2"]]` and part two `"same": [["t2", "t3"]]`, distractor d1 kept; both prose lines now say two lines may come in either order.
- l21 warnings fixed (2): quiz[2] "Only a jump" now "A jump in $f$ does make a corner in $F$"; screens[11] `integral` wrong value 0.175 to 0.00175 (unit %, tolerance abs 5e-06; 0.175 / 100 = 0.00175, recomputed twice). Notes fixed (3): "Call that supremum $s$", "supremum of", "never falls below half the jump's size".
- l23 warning fixed: "Only finite intersections are sure to stay open". Notes fixed (3): l23 screens[0] reason, quiz[3] infimum; l22 screens[11] "scaled to length 1".
- l24 warnings fixed (2): screens[1] "In $\mathbb{R}$, two things can go wrong" (consistent with the discrete $\mathbb{N}$ example in quiz[0]); "nonempty" added to screens[6] prose and summary.ideas[2].
- l20 quiz[1] "With $n$ equal pieces" and homework-5 items[4] "$K$ nonempty" fixed (notes). The homework-5 sentence was re-split to stay under 20 words and three sentences.
- Levels 1 to 4 voice (28 sentences): homework-1 (2), homework-3 (2), homework-4 (2), l3, l5, l6, l8, l10, l11 (2), l12 (2), l13 (2), l14 (6), l16, l17, l19 (2), review-3. l14 screens[3] and l17 screens[3] gain a paragraph break after the display formula so the scanner sees separate sentences; l14 screens[11] drops the word "offsetting" to fit.
- Scripts: `docs/reports/analysis-L5-numbers.py` updated for the l21 `integral` value (0.00175); exit 0, 136 of 136 checks, 66 wrong-value bands.
- Gates: validator 0 errors; voice scan 0 explanations over three sentences and 0 sentences over 20 words for the whole analysis folder; playthrough "All passed" desktop and `--mobile` for all 17 changed lessons and the sets homework-1, homework-3, homework-4, homework-5, review-3.
- Graded answers changed: none to correct answers. l21 `order` widgets now also accept the swapped valid orders; wrong-answer value `integral` (l21 screens[11]) changed from 0.175 to 0.00175.
