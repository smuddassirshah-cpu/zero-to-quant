# Engine backlog inbox

Content agents append their engine and canvas limitations here, under `Raised later (<course> level <n>):`, as bullets. An integration pass numbers them into `ENGINE-BACKLOG.md` and clears this file.


Cleared by engine pass 8 (items up to 1146 in `ENGINE-BACKLOG.md`); the previous text is in the commit before it.
Raised later (exam second item 1.3-1.4):
- No tool lists the (exam, essential skill) pairs with one auto item; each author recomputes them by hand from the exams, every `course.json` and its reviews. A validator warning per topic or stage exam (skill tagged on a level review of the exam's courses, fewer than two non-longform items) would stop a later edit, such as a reader's swap, from bringing a pair back.

Raised later (exam second item 1.5):
- Graph canvas (`markov: true`) at 440 px: a four-node chain in a row draws at about 330 px wide with small nodes, so the label on a short edge (topic-1.5 `e-floor-walk`, 2 to 3) sits tight between the nodes. A width-filling layout or a minimum node radius on phones would help.
Raised later (exam second item stage0):
- A numeric `answers` set (unordered) draws the same narrow field as a single number: at 440 px a placeholder of 26 characters ("angles, separated by commas") was cut off, and four angles typed with commas fill the box. Workaround: placeholder "angles, with commas" on `topic-0.3` `e-double-angle-roots`. Widen the field for a set, or size it to the expected count.

Raised later (exam second item 1.6-1.11):
- An `expression` set (`answers` with `unordered`) cannot take `form`, so a set of complex roots accepts the prompt typed back (`\sqrt{15-8i}, -\sqrt{15-8i}` grades right by value). Allow `form: "rectangular"` per value in a set; topic-1.11 `e-square-root-parts` asks for one root with `form` instead.
- A fenced code block inside a `multi` or `choice` option neither wraps nor scrolls at 440 px: lines past about 36 characters are clipped (seen on topic-1.9 `e-swapped-d` before rewrapping). Give option code blocks `overflow-x: auto`, or have the validator warn on option code lines over 34 characters.

Raised later (problems ito):
- Playthrough at 440 px passes a part whose inline maths overflows the page: one KaTeX span holding a comma list (`$W = 0, 0.3, -0.2, 0.4, 0.6$`) does not wrap, widened the whole card and clipped the question text, yet `--problems ito/problems-2 --shots` was green. Fail a part when `document.documentElement.scrollWidth` exceeds the viewport, as the homework `-marked` shot already does for `.katex-display`.
- `retold` learns stock sentences from committed content, so an instruction line repeated across new sets ("Read $\Phi$ from software or a normal table, and give 4 decimal places.", the wording `[table-source]` asks for) fires as a retelling between the new sets themselves. Treat a sentence that only meets `[table-source]` or `[answer-form]` as stock, or list such lines in the stoplist.

Raised later (problems algebra):
- `playthrough.mjs --problems <course>/problems-<n>` on a new set fails as "the level review's card ... has no Problem set row" and "the set opened in state empty" when `content/manifest.json` was restored with `git checkout` (as the commit rule asks) after the last validator run. The fix is to rerun `validate.mjs` first; the playthrough could say "set not in manifest.json: run tools/validate.mjs" instead.

Raised later (problems measure-prob):
- `fresh-check` same-course reuse warns when a choice option names the four modes of convergence in the usual order ("almost surely, in probability, in mean square and in distribution"), which any modes item must say. Workaround: problems-2 `p-root-of-uniform` part 5 reworded its options. A list of fixed course vocabulary that does not count towards a shared run would stop these warnings.
- After `git checkout app/content/manifest.json` (the commit rule), `playthrough.mjs --problems <set>` fails with "the set opened in state empty, not its start card" and a 20 s timeout until the validator rewrites the manifest. The playthrough could rebuild the manifest itself, or say that the set is missing from it.

Raised later (problems pdes):
- `fresh-check.mjs` reports a `rate` reuse error for a universal constant: the Gibbs overshoot fraction (8.95% of the jump, 0.0895 in `pdes` l7 screen 1, with 1.179 in both) was flagged on a new problem about a different function. Constants such as the Gibbs fraction, $\Phi^{-1}(0.975) = 1.96$ or $\ln 2$ should not count as a shared rate; a short allow-list would do. Workaround: the part was rewritten to end on a different result.
- `playthrough.mjs --problems` on a new set after `git checkout app/content/manifest.json` (as the brief asks before each commit) fails with "the level review's card on the course page has no Problem set row" and "opened in state empty", because the manifest no longer lists the set. Have the playthrough say "set missing from manifest.json: run tools/validate.mjs first", or rebuild the manifest itself.

Raised later (problems topology):
- `playthrough.mjs --problems ... --mobile` stays green when one long inline KaTeX span (a list of eight finite open sets in a problem's `prose` and a part's `question`) runs past the right edge at 440 px; the 440 px shots showed the text clipped. Have the mobile check measure KaTeX spans against their column, or have the validator warn on one maths span over about 45 characters in set text.
- `fresh-check.mjs --file` reports a hit in another course (`analysis` l17, `limits` l17: $x^3 - 3x$ with its interval) under the label `[same-course-reuse] error`. The label should say cross-course, or the rule should say whether other courses count.

Raised later (review problems algebra):
- `fresh-check --files` gave 0 hits on `algebra/problems-3` `p-fifteen-times`, whose map `15x \bmod 36` reuses the pair of exam item "The order of 15 modulo 36" and its line "$12 \mid 5x$, so $12 \mid x$". Read a multiplier and modulus held in one formula as a key pair, against exam titles and explanations too (`docs/reviews/review-problems-algebra-1-3.md` finding 8).
- `retold` missed "has bottom row $7, 9, 10, \dots$. So $\sigma(1) = 7$, $\sigma(2) = 9$, and so on." against the exam's "has bottom row $3, 5, 1, 2, 6, 4$. So $\sigma(1) = 3$, $\sigma(2) = 5$, and so on." Mask a comma list of numbers as one token before comparing skeletons (finding 5).
- A permutation in cycle form is not compared with its inverse or with the same cycles started elsewhere: `(1\,5\,3)(2\,4)` against the exam's `(1\,3\,5)(2\,4)`, both in $S_5$ (finding 6).
- A set problem whose parts each match a different item of one review, lesson or exam file by question skeleton (findings 5, 8, 9) passes every check. Flag a problem when three of its part questions each meet a different course item after numbers and maths are masked.

Raised later (review problems ito):
- `fresh-check` passes a problem whose process is a same-course item's in other units: `ito/problems-1` `p-maker-tally` builds $500t + 1000W_t$ in pounds, `homework-1` `h-drift-below` has $0.5t + W_t$ in thousands, and both ask the chance of being down. Compare the drift-to-volatility ratio (or any key that a course line's printed rule gives) when both items ask the same chance.
- `retold` misses a stem that keeps a course sentence with its numbers and opening clause changed ("a share's squared daily log returns add to", `p-realised-then-risk` against `h-realised-vol`), a story kept with one noun changed ("A junior ... the same call/digital with the real drift ... discounts at $r$", `p-digital-measures` against l11 S5), and a walk of three screens of one lesson in order (`p-one-touch` against l12 S1, S8, S3, with three lines shared with exam `e-daily-touch`). Read exam `explain` lines and lesson option texts as sources, and count a shared clause of five words with the nouns kept.

Raised later (review problems measure-prob):
- No validator rule checks that a slip typed at the places the part asks falls in its own band: problems-1 `p-reciprocal-grid` part 3 asks 2 places and its slip 0.3333 +-0.001 refuses 0.33. `[working-band]` covers keys only. Evidence: `docs/reviews/review-problems-measure-prob-1-3.md` finding 2.
- `fresh-check --file` reads exam stems but not exam option text or `explain`, nor a longform `prompt`: it misses `U^{1/n}` with mean `n/(n+1)` (exam e-swap-limits option a against problems-2 `p-root-of-uniform`) and the law `1/(k(k+1))` with tails `1/n` (homework-1 h-build-space against problems-1 `p-reciprocal-grid`). Findings 1 and 6.
- The `retold` rule did not fire on l6 "Summing the tail" against problems-2 `p-billed-hours` part 2 (same story of an order that fills, same indicator sum, the explain line changed by a few words). Finding 5.
- `[rounding-tie]` reads the stored `wrong[].value`, so a slip stored one digit past the asked places hides its tie: problems-4 `p-ten-trades` part 2 asks 5 places, the slip is $P(A) = 0.0546875$ exactly, stored as 0.054688 with a band of 5e-06, and the rounding 0.05468 gets the generic line. A rule could flag a `wrong` value with one digit more than the asked places and a band of half a step, and ask for the unrounded slip (review-problems-measure-prob-4, finding 2).
- No tool flags a choice part whose correct option alone repeats a phrase or symbol of the question (problems-4 `p-share-numeraire` part 4: "Using $Z_3$" and the only option with $Z_3$; `p-premium-weight` part 4: "any traded price $X$" and the only option with "for any traded $X$"). A check on tokens shared by the question and exactly one option would list candidates (same review, findings 4 and 5).

Raised later (problems measure-prob level 4):
- A second author on a course with a per-course number script (`problems-<course>-numbers.py`) cannot import its helpers (`num_part`, `wrong_is`, `expr_part`, `structural`): the script runs its levels and calls `sys.exit` at import. Level 4 of measure-prob copied them into `problems-measure-prob-4-numbers.py`. Moving these problem-set helpers into `app/tools/numbers_lib.py` would let split scripts share one copy.

Raised later (review problems pdes):
- `fresh-check.mjs` `retold` misses a stem that is mostly maths: `pdes` `p-fk-claim` ("a value $V(t, x)$ solves ..., with $V(T, x) = e^x$. Today $x = 0$ and two years remain.") against exam `e-fk-reverting` (the same two sentences with other coefficients) gives 0 hits, since dropping the maths leaves too few signal words. Keep the shape of a displayed equation (its operators and letters, numbers masked) as signal for the skeleton test.
- No validator rule checks a carried value: `pdes` `p-grid-modes` part 4 restates "0.2200 from part 3", but part 3's printed working ($0.9702^{50}$) gives 0.2203, and the learner who carries it is refused. `[working-band]` could evaluate a "Using <value> from part k" against part k's printed working at one more place than part k asks, and recompute simple printed products and quotients ("$0.6 \times 3.6761 \approx 2.2056$" is 2.2057).
- Number scripts' `says()` helpers match a printed figure as a string, so a false figure passes (`pdes` `p-grid-no-formula`: "$50e^{-0.015} = 49.255582$", true 49.255597). A shared helper that takes the computed value and the places would close this.

Raised later (review problems topology):
- `fresh-check.mjs` passes a question that is another item's question word for word when the numbers round it differ: "What is the smallest $n$ whose a priori bound is below 0.001?" (`topology` `r3-apriori` and `problems-3` `p-input-output` part 3) and "How many open sets does ... generate, $\varnothing$ included?" (l6 `q-basis-count`, `r2-basis-count`, `problems-2` `p-four-point-line` part 1). A whole question sentence shared with a quiz, review or homework item of the course should be at least an advisory.
- `fresh-check.mjs` does not report a 2 by 2 matrix that shares a whole column with a course matrix and takes the same key from it: `topology` l12 screens[6] $\begin{pmatrix} 0.6 & 0.6 \\ 0 & 0.3 \end{pmatrix}$ and `problems-3` `p-input-output` $\begin{pmatrix} 0.5 & 0.6 \\ 0.2 & 0.3 \end{pmatrix}$, both with $q = 0.9$ from the column $0.6 + 0.3$.
- No validator rule finds a whole-number key printed in the part's own question as a restated value (`topology` `problems-3` `p-dyadic-points` part 3: "all but 7 points", key 7). A rule `[key-in-stem]` could warn when a `numeric` key with `tol` 0 is restated as a number in the same part's question.
- No validator rule finds a lesson id written as a code span in set text (`` `l4` `` 13 times in `topology` `problems-1` to `-3`; lessons write l4 bare and keep code spans for another course's name).
- `fresh-check` passes a part that is a course item with one constant folded in: `ito/problems-4` `p-tracking-review` parts 1 to 3 against l13 S1, l14 `q-ratio` and l14 S7 (same explain skeleton, same slips by formula: lesson `whole` 6 and set `no-half` $6\sigma^2$; `unsquared` $ab/\sigma$ in both). Compare slip sets as formulas of the key (ratio of each `wrong` value to its key), and report three such parts in a row as a walk.

Raised later (review problems algebra 4):
- `fresh-check` reads no `canvas.params` matrices of a lesson, so a matrix pair shown on a canvas and retold in a set's `why` is not reported (`algebra` `problems-4` finding 3).
- An `expression` part with no `form` whose key is a polynomial and whose stem holds a `\div` or a fraction of polynomials could raise a validator warning (`algebra` `problems-4` finding 1; the class of the `review-problems-analysis-1-3` finding on a retyped question).

Raised later (fix pass problems measure-prob 4):
- `[rounding-tie]` did not fire on `app/content/courses/measure-prob/problems-4.json` items[2].parts[1].widget.wrong[0] (`no-weight`): slip value 0.0546875 (7/128) at 5 places, band abs 5e-06 around the stored 0.054688, so 0.05468 was refused. The rule reads the stored value, one digit past the asked places, and misses the tie.
