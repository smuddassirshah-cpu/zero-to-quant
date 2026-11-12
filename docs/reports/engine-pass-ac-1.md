# Engine pass AC part 1: green-hash cache and `playthrough.mjs --changed`

## Built

- `app/tools/green-cache.mjs` (new): hashing, cache file, lookup, locked writes.
- `app/tools/playthrough.mjs`: `--changed`, `--no-cache`, `--cache <file>`; every passing item is recorded; usage header documented.
- `app/tools/test-playthrough-changed.mjs` (new): 26 checks, about 66 s (35 s of it two real browser runs).
- `.gitignore`: `app/tools/.green-cache.json`, its `.lock/` and `.tmp` files. `docs/AUTHORING.md`: one paragraph under "Long runs".

Cache file: `{ version: 1, entries: { "<kind>|<id>|<mode>": "<sha1>" } }`. Kinds: lesson, set, fluency, problems, exam, bank, drill, drill-planted, session, routes.

## Decisions

- **Mode** is the viewports actually played: `desktop`, `mobile`, `narrow`, `tablet`, joined with `+`. A green for a superset counts (`desktop+mobile` covers `desktop`, not the reverse). Drills run only at the extra widths when any is given, so their mode has no `desktop`; planted checks are always `desktop`.
- **Shard first, then filter.** Shard membership then depends only on the item list, so shards partition identically on every machine whatever each cache holds. `K of N` counts N after sharding. Banks, drills, the session and routes are not sharded today (unchanged); `--changed --list` lists them too, plain `--list` is unchanged. In list mode the `changed:` line goes to stderr so stdout stays ids only.
- **Concurrent writes:** one shared file; mkdir lock, re-read, merge, write temp, atomic rename; stale locks (over 15 s) are broken. Tested with four processes writing 150 entries each: 600 of 600 kept, no lock or temp left.
- **Snapshot:** every hash is taken before the first item plays and memoised, so an edit made mid-run is never recorded as green for the old content.
- **Recording:** an item is recorded when no failure and no console error arose during it (guarded items), and again a final sweep drops any item whose id appears as a whole token in a failure line or console-error place (late errors). Batches are written every 12 items and at the end; a killed run loses at most the last batch. If Python or the C++ compiler fails to load (`waitPython`, `drillReady`), recording stops for the rest of the run (the item itself already fails). `--why`, `--headed`, `--shots` still record.
- **`content/manifest.json`** holds the file list, samples, self exams, exam minutes, sessions, lesson and set minutes, perf, drill, fluency and problems metadata: all derived by the validator from content files plus the validator's own rules. It is never hashed as bytes. Each item hashes the slices its page reads (its own minutes, session, fluency, problems, drill and exam entries, whether its file is listed or a sample, the perf entries of its course). This keeps lesson edits from invalidating unrelated items through `lessonMinutes`, and still catches a validator rule change that alters an item's own data. The validator was run on the worktree: manifest unchanged and no hash moved. The routes item hashes a normalised copy (note dropped, keys sorted).
- Engine hash: `js/**`, `css/**`, `index.html`, `vendor/**`, `playthrough.mjs`, `green-cache.mjs`, plus the pinned CDN strings read out of those files (mathlive, compute-engine, yowasp clang, pyodide).

## Dependency set per kind (read from `content.js`, `player.js`, `exam.js`, `mock.js`, `select.js`)

Every page at start loads `curriculum.json`, `manifest.json`, `drills/index.json`, `prep.json`, `readiness.json`, `capstones.json`, `warmup.json` (arith) and every `course.json`.

| Kind | Hash covers |
|---|---|
| lesson | the lesson file; `content/data/*` files it names; its `course.json` in full; the other courses' `course.json` without `lessons`, `lessonNames`, `lessonObjectives` (skills, requires, strand); `curriculum.json`; `warmup.json`; the file names in its course folder; manifest perf of its course and its own minutes, session, fluency entries |
| set (review, homework) | same, with the set file and its `setMinutes` |
| fluency | the set file; the lesson file it names (the end card is checked); course common set; fixtures (`fixture/<id>`) use the fixture file plus the course and lesson it names |
| problems | the set file plus the course common set and its `problems` entry; fixtures as above |
| exam | the exam file; every bank or drill file its `draw.from` entries resolve to (the `matchFile` rule: name, `*`, or prefix before a dash); data files of all of those; `drills/index.json` only when it draws drills; `curriculum.json`, `warmup.json`, all course graphs (skill names, topics); manifest exam minutes, self-exam and sample flags |
| bank | the bank file; its data files; the names (not contents) of the other bank files (the deck is built over all of them); the course graph (for `requires`) |
| drill, drill-planted | the drill file; data files; its row in `drills/index.json`; its manifest entry; the course graph |
| session | the session file; the drill files it names; their data files; `drills/index.json` |
| routes | **fallback, as allowed**: every file under `content/` (manifest as a normalised copy) plus `tools/fixtures/**`. The route checks read reviews, lessons, exams, banks, drills, capstones, prep and samples (gating, weekly review, provenance, bank deck), so no smaller set is honest. Any content edit therefore replays the routes. |

Judgement calls to know about: other courses' lesson lists are left out of a course's hash (a lesson added to course B does not replay course A, though `ZQ.prereq.unlock` and `exists` could in principle read them; the playthrough force-unlocks prerequisites, so no run depends on them); a sibling review's edit does not replay the course's lessons (essentials are read only through prerequisite gating, which is force-unlocked).

## Measured

- `--all --changed --list`, empty cache, 2052 items: 1.4 s (bounded by 83 MB of content read once). With `--shard`, `--drills --bank all`: about the same.
- `--changed` with 9 seeded items selected: 0.23 s, "Nothing changed since the last green run."
- Real seeding runs: 7 lessons, 3 sets, a fluency set, a problem set, 2 exams, a bank file, a drill (desktop; two lessons, a set and an exam also at `--mobile`). `--changed` then showed 0 of 9 and 0 of 4; `--tablet` showed 4 of 4; plain desktop showed 0 of 4 after a `--mobile` run.
- Validator: 0 errors, manifest untouched. `test-playthrough-tall.mjs` and `test-playthrough-overflow.mjs` pass (27 s and 15 s). They play a modified copy, so they also write entries (with the copy's hashes) into the default cache, which are harmless.

## Not done or not verified

- The routes recording was not run to the end: a `--routes-only` run takes over 110 s here and was interrupted. The hash is unit-tested (changes with a lesson or `prep.json`, not with a manifest note) and the recording code is a three-line check on failures and console errors around the route block.
- The "Python could not load, no green" rule was run once by hand (`--drill daily-returns` against an empty local CDN: fails after 90 s, no cache file written); it is not in the test because of the 90 s wait.
- Bank, drill and session recording rely on the final failure sweep (their failure lines carry the id) rather than a per-item snapshot.
- Plain `--list` still omits banks, drills and routes (unchanged behaviour); only `--changed --list` shows them.
- `playthrough.mjs` now loads Playwright after `--list`, so `--list` works without it installed.
