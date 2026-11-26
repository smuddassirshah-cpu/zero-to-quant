# Concept audit: quadratics, levels 1 to 3 (round 1, blind)

Scope: `app/content/courses/quadratics/` lessons l1 to l13, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, and the fluency sets for l1, l2, l3, l4, l6 and l7 (28 files). Level 4 is a separate audit. Commit read: `fe9a3b03`.

Stage 0 course, so the ledger is at reduced depth: definitions, rules, "always / never / every / only" claims, conventions, and every graded key, wrong option and slip.

Method. Every file read in full before any earlier read was opened. Every key, wrong option and slip recomputed by hand at the read, then again in `docs/reports/quadratics-L1-3-concepts.py` (sympy 1.14):

- A: 32 expand or factorise choice items, each option tested as an identity against the prompt (an equal option may be marked wrong only when the item asks for "fully" and a bracket still has a common factor).
- B: about 100 graded keys with their slip tables, the business and portfolio models, and the discriminant rule swept over 648 integer triples.
- C: all 20 fluency families enumerated over their whole range under their `where` clauses (8,038 instances): the key is an identity or the exact root set, no slip ever equals the key or another slip, and the smallest gap between a wrong root set and the key in l7 is 0.25, fifty times the tolerance.
- D: 72 points drawn on explain canvases checked against the curves they sit on.

Sources: Gelfand and Shen, *Algebra* (sections cited by title); Pearson Edexcel AS and A level Pure Mathematics Year 1, chapters 1 to 4; Hull, *Options, Futures and Other Derivatives*, ch. 4, for the bond screens.

Ledger: `docs/reports/audit-quadratics-1-3-ledger.md`, 1,164 rows: correct 1,154, wrong 2, imprecise 7, misleading 1, unverified 0.

## What is sound

The watch list came back clean on the mathematics. Signs in expanding and factorising, the difference of two squares, the zero product rule ("only a product of 0"), dividing by $x$ and losing $x = 0$, the ± on a square root, the derivation of the formula (with the right remark that ± covers either sign of $a$), the three discriminant cases, "no real solution" in l6 and l8, vertex and line of symmetry, $a > 0$ opening upwards, quadratic inequalities with strict and non-strict ends, and every applied problem that rejects a root for context (negative time, negative rows, a loss above 100%) are stated correctly. Every graded key is right. No wrong option is a correct answer in disguise except finding 3.

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `l7-the-formula.json` | `screens[7].widget.wrong[id=neg]` and `screens[7].feedback.byKey.neg` | wrong, minor | The slip value is −17 but the line says "You made $b^2$ negative. $3^2 = 9$." Making $b^2$ negative gives $-9 + 8 = -1$, not −17. | For $2x^2 + 3x - 1$: $4ac - b^2 = -8 - 9 = -17$, the subtraction taken the wrong way round (the same slip l8 `screens[2]` calls `flip`). Concepts script, finding line 1. | Keep the value −17 and replace the line with: "You worked out $4ac - b^2$: $-8 - 9$. The order is $b^2 - 4ac$: $9 + 8$."

2. `problems-3.json` | `items[0].parts[1].widget.wrong[id=no-a]` and `items[0].parts[1].feedback.byKey.no-a` | wrong, minor | The slip value is 100 but the line says "You left out the $-0.2$. $10 \times (-10) = -100$". Leaving out $-0.2$ gives −100, as the line itself computes; 100 comes from leaving out the 0.2 and keeping the minus. | $-10 \times (10 - 20) = 100$; $10 \times (10 - 20) = -100$. Concepts script, finding line 2. | Keep the value 100 and replace the line with: "You left out the 0.2: $-10 \times (-10) = 100$. With it, $-0.2 \times 10 \times (-10) = 20$."

3. `l7-the-formula.json` | `quiz[2]` (`q-which-a`): `question`, `widget.options[id=dropsign]` | imprecise, serious | "Look at $5 - 3x - x^2 = 0$. To use the formula, what is $a$?" marks $a = 1$ wrong with "You dropped the minus in front of $x^2$." A learner who first multiplies the equation by −1, a standard and sound first step, has $x^2 + 3x - 5 = 0$ with $a = 1$, $b = 3$, $c = -5$ and the same roots. The item never says the equation must be read as it stands, so the key is right under one reading only and the feedback accuses a correct learner of a sign slip. | Roots of $-x^2 - 3x + 5$ and of $x^2 + 3x - 5$ are both $\tfrac{-3 \pm \sqrt{29}}{2}$ (sympy, concepts script finding line 3). Auditor brief item 5: a wrong option that is correct under a valid alternative method. | `question`: "Reading the equation as it stands, what is $a$ in the formula?" Option `dropsign` `why`: "You dropped the minus in front of $x^2$. Multiplying every term by −1 would make $a = 1$, but then $b$ and $c$ change sign too." `explain.text`, add a third sentence: "Multiplying through by −1 first gives $a = 1$, $b = 3$, $c = -5$ and the same roots."

4. `l12-above-or-below.json` | `screens[4].question` (key 5); `homework-3.json` | `items[4].question` (key 6) | imprecise, minor | "How many whole numbers $x$ satisfy $x^2 - 2x - 8 < 0$?" The key 5 counts −1, and the homework key 6 counts −4 to −1. In the common school meaning (whole numbers are 0, 1, 2, ...) the counts are 4 and 2, and neither is a listed slip, so that learner gets only "Not quite right". The app's wider meaning is stated once, in `equations/l10-ranges-of-answers` ("Whole numbers here include 0 and negatives such as −2"), with the word "here". | Counts by enumeration: 5 against 4, and 6 against 2 (concepts script finding line 4). `l12` `quiz[1]` is unaffected (2, 3, 4, 5 either way). | `l12` `screens[4].question`: "How many whole numbers $x$, negative ones included, satisfy $x^2 - 2x - 8 < 0$?" `homework-3` `items[4].question`: "How many whole numbers, negative ones included, satisfy it?"

5. `l2-product-and-sum.json` | `screens[1].prose` and `screens[1].canvas.state.caption` | imprecise, minor | "The table shows every pair of whole numbers with product 24" and the caption "Every pair of whole numbers that multiplies to 24", over four positive pairs. With the app's meaning of whole number (negatives included) the pairs −1 and −24, −2 and −12, −3 and −8, −4 and −6 are missing, and `screens[4]` of the same lesson lists exactly such pairs for 20. An "every" claim that is false as worded, three screens before the learner needs the negative pairs. | Eight integer pairs have product 24 (concepts script finding line 5). | `prose`: "Now the area is $x^2 + 10x + 24$. Guessing gets slow, so list the candidates. The table shows every pair of positive whole numbers with product 24." Caption: "Every pair of positive whole numbers that multiplies to 24".

6. `l9-shape-of-a-square.json` | `screens[9].explain.text`, last sentence | misleading, minor | "With $a = 0.3 > 0$ the curve opens upwards, so big moves either way help the holder: this is **convexity**." A rise in yields does not help the holder: the screen's own figure is $P(2) = 87.20$, a loss of £12.80, and $P(d) < 100$ for every rise up to 23.3 points. What convexity gives is an asymmetry: the fall in yields gains £15.20, the rise loses £12.80. "Help" is true only relative to the straight-line estimate, or for a hedged position, and neither is on the screen. | $P(d) = 100 - 7d + 0.3d^2$; Hull ch. 4 (duration and convexity): the convexity term raises the price relative to the duration estimate for a move of either sign. Concepts script finding line 6. | Replace the last sentence with: "With $a = 0.3 > 0$ the curve opens upwards, so the bond gains more when yields fall than it loses when they rise: this is **convexity**."

7. `l4-difference-of-squares.json` | `screens[6].explain.text`, `summary.trap`, `quiz[3].widget.options[id=d].why` | imprecise, minor | "we need two numbers with product 9 and sum 0, and none exist" (and "No two numbers have product 9 and sum 0", "No two numbers have product 25 and sum 0"). True for real numbers only, and the screen gives no reason. The learner meets "no real number" in l6 and l8, where the course is careful; here the same idea is stated as an absolute. The one-line reason (a positive product forces matching signs) is the argument `homework-1` part (d) later asks for, so it belongs on the screen. | For reals $pq > 0$ gives equal signs, so $p + q \ne 0$; over the complex numbers $3i$ and $-3i$ work. Gelfand and Shen, "The difference of squares formula" (a sum of squares has no such factorisation with real numbers). | `screens[6].explain.text`: "The square of side $x + 3$ has two $3x$ strips, so it is $x^2 + 6x + 9$. For $x^2 + 9$ we need product 9 and sum 0, but a positive product means matching signs, so no such pair exists on the number line. A difference of squares factorises; a sum of squares does not." `summary.trap`: "$x^2 + 9$ is not $(x + 3)^2$, which is $x^2 + 6x + 9$. No two numbers on the number line have product 9 and sum 0, so $x^2 + 9$ has no bracket factors." Option `d` `why`: "That is a sum of two squares. No two numbers on the number line have product 25 and sum 0."

Counts: wrong 2 (0 serious, 2 minor), imprecise 4 (1 serious, 3 minor), misleading 1 (0 serious, 1 minor). Seven findings: 1 serious, 6 minor. Every fix is a wording change of at most three sentences; no screen needs a rewrite.

## Read and judged correct (not findings)

- `l7` `screens[0]`: "$x^2 + 4x - 1$ will not factorise" means whole-number brackets, the only meaning level 1 gives the word, and the same sentence says the curve still crosses twice.
- `l8` `summary.formula.note`: "Below 0: none" sits beside the idea line "no real roots".
- `l12` `screens[8]`: the rule $a(x - p)(x - q) < 0 \iff p < x < q$ needs $p < q$; the screen before sets it and the summary states it.
- `l5` `summary.ideas[2]`: "Never divide both sides by $x$: it throws away the root $x = 0$" is exact. If both sides are multiples of $x$, then 0 is a root.
- `l4` `screens[8]`: "Volatility costs money even with no trend" is the standard reading of $(1 + r)(1 - r) = 1 - r^2$.
- `l13` `screens[9]` and `quiz[3]`, `l12` `screens[9]`, `homework-3` `items[8]`: each variance quadratic is the expansion of a real two-asset variance (checked with exact fractions).

## Overlap with earlier reads

Filled after the ledger and the findings above were written. Earlier reads then opened: `docs/reviews/review-quadratics-1-3.md` (26 findings and its fix pass, all applied before this commit), `docs/reviews/review-problems-0.2-b.md` (9 findings on `problems-1` to `-3`: freshness, tolerance and typed-form rows, none conceptual), the quadratics rows of `review-delta-problems-aa-2.md`, and the author reports `docs/reports/problems-quadratics.md` and `fluency-quadratics.md`. No earlier concept audit of this course exists (`concept-audit-log.md` has no quadratics row).

Conceptual findings of the earlier review (its `wrong` and its mathematical `misleading` rows): 11. They are 1, 2, 3, 6, 7, 8, 12, 13, 14, 16 and 17: five `wrong` (3, 6, 8, 13, 14) and six `misleading`. The other 15 are continuity, voice, layout and reuse.

| | count |
|---|---|
| Found by this audit only | 7 (findings 1 to 7) |
| Found by the earlier review only | 11 (all fixed before this read, so no longer in the content) |
| Found by both (same defect) | 0 |

New `wrong` that no earlier read found: 2 (findings 1 and 2, both minor slip-line mismatches). That is above the convergence limit of one new `wrong` per three levels, so the course does not close on this round.

Two of this audit's findings sit in text an earlier pass wrote or carried, which the fix-pass read rule exists for:

- Finding 7: the "no two numbers have product 9 and sum 0" wording is the earlier review's own fix for its finding 3 ("a sum of two squares has no factors at all"). The fix cured the common-factor error and left the real-number restriction unstated. Different defect, same lines.
- Finding 6: the earlier review's fix text for its finding 19 rewrote l9 `screens[9].explain` to state the answer and kept "big moves either way help the holder" as it stood.

The earlier review's finding 14 deleted a slip in `homework-3` `items[4]` and read "whole numbers" as including −1 to 4 without comment; finding 4 here is the convention under that count, not the same defect.

## Tools

- Validator: `cd app && node tools/validate.mjs`: 0 errors, 4,619 warnings (none new; no file changed).
- Number scripts: `node tools/run-number-scripts.mjs --only quadratics` with the venv Python first on PATH: 7 of 436 scripts, 7 passed, 0 new failures.
- `node tools/grade-all.mjs --file <file> --local-cdn <pkgs>` on each of the 28 files: 0 failures on every file.
- Concepts script `docs/reports/quadratics-L1-3-concepts.py`: 16,619 checks pass, 0 unexpected failures, 6 finding lines kept failing (findings 1 to 6; finding 7 is a wording finding with no number to test). Exit code 1 until the fix pass, then 0.
- No playthrough (auditor rules). Venv versions are newer than the CI pins; no figure here depends on a version.
