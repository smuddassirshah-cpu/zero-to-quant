# Widget catalogue: Stage 0

Blueprint work file, Stage 2 Phase 1. Draft 1, 6 October 2026.

**Scope.** Every interactive widget needed to teach curriculum Stage 0 (0.1 Number, 0.2 Algebra, 0.3 Precalculus, 0.4 Computer basics, 0.5 Mental arithmetic) at the depth a top quantitative programme expects, and to prepare for the Stage 0 exit tests. Widgets that later stages reuse are specified once here, with their later extensions flagged.

**Read for this file.** `docs/curriculum.md`; `docs/design-research.md` sections 2, 4, 5, 8, 9 and 10; the Stage 1 prototype (`css/tokens.css`, `js/core.js`, `js/screens/lesson.js`, `drill.js`, `drill-worker.js`, `exam.js`); the owner's lesson-creator, maths-teaching, code-craft and project-forge skills with `engineering-floor.md` and `blueprint.md`; the Artifact `sample` and `db` contracts (version 0.2.69).

**Evidence tags**, as in the design research: [verified], [sourced], [inferred], [our choice], and [unverified] for anything not yet measured.

---

## 0. Summary

- **76 widgets:** 17 primitives, 6 answer inputs and 53 composites. Section 14 lists them all.
- **All are P0.** Stage 0 is the first part of the depth-first build, so every widget it needs is P0. Where a widget has an extension that only a later stage needs, the spec marks that feature P1 or P2.
- **Build order.** Inside P0 the widgets ship in four waves, W0 to W3, in the order the depth-first lessons first need them (section 13).
- **Generators.** 51 widgets need seeded item generators for practice, homework and exams, and 4 more use seeds to vary authored items (section 12).
- **A second catalogue overlaps.** `widgets-calc-linalg.md` names the same primitives differently and claims some 0.2 and 0.3 topics. Section 15.1 maps them one to one and recommends single ids. Merged, Stage 0 adds 69 to 71 widgets of its own.
- **The Stage 1 reference lesson** rebuilds from five of these widgets with no lesson-specific code (section 2.8).

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Where lessons live | Lessons are JSON data. Widgets are versioned modules configured by that data | Hand-built screen code per lesson | Stage 1's hand-built lesson took 1,316 lines of JS for 12 minutes and still had 23 review defects, mostly in timers, state and XP machinery |
| 2 | Rendering | SVG by default; Canvas 2D for layers over 1,500 marks; our own small scale and layout code | D3, JSXGraph, an embedded GeoGebra, three.js | We need DOM nodes for focus, ARIA and hit testing. The Artifact forbids iframes, which rules out GeoGebra. three.js is about 600 KB for school solids. D3's scales are about 40 lines of our own code |
| 3 | State | Plain JSON state. The view is a pure function of state. Every timer belongs to the screen | DOM as state, as in the prototype | Restore, redo, tutor descriptions and `db` sync all need serialisable state |
| 4 | Grading | Checks live in content data. Widgets emit typed answers and named predicates | Widgets that grade themselves | One checker, tested in CI against every generator's solution |
| 5 | Geometry | A construction graph (derived objects evaluated in dependency order each frame) | A general geometric constraint solver | It is deterministic and fast, and school geometry is constructive. Solvers jitter under drag |
| 6 | Expression equivalence | Compute Engine canonical forms, then seeded numeric probing at 8 points inside the declared domain. Required forms (factorised, simplest) are separate structural tests | String matching; CAS alone | CAS simplification misses some true equivalences. Probing catches them with negligible false positives for the expression sizes in Stage 0 |
| 7 | Terminal | A simulated POSIX shell over a virtual file system, graded by effect, not by keystrokes | An emulated Linux (v86, JSLinux) | Emulators download tens of megabytes, run slowly on phones and do not fit the Artifact |
| 8 | Practice items | Pure seeded generator functions with solver tests in CI | Hand-written item banks only | Unlimited practice, and every instance is proved solvable before it ships |
| 9 | AI tutor access | Each widget exposes `describe`, `targets`, `highlight`, `annotate` and a guarded `preview` | The tutor reads the DOM or a screenshot | Text is cheap, deterministic and works with both tutor transports. The guard stops the tutor previewing the answer |
| 10 | Drag accessibility | Every drag has a tap-then-tap path and a keyboard path | Keyboard path only | WCAG 2.2 success criterion 2.5.7 requires a single-pointer alternative to dragging |
| 11 | Slider control | Native `<input type="range">`, styled | A custom slider | Keyboard, assistive technology and touch behaviour come free |
| 12 | Code editing | A textarea over a synchronised highlighted `<pre>`, as in the prototype | CodeMirror 6 | Stage 0 and 1.1 programs are short. Revisit at 1.8 (P1) if longer programs need folding or multiple cursors |

### 0.2 Finding: the exit tests assess more than the cover lists

The Stage 0 exit test needs content that the 0.1 to 0.3 "Cover" columns do not name.

- **GCSE Higher paper.** Ofqual weights Higher-tier papers as Number 15%, Algebra 30%, Ratio and proportion 20%, Geometry and measures 20%, Probability and statistics 15% [sourced: cognito.org and savemyexams.com summaries of the Ofqual weights]. The cover lists name no geometry beyond trigonometry and vectors, and no statistics. Up to 35% of the paper's marks would be untaught, so 80% is out of reach without them.
- **Khan Academy Precalculus challenge.** The course covers complex numbers, composite functions, trigonometry, vectors, matrices, conic sections, and probability and combinatorics, with optional units on series and on limits and continuity [sourced: Khan's course description as quoted by third-party listings; khanacademy.org was blocked from this environment]. The 0.3 cover list omits complex numbers, matrices, conic sections and limits.

**What this catalogue does.** It covers the exit tests, not only the cover lists. It therefore includes `geometry-board`, `solid-viewer`, six statistics and probability widgets, `complex-plane`, `matrix-grid`, `linear-map`, and `graph-explorer` overlays for limits, rational functions and conics.

**Owner decision needed (curriculum, not widgets).** We recommend adding two courses:

- a Geometry and measures course in 0.3, before trigonometry;
- a Statistics and probability course in 0.3, alongside counting.

Together they need roughly 40 to 60 more hours [our estimate]. The widgets are specified either way, because the exit test needs them.

---

## 1. The contract every widget follows

This catalogue assumes the contract below. If the engine blueprint defines it differently, the engine wins and these specs adapt. The fields each spec lists map one to one onto it.

### 1.1 Module shape

```ts
interface WidgetModule<C, S> {
  id: string;                         // kebab-case, unique, e.g. 'number-line'
  kind: 'primitive' | 'input' | 'composite';
  version: string;                    // semver; lesson data pins the major version
  configSchema: JSONSchema;           // validated at content build time and again at mount
  answerTypes: Answer['type'][];      // what answer() can return
  predicates?: Record<string, (s: S, args?: unknown) => boolean>;   // named state tests a Check can call
  showWhy?: string[];                 // named explanatory animations
  mount(host: HTMLElement, config: C, ctx: WidgetContext): WidgetInstance<S>;
}

interface WidgetContext {
  rng(label: string): () => number;   // seeded stream, from the screen seed plus a label
  reducedMotion(): boolean;
  theme(): 'light' | 'dark';
  announce(text: string, politeness?: 'polite' | 'assertive'): void;   // one shared live region per screen
  later(fn: () => void, ms: number): number;   // timers owned by the screen; cleared on leave and on Try again
  lazy(dep: 'katex' | 'mathlive' | 'cas' | 'python'): Promise<unknown>;
  sound(name: 'tap' | 'snap'): void;
  haptic(ms: number): void;
  mode: 'lesson' | 'practice' | 'quiz' | 'homework' | 'exam' | 'explore';
}

interface WidgetInstance<S> {
  getState(): S;
  setState(s: S, opts?: { animate?: boolean }): void;
  ready(): boolean;                   // enables Check
  dirty(): boolean;                   // enables Start over
  answer(): Answer;
  lock(on: boolean): void;            // inputs locked during evaluating, correct and revealed states
  mark(m: Marking): void;             // recolours answer objects only
  clearMarks(): void;
  showWhy(key: string, params?: unknown): Promise<void>;
  reveal(solution: unknown): Promise<void>;    // hint-indigo outline, never green
  reset(): void;
  describe(level: 'brief' | 'full'): string;  // tutor and screen-reader text, learner-visible facts only
  targets(): { id: string; label: string; role: string }[];
  highlight(ids: string[], style?: 'ring' | 'wash'): void;
  annotate(id: string, text: string): void;
  preview(patch: Partial<S>): 'shown' | 'refused';   // ghost only; the engine guard may refuse
  clearTutor(): void;
  on(ev: 'change' | 'commit', fn: (e: { state: S; summary: string }) => void): () => void;
  resize(): void;
  destroy(): void;
}

type Marking = { result: 'correct' | 'not-yet' | 'partial'; parts?: Record<string, 'correct' | 'not-yet' | 'kept'> };
```

- `change` fires on every state change during a gesture. `commit` fires on release, drop or Enter.
- Each event carries `summary`, a plain sentence such as "Moved A from (1, 2) to (3, 2)". The engine keeps the last 20 summaries as the action log the tutor reads.

### 1.2 Answers and checks

Widgets produce answers. Lesson data holds the checks. One checker module grades every answer type.

```ts
type Answer =
  | { type: 'choice'; ids: string[] }
  | { type: 'numeric'; raw: string; value: number | null; exact?: [bigint, bigint]; unit?: string }
  | { type: 'expression'; latex: string; json: unknown }            // MathJSON
  | { type: 'set'; ids: string[] }                                  // cells, regions, marks, lattice points
  | { type: 'interval'; parts: { lo: number; hi: number; loClosed: boolean; hiClosed: boolean }[] }
  | { type: 'ordering'; ids: string[] }
  | { type: 'mapping'; pairs: [string, string][] }                 // match, bins
  | { type: 'point'; pts: { id: string; x: number; y: number }[] }
  | { type: 'curve'; samples: [number, number][]; features: CurveFeatures }
  | { type: 'state'; state: unknown }                               // graded by a widget predicate
  | { type: 'code'; files: Record<string, string>; entry: string }
  | { type: 'text'; text: string };

type Check =
  | { kind: 'choice'; correct: string[] }
  | { kind: 'numeric'; value: number | string; tol?: { abs?: number; rel?: number; factor?: number };
      dp?: number; sf?: number; forms?: ('integer' | 'decimal' | 'fraction' | 'mixed' | 'percent' | 'standard-form')[];
      requireForm?: 'fraction' | 'simplest-fraction' | 'standard-form'; unit?: string }
  | { kind: 'expression'; equals: string; domain?: string; forms?: ExprForm[] }
  | { kind: 'set'; equals?: string[]; includes?: string[]; excludes?: string[] }
  | { kind: 'interval'; equals: string }                            // e.g. '[3.35, 3.45)'
  | { kind: 'ordering'; order: string[]; partial?: 'per-position' | 'longest-run' }
  | { kind: 'mapping'; pairs: [string, string][] }
  | { kind: 'point'; target: { id: string; x: number; y: number }[]; tol: number }
  | { kind: 'curve'; features: CurveFeatureSpec[]; band?: number }
  | { kind: 'predicate'; name: string; args?: unknown }
  | { kind: 'code'; tests: CodeTest[]; timeLimitMs: number }
  | { kind: 'text'; rubric: { point: string; marks: number }[]; model: string; marking: 'self' | 'ai-advisory+self' };

type ExprForm = 'expanded' | 'factorised' | 'simplest' | 'single-fraction' | 'exact-surd' | 'rationalised'
              | 'vertex' | 'standard-quadratic' | 'index-form' | 'a+bi' | 'polar';
```

- `tol.factor` grades estimates on a log scale: within a factor of 3 of the reference, for example.
- The accepted-answer rule is shown after grading, as design research section 9.4 requires. The checker builds that text from the `Check`.

### 1.3 Misconceptions and show-why

- Every graded screen may list misconceptions: `{ when: Check; id: string; line: string; showWhy?: { key: string; params?: unknown } }`.
- When a wrong answer matches `when`, the verdict chip shows `line` and the widget plays `showWhy(key)`. This is how "the diagram explains" (design research principle 3) without any lesson code.
- Each composite lists the show-why keys it supports.

### 1.4 Interaction baseline

- **Pointer.** Pointer Events with `setPointerCapture`. Geometry is read once at `pointerdown`, and moves are applied in one `requestAnimationFrame` per frame. `touch-action: none` applies to handles only, so the page still scrolls when you touch empty canvas. Every hit area is at least 44 × 44 px.
- **Drag alternatives.** Every drag also works by tap then tap: select the object, then tap the destination. This meets WCAG 2.2 success criterion 2.5.7.
- **Keyboard.**
  - Every manipulable object is focusable. Groups use a roving tabindex.
  - Arrow keys step, Shift + arrow steps ten times, and Home and End go to the limits.
  - For tokens, Space lifts, the arrow keys move and Space drops. Escape cancels a drag and returns the object to where it started.
  - Enter is Check, handled by the engine.
- **Locking.** During `evaluating`, `correct` and `revealed`, inputs lock (design research section 5.4). After Try again, the learner's input stays.

### 1.5 Visual baseline

These rules use the design tokens in `prototype/css/tokens.css`.

- **Learner-movable objects** (handles, tokens, learner curves, selected cells) use manipulable blue: `--manip` #2F6BFF light, #4D8BFF dark. Handles get a 2px white ring and a 1px ink outline. No data series ever uses `--manip`.
- **Given data and curves** use series slots `--s1` to `--s6` in fixed order, with direct labels. Area models and anything else where marks can touch use at most 3 slots.
- **Geometry ink.**
  - Primary strokes: 2px `--ink`.
  - Gridlines: 1px `--line`.
  - Axes: 1.5px `--text-muted`.
  - Targets and constraints: 1.5px dashed ink, 6 on and 4 off.
  - Construction lines: 1px `--text-muted`.
- **Grading** recolours answer objects only: the chosen card, the placed token, the learner's curve or the shaded cells. It never recolours given series.
  - Correct: `--green-strong` border, `--green-fill` wash and a check badge.
  - Not yet: `--amber-frame` border, `--amber-fill` wash and a cross badge.
  - Correct items the learner kept in a wrong answer dim to grey.
- **Reveal** uses a 2px `--hint` outline, so it never reads as success.
- **Tutor highlight** uses a `--pear-200` wash at 60% plus a 2px ink ring that pulses twice. This is the "Point" rung style from design research section 5.5.
- **Tutor ghosts and annotations.**
  - A ghost from `preview` is a dashed 1.5px `--hint` outline at 60% opacity.
  - An annotation is a callout on `--bg-raised` with `--e2`, `--r-sm` corners, a 2px `--hint` left edge and caption-size text.
- **Type.** Labels use the caption token (Archivo 500, 13/18) with `tabular-nums`. Maths uses KaTeX, inheriting `currentColor`.
- **New tokens this catalogue needs** [our choice]:

  | Token | Light | Dark | Use |
  |---|---|---|---|
  | `--manip-lip` | #1F4FCC | #2F6BFF | the 4px lip under draggable tokens |
  | `--ghost` | `--hint` at 60% | `--hint` at 60% | preview ghosts |
  | `--out` | opacity 0.25 | opacity 0.3 | ruled-out cells and branches |

### 1.6 Motion baseline

- **Direct manipulation is never tweened.** Dragged geometry and everything that depends on it redraws on every pointer frame.
- **Springs on release.**
  - `spring-snap` (300ms) for snapping to grids and slots, and for an invalid drop springing back.
  - `spring-physical` (700ms) for beams, pendulum-like tilts and tree reflows.
  - `spring-bounce` (500ms) for check badges, handled by the engine.
- **Consequence animations** play the result of a learner action: tokens fusing, a value travelling through a machine. They use 200 to 400ms with `ease-standard`, and only ever start from a learner action.
- **Show-why animations** use 480 to 800ms with `ease-morph`. They start only after a Check and can be skipped with a tap.
- **Under reduced motion** (the OS setting or the in-app Motion setting):
  - translations and morphs become a stepped before-and-after with a Play button;
  - springs land at once;
  - flashes become a static highlight that stays until the grade clears;
  - autoplay is off;
  - button press still sinks, because it is feedback.

### 1.7 Accessibility baseline

Target: WCAG 2.2 AA.

- **Root.** Each widget root has a role and an accessible name. A non-interactive diagram is `role="img"`, with its label taken from `describe('brief')`.
- **Text alternative.** `describe('full')` is available through a "Describe" control in the card utilities.
- **Table view.** Every chart or plot offers one, built from `data-table`, toggled with T or the card utility.
- **Live updates.** Value changes reach the shared polite live region, debounced to 250ms and summarised ("Gradient 2, intercept −1"). They are never announced per frame.
- **Colour.** Colour never carries meaning alone. Every verdict has an icon and a word. Every series has a direct label. Negative tiles use hatching and a minus sign as well as colour.
- **Focus.** The focus ring is 2px `--focus` with a 2px offset. Focus is never trapped: in the code editor, Escape then Tab leaves.
- **Equivalent input.** Where a widget's main input is spatial (sketching, constructing), a non-spatial input grades against the same check. `curve-sketch`, for example, has a feature form.

### 1.8 AI-tutor hooks

Bertie, the tutor, is the same on both targets. Only the transport differs: the `sample` capability in the Artifact, and the proxy on the web. Widgets see neither.

**`describe(level)`**

- Facts visible to the learner only. It never includes hidden targets, solutions or check data.
- Format: `<Widget>: <state>. Selected: <...>. Shown: <...>.`, with element ids in square brackets.
- `brief` is at most 300 characters and goes into every tutor prompt. `full` is at most 2 KB and is returned by a tool.
- Numbers are rounded as they are displayed on screen.

**Element ids.** `targets()` returns stable kebab-case ids such as `point-A`, `cell-5-3`, `term-2`. The engine prefixes the widget instance when a screen holds several widgets: `w1:point-A`.

**Tools offered to the tutor** (five, small results, matching the `sample` advice to keep tools few and results small):

| Tool | Input | Effect | Returns |
|---|---|---|---|
| `read_screen` | none | Prompt text, each widget's `describe('full')` and `targets()` | at most 4 KB |
| `highlight` | `{ ids: string[] }` (at most 3), `style` | Pear wash and ink ring, pulsing twice | `ok`, or an error naming any unknown id |
| `annotate` | `{ id, text }` (text at most 80 characters) | A callout beside the element | `ok` |
| `preview` | `{ widget, patch }` | A ghost of a possible state | `shown`, or `refused: would reveal the answer` |
| `clear` | none | Removes highlights, annotations and ghosts | `ok` |

**Preview guard.** Before showing a ghost, the engine runs the screen's check on the patched state. If the check passes, or if the patch sets an answer object, the preview is refused.

**Where the tutor is unavailable.** Tutor tools are disabled in quiz, homework and exam modes, which have no hints (design research section 5.5).

**Clearing.** Highlights and annotations clear on the learner's next `commit`.

### 1.9 Performance baseline

- **Reference device** [our choice]: a 2022 mid-range Android phone, such as a Samsung Galaxy A53, on Chrome stable. The day-to-day proxy is desktop Chrome with 4× CPU throttling. Each wave is checked on a real device before it ships.
- **Budgets per widget:**

  | Measure | Budget |
  |---|---|
  | Mount | 50ms or less, excluding lazy dependencies |
  | Script per pointer frame | 4ms or less |
  | Style, layout and paint per frame | 6ms or less |
  | SVG nodes per screen | 1,500 or fewer; above that, the dense layer moves to Canvas 2D under an SVG handle layer |
  | Tap to visible response | INP 200ms or less |

- **KaTeX is never rendered inside a drag loop.**
  - `tex-terms` renders once with addressable slots, and the drag loop writes only slot text.
  - KaTeX re-renders only on `commit`, at most at 10Hz.
- **No layout reads in move handlers.** ResizeObserver callbacks are throttled to animation frames. On `destroy()`, a widget releases its observers, workers and timers.
- **Lazy dependencies** load on screens that need them and preload during the lesson title screen:

  | Dependency | Size | Evidence |
  |---|---|---|
  | KaTeX | about 270 KB plus fonts | [unverified] |
  | MathLive | size not yet measured | [unverified] |
  | Compute Engine | size not yet measured | [unverified] |
  | Pyodide | about 13 MB | measured from the prototype's vendor folder |
  | MicroPython with ulab | about 0.6 MB | from the platform facts |

- **Persisted state.** At most 32 KB per widget instance, and 128 KB for virtual file systems. That keeps one attempt document well under the `db` limit of 256 KiB and 32 levels of nesting. Trees are therefore stored flat, as path maps.

### 1.10 Artifact and web baseline

- **One codebase.** Both targets run the same ES modules. A `platform` adapter supplies storage, tutor transport, the Python runtime, downloads and dependency URLs. Widgets never branch on the platform themselves.
- **Dependencies.**
  - Artifact: pinned versions from `cdn.jsdelivr.net/npm/` with `integrity` attributes.
  - Web: the same versions vendored, so the PWA works offline.
  - Fonts: Google Fonts in the Artifact, vendored on the web.
- **Workers.** In the Artifact a worker starts from a `blob:` URL or one of the Artifact's own files. On the web it starts from its own file.
- **Python.**
  - Web: Pyodide.
  - Artifact: MicroPython with ulab, if the CSP probe shows WebAssembly is allowed [unverified]. Otherwise a handoff to the web app.
  - Stage 0 code is pure Python, so if WebAssembly works, every Stage 0 drill runs in the Artifact.
- **Artifact-only limits.** No `window.open`, no iframes, and no downloads except through the `downloads` capability. On the web, downloads are plain Blob links.
- **Handoff to the web app.** An ordinary anchor to the web app's URL. Whether the Artifact host lets an anchor open an external page is [unverified]. The fallback is the URL shown as copyable text with a Copy button.

### 1.11 Services widgets depend on (not widgets)

| Service | Responsibility |
|---|---|
| `seeded-rng` | Counter-based: draw $k$ of stream $s$ is a hash of (seed, $s$, $k$), the scheme the calculus and linear algebra catalogue specifies for `sim-runner`. Draw $k$ is therefore the same whatever else was drawn. Generators read it as a stream. Chosen over the prototype's mulberry32, whose state is only $2^{32}$ |
| `num-parse` | Integers, decimals, `a/b`, mixed numbers (`2 1/3`), percentages, standard form (`3.2e4`, `3.2×10^4`), money, units, and en-GB separators. The minus sign accepts U+2212. Returns exact rationals where it can |
| `unit-algebra` | Units as maps from base symbol to exponent, with exact cancellation. Used by `unit-chain` and numeric checks with units |
| `cas` | Compute Engine wrapper: parse, canonicalise, `equivalent(a, b, domain)` (CAS first, then 8 seeded probe points), form predicates, solution sets, and `compile(expr)` to a JS function |
| `python-runner` | Worker-based runner with a 5s limit; it terminates and restarts on timeout. Pyodide on the web; MicroPython in the Artifact when allowed. Stdout and stdin capture; per-test events, as in the prototype `drill-worker.js` |
| `vfs` | Virtual file system as a flat map from path to file or folder entry. POSIX path normalisation. Shared by `file-tree`, `shell-sim`, `code-editor` and `workspace-sim` |
| `announce`, `sound`, `haptic`, `motion` | The prototype `core.js` helpers, rebuilt as engine services |

### 1.12 Priority, waves and naming

- **Priority.**
  - P0: needed for Stage 0 through item 1.5, the depth-first first build.
  - P1: the rest of Stage 1 (1.6 to 1.9).
  - P2: Stages 2 and 3.
- **Waves inside P0:**
  - W0: shared primitives and inputs.
  - W1: 0.1 Number, with 0.5 and typing from the first week.
  - W2: 0.2 Algebra, with 0.4 files, terminal and editor.
  - W3: geometry, statistics and 0.3 Precalculus.
- **Naming.** Widget ids are kebab-case nouns. Element ids inside a widget are kebab-case, with indices joined by hyphens: `cell-5-3`.

---

## 2. Lesson by lesson: what the learner must do

Each row is one lesson idea in suggested depth-first order: the action that makes the idea land, and the widgets that provide it. Later sections specify each widget. A lesson's Explore screen uses the same widget in `explore` mode, with no check.

### 2.1 0.1 Number (60 h)

| # | Lesson idea | What the learner manipulates, sees, builds or predicts | Widgets |
|---|---|---|---|
| 1 | Place value: a digit's worth depends on its column; zero holds a place | Builds numbers from blocks, regroups ten ones into a ten, watches blocks fade into digits | `place-value-chart`, `number-line` |
| 2 | Ordering integers and decimals ($0.5$ against $0.45$) | Places numbers on a line, then zooms into a tenth to see hundredths | `number-line` (zoom lens), `place-value-chart` |
| 3 | Addition and subtraction with exchange | Regroups blocks, then does the column method with carries that point back to the blocks | `place-value-chart`, `written-method` |
| 4 | Multiplication as area; the grid method | Splits $23 \times 47$ into four rectangles and enters the partial products | `area-model` |
| 5 | Division as sharing and as grouping; long division | Partitions a bar into groups; steps through long division with remainders | `bar-model`, `written-method` |
| 6 | Negative numbers: direction, adding and subtracting | Jumps along the line; cancels zero pairs of $+1$ and $-1$ counters | `number-line` (jumps), `algebra-tiles` (counters preset) |
| 7 | Multiplying by a negative | Sees $\times(-1)$ as a half-turn of the whole line about 0 | `number-line` (scale and reflect operators) |
| 8 | Order of operations | Evaluates an expression tree from the leaves up, then predicts where $-3^2$ and $(-3)^2$ differ | `expression-tree` |
| 9 | Factors, multiples, primes | Rearranges $n$ tiles into every rectangle; primes make only a single row | `area-model` (array mode) |
| 10 | Prime factorisation, HCF, LCM | Grows a factor tree, then drops the prime factors of two numbers into a Venn diagram | `factor-tree`, `venn-diagram` |
| 11 | Remainders, divisibility, last-digit cycles | Applies $\times 3$ on a mod-10 clock and watches the orbit 3, 9, 7, 1 repeat | `modular-clock` |
| 12 | Fractions as parts and as numbers | Shades parts of a bar; places the same fraction on a line | `bar-model`, `number-line` |
| 13 | Equivalent fractions and simplifying | Refines 3 of 4 parts into 6 of 8; the shaded length does not change | `bar-model` (refine) |
| 14 | Comparing, adding and subtracting fractions | Refines two bars to a common partition, then combines them | `bar-model`, `number-line` |
| 15 | Multiplying fractions | Shades $\frac{2}{3}$ of the columns and $\frac{3}{4}$ of the rows; the overlap is the product | `area-model` (fraction mode) |
| 16 | Dividing fractions: how many $\frac{3}{4}$ fit in 2? | Lays $\frac{3}{4}$-length pieces along a bar of length 2 | `bar-model` (tape), `number-line` |
| 17 | Terminating and recurring decimals; recurring to fraction | Watches long-division remainders cycle; completes the $100x - x$ derivation | `written-method` (remainder tracker), `derivation` |
| 18 | Percentages as hundredths | Paints a 10 × 10 grid; reads percentage, decimal and fraction together | `region-selector` (percent-grid preset) |
| 19 | Percentage of an amount; percentage change; reverse percentages | Drags a marker on linked % and £ scales; finds 100% from 120% | `double-number-line`, `bar-model` |
| 20 | Successive changes, compound interest, depreciation | Chains multiplier chips; sees +50% then −50% leave 75% | `multiplier-chain` |
| 21 | Ratio: sharing, part to part against part to whole | Splits a tape into equal units and labels the parts | `bar-model` (tape) |
| 22 | Direct and inverse proportion, unit rates, best buy | Moves along double number lines; compares two rates at a common amount | `double-number-line`, `graph-explorer` ($y = kx$, $y = \frac{k}{x}$) |
| 23 | Rates, compound measures and unit conversion | Builds a chain of conversion fractions until the units cancel to the target | `unit-chain` |
| 24 | Powers and index notation; index laws | Expands $2^3 \times 2^4$ into a product of 2s and counts the factors | `expression-tree` (expand-powers mode) |
| 25 | Zero and negative indices | Steps down a table of $2^3, 2^2, \dots$, halving each time, through $2^0 = 1$ to $2^{-1}$ | `data-table` (pattern), `number-line` (scale operator) |
| 26 | Roots, fractional indices, surds, rationalising | Sizes a square to area 30 to bracket $\sqrt{30}$; finds square factors in a tree; rationalises step by step | `area-model` (square mode), `factor-tree`, `equation-workbench`, `expression-entry` |
| 27 | Standard form; very large and very small numbers | Shifts digits past the point; places quantities on a log scale | `place-value-chart` (shift), `number-line` (log10) |
| 28 | Rounding, decimal places, significant figures, estimation | Drags a point; rounding bins show where it lands | `number-line` (rounding bins, lens) |
| 29 | Error intervals and bounds | Drags inputs within their intervals and watches the output range sweep out; predicts its ends first | `number-line` (intervals), `bounds-explorer` |
| 30 | Fermi estimation and orders of magnitude | Decomposes a quantity, gives each factor a range on a log scale, compares with the reference | `fermi-estimator` |
| 31 | Rational and irrational; proof that $\sqrt{2}$ is irrational | Orders the proof's lines; writes the key step in their own words | `derivation` (order mode), `free-response` |
| 32 | Binary and other bases | Uses the place-value chart with base 2; regroups pairs | `place-value-chart` (base mode) |

### 2.2 0.2 Algebra (180 h)

| # | Lesson idea | What the learner manipulates, sees, builds or predicts | Widgets |
|---|---|---|---|
| 1 | Letters stand for numbers; substitution | Drops values onto variable leaves and evaluates the tree | `expression-tree` (substitute), `function-machine` |
| 2 | Collecting like terms | Sorts tiles by kind and cancels zero pairs | `algebra-tiles` |
| 3 | Expanding single brackets; the distributive law | Splits a rectangle of width $x + 3$ | `area-model` (symbolic), `algebra-tiles` |
| 4 | Factorising out a common factor | Arranges tiles into a rectangle with a common edge | `algebra-tiles` |
| 5 | Index laws with letters | Expands and regroups factors | `expression-tree`, `expression-entry` |
| 6 | One-step and two-step equations | Removes equal amounts from both pans; runs a machine backwards | `balance-scale`, `function-machine` (inverse) |
| 7 | Unknowns on both sides, brackets, fractions | Removes boxes from both pans, then moves to symbols | `balance-scale`, `equation-workbench` |
| 8 | Forming equations from words | Draws a tape diagram, then writes its equation | `bar-model` (tape), `equation-workbench` |
| 9 | Rearranging formulae (changing the subject) | Undoes the tree from the root inwards | `expression-tree` (solve mode), `equation-workbench` |
| 10 | Linear inequalities; flipping when multiplying by a negative | Solves, then watches the solution set flip on the strip when both sides are multiplied by $-1$ | `number-line` (intervals), `equation-workbench` (solution-set strip), `balance-scale` (tilted) |
| 11 | Coordinates in four quadrants; plotting from a table | Fills a table and plots its points | `graph-explorer` (points with linked table) |
| 12 | Gradient as rate; $y = mx + c$ | Drags two points; the slope triangle and equation update | `graph-explorer` (slope-triangle overlay) |
| 13 | Parallel and perpendicular lines; midpoint and distance | Rotates a line about a point until it is perpendicular; checks $m_1 m_2 = -1$ | `graph-explorer` |
| 14 | Real-life graphs: distance-time, gradient as speed, area under velocity-time | Reads speeds from gradients; fits trapezia under a curve | `graph-explorer` (trapezia overlay) |
| 15 | Simultaneous linear equations | Adds and scales rows; lines pivot about the fixed intersection | `equation-stack`, `graph-explorer` |
| 16 | Expanding double brackets | Fills an $(x + a)(x + b)$ frame with tiles | `algebra-tiles`, `area-model` (symbolic) |
| 17 | Factorising quadratics, including $a \ne 1$ and the difference of two squares | Arranges tiles into a rectangle, then names its sides | `algebra-tiles`, `expression-entry` |
| 18 | Solving quadratics by factorising | Factorises, then reads the roots off the graph | `equation-workbench`, `graph-explorer` |
| 19 | Completing the square; vertex form | Literally completes the square with tiles; drags the vertex of a parabola | `algebra-tiles` (complete-square), `graph-explorer` (vertex form) |
| 20 | Deriving the quadratic formula; the discriminant | Predicts each line of the derivation; lifts a parabola until its roots vanish | `derivation` (predict mode), `graph-explorer` |
| 21 | Quadratic graphs: roots, intercepts, symmetry | Sketches from features | `curve-sketch`, `graph-explorer` |
| 22 | Quadratic inequalities | Builds a sign chart; shades where the parabola is above the axis | `sign-chart`, `graph-explorer` |
| 23 | Linear-quadratic systems; a line and a circle | Substitutes one equation into the other; drags the line and counts intersections | `equation-stack` (substitute), `graph-explorer` |
| 24 | Algebraic fractions | Simplifies, adds and solves step by step | `equation-workbench`, `expression-entry` |
| 25 | Function notation, domain and range | Feeds inputs into a machine; some are rejected | `function-machine`, `graph-explorer` |
| 26 | Composite and inverse functions | Chains machines in both orders; reflects a graph in $y = x$ | `function-machine` (compose, inverse), `graph-explorer` (reflect in $y = x$) |
| 27 | Cubic, reciprocal and exponential graphs | Matches graphs to equations; sketches them | `card-sort` (match), `curve-sketch`, `graph-explorer` |
| 28 | Transformations of graphs | Drags the curve itself and watches $f(x + a)$ and $f(x) + a$ change | `graph-explorer` (parent ghost, curve drag) |
| 29 | The circle $x^2 + y^2 = r^2$ and the tangent at a point | Drags a point on the circle; the tangent stays perpendicular to the radius | `graph-explorer` (circle family, tangent) |
| 30 | Gradient of a curve; rate of change | Slides a chord's second point towards the first | `graph-explorer` (chord and tangent overlays) |
| 31 | Iteration $x_{n+1} = g(x_n)$ | Drags $x_0$ and steps the cobweb; compares rearrangements that converge with ones that diverge | `iteration-cobweb` |
| 32 | Algebraic proof | Orders lines; writes "show that" arguments | `derivation`, `free-response` |
| 33 | Polynomial division; factor and remainder theorems | Divides step by step; tests candidate roots with a slider | `written-method` (polynomial division), `graph-explorer` |
| 34 | Modulus and piecewise functions | Drags piece endpoints; reflects the negative part | `graph-explorer` |
| 35 | Three-variable linear systems (Algebra 2) | Eliminates in a three-row stack | `equation-stack` (three variables) |
| 36 | Linear against exponential growth | Compares adding with multiplying, step by step | `multiplier-chain`, `graph-explorer` |
| 37 | Proportion with powers: $y \propto x^2$, $y \propto \frac{1}{x}$ | Fits $k$ from one pair, then predicts | `graph-explorer`, `double-number-line` |

### 2.3 Geometry and measures (GCSE exit test; see 0.2)

| # | Lesson idea | What the learner does | Widgets |
|---|---|---|---|
| 1 | Angle facts; parallel lines | Drags a transversal; equal angles stay equal | `geometry-board` (angle-facts preset) |
| 2 | Angle sums of polygons | Splits a polygon into triangles from one vertex | `geometry-board` |
| 3 | Perimeter and area; compound shapes | Decomposes shapes into rectangles and triangles | `geometry-board`, `area-model` |
| 4 | Circles: circumference, area, arcs and sectors | Changes the sector angle; arc length scales with it | `geometry-board`, `unit-circle` |
| 5 | Pythagoras, with a dissection proof | Steps through the rearrangement, then uses it | `geometry-board` (keyframes) |
| 6 | Right-angled trigonometry | Scales a triangle; the side ratios stay fixed | `geometry-board` (triangle-lab preset) |
| 7 | Exact trigonometric values | Reads them off equilateral and right isosceles triangles | `geometry-board`, `unit-circle` |
| 8 | Sine rule, cosine rule, area $\frac{1}{2}ab\sin C$, the ambiguous case | Swings a side of fixed length and sees two triangles appear | `geometry-board` (triangle-lab) |
| 9 | Congruence and similarity; area and volume scale factors | Enlarges a shape by $k$; counts $k^2$ tiles and $k^3$ cubes | `geometry-board`, `solid-viewer` |
| 10 | Transformations, including negative and fractional enlargement | Places an image; finds the centre and scale factor | `geometry-board` (transformations preset) |
| 11 | Constructions and loci | Uses compass and ruler tools; arcs stay visible | `geometry-board` (constructions preset) |
| 12 | Bearings and scale drawings | Measures bearings from north clockwise | `geometry-board` (bearings preset) |
| 13 | Volume, surface area, nets, plans and elevations | Rotates solids, paints faces, unfolds nets, snaps to front, side and plan views | `solid-viewer` |
| 14 | 3D Pythagoras and trigonometry | Taps the space diagonal and the right triangle that contains it | `solid-viewer` |
| 15 | Circle theorems | Drags points round a circle; the theorem's angles stay locked | `geometry-board` (circle-theorems preset) |
| 16 | Vector geometry proofs | Builds paths on a lattice of $\mathbf{a}$ and $\mathbf{b}$ | `vector-plane` (lattice) |
| 17 | Units of measure and compound measures | Chains conversions, including the area-unit trap ($\text{cm}^2$ to $\text{m}^2$) | `unit-chain` |

### 2.4 Statistics and probability (GCSE exit test, 0.3 counting)

| # | Lesson idea | What the learner does | Widgets |
|---|---|---|---|
| 1 | Averages and range; the mean as a balance point | Drags data points; the fulcrum tips until it sits under the mean | `dot-plot-stats` |
| 2 | Resistance to outliers: one outlier moves the mean, not the median | Drags one point far out | `dot-plot-stats` |
| 3 | Frequency tables; estimating a mean from grouped data | Fills a table and compares the estimate with the raw mean | `data-table`, `stat-chart` |
| 4 | Bar, pie, line, frequency polygon, stem-and-leaf | Builds and reads each chart | `stat-chart` |
| 5 | Histograms with unequal widths: area is frequency | Sets bin heights so that the areas match the frequencies | `stat-chart` (histogram, area tiles) |
| 6 | Cumulative frequency, quartiles, box plots, comparing distributions | Plots points, then drags reading lines at $\frac{n}{4}$, $\frac{n}{2}$ and $\frac{3n}{4}$ | `stat-chart`, `dot-plot-stats` |
| 7 | Scatter graphs, correlation, lines of best fit, extrapolation | Drags a line to make the total area of the squared-residual squares small | `scatter-fit` |
| 8 | Sampling, bias, capture-recapture | Samples from a seeded population; solves capture-recapture as a proportion | `trial-simulator`, `double-number-line` |
| 9 | The probability scale; equally likely outcomes | Places events on a 0 to 1 line; counts cells | `number-line`, `outcome-grid` |
| 10 | Sample spaces for two events | Shades events on a two-way grid | `outcome-grid` |
| 11 | Relative frequency and expected frequency | Predicts, then runs seeded trials | `trial-simulator` |
| 12 | Venn diagrams and set notation | Sorts elements; shades $A \cup B$, $A \cap B'$ | `venn-diagram` |
| 13 | Tree diagrams; independent and dependent events | Builds branches; updates the second-stage probabilities without replacement | `tree-diagram` |
| 14 | Conditional probability from tables, Venn diagrams and trees | Applies a condition; the grid shrinks | `outcome-grid`, `venn-diagram`, `tree-diagram` |
| 15 | Misleading charts | Expands a truncated axis to zero; the difference shrinks | `stat-chart` (truncated trap) |

### 2.5 0.3 Precalculus (200 h)

| # | Lesson idea | What the learner does | Widgets |
|---|---|---|---|
| 1 | Exponential growth and decay as repeated multiplication | Chains equal multipliers; compares with adding equal steps | `multiplier-chain`, `graph-explorer` (exp family) |
| 2 | Compounding more often tends to $e$ | Raises compounding periods per year from 1 to 365 and beyond; $(1 + \frac{1}{n})^n$ levels off | `multiplier-chain` (compounding mode) |
| 3 | $e^x$: its gradient equals its value | Slides a tangent along $e^x$; the gradient readout matches the height | `graph-explorer` (tangent overlay) |
| 4 | The logarithm as an inverse | Counts the multiplications needed; reflects $10^x$ in $y = x$ | `slide-rule`, `graph-explorer`, `function-machine` (inverse) |
| 5 | Log laws | Adds lengths on log scales to multiply | `slide-rule`, `derivation` |
| 6 | Change of base | Sees that log scales in different bases are proportional | `slide-rule`, `derivation` |
| 7 | Solving exponential equations | Takes logs of both sides, step by step | `equation-workbench` |
| 8 | Log scales and linearising data | Switches the axes to log; curved data turns straight; reads the gradient as the exponent | `scatter-fit` (log axes) |
| 9 | Modelling: half-life, continuous compounding, log returns | Fits a model; adds log returns where simple returns will not add | `graph-explorer`, `multiplier-chain` (log panel) |
| 10 | Radians | Wraps the radius around the circle | `unit-circle` |
| 11 | Sine, cosine and tangent for any angle; signs by quadrant | Drags the point round the unit circle | `unit-circle` |
| 12 | Graphs of the trigonometric functions | Unrolls circle motion into waves | `circle-to-wave` |
| 13 | Amplitude, period and phase | Matches a target wave with the sliders for $A$, $B$, $C$ and $D$ | `circle-to-wave` |
| 14 | Identities, and proving them | Derives $\sin^2\theta + \cos^2\theta = 1$ from the circle; proves identities step by step; checks by overlaying graphs | `unit-circle`, `equation-workbench`, `graph-explorer` |
| 15 | Compound-angle and double-angle formulae | Steps through a rotation proof | `geometry-board` (keyframes), `derivation` |
| 16 | $a\sin x + b\cos x = R\sin(x + \alpha)$ | Adds two phasors; the resultant is one wave | `circle-to-wave` (phasor mode) |
| 17 | Solving trigonometric equations in a range | A horizontal line meets the circle twice per turn | `unit-circle` (horizontal-line overlay), `graph-explorer` |
| 18 | Inverse trigonometric functions | Restricts the domain until the function is one to one, then reflects | `graph-explorer` (domain handles, reflect) |
| 19 | Arc length and sector area in radians | Changes the angle and the radius | `unit-circle`, `geometry-board` |
| 20 | Arithmetic and geometric sequences; nth term | Drags the first term and the difference or ratio | `sequence-lab` |
| 21 | Quadratic sequences and difference tables | Extends the difference table until a row is constant | `sequence-lab` |
| 22 | Recurrence relations and convergence | Iterates; watches terms settle | `sequence-lab`, `iteration-cobweb` |
| 23 | Sigma notation and index shifts | Expands a sum term by term with an index slider | `sum-visualiser` (sigma mode), `expression-entry` |
| 24 | Arithmetic series: Gauss pairing | Drags a rotated copy of the staircase into place to make a rectangle | `sum-visualiser` |
| 25 | Geometric series and the sum to infinity | Fills a square with halves; shifts and subtracts; drags $r$ past 1 | `sum-visualiser` |
| 26 | Annuities, present value and perpetuities | Discounts each payment; sums a geometric series | `sum-visualiser`, `multiplier-chain` |
| 27 | Proof by induction | Supplies the base case and the step; the dominoes fall only if both hold | `induction-chain` |
| 28 | Pascal's triangle and lattice paths | Builds rows by adding; counts paths | `pascal-triangle` |
| 29 | Binomial expansion; $\binom{n}{k}$ | Picks $a$ or $b$ from each bracket; groups the words | `binomial-expander`, `pascal-triangle` |
| 30 | Specific coefficients, approximations, rational powers | Finds the $x^3$ term in $(2 - 3x)^7$; compares a truncated series with the curve | `binomial-expander` |
| 31 | Vector arithmetic, magnitude and direction | Drags tips; adds tip to tail | `vector-plane` |
| 32 | Position vectors; dividing a line in a ratio | Builds $\vec{OP}$ on a lattice | `vector-plane` (lattice) |
| 33 | The dot product and the angle between vectors | Rotates one vector; watches its projection | `vector-plane` (projection) |
| 34 | Vectors in three dimensions (preview) | Rotates the view of 3D arrows | `vector-plane` (3D mode) |
| 35 | The multiplication principle | Fills slots; the counts multiply | `counting-slots`, `tree-diagram` (count mode) |
| 36 | Permutations and factorials | Arranges $r$ of $n$ in order | `counting-slots` |
| 37 | Combinations | Collapses arrangements of the same set into stacks of $r!$ | `counting-slots` (collapse), `pascal-triangle` |
| 38 | Restrictions, repeated letters, circular arrangements | Glues tokens together; divides by repeats | `counting-slots` |
| 39 | Probability by counting | Counts favourable over total; checks by simulation | `counting-slots`, `trial-simulator` |
| 40 | Inclusion-exclusion | Counts the regions of a three-set Venn diagram | `venn-diagram` |
| 41 | Stars and bars (extension) | Drops dividers between identical stars | `counting-slots` (stars-and-bars mode) |
| 42 | Complex numbers: arithmetic and the Argand plane | Drags $z$ and $w$; multiplying rotates and scales | `complex-plane` |
| 43 | Complex roots of quadratics | Lifts a parabola off the axis; the roots leave the real line as a conjugate pair | `complex-plane` (linked quadratic) |
| 44 | Modulus-argument form; roots of unity | Drags along rays and circles; sets $n$ | `complex-plane` |
| 45 | Rational functions: asymptotes and holes | Drags the factors of the numerator and denominator | `graph-explorer` (asymptote and hole overlays), `sign-chart` |
| 46 | Conic sections | Traces the points equidistant from a focus and a directrix; uses the two-pin string construction for the ellipse | `geometry-board` (conic-locus preset), `graph-explorer` (implicit curves) |
| 47 | Matrices: operations, determinants, inverses, solving systems | Multiplies row by column; inverts a 2 × 2 matrix | `matrix-grid`, `equation-stack` |
| 48 | Matrices as transformations | Drags $\hat{\imath}$ and $\hat{\jmath}$; the grid and the unit square follow | `linear-map` |
| 49 | Limits and continuity | Approaches $a$ from both sides; reads a table of values; finds the hole | `graph-explorer` (approach overlay), `data-table` |
| 50 | Parametric curves | Drags $t$ along a curve traced by $(x(t), y(t))$ | `graph-explorer` (parametric curves) |

### 2.6 0.4 Computer basics (40 h, from week 1)

| # | Lesson idea | What the learner does | Widgets |
|---|---|---|---|
| 1 | Touch typing: home row, letters, numbers, symbols | Types adaptive pseudo-words; keys unlock as speed and accuracy pass the bar | `typing-trainer` |
| 2 | Keyboard shortcuts | Drills copy, paste, undo, save and select-all, with the right keys for their OS | `typing-trainer` (shortcuts mode) |
| 3 | Files and folders; paths; extensions | Moves files between folders; types paths; moves the "you are here" pin | `file-tree` |
| 4 | Installing Python and an editor | Follows OS-specific steps and verifies each by pasting command output | `setup-checklist` |
| 5 | The terminal: `pwd`, `ls`, `cd`, `mkdir`, `touch`, `mv`, `cp`, `rm` | Types commands; a tree beside the terminal shows each effect | `shell-sim`, `file-tree` |
| 6 | Running a script and reading errors | Runs `python3 hello.py` from the wrong folder and reads "No such file or directory" | `shell-sim`, `code-editor` |
| 7 | First programs: values, variables, strings, `print`, `input`, `if`, `for`, functions (Automate the Boring Stuff chapters 1 to 3) | Edits and runs code against visible examples, then hidden tests; traces evaluation order | `code-editor`, `expression-tree` (Python mode), `function-machine` |
| 8 | The editor workflow: save, run, fix | Makes a folder and a file; unsaved changes do not run | `workspace-sim` |
| 9 | Exit item: a ten-line script, run from the terminal on your own machine | Runs a seeded task locally; pastes the script and its output for verification | `setup-checklist` (exit task), `workspace-sim` (rehearsal) |

### 2.7 0.5 Mental arithmetic (20 h, then 10 minutes a day)

| # | Lesson idea | What the learner does | Widgets |
|---|---|---|---|
| 1 | Times tables to 12 | Sees commutativity fold the grid in half; drills the slow cells on their heat map | `times-table-grid`, `speed-drill` (deck) |
| 2 | Two-digit addition and subtraction | Counts up and compensates on a number line, then drills | `strategy-trainer`, `speed-drill` |
| 3 | Two-digit multiplication | Splits on the area model; uses difference of squares and near squares | `strategy-trainer`, `speed-drill` |
| 4 | Fractions to decimals | Learns the anchors: eighths, sevenths, ninths, twelfths | `speed-drill` (fractions-decimals deck), `strategy-trainer` |
| 5 | The daily Zetamac-format run | 120 seconds, auto-advance on a correct answer | `speed-drill` |
| 6 | Estimation | Gives answers within a tolerance; Fermi warm-ups | `speed-drill` (estimation deck), `fermi-estimator` |

### 2.8 Check: the Stage 1 reference lesson, rebuilt

The hand-built lesson (`prototype/js/screens/lesson.js`, "Shrinking the sample space") maps onto catalogue widgets as follows. No lesson-specific code remains.

| Prototype screen | Widgets and configuration |
|---|---|
| `sShade` | `outcome-grid` (6 × 6 dice; task `shade`; event "total is 8"); misconception lines and the `point` hint come from data |
| `sFirstFive` | `outcome-grid` (condition "first die is 5", entering with the `shrink` animation) + `choice-cards` (4 options, each distractor with a `peek` or `flash` show-why) |
| `sCross` | `outcome-grid` (condition "at least one 5", `cross5` outline) + `numeric-entry` (unit "outcomes"; misconceptions 12, 10, 6, 36, 25, each with a show-why) |
| `sTen` | `outcome-grid` + `choice-cards` |
| `sDerive` | `derivation` (fill mode, choice input, live slot) |
| `sSimulate` | `numeric-entry` + `trial-simulator` (dice, filter "at least one 5", event "total 10", `predictFirst: true`, seed 4226) |
| `sStocks` | `outcome-grid` (2 × 2 with custom labels "A up", "B down"; condition "at least one up") + `choice-cards` |
| Quiz items | `choice-cards`, `numeric-entry` |

---

## 3. Primitives

Primitives are building blocks that composites assemble, but each can also stand alone on a screen. Every primitive is P0, wave W0, unless marked otherwise.

### 3.1 `plot-axes`: Plot axes

**Primitive · P0 · W0.** The 2D coordinate frame for every graph, plane and chart. It owns the world-to-screen transform, the grid, the ticks, the labels, the layer stack and the table-view hook.

- **Serves:** 0.1 proportion graphs; all of 0.2; GCSE coordinate geometry and charts; 0.3 trigonometry, vectors, complex numbers and conics; later 1.3 to 3.
- **Uses:** none. Layers (`curve-layer`, `geo-layer`, `bar-layer`, `draggable-point`) register with it.
- **Interactions.**
  - Pointer: optional pan by dragging empty canvas; pinch, or Ctrl + wheel, to zoom; double tap to reset; a `canvas-tap` event with world coordinates, for placing points. Pan and zoom are off by default because they fight page scrolling.
  - Keyboard: if pan or zoom is on, the frame is a tab stop. Arrows pan by one major tick, + and − zoom, and 0 resets.
- **State:** `{ view: { xmin, xmax, ymin, ymax } }`, saved only when pan or zoom is on.
- **Answers:** none of its own. `canvas-tap` lets a host produce `point`.
- **Config:**
```ts
interface PlotAxesConfig {
  x: AxisSpec; y: AxisSpec;
  aspect?: 'equal' | 'free';                       // 'equal' for geometry, vectors, circles
  grid?: 'major' | 'minor' | 'none' | { lattice: [[number, number], [number, number]] };   // skewed basis grid
  pan?: boolean; zoom?: boolean | { min: number; max: number };
  height?: { mobile: number; desktop: number } | 'square';
  tableView?: boolean;
}
interface AxisSpec {
  min: number; max: number; label?: string;
  scale?: 'linear' | 'log10' | 'ln' | 'log2';
  ticks?: number[] | 'auto' | 'pi';
  tickFormat?: 'number' | 'fraction' | 'pi' | 'percent' | 'sci' | 'deg';
}
```
- **Visual:**
  - Gridlines 1px `--line`; axes 1.5px `--text-muted`.
  - Tick labels in the caption token with tabular figures. π ticks are KaTeX fractions rendered once.
  - Log axes: decade lines at full strength, with 2 to 9 minor lines at 50%.
  - The origin label "O" is optional.
- **Motion:** pan and zoom are direct. A programmatic `setView`, as in a show-why zoom, tweens over 480ms with `ease-morph`.
- **Reduced motion:** `setView` jumps.
- **Accessibility:**
  - `role="img"` when nothing inside is interactive, otherwise `role="group"`, named from `describe('brief')`.
  - The table view gathers data from every layer.
  - View changes are announced: "Showing x from −2 to 8".
- **Tutor:**
  - Describe: "Axes: x −5 to 5, y −5 to 5, equal aspect. Layers: line L1 y = 2x + 1; point A (1, 3)."
  - Targets: `axis-x`, `axis-y`, `origin`, plus layer targets.
- **Performance:** SVG, at most 60 grid lines. Ticks regenerate only on view change. A single affine transform is shared by all layers.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.2 `number-line`: Number line

**Primitive · P0 · W0.** A one-dimensional line for order, size, operations as motion (jumps, scaling, reflection), intervals, rounding and zooming.

- **Serves:** 0.1 negatives, placing fractions and decimals, rounding, bounds, error intervals, standard form; 0.2 inequalities; 0.3 log scales and sign charts; 0.5 estimation; later 1.5 (values of a random variable) and 1.6 (confidence intervals).
- **Uses:** `draggable-point` (x-only constraint).
- **Interactions.**
  - Pointer:
    - Tap to place a point. Drag points.
    - Drag interval endpoints. Tap an endpoint to toggle open or closed.
    - Drag from a point to draw a jump arrow.
    - Tap a segment to open a ×10 zoom lens beneath it.
  - Keyboard: points and endpoints are sliders. Space toggles open or closed on a focused endpoint. Z opens the lens at the focused point. Delete removes a point the learner placed.
- **State:** `{ points: {id, x}[], intervals: {id, lo, hi, loClosed, hiClosed}[], jumps: {from, by, op}[], lens?: {centre, factor} }`.
- **Answers:**
  - `point`;
  - `interval`;
  - `ordering` (labelled points from left to right);
  - `numeric` (a value read off the line).
- **Config:**
```ts
interface NumberLineConfig {
  min: number; max: number; scale?: 'linear' | 'log10';
  ticks?: { major: number; minor?: number; labels?: 'number' | 'fraction' | 'decimal' | 'none' };
  snap?: number | 'ticks' | 'none';
  points?: { id: string; x: number; label?: string; tex?: string; movable?: boolean }[];
  intervals?: { id: string; lo: number; hi: number; loClosed: boolean; hiClosed: boolean; movable?: boolean }[];
  allowAdd?: { points?: number; intervals?: number };      // how many the learner may add
  operators?: ('jump' | 'scale' | 'reflect')[];
  lens?: boolean;
  rounding?: { to: number; show: 'bins' | 'none' };        // shades the rounding bins, e.g. to the nearest 0.1
}
```
- **Visual:**
  - The line is 2px ink. Fixed points are ink; learner points are `--manip` handles.
  - Intervals are a 6px `--manip-wash` bar. A filled circle marks a closed end and a hollow circle an open end, the UK school convention.
  - Jumps are arcs with arrowheads labelled "+3".
  - The lens is a magnified strip below, joined to the segment by dashed lines.
  - Rounding bins are alternate `--bg-sunken` bands, with the boundary values labelled.
- **Motion:** dragging is direct; release snaps with `spring-snap`. Show-why keys:
  - `jump`: a token travels the arc, 480ms;
  - `scale`: the line stretches about 0;
  - `reflect`: a half-turn about 0, which returns in complex numbers.
- **Reduced motion:** jumps are drawn at once; `scale` and `reflect` become before-and-after with Play.
- **Accessibility:** points are `role="slider"` with `aria-valuetext` such as "A at 2.75". Intervals read as "from 3.35, included, to 3.45, not included". The table view lists points and intervals.
- **Tutor:**
  - Describe: "Number line 0 to 1, ticks every 0.1. Learner point A at 0.37. Interval [0.3, 0.4)."
  - Targets: `tick-<value>`, `point-<id>`, `interval-<id>`, `lens`.
- **Performance:** SVG, under 150 nodes. A drag updates one transform.
- **Artifact / web:** identical.
- **Generator:** yes, as the host for placement, rounding and interval items (section 12).

### 3.3 `curve-layer`: Curve layer

**Primitive · P0 · W0.** Draws curves on `plot-axes`:

- explicit, parametric, polar and implicit curves;
- piecewise curves;
- sampled data;
- step functions.

It breaks lines correctly at discontinuities.

- **Serves:** 0.1 proportion; every function graph in 0.2 and 0.3; later calculus (1.3), PDFs and CDFs (1.5), payoffs (1.7).
- **Uses:** the `cas` service (`compile`) for expressions.
- **Interactions.**
  - Pointer: optional trace. Touching near a curve shows a snapped point with coordinates. Hosts receive `curve-tap`.
  - Keyboard: when trace is on, arrows move the trace point along the curve by one x-step.
- **State:** trace position only.
- **Answers:** `point` (traced position), `numeric` (a value read off).
- **Config:**
```ts
type CurveSpec =
  | { id: string; type: 'explicit'; expr: string; domain?: [number, number] }
  | { id: string; type: 'parametric'; x: string; y: string; t: [number, number] }
  | { id: string; type: 'polar'; r: string; theta: [number, number] }
  | { id: string; type: 'implicit'; expr: string }                 // F(x, y) = 0
  | { id: string; type: 'piecewise'; pieces: { expr: string; domain: [number, number]; ends: ['open' | 'closed', 'open' | 'closed'] }[] }
  | { id: string; type: 'data'; points: [number, number][]; join: 'line' | 'step' | 'none' };
interface CurveLayerConfig {
  curves: (CurveSpec & { slot?: 1 | 2 | 3 | 4 | 5 | 6 | 'manip' | 'target'; label?: string; trace?: boolean; params?: string[] })[];
}
```
- **Sampling.**
  - Start with 200 samples across the view.
  - Subdivide where the direction turns by more than 10° or $\lvert \Delta y \rvert$ exceeds a fiftieth of the view height. Stop at 2,000 points.
  - Break the path where a value is not finite, or where $\lvert \Delta y \rvert$ exceeds twice the view height with a sign change. This stops false vertical joins on $\tan x$ and $\frac{1}{x}$.
  - Implicit curves use marching squares on an 80 × 80 grid.
- **Visual:**
  - Curves are 2.5px in their slot colour, with a direct label at the curve end.
  - Targets are 1.5px dashed ink.
  - Learner-controlled curves are `--manip`.
  - Asymptotes are 1px dashed `--text-muted`.
  - Holes are hollow circles; closed ends are filled.
- **Motion:** when a parameter changes, the curve redraws each frame. Show-why `morph` interpolates sampled y-values between two curves on the same domain, over 600ms.
- **Reduced motion:** the morph becomes before-and-after.
- **Accessibility:** each curve has a spoken form from `cas` ("y equals 2 x plus 1") and contributes rows to the table view at tick x-values.
- **Tutor:**
  - Describe: "Curve f: y = x² − 4 (slot 1)." It never names features of a hidden target curve.
  - Targets: `curve-<id>`, `asymptote-<k>`, `hole-<k>`.
- **Performance:** a compiled function at 2,000 points costs about 0.3ms. Path building is under 1ms. Four live curves per frame stay inside the 4ms budget.
- **Artifact / web:** identical. `cas` is lazy-loaded; plain expressions use a small built-in compiler, so simple graphs do not wait for the full CAS.
- **Generator:** no.

### 3.4 `geo-layer`: Geometry layer

**Primitive · P0 · W0.** Geometric marks, with a construction graph for derived objects.

- **Marks:**
  - points, segments, rays, lines, polygons;
  - circles, arcs, sectors;
  - angle markers (and right-angle squares);
  - arrows (vectors), braces, labels;
  - equal-length ticks and parallel-arrow marks.
- **Derived objects:** midpoint, intersection, foot of perpendicular, projection onto an axis, rotation, reflection, dilation, translation, point on a circle at an angle, circumcircle, perpendicular bisector, angle bisector, parallel through a point, tangent at a point.
- **Serves:** every geometry, vector, unit-circle and diagram screen.
- **Uses:** none.
- **Interactions.**
  - Pointer: tap selectable marks ("tap the alternate angle").
  - Keyboard: Tab through selectable marks; Space selects.
- **State:** selected mark ids.
- **Answers:** `set`, `choice`.
- **Config:**
```ts
interface GeoLayerConfig {
  objects: GeoObjectSpec[];     // each: { id, type, deps (ids or values), style?: 'primary' | 'construction' | 'target' | 'slot-n', label?, tex? }
  selectable?: string[];
  maxSelect?: number;
}
```
- **Construction graph:** objects are evaluated in topological order on each frame. A cycle is a build-time error caught by schema validation.
- **Visual:**
  - Primary strokes 2px ink; construction lines 1px `--text-muted`.
  - Angle arcs 1.5px with degree labels.
  - Selected marks 3px `--manip`.
  - Grading recolours selected marks only.
- **Motion:** derived objects follow each frame. Show-why keys:
  - `flash`: a pear wash twice at 150ms;
  - `morph`: free points interpolated, 600ms.
- **Reduced motion:** a static highlight.
- **Accessibility:** each selectable mark is a button named in words ("Angle ABC, 40 degrees", "Side AB, 5 cm"). Other marks are summarised in `describe`.
- **Tutor:** any mark id can be highlighted or annotated. Describe lists named objects with their visible measures.
- **Performance:** at most 300 marks. The graph evaluates in O(n) per frame, and intersections are analytic.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.5 `bar-layer`: Bar layer

**Primitive · P0 · W0.** Data marks on `plot-axes`:

- bars, grouped or stacked;
- histogram bins of variable width;
- stacked dot plots;
- a box-plot glyph;
- interval bars.

- **Serves:** GCSE statistics; `multiplier-chain`; `sequence-lab`; `trial-simulator`; later 1.5 distributions and 1.6.
- **Uses:** `plot-axes`.
- **Interactions.**
  - Pointer: drag a bar's top handle to set its height when the bar is editable; tap to select.
  - Keyboard: editable bars are vertical sliders; Space selects.
- **State:** bar values (when editable) and the selection.
- **Answers:** `state` (values), `set` (selected bars).
- **Config:**
```ts
interface BarLayerConfig {
  orientation?: 'vertical' | 'horizontal';
  bins?: { id: string; lo: number; hi: number; value: number; editable?: boolean }[];
  bars?: { id: string; category: string; values: number[]; editable?: boolean }[];
  mode?: 'grouped' | 'stacked';
  valueIs?: 'height' | 'area';          // 'area': histogram with frequency density on y
  snap?: number;
  dots?: { id: string; x: number; movable?: boolean }[];
  box?: { min: number; q1: number; median: number; q3: number; max: number; outliers?: number[] };
}
```
- **Visual:**
  - Bars use slot colours with a 2px gap and no gradients.
  - An editable bar carries a 24 × 6 px `--manip` pill at its top, with a 44px hit area.
  - Value labels sit above bars in the caption token.
  - The box plot is drawn in ink outline.
- **Motion:** heights drag directly and snap on release. Show-why `area` tiles a bin with unit squares over 480ms.
- **Reduced motion:** the tiling appears at once.
- **Accessibility:** the table view lists category or bin with value. Editable bars are sliders: "Bin 10 to 20, frequency density 2.4".
- **Tutor:**
  - Describe: "Histogram: 0 to 10 density 1.2; 10 to 30 density 2.4; ..."
  - Targets: `bin-<lo>-<hi>`, `bar-<category>`, `box`.
- **Performance:** SVG up to 200 marks; Canvas 2D beyond, for large simulator histograms.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.6 `draggable-point`: Draggable point

**Primitive · P0 · W0.** The universal handle: a point the learner moves under a constraint.

- **Serves:** every graph, geometry, vector, statistics and probability composite.
- **Uses:** the host's `plot-axes` transform.
- **Interactions.**
  - Pointer: `pointerdown` within the 44px hit radius captures the pointer. Moves apply once per frame; `pointerup` commits. Escape during a drag returns the point to where it started.
  - Two-tap path: tap the handle to select it, then tap the destination.
  - Keyboard: arrows move by the constraint's step (a grid unit, or 1° on a circle), Shift ten times; Home and End go to the ends of the constraint; Enter commits.
- **State:** `{ id, x, y, t? }`, where `t` is the parameter on a curve or circle.
- **Answers:** `point`.
- **Config:**
```ts
interface DraggablePointConfig {
  id: string; x: number; y: number; label?: string;
  constraint?:
    | { type: 'free' } | { type: 'grid'; step: number } | { type: 'curve'; curve: string }
    | { type: 'segment' | 'line'; a: string; b: string } | { type: 'circle'; centre: string; r: number | string; stepDeg?: number }
    | { type: 'axis'; axis: 'x' | 'y' } | { type: 'region'; polygon: [number, number][] } | { type: 'set'; positions: [number, number][] };
  snapOnRelease?: number;
  bounds?: { xmin: number; xmax: number; ymin: number; ymax: number };
  keyboardStep?: number;
  role: 'answer' | 'control';        // answer handles take grading colours; control handles never do
  showCoords?: boolean;
}
```
- **Visual:**
  - A 20px `--manip` disc with a 2px white ring and a 1px ink outline.
  - While dragged: scale 1.1 and `--e2` shadow.
  - Coordinates appear above in the caption token when `showCoords` is set.
- **Motion:** never tweened during a drag. On release, it snaps or springs back with `spring-snap`.
- **Reduced motion:** snaps are instant.
- **Accessibility:**
  - A one-dimensional constraint gives `role="slider"`.
  - Otherwise the handle is a button with `aria-roledescription="draggable point"` and instructions.
  - The position is announced on key-up, debounced: "A at (2, 3)".
- **Tutor:** target `point-<id>`. `preview` draws a dashed ghost at the proposed position, subject to the guard.
- **Performance:**
  - World coordinates come from the cached inverse transform.
  - Projection costs O(1), except on a curve: a coarse search of cached samples plus local refinement, under 0.2ms.
  - One transform is written per frame.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.7 `slider`: Slider

**Primitive · P0 · W0.** Sets a numeric parameter; dependent geometry redraws live.

- **Serves:** every explorer composite; `area-model`; `bar-model`; `multiplier-chain`; `circle-to-wave`.
- **Uses:** a native `<input type="range">`.
- **Interactions.**
  - Pointer: drag the thumb, or tap the track to jump.
  - Keyboard (native): arrows, Page Up and Page Down, Home and End. Shift + arrow steps ten times, added by us.
- **State:** `value`.
- **Answers:** `numeric`, when the slider value itself is the answer ("set $k$ so the line passes through P").
- **Config:**
```ts
interface SliderConfig {
  id: string; label: string;                    // label may hold $...$ maths
  min: number; max: number; step: number; value: number;
  scale?: 'linear' | 'log';
  ticks?: number[] | 'step'; snapTo?: number[];
  format?: 'number' | 'fraction' | 'percent' | 'deg' | 'rad-pi' | 'money';
  showValue?: 'above' | 'inline' | 'hidden';
  role: 'answer' | 'control'; locked?: boolean;
}
```
- **Visual:**
  - A 4px `--line` track; the filled part is `--manip`.
  - A 24px `--manip` thumb with a white ring and a 44px hit area.
  - The value label sits above the thumb, with tabular figures.
  - The KaTeX label sits to the left (design research section 5.3, item 5).
- **Motion:** direct. Release snaps to `snapTo` with `spring-snap`.
- **Reduced motion:** instant.
- **Accessibility:** native semantics, with `aria-valuetext` in words and units ("gradient m equals 2"). Log scales map 0 to 1,000 internally onto the log range.
- **Tutor:**
  - Describe: "m = 2 (range −5 to 5)".
  - Target: `slider-<id>`.
- **Performance:** one `input` event per frame; dependents update in `requestAnimationFrame`.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.8 `region-selector`: Region selector

**Primitive · P0 · W0.** Tap to select or shade. Modes:

- `grid`: labelled cells;
- `shapes`: arbitrary paths from the host, such as Venn regions or polygon faces;
- `half-plane`: the sides of boundary curves;
- `paint`: drag across cells to set many at once.

- **Serves:** sample spaces; percentage grids; `venn-diagram`; `inequality-regions`; `pascal-triangle`; `times-table-grid`; surface-area painting.
- **Uses:** none.
- **Interactions.**
  - Pointer: tap toggles. In paint mode, the first cell's new state applies to every cell the drag crosses.
  - Keyboard: a grid uses a roving tabindex, with arrows to move and Space to toggle. Shapes follow the host's tab order.
- **State:** `selected: string[]`.
- **Answers:** `set`; `numeric` (the count or fraction shaded).
- **Config:**
```ts
interface RegionSelectorConfig {
  mode: 'grid' | 'shapes' | 'half-plane' | 'paint';
  grid?: { rows: number; cols: number; cellLabel: string; rowLabels?: string[]; colLabels?: string[] };   // cellLabel is a template, e.g. '{r}, {c}'
  shapes?: { id: string; path: string; label: string }[];
  max?: number;
  counter?: 'count' | 'fraction' | 'percent' | 'none';
  preset?: 'percent-grid' | 'dice' | 'coin-die' | 'cards';
}
```
- **Visual:**
  - Cells use `--bg-surface` with a 1px `--line` border, and selected cells `--manip-wash` with a 2px `--manip` border.
  - Graded states follow section 1.5.
  - Ruled-out cells use `--out` and are not focusable.
- **Motion:** an 80ms press. Show-why keys:
  - `flash`: twice at 150ms;
  - `shrink`: out-of-condition cells dim with a 50ms stagger per row, as in the prototype.
- **Reduced motion:** a static highlight, with no stagger.
- **Accessibility:** grid mode is `role="grid"` with toggle buttons (`aria-pressed`) and full labels such as "First die 5, second die 3". The running count reaches the live region and the question line.
- **Tutor:**
  - Describe: "6 × 6 grid; shaded: (2,6) (3,5) (4,4); 3 shaded."
  - Targets: `cell-<r>-<c>`, `region-<id>`, `row-<r>`, `col-<c>`.
- **Performance:** at most 400 DOM cells; 52 for cards, 144 for times tables.
- **Artifact / web:** identical.
- **Generator:** no (its hosts generate).

### 3.9 `token-tray`: Token tray

**Primitive · P0 · W0.** Place-and-sort machinery. Draggable tokens move between a tray, zones and ordered slots, under these rules:

- **combine:** ten tokens fuse into one;
- **split:** the reverse of combine;
- **cancel:** a positive and a negative token make a zero pair and vanish;
- **glue:** two tokens become a block;
- **supply:** an unlimited source.

- **Serves:** place value, algebra tiles, the balance scale, the function machine, unit chains, card sorts, counting slots, multiplier chips, file moves.
- **Uses:** none.
- **Interactions.**
  - Pointer: drag a token. It lifts (scale 1.03, `--e2`, lip drops), the siblings slide aside, and it drops into a zone or slot.
  - Two-tap path: tap the token, then tap the destination. This is the default on coarse pointers.
  - Keyboard: Space lifts; arrows move between slots and zones, announced as they go; Space drops; Escape cancels; Delete returns the token to the tray.
- **State:** `{ placements: Record<tokenId, zoneId | slotId | 'tray'>, order: Record<zoneId, tokenId[]>, spawned: TokenRecord[] }`.
- **Answers:** `ordering`, `mapping`, `set`, `state`.
- **Config:**
```ts
interface TokenTrayConfig {
  tokens: { id: string; label: string; tex?: string; kind?: string; value?: number; supply?: number | 'infinite' }[];
  zones: { id: string; label?: string; capacity?: number; ordered?: boolean; accepts?: string[] }[];
  rules?: { combine?: { kind: string; count: number; into: string }[]; split?: { kind: string; into: string; count: number }[];
            cancel?: [string, string][]; glue?: boolean };
  twoTap?: boolean | 'auto';
}
```
- **Visual:**
  - Tokens use the `lip-token` style: a 2px `--manip` border and a 4px `--manip-lip` bottom edge, with an `--bg-surface` face and an ink label.
  - Zones are 1.5px dashed `--line-control` with `--r-md` corners. Slots are dashed boxes the size of a token.
- **Motion:**
  - Lift takes 80ms. A drop snaps with `spring-snap`, and siblings slide aside over 200ms.
  - Combine: the tokens converge and fuse over 400ms with `ease-morph`, a consequence of the learner's action.
  - Cancel: the pair slides together and fades over 300ms.
- **Reduced motion:** lift and drop are instant. Combine and cancel cross-fade.
- **Accessibility:** tokens are buttons with `aria-roledescription="draggable"`. The live region narrates: "Lifted 3x. Over left pan, position 2. Dropped." Zones are lists.
- **Tutor:**
  - Describe: "Tray: x, x, 1, 1, 1. Left pan: x, x, x, 1, 1. Right pan: x, 1 × 8."
  - Targets: `token-<id>`, `zone-<id>`, `slot-<id>`.
- **Performance:** DOM tokens moved with transforms. Sibling slides use FLIP. At most 80 tokens.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.10 `stepper`: Stepper

**Primitive · P0 · W0.** Steps through a process: Demonstrate screens, worked examples, algorithm traces, written methods and proofs. Each step is a keyframe of the host widget's state plus a caption, and may pause for a prediction.

- **Serves:** `written-method`, `function-machine`, `iteration-cobweb`, `geometry-board` dissections, `sum-visualiser`, `induction-chain`, `pascal-triangle` paths, `counting-slots` enumeration.
- **Uses:** the host's `setState({ animate: true })`.
- **Interactions.**
  - Pointer: previous, next, play and pause buttons; tap a dot to jump.
  - Keyboard: Left and Right step; Space plays and pauses; Home and End jump.
- **State:** `{ index, playing }`.
- **Answers:** none of its own. A step marked `predict` pauses playback and shows an input; the stepper continues only after that input's Check.
- **Config:**
```ts
interface StepperConfig {
  steps: { state: unknown; caption: string; predict?: { input: InputConfig; check: Check } }[];   // caption at most 20 words, may hold $...$
  autoplay?: boolean; msPerStep?: number;
}
```
- **Visual:** 8px dots under the canvas (current ink, done `--text-muted`). Previous and next are 44px secondary icon buttons. The caption uses the prose token below the canvas.
- **Motion:** keyframe transitions use the host's own animation, 480 to 800ms.
- **Reduced motion:** keyframes jump; captions cross-fade over 120ms; autoplay is off.
- **Accessibility:** the caption is in a polite live region. Dots are labelled "Step 3 of 7".
- **Tutor:**
  - Describe: "Step 3 of 7: 'Bring down the 4.'"
  - Targets: `step-next`, `step-<n>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** keyframes can come from algorithm functions, as in `written-method`.

### 3.11 `tex-terms`: Addressable maths

**Primitive · P0 · W0.** Typeset maths whose parts are addressable: each term, factor or operator has an id. Parts can be tapped, highlighted, coloured to match a diagram and annotated. Numbers can change during a drag without re-rendering KaTeX.

- **Serves:** every composite with a live equation; `equation-workbench`; `derivation`; `algebra-tiles`; `unit-chain`; tutor highlighting of terms.
- **Uses:** KaTeX.
- **Interactions.**
  - Pointer: tap a selectable term. Hover (desktop) or tap (mobile) shows its annotation.
  - Keyboard: Tab through selectable terms; Space selects.
- **State:** `selected: string[]`.
- **Answers:** `set` and `choice` ("tap the term that is the gradient").
- **Config:**
```ts
interface TexTermsConfig {
  tex: string;                         // terms wrapped as \htmlId{t1}{...}
  slots?: Record<string, { value: number; format: 'number' | 'fraction' | 'signed'; width: number }>;   // width in ch, stops reflow
  selectable?: string[];
  tint?: Record<string, 1 | 2 | 3 | 4 | 5 | 6 | 'manip'>;   // match diagram colours
  notes?: Record<string, string>;
}
```
- **Implementation:**
  - KaTeX runs with `trust` limited to `\htmlId` and `\htmlClass`, and `output: 'htmlAndMathml'`. Supporting `\htmlId` under this trust policy is [unverified] and gets a build-time test.
  - Slots render as placeholders whose text is replaced each frame, with tabular figures and a U+2212 minus sign.
- **Visual:**
  - Inherits `currentColor`.
  - Tinted terms use their slot colour (an x-term matching the x-tile, for example).
  - Selected terms get a `--manip` underline and wash.
  - Tutor highlights use the standard pear wash and ink ring.
- **Motion:** slot text updates instantly. Rearrangement, as in the workbench, uses FLIP on term boxes over 300ms.
- **Reduced motion:** rearrangements cross-fade.
- **Accessibility:** MathML output for screen readers. Slot changes reach the live region through the host, never per frame.
- **Tutor:**
  - Describe: "2x + 3 = 11 [t1: 2x] [t2: 3] [t3: 11]".
  - Targets: term ids.
- **Performance:** KaTeX renders on structure change only, at about 5ms for a typical expression. A per-frame slot write costs under 0.1ms.
- **Artifact / web:** KaTeX from jsdelivr in the Artifact, vendored on the web.
- **Generator:** no.

### 3.12 `data-table`: Data table

**Primitive · P0 · W0.** Tables in three uses:

- read-only data;
- learner-filled cells (function tables, frequency tables, difference tables, patterns);
- the accessible table view of every chart.

- **Serves:** everywhere.
- **Uses:** `num-parse`, `keypad`.
- **Interactions.**
  - Pointer: tap a cell to edit it; tap a header to sort, when sorting is on.
  - Keyboard: the grid pattern. Arrows move; Enter edits and commits; Escape cancels; Tab goes to the next editable cell.
- **State:** `{ cells: Record<string, string>, sort?: { col, dir } }`.
- **Answers:** `state` (each cell checked as a numeric or expression answer), `ordering` (after a sort).
- **Config:**
```ts
interface DataTableConfig {
  columns: { id: string; header: string; type: 'number' | 'text' | 'expression'; editable?: boolean; format?: string }[];
  rows: Record<string, unknown>[];
  editableCells?: [number, string][];
  sortable?: boolean;
  linkedLayer?: string;            // keeps rows in sync with a plot layer
  maxRows?: number;
}
```
- **Visual:**
  - A container with `--r-md` corners and 1px `--line` row dividers.
  - Headers in the caption token at weight 600 in `--text-2`.
  - Tabular figures throughout. Editable cells use the `field` style; the active cell has a `--manip` border.
- **Motion:** sorting reorders rows with a 200ms FLIP.
- **Reduced motion:** instant.
- **Accessibility:** a real `<table>` with scoped headers. Editable tables use `role="grid"`, with inputs labelled by their row and column headers.
- **Tutor:**
  - Describe: compact CSV, at most 20 rows; longer tables are summarised.
  - Targets: `cell-<row>-<col>`, `col-<id>`.
- **Performance:** DOM, at most 200 rows. Virtualisation is a P1 need for 1.1 data frames.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.13 `keypad`: On-screen keypad

**Primitive · P0 · W0.** Numeric and simple-expression entry on touch devices, and the speed-drill pad. Layouts:

- `digits`;
- `fraction` (adds "/" and a space for mixed numbers);
- `sci` (adds a "×10ⁿ" key);
- `money` (adds "£");
- `speed` (digits, minus and delete only, with large keys).

- **Serves:** `numeric-entry`, `speed-drill`, `strategy-trainer`, `data-table`, exams.
- **Uses:** none.
- **Interactions.**
  - Pointer: keys fire on `pointerdown`, not `click`, because speed drills measure latency.
  - Keyboard: physical keys map straight through. The keypad hides once a physical keyboard is used (the first `keydown`), as in the prototype exam.
- **State:** none. It writes to its target input.
- **Answers:** none.
- **Config:** `{ layout: 'digits' | 'fraction' | 'sci' | 'money' | 'speed'; target: string; haptics?: boolean }`.
- **Visual:** keys at least 56 × 48 px with `--r-sm` corners, a secondary face, a `--lip-neutral` lip and h2-size labels, in a 3 × 4 grid.
- **Motion:** the 80ms press sink.
- **Reduced motion:** unchanged; press is feedback.
- **Accessibility:** named buttons ("minus", "decimal point", "delete"). The target input keeps focus, with `inputmode="none"` on touch so the OS keyboard stays away.
- **Tutor:** none.
- **Performance:** press to value in under 1ms, with no layout reads.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.14 `speed-timer`: Speed timer

**Primitive · P0 · W0.** An honest countdown or elapsed timer for drills and exams.

- **Serves:** `speed-drill`, `strategy-trainer`, `typing-trainer`, exams.
- **Uses:** none.
- **Interactions:** none; it is a display.
- **State:** `{ startedAt, durationMs, interrupted: boolean }`.
- **Answers:** none.
- **Config:** `{ mode: 'countdown' | 'elapsed'; durationMs?: number; warnAtMs?: number[]; display: 'ring' | 'text' | 'bar'; onHide: 'void' | 'continue' }`.
- **Hidden tab** [our choice]: a timed drill whose tab is hidden ends as "interrupted, not scored" (`onHide: 'void'`). Exams continue counting (`'continue'`).
- **Visual:** tabular figures; a thin ring or bar in the interview track accent (`--speed`). In the last 10 seconds the text turns `--amber-text`, without flashing.
- **Motion:** linear progress, allowed for timed tasks (design research section 4.2).
- **Reduced motion:** the bar steps once per second.
- **Accessibility:** `role="timer"`, not live. Announcements at the start, at 30 seconds and at 10 seconds.
- **Tutor:** none.
- **Performance:** uses `performance.now()`, runs `requestAnimationFrame` only while visible, and does not drift.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.15 `view-3d`: 3D view

**Primitive · P0 · W3.** Simple 3D scenes that rotate by dragging: solids, 3D vectors and planes, with surfaces at P1.

- **Serves:** GCSE solids, plans and elevations, 3D Pythagoras; `vector-plane` 3D mode; 1.4 planes and 3D vectors; P1 surfaces $z = f(x, y)$ for 1.3.
- **Uses:** `geo-layer` styles.
- **Interactions.**
  - Pointer: drag to orbit (yaw and pitch, pitch clamped to ±85°); optional pinch zoom; tap to select a vertex, edge or face.
  - Keyboard: arrows rotate 15°; + and − zoom; R resets; Tab cycles selectable elements.
  - View buttons: front, side, plan, isometric.
- **State:** `{ camera: { yaw, pitch, zoom }, selected: string[] }`.
- **Answers:** `set`.
- **Config:**
```ts
interface View3DConfig {
  objects: ({ id: string; type: 'polyhedron'; vertices: [number, number, number][]; faces: number[][] }
          | { id: string; type: 'segment' | 'arrow'; a: [number, number, number]; b: [number, number, number] }
          | { id: string; type: 'plane'; normal: [number, number, number]; d: number }
          | { id: string; type: 'surface'; expr: string; domain: [[number, number], [number, number]]; mesh: number })[];   // surface: P1
  projection: 'orthographic' | 'perspective';
  camera?: { yaw: number; pitch: number; zoom: number };
  axes?: boolean; views?: boolean; selectable?: string[];
}
```
- **Rendering:** projection plus a painter's sort into SVG polygons, up to 200 faces; Canvas 2D for meshes up to 2,500 quads (P1). No WebGL, which avoids a second rendering model.
- **Visual:**
  - Faces use three neutral value steps, lit from the upper left, with 1.5px ink edges.
  - Hidden edges are 1px dashed `--text-muted`, the school convention.
  - The selection is `--manip`.
- **Motion:** rotation is direct, with no inertia, so views stay precise.
- **Reduced motion:** view buttons snap instantly.
- **Accessibility:** view buttons give a full path for anyone who cannot drag. Selectable elements are also listed as buttons ("edge AB, 5 cm").
- **Tutor:**
  - Describe: "Cuboid 3 × 4 × 12, viewed from front right; selected: AG."
  - Targets: `vertex-<id>`, `edge-<id>`, `face-<id>`, `view-front`.
- **Performance:** projection and sort under 2ms for 200 faces.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.16 `code-surface`: Code surface

**Primitive · P0 · W2.** The editing surface: a textarea over a synchronised highlighted `<pre>`, as in the prototype drill. It has:

- line numbers and Python highlighting;
- indentation help: Tab inserts four spaces, Shift + Tab dedents, and Enter keeps the indent and adds one after a colon;
- locked read-only line ranges and error-line marks;
- a symbol bar on mobile.

- **Serves:** `code-editor`, `workspace-sim`, `setup-checklist` (pasted scripts), and every code drill from 1.1 on.
- **Uses:** none.
- **Interactions.**
  - Typing. The mobile symbol bar holds Tab, `:`, `(`, `)`, `[`, `]`, `"`, `=`, `#` and `_`, which phone keyboards hide.
  - Keyboard: Tab and Shift + Tab indent. Ctrl or Cmd + Enter runs. Escape then Tab leaves the editor, so focus is never trapped (WCAG 2.1.2).
- **State:** `{ text, selection: [number, number] }`.
- **Answers:** `code`.
- **Config:** `{ language: 'python' | 'text' | 'shell'; initial: string; locked?: [number, number][]; maxLines?: number; symbolBar?: boolean | 'auto' }`.
- **Visual:**
  - Source Code Pro in the code token, on `--bg-sunken` with `--r-md` corners; line numbers in `--text-muted`.
  - Token colours as in the prototype: keywords `--code-keyword`, built-ins `--code-deep`, strings `--fin-deep`, numbers `--prob-deep`, comments `--text-muted`.
- **Motion:** none.
- **Reduced motion:** n/a.
- **Accessibility:** a real textarea with a label and a line count. Error lines are announced with their messages.
- **Tutor:**
  - Describe: numbered code (truncated past 2 KB) and the last run's result.
  - Targets: `line-<n>`.
- **Performance:** re-highlighting is debounced to animation frames; at most 300 lines.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.17 `text-terminal`: Text terminal

**Primitive · P0 · W2.** A terminal-like surface: a prompt, an input line, scrollback, history and a completion hook. The host supplies the interpreter (`shell-sim`, or a Python REPL from 1.1).

- **Serves:** `shell-sim`, `code-editor` (console and stdin), `workspace-sim`; 1.1 REPL; 1.2 Git and the Linux command line.
- **Uses:** none.
- **Interactions.**
  - Pointer: tap anywhere to focus the input.
  - Mobile symbol bar: `/`, `~`, `.`, `-`, `|`, Tab, ↑ and ↓.
  - Keyboard: Enter runs; Up and Down walk history; Tab completes; Ctrl + C cancels the line.
- **State:** `{ scrollback: string[] (capped at 500), history: string[], input: string }`.
- **Answers:** through the host: `state`, or `text` for typed commands.
- **Config:** `{ prompt: string; interpreter: string; banner?: string; completion?: boolean }`, where `interpreter` names a host-registered interpreter.
- **Visual:**
  - `--bg-sunken` in light mode. A black terminal would break the quiet workbench; dark mode is dark anyway.
  - Code token type; prompt in `--code-keyword`.
  - Errors in `--fail-cross`, always prefixed with "error:" in text.
  - A block cursor that blinks, except under reduced motion.
- **Motion:** none, apart from the cursor.
- **Reduced motion:** the cursor does not blink.
- **Accessibility:** output in `role="log"` with polite announcements; a labelled input; navigable scrollback.
- **Tutor:**
  - Describe: the current folder and the last 20 lines.
  - Targets: `input`, `line-<n>`.
- **Performance:** DOM appends with capped scrollback.
- **Artifact / web:** identical.
- **Generator:** no.

---

## 4. Answer inputs

These are the general answer widgets from design research section 5.3. Stage 0 cannot ship without them. If the engine catalogue specifies them too, its spec wins, and this section is the Stage 0 requirement list. All six are P0.

### 4.1 `choice-cards`: Choice cards

**Input · P0 · W0.** Single and multiple choice on flat cards. Each option can be text, KaTeX, an image or a miniature static canvas. Every distractor carries a misconception id, a feedback line and a show-why key for the screen's canvas.

- **Serves:** everything.
- **Uses:** `tex-terms` for maths options.
- **Interactions.**
  - Pointer: tap selects. In multi mode, taps toggle.
  - Keyboard: keys 1 to 9 select on the web; Tab and arrows move; Space toggles.
- **State:** `{ selected: string[] }`.
- **Answers:** `choice`.
- **Config:**
```ts
interface ChoiceCardsConfig {
  options: { id: string; text?: string; tex?: string; image?: string; mini?: { widget: string; config: unknown } }[];
  multi?: boolean;                  // the question line then says "Select all that apply" and hides the count
  columns?: 1 | 2 | 'auto';        // 'auto': 2 columns when there are 4 or fewer short options
  shuffle?: boolean;                // seeded
}
```
- **Visual:** as design research section 5.3, item 1. Cards with a 2px `--line` border, `--r-sm` corners, at least 60px tall, with 8px gaps. The selected card has a 2px `--manip` border and `--manip-wash`. Graded states follow section 4.5 of the design research.
- **Motion:** the check badge pops on `spring-bounce`; unchosen cards fade to dim.
- **Reduced motion:** no pop.
- **Accessibility:** single choice is a `radiogroup`; multi is a group of checkboxes. The verdict reaches the live region.
- **Tutor:**
  - Describe: "Options: A 5/36, B 1/36, C 1/6, D 5/6. Selected: B."
  - Targets: `option-<id>`.
- **Performance:** trivial; KaTeX renders once.
- **Artifact / web:** identical.
- **Generator:** consumes the options generators produce. The shuffle is seeded.

### 4.2 `numeric-entry`: Numeric entry

**Input · P0 · W0.** One or more number fields. It accepts:

- integers, decimals and fractions (`a/b`);
- mixed numbers (`2 1/3`), percentages and standard form;
- money, with an optional unit suffix.

Multi-field layouts cover coordinates $(x, y)$, ratios $a : b$, and two-ended answers such as bounds.

- **Serves:** everything.
- **Uses:** `keypad`, `num-parse`.
- **Interactions.**
  - Typing, or the keypad on touch devices.
  - A parse preview under the field before Check ("Reads as $2\frac{1}{3}$"), so format slips never cost an attempt.
  - Keyboard: native fields, with Tab between parts.
- **State:** `{ raw: string[] }`.
- **Answers:** `numeric`, with an exact rational when the input was a fraction.
- **Config:**
```ts
interface NumericEntryConfig {
  fields: { id: string; label: string; unit?: string; prefix?: string }[];
  layout?: 'single' | 'pair' | 'ratio' | 'coordinates';
  keypad?: 'digits' | 'fraction' | 'sci' | 'money' | 'auto';
  autoAccept?: boolean;             // speed modes: correct input advances without Enter
}
```
- **Form policy** [our choice]:
  - In lessons, an equivalent form is accepted, with a note such as "Accepted. Simplest form is $\frac{3}{4}$."
  - Only screens whose subject is the form itself (`requireForm`) reject other forms, with a nudge such as "Give an exact fraction".
  - The tolerance rule appears after grading, for example "Accepted: 0.183 to 0.185".
- **Visual:** the `field` style, with the unit in `--text-muted` inside the field. The parse preview is in the caption token. Grading recolours the field border.
- **Motion:** none.
- **Reduced motion:** n/a.
- **Accessibility:** labelled inputs. The parse preview is linked with `aria-describedby`.
- **Tutor:**
  - Describe: "Field 'outcomes left': 12 (reads as 12)."
  - Targets: `field-<id>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** consumes generated values and tolerances.

### 4.3 `expression-entry`: Expression entry

**Input · P0 · W1.** Maths input through a MathLive math-field, graded by `cas`. Virtual keyboard layouts:

- algebra;
- powers and roots;
- trigonometry;
- logs;
- sets and inequalities;
- vectors;
- complex numbers.

- **Serves:** surds and index laws (0.1); all of 0.2 and 0.3; `derivation` predict mode; `equation-workbench` type mode.
- **Uses:** MathLive, `cas`.
- **Interactions.**
  - Typing with maths shortcuts (`/` makes a fraction, `^` a power, `sqrt` a root), or the virtual keyboard.
  - Keyboard: native MathLive keys, with arrows moving through the structure.
- **State:** `{ latex: string }`.
- **Answers:** `expression`, including equations, inequalities and solution sets.
- **Config:**
```ts
interface ExpressionEntryConfig {
  keyboard: ('algebra' | 'powers' | 'trig' | 'logs' | 'sets' | 'vectors' | 'complex')[];
  variables?: string[];
  placeholder?: string;
  prefix?: string;                  // e.g. 'y =' shown before the field
}
```
- **Near-miss diagnostics** (the checker, configured by the screen's misconceptions):
  - a sign error, found by testing the negation;
  - a missing factor, found by testing a constant ratio;
  - right value in the wrong form ("Equivalent, but not factorised");
  - a solution set missing one solution.
- **Fallback:** if MathLive fails to load (offline, or the CDN is blocked), a plain text field accepts ASCII maths (`(x+3)^2`, `sqrt(2)`) through `cas.parse`, with a live KaTeX preview.
- **Visual:** the field style, with the virtual keyboard docked at the bottom on touch devices.
- **Motion:** MathLive's own caret only.
- **Reduced motion:** n/a.
- **Accessibility:** MathLive speaks maths [sourced: MathLive documentation describes its spoken output, not re-checked here]. The ASCII fallback is always available as a toggle.
- **Tutor:**
  - Describe: "Entered: (x + 3)(x − 2)".
  - Targets: `field`.
- **Performance:** lazy load of MathLive and Compute Engine (sizes [unverified]). The first render is under 100ms after load. Equivalence checks take at most 20ms.
- **Artifact / web:** jsdelivr in the Artifact, vendored on the web.
- **Generator:** consumes generated targets.

### 4.4 `card-sort`: Card sort

**Input · P0 · W0.** Sort cards in one of three modes:

- `bins`: classify cards (rational or irrational; linear or not);
- `match`: pair one to one (graph to equation, chart to description);
- `sequence`: put generic steps in order (installation steps, an algorithm).

Proof lines use `derivation` instead.

- **Serves:** all topics.
- **Uses:** `token-tray`.
- **Interactions:** as `token-tray`.
- **State:** the `token-tray` state.
- **Answers:** `mapping`, `ordering`.
- **Config:** `{ mode: 'bins' | 'match' | 'sequence'; cards: {id, text?, tex?, mini?}[]; bins?: {id, label}[]; targets?: {id, text?, tex?, mini?}[] }`.
- **Marking:** per card. Correctly placed cards lock; wrong ones return to the tray on Try again, following design research section 5.4 on multi-part answers.
- **Visual:** cards are tokens. Bins are labelled zones. Match targets sit in a column with a slot beside each.
- **Motion:** as `token-tray`.
- **Reduced motion:** as `token-tray`.
- **Accessibility:** as `token-tray`.
- **Tutor:**
  - Describe: "Bin 'linear': y = 2x + 1, y = 3. Bin 'not linear': y = x². Unplaced: y = 1/x."
  - Targets: `card-<id>`, `bin-<id>`.
- **Performance:** at most 16 cards.
- **Artifact / web:** identical.
- **Generator:** consumes generated cards.

### 4.5 `derivation`: Derivation

**Input · P0 · W0.** Aligned lines of maths with a justification for each line, in five modes:

- `step`: reveal line by line;
- `predict`: the learner enters the next line, checked by equivalence with the target line;
- `fill`: one missing line, chosen or entered;
- `order`: shuffled proof lines, which may include distractor lines, put in order with a mark for each line;
- `justify`: match each line to its reason.

This is how "derive, don't state" from maths-teaching and the lesson-creator rule against "it can be shown" become screens.

- **Serves:** every derivation and proof in Stage 0, among them $\sqrt{2}$ irrational, recurring decimals, the quadratic formula, log laws, series sums, compound-angle formulae and algebraic proof; later 1.3 to 1.6 heavily.
- **Uses:** `tex-terms`, `choice-cards`, `expression-entry`, `card-sort`, `stepper`.
- **Interactions:** by mode.
  - In `predict`, if the learner's line is equivalent to the previous line but is not the target step, the verdict reads "True, but not the step we're after" and gives the hint.
  - Keyboard: as the child inputs.
- **State:** `{ mode, revealed: number, entries: Record<lineId, string>, order?: string[] }`.
- **Answers:** `expression` (per line), `ordering`, `mapping`, `choice`.
- **Config:**
```ts
interface DerivationConfig {
  mode: 'step' | 'predict' | 'fill' | 'order' | 'justify';
  lines: { id: string; tex: string; why: string; hidden?: boolean; input?: 'choice' | 'expression'; options?: string[]; distractor?: boolean }[];
  align?: 'equals' | 'left';
  numbers?: Record<string, string>;     // learner's own values substituted in a closing line, as in the prototype's sDerive
}
```
- **Visual:** KaTeX `aligned`. Justifications go in the right margin on desktop and under each line on mobile (design research section 9.4). The missing line is a dashed slot. Graded lines get the per-line mark.
- **Motion:** revealed lines fade in and rise 8px over 200ms.
- **Reduced motion:** lines appear.
- **Accessibility:** MathML for each line. Justifications are linked to their lines. Order mode uses the `token-tray` keyboard model.
- **Tutor:**
  - Describe: "Derivation, 4 lines, line 3 missing. Line 1: P(A|B) = |A∩B|/|B|. ..."
  - Targets: `line-<id>`, `why-<id>`.
- **Performance:** KaTeX once per line.
- **Artifact / web:** identical.
- **Generator:** yes, where templates exist: recurring-decimal derivations, the quadratic formula for given coefficients.

### 4.6 `free-response`: Free response

**Input · P0 · W0.** Long-form written answers ("explain", "show that", proofs in words), with inline maths using `$...$` and a maths keyboard button. After submission the learner sees the model answer and self-marks against a rubric of up to 10 points, as in the lesson-creator skill. Optional AI marking scores each rubric point with quotes from the answer and is shown as advisory beside the self-mark.

- **Serves:** at least one homework item per level (design research section 8.2); proofs in 0.1 to 0.3; explanation items.
- **Uses:** `expression-entry` (inline), the tutor transport for AI marking.
- **Interactions.** Typing and a Submit button. After submission, the rubric checklist (tick each point earned), then the model answer.
- **State:** `{ text, submitted, selfMarks: boolean[], aiMarks?: {point, earned, quote}[] }`.
- **Answers:** `text`.
- **Config:** `{ prompt: string; rubric: {point: string; marks: number}[]; model: string; minWords?: number; aiMarking?: boolean }`.
- **Visual:** a textarea in the prose token with a word count. The rubric is a list of checkboxes. The model answer uses `--bg-sunken` with `--r-md` corners. AI marks sit in the hint-indigo style beside each point and are labelled "AI suggestion".
- **Motion:** none.
- **Reduced motion:** n/a.
- **Accessibility:** a labelled textarea; the rubric as checkboxes.
- **Tutor:** the full text goes into the prompt for AI marking, at most 4 KB. Target: `answer`.
- **Performance:** trivial.
- **Artifact / web:** AI marking through `sample` in the Artifact and through the proxy on the web. If neither is available, self-marking alone works.
- **Generator:** no.

---

## 5. Composites: Number (0.1)

### 5.1 `place-value-chart`: Place-value chart

**Composite · P0 · W1.** Makes place value physical. Blocks or counters sit in columns:

- regrouping exchanges ten of one column for one of the next;
- multiplying or dividing by ten moves everything one column;
- decimals continue the pattern to the right;
- standard form counts the shifts;
- base mode does the same in base 2, 8 or 16.

- **Serves:** 0.1 place value, ordering, column methods (the meaning of exchange), multiplying and dividing by powers of ten, standard form, rounding (which column decides); binary for 0.4 and 1.1; 0.5 decomposition.
- **Uses:** `token-tray` (combine and split rules), `tex-terms` (readout), `stepper`.
- **Interactions.**
  - Pointer:
    - Drag blocks in from the supply.
    - When a column holds ten or more, drag them together, or tap "Regroup", to fuse them into one block of the next column.
    - Tap "Break" on a block to split it into ten of the next column.
    - The ×10 and ÷10 buttons shift everything.
  - Keyboard: Tab between columns. + and − add and remove a block. R regroups. Shift + Left and Shift + Right multiply and divide by the base.
- **State:** `{ base, counts: Record<number, number> }`. The key is the column power. A count may exceed base − 1 before regrouping.
- **Answers:** `numeric` (value shown), `state` (predicate `canonical`: every count below the base; predicate `equals(n)`).
- **Config:**
```ts
interface PlaceValueConfig {
  base?: 2 | 8 | 10 | 16;
  columns: { min: number; max: number };            // powers, e.g. -3 to 3
  initial?: Record<number, number>;
  supply?: boolean; allowShift?: boolean; allowRegroup?: boolean; allowBreak?: boolean;
  display: 'blocks' | 'counters' | 'digits';        // fades from concrete to symbolic across a ladder
  readout?: 'number' | 'expanded' | 'words' | 'none';
}
```
- **Display decision** [our choice]: whole-number columns may use Dienes blocks (cube, rod, flat). Any chart with decimal columns uses place-value counters: discs labelled 100, 10, 1, 0.1, 0.01. Scaled-down blocks for tenths confuse learners about what "one" is.
- **Visual:**
  - Columns are `--r-md` panels headed with the place name and the power ($10^2$).
  - The decimal point is an 8px ink dot on the column boundary.
  - An overfull column gets a dashed outline and a "Regroup" chip. That is a prompt, not a verdict.
- **Motion:**
  - Fuse: ten tokens converge into one over 400ms.
  - Shift: every token slides one column over 480ms, a consequence of the learner pressing ×10.
  - Drags are direct.
- **Reduced motion:** fuse cross-fades; shift jumps with a 120ms fade.
- **Accessibility:** each column is a list ("Tens: 4 counters"). The readout is live ("3,405.2"). The keyboard path is as above.
- **Tutor:**
  - Describe: "Base 10. Hundreds 3, Tens 12 (overfull), Ones 4. Value 424."
  - Targets: `col-<power>`, `regroup-<power>`, `shift-left`.
- **Performance:** at most 80 DOM tokens, moved with FLIP.
- **Artifact / web:** identical.
- **Generator:** yes. Numbers with zeros in middle columns; the $0.5$ against $0.45$ traps; conversions between bases.

### 5.2 `bar-model`: Bar model

**Composite · P0 · W1.** Fraction bars and tape diagrams in one widget:

- parts of a whole;
- equivalent fractions by refining a partition;
- comparing, adding and subtracting fractions over a common refinement;
- dividing by a fraction as fitting pieces into a length;
- a fraction of an amount;
- sharing in a ratio;
- percentages and reverse percentages;
- before-and-after word problems turned into equations.

- **Serves:** 0.1 fractions, ratio, percentages, proportion; 0.2 forming equations from words; 0.5 fractions of amounts.
- **Uses:** `region-selector` (bar parts), `slider` (part count), `draggable-point` (dividers and bar ends), `tex-terms` (brace labels), `number-line` (optional scale).
- **Interactions.**
  - Pointer:
    - Set the part count with a slider, or tap "Split each part into k".
    - Tap parts to shade them.
    - In tape mode, drag dividers and drag a bar's end to set its length.
    - Add a brace: tap two dividers, then type a label.
  - Keyboard: Tab to a bar. + and − change the part count; arrows walk the parts; Space shades. Divider handles are sliders.
- **State:** `{ bars: { id, length, parts: number[], shaded: number[], braces: {from, to, label}[] }[] }`, where `parts` holds the part sizes.
- **Answers:** `set` (shaded parts), `numeric` (fraction or amount), `state` (predicates `equalParts`, `sameShadedLength(a, b)`, `partsEqual(n)`), `expression` (the label of an unknown).
- **Config:**
```ts
interface BarModelConfig {
  mode: 'fraction' | 'tape';
  bars: { id: string; length: number; parts: number | number[]; shaded?: number[]; label?: string;
          movableDividers?: boolean; resizable?: boolean; unknown?: boolean }[];
  whole?: { value?: number; unit?: string };      // e.g. £60
  maxParts?: number; allowRefine?: boolean;
  scale?: 'none' | 'number-line';
  layout?: 'stacked' | 'wall';                     // 'wall' aligns bars as a fraction wall
}
```
- **Visual:**
  - Bars are 40px tall with `--r-xs` corners, a 2px ink outline and 1.5px ink dividers.
  - Learner shading: `--manip-wash` with a `--manip` border. Given shading: slot 1 at 35%.
  - Braces carry KaTeX labels. Unknown parts show "?".
- **Motion:**
  - Refining: new dividers grow from the bar's top edge over 300ms.
  - Show-why keys: `compare` overlays two bars to align their shaded lengths (480ms); `refine` splits every part to the common denominator; `fit` lays copies of a piece along a length.
- **Reduced motion:** the end states, with Play.
- **Accessibility:** each bar is a group ("Bar A, 8 equal parts, 3 shaded"). Parts are toggle buttons ("part 3 of 8, shaded"). There is a table view of the bars.
- **Tutor:**
  - Describe: "Bar A: 4 parts, shaded 1 to 3 (3/4). Bar B: 8 parts, shaded 1 to 5 (5/8)."
  - Targets: `bar-<id>`, `bar-<id>-part-<k>`, `brace-<k>`.
- **Performance:** SVG; at most 5 bars of 24 parts.
- **Artifact / web:** identical.
- **Generator:** yes. Comparisons between fractions; ratio shares with whole-number unit values; percentage and reverse-percentage problems with tidy multipliers.

### 5.3 `area-model`: Area model

**Composite · P0 · W1.** Multiplication as area. Modes:

- `grid-method`: $23 \times 47 = (20 + 3)(40 + 7)$;
- `fraction`: fraction and decimal products as overlapping shading;
- `array`: find all rectangles with area $n$, so primes and factors show themselves;
- `square`: side against area, so $\sqrt{30}$ lies between 5 and 6;
- `symbolic`: sides such as $x + 3$, the bridge to `algebra-tiles`.

Later uses: independence as area (1.5) and the $(a + b)^2$ proof.

- **Serves:** 0.1 multiplication, fractions, decimals, factors and primes, roots and surds, percentages of percentages; 0.2 expansion; 0.5 strategies; 1.5 independence.
- **Uses:** `plot-axes` (unit grid), `draggable-point` (corner and split handles), `region-selector` (sub-rectangles), `tex-terms`.
- **Interactions.**
  - Pointer:
    - Drag the corner handle to set the dimensions; they snap to integers or to the configured denominators.
    - Drag split handles on the edges to decompose lengths.
    - Tap a sub-rectangle to enter its partial product in place.
    - In fraction mode, tap columns and rows to shade.
    - In array mode, invalid sizes show the leftover tiles.
  - Keyboard: width, height and splits are sliders. Sub-rectangles are focusable, and Enter opens their entry field.
- **State:** `{ width, height, xSplits: number[], ySplits: number[], entries: Record<string, string>, shadedCols: number[], shadedRows: number[] }`.
- **Answers:** `numeric` (the total, or a partial product), `state` (predicates `dimensions(a, b)`, `allPartialsCorrect`), `set` (the shaded overlap), `expression` (symbolic area).
- **Config:**
```ts
interface AreaModelConfig {
  mode: 'grid-method' | 'fraction' | 'array' | 'square' | 'symbolic';
  width: number | string; height: number | string;      // strings in symbolic mode, e.g. 'x+3'
  splits?: { x?: number[]; y?: number[]; movable?: boolean };
  unit?: { denomX: number; denomY: number };             // fraction mode
  resizable?: boolean; snap?: number;
  entry?: 'partials' | 'total' | 'none';
  n?: number;                                            // array mode target area
  max?: { w: number; h: number };
}
```
- **Visual:**
  - The rectangle has a 2px ink border; splits are 1.5px ink lines.
  - Partial-product regions are tinted by their row factor, slot 1 or slot 2 at 25%, which keeps within the three-series rule, and each region is labelled with its product.
  - Fraction overlap: column shading is slot 1 hatch at 25%, row shading is slot 2 at 25%, and the overlap reads as both together.
  - Edge labels are KaTeX outside the rectangle. Handles are `--manip`.
- **Motion:** direct, then snap. Show-why keys:
  - `distribute`: the rectangle parts along its splits by 12px and the partial products travel to a sum line (600ms);
  - `rearrange`: array tiles reflow into a new rectangle (600ms).
- **Reduced motion:** stepped.
- **Accessibility:** handles are sliders with spoken values. Each sub-rectangle is announced with its dimensions and product. There is a table view of the partial products.
- **Tutor:**
  - Describe: "Rectangle 23 by 47, split 20 + 3 by 40 + 7. Entered: 800, 140, 120, ? (bottom right)."
  - Targets: `region-r<i>-c<j>`, `handle-corner`, `split-x-<k>`, `split-y-<k>`.
- **Performance:** SVG; at most 144 tiles in array mode.
- **Artifact / web:** identical.
- **Generator:** yes. Two-digit products with chosen carries; fraction products; values of $n$ with many or few factors; non-square $n$ for root brackets.

### 5.4 `double-number-line`: Double number line

**Composite · P0 · W1.** Two aligned scales with a shared marker, for proportional reasoning:

- ratio tables as positions;
- unit rate at 1;
- percentage of an amount; reverse percentages (100% from 120%);
- best buy by comparing two rates;
- currency and unit conversion;
- capture-recapture.

- **Serves:** 0.1 ratio, proportion, percentages; GCSE capture-recapture; 0.2 direct proportion.
- **Uses:** `number-line` (two of them), `draggable-point` (the marker), `data-table` (optional ratio table).
- **Interactions.**
  - Pointer: drag the marker. Drop pins to record pairs. Type a value on either scale to move the marker there.
  - Keyboard: the marker is a slider on the top scale, and announces the bottom value too. P drops a pin.
- **State:** `{ marker: number, pins: {top, bottom}[] }`.
- **Answers:** `numeric` (the bottom value at a given top value), `point` (marker position), `state` (the pins satisfy the proportion).
- **Config:**
```ts
interface DoubleNumberLineConfig {
  top: { min: number; max: number; label: string; unit?: string; ticks: number };
  bottom: { min: number; max: number; label: string; unit?: string; ticks: number };
  ratio: number | null;                         // bottom per top; null while the learner must discover it
  given?: { top: number; bottom: number }[];
  marker?: { start: number; snap?: number };
  showUnitRate?: boolean;
}
```
- **Visual:**
  - Two 2px ink lines, 56px apart.
  - The marker is a vertical `--manip` line with a handle at its top.
  - Pins and given pairs are ink ticks joining both lines, with values on each.
- **Motion:** direct, then snap.
- **Reduced motion:** n/a.
- **Accessibility:** the marker's `aria-valuetext` reads "120 percent matches £54". The table view lists the pins.
- **Tutor:**
  - Describe: "Top: percent 0 to 150. Bottom: £0 to £90. Marker at 120% matching £54. Pins: 100% matching £45."
  - Targets: `marker`, `pin-<k>`, `tick-top-<v>`, `tick-bottom-<v>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Percentages and reverse percentages; unit conversions; best buys with tidy numbers.

### 5.5 `factor-tree`: Factor tree

**Composite · P0 · W1.** Prime factorisation by splitting, used for:

- seeing that different trees give the same leaves;
- index form;
- testing for squares and cubes (even exponents);
- simplifying surds ($\sqrt{72} = 6\sqrt{2}$);
- feeding prime factors to `venn-diagram` for HCF and LCM.

- **Serves:** 0.1 primes, HCF and LCM, roots and surds; 0.2 simplifying algebraic fractions.
- **Uses:** `token-tray` (factor chips), `geo-layer` (branches), `numeric-entry` (factor input), `stepper`.
- **Interactions.**
  - Pointer:
    - Tap a composite node and enter one factor; the cofactor is computed, and both grow as children. Early lessons offer suggested divisors.
    - Tap "prime" to circle a leaf; a wrong claim is flagged at Check.
    - Drag the leaves into an index-form product line.
  - Keyboard: the tree pattern (arrows). Enter splits, P marks prime.
- **State:** `{ tree: { value, children?: [Node, Node], prime?: boolean } }`.
- **Answers:** `state` (predicate `fullyFactorised`), `expression` (index form), `set` (multiset of leaves).
- **Config:** `{ n: number; second?: number; split: 'free' | 'suggested'; indexForm?: boolean; maxDepth?: number }`.
- **Visual:**
  - Nodes are pill chips in `lip-token` style. Declared primes get a 2px ink ring.
  - Branches are 1.5px ink. Leaves collect in a row at the bottom.
  - Index form uses `tex-terms`, with each prime tinted (at most three slots, otherwise labels only).
- **Motion:** children grow from their parent over 200ms. Show-why `uniqueness`: two different trees for the same number collapse their leaves into the same sorted row (600ms).
- **Reduced motion:** instant.
- **Accessibility:** `role="tree"` with tree items such as "36, split into 6 and 6".
- **Tutor:**
  - Describe: "Tree for 360: 360 → 36 × 10; 36 → 6 × 6 (unsplit); 10 → 2 × 5 (both marked prime)."
  - Targets: `node-<path>` (for example `node-0-1`), `index-form`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Numbers up to 1,000, for non-calculator work, with 3 to 6 prime factors and chosen exponents.

### 5.6 `venn-diagram`: Venn diagram

**Composite · P0 · W1.** Two or three sets. The learner:

- sorts elements into regions;
- shades set expressions ($A \cup B$, $A \cap B'$);
- writes counts in regions.

Uses: inclusion-exclusion; HCF and LCM from prime factors; GCSE probability from Venn diagrams; conditional probability (1.5).

- **Serves:** 0.1 HCF and LCM; GCSE sets and probability; 0.3 inclusion-exclusion; 1.5.
- **Uses:** `region-selector` (shapes), `token-tray` (elements), `numeric-entry` (counts).
- **Interactions.**
  - Pointer: drag elements into regions; tap regions to shade; tap a region to type its count.
  - Keyboard: regions are focusable in a fixed order; Space shades; Enter edits the count. Elements follow the `token-tray` keys.
- **State:** `{ placements, shaded: string[], counts: Record<string, string> }`.
- **Answers:** `mapping` (elements to regions), `set` (shaded regions), `numeric` (counts and probabilities), `state`.
- **Region ids:**
  - Two sets: `a-only`, `b-only`, `ab`, `outside`.
  - Three sets: `a-only`, `b-only`, `c-only`, `ab-only`, `ac-only`, `bc-only`, `abc`, `outside`.
- **Config:**
```ts
interface VennConfig {
  sets: { id: string; label: string }[];          // 2 or 3
  universe?: { label: string };
  elements?: { id: string; label: string; tex?: string }[];
  given?: { region: string; count?: number; elements?: string[] }[];
  task: 'sort' | 'shade' | 'count' | 'probability';
  regionNames?: 'words' | 'notation';            // "A only" or A ∩ B′
}
```
- **Visual:**
  - Circles are 2px ink outlines with ink labels; colour stays free for shading.
  - Shaded regions use `--manip-wash`. Counts are centred KaTeX.
  - The universe is a 2px `--line` rectangle with `--r-md` corners.
- **Motion:** show-why keys:
  - `double-count`: the intersection flashes twice;
  - `complement`: the shading sweeps outward.
- **Reduced motion:** a static highlight.
- **Accessibility:** each region is a button ("In A and B, not C: 4 items"). The table view lists each region with its elements or count.
- **Tutor:**
  - Describe: "A (multiples of 2), B (multiples of 3). A only: 2, 4, 8. AB: 6. B only: 3, 9. Outside: 1, 5, 7. Shaded: none."
  - Targets: the region ids, plus `element-<id>`.
- **Performance:** region paths are computed once from the circle intersections.
- **Artifact / web:** identical.
- **Generator:** yes. Number-property sets; survey problems with consistent totals.

### 5.7 `expression-tree`: Expression tree

**Composite · P0 · W1.** The structure of an expression as a tree. The learner:

- evaluates from the leaves up;
- substitutes values for variables;
- expands powers into products and merges them (index laws);
- rewrites a tree into an equivalent one;
- solves by undoing operations from the root, for rearranging formulae.

It shows why $-3^2 \ne (-3)^2$, and bridges to Python's evaluation order (0.4, 1.1).

- **Serves:** 0.1 order of operations and index laws; 0.2 substitution and rearranging; 0.4 Python expressions; 1.1.
- **Uses:** `geo-layer` (edges), `token-tray` (value chips, palette), `tex-terms` (the linked expression), `stepper`.
- **Interactions.**
  - Pointer:
    - Tap an operator whose children are values to evaluate it; the node collapses into its value.
    - Drag a value chip onto a variable leaf to substitute.
    - In build mode, drag operators and operands into an empty tree.
    - In solve mode, tap the root's outer operation to apply its inverse to both sides.
    - Tapping a node highlights the matching part of the linked expression.
  - Keyboard: the tree pattern. Enter evaluates, digits type a value, and I applies the inverse.
- **State:** `{ tree: Node, evaluated: string[], substitutions: Record<string, number>, sides?: [Node, Node] }`.
- **Answers:** `numeric` (final value), `ordering` (the order of evaluation, as in "what does Python do first"), `state` (predicate `matches(expr)`), `expression`.
- **Config:**
```ts
interface ExpressionTreeConfig {
  expression: string;                    // or an equation in solve mode
  mode: 'evaluate' | 'build' | 'substitute' | 'expand-powers' | 'solve';
  values?: Record<string, number>;
  palette?: string[];
  conventions: 'maths' | 'python';       // python adds **, //, % and their precedence (** is right-associative)
  linkedTex?: boolean;
}
```
- **Visual:**
  - Operator nodes are 36px circles with the operator glyph.
  - Leaves are `lip-token` chips. Variable leaves waiting for a value have a `--manip` outline.
  - Edges are 1.5px ink. Evaluated nodes become ink value chips; evaluation is not grading.
- **Motion:** on evaluation, children slide into the parent and merge (300ms). Show-why `wrong-order` evaluates a ghost copy in the learner's order and sets the two results side by side.
- **Reduced motion:** instant collapse; the show-why is a before-and-after.
- **Accessibility:** `role="tree"`; nodes read as "multiply: 3 and (4 + 5)"; the linked expression is highlighted together with the node.
- **Tutor:**
  - Describe: "Tree of 3 + 4 × 2: root + with children 3 and ×(4, 2). Evaluated: none."
  - Targets: `node-root`, `node-<path>`.
- **Performance:** at most 30 nodes, laid out with a tidy-tree algorithm in O(n).
- **Artifact / web:** identical.
- **Generator:** yes. Bounded-depth expressions with whole-number intermediate results; order-of-operations traps; formulae to rearrange.

### 5.8 `written-method`: Written method

**Composite · P0 · W1.** Animates and drills written algorithms with the reasoning visible:

- column addition with carrying and column subtraction with exchange;
- long multiplication;
- short and long division, including decimal places;
- recurring decimals, detected by a repeated remainder (the cycle);
- polynomial long division and synthetic division (0.2, 0.3).

- **Serves:** 0.1 written methods and recurring decimals; 0.2 the factor and remainder theorems; 0.3 rational functions.
- **Uses:** `stepper`, `tex-terms`, `numeric-entry` (digit cells), `data-table` (grid layout).
- **Interactions.**
  - Watch mode uses the stepper. In do mode, the learner types each digit into the highlighted cell.
  - The remainder tracker lists each remainder. When one repeats, the cycle is bracketed.
  - Keyboard: digits fill the active cell; arrows move.
- **State:** `{ algorithm, operands, cells: { r, c, value, entered? }[], step }`.
- **Answers:** `state` (all cells correct), `numeric` (the result; the cycle length), `expression` (quotient and remainder for polynomials).
- **Config:** `{ algorithm: 'column-add' | 'column-sub' | 'long-mul' | 'short-div' | 'long-div' | 'poly-div' | 'synthetic-div'; operands: (number | string)[]; dp?: number; mode: 'watch' | 'do' | 'mixed'; checkPer: 'cell' | 'row' | 'end'; remainders?: boolean }`.
- **Visual:**
  - A digit grid in Archivo tabular figures with 1px `--line` guide cells.
  - Carries are small digits above, in slot 2.
  - Bring-down arrows are 1.5px ink. The active cell has a `--manip` border.
  - The repeated remainder is ringed.
- **Motion:** each step fades its digit in and draws its arrow, over 300ms.
- **Reduced motion:** digits appear.
- **Accessibility:** the grid is a table with row labels ("partial product 2"). Each step's caption reaches the live region: "7 into 30 goes 4, remainder 2".
- **Tutor:**
  - Describe: "Long division 1 ÷ 7 to 6 dp: quotient so far 0.142; remainders 1, 3, 2, 6; next digit pending."
  - Targets: `cell-<r>-<c>`, `remainder-<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Additions with chosen carries; divisions with chosen cycle lengths (denominators 3, 7, 11, 13 and others); polynomial divisions with whole-number coefficients and a given remainder.

### 5.9 `multiplier-chain`: Multiplier chain

**Composite · P0 · W1.** Percentages as multipliers:

- a change of $p\%$ is a multiplication by $1 \pm \frac{p}{100}$, and successive changes multiply;
- a reverse percentage divides by the multiplier;
- compound interest and depreciation; compounding $n$ times a year tends to $e^{r}$ (0.3).

The log panel makes steps additive, which shows why log returns add while simple returns do not. It also shows why +50% then −50% leaves 75%: volatility drag, the gap between the arithmetic and geometric mean.

- **Serves:** 0.1 percentage change, compound interest, reverse percentages; 0.2 exponential growth; 0.3 $e$, modelling, annuities; 1.7 returns.
- **Uses:** `bar-layer`, `curve-layer`, `token-tray` (multiplier chips), `slider` (rate, $n$, years), `tex-terms`, `plot-axes`.
- **Interactions.**
  - Pointer:
    - Drag multiplier chips into the chain, and edit a chip's value.
    - Drag the start bar to change the starting amount.
    - Sliders set the rate, the periods and the years.
    - In reverse mode, the end is given; build the reverse chain with ÷ chips.
  - Keyboard: the `token-tray` keys for chips; sliders.
- **State:** `{ start, steps: { value, as: 'percent' | 'multiplier' }[], n?, years?, reverse?: boolean }`.
- **Answers:** `numeric` (final amount, original amount, overall percentage change), `expression` (the single equivalent multiplier), `state`.
- **Config:**
```ts
interface MultiplierChainConfig {
  start: number | null; unit?: string;            // null in reverse problems
  steps: { value: number; as: 'percent' | 'multiplier'; editable?: boolean }[];
  palette?: number[];
  view: 'bars' | 'line' | 'both';
  compounding?: { rate: number; nMax: number; years: number };
  logPanel?: boolean;
}
```
- **Visual:**
  - One bar per step in slot 1, with "×1.10" labels between bars.
  - The start level is a 1.5px dashed ink reference line.
  - The log panel shows the same steps as equal increments.
  - In compounding mode, beyond 60 steps the bars give way to a line.
- **Motion:** after a chip drops, the next bar grows from the previous bar's height over 300ms, to show multiplication acting on the previous amount.
- **Reduced motion:** instant.
- **Accessibility:** a table view (step, multiplier, balance). The live region reads "After 3 steps: £1,331.00".
- **Tutor:**
  - Describe: "Start £1,000. Steps ×1.10, ×1.10, ×1.10. Final £1,331.00. Overall +33.1%."
  - Targets: `start`, `chip-<k>`, `bar-<k>`, `slider-rate`.
- **Performance:** trivial; up to 365 steps, drawn as a line.
- **Artifact / web:** identical.
- **Generator:** yes. Percentage-change, reverse-percentage and compound-interest items with tidy multipliers.

### 5.10 `unit-chain`: Unit chain

**Composite · P0 · W1.** Dimensional analysis: multiply by conversion fractions equal to 1 until the units cancel to the target. It covers:

- compound measures (speed, density, pressure);
- area and volume units, including the trap that $1\,\text{cm}^2 = 10^{-4}\,\text{m}^2$;
- currency and time.

Annualising rates starts here; scaling volatility with the square root of time follows in P1 (1.7).

- **Serves:** 0.1 rates and units; GCSE compound measures; 0.4 file sizes (bytes); 1.7.
- **Uses:** `token-tray` (factor cards that flip), `tex-terms` (units with strike-through), `numeric-entry`, the `unit-algebra` service.
- **Interactions.**
  - Pointer: drag factor cards into the chain. Tap a card to flip it (numerator and denominator swap). Units that appear top and bottom strike through. Type the final value.
  - Keyboard: the `token-tray` keys; F flips the focused card.
- **State:** `{ chain: { card: string; flipped: boolean; squared?: boolean }[] }`.
- **Answers:** `state` (predicate `reducesTo(unit)`), `numeric` (final value), `expression`.
- **Config:** `{ start: { value: number; unit: string }; target: { unit: string }; palette: { id: string; num: [number, string]; den: [number, string] }[]; allowPowers?: boolean }`.
- **Visual:**
  - Cards are fraction tiles in `lip-token` style, such as $\frac{1000\,\text{m}}{1\,\text{km}}$.
  - Cancelled units are struck through in `--text-muted`.
  - The remaining unit sits in a result box that turns to ink once it matches the target. Grading still happens only at Check.
- **Motion:** a card flips (rotateX) over 200ms; strike lines draw over 200ms. Both are consequences of a tap.
- **Reduced motion:** instant.
- **Accessibility:** the chain reads as speech: "72 kilometres per hour, times 1000 metres over 1 kilometre, times 1 hour over 3600 seconds; units left: metres per second".
- **Tutor:**
  - Describe: "Start 72 km/h. Chain: (1000 m / 1 km), (1 h / 3600 s). Units left: m/s."
  - Targets: `card-<k>`, `result`.
- **Performance:** trivial; exact rational arithmetic.
- **Artifact / web:** identical.
- **Generator:** yes. Conversions for speed, density, pressure and data sizes; area and volume traps.

### 5.11 `bounds-explorer`: Bounds explorer

**Composite · P0 · W1.** Error intervals and calculations with bounds:

- a value rounded to some accuracy lies in an interval;
- the upper bound of $a - b$ uses the largest $a$ and the smallest $b$;
- the upper bound of $\frac{a}{b}$ uses the largest $a$ and the smallest $b$.

This is worst-case error propagation, which leads into uncertainty in 1.6 and into "which input drives the output".

- **Serves:** 0.1 bounds (GCSE Higher); 1.6 preview.
- **Uses:** `number-line` (one per input, one for the output), `draggable-point`, `tex-terms`.
- **Interactions.**
  - Pointer:
    - First, predict the output's bounds in two fields.
    - Then drag each input within its interval. The output moves live, and the range it has reached so far shades in.
    - "Try the corners" steps through every combination of endpoints.
  - Keyboard: inputs are sliders; C runs the corners.
- **State:** `{ inputs: Record<string, number>, swept: [number, number], predicted?: [number, number] }`.
- **Answers:** `interval`, `numeric` (upper or lower bound), `choice` (which combination gives the maximum).
- **Config:** `{ inputs: { id: string; label: string; value: number; accuracy: { type: 'dp' | 'sf' | 'nearest'; amount: number } }[]; formula: string; ask: 'upper' | 'lower' | 'both' | 'interval' }`.
- **Visual:**
  - Each input line shows its error interval, closed at the bottom and open at the top.
  - Input points are `--manip`.
  - The output line shows the swept range in slot 1 at 25%, and the predicted range as a dashed ink outline.
- **Motion:** direct. Show-why `corners`: the points jump to each corner in turn, 400ms each, and the output marks where it lands.
- **Reduced motion:** a static table of the corner combinations, with marks on the output line.
- **Accessibility:** sliders, the announced output, and a corners table.
- **Tutor:**
  - Describe: "a = 12.3 (1 dp; [12.25, 12.35)). b = 4 (nearest whole; [3.5, 4.5)). a ÷ b now 3.29; reached [2.84, 3.51]."
  - Targets: `input-<id>`, `output`, `corners`.
- **Teaching note:** the stated upper bound, 12.35, is itself excluded from the interval. The widget shows the open circle and a caption explaining the convention, because this confuses learners.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. GCSE-style bounds items, including speed from rounded distance and time.

### 5.12 `modular-clock`: Modular clock

**Composite · P0 · W1.** Remainders and cycles:

- clock arithmetic and divisibility;
- last-digit cycles of powers ($3^n \bmod 10$ runs 3, 9, 7, 1);
- day-of-week problems;
- why decimals recur (remainders modulo the denominator);
- parity arguments.

Later uses: hashing (1.8) and modular exponentiation.

- **Serves:** 0.1 divisibility and remainders, recurring decimals; interview puzzles (3.3); 1.8.
- **Uses:** `geo-layer` (circle and positions), `draggable-point` (the hand, on the circle, restricted to the positions), `stepper`, `data-table`.
- **Interactions.**
  - Pointer:
    - Set the modulus with a slider (2 to 24) and drag the hand.
    - Tap operation chips (+k, ×k) to apply them one step at a time.
    - In orbit mode, repeated multiplication draws the orbit polygon.
  - Keyboard: the hand moves through the positions with arrows; Enter applies the operation.
- **State:** `{ n, position, history: number[], op? }`.
- **Answers:** `numeric` (remainder, cycle length), `set` (positions visited), `state`.
- **Config:** `{ n: number; start: number; ops?: { kind: 'add' | 'mul' | 'pow'; k: number }[]; mode: 'free' | 'orbit'; labels?: 'numbers' | 'days' | 'hours' }`.
- **Visual:**
  - A 2px ink circle with labelled ticks and a `--manip` hand.
  - The orbit's edges are slot 1 arrows; visited positions are filled in slot 1.
- **Motion:** after an operation, the hand travels round over 300ms. Dragging is direct.
- **Reduced motion:** the hand jumps; the orbit appears whole.
- **Accessibility:** positions form a listbox. A history table. Describe: "Orbit 3, 9, 7, 1, 3: cycle length 4".
- **Tutor:** targets `pos-<k>`, `hand`, `orbit`, `op-<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Last-digit, day-of-week and remainder items.

### 5.13 `fermi-estimator`: Fermi estimator

**Composite · P0 · W1.** Order-of-magnitude estimation:

- decompose an unknown quantity into factors you can estimate;
- give each factor a low-to-high range on a log scale;
- combine them; the result range is the product of the factor ranges;
- see which factor dominates the uncertainty;
- compare with a sourced reference value;
- track calibration over time (were your ranges right as often as you meant?).

Interview Fermi questions (3.3) start here.

- **Serves:** 0.1 estimation and standard form; 0.5; 3.3.
- **Uses:** `number-line` (log10 per factor), `draggable-point` (low and high handles), `token-tray` (factor cards), `tex-terms`, `data-table` (calibration history).
- **Interactions.**
  - Pointer:
    - Arrange factor cards to build the decomposition, each card multiplying or dividing.
    - Drag each factor's low and high handles.
    - The result scale shows the product range and the geometric midpoint.
    - Reveal shows the reference value with its source and year.
  - Keyboard: handles are sliders in tenths of a decade; the cards follow the `token-tray` keys.
- **State:** `{ factors: { card, lo, hi, op: 'mul' | 'div' }[], revealed: boolean }`.
- **Answers:** `interval` (the range must contain the reference), `numeric` with `tol.factor` (the point estimate within a set factor of the reference).
- **Config:** `{ question: string; reference: { value: number; unit: string; source: string; year: number }; cards: { id: string; label: string; unit?: string }[]; mode: 'guided' | 'free'; tolFactor: number }`.
- **Visual:**
  - One log scale per factor, labelled $10^k$ at the decades.
  - Each range is a `--manip-wash` bar between its handles.
  - The result range is slot 1. The reference appears as a dashed ink marker.
- **Motion:** the reference marker drops in on `spring-snap`.
- **Reduced motion:** it appears.
- **Accessibility:** handles read as "low 2 million, high 10 million". There is a table view.
- **Tutor:**
  - Describe: "London population [5m, 10m] × share with a piano [1%, 5%] × tunings per year [0.5, 2] ÷ tunings per tuner per year [500, 1,000]. Product [25, 1,000]."
  - Targets: `factor-<k>-lo`, `factor-<k>-hi`, `result`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** no. The item bank is authored, and every reference value carries its source and year. Seeds only shuffle the order.

---

## 6. Composites: Algebra and functions (0.2)

### 6.1 `balance-scale`: Balance scale

**Composite · P0 · W2.** An equation is a balance. Ideas it carries:

- **Same to both sides.** Solve by doing the same to both pans.
- **Unknowns.** Boxes of equal hidden weight.
- **Negatives.** Balloons pull upwards, so subtraction and negative terms stay physical.
- **Division.** Split both pans into equal groups.
- **Inequalities.** A tilted beam keeps its tilt under the same operations.

**Known limit** [our choice to teach openly]: the model breaks for negative and fractional solutions. A Trap screen meets that break, and the lesson then moves to `equation-workbench`.

- **Serves:** 0.2 linear equations (one-step and two-step, unknowns on both sides, brackets), first inequalities; 0.1 negatives.
- **Uses:** `token-tray` (weights, boxes, balloons), `geo-layer` (beam and pans), `tex-terms` (linked equation).
- **Interactions.**
  - Pointer: drag tokens on and off the pans; tap action chips that act on both sides ("−1 from both", "−x from both", "÷2"); tap a pan to circle equal groups.
  - Removing from one side only is allowed: the beam tips, and that tip is the show-why.
  - Keyboard: the `token-tray` keys; action chips are buttons.
- **State:** `{ left: Counts, right: Counts, history: Action[] }`, where Counts is `{ x, negX, unit, balloon }`.
- **Answers:** `state` (predicates `balanced`, `solved`: one box alone on one side with the balance kept), `numeric` (the value of $x$).
- **Config:**
```ts
interface BalanceConfig {
  equation: string;                 // linear, whole-number coefficients up to 12, e.g. '3x + 2 = x + 8'
  relation?: '=' | '<' | '>' | '<=' | '>=';
  allowBalloons?: boolean;
  actions?: ('add' | 'remove' | 'divide')[];
  revealX?: boolean;                // weigh one box at the end
  maxTokens?: number;               // 24
}
```
- **Visual:**
  - A 4px ink beam on a triangular fulcrum; shallow trays with `--r-md` corners.
  - Unit weights are small `--bg-sunken` squares with ink outlines.
  - $x$ boxes are larger squares labelled $x$, with a `--manip` border while draggable.
  - Balloons are circles on strings, labelled "−1".
  - The equation underneath is tinted to match the tokens.
  - Tilt angle: clamp($k \times$ (right − left), ±15°), as in design research section 5.3, item 12.
- **Motion:** the beam settles on `spring-physical` whenever the imbalance changes. Division circles the groups over 400ms.
- **Reduced motion:** the beam takes its new angle at once, without oscillating.
- **Accessibility:**
  - Describe: "Left: 3 boxes and 2 units. Right: 1 box and 8 units. Balanced."
  - Tilts reach the live region: "Tipped left: left is heavier by 2".
- **Tutor:** targets `pan-left`, `pan-right`, `token-<id>`, `action-<name>`.
- **Performance:** at most 24 tokens.
- **Artifact / web:** identical.
- **Generator:** yes. Linear equations and inequalities with positive whole-number solutions and bounded coefficients.

### 6.2 `algebra-tiles`: Algebra tiles

**Composite · P0 · W1 (counters preset), W2 (full).** An area model with symbolic tiles: $x^2$, $x$ and $1$, plus their negatives and, for two variables, $y$, $xy$ and $y^2$. It supports:

- zero pairs and collecting like terms;
- expanding $(x + a)(x + b)$ by filling a frame;
- factorising by arranging tiles into a rectangle;
- completing the square by literally completing it: the missing corner is the constant.

The `counters` preset (only $\pm 1$ tiles) teaches adding and subtracting negatives in 0.1.

- **Serves:** 0.1 negatives; 0.2 collecting, expanding, factorising, completing the square.
- **Uses:** `token-tray` (tiles, with cancel rules), `area-model` (frame), `tex-terms`.
- **Interactions.**
  - Pointer: drag tiles from the supply; tap to flip a tile's sign; rotate an $x$ tile with its rotate button. A positive and a negative tile dragged together vanish as a zero pair. In frame mode, tiles snap into the product frame, and the frame's edges come from the tiles along its top and left.
  - Keyboard: the `token-tray` keys; F flips, R rotates.
- **State:** `{ tiles: { id, kind: 'x2' | 'x' | '1' | 'y' | 'xy' | 'y2', sign: 1 | -1, at: string, rot: 0 | 90 }[], frame?: { top: string[]; left: string[]; inside: string[] } }`.
- **Answers:** `expression` (what the tiles represent), `state` (predicates `isRectangle`, `frameMatches(a, b)`, `completedSquare`), `set`.
- **Config:** `{ preset: 'counters' | 'linear' | 'quadratic' | 'two-variable'; initial?: string; frame?: { top?: string; left?: string }; task: 'add-negatives' | 'collect' | 'expand' | 'factorise' | 'complete-square' | 'free'; zeroPairs?: boolean }`.
- **Visual:**
  - Tile sizes: $x^2$ is $L \times L$, $x$ is $L \times 1$ and $1$ is $1 \times 1$, with $L = 2.6$ units, so an $x$ tile is never mistaken for a whole number of units.
  - Positive tiles: a light fill with an ink outline and a label.
  - Negative tiles: diagonal hatching and a "−" in the label, so colour never carries the sign alone.
  - Draggable tiles have a `--manip` outline.
- **Motion:** a zero pair slides together and fades over 300ms. When factorising succeeds, the edge labels slide in over 300ms. Show-why `complete-square` pulses the missing corner.
- **Reduced motion:** instant.
- **Accessibility:** tiles read as "positive x tile". Describe: "2 x-squared, 5 x, 6 units; frame empty".
- **Tutor:** targets `tile-<id>`, `frame-top`, `frame-left`, `corner`.
- **Performance:** at most 40 tiles.
- **Artifact / web:** identical.
- **Generator:** yes. Factorable quadratics with small integer roots; like-term collections; sums of signed counters.

### 6.3 `function-machine`: Function machine

**Composite · P0 · W2.** Functions as rules from input to output:

- chains of operations;
- composition as machines in series, where order matters;
- inverses by running backwards, undoing each step in reverse order ("socks then shoes");
- domains, where the machine rejects inputs such as a square root of a negative or division by zero;
- finding a hidden rule from input and output pairs.

It links to Python functions (`def f(x): return ...`) in 0.4.

- **Serves:** 0.2 substitution, one-step and two-step equations, functions, composite and inverse functions; 0.3 logs as inverses; 0.4 functions.
- **Uses:** `token-tray` (operation chips into slots), `data-table` (input and output log), `tex-terms` (the formula built from the chain), `stepper` (the trace).
- **Interactions.**
  - Pointer: drop or type an input. Watch it pass through each stage. Build a machine by dragging operation chips (+3, ×2, square, square root, reciprocal). Flip the reverse switch and fill in the inverse operations. In guess-rule mode, feed inputs to a hidden machine, then enter its rule.
  - Keyboard: the `token-tray` keys; Enter runs; R reverses.
- **State:** `{ ops: Op[], log: { in, out }[], reversed: boolean, inverseOps?: Op[] }`.
- **Answers:** `expression` (the rule), `numeric` (an output or input), `ordering` (the inverse operations), `state`.
- **Config:** `{ ops?: Op[]; hidden?: boolean; palette?: Op[]; task: 'evaluate' | 'build' | 'inverse' | 'guess-rule' | 'compose'; machines?: 1 | 2; domainRules?: boolean }`.
- **Visual:**
  - A horizontal pipeline of `--r-md` boxes with 2px ink borders, each labelled in KaTeX.
  - The value is a chip with a `--manip` outline when the learner placed it.
  - A hidden machine is one `--bg-sunken` box with a "?".
  - A rejected input shows a note with an icon ("Not allowed: square root of −4"). It is information, not a verdict.
- **Motion:** the value chip travels through the boxes, 300ms per box, and changes at each one. The learner starts this demonstration. In reverse, it travels right to left.
- **Reduced motion:** a row of intermediate values, with Play.
- **Accessibility:** a log table, with each stage announced. Describe: "Machine: ×2 then +3. In 5, out 13."
- **Tutor:** targets `op-<k>`, `input`, `output`, `log`, `reverse`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Two-step and three-step machines with whole-number outputs; inverse tasks; hidden linear and quadratic rules.

### 6.4 `equation-workbench`: Equation workbench

**Composite · P0 · W1 (surds, rationalising), W2 (full).** Symbolic manipulation in which the learner chooses every move and the engine carries it out exactly.

- **Moves:**
  - add, subtract, multiply or divide both sides;
  - expand, factorise, collect;
  - cross-multiply;
  - square both sides;
  - take logs or exponentials;
  - apply an identity.
- **Step log.** Each step is logged with its justification.
- **Risky moves** are allowed, and their consequences show on a solution-set strip:
  - dividing by an expression that can be zero loses a solution;
  - squaring both sides adds an extraneous one.

That is the maths-teaching rule "show why the direct approach fails" made physical.

- **Serves:**
  - 0.1: surds and rationalising.
  - 0.2: equations, rearranging, inequalities (the sign flip), algebraic fractions, quadratics.
  - 0.3: exponential and log equations, trigonometric identities.
  - Later: 1.3.
- **Uses:** `tex-terms` (selectable terms), `cas`, `number-line` or `curve-layer` (solution-set strip), `derivation` (step log), `expression-entry` (type mode), `keypad` (operation arguments).
- **Interactions.**
  - Pointer: tap a term or a side to open an operation menu ("Subtract 3 from both sides", "Divide both sides by 2"). Dragging a term across "=" is accepted as a gesture, but it is logged and animated as the both-sides operation it is: the folk rule "move it over and change the sign" is never taught. In type mode, enter the next line and it is checked for equivalence. Undo and redo.
  - Keyboard: Tab through terms. Enter opens the menu; number keys choose an operation; Ctrl or Cmd + Z undoes.
- **State:** `{ lines: { latex, json, op?: { name, arg }, note? }[], cursor: number, solutionSet: string }`.
- **Answers:** `expression` (final line), `state` (predicates `isolated(v)`, `solved`, `form(f)`, `stepsValid`, `noLostSolutions`).
- **Config:**
```ts
interface WorkbenchConfig {
  start: string;                    // an equation, inequality, expression or identity
  goal: { kind: 'solve' | 'make-subject' | 'simplify' | 'prove-identity' | 'expand' | 'factorise' | 'rationalise';
          variable?: string; target?: string };
  ops: ('add-both' | 'sub-both' | 'mul-both' | 'div-both' | 'expand' | 'factorise' | 'collect' | 'cross-multiply'
        | 'square-both' | 'sqrt-both' | 'log-both' | 'exp-both' | 'identity' | 'common-denominator' | 'rationalise')[];
  identities?: string[];            // e.g. ['sin^2+cos^2=1'] in 0.3
  entry: 'menu' | 'type' | 'both';
  domain?: string;                  // e.g. 'x > 0'
  strip?: 'number-line' | 'graph' | 'none';
  justify?: boolean;                // learner tags each step with a reason
}
```
- **Visual:**
  - Lines stack aligned on "=" or "⇔". The current line is display size; earlier lines are muted.
  - The selected term has a `--manip` underline and wash.
  - The operation menu is a popover of secondary chips.
  - The solution-set strip marks solutions under the work. A changed set is outlined in `--hint` with a label ("x = 0 lost here").
- **Motion:**
  - Terms move to their new places over 300ms using FLIP (design research section 5.3, item 11).
  - For a both-sides operation, "−3" appears under each side at once, then the sides simplify.
- **Reduced motion:** lines cross-fade.
- **Accessibility:** MathML for each line. Terms are buttons with spoken labels ("term: 3 x"). The menu uses `role="menu"`. History is a list.
- **Tutor:**
  - Describe: "Goal: solve for x. Line 1: 3x + 2 = 11. Line 2: 3x = 9 (subtracted 2 from both sides). Selected: 3x."
  - Targets: `line-<k>`, `term-<line>-<k>`, `op-menu`, `strip`.
- **Performance:** each `cas` operation takes at most 20ms. KaTeX renders once per step.
- **Artifact / web:** `cas` from jsdelivr in the Artifact, vendored on the web.
- **Generator:** yes. Equation templates (linear with brackets and fractions, quadratics, log and exponential); a bank of formulae to rearrange (for example $A = P(1 + r)^n$ for $r$); identities to prove.

### 6.5 `equation-stack`: Equation stack

**Composite · P0 · W2.** Systems of equations as stacked rows. The learner:

- scales rows, adds and subtracts rows, and substitutes;
- watches the linked graph, where every row operation leaves the intersection fixed while the lines pivot about it. That is the key idea: row operations preserve the solution;
- meets inconsistent systems (parallel lines) and dependent systems (the same line);
- works with three variables (Algebra 2) and solves linear-quadratic systems by substitution.

It bridges to matrices (0.3) and Gaussian elimination (1.4).

- **Serves:** 0.2 simultaneous equations; 0.3 matrices; 1.4 elimination.
- **Uses:** `tex-terms` (rows aligned in coefficient columns), `numeric-entry` (scale factors), `token-tray` (drag a row onto a row), `plot-axes` and `curve-layer`, `derivation` (log).
- **Interactions.**
  - Pointer: drag row A onto row B, then choose "B + A" or "B − A". Tap ×k on a row to scale it. Drop an "$x = \dots$" row onto another to substitute.
  - Keyboard: rows are focusable. S scales; A adds into a target chosen with the arrows; Enter applies.
- **State:** `{ rows: string[], history: { op, rows, k? }[], vars: string[] }`.
- **Answers:** `point` (the solution), `numeric` (each variable), `state` (predicates `eliminated(v)`, `triangular`, `solved`), `choice` (one, none or infinitely many solutions).
- **Config:** `{ system: string[]; vars: ('x' | 'y' | 'z')[]; ops: ('scale' | 'add' | 'subtract' | 'swap' | 'substitute')[]; graph?: boolean; exact?: boolean }`.
  - The graph is for two variables only. Planes for three variables are P0 in the 1.4 cluster, through `view-3d`.
- **Visual:**
  - Rows are aligned in columns ($x$, $y$, $z$, "=", constant), like an augmented matrix with variable headers.
  - Each row's line uses its slot (1 to 3), with a matching dot and label beside the row.
  - The intersection is an ink point. After an operation, the old line remains as a dashed ghost.
  - When the graph shows the solution, Check items require the algebra instead, or set `graph: false`.
- **Motion:** while a row is dragged, its ghost follows the pointer. Coefficients combine column by column over 300ms. The line pivots from old to new over 600ms about the fixed intersection, which is the built-in show-why.
- **Reduced motion:** lines jump; the pivot is a before-and-after.
- **Accessibility:** rows form a table; operations are buttons. Describe: "R1: 2x + 3y = 12. R2: x − y = 1. Operations: none."
- **Tutor:** targets `row-<k>`, `coef-<row>-<var>`, `line-<k>`, `intersection`. When the graph is hidden, describe never mentions the intersection.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Systems with whole-number solutions and coefficients up to 12; parallel and coincident cases; linear-quadratic pairs with rational intersections.

### 6.6 `graph-explorer`: Graph explorer

**Composite · P0 · W2.** The main function-graph widget. It combines:

- **Parameter sliders.**
- **Defining points:** two points make a line; roots and a vertex make a parabola.
- **Live equation:** shown in several linked forms, with each coefficient tappable.
- **Overlays:** slope triangle, intercepts, roots, vertex, axis of symmetry, tangent at a point, chord, trapezia, asymptotes, holes, horizontal-line test, reflection in $y = x$, parent-function ghost, domain handles, and limit approach arrows.
- **Optional:** log axes and a linked table.

It covers:

- coordinates; straight lines; real-life graphs;
- quadratics; cubic, reciprocal and exponential graphs; transformations;
- domain and range; inverse and composite functions; circles and tangents;
- gradients of curves; area under a graph;
- trigonometric, exponential and log graphs; rational functions; limits; modulus; parametric curves.

- **Serves:** 0.1 proportion; most of 0.2; most of 0.3; later 1.3 and beyond.
- **Uses:** `plot-axes`, `curve-layer`, `geo-layer`, `draggable-point`, `slider`, `tex-terms`, `data-table`.
- **Interactions.**
  - Pointer:
    - Drag defining points and sliders.
    - Tap a coefficient in the equation to focus its slider.
    - With `dragCurve`, grab the curve itself to translate it, which updates $h$ and $k$.
    - Drag the tangent point, the chord ends and the domain handles.
    - Toggle overlays from chips.
    - Trace along the curve.
  - Keyboard: every handle and slider follows its primitive's keys. T toggles the table view; O cycles overlay chips.
- **State:** `{ params: Record<string, number>, points: Record<string, [number, number]>, overlays: Record<string, boolean>, view, domain?: [number, number] }`.
- **Answers:** `point`, `curve` (from the parameters), `numeric` (gradient, intercept, root, a parameter, a value read off), `expression` (the equation), `state` (predicates `passesThrough(P)`, `parallelTo(id)`, `perpendicularTo(id)`, `paramsEqual`, `oneToOne`).
- **Config:**
```ts
interface GraphExplorerConfig {
  axes: PlotAxesConfig;
  family?: { form: 'line-mc' | 'line-points' | 'quad-standard' | 'quad-vertex' | 'quad-roots' | 'poly-roots' | 'exp' | 'log'
                 | 'trig' | 'reciprocal' | 'rational' | 'circle' | 'modulus' | 'piecewise' | 'parametric' | 'custom';
             expr?: string; params?: SliderConfig[] };
  defining?: { id: string; x: number; y: number; constraint?: DraggablePointConfig['constraint'] }[];
  curves?: (CurveSpec & { slot?: number | 'target' })[];        // given and target curves
  overlays?: {
    slopeTriangle?: boolean; intercepts?: boolean; roots?: boolean; vertex?: boolean; symmetryAxis?: boolean;
    tangentAt?: number | 'draggable'; chord?: [number, number] | 'draggable'; trapezia?: { a: number; b: number; n: number };
    asymptotes?: boolean; holes?: boolean; hlineTest?: boolean; reflectYX?: boolean; parentGhost?: string;
    domainHandles?: boolean; approach?: { a: number; table?: boolean };
  };
  forms?: ('standard' | 'vertex' | 'factorised' | 'mc' | 'point-gradient')[];
  table?: { xs: number[]; editable?: 'x' | 'y' | 'none' };
  dragCurve?: 'translate' | 'none';
}
```
- **Visual:**
  - The learner's curve is 2.5px `--manip`. Given curves use slots; targets are dashed ink.
  - Slope-triangle legs are 1.5px ink, labelled "rise" and "run" with their values.
  - Tangents are slot 2. Trapezia are slot 1 at 25%. Asymptotes are dashed `--text-muted`. The vertex is an ink point with a label.
  - The approach overlay draws two points sliding towards $a$ from either side, with a values table.
- **Motion:** everything follows input on every frame. Show-why keys:
  - `morph`: the learner's curve becomes the correct one, 600ms;
  - `transform`: the parent ghost slides and stretches onto the transformed curve;
  - `chord-to-tangent`: the chord's second point slides to the first.
- **Reduced motion:** stepped, with Play.
- **Accessibility:**
  - The equation is live and debounced: "y = 2x − 1".
  - Handles read as "A at (1, 1)".
  - Overlays are described in words: "gradient 2: rise 4 over run 2".
  - Table view.
- **Tutor:**
  - Describe: "Line through A(0, −1) and B(2, 3): y = 2x − 1. Slope triangle on: rise 4, run 2. Given point P(4, 6)."
  - Targets: `point-<id>`, `slider-<id>`, `term-<param>`, `overlay-<name>`, `curve-main`, `form-<name>`.
- **Performance:** at most 4 live curves and 8 handles. Each frame: about 1ms of resampling per curve, equation slots written through `tex-terms` (no KaTeX re-render), and O(1) overlays.
- **Artifact / web:** identical.
- **Generator:** yes. Lines through lattice points; quadratics with integer roots or vertex; transformation pairs; tangent and gradient items; rational functions with integer asymptotes.

### 6.7 `curve-sketch`: Curve sketch

**Composite · P0 · W2.** Sketch a curve from its key features, graded on the features, not on pixels:

- roots, with multiplicity: crossing or touching the axis;
- the y-intercept;
- turning points;
- end behaviour;
- asymptotes;
- period.

An optional accuracy band covers "plot accurately" items.

- **Serves:** 0.2 quadratics, cubics and reciprocals; 0.3 exponential, log, trigonometric and rational curves; later sketching derivatives (1.3), PDF and CDF shapes (1.5) and payoff diagrams (1.7).
- **Uses:** `plot-axes`, `draggable-point` (knots), `curve-layer`, `geo-layer` (placed asymptotes).
- **Interactions.**
  - Pointer:
    - Tap to add knots (at most 12) and drag them.
    - The curve is a monotone cubic Hermite spline (Fritsch-Carlson) through the knots, which adds no false turning points between them.
    - Drag dashed asymptote lines in from a palette.
    - Tag a knot as root, turning point or intercept.
    - Freehand mode simplifies a finger stroke to knots with Ramer-Douglas-Peucker.
  - Keyboard: a crosshair moves with the arrows and Enter adds a knot; Tab moves between knots.
  - **Equivalent input:** a feature form (fields for roots, intercept and turning points) grades against the same check, for learners who cannot sketch.
- **State:** `{ knots: { id, x, y, tag? }[], asymptotes: { axis: 'x' | 'y'; at: number }[] }`.
- **Answers:** `curve`, with extracted features: sign changes (roots), extrema near $y = 0$ (touch roots), turning points, the intercept, end directions, asymptotes and monotone intervals.
- **Config:** `{ axes: PlotAxesConfig; maxKnots?: number; mode: 'knots' | 'freehand'; palette?: ('asymptote-v' | 'asymptote-h')[]; given?: CurveSpec[] }`. The `given` curves cover items like "sketch $f'$ given $f$".
- **Check example:**
```ts
{ kind: 'curve', features: [ { type: 'root', x: -2, tol: 0.25 }, { type: 'touch', x: 1, tol: 0.25 },
  { type: 'yIntercept', y: 4, tol: 0.5 }, { type: 'end', side: '+inf', dir: 'up' }, { type: 'turning', count: 2 } ] }
```
- **Visual:**
  - The learner's curve is 2.5px `--manip`; knots are 14px handles with 44px hit areas.
  - After grading, a feature checklist shows a check or a cross per feature (design research section 4.5, checklist puzzles), and failed locations get an amber ring.
  - Reveal draws the true curve dashed in `--hint`.
- **Motion:** direct. On reveal, the learner's curve morphs to the true curve (800ms).
- **Reduced motion:** the true curve appears.
- **Accessibility:** the keyboard knot path, the feature form, and a description of the extracted features: "Crosses the x-axis at −2.1 and 0.9; one turning point at (−0.6, −3)".
- **Tutor:** describes the extracted features, which are visible to the learner. Targets: `knot-<id>`, `feature-<k>`.
- **Performance:** a spline evaluation at 200 samples takes under 0.5ms.
- **Artifact / web:** identical.
- **Generator:** yes. Polynomials with chosen roots and multiplicities; rational functions with asymptotes; transformed trigonometric curves.

### 6.8 `inequality-regions`: Inequality regions

**Composite · P0 · W2.** Inequalities in two variables:

- a boundary is solid for $\le$ and dashed for $<$;
- the side is chosen by testing a point;
- several half-planes intersect into a feasible region;
- the integer points in a region can be listed (GCSE);
- as an enrichment item, an objective line slides to the last vertex (linear programming).

- **Serves:** 0.2 (GCSE Higher); later 2.x optimisation intuition.
- **Uses:** `plot-axes`, `curve-layer` (boundaries), `region-selector` (half-planes), `draggable-point` (the test point), `slider` (objective level).
- **Interactions.**
  - Pointer: tap a side of each boundary to choose it; toggle each boundary between solid and dashed; drag the test point, and a checklist shows each inequality as true or false there; tap lattice points to select integer solutions.
  - Keyboard: boundaries are focusable. Left and Right choose a side; Space toggles solid and dashed; the lattice is a grid of toggles.
- **State:** `{ sides: Record<string, 'above' | 'below' | null>, styles: Record<string, 'solid' | 'dashed'>, test: [number, number], lattice: string[] }`.
- **Answers:** `set` (sides and styles, lattice points), `point` (the optimal vertex), `choice`.
- **Config:** `{ inequalities: string[]; task: 'shade' | 'find-inequalities' | 'integer-points' | 'optimise'; convention: 'shade-wanted' | 'shade-unwanted'; objective?: string; lattice?: boolean }`.
  - The convention is stated in the question line. Exam boards vary, so it is never left implicit.
- **Visual:**
  - Boundaries use slots, with labels.
  - The chosen region is `--manip-wash`; the intersection is computed as a single polygon.
  - The test point is a `--manip` handle. Its checklist uses neutral ink check and cross icons, because these are truth values, not grades.
  - Lattice points are 4px ink dots; selected ones are `--manip`.
- **Motion:** shading fades in over 150ms.
- **Reduced motion:** no fade.
- **Accessibility:** a list of boundaries with side choices: "y ≥ 2x + 1: shading above". Lattice points are toggle buttons; at most 120 are shown.
- **Tutor:**
  - Describe: "L1 y = 2x + 1 (solid), side above. L2 x + y = 6 (dashed), side not set. Test point (0, 0): L1 false, L2 true."
  - Targets: `boundary-<id>`, `side-<id>-above`, `test-point`, `lattice-<x>-<y>`.
- **Performance:** Sutherland-Hodgman clipping takes under 0.2ms.
- **Artifact / web:** identical.
- **Generator:** yes. Two to four inequalities that bound a region holding 3 to 12 integer points.

### 6.9 `sign-chart`: Sign chart

**Composite · P0 · W2.** Signs of factors across intervals. One row per factor, critical points on a shared number line, the sign of each factor in each interval, and a product row. Uses:

- quadratic inequalities (GCSE Higher);
- polynomial and rational inequalities (0.3);
- later, where a derivative is positive (1.3).

- **Serves:** 0.2, 0.3, 1.3.
- **Uses:** `number-line`, `data-table`, `region-selector` (solution intervals).
- **Interactions.**
  - Pointer: drag critical points onto the line, or type them; tap cells to cycle through +, −, 0 and "undefined"; tap product-row intervals to pick the solution set; tap an endpoint to make it open or closed.
  - Keyboard: grid navigation; + and − set a sign; Space toggles an endpoint.
- **State:** `{ criticals: number[], cells: Record<string, '+' | '-' | '0' | 'u'>, solution: Interval[] }`.
- **Answers:** `interval`, `state` (every cell correct).
- **Config:** `{ expression: string; relation: '>' | '>=' | '<' | '<='; given: 'factors' | 'criticals' | 'none'; graph?: boolean }`.
- **Visual:**
  - Factor rows are labelled in KaTeX. Interval columns alternate with `--bg-sunken` shading.
  - Sign chips are ink "+" and "−". Red and green would wrongly suggest grades.
  - The solution intervals are `--manip` on the line.
- **Motion:** toggles take 150ms.
- **Reduced motion:** instant.
- **Accessibility:** table semantics, with cells such as "x − 2 on the interval from 2 to 3: positive".
- **Tutor:** targets `cell-<row>-<k>`, `critical-<k>`, `solution-<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Factorised polynomials and rational functions with whole-number critical points.

### 6.10 `iteration-cobweb`: Iteration cobweb

**Composite · P0 · W2.** Iteration $x_{n+1} = g(x_n)$:

- GCSE Higher iteration to find a root;
- the cobweb diagram on $y = g(x)$ and $y = x$;
- convergence or divergence, depending on the slope at the fixed point ($\lvert g'(x^*) \rvert < 1$, met informally here);
- monotone against oscillating convergence;
- different rearrangements of one equation behaving differently.

Later uses: Newton's method (1.3), fixed points of Markov chains (1.5), recurrences (0.3).

- **Serves:** 0.2 iteration; 0.3 recurrences; 1.3; 1.5.
- **Uses:** `plot-axes`, `curve-layer`, `draggable-point` ($x_0$ on the x-axis), `stepper`, `data-table`.
- **Interactions.**
  - Pointer: drag $x_0$; step one iteration at a time, or run 20; switch between rearrangements.
  - Keyboard: $x_0$ is a slider; N steps; R runs.
- **State:** `{ g: string, x0: number, iterates: number[] }`.
- **Answers:** `numeric` ($x_3$, or a root to a given number of decimal places), `choice` (converges or diverges), `state`.
- **Config:** `{ g: string | string[]; x0: number; maxIter: number; show: 'cobweb' | 'table' | 'both'; dp?: number }`.
- **Visual:** $g$ in slot 1; $y = x$ as a 1.5px `--text-muted` line; cobweb segments as 1.5px ink with small arrowheads; $x_0$ as a `--manip` handle on the axis; an iterates table with tabular figures.
- **Motion:** each cobweb segment draws over 200ms during stepping. Dragging $x_0$ redraws every segment at once.
- **Reduced motion:** segments appear.
- **Accessibility:** table view. Describe: "x0 = 2. Iterates 2, 2.25, 2.41, ... settling near 2.62".
- **Tutor:** targets `x0`, `segment-<k>`, `rearrangement-<k>`.
- **Performance:** at most 50 iterations.
- **Artifact / web:** identical.
- **Generator:** yes. Cubics and quadratics, each with one rearrangement that converges and one that does not; answers to set decimal places.

---

## 7. Composites: Geometry and measures (GCSE exit test)

### 7.1 `geometry-board`: Geometry board

**Composite · P0 · W3.** Dynamic geometry for GCSE geometry and for trigonometry. It covers:

- angle facts and parallel lines; polygon angle sums;
- congruence and similarity;
- Pythagoras, with a dissection proof;
- right-angled trigonometry: the ratios stay fixed when you scale the triangle;
- the sine and cosine rules, $\frac{1}{2}ab\sin C$, and the ambiguous case;
- arcs and sectors; circle theorems;
- transformations, including negative and fractional enlargement;
- constructions and loci with compass and ruler;
- bearings;
- conics as loci (0.3), and a proof of the compound-angle formulae by rotation (0.3).

- **Serves:** GCSE geometry; 0.3 trigonometry and conics.
- **Uses:** `plot-axes` (optional grid), `geo-layer` (construction graph), `draggable-point`, `slider`, `data-table` (measurements), `tex-terms`, `stepper` (keyframes).
- **Tools** (each screen enables a subset): move, point, segment, line, ray, polygon, circle, compass (copies a radius), ruler (measures), protractor, perpendicular, parallel, midpoint, bisector, reflect, rotate, translate, enlarge, locus trace.
- **Interactions.**
  - Pointer:
    - Drag free points; derived objects follow.
    - Construct by tapping with the chosen tool.
    - Measurements update live, unless they are hidden for exam-style items.
    - Lock constraints, such as $AB = 5$.
    - Tap objects to answer ("tap the alternate angle").
  - Keyboard: Tab cycles points and objects; arrows move a point by one grid step; letter shortcuts choose tools; Enter confirms a construction step.
- **State:** `{ objects: GeoObjectSpec[], selection: string[], tool: string }`.
- **Answers:**
  - `set` (selected objects);
  - `numeric` (lengths, angles and areas worked out by the learner, with live readouts hidden);
  - `point` (constructed positions);
  - `state`, with predicates `perpendicularBisectorOf(a, b)`, `bisects(angle)`, `congruent(t1, t2)`, `similar(t1, t2)`, `imageOf(shape, transform)`, `onLocus(cond)`, `constructionUses(tools)`;
  - `choice`.
- **Config:**
```ts
interface GeometryBoardConfig {
  axes?: PlotAxesConfig | null;                 // null: a plain board without coordinates
  objects: GeoObjectSpec[];
  tools: string[];
  measure?: { lengths?: 'live' | 'hidden'; angles?: 'live' | 'hidden'; areas?: 'live' | 'hidden'; dp?: number; unit?: 'cm' | 'm' | '' };
  preset?: 'angle-facts' | 'triangle-lab' | 'circle-theorems' | 'transformations' | 'constructions' | 'bearings' | 'conic-locus';
  keyframes?: { caption: string; objects: Partial<GeoObjectSpec>[] }[];   // dissections and rotation proofs
  answerTargets?: string[];
  notToScale?: boolean;                         // exam-style: "Not drawn accurately", measurements hidden
}
```
- **Presets:**

  | Preset | What it gives the screen |
  |---|---|
  | `angle-facts` | Parallel lines and a draggable transversal; angle labels |
  | `triangle-lab` | A triangle with side and angle readouts; a ratio panel; lock controls; swinging a side for the ambiguous case |
  | `circle-theorems` | Points constrained to a circle; theorem angles linked |
  | `transformations` | A grid, and image placement by vertex |
  | `constructions` | Compass and ruler only; arcs persist |
  | `bearings` | A north line at each point, angles measured clockwise from north |
  | `conic-locus` | A focus and directrix, or two pins and a string; locus tracing |

- **Visual:**
  - Primary strokes 2px ink; construction lines 1px `--text-muted`, with compass arcs kept, as exams require.
  - Free points are `--manip`; derived points are 6px ink.
  - Angle arcs carry degree labels; equal sides get tick marks, parallel lines get arrows, right angles get squares.
  - The measurement panel sits beside the board on desktop and below it on mobile.
- **Motion:** free points move directly and derived objects follow every frame. Keyframe transitions run 600 to 800ms with `ease-morph`, for example dissection pieces sliding into place. Show-why `angle-chase` flashes equal angles one after another.
- **Reduced motion:** keyframes step, with Play; flashes become static highlights.
- **Accessibility:**
  - Every object has a name and its properties: "triangle ABC; angle ABC = 47 degrees".
  - An object list is the text alternative.
  - Construction works from the keyboard.
  - Measurement changes are announced, debounced.
- **Tutor:**
  - Describe: "Triangle ABC: A(0, 0), B(4, 0), C(1, 3). AB = 4, angle A = 71.6°. Tool: move. Selected: none."
  - Targets: object ids such as `point-A`, `segment-AB`, `angle-ABC`, `circle-1`.
  - When measurements are hidden, describe hides them too.
- **Performance:** at most 120 objects. Evaluating the construction graph takes under 1ms per frame, with analytic intersections.
- **Artifact / web:** identical.
- **Generator:** yes:
  - triangles built on Pythagorean triples or with tidy trigonometric values;
  - angle-chase configurations;
  - grid transformations with whole-number coordinates;
  - bearings problems;
  - sine-rule cases deliberately set up to be ambiguous.

### 7.2 `solid-viewer`: Solid viewer

**Composite · P0 · W3.** 3D solids for GCSE measures:

- cuboids, prisms, cylinders, cones, pyramids, spheres, hemispheres and frustums;
- nets that fold and unfold;
- volume and surface area;
- plans and elevations;
- 3D Pythagoras and trigonometry (the space diagonal, the angle between a line and a plane);
- similar solids (area factor $k^2$, volume factor $k^3$, by stacking cubes);
- volume by counting unit cubes.

- **Serves:** GCSE measures; 1.3 and 1.4 previews.
- **Uses:** `view-3d`, `slider` (dimensions), `region-selector` (painting faces), `data-table`, `tex-terms`.
- **Interactions.**
  - Pointer:
    - Drag to rotate; sliders change dimensions.
    - Tap faces to paint them; a running surface-area counter tracks the painted faces.
    - "Unfold" and "Fold" turn the solid into its net and back.
    - Tap edges, diagonals and internal triangles.
    - Use the front, side and plan view buttons.
    - In cubes mode, tap a face to add a cube on it, and long-press to remove one.
  - Keyboard: the `view-3d` keys, plus N to unfold and A to add a cube at the focused face.
- **State:** `{ solid, dims: Record<string, number>, camera, painted: string[], unfolded: boolean, selected: string[], cubes?: [number, number, number][] }`.
- **Answers:** `numeric` (volume, area, a length, an angle), `set` (selected elements), `state` (cubes matching a given plan and elevations).
- **Config:** `{ solid: 'cuboid' | 'prism' | 'cylinder' | 'cone' | 'pyramid' | 'sphere' | 'hemisphere' | 'frustum' | 'cubes'; dims: Record<string, number>; editable?: string[]; show?: { net?: boolean; diagonals?: boolean; views?: boolean }; task: 'volume' | 'surface' | 'net' | 'pythagoras-3d' | 'views' | 'similar' | 'free' }`.
- **Visual:** as `view-3d`. Painted faces are `--manip-wash`; edge dimensions are KaTeX labels; the net lies flat in 2D once unfolded.
- **Motion:** rotation is direct. The net folds and unfolds over 800ms; an added cube pops in over 150ms.
- **Reduced motion:** the net steps; cubes appear.
- **Accessibility:** view buttons; a list of faces with their areas; a description of the solid and its dimensions.
- **Tutor:** targets `face-<id>`, `edge-<id>`, `diagonal-<id>`, `view-<name>`, `net`.
- **Performance:** curved solids use 32 segments, keeping within 200 faces.
- **Artifact / web:** identical.
- **Generator:** yes. Dimensions with tidy volumes and areas; scale factors for similar solids; cube arrangements for plan-and-elevation items.

---

## 8. Composites: Statistics and probability

The probability composites are shared with the 1.5 cluster. The more demanding configuration of the two wins, and this section is the Stage 0 minimum.

### 8.1 `dot-plot-stats`: Dot-plot statistics

**Composite · P0 · W3.** Summary statistics by manipulation. Drag data points on a line and watch these respond:

- the mean, as a balance point: a fulcrum tips until it sits under the mean;
- the median, mode and range;
- the quartiles, the IQR and a box plot;
- the standard deviation, as a preview of 1.6.

What it teaches:

- **Resistance to outliers.** One outlier moves the mean, not the median. Returns have fat tails, which is why the median and median absolute deviation matter.
- **Constraint puzzles,** such as five numbers with mean 6 and median 4.
- **Comparing two distributions.**

- **Serves:** GCSE averages and spread; 1.1 descriptive statistics; 1.6.
- **Uses:** `number-line`, `draggable-point` (stacked dots), `bar-layer` (box glyph), `geo-layer` (fulcrum), `data-table`.
- **Interactions.**
  - Pointer: drag dots; tap + to add a dot; long-press to delete one; toggle which statistics show. Before a statistic is revealed, drag a marker to your estimate of it.
  - Keyboard: each dot is a slider; A adds a dot; Delete removes one.
- **State:** `{ data: { id, x }[], shown: string[], predictions: Record<string, number> }`.
- **Answers:** `numeric` (statistics), `state` (predicate `satisfies({ mean?, median?, range?, iqr?, n? })`), `point` (a prediction), `choice` (which statistic changes).
- **Config:** `{ data: number[]; min: number; max: number; step: number; n?: { min: number; max: number }; editable: 'move' | 'add' | 'none'; show: ('mean' | 'median' | 'mode' | 'range' | 'quartiles' | 'box' | 'sd' | 'deviations' | 'fulcrum')[]; compare?: number[]; quartiles: 'gcse' | 'linear' }`.
- **Quartile convention** [our choice]: Stage 0 uses the GCSE positional convention, positions $\frac{n+1}{4}$ and $\frac{3(n+1)}{4}$. When 1.1 introduces NumPy, whose default is linear interpolation, a note shows both answers side by side.
- **Visual:**
  - Dots are 14px `--manip`, stacked.
  - The mean fulcrum is a slot 2 triangle under the line.
  - The median is a vertical ink line with a label. The box plot sits below in ink outline.
  - Deviation lines are `--text-muted`. Predictions are dashed markers.
- **Motion:** dragging is direct. In balance lessons the line tilts about the fulcrum on `spring-physical`.
- **Reduced motion:** the tilt does not oscillate.
- **Accessibility:** a table view of the sorted data and its statistics. Dots read as "data point 3 at 7". Live: "Mean 6.2, median 5".
- **Tutor:**
  - Describe: "n = 7: 2, 3, 3, 5, 6, 8, 20. Mean 6.71, median 5. Shown: mean, median."
  - Targets: `dot-<id>`, `mean`, `median`, `box`, `prediction-<stat>`.
- **Performance:** at most 60 dots, in SVG.
- **Artifact / web:** identical.
- **Generator:** yes. Data sets with whole-number statistics; constraint puzzles whose solutions the generator verifies.

### 8.2 `stat-chart`: Statistics charts

**Composite · P0 · W3.** Build and read the standard charts:

- bar, dual and composite bar, and pie charts;
- line charts (time series) and frequency polygons;
- histograms with unequal class widths: frequency density, and area equals frequency. This is the GCSE Higher idea that becomes the probability density idea in 1.5;
- cumulative frequency curves, read for the median and quartiles;
- box plots from a summary, and back-to-back stem-and-leaf diagrams;
- misleading charts with truncated axes, as a Trap lesson.

- **Serves:** GCSE statistics; 1.1 plotting; 1.5 densities.
- **Uses:** `plot-axes`, `bar-layer`, `curve-layer`, `draggable-point`, `geo-layer` (pie sectors), `data-table`.
- **Interactions.**
  - Pointer:
    - Build a chart by dragging bar heights, histogram heights or pie boundaries; they snap to set steps, or to whole degrees.
    - Plot cumulative frequency points, then join them.
    - Read a chart by tapping bars, or by dragging a reading line across, then down to the axis.
  - Keyboard: bars, bins and sectors are sliders; the reading line is a slider.
- **State:** `{ type, values: Record<string, number>, points?: [number, number][], readings: { kind, at, value }[] }`.
- **Answers:** `numeric` (values read; a frequency from an area), `state` (the chart matches the data within the snap), `point` (plotted points), `set` (selected bars).
- **Config:** `{ type: 'bar' | 'dual-bar' | 'composite-bar' | 'pie' | 'line' | 'freq-polygon' | 'histogram' | 'cumulative' | 'box' | 'stem-leaf'; data: unknown; editable?: boolean; readings?: ('median' | 'lq' | 'uq' | 'value-at')[]; axes?: PlotAxesConfig; truncated?: boolean }`.
- **Visual:** dataviz rules throughout: slot colours, direct labels, light gridlines.
  - Histograms label the y-axis "Frequency density" and can overlay unit tiles.
  - Pies have direct labels and angle values.
  - Stem-and-leaf uses a tabular layout with a key.
- **Motion:** dragging is direct. Show-why keys:
  - `area`: unit tiles fill a bin, 480ms;
  - `misleading`: the truncated axis expands to zero and the difference shrinks, 600ms.
- **Reduced motion:** stepped.
- **Accessibility:** a table view is mandatory. Bars and sectors are sliders. The reading line announces its values.
- **Tutor:** describes the chart type and its visible values. Targets: `bar-<id>`, `bin-<lo>-<hi>`, `sector-<id>`, `reading-line`, `point-<k>`.
- **Performance:** SVG, at most 60 bars.
- **Artifact / web:** identical.
- **Generator:** yes. Grouped data sets with consistent totals; frequency densities with tidy numbers; cumulative frequency data with readable quartiles.

### 8.3 `scatter-fit`: Scatter and fit

**Composite · P0 · W3.** Bivariate data:

- scatter plots, and the type and strength of correlation;
- outliers; dragging a line of best fit by eye;
- the interpolation-versus-extrapolation trap, and the correlation-is-not-causation trap;
- residuals as vertical segments;
- squared residuals as squares whose total area the learner tries to minimise. This is least squares, previewed in Stage 0 and formalised in 1.4 and 1.6;
- log axes to straighten exponential and power-law data (0.3).

- **Serves:** GCSE scatter graphs; 0.3 linearising with logs; 1.4 least squares; 1.6 regression (P1 extensions: $R^2$ and a residual plot).
- **Uses:** `plot-axes`, `draggable-point` (two line handles; data points in influence tasks), `curve-layer`, `geo-layer` (residuals and squares), `slider`, `data-table`.
- **Interactions.**
  - Pointer:
    - Drag the line by either handle, or grab its middle to translate it.
    - Toggle residuals and squares.
    - Drag an x marker to read a prediction.
    - Toggle log axes.
    - In influence tasks, drag one data point and watch the fitted line respond.
  - Keyboard: handles are 2D points; M toggles the fitted line, where the screen allows it.
- **State:** `{ line: [[number, number], [number, number]], residuals: boolean, squares: boolean, logX: boolean, logY: boolean, points?: [number, number][] }`.
- **Answers:**
  - `curve`, graded by the sum of squared errors being within a set ratio of the minimum, which is fairer than a fixed band on the slope;
  - `numeric` (a prediction);
  - `choice` (correlation type).
- **Config:** `{ data: [number, number][] | { seed: number; model: 'linear' | 'exp' | 'power'; n: number; noise: number; outliers?: number }; task: 'fit' | 'read' | 'classify' | 'linearise' | 'influence'; show?: ('residuals' | 'squares' | 'fit')[]; axes: PlotAxesConfig; sseRatio?: number }`.
- **Visual:**
  - Data points are 6px slot 1 dots. They are `--manip` only when movable.
  - The learner's line is 2.5px `--manip` with two handles.
  - Residuals are 1px `--text-muted`; squares are slot 2 at 15% with outlines.
  - The sum of squared errors appears as a readout with tabular figures. The fitted line is dashed ink.
- **Motion:** direct. On reveal, the fitted line morphs from the learner's line over 600ms.
- **Reduced motion:** it appears.
- **Accessibility:** a table view. Describe: "Line y = 1.8x + 2.1; squared-error total 41.2". Correlation is given in words in Stage 0, and as $r$ from 1.6.
- **Tutor:** targets `handle-1`, `handle-2`, `point-<k>`, `residual-<k>`, `sse`.
- **Performance:** SVG up to 200 points; the points move to canvas beyond that.
- **Artifact / web:** identical.
- **Generator:** yes. Seeded linear, exponential and power-law data with noise and optional outliers.

### 8.4 `outcome-grid`: Outcome grid

**Composite · P0 · W3.** Two-way sample spaces: two dice, a coin and a die, cards by suit and rank, two stocks up or down. Each outcome is a cell. The learner:

- shades events and counts them;
- applies a condition, so the grid shrinks: ruled-out cells dim and the denominator changes;
- checks independence by comparing row proportions;
- finds the distribution of a sum.

This is the prototype `DiceGrid`, generalised.

- **Serves:** GCSE sample spaces; 0.3 counting; 1.5 conditional probability (the reference lesson).
- **Uses:** `region-selector` (grid), `tex-terms` (cell labels), `geo-layer` (event outlines), `stepper`.
- **Interactions.**
  - Pointer: tap or paint cells to shade them; apply a condition from chips or row and column headers; switch the cell display between pair, sum, product, maximum and difference.
  - Keyboard: roving grid; Space toggles a cell; C opens the condition chooser.
- **State:** `{ shaded: string[], condition: string | null, display: 'pair' | 'sum' | 'product' | 'max' | 'diff' }`.
- **Answers:** `set`, `numeric` (a count or a probability), `choice`.
- **Config:** `{ rows: { label: string; values: (string | number)[] }; cols: { label: string; values: (string | number)[] }; display?: string; weights?: number[][]; given?: { shaded?: string[]; marked?: string; condition?: string }; task: 'shade' | 'count' | 'probability' | 'conditional'; event?: string }`.
- **Visual:** as in the prototype: cell buttons with `--r-xs` corners and pair labels; shaded cells `--manip-wash`; ruled-out cells at `--out`; event outlines 2px ink; marked cells with a slot 2 dot.
- **Motion:** as in the prototype. `shrink` staggers 50ms per row; `flash` blinks twice at 150ms; `peek` briefly shows all outcomes.
- **Reduced motion:** as in the prototype: no stagger, and static highlights that stay.
- **Accessibility:** as in the prototype: `role="grid"`, cells such as "First die 5, second die 3", and a live count.
- **Tutor:**
  - Describe: "Two dice, 36 cells. Condition: at least one 5 (11 cells). Shaded: none. Display: pair."
  - Targets: `cell-<r>-<c>`, `row-<r>`, `col-<c>`, `condition`.
- **Performance:** at most 52 cells.
- **Artifact / web:** identical.
- **Generator:** yes. Events on dice, coins, spinners and cards; conditional items with tidy fractions.

### 8.5 `tree-diagram`: Tree diagram

**Composite · P0 · W3.** Tree diagrams in two modes:

- **Counting:** the multiplication principle, where the number of leaves is the product of the branch counts.
- **Probability:** multiply along branches and add across leaves; with and without replacement; conditional probabilities on second-stage branches. Reversing the tree (Bayes) is previewed in 1.5.

- **Serves:** GCSE probability; 0.3 counting; 1.5.
- **Uses:** `geo-layer` (branches), `numeric-entry` (branch labels), `region-selector` (leaves), `tex-terms`, `stepper`.
- **Interactions.**
  - Pointer:
    - Add branches with a node's + button.
    - Type branch probabilities in place, with a fraction keypad.
    - Tap leaves that make up an event; their products and sum appear.
    - In counting mode, identical subtrees can collapse into a count.
  - Keyboard: the tree pattern; Enter edits a branch; Space selects a leaf.
- **State:** `{ tree: { label, p?: string, children?: Node[] }, selected: string[] }`.
- **Answers:** `numeric` (an event probability, a leaf count), `state` (every branch probability correct), `set` (leaves).
- **Config:** `{ stages: { label: string; outcomes: string[]; probs?: (string | null)[]; dependsOnPrevious?: boolean }[]; mode: 'count' | 'probability'; event?: string; grow: 'given' | 'learner'; maxLeaves?: number }`.
  - In `probs`, a `null` entry is a branch the learner fills in. `maxLeaves` defaults to 16.
- **Visual:**
  - The tree runs left to right with 1.5px ink branches.
  - Branch probabilities are KaTeX at each branch's midpoint.
  - Leaves show the outcome and the product along the path. Selected leaves are `--manip-wash`, with the sum row below.
- **Motion:** a new branch grows from its node over 200ms. The tree re-lays itself out on `spring-physical`, as design research section 4.3 suggests for probability trees.
- **Reduced motion:** instant layout.
- **Accessibility:** `role="tree"`. Branches read as "First draw red, probability 3 over 8"; leaves as "red then blue: 3/8 × 5/7".
- **Tutor:** targets `branch-<path>`, `leaf-<path>`, `sum`.
- **Performance:** at most 16 leaves; larger trees collapse to counts.
- **Artifact / web:** identical.
- **Generator:** yes. Bags of counters with and without replacement; two-stage events; counting trees.

### 8.6 `trial-simulator`: Trial simulator

**Composite · P0 · W3.** Predict first, then run seeded trials: 10, 100, 1,000 or 10,000. A histogram or a running-proportion trace converges on the exact value. It covers:

- relative frequency and expected frequency (GCSE);
- theory against experiment;
- checking a counting answer by simulation (0.3);
- sampling from a population, for bias and capture-recapture.

Later uses in 1.5: the law of large numbers, the central limit theorem, random walks.

- **Serves:** GCSE probability and sampling; 0.3; 1.5 (heavily).
- **Uses:** `bar-layer`, `curve-layer`, `plot-axes`, `data-table`, the `seeded-rng` service.
- **Interactions.**
  - Pointer: tap a batch-size button to run; reset; "New seed", for exploration; filter trials, keeping only some (as in the reference lesson).
  - When `predictFirst` is set, the run buttons open only after the learner's estimate is checked.
  - Keyboard: the buttons.
- **State:** `{ seed, trials: number, counts: Record<string, number>, trace: number[] (downsampled to 360 points), open: boolean }`.
- **Answers:** `numeric` (the prediction), `state` (at least N trials run).
- **Config:** `{ experiment: { kind: 'dice' | 'coins' | 'spinner' | 'bag' | 'cards' | 'population' | 'custom'; spec: unknown; event: string; filter?: string }; batches: number[]; display: ('last' | 'counts' | 'histogram' | 'trace' | 'share')[]; exact?: number; predictFirst?: boolean; seed: number }`.
- **Seed decision** [our choice]: Reset keeps the same seed, so a run can be repeated and discussed. "New seed" changes it.
- **Visual:** as in the prototype simulation: the last roll, counts, a share bar with the target marker, and a trace with a dashed line at the exact value.
- **Motion:** a batch animates in `requestAnimationFrame` chunks over at most 1.1s, as in the prototype.
- **Reduced motion:** results appear at once.
- **Accessibility:** a counts table. Final counts are announced after each batch, never per frame.
- **Tutor:**
  - Describe: "Two dice, keep at least one 5. Rolled 1,000, kept 309, total 10 in 27 (0.087). Exact 1/11 shown."
  - Targets: `run-<n>`, `trace`, `target-line`, `counts`.
- **Performance:**
  - Up to 10,000 trials run on the main thread, at most 2ms per frame.
  - 100,000 or more go to a worker; that is P0 for 1.5's central limit theorem.
- **Artifact / web:** identical. The worker starts from a `blob:` URL in the Artifact.
- **Generator:** seeds only. The experiments are authored.

---

## 9. Composites: Precalculus (0.3)

Some precalculus topics need no separate widget; they are configurations of widgets specified elsewhere:

| Topic | Configuration |
|---|---|
| Limits | `graph-explorer` with the `approach` and `holes` overlays and a values table |
| Rational functions | `graph-explorer` with asymptotes and holes, plus `sign-chart` |
| Conic sections | `geometry-board` with the `conic-locus` preset, plus `graph-explorer` implicit curves |
| Composite and inverse functions | `function-machine`, plus `graph-explorer` with `reflectYX`, `hlineTest` and domain handles |
| Parametric curves | `graph-explorer` with the `parametric` family |

### 9.1 `slide-rule`: Slide rule

**Composite · P0 · W3.** Logarithms as lengths. Two log scales slide against each other:

- multiplication becomes adding lengths: $\log ab = \log a + \log b$;
- division becomes subtracting lengths;
- powers become repeated addition;
- a change of base rescales every length by the same factor.

It also builds magnitude sense, the habit of reading log-scale charts (price charts, decibels), and the finance point that log returns add.

- **Serves:** 0.3 logs and log laws, change of base; 0.1 orders of magnitude (late in the course); 1.7 log returns.
- **Uses:** `number-line` (two of them, log10), `draggable-point` (the sliding scale and the cursor), `tex-terms`, `geo-layer` (hairline).
- **Interactions.**
  - Pointer: drag the lower scale sideways; drag the cursor hairline; tap a number on the upper scale to align the lower scale's 1 under it.
  - Keyboard: the lower scale's offset is a slider (log units); the cursor is a slider.
- **State:** `{ offset: number, cursor: number }`.
- **Answers:** `numeric` (a product or quotient read off), `state` (aligned to a value), `choice`.
- **Config:** `{ range: [1, 10] | [1, 100]; base?: 10 | 2 | 'e'; showLengths?: boolean; task: 'multiply' | 'divide' | 'power' | 'explore' }`.
- **Visual:** two rulers with log ticks (1 to 10, with minor ticks); the lower ruler has a `--manip` outline; lengths are shown as brackets labelled $\log_{10} 2$; the hairline is `--manip`.
- **Motion:** direct.
- **Reduced motion:** n/a.
- **Accessibility:** sliders. Describe: "Lower 1 under upper 2. Cursor at lower 3 reads upper 6."
- **Tutor:** targets `upper-<v>`, `lower-<v>`, `cursor`, `length-<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Products and quotients that land on readable ticks.

### 9.2 `unit-circle`: Unit circle

**Composite · P0 · W3.** Trigonometric functions as the coordinates of a rotating point: $\cos\theta$ is $x$ and $\sin\theta$ is $y$. It covers:

- degrees and radians, with the radian shown by wrapping the radius around the circle;
- signs by quadrant, reference angles and symmetry identities;
- exact values at 30°, 45° and 60°;
- $\sin^2\theta + \cos^2\theta = 1$ by Pythagoras;
- $\tan\theta$ as a slope and as a tangent segment;
- solving $\sin\theta = k$, where a horizontal line meets the circle twice;
- arc length and sector area.

It is the base for complex numbers and rotation matrices.

- **Serves:** GCSE exact values; 0.3 trigonometry; 0.3 complex numbers; 1.4 rotations.
- **Uses:** `plot-axes` (equal aspect), `geo-layer`, `draggable-point` (on the circle), `slider` (angle), `tex-terms`, `data-table`.
- **Interactions.**
  - Pointer: drag the point; it snaps to 15° or $\frac{\pi}{12}$ when `snap` is set. Type an angle. Toggle projections, the tangent segment, the reference triangle and the horizontal line $y = k$, set with a slider. Winding past 360° is tracked.
  - Keyboard: the point is a slider, in 1° steps or 15° with Shift.
- **State:** `{ theta: number (radians, unbounded), units: 'deg' | 'rad', overlays: string[], k?: number }`.
- **Answers:** `point` (an angle), `numeric` (sine and cosine values, angles), `set` (solutions in a range, chosen from the intersection points), `expression` (exact values).
- **Config:** `{ units: 'deg' | 'rad' | 'both'; snap?: number; overlays: ('cos' | 'sin' | 'tan' | 'reference' | 'quadrants' | 'arc' | 'sector' | 'hline')[]; exactLabels?: boolean; range?: [number, number] }`.
- **Visual:**
  - The circle is 2px ink; the point is `--manip`.
  - The cosine segment is slot 1 on the x-axis, and the sine segment is slot 2, vertical. Both are labelled.
  - The angle arc is `--text-muted` with its value. Quadrant labels are shown.
  - When `exactLabels` is set, exact KaTeX values label the special angles.
- **Motion:** direct. Show-why keys:
  - `radian`: the radius lifts and wraps around the circumference, 800ms;
  - `symmetry`: a mirrored point appears with its equal coordinate highlighted.
- **Reduced motion:** before-and-after.
- **Accessibility:** the angle slider reads "angle 150 degrees; cos −0.866; sin 0.5". There is a table of the special angles.
- **Tutor:**
  - Describe: "θ = 150° (5π/6). cos −0.866, sin 0.5. Shown: cos, sin, reference triangle."
  - Targets: `point`, `seg-cos`, `seg-sin`, `seg-tan`, `arc`, `hline`, `quadrant-<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Exact values at special angles; solving $\sin\theta = k$ in a range; converting between degrees and radians.

### 9.3 `circle-to-wave`: Circle to wave

**Composite · P0 · W3.** Links rotation to waves:

- as the angle runs, $\cos$ and $\sin$ unroll into graphs;
- amplitude, period, phase shift and vertical shift become transformations of the circle's motion: $y = A\sin(B(x - C)) + D$;
- two waves of the same frequency add to one wave: phasor addition, $a\sin x + b\cos x = R\sin(x + \alpha)$;
- periodic modelling (tides, seasonal data).

Fourier ideas (P2) and complex exponentials build on this later.

- **Serves:** 0.3 trigonometric graphs, transformations, $R\sin(x + \alpha)$; P2 previews.
- **Uses:** `unit-circle`, `graph-explorer`, `slider`, `draggable-point`.
- **Interactions.**
  - Pointer: drag the circle point or the graph's tracer; the two are linked. Play runs the angle. Sliders set $A$, $B$, $C$ and $D$. In phasor mode, drag the tips of two phasors.
  - Keyboard: sliders; P plays and pauses.
- **State:** `{ theta, params: { A, B, C, D }, phasors?: { r, phi }[], playing: boolean }`.
- **Answers:** `numeric` (amplitude, period, phase), `expression` (the wave's equation), `curve` (match a target wave, parameters within tolerance), `state`.
- **Config:** `{ mode: 'unwrap' | 'transform' | 'phasor'; params?: Record<string, SliderConfig>; target?: string; units: 'deg' | 'rad' }`.
- **Visual:**
  - Circle on the left (on top on mobile), graph on the right.
  - A dashed horizontal connector joins the circle point to the graph point, so the height is visibly shared.
  - The learner's wave is `--manip`; the target is dashed ink.
  - Phasors are slot 1 and slot 2 arrows, and the resultant is ink.
- **Motion:** direct. Play runs one revolution in 4s, linearly; the learner starts it, and it stops at the end of a turn.
- **Reduced motion:** Play advances 15° per press instead of running.
- **Accessibility:** sliders; the equation described in words; a table of wave values at multiples of 30°.
- **Tutor:** targets `circle-point`, `tracer`, `slider-<p>`, `connector`, `phasor-<k>`, `resultant`.
- **Performance:** both panels together use at most 4ms per frame.
- **Artifact / web:** identical.
- **Generator:** yes. Target waves to match; phasor sums with tidy $R$.

### 9.4 `sequence-lab`: Sequence lab

**Composite · P0 · W3.** Sequences as lists, rules and plots:

- term-to-term and position-to-term rules;
- arithmetic sequences (constant difference, a straight plot) and geometric sequences (constant ratio, an exponential plot);
- difference tables: constant second differences mean a quadratic sequence (GCSE Higher);
- Fibonacci and other recurrences, $u_{n+1} = f(u_n)$;
- convergence and divergence;
- the sequence of partial sums $S_n$;
- compound growth as a geometric sequence.

- **Serves:** GCSE sequences; 0.3 sequences and recurrences; later dynamic programming (1.8) and Markov chains (1.5).
- **Uses:** `data-table` (terms and differences), `bar-layer` (terms as dots or bars), `plot-axes`, `slider` (first term, difference, ratio), `tex-terms`.
- **Interactions.**
  - Pointer: enter terms; drag sliders; extend the difference table (the learner enters the differences, or they fill automatically in explore mode); toggle dots and bars; type a rule and see whether it generates the given terms.
  - Keyboard: table navigation; sliders.
- **State:** `{ terms: (number | null)[], differences: (string | null)[][], rule?: string, recurrence?: string, params: Record<string, number> }`.
- **Answers:** `expression` (the nth-term rule), `numeric` (term values; the first $n$ where $u_n$ passes a value), `state` (difference table complete), `choice` (the type of sequence).
- **Config:** `{ given: number[] | { rule: string } | { recurrence: string; u1: number }; show: ('table' | 'differences' | 'plot' | 'partial-sums')[]; n: number; task: 'next-terms' | 'nth-term' | 'classify' | 'recurrence' | 'limit' | 'explore'; params?: SliderConfig[] }`.
- **Visual:**
  - Terms are dots or bars at $n = 1, 2, \dots$.
  - Difference rows sit beneath, joined by chevrons in the classic layout. A constant row gets an ink bracket labelled "constant".
  - Partial sums are slot 2 bars, with a dashed line at the limit.
- **Motion:** dots follow the sliders directly.
- **Reduced motion:** n/a.
- **Accessibility:** table semantics and a table view of the plot.
- **Tutor:**
  - Describe: "Terms 3, 7, 11, 15, ?. First differences 4, 4, 4."
  - Targets: `term-<n>`, `diff-<level>-<n>`, `rule`, `plot`.
- **Performance:** at most 50 terms.
- **Artifact / web:** identical.
- **Generator:** yes. Arithmetic, geometric and quadratic sequences with whole-number terms; recurrences with fixed points.

### 9.5 `sum-visualiser`: Sum visualiser

**Composite · P0 · W3.** Shows why summation formulas are true:

- **Gauss pairing.** A staircase plus a rotated copy makes a rectangle: $\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$.
- **Odd numbers.** Their sums are squares, built from L-shaped gnomons.
- **Arithmetic series** in general.
- **Geometric series,** two ways: by filling area (halves filling a square) and by the shift-and-subtract trick, $S - rS$.
- **Infinite geometric series.** Convergence when $\lvert r \rvert < 1$, divergence otherwise.
- **Sigma notation,** expansion and index shifts.

The finance transfer is perpetuities and annuities, where present value is a geometric series. The probability transfer is the expected value of a geometric random variable (1.5).

- **Serves:** 0.3 series and sigma notation; 1.5; 1.7.
- **Uses:** `region-selector` (tiles), `token-tray` (staircase blocks), `stepper`, `bar-layer` (partial sums), `tex-terms`, `slider` ($n$, $r$).
- **Interactions.**
  - Pointer: drag the $n$ slider. Drag the rotated copy of the staircase into place; it snaps when it completes the rectangle, so the "aha" is the learner's own action. Drag $r$ from −1.2 to 1.2 and watch the partial sums settle or blow up. Expand a sigma with an index slider. Step through shift-and-subtract: $S$ and $rS$ line up, and matching terms cancel.
  - Keyboard: sliders; the `token-tray` keys for the copy; the stepper keys.
- **State:** `{ mode, n, r, a?, copyPlaced: boolean, expandedTo: number, step: number }`.
- **Answers:** `numeric` (a sum), `expression` (the closed form), `state` (copy placed), `choice` (converges or not).
- **Config:** `{ mode: 'gauss' | 'odd-squares' | 'arith' | 'geom-area' | 'geom-shift' | 'partial-sums' | 'sigma'; n?: number; r?: number; a?: number; sigma?: string }`.
- **Visual:**
  - Unit squares are `--bg-surface` with ink outlines; the copy is slot 1 at 25%.
  - Geometric pieces alternate slot 1 and slot 3, with labels.
  - Partial sums are slot 1 bars with a dashed line at the limit. Cancelled terms are struck through.
- **Motion:** the copy snaps on `spring-snap`. Area pieces fill one per Next press, 300ms each. Cancelling takes 300ms.
- **Reduced motion:** stepped.
- **Accessibility:** a description and a table of partial sums.
- **Tutor:** targets `copy`, `staircase`, `piece-<k>`, `term-<k>`, `limit-line`.
- **Performance:** at most 400 squares ($n \le 20$).
- **Artifact / web:** identical.
- **Generator:** yes. Sums to evaluate; series to classify; present-value items.

### 9.6 `induction-chain`: Induction chain

**Composite · P0 · W3.** Proof by induction as falling dominoes. The chain falls only if:

- the first domino falls (the base case), and
- each domino knocks over the next (the inductive step, $P(k) \Rightarrow P(k + 1)$).

The learner supplies both parts. With no base case, the chain never starts. With a broken step, the chain stops at the first failure.

A companion lesson shows why checking cases is not proof: $n^2 - n + 41$ is prime for $n = 1, \dots, 40$, and the chain breaks at $n = 41$.

- **Serves:** 0.3 series proofs; 1.8 recursion and loop invariants.
- **Uses:** `geo-layer` (dominoes), `derivation` (the inductive step in fill or predict mode), `stepper`, `choice-cards`.
- **Interactions.**
  - Pointer: tap the first domino to check the base case. Complete the step derivation. Press Push to run the chain. In counterexample mode, slide a window along $n$, checking each case.
  - Keyboard: buttons; the `derivation` keys.
- **State:** `{ baseOk: boolean, stepOk: boolean, failingAt?: number, derivation: unknown }`.
- **Answers:** `state` (both parts valid), `expression` (lines of the step), `numeric` (the first failing $n$).
- **Config:** `{ statement: string; base: { n: number }; step: DerivationConfig; counterexample?: { expr: string; firstFail: number } }`.
- **Visual:** a row of rounded ink-outlined dominoes labelled $n = 1, 2, \dots$; fallen dominoes tilt; a broken link shows as a gap.
- **Motion:** the cascade topples each domino over 120ms on `spring-physical`. It runs for at most 2s, can be skipped, and is a boundary moment.
- **Reduced motion:** the dominoes show already fallen, with the failure gap marked.
- **Accessibility:** "Base case verified for n = 1; inductive step incomplete"; the derivation is accessible as in `derivation`.
- **Tutor:** targets `domino-<n>`, `base`, `step-line-<k>`, `push`.
- **Performance:** at most 30 dominoes visible, in a scrolling window.
- **Artifact / web:** identical.
- **Generator:** no. The statements are authored; seeds vary the counterexample windows.

### 9.7 `pascal-triangle`: Pascal's triangle

**Composite · P0 · W3.** Pascal's triangle:

- built by adding the two entries above;
- entry $\binom{n}{k}$ counts lattice paths: tap it to see a path, or step through them all;
- the coefficients of $(a + b)^n$;
- symmetry, $\binom{n}{k} = \binom{n}{n-k}$; row sums of $2^n$; the hockey stick;
- the pattern modulo 2 (Sierpinski).

Later uses: the binomial distribution (1.5) and counting random-walk paths.

- **Serves:** 0.3 binomial expansion and combinations; 1.5.
- **Uses:** `region-selector` (cells), `geo-layer` (paths), `numeric-entry` (cells), `stepper`.
- **Interactions.**
  - Pointer: tap a blank cell and enter its value; tap a filled entry to show a path or step through all its paths; select a diagonal run of cells to see the hockey-stick sum land; toggle parity colouring.
  - Keyboard: triangle navigation (Left and Right within a row, Up and Down to the neighbouring row); Enter edits; P shows paths.
- **State:** `{ rows: number, filled: Record<string, string>, highlight: string[], pathIndex?: number }`.
- **Answers:** `numeric` (entries), `set` (cells forming a pattern), `state` (rows correct).
- **Config:** `{ rows: number; prefilled: 'all' | 'edges' | 'none'; mode: 'build' | 'paths' | 'patterns' | 'mod'; mod?: number }`.
- **Visual:**
  - Rounded cells (`--r-sm`) in a brick layout, with tabular figures.
  - The path is a `--manip` polyline from the apex.
  - Parity colouring fills odd entries with slot 1 and also marks them with a dot, so colour is not the only cue.
- **Motion:** paths step at 300ms each. New values pop in over 150ms.
- **Reduced motion:** the path is drawn whole.
- **Accessibility:** cells read as "row 4, position 2: 6".
- **Tutor:** targets `cell-<n>-<k>`, `path`, `row-<n>`.
- **Performance:** 16 rows (136 cells) in SVG; modulo mode moves to canvas beyond 16 rows.
- **Artifact / web:** identical.
- **Generator:** yes. Missing entries; coefficient questions; path counts.

### 9.8 `binomial-expander`: Binomial expander

**Composite · P0 · W3.** Expanding $(a + b)^n$ by choices:

- each term picks $a$ or $b$ from each bracket;
- list every choice word, of which there are $2^n$ for small $n$;
- group the words by how many $b$s they hold, so each coefficient is $\binom{n}{k}$;
- the general term, $\binom{n}{k}a^{n-k}b^k$;
- finding a particular coefficient, sign traps included (the $x^3$ term in $(2 - 3x)^7$);
- approximations: $(1 + x)^n \approx 1 + nx$ for small $x$;
- the general binomial series for rational $n$, valid only when $\lvert x \rvert < 1$ (A-level). It is shown as truncated series against the curve, so the learner sees where it fails.

- **Serves:** 0.3 binomial expansion; 1.5 the binomial distribution.
- **Uses:** `token-tray` (bracket choices and word chips), `card-sort` (grouping), `tex-terms`, `area-model` (the square for $n = 2$), `graph-explorer` (approximation overlay).
- **Interactions.**
  - Pointer: tap brackets to choose $a$ or $b$ in each, which builds one word. "Generate all" lists every word. Drag words into groups by $k$. Enter coefficients. In general-term mode, a $k$ slider shows each term. In approximation mode, sliders set $x$ and the number of terms.
  - Keyboard: the `token-tray` keys; sliders.
- **State:** `{ n, words: string[], groups: Record<number, string[]>, k?: number, x?: number, terms?: number }`.
- **Answers:** `expression` (an expansion or term), `numeric` (a coefficient), `mapping` (words to groups), `state`.
- **Config:** `{ a: string; b: string; n: number | string; mode: 'choices' | 'group' | 'general-term' | 'approx' | 'rational-n'; target?: { power: number }; terms?: number }`.
- **Visual:** brackets in a row, each with its chosen term marked in `--manip`; words as chips; groups as zones labelled $k = 0$ to $n$; the general term with KaTeX slots.
- **Motion:** "Generate all" sends words into their groups (300ms each, staggered 80ms) as a demonstration. Everything else is direct.
- **Reduced motion:** instant.
- **Accessibility:** the `token-tray` model; terms described in words.
- **Tutor:** targets `bracket-<i>`, `word-<id>`, `group-<k>`, `term-<k>`.
- **Performance:** words for $n \le 5$ (32 words); general-term mode for $n \le 20$.
- **Artifact / web:** identical.
- **Generator:** yes. Coefficient questions with sign and power traps; approximation items.

### 9.9 `counting-slots`: Counting slots

**Composite · P0 · W3.** Counting by the multiplication principle. Fill $r$ ordered slots from $n$ options:

- with or without repetition;
- permutations $^nP_r$;
- combinations, as permutations divided by the $r!$ orders of each group (equivalent arrangements visibly collapse into one);
- words with repeated letters (divide by the repeats);
- circular arrangements;
- restrictions: "must be together" glues tokens, "must not be adjacent" uses the gaps method;
- complementary counting.

Stars-and-bars mode distributes identical items into distinct boxes.

- **Serves:** GCSE counting; 0.3 permutations and combinations; 1.5 counting (stars and bars is shared with that cluster).
- **Uses:** `token-tray` (slots, options, glue), `stepper` (enumeration), `data-table` (the list), `tex-terms` (the product of choices).
- **Interactions.**
  - Pointer:
    - Drag options into slots; each slot shows how many options it had when it was filled ("5 choices", "4 choices").
    - Step through the arrangements systematically, with Next.
    - "Collapse" stacks arrangements of the same set.
    - Glue two tokens into a block.
    - In stars-and-bars mode, drag dividers into the gaps between stars.
  - Keyboard: the `token-tray` keys; N for the next arrangement.
- **State:** `{ slots: (string | null)[], listed: string[][], collapsed: boolean, glued: [string, string][], dividers?: number[] }`.
- **Answers:** `numeric` (a count), `expression` (a product or formula), `state` (a valid arrangement), `set`.
- **Config:** `{ options: { id: string; label: string }[]; slots: number; repetition: boolean; ordered: boolean; restrictions?: ({ together: string[] } | { apart: [string, string] } | { fixed: { slot: number; option: string } })[]; mode: 'slots' | 'enumerate' | 'collapse' | 'stars-bars' | 'circular'; stars?: number; boxes?: number }`.
- **Visual:**
  - Slots are dashed boxes with their choice count in KaTeX above them.
  - The product line, $5 \times 4 \times 3$, sits underneath.
  - Enumerated arrangements scroll in a table. Collapsed groups become stacks with "×6" badges.
- **Motion:** the `token-tray` motion. Collapse stacks the arrangements over 400ms with `ease-morph`.
- **Reduced motion:** instant.
- **Accessibility:** the `token-tray` model, and a table of arrangements.
- **Tutor:** targets `slot-<i>`, `option-<id>`, `group-<k>`, `divider-<i>`, `product`.
- **Performance:** enumeration is capped at 120 arrangements (5!).
- **Artifact / web:** identical.
- **Generator:** yes. Counting templates with restrictions. Every generated answer is checked by brute-force enumeration in the generator's test.

### 9.10 `vector-plane`: Vector plane

**Composite · P0 · W3.** Vectors in two dimensions:

- column vectors as arrows; components;
- addition, tip to tail and by parallelogram; subtraction;
- scalar multiples and parallel vectors;
- magnitude and direction; unit vectors;
- position vectors; the point dividing a line in a ratio, $\vec{OP} = \mathbf{a} + \frac{2}{5}(\mathbf{b} - \mathbf{a})$;
- GCSE vector proofs on a skewed lattice built from $\mathbf{a}$ and $\mathbf{b}$;
- linear combinations and span;
- the dot product as projection.

The 3D mode uses `view-3d`. It is P0 because 1.4 comes before 1.5.

- **Serves:** GCSE vectors; 0.3 vectors; 1.4 (heavily).
- **Uses:** `plot-axes` (including a lattice grid), `geo-layer` (arrows), `draggable-point` (tips and tails), `slider` (scalars), `tex-terms` (column vectors), `view-3d`.
- **Interactions.**
  - Pointer: drag tips, and tails for free vectors. Drag the scalar sliders in $\lambda\mathbf{a} + \mu\mathbf{b}$. Build a path from O to a point by placing arrows tip to tail from a palette ($\mathbf{a}$, $-\mathbf{a}$, $\mathbf{b}$, ...). Toggle components, the parallelogram and the projection.
  - Keyboard: tips are grid points; sliders; the palette follows the `token-tray` keys.
- **State:** `{ vectors: Record<string, { tail: [number, number], tip: [number, number] }>, scalars: Record<string, number>, path: string[] }`.
- **Answers:** `point` (a tip position), `expression` (a vector in terms of $\mathbf{a}$ and $\mathbf{b}$), `numeric` (magnitude, a component, an angle, a dot product), `state` (predicates `pathReaches(P)`, `parallel(u, v)`), `choice`.
- **Config:** `{ vectors: { id: string; tex: string; x: number; y: number; z?: number; tail?: [number, number]; movable: 'tip' | 'both' | 'none' }[]; lattice?: { a: [number, number]; b: [number, number] }; show?: ('components' | 'parallelogram' | 'magnitude' | 'angle' | 'projection' | 'span')[]; task: 'add' | 'path' | 'express' | 'magnitude' | 'dot' | 'explore'; dims: 2 | 3 }`.
- **Visual:**
  - Arrows are 2.5px with filled heads.
  - Given vectors use slot colours, with bold labels ($\mathbf{a}$), following the notation table.
  - Movable tips are `--manip`.
  - Components are dashed `--text-muted` legs; the resultant is ink.
  - The lattice is drawn in 1px `--line`.
- **Motion:** direct. Show-why `tip-to-tail`: the second arrow slides its tail onto the first one's tip, 480ms.
- **Reduced motion:** stepped.
- **Accessibility:** a list of vectors with their components. Tips read as "tip of a at (3, 1)".
- **Tutor:** targets `vec-<id>`, `tip-<id>`, `scalar-<id>`, `resultant`, `path-<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Paths on lattices; magnitude, angle and dot-product items with tidy numbers; ratio-division items.

### 9.11 `matrix-grid`: Matrix grid

**Composite · P0 · W3.** Matrices as arrays of numbers, and the operations on them:

- dimensions; addition; scalar multiples;
- multiplication as row-by-column dot products, with each pair highlighted;
- when a product is defined;
- non-commutativity, with $AB$ and $BA$ computed side by side;
- the identity; the 2 × 2 determinant and inverse;
- solving 2 × 2 systems with an inverse;
- row operations, linked to `equation-stack`.

1.4 extends it.

- **Serves:** 0.3 matrices (exit test); 1.4.
- **Uses:** `data-table` (cells), `tex-terms`, `stepper`, `numeric-entry`.
- **Interactions.**
  - Pointer: edit entries. Tap a result cell to highlight its row and column and expand the dot-product sum. Fill result cells yourself. Swap the order with a button ($AB$ or $BA$).
  - Keyboard: grid navigation; Enter edits.
- **State:** `{ matrices: Record<string, number[][]>, result?: (string | null)[][], focus?: [number, number] }`.
- **Answers:** `state` (result cells correct), `numeric` (a determinant or an entry), `expression` (inverse entries as fractions), `choice` (defined or not; dimensions).
- **Config:** `{ matrices: { id: string; values: (number | string)[][]; editable?: boolean }[]; op: 'add' | 'scale' | 'multiply' | 'det' | 'inverse' | 'solve' | 'row-ops'; fill: 'all' | 'some' | 'none'; fractions?: boolean }`.
- **Visual:**
  - SVG brackets keep the cells editable. Cells use tabular figures.
  - The highlighted row has a slot 1 wash and the column a slot 2 wash. Terms in the expanded sum are tinted to match.
- **Motion:** in the walkthrough, the highlight sweeps across each row-and-column pair, 300ms per pair.
- **Reduced motion:** all pairs highlight together.
- **Accessibility:** tables with labelled cells ("A, row 2, column 1: 3"). Expansions are read as text.
- **Tutor:** targets `<matrix>-<r>-<c>`, `result-<r>-<c>`, `row-<matrix>-<r>`, `col-<matrix>-<c>`.
- **Performance:** at most 4 × 4.
- **Artifact / web:** identical.
- **Generator:** yes. Integer matrices whose inverses have whole-number or simple fractional entries; products that are and are not defined.

### 9.12 `linear-map`: Linear map

**Composite · P0 · W3.** A 2 × 2 matrix as a transformation of the plane:

- drag the images of $\hat{\imath}$ and $\hat{\jmath}$, and the whole grid follows;
- the columns of the matrix are those images;
- the unit square becomes a parallelogram whose signed area is the determinant: negative means the orientation flipped, zero means the plane collapsed onto a line;
- composition is one map after another (a matrix product, where order matters);
- the inverse undoes the map;
- rotation, reflection, shear and enlargement as matrices, which links the GCSE transformations to matrices.

- **Serves:** 0.3 matrices as transformations; 1.4 (heavily; eigenvectors are P0 there).
- **Uses:** `plot-axes`, `geo-layer` (transformed grid, unit square, test shape), `draggable-point` (basis images), `tex-terms`, `slider` ($t$, from the identity to $M$).
- **Interactions.**
  - Pointer: drag the tips of $\hat{\imath}$ and $\hat{\jmath}$. Drag the $t$ slider to morph the identity into $M$. Stack matrix chips to compose maps. Type entries.
  - Keyboard: basis tips are 2D handles; the $t$ slider; entries are editable cells.
- **State:** `{ M: [[number, number], [number, number]], t: number, stack: number[][][] }`.
- **Answers:** `expression` (a matrix), `numeric` (a determinant or an area), `point` (the image of a point), `state` (predicates `matrixEquals`, `isRotation`, `isReflection`), `choice`.
- **Config:** `{ initial: [[number, number], [number, number]]; show?: ('grid' | 'unit-square' | 'shape' | 'det')[]; shape?: [number, number][]; task: 'find-matrix' | 'apply' | 'determinant' | 'compose' | 'inverse' | 'explore'; snap?: number }`.
- **Visual:**
  - The original grid is `--line`; the transformed grid is slot 1 at 60%, 1px.
  - The unit square's image is slot 1 at 25%, with a determinant label and an orientation arrow.
  - Basis tips are `--manip`; the $\hat{\imath}$ shaft is slot 2 and the $\hat{\jmath}$ shaft slot 3, both labelled.
- **Motion:** direct; the $t$ slider is the learner's own morph.
- **Reduced motion:** n/a.
- **Accessibility:** entries are announced. Describe: "M = [[2, 1], [0, 1]], a shear; determinant 2".
- **Tutor:** targets `i-hat`, `j-hat`, `unit-square`, `det`, `entry-<r>-<c>`, `t`.
- **Performance:** at most 40 transformed grid lines per frame; trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Find the matrix of a described transformation; determinants with whole-number areas; compositions.

### 9.13 `complex-plane`: Complex plane

**Composite · P0 · W3.** Complex numbers as points and arrows:

- real and imaginary parts;
- addition as vector addition;
- multiplication as rotate-and-scale: the arguments add and the moduli multiply;
- multiplying by $i$ as a quarter turn;
- the conjugate as a reflection;
- modulus-argument form; division;
- the complex roots of a quadratic, shown with a linked parabola. As the parabola lifts off the axis, a conjugate pair of roots leaves the real line;
- powers and roots of unity (a regular polygon);
- a first look at $e^{i\theta}$.

- **Serves:** 0.3 complex numbers (exit test); 1.4 eigenvalues of non-symmetric matrices; P2 Fourier transforms and characteristic functions.
- **Uses:** `plot-axes` (Argand plane, equal aspect), `geo-layer`, `draggable-point`, `tex-terms`, `graph-explorer` (linked parabola), `slider`.
- **Interactions.**
  - Pointer: drag $z$ and $w$. Operation chips: $z + w$, $zw$, $\bar{z}$, $\frac{1}{z}$, $z^n$, roots. Polar handles let you drag along a ray (modulus) or around a circle (argument). In roots-of-unity mode, an $n$ slider.
  - Keyboard: 2D handles; operation chips are buttons.
- **State:** `{ points: Record<string, [number, number]>, op?: string, n?: number, quadratic?: { a, b, c } }`.
- **Answers:** `point` (a complex value), `expression` ($a + bi$ or polar form), `numeric` (modulus, argument), `set` (roots).
- **Config:** `{ points: { id: string; re: number; im: number; movable: boolean }[]; ops: ('add' | 'sub' | 'mul' | 'div' | 'conj' | 'pow' | 'roots')[]; form: 'cartesian' | 'polar' | 'both'; quadratic?: { a: number; b: number; c: number; editable?: boolean }; argUnits: 'deg' | 'rad' }`.
- **Visual:** as `vector-plane`. The result is ink. Argument arcs show the sum: a slot 1 arc plus a slot 2 arc equals the ink arc.
- **Motion:** direct. Show-why `multiply`: the arrow for $w$ rotates by $\arg z$ and scales by $\lvert z \rvert$, 600ms.
- **Reduced motion:** stepped.
- **Accessibility:** points announce their real and imaginary parts and their polar readouts.
- **Tutor:** targets `point-<id>`, `result`, `arg-<id>`, `op-<name>`, `parabola`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Arithmetic with whole-number parts; quadratics with complex roots; roots of unity.

---

## 10. Composites: Computer basics (0.4)

### 10.1 `typing-trainer`: Typing trainer

**Composite · P0 · W1.** Touch typing with home-row discipline. Targets [our choice]: 35 words per minute at 95% accuracy on prose by the end of 0.4, plus a separate code-symbols track. The trainer:

- unlocks letters adaptively: start with a few, and add the next once every unlocked key passes the speed and accuracy bar (in the manner of keybr);
- then drills code: Python's brackets, colons, quotes, underscores and operators, which programmers type constantly and typing courses neglect;
- then drills shortcuts (copy, paste, undo, save, select all, switch window), with each OS's own keys.

- **Serves:** 0.4 typing and shortcuts; it speeds up every later code drill.
- **Uses:** `speed-timer`, `data-table`, `bar-layer` (speed per key), the `seeded-rng` service (text generation). The keyboard picture is its own DOM.
- **Interactions.**
  - **Keyboard only, by nature.** The current character is highlighted.
  - **Stop on error** is the default for beginners: the cursor waits for the right key, and each wrong press counts against accuracy.
  - **The on-screen keyboard** highlights the next key and names its finger.
  - **Losing focus pauses the session.**
  - **Shortcut drills skip browser-reserved keys:** Ctrl+W, Ctrl+T and Ctrl+N close or open tabs, so they are shown but never drilled.
  - **Touch-only devices** see "Needs a physical keyboard", and the lesson moves on to other 0.4 items.
- **State:** `{ unlocked: string[], focusKey: string, text: string, pos: number, errors: number, keyTimes: Record<string, number[]>, wpm: number, accuracy: number }`.
- **Answers:** `state`, graded by predicate `session({ minWpm, minAccuracy, minSeconds })`.
- **Config:** `{ mode: 'letters' | 'words' | 'code' | 'shortcuts' | 'test'; layout: 'qwerty-uk' | 'qwerty-us'; durationS?: number; targetWpm: number; unlock?: { wpm: number; accuracy: number }; corpus?: 'english' | 'python'; os?: 'mac' | 'win' | 'linux' }`.
- **Correctness and layout:** correctness uses `event.key`; finger mapping uses `event.code`. The learner chooses UK or US layout, because detection works only in Chromium. On UK layouts @ and " swap places and £ is on Shift + 3.
- **Visual:**
  - Target text in Archivo at 22px: typed characters ink, untyped `--text-muted`, the current character underlined in `--manip`.
  - Errors get an amber underline and count towards the total, as a per-character verdict.
  - The keyboard is `--bg-sunken` keys with `--r-xs` corners. The next key gets a pear-200 wash and an ink ring, with its finger named in the caption.
  - Words per minute and accuracy use the stat token.
- **Motion:** none per keystroke, because latency matters. Statistics count up at the end of a session.
- **Reduced motion:** the end statistics appear without counting up.
- **Accessibility:** the current word is read aloud on request (Ctrl + Space) and after errors. The on-screen keyboard can be hidden.
  - **Honest limit:** the trainer is visual by design and is not a typing tutor for blind learners. Screen-reader users are pointed to dedicated tools.
- **Tutor:**
  - After the session only: "38 wpm, 94% accuracy. Slowest keys: b (40% slower than the mean), y. Most errors: ; for '."
  - Targets: `key-<code>`, `text`, `stats`.
- **Performance:** key-down to render in at most 2ms; timing from `event.timeStamp`; no layout reads; at most 120 characters rendered.
- **Artifact / web:** identical.
- **Generator:** yes. Pseudo-words from English letter frequencies, restricted to the unlocked letters; a corpus of Python snippets; shortcut prompts by OS.

### 10.2 `file-tree`: File tree

**Composite · P0 · W2.** Files and folders:

- a file system is a tree; folders hold files and folders;
- absolute paths from the root, and relative paths from the current folder with `.`, `..` and `~`;
- names and extensions (`.py`, `.csv`, `.txt`); hidden dot-files;
- moving, copying and renaming;
- organising a project folder (`data/`, `src/`, `notes/`), the layout every later project uses.

- **Serves:** 0.4 files and paths; 1.1 reading files; 1.2 Git.
- **Uses:** `token-tray` (drag into folders), the `vfs` service, and its own tree view.
- **Interactions.**
  - Pointer:
    - Expand and collapse folders. Drag an item into a folder to move it.
    - Copy with a long-press menu (Move, Copy, Rename, Delete) on any device, or Alt + drag on desktop.
    - New file and new folder buttons; rename in place.
    - Select a node to see its absolute path, and its path relative to the "you are here" pin. Drag that pin onto any folder.
    - In path-entry mode, type a path and the target highlights, or "No such file or directory" appears.
  - Keyboard: tree keys (Right expands, Left collapses). F2 renames. M moves: choose the destination with the arrows and press Enter. N makes a new folder; Delete deletes.
- **State:** `{ fs: Record<string, 'dir' | { content: string }>, cwd: string, selected?: string }`.
- **Answers:** `state` (predicate `fsMatches(spec)`), `text` (a path, compared after normalisation), `set` (a selected node).
- **Config:** `{ fs: Record<string, 'dir' | string>; cwd?: string; task: 'organise' | 'path-of' | 'find' | 'relative-path' | 'explore'; showHidden?: boolean; pathStyle: 'posix' | 'windows'; ops: ('move' | 'copy' | 'rename' | 'delete' | 'create')[] }`.
- **Path decision** [our choice]: paths are taught POSIX-style. One lesson shows the Windows form (backslashes and drive letters) and notes that Python accepts forward slashes on Windows too.
- **Visual:**
  - Rows are 44px tall, with 24px outline folder and file icons and an extension badge.
  - The selected row is `--manip-wash`. The "you are here" pin is a `--manip` marker, because it is movable.
  - Paths appear in the code token.
- **Motion:** expand and collapse over 150ms; a moved item slides with a 200ms FLIP.
- **Reduced motion:** instant.
- **Accessibility:** `role="tree"` with `aria-expanded`. Moves are announced: "Moved prices.csv into data".
- **Tutor:**
  - Describe: an indented tree of at most 40 lines, plus the current folder.
  - Targets: `node-<path>`, `pin`.
- **Performance:** at most 200 nodes.
- **Artifact / web:** identical.
- **Generator:** yes. Random project trees, with tasks: the relative path from A to B, sorting files by extension, finding a file.

### 10.3 `shell-sim`: Shell simulator

**Composite · P0 · W2.** The terminal:

- commands are programs that take arguments;
- the prompt and the current folder;
- navigating, creating, viewing, moving, copying and removing, including a safety lesson on `rm -r`;
- running Python scripts;
- tab completion and history;
- reading error messages.

1.2 extends it with pipes, `grep`, redirection, environment variables and a Git subset. That extension is P0, because 1.2 comes before 1.5.

- **Serves:** 0.4 the terminal; 1.2 the Linux command line and Git.
- **Uses:** `text-terminal`, the `vfs` service, `file-tree` (an optional mirror panel), the `python-runner` service.
- **Commands:**
  - 0.4: `pwd`, `ls` (with `-a` and `-l`), `cd`, `mkdir` (with `-p`), `touch`, `cat`, `head`, `echo`, `mv`, `cp` (with `-r`), `rm` (with `-r` and `-i`), `clear`, `history`, `python3` and `python`, `tree`, and `help`.
  - Added for 1.2: `grep`, `wc`, `sort`, `uniq`, `|`, `>`, `>>`, `less` (simulated), `which`, `export`, `env`, and a Git subset over the virtual file system (`init`, `status`, `add`, `commit`, `log`, `diff`, `branch`, `switch`, `merge`, `restore`).
- **Semantics:** a POSIX subset with deterministic output. Error messages match bash's wording: "bash: cd: nope: No such file or directory".
- **Interactions:** the `text-terminal` keys. The side tree updates live.
- **State:** `{ fs, cwd, history: string[], scrollback: string[], env: Record<string, string> }`.
- **Answers:** `state` (file-system and current-folder predicates), `text` (a typed command).
- **Grading by effect** [our choice]: a typed-command answer is run on a sandbox copy and judged by the resulting state and output. `cd ../data` and `cd ~/project/data` both pass when both reach the same folder.
- **Config:** `{ fs: Record<string, 'dir' | string>; cwd: string; commands: string[]; goal: { kind: 'fs' | 'cwd' | 'output'; spec: unknown }; tree?: boolean; python?: 'run' | 'simulate' | 'off' }`.
- **Windows decision** [our choice]: no PowerShell dialect. The setup lesson recommends Git Bash or WSL on Windows, and one lesson maps these commands to their PowerShell aliases. A second dialect would double the content.
- **Visual:** as `text-terminal`. On desktop the tree sits beside it; on mobile the tree is a toggle.
- **Motion:** none in the terminal. A node a command changed flashes `--manip-wash` for 300ms in the tree.
- **Reduced motion:** a changed node gets a dot instead of a flash.
- **Accessibility:** `role="log"`, commands echoed, tree changes announced.
- **Tutor:**
  - Describe: the current folder, the last 10 commands with their output, and a tree summary.
  - Targets: `input`, `line-<n>`, `node-<path>`.
- **Performance:** trivial.
- **Artifact / web:** identical, except `python3`. It runs real code where a runner exists (Pyodide on the web; MicroPython in the Artifact, if allowed). Otherwise it prints simulated output for authored scripts, with a note.
- **Generator:** yes. Navigation tasks over random trees; "find and move the file" puzzles.

### 10.4 `code-editor`: Code editor

**Composite · P0 · W2.** The code-exercise widget: `code-surface` plus:

- Run, against the visible examples, with a stdout console;
- Submit, against the hidden tests;
- a results list with the first failing test, its input and a diff of expected against actual.

It is the prototype drill, rebuilt as a reusable widget. Stage 0 uses it for first scripts (`print`, variables, `input`, arithmetic, f-strings, simple `if` and `for`). Every later code drill (1.1, 1.8) reuses it.

- **Serves:** 0.4; 1.1; 1.2 (pytest-style tests); 1.8.
- **Uses:** `code-surface`, `text-terminal` (console and interactive stdin), `data-table` (results), the `python-runner` service.
- **Interactions.**
  - Edit; Run (Ctrl or Cmd + Enter); Submit; Reset to the starter code.
  - `input()` prompts appear in the console and accept typed input during Run. Tests supply stdin themselves.
  - Keyboard: as `code-surface`.
- **State:** `{ code: string, lastRun?: { stdout: string; stderr: string; results: TestResult[] }, status: 'idle' | 'loading' | 'running' | 'done' }`.
- **Answers:** `code`.
- **Check:**
  - `{ kind: 'code', tests: CodeTest[], timeLimitMs: 5000 }`, with `CodeTest = { name; call?: string; stdin?: string; expectStdout?: string; expect?: string; compare: 'exact' | 'isclose' | 'fraction' | 'regex' | 'normalised-ws' }`.
  - Stdout comparison trims trailing whitespace on each line.
- **Config:** `{ starter: string; locked?: [number, number][]; examples: CodeTest[]; hidden: CodeTest[]; needs?: string[]; stdin: 'tests' | 'interactive'; brief: string }`.
  - `needs` lists packages. NumPy, for example, forces the web handoff in the Artifact.
- **Visual:** as the prototype drill: editor, brief, a results list with check and cross icons, and a diff view.
- **Motion:** the tangram loader in the button if loading the runtime takes over 400ms (design research section 4.8). Results reveal with an 80ms stagger.
- **Reduced motion:** no stagger.
- **Accessibility:** as the prototype. The summary is announced: "3 of 4 examples passed; first failure: test 2".
- **Tutor:**
  - Describe: the numbered code, the last results and the error.
  - Targets: `line-<n>`, `test-<k>`, `run`, `submit`.
- **Performance:**
  - The runtime runs in a worker with a 5s limit; on timeout it is terminated and restarted.
  - Pyodide is about 13 MB with a slow cold start, so it preloads on the lesson title screen.
  - MicroPython is about 0.6 MB.
- **Artifact / web:**
  - Web: Pyodide.
  - Artifact: MicroPython with ulab, if WebAssembly is allowed [unverified; the probe is running]. Otherwise a handoff to the web app with the code copied.
  - Stage 0 drills are pure Python, so all of them qualify for MicroPython.
  - MicroPython differs from CPython in places, including some format specifiers and some error messages. CI runs every Stage 0 drill's reference solution on both runtimes, and a drill that differs is tagged web-only.
- **Generator:** yes, for seeded test inputs. Problems are authored.

### 10.5 `workspace-sim`: Workspace simulator

**Composite · P0 · W2.** Rehearses the real workflow before the learner does it on their own machine. One virtual file system is shared by three panes: a folder tree, an editor with tabs and a terminal. The learner:

1. creates a project folder and `hello.py`;
2. writes code and saves it (a dot on the tab marks unsaved changes, which do not run);
3. runs `python3 hello.py` from the right folder. Running it from the wrong one gives "No such file or directory", the most common beginner error;
4. fixes it and runs again.

This is the in-app rehearsal of the Stage 0 exit item.

- **Serves:** 0.4 the editor workflow and the exit item; 1.1 projects; 1.2 Git workflow.
- **Uses:** `file-tree`, `code-editor` (with save semantics), `shell-sim`, the `vfs` service.
- **Interactions:** everything from the three child widgets, plus Ctrl or Cmd + S to save and F6 to cycle panes.
  - **Large screens:** tree on the left, editor on the right, terminal below.
  - **Mobile:** tabs (Files, Editor, Terminal).
- **State:** `{ fs, open: { path: string; buffer: string; saved: boolean }[], active: string, terminal: unknown }`.
- **Answers:** `state` (predicates `fileExists(path)`, `filePasses(path, tests)`, `ranFrom(cwd, cmd)`, `outputContains(text)`), `code`.
- **Config:** `{ fs: Record<string, 'dir' | string>; goals: { kind: string; args: unknown }[]; python: 'run' | 'simulate' }`.
- **Visual:** panes with `--r-md` borders; the unsaved dot is 8px ink on the tab; children as specified.
- **Motion:** none beyond the children.
- **Reduced motion:** as the children.
- **Accessibility:** a landmark for each pane; F6 cycles them; saves and runs are announced.
- **Tutor:**
  - Describe, within 2 KB: a tree summary, the active file with line numbers, the last 10 terminal lines and the unsaved files.
  - Targets: child ids prefixed `tree:`, `editor:` and `term:`.
- **Performance:** as the children.
- **Artifact / web:** as `code-editor`.
- **Generator:** no. Scenarios are authored; seeds vary file names and values.

### 10.6 `setup-checklist`: Setup checklist

**Composite · P0 · W2.** Guides real installs on the learner's own computer (Python, an editor, terminal basics) and verifies the outcomes without any access to that machine.

- **Steps** are specific to each OS: Windows, macOS and Linux, chosen once and remembered.
- **Verification by paste:**
  - `python3 --version` is parsed and checked against Python 3.11 or later [our choice];
  - `which python3` (or `where python`) is checked.
- **A screenshot** can optionally go to the tutor for diagnosis, where the transport supports images.
- **The Stage 0 exit item:**
  1. The app issues a seeded task, such as "Write a script that prints the sum of the whole numbers from 1 to 4,817". Only a working local Python run produces the output easily.
  2. The learner pastes the script and its terminal output.
  3. The widget checks the output value.
  4. Where an in-app runner exists, it re-runs the pasted script and compares the outputs.

- **Serves:** 0.4 installation; the Stage 0 exit item; 1.2 Git and tool installs.
- **Uses:** `code-surface` (read-only display of the pasted script), `numeric-entry` and plain text fields (pastes), the `python-runner` service, the tutor hooks.
- **Interactions.**
  - Pointer: choose the OS; expand a step; mark it done; paste output; press Verify. "I'm stuck" sends the pasted error to the tutor.
  - Keyboard: standard controls.
- **State:** `{ os: 'win' | 'mac' | 'linux', steps: Record<string, 'todo' | 'done' | 'verified' | 'failed'>, pastes: Record<string, string> }`.
- **Answers:** `state` (all required steps verified), `text`, `code`.
- **Check:**
  - Per step: `{ kind: 'predicate', name: 'pasteMatches', args: { pattern } }`, for example the pattern `Python 3\.(1[1-9]|[2-9]\d)\.\d+`.
  - Exit task: `{ kind: 'predicate', name: 'outputEquals', args: { value } }`.
- **Config:** `{ steps: { id: string; title: string; os: ('win' | 'mac' | 'linux')[]; body: string; verify?: { command: string; pattern: string; hint: string } }[]; exitTask?: { template: 'sum-to-n' | 'count-words' | 'fizzbuzz-count'; seed: number } }`.
- **Privacy** (engineering floor, data protection): before any paste goes to the tutor, home paths are redacted. `/Users/<name>`, `/home/<name>` and `C:\Users\<name>` become `~`.
- **Visual:**
  - A vertical checklist with status icons (check, cross, clock) and an OS segmented control.
  - Pastes appear in the code token on `--bg-sunken`.
  - A verified step's status chip uses the correct style: green check plus "Verified". Only that chip is recoloured.
- **Motion:** the status chip changes over 150ms.
- **Reduced motion:** instant.
- **Accessibility:** list semantics; statuses as text.
- **Tutor:**
  - Describe: the OS, each step's status, and the last pasted error (redacted, at most 1 KB).
  - Targets: `step-<id>`, `paste-<id>`, `verify-<id>`.
- **Performance:** trivial.
- **Artifact / web:** identical. Screenshots go to the tutor only where `sample.limits()` reports images, or where the proxy accepts them.
- **Honest limit:** verification by paste proves the work, it does not proctor it. A learner could compute the sum by hand. That is acceptable, because the learner is the only person relying on the result.
- **Generator:** yes, for the exit-task seeds and values.

---

## 11. Composites: Mental arithmetic (0.5)

### 11.1 `speed-drill`: Speed drill

**Composite · P0 · W1.** Timed arithmetic in the Zetamac format and its variants.

**Zetamac format:**

- a 120-second sprint of addition, subtraction, multiplication and division [sourced: quantvault.org comparison page];
- default ranges [recalled from arithmetic.zetamac.com; not re-checked, because the site was blocked from here]:
  - addition: 2 to 100 plus 2 to 100;
  - subtraction: additions in reverse;
  - multiplication: 2 to 12 times 2 to 100;
  - division: multiplications in reverse.
- the ranges are configuration, so a correction costs no code.
- a correct answer is accepted the moment it is typed, with no Enter. A wrong answer just sits there until it is corrected.
- the score is the number of correct answers.

**80-in-8 format:** 80 mixed questions in 8 minutes, including decimals, fractions and percentages (the format the curriculum names for some firms). Here Enter submits and Skip is allowed, because wrong answers count.

**Decks:** fractions to decimals, squares, percentages, and estimation (graded within a tolerance).

**Chain mode:** a running total held in your head through several operations.

**Latency logging:** the time taken on each fact feeds `times-table-grid` and `strategy-trainer`.

- **Serves:** 0.5 (daily from week 1); the Stage 0 exit test (Zetamac 25 or more); 3.3 (Zetamac 50 or more, and 80-in-8).
- **Uses:** `keypad` (speed layout), `speed-timer`, `numeric-entry` (auto-accept), `data-table`, the `seeded-rng` service.
- **Interactions.**
  - Type on physical keys, or press the keypad, which fires on `pointerdown`.
  - Escape quits, and the score is void.
  - Keyboard first.
- **State:** `{ format, seed, startedAt, items: { q: string; a: string; entered: string; correct: boolean; ms: number }[], score: number, interrupted: boolean }`.
- **Answers:** `state`, graded by predicate `score({ min })`. The exit test uses `{ format: 'zetamac', min: 25 }`.
- **Config:** `{ format: 'zetamac' | 'eighty-in-eight' | 'deck' | 'chain'; ranges?: { add: [[number, number], [number, number]]; mul: [[number, number], [number, number]] }; ops?: ('add' | 'sub' | 'mul' | 'div')[]; durationS: number; deck?: 'fractions-decimals' | 'squares' | 'percent' | 'estimation'; target?: number; adaptive?: boolean }`.
- **Visual:**
  - The question is centred in the stat token (48px on desktop), with a large answer field below.
  - The timer ring, top right, is in the interview track gold. The score is top left.
  - There are no per-item flashes, because speed matters: the next question simply appears.
  - The end screen shows the score, a breakdown by operation and the slowest facts.
- **Motion:** questions change instantly. The end score counts up over 700ms.
- **Reduced motion:** the end score appears.
- **Accessibility:** each new question goes to the polite live region. Time warnings come at 30 and 10 seconds. An untimed mode exists for learners for whom timing is a barrier; it never counts towards the exit test, and says so.
- **Tutor:** after the session only; the tutor is off during a timed run.
  - Describe: "Score 27: add 11, sub 7, mul 6, div 3. Slowest: 7 × 8 (4.1 s), 96 − 39 (5.2 s)."
  - Targets: `score`, `slow-<k>`, `op-<name>`.
- **Performance:**
  - A correct key press shows the next question within 16ms.
  - 300 questions are generated from the seed at the start.
  - Timing comes from `event.timeStamp`.
  - A hidden tab voids the run.
- **Artifact / web:** identical.
- **Generator:** yes, central. The Zetamac distribution exactly as configured; families for 80-in-8; the decks.

### 11.2 `strategy-trainer`: Strategy trainer

**Composite · P0 · W1.** Teaches the mental strategies behind fast arithmetic, then drills each one. Strategies:

- partitioning with the area model: $47 \times 6 = 240 + 42$;
- compensation: $99 \times 7 = 700 - 7$, and $398 + 247 = 400 + 247 - 2$;
- difference of two squares: $23 \times 17 = 20^2 - 3^2$;
- squaring near a round number: $48^2 = 50^2 - 2 \cdot 50 \cdot 2 + 2^2$;
- doubling and halving: $16 \times 25 = 4 \times 100$;
- multiplying by 5 as ×10 then ÷2; the ×11 pattern;
- swapping percentages: $8\%$ of $25$ is $25\%$ of $8$;
- fraction-to-decimal anchors: sevenths, eighths, ninths, twelfths;
- subtraction by counting up;
- division through factor pairs;
- estimating by rounding, then correcting.

**Phases:**

1. Learn: the strategy is shown once, visually.
2. Practise: items where that strategy is the fastest.
3. Mixed: the learner chooses the strategy.

- **Serves:** 0.5; it supports `speed-drill` and the 3.3 interview formats.
- **Uses:** `area-model`, `number-line` (counting up, compensation jumps), `speed-timer`, `numeric-entry` (auto-accept), `choice-cards` ("which split is fastest?"), the `seeded-rng` service.
- **Interactions.**
  - Learn phase: "Show your split". Drag the split handle on the area model, or the jumps on the number line, then enter the partial results and the answer.
  - Practise phase: timed sets of 10.
  - Keyboard: as the primitives.
- **State:** `{ strategy, phase: 'learn' | 'practise' | 'mixed', items: { q, entered, ms, split? }[] }`.
- **Answers:** `numeric`, `state` (the split chosen), `choice`.
- **Config:** `{ strategy: string; phase: 'learn' | 'practise' | 'mixed'; n: number; timed?: boolean; show?: 'area' | 'jumps' | 'none' }`.
- **Visual:** as `area-model` and `number-line`. In the learn phase the timer is a quiet elapsed time, not a ring.
- **Motion:** as the primitives.
- **Reduced motion:** as the primitives.
- **Accessibility:** as the primitives.
- **Tutor:**
  - Describe: "Strategy: compensation. Item 99 × 7. Split: 100 × 7 − 1 × 7. Entered: 693."
  - Targets: `split`, `partial-<k>`, `answer`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Items aimed at each strategy; compensation items, for instance, always have a factor within 2 of a round number.

### 11.3 `times-table-grid`: Times-table grid

**Composite · P0 · W1.** The multiplication facts to 12 × 12 as a map:

- commutativity halves the facts to learn (fold the grid along its diagonal);
- squares lie on the diagonal;
- patterns: ×9 digit sums, ×5, ×11;
- a personal heat map of speed and accuracy for each fact, from `speed-drill` data;
- tap a region, such as the 7s and 8s, to drill exactly those facts.

- **Serves:** 0.5 times tables.
- **Uses:** `region-selector` (grid, paint), `data-table` (table view), the sequential colour ramp.
- **Interactions.**
  - Pointer: paint cells to choose facts for a drill; switch between facts, heat and pattern views; fold the grid (show-why for commutativity).
  - Keyboard: grid navigation; Space selects; D starts the drill.
- **State:** `{ selected: string[], view: 'facts' | 'heat' | 'patterns' }`.
- **Answers:** `set` (for example "select every fact equal to 24"), `numeric`.
- **Config:** `{ size: 12 | 20; view: 'facts' | 'heat' | 'patterns'; data?: Record<string, { ms: number; accuracy: number }>; task?: 'find-products' | 'drill-select' | 'explore' }`.
- **Visual:**
  - Cells are 26 to 40px. On screens under 480px, products show on tap rather than in every cell, so the caption size never drops below 13px.
  - The heat map uses the sequential blue ramp (#CDE2FB to #0D366B) with a legend. Exact times are in the table view.
  - The diagonal is outlined.
- **Motion:** the fold show-why rotates the lower triangle about the diagonal over 800ms.
- **Reduced motion:** before-and-after.
- **Accessibility:** a grid with cells such as "7 times 8 is 56; average 2.3 seconds", and a table view.
- **Tutor:**
  - Describe: "Slowest facts: 7 × 8 (2.9 s), 6 × 7 (2.6 s), 8 × 12 (2.4 s). Selected: none."
  - Targets: `cell-<r>-<c>`, `row-<r>`, `diagonal`.
- **Performance:** 144 DOM cells.
- **Artifact / web:** identical.
- **Generator:** yes. Drill items from the selected facts; "find the products" targets.

---

## 12. Generators

Practice, review, homework and exams need many instances of each item, and every instance must be solvable and unambiguous. Brilliant's own evaluation found AI-generated puzzles that could not be solved (design research section 10). Our generators are therefore code, never model output.

### 12.1 Contract

```ts
interface Generator<C> {
  id: string;                         // '<widget>/<family>', e.g. 'balance-scale/both-sides'
  widget: string;
  difficulty: [1 | 2 | 3 | 4 | 5, 1 | 2 | 3 | 4 | 5];   // supported range (design research section 8.4)
  generate(rng: () => number, d: 1 | 2 | 3 | 4 | 5, params?: unknown): GeneratedItem<C>;
  solve(item: GeneratedItem<C>): unknown;               // an independent solver, used by CI
}
interface GeneratedItem<C> {
  seed: string;                       // template id plus seed, stored with every attempt
  config: C;                          // the widget configuration
  prompt: string;                     // question line, at most 60 words, $...$ allowed
  check: Check;
  solution: unknown;                  // the state or answer used by reveal()
  misconceptions: { when: Check; id: string; line: string; showWhy?: { key: string; params?: unknown } }[];
  tags: string[];                     // skill ids for mastery tracking
}
```

### 12.2 Rules

- **Pure and deterministic.** The same seed always gives the same item. The generator takes `rng` and nothing else: no clock and no global state.
- **Seed policy** [our choice]:

  | Context | Seeds |
  |---|---|
  | Redo queue (7 and 30 days) | The same seed, because the curriculum says to redo the same problem |
  | Practice and level review | Fresh seeds |
  | Homework | Fixed per learner and level, so a returning learner finds the same set |
  | Exams | Fixed per sitting, and recorded |

- **Tidy numbers.** Each family declares bounds, for example:
  - whole-number intermediate results in non-calculator items;
  - denominators from an allowed set;
  - coordinates on the visible grid;
  - no zero or one coefficients unless the family is about them.
- **Distinct distractors.** Each family produces its distractors from named misconceptions, not at random. Every distractor must differ from the answer and from the other distractors.
- **CI test for every family:** 1,000 seeds at each supported difficulty. Each instance must:
  1. pass its own check with its `solution`;
  2. fail its check with every distractor;
  3. agree with an independent solver, which is brute force where the space allows (counting, small equations) and `cas` elsewhere;
  4. stay within its tidy-number bounds;
  5. regenerate identically from its seed;
  6. render without overflow at 360px wide (a headless layout snapshot on a sample of 20 seeds).
- **Rotation.** Each family has at least 4 surface variants (contexts, names, units), so practice does not repeat surface features.

### 12.3 Generator families by widget

| Widget | Families (examples) | Key constraints |
|---|---|---|
| `number-line` | place a fraction or decimal; round and give the error interval; order values; probability scale | denominators 2 to 12; at most 3 decimal places; tolerance of half a minor tick |
| `derivation` | recurring decimal to fraction; quadratic formula for given coefficients; log-law steps | cycle length 1 to 3; whole-number coefficients |
| `place-value-chart` | build, regroup, shift by powers of 10, convert between bases | zeros in middle columns at difficulty 2 and above; base 2 values below 256 |
| `bar-model` | compare fractions; share in a ratio; percentage and reverse percentage; before-and-after problems | whole-number unit values; totals of 1,000 or less |
| `area-model` | two-digit by two-digit; fraction by fraction; arrays for factors; root brackets | chosen carries; $n \le 144$ for arrays |
| `double-number-line` | percentage of an amount; reverse percentage; unit conversion; best buy | tidy multipliers (1.05, 0.8, 1.2, ...); currency to 2 decimal places |
| `factor-tree` | factorise; HCF and LCM; square and cube tests; surds | $n \le 1000$; 3 to 6 prime factors |
| `venn-diagram` | sort by properties; survey counts; probability from a Venn diagram | totals consistent; no empty region unless intended |
| `expression-tree` | evaluate; order-of-operations traps; substitute; rearrange | whole-number intermediate results; depth 4 or less |
| `written-method` | column add and subtract; long multiplication; long division with a chosen cycle; polynomial division | chosen carries; cycle lengths from 1 to 6; whole-number polynomial coefficients |
| `multiplier-chain` | successive changes; compound interest; reverse; compounding towards $e$ | multipliers with at most 2 decimal places; final amounts in pence |
| `unit-chain` | speed, density, pressure; area and volume units; data sizes | exact rationals; at most 3 cards |
| `bounds-explorer` | bounds of sums, differences, products and quotients; speed from rounded values | accuracy from {nearest whole, 1 dp, 2 sf} |
| `modular-clock` | last digit of $a^n$; day of the week; remainders | $n \le 10^4$; cycle detection proved |
| `balance-scale` | one-step, two-step, both sides; inequalities | positive whole-number solutions; at most 24 tokens |
| `algebra-tiles` | collect; expand; factorise; complete the square; signed counters | roots in −6 to 6; $\lvert a \rvert \le 3$ |
| `function-machine` | evaluate; inverse; hidden rule; compose | whole-number outputs; hidden rules linear or quadratic |
| `equation-workbench` | linear (brackets, fractions), quadratic, rearranging, log and exponential, identities | solutions rational with denominator 12 or less; formula bank of 60 or more |
| `equation-stack` | 2 × 2 systems; 3 × 3; parallel and coincident; linear-quadratic | whole-number solutions; coefficients up to 12 |
| `graph-explorer` | lines through lattice points; quadratic features; transformations; tangent gradients; rational asymptotes | features on grid points; asymptotes at whole numbers |
| `curve-sketch` | polynomials by roots and multiplicities; rational and trigonometric sketches | roots at least 1 unit apart; turning points inside the view |
| `inequality-regions` | shade a region; find the inequalities; integer points; optimise | bounded region with 3 to 12 integer points |
| `sign-chart` | quadratic, cubic and rational inequalities | whole-number critical points, at least 1 apart |
| `iteration-cobweb` | iterate to $n$ dp; converge or diverge | the chosen rearrangement has $\lvert g'(x^*) \rvert < 0.8$ |
| `geometry-board` | Pythagoras; trigonometric ratios; sine and cosine rules; ambiguous case; angle chase; transformations; bearings | Pythagorean triples or tidy trigonometric values; angles in whole degrees |
| `solid-viewer` | volume, surface area, 3D Pythagoras, similar solids, plans and elevations | dimensions up to 20; $\pi$ answers exact or to 1 dp |
| `dot-plot-stats` | compute statistics; constraint puzzles; effect of an outlier | whole-number mean and median at difficulty 2 or below |
| `stat-chart` | build or read each chart type; histogram areas; cumulative frequency quartiles | totals consistent; densities with at most 1 decimal place |
| `scatter-fit` | fit; predict; classify; linearise | seeded noise; $\lvert r \rvert$ between 0.6 and 0.98 for "fit" families |
| `outcome-grid` | events on dice, coins, spinners, cards; conditional probability | fractions in lowest terms checked |
| `tree-diagram` | with and without replacement; two-stage events; counting trees | bag sizes up to 12; at most 16 leaves |
| `slide-rule` | multiply; divide; powers | products landing on readable ticks |
| `unit-circle` | exact values; solve $\sin\theta = k$ in a range; convert degrees and radians | special angles only at difficulty 3 or below |
| `circle-to-wave` | match a wave; read amplitude and period; phasor sums | $R$ and $\alpha$ tidy |
| `sequence-lab` | next terms; nth term (linear, quadratic, geometric); recurrences | whole-number terms; ratios from {2, 3, 1/2, −2} |
| `sum-visualiser` | arithmetic and geometric sums; sum to infinity; present value | $\lvert r \rvert < 1$ for convergent families |
| `pascal-triangle` | missing entries; coefficients; path counts | rows up to 16 |
| `binomial-expander` | specific coefficients; full expansions; approximations | $n \le 10$; sign traps at difficulty 3 and above |
| `counting-slots` | permutations; combinations; restrictions; repeated letters; circular; stars and bars | every answer verified by enumeration (search space up to $10^6$) |
| `vector-plane` | lattice paths; magnitude; angle; dot product; ratio division | whole-number components |
| `matrix-grid` | products; determinant; inverse; solve | inverse entries with denominators dividing the determinant, at most 12 |
| `linear-map` | find the matrix; determinant as area; compositions | whole-number matrices |
| `complex-plane` | arithmetic; modulus and argument; roots of quadratics; roots of unity | whole-number parts; standard arguments |
| `typing-trainer` | pseudo-words from unlocked letters; Python snippets; shortcut prompts | letter frequencies from an English corpus |
| `file-tree` | relative paths; organise by extension; find a file | depth 4 or less; 25 nodes or fewer |
| `shell-sim` | navigate and create; move and copy; find a file | goals reachable in 8 commands or fewer |
| `code-editor` | seeded test inputs for authored problems | values fit the problem's stated bounds |
| `setup-checklist` | exit-task values (sum to $n$, word counts) | $n$ from 1,000 to 9,999 |
| `speed-drill` | Zetamac; 80-in-8; decks; chains | exactly the configured ranges |
| `strategy-trainer` | items aimed at each strategy | each item's best strategy is the target one |
| `times-table-grid` | drills from selected facts; "find the products" | facts up to 12 × 12, or 20 × 20 |

**Totals.** 51 widgets have item generators. Four more use seeds only to vary authored items: `trial-simulator`, `induction-chain`, `fermi-estimator` and `workspace-sim`.

---

## 13. Build order inside P0

The waves follow the depth-first lesson order. 0.4 and 0.5 run alongside from the first week, as the curriculum says, so their first widgets sit in W1.

| Wave | Needed by | Widgets |
|---|---|---|
| W0 | every lesson | `plot-axes`, `number-line`, `curve-layer`, `geo-layer`, `bar-layer`, `draggable-point`, `slider`, `region-selector`, `token-tray`, `stepper`, `tex-terms`, `data-table`, `keypad`, `speed-timer`, `choice-cards`, `numeric-entry`, `card-sort`, `derivation`, `free-response`; services `seeded-rng`, `num-parse`, `unit-algebra`, `announce`, `motion` |
| W1 | 0.1 Number, 0.5 from week 1, typing from week 1 | `place-value-chart`, `bar-model`, `area-model`, `double-number-line`, `factor-tree`, `venn-diagram`, `expression-tree`, `written-method`, `multiplier-chain`, `unit-chain`, `bounds-explorer`, `modular-clock`, `fermi-estimator`, `algebra-tiles` (counters preset), `expression-entry` and the `cas` service (for surds and index laws late in 0.1), `equation-workbench` (rationalising only), `speed-drill`, `strategy-trainer`, `times-table-grid`, `typing-trainer` |
| W2 | 0.2 Algebra, 0.4 files to editor | `balance-scale`, `algebra-tiles` (full), `function-machine`, `equation-workbench` (full), `equation-stack`, `graph-explorer`, `curve-sketch`, `inequality-regions`, `sign-chart`, `iteration-cobweb`, `code-surface`, `text-terminal`, `file-tree`, `shell-sim`, `code-editor`, `workspace-sim`, `setup-checklist`; services `vfs`, `python-runner` |
| W3 | Geometry and statistics (pending the owner's placement decision), 0.3 Precalculus | `view-3d`, `geometry-board`, `solid-viewer`, `dot-plot-stats`, `stat-chart`, `scatter-fit`, `outcome-grid`, `tree-diagram`, `trial-simulator`, `slide-rule`, `unit-circle`, `circle-to-wave`, `sequence-lab`, `sum-visualiser`, `induction-chain`, `pascal-triangle`, `binomial-expander`, `counting-slots`, `vector-plane`, `matrix-grid`, `linear-map`, `complex-plane` |

**Gate per widget.** A widget is done when all of these hold:

- its schema validates every example configuration in this file;
- every state round-trips through `getState` and `setState`;
- keyboard and two-tap paths reach every action;
- reduced-motion mode is checked;
- `describe` is snapshot-tested;
- frame budgets hold on the reference device;
- its generators pass CI.

---

## 14. All widgets

Kinds: **primitive** (a building block, also usable alone), **input** (a general answer widget), **composite** (assembled from primitives). Every widget is P0; the "Later" column notes the curriculum items that reuse or extend it.

| # | Id | Kind | Priority | Wave | Stage 0 items | Later |
|---|---|---|---|---|---|---|
| 1 | `plot-axes` | primitive | P0 | W0 | 0.1, 0.2, 0.3, GCSE geometry and statistics | 1.1 to 3 |
| 2 | `number-line` | primitive | P0 | W0 | 0.1, 0.2, 0.3, 0.5 | 1.5, 1.6 |
| 3 | `curve-layer` | primitive | P0 | W0 | 0.1, 0.2, 0.3 | 1.3, 1.5, 1.7, 2.x |
| 4 | `geo-layer` | primitive | P0 | W0 | 0.1, 0.2, 0.3, GCSE geometry | 1.4 |
| 5 | `bar-layer` | primitive | P0 | W0 | 0.1, 0.3, GCSE statistics | 1.1, 1.5, 1.6 |
| 6 | `draggable-point` | primitive | P0 | W0 | 0.1, 0.2, 0.3, GCSE | all |
| 7 | `slider` | primitive | P0 | W0 | 0.1, 0.2, 0.3 | all |
| 8 | `region-selector` | primitive | P0 | W0 | 0.1, 0.2, 0.3, 0.5, GCSE | 1.5 |
| 9 | `token-tray` | primitive | P0 | W0 | 0.1, 0.2, 0.3, 0.4 | 1.2, 1.8 |
| 10 | `stepper` | primitive | P0 | W0 | 0.1, 0.2, 0.3 | 1.3 to 1.8 |
| 11 | `tex-terms` | primitive | P0 | W0 | 0.1, 0.2, 0.3 | all maths |
| 12 | `data-table` | primitive | P0 | W0 | all of Stage 0 | 1.1, 1.6 |
| 13 | `keypad` | primitive | P0 | W0 | 0.1 to 0.3, 0.5 | exams |
| 14 | `speed-timer` | primitive | P0 | W0 | 0.4, 0.5 | 3.3, exams |
| 15 | `view-3d` | primitive | P0 | W3 | GCSE geometry, 0.3 | 1.3 (P1 surfaces), 1.4 |
| 16 | `code-surface` | primitive | P0 | W2 | 0.4 | 1.1, 1.2, 1.8, 1.9 |
| 17 | `text-terminal` | primitive | P0 | W2 | 0.4 | 1.1, 1.2 |
| 18 | `choice-cards` | input | P0 | W0 | all | all |
| 19 | `numeric-entry` | input | P0 | W0 | all | all |
| 20 | `expression-entry` | input | P0 | W1 | 0.1, 0.2, 0.3 | 1.3 to 1.6 |
| 21 | `card-sort` | input | P0 | W0 | all | all |
| 22 | `derivation` | input | P0 | W0 | 0.1, 0.2, 0.3 | 1.3 to 1.7 |
| 23 | `free-response` | input | P0 | W0 | 0.1, 0.2, 0.3 | all homework |
| 24 | `place-value-chart` | composite | P0 | W1 | 0.1, 0.4, 0.5 | 1.1 (binary) |
| 25 | `bar-model` | composite | P0 | W1 | 0.1, 0.2, 0.5 | none |
| 26 | `area-model` | composite | P0 | W1 | 0.1, 0.2, 0.5, GCSE | 1.5 |
| 27 | `double-number-line` | composite | P0 | W1 | 0.1, 0.2, GCSE | none |
| 28 | `factor-tree` | composite | P0 | W1 | 0.1, 0.2 | none |
| 29 | `venn-diagram` | composite | P0 | W1 | 0.1, 0.3, GCSE | 1.5 |
| 30 | `expression-tree` | composite | P0 | W1 | 0.1, 0.2, 0.4 | 1.1 |
| 31 | `written-method` | composite | P0 | W1 | 0.1, 0.2, 0.3 | none |
| 32 | `multiplier-chain` | composite | P0 | W1 | 0.1, 0.2, 0.3 | 1.7 |
| 33 | `unit-chain` | composite | P0 | W1 | 0.1, 0.4, GCSE | 1.7 |
| 34 | `bounds-explorer` | composite | P0 | W1 | 0.1 | 1.6 |
| 35 | `modular-clock` | composite | P0 | W1 | 0.1 | 1.8, 3.3 |
| 36 | `fermi-estimator` | composite | P0 | W1 | 0.1, 0.5 | 3.3 |
| 37 | `balance-scale` | composite | P0 | W2 | 0.1, 0.2 | none |
| 38 | `algebra-tiles` | composite | P0 | W1, W2 | 0.1, 0.2 | none |
| 39 | `function-machine` | composite | P0 | W2 | 0.2, 0.3, 0.4 | 1.1 |
| 40 | `equation-workbench` | composite | P0 | W1, W2 | 0.1, 0.2, 0.3 | 1.3 |
| 41 | `equation-stack` | composite | P0 | W2 | 0.2, 0.3 | 1.4 |
| 42 | `graph-explorer` | composite | P0 | W2 | 0.1, 0.2, 0.3 | 1.3, 1.5, 1.7 |
| 43 | `curve-sketch` | composite | P0 | W2 | 0.2, 0.3 | 1.3, 1.5, 1.7 |
| 44 | `inequality-regions` | composite | P0 | W2 | 0.2 | 2.x |
| 45 | `sign-chart` | composite | P0 | W2 | 0.2, 0.3 | 1.3 |
| 46 | `iteration-cobweb` | composite | P0 | W2 | 0.2, 0.3 | 1.3, 1.5 |
| 47 | `geometry-board` | composite | P0 | W3 | GCSE geometry, 0.3 | none |
| 48 | `solid-viewer` | composite | P0 | W3 | GCSE geometry | 1.3, 1.4 |
| 49 | `dot-plot-stats` | composite | P0 | W3 | GCSE statistics | 1.1, 1.6 |
| 50 | `stat-chart` | composite | P0 | W3 | GCSE statistics | 1.1, 1.5 |
| 51 | `scatter-fit` | composite | P0 | W3 | GCSE statistics, 0.3 | 1.4; 1.6 (P1) |
| 52 | `outcome-grid` | composite | P0 | W3 | GCSE probability, 0.3 | 1.5 |
| 53 | `tree-diagram` | composite | P0 | W3 | GCSE probability, 0.3 | 1.5 |
| 54 | `trial-simulator` | composite | P0 | W3 | GCSE probability, 0.3 | 1.5 |
| 55 | `slide-rule` | composite | P0 | W3 | 0.3, 0.1 | 1.7 |
| 56 | `unit-circle` | composite | P0 | W3 | 0.3, GCSE | 1.4 |
| 57 | `circle-to-wave` | composite | P0 | W3 | 0.3 | P2 Fourier |
| 58 | `sequence-lab` | composite | P0 | W3 | 0.3, GCSE | 1.5, 1.8 |
| 59 | `sum-visualiser` | composite | P0 | W3 | 0.3 | 1.5, 1.7 |
| 60 | `induction-chain` | composite | P0 | W3 | 0.3 | 1.8 |
| 61 | `pascal-triangle` | composite | P0 | W3 | 0.3 | 1.5 |
| 62 | `binomial-expander` | composite | P0 | W3 | 0.3 | 1.5 |
| 63 | `counting-slots` | composite | P0 | W3 | 0.3, GCSE | 1.5 |
| 64 | `vector-plane` | composite | P0 | W3 | 0.3, GCSE | 1.4 |
| 65 | `matrix-grid` | composite | P0 | W3 | 0.3 | 1.4 |
| 66 | `linear-map` | composite | P0 | W3 | 0.3 | 1.4 |
| 67 | `complex-plane` | composite | P0 | W3 | 0.3 | 1.4, P2 |
| 68 | `typing-trainer` | composite | P0 | W1 | 0.4 | none |
| 69 | `file-tree` | composite | P0 | W2 | 0.4 | 1.1, 1.2 |
| 70 | `shell-sim` | composite | P0 | W2 | 0.4 | 1.2 |
| 71 | `code-editor` | composite | P0 | W2 | 0.4 | 1.1, 1.2, 1.8 |
| 72 | `workspace-sim` | composite | P0 | W2 | 0.4 (exit item) | 1.1, 1.2 |
| 73 | `setup-checklist` | composite | P0 | W2 | 0.4 (exit item) | 1.2 |
| 74 | `speed-drill` | composite | P0 | W1 | 0.5 (exit test) | 3.3 |
| 75 | `strategy-trainer` | composite | P0 | W1 | 0.5 | 3.3 |
| 76 | `times-table-grid` | composite | P0 | W1 | 0.5 | none |

**Counts:** 17 primitives, 6 inputs, 53 composites; 76 in all.

**Features inside P0 widgets that are later priorities:**

| Feature | Priority |
|---|---|
| `view-3d` surfaces $z = f(x, y)$ | P1 (for 1.3, which is P0, unless the 1.3 cluster decides otherwise) |
| `scatter-fit` $R^2$ and residual plots | P1 (1.6) |
| `data-table` virtualisation | P1 |
| `code-surface` replaced by CodeMirror 6, if 1.8 needs it | P1 |
| `circle-to-wave` Fourier sums | P2 |
| `inequality-regions` full linear programming | P2 |

---

## 15. Primitives other clusters will need

Other clusters (Stage 1 maths, probability, Python and tools, finance, ML) should build on these rather than make their own.

| Primitive or service | Why other clusters need it |
|---|---|
| `plot-axes`, `curve-layer`, `draggable-point`, `slider` | Every graph in calculus, probability (PDFs, CDFs), statistics, finance (payoffs, yield curves) and ML (loss curves, decision boundaries) |
| `bar-layer` | Distributions, histograms of simulations, backtest returns |
| `geo-layer` | Linear algebra diagrams, tree and graph structures in 1.8, order-book ladders in 1.7 |
| `region-selector` | Sample spaces, joint distribution tables, confusion matrices |
| `token-tray` | Algorithm traces (sorting, stacks, queues), card sorts, order-book order entry |
| `stepper` | Every algorithm animation in 1.8, every worked derivation, binomial-tree pricing in 1.7 |
| `tex-terms` | Every live equation |
| `data-table` | The table view everywhere; the data frames of 1.1; regression output in 1.6 |
| `view-3d` | 1.3 surfaces and gradients, 1.4 planes and eigenvectors, the 2.x volatility surface |
| `code-surface`, `text-terminal`, `python-runner`, `vfs` | 1.1, 1.2, 1.8 and 1.9 drills; Git and the command line |
| `keypad`, `speed-timer` | Exams; 3.3 interview drills; market-making games |
| `seeded-rng`, `cas`, `num-parse`, `unit-algebra` | Generators and checking in every cluster |
| `trial-simulator` (as a composite) | Law of large numbers, central limit theorem, random walks, Monte Carlo pricing (1.7, P1), bootstrap (1.6, P1) |
| `graph-explorer`, `curve-sketch` (as composites) | 1.3 derivatives and integrals, 1.5 distributions, 1.7 payoff diagrams |

### 15.1 Reconciliation with the calculus and linear algebra catalogue

`widgets-calc-linalg.md` appeared in this folder while this file was being written. It specifies the same primitives under other names, and claims some Stage 0 topics. One id per concept keeps the engine small. Recommendations follow; the merge owner decides.

**Rule** [our choice]: where two specs describe the same thing, keep one id and merge both requirement lists into it. For primitives and inputs we recommend the calculus and linear algebra names. They are shorter, already consistent with one another (`plot-2d` and `plot-3d`, the `*-input` family), and nothing has been built yet, so renaming is free.

| This catalogue | Calculus and linear algebra | Relation | Recommendation |
|---|---|---|---|
| `plot-axes` | `plot-2d` | same concept | Use `plot-2d`. Add skewed lattice grids, π ticks and log axes from 3.1 |
| `view-3d` | `plot-3d` | same concept | Use `plot-3d`. Add view buttons (plan and elevations), hidden-edge dashes and face selection from 3.15 |
| `curve-layer`, `geo-layer`, `bar-layer` | `marks` | one family against three layers | Use `marks`. Add the construction-graph constructors (3.4), the bar, bin, dot-plot and box types (3.5), and angle and equal-length marks |
| `draggable-point` | `drag-point` | same | Use `drag-point`. Keep the constraint list in 3.6 and the two-tap path |
| `region-selector` | `region-select` | same | Use `region-select`. Add paint mode and the half-plane mode |
| `data-table` | `value-table` | same, since `value-table` already edits and serves as the table view | Use `value-table`. Add sorting and per-cell checks |
| `tex-terms` | `live-formula` | same | Use `live-formula`. Keep fixed-width slots and the no-KaTeX-in-the-drag-loop rule |
| `choice-cards`, `numeric-entry`, `expression-entry` | `choice`, `numeric-input`, `expression-input` | same | Use their names. Keep the parse preview, form policy and ASCII fallback from 4.2 and 4.3 |
| `derivation` | `derivation-steps` | same | Use `derivation-steps`. Add `step` and `predict` modes if they are missing |
| `code-editor` (with `code-surface`) | `code-cell` (owned by the programming cluster) | same job | One widget. `code-surface` stays as its internal editing surface |
| `curve-sketch` | `sketch-pad` | same job | One widget. Keep the feature-form alternative and the monotone spline |
| `sign-chart` | `sign-chart` | same id, overlapping specs | One spec: their derivative rows plus our "undefined" state and solution-interval selection |
| `trial-simulator` | `sim-runner` (primitive) | composite on primitive | Build `trial-simulator` on `sim-runner` |
| `matrix-grid` | `matrix` (primitive), `matrix-multiply`, `determinant-lab` | 0.3 needs the gentle subset | Build `matrix-grid` on `matrix`, or configure `matrix-multiply` with entry-wise mode only and bring it forward to W3 |
| `linear-map` | `transform-grid` | same idea | Use `transform-grid`, brought forward to W3 with 2 × 2 Stage 0 tasks |
| `vector-plane` | `vector-combo`, `projection-lab` (both list 0.3, wave A) | overlapping | Use theirs. Add the GCSE lattice paths and ratio division to `vector-combo` |
| `sum-visualiser` (`partial-sums` mode), `sequence-lab` (partial sums) | `series-explorer` (lists 0.3) | partial overlap | Partial sums live in `series-explorer`. `sum-visualiser` keeps the proofs (Gauss, odd squares, area fill, shift-and-subtract) |
| `graph-explorer` (`approach`, `chord`, `tangentAt` overlays) | `limit-explorer`, `secant-tangent` | light against deep | Keep the light overlays for 0.2 and 0.3, built from the same `marks`. The 1.3 lessons use the dedicated composites |
| `function-machine` | `function-mapping` | different pictures of one idea | Keep both. A pipeline suits 0.2 composition and inverses; mapping diagrams suit stretch factors and the chain rule |
| `iteration-cobweb` | `root-finder` | different algorithms | Keep both |
| `scatter-fit` | `least-squares-fit` | GCSE entry against formal method | Keep both on shared `marks`. `scatter-fit` covers correlation, extrapolation and log axes; `least-squares-fit` covers the normal equations |

**Effect on counts.** The renames change nothing about what Stage 0 needs. If the five composites in the merge rows (`curve-sketch`, `sign-chart`, `matrix-grid`, `linear-map`, `vector-plane`) fold into their counterparts, Stage 0 adds 71 widgets of its own, not 76. The three layers folding into `marks` would bring that to 69.

---

## 16. Open questions and unverified items

| # | Item | Status and effect |
|---|---|---|
| 1 | Does the Artifact CSP allow WebAssembly? | A probe is running [unverified]. If yes, every Stage 0 code drill runs in the Artifact through MicroPython. If no, `code-editor`, `shell-sim` (`python3`) and `workspace-sim` hand off to the web app in the Artifact. The widgets are specified for both outcomes |
| 2 | KaTeX `\htmlId` under a restricted `trust` policy | [unverified]. `tex-terms` depends on it. A build-time test in W0. Fallback: wrap terms in our own spans after rendering, by matching KaTeX's output structure |
| 3 | Sizes and load times of MathLive and Compute Engine on the reference device | [unverified]. Affects W1 preloading. To be measured in W0 |
| 4 | Can an Artifact anchor open the web app? | [unverified]. Fallback: copyable URL |
| 5 | Zetamac default ranges | Duration and operations [sourced]; ranges [recalled, unverified]. They are configuration |
| 6 | The Khan Academy Precalculus unit list | [sourced, secondary]. Confirm by opening the course before 0.3 content is written |
| 7 | Geometry and statistics placement | Owner decision (section 0.2). The widgets are needed whatever is decided |
| 8 | `sample` tool count limit | We use 5 tools. Read `sample.limits().tools.maxCount` at runtime. If it is lower, `annotate` folds into `highlight` as an optional text field |
| 9 | Python minimum version for setup | Python 3.11 [our choice]. The owner may prefer the current release |
| 10 | Typing target | 35 words per minute at 95% accuracy [our choice]. The owner may set a different bar |
| 11 | MicroPython differences | CI runs every Stage 0 reference solution on both runtimes. Drills that differ are tagged web-only |
