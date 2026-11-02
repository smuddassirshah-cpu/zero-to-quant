# Engine pass: prep tags and the Prepare for page (ENGINE-BACKLOG 455)

Brief: `docs/briefs/prep-tags.md`, sections "Data" and "Engine". Schema documented in `docs/AUTHORING.md` section 10. No content file was edited except creating `app/content/prep.json` (two engine sample paths) and the validator's regeneration of `app/content/manifest.json`, which now lists `prep.json`.

## What was built

- **Loader** (`app/js/content.js`): `ZQ.content.prep()` and helpers `prepPaths`, `prepPath`, `prepRefLessons`, `prepSteps`, `prepFor(course, lesson)`, `prepForCourse(course)`, `prepDetail(paths)`, `prepChip(paths, cls)`, `prepMonth`, `prepStageLabel`. A course or level ref expands to the lessons listed in `course.json`, written or not. The lesson to paths index is built once, after the courses load. `prep.json` is requested only when the manifest lists it, so a missing file causes no 404.
- **Validator** (`app/tools/validate.mjs`): new block after the exams. Errors: unknown fields (top level, path, step); `asOf` missing or malformed; bad id, duplicate id, bad `kind`; stage path without a valid `stage` and `track`, or two paths for one stage and track pair; `stage`, `source`, `reported` on the wrong kind; a general path with a `track`; firm path without `asOf`, `source` or `reported: true`; a `source` or step `ref` that is not a course, `<course>/level-<n>` or `<course>/<lesson>` in a `course.json`; a mock id not of the form `mock-kebab` (an unwritten mock is allowed) or repeated; `priority` not `must` or `should`; `why` of 20 words or more, or breaking the copy rules (exclamation, emoji, American spelling, em-dash); a repeated ref in a path. Warnings: a firm `asOf` over 12 months old, a path with no steps, a lesson covered by two steps of one path. `--prep <file>` checks a scratch copy and leaves the manifest alone.
- **Chips**: one `.prep-chip` ("Interview prep", neutral, tooltip holds the detail) on a Learn course card (when any lesson of the course is on a path) and on a course map lesson node. The node detail (desktop card and phone sheet) adds "Interview prep: General, OA, superday. Optiver, SIG (reported, October 2026). See the path". Reviews and homework get no chip. The node's accessible name says "Interview prep".
- **Prepare for page** (`app/js/screens/prepare.js`, `app/css/screens/prepare.css`, route `#prepare` and `#prepare/<id>`): pick General, a stage with a role, or a firm; the URL follows the choice. Each step shows its number (in its course's track colour), title, level, Must or Should, Done, In progress, Not started or Not yet written, lesson counts, and the `why` line; it links to the course map. Firm paths say "Reported formats, as of <month year>" and name their source lesson. Mocks link to `#exam/<id>` or read "Not yet written". The page redraws when progress changes.
- **Entry points**: a "Prepare for an assessment or a firm" link under the Learn heading, and the same link inside Review's "Mock assessments" card (the card now shows whenever paths exist). Path names are in the Today search (kind "Prepare"). "Quant path only" is untouched and nothing is gated.
- **Playthrough** (`app/tools/playthrough.mjs`): `--routes-only` now opens `#prepare` and one deep link per path kind in `prep.json`, checks the number of steps drawn against the file, that no step links to an unknown course, and that the page is not wider than the window (also at 390 px with `--mobile`).

## Notes and decisions

- The brief says "lesson card (`learn.js` card)". `card()` draws a course card, so the Learn chip marks a course with any lesson on a path. Lesson-level chips are on the course map.
- The lesson start screen was not given a separate chip; the course map node detail is the lesson's detail.
- `prepDetail` lists "General" first, then stages in OA, interview, superday order, then firms grouped by report month.
- The sample `prep.json`: `general` (mental, puzzles level 1, conditional level 1) and `firm-optiver` (mental-pressure level 1, mm-games level 1; mocks `mock-sample` and the unwritten `mock-oa-arith`, to exercise both states). Both descriptions say they are engine samples. The content agent replaces the file.
- Stage paths are untested against real data (the sample has none); they were exercised through the scratch broken copy and the picker code only. Check them with the first real `oa-*` path.

## Verification

- `node tools/validate.mjs`: 0 errors (386 warnings, all existing "not yet written" notes).
- A broken scratch copy (`prep-broken.json`: missing top `asOf`, unknown fields, bad and unknown refs, bad priority, exclamation, em-dash and a 27-word `why`, a firm path without `asOf`, `source` or `reported`, a bad mock id, a duplicate mock, a stage path without stage or track, a 34-month-old firm date) gave 18 errors and 2 warnings, exit 1.
- Screenshots at 390 px (and 1280 px for the map card and search), checked by eye: Learn course card chip, Learn header link, course map nodes, lesson detail sheet and desktop card, Review mocks card, Prepare for (general, firm, mocks). One fault found and fixed: the chip on the current map node sat a halo's width left of its title.
- Playthrough results: see the final lines below.

