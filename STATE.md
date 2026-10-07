# Build state

Current stage: 2
Last updated: 7 October 2026
Preview Artifact: not yet created (stage 25 creates it; its URL goes here)

`docs/PLAN.md` section 11 holds each stage's deliverable and definition of done; this file records progress against it. From stage 3a up to four sessions run in parallel, each on one stage whose dependencies are approved; every open `stage/<n>` branch is a stage in progress. On a stage branch, edit only that stage's rows here.

## Sessions

| Session | Stage | Branch | Started |
|---|---|---|---|
| Main session (integration, docs, review fixes) and seven sub-sessions (lint, release and CI units; four adversarial reviewers), `session_01J92GRXudcwDnRYVFX2Sqby` | 1 | `stage/1` | 2026-10-07 11:50 UTC |
| The same main session with its workflow sub-sessions (probe builders, tester, adversarial reviewers), `session_01J92GRXudcwDnRYVFX2Sqby` | 2 | `stage/2` | 2026-10-07 16:04 UTC |

## Device-gate queue

Gates waiting for the preview Artifact, oldest first (`PLAN.md` 8.5): none.

## Stages

Status values: pending / in progress / awaiting review / approved. Gate records the date of the owner's "approved, continue". AD is agent-days (6 session hours): the plan's estimate, then the measured figure from the pull requests. Depends on is `PLAN.md` section 11; "10a to 26" means every engine stage from 10a to 26. Batch 38 also needs batch 37's bases, and batch 58 the widgets it embeds from batches 27 to 57 (`PLAN.md` 11.4). The planned total is about 880 AD before content with the 182 AD contingency, and 480 for stages 84 to 100.

| # | Stage | Depends on | AD plan | AD actual | Status | Gate |
|---|---|---|---|---|---|---|
| 1 | Scaffold, toolchain and CI | none | 5 | 1.5 | approved | 2026-10-07 |
| 2 | Spike S1 on the owner's iPhone | 1 | 3 | - | in progress | - |
| 3 | Contracts, maths core, deterministic maths | 1 | 8 | - | pending | - |
| 3a | Numerics in `@zq/mathcore` | 3 | 10 | - | pending | - |
| 3b | `stats-core` in `@zq/mathcore/stats` | 3a | 12 | - | pending | - |
| 3c | `@zq/models/data` | 3a | 14 | - | pending | - |
| 3d | `@zq/models/code` | 3 | 9 | - | pending | - |
| 3e | `@zq/models/algo` and `trace.py` | 3 | 6 | - | pending | - |
| 3f | `@zq/models/git` | 3 | 5 | - | pending | - |
| 3g | `@zq/models/analysis` (added for A1 Real analysis) | 3 | 5 | - | pending | - |
| 4 | Platform adapters and the Artifact host emulator | 2, 3 | 10 | - | pending | - |
| 5 | Design system port | 3 | 8 | - | pending | - |
| 6 | Content schema (C1) | 3 | 5 | - | pending | - |
| 7 | Compiler front end `zq check` (C2) | 6 | 8 | - | pending | - |
| 8 | Independent verifier `zqverify` (C5) | 7 | 8 | - | pending | - |
| 9 | Lesson player reducer and item policies | 3, 6 | 5 | - | pending | - |
| 9a | Event log, `AppendQueue` and fold (assessment stage A1; was stage 68) | 3, 4, 9 | 6 | - | pending | - |
| 10a | Widget runtime | 4, 5 | 7 | - | pending | - |
| 10b | Widget tooling and gallery | 10a | 5 | - | pending | - |
| 11 | Plot primitives | 10b | 12 | - | pending | - |
| 12 | Handles and readouts | 11 | 6 | - | pending | - |
| 13 | Grid and token primitives | 12 | 9 | - | pending | - |
| 14 | Scene layer and four pilots | 13, 3a | 14 | - | pending | - |
| 15 | Expression entry and maths services | 12 | 9 | - | pending | - |
| 16 | Structured inputs | 13, 15 | 8 | - | pending | - |
| 17 | Simulation and data primitives | 13 | 9 | - | pending | - |
| 18 | Free drawing and 3D | 11 | 8 | - | pending | - |
| 19 | Code and text primitives | 13, 3d | 9 | - | pending | - |
| 20 | Graders (C3) | 6, 3 | 8 | - | pending | - |
| 21 | Expression grading (C4) | 15, 20 | 6 | - | pending | - |
| 22 | Generators (C6) | 8, 20 | 8 | - | pending | - |
| 23 | Emit and content runtime (C8, E5) | 7, 8, 10a, 20, 22 | 11 | - | pending | - |
| 24 | Player views and the reference lesson (E6, C9) | 9, 9a, 14, 15, 16, 17, 23 | 10 | - | pending | - |
| 25 | Python runtime on the web app (E8) | 4, 10b, 23, 24 | 11 | - | pending | - |
| 26 | Drill pipeline and SQL (C7) | 7, 25, 3d | 6 | - | pending | - |
| 27 | Widget batch W1a (7 scenes) | 10a to 26 | 7 | - | pending | - |
| 28 | Widget batch W1b (6 scenes, 2 presets) | 10a to 26 | 6 | - | pending | - |
| 29 | Widget batch W1c (2 bespoke, clock-driven) | 10a to 26 | 6 | - | pending | - |
| 30 | Widget batch W1d (bespoke) | 10a to 26 | 6 | - | pending | - |
| 31 | Widget batch W1e (bespoke) | 10a to 26 | 6 | - | pending | - |
| 32 | Widget batch W1f (bespoke on `PythonRuntime`, and 1 scene) | 10a to 26, 3d | 7 | - | pending | - |
| 33 | Widget batch W2a (5 scenes, 1 preset) | 10a to 26 | 6 | - | pending | - |
| 34 | Widget batch W2b (5 scenes) | 10a to 26, 3b | 5 | - | pending | - |
| 35 | Widget batch W2c (2 bespoke) | 10a to 26, 3d | 9 | - | pending | - |
| 36 | Widget batch W3a (6 scenes) | 10a to 26, 3g | 7 | - | pending | - |
| 37 | Widget batch W3b (6 scenes) | 10a to 26 | 6 | - | pending | - |
| 38 | Widget batch W3c (bespoke and 3 presets) | 10a to 26, 37 | 8 | - | pending | - |
| 39 | Widget batch W3d (6 scenes) | 10a to 26, 3b, 3g | 7 | - | pending | - |
| 40 | Widget batch W3e (bespoke) | 10a to 26 | 6 | - | pending | - |
| 41 | Widget batch W3f (2 bespoke, 2 scenes) | 10a to 26, 3d, 3e | 11 | - | pending | - |
| 42 | Widget batch W4a (8 scenes) | 10a to 26, 3e | 7 | - | pending | - |
| 43 | Widget batch W4b (6 scenes) | 10a to 26, 3c | 7 | - | pending | - |
| 44 | Widget batch W4c (5 scenes) | 10a to 26, 3c | 7 | - | pending | - |
| 45 | Widget batch W4d (bespoke and 3 presets) | 10a to 26, 3e | 8 | - | pending | - |
| 46 | Widget batch W4e (3 bespoke) | 10a to 26, 3d | 9 | - | pending | - |
| 47 | Widget batch W4f (2 bespoke) | 10a to 26, 3f | 9 | - | pending | - |
| 48 | Widget batch W4g (3 bespoke) | 10a to 26, 3d | 12 | - | pending | - |
| 49 | Widget batch W5a (9 scenes) | 10a to 26, 3a, 3g | 10 | - | pending | - |
| 50 | Widget batch W5b (8 scenes) | 10a to 26, 3a, 3g | 9 | - | pending | - |
| 51 | Widget batch W5c (7 scenes) | 10a to 26, 3a | 8 | - | pending | - |
| 51a | Widget batch W5d, A1 Real analysis (6 scenes) | 10a to 26, 3g | 8 | - | pending | - |
| 52 | Widget batch W6a (5 scenes) | 10a to 26, 3a | 5 | - | pending | - |
| 53 | Widget batch W6b (5 scenes) | 10a to 26, 3a | 5 | - | pending | - |
| 54 | Widget batch W7a (8 scenes) | 10a to 26, 3b | 10 | - | pending | - |
| 55 | Widget batch W7b (6 scenes) | 10a to 26, 3b | 7 | - | pending | - |
| 56 | Widget batch W7c (8 scenes) | 10a to 26, 3b | 12 | - | pending | - |
| 57 | Widget batch W7d (1 scene, bespoke) | 10a to 26, 3b | 7 | - | pending | - |
| 58 | Widget batch W7e (bespoke) | 10a to 26, 27 to 57 | 6 | - | pending | - |
| 59 | Bertie | 5, 24 | 4 | - | pending | - |
| 60 | Tutor contracts and guards (T0, T1) | 10a, 20 | 6 | - | pending | - |
| 61 | Context assembly and renderers (T2) | 60 | 5 | - | pending | - |
| 62 | Tutor proxy (T3), creates the Class C exposure | 61 | 9 | - | pending | - |
| 63 | Backends and service (T4) | 60, 61, 62 | 5 | - | pending | - |
| 64 | Bertie in the UI (T5) | 59, 63, 9a | 5 | - | pending | - |
| 65 | Modes, wave 1 (T6a) | 63, 64 | 6 | - | pending | - |
| 66 | Modes, wave 2 (T6b, C10) | 65, 32 (`code-cell`), 16, 22 | 7 | - | pending | - |
| 67 | Evals, settings and signals (T7, T8) | 66 | 11 | - | pending | - |
| 68 | (moved to stage 9a; number kept free) | | 0 | | n/a | |
| 69 | Stores (A2), creates the remote-storage exposure | 9a | 10 | - | pending | - |
| 70 | Export, import, sync, result codes, handoff (A3), creates the import exposure | 69 | 5 | - | pending | - |
| 71 | Time, streaks, XP, MP, achievements, ghost race (A4, A14 P0) | 9a | 4 | - | pending | - |
| 72 | Skill graph and mastery (A5) | 9a, 23 | 7 | - | pending | - |
| 73 | Redo queue and review (A6) | 72 | 5 | - | pending | - |
| 74a | App shell and home screens (E7, part 1) | 24, 71, 72 | 7 | - | pending | - |
| 74b | Records and Settings (E7, part 2) | 74a | 5 | - | pending | - |
| 75 | Quiz, review, practice and homework (A7) | 73, 66 | 8 | - | pending | - |
| 76 | Exam engine (A8) | 75 | 13 | - | pending | - |
| 77 | Placement and test-out (A9) | 76 | 5 | - | pending | - |
| 78 | Exit parts and outside work (A10), creates the paste-verify exposure | 70, 76 | 7 | - | pending | - |
| 79 | Planner (A11) | 71, 72, 73, 78 | 8 | - | pending | - |
| 80 | Daily 10 and weekly problems (A12, A13) | 71, 73, 29, 35, 58 | 6 | - | pending | - |
| 81 | Learning record and calibration (A15, P0 parts) | 72, 76, 78 | 4 | - | pending | - |
| 82 | Web target (E9), creates the web-deployment exposure | 74a, 74b, 25, 62, 69, 70 | 7 | - | pending | - |
| 83 | Artifact target and release (E10), creates the published-page exposure | 74a, 74b, 25, 69, 70 | 9 | - | pending | - |
| 84 | Acceptance and first release (C11) | 1 to 83 | 13 | - | pending | - |
| 85 | `crs.numwork` How Numbers Work (0.1 W) | 84 | 21 | - | pending | - |
| 86 | `crs.keys` Keyboard Fluency (0.4 K) | 84, 85 | 10 | - | pending | - |
| 87 | `crs.speed` Arithmetic at Speed (0.5 A) | 84, 86 | 21 | - | pending | - |
| 88 | `crs.bench` Workbench (0.4 B) | 84, 87 | 17 | - | pending | - |
| 89 | `crs.propprec` Proportion, Powers and Precision (0.1 P) | 84, 88 | 31 | - | pending | - |
| 90 | `crs.firstpy` First Programs in Python (0.4 Y) | 84, 89 | 15 | - | pending | - |
| 91 | `crs.expreq` Expressions and Equations (0.2 E) | 84, 90 | 44 | - | pending | - |
| 92 | `crs.lines` Lines and Linear Systems (0.2 L) | 84, 91 | 26 | - | pending | - |
| 93 | `crs.quadpoly` Quadratics and Polynomials (0.2 Q) | 84, 92 | 43 | - | pending | - |
| 94 | `crs.funcs` Functions and Graphs (0.2 F) | 84, 93 | 35 | - | pending | - |
| 95 | `crs.shape` Shape and Space (0.3 S) | 84, 94 | 49 | - | pending | - |
| 96 | `crs.growth` Growth (0.3 G) | 84, 95 | 35 | - | pending | - |
| 97 | `crs.waves` Circles, Waves and Rotations (0.3 T) | 84, 96 | 42 | - | pending | - |
| 98 | `crs.chance` Counting, Chance and Data (0.3 C) | 84, 97 | 34 | - | pending | - |
| 99 | `crs.rigour` Proof, Limits and Curves (0.3 R) | 84, 98 | 34 | - | pending | - |
| 100 | Stage 0 exit | 84, 99 | 10 | - | pending | - |

## Level gates

Stages 84 to 100 are made of level gates (`PLAN.md` 11.6). When a course stage starts, list each of its levels here with branch `stage/<course>/<level>`, its lessons, AD plan and actual, status and gate date.

| Stage | Level | Branch | Lessons | AD plan | AD actual | Status | Gate |
|---|---|---|---|---|---|---|---|
| none yet | | | | | | | |

## Decisions

Running log. One line each: date, decision, reason, `PLAN.md` deviation y/n. Full entries with rejected alternatives are in `docs/DECISIONS.md`.

| Date | Decision | Reason | Deviation |
|---|---|---|---|
| 2026-10-07 | D1 Build order (a): engine and every P0 widget batch before any content; content depth-first from 0.1 | The owner's priority: the best foundation for every later lesson | n |
| 2026-10-07 | D2 Curriculum additions adopted: P1 Research method (35 h, item 2.2c, before 2.3); P2 Continuous-time processes (+15 h in 1.5); P3 Numerical methods, floating point and Monte Carlo (120 h, item 2.0a, first in Stage 2, all tracks); P4 Optimisation (80 h, item 2.0b, before 2.1); O1 contests offset (-80 h from 2.4 outside the developer track); 2.1b Deep learning core (120 h, after 2.1, all tracks); A1 Real analysis (60 h, after 1.3, researcher and ML research tracks). 3,390 h; 3,450 h on the researcher and ML tracks. P5 to P16 not adopted, P8 among them, so files that listed P8 teach its basics themselves. The ML-lab aim stays | The owner's choice of the recommended set; without 2.1b the ML-lab aim is not delivered | n (`PLAN.md` revision 2) |
| 2026-10-07 | D3 Bertie confirmed as drawn except the hair: less spiky, more rounded and fuzzy, soft cloud-like tufts instead of points (`BERTIE.md` draft 3); the owner signs off the hair at stage 59 before baselines | The owner: "Make his hair less spiky, more rounded and fuzzy. Everything else about Bertie is perfect." | n |
| 2026-10-07 | D4 Every other `PLAN.md` 12 decision at its stated default: sealed answer key as recommended; Cloudflare plan by the stated rule; copyright rule and glossary exemption as written, no public release; 9/3/2/1 with borrowing; outside marker and reviewer both, paid; reliance check on; earlier habits off; curriculum D1 to D8 as each item file recommends | The owner took the defaults at review | n |
| 2026-10-07 | D5 Artifact publishing rule: the Artifact publishes only files generated from this repository's own sources; third-party JavaScript from CDNs at exact pinned versions; fonts from Google Fonts only; no Python, SQLite or KaTeX fonts there; MathML; every Python, SQL and C++ drill hands off to the web app. Replaces decision 7, the JSON-part Python layout and fallbacks F1 and F2; `tools/pysplit` removed; stage 2 re-scoped | The publishing tool must read every file it did not write and never publishes one it cannot read | n (`PLAN.md` revision 2, 4.3) |
| 2026-10-07 | D6 Probe Artifacts: to be deleted. Neither was found in the owner's Artifact listing (scope: mine) on 7 October 2026, so nothing was deleted; if either is found, it is deleted with the owner's confirmation (open question 22); `spikes/` keeps the sources and results as the record | The owner's instruction; the results are recorded | n |
| 2026-10-07 | Handoff pack written before stage 1: `CLAUDE.md`, this file, `docs/DECISIONS.md` (sinks S1 and S2, waivers W1 and W2, D1 to D6, open owner items O1 and O2) and `README.md`; stage 1 keeps them current instead of creating them, as its row in `docs/PLAN.md` 11.3 now says | project-forge Phase 2 hands the protocol over with the plan | n |
| 2026-10-07 | Second review round of the Blueprint (`docs/PLAN.md` 13): live-code lesson screens resolve as `read` in the Artifact and are finished in the web app (4.3); decisions 13 (web host before a content licence, default Cloudflare Pages behind Access) and 14 (the Zhou line, default chapter 4) raised for the owner; the stage 2 list made single; provenance over generator modules; one `TexSlots` binding path | Review findings; nothing the owner decided changed | n |
| 2026-10-07 | D7 Decision 13 (b): every deployed web build on Cloudflare Pages behind an Access policy admitting only the owner until a content licence exists; GitHub Pages kept as the public-release path | The owner: "CloudFlare is fine"; keeps "no public release" and the phone handoff | n |
| 2026-10-07 | D8 Decision 14 (b): Zhou chapter 5 joins the Stage 3 exit at 70% cold as exit part `3.3.zhou-ch5` (7 h moved from `3.3.books`); `docs/curriculum.md` gains the checkbox | The owner: "Add in chapter 5"; P2 and PZ6 teach chapter 5 to every learner | n |
| 2026-10-07 | Blueprint approved by the owner ("Approved. Continue"); stage 1 starts | Phase 2 gate | n |
| 2026-10-07 | B1 Tools run on Node's own type stripping; no `tsx` | One fewer loader; the checker refuses what Node cannot run | y: `PLAN.md` 4.1, 3.1; `ARCHITECTURE.md` 3.2, 4.6 |
| 2026-10-07 | B2 `zq/no-colour-literals` on every script file under `src/` | Logic and scenes produce render data too | y: `ARCHITECTURE.md` 10.4 (stricter) |
| 2026-10-07 | B3 The sink rule's two exemptions are hard-coded, with their APIs | A third sink needs a reviewed rule change | n |
| 2026-10-07 | B4 Layering through `zq/layering` | Flat-config entries replace each other per file | y: `ARCHITECTURE.md` 4.5, 10.4 mechanism |
| 2026-10-07 | B5 Merge rights procedural: the GitHub connection is the owner's account; no branch protected yet | GitHub cannot tell a session from the owner | y: `PLAN.md` 7.1 guard mechanism (G1); DoD item not met |
| 2026-10-07 | B6 Hooks advisory, CI the gate; eight pull requests merged before CI existed | A local hook can be skipped | y: `CLAUDE.md` gating rule 3 for #2, #3, #5 to #10 |
| 2026-10-07 | B7 Release budget numbers; retained and peak rows at stage 83 | The host's limits with margin; the ledgers first exist at stage 83 | y: `ARCHITECTURE.md` 6.2.5 |
| 2026-10-07 | B8 Page fragment: `#app`, gate script, bootstrap script | A browser that cannot parse `import()` still shows the gate | y: `ARCHITECTURE.md` 6.2.2 order |
| 2026-10-07 | B9 `ZQ_DEV_ROUTES=1`; `dev:artifact` a watch build until stage 4 | Preview Artifacts need dev routes; the emulator completes at stage 4 | y: `ARCHITECTURE.md` 6.5, 10.1 until stage 4 |
| 2026-10-07 | B10 `stage/1` from the Blueprint branch | `main` lacked the documents stage 1 implements | y: `CLAUDE.md` gating rule 2 |
| 2026-10-07 | B11 Playwright image `v1.63.0-noble` with its digest | A digest cannot move | n |
| 2026-10-07 | B12 No inline lint configuration anywhere | One comment could add a third sink | n |
| 2026-10-07 | B13 Every file belongs to a layer; targets normalised | Unlisted folders and `..` escaped | n |
| 2026-10-07 | B14 Five pull requests over the line cap; no per-pull-request effort records | Units split after the fact, by parallel sessions | y: `PLAN.md` 11.1, `CLAUDE.md` gating rule 3 |
| 2026-10-07 | B15 JSX settings wait for Preact | knip reports an unlisted `preact` | y: `ARCHITECTURE.md` 4.6 |
| 2026-10-07 | B16 Files added outside the trees (`tools/ci/`, `tsconfig.node.base.json`, `src/html/dev.html`, Python and CI data files) | Each implements a stage 1 item; nothing moved | y: `PLAN.md` 10, `ARCHITECTURE.md` 4.4; for the owner |
| 2026-10-07 | L1 Four licence exceptions under stylelint (MIT-0, a legacy `licenses` field) | Development only, permissive | n; for the owner |
| 2026-10-07 | A1 `braces` 3.0.3 advisory waived to 7 November 2026 | No fix exists; development only | n; for the owner |
| 2026-10-07 | A2 `pytest` 9.0.2 advisory waived to 7 November 2026 | Pinned to Pyodide's version | n; for the owner |
| 2026-10-07 | T1 gitleaks 8.30.1, pip-audit 2.10.1, the Go floor; npm-only licence gate until stage 25 | Named in `PLAN.md` 7.1 and 7.6 | n; versions for the owner |
| 2026-10-07 | G1 The label guard: owner's label after the head commit, reset on every push, on `pull_request_target` | The owner cannot approve his own pull request | y: `PLAN.md` 7.1 |
| 2026-10-07 | Stage 1 gate: approved by the owner ("Approved and continue"); A1, A2 (pytest stays at 9.0.2, Pyodide's version), L1, T1 and B16 approved; branch protection to be applied by the owner per `README.md`; the superseded `stage1/*` branches may be deleted once stage 1 reaches `main`; the licence holder is Syed Muddassir Shah | The owner's answers at the gate | n |
| 2026-10-07 | B17 `stage/2` branched from `stage/1`, not `main` | `main` does not carry stage 1 until the owner merges it | y: `CLAUDE.md` gating rule 2 |
| 2026-10-07 | B18 The spike S1 source archived in `spikes/s1/` and `spikes/s1-dbsize/` in one pull request; the npm mirror fetched, not committed | Evidence, not engine code; reviewed before publishing | y: `PLAN.md` 11.1 line cap |
| 2026-10-07 | B19 The probe declares `db` (six rules), `user` (profile) and `sample`; `permissions` is built in and not declared | The capabilities contract 0.2.73 | n |
| 2026-10-07 | B20 The probe's `TexSlots` binding also rewrites KaTeX's TeX annotation, which repeats the sentinels; proposed for decision 37 | No sentinel text may survive in the tree | y: `ARCHITECTURE.md` decision 37 and 5.11, `PLAN.md` conflict 10; for the owner |
| 2026-10-07 | B21 Sub-session files read in full by the publishing session count as the session's own for hard rule 2 | Gating rule 4 delegates; the publisher read and hashed every file | y: interpretation of hard rule 2; for the owner |

## Open questions

Each with the stage it affects; the stage that closes it records the answer in `docs/DECISIONS.md`.

| # | Question | Affects | Closes at |
|---|---|---|---|
| 1 | Does the Artifact page honour an import map in its fragment, and does iOS 18.7 enforce import-map `integrity`? [unverified] | Stage 4 onwards: section 4.3's design or the Preact 10.29.8 UMD fallback | Stage 2, before stage 4 starts |
| 2 | May a module worker in the Artifact import from the CDN hosts? [unverified] | The data worker; if not, its jobs run on the main thread in 8 ms slices | Stage 2 |
| 3 | Is KaTeX's MathML output in system maths fonts good enough on the iPhone, and does `TexSlots`' sentinel binding hold, with slot digits in the swapped `<mn>` matching the maths font? [unverified] | Stages 15, 23; a rejected look goes to the owner before stage 23 | Stage 2 |
| 4 | The `db` total size cap [unverified] | Stage 69: the checkpoint is built only if the cap is below 34 MB times the participants | Stage 2's paced probe (then deleted, with the owner's confirmation) |
| 5 | In the Artifact frame, the single list of `docs/PLAN.md` stage 2 (c): response compression, Web Locks, IndexedDB in a worker, `navigator.storage.estimate()`, **whether an external anchor opens from the frame (the handoff link every drill and live-code screen depends on; otherwise the copyable link)**, file input, inline `style` attributes through `innerHTML`, `version.json` caching despite a query string, version scoping after a republish, `location.reload()`, publishing without the page, `null` removals against 255 paths, the back gesture [unverified] | Stages 4, 69, 70, 83 | Stage 2 |
| 6 | Which locked files cdnjs serves byte-identically [unverified] | `cdn.lock.json` URLs (jsDelivr otherwise) | Stage 4 |
| 7 | Can the session platform's GitHub connection act as an identity separate from the owner's? **Closed, no** [measured, stage 1: it authenticates as the owner's account] | Merge rights are procedural (`CLAUDE.md` hard rule 3; `label-guard.yml` refuses other accounts; `docs/DECISIONS.md` B5) | Closed |
| 8 | The Playwright container tag for 1.63.0: **closed** [measured: `mcr.microsoft.com/playwright:v1.63.0-noble`, digest in `ARCHITECTURE.md` 3.2; `docs/DECISIONS.md` B11] | Visual CI | Closed |
| 9 | `zq/no-inner-html` and the two sinks: **closed** at stage 1 (`docs/DECISIONS.md` B3) | | Closed |
| 10 | Scene layer go or revert per family | Stages 27 to 58; more than one family failing stops the build for a re-plan | Stage 14 |
| 11 | `sys.monitoring` soft-deadline overhead in Pyodide; iPhone memory with pandas and scikit-learn in one worker [unverified] | Drill timeouts; which drills need a computer | Stage 25 |
| 12 | Cloudflare plan with SQLite-backed Durable Objects, the `new_sqlite_classes` key, the `@cloudflare/vitest-pool-workers` version, the proxy log retention setting [unverified] | The proxy limiter (decision 6 default: the paid plan if the free plan lacks them) | Stage 62 |
| 13 | Per-key or per-workspace spend limits for the eval key [unverified] | Eval caps | Stage 67 |
| 14 | Anthropic's API data policy for request content [unverified] | The proxy going live | Stage 82 |
| 15 | Exact capability declaration keys: `sample: {}` is accepted [measured, stage 2 publish]; `downloads` is `true` in contract 0.2.73 [sourced: the `artifact-capabilities` skill], where `ARCHITECTURE.md` 6.2.4 has `{}` (a conflict, `docs/DECISIONS.md` section 4) | The first live publish | Stage 83, against the `artifact-capabilities` skill |
| 16 | The owner's sign-off of draft 3's rounded hair | Bertie's visual baselines | Stage 59 |
| 17 | Cost of the paid marker and reviewer (decision 10) [unverified] | Content gates of curriculum Stage 1 (item 1.1 onwards) | By the first level gate of curriculum Stage 1 |
| 18 | The content licence | Any public release (none planned) | Before anything is public |
| 19 | Pyodide's `optimisation` group (cvxpy with Clarabel, highspy) in a browser [unverified] | 2.0b drills | When the 2.0b wave is briefed |
| 20 | Decision 13: **decided (b)** by the owner (D7): Cloudflare Pages behind an Access policy admitting only him. Still open: Access's free-plan terms [recalled, unverified] | Stages 25 and 82, the proxy's `ALLOWED_ORIGINS`, waiver W1's wording | Stage 25 checks the terms |
| 21 | Decision 14: **closed, (b)** by the owner (D8): exit part `3.3.zhou-ch5`, Zhou chapter 5 at 70% cold | The 3.3 exit data (pending edit 4) | Closed |
| 22 | The Stage 1 probe Artifacts: **closed**, both deleted by link with the owner's confirmation on 7 October 2026 (D6) | None | Closed |
| 23 | Which paid spines the learner is told to buy (`docs/CURRICULUM.md` 6.4 item 6: still open; the adopted items add Abbott, Süli and Mayers, Trefethen and Bau, Wilmott, Howison and Dewynne, Glasserman, Vanderbei and AFML) | Paid-book citation checks and course reports' warnings | The owner, before the first paid-book citation check (stage 84) |
| 24 | The 2.3 re-cut: `stage1-finance-projects.md` still lists the 24 lessons 2.2c moved or retired (`stage2-research-method.md` 0.6), so 2.3 is counted twice in the item file and retired lessons are still examined | `content/curriculum.yaml`, 2.3's papers and hours | Before stage 6 writes `curriculum.yaml` (the item file's revision 2 row already binds content agents to 2.2c's list) |
| 25 | GitHub Actions pinned by major tag (`actions/checkout@v5`, `setup-node@v5`, `setup-python@v6`, `setup-go@v6`; the tags resolve [measured: CI ran them on #11 and #12]); stage 1's sessions could not read those repositories to pin commit SHAs | Supply chain of CI | The first session that can read them; or the owner |
| 26 | `label-guard.yml` runs on `pull_request_target`: whether GitHub reads that workflow from the base or the default branch, and whether its check lands on the head commit as a required check [unverified]. Two known gaps (`docs/DECISIONS.md` G1): the head-commit binding uses the commit's earliest check suite anywhere in the repository, so a commit pushed elsewhere before the label predates it (fix: the earliest `pull_request` run for this pull request); and a later unrelated event turns the check green after a reset, so the visual job must read the label from the API | `visual-approved` enforcement | Stage 5, the first visual pull request |
| 27 | Branch protection or rulesets on a private repository may need a paid plan [recalled, unverified]; settings in `README.md` | Accident guards on `main` and `stage/*` | The owner |
| 28 | `ZQ_DEV_ROUTES` is read from the environment: the release procedure must check it is unset (`docs/DECISIONS.md` B9) | Development routes in a release build | Stage 83 |
| 29 | Python CI packages' licences (pillow MIT-CMU, typing_extensions PSF-2.0) are outside the npm licence gate | Licence allow-list coverage | Stage 25, when Pyodide's packages ship on the web app |
| 30 | `<link rel="icon" href="data:,">` on the web pages needs `img-src data:` in the stage 82 CSP, or the link goes | CSP violation reports | Stage 82 |

## Pending document edits

`docs/CURRICULUM.md` section 7's requests to other papers. Each is applied by the stage that owns it, or before the content it affects is briefed; the owning stage records it here as applied.

| # | Request (`docs/CURRICULUM.md` 7) | Status | Owning stage |
|---|---|---|---|
| 1 | `CONTENT-FORMAT.md` 3.1: 1 to 5 courses a topic | Applied (its tidy row) | |
| 2 | `CONTENT-FORMAT.md` 3.2: `Topic.exam` optional and track-scoped hours applied; **two papers for one topic** (1.5's `exm.prob.finals` and `exm.prob.continuous`) not yet | Partly applied | Stage 6 (content schema) |
| 3 | `CONTENT-FORMAT.md` 6.7: the curriculum drift check per track (3,390, 3,450, 3,450, 3,470) | Pending | Stage 7 (`zq check`) |
| 4 | `ASSESSMENT.md` 2.8 to 2.10, 8.9: data for nine papers and the Arena rounds; exit-part rows for `1.5.continuous`, `a1.exit`, `2.0a.exit`, `2.0b.exit`, `2.1b.exit`, `2.2c.exit`, `2.4.exit-core`, `2.4.exit`, `3.3.zhou-ch5`, `3.3.books`, `3.2.done`; A1 among the `human-mark` topics; plan data for `trk.ml-research` and the Stage 2 order | Pending | Stage 78 (exit parts), with the plan data at stage 79 |
| 5 | The compiler emits `docs/CURRICULUM.md`'s tables and fails on disagreement | Pending | Stage 23 (emit) |
| 6 | 239 new source ids; `src.vanderbei-lp-5e` as `basis`; the adopted and not-adopted proposals recorded. Applied to `content/sources.yaml`, not to `canon-gap.md`, which is history | Pending | Stage 84 seeds `sources.yaml` |
| 7 | Estimate-unit mapping in ten item files (0.3, 0.4, 0.5, 1.5, 1.6, 2.1, 2.2, 3.1, 3.2, 3.3) | Pending | Before each item's first course stage: 0.4 at 86, 0.5 at 87, 0.3 at 95; the rest before their first level gate |
| 8 | Stage 1 and Stage 2 exit tables in `stage1-dsa-cpp.md` 4.5 and `stage3-stochastic-interview.md` 4.5 | Pending | Stage 78, with request 4 |
| 9 | `stage1-finance-projects.md`: the 2.3 re-cut (open question 24) and the 2.0a applications | Pending | Before stage 6 writes `curriculum.yaml` |
| 10 | `stage2-ml-papers.md`: 2.0b recaps, 2.1b pointers, 2.2c recaps | Pending | Before the 2.1 wave is briefed |
| 11 | Pointers in `stage1-calculus.md`, `stage1-probability.md`, `stage1-statistics-ts.md`, `stage3-stochastic-interview.md` | Pending | Before each item's first level gate |
| 12 | `docs/PLAN.md` section 1 scope and section 12's build table | Applied (revision 2) | |
| 13 | `docs/AI-TUTOR.md`: `top.real-analysis` proof-heavy; the adopted items' Bertie rules | Applied (second review round: 2.5, 3.1, 2.12) | |

## Stage 1 record

**Pull requests into `stage/1`** (all merged by the session; smuddassirshah-cpu/zero-to-quant#4 closed as replaced by #6). Changed lines are additions plus deletions from `git diff --shortstat` of each merge. Review rounds count the adversarial review and each re-verification by the reviewing session.

| PR | Unit | Changed lines | Review rounds | Writing session, hours | Reviewing session, hours |
|---|---|---|---|---|---|
| #2 | Workspace, pins, TypeScript projects, Vite modes, empty app, formatter, stylelint, knip, lefthook, env examples, licence, `CODEOWNERS`, template | 6,181 (about 5,900 of them `package-lock.json`) | 2 | main session (part of 2.7) | 0.45 |
| #3 | `budgets.ts`, `page.ts`, `.size-limit.json` | 679 | 1, then the main session's own verification | 0.93 (with #5) | 0.22 (with #5) |
| #5 | Minimal `tools/artifact-host`, Playwright boot tests on three paths | 527 | 1, then the main session's own verification | with #3 | with #3 |
| #6 | `eslint-plugin-zq`: four rules, `noInlineConfig`, planted test | 1,197 (683 code and config) | 2 | 1.37 (with #7) | 0.47 (with #7) |
| #7 | `zq/layering` and the layer table, residual rule fixes | 816 | 2, then the main session's own verification | with #6 | with #6 |
| #8 | gitleaks tool, `.gitleaks.toml`, hooks that fail closed | 847 | 2 | 2.00 (with #9 to #11) | 0.56 (with #9 to #11) |
| #9 | `tools/py` with `uv.lock` | 863 (42 without the lock) | 2 | with #8 | with #8 |
| #10 | Licences, `npm audit`, `pip-audit`, waivers | 984 | 2 | with #8 | with #8 |
| #11 | `ci.yml`, `nightly.yml`, `label-guard.yml`, `VITE_*` check, last scan fixes | 891 | 3; CI green on its first run | with #8 | with #8 |
| #12 | Records: `docs/DECISIONS.md` B1 to B16, `ARCHITECTURE.md`, `README.md`, this file | see the pull request | 1 | main session | 0.15 |

**Measured effort** [measured from the session transcripts, first to last tool call, gaps over 15 minutes removed]: 8.8 session-hours to the stage report across the main session (2.7, which also integrated, verified and wrote the records) and eight sub-sessions, 1.5 AD against the plan's 5. Tokens: 0.24 million output and 0.34 billion input including cache reads; sub-session output counts look understated by the transcript format [unverified]. Pull requests did not record their own hours (`docs/DECISIONS.md` B14).

**Tree entries of `PLAN.md` 10 that later stages create**, correctly not built at stage 1: `cdn.lock.json`, `tools/cdn/` and `tools/release/provenance.ts` (stage 4); `content/` (stages 6 and 7); `.github/workflows/pages.yml` (stages 25 and 82); `proxy/` and `.github/workflows/proxy.yml` (stage 62); `releases/` and `tools/release/artifact-plan.ts` (stage 83); `docs/engine/` (stages 10b and 83). Stage 1 added files outside the trees, listed in `docs/DECISIONS.md` B16 for the owner.

**Owner actions waiting** (stage report): branch protection or rulesets (`README.md`; open question 27); decisions on A1, A2, L1, the pins of T1 and the tree additions of B16; the superseded and merged remote branches (`stage1/*`), which can be deleted once stage 1 reaches `main`.

## Next action

Stage 1 approved on 7 October 2026 (the owner: "Approved and continue"). The owner merges the Blueprint (smuddassirshah-cpu/zero-to-quant#1) and then the stage 1 pull request into `main`. Stage 2 (spike S1 on the owner's iPhone) is in progress on `stage/2`: the probe (https://claude.ai/artifact/KfYB1yPs9DfKTakjZZrGFD) and the `db` size probe (https://claude.ai/artifact/DF7mBFRaKCWkrXp14eRgXs) were published on 7 October 2026 and wait for the owner's run on the iPhone. When he says "S1 ready for republish", the session publishes v2 to the same URL and writes the signal (`spikes/s1/CONTRACT.md`, the runbook); after "S1 republish checks done" and his reload and back-gesture checks, it makes the omit-page publish, then reads the results from `ops/s1-run-*` and `status/s1-size`.
