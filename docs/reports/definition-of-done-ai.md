# Definition of done check (docs/PLAN.md section 13), session AI

Read at HEAD 99be2fe9. Last green full acceptance: run 35 at 5b651e21 (59 jobs); later commits touch docs only. Nothing was replayed here except the validator.

| # | Item | Verdict | Evidence |
|---|------|---------|----------|
| 1 | Validator passes | MET | `node tools/validate.mjs` run now: "0 errors, 4607 warnings". `git status` clean afterwards, so `content/manifest.json` did not change. CI `static` job step "Validator (0 errors)". |
| 2 | Playthrough for every authored lesson | MET | CI `play` job: `playthrough.mjs --all --shard i/N --no-routes`, matrix of shards by `desktop` and `mobile` (hash sharding, each item once). `--all` covers lessons, reviews, homework, exams (header of `tools/playthrough.mjs`, lines 9 to 12). `extras` job (desktop and mobile): problems 1 to 2, fluency 1 to 4, drills 1 to 3 plus `--session`, routes-1. Census: lessons 1,236 of 1,236. Guards: `test-playthrough-manifest.mjs`, `-changed.mjs`, `-overflow.mjs`, `-text-overflow.mjs`, `-tall.mjs`. |
| 3 | Every screen with empty and populated state | PARTLY | The playthrough starts every run on a fresh profile (`freshSetup`, playthrough.mjs ~508) and visits Today, Learn, You, exam routes, Review (`#review`, ~2253), Drill (filters, session), Prepare in the routes pass. Later routes run on a populated state (imports, played lessons). `tools/gallery-shots.mjs` and `docs/reports/gallery-themes-ah.md` cover the System gallery in light and dark at two widths. `tools/test-today-tested-out.mjs` covers one Today state. No test asserts "empty then populated" per screen as such. See Gaps 1. |
| 4 | course.json per course; unwritten lessons never throw | MET | Census: 79 course maps, courses with 0 lessons 0, missing 0. Unwritten handling is covered by the routes pass (playthrough.mjs ~2585 to 2605: route limits from `course.json` against `ZQ.prereq.routeLimitsForCourse`, Learn card "Route limited: X unwritten") and `tools/test-hours-split.mjs` (an unwritten lesson counts the short norm). There are 0 unwritten lessons now, so the unwritten path has only that regression coverage, no dedicated fixture. See Gap 2. |
| 5 | Reference lesson identical to prototype | NOT MET (not testable) | `prototype/` no longer exists: `git mv prototype app` (docs/PLAN.md E1, line 293). No test or report compares a lesson with a prototype render. Only indirect evidence: the engine player replaced `prototype/js/lesson.js` and every lesson plays green. Needs a decision, not work. See Gap 3. |
| 6 | Export then import round-trips state | MET | `tools/test-cumulative.mjs` line 185 (`S.export(); S.reset(); S.import(text)`) and `tools/test-problems.mjs` line 120 (same, plus old-save import without the key). playthrough.mjs lines 1805, 1634, 1684, 2308 to 2317 export, mutate and re-import real state (old save without bank or timing loads cleanly). Both tests run in CI `static` or `tests-browser`. Gap: no single test deep-compares full `export()` before and after for all keys. See Gap 4. |
| 7 | Second-reader pass for every topic | MET | Census: "283 of 283 levels read and fixed; every topic exam has a second-read file"; `docs/reviews` has 499 entries. Per-level `review-<topic>.md` files, per-exam `review-exam-*.md`, stage exams `review-exam-stage-1/2/3.md`, grouped files `review-exam-second-item-*.md`. Exam files for 0.5, 1.4, 1.5 are in grouped second-item files or `review-0.5.md`/`review-1.4.md`/`review-1.5.md` (a name grep found no `review-exam-0.5.md`; not individually confirmed, see Gap 5). |
| 8a | C++ via clang wasm with hidden tests | MET | 70 course files carry `language: "cpp"`; `test-bank-code.mjs` and `test-drill-page.mjs` run in CI "Python and C++ tests (Pyodide and YoWASP from jsDelivr)"; `test-grade-code.mjs` and `grade-all.mjs` check hidden tests and the starter failing; reports `docs/reports/cpp-1.md` to `cpp-4*.md`, `audit-cpp-*`. |
| 8b | Git and terminal say on first screen they teach by reading and tracing | NOT MET | DECISIONS.md line 10 records the policy, but the git first lesson `app/content/courses/git/l1-every-version.json` opens "A script that worked on Monday gives nonsense on Thursday..." and the terminal first lesson `l1-home-row.json` opens "Look down at your own keyboard...". `course.json` descriptions ("Keep every version of your work, and share it on GitHub.") have no such line. No mention anywhere in `git/` or `terminal/` content. |

## Gaps

1. Empty versus populated state per screen (small to medium). Add one routes check, or a small `tools/test-screens-states.mjs`, that visits each of #today, #learn, #review, #drill, #prepare, #you, #system on a fresh profile, then on an imported populated profile, and asserts no console error and a non-empty main region.
2. Unwritten lesson fixture (small). Add a `tools/fixtures/mini-app` course with one unwritten lesson id and assert Learn, Course and the lesson route show it and do not throw.
3. Reference lesson versus prototype (small decision). The prototype is gone. Either amend docs/PLAN.md item 5 to "the reference lesson plays green under the engine player" or retrieve `prototype/` from git history and compare screenshots (large, low value).
4. Export/import completeness (small). Add one assertion that `JSON.stringify(S.export())` equals the re-export after `reset` and `import` for a fully populated profile.
5. Exam second-read mapping (small). Confirm with a script that each of the 29 topic exams (notably 0.5, 1.4, 1.5, 1.7, 1.8) is named in a review file; census says yes, filenames are grouped.
6. Git and terminal "reading and tracing" line (small). Add one sentence to the first screen of `git/l1-every-version` and `terminal/l1-home-row` (or the git and terminal `course.json` description, if the Learn card shows it), for example "Here you read and trace commands; the browser has no shell." Needs a content agent, since content agents own lesson files; then validate and replay those two files.

## After the session AI fixes

| Item | Verdict now | Evidence |
|---|---|---|
| 1 | MET | `validate.mjs` 0 errors, 4,606 warnings at 5bb35c99 |
| 2 | MET | CI `play` and `extras` shards, desktop and `--mobile` (full run at 5bb35c99) |
| 3 | MET | `app/tools/test-screen-states.mjs`: 27 routes on an empty, a truly empty and a played state, 1280 and 440 px (CI `tests-browser` ui leg; `docs/reports/screen-states-ai.md`) |
| 4 | MET | same test: an unwritten lesson on `tools/fixtures/mini-app` shows "Not yet written" and its route shows a card |
| 5 | PARTLY | `docs/reports/prototype-compare-ai.md`: same screens, answers and grading; rows 2, 4, 6 and 12 now match (engine 1211 to 1213, content fix); the derive screen is an ordering task where the prototype picked a line, the simulate canvas looks different, options shuffle (backlog 591), wording was edited later. Not literally identical |
| 6 | MET | same test: export, import into a fresh context, deep-equal, also after a reload |
| 7 | MET | 283 of 283 levels read and fixed; every topic and stage exam is named in at least one `docs/reviews` file (checked by grep this session) |
| 8 | MET | C++ hidden tests via YoWASP clang; the first screens of `git/l1-every-version` and `terminal/l1-home-row` now say the course teaches by reading and tracing |

Item 5 after the user's decision (17 Nov): MET. The simulate screen now uses the `dice-sim` canvas (engine 1217) and matches the prototype's dice, Rolled / Kept / Total 10 counters, share bar and running trace against 1/11; the derive screen stays an ordering task by the user's choice. Option shuffling (backlog 591) and later wording edits stand.
