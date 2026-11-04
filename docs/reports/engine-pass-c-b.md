# Engine pass C, agent B: data files (469) and allocation counting (470)

## Status lines

469. Done (E14, C-data-cap): `data: { "name.csv": "content/data/<path>" }` on a Python `code` widget (lesson, quiz, review, homework, exam and mock items) and on a drill file. Each file is fetched once (`ZQ.content.dataFiles`, `app/js/content.js`), cached, and written into the working directory before every run, through the existing `files` mechanism in `app/js/engine/widgets/code.js` (before `prelude`, so the learner's code, `prelude`, `postlude`, `setup` and hidden `tests` all open it by bare name). A drill gets it as `spec.prelude` in `app/js/screens/drill.js` (hidden tests are expressions that read the file inside `call`). A closed "Data files in the working directory" panel under the editor shows each file's size and first six lines; `dataPeek: false` hides it (CSS in `app/css/widgets.css`). Cap: 256 KB a file, text (UTF-8) only. Validator rules (`app/tools/validate.mjs`, function `dataFiles`): `data` not a non-empty object; name not a bare file name; name also a key of `files`; path not under `content/data/`, containing `..`, or not an existing file; file over 262,144 bytes; file not UTF-8; `data` on a C++ widget; `dataPeek` not boolean. Checked on every widget the validator walks and on drill files.
470. Done (C-alloc-check): `allocCheck: true` on a C++ `code` widget gives `alloc_count()` and `reset_alloc_count()` (`app/js/engine/widgets/cpp-grade.js`: `ALLOC_CNT`, `ALLOC_OPS`, `LEAK_COUNTED`). One volatile `int` counter bumped by the global `operator new`, `operator new[]` and their `std::nothrow` forms (which call `malloc`); the counting rule is the brief's (whole program since the last reset or start-up, harness and setup included, `malloc` not counted). With `leakCheck` the leak wrapper's own operators are patched to bump the same counter, so the two coexist (two sets of replacement operators would not link). The unit is compiled with `-fno-builtin` when `allocCheck` is on (added to the worker's flag allow-list in `app/js/screens/cpp-worker.js`; authors cannot write it). Validator: `allocCheck` not boolean or on a Python widget; a hidden `prelude`, `postlude` or `files` source with `operator new` or defining `alloc_count`/`reset_alloc_count`; warning when no test reads `alloc_count()`.
Isclose bullet (DataFrame compare, `nan: "equal"`): not done. The research-int brief (line 157, and H4.2) already works round it (scalar or `.round(6).to_numpy().tolist()`, and `bool(np.isnan(...))` expecting `True`), so it was redesigned away. Left as a follow-up if a later brief wants frames or NaN compared directly.

## Files

- Engine: `app/js/content.js` (`dataFiles`), `app/js/engine/widgets/code.js`, `app/js/engine/widgets/cpp-grade.js`, `app/js/screens/cpp-worker.js`, `app/js/screens/drill.js`, `app/css/widgets.css`.
- Validator: `app/tools/validate.mjs` (`dataFiles`, `DATA_CAP`, `allocCheck` rules; a sample drill is not warned about for missing from `drills/index.json`). No rule needed for `"sample": true` (unknown top-level keys are accepted).
- Docs: `docs/AUTHORING.md` (code widget "Data files", C++ "Counting allocations", section 5 drill bullet, section 7 "Data and allocation rules").
- Samples (all `"sample": true`, used by no course): `app/content/data/sample-prices.csv` (10 rows), `app/content/drills/sample-data-drill.json`, `app/content/exams/mock-sample-data.json` (a Python `data` item, a C++ `allocCheck` pool item, a C++ `allocCheck` + `leakCheck` buffer item). `app/content/manifest.json` regenerated.

## Tested

Local CDN, Chromium via Playwright.
- `node tools/validate.mjs`: 0 errors (392 warnings, all pre-existing "not yet written" and hint warnings).
- Scratch bad cases (deleted afterwards): missing file, 280 KB file, non-UTF-8 file, `..` path, absolute path, path outside `content/data/`, bad names, empty `data`, non-boolean `dataPeek`, `data` on C++, `allocCheck` on Python, `allocCheck: "yes"`, an `operator new` and an `alloc_count()` in a prelude: each gave the intended error.
- `playthrough --exam mock-sample-data` (and with `--mobile`): 3 items, 3 of 3, passed; mock checks pass. A direct widget probe (scratch) graded each starter and solution: Python data item starter fails tests 1 and 2, solution passes 4 of 4 (including a test that reads `sample-prices.csv` by bare name in `setup`, and one that writes its own `tiny.csv`); the 390 px screenshot of the data panel reads correctly.
- Drill probe (scratch, Playwright on `#drill/sample-data-drill`): edited starter fails tests 1 and 2, solution passes 4 of 4.
- `allocCheck` pool item (the brief's P-pool tests): reference passes 10 of 10 with `alloc_count()` 0 after 100 allocate/release; a correct starter that copies a vector per call fails only test 10 with "Expected 0, got 100". With `leakCheck` also on, the buffer reference passes 5 of 5; the starter (no destructor) fails every row with the leak message.
- The four systems brief problems, with the brief's own tests, `allocCheck: true`, under the app's clang 21 at `-O1`: P-pool, P-format-price, P-latency-hist and P-handler references all pass (10, 9, 12, 14 of 14), starters fail (P-pool 7 of 10, P-format-price 6 of 9 with the count test reading 6, P-latency-hist 10 of 12, P-handler 11 of 14 including the count test). (P-handler needs `#include <vector>` in its prelude; the brief's prelude must carry it.)
- Optimiser behaviour (important): at `-O1` clang 21 deletes a visible `new`/`delete` pair even though `operator new` is replaced and the counter is volatile. Measured without a flag: a loop of `int* t = new int(i); delete t;` and one with `new int[8]` counted 0 for 10 iterations, while `make_unique`, `std::nothrow` new, `std::vector` and `std::string` (heap) counted 10. Host clang 18 reproduces it and shows `-fno-builtin` fixes it (`-fno-assume-sane-operator-new` does not). With `-fno-builtin` all six forms count 10 at `-O1`, `-O2`, `-O3`, with and without `leakCheck`, and a `new int[]`/`delete[]` per call in a leak-checked class counted 20 for 20 calls. This differs from the README's claim that the plain stand-in header survives `-O1`: it did for the brief's four problems (allocations through `std::vector`), not for raw `new`/`delete`.
- Regression: `playthrough --lesson cpp/l2-fixed-types, cpp/l9-owning-memory, cpp/l11-creation-destruction, alpha/l1-choosing-a-universe`: all ok. No existing lesson uses `leakCheck`; the only `leakCheck` use is my sample. `playthrough --exams` (every exam including the new sample): All passed. The full `--all` lesson run was not repeated (the brief asked for a regression subset plus `--exams`).

## Deviations from the brief shapes

- `data` is Python only and the validator rejects it on C++ (as the inbox says); the brief shape is otherwise exact (`data: { "x.csv": "content/data/x.csv" }`, subfolders under `content/data/` are allowed, for example `content/data/systems/feed.hex`).
- Drill tests cannot use `setup` (the drill harness evaluates each `call` as one expression); read or write files inside the call.
- `allocCheck` also adds `-fno-builtin` (not in the brief) and so skips the precompiled header; over-aligned `new` is not counted (the stand-in did not count it either). The inbox bullet's "also a read-only panel" was built as an opt-out panel (`dataPeek: false`).
- `alloc_count()` returns `int`.

## Follow-ups

- Systems level agents: the four problems pass as written; P-handler's prelude needs `#include <vector>`. A `how` line should say which calls are counted.
- Agent A's `sample` flag: nothing in the validator or loader depends on it yet; the sample drill is hidden from the validator's index warning only. The sample exam `mock-sample-data` will appear in the mock list until the flag hides it.
- If a content level needs a data file that the learner should discover unaided, set `dataPeek: false`.
- Not done: DataFrame and NaN compare for `isclose`/`equal` (briefs worked round it).
