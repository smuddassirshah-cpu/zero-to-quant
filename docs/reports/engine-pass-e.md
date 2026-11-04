# Engine pass E: prerequisite gating (items 481 to 490)

Brief: `docs/briefs/prereq-gating.md` sections 1 to 7. Author docs: `docs/AUTHORING.md` section 11. Learner docs: `app/README.md` ("Moving around: locked lessons"). Backlog: `docs/ENGINE-BACKLOG.md` items 481 to 490 (all Done).

## What was built
- `app/js/prereq.js` (`ZQ.prereq`): the rules. Level and lesson references, the implicit previous-level rule, the met rule, locked checks, `missingFor` / `missingForLevel` / `missingRefs` (direct, indirect, Start here), `refreshFor`, test hooks `unlock` and `unlockRefs`, `sync` (records levels found met, grandfathers an old save once).
- `app/js/state.js`: `doc.prereq { met, testouts, opened, grandfathered }`, `ZQ.state.prereq.mark/testout/open/grandfather`, `settings.strictPrereqs` (default true), a sticky `passed` on review records (`reviewFinished({ pass })`, default 0.7; a review file may carry `pass`).
- `app/js/screens/locked.js` and `css/screens/locked.css`: the locked card, shared by lesson, review, homework and mock routes.
- `review.js`: `#testout/<course>/<n>` on the set page; locks on `#review` and `#homework`. `lesson.js`: lock on `#lesson`. `exam.js`: a mock with `requires` shows the card. `course.js`: locked nodes. `today.js`, `learn.js`: unlocked lessons only, Today's locked line. `prepare.js`: lock marks. `you.js`: the Strict switch and the opened-early tile. `player.js`: the Refresh chip.
- `tools/validate.mjs`: the rules in AUTHORING section 11, plus `pass` on a review. `tools/playthrough.mjs`: `unlockRoute` before lessons, sets and mocks; `gatingChecks` in `--routes-only`.

## Decisions the brief left open
- Lesson-level override: a top-level `lessonRequires: { "<lesson-id>": [refs] }` in `course.json` (the brief's "lesson map entry"; the map entries are strings, so a sibling map is used). It replaces the level's list for that lesson; the level's review and homework keep the level's list.
- Mocks: an optional top-level `requires` on `exams/mock-*.json` (same format). Without it a mock is never locked. No item or draw is inspected.
- A review has no pass rule in content today: the default is 0.7 (`ZQ.prereq.PASS`), overridable by `"pass"` in the review file. A record from before this pass counts as passed when score over items is at least 0.7.
- A level with no written review is met when every written lesson is finished (test-out needs a written review).
- Met is cut at the first met level when walking the chain: a met level satisfies its own chain, so grandfathered or tested-out work never drags its unmet ancestors back into the card.
- A finished lesson, an existing review or homework record, and a level opened early are never locked.
- The learner's starting stage does not unlock anything.
- A met record is also written for every level found met by derivation (`sync`), so a later change (a review written, a pass rule changed) never relocks.

## Verification (from `app/`)
- `node tools/validate.mjs`: 0 errors (432 warnings, none new).
- Scratch copies of `content/` (outside the repo): a good fixture (explicit `requires` across courses with an indirect chain, `lessonRequires`) passes `--routes-only --mobile`, showing "and 1 more in Stage 1"; a bad fixture gives the expected errors (unknown course, level, lesson, self reference, non-string, earlier-to-later stage, `lessonRequires` on a missing lesson), the unwritten-level warning and the later-topic warning; a cycle prints `conditional/L1 -> conditional/L2 -> conditional/L1`; `pass: 2` on a review errors.
- `--routes-only` with and without `--mobile`: all passed (card checked at 1280 and 390 px, no horizontal overflow). Screenshots of the card, the test-out result and the locked map node looked at in both widths.
- Smoke: lessons `puzzles/l7-cards-and-colours` (a locked level 2 lesson), `markov/l1-only-now`, `first-python/l5-decisions`; sets `markov/review-2`, `puzzles/homework-2`; exams `topic-1.5`, `mock-oa-sig`; `--bank all` (200 of 200); `--drills` (all passed). The full `--all` was not run (the orchestrator runs the split).

## For the mapping agent
- Write `requires` on levels in `course.json` (and `lessonRequires` only where a lesson needs less or more). Validate after each course: unknown refs and cycles are errors; earlier-stage-to-later is an error; later topic in the same stage is a warning.
- A reference to a level with no written lesson (momentum-rep L2, ito L2 and so on) is a warning and keeps the dependent locked until it is written. Reference written levels where the brief allows.
- `"requires": []` makes a later level open (it overrides the implicit previous-level rule); omit the field to keep the implicit rule.
- Add `requires` to a mock only if it should be locked (no mock has one now).
- After mapping, a Stage 3 level 1 may be locked too: the routes check picks the first Stage 3 (else Stage 2) level 2 lesson and checks the card against the rules, so it holds either way. If a course's level 1 has `requires` that Stage 0 first lessons depend on, the check "a Stage 0 first lesson opens on a fresh profile" will fail: keep the first level of the first Stage 0 course open.
- The check "Today with a Stage 3 start" only asserts a locked line when no Stage 3 course has an open lesson.

## Not done / notes
- The work is left uncommitted in the worktree: the engine agent's standing rule forbids git write commands, so the commit the launch message asked for is for the orchestrator to make.
- Review "passed" is not shown on the course map node (a review node still draws done after any attempt, as before).
