# Functions levels 1 and 2 (Functions; Straight lines): second-reader findings

Scope: `app/content/courses/functions/` l1 to l9, `review-1.json`, `review-2.json`, `homework-1.json`, `homework-2.json`. Continuity skim of l10 to l18 and review-3, review-4, homework-3, homework-4 (first three screens of each lesson, terms, notation, every cross-reference to l1 to l9). Stage 0, read for a GCSE-entry learner: every step was also checked against what this course and its prerequisites (`equations` L1 and L2, and through them `number-sense` L2 and L3) have taught, and against UK GCSE notation and wording.

Functions predates the brief and report system: there is no `docs/briefs/functions.md`, no `docs/reports/functions-<n>.md` and no number script. Coverage was judged against `docs/curriculum.md` topic 0.2 and the `lessonObjectives` in `course.json`.

Method: every graded key, every `wrong[]` value and every number in prose, hints, feedback, explanations and the two longform models recomputed with exact fractions in two new scripts, plus `stated` and `claim` checks for each false claim (those fail until the claim is fixed). Every `why` and `byKey` line read against the slip it names, with the slip recomputed. The seven `expression` widgets graded with the real grader (`app/js/engine/grade.js` and Compute Engine 0.30.2 from the local CDN) on 98 learner forms (70 bare, 28 with a left-hand side). Every `drag-point` region and `slider` band checked against every target (`drag-point.js` line 86 tests every region against every point). No code items in these levels.

Tool results:
- `python3 docs/reports/functions-L1-numbers.py` (new): exit 1, 225 of 228. The three failing checks are content errors and stay failing until fixed: findings 1, 4 and 10. 29 "check by hand" lines, each a `byKey` line that describes its slip without stating the value; every one was recomputed and agrees.
- `python3 docs/reports/functions-L2-numbers.py` (new): exit 1, 191 of 195. The four failing checks are findings 6, 7, 8 and 9. 45 "check by hand" lines, all read and recomputed; all agree.
- Expression grading (scratch `expr-check.mjs`, real `grade.js` plus Compute Engine 0.30.2): 70 of 70 bare forms as intended. l1 `screens[8]` (`5(x-4)`), l2 `screens[2]` (`4x+5`), l8 `screens[2]` (`0.5x+4`), l8 `screens[3]` (`-2x+4`), review-2 `items[3]` (`2x+5`), homework-1 `items[0]` (`4x-7`) and homework-2 `items[2]` (`0.5x+2`) accept every reordered, `\cdot`, `\times`, `\frac{1}{2}x`, `\frac{x}{2}`, `x\div2`, `0.50x` and single-fraction form (`\frac{x+8}{2}`). Every listed slip returns its own key, including `x-4\times5`, `-\frac{1}{2}x+\frac{11}{2}` and `4x-28`; unlisted slips get the generic line. All 14 correct answers typed with a left-hand side (`y=0.5x+4`, `f(x)=5(x-4)` and so on) are graded wrong with the generic line: finding 5. Putting such forms in `accept` is not a safe workaround: the grader then accepts `y=5` for `y=0.5x+4` (Engine 2).
- `cd app && node tools/validate.mjs`: 0 errors (4190 warnings across the app). L1 and L2 warnings: 15. Six `key-length` (l3 `screens[0]`, l4 `screens[0]`, l7 `screens[1]`, l9 `screens[0]`, review-1 `items[5]`: finding 15; l9 `quiz[2]` "Perpendicular" against "Parallel" and "Neither" is not a giveaway). Three `O2-long-explain` (findings 13, 14, 26). One `O2-explain-answer`, l1 `screens[1]` (finding 16). Five `O2-long-sentence` of 20 to 35 words (l2 `screens[7].prose`, l8 `screens[7].prose`, l9 `screens[5].explain.text`, review-1 `items[5].prose`, homework-1 `items[6].prose`): under the 35-word gate, left as they are.
- `VOICE_BASE=app/content/courses/functions python3 docs/reviews/voice-scan.py 35`: 0 sentences over 35 words in the whole course. 3 explanations over three sentences, all in L1 and L2: l2 `screens[4]`, review-2 `items[6]`, homework-1 `items[6]` (findings 13, 14, 26). My own sweep of L1 and L2: no exclamation marks, no em-dashes, no American spellings, £ throughout, no option named by place. "edge case" four times (finding 13).
- `node tools/fresh-check.mjs --file content/courses/functions/<set>.json --min-run 10`: 0 hits for review-1, review-2, homework-1 and homework-2. A grep of key nouns found three setup repeats the n-gram check misses (findings 24 to 26). homework-2 `items[8]` (two trend-line points, predict day 30) mirrors l8 `screens[8]`, but it is a five-part synthesis that also asks for a crossing, a parallel case and a caution, so it is left.
- Playthroughs with `--local-cdn`: all 26 green on the first run (9 lessons, review-1, review-2, homework-1, homework-2, desktop and `--mobile`), no reruns, 0 browser relaunches. Screenshots sampled at 440 px and desktop (l3 `screens[4]`, l4 `screens[1]`, l5 `screens[8]`, l6 `screens[9]`, l9 `screens[6]`): one label fault (finding 27). The l9 `screens[6]` squashed-axis trap still reads as "not a right angle" at 440 px.

Format: `N. file | JSON path | severity | problem | evidence | exact fix`. Severities: wrong, misleading, voice, layout, continuity. GCSE-convention points and freshness repeats are filed as continuity.

## Findings

1. l2-table-to-rule.json | `screens[6]` | wrong | Three rows (1 to 2, 2 to 4, 3 to 8) do not fix $f(4)$. The lesson's own quiz[2] method, "the climbs grow by 2", gives climbs 2, 4, 6 and $f(4) = 14$, which is marked wrong. The screen's lesson is "a rule that fits two rows can fail the third", so the key must not rest on three rows either. | $x^2 - x + 2$ gives 2, 4, 8, then 14. L1 script check `stated l2 screens[6].question` fails. | Add a fourth known row and ask for $f(5)$: climbs 2, 4, 8 have no constant growth, so the quiz[2] method gives no rival answer.
   - `canvas.params.rows`: `[["1", "2"], ["2", "4"], ["3", "8"], ["4", "16"], ["5", "?"]]`
   - `question`: "What is $f(5)$?"
   - `widget.options`: `doubles-x` text "$10$" (why unchanged); `right` text "$32$"; `last-climb` text "$24$", why "You added the last climb, 8, again. The climbs double too: 2, 4, 8, so next 16."
   - `hints[2].text`: "Each output is double the one before: 2, 4, 8, 16, so the next is 32."
   - `feedback.correct`: "Each output doubles the one before, so $f(5) = 32$."
   - `explain.text`: "A rule that fits two rows can still fail the third. Here each output doubles the one before, so $f(5) = 32$. Always test a rule on every row."; `explain.canvas.values`: `{ "r4c1": "32" }`.

2. homework-1.json | `items[4].prose` | misleading | The item asks for the range of a call option's P&L but never says what a call pays or what a premium is. L1 has not taught options; l18 `screens[0]` defines a call from scratch. A GCSE-entry learner can only read the graph's lowest height. | review-1 `items[5]` and l3 `screens[8]` both define their payoff in the prose; this item does not. | "You buy a call option with strike £120.00 for a premium of £4.50. The call pays the final share price minus £120.00 when the price ends above £120.00, and nothing otherwise. You pay the £4.50 premium up front, so your profit and loss is the payoff minus £4.50. The graph shows it against the final share price."

3. l3-what-goes-in.json | `screens[8].widget.options[1].why` (`no-top`) | misleading | "You treated it like a call" explains a slip with a term the learner has not met (l18 defines a call). | No L1 screen defines a call option. | "You assumed the payoff keeps growing. This put pays most when $S$ is 0, and then it pays £100.00."

4. l3-what-goes-in.json | `screens[4].widget.wrong[0]` (`reversed`) | misleading | The region x 6.7 to 7.3 also holds the correct target of `hi` (7). `drag-point.js` line 86 tests every region against every point, so a learner with "highest" right at 7 and "lowest" wrong (left at 0, or at 3) is told "A point sits at 7. If it is your lowest, that is the highest output". A region cannot name its point (Engine 1). | Target `hi` is `[7, 0]`. L1 script check `l3 screens[4] no wrong[] region holds a correct target` fails. | Delete `widget.wrong[0]` (`reversed`) and `feedback.byKey.reversed`. A reversed pair then gets `byKey.lo`, "Your lowest output is off. The biggest input, 8, gives the smallest output.", which names the same idea.

5. l1-machines.json, l2-table-to-rule.json, l8-line-through-two-points.json, review-2.json, homework-1.json, homework-2.json | l1 `screens[8].question`; l2 `screens[2].question`; l8 `screens[2].question`, `screens[3].question`; review-2 `items[3].question`; homework-1 `items[0].question`; homework-2 `items[2].question` | misleading | Each question shows "$f(x) = \ldots$" or "$y = \ldots$" above an empty field with no prefix. A GCSE learner who types the whole line, as GCSE answers are written, is marked wrong and gets the generic line, which tells them to do what they did. | Real grader: all 14 left-hand-side forms of the correct answers return the generic key (`f(x)=5(x-4)`, `y=0.5x+4`, `y=-2x+4` ...). The open inbox bullet "Raised later (review equations L1 to L2)" asks for left-hand-side stripping. Do not add `y=...` forms to `accept`: the grader then accepts `y=5` (Engine 2). | Until the engine strips a left-hand side, say what to type:
   - l1 `screens[8].question` and homework-1 `items[0].question`: "Complete the rule $f(x) = \ldots$. Type only what comes after the $=$ sign."
   - l2 `screens[2].question`: "Complete the rule for this table, $f(x) = \ldots$. Type only what comes after the $=$ sign."
   - l8 `screens[2].question`, l8 `screens[3].question`, review-2 `items[3].question`, homework-2 `items[2].question`: "Complete the equation $y = \ldots$. Type only what comes after the $=$ sign."

6. homework-2.json | `items[6].widget.lines[4].text` | wrong | "If $b_1 = b_2$ the fee lines are parallel and there is no break-even" is false when $a_1 = a_2$ too: the lines coincide and every trade size breaks even. | $a_1 = a_2$, $b_1 = b_2$ gives one line. L2 script check `stated homework items[6].widget.lines[4].text` fails. | "If $b_1 = b_2$ and $a_1 \neq a_2$, the fee lines are parallel and there is no break-even"

7. l7-slope-and-start.json | `screens[5].feedback.byKey.first` | misleading | "Set $m = 5$ on the slider" asks for a move the slider cannot make: its `m` control runs from −3 to 3. | `canvas.controls[0]`: `"min": -3, "max": 3`. L2 script check fails. | "You took the first number as the gradient. With $m = 5$ the line would climb steeply instead of falling."

8. l9-parallel-perpendicular.json | `screens[5].explain.text` | misleading | "This is the one perpendicular pair the rule does not cover" says there is one such pair; every horizontal line with every vertical line is one. | `screens[7].prose` says "Neither rule covers a vertical line". L2 script check fails. | Replace the last sentence with "This is the one kind of perpendicular pair the rule does not cover."

9. l5-plotting.json | `screens[5].widget.placeholder` | misleading | The placeholder "For example 1.5" is the value of the `minus` slip, $(4 - 1) \div 2$, one keystroke from a wrong answer. | `widget.wrong[1].value` is 1.5. L2 script check fails. | `"placeholder": "For example 0.5"`

10. l4-one-output.json | `quiz[3].prose` | misleading | "Three graphs are drawn on the plane" but the item has no canvas; the graphs are only named in the options. | `quiz[3]` has no `canvas`. L1 script check fails. | "Picture three graphs drawn on one pair of axes."

11. l8-line-through-two-points.json | `quiz[2].widget.options[2].why` (`rise`, $y = 8x + 1$) | misleading | The why explains the 8 but not the $+1$, so the learner cannot see the slip. Using $m = 8$ through $(4, 1)$ would give $c = -31$; the $+1$ is the first point's height. | $8 \times 4 + 1 = 33 \ne 1$. | "You used the rise, 8, as the gradient and the first point's height, 1, as $c$. The run is 0, so the line has no gradient at all."

12. review-1.json | `items[8].widget.options[2].why` (`is-function`) | voice | "its reverse gives output 9 two inputs" does not parse. | — | "$f$ is a function, but running it backwards from 9 gives two inputs, 3 and −3. An undoing must give one input for each output."

13. l1-machines.json, l2-table-to-rule.json, l4-one-output.json, l6-how-steep.json | l1 `screens[5].explain.text`; l2 `screens[4].explain.text`; l4 `screens[3].explain.text`; l6 `screens[5].explain.text` | voice | Authoring jargon "edge case" in learner text (the number-sense review raised the same word); l2's explanation also has four sentences. | Voice scan: l2 `screens[4]` 4 sentences. | 
   - l1: replace the last sentence with "We call such a machine constant."
   - l2: "The climbs are 1, 3, 5, 7, so no single multiplier fits. Each output is the input squared: $f(x) = x^2$, so $f(6) = 36$. A table whose climb changes has no rule of the form $mx + c$."
   - l4: replace the last sentence with "A jump is fine when each input lands on one dot."
   - l6: replace the last sentence with "A vertical line is the opposite case: its run is 0, and we cannot divide by 0."

14. homework-1.json | `items[6].explain.text` | voice | Four sentences. | Voice scan. | "£500.00 and £2,500.00 stay in their lower bands, at £3.00 and £7.50. £4,000.00 is above £2,500.00, so its fee is $0.004 \times 4000 = 16$. The total is £26.50."

15. l3-what-goes-in.json, l4-one-output.json, l7-slope-and-start.json, l9-parallel-perpendicular.json, review-1.json | option texts below | voice | The key is the only long option and carries its own reason, so length gives it away (validator `key-length`; advisory rule 586). | Validator warnings listed above. | 
   - l3 `screens[0].widget.options[3]` (`none`): "No output at all"
   - l4 `screens[0].widget.options`: `five` "It gives 5", `six` "It gives 6", `average` "It gives 5.5", `right` "No single output" (whys unchanged)
   - l7 `screens[1].widget.options[0]` (`slide`): "Slides it up or down"
   - l9 `screens[0].widget.options[0]` (`never`): "Never: the gap stays at 4"
   - review-1 `items[5].widget.options[0]` (`right`): "£0.00 upwards, no top"

16. l1-machines.json | `screens[1].explain.text` | voice | The explanation never states the answer, 23 (validator `O2-explain-answer`). | — | "You doubled 10 to get 20, then added 3 to get 23. A machine never changes its rule between inputs. That is why one row lets you predict the next."

17. l4-one-output.json | `screens[2].widget.options[1].why`; `screens[6].widget.options[1].text`; `screens[6].widget.options[1].why` | continuity | "level line" is not GCSE wording; GCSE and the rest of this course say "horizontal line" (l6 `screens[5]`, l7 `screens[4]`, l9 `screens[5]`). | — | "You checked a horizontal line, not a vertical one. Two inputs sharing an output is allowed. The trouble is one input with two outputs."; option text "Yes: each horizontal line meets it at most twice"; why "You tested with horizontal lines. The test uses vertical lines, and most of them meet the circle twice."

18. l4-one-output.json | `screens[2].explain.text`; `screens[7].widget.options[0].text`, `options[2].text`; `screens[7].explain.text` | continuity | l4 uses "parabola" four times with no gloss; l10 `screens[3].prose` then bolds **parabola** as a new word. L1 side should change. | l10: "The U-shape of $y = x^2$ is a **parabola**". | s2 explain: "Each vertical line meets the U-shaped curve once: one output per input. Two inputs may share an output, as −2 and 2 share 0. That is allowed; one input with two outputs is not." s7 options: "A U-shaped curve, $y = x^2$" and "A U-shape on its side, $y^2 = x$". s7 explain: "... The circle and the sideways U-shape both have inputs with two outputs."

19. l5-plotting.json | `screens[2].prose` | continuity | L2 never names the x-axis and y-axis: it says "vertical axis", "horizontal axis" and "fee axis". GCSE uses x-axis and y-axis, and l10 and l11 use both as known words (l10 `screens[4]`, `screens[5]`; l11 `screens[1]` to `screens[3]`). | Grep of L1 and L2: no "x-axis" or "y-axis". | Append to the prose: "The across axis is the **x-axis** and the up axis is the **y-axis**."

20. l7-slope-and-start.json | `screens[2].prose` | continuity | GCSE calls $c$ the y-intercept, and l11's objective reads "Read the roots and the y-intercept of a curve"; L2 says only "intercept". | Grep of L1 and L2: no "y-intercept". | "In $y = mx + c$, $m$ is the **gradient** from last lesson. $c$ is the **y-intercept**, or just the intercept: the value of $y$ where the line crosses the y-axis, at $x = 0$."

21. l9-parallel-perpendicular.json | `screens[7].prose` | continuity | GCSE names $-\tfrac{1}{m_1}$ the negative reciprocal; L2 says "flip and change the sign" and "the flip-and-negate rule" (`screens[5]`) but never gives the GCSE term. | Grep: no "reciprocal" in L1 or L2. | Insert after the display: "$m_2$ is the **negative reciprocal** of $m_1$."

22. l5-plotting.json, homework-2.json | l5 `screens[1].explain.text`; homework-2 `items[0].explain.text` | continuity | GCSE says quadrant; L2 says "four regions" and "the bottom-left region". Low priority. | — | l5: "...The two axes split the grid into four **quadrants**, and P sits in the bottom-left one." homework-2: "...The point is in the bottom-left quadrant."

23. l2-table-to-rule.json | `screens[7].prose` | continuity | l2 is the GCSE nth-term method (difference gives the multiplier, then adjust), but "climb" is never tied to the GCSE word "difference". Low priority. | — | Add after the display: "The climb between outputs is also called the **difference**."

24. review-1.json | `items[7]` | continuity | Repeats l1 `quiz[4]`'s setup in new numbers: shares bought above the sale price, a flat fee for both trades, profit as a function of shares. | l1 `quiz[4]`: "You buy shares at £8.60 and sell them at £8.25. A flat £5.00 fee covers the round trip." | Same numbers, new setting. `prose`: "A shop buys 120 umbrellas at £24.60 each and sells them in a sale at £23.85 each. A delivery charge of £4.50 covers the order." `question`: "What is the shop's profit on the 120 umbrellas, in pounds?" `label`: "Profit on 120 umbrellas". `feedback.generic`: "Not quite right. Find the profit per umbrella first: sale price minus purchase price." `byKey.gain-sign`: "You took the gap as a gain. The shop sold below what it paid, so each umbrella loses £0.75." `byKey.fee-added`: "You added the charge back. A cost makes the loss bigger." `byKey.no-fee`: "You left out the £4.50 delivery charge." `explain.text`: "Each umbrella makes $23.85 - 24.60 = -0.75$ pounds, so $P(q) = -0.75q - 4.5$. Then $P(120) = -90 - 4.5 = -94.5$." Answer and wrong values unchanged.

25. review-2.json | `items[5]` | continuity | Repeats l6 `quiz[3]`'s setup and option set: a share chart with a stretched price axis, gradient in pounds per day, distractors "by eye", "swapped" and "whole rise". | l6 `quiz[3]`: "A chart shows a share rising from £20.00 to £26.00 over 4 days. Its price axis is stretched, so the line looks steep." | New setting, same numbers. `prose`: "A chart shows a savings pot over 10 months. Its value axis runs only from £100.00 to £101.00, so the line looks steep." `canvas.params.xLabel`: "Month"; `yLabel`: "Value (£)". Options: `right` "£0.10 per month"; `eye` why "You read the slope off the picture. The value axis covers only £1.00, which makes a gentle rise look steep."; `swapped` "£10.00 per month", why "You divided the months by the change in value. Gradient is pounds per month: £1.00 over 10 months."; `rise` "£1.00 per month", why "That is the whole rise over 10 months. Divide it by 10." `feedback.correct`: "£1.00 over 10 months." `explain.text`: "The value rises from £100.00 to £101.00, a rise of £1.00, over a run of 10 months. So the gradient is $1 \div 10 = 0.10$ pounds per month. The steep look comes from the narrow value axis."

26. review-2.json | `items[6]` | continuity | Repeats l5 `quiz[3]`'s setup (a fixed charge plus a rate per share, the fee for 400 shares); its explanation also has four sentences. | l5 `quiz[3]`: "£3.00 per trade plus £0.01 per share ... (400, £7.00)". Voice scan: 4 sentences. | Same numbers, new setting. `prose`: "A taxi fare in pounds is $y = 1.50x + 3.50$, where $x$ is the distance in miles." `question`: "What is the fare for a 4-mile journey?" `label`: "Fare for 4 miles". `feedback.correct`: "$1.50 \\times 4 + 3.50 = 9.50$." `feedback.generic`: "Not quite right. Work out the per-mile part, then add the fixed £3.50." `byKey.no-c`: "That is only the per-mile part. Add the fixed £3.50 that every journey pays." `explain.text`: "The per-mile part is $1.50 \times 4 = 6.00$, and the fixed part is 3.50. The fare is £9.50. The gradient is the rate per mile and the intercept is the fixed charge." Answer 9.5 and wrong value 6.0 unchanged.

27. l9-parallel-perpendicular.json | `screens[6].canvas.params.functions[1]` | layout | The label "$y = -0.5x + 5$" sits on its own line at $x = 7$ and reads as struck through, on desktop and at 440 px. | Screenshots `functions_l9-parallel-perpendicular-lesson-06-trap.png` and `-440.png`. | Use a point label, as `screens[0]` of the same lesson does: delete `"label"` and `"labelAt"` from `functions[1]` and set `"state": { "points": [{ "id": "gl", "x": 6, "y": 2, "label": "$y = -0.5x + 5$", "labelPos": "ne", "colour": 2 }] }`. $(6, 2)$ is on the line. Replay desktop and `--mobile`.

## Continuity

Notation in L3 and L4 matches L1 and L2 on the main points: the machine picture, $f(x)$ read "f of x", replacing $x$ by a bracketed input, ranges written $0 \le f(x) \le 9$ with filled and hollow ends, $m$ and $c$ in $y = mx + c$, gradient as rise over run, and £ money throughout. l10 `screens[0]` ("Rules like $y = 2x - 1$ gave straight lines") picks up l5 correctly. Findings 18 to 21 are continuity findings on the L1 and L2 side (parabola, x-axis and y-axis, y-intercept), and finding 2 and 3 cover option words L1 uses before l18 defines them. The two below are for the L3 and L4 reader to weigh; their files were not written here.

28. l17-running-backwards.json `screens[0]`, `screens[5]` against l2-table-to-rule.json `screens[5]` and review-1.json `items[8]` | continuity | l17 teaches "undo the last step first" as new with a near copy of l2 `screens[5]` (double, add, find the input), and l17 `screens[5]` repeats review-1 `items[8]` ($x^2$ cannot be undone because 3 and −3 both give 9). L4 side should change. | l2 `screens[5].prose`: "Running a machine backwards like this is called undoing it." | l17 `screens[0].prose`: "In l2 you undid a machine by reversing its steps. The machine $f$ doubles its input, then adds 3. A number went in and 17 came out." The $x^2$ repeat can stay: review-1 is retrieval, and l17 adds the restriction $x \ge 0$.

29. l16-machine-after-machine.json `screens[7].prose` | continuity | GCSE convention: GCSE papers write a composite as $fg(x)$, meaning $f(g(x))$. l16 uses $g(f(x))$ and $(g \circ f)(x)$ only, so a GCSE learner meets an unfamiliar notation and never sees the one on their papers. L4 side should change. | l16 `screens[7].prose`: "$(g \circ f)(x) = g(f(x))$". | Add after the display: "Exam papers often write $gf(x)$ for $g(f(x))$: the function next to $x$ acts first."

## Orchestrator

`course.json` prerequisite edge. l3 writes domains and ranges as inequalities throughout ($-2 \le x \le 3$, $-3 < x \le 2$, $x \ne 2$, $0 \le f(x) < 9$) and uses open and closed ends on a number line, without saying what $\le$ and $<$ mean. That is what `equations` l10 ("Show an inequality on a number line with open and closed ends") teaches, but functions L1 requires only `equations/L1`. l3 `screens[3].hints[1]` and `quiz[0]` also solve $x - 2 = 0$ and $x + 4 = 0$ (equations L2), which this edge covers by chain. Add to functions level 1 `requires`:

`{ "ref": "equations/l10-ranges-of-answers", "why": "Reads domains and ranges written as inequalities, such as $-2 \\le x \\le 3$ and $0 \\le f(x) < 9$, with filled and hollow ends on a number line." }`

If gating functions L1 behind equations L3 is not wanted, the content alternative is to append to l3 `screens[2].prose`: "Here $-2 \le x \le 3$ means $x$ is at least −2 and at most 3." That still leaves $<$ and $\ne$ untaught.

## Engine

1. `drag-point` (`app/js/engine/widgets/drag-point.js` line 86): a `wrong[]` region is tested against every point, so with two or more points a region can fire for a point that is correct (functions l3 `screens[4]`, finding 4). An optional `point: "<id>"` on a wrong entry, and a validator warning when a region without `point` holds any point's target, would let authors keep such slips. Inbox bullet.
2. `exprEqual` (`app/js/engine/grade.js` line 330) on two equations gives false positives: with Compute Engine 0.30.2, `y=5` is equal to `y=0.5x+4`, and `y=5x-20` to `f(x)=5(x-4)`, while `y=2x+1` is not. No live `expression` key holds `=` today, but a fixer adding `y=...` forms to `accept` would open a hole. The validator should reject `=` in an expression `answer`, `accept` or `wrong[].tex` until left-hand-side stripping (open bullet from review equations L1 to L2) lands. Inbox bullet.
3. Plane canvas: a function label on a falling line can be placed on the line itself (functions l9 `screens[6]`, finding 27). Inbox bullet.

## Fix pass

Status per finding (27 fixed, 0 disputed, 2 deferred in part; findings 28 and 29 belong to the L3 and L4 fix pass). One graded answer changed: l2 `screens[6]` key 16 to 32. Basis lines are my own derivations or the named GCSE source (DfE GCSE Mathematics subject content, algebra strand A, and the Edexcel and AQA specifications' wording).

1. fixed: l2 `screens[6]` now has rows 2, 4, 8, 16 and asks $f(5)$, key $32$ (outputs $2^x$; climbs 2, 4, 8 are not constant, so the quiz[2] method gives no rival). Slips 10 ($2 \times 5$) and 24 ($16 + 8$) recomputed; $x^2 - x + 2$ gives 14 at 4, not 16, so it fails the fourth row.
2. fixed: homework-1 `items[4].prose` defines the call payoff and the premium.
3. fixed: l3 `screens[8]` `no-top` why no longer uses "call".
4. fixed: `reversed` region and its `byKey` line removed (x 6.7 to 7.3 held the target of `hi`, 7); `lo` and `hi` lines cover a reversed pair.
5. fixed in content, deferred in engine: the seven questions say "Type only what comes after the $=$ sign". No `y = ...` or `f(x) = ...` accept form added; left-hand-side stripping is the engine agent's fix, after which the sentence can go.
6. fixed: homework-2 `items[6]` line o5 reads "$b_1 = b_2$ and $a_1 \neq a_2$". Basis: equal rates with equal fixed charges give one line, so every $x$ breaks even.
7. fixed: l7 `screens[5]` `first` no longer asks for $m = 5$ (slider stops at 3).
8. fixed: l9 `screens[5].explain.text` says "the one kind of perpendicular pair".
9. fixed: l5 `screens[5]` placeholder is "For example 0.5" (key 2.5, slips 7 and 1.5).
10. fixed: l4 `quiz[3].prose` is "Picture three graphs drawn on one pair of axes."
11. fixed: l8 `quiz[2]` `rise` why; $8 \times 4 + 1 = 33 \ne 1$ and the rise of $(4,1)$ to $(4,9)$ is 8.
12. fixed: review-1 `items[8]` `is-function` why.
13. fixed: four "edge case" sentences reworded; l2 `screens[4].explain.text` is three sentences ($f(6) = 36$ rechecked).
14. fixed: homework-1 `items[6].explain.text` is three sentences ($0.004 \times 4000 = 16$; $3 + 7.5 + 16 = 26.5$).
15. fixed: the five option sets shortened as listed (l3 `none`, l4 `screens[0]`, l7 `slide`, l9 `never`, review-1 `right`); the `key-length` warnings are gone.
16. fixed: l1 `screens[1].explain.text` states 23 ($2 \times 10 + 3$).
17. fixed: l4 `screens[2]` and `screens[6]` say "horizontal line". Basis: GCSE wording for lines parallel to the x-axis.
18. fixed: l4 "parabola" replaced by "U-shaped curve" in `screens[2]`, `screens[7]` options and explain. Basis: l10 `screens[3]` introduces **parabola** as new.
19. fixed: l5 `screens[2].prose` names the **x-axis** and **y-axis** (DfE GCSE content, coordinates strand).
20. fixed: l7 `screens[2].prose` names the **y-intercept**.
21. fixed: l9 `screens[7].prose` names the **negative reciprocal**; $-1/m_1$ is it by definition.
22. fixed: l5 `screens[1]` and homework-2 `items[0]` say quadrant.
23. fixed: l2 `screens[7].prose` ties "climb" to **difference** (the GCSE nth-term word).
24. fixed: review-1 `items[7]` is now umbrellas with the same numbers ($23.85 - 24.60 = -0.75$; $-90 - 4.5 = -94.5$). Answer and wrong values unchanged.
25. fixed: review-2 `items[5]` is now a savings pot in months, same numbers (1 over 10 is 0.10; slips 10 and 1.00).
26. fixed: review-2 `items[6]` is now a taxi fare ($1.50 \times 4 + 3.50 = 9.50$; per-mile part 6.00). Answer 9.5 and wrong 6.0 unchanged; explanation is three sentences.
27. fixed: l9 `screens[6]` label is now a point label at $(6, 2)$ (on $y = -0.5x + 5$: $-3 + 5 = 2$). Playthrough green; not re-screenshotted.
Orchestrator: fixed (orchestrator), `requires` on `equations/l10-ranges-of-answers` applied in d15d051 and 59fc047; `course.json` untouched.
Engine 1 to 3: deferred, already in the inbox.

Gates:
- Number scripts: `functions-L1-numbers.py` exit 0 (238 of 238), `functions-L2-numbers.py` exit 0 (208 of 208). Checks for fixed findings 1, 6, 7, 8, 9, 10 and 27 now require the new text or value, so a revert fails them; check for l2 `screens[6]` replaced with the new table.
- Voice scan (35): 0 sentences over 35 words and 0 explanations over three sentences, whole course. Nothing left in L3 or L4.
- Validator: 0 errors (4165 warnings app-wide); the remaining L1 and L2 warnings are the five 20-to-35-word sentences and l9 `quiz[2]` `key-length` (judged not a giveaway).
- Playthrough with `--local-cdn`: l1 to l9, review-1, review-2, homework-1, homework-2, desktop and `--mobile`: 26 of 26 All passed, no reruns. No code items in these levels.
