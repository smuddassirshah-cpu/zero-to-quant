# Concept audit: mental, levels 1 to 3

Blind concept audit (brief: `docs/briefs/concept-audit.md`) of `app/content/courses/mental/` levels 1 to 3: l1 to l12, review-1 to review-3, homework-1 to homework-3. Claim ledger: `docs/reports/audit-mental-1-3-ledger.md` (230 rows: correct 219, imprecise 11, wrong 0, misleading 0, unverified 0). Checks: `docs/reports/mental-L1-concepts.py`, `-L2-concepts.py`, `-L3-concepts.py`. The scripts recompute every keyed number and slip value they name from the content files, and test each always, never, every or only claim by exhaustive enumeration over its finite domain. This audit covers meaning: definitions, methods and the conditions under which they work, conventions, bounds, and the reasoning in explain, why, hint and feedback lines.

Findings are `N. file | JSON path | severity | weight | problem | evidence and basis | exact fix`. Severities: `wrong`, `imprecise`, `misleading`. Weight is `serious` (a learner would carry away a wrong definition, method, convention or graded answer) or `minor` (wording or precision that changes no understanding).

No `wrong` and no `misleading` finding was made. No graded key, accepted answer or slip value is wrong, and no `wrong[]` option is correct under a valid alternative method. Every finding is `imprecise`: true under a hypothesis or a reading that the text drops. Eight findings: one serious, seven minor.

## Level 1

1. l1-left-to-right.json | screens[1].explain | imprecise | minor | "Adding tens changes only the tens digit." The lesson's own screens[5] has 66 + 50 = 116, where the hundreds digit changes too. What never changes is the units digit, which is the point the next sentence makes. | `L1-concepts.py:l1_units_ride_along` (units digit unchanged for all 810 two-digit start and tens-jump pairs) and `l1_tens_digit_only` (450 of the 810 also change the hundreds digit). Place value. Ledger row l1 screens[1].explain. | screens[1].explain.text: "You jumped three tens: 57, 67, 77. Adding tens never changes the units digit. The 7 units ride along."

2. l3-making-100.json | screens[3].prose; summary.ideas[2]; quiz[1].prose | imprecise | minor | The digit rule "tens to 9, units to 10" is given as the definition of the complement and again in the summary with no exception. Screens[2].explain states the exception once ("except numbers ending in 0"), and homework-1 items[2] carries the hypothesis, but the lines a learner revises from do not. Quiz[1] then extends the rule to pence, "every digit goes up to 9 except the last, which goes up to 10", which fails for every price ending in 0p: for £37.40 it asks for a digit of 10. | `L1-concepts.py:l3_complement_rule` (the rule holds for 90 of the numbers 1 to 99 and fails exactly on 10, 20, ..., 90); `l3_pence_rule` (holds for the 9,000 amounts under £100 whose last digit is not 0, fails on the other 999); `l3_pence_rule_general` (with "the last digit that is not 0" it holds for all 9,999). Derivation: 100 - (10t + u) = 10(9 - t) + (10 - u) needs 10 - u to be a digit, so u is not 0. | screens[3].prose: "The partner is the **complement to 100**. Tens to 9, units to 10, unless the number ends in 0. The complement of 37 is 63." summary.ideas[2]: "The complement to 100 takes the tens to 9 and the units to 10, unless the number ends in 0." quiz[1].prose: "You pay for a £37.45 item with a £100 note. With pence, every digit goes up to 9 except the last, which goes up to 10. If the price ends in 0, use the last digit that is not 0."

3. l4-running-total.json | quiz[3].widget.options[1].why | imprecise | minor | "Each number moved by at most 2 when rounded, so the total can be off by no more than 6." The bound 6 is right, but it does not follow from the reason given: four numbers each moved by at most 2 give at most 8. The 6 comes from the actual moves 1, 2, 2 and 1, as the explain and option a say. The line reaches the right number by a step that is not valid. | `L1-concepts.py:l4_quiz3_inference` (moves [1, 2, 2, 1], sum 6; 4 x 2 = 8). Triangle inequality: the error of the sum is at most the sum of the moves. | options[1].why: "You allowed too much slack. The four numbers moved by 1, 2, 2 and 1 when rounded, so the total can be off by no more than 6."

## Level 2

4. l5-tables.json | screens[6].prose; objectives[2] | imprecise | minor | "$a \times b = b \times a$ halves the table" and the objective "Use symmetry to halve the facts you need to learn". Symmetry leaves 78 of 144 facts, which the lesson itself teaches, and quiz[3] keys 72 with the id `halved` as a slip. The loose wording invites the very answer the quiz marks wrong. | `L2-concepts.py:l5_78_facts`, `l5_halves` (78 of 144 is 54%). Count of unordered pairs from 1 to 12: 12 + 132 / 2. | screens[6].prose, last sentence: "And $a \\times b = b \\times a$ cuts the table from 144 cells to 78 facts." objectives[2]: "Use symmetry to cut the 144 cells to 78 facts".

5. l6-splitting.json | screens[1].widget.options[1].why; screens[1].feedback.generic; screens[1].explain | imprecise | minor | The key (cut 23 at 20 and 3) is justified by "both pieces are table facts", and the 12 and 11 cut is dismissed because "12 × 7 and 11 × 7 both need their own working". But 12 × 7 = 84 and 11 × 7 = 77 are facts of the 12 by 12 table that l5 has just drilled, so the stated criterion also fits the wrong option. The key is still the better cut, for a reason the text does not give: 140 + 21 adds without a carry and 84 + 77 does not. | `L2-concepts.py:l6_cut_criterion` (the only cut of 23 with both parts at most 12 is 12 and 11; 84 and 77 are in the table). l5 summary.ideas[1] teaches 12n = 10n + 2n and 11n = 10n + n for recall. | options[1].why: "You cut near the middle. 12 × 7 = 84 and 11 × 7 = 77 are table facts, but adding them needs a carry." feedback.generic: "Not quite right. Look for a cut at a ten, so the two pieces add without a carry." explain.text: "Every cut gives the same total, 161, because the rectangle never changes. Cutting at 20 gives $2 \\times 7$ with a zero and $3 \\times 7$, which add without a carry. That is the cut to reach for."

6. l8-squaring.json | screens[4].explain; screens[6].prose; summary.ideas[2]; objectives[2] | imprecise | serious | The shortcut is stated as a rule for "two numbers either side of a round number": they "multiply to its square, less the gap squared", and "the strips always cancel". That holds only when the two numbers are the same distance from the round number. For 18 × 21 the strips are $-40$ and $+20$, they do not cancel, and the product is 378, not $400 - 4$ or $400 - 1$. Every worked case (19 × 21, 18 × 22, 17 × 23, 37 × 43) has equal gaps and the formula $(a - b)(a + b)$ carries the condition, but the rule in words, which is what a learner recalls under the clock, drops it in four places, with the word "always". | `L2-concepts.py:l8_equal_gaps_only` and `l8_either_side`: of the 648 pairs with one number 1 to 9 below and one 1 to 9 above a multiple of ten from 20 to 90, the strips cancel in exactly the 72 with equal gaps. Identity: $(r - g)(r + h) = r^2 + r(h - g) - gh$, and the middle term vanishes only when $g = h$. | screens[4].explain.text: "The strips $+20$ and $-20$ cancel, leaving $400 - 1 = 399$. Two numbers the same distance either side of a round number multiply to its square, less the gap squared. Here the gap is 1, so $1^2 = 1$ comes off." screens[6].prose: "For two numbers the same distance either side of a round number, the strips always cancel. For any $a$ and $b$, $$(a - b)(a + b) = a^2 - b^2$$ Now give a reason for each line of $19 \\times 21$." summary.ideas[2]: "The same distance either side of a round number, the strips cancel: $19 \\times 21 = 20^2 - 1^2 = 399$." objectives[2]: "Multiply two numbers the same distance either side of a round number with $(a - b)(a + b) = a^2 - b^2$". For consistency, the three prompts that say only "sit either side" can name the gap: l8 quiz[1].prose "18 and 22 sit 2 either side of 20."; review-2 items[9].prose "17 and 23 sit 3 either side of 20."; homework-2 items[5].prose "Beyond the squares to 20, the same pattern still works. 37 and 43 sit 3 either side of 40."

## Level 3

7. l9-missing-multiplication.json | screens[4].prose | imprecise | minor | "The 4 times table stops at 48, so 96 is off the table." 96 is in the 12 by 12 table, as 8 × 12 and 12 × 8, and screens[2] has just taught that a number can sit in several places. What is true is that 96 is past the end of column 4. | `L3-concepts.py:l9_96_off_table` (96 sits in cells r8c12 and r12c8, and in no cell of column 4). | screens[4].prose: "Now $96 \\div 4$. Column 4 stops at 48, so 96 is past the end of it. Picture a rectangle 4 tall with area 96, cut into $80 + 16$."

8. l12-against-the-clock.json | summary.ideas[2] | imprecise | minor | "Split at multiples of the divisor, not at round numbers: 126 is 70 + 56 for 7." The good split is itself at a round number, 70, as are 120, 140 and 90 in the lesson's other splits. The contrast the trap screen draws is with the hundred (100 + 26) and with the tens of the number (120 + 6), neither a multiple of 7. | Screens[7] options and explain; `L3-concepts.py:l12_splits`. | summary.ideas[2]: "Split at multiples of the divisor, not at the hundred or the tens: 126 is 70 + 56 for 7."

## What was checked and held

- Graded keys and slip values: every numeric key, table cell, tap set and ordered derivation in scope was recomputed (exact fractions for money and decimals). All agree. No `wrong[]` value lies within its answer's tolerance, and the accept lines that name alternatives (l10 screens[4], review-3 items[5]) match the tolerances.
- Compensation direction (l2, l7): the correction sign is right in every screen, quiz, review and homework item, for sums, differences and products.
- Always, never, every and only claims that hold: the complement rule with its stated exception (l3 screens[2]); units that add to 10 always pair into a ten (l4); the digits of 9n add to a multiple of 9 (l5, checked to n = 99,999); 99 is the only 9-row product whose digits do not add to 9; 56 appears only as 7 × 8 and 8 × 7; the 11 shortcut with its carry condition holds for all two-digit numbers (l6); splitting both numbers always gives four pieces; never split the divisor (l9, no positive counter-example); r is always less than b (l10); halving 10% gives 5% every time (l11).
- Estimate bounds (l4, homework-1): the true total lies within the summed rounding moves of the estimate (triangle inequality, 20,000 seeded cases), and each cited bound (8, 6, 9, and £1 in the longform) is right.
- Conventions: bid, ask and spread (l3); hedge ratio as pounds of index per pound of stock (l7, homework-2); variance as volatility squared, variances of independent risks adding, and annualising by the square root of 252 trading days (l8); simple return as profit over capital (l10, review-3, homework-3). Each matches standard usage and is said where it first matters.
- Zetamac claims (l6, l7, l9, l12) match the app's copy of the default settings in `app/content/warmup.json`. The vendor site was not reachable, so the check is against the app.

## Overlap with the earlier second read

Read after the ledger and findings were committed: `docs/reviews/review-0.5.md` (2 errors, 8 warnings, 13 notes, with its Fix pass). Its findings on the exam, on sentence length, on layout and on the order in which methods are introduced (percentages used before l11) are outside a concept audit and are not counted. Its conceptual findings inside this scope are seven, all fixed before this audit read the files, so this audit could only confirm the fixed text. Each of the seven is a `correct` row in the ledger now.

| Earlier conceptual finding (review-0.5) | State when audited | This audit |
|---|---|---|
| l4 screens[2]: two right answers for the number with no partner | fixed (31) | key unique, `L1:l4_odd_one` |
| homework-1 items[9] model (d): "£10 away" was £10.50 | fixed | `L1:hw1_longform_estimate` |
| l5 screens[1].explain: tens up, units down fails from 90 to 99 | fixed | `L2:l5_nines_digit_sum` |
| l8 screens[7].explain: variances add only for independent risks | fixed | `L2:l8_variances_add` |
| l9 quiz[1].prose: largest Zetamac answers reach 100 was false | fixed (division answers) | `L3:l9_zetamac_division` |
| l10 screens[4], quiz[1]: tolerance accepted the chopped value | fixed (0.00035) | `L3:l10_sixth_tolerance` |
| review-3 items[5]: tolerance accepted 0.8334 | fixed (0.00035) | tolerance recomputed, ledger row review-3 items[5] |

| Conceptual findings | Count |
|---|---|
| Found by this audit only | 8 (findings 1 to 8; 0 wrong, 8 imprecise; 1 serious, 7 minor) |
| Found by the earlier review only | 7 (2 errors, 3 warnings, 2 notes; all already fixed) |
| Found by both | 0 |

Reading: the earlier read caught every false number and wrong grading that this audit could find evidence of, and this audit found no new `wrong`. What the single read missed is one class: a rule stated in words without the condition that makes it true (findings 2, 5, 6, 7 and 8), plus two loose inferences (1 and 3) and one loose count (4). On the convergence rule the course meets the test for closing: no new `wrong` in three levels.

## Checks run

- Concepts scripts, from the repo root with `python3 -I`: `docs/reports/mental-L1-concepts.py`, `mental-L2-concepts.py` and `mental-L3-concepts.py` all exit 0. No `EXPECTED_FAIL`, since no content was found wrong; the eight imprecise claims are printed as `note` lines or cited from the passing checks beside them.
- Validator, from `app/`: `node tools/validate.mjs` gives 0 errors, 4110 warnings (repository-wide count). It rewrote no tracked file.
- Voice: `VOICE_BASE=app/content/courses/mental/ python3 docs/reviews/voice-scan.py 35 --summary` gives 0 explanations over three sentences and 0 of 5,226 sentences over 35 words. Every proposed fix above keeps to three sentences and under 35 words a sentence.
- Author number scripts: none exists for this course (`docs/reports/mental-L*-numbers.py` is absent). The concepts scripts recompute the keyed numbers and can serve as the committed recompute script for the fix pass.
- Playthrough with `--local-cdn`, desktop and `--mobile`: `--lesson mental/l3-making-100`, `--lesson mental/l8-squaring`, `--lesson mental/l12-against-the-clock` and `--set mental/homework-2` all end "All passed".
- Engine limits met: none, so nothing was added to `docs/BACKLOG-INBOX.md`.

## Fix pass

Bases computed in my own scratch script, independent of the auditor's checks.

1. fixed | basis: (n + 10k) mod 10 = n mod 10 for every two-digit n and k from 1 to 9, while 66 + 50 = 116 moves the hundreds digit (450 of the 810 pairs do). Auditor's text.
2. fixed, with my own quiz[1] sentence and one further repeat | basis: 100 − (10t + u) = 10(9 − t) + (10 − u) needs 10 − u to be a digit, so u ≠ 0; enumeration over 1 to 99 fails exactly on 10, 20, ..., 90. For pence, the last-digit rule holds on 9,000 of 9,999 amounts, the last-non-zero-digit rule on all 9,999; £100 − £37.40 = £62.60 both ways. quiz[1].prose reads "If the price ends in 0, the last non-zero digit goes up to 10 and the zeros stay.", since the auditor's "use the last digit that is not 0" did not say what happens to the zeros. screens[8].prose, a general statement of the same rule not named in the finding, now ends "unless $a$ ends in 0". Item-specific hints and feedback ("Tens to 9, units to 10." on 58, 64 and 73) are left: none ends in 0.
3. fixed, in shorter words | basis: |29 − 30| + |52 − 50| + |38 − 40| + |71 − 70| = 1 + 2 + 2 + 1 = 6, whereas four moves of at most 2 bound only 8. Text: "You allowed too much slack. Rounding moved the numbers by 1, 2, 2 and 1, so the total is off by at most 6." The auditor's sentence passed the 35-word gate but drew a new under-20 warning, so I shortened it.
4. fixed | basis: unordered pairs from 1 to 12 number 12 + 66 = 78, set-counted directly; 144 / 2 = 72 is the keyed slip. Auditor's text.
5. fixed | basis: the only cut of 23 with both parts at most 12 is 12 and 11; 84 and 77 are table cells and 84 + 77 carries in the units, while 140 + 21 carries nowhere; both give 161. Auditor's text.
6. fixed, all four plus the three prompts and one further repeat | basis: (r − g)(r + h) = r² + r(h − g) − gh, so the strips cancel only when g = h; 18 × 21 = 378, not 396 or 399; enumeration over r = 20 to 90 and gaps 1 to 9 gives 72 cancelling pairs of 648, exactly the equal gaps. Auditor's text, except summary.ideas[2], which I wrote as "For two numbers the same distance either side of a round number, the strips cancel: ..." because the auditor's opening phrase had no subject. screens[6].explain "so they always cancel" now reads "so they cancel", since "always" there reread as the general rule. Gaps named: l8 quiz[1] (2), review-2 items[9] (3), homework-2 items[5] (3); 22 − 20 = 20 − 18, 23 − 20 = 20 − 17, 43 − 40 = 40 − 37.
7. fixed | basis: the cells of the 12 by 12 table holding 96 are r8c12 and r12c8 only; column 4 ends at 4 × 12 = 48. Auditor's text.
8. fixed | basis: 126 = 70 + 56 with 70 = 7 × 10 and 56 = 7 × 8, so the good split is itself round; 100 and 120 leave remainders 2 and 1 on division by 7. Auditor's text.

Counts: fixed 8, disputed 0, deferred 0.

Graded answers changed: none. No key, `wrong[]` value, slip, tolerance or lesson id changed; only prose, objectives, summary ideas, explain, why and feedback lines.

Concepts scripts: the seven `note` lines (l1_tens_digit_only, l3_rule_without_exception, l4_quiz3_inference, l5_halves, l6_cut_criterion, l8_either_side, l9_96_off_table) are now checks marked "(corrected claim, fix pass)". Each recomputes the corrected claim and asserts the content states it and no longer states the old wording. New checks: l3_change_ends_in_0, l8_gap_named, l12_split_contrast. No check was weakened.

Checks:
- Validator (from `app/`): `0 errors, 4110 warnings`, the audit's count; it rewrote no tracked file.
- Voice (35): `# explanations over three sentences: 0`, `# sentences scanned: 5227; over 35 words: 0`.
- Concepts scripts with `python3 -I`: `mental-L1-concepts.py`, `-L2-`, `-L3-` exit 0.
- Playthrough (`--local-cdn <pkgs>`) of l1-left-to-right, l3-making-100, l4-running-total, l5-tables, l6-splitting, l8-squaring, l9-missing-multiplication, l12-against-the-clock, review-2, homework-2: desktop and `--mobile` all `All passed.`
