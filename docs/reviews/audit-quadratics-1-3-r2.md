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

## Fix pass

Opus fixer, from `ab276fd4`. Each fix was derived from the item itself before the audit's text was used. No key, slip, hidden test or rubric line changed.

1. `problems-1` items[0].parts[3] option `last-term` | fixed | Removing a fixed number of seats leaves $x^2 + 15x + c$, so the last term can change and only $2k = 15$ blocks a square; the new text "No. Taking seats out cannot change the last term, and 44 is not a square number." has a false first clause, so the key `no-middle` is the only true option, and the existing why-line now answers it directly.
2. `l5` summary.ideas[2] | fixed differently | Division by $x$ is valid only where $x \ne 0$, so it loses a root exactly when 0 is one ($x^2 = 5x$ loses 0; $x^2 + 6x + 5 = 0$ loses nothing). New text: "Dividing both sides by $x$ can lose the root $x = 0$, so factorise instead, or check $x = 0$ separately." This keeps the lesson's method advice and adds the separate check, which the audit's wording lacked.
3. `l2` screens[5].prose and quiz[0].explain.text | fixed | $(-1)(-25) = (-5)(-5) = 25$ and $(-1)(-15) = (-3)(-5) = 15$, so "the pairs" listed only the positive ones; both lines now say "The positive pairs". "Only 3 and 5 add to 8" stays true over all integer pairs, as negative pairs have negative sums.
4. `homework-1` items[8].prompt (d) | fixed differently | The rubric's line 10 argument (positive product, so equal signs, so the sum is not 0) needs negatives in view; the prompt now reads "cannot be factorised into brackets $(x + p)(x + q)$, whatever whole numbers $p$ and $q$ are, positive or negative." I kept "whole numbers" rather than the audit's "whatever numbers", which would be false over complex numbers ($x^2 + 16 = (x + 4i)(x - 4i)$) and goes beyond the model's pair check.

Gates: validator 0 errors; `voice-scan.py 35` on the four files 0 and 0; `quadratics-L1-3-concepts-r2.py` and `quadratics-L1-3-concepts.py` exit 0 (neither encodes the changed text, so neither was re-pointed); `run-number-scripts.mjs --only quadratics` 7 of 7 passed; `grade-all.mjs --file` 0 failures on each edited file; playthrough of `l2`, `l5`, `homework-1` and `problems-1`, desktop and `--mobile`, all passed.

## Fix-pass read

Fresh reader, blind to this audit until the rows below were written. Diff read: `git show 56be4904 -- app/content/courses` (four files, five changed strings). Basis script, not committed: sympy and brute force in the reader's scratch folder (`chk.py`).

| # | File | JSON path | Claim | Verdict | Basis |
|---|------|-----------|-------|---------|-------|
| 1 | `problems-1.json` | `items[0].parts[3].widget.options[3].text` (`last-term`) | "No. Taking seats out cannot change the last term, and 44 is not a square number." is a false option, leaving `no-middle` as the only true one. | correct | Derivation: removing $c$ seats gives $x^2 + 15x + (44 - c)$, so the last term does change; the first clause is false and the option fails as a whole. Its second clause is true ($6^2 = 36 < 44 < 49 = 7^2$; run: no $n$ with $n^2 = 44$), which is what the item needs: the option now fails for one reason only, the one the unchanged `why` names. Other options rechecked by run: $(x + 6)^2 = x^2 + 12x + 36$ and $(x + 5)^2 = x^2 + 10x + 25$, both false; $2k = 15$ has no whole $k$, true. Exactly one keyed answer is true. |
| 2 | `l5-product-of-zero.json` | `summary.ideas[2]` | "Dividing both sides by $x$ can lose the root $x = 0$, so factorise instead, or check $x = 0$ separately." | correct | Derivation: dividing by $x$ is valid only for $x \neq 0$, so the case $x = 0$ is left untested; it is lost exactly when 0 is a root, hence "can". Run: $x^2 = 5x$ has roots 0 and 5, the divided form gives 5 only. Agrees with the lesson's screen on $x^2 = 5x$, the `summary.trap` and `q-divide-trap`. |
| 3 | `l2-product-and-sum.json` | ladder prose, "Try $x^2 + 10x + 25$ ..." (line 622) | "The positive pairs that multiply to 25 are 1 and 25, and 5 and 5." | correct | Run: positive factor pairs of 25 are (1, 25) and (5, 5), sums 26 and 10. The screen follows the one on $x^2 - 9x + 20$, where negative pairs were introduced, so "positive" is now needed and the list is complete. |
| 4 | `l2-product-and-sum.json` | `explain.text` of the $x^2 + 8x + 15$ question (line 1028) | "The positive pairs for 15 are 1 and 15, and 3 and 5. Only 3 and 5 add to 8." | correct | Run: positive pairs (1, 15) and (3, 5), sums 16 and 8. The negative pairs give $-16$ and $-8$, so the conclusion holds over all pairs too. |
| 5 | `homework-1.json` | `items[8].prompt`, part (d) | "$x^2 + 16$ cannot be factorised into brackets $(x + p)(x + q)$, whatever whole numbers $p$ and $q$ are, positive or negative." | correct | Derivation: needs $pq = 16$ and $p + q = 0$, so $p^2 = -16$, impossible for any real $p$. Run: no integer pair in $-200..200$; discriminant $-64$. The claim is about this one quadratic, not a family; it is true for all real $p, q$, so naming whole numbers of either sign states a weaker, still true claim, and it is exactly the set the model answer's pair check runs over ($\pm 1, \pm 16$; $\pm 2, \pm 8$; $\pm 4, \pm 4$). The model's sign argument and both (d) rubric lines still match the prompt. |

Counts: 5 rows; correct 5, wrong 0, imprecise 0, misleading 0, unverified 0. No fix needed for the diff.

Outside the diff, seen while reading the surrounding items (not counted, for the next reader):

- `problems-1.json` `items[0].parts[3].question`: "take some seats out ... for every $x$" does not say the number removed is fixed. If it may depend on $x$, removing $3x + 8$ seats leaves $(x + 6)^2$ for every $x$ (run: $x^2 + 15x + 44 - (x + 6)^2 = 3x + 8$), and the keyed "No" fails. The feedback and explain assume a fixed number. Paste-ready: "Could the cinema take the same fixed number of seats out of $x^2 + 15x + 44$, whatever $x$ is, and leave a square block $(x + k)^2$ with $k$ a whole number?"
- `problems-1.json` `items[0].parts[1].explain.text`: "Product 36 gives 1 and 36, ..." lists positive pairs only, the same pattern rows 3 and 4 fixed in l2. Paste-ready: "The positive pairs with product 36 are 1 and 36, 2 and 18, 3 and 12, 4 and 9, and 6 and 6."
