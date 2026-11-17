# Delta read AG, topology problem sets 1 to 3: the four re-authored problems and the fix-pass parts

Counts: `wrong` 0, `misleading` 2 (findings 6, 7), `reuse` 3 (findings 1, 4, 5), `re-author` 0, `continuity` 3 (findings 2, 3, 8), `voice` 2 (findings 9, 10), `other` 0. No key, `wrong` value or printed number is mistaken, and no fix changes a key. Finding 1 has no wording fix: the main session rules it (KNOWN_ISSUES, or a second re-author with the list given).

Scope, commit range `470b65ad..e3a000b1` on `app/content/courses/topology/problems-1.json`, `-2`, `-3`, read at `b7e515b6`:

- re-authored: `p-signal-bands` (set 2), `p-kernel-equation`, `p-trapping-interval`, `p-coin-paths` (set 3);
- fix-pass parts on kept problems: the 8 lesson references now in words (5 in set 1, 1 in set 2, 2 in set 3); `p-four-point-line` parts 1 and 4; `p-gapped-domain` parts 2 and 4; `p-right-rays` parts 1 and 2; `p-cube-delta` parts 3 and 4; and the `p-plotter-zone` part 4 explanation the fixer left as it was.

Brief: `docs/briefs/delta-read-af.md` with the session AG additions (exam items by skill id; set 3's lesson cover and difficulty; printed keys, terms, replaced walks and lesson ids from the first read; proof-heavy claims; story scope all of `app/content/`; pass 8 rules by hand). No browser, no content or engine edit.

## Method

- Each part was solved from its text before its key was read, then again in `docs/reports/delta-review-delta-ag-topology-numbers.py`, which imports no earlier script and uses the standard library only. Routes: every subset, family and subspace of the three-point and four-point spaces by brute force (the 29 topologies, the 7 inside $\tau$, the 6 connected subsets, the 24 bijections); the integral operator applied on a grid by the trapezium rule next to exact Fractions, with 200 random pairs for the constant; bisection, a sign scan below the root and plain iteration for the trapping interval; paths as 0/1 tuples with Fractions for the coin space; bisection and the quadratic formula for the cube root. Each numeric band is rebuilt with the engine's rule and fed the figure the part's own working prints.
- The engine's graders were run in node on every typed part in scope (`probe.mjs` in the scratch folder, built on the second reader's `grade-probe.mjs`): 303 checks and 105 rows of my own (fractions, 3-place and 4-place roundings, each slip, other forms of $0.2e^r$). Three rows failed and are not findings: they typed LaTeX (`\frac14`, `2^{-3}`) into a numeric field, which takes `1/4` and `1/8`.
- Claims read for their hypotheses: $(C[0, 1], d_\infty)$ complete (l11 screens[4]); a closed subset of a complete space is complete (l11 screens[3]); $q = \tfrac14 < 1$ and $q = 0.2e^r < 1$ exactly for $r < \ln 5$; the a posteriori bound $\tfrac{q}{1 - q}d(x_n, x_{n-1})$ as l13 screens[2] states it, and $\tfrac{1}{1 - q}d(x_1, x_0)$ as a bound for $d(x_0, x^*)$; the strong triangle inequality for $d = 2^{-k}$; $|V(\omega) - V(\omega')| \le 2d(\omega, \omega')$; $\Omega$ complete (stated, true); $x^3$ on $[0, \infty)$ not uniformly continuous.
- Reuse: every screen and quiz of l5, l8, l9 to l13, `review-2`, `review-3`, `homework-2`, `homework-3` and all 30 items of `exams/topic-3.4.json` (13 carry a `tg-` skill; no other exam or bank file carries one) were read as learner text; l6 and l7 by grep. `app/content/` was searched for each story and key number: sell, hold and buy signals, 98 and 102, integral equation, $0.2e^x$, 0.2711, 0.2592, 1.9582, first-difference metrics, binary expansions, $udud$.
- Each fix text was applied to a copy of `app` in the scratch folder (`delta-review-delta-ag-topology/copy`, `apply_fixes.py`) and run there; the worktree content was never edited.

## Tool results

| check | result |
|---|---|
| author's script `problems-topology-numbers.py` | 748 checks, 0 failures, numbers_lib 77, 66, 94; exit 0 |
| reader's script `problems-topology-numbers-read.py` | 541 checks, 0 FINDING lines, exit 0 |
| `delta-review-delta-ag-topology-numbers.py` | 365 checks, 0 failed, 10 FINDING lines, exit 0; on the fixed copy 365 checks, 0 failed, 9 `resolved`, finding 1 open |
| validator | 0 errors, 4567 warnings, none on the three sets (no pass 8 warning); none on the fixed copy |
| voice scan 35, course folder | 0 and 0; 0 and 0 on the fixed copy |
| `fresh-check --file`, three sets | 0 hits each (set 1 keeps its $d_p$ advisory); the same on the fixed copy |
| `grade-all --file`, three sets | 16, 16 and 16 widgets, 0 failures; 0 failures on the fixed copy |
| author's script on the fixed copy | not run (its `numbers_lib` was not copied); the fixes change no key and one slip `tol` |

## Verdict per item

| set | item | numbers and claims | closest course material | verdict |
|---|---|---|---|---|
| 2 | `p-signal-bands` | clean | l5 screens[0] and l8 screens[1] (the same three-point space), `h2-five-families`, `r2-preimage-sierpinski`, l8 quiz `q-connected-count`; exam `e-four-point-topology` | reuse (finding 1); also findings 2, 3, 4 |
| 3 | `p-kernel-equation` | clean | l13 screens[7] (Picard, $q = \tfrac12$, iterates from $y_0 = 1$), l13 screens[2], `h3-aposteriori`, `q-which-bound`; exam `e-plane-contraction`, `e-two-function-metrics` | clean; one slip line reused (finding 5) |
| 3 | `p-trapping-interval` | clean; one hypothesis false by $4.4 \times 10^{-6}$ (finding 6) | l13 screens[1], [3], [11], `h3-use-it`, `r3-hypothesis`, `r3-constant`; exam `e-plane-contraction`, `e-power-contraction-proof` | clean |
| 3 | `p-coin-paths` | clean; one "always" false at the ends (finding 7) | l9 screens[8], l11 screens[1] and [8], `r3-subcover-count`, `h3-arctan-tail`; exam `e-compact-subsets`, `e-log-metric` | clean; finding 8 |
| 3 | `p-cube-delta` parts 3, 4 | clean; applied as the review gave them | l10 screens[5], `r1-delta-max` | clean |
| 2 | `p-four-point-line` parts 1, 4 | clean; applied exactly | `q-basis-count`, `r2-basis-count` | clean |
| 2 | `p-gapped-domain` parts 2, 4 | clean; applied exactly | `h2-subspace-split` | clean |
| 2 | `p-right-rays` parts 1, 2 | clean; applied with "the closure lesson" | l3 screens[5] | clean |
| 1 | lesson references, `p-plotter-zone` | clean | | findings 9, 10 |

Plain answers to the questions asked.

- **Replaced walks.** `p-kernel-equation` is not l12, l13 or `homework-3` with another map: no a priori count, no into-itself image, no rate at the fixed point; the constant comes from bounding a kernel, the fixed point from an ansatz, and part 4 measures the a posteriori bound against a true error, which no course item does. l13 screens[7] also iterates an integral operator from the constant 1, but asks only for $P_3(\tfrac12)$. `p-trapping-interval` shares one step with l13 screens[2] and [3] (the mean value theorem, the largest slope at the right end), now as a function of $r$; parts 2 and 3 (invariance from $|T(0)| \le (1 - q)r$, the smallest such $r$) are in no lesson, review, homework or exam item. `p-coin-paths` is not l9 screens[8] with another sequence, and the course has no sequence-space or Cantor-set screen: the grep for binary, dyadic, Cantor, coin and $2^{-k}$ in the course folder is empty.
- **Printed keys.** No part in scope prints its own key or lists the things whose count is the key. `p-gapped-domain` part 2 no longer lists the three pieces. `p-four-point-line` part 2 lists the 8 open sets, which is part 1's key restated, as the chain rule asks.
- **Terms.** All defined by the level or the stem, except $f \circ p$ (finding 3). "Cut point", "component", closure as smallest closed set and interior as largest open set are now given in one sentence each.
- **Lesson ids.** None left in learner text; the eight references in words name the right lessons ("the continuity lesson" l4, "the open balls lesson" l2, "the closure lesson" l3, "the distances lesson" l1, "the connectedness lesson" l8, "the open covers lesson" l9, "the compact images lesson" l10).
- **Set 3.** `p-kernel-equation` has difficulty 5. Every lesson is drawn on: l9 by `p-cube-delta` part 1 and `p-coin-paths` part 1; l10 by `p-cube-delta` parts 2 to 4; l11 by `p-coin-paths` part 4 and the completeness hypotheses of the two contraction problems; l12 by `p-kernel-equation` parts 1 and 2 and `p-trapping-interval` part 2; l13 by `p-kernel-equation` part 4 and `p-trapping-interval` parts 1 and 4.
- **`p-plotter-zone` part 4.** The numbers are right: $(3.7, 0.9)$ lies on $3x + y = 12$, and $0.4\sqrt{10} \approx 1.2649$ is above 1.1926. The sentence is not: it says the point is above the floor. The fixer's reason for leaving it does not hold, since `[working-band]` skips a text with a number after its last maths span (the earlier rewording raises no warning on the copy). Finding 10 gives a wording that also ends on the key.
- **Pass 8 by hand.** No key or slip is a tie at its asked places ($0.27110667$, $0.25917110$, $1.95818865$). Each band takes the figure its working prints (0.2711, 0.2592, 1.9582, 0.05) and refuses each slip; no slip band meets a key band. A learner who stops the iteration of `p-trapping-interval` part 4 one step early types 0.2591, which the band takes. No percentage part, no table value.

## Findings

Format: `N. file | JSON path | class | problem | evidence | exact fix`.

1. `problems-2.json` | `items[1]` (`p-signal-bands`), parts 2 and 3 | reuse | $\tau$ is the level's own three-point space with the points renamed, and the deciding step of parts 2 and 3 is a lesson screen.
   Course, l5 screens[0] (the level's opening screen): the family $\varnothing$, $\{a\}$, $\{b\}$, $X$ on $\{a, b, c\}$ lacks $\{a\} \cup \{b\}$; "With it the family $\{\varnothing, \{a\}, \{b\}, \{a, b\}, X\}$ is closed under unions and intersections." `h2-five-families` has the same family as an option and "$\{b\} \cup \{c\} = \{b, c\}$ is missing". l8 screens[1]: "Now take $\tau = \{\varnothing, \{a\}, \{b\}, \{a, b\}, X\}$ on $\{a, b, c\}$ ... No pair: the only open set holding $c$ is $X$ ... Whichever set holds $c$ must be $X$, leaving the other empty. So no separation exists". l8 screens[10] tests the same family in its doctest, and `q-connected-count` settles the two-point subspaces.
   Problem: $\tau = \{\varnothing, \{\text{sell}\}, \{\text{buy}\}, \{\text{sell}, \text{buy}\}, S\}$, with sell, buy, hold for $a$, $b$, $c$. Part 2: "Only $\{\varnothing, \{\text{sell}\}, \{\text{buy}\}, S\}$ fails, since it misses a union." Part 3: "The only member of $\tau$ holding hold is $S$, so a subset holding hold has no separation."
   What is new: the count of sets with open preimage (5), the count of topologies inside $\tau$ (7), the count over all subspaces (6) and the argument of part 4. The author's report names l5 screens[4] and l8 screens[2] as closest and misses both screens above. The checker reads no finite topology up to a renaming of points.
   No wording clears it: the story's three bands force this $\tau$, and the other band layouts give the chain or the space with one open middle point, both also in the course (`h2-relabellings`, `h2-five-families`). There are only 9 topologies on three points up to renaming, so a three-signal problem cannot avoid the lessons' spaces. Ruling asked of the main session: record in KNOWN_ISSUES (my view, since three of the four tasks are new), or re-author on a space the level does not hold.
   Not to walk, if re-authored: l5 screens[0]; l8 screens[0], [1], [10]; `h2-five-families`; `q-connected-count`; `r2-preimage-sierpinski`; any topology on three points.

2. `problems-2.json` | `items[1].parts[1].question`, `items[1].parts[2].question` (`p-signal-bands`) | continuity | parts 2 and 3 restate the count 5 and the name $\tau$, not the five sets. A learner who missed part 1 cannot do either part.
   Fix, part 2: replace "Using part 1, the 5 sets with open preimage form a topology $\tau$ on $S$." with "Using part 1, the 5 sets with open preimage are $\varnothing$, $\{\text{sell}\}$, $\{\text{buy}\}$, $\{\text{sell}, \text{buy}\}$ and $S$. They form a topology $\tau$ on $S$."
   Fix, part 3: replace "Using $\tau$ from part 2: give each" with "Using $\tau$ from part 2, whose sets are $\varnothing$, $\{\text{sell}\}$, $\{\text{buy}\}$, $\{\text{sell}, \text{buy}\}$ and $S$: give each". One maths span per set, as the 440 px layout needs.

3. `problems-2.json` | `items[1].parts[3].question`, `.explain.text` (`p-signal-bands`) | continuity | $f \circ p$ is used in the options and never defined; the course writes $\circ$ only for the interior $U^\circ$, and no lesson states that a composite of continuous maps is continuous.
   Fix, question: after "with $p(0) = 97$ and $p(1) = 104$." insert "The signal at time $t$ is $f(p(t))$, written $(f \circ p)(t)$."
   Fix, explain, first sentence: "$[0, 1]$ is connected, and $f \circ p$ is continuous into $(S, \tau)$: for $W$ in $\tau$, $p^{-1}(f^{-1}(W))$ is open."

4. `problems-2.json` | `items[1]` (`p-signal-bands`), every string with 97, 98, 102 or 104 | reuse (other course, slight) | `first-python` l5 is built on the same rule and two of the numbers.
   Course: "You bought shares at £104.00 and set a stop-loss at £98.00. The desk's rule: sell when a price is strictly below the stop, otherwise hold." Problem: "A desk's signal read from a price: ... sell when $x < 98$, hold when $98 \le x \le 102$", with the path ending at 104.
   Fix: in `p-signal-bands` replace 98 by 60, 102 by 64, 97 by 58 and 104 by 67 throughout (prose, part 1 feedback and explanation, part 4 question, options and explanation). No key changes. Tested with finding 2 and 3 on the copy.

5. `problems-3.json` | `items[0].parts[3].feedback.byKey.over-one-minus` (`p-kernel-equation`) | reuse | the slip line is `h3-aposteriori`'s line.
   Course: "$\tfrac{d}{1 - q}$ bounds $d(x_{n-1}, x^*)$, one step earlier. One more step gains the factor $q$." Problem: "You used $\tfrac{1}{1 - q}\,d_\infty(f_1, f_0)$, which bounds the distance from $f_0$ to $f^*$. The bound for $f_1$ carries the extra factor $q$."
   Fix: "You left $q$ out of the numerator: $\tfrac{1}{1 - q} \cdot \tfrac14 = \tfrac13$, which is $\tfrac{20}{3}$ times the error. The bound is $\tfrac{q}{1 - q} \cdot \tfrac14 = \tfrac{1}{12}$."

6. `problems-3.json` | `items[1].parts[3].question`, `.explain.text`, `.widget.wrong[1]`, `.feedback.byKey.radius` (`p-trapping-interval`) | misleading | part 4 takes $r = 0.2711$ and says part 2 promised the invariance, but the smallest radius is $0.27110667$: at 0.2711 the condition $0.2 \le (1 - q)r$ fails by $4.4 \times 10^{-6}$.
   The statement "T maps $B_r$ into itself" is still true at 0.2711 ($T$ increases and $T(r) \le r$ from $r = x^* \approx 0.2592$), so no learner is marked wrongly; the stated reason is what fails.
   Fix, question: replace "Using $r = 0.2711$ from part 3: $T$ maps" with "Using part 3, round the smallest radius 0.2711 up to $r = 0.2712$, where part 2's condition holds. $T$ maps".
   Fix, explain: "lies in $B_{0.2712}$, as part 2 promised".
   Fix, slip `radius`: `value` 0.2711 kept, `tol` `{ "abs": 0.00015 }` (takes 0.2711 and 0.2712; the key band ends at 0.25927); line "That is the radius from part 3. The fixed point lies inside $B_r$, where $x = 0.2e^x$."
   Note, no change asked: for this increasing $T$ the interval $B_r$ is invariant from $r = x^*$, so the 0.2711 of part 3 is the smallest radius of the triangle condition, not of the theorem. The text claims only the first.

7. `problems-3.json` | `items[2].parts[2].explain.text` (`p-coin-paths`) | misleading | "a score with a finite binary form has two paths" is false for the scores 0 and 1, which have one path each.
   Fix: "As $0.5 = 0.4999\dots$ in decimals, a score strictly between 0 and 1 with a finite binary form has two paths."

8. `problems-3.json` | `items[2].parts[3].question` (`p-coin-paths`) | continuity | "Using part 3, $V$ is continuous." The continuity is part 2's bound; part 3 showed $V$ is not one-to-one, and part 4 uses nothing else of it.
   Fix: "Using parts 2 and 3, $V$ is continuous, though not one-to-one."

9. `problems-1.json` | `items[0].parts[2].explain.text` (`p-plotter-zone`) | voice | "the step in the the open balls lesson proof that equivalent metrics share open sets": a doubled word left by the lesson-reference fix.
   Fix: "the step by which the open balls lesson proves that equivalent metrics share open sets".

10. `problems-1.json` | `items[0].parts[3].explain.text` (`p-plotter-zone`) | voice | "The nearest point is $y + 0.4(3, 1) = (3.7, 0.9)$, above part 3's floor of 1.1926." A point is not above a floor; the distance is.
   Fix, sentences 2 and 3: "The nearest point is $y + 0.4(3, 1) = (3.7, 0.9)$. Its distance, above part 3's floor of 1.1926, is $0.4\sqrt{10} = \tfrac{4}{\sqrt{10}} \approx 1.2649$." It ends on the key, and stays at three sentences.

## Verified with no finding

- `p-signal-bands`: 5 of the 8 preimages are open, and one that holds $[98, 102]$ is open only as $\mathbb{R}$; $f$ is continuous into $(S, \sigma)$ exactly when $\sigma \subseteq \tau$, checked on all 29 topologies; 7 lie inside $\tau$ and the one failing choice of the 8 is the two singletons without their union; 6 of the 7 non-empty subsets are connected; the only connected subset with sell and buy is $S$; each of the three wrong arguments is false for the reason its `why` gives.
- `p-kernel-equation`: $q = \tfrac14$ is attained by $f - g = 1$; $c = \tfrac14 + \tfrac{c}{6}$ gives $\tfrac{3}{10}$, and 40 iterations on a grid reach $1 + 0.3x$; the error after one step is $\tfrac{1}{20}$; the bound is $\tfrac{1}{12}$ and holds; the ratio is $\tfrac53$; each of the 10 slips is the value its line names. The key 0.05 is also the answer of `r3-ramps` ($\tfrac1{10} - \tfrac1{20}$), by another sum: one number, no finding.
- `p-trapping-interval`: $0.2e^r$ is the best constant at four radii (4,000 pairs each); the triangle line is the one valid option; the root 0.27110667 is the first, with the left side negative on a scan below it; "short by about 0.0007" and "over" at 0.272; $q \approx 0.2623$; iterates 0.2, 0.2443, 0.2553, 0.2582; $x^* = 0.25917110$.
- `p-coin-paths`: 8 balls, pairwise equal or disjoint; the gap $\tfrac18$ is attained; $|V(\omega) - V(\omega')| \le 2d$; exactly 2 paths score $\tfrac58$; $\omega_m$ and $\omega_n$ first differ on day $2\min(m, n) + 1$; the series gives $\tfrac23$.
- `p-cube-delta`: the second factor peaks at 12; the expansion $\tfrac{x^2}{4} + \tfrac{x}{48} + \tfrac{1}{1728}$; the root 1.95818865 by bisection and by the quadratic formula; $x + \tfrac1{12} \approx 2.0415$ lies past the end of $K$; the gap grows further out.
- Kept problems of set 2: 8 open sets, 2 cut points and 1 homeomorphism by brute force; 3 components; forced values of length 5; closure end 5 and interior end 10.

## Engine

- `fresh-check` reads no finite topology up to a renaming of its points: `p-signal-bands` carries the space of l5 screens[0] and l8 screens[1] with sell, buy, hold for $a$, $b$, $c$, and part 3's reason retells l8 screens[1] with no hit.
- No rule finds a doubled word in learner text ("the the open balls lesson proof", `problems-1` `p-plotter-zone`).
- No rule finds a restated key that, at its rounded value, fails the inequality it was the smallest solution of (`p-trapping-interval` part 4: 0.2711 against the root 0.27110667).

Inbox: three bullets under `Raised later (review-delta-ag-topology):` in `docs/BACKLOG-INBOX.md`.
