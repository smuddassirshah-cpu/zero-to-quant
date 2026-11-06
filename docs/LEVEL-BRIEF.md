# Brief for a content agent: author one level of one course

You are writing the lessons, the level review and the homework for one level of one course in the Zero to Quant app. The orchestrator names the course and level. Read, in this order, before writing anything:

1. `docs/AUTHORING.md` (the schema, the voice rules and the validation rules; binding).
2. `docs/curriculum.md`: the entry for the course's topic (its `Cover` and `Exit` lines are what the level must serve).
3. `app/content/courses/<course>/course.json`: the level's lesson ids, names, objectives and the course skills. Use these ids and names exactly. Every lesson's `skills` must be course skill ids.
4. `app/content/courses/conditional/l3-shrinking.json` and `l1-what-changes.json`: the reference lessons. Match their depth, structure and tone.
5. `app/js/engine/canvas/README.md` and `README-B.md`: the parameters of every canvas kind. Use only what they document.
6. `docs/design-research.md` sections 8.3, 8.4, 9.1 to 9.4 (sequencing, difficulty ramp, how a concept is introduced, voice, explanation conventions).

## What to write

- One file per lesson: `app/content/courses/<course>/<lesson-id>.json`, 8 to 12 screens, `summary`, 3 to 5 quiz items, following the lesson shape (hook, explore, name, ladder of 2 to 4, trap, generalise and derive, transfer, summary). Every lesson needs a real interactive canvas early (tap, drag, slider, manipulate, balance, place, order, table, code, as fits the subject) and a quant-context transfer screen.
- `app/content/courses/<course>/review-<n>.json`: 6 to 10 items interleaving every lesson of the level, difficulty 2 to 4.
- `app/content/courses/<course>/homework-<n>.json`: 6 to 12 items, difficulty 3 to 5 with at least one 5, at least one `longform` item with a 10-point rubric and a full model answer, and at least one `code` item for programming courses or one `order` or `expression` derivation item for maths courses.

## Teaching quality bar

- Puzzle first. The learner acts on the diagram before any rule is named. The rule, when it comes, describes what they just did.
- Every distractor is a real misconception a learner holds, and its `why` names the learner's action ("You added the two chances, but...").
- Every `trap` screen targets the misconception most learners actually have for this topic. Every lesson has one edge case.
- Explanations are at most three sentences and come with a diagram state patch where a canvas exists.
- Derivations carry a justification per line. No "it can be shown".
- Numbers are correct. Compute every answer yourself and check it twice; for simulations state the exact value the empirical frequency converges to.
- Every summary, `explain` and `why` sentence that states a general rule carries its hypotheses (convexity, a constraint qualification, a sample size or independence condition). Write no unqualified "always" or "any". Check this before you hand the level on.
- Transfer screens use real quant contexts (a bet, a price path, a portfolio, an order book, a dataset, a backtest, a signal, a P&L), with realistic numbers.
- British English, no exclamation marks, no emoji, sentences under 20 words, second person, "we" when reasoning together.
- Programming lessons use the `code` widget with hidden tests that run in Pyodide (pure Python, standard library only, no numpy unless the course is numpy-pandas or later, where `numpy` and `pandas` are available in Pyodide but slow to load: prefer pure Python for tests).
- C++ lessons use the same `code` widget with `"language": "cpp"`: the code is compiled by clang in the browser and tested like Python (function calls with JSON `args` and `expect`, or programs on `stdin` and `stdout`). Read the C++ addendum at the end of `AUTHORING.md` section 3 (types, script mode, prelude and postlude, limits: no `try`/`catch`) before writing one.

## Mechanics

- Lesson, review and homework files are JSON. Escape backslashes in KaTeX (`"\\dfrac"`). Keep KaTeX inline as `$...$` and display as `$$...$$`.
- Use the grid's named id sets (`row5`, `col3`, `cross5`, `all`) rather than listing every cell where possible.
- Do not edit any file outside `app/content/courses/<course>/` for your level, and never edit `course.json`, other levels' files, engine files or docs. If the course map needs a change (a lesson that cannot be taught as named, a missing skill), write your lessons to the map as it is and state the proposed change in your report.
- Run `node app/tools/validate.mjs` from `/home/user/zero-to-quant/app` until it reports 0 errors for your files (warnings about other courses' unwritten lessons are fine). It writes `content/manifest.json`; that is expected.
- Number recompute: commit `docs/reports/<course>-L<n>-numbers.py` and make it exit 0. Compute every value twice, then use `app/tools/numbers_lib.py` (`lv = Level("<course>", <n>)`, `lv.expect(file, path, value)`, `lv.check_wrongs()`, `lv.report()`) to check that the value appears in the lesson JSON at the path where it is stated. Check every stated number in prose, `wrong[]` values, `why` and `explain`, not only the answer. `lv.check_wrongs()` asserts every numeric `wrong[].value` lies outside its answer's tolerance and lists any `byKey` text that states a different number (check those by hand). The validator warns when a written level's script never uses `Level(` and `expect(`, and when a wrong value cannot fire (item 581).
- Review rule: every level review carries `pass` (the share that counts as passed, 0.8 by default); the validator errors on a mapped review without it.
- Play every lesson: `node app/tools/playthrough.mjs --lesson <course>/<lesson>` (if the tool exists; it serves the app itself). A level is accepted with and without `--mobile` (440 x 956, the user's phone) and with `--tablet` (1032 x 1376 and 1376 x 1032, the user's iPad); `--narrow` (390 x 844) is the stricter optional width. Look at the `-440`, `-1032` and `-1376` screenshots when you pass `--shots`. These passes resize the window and do not emulate touch. If it does not exist yet, serve `app/` with `python3 -m http.server 8080` (reuse a running server on 8080 if there is one) and drive `http://localhost:8080/#lesson/<course>/<lesson>` with Playwright (chromium at `/opt/pw-browsers/chromium`, `executablePath`) using the hook: loop `ZQ.test.answerCorrect(); await ZQ.test.check(); await ZQ.test.continue()` until `ZQ.test.current().kind === 'done'`, asserting every check is ok and there are no console errors other than blocked requests to cdn.jsdelivr.net (that host is blocked in this sandbox only). First complete the app's setup once (route `#setup`) in the same browser context so routes do not redirect. Take one screenshot per screen into your own subfolder of the scratchpad named `<course>-<level>` (the scratchpad is shared with other agents; keep every helper script and generator in that subfolder too and never touch another folder) and look at the PNGs: fix overlapping labels, empty canvases, a wrong state after `enter`, options that do not fit, and anything that would confuse a learner.
- Programming courses that import `numpy` or `pandas`: the worker loads packages from the learner's imports on first run (slow the first time). In this sandbox the browser playthrough needs a local CDN that holds the wheels: use `--local-cdn <pkgs>`, where `<pkgs>` is the folder named in your brief or the orchestrator prompt; if it is missing, build it with `bash app/tools/fetch-local-cdn.sh <pkgs>` (about 40 s and 870 MB: full Pyodide 0.27.7 with every wheel, MathLive, Compute Engine, YoWASP clang). Compare arrays with `np.round(f(...), 6).tolist()` and `compare: "equal"`; never show a dtype name in an answer (wasm integers are int32).
- In your own worktree, commit once per level with the level in the message; never push or open a pull request. Outside a worktree, do not commit; the orchestrator commits.

## Report

Write the full report to `docs/reports/<course>-<level>.md` (for example `docs/reports/arma-1.md`): files written with screen and item counts; the validator result; the playthrough result per lesson, review and homework; every number you state with its source; any proposed change to `course.json`; the dataset or seed conventions you used. Put every engine or canvas limitation that blocked or bent a teaching idea in `docs/BACKLOG-INBOX.md` under a heading `Raised later (<course> level <n>):` as bullet points (name the canvas or widget, what you needed, and the workaround you used); do not number them. Then hand back to the orchestrator no more than six lines: the report path, "validator 0 errors" or the error list, "playthrough all passed" or the failures, the count of backlog bullets added, and any proposed `course.json` change in one line. Nothing else; the orchestrator reads the file only when something failed.
