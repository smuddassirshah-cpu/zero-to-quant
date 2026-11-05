Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, with own pass 243; exams 22 topic, 1 stage, 11 mock; drills 35 (oa 8); bank 200; hours 3,265 stored, 3,695 summed.

Task: PLAN 2c item 7, dependency rationale pass (F02, F03).

Context not in state files:
- 248 cross-course `requires` edges, all plain strings, none with `why`. Engine-dev picks the schema (object form or a parallel map), keeps strings valid, and the validator errors on a missing `why` only after the fill.
- Content agents never edit `course.json`: one Sonnet agent drafts a JSON proposal of `why` lines; the main session reviews and applies it by script. Edges without a defensible reason are cut or become diagnostics, each listed in the report.
- Gates and the Strict default stay (DECISIONS "Interview closures under Strict mode").
- pdes/L1 and L3 hang on unwritten odes/L4 and numerics/L4. Ask the user once whether those are written before 2b; do not act unasked.
- Local CDN: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Prune with `node app/tools/perf-pending.mjs --prune` after any merge.

Steps: one engine-dev in place (schema, rule, route-limited label, closure tool); main session applies `why` by script.

Files: `app/content/courses/*/course.json` (by script), `app/tools/validate.mjs`, `app/js/screens/learn.js`, `app/js/screens/prepare.js`, `docs/AUTHORING.md`, `docs/reports/closure-item7.md`.

Acceptance:
- Closure report in `docs/reports/` with the trader closure before and after.
- No cross-course edge without `why`; validator 0 errors; readiness-sums exits 0.
- Learn shows "route limited: odes/L4, numerics/L4 unwritten" on pdes.
- `--routes-only --local-cdn` green with and without `--mobile`.
- Next prompt: item 8.
