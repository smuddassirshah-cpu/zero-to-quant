# Mobile overflow, engine pass AH (CI run on 74f4f090)

Cause of the 41 entries in 29 sets, all engine faults, none a probe false positive (the probe already allows 1 px and skips boxes that scroll sideways):

1. Inline maths over 34 characters was the only span set in a scrolling box (`.lsn-wide`). Spans of 15 to 34 characters (chains of equalities, `Var(...)` lines) stayed `white-space: nowrap` and ran past a 440 px line. Threshold now 14 (`js/engine/grade.js`, `texLen`).
2. `.lsn-set` (set-mode column) was a grid with an automatic column, so one wide child stretched the progress caption row and the prose to 470 to 490 px. Column is now `minmax(0, 1fr)` (`css/screens/lesson.css`).
3. The self-marking rubric (`.wd-rubric`, `.wd-rbs`) had the same automatic column; rows now shrink (`css/widgets.css`), points label stays on one line.
4. Homework header title (`.hw-ttl-a`, `.hw-ttl-n`) was one line cut with an ellipsis; it now wraps at phone width (`css/screens/review.css`).

Probe changes (`app/tools/playthrough.mjs`): the "maths span" culprit search skips spans that scroll inside their own box; a stretched element names the ancestors that run past the window; lesson screens are probed (see below).

Entries needing a content rewording: none. All 29 sets pass `--mobile`.

Lesson coverage: the probe now runs on every lesson screen under `--mobile` (before answering: prose, options, widgets; again with the feedback and explanation open). Not probed: the lesson end card and the quiz result page beyond the existing page-width check.
