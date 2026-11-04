# Prerequisite gating: brief

User request, 4 Nov: a lesson stays locked until the lessons it relies on are learned, so foundations are solid before a topic is started; a locked lesson shows which stages, topics, courses and lessons must be completed first. Research summary and sources in "Evidence" below. Two passes: an engine pass (this brief, sections 1 to 7) and a content pass that writes the `requires` lists (section 8). Number engine items into `docs/ENGINE-BACKLOG.md` from 481.

## Evidence (summary)
- Mastery learning raises exam scores by about 0.5 SD on average, most for weaker learners, at a cost in time (Kulik, Kulik and Bangert-Drowns 1990, 108 studies; Slavin 1987 argues smaller effects on standardised tests).
- Free choice of sequence adds almost nothing to achievement (Karich, Burns and Maki 2014, g about 0.05); weaker learners do better with a logical maths order. Autonomy still matters for motivation, so a gate needs an escape.
- ALEKS (knowledge space theory) offers only the "outer fringe", items whose prerequisites are mastered; Math Academy unlocks a topic as soon as its own prerequisites are mastered, not a whole unit, and admits that a wrong graph edge blocks learners falsely.
- Duolingo's "Jump here" unlocks a later unit by a short test.
Conclusion: gate at the level grain on demonstrated mastery, with test-out and (outside Strict mode) an override.

## 1. Data
- `course.json`: each level may carry `requires: ["<course>/L<n>", "<course>/<lesson-id>", ...]`. A level reference means the whole level; a lesson reference is for the few cases where one lesson is enough. Same-course references are allowed (`"markov/L2"`). The first level of a course with no `requires` is open; a later level with no `requires` implicitly requires the previous level of its own course.
- (As built: the override is a top-level `lessonRequires: { "<lesson-id>": [refs] }` map, because map entries are strings; see DECISIONS.) A lesson may override with `requires` in its `course.json` lesson map entry only when it needs less or more than its level (rare; the content pass justifies each one in its report).
- Topics and stages carry no `requires`; their order comes from the levels inside them.
- Lesson ids are never renamed, so progress data and references stay valid.

## 2. What counts as met
A level reference is met when any of these holds:
1. the level review (`review-<n>`) has a passed attempt (the review's own pass rule), or
2. the level's topic exam is passed (tested out, as today), or
3. a stage exit test covering that topic is passed, or
4. the learner passed a test-out check for that level (section 4).
A lesson reference is met when that lesson is finished and its quiz passed, or its level is met. Opening a lesson never counts. A met prerequisite stays met: nothing that was unlocked ever locks again (progress data is never taken away). Old saves: on the first load after this pass ships, every level whose lessons are all finished is recorded as met (once, in state), so a learner's finished work never locks.

## 3. Locking and the locked card
- A level is locked while any of its references (and, transitively, theirs) is unmet. Lessons, review and homework of a locked level are locked.
- The course map draws locked nodes with a lock and no "Jump ahead"; the route `#lesson/...` to a locked lesson opens the locked card instead of the lesson.
- The locked card lists what is missing, grouped Stage, then Topic, then Course, then level and lesson, each group with a count ("Stage 1 › 1.5 Probability › markov: 3 of 5 lessons, review not passed"). Direct prerequisites come first and open by default; indirect ones collapse into one line per stage ("and 14 more in Stage 1"), expandable. The first missing lesson (the earliest in curriculum order whose own prerequisites are met) is a primary button, "Start here".
- Each missing level offers "Test out" (section 4). Outside Strict mode a secondary "Open anyway" opens the lesson and records the override (shown on You as "Opened early: 3").

## 4. Test-out
A short check for one level: up to 6 items drawn from that level's `review-<n>` items (seeded, shuffled), passed at the review's pass share. Pass marks the level met; a fail shows which items were missed and links to their lessons, and can be retaken after 24 hours. A level with no written review cannot be tested out; its lessons must be finished. Reuse the set player (no new item kinds).

## 5. Strict mode
Setting on You, Settings, Study plan: "Strict prerequisites" (`settings.strictPrereqs`), **on by default** (the user asked for a solid foundation first). On: no "Open anyway"; test-out stays. Off: "Open anyway" shown. Prep paths, the bank (`requires` already gates items) and mocks follow the same lock; a mock whose papers draw from locked levels shows the locked card naming them.

## 6. Today, Learn and Prepare
- Today and Learn pick the next lesson among unlocked ones only; if the learner's chosen course is locked, Today says so in one line and offers "Start here".
- The Prepare page marks each blocked step with a lock and its first missing prerequisite.
- Forgetting: a met prerequisite not reviewed for 30 days shows a "Refresh" chip on the dependent lesson's start screen (a link to its review); it never relocks.

## 7. Validator, playthrough, docs
- Validator: every reference names an existing course and level or a lesson of that course map (written or not); no cycles across all courses (report the cycle); no reference from an earlier stage to a later one (error) or to a later topic in the same stage (warning); a reference to an unwritten level is a warning (the dependent level would be unreachable until it is written).
- `--routes-only` checks: a fresh profile sees the first lessons of Stage 0 unlocked and a Stage 3 lesson locked with a correct card; test-out unlocks; Strict mode hides "Open anyway"; an old save with finished lessons is grandfathered.
- `--lesson`, `--set`, `--exams`, `--bank` keep working: the playthrough marks every prerequisite of the target met before playing it (as `--bank` does for `requires` today).
- Document `requires`, the met rule, test-out and Strict mode in `docs/AUTHORING.md` (new section 11) and the learner-facing behaviour in `app/README.md` if it describes navigation.

## 8. Content pass: writing the `requires` lists
One mapping agent (like the prep mapping of 2 Nov), then a second reader. Sources: each brief's "Context" and "Builds on" lines, `docs/curriculum.md`, `docs/briefs/breadth-plan.md` and `gaps-plan.md`, and the lesson objectives. Rules: list only direct prerequisites (the engine follows the chain); prefer the smallest set that the level genuinely uses; a Pure course never gates a Quant or interview course (`strand`); interview courses (topics 0.7, 3.3, 3.5) gate only on what their briefs name, so the interview path is not held behind unrelated breadth courses. The report lists, per course, each level's references with a one-line reason, and the depth of the longest chain. The mapping agent may edit every `course.json` for this field only (an exception to the content-agent rule, recorded in DECISIONS).

## Acceptance
Validate 0 errors with the lists in place and no cycles; routes checks above green with and without `--mobile`; full split playthrough green; AUTHORING section 11 written; a fresh profile can reach a Stage 3 interview lesson by finishing or testing out of exactly the levels its card lists.
