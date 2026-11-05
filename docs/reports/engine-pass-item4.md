# Engine pass, PLAN 2c item 4: met rule rewrite (ENGINE-BACKLOG 528)

Findings addressed: N02, N03, F05.1 to F05.4 (`docs/reviews/review-course-correction.md`).

## What changed

| Rule | Constant | Where | Behaviour |
|---|---|---|---|
| 1 Review pass | `PASS = 0.8` (`prereq.js`), `REVIEW_PASS = 0.8` (`state.js`) | `reviewFinished`, `review.js` fallbacks | Reads the review file's `pass`; fallback now 0.8, equal to MASTERY. The main session writes `"pass": 0.8` into each review file after merge. |
| 2 Skill floor | `SKILL_FLOOR = 0.7` (both files; the test asserts they match) | `reviewFinished`, `prereq.reviewPassed`, `review.js` test-out | `passedAuto` needs the aggregate pass and every skill tagged on the items at 0.7 over auto rows in that attempt. The record keeps `essential`, `bySkill`, `passBySkill`. Met also needs `skills[s].seen > 0`. Test-out applies the floor to the skills it drew (no `seen` test: a test-out earns no skill record). |
| 3 Reveal cap | `REVEAL_CAP = 0.25` (`state.js`) | `screenGraded`, `lessonFinished`, `lessonCounts` | Lesson records keep `revealed` (screen indices, added only while the lesson is unfinished, cleared by an honest solve on replay) and `gradable` (from `lessonFinished` `firstTry[1]`, which is task screens plus quiz items). `lessonCounts` is false above the cap. Used by `lessonDone` (so `fullyFinished`, `launchOf`, `nodeOf`), `lessonMet` and `summary()` figures. Raw `done` still unlocks and keeps a level started. Revealed screens never call `rate()`. No `player.js` edit was needed. |
| 4 Exam coverage | uses `SKILL_FLOOR` | `examFinished`, `prereq.examMeets`, `content.js` | Exam attempts now store `bySkillAuto` (auto and external rows). A topic or stage pass meets a level only if one passing attempt covers all the level's essential skills at the floor. Essentials come from the level review's item skills, kept as reviews load (`essentialSkills`) and preloaded by `prereq.sync` for courses whose exam is passed (`loadEssentials`). Unknown essentials mean not met until loaded. |
| 5 Quiz redo | none | `quizFinished` | Misses always queue. |

Docs: `docs/AUTHORING.md` section 11 (met rule, test-out line). Backlog item 528.

## Decisions and caveats

- Old review records with `passedAuto: true` and no `essential` stay met (no per-skill data to re-judge); levels already in `state.prereq.met` stay met.
- The reveal cap's denominator includes quiz items, as `player.js` `GRADED` does. A revealed note on the learner's screens was not added (not cheap: several screens read `done`); finished lessons still show as finished.
- Topic and stage exam `pass` values (0.7) are unchanged; only level met changed. `exam.js` was not in scope.
- Tests are logic-level (real state, content and prereq with fake storage and fetch). The test-out floor is checked through the shared helper and a source check of `review.js`; the DOM flow is covered by the playthrough.
- `docs/AUTHORING.md` tells authors to tag review items with the skills the level should prove; a skill on one item must be right.

## Verification

- `node app/tools/test-met-rule.mjs`: 10 of 10 (one test per rule, the reveal-everything acceptance learner with zero levels met and zero lessons counted, and the cold review 8 of 10 with and without the floor).
- `node tools/validate.mjs`: 0 errors.
- Playthrough `--all --routes-only`, with and without `--mobile`: see the hand-back line.
