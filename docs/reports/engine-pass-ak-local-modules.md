# Engine 1266: shipped modules never trigger a package load

A module a widget ships (any `.py` name in `files` or `data`, by basename) is no longer passed to package loading, so a shipped `autograd.py` downloads no Pyodide `autograd` wheel.

- `drill-worker.js`: `importsToLoad(code, spec)` reads `spec.local`; with shipped modules it loads only the other imports (via `find_imports`), otherwise passes the code unchanged.
- `code.js`: `shippedNames`, `importHintFor(files, ...)` (hint leaves shipped modules out); `spec.local` sent for code widgets and the trainer; `casePlan` returns `local`.
- `drill.js`: same for drills (`P.data`). `code-runner.mjs` mirrors the worker for `grade-all`.
- Test: six checks in `tools/test-trainer.mjs` (autograd skipped, numpy and pandas still loaded, no change without a shipped module, hint, trainer still imports the local file).
- Docs: backlog 1266 and status line, AUTHORING section 9.

Run: test-trainer 16/0, test-engine-runtime all passed, grade-all `--code --strand ai` 0 failures, validate 0 errors, playthrough backprop l16 desktop and mobile green.
