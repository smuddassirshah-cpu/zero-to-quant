# Engine pass 1: strand, badge, Quant path only (PLAN task 2b)

Backlog items 424 to 428 in `docs/ENGINE-BACKLOG.md`.

## Changed
- `app/js/content.js`: `stages()` and `courses()` honour `settings.quantOnly`; new `allStages`, `allCourses`, `topicStrand`, `strandNoteOf`, `strandBadge`, `examWritten`, `quantOnly`; `course()` carries `strand` and `strandNote`.
- `app/js/state.js`: `settings.quantOnly: false` default; `courseProgress` computed over all courses.
- `app/js/screens/learn.js`: badge on cards and topic chip row, "Target" line from the topic's `exit`, topic exam chip badge and "Not written yet" state.
- `app/js/screens/review.js`: exam list includes unwritten topic exams and badges.
- `app/js/screens/course.js`, `app/js/engine/player.js`: badge on the course page and lesson title screen.
- `app/js/screens/you.js`: "Quant path only" switch; mastery map rebuilt on change.
- `app/tools/validate.mjs`: strand rules. CSS: `components.css`, `learn.css`, `course.css`, `lesson.css`, `review.css`.
- `docs/AUTHORING.md`: section 9 and validation rule 10.

## Checks
- Validator: 0 errors. A scratch copy (outside the repo) with strand "puree", a missing `strandNote`, a blank `strandNote` and a `strandNote` with no `strand` gave exactly four errors.
- Routes playthrough passed (every new course map opens). Lesson playthroughs: number-sense, limits, regression, options passed.
- Screenshots in the session scratchpad `shots/`, light and dark: badge legible and distinct (violet pure, amber quant); no badge on untagged topics; with the setting on, Stage 1 lists 10 topics (1.10 hidden) and counts "0 of 10 topics passed"; no console errors visiting Today, Review, You, hidden course pages and a missing exam.
