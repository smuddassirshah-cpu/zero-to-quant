# Engine architecture

> **Appendix to `docs/PLAN.md`.** Moved from `docs/blueprint/work/arch-decision.md` on 7 October 2026 and tidied for the blueprint. Section numbers are unchanged, so citations elsewhere (which say "arch" or `arch-decision.md`) still resolve. `docs/PLAN.md` wins where the two differ; this file wins over the widget catalogues and the working papers in `docs/blueprint/work/`. Tidied in place:
>
> | Where | Was | Now |
> |---|---|---|
> | 4.1, 10.5 | `docs/engine/WIDGETS.md` and `docs/engine/ARCHITECTURE.md` | `docs/engine/WIDGET-AUTHORING.md` (so it cannot be confused with `docs/WIDGETS.md`, the library) and this file at `docs/ARCHITECTURE.md` |
> | 4.3 | Seven packages | Plus `@zq/models` (`docs/WIDGETS.md` 0.3) |
> | 5.9, 6.2.1, 6.2.5 | A generator module per course; 50 courses | One generator module per topic; 85 courses; budgets recomputed |
> | 5.9 `CppRuntime` | In-browser Clang or the proxy to Compiler Explorer | In-browser Clang only; the proxy serves the tutor alone |
> | 6.2.2, 14 item 1 | Entry as `<script type="module">`; open question | Classic inline bootstrap with dynamic `import()`, the measured path |
> | 13 | Stage names E0 to E10 | Kept; `docs/PLAN.md` section 11 maps them to its stages |
> | 0.1 decision 7, new decision 36, 4.2, 4.5, 5.3, new 5.14, 8.1.1, 12 risk 7 | Four tiers; about 100 widgets | Five tiers with `scene`: composites written as data over primitives plus a pure model (`docs/PLAN.md` section 3.2, conflict 1) |
> | 4.3 | `@zq/mathcore` without `dmath`; `@zq/graders` without the leak extractor | `dmath` in `@zq/mathcore` from the first engine stage; `leak.ts` in `@zq/graders` (`docs/PLAN.md` conflicts 6 and 7) |
> | 5.10.3, 6.3.1 | No fetch timeouts; no rule for a stalled Python load | `AbortSignal.timeout` on own-file fetches; a load silent for 30 s is a network failure (`docs/PLAN.md` 8.1) |
> | 4.2 | `src/ui/bertie/` without `markup.ts` | `markup.ts` added (`BERTIE.md` decision 19) |
> | 6.4.2 | `connect-src` silent on third-party APIs | No third-party origin: the GitHub and Codeforces calls are withdrawn (`docs/PLAN.md` conflict 5) |
> | 13 | Widget waves beside E5 to E10; content from the end of E6 | `docs/PLAN.md` section 11 orders the build: engine, Python, every P0 widget batch, tutor, progress, assessments, builds, then content |

> **Revised by the `docs/PLAN.md` review, 7 October 2026** (its section 13 lists the findings). Section numbers are unchanged.
>
> | Where | Was | Now |
> |---|---|---|
> | 4.3, 13 | The services widgets' numbers come from had no stage | `docs/PLAN.md` stages 3a to 3f build `@zq/mathcore` numerics and `stats-core` and `@zq/models` data, code, algo and git, each with Python or `git` parity against the pinned versions |
> | 5.7.1, 5.7.3 | Hints open after the lesson's first Check | Per screen: after this screen's first Check or 90 s of active input; `trap` screens after a first Check only |
> | 6.2.6, decision 17 | Drift, garbage collection and rollback read the ignored `dist/artifact/publish-plan.json`; no resume rule; the read-before-publish rule unaddressed | A committed release ledger per release (`releases/<release>.json`) whose hash goes into `meta/release`; the session rebuilds and verifies every file against it; a resume rule; the provenance question goes to Anthropic (`docs/PLAN.md` 12 decision 7) |
> | 6.3.3, risk 16 | One fallback (the spike's layout) for both a behaviour failure and a policy objection | F1 for behaviour (the spike's layout plus `testing`, with raised file limits) and F2 for policy (no Python in the Artifact) (`docs/PLAN.md` 4.3) |
> | 6.5 | A new preview Artifact per lesson | One long-lived preview Artifact, republished per gate, results in its `db` at `ops/gate-<stage>` (`docs/PLAN.md` stage 25) |
> | 8.1, 8.3 | Baselines for every screen, widget state and storyboard, committed | Baselines for widget fixture states (390 px, both themes) and app screens (both widths and themes) only, on an orphan `visual-baselines` branch with a budget; storyboards are pull request artefacts; nightly runs deterministic tutor graders only |
> | Decision 31, 3.2 | CPython 3.11 floor; timeouts there undecided; Python pins unlisted | CPython 3.12 floor (`sys.monitoring`, and SciPy 1.18.0 needs 3.12 [measured]); `tools/py/uv.lock` pins the CI packages to Pyodide's versions |
> | 6.2.3, decision 29, risk 5, 14 item 10 | Page-level `import()` unverified; generator modules per course; "67 MB against 105 MB"; the `db` cap probe in A2 | Measured; per topic; 75 MB; the bounded probe of `docs/PLAN.md` stage 2 |

> **Revision 2, 7 October 2026: the owner's decisions at Blueprint review** (`docs/PLAN.md` revision 2 note and section 4.3). These rows win over anything below that reads otherwise. Section numbers are unchanged; 6.2.7 and decision 37 are new.
>
> | Where | Was | Now |
> |---|---|---|
> | Decisions 15, 16; 5.9; 6.3; risks 5, 16 | Pyodide on both targets; the Artifact's split-archive loader with JSON parts; fallbacks F1 and F2 | **Pyodide on the web app only.** The Artifact publishes only files generated from this repository's own sources, so it has no Python, SQLite or compiler: `PythonRuntime` and `SqlRuntime` are handoff stubs there and every drill returns by result code. 6.3.3 stays as the record of a measured layout, not built |
> | Decision 24; 3.1; 6.1; 6.2; new 6.2.7 | Every dependency bundled as the Artifact's own files | **Third-party JavaScript from CDNs at exact versions in the Artifact**, through an import map written from `cdn.lock.json`; workers import self-contained modules by full URL; the web app keeps bundling |
> | New decision 37; 5.11; 11.6; 14 items 2, 4 | KaTeX fonts as own files; MathLive in both targets | **MathML in the Artifact** (KaTeX `output: 'mathml'`, system maths fonts, no KaTeX CSS or fonts); MathLive web only; the plain expression field with the symbol bar and a live MathML preview in the Artifact |
> | 4.2, 4.4 | `tools/pysplit`; `loader-split.ts`, `zipstore.ts`, `verify.ts` | `tools/pyvendor` (fetch for the web build only), `tools/cdn` (lock and drift check), `tools/release/provenance.ts`, `platform/artifact/cdn.ts`, `styles/math.css` |
> | 6.2.5 | About 214 files and 190 MB per release, Python 15 files and 67 MB | About 198 files and 125 MB: 36 app files, about 162 content files, no Python; limits 230 files and 150 MB per release |
> | 13 E0 (spike S1) | Own fonts, `FontFace`, the JSON-part Python layout, MathLive | CDN loading through an import map (page and module worker), import-map integrity, the UMD fallback, MathML quality and `TexSlots` in MathML; the platform and capability checks kept |
> | Decision 8, 6.4.1, 9.2 | 22 widget clusters | 26 (`analysis`, `numerics`, `optim`, `dl`; `docs/WIDGETS.md` decision 19) |
> | 4.3, 13 | Services 3a to 3f | Plus `@zq/models/analysis` (`docs/PLAN.md` stage 3g) for A1, and `numerics`, `optim`, `research` with their P2 waves |
> | Decisions 7 and 29, risk 7 | 314 widget ids, 125 P0 scenes; 21 generator modules | 338 ids, 131 P0 scenes and 22 bespoke (`docs/WIDGETS.md` 0.2); 26 generator modules, one per topic (`docs/CURRICULUM.md` 0.1) |

> **Second review round of `docs/PLAN.md`, 7 October 2026** (its section 13). Edited in place: decision 7 (338 ids, 24 presets), 8 (one bundle per course), 31 (only the web app runs Python), 36 (about 240 AD less), 37 and 5.11 (`TexSlots` binds sentinels on both outputs, `<mn>` in MathML), 0.3 (CPython 3.12), 3.1 (`@preact/signals-core` 1.14.4), 3.2 (esbuild per topic), 5.7.2 (live-code screens in the Artifact resolve as `read` and are finished in the web app), 6.2.7 item 5 (provenance reads esbuild's metafile too), 9.2 (whole-path learner), 11.3 (exactly two sinks), 12 risk 7 (four pilots, 338 ids), 13 E0 (the single S1 list of `docs/PLAN.md` stage 2) and E9 (the decision-13 web host), 14 items 6 and 20. Wherever 6.1 (`base`), 6.3.1, 6.4.2 and 6.4.3 say GitHub Pages, read the web host of `docs/PLAN.md` 12 decision 13 (default: Cloudflare Pages behind Access, `base` `/`); the meta CSP and the no-isolation-headers design stay, so the hosts remain interchangeable.

Working paper for the Stage 2 Blueprint, 6 October 2026. Scope: the stack, the module tree, every interface between the engine, the widget library, the content, the tutor and the two runtime targets, the two builds, versioning and migrations, testing and CI, developer experience, risks and the engine's build stages. Input to `docs/PLAN.md` sections 3, 4, 6, 8, 10 and 11. With `CONTENT-FORMAT.md`, `AI-TUTOR.md`, `ASSESSMENT.md`, `BERTIE.md` and the six widget catalogues, it is meant to leave Phase 2 with no architectural decision to make.

**How to read it.**

- Section 0 lists every decision with the rejected alternatives, what was measured for this paper, and what this paper changes in the other working papers.
- Section 1 states the requirements the engine has to meet, collected from the other papers.
- Section 2 is the stack decision: three candidates, the measurements and the choice.
- Sections 3 and 4 pin the toolchain and lay out the repository.
- Section 5 is the contract layer: every TypeScript interface the build implements.
- Sections 6 to 10 cover the two build targets, versioning and migrations, testing and CI gates, performance budgets and developer experience.
- Sections 11 to 14 cover security and failure behaviour owned by the engine, risks, build stages and open questions.
- The Review log at the end lists what an adversarial staff-engineer review found on 6 October 2026 and what changed.

**Ownership.** `CONTENT-FORMAT.md` owns the content format, the compiler, the graders and the verifier; `AI-TUTOR.md` owns Bertie's brain and the proxy; `ASSESSMENT.md` owns the progress model, mastery, scheduling and exams; `BERTIE.md` owns the mascot's art and rig; the widget catalogues own each widget's behaviour. This paper owns everything those papers call "the engine": the runtime they all plug into, and the two builds. Where a paper deferred a choice to "the engine blueprint", the choice is made here and listed in section 0.3.

**Evidence tags** follow the sibling papers: [measured] for values measured while writing this paper (section 0.2), [sourced] for facts from the platform contracts or the brief's verified platform list, [recalled] for facts from memory that a person should confirm, [unverified] for facts not checked, [inferred] for deductions, [our choice] for decisions without outside evidence. Values taken from a sibling paper cite it and carry its tag.

---

## 0. Decisions in brief

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | UI stack | **TypeScript 6.0.3, Preact 11.0.0, @preact/signals 2.11.3, Vite 8.3.3** (candidate a) | (b) Lit 3.3.3 web components with Vite; (c) no framework: an in-house renderer with signals | With render discipline (decision 2), Preact's drag frames and mount times equal hand-written DOM code; Lit was 0.3 to 0.6 ms faster on the base widget, inside run-to-run noise, and 1.0 ms slower on the heavy one [measured, section 2.3]. The decision therefore falls to maintainability: typed JSX and hooks are the idiom agents write most reliably, type-checked end to end; Lit's templates are strings the compiler does not check and its shadow DOM fights KaTeX's global stylesheet and our token cascade; an in-house renderer re-creates exactly the machinery where the Stage 1 lesson's 23 defects lived |
| 2 | Render discipline | **Per-frame values are signals bound straight to attributes and text; static layers sit in memoised components; dense layers go to Canvas 2D.** A lint rule and a per-widget frame-time test enforce it | Free-form components that read state in render | With 1,200 static SVG cells on screen, a component that re-renders everything costs 5.2 ms median per drag frame against 2.8 ms for the disciplined version, at 4x CPU throttling on Preact 11 [measured]. The disciplined version matches hand-written DOM code (2.8 ms) |
| 3 | Preact major | **11.0.0, exact pin**; 10.29.8 is the named fallback | 10.29.8 now and a migration later | Preact 11 re-renders the undisciplined case 37% faster than 10.29.8 (5.2 against 8.2 ms median) [measured]; signals, Prefresh and the Vite preset declare 11 [measured: peer ranges]; the build runs for months, so starting on 11 avoids a major upgrade mid-build. 11.0.0 is six days old, hence the exact pin and the fallback, which ran the same benchmark code unchanged [measured] |
| 4 | TypeScript | **6.0.3** (16 April 2026) | 7.0.2, the native compiler (latest) | typescript-eslint 8.71.1 declares `typescript >=4.8.4 <6.1.0` [measured]; type-aware lint rules are part of the agent guard rails. Move when typescript-eslint supports 7 |
| 5 | Widget contract | **A pure logic module (Node-safe), a Preact view and a build-time schema per widget; the engine's `WidgetHost` implements the lifecycle once** (lock, marks, highlight, annotate, ghost preview, reset, reveal, serialisation, timers, announcements) | Each widget implements a 20 to 25 method instance interface (`widgets-stage0.md` 1.1, `widgets-calc-linalg.md` 2.2) | The prototype's defects were in machinery: timers, state and XP. Writing the machinery once and keeping widget code to pure functions plus a view makes 100 widgets testable in Node and leaves agents nothing stateful to get wrong |
| 6 | Widget state | **Two parts: `a` (answer state, graded and saved) and `v` (view state: zoom, step, time cursor)** | One state object | Show-why may tween only `v`, so "show-why never edits answer state" (calc-linalg 2.6) becomes a type rule; Try again restores `v` from a snapshot |
| 7 | Library tiers | **Five tiers: primitives (29) and inputs (8), hand-written; scenes (about 225, P0 131): composites written as data over primitives plus a pure model, turned into widget modules by the engine (decision 36, section 5.14); bespoke composites with their own view (about 50, P0 22); presets (24): configuration over a base widget, expanded at compile time** (revised for `docs/PLAN.md`; `docs/WIDGETS.md` 0.2 gives the 338 ids) | Every catalogue entry as a module with a view; this paper's first estimate of about 25, 75 and the rest | The library has 338 ids, 277 of them composites (draft 1: 314 and 254). A preset costs a config transform and a test; a scene costs a layout, a model function and fixtures, not a component; only interactions no primitive offers get a view of their own |
| 8 | Code splitting | **One lazy chunk per widget cluster (26 clusters since revision 2); modules shared by two or more clusters (primitives, inputs, render helpers, `@zq/mathcore`) go to the `w-core` cluster chunk, never to the entry; one content bundle per course (content-format decision 13; `docs/PLAN.md` 5.2); lazy chunks for KaTeX, MathLive, the Compute Engine parser and MiniSearch on the web, which the Artifact loads from the CDN instead (decision 24; MathLive is web only)** | A chunk per widget; one bundle; shared modules merged into the entry | A chunk per widget is about 100 more files against 255 per publish and 511 per version [sourced]; one bundle makes the first load pay for Stage 3; merging shared widget code into the entry would move every primitive used by two clusters into the first load, and the entry budget (section 9.2) would fail as the library grows |
| 9 | CSS | **Design tokens as custom properties, CSS Modules per component, one stylesheet per target (`cssCodeSplit: false`)** | A CSS file per chunk; CSS-in-JS | Saves about 25 files; widget styles are present before a lazy widget renders, so no unstyled flash; one own-file stylesheet is within the Artifact's style policy [sourced] |
| 10 | Runtime validation | **Classic `zod` 4.6.5 only in workers, Node and CI; `zod/mini` on the main thread** | Classic zod everywhere | A one-object schema bundles to 92 KB gzipped with classic zod and 6.4 KB with `zod/mini` [measured]. Course bundles, imports and remote events are validated in the data worker, which is where classic zod lives |
| 11 | App state | **Signals in small per-domain stores; progress is the event fold of `ASSESSMENT.md` 13, run in the data worker for rebuilds and on the main thread for single events** | A global store library; mutable progress documents | XP, streak and mastery shown on screen are derived, never incremented by UI code, which removes the class of XP defects the prototype had |
| 12 | Lesson player | **A pure reducer `step(state, event) -> [state, effects]` and a separate effect runner** | XState; state in components | The whole Check, Continue and feedback machine (design research 5.4) becomes a table of tests; no dependency; agents can read it |
| 13 | Timers, frames, listeners | **Every one belongs to a `Scope`, disposed on leave, Try again and Start over; a grade generation number cancels stale show-why**; raw timers are a lint error in widgets and screens | Ad hoc timers with guards | Generalises the prototype's `showGen` fix, which was the cure for its timer defects |
| 14 | Randomness | **Philox4x32-10 counter-based generator in `@zq/mathcore`**, addressed by (seed, stream, index) | mulberry32 (prototype); xorshift | Calc-linalg decision 9 needs addressable draws; Philox uses only 32-bit integer multiplies, so every engine gives identical bits |
| 15 | Python | **Pyodide 314.0.7 on the web app only: one worker, the native loader. None in the Artifact** (revision 2), where every drill hands off by result code | Pyodide in the Artifact through the split-archive loader (draft 1, measured working on the owner's iPhone); MicroPython (dropped by the owner) | The owner's publishing rule: the Artifact publishes only files generated from our sources, and Pyodide is a third-party binary. One Python target keeps one grader and one test protocol |
| 16 | Python files in the Artifact | **Withdrawn by revision 2: none are published.** Draft 1's decision, kept as the record of section 6.3.3: **every published file is genuinely the type its extension names. Each load group's archive members ship as JSON parts of at most 8 MB holding every member's original deflate-compressed bytes as base64; the worker rebuilds each archive in memory from those bytes (no recompression), Python's `zipfile` checks every member's CRC-32 on extraction, and our manifest's SHA-256 checks every part** | Concatenated side modules served as `.wasm` (this paper's first draft); one `.wasm` per side module (the spike's layout); wheels renamed to a served extension | A concatenation of side modules is not WebAssembly, so serving it as `.wasm` sidesteps the host's served-type list, which `widgets-programming.md` 13.1 already refused for renamed archives without the platform's confirmation. The spike's layout needs 276 side-module files for the scientific stack [measured, section 6.3.3], over 255 per publish. The whole stack is 153 MB raw, over any Python budget that leaves room for content, but about 67 MB in 15 files in this layout [measured] |
| 17 | Artifact release | **Content-addressed files; a committed release ledger per release, its hash in `meta/release`; a publish plan in batches derived from the new and previous ledgers (content first under the live page, then the new page, then garbage collection; every publish carries a page and every intermediate version is a working app, because the tool refuses a publish without the page and the host reloaded the open page into each version [measured: S1, 7 October 2026]; `docs/DECISIONS.md` B24), resumable from the first step whose effect is not visible; budgets per release, for the retained version and for the peak (section 6.2.5)** | Ad hoc publishes; a plan kept only in ignored build output | A full turnover must fit 511 files per version with the old release still live, and every app release renames about 40 chunks because hashed import specifiers cascade |
| 18 | Web offline | **vite-plugin-pwa 2.0.0 with `injectManifest` and Workbox 7.4.1**: app precached, content and Python cached by hash at runtime, per-course "Keep offline" | `generateSW`; a hand-written service worker | Our routing of hashed content, Python and update timing needs code; Workbox gives tested precaching and strategies |
| 19 | Routing | **Hash routes keyed by content ids; a typed in-house router of about 80 lines** | Path routes; preact-iso; wouter | Neither the Artifact page nor GitHub Pages can rewrite paths; ids are identity (content-format 4.1), display numbers are breadcrumbs. In the Artifact frame a slash route such as `#/learn/crs.numwork` round-trips through `location.hash` and fires `hashchange` within 2 ms [measured: S1, 7 October 2026]; the system back gesture fires nothing there, so the router never depends on it (section 5.8) |
| 20 | Test layers | **Vitest 5.0.3 in Node for pure modules; Vitest browser mode on Playwright Chromium for widgets; Playwright 1.63.0 end to end on both targets, the Artifact through a local host emulator with a fake `window.claude`** | jsdom or happy-dom for widgets; Storybook | Widgets need layout, pointer capture and SVG geometry, which DOM emulators lack; the in-app gallery uses the real host |
| 21 | Visual regression | **Playwright screenshots in the pinned Playwright container, 390 and 1,280 px, light and dark, under a `test` motion mode** | A hosted service | No third party; deterministic fonts and frames |
| 22 | Package manager | **npm workspaces** (npm 10.9 with Node 22.22) | pnpm 12.9.1; Bun | Every agent container already has npm; at ten workspace packages pnpm's speed and strictness gain little, and `knip` catches undeclared dependencies |
| 23 | Lint and format | **ESLint 10.12.0 with typescript-eslint strict type-checked rules, eslint-plugin-react-hooks 7.1.1 and our `eslint-plugin-zq`; Prettier 3.9.9; stylelint 17.16.0; knip 6.39.0** | Biome alone; eslint-plugin-jsx-a11y | Our custom rules need ESLint. jsx-a11y last released in October 2024 and declares ESLint up to 9 [measured]; axe in the browser tests covers the outcome |
| 24 | Dependencies in the Artifact | **Revised by revision 2: no third-party file is published. Third-party JavaScript loads at run time from cdnjs where it hosts the identical file, otherwise jsDelivr's `/npm/` path, at exact versions listed in `cdn.lock.json` (URL, SHA-384, import kind); the page resolves bare names through an import map with `integrity`, workers import full URLs; fonts only from Google Fonts. The web app bundles everything** (section 6.2.7) | Everything bundled as own files (draft 1; the publishing rule forbids it); jsDelivr's `+esm` builds (dependency ranges resolved on the CDN, so `@preact/signals`' peer `preact` would not be ours to pin); unpinned or `@latest` URLs | The rule; exact versions keep both targets on the same code; the nightly drift check and the host's CSP bound what SRI cannot cover |
| 25 | Sound | **Synthesised with Web Audio** from the design research 4.9 table | Audio files | Zero files against the budget; four short tones |
| 26 | Two tabs on one device | **Web Locks leader election: one writer per device; other tabs read only with "Use here"** | A device id per tab | `ASSESSMENT.md` 13 assumes one writer per device id; two tabs would collide on `seq` |
| 27 | Telemetry | **None leaves the device; a local ring-buffer log and a "Copy diagnostics" action** | Remote error reporting | Privacy (assessment 15), and the Artifact can reach no other host [sourced] |
| 28 | Bertie | **The prototype rig ported to TypeScript, mounted imperatively inside a Preact wrapper, sharing `engine/motion/spring.ts`** | Rendering the rig through Preact | The rig writes SVG transforms every frame; that belongs outside the virtual DOM (decision 2) |
| 29 | Generator modules | **Self-contained ES modules per topic (21 files), built by the content compiler with esbuild, loaded by dynamic import** | Generators importing the app's hashed chunks | Content and app chunks stay independent; a generator module is plain data in, plain JSON out |
| 30 | Release coupling | **The app and the content are always built and released together; the page names the content manifest file by its hash (`<meta name="zq-manifest">`), and the manifest is a content-addressed file of its own, not part of the entry chunk** | Independent content releases; the manifest embedded in the entry chunk (this paper's first draft) | One compatibility state to test. With the manifest inside the entry, every content fix renames the entry, and through hashed import specifiers every lazy chunk: about 40 files republished to the Artifact and 1.8 MB re-precached on the web for a typo. Depth-first content means years of content-only releases, so a content release now changes only the page, the manifest and the courses it touches |
| 31 | Python timeouts | **Two levels: a soft deadline, checked from a `sys.monitoring` callback on backward jumps (every loop iteration) once per 1,000 jumps, raises `ZqTimeout`, a `BaseException` subclass that a learner's `except Exception` cannot swallow; the page's watchdog terminates the worker only when the soft deadline does not fire (a long call inside C code)** | Watchdog only (this paper's first draft); `sys.settrace` line events | The web app, the one target that runs Python, cannot use Pyodide's interrupt buffer (section 6.3.1). With the watchdog alone, every learner infinite loop costs a worker restart, about 3 to 4 s on the owner's iPhone. `sys.monitoring` exists from Python 3.12 and a raising callback propagates into the monitored code [recalled]; line tracing costs more per line than a jump callback costs per loop iteration [recalled]. CI's floor is therefore CPython 3.12, not 3.11 (SciPy 1.18.0, Pyodide's version, also requires 3.12 [measured: `uv pip compile`, 7 October 2026]), and the CI harness wraps every drill run in a subprocess wall-clock limit as an outer guard. Overhead is measured at E8; above 1.3 times on the reference drills, the soft deadline is dropped and the watchdog alone remains |
| 32 | Artifact update signal | **A `meta/release` document in `db`, written by the release session through `ArtifactData` and read with one `onSnapshot`; `version.json` stays the web target's signal**. A write to `meta/release` reached the open page through that subscription about 3 s after the write's timestamp (cross-clock, a hint) [measured: S1, 7 October 2026] | `version.json` on both targets | Kept after S1. The host reloaded the page open in the foreground on the owner's iPhone to the newest version after each publish [measured: S1, 7 October 2026], and other open views reload too [sourced: `artifact.d.ts`, contract 0.2.73]; a backgrounded app, a second device and the desktop and web viewers were not measured [unverified]. `version.json` reported each load's own release on all five runs that fetched it [measured: S1], but each was a fresh load of the newest version, so the reads cannot tell version-scoped paths from newest-version serving; that a view's relative URLs serve the version it loaded is [inferred from `artifact.d.ts` 0.2.73, which states it for the publishing view] and unmeasured (`docs/DECISIONS.md` B28). The signal matters for a page the host did not reload |
| 33 | Compiler access to widgets | **`@zq/compiler` takes a `CompilerRegistry` as a parameter; `tools/zq` builds it from a generated `src/widgets/registry.node.gen.ts` (logic, schema and preset files, no views)** | The compiler package importing `src/widgets` directly | Section 4.5 forbids packages importing `src/`; injection keeps the package testable with a fake registry and keeps views and CSS out of Node |
| 34 | Single-key shortcuts | **On by default, with a Settings switch "Single-key shortcuts"; never active while focus is in a field or on a control that handles the key itself** | Always on | WCAG 2.2 SC 2.1.4 (level A) requires a way to turn off single-character shortcuts, and this paper claims AA |
| 35 | Phone text entry | **Numeric and expression answers on touch devices use the in-app keypad and symbol bar (`inputmode="none"`, as the prototype's exam screen does); free text and code keep the system keyboard, with the button row lifted above it through `visualViewport`** | The system keyboard everywhere | The system keyboard covers the Check row on a 390 px phone and offers no fraction or minus keys that match the graders' forms |
| 36 | Scenes | **A `scene` tier: `defineScene({ init, derive, layout, answer, describe, ... })` in a pure `scene.ts`; bindings are typed paths into answer state, view state, derived values and config; `derive` calls `@zq/models` and `@zq/mathcore`; the generic `SceneView` renders the layout with the primitives' controlled components and memoises every layer that binds only config. A composite is a scene unless it needs free text or code editing, a clock-driven loop, a service with its own state machine, a gesture no primitive offers, or fails the frame budget as a scene** | Every composite with its own view; a declarative dataflow inside content (`docs/WIDGETS.md` decision 4 rejected that, rightly) | About 240 agent-days less for P0 alone (about 240 against about 480, `docs/PLAN.md` 3.2); render discipline (section 2.5) holds by construction; content still holds only configuration |
| 37 | Maths in the Artifact | **MathML (revision 2).** KaTeX 0.19.0 from the CDN with `output: 'mathml'`, rendered in the system's maths font through `styles/math.css`; no KaTeX CSS or fonts. `TexSlots` marks each slot with a sentinel `\text{}` token on both outputs, one binding path (second review round): it binds the HTML span's text node on the web, and in every MathML tree (the Artifact's output and the web's hidden copy) it swaps the sentinel `<mtext>` for an `<mn>` built with `createElementNS`, so slot digits use the maths font and screen readers hear the live value. `\htmlData` attributes are an HTML-output feature: KaTeX 0.19.0's MathML output drops them [measured: S1, 7 October 2026], so slots never depend on them, and the built-in `\htmlData` anchors terms on the web only. In the Artifact, with the runtime flag `artifact.termBinding` on, `TexService`'s authored configuration defines `\htmlData` as a KaTeX function macro that renders `term=<k>` as `\textcolor{<sentinel k>}{<body>}`, with a reserved sentinel colour, and any other attribute as its body alone; it acts at render time, so content bundles, `contentHash`, `answerHash`, tutor context and search are the same on both targets. A term binding turns the scoped `<mstyle mathcolor>` KaTeX emits for each anchor into the term's target, on the model of `TexSlots`' sentinels, and the TeX annotation keeps the authored TeX [measured: KaTeX 0.19.0 in Node, 8 October 2026: `\htmlData{term=ab}{b^2}-4ac` with the macro and `output: 'mathml'` renders an `<mstyle>` with a term-range `mathcolor` around exactly `b^2`, and the annotation reads `\htmlData{term=ab}{b^2}-4ac`], so `docs/DECISIONS.md` B20 concerns only `TexSlots`' slot sentinels; its device check is `docs/PLAN.md` stage 12's iPhone check, taken in stage 25's preview Artifact (`docs/PLAN.md` 11.1), whose build turns the flag on, off by default, and `live-formula`'s term list is the floor and, until the owner decides, the default (proposed for the owner, `docs/DECISIONS.md` B27; section 14 item 20). On the owner's iPhone the MathML lays out natively, the owner accepted all 40 specimen formulas, and the swapped `<mn>` digits match the maths font and VoiceOver reads their current values [measured: S1, 7 October 2026, with the TeX annotation also rewritten, `docs/DECISIONS.md` B20]. MathLive is web only; the Artifact's expression input is the plain field with the symbol bar and a live MathML preview, graded by the same Compute Engine parser | MathML emitted at build time; MathLive without its fonts; KaTeX HTML output with fonts as `FontFace` from own files | Fonts load only from Google Fonts and no third-party file may be published; generated items, live formulas and Bertie's replies need run-time rendering anyway, so build-time MathML would be a second path; MathLive lays out with KaTeX's font metrics [recalled] |

### 0.2 What was executed

All on 6 October 2026, in a scratch folder outside the repository [measured]:

- **Versions.** `npm view` for every package in section 3. Notable: TypeScript 7.0.2 is `latest` but typescript-eslint 8.71.1 declares TypeScript below 6.1; Preact 11.0.0 was published on 30 September 2026 after release candidates from 10 August; @preact/signals 2.11.3, @prefresh/core and @prefresh/vite declare Preact 11; @preact/preset-vite 2.10.6 declares Vite 8 and `@babel/core` 7; vite-plugin-pwa 2.0.0 declares Vite 8; Vite 8.3.3 bundles with Rolldown 1.2 and names its options `build.rolldownOptions` and `output.codeSplitting`.
- **Frame benchmark.** One widget written four ways: Preact rendering everything in one component ("naive"), Preact with static layers memoised and per-frame values bound as signals ("split"), Lit 3.3.3 in light DOM, and hand-written DOM with `@preact/signals-core` effects (candidate c). The widget: a draggable vertex of a parabola, a 200-point curve, a tangent, a readout and a 12-row table depending on it, beside a static grid of 42 lines and 22 labels; a heavy variant adds 1,200 static cells. Chromium 141 (Playwright build 1194), viewport 390 by 844, CPU throttled through the DevTools protocol, one update per animation frame, timing script plus a forced layout, 3 runs of 400 frames after 60 warm-up frames. Results in section 2.3.
- **Mount benchmark.** The heavy variant, time from module start to the first frame after mount, 7 runs at 4x throttling.
- **Sizes.** esbuild 0.28.2 minified and `gzip -9`: framework baselines, KaTeX, MathLive, the Compute Engine parser, MiniSearch, ts-fsrs, fflate, and classic zod against `zod/mini` for the same schema. Results in sections 2.3 and 9.
- **Pyodide.** The `pyodide` 314.0.7 npm package and its `pyodide-lock.json`: 357 packages; NumPy 2.4.6, pandas 3.0.2, SciPy 1.18.0, statsmodels 0.14.6, scikit-learn 1.8.0, matplotlib 3.10.8 with 19 archives in their dependency closure; `pyodide.asm.wasm` 9,598,218 bytes, `python_stdlib.zip` 2,545,637 bytes, `pyodide.asm.mjs` 1,250,344 bytes. Wheel sizes for SciPy and the rest could not be measured while the first draft was written: jsDelivr and the GitHub release host were blocked.
- **Pyodide wheels (added in review, same day).** The 314.0.7 release tarball (337,536,678 bytes) streamed from GitHub's release host, which was reachable by then; the 30 archives of the six load groups (closures from `pyodide-lock.json`) measured with the spike's strip rules (no `tests/`, `.pyi`, `.c`, `.h`, `.pxd`, `.a`). Results in section 6.3.3. `pyodide.asm.wasm` gzips (`-9`) to 3,542,413 bytes. `hypothesis` is not among the lock file's 357 packages; `sortedcontainers` is. jsDelivr still answered 403.
- **eval scan.** No `new Function` and no `eval(` in KaTeX 0.19.0, MathLive 0.111.0, the Compute Engine `latex-syntax` entry, Preact or Lit; 6 `eval(` call sites in `pyodide.asm.mjs`, the Emscripten glue, which runs only inside the Python worker.
- **Fonts.** KaTeX ships 20 fonts in three formats; the 20 `woff2` files total 259,792 bytes. MathLive ships a font folder of the same 20 names and the same total size.

### 0.3 What this paper changes in the other papers

| Paper | Was | Now | Why |
|---|---|---|---|
| `widgets-stage0.md` 1.1, `widgets-calc-linalg.md` 2.2, `widgets-programming.md` 2 | Each widget implements a lifecycle instance (`getState`, `setState`, `lock`, `mark`, `showWhy`, `reveal`, `reset`, `describe`, `targets` or `ids`, `highlight`, `annotate`, `preview`, `on`, `destroy`) | Section 5.3: pure `WidgetLogic` plus a view; the host does the rest. Section 5.6 maps every old method to its new home | Decision 5 |
| `widgets-stage0.md` 1.10, 1.11; `widgets-programming.md` 0.1 decision 3, 2.4, 2.10; `CONTENT-FORMAT.md` 7.6 | MicroPython with `ulab` in the Artifact, handoff otherwise; drills tagged compatible | Pyodide on the web app (section 6.3); in the Artifact every drill hands off (revision 2) | The owner's decision after the iPhone spike, then his publishing rule |
| `ASSESSMENT.md` 17 | Drills tagged `micropython-ok` | Dropped; drills declare `needs`, and the compiler aggregates them per course | As above |
| `widgets-stage0.md` 1.10 | Artifact dependencies from `cdn.jsdelivr.net/npm/` with `integrity` | Draft 1 bundled them as own files; revision 2 returns to pinned CDN copies through an import map with `integrity` (decision 24) | The publishing rule |
| `widgets-stage0.md` 1.8; `AI-TUTOR.md` 0.2 | Element ids `kind:name`, multi-widget prefix `w2/` | Kept; the prefix is the screen's widget id, not a position: `grid/cell:5,3` | Positions change when an author adds a canvas widget; local ids do not (content-format 4.1) |
| `CONTENT-FORMAT.md` 3.2, 8.2 | The runtime validates bundles with the shared zod schemas | It does, in the data worker only (decision 10) | Main-thread size |
| `CONTENT-FORMAT.md` 9.2 | Preview routes under `#/preview/...` on the dev server | Kept, plus `#/gallery/<widget>` and the `dev:artifact` emulator (section 10) | Widget-level preview |
| `BERTIE.md` 12.1 | `src/ui/bertie/*.js`; its own `spring.js` | `src/ui/bertie/*.ts`; the integrator moves to `src/engine/motion/spring.ts` and Bertie imports it | One spring implementation |
| `AI-TUTOR.md` 11.1 | "If the engine blueprint chooses JSDoc-typed JavaScript..." | TypeScript throughout; the tutor's reply schemas use `zod/mini` on the main thread | Decisions 1 and 10 |
| `AI-TUTOR.md` 6.3.6 | Proxy token entered in Settings (store unstated) | Kept in IndexedDB through `KeyValue`, never `localStorage`; section 11 records the residual risk | Engineering floor: no credentials in `localStorage` |
| `ASSESSMENT.md` 13.7 | A device id per install, one writer per device | Plus a Web Locks writer election across tabs (decision 26) | Two tabs would share a device id |
| `design-research.md` 8.2 | URL scheme `/learn/{stage}/{topic}/{course}/{level}/{lesson}/{screen}` | Hash routes by id, `#/lesson/<lsn id>/<screen id>`; the stage-to-screen path is a breadcrumb | Decision 19 |
| `design-research.md` 4.1 principle 8 | "A shared Rive file or a shared JS/CSS state machine" | Shared TypeScript state machines and Web Animations; no Rive (agrees with `BERTIE.md` 11) | Rive's runtime and asset type do not fit the Artifact |
| `widgets-calc-linalg.md` 2.10, `widgets-stage0.md` 1.9 | Two different reference phones | One budget device class and one CI proxy (section 9.1) | One number to test against |
| `CONTENT-FORMAT.md` decision 18, 3.2 (`RuntimeTag`, `Drill.aim`), 6.11, stage C7 | Tags `micropython-ok`, `ulab-ok`, `pyodide-core`, `web`; MicroPython as the Artifact's fallback | `RuntimeTag` and `aim` dropped. CI runs every drill on CPython 3.12 and Pyodide 314.0.7; where a drill runs is decided at run time from its `needs` against `PythonRuntime.available()` (section 5.9), which in the Artifact is the handoff stub (revision 2). C7's MicroPython checks go | The owner dropped MicroPython |
| `CONTENT-FORMAT.md` 12.1 | `targets(config)` static form with labels and roles; recipes with argument schemas; `exports` with per-element metadata; `resolve(config, expr)` | `staticTargets`, `recipeArgs` (in `schema.ts`), `exports`, `elementMeta` and `resolvers` on the widget contract (section 5.3), reached by the compiler through `CompilerRegistry` (decision 33) | The first draft's `staticIds` returned ids only and had no recipe argument schemas, so the compiler could not check hint labels or recipe arguments |
| `CONTENT-FORMAT.md` 5.4, 12.2; `ASSESSMENT.md` 3 and 10 | `hash32(id, seed)`; `hash32(attemptId, slotIndex, k)`; this paper's `hash32(string)` | One definition: `hash32(...parts: (string \| number)[])` (section 5.1) | Three spellings of one function |
| `CONTENT-FORMAT.md` 5.4, `AI-TUTOR.md` 2.11 | `makeWhere(partial, seed)` assumed of the engine | `GeneratorModule.makeWhere` (section 5.9) | It had no interface here |
| `CONTENT-FORMAT.md` 8.2 | About 250 files and 105 to 135 MB per version, Pyodide as 69 files and 49 MB | Section 6.2.5: about 198 files per release and no Python (revision 2) | The publishing rule |
| `CONTENT-FORMAT.md` 3.2 `Drill.needs` | `'sklearn'` | Kept; `PyPackage` here now spells it the same way (it said `'scikit-learn'`) | One enum |
| `ASSESSMENT.md` 12.5 | The whole `db` rule set (its decision 32) | Adopted unchanged, plus one rule for `meta` (section 6.2.4); this paper's first draft had declared a different root rule | One owner for the rule set |
| `widgets-programming.md` decision 9, 2.10 table | `cpp-runner` and `shell-interpreter` named; no engine interface | `CppRuntime` (web only, `null` in the Artifact) and shell drills graded in-widget (section 5.9) | Every drill language needs a contract |

---

## 1. What the engine must do

Collected from the other papers, as the acceptance test for this architecture:

1. **Content is data.** No lesson ships code. Lessons, items, sets, exams and drills arrive as compiled JSON per course; generators as one ES module per course (content-format 8.2). The engine renders any valid lesson with zero lesson-specific code (widgets-stage0 2.8).
2. **A widget library at catalogue scale.** 332 distinct ids across six catalogues [measured], written mostly by agents and reviewed by the owner, each with a check, keyboard path, text alternative, tutor hooks, show-why recipes and generators where needed.
3. **Brilliant-grade interaction.** Direct manipulation redrawn every pointer frame, springs only on release, show-why morphs of 480 to 800 ms, a living mascot, celebrations that can be skipped, reduced motion everywhere (design research 4).
4. **Two targets, one codebase.** The Artifact (no service worker, own files plus a few CDNs, 255 `files` entries per publish with removals counted and the page in every publish [measured: S1, 7 October 2026], 511 files per version, `sample`, `db`, `user`, `downloads` capabilities) and a static web app (offline PWA, Pyodide with the scientific stack, the tutor through a proxy).
5. **The tutor from day one,** behind one service with two backends, reading widget state through `describe`, `targets`, `secret` and `tryable`, acting through validated effects (ai-tutor 5, 6).
6. **Assessment and progress** as an append-only event log with a deterministic fold, single-writer documents in `db`, export and import (assessment 13, 14).
7. **Verified correctness.** One grader module shared by runtime and CI (content-format 7.1); every random draw reproducible.
8. **Accessibility** to WCAG 2.2 AA: keyboard and single-pointer paths for every drag, a live region, text and table views (widgets-stage0 1.7).
9. **Budgets.** Per-frame script at most 4 ms for primitives and 8 ms for composites at P95 on the budget device; tap to response within 200 ms; Check within 150 ms for non-code checks (widgets-stage0 1.9, calc-linalg 2.10, content-format 7.1).

---

## 2. The stack decision

### 2.1 Candidates

| | (a) Preact + signals + Vite | (b) Lit + Vite | (c) No framework + signals + Vite |
|---|---|---|---|
| Components | Function components in TSX, hooks | `LitElement` classes, tagged-template `html` and `svg` | Our own `h()` helper and imperative DOM, components as functions returning nodes |
| Reactivity | `@preact/signals`: signals bound into JSX update the DOM without re-rendering the component | Reactive properties; asynchronous batched `update()`; template parts diff by value | `@preact/signals-core` effects writing to DOM nodes |
| Encapsulation | CSS Modules | Shadow DOM by default; light DOM by override | CSS Modules or prefixes |
| HMR | Prefresh keeps component state | No state-preserving reload [recalled] | Full page reload |
| Test idiom | Render a component, drive the DOM | Mount an element, drive the DOM | Mount a function, drive the DOM |

### 2.2 Criteria

| Criterion | (a) Preact | (b) Lit | (c) None |
|---|---|---|---|
| **Maintainability at content scale** (100 widgets and their presets, mostly agent-written, owner-reviewed) | Strong. TSX is type-checked through every prop and child; hooks and function components are the most common UI idiom in public code [inferred], so agents write them fluently; one obvious way to compose primitives into composites | Medium. Template bindings are strings the TypeScript compiler does not check without the separate lit-analyzer tooling [recalled]; class components with decorators or static `properties` add ceremony; composing primitives means nesting custom elements whose complex config passes as properties, not attributes | Weak. Every widget writes DOM creation and update by hand; a reviewer must check node bookkeeping in every file; the in-house renderer is a framework we would maintain, with no ecosystem |
| **Runtime fit: Artifact policy** | No `eval`, no `new Function` [measured]; bundles to own files on the web, loads from a CDN in the Artifact (revision 2) | Same [measured] | Same |
| **Runtime fit: size** | 8.5 KB gzipped for Preact, hooks and signals [measured] | 6.8 KB [measured] | 1.8 KB [measured] |
| **Runtime fit: drag frame time** | Equal to hand-written DOM when per-frame values are bound as signals (decision 2) [measured] | Slightly slower than both with large static arrays in a template, because each part diffs by value [measured] | The floor, but only as fast as (a) with discipline [measured] |
| **Learner-experience fidelity** (springs, show-why morphs, mascot, keyboard paths) | Equal: motion runs on signals and Web Animations outside rendering; refs give per-frame imperative writes where needed | Equal | Equal |
| **Ecosystem used here** | Prefresh HMR, `preact/compat` `memo`, hooks lint | Context, task and signals add-ons are separate packages | None needed, none available |
| **Interoperability** | MathLive and Bertie mount into refs | Native custom elements, the strongest point for a library shared with other frameworks, which we do not need | Same as (a) |

### 2.3 Measurements

Drag update, script plus forced layout per frame, milliseconds, Chromium at the stated CPU throttling, 1,200 frames per row [measured]:

| Variant | 4x median | 4x P95 | 6x median | 6x P95 |
|---|---|---|---|---|
| Base widget (64 static nodes), Preact 11 naive | 3.5 | 5.5 | 4.8 | 8.2 |
| Base widget, Preact 11 split | 3.3 | 5.0 | 5.4 | 10.4 |
| Base widget, Lit 3.3.3 | 2.7 | 4.3 | 4.4 | 7.7 |
| Base widget, no framework | 3.0 | 4.9 | 4.5 | 7.8 |
| Heavy widget (1,264 static nodes), Preact 11 naive | 5.2 | 9.4 | 8.2 | 14.8 |
| Heavy widget, Preact 11 split | 2.8 | 4.6 | 4.5 | 7.8 |
| Heavy widget, Lit 3.3.3 | 3.8 | 6.0 | 6.6 | 10.1 |
| Heavy widget, no framework | 2.8 | 4.7 | 4.5 | 7.6 |
| Heavy widget, Preact 10.29.8 naive | 8.2 | 10.7 | 9.3 | 16.2 |
| Heavy widget, Preact 10.29.8 split | 3.0 | 4.8 | 4.9 | 8.2 |

What the table says:

- For a typical widget the stack is invisible: the shared work (building a 200-point path string and laying out) dominates, and the four variants sit within about 1 ms of each other, which is inside run-to-run noise (naive and split Preact swap places between 4x and 6x).
- Static content inside a re-rendering component is the one thing that costs: 1.9 times on Preact 11 and 2.7 times on Preact 10 at 1,200 static nodes. Bound signals and a memoised static layer remove it entirely.
- Mount time for the heavy widget at 4x: 174 ms naive, 191 ms split, 164 ms Lit, 181 ms hand-written [measured, medians of 7]. DOM creation and layout dominate; the stack does not decide it. Dense layers therefore move to Canvas 2D by the catalogues' rules, whatever the stack.
- Gzipped size with the base widget included: 8.9 KB naive Preact, 10.4 KB split (it pulls `memo` from `preact/compat`), 6.7 KB Lit, 2.8 KB hand-written [measured]. KaTeX alone is 77 KB [measured], so the spread is immaterial.

### 2.4 Decision

**(a) TypeScript + Preact + @preact/signals + Vite.**

- **Why it wins.** Performance and fit do not separate the candidates, so the deciding criterion is the one that compounds over four years of content: how reliably agents write, and the owner reviews, about 100 widget views, 25 screens and the player. Typed TSX catches wrong props at compile time in the exact place agents make mistakes (configs, answer shapes, callback signatures). Function components with hooks are the idiom with the most public examples. Prefresh keeps state across edits, which matters when authoring a lesson against a live widget.
- **Why not (b) Lit.** Its strengths (native custom elements, encapsulation, framework-free consumers) solve problems we do not have. Shadow DOM would have to be turned off to let KaTeX's global stylesheet, our tokens and the grading and highlight styles reach inside widgets, at which point Lit is a template library whose bindings the type checker does not see. It also diffed large static arrays slower than disciplined Preact [measured].
- **Why not (c) no framework.** It measured no faster than disciplined Preact. Its cost is that every widget hand-writes node creation, keyed list updates, cleanup and event wiring: the machinery that produced most of the 23 defects in the 1,316-line Stage 1 lesson. Saving 7 KB is not worth re-owning that across 100 widgets.

### 2.5 Rules that make the choice hold

The benchmark shows Preact is only as fast as its use. These rules are enforced by lint (section 10.4) and by each widget's frame-time test (section 8):

1. **Per-frame values never pass through a component render.** A view derives what it draws with `useComputed` from the state signal and binds the computed signal directly (`<path d={d} />`, `<text>{label}</text>`). Reading `api.state.value` in a view's body is a lint error.
2. **Static layers are separate memoised components** (axes, grids, given data, labels), so a drag frame never diffs them.
3. **Layers above 1,500 marks, path bundles above 20 paths and heatmaps use `CanvasLayer`** (widgets-stage0 1.9, calc-linalg 2.10), which redraws on an animation frame when its signals change.
4. **KaTeX never renders in a drag loop.** Live numbers inside formulas patch text slots (`TexSlots`, section 5.11).
5. **Motion writes signals or Web Animations, not component state.** Springs, tweens and Bertie's rig update outside rendering.
6. **Lists that change during a gesture are keyed by stable element ids,** never by index.

---

## 3. Pinned toolchain and dependencies

Every version is pinned exactly (`save-exact=true` in `.npmrc`), and `package-lock.json` is committed. Licences are compatible with an MIT licence for the repository; MPL-2.0 (axe-core, Pyodide) and Apache-2.0 (TypeScript, Playwright, SQLite WebAssembly) are file-level or permissive and impose nothing on our code.

### 3.1 Runtime dependencies (shipped to learners)

| Package | Version | Licence | Role | Where it loads |
|---|---|---|---|---|
| `preact` | 11.0.0 | MIT | Components and rendering | Entry chunk |
| `@preact/signals` | 2.11.3 | MIT | Signals and their Preact bindings | Entry chunk |
| `@preact/signals-core` | 1.14.4 | MIT | Transitive runtime dependency of `@preact/signals` (it imports it by bare name), locked in `cdn.lock.json` and covered by the shipped-licence allow-list | Entry chunk on the web; from the CDN through the import map in the Artifact |
| `zod` (`zod/mini` entry) | 4.6.5 | MIT | Main-thread validation of tutor replies and route params | Entry chunk, about 6 KB, on the web; in the Artifact its whole closure from the CDN, 92 files (section 6.2.7 item 7) |
| `zod` (classic) | 4.6.5 | MIT | Bundle, import and event validation | Data worker only |
| `katex` | 0.19.0 | MIT | Maths typesetting (content-format decision 9 pins it) | Lazy `tex` chunk, preloaded at idle |
| `mathlive` | 0.111.0 | MIT | Maths keyboard for `expression-entry` | Lazy chunk, expression screens only |
| `@cortex-js/compute-engine` (`latex-syntax` entry) | 0.148.0 | MIT | LaTeX to MathJSON for expression grading (content-format decision 10) | Lazy chunk with `expression-entry` |
| `minisearch` | 7.2.0 | MIT | Search (content-format decision 14) | Lazy chunk, search screen |
| `ts-fsrs` | 5.4.2 | MIT | FSRS-6 scheduling (assessment decision 7) | Entry chunk and data worker |
| `fflate` | 0.8.3 | MIT | gzip for log packs, export files, result codes; inflate where `DecompressionStream` is missing | Data worker; Node tools |
| `idb` | 8.0.4 | ISC | Promise wrapper for IndexedDB | Entry chunk |
| `pyodide` | 314.0.7 | MPL-2.0 | Python 3.14.2 in a worker | Python worker, lazy |
| `hypothesis` (PyPI wheel, pure Python) | pinned at E8 with its SHA-256 | MPL-2.0 | Property-based drills (`needs: hypothesis`); not in Pyodide's distribution [measured], so `tools/pyvendor/fetch.ts` takes it from PyPI into the `testing` group | Python worker, lazy (web) |
| `@sqlite.org/sqlite-wasm` | 3.53.4-build2 | Apache-2.0 | SQL drills (programming decision 7) | SQL worker, lazy |
| `workbox-precaching`, `workbox-routing`, `workbox-strategies`, `workbox-expiration`, `workbox-window` | 7.4.1 | MIT | Web service worker and its registration | Web target only |

**Where they load, by target (revision 2).** The web build bundles every package above into its own chunks and workers. The Artifact publishes none of them: `preact`, `@preact/signals` (with `@preact/signals-core`), `zod`, `katex`, the Compute Engine `latex-syntax` entry, `minisearch`, `ts-fsrs`, `fflate` and `idb` load from the CDN URLs in `cdn.lock.json` (section 6.2.7); `mathlive`, `pyodide`, `hypothesis`, `@sqlite.org/sqlite-wasm` and the `workbox-*` packages are web only.

Fonts: Archivo, Besley and Source Code Pro (SIL Open Font Licence) through Google Fonts in the Artifact, as in the prototype; the same faces as committed `woff2` files on the web. KaTeX's 20 `woff2` files serve both KaTeX and MathLive on the web; the `woff` and `ttf` copies are not shipped. The Artifact ships no KaTeX font and renders maths as MathML (decision 37).

### 3.2 Build, test and authoring tools

| Package | Version | Licence | Role |
|---|---|---|---|
| Node.js | 22.22.0 (`.nvmrc`; `engines: >=22.12 <25`) | MIT | All tooling; Vite 8 requires `^20.19 \|\| >=22.12` [measured] |
| npm | 10.9.4 (bundled) | Artistic-2.0 | Workspaces and lockfile |
| `typescript` | 6.0.3 | Apache-2.0 | Type checking (decision 4) |
| `vite` | 8.3.3 | MIT | Dev server, builds (Rolldown 1.2 inside) |
| `@preact/preset-vite` | 2.10.6 | MIT | JSX transform, Prefresh HMR, hook names in development |
| `@babel/core` | 7.29.7 | MIT | Peer of the preset (it declares 7.x; 8.0.6 is latest) |
| `vite-plugin-pwa` | 2.0.0 | MIT | Web manifest and service worker build |
| `workbox-build` | 7.4.1 | MIT | Peer of `vite-plugin-pwa` 2.0.0 (`^7.4.1`) [measured: peer range]; builds the precache manifest |
| `@vite-pwa/assets-generator` | 2.0.0 | MIT | App icons from the logo SVG |
| `esbuild` | 0.28.2 | MIT | Content compiler and the per-topic generator modules (content-format 8.1); its metafile feeds `tools/release/provenance.ts` (6.2.7) |
| `tsx` | 4.23.15, **not installed** (stage 1, `docs/DECISIONS.md` B1) | MIT | Was: running TypeScript tools in Node. Node 22.22.0 strips types itself with no warning [measured], so tools and `eslint-plugin-zq` run as `node tools/x.ts` with erasable syntax and explicit `.ts` imports; added only if a tool needs JSX or path aliases |
| `vitest`, `@vitest/browser`, `@vitest/browser-playwright`, `@vitest/coverage-v8` | 5.0.3 | MIT | Unit and widget tests |
| `@playwright/test` | 1.63.0 | Apache-2.0 | End-to-end, visual, performance harness |
| `axe-core` | 4.14.0 | MPL-2.0 | Accessibility checks inside widget tests |
| `@axe-core/playwright` | 4.13.0 | MPL-2.0 | Accessibility checks end to end |
| `fast-check` | 4.10.2 | MIT | Property tests (fold, graders, mathcore, parsers) |
| `fake-indexeddb` | 6.2.5 | Apache-2.0 | IndexedDB in Node tests |
| `size-limit`, `@size-limit/file` | 14.1.0 | MIT | Bundle size gates |
| `eslint` | 10.12.0 | MIT | Lint |
| `@eslint/js` | 10.0.1 | MIT | Base rules |
| `typescript-eslint` | 8.71.1 | MIT | Type-aware rules |
| `eslint-plugin-react-hooks` | 7.1.1 | MIT | Hook rules (Preact hooks share the rules) |
| `prettier` | 3.9.9 | MIT | Formatting |
| `stylelint`, `stylelint-config-standard` | 17.16.0, 40.0.0 | MIT | CSS lint; colours only from tokens |
| `knip` | 6.39.0 | ISC | Unused files, exports and undeclared dependencies |
| `lefthook` | 2.1.17 | MIT | Pre-commit and pre-push hooks; advisory, since a missing binary skips them: CI is the binding gate (`docs/DECISIONS.md` B6) |
| gitleaks | 8.30.1, built by `go install` from the Go module proxy into `.zq/bin` (stage 1) | MIT | Secret scanning of staged changes and the full history, in CI and the hooks; Go's checksum database verifies the module (`docs/DECISIONS.md` section 5) |
| `@types/node` | 22.20.5 | MIT | Node types matching the runtime |
| `yaml` | 2.9.1 | ISC | Content parsing (content-format 2.3) |
| `wrangler`, `@anthropic-ai/sdk`, `@cloudflare/workers-types` | 4.147.0, 0.131.0, 5.20261006.1 | MIT or Apache-2.0 | Tutor proxy (`AI-TUTOR.md` 6.3) |
| Python via `uv` 0.8.17 | 3.12 (3.12.15 since stage 1, `tools/py/.python-version`; uv itself installed by wheel hash from `tools/py/uv-bootstrap.txt`) for CI drill runs and `zqverify`, with Pyodide's 3.14 beside it; `tools/py/uv.lock` pins NumPy 2.4.6, pandas 3.0.2, SciPy 1.18.0, statsmodels 0.14.6, scikit-learn 1.8.0, matplotlib 3.10.8, SymPy 1.14.0, pytest and hypothesis (resolves on 3.12 [measured]); stage 1 pinned pytest 9.0.2 (Pyodide's), hypothesis 6.168.5 and, in the `dev` group, pip-audit 2.10.1 | PSF | Learner floor (programming decision 16, raised from 3.11 by the `docs/PLAN.md` review), Pyodide parity, verifier |
| Playwright container | `mcr.microsoft.com/playwright:v1.63.0-noble`, index digest `sha256:eff16c30e6f3f4af0a03fa4b706120d5e9b0891c344a27d64559aff5900a4a27` [measured, MCR tag list and manifest, 7 October 2026] | Apache-2.0 | Visual baselines render in one pinned image |

### 3.3 Browser support

| Browser | Minimum | Why |
|---|---|---|
| Safari on iOS and macOS | 17.2 | CSS `linear()` easing for the spring approximations (design research 4.3) arrived in 17.2 [recalled]. The owner's phone, an iPhone 17 Pro Max, runs iOS 27.2 [sourced: the owner, from Settings, 7 October 2026]; its Claude app's user agent reports `iPhone OS 18_7` [measured: S1, 7 October 2026], a frozen value and the likely source of the earlier "iOS 18.7" [inferred], so nothing reads the OS version from the user agent [our choice] and the classic-script check below tests features |
| Chrome and Edge | 120 | Two years back on Android, the budget device class |
| Firefox | 121 | Same window |

Build target `es2022`. Older browsers get a static "This browser is too old for Zero to Quant" page from a classic script that tests for `structuredClone`, `Array.prototype.at` and CSS `linear()` before the module entry runs.

### 3.4 Upgrade policy

- A monthly dependency pull request, opened by a Claude session, upgrades within majors, runs the full nightly suite and records release notes read. No bot.
- Security advisories from `npm audit` and `pip-audit` are fixed within a week or waived in `docs/DECISIONS.md` with a reason.
- Majors (TypeScript 7, ESLint plugins, Pyodide) get their own pull request with the full suite and a note in `DECISIONS.md`.
- **Pyodide** moves only with the content pin: the pandas version decides some lessons (programming 0.2), so a Pyodide bump runs every drill, every recorded output and every lesson on views and copies.
- **Node 22** leaves maintenance in April 2027 [recalled]; the move to Node 24 is scheduled for March 2027.

---

## 4. Repository and module tree

### 4.1 Top level

```
zero-to-quant/                         [npm workspaces root]
├── package.json                       workspaces, scripts (section 10.1), engines, exact pins
├── package-lock.json                  committed
├── cdn.lock.json                      generated by tools/cdn: every third-party file the Artifact loads (section 6.2.7)
├── .nvmrc  .npmrc                     22.22.0; save-exact=true, engine-strict=true
├── tsconfig.base.json                 strict settings shared by every project (section 4.6)
├── vite.config.ts                     one config, three modes: web, artifact, dev (section 6.1)
├── vitest.config.ts                   projects: node, browser (section 8)
├── playwright.config.ts               projects: web, artifact, visual, perf (section 8)
├── eslint.config.js  .prettierrc  .stylelintrc.json  knip.json  lefthook.yml  .size-limit.json
├── .env.example                       VITE_ZQ_TUTOR_URL, VITE_ZQ_WEB_APP_URL (no secrets)
├── .gitignore                         node_modules, dist, .zq/cache, .env, py-vendor, test-results
├── LICENSE                            MIT
├── CLAUDE.md  STATE.md                Phase 2 protocol and stage tracker (project-forge)
├── .github/workflows/
│   ├── ci.yml                         pull-request gates (section 8.3)
│   ├── nightly.yml                    full visual, cross-browser, full verify, performance, audits
│   ├── pages.yml                      web build and deploy to the web host on a release tag (`docs/PLAN.md` 12 decision 13)
│   └── proxy.yml                      manual Worker deploy with wrangler (AI-TUTOR.md 6.3.7)
├── content/                           lessons and libraries [YAML]  (CONTENT-FORMAT.md 2.5)
├── docs/
│   ├── PLAN.md  DECISIONS.md
│   ├── blueprint/work/                these working papers
│   └── engine/
│       ├── WIDGET-AUTHORING.md        the agent-facing widget authoring guide (section 10.5)
│       └── RELEASE.md                 the Artifact release checklist (section 6.2.6)
│   (this paper is docs/ARCHITECTURE.md, an appendix of docs/PLAN.md, kept current after Phase 1)
├── packages/                          shared libraries [TypeScript]  (section 4.3)
├── src/                               the app, both targets [TypeScript, TSX, CSS]  (section 4.2)
├── proxy/                             tutor proxy [TypeScript]  (AI-TUTOR.md 11.1)
├── tools/                             build, release and test tools (section 4.4)
├── tests/                             end-to-end, visual, performance, fixtures (section 8)
├── prototype/  spikes/                Stage 1 mockups and platform spikes; read-only references
└── dist/                              build output (ignored): web/, artifact/, preview/
```

### 4.2 `src/`, the app

```
src/                                   [TypeScript, TSX, CSS Modules]
├── entries/
│   ├── web.tsx                        boot with WebPlatform; registers the service worker
│   ├── artifact.tsx                   boot with ArtifactPlatform; capability discovery
│   └── dev.tsx                        dev and preview builds: either platform plus dev routes
├── app/
│   ├── boot.ts                        start-up sequence (section 5.10.1); one place for ordering
│   ├── router.ts                      hash router: parse, match, guards, focus and title on navigate
│   ├── routes.ts                      the route table (section 5.8); lazy screen imports
│   ├── config.ts                      typed build-time config and feature flags (section 11.4)
│   ├── log.ts                         ring-buffer logger, redaction, Copy diagnostics
│   ├── copy.ts                        shell copy (en-GB); linted like content
│   ├── shell/                         Shell, NavBar (bottom at < 768 px, rail above), TopBar,
│   │                                  ToastHost, SheetHost, ModalHost, ErrorBoundary, UpdateBanner
│   └── stores/                        signals per domain: settings, progress (derived), content,
│                                      session, tutor, connectivity, writer (tab election)
├── platform/                          the only target-specific code (section 5.9)
│   ├── types.ts                       re-exports @zq/contracts platform interfaces
│   ├── shared/                        idb.ts, kv.ts, blob-cache.ts, clock.ts, random.ts,
│   │                                  feedback.ts (Web Audio, vibrate), lifecycle.ts (visibility,
│   │                                  online, Web Locks), memory-store.ts, handoff.ts
│   ├── web/                           index.ts, idb-store.ts (ProgressStore), files.ts (Blob link),
│   │                                  sw-client.ts (updates, offline courses), identity.ts
│   ├── artifact/                      index.ts, capabilities.ts (claude.use, absence),
│   │                                  db-store.ts (ProgressStore on db), downloads.ts, identity.ts,
│   │                                  cdn.ts (awaits the CDN modules at boot, failure codes, Retry),
│   │                                  python-handoff.ts and sql-handoff.ts (the runtime stubs)
│   └── fake/                          FakePlatform for tests, gallery and storyboards: scripted
│                                      tutor, MemoryStore, FakeClock, fixed seeds
├── engine/
│   ├── scope.ts                       Scope: timers, frames, listeners, aborts (section 5.1)
│   ├── rpc.ts                         typed worker RPC with transferables and cancellation
│   ├── content/                       manifest.ts, loader.ts, bundle-cache.ts, prose.tsx (token
│   │                                  lists), templates.ts, gen-runtime.ts, hmr.ts (dev only)
│   ├── widgets/                       registry.ts, host.tsx (WidgetHost), api.ts (WidgetApi and
│   │                                  hooks), overlay.tsx (marks, badges, highlights, annotations,
│   │                                  ghosts), showwhy.ts, guard.ts (preview guard), describe.ts
│   │                                  (screen description for the tutor), persist.ts (drafts,
│   │                                  migrations), presets.ts
│   ├── interaction/                   drag.ts (pointer capture, frame coalescing), taptap.ts,
│   │                                  roving.ts, keymap.ts, exact-editor.tsx (E key), hit.ts
│   ├── motion/                        spring.ts, tween.ts, easing.ts, presets.ts (tokens),
│   │                                  mode.ts (full, reduced, test), waapi.ts, celebrate.ts
│   ├── render/                        Svg.tsx, Layer.tsx (memoised static layer), CanvasLayer.tsx,
│   │                                  Tex.tsx, TexSlots.tsx, scales.ts, tokens.ts (read CSS
│   │                                  variables for canvas), table-view.tsx
│   ├── a11y/                          announcer.ts (one polite region), focus.ts, describe-sheet.tsx
│   ├── player/                        machine.ts (pure reducer), effects.ts (runner), policy.ts
│   │                                  (item modes), LessonPlayer.tsx, ScreenFrame.tsx, TopBar.tsx,
│   │                                  ButtonRow.tsx, VerdictBubble.tsx, HintSheet.tsx, WhySheet.tsx,
│   │                                  SolutionReveal.tsx, Quiz.tsx, Complete.tsx, transitions.ts
│   ├── items/                         ItemRunner.tsx (quiz, practice, review, redo, homework,
│   │                                  exam, placement through policy.ts), dots.tsx
│   ├── progress/                      events.ts (envelope, kinds), append.ts (queue, writer lock),
│   │                                  fold/ (assessment rules), snapshot.ts, outbox.ts, lease.ts,
│   │                                  export.ts, import.ts, result-code.ts, time.ts (active time,
│   │                                  study day)
│   ├── schedule/                      fsrs.ts, redo.ts, composer.ts      (ASSESSMENT.md 5, 6)
│   ├── assess/                        homework.ts, exam/, placement.ts   (ASSESSMENT.md 2, 3, 7)
│   ├── python/                        client.ts (PythonRuntime, web), budget.ts (packages per course)
│   ├── sql/                           client.ts (SqlRuntime, web)
│   └── cas/                           expression.ts (lazy Compute Engine parser), mathfield.ts
│                                      (lazy MathLive, fonts and sounds configured; web only)
├── workers/
│   ├── data.worker.ts                 bundle validation, fold rebuilds, search, export, import
│   ├── python.worker.ts               Pyodide, the native loader, the grader (section 6.3); web only
│   ├── python/                        loader-native.ts, grader.py, zqtest.py (content-format 3.9), trace.py
│   └── sql.worker.ts                  SQLite WebAssembly; web only
├── widgets/                           the library (section 5.3)
│   ├── registry.gen.ts                generated: type@v -> cluster loader (CI checks it is current)
│   ├── registry.node.gen.ts           generated: logic, schema and preset modules only, for tools/zq (decision 33)
│   ├── clusters/<cluster>.ts          generated: one entry per cluster, the lazy chunk boundary;
│   │                                  imports logic and View (a scene's scene.ts with SceneView) and
│   │                                  preset runtime parts, never schema.ts
│   ├── primitives/<type>/             logic.ts, schema.ts, View.tsx, view.module.css,
│   │                                  fixtures.ts, logic.test.ts, view.browser.test.ts,
│   │                                  states/v<n>.json (one per past stateVersion)
│   ├── inputs/<type>/                 same shape
│   ├── scene/                         the scene layer (section 5.14): define.ts (SceneDef -> WidgetModule),
│   │                                  bind.ts (typed paths), SceneView.tsx, layout.tsx (row, column, stack,
│   │                                  grid, overlay, embed), nodes.ts (primitive name -> controlled component)
│   ├── scenes/<cluster>/<type>/       scene.ts (pure: data and functions), schema.ts, fixtures.ts,
│   │                                  scene.test.ts, states/v<n>.json; no View.tsx, no CSS
│   ├── composites/<cluster>/<type>/   bespoke composites only; same shape as primitives
│   └── presets/<cluster>/<type>.ts    preset: base widget, config transform, predicates, recipes
├── screens/                           one folder per screen: View.tsx, load.ts, copy.ts, *.module.css
│   ├── today/ learn/ course/ lesson/ review/ practice/ redo/ homework/ exam/ drill/ daily/
│   ├── weekly/ notebook/ search/ plan/ log/ you/ settings/ onboarding/ import/
│   └── dev/                           preview/ storyboard/ specimen/ gallery/ tutor/ system/
├── tutor/                             Bertie's brain, unchanged from AI-TUTOR.md 11.1
├── ui/                                design system: Button (lipped), OptionCard, Sheet, Modal,
│   │                                  Toast, ProgressBar, Dots, Chip, VerdictChip, Tangram, Icon,
│   │                                  StatBadge, Tabs, Switch, TextField, Keypad, SymbolBar, Table,
│   │                                  art.ts (course art drawn in code, from prototype/js/art.js)
│   └── bertie/                        geometry.ts, poses.ts, markup.ts (DOMParser), bertie.ts, bertie.css, Bertie.tsx
├── sw/
│   └── sw.ts                          web service worker (Workbox), web build only
├── styles/                            tokens.css (from prototype/css/tokens.css), base.css,
│                                      katex.css (KaTeX's, with font URLs rewritten; web only),
│                                      math.css (ours: MathML layout and the maths font stack; Artifact),
│                                      fonts-web.css, fonts-artifact.css
└── assets/fonts/                      Archivo, Besley, Source Code Pro woff2 (OFL), web only
```

### 4.3 `packages/`

```
packages/                              [TypeScript, no DOM unless stated]
├── contracts/      @zq/contracts      types: ids, Answer, Grade, ShowStep, widget contract,
│                                      platform interfaces, events, RPC messages (section 5); one
│                                      constants module: KaTeX's reserved colours and the
│                                      term-sentinel mapping, for engine/render and zq check (B27, B33)
├── mathcore/       @zq/mathcore       pure maths shared by widgets, graders and generators:
│                                      rng (Philox4x32-10), rational (BigInt), num-parse, expr
│                                      (calc-linalg 2.3 grammar, no eval), dmath (deterministic exp,
│                                      log, log1p, expm1, tanh, pow, sin, cos), sample, quad, ode,
│                                      roots, linalg, stats, units
├── content-schema/ @zq/content-schema zod schemas and inferred types        (content-format 3.2)
├── content-compiler/ @zq/compiler     compile(project, { registry: CompilerRegistry }); the CLI
│                                      entry is tools/zq (decision 33)        (content-format 8)
├── graders/        @zq/graders        pure graders and the predicate registry interface
│                                      (content-format 7); leak.ts, the candidate-answer extractor
│                                      shared by the compiler's tutor-field lint and the tutor's leak
│                                      probe; imports @zq/mathcore only
├── gen-kit/        @zq/gen            defineGenerator, phrases, exact values  (content-format 5)
├── models/         @zq/models         pure domain models shared by widgets, workers, generators and CI: algo, code,
│                                      data, git, analysis, markets, ml, numerics, optim, research
│                                      (docs/WIDGETS.md 3); one entry point per domain
└── eslint-plugin-zq/                  the custom lint rules (section 10.4)
```

`@zq/graders`, `@zq/mathcore` and every widget's `logic.ts` and `schema.ts` run unchanged in Node (compiler, CI replay) and in the browser. A CI test imports all of them in plain Node with no DOM globals defined. The numeric services of `@zq/mathcore` (`linalg`, `quad`, `ode`, `roots`, `units`, `sample`, `stats`) and the `@zq/models` domains `data`, `code`, `algo`, `git` and `analysis` are built in `docs/PLAN.md` stages 3a to 3g, each with Python or `git` parity against the versions in `tools/py/uv.lock`, before the widget batches that use them; `markets`, `ml`, `numerics`, `optim` and `research` are built with their P1 and P2 waves.

### 4.4 `tools/` and `tests/`

```
tools/
├── zq/                                the zq CLI: builds CompilerRegistry from registry.node.gen.ts
│                                      and calls @zq/compiler (decision 33)
├── zqverify/                          independent Python verifier             (content-format 6)
├── pyvendor/                          the web build's Pyodide files (section 6.3.2)
│   └── fetch.ts                       downloads the pinned release wheels, checks pyodide-lock SHA-256;
│                                      the hypothesis wheel from PyPI, checked against our pinned SHA-256
├── cdn/                               the Artifact's third-party modules (section 6.2.7)
│   ├── lock.ts                        writes cdn.lock.json from package-lock.json: URL, SHA-384, import kind,
│   │                                  bare imports of each file; prefers cdnjs where its file is identical
│   └── drift.ts                       nightly: fetches every locked URL and fails on any byte difference
├── release/
│   ├── artifact-plan.ts               publish batches, garbage collection, budgets (section 6.2.6)
│   ├── page.ts                        rewrites Vite's index.html into the Artifact page fragment, with the import map
│   ├── provenance.ts                  fails the Artifact build if a node_modules module or a binary would be published
│   └── budgets.ts                     file counts and sizes per target; fails the build
├── artifact-host/                     local emulator of the Artifact host (section 8.2)
│   ├── server.ts                      file-type allow-list, CSP header, no service worker
│   └── fake-claude.ts                 window.claude with sample, db (rules), user, downloads
├── perf/                              frame-time harness (CDP throttling) and startup traces
├── scaffold/                          npm run new:widget, new:screen
└── registry/                          generates src/widgets/registry.gen.ts and clusters/*.ts
tests/
├── e2e/                               Playwright specs, run against both targets
├── visual/                            screenshot specs; baselines in __screenshots__/
├── perf/                              per-widget drag specs, startup, fold rebuild
├── fixtures/learners/                 learner logs of the last six releases (content-format 4.5)
├── fixtures/events/                   one file per event version, for upgrade tests
└── synthetic/                         the four-year synthetic learner generator (assessment A1)
```

### 4.5 Layering: who may import whom

Enforced by `zq/layering`, which encodes this table in `eslint.config.js` (stage 1; it replaces draft 1's `no-restricted-imports` per directory, whose flat-config entries replace each other per file), and by `knip`. A higher row may import any row below it; nothing imports upwards.

| Layer | May import | Must not import |
|---|---|---|
| `entries/` | everything | |
| `app/`, `screens/` | `engine/`, `widgets/registry`, `tutor/`, `ui/`, `platform/types`, packages | another screen's internals |
| `tutor/` | `engine/` (player state, widget describe), `ui/`, packages | `screens/`, `platform/*` implementations |
| `engine/` | `ui/`, packages, `platform/types` | `screens/`, `tutor/` (the player receives `TutorService` by injection), `platform/web`, `platform/artifact` |
| `widgets/` | `engine/widgets/api`, `engine/interaction`, `engine/render`, `engine/motion`, `ui/`, `@zq/mathcore`, `@zq/models`, `@zq/contracts` | `platform/`, `app/`, `tutor/`, `engine/player`, `engine/progress`, `zod` (classic) |
| `widgets/**/logic.ts`, `widgets/scenes/**/scene.ts` | `@zq/mathcore`, `@zq/models`, `@zq/contracts`, its own folder; a scene also `widgets/scene/define.ts` and the primitives' `logic.ts` | anything with DOM, Preact, CSS |
| `widgets/scene/` (`SceneView`, `nodes.ts`) | primitives' and inputs' controlled components, the engine layers `widgets/` may import | composites' internals other than their exported controlled component |
| `ui/` | `engine/motion`, `@zq/contracts` | `engine/` otherwise |
| `platform/web`, `platform/artifact` | `platform/shared`, packages | `engine/` beyond types |
| `packages/*` | each other per their manifests | `src/` (the compiler receives widgets through `CompilerRegistry`) |
| `tools/zq` | `packages/*`, `src/widgets/registry.node.gen.ts` and the `logic.ts`, `schema.ts` and preset files it lists | any other part of `src/`, every `View.tsx` and CSS file |
| `workers/` | `engine/progress/fold`, `engine/rpc`, packages | `ui/`, `widgets/` views, `widgets/**/schema.ts` |
| anything bundled for the main thread | | `widgets/**/schema.ts` (classic zod, about 92 KB gzipped); `size-limit` on the entry and every cluster chunk catches a leak |

### 4.6 TypeScript configuration

`tsconfig.base.json`: `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `verbatimModuleSyntax`, `isolatedModules`, `moduleResolution: "bundler"`, `module: "esnext"`, `target: "es2022"`, `skipLibCheck: false` for our packages. Project references: `src` (DOM libs), `src/workers` (WebWorker lib), `src/sw` (WebWorker and Workbox types), each `packages/*`, `tools` (Node types), `proxy` (Workers types). Path aliases: `@/` for `src/`, `@zq/*` for packages; the same aliases in Vite and Vitest.

**Stage 1 additions** (`docs/DECISIONS.md` B1): `erasableSyntaxOnly` and `allowImportingTsExtensions` in the base; `tools`, `tests` and every `packages/*` project extend `tsconfig.node.base.json` (`module` and `moduleResolution` `nodenext`, `.ts` extensions required), because Node runs them directly; `src` keeps `bundler` resolution, which Vite runs. Every project is `composite` with `emitDeclarationOnly` into the ignored `.zq/tsc/`. `jsx: "react-jsx"` and `jsxImportSource: "preact"` are added with Preact's installation (stage 3 or 4), because knip reports an unlisted `preact` before then.

### 4.7 Threads and shared state

| Thread | Owns | Talks through |
|---|---|---|
| Main | Rendering, signals stores, widget state, the player, grading (non-code), the single-event fold, the append queue | `rpc.ts` to workers; `ProgressStore` |
| Data worker (one) | Bundle validation (classic zod), full fold rebuilds and late-event re-folds, search queries, export packing, import validation and unpacking (fflate); in the Artifact its libraries come from the CDN by full URL (section 6.2.7) | Messages; transfers `ArrayBuffer`s |
| Python worker (web, at most one) | Pyodide, packages, test runs | Messages; terminated on timeout and restarted |
| SQL worker (web, at most one) | SQLite | Messages |
| Service worker (web only) | Caches | `workbox-window` messages |

**Shared mutable state.** None crosses a thread: workers receive copies or transferred buffers and return results. On the main thread:

- Widget state lives in one signal per widget instance, written only by its `WidgetApi` (`change`, `commit`) and by the host (`reset`, `reveal`, show-why on `v` only).
- Progress events go through one `AppendQueue`: a promise chain that assigns `seq`, applies the single-event fold, then persists. Ordering is the queue's order; nothing else assigns `seq`.
- Only the **writer tab** appends. `lifecycle.ts` takes the Web Lock `zq-writer` with `{ ifAvailable: true }`; a tab without it renders read-only with a banner and a "Use here" button that requests the lock with `steal: true`. Where Web Locks is missing, the tab falls back to a `localStorage` heartbeat lease of 10 seconds [our choice]. Web Locks works inside the Artifact frame: `ifAvailable` gets `null` while the lock is held, and `steal: true` takes a held lock, the holder's request rejecting with `AbortError`, also when a dedicated worker holds it [measured: S1, 7 October 2026].
- A late event arriving from another device or an import triggers a re-fold in the data worker; the main thread swaps the derived state signal in one assignment when the worker replies (assessment 13.3).

---

## 5. Contracts

Every type in this section lives in `packages/contracts` (`@zq/contracts`), except where a path says otherwise. Types that another paper owns are referenced, not repeated: `TutorRequest`, `TutorBackend` and the action schemas (`AI-TUTOR.md` 4.1, 5.3, 6.1), the event kinds and `ProgressStore` (`ASSESSMENT.md` 13.2, 13.5), the content schemas and `Grade` (`CONTENT-FORMAT.md` 3.2, 7.1).

### 5.1 Shared primitives

```ts
// @zq/contracts/src/base.ts
export type Json = null | boolean | number | string | Json[] | { [key: string]: Json };
export type ContentId = string;   // 'lsn.cond.shrinking-sample-space' (content-format 4.1)
export type LocalId = string;     // 'shade', 'grid', 'd': unique inside its parent
export type ElementId = string;   // 'cell:5,3'; on a screen with several widgets the host prefixes the widget id: 'grid/cell:5,3'
export type Mark = 'correct' | 'not-yet' | 'kept' | 'reveal';        // grading styles (widgets-stage0 1.5)
export type HighlightStyle = 'ring' | 'wash' | 'flash';               // tutor and hint "Point" styles

/** Compiled ZQ Markdown (content-format 2.4). The compiler emits it; the engine's Prose renderer is its only reader. */
export type Token =
  | ['t', string]                                // text
  | ['b' | 'i', Token[]]                         // bold, italic
  | ['c', string]                                // inline code
  | ['m' | 'M', string]                          // inline and display maths (KaTeX source)
  | ['l', ContentId, Token[]]                    // link to a glossary term, lesson, card or item
  | ['v', string]                                // template value path (content-format 3.6)
  | ['if', string, Token[], Token[]]             // one level of condition
  | ['p']                                        // paragraph break
  | ['ul', Token[][]];                           // list (summary ideas, solution steps, model answers)
export type TokenList = Token[];

/** Owns every timer, frame callback, listener, effect and abort in one screen or widget. */
export interface Scope {
  readonly signal: AbortSignal;                                         // aborts on dispose
  readonly disposed: boolean;
  later(fn: () => void, ms: number): () => void;                        // returns a cancel function
  every(fn: () => void, ms: number): () => void;
  frame(fn: (t: number) => void): () => void;                           // one animation frame
  loop(fn: (t: number, dt: number) => boolean): () => void;             // runs each frame while fn returns true
  listen(target: EventTarget, type: string, fn: (e: Event) => void, opts?: AddEventListenerOptions): void;
  effect(fn: () => void | (() => void)): void;                          // a signals effect disposed with the scope
  own(dispose: () => void): void;                                       // anything else (observers, workers)
  child(): Scope;                                                       // disposed with its parent
  dispose(): void;                                                      // idempotent
}

/** Counter-based Philox4x32-10 (@zq/mathcore/rng). Draw k of stream s is a pure function of (seed, s, k). */
export interface Rng {
  next(): number;                       // uniform on [0, 1) with 53 random bits; advances the counter
  at(index: number): number;            // the draw at an index, without advancing
  int(lo: number, hi: number): number;  // inclusive, unbiased by rejection on 32-bit words
  normal(): number;                     // Box-Muller from two draws
  fork(stream: string): Rng;            // an independent stream
}
export interface SeedSource { readonly seed: number; rng(stream: string): Rng }
```

**Seeds.** A lesson screen's seed is `hash32(lessonId, screenId)`, so every learner sees the same canvas and the storyboard matches what learners see; a widget config may override it (`seed`). An item instance's seed comes from its generator draw (`{ gen, v, level, seed }`, content-format 4.3). The one hash every paper uses lives in `@zq/mathcore` [our choice]:

```ts
/** 32-bit FNV-1a over the UTF-8 bytes of the parts joined by U+001F; numbers as their shortest round-trip decimal (`String(n)`), integers only.
 *  content-format's hash32(gen.id, seed), assessment's hash32(attemptId, slotIndex, k) and the screen seed above are all this function. */
export function hash32(...parts: (string | number)[]): number;   // unsigned, 0 to 2^32 - 1
```

A non-integer number part is a development error (it throws), so no part's decimal form can differ between engines. Known-answer vectors in E1 fix the bytes.

### 5.2 Answers, grades and show-why

```ts
// @zq/contracts/src/answer.ts. Widgets produce answers; graders (content-format 7) read them. Widgets never parse or grade.
export type Answer =
  | { type: 'choice'; ids: LocalId[] }
  | { type: 'numeric'; raw: string }                                   // as typed; @zq/graders normalises and parses (content-format 7.2)
  | { type: 'expression'; latex: string }
  | { type: 'set'; ids: ElementId[] }
  | { type: 'interval'; raw: string }                                  // '[3.35, 3.45)'; unions with 'U'
  | { type: 'ordering'; ids: LocalId[] }
  | { type: 'mapping'; pairs: [LocalId, LocalId][] }
  | { type: 'point'; pts: { id: ElementId; x: number; y: number; z?: number }[] }
  | { type: 'curve'; samples: [number, number][] }                     // at most 400 samples
  | { type: 'matrix'; entries: string[][] }                            // exact strings, parsed by graders
  | { type: 'distribution'; support: (number | string)[]; masses: string[] }
  | { type: 'state' }                                                  // graded by a predicate on the widget's own state
  | { type: 'output'; text: string }
  | { type: 'resultset'; columns: string[]; rows: Json[][] }
  | { type: 'code'; files: Record<string, string>; entry: string }
  | { type: 'long-form'; text: string }
  | { type: 'parts'; parts: Record<LocalId, Answer> };
export type AnswerType = Answer['type'];

/** Supplied by the engine to @zq/graders for one grading call. */
export interface GradeCtx {
  predicate(name: string, args: Record<string, Json>): boolean;       // bound to the answering widget's config and state
  cas(): Promise<CasService>;                                          // lazy LaTeX to MathJSON (content-format decision 10)
  seed: number;                                                        // for probing points in expression checks
  locale: 'en-GB';
}

/** What a widget recipe expands into: data the engine animates. Richer than authored ShowStep, still declarative. */
export type MotionStep =
  | { k: 'set'; widget: LocalId; values: Record<string, number | string>; ms: number;
      ease: 'morph' | 'standard' | 'spring-snap' | 'spring-physical' }  // view state only (section 5.3)
  | { k: 'highlight'; ids: ElementId[]; style: HighlightStyle; times?: number; gapMs?: number }
  | { k: 'annotate'; at: ElementId; text: string }                     // at most 80 characters
  | { k: 'wait'; ms: number }
  | { k: 'together'; steps: MotionStep[] };
```

`Grade` is `CONTENT-FORMAT.md` 7.1's type with one amendment: `answerObjects` is filled by the host from `WidgetLogic.answerObjects`, and graders leave it empty, because only the widget knows its element ids. Authored `ShowStep`s (content-format 3.2) compile to `MotionStep`s in the host: a declarative step becomes `set`, `highlight` and `annotate` steps run together; a widget recipe step calls the widget's `recipes[name]`.

### 5.3 The widget contract

A widget is a folder with five source files, two test files and a `states/` folder: `logic.ts` (pure, Node-safe), `schema.ts` (classic zod, build time only: the config schema and the recipe argument schemas), `View.tsx` (Preact), `view.module.css`, `fixtures.ts` (configs and scripted interactions shared by tests, the gallery and the storyboard, typed below), `logic.test.ts`, `view.browser.test.ts`, and `states/v<n>.json` for every past `stateVersion`. The engine's `WidgetHost` turns logic and view into a running instance.

```ts
// @zq/contracts/src/widget.ts
export type WidgetTier = 'primitive' | 'input' | 'scene' | 'composite' | 'preset';   // 'scene': section 5.14
export type ClusterId =
  | 'core' | 'number' | 'algebra' | 'geometry' | 'precalc' | 'computing'
  | 'calculus' | 'linalg' | 'stochastic' | 'probability' | 'statistics' | 'timeseries'
  | 'python' | 'data' | 'tools' | 'algorithms' | 'cpp'
  | 'finance' | 'projects' | 'interview' | 'ml' | 'research';            // 22 lazy chunks
export type WidgetMode = 'lesson' | 'explore' | 'demonstrate' | 'quiz' | 'practice' | 'review'
                       | 'homework' | 'exam' | 'placement' | 'readonly';
export type MotionMode = 'full' | 'reduced' | 'test';                  // 'test': every animation lands at once

/** Fields every widget config has (content-format WidgetUse); the rest is the widget's own schema. */
export interface BaseConfig { id: LocalId; type: string; v: number; label: string; preset?: `${string}@${number}`; seed?: number }   // preset: the compiler records which preset produced this config, pinned, e.g. 'two-dice@1'

/** a: answer state, graded, saved and restored. v: view state (zoom, step, time cursor), which show-why may tween. Both JSON. */
export interface WidgetState<A extends Json, V extends Json> { a: A; v: V }

export interface Target {
  id: ElementId; label: string;
  role: 'handle' | 'cell' | 'region' | 'token' | 'slot' | 'option' | 'mark' | 'control' | 'line' | 'node' | 'edge' | 'term' | 'readout' | 'test';
}
export interface Tryable { control: ElementId; label: string; range?: [number, number]; step?: number; options?: string[] }
export interface TableView { caption: string; columns: string[]; rows: (string | number)[][] }
export type Predicate<C, A extends Json, V extends Json> = (config: C, s: WidgetState<A, V>, args: Record<string, Json>) => boolean;

/** Pure and Node-safe: no DOM, no Preact, no CSS, no clock, no Math.random. Imported by the app, the compiler and CI. */
export interface WidgetLogic<C extends BaseConfig, A extends Json, V extends Json> {
  readonly type: string;                                   // kebab-case, unique
  readonly v: number;                                      // major version; content pins it (content-format 3.5)
  readonly tier: Exclude<WidgetTier, 'preset'>;
  readonly cluster: ClusterId;
  readonly answers: readonly AnswerType[];                 // [] for display-only widgets
  readonly stateVersion: number;                           // bump when the saved shape of a or v changes
  readonly tweenable?: readonly (keyof V & string)[];      // view fields show-why may tween
  readonly needs?: readonly ('python' | 'sql' | 'cas' | 'mathfield')[];   // services the host must inject

  // State
  init(config: C, seed: SeedSource): WidgetState<A, V>;
  migrate?(saved: Json, fromVersion: number, config: C): WidgetState<A, V> | null;   // null: discard the draft
  answer(config: C, s: WidgetState<A, V>): Answer | null;                              // null keeps Check disabled
  dirty(config: C, s: WidgetState<A, V>): boolean;                                     // enables Start over
  solved?(config: C, s: WidgetState<A, V>, key: Json): WidgetState<A, V>;             // Show solution; key: the check's canonical answer
  summarise(config: C, before: WidgetState<A, V>, after: WidgetState<A, V>): string;   // action-log sentence, at most 120 characters

  // Grading support
  answerObjects(config: C, s: WidgetState<A, V>): ElementId[];                         // the only elements grading may recolour
  marks?(config: C, s: WidgetState<A, V>, grade: Grade): Record<ElementId, Mark>;     // default: every answer object takes the verdict
  predicates?: Record<string, Predicate<C, A, V>>;                                     // named state tests a `predicate` check may call

  // Build time (the compiler calls these through CompilerRegistry; content-format 6.7, 8.1, 12.1)
  staticTargets(config: C): Target[];                                                  // every element content may reference in hints and show-why, with label and role, no DOM
  exports?: Record<string, (config: C, s: WidgetState<A, V>) => string | number>;      // template values (content-format 3.6); the keys are the paths the compiler checks
  elementMeta?(config: C, id: ElementId): Record<string, string | number> | null;      // per-element template metadata for set answers ('label', 'sum'; content-format 12.1)
  resolvers?: Record<string, (config: C, query: Json) => string[]>;                    // `{ where }` sets to explicit ids

  // Show-why
  recipes?: Record<string, (config: C, s: WidgetState<A, V>, args: Record<string, Json>) => MotionStep[]>;

  // Text, tables and the tutor (ai-tutor 5.5)
  describe(config: C, s: WidgetState<A, V>, level: 'brief' | 'full'): string;         // learner-visible facts only; brief at most 300 characters, full at most 2 KB
  targets(config: C, s: WidgetState<A, V>): Target[];                                  // at most 40
  table?(config: C, s: WidgetState<A, V>): TableView | null;                           // every chart's Table view
  secret?(config: C, s: WidgetState<A, V>): string | null;                             // hidden truths, sent only in the sealed answer block
  tryable?(config: C, s: WidgetState<A, V>): Tryable[];                                // never an answer object
  tryValue?(config: C, s: WidgetState<A, V>, control: ElementId, value: number | string): WidgetState<A, V> | null;
  code?(config: C, s: WidgetState<A, V>): { files: { name: string; numbered: string }[] } | null;   // programming 2.8
}

export interface WidgetViewProps<C extends BaseConfig, A extends Json, V extends Json> { config: C; api: WidgetApi<A, V> }
export type WidgetView<C extends BaseConfig, A extends Json, V extends Json> = (props: WidgetViewProps<C, A, V>) => VNode | null;
export interface WidgetModule<C extends BaseConfig, A extends Json, V extends Json> { logic: WidgetLogic<C, A, V>; View: WidgetView<C, A, V> }

/** A preset: configuration over a base widget, expanded by the compiler. No view, no state of its own. */
export interface PresetDef<P extends BaseConfig, C extends BaseConfig> {
  type: string; v: number; cluster: ClusterId;
  base: { type: string; v: number };
  expand(config: P): Omit<C, 'id' | 'label'>;               // pure; the result is validated by the base widget's schema
  predicates?: Record<string, Predicate<C, Json, Json>>;     // registered as '<preset type>/<name>'
  recipes?: Record<string, (config: C, s: WidgetState<Json, Json>, args: Record<string, Json>) => MotionStep[]>;
  describeAs?: string;                                       // replaces the base widget's name in describe()
}

/** What `schema.ts` exports. Classic zod; imported only by registry.node.gen.ts (the compiler and CI), never by a cluster chunk. */
export interface WidgetSchemaModule {
  config: ZodType;                                           // the widget-specific config fields at this major
  recipeArgs: Record<string, ZodType>;                       // one schema per recipe name; the compiler validates every authored recipe call
}

/** Handed to @zq/compiler by tools/zq (decision 33). No views, no CSS, no DOM. */
export interface CompilerRegistry {
  widget(type: string, v: number): { logic: WidgetLogic<BaseConfig, Json, Json>; schema: WidgetSchemaModule } | undefined;
  preset(type: string, v: number): PresetDef<BaseConfig, BaseConfig> | undefined;
  all(): readonly { type: string; v: number; tier: WidgetTier; cluster: ClusterId }[];   // for registry freshness and the compiler's "unknown type@v" error
}

/** fixtures.ts default-exports WidgetFixture[]. The contract suite, the browser tests, the gallery and the storyboard all read this one shape. */
export interface WidgetFixture<C extends BaseConfig, A extends Json, V extends Json> {
  name: string;                                              // kebab-case; the gallery URL segment
  config: C;
  seed?: number;
  states?: Record<string, WidgetState<A, V>>;               // named states for screenshots ('engaged', 'solved')
  paths?: {                                                  // every interactive fixture has all three, and all three reach `expect`
    pointer: FixtureStep[]; keyboard: FixtureStep[]; tapTap: FixtureStep[];
  };
  expect?: { answer?: Answer | null; predicates?: Record<string, boolean> };
  sealed?: Json;                                             // the check's canonical answer, for the leak tests of section 8.1.1
}
export type FixtureStep =
  | { do: 'drag'; id: ElementId; to: { x: number; y: number } }     // widget coordinates, converted through the host scale
  | { do: 'tap'; id: ElementId }
  | { do: 'key'; key: string; id?: ElementId; times?: number }       // focuses `id` first when given
  | { do: 'type'; id: ElementId; text: string }
  | { do: 'expect'; answer?: Answer | null; announce?: string };
```

```ts
// @zq/contracts/src/widget-api.ts, implemented by src/engine/widgets/host.tsx. What a view receives; everything stateful is the host's.
// @zq/contracts has type-only dependencies on preact, @preact/signals-core and zod (for WidgetSchemaModule).
export interface WidgetApi<A extends Json, V extends Json> {
  readonly state: ReadonlySignal<WidgetState<A, V>>;   // read through useComputed only (section 2.5 rule 1)
  readonly locked: ReadonlySignal<boolean>;            // evaluating, correct, revealed, graded quiz items, exam review
  readonly ghost: boolean;                             // true for the tutor's ghost copy: render read-only
  readonly mode: WidgetMode;
  readonly motion: ReadonlySignal<MotionMode>;
  readonly theme: ReadonlySignal<'light' | 'dark'>;
  readonly scope: Scope;
  readonly seed: SeedSource;
  readonly services: WidgetServices;

  change(update: (s: WidgetState<A, V>) => WidgetState<A, V>): void;    // during a gesture; the first change engages Check
  commit(update?: (s: WidgetState<A, V>) => WidgetState<A, V>): void;  // gesture end: action log, announcement, draft save, clears tutor marks
  view(update: (v: V) => V): void;                                      // view-only change: never engages Check, never graded
  announce(text: string): void;                                         // the screen's polite region, at most one message per 600 ms
  feedback(event: 'tap' | 'snap' | 'lift' | 'drop'): void;              // sound and haptic through the platform
  el(id: ElementId): ElementProps;                                      // spread onto every targetable element; returns the same object for the same id for the instance's life, so refs and bound signals never churn a render
}
export interface ElementProps {
  ref: Ref<Element>;                                                    // lets the overlay place badges, rings and notes
  'data-zq-id': string;
  'data-zq-mark': ReadonlySignal<Mark | undefined>;                     // bound signal: no re-render on grade
  'data-zq-hl': ReadonlySignal<HighlightStyle | undefined>;
}
export interface CasService { parse(latex: string): Json }             // LaTeX to MathJSON through the Compute Engine parser
export interface MathfieldService {                                    // MathLive, lazily loaded, fonts shared with KaTeX, sounds off
  mount(el: HTMLElement, o: { value: string; onInput(latex: string): void }): { set(latex: string): void; focus(): void; destroy(): void };
}
export interface WidgetRegistry {
  has(type: string, v: number): boolean;
  cluster(type: string, v: number): ClusterId;
  load(type: string, v: number): Promise<WidgetModule<BaseConfig, Json, Json>>;   // imports the cluster chunk once per session
  preset(ref: `${string}@${number}`): Promise<PresetRuntime | null>;              // the preset's runtime parts, from its own cluster chunk; null if unknown
  preload(clusters: readonly ClusterId[]): Promise<void>;
}
/** A preset at run time: `expand` is compile-only and is not bundled. */
export type PresetRuntime = Pick<PresetDef<BaseConfig, BaseConfig>, 'type' | 'v' | 'predicates' | 'recipes' | 'describeAs'>;
export interface WidgetServices {
  tex: TexService;                                                      // section 5.11
  cas: (() => Promise<CasService>) | null;                              // only when logic.needs includes 'cas'
  mathfield: (() => Promise<MathfieldService>) | null;
  python: PythonRuntime | null;                                         // only for widgets that declare 'python'
  sql: SqlRuntime | null;
}
```

**Primitives are also building blocks.** Beside its `WidgetModule`, every primitive exports controlled components (`<Plot2D>`, `<DragPoint>`, `<Marks>`, `<TokenTray>`) that take signals and callbacks as props. A composite composes them inside its own view with its own single state; a screen widget is always exactly one host and one state, never hosts nested inside hosts.

**Gesture and focus hooks** (`src/engine/interaction`). Composites never attach pointer listeners themselves (lint rule `zq/no-raw-pointer`); they use these, so hit areas, capture, frame coalescing, keyboard paths, tap-then-tap and reduced motion are written once:

```ts
export function useDrag(id: ElementId, o: {
  toLocal(clientX: number, clientY: number): { x: number; y: number };   // from the host scale
  start(): { x: number; y: number };
  move(p: { x: number; y: number }, mods: { shift: boolean; alt: boolean }): void;   // at most once per animation frame, latest pointer
  end(committed: boolean): void;                                         // false on Escape or pointercancel: the host restores the start
  snap?(p: { x: number; y: number }): { x: number; y: number };          // applied on release with spring-snap
  keys: { step: number; big: number; fine?: number; bounds?: [[number, number], [number, number]] };
  exact?: { fields: ('x' | 'y')[]; format(v: number): string };          // E or double tap opens the exact-value editor
  tapTap?: boolean;                                                      // default true (WCAG 2.2 SC 2.5.7)
}): DragBinding;                                                         // props for the handle element, including role="slider" and aria-valuetext
export function useRoving(ids: readonly ElementId[], layout: { kind: 'grid'; cols: number } | { kind: 'list' } | { kind: 'tree' }): RovingBinding;
export function useLiftDrop(ids: readonly ElementId[], slots: readonly ElementId[]): LiftDropBinding;   // tokens: Space lifts, arrows move, Space drops
```

### 5.4 Lifecycle of a widget instance

1. **Compile.** The compiler, through `CompilerRegistry`, validates the config with `schema.ts`, expands presets (recording `preset: 'type@v'`), merges `from:`, resolves `{ where }` sets with `resolvers`, checks every element reference and its label against `staticTargets`, and checks every recipe call against `recipeArgs` (content-format 6.7, 12.1).
2. **Load.** The player reads the screen's widget types, and `registry.load(type, v)` imports the cluster chunk (once per session) and returns the module; a config with `preset` also awaits `registry.preset(ref)`, whose predicates and recipes the host registers as `<preset type>/<name>`.
3. **Mount.** The host creates a child `Scope`, restores a draft (calling `migrate` when its `stateVersion` is older) or calls `init`, renders the view inside an error boundary, gives the root `role="group"`, the config `label` as its name and `describe('brief')` as its description.
4. **Interact.** The view calls `change` during gestures and `commit` at their end. The first `change` engages Check. `commit` writes the action-log line from `summarise`, announces, clears tutor highlights and saves a draft (debounced 1 second, at most 32 KB of JSON; larger is a development error). A pending draft is flushed at once on `visibilitychange` to hidden and on `pagehide`, because iOS may end a backgrounded web view without another event. In the Artifact the host reloaded the open page after each publish [measured: S1, 7 October 2026], and S1 could not record whether either event fires first [unverified: S1 did not record it], so `commit` also writes the draft synchronously to `sessionStorage` through `DraftStore.mirror`; `sessionStorage` survived the host's reload [measured: S1, 7 October 2026], and the mount restores the newer copy (section 6.2.6; `docs/DECISIONS.md` B22).
5. **Check.** The player locks the widget (while locked, `change` and `commit` are ignored), takes `answer`, calls `@zq/graders` with a `GradeCtx` bound to this widget's predicates, and the host paints `marks` through the overlay. On a diagnosis, the show-why runner snapshots `v`, expands the steps and plays them under the current grade generation.
6. **Try again.** The generation increments (cancelling show-why), marks clear, `v` restores from the snapshot, and the lock lifts. `a` is untouched, so the learner's input stays (design research 5.4).
7. **Show solution.** The generation increments; `solved` gives the revealed state; the overlay paints `reveal` marks in hint indigo, never green.
8. **Start over.** The generation increments; `init` with the same seed.
9. **Leave.** The scope disposes every timer, frame, listener, effect and worker handle the instance owned; a final draft is saved unless the screen is complete.

### 5.5 Keyboard, pointer and accessibility contract

**Global keys** (`engine/interaction/keymap.ts`), active unless focus is in a text field or the code editor, where Ctrl or Cmd with Enter replaces Enter. Two rules keep them safe:

- **Enter** acts as the primary button only when focus is on the screen itself (the question heading, a widget's group, or nothing). On a button, link, option card or other control, the browser's own activation runs and the global handler does nothing, so Enter never fires twice.
- **Single-character keys** (H, W, D, T, 1 to 9, ?) are on by default and turned off by Settings, Accessibility, "Single-key shortcuts" (decision 34; WCAG 2.2 SC 2.1.4). With them off, the same actions stay on visible buttons; Enter and Escape are not single-character shortcuts and stay.

| Key | Action |
|---|---|
| Enter | The primary button: Check, Continue or Try again |
| Escape | Close the open sheet or modal; cancel a drag in progress |
| H | Open the hint ladder (when available) |
| W | Why? (after grading) |
| D | Describe sheet: `describe('full')` for every widget on the screen |
| T | Table view of the focused chart |
| 1 to 9 | Select option cards in order |
| ? | Keyboard help sheet |

**Widget keys** are those of calc-linalg 2.8 and programming 2.7, implemented by `useDrag`, `useRoving` and `useLiftDrop`: arrows step, Shift steps ten times, Alt a tenth, Home and End go to the limits, E opens the exact-value editor, Space toggles or lifts and drops, Escape cancels.

**Pointer pipeline.** `pointerdown` reads geometry once and captures the pointer; `pointermove` stores the latest position; one animation frame callback per frame calls `move`; state flows through signals to bound attributes in the same frame. `touch-action: none` is set on handles only, so the page scrolls when a finger lands on empty canvas. Hit areas are at least 44 by 44 px.

**Announcements.** One polite live region per screen, owned by the player. Widgets announce on commit only, throttled to one message per 600 ms. The verdict uses the same region; exams use none until submission.

**Focus.** On a new screen, focus moves to the screen's question heading. Sheets and modals trap focus while open and return it on close. The code editor never traps: Escape then Tab leaves it.

**Text entry on phones** (decision 35). On a device whose primary pointer is coarse (`matchMedia('(pointer: coarse)')`), numeric, interval, matrix-cell and expression answers render `inputmode="none"` and open the in-app `Keypad` and `SymbolBar` from `ui/`, which carry the fraction bar, minus sign, `^` and the interval brackets the graders accept; a "Use system keyboard" key switches one field to the system keyboard for the visit. Free text, chat, long-form answers and code use the system keyboard; while it is open, the player's button row is positioned from `visualViewport.height` and `offsetTop` so Check stays above the keyboard, and the focused field scrolls into the space left. Fixed elements also respect `env(safe-area-inset-*)`, as the prototype's sheet and tab bar do.

**Text alternatives.** `describe('brief')` is the widget's accessible description; `table()` backs the Table view; display-only diagrams render `role="img"` with the brief description as the label.

### 5.6 Where the catalogues' methods went

| Catalogue method | New home |
|---|---|
| `getState`, `setState` | `api.state` (read), `api.change` and `api.commit` (write); the host restores drafts |
| `ready()`, `answer()` | `logic.answer` (non-null means ready) |
| `dirty()` | `logic.dirty` |
| `lock(on)` | `api.locked`, driven by the player |
| `mark(m)`, `showGrade(g)`, `clearMarks()`, `clearGrade()` | `logic.marks` plus the host overlay |
| `showWhy(key)` | `logic.recipes` plus the host's show-why runner |
| `reveal()` | `logic.solved` plus `reveal` marks |
| `reset()` | the host calls `logic.init` |
| `describe(level)` | `logic.describe` |
| `targets()`, `ids()` | `logic.targets` |
| `highlight(ids)`, `annotate(id, text)`, `clearTutor()` | the host overlay, driven by hints, the tutor and show-why |
| `preview(patch)` | the host renders a ghost copy of the view (`api.ghost`) after the guard (section 5.7.4) |
| `secret()`, `tryable()`, `tryValue()`, `code()` | the same names on `logic` |
| `snapshot()` (calc-linalg, P1) | the host rasterises the widget's SVG root through an `Image` and a canvas; no widget code. An SVG drawn as an image sees neither the page's CSS variables nor its web fonts, and a `foreignObject` (KaTeX labels) taints the canvas in Safari [recalled], so the host serialises computed colours inline, embeds the used fonts as `data:` URIs, draws HTML labels onto the canvas separately, and offers the action only where `limits().images` exists (absent in the owner's iPhone view [measured by the owner]) |
| `on('change' \| 'commit')` | the host emits engine events from `change` and `commit` |
| `resize()` | a `ResizeObserver` in the host updates the scale signal views read |
| `destroy()` | the host's scope |
| `predicates`, generators, `configSchema` | `logic.predicates`; generators stay in `content/generators` (content-format 5); `schema.ts` |
| `targets()` id syntax | `kind:name`, prefixed with the widget id on multi-widget screens (section 0.3) |

### 5.7 The lesson player

The player is a pure reducer plus an effect runner. The reducer never touches the DOM, a timer or the network; the runner (`effects.ts`) performs effects and feeds results back as events. Every transition is a row in a test table.

#### 5.7.1 Types

```ts
// src/engine/player/machine.ts
export type Phase =
  | { k: 'reading' }                                    // title, demonstrate, summary: Continue only
  | { k: 'exploring'; satisfied: boolean }              // explore: Continue once continueWhen holds (or at once without one)
  | { k: 'idle' }                                       // task screen, no usable answer yet: Check disabled
  | { k: 'engaged' }                                    // Check enabled
  | { k: 'evaluating'; gen: number }                    // inputs locked, at most 150 ms for non-code checks
  | { k: 'running'; gen: number; what: 'run' | 'submit' }   // code screens
  | { k: 'correct'; grade: Grade; firstTry: boolean }
  | { k: 'not-yet'; grade: Grade }
  | { k: 'revealed' }
  | { k: 'blocked'; why: 'python-loading' | 'python-failed' | 'widget-failed' };

export type Overlay = null | { k: 'hints'; rung: 1 | 2 | 3 } | { k: 'why' } | { k: 'describe' } | { k: 'tutor' } | { k: 'keys' };

export interface Tally { attempts: number; hints: 0 | 1 | 2 | 3; result?: 'first-try' | 'retry' | 'revealed' | 'explored' | 'read'; mc?: ContentId }

export interface PlayerState {
  lesson: ContentId; rev: number;
  section: 'screens' | 'quiz' | 'complete';
  index: number;                                        // screen index, or quiz item index
  phase: Phase;
  overlay: Overlay;
  nudge: TokenList | null;                              // shown under the input; costs no attempt
  gen: number;                                          // grade generation; stale results and show-why compare against it
  checked: Record<LocalId, number>;                     // Checks per screen; hints open after this screen's first Check,
  activeInputMs: Record<LocalId, number>;               // or after 90 s of active time with an input (trap screens: first Check only)
  tally: Record<LocalId, Tally>;
  quiz: Record<ContentId, { verdict: 'correct' | 'not-yet'; whyOpened: boolean }>;
  complete: null | 'celebrate' | 'rest-day' | 'streak' | 'next';
}

export type PlayerEvent =
  | { t: 'open'; resume?: { section: 'screens' | 'quiz'; index: number } }
  | { t: 'engage' } | { t: 'disengage' }
  | { t: 'check' } | { t: 'run' } | { t: 'submit' }
  | { t: 'graded'; gen: number; grade: Grade }
  | { t: 'ran'; gen: number; result: RunResult; grade?: Grade }       // grade only after submit
  | { t: 'try-again' } | { t: 'start-over' }
  | { t: 'hints' } | { t: 'next-rung' } | { t: 'why' } | { t: 'describe' } | { t: 'tutor' } | { t: 'keys' } | { t: 'close' }
  | { t: 'show-solution' }
  | { t: 'satisfied' }
  | { t: 'continue' }
  | { t: 'blocked'; why: 'python-loading' | 'python-failed' | 'widget-failed' } | { t: 'unblocked' }
  | { t: 'leave' };

export type Effect =
  | { e: 'lock'; on: boolean }
  | { e: 'grade'; gen: number }                                     // grades the answer widget, then dispatches 'graded'
  | { e: 'run-code'; gen: number; tests: 'examples' | 'all' }
  | { e: 'paint'; grade: Grade } | { e: 'unpaint' }
  | { e: 'show'; gen: number; steps: ShowStep[] }                  // diagnosis show-why or the screen's `after`
  | { e: 'restore-view' } | { e: 'reset-widgets' } | { e: 'reveal'; gen: number }
  | { e: 'highlight'; ids: ElementId[] }                            // the "Point" rung
  | { e: 'record'; draft: EventDraft }                              // an ASSESSMENT.md 13.2 event: att, lsn
  | { e: 'feedback'; sound?: SoundName; haptic?: HapticName }
  | { e: 'announce'; text: TokenList }
  | { e: 'bertie'; state: 'correct' | 'notyet' | 'celebrate' | 'streak' | 'idle' }
  | { e: 'tutor-auto'; mode: 'diagnose' | 'recap' }                // the tutor gate and consent rule still apply (ai-tutor 0.1 decision 22)
  | { e: 'save-position' }
  | { e: 'prefetch'; what: 'next-screen' | 'quiz' | 'next-lesson' }
  | { e: 'focus'; on: 'question' | 'primary' | 'verdict' }
  | { e: 'navigate'; to: Route };

export function step(s: PlayerState, ev: PlayerEvent, lesson: CompiledLesson, policy: ItemPolicy): readonly [PlayerState, readonly Effect[]];
```

`EventDraft` is an event body without its envelope; `engine/progress/append.ts` adds `id`, `t`, `tz`, `dev`, `seq`, `rel`, `app` and `v`. XP and MP values on an `att` event come from the pure rules in `engine/progress/fold/points.ts` (assessment 12.2, 12.3), called by the reducer, so the number the learner sees and the number the log stores cannot differ.

#### 5.7.2 Transitions on a task screen (lesson policy)

| From | Event | Guard | To | Effects |
|---|---|---|---|---|
| `idle` | `engage` | | `engaged` | |
| `engaged` | `disengage` | `answer()` is null again | `idle` | |
| `engaged` | `check` | | `evaluating(gen)` | `lock on`, `grade(gen)` |
| `evaluating` | `graded`, verdict nudge | same `gen` | `engaged` | `lock off`, nudge shown and announced; no attempt counted |
| `evaluating` | `graded`, correct | same `gen` | `correct` | `paint`, `feedback correct`, `announce` reason, `record att`, `show after`, `bertie correct`, `focus primary` |
| `evaluating` | `graded`, not yet | same `gen` | `not-yet` | `paint`, `feedback not-yet`, `announce` diagnosis line, `record att`, `show` diagnosis steps, `bertie notyet`; `tutor-auto diagnose` when no authored diagnosis matched |
| any | `graded` or `ran` | different `gen` | unchanged | none: a stale result |
| `not-yet` | `try-again` | | `engaged` | `gen + 1`, `unpaint`, `restore-view`, `lock off`, `focus question` |
| `idle`, `engaged`, `not-yet` | `hints` | `firstCheckDone`, policy allows hints | overlay `hints(1)` | |
| overlay `hints(n)` | `next-rung` | `n < 3` | `hints(n + 1)` | at rung 2: `highlight(point ids)` |
| `not-yet` | `show-solution` | `attempts >= 2` or rung 3 seen | `revealed` | `gen + 1`, `reveal`, `record att` with verdict revealed and 0 XP, `announce` solution line |
| `correct`, `not-yet`, `revealed` | `why` | | overlay `why` | |
| `idle`, `engaged`, `not-yet` | `start-over` | | `idle` | `gen + 1`, `unpaint`, `reset-widgets` |
| `correct`, `revealed` | `continue` | | next screen's entry phase | `record lsn screen`, `save-position`, `prefetch next-screen`, progress bar advances here and only here |
| `reading` | `continue` | | next screen | `record lsn screen` |
| `exploring(false)` | `satisfied` | | `exploring(true)` | Continue enabled |
| `exploring(true)` | `continue` | | next screen | `record lsn screen` |
| `engaged` (code) | `run` | runtime ready | `running(run)` | `run-code examples` |
| `engaged` (code) | `submit` | runtime ready | `running(submit)` | `lock on`, `run-code all` |
| `running(run)` | `ran` | same `gen` | `engaged` | results shown |
| `running(submit)` | `ran` | same `gen` | `correct` or `not-yet` | as for `graded` |
| entry to a code screen or code quiz item | `open` or `continue` from the previous screen | its runtime answers `not-in-this-build` (the Artifact: `PythonRuntime` or `SqlRuntime` is the handoff stub) | `reading`, with the handoff panel (starter code, recorded output, link) | Continue enabled at once (second review round; `docs/PLAN.md` 4.3, live-code screens) |
| `reading` (handoff panel) | `continue` | | next screen or quiz item | `record lsn screen` with `deferred: 'web'`; tally `read`: no attempt, no XP, no Redo entry; the fold derives a "Finish in the web app" item keyed by (lesson id, `rev`, screen id), which a matching result code clears (`ASSESSMENT.md` 14.3) |
| any task phase | `blocked` | | `blocked` | Check disabled, reason shown with Retry |
| `blocked` | `unblocked` | | `idle` or `engaged` | |
| last screen | `continue` | | quiz item 0 | `prefetch quiz` |
| last quiz item, graded or deferred | `continue` | | `complete: celebrate` | `record lsn complete` (with `perfect`, and the ids of deferred items, whose result codes the "Passed" star waits for), `bertie celebrate`, `feedback complete`, `tutor-auto recap` |
| `complete` | `continue` | | rest-day if earned today, then streak if this lesson qualified the day, then `next` | values read from the derived state, never computed here |
| any | `leave` | | unchanged | `save-position`, `navigate` course map; the scope disposes |

Overlays close on `close` or Escape and never change the phase. Bertie's held state follows the phase through one mapping table in `effects.ts`.

#### 5.7.3 Item policies

The quiz, practice, review, redo, homework, exam and placement flows reuse the same reducer with a different policy, through `ItemRunner`:

```ts
// src/engine/player/policy.ts
export interface ItemPolicy {
  mode: WidgetMode;
  feedback: 'immediate' | 'on-submit' | 'silent';      // silent: placement records without verdicts
  attempts: 'unlimited' | 1;
  hints: boolean;
  why: 'after-grade' | 'after-submit' | 'never';
  solution: 'after-two' | 'after-grade' | 'after-submit' | 'never';
  points: 'lesson-screen' | 'quiz' | 'practice' | 'homework' | 'exam' | 'none';   // which rule in fold/points.ts
  redo: 'revealed' | 'wrong-first-try' | 'none';      // what enters the Redo queue (assessment 6.1)
  timer: null | { attempt: string };                  // exam papers: the clock lives in exam events (assessment 3.4)
  sound: boolean; haptics: boolean;                    // never during exams (design research 4.9)
}
```

| Policy | Feedback | Attempts | Hints | Why | Solution | Redo | Source |
|---|---|---|---|---|---|---|---|
| Lesson screen | immediate | unlimited | after this screen's first Check or 90 s of active input (`trap`: first Check only) | after grade | after two | revealed | design research 5.4, assessment 0.1 decision 11, `docs/PLAN.md` 6.5 |
| Lesson quiz | immediate | 1 | none | after grade | after grade | wrong first try | design research 5.9 |
| Practice | immediate | 1 | only in help-enabled sets | after grade | after grade | wrong first try | assessment 2.6 |
| Level review, redo | immediate | 1 | none | after grade | after grade | wrong first try | assessment 2.4, 6 |
| Homework | on submit | edits until submit | none | after submit | after submit | wrong first try | assessment 0.1 decision 2 |
| Exam paper | on submit | edits until submit | none | after submit | after submit | wrong first try | assessment 3 |
| Placement | silent | 1 | none | never | never | none | assessment 7.1 |

Whether Bertie is available is never a policy field: `TutorService`'s gate decides from the same state (ai-tutor 2.2), so there is one choke point.

#### 5.7.4 Tutor effects and the preview guard

The player passes Bertie's validated actions (ai-tutor 5) to the host:

- `highlight` and notes go to the overlay; they clear on the learner's next commit, on Try again and on leaving.
- `setWidgetHint` with `kind: 'chip'` shows a "Try this" chip; tapping it calls `logic.tryValue` and applies the result through `change` and `commit`, so it is the learner's own action in the log.
- `setWidgetHint` with `kind: 'ghost'` passes the **guard**: the host computes the patched state with `tryValue`; it refuses if `logic.answer` on the patched state differs from the current answer, or if grading the patched answer would give `correct`. Otherwise it renders a second, read-only copy of the view at 60% opacity with dashed outlines over the original (`api.ghost = true`), at most one at a time.
- No action can reach `change`, a grade, the Redo queue or the position (ai-tutor 5.4 rule 1); the host exposes no such path to the tutor.

### 5.8 Screens and routing

```ts
// src/app/router.ts
export interface ScreenDef<P extends Record<string, string>> {
  id: string;
  pattern: string;                                              // '#/lesson/:lesson/:screen?'
  chrome: 'shell' | 'focus' | 'bare';                           // shell: navigation; focus: lesson or paper frame; bare: onboarding, handoff
  parse(raw: Record<string, string>): P | null;                 // zod/mini; null renders Not found
  title(params: P, data: unknown): string;                      // document title, announced after navigation
  load?(params: P, app: AppContext): Promise<unknown>;          // before first render; the tangram shows after 400 ms
  guard?(params: P, app: AppContext): Route | null;             // redirect, for example to an exam in progress
  leave?(app: AppContext): 'ok' | 'confirm';                    // a paper in progress asks first
  View: FunctionComponent<{ params: P; data: unknown }>;
  devOnly?: true;                                               // compiled out of production builds
}
```

`Route` is a hash string (`'#/lesson/lsn.cond.shrinking-sample-space/cross'`), built only through typed helpers in `routes.ts`. `AppContext` is `{ platform: Platform; stores: Stores; registry: WidgetRegistry; tutor: TutorService | null; motion: MotionService }`, created once in `boot.ts` and passed down through a Preact context.

| Route | Screen | Chrome | Main data |
|---|---|---|---|
| `#/today` (also `#/`) | Today: streak, weekly plan, due work, Daily 10, resume | shell | derived state, plan (assessment 8) |
| `#/onboarding` | Onboarding with placement | bare | assessment 7.1 |
| `#/learn`, `#/learn/:stage` | Catalogue by stage, topic and course | shell | manifest, derived state |
| `#/course/:course` | Course map | shell | course bundle (levels only), derived state |
| `#/lesson/:lesson`, `#/lesson/:lesson/:screen` | Lesson player | focus | course bundle |
| `#/review` | Redo queue, practice, homework list, exams | shell | derived state |
| `#/practice/:set`, `#/redo` | Practice and the daily review session | focus | generators, derived state |
| `#/homework/:instance` | Homework set | focus | bundle, draft (lease) |
| `#/exam/:exam`, `#/paper/:attempt` | Rules screen; the paper | focus | assessment 3 |
| `#/drill/:drill` | Standalone code drill; the handoff target | focus | bundle, Python |
| `#/daily` | Daily 10 mental arithmetic | focus | assessment 9 |
| `#/weekly` | Weekly probability problems | shell | assessment 10 |
| `#/notebook`, `#/notebook/:card` | Formula and notation cards | shell | notebook file |
| `#/search` | Search | shell | MiniSearch index per stage |
| `#/plan` | Weekly plan and weekly review | shell | assessment 8 |
| `#/log` | Outside work, projects, real papers | shell | assessment 11 |
| `#/you` | Profile, mastery map, ghost race, achievements, record export | shell | derived state |
| `#/settings`, `#/settings/:section` | Theme, motion, sound, haptics, accessibility (single-key shortcuts), tutor, mascot, study day, storage, export and import, diagnostics with Self-test | shell | settings store |
| `#/import` | Import a progress file or paste a result code | shell | assessment 14 |
| `#/preview/...`, `#/storyboard/...`, `#/specimen/...`, `#/gallery/...`, `#/tutor/...`, `#/system` | Development routes (section 10.2) | bare | dev only |

On navigation the router moves focus to the screen's `h1`, sets the title, announces it, and disposes the previous screen's scope. Unknown routes render Not found with a link to Today. A `#/drill/...` route may carry `?h=<payload>` from the Artifact handoff; the payload is validated (section 11.2) before use. Every screen with `focus` or `bare` chrome has a visible back or close control, so no route depends on a browser back button. Inside the Claude app the system back gesture does nothing in the frame: no `popstate`, and the hash stays where it was [measured: S1, 7 October 2026]. The fallback, now in force: the router never relies on the gesture. Every route except the four tab roots (`#/today`, `#/learn`, `#/review`, `#/you`; design research 7.1) shows a visible back or close control, shell screens such as `#/learn/:stage`, `#/course/:course`, `#/notebook/:card` and `#/settings/:section` included. The control navigates to the screen's parent route, a typed `Route` from `routes.ts`, never through `history.back()` or `history.go()`: in one of five S1 runs (`muyo87q6`) a second hash change left `history.length` unchanged and walking back fired no `popstate` [measured: S1, 7 October 2026]. A route test checks that every route except the tab roots renders a back or close control with an accessible name [our choice], and `zq/no-forbidden-apis` refuses `history.back` and `history.go` (section 10.4); both arrive with the router at `docs/PLAN.md` stage 74a. The control on shell screens adds to design research 7's shell (`docs/DECISIONS.md` B23). Nothing is lost: the position is saved on every Continue, and a reopened lesson resumes at its screen (section 5.7.2).

### 5.9 Platform adapters

The only target-specific code. Engine, widgets, screens and the tutor see these interfaces and nothing else.

```ts
// @zq/contracts/src/platform.ts
export interface Platform {
  readonly target: 'artifact' | 'web' | 'test';
  readonly build: { app: string; content: string; commit: string };
  readonly content: ContentSource;
  readonly progress: ProgressStore;        // ASSESSMENT.md 13.5, unchanged
  readonly drafts: DraftStore;             // per-device lesson drafts; homework and papers use progress.draft (leased)
  readonly cache: BlobCache;               // disposable: bundles, generator modules
  readonly kv: KeyValue;
  readonly tutor: TutorBackend | null;     // AI-TUTOR.md 6.1; null when this view has no tutor
  readonly python: PythonRuntime;          // web: Pyodide; Artifact: the handoff stub (revision 2)
  readonly sql: SqlRuntime;                // web: SQLite; Artifact: the handoff stub
  readonly cpp: CppRuntime | null;         // web only (programming decision 9); null in the Artifact, where C++ drills hand off
  readonly feedback: Feedback;
  readonly clock: Clock;
  readonly random: RandomSource;
  readonly files: FileSaver;
  readonly identity: Identity;
  readonly handoff: Handoff;
  readonly lifecycle: Lifecycle;
}

export interface ContentSource {
  manifest(): Manifest;                                    // synchronous after boot, which fetches the file the page's <meta name="zq-manifest"> names (decision 30)
  course(id: ContentId): Promise<CourseBundle>;            // by hash: cache, else fetch; validated once per hash in the data worker
  generators(id: ContentId): Promise<GeneratorModule>;     // course id in; dynamic import of the topic's gen/<top>.<hash>.mjs (one module per topic)
  searchIndex(stage: 0 | 1 | 2 | 3): Promise<Json>;
  glossary(): Promise<Glossary>;
  notebook(): Promise<NotebookCards>;
  assetUrl(name: string): string;
  prefetch(id: ContentId): void;                           // idle priority
  keepOffline(id: ContentId, on: boolean): Promise<void>;  // web: service worker cache; Artifact: resolves, no effect
  onChange(fn: () => void): () => void;                    // development hot reload only
}
export interface Manifest {
  release: string; format: 1; app: string;
  courses: Record<ContentId, {
    bundle: string; gen?: string; bytes: number;
    clusters: ClusterId[];                                 // widget chunks the course needs
    python: PyPackage[];                                   // union of its drills' `needs`
    sql: boolean;
  }>;
  search: string[]; glossary: string; notebook: string; assets: Record<string, string>;
}
export interface GeneratorModule {
  readonly v: Record<ContentId, number>;
  make(gen: ContentId, seed: number, level: 1 | 2 | 3 | 4 | 5, pool: 'practice' | 'exam'): ItemBody;   // content-format 5.4
  /** Bertie's practice picks (content-format 5.4, ai-tutor 2.11): a seeded point from the level's admissible, non-reserved index matching
   *  the partial assignment over the generator's `tutorParams`; null when nothing matches (the pick is dropped and counted). */
  makeWhere(gen: ContentId, partial: Record<string, Json>, seed: number, level: 1 | 2 | 3 | 4 | 5): ItemBody | null;
}

export interface BlobCache {                               // IndexedDB; least recently used beyond 300 MB or 60% of quota
  get(key: string): Promise<ArrayBuffer | null>;
  put(key: string, data: ArrayBuffer, kind: 'course' | 'gen' | 'search'): Promise<void>;
  evict(kind?: 'course' | 'gen' | 'search'): Promise<void>;
  usage(): Promise<{ bytes: number; quota: number | null }>;
}
export interface DraftStore {                             // keys: 'lesson:<lsn id>@<rev>:<screen id>:<widget id>', so a new rev never meets an old draft
  get(key: string): Promise<Json | null>; put(key: string, value: Json): Promise<void>; drop(prefix: string): Promise<void>;
  mirror(key: string, value: Json): void;                 // Artifact: a synchronous sessionStorage copy at every commit, before the debounced put; get returns the newer copy, drop clears both (section 6.2.6; DECISIONS.md B22). A no-op on the web
}
export interface KeyValue {                                // small device-local values; synchronous reads from a mirror loaded at boot
  get<T extends Json>(key: string): T | undefined;
  set(key: string, value: Json): void;
  secret(name: 'tutor-token'): Promise<string | null>;     // IndexedDB only, never localStorage
  setSecret(name: 'tutor-token', value: string | null): Promise<void>;
}

export type PyPackage = 'numpy' | 'pandas' | 'scipy' | 'statsmodels' | 'sklearn' | 'matplotlib' | 'pytest' | 'hypothesis';   // the content schema's Drill.needs enum, spelt identically; 'cvxpy' and 'highspy' join at the 2.0b wave (docs/PLAN.md 5.7)
export interface PythonRuntime {
  readonly status: ReadonlySignal<
    | { k: 'cold' } | { k: 'loading'; step: string; done: number; total: number }
    | { k: 'ready'; packages: PyPackage[] } | { k: 'failed'; code: 'network' | 'integrity' | 'memory' | 'crashed' | 'unsupported' }>;
  available(packages: readonly PyPackage[]): { ok: true; downloadBytes: number } | { ok: false; reason: 'not-in-this-build' };   // downloadBytes: what is not yet cached; 0 means warm() needs no network
  warm(packages: readonly PyPackage[]): Promise<void>;     // idempotent; starts the worker and loads packages
  run(req: RunRequest, io: { signal: AbortSignal; onEvent(e: RunEvent): void }): Promise<RunResult>;
  terminate(): void;
}
export interface RunRequest {
  drill: ContentId; rev: number;
  mode: 'drill' | 'script' | 'pytest' | 'answer' | 'checker';   // content-format Drill.mode (sql and C++ use their own runtimes)
  files: Record<string, string>;                           // the learner's files
  support: Record<string, string>;                         // tests.py, zqtest.py, data files: from the course bundle
  entry?: string;
  tests: 'examples' | 'all';
  examples: string[];
  timeLimitMs: number;                                     // per test (content-format: 5,000 by default)
  needs: readonly PyPackage[];
}
export type RunEvent =
  | { k: 'stdout' | 'stderr'; text: string }               // at most 4,000 characters per stream (programming 2.4)
  | { k: 'test'; name: string; status: 'pass' | 'fail' | 'error' | 'timeout'; ms: number; hidden: boolean;
      input?: string; expected?: string; actual?: string; error?: { type: string; message: string; line?: number } };
export interface RunResult { status: 'pass' | 'fail' | 'error' | 'timeout' | 'cancelled'; passed: number; total: number; firstFailure?: string; ms: number }
export interface CppRuntime {                              // web only; present only if the 1.9 cpp-runner spike passes (programming 8); no Compiler Explorer route (docs/PLAN.md)
  readonly backend: 'clang-wasm';
  run(req: RunRequest & { language: 'cpp'; flags: string[] }, io: { signal: AbortSignal; onEvent(e: RunEvent): void }): Promise<RunResult>;
}
export interface SqlRuntime {
  load(db: { name: string; sql: string }): Promise<void>;
  query(sql: string, o: { signal: AbortSignal; maxRows: 1000 }): Promise<{ columns: string[]; rows: Json[][]; plan?: string[] } | { error: string }>;
}

export type SoundName = 'correct' | 'not-yet' | 'complete' | 'streak' | 'tap' | 'snap';
export type HapticName = 'correct' | 'not-yet' | 'snap' | 'complete';
export interface Feedback {
  readonly soundOn: Signal<boolean>; readonly hapticsOn: Signal<boolean>;
  sound(name: SoundName): void;            // Web Audio synthesis; peak about 12 dB below full scale
  haptic(name: HapticName): void;          // navigator.vibrate where it exists (Android Chrome); a no-op elsewhere
  unlock(): void;                          // resumes the AudioContext on the first gesture
  suppress(on: boolean): void;             // exams
}
export interface Clock { now(): number; perf(): number; tz(): number }   // tz: minutes east of UTC
export interface RandomSource { deviceId(): string; seed(): number; nonce(bytes: number): string }   // crypto.getRandomValues
export interface FileSaver {
  save(name: string, mime: string, data: Blob | string): Promise<'saved' | 'unsupported' | 'cancelled' | 'failed'>;
  pick(accept: readonly string[]): Promise<File | null> | null;   // null: no file picker in this view, offer paste instead
}
export interface Identity { viewerId(): Promise<string | null>; canWrite(): Promise<boolean | null> }
export interface Handoff {
  toWeb(route: string, payload?: Json): { href: string | null; copyText: string };   // href null where links cannot leave the Artifact
  receive(): Json | null;                                   // web: the validated ?h= payload of the current route
}
export interface Lifecycle {
  readonly visible: ReadonlySignal<boolean>;
  readonly online: ReadonlySignal<boolean>;
  readonly writer: ReadonlySignal<'this-tab' | 'other-tab'>;
  takeWriter(): Promise<void>;
  persist(): Promise<boolean>;                              // navigator.storage.persist on the web
  reload(): void;
}
```

`CourseBundle`, `CompiledLesson`, `ItemBody`, `Glossary` and `NotebookCards` are the compiled output types of `@zq/content-schema` (content-format 8); `ImportReport` is assessment 14.2's; `EventDraft` is an `ASSESSMENT.md` 13.2 event without its envelope.

| Interface | Web | Artifact | Tests and gallery |
|---|---|---|---|
| `ContentSource` | same-origin fetch, service worker cache | own-file fetch, `BlobCache` | in-memory bundles |
| `ProgressStore` | `IdbStore` (assessment 13.5) | `DbStore` with `IdbStore` mirror; `IdbStore` alone when `db` or `user` is absent | `MemoryStore` |
| `DraftStore`, `BlobCache`, `KeyValue` | IndexedDB (`idb`), `localStorage` mirror for theme and motion only | same, plus a synchronous `sessionStorage` mirror of the route and of every pending draft (a widget's through `DraftStore.mirror`; a homework set's and a paper's answers through `ProgressStore.draft`, assessment 13.4), kept for the session's lifetime and cleared by "Delete my progress" (section 6.2.6; `docs/DECISIONS.md` B22) | memory |
| `TutorBackend` | proxy backend (ai-tutor 6.3) | `sample` backend (ai-tutor 6.2) | scripted fake |
| `PythonRuntime` | worker, native loader | handoff stub: `available()` answers `not-in-this-build` for every drill, and `run` is never called (revision 2) | worker in browser tests; a stub in Node |
| `SqlRuntime` | SQLite worker | handoff stub | same |
| `CppRuntime` | the W-C spike's backend | `null`: handoff and local paste (programming 2.4) | recorder |
| `FileSaver` | Blob link and `<input type=file>` | `downloads` capability to save; `<input type=file>` to pick, which opened the picker in the frame [measured: S1, 7 October 2026; a full read not tried]; paste where no picker | recorder |
| `Identity` | `null` id, can write | `user` capability | fixed |
| `Handoff` | receives | builds anchor links (`target="_blank"`) to the web app with the payload in the fragment, at most 8 KB; an anchor opens a browser from the frame and `window.open` does nothing [measured: S1, 7 October 2026]; whether a fragment of up to 8 KB survives the host's link handling is [unverified: S1's link had no fragment], checked in `docs/PLAN.md` stage 82's iPhone handoff check (`docs/DECISIONS.md` B30), with the copyable text of assessment 14.3 as the fallback | recorder |
| `Lifecycle` | Web Locks, `navigator.onLine`, `storage.persist` | Web Locks, which work in the frame [measured: S1, 7 October 2026], else heartbeat lease | fake |

**Shell drills** (`language: shell`) need no runtime: they run in the `shell-interpreter` that backs `shell-sim` (pure JavaScript over the virtual file system, programming 2.4) and are graded by that widget's predicates, on both targets.

### 5.10 Content loading

#### 5.10.1 Start-up

1. A classic script tests for `structuredClone`, `Array.prototype.at`, `CSS.supports('animation-timing-function', 'linear(0, 1)')` and module support; failing any, it shows the old-browser page.
2. The entry module applies theme and motion from the `localStorage` mirror before first paint, renders the shell with skeletons, and fetches the content manifest named by the page's `<meta name="zq-manifest">` (about 10 KB; decision 30). A failed fetch retries once, then shows "Could not start Zero to Quant. Check the connection and try again." with Retry; on the web the service worker serves it offline.
3. The platform constructs. In the Artifact, `claude.use('db' | 'user' | 'sample' | 'downloads')` run in parallel; each resolves or turns `null` after the host's 10 seconds [sourced: `claude.d.ts`], and the app renders without them meanwhile (design for absence).
4. Writer election (section 4.7), then `progress.load()`: the newest snapshot and the events after its basis. Up to 2,000 tail events fold on the main thread; more go to the data worker.
5. The derived state signal is set; the route renders.
6. At idle: the data worker starts, the `core` widget cluster and KaTeX (the web chunk, or the CDN module in the Artifact) preload, and the current course's bundle prefetches. In the Artifact, steps 2 to 6 run only after the bootstrap's `import()` of the entry has resolved its CDN modules through the import map (section 6.2.7).
7. Web only: the service worker registers after the first render.

#### 5.10.2 Entering a course

`manifest.courses[id]` gives the bundle and generator file names (content hashes) and the course's clusters and Python packages. The loader asks `BlobCache` by hash, else fetches; a newly fetched bundle goes to the data worker, which checks its SHA-256 against the hash in its file name and validates it once against `@zq/content-schema`'s structural schemas, and is cached with a "validated" flag. Widget-specific config fields are validated at compile time only (CI, through `CompilerRegistry`), never at run time, so the data worker's size does not grow with the widget library; at run time a config is checked for its `BaseConfig` fields and a registered `type@v`. The player then preloads the course's widget clusters. On the web, if the current lesson has code screens and `python.available(course.python).downloadBytes` is 0, `python.warm(course.python)` starts on the lesson's title screen; otherwise the title screen shows "This lesson runs Python. Download it now (21 MB)?", the figure being `downloadBytes` (21 MB is core, standard library, NumPy and pandas in the native layout, section 6.4.1), and warming starts on that tap or when the learner reaches the first code screen, never on its own over a connection the learner has not chosen. In the Artifact the title screen says which screens open the web app instead. Generator modules load on the first practice, review or homework item.

#### 5.10.3 Failure behaviour

| Failure | Behaviour |
|---|---|
| Course fetch fails | One retry after 1 second; then "Could not load this course. Check the connection and try again." with Retry; other courses and screens keep working |
| Bundle bytes do not match the hash in their name | Refetched once with a cache-busting query; then treated as "fails validation" |
| Bundle fails validation | Not cached; "This course could not be opened. Update the app." and a log entry with the first schema path; never a partial lesson |
| Bundle `zq` major unknown | "Update the app to open this course" (content-format 4.5); only stale caches can cause it (decision 30) |
| Lazy chunk import fails | One retry; then "A new version is available. Reload to continue." with Reload. The host reloaded the open page after each publish [measured: S1, 7 October 2026], so the cause is the network or a page the host did not reload, such as a backgrounded app, a second device or the desktop and web viewers [unverified], whose own-file fetches reach a newer version that no longer holds its files (version scoping is unmeasured; sections 6.2.6 and 8.2) |
| A fetch hangs | Every own-file fetch carries `AbortSignal.timeout` (20 s for the manifest and bundles, 120 s per Python package on the web); a timeout is a failed fetch under the rows above (added by `docs/PLAN.md` 8.1) |
| Widget throws in render or logic | The widget's error boundary shows "This part of the screen failed. Skip this screen" (Continue enabled, result `read`), logs the error with the widget type and version, never the state |
| Generator throws | The item is skipped, the set draws the next seed, the error is logged with `gen`, `v` and the seed |
| IndexedDB unavailable or full | `BlobCache` and `DraftStore` fall back to memory; content refetches per session; progress follows assessment 13.8 |

### 5.11 Motion and rendering services

```ts
// src/engine/motion/presets.ts. Values from design research 4.2 to 4.4; mass 1.
export const SPRINGS = {
  snap:     { stiffness: 500, damping: 40 },   // damping ratio 0.89: drop into slot, sheet snap
  bounce:   { stiffness: 320, damping: 24 },   // 0.67: check badge, XP chip, streak bolt, node completion
  physical: { stiffness: 170, damping: 14 },   // 0.54: balance beams, tree swings
} as const;
export type EaseName = 'standard' | 'enter' | 'exit' | 'morph' | 'linear';
export const DURATIONS = { press: 80, hover: 120, micro: 150, base: 200, enter: 200, exit: 120, sheetIn: 280, sheetOut: 200,
                           progress: 320, explainMin: 480, explainMax: 800, count: 700, stagger: 80 } as const;

// src/engine/motion/index.ts
export interface MotionService {
  readonly mode: ReadonlySignal<MotionMode>;                // OS setting, in-app setting (System, Full, Reduced), or 'test'
  spring(target: Signal<number>, to: number, spring: keyof typeof SPRINGS | { stiffness: number; damping: number },
         scope: Scope, velocity?: number): Promise<void>;   // reduced and test: lands at once
  tween(target: Signal<number>, to: number, ms: number, ease: EaseName, scope: Scope): Promise<void>;
  animate(el: Element, frames: Keyframe[], o: { ms: number; ease: EaseName; delay?: number }, scope: Scope): Promise<void>;   // Web Animations
  sequence(steps: (() => Promise<void>)[], scope: Scope, skippable: boolean): Promise<void>;   // celebrations: a tap jumps to the end
}
```

- **Integrator.** `spring.ts` is semi-implicit Euler with fixed substeps of $\tfrac{1}{240}$ s, sleeping when $|x - x^\ast| < 10^{-3}$ and $|v| < 10^{-3}$, so a still screen requests no frames. It retargets mid-flight without a jump, which Bertie's bobble needs (`BERTIE.md` 4.2). Bertie and widgets share it.
- **CSS springs.** Pressed buttons, sheets and chips use the `linear()` approximations in `tokens.css` (design research 4.3), with no JavaScript.
- **Reduced motion.** Springs and tweens land at once; the show-why runner turns morphs into a before-and-after pair with a Play button; pulses become a static ring; count-ups show the final value; the button press still sinks (design research 4.9).
- **Test mode.** Set by `?motion=test` in development and preview builds only: every spring, tween, animation, stagger and celebration completes in the same frame, which is what makes screenshots deterministic.

```ts
// src/engine/render
export interface TexService {
  ready(): boolean;
  load(): Promise<void>;                                     // imports KaTeX once: the web chunk, or the locked CDN module in the Artifact
  html(src: string, display?: boolean, source?: 'authored' | 'untrusted'): string; // KaTeX output, least-recently-used cache of 1,000 entries keyed by source;
                                                             // macros from content/tex-macros.yaml;
                                                             // output 'htmlAndMathml' on the web, 'mathml' in the Artifact (decision 37);
                                                             // authored configuration, the default (docs/DECISIONS.md B33): throwOnError true; strict a
                                                             // function returning 'ignore' for the code 'htmlExtension' and 'error' for every other code;
                                                             // trust limited to \htmlData with a name matching ^[a-z][a-z0-9-]{0,15}$; errorColor '#0a0100',
                                                             // the reserved colour KaTeX gives a command trust refuses, which zq check fails (section 11.3);
                                                             // in the Artifact with the runtime flag artifact.termBinding on, also a function macro for
                                                             // \htmlData: term=<k> renders as \textcolor{<sentinel k>}{<body>}, any other attribute as its
                                                             // body alone, at render time (B27; section 14 item 20). 'untrusted' (Bertie's replies and
                                                             // learner text): trust false, strict 'ignore', maxSize 10, maxExpand 1000 (ai-tutor 8.8).
                                                             // The reserved colours and the sentinel mapping are imported from @zq/contracts (B27, B33)
}
// <Tex src display />: the only component that sets innerHTML, and only to KaTeX output (section 11.1).
//   A display formula wider than its line box scrolls sideways in its own container and is never clipped or scaled:
//   5 of the 40 specimen display formulas were wider than the owner's phone, formula 40 at 486 px in a 377 px line box
//   [measured: S1, 7 October 2026, mathml.specimen].
// <TexSlots src slots={{ a: signal }} />: renders once with each slot as a sentinel \text{} token, on both outputs (decision 37);
//   the web's HTML span text node is bound to its signal, and in every MathML tree (the Artifact's output, the web's hidden copy)
//   the sentinel <mtext> is swapped for an <mn> made with createElementNS whose textContent follows the signal,
//   so live numbers inside formulas cost a text write per frame, render in the maths font and read correctly aloud.
// <Layer> memoises a static SVG group (section 2.5 rule 2).
// <CanvasLayer draw={(ctx, t) => ...} deps={[...signals]} dprCap={2} />: redraws on the next frame after a dependency changes;
//   `t` is the design tokens read from CSS variables, refreshed when the theme signal changes.
// scales.ts: linear and log scales, nice ticks, about 60 lines of our own (widgets-stage0 decision 2).
// format.ts: every number shown to a learner goes through Intl.NumberFormat('en-GB') with tabular figures; U+2212 for minus.
```

### 5.12 App stores

Small modules of signals in `src/app/stores`. Each exposes read-only signals and named actions; no component writes another domain's signals.

| Store | Holds | Written by |
|---|---|---|
| `settings` | theme, motion, sound, haptics, single-key shortcuts, tutor on, mascot on, study-day hour, weekly goal, streak mode | `set` events through the append queue; the `localStorage` mirror for theme and motion |
| `progress` | `derived: ReadonlySignal<DerivedState>` (assessment 13.3) and selectors: streak, XP today, MP, due counts, lesson status, mastery | the append queue (single events) and the data worker (rebuilds) |
| `content` | manifest, loaded course bundles by id, glossary | the content loader |
| `session` | current lesson or paper, writer status, active-time tracker | the player, `engine/progress/time.ts` |
| `tutor` | availability, consent state, usage counts | `TutorService` (ai-tutor 6.1) |
| `connectivity` | online, update available (web), Python status | platform lifecycle, service worker client, Python runtime |

### 5.13 Worker RPC

```ts
// src/engine/rpc.ts. About 100 lines; requests carry an id; replies resolve or reject; an AbortSignal posts a cancel.
export type RpcApi = Record<string, (...args: never[]) => Promise<unknown>>;
export function connect<A extends RpcApi>(worker: Worker): { call: <K extends keyof A>(m: K, ...a: Parameters<A[K]>) => ReturnType<A[K]>; close(): void };
export function serve<A extends RpcApi>(api: A): void;   // inside the worker

export interface DataWorkerApi extends RpcApi {
  validateCourse(hash: string, bytes: ArrayBuffer): Promise<{ ok: true } | { ok: false; path: string; message: string }>;
  rebuild(input: { snapshot?: ArrayBuffer; events: ArrayBuffer; release: string }): Promise<ArrayBuffer>;   // derived state, structured-cloned
  search(stage: 0 | 1 | 2 | 3, query: string): Promise<{ id: ContentId; title: string; kind: string }[]>;
  packExport(): Promise<ArrayBuffer>;
  validateImport(text: string): Promise<ImportReport>;          // assessment 14.2 step 2
  decodeResultCode(code: string): Promise<{ ok: true; events: Json[] } | { ok: false; reason: string }>;
}
```

The Python and SQL workers speak their own message protocols (section 6.3), because their runs stream events and must be terminable mid-run.

### 5.14 Scenes

Added for `docs/PLAN.md` (its section 3.2 and conflict 1). A scene is a composite written as data: a layout of primitive nodes, a pure model that derives every value shown, and typed bindings between them. `defineScene` turns it into the `WidgetLogic` of section 5.3, and the generated cluster entry pairs that logic with the generic `SceneView`, so the host, the compiler, the tutor, content and every test suite treat a scene exactly as they treat a hand-written composite.

```ts
// @zq/contracts/src/scene.ts
/** The five sources a scene binds to: config, prepared constants, answer state, view state, derived values. */
export interface SceneSrc<C, K, A, V, D> { c: C; k: K; a: A; v: V; d: D }
/** Dotted paths into T, checked by the type system ('d.point.x', 'a.theta'). */
export type PathOf<T> = /* recursive template-literal path type, depth at most 5 */ string;
export type Bind<S, T = unknown> = PathOf<S> | { from: (src: S) => T };      // a path, or a named pure function written in scene.ts
export interface Write<S, A, V, T> {                                          // controls write answer or view state only
  path: PathOf<{ a: A; v: V }>;
  from?: (value: T, src: S) => Json;                                          // e.g. a dragged point to an angle
}

export type SceneNode<S, A, V> =
  | { id: LocalId; prim: PrimType; props: Bindable<S>;                                          // any primitive or input other than the three below
      children?: SceneNode<S, A, V>[];                                                          // HostPrim only
      writes?: Write<S, A, V, Json>;                                                            // WritingPrim only
      answer?: true; tryable?: true; visibleWhen?: Bind<S, boolean> }
  | { id: LocalId; prim: 'marks'; type: MarkType; data: Bind<S>; style?: Bindable<S>; table?: true; visibleWhen?: Bind<S, boolean> }
  | { id: LocalId; prim: 'live-formula'; tex: string; slots: Record<string, Bind<S>> }
  | { id: LocalId; prim: 'value-table'; rows: Bind<S>; columns: { key: string; label: string }[]; table?: true }
  | { layout: 'row' | 'column' | 'stack' | 'grid' | 'overlay'; gap?: SpaceToken; children: SceneNode<S, A, V>[] }
  | { id: LocalId; embed: `${string}@${number}`; config: Bind<S>; state: PathOf<{ a: A; v: V }> };   // another scene, or a bespoke composite's controlled component

export interface SceneDef<C extends BaseConfig, K extends Json, A extends Json, V extends Json, D extends Json> {
  readonly type: string; readonly v: number; readonly cluster: ClusterId;
  readonly answers: readonly AnswerType[]; readonly stateVersion: number;
  readonly tweenable?: readonly (keyof V & string)[];
  readonly needs?: WidgetLogic<C, A, V>['needs'];
  prepare?(config: C): K;                                    // once per config: paths, grids, constants; layers binding only c and k are static
  init(config: C, seed: SeedSource): WidgetState<A, V>;
  derive(config: C, k: K, s: WidgetState<A, V>): D;          // pure; once per state change; at most 2 ms P95 at 4x throttling
  readonly layout: SceneNode<SceneSrc<C, K, A, V, D>, A, V>;
  answer(config: C, s: WidgetState<A, V>, d: D): Answer | null;
  describe: { brief: string; full?: string };                // templates over {c.*}, {k.*}, {a.*}, {v.*}, {d.*}; node phrases are appended
  exports?: readonly PathOf<{ d: D }>[];                     // template values content may use
  recipes?: Record<string, DeclarativeRecipe | ((config: C, s: WidgetState<A, V>, args: Record<string, Json>) => MotionStep[])>;
  secret?(config: C, s: WidgetState<A, V>, d: D): string | null;
  solved?(config: C, s: WidgetState<A, V>, key: Json): WidgetState<A, V>;
  migrate?: WidgetLogic<C, A, V>['migrate'];
  overrides?: Partial<Pick<WidgetLogic<C, A, V>, 'dirty' | 'summarise' | 'marks' | 'predicates' | 'targets' | 'table' | 'tryValue' | 'resolvers' | 'elementMeta'>>;   // at most 3
}
/** Node-safe: imported by registry.node.gen.ts, the compiler and CI. */
export function defineScene<C extends BaseConfig, K extends Json, A extends Json, V extends Json, D extends Json>(def: SceneDef<C, K, A, V, D>): WidgetLogic<C, A, V> & { readonly scene: SceneDef<C, K, A, V, D> };
```

Builders in `src/widgets/scene/build.ts` (`plot2d`, `plot3d`, `marks`, `dragPoint`, `slider`, `stepper`, `tokenTray`, `liveFormula`, `valueTable`, `row`, `column`, `stack`, `grid`, `overlay`, `embed`) return these nodes with their types inferred, so a scene reads as a short layout (`docs/PLAN.md` 3.2 shows one).

**Node kinds.** `HostPrim`, the primitives whose controlled component hosts child layers: `plot-2d`, `plot-3d`, `number-line`, `cell-grid`, `node-link`, `array-strip`, `matrix`, `price-ladder`, `cashflow-timeline`, `span-track`. `WritingPrim`, the primitives and inputs that change state: every one except `marks`, `live-formula`, `value-table`, `code-surface`, `diff-view` and `text-terminal`, which only display. `src/widgets/scene/nodes.ts` encodes both lists, the builders' types enforce them, and a test checks that every primitive and input is in the table.

**What `defineScene` generates.**

| `WidgetLogic` member | From |
|---|---|
| `tier` | always `'scene'` |
| `init`, `answer`, `secret`, `solved`, `migrate` | the scene's own functions (`answer` and `secret` receive `derive`'s result) |
| `dirty` | answer state differs from `init` with the same seed, unless overridden |
| `answerObjects` | element ids of nodes marked `answer` |
| `staticTargets`, `targets` | each node's primitive targets, named by node id under the `kind:name` rule (`handle:p`, `mark:arc`, `cell:3,4`); the scene suite fails on a collision; at most 40 |
| `describe` | the scene's template, then each visible node's phrase from its primitive; brief at most 300 characters, full at most 2 KB |
| `table` | marks and value tables marked `table` |
| `tryable`, `tryValue` | control nodes marked `tryable`, set through their `writes` path |
| `summarise` | the changed control's label and new value |
| `exports` | the declared `d.*` paths |
| `recipes` | declarative steps (`set` on `v.*` paths in `tweenable`, `highlight`, `annotate`, waits) or named functions |
| `predicates`, `marks`, `resolvers`, `elementMeta` | overrides only |

**`SceneView`** (in `src/widgets/scene/`, the widgets layer, because it imports primitives' controlled components). One computed signal per instance holds `derive(config, k, state)`; every bound property is a computed signal over the five sources; a node whose bindings read only `c.*` and `k.*` renders inside a memoised `Layer`, so a drag frame never diffs it (section 2.5 rules 1 and 2 hold by construction). Control nodes call `api.change` during a gesture and `api.commit` at its end for `a.*` writes, and `api.view` for `v.*` writes, which never engage Check. Pointer, keyboard and tap-then-tap paths are the primitives' own. Dense marks go to `CanvasLayer` by the marks primitive's own threshold.

**Tests.** Every scene runs the generic contract suite (section 8.1.1) and the generic browser suite over its fixtures, plus the scene suite: every binding resolves for every fixture state; every `writes` path lies in `a` or `v`; `derive` returns equal results on repeated calls and stays within 2 ms P95 at 4x; a render probe shows no static node re-rendering during a drag; templates resolve; generated targets include every `staticTargets` id. A scene has no per-scene browser test file and no CSS. Model functions that `derive` calls live in `@zq/models` or `@zq/mathcore` with unit, property and Python parity tests.

**Limits.** A `scene.ts` above 400 lines, or one needing more than three overrides, becomes a bespoke composite; so does a composite that needs free text or code editing, a clock-driven loop, a service with its own state machine, a gesture no primitive offers, or that fails the frame budget as a scene (`docs/PLAN.md` 3.2 rule 3). The pull request names the reason.

---

## 6. Build targets

### 6.1 One configuration, three modes

`vite.config.ts` reads the mode (`web`, `artifact`, `dev`) and sets:

| Setting | Web | Artifact | Why |
|---|---|---|---|
| HTML entry | `html/web.html` | `html/artifact.html` | Different heads: web manifest, CSP meta and self-hosted fonts against Google Fonts, the import map and no manifest |
| `base` | `/zero-to-quant/` (GitHub Pages) or `/` (local), from `VITE_BASE` | `./` | The Artifact references published files by relative path [sourced] |
| `define` | `__TARGET__ = 'web'` | `__TARGET__ = 'artifact'` | Dead-code elimination removes the other platform |
| `build.target` | `es2022` | `es2022` | Section 3.3 |
| `build.cssCodeSplit` | `false` | `false` | Decision 9 |
| `build.modulePreload.polyfill` | `false` | `false` | No inline polyfill script |
| `build.assetsInlineLimit` | 4 KB, never fonts or `.wasm` | same | Fonts load as own files, not `data:` URIs, whose font policy in the Artifact is [unverified] |
| `build.sourcemap` | `hidden`, kept as CI artefacts only | off | Source maps would cost Artifact files and bytes |
| Chunk names | `assets/[name].[hash].js` | same | Content-addressed, immutable |
| Service worker | `vite-plugin-pwa`, `injectManifest`, `src/sw/sw.ts` | none | No service workers in the Artifact [sourced] |
| Python files | `py/314.0.7/` in Pyodide's native layout | none (revision 2) | The publishing rule |
| Third-party modules | bundled into our chunks | external: bare names left for the page's import map, full URLs in the data worker, both from `cdn.lock.json` (`vite-plugin-zq-cdn`, section 6.2.7) | The publishing rule |
| KaTeX output | `htmlAndMathml`, KaTeX fonts self-hosted | `mathml`, no KaTeX CSS or fonts | Decision 37 |

Chunking follows decision 8. Dynamic `import()` of `src/widgets/clusters/<cluster>.ts` makes 26 widget chunks; four screen groups (home: Today, Learn, Course, Review, You; assessment: practice, redo, homework, exam, daily, weekly; records: plan, log, notebook, search, import, settings; onboarding) and the tutor are lazy; On the web, KaTeX, MathLive, the Compute Engine parser and MiniSearch each get a named chunk; in the Artifact they are lazy CDN imports and MathLive is absent. `build.rolldownOptions.output.codeSplitting.groups` puts modules shared by two or more widget clusters into the `w-core` chunk and modules shared by two or more screen groups into the entry, so no small shared chunks appear and widget code never inflates the first load (decision 8); the chunk count is a budget (section 6.2.5), so the configuration is tested, not trusted. Workers are bundled from `new Worker(new URL('../workers/x.worker.ts', import.meta.url), { type: 'module' })`.

Content: `zq build` writes `dist/content/`; a small Vite plugin (`vite-plugin-zq-content`) copies it into the target's `content/` folder, writes the manifest as `content/manifest.<hash>.json`, and injects `<meta name="zq-manifest" content="content/manifest.<hash>.json">` into the page, so the page and its content are pinned together while no app chunk changes when only content does (decision 30). In `dev` mode the same plugin serves the manifest from memory and pushes changes (section 10.3). A CI check builds twice with one changed lesson and asserts that only the page, the manifest and that course's files differ.

### 6.2 The Artifact

#### 6.2.1 Layout

```
dist/artifact/
├── index.html                            the page, rewritten as a fragment by tools/release/page.ts
├── version.json                          the release id at a stable path (section 7.2)
├── assets/
│   ├── app.<hash>.js                     shell, engine, ui, player, Bertie; no third-party code (revision 2)
│   ├── app.<hash>.css                    tokens, base, every component and widget style, math.css
│   ├── s-home.<hash>.js  s-assess.<hash>.js  s-records.<hash>.js  s-onboarding.<hash>.js
│   ├── tutor.<hash>.js
│   ├── w-<cluster>.<hash>.js             26 widget clusters
│   └── data.worker.<hash>.js             the only worker; its libraries come from the CDN
└── content/                              CONTENT-FORMAT.md 8.2; manifest.<hash>.json, named by the page's meta tag
    ├── course/<crs>.<hash>.json  gen/<top>.<hash>.mjs
    ├── search/<stage>.<hash>.json  glossary.<hash>.json  notebook.<hash>.json
    └── assets/<name>.<hash>.svg
```

Draft 1's `fonts/`, `sqlite/`, `py/314.0.7/` and `lib-*.js` files are gone (revision 2): they were third-party code or binaries.

#### 6.2.2 The page

The host wraps the published page in its own document skeleton [sourced: Artifact tool contract], so `tools/release/page.ts` rewrites Vite's `index.html` into the fragment form the prototype and the spikes used: `<meta charset>`, `<title>Zero to Quant</title>`, the Google Fonts `<link>`s, the app stylesheet `<link>`, `<div id="app">`, the old-browser gate as a classic inline script (it writes its message into `#app` and sets a flag; stage 1, `docs/DECISIONS.md` B8), the `<script type="importmap">` written from `cdn.lock.json` (section 6.2.7), and a classic inline bootstrap, which returns at once when the gate's flag is set and otherwise calls `import('./assets/app.<hash>.js')` (the path the Artifact probe measured: a page-level dynamic `import()` of an own module file; no `<script type="module">` is relied on). The tokens define light and dark colours on `:root` guarded by `:root:not([data-theme="light"])` and `:root[data-theme="dark"]`, and `body` has an explicit background (both already true of `prototype/css/tokens.css`).

#### 6.2.3 Fit with the host's rules

| Host rule [sourced] | How the build complies | Status |
|---|---|---|
| Scripts only from the listed CDNs or own files | Our own files, plus third-party ES modules from cdnjs or jsDelivr at exact versions through the import map (section 6.2.7) | Page-level dynamic `import()` of an own `.mjs` [measured by the Artifact probe on the owner's iPhone, section 14 item 1]; module workers [measured by the owner's spike]; the import map, CDN modules on the page and in a module worker, and import-map `integrity` [measured: S1, 7 October 2026] |
| Publishing rule: the session reads every file it did not write; nothing unreadable is published (the owner's correction, revision 2) | Every published file is generated by the session's own build from the repository's sources: app chunks, the stylesheet, content bundles, generator modules, the page and `version.json`; `tools/release/provenance.ts` fails the build on any `node_modules` module or binary | Enforced |
| Stylesheets only from Google Fonts or own files | One own stylesheet; Google Fonts for Archivo, Besley, Source Code Pro; no KaTeX CSS (MathML output needs none) | KaTeX 0.19.0's MathML lays out natively in the system maths font, and the owner accepted the 40-formula specimen on his iPhone [measured: S1, 7 October 2026] |
| Fonts | No own font files: Google Fonts for text, the system's maths font for MathML (`math.css`) | Decided (decision 37); Archivo and Source Code Pro load from Google Fonts in the frame [measured: S1, 7 October 2026]; Besley was not tried |
| No fetch to other hosts | Content is own files; the tutor uses `sample`; CDN modules arrive as scripts, never by `fetch`, so nothing probes a CDN at run time | Measured for `.json` |
| Served types only | `.html .js .mjs .css .json .svg` only; `tools/release/budgets.ts` fails on any other extension, on any `.wasm`, and on a root `preflight.js`, which the host reserves [sourced: Artifact tool contract] | Enforced |
| 16 MB per text file, 15 MB per binary | No binaries; the largest files are course bundles of a few MB | Enforced |
| No service worker, iframe, `window.open`, print | None used; handoff is an anchor or a copy button | Enforced by lint (`zq/no-forbidden-apis`). In the frame `window.open` returned `null` and nothing opened, while an anchor with `target="_blank"` opened a browser and `clipboard.writeText` from a tap copied a link [measured: S1, 7 October 2026] |
| Downloads only through `downloads` | `FileSaver` uses it | |
| WebAssembly | None published (draft 1's Pyodide and SQLite are web only) | Decided |
| The `assets` store | Not used for app or content files: declaring `assets` makes the artifact organisation-internal and unshareable by public link [sourced: `assets.d.ts`] | Decided |

#### 6.2.4 Capabilities

Declared at publish: `sample`, `db`, `user`, `downloads`. The `db` rule set belongs to `ASSESSMENT.md` 12.5 (its decision 32) and is adopted unchanged; this paper adds one rule, for the release signal (decision 32 here). This paper's first draft declared a different root rule (`read: "admin", write: "admin"`), which would have let Editors write shared data and contradicted the owning paper; it is withdrawn.

```js
capabilities: {
  db: { rules: [
    { path: '', read: 'interact', write: 'owner' },          // assessment 12.5
    { path: 'data/users/{self}', write: 'interact' },        // assessment 12.5: each person's private progress
    { path: 'board', read: 'interact', write: 'owner' },     // assessment 12.5: the friends board
    { path: 'board/{self}', write: 'interact' },             // assessment 12.5
    { path: 'meta', read: 'view', write: 'owner' },          // this paper: meta/release, readable by every admitted viewer, written only by the owner
  ] },
  user: { scopes: ['profile'] },                             // assessment 12.5 [sourced: user.d.ts]
  sample: {},
  downloads: {},
}
```

`ops/selftest-<release>` (section 6.2.6) falls under the root rule: the owner writes it, Contributors can read it, and it holds no personal data. The `{name: config}` form and the `db` and `user` entries are [sourced: `db.d.ts`, `user.d.ts`]; `sample: {}` was accepted and stored as sent, and the probe's declaration (this rule set plus one canary rule, `user` with `profile`, `sample: {}`) was in effect on the host [measured: S1, 7 October 2026: the canary refused the owner's write to a sibling's path]. The `downloads` entry is open: `{}` here, `true` in runtime contract 0.2.73 [sourced: the `artifact-capabilities` skill], a conflict that stage 83 settles against the skill (`STATE.md` open question 15). The `artifact-capabilities` skill is still loaded before the first publish that declares capabilities (the Artifact tool requires it), and the declaration is checked against it then.

#### 6.2.5 File and size budget

Recomputed by revision 2: no Python, SQLite, KaTeX fonts or library chunks; 103 course bundles and 26 topic generator modules for the adopted curriculum (`docs/CURRICULUM.md` 0.1).

| Group | Files | Raw size | Basis |
|---|---|---|---|
| Page, entry script, stylesheet, `version.json` | 4 | | section 7.2 |
| Screen groups and tutor | 5 | | |
| Widget clusters, `w-core` among them | 26 | | decision 8 |
| The data worker | 1 | | |
| **App** | **36** | **at most 12 MB** | about 8 MB [inferred from the gzipped budgets of section 9.2] |
| Third-party libraries | 0 | | loaded from the CDNs in `cdn.lock.json` (section 6.2.7) |
| Content manifest, search indexes (4), glossary, notebook, skill graphs (4), curriculum, plan | 13 | under 6 MB | content-format 8.2 |
| Course bundles | 103 | 80 to 115 MB | 2,445 lessons at about 27 KB each plus items and recorded output [scaled from draft 1's 70 to 100 MB for 2,148 lessons] |
| Generator modules, one per topic | 26 | under 12 MB | 26 topics |
| Assets of 8 KB or more | at most 20 | under 4 MB | content-format 8.2 |
| **Content** | **about 162** | **at most 130 MB** | |
| **One release** | **about 198** | **about 125 MB** | |

**Turnover.** Hashed names cascade: a changed entry chunk changes the import specifiers inside every lazy chunk that imports from it, so an app release renames about 36 files (up to 12 MB). A content-only release renames the page, the manifest and the touched course files only (decision 30). A third-party version change renames no published file except the page, whose import map changes.

**Limits** [our choice]. `tools/release/budgets.ts` checks the one-release row on every build, failing it and naming the largest groups; the retained-version and peak rows need the previous release's ledger, so `tools/release/artifact-plan.ts` checks them when it writes the publish plan (stage 83; `docs/DECISIONS.md` B7):

| Limit | Files | Size | Why |
|---|---|---|---|
| One release | at most 230 | at most 150 MB (app 12, content 130, margin 8) | Room for growth inside the two limits below |
| Retained version: this release plus the files only the previous release uses, after garbage collection | at most 300 | at most 200 MB | Rollback (section 6.2.6 step 7) finds the previous release in place, and a page opened before the release that the host did not reload still loads its lazy chunks if its own-file fetches reach the newest version, which S1 could not measure (section 8.2; `docs/DECISIONS.md` B28). The host reloaded the open page after each publish [measured: S1, 7 October 2026] and reloads other open views [sourced: `artifact.d.ts`, contract 0.2.73], but a backgrounded app, a second device and the desktop and web viewers were not measured [unverified] |
| Peak, while a release is staged | at most 480 | at most 250 MB | The host allows 511 files and 256 MB per version [sourced]; the margin absorbs a miscount |

A release whose peak would exceed the last row becomes a maintenance release (section 6.2.6): expected only for a format-wide re-emit of every course (up to 130 MB renamed at once), not for ordinary releases (about 270 files and 150 MB at peak: one release, the previous release's 36 renamed app files, and the next release's 36).

**What runs where.** Every Python, SQL and C++ drill runs on the web app; the Artifact's `PythonRuntime` answers `not-in-this-build`, so the drill screen offers the web app with a result code (assessment 14.3). Section 6.3.3 keeps draft 1's measured Python layout as a record.

**Size budgets per file** are in section 9.

#### 6.2.6 Release procedure

Publishing an Artifact is a Claude tool call, not a CI step, so a release is a plan a Claude session executes. The owner, not the session, runs the checks on the live page: a cloud session cannot operate the page inside the owner's Claude app. Releases run in fresh cloud sessions, so nothing a release needs may live only in ignored build output.

**What a publish does** [measured: S1, 7 October 2026, on the owner's iPhone, unless tagged otherwise]. The tool refuses a publish without the page, and one of more than 255 `files` entries with `null` removals counted, and then publishes nothing. Each accepted publish S1 sent made a new version; omitting `capabilities` carried the stored declaration forward. After each publish the host reloaded the page open in the foreground to the newest version, about 4 s and 1 to 2 s after the two publishes (a second-resolution version stamp against the phone's clock), between the batches of one release too, so the open page was shown every intermediate version of S1's two-batch release. Other open views reload too [sourced: `artifact.d.ts`, contract 0.2.73], and the host's page-design guidance says published changes reach open viewers "automatically at their next quiet moment, with state preserved where possible" [sourced: the Artifact tool's page-design guidance, read 7 October 2026; quoted in `docs/DECISIONS.md` section 4]; a backgrounded app, a second device and the desktop and web viewers were not measured [unverified], so a page left on an older version stays possible (section 12 risk 14). A fresh load serves the added files and not the removed ones. The own files S1 fetched carry `cache-control: private, max-age=31536000, immutable, no-transform` and gzip. The procedure below follows from these results (`docs/DECISIONS.md` B24).

**Learner work across the reload.** The host's reload ends the page wherever the learner is, mid-lesson or mid-paper, and whether `pagehide` or `visibilitychange` fires before the reload ends the page is [unverified: S1 did not record it]. So nothing that counts waits in memory: `ProgressStore.append` resolves only once the event is in IndexedDB, and the outbox carries the `db` write across the reload (assessment 13.4); the current route and every pending draft (a lesson widget's, a homework set's, a paper's answers) are also written synchronously to `sessionStorage`, which survived the host's reload [measured: S1, 7 October 2026: runs `muyonw26` and `muyoo2d3` read the previous run's id from it], and the restarted page restores the newer copy [our choice], as `artifact.d.ts` 0.2.73 advises for unsent input across a reload [sourced] (`docs/DECISIONS.md` B22). A paper's or homework set's lease is owned by the device and tab identity kept in `sessionStorage`, so the reloaded page re-acquires its own lease at once instead of waiting out its term while the paper's clock runs; the owner key is checked against `db.d.ts`'s `acquire` semantics when the store is built (assessment 13.7; `docs/DECISIONS.md` B26). These are built and tested at `docs/PLAN.md` stages 10a (widget drafts, `DraftStore.mirror`), 69 (homework and paper drafts through `ProgressStore.draft`, and the lease) and 74a (the route). The host also offers `window.claude.hot`, the viewer's own update hook: a page registers `snapshot(...)` before an update and boots through `ready(start)`, or reads `data` on start [sourced: the Artifact tool's page-design guidance, read 7 October 2026; quoted in `docs/DECISIONS.md` section 4]. If it fits, the page also hands it the open screen before the update and restores from it after; stage 83 reads that contract before relying on it, and the `sessionStorage` mirror stays the floor.

1. **The release ledger.** `npm run release:artifact` builds content and app from the tagged commit, runs the budgets, and writes `releases/<release>.json`: every path the release publishes with its SHA-256 and size, the page's hash, the manifest's name and the release id. The ledger is committed in the release pull request and reviewed there; CI builds twice and checks that both builds match it. The same command writes `dist/artifact/publish-plan.json`, an ordered list of publishes, each at most 255 entries with the page and every removal counted (the tool counts `null` removals against its 255 `files` entries [measured: S1, 7 October 2026]; counting the page too is our choice, and 254 `files` entries plus the page, 255 counted our way, were accepted) and 64 MB [sourced], each with a `files` map, the paths to remove (`null`), a label, and the page it re-sends, named by role: `page: 'previous' | 'new' | 'maintenance'`. Staging publishes carry `previous`, the new-page publish `new`, garbage-collection publishes `new`, and a maintenance release's publishes before its new page carry `maintenance`, and its new-page publish `new` (step 6); `docs/PLAN.md` stage 83's planner tests assert each (`docs/DECISIONS.md` B24). The plan is derived from the new ledger and the previous one, so any session can regenerate it.
2. **Build and verify in the session.** The release session checks out the tag, rebuilds every file itself from the hash-pinned inputs (`package-lock.json`, `cdn.lock.json`), and checks each file's SHA-256 against the committed ledger; it publishes only bytes it built from the repository's own sources and verified, and it reads in full every text file it writes by hand or that no reviewed source produced (the page fragment with its import map, `version.json`, the publish plan). Under the owner's publishing rule (revision 2) no published file is third-party code or a binary, so draft 1's question to Anthropic is withdrawn.
3. **Before the first publish** the session lists the live artifact's files (`scope: "files"`) and compares them with the **previous release's committed ledger** (named by the hash in `meta/release`). Any difference stops the release: the Artifact tool refuses to replace paths the session has neither read, listed nor published, and a difference means someone published in between.
4. **Order.** The host reloaded the open page into each version S1's release made (above), so each version must be a working app. First the new content files (new names, nothing referencing them yet). Each of these staging publishes re-sends the **previous** release's page, the one still live, byte for byte (`page: 'previous'`), because the tool refuses a publish without the page [measured: S1, 7 October 2026], so a reloaded page comes back on the release it was on [inferred: S1's first v2 batch already carried the new page, so no staging publish was tried]. Before the first staging publish the session reads the live `index.html` with the Artifact tool's `path` read and checks its SHA-256 against the previous ledger's page hash; it then re-sends exactly those bytes, and a mismatch is step 3's drift stop [our choice: the tool publishes only what the session read or wrote, and step 2 rebuilds only the new release's files]. Then the publish with the new page, `version.json` and the app files (`page: 'new'`, the moment the release goes live); the page and `version.json` change only in this publish, so no staging version reports a release it does not run. Then the session writes `meta/release` (`{ release, at, ledger: <SHA-256 of the ledger> }`) with `ArtifactData`, which raises the update notice on a page the host did not reload (decision 32). Last, garbage-collection publishes, each re-sending the new page (`page: 'new'`), remove every path that neither the new ledger nor the previous one names, in as many publishes as the removals need at 255 entries each. No publish passes `capabilities` or `contract` unless the release changes the declaration (it then goes with the new page) or moves the runtime contract on purpose (S1's probe was written against contract 0.2.73's type definitions [sourced: `spikes/s1/CONTRACT.md`], and the runtime version it was served was not recorded; 0.2.74 exists [sourced: the publish result and the `artifact-capabilities` skill, 7 October 2026]).
5. **Resume.** A session that dies part-way is replaced by one that re-runs the procedure from the first step whose effect is not yet visible: staged files missing from the listing are published again (content-addressed, so a repeat changes no file; that it still makes a version and reloads open pages is [inferred]: S1 sent no identical repeat); a listing that holds the new page but a `meta/release` that still names the old ledger resumes at the `meta/release` write; a `meta/release` naming the new ledger with old files still listed resumes at garbage collection. Drift in step 3 is then judged against the union of the previous ledger and the new ledger's already-published paths.
6. **Peak check.** The plan computes the version's peak (retained plus new files). Above the peak limit of section 6.2.5, the plan becomes a **maintenance release**: publish a small page that says "Zero to Quant is updating. Your progress is safe; come back in a few minutes." with the first removals (`page: 'maintenance'`), then remove the rest of the old files and upload the new files in publishes that each re-send that page (`page: 'maintenance'`), then publish the new page (`page: 'new'`). Open pages reload to the small page at its first publish [inferred from S1's reloads].
7. **Rollback** publishes the previous ledger's page and app files, which the retained version still holds, and writes `meta/release` back to the previous ledger's hash.
8. **Self-test.** The owner opens Settings, Diagnostics, Self-test on the iPhone: capabilities present, the manifest named by the page fetched and its hash checked, one course bundle fetched and validated, every locked CDN module loaded through the import map (with the integrity result where the browser reports one), a formula rendered as MathML, a widget cluster loaded, a drill's handoff link built, `meta/release` equal to the page's own release. The page shows the result and writes it to `ops/selftest-<release>` in `db`; the session reads that document with `ArtifactData` and records it in the release checklist. Nothing is written to progress. Whenever a page is found on an older release, its Reload must bring it to the newest (section 14 item 14). A handoff link whose fragment carries a payload at the 8 KB limit is checked once, in `docs/PLAN.md` stage 82's iPhone handoff check (section 5.9; `docs/DECISIONS.md` B30).
9. The owner goes through the rest of the release checklist in `docs/engine/RELEASE.md` on the phone.

#### 6.2.7 Third-party modules from CDNs (revision 2)

1. **The lock.** `tools/cdn/lock.ts` reads `package-lock.json` and writes `cdn.lock.json`: for each runtime package the Artifact uses, the exact file our build imports (for example `preact@11.0.0/dist/preact.mjs`, `preact@11.0.0/hooks/dist/hooks.mjs`, `@preact/signals@2.11.3/dist/signals.mjs` (the `import` condition's file, which S1 locked and measured, not the `browser` condition's `signals.module.js` [our choice]), `@preact/signals-core@1.14.4`, `zod@4.6.5`'s `mini` and `v4/classic` entries, `katex@0.19.0/dist/katex.mjs`, the Compute Engine 0.148.0 `latex-syntax` entry, `minisearch@7.2.0/dist/es/index.js`, `ts-fsrs@5.4.2/dist/index.mjs`, `fflate@0.8.3/esm/browser.js`, `idb@8.0.4/build/index.js`), its URL, its SHA-384, the bare names it imports and where it loads (page or worker). The URL is cdnjs's when cdnjs serves a byte-identical file at that version, otherwise `https://cdn.jsdelivr.net/npm/<name>@<version>/<path>`; never a range, `@latest` or `+esm`. `unpkg.com` is the named alternative host if jsDelivr stops serving a path. Of 14 cdnjs URLs for seven locked entries, each imported with the npm file's hash in the import map, S1 found one byte-identical: KaTeX 0.19.0's `katex.mjs`, at `ajax/libs/KaTeX/0.19.0/katex.mjs` (its `dist/` path failed); Preact, `preact/hooks`, both signals packages, `zod/mini` and fflate failed to import at both paths tried, with a load error rather than an integrity mismatch [measured: S1, 7 October 2026], so those paths are not served [inferred]. jsDelivr is the host for every other locked file unless the lock tool finds a byte-identical cdnjs file. S1 tried two guessed paths per package and did not try classic zod, ts-fsrs, idb, MiniSearch or the Compute Engine entry, so the lock tool checks every locked file against cdnjs's listing, the tried ones included, and locks jsDelivr's URL for any file whose identity it cannot check (this sandbox cannot reach cdnjs).
2. **What the tarballs show** [measured on the npm tarballs, 7 October 2026]: Preact 11.0.0 ships ES modules only, and its `hooks` and `compat` entries import `preact` by bare name; `@preact/signals` 2.11.3 imports `preact`, `preact/hooks` and `@preact/signals-core`; the Compute Engine's chunks import `@cortex-js/compute-engine/integration-rules`; KaTeX's `katex.mjs`, MiniSearch, ts-fsrs, fflate, idb and zod's entries import only relative paths. Preact 10.29.8 ships UMD builds.
3. **The page.** `tools/release/page.ts` writes one `<script type="importmap">` into the page fragment, before the bootstrap: `imports` maps every bare name our chunks and the locked libraries use to its URL, and `integrity` maps each URL to its SHA-384. The Artifact build (`vite-plugin-zq-cdn`) marks those packages external, so our chunks keep bare names and the browser resolves them through the map, for static imports and for the bootstrap's dynamic `import()`: S1 measured both on the owner's iPhone, each resolving to the locked jsDelivr URL, and two wrong-hash entries refused beside a control that loaded [measured: S1, 7 October 2026]. Lazy libraries (KaTeX, the Compute Engine parser, MiniSearch) are dynamic imports through the same map.
4. **Workers.** Import maps do not reach workers [recalled], so the data worker's third-party imports (classic zod, ts-fsrs, fflate, all free of bare imports) are rewritten to their full locked URLs at build time. No integrity applies there. S1's module worker imported all three from jsDelivr by full URL and ran each, ts-fsrs and fflate giving Node's results [measured: S1, 7 October 2026], so section 14 item 19's main-thread fallback is not needed.
5. **Checks.** `provenance.ts` fails the Artifact build if any published JavaScript file has an input under `node_modules`: it reads Rolldown's module graph for every app chunk and the data worker, and esbuild's metafile for every generator module, which the content compiler builds outside Rolldown (second review round; a planted import in a fixture generator fails it at stage 4); CI's emulator serves the locked URLs from local copies checked against `cdn.lock.json` (section 8.2), so tests never depend on a live CDN; the nightly `drift.ts` job fetches every locked URL and fails on any byte difference, which blocks Artifact releases until the file is re-pinned.
6. **Named fallback**, not used: S1 found the import map honoured, so items 1 to 5 stand [measured: S1, 7 October 2026]. If the page ever ignored the map: Preact 10.29.8 and `@preact/signals` (with `@preact/signals-core`) load as UMD classic scripts with `integrity` attributes, generated shims (our code) re-export their globals, and the libraries free of bare imports load by full URL as in the worker. Preact 10.29.8 already ran the frame benchmark unchanged (decision 3), and S1 ran this path on the iPhone: the four scripts loaded with `integrity`, rendered with `useState`, updated on a signal change, and a wrong hash was refused at two URLs [measured: S1, 7 October 2026].
7. **Request cost of `zod/mini`** (S1's finding, for stage 4). The browser loads a CDN module's whole static closure: for `zod/mini` 4.6.5 that is 92 files [measured: S1, 7 October 2026], 788,560 bytes raw and 197,653 gzipped file by file, 64 of them (341,403 bytes raw) locales that `v4/mini/external.js` re-exports [measured: zod 4.6.5 npm tarball, zlib 1.3 level 9 through Python's `gzip`, 8 October 2026]. No public entry avoids them: `zod/v4/core` re-exports the same locales [measured: zod 4.6.5 npm tarball, 7 October 2026]. On the owner's iPhone the first, cold load of the static imports (Preact, its hooks, both signals packages and `zod/mini`) took 2,783 ms, and zod's 92 requests took 9,393 of the 9,646 ms of request time summed over the 96 CDN requests, the four Preact and signals files 253 ms; later loads took 36 to 47 ms, and 207 and 257 ms on the two pages the host reloaded during the republish [measured: S1, 7 October 2026] (the network was not recorded). Resource Timing reports zero sizes for the CDN files there (own files report theirs), so the bytes on the wire were not measured. The closure alone is above the 110 KB that section 9.2 allows the Artifact's entry with its CDN modules. Classic zod's `index.js` entry, which S1's module worker imported, is 95 files, 212,061 bytes gzipped file by file, 83 of them shared with `zod/mini` [measured: zod 4.6.5 npm tarball, zlib 1.3 level 9 through Python's `gzip`, 8 October 2026; files from S1's `cdn-lock.json`], so the worker's imports mostly reuse the page's cached files [inferred]. The options the publishing rule leaves are in `docs/PLAN.md` 4.3, and the choice is the owner's, `docs/PLAN.md` section 12 row 15, needed by stage 4; until he chooses, `zod/mini` stays as locked.

### 6.3 Python on the web app

#### 6.3.1 One worker

`src/workers/python.worker.ts` loads Pyodide 314.0.7 and runs drills with `grader.py` and `zqtest.py` (content-format 3.9). It exists in the web build only (revision 2); the Artifact's `PythonRuntime` is the handoff stub:

```ts
// src/workers/python/protocol.ts
export type ToPython =
  | { k: 'init'; loader: 'native'; base: string }                         // base: absolute URL of py/314.0.7/ (draft 1 also had 'split')
  | { k: 'load'; packages: PyPackage[] }
  | { k: 'run'; id: number; req: RunRequest }
  | { k: 'trace'; id: number; code: string; maxSteps: number };          // programming 2.3, live tracing
export type FromPython =
  | { k: 'progress'; step: string; done: number; total: number }
  | { k: 'ready'; python: string; packages: PyPackage[]; ms: number }
  | { k: 'test-start'; id: number; name: string }                        // the page's per-test watchdog starts here
  | { k: 'event'; id: number; e: RunEvent }
  | { k: 'figure'; id: number; png: ArrayBuffer; svg?: string }          // matplotlib, Agg backend
  | { k: 'done'; id: number; result: RunResult }
  | { k: 'failed'; code: 'network' | 'integrity' | 'memory' | 'crashed'; message: string };
```

- **Timeouts** (decision 31). The web app cannot send the cross-origin isolation headers that `SharedArrayBuffer` and Pyodide's interrupt buffer need: GitHub Pages sets no custom headers [recalled]. (A service worker could add the headers to the responses it serves [recalled]; rejected, because the first visit is not yet controlled by it.) Two levels instead:
  1. **Soft deadline.** `grader.py` registers a `sys.monitoring` callback for backward jumps on the learner's code objects; every 1,000 jumps it compares `time.monotonic()` with the test's deadline and raises `ZqTimeout` (a `BaseException` subclass), which the grader reports as `timeout` for that test. The worker stays warm and the next test runs at once. The efficiency probes' line counter (programming decision 10) runs separately under `sys.settrace`, only for the probe runs.
  2. **Hard watchdog.** The page expects a `test-start` and then an `event` for that test within its limit plus 1,500 ms; otherwise it terminates the worker, reports `timeout`, and restarts it, warm from the service worker cache. This catches long calls inside C code (a huge NumPy allocation), which never jump in Python bytecode.
- **Load stall.** While loading, a worker that sends no `progress` message for 30 s is terminated and reported as `failed: network`, with Retry (added by `docs/PLAN.md` 8.1).
- **Memory.** A `memory` failure or a crash restarts the worker once; a second failure sets `failed` and suggests the web app on a computer. The worker is terminated when the learner leaves a course, and after 10 minutes without a code screen. Loading a group drops nothing already loaded, so a lesson that needs `sklearn` after `numpy-pandas` adds to one interpreter; the memory each group adds is measured at E8 on the owner's phone (risk 4).
- **Core caching.** The service worker caches `py/<version>/**` cache-first (section 6.4.1), so a warm start fetches nothing; draft 1's `fetch` interception and `BlobCache` copies served only the Artifact's split layout.
- **Isolation.** Learner code runs only in this worker: no DOM, no storage of ours, no network beyond the loader's own files (programming 2.12).

#### 6.3.2 Web: the native loader

`loadPyodide({ indexURL: base })`, then `loadPackage(needs, { checkIntegrity: true })`. The web build copies Pyodide's core files and the wheels of the allowed packages into `py/314.0.7/` unchanged. `tools/pyvendor/fetch.ts` downloads the pinned release once (cached by CI), and checks every wheel against the SHA-256 in `pyodide-lock.json` before anything is copied.

#### 6.3.3 Artifact: the split-archive loader (measured; not adopted)

> **Not built (revision 2).** The owner's publishing rule lets the Artifact publish only files generated from this repository's own sources, and these parts are repackaged third-party binaries, so the Artifact has no Python and `tools/pysplit` is removed. The section stays as the record of a measured layout, with `spikes/README.md`; its sizes still describe the web app's wheels.

The spike's method (`spikes/pyodide-in-artifact`), with every published file genuinely its type, fewer files and fewer bytes (decision 16):

1. **Load groups.** Archives are grouped by what loads together, each group's closure taken from `pyodide-lock.json` minus the archives of earlier groups [measured]: `stdlib` (`python_stdlib.zip`); `numpy-pandas` (NumPy, pandas, python-dateutil, pytz, six); `scipy-statsmodels` (SciPy, statsmodels, patsy, packaging; SciPy's lock entry depends on NumPy only, so `libopenblas` is not in the closure); `sklearn` (scikit-learn, joblib, threadpoolctl); `matplotlib` (matplotlib, contourpy, cycler, fonttools, kiwisolver, pillow, pyparsing); `testing` (pytest and its 9 pure-Python dependencies, plus `hypothesis` and `sortedcontainers`; `hypothesis` comes from PyPI because Pyodide does not ship it). `engine/python/budget.ts` maps each `PyPackage` to its group.
2. **Members, not archives.** For every member the spike keeps (it drops `tests/`, `.pyi`, `.c`, `.h`, `.pxd` and `.a`), `split.ts` copies the member's bytes exactly as they sit compressed in the wheel, with its compression method, CRC-32 and both sizes from the central directory, and writes them as base64 into JSON parts of at most 8 MB: `{ "<archive>": { "<path>": [method, crc32, size, "<base64>"] } }`. Nothing is recompressed at build time and nothing is decompressed in JavaScript. Text and side modules (`.so`) are treated alike; the spike's base64 path for time-zone tables is the same mechanism, now used for every member.
3. **Manifest.** `py/314.0.7/manifest.json` lists groups, archives, the members of each archive in their original order, the part holding each, and the SHA-256 of every part.
4. **At run time** the worker replaces `self.fetch` before loading Pyodide (the spike's interception). A request for an archive name in the manifest is answered by fetching its group's parts, checking each part's SHA-256 with `crypto.subtle.digest`, and writing a zip in memory whose local headers carry each member's original method, CRC-32 and sizes, followed by the member's original compressed bytes and a central directory; the result returns as a `Response`. Python's `zipfile` inflates each member and checks its CRC-32 as Pyodide unpacks it. Pyodide loads with `checkIntegrity: false`, because the rebuilt archive's bytes differ from the wheel's; the per-part SHA-256 and the per-member CRC-32 replace that check. A mismatch is an `integrity` failure: the cached parts are dropped and fetched once more.
5. **Cache.** Rebuilt archives are stored in `BlobCache` (IndexedDB, in workers; S1 showed only that IndexedDB works in a module worker in the Artifact frame, with 100 small records [measured: S1, 7 October 2026], not this cache's archives) by archive name and manifest hash, so the second start skips the network and the rebuild. They are compressed archives, so the cache holds about 41 MB for the whole stack, not 142 MB. If the quota refuses, Python still runs, rebuilding each session.

Measured for Pyodide 314.0.7 in review (section 0.2), with the spike's strip rules; "Raw" is the members kept, uncompressed, which is what the first draft's layout and the spike publish; "Parts" is this layout:

| Group | Archives | Wheels | Raw kept | Side modules (`.so`) | Compressed members | Parts (base64) |
|---|---|---|---|---|---|---|
| `stdlib` | 1 | 2.5 MB | 9.6 MB | 0 | 2.5 MB | 3.3 MB |
| `numpy-pandas` | 5 | 7.9 MB | 27.3 MB | 58 | 7.3 MB | 9.8 MB |
| `scipy-statsmodels` | 4 | 22.4 MB | 54.7 MB | 133 | 15.3 MB | 20.4 MB |
| `sklearn` | 3 | 4.6 MB | 16.1 MB | 69 | 4.5 MB | 6.0 MB |
| `matplotlib` | 7 | 9.5 MB | 25.3 MB | 16 | 9.2 MB | 12.3 MB |
| `testing` (without `hypothesis` and `sortedcontainers`) | 10 | 2.7 MB | 9.4 MB | 0 | 2.5 MB | 3.3 MB |
| **Total** | **30** | **49.6 MB** | **142.4 MB** | **276** | **41.3 MB** | **55.1 MB** |

With the core (11.0 MB), the spike's layout for NumPy and pandas is 49 MB in 69 files, matching the spike's README; this layout is 24 MB in 8 files (core 5, stdlib 1, numpy-pandas 2), and the whole stack is about 67 MB in 15 files against 153 MB in about 311. If the host compresses responses, the transfer for NumPy and pandas is about 14 MB either way (the numpy-pandas parts gzip from 10.4 to 7.7 MB [measured]); if it does not, this layout halves the first download.

Measured on the owner's iPhone with the spike's layout for core, stdlib, NumPy and pandas: Python ready at 2.8 s, packages at 5.1 s, the calculation at 6.2 s (spike README). Draft 1 planned to re-run that calculation with this layout at S1 and named two fallbacks, F1 (the spike's own layout) and F2 (no Python in the Artifact); the owner's rule makes F2's outcome the design, so neither is built.

### 6.4 The web app

#### 6.4.1 Service worker

`src/sw/sw.ts`, built by `vite-plugin-pwa` 2.0.0 with `injectManifest` and Workbox 7.4.1:

| Request | Strategy | Cache |
|---|---|---|
| App files: entry, stylesheet, screen groups, tutor, all 26 widget clusters, lazy libraries, workers, fonts, SQLite | Precache (Workbox revision manifest) | `zq-app` (Workbox-managed) |
| `content/**` (hashed names) | Cache first; filled on first use, by prefetch, and by Keep offline | `zq-content`; on activate, entries not in the new manifest are deleted |
| `py/<version>/**` | Cache first | `zq-py-<version>`; other versions deleted on activate |
| The tutor proxy | Network only, never cached | |
| Navigations | The precached `index.html` | |

Precaching every widget cluster costs at most 2.1 MB gzipped once (26 clusters at the 80 KB budget of section 9) and means any course whose content is cached works offline.

**Offline courses.** The course map's "Keep offline" caches the course's bundle, generator module and assets, and offers the course's Python with its size ("Python for this course: 21 MB" for NumPy and pandas: the core files, `python_stdlib.zip` and five wheels, 21.4 MB as files [measured], less on the wire if GitHub Pages compresses the core). The first draft's 49 MB was the Artifact spike's uncompressed layout, which the web target never uses. The current course is kept automatically; Python is cached on the first drill run.

**Updates.** A new service worker installs in the background; `workbox-window` reports it waiting; the update banner shows on Today, the course map and Settings, never inside a lesson or paper: "An update is ready. Restart to use it." Restart sends `SKIP_WAITING` and reloads. A deferred update applies on the next cold start.

**Storage.** `navigator.storage.persist()` is requested at the first completed lesson; if refused, the weekly review reminds the learner to export (assessment 13.5).

#### 6.4.2 Content Security Policy

A `<meta http-equiv="Content-Security-Policy">` in `html/web.html`, because GitHub Pages sets no headers:

```
default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline';
font-src 'self'; img-src 'self' data: blob:; connect-src 'self' <tutor proxy origin>;
worker-src 'self' blob:; manifest-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'
```

- `'unsafe-inline'` for styles is needed because KaTeX's output carries inline `style` attributes; scripts allow no inline code and no `eval`.
- The Python worker is created from its own file, so the document's meta policy does not govern it; Pyodide's 6 `eval(` call sites [measured] run there.
- The tutor proxy origin comes from `VITE_ZQ_TUTOR_URL` at build time and is fixed for that build; Settings holds only the token (ai-tutor 6.3.6).
- No third-party origin is allowed: the GitHub and Codeforces API lookups that `ASSESSMENT.md` once planned are withdrawn (`docs/PLAN.md` conflict 5), so the proxy is the only host outside the app's own origin that a page can reach.

#### 6.4.3 Deploy

- `pages.yml` runs on a tag `v*`: `npm ci`, the full CI gate, `zq build`, `pyvendor fetch`, `vite build --mode web`, then the deploy to the web host of `docs/PLAN.md` 12 decision 13: under its default (b), `wrangler pages deploy` to a Cloudflare Pages project behind an Access policy admitting only the owner; under (a), the official GitHub Pages upload and deploy actions.
- **Locally:** `npm run serve:web` serves `dist/web` and starts the Node variant of the proxy on 127.0.0.1 (ai-tutor 6.3.7).
- The web manifest and icons come from `@vite-pwa/assets-generator` and the logo mark in `prototype/js/core.js`.

### 6.5 Development and preview builds

- **`npm run dev`.** The Vite dev server in `dev` mode with `WebPlatform`, development routes, content compiled on the fly from `content/` with hot reload (section 10.3), and the tutor through the local proxy when `.env` has a key.
- **`npm run dev:artifact`.** The same app with `ArtifactPlatform`, served by `tools/artifact-host` (section 8.2), which enforces the file-type allow-list and a CSP like the host's, has no service worker, and provides a fake `window.claude` (`sample` replays recorded replies or calls the local proxy; `db` is in memory with the declared rules enforced; `user` and `downloads` are fakes).
- **`zq preview --artifact`** (built at `docs/PLAN.md` stage 25; content-format 9.1 step 7). An Artifact build whose manifest holds one course (or the gallery), whose start route is a lesson, a level, a course or `#/gallery`, with the development routes compiled in (and no Python, as every Artifact build). A Claude session republishes it to **one long-lived private preview Artifact** (its URL in `STATE.md`) for each device gate, never creating a new one, so no preview needs deleting; each republish carries the page and counts its removals against the 255 entries [measured: S1, 7 October 2026] and reloads the owner's open preview page as S1's open page was reloaded [inferred]; the owner records the gate's result in its `db` at `ops/gate-<stage>` (`{ result: 'pass' | 'fail', notes, at }`), which the session reads with `ArtifactData`.

---

## 7. Content versioning and progress migrations

`CONTENT-FORMAT.md` 4 owns content identity, `rev`, the answer hash and `migrations.yaml`; `ASSESSMENT.md` 13 owns the event log and the fold. This section fixes the version numbers the engine adds and the compatibility rules between them.

### 7.1 Version numbers in play

| Number | Where it lives | Changes when | Reader behaviour on mismatch |
|---|---|---|---|
| Release (`2026.11.02.1`) | `version.json` (stable path), `meta/release` in the Artifact's `db`, the app build, the manifest, every event's `rel` and `app` | Every release; app and content share it (decision 30) | Section 7.3 |
| Content format (`zq: 1`) | Every bundle | A breaking change to the compiled format | "Update the app to open this course" |
| Widget major (`v`) | Widget configs in content; `logic.v` | A breaking config change | The compiler refuses content that names a major the app's registry lacks |
| Widget `stateVersion` | Each saved draft | The saved shape of `a` or `v` changes | `migrate`, else the draft is discarded with the note "Your unfinished work on this screen was reset after an update." |
| Lesson, item, drill `rev`; generator `v` | Content | content-format 4.2 | content-format 4.4 table; lesson drafts are keyed by `rev`, so an old draft never mounts on a new screen order |
| Event format (`v: 1`) | Every event | A breaking change to an event kind | Readers upgrade older events in memory; an event newer than the reader is quarantined (assessment 13.8) |
| Fold rules version | The data worker and `fold/` | Any change to XP, MP, streak, FSRS mapping or retention rules | A snapshot with another rules version is ignored and the state rebuilt from events (assessment decision 20) |
| Snapshot format | Each snapshot | Its own layout changes | Ignored and rebuilt |
| Export format (`v: 1`) | Export files, result codes (`ZQR1.`) | A breaking change | Import rejects with the first error (assessment 14.2) |
| Tutor `promptVersion` | `AI-TUTOR.md` 11.1 | The core prompt changes | Recorded on replies; no migration |
| Pyodide (`314.0.7`) | `py/<version>/`, cache names | A Pyodide upgrade (section 3.4) | Old caches deleted; drafts unaffected |

### 7.2 Compatibility rules

1. **One registry, checked at compile.** `zq build` reads `src/widgets/registry.gen.ts` and fails if content names a `type@v` the app does not register. A widget's old major stays in the library until no content uses it; the compiler lists the screens still on it, and a codemod moves them (content-format 3.5).
2. **Drafts are disposable; progress is not.** Lesson drafts (widget states mid-screen) are per device and may be discarded with a note; nothing that counts (attempts, completions, marks) lives in a draft.
3. **Content migrations apply in the fold on read** (assessment 13.9); stored events are never rewritten.
4. **Mixed versions across devices.** Every event carries `app` and `rel`. A device on an older app reads newer `v: 1` events normally (kinds and fields only grow within a format version) and quarantines anything newer than it knows. In the Artifact, the host reloaded the page open in the foreground on the owner's iPhone to the newest version after each publish [measured: S1, 7 October 2026], and other open views reload too [sourced: `artifact.d.ts`, contract 0.2.73], so a view runs an older page only if the host did not reload it [unverified: a backgrounded app, a second device and the desktop and web viewers were not measured].
5. **Update notice.** The web target fetches `version.json` (with a cache-busting query) when the page becomes visible, at most once an hour, and defers to the service worker's update flow. In the Artifact the host reloaded the open page itself after each publish [measured: S1, 7 October 2026], so the notice is for a page it did not reload (item 4). The page subscribes once to `meta/release` (decision 32), which reached the open page about 3 s after the write's timestamp (cross-clock, a hint) [measured: S1, 7 October 2026], and polls `version.json` as a fallback when `db` is absent, with a fresh query and `cache: 'no-store'`, because the own files S1 fetched carry `cache-control: private, max-age=31536000, immutable, no-transform` [measured: S1, 7 October 2026] (`docs/DECISIONS.md` B24). A newer release shows "A new version is available. Reload to continue." outside lessons and papers; Reload calls `location.reload()` [our choice], which reloaded a page already on the newest version (v2 to v2) from the same base path with `sessionStorage` intact [measured: S1, 7 October 2026]. Whether it brings a page on an older version to the newest is [unverified], because the host had already reloaded the probe; stage 83 checks it (section 14 item 14).

### 7.3 Tests

- **Learner fixtures** of the last six releases migrate to the current one, and every id they reference exists and is not retired (content-format 4.5).
- **Event fixtures** for each event format version upgrade in memory to the current shape (`tests/fixtures/events/`).
- **Widget state fixtures.** Each widget folder keeps `states/v<n>.json` for every past `stateVersion`; the generic contract suite migrates each one and checks the result against the current state shape.
- **Snapshot equivalence.** For the synthetic learner, a rebuild from events equals incremental application from any snapshot (assessment 13.3 properties).

---

## 8. Testing and CI

### 8.1 The pyramid

| Layer | Tool | Runs on | What it proves | Scale |
|---|---|---|---|---|
| Static | `tsc -b`, ESLint with `eslint-plugin-zq`, Prettier, stylelint, knip, registry freshness, copy lint of every `copy.ts` | Node | Types, layering, determinism rules, raw-HTML ban, tokens-only colours, no dead code, British English UI copy | Whole repository on every pull request |
| Unit | Vitest, Node environment, fast-check | Node | `packages/*`, the player reducer (every row of section 5.7.2), the fold properties (assessment 16), the release planner, budgets, protocols | Thousands of tests, under 60 s |
| Widget contract | Vitest, one generic suite over every widget's `logic` and `fixtures` | Node | Section 8.1.1 | Every widget on every pull request |
| Widget interaction | Vitest browser mode, `@vitest/browser-playwright`, Chromium | Browser | Pointer, tap-then-tap and keyboard paths reach the canonical answer; reduced motion; axe in every state; focus order; no console errors; the scope is empty after unmount | Changed clusters on pull requests, all nightly |
| Content | `zq check`, `zq verify`, grader replay, storyboards (content-format 6, 9) | Node, Python, Chromium | Every answer proved twice, every screen renders | content-format 6.12 |
| End to end | Playwright, both targets | Chromium (pull request), WebKit and Firefox (nightly) | Section 8.1.2 | About 40 specs |
| Visual | Playwright `toHaveScreenshot`, pinned container | Chromium | Every widget fixture state at 390 by 844, light and dark; every app screen at 390 by 844 and 1,280 by 800, light and dark; motion `test`. The owner's Artifact frame is 440 by 820 CSS px at dpr 3 (894 tall on the two loads the host reloaded) [measured: S1, 7 October 2026]; 390 stays the baseline width (decision 21), as the narrower phone the design serves [our choice]. Lesson storyboards are rendered for pull requests as artefacts, never as baselines. Baselines live on the orphan branch `visual-baselines`, rewritten as one commit when the owner approves a change; `main` holds `tests/visual/baselines.lock.json` with each image's SHA-256; `budgets.ts` caps the set at 4,000 images and 300 MB | Changed areas on pull requests, all nightly |
| Accessibility | `@axe-core/playwright` on every screen and storyboard state; a keyboard-only run of the reference lesson; a manual VoiceOver pass per wave on the owner's iPhone | Chromium, device | WCAG 2.2 AA to the extent tools can tell | Every pull request |
| Performance | `tests/perf`: per-widget drag at 4x throttling, start-up traces, fold rebuild, `size-limit`, release budgets | Chromium, Node | Section 9 budgets | Changed widgets on pull requests, all nightly |
| Devices | The preview Artifact on the owner's iPhone; an Android phone of the budget class when available | Devices | Feel, timing, memory | Each widget wave and each release |

#### 8.1.1 The generic widget contract suite

Run for every widget (scenes included; they add the scene suite of section 5.14) and every fixture in Node, with no widget-specific code:

- `init` is deterministic for a seed; the state survives a JSON round trip and is at most 32 KB.
- `describe('brief')` is at most 300 characters and `describe('full')` at most 2 KB; neither contains `secret()` as a substring, nor any value of the check's canonical answer for a sealed fixture.
- `targets()` has at most 40 entries, unique ids of the `kind:name` form, and includes every `staticTargets(config)` id with the same label and role.
- No `tryable()` control is among `answerObjects()`; `tryValue` never changes `answer()` for an input widget's answer controls.
- Recipes only `set` fields listed in `tweenable`, and only for their own widget.
- Predicates and every pure function return equal results on repeated calls with equal inputs.
- `migrate` handles every stored `states/v<n>.json` fixture.
- `summarise` returns at most 120 characters and never includes a secret.
- `logic.ts` and `schema.ts` import in plain Node with no DOM globals.
- Every interactive fixture has `pointer`, `keyboard` and `tapTap` paths; the browser tests replay all three and each reaches the fixture's `expect`.
- The copy lint (British spelling, banned filler, voice) runs over the outputs of `describe`, `summarise`, every `targets` and `staticTargets` label, every `table` caption and every recipe `annotate` text, for every fixture and named state, because those strings are learner-facing but live in `logic.ts`, outside the `copy.ts` files the static lint reads.

#### 8.1.2 End-to-end scenarios

Each runs on the web build (served with its service worker) and on the Artifact build (through the emulator), unless marked:

1. First run, onboarding with placement, Today.
2. The reference lesson start to finish: a wrong answer with show-why, the hint ladder, Show solution after two attempts, the quiz, celebration, streak day one.
3. Resume mid-lesson after a reload; a lesson whose `rev` changed underneath (content-format 4.4).
4. Keyboard only, the reference lesson.
5. A code drill: Run, a failing Submit with a diagnosis, a passing Submit; a timeout; a crash and restart (real Pyodide, cached by CI). Web build only; on the Artifact build the same drill shows the handoff link and accepts the result code the web run produced (revision 2).
6. Homework: drafts with a lease, submission, marking, a long-form item with the scripted tutor's suggestions.
7. An exam paper with the fake clock: pause budget, reload mid-paper, submission, result, cool-down.
8. Export, then import on the other target; a result code from the web app pasted into the Artifact.
9. Tutor through the fake backend: hint, diagnosis, chat, Stop, every error copy; the off switch hides every surface.
10. Two tabs: the second is read-only until "Use here" (web).
11. Offline: cache a course, go offline, finish a lesson, come back online (web only).
12. Update: a second build activates only after Restart, never mid-lesson (web only).
13. Capability absence: no `db` (browser-only banner), no `sample` (no AI surfaces), `sample` consent declined (Artifact only).
14. Failure injection: course fetch fails, chunk load fails, `db` returns `unavailable` then recovers.
15. A learner infinite loop and a long NumPy call: the first ends by the soft deadline with the worker still warm; the second by the watchdog with a restart (real Pyodide).
16. First Python use with an empty cache (web build): the title screen offers the download with its size and nothing downloads before the tap.
17. Release (Artifact only): a publish plan of several batches in the emulator reloads an open page into each version, mid-lesson and mid-paper; each version works, and after each reload the learner is on the same screen with its drafts and every event kept, and a paper resumes without waiting for its own lease (`docs/DECISIONS.md` B26). On a page the host does not reload (the emulator's fault injection "the host does not reload this page", section 8.2), writing `meta/release` shows the update notice on Today, never inside a lesson, and Reload brings the page to the newest release. With both fault injections on, a page left on the previous release loads its lazy chunks from the retained version after garbage collection, and once a further release removes that version, the failed chunk shows the reload message (test).
18. Single-key shortcuts off: H, W, D and T do nothing; every action stays reachable by visible buttons and Tab.

### 8.2 The Artifact host emulator

`tools/artifact-host` lets every pull request test the Artifact build without publishing:

- **Serving.** Only the host's served file types; anything else is a 404. Every response carries a CSP approximating the host's (scripts: self and the five listed CDNs; styles: self, Google Fonts and inline, as the host allows: a `style` attribute parsed through `innerHTML` applies in the frame with no CSP violation [measured: S1, 7 October 2026]; fonts: self and Google's font host; connect: self; workers: self and `blob:`).
- **Framing.** The page is wrapped in a document skeleton and loaded in a sandboxed iframe on a second origin; `navigator.serviceWorker` is removed by an init script.
- **Fake `window.claude`.** Implements `claude.use` and the `sample`, `db`, `user` and `downloads` contracts of the `.d.ts` files of runtime contract 0.2.74, which the stage 4 emulator targets [our choice] (`docs/DECISIONS.md` B29, revised). It differs from 0.2.73, the contract the S1 probe was written against [sourced: `spikes/s1/CONTRACT.md`], only in `user.d.ts`, whose `can()` gains the name `"people.add"` [measured: diff of the bundled `artifact-capabilities` contract folders, 8 October 2026]; the facts S1 measured stay tagged 0.2.73. This paper was written against 0.2.69, and the runtime version S1 was served was not recorded. The live Artifact's pin is still decided at `docs/PLAN.md` stage 83, against the contract current then (`STATE.md` open question 37). In the fake, `sample` streams scripted replies through `onText`, honours `AbortSignal` and the `cache` rules, and injects every error code on request; `db` is an in-memory document store with path parity, the declared rules (including `{self}`), `onSnapshot`, last-writer-wins and injected `unavailable`, `resource_exhausted` and `quota_exceeded`; `downloads` records saved files and can refuse `html`.
- **Versions.** The emulator keeps every published version and models a publish as S1 measured it on the owner's iPhone (7 October 2026; `docs/DECISIONS.md` B25): it refuses a publish without the page, or of more than 255 `files` entries with `null` removals counted, and then publishes nothing; by default it reloads every open page to the newest version within 5 s of each accepted publish [our choice: S1 saw two reloads, about 4 s and 1 to 2 s after their publishes, cross-clock]. Until its reload a page's own-file fetches reach the version it loaded [inferred from `artifact.d.ts` 0.2.73, which states this for the publishing view]. Two per-page fault injections keep the cases S1 did not measure testable, beside scenario 14's injected chunk failure. "The host does not reload this page" keeps a page on its version, as a backgrounded app, a second device or the desktop and web viewers may [unverified], for scenario 17 and the stale-page case. "This page's own-file fetches reach the newest version" models the other serving, which stays possible while version scoping is unmeasured; the lazy-chunk row of section 5.10.3 and the retained version of section 6.2.5 are tested on a page carrying both injections ("the host does not reload this page" and "this page's own-file fetches reach the newest version"), because under version-scoped serving a page left on its version never loses its files, and a page the host reloads reaches the newest release before any garbage collection [inferred]. Stage 4 builds the injections; the tests that use them, of the lazy-chunk row and the retained version, are `docs/PLAN.md` stage 83's, because garbage collection and retention are built there. Version scoping was not measured: S1 skipped `platform.version-scoping` and `platform.version-json-after`, because the host reloaded the open v1 page, so `docs/PLAN.md` stage 2's switch item is not met; the emulator default is set by inference pending the owner's waiver or a measurement (`docs/DECISIONS.md` B28).
- **CDN modules.** The emulator, and every Playwright run against the Artifact build, answers requests to the locked CDN URLs from local copies of the same npm files, each checked against its SHA-384 in `cdn.lock.json`; any other CDN URL is refused, so a missing lock entry fails a test instead of reaching the network (revision 2).
- **Honest limit.** The emulator encodes what the contracts and the spikes say; differences in the real host are caught only by the release self-test and the owner's phone (section 6.2.6).

### 8.3 CI gates

| Job | When | Blocks merge | Target time |
|---|---|---|---|
| `static` | Every pull request | Yes | 3 min |
| `unit` (with coverage: 90% lines and branches for `packages/*`, `engine/player`, `engine/progress`, `engine/widgets`; 80% for the rest of `engine/`) | Every pull request | Yes | 3 min |
| `widgets` (contract suite for all; browser tests for changed clusters, found from the import graph) | Every pull request | Yes | 6 min |
| `content` (content-format 6.12) | Pull requests touching `content/`, `packages/content-*`, `packages/graders`, widgets | Yes | per content-format |
| `build` (both targets; release budgets; `size-limit`) | Every pull request | Yes | 4 min |
| `e2e` (Chromium, both targets) | Every pull request | Yes | 10 min, sharded |
| `visual` (changed areas) | Every pull request | Yes; a changed baseline needs the owner's `visual-approved` label, and `label-guard.yml` fails the job if any other account applied it | 6 min |
| `perf` (changed widgets; web start-up) | Every pull request | Yes | 5 min |
| `nightly`: full visual (about 3,000 baselines), full performance, WebKit and Firefox end to end and generator goldens, full `zq verify` with Monte Carlo, `npm audit`, `pip-audit`, licence allow-lists, the CDN drift check (`tools/cdn/drift.ts`), the deterministic tutor graders over the last accepted run's recorded replies (no key; ai-tutor 9.1), fold rebuild benchmark | Daily on `main` | Opens an issue on failure | 60 min |
| `release`: everything above, two clean builds with identical file hashes, the Artifact publish plan dry run, the Pages deploy | On a `v*` tag | Yes | 75 min |

Browsers, Pyodide's distribution and the Playwright container are cached between runs, keyed by their pinned versions.

---

## 9. Performance budgets

### 9.1 Devices

- **CI proxy:** Chromium at 390 by 844 with 4x CPU throttling through the DevTools protocol, the method of section 0.2. Every frame-time budget below is enforced there.
- **Budget device class:** a 2022 mid-range Android phone (Galaxy A53 class) on Chrome stable, replacing the two different models the catalogues named. Checked by hand per wave when such a phone is available; the record says when it was not.
- **The owner's iPhone** (an iPhone 17 Pro Max on iOS 27.2 [sourced: the owner, from Settings, 7 October 2026]) for every wave and release, through the preview or live Artifact.

### 9.2 Budgets

The CDN sizes below were taken with zlib 1.3 at level 9 through Python's `gzip`; `budgets.ts` runs on Node 22.22.0, whose bundled zlib (1.3.1-470d3a2) gives figures within 0.6% of these on the small Preact and ts-fsrs files and within 0.05% on the three files that breach a row [measured: S1's `cdn-lock.json` files, Node against Python, 8 October 2026; for example `preact/jsx-runtime` 868 against 863 bytes], which changes no verdict; `budgets.ts`'s own Node figures are the gate, and the figures here are context.

| Measure | Budget | Basis |
|---|---|---|
| Entry script, gzipped | at most 110 KB on the web; in the Artifact the same budget covers the entry plus its locked CDN modules, and until `docs/PLAN.md` section 12 row 15 is decided CI gates only the entry's own code there | Preact, hooks and signals 8.5 KB bundled [measured]; as the Artifact loads them, the four locked files gzip one by one to 10,204 bytes (Preact 4,916, hooks 1,582, `@preact/signals` 1,771, `@preact/signals-core` 1,935), with 863 more for `preact/jsx-runtime` [measured: preact 11.0.0, `@preact/signals` 2.11.3 and `@preact/signals-core` 1.14.4 npm tarballs, zlib 1.3 level 9 through Python's `gzip`, 8 October 2026; files from S1's `cdn-lock.json`]; engine, UI, player, Bertie (at most 12 KB, `BERTIE.md` 9), stores [our estimate]; no widget code (`w-core` holds it) and no manifest (its own file, decision 30). In the Artifact the locked set breaches it: `zod/mini`'s unbundled closure alone is 197,653 bytes gzipped file by file [measured: zod 4.6.5 npm tarball, zlib 1.3 level 9 through Python's `gzip`, 8 October 2026], pending the owner's choice (`docs/PLAN.md` section 12 row 15; section 6.2.7 item 7). The CDN part is computed in CI from the locked files gzipped one by one, since the device reports no CDN sizes [our choice]; until the owner decides `docs/PLAN.md` section 12 row 15, `budgets.ts` reports the Artifact's CDN figures for the entry, the data worker and KaTeX, each as a figure of its own, without failing on them (`docs/DECISIONS.md` B36; `docs/PLAN.md` stage 4 builds the report); our own code keeps its gates, here the entry's 110 KB |
| App stylesheet, gzipped | at most 70 KB | Prototype styles plus widget styles [our estimate] |
| Each screen group, the tutor chunk | at most 60 KB gzipped each | |
| Each widget cluster | at most 80 KB gzipped; each composite at most 25 KB minified (calc-linalg 2.10) | |
| KaTeX, MathLive, Compute Engine parser, MiniSearch chunks (web); the same files from the CDN in the Artifact, without MathLive | 80, 230, 135, 20 KB gzipped | 77, 226, 128, 18 KB [measured]. In the Artifact, KaTeX's `dist/katex.mjs`, the ES module the page loads, is unminified: 602,889 bytes raw and 148,753 gzipped [measured: KaTeX 0.19.0 npm tarball, zlib 1.3 level 9 through Python's `gzip`, 8 October 2026], above the 80 KB row. The recommendation in `docs/PLAN.md` section 12 row 15 is loading `katex.min.js` (75,906 bytes gzipped [measured: KaTeX 0.19.0 npm tarball, zlib 1.3 level 9 through Python's `gzip`, 8 October 2026], inside the row) as a classic script with the lock's `integrity`, the path S1's UMD check proved in the frame (section 6.2.7 item 6), with `Tex` waiting for its `load` event; `katex.mjs` as locked stays the default until the owner decides `docs/PLAN.md` section 12 row 15 (`STATE.md` open question 36), and until then `budgets.ts` reports the Artifact's CDN figures for the entry, the data worker and KaTeX, each as a figure of its own, without failing on them (`docs/DECISIONS.md` B36); our own code keeps its gates. KaTeX preloads at idle, outside the entry (section 5.10.1 step 6) |
| Data worker | at most 150 KB gzipped | classic zod 92 KB [measured] plus the fold. In the Artifact the worker imports classic zod unbundled from the CDN, a 95-file closure of 212,061 bytes gzipped file by file [measured: zod 4.6.5 npm tarball, zlib 1.3 level 9 through Python's `gzip`, 8 October 2026], which breaches it, pending the owner's choice (`docs/PLAN.md` section 12 row 15); until the owner decides `docs/PLAN.md` section 12 row 15, `budgets.ts` reports the Artifact's CDN figures for the entry, the data worker and KaTeX, each as a figure of its own, without failing on them (`docs/DECISIONS.md` B36); our own code keeps its gates, here the worker's own code within 150 KB |
| Web start-up, cold, "Fast 3G" and 4x CPU | Today interactive within 3.0 s | [our choice] |
| Start-up, warm (cached), web and Artifact | Today interactive within 1.2 s; 1.5 s on the owner's iPhone in the Artifact | [our choice]; measured at E7 and E10 |
| Continue to the next screen painted | within 100 ms | content in memory, next screen prefetched |
| Drag, script per frame, P95 at 4x | 4 ms for a primitive, 8 ms for a composite | widgets-stage0 1.9, calc-linalg 2.10; the section 2.3 composite measured 2.7 to 3.8 ms median and 4.3 to 6.0 ms P95 at 4x in its disciplined variants [measured] |
| Widget mount, excluding lazy dependencies | 50 ms for a primitive, 100 ms for a composite | widgets-stage0 1.9, calc-linalg 2.10 |
| Check to verdict, non-code checks | within 150 ms, expressions included | design research 5.4 |
| Interaction to next paint | at most 200 ms | widgets-stage0 1.9 |
| Idle screen | zero animation frames requested once springs settle | `BERTIE.md` 9 |
| Fold | single event within 2 ms on the main thread; full rebuild of the synthetic whole-path learner (about 121,000 events, `docs/PLAN.md` 5.5) within 3 s in the worker on the owner's iPhone | assessment 13.3 |
| Python warm start from cache (web app) | within 4 s on the owner's iPhone | spike: 2.8 s to Python, 5.1 s with NumPy and pandas from the network (inside an Artifact, a comparable record) |
| Python cold download, NumPy and pandas (web app) | at most 22 MB of files; within 15 s on the owner's iPhone on Wi-Fi | 21.4 MB in the native layout [measured, section 6.4.1]; the time is [our choice], measured at `docs/PLAN.md` stage 25 |
| Recovery from a learner infinite loop | next test running within 500 ms | soft deadline (decision 31); a watchdog restart is the exception |
| Memory | at most 30 MB per widget; main-thread heap at most 150 MB outside the Python worker | calc-linalg 2.10 |
| Celebrations | at most 2.4 s, skippable | design research 4.1 principle 7 |

---

## 10. Developer experience

### 10.1 Commands

| Command | Does |
|---|---|
| `npm run dev` | Web dev server, content compiled on the fly, hot reload, development routes |
| `npm run dev:artifact` | The Artifact build through the host emulator with hot reload |
| `npm run check` | Every static check |
| `npm test`, `npm run test:widgets -- <type>`, `npm run test:e2e`, `npm run test:visual` | The test layers |
| `npm run perf -- <type>` | The drag harness for one widget, printing median and P95 at 4x and 6x |
| `npm run new:widget -- <type> --cluster <c> --tier <t>` | Scaffolds the widget folder with every file, a failing test per contract item, and a registry entry |
| `npm run new:screen -- <id>` | Scaffolds a screen |
| `npm run build:web`, `npm run build:artifact` | Production builds with budgets |
| `npm run serve:web` | Serves the web build with the local tutor proxy |
| `npm run release:artifact` | Builds the Artifact and writes the publish plan (section 6.2.6) |
| `zq ...` | The content CLI (content-format 8, 9) |

### 10.2 Development routes

Compiled into `dev` builds and preview Artifacts only (`devOnly`):

| Route | Shows |
|---|---|
| `#/preview/<lesson>`, `#/preview/<lesson>/<screen>?state=...` | content-format 9.2 |
| `#/storyboard/<lesson>` | Every screen in every state on one page (content-format 9.2) |
| `#/specimen/<gen>` | One item per enum combination (content-format 9.2) |
| `#/gallery`, `#/gallery/<widget>`, `#/gallery/<widget>/<fixture>?state=...` | Every widget fixture in the real host, with state controls (idle, engaged, each mark, revealed, highlighted, ghost), theme, width, motion, the Describe text, the tutor's `describe`, `targets`, `tryable` and `secret` output, and the frame-time readout of the last drag |
| `#/tutor/<lesson>/<screen>` | The exact tutor request (content-format 9.2, ai-tutor 4) |
| `#/system` | Tokens, type, buttons, states, motion presets, Bertie states (the prototype's system screen) |

Query parameters `&theme=dark`, `&w=390` and `&motion=reduced|test` work on every development route.

### 10.3 Hot reload

- **Components and CSS:** Prefresh and Vite's CSS hot replacement keep state.
- **Widget logic:** a change to a `logic.ts` hot-replaces its cluster module; the host remounts the widgets of that type on the current screen with their current state (through `migrate` if `stateVersion` changed).
- **Content:** `vite-plugin-zq-content` watches `content/`, recompiles changed files through the compiler's incremental cache (content-format 8.5) and sends a `zq:content` event with the changed ids. The player keeps the screen index and widget states when the lesson's screen ids are unchanged, and otherwise reopens at the same screen id if it still exists. Compile errors show as an overlay with the file and line, and the last good version stays on screen.

### 10.4 Lint rules

typescript-eslint `strict-type-checked` and `stylistic-type-checked`, `eslint-plugin-react-hooks` recommended, and `eslint-plugin-zq`:

| Rule | Scope | Bans or requires |
|---|---|---|
| `zq/no-nondeterminism` | `widgets/**/logic.ts`, `packages/{mathcore,graders,gen-kit}`, `content/generators` | `Math.random`, `Date`, `performance.now`, `crypto.getRandomValues`, transcendental `Math` in generator `accept`, `level` and `answer` (content-format 5.3) |
| `zq/no-raw-timers` | `widgets/`, `screens/`, `engine/player` | `setTimeout`, `setInterval`, `requestAnimationFrame`; use the `Scope` |
| `zq/no-raw-pointer` | `widgets/composites`, `widgets/presets` | `addEventListener` and `on*` pointer and touch handlers; use the interaction hooks |
| `zq/no-state-in-render` | `widgets/**/View.tsx` | Reading `api.state.value` in a component body; use `useComputed` |
| `zq/no-inner-html` | everywhere | `innerHTML` and `outerHTML` (assigned or as object keys), `insertAdjacentHTML`, `dangerouslySetInnerHTML`, `write` and `writeln` on any `Document`, `setHTMLUnsafe`, `parseHTMLUnsafe`, `createContextualFragment`, `DOMParser` and `parseFromString`; the two exemptions are hard-coded in the rule: `engine/render/Tex.tsx` (S1) and, for `DOMParser`, `ui/bertie/markup.ts` (S2) |
| `zq/no-forbidden-apis` | `src/` | `open`, `print` and `eval` as globals or on any `Window` (aliases and destructuring included, through the type checker); `Function` and any `FunctionConstructor`; `iframe`, `object` and `embed` elements (JSX, `createElement`, `createElementNS`, `h()`); `navigator.serviceWorker` outside `platform/web` and `sw/`; `back` and `go` on any `History`, from `docs/PLAN.md` stage 74a (section 5.8; `docs/DECISIONS.md` B23) |
| `zq/no-classic-zod` | `src/` except `workers/` and `**/schema.ts` | Importing `zod`; `zod/mini` is allowed |
| `zq/no-schema-import` | `src/` except `widgets/registry.node.gen.ts` | Importing any `widgets/**/schema.ts` (decision 33; section 4.5) |
| `zq/no-colour-literals` | `src/**/*.{ts,tsx,js,mjs}` (widened at stage 1, `docs/DECISIONS.md` B2) | Hex, `rgb()` and `hsl()` literals; colours come from tokens (stylelint enforces the same in CSS). KaTeX's reserved colours, the term-sentinel range and `errorColor`, live in `@zq/contracts`, outside the rule's `src/**` scope (`docs/DECISIONS.md` B27 and B33) |
| `zq/no-empty-catch` | everywhere | A `catch` clause, or a `.catch(fn)` or `.then(a, fn)` handler (inline or a local function), that neither rethrows, logs (`log`, `logger`, `console`) nor passes its error on (returned, thrown, passed to a call that is not a conversion, or stored outside the handler) (engineering floor) |
| `zq/copy-in-copy-files` | `screens/`, `app/`, `engine/player`, `tutor/ui` | Learner-facing string literals in JSX; they live in `copy.ts`, which the copy lint checks for British spelling, banned filler and voice |
| `zq/layering` | `.ts`, `.tsx`, `.js` and `.mjs` files under `src`, `packages`, `tools`, `proxy` and `tests`, and the root `*.config.{ts,js}` files | The layering of section 4.5, with `$1` captures for a screen's own folder |

No file may switch a rule off: `linterOptions.noInlineConfig` is set for the whole repository, so an `eslint-disable` comment does nothing and an exception can only live in `eslint.config.js`, where review sees it (stage 1, `docs/DECISIONS.md` B12).

### 10.5 Authoring widgets with agents

`docs/engine/WIDGET-AUTHORING.md`, written in stage E4, is the agent-facing guide: the contract by example (the reference lesson's widgets are its main examples), the render discipline of section 2.5, the folder shape, the `WidgetFixture` shape and its three input paths (section 5.3), the test kinds, the budgets, the visual rules of widgets-stage0 1.5 and calc-linalg 2.5, and when to write a preset instead of a composite. The workflow mirrors content-format 9.1:

1. **Brief:** the catalogue entry, the cluster, the lessons that need it, the primitives it should compose.
2. **Scaffold** with `new:widget`; write `logic.ts` and its tests first, then `schema.ts`, `fixtures.ts`, `View.tsx`.
3. **Look:** the gallery at 390 and 1,280, light and dark, reduced motion; `npm run perf -- <type>`.
4. **Self-review** against the pull request template (contract items, keyboard path, tap-then-tap path, Table view, Describe text quoted, budgets with numbers).
5. **Adversarial review** by a second agent session that did not write it.
6. **Owner review and merge:** one widget per pull request, or one cluster's presets per pull request.

A new composite with its own view needs one line in the pull request saying why a preset over an existing widget cannot do the job (decision 7).

---

## 11. Security, failure behaviour and operations owned by the engine

### 11.1 Threat class and scope

`docs/PLAN.md` section 7 classifies the project as Class C: the web target's tutor proxy is an endpoint holding a secret and accepting browser requests, and the only people whose data the app holds are the owner and, at P2, invited friends; it names the trigger that would make it Class D. `AI-TUTOR.md` 10 covers the proxy, its secrets, authentication and rate limits; `ASSESSMENT.md` 15 covers the data held and its retention. The engine runs only in browsers and holds no secret of its own; what it owns is input validation at its boundaries, raw-HTML sinks, sandboxing of learner code, and the failure behaviour of the runtime.

### 11.2 Entry points

| Input | Origin | Validation | On failure |
|---|---|---|---|
| Course bundle | Own file, built by our CI | SHA-256 against the hash in its name, then the structural classic zod schema in the data worker, once per hash; widget configs were validated at compile time (section 5.10.2) | Not cached; error screen (section 5.10.3) |
| Generator module | Own file, built by our CI; executes as code | Trusted like the app's own chunks: same origin, same pipeline, file name pinned by the manifest the page names | Item skipped, logged |
| Route and query parameters | The address bar | `zod/mini` parse per screen; unknown routes render Not found | Not found |
| Content manifest | Own file named by the page's meta tag | SHA-256 against the hash in its name; `zod/mini` shape check | Start-up error with Retry (section 5.10.1) |
| `meta/release` and `ops/*` documents | `db`, written by the owner | `zod/mini` shape check; a release id only ever triggers a notice, never code | Ignored |
| Handoff payload (`?h=`) | A link from the Artifact | At most 8 KB; base64url and deflate decode; schema; the drill, homework instance and seed must exist | "This link could not be opened." |
| Progress import, result code | A file or pasted text | assessment 14.2 and 14.3, in the data worker | Rejected with the first error; nothing written |
| Events from other devices (`db`) | Our own writers, but stored remotely | Event schema on load | Quarantined (assessment 13.8) |
| Learner code | The learner | None needed: it runs on the web app only, in the Python or SQL worker with no DOM, no app storage, no network beyond the loader | Terminated on timeout; restarted on crash |
| Third-party modules (Artifact) | cdnjs or jsDelivr | Exact-version URLs from `cdn.lock.json` only; import-map `integrity` where the browser enforces it; none in the worker; the nightly drift check (section 6.2.7) | The boot or lazy-load failure rows of section 11.6 |
| Learner text (long-form, chat, outside-work log) | The learner | Length caps from the schemas; rendered as text, never HTML | Truncated with a note |
| Tutor replies | Claude | ai-tutor 5.4 and 8: act-line schemas (`zod/mini`), id checks, leak probe, code guard, Markdown subset rendered to DOM nodes | Effects dropped and counted |
| `KeyValue`, drafts, cache entries | This device | Schema per key on read; cache entries by hash | Discarded |

### 11.3 Raw-HTML sinks

Exactly two, both justified in `docs/DECISIONS.md` as the engineering floor requires:

1. **S1, `engine/render/Tex.tsx`**, sets `innerHTML` to KaTeX's output, HTML with MathML on the web and MathML alone in the Artifact (decision 37). KaTeX escapes its input. Authored TeX renders with `throwOnError: true`, the shared macros, and `strict` set to a function that returns `'ignore'` for the code `htmlExtension` and `'error'` for every other code, because KaTeX 0.19.0 refuses `\htmlData` under `strict: 'error'` before it reads `trust`, on both outputs [measured: KaTeX 0.19.0 in Node, 8 October 2026; `src/functions/html.ts` reports `htmlExtension` to the strict handler]; under the function the anchor renders and keeps `data-term` on the web, while an accented letter in maths mode and a trailing `%` comment still throw [measured: KaTeX 0.19.0 in Node, 8 October 2026]. Its `trust` callback allows only `\htmlData` with a name matching `^[a-z][a-z0-9-]{0,15}$` (term anchors on the web; KaTeX's MathML output drops `\htmlData` [measured: spike S1, 7 October 2026], so in the Artifact, with the runtime flag `artifact.termBinding` on, the authored configuration defines `\htmlData` as a KaTeX function macro that renders each term anchor as a sentinel `\textcolor` at render time and any other attribute as its body alone, if the owner accepts `docs/DECISIONS.md` B27, decision 37). A command `trust` refuses does not throw: KaTeX renders its name as text in `errorColor` [measured: KaTeX 0.19.0 in Node, 8 October 2026: `\htmlId{a}{b}` gives `<mstyle mathcolor="#cc0000"><mtext>\htmlId</mtext></mstyle>` with the default colour], so the authored configuration sets `errorColor` to the reserved `#0a0100`, and `zq check` (`docs/PLAN.md` stage 7) fails any authored formula whose output carries it, compared without regard to case, as it fails the term range (section 14 item 20; `docs/DECISIONS.md` B33). Bertie's maths renders with `trust: false` and `strict: 'ignore'`, unchanged (ai-tutor 8.8). `TexSlots` binds slots by sentinel `\text{}` tokens on both outputs and never through `\htmlData` (decision 37): the HTML span's text node on the web, and in every MathML tree an `<mn>` built with `createElementNS` in place of the sentinel `<mtext>`, so live digits use the maths font.
2. **S2, `src/ui/bertie/markup.ts`**, parses Bertie's SVG template, built from the module's own constants, with `DOMParser` as `image/svg+xml` (BERTIE.md decision 19). No data reaches it.

The tutor's Markdown renderer and Bertie's `say()` build DOM nodes or set `textContent` (ai-tutor 8.8, BERTIE.md decision 13). The lint rule `zq/no-inner-html` keeps these the only two: stage 1 extends it from the `innerHTML` family (section 10.4) to `DOMParser.prototype.parseFromString` and `Range.prototype.createContextualFragment` outside `markup.ts` (`docs/DECISIONS.md` S2).

### 11.4 Secrets and configuration

- **Secrets in the client:** none of ours. The web app stores one learner-entered credential, the tutor proxy token, in IndexedDB through `KeyValue.setSecret`, never in `localStorage`. Its exposure is an XSS on our own origin, which section 11.3 keeps narrow; its damage is capped by the proxy's spend limits (ai-tutor 0.1 decision 8). Accepted and written down.
- **Build-time configuration** comes from `VITE_*` variables (`VITE_BASE`, `VITE_ZQ_TUTOR_URL`, `VITE_ZQ_WEB_APP_URL`), with `.env.example` committed and `.env` ignored. No secret is a `VITE_*` variable, because Vite inlines them into the bundle; a CI check fails if any `VITE_*` name contains `KEY`, `TOKEN` or `SECRET`.
- **Feature flags** live in `src/app/config.ts` with typed defaults per target, nowhere else: `tutor.answerKey: 'sealed' | 'never'` (ai-tutor decision 2's kill switch), `friendsBoard`, `devRoutes`, `artifact.termBinding` (`docs/DECISIONS.md` B27: the Artifact's `\htmlData` term macro in `TexService`'s authored configuration and the term binding, both built at `docs/PLAN.md` stage 12; false by default, true in stage 25's preview build). Draft 1's `python.groups` is gone with the Artifact's Python (revision 2).

### 11.5 Logging and diagnostics

- `app/log.ts` keeps 500 entries in memory and the last 2,000 in IndexedDB: time, level, module, message, and ids only (content ids, widget type and version, error codes, release).
- Never logged: learner answers, code, long-form text, chat, tutor replies, tokens, viewer ids.
- Nothing leaves the device. Settings, Diagnostics offers **Copy diagnostics** (the log, the release, the capability summary, storage usage, Python status on the web, CDN module status in the Artifact) and **Self-test** (section 6.2.6), so a problem report is a paste the owner chooses to make.

### 11.6 Failure behaviour of the engine's own dependencies

Beyond sections 5.10.3 and 6.3.1, and the tutor's and progress papers' tables:

| Dependency | Failure | Behaviour |
|---|---|---|
| Google Fonts (Artifact) | Unreachable | The token font stacks fall back to system fonts; layout tolerates the metric change |
| KaTeX (web chunk or Artifact CDN module) | Fails to load | Maths renders as its TeX source in the code style, with a Retry in the verdict area |
| Core CDN modules (Artifact: Preact, signals, `zod/mini`, `idb`, `ts-fsrs`) | Unreachable, 404, or integrity refused | The bootstrap's `import()` rejects; one retry after 2 s; never a URL outside the lock; "Zero to Quant could not load part of itself. Check the connection and try again." with Retry and the web app's address; logged as `cdn-network` or `cdn-integrity` |
| The data worker's CDN modules (Artifact) | Fail to load | `failed: dependency`, restart once; a bundle whose SHA-256 matches its name opens without the structural check, logged; imports and result codes wait |
| `meta/release` (Artifact) | `db` absent or the subscription ends | `version.json` polling as on the web (section 7.2) |
| MathLive chunk (web) | Fails to load | `expression-entry` falls back to the plain field with the symbol bar and a live preview, which the Artifact always uses; grading is unchanged |
| Compute Engine parser (either target) | Fails to load | Expression screens keep Check disabled with "Maths checking could not load" and Retry; other screens work |
| SQLite (web) | Fails | "SQL could not start in this browser" with Retry; replays of authored queries still show (programming 2.10). In the Artifact SQL drills always hand off |
| Service worker (web) | Registration fails | The app works online; Settings says "Offline use is unavailable in this browser." |
| AudioContext | Blocked or absent | Sound silently unavailable; the Settings toggle explains why |
| Web Locks | Absent | The `localStorage` heartbeat lease (section 4.7) |
| `version.json` | Fetch fails | Ignored; tried again at the next visibility change an hour later |
| Clipboard | Write refused | The text is shown selected in a sheet with "Copy it from here" |
| A capability (Artifact) | `null` | Per section 5.9: `db` or `user` absent means browser-only progress with a banner; `sample` absent hides AI surfaces; `downloads` absent offers copy-to-clipboard for exports under 1 MB and says so for larger ones |

---

## 12. Risks and mitigations

| # | Risk | Likelihood | Effect | Mitigation |
|---|---|---|---|---|
| 1 | Preact 11.0.0, six days old, has a regression that bites us | Medium | Rendering bugs | Exact pin; the full suite at every upgrade; 10.29.8 measured working with the same code, so the fallback is a one-line change and a test run |
| 2 | Spike S1 fails: the import map, CDN modules on the page or in a worker, import-map integrity, MathML quality, Web Locks, version scoping or reload behave differently in the Artifact | Closed by S1 [measured: S1, 7 October 2026] | | S1 ran in stage E0 before anything depended on it, and every check had a named fallback (sections 5.9, 6.2.3, 6.2.7, 11.6). Passed: the import map and its integrity, CDN modules on the page and in a module worker, MathML quality, Web Locks and the host's reload of the open page. Failed, with the fallbacks in force: the system back gesture (section 5.8) and `\htmlData` in MathML (section 14 item 20). Not measured: version scoping (section 8.2; `docs/DECISIONS.md` B28) and `location.reload()` from a page on an older version (section 14 item 14). Open: `zod/mini`'s request cost (section 14 item 22) |
| 3 | The Artifact host changes its policy, limits or capability contracts | Low to medium | A target breaks | Design for absence everywhere; the emulator encodes the contracts we rely on; the release self-test; the web app as the full-function fallback |
| 4 | Pyodide with pandas, SciPy or scikit-learn exhausts iPhone memory in the web app | Medium | Drills crash on the phone | One worker, packages per course, termination when idle, restart once, then the web app on a computer; memory measured at E8 on the owner's phone |
| 5 | Draft 1: the scientific stack does not fit the Artifact's Python budget | Closed by revision 2 | | The Artifact has no Python; every drill hands off by result code (assessment 14.3) |
| 6 | Agent-written widgets drift from render discipline and budgets | High | Janky drags on phones | Lint (`zq/no-state-in-render`, `zq/no-raw-pointer`), the per-widget frame test as a merge gate, the gallery's frame readout, adversarial review |
| 7 | Catalogue scale (338 ids after the merge; draft 1: 314) overwhelms the library | High | Inconsistent widgets, slow build | Scenes as the default composite (decision 36, section 5.14) and presets as a tier (decision 7); a bespoke composite needs one of the five written reasons; the generic contract suite makes each new widget's floor automatic; four pilot scenes, one per family, test the bet before the batches start (`docs/PLAN.md` stage 14) |
| 8 | File or size budget creep in the Artifact | Low (about 198 files and 125 MB against 230 and 150) | Releases fail | Budgets enforced in every build, not at release time; the maintenance release path |
| 9 | Determinism breaks across browsers (generators, Philox, number formatting) | Low | Different items on different devices | Integer-only RNG; known-answer tests and golden seeds in Chromium, WebKit and Firefox nightly |
| 10 | Two targets drift apart | Medium | Bugs on one target only | One codebase; platform code is the only difference; one conformance suite per adapter; every end-to-end scenario on both targets |
| 11 | Visual tests flake | Medium | Ignored failures | Pinned container, committed fonts, `test` motion mode, `document.fonts.ready` before screenshots, zero tolerance only for layout and a small pixel ratio for anti-aliasing |
| 12 | iOS evicts web-app storage after a period without use [recalled: Safari's seven-day rule for sites not added to the Home Screen] | Medium | Lost local progress on the web | Persistence request; export reminders (assessment 13.5); the Artifact's `db` is the durable copy for Artifact users, whose frame storage is not persisted either (`persisted: false`, a 983 MiB quota [measured: S1, 7 October 2026]) |
| 13 | TypeScript 7 and its faster checker stay out of reach | Low | Slower type checks | Revisit when typescript-eslint declares support; nothing in the code depends on the version |
| 14 | A release reloads an open page mid-lesson or mid-paper (the host reloaded the open page after each publish [measured: S1, 7 October 2026]); a page it does not reload, such as a backgrounded app, a second device or the desktop and web viewers, goes stale | High for the reload; [unverified] for a stale page | Interrupted work and a fresh start per batch; lazy chunk 404s on a stale page | Events durable on the device before the reload, and the route and drafts mirrored to `sessionStorage` (section 6.2.6; `docs/DECISIONS.md` B22); every intermediate version works (`docs/DECISIONS.md` B24); the retained previous release (section 6.2.5); chunk failures show the reload message; `meta/release` and `version.json` checks; the emulator's two fault injections keep the stale page and its lazy chunks tested (section 8.2) |
| 15 | Bertie drops frames on mid-range Android | Low | A sluggish mascot | `BERTIE.md` 9 budget, the three-instance rule, the frame test, and its own fallback (fewer particles and strands) |
| 16 | Draft 1: the platform objects to repackaged archives in published files | Closed by revision 2 | | The owner's publishing rule publishes no third-party file |
| 17 | The soft deadline's `sys.monitoring` callback slows learner code noticeably | Low | Efficiency drills misjudge, or tests near their limit fail | Measured at E8 on the reference drills; above 1.3 times, the soft deadline is dropped (decision 31); efficiency probes already compare against the reference on the same device under the same instrumentation |
| 18 | A CDN is unreachable, drops a path, or serves altered bytes for a pinned file (Artifact) | Low | The Artifact cannot start, or runs altered code | Exact-version URLs; import-map integrity where enforced; the nightly drift check; the host's CSP limits where altered code can send data; the web app as the fallback; a waiver in `DECISIONS.md` for imports SRI cannot cover |
| 19 | MathML in system fonts looks worse than KaTeX's HTML on the owner's iPhone | Low: the owner accepted S1's 40-formula specimen [measured: S1, 7 October 2026] | Maths reads less well in daily use | The accepted sheet set no maths font: it used the browser's `math` family at 1.21em, each formula in its own sideways-scrolling box [measured: S1, 7 October 2026], the rule `Tex` keeps for display formulas (section 5.11), so `math.css` starts from that default; a look the owner rejects later goes to him with the measured options |

---

## 13. Build stages

> **Superseded as an order by `docs/PLAN.md` section 11**, which builds the engine, the Python runtime and every P0 widget batch before the tutor, progress, assessments and builds, then content. The E stages map to it as follows: E0 is stages 1 and 2; E1 stage 3, with its numerics in 3a and 3b and the `@zq/models` services in 3c to 3f; E2 stage 4; E3 stage 5 (Bertie moves to stage 59); E4 stages 10a to 19 (with the scene layer, stage 14); E5 stage 23; E6 stages 9 and 24, with assessment A1 (the event log and `AppendQueue`) as stage 9a before the player; E7 stages 74a and 74b; E8 stages 25 and 26; E9 stage 82; E10 stage 83. The rows below keep their deliverables and definitions of done, which `docs/PLAN.md` cites.

Each stage is one review gate. Engine stages are numbered E0 to E10; content stages are those of `CONTENT-FORMAT.md` section 14, assessment stages A1 to A15 (`ASSESSMENT.md` 19), tutor stages T0 to T8 (`AI-TUTOR.md` 11.2), widget waves W0 to W3 per catalogue (`widgets-stage0.md` 1.12 and the sibling catalogues). Security and test work sits inside the stage that creates the exposure.

| Stage | Deliverable | Depends on | Done when |
|---|---|---|---|
| **E0 Foundation and spike S1** | Repository scaffold (section 4), pinned toolchain (section 3), CI skeleton with `static`, `unit` and `build` jobs; an empty app booting on the web dev server and in the emulator; `tools/release/page.ts` and `budgets.ts`. **Spike S1** (re-scoped by revision 2), a page published by a Claude session from files it writes itself and opened on the owner's iPhone, checking: an import map in the page fragment, honoured by the classic bootstrap's dynamic `import()`; Preact 11.0.0, `@preact/signals` and `zod/mini` from jsDelivr, and from cdnjs where it hosts the identical file, through the map; whether import-map `integrity` is enforced (a wrong hash must be refused); a module worker importing classic zod, ts-fsrs and fflate by full URL (if refused, the data worker's jobs move to the main thread, section 14 item 19); a classic CDN `<script>` with `integrity` for the Preact 10.29.8 UMD fallback; KaTeX 0.19.0 from the CDN with `output: 'mathml'` on a 40-formula specimen sheet judged by the owner beside the web app's HTML output, and `TexSlots`' sentinel binding, with slot digits in the swapped `<mn>` against the maths font; and the platform checks of `docs/PLAN.md` stage 2 (c), the single list, mirrored here: inline `style` attributes through `innerHTML`; whether responses are compressed (transfer against file sizes); Web Locks; IndexedDB inside a worker; `navigator.storage.estimate()`; whether an anchor to an external URL opens from the frame (the handoff link); a file input; whether `version.json` is cached despite a query string (item 12); after a second publish, whether the open page still fetches a file only the first version had, and whether `location.reload()` loads the second version; whether a publish may omit the page and whether `null` removals count against 255 paths (item 15); `meta/release` through `onSnapshot`; `sample`, `user` and the `db` rules; whether the system back gesture walks the frame's history. Draft 1's own-font, `FontFace`, JSON-part Python and MathLive checks are dropped | none | CI green on both targets; S1 results in `docs/DECISIONS.md`; every failed check has switched to its named fallback in this paper (section 6.2.7 item 6 for the import map, not needed: S1 found the map honoured [measured: S1, 7 October 2026]; the system back gesture failed, section 5.8; `\htmlData` in MathML failed, section 14 item 20) before E1 starts |
| **E1 Contracts and maths core** | `@zq/contracts` (section 5 types); `@zq/mathcore`: Philox4x32-10, FNV-1a, rationals, number parsing (shared with the graders), the expression compiler without `eval`, scales, basic statistics; `engine/scope.ts`, `engine/rpc.ts` | E0 | Unit and property tests; Philox and `hash32` known-answer vectors; golden draws identical in Node, Chromium, WebKit and Firefox; a scope leak test (no callbacks after dispose); 90% coverage |
| **E2 Platform adapters** | Section 5.9 for web, Artifact and fake; `KeyValue`, `DraftStore`, `BlobCache`, `Clock`, `RandomSource`, `Feedback` (synthesised tones), `FileSaver`, `Identity`, `Handoff`, `Lifecycle` with writer election; `tools/artifact-host` with the fake `window.claude` | E1; A1 (`MemoryStore`, event envelope) | One conformance suite per interface passes against every implementation; emulator rule and error-injection tests; the emulator, on contract 0.2.74 (`docs/DECISIONS.md` B29, revised), refuses a publish without the page or of more than 255 `files` entries with removals counted, reloads open pages within 5 s of each accepted publish by default, and has both per-page fault injections of section 8.2, each tested (`docs/DECISIONS.md` B25 and B28); the two-tab writer test |
| **E3 Design system, motion, Bertie** | `styles/` from the prototype tokens; `ui/` components; the motion service (section 5.11); Bertie in TypeScript with `Bertie.tsx`; the `#/gallery` and `#/system` routes | E1 (E2 in parallel) | Visual baselines at 390 and 1,280, light and dark; axe clean; keyboard paths for every interactive component; `BERTIE.md` 12.2 tests and its 12 KB budget; spring settling and stability tests; a script checks every text and background token pair against WCAG AA |
| **E4 Widget runtime and first widgets** | Registry generators (`registry.gen.ts`, `registry.node.gen.ts`), `CompilerRegistry`, the `WidgetFixture` runner shared by the contract suite, browser tests and gallery, `WidgetHost`, `WidgetApi`, the interaction hooks, the overlay, the show-why runner, the preview guard, `describe` aggregation, drafts and migration (with the Artifact's synchronous `sessionStorage` mirror, `DraftStore.mirror`), the scaffolder, the generic contract suite, the frame-time harness; the widgets the reference lesson needs (`widgets-stage0.md` 2.8) plus `plot-2d`, `drag-point` and `slider`; `docs/engine/WIDGET-AUTHORING.md` | E2, E3 | Every widget passes the generic suite and its browser tests (pointer, tap-then-tap, keyboard), axe in every state, P95 frame time within budget at 4x, an empty scope after unmount; the guard refuses a ghost that would reveal the answer; drafts survive a reload, one that fires no `pagehide` included (the mirror; `docs/DECISIONS.md` B22) |
| **E5 Content runtime** | The manifest file and its page meta tag (`vite-plugin-zq-content`), the loader, `BlobCache` wiring, validation in the data worker, `Prose`, `Tex` and `TexSlots`, templates, the generator runtime with `make` and `makeWhere` | E4; content-format C1 (schema) and C8 (emit of the reference lesson) | The reference lesson's bundle loads and validates; every row of section 5.10.3 is tested; a content edit hot-reloads into an open lesson without losing the screen; a content-only rebuild changes only the page, the manifest and that course's files (section 6.1) |
| **E6 Lesson player and item runner** | Section 5.7: reducer, effect runner, views, hint ladder, Why, Show solution, quiz, completion sequence, key map, announcements, `ItemRunner` and the policies; graders wired in; progress events through the append queue | E5; the graders package (content-format 14); A1, A4 (points rules) | Every row of the transition table tested; the reference lesson runs end to end on both targets with no lesson-specific code; keyboard-only run; axe; the storyboard renders every state; no animation frames once idle |
| **E7 App shell and screens** | Router, shell, stores, the screens of section 5.8 (Today, Learn, Course, Review, You, Settings with Diagnostics, Notebook, Search, Import, Onboarding shell), error boundaries, update notices, `version.json` | E6; A4 and A5 for live data (the synthetic learner until then) | Visual baselines for every screen at both widths and themes with the synthetic learner; axe; route, focus and title tests; every route except the four tab roots renders a back or close control with an accessible name that navigates to its typed parent route, and `zq/no-forbidden-apis` refuses `history.back()` and `history.go()` (`docs/DECISIONS.md` B23); in the Artifact build the current route is mirrored to `sessionStorage` and restored after a reload (B22); warm start-up within budget |
| **E8 Python and SQL (web app)** | The Python worker and protocol, the native loader, `tools/pyvendor`, the watchdog, the drill screen and `code-cell` integration; the SQLite worker; the Artifact's handoff stubs; `zq preview --artifact` and the long-lived preview Artifact | E4, E5 (parallel with E6 and E7) | The reference course's drills pass on the web build in CI with real Pyodide, and every code screen of the Artifact build shows the handoff link; soft-deadline, watchdog and crash tests; soft-deadline overhead on the reference drills recorded (decision 31); iPhone timings and memory recorded by the owner in the web app for every load group, the stage passing on `stdlib` and `numpy-pandas`; in the preview Artifact, `docs/PLAN.md` stage 12's term-target check on the iPhone and, if `docs/PLAN.md` section 12 row 15 chose (b), the `modulepreload` gain recorded there |
| **E9 Web target** | Service worker, Keep offline, update flow, CSP, web manifest and icons, `pages.yml`, `serve:web` | E7, E8 | Offline and update end-to-end scenarios; zero CSP violations reported across the end-to-end suite; a tagged deploy reaches the web host of `docs/PLAN.md` decision 13 (default: Cloudflare Pages behind Access) and installs on the owner's phone, where a handoff from the Artifact whose fragment carries an 8 KB payload arrives intact and its result code comes back (section 5.9; `docs/DECISIONS.md` B30) |
| **E10 Artifact target and release** | `page.ts`, the capability declaration (after loading the `artifact-capabilities` skill), the release ledger, the publish planner with batches, rebuild-and-verify, garbage collection and rollback from ledgers, the resume rule, peak check and the maintenance path, Self-test, `docs/engine/RELEASE.md` | E7, E8 | Planner tests (batch limits with removals counted, the page in every publish and its role, `previous`, `new` or `maintenance`, asserted for each per `docs/DECISIONS.md` B24, drift stop against the previous ledger, order, previous-release retention, resume after a session death at each step, maintenance path); every intermediate version of a plan boots and plays in the emulator, and a page reloaded mid-lesson or mid-paper at each publish keeps its screen, its drafts and every event, and a paper resumes without waiting for its own lease (`docs/DECISIONS.md` B26); the built Artifact passes every end-to-end scenario in the emulator, a page the host does not reload included; with both fault injections on, a page left on the previous release loads its lazy chunks from the retained version after garbage collection, and once a further release removes that version, the failed chunk shows the reload message (test); the first live publish passes Self-test on the owner's iPhone, and the session reads the result from `ops/selftest-<release>` |

**Interleaving.** Content stages (`CONTENT-FORMAT.md` 14) map in as follows: C1 (schema) and C2 (`zq check`) run beside E1 to E3; C2's element-reference checks need E4's `CompilerRegistry`; E5 needs C1 and the C8 emit of the reference lesson; E6 needs C3 (graders); C4's expression grader needs E1's `expr` core; E8 needs C7 (drill pipeline, without MicroPython and, since revision 2, with no Artifact runtime); C9 (preview and storyboard) needs E6; C10 needs the tutor stages; C11 (acceptance on both targets) needs E10. Widget waves start once E4 is approved and run beside E5 to E10, one widget per review. T0 and T1 start once E4 fixes the widget hooks; T5 needs E6; A2 needs E2; A7 needs E6. The first complete vertical slice, the reference lesson on both targets with Bertie through fake backends, is the end of E6, and it is the point where content authoring at volume can begin.

---

## 14. Open questions and unverified items

| # | Question | Effect if the answer is unfavourable | How it closes |
|---|---|---|---|
| 1 | Page-level module scripts and dynamic `import()` in the Artifact | **Closed**: the Artifact probe imported an own `.mjs` with a page-level dynamic `import()` on the owner's iPhone [measured]; the page boots through a classic inline script that imports the entry (section 6.2.2) | |
| 2 | Own `woff2` fonts under the Artifact's font policy | **Closed by revision 2**: the Artifact publishes no font and renders MathML in system maths fonts (decision 37) | |
| 3 | The JSON-part Python layout on the owner's iPhone, and the platform's view of it | **Closed by revision 2**: not built; no Python in the Artifact | |
| 4 | MathLive's shadow DOM and adopted stylesheets in the Artifact | **Closed by revision 2**: MathLive is web only | |
| 5 | Web Locks and file inputs inside the Artifact frame | **Closed**: both work [measured: S1, 7 October 2026]. Web Locks honours `ifAvailable` and `steal: true`, also against a dedicated worker's lock; a file input opened the picker and `FileReader` read the first 64 bytes of the chosen 62,511-byte file; reading a whole backup-sized file was not tried. The heartbeat lease and paste stay as the fallbacks for their absence | |
| 6 | Wheel sizes of SciPy, statsmodels, scikit-learn and matplotlib for Pyodide 314.0.7 | **Closed in review** [measured, section 6.3.3]: the whole stack is 67 MB in 15 files in the JSON-part layout, which revision 2 does not build; the web app's native layout is measured in `docs/PLAN.md` 5.5 | |
| 7 | Whether the Artifact host compresses responses | **Closed**: it does, with gzip: 6.4 KiB on the wire for 62.7 KiB of JSON (`content-encoding: gzip`, Resource Timing's decoded size equal to the body read) [measured: S1, 7 October 2026] | |
| 8 | iPhone memory with pandas plus scikit-learn in one worker, in the web app [unverified] | Those drills need the web app on a computer | E8 |
| 9 | Exact capability declaration keys for `sample` and `downloads` | **Mostly closed**: section 6.2.4 gives the declaration; `db` and `user` are sourced, and the host accepted and stored `db`, `user` and `sample: {}` as sent [measured: S1, 7 October 2026]; the `downloads` entry is open, `{}` in section 6.2.4 and `true` in contract 0.2.73 [sourced: the `artifact-capabilities` skill] (`STATE.md` open question 15), and a wrong one may fail the first publish [unverified] | Checked against the skill at E10 |
| 10 | The total size cap of one Artifact's database | **Closed** [measured: S1, 7 October 2026]: the bounded probe of `docs/PLAN.md` stage 2 wrote 320 documents of 196,608 bytes (62,914,560 bytes, 60 MiB) with no `quota_exceeded` and no `resource_exhausted`, then deleted them; that is above 34 MB times one participant, so the checkpoint fallback of assessment 13.6 is not built | |
| 11 | The Playwright container tag format for 1.63.0 | **Closed at stage 1** [measured]: `mcr.microsoft.com/playwright:v1.63.0-noble` exists, digest in section 3.2 | |
| 12 | Whether `version.json` is cached by the Artifact host despite a query string | **Closed for loads; after a publish, unmeasured** [measured: S1, 7 October 2026]: every own file S1 fetched, `version.json` included, is served with `cache-control: private, max-age=31536000, immutable, no-transform` and `cf-cache-status: DYNAMIC`, and a fetch with a fresh query read the release of its own load on all five runs that made it. Whether an open page could read a stale copy after a publish could not be measured, because the host reloaded the open page on each publish (`platform.version-json-after` was skipped; `docs/PLAN.md` stage 2's version-scoping item is not met, and the emulator default is set by inference pending the owner's waiver or a measurement, `docs/DECISIONS.md` B28); the fallback poll keeps its fresh query and adds `cache: 'no-store'` (section 7.2) | On the device, if a page the host did not reload is ever found (item 14) |
| 13 | `CONTENT-FORMAT.md` sections 12 to 14 against this paper | **Closed in review**: 12.1's compile-time exports, 12.2's `hash32` and `makeWhere`, the runtime-tag change and the C1 to C11 mapping are in sections 0.3, 5.1, 5.3, 5.9 and 13. Section 10.5 (the compiled screen example) was not re-read | |
| 14 | Whether an open page keeps fetching its own version's files after a republish, and whether `location.reload()` loads the newest version | **Closed for a foreground page** [measured: S1, 7 October 2026]: the host reloaded the page open in the foreground on the owner's iPhone to the newest version after each publish, about 4 s and 1 to 2 s after the two publishes (cross-clock), between the batches of one release too. Other open views reload too [sourced: `artifact.d.ts`, contract 0.2.73]; a backgrounded app, a second device and the desktop and web viewers were not measured [unverified], so a page the host does not reload stays possible (risk 14), and whether it keeps fetching its own version's files was not measured (section 8.2; `docs/DECISIONS.md` B28). `location.reload()` reloaded a page already on the newest version (v2 to v2) from the same base path with `sessionStorage` intact [measured: S1, 7 October 2026]; from a page on an older version it is [unverified], because the host had already reloaded the probe. Garbage collection keeps the previous release for rollback and for pages the host did not reload (section 6.2.5); the emulator reloads open pages by default, and its two fault injections can leave one on its version and send its own-file fetches to the newest version; the lazy-chunk row and the retained version are tested on a page carrying both injections ("the host does not reload this page" and "this page's own-file fetches reach the newest version"), at `docs/PLAN.md` stage 83, since stage 4 builds the injections and stage 83 builds garbage collection and retention (section 8.2) | `location.reload()` from an older page: `docs/PLAN.md` stage 83, in the emulator with a page the host does not reload (scenario 17) and in the Self-test on the device if the case ever occurs (section 6.2.6 step 8) |
| 15 | Whether a publish can omit the page, and whether `null` removals count toward 255 paths | **Closed** [measured: S1, 7 October 2026]: the tool refuses a publish without the page before sending, and counts `null` removals against its 255 `files` entries (303 entries were refused and nothing was published; 254, then 49, were accepted). The planner re-sends a page in every publish and counts removals (section 6.2.6) | |
| 16 | Whether the system back gesture in the Claude app walks the frame's history | **Closed, failed** [measured: S1, 7 October 2026]: the gesture does nothing in the frame (no `popstate`, the hash unchanged). The fallback of section 5.8 is in force: every route except the tab roots has its own back or close control, and the router never uses the gesture, `history.back()` or `history.go()`, which `zq/no-forbidden-apis` refuses (section 10.4; `docs/DECISIONS.md` B23) | |
| 17 | Overhead of the `sys.monitoring` soft deadline in Pyodide [unverified] | The watchdog alone remains (decision 31) | E8 |
| 18 | Whether the Artifact page honours an import map in its fragment, and whether the owner's iPhone enforces import-map `integrity` | **Closed by S1** [measured: S1, 7 October 2026]: the classic bootstrap's `import()` and static bare imports resolve through the map to the locked URLs, and two wrong-hash URLs were refused beside a control that loaded; section 6.2.7's design stands, and the UMD fallback of item 6, which also worked, stays named | |
| 19 | Whether a module worker in the Artifact may import from the CDN hosts | **Closed by S1** [measured: S1, 7 October 2026]: a module worker imported classic zod, ts-fsrs and fflate by full URL and ran each, so the main-thread transport is not needed; those imports carry no integrity (`docs/DECISIONS.md` W2) | |
| 20 | MathML quality on the owner's iPhone; slot digits in the swapped `<mn>` against the surrounding maths font; whether `\htmlData` term anchors survive KaTeX's MathML output | **Closed by S1** [measured: S1, 7 October 2026]: KaTeX 0.19.0's MathML lays out natively and the owner accepted all 40 specimen formulas; `TexSlots`' binding left no sentinel text once the TeX annotation was also rewritten (`docs/DECISIONS.md` B20, for the owner); the swapped `<mn>` digits match the maths font, look the same as the `<mtext>` copy, and VoiceOver reads their current values. `\htmlData` does not survive the MathML output, while the HTML output keeps it; no `\html*` command can anchor a term there, since their MathML builder emits the body alone [sourced: KaTeX 0.19.0 `src/functions/html.ts`]. `\textcolor{#0a0001}{b^2}` renders as a scoped `<mstyle mathcolor="#0a0001">` around exactly that term, while `\color` is a switch that nests into later terms, `\htmlId` is dropped and `\class` is undefined [measured: Node, KaTeX 0.19.0, `output: 'mathml'`, 8 October 2026]. **Proposed for the Artifact** (`docs/DECISIONS.md` B27, for the owner): with the runtime flag `artifact.termBinding` on, `TexService`'s authored configuration (in `engine/render`) defines `\htmlData` as a KaTeX function macro that renders `\htmlData{term=<k>}{...}` as `\textcolor{<sentinel colour k>}{...}` and any other attribute as its body alone, the sentinels drawn from a reserved range (`#0a00` followed by two hex digits for $k$) that authored colours may not use. The macro acts at render time, so content bundles, `contentHash`, `answerHash`, tutor context and search are the same on both targets (`docs/PLAN.md` 6.4); the reserved colours (the term range and `errorColor` `#0a0100`) and the sentinel mapping live in `@zq/contracts`, which `engine/render` and `tools/zq` may both import (section 4.5). After rendering, the term binding finds each `mstyle[mathcolor="<sentinel>"]`, removes the `mathcolor` so the term takes the token colour, and sets `data-term`, `role`, `tabindex` and `aria-label` on the `mstyle`, which becomes the term's target, as `TexSlots` swaps its sentinel `<mtext>` (decision 37). With the macro, KaTeX's TeX annotation keeps the authored TeX: `\htmlData{term=ab}{b^2}-4ac` renders an `<mstyle>` with a term-range `mathcolor` around exactly `b^2`, and the annotation reads `\htmlData{term=ab}{b^2}-4ac` [measured: KaTeX 0.19.0 in Node, `output: 'mathml'`, 8 October 2026], so B20, which the owner decides before stage 12, concerns only `TexSlots`' slot sentinels; he decides B27 with stage 25's device result. It serves `live-formula` and every composite with `term:` targets, among them equation-workbench, first-step-solver, binomial-expander, sum-visualiser, generating-function, graph-explorer and dependency-graph (`WIDGETS.md` 4.1.6). Where it is built: the reserved-colour error in `zq check` at `docs/PLAN.md` stage 7; the macro and the binding at stage 12, under the same flag, tested with a hand-written fixture until stage 23's Artifact output exists. The reserved-colour check reads KaTeX's output, not the authored text: stage 7's KaTeX render refuses any rendered colour (`mathcolor` or `color`) in the reserved range `#0a00` followed by two hex digits, compared without regard to case, whatever the colour command or spelling, `\textcolor{0a0001}{x}` and `\textcolor{#0A0001}{x}` included [measured: KaTeX 0.19.0 keeps the authored case, 8 October 2026], with a failing fixture for each. `zq check` always renders the authored source with the authored configuration and reads that output; the macro acts only at run time in the Artifact under its flag, so every reserved colour in the checked output is authored. The `errorColor` `#0a0100` (section 11.3, sink S1; `docs/DECISIONS.md` B33) sits outside the term range and is refused in the same way. Pointer and keyboard interaction on MathML elements in iOS Safari (a click, focus through `tabindex`) is [unverified]. **Floor**: if stage 12's iPhone check, taken in stage 25's preview Artifact, fails, `live-formula` lists its linked terms beside the formula, focusing a term in the list lights its mark, and the reverse; a Stage 0 interaction that degrades then goes to the owner. **Default until the owner decides**: stage 12 builds the term list, the named fallback, and builds the macro and the sentinel binding behind the runtime flag `artifact.termBinding`, off by default. With the binding off, each entry of the term list carries the term's `data-term`, its role, `tabindex` and `aria-label`, so `term:<id>` targets and `set` and `choice` answers bind to the list entries [our choice]. Stage 25's preview build turns the flag on for stage 12's iPhone check, whose result goes to the owner with B27 | `docs/PLAN.md` stage 12's iPhone check, taken in stage 25's preview Artifact (`docs/PLAN.md` 11.1), with `live-formula`, the first widget built on the binding |
| 21 | Which locked files cdnjs serves byte-identically | **Partly closed by S1** [measured: S1, 7 October 2026]: of 14 URLs for seven locked entries, only KaTeX 0.19.0's `katex.mjs` matched; the others failed to import with a load error, not on integrity, so jsDelivr's `/npm/` path for the rest (section 6.2.7 item 1). S1 tried two guessed paths per package, and classic zod, ts-fsrs, idb, MiniSearch and the Compute Engine entry were not tried [unverified: cdnjs unreachable from this sandbox] | `tools/cdn/lock.ts` at stage 4, which checks every locked file against cdnjs's listing, the tried ones included |
| 22 | `zod/mini`'s closure in the Artifact: 92 CDN requests among the static imports, which took 2,783 ms on the first, cold load on the owner's iPhone, zod's requests being 9,393 of the 9,646 ms of summed request time [measured: S1, 7 October 2026]; and 197,653 bytes gzipped file by file, above section 9.2's entry budget [measured: zod 4.6.5 npm tarball, zlib 1.3 level 9 through Python's `gzip`, 8 October 2026] | A slow first visit; the Artifact's entry budget exceeded | The owner's choice among the options of `docs/PLAN.md` 4.3, in `docs/PLAN.md` section 12 row 15 (needed by stage 4; default (a), keep as locked), before stage 4 writes the import map (section 6.2.7 item 7); until then `budgets.ts` reports the Artifact's CDN figures for the entry, the data worker and KaTeX, each as a figure of its own, without failing on them, and our own code keeps its gates (section 9.2; `docs/DECISIONS.md` B36) |

---

## Review log

Adversarial review, 6 October 2026, through three lenses in turn. Each finding names what changed; "measured" means measured during the review (section 0.2).

**Maintainability at content scale by AI authors**

| # | Finding | Change |
|---|---|---|
| R1 | `@zq/compiler` must call widget `logic.ts` and `schema.ts`, but section 4.5 forbade packages importing `src/`: the layering could not be built as written | Decision 33: `CompilerRegistry` injected by `tools/zq` from a generated `registry.node.gen.ts`; layering rows added (4.3 to 4.5, 5.3) |
| R2 | The widget contract lacked what `CONTENT-FORMAT.md` 12.1 requires at compile time: static targets with labels and roles, recipe argument schemas, per-element set metadata | `staticTargets`, `recipeArgs` in `schema.ts` (`WidgetSchemaModule`), `elementMeta`; lifecycle step 1 and the contract suite check them |
| R3 | Presets carry runtime predicates and recipes, but `WidgetRegistry` could not load them and `BaseConfig.preset` was unpinned | `preset: 'type@v'`, `registry.preset()`, `PresetRuntime` (`expand` never bundled) |
| R4 | The fixture format that tests, gallery, storyboard and agents all share was undefined; `fixtures.ts` clashed with `fixtures/state-v<n>.json` | `WidgetFixture` and `FixtureStep` types with pointer, keyboard and tap-then-tap paths; state files moved to `states/` |
| R5 | Three spellings of `hash32` across papers; `makeWhere` assumed by two papers had no interface | Variadic `hash32` with a byte-exact definition (5.1); `GeneratorModule.makeWhere` (5.9) |
| R6 | `PyPackage` said `'scikit-learn'`, the content schema says `'sklearn'`; `hypothesis` is not in Pyodide 314.0.7 [measured] | Enum aligned; `hypothesis` vendored from PyPI into the `testing` group (3.1, 6.3.3) |
| R7 | `CONTENT-FORMAT.md` still carried MicroPython runtime tags and C7 checks; section 0.3 did not list them | Rows added to 0.3: tags and `aim` dropped, placement decided at run time from `needs` |
| R8 | Run-time validation of widget configs was undecided; validating every widget schema in the data worker would grow it with the library | Structural validation plus a SHA-256 check at run time; widget configs at compile time only (5.10.2, 11.2) |
| R9 | Learner-facing strings produced by widget logic escaped the copy lint | The contract suite lints `describe`, `summarise`, labels, captions and annotations for every fixture (8.1.1) |
| R10 | `schema.ts` (classic zod, 92 KB gzipped) could leak into main-thread chunks; `el(id)` identity unstated | `zq/no-schema-import`, generated clusters never import schemas, `size-limit` on every chunk; `el(id)` stable per id |
| R11 | Open question 13: content-format 12 to 14 never cross-checked | Done; stage mapping C1 to C11 added to section 13 |

**Runtime and platform fit**

| # | Finding | Change |
|---|---|---|
| R12 | Decision 16's concatenated `.wasm` packs are not WebAssembly: serving them as `.wasm` sidesteps the served-type list, which `widgets-programming.md` 13.1 had already refused for renamed archives. The raw layout also cannot fit: the scientific stack measured 153 MB raw and 276 side modules | Decision 16 rewritten: JSON parts of each member's original compressed bytes; 15 files and about 67 MB for the whole stack, 24 MB for NumPy and pandas [measured]; CRC-32 and SHA-256 integrity; S1 re-runs the spike with it; the spike's layout is the named fallback; risk 16 |
| R13 | Pyodide sizes were unmeasured and the group closures partly guessed (`libopenblas` is not in SciPy's closure) | Release tarball measured; table in 6.3.3; closures from the lock file |
| R14 | Web offline size "49 MB" was the Artifact spike's uncompressed layout | 21 MB for NumPy and pandas on the web [measured] (6.4.1) |
| R15 | The file budget ignored hash cascades (every app release renames about 40 chunks) and mixed "one release" with "live version" | Per-release, retained and peak limits (6.2.5) |
| R16 | The manifest embedded in the entry chunk made every content fix rename every app chunk: Artifact publish churn and a 1.8 MB web re-precache, for years of content-only releases | Decision 30: manifest as its own hashed file named by a page meta tag; CI asserts a content-only rebuild changes only page, manifest and course |
| R17 | Shared modules were merged into the entry, so primitives used by two clusters would land in the first load | Decision 8: shared widget code goes to `w-core` |
| R18 | The release plan ignored that every publish names the page, the tool's rule against overwriting unlisted paths, and the reserved `preflight.js` | Staging publishes re-send the live page; the session lists files first and stops on drift; `preflight.js` banned (6.2.3, 6.2.6) |
| R19 | "The session opens Diagnostics and runs Self-test": a cloud session cannot operate the page on the owner's phone | The owner runs it; the result goes to `ops/selftest-<release>`; the session reads it with `ArtifactData` |
| R20 | `version.json` may always report the page's own release if published files are version-scoped | Decision 32: `meta/release` in `db`; `version.json` stays for the web and as fallback; S1 and the emulator test both behaviours |
| R21 | The `db` rule set contradicted `ASSESSMENT.md` 12.5, which owns it | Adopted the owning paper's set plus one `meta` rule; declaration keys given (6.2.4) |
| R22 | C++ and shell drills had no runtime contract | `CppRuntime` (web only) and the shell-drill rule (5.9) |
| R23 | Every learner infinite loop cost a worker restart of 3 to 4 s on the iPhone | Decision 31: soft deadline through `sys.monitoring`, watchdog for C code; overhead gate at E8 |
| R24 | Core Pyodide files were not cached and their transfer depended on unknown host compression | Core files cached by hash; core wasm shipped compressed if S1 finds no host compression (6.3.1) |
| R25 | KaTeX font fallback relied on `data:` fonts, governed by the same font policy; the "published prototype" evidence for KaTeX styles has no record in the repository | `FontFace` from fetched bytes as first fallback; KaTeX styles marked [unverified] for S1 |
| R26 | SVG snapshots for the tutor would lose tokens and fonts and taint the canvas in Safari | Inline colours and fonts, labels drawn separately, gated by `limits().images` (5.6) |
| R27 | `workbox-build`, a peer of `vite-plugin-pwa` 2.0.0, was missing from the toolchain | Added (3.2) |

**Learner-experience fidelity**

| # | Finding | Change |
|---|---|---|
| R28 | Single-character shortcuts with no off switch fail WCAG 2.2 SC 2.1.4 (level A) while the paper claims AA; a global Enter would double-fire on focused buttons | Decision 34: Settings switch; Enter acts only when focus is on the screen itself (5.5) |
| R29 | No rule kept Check visible above the iPhone keyboard or matched the keypad to the graders' forms | Decision 35: in-app keypad on touch for numeric and expression answers; `visualViewport` and safe areas for the rest (5.5) |
| R30 | `warm()` would start a 24 MB first download on its own at a lesson's title screen | Download offered with its size; automatic warming only from cache (5.10.2) |
| R31 | Drafts could be lost when iOS ends a backgrounded view | Flush on `visibilitychange` and `pagehide` (5.4) |
| R32 | No rule for the Claude app's back gesture | Every focus and bare screen has its own back or close control; S1 checks the gesture (5.8) |
| R33 | Decision 1 said Lit "is no faster"; it measured faster on the base widget. Section 9.2 quoted a 6x figure as the 4x basis | Wording matches the measurements (0.1, 9.2) |

Stack choices that survived the review: Preact with signals over Lit and no framework, the reducer player, the `Scope` rule, Philox, npm workspaces, Workbox with `injectManifest`, hash routing and one Pyodide worker with two loaders. Decisions 8, 16, 17 and 30 changed and 31 to 35 are new; for every other decision, no rejected alternative was clearly better than the choice.

