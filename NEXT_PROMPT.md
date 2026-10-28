Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2b, "Briefs for 2.5, 2.6, 3.2 additions and 3.4 courses". Briefs only; never edit content, engine files or `course.json`.

Goal: one brief per course, written from its section of `docs/briefs/breadth-plan.md`: `docs/briefs/numerics.md` and `convex.md` (topic 2.5), `stat-models.md` (2.6), `measure-prob.md` and `pdes.md` (3.2 additions), `algebra.md` and `topology.md` (3.4, optional and uncounted). Each brief has a course-context paragraph and one section per level, in the shape of the seven finished breadth briefs (`docs/briefs/odes.md` and `linear-maps.md` are good patterns), following `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md`.

Context not in the state files:
- Design every visual with the engine as it now is: `expression` (complex, vector, `\min`, `\max`, capital N, `\epsilon`), complex `isclose`, `order` `distractors` and `same`, `plane` `field`/`slopeField`/`trajectory`, `complex-map`, `space`, `vectors` `state.matrix`, `walk` overlays and `model: "ou"` (`docs/reports/engine-breadth-2.md`, `app/js/engine/canvas/README-B.md`). No fallbacks to static visuals; a real limit cites ENGINE-BACKLOG items 438 to 448 or goes to `docs/BACKLOG-INBOX.md`.
- Pure courses (algebra, topology) grade proofs step by step (`order`, `choice`, fill-ins) with whole proofs as `longform` homework (DECISIONS, breadth briefs line).
- `numerics` and `pdes` build on `odes` (l11 to l13 and l2, l7, l12 are named in `odes.md`).
- Run seven brief-writers in parallel, one per course, each editing only its brief; every stated number computed twice.

Files likely touched: the seven new briefs, `docs/BACKLOG-INBOX.md`, PLAN.md, PROGRESS.md, DECISIONS.md, NEXT_PROMPT.md.

Acceptance: seven briefs exist; every lesson id and title matches its `course.json` map; each level section names canvases and widgets by option; no "fallback", "precomputed" or "static" workaround for a feature that exists; PLAN.md ticks the task; NEXT_PROMPT.md names the next task ("proof L1: Statements and logic").
