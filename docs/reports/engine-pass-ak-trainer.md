# Engine pass AK: trainer widget and data files (PLAN section 8, A3 widget and data part)

Items 1237 to 1241 in `docs/ENGINE-BACKLOG.md` (status block "Engine pass AK").

## Trainer (1237)

- **Mode of `code.js`, not a new file.** It needs the private Python runner (`Py`) and `Editor`; a separate file would mean exporting both. It registers as `kind: "trainer"` so authors and the validator see a distinct widget. Player change: one line, `graded` is false for `trainer` (screen is read-only, Continue always open, not counted in the graded total; Start over resets it).
- **Plumbing reused.** Same worker. `drill-worker.js` gained one line: `drl_run` publishes `emit` as `builtins.__zq_emit__`, so the trainer's harness streams `{kind:"steps", rows}` events while the Python is still running. `Py.stop()` (new) ends a run by replacing the worker, as the existing timeouts do.
- **Behaviour.** `report(step, loss, name=value)` or a printed `step N loss X` line fills the series; rows batch at 50 ms and the page redraws every 80 ms through `canvas.set({series:{id:{values}}})`. Step cap (`steps`, default 500, counted in reports) and wall-clock cap (`maxSeconds`, default 120, max 300, package load excluded) raise a `BaseException` the learner's `except Exception` cannot swallow; the page timer is the backstop for a loop that never reports. Defaults follow the timing spike (500 GPT steps 43 s on a desktop, 3 to 5 times that on a phone): authors set `maxSeconds` for the phone.
- **Canvas.** `series` gained `params.length` (fixed x width); the validator requires `params.y`, `params.length >= steps` and declared series ids.
- **Tests.** `tools/test-trainer.mjs` (10 cases, runs the harness in Pyodide with the page's grader), `tools/test-validate-trainer.mjs` (20 cases). Not exercised in a real browser on a lesson screen: no content uses the widget yet; the first AI lesson should be played with `playthrough.mjs --lesson`.

## Data (1238, 1239)

- `app/content/data/ai/names.txt`: 32,032 names, 228,145 bytes. makemore `LICENSE` read: MIT, Copyright (c) 2022 Andrej Karpathy. Names come from SSA 2018 data.
- `app/content/data/ai/tiny-shakespeare.txt`: the first 250,000 characters (250,000 bytes, ASCII, 62 of the 65 characters; the cap is 256 KB, unchanged) of char-rnn `data/tinyshakespeare/input.txt` (1,115,394). `tiny-shakespeare-vocab.json` lists all 65 characters of the full text (the slice lacks `$`, `3`, `X`). Text is public domain. **Not verified:** the char-rnn repository's own licence (API blocked, LICENSE paths 404); the README says so.
- Credit lines and the digits note are in `content/data/ai/README.md`. `load_digits()` works offline in Pyodide (scikit-learn 1.6.1, 1,797 by 64, checked here); UCI, CC BY 4.0.

## Drill pattern (1240)

No engine change. The drill form already gives timed from-scratch Python (stopwatch with `pace`, 60-minute sessions, NumPy, `data`, planted wrong solutions). Recipe and limits (5 s a test, no `budget`, no ML slug in `PATTERNS`, `pattern` optional) are in AUTHORING section 5. The bank family for the mock is not part of this item.

## Checks

`node tools/validate.mjs`: 0 errors. Passed: `test-trainer`, `test-validate-trainer`, `test-validate-harness`, `test-validate-perf`, `test-validate-dice-sim`, `test-engine-runtime`, `test-grade-code`. Playthrough smoke (`--all --changed --shard 1/16`): see the hand-back line.
