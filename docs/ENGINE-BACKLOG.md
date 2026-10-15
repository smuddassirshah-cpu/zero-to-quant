# Engine backlog (raised by content agents; scheduled by the orchestrator)

Fix in one integration pass, then update AUTHORING.md and the canvas READMEs.

1. `tap-regions`: a count mode (`count: k`, optional `among: [ids]`) so "shade any 3 of 4" grades.
2. `validate.mjs`: area ids with 10 or more rows or columns are `c1-10`, not `c110`; accept a bare number `target` for `drag-point` on number-line and circle.
3. `area` canvas: honour `canvas.controls` bound to `split`/`grid` so the learner can re-cut; slider readouts support a `format: "fraction"`.
4. `number-line`: `labelPos` (above, below, left, right) on points and intervals; avoid label collisions with arrows and between close points.
5. `area`: grid lines inside shaded cells too faint.
6. `canvas.controls[].start`: document (AUTHORING.md and READMEs); default to the bound point's current value.
7. `ZQ.test` hook in set mode (runSet, homework, exams) so playthroughs cover reviews, homework and exams.
8. `number-line`: tap mode on points.
9. `state.practiceResult({results})`: Elo and the streak problem count for practice and weekly problems; `select.js` to call it.
10. `examFinished`: misses join the redo queue with ref `{ exam, item }`; `select.resolve` understands it.
11. `longform` widget help text: "Check" versus "Mark my answer" wording to match the homework button.
12. Today: show the weekly probability problems row from `select.weeklyStatus()`.
