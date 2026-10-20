# Zero to Quant: engine blueprint

Status: the build contract. Every agent working on `app/` follows this file. Where it conflicts with `design-research.md`, this file wins; where it is silent, `design-research.md` is the reference for look, motion and copy.

## 1. What we are building

A single-user, Brilliant-style interactive teaching app for the curriculum in `curriculum.md`, running in one Chrome browser from a static folder. No accounts, no server, no sync, no mobile layouts, no leagues, no notifications. Everything that makes the teaching good stays: the lesson mechanics, the widgets and diagrams, the feedback state machine, the hint ladder, explanations with diagram states, quizzes, level reviews, homework, exams, the redo queue, mastery, streak and XP.

The prototype in `prototype/` becomes the app in `app/`. Its CSS, router, icons, KaTeX helpers, art and screen layouts are kept. What changes: every screen reads real learner state and real content instead of fixtures, and the lesson player becomes a renderer over declarative lesson files.

## 2. Non-goals (do not build)

- Accounts, login, sync, PWA, offline caching, service workers.
- Mobile-specific layouts. Keep responsive CSS that already exists; add none.
- Leagues, league board, notifications, planned breaks, achievements.
- Block code (interaction 9). The code editor covers programming.
- C++ drills in the browser. C++ items link out to the learner's own machine.
- AI tutor or explainer.
- A build step. Plain `<script>` files, no bundler, no framework, no TypeScript.

## 3. Runtime

- Static files. Run with `app/run.sh` (python `http.server` on port 8080) or any static server. `http` is required because content is fetched and Pyodide needs it.
- Chrome only, current version. ES2022 is fine. No transpilation.
- KaTeX from `app/vendor/katex` (already vendored).
- Pyodide from the jsDelivr CDN (`https://cdn.jsdelivr.net/pyodide/v0.27.7/full/`), loaded lazily by the drill worker. Drop `scripts/vendor.sh`.
- MathLive and the CortexJS Compute Engine from jsDelivr, loaded lazily on the first expression widget. If they fail to load, the expression widget falls back to normalised string comparison against the accepted forms listed in the item.
- Persistence: `localStorage` key `zq.state` (one JSON document) plus a JSON export and import on the You screen. The state module debounces writes.

## 4. Layout of `app/`

```
app/
  index.html
  run.sh
  css/                      tokens, components, screens (kept), widgets.css, canvases.css (new)
  js/
    core.js                 kept: router, icons, tex, settings, shell, store
    data.js                 removed; replaced by content.js + state.js
    art.js                  kept
    state.js                learner state model (section 6)
    content.js              content loader and registry (section 5)
    engine/
      player.js             lesson player (section 7)
      grade.js              shared grading helpers (numeric tolerance, fraction parse, set compare, expression equivalence)
      widgets/<kind>.js     one file per widget kind (section 8)
      canvas/<kind>.js      one file per canvas kind (section 9)
      sim.js                seeded RNG and simulation helpers
    screens/
      setup.js              replaces onboarding: name, track, weekly hours, starting stage
      today.js learn.js course.js lesson.js review.js exam.js drill.js you.js system.js
      drill-worker.js
  content/
    curriculum.json         stages, topics, courses, skills (section 5)
    courses/<course>/course.json
    courses/<course>/<lesson>.json
    courses/<course>/review-<level>.json      level review
    courses/<course>/homework-<level>.json
    exams/topic-<topic>.json
    exams/stage-<n>.json
    drills/<id>.json
    warmup.json             mental arithmetic drill settings
  tools/
    validate.mjs            node: validates every content file against the schema and the semantic rules
    playthrough.mjs         Playwright: plays every lesson with the authored answers, fails on any console error
```

File ownership during the build is in section 12.

## 5. Content model

`content/curriculum.json`:

```json
{
  "stages": [
    { "id": 0, "name": "From nothing", "hours": 500, "exit": "...",
      "topics": [
        { "id": "0.1", "name": "Number", "hours": 60, "track": "maths",
          "resource": { "name": "Khan Academy: Arithmetic, then Pre-algebra", "url": "https://..." },
          "courses": ["number-sense", "ratio"] }
      ] }
  ],
  "courses": {
    "number-sense": { "name": "Number Sense", "topic": "0.1", "art": "fraction", "description": "..." }
  },
  "tracks": { "maths": "Maths", "prob": "Probability and statistics", "code": "Programming", "fin": "Finance", "ml": "Machine learning", "speed": "Interview and speed" }
}
```

`content/courses/<course>/course.json`:

```json
{
  "id": "conditional", "name": "Conditional Probability", "topic": "1.5", "art": "tree",
  "description": "Update a probability when you learn something. Build to Bayes' rule and use it on trades.",
  "skills": { "cond-shrink": "Shrinking the sample space", "cond-mult": "Multiplication rule", "bayes": "Bayes' rule" },
  "levels": [
    { "n": 1, "name": "Updating on evidence",
      "lessons": ["l1-what-changes", "l2-counting-left", "l3-shrinking"],
      "review": "review-1", "homework": "homework-1" }
  ]
}
```

Lesson, review, homework, exam and drill schemas are in `AUTHORING.md`. Every content file is plain JSON. Ids are lower-case kebab-case and unique within the course; the global id of a lesson is `<course>/<lesson>`.

`content.js` exposes `ZQ.content`:

- `load()` fetches `curriculum.json` and every `course.json` at start (60 small files, fine).
- `course(id)`, `topic(id)`, `stage(n)`, `lesson(courseId, lessonId)` (fetches and caches the lesson file, returns a Promise), `review(...)`, `homework(...)`, `exam(id)`, `drill(id)`.
- `courseLessons(id)` returns the ordered list of lesson ids with level numbers.
- `next(courseId, lessonId)` returns the next item in the course (lesson, review or homework).
- Missing files are not errors: a course whose lessons are not yet authored shows its map with locked "Not yet written" nodes and the topic's external resource. The validator reports them.

## 6. Learner state (`state.js`)

One object, saved to `localStorage['zq.state']`, versioned (`v: 1`). `ZQ.state` exposes typed mutators, never raw writes from screens.

```js
{
  v: 1,
  profile: { name, initial, track: 'Trader'|'Researcher'|'Developer'|'Undecided', weeklyGoalH: 5|10|15|25, startStage: 0..3, createdAt },
  settings: { theme, motion, sound, streakMode: 'daily'|'off' },
  xp: 0, mp: 0,
  lessons: { '<course>/<lesson>': { attempts, done, firstTry: [ok, total], xp, bestQuiz: [score, items], mastered, perfect, completedAt, secondsSpent, position } },
  reviews: { '<course>/review-1': { score, items, at } },
  homework: { '<course>/homework-1': { assignedAt, due, submitted, score, items, selfMarks } },
  exams: { 'topic-1.5': { attempts: [{ at, score, passed, bySkill }] } },
  skills: { '<skill>': { mp, elo: 1200, seen, correct, lastAt } },
  redo: [ { id, kind: 'screen'|'quiz'|'homework'|'exam', ref: { course, lesson, screen } | { course, lesson, item } | { exam, item }, due, interval: 7|30, misses } ],
  notebook: [ { course, lesson, name, tex, note, at } ],
  drills: { '<id>': { verified, code, at, draft, draftAt } },   // draft: unverified code (drills.draft), keyed by drill id or item path
  warmup: { history: [ { date, score } ] },
  hours: [ { date, block: 'main'|'build'|'review'|'mental', minutes, source } ],
  streak: { current, best, lastDay, restDays, restEarnedAt, days: { 'YYYY-MM-DD': true } },
  flags: { setupDone, streakGoal }
}
```

Rules the mutators enforce (from `design-research.md` 6.2, 8.2, 5.7):

- XP: 15 first-try screen, 5 after retry, 0 after Show solution, 20 lesson finish, 15 perfect, 15 per quiz item correct, 50 + 5 per correct homework item, 200 topic exam pass, 1,000 stage exam pass, 0 for repeating completed content.
- MP: first-try correct in quizzes, reviews, homework and exams, and successful 7-day and 30-day redos. Each adds MP to the item's skills and updates the Elo-style skill score (K = 32, item difficulty maps 1 to 5 onto 1000 to 1600).
- Mastered: lesson quiz at 80% or more. Below 80%, each wrong quiz item joins the redo queue.
- Redo: a wrong screen or item is queued for 7 days; a correct redo re-queues at 30 days; a correct 30-day redo leaves the queue. A wrong redo resets to 7 days.
- Streak: a day qualifies on 3 graded problems or 1 finished lesson, quiz, review or homework. One rest day is earned per 7 qualifying days, at most 2 held, applied automatically to a missed day.
- Hours: lesson, quiz, review and homework time is logged to `main`; drills to `build`; redo and practice to `review`; warm-up to `mental`. Manual entries are allowed from You.
- Practice and weekly problems: `practiceResult({ results: [{ id, ok, skills, difficulty }], source })` updates the Elo skill scores and the streak's problem count only (no XP, no MP).
- Exams: `examFinished` queues every missed item that has an id for redo, kind `exam`, ref `{ exam, item }`; `ZQ.select.resolve` returns that exam item without hints.
- Drill drafts: `drills.draft(id, code)` keeps unverified code in the document (so Export carries it); `drills.draft(id)` reads it and `drills.draft(id, null)` clears it. The drill screen keys by drill id; the code widget keys by item path (`course/lesson/item`, `exam/item`).
- Export produces the JSON document; import replaces it after validation of `v`.

## 7. Lesson player (`engine/player.js`)

The player renders a lesson file (schema in `AUTHORING.md`) using the existing `css/screens/lesson.css` look: top bar, frame, utilities, prose column, canvas, question, widget, verdict chip, button group. It replaces the bespoke `prototype/js/screens/lesson.js`. Routes: `#lesson/<course>/<lesson>` starts or resumes, `#lesson/<course>/<lesson>/quiz`, `#lesson/<course>/<lesson>/done`.

Per screen:

1. Render title and prose (`ZQ.md`), then the canvas (if any) via `ZQ.canvas.create`, then the question line and the widget via `ZQ.widgets.create`. Canvas and widget are linked: the player passes the canvas instance to the widget in `ctx`, so canvas-bound widgets (slider, drag-point, tap-regions, sketch, balance) drive it.
2. State machine exactly as `design-research.md` 5.4: idle, engaged, evaluating, correct, not-yet, revealed. Buttons, frame colour, wash, verdict chip, XP tick, Why?, Get help, Try again, Show solution after two misses, Continue.
3. Grading calls `widget.grade()` which returns `{ ok, key, detail }`. `key` selects the feedback line: the matched distractor or misconception, else the generic line. On not-yet, if the widget supports `showWhy(key)` the player calls it (canvas animation of the consequence).
4. Hints: `Get help` opens the sheet with the authored rungs in order; rung 2 (`point`) calls `canvas.highlight(ids)`; after rung 3 the sheet offers Show solution. Hints are available after the first Check.
5. Explanation: `Why?` opens the modal with `explain.text` and applies `explain.canvas` state to a cloned canvas inside the modal.
6. Non-task screens (title, demonstrate, generalise, summary) have Continue only. `demonstrate` renders a stepper over `steps[]`, each step setting canvas state and showing a caption.
7. Progress bar advances on Continue. Position is saved on every Continue and on close; reopening resumes.
8. End of lesson: celebration (reuse the prototype's), summary card (ideas, formula card saved to the Notebook, trap), quiz (one attempt each, dot progress, Why? after each), then streak moment if the day just qualified, then Next (next item in the course) or Done.
9. Everything written to `ZQ.state` through mutators: `screenGraded`, `lessonFinished`, `quizFinished`, `redo.add`, `notebook.add`, `hours.log`.
10. Keyboard: Enter is the primary button; Escape closes sheets; keys 1 to 9 pick options.

The same player renders level reviews, homework, redo sessions, practice sets and exams in "set mode": a list of items with dot progress, no hints, one attempt per item, and the timer and flagging that `exam.js` already has. Exams keep their own screen (`exam.js`) for the start card, timer, flag list and result, but render each item through `player.renderItem(item, host, { mode: 'exam' })`.

Test hook: `window.ZQ.test = { current(): { screenIndex, kind }, answerCorrect(): applies the authored answer to the widget, check(), continue() }`. The playthrough script uses it. The same four calls exist in set mode: `runSet` (level reviews, practice, redo) and the set page around it, the homework page and the exam screen each install `ZQ.test`, where `current().kind` is `loading`, `start` (continue() begins), `item` (answerCorrect, check, continue), `submit` (homework: continue() submits) or `done`. On homework and exam pages check() grades the shown item without marking it; the marks come on submit as for the learner. Every widget has an authored correct answer the hook can apply, including `balance` (the shortest sequence of the allowed moves to the target) and `sketch` (the control points on the target curve).

## 8. Widgets (`engine/widgets/`)

Registry: `ZQ.widgets.register(kind, factory)`. `factory(host, spec, ctx)` returns:

```js
{
  el,                       // root element, already appended to host
  value(),                  // current learner input (serialisable)
  set(value),               // restore an input (resume, redo)
  grade(),                  // { ok: boolean, key: string|null, detail: any }  pure, no side effects
  lock(), unlock(),         // during evaluating / after grading; Try again unlocks
  markGraded(result),       // apply correct / not-yet styling to answer objects (never to series)
  reveal(),                 // animate to the correct answer in hint-indigo (Show solution)
  showWhy(key),             // optional: animate the consequence of the wrong answer
  reset(),                  // Start over
  focus(),
  destroy(),
  onChange(fn)              // fires on every learner interaction; the player moves idle -> engaged
}
```

`ctx` carries `{ Z: ZQ, canvas, rng, reducedMotion, mode: 'lesson'|'set'|'exam' }`.

The kinds, with grading rules. Specs are in `AUTHORING.md`.

| kind | Input | grade() |
|---|---|---|
| `choice` | one option | the chosen option's `correct`; `key` = option id |
| `multi` | set of options | exact set match; `key` = first wrong or missing option id |
| `numeric` | text | parses integers, decimals, fractions `a/b`, percentages if `unit` is `%`; `abs` or `rel` tolerance; `key` = the matching `wrong[]` entry id |
| `expression` | MathLive field (fallback: text) | symbolic equivalence via Compute Engine `isEqual` after `simplify`, and with `form` the canonical shape (expanded, factorised, simplified; key `form`); fallback compares normalised strings against `accept[]`; `key` from `wrong[]` by the same test |
| `slider` | number | within `answer ± tol`; `key` from `wrong[]` ranges |
| `drag-point` | point or points on the canvas | each within `tol` of its target (canvas units); `key` from `wrong[]` regions |
| `place` | mapping token -> slot, or items in the containers of a `boxes` canvas (`mode: "boxes"`) | exact mapping (tokens with the same text interchangeable under `byText`, or a `same` group), or `order` of tokens in one slot, or each named container's items; `key` = first misplaced token or item |
| `tap-regions` | set of canvas region ids | exact set match; `key` from `wrong[]` sets, else first wrong region id |
| `order` | permutation of lines | exact order; per-line marks after grading |
| `table` | cell values | every editable cell within tolerance |
| `manipulate` | path through the authored state graph | reaching a `target` state; `key` from the state's `why` |
| `balance` | moves on the pans (signed pans: subtract or add any amount, divide by any non-zero number) | pans level with the unknown alone on one side (authored `target`) |
| `sketch` | control points | every sampled x within the tolerance band of the target curve |
| `code` | source | hidden tests pass (Pyodide worker, reused from `drill.js`) |

`simulate` is not a widget: it is a canvas (`bars` or `walk` with `sim`) plus any widget asking about the result.

## 9. Canvases (`engine/canvas/`)

Registry: `ZQ.canvas.register(kind, factory)`. `factory(host, params, ctx)` returns:

```js
{
  el,
  set(state),               // apply a state patch (merges); animates over 480 to 800ms unless reduced motion
  get(),                    // current state
  highlight(ids, on=true),  // pear wash + 2px ink ring pulsing twice on the named elements
  clone(host2),             // a static copy for the explanation modal
  on(event, fn),            // 'change' for interactive canvases, with the interaction payload
  enable(mode),             // interactive mode requested by a widget: 'tap', 'drag', 'slider', 'sketch', 'balance'
  destroy()
}
```

All canvases are SVG, theme-aware through CSS custom properties from `tokens.css`, use the diagram palette (`design-research.md` 2.6: six series slots in order, manipulable blue for movable things, 2px primary strokes, 1px gridlines, 1.5px axes, dashed targets), label series directly, and scale to the 540px column (`viewBox`, width 100%). Every element an author may highlight or an explanation may recolour has a stable id in the state (cells `r1c1`, branches `b-a-b`, regions `A`, `AB`, points `p1`, bars `x3`, nodes `n2`).

| kind | Shows | Params (summary) | Interactive modes |
|---|---|---|---|
| `grid` | n×m cell grid: sample spaces, two-dice tables, area models, Punnett squares | rows, cols, row/col labels, cell text fn or table, shaded sets, outlines | tap (regions) |
| `tree` | probability tree, decision tree | levels of branches with labels and probabilities, highlighted paths, leaf values | tap (branches) |
| `venn` | 2 or 3 set Venn with counts or probabilities per region | sets, labels, region values, shaded regions | tap (regions) |
| `number-line` | points, intervals, arrows, ticks | range, ticks, points, intervals | drag (points), slider |
| `boxes` | balls in boxes, cards, coins, urns, slots for counting | containers and items, draw animation | drag (place) |
| `area` | fraction and multiplication area models, geometric probability | shape, shaded fraction, grid | tap |
| `balance` | two-pan scale with weights and unknown blocks | left, right items; tilt computed | balance |
| `circle` | unit circle, angles, sine and cosine projections, radians | angle, shown projections | drag (angle point) |
| `plane` | coordinate plane: functions (expression strings evaluated in JS), points, segments, tangent lines, shaded areas under curves, Riemann rectangles, vectors | xRange, yRange, functions, points, areas, vectors | drag (points), sketch (curve from control points), slider-bound parameters |
| `bars` | bar chart and histogram; live simulation fill with an exact value line | categories or bins, values, exact line, `sim` block (trials, outcome fn) | slider (trials) |
| `distribution` | pmf or pdf with parameters and a shaded probability region | family (binomial, geometric, poisson, normal, exponential, uniform, t), params, shade from/to | slider-bound parameters, drag (shade bounds) |
| `scatter` | points with an optional fitted line, residuals, outliers | points, line, residuals | drag (points, line endpoints) |
| `series` | time series line (prices, returns, cumulative P&L), candles optional, drawdown shading | series, labels, markers, shaded ranges | slider (window) |
| `walk` | random walk or price path simulation, many paths, hit levels | steps, paths, p, barriers, `sim` | slider |
| `matrix` | one or more matrices with highlighted rows, columns, pivots; row operation arrows; the product cell animation | matrices, highlights, ops | tap (cells) |
| `vectors` | 2D vectors: arrows, sums, scaling, projection, span, basis change | vectors, show sum/projection/grid | drag (vector heads) |
| `graph` | nodes and edges: algorithms, Markov chains with transition probabilities, trees | nodes, edges (directed, weighted), visited order, current | tap (nodes) |
| `array` | array or list cells with index labels and pointer arrows: sorting, two pointers, binary search, stacks, queues | cells, pointers, highlighted ranges, stack mode | tap (cells), drag (reorder) |
| `payoff` | option payoff and P&L against the underlying: calls, puts, spreads, strikes, premiums, breakevens | legs, range, strike, premium | slider (strike), drag (strike) |
| `orderbook` | bid and ask ladder with sizes, spread, a market order walking the book | bids, asks, order animation | tap (levels) |
| `table` | static or editable data table with highlights | columns, rows, editable cells | table widget |
| `pair` | two canvases side by side (a circle beside its sine graph); `derive` reads across both | `left`, `right` canvases, `active` side | the active side's modes; ids prefixed `left:` / `right:` |

`sim` blocks run with the seeded RNG from `engine/sim.js` so a lesson replays identically. Trials animate the chart over at most 1,200ms with a Run 10 / 100 / 1,000 control rendered by the canvas.

## 10. Screens

All screens keep their current layout and CSS and drop their fixtures.

- `setup`: three steps on first run (name, track, weekly hours, starting stage); writes `profile` and `flags.setupDone`. Rerunnable from You.
- `today`: streak and week strip from `streak`, weekly goal blocks from `hours`, due work from `redo` and `homework`, warm-up from `warmup`, resume from the last unfinished lesson, next exam readiness from skills. No league card.
- `learn`: catalogue from `curriculum.json` with progress per course; the Paths view stays, from `profile.track`. Each topic card links its external resource and shows the topic exam and its state.
- `course`: the map generated from `course.json` and lesson state. The same serpentine pucks. Node states: done, mastered, current, upcoming, locked, not-written. Level review and homework nodes. Course card with progress, Start or Continue.
- `lesson`: the player.
- `review`: Redo queue (real, due items first), Practice (sets generated by the selection rule in `design-research.md` 8.4 from quiz, review and homework item pools of finished lessons), Homework (assigned when a level's last lesson is finished), Exams (topic exams unlocked when every course in the topic has at least one mastered lesson, always allowed "sit early"), Notebook (real cards and the topic notation cards). The self-marked long-form rubric flow stays.
- `exam`: from `content/exams/*.json`, rendered through the player's set mode with the existing start card, timer, flags, result, per-skill breakdown and pass stamp. Stage exams list the parts the app cannot mark (a script that runs, a GCSE paper) as self-ticked checks.
- `drill`: from `content/drills/*.json`; the existing editor, worker, hidden tests, "How it is checked". Pyodide from CDN.
- `you`: profile, mastery map from `skills` grouped by track and topic, streak calendar from `streak.days`, stats, settings, export and import, "run setup again", manual hours entry. No league board.
- `system`: kept as is, plus a gallery that renders every canvas kind and every widget kind with sample params (this is the visual test page).

## 11. Tools

- `tools/validate.mjs` (node, no dependencies): loads `curriculum.json`, every course, lesson, review, homework, exam and drill file; checks the schema and the semantic rules in `AUTHORING.md` section 7; prints one line per problem with the file and path; exits non-zero on any error; `--summary` prints lesson counts per course and the list of mapped-but-unwritten lessons.
- `tools/playthrough.mjs` (Playwright, Chromium at `/opt/pw-browsers/chromium`): starts the static server, opens every lesson, drives `ZQ.test` to answer every screen correctly and finish the quiz, asserts zero console errors and that the completion screen is reached; also opens every other route once. `--lesson <course>/<lesson>` runs one. `--sets` plays every written level review and homework, `--exams` every exam, through the set-mode hook, answering every item correctly and asserting the recorded result is full marks (and the exam passed); `--set <course>/<id>` and `--exam <id>` pick one; `--all` runs lessons, routes, sets and exams. A screen with a `code` widget is checked only once its Python status reads ready; Python failing to load (no CDN access without `--local-cdn <dir>`) is a failure, and so is an authored answer that applies with nothing to check, so no screen is skipped silently.

## 12. Build phases and file ownership

Agents never commit; the orchestrator commits. Agents do not edit files owned by another agent in the same phase. Shared files in a phase are listed with one owner.

Phase 1, engine (parallel):

- E1 Foundation: `git mv prototype app`; `js/state.js`, `js/content.js`, `js/screens/setup.js`, `content/curriculum.json` (structure from `data.js`, resources and URLs from `curriculum.md`), `index.html` (script and stylesheet list: add every file the other agents will create, by the names in this plan), `run.sh`, `js/screens/drill-worker.js` CDN switch, `tools/validate.mjs`, root `README.md` and `app/README.md`. Owner of `js/core.js` (add `ZQ.state`, `ZQ.content` wiring, route params `#lesson/<course>/<lesson>`).
- E2 Player and input widgets: `js/engine/player.js`, `js/engine/grade.js`, `css/widgets.css`, widgets `choice`, `multi`, `numeric`, `expression`, `order`, `table`, `place`, `code`, `manipulate`; `js/screens/lesson.js` rewritten as a thin screen that mounts the player; port the prototype's conditional-probability lesson 3 to `content/courses/conditional/l3-shrinking.json` as the reference lesson, using the `grid` canvas (stub it locally if E3 has not landed; E3 owns the real one).
- E3 Canvases A: `js/engine/canvas/{grid,tree,venn,number-line,boxes,area,balance,circle,table}.js`, `css/canvases.css`, canvas-bound widgets `tap-regions`, `balance`, `drag-point` (works against any canvas exposing `enable('drag')`), `js/engine/sim.js`, `js/engine/canvas/_base.js` (shared SVG helpers, palette, animation, highlight).
- E4 Canvases B: `js/engine/canvas/{plane,bars,distribution,scatter,series,walk,matrix,vectors,graph,array,payoff,orderbook}.js`, widgets `slider`, `sketch`. Uses `_base.js` from E3 (agreed helper names in section 9 and `_base.js` header; E3 lands first or E4 writes to the same API and the orchestrator merges).

Phase 2, screens (parallel, after phase 1):

- S1: `today.js`, `learn.js`, `course.js` on real state and content.
- S2: `review.js`, `exam.js`, the practice and redo selection in `js/engine/select.js`, `content/exams/` schema support.
- S3: `drill.js` on `content/drills`, `you.js` (mastery, calendar, export and import, settings), `system.js` gallery, `tools/playthrough.mjs`.

Phase 3, content: curriculum design (every `course.json`), then lessons level by level, then topic exams, stage exams and drills. Authoring rules in `AUTHORING.md`.

Phase 4, review: validator clean, playthrough green, orchestrator spot-reads lessons and plays the app.

## 13. Definition of done

1. `node tools/validate.mjs` passes.
2. `node tools/playthrough.mjs` passes for every authored lesson.
3. Every screen works with an empty state (fresh browser) and with a populated state (after playing).
4. Every course has a `course.json`; unwritten lessons show as such and never throw.
5. The reference lesson plays identically to the prototype's bespoke version.
6. Export then import round-trips the state.
7. Content second-reader pass: once a topic's courses are complete, a fresh agent reads every lesson of the topic as a learner (not its author), recomputes every stated number, checks each derivation line and each distractor's `why`, and reports errors for the orchestrator to fix. The playthrough proves the app grades its own answers consistently; this pass is what checks that the answers are right.
8. Programming courses that cannot run in the browser (C++; a real shell for git and terminal) teach by reading, tracing and predicting output, with Python-checked or choice answers, and say so on their first screen. A C++ compiler in WebAssembly is engine work for later if wanted.
