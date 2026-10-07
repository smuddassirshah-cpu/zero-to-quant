# Zero to Quant Blueprint

> **Revision 2, 7 October 2026: the owner's decisions at Blueprint review.** These win over anything below that reads otherwise. What changed:
>
> 1. **Decisions recorded** (section 12): build order (a); the recommended curriculum additions adopted (P1 as item 2.2c, P2 inside 1.5, P3 as 2.0a, P4 as 2.0b, the O1 offset, 2.1b and A1), P5 to P16 not adopted, P8 among them; Bertie confirmed as drawn, with the hair redrawn as soft rounded tufts (`BERTIE.md` draft 3); every other decision at its stated default.
> 2. **The Artifact publishing rule** replaces decision 7 and fallbacks F1 and F2 (section 4.3): the Artifact publishes only files generated from this repository's own sources; third-party JavaScript loads from CDNs at exact versions through an import map; no Python, SQLite or KaTeX fonts in the Artifact; maths renders as MathML; every Python, SQL and C++ drill hands off to the web app. The web app keeps Pyodide with every load group, SQLite and KaTeX fonts. `tools/pysplit` and the JSON-part layout are removed; the measured Pyodide-in-Artifact run stays in `spikes/README.md` as a record.
> 3. **Scope** (section 1): 3,390 mapped hours on the trader track, 3,450 on the researcher and ML research tracks, 3,470 on the developer track; 25 items plus optional 3.2, 103 courses, 2,445 lessons (3.2's 5 courses and 104 lessons included).
> 4. **Build** (sections 3 to 10): the CDN lock and import map, the Artifact budget without Python (about 198 files and 125 MB a release), target differences, supply chain, failure rows, limitations and the repository tree.
> 5. **Stages** (section 11): spike S1 re-scoped; new stages 3g (`@zq/models/analysis`) and 51a (batch W5d, A1's six scenes); the adopted P0 modes added to their batches; Python stages web-only; effort and forecast re-estimated: about 880 AD before content, about 4,600 for the programme.
> 6. **Conflicts** 2, 8, 9 and 12 restated; 20 to 22 added.
> 7. **Appendices** edited to match: `ARCHITECTURE.md`, `CONTENT-FORMAT.md`, `ASSESSMENT.md`, `AI-TUTOR.md` and `spikes/README.md`. `CURRICULUM.md` (the index), `WIDGETS.md` and `BERTIE.md` were revised for the decisions before this pass. The four new item files (`stage1-real-analysis.md`, `stage2-deep-learning.md`, `stage2-numerics-optimisation.md`, `stage2-research-method.md`) were written under the decisions; the second review round (section 13) added a binding revision 2 header row for the publishing rule to the other eleven: `stage0-number-algebra.md`, `stage0-precalc-computing.md`, `stage1-calculus.md`, `stage1-dsa-cpp.md`, `stage1-finance-projects.md`, `stage1-linear-algebra.md`, `stage1-probability.md`, `stage1-python-tools.md`, `stage1-statistics-ts.md`, `stage2-ml-papers.md` and `stage3-stochastic-interview.md`.
> 8. **Second review round** (section 13): live-code lesson screens in the Artifact (4.3), the web host before a content licence (decision 13), the Zhou exit line (decision 14), the spike S1 list, provenance over generator modules, and one `TexSlots` binding path.
> 9. **Decisions 13 and 14 decided** by the owner at the Blueprint approval, 7 October 2026: (b) for both. The web app is served from Cloudflare Pages behind an Access policy admitting only the owner until a content licence exists; Zhou chapter 5 joins the Stage 3 exit at 70% cold as exit part `3.3.zhou-ch5` (section 12).

## 1. Scope and purpose

Zero to Quant is an interactive learning app that takes one adult from school arithmetic to quant-interview readiness, and towards the research habits of a machine-learning lab, along the owner's curriculum (`docs/curriculum.md` with the additions adopted on 7 October 2026: 3,390 mapped hours on the trader track, 3,450 on the researcher and ML research tracks and 3,470 on the developer track, in Stages 0 to 3, indexed in `docs/CURRICULUM.md` as 25 items plus optional 3.2, 103 courses and 2,445 lessons (3.2's 5 courses and 104 lessons included); with habits, review and holidays about 6.1 years at 15 hours a week, 6.2 on the researcher and ML research tracks, section 12). It teaches the way Brilliant does: short screens built around a diagram the learner manipulates, immediate diagnosed feedback, then spaced review, homework, timed papers and exit tests that gate each stage. Brainy Bertie, a minimal, stylised Einstein-style bobble head, is the mascot and the face of an AI tutor that tailors hints, explains again, marks long-form work against rubrics and reviews code, but never becomes the source of truth: every auto-graded numeric, symbolic and set answer, and every generator, is proved by two independent implementations in CI; code is graded by authored test suites that CI runs against a reference solution and known-wrong solutions; long-form work is marked against authored rubrics, and in a gate each rubric point counts the lower of the learner's and Bertie's marks. One TypeScript codebase builds two targets: a claude.ai Artifact for daily use on any device (the tutor runs on the viewer's own Claude account through the `sample` capability; progress syncs through the `db` capability) and a static, offline-capable web app (local, or a deployed static site that stays behind access control until the owner chooses a content licence, decision 13) whose tutor calls a small proxy holding the API key. The web app runs full Python for code drills (Pyodide 314.0.7 with NumPy, pandas, SciPy, statsmodels, scikit-learn and matplotlib, loaded per course), SQLite and, if its spike passes, C++. The Artifact publishes only files built from this repository's own sources (section 4.3), so it runs no Python, SQL or C++: those drills open the web app and return by result code, while lessons, whose authored code runs at build time, play fully on both. This document is the Stage 2 Phase 1 blueprint: it fixes every architectural decision, the build order (engine and widget library first, then content depth-first in curriculum order) and the definition of done of each review gate.

### Non-goals

- No server, accounts or database of our own. The tutor proxy is the only server and holds no learner data.
- One learner in this phase: the owner. The friends board is P2; admitting other learners or a public release reclassifies the project as Class D (section 7) and is out of scope. No deployed build is world-readable before the owner chooses a content licence (decision 13).
- No generated content on the main path: hints, answers, items and explanations that the app grades or stores are authored and verified; Bertie works on top of them and can be switched off without losing a lesson.
- No AI marking that raises a mark: the learner marks each rubric point first, Bertie's draft appears after, and a gate counts the lower of the two per point (section 6.5). Decision 10 (section 12) adds a person who marks one finals-style sitting per Stage 1 maths topic.
- No offline mode in the Artifact: the host has no service workers.
- No third-party file published to the Artifact: no Python, SQLite, compiler or font files there; third-party JavaScript comes from CDNs (section 4.3).
- No native or app-store builds; the web app is an installable PWA.
- No telemetry, analytics or remote error reporting on either target.
- No code leaves the device to run: no Compiler Explorer, no remote Python. C++ runs in-browser on the web app only if the 1.9 spike passes, otherwise on the learner's own machine with pasted output.
- No PyTorch, JAX or GPU training (not in Pyodide).
- No leagues, simulated rivals, monetisation or real-money trading features.
- No widget for a lesson that does not exist: P1 and P2 widgets wait for their content, and `vim-sim` is dropped.
- No in-app content editor: content lives in the repository and is reviewed as diffs.

### Documents and authority

This plan wins wherever it differs from an appendix. Each appendix owns its domain and wins over the working papers in `docs/blueprint/work/`, which are history.

| File | Owns |
|---|---|
| `docs/ARCHITECTURE.md` | Stack, module tree, every TypeScript contract, builds, versioning, testing, budgets, developer workflow (section numbers stable) |
| `docs/WIDGETS.md` | Every widget id, tier, cluster, priority, size, first use and composition; the catalogue sections it names own each widget's behaviour |
| `docs/CONTENT-FORMAT.md` | Content format, schema, ids and migrations, generators, verification, graders, compile step, authoring workflow |
| `docs/AI-TUTOR.md` | Bertie's modes, prompt, context assembly, page actions, both backends, the proxy, guardrails, evals |
| `docs/ASSESSMENT.md` | Assessment ladder, exam engine, skill graph, mastery and scheduling, planner, motivation, the progress data model, privacy |
| `docs/BERTIE.md` with `prototype/bertie.html` | The mascot's art, rig, motion, states and API |
| `docs/CURRICULUM.md` with `docs/curriculum/*.md` | The curriculum index and the fifteen item files: courses, levels, lessons, homework, papers, reading |
| `docs/blueprint/work/canon-gap.md` | The proposed curriculum additions; the owner's decisions on them are section 12 decision 2 and `docs/CURRICULUM.md` 6 |
| `spikes/README.md` | Measured platform results |
| The owner's skills | lesson-creator and maths-teaching are encoded as compiler-checked rules in the authoring checklist (`CONTENT-FORMAT.md` 9.3) and in Bertie's teaching rules (`AI-TUTOR.md` 3.1); code-craft is the format of Bertie's code reviews and of `code-annotator`; project-forge is this plan's process and the method the 2.3 project lessons teach |

### Terms used in this plan

| Term | Meaning |
|---|---|
| Gate, stage | One owner review of a coherent deliverable; section 11 numbers them 1 to 100, with lettered stages (3a to 3g, 9a, 10a, 10b, 51a, 74a, 74b) inserted so that no cited number moves; 68 is kept empty |
| Stage branch | `stage/<n>`: every pull request of a stage merges there; the branch reaches `main` only when the owner approves the gate (section 11.1) |
| Level gate | The content gate: one level (4 to 7 lessons, its bank, level review and homework set), about 6 AD; a course is a release milestone made of level gates |
| Release ledger | `releases/<release>.json`, committed in the release pull request: every published path with its SHA-256 and size, the page hash and the manifest name (section 8.6) |
| Preview Artifact | The one long-lived private Artifact the sessions republish for every device gate; the owner records results in its `db` at `ops/gate-<stage>` |
| P0, P1, P2 | Widget priority by first use: items 0.1 to 1.5 with A1, then 1.6 to 1.9, then Stages 2 and 3 (`WIDGETS.md` 1.5) |
| Primitive, input | Hand-written building blocks with their own views (37) |
| Scene | A composite written as data over primitives plus a pure model, with no view of its own (section 3.2) |
| Bespoke composite | A composite with its own view, kept for interactions no primitive offers (22 at P0) |
| Preset | Compile-time configuration over a base widget (24) |
| Cluster | One of 26 lazy code chunks that group widgets by topic |
| Load group | A set of Python packages that load together on the web app (`stdlib`, `numpy-pandas`, `scipy-statsmodels`, `sklearn`, `matplotlib`, `testing`, and `optimisation` from 2.0b) |
| Sealed screen | An unresolved lesson or explore screen, on which Bertie holds the answer key behind the leak probe |
| Fold | The deterministic function from the event log to derived progress state |
| AD | Agent-day: 6 hours of agent session time on a stage, measured from the session logs (first to last tool call, gaps over 15 minutes removed), including the self-review and the adversarial and semantic review sessions, excluding the owner's time. Every pull request records its session hours and tokens in its description; one session delivers about 5 AD a week [our estimate, measured from stage 1] |

### Conflicts resolved here

| # | Conflict | Decision | Rejected | Reason | Changed in |
|---|---|---|---|---|---|
| 1 | Widget scale: `ARCHITECTURE.md` decision 7 assumed about 100 widgets; `WIDGETS.md` decision 16 lists 338 ids (192 at P0) with 277 composites each owning a view (draft 1: 314 ids, 186 at P0, 254 composites), and its decision 4 rejects a declarative scene engine | **A fifth tier, `scene`**: a composite written as data over primitives plus a pure, tested model function, turned into an ordinary widget module by the engine. About 131 of the 153 P0 composites become scenes; 22 stay hand-written (section 3.2) | Every composite with its own view; a dataflow language inside content | Halves P0 widget effort (about 240 AD against about 480, section 3.2) and removes 131 copies of pointer and render code; `WIDGETS.md`'s objection was to logic in content, and scenes keep logic in typed library code | `ARCHITECTURE.md` decisions 7 and 36, 4.2, 4.5, 5.3, 5.14; `WIDGETS.md` 0.1 |
| 2 | Python runtime: catalogues and early papers planned MicroPython in the Artifact; draft 1 of this plan shipped Pyodide there as JSON parts of wheel members, and the appendices run NumPy and pandas drills in the Artifact | **Pyodide 314.0.7 on the web app only; no Python in the Artifact** (the owner's publishing rule, 7 October 2026, section 4.3): every Python, SQL and C++ item in the Artifact hands off to the web app and returns by result code; load groups ship per course on the web (section 5.7) | MicroPython with `ulab` in the Artifact; Pyodide in the Artifact as JSON parts (measured working on the owner's iPhone, `spikes/README.md`) | Both publish third-party binaries, which the rule forbids; one Python target means one grader and one set of tracebacks | `ARCHITECTURE.md` decisions 15, 16, 6.3; `CONTENT-FORMAT.md` decision 18, 6.11, 7.6; `ASSESSMENT.md` decision 30, 2.9, 3.3, 14.3; `AI-TUTOR.md` decision 26 (each in its revision 2 note) |
| 3 | Build order: `ARCHITECTURE.md` 13 and `WIDGETS.md` 7 run widget waves beside engine stages and start content at the first vertical slice | **Engine and every P0 widget batch before content** (the owner's instruction), with two dependency-driven moves: the Python runtime precedes the widget batches (`code-cell` is first used at 0.1 lesson 42, and most of the 1.1 and 1.2 widgets run code), and generators follow the graders | Interleaving content with engine work | The owner's priority; the reorder avoids building the code widgets against a fake runtime and re-testing them | Section 11; `ARCHITECTURE.md` 13 note |
| 4 | Stage numbers: `CONTENT-FORMAT.md` 14 (C7) and `AI-TUTOR.md` 12 item 16 cite "stage 22" for the Python worker; `AI-TUTOR.md` maps T0 to T8 to "stages 24 to 31" | Python worker is **stage 25**; T0 to T8 are **stages 60 to 67** | | Section 11 numbering | `CONTENT-FORMAT.md`, `AI-TUTOR.md` |
| 5 | `ASSESSMENT.md` 2.9 (`1.2.exit`), 11.6 and 15.2 call GitHub's and Codeforces' public APIs from the web app; `ARCHITECTURE.md` 6.4.2's CSP allows only the app's origin and the proxy | **No third-party API calls.** Paste-verify (`git log`, `git status`, `pytest -q`) and manual contest entries on both targets; `connect-src` stays `'self'` plus the proxy | Adding `api.github.com` and `codeforces.com` to `connect-src` | The CSP's single outbound channel is the guarantee that an injected script cannot send the tutor token anywhere useful (`AI-TUTOR.md` 8.8); paste-verify already proves what the exit asks; the two targets stay identical | `ASSESSMENT.md` 2.9, 11.6, 15.2 |
| 6 | `CONTENT-FORMAT.md` 3.10 puts the candidate-answer extractor in `@zq/graders` (`leak.ts`); `AI-TUTOR.md` 11.1 puts the leak probe in `src/tutor/reply/leakprobe.ts` | Both: `packages/graders/src/leak.ts` extracts candidates and grades them with the screen's check; the compiler's tutor-field lint and Bertie's probe both call it; `leakprobe.ts` adds streaming, the "already visible" exemption and the withheld flow | Two extractors | One extractor means the lint and the probe accept exactly the same leaks | Section 3.1 |
| 7 | `WIDGETS.md` 3 requires `dmath` in `@zq/mathcore` from the first engine stage; `ARCHITECTURE.md` 4.3 omitted it | `dmath` is in `@zq/mathcore`, built in stage 3 | | Seeded numbers shown or graded must not depend on each engine's `Math.exp` | `ARCHITECTURE.md` 4.3 |
| 8 | `CONTENT-FORMAT.md` 13 item 2 quotes a first Python load of 13 MB or 49 MB; `ARCHITECTURE.md` 6.3.3 measured 24 MB for NumPy and pandas in the JSON-part layout | The web app's figure: 21 MB of files for the core, the standard library, NumPy and pandas in Pyodide's native layout (`ARCHITECTURE.md` 6.4.1); the Artifact downloads no Python | | Measured on the release tarball; the JSON-part layout is not built | `CONTENT-FORMAT.md` 13 |
| 9 | Stage 0 needs NumPy and matplotlib for 0.3's Precalc Lab part 3 (`stage0-precalc-computing.md` decision 9), while draft 1 let only `stdlib` and `numpy-pandas` gate stage 25 | Settled by the publishing rule: every Stage 0 drill, the lab part included, runs on the web app, which ships every group. Stage 25 passes when `stdlib` and `numpy-pandas` meet their timing and memory on the owner's iPhone in the web app; every other group is measured and recorded there | Making `matplotlib` a pass condition of stage 25 | One code target, so no group decides where a drill runs | Section 5.7; `ARCHITECTURE.md` 13 E8 |
| 10 | KaTeX trust: `ARCHITECTURE.md` 11.3 allows `\htmlData` through a `trust` callback; `AI-TUTOR.md` 8.8 sets `trust: false` | Not a conflict: authored content renders with the narrow callback (`\htmlData` with a checked name only); Bertie's replies render with `trust: false`. Two configurations of one sink. `TexSlots` binds slots by sentinel `\text{}` tokens on both outputs, one path (second review round): on the web it binds the HTML span's text node and the hidden MathML copy; in the MathML tree it swaps each sentinel `<mtext>` for an `<mn>` built with `createElementNS`, so live digits render in the maths font and screen readers hear the current value | `\htmlData` placeholders on the web and sentinels in the Artifact, two binding paths | Model output gets the narrower setting; one binding path is one set of tests, and the hidden MathML copy no longer holds a stale placeholder | Section 6.5; `ARCHITECTURE.md` decision 37, 5.11, 11.3 |
| 11 | `BERTIE.md` 12.1 lists `src/ui/bertie/markup.ts` (the `DOMParser` template); `ARCHITECTURE.md` 4.2 omits it | Included | | `BERTIE.md` decision 19 needs it | `ARCHITECTURE.md` 4.2 |
| 12 | `CONTENT-FORMAT.md` C11 accepts the engine on the 1.5 reference lesson with a complete first level; depth-first content starts at 0.1; decision 7 cited "a reference homework with a drill" | Acceptance (stage 84) runs the reference lesson `lsn.cond.shrinking-sample-space` (already authored) and the whole of level W1 of `crs.numwork`: its 5 lessons from `lsn.numwork.digit-worth`, bank, level review and homework set `set.numwork.place-value` with drill `drl.num.divmod-check`. The rest of 1.5 level H1 is not authored ahead of depth-first order | The reference lesson's whole level; two lessons only | The reference lesson is already verified end to end; level W1 proves the Stage 0 widgets, a level gate and a Python drill handed from the Artifact to the web app and back by result code on the phone | Section 11.6; `CONTENT-FORMAT.md` 14 C11 |
| 13 | `AI-TUTOR.md` 6.3.7 says the Node proxy relies on "Node 20" globals; the toolchain pins Node 22.22.0 | Node 22.22.0 everywhere | | One runtime in CI and locally | `AI-TUTOR.md` 6.3.7 |
| 14 | `ASSESSMENT.md` 10.3 serves recreated Mosteller and Zhou problems warm in Stages 1 and 2; `stage1-probability.md` decision 13 and `stage3-stochastic-interview.md` decision 8 hold them back for the cold 3.3 exit | **The weekly bank serves `original` problems only before 3.3**; every recreated problem names the book problem it imitates, and CI keeps imitations of Zhou chapters 4 and 5 and of any Mosteller, Crack or Joshi problem out of every pool before 3.3; a recognised book problem is logged "seen" and leaves both numerator and denominator | Counting "recognised and re-solved" as cold | Recall of a solution met with hints is not cold solving, and the 3.3 exit is the main measure of interview readiness | `ASSESSMENT.md` 10.3, 10.5, 11.9; both item files |
| 15 | `ASSESSMENT.md` decision 17 says warm weekly problems get "Bertie after grading"; its 10.4 and `AI-TUTOR.md` 2.2 say "after the first Check" | **After grading**; and from 1.5 one weekly problem in three is cold, from Stage 2 two in three | "After the first Check" | Support should fade towards the cold interview | `ASSESSMENT.md` 10.4; `AI-TUTOR.md` 2.2 |
| 16 | `ARCHITECTURE.md` 8.1 baselines every storyboard state; `CONTENT-FORMAT.md` 9.2 attaches storyboards to pull requests | **Baselines for widget fixture states and app screens only**, kept on an orphan `visual-baselines` branch with a count and size budget; lesson storyboards are pull request artefacts | Committed baselines for 2,148 lessons | Tens of thousands of images and several GB of history; every content pull request would need a visual approval | `ARCHITECTURE.md` 8.1, 8.3 |
| 17 | Section 11.6 asked for exact checked citation locations; `CONTENT-FORMAT.md` 9.3 rule 27 lists unchecked ones as warnings | **Rule 27, sharpened**: `loc` on every citation; free sources checked by fetching during authoring; paid books checked when the owner reads that section; unchecked ones listed in the course report | Exact checked locations for about 506 source ids (draft 1: about 398 works) at every course gate | Only a person holding a paid book can check it, and no stage, time or book access was planned for that | Section 11.6; `CONTENT-FORMAT.md` 9.4 |
| 18 | `ASSESSMENT.md` 4.1 sized the mastery model at 1 or 2 skills a lesson; `CONTENT-FORMAT.md` allows 4 and every sample lesson introduces 3 or 4 | **Skills at level grain**: an examinable method, 3 to 8 per level, about 1,500 on the path (about 1,700 after revision 2, section 5.5); `Lesson.introduces` at most 2; finer distinctions become step tags with no card; CI budgets cards per topic | 3 or 4 skills a lesson (about 7,600 skills) | At that count maintenance alone is about 1,140 hours over the path, 9 hours a week late in it [simulated, section 12], and each skill gets 5 or 6 pieces of evidence | `ASSESSMENT.md` 4.1, 6.5; `CONTENT-FORMAT.md` 3.2; the header note of `CURRICULUM.md` |
| 19 | Section 4.1 set CPython 3.11 as the CI floor; the soft deadline needs `sys.monitoring` (3.12); SciPy 1.18.0, Pyodide's version, requires Python 3.12 or later [measured with `uv pip compile`, 7 October 2026] | **CPython 3.12 is the floor**; `tools/py/uv.lock` pins the CI packages to Pyodide's versions (section 4.2) | A 3.11 floor with a second timeout mechanism | One timeout mechanism, and the floor can install the versions the drills are written against | `ARCHITECTURE.md` decision 31; `CONTENT-FORMAT.md` 6.11 |
| 20 | `ARCHITECTURE.md` decision 24 bundles every dependency into the Artifact's own files, which the publishing rule forbids | **Third-party JavaScript loads from CDNs at exact versions in the Artifact**, through an import map written from `cdn.lock.json` (section 4.3); the web app keeps bundling everything | Bundling into Artifact files; jsDelivr's `+esm` builds, which resolve dependency ranges on the CDN, so a peer such as `preact` would not be ours to pin | The rule; one locked list of versions for both targets | `ARCHITECTURE.md` decisions 8, 24, 37; 6.1, 6.2 |
| 21 | KaTeX's and MathLive's font files can no longer be published, and the Artifact loads fonts only from Google Fonts | **MathML in the Artifact**: KaTeX from the CDN with `output: 'mathml'` in system maths fonts; MathLive web only; the Artifact's expression input is the plain field with the symbol bar and a live MathML preview, graded by the same parser | MathML emitted at build time; MathLive without its fonts | Generated items, live formulas and Bertie's replies need run-time rendering anyway, so build-time MathML would be a second path; MathLive lays out with KaTeX's font metrics [recalled] | `ARCHITECTURE.md` decision 37, 5.11, 11.6; `AI-TUTOR.md` 7.3, 8.8 |
| 22 | `WIDGETS.md` decision 18 and 7.3 called A1's wave "W5b", which is stage 50's batch label in section 11.4 | **A1's batch is W5d, stage 51a.** Resolved in the source by the second review round: `WIDGETS.md` now says W5d everywhere | Renaming stage 50's batch | No cited batch label moves | Sections 3.2, 11.4; `WIDGETS.md` decision 18, 0.3, 7.3 |

---

## 2. Signal

Zero to Quant shows that its author builds correctness-critical software the way a desk builds a pricing library: every auto-graded number has two independent implementations (TypeScript generators checked exhaustively over their parameter boxes against Python verifiers), code drills are graded by test suites that CI proves against reference and known-wrong solutions, randomness is counter-based and bit-identical across browser engines, learner state is an event log whose fold is property-tested for determinism and order independence, an LLM sits behind a deterministic answer-leak probe and a regression eval gate, and the one endpoint that holds a secret is built to a stated threat model.

Draft CV bullet: *Built Zero to Quant, a TypeScript and Python learning platform with two deployment targets, a 338-widget interactive library and an AI tutor; every auto-graded numeric, symbolic and set answer and every item generator is proved by two independent implementations in CI, progress is event-sourced with a property-tested deterministic fold, and the tutor is gated by an answer-leak probe and an eval suite on both deployment targets.*

---

## 3. Component tree

### 3.1 Tree

Leaf paths follow `ARCHITECTURE.md` 4, which lists every file; this tree names each component and its responsibility. Section 10 is the full repository layout.

```
zero-to-quant
├── content/                 [YAML, ZQ Markdown, TypeScript, Python]  the curriculum as data (CONTENT-FORMAT 2.5)
│   ├── <topic>/<course>/<level>/<lesson>.yaml   one lesson per file: screens, checks, diagnoses, quiz, tutor fields
│   ├── <topic>/library/                         skills, misconceptions, items, sets, exams, drills, glossary, cards
│   ├── generators/<topic>/<gen>.ts|.yaml|.verify.py   on-device generator, its parameter box, its independent Python twin
│   └── curriculum.yaml  plan.yaml  sources.yaml  migrations.yaml  ids.lock.json   hierarchy, tracks, canon, data migrations, answer hashes
├── packages/                [TypeScript, no DOM; Node-safe]
│   ├── contracts/                  types only: ids, Answer, Grade, widget, scene and platform contracts, events, RPC messages
│   ├── mathcore/                   Philox4x32-10 (O(1) addressable draws), hash32, BigInt rationals, en-GB number parsing,
│   │                               expression compiler (no eval), dmath (stage 3); linalg, quad, ode, roots, units (3a); stats-core (3b)
│   ├── models/                     pure domain models by entry point: data (3c), code with vfs and shell (3d), algo (3e), git (3f),
│   │                               analysis (3g, for A1); markets, ml, numerics, optim and research with their P1 and P2 waves;
│   │                               every model feeding a shown or graded number has a parity test
│   ├── content-schema/             zod 4 schemas, inferred types, JSON Schema export for editors
│   ├── content-compiler/           compile(project, {registry}): parse, merge, resolve references, lint, emit bundles
│   ├── graders/                    pure graders per check kind, predicate registry, accepted-answer rule, leak.ts
│   │                               (candidate-answer extractor shared by the tutor-field lint and Bertie's probe)
│   ├── gen-kit/                    defineGenerator, admissible index, exam reserve, phrasebooks
│   └── eslint-plugin-zq/           determinism, raw timers, raw pointers, state in render, innerHTML, colours, copy, layering
├── src/                     [TypeScript, TSX on Preact 11, CSS Modules]  the app, both targets
│   ├── entries/                    web.tsx, artifact.tsx, dev.tsx: boot with the right Platform
│   ├── app/                        boot order, typed hash router, build config and flags, ring-buffer log, shell, signal stores
│   ├── platform/                   the only target-specific code (ARCHITECTURE 5.9)
│   │   ├── web/                    IdbStore, Blob downloads and file input, service worker client, identity
│   │   ├── artifact/               claude.use discovery and absence, DbStore on db with IdbStore mirror, downloads, identity,
│   │   │                           cdn.ts (awaits the CDN modules at boot, maps failures to codes, Retry)
│   │   ├── shared/                 IndexedDB, KeyValue (tutor token in IndexedDB only), BlobCache (LRU, 300 MB or 60% of quota),
│   │   │                           clock, Web Audio tones, Web Locks writer election with heartbeat fallback, MemoryStore
│   │   └── fake/                   FakePlatform: scripted tutor, MemoryStore, FakeClock, fixed seeds (tests, gallery, storyboards)
│   ├── engine/
│   │   ├── scope.ts                owns every timer, frame, listener and abort; disposed on leave, Try again and Start over
│   │   ├── rpc.ts                  typed worker RPC with transferables and cancellation
│   │   ├── content/                manifest, loader, bundle cache, Prose token lists, templates, generator runtime
│   │   ├── widgets/                WidgetHost (lifecycle written once), WidgetApi, overlay, show-why runner, preview guard,
│   │   │                           describe aggregation for the tutor, drafts and state migration
│   │   ├── interaction/            useDrag (one update per frame), roving focus, lift-and-drop, key map, exact-value editor
│   │   ├── motion/                 spring integrator (1/240 s substeps, sleeps at rest), tweens, Web Animations, motion modes
│   │   ├── render/                 Svg, memoised Layer, CanvasLayer, Tex (raw-HTML sink S1), TexSlots, scales, en-GB format
│   │   ├── player/                 machine.ts: step(state, event) -> [state, effects], pure; effect runner; player views
│   │   ├── items/                  ItemRunner: quiz, practice, review, redo, homework, exam, placement through policies
│   │   ├── progress/               event envelope, AppendQueue (the only seq assigner), fold, points rules, snapshots,
│   │   │                           outbox, leases, export, import, result codes, active time
│   │   ├── schedule/               FSRS-6 cards by band, retention tiers, Redo queue, review composer
│   │   ├── assess/                 homework, exam engine, placement, exit parts
│   │   └── python/ sql/ cas/       PythonRuntime and SqlRuntime (web; handoff stubs in the Artifact); lazy parser; MathLive (web)
│   ├── widgets/                    the library (WIDGETS.md)
│   │   ├── primitives/ inputs/     37 hand-written building blocks: pure logic.ts, schema.ts, View.tsx, fixtures, tests
│   │   ├── scene/                  the scene layer: defineScene, typed binding paths, SceneView, layout containers (3.2)
│   │   ├── scenes/<cluster>/       about 220 scenes (P0 131): scene.ts (pure data and functions), schema.ts, fixtures
│   │   ├── composites/<cluster>/   about 50 bespoke composites (P0 22), same folder shape as primitives
│   │   ├── presets/<cluster>/      24 presets: compile-time configuration over a base widget
│   │   └── *.gen.ts, clusters/     generated registries and the 26 lazy cluster entries; CI checks they are current
│   ├── workers/           [TypeScript; Python for grader.py, zqtest.py, trace.py]
│   │                               data.worker (classic zod validation, fold rebuilds, search, export, import), both targets;
│   │                               python.worker (Pyodide, the grader) and sql.worker (SQLite), web only
│   ├── screens/                    one folder per screen (ARCHITECTURE 5.8) plus development routes
│   ├── tutor/                      Bertie's brain (AI-TUTOR 11.1): gate, paste guard, context, prompt, renderers, backends,
│   │                               reply pipeline (act line, leak probe, code guard, lint, Markdown to DOM), tools, UI, evals
│   ├── ui/                         design system components, Keypad, SymbolBar, course art
│   │   └── bertie/                 geometry, poses, markup (DOMParser), controller, Preact wrapper; at most 12,000 bytes gzipped
│   ├── sw/sw.ts                    web service worker (Workbox injectManifest), web build only
│   └── styles/                     tokens.css (light and dark), base, font faces per target; KaTeX CSS (web), math.css for MathML (Artifact)
├── proxy/                   [TypeScript]  tutor proxy: one handler, Cloudflare Worker and Node 22 entries
│   ├── handler.ts                  auth, CORS, validation, prompt rendering, upstream stream, event mapping, counting
│   ├── limits.ts                   per-token rate and spend limits (Durable Object, or in memory for Node)
│   ├── sign.ts                     HMAC-SHA-256 signing of chat call blocks
│   └── prices.ts  events.ts        price table and spend; Anthropic stream to our event stream
└── tools/                   [TypeScript via tsx; Python]
    ├── zq/                         content CLI (check, verify, build, preview, fmt); builds CompilerRegistry
    ├── zqverify/          [Python 3.12]  independent verifier: whitelisted ast evaluator, SymPy, NumPy, Monte Carlo, sandbox
    ├── pyvendor/                   fetch the pinned Pyodide release and the hypothesis wheel (SHA-256 against the locks), web build only
    ├── cdn/                        write cdn.lock.json (exact-version URL, SHA-384, import kind) from package-lock.json; nightly drift check
    ├── release/                    Artifact publish planner, release ledger and resume, page fragment and import map writer,
    │                               provenance check (no node_modules input in any published JavaScript file), file and size budgets
    ├── artifact-host/              local emulator: served-type allow-list, CSP, sandboxed frame, fake window.claude
    └── perf/ scaffold/ registry/   frame-time harness; new:widget, new:scene, new:screen; registry generator
```

**The tutor is built in from the start.** Its hooks (`describe`, `targets`, `secret`, `tryable`, `tryValue`, ghost previews) are part of the widget contract from stage 10a and every widget's contract suite tests them; the content compiler emits tutor context from stage 23; the service, both backends and Bertie (stages 59 to 67) land before any content stage, so no lesson ever ships without them. Authored hints, Why text and Show solution work with the tutor off.

Load-bearing commitments, each tested in its stage: Check to verdict within 150 ms for non-code checks; drag script per frame at most 4 ms (primitive) and 8 ms (composite or scene) at P95 on the CI proxy; a single event folds within 2 ms on the main thread and a full rebuild of the synthetic learner over the whole path (about 121,000 events for 2,445 lessons, scaled from `ASSESSMENT.md` 13.6's 106,000 for 2,148 [our estimate]) within 3 s in the data worker on the owner's iPhone; the paste guard is $O(n)$ in the message length; an idle screen requests zero animation frames.

### 3.2 The widget library at scale: scenes

**The problem.** `WIDGETS.md` merges six catalogues and the adopted items' four curriculum files into 338 ids: 29 primitives, 8 inputs, 277 composites and 24 presets, 192 of them P0 (draft 1: 314 ids, 186 P0). Its composite rule (decision 3) already keeps composites from drawing or handling gestures themselves, but each composite still owns a view, a state derivation, keyboard wiring, `describe`, `targets`, a table view and tests. At the sizes `WIDGETS.md` assigns, the 153 P0 composites alone would cost about 480 agent-days as hand-written modules (section 11.2), and the Stage 1 prototype showed where defects live: in repeated machinery, not in the maths.

**The decision.** A fifth widget tier, `scene`, in the spirit of Brilliant's in-house declarative diagram framework, Diagrammar [recalled, unverified]: a composite is written as a typed data description of primitive layers, a pure model function that derives everything shown, and bindings between them. `defineScene` turns that description into ordinary widget logic, and the generated cluster entry pairs it with the generic `SceneView`, so the host, the compiler, the tutor, the contract suite and content cannot tell a scene from a hand-written composite. The full contract is `ARCHITECTURE.md` 5.14; in outline:

```ts
// src/widgets/scenes/precalc/unit-circle/scene.ts: pure, imported by the app, the compiler and CI
export default defineScene({
  type: 'unit-circle', v: 1, cluster: 'precalc', answers: ['point', 'numeric'], stateVersion: 1,
  prepare: (c) => ({ circle: circlePath(c.view) }),          // once per config
  init: (c) => ({ a: { theta: c.start }, v: { showLegs: false } }),
  derive: (c, k, s) => unitCircle(s.a.theta, c.units),       // @zq/models: point, sine, cosine, arc; Python parity-tested
  layout: plot2d('plane', { view: 'c.view', aspect: 'equal' }, [
    marks('circle', 'param-curve', { data: 'k.circle' }),     // binds only c and k: static, memoised automatically
    marks('arc', 'angle', { data: 'd.arc', table: true }),
    marks('legs', 'segment', { data: 'd.legs', visibleWhen: 'v.showLegs' }),
    dragPoint('p', { at: 'd.point', writes: { path: 'a.theta', from: angleOf }, constraint: 'on-circle', answer: true }),
    liveFormula('read', { tex: '\\sin\\theta = \\slot{s}', slots: { s: 'd.sinText' } }),
  ]),
  answer: (c, s, d) => ({ kind: 'point', x: d.point.x, y: d.point.y }),
  describe: { brief: 'Unit circle, angle {d.thetaText}; point ({d.cosText}, {d.sinText}).' },
});
```

**What the engine generates** from a scene: `init`, `answer`, `dirty` (answer state differs from `init`), `answerObjects` (nodes marked as answers), `staticTargets` and `targets` (each node contributes its primitive's targets under its id), `describe` (the scene's template plus each node's phrase), `table` (marks with `table: true`), `tryable` and `tryValue` (controls marked `tryable`), `summarise` (the control's label and new value), `exports` (declared `d.*` paths) and declarative show-why recipes over `v.*` paths. Any member may be overridden with a pure function. The view is the generic `SceneView`: it renders the layout tree with the primitives' controlled components, binds every property as a computed signal over (config, state, derived), runs `derive` once per state change, and wraps every node whose bindings read only `c.*` and `k.*` in a memoised layer, so the render discipline of `ARCHITECTURE.md` 2.5 holds by construction instead of by lint.

**Rules.**

1. **Scenes are library code.** Content never contains a binding, a function or a dataflow; it configures a scene through the scene's zod config schema exactly as it configures any widget. This is the answer to `WIDGETS.md` decision 4, whose objection was to an expression language inside content that the verifier would have to check like code. Bindings are typed paths (`c.*` config, `k.*` constants prepared once per config, `a.*` answer state, `v.*` view state, `d.*` derived values) checked by the TypeScript compiler through template-literal path types; transforms are named pure functions in the scene file.
2. **Every number comes from `derive`.** `derive` calls `@zq/models` or `@zq/mathcore`; each function feeding a shown or graded number has unit tests, property tests and a Python parity test (`WIDGETS.md` 7.5).
3. **Scene by default.** A new composite is a scene unless one of five reasons holds, stated in its pull request: free text or code editing beyond the inputs; a clock-driven loop (speed runs, typing); a service with its own state machine (virtual shell, git model, algorithm stepping, exchange simulator, interview engine); a gesture no primitive offers; or a measured failure of its scene version against the frame budget.
4. **Size cap.** A `scene.ts` above 400 lines, or one needing more than three overridden members, becomes bespoke by rule.
5. **Embedding.** An `embed` node renders another scene, or a bespoke composite's controlled component, bound to a sub-path of the state; a screen widget is still one host with one state.

**Classification at P0.** Bespoke (22, sizes from `WIDGETS.md`): `code-cell` L, `graph-explorer` L, `equation-workbench` L, `shell-sim` L, `geometry-board` L, `code-tracer` L, `algo-lab` L, `git-graph` L, `mutant-hunter` L, `elimination-lab` L, `puzzle-workbench` L, `game-lab` L, `speed-drill` M, `typing-trainer` M, `strategy-trainer` M, `workspace-sim` M, `regex-lab` M, `bench-lab` M, `plot-workbench` M, `merge-conflict` M, `code-review` M, `injection-lab` M. Every other P0 composite (131: 25 S, 98 M, 8 L, A1's six included) is a scene; the 9 P0 presets stay presets; the 30 P0 primitives and inputs are hand-written as before. The adopted items' 23 new composites are all scenes and `scaling-plot` is a preset (`WIDGETS.md` decision 17). Among P1 and P2, about 28 more are expected to be bespoke (the market simulators, `problem-workbench`, `contest-arena`, `mock-interview`, `mm-game`, `viva`, `backtest-lab`, `paper-trader`, `feed-sim` and similar), classified by rule 3 when their wave is briefed.

By build batch (section 11.4):

| Wave (stages) | Serves | Scenes | Bespoke | Presets |
|---|---|---|---|---|
| Stage 14 pilots and stage 24 | the reference lesson, 0.1, 0.3, 1.4 | 5 | 0 | 0 |
| W1 (27 to 32) | 0.1 with 0.4 and 0.5 from week 1 | 14 | 5 | 2 |
| W2 (33 to 35) | 0.2 | 10 | 2 | 1 |
| W3 (36 to 41) | 0.3, with five 1.3 and 1.4 bases pulled forward | 20 | 4 | 3 |
| W4 (42 to 48) | 1.1 and 1.2 | 19 | 9 | 3 |
| W5 (49 to 51) | 1.3 | 24 | 0 | 0 |
| W5d (51a; conflict 22) | A1 Real analysis | 6 | 0 | 0 |
| W6 (52, 53) | 1.4 (`svd-stepper` built in stage 14) | 10 | 0 | 0 |
| W7 (54 to 58) | 1.5 with its continuous-time levels, and the weekly problems | 23 | 2 | 0 |
| **P0** | | **131** | **22** | **9** |

**Effort** [our estimate, agent-days as defined in section 11.2]:

| P0 composites | All hand-written | With scenes (chosen) |
|---|---|---|
| 25 S, 98 M, 8 L that can be scenes | 37.5 + 294 + 48 = 379.5 (S 1.5, M 3, L 6) | 12.5 + 98 + 16 = 126.5 (S 0.5, M 1, L 2) |
| 22 bespoke (10 M, 12 L) | 102 | 102 |
| The scene layer (stage 14, four pilots) | | 14 |
| **Total** | **about 480** | **about 240** |

A hand-written composite is about 800 to 1,500 lines with its tests; a scene is about 150 to 350 lines plus its model functions, which a hand-written composite would also need [our estimate]. The scene rates price the layout, the modes, the three input paths, `describe` snapshots and the visual baselines of every fixture state (390 px, light and dark), not the domain models: those are built and costed once, in the service stages 3a to 3g (61 AD, section 11.3), because both columns need them. Stage 14 builds the layer with four pilots that cover the four families (`place-value-chart`: tokens and steppers without axes; `outcome-grid`: the reference lesson's grid with its recipes and element ids; `unit-circle`: a plot with a constrained handle; `svd-stepper`: a heavy model from stage 3a with several P0 modes and Python parity). Its gate is quantitative: each pilot at most 350 lines of `scene.ts`, P95 frame time within 8 ms at 4x throttling, every generic suite green, and each pilot's measured AD recorded; the rate per family is recalibrated from its pilot before stage 27. If a family fails, its composites revert to bespoke and the estimate is redone before stage 27; the result goes in `docs/DECISIONS.md`. The worst case is bounded: every family reverting costs about 240 AD more, against the 40% contingency of 182 AD on stages 11 to 58 and the service stages (section 11.2), so if more than one family fails the build stops at stage 14 and the owner re-plans before stage 27.

**Rejected.** (a) `WIDGETS.md` as written, every composite with its own view: about 240 AD more for P0 alone and 131 copies of the machinery the prototype got wrong. (b) A dataflow or expression language in content: logic in data that `zqverify` would have to prove like code. (c) Forcing composites into presets: a preset has no state derivation (`WIDGETS.md` decision 4 stands for presets). (d) A third-party diagram library such as JSXGraph or Mafs [recalled]: neither offers our contract (`describe`, `targets`, sealed secrets, three input paths, ghost previews) and either would add a second rendering model beside Preact and signals.

---

## 4. Language selection

### 4.1 Languages

| Component | Language | Justification |
|---|---|---|
| App, engine, widgets, scenes, tutor client | TypeScript 6.0.3, TSX on Preact 11.0.0 with @preact/signals | Measured: with signals bound to attributes, Preact's drag frames equal hand-written DOM code (2.8 ms median, 4x throttling, 1,264 static nodes), so the choice falls to maintainability; typed props catch the config and callback errors agent-written code makes; no `eval` or `new Function`, which the Artifact's script policy needs (`ARCHITECTURE.md` 2) |
| Styles | CSS custom properties, CSS Modules, one stylesheet per target | One own-file stylesheet fits the Artifact's style policy; tokens are the theme switch; no unstyled flash for lazy widgets |
| Content | YAML 1.2 under a strict profile, prose in ZQ Markdown | 74% of a lesson's lines are structure [measured]; TeX backslashes need no escaping; line-by-line diffs (`CONTENT-FORMAT.md` 2) |
| Generators | TypeScript on the device, a Python twin in CI | Unlimited practice needs code on the device; the twin, written from the plain-language semantics without reading the TypeScript, is the second implementation |
| Verifier | Python 3.12 with SymPy and NumPy | Exact rational and symbolic arithmetic in a different language and library from the runtime, so a shared-logic bug cannot pass both |
| Learner Python | Python 3.14.2 on Pyodide 314.0.7 in the web app; CPython 3.12 in CI as the floor | Real CPython semantics, tracebacks and NumPy/pandas versions; the Artifact has no Python (section 4.3); the floor keeps drills valid for a learner's own machine, and 3.12 is the oldest Python that has `sys.monitoring` for the soft deadline and installs SciPy 1.18.0 [measured: `uv pip compile`, 7 October 2026] (conflict 19) |
| SQL drills | SQLite 3.53 in WebAssembly, web app only | A real SQL engine in a worker, no server; the Artifact publishes no third-party binary |
| C++ drills (P1) | Clang in WebAssembly on the web app if the 1.9 spike passes; otherwise the learner's machine | The Artifact publishes no compiler toolchain; no remote compile keeps learner code on the device |
| Tutor proxy | TypeScript on Cloudflare Workers, with a Node 22 entry | Fetch-native streaming; shares `context/schema.ts` and `render/anthropic.ts` with the browser byte for byte, so validation and escaping happen at one trust boundary |
| Build, release and test tools | TypeScript through `tsx` | Same packages as the app, so the compiler and CI replay run the shipped graders |
| Mascot | Inline SVG, a TypeScript spring integrator, Web Animations | Measured 11,067 bytes gzipped (draft 3 hair, 7 October 2026) with live physics and theme tokens; Rive's runtime fetch is blocked in the Artifact (`BERTIE.md` 11) |

### 4.2 Pinned versions

Every version is exact (`save-exact=true`), the lockfile is committed, and `ARCHITECTURE.md` 3 lists the full set with licences. The load-bearing pins:

| Dependency | Version | Why this one |
|---|---|---|
| Node.js, npm | 22.22.0, 10.9.4 | Vite 8 needs 20.19 or 22.12 and above; maintenance until April 2027 [recalled], move to 24 planned for March 2027 |
| TypeScript | 6.0.3 | typescript-eslint 8.71.1 declares below 6.1; type-aware lint is a guard rail; 7.x when the lint supports it |
| Preact, @preact/signals, @preact/signals-core | 11.0.0 (fallback 10.29.8), 2.11.3, 1.14.4 (MIT; transitive, imported by `@preact/signals`) | 37% faster than 10.29.8 on the undisciplined case [measured]; the fallback ran the same benchmark unchanged. 11.0.0 ships ES modules only, 10.29.8 also ships UMD builds [measured on the npm tarballs, 7 October 2026], which makes 10.29.8 the Artifact's fallback if its import map fails (section 4.3) |
| Vite, esbuild | 8.3.3, 0.28.2 | Rolldown code splitting groups for the cluster chunks; esbuild for the content compiler and generator modules |
| zod | 4.6.5 (`zod/mini` on the main thread) | Classic zod bundles to 92 KB gzipped against 6.4 KB for `zod/mini` [measured]; classic only in workers, Node and CI |
| KaTeX | 0.19.0 | Strict mode; no `eval`; one innerHTML sink; `output: 'mathml'` in the Artifact, which has no KaTeX fonts (conflict 21) |
| MathLive, Compute Engine `latex-syntax` | 0.111.0, 0.148.0 | Maths keyboard (web only); one LaTeX parser for grading at run time on both targets and in CI (128 KB gzipped against 1.19 MB for the full engine) |
| ts-fsrs | 5.4.2 | FSRS-6 per skill and band (`ASSESSMENT.md` decision 7) |
| fflate, idb, minisearch | 0.8.3, 8.0.4, 7.2.0 | Log packs and exports; IndexedDB promises; one search index file per stage |
| Pyodide | 314.0.7 (Python 3.14.2, NumPy 2.4.6, pandas 3.0.2) | Web app only; moves only with the content pin. It ran on the owner's iPhone inside an Artifact (`spikes/README.md`), a record the publishing rule does not adopt |
| CPython in CI, uv | 3.12 (latest patch at stage 1), uv 0.8.17 | `tools/py/uv.lock` pins NumPy 2.4.6, pandas 3.0.2, SciPy 1.18.0, statsmodels 0.14.6, scikit-learn 1.8.0, matplotlib 3.10.8, SymPy 1.14.0, pytest and hypothesis to Pyodide 314.0.7's lock where drills depend on them; the set resolves on 3.12 [measured] |
| @cloudflare/vitest-pool-workers | pinned at stage 62 [unverified: version] | Runs the `TutorLimits` Durable Object tests in the Workers runtime, not only in Node (section 7.3) |
| @sqlite.org/sqlite-wasm | 3.53.4-build2 | SQL drills, web app only |
| `cdn.lock.json` | generated from `package-lock.json` by `tools/cdn` | Every third-party file the Artifact loads: its exact-version URL, SHA-384 and how it loads (section 4.3) |
| Workbox, vite-plugin-pwa | 7.4.1, 2.0.0 | Tested precaching and strategies with our own routing (`injectManifest`) |
| Vitest, Playwright | 5.0.3, 1.63.0 | Browser-mode widget tests on real Chromium; end to end on both targets |
| ESLint, typescript-eslint | 10.12.0, 8.71.1 | Our custom rules need ESLint |
| @anthropic-ai/sdk, wrangler | 0.131.0, 4.147.0 | Proxy upstream client with retries; Worker deploys |
| Model | `claude-opus-5-5`, configuration not code | Project default; effort per mode through a per-message effort message so the cache prefix stays byte-stable (`AI-TUTOR.md` decision 23) |

### 4.3 The Artifact publishing rule, and Python on the web app

**The rule** (the owner's correction of 7 October 2026; it replaces draft 1's decision 7, its JSON-part Python layout and fallbacks F1 and F2). The Artifact publishing tool requires the publishing session to read every file it did not write before publishing it, and never publishes a file it cannot read. The Artifact therefore publishes **only files generated from this repository's own sources**: our compiled app code, content bundles, generator modules, our CSS and data. It publishes no third-party code and no binary. The web app (GitHub Pages or local; where it is served before a content licence exists is decision 13) is not published through the Artifact tool and keeps everything.

| Area | Artifact | Web app |
|---|---|---|
| Third-party JavaScript | Loaded at run time at exact versions from cdnjs where it hosts the identical file, otherwise jsDelivr's `/npm/` path [our choice; cdnjs coverage per file is checked by `tools/cdn`, unverified today]; fonts only from Google Fonts | Bundled into our own chunks |
| Python, SQL, C++ | None. A code screen shows its starter code, recorded output and the handoff link ("This drill runs in the web app" on a drill, "Finish this in the web app" on a lesson screen); the link and the result code (`ASSESSMENT.md` 14.3) carry the attempt there and back | Pyodide 314.0.7 with every load group (section 5.7), SQLite, Clang if the 1.9 spike passes |
| Maths | KaTeX from the CDN with `output: 'mathml'`, in system maths fonts; no KaTeX CSS or fonts | KaTeX bundled; HTML and MathML output with self-hosted KaTeX fonts |
| Expression input | Plain field with the symbol bar and a live MathML preview; the same parser and grader | MathLive |
| Lessons | Every screen plays: authored code runs at build time and every number a widget shows comes from our own JavaScript models. A screen whose widget executes learner input resolves as `read` and is finished in the web app (below) | Every screen plays and grades |

**How the Artifact loads third-party modules.** `tools/cdn/lock.ts` writes `cdn.lock.json` from `package-lock.json`: for each runtime package, the file our build imports, its exact-version URL, its SHA-384 and how it loads. Preact 11.0.0 ships ES modules only, its `hooks` and `compat` entries import `preact` by bare name, and `@preact/signals` 2.11.3 imports `preact`, `preact/hooks` and `@preact/signals-core` [measured on the npm tarballs, 7 October 2026]. So the page carries an **import map**, written into the page fragment by `tools/release/page.ts` before the bootstrap script, mapping every bare name our chunks and these libraries use to its pinned URL, with an `integrity` entry per URL. The Artifact build marks those packages external, so our chunks keep bare names and the browser resolves them through the map. Workers see no import map [recalled], so the data worker's imports (classic zod, ts-fsrs and fflate, each a module with no bare imports [measured]) are rewritten to full URLs at build time. `tools/release/provenance.ts` fails the Artifact build if any input from `node_modules` lands in any published JavaScript file: it reads Rolldown's module graph for the app chunks and the data worker, and esbuild's metafile for each of the 26 generator modules, which the content compiler builds outside Rolldown (second review round). Rejected: jsDelivr's `+esm` builds, which resolve dependency ranges on the CDN, so `@preact/signals`' peer `preact` would not be ours to pin; an import map built at run time, which cannot be probed because the page may fetch nothing from the CDN hosts.

**Integrity.** The import map's `integrity` field is the only subresource integrity a module import can carry; whether iOS 18.7 enforces it is [unverified] (spike S1), and worker imports carry none. Where SRI is absent the controls are exact-version URLs (never a range, `@latest` or `+esm`), a nightly job that fetches every locked URL and fails on any byte difference, and the host's CSP, under which an altered script can reach no host beyond the listed CDNs (section 7.6).

**Named fallback.** If S1 finds the import map ignored in the Artifact page: Preact 10.29.8, the measured fallback version, whose UMD builds load with `@preact/signals`' UMD build as classic `<script>` tags with `integrity` attributes; generated shims (our code) re-export the globals, and the self-contained libraries keep loading by full URL.

**Python on the web app.** One worker (`src/workers/python.worker.ts`), one grader (`grader.py`, `zqtest.py`), Pyodide's native layout with `loadPackage` and its integrity checks. Timeouts have two levels: a soft deadline raised inside Python from a `sys.monitoring` jump callback (the worker stays warm), and a page watchdog that terminates and restarts the worker only when the soft deadline cannot fire (long C calls); CI runs on CPython 3.12 and Pyodide's 3.14, both of which have `sys.monitoring`, and the CI harness adds a subprocess wall-clock limit around every drill run. Details: `ARCHITECTURE.md` 6.3.

**Live-code screens in the Artifact** (second review round). A lesson screen or lesson quiz item whose widget executes learner input (any `code` check; `code-cell`'s Run and Submit; `mutant-hunter`; `injection-lab`'s `code` answers; `code-tracer`'s live mode; `bench-lab`'s device races; `plot-workbench`'s `code` answers) has no runtime in the Artifact, so:

1. The screen shows its handoff state: the starter code, the authored recorded output and "Finish this in the web app" with the handoff link. Each such widget's `WIDGETS.md` entry states this mode; `parsons`, whose `ordering` answer needs no execution, plays fully and shows the reference order's recorded output.
2. The reducer enters `reading` instead of `idle` when the screen's runtime answers `not-in-this-build`; Continue is enabled at once, the tally records `read` (no attempt, no XP, no Redo entry), and the `lsn screen` event carries `deferred: 'web'` (`ARCHITECTURE.md` 5.7.2).
3. The fold derives a "Finish in the web app" item from every deferred screen, keyed by (lesson id, `rev`, screen id), shown on Today and on the course map until it clears.
4. The handoff link carries `{ kind: 'screen', lesson, rev, screen }`; the web app opens the lesson at that screen, and after the learner's attempt shows a result code whose `ref` is (lesson id, `rev`, screen id) (`ASSESSMENT.md` 14.3). Merged in the Artifact, the attempt clears the item and earns XP by the lesson-screen rule.
5. The lesson completes in the Artifact with deferred screens counted as resolved; the lesson's "Passed" star waits for the result code of any deferred quiz item. A `rev` bump retires a pending item, because the screen it names no longer exists in that form.

Stage 24 tests the reducer rows with the Artifact's handoff stub; stage 70 tests the screen result code round trip; stage 82 finishes one from the Artifact on the phone.

**Effect on daily use.** Every homework set has a drill from level W1, so in Stage 0 the learner opens the web app about once a level for homework and to finish the live-code screens of the 0.4 course Y lessons; 1.1, 1.2 and 1.9 are code-heavy and are best studied in the web app. Every other lesson screen, quiz, level review and non-code item plays fully in the Artifact.

**What the rule removes.** `tools/pysplit`, the JSON-part layout and its 15 Artifact files, the Python rows of the Artifact budget, the `python.groups` flag, KaTeX font files and SQLite in the Artifact, decision 7 and fallbacks F1 and F2. The measured run of Pyodide inside an Artifact on the owner's iPhone stays in `spikes/README.md` as a record, marked not adopted.

---

## 5. Data

### 5.1 Sourcing

| Data | Source | Licence and access constraints |
|---|---|---|
| Lessons, items, generators, drills, papers | Authored in the repository by agents and the owner, following the fifteen item files | Ours (MIT for code; content licence chosen at publication, section 12). Adapted textbook problems follow the copyright rule of `CONTENT-FORMAT.md` 9.4, which needs the owner's sign-off |
| Canon references | About 506 source ids (`canon-gap.md` 6's 267 plus 239 new ids the item files cite; 425 of the 506 cited, `docs/CURRICULUM.md` 5.3; draft 1: about 398 works) as `content/sources.yaml` entries; every citation carries a `loc` | Citations only; no copyrighted text is copied. Locations in free sources (OCW, OpenStax, open notes, free book PDFs) are checked by fetching them while authoring; paid-book locations stay `checked: false` until the owner reads that section, and each course report lists them as warnings (`CONTENT-FORMAT.md` 9.3 rule 27, 9.4) |
| Drill datasets | Synthetic data generated by seeded scripts committed with the course; public-domain or permissively licensed sets where a lesson names one | Licence recorded per dataset in `sources.yaml`; no data whose terms forbid redistribution |
| Pyodide and wheels (web app) | The official Pyodide 314.0.7 release; `hypothesis` from PyPI | MPL-2.0 and package licences; every wheel checked against the SHA-256 in `pyodide-lock.json` (ours pinned for `hypothesis`) before use; never published to the Artifact |
| Third-party JavaScript (Artifact) | cdnjs or jsDelivr at the exact versions `package-lock.json` pins, listed in `cdn.lock.json` | The same licences as the web build's bundled copies (section 7.6); loaded at run time, never published |
| Fonts | Archivo, Besley, Source Code Pro (SIL OFL); KaTeX fonts | Google Fonts in the Artifact, committed `woff2` on the web; KaTeX `woff2` on the web only, since the Artifact renders MathML in system maths fonts |
| Learner data | The learner, on their own device and (Artifact, unless device-only mode) their private `db` subtree | Never in the repository; tests use the synthetic learner. A tutor eval fixture derived from a real reply has every learner string replaced by an owner-approved paraphrase and carries `redacted: true`; CI fails any fixture without `synthetic: true` or `redacted: true` (`AI-TUTOR.md` 9.7) |

### 5.2 Storage and formats

| Data | Format | Why |
|---|---|---|
| Content source | Strict YAML plus ZQ Markdown, one lesson per file | Reviewable diffs; no executable content |
| Compiled courses | One JSON bundle per course, content-addressed names | Native parse, a served type on both hosts, validated once per hash; one file per course fits the 255-files-per-publish limit where per-lesson files would not |
| Generators at run time | One self-contained ES module per topic (`.mjs`), built by esbuild | Code must run on the device; plain data in, plain JSON out; 26 files instead of 103 |
| Content manifest | One JSON file named by its hash, referenced by the page's `<meta name="zq-manifest">` | A content-only release renames only the page, the manifest and the touched courses (`ARCHITECTURE.md` decision 30) |
| Third-party modules in the Artifact | `cdn.lock.json` (URL, SHA-384, import kind), turned into the page's import map | The Artifact publishes none of them (section 4.3); one locked list the nightly drift check reads |
| Progress | Append-only JSON events; derived state by a deterministic fold; snapshots | Merge across devices and targets is a set union; model changes are rebuilds, not migrations (`ASSESSMENT.md` 13) |
| Progress at rest, device | IndexedDB (`zq` database: events, snapshot, drafts) | Durable within the browser's quota; works offline |
| Progress at rest, Artifact replica | `db` documents: per-device chunks (48 KiB, 200 events), gzip-plus-base64 packs (192 KiB), snapshot parts, leased drafts | The store is last-writer-wins without transactions, so every document has exactly one writing device |
| Caches | `BlobCache` in IndexedDB by hash: bundles and generator modules; on the web, Python packages in the service worker cache | Disposable; the Artifact has no service worker |
| Exports | One HTML record plus CSV tables in a zip (`downloads` capability); sync files and result codes as text | Opens anywhere; a week's sync file is about 40 KB, small enough to paste on a phone |
| Release ledger | `releases/<release>.json`, committed with the release pull request; its SHA-256 is written into `meta/release` | A fresh cloud session must know exactly what the previous release published: drift, garbage collection and rollback all read ledgers, not ignored build output (section 8.6) |

### 5.3 Data model

- **Content.** Stage, topic, course, level, lesson, screen; items, sets (practice, homework, review), exams with forms and sections, drills, generators, skills (a graph with `requires`, `encompasses`, `exercises`; at level grain, at most 2 introduced per lesson, finer distinctions as step tags that carry no card), misconceptions, glossary terms, Notebook cards, sources, tracks and the plan. Ids are immutable, human-readable and kind-prefixed (`lsn.numwork.digit-worth`, `crs.numwork`, `gen.alg.*`); display numbers come from position. Every lesson, item, drill and generator carries a `rev`; an answer hash in `ids.lock.json` forces a `rev` bump and a changelog line whenever an accepted answer, tolerance or screen order changes; learner-state migrations are data (`rename`, `merge`, `split`, `retire`). Owner: `CONTENT-FORMAT.md` 3 and 4.
- **Id kinds** (`CONTENT-FORMAT.md` 4.1): `stg.` stage, `top.` topic, `crs.` course, `lvl.` level, `lsn.` lesson, `itm.` item, `set.` set, `exm.` exam, `drl.` drill, `gen.` generator, `skl.` skill, `mc.` misconception, `gls.` glossary term, `crd.` Notebook card, `src.` source, `trk.` track, `prj.` project; library ids carry the topic's namespace (`gen.alg.*`, `skl.dsa.*`). Element ids inside widgets are `kind:name` (`cell:5,3`), prefixed by the widget's local id on multi-widget screens (`grid/cell:5,3`).
- **Widget state.** `{ a, v }`: `a` is answer state (graded, saved), `v` is view state (show-why may tween it); JSON, at most 32 KB; drafts keyed `lesson:<id>@<rev>:<screen>:<widget>` so a new `rev` never meets an old draft. Owner: `ARCHITECTURE.md` 5.3.
- **Progress.** Events with the envelope `id, t, tz, dev, seq, rel, app, v` and kinds `att`, `lsn`, `hw`, `exam`, `mark`, `ment`, `weekly`, `out`, `proj`, `paste`, `time`, `prior`, `set`, `plan`, `import`. Derived state: lesson progress, homework and paper states, FSRS cards, the Redo queue, seen generator points, the fact model, streaks, XP and MP, hours, exit parts, the plan. Owner: `ASSESSMENT.md` 13.
- **Tutor.** `TutorRequest` is assembled per call and not stored; marking results, recaps, diagnosis ids and usage counts persist as learner data; chat threads live for the session only. Owner: `AI-TUTOR.md` 4 and decision 20.

### 5.4 Lifecycle

```
content/*.yaml --zq check--> --zq verify--> --zq build--> dist/content/ (bundles, gen modules, manifest, search, glossary, Notebook)
                                                    \--> vite build --mode web | artifact --> dist/web/, dist/artifact/
pyvendor fetch (pinned release, SHA-256) --> .zq/py-vendor/ --> dist/web/py/314.0.7/ (native layout, web only)
package-lock.json --cdn lock--> cdn.lock.json --> Artifact build: third-party imports external; page.ts writes the import map
learner actions --> events --> IndexedDB (both) [--> db replica (Artifact)] --> fold --> derived state --> screens
```

| Committed | Ignored |
|---|---|
| `content/`, `ids.lock.json`, `migrations.yaml`, generator Python twins, `releases/*.json`, `cdn.lock.json`, `tests/visual/baselines.lock.json` (the SHA-256 of every approved baseline), synthetic learner generator and its seeds, learner fixtures built from synthetic logs, `.env.example`, `.env.eval.example`, `.dev.vars.example`, `package-lock.json`, `tools/py/uv.lock` | `node_modules/`, `dist/`, `.zq/cache/`, `.zq/py-vendor/` (Pyodide release, cached by CI keyed on its version), `test-results/`, `.env`, `.env.eval`, `.dev.vars`, `proxy/.state/`, `prototype/vendor/pyodide/`. Visual baselines live on the orphan branch `visual-baselines`, rewritten as one commit whenever the owner approves a change, so `main` history carries no images (`ARCHITECTURE.md` 8.3) |

### 5.5 Volume assumptions

| Quantity | Size | Consequence |
|---|---|---|
| Lessons | 2,445 (2,341 counted plus 104 in optional 3.2; draft 1: 2,148); about 27 KB compiled each | 103 course bundles, 80 to 115 MB in all [scaled from draft 1's 70 to 100 MB] |
| Lesson source | About 800 lines of YAML for a 12-minute lesson, plus its library entries | One lesson and its library entries per pull request, with no line cap on YAML; generators with their Python twins in pull requests of their own (section 11.1) |
| Python, whole stack (web app, native layout) | Core and standard library 13.5 MB, the six groups' wheels 49.6 MB [measured, `ARCHITECTURE.md` 0.2 and 6.3.3]; with NumPy and pandas 21 MB (`ARCHITECTURE.md` 6.4.1) | Load groups per course (5.7); first download offered with its size; nothing in the Artifact |
| Progress, whole path | About 121,000 events for 2,445 lessons, 66 MB as JSON, about 30 MB packed in about 160 packs; snapshot about 1.4 MB (scaled by lessons from `ASSESSMENT.md` 13.6's 106,000 events for 2,148 [our estimate]) | About 215 `db` documents per learner against 25,000 allowed; fold rebuild in the data worker within 3 s on the iPhone |
| Skills and cards | About 1,700 skills at level grain (431 levels, about 4 each), about 1,860 scheduled cards with the stretch cards of the core-interview topics [scaled from draft 1's 1,500 and 1,630 on 377 levels] | Maintenance about 340 h over the path at 15 h a week [scaled from the simulated 300 h, section 12]; about 33 unscaffolded attempts per skill |
| Tutor, learning | About USD 15 to 25 a month on the web at 15 hours a week [inferred]; spend capped at USD 3 a day and USD 30 a month | Proxy limits; the Artifact spends the viewer's own plan |
| Tutor, evals | A full web run is about USD 31: 435 tutor calls on `claude-opus-5-5`, about USD 18, and 435 judge calls on `claude-sonnet-5-5` at half Opus 5.5's per-token price, about USD 13 [sourced prices; token counts inferred]. If the judge fails calibration it moves to `claude-fable-5-1` (about USD 62 of judge calls, USD 80 a run). Budget: about 10 full runs over stages 60 to 67 (about USD 310, USD 800 with the stronger judge); after that one full run per prompt, renderer or model change; per course, a hint and diagnose subset of 10 scenarios (6 hint, 4 diagnose) at 3 repeats, about USD 2 a course, USD 210 over the path's 103 courses; the judged Artifact tier run about USD 5 of judge calls per tutor-changing release [inferred from `AI-TUTOR.md` 6.5] | A separate eval environment with its own token and caps: the eval proxy at USD 60 and 2,000 requests a day for tutor calls, and the runner's own cap of USD 75 a run for judge calls, which go to Anthropic directly (section 7.3); eval spend never touches the learning cap. The authoring agent drafts each course subset's `should`, `mustNot` and diagnose gold labels from the screen's authored register, the semantic reviewer checks them, and the owner approves the set for Stage 0 courses, the decision-10 reviewer beyond Stage 0 |

### 5.6 Artifact file and size budget

Recomputed on 7 October 2026 for the publishing rule (no Python, SQLite, KaTeX fonts or third-party libraries among the published files) and for the adopted curriculum: 103 course bundles, 26 topic generator modules and 26 widget clusters (the scene tier adds no chunk: scenes live in their cluster). Enforced by `tools/release/budgets.ts` and `provenance.ts` in every build, not only at release.

| Group | Files | Raw size |
|---|---|---|
| App: page, entry, stylesheet, `version.json`, 4 screen groups, tutor, 26 clusters, the data worker | 36 | at most 12 MB (about 8 MB [inferred from the gzipped budgets of `ARCHITECTURE.md` 9.2]) |
| Third-party libraries (Preact, signals, zod, KaTeX, the Compute Engine parser, MiniSearch, ts-fsrs, fflate, idb) | 0: loaded from the CDNs in `cdn.lock.json` | |
| Python, SQLite, fonts | 0 | |
| Content: manifest, 4 search indexes, glossary, Notebook, 4 skill graphs, curriculum, plan (13); 103 bundles; 26 generator modules; up to 20 assets | about 162 | at most 130 MB |
| **One release** | **about 198** | **about 125 MB** |

| Limit [our choice] | Files | Size | Host limit [sourced] |
|---|---|---|---|
| One release | 230 | 150 MB | |
| Retained version (this release plus files only the previous one uses) | 300 | 200 MB | |
| Peak while staging | 480 | 250 MB | 511 files, 256 MB per version; 255 files and 64 MB per publish |

`budgets.ts` also caps the visual baselines (section 5.4): at most 4,000 images and 300 MB on the `visual-baselines` branch, which hold widget fixture states at 390 px in both themes and app screens at 390 and 1,280 px in both themes.

A release whose peak would exceed the last row becomes a maintenance release (`ARCHITECTURE.md` 6.2.6): expected only for a format-wide re-emit of every course. An ordinary app release renames about 36 files (up to 12 MB), so its peak is about 270 files and 150 MB.

### 5.7 Python load groups per course (web app)

The web build ships every group; the Artifact ships none and hands every drill off. Stage 25 measures each group's timing and memory on the owner's iPhone in the web app; it passes when `stdlib` and `numpy-pandas` pass, and the rest are recorded (conflict 9). A group that exhausts the phone's memory still runs in the web app on a computer.

| Curriculum | Drills need | Groups | Web download when first needed |
|---|---|---|---|
| 0.1, 0.2, 0.4, 0.5; 0.3 drills; A1 (`zq_ra` prelude: `fractions`) | standard library only (`needs: []`) | core, `stdlib` | 13.5 MB |
| 0.3 Precalc Lab part 3 | NumPy, matplotlib | `numpy-pandas`, `matplotlib` | +7.9 MB and +9.5 MB of wheels |
| 1.1 Python | NumPy, pandas, matplotlib; pytest or hypothesis where a drill names them | as above, plus `testing` with the first drill that needs it | `testing`: +2.7 MB |
| 1.2 Tools | pytest, hypothesis | `testing` | none new if 1.1 loaded it |
| 1.3, 1.4, 1.5, 2.0a | SciPy where named | `scipy-statsmodels` | +22.4 MB |
| 1.6, 2.2, 2.2c | statsmodels | `scipy-statsmodels` | none new |
| 2.0b | cvxpy-base with Clarabel, highspy | a new `optimisation` group, on SciPy [present in Pyodide 314.0.7's lock; untested in a browser]; its drills fall back to `highspy` if cvxpy fails (`stage2-numerics-optimisation.md`) | [unverified], measured when the 2.0b wave is briefed |
| 2.1, 2.1b, 3.1 | scikit-learn; NumPy for 2.1b's from-scratch engine | `sklearn`, `numpy-pandas` | `sklearn`: +4.6 MB |
| 1.9, 2.4 C++ | Clang | none | in-browser Clang if the 1.9 spike passes, else local paste |

Where a drill runs is decided at run time: `PythonRuntime.available(needs)` answers from `engine/python/budget.ts` on the web, and is the handoff stub in the Artifact, which shows "This drill runs in the web app" with a handoff link and returns by result code (`ASSESSMENT.md` 14.3). `optimisation` adds `cvxpy` and `highspy` to `PyPackage` and `Drill.needs` at the 2.0b wave (`ARCHITECTURE.md` 5.9, `CONTENT-FORMAT.md` 3.2).

---

## 6. Interfaces and data flow

### 6.1 Flow

```
AUTHORING AND CI
  content/*.yaml -> zq check (CompilerRegistry: widget logic, schemas, scenes, presets; leak lint via @zq/graders)
                 -> zq verify (zqverify, Python: every answer, misconception value and claim recomputed independently)
                 -> zq build -> bundles (.json), generator modules (.mjs), manifest (named by the page)

RUNTIME, EITHER TARGET
  page -> manifest -> ContentSource -> data worker (SHA-256, structural schema) -> LessonPlayer (pure reducer)
  LessonPlayer -> WidgetHost -> primitive, scene or bespoke view        (lock, marks, show-why, reveal)
  WidgetHost --answer--> @zq/graders --Grade--> LessonPlayer --EventDraft--> AppendQueue -> ProgressStore
  ProgressStore: IdbStore (web) | IdbStore mirror + DbStore -> db (Artifact)  -> fold -> derived state -> screens
  code screen (web) -> PythonRuntime -> python.worker (Pyodide, native loader) -> grader.py -> RunResult -> Grade
  code screen (Artifact) -> handoff link to the web app -> result code pasted back -> import
  Artifact page -> import map from cdn.lock.json -> third-party modules from cdnjs or jsDelivr (exact versions)

TUTOR
  player state + widget describe/targets/secret + content tutor fields -> TutorService (gate) -> TutorRequest
    Artifact: render/sample -> claude.use('sample') (viewer's account, streamed onText)
    Web:      POST /v1/tutor (bearer token) -> proxy: validate, render, sign -> Anthropic Messages API (streamed)
  reply stream -> act line validation, leak probe, code guard, lint -> DOM text + validated actions -> host overlay

BETWEEN TARGETS
  Artifact -> web app: handoff link (?h=, at most 8 KB); web app -> Artifact: result code; either way: sync file (union merge)
RELEASE
  release PR commits releases/<release>.json (ledger) -> Claude session rebuilds from the tag, checks every SHA-256 against the ledger
    -> Artifact tool publishes (planned batches) -> db meta/release {release, ledger hash} -> open pages show the update notice
```

### 6.2 Interfaces

| # | Boundary | What crosses | Format | Direction | Contract |
|---|---|---|---|---|---|
| 1 | `content/` to compiler | Lessons, library entries, generator specs | Strict YAML, ZQ Markdown | in | `CONTENT-FORMAT.md` 2, 3 |
| 2 | Widget library to compiler | `CompilerRegistry`: logic, schemas, presets, scenes (no views) | TypeScript objects in Node | library to compiler | `ARCHITECTURE.md` decision 33, 5.3, 5.14 |
| 3 | Compiler to `zqverify` | Verify jobs: spaces, MathJSON, chains, claims | JSON files | out | `CONTENT-FORMAT.md` 6 |
| 4 | Build to runtime | Bundles, generator modules, manifest, search, glossary | Hashed `.json` and `.mjs` own files | out | `CONTENT-FORMAT.md` 8.2; `ContentSource` (`ARCHITECTURE.md` 5.9) |
| 5 | Main thread and data worker | Bundle bytes; fold rebuilds; search; export and import | Messages with transferred `ArrayBuffer`s | both | `ARCHITECTURE.md` 5.13 |
| 6 | Player and widget host | Lock, `answer`, paint marks, show-why steps, reveal, reset | TypeScript calls and signals | both | `ARCHITECTURE.md` 5.3, 5.4, 5.7 |
| 7 | Scene to widget logic | `SceneDef` to `WidgetLogic` (tier `scene`), paired with `SceneView` by the generated cluster entry | TypeScript, at module load | in | `ARCHITECTURE.md` 5.14 |
| 8 | Player and graders | `Answer`, `Check`, `GradeCtx` to `Grade` (verdict, marks, diagnosis, nudge) | Pure function call | both | `CONTENT-FORMAT.md` 7.1 |
| 9 | Player and progress | `EventDraft` to an enveloped event | JSON | out | `ASSESSMENT.md` 13.2; `ARCHITECTURE.md` 5.7.1 |
| 10 | `DbStore` and `db` | Chunks, packs, snapshots, leased drafts, board entry | `db` documents under `data/users/<id>/` | both | `ASSESSMENT.md` 13.4, 12.5 |
| 11 | Engine and platform | The `Platform` interfaces | TypeScript interfaces | both | `ARCHITECTURE.md` 5.9 |
| 12 | `PythonRuntime` and Python worker | `init`, `load`, `run`, `trace`; progress, events, figures, results, failures | `ToPython` and `FromPython` messages | both | `ARCHITECTURE.md` 6.3.1 |
| 13 | Python worker and own files (web) | Pyodide core and wheels | `loadPackage` with integrity checks | in | `ARCHITECTURE.md` 6.3.2 |
| 14 | Engine to tutor | `TutorRequest`: screen, outline, widget describe and targets, sealed block, learner input | TypeScript object, validated by the shared schema | out | `AI-TUTOR.md` 4.1 |
| 15 | Tutor and `sample` | Turns, options (`modelTier`, `cache`, `tools`, `signal`), streamed text, errors with `code` | Capability calls | both | `AI-TUTOR.md` 6.2; `sample.d.ts` 0.2.69 |
| 16 | Tutor and proxy | `WireRequest` (`v`, `promptVersion`, `request`, signed history, tool loop with signed assistant blocks and schema-checked results); event stream | HTTPS JSON in; streamed events out | both | `AI-TUTOR.md` 6.3.2, 6.3.3 |
| 17 | Proxy and Anthropic | Messages API body (tools, two system blocks, messages, effort message, fallbacks) | HTTPS, streaming | both | `AI-TUTOR.md` 6.3.4, 4.7 |
| 18 | Tutor reply to page | Act line actions: `highlight`, `showHintRung`, `setWidgetHint`, `openNotebookCard`; tools `getScreenState`, `compute` | One JSON line, validated; tool results | in | `AI-TUTOR.md` 5 |
| 19 | Artifact and web app | Handoff payload, result code, sync file | base64url of deflated JSON; text | both | `ASSESSMENT.md` 14 |
| 20 | Release session and host | Publish batches, file listing against the previous ledger, `meta/release`, `ops/selftest-<release>`, `ops/gate-<stage>` from the preview Artifact | Artifact and ArtifactData tool calls; `releases/<release>.json` in git | out, then in | `ARCHITECTURE.md` 6.2.6 |
| 21 | Web app and service worker | Update waiting, skip waiting, keep offline | `workbox-window` messages | both | `ARCHITECTURE.md` 6.4.1 |
| 22 | Artifact page and the CDNs | Third-party ES modules at exact versions | Import map with `integrity`; full URLs in the data worker | in | `ARCHITECTURE.md` 6.2.7 |

### 6.3 Four sequences

**Check on a task screen.** (1) A gesture ends: the view calls `api.commit`; `logic.answer` becomes non-null and the player receives `engage`, enabling Check. (2) Check: the reducer moves to `evaluating(gen)` and emits `lock` and `grade(gen)`. (3) The effect runner takes the widget's answer and calls `@zq/graders` (pure, within 150 ms), then dispatches `graded(gen, grade)`. (4) With a matching generation, the reducer moves to `correct` or `not-yet` and emits `paint`, `feedback`, `announce`, `record` (an `att` event whose XP and MP come from `fold/points.ts`), `show` (the matched diagnosis's show-why or the screen's `after`), the Bertie state and, when no authored diagnosis matched, `tutor-auto diagnose` (subject to the gate and, in the Artifact, to prior consent). (5) `record` passes through the `AppendQueue`: envelope, single-event fold, IndexedDB, and in the Artifact the outbox and a chunk write at most every 5 seconds. (6) The derived state signal changes, and the XP chip and progress bar read it. A result with a stale generation is ignored.

**A hint from Bertie.** (1) The learner asks; `TutorService` checks the gate (assessment state, this screen's first Check or 90 seconds of active input, the off switch, consent in the Artifact), assembles a `TutorRequest` by the mode's recipe (caps, escaping, the sealed block on an unresolved screen) and chooses the backend. (2) Artifact: `render/sample` builds the turns and calls `sample` on the quick tier with an `AbortSignal`, streaming through `onText`. Web: the browser posts the request with the bearer token; the proxy authenticates, checks limits, validates, renders the Messages API body with its stable cached prefix (tools, core prompt, lesson block), the per-call system message and the effort message, and streams events back. (3) Each completed sentence passes the act-line validator, the leak probe, the code guard and the lint before it renders as DOM text; validated actions reach the host overlay (a ghost only through the preview guard). (4) A leak aborts the call and shows the next authored rung; an error maps to its code and copy; usage counts are recorded without text.

**Submitting code.** (1) Submit: the reducer moves to `running(submit)` and emits `run-code all`. (2) On the web, `PythonRuntime.run` checks `available(needs)`; if nothing is cached, the download was already offered on the title screen. In the Artifact the screen has no Submit: it offers the web app (the next sequence). (3) The worker loads any missing group, then `grader.py` runs each test under the soft deadline while the page's watchdog watches each `test-start`. (4) Events stream back (output capped at 4,000 characters a stream, test results with hidden flags); the `RunResult` is graded by the `code` check and dispatched as `ran`, which the reducer treats as `graded`.

**A drill handed off to the web app.** (1) The Artifact builds a web-app link with the drill, homework instance, slot and seed in the fragment (for a live-code lesson screen, the lesson id, `rev` and screen id, section 4.3; at most 8 KB), or shows it as copyable text where links cannot leave the frame. (2) The web app validates the payload and runs the drill. (3) After submission it shows a result code (`ZQR1.`, deflated attempt events, CRC-32). (4) Pasted into the Artifact, the code is checked (checksum, schema, matching reference, not already present) and merged as an import. The checksum catches copying errors, not forgery; the learner is the only party relying on it.

### 6.4 What differs between the targets

Everything not in this table is the same source code. The bytes differ where the table says: third-party modules are bundled into our chunks on the web and imported from CDNs in the Artifact.

| Concern | Artifact | Web app |
|---|---|---|
| Platform adapter | `platform/artifact` | `platform/web` |
| Third-party JavaScript | From cdnjs or jsDelivr at exact versions, through the import map (section 4.3) | Bundled |
| Tutor backend | `sample` on the viewer's Claude account; tiers quick, default, complex, each certified by the judged Artifact eval before a tutor-changing release (`AI-TUTOR.md` 9.6) | Proxy to `claude-opus-5-5` with effort per mode, certified by the full web eval |
| Progress at rest | IndexedDB mirror plus the private `db` replica (switchable to device-only) | IndexedDB, persistence requested |
| Python and SQL drills | None: every drill hands off and returns by result code | Pyodide's native layout with every group; SQLite |
| C++ drills (P1) | Hand off | In-browser Clang if the 1.9 spike passes |
| Maths | KaTeX from the CDN, MathML output, system maths fonts | KaTeX bundled, HTML and MathML output, self-hosted KaTeX fonts |
| Expression input | Plain field, symbol bar, live MathML preview | MathLive |
| Offline | None | Service worker: app precached, courses and Python cached, "Keep offline" |
| Updates | `meta/release` in `db` raises the notice; reload | Service worker update with Restart |
| Fonts | Google Fonts for text faces only | All self-hosted |
| CSP | The host's: scripts from our files and the listed CDNs | Our meta CSP: `connect-src 'self'` plus the proxy |
| Files and downloads | `downloads` capability; paste where no picker | Blob links and file input |
| Release | A Claude session executes the publish plan; the owner runs Self-test | `pages.yml` on a `v*` tag |

### 6.5 Rules at the boundaries

- **One reveal path.** Only Show solution reveals an answer; it records the attempt as revealed with 0 XP and queues a redo. Bertie can offer it but never state the answer on a sealed screen (`AI-TUTOR.md` decision 13).
- **The Why rule.** On a screen that is still unresolved (graded not yet, neither correct nor revealed), the Why sheet shows the matched diagnosis line and `why.shown` only; `why.then`, which states the result, appears only after a correct answer or Show solution. `why.shown` therefore passes the same leak lint as the tutor fields. Bertie's `why` mode keys on the same answer status.
- **The sealed key.** On an unresolved lesson or explore screen the tutor receives the compiler's one-line check summary, the widget's `secret()` and the authored solution inside a sealed block; every sentence, note and chip of the reply passes the leak probe before it shows. Kill switch: config `tutor.answerKey: 'never'`.
- **The tutor cannot grade.** No path leads from a tutor action to `change`, a grade, the Redo queue or the position; ghost previews pass the preview guard, which refuses any patch that changes the answer or would grade correct.
- **Help opens per screen.** Hints and every sealed Bertie mode open after a first Check on that screen, or after 90 seconds of active time with an input, whichever comes first; on `trap` screens only after a first Check. Chat before the first Check answers wording questions with a hint-rung ceiling of 0, and Bertie never comments on anything the learner has typed before that screen's first Check (`AI-TUTOR.md` 2.2, 2.6).
- **Marks in a gate are the lower of two.** The learner marks each rubric point blind, then Bertie's marks appear; a gate counts $\min(\text{learner}, \text{Bertie})$ per point, a point the learner holds above Bertie goes on a disputed list resolved by a fresh exit-item sitting on that slot, and with the tutor off a gate's long-form marks stay provisional until Bertie or a person marks them (`ASSESSMENT.md` decision 6).
- **Derived numbers are derived.** XP, MP, streaks and mastery shown on screen are read from the fold; no UI code increments them.
- **Content and app ship together.** One release id; the page names the manifest by hash; a content-only release changes only the page, the manifest and the touched courses (a CI test builds twice to prove it).
- **Two KaTeX configurations, two outputs, one slot binding.** Authored maths renders in strict mode with `trust` limited to `\htmlData` with a checked name (`^[a-z][a-z0-9-]{0,15}$`); Bertie's maths renders with `trust: false`, `maxSize: 10`, `maxExpand: 1000`. The web app emits HTML with MathML; the Artifact emits MathML only, through the same sink. `TexSlots` binds every live slot the same way on both outputs: the slot renders as a sentinel `\text{}` token; on the web its HTML span's text node is bound, and in every MathML tree (the Artifact's output and the web's hidden copy) the sentinel `<mtext>` is replaced by an `<mn>` element built with `createElementNS`, whose `textContent` follows the signal, so slot digits use the maths font and screen readers hear the current value (conflict 10).
- **Shared code across a boundary is shared, not copied.** The tutor schema and Anthropic renderer compile into both the browser and the proxy; the graders run in the app, the compiler and CI replay; every widget's `logic.ts` and every `scene.ts` import in plain Node.

---

## 7. Security and threat surface

**Threat class C (serving):** the web target's tutor proxy is an endpoint that accepts requests from browsers and spends money against a held API key; the app has no other users and holds only the owner's own study data, and the Artifact's AI calls run on each viewer's own Claude account, so no learner other than the owner exists yet (Class D applies the day another learner is admitted, through the friends board or a public release, and this section is redone at that class before it happens). No deployment is public in this phase: every deployed web build sits behind access control until the owner chooses a content licence (decision 13, default (b)), and making one world-readable is itself a Class D trigger.

### 7.1 Secrets

| Secret | Where it lives | Loading mechanism | Never |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Cloudflare Worker secret (`wrangler secret put`), per environment `dev` and `prod`; local `.env` for the Node proxy; local `.dev.vars` for `wrangler dev` | `env.ANTHROPIC_API_KEY` in the Worker; `process.env` in Node, loaded by `node --env-file=.env` (Node 22's built-in loader, no dotenv package) | In git, the browser, a response, a log line or an error message |
| `TUTOR_TOKEN` (at least 32 random bytes, base64url) | Worker secret and local `.env`; entered once per device in Settings | Bearer header from the browser; on the device in IndexedDB through `KeyValue.setSecret`, never `localStorage` | In git, a URL, a log line |
| `CALL_SIGNING_KEY` (32 random bytes) | Worker secret and local `.env` | Imported once per isolate as an HMAC `CryptoKey`; signs chat call blocks and the assistant blocks of tool turns | Outside the proxy; only signatures travel |
| Eval keys: `ANTHROPIC_API_KEY` (a separate eval key, given a console spend limit of USD 500 a month where the console offers one [recalled, unverified: per-key or per-workspace limits]), an eval-only `TUTOR_TOKEN` and `CALL_SIGNING_KEY` | Local `.env.eval` on the owner's machine only | The eval proxy runs as `node --env-file=.env.eval proxy/dist/node.js`; the eval runner and its judge as `node --env-file=.env.eval tutor/evals/run.ts`; the judge calls Anthropic directly with that key | In CI, in git, in the browser, in any Worker environment; the learning token never works against the eval proxy and the eval token never against `prod` |
| `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | GitHub Actions secrets in a `production` environment that requires the owner's approval | Read only by `proxy.yml` (manual dispatch) for `wrangler deploy`; token scoped to Workers edit on one account | In logs (masked), in any other workflow |
| Web deploy (decision 13) | Default (b), Cloudflare Pages behind Access: `CLOUDFLARE_PAGES_TOKEN`, scoped to Pages edit on the one account, a GitHub Actions secret in the `production` environment (stage 25's development project uses a `preview` environment with its own token); the Access policy admitting only the owner's account is set in the Cloudflare dashboard and holds no secret in the repository. Option (a), GitHub Pages: no stored secret, the official Pages actions with OIDC and `pages: write` | Read only by `pages.yml` | In logs (masked), in any other workflow, or with Workers rights |
| Agents' GitHub identity | A GitHub App installed on the repository with contents and pull-request write and no administration; the platform running the sessions holds its credentials, none sit in the repository | The session environment's GitHub connection | Able to merge into `main`, approve, or apply `visual-approved` (branch protection, `label-guard.yml`). Whether the Claude Code GitHub connection can act as an identity separate from the owner's account is [unverified]; if it cannot, the merge rule is procedural (a `CLAUDE.md` hard rule, and `label-guard.yml` checks the label against the owner's own approval review), stated in section 9 |

- `.gitignore` excludes `.env`, `.env.eval`, `.dev.vars`, `proxy/.state/` and key files from the first commit; `.env.example`, `.env.eval.example` and `.dev.vars.example` list every name with dummy values. At start-up the Node proxy, the Worker (on its first request) and the eval runner check every required variable and fail naming the missing ones, never echoing a value. `VITE_*` variables are inlined into the bundle, so a CI check fails any `VITE_*` name containing `KEY`, `TOKEN` or `SECRET`.
- `gitleaks` scans the full history in CI on every pull request and in the pre-push hook. A secret that ever reaches git history is rotated, not deleted.
- **Recorded waiver** (`docs/DECISIONS.md`): the tutor token is a credential stored in the browser (IndexedDB) because the static web host (decision 13) and the Worker are different sites, which rules out an httpOnly first-party cookie. Compensating controls: the token can only spend on the tutor within the day and month caps; the CSP limits `connect-src` to the app's origin and the proxy; no model output or learner text reaches an HTML sink; rotation is one `wrangler secret put`. Upgrade path for Class D: the proxy as a same-origin Pages function beside the front end and an httpOnly session cookie.

### 7.2 Entry points

Content is trusted (authored, reviewed, built by our CI). Learner text, imported files, remote `db` documents, model output and tool inputs are not.

| Entry point | Origin | Validation (at the boundary, once) | On failure |
|---|---|---|---|
| `POST /v1/tutor` | Any client on the internet | Bearer token (constant-time digest compare); `Origin` exact match against `ALLOWED_ORIGINS`; body at most 256 KB; JSON; `v` is 1; `promptVersion` current or previous; `request` parsed by the shared schema with every byte cap of `AI-TUTOR.md` 4.3 and the sealed and open invariants; unknown fields rejected; earlier chat call blocks must carry a valid HMAC; tool loop at most 3 entries, each entry's assistant blocks carrying the HMAC the proxy issued with its `turn` event (over the call id and the blocks), and each tool result parsed against that tool's output schema with the 4 KB cap | 401, 403, 400, 409 or 429 with a code; nothing sent upstream |
| `GET /v1/health`, `OPTIONS` | Same | Bearer token; CORS preflight answered only for allowed origins | 401; no CORS headers |
| **Learner free text sent to Claude** (chat, typed answers, long-form working, code, outside-work notes quoted in context, official solutions pasted for a real-paper marking pass) | The learner | Browser: schema length caps, paste guard against open assessment items, escaping by the renderer (`<` and `>` to `‹` and `›`, `@@` line starts broken, control characters stripped), wrapping in `<learner_message>`, `<learner_answer>`, `<learner_working>`, `<learner_code>`. Web: the proxy re-validates the whole request and renders the prompt itself with the same escaping, so the trust boundary is the proxy. Trusted per-call context goes in a `role: "system"` message on the web and in tagged blocks in the Artifact | Rejected or truncated with a note; the learner sees the cap |
| Model output (text, act line, structured output, marking lines) | Claude | Act line parsed by a tolerant parser and validated against action schemas (`zod/mini`), ids must exist in `targets()`; leak probe; code guard; output lint; Markdown subset rendered to DOM nodes with `textContent`; URLs removed | Effect dropped and counted; withheld flow on a leak |
| Proxy event stream | Our proxy, over the network | Each event's JSON validated against the event schema (`zod/mini`); unknown event types ignored; `call` and `sig` stored opaque and only sent back | The call ends as `upstream_error`, partial kept |
| Tool inputs from the model (`getScreenState`, `compute`) | Claude | Schema per tool; `compute` expressions through the restricted grammar, never `eval`; results at most 4 KB | Tool error result returned to the model |
| Course bundle, manifest | Own files | SHA-256 against the hash in the name; structural zod schema in the data worker; widget `type@v` registered | Not cached; error screen; never a partial lesson |
| Generator module | Own file, executes as code | Trusted like app chunks: same origin, same pipeline, name pinned by the manifest the page names | Item skipped, logged |
| Third-party modules (Artifact) | cdnjs or jsDelivr, executes as code | Exact-version URLs from `cdn.lock.json` in the page's import map, `integrity` per URL where the browser enforces it [unverified on iOS 18.7]; full URLs without integrity in the data worker; nightly byte comparison against the lock | Load failure rows of section 8.1; nothing runs from a URL not in the lock |
| Route and query parameters | Address bar | `zod/mini` parse per screen | Not found |
| Tutor token typed or pasted in Settings | The owner | Trimmed, then must match `^[A-Za-z0-9_-]{43,}$`; stored only through `KeyValue.setSecret`; never logged, never shown again after saving (the field shows the last four characters) | "That does not look like a tutor token."; nothing stored |
| `version.json` (web) | Own file | `zod/mini` schema (`{ release: string, at: number }`) | Ignored until the next check |
| Handoff payload `?h=` | Link from the Artifact | At most 8 KB; base64url and deflate decode; schema; referenced drill, instance and seed must exist | "This link could not be opened." |
| Progress import, sync file, result code | File or pasted text | At most 64 MB; known `format`, `v` and `kind`; SHA-256 over the canonical JSON; every pack decodes within the output cap; every event passes its schema with string caps; result codes by checksum, schema and matching reference; all in the data worker before anything is written (`ASSESSMENT.md` 14.2, 14.3) | Rejected with the first error; nothing written |
| Events and snapshots from other devices (`db`) | Our writers, stored remotely | Event schema on load; snapshots only as a cache, rebuilt if invalid | Quarantined; "3 records could not be read" |
| `meta/release`, `ops/*` (`db`) | Written by the owner | `zod/mini` shape; a release id only ever raises a notice | Ignored |
| Paste-verify text (`git log`, `pytest -q` output) | The learner | At most 4 KB; parsed by fixed patterns; stored redacted (home paths removed) | "That does not look like the output of …" with the command |
| Learner code | The learner | Executed by design, on the web app only, and only inside the Python or SQL worker: no DOM, no app storage, no network beyond the loader's own files; SQL runs against an in-memory drill database, and the app itself never builds SQL; stdout and stderr capped at 4,000 characters per stream and rendered as text | Soft deadline, watchdog termination, restart once |
| Learner text shown back (notes, board entries, links) | The learner, friends at P2 | Rendered with `textContent` or KaTeX only; links shown as text with their host | |
| Device stores (`KeyValue`, drafts, cache) | This device | Schema per key on read; cache entries by hash | Discarded |
| File picker | The learner | `.json` only, at most 64 MB, decompressed packs capped at 256 MB and 1,000,000 events, parsed in the data worker (`ASSESSMENT.md` 14.2) | Rejected with the first error |

The engine has exactly two raw-HTML sinks: `engine/render/Tex.tsx`, which sets KaTeX output (S1), and `src/ui/bertie/markup.ts`, which parses Bertie's rig from module constants with `DOMParser` (S2). Both are justified in `docs/DECISIONS.md` and enforced by `zq/no-inner-html`, which stage 1 extends from the `innerHTML` family to `DOMParser.prototype.parseFromString` and `Range.prototype.createContextualFragment` outside `markup.ts` (`DECISIONS.md` S2).

### 7.3 Authentication, authorisation and rate limiting

- **Proxy.** One principal: whoever holds `TUTOR_TOKEN`. No per-object authorisation is needed because the proxy stores no objects. The origin allow-list (`ALLOWED_ORIGINS`: the decision-13 web host's origin, `http://localhost:5173`, `http://127.0.0.1:5173`) is defence in depth; the token is the control.
- **Limits per token** (a SQLite-backed Durable Object class keyed by the token digest, pinned in the `wrangler.toml` migrations as `new_sqlite_classes` [recalled, unverified: key name, checked at stage 62]; an in-memory map with a daily file on Node), checked before each request and failing closed. `TutorLimits` is tested in the Workers runtime (`@cloudflare/vitest-pool-workers`, or `wrangler dev` where the pool cannot run it): concurrent requests against one counter, fail-closed behaviour, and day and month rollover; the cost-exhaustion and 100-requests-a-minute attacks run against the deployed `dev` environment at stage 62:

| Limit | Default | Config |
|---|---|---|
| Requests in flight | 2 | `MAX_INFLIGHT` |
| Requests per minute | 20 | `MAX_PER_MINUTE` |
| Requests per day (UTC) | 600 | `MAX_PER_DAY` |
| Spend per day | USD 3 | `MAX_USD_DAY` |
| Spend per month | USD 30 | `MAX_USD_MONTH` |

  Spend is computed from each response's `usage` (summed over fallback iterations at each model's price) with a price table in config; in-flight leases expire after 6 minutes; a client disconnect aborts the upstream stream so a closed tab stops spending. The eval environment (`[env.eval]` in `wrangler.toml`, `.env.eval` for the Node proxy) has its own token and caps: 4 in flight, 60 a minute, 2,000 requests and USD 60 a day, USD 500 a month. The judge's calls go from the eval runner to Anthropic directly, so the runner enforces its own cap of USD 75 a run from each response's `usage` and the same price table.
- **Artifact.** Authentication is the platform's. Authorisation is the `db` rule set of `ASSESSMENT.md` 12.5 plus one `meta` rule: the root is readable at Contributor and writable by the owner; `data/users/{self}` is writable only by that viewer and invisible to every other viewer including the owner; `board/{self}` likewise (P2); `meta` is readable by every admitted viewer and written by the owner. Object-level checks are the `{self}` rules, enforced by the platform and tested in the emulator.
- **Web app.** No server-side objects; nothing to authorise beyond the proxy token.
- **Abuse of the viewer's own `sample` quota** is bounded by the page: at most 2 calls in flight, no automatic retries, automatic modes only after the viewer's first explicit request (consent).

### 7.4 Abuse cases

| Case | What the attacker gets | Control |
|---|---|---|
| The tutor token leaks (device, screenshot, XSS) | Tutor calls until rotated | Spend caps of USD 3 a day and USD 30 a month; requests per minute and day; rotation is one secret put; counts per token in the log show the misuse |
| A script calls the proxy from another site | Nothing without the token; with it, the same as above | Token required; origin allow-list returns 403 with no CORS headers |
| The proxy is used as a general Claude relay | Nothing: the proxy accepts only a typed `TutorRequest` and renders the prompt itself | Schema with caps; unknown fields rejected; no raw system text accepted; signed history blocks; signed tool-turn assistant blocks; tool results validated against each tool's output schema and capped at 4 KB |
| A crafted or replayed chat history block | A forged operator message | HMAC over prompt version, lesson id and block; a block from another lesson or an older prompt fails |
| Prompt injection in learner text, data or code comments | Bertie says something wrong | Escaping and tag wrapping; validated non-destructive actions only; the leak probe; no tool can write; the grader never reads tutor output; marking needs verbatim evidence, and in a gate Bertie's mark can only lower the learner's |
| The eval key or token leaks from the owner's machine | Spend until rotated | Eval caps of USD 60 a day and USD 500 a month; the eval proxy binds 127.0.0.1 only; the eval token works only there; rotation as section 8.6 |
| Cost exhaustion through long requests | Spend | 256 KB body cap, per-field caps, `max_tokens` per mode, spend checked before every request, disconnect aborts upstream |
| A malicious import file or handoff link | Corrupt progress or script execution | Validated in the data worker against schemas and hashes, written only after full validation, rendered as text |
| XSS through content or model output | Token theft | Two raw-HTML sinks: KaTeX output (strict mode, two trust settings) and Bertie's constant rig markup; Markdown subset to DOM nodes; lint bans other sinks; on the web, our CSP blocks inline script and every outside host but the proxy; the Artifact holds no tutor token |
| A compromised dependency | Code in the bundle | Exact pins, lockfile, audit gates, licence allow-list, new dependencies need approval |
| A CDN serves altered bytes for a pinned file (Artifact) | Script in the page: it could read the viewer's progress, write their `db` subtree and call `sample` on their account, but the host's CSP lets it reach no host beyond the listed CDNs [inferred] | Import-map `integrity` refuses altered bytes where enforced; exact-version URLs; the nightly drift check; worker imports and unenforced integrity are a residual risk, recorded as a waiver in `DECISIONS.md`; the web app bundles and is not exposed |
| A friend with Editor access (P2) | Could republish the app | Stated in `ASSESSMENT.md` 15.5: invite as Editor only people trusted with the app; `db` rules still keep each subtree private |

### 7.5 Data held

| Category | Where it rests | Encryption | Retention |
|---|---|---|---|
| Learning record (attempts, answers, code, long-form text, timings, marks, cards), outside work, interview transcripts (text only), settings, tutor records | IndexedDB on the device; in the Artifact also the viewer's private `db` subtree on claude.ai unless device-only mode is on | TLS in transit everywhere; at rest, the device's storage encryption [recalled: iOS data protection] and the platform's storage [unverified: claude.ai encryption at rest for artifact data] | Until the learner deletes it ("Delete my progress", typed confirmation, every document deleted one by one) or the Artifact is deleted; the release process never deletes the Artifact |
| Proxy counters | Durable Object storage or `proxy/.state/limits.json` | Platform-managed [recalled, unverified]; local file on the owner's machine | Daily counters 35 days, monthly 13 months |
| Proxy logs | Workers observability | Platform-managed | Counts only, shortest retention available [unverified: exact setting fixed in stage 62] |
| Request content at Anthropic | While processed | TLS | Anthropic's API data policy [recalled, unverified: check before the proxy goes live] |
| Friends board entry (P2, opt-in) | `board/<uid>` | As `db` | Until opt-out or deletion |

Held nowhere: email addresses, names (resolved at render from `user.profiles()`), location, analytics, third-party trackers. No personal data in the repository, fixtures or tests: every fixture comes from the synthetic learner generator, and a tutor eval fixture taken from a real reply is redacted before commit (section 5.1).

### 7.6 Supply chain and publication hygiene

- Exact pins and a committed lockfile; a new dependency needs the owner's approval and a note (maintained, last release, licence) in `DECISIONS.md`.
- `npm audit` and `pip-audit` in CI nightly and in the pre-push gate; critical advisories fixed within a week or waived in `DECISIONS.md`.
- A licence allow-list checked in CI: MIT, ISC, BSD, Apache-2.0, MPL-2.0 and OFL (fonts) for shipped runtime dependencies; development tools may also be 0BSD, BlueOak-1.0.0, CC0-1.0, CC-BY-4.0 (`caniuse-lite`) or Python-2.0 [recalled: the licences common in a Vite and ESLint tree]; any further exception is listed in `DECISIONS.md`.
- **Merge rights.** `main` is protected: a pull request into it merges only with an approving review from the owner's account, which `.github/CODEOWNERS` names for every path, and only the owner merges it. `stage/*` branches are protected too: a pull request into one merges only with CI green and the adversarial (and, for content, semantic) review recorded, and the agents' GitHub App (bot) identity may merge it there, never into `main`. The bot cannot approve its own pull requests; the workflow `label-guard.yml` fails a pull request whose `visual-approved` label was applied by any account but the owner's.
- Pyodide wheels checked against `pyodide-lock.json` SHA-256 before the web build copies them. **CDN pinning in the Artifact** (`ARCHITECTURE.md` decision 24): every third-party file it loads is in `cdn.lock.json` with an exact-version URL and its SHA-384, generated from `package-lock.json`, so both targets run the same versions; the import map carries `integrity` for every entry, but subresource integrity may not be available for every CDN script (iOS 18.7's support for import-map integrity is [unverified], and worker imports have none), so a nightly job refetches every locked URL and fails on any byte change; `provenance.ts` fails a build that would publish a `node_modules` module. The web app loads nothing from a CDN.
- The repository is private [measured, GitHub REST API, 7 October 2026]. Its code carries the MIT licence from stage 1; the content licence waits for the owner (decision 8, `STATE.md` open question 18), and the repository is not made public before it. CI runs on every push, with a status badge that only the repository's collaborators can see; the Phase 3 pre-push gate of the engineering floor includes the manual attack pass against the proxy.

### 7.7 Blocks skipped

None: Class C makes every block mandatory. Two engineering-floor items do not apply and are stated, not waived: password hashing (no passwords exist) and session cookies (no sessions; the token waiver in 7.1 covers the stored credential).

---

## 8. Failure modes and operations

### 8.1 External interactions

**Timeouts** [our choice; added by this plan]: every own-file fetch carries `AbortSignal.timeout`, 20 s for the manifest and course bundles and 120 s for each Python package on the web, and a timeout counts as a failed fetch under its row; a Python load that reports no `progress` for 30 s is terminated and reported as `failed: network`; the proxy sends a `ping` event every 15 s while its upstream is open, and the browser treats 45 s without any event as a dropped connection (`upstream_error`, partial kept). Tutor calls have no other timeout: captions at 8 s and 60 s and the Stop button cover long thinking (`AI-TUTOR.md` 7.4), and the proxy's in-flight lease (6 minutes) bounds a stuck upstream.

| Interaction | Failure | Behaviour | Retry | What the learner sees; state left behind |
|---|---|---|---|---|
| Content manifest at boot | Fetch fails | Retry, then error screen | 1 retry | "Could not start Zero to Quant. Check the connection and try again." with Retry; on the web the service worker serves it offline |
| Course bundle | Fetch fails; hash mismatch; schema fails; unknown format major | Refetch once with a cache-busting query on mismatch; never cache an invalid bundle | 1 retry after 1 s | "Could not load this course" with Retry, or "Update the app to open this course"; other courses keep working |
| Lazy chunk import | Fails (usually a stale page after a release) | | 1 retry | "A new version is available. Reload to continue." |
| Generator module or a generator | Import fails; throws | Item skipped; the set draws the next seed; logged with generator, version, seed | none | Next item |
| Widget render or logic | Throws | Widget error boundary | none | "This part of the screen failed. Skip this screen" (result `read`); logged with type and version, never state |
| Third-party modules at boot (Artifact: Preact, signals, `zod/mini`, `idb`, `ts-fsrs`) | A CDN unreachable, a 404, or bytes that fail the import map's integrity | The bootstrap's `import()` of the entry rejects; it retries once after 2 s and never falls back to a URL outside `cdn.lock.json`; logged as `cdn-network` or `cdn-integrity` | 1 | "Zero to Quant could not load part of itself. Check the connection and try again." with Retry and the web app's address; nothing written, progress untouched |
| Lazy third-party module (Artifact: KaTeX, the Compute Engine parser, MiniSearch) | Same | As the web chunks below: maths shows its TeX source; expression screens keep Check disabled with "Maths checking could not load" and Retry; search says it could not load | 1 retry on tap | Other screens keep working |
| The data worker's modules (Artifact: classic zod, ts-fsrs, fflate) | Fail to load | The worker reports `failed: dependency` and restarts once; a course bundle whose SHA-256 matches its name opens without the structural check (it is the bytes CI validated), logged; imports, sync files and result codes wait, because they are untrusted | restart once | "Importing needs a part of the app that could not load. Try again later."; lessons keep working |
| KaTeX chunk (web) | Fails | TeX source shown in code style | 1 retry on tap | Retry in the verdict area |
| MathLive (web) | Fails | The plain field with the symbol bar and a live preview, which the Artifact always uses; grading unchanged | 1 retry | Plainer input |
| Google Fonts (Artifact) | Unreachable | System font stacks | | Different typeface |
| Any Python, SQL or C++ drill (Artifact) | No runtime, by the publishing rule | `available()` answers `not-in-this-build` | | Handoff link and result code |
| Pyodide core (web) | Network | `failed: network`; nothing cached half-written | Learner's Retry | "Python could not download. Check the connection and try again." Check stays disabled (`blocked: python-failed`) |
| Python first download (web) | Not cached | Never starts on its own: the title screen offers "Download it now (14 MB)?", the size computed from the manifest's sizes of the groups the drill's `needs` require that are not yet cached (13.5 MB for core and `stdlib`, 21 MB with `numpy-pandas`) | | Nothing downloads before the tap |
| Learner code | Infinite loop in Python bytecode | The soft deadline is checked every 1,000 backward jumps; past it, `ZqTimeout` (a `BaseException` that `except Exception` cannot swallow) ends the test | | That test reports `timeout`; the next runs at once (within 500 ms) |
| Learner code | Long call inside C | Watchdog: no event within the limit plus 1,500 ms terminates the worker, reports `timeout`, restarts warm from the service worker cache | restart once | `timeout`; worker ready again in about 3 to 4 s on the iPhone |
| Python worker (web) | Memory or crash | Restart once; second failure sets `failed: memory` or `crashed` | 1 | "This drill needs more memory than this device has. Open it on a computer."; the attempt stays open |
| Python packages (web) | `loadPackage` fails on the network or integrity check | As the core: `failed: network` or `integrity`; the service worker cache is checked first | Learner's Retry | Same copy as the core |
| SQLite worker (web) | Fails | "SQL could not start in this browser"; authored query replays still show | Learner's Retry | The drill stays open |
| `sample` (Artifact) | `null` capability, `not_granted`, `sampling_disabled`, `capability_*` | Hide every AI surface for the view | never from code | Authored hints and Show solution remain |
| `sample` | `rate_limited`, `upstream_error` or unknown, `empty_completion`, `invalid_json`, `refused`, `prompt_too_large`, `session_expired`, `tools_unavailable` | Per `AI-TUTOR.md` 6.4: keep the partial marked interrupted, or clear it, or drop tools for later calls | never from code; Try again is the learner's | Error copy of `AI-TUTOR.md` 7.5 |
| Proxy, browser side | Offline; 401; 409; 429 rate or budget; `upstream_error` mid-stream; `refused`; 400 | Codes `offline`, `auth_failed`, `version_mismatch`, `rate_limited`, `budget_exhausted`, `upstream_error`, `refused`, `invalid_request` | never automatic | Settings prompt, "Reload to update", which cap and when it resets, partial kept as interrupted |
| Proxy, server side | Upstream 429, 529 or 5xx before streaming | SDK retries with backoff | 2 | After retries: `rate_limited` or `upstream_error` |
| Proxy, server side | Failure after streaming starts; `refusal` without fallback; `max_tokens`; Durable Object down; signature fails; client disconnect | No retry (it would duplicate text); partial discarded on refusal; fail closed 503 on the Durable Object; 400 and a fresh thread on a bad signature; upstream aborted on disconnect | none | As `AI-TUTOR.md` 6.3.8 |
| `db` (Artifact) | `unavailable` | Events stay in the IndexedDB outbox | 1 retry after 0.5 to 1.5 s, then 2, 4, 8 s up to 60 s, indefinitely while open | "Saved on this device" chip until the outbox empties |
| `db` | `resource_exhausted` | Double the write-coalescing interval up to 60 s | | None |
| `db` | `quota_exceeded` | Stop creating documents; keep the open chunk | | "Your progress store is full" with Export and the checkpoint option |
| `db` | `invalid_argument` | Programming error: keep events in the outbox, record locally | | "Could not save. Export your progress now." |
| `db`, `user` | Absent, revoked, no write access | `IdbStore` alone | | "Progress is saved in this browser only. Export it regularly." |
| IndexedDB | Unavailable or full | `MemoryStore` for progress; memory for caches and drafts | | "Nothing will be kept after this tab closes" with Export |
| Web Locks | Absent | `localStorage` heartbeat lease of 10 s | | Second tab read-only with "Use here" |
| `version.json` | Fetch fails | Ignored; tried again at the next visibility change, at most hourly | | None |
| `meta/release` | `db` absent or subscription ends | `version.json` polling at visibility changes, at most hourly | | Update notice on Today, never inside a lesson or paper |
| Offline, web | No network | Service worker serves the app, cached courses and Python; tutor hidden (`offline`); events in IndexedDB | | Courses marked "Keep offline" work fully |
| Offline, Artifact | No network | No offline mode: a cold start needs the network. Mid-session, loaded and cached courses continue; events wait in the outbox; the tutor shows `upstream_error` | | "Saved on this device" chip |
| Keep offline (web) | Cache storage quota refused | The course stays online-only; nothing partial is kept | | "Not enough space to keep this course offline." |
| Persistent storage (web) | `navigator.storage.persist()` refused | The app works; eviction is possible | | The weekly review reminds the learner to export |
| Service worker (web) | Registration fails; update waiting | App works online; update applies only on Restart or the next cold start | | "Offline use is unavailable in this browser."; "An update is ready. Restart to use it." |
| `downloads` capability | Absent or refused | Copy to clipboard for exports under 1 MB | | Says so for larger files |
| File picker (Artifact) | Not available in the frame | Paste instead | | Paste box |
| Clipboard | Write refused | Text shown selected in a sheet | | "Copy it from here" |
| Handoff link | Cannot leave the Artifact frame | Copy button with the link text | | Copyable link |
| Artifact publish (release session) | Live file listing differs from the previous release's committed ledger; a file's SHA-256 differs from the new ledger; a batch is refused; peak over limit; the session dies mid-release | Stop before the first publish; never force; maintenance release for the peak; a new session resumes from the first step whose effect is not yet visible in the listing or in `meta/release` (section 8.6) | none automatic | Live page unchanged until the page publish; owner runs Self-test |
| Pages deploy, Worker deploy | Fail | Previous deployment stays live | manual | None |
| Eval run (owner's machine) | The eval caps are reached, the judge errors, or the network drops mid-run | The run stops at the failing scenario, writes a partial report marked incomplete, and `--resume` continues from the next scenario; a partial run never becomes a baseline | none automatic | Not learner-facing |
| Preview Artifact (sessions) | A publish is refused as a conflict; `ops/gate-<stage>` is absent when a session reads it | Re-read the live version and republish only if the gate shown is the session's own; an absent record means the gate is still open, and the session waits | none automatic | The owner sees one gate at a time |
| AudioContext | Blocked | Sound unavailable | | Settings explains why |

**Writes that cross a network are idempotent**: `db` chunk writes carry their own `seqFrom` and `seqTo` and readers deduplicate by event id; imports are union merges keyed by event id; Artifact publishes are content-addressed, so re-sending a batch changes nothing. Tutor calls are not idempotent (they spend), which is why nothing retries them automatically.

### 8.2 Error-handling policy

- Nothing is swallowed: `zq/no-empty-catch` fails any `catch` that neither rethrows nor logs.
- Learner-facing copy comes from `copy.ts` files and `AI-TUTOR.md` 7.5, in British English, and never contains stack traces, paths, query text, status codes or model names. Internal detail goes to the local log.
- Error boundaries at three levels: widget (skip the screen), screen (back to Today), app (reload with Copy diagnostics).
- A capability or runtime that is absent is a designed state, not an error (design for absence).

### 8.3 Config

- **Build time:** `VITE_BASE`, `VITE_ZQ_TUTOR_URL`, `VITE_ZQ_WEB_APP_URL` from `.env` (ignored) with `.env.example` committed; none secret.
- **Feature flags and tunables:** `src/app/config.ts` only, typed defaults per target: `tutor.answerKey`, `friendsBoard`, `devRoutes`, Python time limits (web), cache caps. The Artifact's lack of Python is not a flag: its `PythonRuntime` is the handoff stub by construction. Learning tunables (retention tiers, pass marks, cool-downs, XP rules) are content or rules data with versions, never literals in screens.
- **Proxy:** `wrangler.toml` `[env.dev]`, `[env.prod]` and `[env.eval]` with separate secrets, caps, origins and `MODEL`; `wrangler dev` reads local secrets from `.dev.vars`; the Node variant reads the same names from the environment, started as `npm run proxy:local` (`node --env-file=.env proxy/dist/node.js`) or `npm run proxy:eval` (`node --env-file=.env.eval ...`).
- **Environments:** development (dev server, local proxy, fake or recorded tutor), eval (the local proxy with `.env.eval` and the judge), preview (the one long-lived preview Artifact, republished by a session for each device gate with dev routes compiled in and the gallery or a course as its start route; its URL is in `STATE.md`; nothing else is published for previews, so no preview needs deleting), production (the live Artifact and Pages).

### 8.4 Logging

- **App:** `app/log.ts`, structured entries (time, level, module, message, ids: content ids, widget type and version, error codes, release); 500 in memory and the last 2,000 in IndexedDB. Never logged: answers, code, long-form text, chat, tutor replies, tokens, viewer ids. Nothing leaves the device; Settings, Diagnostics offers Copy diagnostics and Self-test.
- **Proxy:** one JSON line per request with counts only (day, mode, status, stop reason, tokens in and out, cache reads and writes, spend, milliseconds, fallback flag). Never: request or response text, learner messages, the token or its digest, IP addresses, headers. Enough to answer "what happened at time T" for spend and errors.

### 8.5 Concurrency and shared state

| Thread | Owns | Talks through |
|---|---|---|
| Main | Rendering, signal stores, widget state, the player, non-code grading, the single-event fold, the append queue | Typed RPC to workers; `ProgressStore` |
| Data worker (one) | Bundle validation, full and late-event re-folds, search, export, import | Messages; transferred buffers |
| Python worker (web, at most one) | Pyodide and loaded packages | Messages; terminated on timeout, idle 10 minutes, or leaving a course |
| SQL worker (web, at most one) | SQLite | Messages |
| Service worker (web) | Caches | `workbox-window` |
| Proxy | Stateless per request; the Durable Object serialises its counters | |

- **No shared mutable state crosses a thread:** workers receive copies or transferred buffers. On the main thread, each widget instance's state is one signal written only by its `WidgetApi` and by the host; progress events pass through one `AppendQueue` (a promise chain that assigns `seq`, folds the event, then persists), and only the writer tab, elected by the Web Lock `zq-writer`, appends. A late event triggers a re-fold in the data worker; the main thread swaps the derived state in one assignment.
- **IndexedDB:** `BlobCache` is written by the main thread only (bundles, generator modules), and each IndexedDB transaction serialises its own writes; on the web, Python files live in the service worker's cache; `KeyValue` writes from any tab are last-writer-wins and hold only device preferences, never progress.
- **Proxy:** stateless per request; the Durable Object serialises its counter updates; the Node variant updates its in-memory counters synchronously on one event loop.
- **`db`:** every document has one writing device; each write awaits the previous write to the same document; drafts use 60-second leases renewed every 20 s.
- **The preview Artifact** is shared by the four sessions. One gate shows at a time: a session republishes it only when the gate currently shown has its `ops/gate-<stage>` record; the queue of waiting gates lives in `STATE.md`, and the Artifact tool's conflict refusal catches a race.
- **Bounded resources:** tutor calls at most 2 in flight; one Python and one SQL worker; `BlobCache` least-recently-used beyond 300 MB or 60% of quota; log ring buffers 500 and 2,000; `db` subscriptions at most 4 device queries before falling back to a 60 s refresh. One unbounded path, accepted and listed in section 9: the outbox, bounded only by the device's storage quota.

### 8.6 Operations

- **Web release.** A `v*` tag runs the release job (every CI gate, two clean builds with identical hashes, the Artifact publish-plan dry run) and `pages.yml` deploys to the decision-13 host (default: Cloudflare Pages behind Access). Rollback: run `pages.yml` on the previous tag; the service worker picks it up on the next Restart.
- **Artifact release.** The release pull request commits `releases/<release>.json`, the ledger CI built from the tagged commit (every published path with its SHA-256 and size, the page hash, the manifest name). A Claude session then (1) rebuilds every file itself from the tag with the hash-pinned inputs (`package-lock.json`, `cdn.lock.json`) and checks each file's SHA-256 against the ledger, so it publishes only bytes it built from the repository's own sources and verified; no published file is third-party code or a binary (section 4.3); (2) reads in full every text file it writes by hand or that no reviewed source produced (the page fragment, `version.json`, the publish plan); (3) lists the live files and compares them with the previous ledger, stopping on any drift; (4) publishes content first (re-sending the live page), then the new page, writes `meta/release` (`{ release, at, ledger: <SHA-256> }`), then garbage-collects every path that neither the new ledger nor the previous one names. **Resume:** a session that dies mid-release is replaced by one that re-runs from the first step whose effect is not yet visible in the file listing or in `meta/release`; every step is idempotent because publishes are content-addressed. The owner runs Self-test on the iPhone and the session reads `ops/selftest-<release>`. Rollback: publish the previous ledger's page and files, which the retained version still holds. The Artifact is never deleted, because deleting it erases every learner's `db` store.
- **Proxy release.** `proxy.yml` on manual dispatch with the owner's approval of the `production` environment; `wrangler rollback` restores the previous version.
- **Secret rotation.** `TUTOR_TOKEN` and `CALL_SIGNING_KEY`: `wrangler secret put`, then re-enter the token on each device (open chat threads restart with a summary). `ANTHROPIC_API_KEY`: create a new key in the Anthropic console, put it, revoke the old one. Eval secrets: regenerate the values in `.env.eval` and revoke the old eval key. Any secret that reaches git history is rotated the same day.
- **Dependency upkeep.** A monthly upgrade pull request within majors with the full nightly suite, which regenerates `cdn.lock.json` with `package-lock.json`; majors (TypeScript 7, Pyodide) in their own pull request with `DECISIONS.md` notes; Pyodide moves only with the content pin, re-running every drill and recorded output. A nightly drift failure (a locked CDN file changed) blocks Artifact releases until the file is re-pinned or the version moved.
- **Learner data.** The weekly review reminds the learner to export a backup; restore is an import on either target. "Delete my progress" is the only deletion path.
- **Tutor evals.** Run locally only, through the eval environment: a full run before any prompt, renderer or model change; the course subset at each course milestone; the judged Artifact tier run before each tutor-changing Artifact release (`AI-TUTOR.md` 9.6). CI and nightly run only the deterministic graders over recorded replies, with no key.
- **When something breaks.** The owner copies diagnostics from Settings into a session; the log carries ids and codes only. A failed Self-test blocks the release checklist until fixed or rolled back.

---

## 9. Limitations and trade-offs

- **The app trails its only learner, by the owner's choice.** The owner is the learner; at 15 hours a week he finishes Stage 0 in about 9 months and reaches 1.5 in about 20, while library-first building at four parallel sessions delivers Stage 0 content in about 15 months and meets the learner in 1.5 around November 2028 (section 11.2). The owner chose this order at review (decision 1(a)); the stage 28 re-forecast lever still applies.
- **The path is longer than its headline.** 3,390 mapped hours (3,450 on the researcher and ML research tracks) become about 4,180 (4,260) at 15 hours a week once the Daily 10, the weekly problems, maintenance review and retention sittings are counted: 5.4 years with no weeks off, 6.1 years at 46 study weeks a year (5.5 and 6.2) (section 12, duration table).
- **The Artifact cannot work offline.** No service worker on the host: a cold start needs the network, and a long offline spell means the web app.
- **No Python, SQL or C++ in the Artifact, so every drill opens the web app.** The publishing rule (section 4.3) keeps third-party binaries out of the Artifact. In Stage 0 that means the web app about once a level for homework and for the 0.4 course Y lessons with live code; 1.1, 1.2 and 1.9 are best studied in the web app; a paper with a code item is sat there. Lessons, quizzes and every non-code item play in the Artifact, and results return by result code or sync file.
- **The Artifact depends on two CDNs.** If cdnjs and jsDelivr cannot serve a locked file, the Artifact cannot start (section 8.1); the web app is the fallback. Import-map integrity may not be enforced on every browser and worker imports carry none: a residual supply-chain risk, bounded by exact versions, the nightly drift check and the host's CSP (section 7.6).
- **Maths in the Artifact is MathML in system fonts.** It may look less polished than KaTeX's HTML output on the web, and there is no MathLive there; spike S1 judges it on the owner's iPhone.
- **Phone memory, not file size, limits Python in the web app on a phone.** Pandas with SciPy or scikit-learn in one worker may exhaust an iPhone's memory; those drills then need the web app on a computer. Measured per group at stage 25; older phones are not measured.
- **A long C-level call costs a worker restart** of about 3 to 4 s, because the design does not rely on the cross-origin isolation headers Pyodide's interrupt buffer needs: GitHub Pages cannot send them, and decision 13's hosts are kept interchangeable.
- **The tutor token is a credential in browser storage.** Written down as a waiver with compensating controls (section 7.1); an XSS on our origin could read it, capped by the spend limits.
- **The leak probe does not cover every answer type.** Curves, predicates, states and long-form answers rely on instruction and evals alone; a determined learner can also rephrase past the paste guard, and a second device has no lockout. The app calls these honesty aids, not proctoring. The method-comment channel before a Check is closed by rule (Bertie comments on nothing typed) and tested by paired evals, not by the probe.
- **Quick-tier tutor replies can be wrong.** The Artifact's tiers are models the platform chooses; the judged Artifact tier run gates them per tier, and a failing tier loses the sealed key, then moves to the default tier, then falls back to authored rungs (`AI-TUTOR.md` 9.6).
- **The judge is a model.** It runs on `claude-sonnet-5-5`, a different and cheaper model than the tutor's, and the owner hand-grades 30 sampled replies per release; a weaker judge can miss what a stronger tutor gets subtly wrong, which is why a failed calibration moves it to `claude-fable-5-1`, and a shared blind spot between two models remains possible.
- **Device clocks order events.** A wrong clock can misplace events in a study day; there is no server clock to correct it.
- **The outbox is unbounded** apart from the device's quota, so months offline fit, but a full disk stops saving with a visible message.
- **The `db` database's total size cap is unknown** until stage 2's bounded probe; the checkpoint fallback (freeze a snapshot, export old packs) is specified and built only if the probe shows a cap below 34 MB times the expected number of participants.
- **The emulator is not the host.** It encodes the contracts and the spikes; differences in the real host surface only in the release Self-test on the owner's phone.
- **Scenes trade flexibility for consistency.** A widget that needs an interaction no primitive offers must become bespoke; the four pilots in stage 14 test the bet before 131 composites rely on it.
- **Effort estimates are estimates.** Agent build time per size class is unmeasured until the first pull requests record it; AD is recorded per pull request from stage 1, the plan carries a 40% contingency on stages 11 to 58 and the service stages, and every batch gate re-forecasts.
- **The owner cannot check maths he has not learned.** The semantic check that the English means what the maths computes rests on an independent reviewer agent's restatement of every lesson, verified by `zqverify`, and from Stage 1 on a paid human spot check of five lessons per course; the owner judges the learning experience per level. Two agents can still share a misreading.
- **Sync between the two targets is manual**: a sync file of about 40 KB a week, or a result code per handed-off attempt or live-code screen; there is no server to sync through.
- **The web app needs an Access sign-in on each device** (decision 13, default (b)) until a content licence allows a public site; the Access session lifetime is a Cloudflare setting, and whether an expired session interferes with the service worker's update checks is [unverified] until stage 82.
- **iOS may evict web-app storage** after a period without use [recalled]; the persistence request and export reminders mitigate it, and the Artifact's `db` copy is the durable record for Artifact users.
- **Long-form marks rest on two models of one learner's work.** A gate counts the lower of the learner's blind mark and Bertie's; a person marks one finals-style sitting per Stage 1 maths topic. Between those points no human examiner reads the proofs.
- **ML-lab-calibre thinking is taught at toy scale.** The adopted 2.1b (deep learning core), 2.2c (research method), 2.0a and 2.0b carry the aim with 3.1; widget models stay below about 5,000 parameters and run in `ml-core` on both targets; drills train in NumPy on the web app, and nothing in the app trains on a GPU.
- **Merge rights may be procedural.** If the session platform cannot give agents a GitHub identity separate from the owner's, branch protection cannot tell an agent's merge from the owner's; the rule then rests on `CLAUDE.md` and on the owner's approval review, which `label-guard.yml` checks.
- **No telemetry** means problems are found only through Copy diagnostics and the owner's own use.
- **What a production version would do differently:** a same-origin backend with sessions instead of a bearer token, server-side sync between targets, a hosted Python sandbox so that drills run on every target, telemetry with consent, and human examiners for gated long-form work.

---

## 10. Repository structure

```
zero-to-quant/                              [npm workspaces root]
├── package.json  package-lock.json         workspaces, scripts, engines, exact pins; lockfile committed
├── cdn.lock.json                           generated from package-lock.json: every third-party file the Artifact loads (URL, SHA-384, kind)
├── .nvmrc  .npmrc                          22.22.0; save-exact=true, engine-strict=true
├── tsconfig.base.json                      strict, noUncheckedIndexedAccess, exactOptionalPropertyTypes; project references
├── vite.config.ts  vitest.config.ts  playwright.config.ts   one Vite config, three modes; test projects
├── eslint.config.js  .prettierrc  .stylelintrc.json  knip.json  lefthook.yml  .size-limit.json  .gitleaks.toml
├── .env.example  .env.eval.example  .dev.vars.example   every variable name with dummy values (app, proxy, eval, wrangler dev)
├── .gitignore                              node_modules, dist, .zq/, .env, .env.eval, .dev.vars, proxy/.state, test-results, prototype/vendor/pyodide
├── LICENSE                                 MIT
├── README.md                               getting started, both targets, limitations (from section 9)
├── CLAUDE.md  STATE.md                     Phase 2 protocol and hard rules; stage tracker (with the preview Artifact's URL)
├── releases/                               <release>.json ledgers, one per Artifact release (section 8.6)
├── .github/
│   ├── CODEOWNERS                          the owner's account on every path
│   ├── workflows/ci.yml                    pull-request gates: static, unit, widgets, content, build, e2e, visual, perf, gitleaks
│   ├── workflows/nightly.yml               full visual, cross-browser, full verify with Monte Carlo, audits, licences, deterministic tutor graders over recorded replies (no key)
│   ├── workflows/label-guard.yml           fails a pull request whose visual-approved label was not applied by the owner
│   ├── workflows/pages.yml                 tag v*: full gate, build web, deploy to the decision-13 web host
│   ├── workflows/proxy.yml                 manual: deploy the Worker to the production environment
│   └── pull_request_template.md            contract items, three input paths, budgets with numbers, Describe text quoted
├── docs/
│   ├── PLAN.md                             this blueprint
│   ├── ARCHITECTURE.md  WIDGETS.md  CONTENT-FORMAT.md  AI-TUTOR.md  ASSESSMENT.md  BERTIE.md  CURRICULUM.md   appendices
│   ├── DECISIONS.md                        decisions made in Phase 2, waivers, raw-HTML sink justifications, spike results
│   ├── curriculum.md  curriculum/*.md      the owner's curriculum and the fifteen item files
│   ├── design-research.md                  the Brilliant recreation spec
│   ├── engine/WIDGET-AUTHORING.md          agent-facing widget and scene authoring guide (stages 10b and 14)
│   ├── engine/RELEASE.md                   Artifact release checklist (stage 83)
│   └── blueprint/work/                     working papers (history) and canon-gap.md
├── content/                                [YAML, ZQ Markdown, TypeScript, Python]
│   ├── AUTHORING.md                        the agent-facing content guide (stage 7)
│   ├── curriculum.yaml  plan.yaml  sources.yaml  tex-macros.yaml  migrations.yaml  ids.lock.json
│   ├── <topic>/<course>/<level>/<lesson>.yaml
│   ├── <topic>/library/                    skills, misconceptions, items, sets, exams, drills (with tests.py and data), glossary, cards
│   └── generators/<topic>/                 <gen>.ts, <gen>.yaml, <gen>.verify.py, goldens
├── packages/                               [TypeScript]  contracts, mathcore, models, content-schema, content-compiler,
│                                           graders, gen-kit, eslint-plugin-zq (section 3.1)
├── src/                                    [TypeScript, TSX, CSS Modules]  section 3.1; every file in ARCHITECTURE.md 4.2
│   └── html/web.html  html/artifact.html   the two page heads (CSP meta and manifest on the web; Google Fonts and the import map in the Artifact)
├── proxy/                                  [TypeScript]  src/, wrangler.toml (no secrets), .env.example, test/
├── tools/                                  [TypeScript, Python]  zq, zqverify, pyvendor (web), cdn, release, artifact-host, perf, scaffold, registry;
│                                           py/ (pyproject.toml and uv.lock: CPython 3.12 CI packages pinned to Pyodide's versions)
├── tests/
│   ├── e2e/                                Playwright specs on both targets (ARCHITECTURE.md 8.1.2)
│   ├── visual/                             screenshot specs; baselines.lock.json (hashes); images on the visual-baselines branch
│   ├── perf/                               per-widget drag, start-up, fold rebuild
│   ├── fixtures/learners/  fixtures/events/   synthetic learner logs per release; one file per event version
│   └── synthetic/                          the whole-path synthetic learner generator (about 121,000 events)
├── prototype/  spikes/                     Stage 1 mockups and platform spikes; read-only references
└── dist/                                   build output, ignored: web/, artifact/, preview/, content/
```

---

## 11. Execution stages

### 11.1 Rules for every stage

- **One stage, one gate, one stage branch.** Every pull request of a stage merges into `stage/<n>`; the owner reviews the stage as a whole on that branch, and it reaches `main` only on the owner's approval, so a rejected gate is fixed on the branch or the branch is dropped and `main` never needs a revert. Content gates are levels (section 11.6): a level's pull requests merge into `stage/<course>/<level>`.
- **Pull requests.** Code: one module, widget, scene group (at most three scenes) or service per pull request, at most about 800 changed lines excluding fixtures and baselines. Content: one lesson plus its library entries per pull request, with no line cap on YAML; generators with their Python twins and goldens in pull requests of their own. Each has a self-review and an adversarial review by a second agent session; content adds the semantic review of section 11.6. Every pull request records its session hours and tokens.
- **Every definition of done includes**, beyond the tests named in its row: CI green (static, unit with the coverage floors of `ARCHITECTURE.md` 8.3, widget contract suite, build of both targets within budgets, end to end for touched flows, changed visual baselines approved by the owner's `visual-approved` label, performance for touched widgets); contracts in `ARCHITECTURE.md` updated if they changed; `DECISIONS.md` entries for any decision made; `STATE.md` updated; every `[unverified]` item the stage was meant to close, closed.
- **Security work sits in the stage that creates the exposure** (named in the rows).
- **Merge rights.** Only the owner's account approves and merges into `main` (`CODEOWNERS`); agents, through a GitHub App identity, merge reviewed pull requests into `stage/*` branches only and never apply `visual-approved` (section 7.6). The owner therefore reviews each stage or level as a whole, not each diff.
- **Parallel sessions.** Four sessions from stage 3a (section 11.2) run stages whose dependencies are approved; the stage numbers give the review order.
- **Hardware the owner holds:** stages whose definition of done names the owner's iPhone (2, 25, 59, 82, 83, 84, every widget batch and every level gate) are closed by the owner on the device. From stage 25 a session republishes the one long-lived preview Artifact (`zq preview --artifact`, with the gallery or a course as its start route) for the gate, and the owner records the result in its `db` at `ops/gate-<stage>`, which the session reads with ArtifactData. Stage 2 uses its own probe Artifacts; stage 9a's on-device timing is taken at stage 25. A batch whose widgets run on `PythonRuntime` or `SqlRuntime` is also checked in the web app on the iPhone, through stage 25's development deploy (11.4).

**Appendix stage names**, for tracing each row to its source: engine E0 is stages 1 and 2, E1 is 3 (its numerics are 3a and 3b), E2 is 4, E3 is 5 (Bertie moves to 59), E4 is 10a to 19, E5 is 23, E6 is 9 and 24, E7 is 74a and 74b, E8 is 25 and 26, E9 is 82, E10 is 83; the services of `WIDGETS.md` 3 are 3a to 3g; content C1 is 6, C2 is 7, C3 is 20, C4 is 21, C5 is 8, C6 is 22, C7 is 26, C8 is 23, C9 is 24, C10 is 66, C11 is 84; tutor T0 and T1 are 60, T2 is 61, T3 is 62, T4 is 63, T5 is 64, T6a is 65, T6b is 66, T7 and T8 are 67; assessment A1 is 9a, A2 is 69, A3 is 70, A4 is 71, A5 is 72, A6 is 73, A7 is 75, A8 is 76, A9 is 77, A10 is 78, A11 is 79, A12 and A13 are 80, A14 is 71 for the ghost race (the friends board is P2), A15 is 81 (the FSRS optimiser is P1); the widget waves of `WIDGETS.md` 7 are stages 11 to 19 and 27 to 58.

The test layers every stage draws on (`ARCHITECTURE.md` 8):

| Layer | Tool | Proves |
|---|---|---|
| Static | `tsc -b`, ESLint with `eslint-plugin-zq`, stylelint, knip, copy lint, registry freshness | Types, layering, determinism, sinks, tokens-only colour, British English copy |
| Unit and property | Vitest in Node, fast-check | Packages, the player reducer, the fold, graders, planners, budgets, protocols |
| Parity | Vitest against recorded outputs of CPython 3.12 with `tools/py/uv.lock` | Every service function feeding a shown or graded number agrees with NumPy, pandas, SciPy, statsmodels or real `git` |
| Widget contract and scene suites | Vitest in Node over every fixture | The contract of `ARCHITECTURE.md` 8.1.1 and 5.14 for every widget |
| Widget interaction | Vitest browser mode on Playwright Chromium, axe | Pointer, tap-then-tap and keyboard paths reach the answer; accessibility in every state |
| Content | `zq check`, `zq verify`, grader replay, generator cross-checks, drill runs, storyboards as pull request artefacts | Every auto-graded answer proved twice; every screen renders |
| End to end | Playwright on both targets (the Artifact through the emulator) | The 18 scenarios of `ARCHITECTURE.md` 8.1.2 |
| Visual | Playwright screenshots in the pinned container: widget fixture states at 390 px and app screens at 390 and 1,280 px, light and dark | Layout and theme regressions |
| Performance | CDP-throttled drag harness, start-up traces, `size-limit`, release budgets | The budgets of `ARCHITECTURE.md` 9.2 |
| Tutor evals | Deterministic graders in CI over recorded replies; the eval runner with a calibrated judge on a different model, locally, in the eval environment | `AI-TUTOR.md` 9.5 gates before any prompt or model change; per-tier Artifact gates (9.6) |
| Devices | The preview Artifact on the owner's iPhone; for code widgets, also the web app's development deploy (stage 25) on the same phone | Feel, timing, memory |

### 11.2 Effort and forecast

AD is defined in the terms table (section 1). All figures are [our estimate]. AD is recorded per pull request from stage 1, and every batch gate re-forecasts the rest of the plan from the measured rates; the stage 14 pilots set the scene rates per family.

| Stages | Phase | AD |
|---|---|---|
| 1 to 26, with 9a, 10a and 10b | Engine core: scaffold, contracts, platform with the CDN loader, design system, content pipeline, player, event log, widget runtime, scene layer with four pilots, primitives, grading, content runtime, Python on the web and the preview Artifact | 222 |
| 3a to 3g | Domain services: numerics, `stats-core`, data, code, algorithms, git and A1's `analysis`, each with Python or `git` parity | 61 |
| 27 to 58, with 51a | P0 widget batches in first-use order, A1's batch W5d and the adopted items' 14 P0 modes included | 249 |
| 59 to 67 | Bertie and the AI tutor, with the eval environment and the judged Artifact tier run | 58 |
| 69 to 81 | Progress, mastery, screens, assessments and exams | 94 |
| 82 to 83 | Web and Artifact builds and release | 16 |
| Contingency | 40% of stages 11 to 58 and 3a to 3g (454 AD) | 182 |
| **1 to 83** | **Everything before content** | **about 880** |
| 84 to 100 | Acceptance and Stage 0 content (346 lessons, about 1.4 AD a lesson with its homework, reviews, generators and drills) | about 480 |
| After Stage 0 | Stage 1 content (988 lessons, A1's 48 and 1.5's 12 continuous-time lessons included) | about 1,380 |
| | P1 and P2 widget waves (146 widgets, about 28 bespoke, with the `markets`, `ml`, `numerics`, `optim` and `research` models and the adopted items' 18 widgets and about 50 modes), contingency included | about 470 |
| | Stage 2 and Stage 3 content (1,007 lessons: 2.0a 91, 2.0b 58, 2.1b 80 and 2.2c 32 added, 24 moved out of 2.3), excluding optional 3.2 (104 lessons, about 146 AD) | about 1,410 |
| **Whole programme** | | **about 4,600** (about 4,750 with optional 3.2) |

Revision 2 re-estimated these rows for the adopted additions [our estimate]: the P0 widgets rows add stage 3g (5 AD), batch W5d at the scene rates (8 AD) and the 14 P0 modes A1 and 1.5's continuous-time levels add to existing widgets (9 AD, about 0.6 AD a mode with fixtures and baselines); the engine core is unchanged in total (the CDN loader and lock add 2 AD at stage 4 and MathML output 1 AD at stage 23, while stage 25 loses 3 AD with the split loader); the P2 waves add 18 widgets (3 S, 8 M, 7 L: about 24 AD at the scene rates), about 19 AD of services and about 31 AD of modes, with contingency about 100 AD; content rows are 1.4 AD a lesson. Draft 1's contingency base was printed as 444 AD; its rows summed to 434.

**Throughput levers, decided.** (1) Four sessions in parallel from stage 3a, about 20 AD a week: during the build one each on the engine, the services, the widget batches, and the tutor and progress; from stage 84 all four on content, one level each. (2) The owner reviews per stage gate in the build phase (about 3 a week, 1 to 2 hours each) and per level gate in the content phase (about 3 a week, about 1.5 hours each on the phone): about 4 to 5 hours a week beside his own study. (3) The semantic check moves from the owner to the independent reviewer (section 11.6). (4) If the stage 28 re-forecast measures below 15 AD a week, a fifth session is added, or the owner is asked whether to revisit the build order he chose (decision 1(a), section 12).

**Content delivery against the learner** [our estimate; learner at 15 hours a week starting now, 12 mapped hours a week after the habits and review, `docs/CURRICULUM.md` 6.5]:

| Milestone | 2 sessions (10 AD a week) | 4 sessions (20 AD a week, chosen) | The learner |
|---|---|---|---|
| Stages 1 to 83 done | June 2028 | August 2027 | In 1.1 (about 550 mapped hours) in August 2027 |
| Stage 0 content complete | May 2029 | January 2028 | Finished Stage 0 in July 2027 |
| 1.5 content complete (A1 included) | February 2031 | December 2028 | Reaches 1.5 in May 2028 (June 2028 with A1), leaves it in November 2028 (December with A1) |
| Stage 1 content complete | March 2032 | July 2029 | Finishes Stage 1 in October 2029 (November 2029 with A1) |
| Content catches the learner | Never: content advances 10.8 mapped hours a week against the learner's 12 | About November 2028, late in 1.5, under the order the owner chose (decision 1(a)) | |

Revision 2 moved each date by the adopted additions: about 20 AD more before content, A1's 48 and 1.5's 12 new lessons before 1.5 closes, and 75 more mapped hours for a learner on the researcher or ML research track. At four sessions the chosen order leaves the learner without app lessons for about two years, from Stage 0 to late 1.5; the owner accepted this at review (decision 1(a)), and until then he studies from the canonical resources the item files name.

### 11.3 Engine core: stages 1 to 26

| # | Stage | Deliverable | Depends on | Done when | AD |
|---|---|---|---|---|---|
| 1 | Scaffold, toolchain and CI | Repository tree (section 10); npm workspaces with exact pins; tsconfig projects; ESLint with typescript-eslint and the first `eslint-plugin-zq` rules (`no-empty-catch`, `no-inner-html`, `no-forbidden-apis`, `no-colour-literals`, layering); Prettier, stylelint, knip, lefthook; `.gitignore`; CI `static`, `unit`, `build`; gitleaks over full history in CI and pre-push; `npm audit` and the licence allow-lists (shipped and development, section 7.6); branch protection on `main` and `stage/*`, `.github/CODEOWNERS`, the agents' GitHub App identity and `label-guard.yml`; `tools/py/` with `uv.lock` for CPython 3.12; `.env.example`, `.env.eval.example` and `.dev.vars.example`; an empty app booting on the dev server and in a minimal `tools/artifact-host`; `tools/release/budgets.ts` and `page.ts`; keeps the handoff pack written before stage 1 current (`CLAUDE.md`, `STATE.md`, `docs/DECISIONS.md` with the two raw-HTML sink justifications and the waivers, `README.md`) | none | A clean clone follows README to green CI; a planted violation of each lint rule fails; a planted fake key fails gitleaks; budgets fail a planted `.zip`, a `.wasm`, a `preflight.js` and a 17 MB file in the Artifact build; a merge into `main` and a `visual-approved` label from the bot identity are both refused, while its merge into a `stage/*` branch with CI green succeeds; `uv sync` reproduces the lock; both targets build | 5 |
| 2 | Spike S1 on the owner's iPhone | A probe Artifact published by a session from files it writes itself, checking the items of `ARCHITECTURE.md` 13 E0: (a) **CDN loading**: an import map in the page fragment, honoured by the classic bootstrap's dynamic `import()`; Preact 11.0.0, `@preact/signals` and `zod/mini` resolved through it from jsDelivr and from cdnjs where it hosts the identical file; the map's `integrity` enforced (an entry with a wrong hash must be refused) [unverified]; a module worker importing classic zod, ts-fsrs and fflate by full URL (if refused, the data worker's jobs run on the main thread in 8 ms slices, `ARCHITECTURE.md` 14 item 19); a classic CDN `<script>` with `integrity` for the Preact 10.29.8 UMD fallback; (b) **MathML**: KaTeX 0.19.0 from the CDN with `output: 'mathml'` rendering a 40-formula specimen sheet (fractions, matrices, sums, integrals, accents, aligned derivations) in system maths fonts, judged by the owner beside the web app's KaTeX HTML, and `TexSlots`' sentinel binding, with slot digits in the swapped `<mn>` node compared against the surrounding maths font and against the sentinel's own `<mtext>`, and VoiceOver reading the current value (conflict 10); (c) the platform checks, of which this list is the single source (`ARCHITECTURE.md` 13 E0 and 14 and `STATE.md` open question 5 mirror it): response compression (transfer against file sizes), Web Locks, IndexedDB in a worker, `navigator.storage.estimate()`, whether an external anchor opens from the frame (the handoff link of `ASSESSMENT.md` 14.3; otherwise the copyable link of section 8.1), file input, inline `style` attributes through `innerHTML`, whether `version.json` is cached despite a query string, version scoping after a second publish (whether the open page still fetches a file only the first version had), `location.reload()` after it, whether a publish may omit the page, whether `null` removals count against the 255 paths of a publish, the back gesture; (d) the capabilities: `sample` (consent, streaming, tiers, abort, page tools), `user` (viewer id, profile) and `db` (`meta/release` through `onSnapshot`, the rule set), plus the `db` size probe in a separate probe Artifact: it writes 192 KiB documents at a paced rate (one every 2 s, doubling the pause on `resource_exhausted`) up to a fixed ceiling of 60 MB in about 320 documents, records success or the cap it reached, then deletes its documents, and the owner confirms deleting the probe Artifact. The earlier JSON-part Python check is dropped (section 4.3) | 1 | Results with device, app version and date in `DECISIONS.md`; the import-map result chooses between section 4.3's design and its named fallback before stage 4 starts; the MathML verdict recorded with screenshots, and if the owner rejects it, the gap goes to the owner before stage 23; the probe's rule applied: a cap at or above 34 MB times the expected number of participants (one today; 34 MB is the whole-path log with its snapshot and drafts, `ASSESSMENT.md` 13.6 scaled to 2,445 lessons) means the checkpoint of `ASSESSMENT.md` 13.6 is not built; each failed check's named fallback written into `ARCHITECTURE.md` before any stage that depends on it starts; the emulator's version-scoping switch set to the measured behaviour | 3 |
| 3 | Contracts, maths core, deterministic maths | `@zq/contracts` (all `ARCHITECTURE.md` 5 types, `SceneDef`, `CompilerRegistry`, the event envelope); `@zq/mathcore`: Philox4x32-10, variadic `hash32`, BigInt rationals, en-GB number parsing, the expression compiler without `eval`, `dmath`, basic statistics (mean, variance, quantiles), scales (the numeric services are stages 3a and 3b); `engine/scope.ts`, `engine/rpc.ts`; the lint rule `zq/no-nondeterminism` | 1 | Unit and fast-check property tests; Philox and `hash32` known-answer vectors; `dmath` bit-identical in Node, Chromium, WebKit and Firefox on 10,000 golden inputs and within $10^{-15}$ relative error of a 50-digit reference; expression parser fuzzed (no property access outside the grammar); scope leak test; a planted `Math.random` in `mathcore` fails lint; `dmath` speed recorded (`WIDGETS.md` 9.2 item 5); 90% coverage | 8 |
| 3a | Numerics in `@zq/mathcore` | `linalg` (LU, QR, Cholesky, symmetric and general eigenvalues, SVD, least squares, condition numbers), `quad`, `ode`, `roots`, `units`, `sample` | 3 | Unit and fast-check property tests; Python parity against NumPy 2.4.6 and SciPy 1.18.0 (`tools/py/uv.lock`) on a seeded corpus per function within stated tolerances, ill-conditioned and repeated-eigenvalue cases included; paths that feed graded numbers use `dmath` and are bit-identical in Node, Chromium, WebKit and Firefox; 90% coverage | 10 |
| 3b | `stats-core` in `@zq/mathcore/stats` | Special functions (gamma, beta, `erf`, regularised incomplete gamma and beta), every distribution family the P0 catalogue entries name (density, CDF, quantile, sampling), tests, OLS with its summary fields, time-series recursions (ACF, ARMA, GARCH filters) | 3a | Parity against SciPy 1.18.0 and statsmodels 0.14.6, tails included (relative error at most $10^{-12}$ where SciPy's own accuracy allows, stated per function otherwise); sampling checked by goodness of fit at fixed seeds | 12 |
| 3c | `@zq/models/data` | `nd-core` (dtypes, broadcasting, axis reductions, NaN rules), `frame-core` (index alignment, missing values, dtypes, `groupby`, joins, reshape) and `price-series` | 3a | Parity against NumPy 2.4.6 and pandas 3.0.2 on a generated corpus of arrays and frames, including duplicate keys, all-NaN groups, mixed dtypes and misaligned indexes; every operation a P0 scene shows is in the corpus | 14 |
| 3d | `@zq/models/code` | `code-lex`, `seed-bank`, `mutant-forge`, `vfs`, `shell` | 3 | Lexer round trips on every drill reference in the item files' samples; `mutant-forge` emits the mutant classes `CONTENT-FORMAT.md` 6.11 names; `vfs` and `shell` agree with a real POSIX shell on a temporary directory for the commands 0.4 and 1.2 teach (CI parity) | 9 |
| 3e | `@zq/models/algo` and `trace.py` | `algo-trace` for every algorithm `algo-lab` and its presets step; `workers/python/trace.py` and its recorder format | 3 | Step traces equal reference runs in CPython 3.12; `trace.py` gives identical traces on CPython 3.12 and Pyodide for the reference programs | 6 |
| 3f | `@zq/models/git` | `git-model`: commits, branches, merge, rebase and conflicts as 1.2 teaches them | 3 | Each operation's result equals real `git` on a temporary repository for a scripted corpus | 5 |
| 3g | `@zq/models/analysis` (added for A1) | Exact rational arithmetic over `@zq/mathcore`'s rationals, the topology grammar and classifier, closed-form sup gaps for the generator families, the quantifier engine and its adversary search (`stage1-real-analysis.md` 8.2) | 3 | Parity against Python's `fractions` and SymPy on a seeded corpus per function; the adversary finds the known defeating move in every negative fixture and none in the positive ones; no float on a graded path; 90% coverage | 5 |
| 4 | Platform adapters and the Artifact host emulator | Every `Platform` interface for web, Artifact and fake; `MemoryStore`; Web Locks writer election with heartbeat fallback; `tools/artifact-host` complete: served-type allow-list, CSP, sandboxed second origin, fake `window.claude` (`sample` with scripted streams and every error code, `db` with rules, `{self}`, `onSnapshot` and injected errors, `user`, `downloads`); `app/log.ts`, the ring-buffer logger with redaction; the CDN path of section 4.3: `tools/cdn` (`cdn.lock.json` from `package-lock.json`, the cdnjs identity check, the nightly drift job), the Artifact build's externals and the import map writer in `page.ts`, `tools/release/provenance.ts`, `platform/artifact/cdn.ts`, and the emulator serving locked CDN URLs from local copies checked against the lock | 2, 3 | One conformance suite per interface passes against every implementation; a planted `node_modules` module in an Artifact chunk fails the build, and so does a planted `node_modules` import in a fixture generator module built by esbuild (`provenance.ts` reading its metafile; stage 23 runs the same check on the real generator modules); a locked file changed by one byte fails the drift job; the emulator refuses a CDN URL not in the lock and boots the Artifact build with every third-party module from the lock; a viewer writing another's subtree is refused in the emulator; error injection tests; two-tab writer test; boot with every capability absent; logging an object with answer, code, text, token or viewer-id fields records none of them | 10 |
| 5 | Design system port | `styles/` from `prototype/css/tokens.css` (light and dark guards, explicit body background), KaTeX CSS with rewritten font URLs and KaTeX fonts (web), `math.css` for MathML (Artifact), font faces per target; `ui/` components including Button (lipped, black labels on green and amber), Sheet, Modal, Toast, Keypad, SymbolBar; the motion service with full, reduced and test modes; synthesised sounds; `#/system`; the copy lint for `copy.ts` | 3 | Visual baselines at 390 and 1,280 px, light and dark; axe clean; keyboard paths for every interactive component; a script checks every text and background token pair against WCAG 2.2 AA (4.5:1 text, 3:1 large text and UI), black on `--green-face` and `--amber-face` included; spring settle and stability tests; reduced motion lands at once | 8 |
| 6 | Content schema (C1) | `@zq/content-schema`: `CONTENT-FORMAT.md` 3.2 schemas including curriculum, tracks, plan, exit parts with `slotMin`, `sets`, `count`, exams with forms and sections; inferred types; JSON Schema export; `zq fmt` | 3 | The worked example and revision 2 fixtures validate; 40 invalid fixtures fail with their expected messages; `zq fmt` idempotent on every fixture | 5 |
| 7 | Compiler front end `zq check` (C2) | Strict YAML profile, references, `from:` merging, element references through `CompilerRegistry` (a fake registry until stage 10a), structure rules, copy lints (British spelling, banned filler, dashes, reading level), tutor-field leak lint behind the grader interface, KaTeX render of every formula; `content/AUTHORING.md` | 6 | The worked example passes; each lint rule has a failing and a passing fixture; a broken copy of the lesson reproduces findings 1 and 2 of `CONTENT-FORMAT.md` 10.6 and the six planted faults of its 0.2 | 8 |
| 8 | Independent verifier `zqverify` (C5) | Spaces, the whitelisted verify language walked from `ast`, chains, arithmetic claims in copy, Monte Carlo second checks, the Node pre-pass to MathJSON, a sandbox for `.verify.py` (no network, no writes outside a temporary folder, CPU and memory caps) | 7 | The worked example verifies; the re-expressed prototype `sTen` fails with "same value"; 50 textbook answers across probability, calculus and linear algebra; the verify language rejects attribute access, imports and calls outside its whitelist (fuzzed) | 8 |
| 9 | Lesson player reducer and item policies | `engine/player/machine.ts`, `policy.ts`, effect types; `engine/progress/fold/points.ts` (XP and MP rules, `ASSESSMENT.md` 12.2 and 12.3) | 3, 6 | Every row of `ARCHITECTURE.md` 5.7.2 and every policy row of 5.7.3 is a test; property test: a result with a stale generation never changes state; a reveal always records 0 XP; 100% branch coverage of `machine.ts` | 5 |
| 9a | Event log, `AppendQueue` and fold (A1; was stage 68) | Event schemas per kind and the envelope, `AppendQueue` (the only assigner of `seq`), the fold framework, snapshots, the synthetic whole-path learner (about 121,000 events for the adopted path) | 3, 4, 9 | Fold properties (deterministic, order-independent, idempotent, incremental equals rebuild) as fast-check tests; the `AppendQueue` contract tests (one writer, monotonic `seq`, persist after fold, recovery after a failed write) pass against `MemoryStore`, and stage 69's stores must pass the same suite; full rebuild within 1.5 s on the CI proxy and within 3 s in a worker on the iPhone (taken at stage 25); a single event within 2 ms | 6 |
| 10a | Widget runtime | Registry generators (`registry.gen.ts`, `registry.node.gen.ts`, `aliases.ts`), `CompilerRegistry` for `tools/zq`, `WidgetHost`, `WidgetApi`, interaction hooks, overlay, show-why runner, preview guard, describe aggregation, drafts and migration (flush on `visibilitychange` and `pagehide`); two internal test widgets | 4, 5 | Both test widgets work on pointer, tap-then-tap and keyboard paths in the browser; the guard refuses a ghost that changes the answer or would grade correct; empty scope after unmount; drafts survive a reload; `zq check` passes against the real registry | 7 |
| 10b | Widget tooling and gallery | The fixture runner, the generic contract suite (`ARCHITECTURE.md` 8.1.1), browser harness, frame-time harness, `new:widget`, `#/gallery`; the widget lint rules (`zq/no-raw-timers`, `zq/no-raw-pointer`, `zq/no-state-in-render`, `zq/no-classic-zod`, `zq/no-schema-import`, `zq/copy-in-copy-files`); `docs/engine/WIDGET-AUTHORING.md` first draft | 10a | Both test widgets pass the contract suite; `size-limit` catches a planted `schema.ts` import in a cluster chunk; each new lint rule has a failing and a passing fixture; a stale generated registry fails the freshness check; `new:widget` output compiles and its generated contract tests fail until implemented | 5 |
| 11 | Plot primitives | `plot-2d` and `marks` with the mark types Stage 0 uses first (curve, parametric curve, point, segment, line, ray, vector, polygon, region, angle, brace, label, ghost, bars, scatter, dot-plot, box, bin, construction marks) and `CanvasLayer` for dense layers; every later mark type is added, as its own module, in the batch that first needs it | 10b | `WIDGETS.md` 7.5 gate; per-type geometry and describe-phrase unit tests; P95 at most 4 ms per drag frame at 4x with 1,200 static nodes; Table view for every chart | 12 |
| 12 | Handles and readouts | `drag-point`, `slider`, `live-formula` (on `TexSlots`), `value-table` | 11 | `WIDGETS.md` 7.5 gate; exact-value editor on every handle; `aria-valuetext` with units; KaTeX never re-renders during a drag (frame test) | 6 |
| 13 | Grid and token primitives | `number-line`, `region-select`, `token-tray`, `stepper`, `cell-grid` | 12 | `WIDGETS.md` 7.5 gate; lift-and-drop keyboard model; element ids of the 0.1 sample lesson (`span:`, `token:`, `lens:main`) | 9 |
| 14 | Scene layer and four pilots | `src/widgets/scene/`: `defineScene`, typed binding paths, `SceneView`, layout containers (row, column, stack, grid, overlay, embed), automatic static-layer memoisation, generated logic members, declarative recipes; the scene contract suite (every binding resolves for every fixture; `derive` deterministic and within 2 ms P95 at 4x); `new:scene`; the scene chapter of `WIDGET-AUTHORING.md`; pilots `place-value-chart`, `outcome-grid` (with the element ids and recipes of `CONTENT-FORMAT.md` 12.1), `unit-circle` and `svd-stepper` (a heavy model on stage 3a, with every P0 mode); `ARCHITECTURE.md` 5.14 confirmed against the code | 13, 3a | Each pilot passes the generic and scene suites, at most 350 lines of `scene.ts`, P95 within 8 ms at 4x; model functions parity-tested against Python; a planted bad binding path fails type checking; each pilot's AD recorded and the rate per family recalibrated (section 3.2); the go or revert decision per family recorded in `DECISIONS.md` | 14 |
| 15 | Expression entry and maths services | `expression-input`, the `cas` service (Compute Engine `latex-syntax`, lazy, from the CDN in the Artifact) and `mathfield` (MathLive, lazy, KaTeX fonts, sounds off, web only), `numeric-input`, `choice` | 12 | `WIDGETS.md` 7.5 gate; keypad on coarse pointers; the plain field with the symbol bar and live MathML preview, the Artifact's input, works with MathLive absent; parse of the conformance corpus's LaTeX within 20 ms on the CI proxy | 9 |
| 16 | Structured inputs | `card-sort`, `derivation-steps`, `scratch-pad`, `free-response` (voice mode deferred to P1) | 13, 15 | `WIDGETS.md` 7.5 gate; learner text rendered as text only (an injection fixture renders literally) | 8 |
| 17 | Simulation and data primitives | `sim-runner` (worker jobs), `chance-object`, `mass-editor`, `array-strip`, `matrix` | 13 | `WIDGETS.md` 7.5 gate; simulations reproducible from (seed, stream, index); a simulated estimate is never graded (contract test) | 9 |
| 18 | Free drawing and 3D | `sketch-pad` (feature grading, monotone spline), `plot-3d` | 11 | `WIDGETS.md` 7.5 gate; 3D view buttons and keyboard rotation; frame budget | 8 |
| 19 | Code and text primitives | `node-link`, `code-surface`, `diff-view`, `text-terminal`, `speed-timer` | 13, 3d | `WIDGETS.md` 7.5 gate; terminal and code text rendered as text; timer under the fake clock | 9 |
| 20 | Graders (C3) | `@zq/graders` for numbers, choice, sets, mappings, ordering, intervals, matrices, distributions, points, curves and predicates; matching order; the accepted-answer rule; `leak.ts`; grader replay in CI; the tutor-field lint switched to the real graders | 6, 3 | Property tests on the numeric parser (every form, en-GB separators, nudges); replay passes on the worked example; every accepted rule of `CONTENT-FORMAT.md` 7.9 produced; 10 leak and 10 non-leak extractor fixtures per probed kind | 8 |
| 21 | Expression grading (C4) | MathJSON normalisation, seeded numeric probing in the declared domain, relations, form checks; the SymPy-generated conformance corpus | 15, 20 | 100% agreement on the required corpus; unit tests per form check; grading within 20 ms on the CI proxy | 6 |
| 22 | Generators (C6) | `@zq/gen`: box enumeration, the Node and Python harness, built-item checks, admissible index and exam reserve, `make` and `makeWhere`, golden files, specimen sheet | 8, 20 | The `CONTENT-FORMAT.md` 11 generator agrees with its twin at all 21,760 points; the `>=` mutation is caught; golden hashes match in Chromium, WebKit and Firefox | 8 |
| 23 | Emit and content runtime (C8, E5) | Bundles, generator modules, manifest file with the page meta tag (`vite-plugin-zq-content`), search, glossary, Notebook, skill graphs, tutor context with check summaries, `ids.lock.json` and the `rev` rule, migrations runtime; the loader, `BlobCache` wiring, data-worker validation, `Prose`, `Tex` and `TexSlots` with HTML-and-MathML output on the web and MathML output in the Artifact, templates, the generator runtime; content hot reload | 7, 8, 10a, 20, 22 | Bundle sizes within budget for the worked course; rename and split migrations pass on learner fixtures; a changed answer without a `rev` bump fails CI; every row of `ARCHITECTURE.md` 5.10.3 tested; a content-only rebuild changes only the page, the manifest and that course; `Tex` renders a KaTeX injection corpus (`\href` with a script URL, `\htmlData` with a bad name, raw HTML in text) as inert in both outputs | 11 |
| 24 | Player views and the reference lesson (E6, C9) | `LessonPlayer`, `ScreenFrame`, `ButtonRow`, `VerdictBubble`, `HintSheet`, `WhySheet` (the Why rule), `SolutionReveal`, `Quiz`, `Complete`, the key map with the single-key switch, announcements; `ItemRunner`; the `record` effect through stage 9a's `AppendQueue` to `MemoryStore` (stage 69 swaps in `IdbStore` and `DbStore` behind the same `ProgressStore` interface); the `trial-simulator` scene; preview, storyboard, specimen and tutor-request routes with Playwright capture | 9, 9a, 14, 15, 16, 17, 23 | The reference lesson runs end to end on both targets (emulator for the Artifact) with no lesson-specific code; the live-code screen rule of section 4.3 holds against the Artifact's handoff stub: a code screen enters `reading`, records `read` with `deferred: 'web'` and no XP, and a lesson with a deferred screen completes (reducer table rows and a fixture lesson); keyboard-only run; axe; the storyboard renders every state at both widths and themes with no overflow; no animation frames once idle; Check to verdict within 150 ms | 10 |
| 25 | Python runtime on the web app (E8) | Python worker and protocol, the native loader with `loadPackage` integrity checks, `tools/pyvendor` (fetch with SHA-256), soft deadline and watchdog, `PythonRuntime.available` with `budget.ts` on the web and the handoff stub in the Artifact; `zq preview --artifact` (one-course and gallery builds with development routes, published by a session to the one long-lived preview Artifact, gate results read from its `db` at `ops/gate-<stage>`); a manual `pages.yml` dispatch that deploys the web build with development routes to the decision-13 host for phone checks (default (b): a Cloudflare Pages development project behind an Access policy admitting only the owner; the production deploy is stage 82) | 4, 10b, 23, 24 | Soft-deadline, watchdog, memory and crash tests with real Pyodide in CI; soft-deadline overhead on reference drills recorded (above 1.3 times drops it, decision 31); on the owner's iPhone in the web preview, timings and memory recorded for every load group, the stage passing when `stdlib` and `numpy-pandas` pass (warm start within 4 s) (conflict 9); stage 9a's fold rebuild timed on the phone in the preview Artifact; the preview Artifact opens on the gallery and on a course start route, and a second gate republishes it instead of creating another; in the Artifact build every code screen shows the handoff link and no Python file is built (test); learner code cannot reach `fetch` beyond the loader's files (test); a load stalled for 30 s is terminated and reported (test with a throttled server); an anonymous request to the development deploy is refused by Access (test), and Access's free-plan terms are recorded in `docs/DECISIONS.md` | 11 |
| 26 | Drill pipeline and SQL (C7) | `zqtest`, `grader.py`, CI runs on CPython 3.12 (`tools/py/uv.lock`) and Pyodide with exactly each drill's `needs`, each run inside a subprocess wall-clock limit, starter and wrong-solution checks, mutant-forge integration; the SQLite worker and `SqlRuntime` on the web, the handoff stub in the Artifact | 7, 25, 3d | The Homework 1 drill passes every rule of `CONTENT-FORMAT.md` 6.11 on both interpreters; an undeclared `import numpy` fails the build; a planted weak test suite is caught by a surviving mutant; SQL drills run with a 1,000-row cap on the web and hand off in the Artifact build | 6 |

### 11.4 P0 widget batches: stages 27 to 58

Order is first use in the depth-first content order (`WIDGETS.md` 7.3, whose row numbers are cited); every widget's behaviour comes from the catalogue section its entry names. All batches depend on stages 10a to 26 and on the service stage named in their row (3a numerics for 49 to 53, 3g analysis for 51a and for the A1 modes of 36, 39, 49 and 50, 3b `stats-core` for 34, 39 and 54 to 57, 3c data for 43 and 44, 3d code for 32, 35, 41, 46 and 48, 3e algorithms for 41, 42 and 45, 3f git for 47).

**Batch definition of done:** for every widget, the `WIDGETS.md` 7.5 gate (schema validates every fixture; generic contract suite; pointer, keyboard and tap-then-tap paths reach the expected answers; axe clean in every state; reduced and test motion; `describe` snapshots; P95 frame time within budget at 4x; empty scope after unmount; generators pass CI; Python parity for every function feeding a shown or graded number, the services' own parity having passed in stages 3a to 3f); for scenes, the scene suite; every P0 mode in the entry implemented with a fixture; new mark types with their unit tests; measured AD recorded and the plan re-forecast; the owner checks the batch in the preview Artifact on the iPhone and records it at `ops/gate-<stage>`. **A batch with any widget on `PythonRuntime` or `SqlRuntime`** (stages 32, 41, 46 and 48: `code-cell`, `parsons`, `code-tracer` with `trace.py`, `bench-lab`, `plot-workbench`, `mutant-hunter`, `injection-lab`) adds two checks: each such widget's Artifact handoff mode (4.3, live-code screens) in the preview Artifact, and its running behaviour, timing and memory in the web app on the iPhone through stage 25's development deploy; the gate's `ops/gate-<stage>` record holds both targets' results.

| # | Batch | Contents (`WIDGETS.md` 7.3 rows) | Kind | AD |
|---|---|---|---|---|
| 27 | W1a | `written-method`, `area-model`, `bar-model`, `algebra-tiles`, `expression-tree`, `factor-tree`, `counting-slots` (rows 2 to 6, 8, 9) | 7 scenes | 7 |
| 28 | W1b | `venn-diagram`, `modular-clock`, `double-number-line`, `multiplier-chain`, `unit-chain`, `fermi-estimator`; presets `times-table-grid`, `bounds-explorer` (rows 10, 11, 13, 14, 16, 18 to 20) | 6 scenes, 2 presets | 6 |
| 29 | W1c | `speed-drill` (with the 80-in-8 configuration and per-item records), `typing-trainer` (rows 7, 12) | 2 bespoke, clock-driven | 6 |
| 30 | W1d | `graph-explorer` (row 15) | bespoke; a host that later scenes embed | 6 |
| 31 | W1e | `equation-workbench` (row 17) | bespoke; algebraic manipulation gesture | 6 |
| 32 | W1f | `code-cell` (row 21: editor, Run, Submit, results, tracebacks, figures, runtime states), then `parsons` (row 52). One direction only: `parsons` embeds `code-cell`'s runner component, and `code-cell`'s Parsons mode (small screens) is configuration that swaps its editor pane for `token-tray`, so neither widget composes the other | bespoke on `PythonRuntime`, and 1 scene | 7 |
| 33 | W2a | `function-machine`, `balance-scale`, `file-tree`, `scatter-fit`, `equation-stack`; preset `inequality-regions` (rows 22, 24 to 28) | 5 scenes, 1 preset | 6 |
| 34 | W2b | `setup-checklist`, `sign-chart`, `dot-plot-stats`, `complex-plane`, `iteration-cobweb` (rows 29 to 31, 33, 34) | 5 scenes | 5 |
| 35 | W2c | `strategy-trainer` (row 23), `shell-sim` (row 32) on stage 3d's `vfs` and `shell` | 2 bespoke | 9 |
| 36 | W3a | `solid-viewer`, `sequence-lab`, `slide-rule`, `sum-visualiser`, `series-explorer`, `circle-to-wave` (rows 36, 39, 40, 42, 43, 46), with A1's modes on `sequence-lab` and `series-explorer` | 6 scenes | 7 |
| 37 | W3b | `vector-combo`, `projection-lab`, `row-column-picture`, `matrix-multiply`, `determinant-lab`, `transform-grid` (rows 124, 110, 125, 49, 51, 117): the bases the 0.3 presets expand to, pulled forward | 6 scenes | 6 |
| 38 | W3c | `elimination-lab` (row 126), then presets `vector-plane`, `matrix-grid`, `linear-map` (rows 37, 48, 50) | bespoke (row operations) and 3 presets | 8 |
| 39 | W3d | `tree-diagram`, `pascal-triangle`, `binomial-expander`, `stat-chart`, `induction-chain`, `limit-explorer` (rows 53, 54, 56, 58 to 60), with A1's sequence probes on `limit-explorer` | 6 scenes | 7 |
| 40 | W3e | `geometry-board` (row 35) | bespoke; construction gestures | 6 |
| 41 | W3f | `workspace-sim` (row 38), `code-tracer` (row 47) with `trace.py`, then `predict-output` and `diagnostic-reader` (rows 41, 44), which embed the tracer | 2 bespoke, 2 scenes | 11 |
| 42 | W4a | `float-inspector`, `code-blanks`, `complexity-lab`, `format-lab`, `pipeline-flow`, `json-explorer`, `search-path`, `code-annotator` (rows 61 to 64, 70, 72, 75, 76) | 8 scenes | 7 |
| 43 | W4b | `csv-inspector`, `time-series-lab`, `ndarray-lab`, `broadcast-lab`, `dataframe-lab`, `groupby-lab` (rows 71, 73, 77, 78, 80, 81) on stage 3c | 6 scenes | 7 |
| 44 | W4c | `path-simulator` with the Brownian `refine` mode 1.5's continuous-time levels promote to P0, `join-lab`, `reshape-lab`, `drawdown-lab`, `permission-bits` (rows 79, 82 to 84, 86) | 5 scenes | 7 |
| 45 | W4d | `algo-lab` with presets `sort-lab`, `recursion-tree`, `hash-table` (rows 65 to 68) on stage 3e | bespoke and 3 presets | 8 |
| 46 | W4e | `bench-lab`, `regex-lab`, `plot-workbench` (rows 69, 74, 85) | 3 bespoke | 9 |
| 47 | W4f | `git-graph`, `merge-conflict` (rows 87, 88) on stage 3f | 2 bespoke | 9 |
| 48 | W4g | `mutant-hunter`, `code-review`, `injection-lab` (rows 89 to 91) | 3 bespoke | 12 |
| 49 | W5a | `epsilon-delta`, `local-zoom`, `derivative-tracer`, `growth-rectangle`, `function-mapping`, `rates-scene`, `taylor-builder`, `root-finder`, `secant-tangent` (rows 92 to 100), with A1's modes on `epsilon-delta` (Thomae, uniform), `local-zoom`, `derivative-tracer`, `secant-tangent` and `plot-2d`'s Thomae and step-function configurations | 9 scenes | 10 |
| 50 | W5b | `objective-explorer`, `convexity-chord`, `descent-lab`, `riemann-sum`, `accumulator`, `slope-field`, `solid-of-revolution`, `volume-slicer` (rows 101 to 108), with A1's three-chord mode on `convexity-chord` | 8 scenes | 9 |
| 51 | W5c | `surface-explorer`, `dependency-graph`, `gradient-compass`, `quadratic-form`, `least-squares-fit`, `lagrange-explorer`, `region-bounds` (rows 109, 111 to 116) | 7 scenes | 8 |
| 51a | W5d (A1; conflict 22) | `bound-lab`, `quantifier-game`, `cardinality-lab`, `proof-builder`, `line-topology`, `uniform-lab` (`WIDGETS.md` 7.3 rows 118 to 123) on stage 3g; a scene above rule 4's cap splits into the preset its entry names | 6 scenes (4 M, 2 L) | 8 |
| 52 | W6a | `subspace-tester`, `solution-set`, `four-subspaces`, `basis-change`, `gram-schmidt` (rows 127 to 131) | 5 scenes | 5 |
| 53 | W6b | `eigen-finder`, `linear-dynamics`, `pca-lab`, `low-rank-approx`, `condition-number` (rows 132, 133, 135 to 137; `svd-stepper`, row 134, is a stage 14 pilot) | 5 scenes | 5 |
| 54 | W7a | `indicator-board`, `prob-square`, `dist-explorer`, `trial-strip`, `first-step-solver` (with its continuous-time mode for 1.5 level Z4b), `odds-ledger`, `contingency-table`, `icon-array` (rows 139, 140, 148, 141 to 143, 145, 144), in that order because each later one embeds an earlier one | 8 scenes | 10 |
| 55 | W7b | `rv-mapper`, `galton-board`, `convolver`, `sampling-lab`, `generating-function`, `order-statistics` (rows 147, 149 to 153) | 6 scenes | 7 |
| 56 | W7c | `joint-density`, `geo-prob`, `covariance-lab`, `gaussian-2d`, `filtration-tree`, `cond-expectation`, `markov-chain` (with the `ctmc`, generator and birth-death modes of 1.5 levels Z4b and Z4c), `lattice-walk` (rows 154 to 157, 159, 158, 160, 161) | 8 scenes | 12 |
| 57 | W7d | `kelly-lab` (row 162), then `game-lab` (row 146), which embeds it | 1 scene, bespoke | 7 |
| 58 | W7e | `puzzle-workbench` (row 138), which embeds widgets from W1 to W7d, with its selection hook and ratings | bespoke | 6 |

Built elsewhere: rows 1 (`place-value-chart`), 45 (`unit-circle`), 57 (`outcome-grid`) and 134 (`svd-stepper`) in stage 14, row 55 (`trial-simulator`) in stage 24. Row numbers follow `WIDGETS.md` 7.3 as revised on 7 October 2026, which inserted A1's rows 118 to 123. The adopted items' 14 P0 modes (`WIDGETS.md` 8.4) are built with the widget they extend, as the rows above say. `plot-2d` is built in stage 11 with its slots for handle layers; each handle primitive (stages 12, 13, 18) is tested inside it. Modes that embed a P1 or P2 widget (`free-response` voice, `sampling-lab` Q-Q view, `puzzle-workbench` voice and `bet-lab`) arrive with that widget's wave. A script in CI checks that every widget's composed and preset-base widgets are built in an earlier stage or earlier in the same batch, which a composition cycle fails by construction. `core` cluster size is measured after stage 19 and again after stage 32, when `code-cell` exists (`WIDGETS.md` 9.2 item 1); above 80 KB gzipped, `code-cell` and the code primitives (`code-surface`, `diff-view`, `text-terminal`) move to a `core-code` chunk loaded with a lesson's first code screen. The P1 finance primitives do not exist at P0, so a `core-markets` split could not shrink `core`.

### 11.5 Tutor, progress, assessments and builds: stages 59 to 83

| # | Stage | Deliverable | Depends on | Done when | AD |
|---|---|---|---|---|---|
| 59 | Bertie | `src/ui/bertie/` ported from `prototype/bertie.html` to TypeScript (geometry, poses, markup, controller, `Bertie.tsx`), sharing `engine/motion/spring.ts`; the player's `bertie` effects wired | 5, 24 | `BERTIE.md` 12.2 tests (spring, geometry, state machine, speech safety, rate limit, sleep, ids, clean-up, visual at 32, 96 and 220 px, axe, size at most 12,000 bytes); the owner's sign-off on draft 3's rounded hair before baselines are committed (the rest of the face was confirmed at review, decision 4); 60 fps celebration at 160 px measured on the iPhone | 4 |
| 60 | Tutor contracts and guards (T0, T1) | `context/schema.ts`, act-line parser, action schemas, error codes, copy; `leakprobe.ts` on `leak.ts`, `codeguard.ts`, `lint.ts`, `markdown.ts`, `gate.ts`, `paste.ts` | 10a, 20 | Schema fixtures valid and invalid per mode; act-line parser fuzzed with 1,000 strings without throwing; every action rejects unknown ids and over-cap input; gate table tested row by row; the Markdown renderer never produces an element outside its allow-list (property test) | 6 |
| 61 | Context assembly and renderers (T2) | `assemble.ts`, `caps.ts`, `escape.ts`, `render/sample.ts`, `render/anthropic.ts`, `prompt/core.md`, `version.ts` | 60 | Byte-identical renders for identical state; sealed and open invariants; escaping blocks forged tags and act lines (fixtures with `</learner_message>` and `@@` lines); snapshot of one render per mode per target | 5 |
| 62 | Tutor proxy (T3); creates the Class C exposure | `proxy/` complete: Worker and Node entries, auth, origins, validation, rendering, signing of chat call blocks and of tool-turn assistant blocks, tool-result validation against each tool's output schema, limits with the SQLite-backed `TutorLimits` Durable Object pinned in the `wrangler.toml` migrations, events, prices, logging; `wrangler.toml` `[env.dev]`, `[env.prod]` and `[env.eval]`; `proxy:local` and `proxy:eval` through `node --env-file`; start-up checks that name missing variables; `proxy.yml` | 61 | Integration tests against a fake upstream: auth, origins, validation, every event type, tool-loop continuation with signed assistant blocks (a forged block and a 5 KB tool result are refused), refusal with and without fallback, `max_tokens`, disconnect stops the upstream, limits fail closed, tampered and foreign signatures rejected; `TutorLimits` tested in the Workers runtime (`@cloudflare/vitest-pool-workers`): concurrent requests on one counter, fail-closed when storage throws, day and month rollover; the attack pass of `AI-TUTOR.md` 10.5 on the local proxy, and the cost-exhaustion and 100-requests-a-minute attacks again against the deployed `dev` environment; a missing variable stops start-up with its name and no value; live smoke calls show cache reads above 0 on the second call and the betas' availability recorded; `ping` events every 15 s during a long thinking call; log lines contain no text (test) | 9 |
| 63 | Backends and service (T4) | `backends/artifact-sample.ts`, `backends/web-proxy.ts`, `service.ts`, `stream.ts`, `usage.ts` | 60, 61, 62 | The Artifact backend against the emulator's `sample` with every error code, consent decline, tier substitution and tools absent; the web backend against the proxy with a fake upstream; abort and supersede; at most 2 calls in flight; no automatic retry (test); a stream silent for 45 s ends as `upstream_error` with the partial kept | 5 |
| 64 | Bertie in the UI (T5) | `tutor/ui/*`: mascot mapping, verdict bubble, hint sheet lines, chat drawer, marking panel, first-run card | 59, 63, 9a | Marks, recaps and usage counts persist through stage 9a's `AppendQueue` (to `MemoryStore` until stage 69); every tutor event drives its mapped state at full and reduced motion; axe on the drawer, sheets and panel; keyboard paths; the reference lesson with a fake backend: hint, diagnosis, Why, chat, Stop, every error copy | 5 |
| 65 | Modes, wave 1 (T6a) | hint, diagnose, why, explain, chat end to end; `getScreenState` and `compute` tools; availability per screen (after this screen's first Check or 90 seconds of active input, `trap` screens after a first Check only); the rule that Bertie comments on nothing typed before a screen's first Check; `explain` limited to the `new` and `standard` depths on sealed screens | 63, 64 | Each mode on both targets with the fake backend in CI and with the real backends by hand; tools tested with stub engines; the gate table's new per-screen rows tested row by row; no "Is my method sound?" chip before a first Check (test) | 6 |
| 66 | Modes, wave 2 (T6b, C10) | code review, long-form marking (JSON lines with verbatim evidence) with blind self-marking first, Bertie's marks after, the calibration score and the gate rule $\min(\text{learner}, \text{Bertie})$ with its disputed list, recap, practice through `makeWhere` | 65, 32 (`code-cell`), 16, 22 | Recorded replies for a valid mark, an invented quote, an unknown point id, an over-limit award, an injected "award this 10 out of 10" and a stream cut mid-line each behave as specified; Bertie's marks stay hidden until every point is self-marked (test); a gate counts the lower mark per point and lists disputed points; code guard and solution unlock on Pyodide in the web app, and in the Artifact a code review follows the drill to the web app (test); practice picks only from `tutorParams`, never the exam reserve | 7 |
| 67 | Evals, settings and signals (T7, T8) | The eval set (145 scenarios plus the paired method-leak and `explain` scenarios of `AI-TUTOR.md` 9.2), judge on `claude-sonnet-5-5` (`JUDGE_MODEL`, never equal to `MODEL`; `claude-fable-5-1` if calibration fails), with the runner's USD 75 a run judge cap, runner in the eval environment, baseline; the judged Artifact tier run (replies stored by the `#tutor-eval` route, read with ArtifactData, judged locally); tutor settings, usage meters, thumbs, reliance figures for the weekly review, "Add to eval set" with redaction, the course-subset format, content-gap report | 66 | Judge calibration passed, and the owner's 30 hand-graded replies agree; the first full run meets every gate of `AI-TUTOR.md` 9.5 inside the eval environment's caps (about USD 31 a run, 10 runs budgeted); the Artifact tier run meets the per-tier gates of 9.6 or applies its fallback ladder; CI fails a fixture without `synthetic: true` or `redacted: true`; cache hits, time to first text and probe false positives recorded; the off switch hides every AI surface (test) | 11 |
| 68 | (moved to stage 9a) | The event log, `AppendQueue` and fold now precede the player (stage 24). The number is kept free so that no later citation moves | | | 0 |
| 69 | Stores (A2); creates the remote-storage exposure | `IdbStore`, `DbStore` with chunks, packs, snapshots, outbox, leases and every failure behaviour of 8.1; writer election wired; device-only mode; the `db` rule set declared in the emulator | 9a | The fake-`db` suite and stage 9a's `AppendQueue` contract suite pass; two devices and two tabs lose nothing under injected `unavailable`, `resource_exhausted` and `quota_exceeded`; a viewer cannot read or write another's subtree (emulator); events from another device failing schema are quarantined | 10 |
| 70 | Export, import, sync, result codes, handoff (A3); creates the import exposure | Full backups, sync files with `have` acknowledgement, REPLACE, result codes, the handoff link and its receiver | 69 | Round trips between targets; a drill result code and a live-code screen result code (`ref` = lesson id, `rev`, screen id) each clear their pending item, and a screen code for a retired `rev` is refused; every rejection case (oversize, bad schema, wrong hash, future version, crafted payload) writes nothing; re-import idempotent and order-free; handoff payload over 8 KB refused | 5 |
| 71 | Time, streaks, XP, MP, achievements, ghost race (A4, A14 P0) | Active-time tracking, study day, streaks, rest days, breaks, ledgers, achievements, ghost curves | 9a | `ASSESSMENT.md` 16 streak and points tests; Today and You read only derived state (lint and test) | 4 |
| 72 | Skill graph and mastery (A5) | Skill graph loading, FSRS-6 cards by band, grade mapping, retention tiers including the `core-interview` tier and its stretch cards, implicit repetition, mastery numbers, readiness; the per-topic card budget check | 9a, 23 | Golden card states; a topic over its card budget fails the build; readiness hand checks; the mastery map renders from the synthetic learner | 7 |
| 73 | Redo queue and review (A6) | Redo queue, review composer, weekly load balancer, lesson-start warm-up | 72 | The date table; variant rules; budget and interleaving on synthetic queues | 5 |
| 74a | App shell and home screens (E7, part 1) | Router, shell, stores, Today, Learn, Course, Review, Notebook, Search, Onboarding shell, error boundaries, update notices | 24, 71, 72 | Visual baselines for every screen at both widths and themes with the synthetic learner; axe; route, focus and title tests; search finds the expected lessons for 20 fixture queries; warm start-up within 1.2 s on the CI proxy | 7 |
| 74b | Records and Settings (E7, part 2) | You (stats, mastery map, weekly review frame), Settings with Diagnostics and Self-test, Import | 74a | Visual baselines and axe for each screen; Copy diagnostics contains no learner text (test); Self-test runs every check against the emulator | 5 |
| 75 | Quiz, review, practice and homework (A7) | The flows of `ASSESSMENT.md` 2.3 to 2.6 with drafts, submission, marking, the long-form hook and pending web-app items; quiz production items on Prove, Derive and Show lessons; homework drawing 25 to 30% from earlier levels and topics, unlabelled and mixed; level reviews drawing from earlier courses; long-form redo siblings; the lesson fast path | 73, 66 | A level's quiz, review and homework run end to end on both targets with recorded tutor replies; the gate keeps Bertie off ungraded items (test); a homework instance's earlier-level share and its "which tool?" items match the rules on a scripted learner; a failed long-form item's redo serves its sibling | 8 |
| 76 | Exam engine (A8) | Paper kinds including `exit-item`, forms and freshness, slot order shuffled per form and two unlabelled slots per form, sections with their own clocks, calculators and bars, aids, follow-through marking, rules screen, clock and pause budget, navigator, results (model answers withheld for held-out long-form items after a fail), cool-downs, remediation, one diagnostic sitting per topic and stage paper, retention sittings at 3 and 12 months with their reopening rule, the cumulative Stage 1 and Stage 2 papers, the gate marking rule and disputed list, integrity record | 75 | Exam tests with a fake clock; the 0.3 topic exam (two timed sections), a finals-style paper with a section bar and a GCSE-style paper sat end to end; reload mid-paper keeps the clock; a second diagnostic sitting carries the cool-down; two forms of one paper differ in slot order; a retention sitting below 60% reopens the topic in the planner | 13 |
| 77 | Placement and test-out (A9) | Onboarding ladders, stage-entry diagnostics, test-out, level checks (two items per skipped level, at least one at difficulty 4, between 5 and 20 items; a 3-day cool-down after a second fail), credited hours | 76 | The ladder algorithm on scripted answer sequences; priors written as specified; level-check sizes and cool-down at the boundaries | 5 |
| 78 | Exit parts and outside work (A10); creates the paste-verify exposure | Every instrument kind including `human-mark`, real papers sat typed in the app under their own timer with their `aids` text and a Bertie marking pass against the pasted official solutions, problem sets, projects, ledgers, book-log ("seen" outcome), mock log; paste-verify parsers | 70, 76 | Every instrument satisfied and not satisfied in tests; the Stage 0 checklist completes on a scripted learner; a real-paper confirm counts $\min(\text{learner}, \text{Bertie})$ per point; a "seen" book problem leaves both numerator and denominator; paste-verify rejects oversized and malformed pastes and stores redacted copies | 7 |
| 79 | Planner (A11) | Blocks, alongside shares, sessions, the 60% rule, the stage rule, the soft gate per level, hours with earned hours scaled by each item's estimate share, forecast, weekly review with reliance figures and the marking calibration score | 71, 72, 73, 78 | Planner tests; a 15-hour Stage 1 week matches 9/3/2/1; the next level enters Main only after its soft-gate condition or a remediation set, and an override is recorded; a completed item reads 100% of its hours | 8 |
| 80 | Daily 10 and weekly problems (A12, A13) | Daily 10 and Daily 5 orchestration, fact model, Zetamac and 80-in-8 rules; weekly probability scheduler with `original` problems only before 3.3, the `imitates` check, warm mode with Bertie after grading, one cold problem a week from 1.5 and two from Stage 2, the one-line plan before hints from Stage 1 and the daily cap on sealed tutor calls from Stage 2 | 71, 73, 29, 35, 58 | Median exit rule, voiding, weakest-fact selection; three weeks of weekly assignments for a scripted 1.5 learner, one of them cold; CI fails a pool that makes an imitation of Zhou chapters 4 or 5, or of any Mosteller, Crack or Joshi problem, eligible before 3.3 | 6 |
| 81 | Learning record and calibration (A15, P0 parts) | HTML record, CSV zip through `downloads`, calibration report | 72, 76, 78 | The record renders every section from the synthetic learner; the zip holds five valid CSV files; `downloads` absent falls back as specified | 4 |
| 82 | Web target (E9); creates the web-deployment exposure | Service worker, Keep offline, update flow, the persistent-storage request at the first completed lesson, CSP meta (`connect-src 'self'` plus the proxy origin), web manifest and icons, `pages.yml`, `serve:web`; the proxy deployed to Cloudflare `prod` with its secrets | 74a, 74b, 25, 62, 69, 70 | Offline and update end-to-end scenarios; zero CSP violations across the suite; a tagged deploy reaches the decision-13 host and installs on the iPhone, where a Python drill, a SQL drill, a handoff from the Artifact with its result code back and a live-code lesson screen finished from the Artifact all complete; under default (b) an anonymous request to the production site is refused by Access and the service worker's update check is tested across an expired Access session; the attack pass repeated against the deployed proxy; the Anthropic data policy checked and the first-run disclosure updated | 7 |
| 83 | Artifact target and release (E10); creates the published-page exposure | `page.ts`, the capability declaration (after loading the `artifact-capabilities` skill), the publish planner with batches, live-page re-send, the release ledger and its drift check, rebuild-and-verify of every file against the ledger, garbage collection and rollback from ledgers, the resume rule, peak check and maintenance path, Self-test, `docs/engine/RELEASE.md` | 74a, 74b, 25, 69, 70 | Planner tests for every rule; a release resumed after a simulated session death at each step converges to the same live listing; the built Artifact passes every end-to-end scenario in the emulator and contains no `node_modules` module and no binary; the first live publish passes Self-test on the iPhone (every locked CDN module loaded through the import map, a formula rendered as MathML) and the session reads `ops/selftest-<release>`; `meta/release` carries the ledger's hash; the declaration read back from the live Artifact equals the rule set of section 7.3 | 9 |

### 11.6 Content: stages 84 to 100

Stage 84 depends on stages 1 to 83; each course stage depends on stage 84 and on the course before it in the table, whose order is the depth-first order of `docs/CURRICULUM.md` with 0.4 and 0.5 interleaved as their item file sets them (K from week 1, B in week 2, Y after B). Each course is a release milestone made of level gates.

**Level gate definition of done** (one level: 4 to 7 lessons, its bank, level review and homework set, about 6 AD): every lesson meets the `CONTENT-FORMAT.md` 9.3 checklist and passes `zq check`, `zq verify` (both implementations agree on every auto-graded answer, misconception value and arithmetic claim; Monte Carlo agrees for probability items), grader replay, generator cross-checks over the full box, drill runs on CPython 3.12 and Pyodide with exactly their `needs`, storyboards (attached to the pull requests) at both widths and themes with no overflow or axe violation, and the copy and tutor leak lints; the **semantic review** passed: an independent reviewer agent, given only the English of every graded screen and item (no `verify` blocks, answers or diagnoses), writes its own restatement in the verify language, and `zqverify` checks that restatement against the authored answer, every disagreement resolved in the pull request; every citation carries a `loc`, free-source locations are checked by fetching them and paid-book locations are listed as warnings (`CONTENT-FORMAT.md` 9.3 rule 27); the level plays end to end on both targets in the emulator; the owner plays it on the iPhone through the preview Artifact and records the gate at `ops/gate-<level>`, judging the learning experience, not the maths.

**Course milestone definition of done:** every level gate passed; hours map to estimate units within the 10% rule; the course's topic paper (where it closes a topic) sits end to end; the tutor eval subset for the course passes (10 scenarios on its trap and hardest screens: 6 hint at rungs 1 and 2, 4 diagnose; 3 repeats; about USD 2; gold labels drafted by the authoring agent from the authored registers, checked by the semantic reviewer, approved by the owner for Stage 0 and by the decision-10 reviewer beyond it); from Stage 1 onwards, a paid human spot check of 5 lessons per course by a reviewer with a degree in the subject, findings fixed before release (decision 10); the course ships in a release to the live Artifact and the web app.

| # | Stage | Content | Lessons | Also | AD |
|---|---|---|---|---|---|
| 84 | Acceptance and first release (C11) | The reference lesson (`lsn.cond.shrinking-sample-space`, already authored) and the whole of level W1 of `crs.numwork`: its 5 lessons from `lsn.numwork.digit-worth`, bank, level review and homework `set.numwork.place-value` with drill `drl.num.divmod-check`; the real player on both targets, the full authoring workflow, Bertie on both backends, progress synced, and a real release. The rest of 1.5 level H1 waits for depth-first order | 6 | Owner approves the look against the prototype screen by screen; the drill hands off from the Artifact to the web app on the phone and its result code returns | 13 |
| 85 | `crs.numwork` How Numbers Work (0.1 W) | Levels W2 to W4 (W1 is in stage 84) | 16 | | 21 |
| 86 | `crs.keys` Keyboard Fluency (0.4 K) | K1, K2 | 8 | Runs alongside from week 1 | 10 |
| 87 | `crs.speed` Arithmetic at Speed (0.5 A) | A1 to A4, Daily 10 decks | 16 | 0.5 exit | 21 |
| 88 | `crs.bench` Workbench (0.4 B) | B1 to B3 | 13 | `shell-sim` drills | 17 |
| 89 | `crs.propprec` Proportion, Powers and Precision (0.1 P) | P1 to P4 | 21 | 0.1 topic paper and exit part | 31 |
| 90 | `crs.firstpy` First Programs in Python (0.4 Y) | Y1, Y2 | 10 | 0.4 exit | 15 |
| 91 | `crs.expreq` Expressions and Equations (0.2 E) | E1 to E6 | 34 | | 44 |
| 92 | `crs.lines` Lines and Linear Systems (0.2 L) | L1 to L3 | 20 | | 26 |
| 93 | `crs.quadpoly` Quadratics and Polynomials (0.2 Q) | Q1 to Q6 | 33 | | 43 |
| 94 | `crs.funcs` Functions and Graphs (0.2 F) | F1 to F4 | 24 | 0.2 topic paper and exit part | 35 |
| 95 | `crs.shape` Shape and Space (0.3 S) | S1 to S8 | 38 | | 49 |
| 96 | `crs.growth` Growth (0.3 G) | G1 to G5 | 27 | Precalc Lab parts | 35 |
| 97 | `crs.waves` Circles, Waves and Rotations (0.3 T) | T1 to T6 | 32 | | 42 |
| 98 | `crs.chance` Counting, Chance and Data (0.3 C) | C1 to C5 | 26 | | 34 |
| 99 | `crs.rigour` Proof, Limits and Curves (0.3 R) | R1 to R5 | 23 | 0.3 topic paper (two timed sections) and exit part | 34 |
| 100 | Stage 0 exit | Stage 0 papers, the `s0.*` exit parts (GCSE-style and Khan-style confirm steps), Stage 0 review | | Owner sits the in-app papers | 10 |

### 11.7 After Stage 0

Stage 1 follows the same rule: level gates in curriculum order and one release milestone per course (1.1 to 1.9, with A1 between 1.3 and 1.4 and 1.7 alongside 1.3 to 1.6 as the curriculum sets it). All P0 widgets already exist. Each P1 wave (`WIDGETS.md` 7.4: 1.6, 1.7, 1.8, 1.9) is built in batches by the same rules immediately before its item's first level gate, and P2 waves likewise before Stage 2; each wave's bespoke composites are classified by section 3.2 rule 3 when it is briefed, and the waves' cost (about 470 AD with contingency, section 11.2) is re-forecast from the P0 batches' measured rates. Every Python load group is in the web build from stage 25 (section 5.7). The adopted additions are already in the curriculum files (decision 2): Stage 2 opens with 2.0a and 2.0b, and their P2 widgets and services are built in the first Stage 2 waves, 2.0a's before 2.0b's, then 2.1b's and 2.2c's (`WIDGETS.md` 7.4).

---

## 12. Decisions for the owner at approval

Each decision names the first stage that needs it and the default that applies if the owner has not decided by then. **Decisions 1 to 12 were decided at Blueprint review on 7 October 2026** (last column): decisions 1, 2 and 4 by the owner's choice, decision 7 by his correction of the publishing rule, and the rest at their stated defaults. **Decisions 13 and 14 were raised by the second review round** (section 13) and decided by the owner at the Blueprint approval the same day: (b) for both.

| # | Decision | Options | Recommendation | Needed by | Default | Decided (7 October 2026) |
|---|---|---|---|---|---|---|
| 1 | Build order, and where content starts (section 11.2) | (a) As planned and instructed: every P0 widget batch before any content, content depth-first from 0.1; learner and content meet about October 2028 (November 2028 after revision 2), late in 1.5. (b) A companion release first: stages 1 to 9a, 20, 23 (curriculum and plan data), 29, 35 (`strategy-trainer` only), 59 to 63, 69 to 71, 73, 74a, 74b, 78 (outside work and real-paper logs), 79, 80, 82 and 83, plus a pasted-problem chat mode for Bertie (`AI-TUTOR.md` 2.13, about 4 AD), about 200 AD in all, so the learner studies the canonical resources with the planner, outside-work log, Redo queue over textbook problems, Daily 10, weekly problems and Bertie from about March 2027; the library follows, and stage 83 still ends about August 2027, because these stages are reordered, not added (4 AD more); learner and lessons still meet about October 2028 (November 2028 after revision 2). (c) Content starts where the learner will be when stage 83 ends (forecast: 1.1, August 2027) and proceeds depth-first from there; Stage 0 is backfilled afterwards by a fifth session; learner and content meet about September 2027. (d) The earlier option: Stage 0 content after stage 41 and the stages it needs from 59 to 83, with W4 to W7 in parallel | (b) with (c): the learner uses the app from about March 2027 and meets authored lessons in 1.1 about September 2027. It departs from the instruction to build every widget before content and to author Stage 0 first, which is why it is the owner's call | Stage 3a (the session plan) | (a) | **(a)**, by the owner: every P0 widget batch before any content; content depth-first from 0.1. Revision 2 forecasts content meeting the learner about November 2028 (section 11.2) |
| 2 | Curriculum additions from `canon-gap.md`, with the review's 2.1b (hours net of what the item files already teach; consequences in the table below) | P1 research method 35; P2 continuous-time processes +15; P3 numerical methods and Monte Carlo 120; P4 optimisation 80; P5 inference second pass +25; P6 portfolio, risk, fixed income 75; P7 proof and discrete maths 70; P8 differential equations 45; P9 information theory +20 (the 2.1 file advises about 12); P10 matrix calculus +10 (the 2.1 file advises withdrawal); P11 financial econometrics 80 + 15; P12 microstructure 50; P13 systems and performance 150 (developer track); P14 ML research track 380; P15 Bayesian computation 40; P16 derivatives add-on 370; O1 contests offset -80 outside the developer track; **2.1b deep learning core, 120 h** (Prince, *Understanding Deep Learning*, chapters 1 to 12; Karpathy's *Neural Networks: Zero to Hero* re-implemented in NumPy so that micrograd, an MLP and a character-level transformer at toy scale run in Pyodide; the MIT 6.7960 problem sets; a toy double-descent replication as a 3.1 option); about 60 h of real analysis after 1.3 on the researcher and ML tracks (Abbott, *Understanding Analysis*, chapters 1 to 6), taken from P7 or P16 | **Core, not a cap option: P1 to P4 with O1 (net +170 h) and 2.1b (+120 h): 3,390 h; 3,450 h with the analysis on the researcher and ML tracks.** Without 2.1b the stated aim of ML-lab-calibre thinking is not delivered and should be dropped from section 1; the four subjects of P1 to P4 are core in every programme `canon-gap.md` surveys. All proposals: 3,565 to 3,820 h by track. Each accepted proposal adds widgets, modes and possibly a Python group (table below); none changes the engine's contracts | Stage 44 for P2 (its `path-simulator` modes); stage 54 for the rest; stage 25 if P4's `optimisation` group is to be measured on the phone with the others | No additions, and section 1's ML-lab aim is then dropped | **Adopted as recommended**, by the owner: P1 as item 2.2c (35 h, before 2.3), P2 inside 1.5 (+15 h), P3 as item 2.0a (120 h, first in Stage 2, all tracks), P4 as item 2.0b (80 h, before 2.1), O1 (-80 h outside the developer track), 2.1b (120 h, after 2.1, all tracks), A1 (60 h after 1.3, researcher and ML research tracks): 3,390 h, 3,450 h on those two tracks. P5 to P16 not adopted, P8 included, so files that listed P8 teach its basics themselves. The ML-lab aim of section 1 stays |
| 3 | Curriculum decisions D1 to D8 (`CURRICULUM.md` 6.3) | GCSE geometry and statistics inside 0.3; Khan precalculus units in 0.3; 3.2 counted at 150 h when taken; an exit for 2.4; topic papers for 2.3, 3.1, 3.3 and Arena rounds; `3.3.books`; three projects on the Trader track; mocks with Bertie not counting | As each item file recommends | Stage 95 (D1 and D2 affect Stage 0 content); the rest by the first level gate of their item | As each item file recommends | **Defaults**: as each item file recommends (owner decision 4; `CURRICULUM.md` 6.3) |
| 4 | Bertie's face | Confirm the hairline, lidded eyes and resting smile of `BERTIE.md` draft 2 | Confirm | Stage 59, before its visual baselines | Draft 2 as drawn | **Confirmed as drawn except the hair**, by the owner: soft, rounded, fuzzy tufts instead of points (`BERTIE.md` draft 3); he signs off the redrawn hair at stage 59 |
| 5 | The sealed answer key | `tutor.answerKey: 'sealed'` (Bertie sees the key behind the leak probe) or `'never'`; per backend | `sealed` on the web; on the Artifact, `sealed` only for the tiers that pass the judged tier run, `never` for any that fails (`AI-TUTOR.md` 9.6) | Stage 61 (context assembly) | As recommended | **Default**: as recommended |
| 6 | Cloudflare plan for the limiter | SQLite-backed Durable Objects on the Workers free plan [recalled, unverified: offered since 2025]; the Workers paid plan [recalled, unverified: about USD 5 a month]. The Rate Limiting binding with KV and eventually consistent day totals is withdrawn: consistent spend counters are the control on the key | Whichever plan offers SQLite-backed Durable Objects, checked at stage 62 | Stage 62 | The paid plan if the free plan lacks them | **Default**: the plan by the stated rule, checked at stage 62 |
| 7 | Platform questions to Anthropic (draft 1) | Draft 1 asked whether JSON parts of wheel members, and repackaged third-party binaries a session built and verified, could be published | Withdrawn | | | **Replaced by the owner's correction**: the Artifact publishes only files generated from our sources; third-party JavaScript from CDNs at exact versions; no Python, SQLite or KaTeX fonts there; every code drill hands off (section 4.3). Nothing goes to Anthropic |
| 8 | Copyright and writing rules | The adapted-problem rule (`CONTENT-FORMAT.md` 9.4); the glossary exemption for standard technical terms that contain a word on the banned list (`CONTENT-FORMAT.md` 13 item 11); a licence for the content when published | Sign off the problem rule; allow the glossary exemption; decide the content licence before anything is public | Stage 7 for the exemption (the copy lint); stage 84 for the problem rule; before anything is public for the licence | Exemption allowed; problem rule as written; no public release | **Defaults**: problem rule as written, glossary exemption allowed, no public release |
| 9 | Weekly hours split | 9/3/2/1 with borrowing from Main, or 8/3/3/1 from Stage 1. The rerun simulation [simulated, `ASSESSMENT.md` 6.5]: maintenance at level grain with the core-interview holds is 1.45 h a week on average, 2.3 h in the last half-year and 2.7 h at its 4-week peak, plus about 0.6 h of older redo: about 2.05 h on average and 2.9 h late, so 9/3/2/1 holds on average and needs nearly the full hour of borrowing late in the path; with 1.6 held as core-interview on the researcher track, maintenance reaches 2.8 h late and 3.4 h with redo, beyond the block plus its hour of borrowing | 9/3/2/1 with up to 1 h of borrowing; 8/3/3/1 from Stage 2 on the researcher track | Stage 79 | 9/3/2/1 with borrowing | **Default**: 9/3/2/1 with borrowing |
| 10 | People outside the app | (i) A person (study partner, tutor or paid marker) marks one finals-style sitting per Stage 1 maths topic (1.3, 1.4, 1.5, 1.6), the `human-mark` confirm of their exits; (ii) a paid reviewer with a degree in the subject spot-checks 5 lessons per course from Stage 1 [cost unverified] | Both | (ii) by the first Stage 1 level gate; (i) by the first Stage 1 exit | Both, paid; if declined, the records and course reports say "no external check" | **Default**: both, paid |
| 11 | The reliance check | Switch Bertie off for a random 20% of skills (chosen by `hash32` of the skill and a learner seed) and compare 30-day redo success with the rest in the weekly review | On, with a Settings switch | Stage 79 | On | **Default**: on |
| 12 | Earlier habits | (i) One interview-style problem a week from 0.3 level C4, rising to three at 1.5; (ii) on the Trader track, one market-making game a week from 1.7 level MK1 in `mm-game` practice mode (a P1 widget) | Both | Stage 80 | Off | **Default**: off |
| 13 | Where the web app is served before a content licence exists (raised by the second review round). Decision 8's default is no public release, but stages 25 and 82 deployed to GitHub Pages, which serves any visitor who has the address [recalled, unverified: only GitHub Enterprise Cloud offers access-controlled Pages], so lesson content, adapted textbook problems included, would have been public from stage 25. The repository is private [measured, GitHub REST API, 7 October 2026] | (a) GitHub Pages, unlisted but world-readable: counts as public, so the content licence (`STATE.md` open question 18) and the `CONTENT-FORMAT.md` 9.4 sign-off are needed before stage 25's first deploy, and a public deployment triggers the Class D review of section 7. (b) Cloudflare Pages behind a Cloudflare Access policy that admits only the owner's account, until he chooses a licence; `serve:web` locally as before; GitHub Pages becomes the public-release path, used only after the licence decision and the Class D review. Cost: none expected [recalled, unverified: Access free for up to 50 users; checked at stage 25]; the Cloudflare account already exists for the proxy. (c) Local only (`serve:web`): no access control needed, but no handoff from the Artifact on the phone away from the owner's network | (b): the only option that keeps decision 8's "no public release" and the phone handoff the Artifact's drills depend on. It departs from the brief's "GitHub Pages or local" only in which static host serves the same files, which is why it is the owner's call | Stage 25 (its development deploy) | (b) | **(b)**, by the owner ("CloudFlare is fine"): Cloudflare Pages behind an Access policy admitting only his account until he chooses a content licence; GitHub Pages stays the public-release path |
| 14 | The Stage 3 Zhou exit line (`docs/CURRICULUM.md` 6.2 and 6.4; raised by the second review round) | (a) `3.3.zhou` stays at Zhou chapter 4 logged cold at 80%. (b) canon-gap 4.4's line with P2: 80% of chapter 4 and 70% of chapter 5 cold; `stage3-stochastic-interview.md` (level PZ6's reading row) already makes chapter 5 join the exit at 70% if P2 is accepted, and P2 was adopted | (b): P2's levels Z4b and Z4c and 3.3's level PZ6 teach chapter 5's processes and Itô's formula at interview depth to every learner, so the line measures what the path teaches | Before the 3.3 wave is briefed | (a) until the owner confirms | **(b)**, by the owner ("Add in chapter 5"): a new exit part `3.3.zhou-ch5`, Zhou chapter 5 logged cold at 70% in the learner's own copy, beside `3.3.zhou` (chapter 4 at 80%, unchanged); its 7 hours move out of `3.3.books`; `docs/curriculum.md` gains the checkbox |

**Duration** [simulated: `ASSESSMENT.md` 6.5's FSRS rerun for maintenance and the planner's block rules for habits; our estimate for the 60 h of retention sittings]. Total hours count the mapped hours, the Daily 10 after 0.5, the weekly probability problems from 1.5, maintenance review and retention sittings; years are at 52 study weeks, with 46 study weeks a year in brackets (`docs/CURRICULUM.md` 6.5):

| Scope (mapped hours) | 10 h a week | 15 h a week | 25 h a week |
|---|---|---|---|
| Draft 1 (3,100) | 4,170 h: 8.0 years (9.1) | 3,820 h: 4.9 years (5.5) | 3,550 h: 2.7 years (3.1) |
| **Adopted, trader track (3,390)** | 4,570 h: 8.8 (9.9) | 4,180 h: 5.4 (6.1) | 3,880 h: 3.0 (3.4) |
| **Adopted, researcher or ML research track, with A1 (3,450)** | 4,650 h: 8.9 (10.1) | 4,260 h: 5.5 (6.2) | 3,950 h: 3.0 (3.4) |

The developer track's 3,470 mapped hours were not simulated; they are 20 h more than the researcher row [inferred]. The curriculum's "roughly 4.3 years at 15 hours a week" counts mapped hours only. At 15 h a week, draft 1's scope added about 360 h of habits and 360 h of maintenance and retention sittings.

**What the adopted additions ask of the build** (`WIDGETS.md` decisions 17 and 18, 0.3; none adds an Artifact file beyond its course bundles):

| Addition | New widgets | Changes to existing widgets | Python (web app) | Tutor |
|---|---|---|---|---|
| P1 Research method (2.2c) | `bias-audit` (P2); `forking-paths` is `multiple-testing`'s `garden` mode | 2.2c modes on `backtest-lab`, `sharpe-lab`, `test-lab`, `icon-array`, `contingency-table`; `@zq/models/research` | `numpy-pandas`, `scipy-statsmodels` | `results-note` marking against the P1 checklist |
| P2 Continuous time (1.5 levels Z4b, Z4c) | none: `ctmc-clock` and `brownian-path` are modes of `markov-chain` and `path-simulator`, now P0 | those two modes and `first-step-solver`'s continuous-time mode, P0 (stages 44, 54, 56) | none | none |
| P3 Numerical methods (2.0a) | `backward-error`, `convergence-plot`, `interp-lab`, `fd-grid`, `rng-lab`, `mc-variance` (P2 scenes) | with 2.0b, 29 modes on 16 widgets; `@zq/models/numerics` | `numpy-pandas`, `scipy-statsmodels` | none |
| P4 Optimisation (2.0b) | `feasible-region`, `dual-pair`, `convex-set`, `frontier-lab` (P2 scenes) | as P3; `@zq/models/optim` | a new `optimisation` group [present in Pyodide 314.0.7's lock; untested in a browser] | none |
| 2.1b Deep learning | `training-curves`, `autodiff-tape`, `lm-sampler`, `conv-lab`, `attention-lab`, `tokeniser-lab` (P2 scenes) and the preset `scaling-plot` | a tensor autodiff in `ml-core` | `numpy-pandas` | code review on longer drills |
| A1 Real analysis | `bound-lab`, `quantifier-game`, `cardinality-lab`, `proof-builder`, `line-topology`, `uniform-lab` (P0 scenes, stage 51a) | ten modes on nine P0 widgets (stages 36 to 50); `@zq/models/analysis` (stage 3g) | standard library (`zq_ra` prelude) | proof marking: the mark mode's gold set gains A1's proofs |
| O1 Contests offset | none | none | none | none |

---

## 13. Review log

### 13.1 Second review round, 7 October 2026 (after revision 2)

29 findings (1 blocker, 12 majors, 16 minors), all fixed as the findings ask, here and in the files named. One extension beyond a finding's fix is declined, with its reason in row R1. "Changed" marks a fix that departs from the finding's suggested wording.

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| R1 | B | 11 of 15 item files still brief content agents with "Pyodide on both targets" and open Artifact-build items | Fixed: a binding revision 2 header row in each of the eleven (no Python, SQL or C++ in the Artifact; drills, code items and live-code screens hand off by result code; papers with code items sat in the web app; CI parity CPython 3.12 against Pyodide on the web app); precalc 7, calculus 3, ml-papers 3, probability 5 and statistics 7 with its capstone row closed by the rule; the revision note's item 7 names the files. Changed: the decision rows, runtime paragraphs and paper rows the finding named were also corrected in place. Other "both targets" mentions in the files' bodies stand under the binding row, which says how to read them; **declined** for now: they are rewritten when content agents write the lesson files, since rewriting about 40 body lines now adds no decision |
| R2 | M | `code-cell`, `expression-input` and `live-formula` entries contradict the rule | Fixed: `WIDGETS.md` entries rewritten per target (`code-cell` web only with its Artifact handoff state; the plain field with symbol bar and MathML preview primary in the Artifact; MathML-only output and sentinel slots) |
| R3 | M | `AI-TUTOR.md` T6b and its tidy row; real analysis not proof-heavy; request 13 unapplied | Fixed: T6b on Pyodide in the web app; the tidy row marked superseded; `top.real-analysis` proof-heavy; the subject rules of A1, 2.0a, 2.0b, 2.1b and 2.2c in 3.1; Bertie away during 2.2c's exit audit and A1 portfolio writing (2.12) |
| R4 | M | `ASSESSMENT.md` keeps draft 1's totals in Scope, 8.7 and 13.3 | Fixed in place and in its revision 2 table: $P$ is the track total (3,390, 3,450, 3,470), the example reads 3,390, the fold budget about 121,000 events; the all-proposals range dropped |
| R5 | M | A live-code lesson screen has no outcome in the Artifact | Fixed: section 4.3's rule (resolve as `read`, no XP, "Finish in the web app" item, result code keyed by lesson id, `rev` and screen id); `ARCHITECTURE.md` 5.7.2 rows; `ASSESSMENT.md` 14.3; each code-running `WIDGETS.md` entry states its Artifact mode; stages 24, 70 and 82 test it. Changed: `parsons` plays fully, because its `ordering` answer needs no execution |
| R6 | M | Code widgets never device-checked running at their gate | Fixed: batches 32, 41, 46 and 48 are also checked in the web app on the iPhone through stage 25's development deploy, both targets in `ops/gate-<stage>` (11.1, 11.4) |
| R7 | M | 11.7 prices the waves at draft 1's 370 AD | Fixed: about 470 AD (section 11.2) |
| R8 | M | Conflict 1 and `ARCHITECTURE.md` decision 36 keep draft 1's counts | Fixed: 338 ids, 192 P0, 277 composites, 131 of 153 P0 composites as scenes; about 240 AD less; the `WIDGETS.md` note marked as draft 1's |
| R9 | M | The spike S1 list disagrees across four documents; the external link unchecked | Fixed: stage 2 (c) is the single list, with `version.json` caching, a publish without the page, `null` removals and inline styles added, and the external anchor named as the handoff link; `ARCHITECTURE.md` E0 and `STATE.md` open question 5 mirror it |
| R10 | M | Open decisions and pending edits from `CURRICULUM.md` untracked | Fixed: `STATE.md` open questions 21 (Zhou line), 23 (paid spines, by stage 84) and 24 (the 2.3 re-cut, before stage 6), and a Pending document edits table for requests 1 to 13 with owning stages; the Zhou line is decision 14 here and open owner item O2 in `DECISIONS.md`; `stage1-finance-projects.md`'s header row stops agents authoring the 24 moved or retired lessons |
| R11 | M | README says the Blueprint is approved | Fixed: "awaits his 'approved, continue'" |
| R12 | M | GitHub Pages makes content public from stage 25 against decision 8's "no public release"; repository visibility unstated | Fixed: decision 13 with options and default (b), Cloudflare Pages behind Access until a content licence; Class D wording in sections 1 and 7; repository private [measured]; stages 25 and 82, 7.1, 7.3, 7.6, 8.6 and 9 follow. Changed: recorded as an open owner decision with a default, because (b) departs from the brief's "GitHub Pages or local" |
| R13 | M | Provenance misses the esbuild-built generator modules | Fixed: `provenance.ts` reads esbuild's metafile too (3.1, 4.3; `ARCHITECTURE.md` 6.2.7); stage 4 tests a planted import in a fixture generator |
| R14 | m | Two `TexSlots` binding paths; `<mtext>` digits in the text font | Fixed: sentinels on both outputs, the MathML `<mtext>` swapped for an `<mn>` by `createElementNS`; 6.5, conflict 10, `ARCHITECTURE.md` decision 37, 5.11, 11.3, `DECISIONS.md` S1; slot digits in the stage 2 specimen. Changed: the narrow `\htmlData` callback stays for term anchors on the web; slots no longer use it |
| R15 | m | "Exactly one" sink against "exactly two" | Fixed: 7.2 and `ARCHITECTURE.md` 11.3 say two, with the lint extension of S2 |
| R16 | m | Researcher-row durations misprinted | Fixed: 8.9 (10.1) and 3.0 (3.4) here and in `CURRICULUM.md` 6.5 |
| R17 | m | Decision 1's options say October 2028 | Fixed: "(November 2028 after revision 2)" |
| R18 | m | Terms table omits 10b, 74a, 74b | Fixed |
| R19 | m | Counts mix bases; 398 works; 1,500 skills | Fixed: "25 items plus optional 3.2"; 11.2 excludes 3.2 (104 lessons, about 146 AD) by name; about 506 source ids; about 1,700 skills after revision 2 |
| R20 | m | Rows 2, 3, 8, 14 and 22 below cite draft 1 states | Fixed: the note at the head of 13.2 |
| R21 | m | Stale details in `ARCHITECTURE.md`, `CONTENT-FORMAT.md`, `AI-TUTOR.md` | Fixed in place: presets 24, one bundle per course, CPython 3.12, esbuild per topic, four pilots and 338 ids, the whole-path learner, the JSON-part layout not built, decision 31's one Python target; `CONTENT-FORMAT.md` decision 13's 103 courses in 26 topics; open items 8 and 11 and `AI-TUTOR.md` 8.7 closed at decision 8's defaults |
| R22 | m | Missing dependencies (25 on 10b and 24; A1 modes on 3g; 4 on 2) | Fixed here and in `STATE.md`: 3g added to batches 36, 39, 49 and 50, since their A1 modes may use `@zq/models/analysis` |
| R23 | m | Stage 1 creates files that already exist | Fixed: stage 1 keeps the handoff pack current |
| R24 | m | D6 says the probes "are deleted" on an unscoped listing | Fixed: "to be deleted; not found in the listing (scope: mine)"; `STATE.md` open question 22 deletes either if found, with the owner's confirmation |
| R25 | m | ML bullet says widget models run in NumPy | Fixed: `ml-core` on both targets; drills in NumPy on the web app |
| R26 | m | Stage 84 missing from the phone-closed list; copy shown inside the web app | Fixed: 84 added; "Open it on a computer." |
| R27 | m | `@preact/signals-core` unlisted | Fixed: 1.14.4 (MIT) in `ARCHITECTURE.md` 3.1 and 4.2 |
| R28 | m | `WIDGETS.md` calls A1's batch W5b | Fixed in the source: W5d everywhere; conflict 22 resolved |
| R29 | m | README totals and overclaim; "roughly 4 years" | Fixed: 3,470 on the developer track and the narrowed wording in README; "roughly 4.3 years" here and in the `CURRICULUM.md` header |

### 13.2 First review, 7 October 2026 (draft 1)

Figures in this table are draft 1's; revision 2 superseded rows 2 (3a to 3g cost 61 AD), 3 (contingency 182 AD), 8 (F1 and F2 withdrawn by the publishing rule), 14 (decision 7 withdrawn) and 22 (the threshold is 34 MB a participant), as the revision 2 note at the top of this plan says.

Review of 7 October 2026: 60 findings (4 blockers, 32 majors, 24 minors), each fixed here and, where it belongs, in the appendix named; none declined. Severity: B blocker, M major, m minor. "Changed" marks a fix that departs from the finding's suggested wording, with the reason.

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| 1 | B | Tutor eval gate cannot run inside the learning caps; judge key unloaded; nightly evals contradict 9.1 | Fixed: eval environment (`[env.eval]`, `.env.eval`, USD 60 and 2,000 requests a day for tutor calls, a runner cap of USD 75 a run for judge calls), eval budget (5.5; about USD 31 a run with the judge on `claude-sonnet-5-5`), eval keys in 7.1 via `node --env-file`, nightly deterministic only (10); `AI-TUTOR.md` 9.1, 9.6, 10.1 |
| 2 | M | Domain services had no stage, cost or parity plan | Fixed: stages 3a to 3f, 56 AD, parity against the pinned versions; `WIDGETS.md` 3, `ARCHITECTURE.md` 4.3 |
| 3 | M | Scene rates unproven on heavy models; no contingency; unbounded revert | Fixed: fourth pilot `svd-stepper`, per-family recalibration, 40% contingency (178 AD), AD recorded from stage 1, worst case bounded (3.2) |
| 4 | M | No end-to-end forecast; AD not measurable | Fixed: AD as 6 session-hours from logs; whole-programme forecast against the learner (11.2); levers decided (four sessions, level review, semantic reviewer) |
| 5 | M | The owner, also the learner, is the only semantic check | Fixed: independent reviewer's restatement checked by `zqverify`, paid spot check of 5 lessons a course from Stage 1, owner reviews per level (11.6; `CONTENT-FORMAT.md` 6.13, 9.1) |
| 6 | M | `AppendQueue` built after the stages that use it; 82 and 83 deps | Fixed: A1 moved to stage 9a with its contract suite; 68 kept empty; 69 and 70 added to 82 and 83 |
| 7 | M | Release drift, garbage collection and rollback read ignored output; no resume | Fixed: committed release ledger with its hash in `meta/release`; resume rule (8.6; `ARCHITECTURE.md` 6.2.6) |
| 8 | M | One fallback for two failures, and it does not fit or answer policy | Fixed: F1 and F2 with budgets and Stage 0 effect; default for an unanswered decision 7 (4.3, 5.6, 12) |
| 9 | M | Five item files still prescribe MicroPython tags and a Parsons fallback | Fixed: header tables in the five files; open item 7 closed; no Parsons fallback on a handed-off screen (`WIDGETS.md` 5.1.1) |
| 10 | M | No quality gate on the Artifact tiers | Fixed: judged Artifact tier run, per-tier gates and fallback ladder (`AI-TUTOR.md` 9.6). Changed: the ladder takes the key away first, then moves tiers, because moving hints to `default` costs seconds of latency |
| 11 | M | Decision 2 said "no architecture"; no deadline | Fixed: consequences table and deadlines (12). Changed: P2's deadline is stage 44, where `path-simulator` is built, not 54 |
| 12 | M | Baselines for every storyboard state would swamp git | Fixed: baselines for widget fixtures and app screens only, on an orphan branch, with a budget; storyboards as artefacts (conflict 16) |
| 13 | M | Gates too large; rejected gates mean reverts | Fixed: level gates, stage branches, stage 10 and stage 74 split (11.1, 11.3, 11.5) |
| 14 | M | Read-before-publish rule unaddressed for 190 MB of files | Fixed: rebuild and verify against the ledger in the session; hand-written files read in full; provenance question added to decision 7 |
| 15 | M | Production limiter untested before production | Fixed: Workers-runtime tests, SQLite-backed class pinned, attacks on deployed `dev` at stage 62 |
| 16 | M | Exact citation locations demanded with no means to check them | Fixed: rule 27 sharpened; free sources fetched, paid books checked as read (conflict 17) |
| 17 | M | `zq preview --artifact` in no stage; previews pile up | Fixed: built at stage 25; one long-lived preview Artifact; results at `ops/gate-<stage>` |
| 18 | m | Stage 25's matplotlib condition read two ways | Fixed: passes on `stdlib` and `numpy-pandas`; the rest recorded (conflict 9) |
| 19 | m | One lesson per pull request against an 800-line cap | Fixed: content rule without a YAML cap; generators in their own pull requests (11.1) |
| 20 | m | Agents could apply the label and merge | Fixed: `main` protected with `CODEOWNERS`, bot identity, `label-guard.yml` (7.6) |
| 21 | m | "Add to eval set" commits learner text | Fixed: paraphrase redaction and a CI flag check (5.1, 7.5; `AI-TUTOR.md` 9.7) |
| 22 | m | Unbounded `db` probe; placed in A2 | Fixed: paced probe to 60 MB, then deleted; moved out of A2. Changed: the threshold is 30 MB a participant, the recomputed log of 13.6 |
| 23 | m | Core split cannot shrink `core`; `code-cell` and `parsons` cycle | Fixed: one-way composition; `core-code` fallback measured after stage 32 |
| 24 | m | Stage 84's scope stated three ways | Fixed: reference lesson plus level W1 of `crs.numwork` with its drill; C11 matches (conflict 12) |
| 25 | m | `sys.monitoring` absent on 3.11; Python pins unlisted | Fixed: floor raised to 3.12 after measuring that SciPy 1.18.0 needs it; `tools/py/uv.lock` (conflict 19) |
| 26 | m | Licence list fails common development dependencies | Fixed: strict list for shipped code, wider list for tools (7.6) |
| 27 | m | GitHub API remnants; volumes from 1,550 lessons; probe in A2 | Fixed: `ASSESSMENT.md` 2.9, 11.4, 13.6 (about 106,000 events), 18, 19 |
| 28 | m | Stale statements in four papers | Fixed: `ARCHITECTURE.md` 6.2.3, decision 29, risk 5; `CONTENT-FORMAT.md` 13 item 1, C8; `canon-gap.md` 5 |
| 29 | m | First-download prompt fixed at 24 MB | Fixed: size computed from the uncached groups `needs` requires (8.1) |
| 30 | m | Tool-loop blocks unsigned; results only size-capped | Fixed: HMAC on `turn` blocks; results schema-checked at 4 KB (7.2, 7.4; `AI-TUTOR.md` 6.3) |
| 31 | m | Nothing loads `.env`; `.dev.vars` undocumented | Fixed: `--env-file`, `.dev.vars`, example files, fail-fast start-up (7.1, 8.3) |
| 32 | m | Token entry and `version.json` unvalidated | Fixed: two entry-point rows (7.2) |
| 33 | m | Most decisions lack deadlines | Fixed: needed-by and default columns (12) |
| 34 | m | "Every answer proved twice" overclaims | Fixed: narrowed in 1 and 2; code and long-form grading named separately |
| 35 | B | Mastery model sized for the wrong number of skills | Fixed: level grain, `introduces` at most 2, step tags, card budget; simulation rerun (299 h, 2.3 h a week late) and published before decision 9 (conflict 18; `ASSESSMENT.md` 4.1, 6.5) |
| 36 | B | Every written gate self-marked | Fixed: blind self-mark then the lower of two per point, disputed list, provisional with the tutor off, typed real papers marked by Bertie, `human-mark` confirms (6.5; decision 10). Changed: typed sittings, not P0 handwriting, because the owner's iPhone view has no image input |
| 37 | B | Weekly bank spends the problems the 3.3 exit counts as cold | Fixed: `original` only before 3.3, `imitates` tags with a CI check, "seen" leaves both counts (conflict 14) |
| 38 | M | Unlimited diagnostic sittings | Fixed: one diagnostic per paper, model answers withheld after a fail, pools of 12, retirement (`ASSESSMENT.md` 3.2, 3.7, 3.8, 7) |
| 39 | M | Fixed slot map names the method | Fixed: shuffled order, method-free stems, cross-method pools, two unlabelled slots (`ASSESSMENT.md` 3.2; 1.5 file 4.1) |
| 40 | M | The 4-year headline omits habits, review and holidays | Fixed: duration table (12; `CURRICULUM.md` 6.5); earned hours scale by estimate share (`ASSESSMENT.md` 8.7) |
| 41 | M | The app trails its only learner by about two years | Fixed: decision 1 with options, meeting dates and a recommendation; default the owner's instruction |
| 42 | M | Nothing inside an item holds the learner back | Fixed: planner soft gate per level with overrides (`ASSESSMENT.md` 8.5) |
| 43 | M | Proof objectives, recognition quizzes | Fixed: production item on Prove, Derive and Show lessons, "write the missing step", self-explanation prompts (rules 15 and 38) |
| 44 | M | Homework blocked by level | Fixed: 25 to 30% from earlier levels and topics, "which tool?" items, reviews across courses (`ASSESSMENT.md` 2.4, 2.5) |
| 45 | M | Interview-level skill never maintained | Fixed: `core-interview` tier at 0.90 with stretch cards at 0.80, balancer lowers non-core first (`ASSESSMENT.md` 5.2, 5.4) |
| 46 | M | Nothing re-tests a topic after its exam | Fixed: retention sittings at 3 and 12 months that reopen a topic below 60%; Stage 1 and Stage 2 cumulative papers (`ASSESSMENT.md` 3.8, 2.9) |
| 47 | M | Method comments before Check leak the verdict | Fixed: no comment on typed work before a first Check, chip moved, nothing typed sent, paired evals (`AI-TUTOR.md` 2.6, 3.3, 3.4, 4.2, 9.2) |
| 48 | M | Help offered before an attempt | Fixed: per-screen availability, `trap` screens after a first Check, sealed `explain` limited to two depths, 10 scenarios (6.5; `AI-TUTOR.md` 2.2, 2.5) |
| 49 | M | Evals miss the daily target and dependence | Fixed: judged Artifact tier run, judge on a different model plus 30 owner-graded replies, reliance figures, the 20% reliance check (decision 11) |
| 50 | M | Support never fades | Fixed: warm means Bertie after grading; cold weekly problems from 1.5; plan line from Stage 1; daily cap from Stage 2 (conflict 15) |
| 51 | M | Learner anchors on Bertie's marks; 20 mark scenarios | Fixed: blind marking first, calibration score, gold set of 100 with 25 fluent but wrong. Changed: gold beyond Stage 0 is marked by the paid reviewer, since the owner cannot mark what he has not learned |
| 52 | M | Lesson-creator's final-test mix and adaptive pace missing | Fixed: `topic` kind floor 30% and target 40% long-form, applied items, `consequence` line, `fastPath` (rule 35) |
| 53 | M | ML-lab aim not delivered | Fixed: 2.1b recommended as core in decision 2; without it the aim is dropped, as section 1 and 9 state |
| 54 | M | P1 to P4 offered only as a cap | Fixed: recommended as core with O1; 60 h of analysis on research tracks (decision 2) |
| 55 | m | Weekly problems start late; no betting games on the trader track | Fixed: proposed as decision 12 |
| 56 | m | "Mastered" means two things | Fixed: the lesson star is "Passed" |
| 57 | m | Five items credit a skip | Fixed: two items per skipped level, one at difficulty 4, 3-day cool-down |
| 58 | m | Long-form redo repeats the read answer | Fixed: required siblings; Hard cap without one |
| 59 | m | Uniform time guesses; all Stat 110 lectures | Fixed: estimates by difficulty (rule 37); lectures pull-based; 1.5's hours re-balanced |
| 60 | m | Attestation "without notes" against printed rules; reserved finals easy to open | Fixed: `aids` per paper; the planner names reserved papers at the start of 1.3 to 1.5 |
