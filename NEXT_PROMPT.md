Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2b, second item: the engine item for the maths breadth pass. Launch one `engine-dev` agent (Sonnet). The main session plans and reviews only.

Context: the breadth plan is done (`docs/briefs/breadth-plan.md`, read its `## Engine notes` section). Thirteen new course maps (`proof`, `analysis`, `linear-maps`, `complex`, `vector-calc`, `odes`, `numerics`, `convex`, `stat-models`, `measure-prob`, `pdes`, `algebra`, `topology`) carry top-level `strand` ("quant" or "pure") and `strandNote` (roles). The validator accepts these fields without checking them and the app ignores them. Topics 0.6, 1.10, 1.11, 2.5, 2.6, 3.4 and the 3.2 additions are in `app/content/curriculum.json`; every new lesson is unwritten. Stage hours and exit lines in curriculum.json were left unchanged.

The agent must:
1. Show the new topics with targets on the Learn screen (`app/js/screens/learn.js`); exams list them; nothing throws on a course with no written lessons.
2. Validator accepts and checks `strand` (only "quant" or "pure") and `strandNote` (non-empty string when `strand` is set).
3. Add a "Pure maths" or "Quant" badge, with `strandNote` as its detail, on course cards, the lesson start screen, topic chips and exam chips; distinct in light and dark themes; untagged courses show no badge.
4. Add a "Quant path only" setting that hides pure courses and drops them from stage-exam gating and stage progress.
5. Document it in `docs/AUTHORING.md`; number any inbox bullets it adds per CLAUDE.md.

Files likely touched: `app/js/screens/learn.js`, course card and lesson start screens, settings screen, exam list, `app/css/`, `app/tools/validate.mjs`, `docs/AUTHORING.md`, `docs/ENGINE-BACKLOG.md`.

Acceptance:
- From `app/`, `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors, and a bad `strand` value in a scratch copy is rejected.
- Playthrough of one existing lesson per stage and the routes is green (`--routes-only`, with `--local-cdn` built by `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`).
- Screenshots in both themes show the badge on a pure and a quant course and none on a core course; with "Quant path only" on, pure courses vanish.
- PLAN.md ticks the engine item; NEXT_PROMPT.md names the briefs item for 0.6, 1.10, 1.11 and markov L5.
