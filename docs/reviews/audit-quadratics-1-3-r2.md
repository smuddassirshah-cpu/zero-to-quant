# Blind concept audit, round 2: quadratics levels 1 to 3

Name `quadratics-1-3-r2`. Commit read: `970398bf`. Stage 0 course (reduced ledger depth; every graded key, wrong option, slip and stated rule has a row).

Scope: lessons `l1` to `l13`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, and the fluency sets of `l1`, `l2`, `l3`, `l4`, `l6` and `l7` (28 files). Sources: Gelfand and Shen, *Algebra* (the square of a sum, the difference of squares, Vieta's theorem, the formula for the roots, the graph and the extreme values of a quadratic polynomial, quadratic inequalities); Edexcel *Pure Mathematics Year 1/AS*, chapters 1 to 3.

Ledger: `docs/reports/audit-quadratics-1-3-r2-ledger.md`, 1109 rows: 1104 `correct`, 5 `imprecise`, 0 `wrong`, 0 `misleading`, 0 `unverified`.

Script: `docs/reports/quadratics-L1-3-concepts-r2.py`, exit 0, 29,856 checks. It was written before any earlier read was opened.

## What was checked, and how

- **Every numeric key and slip (97 widgets, 256 slips).** Part A recomputes each key from the item, and each slip as the value that the mistake its feedback line names would give. All agree with the stored values. No slip sits inside its key's band and no two slips of one item share a value. Round 1's class of fault (a slip line naming a mistake that gives a different number) does not recur: each of the 256 lines was read against its recomputed value.
- **Every expand or factorise choice (30 items).** Part B: sympy says the key equals the task, each wrong option differs, and where the task says "fully" the equal options still hold a common factor. Every "That expands to" claim in a why-line is expanded.
- **Every expression widget (13).** Part C: key equal to the task, accept forms equal to the key, slips different.
- **Solving, counting roots, inequalities, vertices, models.** Part D: 12 root sets, 11 root counts, 9 inequality items (each option parsed to a set; exactly one equals the true set) and 46 single facts, among them every profit, revenue and variance model, every completed square form and the rejected roots.
- **Canvases.** Part E: 40 labelled plane functions against their labels at 201 points across the drawn x range; five tables of values; four factor-pair tables; every drag target, slider key and sketch target.
- **Fluency.** Part F renders the templates itself and runs every distinct draw of all 20 families over the whole range of their variables (8,038 draws; the letter is fixed, as it only renames the variable). On each draw the key is recomputed from the vars, each offered slip must be the value its line names, differ from the key (by more than the tolerance for numeric sets) and differ from the other slips. 0 bad draws.
- **Rules.** Part G is a 20,000-draw guard on the vertex form, the extreme value, the discriminant cases, "opposite signs of a and c give two roots", the sign of a factorised quadratic and `(1 + r)(1 - r) = 1 - r^2`. No claim in these levels is empirical, so no Monte Carlo estimate was needed.
- **A mutation test** (three seeded faults in a scratch copy: one numeric slip, one fluency slip template, one choice key) made the script fail on each, so the checks bite.

The watch list, item by item: expanding and factorising signs (clean; every sign slip recomputed); difference of squares (clean, the `100 - x^2` order included); the zero-product rule (stated as an "if and only if", with the "only 0 has this property" argument correct); completing the square (clean, the `a` outside the bracket included); the formula and the three discriminant cases (clean; "no real roots" is said with "real" each time); dividing by `x` (finding 2, wording only); graphs (clean); rejected roots (each is named and given its reason: `l6` quiz, `review-2` items[8], `homework-2` items[3] and items[5], `problems-2` flare and can stack); "whole numbers" against integers (finding 4; elsewhere the items say "negative ones included" or sit after the convention is stated in equations level 3).

## Findings

All four are `imprecise` and `minor`. No learner would carry away a wrong rule, method or graded answer from them.

1. `problems-1.json` | `.items[0].parts[3].widget.options[last-term]` | imprecise, minor | The wrong option reads "No. The last term of a square must be a square number, and 44 is not." Each of its three statements is true: the answer to the question is No, the last term of `(x + k)^2` is `k^2`, and 44 is not a square. Only the unwritten "because" is false, so a learner who picks it has chosen nothing untrue and is marked wrong. | The key is "No" with the reason `2k = 15`; the why-line of this option itself says "Taking out seats changes the last term". Basis: an option must be false under the item's premises, not merely a weaker reason. | Replace the option text with: `No. Taking seats out cannot change the last term, and 44 is not a square number.` The why-line stays as it is: "Taking out seats changes the last term, so it could be made a square. The middle term $15x$ is what cannot change."

2. `l5-product-of-zero.json` | `.summary.ideas[2]` | imprecise, minor | "Never divide both sides by $x$: it throws away the root $x = 0$." As an absolute rule this is true only when `x = 0` is a root. The same lesson says it correctly in its feedback ("Dividing by something that might be 0 can throw a root away") and `review-2` items[1] says "Never divide by $x$ when $x$ might be 0". | `x^2 = 5x` has the root 0; `x^2 + 6x + 5 = 0` (lesson 6, where the same step is offered) does not, and there the step loses nothing. Basis: division by an expression is valid exactly where it is non-zero (Edexcel Year 1, 2.1). | Replace the idea with: `Do not divide both sides by $x$ when $x$ might be 0: that throws away the root $x = 0$.`

3. `l2-product-and-sum.json` | `.screens[5].prose` and `.quiz[0].explain.text` | imprecise, minor | "The pairs that multiply to 25 are 1 and 25, and 5 and 5", and "The pairs for 15 are 1 and 15, and 3 and 5". The screen just before lists `-1 and -20`, `-2 and -10`, `-4 and -5` as pairs that multiply to 20, so "the pairs" here are only the positive ones. Screen 1 says "positive whole numbers" correctly. | `(-1)(-25) = 25` and `(-5)(-5) = 25`. Basis: the list of factor pairs over the integers. | `.screens[5].prose`: `Try $x^2 + 10x + 25$. The positive pairs that multiply to 25 are 1 and 25, and 5 and 5.` `.quiz[0].explain.text`: `The positive pairs for 15 are 1 and 15, and 3 and 5. Only 3 and 5 add to 8. So $x^2 + 8x + 15 = (x + 3)(x + 5)$.`

4. `homework-1.json` | `.items[8].prompt`, part (d) | imprecise, minor | "explain why $x^2 + 16$ cannot be factorised into brackets with whole numbers". The model answer and the rubric test negative pairs (`±1, ±16` and so on). "Whole numbers" is said to include negatives only in equations level 3 ("Whole numbers here include 0 and negatives such as −2"), and quadratics level 1 requires equations level 1 only. A learner reading "whole numbers" as 0, 1, 2, ... can answer in one line and miss the sign argument the rubric marks. | Rubric lines 9 and 10 need "product 16 and sum 0" and "a positive product forces equal signs". Basis: the course's own convention and where it is first stated. | In the prompt, replace the last sentence with: `Then (d) explain why $x^2 + 16$ cannot be factorised into brackets $(x + p)(x + q)$, whatever numbers $p$ and $q$ are, positive or negative.`

## Read and judged correct, though a reader might pause

- `l1` screens[6]: "A squared bracket always has a middle term". True for every bracket `x + a` with `a` not 0, which is the case on screen.
- `l5` screens[1]: the sliders allow `a = b`, where the curve touches at one point. The key "At $x = a$ and at $x = b$" still holds.
- `l7` screens[0]: "No two whole numbers multiply to −1 and add to 4". Level 2 requires equations level 3, where whole numbers are said to include negatives.
- `l7` screens[4]: "$\sqrt{4a^2} = 2a$, and the ± covers either sign of $a$". Correct as written; the ± is what makes it so.
- `l6` screens[5], slip `flip` (−1): the line says "You flipped a sign". The value is what a bracket `(x − 1.5)^2` gives, and also the positive root negated, so the line fits.
- `problems-2` items[1].parts[2], slip `half-root` (−0.4641): this is `3 − √12`, the 6 halved and the root not. The line ("the whole top goes over 2") is right for it, though the id reads the other way.
- `problems-1` items[1].parts[2], slip `both-sides` (`6(x+5)^2`): the line names adding the shared side twice, which gives `2(x+5) × 3(x+5)`. Agrees.
- `l9` screens[9] and `homework-3` items[0]: the bond formula is the usual duration and convexity approximation, and the homework says where it fails.

## Runs

- `node tools/validate.mjs`: 0 errors (4,621 warnings, none new: no content was edited).
- `node tools/run-number-scripts.mjs --only quadratics`: 7 scripts, 7 passed, 0 new failures.
- `node tools/grade-all.mjs --file` on all 28 files: 468 widgets and 20 fluency templates, 0 failures.
- `docs/reports/quadratics-L1-3-concepts-r2.py`: exit 0 (sympy 1.14.0 and Python 3.13 in the scratch venv; nothing depends on the version).
- No playthrough, as the brief says.

## Overlap with the earlier reads

Filled after the ledger, the script and the findings above were written. Earlier reads then opened: `docs/reviews/audit-quadratics-1-3.md` (round 1: 7 findings and its fix pass), `docs/reviews/review-quadratics-1-3.md` (26 findings, 11 of them conceptual, and its fix pass), `docs/reviews/review-problems-0.2-b.md` (quadratics rows: freshness, tolerance and typed form, none conceptual), and the author reports `docs/reports/problems-quadratics.md` and `fluency-quadratics.md`.

| | count |
|---|---|
| Found by this audit only | 4 (findings 1 to 4, all `imprecise`, minor) |
| Found by the earlier reads only | 18 (round 1's 7 and the review's 11 conceptual; all fixed before this commit, and each fix was found in place and correct) |
| Found by both (same defect) | 0 |

New `wrong` that no earlier read found: **0**. Round 1's two `wrong` (`l7` screens[7] slip `neg`, `problems-3` arch slip `no-a`) are fixed: part A recomputes both stored values from the mistakes their new lines name (−17 from `4ac − b^2`; 100 from dropping the 0.2 and keeping its minus). Serious findings: 0. Minor: 4.

Notes on near overlaps, none counted as "both":

- Finding 2 (`l5` `summary.ideas[2]`): round 1 read the same line and judged it exact, on the ground that both sides can be divided by `x` only when both are multiples of `x`, and then 0 is a root. This audit reads it as a learner would carry it, as a rule about any equation; `l6` screens[4] offers "Divide both sides by $x$" on an equation where 0 is not a root. It is a wording call, and the fix agent may leave the line if it prefers round 1's reading.
- Finding 3 is the class of round 1's finding 5 (`l2` screens[1], "every pair of whole numbers"), on two other lines of the same lesson that the fix did not reach.
- Finding 4 is the convention under round 1's finding 4 (`l12` and `homework-3` counts), in a level 1 item that comes before the convention is stated.
- Finding 1: the option text was written in the fix for `review-problems-0.2-b` finding 1, so it has had one read fewer than the lessons.

## Engine

No engine limit met. Nothing added to `docs/BACKLOG-INBOX.md`.
