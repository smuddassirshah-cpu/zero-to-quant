NEXT_PROMPT-AI: AI strand build sessions (after session AK, 27 Nov)

This file drives AI-strand build sessions only. Audit sessions use `NEXT_PROMPT.md`; never mix the two in one session (DECISIONS "Session AK").

Read CLAUDE.md, `docs/briefs/ai-strand-curriculum.md` (approved), `docs/reviews/review-ai-strand.md` (findings F1 to F18), DECISIONS "Session AK", PLAN section 8.

Next task: the first unticked item of PLAN section 8. Order is fixed: A1 (strand `ai`, blocking) and A2 (timing spike) before A3; A3 and A4 before any content wave.

Context not in state files:
- Strands today are only `quant` and `pure` (`app/js/content.js` lines 56 to 77 and 139; `learn.js` 283). The stage topic count and role readiness count every course, so an AI course would join the quant path without A1.
- No AI level is ever added to an existing course; reuse is by `requires` edges only.
- In-app code is NumPy and pure Python in Pyodide; no PyTorch. Code cases time out at 5 s plus the case budget (`app/js/engine/widgets/code.js` line 28).
- This container's system Python has no scikit-learn; number scripts need the venv named in `docs/LEVEL-BRIEF.md` or a fresh one.

Files to touch for A1: `app/js/content.js`, `app/js/hours.js`, `app/tools/curriculum-hours.mjs`, `app/tools/census.mjs`, `app/tools/validate.mjs`, the settings and Today screens, `tools/fixtures/mini-app`, `docs/AUTHORING.md`.

Acceptance: validator 0 errors; tests the engine agent touched pass; `playthrough.mjs --changed` green; a green `acceptance.yml` run on the pushed HEAD. Census unchanged by A1 and A2 (no content): lessons 1,236; levels 283; hours 3,695, gap 0.
