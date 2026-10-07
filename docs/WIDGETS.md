# Widget library

Definitive library for Zero to Quant, Stage 2 Phase 1 (Blueprint), 6 October 2026. It merges the six widget catalogues in `docs/blueprint/work/` (`widgets-stage0.md`, `widgets-calc-linalg.md`, `widgets-prob-stats-ts.md`, `widgets-programming.md`, `widgets-finance-games.md`, `widgets-ml-research.md`) into one set of final ids, consistent with the engine architecture (`docs/ARCHITECTURE.md`), and checks it against every lesson in the eleven curriculum files in `docs/curriculum/`. Input to `docs/PLAN.md`.

**What this file owns.** Every widget's final id, tier, kind, cluster, priority, build size and build order; which primitives each composite composes; the name map from catalogue ids to final ids; the merges; and the coverage check against the curriculum. **What it does not own.** Each widget's detailed behaviour (interactions, visuals, show-why recipes, generators, misconceptions) stays in the catalogue section named as its "spec", as `ARCHITECTURE.md` says ("the widget catalogues own each widget's behaviour"). Where this file and a catalogue disagree on a name, a priority, a merge or a contract detail, this file wins. The agent-facing authoring guide, `docs/engine/WIDGET-AUTHORING.md` (arch 10.5, written at stage E4), is a different file and cites this one.

**How to read it.** Section 0 lists the decisions and the counts. Section 1 states the contract every entry assumes. Section 2 maps catalogue ids to final ids. Section 3 lists the services widgets depend on. Sections 4 to 6 are the entries: primitives and inputs, composites by cluster, presets. Section 7 is the build order. Section 8 is the curriculum coverage, including the table of which items each widget serves and the P0 confirmation. Section 9 lists rejected alternatives and open questions.

**Evidence tags** follow the sibling papers: [measured], [sourced], [recalled], [unverified], [inferred], [our choice]. Counts in this file were produced by a script over the catalogues and curriculum files on 6 October 2026 [measured]; section 8.1 describes it.

---

## 0. Decisions in brief

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Shared names | The calculus and linear algebra family: `plot-2d`, `plot-3d`, `marks`, `drag-point`, `region-select`, `value-table`, `live-formula`, `choice`, `numeric-input`, `expression-input`, `derivation-steps`. 18 catalogue ids become aliases (section 2) | The Stage 0 names (`plot-axes`, `draggable-point`, `data-table`, `tex-terms`, `choice-cards`, `numeric-entry`), which the prob-stats catalogue and the statistics curriculum file still use | Four of the six catalogues use them and Stage 0 recommended them (its 15.1); `CONTENT-FORMAT.md` section 1 and ten of the eleven curriculum files use them; nothing is built, so a rename is free; the compiler resolves aliases (section 2) |
| 2 | Tiers and kinds | The four tiers of arch decision 7 (primitive, input, composite, preset); each entry also states its kind, primitive or composite. An input is a primitive or a composite that produces an answer; a preset is a composite with no view | Two kinds only | The tier decides the folder, the cluster chunk and the tests (arch 4.2, 5.3); the kind is what the brief asked for |
| 3 | Composite rule, library-wide | A composite draws nothing a mark cannot draw and handles no gesture a primitive does not: a new shape becomes a `marks` type, a new gesture a primitive or an interaction hook | Composite-specific drawing and pointer code | calc-linalg decision 1, now for every cluster; it is what the lint rules `zq/no-raw-pointer` and `zq/no-state-in-render` enforce (arch 10.4), and it keeps composite views thin layouts of primitives |
| 4 | Presets | 23 catalogue entries become presets: configuration over a base widget plus predicates and recipes, expanded at compile time | A generic declarative scene engine that turns every graph composite into a preset of `plot-2d` | A preset has no `init`, no state derivation and no view (arch 5.3 `PresetDef`). Composites that derive state (Riemann bars from $n$, a posterior from evidence) would need an expression dataflow language inside content, which the compiler and verifier would have to check like code. Presets are used where a base widget already derives everything |
| 5 | `algo-lab` | One new base composite for "be the algorithm"; 15 programming composites become its presets (section 6) | Fifteen composites with their own views | They share `algo-trace`, the panes (`array-strip`, `node-link`, `cell-grid`, `code-surface`), the move check against a recorded trace and the tie rule (programming decisions 5, 11, 13). One view gives one keyboard model and one set of tutor ids |
| 6 | Merges of duplicates | `sharpe-lab`, `signal-lab`, `calibration-lab` (finance and ML specs of one idea each); `market-maker-sim` absorbs `dealer-sim`; `node-link` absorbs `node-graph`; `sign-chart`, `code-cell`, `binomial-tree`, `setup-checklist`, `shell-sim`, `workspace-sim` merge their two specs | Keeping both specs under one id or two ids | Two specs of one model means two sets of defects; the curriculum files already name one id for each (finance-projects request 4) |
| 7 | `binomial-tree` ownership | Finance owns it (1.7 is its first and heaviest user); `BinomialTreeConfig.q` is renamed `divYield` | Calc-linalg ownership; Hull's $q$ | finance 5.1; finance-projects decision 7: $q$ is the risk-neutral probability |
| 8 | `keypad` | Leaves the widget library; it is `ui/Keypad` with `SymbolBar`, opened by every numeric, interval, matrix-cell and expression field on a coarse pointer and built into `speed-drill` | A `keypad` widget | arch decision 35 and section 5.5 put it in the design system |
| 9 | Element ids | `kind:name` everywhere; on a multi-widget screen the host prefixes the widget's local id (`grid/cell:5,3`). Stage 0's `kind-name` ids convert by turning the first hyphen into a colon; the ids that sample lessons already use (0.1 requests R4 and R5, the 1.3 sample) are binding | `kind-name` | arch 0.3 and 5.1; `CONTENT-FORMAT.md` decision 17 |
| 10 | Priority rule | P0: needed by a lesson in 0.1 to 1.5 or by the weekly problems that start at 1.5. P1: first needed in 1.6 to 1.9. P2: first needed in Stage 2 or 3. A widget takes the priority of its earliest mode; later modes carry their own priority in the entry | Catalogue priorities as written | The owner's depth-first order; the curriculum files moved several widgets and modes (0.3 below) |
| 11 | 1.7 stays P1 | 1.7 Finance basics is P1 although it runs "alongside 1.3 to 1.6"; its first three courses (RB, EQ, MK, Stage 0 maths only) are the first P1 wave | All of 1.7 in P0 | finance decision 14 and finance-projects decision 4: skill gates unlock it; the P0 build stays bounded |
| 12 | Cluster rule | A widget sits in the cluster of its home catalogue section (arch's 22 lazy chunks); primitives, inputs and `code-cell` sit in `core`; `path-simulator`, `filtration-tree`, `kelly-lab` and `puzzle-workbench` sit in `probability`, where their P0 use is | Cluster by first use; everything shared in `core` | Home-topic chunks keep related widgets together; `core` is loaded with every lesson, so only code used everywhere goes there (arch decision 8, budget 9.2); the compiler preloads every cluster a course uses |
| 13 | Python | Pyodide 314.0.7 on both targets (arch decision 15). Every catalogue mention of MicroPython, `ulab`, `micropython-ok` or `ulab-ok` is void; a drill declares `needs` and hands off only for C++ or for a package its course has not budgeted in the Artifact | The catalogues' MicroPython split | The owner's iPhone measurement: Pyodide with NumPy and pandas runs inside the Artifact |
| 14 | Build size | S, M or L per entry (1.6) | Line or day estimates | Relative size is what orders a wave; absolute estimates for agent work are [unverified] |
| 15 | Drops and proposals | `vim-sim` is dropped (no lesson uses it). The canon-gap proposals are not added as widgets: the curriculum covers those lessons with modes of existing widgets (8.5); `brownian-path` and `ctmc-clock` become modes of `path-simulator` and `markov-chain` | Keeping unused widgets in the library | A widget nobody uses costs a build and a review; the curriculum is the test |
| 16 | Library size | 37 primitives and inputs, 254 composites, 23 presets: 314 ids. This supersedes the estimate in arch decision 7 (about 25, 75 and the rest); the tiers stand | Forcing composites into presets to meet the estimate | The catalogues' composites derive state, which presets cannot (decision 4). The cost stays bounded because composite views are thin (decision 3), and every P1 and P2 composite brief must first show that a preset cannot do the job (arch 10.5) before it is built |

### 0.2 Counts

The six catalogues name 332 distinct ids [measured]. After the name map, the merges and one drop, the library has **314 ids**, one of them new (`algo-lab`).

| Tier | Kind | P0 | P1 | P2 | All |
|---|---|---|---|---|---|
| primitive | primitive | 24 | 4 | 1 | 29 |
| input | primitive or composite | 6 | 2 | 0 | 8 |
| composite | composite | 147 | 46 | 61 | 254 |
| preset | composite (no view) | 9 | 14 | 0 | 23 |
| **all** | | **186** | **66** | **62** | **314** |

By kind: primitive 34 (P0 27, P1 6, P2 1), composite 280 (P0 159, P1 60, P2 61).

By build size: S 55 (P0 38), M 219 (P0 123), L 40 (P0 25).

### 0.3 What this file changes in the other papers

| Paper | Was | Now | Why |
|---|---|---|---|
| All six catalogues | Their own names for shared primitives; `kind-name` ids in Stage 0 | Section 2 names; `kind:name` ids | Decisions 1 and 9 |
| `widgets-calc-linalg.md` 6.19 | `condition-number` P1 | P0 | 1.4 lesson 88 needs it (linear-algebra request) |
| `widgets-calc-linalg.md` 7.9, `widgets-prob-stats-ts.md` 5 | `filtration-tree` P2 | P0 for its conditional-expectation and tower modes | 1.5 lesson 108 |
| `widgets-programming.md` 7.16 | `recursion-tree` P1 composite | P0 preset of `algo-lab` | 1.1 lessons 21 and 33 (python-tools decision 19) |
| `widgets-programming.md` 6.6, 6.10 | `mutant-hunter` property mode and `shell-sim` job, remote and `awk` modes P1 | P0 | 1.2 lessons 3, 8 and 24 |
| `widgets-prob-stats-ts.md` 6.4.2, 6.4.4 | `game-lab` Kelly mode and `markov-chain` Metropolis mode P2 | P0 | 1.5 lessons 154 and 134 |
| `widgets-finance-games.md` 8.3 | `kelly-lab` P2 | P0 core (one repeated bet and its growth curve), embedded by `game-lab` | Follows the `game-lab` change and finance decision 17 |
| `widgets-calc-linalg.md` 7.1 | `path-simulator` price mode P2 | P0 | 1.1 lessons 72 and 73 |
| `widgets-prob-stats-ts.md` 8.2, 8.4; `widgets-ml-research.md` 7.3; `widgets-calc-linalg.md` 7.6, 7.10 | `acf-lab`, `forecast-lab`, `factor-model-lab`, `gbm-lab`, `hedging-sim` P2 | P1 for the modes 1.6 and 1.7 use | First uses at 1.6 lessons 56 and 64 and 1.7 lessons 23, 28 and 78 |
| `widgets-finance-games.md` 6.8.3, `widgets-ml-research.md` 7.5 | `dealer-sim` and `market-maker-sim` | One widget, `market-maker-sim`, P1 core | Decision 6 |
| `widgets-finance-games.md` 7.2, 7.3, 8.5; `widgets-ml-research.md` 6.2.4, 6.8.1, 7.2 | Two `sharpe-lab`, two `signal-lab`, two `calibration-lab` | One each | Decision 6 |
| `widgets-programming.md` 4.14 and 7.2 to 7.17 (not 7.9, 7.10) | 15 algorithm composites | `algo-lab` and 14 presets (`hash-table` is the 15th, in `python`) | Decision 5 |
| `widgets-stage0.md` 9.10 to 9.12, 5.11, 6.8, 11.3; `widgets-prob-stats-ts.md` 7.1; `widgets-calc-linalg.md` 7.6 | `vector-plane`, `matrix-grid`, `linear-map`, `bounds-explorer`, `inequality-regions`, `times-table-grid`, `estimator-compare`, `gbm-lab` composites | Presets | Decision 4; each base already carries the interaction |
| `widgets-stage0.md` 3.13 | `keypad` primitive | `ui/Keypad` | Decision 8 |
| `widgets-programming.md` 6.8 | `vim-sim` P1 | Dropped | Decision 15 |
| `ARCHITECTURE.md` decision 7 | About 25 primitives and inputs, 75 composites | 37, 254 and 23 presets | Decision 16 |
| `ARCHITECTURE.md` 4.3 | Seven packages | Plus `@zq/models` for the pure models widgets, workers, generators and CI share (section 3), and `dmath` inside `@zq/mathcore` from E1 | Section 3; ML decision 2: seeded numbers must not depend on the engine's `Math.exp` |

---

## 1. The contract every entry assumes

### 1.1 Module shape

Every primitive, input and composite is the folder of arch 5.3: `logic.ts` (pure, Node-safe), `schema.ts` (classic zod, build time only), `View.tsx`, `view.module.css`, `fixtures.ts`, `logic.test.ts`, `view.browser.test.ts` and `states/v<n>.json`. The engine's `WidgetHost` implements lock, marks, highlight, annotate, ghost preview, reset, reveal, drafts, timers and announcements once; a widget implements none of them (arch decision 5). State has two parts: `a`, the answer state that is graded and saved, and `v`, the view state that show-why may tween (arch decision 6). The catalogues' lifecycle methods map to the contract as arch 5.6 lists; nothing in an entry below overrides it.

A preset is the file of arch 5.3 `PresetDef`: a base widget and version, a pure `expand(config)` run by the compiler, and optional predicates, recipes and `describeAs`. It has no view and no state of its own.

**Embedding.** A composite may compose another composite's controlled component when the entry lists it under Composes (for example `game-lab` embeds `kelly-lab`'s growth curve, `forecast-lab` embeds `time-cv-lab`'s fold strip). The screen still holds one host and one state (arch 5.3).

### 1.2 Fields in each entry

- **Header line:** kind, tier, cluster (the lazy chunk, arch decision 8), priority, size, spec (the catalogue sections that hold the behaviour; the first is the owner), and first use (curriculum item and lesson number, from section 8).
- **Composes:** final ids of the primitives (and embedded composites) the view lays out, the `marks` types it draws and the services it calls.
- **Config:** the widget-specific config interface and its top-level fields; `BaseConfig` (`id`, `type`, `v`, `label`, `preset?`, `seed?`) is implied (arch 5.3). The full field types are in the spec.
- **Answers:** the `Answer` types of arch 5.2 it can produce. `state` means a `predicate` check over the widget's own state; the predicates are named in the spec.
- **AI hooks:** the `targets()` ids Bertie and hints may point at, an example `describe()` sentence, what `secret()` carries (sent only in the sealed answer block, in lesson and explore modes, ai-tutor 5.5), and the `tryable()` controls Bertie may propose as a ghost preview, never an answer object.
- **Accessibility** and **Reduced motion:** what the entry adds to the baselines in 1.4.
- **Modes added:** modes from other catalogues and from curriculum requests, each with its own priority and source. A mode marked "curriculum" was requested by a curriculum file and is accepted here.

### 1.3 Answer types

One union for every widget (arch 5.2): `choice`, `numeric`, `expression`, `set`, `interval`, `ordering`, `mapping`, `point`, `curve`, `matrix`, `distribution`, `state`, `output`, `resultset`, `code`, `long-form`, `parts`. The catalogues' check names map to it as `CONTENT-FORMAT.md` section 1 lists (`probability` is `numeric` with `probability: true`; programming's `text` is `output`; Stage 0's `text` and calc-linalg's `free-text` are `long-form`; `policy` is a `predicate`). Widgets never parse or grade; `@zq/graders` does (arch 5.2). Two grading rules hold library-wide: a simulated estimate is never graded (prob-stats decision 3, ML decision 3), and realised P&L is never a pass or a fail (finance decision 6).

### 1.4 Baselines

- **Accessibility** (arch 5.5, widgets-stage0 1.7, calc-linalg 2.8): WCAG 2.2 AA; every drag has a keyboard path and a tap-then-tap path; arrows step, Shift ten steps, Alt a tenth, Home and End go to the limits, E opens the exact-value editor; hit areas at least 44 by 44 px; `describe('brief')` is the accessible description; every chart has a Table view; one polite live region per screen, announcements on commit only, at most one per 600 ms; colour is never the only carrier of meaning.
- **Reduced motion** (arch 5.11): baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play); pulses become a static ring; count-ups show the final value; the button press still sinks. "Baseline" in an entry means this and nothing more.
- **Performance** (arch 9.2): per-frame script at most 4 ms for a primitive and 8 ms for a composite at P95 on the CI proxy; mount at most 50 ms and 100 ms; each composite at most 25 KB minified; each cluster chunk at most 80 KB gzipped.
- **Determinism:** draws come from Philox4x32-10 by (seed, stream, index); `Math.random` and the clock are lint errors in `logic.ts` (arch decisions 13, 14); seeded numbers that are shown or graded use `dmath` (section 3).
- **Artifact and web:** identical unless the entry says otherwise. Code drills follow decision 13; C++ never runs in the Artifact (dsa-cpp decision 12).

### 1.5 Priorities

P0 covers items 0.1 to 0.5, 1.1, 1.2, 1.3, 1.4 and 1.5, and the weekly probability problems that start at 1.5 lesson 1 (assessment decision 17). P1 covers 1.6, 1.7, 1.8 and 1.9. P2 covers 2.1 to 2.4 and 3.1 to 3.3. A widget's priority is the earliest of: the priority of its first curriculum use (section 8), the priority its catalogue gave its first mode, and an explicit decision in section 0.3. A primitive or input takes the earliest priority of anything that composes it. A widget's later modes keep their own priorities, listed in its entry.

### 1.6 Build size

- **S:** one interaction model, at most two modes, no service of its own; a few hundred lines of logic and view.
- **M:** several modes or linked panes, show-why recipes, generators; the common case.
- **L:** many modes, a worker or service behind it (Python, `exchange-sim`, `ml-core`, `git-model`), or a host other widgets depend on. L entries get their own pull request series and a frame-time review at 4x throttling before merge.

Sizes are relative [our choice]; agent build times per size are [unverified] until the first wave records them.

---

## 2. Names: one id per concept

The compiler resolves each alias to its final id and warns (`widget-alias`); `zq fmt --fix` rewrites content to the final id. Aliases live in a generated `src/widgets/aliases.ts` read by `CompilerRegistry` (arch decision 33). No release ships an alias in compiled content. Presets are not aliases: they stay valid ids with their own entries (section 6).

| Catalogue or curriculum id | Final id | Change | Notes |
|---|---|---|---|
| `plot-axes` | `plot-2d` | rename | Stage 0 adds skewed lattices, $\pi$ ticks, log axes |
| `view-3d` | `plot-3d` | rename | Stage 0 adds view buttons, hidden-edge dashes, face selection |
| `curve-layer` | `marks` | merge | one mark family |
| `geo-layer` | `marks` | merge | construction graph becomes mark constructors |
| `bar-layer` | `marks` | merge | bar, bin, dot-plot and box types |
| `draggable-point` | `drag-point` | rename | constraint list and tap-then-tap kept |
| `region-selector` | `region-select` | rename | paint and half-plane modes kept |
| `data-table` | `value-table` | rename | sorting and per-cell checks kept |
| `tex-terms` | `live-formula` | rename | fixed-width slots kept |
| `choice-cards` | `choice` | rename | Stage 0 spec is the owner |
| `numeric-entry` | `numeric-input` | rename | Stage 0 spec is the owner |
| `expression-entry` | `expression-input` | rename | Stage 0 spec is the owner |
| `derivation` | `derivation-steps` | rename | `step` and `predict` modes kept |
| `code-editor` | `code-cell` | merge | Stage 0 lessons configure one Python file |
| `curve-sketch` | `sketch-pad` | merge | feature grading and monotone spline kept |
| `node-graph` | `node-link` | merge | weights, tokens and edge masses kept |
| `dealer-sim` | `market-maker-sim` | merge | section 5, `market-maker-sim` |
| `keypad` | `ui/Keypad` | ui | design-system component, not a widget |
| `brownian-path` | `path-simulator` | mode | its `refine` mode (proposed by canon-gap P2; 3.2 files fall back to it) |
| `ctmc-clock` | `markov-chain` | mode | its `ctmc` mode (same) |

Entries that merge two or more catalogue specs under one id: `binomial-tree`, `calibration-lab`, `choice`, `code-cell`, `code-surface`, `derivation-steps`, `drag-point`, `expression-input`, `live-formula`, `market-maker-sim`, `marks`, `node-link`, `number-line`, `numeric-input`, `plot-2d`, `plot-3d`, `region-select`, `setup-checklist`, `sharpe-lab`, `shell-sim`, `sign-chart`, `signal-lab`, `sketch-pad`, `slider`, `stepper`, `text-terminal`, `token-tray`, `value-table`, `workspace-sim`. The first spec named in each entry is the owner; the others add modes.

---

## 3. Services widgets depend on

Services are not widgets: they have no view and no state of their own. Pure services live in packages so that widgets, workers, generators and CI parity tests import the same code (arch 4.5 forbids workers from importing `src/widgets`). This adds one package, `@zq/models`, with one entry point per domain so a cluster chunk imports only its own.

| Service | Home | Used by | Spec |
|---|---|---|---|
| `rng`, `hash32`, `rational`, `num-parse`, `expr`, `units`, `sample`, `quad`, `ode`, `roots`, `linalg`, `stats` | `@zq/mathcore` (arch 4.3) | every widget, grader and generator | arch 5.1; calc-linalg 2.3, 2.13 |
| `dmath` (deterministic `exp`, `log`, `log1p`, `expm1`, `tanh`, `pow`, `sin`, `cos`) | `@zq/mathcore`, from E1 | `Rng.normal`, `sim-runner`, every seeded number shown or graded | ML decision 2 |
| `stats-core` (`dist`, special functions, `tests`, `ols`, `ts`) | `@zq/mathcore/stats` | probability, statistics, time-series, ML and research widgets | prob-stats decisions 5, 6 |
| `cas`, `mathfield`, `tex` | `src/engine/cas`, `src/engine/render` (arch 5.3, 5.11) | `expression-input`, `equation-workbench`, `live-formula` | arch 5.3 |
| `algo-trace`, `trace-recorder` | `@zq/models/algo`; the recorder is `workers/python/trace.py` | `algo-lab` and its presets, `code-tracer`, `complexity-lab` | programming decisions 4, 5 |
| `code-lex`, `seed-bank`, `mutant-forge`, `vfs`, `shell` | `@zq/models/code` | code widgets, `shell-sim`, `workspace-sim`, `mutant-hunter` | programming 2.4 |
| `nd-core`, `frame-core`, `price-series` | `@zq/models/data` | NumPy and pandas widgets; finance and time-series data | programming decision 6 |
| `git-model` | `@zq/models/git` | `git-graph`, `merge-conflict` | programming decision 8 |
| `PythonRuntime`, `SqlRuntime`, `CppRuntime` (web only), `handoff` | `src/engine/python`, `src/engine/sql`, platform adapters (arch 5.9) | `code-cell` and every drill | arch 6.3 |
| `exchange-sim`, `ledger`, `finance-core`, `market-gen`, `backtest-core` | `@zq/models/markets` | finance, projects and interview widgets | finance decisions 2, 3, 8, 16 |
| `ml-core`, `dataset-gen`, `panel-sim`, `sharpe-stats`, `as-sim` | `@zq/models/ml`, run in the data worker through `sim-runner` jobs | ML and research widgets, `market-maker-sim` | ML decisions 1, 4, 7 |
| `speech` | `src/platform/shared/speech.ts` | `voice-capture` | finance decision 10 |
| `interview-engine`, `problem-bank` | `src/tutor` (ai-tutor 11.1) and content libraries | `mock-interview`, `puzzle-workbench`, `viva` | finance decision 11; ML decision 10 |

---

## 4. Primitives and inputs

29 primitives and 8 inputs, all in the `core` cluster. Every primitive is also a building block: beside its `WidgetModule` it exports controlled components that composites lay out (arch 5.3).

### 4.1 Primitives

#### 4.1.1 `plot-2d`

primitive · tier primitive · cluster `core` · **P0** · size L · spec calc-linalg 3.1, stage0 3.1 · first use 1.1 L70

A coordinate plane that hosts marks and handles.

- **Composes** `marks`, `drag-point`, `region-select`, `sketch-pad`.
- **Config** `Plot2DConfig { view, aspect?, coords?, axes?, grid?, zoom?, pan?, link?, layers, table? }`.
- **Answers** `point`.
- **AI hooks** targets `axis:x`, `axis:y`, `grid`, `origin`; describe, e.g. "Axes: x −5 to 5, y −5 to 5, equal aspect. Layers: line L1 y = 2x + 1; point A (1, 3)."
- **Accessibility** `role="group"` named by `label`. With no handles, the SVG is `role="img"` with `describe('brief')` as its description. The Table toggle lists the data of every mark marked `table: true`.
- **Reduced motion** Zoom buttons jump.
- Absorbs `plot-axes`: skewed lattice grids, $\pi$ ticks and log axes come from Stage 0 3.1.
- Gains stacked panels with a linked $x$ axis and a sideways marginal panel (prob-stats 4.2), a trading-time axis and linked crosshairs (finance 4.2), reversed log axes, anchored insets and a weight-space preset (ML 4).
- Hosts handle layers (`drag-point`, `region-select`, `sketch-pad`) so a primitives-only screen is one widget with one state.

#### 4.1.2 `marks`

primitive · tier primitive · cluster `core` · **P0** · size L · spec calc-linalg 3.5, stage0 3.3, stage0 3.4, stage0 3.5, prob-stats 4.1, finance 4.1 · first use 1.3 L65

Declarative layers inside a host, each with a stable id, whose coordinates may be Exprs over widget variables.

- **Composes** nothing (a leaf primitive).
- **Config** `MarkSpec { id, type, style?, table?, visibleWhen?, ...TypeFields }`.
- **Answers** none (display or host; the screen grades through its handles or a predicate).
- **AI hooks** targets `<the declared mark ids>`; describe, e.g. "Curve f: y = x² − 4 (slot 1)."
- **Accessibility** Each mark contributes a phrase to `describe()` and, when `table: true`, rows to the table view.
- **Reduced motion** no motion of its own.
- One mark family replaces Stage 0's `curve-layer`, `geo-layer` and `bar-layer`; a composite may not draw anything a mark cannot draw (calc-linalg decision 1, now library-wide).
- Types: `curve`, `param-curve`, `polar-curve`, `implicit`, `contours`, `heatmap`, `field`, `point`, `segment`, `line`, `ray`, `vector`, `polygon`, `region`, `bars`, `scatter`, `paths`, `band`, `angle`, `ellipse`, `tangent`, `brace`, `label`, `ghost`; Stage 0 constructors (construction graph, equal-length and angle marks, bin, dot-plot and box types); prob-stats `stems`, `step`, `hist`, `glyphs`, `intervals`, `rug`, `fan`, `rect-signed`, `connector`, fill patterns; finance `candles`, `ohlc-bars`, `depth`, `payoff`, `signed-fill`, `waterfall`, `quote-band`, `trade-glyphs`, `event-rug`; ML `field` with `boundary` contours, `partition`, `norm-ball`, scatter shape and hollow channels, bar whiskers; programming `icicle` and horizontal interval bars (`gantt`).
- Each type is its own module inside the primitive, so a cluster chunk imports only the types it uses.

#### 4.1.3 `drag-point`

primitive · tier primitive · cluster `core` · **P0** · size M · spec calc-linalg 3.6, stage0 3.6 · first use 0.2 L36

The universal handle: a point the learner moves under a constraint, with snapping.

- **Composes** nothing (a leaf primitive).
- **Config** `DragPointConfig { id, at, constraint?, snap?, bind?, shape?, tail?, readout?, label? }`.
- **Answers** `point`, `state`, `numeric`.
- **AI hooks** targets `handle:<id>`, `point:<id>`, `preview`.
- **Accessibility** Slider semantics with every coordinate in `aria-valuetext`; announced on release.
- **Reduced motion** Snap is instant.
- Keeps Stage 0's constraint list (on a curve, a segment, a grid, a circle, between bounds) and the tap-then-tap path.
- E or double tap opens the exact-value editor on every handle (calc-linalg decision 7).

#### 4.1.4 `slider`

primitive · tier primitive · cluster `core` · **P0** · size S · spec calc-linalg 3.7, stage0 3.7 · first use 0.1 L34

Set a scalar: continuous, stepped, logarithmic, integer, or from a discrete list.

- **Composes** nothing (a leaf primitive).
- **Config** `SliderConfig { id, bind, min, max, step?, scale?, values?, label, format?, decimals?, units?, ticks?, play?, orientation? }`.
- **Answers** `numeric`, `state`, `set`.
- **AI hooks** targets `slider:<id>`; describe, e.g. "m = 2 (range −5 to 5)"; tryable `slider:<id>`.
- **Accessibility** Native `<input type="range">` underneath with `aria-valuetext` including units.
- **Reduced motion** Play steps without interpolation, four steps per second.
- **Modes added** value lists and a hidden-value quiz mode (P0, prob-stats 4.2); log scales, unit suffixes (P1, finance 4.2); decade ticks and paired thumbs for windows (P2, ML 4).

#### 4.1.5 `number-line`

primitive · tier primitive · cluster `core` · **P0** · size M · spec stage0 3.2, calc-linalg 3.3 · first use 0.1 L1

A one-dimensional line for order, size, operations as motion (jumps, scaling, reflection), intervals, rounding and zooming.

- **Composes** `drag-point`, `marks`.
- **Config** `NumberLineConfig { min, max, scale?, ticks?, snap?, points?, intervals?, allowAdd?, operators?, lens?, rounding? }`.
- **Answers** `point`, `interval`, `ordering`, `numeric`.
- **AI hooks** targets `point:<id>`, `interval:<id>`, `end:<id>:a`, `end:<id>:b`, `tick:<value>`, `span:<from>-<to>`, `token:<value>`, `lens:main`; describe, e.g. "Number line 0 to 1, ticks every 0.1. Learner point A at 0.37. Interval [0.3, 0.4)."
- **Accessibility** points are `role="slider"` with `aria-valuetext` such as "A at 2.75". Intervals read as "from 3.35, included, to 3.45, not included". The table view lists points and intervals.
- **Reduced motion** jumps are drawn at once; `scale` and `reflect` become before-and-after with Play.
- **Modes added** float-spacing mode: gaps between neighbouring doubles (P0, 1.1 L4, curriculum); dual log-odds scale with probability ticks (P0, prob-stats 4.2); quote bracket with bid, ask and centre handles (P1, finance 4.2); log mode with interval brackets (P2).
- Stage 0 spec owns operators, lens and rounding; calc-linalg adds interval ends with closed and open toggles.
- Element ids from the 0.1 sample lesson (request R5): `span:<from>-<to>`, `token:<value>`, `lens:main`.

#### 4.1.6 `live-formula`

primitive · tier primitive · cluster `core` · **P0** · size M · spec calc-linalg 3.14, stage0 3.11 · first use 1.8 L25

A KaTeX formula whose numbers update from widget variables, with terms linked to marks: focus a term and its mark lights up, and the reverse.

- **Composes** nothing (a leaf primitive).
- **Config** `LiveFormulaConfig { tex, slots, expr, decimals?, format?, links?, toggles? }`.
- **Answers** `set`, `choice`.
- **AI hooks** targets `term:<id>`; describe, e.g. "2x + 3 = 11 [t1: 2x] [t2: 3] [t3: 11]".
- **Accessibility** KaTeX outputs MathML alongside HTML; the engine announces key values on commit.
- **Reduced motion** no motion of its own.
- Absorbs `tex-terms`: addressable terms and fixed-width numeric slots; KaTeX never re-renders inside a drag (arch 5.11 `TexSlots`).

#### 4.1.7 `value-table`

primitive · tier primitive · cluster `core` · **P0** · size M · spec calc-linalg 3.13, stage0 3.12, programming 3.8 · first use 0.1 L16

A live table: $x$ and $f(x)$ approaching a limit, partial sums, iterates, data points, residuals.

- **Composes** nothing (a leaf primitive).
- **Config** `ValueTableConfig { columns, key, label, expr?, decimals?, editable?, rows, from, maxRows?, linkMarks? }`.
- **Answers** `numeric`, `choice`, `state`, `ordering`, `expression`, `set`, `resultset`.
- **AI hooks** targets `row:<i>`, `cell:<i>,<key>`, `cell:<row>-<col>`, `col:<id>`; describe, e.g. "Selected rows 2024-01-03 to 2024-01-05, column 'close' (3 cells)."
- **Accessibility** A native `<table>` with a caption and scoped headers. It is the accessible fallback for charts, so it must be complete.
- **Reduced motion** no motion of its own.
- **Modes added** frame mode: faithful DataFrame and SQL result view (P0, programming 3.8); rows that fill as a linked slider visits a stop (P0, 1.3 L1, curriculum); deviations column from the learner's mean (P1, 1.6 sample, curriculum); margins and a conditional view (P0, prob-stats 4.2); presets `blotter`, `chain`, `book` (P1, finance 4.2); panel view with as-of greying (P2, ML 4).
- Absorbs `data-table`: sorting and per-cell checks (Stage 0 3.12); it is also the Table view of every chart.

#### 4.1.8 `region-select`

primitive · tier primitive · cluster `core` · **P0** · size M · spec calc-linalg 3.9, stage0 3.8 · first use 0.1 L13

Choose regions: cells of a grid, parts of a diagram, intervals of a sign table, atoms of a partition; or bracket an interval $[a,b]$ on an axis with two handles.

- **Composes** nothing (a leaf primitive).
- **Config** `RegionSelectConfig { regions, id, shape, cell, interval, mark, label?, states?, maxSelected?, bracket?, axis, range, showCount? }`.
- **Answers** `set`, `interval`, `numeric`.
- **AI hooks** targets `region:<id>`, `cell:<r>,<c>`, `row:<r>`, `col:<c>`; describe, e.g. "6 × 6 grid; shaded: (2,6) (3,5) (4,4); 3 shaded."
- **Accessibility** Each region is a toggle button with `aria-pressed` (or a named state for cycles); the running count is announced.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** half-plane arrangement cells with exact areas (P0, prob-stats 4.2); two time brushes A and B (P2, prob-stats 4.2); chain-cell selection (P1, finance 4.2); coarse paint grid for predicted decision regions (P2, ML 4).
- Absorbs `region-selector`: paint mode and half-plane mode (Stage 0 3.8); the prototype's dice grid is an instance.

#### 4.1.9 `token-tray`

primitive · tier primitive · cluster `core` · **P0** · size M · spec stage0 3.9, calc-linalg 3.10 · first use 0.2 L1

Place-and-sort machinery.

- **Composes** nothing (a leaf primitive).
- **Config** `TokenTrayConfig { tokens, zones, rules?, twoTap? }`.
- **Answers** `ordering`, `mapping`, `set`, `state`, `expression`.
- **AI hooks** targets `token:<id>`, `zone:<id>`, `slot:<id>`; describe, e.g. "Tray: x, x, 1, 1, 1. Left pan: x, x, x, 1, 1. Right pan: x, 1 × 8."
- **Accessibility** tokens are buttons with `aria-roledescription="draggable"`. The live region narrates: "Lifted 3x. Over left pan, position 2. Dropped." Zones are lists.
- **Reduced motion** lift and drop are instant. Combine and cancel cross-fade.
- **Modes added** term chips with coefficient and variable; evidence cards with a likelihood ratio (P0, prob-stats 4.2); typed expression slots with arity and type (P2, ML 4).

#### 4.1.10 `stepper`

primitive · tier primitive · cluster `core` · **P0** · size M · spec calc-linalg 3.8, stage0 3.10, programming 3.7 · first use 0.3 L82

Walk through a fixed sequence of states: Demonstrate screens, algorithm traces (Newton iterations, elimination history, Gram-Schmidt, SVD stages, backward induction).

- **Composes** nothing (a leaf primitive).
- **Config** `StepperConfig { steps, state, caption?, highlight?, predict?, prompt, check, autoplayMs?, loop? }`.
- **Answers** none (display or host; the screen grades through its handles or a predicate).
- **AI hooks** targets `step:<i>`, `step:next`, `step:<n>`, `bp:<line>`; describe, e.g. "Step 3 of 7: 'Bring down the 4.'".
- **Accessibility** Buttons named "Step 2 of 5"; the caption is announced on each step.
- **Reduced motion** Cross-fade of 120ms.
- **Modes added** trace mode for long recorded executions (P0, programming 3.7); replay speed 0.5x to 8x (P1, finance 4.2); reads job snapshots: epochs, rounds, folds (P2, ML 4).

#### 4.1.11 `sketch-pad`

primitive · tier primitive · cluster `core` · **P0** · size M · spec calc-linalg 3.11, stage0 6.7 · first use 0.2 L68

The learner draws a curve on a `plot-2d`, freehand or by moving control points; graded against a target by values and by features.

- **Composes** `drag-point`.
- **Config** `SketchPadConfig { plot, domain, mode, knots?, anchor? }`.
- **Answers** `curve`, `point`.
- **AI hooks** targets `stroke`, `knot:<i>`, `feature:<i>`, `knot:<id>`, `feature:<k>`.
- **Accessibility** Points mode; `describe()` turns the sketch into words ("decreasing from x = −2 to 0, increasing after; crosses zero near x = 1.1").
- **Reduced motion** The target appears at once.
- **Modes added** step-function features `jump` and `flat` for CDFs (P0, prob-stats 4.2); piecewise-linear snapping to a strike grid (P1, finance 5); two labelled curves with `interior-min`, `monotone`, `plateau`, `peak-near` (P2, ML 4).
- Absorbs Stage 0's `curve-sketch`: graded on features (intercepts, turning points, asymptotes, monotone pieces), never on pixels; the feature-form alternative and the monotone spline stay.

#### 4.1.12 `cell-grid`

primitive · tier primitive · cluster `core` · **P0** · size M · spec programming 3.3 · first use 1.1 L14

A two-dimensional (and layered three-dimensional) lattice of cells where position carries meaning: NumPy arrays, DP tables, grid graphs, the sieve, the pair grid behind two pointers, prefix-sum rectangles, cache lines.

- **Composes** `region-select`.
- **Config** `CellGridConfig { shape, values?, headers?, indexLabels?, states?, select?, editable?, markers?, rects?, arrows?, path?, heat?, cellSize? }`.
- **Answers** `set`, `state`, `point`, `numeric`, `choice`, `output`, `expression`.
- **AI hooks** targets `cell:<r>,<c>`, `row:<r>`, `col:<c>`, `layer:<l>`, `rect:<id>`, `marker:<id>`; describe, e.g. "Grid 5 × 6 (DP table for edit distance 'kitten' to 'sitting'), 18 of 30 cells filled; focus at (3, 4) = 2."
- **Accessibility** a real `grid` with row and column headers; each cell reads "row 2, column 5, value 7, done"; dependency arrows are listed in the focused cell's description ("reads row 1 column 5 and row 2 column 4").
- **Reduced motion** layer changes and fills cut.
- **Modes added** triangle paint above the diagonal with a mirrored ghost (P1, 1.8 sample, curriculum); signed heatmaps, headers, permutation reorder, split-matrix paint (P2, ML 4).

#### 4.1.13 `matrix`

primitive · tier primitive · cluster `core` · **P0** · size M · spec calc-linalg 3.4 · first use 1.7 L10

Show and edit matrices and vectors with exact entries; select rows, columns and cells; carry the row-operation gestures; mark pivots; draw augmented bars and partitions; colour entries in heatmap mode.

- **Composes** `cell-grid`.
- **Config** `MatrixConfig { rows, cols, entries, editable?, augmentAfterCol?, partition?, number?, decimals?, select?, rowGestures?, heat?, labels?, bracket? }`.
- **Answers** `matrix`, `numeric`, `choice`, `set`.
- **AI hooks** targets `cell:<i>,<j>`, `row:<i>`, `col:<j>`, `pivot:<k>`.
- **Accessibility** `role="grid"` with row and column counts; each cell named "row 2, column 3, five halves". Row operations are announced with the resulting row ("Row 2 minus 3 times row 1. Row 2 is now 0, 2, minus 1").
- **Reduced motion** No slide; the wash still marks changed entries.
- **Modes added** row-stochastic editing through a `mass-editor` popover (P0, prob-stats 4.2).
- Renders through `cell-grid`'s grid and roving keyboard (programming 3.3 recommendation) and adds brackets, augmented bars and row gestures.

#### 4.1.14 `plot-3d`

primitive · tier primitive · cluster `core` · **P0** · size L · spec calc-linalg 3.2, stage0 3.15 · first use 1.3 L107

Show surfaces, planes, vectors, points, curves, columns and solids in 3D with an orbit camera, linked to 2D views.

- **Composes** `marks`, `drag-point`.
- **Config** `Plot3DConfig { box, camera?, axes?, floor?, orbit?, presets?, layers, mesh?, link? }`.
- **Answers** `set`.
- **AI hooks** targets `surface:<id>`, `plane:<id>`, `vec:<id>`, `point:<id>`, `slice:<axis>`, `column:<i>,<j>`, `vertex:<id>`, `edge:<id>`, `face:<id>`, `view:front`; describe, e.g. "Cuboid 3 × 4 × 12, viewed from front right; selected: AG."; tryable `view:front`.
- **Accessibility** A 3D view cannot carry meaning alone: every scene has a 2D companion (contour map, slice panel or coordinates table) and a description that states the geometry.
- **Reduced motion** Presets jump.
- Absorbs `view-3d`: plan and elevation buttons, hidden-edge dashes and face selection (Stage 0 3.15).
- Hand-written projection with painter's sorting; no WebGL (calc-linalg decision 4).

#### 4.1.15 `sim-runner`

primitive · tier primitive · cluster `core` · **P0** · size L · spec calc-linalg 3.12 · first use 1.1 L69

Reproducible random simulation: run batches, play, pause and step; stream results into marks; offload heavy work to a worker.

- **Composes** nothing (a leaf primitive).
- **Config** `SimRunnerConfig { seed, model, params, batches, maxSamples, worker?, feeds }`.
- **Answers** none (display or host; the screen grades through its handles or a predicate).
- **AI hooks** targets `run:<n>`, `reset`.
- **Accessibility** After each batch: "1,000 runs. Mean 0.02. 68% within one standard deviation."
- **Reduced motion** Each batch shows its final state at once.
- Absorbs Stage 0's `seeded-rng` use inside `trial-simulator`; draws are Philox4x32-10 by (seed, stream, index) (arch decision 14).
- Models: prob-stats `bernoulli-seq`, `urn`, `permutation`, `birthday`, `coupon`, `pattern`, `poisson-process`, `galton`, `sample-statistic`, `bootstrap`, `permutation-test`, `ci`, `policy`, `markov-walk`, `lattice-walk`, `arma`, `garch`, `pair`; finance `order-flow`, `bet-sequence`, `null-strategy`, `latency`; ML jobs `train`, `resample-fit`, `strategy-zoo`, `cscv`, `as-market`, `tick-stream`, `panel`, `nn-distance`; up to $10^7$ draws per run in a worker, paused while the tab is hidden.
- Never the source of a graded number: simulations are graded on predictions or exact values (prob-stats decision 3).

#### 4.1.16 `chance-object`

primitive · tier primitive · cluster `core` · **P0** · size M · spec prob-stats 3.3 · first use 1.5 L6

Show the physical story behind a random experiment, and let the learner act on it: flip, roll, draw a ball, open a door, pick an envelope.

- **Composes** nothing (a leaf primitive).
- **Config** `ChanceObjectConfig { id, kind, sides?, sectors?, balls?, value?, interactive?, size?, label? }`.
- **Answers** `choice`.
- **AI hooks** targets `coin:<i>`, `die:<i>`, `card:<i>`, `door:<i>`, `ball:<i>`, `urn`; describe, e.g. "Urn: 3 red, 2 blue. Drawn without replacement: R, B."
- **Accessibility** Non-interactive objects are `role="img"` ("Die showing 5"). Interactive ones are buttons ("Door 2, closed"). The host announces results.
- **Reduced motion** The value appears with a 120ms cross-fade.

#### 4.1.17 `mass-editor`

primitive · tier primitive · cluster `core` · **P0** · size M · spec prob-stats 3.1 · first use 1.5 L12

Build and reshape PMFs, priors, Markov transition rows, spinner sectors and mixture weights by hand, with the sum constraint made visible rather than enforced by an error message.

- **Composes** `plot-2d`, `marks`, `drag-point`.
- **Config** `MassEditorConfig { id, support, masses, total?, layout, policy?, step?, locked?, show?, role }`.
- **Answers** `distribution`, `numeric`, `state`.
- **AI hooks** targets `mass:<id>`, `divider:<i>`, `total`, `normalise`; describe, e.g. "Masses on 0..4: 1/16, 4/16, 6/16, 4/16, 0; total 15/16 (needs 1)."
- **Accessibility** A group named by the host ("Distribution of X, total 1"). Each bar is a slider with `aria-valuetext` such as "P of X equals 3: five thirty-sixths". The total is announced on commit.
- **Reduced motion** Normalise and snaps are instant.
- **Modes added** entropy readout (P2, 2.1 L13, curriculum).

#### 4.1.18 `array-strip`

primitive · tier primitive · cluster `core` · **P0** · size M · spec programming 3.2 · first use 1.1 L7

A one-dimensional indexed sequence with pointer markers, ranges and per-cell states: lists, strings, bit patterns, bytes in memory, sorting bars, windows, prefix arrays, heap arrays and ring buffers.

- **Composes** `drag-point`, `token-tray`.
- **Config** `ArrayStripConfig { values, mode, orientation?, indices?, markers?, ranges?, states?, editable?, swappable?, bits?, link?, maxVisible? }`.
- **Answers** `point`, `set`, `ordering`, `output`, `state`, `expression`.
- **AI hooks** targets `cell:<i>`, `ptr:<id>`, `range:<id>`; describe, e.g. "Array [3, 8, 9, 12, 17] with lo at 1, hi at 5 (exclusive), mid at 3. Cells 0 ruled out."
- **Accessibility** the strip is a `grid` with one row; cells read "index 3, value 17, active"; markers are sliders with `aria-valuetext` ("lo at index 2, before value 9"); the table view lists index, value and state.
- **Reduced motion** swaps and shifts cut to the final state; the moved cells keep the "active" state for one step so the change stays visible.
- **Modes added** bytes mode (P0, 1.1 L10, curriculum).

#### 4.1.19 `node-link`

primitive · tier primitive · cluster `core` · **P0** · size L · spec programming 3.4, prob-stats 3.2 · first use 1.1 L1

The one renderer for trees, graphs, DAGs and memory diagrams.

- **Composes** `drag-point`, `token-tray`, `mass-editor`.
- **Config** `NodeLinkConfig { nodes, edges, layout, layoutOptions?, interact?, states? }`.
- **Answers** `set`, `ordering`, `mapping`, `state`.
- **AI hooks** targets `node:<id>`, `edge:<id>`, `slot:<node>.<slot>`, `edge:<from>-<to>`, `walker:<i>`; describe, e.g. "Graph 9 nodes, 12 edges. Visited: A, B, D. Queue: E, F. Active: D."
- **Accessibility** the diagram is a `group` with a structured text alternative (trees as nested lists, graphs as adjacency lists, heaps as name-to-object lists); each node is focusable with a name like "node 7, visited, neighbours 3, 5, 9".
- **Reduced motion** reflows cut; the moved nodes keep the "active" state for one step.
- **Modes added** class-diagram layout (P0, 1.1 L52, curriculum); fixed-layout state machines with highlighted transitions (P2, finance 5); `layered-dense` network and `dendrogram` layouts (P2, ML 4).
- Absorbs prob-stats' `node-graph`: weights, labels, values, moving tokens and edge masses edited through `mass-editor`; one renderer for trees, graphs, state diagrams, DAGs, networks and memory diagrams.
- Deterministic layouts: tidy tree, layered, fixed, circular, grid, outline, heap, row; an object keeps its position between steps.

#### 4.1.20 `code-surface`

primitive · tier primitive · cluster `core` · **P0** · size M · spec programming 3.5, stage0 3.16 · first use 2.3 L71

Stage 0's editing surface (textarea over a synchronised highlighted `<pre>`) stays.

- **Composes** nothing (a leaf primitive).
- **Config** `CodeSurfaceConfigAdditions { language, mode, gutters?, selectable?, slots?, callouts?, diagnostics? }`.
- **Answers** `code`.
- **AI hooks** targets `tok:<line>:<col>`, `line:<n>`; describe, e.g. "Python, 18 lines, read-only; line 7 marked as the next line."
- **Accessibility** a real textarea with a label and a line count. Error lines are announced with their messages.
- **Reduced motion** no motion of its own.
- Textarea over a synchronised highlighted `<pre>` through P1; CodeMirror 6 only on the measured triggers of programming decision 12.

#### 4.1.21 `diff-view`

primitive · tier primitive · cluster `core` · **P0** · size M · spec programming 3.1 · first use 1.1 L48

Shows how one text differs from another: expected against actual output, a commit's changes, a pull request, a mutant against the reference, a failing version beside its fix (design research 9.4), and three-way merges.

- **Composes** `code-surface`.
- **Config** `DiffViewConfig { a, b, base?, language, labels?, view?, context?, intraline?, hunkSelect?, comments?, whitespace? }`.
- **Answers** `set`, `state`, `code`.
- **AI hooks** targets `hunk:<n>`, `line:a<n>`, `line:b<n>`; describe, e.g. "Diff expected against actual: 1 hunk, line 3 differs: expected '0.1542', actual '0.1541'."
- **Accessibility** each line is prefixed in its accessible name ("added line 14: return total"); hunks are a list with a count ("Hunk 2 of 4, 3 lines removed, 5 added"); the split view keeps a reading order of old then new per hunk.
- **Reduced motion** instant expansion.

#### 4.1.22 `text-terminal`

primitive · tier primitive · cluster `core` · **P0** · size S · spec programming 3.6, stage0 3.17 · first use 0.4 L16

Stage 0's terminal surface stays.

- **Composes** nothing (a leaf primitive).
- **Config** `TextTerminalConfig { interpreter, banner?, completion? }`.
- **Answers** `state`, `long-form`.
- **AI hooks** targets `line:<n>`, `input`.
- **Accessibility** output in `role="log"` with polite announcements; a labelled input; navigable scrollback.
- **Reduced motion** the cursor does not blink.

#### 4.1.23 `speed-timer`

primitive · tier primitive · cluster `core` · **P0** · size S · spec stage0 3.14 · first use 0.4 L1

An honest countdown or elapsed timer for drills and exams.

- **Composes** nothing (a leaf primitive).
- **Config** `SpeedTimerConfig { durationMs?, warnAtMs?, display, onHide }`.
- **Answers** none (display or host; the screen grades through its handles or a predicate).
- **AI hooks** targets: the ids of its marks and handles.
- **Accessibility** `role="timer"`, not live. Announcements at the start, at 30 seconds and at 10 seconds.
- **Reduced motion** the bar steps once per second.
- **Modes added** count-up mode with a soft target that never ends the attempt (P0, finance 4.2).
- Reads time from the platform `Clock` through the widget `Scope`; raw timers are a lint error (arch decision 13).

#### 4.1.24 `scratch-pad`

primitive · tier primitive · cluster `core` · **P0** · size S · spec finance 3.7 · first use 0.1 L41 (through `free-response`)

Where the learner works a puzzle or a long-form problem.

- **Composes** `live-formula`.
- **Config** `ScratchPadConfig { pages, template? }`.
- **Answers** none (display or host; the screen grades through its handles or a predicate).
- **AI hooks** targets `block:<id>`, `ink:page:<n>`.
- **Accessibility** Text blocks are real textareas; the ink layer is described as "Ink page 1, 34 strokes" and is readable by Bertie only through the image.
- **Reduced motion** no motion of its own.
- P0 because the weekly probability problems start at 1.5 lesson 1 and long-form homework from 0.1 allows its ink layer (assessment 2, 10).

#### 4.1.25 `cashflow-timeline`

primitive · tier primitive · cluster `core` · **P1** · size M · spec finance 3.2 · first use 1.7 L1

Every time-value idea: discounting, NPV, annuities and loans, bond cash flows, duration as a balance point, the replicating trades behind forwards, swap legs, the bond in put-call parity.

- **Composes** `marks`, `drag-point`.
- **Config** `CashflowTimelineConfig { horizon, period, lanes, flows, amountStep, amountRange, scale, discount?, show }`.
- **Answers** `point`, `set`.
- **AI hooks** targets `flow:<id>`, `lane:<id>`, `pv:<id>`, `net:<t>`, `fulcrum`, `bracket:<id>`; describe, e.g. "3 lanes. Net today 0.00. Borrow lane: receive 100 at t=0, pay 105.13 at t=1."
- **Accessibility** Each flow is a control reading "Year 3, receive 50 pounds, present value 43.19." The table view lists $t$, amount, discount factor and present value. Lanes are groups with names.
- **Reduced motion** Ghosts appear at $t = 0$.

#### 4.1.26 `price-ladder`

primitive · tier primitive · cluster `core` · **P1** · size M · spec finance 3.1 · first use 1.7 L29

The canvas for every order-book idea, and for any widget that shows or takes orders at prices.

- **Composes** nothing (a leaf primitive).
- **Config** `PriceLadderConfig { tick, lot, columns, rows, entry, amendByDrag, showQueuePosition, showLast }`.
- **Answers** `set`.
- **AI hooks** targets `level:<ticks>`, `bid:<ticks>`, `ask:<ticks>`, `order:<id>`, `spread`, `mid`, `last`; describe, e.g. "Best bid 99.98 (300), best ask 100.01 (200), spread 3 ticks. Your orders: buy 100 at 99.97, 2nd in queue."
- **Accessibility** `role="grid"`; each row reads "Price 100.02. Ask 200 shares. Your order: none." The table view lists every level. Fills are announced on commit ("Bought 200 at 100.01, 200 at 100.02, 100 at 100.04").
- **Reduced motion** Widths and rows change at once.

#### 4.1.27 `position-editor`

primitive · tier primitive · cluster `core` · **P1** · size M · spec finance 3.3 · first use 1.7 L46

Build positions: option strategies, replicating portfolios, arbitrage trades, hedges.

- **Composes** nothing (a leaf primitive).
- **Config** `PositionEditorConfig { instruments, maxLegs, qty, strikeGrid, pricing, locked?, showCost }`.
- **Answers** none (display or host; the screen grades through its handles or a predicate).
- **AI hooks** targets `leg:<id>`, `leg:<id>:qty`, `leg:<id>:K`, `palette:<instrument>`, `net:cost`.
- **Accessibility** A list; each row reads "Long 2 calls, strike 100, expiry 0.5 years, premium 4.20 each." The net cost is announced on commit.
- **Reduced motion** Instant.

#### 4.1.28 `voice-capture`

primitive · tier primitive · cluster `core` · **P1** · size M · spec finance 3.6 · first use 1.7 L45

Explanations aloud (the 1.7 exit rehearsal), thinking aloud in puzzles, spoken market-making, mock interviews.

- **Composes** nothing (a leaf primitive).
- **Config** `VoiceCaptureConfig { lang, mode, grammar?, maxMinutes?, showInterim }`.
- **Answers** `long-form`.
- **AI hooks** targets `segment:<n>`, `mic`; describe, e.g. "Transcript 412 words over 6 min 10 s; last segment: 'so the expected sum is seven'."
- **Accessibility** The typed path is equivalent and says so; the host captions the other speaker; lessons set no time limit on speaking.
- **Reduced motion** The meter becomes a static "sound detected" dot.
- Browser `SpeechRecognition` where present; the typed path always counts the same; audio is never stored (finance decision 10).

#### 4.1.29 `span-track`

primitive · tier primitive · cluster `core` · **P2** · size M · spec ML 3.1 · first use 2.1 L119

Much of financial machine learning and paper replication is about which interval overlaps which: a label's return window against a test fold (purging), a feature's availability against a decision time (leakage), the formation.

- **Composes** `plot-2d`, `drag-point`, `marks`.
- **Config** `SpanTrackConfig { axis, spans, layout, rowLabels?, editable?, editableRoles?, snap?, select?, selectableRoles?, concurrency?, maxRowsShown? }`.
- **Answers** `set`, `interval`, `point`, `state`.
- **AI hooks** targets `span:<id>`, `row:<r>`, `handle:<id>:start`, `handle:<id>:end`, `band:<role>`, `series:concurrency`; describe, e.g. "40 label spans, lengths 3 to 8 days. Test fold days 21 to 30. Selected: 14, 15, 16."
- **Accessibility** A group named by the host ("Label spans, 40 examples"). Each span is focusable with a name such as "Label 14, days 30 to 38, training". Selection is announced on commit ("Selected 6 of 40").
- **Reduced motion** Snaps and role changes are instant.

### 4.2 Inputs

#### 4.2.1 `choice`

primitive · tier input · cluster `core` · **P0** · size S · spec stage0 4.1, calc-linalg 3.15 · first use 0.1 L1

Single and multiple choice on flat cards.

- **Composes** `live-formula`.
- **Config** `ChoiceCardsConfig { options, multi?, columns?, shuffle? }`.
- **Answers** `choice`.
- **AI hooks** targets `option:<id>`; describe, e.g. "Options: A 5/36, B 1/36, C 1/6, D 5/6. Selected: B."
- **Accessibility** single choice is a `radiogroup`; multi is a group of checkboxes. The verdict reaches the live region.
- **Reduced motion** no pop.
- Options may hold a read-only mini plot (calc-linalg 3.15, prob-stats 4.2); every distractor carries a misconception id, a feedback line and a show-why key.

#### 4.2.2 `numeric-input`

primitive · tier input · cluster `core` · **P0** · size M · spec stage0 4.2, calc-linalg 3.16 · first use 0.1 L1

One or more number fields.

- **Composes** nothing (a leaf primitive).
- **Config** `NumericEntryConfig { fields, layout?, keypad?, autoAccept? }`.
- **Answers** `numeric`, `interval`.
- **AI hooks** targets `field:<id>`; describe, e.g. "Field 'outcomes left': 12 (reads as 12)."
- **Accessibility** labelled inputs. The parse preview is linked with `aria-describedby`.
- **Reduced motion** no motion of its own.
- **Modes added** probability forms (fraction, decimal, percent, odds) and the $[0, 1]$ nudge (P0, prob-stats 4.2).
- On a coarse pointer it renders `inputmode="none"` and opens `ui/Keypad` and `SymbolBar` (arch decision 35).
- Also produces `interval` answers (`[3.35, 3.45)`).

#### 4.2.3 `expression-input`

primitive · tier input · cluster `core` · **P0** · size L · spec stage0 4.3, calc-linalg 3.17 · first use 0.1 L12

Maths input through a MathLive math-field, graded by `cas`.

- **Composes** nothing (a leaf primitive).
- **Config** `ExpressionEntryConfig { keyboard, variables?, placeholder?, prefix? }`.
- **Answers** `expression`.
- **AI hooks** targets `field`, `field:<id>`; describe, e.g. "Entered: (x + 3)(x − 2)".
- **Accessibility** MathLive speaks maths [sourced: MathLive documentation describes its spoken output, not re-checked here]. The ASCII fallback is always available as a toggle.
- **Reduced motion** no motion of its own.
- **Modes added** probability keyboard layer (P0, prob-stats 4.2).
- MathLive field loaded lazily, parsed by the Compute Engine LaTeX parser to MathJSON; plain field fallback (arch 11.6).

#### 4.2.4 `card-sort`

composite · tier input · cluster `core` · **P0** · size S · spec stage0 4.4 · first use 0.2 L2

Sort cards in one of three modes.

- **Composes** `token-tray`.
- **Config** `CardSortConfig { cards, bins?, targets? }`.
- **Answers** `mapping`, `ordering`.
- **AI hooks** targets `card:<id>`, `bin:<id>`; describe, e.g. "Bin 'linear': y = 2x + 1, y = 3. Bin 'not linear': y = x². Unplaced: y = 1/x."
- **Accessibility** as `token-tray`.
- **Reduced motion** as `token-tray`.
- **Modes added** bins for sampling schemes (P0, prob-stats 5); match mode with mini-plot cards (P1, prob-stats 5); two-bin sort (P2, 2.1 sample, curriculum).

#### 4.2.5 `derivation-steps`

composite · tier input · cluster `core` · **P0** · size L · spec calc-linalg 4.1, stage0 4.5 · first use 0.1 L1

Derive screens (design 5.2): a derivation shown as aligned lines where some lines are blank (type them), shuffled (order them) or missing a justification (pick it from a tray).

- **Composes** `token-tray`, `expression-input`, `live-formula`, `stepper`, `choice`, `card-sort`.
- **Config** `DerivationStepsConfig { lines, shuffle?, chips?, grid?, canvas? }`.
- **Answers** `choice`, `ordering`, `expression`, `set`, `mapping`.
- **AI hooks** targets `line:<id>`, `chip:<id>`, `cell:<row>,<col>`, `why:<id>`; describe, e.g. "Derivation, 4 lines, line 3 missing. Line 1: P(A|B) = |A∩B|/|B|. ..."; tryable `chip:<id>`.
- **Accessibility** Lines form an ordered list; each blank is a labelled field; chips use token-tray semantics.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** `links` from a line to elements of a widget on an earlier screen (P0, 1.3 sample, curriculum); fill mode with a `leap` block (P1, 1.6 sample, curriculum).
- Absorbs Stage 0's `derivation`; keeps its `step` and `predict` modes; `leap` blocks (naive, fails, points to) for motivated leaps.

#### 4.2.6 `free-response`

composite · tier input · cluster `core` · **P0** · size M · spec stage0 4.6 · first use 0.1 L41

Long-form written answers ("explain", "show that", proofs in words), with inline maths using `$...$` and a maths keyboard button.

- **Composes** `expression-input`, `scratch-pad`, `voice-capture`.
- **Config** `FreeResponseConfig { rubric, point, marks, model, minWords?, aiMarking? }`.
- **Answers** `long-form`.
- **AI hooks** targets `answer`.
- **Accessibility** a labelled textarea; the rubric as checkboxes.
- **Reduced motion** no motion of its own.
- **Modes added** voice input through `voice-capture`; `tutor-draft` and `partner` rubric marking (P1, finance 5); timed no-notes mode for `viva` (P1, ML 5).

#### 4.2.7 `order-ticket`

primitive · tier input · cluster `core` · **P1** · size M · spec finance 3.4 · first use 1.7 L29

Every order the learner sends.

- **Composes** nothing (a leaf primitive).
- **Config** `OrderTicketConfig { tick, lot, types, tifs, allowPostOnly, allowIceberg, quickSizes?, preview, fixed? }`.
- **Answers** `state`.
- **AI hooks** targets `ticket:side`, `ticket:type`, `ticket:px`, `ticket:qty`, `ticket:tif`, `ticket:preview`.
- **Accessibility** Form semantics; errors linked by `aria-describedby`; the preview in the polite live region.
- **Reduced motion** no motion of its own.

#### 4.2.8 `quote-entry`

primitive · tier input · cluster `core` · **P1** · size S · spec finance 3.5 · first use 1.7 L42 (through `market-maker-sim`)

Making markets: `dealer-sim` in manual mode, `mm-game`, and the quote mode of `order-book`.

- **Composes** nothing (a leaf primitive).
- **Config** `QuoteEntryConfig { tick, width?, sizes?, shorthand, voice, host? }`.
- **Answers** `numeric`, `state`.
- **AI hooks** targets `quote:bid`, `quote:ask`, `quote:width`, `quote:centre`, `quote:text`.
- **Accessibility** "Your market: bid 30, ask 35, width 5, centre 32.5", announced on send.
- **Reduced motion** no motion of its own.

---

## 5. Composites

254 composites, grouped by cluster in curriculum order and, inside a cluster, by first use.

### 5.1 Core (shared by every cluster)

#### 5.1.1 `code-cell`

composite · tier composite · cluster `core` · **P0** · size L · spec programming 4.1, stage0 10.4, calc-linalg 3.18 · first use 0.1 L42

The code exercise: edit, Run against visible examples, Submit against hidden tests, read the results.

- **Composes** `code-surface`, `text-terminal`, `value-table`, `diff-view`, `node-link`, `parsons`; services `python-runner`, `sql-runner`, `cpp-runner`, `shell-interpreter`, `vfs`, `handoff`.
- **Config** `CodeCellConfig { language, mode, layout?, brief, files, entry?, examples, suite, db?, data?, stdin?, parsons?, review?, answer?, heldOut? }`.
- **Answers** `code`.
- **AI hooks** targets `line:<n>`, `test:<k>`, `file:<path>`, `cell:<k>`, `run`, `submit`; describe, e.g. "Drill max_drawdown (Python). Last submit: 5 of 7 hidden tests passed; first failure 'flat prices': expected 0.0, got nan."
- **Accessibility** the result summary is announced ("3 of 4 examples passed; first failure: test 2, expected 0.25, got 0.2"); results form a list.
- **Reduced motion** no stagger.
- **Modes added** helpers `zq_rng`, `assert_mc_close`, `assert_fixture` (P0, prob-stats 4.2); NumPy subspace helpers (P0, calc-linalg 12.3); `zq_fin` and `zq_market` preludes (P1, finance 5); ML helpers and the local paste-back mode for PyTorch (P2, ML 4).
- Absorbs Stage 0's `code-editor`; one widget for Python, SQL, C++ and shell.
- Python is Pyodide 314.0.7 on both targets (arch decision 15): the catalogues' MicroPython and `ulab` tags are void; a drill declares `needs` and hands off only for C++ or for a package the course has not budgeted in the Artifact.
- Cluster `core` because 20 of the 21 curriculum items use it.

### 5.2 Number and mental arithmetic (0.1, 0.5)

#### 5.2.1 `place-value-chart`

composite · tier composite · cluster `number` · **P0** · size M · spec stage0 5.1 · first use 0.1 L1

Makes place value physical.

- **Composes** `token-tray`, `live-formula`, `stepper`.
- **Config** `PlaceValueConfig { base?, columns, initial?, supply?, allowShift?, allowRegroup?, allowBreak?, display, readout? }`.
- **Answers** `numeric`, `state`.
- **AI hooks** targets `col:<place>`, `op:times-10`, `op:times-100`, `op:divide-10`, `op:divide-100`, `tray:<place>`, `chip:swap-<place>`; describe, e.g. "Base 10. Hundreds 3, Tens 12 (overfull), Ones 4. Value 424."; tryable `chip:swap-<place>`.
- **Accessibility** each column is a list ("Tens: 4 counters"). The readout is live ("3,405.2"). The keyboard path is as in the spec.
- **Reduced motion** fuse cross-fades; shift jumps with a 120ms fade.
- Element ids from the 0.1 sample lesson (request R4): `col:<place>`, `op:times-10`, `op:times-100`, `op:divide-10`, `op:divide-100`, `tray:<place>`, `chip:swap-<place>`; predicate `pv-fewest-pieces` with a Python twin.

#### 5.2.2 `written-method`

composite · tier composite · cluster `number` · **P0** · size M · spec stage0 5.8 · first use 0.1 L2

Animates and drills written algorithms with the reasoning visible.

- **Composes** `stepper`, `live-formula`, `numeric-input`, `value-table`.
- **Config** `WrittenMethodConfig { operands, dp?, mode, checkPer, remainders? }`.
- **Answers** `state`, `numeric`, `expression`.
- **AI hooks** targets `cell:<r>,<c>`, `remainder:<k>`; describe, e.g. "Long division 1 ÷ 7 to 6 dp: quotient so far 0.142; remainders 1, 3, 2, 6; next digit pending."
- **Accessibility** the grid is a table with row labels ("partial product 2"). Each step's caption reaches the live region: "7 into 30 goes 4, remainder 2".
- **Reduced motion** digits appear.

#### 5.2.3 `area-model`

composite · tier composite · cluster `number` · **P0** · size M · spec stage0 5.3 · first use 0.1 L3

Multiplication as area.

- **Composes** `plot-2d`, `drag-point`, `region-select`, `live-formula`.
- **Config** `AreaModelConfig { mode, width, height, splits?, unit?, resizable?, snap?, entry?, n?, max? }`.
- **Answers** `numeric`, `state`, `set`, `expression`.
- **AI hooks** targets `handle:corner`, `split:x-<k>`, `split:y-<k>`; describe, e.g. "Rectangle 23 by 47, split 20 + 3 by 40 + 7. Entered: 800, 140, 120, ? (bottom right)."
- **Accessibility** handles are sliders with spoken values. Each sub-rectangle is announced with its dimensions and product. There is a table view of the partial products.
- **Reduced motion** stepped.

#### 5.2.4 `bar-model`

composite · tier composite · cluster `number` · **P0** · size M · spec stage0 5.2 · first use 0.1 L4

Fraction bars and tape diagrams in one widget.

- **Composes** `region-select`, `slider`, `drag-point`, `live-formula`, `number-line`.
- **Config** `BarModelConfig { mode, bars, whole?, maxParts?, allowRefine?, scale?, layout? }`.
- **Answers** `set`, `numeric`, `state`, `expression`, `parts`.
- **AI hooks** targets `bar:<id>`, `bar:<id>-part-<k>`, `brace:<k>`; describe, e.g. "Bar A: 4 parts, shaded 1 to 3 (3/4). Bar B: 8 parts, shaded 1 to 5 (5/8)."
- **Accessibility** each bar is a group ("Bar A, 8 equal parts, 3 shaded"). Parts are toggle buttons ("part 3 of 8, shaded"). There is a table view of the bars.
- **Reduced motion** the end states, with Play.

#### 5.2.5 `expression-tree`

composite · tier composite · cluster `number` · **P0** · size M · spec stage0 5.7 · first use 0.1 L9

The structure of an expression as a tree.

- **Composes** `marks`, `token-tray`, `live-formula`, `stepper`.
- **Config** `ExpressionTreeConfig { expression, mode, values?, palette?, conventions, linkedTex? }`.
- **Answers** `numeric`, `ordering`, `state`, `expression`.
- **AI hooks** targets `node:root`, `node:<path>`; describe, e.g. "Tree of 3 + 4 × 2: root + with children 3 and ×(4, 2). Evaluated: none."
- **Accessibility** `role="tree"`; nodes read as "multiply: 3 and (4 + 5)"; the linked expression is highlighted together with the node.
- **Reduced motion** instant collapse; the show-why is a before-and-after.
- Drawn by `node-link`; a Python precedence mode serves 1.1 L7.

#### 5.2.6 `factor-tree`

composite · tier composite · cluster `number` · **P0** · size S · spec stage0 5.5 · first use 0.1 L12

Prime factorisation by splitting, used for.

- **Composes** `token-tray`, `marks`, `numeric-input`, `stepper`.
- **Config** `FactorTreeConfig { second?, split, indexForm?, maxDepth? }`.
- **Answers** `state`, `expression`, `set`.
- **AI hooks** targets `node:<path>`, `node:0-1`, `index:form`; describe, e.g. "Tree for 360: 360 → 36 × 10; 36 → 6 × 6 (unsplit); 10 → 2 × 5 (both marked prime)."
- **Accessibility** `role="tree"` with tree items such as "36, split into 6 and 6".
- **Reduced motion** instant.
- Drawn by `node-link` in tidy-tree layout.

#### 5.2.7 `venn-diagram`

composite · tier composite · cluster `number` · **P0** · size M · spec stage0 5.6 · first use 0.1 L14

Two or three sets.

- **Composes** `region-select`, `token-tray`, `numeric-input`.
- **Config** `VennConfig { sets, universe?, elements?, given?, task, regionNames? }`.
- **Answers** `mapping`, `set`, `numeric`, `state`.
- **AI hooks** targets `element:<id>`; describe, e.g. "A (multiples of 2), B (multiples of 3). A only: 2, 4, 8. AB: 6. B only: 3, 9. Outside: 1, 5, 7. Shaded: none."
- **Accessibility** each region is a button ("In A and B, not C: 4 items"). The table view lists each region with its elements or count.
- **Reduced motion** a static highlight.
- **Modes added** Probability mode: atom masses edited through `mass-editor`; non-negative atoms enforced (P0, prob-stats 5).

#### 5.2.8 `modular-clock`

composite · tier composite · cluster `number` · **P0** · size S · spec stage0 5.12 · first use 0.1 L16

Remainders and cycles.

- **Composes** `marks`, `drag-point`, `stepper`, `value-table`.
- **Config** `ModularClockConfig { start, ops?, kind, k, mode, labels? }`.
- **Answers** `numeric`, `set`, `state`.
- **AI hooks** targets `pos:<k>`, `hand`, `orbit`, `op:<k>`.
- **Accessibility** positions form a listbox. A history table. Describe: "Orbit 3, 9, 7, 1, 3: cycle length 4".
- **Reduced motion** the hand jumps; the orbit appears whole.

#### 5.2.9 `speed-drill`

composite · tier composite · cluster `number` · **P0** · size M · spec stage0 11.1 · first use 0.5 L1

Timed arithmetic in the Zetamac format and its variants.

- **Composes** `speed-timer`, `numeric-input`, `value-table`; services `seeded-rng`.
- **Config** `SpeedDrillConfig { ranges?, add, mul, ops?, durationS, deck?, target?, adaptive? }`.
- **Answers** `state`.
- **AI hooks** targets `score`, `slow:<k>`, `op:<name>`; describe, e.g. "Score 27: add 11, sub 7, mul 6, div 3. Slowest: 7 × 8 (4.1 s), 96 − 39 (5.2 s)."
- **Accessibility** each new question goes to the polite live region. Time warnings come at 30 and 10 seconds. An untimed mode exists for learners for whom timing is a barrier; it never counts towards the exit test, and says so.
- **Reduced motion** the end score appears.
- **Modes added** decks `ev`, `odds`, `options`, `sequences` and 80-in-8 options (P2; `options` P1, finance 5).
- Carries its own keypad (`ui/Keypad`); the Zetamac defaults are configuration.

#### 5.2.10 `double-number-line`

composite · tier composite · cluster `number` · **P0** · size S · spec stage0 5.4 · first use 0.1 L24

Two aligned scales with a shared marker, for proportional reasoning.

- **Composes** `number-line`, `drag-point`, `value-table`.
- **Config** `DoubleNumberLineConfig { top, bottom, ratio, given?, marker?, showUnitRate? }`.
- **Answers** `numeric`, `point`, `state`.
- **AI hooks** targets `marker`, `pin:<k>`, `tick:top-<v>`, `tick:bottom-<v>`; describe, e.g. "Top: percent 0 to 150. Bottom: £0 to £90. Marker at 120% matching £54. Pins: 100% matching £45."
- **Accessibility** the marker's `aria-valuetext` reads "120 percent matches £54". The table view lists the pins.
- **Reduced motion** no motion of its own.

#### 5.2.11 `multiplier-chain`

composite · tier composite · cluster `number` · **P0** · size M · spec stage0 5.9 · first use 0.1 L25

Percentages as multipliers.

- **Composes** `marks`, `token-tray`, `slider`, `live-formula`, `plot-2d`.
- **Config** `MultiplierChainConfig { start, unit?, steps, palette?, view, compounding?, logPanel? }`.
- **Answers** `numeric`, `expression`, `state`.
- **AI hooks** targets `start`, `chip:<k>`, `bar:<k>`, `slider:rate`; describe, e.g. "Start £1,000. Steps ×1.10, ×1.10, ×1.10. Final £1,331.00. Overall +33.1%."; tryable `chip:<k>`, `slider:rate`.
- **Accessibility** a table view (step, multiplier, balance). The live region reads "After 3 steps: £1,331.00".
- **Reduced motion** instant.
- **Modes added** tile mode: palette, log axis, target line, partial tile, Glue, halving (P0, 0.3 sample, curriculum); returns preset (P1, finance 5).

#### 5.2.12 `unit-chain`

composite · tier composite · cluster `number` · **P0** · size S · spec stage0 5.10 · first use 0.1 L30

Dimensional analysis: multiply by conversion fractions equal to 1 until the units cancel to the target.

- **Composes** `token-tray`, `live-formula`, `numeric-input`; services `unit-algebra`.
- **Config** `UnitChainConfig { value, unit, target, palette, id, num, den, allowPowers? }`.
- **Answers** `state`, `numeric`, `expression`.
- **AI hooks** targets `card:<k>`, `result`; describe, e.g. "Start 72 km/h. Chain: (1000 m / 1 km), (1 h / 3600 s). Units left: m/s."
- **Accessibility** the chain reads as speech: "72 kilometres per hour, times 1000 metres over 1 kilometre, times 1 hour over 3600 seconds; units left: metres per second".
- **Reduced motion** instant.

#### 5.2.13 `fermi-estimator`

composite · tier composite · cluster `number` · **P0** · size M · spec stage0 5.13 · first use 0.1 L40

Order-of-magnitude estimation.

- **Composes** `number-line`, `drag-point`, `token-tray`, `live-formula`, `value-table`.
- **Config** `FermiEstimatorConfig { reference, value, unit, source, year, cards, id, label, unit?, mode, tolFactor }`.
- **Answers** `interval`, `numeric`, `point`, `set`.
- **AI hooks** targets `factor:<k>-lo`, `factor:<k>-hi`, `result`; describe, e.g. "London population [5m, 10m] × share with a piano [1%, 5%] × tunings per year [0.5, 2] ÷ tunings per tuner per year [500, 1,000]. Product [25, 1,000]."
- **Accessibility** handles read as "low 2 million, high 10 million". There is a table view.
- **Reduced motion** it appears.
- **Modes added** exports a log-normal estimate to `mm-game` and `calibration-lab` (P2, finance 5).

#### 5.2.14 `strategy-trainer`

composite · tier composite · cluster `number` · **P0** · size M · spec stage0 11.2 · first use 0.5 L3

Teaches the mental strategies behind fast arithmetic, then drills each one.

- **Composes** `area-model`, `number-line`, `speed-timer`, `numeric-input`, `choice`; services `seeded-rng`.
- **Config** `StrategyTrainerConfig { phase, n, timed?, show? }`.
- **Answers** `numeric`, `state`, `choice`.
- **AI hooks** targets `split`, `partial:<k>`, `answer`; describe, e.g. "Strategy: compensation. Item 99 × 7. Split: 100 × 7 − 1 × 7. Entered: 693."
- **Accessibility** as the primitives.
- **Reduced motion** as the primitives.
- **Modes added** decimal, percentage and fast-division strategies (P2, finance 5).

### 5.3 Algebra (0.2)

#### 5.3.1 `algebra-tiles`

composite · tier composite · cluster `algebra` · **P0** · size M · spec stage0 6.2 · first use 0.1 L7

An area model with symbolic tiles: $x^2$, $x$ and $1$, plus their negatives and, for two variables, $y$, $xy$ and $y^2$.

- **Composes** `token-tray`, `area-model`, `live-formula`.
- **Config** `AlgebraTilesConfig { initial?, frame?, top?, left?, task, zeroPairs? }`.
- **Answers** `expression`, `state`, `set`.
- **AI hooks** targets `tile:<id>`, `frame:top`, `frame:left`, `corner`.
- **Accessibility** tiles read as "positive x tile". Describe: "2 x-squared, 5 x, 6 units; frame empty".
- **Reduced motion** instant.
- Builds on `area-model` (embedded) and `token-tray`; zero pairs cancel.

#### 5.3.2 `graph-explorer`

composite · tier composite · cluster `algebra` · **P0** · size L · spec stage0 6.6 · first use 0.1 L26

The main function-graph widget.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `live-formula`, `value-table`.
- **Config** `GraphExplorerConfig { axes, family?, defining?, curves?, overlays?, forms?, table?, dragCurve? }`.
- **Answers** `point`, `curve`, `numeric`, `expression`, `state`.
- **AI hooks** targets `point:<id>`, `slider:<id>`, `term:<param>`, `overlay:<name>`, `curve:main`, `form:<name>`; describe, e.g. "Line through A(0, −1) and B(2, 3): y = 2x − 1. Slope triangle on: rise 4, run 2. Given point P(4, 6)."; tryable `slider:<id>`.
- **Accessibility** The equation is live and debounced: "y = 2x − 1". - Handles read as "A at (1, 1)". - Overlays are described in words: "gradient 2: rise 4 over run 2". - Table view.
- **Reduced motion** stepped, with Play.
- **Modes added** reflect in $y = x$ toggle (P0, 0.3 sample, curriculum); integer-domain functions drawn as stems (P0, prob-stats 5).

#### 5.3.3 `equation-workbench`

composite · tier composite · cluster `algebra` · **P0** · size L · spec stage0 6.4 · first use 0.1 L35

Symbolic manipulation in which the learner chooses every move and the engine carries it out exactly.

- **Composes** `live-formula`, `number-line`, `marks`, `derivation-steps`, `expression-input`; services `cas`.
- **Config** `WorkbenchConfig { start, goal, ops, identities?, entry, domain? }`.
- **Answers** `expression`, `state`.
- **AI hooks** targets `line:<k>`, `term:<line>-<k>`, `op:menu`, `strip`; describe, e.g. "Goal: solve for x. Line 1: 3x + 2 = 11. Line 2: 3x = 9 (subtracted 2 from both sides). Selected: 3x."
- **Accessibility** MathML for each line. Terms are buttons with spoken labels ("term: 3 x"). The menu uses `role="menu"`. History is a list.
- **Reduced motion** lines cross-fade.
- The learner chooses every move; `cas` carries it out exactly.

#### 5.3.4 `function-machine`

composite · tier composite · cluster `algebra` · **P0** · size S · spec stage0 6.3 · first use 0.2 L1

Functions as rules from input to output.

- **Composes** `token-tray`, `value-table`, `live-formula`, `stepper`.
- **Config** `FunctionMachineConfig { hidden?, palette?, task, machines?, domainRules? }`.
- **Answers** `expression`, `numeric`, `ordering`, `state`.
- **AI hooks** targets `op:<k>`, `input`, `output`, `log`, `reverse`.
- **Accessibility** a log table, with each stage announced. Describe: "Machine: ×2 then +3. In 5, out 13."
- **Reduced motion** a row of intermediate values, with Play.

#### 5.3.5 `balance-scale`

composite · tier composite · cluster `algebra` · **P0** · size M · spec stage0 6.1 · first use 0.2 L18

An equation is a balance.

- **Composes** `token-tray`, `marks`, `live-formula`.
- **Config** `BalanceConfig { equation, relation?, allowBalloons?, actions?, revealX?, maxTokens? }`.
- **Answers** `state`, `numeric`.
- **AI hooks** targets `pan:left`, `pan:right`, `token:<id>`, `action:<name>`.
- **Accessibility** Describe: "Left: 3 boxes and 2 units. Right: 1 box and 8 units. Balanced." - Tilts reach the live region: "Tipped left: left is heavier by 2".
- **Reduced motion** the beam takes its new angle at once, without oscillating.

#### 5.3.6 `equation-stack`

composite · tier composite · cluster `algebra` · **P0** · size M · spec stage0 6.5 · first use 0.2 L49

Systems of equations as stacked rows.

- **Composes** `live-formula`, `numeric-input`, `token-tray`, `plot-2d`, `marks`, `derivation-steps`.
- **Config** `EquationStackConfig { vars, ops, graph?, exact? }`.
- **Answers** `point`, `numeric`, `state`, `choice`.
- **AI hooks** targets `row:<k>`, `coef:<row>-<var>`, `line:<k>`, `intersection`.
- **Accessibility** rows form a table; operations are buttons. Describe: "R1: 2x + 3y = 12. R2: x − y = 1. Operations: none."
- **Reduced motion** lines jump; the pivot is a before-and-after.

#### 5.3.7 `sign-chart`

composite · tier composite · cluster `algebra` · **P0** · size M · spec calc-linalg 5.11, stage0 6.9 · first use 0.2 L70

Sign analysis on a number line: factors of an expression for inequalities, $f'$ for monotonicity, $f''$ for concavity, linked to a graph.

- **Composes** `number-line`, `region-select`, `drag-point`, `marks`, `choice`, `plot-2d`, `value-table`.
- **Config** `SignChartConfig { rows, id, label, expr?, points, truePoints, linkPlot?, derivedRow?, relation, given, graph? }`.
- **Answers** `set`, `choice`, `interval`, `point`, `state`.
- **AI hooks** targets `point:<i>`, `cell:<row>:<interval>`, `cell:<row>-<k>`, `critical:<k>`, `solution:<k>`.
- **Accessibility** Grid semantics; each cell named "row x minus 1, interval 1 to 3".
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- One spec: calc-linalg's derivative rows plus Stage 0's "undefined" state and solution-interval selection.

#### 5.3.8 `iteration-cobweb`

composite · tier composite · cluster `algebra` · **P0** · size S · spec stage0 6.10 · first use 0.2 L107

Iteration $x_{n+1} = g(x_n)$.

- **Composes** `plot-2d`, `marks`, `drag-point`, `stepper`, `value-table`.
- **Config** `IterationCobwebConfig { x0, maxIter, show, dp? }`.
- **Answers** `numeric`, `choice`, `state`.
- **AI hooks** targets `x0`, `segment:<k>`, `rearrangement:<k>`.
- **Accessibility** table view. Describe: "x0 = 2. Iterates 2, 2.25, 2.41, ... settling near 2.62".
- **Reduced motion** segments appear.
- **Modes added** cobweb of $s \mapsto G(s)$ on $[0, 1]$, hosted by `generating-function` (P0, prob-stats 5).

### 5.4 Geometry (0.3, GCSE geometry)

#### 5.4.1 `geometry-board`

composite · tier composite · cluster `geometry` · **P0** · size L · spec stage0 7.1 · first use 0.3 L1

Dynamic geometry for GCSE geometry and for trigonometry.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `value-table`, `live-formula`, `stepper`.
- **Config** `GeometryBoardConfig { axes?, objects, tools, measure?, preset?, keyframes?, answerTargets?, notToScale? }`.
- **Answers** `set`, `numeric`, `point`, `state`, `choice`.
- **AI hooks** targets `circle:1`; describe, e.g. "Triangle ABC: A(0, 0), B(4, 0), C(1, 3). AB = 4, angle A = 71.6°. Tool: move. Selected: none."
- **Accessibility** Every object has a name and its properties: "triangle ABC; angle ABC = 47 degrees". - An object list is the text alternative. - Construction works from the keyboard. - Measurement changes are announced, debounced.
- **Reduced motion** keyframes step, with Play; flashes become static highlights.
- **Modes added** points on a circle with a region counter; the $64 = 65$ dissection preset (P0, 0.3 L125, L128, curriculum).

#### 5.4.2 `solid-viewer`

composite · tier composite · cluster `geometry` · **P0** · size M · spec stage0 7.2 · first use 0.3 L8

3D solids for GCSE measures.

- **Composes** `plot-3d`, `slider`, `region-select`, `value-table`, `live-formula`.
- **Config** `SolidViewerConfig { dims, editable?, show?, net?, diagonals?, views?, task }`.
- **Answers** `numeric`, `set`, `state`.
- **AI hooks** targets `face:<id>`, `edge:<id>`, `diagonal:<id>`, `view:<name>`, `net`; tryable `view:<name>`.
- **Accessibility** view buttons; a list of faces with their areas; a description of the solid and its dimensions.
- **Reduced motion** the net steps; cubes appear.

### 5.5 Precalculus, GCSE statistics and probability (0.3)

#### 5.5.1 `counting-slots`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 9.9 · first use 0.1 L13

Counting by the multiplication principle.

- **Composes** `token-tray`, `stepper`, `value-table`, `live-formula`.
- **Config** `CountingSlotsConfig { id, label, slots, repetition, ordered, restrictions?, together, apart, fixed, slot, option, mode, stars?, boxes? }`.
- **Answers** `numeric`, `expression`, `state`, `set`.
- **AI hooks** targets `slot:<i>`, `option:<id>`, `group:<k>`, `divider:<i>`, `product`.
- **Accessibility** the `token-tray` model, and a table of arrangements.
- **Reduced motion** instant.
- **Modes added** procedure comparison, multinomial, stars-and-bars probability toggle (P0, prob-stats 5).
- First used at 0.1 L13, so it ships in the first Stage 0 wave (curriculum request R3).

#### 5.5.2 `scatter-fit`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 8.3 · first use 0.2 L46

Bivariate data.

- **Composes** `plot-2d`, `drag-point`, `marks`, `slider`, `value-table`.
- **Config** `ScatterFitConfig { seed, model, n, noise, outliers?, task, show?, axes, sseRatio? }`.
- **Answers** `curve`, `numeric`, `choice`, `set`.
- **AI hooks** targets `handle:1`, `handle:2`, `point:<k>`, `residual:<k>`, `sse`.
- **Accessibility** a table view. Describe: "Line y = 1.8x + 2.1; squared-error total 41.2". Correlation is given in words in Stage 0, and as $r$ from 1.6.
- **Reduced motion** it appears.
- **Modes added** $R^2$ and residual plot (P1, prob-stats 5).

#### 5.5.3 `dot-plot-stats`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 8.1 · first use 0.2 L75

Summary statistics by manipulation.

- **Composes** `number-line`, `drag-point`, `marks`, `value-table`.
- **Config** `DotPlotStatsConfig { min, max, step, n?, editable, show, compare?, quartiles }`.
- **Answers** `numeric`, `state`, `point`, `choice`.
- **AI hooks** targets `dot:<id>`, `mean`, `median`, `box`, `prediction:<stat>`; describe, e.g. "n = 7: 2, 3, 3, 5, 6, 8, 20. Mean 6.71, median 5. Shown: mean, median."
- **Accessibility** a table view of the sorted data and its statistics. Dots read as "data point 3 at 7". Live: "Mean 6.2, median 5".
- **Reduced motion** the tilt does not oscillate.
- **Modes added** movable centre with a sum-of-squares readout; divisor chips (P1, prob-stats 5).

#### 5.5.4 `complex-plane`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 9.13 · first use 0.2 L85

Complex numbers as points and arrows.

- **Composes** `plot-2d`, `marks`, `drag-point`, `live-formula`, `graph-explorer`, `slider`.
- **Config** `ComplexPlaneConfig { id, re, im, movable, ops, form, quadratic?, a, b, c, editable?, argUnits }`.
- **Answers** `point`, `expression`, `numeric`, `set`.
- **AI hooks** targets `point:<id>`, `result`, `arg:<id>`, `op:<name>`, `parabola`.
- **Accessibility** points announce their real and imaginary parts and their polar readouts.
- **Reduced motion** stepped.
- **Modes added** locus tracer with region shading (P0, 0.3 L93, curriculum); AR and MA roots against the unit circle (P2, prob-stats 5).
- First used at 0.2 L85 (curriculum request R3).

#### 5.5.5 `sequence-lab`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 9.4 · first use 0.3 L39

Sequences as lists, rules and plots.

- **Composes** `value-table`, `marks`, `plot-2d`, `slider`, `live-formula`.
- **Config** `SequenceLabConfig { rule, recurrence, u1, show, n, task, params? }`.
- **Answers** `expression`, `numeric`, `state`, `choice`.
- **AI hooks** targets `term:<n>`, `diff:<level>-<n>`, `rule`, `plot`; describe, e.g. "Terms 3, 7, 11, 15, ?. First differences 4, 4, 4."
- **Accessibility** table semantics and a table view of the plot.
- **Reduced motion** no motion of its own.
- **Modes added** explicit and recursive views side by side, index-origin toggle, two-term mode with ratio row, tolerance band (P0, 0.3 L39 to L43, curriculum).
- Partial sums live in `series-explorer` (Stage 0 15.1).

#### 5.5.6 `slide-rule`

composite · tier composite · cluster `precalc` · **P0** · size S · spec stage0 9.1 · first use 0.3 L51

Logarithms as lengths.

- **Composes** `number-line`, `drag-point`, `live-formula`, `marks`.
- **Config** `SlideRuleConfig { base?, showLengths?, task }`.
- **Answers** `numeric`, `state`, `choice`.
- **AI hooks** targets `upper:<v>`, `lower:<v>`, `cursor`, `length:<k>`.
- **Accessibility** sliders. Describe: "Lower 1 under upper 2. Cursor at lower 3 reads upper 6."
- **Reduced motion** no motion of its own.

#### 5.5.7 `sum-visualiser`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 9.5 · first use 0.3 L60

Shows why summation formulas are true.

- **Composes** `region-select`, `token-tray`, `stepper`, `marks`, `live-formula`, `slider`.
- **Config** `SumVisualiserConfig { n?, r?, a?, sigma? }`.
- **Answers** `numeric`, `expression`, `state`, `choice`.
- **AI hooks** targets `copy`, `staircase`, `piece:<k>`, `term:<k>`, `limit:line`.
- **Accessibility** a description and a table of partial sums.
- **Reduced motion** stepped.
- Keeps the proofs (Gauss, odd squares, area fill, shift-and-subtract); partial sums move to `series-explorer`.

#### 5.5.8 `unit-circle`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 9.2 · first use 0.3 L66

Trigonometric functions as the coordinates of a rotating point: $\cos\theta$ is $x$ and $\sin\theta$ is $y$.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `live-formula`, `value-table`.
- **Config** `UnitCircleConfig { snap?, overlays, exactLabels?, range? }`.
- **Answers** `point`, `numeric`, `set`, `expression`.
- **AI hooks** targets `point`, `seg:cos`, `seg:sin`, `seg:tan`, `arc`, `hline`, `quadrant:<k>`; describe, e.g. "θ = 150° (5π/6). cos −0.866, sin 0.5. Shown: cos, sin, reference triangle."
- **Accessibility** the angle slider reads "angle 150 degrees; cos −0.866; sin 0.5". There is a table of the special angles.
- **Reduced motion** before-and-after.
- Angle handle and the triangle, sector, triangle area overlays requested by calc-linalg 12.3 (1.3.1 L4, 1.3.2 L8).

#### 5.5.9 `circle-to-wave`

composite · tier composite · cluster `precalc` · **P0** · size S · spec stage0 9.3 · first use 0.3 L71

Links rotation to waves.

- **Composes** `unit-circle`, `graph-explorer`, `slider`, `drag-point`.
- **Config** `CircleToWaveConfig { params?, target?, units }`.
- **Answers** `numeric`, `expression`, `curve`, `state`.
- **AI hooks** targets `circle:point`, `tracer`, `slider:<p>`, `connector`, `phasor:<k>`, `resultant`; tryable `slider:<p>`.
- **Accessibility** sliders; the equation described in words; a table of wave values at multiples of 30°.
- **Reduced motion** Play advances 15° per press instead of running.
- Embeds `unit-circle`; Fourier sums are a P2 mode.

#### 5.5.10 `tree-diagram`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 8.5 · first use 0.3 L98

Tree diagrams in two modes.

- **Composes** `marks`, `numeric-input`, `region-select`, `live-formula`, `stepper`.
- **Config** `TreeDiagramConfig { label, outcomes, probs?, dependsOnPrevious?, mode, event?, grow, maxLeaves? }`.
- **Answers** `numeric`, `state`, `set`.
- **AI hooks** targets `branch:<path>`, `leaf:<path>`, `sum`.
- **Accessibility** `role="tree"`. Branches read as "First draw red, probability 3 over 8"; leaves as "red then blue: 3/8 × 5/7".
- **Reduced motion** instant layout.
- **Modes added** `flip` mode, natural-frequency labels, loop leaves handing over to `first-step-solver` (P0, prob-stats 5).
- Drawn by `node-link`.

#### 5.5.11 `pascal-triangle`

composite · tier composite · cluster `precalc` · **P0** · size S · spec stage0 9.7 · first use 0.3 L99

Pascal's triangle.

- **Composes** `region-select`, `marks`, `numeric-input`, `stepper`.
- **Config** `PascalTriangleConfig { prefilled, mode, mod? }`.
- **Answers** `numeric`, `set`, `state`.
- **AI hooks** targets `cell:<n>-<k>`, `path`, `row:<n>`.
- **Accessibility** cells read as "row 4, position 2: 6".
- **Reduced motion** the path is drawn whole.
- **Modes added** row-to-PMF view, peg links to `galton-board`, Catalan highlight (P0, prob-stats 5).

#### 5.5.12 `trial-simulator`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 8.6 · first use 0.3 L106

Predict first, then run seeded trials: 10, 100, 1,000 or 10,000.

- **Composes** `sim-runner`, `chance-object`, `plot-2d`, `marks`, `value-table`, `numeric-input`.
- **Config** `TrialSimulatorConfig { kind, spec, event, filter?, batches, display, exact?, predictFirst?, seed }`.
- **Answers** `numeric`, `state`.
- **AI hooks** targets `run:<n>`, `trace`, `target:line`, `counts`; describe, e.g. "Two dice, keep at least one 5. Rolled 1,000, kept 309, total 10 in 27 (0.087). Exact 1/11 shown."
- **Accessibility** a counts table. Final counts are announced after each batch, never per frame.
- **Reduced motion** results appear at once.
- **Modes added** urn, permutation, birthday, coupon and pattern experiments; standard-error funnel; count-deviation trace (P0, prob-stats 5).
- Rebuilt on `sim-runner` and `chance-object` (prob-stats 5): the runner holds seed, runs and counts; the composite keeps display choices and the predict-first gate.

#### 5.5.13 `binomial-expander`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 9.8 · first use 0.3 L108

Expanding $(a + b)^n$ by choices.

- **Composes** `token-tray`, `card-sort`, `live-formula`, `area-model`, `graph-explorer`.
- **Config** `BinomialExpanderConfig { b, n, mode, target?, power, terms? }`.
- **Answers** `expression`, `numeric`, `mapping`, `state`.
- **AI hooks** targets `bracket:<i>`, `word:<id>`, `group:<k>`, `term:<k>`.
- **Accessibility** the `token-tray` model; terms described in words.
- **Reduced motion** instant.
- **Modes added** probability mode: terms of $(p + q)^n$ (P0, prob-stats 5).

#### 5.5.14 `outcome-grid`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 8.4 · first use 0.3 L112

Two-way sample spaces: two dice, a coin and a die, cards by suit and rank, two stocks up or down.

- **Composes** `cell-grid`, `region-select`, `live-formula`, `marks`, `stepper`, `value-table`.
- **Config** `OutcomeGridConfig { label, values, cols, display?, weights?, given?, shaded?, marked?, condition?, task, event? }`.
- **Answers** `set`, `numeric`, `choice`.
- **AI hooks** targets `cell:<r>,<c>`, `row:<r>`, `col:<c>`, `condition`; describe, e.g. "Two dice, 36 cells. Condition: at least one 5 (11 cells). Shaded: none. Display: pair."
- **Accessibility** as in the prototype: `role="grid"`, cells such as "First die 5, second die 3", and a live count.
- **Reduced motion** as in the prototype: no stagger, and static highlights that stay.
- **Modes added** non-uniform weights, event chips, random-variable display, list and layered layouts (P0, prob-stats 5).
- Renders through `cell-grid` and `region-select`.

#### 5.5.15 `stat-chart`

composite · tier composite · cluster `precalc` · **P0** · size M · spec stage0 8.2 · first use 0.3 L119

Build and read the standard charts.

- **Composes** `plot-2d`, `marks`, `drag-point`, `value-table`.
- **Config** `StatChartConfig { data, editable?, readings?, axes?, truncated? }`.
- **Answers** `numeric`, `state`, `point`, `set`.
- **AI hooks** targets `bar:<id>`, `bin:<lo>-<hi>`, `sector:<id>`, `reading:line`, `point:<k>`.
- **Accessibility** a table view is mandatory. Bars and sectors are sliders. The reading line announces its values.
- **Reduced motion** stepped.
- **Modes added** histogram bin-width slider and density scaling (P0, prob-stats 5).

#### 5.5.16 `induction-chain`

composite · tier composite · cluster `precalc` · **P0** · size S · spec stage0 9.6 · first use 0.3 L129

Proof by induction as falling dominoes.

- **Composes** `marks`, `derivation-steps`, `stepper`, `choice`.
- **Config** `InductionChainConfig { base, n, step, counterexample?, expr, firstFail }`.
- **Answers** `state`, `expression`, `numeric`, `parts`.
- **AI hooks** targets `domino:<n>`, `base`, `step:line-<k>`, `push`.
- **Accessibility** "Base case verified for n = 1; inductive step incomplete"; the derivation is accessible as in `derivation`.
- **Reduced motion** the dominoes show already fallen, with the failure gap marked.

### 5.6 Computer basics (0.4)

#### 5.6.1 `typing-trainer`

composite · tier composite · cluster `computing` · **P0** · size M · spec stage0 10.1 · first use 0.4 L1

Touch typing with home-row discipline.

- **Composes** `speed-timer`, `value-table`, `marks`; services `seeded-rng`.
- **Config** `TypingTrainerConfig { layout, durationS?, targetWpm, unlock?, wpm, accuracy, corpus?, os? }`.
- **Answers** `state`.
- **AI hooks** targets `key:<code>`, `text`, `stats`.
- **Accessibility** the current word is read aloud on request (Ctrl + Space) and after errors. The on-screen keyboard can be hidden. - Honest limit: the trainer is visual by design and is not a typing tutor for blind learners.
- **Reduced motion** the end statistics appear without counting up.

#### 5.6.2 `file-tree`

composite · tier composite · cluster `computing` · **P0** · size S · spec stage0 10.2 · first use 0.4 L9

Files and folders.

- **Composes** `token-tray`; services `vfs`.
- **Config** `FileTreeConfig { cwd?, task, showHidden?, pathStyle, ops }`.
- **Answers** `state`, `long-form`, `set`.
- **AI hooks** targets `node:<path>`, `pin`.
- **Accessibility** `role="tree"` with `aria-expanded`. Moves are announced: "Moved prices.csv into data".
- **Reduced motion** instant.
- Drawn by `node-link` in outline layout over the `vfs` service.

#### 5.6.3 `setup-checklist`

composite · tier composite · cluster `computing` · **P0** · size M · spec stage0 10.6, programming 6.11 · first use 0.4 L11

Guides real installs on the learner's own computer (Python, an editor, terminal basics) and verifies the outcomes without any access to that machine.

- **Composes** `code-surface`, `numeric-input`; services `python-runner`.
- **Config** `SetupChecklistConfig { id, title, os, body, verify?, command, pattern, hint, exitTask?, template, seed }`.
- **Answers** `state`, `long-form`, `code`.
- **AI hooks** targets `step:<id>`, `paste:<id>`, `verify:<id>`.
- **Accessibility** list semantics; statuses as text.
- **Reduced motion** instant.
- **Modes added** project mode verifying by pasted output; exit checks for 1.1, 1.2 and 1.9 (P0; C++ items P1, programming 6.11); 2.3 milestones, starter-suite download, metrics JSON (P2, finance 5); Project templates for the 2.1 capstone and the 3.1 replication: README sections, tests present, results note present (P2, ML 5).

#### 5.6.4 `shell-sim`

composite · tier composite · cluster `computing` · **P0** · size L · spec stage0 10.3, programming 6.10 · first use 0.4 L13

The terminal.

- **Composes** `text-terminal`, `file-tree`; services `vfs`, `python-runner`.
- **Config** `ShellSimConfig { cwd, commands, goal, kind, spec, tree?, python? }`.
- **Answers** `state`, `long-form`.
- **AI hooks** targets `input`, `line:<n>`, `node:<path>`.
- **Accessibility** `role="log"`, commands echoed, tree changes announced.
- **Reduced motion** a changed node gets a dot instead of a flash.
- **Modes added** job control, remote (`ssh`) and `awk` modes (P0, moved from P1; 1.2 L3, L8, curriculum).
- Programming 6.10 fixes the shell language and adds the 1.2 commands.

#### 5.6.5 `workspace-sim`

composite · tier composite · cluster `computing` · **P0** · size M · spec stage0 10.5, programming 6.9 · first use 0.4 L20

Rehearses the real workflow before the learner does it on their own machine.

- **Composes** `file-tree`, `code-cell`, `shell-sim`; services `vfs`.
- **Config** `WorkspaceSimConfig { goals, kind, args, python }`.
- **Answers** `state`, `code`.
- **AI hooks** targets `tree:`, `editor:`, `term:`, `code:cell`.
- **Accessibility** a landmark for each pane; F6 cycles them; saves and runs are announced.
- **Reduced motion** as the children.
- Three panes on one `vfs`: `file-tree`, `code-cell` (single file), `shell-sim`.

### 5.7 Python (1.1.1)

#### 5.7.1 `predict-output`

composite · tier composite · cluster `python` · **P0** · size M · spec programming 4.3 · first use 0.4 L22

"Act before you read" for code.

- **Composes** `code-surface`, `free-response`, `value-table`, `choice`, `diff-view`, `code-tracer`.
- **Config** `PredictOutputConfig { language, source, setup?, predict, recorded, trace?, compare? }`.
- **Answers** `output`, `resultset`, `set`, `choice`.
- **AI hooks** targets `line:<n>`, `pred:<n>`, `out:<n>`.
- **Accessibility** a labelled multi-line field; the reveal is announced ("Actual output has 3 lines; line 2 differs").
- **Reduced motion** cuts.

#### 5.7.2 `diagnostic-reader`

composite · tier composite · cluster `python` · **P0** · size M · spec programming 4.7 · first use 0.4 L23

Read error output: link each frame or diagnostic to its code, find the one that matters, say what it means.

- **Composes** `code-surface`, `region-select`, `choice`.
- **Config** `DiagnosticReaderConfig { format, report, code?, task, ownCode?, choices? }`.
- **Answers** `set`, `choice`, `mapping`.
- **AI hooks** targets `frame:<n>`, `diag:<n>`, `line:<path>:<n>`; describe, e.g. "Python traceback, 4 frames (2 in learner code). ZeroDivisionError: division by zero at analysis.py:12 in max_drawdown."
- **Accessibility** frames form a list ("frame 3 of 4: analysis.py, line 12, in max_drawdown"); the raw report stays available.
- **Reduced motion** the connector appears at once.
- **Modes added** mypy format (P0, 1.1 L54, curriculum).

#### 5.7.3 `code-tracer`

composite · tier composite · cluster `python` · **P0** · size L · spec programming 4.2 · first use 0.4 L24

Steps through code and shows the current line, the frames, the objects and the output.

- **Composes** `code-surface`, `stepper`, `node-link`, `text-terminal`, `value-table`; services `trace-recorder`.
- **Config** `CodeTracerConfig { language, source, trace?, live?, mode, checkpoints?, inlinePrimitives?, panels?, startAt?, showWhy? }`.
- **Answers** `mapping`, `output`, `numeric`, `set`, `ordering`, `choice`.
- **AI hooks** targets `line:<n>`, `frame:<fn>#<k>`, `var:<frame>.<name>`, `obj:<id>`, `slot:<obj>.<i>`, `out:<n>`, `step:<n>`, `bp:<line>`; describe, e.g. "Step 12 of 40, line 5. Frame f: n = 3, acc refers to o2. Output so far: '1', '2'."
- **Accessibility** a text alternative per step ("Frames: global: a refers to o1, b refers to o1. Objects: o1 list [1, 2]."); each step announced on commit; the watch list is a table.
- **Reduced motion** all cuts; the changed parts keep the "changed" underline for one step.
- **Modes added** `hits` mode expanding hidden built-in scans (P1, 1.8 sample, curriculum).

#### 5.7.4 `parsons`

composite · tier composite · cluster `python` · **P0** · size M · spec programming 4.4 · first use 0.4 L26

Put shuffled lines of code in order and at the right indentation, leaving out distractors.

- **Composes** `token-tray`, `code-surface`, `code-cell`.
- **Config** `ParsonsConfig { language, lines, distractors?, grading, indentation?, fixedLines?, adaptive? }`.
- **Answers** `ordering`.
- **AI hooks** targets `pline:<id>`, `slot:<n>`; describe, e.g. "Parsons: 5 of 7 lines placed. Order: L1, L3, L2, L4, L6. Indents: 0, 1, 1, 2, 1."
- **Accessibility** the solution is a list; each line reads "line 3 of 7, indent 2: total += x"; moves are announced.
- **Reduced motion** instant placement.
- Every `code-cell` drill derives a Parsons version for screens under 768 px (programming decision 15).

#### 5.7.5 `float-inspector`

composite · tier composite · cluster `python` · **P0** · size M · spec programming 4.8 · first use 1.1 L4

What a float really stores, and the consequences: binary fractions, the gap between neighbouring doubles, comparisons with tolerance, cancellation, summation order, NaN and infinity, and decimal arithmetic for money.

- **Composes** `array-strip`, `number-line`, `live-formula`, `slider`, `value-table`, `numeric-input`.
- **Config** `FloatInspectorConfig { mode, width?, value?, sum?, decimal?, locked? }`.
- **Answers** `numeric`, `choice`, `set`, `output`.
- **AI hooks** targets `bit:<i>`, `field:sign`, `field:exponent`, `field:mantissa`, `tick:<k>`; describe, e.g. "Double nearest 0.1 is 0.1000000000000000055511151231257827...; error 5.55e-18. Neighbours 0.09999999999999999 and 0.10000000000000002."
- **Accessibility** bits read as "bit 52, exponent, 1"; the value, its exact expansion and the error are text; the table view lists neighbours.
- **Reduced motion** nothing to change.

#### 5.7.6 `code-blanks`

composite · tier composite · cluster `python` · **P0** · size M · spec programming 4.5 · first use 1.1 L8

Complete code with gaps: type an expression, pick from a menu, or drag a token into the slot ("drag the right update into `lo = ...`").

- **Composes** `code-surface`, `token-tray`, `choice`, `code-cell`.
- **Config** `CodeBlanksConfig { language, template, slots, palette?, grading }`.
- **Answers** `mapping`, `code`.
- **AI hooks** targets `slot:<id>`, `token:<id>`, `line:<n>`; describe, e.g. "line 4: if ⟦a: lo <= hi⟧: ...; line 6: lo = ⟦b: empty⟧."
- **Accessibility** slots are labelled inputs or buttons ("blank 2 of 3, line 4").
- **Reduced motion** instant.

#### 5.7.7 `format-lab`

composite · tier composite · cluster `python` · **P0** · size S · spec programming 4.9 · first use 1.1 L9

Build format specifications and see the output change for several values at once: Python's format mini-language, `strftime` and `strptime` date codes, and `std::format`.

- **Composes** `token-tray`, `code-surface`, `value-table`, `numeric-input`.
- **Config** `FormatLabConfig { values, targets?, parts?, free? }`.
- **Answers** `output`.
- **AI hooks** targets `part:<name>`, `row:<i>`; describe, e.g. "Spec ',.2f'; outputs: 1,234,567.89 / -0.07 / nan."
- **Accessibility** outputs are a table; the spec is a labelled field.
- **Reduced motion** nothing to change.

#### 5.7.8 `pipeline-flow`

composite · tier composite · cluster `python` · **P0** · size M · spec programming 4.12 · first use 1.1 L29

Data moving through stages, with every connector inspectable: shell pipes (lines of text), Python iterator chains (lazy, one item at a time), the logical order of a SQL query (tables), pandas method chains (frames).

- **Composes** `token-tray`, `node-link`, `text-terminal`, `value-table`, `stepper`; services `shell-interpreter`, `sql-runner`, `frame-core`.
- **Config** `PipelineFlowConfig { mode, stages, palette?, input, intermediates?, task, predictAt?, goal? }`.
- **Answers** `ordering`, `output`, `resultset`, `state`.
- **AI hooks** targets `stage:<id>`, `pipe:<n>`; describe, e.g. "Shell pipeline: grep ERROR log.txt | cut -d, -f2 | sort | uniq -c. Stage 3 output: 14 lines."
- **Accessibility** stages form a list; each connector's content is reachable as text or a table; pulls are announced ("next() returned 4; filter skipped 3").
- **Reduced motion** items appear at their destination; reorders cut.
- **Modes added** scikit-learn pipeline mode showing leakage per stage (P2, ML 5).

#### 5.7.9 `json-explorer`

composite · tier composite · cluster `python` · **P0** · size S · spec programming 4.10 · first use 1.1 L41

Navigate nested dictionaries and lists (an API response, a config file).

- **Composes** `node-link`, `code-surface`, `value-table`.
- **Config** `JsonExplorerConfig { source, task, target? }`.
- **Answers** `output`, `set`, `choice`.
- **AI hooks** targets `node:<path>`; describe, e.g. "JSON object, 3 top-level keys; selected data['quotes'][0]['bid'] = 101.25."
- **Accessibility** a `tree` with `aria-expanded`; each node reads "key bid, float, 101.25, path data, quotes, 0, bid".
- **Reduced motion** instant.
- **Modes added** feed-message presets (P2, finance 5).

#### 5.7.10 `regex-lab`

composite · tier composite · cluster `python` · **P0** · size M · spec programming 4.13 · first use 1.1 L43

Regular expressions with live highlighting over test strings: match all the positives and none of the negatives, capture groups, greedy against lazy, anchors and flags.

- **Composes** `code-surface`, `value-table`, `region-select`, `token-tray`, `array-strip`.
- **Config** `RegexLabConfig { flavour?, positives, negatives?, groups?, files?, pattern? }`.
- **Answers** `output`, `set`, `choice`.
- **AI hooks** targets `ptok:<i>`, `str:<i>`, `group:<n>`; describe, e.g. "Pattern `^[A-Z]{1,5}$`, flags none; matches 7 of 8 positives (misses 'BRK.B'), 0 of 6 negatives."
- **Accessibility** each string reads "matches, group 1 '2024', group 2 '03'" or "no match"; explanations are a list.
- **Reduced motion** nothing to change.

#### 5.7.11 `search-path`

composite · tier composite · cluster `python` · **P0** · size S · spec programming 4.11 · first use 1.1 L45

Ordered search where the first match wins: `PATH` for commands and `sys.path` for imports.

- **Composes** `token-tray`, `node-link`, `text-terminal`.
- **Config** `SearchPathConfig { dirs, path, contents, kind?, query?, goal?, name, mustResolveTo }`.
- **Answers** `choice`, `set`, `ordering`, `state`.
- **AI hooks** targets `dir:<path>`, `file:<path>`; describe, e.g. "PATH order: .venv/bin, /usr/local/bin, /usr/bin. venv active. python3 resolves to .venv/bin/python3."
- **Accessibility** the list is ordered and announced ("python3 found in /home/you/project/.venv/bin, the first of 5 directories").
- **Reduced motion** the result appears with the checked directories marked.

#### 5.7.12 `code-annotator`

composite · tier composite · cluster `python` · **P0** · size M · spec programming 4.6 · first use 1.1 L48

The owner's code-craft format as an interactive worked example: code notes with complexity, inline rationale on non-obvious lines, the senior-developer paragraph and the plain-English translation.

- **Composes** `code-surface`, `slider`, `token-tray`, `live-formula`, `region-select`.
- **Config** `CodeAnnotatorConfig { language, source, notes, inline, seniorDev, restatement?, blocks, segments?, tokens?, depth?, exercise? }`.
- **Answers** `mapping`, `set`, `choice`.
- **AI hooks** targets `block:<id>`, `line:<n>`, `tok:<l>:<c>`; describe, e.g. "Annotated solution, depth 3, 4 blocks; block 2 open."
- **Accessibility** all text; the depth slider is a native range labelled "Depth 3: block by block".
- **Reduced motion** instant.

### 5.8 NumPy, pandas and plotting (1.1.2 to 1.1.4)

#### 5.8.1 `bench-lab`

composite · tier composite · cluster `data` · **P0** · size M · spec programming 5.11 · first use 1.1 L28

Measuring speed honestly: races between implementations, then methodology (warm-up, repeats, spread, optimisation levels, dead-code elimination), the Python against C++ comparison for the 1.9 exit, and profiles.

- **Composes** `plot-2d`, `marks`, `value-table`, `code-surface`; mark types `icicle`.
- **Config** `BenchLabConfig { impls, id, label, code, language, sizes?, recorded?, device, times, profile?, paste?, format }`.
- **Answers** `numeric`, `choice`, `set`.
- **AI hooks** targets `impl:<id>`, `point:<impl>.<n>`, `frame:<fn>`; describe, e.g. "Race: loop vs vectorised at n = 10^6: 410 ms vs 3.1 ms (132×), web Pyodide."
- **Accessibility** table view of size, implementation and time; the speed-up announced.
- **Reduced motion** results appear together when the run ends.
- **Modes added** denormals (P1, 1.9, curriculum).
- Race mode P0; rigorous and profile modes P1; 1.1 L68 shows a build-time profile in `value-table`.

#### 5.8.2 `csv-inspector`

composite · tier composite · cluster `data` · **P0** · size M · spec programming 5.8 · first use 1.1 L40

The raw text of a CSV beside the table it becomes, with every option that changes the parse: quoted commas, headers, index columns, dates, thousands and decimal separators, missing-value strings, skipped rows, encodings.

- **Composes** `code-surface`, `value-table`, `token-tray`, `code-blanks`.
- **Config** `CsvInspectorConfig { text, generator, seed, messiness, options?, task }`.
- **Answers** `set`, `code`, `mapping`, `choice`.
- **AI hooks** targets `raw:<line>:<col>`, `cell:<r>,<c>`, `opt:<name>`; describe, e.g. "CSV 8 lines; options sep=',' header=0; column volume parsed as object (thousands separators)."
- **Accessibility** the raw text is real text; each cell names its source line and column.
- **Reduced motion** nothing to change.

#### 5.8.3 `time-series-lab`

composite · tier composite · cluster `data` · **P0** · size M · spec programming 5.7 · first use 1.1 L42

pandas time series on a real timeline: dates and frequencies, `shift` and returns, resampling and its labelling rules, rolling and exponentially weighted windows, time zones and daylight saving, and aligning two calendars.

- **Composes** `plot-2d`, `marks`, `value-table`, `region-select`, `slider`; mark types `band`; services `frame-core`, `price-series`.
- **Config** `TimeSeriesLabConfig { series, generator, seed, days, task, pandasVersion }`.
- **Answers** `set`, `numeric`, `mapping`, `output`.
- **AI hooks** targets `row:<date>`, `window`, `bin:<n>`; describe, e.g. "Daily prices 2024-01-02 to 2024-03-28 (61 trading days). shift(-1) applied: 61 returns use the next day's price."
- **Accessibility** a table view with date, price, shifted price, return; window positions announced as date ranges.
- **Reduced motion** shifts cut.
- **Modes added** irregular tick data from `market-gen` (P2, finance 5); Alignment trap: a centred rolling window is flagged as using future rows; `shift` direction shown as arrows (P2, ML 5).

#### 5.8.4 `ndarray-lab`

composite · tier composite · cluster `data` · **P0** · size M · spec programming 5.1 · first use 1.1 L56

NumPy arrays as cells you can see: shape and axes, slicing, views against copies, strides and memory order, boolean masks and fancy indexing, dtypes, reductions and stacking.

- **Composes** `cell-grid`, `array-strip`, `drag-point`, `slider`, `token-tray`, `live-formula`, `code-surface`.
- **Config** `NdarrayLabConfig { mode, arrays, expr?, target?, editable?, showBuffer?, showStrides? }`.
- **Answers** `output`, `set`, `choice`, `numeric`, `expression`.
- **AI hooks** targets `cell:<r>,<c>`, `axis:<k>`, `buf:<i>`, `view:<id>`; describe, e.g. "int64 array, shape (3, 4). Selection a[1:, ::2]: 4 cells, a view of a (shares memory)."; tryable `view:<id>`.
- **Accessibility** the grid's cell reads include indices and buffer offset; the expression and its result shape are announced.
- **Reduced motion** before and after with Play.

#### 5.8.5 `broadcast-lab`

composite · tier composite · cluster `data` · **P0** · size S · spec programming 5.2 · first use 1.1 L62

Broadcasting as a picture: shapes aligned from the right, size-1 dimensions stretched, the result shape, and the error when two dimensions disagree.

- **Composes** `token-tray`, `cell-grid`, `live-formula`, `code-surface`, `choice`.
- **Config** `BroadcastLabConfig { operands, name, shape, values?, op, task }`.
- **Answers** `output`, `choice`, `code`, `mapping`.
- **AI hooks** targets `dim:<operand>.<k>`, `result`; describe, e.g. "(3, 4) + (3,): aligned from the right, 4 against 3 mismatch."
- **Accessibility** alignment read column by column ("from the right: 4 and 4 match; 3 and 1 stretch to 3").
- **Reduced motion** before and after.

#### 5.8.6 `dataframe-lab`

composite · tier composite · cluster `data` · **P0** · size M · spec programming 5.3 · first use 1.1 L76

pandas DataFrames: anatomy, selection with `[]`, `loc` and `iloc`, boolean filters, index alignment, missing data, chained assignment under copy-on-write, sorting and ranking, dtypes and memory, MultiIndex.

- **Composes** `value-table`, `code-surface`, `token-tray`; services `frame-core`.
- **Config** `DataframeLabConfig { frames, expr?, target?, allowed?, pandasVersion }`.
- **Answers** `output`, `set`, `numeric`, `choice`.
- **AI hooks** targets `cell:<row>,<col>`, `row:<label>`, `col:<name>`; describe, e.g. "Frame prices 6 × 3 (date index). Learner selection rows 2024-01-03 to 2024-01-05, column close. Expression df.iloc[2:4, 0] selects 2 rows."
- **Accessibility** frame-mode table semantics; selections announced ("loc selects 3 rows, 1 column").
- **Reduced motion** the result appears at once.

#### 5.8.7 `groupby-lab`

composite · tier composite · cluster `data` · **P0** · size M · spec programming 5.4 · first use 1.1 L86

Split, apply, combine, shown as motion: rows sorted into groups, each group reduced, the results gathered.

- **Composes** `value-table`, `token-tray`, `stepper`, `code-surface`.
- **Config** `GroupbyLabConfig { frame, keys?, aggs?, dialect, task, dropna? }`.
- **Answers** `mapping`, `resultset`, `numeric`, `code`.
- **AI hooks** targets `row:<i>`, `group:<key>`, `agg:<key>.<col>`; describe, e.g. "Group by sector, sum of value. Stage apply. 3 groups: Energy 2 rows, Tech 3 rows, Banks 2 rows."
- **Accessibility** groups read as lists ("group Tech: 3 rows, sum 412"); windows read per row ("row 5: partition AAPL, frame rows 1 to 5").
- **Reduced motion** each stage shown as a static state with Play.
- **Modes added** Cross-sectional mode: rank, z-score and `qcut` within each date (P2, ML 5).

#### 5.8.8 `join-lab`

composite · tier composite · cluster `data` · **P0** · size M · spec programming 5.5 · first use 1.1 L87

Joins as matched rows, not Venn diagrams: lines join rows with equal keys, duplicate keys fan out and multiply rows, unmatched rows are kept or dropped by the join type, and missing values pad the gaps.

- **Composes** `value-table`, `marks`, `token-tray`, `code-surface`.
- **Config** `JoinLabConfig { left, right, on, how?, dialect, task }`.
- **Answers** `numeric`, `set`, `mapping`, `resultset`, `code`.
- **AI hooks** targets `lrow:<i>`, `rrow:<i>`, `res:<i>`, `match:<i>-<j>`; describe, e.g. "Left 5 rows, right 4 rows, inner join on ticker. Duplicate key MSFT on the right (2 rows). Learner predicted 5 rows."
- **Accessibility** matches listed as text ("left row 2 (AAPL) matches right rows 1 and 4").
- **Reduced motion** the result appears at once.
- **Modes added** `asof` join (P0, 1.1 L88, curriculum).

#### 5.8.9 `reshape-lab`

composite · tier composite · cluster `data` · **P0** · size S · spec programming 5.6 · first use 1.1 L90

Long and wide data: `pivot`, `pivot_table` (with an aggregation when keys repeat), `melt`, `stack` and `unstack` with MultiIndex levels, `get_dummies` and `crosstab`.

- **Composes** `value-table`, `token-tray`, `marks`, `stepper`.
- **Config** `ReshapeLabConfig { frame, task, target? }`.
- **Answers** `mapping`, `output`, `code`, `choice`.
- **AI hooks** targets `slot:<name>`, `src:<r>,<c>`, `dst:<r>,<c>`; describe, e.g. "melt with id_vars [date], value_vars [AAPL, MSFT]; result 10 rows × 3 columns."
- **Accessibility** "Cell (2024-01-02, AAPL, close) moves to row 2024-01-02, column AAPL."
- **Reduced motion** before and after, with the followed cell ringed in both.

#### 5.8.10 `drawdown-lab`

composite · tier composite · cluster `data` · **P0** · size M · spec programming 5.9 · first use 1.1 L97

The 1.1 exit maths on a price path: simple and log returns, annualised volatility, the running maximum, the drawdown series and the maximum drawdown with its dates.

- **Composes** `plot-2d`, `marks`, `drag-point`, `region-select`, `live-formula`, `value-table`.
- **Config** `DrawdownLabConfig { series, generator, seed, days, drawdowns?, dates?, task }`.
- **Answers** `point`, `numeric`, `choice`.
- **AI hooks** targets `handle:peak`, `handle:trough`, `panel:price`, `panel:dd`; describe, e.g. "Price path 252 days. Learner peak 2024-03-14 (131.2), trough 2024-05-02 (112.9): fall -13.9%."
- **Accessibility** handles are sliders over trading days ("peak 14 March 2024, 131.20"); the table view lists date, price, running maximum and drawdown.
- **Reduced motion** ghosts appear in place.
- **Modes added** compare mode with Sharpe, Sortino, Calmar and rolling Sharpe (P2, finance 5); Accepts a return series bound from another widget (section 2.1 requirement 4) (P2, ML 5).
- Shared with finance; carries the 1.1 exit maths.

#### 5.8.11 `plot-workbench`

composite · tier composite · cluster `data` · **P0** · size M · spec programming 5.10 · first use 1.1 L99

matplotlib's model (Figure, Axes, Artists) and plotting judgement.

- **Composes** `code-surface`, `token-tray`, `code-blanks`, `choice`, `value-table`.
- **Config** `PlotWorkbenchConfig { code, svg?, artists?, gid, line, kind, data?, toggles?, id, label, options, fixTarget? }`.
- **Answers** `mapping`, `state`, `code`, `choice`.
- **AI hooks** targets `artist:<gid>`, `line:<n>`; describe, e.g. "Figure with 2 axes; axes 1 has 1 line, no y label; axes 2 is a histogram with 40 bins."
- **Accessibility** alt text from the artist list ("Axes 1: line 'close'; x label 'Date'; y label 'Price (USD)'; log scale"); each artist is listed as a button linked to its line.
- **Reduced motion** nothing to change.
- matplotlib's own SVG with artist ids, recorded at build time.

### 5.9 Tools (1.2)

#### 5.9.1 `permission-bits`

composite · tier composite · cluster `tools` · **P0** · size S · spec programming 6.4 · first use 1.2 L5

Unix permissions as a $3 \times 3$ grid of read, write and execute for owner, group and others, with the octal digits, the `ls -l` string and symbolic `chmod` kept in step.

- **Composes** `region-select`, `live-formula`, `text-terminal`.
- **Config** `PermissionBitsConfig { target?, kind, scenario?, umask? }`.
- **Answers** `output`, `state`.
- **AI hooks** targets `bit:<who>.<perm>`; describe, e.g. "Mode 640 (rw-r-----), file report.sh; scenario: not executable."
- **Accessibility** each cell is a toggle ("group, write, off"); the mode is announced as "750, rwxr-x---".
- **Reduced motion** nothing to change.

#### 5.9.2 `git-graph`

composite · tier composite · cluster `tools` · **P0** · size L · spec programming 6.1 · first use 1.2 L9

Git as a picture you can operate: the commit graph with branch labels and HEAD, the three trees (working directory, index, HEAD), a remote, and the goal graph of a puzzle drawn as a ghost.

- **Composes** `node-link`, `diff-view`, `text-terminal`, `token-tray`, `value-table`; services `git-model`, `vfs`.
- **Config** `GitGraphConfig { repo, remote?, goal?, panels?, input, allowed?, checks?, bisect? }`.
- **Answers** `state`, `output`, `numeric`, `ordering`.
- **AI hooks** targets `commit:<hash>`, `ref:<name>`, `file:<tree>:<path>`, `cmd`; describe, e.g. "Repo: 7 commits; main at c4, feature at c6 (HEAD). Staged: report.py. Modified: analysis.py. Goal: feature rebased on main, par 2."
- **Accessibility** a log table (hash, message, parents, refs); every command's effect announced ("main moved from c4 to c5; working tree unchanged").
- **Reduced motion** cuts, with the moved labels marked "moved" for one step.
- Over the `git-model` service: blobs, trees, commits, refs, index and reflog with SHA-1 over a deterministic clock.

#### 5.9.3 `merge-conflict`

composite · tier composite · cluster `tools` · **P0** · size M · spec programming 6.2 · first use 1.2 L14

Resolve a conflict in a three-way view, then run the tests, because a clean textual merge can still be wrong.

- **Composes** `diff-view`, `code-surface`, `code-cell`; services `git-model`.
- **Config** `MergeConflictConfig { ours, theirs, language, suite?, markers?, task }`.
- **Answers** `code`, `state`, `set`.
- **AI hooks** targets `hunk:<n>`, `line:<n>`, `test:<k>`; describe, e.g. "2 conflict hunks; hunk 1 resolved (ours), hunk 2 open. Tests not run."
- **Accessibility** hunks as a list with their choices; markers read as "start of our version".
- **Reduced motion** instant.

#### 5.9.4 `code-review`

composite · tier composite · cluster `tools` · **P0** · size M · spec programming 6.3 · first use 1.2 L17

A pull request to review: the description, commits, changed files and checks.

- **Composes** `diff-view`, `choice`, `free-response`, `value-table`.
- **Config** `CodeReviewConfig { description, files, path, before, after, checks?, defects, id, file, lines, tag, mustFind, explain }`.
- **Answers** `set`, `choice`, `output`.
- **AI hooks** targets `file:<path>`, `line:<path>:<n>`, `comment:<k>`; describe, e.g. "PR 'Add drawdown', 2 files, 41 changed lines; learner flagged 2 lines (bug, naming); decision none."
- **Accessibility** comments listed with file and line; defects explained in text after grading.
- **Reduced motion** nothing to change.

#### 5.9.5 `mutant-hunter`

composite · tier composite · cluster `tools` · **P0** · size L · spec programming 6.6 · first use 1.2 L19

Learn testing by killing bugs.

- **Composes** `code-cell`, `code-surface`, `diff-view`, `value-table`; services `mutant-forge`, `python-runner`.
- **Config** `MutantHunterConfig { signature, reference, mutants, show, starterTests?, needs?, coverage?, property? }`.
- **Answers** `code`.
- **AI hooks** targets `mutant:<id>`, `test:<name>`, `line:<n>`; describe, e.g. "6 mutants: 4 killed, 2 alive (kinds: boundary, tolerance). Reference passes. Learner has 5 tests."
- **Accessibility** the board is a table; results announced ("4 of 6 mutants killed; reference passes").
- **Reduced motion** the state changes without the flip.
- **Modes added** property mode (P0, moved from P1; 1.2 L24, curriculum); coverage overlay (P1, programming 6.6); C++ mutants (P1, 1.9, curriculum).

#### 5.9.6 `injection-lab`

composite · tier composite · cluster `tools` · **P0** · size M · spec programming 6.5 · first use 1.2 L32

Why data must never become code.

- **Composes** `code-surface`, `token-tray`; services `code-lex`, `sql-runner`.
- **Config** `InjectionLabConfig { template, context, db?, schema, rows, task }`.
- **Answers** `output`, `choice`, `code`.
- **AI hooks** targets `tok:<i>`, `input`, `method`; describe, e.g. "SQL, string context, concatenation. Input \".
- **Accessibility** the token list is text ("keyword OR, from input"); the banner is announced.
- **Reduced motion** nothing to change.

#### 5.9.7 `schema-builder`

composite · tier composite · cluster `tools` · **P2** · size M · spec programming 6.7 · first use 2.3 L204

Design tables from one wide sheet: split columns into tables, pick primary keys, draw foreign keys, and see the update anomalies that normalisation removes.

- **Composes** `token-tray`, `node-link`, `value-table`, `code-surface`.
- **Config** `SchemaBuilderConfig { dependencies, target? }`.
- **Answers** `state`, `code`.
- **AI hooks** targets `table:<name>`, `col:<table>.<name>`, `fk:<k>`; describe, e.g. "3 tables: trades(id, instrument_id, qty, price), instruments(id, symbol, company), ... FK trades.instrument_id to instruments.id."
- **Accessibility** tables listed as text with their keys and foreign keys; anomalies announced in words.
- **Reduced motion** instant placement; the anomaly shows before and after.
- **Modes added** time-partitioned trades and candles tables (P2, finance 5).
- No longer used in 1.2 (python-tools decision 19); first use 2.3 L204.

### 5.10 Calculus (1.3)

#### 5.10.1 `series-explorer`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.17 · first use 0.3 L63

Series as partial sums: convergence and divergence; geometric series; the integral, comparison, ratio and alternating tests; power series at a chosen $x$ and the radius of convergence.

- **Composes** `plot-2d`, `marks`, `slider`, `number-line`, `drag-point`, `value-table`, `live-formula`, `numeric-input`, `choice`.
- **Config** `SeriesExplorerConfig { start, mode, NRange, x?, range, init, limit?, compareTo? }`.
- **Answers** `numeric`, `choice`, `interval`, `point`.
- **AI hooks** targets `slider:N`, `bar:<n>`, `sum:<N>`, `limit`, `tail`, `handle:x`, `interval`, `overlay:integral`; tryable `slider:N`.
- **Accessibility** Table of $N$ and partial sums.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** Fourier mode (P0, 1.4 L53, curriculum); annuity and perpetuity presets linked to `cashflow-timeline` (P1, finance 5).
- First used at 0.3 L63 (geometric series), so it ships with Stage 0; owns partial sums for `sequence-lab` and `sum-visualiser`.

#### 5.10.2 `limit-explorer`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.1 · first use 0.3 L142

Approach a point from each side and read what the function approaches.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `value-table`, `numeric-input`, `live-formula`.
- **Config** `LimitExplorerConfig { f?, pieces?, a, mode, valueAt?, null, view, closeness?, autoZoom?, sides?, bounds?, table? }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `handle:left`, `handle:right`, `slider:h`, `hole`, `dot:value`, `guide:left`, `guide:right`, `curve:f`, `bound:<id>`, `row:<i>`; describe, e.g. "f(x) = (x^2 − 4)/(x − 2), a = 2, hole at x = 2. Left handle x = 1.9 (f = 3.9), right handle x = 2.1 (f = 4.1). Answer field: DNE."; tryable `slider:h`.
- **Accessibility** The value table is the primary alternative; handle text reads "x = 1.99, f(x) = 3.99".
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- First used at 0.3 L142 (precalc limits), so it ships with Stage 0.

#### 5.10.3 `secant-tangent`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.4 · first use 1.3 L1

Average rate of change becomes instantaneous: the slope of secant $PQ$ as $Q\to P$.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `value-table`, `live-formula`, `numeric-input`, `expression-input`.
- **Config** `SecantTangentConfig { curve, P, Q?, h?, mode, showTangent, braces?, table? }`.
- **Answers** `numeric`, `expression`, `choice`, `state`, `point`.
- **AI hooks** targets `handle:P`, `handle:Q`, `handle:Qm`, `handle:C`, `slider:h`, `line:secant`, `line:tangent`, `brace:rise`, `brace:run`, `ruler:tower`, `readout:radar`, `row:<i>`; tryable `slider:h`.
- **Accessibility** Table of $h$ against slope; "Secant through P(1, 1) and Q(1.5, 2.25): slope 2.5."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** motion preset with tower, ruler and time scrubber; signed stops excluding 0; centred-window mode with `handle:Qm`; switching position functions (P0, 1.3 L1, curriculum: lesson 1 cannot be built without them).

#### 5.10.4 `epsilon-delta`

composite · tier composite · cluster `calculus` · **P0** · size S · spec calc-linalg 5.2 · first use 1.3 L4

Make the formal definition a game.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `live-formula`, `expression-input`.
- **Config** `EpsilonDeltaConfig { f, a, L, mode, eps, deltaRange, liveEscape, askFormula? }`.
- **Answers** `choice`, `state`, `point`.
- **AI hooks** targets `handle:delta`, `band:eps`, `strip:delta`, `escape:<i>`, `field:formula`.
- **Accessibility** Describes escape points: "With δ = 0.3, f leaves the band at x = 2.27, where f = 5.15, above L + ε = 5.1."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.10.5 `local-zoom`

composite · tier composite · cluster `calculus` · **P0** · size S · spec calc-linalg 5.3 · first use 1.3 L9

Zoom into a point on a curve until it looks straight (differentiable), or does not (corner, cusp, oscillation, Brownian path).

- **Composes** `plot-2d`, `drag-point`, `slider`, `marks`, `live-formula`.
- **Config** `LocalZoomConfig { f, g?, x0, movable, magRange, showTangent, measure?, path? }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `handle:centre`, `slider:mag`, `inset`, `tangent`, `slope:left`, `slope:right`, `curve:f`, `curve:g`; tryable `slider:mag`.
- **Accessibility** "At ×1,000 around x = 0, |x| still shows a corner: slope −1 on the left, +1 on the right."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- Brownian mode is P2.

#### 5.10.6 `derivative-tracer`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.5 · first use 1.3 L10

Link $f$, $f'$ and $f''$.

- **Composes** `plot-2d`, `marks`, `drag-point`, `sketch-pad`, `slider`, `live-formula`, `choice`.
- **Config** `DerivativeTracerConfig { f, domain, params?, panels, mode, reveal, anchor?, concavityBands? }`.
- **Answers** `curve`, `point`, `choice`, `expression`, `interval`.
- **AI hooks** targets `handle:x`, `tangent`, `trace`, `curve:f`, `curve:df`, `curve:d2f`, `sketch`, `feature:<i>`, `band:<i>`, `slider:<param>`; tryable `slider:<param>`.
- **Accessibility** Table of $x$, $f(x)$, $f'(x)$ at sample points; sketches described in words.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.10.7 `growth-rectangle`

composite · tier composite · cluster `calculus` · **P0** · size S · spec calc-linalg 5.6 · first use 1.3 L11

Derive derivative rules from growth.

- **Composes** `plot-2d`, `plot-3d`, `drag-point`, `slider`, `marks`, `token-tray`, `live-formula`.
- **Config** `GrowthRectangleConfig { f?, g?, x, dxRange, labelTokens?, ratioReadout? }`.
- **Answers** `set`, `numeric`, `expression`.
- **AI hooks** targets `handle:corner`, `slider:dx`, `strip:1`, `strip:2`, `corner`, `slot:<i>`, `readout:ratio`; tryable `slider:dx`.
- **Accessibility** Areas described numerically, for example "strips 2 × 3 × 0.1 = 0.6, corner 0.01".
- **Reduced motion** A three-row table ($dx = 0.5$, $0.05$, $0.005$) replaces the tween.

#### 5.10.8 `function-mapping`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.7 · first use 1.3 L15

Functions as maps between number lines.

- **Composes** `number-line`, `marks`, `drag-point`, `slider`, `live-formula`.
- **Config** `FunctionMappingConfig { maps, lines, mode, x, dxRange, gridPoints?, integrand? }`.
- **Answers** `numeric`, `expression`, `choice`.
- **AI hooks** targets `handle:x`, `slider:dx`, `band:<variable>`, `factor:<map>`, `line:<variable>`; tryable `slider:dx`.
- **Accessibility** "x = 1.2 → u = 1.44 → y = 0.99. A step dx = 0.01 becomes du = 0.024 (×2.4), then dy = 0.0041 (×0.17). Overall ×0.41, the derivative."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** density mode: interval images conserve mass (P0, prob-stats 5).

#### 5.10.9 `rates-scene`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.9 · first use 1.3 L24

Related rates in a physical scene: a ladder sliding down a wall, a cone filling, a ripple spreading, two cars, a lengthening shadow.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `live-formula`, `numeric-input`, `expression-input`.
- **Config** `RatesSceneConfig { relation, scene, driver, var, rate, units, rates, arrowAt, askAt? }`.
- **Answers** `numeric`, `expression`, `choice`.
- **AI hooks** targets `handle:driver`, `slider:t`, `arrow:<var>`, `shape:<id>`; tryable `slider:t`.
- **Accessibility** The scene described with numbers and units.
- **Reduced motion** Play steps at four frames per second.

#### 5.10.10 `taylor-builder`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.18 · first use 1.3 L32

Build Taylor polynomials by matching value, slope and curvature at a centre; see the error and the remainder bound; find the radius of convergence; apply it to bonds (duration and convexity) and options (delta and gamma).

- **Composes** `plot-2d`, `drag-point`, `slider`, `marks`, `live-formula`, `value-table`, `numeric-input`, `expression-input`.
- **Config** `TaylorBuilderConfig { centre, movableCentre, degree, maxDegree, mode, coefficientRanges?, errorBand?, radius?, preset? }`.
- **Answers** `numeric`, `expression`, `point`, `choice`.
- **AI hooks** targets `handle:centre`, `slider:degree`, `coef:<k>`, `curve:f`, `curve:T`, `error`, `radius`, `handle:delta`; tryable `slider:degree`.
- **Accessibility** Table of $x$, $f(x)$, $T_n(x)$ and error; the polynomial read as text.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** bond preset with a stated compounding convention (P0, 1.3, curriculum); MGF series (P0) and delta-method mode (P1, prob-stats 5).

#### 5.10.11 `root-finder`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.8 · first use 1.3 L33

Algorithms that find zeros.

- **Composes** `plot-2d`, `marks`, `drag-point`, `stepper`, `value-table`, `live-formula`, `numeric-input`, `choice`.
- **Config** `RootFinderConfig { method, x0?, bracket?, maxSteps, predict?, errorPlot? }`.
- **Answers** `point`, `numeric`, `choice`.
- **AI hooks** targets `handle:x0`, `handle:lo`, `handle:hi`, `iterate:<n>`, `tangent:<n>`, `bracket:<n>`, `row:<n>`, `marker:predict`.
- **Accessibility** The table ($n$, $x_n$, $f(x_n)$, error) is primary.
- **Reduced motion** Steps appear at once.

#### 5.10.12 `objective-explorer`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.10 · first use 1.3 L35

Optimise one variable in context.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `live-formula`, `numeric-input`, `expression-input`, `sign-chart`.
- **Config** `ObjectiveExplorerConfig { x, var, range, init, objective, expr, label, units?, showCurve, preset? }`.
- **Answers** `point`, `numeric`, `expression`, `choice`.
- **AI hooks** targets `handle:x`, `scene:<shape>`, `curve:objective`, `marker:best`, `point:optimum`.
- **Accessibility** Table of $x$ against the objective.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** likelihood mode (P0, 1.3 L47, curriculum).

#### 5.10.13 `convexity-chord`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.12 · first use 1.3 L50

Convex and concave functions through chords and tangents; Jensen's inequality, $E[f(X)]\ge f(E[X])$ for convex $f$; the start of the intuition behind volatility drag and option convexity.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `live-formula`, `choice`.
- **Config** `ConvexityChordConfig { domain, mode, points, weights? }`.
- **Answers** `choice`, `numeric`, `state`, `interval`, `curve`.
- **AI hooks** targets `handle:x1`, `handle:x2`, `handle:lambda`, `chord`, `tangent`, `gap`, `atom:<i>`, `point:Ef`, `point:fE`.
- **Accessibility** "The chord lies above the curve everywhere between 1 and 3; at λ = 0.5 the gap is 0.25."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** random-variable mode with the Jensen gap (P0, prob-stats 5); volatility-drag preset (P1) and Kelly growth preset (P2, finance 5).

#### 5.10.14 `descent-lab`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.21 · first use 1.3 L53

Gradient descent on a contour map: the learning rate, divergence, zig-zagging in narrow valleys, and the link between convergence and the eigenvalues of the Hessian.

- **Composes** `plot-2d`, `drag-point`, `slider`, `stepper`, `marks`, `value-table`, `numeric-input`, `choice`.
- **Config** `DescentLabConfig { start, movableStart, eta, etaRange, method, steps, showLoss, noise?, seed, scale }`.
- **Answers** `numeric`, `choice`, `point`.
- **AI hooks** targets `handle:start`, `slider:eta`, `iterate:<k>`, `path`, `plot:loss`, `marker:predict`; tryable `slider:eta`.
- **Accessibility** Table of $k$, $\mathbf x_k$ and $f(\mathbf x_k)$.
- **Reduced motion** Run shows all iterates at once.
- **Modes added** stochastic mode (P2, 2.1 L19, curriculum); RMSProp and Adam beside the existing momentum and SGD modes; a race of four optimisers from one start (P2, ML 5).
- Newton mode P1; momentum and stochastic modes P2.

#### 5.10.15 `riemann-sum`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.13 · first use 1.3 L54

Area by rectangles: left, right, midpoint, upper and lower sums, trapezoids and Simpson's rule; signed area; area between curves; average value; error against $n$.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `choice`, `value-table`, `live-formula`.
- **Config** `RiemannSumConfig { f, g?, a, b, movableEnds, n, nValues?, rules, showExact, errorInset?, signed?, averageMode? }`.
- **Answers** `numeric`, `choice`, `point`.
- **AI hooks** targets `handle:a`, `handle:b`, `slider:n`, `rule:<r>`, `bar:<i>`, `gap:<i>`, `curve:f`, `readout:sum`, `inset:error`, `handle:level`; tryable `slider:n`, `rule:<r>`.
- **Accessibility** Table of $i$, $x_i^*$, $f(x_i^*)$, area of bar $i$, and the total.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.10.16 `accumulator`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.14 · first use 1.3 L56

The accumulation function $A(x)=\int_a^x f(t)\,dt$ linked to $f$: area so far, the fundamental theorem ($A'=f$), families of antiderivatives ($+C$), improper integrals by pushing the upper limit to infinity, densities and CDFs.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `sketch-pad`, `live-formula`, `numeric-input`, `expression-input`.
- **Config** `AccumulatorConfig { a, movableA, x, domain, mode, reveal, closedForm? }`.
- **Answers** `numeric`, `curve`, `choice`, `expression`.
- **AI hooks** targets `handle:x`, `handle:a`, `region`, `curve:f`, `curve:A`, `tangent:A`, `panel:convergence`.
- **Accessibility** Table of $x$ against $A(x)$.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** PDF-to-CDF mode on the `dist` service (P0, prob-stats 5).

#### 5.10.17 `slope-field`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.15 · first use 1.3 L60

First-order differential equations $y'=F(x,y)$: direction fields, solution curves through chosen points, Euler's method and its error, equilibria.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `stepper`, `value-table`, `sketch-pad`, `choice`.
- **Config** `SlopeFieldConfig { view, arrowsPerSide, ic?, movableIc, euler?, h, steps, predict?, exact?, params? }`.
- **Answers** `point`, `numeric`, `curve`, `choice`, `expression`.
- **AI hooks** targets `handle:ic`, `solution`, `euler:<k>`, `field`, `slider:h`, `marker:predict`; tryable `slider:h`.
- **Accessibility** Qualitative description computed from the field: equilibria and their stability ("y = 0 unstable, y = 1 stable").
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.10.18 `solid-of-revolution`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.16 · first use 1.3 L77

Volumes of revolution by discs, washers and shells.

- **Composes** `plot-2d`, `plot-3d`, `drag-point`, `slider`, `choice`, `marks`, `live-formula`.
- **Config** `SolidOfRevolutionConfig { g?, a, b, axis, kind, at, methods, n }`.
- **Answers** `numeric`, `expression`, `choice`, `set`.
- **AI hooks** targets `slider:sweep`, `handle:x`, `slice`, `profile`, `solid`, `axis`; tryable `slider:sweep`.
- **Accessibility** The solid described in words; table of slice volumes.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.10.19 `volume-slicer`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.25 · first use 1.3 L77

A double integral as the volume under a surface: Riemann columns; slicing into cross-sections with area $A(x)=\int f(x,y)\,dy$; iterated integrals; polar wedges and cylindrical shells, including the Gaussian integral.

- **Composes** `plot-3d`, `plot-2d`, `slider`, `drag-point`, `marks`, `live-formula`, `numeric-input`.
- **Config** `VolumeSlicerConfig { region, mode, n?, sliceAxis? }`.
- **Answers** `numeric`, `expression`, `choice`.
- **AI hooks** targets `column:<i>,<j>`, `slice`, `area:slice`, `plot:A`, `shell:<k>`.
- **Accessibility** Volume estimate and slices described; table of $A(x)$.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.10.20 `surface-explorer`

composite · tier composite · cluster `calculus` · **P0** · size L · spec calc-linalg 5.19 · first use 1.3 L106

Functions of two variables as surfaces and contour maps; partial derivatives as slopes of slices; tangent planes and linear approximation.

- **Composes** `plot-3d`, `plot-2d`, `marks`, `drag-point`, `slider`, `live-formula`, `numeric-input`, `expression-input`.
- **Config** `SurfaceExplorerConfig { box, contours, levels, labels, point, show, surface, contour, slices, tangentPlane, layout }`.
- **Answers** `numeric`, `choice`, `point`, `expression`.
- **AI hooks** targets `handle:point`, `slice:x`, `slice:y`, `panel:x`, `panel:y`, `contour:<level>`, `plane:tangent`, `surface`.
- **Accessibility** The contour map is the accessible view; "At (1, 2), f = 5. Moving in +x, f rises 2 per unit; moving in +y, f falls 1 per unit." An optional coarse 7 by 7 value table.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** log-likelihood surfaces (P1, prob-stats 5); Loss surfaces over two weights: convex logistic loss; the non-convex loss of a two-weight network with its symmetric (P2, ML 5).

#### 5.10.21 `dependency-graph`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.23 · first use 1.3 L112

The multivariable chain rule as a sum over paths of products of partial derivatives; computational graphs; backpropagation as accumulating derivatives in reverse.

- **Composes** `marks`, `token-tray`, `region-select`, `live-formula`, `expression-input`, `stepper`.
- **Config** `DependencyGraphConfig { id, label, layer, edges, from, to, partial, build, target, values?, mode }`.
- **Answers** `set`, `expression`, `numeric`, `point`.
- **AI hooks** targets `node:<id>`, `edge:<from>-<to>`, `path:<leaf>`, `term:<path>`.
- **Accessibility** The tree as a nested list of paths.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** Backprop mode extended: neuron operations (affine, ReLU, sigmoid, softmax with cross-entropy) as nodes (P2, ML 5).
- Drawn by `node-link` in layered layout; backpropagation mode P2.

#### 5.10.22 `gradient-compass`

composite · tier composite · cluster `calculus` · **P0** · size S · spec calc-linalg 5.20 · first use 1.3 L114

Directional derivatives and the gradient: which way is steepest, why the gradient crosses contours at right angles, and $D_{\mathbf u}f=\nabla f\cdot\mathbf u=\lvert\nabla f\rvert\cos\theta$.

- **Composes** `plot-2d`, `drag-point`, `marks`, `live-formula`.
- **Config** `GradientCompassConfig { point, movablePoint, theta, revealGradient, anglePlot }`.
- **Answers** `point`, `numeric`, `expression`, `choice`.
- **AI hooks** targets `handle:point`, `handle:direction`, `vector:grad`, `contour:through-point`, `plot:angle`.
- **Accessibility** The direction handle reports degrees; "Heading 30°: f rises at 1.73 per unit; steepest rise 2.0 at 0°."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.10.23 `quadratic-form`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.22 · first use 1.3 L119

$q(\mathbf x)=\mathbf x^\top A\mathbf x$ for symmetric $A$: bowl, saddle or ridge; eigenvectors as principal axes; the tests for positive definiteness; the second-derivative test through the Hessian; covariance ellipses.

- **Composes** `matrix`, `slider`, `plot-3d`, `plot-2d`, `drag-point`, `marks`, `live-formula`, `choice`.
- **Config** `QuadraticFormConfig { editable, ranges, views, mode, f?, at? }`.
- **Answers** `choice`, `set`, `numeric`, `matrix`.
- **AI hooks** targets `slider:a`, `slider:b`, `slider:c`, `slider:r12`, `slider:r13`, `slider:r23`, `cell:<i>,<j>`, `axis:1`, `axis:2`, `test:pivots`, `test:eigenvalues`, `test:minors` and 2 more; tryable `slider:a`, `slider:b`, `slider:c`, `slider:r12`.
- **Accessibility** "q = 2x² + 6xy + 2y²: eigenvalues 5 and −1, indefinite (a saddle). Along (1, −1)/√2, q is negative."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** covariance ellipses and Mahalanobis distance (P0); coefficient confidence ellipse (P1, prob-stats 5); Ridge-shift mode: $X^\top X + \lambda I$ moves every eigenvalue up by $\lambda$ and rounds the bowl (P2, ML 5).

#### 5.10.24 `lagrange-explorer`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.26 · first use 1.3 L124

Constrained optimisation: walk along a constraint and watch $f$; at the optimum the level curve is tangent to the constraint and $\nabla f=\lambda\nabla g$; $\lambda$ is the shadow price; portfolio weights on a simplex.

- **Composes** `plot-2d`, `plot-3d`, `drag-point`, `slider`, `marks`, `live-formula`, `numeric-input`, `expression-input`, `choice`.
- **Config** `LagrangeExplorerConfig { g, c, cRange?, start, show, contours, gradients, profile, coords, vars }`.
- **Answers** `point`, `numeric`, `expression`, `choice`.
- **AI hooks** targets `handle:point`, `curve:constraint`, `vector:gradf`, `vector:gradg`, `contour:<level>`, `plot:profile`, `slider:c`; tryable `slider:c`.
- **Accessibility** "On the circle at 40°: f = 3.2. The gradients differ by 25°, so moving along the circle still changes f."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** minimum-variance portfolio preset (P1, finance 5).

#### 5.10.25 `region-bounds`

composite · tier composite · cluster `calculus` · **P0** · size M · spec calc-linalg 5.24 · first use 1.3 L130

Set up double and triple integrals: describe a region by bounds, with vertical or horizontal strips; swap the order of integration; polar regions; probability over regions.

- **Composes** `plot-2d`, `marks`, `drag-point`, `choice`, `expression-input`, `live-formula`, `plot-3d`.
- **Config** `RegionBoundsConfig { id, expr, kind, target, coords, askOrder?, integrand?, density?, dims?, zBounds? }`.
- **Answers** `expression`, `numeric`, `choice`, `state`.
- **AI hooks** targets `boundary:<id>`, `strip`, `bound:outer-lo`, `bound:outer-hi`, `bound:inner-lo`, `bound:inner-hi`, `bound:z-lo`, `bound:z-hi`, `mismatch`.
- **Accessibility** Boundaries and their intersection points described; bound fields fully keyboard-driven.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** joint density as the integrand (P0, prob-stats 5).

### 5.11 Linear algebra (1.4)

#### 5.11.1 `matrix-multiply`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.5 · first use 0.3 L88

$AB$ by entries (row times column), by columns (combinations of $A$'s columns), by rows, and as a sum of outer products; shape rules; non-commutativity; permutation and elimination matrices acting on rows; transpose rules.

- **Composes** `matrix`, `marks`, `choice`, `numeric-input`, `stepper`, `token-tray`.
- **Config** `MatrixMultiplyConfig { B, view, fill?, shapes? }`.
- **Answers** `matrix`, `numeric`, `choice`, `set`.
- **AI hooks** targets `layer:<k>`.
- **Accessibility** "C row 2, column 1 = row 2 of A dot column 1 of B = 3·1 + 0·2 = 3."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** `entrywise` mode and 2 by 2 inverse readout for `matrix-grid` (P0, 0.3); entry, column, row and outer views, shape puzzle, multiplication counter (P0, 1.4 L9, curriculum); two-step transition sums (P0, prob-stats 5).
- First used at 0.3 L88 and pulled into 1.1 L67 (python-tools decision 19).

#### 5.11.2 `determinant-lab`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.13 · first use 0.3 L91

The determinant as signed area or volume; its three defining properties seen through row operations (a shear keeps the area, a swap flips the sign, scaling a row scales the area); $\det(AB)=\det A\det B$; cofactor expansion.

- **Composes** `plot-2d`, `plot-3d`, `drag-point`, `matrix`, `marks`, `stepper`, `live-formula`, `numeric-input`, `choice`.
- **Config** `DeterminantLabConfig { A, movable, mode }`.
- **Answers** `numeric`, `choice`, `state`, `matrix`.
- **AI hooks** targets `shape`, `handle:col1`, `handle:col2`, `handle:col3`, `cell:<i>,<j>`, `minor:<i>,<j>`, `op:<k>`, `step:<k>`.
- **Accessibility** Area and sign described; expansions read as sums.
- **Reduced motion** Before and after.
- First used at 0.3 L91, so it ships with Stage 0.

#### 5.11.3 `projection-lab`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.2 · first use 1.3 L107

Lengths, dot products and angles; the projection of $\mathbf b$ onto a line and onto a plane; the error vector perpendicular to what it was projected onto; projection matrices; the cross product in 3D.

- **Composes** `plot-2d`, `plot-3d`, `drag-point`, `marks`, `live-formula`, `matrix`, `numeric-input`.
- **Config** `ProjectionLabConfig { a?, A?, b, movable, mode, showMatrix? }`.
- **Answers** `point`, `numeric`, `matrix`, `choice`.
- **AI hooks** targets `vec:a`, `vec:b`, `vec:p`, `vec:e`, `angle:right`, `plane`, `marker:predict`, `region:positive`, `region:negative`, `vec:cross`.
- **Accessibility** "a = (3, 1), b = (2, 2). a · b = 8. p = 0.8a = (2.4, 0.8); e = (−0.4, 1.2), at 90° to a."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.11.4 `least-squares-fit`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.11 · first use 1.3 L122

Fitting a line or polynomial by least squares: residuals and the sum of squared errors; the error bowl over (intercept, slope); the normal equations $A^\top A\hat{\mathbf x}=A^\top\mathbf b$; the picture in $\mathbb R^m$.

- **Composes** `plot-2d`, `drag-point`, `marks`, `value-table`, `matrix`, `live-formula`, `sim-runner`, `code-cell`, `projection-lab`.
- **Config** `LeastSquaresFitConfig { generate, n, slope, intercept, noise, seed, movablePoints, degree, line?, C, D, show, residuals, squares, errorMap, matrices, r3?, preset? }`.
- **Answers** `numeric`, `point`, `matrix`, `choice`, `code`.
- **AI hooks** targets `handle:line-1`, `handle:line-2`, `point:<i>`, `residual:<i>`, `square:<i>`, `map:error`, `point:learner-cd`, `point:optimum`, `cell:<i>,<j>`.
- **Accessibility** Table of data, fitted values and residuals; "Your line y = 1.2 + 0.8x has a total of 4.31; the smallest possible is 3.95."
- **Reduced motion** Before and after.
- **Modes added** ridge mode (P0, 1.4 L47, curriculum); Linked from `regression-lab`; already declared shared with 1.6 (P1, prob-stats 5).

#### 5.11.5 `transform-grid`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.6 · first use 1.3 L134

A matrix as a transformation: the images of $\mathbf e_1$ and $\mathbf e_2$ are its columns; composition is multiplication; the inverse undoes; the determinant is the signed area factor.

- **Composes** `plot-2d`, `plot-3d`, `drag-point`, `slider`, `matrix`, `marks`, `live-formula`.
- **Config** `TransformGridConfig { A, movableColumns, target?, mode, B?, map?, x, y, domain, glyph?, snap? }`.
- **Answers** `matrix`, `numeric`, `choice`, `point`.
- **AI hooks** targets `handle:col1`, `handle:col2`, `handle:col3`, `glyph`, `square`, `grid`, `slider:t`, `probe`, `inset`, `cell:<i>,<j>`; tryable `slider:t`.
- **Accessibility** "A = [[2, 1], [0, 1]]: e1 goes to (2, 0), e2 to (1, 1). Areas double; orientation is kept."
- **Reduced motion** Play becomes a before-and-after pair.
- **Modes added** non-square $A$, 3D to the plane (P0, 1.4 L17, curriculum); Cholesky and Box-Muller presets (P0, prob-stats 5).

#### 5.11.6 `vector-combo`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.1 · first use 1.4 L1

Vectors as arrows; linear combinations $c\mathbf v+d\mathbf w$; reaching a target; span as a line, a plane or everything; independence; $A\mathbf x$ as a combination of columns.

- **Composes** `plot-2d`, `plot-3d`, `drag-point`, `slider`, `marks`, `live-formula`, `matrix`, `numeric-input`.
- **Config** `VectorComboConfig { vectors, id, at, movable, label, coeffs?, for, range, step?, target?, mode, lattice?, snap? }`.
- **Answers** `numeric`, `point`, `choice`, `matrix`, `state`.
- **AI hooks** targets `vec:<id>`, `handle:<id>`, `handle:combo`, `slider:c`, `slider:d`, `span`, `target`, `volume`; tryable `slider:c`, `slider:d`.
- **Accessibility** "v = (2, 1), w = (1, 3). 1.5v − 0.5w = (2.5, 0). The target (3, 4) needs c = 1, d = 1."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** `lattice` and `path` modes for `vector-plane` (P0, 0.3); `readout: after-check` and an export `result` for feedback templates (P0, 1.4 sample, curriculum).

#### 5.11.7 `row-column-picture`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.3 · first use 1.4 L6

$A\mathbf x=\mathbf b$ two ways: rows as lines (or planes) meeting at the solution; columns combining to reach $\mathbf b$.

- **Composes** `plot-2d`, `plot-3d`, `matrix`, `drag-point`, `slider`, `marks`, `live-formula`.
- **Config** `RowColumnPictureConfig { b, editable, A?, b?, views, dims }`.
- **Answers** `matrix`, `numeric`, `choice`, `point`.
- **AI hooks** targets `line:<i>`, `plane:<i>`, `point:solution`, `col:<j>`, `vec:b`, `cell:<i>,<j>`, `slider:x<j>`; tryable `slider:x<j>`.
- **Accessibility** "Row picture: 2x − y = 0 and −x + 2y = 3 meet at (1, 2). Column picture: 1·(2, −1) + 2·(−1, 2) = (0, 3)."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.11.8 `elimination-lab`

composite · tier composite · cluster `linalg` · **P0** · size L · spec calc-linalg 6.4 · first use 1.4 L7

Gaussian elimination by hand in exact arithmetic: pivots, multipliers, row operations and exchanges; reaching $U$; back substitution; Gauss-Jordan to RREF and the inverse.

- **Composes** `matrix`, `numeric-input`, `stepper`, `marks`, `live-formula`, `row-column-picture`.
- **Config** `EliminationLabConfig { b?, goal, allowed, autoMultiplier?, showRowPicture?, maxOps? }`.
- **Answers** `matrix`, `numeric`, `set`.
- **AI hooks** targets `row:<i>`, `cell:<i>,<j>`, `pivot:<k>`, `op:<n>`, `builder:target`, `builder:source`, `builder:multiplier`.
- **Accessibility** Each operation announced with its resulting row; the matrix is a grid.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** floating mode (P0, 1.4 L16, curriculum).

#### 5.11.9 `subspace-tester`

composite · tier composite · cluster `linalg` · **P0** · size S · spec calc-linalg 6.7 · first use 1.4 L19

What makes a subspace: it contains $\mathbf 0$ and is closed under addition and scalar multiplication.

- **Composes** `plot-2d`, `plot-3d`, `drag-point`, `slider`, `marks`, `choice`.
- **Config** `SubspaceTesterConfig { set, kind, def, allowCounterexample }`.
- **Answers** `choice`, `state`.
- **AI hooks** targets `handle:u`, `handle:w`, `vec:sum`, `vec:scaled`, `slider:c`, `set`; tryable `slider:c`.
- **Accessibility** Membership tests described numerically ("u + w = (−1, 2) is not in the first quadrant").
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.11.10 `solution-set`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.9 · first use 1.4 L22

The complete solution $\mathbf x=\mathbf x_p+\mathbf x_n$: free variables as parameters; a point, line or plane offset from the origin, parallel to the nullspace; the rank cases.

- **Composes** `matrix`, `slider`, `plot-3d`, `marks`, `expression-input`, `choice`.
- **Config** `SolutionSetConfig { b, editableB?, showRref?, view3d? }`.
- **Answers** `matrix`, `numeric`, `choice`, `state`, `set`.
- **AI hooks** targets `slider:<free>`, `set:solution`, `set:null`, `pivot:<k>`, `row:<i>`; tryable `slider:<free>`.
- **Accessibility** The set read as a parametric equation.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.11.11 `four-subspaces`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.8 · first use 1.4 L24

Strang's big picture: row space and nullspace in $\mathbb R^n$, column space and left nullspace in $\mathbb R^m$, with dimensions $r$, $n-r$, $r$, $m-r$; orthogonal complements.

- **Composes** `marks`, `token-tray`, `matrix`, `numeric-input`, `plot-3d`, `drag-point`, `live-formula`.
- **Config** `FourSubspacesConfig { tokens, id, vector, ask }`.
- **Answers** `numeric`, `set`, `choice`.
- **AI hooks** targets `box:row`, `box:null`, `box:col`, `box:leftnull`, `token:<id>`, `dim:<box>`, `handle:x`.
- **Accessibility** The diagram described as four labelled lists.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** graph mode (P0, 1.4 L32 and L97, curriculum).

#### 5.11.12 `basis-change`

composite · tier composite · cluster `linalg` · **P0** · size S · spec calc-linalg 6.10 · first use 1.4 L33

Coordinates relative to a basis; change-of-basis matrices; the same transformation written in another basis (similar matrices); diagonalisation as switching to the eigenbasis.

- **Composes** `plot-2d`, `drag-point`, `matrix`, `marks`, `numeric-input`.
- **Config** `BasisChangeConfig { movableBasis, x, T?, mode }`.
- **Answers** `numeric`, `matrix`, `choice`.
- **AI hooks** targets `handle:b1`, `handle:b2`, `handle:x`, `grid:standard`, `grid:basis`, `cell:<i>,<j>`.
- **Accessibility** Both coordinate pairs described.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.11.13 `gram-schmidt`

composite · tier composite · cluster `linalg` · **P0** · size S · spec calc-linalg 6.12 · first use 1.4 L50

Turn a basis into an orthonormal basis step by step; assemble $A=QR$.

- **Composes** `plot-2d`, `plot-3d`, `stepper`, `drag-point`, `marks`, `matrix`, `live-formula`.
- **Config** `GramSchmidtConfig { vectors, movable, predict, showQR }`.
- **Answers** `point`, `matrix`, `numeric`.
- **AI hooks** targets `vec:a`, `vec:b`, `vec:c`, `proj:<k>`, `q:<k>`, `step:<k>`, `handle:predict`.
- **Accessibility** Each step described numerically.
- **Reduced motion** Before and after per step.

#### 5.11.14 `eigen-finder`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.14 · first use 1.4 L60

Eigenvectors as directions that do not turn; eigenvalues as stretch factors; finding them through $\det(A-\lambda I)=0$; trace and determinant; complex eigenvalues (a rotation leaves no real direction).

- **Composes** `plot-2d`, `drag-point`, `matrix`, `slider`, `marks`, `live-formula`, `numeric-input`, `choice`.
- **Config** `EigenFinderConfig { editable?, mode, showEllipse?, showAngle }`.
- **Answers** `point`, `numeric`, `choice`, `expression`, `state`.
- **AI hooks** targets `handle:x`, `vec:Ax`, `ellipse`, `eigenline:<k>`, `slider:lambda`, `plot:charpoly`, `root:<k>`, `cell:<i>,<j>`; tryable `slider:lambda`.
- **Accessibility** "x at 30°: Ax = (2.1, 1.3), pointing at 31.8°, 1.8° away; it is 2.5 times as long."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** left eigenvector for $\lambda = 1$ as the stationary distribution (P0, prob-stats 5).

#### 5.11.15 `linear-dynamics`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.15 · first use 1.4 L65

Powers $A^k$ through the eigen-decomposition; long-run behaviour; Markov matrices and steady states; Fibonacci growth; continuous systems $\frac{d\mathbf u}{dt}=A\mathbf u$, their stability and phase portraits.

- **Composes** `plot-2d`, `drag-point`, `stepper`, `slider`, `marks`, `matrix`, `value-table`, `live-formula`, `numeric-input`, `choice`.
- **Config** `LinearDynamicsConfig { mode, x0, kMax, showDecomposition, field? }`.
- **Answers** `numeric`, `point`, `choice`, `state`.
- **AI hooks** targets `handle:x0`, `iterate:<k>`, `eigenline:<k>`, `component:<k>`, `field`, `trajectory:<i>`, `slider:k`; tryable `slider:k`.
- **Accessibility** Table of $k$ and $\mathbf x_k$; the portrait described by type and eigenvalues.
- **Reduced motion** Steps jump.
- **Modes added** Markov mode linked from `markov-chain` (P0, prob-stats 5).

#### 5.11.16 `svd-stepper`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.16 · first use 1.4 L72

$A=U\Sigma V^\top$ as rotate, stretch, rotate; singular values as the ellipse's semi-axes; singular vectors; rank; the pseudoinverse; the symmetric case $A=Q\Lambda Q^\top$ (the spectral theorem).

- **Composes** `plot-2d`, `stepper`, `slider`, `matrix`, `drag-point`, `marks`, `live-formula`.
- **Config** `SvdStepperConfig { mode, dims, editable? }`.
- **Answers** `numeric`, `point`, `matrix`, `choice`.
- **AI hooks** targets `stage:<k>`, `vec:v1`, `vec:v2`, `vec:u1`, `vec:u2`, `ellipse`, `sigma:<k>`, `handle:axis1`, `handle:axis2`.
- **Accessibility** Stages described numerically ("Stretch: 3 along the first axis, 1 along the second").
- **Reduced motion** Stepped stages.
- 3D mode P1.

#### 5.11.17 `pca-lab`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.18 · first use 1.4 L74

PCA as finding the direction of greatest variance: projections onto a line; covariance and its top eigenvector; centring and scaling; explained variance; reconstruction; PCA of yield-curve changes (level, slope, curvature).

- **Composes** `plot-2d`, `plot-3d`, `drag-point`, `marks`, `sim-runner`, `slider`, `value-table`, `token-tray`, `code-cell`.
- **Config** `PcaLabConfig { generate, n, cov, mean, seed, points, preset, dims, mode, centre, standardise?, angle? }`.
- **Answers** `point`, `numeric`, `choice`, `set`, `code`.
- **AI hooks** targets `handle:angle`, `line:direction`, `proj:<i>`, `point:<i>`, `bar:variance`, `ellipse:cov`, `pc:<k>`, `loading:<k>`, `toggle:centre`, `toggle:standardise`; tryable `toggle:centre`, `toggle:standardise`.
- **Accessibility** "Your line at 20° captures variance 3.1; the most possible is 4.4 at 35°." Table of points and projections.
- **Reduced motion** Before and after.
- **Modes added** scree view and returns-panel preset (P0, 1.4 L93, curriculum); PCR link (regress on the top $m$ components, sending coefficients to `regularisation-path`) (P2, ML 5).

#### 5.11.18 `low-rank-approx`

composite · tier composite · cluster `linalg` · **P0** · size S · spec calc-linalg 6.17 · first use 1.4 L86

A rank-$k$ approximation as a sum of rank-one layers $\sigma_i\mathbf u_i\mathbf v_i^\top$; the Eckart-Young theorem; the singular-value spectrum; compression and denoising; factor structure in a returns matrix.

- **Composes** `marks`, `slider`, `plot-2d`, `stepper`, `live-formula`, `numeric-input`, `choice`.
- **Config** `LowRankApproxConfig { image, matrix, generate, m, n, rank, noise, seed, kMax, showLayers }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `slider:k`, `bar:<i>`, `layer:<i>`, `heatmap:A`, `heatmap:Ak`, `heatmap:residual`, `slider:noise`; tryable `slider:k`, `slider:noise`.
- **Accessibility** "k = 5 keeps 92% of the energy; the error is 0.08." Table of singular values.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.11.19 `condition-number`

composite · tier composite · cluster `linalg` · **P0** · size M · spec calc-linalg 6.19 · first use 1.4 L88

How sensitive $A\mathbf x=\mathbf b$ is to small changes in $\mathbf b$: a small disc of perturbations maps to a long ellipse of solutions; $\kappa=\sigma_{\max}/\sigma_{\min}$; near-singular systems.

- **Composes** `plot-2d`, `drag-point`, `slider`, `sim-runner`, `marks`, `live-formula`, `numeric-input`, `choice`.
- **Config** `ConditionNumberConfig { family, eps, b, delta, samples, mode }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `handle:b`, `disc`, `cloud`, `ellipse`, `slider:eps`, `slider:delta`; tryable `slider:eps`, `slider:delta`.
- **Accessibility** "A 1% change in b moves x by up to 40%; κ = 40."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** norm-balls mode shared with `penalty-geometry` (P2, ML 4).
- Moved from P1 to P0: 1.4 L88 needs it and L45 previews it (linear-algebra request).

### 5.12 Probability (1.5)

#### 5.12.1 `path-simulator`

composite · tier composite · cluster `probability` · **P0** · size L · spec calc-linalg 7.1 · first use 1.1 L72

Random walks and Brownian motion: the scaling limit, a fan of paths, the distribution at time $t$, independent increments, absorbing barriers (gambler's ruin), correlated paths in two dimensions, self-similarity.

- **Composes** `plot-2d`, `sim-runner`, `slider`, `drag-point`, `marks`, `value-table`, `numeric-input`, `choice`.
- **Config** `PathSimulatorConfig { seed, paths, initial, max, n?, values, T, drift?, sigma?, barriers?, lower?, upper?, absorbing, rho?, show, envelope, histogramAtT, density, predictFirst? }`.
- **Answers** `numeric`, `choice`, `point`.
- **AI hooks** targets `path:<i>`, `path:sample`, `cursor:t`, `hist:t`, `density`, `envelope`, `barrier:upper`, `barrier:lower`, `slider:n`, `slider:rho`; tryable `slider:n`, `slider:rho`.
- **Accessibility** "200 paths to T = 1. At t = 0.5 the sample variance is 0.49 (theory 0.5)." Quantile table at the cursor.
- **Reduced motion** Paths appear at once.
- **Modes added** random-walk and price modes (P0, moved from P2; 1.1 L72, L73, curriculum); drift with the ruin formula, running-maximum histogram, link to `lattice-walk` (P0, prob-stats 5); `bridge`, `ratio` and asynchronous two-path modes (P2, 3.2 L39, L69, L71, curriculum).
- Cluster `probability` because its P0 modes (walk, barrier, scaled walk, price) serve 1.1 L72 and L73 and 1.5.
- Brownian, two-dimensional and Poisson modes are P2; the 3.2 `brownian-path` request is its `refine` mode (midpoint refinement keeps coarse paths fixed, calc-linalg decision 9).

#### 5.12.2 `puzzle-workbench`

composite · tier composite · cluster `probability` · **P0** · size L · spec finance 8.1 · first use 1.5 L1 (through the weekly problems)

Interview problems are solved on paper and aloud, not on a canvas.

- **Composes** `scratch-pad`, `speed-timer`, `numeric-input`, `expression-input`, `choice`, `free-response`, `derivation-steps`, `voice-capture`, `live-formula`, `first-step-solver`, `indicator-board`, `geo-prob`, `lattice-walk`, `order-statistics`, `markov-chain`, `game-lab`, `outcome-grid`, `counting-slots`, `path-simulator`, `bet-lab`, `kelly-lab`; services `problem-bank`.
- **Config** `PuzzleWorkbenchConfig { mode, problem, answer, linked?, timer, template?, source? }`.
- **Answers** `numeric`, `expression`, `choice`, `state`.
- **AI hooks** targets `problem`, `notes`, `answer`, `timer`, `picture`, `step:<n>`; describe, e.g. "Problem: expected rolls of a fair die until two sixes in a row. Attempt 1: 36 (not yet). Notes: 3 lines, defines states 0, 1."; secret: the answer and the solution outline. Bertie may read the notes text; the ink only as an image on request.
- **Accessibility** The problem is text; the timer can be hidden; cold mode offers the "more time" setting with adjusted marking (section 2.8).
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** `debrief-variance` mode (P2, 3.3 L40, curriculum).
- P0 core (weekly, practice and book-log modes) because three weekly problems start at 1.5 lesson 1 (assessment decision 17); cold and aloud modes P2.
- Cluster `probability` for its P0 core.
- Its linked pictures (`first-step-solver`, `markov-chain`, `game-lab`, `bet-lab` and the rest under Composes) are optional links; each link waits for that widget's own wave, so the P0 core depends only on `scratch-pad`, `speed-timer` and the inputs.

#### 5.12.3 `indicator-board`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.2.5 · first use 1.5 L10

$X = \sum_j I_j$, so $E[X] = \sum_j P(A_j)$, whether or not the events are independent.

- **Composes** `chance-object`, `marks`, `sim-runner`, `slider`, `live-formula`, `numeric-input`, `value-table`; mark types `hist`.
- **Config** `IndicatorBoardConfig { scenario, n, params?, editable?, show, predictFirst? }`.
- **Answers** `numeric`, `expression`, `choice`.
- **AI hooks** targets `object:<j>`, `lamp:<j>`, `count`, `trace:mean`, `line:exact`, `cov:<i>,<j>`, `slider:n`; describe, e.g. "Fixed points, n = 10. 1,000 instances: mean count 1.004. Exact line hidden. Lamp 3 open: P(card 3 in place) entered 1/10."; secret: $E[X]$ and $\mathrm{Var}(X)$; tryable `slider:n`.
- **Accessibility** Each position reads "Position 3: card 3, a match, 1". Table view of instance counts. Batches announce the running mean and the exact value when shown.
- **Reduced motion** Instant.

#### 5.12.4 `prob-square`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.1.1 · first use 1.5 L13

Make $P(A \cap B) = P(A)\,P(B \mid A)$ a rectangle the learner can resize.

- **Composes** `plot-2d`, `drag-point`, `mass-editor`, `region-select`, `marks`, `live-formula`, `stepper`.
- **Config** `ProbSquareConfig { mode, labels, init, editable, snap?, show, evidenceSequence?, task? }`.
- **Answers** `numeric`, `set`, `state`.
- **AI hooks** targets `split:a`, `split:b|a`, `split:b|not-a`, `region:a-b`, `region:a-notb`, `region:nota-b`, `region:nota-notb`, `col:<i>`, `prior:<i>`, `lik:<i>`, `formula`; describe, e.g. "Square: P(A) = 0.30; P(B|A) = 0.40, P(B|not A) = 0.40 (splits aligned). Conditioned on: none."; secret: target posterior and the exact areas the task asks for.
- **Accessibility** Rectangles are buttons named with their event and area ("A and B, 0.12"). Handles are sliders ("Probability of B given A, 0.40").
- **Reduced motion** Renormalise and show-why become before-and-after with Play; flashes become a static highlight.

#### 5.12.5 `trial-strip`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.2.6 · first use 1.5 L16

Discrete: a strip of coin flips shows the wait to the first head (geometric), to the $r$th head (negative binomial), to a pattern such as HH or HT, and runs.

- **Composes** `chance-object`, `marks`, `region-select`, `slider`, `token-tray`, `sim-runner`, `dist-explorer`; mark types `hist`, `stems`.
- **Config** `TrialStripConfig { mode, p?, lambda?, n?, pattern?, displays, condition?, streams?, thinning?, predictFirst? }`.
- **Answers** `numeric`, `choice`, `distribution`.
- **AI hooks** targets `cell:<i>`, `pattern:<id>`, `window`, `tick:<i>`, `hist:waits`, `hist:window`, `slider:p`, `slider:lambda`, `slider:n`; describe, e.g. "Pattern race HH against HT, fair coin. 1,000 sequences: mean wait HH 5.96, HT 4.02. Exact hidden."; secret: exact expected waits; tryable `slider:p`, `slider:lambda`, `slider:n`.
- **Accessibility** The strip reads as text ("H T T H H"); the window announces its count ("3 arrivals between 2.0 and 4.5"). Table views for every histogram.
- **Reduced motion** Cells and histograms appear at once.
- **Modes added** arrival marker in Poisson mode (P0, 1.5 L75, curriculum).

#### 5.12.6 `first-step-solver`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.4.3 · first use 1.5 L16

Most interview probability questions with "until" or "first" in them are first-step problems.

- **Composes** `node-link`, `token-tray`, `expression-input`, `matrix`, `sim-runner`, `live-formula`, `stepper`.
- **Config** `FirstStepSolverConfig { chain, unknown, target?, start, editable, simulate? }`.
- **Answers** `state`, `numeric`, `expression`, `choice`.
- **AI hooks** targets `node:<id>`, `edge:<a>-<b>`, `eq:<id>`, `term:<id>:<k>`, `chip:one`, `solve`, `sim`; describe, e.g. "States 0, H, HH (absorbing). Unknown: expected tosses. x0 = 1 + ½xH + ½x0 entered; xH missing; boundary xHH = 0 set."; secret: the solution vector; tryable `chip:one`.
- **Accessibility** Equations as text ("x zero equals 1 plus one half x H plus one half x zero"); states as buttons; walker results announced after each batch.
- **Reduced motion** Chips appear in place.

#### 5.12.7 `odds-ledger`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.1.4 · first use 1.5 L17

$\text{posterior odds} = \text{prior odds} \times \text{likelihood ratio}$.

- **Composes** `number-line`, `token-tray`, `slider`, `drag-point`, `live-formula`.
- **Config** `OddsLedgerConfig { hypotheses, prior, evidence, scale?, show, predict? }`.
- **Answers** `numeric`, `point`, `choice`.
- **AI hooks** targets `card:<id>`, `marker:prior`, `marker:posterior`, `marker:prediction`, `slider:prior`, `ledger`; describe, e.g. "Prior odds 1:99 (P = 0.01). Applied: positive test (× 10). Posterior odds 10:99 (P = 0.092)."; tryable `slider:prior`.
- **Accessibility** The line is a slider-like readout with `aria-valuetext` "odds 18 to 99, probability 0.154". The ledger is a list.
- **Reduced motion** The marker jumps.
- Bayes factors P1.

#### 5.12.8 `icon-array`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.1.2 · first use 1.5 L27

Natural frequencies make conditional probability countable: "Of 1,000 people, 10 have it; 9 of those test positive; 89 of the 990 without it also test positive." The learner filters to positives and counts.

- **Composes** `marks`, `slider`, `region-select`, `contingency-table`, `live-formula`; mark types `glyphs`.
- **Config** `IconArrayConfig { n, mode, attributes, editable?, glyph?, layout?, strata? }`.
- **Answers** `numeric`, `set`, `choice`.
- **AI hooks** targets `block:<attr-combination>`, `block:cond-pos`, `chip:<filter>`, `slider:<rate>`; describe, e.g. "1,000 people: 10 with condition, 9 of them positive; 89 of 990 without it positive. Filter: positive (98 shown). Sorted: yes."; secret: the requested count; tryable `chip:<filter>`, `slider:<rate>`.
- **Accessibility** Group named "1,000 people"; the table view is the $2 \times 2$ count table; the filter result is announced ("Showing 98 people who test positive; 9 have the condition").
- **Reduced motion** Instant.
- **Modes added** Imbalance mode: 1,000 glyphs coloured by confusion outcome, bound to `threshold-lab`'s threshold (P2, ML 5).
- FDR mode P1.

#### 5.12.9 `contingency-table`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.1.3 · first use 1.5 L28

Joint, marginal and conditional distributions of two categorical variables; independence as "every row has the same shape"; Simpson's paradox as strata that disagree with their sum; in 1.6.

- **Composes** `value-table`, `mass-editor`, `marks`, `slider`, `live-formula`.
- **Config** `ContingencyTableConfig { rows, cols, cells?, editable?, display?, strata?, mosaic?, chi2? }`.
- **Answers** `numeric`, `state`, `choice`.
- **AI hooks** targets `cell:<r>,<c>`, `row:<r>`, `col:<c>`, `margin:row:<r>`, `margin:col:<c>`, `stratum:<i>`, `mosaic`; describe, e.g. "2 × 2 counts. Treated: 81/87 and 192/263; Control: 234/270 and 55/80. Display: row conditional. Combined: no."
- **Accessibility** A native table with scoped headers; conditional displays announce their denominator ("Row: smokers, 120 people").
- **Reduced motion** Instant.
- **Modes added** confusion preset with precision, recall, F1 and MCC; mutual-information readout (P2, ML 5, 2.1 L16).
- Expected counts and $\chi^2$ P1.

#### 5.12.10 `game-lab`

composite · tier composite · cluster `probability` · **P0** · size L · spec prob-stats 6.4.2 · first use 1.5 L39

Interview games teach expectation, conditioning and optimal stopping better than any formula sheet.

- **Composes** `chance-object`, `sim-runner`, `stepper`, `slider`, `value-table`, `marks`, `choice`.
- **Config** `GameLabConfig { game, params, modes, rounds, predictFirst? }`.
- **Answers** `numeric`, `choice`, `state`, `ordering`.
- **AI hooks** targets `door:<i>`, `die`, `decision:<id>`, `slider:<policy>`, `trace`, `line:exact`, `value:<stage>`, `path:median`; secret: exact values and the optimal policy; tryable `slider:<policy>`.
- **Accessibility** Every decision is a button; "Monty Hall, 3 doors, host knows. Hand play: 7 rounds; switched 4 times and won 3; stuck 3 times and won 1. Policy always switch: 10,000 rounds, won 0.668; exact two thirds."
- **Reduced motion** Instant.
- **Modes added** Kelly mode, embedding `kelly-lab`'s growth curve per finance decision 17 (P0, moved from P2; 1.5 L154, curriculum); interview betting presets linked to `bet-lab` (P2, finance 5).

#### 5.12.11 `rv-mapper`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.2.1 · first use 1.5 L45

Assign numbers to outcomes, then pour each outcome's probability along its arrow into a stem over its value: the PMF appears as the sum of preimage masses.

- **Composes** `outcome-grid`, `node-link`, `marks`, `number-line`, `token-tray`, `live-formula`, `stepper`; mark types `connector`, `stems`.
- **Config** `RvMapperConfig { space, rule?, ruleChips?, editable, axis, g?, show, task }`.
- **Answers** `mapping`, `distribution`, `numeric`, `set`.
- **AI hooks** targets `outcome:<id>`, `value:<x>`, `stem:<x>`, `connector:<outcome>`, `g:<y>`, `rule:<id>`; describe, e.g. "Two dice, X = sum. Assigned 36 of 36. Collected: yes. P(X = 7) = 6/36 shown. Lit: preimage of 7."; secret: the target PMF; tryable `rule:<id>`.
- **Accessibility** Table view: outcome, probability, $X$ value, $g(X)$ value; a second table for the PMF. Assignments are announced ("Outcome (2, 5) assigned 7").
- **Reduced motion** Stems fill at once; connectors light without travel.

#### 5.12.12 `dist-explorer`

composite · tier composite · cluster `probability` · **P0** · size L · spec prob-stats 6.2.2 · first use 1.5 L47

One place to learn every named distribution by its story and its shape; to read $P(a < X \le b)$ as an area and as $F(b) - F(a)$; to find quantiles; to see the mean as a balance point and the SD as a spread.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `mass-editor`, `choice`, `sim-runner`, `sketch-pad`, `live-formula`; mark types `stems`, `curve`, `step`, `region`, `band`, `hist`.
- **Config** `DistExplorerConfig { family, params, editableParams?, ranges?, panels, compare?, bracket?, quantile?, overlays?, mode?, sample?, geometricConvention?, show }`.
- **Answers** `numeric`, `interval`, `point`, `curve`, `choice`, `state`.
- **AI hooks** targets `family`, `slider:<param>`, `stem:<x>`, `curve:density`, `curve:cdf`, `bracket:a`, `bracket:b`, `region:bracket`, `handle:quantile`, `marker:mean`, `band:sd`, `curve:compare` and 3 more; describe, e.g. "Binomial(n = 10, p = 0.3). Bracket 2 ≤ X ≤ 4: 0.5372. Mean 3, SD 1.449. Compare: none. Mode: explore."; secret: target probability, quantile or parameters; tryable `slider:<param>`.
- **Accessibility** Table view: for discrete, $x$, $P(X = x)$ and $F(x)$ for up to 60 rows; for continuous, quantiles at 5% steps and the bracket probability. Sliders say their parameter ("lambda, 3.5").
- **Reduced motion** Show-why becomes before-and-after with Play; the dot stream lands as a finished histogram.
- **Modes added** Beta update (P0, 1.5 L84, curriculum); lognormal preset with $N(d_2)$ (P1, finance 5); A "maximum of $N$" family: density $N\varphi(x)\Phi(x)^{N-1}$ for $N$ independent standard normals, with the $E[\max]$ (P2, ML 5).

#### 5.12.13 `galton-board`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.2.3 · first use 1.5 L48

One ball's path is $n$ Bernoulli trials and also a random walk; the bins count successes; the number of paths into bin $k$ is $\binom{n}{k}$; tilting the board sets $p$; with many rows the shape approaches the normal.

- **Composes** `plot-2d`, `marks`, `slider`, `sim-runner`, `pascal-triangle`, `mass-editor`, `stepper`; mark types `hist`, `stems`, `curve`.
- **Config** `GaltonBoardConfig { n, p, editable, mode, overlays?, maxBalls?, predictFirst? }`.
- **Answers** `numeric`, `distribution`, `choice`.
- **AI hooks** targets `peg:<row>,<k>`, `bin:<k>`, `slider:n`, `slider:p`, `path:steered`, `overlay:normal`, `overlay:binomial`; describe, e.g. "12 rows, p = 0.5. 500 balls dropped; counts 0, 2, 9, 28, 61, 97, 113, 95, ... Overlays: binomial."; tryable `slider:n`, `slider:p`.
- **Accessibility** Table view: bin, count, expected count. Steering uses named buttons. After each batch: "500 balls, 12 rows, p = 0.5. Most in bin 6 (113)."
- **Reduced motion** No bouncing; counts increment.

#### 5.12.14 `convolver`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.2.4 · first use 1.5 L68

Discrete: $P(X + Y = s)$ is the sum along one anti-diagonal of the joint grid.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `outcome-grid`, `live-formula`; mark types `stems`, `curve`, `region`, `hist`.
- **Config** `ConvolverConfig { mode, X, Y?, range, nMax?, standardise?, trace? }`.
- **Answers** `numeric`, `curve`, `choice`, `expression`.
- **AI hooks** targets `handle:s`, `curve:fx`, `curve:fy-flipped`, `region:overlap`, `curve:result`, `diag:<s>`, `slider:n`; describe, e.g. "Flip and slide: X, Y uniform(0, 1). s = 1.4: overlap 0.6. Traced from 0 to 1.4."; tryable `slider:n`.
- **Accessibility** Table view of $s$ against $P(X + Y = s)$ or $f(s)$ on a grid; the overlap value announced on commit.
- **Reduced motion** Jumps.

#### 5.12.15 `sampling-lab`

composite · tier composite · cluster `probability` · **P0** · size L · spec prob-stats 6.3.2 · first use 1.5 L69

The picture under all of statistics.

- **Composes** `plot-2d`, `marks`, `sim-runner`, `slider`, `choice`, `chance-object`, `mass-editor`, `drag-point`, `qq-plot`; mark types `curve`, `hist`, `rug`, `band`.
- **Config** `SamplingLabConfig { mode, population, n, statistic, batches, overlays?, standardise?, groups?, test?, predictFirst? }`.
- **Answers** `numeric`, `point`, `interval`, `choice`, `state`.
- **AI hooks** targets `panel:population`, `panel:sample`, `panel:stat`, `dot:<i>`, `stat:last`, `hist:stat`, `curve:normal`, `curve:t`, `line:truth`, `bracket:prediction`, `slider:n`, `chip:<statistic>`; describe, e.g. "Mode CLT. Population: exponential(1). n = 5. 1,000 means drawn; standardised; normal overlay on. Prediction bracket SD 0.40."; secret: the exact standard error and the truth; tryable `slider:n`, `chip:<statistic>`.
- **Accessibility** "Population exponential, mean 1. n = 30. 1,000 sample means: mean 1.003, SD 0.181; theory 0.183." Table views for each panel's histogram.
- **Reduced motion** Results appear at once.
- **Modes added** `predict-se`, correlated population `correlated: { rho }` and `ecdf` view (P1, 1.6 L2 and L4, curriculum); several statistics side by side for `estimator-compare` (P1); Bootstrap rows never drawn are marked out-of-bag; the share converges to $1 - e^{-1}$ (P2, ML 5).
- Sampling, LLN, CLT and $t$ modes P0; bootstrap, permutation and p-value modes P1.

#### 5.12.16 `generating-function`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.2.7 · first use 1.5 L78

$M_X(t) = E[e^{tX}]$: the slope at $t = 0$ is $E[X]$ and the second derivative is $E[X^2]$; the Taylor coefficients are $E[X^k]/k!$.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `live-formula`, `taylor-builder`, `iteration-cobweb`, `choice`; mark types `curve`.
- **Config** `GeneratingFunctionConfig { kind, family, params, show, combine?, tRange?, offspring? }`.
- **Answers** `numeric`, `expression`, `choice`, `distribution`.
- **AI hooks** targets `curve:m`, `handle:t`, `tangent`, `parabola`, `term:<k>`, `curve:product`, `cobweb`, `iterate:<k>`; describe, e.g. "MGF of Poisson(2). Tangent at 0: slope 2.00. Curvature toggle on."
- **Accessibility** Table of $t$ against $M(t)$; readouts announce "slope at zero 2, so E of X is 2".
- **Reduced motion** Steps jump.

#### 5.12.17 `order-statistics`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.3.1 · first use 1.5 L83

For $n$ uniforms, the sorted values cut $[0, 1]$ into $n + 1$ pieces of equal expected length, so $E[U_{(k)}] = \frac{k}{n+1}$ and $U_{(k)} \sim \text{Beta}(k, n - k + 1)$.

- **Composes** `number-line`, `sim-runner`, `marks`, `slider`, `drag-point`, `choice`; mark types `hist`, `curve`.
- **Config** `OrderStatisticsConfig { base, n, k, editable, show, predictFirst? }`.
- **Answers** `numeric`, `point`, `expression`, `choice`.
- **AI hooks** targets `dot:<i>`, `kth`, `spacing:<i>`, `hist`, `curve:beta`, `slider:n`, `slider:k`, `marker:prediction`; describe, e.g. "Uniform, n = 5, k = 5. Last sample sorted: 0.11, 0.38, 0.52, 0.70, 0.93. 1,000 samples: mean of U(5) 0.834."; tryable `slider:n`, `slider:k`.
- **Accessibility** The sample is listed in sorted order; histogram table view; "1,000 samples of 5: mean of the maximum 0.834, Beta(5, 1) mean 0.833".
- **Reduced motion** Instant.

#### 5.12.18 `joint-density`

composite · tier composite · cluster `probability` · **P0** · size L · spec prob-stats 6.3.3 · first use 1.5 L88

Integrate out to get a marginal (the heatmap squashes onto an axis); slice at $X = x$ and renormalise to get $f_{Y \mid X}(y \mid x)$; test independence by asking whether every slice has the same shape.

- **Composes** `plot-2d`, `plot-3d`, `marks`, `drag-point`, `region-select`, `slider`, `region-bounds`, `contingency-table`; mark types `stems`, `curve`, `region`.
- **Config** `JointDensityConfig { joint, show, slice?, regions?, task? }`.
- **Answers** `numeric`, `choice`, `curve`, `expression`, `set`.
- **AI hooks** targets `heat`, `contours`, `slice`, `panel:conditional`, `panel:marginal-x`, `panel:marginal-y`, `region:<id>`, `support`; describe, e.g. "Density f(x, y) = x + y on the unit square. Slice at x = 0.25: conditional density (0.25 + y)/0.75. Region X < Y: 0.5 shown."; secret: region probabilities and marginal formulas.
- **Accessibility** Discrete: the table view is a `contingency-table`. Continuous: a description of the support, the mode and the correlation, a values table on a $9 \times 9$ grid, and a slice table.
- **Reduced motion** Before-and-after.

#### 5.12.19 `geo-prob`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.4.1 · first use 1.5 L92

Two independent uniforms are one uniform point in the unit square, so any event about them is a region and its probability is its area.

- **Composes** `plot-2d`, `region-select`, `drag-point`, `marks`, `slider`, `sim-runner`, `expression-input`, `numeric-input`; mark types `region`, `curve`.
- **Config** `GeoProbConfig { space, story?, constraints?, editable, params?, darts?, task? }`.
- **Answers** `numeric`, `set`, `expression`, `state`.
- **AI hooks** targets `region`, `constraint:<i>`, `boundary:<i>`, `point:sample`, `inset`, `darts`, `slider:<param>`, `cell:<id>`; describe, e.g. "Broken stick. Point (0.30, 0.70): triangle yes. Region built: x < 0.5, y > 0.5, y - x < 0.5 (area 0.125). Darts: none."; secret: target region and area; tryable `slider:<param>`.
- **Accessibility** The region is described as inequalities with its area; the point announces both views ("X 0.30, Y 0.70: pieces 0.30, 0.40, 0.30, a triangle"); darts summarised as counts.
- **Reduced motion** Darts appear at once.
- **Modes added** circle mode (P0, 1.5 L148, curriculum).

#### 5.12.20 `covariance-lab`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.3.4 · first use 1.5 L94

For each point, the rectangle from $(\bar x, \bar y)$ to the point has signed area $(x_i - \bar x)(y_i - \bar y)$; covariance is their average.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `numeric-input`, `sim-runner`; mark types `rect-signed`.
- **Config** `CovarianceLabConfig { data, movable, show, task? }`.
- **Answers** `numeric`, `choice`, `state`, `set`.
- **AI hooks** targets `point:<i>`, `rect:<i>`, `mean:x`, `mean:y`, `readout:r`, `readout:cov`; describe, e.g. "20 points. Covariance 1.80, r 0.62. Rectangles on. Guess entered: none."; secret: the target $r$ in the guessing game.
- **Accessibility** Table view with columns $x$, $y$, deviations and their product; "n = 20, covariance 1.8, r = 0.62; 14 positive rectangles, 6 negative".
- **Reduced motion** no motion of its own.
- Anscombe preset P1.

#### 5.12.21 `gaussian-2d`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.3.5 · first use 1.5 L96

Set $\sigma_X$, $\sigma_Y$ and $\rho$ and see the 1- and 2-standard-deviation ellipses.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `matrix`, `quadratic-form`, `transform-grid`, `sim-runner`; mark types `ellipse`, `band`, `curve`, `hist`.
- **Config** `Gaussian2DConfig { mu, sigma, rho, editable, mode, samples?, assetLabels? }`.
- **Answers** `numeric`, `point`, `choice`.
- **AI hooks** targets `handle:sx`, `handle:sy`, `handle:rho`, `ellipse:1`, `ellipse:2`, `line:regression`, `line:major-axis`, `slice`, `band:conditional`, `handle:w`, `shadow`, `curve:portfolio` and 1 more; describe, e.g. "σx 1, σy 1, ρ 0.6. Slice at x = 1.5: conditional mean 0.9, SD 0.8. Mode: conditional."
- **Accessibility** Table of $\Sigma$, conditional parameters and portfolio points; "Correlation 0.6. At x = 1, Y has mean 0.6 and SD 0.8."
- **Reduced motion** Static highlights; before-and-after for the flip.

#### 5.12.22 `cond-expectation`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.3.6 · first use 1.5 L106

Group $Y$ by slices of $X$ and average each: that function of $X$ is $E[Y \mid X]$.

- **Composes** `plot-2d`, `marks`, `region-select`, `drag-point`, `stepper`, `filtration-tree`, `live-formula`.
- **Config** `CondExpectationConfig { data, bins?, show, task? }`.
- **Answers** `numeric`, `state`, `expression`, `choice`.
- **AI hooks** targets `slice:<k>`, `handle:pred:<k>`, `mean:<k>`, `point:<i>`, `bar:within`, `bar:between`, `readout:mse`; describe, e.g. "8 slices. Predictions set: 8 of 8. MSE 2.41 (slice means 2.07). Collapsed: no."; secret: the slice means.
- **Accessibility** Table view: slice range, count, mean, variance; "Your predictions: mean squared error 2.41; slice means give 2.07".
- **Reduced motion** Before-and-after.

#### 5.12.23 `filtration-tree`

composite · tier composite · cluster `probability` · **P0** · size M · spec calc-linalg 7.9 · first use 1.5 L108

Information as partitions of the outcomes; $E[X\mid\mathcal F_n]$ as the average over each atom; the tower property; martingales; adapted processes; stopping times.

- **Composes** `marks`, `region-select`, `numeric-input`, `choice`, `stepper`, `live-formula`.
- **Config** `FiltrationTreeConfig { p, X, ask, n?, tau? }`.
- **Answers** `numeric`, `choice`, `set`, `state`.
- **AI hooks** targets `node:<path>`, `atom:<n>:<id>`, `leaf:<outcome>`, `entry:<atom>`, `step:<n>`.
- **Accessibility** Outcomes as a table with columns for each $\mathcal F_n$ atom.
- **Reduced motion** Splits jump.
- **Modes added** `radon-nikodym` mode (P2, 3.2 L10 to L13, curriculum).
- Conditional-expectation and tower modes moved from P2 to P0 (prob-stats 5; 1.5 L108).
- Cluster `probability` for its P0 modes.

#### 5.12.24 `markov-chain`

composite · tier composite · cluster `probability` · **P0** · size L · spec prob-stats 6.4.4 · first use 1.5 L123

Every row of $P$ is "where next from here".

- **Composes** `node-link`, `matrix`, `mass-editor`, `sim-runner`, `marks`, `stepper`, `region-select`, `linear-dynamics`, `eigen-finder`, `first-step-solver`.
- **Config** `MarkovChainConfig { states, P, editable, views, nMax, alpha?, task? }`.
- **Answers** `matrix`, `numeric`, `state`, `choice`.
- **AI hooks** targets `node:<id>`, `edge:<a>-<b>`, `cell:<i>,<j>`, `row:<i>`, `walker`, `bar:<id>`, `class:<k>`, `pi:<id>`, `slider:alpha`, `step`; describe, e.g. "3 states. P rows: A (0.9, 0.1, 0), B (0.5, 0, 0.5), C (0, 0.5, 0.5). π10 = (0.71, 0.14, 0.15). Walker at B after 57 steps."; secret: $\pi$ and the classes; tryable `slider:alpha`.
- **Accessibility** The matrix is the table view; each state is described with its outgoing row and current probability; "Walker at B after 57 steps; visits A 40, B 9, C 8".
- **Reduced motion** Jumps; Play steps without interpolation.
- **Modes added** Metropolis mode (P0, moved from P2; 1.5 L134, curriculum); run-length preset (P0, 1.5 L155, curriculum); `ctmc` mode with competing exponential clocks, the 3.2 `ctmc-clock` request (P2, 3.2, curriculum).

#### 5.12.25 `lattice-walk`

composite · tier composite · cluster `probability` · **P0** · size M · spec prob-stats 6.4.5 · first use 1.5 L135

A path of $n$ steps ending at $k$ is a choice of which $\frac{n+k}{2}$ steps go up, so there are $\binom{n}{(n+k)/2}$ of them.

- **Composes** `plot-2d`, `marks`, `drag-point`, `stepper`, `sim-runner`, `pascal-triangle`, `path-simulator`.
- **Config** `LatticeWalkConfig { n, start, endpoint?, barrier?, mode, simulate? }`.
- **Answers** `numeric`, `expression`, `state`, `choice`.
- **AI hooks** targets `path`, `step:<i>`, `endpoint`, `barrier`, `touch`, `path:reflected`, `count`; describe, e.g. "n = 6, start 0, endpoint (6, 2). Barrier at −1. Learner path U U D U D U touches the barrier: no."; secret: counts asked for.
- **Accessibility** The path reads as "up, up, down, up"; counts table; "Paths from 0 to 2 in 6 steps: 15; touching minus 1: 6".
- **Reduced motion** Before-and-after.

#### 5.12.26 `kelly-lab`

composite · tier composite · cluster `probability` · **P0** · size M · spec finance 8.3 · first use 1.5 L154 (through `game-lab`)

A favourable bet can still ruin you if you bet too much.

- **Composes** `plot-2d`, `drag-point`, `slider`, `sim-runner`, `mass-editor`, `marks`, `live-formula`, `numeric-input`, `choice`, `convexity-chord`.
- **Config** `KellyLabConfig { mode, bet?, outcomes?, bets?, continuous?, sim, pRange? }`.
- **Answers** `numeric`, `point`, `choice`, `state`.
- **AI hooks** targets `handle:f`, `curve:growth`, `peak`, `fan`, `line:median`, `line:ruin`, `slider:<param>`, `stake:<k>`; tryable `slider:<param>`.
- **Accessibility** "p 0.55, even odds: Kelly fraction 0.10; at 0.10 the growth rate is 0.50% a bet; at 0.20 it is about zero (−0.01%)." Path quantiles as a table.
- **Reduced motion** Paths at once.
- P0 core (one repeated bet, the growth curve $g(f)$ and its peak) because `game-lab` embeds it at 1.5 L154; several outcomes, simultaneous bets, uncertain edge and the continuous version stay P2.
- Cluster `probability` for its P0 core.

### 5.13 Statistics (1.6)

#### 5.13.1 `regression-lab`

composite · tier composite · cluster `statistics` · **P1** · size L · spec prob-stats 7.6 · first use 1.7 L27

Everything about OLS that a summary table hides: residuals and the $SST = SSR + SSE$ decomposition behind $R^2$; the sampling distribution of $\hat\beta$ that standard errors describe; confidence against prediction bands.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `sim-runner`, `plot-3d`, `matrix`, `least-squares-fit`, `qq-plot`, `ci-ladder`, `summary-table`, `live-formula`; mark types `band`, `ellipse`, `stems`.
- **Config** `RegressionLabConfig { data, predictors, show, diagnostics?, editable, task? }`.
- **Answers** `numeric`, `interval`, `choice`, `state`, `code`, `point`.
- **AI hooks** targets `point:<i>`, `line:fit`, `residual:<i>`, `bar:sst`, `bar:ssr`, `bar:sse`, `band:ci`, `band:pi`, `panel:<tab>`, `slider:<id>`, `hist:slopes`, `plane`; secret: the true coefficients of generated data; tryable `slider:<id>`.
- **Accessibility** Table view of data, fitted values, residuals and hat values; "y on x, n = 50: intercept 1.02, slope 2.98, R squared 0.81, slope standard error 0.14".
- **Reduced motion** Before-and-after.
- **Modes added** `ar1` errors for 1.6 L56 (P1, curriculum); beta preset (P1, finance 5); prediction mode and HAC standard errors (Newey-West, Hansen-Hodrick), required for 3.1 (P2, ML 5); `glm` mode (P2, 2.1 L39, curriculum).

#### 5.13.2 `viva`

composite · tier composite · cluster `statistics` · **P1** · size M · spec ML 6.9.2 · first use 1.7 L45

Exit tests that say "explain without notes" need an examiner who follows up.

- **Composes** `free-response`, `live-formula`, `value-table`.
- **Config** `VivaConfig { bank, pick, timeLimitS?, maxFollowUps, noNotes, offline }`.
- **Answers** `long-form`.
- **AI hooks** targets `question:<k>`, `answer:<k>`, `followup:<k>`, `rubric:<point>`, `timer`.
- **Accessibility** The transcript is a log region; the timer announces at the half-way point and one minute before the end; timing can be extended or switched off before starting (WCAG 2.2 success criterion 2.2.1).
- **Reduced motion** Turns appear; the face is static.
- Input-like composite: Bertie asks, probes twice against a rubric and drafts a mark the learner confirms; first used at the 1.6 exit.

#### 5.13.3 `qq-plot`

composite · tier composite · cluster `statistics` · **P1** · size S · spec prob-stats 7.8 · first use 1.6 L8

A QQ plot pairs the $i$th smallest observation with the reference quantile at plotting position $p_i$.

- **Composes** `plot-2d`, `marks`, `token-tray`, `dist-explorer`, `slider`, `sim-runner`.
- **Config** `QqPlotConfig { data, reference, mode, positions, envelope? }`.
- **Answers** `choice`, `mapping`, `numeric`.
- **AI hooks** targets `point:<i>`, `line:reference`, `band:envelope`, `slot:<i>`.
- **Accessibility** Table: rank, observation, plotting position, reference quantile; a sentence describing departures ("points rise above the line at the right end: heavier right tail").
- **Reduced motion** Instant.

#### 5.13.4 `likelihood-lab`

composite · tier composite · cluster `statistics` · **P1** · size M · spec prob-stats 7.2 · first use 1.6 L11

Fix the data and move $\theta$: the model density slides over the data, each point's density height changes, and their product (or the sum of their logs) is $L(\theta)$, plotted in a second panel.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `surface-explorer`, `live-formula`, `derivation-steps`; mark types `rug`, `curve`, `stems`.
- **Config** `LikelihoodLabConfig { model, data, params, show, task? }`.
- **Answers** `numeric`, `point`, `expression`, `interval`, `choice`.
- **AI hooks** targets `handle:theta`, `curve:loglik`, `curve:model`, `stem:<i>`, `readout:loglik`, `parabola`, `cut`, `contour`; describe, e.g. "Bernoulli, 7 heads in 10. θ = 0.55: log-likelihood −6.27. Log scale on."; secret: the MLE.
- **Accessibility** Table view of $\theta$ on a grid against $\ell(\theta)$; data list; "theta 0.4: log-likelihood −6.73".
- **Reduced motion** Before-and-after.
- **Modes added** `logistic` and `exponential-censored` models (P1, 1.6 L65 and ES3 homework, curriculum).

#### 5.13.5 `ci-ladder`

composite · tier composite · cluster `statistics` · **P1** · size M · spec prob-stats 7.3 · first use 1.6 L21

"95%" describes the method: about 95 of 100 intervals built this way cover $\mu$.

- **Composes** `sim-runner`, `marks`, `slider`, `choice`, `number-line`, `dist-explorer`, `live-formula`; mark types `intervals`.
- **Config** `CiLadderConfig { model, methods, n, level, truth, hideTruth?, show, predictFirst? }`.
- **Answers** `numeric`, `interval`, `choice`.
- **AI hooks** targets `interval:<i>`, `line:truth`, `counter`, `curve:coverage`, `slider:n`, `slider:level`, `method:<id>`; describe, e.g. "Normal mean, t at 95%, n = 10. 100 run, 94 cover. Truth hidden."; secret: the truth; tryable `slider:n`, `slider:level`.
- **Accessibility** Table of the latest intervals; "100 intervals, 95% t, n = 10: 94 cover the truth".
- **Reduced motion** The ladder updates at once.
- **Modes added** `variance` model (P1, 1.6 L24, curriculum).

#### 5.13.6 `test-lab`

composite · tier composite · cluster `statistics` · **P1** · size M · spec prob-stats 7.4 · first use 1.6 L26

A test is a rule: reject when the statistic lands in a region chosen to have probability $\alpha$ under the null.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `choice`, `dist-explorer`, `sim-runner`, `live-formula`; mark types `curve`, `region`.
- **Config** `TestLabConfig { test, null, alt?, alpha, sided, editable, data?, show, simulatedNull? }`.
- **Answers** `numeric`, `interval`, `point`, `choice`.
- **AI hooks** targets `curve:null`, `curve:alt`, `region:alpha`, `region:beta`, `handle:crit-left`, `handle:crit-right`, `marker:observed`, `region:p`, `curve:power`, `slider:<id>`; secret: the p-value and decision asked for; tryable `slider:<id>`.
- **Accessibility** "Two-sided z test at 0.05: reject when the absolute value of z exceeds 1.96. Effect 0.5, n 25: power 0.71. Observed z 2.31, p 0.021."
- **Reduced motion** Before-and-after.
- **Modes added** `ks` test (P1, 1.6 L34, curriculum); compact ADF readout embeddable in `fracdiff-lab` (P2, ML 5).
- Simulated Dickey-Fuller null P2.

#### 5.13.7 `multiple-testing`

composite · tier composite · cluster `statistics` · **P1** · size M · spec prob-stats 7.5 · first use 1.6 L38

Run $m$ tests at 5% and some will reject by chance: $P(\text{at least one}) = 1 - 0.95^m$.

- **Composes** `icon-array`, `marks`, `drag-point`, `slider`, `contingency-table`, `sim-runner`; mark types `stems`.
- **Config** `MultipleTestingConfig { m, pi1, effect, alpha, methods, mode, pValues?, zoo?, hideTruth? }`.
- **Answers** `numeric`, `set`, `choice`.
- **AI hooks** targets `cell:<i>`, `line:bh`, `line:bonferroni`, `stem:<rank>`, `table:outcomes`, `point:best`, `slider:<id>`; describe, e.g. "m = 100, 10 real, BH at q = 0.1: 12 discoveries. Truth hidden."; secret: which hypotheses are real; tryable `slider:<id>`.
- **Accessibility** Sorted p-value table with each method's decision; "20 tests, none real: 1 rejected at 5% with no correction".
- **Reduced motion** Instant.
- **Modes added** `forking` mode for 1.6 L41 (P1, curriculum); $t$ axis, BHY, `zoo-timeline` (P2, ML 5); The strategy zoo draws its noise strategies from `backtest-core` and links to `sharpe-lab`'s deflated Sharpe (P2, finance 5).
- Its strategy-zoo mode embeds `overfit-lab`'s zoo panel (ML decision 6).

#### 5.13.8 `summary-table`

composite · tier composite · cluster `statistics` · **P1** · size M · spec prob-stats 7.7 · first use 1.6 L45

The 1.6 exit test: fit a regression in NumPy, match statsmodels, and explain every number.

- **Composes** `value-table`, `live-formula`, `regression-lab`, `dist-explorer`, `qq-plot`, `marks`, `numeric-input`, `free-response`, `code-cell`.
- **Config** `SummaryTableConfig { data, covType, hidden?, toggles?, fixture? }`.
- **Answers** `numeric`, `choice`, `long-form`, `code`.
- **AI hooks** targets `cell:<field>`, `cell:r-squared`, `cell:coef:x1`, `cell:se:x1`, `cell:dw`, `card`, `plot:<id>`; describe, e.g. "OLS, y on x1 and x2, n = 50. Selected: std err of x1 (0.141). Blanked: t of x1, Adj. R-squared. Toggles: none."; secret: blanked values.
- **Accessibility** A real table with headers; each value a button named "R-squared, 0.812"; cards are regions with headings.
- **Reduced motion** Instant.
- **Modes added** HAC covariance type (P2, ML 5).
- Recomputed in JavaScript; real statsmodels only in code drills; every number is a button that explains itself (prob-stats decision 10).

#### 5.13.9 `posterior-lab`

composite · tier composite · cluster `statistics` · **P1** · size M · spec prob-stats 7.9 · first use 1.6 L70

Shape a prior over $\theta$ (bars on a grid, or a Beta curve), observe data, multiply by the likelihood point by point and renormalise.

- **Composes** `plot-2d`, `mass-editor`, `marks`, `slider`, `chance-object`, `sim-runner`, `number-line`, `live-formula`; mark types `curve`, `stems`, `intervals`.
- **Config** `PosteriorLabConfig { model, prior, data?, editable, show, groups?, task? }`.
- **Answers** `numeric`, `interval`, `distribution`, `expression`, `choice`.
- **AI hooks** targets `curve:prior`, `curve:likelihood`, `curve:posterior`, `bar:<theta>`, `bracket:interval`, `slider:alpha`, `slider:beta`, `flip`, `group:<i>`, `slider:strength`; secret: requested posterior quantities; tryable `slider:alpha`, `slider:beta`, `slider:strength`.
- **Accessibility** Grid table: $\theta$, prior, likelihood, posterior; "Posterior Beta(9, 5): mean 0.643; 95% interval 0.39 to 0.86".
- **Reduced motion** Stages swap without interpolation.
- **Modes added** MAP mode in coefficient space: a Gaussian prior's circular contours against the ridge disc, a Laplace prior's diamonds (P2, ML 5).

### 5.14 Finance basics (1.7)

#### 5.14.1 `compounding-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.1.1 · first use 1.7 L1

Make "interest on interest" a visible layer, show that compounding more often has a ceiling ($e^r - 1$), and make conventions explicit before any market quotes a rate.

- **Composes** `plot-2d`, `marks`, `slider`, `drag-point`, `token-tray`, `live-formula`, `numeric-input`, `expression-input`, `multiplier-chain`.
- **Config** `CompoundingLabConfig { mode, principal, currency, rate, years, mValues?, inflation?, compare?, predictFirst? }`.
- **Answers** `numeric`, `expression`, `ordering`, `point`.
- **AI hooks** targets `slider:rate`, `slider:years`, `slider:m`, `bar:<year>`, `layer:principal`, `layer:simple`, `layer:compound`, `curve:continuous`, `asymptote`, `handle:prediction`; describe, e.g. "Rate 5% annual, 10 years: 1,000 grows to 1,628.89; interest on interest 128.89."; tryable `slider:rate`, `slider:years`, `slider:m`.
- **Accessibility** Table view by year (principal, simple interest, compound interest, balance); slider values announced on commit ("5%, annual, 10 years: balance 1,628.89 pounds").
- **Reduced motion** Splits appear at once.

#### 5.14.2 `tvm-timeline`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.1.2 · first use 1.7 L1

One picture for every discounting idea: a cash flow shrinks as it slides back in time; NPV is the sum of the ghosts; the IRR is where the NPV curve crosses zero.

- **Composes** `cashflow-timeline`, `plot-2d`, `drag-point`, `slider`, `value-table`, `live-formula`, `numeric-input`, `expression-input`, `series-explorer`.
- **Config** `TvmTimelineConfig { mode, timeline, rate, loan?, growth?, showNpvCurve }`.
- **Answers** `numeric`, `expression`, `point`, `curve`.
- **AI hooks** targets `flow:<id>`, `curve:npv`, `handle:rate`, `irr:<n>`, `bar:<k>`, `knot:<t>`, `control:shift`; describe, e.g. "5 flows: pay 1,000 at 0, receive 300 at years 1 to 4. At 8%: NPV −6.36; IRR 7.71%."; tryable `control:shift`.
- **Accessibility** Table view: $t$, flow, discount factor, present value, cumulative; the NPV curve's table by rate.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.3 `bond-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.3.1 · first use 1.7 L7

Tie every bond number to arrows on a timeline, so "price falls when yields rise" is seen as every arrow's present value shrinking at once.

- **Composes** `cashflow-timeline`, `plot-2d`, `drag-point`, `slider`, `live-formula`, `numeric-input`, `value-table`.
- **Config** `BondLabConfig { mode, face, coupon, freq, maturity, yield, quote?, dayCount?, dates?, credit? }`.
- **Answers** `numeric`, `choice`, `curve`.
- **AI hooks** targets `flow:<k>`, `curve:price-yield`, `handle:yield`, `line:quote`, `line:par`, `series:dirty`, `series:clean`, `slider:hazard`; tryable `slider:hazard`.
- **Accessibility** "5-year 4% annual bond at 5% yield: price 95.67, discount." Table of flows with discount factors.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** `bootstrap-exam` timed variant without knot handles (P1, curriculum).

#### 5.14.4 `yield-curve-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.3.2 · first use 1.7 L10

One curve prices every safe cash flow; bootstrapping recovers it from bonds one maturity at a time; forwards are what today's curve locks in.

- **Composes** `plot-2d`, `drag-point`, `cashflow-timeline`, `slider`, `value-table`, `live-formula`, `numeric-input`.
- **Config** `YieldCurveLabConfig { mode, convention, curve, bonds?, swap?, portfolio? }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `knot:<t>`, `row:<bond>`, `entry:<t>`, `route:a`, `route:b`, `lane:fixed`, `lane:float`, `slider:shift`, `slider:twist`; tryable `slider:shift`, `slider:twist`.
- **Accessibility** Table of maturity, discount factor, zero rate and forward rate.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.5 `duration-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.3.3 · first use 1.7 L13

Make duration a physical balance point before it becomes a derivative, then show the tangent and the curvature on the price-yield curve.

- **Composes** `cashflow-timeline`, `plot-2d`, `drag-point`, `slider`, `live-formula`, `numeric-input`, `choice`.
- **Config** `DurationLabConfig { mode, bonds, yield, liability?, shockRange? }`.
- **Answers** `numeric`, `choice`, `state`.
- **AI hooks** targets `fulcrum`, `block:<t>`, `beam`, `curve:price-yield`, `line:tangent`, `curve:quadratic`, `slider:shock`, `bond:<id>`; tryable `slider:shock`.
- **Accessibility** "Fulcrum at 4.40 years; beam tips right; balance point is later." Table of $t$, PV and $t \times PV$.
- **Reduced motion** The beam shows its final angle at once.

#### 5.14.6 `share-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.2.1 · first use 1.7 L17

Ground equity in a company's balance: a share is a slice; paying a dividend moves cash from the company to its owners without creating wealth; a split relabels slices.

- **Composes** `marks`, `plot-2d`, `slider`, `stepper`, `region-select`, `value-table`, `numeric-input`, `drawdown-lab`; mark types `event-rug`.
- **Config** `ShareLabConfig { mode, company, holder?, events?, history?, index? }`.
- **Answers** `numeric`, `set`, `choice`.
- **AI hooks** targets `tile:<k>`, `band:cash`, `band:ops`, `wallet`, `event:<date>`, `series:raw`, `series:adjusted`, `index:price-weighted`, `index:cap-weighted`, `divisor`.
- **Accessibility** "Company value 500 million: cash 50 million, operations 450 million; 10 million shares at 50." Table view of history with raw, factor and adjusted columns.
- **Reduced motion** Cash moves at once.

#### 5.14.7 `margin-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.2.2 · first use 1.7 L22

Show, as a balance sheet that moves with the price, why borrowing scales returns in both directions and exactly where the broker calls.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `sim-runner`, `value-table`, `numeric-input`, `choice`.
- **Config** `MarginLabConfig { mode, qty, entry, initialMargin, maintenance, feeRate?, path? }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `handle:price`, `bar:assets`, `bar:loan`, `bar:equity`, `line:maintenance`, `line:long`, `line:short`, `meter:ratio`.
- **Accessibility** "Price 80: assets 8,000, loan 5,000, equity 3,000, margin ratio 37.5%, maintenance 25%."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.8 `portfolio-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.2.3 · first use 1.7 L24

The mean-variance picture in the $(\sigma, \mu)$ plane, manipulated directly: correlation bends the curve; a risk-free asset turns the frontier into a line; beta is a slope.

- **Composes** `plot-2d`, `drag-point`, `slider`, `mass-editor`, `marks`, `live-formula`, `numeric-input`, `regression-lab`, `lagrange-explorer`.
- **Config** `PortfolioLabConfig { mode, assets, corr, rf?, shortSelling, cloud?, beta? }`.
- **Answers** `point`, `numeric`, `choice`, `state`.
- **AI hooks** targets `asset:<id>`, `handle:portfolio`, `curve:frontier`, `line:cml`, `point:tangency`, `point:min-var`, `slider:rho`, `line:beta`, `cloud`; tryable `slider:rho`.
- **Accessibility** "Weight in A 0.62: volatility 13.1%, expected return 7.2%, Sharpe 0.40." Table view of the curve by weight.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.9 `order-book`

composite · tier composite · cluster `finance` · **P1** · size L · spec finance 6.4.1 · first use 1.7 L29

Let the learner be a participant: place orders, watch them rest in queues, send orders that cross the spread, and see exactly which resting orders fill at what prices.

- **Composes** `price-ladder`, `order-ticket`, `quote-entry`, `plot-2d`, `marks`, `value-table`, `stepper`, `sim-runner`, `token-tray`, `numeric-input`, `choice`; mark types `depth`.
- **Config** `OrderBookConfig { mode, tick, lot, book, queues?, order?, flow?, fees?, amendRule, predictFirst?, show }`.
- **Answers** `numeric`, `ordering`, `set`, `choice`.
- **AI hooks** targets `ticket:*`, `depth`, `microprice`, `fill:<n>`, `queue:<tick>:<k>`, `race:result`; describe, e.g. "Best bid 99.98 (300), best ask 100.01 (200), spread 0.03. Staged: market buy 500. No fills yet."; secret: in race mode, the future flow and the fill outcome.
- **Accessibility** Ladder grid semantics; fills announced; the depth chart has a table view; race results as a table.
- **Reduced motion** Fills appear at once with a fill list; replays step.
- **Modes added** `sequence` replay of a scripted order list (P1, MK1 homework, curriculum).
- Fills come only from the shared `exchange-sim` (finance decision 2).

#### 5.14.10 `auction-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.4.2 · first use 1.7 L35

Show that a call auction is one price for everyone, chosen where the cumulative demand and supply curves cross, and that your own order moves the indicative price.

- **Composes** `price-ladder`, `plot-2d`, `marks`, `drag-point`, `order-ticket`, `value-table`, `numeric-input`, `choice`.
- **Config** `AuctionLabConfig { tick, lot, orders, tieBreak, referencePrice?, allowOwnOrder }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `handle:candidate`, `curve:demand`, `curve:supply`, `bar:<tick>`, `order:<id>`.
- **Accessibility** Table by price: cumulative demand, cumulative supply, executable volume, imbalance.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.11 `tape-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.8.1 · first use 1.7 L40

The spread a trader really pays is measured from trades, and trades bounce between bid and ask; Roll turns that bounce into a spread estimate from prices alone.

- **Composes** `plot-2d`, `marks`, `value-table`, `region-select`, `numeric-input`, `choice`; mark types `quote-band`, `trade-glyphs`.
- **Config** `TapeLabConfig { mode, tape, rule, horizon? }`.
- **Answers** `set`, `numeric`, `choice`.
- **AI hooks** targets `trade:<n>`, `row:<n>`, `band`, `scatter`, `line:roll`; secret: the true initiator of every trade.
- **Accessibility** The tape is the table view; each row reads "10:00:03, 100.02, 300 shares; bid 100.00, ask 100.02."
- **Reduced motion** no motion of its own.

#### 5.14.12 `market-maker-sim`

composite · tier composite · cluster `finance` · **P1** · size L · spec finance 6.8.3, ML 7.5 · first use 1.7 L42

Turn the two spread theories into one running business with inventory risk, and prepare the 3.1 replication of Avellaneda and Stoikov.

- **Composes** `plot-2d`, `slider`, `quote-entry`, `price-ladder`, `sim-runner`, `marks`, `value-table`, `numeric-input`, `choice`, `drag-point`, `live-formula`; mark types `quote-band`, `waterfall`, `paths`, `step`, `hist`, `curve`.
- **Config** `MarketMakerSimConfig { mode, flow, policy, tick, showLadder, params, strategies, batch?, extensions?, editable }`.
- **Answers** `numeric`, `choice`, `point`, `ordering`, `code`, `curve`.
- **AI hooks** targets `slider:<param>`, `panel:mid`, `panel:inventory`, `panel:pnl`, `bar:<component>`, `fill:<n>`, `series:mid`, `series:r`, `series:bid`, `series:ask`, `fill:<i>`, `series:inventory` and 8 more; secret: the informed share and the value path; tryable `slider:<param>`, `toggle:<ext>`.
- **Accessibility** "Session 10 minutes: 214 fills; spread captured +312; adverse selection −198; inventory −41; fees −22; net +51." The blotter is the table view.
- **Reduced motion** The replay steps without interpolation.
- **Modes added** `glft` mode (P2, 3.1 L78, curriculum); play mode for 3.3 market-making practice (P2, ML 13.2).
- One market-maker widget: finance's `dealer-sim` (spread from noise flow, adverse selection, inventory skew, P&L decomposition, P1) and ML's Avellaneda-Stoikov replication (fill intensity, reservation price, optimal spread, blind spots, P2) were two specs of one model on one `exchange-sim`; the final id is the more descriptive one, `dealer-sim` is an alias.

#### 5.14.13 `adverse-selection`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.8.2 · first use 1.7 L43

The spread exists even for a dealer with no costs, because every trade might come from someone who knows more.

- **Composes** `number-line`, `slider`, `stepper`, `plot-2d`, `marks`, `value-table`, `live-formula`, `numeric-input`; mark types `quote-band`.
- **Config** `AdverseSelectionConfig { mode, VL, VH, prior, mu, trades?, tick }`.
- **Answers** `numeric`, `curve`.
- **AI hooks** targets `handle:bid`, `handle:ask`, `slider:mu`, `bar:belief`, `trade:<n>`, `row:<n>`; secret: the true value; tryable `slider:mu`.
- **Accessibility** "Values 90 or 110, belief 0.50, informed share 20%: break-even ask 102, bid 98."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.14 `execution-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.8.4 · first use 1.7 L44

Market against limit, scaled up: the faster you trade, the more you pay in impact; the slower, the more the price can wander.

- **Composes** `plot-2d`, `mass-editor`, `slider`, `marks`, `sim-runner`, `numeric-input`, `choice`, `drag-point`; mark types `waterfall`.
- **Config** `ExecutionLabConfig { mode, market, order, impact, seed? }`.
- **Answers** `numeric`, `choice`, `point`.
- **AI hooks** targets `slider:size`, `bucket:<k>`, `curve:volume`, `line:arrival`, `bar:<cost>`, `frontier`, `handle:lambda`; tryable `slider:size`.
- **Accessibility** "Buying 5% of daily volume over 1 hour: expected cost 18 bp (spread 2, impact 16)."
- **Reduced motion** Paths appear at once.
- Almgren-Chriss frontier mode P2.

#### 5.14.15 `payoff-builder`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.6.1 · first use 1.7 L46

The central options canvas.

- **Composes** `plot-2d`, `marks`, `position-editor`, `drag-point`, `slider`, `sketch-pad`, `live-formula`, `numeric-input`, `choice`; mark types `payoff`, `signed-fill`.
- **Config** `PayoffBuilderConfig { mode, editor, initial?, target?, range, model?, show }`.
- **Answers** `numeric`, `choice`, `curve`.
- **AI hooks** targets `leg:<id>`, `handle:K:<id>`, `curve:total`, `curve:leg:<id>`, `kink:<K>`, `breakeven:<n>`, `probe`, `target`; secret: in match mode, one minimal solution.
- **Accessibility** "Long call 95, short 2 calls 100, long call 105: payoff 0 below 95, rising to 5 at 100, back to 0 at 105 and above. Net premium 0.62 paid. Break-evens 95.62 and 104.38." Table view at each kink.
- **Reduced motion** A before-and-after pair for `sum-legs`.
- Not used in Stage 0 (number-algebra decision 16) or 1.1 (python-tools decision 19); first use 1.7 L46.

#### 5.14.16 `carry-arb`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.5.1 · first use 1.7 L47

Derive the forward price by building the trade that would profit if it were wrong.

- **Composes** `cashflow-timeline`, `position-editor`, `slider`, `live-formula`, `derivation-steps`, `numeric-input`, `choice`.
- **Config** `CarryArbConfig { mode, S0, T, r, q?, rf?, income?, storage?, convenience?, quoteF, K?, lockedLegs? }`.
- **Answers** `numeric`, `expression`, `choice`, `state`.
- **AI hooks** targets `lane:<id>`, `flow:<id>`, `net:0`, `net:T`, `handle:F`, `marker:fair`, `leg:<id>`; secret: the fair forward.
- **Accessibility** "Borrow lane: receive 100 today, pay 105.13 at 1 year. Asset lane: pay 100 today, deliver the asset. Forward lane: receive 107 at 1 year. Net today 0; net at 1 year +1.87."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.17 `futures-mtm`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.5.2 · first use 1.7 L50

Futures P&L arrives every day; the learner keeps the margin account by hand until the pattern is obvious, then sees basis converge at expiry.

- **Composes** `plot-2d`, `value-table`, `drag-point`, `slider`, `numeric-input`, `choice`.
- **Config** `FuturesMtmConfig { mode, contract, initialMargin, maintenanceMargin, path, spot?, term?, position, contracts, fill }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `cell:<day>:<col>`, `line:balance`, `line:maintenance`, `line:initial`, `marker:call:<day>`, `cursor:day`.
- **Accessibility** The ledger is the table view; calls announced ("Day 4: balance 3,400 below maintenance 4,000; call 2,600 to restore 6,000").
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.18 `hedge-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.5.3 · first use 1.7 L52

The best hedge ratio is a regression slope, not 1; what remains after hedging is the part of the risk the future cannot explain.

- **Composes** `plot-2d`, `drag-point`, `slider`, `marks`, `position-editor`, `live-formula`, `numeric-input`, `choice`.
- **Config** `HedgeLabConfig { mode, sigmaS, sigmaF, rho, sample?, exposure?, beta? }`.
- **Answers** `numeric`, `point`, `choice`, `state`.
- **AI hooks** targets `handle:h`, `scatter`, `curve:variance`, `hist:hedged`, `slider:rho`; secret: $h^*$; tryable `slider:rho`.
- **Accessibility** "Hedge ratio 0.80 with correlation 0.9: hedged standard deviation 0.87% against 2.00% unhedged."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.19 `option-chain`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.6.4 · first use 1.7 L54

Real option data arrive as a table with traps: the last price can be hours old, wide quotes are not prices, and illiquid strikes distort a surface.

- **Composes** `value-table`, `region-select`, `plot-2d`, `marks`, `numeric-input`, `choice`.
- **Config** `OptionChainConfig { mode, chain, columns }`.
- **Answers** `numeric`, `set`, `choice`.
- **AI hooks** targets `cell:<K>:<call|put>:<field>`, `strike:<K>`, `expiry:<id>`, `plot:parity`, `line:fit`; secret: the planted defects.
- **Accessibility** The chain is a grid; each cell reads "Call, strike 105, bid 2.10, ask 2.30, last 1.85 at 10:02."
- **Reduced motion** no motion of its own.
- Read and parity modes P1; clean and smile modes P2.

#### 5.14.20 `option-bounds`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.6.2 · first use 1.7 L58

Before any model, prices must lie in a region; outside it, a trade makes money in every state.

- **Composes** `plot-2d`, `drag-point`, `position-editor`, `marks`, `live-formula`, `numeric-input`, `choice`.
- **Config** `OptionBoundsConfig { mode, S0, r, T, K?, quotes, predictFirst }`.
- **Answers** `choice`, `numeric`, `set`, `state`.
- **AI hooks** targets `handle:quote:<id>`, `bound:lower`, `bound:upper`, `intrinsic`, `chord:<K1>-<K3>`, `leg:<id>`; secret: whether each quote is admissible.
- **Accessibility** "Call quoted 3.00; lower bound 4.88; outside the region by 1.88."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.21 `parity-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.6.3 · first use 1.7 L60

Parity is not a formula to memorise; it is the observation that a call plus a bond and a put plus a share pay the same in every state, so they cost the same.

- **Composes** `payoff-builder`, `position-editor`, `cashflow-timeline`, `derivation-steps`, `slider`, `value-table`, `live-formula`, `numeric-input`.
- **Config** `ParityLabConfig { mode, S0, K, r, T, q?, quotes?, derivation?, style }`.
- **Answers** `expression`, `numeric`, `ordering`, `state`.
- **AI hooks** targets `portfolio:A`, `portfolio:B`, `probe`, `case:below`, `case:above`, `quote:<id>`, `step:<n>`, `line:fit`; secret: the violation's direction and size.
- **Accessibility** "At S_T 120: A pays 20 from the call plus 100 from the bond, 120 in all; B pays 0 from the put plus 120 from the share, 120 in all."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.22 `binomial-tree`

composite · tier composite · cluster `finance` · **P1** · size L · spec finance 5.1, calc-linalg 7.8 · first use 1.7 L64

Build an $N$-step tree; replicate with $\Delta$ shares and a bond; derive the risk-neutral probability $q = \frac{e^{r\Delta t} - d}{u - d}$; price by backward induction; American early exercise.

- **Composes** `marks`, `slider`, `stepper`, `numeric-input`, `value-table`, `plot-2d`, `region-select`, `position-editor`, `cashflow-timeline`, `array-strip`, `live-formula`.
- **Config** `BinomialTreeConfig { S0, K, r, T, N, NMax, move, q?, payoff, style, mode, fill, qMode, link?, u, d, type, expr?, q }`.
- **Answers** `numeric`, `choice`, `set`, `code`, `state`.
- **AI hooks** targets `node:<n>,<j>`, `edge:<n>,<j>,up`, `edge:<n>,<j>,down`, `q`, `delta:<n>,<j>`, `bond:<n>,<j>`, `cell:<j>`, `plot:converge`, `slider:<param>`; secret: the full solved tree; tryable `slider:<param>`.
- **Accessibility** The tree also renders as a table by time step and state; arrow keys follow the tree; delta values are read with each node.
- **Reduced motion** Layers and overwrites appear at once.
- **Modes added** `path-dependent` (lookback, Asian), `trinomial` and `perpetual` modes (P2, 3.2 L2 to L4, L20, curriculum); Modes `crr`, `delta`, `dividend`, `vector`, `state-prices`; specified in full in section 5.1 (P1, finance 5).
- Ownership moves to finance (1.7 is its first and heaviest user; the 1.9 C++ exit checks against it).
- `BinomialTreeConfig.q` is renamed `divYield`: $q$ is the risk-neutral probability, $\delta$ the dividend yield (finance-projects decision 7).

#### 5.14.23 `bs-explorer`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.7.1 · first use 1.7 L72

Read the formula rather than memorise it: $c = S_0 e^{-qT} N(d_1) - K e^{-rT} N(d_2)$ is an asset-or-nothing claim minus a cash-or-nothing claim; $N(d_2)$ is the risk-neutral chance of exercise; the real drift does not appear.

- **Composes** `plot-2d`, `slider`, `marks`, `live-formula`, `sketch-pad`, `numeric-input`, `choice`, `dist-explorer`, `binomial-tree`.
- **Config** `BsExplorerConfig { mode, type, params, editable, slices?, predictFirst? }`.
- **Answers** `numeric`, `choice`, `curve`, `point`.
- **AI hooks** targets `slider:<param>`, `curve:T=<t>`, `component:asset`, `component:cash`, `density`, `tail`, `formula:d1`, `formula:d2`, `table:signs`; tryable `slider:<param>`.
- **Accessibility** "S 100, K 100, T 0.5 years, volatility 20%, r 3% continuous: call 6.37, put 4.88; d1 0.177, d2 0.035." Table by $S$.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.24 `greeks-lab`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.7.2 · first use 1.7 L75

Each Greek is a shape on the price curve before it is a formula: delta is the tangent's slope, gamma its rate of turning, theta the gap between today's and tomorrow's curves.

- **Composes** `plot-2d`, `drag-point`, `slider`, `position-editor`, `plot-3d`, `marks`, `value-table`, `live-formula`, `numeric-input`, `choice`.
- **Config** `GreeksLabConfig { mode, base, Srange, tSlices?, editor?, units }`.
- **Answers** `numeric`, `point`, `choice`, `state`.
- **AI hooks** targets `handle:S`, `line:tangent`, `curve:price`, `curve:<greek>:T=<t>`, `table:portfolio`, `cell:<leg>:<greek>`.
- **Accessibility** "At S 100: delta 0.570 per share, gamma 0.028 per unit, theta −0.019 per day, vega 0.28 per volatility point." Table of Greeks by $S$.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- Surface mode P2.

#### 5.14.25 `pnl-attribution`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.7.3 · first use 1.7 L77

The desk's daily question, "why did we make or lose money?", answered with a waterfall.

- **Composes** `marks`, `plot-2d`, `slider`, `position-editor`, `value-table`, `numeric-input`, `choice`; mark types `waterfall`.
- **Config** `PnlAttributionConfig { mode, position, market, move?, path? }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `bar:delta`, `bar:gamma`, `bar:theta`, `bar:vega`, `bar:residual`, `marker:full`, `slider:dS`, `slider:dSigma`; tryable `slider:dS`, `slider:dSigma`.
- **Accessibility** "Move +2.00: delta +1.14, gamma +0.06, theta −0.02, vega 0; explained +1.18; actual +1.19; residual +0.01."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.14.26 `iv-solver`

composite · tier composite · cluster `finance` · **P1** · size M · spec finance 6.7.4 · first use 1.7 L79

Implied volatility is the one number the market quotes options in.

- **Composes** `plot-2d`, `drag-point`, `stepper`, `token-tray`, `live-formula`, `numeric-input`, `choice`, `code-cell`.
- **Config** `IvSolverConfig { mode, option, market, sigmaRange, start? }`.
- **Answers** `numeric`, `ordering`, `choice`, `point`.
- **AI hooks** targets `handle:sigma`, `curve:price`, `line:market`, `iterate:<n>`, `bracket`, `smile:<K>`; secret: the true volatility used to generate the quote.
- **Accessibility** "Market 4.20; at volatility 22.0% the model gives 4.05; increase volatility." Iterates as a table.
- **Reduced motion** Tangents appear at once.
- Algorithm mode P2.

### 5.15 Data structures, algorithms and contests (1.8, 2.4)

#### 5.15.1 `complexity-lab`

composite · tier composite · cluster `algorithms` · **P0** · size M · spec programming 7.1 · first use 1.1 L8

How cost grows with input size: comparing growth rates, counting steps in code, races between data structures, operation budgets from constraints, and measuring an exponent from timings.

- **Composes** `plot-2d`, `marks`, `slider`, `token-tray`, `code-surface`, `value-table`, `expression-input`, `live-formula`; services `algo-trace`, `trace-recorder`.
- **Config** `ComplexityLabConfig { functions?, snippet?, source, hits, race?, a, b, counts, budget?, n, seconds, language }`.
- **Answers** `ordering`, `expression`, `choice`, `numeric`.
- **AI hooks** targets `curve:<f>`, `slider:n`, `line:<n>`; describe, e.g. "Growth plot n from 1 to 1,000, log y. 100n and n^2 cross at n = 100. Learner ranking: log n, n, n log n, n^2, 2^n."; tryable `slider:n`.
- **Accessibility** the table view lists $n$ and each function's value; the ranking is a list.
- **Reduced motion** nothing to change.
- **Modes added** three-lane race (P1, 1.8 sample, curriculum).
- Growth, race and code modes P0 (1.1 L8); budget and timing modes P1.

#### 5.15.2 `algo-lab`

composite · tier composite · cluster `algorithms` · **P0** · size L · spec this file (section 6.1) · first use 1.1 L19 (through `sort-lab`)

One composite for every "be the algorithm" screen: the learner performs the next operation of a recorded algorithm on linked panes, or watches, predicts and scrubs it.

- **Composes** `array-strip`, `node-link`, `cell-grid`, `code-surface`, `value-table`, `stepper`, `live-formula`, `slider`, `plot-2d`, `choice`, `numeric-input`.
- **Config** `AlgoLabConfig { algorithm, instance, panes, mode, moves?, invariant?, code?, controls?, readouts?, ties? }`: `algorithm` names an `algo-trace` entry; `panes` bind primitives to trace state; `mode` is `watch`, `predict-next`, `be-the-algorithm`, `scrub` or `build`.
- **Answers** `state` (predicates `moveMatchesAlgorithm`, `isHeap`, `listShape`, `isSorted`, `validTopoOrder` and the preset's own), `ordering`, `numeric`, `set`, `choice`.
- **AI hooks** targets `cell:<i>`, `node:<id>`, `edge:<a>-<b>`, `ptr:<name>`, `line:<n>`, `step:<k>`; describe gives the algorithm, the step and the invariant; secret: the next correct move and the final state; tryable: instance controls.
- **Accessibility** each pane keeps its primitive's keyboard model; the move palette is a row of buttons; the Table view lists the trace (step, operation, state); every move is announced on commit.
- **Reduced motion** moves land at once; step changes cross-fade in 120 ms.
- New base composite for "be the algorithm" (programming section 7): panes of `array-strip`, `node-link`, `cell-grid`, `code-surface` and `value-table` bound to one `algo-trace` run; the learner performs the next operation and the predicate `moveMatchesAlgorithm` checks it against the trace (any valid order where ties exist, programming decision 13).
- Replaces 15 catalogue composites, which become presets: each supplies an algorithm family, panes, allowed moves, predicates and recipes, and no view.

#### 5.15.3 `counterexample-lab`

composite · tier composite · cluster `algorithms` · **P1** · size M · spec programming 7.18 · first use 1.8 L21

Break a claim by building an input.

- **Composes** `array-strip`, `interval-sweep`, `node-link`, `value-table`, `diff-view`; services `algo-trace`, `python-runner`.
- **Config** `CounterexampleLabConfig { inputType, constraints, candidate, reference, property?, generator?, language? }`.
- **Answers** `state`, `output`.
- **AI hooks** targets `input`, `out:candidate`, `out:reference`; describe, e.g. "Greedy coins {1, 3, 4}, amount 6: greedy 3 coins (4+1+1), optimal 2 (3+3). Learner input differs: yes."
- **Accessibility** inputs and outputs as text; stress progress announced every 100 inputs.
- **Reduced motion** nothing to change.
- Not used in 1.2 (python-tools decision 19); first use 1.8 L21; hack mode P2.

#### 5.15.4 `interval-sweep`

composite · tier composite · cluster `algorithms` · **P1** · size M · spec programming 7.9 · first use 1.8 L52

Intervals on a timeline: merging, inserting, the greedy that schedules the most non-overlapping intervals (by earliest end), the fewest removals, meeting rooms, and points that stab every interval.

- **Composes** `plot-2d`, `marks`, `drag-point`, `heap-lab`, `token-tray`, `stepper`; services `algo-trace`.
- **Config** `IntervalSweepConfig { intervals, id, start, end, label?, closed? }`.
- **Answers** `set`, `numeric`, `state`.
- **AI hooks** targets `iv:<id>`, `sweep`; describe, e.g. "8 intervals sorted by end. Chosen: [1, 3], [4, 6]. Sweep at 6."
- **Accessibility** intervals listed with start and end; overlaps announced.
- **Reduced motion** cuts.

#### 5.15.5 `bit-lab`

composite · tier composite · cluster `algorithms` · **P1** · size M · spec programming 7.10 · first use 1.8 L78

Integers as bits: binary and hexadecimal, two's complement, shifts and masks, the classic tricks, counting bits, fast exponentiation, fixed-width C++ integers against Python's unbounded ones, and bitmasks as subsets.

- **Composes** `array-strip`, `region-select`, `slider`, `live-formula`, `cell-grid`, `place-value-chart`.
- **Config** `BitLabConfig { width, signed?, value?, target?, language? }`.
- **Answers** `output`, `numeric`, `state`, `choice`.
- **AI hooks** targets `bit:<i>`, `mask:<i>`, `wheel`; describe, e.g. "8-bit value 0b10110100 (180 unsigned, -76 signed); mask 0b00001111; AND gives 0b00000100."
- **Accessibility** "8-bit signed 11110110 is -10; unsigned 246".
- **Reduced motion** shifts cut.
- **Modes added** C++ precedence (P1, curriculum).
- Subset mode P2.

#### 5.15.6 `problem-workbench`

composite · tier composite · cluster `algorithms` · **P1** · size L · spec programming 7.19 · first use 1.8 L146

The practice surface for the 150 problems and for contests.

- **Composes** `code-cell`, `speed-timer`, `choice`, `free-response`, `value-table`, `token-tray`, `diagnostic-reader`, `counterexample-lab`, `code-annotator`.
- **Config** `ProblemWorkbenchConfig { id, title, difficulty, statement, constraints, patterns, heldOut?, cell, mode, edgeCases?, input, expected, editorial?, timeLimitMin? }`.
- **Answers** `code`, `output`, `choice`.
- **AI hooks** targets `stage:<n>`, `case:<k>`, `code:cell`; describe, e.g. "Problem 'Top K Frequent Elements' (medium), stage 4 code. Patterns chosen: heap. Target O(n log k). Last run: 2 of 3 examples."
- **Accessibility** the stage rail is a list of links with status words; the timer follows `speed-timer`'s rules.
- **Reduced motion** cut.
- Interview mode P2; supports the 40 held-out timed mediums of the 1.8 exit (dsa-cpp decision 8).

#### 5.15.7 `contest-arena`

composite · tier composite · cluster `algorithms` · **P2** · size M · spec programming 9.1 · first use 2.4 L1

A virtual contest: a problem set under a clock, verdicts per submission, a scoreboard, an optional hacking phase, then editorials and an upsolve list.

- **Composes** `problem-workbench`, `code-cell`, `speed-timer`, `value-table`, `counterexample-lab`, `code-annotator`.
- **Config** `ContestArenaConfig { scoring, durationMin, rivals, count, seed, hacking?, calibrate? }`.
- **Answers** `code`, `state`.
- **AI hooks** targets: the ids of its marks and handles.
- **Accessibility** the timer follows `speed-timer`; verdicts announced; the scoreboard is a table.
- **Reduced motion** cuts.
- **Modes added** ICPC penalty of 20 minutes per rejected submission; web-only problems flagged (P2, dsa-cpp request 7).

#### 5.15.8 `number-theory-lab`

composite · tier composite · cluster `algorithms` · **P2** · size M · spec programming 9.2 · first use 2.4 L20

The number theory contests use: the sieve, Euclid's algorithm as cutting squares from a rectangle, the extended algorithm and modular inverses, fast modular powers, modular arithmetic with negative numbers in Python and C++.

- **Composes** `cell-grid`, `plot-2d`, `marks`, `value-table`, `live-formula`, `bit-lab`, `modular-clock`, `factor-tree`.
- **Config** `NumberTheoryLabConfig { n?, a?, b?, m?, p?, k? }`.
- **Answers** `numeric`, `state`, `set`.
- **AI hooks** targets `cell:<n>`, `square:<k>`, `row:<k>`; describe, e.g. "Sieve to 100: primes 2, 3, 5 done; next uncrossed 7."
- **Accessibility** "Crossed out multiples of 3 from 9: 9, 12, 15, ...; 25 primes below 100".
- **Reduced motion** cuts.
- **Modes added** CRT and Grundy values (P2, curriculum).

### 5.16 C++ (1.9)

#### 5.16.1 `memory-layout`

composite · tier composite · cluster `cpp` · **P1** · size M · spec programming 8.2 · first use 1.8 L24

What objects look like in bytes: type sizes, alignment and padding, field order, endianness, arrays and address arithmetic, contiguous values against pointers to scattered objects, and cache lines.

- **Composes** `array-strip`, `token-tray`, `live-formula`, `cell-grid`, `node-link`.
- **Config** `MemoryLayoutConfig { struct?, name, fields, type, matrix?, rows, cols, elem, line? }`.
- **Answers** `numeric`, `state`, `choice`.
- **AI hooks** targets `field:<name>`, `byte:<i>`, `line:<k>`; describe, e.g. "struct Quote { char side; double px; int qty; }: offsets 0, 8, 16; size 24; padding 11 bytes."
- **Accessibility** a table of field, offset, size and alignment, plus total padding.
- **Reduced motion** cuts.
- **Modes added** false sharing (P1, curriculum).

#### 5.16.2 `compile-pipeline`

composite · tier composite · cluster `cpp` · **P1** · size M · spec programming 8.1 · first use 1.9 L1

From source to program: the preprocessor expands includes and macros into a translation unit, the compiler turns each unit into an object file with defined and undefined symbols, and the linker joins objects and libraries.

- **Composes** `node-link`, `token-tray`, `code-surface`, `diagnostic-reader`, `value-table`.
- **Config** `CompilePipelineConfig { files, path, source, recorded, expandedLines?, symbols?, defined, undefined, errors?, stage, text, deps?, edited? }`.
- **Answers** `ordering`, `mapping`, `set`.
- **AI hooks** targets `file:<path>`, `stage:<name>`, `sym:<name>`, `obj:<path>`; describe, e.g. "3 sources, 2 headers. Linker stage: undefined reference to price(double) in main.o; defined nowhere."
- **Accessibility** lanes as lists; symbols as tables; errors through `diagnostic-reader`.
- **Reduced motion** cuts.
- Concept screens use compiler output recorded at build time; C++ never runs in the Artifact (dsa-cpp decision 12).

#### 5.16.3 `ownership-lab`

composite · tier composite · cluster `cpp` · **P1** · size M · spec programming 8.3 · first use 1.9 L23

Who owns a resource and when it is released: raw `new` and `delete`, RAII, copying against moving, the rules of zero, three and five, `unique_ptr`, `shared_ptr` counts and cycles, and `weak_ptr`.

- **Composes** `node-link`, `token-tray`, `value-table`, `diagnostic-reader`, `code-surface`.
- **Config** `OwnershipLabConfig { start, owners, blocks, ops?, predictAfter?, program }`.
- **Answers** `state`, `numeric`, `ordering`, `choice`.
- **AI hooks** targets `owner:<id>`, `block:<id>`, `ctrl:<id>`, `op:<k>`; describe, e.g. "Owners: shared_ptr a, b to block X (strong 2); weak_ptr w to X. Next: end of scope f."
- **Accessibility** owners and blocks as a table; each operation's effect announced ("p moved to q; p is now empty; block A owned by q").
- **Reduced motion** cuts.

### 5.17 Machine learning (2.1)

#### 5.17.1 `fit-explorer`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.1.1 · first use 2.1 L1

The founding idea of the course: a model is judged on new data.

- **Composes** `plot-2d`, `marks`, `sketch-pad`, `slider`, `choice`, `live-formula`, `error-curves`, `least-squares-fit`, `basis-lab`; mark types `curve`.
- **Config** `FitExplorerConfig { data, mode, models, ranges?, show, gateTest, freshSet? }`.
- **Answers** `choice`, `numeric`, `point`, `curve`.
- **AI hooks** targets `point:<i>`, `curve:fit`, `curve:truth`, `curve:sketch`, `handle:<i>`, `slider:degree`, `slider:k`, `slider:p`, `readout:train`, `readout:test`, `set:fresh`; secret: the true function, $\sigma$, and test values while gated; tryable `slider:degree`, `slider:k`, `slider:p`.
- **Accessibility** Table of $x$, $y$, set (train, test, fresh), fitted value and residual. Describe: "Degree 9 polynomial on 15 training points: train MSE 0.02, test MSE 1.84. The curve swings between 0.8 and 0.95."
- **Reduced motion** Fresh points appear at once with residuals.
- **Modes added** `sketch` mode with "Thread every point" and fixed-data "Reveal tomorrow"; compare mode with clipped curves (P2, 2.1 sample, curriculum).

#### 5.17.2 `error-curves`

composite · tier composite · cluster `ml` · **P2** · size S · spec ML 6.1.3 · first use 2.1 L1

The single picture that most of 2.1 returns to.

- **Composes** `plot-2d`, `marks`, `sketch-pad`, `drag-point`, `value-table`; mark types `curve`.
- **Config** `ErrorCurvesConfig { x, source, show, mode, noiseFloor? }`.
- **Answers** `curve`, `point`, `numeric`.
- **AI hooks** targets `curve:train`, `curve:cv`, `curve:test`, `whisker:<x>`, `cursor`, `line:noise`, `marker:min`, `marker:1se`, `sketch:train`, `sketch:test`; secret: the test curve while gated.
- **Accessibility** Table of $x$, train, CV, standard error and test. "Test error lowest at degree 3 (0.41). Training error keeps falling to 0.02 at degree 12."
- **Reduced motion** Curves appear complete.
- **Modes added** predict mode on fixed data with a per-degree table (P2, 2.1 sample, curriculum).

#### 5.17.3 `classifier-plane`

composite · tier composite · cluster `ml` · **P2** · size L · spec ML 6.2.2 · first use 2.1 L3

One plane, many models, so the learner sees what each assumes.

- **Composes** `plot-2d`, `marks`, `drag-point`, `region-select`, `sketch-pad`, `slider`, `choice`, `sim-runner`; mark types `scatter`, `field`, `boundary`.
- **Config** `ClassifierPlaneConfig { data, models, mode, editable, overlays, grid }`.
- **Answers** `set`, `numeric`, `choice`, `state`, `point`.
- **AI hooks** targets `point:<i>`, `field`, `boundary`, `boundary:bayes`, `margin`, `sv:<i>`, `chip:<model>`, `slider:<param>`, `cell:<r>,<c>`; secret: the generating densities and the Bayes error; tryable `chip:<model>`, `slider:<param>`.
- **Accessibility** Describe: "QDA on 'circles', 200 points: class A inside a ring of radius 1.1; held-out accuracy 0.93. 3 held-out points misclassified." The table lists points with true class, predicted class and probability.
- **Reduced motion** Show-why becomes before-and-after; the field still follows drags (the learner's own motion).
- Every 2.1 model drawn as decision regions through the `field` mark on a 64 by 64 grid (ML decision 13).

#### 5.17.4 `bias-variance-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.1.4 · first use 2.1 L6

Draw $M$ training sets from the same process and fit the same model to each.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `sim-runner`, `error-curves`, `derivation-steps`, `value-table`; mark types `curve`, `hist`, `bars`, `band`.
- **Config** `BiasVarianceLabConfig { data, models, mode, x0?, M, show, tableOfFits? }`.
- **Answers** `ordering`, `numeric`, `expression`, `choice`.
- **AI hooks** targets `handle:x0`, `curve:truth`, `curve:average`, `fits`, `hist:x0`, `bar:bias2`, `bar:variance`, `bar:noise`, `slider:<param>`; secret: none beyond the generator; tryable `slider:<param>`.
- **Accessibility** Table at $x_0$: fit index and $\hat f(x_0)$, then mean, bias and variance. "Degree 1: bias squared 0.30, variance 0.01 at x0 = 0.8. Degree 9: bias squared 0.00, variance 0.42."
- **Reduced motion** Batches appear complete.

#### 5.17.5 `loss-lab`

composite · tier composite · cluster `ml` · **P2** · size S · spec ML 6.1.2 · first use 2.1 L11

A loss is a choice about what to predict.

- **Composes** `plot-2d`, `drag-point`, `marks`, `slider`, `choice`, `live-formula`; mark types `curve`.
- **Config** `LossLabConfig { mode, data, losses, delta?, tau?, movable, showMinimiser }`.
- **Answers** `point`, `interval`, `numeric`, `mapping`, `choice`, `set`.
- **AI hooks** targets `handle:c`, `point:<i>`, `curve:<loss>`, `tick:mean`, `tick:median`, `tick:quantile`, `slider:delta`, `slider:tau`; secret: none beyond the minimisers while hidden; tryable `slider:delta`, `slider:tau`.
- **Accessibility** "c = 2.4. Squared loss 18.2 (minimum 11.6 at the mean, 3.1). Absolute loss 9.0 (minimum 8.2 at any c from 2.0 to 2.6)." Table of points and residuals.
- **Reduced motion** Before-and-after pair.
- **Modes added** `pinball-set` mode showing a flat minimiser interval (P2, LD3 homework, curriculum).

#### 5.17.6 `logistic-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.2.1 · first use 2.1 L15

Logistic regression models $p(x) = \sigma(wx + b) = \frac{1}{1 + e^{-(wx + b)}}$, so the log-odds $\ln\frac{p}{1 - p} = wx + b$ are linear and each unit of $x$ multiplies the odds by $e^w$.

- **Composes** `plot-2d`, `drag-point`, `marks`, `slider`, `mass-editor`, `surface-explorer`, `descent-lab`, `node-link`, `live-formula`; mark types `curve`, `field`, `boundary`.
- **Config** `LogisticLabConfig { mode, data?, init?, editable, show, softmax? }`.
- **Answers** `point`, `numeric`, `choice`, `expression`, `state`.
- **AI hooks** targets `handle:mid`, `handle:73`, `curve:learner`, `curve:mle`, `bar:<i>`, `point:<i>`, `vec:w`, `handle:offset`, `logit:<k>`, `slider:temperature`, `slider:l2`, `readout:loglik`; secret: the true $(w, b)$ of generated data and the MLE; tryable `slider:temperature`, `slider:l2`.
- **Accessibility** Table of $x$, $y$, $p(x)$ and log loss. "Midpoint at x = 1.2, slope at midpoint 0.6 per unit (w = 2.4). Log-likelihood −8.31; the maximum is −7.95."
- **Reduced motion** Before-and-after pairs.

#### 5.17.7 `cv-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.3.1 · first use 2.1 L23

A single validation split gives an estimate that moves with the split.

- **Composes** `cell-grid`, `marks`, `stepper`, `slider`, `choice`, `regression-lab`, `error-curves`, `sim-runner`.
- **Config** `CvLabConfig { data, model, scheme, k, kRange?, stratify?, groups?, tuning?, trap?, task }`.
- **Answers** `numeric`, `set`, `ordering`, `choice`, `state`.
- **AI hooks** targets `row:<i>`, `fold:<j>`, `bar:fold-<j>`, `readout:estimate`, `readout:se`, `hist:repeats`, `panel:inner-<j>`, `trap:outside`, `trap:inside`; secret: the true test error.
- **Accessibility** "5-fold CV, fold 3 of 5 held out: rows 25 to 36. Fold MSEs 0.92, 1.10, 0.85, 1.31, 0.97; estimate 1.03, standard error 0.08." The row grid has a table view with row, fold and role.
- **Reduced motion** Bands jump.
- **Modes added** `loocv-shortcut` with hat values (P2, 2.1 L25, curriculum).

#### 5.17.8 `leakage-detective`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.6.2 · first use 2.1 L28

Leakage is information at training or decision time that would not exist in live trading.

- **Composes** `span-track`, `pipeline-flow`, `value-table`, `portfolio-sort`, `card-sort`, `choice`, `drag-point`, `marks`; mark types `gantt`.
- **Config** `LeakageDetectiveConfig { mode, features?, decisionTime?, pipeline?, panel?, study? }`.
- **Answers** `set`, `ordering`, `numeric`, `code`.
- **AI hooks** targets `feature:<name>`, `span:<name>:event`, `span:<name>:available`, `cursor:decision`, `stage:<id>`, `toggle:pit`, `toggle:delist`, `card:<flaw>`; secret: the planted leaks and their reasons; tryable `toggle:pit`, `toggle:delist`.
- **Accessibility** Features listed with event and availability times and whether each is known at the decision time. "Decision at 15:59 on day t. Close(t) available 16:00: not known. Volume(t−1): known."
- **Reduced motion** Static highlights.

#### 5.17.9 `tuning-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.3.2 · first use 2.1 L29

With a budget of nine evaluations over two hyperparameters, a 3 by 3 grid tries 3 distinct values of each; random search tries 9 of each, which wins when only one hyperparameter matters (Bergstra and Bengio 2012).

- **Composes** `plot-2d`, `marks`, `region-select`, `choice`, `slider`, `sim-runner`; mark types `scatter`, `field`, `rug`, `step`.
- **Config** `TuningLabConfig { surface, axes, strategies, budget, show }`.
- **Answers** `choice`, `numeric`, `state`, `point`.
- **AI hooks** targets `point:<i>`, `rug:x`, `rug:y`, `field:surface`, `marker:optimum`, `curve:best-so-far`, `chip:<strategy>`, `slider:budget`; secret: the surface and its optimum; tryable `chip:<strategy>`, `slider:budget`.
- **Accessibility** "Random search, 9 evaluations: 9 distinct learning rates, 9 distinct depths. Best CV score 0.71 at (0.03, 6); its hold-out score 0.66."
- **Reduced motion** Points appear together.

#### 5.17.10 `regularisation-path`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.3.3 · first use 2.1 L31

Shrinking coefficients trades a little bias for less variance.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `choice`, `error-curves`, `cv-lab`, `pca-lab`, `matrix`, `value-table`, `sim-runner`; mark types `curve`, `bars`.
- **Config** `RegularisationPathConfig { data, methods, lambdaGrid, panels, standardise, truth, cvFolds? }`.
- **Answers** `numeric`, `point`, `set`, `choice`, `ordering`.
- **AI hooks** targets `cursor:lambda`, `path:<feature>`, `bar:<feature>`, `svd:<j>`, `curve:cp`, `curve:aic`, `curve:bic`, `curve:adjr2`, `freq:<feature>`, `toggle:standardise`, `chip:<method>`; secret: the true coefficients; tryable `toggle:standardise`, `chip:<method>`.
- **Accessibility** "Lasso at log λ = −1.2: 4 features kept (x1 0.82, x3 −0.40, x7 0.11, x12 0.05). CV MSE 1.21 (standard error 0.06); λ1se is at −0.8." Tables for the path (rows by $\lambda$), bars and criteria.
- **Reduced motion** Before-and-after.

#### 5.17.11 `feature-builder`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.2.5 · first use 2.1 L35

Models see numbers in columns, not categories or dates.

- **Composes** `value-table`, `token-tray`, `matrix`, `regression-lab`, `logistic-lab`, `condition-number`; services `frame-core`.
- **Config** `FeatureBuilderConfig { frame, palette, split?, flagLeaks, linkedFit?, task }`.
- **Answers** `resultset`, `numeric`, `set`, `choice`, `code`.
- **AI hooks** targets `col:<name>`, `chip:<kind>`, `cell:<r>,<c>`, `readout:rank`, `readout:cond`, `combo:dependent`; secret: the planted leaks; tryable `chip:<kind>`.
- **Accessibility** The frames are real tables. "Encoded 'sector' into 4 columns (drop first). Rank 6 of 6. Linked fit: test MSE 0.84."
- **Reduced motion** Columns appear at once; the sum shows as a static equation.

#### 5.17.12 `basis-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.2.6 · first use 2.1 L40

Linear models fit curves by adding columns: powers of $x$, steps, hinges $(x - \xi)_+$, cubic splines with knots $\xi_k$, natural splines (linear beyond the boundary knots), Gaussian bumps, or sines and cosines.

- **Composes** `plot-2d`, `drag-point`, `marks`, `choice`, `slider`, `fit-explorer`, `error-curves`, `live-formula`; mark types `curve`, `scatter`.
- **Config** `BasisLabConfig { data, families, knots, maxKnots, editable, show, gam? }`.
- **Answers** `numeric`, `choice`, `mapping`, `state`.
- **AI hooks** targets `knot:<i>`, `basis:<j>`, `scaled:<j>`, `curve:fit`, `zone:extrapolation`, `chip:<family>`, `readout:df`, `readout:rss`; secret: the generator's change points; tryable `chip:<family>`.
- **Accessibility** "Natural cubic spline, 4 knots at 0.2, 0.4, 0.6, 0.8: 4 degrees of freedom. RSS 3.1." Table of $x$, each basis value and the fit.
- **Reduced motion** Before-and-after.
- **Modes added** `gam` and `kernel` modes (P2, 2.1 L43, L44, curriculum).

#### 5.17.13 `penalty-geometry`

composite · tier composite · cluster `ml` · **P2** · size S · spec ML 6.3.4 · first use 2.1 L47

With two coefficients, the residual sum of squares has elliptical contours centred at the OLS estimate, shaped by $X^\top X$.

- **Composes** `plot-2d`, `marks`, `drag-point`, `slider`, `choice`, `card-sort`, `posterior-lab`; mark types `norm-ball`, `curve`.
- **Config** `PenaltyGeometryConfig { mode, ols, gram?, penalties, budget, movable, show }`.
- **Answers** `point`, `numeric`, `mapping`, `choice`, `state`.
- **AI hooks** targets `handle:ols`, `ball`, `contour:touch`, `point:solution`, `handle:guess`, `path:solution`, `slider:t`, `slider:rho`, `curve:ridge`, `curve:lasso`, `curve:subset`; secret: the solution while hidden; tryable `slider:t`, `slider:rho`.
- **Accessibility** "OLS at (2.0, 0.6), correlation 0.5. Lasso budget 1.5: solution (1.5, 0.0), on the β1 axis. Your guess (1.4, 0.1), 0.14 away."
- **Reduced motion** Before-and-after.

#### 5.17.14 `threshold-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.2.3 · first use 2.1 L71

A classifier outputs a score; a decision needs a threshold.

- **Composes** `plot-2d`, `drag-point`, `marks`, `contingency-table`, `icon-array`, `cell-grid`, `slider`, `live-formula`; mark types `hist`, `curve`, `step`.
- **Config** `ThresholdLabConfig { scores, baseRate, panels, costs?, payoff?, editable }`.
- **Answers** `numeric`, `point`, `interval`, `choice`, `set`.
- **AI hooks** targets `handle:threshold`, `region:tp`, `region:fp`, `region:tn`, `region:fn`, `curve:roc`, `curve:pr`, `point:roc`, `point:pr`, `area:auc`, `curve:profit`, `cell:<i>,<j>` and 1 more; secret: the profit-maximising threshold; tryable `slider:base-rate`.
- **Accessibility** "Threshold 0.62. TP 42, FP 18, TN 920, FN 20. Precision 0.70, recall 0.68, false positive rate 0.019. AUC 0.91." The table lists thresholds with the four counts.
- **Reduced motion** Before-and-after.

#### 5.17.15 `calibration-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.2.4, finance 8.5 · first use 2.1 L76

A forecast of 70% should come true 70% of the time.

- **Composes** `plot-2d`, `marks`, `sketch-pad`, `slider`, `choice`, `sim-runner`, `drawdown-lab`, `live-formula`, `number-line`, `numeric-input`, `value-table`, `fermi-estimator`; mark types `scatter`, `step`, `hist`, `paths`.
- **Config** `CalibrationLabConfig { forecasts, mode, methods, split?, sizing?, items, coverage, scale }`.
- **Answers** `numeric`, `choice`, `curve`, `interval`, `state`.
- **AI hooks** targets `bin:<k>`, `line:diagonal`, `curve:distortion`, `curve:platt`, `curve:isotonic`, `handle:p`, `path:stated`, `path:true`, `readout:brier`, `item:<id>`, `bracket:<id>`, `truth:<id>` and 1 more; secret: the true calibration curve.
- **Accessibility** "10 bins. Forecasts near 0.9 come true 0.74 of the time: over-confident. Brier 0.192 = reliability 0.021 − resolution 0.079 + uncertainty 0.250." Table of bins with counts, mean forecast, observed frequency and interval.
- **Reduced motion** Before-and-after.
- One widget for stated against observed frequency: `subject: model` is ML's reliability diagram, recalibration and sizing; `subject: self` is finance's 50% and 90% intervals, hit rate and interval score for 3.3; both share the binning and the scoring rules (Brier, log, interval score).

#### 5.17.16 `tree-builder`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.4.2 · first use 2.1 L86

A tree partitions the plane into boxes and predicts the majority class (or mean) in each.

- **Composes** `plot-2d`, `marks`, `node-link`, `split-scorer`, `drag-point`, `slider`, `stepper`, `error-curves`, `sim-runner`; mark types `partition`, `scatter`, `step`.
- **Config** `TreeBuilderConfig { data, mode, criterion, limits?, show, query? }`.
- **Answers** `numeric`, `ordering`, `set`, `choice`, `point`.
- **AI hooks** targets `node:<id>`, `leaf:<id>`, `box:<id>`, `line:split`, `toggle:axis`, `slider:depth`, `slider:alpha`, `panel:scorer`; secret: the generator's true boundary and held-out labels while gated; tryable `toggle:axis`, `slider:depth`, `slider:alpha`.
- **Accessibility** The tree is a nested list with counts and impurity at each node; boxes are named by their bounds ("x1 ≤ 0.42 and x2 > 1.3: 14 points, 13 A"). "Depth 3, 6 leaves; training accuracy 0.91, held-out 0.78."
- **Reduced motion** Splits and folds are instant; resamples show side by side.

#### 5.17.17 `split-scorer`

composite · tier composite · cluster `ml` · **P2** · size S · spec ML 6.4.1 · first use 2.1 L87

A tree grows by choosing, at each node, the feature and threshold that most reduce impurity.

- **Composes** `plot-2d`, `drag-point`, `marks`, `choice`, `live-formula`; mark types `scatter`, `curve`, `bars`.
- **Config** `SplitScorerConfig { node, criteria, predict, show }`.
- **Answers** `numeric`, `interval`, `choice`.
- **AI hooks** targets `handle:threshold`, `strip:<feature>`, `bar:left`, `bar:right`, `curve:score`, `marker:best`, `panel:concavity`, `chip:<criterion>`; secret: the best split; tryable `chip:<criterion>`.
- **Accessibility** "x2 at 3.45: left 12 (10 A, 2 B), right 18 (3 A, 15 B). Gini parent 0.499, children weighted 0.271, gain 0.228." Table of thresholds and scores.
- **Reduced motion** Static chords.
- **Modes added** `chord` mode for the ESL tie (P2, 2.1 L87, curriculum).

#### 5.17.18 `ensemble-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.4.3 · first use 2.1 L92

Averaging $B$ identically distributed predictions with variance $\sigma^2$ and pairwise correlation $\rho$ gives variance $\rho\sigma^2 + \frac{1 - \rho}{B}\sigma^2$: more trees remove the second term, never the first.

- **Composes** `plot-2d`, `marks`, `slider`, `choice`, `sim-runner`, `error-curves`, `tree-builder`, `live-formula`; mark types `field`, `curve`.
- **Config** `EnsembleLabConfig { data, methods, B, mtry?, depth?, minLeaf?, show }`.
- **Answers** `numeric`, `choice`, `ordering`.
- **AI hooks** targets `member:<i>`, `curve:mean`, `field`, `curve:oob`, `curve:test`, `line:floor`, `slider:B`, `slider:mtry`, `formula:var`; secret: the true function; tryable `slider:B`, `slider:mtry`.
- **Accessibility** "Random forest, 200 trees, mtry 3 of 10: OOB error 0.142, test error 0.150; mean pairwise correlation of tree predictions 0.31."
- **Reduced motion** The final state appears.

#### 5.17.19 `boosting-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.4.4 · first use 2.1 L96

Gradient boosting builds $F_m = F_{m-1} + \nu h_m$, where $h_m$ is a small tree fitted to the negative gradient of the loss: the residuals $y - F_{m-1}$ for squared loss, and $y - p$ for log loss with $p = \sigma(F)$.

- **Composes** `plot-2d`, `marks`, `drag-point`, `split-scorer`, `slider`, `stepper`, `error-curves`, `classifier-plane`, `sim-runner`; mark types `scatter`, `step`.
- **Config** `BoostingLabConfig { data, loss, nu, depth, rounds, mode, show }`.
- **Answers** `numeric`, `expression`, `point`, `choice`, `state`.
- **AI hooks** targets `handle:split`, `handle:left`, `handle:right`, `stump:best`, `curve:fit`, `residual:<i>`, `point:<i>`, `slider:nu`, `curve:train`, `curve:val`, `marker:stop`; secret: the best stump while hidden; tryable `slider:nu`.
- **Accessibility** "Round 3 of 50, ν = 0.3, stumps. Training MSE 0.84, validation 0.91. Your stump: split at 0.42, levels −0.31 and 0.27; best: 0.45, −0.33 and 0.29."
- **Reduced motion** Rounds apply instantly.

#### 5.17.20 `importance-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.4.5 · first use 2.1 L102

Impurity importance (MDI) is computed in-sample and favours features with many distinct values, so a pure-noise ID column can top the chart (Strobl and others 2007).

- **Composes** `value-table`, `marks`, `plot-2d`, `choice`, `slider`, `cluster-lab`, `sim-runner`, `card-sort`, `live-formula`; mark types `bars`, `curve`.
- **Config** `ImportanceLabConfig { data, model, methods, evaluation, editable, shapleyToy? }`.
- **Answers** `ordering`, `choice`, `numeric`, `curve`.
- **AI hooks** targets `bar:<method>:<feature>`, `col:<feature>`, `bracket:twins`, `curve:pdp`, `ice:<i>`, `slider:twin-rho`, `toggle:id`, `cell:<coalition>`; secret: feature roles; tryable `slider:twin-rho`, `toggle:id`.
- **Accessibility** Table of features with each method's importance and spread. "Permutation importance on held-out data: x1 0.21, x2 0.19 (twins, correlation 0.9), x5 0.03; ID column 0.00. MDI ranks the ID column second."
- **Reduced motion** Before-and-after.

#### 5.17.21 `nn-playground`

composite · tier composite · cluster `ml` · **P2** · size L · spec ML 6.5.1 · first use 2.1 L107

Hidden units are learned features: each draws its own boundary, and the next layer combines them.

- **Composes** `node-link`, `plot-2d`, `marks`, `slider`, `choice`, `stepper`, `error-curves`, `sim-runner`, `matrix`; mark types `field`, `boundary`, `scatter`, `hist`.
- **Config** `NnPlaygroundConfig { data, mode, architecture, features, featurePalette?, optimiser, regularise?, editable, epochs }`.
- **Answers** `choice`, `numeric`, `curve`, `state`, `set`.
- **AI hooks** targets `unit:<layer>:<i>`, `edge:<layer>:<i>-<j>`, `field:output`, `curve:train`, `curve:test`, `chip:<feature>`, `slider:lr`, `slider:l2`, `slider:dropout`, `hist:layer-<l>`; secret: the generator and the Bayes error; tryable `chip:<feature>`, `slider:lr`, `slider:l2`, `slider:dropout`.
- **Accessibility** Layers as a table of units with their weights and biases; each unit's map described by its boundary ("unit 2 of layer 1: active right of the line x1 + 0.4 x2 = 0.3").
- **Reduced motion** No live repaint: the state updates on Pause, Step and at the end of a run.

#### 5.17.22 `relu-composer`

composite · tier composite · cluster `ml` · **P2** · size S · spec ML 6.5.2 · first use 2.1 L109

One hidden layer of ReLU units computes $c + \sum_i a_i \max(0, w_i x + b_i)$: a piecewise linear function with a kink at each $-b_i/w_i$.

- **Composes** `plot-2d`, `drag-point`, `marks`, `slider`, `live-formula`; mark types `curve`.
- **Config** `ReluComposerConfig { target, mode, maxUnits, init?, show }`.
- **Answers** `curve`, `numeric`, `choice`, `state`.
- **AI hooks** targets `unit:<i>`, `kink:<i>`, `slope:<i>`, `curve:sum`, `curve:target`, `readout:mse`, `readout:pieces`, `slider:depth`; secret: the best achievable MSE; tryable `slider:depth`.
- **Accessibility** Units listed with kink, slope and contribution. "5 units, kinks at −1.2, −0.4, 0.3, 0.9, 1.6. MSE against the target 0.012. 6 linear pieces."
- **Reduced motion** Before-and-after.

#### 5.17.23 `sequence-filter`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.5.3 · first use 2.1 L115

Networks for sequences reuse three ideas a quant already knows.

- **Composes** `plot-2d`, `drag-point`, `marks`, `slider`, `choice`, `regularisation-path`; mark types `stems`, `paths`, `bars`.
- **Config** `SequenceFilterConfig { series, mode, L, init?, presets?, allowCentred, target? }`.
- **Answers** `numeric`, `choice`, `state`, `set`.
- **AI hooks** targets `stem:<k>`, `series:input`, `series:output`, `zone:future`, `slider:alpha`, `slider:tau`, `handle:query`, `bar:<k>`; secret: the AR coefficients of generated series; tryable `slider:alpha`, `slider:tau`.
- **Accessibility** Kernel as a table of lags and weights; "Causal kernel of length 5 (moving average): output at t = 40 is 0.31."
- **Reduced motion** Static highlight.

#### 5.17.24 `ml-workbench`

composite · tier composite · cluster `ml` · **P2** · size L · spec ML 6.9.1 · first use 2.1 L116

The exit asks for one tabular prediction problem done end to end with time-ordered cross-validation.

- **Composes** `feature-builder`, `labelling-lab`, `time-cv-lab`, `leakage-detective`, `pipeline-flow`, `tuning-lab`, `regularisation-path`, `ensemble-lab`, `boosting-lab`, `nn-playground`, `signal-lab`, `sharpe-lab`, `error-curves`, `value-table`, `free-response`, `setup-checklist`, `code-cell`.
- **Config** `MlWorkbenchConfig { data, steps, audit, models, rubric, mode }`.
- **Answers** `choice`, `numeric`, `long-form`, `code`, `state`, `point`.
- **AI hooks** targets `step:<name>`, `audit:<rule>`, `arena:<model>`, `ledger:<id>`, `holdout`, `export`; describe, e.g. "Step 5 of 8 (folds). Purged walk-forward, 6 splits, embargo 5 days. Audit: green. Ledger: 14 trials."; secret: the planted signal and leaks of generated data. Bertie can review the results note at the `complex` tier on request.
- **Accessibility** The audit strip is a live region on commit ("Audit: 1 rule failing. Feature 'eps_next' is not known at the decision time."). Every panel follows its widget's accessibility; the ledger and arena results are tables.
- **Reduced motion** Panels cut.

#### 5.17.25 `time-cv-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.6.1 · first use 2.1 L117

Financial labels span time: a label at $t$ uses returns from $t_{i,0}$ to $t_{i,1}$, and features are autocorrelated.

- **Composes** `span-track`, `cell-grid`, `stepper`, `slider`, `choice`, `marks`, `sim-runner`, `tuning-lab`; mark types `bars`.
- **Config** `TimeCvLabConfig { data, scheme, split?, model?, task, show, editable }`.
- **Answers** `set`, `numeric`, `choice`, `state`.
- **AI hooks** targets `span:<id>`, `band:test`, `band:train`, `band:embargo`, `slider:embargo`, `split:<j>`, `cell:<group>,<split>`, `path:<p>`, `bar:<scheme>`; secret: the exact purge and embargo sets; the true out-of-sample score; tryable `slider:embargo`.
- **Accessibility** Spans as a table (id, start, end, role in this split). "Purged 4-fold, split 2: test days 11 to 20; 5 examples purged (3 before, 2 after the test fold); embargo 1 day removes 1 more."
- **Reduced motion** Static highlights.
- Owns folds, label spans, purging, embargo and CPCV; `forecast-lab` embeds its fold strip (ML decision 5).

#### 5.17.26 `labelling-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.7.1 · first use 2.1 L119

López de Prado's chapters 2 to 4 in one workbench on a price path.

- **Composes** `plot-2d`, `drag-point`, `span-track`, `marks`, `slider`, `threshold-lab`, `sim-runner`, `value-table`; mark types `paths`, `step`.
- **Config** `LabellingLabConfig { prices, mode, cusum?, barriers?, primary?, editable, task }`.
- **Answers** `choice`, `point`, `numeric`, `set`.
- **AI hooks** targets `event:<id>`, `barrier:upper`, `barrier:lower`, `barrier:vertical`, `marker:touch`, `span:<id>`, `series:concurrency`, `bar:prob-<id>`, `slider:<param>`; secret: labels while predicting; tryable `slider:<param>`.
- **Accessibility** Events as a table (start, end, barrier touched, label, return, uniqueness). "Event 7 on day 112: upper barrier 104.1, lower 97.3, time limit day 122. Touched lower on day 116: label −1."
- **Reduced motion** The touch point is marked statically.

#### 5.17.27 `bar-sampler`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.7.2 · first use 2.1 L134

Time bars sample at fixed clock intervals, but information arrives with trading.

- **Composes** `plot-2d`, `marks`, `slider`, `choice`, `sim-runner`, `value-table`, `qq-plot`; mark types `scatter`, `hist`, `curve`.
- **Config** `BarSamplerConfig { trades, types, thresholds, panels, task }`.
- **Answers** `numeric`, `set`, `choice`, `ordering`.
- **AI hooks** targets `bar:<i>`, `trade:<i>`, `hist:returns`, `curve:normal`, `chip:<type>`, `slider:threshold`, `readout:kurtosis`; secret: none; tryable `chip:<type>`, `slider:threshold`.
- **Accessibility** Bars as a table (open time, close time, OHLC, volume). "Dollar bars of 2 million: 41 bars today, 14 in the first hour. Return kurtosis 3.4 against 7.9 for 5-minute bars."
- **Reduced motion** Static.

#### 5.17.28 `fracdiff-lab`

composite · tier composite · cluster `ml` · **P2** · size S · spec ML 6.7.3 · first use 2.1 L135

Prices keep memory but are not stationary; returns ($d = 1$) are stationary but have forgotten the level.

- **Composes** `plot-2d`, `marks`, `slider`, `drag-point`, `test-lab`, `series-lab`; mark types `stems`, `paths`, `curve`.
- **Config** `FracdiffLabConfig { series, log, dGrid, tau, show }`.
- **Answers** `numeric`, `point`, `choice`, `curve`.
- **AI hooks** targets `slider:d`, `slider:tau`, `stem:<k>`, `series:original`, `series:fracdiff`, `curve:adf`, `line:critical`, `curve:corr`, `marker:d`; secret: $d^*$; tryable `slider:d`, `slider:tau`.
- **Accessibility** "d = 0.35: 214 weights above τ; ADF −3.1 against a 5% critical value of −2.86: stationary; correlation with log price 0.91." Table of $d$, ADF and correlation.
- **Reduced motion** Static overlays.

#### 5.17.29 `cluster-lab`

composite · tier composite · cluster `ml` · **P2** · size M · spec ML 6.4.6 · first use 2.1 L137

k-means alternates two steps, assign each point to its nearest centroid and move each centroid to its points' mean, and stops at a fixed point that depends on the start; within-cluster sum of squares falls with $k$.

- **Composes** `plot-2d`, `drag-point`, `marks`, `node-link`, `cell-grid`, `stepper`, `slider`, `choice`; mark types `scatter`, `curve`.
- **Config** `ClusterLabConfig { mode, data, k?, linkage?, task }`.
- **Answers** `mapping`, `numeric`, `ordering`, `set`, `state`, `point`.
- **AI hooks** targets `centroid:<j>`, `point:<i>`, `cell:<i>,<j>`, `merge:<m>`, `line:cut`, `curve:elbow`, `chip:<linkage>`; secret: the generating clusters; tryable `chip:<linkage>`.
- **Accessibility** Assignments as a table; the dendrogram as a merge list with heights; the heatmap as a table. "k = 3 after 4 iterations: sizes 40, 35, 25; inertia 61.2."
- **Reduced motion** Steps cut.
- **Modes added** `gmm` mode (P2, 2.1 L142, curriculum).

#### 5.17.30 `overfit-lab`

composite · tier composite · cluster `ml` · **P2** · size L · spec ML 6.8.2 · first use 2.1 L144

Selection is the overfitting.

- **Composes** `plot-2d`, `marks`, `cell-grid`, `slider`, `drag-point`, `sim-runner`, `drawdown-lab`, `sharpe-lab`; mark types `scatter`, `curve`, `field`, `hist`.
- **Config** `OverfitLabConfig { mode, zoo?, sweep?, cscv?, minbtl?, leaderboard?, seed }`.
- **Answers** `choice`, `numeric`, `point`.
- **AI hooks** targets `point:<i>`, `point:picked`, `curve:max-sim`, `curve:max-theory`, `cell:<i>,<j>`, `block:<b>`, `hist:logits`, `area:pbo`, `curve:minbtl`, `handle:research`, `slider:<param>`; secret: which strategies carry a planted edge; tryable `slider:<param>`.
- **Accessibility** "100 noise strategies, 2 years in sample: best in-sample Sharpe 1.83 (theory 1.79); its out-of-sample Sharpe −0.12. CSCV with 16 blocks: PBO 0.63." Tables for scatter points (top 20), the sweep grid and the logit histogram.
- **Reduced motion** Final states only.
- Owns the strategy zoo; `multiple-testing` embeds its zoo panel (ML decision 6).

### 5.18 Time series (2.2)

#### 5.18.1 `acf-lab`

composite · tier composite · cluster `timeseries` · **P1** · size M · spec prob-stats 8.2 · first use 1.6 L56

At lag $k$, plot $x_t$ against $x_{t-k}$; its correlation is the bar $r_k$ of the correlogram.

- **Composes** `plot-2d`, `marks`, `slider`, `drag-point`, `test-lab`, `regression-lab`, `series-lab`; mark types `stems`, `band`.
- **Config** `AcfLabConfig { source, maxLag, mode, show, theory?, predict? }`.
- **Answers** `numeric`, `distribution`, `choice`.
- **AI hooks** targets `slider:lag`, `scatter:lag`, `stem:<k>`, `band`, `pacf:<k>`, `readout:q`; secret: the generating model; tryable `slider:lag`.
- **Accessibility** Table: lag, $r_k$, outside band or not; "Lag 1: 0.62, outside the band. Ljung-Box over 10 lags: Q 210, p below 0.001".
- **Reduced motion** The full correlogram appears.
- Lag scatter and correlogram P1 (1.6 L56 autocorrelated errors); PACF and Ljung-Box P2.

#### 5.18.2 `forecast-lab`

composite · tier composite · cluster `timeseries` · **P1** · size M · spec prob-stats 8.4 · first use 1.6 L64

Forecasts from a stationary model revert to the mean and their intervals saturate; random-walk forecasts are flat and their intervals grow like $\sqrt{h}$.

- **Composes** `plot-2d`, `marks`, `region-select`, `slider`, `choice`, `sim-runner`, `value-table`; mark types `fan`.
- **Config** `ForecastLabConfig { source, methods, h, split, show }`.
- **Answers** `numeric`, `choice`, `ordering`, `interval`.
- **AI hooks** targets `split`, `method:<id>`, `fan:<id>`, `slider:h`, `origin`, `errors`, `table:scores`; tryable `slider:h`.
- **Accessibility** Score table; "AR(1) RMSE 1.02 against naive 1.31 over 50 origins".
- **Reduced motion** Steps without interpolation.
- **Modes added** `ses` and `holt` methods (P2, 2.2 L19, curriculum); Its shuffled-CV comparison embeds `time-cv-lab`'s fold strip and purge logic (decision 5) (P2, ML 5).
- Naive and rolling-origin evaluation P1 (1.6 L64); the rest P2; shuffled-CV comparison embeds `time-cv-lab`'s fold strip.

#### 5.18.3 `series-lab`

composite · tier composite · cluster `timeseries` · **P2** · size M · spec prob-stats 8.1 · first use 2.2 L1

Prices wander and returns hover.

- **Composes** `plot-2d`, `marks`, `region-select`, `slider`, `choice`, `sim-runner`, `value-table`, `acf-lab`; mark types `hist`, `band`, `rug`.
- **Config** `SeriesLabConfig { source, transforms?, editable, panels }`.
- **Answers** `choice`, `numeric`, `state`.
- **AI hooks** targets `series:level`, `series:transformed`, `brush:a`, `brush:b`, `hist:a`, `hist:b`, `band:rolling`, `chip:<transform>`, `slider:window`; describe, e.g. "Random walk, T = 500. Transforms: log, diff. Window A days 50 to 150, B days 350 to 450: means 0.0004 and 0.0001, SDs 0.010 and 0.010."; secret: the generator; tryable `chip:<transform>`, `slider:window`.
- **Accessibility** Window summaries ("Window A: mean 101.2, SD 3.1. Window B: mean 87.6, SD 4.0"); table view of the first 200 rows with CSV export.
- **Reduced motion** no motion of its own.

#### 5.18.4 `arma-lab`

composite · tier composite · cluster `timeseries` · **P2** · size M · spec prob-stats 8.3 · first use 2.2 L11

AR(1) with $\varphi$ is mean reversion with half-life $\frac{\ln 0.5}{\ln \varphi}$; at $\varphi = 1$ the series is a random walk.

- **Composes** `plot-2d`, `complex-plane`, `marks`, `slider`, `drag-point`, `sim-runner`, `acf-lab`, `value-table`.
- **Config** `ArmaLabConfig { p, q, init, editable, show, T, seed }`.
- **Answers** `numeric`, `point`, `choice`, `state`.
- **AI hooks** targets `point:phi`, `triangle`, `root:<i>`, `unit:circle`, `path`, `irf:<k>`, `cell:<p>,<q>`, `slider:<param>`; tryable `slider:<param>`.
- **Accessibility** "AR(2) with phi 1 = 0.5 and phi 2 = 0.3: stationary, real roots; ACF decays without cycles." Tables for ACF and impulse response.
- **Reduced motion** no motion of its own.

#### 5.18.5 `garch-lab`

composite · tier composite · cluster `timeseries` · **P2** · size M · spec prob-stats 8.5 · first use 2.2 L23

$\sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta \sigma_{t-1}^2$: a shock raises tomorrow's variance and the effect decays at rate $\alpha + \beta$.

- **Composes** `plot-2d`, `marks`, `slider`, `drag-point`, `sim-runner`, `acf-lab`, `qq-plot`, `dist-explorer`; mark types `band`, `curve`.
- **Config** `GarchLabConfig { mode, params, innovations, df?, source?, show, T, seed }`.
- **Answers** `numeric`, `point`, `choice`, `state`.
- **AI hooks** targets `slider:<param>`, `series:returns`, `band:sigma`, `map:loglik`, `handle:ab`, `boundary`, `curve:term`, `curve:nic`, `exceed:<i>`; secret: the true parameters and the MLE; tryable `slider:<param>`.
- **Accessibility** "GARCH(1,1), omega 0.02, alpha 0.08, beta 0.90: persistence 0.98, long-run daily SD 1.0%, half-life 34 days."
- **Reduced motion** no motion of its own.
- **Modes added** `gjr` with the news impact curve (P2, 2.2 L26, curriculum).

#### 5.18.6 `coint-lab`

composite · tier composite · cluster `timeseries` · **P2** · size M · spec prob-stats 8.6 · first use 2.2 L35

Two non-stationary prices that share a stochastic trend have a stationary combination $y_t - \beta x_t$.

- **Composes** `plot-2d`, `marks`, `slider`, `drag-point`, `sim-runner`, `test-lab`, `regression-lab`, `sde-stepper`, `code-cell`, `free-response`.
- **Config** `CointLabConfig { pair, steps, editable, task? }`.
- **Answers** `numeric`, `choice`, `state`, `code`, `long-form`.
- **AI hooks** targets `series:y`, `series:x`, `scatter`, `handle:beta`, `spread`, `band:entry`, `band:exit`, `readout:adf`, `line:critical`, `panel:ecm`, `split`; describe, e.g. "Pair: cointegrated (hidden). β = 1.40. Step 1 done (OLS β 1.52). Spread ADF −2.1."; secret: the pair's kind and true $\beta$.
- **Accessibility** "Your beta 1.40: spread ADF −2.1; Engle-Granger 5% critical value −3.37: unit root not rejected." Table view of both series with CSV export.
- **Reduced motion** no motion of its own.
- **Modes added** pairs selected by distance from `pairs-lab` (P2, ML 5).

### 5.19 Projects (2.3)

#### 5.19.1 `signal-lab`

composite · tier composite · cluster `projects` · **P2** · size M · spec finance 7.3, ML 7.2 · first use 2.1 L136

Research is measuring a weak relationship across many stocks: an IC of 0.03 is invisible on any one date and valuable across hundreds of names and years.

- **Composes** `plot-2d`, `marks`, `slider`, `region-select`, `token-tray`, `value-table`, `numeric-input`, `choice`, `portfolio-sort`, `sharpe-lab`, `sim-runner`, `live-formula`; mark types `scatter`, `bars`, `paths`, `curve`; services `market-gen`.
- **Config** `SignalLabConfig { mode, panel, recipe?, quantiles, cost, source, operators?, fields?, delay, enforceDelay, panels, costBps? }`.
- **Answers** `numeric`, `ordering`, `choice`, `code`, `state`, `expression`.
- **AI hooks** targets `token:<k>`, `slider:<param>`, `date:<d>`, `scatter`, `series:ic`, `band:se`, `bar:q<k>`, `bar:long-short`, `line:turnover`, `token:<i>`, `slot:<path>`, `stem:<h>` and 6 more; secret: the planted IC and decay; tryable `slider:<param>`, `chip:<neutraliser>`, `slider:cost`, `slider:breadth`.
- **Accessibility** "Momentum 12-1, sector neutral: mean rank IC 0.031 over 120 months, t 2.4; quantile spread 0.42% a month; one-way turnover 38% a month; net Sharpe 0.41 at 10 bp." Tables for every panel.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- One widget: finance's cross-sectional signal research (IC by date, decay, quantile spreads, turnover, Sharpe after costs) plus ML's breadth and formulaic alphas from typed operator tokens (finance-projects request 4).

#### 5.19.2 `results-note`

composite · tier composite · cluster `projects` · **P2** · size M · spec finance 7.11 · first use 2.1 L151

The curriculum asks for a note that includes what failed.

- **Composes** `free-response`, `value-table`, `setup-checklist`.
- **Config** `ResultsNoteConfig { project, sections, metricsSchema, rubric, flags }`.
- **Answers** `long-form`, `state`.
- **AI hooks** targets `section:<id>`, `metric:<name>`, `check:<id>`, `mark:<item>`.
- **Accessibility** Real text areas; each check is announced on blur.
- **Reduced motion** no motion of its own.

#### 5.19.3 `backtest-lab`

composite · tier composite · cluster `projects` · **P2** · size L · spec finance 7.1 · first use 2.3 L4

Most backtests that look good are wrong in one of a few known ways.

- **Composes** `stepper`, `plot-2d`, `marks`, `region-select`, `slider`, `value-table`, `code-surface`, `node-link`, `card-sort`, `live-formula`, `numeric-input`, `choice`; mark types `event-rug`, `signed-fill`; services `backtest-core`, `price-series`, `market-gen`.
- **Config** `BacktestLabConfig { mode, data, strategy, fill, costs, biases?, holdout?, code? }`.
- **Answers** `ordering`, `choice`, `numeric`, `set`, `mapping`, `state`, `code`.
- **AI hooks** targets `step:<n>`, `window`, `row:<date>`, `toggle:<bias>`, `curve:equity`, `curve:biased`, `bracket:<id>`, `line:<n>`, `metric:<name>`, `component:<id>`; secret: the planted bias and the bug lines; tryable `toggle:<bias>`.
- **Accessibility** "Bar 2023-05-04: signal long; target 100 shares; order filled at the next open, 101.20; equity 10,412." Metrics table; the data window is a table.
- **Reduced motion** Steps cut; runs appear at once.

#### 5.19.4 `sharpe-lab`

composite · tier composite · cluster `projects` · **P2** · size M · spec finance 7.2, ML 6.8.1 · first use 2.3 L7

A Sharpe ratio is an estimate with a wide error bar.

- **Composes** `sim-runner`, `plot-2d`, `marks`, `slider`, `value-table`, `live-formula`, `numeric-input`, `choice`, `drawdown-lab`, `multiple-testing`, `drag-point`, `dist-explorer`, `qq-plot`; mark types `hist`, `curve`, `band`.
- **Config** `SharpeLabConfig { mode, returns?, sim?, autocorrelation?, reported?, trials?, tests?, editable }`.
- **Answers** `numeric`, `choice`, `ordering`.
- **AI hooks** targets `hist:null`, `marker:learner`, `line:p95`, `slider:<param>`, `curve:years`, `hist:srhat`, `curve:theory`, `line:true`, `handle:srhat`, `curve:psr`, `line:benchmark`, `bar:reported` and 2 more; secret: the true Sharpe ratio of generated returns; tryable `slider:<param>`.
- **Accessibility** "1,000 null strategies over 3 years: 95th percentile Sharpe 0.95; your strategy 0.90." Histogram table view.
- **Reduced motion** Final histograms at once.
- One widget: finance's performance metrics and their noise (SE, $t$, Sortino, Calmar, drawdown distribution, best of many nulls, deflated Sharpe) and ML's sampling error, annualisation, fat tails and deflations were one idea specified twice (finance-projects request 4).

#### 5.19.5 `paper-trader`

composite · tier composite · cluster `projects` · **P2** · size M · spec finance 7.10 · first use 2.3 L17

Build the curriculum's fifth project's strategy logic, then test it against random entries with the same number of trades.

- **Composes** `plot-2d`, `marks`, `token-tray`, `slider`, `sim-runner`, `value-table`, `numeric-input`, `choice`; mark types `candles`, `trade-glyphs`; services `backtest-core`.
- **Config** `PaperTraderConfig { mode, series, indicators, rule?, cost, nullRuns? }`.
- **Answers** `numeric`, `state`, `choice`.
- **AI hooks** targets `token:<k>`, `slider:<param>`, `series:ema:<n>`, `panel:rsi`, `trade:<n>`, `curve:equity`, `band:null`; tryable `slider:<param>`.
- **Accessibility** "Rule: 23 trades, net return 6.1% after costs; 41% of random strategies did better." Tables of indicator values and trades.
- **Reduced motion** At once.

#### 5.19.6 `order-lifecycle`

composite · tier composite · cluster `projects` · **P2** · size M · spec finance 7.9 · first use 2.3 L63

A bot is mostly bookkeeping under uncertainty: an order can be filled while your cancel is in flight, a fill message can arrive twice, and after a crash your own records are the least trustworthy thing you have.

- **Composes** `node-link`, `order-ticket`, `value-table`, `token-tray`, `stepper`, `card-sort`, `numeric-input`, `choice`; services `exchange-sim`, `ledger`.
- **Config** `OrderLifecycleConfig { mode, events?, limits? }`.
- **Answers** `set`, `ordering`, `mapping`, `state`.
- **AI hooks** targets `order:<clOrdId>`, `event:<n>`, `state:<name>`, `row:local:<id>`, `row:broker:<id>`, `limit:<name>`, `kill`.
- **Accessibility** "Order C-17: new, then partially filled 200 of 500, then pending cancel; a fill of 300 arrives." Tables are the table view.
- **Reduced motion** Instant.
- **Modes added** `reconcile-diff` (P2, 2.3 L218, curriculum).

#### 5.19.7 `vol-surface`

composite · tier composite · cluster `projects` · **P2** · size M · spec finance 7.4 · first use 2.3 L144

The surface is where Black-Scholes is used as a quoting language.

- **Composes** `plot-2d`, `plot-3d`, `slider`, `region-select`, `value-table`, `numeric-input`, `choice`, `option-chain`.
- **Config** `VolSurfaceConfig { mode, surface, forward, r }`.
- **Answers** `set`, `choice`, `numeric`, `state`.
- **AI hooks** targets `smile:<expiry>`, `point:<expiry>:<K>`, `line:w:<expiry>`, `density`, `slider:<param>`, `surface`; secret: the planted violations; tryable `slider:<param>`.
- **Accessibility** Strike-by-expiry grid as the table view; "Expiry 3 months: total variance crosses the 6-month line at log-moneyness −0.35."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** `event` term structures (P2, 2.3 L150, curriculum); `local-vol` and `heston` (P2, 3.2 L101, L102, curriculum).

#### 5.19.8 `pricer-compare`

composite · tier composite · cluster `projects` · **P2** · size M · spec finance 7.5 · first use 2.3 L160

The options dashboard compares pricers; the learner should know before coding that a tree's error falls like $1/N$ with an odd-even wobble, Monte Carlo's like $1/\sqrt{N}$.

- **Composes** `plot-2d`, `slider`, `sim-runner`, `value-table`, `numeric-input`, `choice`, `binomial-tree`, `gbm-lab`.
- **Config** `PricerCompareConfig { mode, option, NRange, pathsRange, seed }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `series:tree`, `series:mc`, `line:exact`, `slider:N`, `slider:paths`, `toggle:antithetic`, `toggle:control`; tryable `slider:N`, `slider:paths`, `toggle:antithetic`, `toggle:control`.
- **Accessibility** Table of method, $N$, price, error and time.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** `pde` method (P2, 2.3 L164, curriculum).

#### 5.19.9 `feed-sim`

composite · tier composite · cluster `projects` · **P2** · size M · spec finance 7.6 · first use 2.3 L180

A feed handler is correct only if it notices when it has missed something.

- **Composes** `price-ladder`, `code-surface`, `stepper`, `node-link`, `token-tray`, `value-table`, `numeric-input`, `choice`, `json-explorer`; services `exchange-sim`.
- **Config** `FeedSimConfig { mode, stream, backoff? }`.
- **Answers** `set`, `ordering`, `numeric`, `state`.
- **AI hooks** targets `msg:<seq>`, `level:<tick>`, `state:<name>`, `step:<k>`, `delay:<k>`; secret: gap positions.
- **Accessibility** Messages are text; "Message 1043 follows 1041: one message missing."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.19.10 `candle-builder`

composite · tier composite · cluster `projects` · **P2** · size M · spec finance 7.7 · first use 2.3 L192

Candles look trivial and hide conventions: which bar owns a tick at exactly 10:01:00, what to do with a tick that arrives late, and why a 5-minute bar must be built from 1-minute bars rather than ticks once the ticks are gone.

- **Composes** `plot-2d`, `marks`, `array-strip`, `region-select`, `drag-point`, `value-table`, `numeric-input`, `card-sort`, `choice`; mark types `candles`, `trade-glyphs`.
- **Config** `CandleBuilderConfig { mode, ticks, interval, closed, label, tz? }`.
- **Answers** `numeric`, `mapping`, `choice`, `state`.
- **AI hooks** targets `tick:<n>`, `bar:<start>`, `window`, `boundary:<t>`, `field:<o|h|l|c|v>`.
- **Accessibility** "Bar 10:00 to 10:01: 14 ticks; open 100.02, high 100.09, low 99.98, close 100.05, volume 3,200."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.19.11 `latency-lab`

composite · tier composite · cluster `projects` · **P2** · size M · spec finance 7.8 · first use 2.3 L197

Latency is a distribution, not a number; its tail is what hurts; measuring it honestly takes synchronised clocks and a load generator that does not wait for slow replies.

- **Composes** `node-link`, `plot-2d`, `marks`, `drag-point`, `slider`, `sim-runner`, `value-table`, `numeric-input`, `choice`.
- **Config** `LatencyLabConfig { mode, samples?, pipeline?, queue? }`.
- **Answers** `numeric`, `point`, `choice`.
- **AI hooks** targets `stage:<name>`, `hist`, `handle:<p>`, `line:true:<p>`, `slider:rate`, `curve:wait`; tryable `slider:rate`.
- **Accessibility** "p50 180 microseconds, p99 2.1 milliseconds, p99.9 9.8 milliseconds; mean 310 microseconds." Histogram table.
- **Reduced motion** At once.
- **Modes added** `histogram-from-log` (P2, MS4 homework, curriculum).

### 5.20 Research papers (3.1)

#### 5.20.1 `factor-model-lab`

composite · tier composite · cluster `research` · **P1** · size L · spec ML 7.3 · first use 1.7 L28

Fama and French (1993) explain the cross-section of returns with three factors.

- **Composes** `plot-2d`, `slider`, `marks`, `cell-grid`, `regression-lab`, `summary-table`, `dist-explorer`, `stepper`, `choice`, `portfolio-sort`, `matrix`, `live-formula`; mark types `scatter`, `bars`, `paths`.
- **Config** `FactorModelLabConfig { source, mode, models, portfolio?, se?, task }`.
- **Answers** `numeric`, `choice`, `code`, `state`.
- **AI hooks** targets `point:<portfolio>`, `line:capm`, `line:fit`, `slider:b`, `slider:s`, `slider:h`, `cell:<size>,<value>`, `readout:alpha`, `readout:grs`, `series:lambda`, `chip:<model>`; secret: the planted factor structure; tryable `slider:b`, `slider:s`, `slider:h`, `chip:<model>`.
- **Accessibility** Grids as tables; "Small-value portfolio on three factors: alpha 0.12% a month (t 1.4), b 1.02, s 1.31, h 0.74, R squared 0.94. CAPM alpha was 0.61% (t 3.2)."
- **Reduced motion** Before-and-after.
- CAPM single-factor mode P1 for 1.7 L28; three-factor, GRS and Fama-MacBeth P2.

#### 5.20.2 `portfolio-sort`

composite · tier composite · cluster `research` · **P2** · size L · spec ML 7.1 · first use 2.1 L127

The empirical method behind most of 3.1.

- **Composes** `plot-2d`, `drag-point`, `span-track`, `marks`, `cell-grid`, `slider`, `choice`, `stepper`, `value-table`, `regression-lab`, `sim-runner`; mark types `gantt`, `scatter`, `bars`, `paths`.
- **Config** `PortfolioSortConfig { panel, sort, characteristic, windows, quantiles, breakpoints, weighting, filters?, grid?, task }`.
- **Answers** `numeric`, `set`, `state`, `choice`, `code`.
- **AI hooks** targets `handle:bp:<i>`, `decile:<q>`, `path:wml`, `cell:<J>,<K>`, `cohort:<c>`, `span:<cohort>:<window>`, `chip:<characteristic>`, `toggle:<filter>`, `slider:<window>`; secret: planted premia, decay and $t_{\text{pub}}$; tryable `chip:<characteristic>`, `toggle:<filter>`, `slider:<window>`.
- **Accessibility** The decile table (mean, $t$, SD, average stocks).
- **Reduced motion** Cohort changes cut.
- **Modes added** `hansen-hodrick` beside Newey-West (P2, 3.1 L16, curriculum).

#### 5.20.3 `pairs-lab`

composite · tier composite · cluster `research` · **P2** · size M · spec ML 7.4 · first use 2.3 L79

Normalise each stock's total-return index to 1 at the start of a 12-month formation period; for every pair compute the sum of squared deviations $\text{SSD}_{AB} = \sum_t (P^A_t - P^B_t)^2$; take the pairs with the smallest SSD.

- **Composes** `plot-2d`, `cell-grid`, `span-track`, `marks`, `slider`, `drag-point`, `choice`, `coint-lab`, `sde-stepper`, `sim-runner`, `value-table`; mark types `paths`, `band`.
- **Config** `PairsLabConfig { universe, formationDays, tradingDays, threshold, topN, wait, basis, costBps, mode, task? }`.
- **Answers** `numeric`, `set`, `point`, `choice`, `matrix`.
- **AI hooks** targets `cell:<a>,<b>`, `series:a`, `series:b`, `series:spread`, `band:upper`, `band:lower`, `marker:open:<k>`, `marker:close:<k>`, `span:trade:<k>`, `toggle:wait`, `chip:<basis>`, `slider:threshold`; secret: the true clusters and break dates; tryable `toggle:wait`, `chip:<basis>`, `slider:threshold`.
- **Accessibility** The SSD matrix as a ranked table of pairs; trades as a table (open, close, legs, return); "Top 20 pairs, 6-month trading, committed capital: 0.71% a month before costs, 0.38% after 10 basis points per side."
- **Reduced motion** Static.

#### 5.20.4 `replication-workbench`

composite · tier composite · cluster `research` · **P2** · size L · spec ML 7.6 · first use 3.1 L1

The 3.1 method in one place.

- **Composes** `value-table`, `cell-grid`, `span-track`, `plot-2d`, `marks`, `card-sort`, `free-response`, `viva`, `setup-checklist`, `code-cell`, `summary-table`.
- **Config** `ReplicationWorkbenchConfig { paper, card, table?, ledger, compareTo, periods?, rubric, mode }`.
- **Answers** `mapping`, `numeric`, `interval`, `set`, `long-form`, `code`, `state`.
- **AI hooks** targets `cell:<row>,<col>`, `ledger:<field>`, `band:in-sample`, `band:post-sample`, `band:post-publication`, `readout:ratio`, `note`, `rubric:<k>`; secret: rehearsal truth (planted premium and decay). Bertie reviews the note at the `complex` tier on request, after the learner's self-mark.
- **Accessibility** All tables are real tables; "Momentum 6-1-6 on rehearsal data: in-sample 0.94% a month (t 4.4); post-publication 0.41% (t 1.6). Survival ratio 0.44, 95% interval 0.05 to 0.83."
- **Reduced motion** Static.

### 5.21 Stochastic calculus (3.2)

#### 5.21.1 `hedging-sim`

composite · tier composite · cluster `stochastic` · **P1** · size M · spec calc-linalg 7.10 · first use 1.7 L78

Black-Scholes-Merton by replication: short a call, hold $\Delta$ shares, rebalance every $\Delta t$; hedging error shrinks like one over the square root of the number of rebalances.

- **Composes** `plot-2d`, `sim-runner`, `slider`, `marks`, `value-table`, `numeric-input`, `choice`.
- **Config** `HedgingSimConfig { K, T, r, sigmaImplied, sigmaRealised, rebalance, values, seed, paths, mode }`.
- **Answers** `numeric`, `choice`, `long-form`.
- **AI hooks** targets `slider:rebalance`, `slider:sigma-realised`, `slider:sigma-implied`, `path`, `pnl`, `hist:error`; tryable `slider:rebalance`, `slider:sigma-realised`, `slider:sigma-implied`.
- **Accessibility** "Rebalancing 52 times: hedging error standard deviation 1.9; 208 times: 0.96."
- **Reduced motion** At once.
- **Modes added** The `one-path` mode promoted to P1 with a daily-rebalance default and a gamma-theta split per day (P1, finance 5).
- One-path mode P1 with daily rebalance and a gamma-theta split (finance 5; 1.7 L78); distribution mode P2.

#### 5.21.2 `sde-stepper`

composite · tier composite · cluster `stochastic` · **P2** · size M · spec calc-linalg 7.12 · first use 2.2 L40

Simulate stochastic differential equations with Euler-Maruyama: arithmetic and geometric Brownian motion, Ornstein-Uhlenbeck, Vasicek and CIR; mean reversion.

- **Composes** `plot-2d`, `sim-runner`, `slider`, `expression-input`, `marks`, `value-table`, `numeric-input`, `choice`.
- **Config** `SdeStepperConfig { drift?, diffusion?, x0, params, dtValues, T, seed, paths, compareExact?, stationary? }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `slider:<param>`, `dt:<value>`, `path:<i>`, `line:mean`, `density:stationary`, `plot:error`, `field:drift`, `field:diffusion`; tryable `slider:<param>`.
- **Accessibility** Parameters and statistics read out; the error table by $\Delta t$.
- **Reduced motion** At once.
- **Modes added** Ornstein-Uhlenbeck half-life (P2, prob-stats 5); `cir-feller` mode (P2, 3.2 L84, curriculum).

#### 5.21.3 `measure-change`

composite · tier composite · cluster `stochastic` · **P2** · size M · spec calc-linalg 7.7 · first use 3.2 L30

Risk-neutral pricing and Girsanov's theorem: changing probabilities (reweighting paths) changes the drift, not the volatility.

- **Composes** `plot-2d`, `sim-runner`, `slider`, `marks`, `live-formula`, `numeric-input`, `choice`.
- **Config** `MeasureChangeConfig { r, sigma, S0, T, seed, paths, mode, u?, d? }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `slider:theta`, `slider:q`, `hist:P`, `hist:Q`, `readout:mean-Q`, `tree`; tryable `slider:theta`, `slider:q`.
- **Accessibility** "Under the reweighting, the discounted mean is 100.4 against S0 = 100."
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** `importance-sampling` mode (P2, 3.2 L31, curriculum).

#### 5.21.4 `quadratic-variation`

composite · tier composite · cluster `stochastic` · **P2** · size M · spec calc-linalg 7.2 · first use 3.2 L41

The roughness that defines Brownian motion: as the partition refines, $\sum(\Delta W)^2\to T$ while $\sum\lvert\Delta W\rvert\to\infty$; a smooth path has zero quadratic variation.

- **Composes** `plot-2d`, `sim-runner`, `slider`, `marks`, `value-table`, `numeric-input`, `choice`.
- **Config** `QuadraticVariationConfig { T, kRange, comparison?, show }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `slider:k`, `path`, `ticks`, `qv`, `tv`, `line:t`; tryable `slider:k`.
- **Accessibility** Table of $k$, total variation and quadratic variation.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.21.5 `heat-diffusion`

composite · tier composite · cluster `stochastic` · **P2** · size M · spec calc-linalg 7.11 · first use 3.2 L45

The Black-Scholes PDE as a heat equation: going back from expiry, the price curve is the payoff smoothed by a Gaussian kernel; equivalently, each point's value is the average payoff over paths that start there (Feynman-Kac).

- **Composes** `plot-2d`, `sketch-pad`, `slider`, `sim-runner`, `marks`, `plot-3d`.
- **Config** `HeatDiffusionConfig { sketch, sigma, r, tauRange, showPaths, seed, view3d? }`.
- **Answers** `curve`, `numeric`, `choice`, `point`.
- **AI hooks** targets `slider:tau`, `curve:price`, `payoff`, `probe`, `paths:probe`, `sketch`; tryable `slider:tau`.
- **Accessibility** Curve values at strikes read out; a table of $S$ against value.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).
- **Modes added** `finite-difference` mode (P2, 3.2 L88, curriculum).

#### 5.21.6 `reflection-principle`

composite · tier composite · cluster `stochastic` · **P2** · size M · spec calc-linalg 7.3 · first use 3.2 L46

$P(\max_{t\le T}W_t\ge m)=2P(W_T\ge m)=2\bigl(1-\Phi(m/\sqrt T)\bigr)$ for $m>0$, by reflecting each path after it first hits $m$; the lattice-path version for random walks.

- **Composes** `plot-2d`, `sim-runner`, `drag-point`, `marks`, `value-table`, `live-formula`, `numeric-input`, `choice`.
- **Config** `ReflectionPrincipleConfig { seed, T, m, movableM, paths }`.
- **Answers** `numeric`, `choice`, `ordering`.
- **AI hooks** targets `handle:m`, `path:<i>`, `reflected:<i>`, `tau:<i>`, `tally:<k>`.
- **Accessibility** Tallies read as counts and fractions.
- **Reduced motion** The reflection appears at once.
- **Modes added** `drift` mode (P2, 3.2 L49, L50, L90, curriculum).

#### 5.21.7 `ito-sum`

composite · tier composite · cluster `stochastic` · **P2** · size M · spec calc-linalg 7.4 · first use 3.2 L52

The Itô integral as the limit of left-point (non-anticipating) sums; why the evaluation point matters for Brownian motion and not for smooth integrators; $\int_0^TW\,dW=\frac12(W_T^2-T)$.

- **Composes** `plot-2d`, `sim-runner`, `slider`, `choice`, `marks`, `live-formula`, `numeric-input`.
- **Config** `ItoSumConfig { seed, T, kRange, rules }`.
- **Answers** `numeric`, `choice`.
- **AI hooks** targets `slider:k`, `rule:<r>`, `sum:<r>`, `step:<i>`, `path`; tryable `slider:k`, `rule:<r>`.
- **Accessibility** Table of $k$ against each sum.
- **Reduced motion** baseline (springs and tweens land at once; show-why plays as a before-and-after pair with Play).

#### 5.21.8 `ito-lemma-lab`

composite · tier composite · cluster `stochastic` · **P2** · size M · spec calc-linalg 7.5 · first use 3.2 L57

Make Itô's lemma visible: for convex $f$, the average of $f(W_t)$ drifts upwards at rate $\frac12f''$; $f(W_t)-\int_0^t\frac12f''(W_s)\,ds$ has a flat average (a martingale).

- **Composes** `plot-2d`, `sim-runner`, `choice`, `slider`, `marks`, `derivation-steps`, `numeric-input`, `expression-input`.
- **Config** `ItoLemmaLabConfig { seed, T, paths, show, mean, predicted, compensated, zoomStep? }`.
- **Answers** `choice`, `numeric`, `expression`, `ordering`.
- **AI hooks** targets `path:mean`, `curve:predicted`, `toggle:compensated`, `bar:first-order`, `bar:second-order`, `option:<f>`; tryable `toggle:compensated`.
- **Accessibility** "The mean of W_t² over 500 paths at t = 1 is 1.03 (theory 1)."
- **Reduced motion** Paths at once.

### 5.22 Interview preparation (3.3)

#### 5.22.1 `bet-lab`

composite · tier composite · cluster `interview` · **P2** · size M · spec finance 8.2 · first use 2.3 L11

Interviewers ask "would you play this game, and for how much?" The answer is an expected value, a variance and a bankroll consideration, in that order.

- **Composes** `value-table`, `mass-editor`, `chance-object`, `slider`, `plot-2d`, `numeric-input`, `choice`, `game-lab`, `kelly-lab`.
- **Config** `BetLabConfig { mode, outcomes?, books?, game?, format, seed? }`.
- **Answers** `numeric`, `choice`, `state`.
- **AI hooks** targets `row:<outcome>`, `stake:<k>`, `slider:price`, `book:<id>`, `device`; tryable `slider:price`.
- **Accessibility** "Game: pay 3.50 to roll a die and receive the face value. Expected value 3.50; fair."
- **Reduced motion** Devices show results with a cross-fade.

#### 5.22.2 `mock-interview`

composite · tier composite · cluster `interview` · **P2** · size L · spec finance 8.6 · first use 2.3 L41

Interviewers mark the reasoning as it happens.

- **Composes** `voice-capture`, `scratch-pad`, `speed-timer`, `puzzle-workbench`, `mm-game`, `speed-drill`, `free-response`, `value-table`, `plot-2d`; services `interview-engine`, `speech`, `problem-bank`.
- **Config** `MockInterviewConfig { mode, track, rounds, style, voice, rubric, banks, silencePromptS, hintAfterS }`.
- **Answers** `state`.
- **AI hooks** targets `marker:<n>`, `segment:<n>`, `mark:<item>`, `item:<n>`.
- **Accessibility** Captions always on; typed answers count the same; timing can be relaxed and is recorded as adjusted.
- **Reduced motion** Bertie's speaking animation becomes a static "speaking" label.

#### 5.22.3 `mm-game`

composite · tier composite · cluster `interview` · **P2** · size L · spec finance 8.4 · first use 3.3 L84

Trader interviews test whether you can turn a probability into a price, set a width that reflects uncertainty and adverse selection, move when you are hit, and stay consistent across related markets, all aloud and quickly.

- **Composes** `quote-entry`, `number-line`, `chance-object`, `price-ladder`, `value-table`, `speed-timer`, `voice-capture`, `scratch-pad`, `plot-2d`, `fermi-estimator`, `calibration-lab`; services `exchange-sim`, `ledger`, `interview-engine`.
- **Config** `MmGameConfig { mode, quantity, reveals?, counterparties, rules, scoring, seed }`.
- **Answers** `numeric`, `state`.
- **AI hooks** targets `interview:engine`, `quote:<n>`, `trade:<n>`, `reveal:<n>`, `posterior:<n>`, `band`, `inventory`; secret: the hidden value and every bot's policy.
- **Accessibility** "Round 3. Two dice, one shows 5. Your market 8 at 10. Trader B buys 1 at 10. Position short 1." Untimed mode is always offered; timed scores carry their mode.
- **Reduced motion** Reveals cross-fade; actions appear at once.
- **Modes added** `figgie` mode (P2, 3.3 L92, curriculum).
- Seeded bots decide every trade; Bertie only narrates and debriefs (finance decision 5).

---

## 6. Presets

23 presets. Each is a `PresetDef` (arch 5.3): its `expand` runs in the compiler and the result is validated by the base widget's schema; its predicates and recipes register as `<preset>/<name>`. The base widget must carry every mode a preset needs; those modes are listed under the base's entry.

### 6.1 The `algo-lab` family

`algo-lab` (entry 5 under Data structures, algorithms and contests) runs a named `algo-trace` algorithm on a seeded or authored instance and binds its state to panes. Each preset fixes the algorithm family, the panes and their layouts, the moves the learner may make, the predicates (`isHeap`, `listShape`, `moveMatchesAlgorithm` with the tie rule), the show-why recipes and the generator. The CI parity rule of programming decision 5 applies to every algorithm: the JavaScript trace and the Python under `sys.settrace` must emit the same (event, line) sequence.

#### 6.1.1 `sort-lab`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P0** · size M · spec programming 7.2 · first use 1.1 L19

Sorting with keys, then the algorithms themselves: insertion, selection, merge, quick (Lomuto and Hoare partitions), heap, counting and radix sort, stability, the comparison lower bound, and comparators in C++.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- Algorithms and panes: insertion, selection, merge, quick (Lomuto, Hoare), heap, counting and radix sort on an `array-strip` of bars or records.
- Priority: key and stability modes P0 (1.1 L19); algorithms P1.

#### 6.1.2 `recursion-tree`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P0** · size S · spec programming 7.16 · first use 1.1 L21

Recursion made visible: the call tree growing in execution order with the stack beside it, backtracking with pruning, memoisation collapsing repeated calls, divide and conquer, and the recursion-tree method for recurrences.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- Algorithms and panes: call tree growing in execution order on `node-link` with the stack on `array-strip`; memoisation collapses repeated calls.
- Priority: P1 in the catalogue; pulled to P0 for 1.1 L21 and L33 (python-tools decision 19).

#### 6.1.3 `hash-table`

preset of `algo-lab` · composite · tier preset · cluster `python` · **P0** · size M · spec programming 4.14 · first use 1.1 L25

How hashing turns a key into a bucket, why lookups are $O(1)$ on average and $O(n)$ at worst, why keys must not change, and what resizing costs.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- Algorithms `hash.chaining`, `hash.open-addressing`, `hash.resize`; panes: bucket `array-strip` with `node-link` chains; controls: load factor; readouts: probes per lookup; P1 parts are open addressing, resizing cost and adversarial keys.

#### 6.1.4 `dynamic-array`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size S · spec programming 7.3 · first use 1.8 L4

Why `append` is cheap on average: a buffer with spare capacity, reallocation when full, and the amortised cost.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- Algorithms and panes: buffer with spare capacity, reallocation and amortised cost; `array-strip` plus a cost `plot-2d` readout.
- Priority: P1.

#### 6.1.5 `heap-lab`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size S · spec programming 7.12 · first use 1.8 L23

A binary heap as a tree and as an array at once: sift up after a push, sift down after a pop, bottom-up heapify in $O(n)$, heap sort, top-$k$, the running median with two heaps, and $k$-way merging.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- Algorithms and panes: heap as `node-link` tree and `array-strip` array at once: sift, heapify, top-$k$, two-heap median.
- Priority: P1.

#### 6.1.6 `pointer-walk`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size S · spec programming 7.4 · first use 1.8 L30

Two pointers and sliding windows: pointers from both ends, fast and slow pointers on arrays, fixed and variable windows, three-way partitioning, and merging.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- **Modes added** `reach` mode (P1, 1.8, dsa-cpp request 6, curriculum).
- Algorithms and panes: two pointers and sliding windows on `array-strip` with the pair grid on `cell-grid`.
- Priority: P1.

#### 6.1.7 `range-query-lab`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size M · spec programming 7.5 · first use 1.8 L34

Answering many range queries fast: prefix sums and products, difference arrays for range updates, 2D prefix sums by inclusion-exclusion, then Fenwick and segment trees for contests.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- **Modes added** sparse table (P2, 2.4, dsa-cpp request 6, curriculum).
- Algorithms and panes: prefix sums, difference arrays, 2D prefix sums on `array-strip` and `cell-grid`, trees on `node-link`.
- Priority: prefix and difference families P1; Fenwick, segment tree and sparse table P2.

#### 6.1.8 `stack-queue-lab`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size S · spec programming 7.7 · first use 1.8 L40

Stacks, queues, deques and ring buffers, and the patterns built on them: bracket matching, Reverse Polish evaluation, the min stack, monotonic stacks and deques, a queue from two stacks.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- Algorithms and panes: stacks, queues, deques, ring buffers and monotonic stacks on `array-strip`.
- Priority: P1.

#### 6.1.9 `dp-table`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size M · spec programming 7.17 · first use 1.8 L45

Dynamic programming as a table you fill: state, recurrence, fill order, dependencies, and reconstruction of the answer, in one and two dimensions, with state machines, rolling arrays and the top-down against bottom-up comparison.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- Algorithms and panes: fill a `cell-grid` in dependency order, with dependency arrows, rolling arrays and reconstruction.
- Priority: P1.

#### 6.1.10 `binary-search-lab`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size S · spec programming 7.6 · first use 1.8 L46

Binary search done right: the invariant, closed and half-open conventions, updates that always shrink the range, `bisect_left` against `bisect_right`, searching a monotone predicate over an answer space.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- Algorithms and panes: `lo`, `hi` and `mid` markers on `array-strip`, monotone predicates over an answer space, sorted matrices on `cell-grid`.
- Priority: P1.

#### 6.1.11 `linked-list-lab`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size S · spec programming 7.8 · first use 1.8 L63

Nodes and pointers you rewire by hand: traversal, insertion and deletion with a dummy head, in-place reversal, fast and slow pointers, merging, the LRU cache, and copying a list with random pointers.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- Algorithms and panes: nodes and `next` pointers on `node-link` that the learner rewires; unreachable nodes grey out.
- Priority: P1.

#### 6.1.12 `tree-lab`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size M · spec programming 7.11 · first use 1.8 L79

Binary trees and their recursions, binary search trees, balance, construction from traversals, serialisation, lowest common ancestors and tries.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- **Modes added** Euler tour and binary lifting (P1, 1.8, dsa-cpp request 6, curriculum).
- Algorithms and panes: traversals, BSTs, balance, construction from traversals, tries on `node-link`.
- Priority: P1; B-tree mode P2.

#### 6.1.13 `graph-search`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size M · spec programming 7.13 · first use 1.8 L91

Graphs and how to explore them: representations, BFS with layers and shortest unweighted paths, multi-source BFS, DFS with discovery and finish times, components and flood fill, cycle detection with three colours.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- **Modes added** SCC, bridges and 2-SAT (P1, 1.8, dsa-cpp request 6, curriculum).
- Algorithms and panes: BFS layers, DFS times, components, cycles, topological sort on `node-link` with the frontier on `array-strip`.
- Priority: P1.

#### 6.1.14 `shortest-path`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size M · spec programming 7.14 · first use 1.8 L98

Weighted graphs: Dijkstra's algorithm with a priority queue, why negative edges break it, Bellman-Ford and its $k$-stops variant, and minimum spanning trees by Prim and Kruskal with the cut property.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- **Modes added** Floyd-Warshall (P1, 1.8, dsa-cpp request 6, curriculum).
- Algorithms and panes: Dijkstra, Bellman-Ford, Prim and Kruskal on `node-link` with the heap on `array-strip`.
- Priority: P1; 0-1 BFS mode P2.

#### 6.1.15 `union-find`

preset of `algo-lab` · composite · tier preset · cluster `algorithms` · **P1** · size S · spec programming 7.15 · first use 1.8 L102

Disjoint sets as a forest and a parent array: union by rank or size, path compression, component counting, finding the redundant edge, and its role in Kruskal's algorithm.

- **Composes** `algo-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `algo-lab`; `describeAs` names the preset.
- Algorithms and panes: forest on `node-link` and parent array on `array-strip`; union by rank, path compression.
- Priority: P1.

### 6.2 Other presets

#### 6.2.1 `times-table-grid`

preset of `cell-grid` · composite · tier preset · cluster `number` · **P0** · size S · spec stage0 11.3 · first use 0.5 L2

The multiplication facts to 12 × 12 as a map.

- **Composes** `cell-grid`.
- **Answers, AI hooks, accessibility and reduced motion** those of `cell-grid`; `describeAs` names the preset.
- Expands to a 12 by 12 `cell-grid` whose values `expand` computes; patterns (squares, commutativity, nines) are recipes; facts are predicates.

#### 6.2.2 `bounds-explorer`

preset of `number-line` · composite · tier preset · cluster `number` · **P0** · size S · spec stage0 5.11 · first use 0.1 L39

Error intervals and calculations with bounds.

- **Composes** `number-line`.
- **Answers, AI hooks, accessibility and reduced motion** those of `number-line`; `describeAs` names the preset.
- Expands to `number-line` in rounding and interval mode; the bound combinations for a calculation are computed by `expand` at compile time, because the inputs are fixed numbers.

#### 6.2.3 `inequality-regions`

preset of `plot-2d` · composite · tier preset · cluster `algebra` · **P0** · size S · spec stage0 6.8 · first use 0.2 L33

Inequalities in two variables.

- **Composes** `plot-2d`.
- **Answers, AI hooks, accessibility and reduced motion** those of `plot-2d`; `describeAs` names the preset.
- Expands to `plot-2d` with boundary `curve` marks, a `region-select` half-plane layer and a test `drag-point`; linear programming stays a P2 mode.

#### 6.2.4 `vector-plane`

preset of `vector-combo` · composite · tier preset · cluster `precalc` · **P0** · size S · spec stage0 9.10 · first use 0.3 L11

Vectors in two dimensions.

- **Composes** `vector-combo`.
- **Answers, AI hooks, accessibility and reduced motion** those of `vector-combo`; `describeAs` names the preset.
- Expands Stage 0's 2D vector config to `vector-combo` in `lattice` and `path` modes (GCSE lattice paths, ratio division, magnitude and angle readouts); a dot-product task expands to `projection-lab` 2D instead.

#### 6.2.5 `matrix-grid`

preset of `matrix-multiply` · composite · tier preset · cluster `precalc` · **P0** · size S · spec stage0 9.11 · first use 0.3 L87

Matrices as arrays of numbers, and the operations on them.

- **Composes** `matrix-multiply`.
- **Answers, AI hooks, accessibility and reduced motion** those of `matrix-multiply`; `describeAs` names the preset.
- Expands to `matrix-multiply` in `entrywise` mode (add, scale) or row-by-column mode, with a `2x2` determinant and inverse readout; row operations expand to `elimination-lab`.

#### 6.2.6 `linear-map`

preset of `transform-grid` · composite · tier preset · cluster `precalc` · **P0** · size S · spec stage0 9.12 · first use 0.3 L89

A 2 × 2 matrix as a transformation of the plane.

- **Composes** `transform-grid`.
- **Answers, AI hooks, accessibility and reduced motion** those of `transform-grid`; `describeAs` names the preset.
- Expands Stage 0's 2 by 2 tasks (find the matrix, apply, determinant, compose, inverse) to `transform-grid` in 2D.

#### 6.2.7 `gbm-lab`

preset of `path-simulator` · composite · tier preset · cluster `stochastic` · **P1** · size S · spec calc-linalg 7.6 · first use 1.7 L23

Geometric Brownian motion $S_t=S_0e^{(\mu-\frac12\sigma^2)t+\sigma W_t}$: log-normal terminal values; mean against median; volatility drag; Monte Carlo prices with confidence intervals.

- **Composes** `path-simulator`.
- **Answers, AI hooks, accessibility and reduced motion** those of `path-simulator`; `describeAs` names the preset.
- **Modes added** A 1.7 mode, promoted from P2: lognormal terminal distribution, median against mean, $\mu - \frac{1}{2}\sigma^2$ as the (P1, finance 5).
- Expands to `path-simulator` with the `gbm` model, a log price axis, the terminal histogram and median and mean lines.
- 1.7 mode P1 (lognormal terminal distribution, $\mu - \frac12\sigma^2$ as the median growth rate, no Itô notation; finance 5); Itô modes P2.

#### 6.2.8 `estimator-compare`

preset of `sampling-lab` · composite · tier preset · cluster `statistics` · **P1** · size S · spec prob-stats 7.1 · first use 1.6 L3

Bias is where a sampling distribution centres relative to $\theta$; variance is its spread; $\text{MSE} = \text{bias}^2 + \text{variance}$.

- **Composes** `sampling-lab`.
- **Answers, AI hooks, accessibility and reduced motion** those of `sampling-lab`; `describeAs` names the preset.
- **Modes added** `trimmed` and `mad` estimators (P1, 1.6 L8, curriculum).
- Expands to `sampling-lab` with up to three statistics side by side and bias, variance and MSE readouts.

---

## 7. Build order

The build follows the depth-first content order. Widget work starts when stage E4 is approved and runs beside E5 to E10, one widget per pull request (arch 13, 10.5). These waves replace the catalogues' own waves (W0 to W3, A to D, D0 to D4, W-A1 to W-D, G1 to J, G0 to H2); 7.5 maps them.

### 7.1 Stage E4: the reference lesson set

E4 builds the widgets the Stage 1 reference lesson needs (widgets-stage0 2.8: `outcome-grid`, `choice`, `numeric-input`, `derivation-steps`, `trial-simulator`), plus `plot-2d`, `drag-point` and `slider` (arch 13), and every primitive and input they compose: `marks`, `live-formula`, `value-table`, `region-select`, `token-tray`, `stepper`, `cell-grid`, `sim-runner`, `chance-object`, `expression-input`, `card-sort`. These are the first examples in `docs/engine/WIDGET-AUTHORING.md`.

### 7.2 Wave L0: the remaining P0 primitives and inputs

In dependency order: hosts before the layers they host, layers before the inputs that use them.

| # | Id | Kind | Size | First needed by |
|---|---|---|---|---|
| 1 | `number-line` | primitive | M | its own use (0.1 L1) |
| 2 | `sketch-pad` | primitive | M | its own use (0.2 L68) |
| 3 | `matrix` | primitive | M | `matrix-multiply` (0.3 L88) |
| 4 | `plot-3d` | primitive | L | `solid-viewer` (0.3 L8) |
| 5 | `mass-editor` | primitive | M | its own use (1.5 L12) |
| 6 | `array-strip` | primitive | M | `float-inspector` (1.1 L4) |
| 7 | `node-link` | primitive | L | `code-cell` (0.1 L42) |
| 8 | `code-surface` | primitive | M | `code-cell` (0.1 L42) |
| 9 | `diff-view` | primitive | M | `code-cell` (0.1 L42) |
| 10 | `text-terminal` | primitive | S | `code-cell` (0.1 L42) |
| 11 | `speed-timer` | primitive | S | its own use (0.4 L1) |
| 12 | `scratch-pad` | primitive | S | 0.1 L41 (through `free-response`) |
| 13 | `free-response` | composite | M | its own use (0.1 L41) |

The P1 and P2 primitives and inputs (`cashflow-timeline`, `price-ladder`, `order-ticket`, `position-editor`, `voice-capture`, `quote-entry`, `span-track`) are built at the start of the wave that first needs them (7.4).

### 7.3 P0 composites and presets by first curriculum use

First use is the earliest lesson row naming the widget (section 8), placed on one timeline: main items in curriculum order, with 0.4 and 0.5 spread across 0.1 to 0.3 and 1.7 across 1.3 to 1.6, because they run alongside (curriculum; assessment decision 13). A wave is due before its first lesson reaches the content stage. Inside a wave, build in the order listed.

| # | Wave | Id | Tier | Cluster | Size | First use |
|---|---|---|---|---|---|---|
| 1 | W1 | `place-value-chart` | composite | `number` | M | 0.1 L1 |
| 2 | W1 | `written-method` | composite | `number` | M | 0.1 L2 |
| 3 | W1 | `area-model` | composite | `number` | M | 0.1 L3 |
| 4 | W1 | `bar-model` | composite | `number` | M | 0.1 L4 |
| 5 | W1 | `algebra-tiles` | composite | `algebra` | M | 0.1 L7 |
| 6 | W1 | `expression-tree` | composite | `number` | M | 0.1 L9 |
| 7 | W1 | `typing-trainer` | composite | `computing` | M | 0.4 L1 |
| 8 | W1 | `factor-tree` | composite | `number` | S | 0.1 L12 |
| 9 | W1 | `counting-slots` | composite | `precalc` | M | 0.1 L13 |
| 10 | W1 | `venn-diagram` | composite | `number` | M | 0.1 L14 |
| 11 | W1 | `modular-clock` | composite | `number` | S | 0.1 L16 |
| 12 | W1 | `speed-drill` | composite | `number` | M | 0.5 L1 |
| 13 | W1 | `double-number-line` | composite | `number` | S | 0.1 L24 |
| 14 | W1 | `multiplier-chain` | composite | `number` | M | 0.1 L25 |
| 15 | W1 | `graph-explorer` | composite | `algebra` | L | 0.1 L26 |
| 16 | W1 | `unit-chain` | composite | `number` | S | 0.1 L30 |
| 17 | W1 | `equation-workbench` | composite | `algebra` | L | 0.1 L35 |
| 18 | W1 | `times-table-grid` | preset | `number` | S | 0.5 L2 |
| 19 | W1 | `bounds-explorer` | preset | `number` | S | 0.1 L39 |
| 20 | W1 | `fermi-estimator` | composite | `number` | M | 0.1 L40 |
| 21 | W1 | `code-cell` | composite | `core` | L | 0.1 L42 |
| 22 | W2 | `function-machine` | composite | `algebra` | S | 0.2 L1 |
| 23 | W2 | `strategy-trainer` | composite | `number` | M | 0.5 L3 |
| 24 | W2 | `balance-scale` | composite | `algebra` | M | 0.2 L18 |
| 25 | W2 | `inequality-regions` | preset | `algebra` | S | 0.2 L33 |
| 26 | W2 | `file-tree` | composite | `computing` | S | 0.4 L9 |
| 27 | W2 | `scatter-fit` | composite | `precalc` | M | 0.2 L46 |
| 28 | W2 | `equation-stack` | composite | `algebra` | M | 0.2 L49 |
| 29 | W2 | `setup-checklist` | composite | `computing` | M | 0.4 L11 |
| 30 | W2 | `sign-chart` | composite | `algebra` | M | 0.2 L70 |
| 31 | W2 | `dot-plot-stats` | composite | `precalc` | M | 0.2 L75 |
| 32 | W2 | `shell-sim` | composite | `computing` | L | 0.4 L13 |
| 33 | W2 | `complex-plane` | composite | `precalc` | M | 0.2 L85 |
| 34 | W2 | `iteration-cobweb` | composite | `algebra` | S | 0.2 L107 |
| 35 | W3 | `geometry-board` | composite | `geometry` | L | 0.3 L1 |
| 36 | W3 | `solid-viewer` | composite | `geometry` | M | 0.3 L8 |
| 37 | W3 | `vector-plane` | preset | `precalc` | S | 0.3 L11 |
| 38 | W3 | `workspace-sim` | composite | `computing` | M | 0.4 L20 |
| 39 | W3 | `sequence-lab` | composite | `precalc` | M | 0.3 L39 |
| 40 | W3 | `slide-rule` | composite | `precalc` | S | 0.3 L51 |
| 41 | W3 | `predict-output` | composite | `python` | M | 0.4 L22 |
| 42 | W3 | `sum-visualiser` | composite | `precalc` | M | 0.3 L60 |
| 43 | W3 | `series-explorer` | composite | `calculus` | M | 0.3 L63 |
| 44 | W3 | `diagnostic-reader` | composite | `python` | M | 0.4 L23 |
| 45 | W3 | `unit-circle` | composite | `precalc` | M | 0.3 L66 |
| 46 | W3 | `circle-to-wave` | composite | `precalc` | S | 0.3 L71 |
| 47 | W3 | `code-tracer` | composite | `python` | L | 0.4 L24 |
| 48 | W3 | `matrix-grid` | preset | `precalc` | S | 0.3 L87 |
| 49 | W3 | `matrix-multiply` | composite | `linalg` | M | 0.3 L88 |
| 50 | W3 | `linear-map` | preset | `precalc` | S | 0.3 L89 |
| 51 | W3 | `determinant-lab` | composite | `linalg` | M | 0.3 L91 |
| 52 | W3 | `parsons` | composite | `python` | M | 0.4 L26 |
| 53 | W3 | `tree-diagram` | composite | `precalc` | M | 0.3 L98 |
| 54 | W3 | `pascal-triangle` | composite | `precalc` | S | 0.3 L99 |
| 55 | W3 | `trial-simulator` | composite | `precalc` | M | 0.3 L106 |
| 56 | W3 | `binomial-expander` | composite | `precalc` | M | 0.3 L108 |
| 57 | W3 | `outcome-grid` | composite | `precalc` | M | 0.3 L112 |
| 58 | W3 | `stat-chart` | composite | `precalc` | M | 0.3 L119 |
| 59 | W3 | `induction-chain` | composite | `precalc` | S | 0.3 L129 |
| 60 | W3 | `limit-explorer` | composite | `calculus` | M | 0.3 L142 |
| 61 | W4 | `float-inspector` | composite | `python` | M | 1.1 L4 |
| 62 | W4 | `code-blanks` | composite | `python` | M | 1.1 L8 |
| 63 | W4 | `complexity-lab` | composite | `algorithms` | M | 1.1 L8 |
| 64 | W4 | `format-lab` | composite | `python` | S | 1.1 L9 |
| 65 | W4 | `algo-lab` | composite | `algorithms` | L | 1.1 L19 (through `sort-lab`) |
| 66 | W4 | `sort-lab` | preset | `algorithms` | M | 1.1 L19 |
| 67 | W4 | `recursion-tree` | preset | `algorithms` | S | 1.1 L21 |
| 68 | W4 | `hash-table` | preset | `python` | M | 1.1 L25 |
| 69 | W4 | `bench-lab` | composite | `data` | M | 1.1 L28 |
| 70 | W4 | `pipeline-flow` | composite | `python` | M | 1.1 L29 |
| 71 | W4 | `csv-inspector` | composite | `data` | M | 1.1 L40 |
| 72 | W4 | `json-explorer` | composite | `python` | S | 1.1 L41 |
| 73 | W4 | `time-series-lab` | composite | `data` | M | 1.1 L42 |
| 74 | W4 | `regex-lab` | composite | `python` | M | 1.1 L43 |
| 75 | W4 | `search-path` | composite | `python` | S | 1.1 L45 |
| 76 | W4 | `code-annotator` | composite | `python` | M | 1.1 L48 |
| 77 | W4 | `ndarray-lab` | composite | `data` | M | 1.1 L56 |
| 78 | W4 | `broadcast-lab` | composite | `data` | S | 1.1 L62 |
| 79 | W4 | `path-simulator` | composite | `probability` | L | 1.1 L72 |
| 80 | W4 | `dataframe-lab` | composite | `data` | M | 1.1 L76 |
| 81 | W4 | `groupby-lab` | composite | `data` | M | 1.1 L86 |
| 82 | W4 | `join-lab` | composite | `data` | M | 1.1 L87 |
| 83 | W4 | `reshape-lab` | composite | `data` | S | 1.1 L90 |
| 84 | W4 | `drawdown-lab` | composite | `data` | M | 1.1 L97 |
| 85 | W4 | `plot-workbench` | composite | `data` | M | 1.1 L99 |
| 86 | W4 | `permission-bits` | composite | `tools` | S | 1.2 L5 |
| 87 | W4 | `git-graph` | composite | `tools` | L | 1.2 L9 |
| 88 | W4 | `merge-conflict` | composite | `tools` | M | 1.2 L14 |
| 89 | W4 | `code-review` | composite | `tools` | M | 1.2 L17 |
| 90 | W4 | `mutant-hunter` | composite | `tools` | L | 1.2 L19 |
| 91 | W4 | `injection-lab` | composite | `tools` | M | 1.2 L32 |
| 92 | W5 | `secant-tangent` | composite | `calculus` | M | 1.3 L1 |
| 93 | W5 | `epsilon-delta` | composite | `calculus` | S | 1.3 L4 |
| 94 | W5 | `local-zoom` | composite | `calculus` | S | 1.3 L9 |
| 95 | W5 | `derivative-tracer` | composite | `calculus` | M | 1.3 L10 |
| 96 | W5 | `growth-rectangle` | composite | `calculus` | S | 1.3 L11 |
| 97 | W5 | `function-mapping` | composite | `calculus` | M | 1.3 L15 |
| 98 | W5 | `rates-scene` | composite | `calculus` | M | 1.3 L24 |
| 99 | W5 | `taylor-builder` | composite | `calculus` | M | 1.3 L32 |
| 100 | W5 | `root-finder` | composite | `calculus` | M | 1.3 L33 |
| 101 | W5 | `objective-explorer` | composite | `calculus` | M | 1.3 L35 |
| 102 | W5 | `convexity-chord` | composite | `calculus` | M | 1.3 L50 |
| 103 | W5 | `descent-lab` | composite | `calculus` | M | 1.3 L53 |
| 104 | W5 | `riemann-sum` | composite | `calculus` | M | 1.3 L54 |
| 105 | W5 | `accumulator` | composite | `calculus` | M | 1.3 L56 |
| 106 | W5 | `slope-field` | composite | `calculus` | M | 1.3 L60 |
| 107 | W5 | `solid-of-revolution` | composite | `calculus` | M | 1.3 L77 |
| 108 | W5 | `volume-slicer` | composite | `calculus` | M | 1.3 L77 |
| 109 | W5 | `surface-explorer` | composite | `calculus` | L | 1.3 L106 |
| 110 | W5 | `projection-lab` | composite | `linalg` | M | 1.3 L107 |
| 111 | W5 | `dependency-graph` | composite | `calculus` | M | 1.3 L112 |
| 112 | W5 | `gradient-compass` | composite | `calculus` | S | 1.3 L114 |
| 113 | W5 | `quadratic-form` | composite | `calculus` | M | 1.3 L119 |
| 114 | W5 | `least-squares-fit` | composite | `linalg` | M | 1.3 L122 |
| 115 | W5 | `lagrange-explorer` | composite | `calculus` | M | 1.3 L124 |
| 116 | W5 | `region-bounds` | composite | `calculus` | M | 1.3 L130 |
| 117 | W5 | `transform-grid` | composite | `linalg` | M | 1.3 L134 |
| 118 | W6 | `vector-combo` | composite | `linalg` | M | 1.4 L1 |
| 119 | W6 | `row-column-picture` | composite | `linalg` | M | 1.4 L6 |
| 120 | W6 | `elimination-lab` | composite | `linalg` | L | 1.4 L7 |
| 121 | W6 | `subspace-tester` | composite | `linalg` | S | 1.4 L19 |
| 122 | W6 | `solution-set` | composite | `linalg` | M | 1.4 L22 |
| 123 | W6 | `four-subspaces` | composite | `linalg` | M | 1.4 L24 |
| 124 | W6 | `basis-change` | composite | `linalg` | S | 1.4 L33 |
| 125 | W6 | `gram-schmidt` | composite | `linalg` | S | 1.4 L50 |
| 126 | W6 | `eigen-finder` | composite | `linalg` | M | 1.4 L60 |
| 127 | W6 | `linear-dynamics` | composite | `linalg` | M | 1.4 L65 |
| 128 | W6 | `svd-stepper` | composite | `linalg` | M | 1.4 L72 |
| 129 | W6 | `pca-lab` | composite | `linalg` | M | 1.4 L74 |
| 130 | W6 | `low-rank-approx` | composite | `linalg` | S | 1.4 L86 |
| 131 | W6 | `condition-number` | composite | `linalg` | M | 1.4 L88 |
| 132 | W7 | `puzzle-workbench` | composite | `probability` | L | 1.5 L1 (through the weekly problems) |
| 133 | W7 | `indicator-board` | composite | `probability` | M | 1.5 L10 |
| 134 | W7 | `prob-square` | composite | `probability` | M | 1.5 L13 |
| 135 | W7 | `trial-strip` | composite | `probability` | M | 1.5 L16 |
| 136 | W7 | `first-step-solver` | composite | `probability` | M | 1.5 L16 |
| 137 | W7 | `odds-ledger` | composite | `probability` | M | 1.5 L17 |
| 138 | W7 | `icon-array` | composite | `probability` | M | 1.5 L27 |
| 139 | W7 | `contingency-table` | composite | `probability` | M | 1.5 L28 |
| 140 | W7 | `game-lab` | composite | `probability` | L | 1.5 L39 |
| 141 | W7 | `rv-mapper` | composite | `probability` | M | 1.5 L45 |
| 142 | W7 | `dist-explorer` | composite | `probability` | L | 1.5 L47 |
| 143 | W7 | `galton-board` | composite | `probability` | M | 1.5 L48 |
| 144 | W7 | `convolver` | composite | `probability` | M | 1.5 L68 |
| 145 | W7 | `sampling-lab` | composite | `probability` | L | 1.5 L69 |
| 146 | W7 | `generating-function` | composite | `probability` | M | 1.5 L78 |
| 147 | W7 | `order-statistics` | composite | `probability` | M | 1.5 L83 |
| 148 | W7 | `joint-density` | composite | `probability` | L | 1.5 L88 |
| 149 | W7 | `geo-prob` | composite | `probability` | M | 1.5 L92 |
| 150 | W7 | `covariance-lab` | composite | `probability` | M | 1.5 L94 |
| 151 | W7 | `gaussian-2d` | composite | `probability` | M | 1.5 L96 |
| 152 | W7 | `cond-expectation` | composite | `probability` | M | 1.5 L106 |
| 153 | W7 | `filtration-tree` | composite | `probability` | M | 1.5 L108 |
| 154 | W7 | `markov-chain` | composite | `probability` | L | 1.5 L123 |
| 155 | W7 | `lattice-walk` | composite | `probability` | M | 1.5 L135 |
| 156 | W7 | `kelly-lab` | composite | `probability` | M | 1.5 L154 (through `game-lab`) |

| Wave | Content it serves | Widgets |
|---|---|---|
| W1 | 0.1 Number (with 0.4 and 0.5 from week 1) | 21 |
| W2 | 0.2 Algebra | 13 |
| W3 | 0.3 Precalculus, GCSE geometry and statistics | 26 |
| W4 | 1.1 Python and 1.2 Tools | 31 |
| W5 | 1.3 Calculus | 26 |
| W6 | 1.4 Linear algebra | 14 |
| W7 | 1.5 Probability and the weekly problems | 25 |

Three P0 entries are needed before the curriculum names them, because other widgets depend on them: `algo-lab` with its first preset (`sort-lab`, 1.1 L19), `kelly-lab` with `game-lab`'s Kelly mode (1.5 L154), and `puzzle-workbench` with the first weekly problem (1.5 L1).

### 7.4 P1 and P2 waves

**P1**, by the item of first use:

- **1.6** (10): `estimator-compare`, `qq-plot`, `likelihood-lab`, `ci-ladder`, `test-lab`, `multiple-testing`, `summary-table`, `acf-lab`, `forecast-lab`, `posterior-lab`.
- **1.7** (37): `cashflow-timeline`, `price-ladder`, `order-ticket`, `quote-entry`, `voice-capture`, `position-editor`, `compounding-lab`, `tvm-timeline`, `bond-lab`, `yield-curve-lab`, `duration-lab`, `share-lab`, `margin-lab`, `gbm-lab`, `portfolio-lab`, `regression-lab`, `factor-model-lab`, `order-book`, `auction-lab`, `tape-lab`, `market-maker-sim`, `adverse-selection`, `execution-lab`, `viva`, `payoff-builder`, `carry-arb`, `futures-mtm`, `hedge-lab`, `option-chain`, `option-bounds`, `parity-lab`, `binomial-tree`, `bs-explorer`, `greeks-lab`, `pnl-attribution`, `hedging-sim`, `iv-solver`.
- **1.8** (17): `dynamic-array`, `counterexample-lab`, `heap-lab`, `memory-layout`, `pointer-walk`, `range-query-lab`, `stack-queue-lab`, `dp-table`, `binary-search-lab`, `interval-sweep`, `linked-list-lab`, `bit-lab`, `tree-lab`, `graph-search`, `shortest-path`, `union-find`, `problem-workbench`.
- **1.9** (2): `compile-pipeline`, `ownership-lab`.

**P2**, by the item of first use:

- **2.1** (34): `span-track`, `fit-explorer`, `error-curves`, `classifier-plane`, `bias-variance-lab`, `loss-lab`, `logistic-lab`, `cv-lab`, `leakage-detective`, `tuning-lab`, `regularisation-path`, `feature-builder`, `basis-lab`, `penalty-geometry`, `threshold-lab`, `calibration-lab`, `tree-builder`, `split-scorer`, `ensemble-lab`, `boosting-lab`, `importance-lab`, `nn-playground`, `relu-composer`, `sequence-filter`, `ml-workbench`, `time-cv-lab`, `labelling-lab`, `portfolio-sort`, `bar-sampler`, `fracdiff-lab`, `signal-lab`, `cluster-lab`, `overfit-lab`, `results-note`.
- **2.2** (5): `series-lab`, `arma-lab`, `garch-lab`, `coint-lab`, `sde-stepper`.
- **2.3** (13): `backtest-lab`, `sharpe-lab`, `bet-lab`, `paper-trader`, `mock-interview`, `order-lifecycle`, `pairs-lab`, `vol-surface`, `pricer-compare`, `feed-sim`, `candle-builder`, `latency-lab`, `schema-builder`.
- **2.4** (2): `contest-arena`, `number-theory-lab`.
- **3.1** (1): `replication-workbench`.
- **3.2** (6): `measure-change`, `quadratic-variation`, `heat-diffusion`, `reflection-principle`, `ito-sum`, `ito-lemma-lab`.
- **3.3** (1): `mm-game`.

### 7.5 Catalogue waves mapped

| Catalogue | Its waves | Library waves |
|---|---|---|
| stage0 | W0, W1, W2, W3 | E4 and L0; W1; W2; W3 (with `counting-slots` in W1 and `scatter-fit`, `dot-plot-stats`, `complex-plane` in W2, curriculum request R3) |
| calc-linalg | A, B, C, D, then P1 and P2 | A splits across L0 and W1 to W4; B is W5; C is W6 (with `matrix-multiply`, `determinant-lab`, `series-explorer` and `limit-explorer` pulled into W3); D is W7 |
| prob-stats | D0 to D4, E, F | D0 to D4 are W7; E is the 1.6 P1 wave; F is the 2.2 P2 wave |
| programming | W-A1 to W-A3, W-B1, W-B2, W-C, W-D | W-A1 to W-A3 are W4; W-B1 and W-B2 are the 1.8 P1 wave; W-C the 1.9 wave; W-D the 2.4 wave |
| finance | D4, G1 to G3, H, J | D4 is W7; G1 to G3 are the 1.7 P1 wave in that order; H is 2.3; J is 3.3 |
| ML | G0 to G5, H1, H2, E | E (`viva`) is the 1.6 wave; G0 to G5 are 2.1; H1 and H2 are 3.1 |

**Gate per widget**, the union of the catalogues' gates and arch E4: the schema validates every fixture; the generic contract suite passes (arch 8.1.1); pointer, keyboard and tap-then-tap fixture paths reach their expected answers; axe is clean in every state; reduced motion and `test` motion are checked; `describe` is snapshot-tested; P95 frame time is within budget at 4x throttling; the scope is empty after unmount; generators pass CI; parity tests pass for every JavaScript core the widget relies on (programming 12; prob-stats decision 6; finance decision 16; ML decision 1).

---

## 8. Curriculum coverage

### 8.1 Method

A script read every Markdown table in the eleven curriculum files whose header has a Widgets column, split cells on unescaped pipes, assigned each row to its curriculum item by its section, and resolved every backticked id in the Widgets cell through the name map of section 2 [measured]. It found 2,148 lesson rows (876 in P0 items) and 48 sample-lesson screen rows. Every id it met is a library id, an alias (section 2), or one of three things it ignores: a local widget name inside a sample lesson (`combo`, `mm`, `heap`, `code`, `grid`), a package or runtime tag (`web`, `numpy`, `pandas`, `statsmodels`, and `micropython-ok`, void under decision 13), or an editor name (`nano`). Rows per item: 0.1 42, 0.2 111, 0.3 146, 0.4 31, 0.5 16, 1.1 107, 1.2 32, 1.3 137, 1.4 98, 1.5 156, 1.6 80, 1.7 80, 1.8 150, 1.9 88, 2.1 152, 2.2 43, 2.3 229, 2.4 84, 3.1 108, 3.2 104, 3.3 154.

### 8.2 Which curriculum items each widget serves

Numbers are lesson rows naming the widget in that item; "first" is the first lesson that names it. Aliases are folded into their final id.

| Widget | Tier | P | First | Items served (lesson rows) |
|---|---|---|---|---|
| `accumulator` | composite | P0 | 1.3 L56 | 1.3 (10), 1.5 (2), 3.3 (1) |
| `acf-lab` | composite | P1 | 1.6 L56 | 1.6 (2), 2.2 (9) |
| `adverse-selection` | composite | P1 | 1.7 L43 | 1.7 (1) |
| `algebra-tiles` | composite | P0 | 0.1 L7 | 0.1 (1), 0.2 (7) |
| `algo-lab` | composite | P0 | 1.1 L19 (through `sort-lab`) | none: used through its presets |
| `area-model` | composite | P0 | 0.1 L3 | 0.1 (7), 0.2 (12) |
| `arma-lab` | composite | P2 | 2.2 L11 | 2.2 (7) |
| `array-strip` | primitive | P0 | 1.1 L7 | 1.1 (8), 1.8 (10), 2.3 (1), 2.4 (6) |
| `auction-lab` | composite | P1 | 1.7 L35 | 1.7 (1) |
| `backtest-lab` | composite | P2 | 2.3 L4 | 2.3 (39) |
| `balance-scale` | composite | P0 | 0.2 L18 | 0.2 (3) |
| `bar-model` | composite | P0 | 0.1 L4 | 0.1 (8), 0.2 (3) |
| `bar-sampler` | composite | P2 | 2.1 L134 | 2.1 (1), 2.3 (1) |
| `basis-change` | composite | P0 | 1.4 L33 | 1.4 (4) |
| `basis-lab` | composite | P2 | 2.1 L40 | 2.1 (5) |
| `bench-lab` | composite | P0 | 1.1 L28 | 1.1 (7), 1.8 (1), 1.9 (12), 2.3 (6), 2.4 (1), 3.3 (2) |
| `bet-lab` | composite | P2 | 2.3 L11 | 2.3 (1), 3.3 (9) |
| `bias-variance-lab` | composite | P2 | 2.1 L6 | 2.1 (4) |
| `binary-search-lab` | preset | P1 | 1.8 L46 | 1.8 (8), 1.9 (1), 2.4 (3) |
| `binomial-expander` | composite | P0 | 0.3 L108 | 0.3 (3), 1.5 (1) |
| `binomial-tree` | composite | P1 | 1.7 L64 | 1.7 (8), 1.9 (2), 2.3 (3), 3.2 (16), 3.3 (2) |
| `bit-lab` | composite | P1 | 1.8 L78 | 1.8 (5), 1.9 (3), 2.4 (9) |
| `bond-lab` | composite | P1 | 1.7 L7 | 1.7 (4) |
| `boosting-lab` | composite | P2 | 2.1 L96 | 2.1 (5) |
| `bounds-explorer` | preset | P0 | 0.1 L39 | 0.1 (1) |
| `broadcast-lab` | composite | P0 | 1.1 L62 | 1.1 (2) |
| `bs-explorer` | composite | P1 | 1.7 L72 | 1.7 (4), 2.3 (1), 3.2 (8), 3.3 (4) |
| `calibration-lab` | composite | P2 | 2.1 L76 | 2.1 (6), 3.3 (3) |
| `candle-builder` | composite | P2 | 2.3 L192 | 2.3 (5) |
| `card-sort` | input | P0 | 0.2 L2 | 0.2 (12), 0.3 (9), 0.4 (1), 1.3 (4), 1.5 (2), 1.6 (4), 1.7 (4), 2.1 (4), 2.2 (2), 2.3 (24), 3.1 (14), 3.2 (1), 3.3 (9) |
| `carry-arb` | composite | P1 | 1.7 L47 | 1.7 (3) |
| `cashflow-timeline` | primitive | P1 | 1.7 L1 | 1.7 (6) |
| `cell-grid` | primitive | P0 | 1.1 L14 | 1.1 (4), 1.8 (10), 2.1 (1), 2.4 (3) |
| `chance-object` | primitive | P0 | 1.5 L6 | 1.5 (3), 3.2 (1), 3.3 (2) |
| `choice` (also `choice-cards`) | input | P0 | 0.1 L1 | 0.1 (5), 0.3 (5), 0.4 (2), 1.1 (9), 1.3 (29), 1.4 (7), 1.5 (2), 1.8 (7), 2.4 (1) |
| `ci-ladder` | composite | P1 | 1.6 L21 | 1.6 (8) |
| `circle-to-wave` | composite | P0 | 0.3 L71 | 0.3 (5) |
| `classifier-plane` | composite | P2 | 2.1 L3 | 2.1 (10) |
| `cluster-lab` | composite | P2 | 2.1 L137 | 2.1 (6), 2.3 (1) |
| `code-annotator` | composite | P0 | 1.1 L48 | 1.1 (4), 1.9 (3) |
| `code-blanks` | composite | P0 | 1.1 L8 | 1.1 (2), 1.8 (3) |
| `code-cell` (also `code-editor`) | composite | P0 | 0.1 L42 | 0.1 (1), 0.2 (2), 0.3 (1), 0.4 (10), 1.1 (31), 1.2 (9), 1.3 (5), 1.4 (12), 1.5 (3), 1.6 (7), 1.7 (2), 1.8 (7), 1.9 (27), 2.1 (2), 2.2 (7), 2.3 (31), 2.4 (6), 3.1 (6), 3.2 (5), 3.3 (5) |
| `code-review` | composite | P0 | 1.2 L17 | 1.2 (1), 1.9 (3) |
| `code-surface` | primitive | P0 | 2.3 L71 | 2.3 (1), 3.3 (5) |
| `code-tracer` | composite | P0 | 0.4 L24 | 0.4 (5), 1.1 (25), 1.8 (4), 1.9 (17) |
| `coint-lab` | composite | P2 | 2.2 L35 | 2.2 (7), 3.1 (2) |
| `compile-pipeline` | composite | P1 | 1.9 L1 | 1.9 (7) |
| `complex-plane` | composite | P0 | 0.2 L85 | 0.2 (3), 0.3 (5), 1.3 (2), 1.4 (2), 2.2 (2) |
| `complexity-lab` | composite | P0 | 1.1 L8 | 1.1 (3), 1.8 (15), 1.9 (1), 2.4 (3) |
| `compounding-lab` | composite | P1 | 1.7 L1 | 1.7 (3), 3.3 (1) |
| `cond-expectation` | composite | P0 | 1.5 L106 | 1.5 (6) |
| `condition-number` | composite | P0 | 1.4 L88 | 1.4 (1) |
| `contest-arena` | composite | P2 | 2.4 L1 | 2.4 (3) |
| `contingency-table` | composite | P0 | 1.5 L28 | 1.5 (7), 1.6 (1), 2.1 (4) |
| `convexity-chord` | composite | P0 | 1.3 L50 | 1.3 (3), 1.5 (1), 1.7 (2), 3.3 (1) |
| `convolver` | composite | P0 | 1.5 L68 | 1.5 (5) |
| `counterexample-lab` | composite | P1 | 1.8 L21 | 1.8 (7), 2.4 (4) |
| `counting-slots` | composite | P0 | 0.1 L13 | 0.1 (1), 0.3 (8), 1.1 (1), 1.5 (12), 2.4 (1), 3.3 (4) |
| `covariance-lab` | composite | P0 | 1.5 L94 | 1.5 (5), 2.3 (6), 3.2 (3), 3.3 (5) |
| `csv-inspector` | composite | P0 | 1.1 L40 | 1.1 (3) |
| `cv-lab` | composite | P2 | 2.1 L23 | 2.1 (8) |
| `dataframe-lab` | composite | P0 | 1.1 L76 | 1.1 (11) |
| `dependency-graph` | composite | P0 | 1.3 L112 | 1.3 (3), 2.1 (1) |
| `derivation-steps` (also `derivation`) | input | P0 | 0.1 L1 | 0.1 (7), 0.2 (8), 0.3 (32), 1.1 (6), 1.3 (39), 1.4 (25), 1.5 (15), 1.6 (21), 1.7 (6), 1.8 (9), 2.1 (13), 2.2 (6), 2.3 (2), 3.1 (6), 3.2 (37), 3.3 (5) |
| `derivative-tracer` | composite | P0 | 1.3 L10 | 1.3 (12) |
| `descent-lab` | composite | P0 | 1.3 L53 | 1.3 (2), 1.4 (1), 2.1 (5) |
| `determinant-lab` | composite | P0 | 0.3 L91 | 0.3 (1), 1.3 (1), 1.4 (5) |
| `diagnostic-reader` | composite | P0 | 0.4 L23 | 0.4 (2), 1.1 (9), 1.2 (2), 1.9 (25), 2.4 (2) |
| `diff-view` | primitive | P0 | 1.1 L48 | 1.1 (1), 1.2 (2) |
| `dist-explorer` | composite | P0 | 1.5 L47 | 1.5 (28), 1.6 (9), 1.7 (2), 2.1 (3), 2.3 (4), 3.1 (1), 3.2 (4), 3.3 (2) |
| `dot-plot-stats` | composite | P0 | 0.2 L75 | 0.2 (2), 0.3 (2), 1.6 (1) |
| `double-number-line` | composite | P0 | 0.1 L24 | 0.1 (4), 0.2 (2), 0.3 (2) |
| `dp-table` | preset | P1 | 1.8 L45 | 1.8 (18), 2.4 (10) |
| `drag-point` (also `draggable-point`) | primitive | P0 | 0.2 L36 | 0.2 (1), 0.3 (1), 1.3 (3) |
| `drawdown-lab` | composite | P0 | 1.1 L97 | 1.1 (3), 1.7 (1), 2.3 (8) |
| `duration-lab` | composite | P1 | 1.7 L13 | 1.7 (3) |
| `dynamic-array` | preset | P1 | 1.8 L4 | 1.8 (2), 1.9 (2) |
| `eigen-finder` | composite | P0 | 1.4 L60 | 1.4 (12), 1.5 (2), 2.3 (1), 3.3 (1) |
| `elimination-lab` | composite | P0 | 1.4 L7 | 1.4 (20) |
| `ensemble-lab` | composite | P2 | 2.1 L92 | 2.1 (4) |
| `epsilon-delta` | composite | P0 | 1.3 L4 | 1.3 (3) |
| `equation-stack` | composite | P0 | 0.2 L49 | 0.2 (7), 0.3 (1) |
| `equation-workbench` | composite | P0 | 0.1 L35 | 0.1 (1), 0.2 (28), 0.3 (11) |
| `error-curves` | composite | P2 | 2.1 L1 | 2.1 (11) |
| `estimator-compare` | preset | P1 | 1.6 L3 | 1.6 (8) |
| `execution-lab` | composite | P1 | 1.7 L44 | 1.7 (1), 2.3 (2) |
| `expression-input` (also `expression-entry`) | input | P0 | 0.1 L12 | 0.1 (4), 0.2 (17), 0.3 (10), 1.3 (42), 1.8 (4) |
| `expression-tree` | composite | P0 | 0.1 L9 | 0.1 (3), 0.2 (4), 0.4 (1), 1.1 (1) |
| `factor-model-lab` | composite | P1 | 1.7 L28 | 1.7 (1), 2.3 (5), 3.1 (17) |
| `factor-tree` | composite | P0 | 0.1 L12 | 0.1 (5), 2.4 (1) |
| `feature-builder` | composite | P2 | 2.1 L35 | 2.1 (6) |
| `feed-sim` | composite | P2 | 2.3 L180 | 2.3 (6) |
| `fermi-estimator` | composite | P0 | 0.1 L40 | 0.1 (1), 0.5 (1), 3.3 (3) |
| `file-tree` | composite | P0 | 0.4 L9 | 0.4 (8), 1.1 (2), 1.2 (1) |
| `filtration-tree` | composite | P0 | 1.5 L108 | 1.5 (2), 3.2 (15) |
| `first-step-solver` | composite | P0 | 1.5 L16 | 1.5 (10), 2.4 (1), 3.2 (1), 3.3 (3) |
| `fit-explorer` | composite | P2 | 2.1 L1 | 2.1 (10) |
| `float-inspector` | composite | P0 | 1.1 L4 | 1.1 (3), 1.2 (1), 1.9 (4) |
| `forecast-lab` | composite | P1 | 1.6 L64 | 1.6 (1), 2.2 (7) |
| `format-lab` | composite | P0 | 1.1 L9 | 1.1 (1), 1.9 (1) |
| `four-subspaces` | composite | P0 | 1.4 L24 | 1.4 (11) |
| `fracdiff-lab` | composite | P2 | 2.1 L135 | 2.1 (1) |
| `free-response` | input | P0 | 0.1 L41 | 0.1 (1), 0.2 (1), 0.3 (5), 1.3 (5), 1.6 (1), 1.7 (2), 1.8 (1), 2.1 (1), 2.2 (1), 2.3 (11), 3.1 (6), 3.3 (5) |
| `function-machine` | composite | P0 | 0.2 L1 | 0.2 (11), 0.3 (3), 0.4 (1) |
| `function-mapping` | composite | P0 | 1.3 L15 | 1.3 (6), 1.5 (2) |
| `futures-mtm` | composite | P1 | 1.7 L50 | 1.7 (2), 3.2 (2) |
| `galton-board` | composite | P0 | 1.5 L48 | 1.5 (2) |
| `game-lab` | composite | P0 | 1.5 L39 | 1.5 (8), 2.1 (1), 2.4 (2), 3.1 (1), 3.3 (2) |
| `garch-lab` | composite | P2 | 2.2 L23 | 2.2 (9) |
| `gaussian-2d` | composite | P0 | 1.5 L96 | 1.5 (4), 1.6 (1), 3.2 (1), 3.3 (2) |
| `gbm-lab` | preset | P1 | 1.7 L23 | 1.7 (2), 3.2 (8) |
| `generating-function` | composite | P0 | 1.5 L78 | 1.5 (4) |
| `geo-prob` | composite | P0 | 1.5 L92 | 1.5 (6), 3.3 (3) |
| `geometry-board` | composite | P0 | 0.3 L1 | 0.3 (36), 2.4 (4) |
| `git-graph` | composite | P0 | 1.2 L9 | 1.2 (11) |
| `gradient-compass` | composite | P0 | 1.3 L114 | 1.3 (2), 1.4 (1) |
| `gram-schmidt` | composite | P0 | 1.4 L50 | 1.4 (2) |
| `graph-explorer` | composite | P0 | 0.1 L26 | 0.1 (3), 0.2 (57), 0.3 (36), 1.5 (1) |
| `graph-search` | preset | P1 | 1.8 L91 | 1.8 (12), 2.4 (7) |
| `greeks-lab` | composite | P1 | 1.7 L75 | 1.7 (3), 2.3 (5), 3.2 (1), 3.3 (1) |
| `groupby-lab` | composite | P0 | 1.1 L86 | 1.1 (2), 1.2 (2) |
| `growth-rectangle` | composite | P0 | 1.3 L11 | 1.3 (2) |
| `hash-table` | preset | P0 | 1.1 L25 | 1.1 (3), 1.8 (15), 1.9 (1), 2.4 (5) |
| `heap-lab` | preset | P1 | 1.8 L23 | 1.8 (11), 1.9 (1) |
| `heat-diffusion` | composite | P2 | 3.2 L45 | 3.2 (4) |
| `hedge-lab` | composite | P1 | 1.7 L52 | 1.7 (1) |
| `hedging-sim` | composite | P1 | 1.7 L78 | 1.7 (1), 2.3 (1), 3.2 (3), 3.3 (1) |
| `icon-array` | composite | P0 | 1.5 L27 | 1.5 (5), 1.6 (1), 2.1 (1) |
| `importance-lab` | composite | P2 | 2.1 L102 | 2.1 (6) |
| `indicator-board` | composite | P0 | 1.5 L10 | 1.5 (14), 2.4 (1), 3.3 (4) |
| `induction-chain` | composite | P0 | 0.3 L129 | 0.3 (4) |
| `inequality-regions` | preset | P0 | 0.2 L33 | 0.2 (1) |
| `injection-lab` | composite | P0 | 1.2 L32 | 1.2 (1) |
| `interval-sweep` | composite | P1 | 1.8 L52 | 1.8 (6), 2.4 (1) |
| `iteration-cobweb` | composite | P0 | 0.2 L107 | 0.2 (1), 0.3 (1), 1.3 (1), 1.5 (1), 3.3 (1) |
| `ito-lemma-lab` | composite | P2 | 3.2 L57 | 3.2 (6), 3.3 (3) |
| `ito-sum` | composite | P2 | 3.2 L52 | 3.2 (6) |
| `iv-solver` | composite | P1 | 1.7 L79 | 1.7 (2), 2.3 (4), 3.2 (2) |
| `join-lab` | composite | P0 | 1.1 L87 | 1.1 (3), 1.2 (1) |
| `joint-density` | composite | P0 | 1.5 L88 | 1.5 (7) |
| `json-explorer` | composite | P0 | 1.1 L41 | 1.1 (1), 2.3 (5) |
| `kelly-lab` | composite | P0 | 1.5 L154 (through `game-lab`) | 2.3 (1), 3.3 (6) |
| `labelling-lab` | composite | P2 | 2.1 L119 | 2.1 (6), 2.3 (1) |
| `lagrange-explorer` | composite | P0 | 1.3 L124 | 1.3 (5), 1.4 (1), 1.7 (1), 2.3 (1), 3.2 (1) |
| `latency-lab` | composite | P2 | 2.3 L197 | 2.3 (6), 3.3 (1) |
| `lattice-walk` | composite | P0 | 1.5 L135 | 1.5 (6), 3.2 (1) |
| `leakage-detective` | composite | P2 | 2.1 L28 | 2.1 (6), 3.1 (4) |
| `least-squares-fit` | composite | P0 | 1.3 L122 | 1.3 (1), 1.4 (8), 1.5 (1), 1.6 (3) |
| `likelihood-lab` | composite | P1 | 1.6 L11 | 1.6 (12) |
| `limit-explorer` | composite | P0 | 0.3 L142 | 0.3 (1), 1.3 (6) |
| `linear-dynamics` | composite | P0 | 1.4 L65 | 1.4 (7), 1.5 (1), 2.2 (1) |
| `linear-map` | preset | P0 | 0.3 L89 | 0.3 (4) |
| `linked-list-lab` | preset | P1 | 1.8 L63 | 1.8 (6), 2.4 (1) |
| `live-formula` (also `tex-terms`) | primitive | P0 | 1.8 L25 | 1.8 (4), 2.4 (1), 3.1 (2) |
| `local-zoom` | composite | P0 | 1.3 L9 | 1.3 (4) |
| `logistic-lab` | composite | P2 | 2.1 L15 | 2.1 (9) |
| `loss-lab` | composite | P2 | 2.1 L11 | 2.1 (6) |
| `low-rank-approx` | composite | P0 | 1.4 L86 | 1.4 (3) |
| `margin-lab` | composite | P1 | 1.7 L22 | 1.7 (1), 2.3 (3) |
| `market-maker-sim` (also `dealer-sim`) | composite | P1 | 1.7 L42 | 1.7 (1), 3.1 (17) |
| `markov-chain` (also `ctmc-clock`) | composite | P0 | 1.5 L123 | 1.5 (12), 3.3 (3) |
| `marks` (also `curve-layer`, `geo-layer`, `bar-layer`) | primitive | P0 | 1.3 L65 | 1.3 (1) |
| `mass-editor` | primitive | P0 | 1.5 L12 | 1.5 (6), 1.6 (1), 2.1 (4), 3.3 (1) |
| `matrix` | primitive | P0 | 1.7 L10 | 1.3 (2), 1.4 (21), 1.5 (2), 1.6 (1), 1.7 (3), 2.1 (5), 2.3 (4), 2.4 (1), 3.2 (3), 3.3 (3) |
| `matrix-grid` | preset | P0 | 0.3 L87 | 0.3 (4) |
| `matrix-multiply` | composite | P0 | 0.3 L88 | 0.3 (1), 1.1 (1), 1.4 (14), 1.5 (2), 1.8 (1), 2.4 (1) |
| `measure-change` | composite | P2 | 3.2 L30 | 3.2 (8) |
| `memory-layout` | composite | P1 | 1.8 L24 | 1.8 (1), 1.9 (10) |
| `merge-conflict` | composite | P0 | 1.2 L14 | 1.2 (1) |
| `ml-workbench` | composite | P2 | 2.1 L116 | 2.1 (8), 2.3 (3), 3.1 (1), 3.3 (4) |
| `mm-game` | composite | P2 | 3.3 L84 | 3.3 (12) |
| `mock-interview` | composite | P2 | 2.3 L41 | 2.3 (5), 3.3 (12) |
| `modular-clock` | composite | P0 | 0.1 L16 | 0.1 (1), 1.1 (1), 2.4 (1) |
| `multiple-testing` | composite | P1 | 1.6 L38 | 1.6 (5), 2.3 (2), 3.1 (6), 3.3 (1) |
| `multiplier-chain` | composite | P0 | 0.1 L25 | 0.1 (2), 0.2 (2), 0.3 (9), 1.7 (1), 3.3 (1) |
| `mutant-hunter` | composite | P0 | 1.2 L19 | 1.2 (5), 1.9 (3) |
| `ndarray-lab` | composite | P0 | 1.1 L56 | 1.1 (7) |
| `nn-playground` | composite | P2 | 2.1 L107 | 2.1 (5) |
| `node-link` (also `node-graph`) | primitive | P0 | 1.1 L1 | 1.1 (8), 1.2 (1), 1.5 (3), 1.7 (1), 1.8 (2), 2.3 (7), 3.3 (3) |
| `number-line` | primitive | P0 | 0.1 L1 | 0.1 (17), 0.2 (6), 0.3 (3), 0.5 (1), 1.1 (5), 1.3 (1), 1.9 (1) |
| `number-theory-lab` | composite | P2 | 2.4 L20 | 2.4 (15) |
| `numeric-input` (also `numeric-entry`) | input | P0 | 0.1 L1 | 0.1 (6), 0.2 (2), 0.3 (25), 1.1 (5), 1.3 (80), 1.4 (12), 1.5 (1), 1.6 (2), 1.8 (7), 3.1 (1), 3.2 (1), 3.3 (1) |
| `objective-explorer` | composite | P0 | 1.3 L35 | 1.3 (9) |
| `odds-ledger` | composite | P0 | 1.5 L17 | 1.5 (5), 1.6 (3), 3.1 (1), 3.3 (3) |
| `option-bounds` | composite | P1 | 1.7 L58 | 1.7 (3), 2.3 (1), 3.3 (1) |
| `option-chain` | composite | P1 | 1.7 L54 | 1.7 (2), 2.3 (4) |
| `order-book` | composite | P1 | 1.7 L29 | 1.7 (10), 2.3 (2), 3.3 (1) |
| `order-lifecycle` | composite | P2 | 2.3 L63 | 2.3 (7) |
| `order-statistics` | composite | P0 | 1.5 L83 | 1.5 (2), 3.3 (2) |
| `order-ticket` | input | P1 | 1.7 L29 | 1.7 (3) |
| `outcome-grid` | composite | P0 | 0.3 L112 | 0.3 (2), 1.5 (7), 3.3 (1) |
| `overfit-lab` | composite | P2 | 2.1 L144 | 2.1 (2), 2.3 (6), 3.3 (1) |
| `ownership-lab` | composite | P1 | 1.9 L23 | 1.9 (9) |
| `pairs-lab` | composite | P2 | 2.3 L79 | 2.3 (1), 3.1 (15) |
| `paper-trader` | composite | P2 | 2.3 L17 | 2.3 (5) |
| `parity-lab` | composite | P1 | 1.7 L60 | 1.7 (3), 2.3 (1) |
| `parsons` | composite | P0 | 0.4 L26 | 0.4 (1), 1.1 (4), 1.8 (1) |
| `pascal-triangle` | composite | P0 | 0.3 L99 | 0.3 (5), 1.5 (3), 2.4 (1) |
| `path-simulator` (also `brownian-path`) | composite | P0 | 1.1 L72 | 1.1 (2), 1.5 (6), 3.2 (16), 3.3 (2) |
| `payoff-builder` | composite | P1 | 1.7 L46 | 1.7 (7), 2.3 (1), 3.2 (1), 3.3 (2) |
| `pca-lab` | composite | P0 | 1.4 L74 | 1.4 (8), 2.1 (3), 3.1 (2), 3.3 (1) |
| `penalty-geometry` | composite | P2 | 2.1 L47 | 2.1 (5) |
| `permission-bits` | composite | P0 | 1.2 L5 | 1.2 (1) |
| `pipeline-flow` | composite | P0 | 1.1 L29 | 1.1 (4), 1.2 (4), 2.1 (2) |
| `place-value-chart` | composite | P0 | 0.1 L1 | 0.1 (13) |
| `plot-2d` (also `plot-axes`) | primitive | P0 | 1.1 L70 | 1.1 (5), 1.3 (11), 1.4 (3), 1.7 (4), 1.8 (2), 1.9 (2), 2.1 (3), 2.3 (3), 2.4 (2), 3.1 (1), 3.2 (8), 3.3 (10) |
| `plot-3d` (also `view-3d`) | primitive | P0 | 1.3 L107 | 1.3 (3), 1.4 (1), 3.2 (1) |
| `plot-workbench` | composite | P0 | 1.1 L99 | 1.1 (5) |
| `pnl-attribution` | composite | P1 | 1.7 L77 | 1.7 (2), 2.3 (2), 3.2 (1), 3.3 (1) |
| `pointer-walk` | preset | P1 | 1.8 L30 | 1.8 (12), 2.4 (3) |
| `portfolio-lab` | composite | P1 | 1.7 L24 | 1.7 (4), 2.3 (3) |
| `portfolio-sort` | composite | P2 | 2.1 L127 | 2.1 (1), 2.3 (2), 3.1 (18) |
| `position-editor` | primitive | P1 | 1.7 L46 | 1.7 (5), 2.3 (2), 3.2 (2) |
| `posterior-lab` | composite | P1 | 1.6 L70 | 1.6 (11), 2.1 (2), 3.1 (1) |
| `predict-output` | composite | P0 | 0.4 L22 | 0.3 (1), 0.4 (2), 1.1 (42), 1.2 (3), 1.4 (5), 1.6 (4), 1.8 (1), 1.9 (27) |
| `price-ladder` | primitive | P1 | 1.7 L29 | 1.7 (2), 2.3 (2), 3.3 (1) |
| `pricer-compare` | composite | P2 | 2.3 L160 | 2.3 (7), 3.2 (1) |
| `prob-square` | composite | P0 | 1.5 L13 | 1.5 (11) |
| `problem-workbench` | composite | P1 | 1.8 L146 | 1.8 (3), 1.9 (1), 2.4 (3), 3.3 (10) |
| `projection-lab` | composite | P0 | 1.3 L107 | 1.3 (1), 1.4 (8) |
| `puzzle-workbench` | composite | P0 | 1.5 L1 (through the weekly problems) | 3.3 (58) |
| `qq-plot` | composite | P1 | 1.6 L8 | 1.6 (5), 2.2 (2) |
| `quadratic-form` | composite | P0 | 1.3 L119 | 1.3 (2), 1.4 (6), 1.5 (1), 1.6 (1), 3.2 (2) |
| `quadratic-variation` | composite | P2 | 3.2 L41 | 3.2 (4) |
| `quote-entry` | input | P1 | 1.7 L42 (through `market-maker-sim`) | 3.3 (1) |
| `range-query-lab` | preset | P1 | 1.8 L34 | 1.8 (7), 2.4 (12) |
| `rates-scene` | composite | P0 | 1.3 L24 | 1.3 (1) |
| `recursion-tree` | preset | P0 | 1.1 L21 | 1.1 (2), 1.8 (18) |
| `reflection-principle` | composite | P2 | 3.2 L46 | 3.2 (8), 3.3 (2) |
| `regex-lab` | composite | P0 | 1.1 L43 | 1.1 (1), 1.2 (2) |
| `region-bounds` | composite | P0 | 1.3 L130 | 1.3 (5), 1.5 (2) |
| `region-select` (also `region-selector`) | primitive | P0 | 0.1 L13 | 0.1 (2), 0.3 (3), 1.3 (2), 1.5 (2), 1.7 (1), 3.2 (5), 3.3 (1) |
| `regression-lab` | composite | P1 | 1.7 L27 | 1.6 (19), 1.7 (2), 2.1 (6), 2.2 (3), 2.3 (7), 3.1 (4), 3.2 (1), 3.3 (4) |
| `regularisation-path` | composite | P2 | 2.1 L31 | 2.1 (12), 2.3 (1) |
| `relu-composer` | composite | P2 | 2.1 L109 | 2.1 (2) |
| `replication-workbench` | composite | P2 | 3.1 L1 | 3.1 (22) |
| `reshape-lab` | composite | P0 | 1.1 L90 | 1.1 (2) |
| `results-note` | composite | P2 | 2.1 L151 | 2.1 (1), 2.3 (10), 3.1 (5), 3.3 (7) |
| `riemann-sum` | composite | P0 | 1.3 L54 | 1.3 (9) |
| `root-finder` | composite | P0 | 1.3 L33 | 1.3 (1), 3.3 (1) |
| `row-column-picture` | composite | P0 | 1.4 L6 | 1.4 (4) |
| `rv-mapper` | composite | P0 | 1.5 L45 | 1.5 (5) |
| `sampling-lab` | composite | P0 | 1.5 L69 | 1.5 (9), 1.6 (10), 2.1 (2), 2.2 (1), 2.3 (1), 3.3 (1) |
| `scatter-fit` | composite | P0 | 0.2 L46 | 0.2 (1), 0.3 (3) |
| `schema-builder` | composite | P2 | 2.3 L204 | 2.3 (2) |
| `scratch-pad` | primitive | P0 | 0.1 L41 (through `free-response`) | none: see 8.5 |
| `sde-stepper` | composite | P2 | 2.2 L40 | 2.2 (1), 3.1 (3), 3.2 (7) |
| `search-path` | composite | P0 | 1.1 L45 | 1.1 (2), 1.2 (1) |
| `secant-tangent` | composite | P0 | 1.3 L1 | 1.3 (11) |
| `sequence-filter` | composite | P2 | 2.1 L115 | 2.1 (1) |
| `sequence-lab` | composite | P0 | 0.3 L39 | 0.3 (5) |
| `series-explorer` | composite | P0 | 0.3 L63 | 0.3 (2), 1.3 (12), 1.4 (1), 1.5 (1), 1.7 (1), 3.3 (3) |
| `series-lab` | composite | P2 | 2.2 L1 | 2.2 (10) |
| `setup-checklist` | composite | P0 | 0.4 L11 | 0.4 (5), 1.1 (1), 1.9 (2), 2.3 (20), 3.1 (1), 3.3 (3) |
| `share-lab` | composite | P1 | 1.7 L17 | 1.7 (4), 2.3 (2) |
| `sharpe-lab` | composite | P2 | 2.3 L7 | 2.3 (11), 3.1 (5), 3.3 (1) |
| `shell-sim` | composite | P0 | 0.4 L13 | 0.4 (6), 1.1 (2), 1.2 (8) |
| `shortest-path` | preset | P1 | 1.8 L98 | 1.8 (7), 2.4 (2) |
| `sign-chart` | composite | P0 | 0.2 L70 | 0.2 (1), 0.3 (3), 1.3 (4) |
| `signal-lab` | composite | P2 | 2.1 L136 | 2.1 (2), 2.3 (28), 3.1 (2), 3.3 (1) |
| `sim-runner` | primitive | P0 | 1.1 L69 | 1.1 (5), 1.3 (3), 1.4 (5), 1.5 (1), 1.6 (1), 1.7 (1), 1.8 (5), 1.9 (3), 2.1 (1), 2.2 (1), 2.3 (4), 2.4 (1), 3.1 (1), 3.2 (2) |
| `sketch-pad` (also `curve-sketch`) | primitive | P0 | 0.2 L68 | 0.2 (4), 0.3 (1), 1.3 (4), 1.5 (1), 1.7 (2) |
| `slide-rule` | composite | P0 | 0.3 L51 | 0.3 (3) |
| `slider` | primitive | P0 | 0.1 L34 | 0.1 (1), 0.2 (10), 0.3 (2), 1.3 (7), 1.4 (1), 1.7 (1), 2.3 (3) |
| `slope-field` | composite | P0 | 1.3 L60 | 1.3 (5) |
| `solid-of-revolution` | composite | P0 | 1.3 L77 | 1.3 (2) |
| `solid-viewer` | composite | P0 | 0.3 L8 | 0.3 (5) |
| `solution-set` | composite | P0 | 1.4 L22 | 1.4 (7) |
| `sort-lab` | preset | P0 | 1.1 L19 | 1.1 (2), 1.8 (11), 1.9 (1), 2.4 (3) |
| `span-track` | primitive | P2 | 2.1 L119 | 2.1 (2), 3.1 (2) |
| `speed-drill` | composite | P0 | 0.5 L1 | 0.5 (16), 1.7 (1), 3.3 (14) |
| `speed-timer` | primitive | P0 | 0.4 L1 | 0.4 (1), 0.5 (1), 1.8 (1), 3.3 (1) |
| `split-scorer` | composite | P2 | 2.1 L87 | 2.1 (3) |
| `stack-queue-lab` | preset | P1 | 1.8 L40 | 1.8 (8), 2.4 (2) |
| `stat-chart` | composite | P0 | 0.3 L119 | 0.3 (4), 1.1 (2), 1.5 (1) |
| `stepper` | primitive | P0 | 0.3 L82 | 0.3 (1), 1.2 (1), 1.4 (2), 1.8 (3), 2.4 (4) |
| `strategy-trainer` | composite | P0 | 0.5 L3 | 0.5 (13), 3.3 (8) |
| `subspace-tester` | composite | P0 | 1.4 L19 | 1.4 (2) |
| `sum-visualiser` | composite | P0 | 0.3 L60 | 0.3 (8) |
| `summary-table` | composite | P1 | 1.6 L45 | 1.6 (13), 2.2 (1), 3.1 (1) |
| `surface-explorer` | composite | P0 | 1.3 L106 | 1.3 (12), 1.4 (2), 1.6 (1), 2.1 (1) |
| `svd-stepper` | composite | P0 | 1.4 L72 | 1.4 (8) |
| `tape-lab` | composite | P1 | 1.7 L40 | 1.7 (2) |
| `taylor-builder` | composite | P0 | 1.3 L32 | 1.3 (7), 1.5 (2), 1.6 (1), 3.1 (1) |
| `test-lab` | composite | P1 | 1.6 L26 | 1.6 (13), 2.2 (6) |
| `text-terminal` | primitive | P0 | 0.4 L16 | 0.4 (1), 1.2 (1), 1.9 (3) |
| `threshold-lab` | composite | P2 | 2.1 L71 | 2.1 (8) |
| `time-cv-lab` | composite | P2 | 2.1 L117 | 2.1 (8), 2.3 (5), 3.3 (2) |
| `time-series-lab` | composite | P0 | 1.1 L42 | 1.1 (9), 2.3 (12) |
| `times-table-grid` | preset | P0 | 0.5 L2 | 0.5 (1), 3.3 (1) |
| `token-tray` | primitive | P0 | 0.2 L1 | 0.2 (1), 0.3 (1), 0.4 (1), 1.1 (1), 1.2 (1), 1.3 (4), 1.4 (1), 1.5 (1), 1.8 (2), 2.3 (1), 3.1 (1), 3.3 (1) |
| `transform-grid` | composite | P0 | 1.3 L134 | 1.3 (1), 1.4 (9), 1.5 (3) |
| `tree-builder` | composite | P2 | 2.1 L86 | 2.1 (4) |
| `tree-diagram` | composite | P0 | 0.3 L98 | 0.3 (3), 1.5 (10), 1.7 (1), 3.3 (2) |
| `tree-lab` | preset | P1 | 1.8 L79 | 1.8 (14), 1.9 (2), 2.4 (7) |
| `trial-simulator` | composite | P0 | 0.3 L106 | 0.3 (5), 1.5 (16), 3.3 (3) |
| `trial-strip` | composite | P0 | 1.5 L16 | 1.5 (17), 3.3 (2) |
| `tuning-lab` | composite | P2 | 2.1 L29 | 2.1 (4) |
| `tvm-timeline` | composite | P1 | 1.7 L1 | 1.7 (6) |
| `typing-trainer` | composite | P0 | 0.4 L1 | 0.4 (9) |
| `union-find` | preset | P1 | 1.8 L102 | 1.8 (2), 2.4 (2) |
| `unit-chain` | composite | P0 | 0.1 L30 | 0.1 (1), 0.2 (3) |
| `unit-circle` | composite | P0 | 0.3 L66 | 0.3 (8), 1.3 (2) |
| `value-table` (also `data-table`) | primitive | P0 | 0.1 L16 | 0.1 (5), 0.2 (17), 0.3 (22), 1.1 (4), 1.2 (1), 1.3 (10), 1.4 (5), 1.5 (2), 1.6 (3), 1.7 (2), 1.8 (3), 2.1 (2), 2.3 (11), 3.1 (1), 3.2 (14), 3.3 (11) |
| `vector-combo` | composite | P0 | 1.4 L1 | 1.4 (10) |
| `vector-plane` | preset | P0 | 0.3 L11 | 0.3 (10) |
| `venn-diagram` | composite | P0 | 0.1 L14 | 0.1 (1), 0.3 (5), 1.1 (1), 1.5 (4), 2.4 (1), 3.3 (1) |
| `viva` | composite | P1 | 1.7 L45 | 1.7 (1), 2.1 (1), 2.3 (5), 3.1 (1), 3.3 (2) |
| `voice-capture` | primitive | P1 | 1.7 L45 | 1.7 (1), 3.3 (7) |
| `vol-surface` | composite | P2 | 2.3 L144 | 2.3 (14), 3.2 (4), 3.3 (1) |
| `volume-slicer` | composite | P0 | 1.3 L77 | 1.3 (6) |
| `workspace-sim` | composite | P0 | 0.4 L20 | 0.4 (4), 1.1 (3) |
| `written-method` | composite | P0 | 0.1 L2 | 0.1 (5), 0.2 (2) |
| `yield-curve-lab` | composite | P1 | 1.7 L10 | 1.7 (4), 3.2 (5), 3.3 (1) |

### 8.3 P0 confirmation

- **Every P0 lesson has a widget.** All 876 lesson rows in items 0.1 to 1.5 name at least one library widget (0 lesson rows in the whole curriculum name none).
- **Every widget a P0 lesson names is P0.** 0 exceptions [measured]. This includes the widgets the depth-first order pulls forward (0.3), and the presets and modes those lessons use.
- **Sample-lesson screens.** Of the 48 screen rows in the four full sample lessons, 10 name no library id: title and summary screens (art only, by design), and two linear-algebra screens that refer to widgets declared on an earlier screen by their local ids (`combo`, a `vector-combo`; `mm`, a `matrix-multiply`).
- **Modes.** Every mode a P0 lesson marks [mode to add] is accepted as a P0 mode in its widget's entry (8.4). Where a curriculum file said a lesson "falls back to `plot-2d` with `sim-runner`" without its mode, the mode is now in the library and the fallback is not needed.
- **The weekly problems** from 1.5 lesson 1 use `puzzle-workbench` (P0 core) with `scratch-pad`; the Daily 10 and spaced review reuse each item's own widget.

### 8.4 Modes requested by the curriculum files

Each row is accepted. The priority is the priority of the lesson that asks.

| Widget | Mode or option | Priority and source |
|---|---|---|
| `array-strip` | bytes mode | P0, 1.1 L10, curriculum |
| `basis-lab` | `gam` and `kernel` modes | P2, 2.1 L43, L44, curriculum |
| `bench-lab` | denormals | P1, 1.9, curriculum |
| `binomial-tree` | `path-dependent` (lookback, Asian), `trinomial` and `perpetual` modes | P2, 3.2 L2 to L4, L20, curriculum |
| `bit-lab` | C++ precedence | P1, curriculum |
| `bond-lab` | `bootstrap-exam` timed variant without knot handles | P1, curriculum |
| `card-sort` | two-bin sort | P2, 2.1 sample, curriculum |
| `cell-grid` | triangle paint above the diagonal with a mirrored ghost | P1, 1.8 sample, curriculum |
| `ci-ladder` | `variance` model | P1, 1.6 L24, curriculum |
| `cluster-lab` | `gmm` mode | P2, 2.1 L142, curriculum |
| `code-tracer` | `hits` mode expanding hidden built-in scans | P1, 1.8 sample, curriculum |
| `complex-plane` | locus tracer with region shading | P0, 0.3 L93, curriculum |
| `complexity-lab` | three-lane race | P1, 1.8 sample, curriculum |
| `contest-arena` | ICPC penalty of 20 minutes per rejected submission; web-only problems flagged | P2, dsa-cpp request 7 |
| `cv-lab` | `loocv-shortcut` with hat values | P2, 2.1 L25, curriculum |
| `derivation-steps` | `links` from a line to elements of a widget on an earlier screen | P0, 1.3 sample, curriculum |
| `derivation-steps` | fill mode with a `leap` block | P1, 1.6 sample, curriculum |
| `descent-lab` | stochastic mode | P2, 2.1 L19, curriculum |
| `diagnostic-reader` | mypy format | P0, 1.1 L54, curriculum |
| `dist-explorer` | Beta update | P0, 1.5 L84, curriculum |
| `elimination-lab` | floating mode | P0, 1.4 L16, curriculum |
| `error-curves` | predict mode on fixed data with a per-degree table | P2, 2.1 sample, curriculum |
| `estimator-compare` | `trimmed` and `mad` estimators | P1, 1.6 L8, curriculum |
| `filtration-tree` | `radon-nikodym` mode | P2, 3.2 L10 to L13, curriculum |
| `fit-explorer` | `sketch` mode with "Thread every point" and fixed-data "Reveal tomorrow"; compare mode with clipped curves | P2, 2.1 sample, curriculum |
| `forecast-lab` | `ses` and `holt` methods | P2, 2.2 L19, curriculum |
| `four-subspaces` | graph mode | P0, 1.4 L32 and L97, curriculum |
| `game-lab` | Kelly mode, embedding `kelly-lab`'s growth curve per finance decision 17 | P0, moved from P2; 1.5 L154, curriculum |
| `garch-lab` | `gjr` with the news impact curve | P2, 2.2 L26, curriculum |
| `geo-prob` | circle mode | P0, 1.5 L148, curriculum |
| `geometry-board` | points on a circle with a region counter; the $64 = 65$ dissection preset | P0, 0.3 L125, L128, curriculum |
| `graph-explorer` | reflect in $y = x$ toggle | P0, 0.3 sample, curriculum |
| `graph-search` | SCC, bridges and 2-SAT | P1, 1.8, dsa-cpp request 6, curriculum |
| `heat-diffusion` | `finite-difference` mode | P2, 3.2 L88, curriculum |
| `join-lab` | `asof` join | P0, 1.1 L88, curriculum |
| `latency-lab` | `histogram-from-log` | P2, MS4 homework, curriculum |
| `least-squares-fit` | ridge mode | P0, 1.4 L47, curriculum |
| `likelihood-lab` | `logistic` and `exponential-censored` models | P1, 1.6 L65 and ES3 homework, curriculum |
| `loss-lab` | `pinball-set` mode showing a flat minimiser interval | P2, LD3 homework, curriculum |
| `market-maker-sim` | `glft` mode | P2, 3.1 L78, curriculum |
| `markov-chain` | Metropolis mode | P0, moved from P2; 1.5 L134, curriculum |
| `markov-chain` | run-length preset | P0, 1.5 L155, curriculum |
| `markov-chain` | `ctmc` mode with competing exponential clocks, the 3.2 `ctmc-clock` request | P2, 3.2, curriculum |
| `mass-editor` | entropy readout | P2, 2.1 L13, curriculum |
| `matrix-multiply` | entry, column, row and outer views, shape puzzle, multiplication counter | P0, 1.4 L9, curriculum |
| `measure-change` | `importance-sampling` mode | P2, 3.2 L31, curriculum |
| `memory-layout` | false sharing | P1, curriculum |
| `mm-game` | `figgie` mode | P2, 3.3 L92, curriculum |
| `multiple-testing` | `forking` mode for 1.6 L41 | P1, curriculum |
| `multiplier-chain` | tile mode: palette, log axis, target line, partial tile, Glue, halving | P0, 0.3 sample, curriculum |
| `mutant-hunter` | property mode | P0, moved from P1; 1.2 L24, curriculum |
| `mutant-hunter` | C++ mutants | P1, 1.9, curriculum |
| `node-link` | class-diagram layout | P0, 1.1 L52, curriculum |
| `number-line` | float-spacing mode: gaps between neighbouring doubles | P0, 1.1 L4, curriculum |
| `number-theory-lab` | CRT and Grundy values | P2, curriculum |
| `objective-explorer` | likelihood mode | P0, 1.3 L47, curriculum |
| `order-book` | `sequence` replay of a scripted order list | P1, MK1 homework, curriculum |
| `order-lifecycle` | `reconcile-diff` | P2, 2.3 L218, curriculum |
| `path-simulator` | random-walk and price modes | P0, moved from P2; 1.1 L72, L73, curriculum |
| `path-simulator` | `bridge`, `ratio` and asynchronous two-path modes | P2, 3.2 L39, L69, L71, curriculum |
| `pca-lab` | scree view and returns-panel preset | P0, 1.4 L93, curriculum |
| `pointer-walk` | `reach` mode | P1, 1.8, dsa-cpp request 6, curriculum |
| `portfolio-sort` | `hansen-hodrick` beside Newey-West | P2, 3.1 L16, curriculum |
| `pricer-compare` | `pde` method | P2, 2.3 L164, curriculum |
| `puzzle-workbench` | `debrief-variance` mode | P2, 3.3 L40, curriculum |
| `range-query-lab` | sparse table | P2, 2.4, dsa-cpp request 6, curriculum |
| `reflection-principle` | `drift` mode | P2, 3.2 L49, L50, L90, curriculum |
| `regression-lab` | `ar1` errors for 1.6 L56 | P1, curriculum |
| `regression-lab` | `glm` mode | P2, 2.1 L39, curriculum |
| `sampling-lab` | `predict-se`, correlated population `correlated: { rho }` and `ecdf` view | P1, 1.6 L2 and L4, curriculum |
| `sde-stepper` | `cir-feller` mode | P2, 3.2 L84, curriculum |
| `secant-tangent` | motion preset with tower, ruler and time scrubber; signed stops excluding 0; centred-window mode with `handle:Qm`; switching position functions | P0, 1.3 L1, curriculum: lesson 1 cannot be built without them |
| `sequence-lab` | explicit and recursive views side by side, index-origin toggle, two-term mode with ratio row, tolerance band | P0, 0.3 L39 to L43, curriculum |
| `series-explorer` | Fourier mode | P0, 1.4 L53, curriculum |
| `shell-sim` | job control, remote (`ssh`) and `awk` modes | P0, moved from P1; 1.2 L3, L8, curriculum |
| `shortest-path` | Floyd-Warshall | P1, 1.8, dsa-cpp request 6, curriculum |
| `split-scorer` | `chord` mode for the ESL tie | P2, 2.1 L87, curriculum |
| `taylor-builder` | bond preset with a stated compounding convention | P0, 1.3, curriculum |
| `test-lab` | `ks` test | P1, 1.6 L34, curriculum |
| `transform-grid` | non-square $A$, 3D to the plane | P0, 1.4 L17, curriculum |
| `tree-lab` | Euler tour and binary lifting | P1, 1.8, dsa-cpp request 6, curriculum |
| `trial-strip` | arrival marker in Poisson mode | P0, 1.5 L75, curriculum |
| `value-table` | rows that fill as a linked slider visits a stop | P0, 1.3 L1, curriculum |
| `value-table` | deviations column from the learner's mean | P1, 1.6 sample, curriculum |
| `vector-combo` | `readout: after-check` and an export `result` for feedback templates | P0, 1.4 sample, curriculum |
| `vol-surface` | `event` term structures | P2, 2.3 L150, curriculum |
| `vol-surface` | `local-vol` and `heston` | P2, 3.2 L101, L102, curriculum |

### 8.5 Widgets no lesson row names

| Widget | Why it stays |
|---|---|
| `algo-lab` | Every use is through one of its presets |
| `scratch-pad` | The ink layer of long-form homework and the working space of `puzzle-workbench` (assessment 2) |

Dropped: `vim-sim`: No lesson uses it: python-tools decision 19 covers 1.2 L8 with a `text-terminal` recording. Rejected rather than deferred; a later lesson that needs it writes a brief. The canon-gap proposals (`forking-paths`, `shrinkage-lab`, `hac-lab`, `var-backtest` and the rest of canon-gap 5.1) are not widgets: the in-budget lessons it flagged use `multiple-testing` (forking mode, 1.6 L41), `pca-lab` (scree view, 1.4 L95), `regression-lab` (`ar1`, 1.6 L56) and `garch-lab` with `test-lab` (2.2 L30). If the owner accepts a canon-gap course, its curriculum file names widgets and this library adds them through the same rules.

---

## 9. Rejected alternatives and open questions

### 9.1 Rejected

| Alternative | Why rejected |
|---|---|
| One widget per catalogue entry (332 modules) | Duplicates and synonyms would ship twice: 18 catalogue ids are another name for a library widget, and 29 entries merge two or more specs of one widget (section 2) |
| A generic scene engine with every graph composite as a `plot-2d` preset | Decision 4: presets cannot derive state; the logic would move into an expression dataflow language inside content |
| Keeping the Stage 0 primitive names because the prob-stats catalogue and the statistics curriculum file use them | Aliases cost nothing at compile time; four catalogues and the other ten curriculum files use the calc-linalg names |
| `vector-plane`, `matrix-grid`, `linear-map` as aliases | Their Stage 0 configs differ in shape from the 1.4 widgets; a preset's `expand` converts them, so the 0.3 lessons keep their ids |
| Separate `dealer-sim` and `market-maker-sim` | One market model, one `exchange-sim`, two specs; 3.3 play mode would have been a third |
| Two `calibration-lab` widgets (model and self) | Both are stated against observed frequency with the same scoring rules; one reliability core |
| Putting every shared composite in `core` | `core` loads with every lesson; the 80 KB cluster budget would fail |
| Promoting all of 1.7 to P0 because it runs alongside 1.3 to 1.6 | Decision 11 |
| Retaining `vim-sim` for a possible optional lesson | Decision 15 |

### 9.2 Open questions

| # | Question | Effect if unfavourable | How it closes |
|---|---|---|---|
| 1 | Does `core` (37 primitives and inputs plus `code-cell`) fit the 80 KB gzipped cluster budget? [unverified] | Split `core` into `core` (P0 hosts and inputs) and `core-markets` (the P1 finance primitives) | Measured by `size-limit` at the end of L0 |
| 2 | Do composite views stay within 25 KB minified when they lay out four or more primitives (for example `prob-square`, `dist-explorer`)? [unverified] | Move a mode into a sibling composite or a preset | The per-widget budget check in CI |
| 3 | Does `algo-lab`'s one view carry linked-list rewiring and heap sifting at Brilliant quality? [inferred yes, because the gestures live in `node-link` and `array-strip`] | Promote that preset to a composite with a written reason (arch 10.5) | The first two presets built (`sort-lab`, `recursion-tree`) in W4 |
| 4 | Agent build time per size class [unverified] | Wave dates move | Recorded per pull request from W1 |
| 5 | Is `dmath` fast enough for `ml-core` training loops on the budget phone? [unverified] | Use `Math` in visual-only paths and `dmath` only where a number is shown or graded | E1 benchmark |
| 6 | The `downloads` capability for starter suites (finance-projects open item 7) [unverified] | `setup-checklist` project mode offers `.txt` suites with rename instructions | E10 |

