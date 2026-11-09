# Brief: performance-task retrofit (PLAN 2a Phase 3, session X)

Binding for every retrofit agent. Read `docs/AUTHORING.md` section 5 "Performance task" in full, then sections 6, 7 and 11, then `docs/reports/ito-2-perf.md` and `docs/reviews/review-perf-pilots.md` (the quality bar and the faults the pilots had). Your courses and levels are named in your prompt; they are the `course/L<n>` keys in `app/tools/perf-pending.json`.

## What to write

- One item per level, nothing else. Not a level rewrite. Append the item to `homework-<n>.json` (or `review-<n>.json` for an auto kind where the homework is at its 12-item cap). If the homework is at the cap, convert the existing item closest to the matched objective instead of adding one, and say so in the report.
- Pick the objective the verb rule matches (the `objectives` in the lesson JSON, not `course.json`). Name it in the report. One task per level, so where several objectives match, choose the one whose product best proves the level: a code or derivation product over an explanation.
- Kind by verb (AUTHORING section 5): write, code, build, implement give `code`; derive, prove give `derivation`; explain, defend, justify give `aloud` (or `derivation` where the answer is written maths); design gives `code` where it runs, else `aloud`; a task read from a data file is `data`.
- The task asks for the product from a blank start and grades the product. It is not a quiz item. No hints, no steps, no scaffold.
- Fresh: the task repeats no lesson screen, review item or homework item of the course. It may ask for the product a lesson works through (that is the objective), but on new inputs or a new setting and with at least one part the lesson does not lay out; never the lesson's code or derivation line for line. The report names every lesson screen that lays out the same product and lists the new parts. Grep the course folder for the task's key nouns, numbers and function names and read every hit before you write it.
- A `derivation` or `aloud` model answer justifies every line (the pilots were sent back for asserted steps). The rubric has 3 to 5 rows summing to 10; mark `"required": true` on the row that carries the core result, and on one row for each further distinct part the matched objective or the task's own question names, so no 7 of 10 pass skips a named part (never every row). Word each required row by the result it needs, not by one route to it: a correct proof by any method the level teaches must be able to tick it (third sighting: contests L3, integrals, markov L5). List every passing tick set in your numbers script and check none skips a named part (`node tools/rubric-passes.mjs` once it exists, ENGINE-BACKLOG 698). State hypotheses in plain words.
- A `code` task: a stub `starter` that the playthrough proves fails; a `solution`; `tests` of 3 or more with strictly more tests than `examples`; the hidden tests catch at least three plausible wrong solutions, which you plant and run. Python runs in Pyodide 0.27.7 (NumPy, pandas 2.2.3, SciPy, scikit-learn 1.6.1, statsmodels); keep tests fast, prefer the standard library where the course allows. C++ runs in YoWASP clang 21 at `-O1` with no exceptions: read the C++ addendum in AUTHORING section 3.
- An `aloud` task carries `seconds` (15 to 1800) and 1 to 5 `followUps`; optional `think` and `lockAtZero`.
- Voice: British English, no exclamation marks, no em-dashes or en-dashes, £ for money, sentences aim under 20 words (gate 35), explanations at most three sentences, no lesson cited by number.

## Gates before you hand a level back (all four, or it goes back to you)

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors. The warning "<course>/L<n>: has a performance task, remove from perf-pending" is expected. Never edit `tools/perf-pending.json`, `course.json`, other levels, other courses or engine files. Restore `app/content/manifest.json` (`git checkout app/content/manifest.json`) before you commit.
2. `VOICE_BASE=app/content/courses/<course> python3 docs/reviews/voice-scan.py 35`: 0 and 0 for the whole course folder.
3. `docs/reports/<course>-<n>-perf-numbers.py` committed and exiting 0: every number in the item, model and rubric computed twice by independent routes; for a code task it runs the solution and the starter and the planted bugs against every test (for pandas or matplotlib use the venv named in your prompt).
4. Run the validator first and play through with its regenerated `content/manifest.json` in place (restore the manifest only after the playthrough, just before you commit): with the old manifest the new task shows as "practice only". Then `node tools/playthrough.mjs --set <course>/homework-<n> --local-cdn <pkgs>` (and `review-<n>` if you touched it), green with and without `--mobile`. Look at the shots for a display equation that scrolls sideways at 440 px and split it with `aligned`.

## Report and hand-back

- Report under 200 words to `docs/reports/<course>-<n>-perf.md`: file, item id and index, kind, matched objective, rubric or test design, the four gate results with the exact commands, the freshness grep terms.
- Engine limitations as bullets in `docs/BACKLOG-INBOX.md` under `Raised later (<course> level <n> perf):`.
- Commit once per level in your worktree: `perf task <course> L<n>: <item id>`. Never push, never touch other branches, never open a pull request.
- Hand back at most six lines: levels done, item ids and kinds, validator, playthrough, bullet count, anything you could not do.
