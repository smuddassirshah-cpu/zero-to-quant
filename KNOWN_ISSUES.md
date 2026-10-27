# KNOWN ISSUES

Open at migration (27 Oct 2026)
- Work left in flight: engine pass 7 edits in `app/js/` may be half-applied (validator shows 0 errors; full playthrough not re-run since). Content on disk without reports: arma L2, L3; alpha L3, L4; opt-dash L2 to L4 partial. `docs/reviews/review-1.9.md` may be partial (its reader never reported). See PLAN.md task 0.
- `docs/BACKLOG-INBOX.md` holds about 136 unnumbered engine bullets awaiting pass 7.
- Seven homework items have both prose and a hidden longform prompt (list in ENGINE-BACKLOG.md pass 6 note).
- Topic 1.8 and 1.9 have no exams; Stage 2 and 3 have none.

Engine gotchas
- `unit: "%"` on a numeric widget divides the typed value by 100: store the fraction.
- `fmtNum` rounds numeric answers to 6 decimal places, so answers below 1e-6 must be rescaled in the prose.
- `__learner_source__` is visible to tests only when a prelude or postlude exists.
- The grader reads a capital `N` in a formula as a built-in function.
- Code cases: a 5 s limit per case (plus `budget` or 30 s for heavy imports), reported against the case that hit it; `isclose` has a fixed 1e-12 tolerance (C++) or rel 1e-9 (Python); no per-test `tol` yet.
- A shared generator line `import numpy as np, pandas as pd` loads numpy only in the worker; write separate import lines.
- `graph` edges draw undirected unless `directed` is set, against README-B.
- `tree` canvas: no binary mode, no inner-node values, no per-node label patch, throws when the root is collapsed; recombining lattices are drawn with `graph` rectangles.
- `grid`: a `null` in a `mark` patch prints "null".
- `plane`: `derive` cannot target an `area` by id (use `area.to`); no `erf`/Phi in curve formulas before pass 7.
- Set-mode playthrough is flaky while other agents write files in the same folder; re-run alone before treating a failure as real.
- Pyodide first loads: scikit-learn 20 to 40 s, statsmodels 20 to 40 s; every `how` on such screens says so.

C++ runtime
- Compiles at `-O1`, asserts on, no `-Wall`, one file only, no `try`/`catch` (no unwinder; a `throw` ends the program).
- Precompiled-header bug: a later `#include` of a new header can fail depending on timing; put headers in the hidden setup code.
- Undefined behaviour never traps in WebAssembly (null reads, use after free, double delete run silently); lessons show native sanitiser output instead.
- libc++ `std::normal_distribution` draws differ from libstdc++ and NumPy; expected values come from the app runtime.
- `std::chrono::steady_clock` ticks every 100 µs in Chromium; timings are illustrative, never graded.
- A range-for over a braced list needs `<initializer_list>` included.

Process
- Session and weekly usage caps stop every agent mid-task; work is saved on disk, so checkpoint-commit, then resume or triage.
- Validator warnings are mostly "ladder changes canvas kind" and "not yet written"; only errors block.
