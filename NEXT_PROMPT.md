Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2b, "Brief revision". Briefs only; never edit content or engine files.

Goal: every engine fallback in the seven breadth briefs (`docs/briefs/proof.md`, `analysis.md`, `linear-maps.md`, `complex.md`, `vector-calc.md`, `odes.md`, `gap-markov-2.md`) is replaced with the features the engine now has, so no level ships a static or reduced visual. Fallbacks sit in each brief's "Engine limits known before writing" bullets and in per-level canvas and widget lines (fixed oblique projections, pairs of planes, hand-listed arrows and orbits, Re and Im graded as separate cells, per-component curl answers, `choice` for flawed-line spotting, walks without overlays).

New features (option names and examples: `docs/reports/engine-breadth-2.md`, `docs/AUTHORING.md`, `app/js/engine/canvas/README-B.md`, System gallery `#system`):
- `expression`: complex values by real and imaginary parts; vector answers `(a, b, c)` or pmatrix; `\min`, `\max`, capital N, `\epsilon` = `\varepsilon`.
- Code: complex `isclose` (Python `cmath`; C++ `expect: { "re", "im" }`).
- `order`: `distractors` (a "Left out" list) and `same` groups.
- `plane`: `field`, `slopeField`, `trajectory` (RK4 from a dragged start), slider-bound.
- `complex-map` canvas: z-plane grid beside its image under f, dragged z, slider-bound f.
- `vectors`: `state.matrix` maps every vector; `derive` reads `matrix`, `det`, `image.<id>`.
- `walk`: overlays `sq`, `ratio`, `bankroll`, `expr`; `showStopped`; slider-bound `lower`/`upper`; `model: "ou"`.
- `space` canvas: rotatable 3D vectors, spans, curves, surfaces, fields (no 3D dragging yet: item 438; about 1,600 cells cap).

Do: one agent per brief in parallel (Sonnet, or Opus if the user says so), each editing only its brief. Also update DECISIONS.md's breadth-brief line on complex grading. Remaining real limits stay in the brief, numbered against ENGINE-BACKLOG items 438 to 448.

Acceptance: `grep -n -i "fallback\|oblique\|pair of planes\|by hand\|per component\|separate cells"` over the seven briefs finds no engine workaround still in use; each brief names the new option for every visual it changed; lesson ids unchanged; PLAN.md ticks "Brief revision"; NEXT_PROMPT.md names the next task ("Briefs for 2.5, 2.6, 3.2 additions and 3.4 courses").
