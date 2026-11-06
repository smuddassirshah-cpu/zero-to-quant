# Topology level 3 (Compact and complete): second-reader findings

Scope: `l9-open-covers`, `l10-compact-images`, `l11-complete-spaces`, `l12-contraction-mapping`, `l13-fixed-point-iteration`, `review-3`, `homework-3` in `app/content/courses/topology/`.
Method: every file read in full; every stated number and wrong-option value recomputed in an independent scratch script (brute force over subsets, bisection for the Lebesgue number, midpoint sums for the $d_1$ gaps, exact `Fraction`s, loops against log formulas, bisection for $x^*$ and the implied volatility); every code widget's solution and starter run against its hidden tests in CPython; hypotheses of each general claim checked by hand.
Format: `n. path | JSON path | severity | problem | evidence | fix`. Severity: wrong = false statement or wrong number; misleading = true but mis-hypothesised, mis-cited or a distractor that cannot fire; voice; layout.

## Tool results

- `python3 docs/reports/topology-L3-numbers.py`: exit 0, "242 of 242 checks passed", plus seven "check by hand" byKey lines (l12 noseries and plus, l13 deg, phi and neg, review-3 two, homework-3 vol), all of which I read and found right.
- Not checked by the author's script: hint and explain prose that states a fact without a number field (findings 1 and 2), code behaviour claims in prose (finding 3), whether $\cos$ on $[0, 2]$ has a constant below 1 (finding 10), and the tolerance of wrong values against the requested rounding (finding 13).
- `node tools/validate.mjs`: 0 errors, 2349 warnings; topology L3 warnings are only "a problem screen without a canvas before the ladder ends" (l9 screens 3 to 5, l10 screens 3, 4, 6, l11 screen 4, l12 screen 4). No `[table-slip-key]` warning on any topology file.
- `VOICE_BASE=app/content/courses/topology python3 docs/reviews/voice-scan.py`: 0 explanations over three sentences; 5,835 sentences scanned, 0 over 20 words.
- Code widgets (CPython): every solution passes all its tests (l9 7/7, l11 6/6, l12 7/7, l13 9/9, homework 7/7); every starter fails (l9 starter passes the three `None` tests and fails four; the rest pass none).
- Recomputed and right: $\{I_1, I_2, I_3\}$ unique smallest; Lebesgue number 0.05; 41 and £5,000; $\tfrac1e \approx 0.3679$, $f(3) \approx 0.1494$; $w_1 = 0.1053$, 9.787%, $-0.0769$ (vol 0.0992), long-only minimum at 0; 0.0625, 0.5, 0.025, 0.05; 0.089669; $N$ = 10, 20, 100, 1000; 96 and 48; the $0.5x + 1$ iterates and 1.25; 21 (20.93); 1.2, 0.9, 0.8762, $(\tfrac{65}{14}, \tfrac{10}{7})$, the eight matrix iterates, 160, 31; Gordon £4.72, £9.26, £13.62, 120.28, 115.74, 111.38, 0.9623, 245.24, 0.0101, 0.00971, 246; 7% table 49.2 and 779, 1.0094, $-$£500; quiz 0.2147, 0.0429, 0.0239; the cobweb points from 2.5; 0.5403 to 0.7014; 0.739085, 0.8415, 0.6736; 2.900, 86.2, $2.9 \times 10^{-6}$, $1.04 \times 10^{-6}$, $8.7 \times 10^{-7}$, 87, 39, 32; Newton 1.5 to 1.414214 with errors 0.086, 0.0025, $2.1 \times 10^{-6}$, $1.6 \times 10^{-12}$, count 20; Picard 1.6458333, 1.6487213, 0.0028879; $M = 39.8942$, 0.200572, 0.205690, $q = 0.0308$, 0.200866, 0.200867 (third step within $7.5 \times 10^{-9}$), 0.200867441; $\tfrac{1}{1 + x}$: 17, 15, 14, 0.5 to 0.615385, 0.618034; review 3, 12, 0.00195, 0.00098, 0.5; homework 19.983, 0.009712016494, 0.2, 0.3333.

## Findings

1. app/content/courses/topology/l9-open-covers.json | screens[0].hints[2].text | wrong | "Then only $I_2$ holds 0.35 and 0.6." is false: $I_5 = (0.4, 0.62)$ also holds 0.6. | 0.4 < 0.6 < 0.62; the explain itself uses 0.65, not 0.6. | "Then only $I_2$ holds 0.35."

2. app/content/courses/topology/l9-open-covers.json | screens[10].explain.text | wrong | "The 41 balls of radius 0.25% are a finite subcover of the scenario interval." Open balls of radius 0.25 centred every 0.5 miss every midpoint. | $-9.75$ is exactly 0.25 from $-10$ and from $-9.5$, so it lies in neither open ball. | "The 41 open balls of radius 0.3% round the grid points are a finite subcover of the scenario interval."

3. app/content/courses/topology/l12-contraction-mapping.json | screens[9].hints[1].text and screens[9].explain.text | wrong | Both say that without the $q \ge 1$ check the loop never ends. In the solution's loop, $q = 1$ raises `ZeroDivisionError` at once (the bound divides by $1 - q$), and $q > 1$ makes the bound negative, so the loop returns 0. | Ran the solution's loop without the guard: `apriori_steps(1, 1, 0.01)` gives ZeroDivisionError; `apriori_steps(1.5, 1, 0.01)` returns 0. | hints[1]: "Check $q \ge 1$ before the loop: at $q = 1$ the bound divides by zero." explain: "The loop stops at the first $n$ with a bound below the tolerance. Without the check, $q = 1$ divides by zero. A $q > 1$ makes the bound negative, so the loop wrongly returns 0."

4. app/content/courses/topology/l9-open-covers.json | summary.ideas[2]; and l10-compact-images.json | screens[4].widget.options[0].text | misleading | l9 states the Lebesgue lemma as "A finite cover of a compact set has a Lebesgue number". The lemma needs a metric space and holds for every open cover. l10 then applies it, citing l9, to the infinite cover $\{B(x, \delta_x)\}$, which the l9 wording does not cover. | l10 screens[4] prose: "Each $x$ has $\delta_x$ ..."; the cover has one ball per point of $K$. | l9 summary.ideas[2]: "... are compact. Every open cover of a compact metric space has a Lebesgue number: 0.05 for the hook's cover." l10 option text: "The balls $B(x, \delta_x)$ cover $K$; take $\delta$ a Lebesgue number of this cover, which exists as $K$ is a compact metric space."

5. app/content/courses/topology/l9-open-covers.json | screens[2].widget.lines[4].why and screens[2].feedback.byKey.d1 | misleading | "one member per point is infinitely many" is not always so: if the cover is finite, one member per point gives a finite set. The flaw is that it may be infinite. | Any finite cover of $[0, 1]$, such as the hook's. | why: "That gives a subcover, but it may have infinitely many members. Compactness needs a finite one." byKey.d1: "You kept a member for every point. That can be infinitely many, so it is no finite subcover."

6. app/content/courses/topology/l9-open-covers.json | screens[9].explain.text | misleading | "Greedy reach is optimal: any cover needs an interval round each handover point." The handover points are greedy's own; another subcover has different ones, so this is not the reason. | The standard argument is by induction on the number of picks. | "Greedy reach is optimal: after $k$ picks it reaches at least as far as any $k$ intervals can."

7. app/content/courses/topology/l10-compact-images.json | screens[6].widget.lines[3].text | misleading | "compact subsets of a Hausdorff space are closed" is used as known, but l9 screens[4] proved it only in a metric space. | l9 screens[4].prose: "Let $K$ be compact in a metric space". | "$h(F)$ is closed: compact sets in a Hausdorff space are closed, as in l9 with disjoint open sets for balls."

8. app/content/courses/topology/l11-complete-spaces.json | screens[7].prose, screens[7].widget.options[1].why, screens[7].widget.options[2].why | misleading | The trap says $(0, 1) \cong \mathbb{R}$ "(l7)" and "l7 built one", and names l7's map $\tfrac{x}{1 - \lvert x\rvert}$. l7 built $(-1, 1) \cong \mathbb{R}$ with that map; it never treats $(0, 1)$. screens[6].prose also cites l7 for $\arctan$, which l7 does not mention. | l7: "Proving $(-1, 1) \cong \mathbb{R}$"; `grep arctan l7-homeomorphisms.json` finds nothing. | prose: "... are homeomorphic, by $2x - 1$ and then l7's map." options[1].why: "You treated completeness as topological. $2x - 1$ then l7's $\tfrac{x}{1 - \lvert x\rvert}$ stretch Cauchy sequences into divergent ones." options[2].why: "They are: $2x - 1$ maps $(0, 1)$ onto $(-1, 1)$, and l7's map takes that onto $\mathbb{R}$." screens[6]: "since $\arctan$ is a homeomorphism onto $(-\tfrac\pi2, \tfrac\pi2)$, in the sense of l7."

9. app/content/courses/topology/l11-complete-spaces.json | summary.ideas[0], screens[8].feedback.correct | misleading | "discrete spaces are" complete and "Every discrete space is complete" read as spaces with the discrete topology, which is false, and is the very trap of this lesson (completeness is not topological). Only the discrete metric makes the claim true. | $\{\tfrac1n : n \ge 1\}$ with $\lvert x - y\rvert$ has the discrete topology, and $\tfrac1n$ is Cauchy with no limit in it. | ideas[0]: "... are not; a space with the discrete metric is." feedback.correct: "Right. The discrete metric always gives a complete space."

10. app/content/courses/topology/l12-contraction-mapping.json | screens[7].widget.options[2].why, screens[7].explain.text, screens[7].feedback.correct | misleading | $\cos$ on $[0, 2]$ also has no constant $q < 1$: $\lvert\sin\rvert$ reaches 1 at $\tfrac\pi2 \in [0, 2]$. So it drops two hypotheses, while feedback.correct says "Each of the others drops one hypothesis" and the hint tells the learner to test $q$ on each map. | $\max_{[0, 2]}\lvert\sin x\rvert = \sin\tfrac\pi2 = 1$. | Either swap the interval for $[0.6, 1.2]$ ($\cos$ maps it into $[0.3624, 0.8253]$, not inside; $q = \sin 1.2 \approx 0.9320 < 1$; the fixed point 0.739 lies inside, so only "into itself" fails), or keep $[0, 2]$ and add to the why "And $\lvert\sin\rvert$ reaches 1 at $\tfrac\pi2$, so no $q < 1$ works either.", with feedback.correct "Right. Each of the others drops at least one hypothesis."

11. app/content/courses/topology/l12-contraction-mapping.json | screens[5].feedback.byKey.noseries, screens[10].feedback.byKey.off; l13-fixed-point-iteration.json | screens[4].feedback.byKey.eighty-six | misleading | Each why states the consequence but not the learner action. 20 is exactly what dropping $\tfrac{1}{1 - q}$ gives ($0.5^{20} < 10^{-6}$); 245 and 86 come from rounding 245.2 and 86.2 down. | $0.5^{20} = 9.5 \times 10^{-7}$; $\ln(0.00008)/\ln q = 245.24$; 86.21 for cosine. | l12 noseries: "You dropped the factor $\tfrac{1}{1 - q} = 2$. The bound $2 \times 0.5^{20} \approx 1.9 \times 10^{-6}$ is still above." l12 off: "You rounded 245.2 down. At 245 steps $125q^{245} \approx 0.0101$, still above £0.01." l13: "You rounded 86.2 down. At 86 the bound is about $1.04 \times 10^{-6}$, still above."

12. app/content/courses/topology/l13-fixed-point-iteration.json | screens[7].explain.text | misleading | "proves that ordinary differential equations have solutions" drops the hypotheses: Picard's argument needs $f(t, y)$ Lipschitz in $y$ and gives a solution on a short interval. | $y' = y^{2/3}$, $y(0) = 0$ is not Lipschitz at 0 and has two solutions; $y' = y^2$ blows up. | "The same argument, in a space of functions, proves that $y' = f(t, y)$ has one solution near the start when $f$ is Lipschitz in $y$ (`odes`)."

13. app/content/courses/topology/l13-fixed-point-iteration.json | screens[11].widget.wrong[1].tol and screens[11].widget.wrong[0].tol | misleading | The question asks for 3 significant figures. A learner who makes the $\tfrac1{32}$ slip types 0.0313 (or 0.0312), outside the 'exp' tolerance $5 \times 10^{-6}$ of 0.03125; the 'ratio' slip typed as 0.969 misses 0.9692 $\pm 5 \times 10^{-5}$. Neither byKey line can fire for an answer given as asked. | $\lvert 0.0313 - 0.03125\rvert = 5 \times 10^{-5}$; $\lvert 0.969 - 0.9692\rvert = 2 \times 10^{-4}$. | 'exp' tol abs 0.00006 (range 0.03119 to 0.03131, clear of the answer's 0.03075 to 0.03085); 'ratio' tol abs 0.0005.

14. app/content/courses/topology/review-3.json | items[4].widget.options[2].why | misleading | "$(0, 1)$ is incomplete too, but $T$ already leaves the space, which matters first." No hypothesis matters first; the option is wrong only because completeness is not the only failure. The question "Which hypothesis fails?" also reads as if one does. | $(0, 1)$ is not complete and $T$ maps it into $(1, \tfrac43)$: both fail. | question: "Which hypothesis fails, beyond completeness?" why: "$(0, 1)$ is incomplete, but that is not the only failure: $T$ also leaves the space."

15. app/content/courses/topology/homework-3.json | items[2].prose | misleading | The proof's line o2 takes a minimum "at some $k \in K$", which needs $K \ne \varnothing$; the prose assumes only $F \ne \varnothing$. l10's extreme value screen states $K \ne \varnothing$. | l10 screens[3].prose: "on a compact space $K \ne \varnothing$". | "... with $K \cap F = \varnothing$ and $K, F \ne \varnothing$."

16. app/content/courses/topology/l13-fixed-point-iteration.json | quiz[1].widget.options[1].why | misleading | "The last step understates the error by up to $\tfrac{q}{1 - q}$" has no meaning when $q < \tfrac12$, where that factor is below 1. The point is that the true error can be $\tfrac{q}{1 - q}$ times the last step. | $q = 0.3$ gives $\tfrac{q}{1 - q} = 0.43$. | "The error can be $\tfrac{q}{1 - q}$ times the last step, which is large when $q$ is near 1."

17. app/content/courses/topology/l9-open-covers.json | screens[10].widget.rows[1][0] | voice | "most the true worst loss can exceed the grid's worst (£)" is not a phrase. | Table row label. | "how far the true worst loss can exceed the grid's (£)".

18. app/content/courses/topology/l11-complete-spaces.json | screens[9].widget.how | voice | "the width uses math.isclose" in prose without code formatting (flagged in review-1.5 as American "math"). | review-1.5, l10-birthday and homework-5. | "the width uses `math.isclose`."

19. app/content/courses/topology/l11-complete-spaces.json | screens[5].hints[0].text, screens[11].hints[0].text | layout | Both hints say "the dashed gap", but the `gap` segment has no `dashed: true`, and plane segments draw solid by default. | plane.js draws `cvb-dash` only when `s.dashed`. | Add `"dashed": true` to `canvas.state.segments[0]` on both screens, or say "the coloured gap".

20. app/content/courses/topology/l10-compact-images.json | screens[0].canvas.controls | layout | $a$ and $b$ each run from 0 to 4, so a learner can set $a > b$; the domain reverses and the derive's image $[\min(f(a), f(b)), f(\min(\max(1, a), b))]$ then prints a wrong interval. | At $a = 3$, $b = 1$ the caption reads $[0.1494, 0.3679]$ for an empty domain. | Limit $a$ to 0 to 2 and $b$ to 2 to 4 (start 3), so $a \le b$ always; the hook's $[0, 3]$ stays reachable.

## Summary

20 findings: 3 wrong, 13 misleading, 2 voice, 2 layout. No engine change needed. The five figures the author's script caught in l12 and l13 are now right; l12 and l13 still carry findings 3, 10, 11, 12, 13 and 16, all in prose, hints and tolerances rather than in stated figures.

## Fix pass

1. fixed: l9 hint now says only $I_2$ holds 0.35 (0.6 lies in $I_2$ and $I_5$, checked in the number script).
2. fixed: "41 open balls of radius 0.3% round the grid points"; the script shows radius 0.25 open balls miss the midpoints and 0.3 covers.
3. fixed: l12 hint and explain now state $q = 1$ divides by zero and $q > 1$ returns 0 (both run in CPython, now asserted in the script). Code and tests unchanged.
4. fixed: l9 idea now "every open cover of a compact metric space"; l10 option cites compactness of $K$ (reworded to stay under 20 words).
5. fixed: l9 line why and byKey.d1 say "may" and "can be" infinitely many.
6. fixed: greedy-reach justification now by induction on picks.
7. fixed: l10 Hausdorff step cites l9 with disjoint open sets for balls.
8. fixed: l11 prose, options[1].why and options[2].why use $2x - 1$ then l7's map; arctan cited "in the sense of l7".
9. fixed: l11 idea and feedback.correct now say the discrete metric.
10. fixed: kept $[0, 2]$; why adds that $|\sin|$ reaches 1 at $\tfrac\pi2$, feedback.correct says "at least one", explain notes the missing $q < 1$ (split into three sentences for the voice scan).
11. fixed: l12 noseries and off, l13 eighty-six now state the learner action; 0.5^20 x 2 = 1.9e-6, 125 q^245 = 0.0101 recomputed.
12. fixed: l13 explain now states the Lipschitz and near-the-start hypotheses (shortened to one sentence under 20 words).
13. fixed: ratio tol abs 0.0005; exp tol abs 6e-5 (0.0312 and 0.0313 both inside; answer range 0.03075 to 0.03085 clear). The script now tests every numeric wrong against its question's stated rounding, with half-up and half-even.
14. fixed: review-3 option why reworded; question now reads "beyond completeness".
15. fixed: homework-3 prose adds $K, F \ne \varnothing$.
16. fixed: l13 quiz option why now "the error can be q/(1-q) times the last step".
17. fixed: row label reworded.
18. fixed: `math.isclose` in code format.
19. fixed: `"dashed": true` added to both gap segments.
20. fixed: l10 controls a in 0 to 2, b in 2 to 4 (start 3); $[0, 3]$ still reachable.

Counts: 20 fixed, 0 disputed, 0 deferred.

Gates: validate 0 errors; voice scan 0 and 0; `python3 docs/reports/topology-L3-numbers.py` exit 0 (242 of 242 plus the new asserts); playthrough green with and without `--mobile` for l9 to l13 (`--lesson`) and review-3, homework-3 (`--set`).
Graded answers changed: none.
