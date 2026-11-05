# Engine pass: C++ freed-memory harness (items 518 to 520)

- 518: `app/js/engine/widgets/cpp-grade.js`. One operator set for `allocCheck` and `leakCheck` (the bare-malloc `ALLOC_OPS` is gone). Header holds magic, kind, size. `delete` poisons with 0xDD, marks the header freed, keeps the block (quarantine, 64 MB cap then plain free). A second delete prints "Memory error: a block was deleted twice." and exits 1. Leak reporting is off for `allocCheck` alone.
- 519: `free_count()` and `live_blocks()`; validator updated in `app/tools/validate.mjs`.
- 520: `highlight.ranges` documented in `app/js/engine/canvas/README-B.md`.
- Docs: `docs/AUTHORING.md` section 3, `docs/ENGINE-BACKLOG.md`, inbox bullets marked.

Checks: validate 0 errors. App-toolchain runner (c++17): P-copy-samples solution 0 of 13 failed; `unc:delete-first-no-guard` now 1 of 13 failed ("a = a" case reads poison, got 0); P-move-buffer `move-ctor-forgets-null` and `move-assign-forgets-null` fail via "Memory error: a block was deleted twice.". Playthroughs: systems l15, l18, homework-4 and mock-sample-data pass; `--drills` all ok except Python drill rq-clean-frame-py (no C++, not touched; fails alone too).
