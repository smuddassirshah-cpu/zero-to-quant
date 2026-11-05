# Engine pass, PLAN 2c item 5: performance tasks (ENGINE-BACKLOG 529)

Finding addressed: N07 (`docs/reviews/review-course-correction.md`). Rules: DECISIONS "Performance tasks (5 Nov 2026, user decision)".

## What changed

| Part | Where | Behaviour |
|---|---|---|
| Kind and shapes | `app/tools/perf-rules.mjs` (`checkTask`, `howOf`), `validate.mjs` `perfItem` | `"performance": "code" | "derivation" | "aloud" | "data"` on a homework or review item; shape errors per kind. |
| Verb rule | `perf-rules.mjs` `matchVerb`, `validate.mjs` `perfLevel` | Reads lesson-file `objectives` of a written level (all lessons, review and homework present). |
| Grandfathering | `app/tools/perf-pending.json`, `perf-pending.mjs` | `--write` regenerates, `--prune` drops levels that gained a task. Matched and unlisted without a task: error. Listed without: one count warning. Listed with a task: "remove from perf-pending". |
| Manifest | `validate.mjs` | `manifest.perf`: `"course/L<n>" -> { file, item, kind, how }`, so the engine needs no extra fetch. |
| Met hook | `state.js` `perfPass`, `content.js` `perfOf`, `prereq.js` `perfNeeded` `perfPassed` `derivedMet` `levelMet` | Extra AND on review, topic, stage and no-review routes; a `testout` record counts only with the task. Grandfathered `finished` records and sticky `derived` records are exempt. |
| Storage | `state.perf["course/L<n>"] = { item, kind, how, at }` | Written by `homeworkSubmitted` and `reviewFinished` for a result row carrying `perf` that is `ok`; `how` is the row's provenance (`auto`, `self`, `external`). Sticky. Level from `level` (homework) or the `review-<n>` id. |
| Screens | `review.js`, `locked.js` | Rows carry `perf`; the locked card says "performance task not passed"; the test-out note says the pass is a badge until the task is passed. |
| Widgets | `longform.js`, `numeric.js`, `_base.js` `dataPanel`, `widgets.css` | `seconds` (clock, never locks, box optional) and `followUps` (shown before the model) on longform; `data` panel (download link, first rows) on numeric and longform. |

## Counts and reconciliation

Rule-matched written levels: **111** (Stage 0: 4, Stage 1: 63, Stage 2: 22, Stage 3: 22), equal to the DECISIONS figure at 1e67d6f. Written levels (all lessons, review and homework): 243. Pending list: 111, every one without a task. `course.json` `lessonObjectives` is not read.

## Verification (from `app/`)

- `node tools/validate.mjs`: 0 errors, one pending count warning.
- `node tools/test-validate-perf.mjs`: 33 of 33 (rule fixtures in `tools/fixtures/perf/`: matched without task errors, pending is a warning, Stage 0 excluded, each kind ok, 17 malformed cases error).
- `node tools/test-met-rule.mjs`: 16 of 16 (6 new: task blocks a review pass, self mark alone meets nothing, no-task level unchanged, task row in a review, test-out badge, topic-exam badge).
- `node tools/test-validate-o2.mjs`: 6 passed.
- `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>`, desktop and `--mobile`: all passed.
- Scratch copy of `app/` (not committed): removing `coding-int/L1` from the list errors; a task on it warns "remove from perf-pending"; three tasks, a longform-less `derivation` and `aloud` error. A scratch homework with an `aloud` item and a numeric item with `data` played green (`--set coding-int/homework-1`), and a headless check confirmed the clock (1:30), the follow-ups block, `ready()` true without notes, and the data rows.

## Caveats

- A level is held to the rule only once written (every lesson, review and homework). A half-written level is not yet an error.
- A `derived` met record made before a task is added stays met (nothing unlocked locks again); only levels not yet met are held to it.
- Self kinds live in homework (longform is homework-only, existing rule). `code` and numeric `data` may sit in the review, where a pass also counts toward its auto rows.
- `external` has no producer yet (PLAN 2c item 8).
- Practice sets leave out code and longform items, as before; a performance task is reached from homework or the review.
- Not covered: a DOM playthrough of a real pilot (none exists yet); the playthrough's authored-answer path plays a self kind as "followed the model" (marks 10 of 10).

## Worked examples (copy the shape)

Code (hidden tests: more tests than examples; a stub starter):
```json
{ "id": "h-write-overlap", "performance": "code", "difficulty": 4, "skills": ["intervals"],
  "question": "Write max_overlap(intervals): the most intervals that share one point. Touching ends do not overlap.",
  "widget": { "kind": "code", "language": "python",
    "starter": "def max_overlap(intervals):\n    pass\n",
    "examples": [ { "name": "two", "call": "max_overlap", "args": [[[1, 3], [2, 4]]], "expect": 2 } ],
    "tests": [ { "name": "two", "call": "max_overlap", "args": [[[1, 3], [2, 4]]], "expect": 2 },
               { "name": "none", "call": "max_overlap", "args": [[]], "expect": 0 },
               { "name": "touch", "call": "max_overlap", "args": [[[1, 2], [2, 3]]], "expect": 1 },
               { "name": "nested", "call": "max_overlap", "args": [[[1, 9], [2, 3], [2, 4]]], "expect": 3 } ],
    "solution": "def max_overlap(intervals):\n    ev = sorted([(a, 1) for a, b in intervals] + [(b, -1) for a, b in intervals])\n    cur = best = 0\n    for _, d in ev:\n        cur += d\n        best = max(best, cur)\n    return best\n" },
  "feedback": { "correct": "...", "generic": "Sort the end points and sweep." }, "explain": { "text": "..." } }
```
Derivation (empty box, rubric of 3 or more summing to 10, model shown only after the mark):
```json
{ "id": "h-prove-linearity", "performance": "derivation", "difficulty": 5, "skills": ["expectation"], "kind": "longform",
  "prompt": "Prove that $E[X+Y]=E[X]+E[Y]$ for discrete $X$ and $Y$, with no independence assumed.",
  "model": "Write $E[X+Y]=\\sum_{x,y}(x+y)p(x,y)$ ...",
  "rubric": [ { "points": 3, "text": "Writes the joint sum" }, { "points": 4, "text": "Splits it and marginalises each part" }, { "points": 3, "text": "States that no independence was used" } ] }
```
Aloud (a clock and follow-ups; the box is optional notes):
```json
{ "id": "h-defend-estimate", "performance": "aloud", "difficulty": 4, "skills": ["estimation"], "kind": "longform",
  "prompt": "Defend your estimate of the number of piano tuners in London, aloud.", "seconds": 120,
  "followUps": ["Which assumption moves the answer most?", "How would you check it with one data point?"],
  "model": "A good answer states the chain ...",
  "rubric": [ { "points": 4, "text": "States a chain of factors" }, { "points": 3, "text": "Gives a number for each" }, { "points": 3, "text": "Names the weakest assumption" } ] }
```
Data (numeric is `auto`; a longform with the same `data` is `self`):
```json
{ "id": "h-fit-slope", "performance": "data", "difficulty": 4, "skills": ["regression"],
  "question": "Regress price on area in houses.csv. Give the slope, to two decimal places.",
  "widget": { "kind": "numeric", "answer": 1.52, "tol": { "abs": 0.01 }, "data": { "houses.csv": "content/data/houses.csv" } },
  "feedback": { "correct": "...", "generic": "Fit by least squares and read the area coefficient." }, "explain": { "text": "..." } }
```
(Compute `answer` twice from the real file before authoring; the figures above are placeholders for the shape.)

## For a content author writing a pilot

Add one item to the level's `homework-<n>.json` (or `review-<n>.json` for `code` and numeric `data`) with `performance`; the validator prints the shape error if it is wrong. Tag its `skills` as usual. Pilots: one level in each of `coding-int` (code), `ito` (derivation or aloud), `proof` (derivation) and `research-int` (data or aloud). The level then needs the task passed as well as its review. Do not edit `tools/perf-pending.json`; the main session runs `node tools/perf-pending.mjs --prune`.
