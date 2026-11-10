# Engine pass: planted-wrong-solution check (ENGINE-BACKLOG 844)

No existing drill holds wrong solutions under another name, so the new optional field is `planted`: `[{ "code", "slip" }]`.

Changes:
- `app/tools/playthrough.mjs`: new `--planted` mode with `--drill` or `--drills` (`plantedOne`). It reuses `drillReady`, `drillSubmit` and the `ZQDrill` hooks, so Python and C++ both work. The starter, every planted solution and the model solution are submitted; one `PLANTED-FAIL` line per problem, `PLANTED-OK` per clean drill. It also fails a starter that passes every test (the spec named only the model and planted checks; the starter run was asked for).
- `app/tools/planted-check.mjs`: the CLI. Chooses the drills, runs the playthrough once, formats failures, adds `--require` and the skip count, exits 1 on any failure. Honours `ZQ_APP_DIR`.
- `app/tools/validate.mjs`: shape only (array, objects, non-empty `code` and `slip`; unknown keys warn).
- `app/tools/test-planted-check.mjs` and `app/tools/fixtures/planted/` (four drills, built by `gen.mjs`): caught and missed, in Python and C++, plus `--require`, the skip, and three bad shapes. The copy's own validator lists the fixtures in its manifest first.
- Docs: `docs/AUTHORING.md` section 5, `docs/briefs/drills-1.8.md` check 4a, `docs/ENGINE-BACKLOG.md` item 844. No content edited.

Open: no existing drill carries `planted` yet, so the tool has run only on fixtures; a content pass must add the planted solutions from the two reviews.

## Usage

```
cd app
node tools/planted-check.mjs --drill <id> [--drill <id2>] [--require] [--local-cdn <pkgs>]
node tools/planted-check.mjs --all-drills [--require] [--local-cdn <pkgs>]
node tools/test-planted-check.mjs [--no-cpp] [--local-cdn <pkgs>]
```
Output: `FAIL <id>: planted[0] passes all 14 hidden tests (slip: ...)`, then `planted-check: N drills checked, M planted solutions, K skipped without any, F failures`. Exit 1 on any failure.

- Item 844 fix (stale read after a timed-out planted solution): `plantedOne` in `app/tools/playthrough.mjs` now submits through a local helper that awaits `drillReady` first, then awaits that submit's own promise before reading the results panel, so a Python restart can no longer leave the previous run's results to be read as the model's.
- Test: fixture `planted-py-timeout` (first planted solution loops forever, second fails normally) added to `tools/test-planted-check.mjs`; green, as is `--require` over the 15 pack-1 `ci-` drills (44 planted solutions, 0 failures).
