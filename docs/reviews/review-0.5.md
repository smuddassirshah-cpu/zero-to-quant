# Topic 0.5 (Mental arithmetic): second-reader findings

Scope: every lesson, review and homework file in `app/content/courses/mental/` (l1 to l12, review-1 to review-3, homework-1 to homework-3) and `app/content/exams/topic-0.5.json`.
Method: every keyed answer recomputed twice, once by hand from the screen text and once in Python with `fractions.Fraction` (script in the reviewer's scratchpad folder `read-0.5`). That covers each numeric answer, table cell, choice key, order line and the two longform models, and every `wrong[]` value re-derived from its byKey line. Grading was checked against the engine (`grade.js` `parseNum` and `within`, which adds 1e-9 to `tol`): alternative forms (`£95.33`, `1/12`, `8.33%`, `3,000`, `−5.25`) and borderline wrong answers were probed. Style was scanned with a script (`style.py`: exclamation marks, em and en dashes, dollar amounts, American spellings, sentences over 20 words, explanations and byKey lines over three sentences, prose over 60 words). Playthrough from `app/` with `--local-cdn` and `--mobile --shots`: all 12 lessons, all six sets and the exam pass ("All passed", exam 20 of 20). Screenshots at 390 px and desktop were looked at for l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, homework-1 and the exam.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, overstated claim, grading that accepts or rejects the wrong thing, or a binding-rule breach; note = style or layout. Screen, item and quiz numbers are zero-based.

All keyed answers check, with one exception. That is l4 s2, where the key is one of two right answers. The rechecked figures include every sum and gap in level 1 (95.33, 23.42, 27p, 62.55, the running totals 38, 26, 71, 42, 99 and 12.40, 4.55, 27.65, 12.00), every product in level 2 (296, 1044, 564, 290, 3000, 6336, 0.0324, 1152, 8232, 12000, 1591, 7225, 0.0576, 588) and every division, decimal and percentage in level 3 (95.50, 0.1667, 0.5833, 4.75, 4.83, 0.4167, 0.0833, 57.80, 127.40, 42, 5070 and 3380, 98.50, 0.003, 0.125, 128.25, 425.50, 15, 0.0417, 143.50, 1.722, 0.25). The exam answers (85 to 6.5%) all check. Rubrics sum to 10. No exclamation marks, no em or en dashes, £ throughout, no American spellings. No code screens in the topic. The exam ramp is 4, 10, 4 and 2 items at difficulty 2 to 5, and all four skills are tagged.

## Level 1 (adding and subtracting)

- app/content/courses/mental/l4-running-total.json | screens[2] | error | "Tap the one number with no partner" among 18, 25, 32, 15, 22 has two right answers. 18 pairs with 22 or with 32 (8 + 2 = 10 either way), so 22 is as much the odd one out as 32. The key accepts only 32, and the byKey line for 22 ("22 pairs with 18") rejects the other valid pairing. | Change C to 31: canvas row `["18","25","31","15","22"]`. Nudge "Which units digits add to 10: 8, 5, 1, 5, 2?". FC "31 is the odd one out.". Explain "$18 + 22 = 40$ and $25 + 15 = 40$. The 31 is left over, so the total is $40 + 40 + 31 = 111$." The key `r0c2` and the other byKey lines stand.
- app/content/courses/mental/l1-left-to-right.json | screens[4] byKey `t2` | note | "The $+2$ is the hop that reaches the ten" states the rule but does not name what the learner did (it fires when +2 sits in the second slot). | "You put the $+2$ after 70. It is the hop from 68 to 70, so it goes first."
- app/content/courses/mental/l3-making-100.json | screens[4] prose | note | 21-word sentence. | "For $83 - 47$, start at 47 and count up to 83. Go to the next ten, then by tens, then the rest."
- app/content/courses/mental/l4-running-total.json | screens[5] explain | note | Third sentence has 21 words. | "146 is 24 below 170, so it is wrong. Your friend left out the 22; the true total is 168." (The explain stays at three sentences if the first two are merged: "The estimate is 170, and rounding moved the numbers by 2, 1, 3 and 2, at most 8 in all.")
- app/content/courses/mental/homework-1.json | items[2] prose | note | 24-word sentence. | "A two-digit number's complement to 100 has its tens digit up to 9 and its units digit up to 10. Show why."
- app/content/courses/mental/homework-1.json | items[9] rubric[0] | note | 22-word line. | "Finds £96.00 for the two buys. Names a mental method, such as pairing 96p with 4p."
- app/content/courses/mental/homework-1.json | items[9] model (d) | note | "£16.50 is £10 away from £6": it is £10.50 away. | "£16.50 is more than £10 away from £6, so it cannot be right."

## Level 2 (multiplying)

- app/content/courses/mental/l7-near-round.json | quiz[2] `q-hedge` | warning | The feedback works in per cent ("less 1% of it", "take 1% of £6,400", "You took off 10%"), but percentages are taught in l11, a level later. The rule "never state a rule before the learner has used it" is broken in a level-2 quiz. | FC "£6,400 less a hundredth of it: £6,400 − £64 = £6,336." FG "0.99 is 1 less 0.01, so take a hundredth of £6,400 off £6,400." byKey `one-not-lot`: "You took £1 off. The gap is 0.01 of every pound, so take off a hundredth of £6,400, which is £64." `ten-percent`: "You took off a tenth. 0.99 is 0.01 below 1, so take off a hundredth: £64." `added`: "You added a hundredth. 0.99 is below 1, so it comes off." The explain already uses 0.01.
- app/content/courses/mental/review-2.json | items[7] `rv-return-notional` | warning | Same sequencing break. The prose sets up the multiplication route ($0.025 = \tfrac{25}{1000}$), but FC, FG, byKey and explain switch to "a quarter of 10%", an l11 method. | FC "£400,000 ÷ 1,000 = £400, and 25 × 400 = £10,000." FG "0.025 is 25 thousandths. Divide by 1,000, then multiply by 25." byKey `twenty-five`: "That is 0.25 of the book. 0.025 is ten times smaller." `point-25`: "That is 0.0025 of the book. 0.025 is ten times bigger." `halved-once`: "That is 50 lots of £400. Halve again for 25 lots." Explain: "£400,000 ÷ 1,000 = £400. 25 lots of £400 is a quarter of 100 lots, £40,000, so £10,000. It is the ×25 move: a quarter of a round number." (Checked: 50 × 400 = 20,000; 250 × 400 = 100,000; 2.5 × 400 = 1,000.)
- app/content/courses/mental/homework-2.json | items[3] `hw-hedge`, items[4] `hw-notional` | warning | Same break: "2% of £8,400", "1% of the book is £48,000", "0.25% is a quarter of 1%". | items[3]: FC "£8,400 less 0.02 of it: £8,400 − £168 = £8,232." FG "0.98 is 0.02 below 1, so take two hundredths of £8,400 off." byKey `gap-only` "... take off 0.02 of £8,400, which is £168."; `one-percent` "You took off one hundredth, £84. The gap is two hundredths, so take off £168."; `added` "You added 0.02 of it. 0.98 is below 1, so it comes off." Explain "... A hundredth of £8,400 is £84, so 0.02 of it is £168." items[4]: prose "A £4,800,000 book returns 0.0025 of its value today, which is 25 ten-thousandths." FC "£4,800,000 ÷ 10,000 = £480, and 25 × £480 = £12,000." FG "Divide by 10,000, then multiply by 25." byKey `two-point-five` "That is 0.025 of the book, ten times too big."; `too-small` "That is 0.00025 of the book, ten times too small."; `one-percent` "That is 100 lots of £480. 25 lots is a quarter of it."; `halved-once` "That is 50 lots of £480. Halve again for 25 lots." Explain "£4,800,000 ÷ 10,000 = £480. 100 lots of £480 is £48,000, and a quarter is two halvings: £24,000, then £12,000." Alternatively, move both items to homework-3 as they stand.
- app/content/courses/mental/l8-squaring.json | screens[7] explain | warning | "Risk models add variances, not volatilities" is overstated. Variances add only for independent (uncorrelated) risks. | "Variances of independent risks add and volatilities do not, so this square comes up all the time."
- app/content/courses/mental/l5-tables.json | screens[1] explain | note | "So the tens digit climbs by one and the units digit falls by one" fails from 90 to 99 and from 99 to 108, the very cells the screen is about. | "From 9 to 90 the tens digit climbs by one and the units digit falls by one, so their sum stays at 9."
- app/content/courses/mental/l8-squaring.json | quiz[2] `q-root-252` FG | note | "Which square to 20 is nearest 252?" is unclear. | "Which of the squares up to $20^2$ is nearest 252?"

## Level 3 (dividing and fractions)

- app/content/courses/mental/l9-missing-multiplication.json | quiz[1] `q-seven-hundred` prose | error | "The largest answers in a default Zetamac round reach 100" is false. The default multiplication range is 2 to 12 times 2 to 100, so products reach 1,200 and sums reach 200. Only the division answers stop at 100. | "In a default Zetamac round, division answers go up to 100."
- app/content/courses/mental/l10-known-decimals.json | screens[4], quiz[1] `q-two-thirds` | warning | `tol: 0.0004` around 0.167 and 0.667 accepts 0.1666 and 0.6666, the chopped four-place values. Those are the slip these screens teach against. The tolerance also accepts 0.1674. | `tol: { "abs": 0.00035 }` on both. Checked with the engine's 1e-9 slack: it accepts 0.167, 0.1667 and 0.16667 (and 0.667, 0.6667, 0.66667), and rejects 0.1666, 0.1674 and 0.6666.
- app/content/courses/mental/review-3.json | items[5] `r-five-sixths` | warning | `tol: 0.0004` around 0.833 accepts 0.8334, a wrong rounding of 0.83333. | `tol: { "abs": 0.00035 }`. It accepts 0.833, 0.8333 and 0.83333, and rejects 0.8334.

## Exam (topic-0.5)

- app/content/exams/topic-0.5.json | items[15] `m-halve-both` | warning | The keyed method, "Halve both: 189 ÷ 7", appears nowhere in the course. l9 and l12 halve only the number being divided. The item is solvable by the taught split, but its FC, FG and explain teach a new rule in the exam. | Title "Past the table". FG "Split 378 into two multiples of 14." FC "$280 \div 14 + 98 \div 14 = 20 + 7 = 27$." Explain "378 = 280 + 98, and both are multiples of 14. That gives $20 + 7 = 27$. Check: $27 \times 14 = 378$." byKey `one-side`: "54 is $378 \div 7$. The divisor is 14, so the answer is half of that." (Checked: 14 × 20 = 280, 14 × 7 = 98, 378 ÷ 7 = 54.) Or add "halve both numbers" to the l12 method card first.
- app/content/exams/topic-0.5.json | items[3], items[13], coverage | warning | No item examines l10's core content: remainders as decimals, and the sixths, eighths and twelfths. Items[3] (7/20) and [13] (3/40) test conversions the course never teaches. The exam also has no item on ×5, ÷5 or ×11, and it uses 20 of the allowed 30 slots. | Replace items[13] with a new item `m-remainder-eight` (difficulty 3, skills `ma-div`, `ma-frac`): "What is 43 ÷ 8 as a decimal?", answer 5.375, `tol: { "abs": 0.0005 }`, wrong `rem-digit` 5.3, `rem-hundredths` 5.03, `whole` 5. FC "5 remainder 3, and $\tfrac38 = 0.375$: 5.375." Replace items[3] with `m-one-sixth` (difficulty 2, `ma-frac`): "What is 1/6 to two decimal places?", answer 0.17, `tol: { "abs": 0.0005 }`, wrong `chopped` 0.16, `digit` 0.6, `flip` 6. FC "$\tfrac16 = 0.1666\ldots$, which rounds to 0.17." Both keep the ramp. Optionally add a d3 item on 5 × 86 or 165 ÷ 5 and one on 11 × 68 (with two more at 2, 4 and 5 to hold the ramp).
- app/content/exams/topic-0.5.json | items[0] `m-add-bridge` | note | FC, FG and explain teach "add the tens, then the units, then combine" (70 + 15). That is the side-by-side route l1 warns about, not the course's left-to-right stops. | FC "47, 77, 85." FG "Add 30, then 8, bridging through 80." Explain "From the left: $47 + 30 = 77$. Then 3 reaches 80 and 5 more gives 85."
- app/content/courses/mental/l3-making-100.json screens[9], quiz[3]; review-1.json items[5]; homework-1.json items[5] | note | The pence fields (`unit: "p"`) leave "27p" unparsed: `parseNum` strips a leading £ but not a trailing p, so Check stays disabled. A learner who types the unit gets no response. | Engine bullet in `docs/BACKLOG-INBOX.md`: let `parseNum` drop a trailing unit that matches the widget's `unit`. No content change.

## Layout (playthrough screenshots)

- app/content/courses/mental/l4-running-total.json | screens[3] | note | At 390 px the `−18` arc stacks above the `+27` arc, and its label sits on the `+27` line. | `"side": "below"` on arrow `a2`.
- app/content/courses/mental/l2-round-and-adjust.json | screens[2] | note | The correction arrow (`a2`, a jump of 1 or 2) draws as a small loop above the point, with its `−1` label crowded into the loop at 390 px. | `"side": "below"` on `a2` in `state.arrows`; the `derive` keys still apply.
- (engine) l5 screens[0] to [5], l9 screens[1] to [3] | note | At 390 px the 12 × 12 grid and the 1 × 12 rows give cells about 22 px wide with digits near 8 px. They are readable but small touch targets for a tap task. | ENGINE-BACKLOG: a minimum cell size on `grid`, with the canvas scrolling sideways, or wrapping a single row of 12 into two rows of 6.

## Counts

2 errors, 8 warnings, 13 notes.

## Fix pass

Targeted string edits only; no file was regenerated, and no lesson, screen or item id changed except the exam items replaced below. The exam file was edited through Python's `json` module, which round-trips it byte for byte, so its diff holds only the changed items. Every number I touched was recomputed by hand and in Python with `fractions.Fraction` (script `check.py` in the scratchpad folder `fix-0.5`), and each new tolerance was probed with the engine's 1e-9 slack. A scan of every added line finds no exclamation mark, em or en dash, and no new sentence over 20 words.

Status: fixed 21, disputed 0, deferred 2 (engine changes). Where a fix differs from the proposal, the line says why. Screen, item and quiz numbers are zero-based, as in the findings.

### Level 1 (7)

1. l4 s2 (error): fixed as proposed. The row is 18, 25, 31, 15, 22, with units 8, 5, 1, 5, 2; the only pairs to a ten are 18 + 22 and 25 + 15, so 31 is the one odd number. The nudge, FC, explain and caption now say 31 and $40 + 40 + 31 = 111$. Key `r0c2` and the byKey lines are unchanged.
2. l1 s4 byKey `t2`: fixed as proposed.
3. l3 s4 prose: fixed as proposed.
4. l4 s5 explain: fixed with the merged first sentence, so it stays at three sentences. Checked: $48 + 31 + 67 = 146$ and $48 + 31 + 67 + 22 = 168$.
5. homework-1 items[2] prose: fixed as proposed.
6. homework-1 items[9] rubric[0]: fixed as two sentences. I kept "or adding from the left", since the model gives both methods; the second sentence is 15 words.
7. homework-1 items[9] model (d): fixed, "more than £10 away" ($16.50 - 6 = 10.50$). The sentence then ran to 21 words, so it is split before "It looks like an extra ten crept in."

### Level 2 (6)

8. l7 quiz[2] `q-hedge`: fixed as proposed; FC, FG and all three byKey lines now work in hundredths. Checked: $6400 - 64 = 6336$, $6400 - 1 = 6399$, $6400 - 640 = 5760$, $6400 + 64 = 6464$.
9. review-2 items[7] `rv-return-notional`: fixed as proposed (FC, FG, the three byKey lines and the explain). The prose keeps "2.5% in a month" as the stated return, since it turns it into 0.025 and $\tfrac{25}{1000}$ at once. Checked: $400{,}000 \div 1{,}000 = 400$, $25 \times 400 = 10{,}000$, and the wrong values 100,000, 1,000 and 20,000 are 0.25, 0.0025 and 50 lots of £400.
10. homework-2 items[3] and [4]: fixed in place with the proposed wording, not moved to homework 3. items[3]: $8400 - 168 = 8232$; wrong values $8398$, $8316$, $8568$ check. items[4]: the prose now gives 0.0025 as 25 ten-thousandths; $4{,}800{,}000 \div 10{,}000 = 480$ and $25 \times 480 = 12{,}000$; wrong values 120,000, 1,200, 48,000 and 24,000 are 0.025, 0.00025, 100 lots and 50 lots. The explain ends "It is the ×25 move again." The byKey ids (`one-percent` and so on) are internal and unchanged.
11. l8 s7 explain: fixed as proposed.
12. l5 s1 explain: fixed with different wording. The proposed sentence is 23 words, and splitting it would make four sentences. It now reads "Each step adds 9, one ten up and one unit down. From 9 to 90 that keeps the digit sum at 9. At 99 the sum is 18, still a multiple of 9."
13. l8 quiz[2] FG: fixed as proposed.

### Level 3 (3)

14. l9 quiz[1] (error): fixed as proposed, "In a default Zetamac round, division answers go up to 100."
15. l10 s4 and quiz[1]: fixed, `tol: { "abs": 0.00035 }` on both. Probed: 0.167, 0.1667 and 0.16667 pass, 0.1666 and 0.1674 fail; 0.667, 0.6667 and 0.66667 pass, 0.6666 and 0.6674 fail.
16. review-3 items[5]: fixed, `tol: { "abs": 0.00035 }`. 0.833, 0.8333 and 0.83333 pass; 0.8334 and 0.8326 fail.

### Exam (4)

17. items[15] `m-halve-both`: fixed with the taught split. Title "Past the table"; FC "280 ÷ 14 + 98 ÷ 14 = 20 + 7 = 27."; FG "Split 378 into two multiples of 14."; the proposed explain. The `one-side` line adds "twice 7" so it says why the answer is half of 54. The id stays. Checked: $14 \times 20 = 280$, $14 \times 7 = 98$, $378 \div 7 = 54$, $27 \times 14 = 378$, $14 \times 26 = 364$.
18. Coverage: fixed by replacing two items and adding two.
    - items[3] `m-seven-twentieths` is now `m-one-sixth` (d2, `ma-frac`): "What is 1/6 to two decimal places?", 0.17, `tol` 0.0005, wrong `chopped` 0.16, `digit` 0.6, `flip` 6. $\tfrac16 = 0.1666\ldots$ rounds to 0.17.
    - items[13] `m-three-fortieths` is now `m-remainder-eight` (d3, `ma-div`, `ma-frac`): "What is 43 ÷ 8 as a decimal?", 5.375, `tol` 0.0005. Wrong values: `rem-digit` 5.3, `one-eighth` 5.125 and `whole` 5. I used 5.125 (one eighth for a remainder of 3) in place of the proposed 5.03, which names no slip the course teaches against. Checked: $8 \times 5 = 40$, remainder 3, $3 \times 0.125 = 0.375$.
    - Added `m-times-eleven` (d3, `ma-mult`): 11 × 76 = 836, wrong `no-carry` 7136, `lost-carry` 736, `ten-only` 760. I used 76, not 68, because $11 \times 68$ is l6's own worked example. Checked: $760 + 76 = 836$ and $7 + 6 = 13$.
    - Added `m-divide-five` (d3, `ma-div`): 165 ÷ 5 = 33 by doubling, then dividing by 10, as l12 teaches. Wrong `no-tenth` 330, `halved` 82.5, `times` 825. Checked: $5 \times 33 = 165$.
    - The exam now has 22 items at 4, 12, 4 and 2 (18%, 55%, 18%, 9%), inside the ±10% ramp, with all four skills tagged.
19. items[0] `m-add-bridge`: fixed as proposed (FC, FG, explain). I also reworded the `no-carry` line to the left-to-right route: "You lost a ten. From 77, the 8 crosses 80, so the answer is past 80." Checked: $47 + 30 = 77$, $77 + 3 = 80$, $80 + 5 = 85$.
20. Pence fields and "27p": deferred, as the finding says. The `parseNum` bullet is under "Raised later (fix pass 0.5)" in `docs/BACKLOG-INBOX.md`. No content change.

### Layout (3)

21. l4 s3: fixed, `"side": "below"` on `a2`. At 390 px the −18 arc now sits under the axis with its label clear; the 55 label stays below, beside the arc's end (screenshot looked at).
22. l2 s2: fixed, `"side": "below"` on `a2`. At 390 px the correction loop and its −1 label sit under the axis, away from the +30 arc (screenshot looked at). The `derive` keys still drive it.
23. Grid cell size (l5, l9): deferred, an engine change. The bullet is in the inbox and points to the two earlier grid bullets asking for the same thing.

### Acceptance

From `app/`, with `--local-cdn`:
- `node tools/validate.mjs`: 0 errors (385 warnings, none in `mental/` or topic-0.5).
- `--lesson`: l1, l2, l3, l4, l5, l7, l8, l9 and l10 pass; l2 and l4 also with `--mobile`.
- `--set`: homework-1, homework-2, review-2 and review-3 pass.
- `--exam topic-0.5`: 22 of 22, passed.

Graded answers changed: three tolerances (l10 s4 and quiz[1], review-3 items[5], 0.0004 to 0.00035). In l4 s2 the cell under key `r0c2` now reads 31, so the key is unique. In the exam, two items were replaced (0.35 and 0.075 out; 0.17 and 5.375 in) and two added (836 and 33). Every other keyed option, cell and number is unchanged. Not changed: `course.json`, any lesson id, engine files.
