# Zero to Quant

An interactive learning app that takes one adult from school arithmetic to quant-interview readiness, and towards the research habits of a machine-learning lab, along the curriculum in `docs/curriculum.md`: Stages 0 to 3, 3,390 mapped hours on the trader track, 3,450 on the researcher and ML research tracks and 3,470 on the developer track. It teaches the way Brilliant does: short screens built around a diagram the learner manipulates, immediate diagnosed feedback, spaced review, homework and timed papers. Brainy Bertie, a small Einstein-style bobble head, is the mascot and the face of an AI tutor that never becomes the source of truth.

One TypeScript codebase builds two targets:

- a claude.ai Artifact for daily use on any device, whose tutor runs on the viewer's own Claude account and whose progress syncs through the Artifact's database;
- a static, offline-capable web app (local, or deployed behind access control until a content licence is chosen: `docs/PLAN.md` 12 decision 13) with full Python in the browser (Pyodide with NumPy, pandas, SciPy, statsmodels, scikit-learn and matplotlib) for code drills, whose tutor calls a small proxy that holds the API key.

## Status

The Blueprint carries the owner's decisions of 7 October 2026 and awaits his "approved, continue" (this line is updated at the gate merge). The build has not started; `STATE.md` tracks it stage by stage. Getting-started instructions arrive with build stage 1.

## Where things are

| Path | What |
|---|---|
| `docs/PLAN.md` | The blueprint: every architectural decision, the threat model, and the build stages with their definitions of done |
| `docs/ARCHITECTURE.md`, `WIDGETS.md`, `CONTENT-FORMAT.md`, `AI-TUTOR.md`, `ASSESSMENT.md`, `BERTIE.md`, `CURRICULUM.md` | The appendices; `PLAN.md` section 1 lists what each owns |
| `docs/DECISIONS.md` | Decisions with their rejected alternatives, waivers, raw-HTML sink justifications, spike results |
| `CLAUDE.md` | The build protocol every build session follows |
| `STATE.md` | Stage status, gates, open questions and the next action |
| `docs/curriculum.md`, `docs/curriculum/` | The owner's curriculum and the fifteen item files that detail it |
| `docs/design-research.md` | The researched Brilliant recreation spec |
| `prototype/` | The approved Stage 1 clickable mockups (`prototype/README.md` says how to open them) |
| `spikes/` | Measured platform spikes |

## How the build is gated

- The build runs in the numbered stages of `docs/PLAN.md` section 11: the engine and its domain services, every P0 widget batch, Bertie and the tutor, progress and assessments, the two builds, then content depth-first from 0.1, one level per gate.
- Each stage has its own branch, `stage/<n>`. Every pull request is reviewed by a second agent session and merges into that branch; the owner reviews the stage as a whole, and the next stage starts only after his literal reply "approved, continue". Only the owner merges into `main`.
- Every auto-graded numeric, symbolic and set answer, and every item generator, is proved by two independent implementations in CI; code drills are graded by authored test suites that CI runs against a reference solution and known-wrong solutions; long-form work is marked against authored rubrics, and in a gate each rubric point counts the lower of the learner's and Bertie's marks.
- The Artifact publishes only files built from this repository's own sources: third-party JavaScript loads from CDNs at pinned versions, and every Python, SQL and C++ drill hands off to the web app.

## Licence

Code: MIT (added at build stage 1). The repository is private; the content licence is decided before anything is made public.
