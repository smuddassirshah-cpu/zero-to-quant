# Engine pass C, agent D: drill library (item 472, E8 with C-drill-patterns)

## Status line (backlog style)

472. Done (E8, with C-drill-patterns): drill library. A drill file may carry `language: "cpp"` (graded by the C++ code widget and `cpp-grade.js`, so the cases are `call`/`args`/`types`/`expect`/`compare`; nested `std::vector<std::vector<int>>`, `std::vector<long long>` and `long long` documented in AUTHORING section 3 and exercised by two sample drills), `pattern` (one slug of a fixed vocabulary, `PATTERNS` in `js/screens/drill-lib.js`, read by the validator), `pace` (seconds), `tags` and `sample: true`. Every drill page shows a stopwatch (pause, restart, pace; amber past the pace) and records its reading with each submit (`ZQ.state.drills.time`, `runs` and `best` on the drill record). `#drill` has pattern, difficulty-range and language filters (kept in `ZQ.store 'drill.filters'`). `#drill/session` (and `#drill/session/<id>` for a set session file `drills/sessions/<id>.json`) sits two drills against one 60-minute countdown with a tab per drill, resume after leaving, auto-close at zero, and a result screen (time on each drill, hidden tests passed, solved) kept with `ZQ.state.drills.session` (`doc.drillSessions`, last 50). A lesson reads the latest session as `{{carry.session.minutes1|minutes2|passed1|total1|passed2|total2|solved|minutes}}`. Files: new `app/js/screens/drill-lib.js`, `app/css/screens/drill-lib.css`; edited `app/js/screens/drill.js` (list filters, stopwatch, options, routing), `app/js/content.js` (`drills()` merges manifest metadata; `drillSessionIds`, `drillSession`), `app/js/state.js` (`drills.time`, `drills.session`, `drills.sessions`, `drillSessions`), `app/js/engine/player.js` (`carry.session`), `app/js/core.js` (pause icon), `app/index.html`, `app/tools/validate.mjs`, `app/tools/playthrough.mjs`, `docs/AUTHORING.md` (sections 3, 5, 7). Validator rules: `language` not python or cpp; `pattern` outside the vocabulary; `sample` not boolean; ids `index`, `session`, `sessions`; a C++ drill checked as a C++ code widget (3 to 15 tests, case shapes, `types`, `compare`, `tol`, flags, budget), empty starter, no `solution`, no example; warning for `fn` on a C++ drill; `CPP_TYPES` now include the nested and `long long` vectors; session files (id is the file name, `drills` exactly two different existing ids, `minutes` 10 to 180, `sample` boolean, unknown field a warning); `manifest.json` lists `drills/sessions/*.json` and gains a `drills` map (language, pattern, pace, tags, sample per file); a sample drill needs no `index.json` row; `{{carry.session...}}` is always allowed in a lesson. Playthrough: `--drill <id>` (repeatable), `--drills`, `--session`; `--routes-only` now also checks the list filters and the session setup.

## What was built

- **C++ drills** (`mountCpp` in `drill-lib.js`): own page (brief, examples, constraints, hint after first run, how it is checked, the C++ widget with Run examples and its result list, Submit, summary, model solution). Submit calls `widget.grade()`; a compile error or missing compiler is not an attempt. Draft, verified code, failed count and reveal use the same state as Python drills.
- **Stopwatch**: `Stopwatch` (Date.now based, so tests skew it) and `stopwatchPill`; on Python and C++ pages; replaced by the session clock inside a session.
- **Filters**: pattern (only slugs in use), language, difficulty from and to (kept ordered); shared by `#drill` and the session setup.
- **Sessions**: setup (filters, two picks, Pick again, set sessions list, resume or abandon a running one), running view (bar with tabs, countdown, Finish, amber under 5 minutes, drill mounted below), result view. Minutes per drill are wall-clock time the drill was the current tab. Inside a session Submit always grades even a drill verified before. Test hook `window.ZQSession` (`state`, `switchTo`, `finish`, `setRemaining`, `tick`, `result`).
- **Lesson carry**: `carryReset` in `player.js` seeds `Z.carry.session` from the latest session.

## Tests (from `app/`, `--local-cdn` the scratchpad `pkgs`)

| Command | Result |
| --- | --- |
| `node tools/validate.mjs` | 0 errors, 392 warnings (all pre-existing: unwritten levels) |
| `node tools/playthrough.mjs --drills` | all passed: 7 Python drills and the 2 C++ samples (starter fails, model solution passes every test, stopwatch read and recorded after a 130 s clock move), then the sample session |
| `node tools/playthrough.mjs --drills --mobile` | all passed (390 px, no sideways scroll on drill, session setup, running or result pages) |
| `node tools/playthrough.mjs --session` | all passed (also with `--shots`) |
| `node tools/playthrough.mjs --routes-only` and `--routes-only --mobile` | all passed, including `drill filters and session setup` |
| `node tools/playthrough.mjs --lesson conditional/l3-shrinking` | ok (carry reset unchanged for a lesson) |

Validator scratch cases (files created and deleted): bad pattern, bad language, non-boolean `sample`, two tests only, `types` of the wrong length, missing solution, id `session`, id and file name mismatch, a session with the same drill twice and `minutes: 5`, a session naming a missing drill with an unknown field. Each gave the expected error or warning; no scratch file remains. The full `--all` run was not repeated here (it takes the lessons of every course; this change touches only drills, `carryReset` and the state document).

## Deviations and decisions

1. **Pattern vocabulary is wider than the inbox's twelve.** The systems brief uses `cache` and `rate-limiter`, and drill packs 2 to 8 of the interview plan need slugs for two pointers, binary search, trees, graphs, DP, backtracking and greedy. Added: `cache`, `rate-limiter`, `two-pointers`, `binary-search`, `trees`, `graphs`, `dp`, `backtracking`, `greedy`. The main session should confirm or trim `PATTERNS` (one array).
2. **No `<pack>/<id>`.** Drill files are flat; a pack is an id prefix. The flags are `--drill <id>`, `--drills`, `--session`.
3. **Filter data comes from the manifest**, not `index.json`: authors append the four fields only, so the validator copies `language`, `pattern`, `pace` and `tags` into `manifest.json` (`drills` key) and `content.js` merges them into `drills()`.
4. **Result screen "tests passed" is the best submit** of each drill (not the last). Minutes are time as the current tab, up to the budget.
5. `sample: true` was added with no validator conflict (unknown fields were ignored); the check is a boolean type test only, so agent A's rule may replace it at merge. Sample drills are never listed and never picked for a session (`pickTwo` skips them).
6. A C++ drill's example input is shown as `function([json args])` and the output as JSON, not as C++ source.

## Follow-ups

- Pre-existing Python drills have no `pattern`; the content agents add it as they touch them (not an error).
- Session minutes after the clock is moved are not recorded as build hours separately; each drill logs its own page time as before.
- C-draw-code (agent A) can read `pattern`, `language`, `difficulty` and `pace` from `ZQ.content.drills()` rows.
- Mobile: the session Finish button sits in the top bar at 390 px; the drill's own title row below it repeats the drill name (acceptable, could be hidden in a session).
- The sample files `drills/sample-cpp-row-sums.json`, `sample-cpp-merge-intervals.json` and `sessions/sample-session.json` are for authors and tests only.
