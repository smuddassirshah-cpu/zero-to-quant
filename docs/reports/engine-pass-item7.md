# Engine pass, item 7 (dependency rationale, route limitation, closure tool)

PLAN 2c item 7, engine part (F02, F03). ENGINE-BACKLOG 551 to 555. Gates and the Strict default are unchanged. No content was edited.

## What changed

- **Schema (551).** A level's `requires` entry, and a `lessonRequires` entry, is a string or `{ ref, why, gate }`. Exam files stay strings (the validator rejects objects there; mocks are not course edges). One normaliser in `js/prereq.js`: `entryOf`, `entriesOf`, `refsOf`, `whyOf`; the file also exports them to node (`createRequire(import.meta.url)('../js/prereq.js')`), so tools share it. `levelRefs`, `lessonRefs`, `examRefs` return gating strings, so `engine/select.js` and `engine/mock.js` (item-level `requires`, always strings) needed no change. Readers converted: `prereq.js`, `screens/exam.js`, `screens/prepare.js`, `tools/readiness-sums.mjs`, `tools/census.mjs`, `tools/validate.mjs`, `tools/closure.mjs`, playthrough 7d.
- **Why shown (552).** Lock card row (under each missing prerequisite), Learn node card (first missing), Prepare step lock line. Diagnostics (`gate: false`): "Check first: <name>. <why>" plus "Sit its review as a check" on the lock card, the lesson start screen (`engine/player.js` strip) and the Learn node card.
- **Validator (553).** Unknown keys, `why` one line, under 20 words, no em-dash, `gate` boolean, `gate: false` needs `why`; a cross-course entry without `why` is a warning, an error with `--strict-why`. Prints `Requires: 248 cross-course edges, 248 without why`. Warning total at HEAD is now 2352 (2104 plus 248). Scratch cases: `app/tools/test-validate-why.mjs` (11 cases: string, object, missing why, strict, long, em-dash, multi-line, diagnostic ok, diagnostic without why, unknown key, bad ref), all pass.
- **Route limitation (554).** `ZQ.prereq.routeLimits`, `routeLimitsForCourse|Level|Lesson`, `routeText`. "Route limited: <course> unwritten" (or "partly unwritten") as one chip per course on the Learn course card, Learn node card, lock card, lesson start and each Prepare step plus the path header. Own course excluded; `gate: false` edges excluded. pdes shows odes, numerics and complex (level 1 of complex has no written lesson, so it is a real limit). The static `limited.pdes` text from `readiness.json` is hidden on the card while the computed label exists. Playthrough 7d2 (inside `--routes-only`) compares the engine list with one computed from `course.json` and lesson files for every course, and checks the Learn card for pdes.
- **Closure tool (555).** `app/tools/closure.mjs`. At HEAD:
  - `--target mock-superday-trader`: 107 levels, 35 courses, 470 mapped lessons (all written), no unwritten course. This is the review's trader figure.
  - `--target mock-superday-research` and `mock-oa-quant-data`: 89, 32, 375. `--target mock-oa-code`: 38, 16, 163.
  - Level targets exclude the level itself and match the review: research-int/L1 61, systems/L1 55, coding-int/L1 27, puzzles/L1 27, brainteasers/L1 7.
  - `--role trader` (union of its present mocks, which adds the OA and SIG mocks): 109 levels, 35 courses, 479 lessons.
  - `--target pdes/L3` reaches unwritten odes and numerics (plus complex L1).
  - `--proposal-template <file>` wrote 248 edges (checked to /scratchpad); `--edges` lists cross-course edges in a closure with `why`.
- **Census.** The "Levels fully written" summary line gains `cross-course requires edges 248, without why 248`.

## Counts

Cross-course edges without `why`: **248 of 248** (level `requires` and `lessonRequires` together, duplicates not counted).

## Verification (from `app/`)

- `node tools/validate.mjs`: 0 errors, 2352 warnings.
- `node tools/readiness-sums.mjs`: exit 0. `test-met-rule` 17 of 17, `test-validate-perf` 33 of 33, `test-validate-versions` 5 of 5, `test-validate-why` 11 of 11.
- `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>`: All passed, with and without `--mobile`. Full `--all` not run, as asked.
- Scratch copy of `app/` (not the repo): `pdes` level 1 got `{ref: odes/L4, why}` and `{ref: ito/L3, why, gate: false}`, `ito` level 1 got an object entry. Validator 0 errors; `closure.mjs --target pdes/L1` drops from 91 to 60 levels (the diagnostic leaves the closure); `--routes-only` passed there too.

## For the main session

- Apply the `why` entries from `closure.mjs --proposal-template <file>` into `course.json`, then run the validator with `--strict-why` and consider making it the default.
- Playthrough 7a (Refresh chip candidate search, near line 1556) reads `lv.requires` as strings and skips object entries silently; harmless but it will find fewer candidates once content converts. It sits outside the 7d block the sharding agent leaves me, so I did not touch it.
- There is no Learn course-card "Check first" line; diagnostics show on the lock card, lesson start strip and Learn node card.
- Not done: no DOM-level test of the "Check first" card (covered by the API and the validator cases only).
