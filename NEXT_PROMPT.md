Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2b, "Engine: breadth visuals and complex grading". Engine only; never edit content. Source: the inbox section "Raised later (breadth briefs ...)" in `docs/BACKLOG-INBOX.md`; number its bullets from 429 in `docs/ENGINE-BACKLOG.md`.

Do: launch `engine-dev` agents in parallel, each owning disjoint files:
1. Grading (`app/js/engine/grade.js`, `widgets/expression.js`, `widgets/order.js`, code harnesses): compare real and imaginary parts at every seeded point; accept 1/(1 + i) = (1 − i)/2; reject 3 − 4i for 3 + 4i and 0 for (1 + i)²; complex `isclose` with tolerance in Python and C++; vector answers in one `expression`; `order` distractor lines.
2. `plane.js`: vector-field and slope-field layers, slider-bound; a trajectory traced by RK4 from a dragged start.
3. A new complex-mapping canvas (z-plane grid beside its image under f); `vectors.js` exposes `state.matrix` to `derive` and maps every vector.
4. `walk.js`: overlays (S_n² − n, (q/p)^S_n, a bankroll), the average at stopping, slider-bound barriers, a mean-reverting mode.
5. A new rotatable 3D canvas (item 241): drag to rotate, depth order, vectors, curves, surfaces, field arrows.
Parallel agents put shared-file changes (`validate.mjs`, `playthrough.mjs`, canvas registry, AUTHORING.md, READMEs, System gallery) in their reports; one integration agent then applies them, adds gallery examples, and documents every feature.

Context not in state files: the breadth briefs list fallbacks under "engine limits"; the next task rewrites them. `pkgs` is unbuilt: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Acceptance:
- Each feature has a gallery example in both themes, screenshotted at desktop and `--mobile`.
- From `app/`, `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors; `git diff app/content` touches only `manifest.json`.
- Playthrough with `--local-cdn` is green for every existing lesson using `expression`, `order`, `plane`, `vectors`, `walk` or `code`.
- Report `docs/reports/engine-breadth-2.md`; PLAN.md ticks the item; NEXT_PROMPT.md names "Brief revision".
