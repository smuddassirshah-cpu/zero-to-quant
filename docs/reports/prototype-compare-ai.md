# Prototype comparison: the reference lesson (PLAN 13 item 5)

Verdict: **equivalent with listed differences** (not identical). Item 5 says "plays identically"; that is not literally true.

Reference lesson: conditional probability lesson 3, `app/content/courses/conditional/l3-shrinking.json` (PLAN E2). Prototype: commit 646a8317 (parent of 069c5ea6), `prototype/js/screens/lesson.js`. Both walked at 1376 x 1032, one wrong answer then the right one per task, then the quiz. Screenshots: `scratchpad/prototype-compare/shots/{proto,app,compare}/` (compare = prototype left, app right). Scratchpad is under `/tmp/claude-0/-home-user-zero-to-quant/639b0236-ba38-5c74-a772-dab604bd46c7/`.

Same: 9 lesson screens plus a 3-question quiz; same order (title, shade 8, first die 5, cross, ten, derive, simulate, stocks, summary); same answers and same graded outcomes on every screen walked; same hints, XP per check (+5 on retry), Check / Try again / Why? states, quiz one-try, summary and completion figures.

| # | Screen | Class | Difference |
|---|---|---|---|
| 1 | derive | behaviour | Prototype: pick the missing line from 3 options. App: put 3 lines in order (drag or keyboard). Different widget and grading; same final line and explanation. |
| 2 | simulate | behaviour | Prototype locks the Roll buttons until the estimate is correct. App buttons are live before predicting. |
| 3 | simulate | look | Prototype: dice, Rolled/Kept/Total 10 counters, share bar, running-share trace. App: two-bar chart (Kept, Filtered out), Run 10/100/1,000, Reset. |
| 4 | stocks | behaviour/look | Prototype fills the grid on a correct answer: Both down fades, cells change from 1/4 to 1/3. App grid kept all four cells unchanged in the shot (the shrink only appears in the Why? explanation). Table is plainer in the app. |
| 5 | all choices | behaviour | App shuffles option order per page visit (backlog 591); the prototype's order is fixed. |
| 6 | shade | behaviour | Wrong-cell feedback: prototype names the cell ("(1, 1) adds to 2"). App uses it only for listed cells; (1, 1) gets the generic line. |
| 7 | shade, cross, ten | look | App shows "r, c" labels in every cell and dims non-cross cells; the prototype cells are blank. Grid sits slightly right and caption moves below the grid. |
| 8 | all tasks | look | Verdict chip is full width above the buttons (prototype: bottom left). Title "That's it." / "Correct." (prototype "Correct"). |
| 9 | cross, ten, stocks | content | Prose reworded ("you ask your friend one question", "yes", "you ask one question"). Prototype: "hear one fact". |
| 10 | first5 | content | "The marked cells" (prototype: "cells marked in orange"). |
| 11 | summary | content | Idea 3 expanded; trap sentence reordered (first leaves 11, second leaves 6). |
| 12 | quiz | behaviour | Prototype adds "Added to your Redo queue." to wrong answers; absent in the app chip. |
| 13 | complete | look/behaviour | App: real streak, next lesson, Done and Next buttons. Prototype: demo streak, "Tap anywhere to skip". |

Not checked: derive wrong-order feedback (keyboard reorder always landed on the correct order); mobile widths; the prototype's "Start over" link, absent from the app on some screens (cross, ten).

Items 1, 2 and 3 are the substantive departures; 9 to 11 are deliberate wording changes. A strict reading of item 5 should be amended to "same teaching sequence and grading, with listed differences".

## Fix pass (session AI)

Rows 2, 4 and 6 now match the prototype. Simulate: `controlsAfter: "check"` locks Run until a checked estimate. Stocks: a correct answer dims Both down and captions "each 1/3". Shade: wrong cells (1, 1), (2, 2), (3, 3), (1, 5), (5, 5), (6, 6) name their totals. Validator 0 errors; playthrough green, desktop and mobile.

## Fix pass 2 (session AI)

Row 3 now matches: `conditional/l3-shrinking` simulate uses `dice-sim` (seed 4226: 308 kept, 28 total 10, share 0.091 against 1/11). Feedback already had "Now roll to test it."; explanation now points at the share settling near 1/11. Validator 0 errors, playthrough green, desktop and mobile.
