Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored"). Work on `claude/amazing-wright-d4mx7i` only (DECISIONS "Branches (4 Nov)").

Task: PLAN.md 2a order item 5, engine pass C part 1: E11 follow-up parts with `C-parts-credit`, `C-parts-mixed` and `C-parts-code`; then E14 data files with `C-data-cap`.

Steps:
1. One engine-dev agent (Sonnet) numbers the bullets into `docs/ENGINE-BACKLOG.md` from 467. Sources: `docs/briefs/interview-plan.md` section (f) (E11, E14), the `docs/BACKLOG-INBOX.md` sections "Raised later (brief research-int / coding-int / systems, 4 Nov)", "(fix pass ... brief, 4 Nov)" and "(topic 3.5 briefs, engine requirements, 4 Nov)". The field shapes the levels use are in `docs/briefs/research-int.md` (engine table), `coding-int.md` and `systems.md` (engine sections).
2. Build `parts` on items in lessons' review and homework, sets, bank and exam papers (not quiz items). Parts may mix `numeric`, `choice`, `multi`, `table` and `code`; per-part credit, reveal after each check. Then `data` on `code` widgets, drills and exam items, with the size cap. Add validator checks, a sample under `content/` touched by no course, and playthrough support. Document both in `docs/AUTHORING.md`.
3. An answer-check or second-reader agent tests the sample against the brief uses: research-int R1.2, systems homework-1 item 2, coding-int homework-4 items 1 and 2 (`parts`); research-int l10 (`data`).

Context: no level files exist yet. Build the local CDN (`bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`); split runs per KNOWN_ISSUES.

Files likely touched: `app/js/engine/` (item and widget code, code runner), `app/js/screens/` (review, exam, bank deck), `app/tools/validate.mjs`, `app/tools/playthrough.mjs`, `docs/AUTHORING.md`, `docs/ENGINE-BACKLOG.md`, `docs/reports/engine-pass-c-1.md`, state files.

Acceptance: from `app/`, `node tools/validate.mjs 2>&1 | tail -5` gives 0 errors; the sample plays green with and without `--mobile`. `--sets`, `--exams`, `--bank all` and `--routes-only` stay green. AUTHORING documents `parts` and `data`. PLAN marks part 1 done. Next: engine pass C part 2 (E8, E3, `C-alloc-check`, E13), with coding-int L1 able to start in parallel.
