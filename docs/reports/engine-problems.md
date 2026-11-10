# Engine pass: level problem sets (ENGINE-BACKLOG 845 to 851, PLAN 2d item M)

A level may carry `content/courses/<course>/problems-<n>.json`: 3 to 5 chained problems, each with 3 to 5 graded `parts`, difficulty 3 to 5 with one 5, `skills` from the level's lessons. It plays on the shared set page (no new player) at `#problems/<course>/problems-<n>`: untimed, repeatable, never a gate, each part graded with its own feedback. A level without a file is not an error. No content was added.

- Course map: the level review's card lists "Problem set"; the review's result page links to it. It locks with its level.
- XP: homework scale (50 and 5 an item right, mastery points) on the first finish only; no redo queue.
- Weekly review: problem-set items of met levels join the unseen pool. An item with parts already played correctly there (no fault found); a miss queues under the set's ref and resolves with its parts.
- Hours: in-app minutes count the set (`minutes`, else 40). Stored hours and the census "hours 3,695, gap 0" are unchanged; with sets present, outside hours fall by the same minutes.
- Playthrough flag: `node tools/playthrough.mjs --problems <course>/problems-<n>` (also `fixture/<file>`, `--problems all`, and inside `--all`; `--mobile`, `--local-cdn`). Census prints "Problem sets n (items m)".

Results: `test-validate-problems` 33/33, `test-problems` 19/19, `test-cumulative` 26/26, `test-hours-split` 209 checks, `test-fluency` 893/893, `test-engine-runtime` and `test-validate-session` pass; validator 0 errors; readiness-sums OK; one review and one Fluency set play green. Left uncommitted.

Files: `app/js/{content,hours,prereq,state}.js`, `app/js/engine/select.js`, `app/js/screens/{course,locked,review}.js`, `app/tools/{validate,playthrough,census,hours-source}.mjs`, new `app/tools/{test-problems,test-validate-problems}.mjs`, `app/tools/fixtures/problems/problems-fixture-3.json`, `app/README.md`, `docs/AUTHORING.md` (sections 5 and 7), `docs/ENGINE-BACKLOG.md`.
