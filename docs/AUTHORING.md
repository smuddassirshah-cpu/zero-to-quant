# Authoring guide: lessons, reviews, homework, exams and drills

This is the contract between content authors and the engine. Every content file is JSON under `app/content/`. `node app/tools/validate.mjs` enforces section 7. Read `PLAN.md` sections 5, 8 and 9 for the engine side, and `design-research.md` sections 5, 8 and 9 for the pedagogy and voice this encodes.

## 1. Lesson file

`content/courses/<course>/<lesson>.json`

```json
{
  "id": "l3-shrinking",
  "course": "conditional",
  "title": "Shrinking the sample space",
  "minutes": 12,
  "objectives": ["Compute a conditional probability by counting what is left", "Explain why the condition shrinks the denominator"],
  "skills": ["cond-shrink"],
  "screens": [ ...8 to 12 screens... ],
  "summary": {
    "ideas": ["A condition throws away every outcome that contradicts it.", "...", "..."],
    "formula": { "name": "Conditional probability", "tex": "P(A \\mid B) = \\dfrac{P(A \\cap B)}{P(B)}", "note": "Count inside B, not inside everything." },
    "trap": "Adding the two chances counts the corner cell twice."
  },
  "quiz": [ ...3 to 5 items... ]
}
```

- `skills` are ids declared in the course's `course.json`. Every lesson names at least one.
- `minutes` is the planned time, 10 to 15.

## 2. Screens

Every screen has `type`, and most have `canvas`, `question` and `widget`. Prose supports inline `$...$` and display `$$...$$` KaTeX, `**bold**`, `*italic*`, inline code in backticks, and fenced code blocks (```python). A fenced block shows its language and a Copy button in a strip above the code (an output block, ` ```text ` or ` ```output `, has no Copy button); long lines scroll sideways inside the block. Inline code keeps its spaces and may wrap when a line is full. Code spans are read first, so `$` and `*` inside backticks stay literal (`` `echo $HOME` ``, `` `ls *.py` ``). Display maths wider than the column scrolls sideways in its own box on a phone. Lines starting `- ` (or `* `) make a bulleted list and `1. ` a numbered one, in lesson prose and in set items alike. A Markdown table (a header row `| a | b |`, a separator `|---|---:|`, then rows) renders as a table in prose, set-item prompts and long-form model answers; `:---:` and `---:` align a column. A fenced block fits about 54 characters a line in the 540px column before it scrolls, so wrap long code by hand where the line breaks naturally. Canvas captions render the same way. Keep prose under 60 words per screen.

Any screen may also carry `tags` (a list of kebab-case family names, the first being its family) and `pace` (seconds); both are defined in section 5 and checked by the validator. A lesson screen's `tags` are not read by the Interview practice deck yet (only quiz, review and homework items are), but the pace line uses them.

The player shows Start over only where there is something to put back: a canvas-bound widget, a canvas with controls or a draggable point, or an `order`, `place`, `manipulate` or `table` widget. Choice, numeric and code screens with a static diagram have none. Start over puts the canvas back as it was first drawn (its own defaults for anything the screen did not set).

```json
{
  "type": "problem",
  "difficulty": 2,
  "title": "Optional short heading",
  "prose": "Two fair dice. You learn the first die shows a 5. $P(\\text{total} = 7)$ before and after?",
  "canvas": { "kind": "grid", "params": { ... }, "state": { ... } },
  "question": "How many outcomes are still possible?",
  "widget": { "kind": "numeric", ... },
  "hints": [
    { "rung": "nudge", "text": "Which cells disagree with what you learned?" },
    { "rung": "point", "text": "The first die is fixed.", "highlight": ["r5c1", "r5c2", "r5c3", "r5c4", "r5c5", "r5c6"] },
    { "rung": "step", "text": "Only row 5 survives: six cells. Now count the ones summing to 7 inside that row." }
  ],
  "feedback": {
    "correct": "Six cells survive, one for each second die.",
    "generic": "Not quite right. Count only the cells that agree with the first die showing 5.",
    "byKey": { "36": "You counted the whole table. The condition rules most of it out.", "r5c2": "That cell is in the row, but you shaded more than the row." }
  },
  "explain": {
    "text": "Learning the first die shows 5 keeps row 5 and nothing else. That row is the new whole. Any probability now is a count within it over 6.",
    "canvas": { "shade": { "survivors": ["r5c1","r5c2","r5c3","r5c4","r5c5","r5c6"] }, "outline": "row5" }
  }
}
```

Screen types and what they require:

| type | Purpose | Requires |
|---|---|---|
| `title` | lesson name, one framing sentence, optional canvas in a static state | `prose`; no widget |
| `explore` | free manipulation, then one observation question | `canvas` with an interactive mode (`controls`, a canvas-bound widget, points with `drag: true`, vectors in `state.drag`, or a `sim`), `widget` |
| `problem` | a graded task | `question`, `widget`, `feedback` |
| `ladder` | same canvas, one new constraint | as `problem`; reuse the previous canvas kind |
| `demonstrate` | animated step-through | `steps: [{ "caption": "...", "canvas": {state patch} }]`, 3 to 6 steps; no widget |
| `trap` | the common misconception, met and resolved | as `problem`; at least one `byKey` line naming the misconception |
| `generalise` | the rule as a description of what the learner just did | `prose` with the formula in KaTeX (in a programming course, a topic on the code track, a fenced code block stating the pattern does instead); `widget` with one confirmation item |
| `derive` | complete a missing line | `widget` of kind `expression`, `order` or `choice` |
| `transfer` | same idea in a quant context | as `problem` |
| `summary` | not a screen: the `summary` block renders after the last screen | |

Lesson shape (design-research 8.3): hook (problem or explore), explore, name (generalise comes later, but the term is introduced on this screen by what was just done), ladder 2 to 4 screens, trap, generalise and derive, transfer, then summary and quiz. Eight to twelve screens, at most one `title` and at most two non-task screens (`title`, `demonstrate`, `generalise` without a task) per lesson. Difficulty runs 1 up to 3 across the screens.

`hints`: up to three rungs in the order nudge, point, step. `point` carries `highlight` ids for the canvas. Hints are optional on `explore`, required on `problem`, `ladder`, `trap`, `transfer` and `derive`.

`feedback.byKey`: keys are the `key` values the widget can return (option ids, `wrong[]` ids, region ids, token ids, state ids). Each line names the learner's own action, never the rule. At most three sentences.

The engine's end-of-lesson order is: summary card (last progress step), quiz, celebration with the streak moment, Next or Done.

`explain.text`: at most three sentences, refers to what the learner did, with the `explain.canvas` patch showing the annotated state.

## 3. Widgets

Each `widget` has `kind` and the fields below. `label` is the accessible name of the control.

### `choice`

```json
{ "kind": "choice", "layout": "grid|stack", "options": [
  { "id": "a", "text": "$1/6$", "correct": true },
  { "id": "b", "text": "$1/36$", "why": "You kept the whole table as the denominator." },
  { "id": "c", "text": "$2/6$", "why": "You counted (5, 2) and (2, 5), but (2, 5) is gone." }
] }
```

Exactly one `correct`. Every distractor has `why` (one named misconception each). Options may be text, KaTeX, or `{ "image": "art-id" }` for a course art glyph. `shuffle: true` is allowed except when options are ordered (ranges, steps).

An option may hold a fenced code block (```` ```python ... ``` ````): it is drawn as a small multi-line code block inside the option, with no Copy button, and any text around it stays inline.

Any `choice` or `multi` option, and any `numeric`, `slider` or `tap-regions` `wrong[]` entry, may carry a `canvas` patch: it is applied by Show why after that wrong answer and reverted on Try again. Use it to show the consequence of the misconception on the diagram (highlight the double-counted cell, mark it `×2`).

### `multi`

Same as `choice`, several `correct`. The question line must say "Select all that apply".

### `numeric`

```json
{ "kind": "numeric", "answer": 0.1667, "tol": { "abs": 0.0005 }, "unit": "", "placeholder": "fraction or decimal",
  "accept": "Any form equal to 1/6, or 0.1667 ± 0.0005",
  "wrong": [ { "id": "whole", "value": 0.0278, "tol": { "abs": 0.001 } }, { "id": "double", "value": 0.3333, "tol": { "abs": 0.001 } } ] }
```

`tol` is `{ "abs": x }` or `{ "rel": r }`. Integers use `{ "abs": 0 }`. `unit` may be `%`, `£`, `$`, or a word; with `%` the learner types 16.7 and the engine compares 0.167. `accept` is shown after grading. Each `wrong` entry id is a `byKey` key.

### `expression`

```json
{ "kind": "expression", "answer": "\\frac{x+1}{2}", "accept": ["(x+1)/2", "x/2+1/2", "0.5x+0.5"],
  "wrong": [ { "id": "forgot-half", "tex": "x+1" } ], "keyboard": "algebra|calculus|probability" }
```

Graded by symbolic equivalence; `accept` is the fallback list of forms (plain text as a learner would type).

`"form": "expanded" | "factorised" | "simplified"` also asks for a shape, for expand and factorise tasks with free entry. Expanded: no bracketed sum left inside a product or power (`2x + 6`, not `2(x + 3)`). Factorised: a product with a bracketed sum among its factors, or a power of one (`2(x + 3)`, `(x + 1)^2`, a leading minus allowed). Simplified: like terms collected and fractions cancelled (`5x`, not `3x + 2x`). An equal answer in the wrong shape returns the key `form` (give it a `byKey` line; the default line says what to do). Without the maths engine the text fallback accepts only `answer` and `accept[]`, so write every accepted form in the asked shape.

How equivalence is decided: when both sides evaluate to numbers, agreement at six seeded points (every free symbol from 0.3 to 3) decides, so true identities the symbolic engine misses still pass and `5R` fails for `5\sqrt{R}`. Counting answers may use `\binom{n}{k}` (also `\dbinom`, `\tbinom`, `{n \choose k}`) and factorials: both sides are then compared at whole-number points from 1 to 12 (points where either side is undefined are skipped), so `\binom{n}{2}` and `\frac{n(n-1)}{2}` agree and `\frac{n!}{(n-k)!}` can be an answer. `"upToConstant": true` accepts an answer that differs from `answer` by a constant (antiderivatives: `x^2 + C`, `x^2 + 5` and `x^2` all pass for `x^2`), so `+C`, `+c` and `+K` need not be listed in `accept`.

**Complex answers.** An `i` in the answer or in the learner's input is the imaginary unit (`\mathrm{i}` too), and the grader compares the real and the imaginary part at every seeded point, so `\frac{1}{1+i}`, `\frac{1-i}{2}` and `0.5-0.5i` agree, `3-4i` fails for `3+4i`, and `0` fails for `(1+i)^2`. Free symbols stay real: write `x + iy`, not `z` and `\bar{z}`. `\overline{...}` and `\bar{...}` are the conjugate, `|z|` the modulus, and `e^{i\theta}` equals `\cos\theta + i\sin\theta`. A real answer must not use a bare `i` as an index or variable; use `k`, `j` or `n`.

**Vectors and matrices.** One widget can take a vector: `"answer": "(2, -1, 3)"` or `\begin{pmatrix}2\\-1\\3\end{pmatrix}`. A column, a row, `(a, b, c)`, `[a, b, c]` and `\langle a, b, c\rangle` are the same vector, each entry is compared by the usual seeded-point test (symbols and complex entries are fine), and a matrix answer (`pmatrix` with rows and columns) is compared entry by entry and needs the same shape. A wrong number of entries returns the key `length` (give it a `byKey` line; the default says "Your answer has 2 components. The answer has 3 components."). `\mathbf{i}, \mathbf{j}, \mathbf{k}` notation is not read: ask for the components.

**`\min`, `\max`, `N`, `\epsilon`.** `\min(a, b)` and `\max(a, b, c)` work anywhere in an answer, also added to or multiplied by something. A capital `N` or `D` is an ordinary symbol. `\epsilon`, `\varepsilon` and ε are one symbol, so list only one form. Seeded points lie between 0.3 and 3, so a switch at 0 or below (`\max(0, x)` against `x`) cannot be told apart.

### `slider`

```json
{ "kind": "slider", "min": 0, "max": 1, "step": 0.01, "start": 0.5, "bind": "p", "unitLabel": "", "answer": 0.5, "tol": 0.02,
  "wrong": [ { "id": "too-high", "from": 0.6, "to": 1 } ] }
```

`bind` names a canvas parameter the slider drives live (the canvas redraws on every change). Without `answer` the slider is an explore control and the screen's task comes from another widget; in that case put the slider under `canvas.controls` instead (section 4). `"format": "fraction"` shows the value as a fraction in lowest terms (0.375 reads 3/8) on the thumb and the ends; `"percent"` shows 0.375 as 37.5%.

### `sliders`

Two or more sliders graded together, for "find a and b that reach the target".

```json
{ "kind": "sliders", "sliders": [ { "id": "a", "bind": "a", "min": 0, "max": 5, "step": 0.1, "label": "$a$" }, { "id": "b", "bind": "b", "min": 0, "max": 5, "step": 0.1, "label": "$b$" } ],
  "answer": { "a": 2, "b": 3 }, "tol": 0.05, "wrong": [ { "id": "swapped", "check": "a > b" } ] }
```

Each slider drives the canvas as a `slider` does (`bind`). `tol` is one number or one per slider (`{ "a": 0.05, "b": 0.1 }`). Instead of `answer`, `"check": "a * b"` with `"value": 6` and `tol` accepts any pair whose expression is within `tol` of `value` (give `show: { "a": 2, "b": 3 }` for Show solution). Keys: the first `wrong[]` whose `check` holds, else the id of the first slider off its answer (`off` in the check form).

### `trade`

A market-making game over the `orderbook` canvas (ENGINE-BACKLOG 459). Each turn the learner sets a bid, an ask and a size and sends them. A seeded counterparty hits the bid, lifts the ask or stays out. Cards arrive on a schedule, a position limit applies, a live ledger shows position, cash, mark-to-market and realised P&L, and after the last turn the hidden value settles the position. Put it on a `problem`, `ladder` or `transfer` screen (or a set or exam item) with an `orderbook` canvas: the learner's quote appears in the book as "You" and the opening mark as the fair value. Without that canvas the widget still plays; the validator warns.

```json
{ "kind": "trade", "seed": 6, "turns": 8, "fair": 100, "value": 103, "tick": 0.5, "range": [94, 108], "currency": "£",
  "size": { "min": 1, "max": 3, "start": 1 }, "limit": 4, "spread": { "min": 1, "max": 4 }, "quote": { "bid": 98, "ask": 102, "size": 1 },
  "counterparty": [ { "type": "noise", "rate": 0.8, "turns": [1, 4] }, { "type": "informed", "edge": 0.5, "turns": [5, 8] } ],
  "schedule": [ { "turn": 1, "text": "The share last traded at £100." },
                { "turn": 4, "text": "A report beats forecasts. Fair is now £101.50.", "fair": 101.5 },
                { "turn": 7, "text": "The value is revealed: £103.", "reveal": true } ],
  "benchmark": 8, "maxBreaks": 0,
  "strategy": [ { "bid": 99, "ask": 101, "size": 2 }, { "bid": 99, "ask": 101, "size": 2 }, { "bid": 99, "ask": 101, "size": 2 }, { "bid": 99, "ask": 101, "size": 2 },
                { "bid": 100.5, "ask": 103.5, "size": 1 }, { "bid": 100.5, "ask": 103.5, "size": 1 }, { "bid": 100.5, "ask": 103.5, "size": 1 }, { "bid": 100.5, "ask": 103.5, "size": 1 } ] }
```

The authored sample is `content/exams/mock-trade-sample.json` (play it with `node tools/playthrough.mjs --exam mock-trade-sample`).

**Fields**
- `seed` (whole number, required), `turns` (2 to 40), `fair` (the opening mark, public), `value` (the hidden settlement value). The game is deterministic: the counterparty's random draws for turn `t` come from `seed` and `t` alone, so the same quotes meet the same counterparty every time, and the playthrough can replay `strategy`.
- `tick` (price step, default 0.5; the inputs snap to it), `range: [low, high]` (lowest and highest price, default fair plus or minus 20 ticks), `size: { min, max, start, step }` (defaults 1, 5, 1, 1), `quote: { bid, ask, size }` (the opening values; default fair minus and plus two ticks), `currency` (`"£"`), `dp` (price decimals, default from `tick`).
- `limit`: the position limit, either way. A quote whose size is more than the room left on a side (room to buy is `limit - position`, room to sell is `limit + position`) is cut back to the room and counts as a `limit` break.
- `spread: { min, max }`: the allowed width, ask minus bid. A spread outside it counts as a `spread` break (the quote still goes out). A bid at or above the ask is a `crossed` break and is rejected: nobody trades that turn.
- `counterparty`: one object or a list. Each has a `type` and an optional `turns: [first, last]` (1-based); the first entry whose `turns` contains the turn is used, else the first entry without `turns`.
  - `noise`: trades with chance `rate` (default 0.6), on a random side, for 1 to `maxSize` (default `size.max`), at your price. `reach` (default none) makes it refuse a price further than `reach` from the current mark.
  - `informed`: knows `value`. With chance `rate` (default 1) it lifts your ask when `value - ask > edge`, or hits your bid when `bid - value > edge` (`edge` default 0, a price distance; larger means it only trades on a clear mistake), for your full quoted size (or `maxSize`).
  - `scripted`: `trades: [{ act, size, price }]`, one entry per turn. `act` is `"hit"` (it sells to your bid: you buy), `"lift"` (it buys from your ask: you sell) or `"none"`. `price` is its limit: a hit happens only if your bid is at least `price`, a lift only if your ask is at most `price`. `size` defaults to 1.
- `schedule`: cards, `[{ turn, text, fair, reveal }]`. A card shows before that turn's quote. `fair` moves the mark (the ledger's mark-to-market and the book's fair value); `reveal: true` shows the hidden value (the mark becomes `value`). `text` may hold `$maths$`. The value always settles after the last turn.
- Grade: `benchmark` (final P&L at least this) or `band: [low, high]` (final P&L inside it), exactly one. `maxBreaks` (default 0) is how many rule breaks are allowed in all (one per turn and kind). Rule breaks fail the screen first, then the P&L.
- `strategy`: required, `[{ bid, ask, size }]`, one entry per turn: a run that meets the target. The test hook, Show solution and the Why? replay play it, and the validator plays it through the same game and errors if it misses the target or breaks a rule. It also warns when the opening quote left untouched for every turn already meets the target.
- `carry`: a name; see "Carried values" below.

**Keys for `feedback.byKey`:** `low` (P&L under the benchmark or band), `high` (over the band; only with `band`), `limit` (only with `limit`), `crossed`, `spread` (only with `spread`). The engine writes the per-turn lines itself ("Turn 3: you quoted £99.0 / £101.0 for 2. Your bid was hit: you bought 2 at £99.0. Position +2."), shows a warning under the inputs before a quote that would break a rule, and, when the eight turns are done, a results box: final P&L, the target, the rule breaks, and a table of every turn with the counterparty type and each trade's edge against the value (negative: made against someone who knew more). Check unlocks after the last turn; a miss under Try again starts the game afresh (same seed, same counterparty). Ledger: average-cost realised P&L, mark-to-market is cash plus position at the mark, final P&L is cash plus position at the value (the settlement is added to realised).

**Layout and keys.** Three steppers (bid, ask, size) with minus and plus buttons of 44 px, a ledger of four tiles (two by two at 390 px), the cards, the turn log. Arrow up and down change the focused value by one tick; Enter in a field sends the quote (it does not also press Check). Both themes use tokens only.

### Carried values (`carry`, ENGINE-BACKLOG 460)

Any widget may carry `"carry": "name"` (letters and digits). When its screen is checked or revealed, the learner's value is stored for the rest of the lesson (or set): a number for `numeric` (as typed), the `{ id: value }` map for `sliders`, and `{ pnl, position, cash, realised, mtm, breaks, turns, value }` for `trade`. A later screen reads it with `{{carry.name}}` or `{{carry.name.pnl}}` (add `|text` for a fallback: `{{carry.name|none}}`) in any string of its spec: prose, a canvas `state` or `params`, a `numeric` `answer`. A string that is only the placeholder becomes the number itself, so `"fair": "{{carry.desk.pnl}}"` is a number on the canvas and `"answer": "{{carry.desk.pnl}}"` grades what the learner earned; in running text numbers show to at most two places with a proper minus. The validator errors when a screen reads a name that no earlier screen of the lesson stores. Limits: the store lives in memory (reopening a lesson part-way forgets it and the fallback or 0 shows), is cleared when a lesson or a set starts, and an exam or homework item cannot read it because those papers draw every item at once.

### `drag-point`

```json
{ "kind": "drag-point", "points": [ { "id": "p1", "target": [2, 4], "tol": 0.3 } ],
  "wrong": [ { "id": "on-axis", "region": { "x": [1.5, 2.5], "y": [-0.3, 0.3] } } ] }
```

The canvas must list the same point ids as draggable. On a number-line or circle `target` is a bare number (the x value, or the angle; on a circle in radians a `tol` of 0.25 is about 14 degrees, so give 0.02 there); elsewhere it is `[x, y]`. `tol` is optional (default 0.25). On a plane, `tol: [dx, dy]` is a per-axis tolerance, `tolX` checks x alone, and a target `{ "on": "f", "x": 12.3 }` is the point of function `f` at that x, graded on x alone (so dragging along a steep curve is fair). Keys: the id of a `wrong[]` region that holds a point, else the id of the first point that is off target, so `byKey` may speak to a point by its id.

A whole line or level set can be the target: `{ "line": [[0, 0], [1, -2]] }` accepts any point within `tol` of that line, and `{ "expr": "2*x + y", "value": 0, "show": [1, -2] }` any point where the expression is within `tol` of `value` ("drag until the dot product is 0"). `show` is where Show solution puts the point (a line defaults to its first point; an `expr` target needs `show`). A plane point the widget names is draggable even without `drag: true` in the canvas.

### `place`

```json
{ "kind": "place", "tokens": [ { "id": "t1", "text": "$n!$" }, { "id": "t2", "text": "$(n-k)!$" } ],
  "slots": [ { "id": "num", "label": "numerator", "accepts": ["t1"] }, { "id": "den", "label": "denominator", "accepts": ["t2"] } ],
  "mode": "assign|order" }
```

`mode: "order"` uses one slot and grades the token sequence against `order: ["t1", "t2"]`.

Interchangeable tokens: with `"byText": true` tokens with the same text count as the same token (two `$x$` chips can go either way round); `"same": [["t1", "t2"]]` (or one list) names groups by id instead.

`mode: "boxes"` places the items of the screen's `boxes` canvas: the learner drags them between containers, with no tokens or slots of its own.

```json
{ "kind": "place", "mode": "boxes", "answer": { "hand": ["b2", "b3"] }, "ordered": false }
```

`answer` maps each container id that matters to the item ids it must hold (any order; `"ordered": true` for a row whose order matters); items not listed may be anywhere. Keys: the first item out of place (its item id). Instead of `answer`, `"count": { "hand": 2 }` asks only how many items a container holds (key `count-hand`), and `"free": true` accepts any arrangement once an item has moved (an explore task: it makes the canvas interactive for the explore rule).

`mode: "array"` orders the cells of the screen's `array` canvas: the learner drags cells along the row, and `answer` lists the opening cell ids in the order wanted (`["c2", "c0", "c1"]`, ids by opening index). Key: the first id out of place.

```json
{ "kind": "place", "mode": "array", "answer": ["c1", "c2", "c0"] }
```

In assign and order modes a token may carry `onPlace`, a canvas state patch applied while the token sits in a slot (or `{ "<slot id>": patch }` for one slot), over the canvas as it opened: dropping a `call` token into the position adds that leg to the payoff (`"onPlace": { "legs": { "c1": { "type": "call", "strike": 100 } } }`).

### `tap-regions`

```json
{ "kind": "tap-regions", "answer": ["r5c2", "r2c5"], "max": null,
  "wrong": [ { "id": "double", "set": ["r5c2", "r2c5", "r5c5"] } ] }
```

The canvas provides the regions (grid cells, venn regions, tree branches, area cells, table cells, boxes items, and number-line points by their point ids). The question line shows the running count. Optional: `wrong[].flash` (ids to flash on Show why), `countWord` (the noun in the count, on every canvas; default "shaded" on a grid, else "selected"), `only` (restrict tappable ids).

`only` limits what can be tapped; on a grid it takes set names as well as ids (`["col7", "row5"]`). The regions also include table rows (`tap: "rows"`), console lines (`l3`), vector arrows and points, graph edges (`tapEdges`), and whole sides of a pair (`tap: "sides"`, ids `left` and `right`).

Count mode, for "shade any 3 of the 4": give `count` instead of `answer`, and optionally `among`.

```json
{ "kind": "tap-regions", "count": 3, "among": ["c11", "c12", "c13", "c14"], "countWord": "parts" }
```

It is correct when exactly `count` regions are selected and, with `among`, every one is in `among`. The count reads "2 of 3 parts". Keys: a `wrong[]` id whose set matches, else the first selected id outside `among`, else `too-few` or `too-many`. Show solution selects the first `count` ids of `among`.

Ordered mode, for "tap the nodes in the order BFS visits them" or "tap the cells binary search reads": give `"ordered": true` with `answer` as the sequence. Each tapped object wears its number (1, 2, 3) on the canvas. It is correct when the taps match `answer` in order; keys: a `wrong[]` whose `set` matches the taps as a sequence, else the first tapped id not in `answer`, else the first missing one, else `order` (the right ids in the wrong order). Not combined with `count`.

### `order`

```json
{ "kind": "order", "lines": [ { "id": "s1", "text": "Write $P(A \\cap B) = P(A \\mid B)P(B)$" }, { "id": "s2", "text": "..." } ], "answer": ["s1", "s2", "s3"] }
```

Lines are shuffled on render. Per-line marks after grading. `"same": [["s2", "s3"]]` (or one list) makes lines interchangeable among their places, for independent steps of a derivation: any order of `s2` and `s3` in those two places is correct. `"distractors": ["d1", "d2"]` lists lines that must be left out (a flawed proof step, a wrong justification): include them in `lines`, leave them out of `answer`, and give each a `why` (shown as the feedback when the learner uses it). Each line gets a cross that moves it to a "Left out" list. Using a distractor returns its id as the `byKey` key, leaving out a line that belongs returns `left-out`, any other mistake the id of the first misplaced line as before. `same` and `distractors` combine.

### `table`

```json
{ "kind": "table", "columns": ["x", "P(X=x)"], "rows": [ ["0", { "edit": true, "answer": 0.25, "tol": { "abs": 0.001 } }], ["1", "0.5"] ] }
```

A cell whose `answer` is text (`"True"`, `"AAPL"`) is graded as text, ignoring case and spaces at the ends, with no `tol`; `accept: ["T", "yes"]` lists other spellings.

A cell may name its own wrong answers: `"wrong": [{ "id": "used-mean", "value": 0.12, "tol": { "abs": 0.005 } }, { "id": "linear", "text": "O(n)" }]`; when the first wrong cell matches one, the key is that id (a `byKey` line can name the slip). An answer written `O(...)` (or with `"compare": "bigO"`) is compared as big-O: the `O`, spaces, case, `*` and the log base are ignored, so `n log n`, `O(N log N)` and `O(n*log2 n)` all match `O(n log n)`, and `1` matches `O(1)`. `"deps": ["r1c2", "r2c1"]` (canvas ids) highlights those cells on the screen's canvas while the cell has focus, for filling a DP table beside its grid. A cell with `bind` writes what the learner types to the canvas as they type (`cells.r2c3` on a grid, `p.a-b` on a tree branch, `values.<category>` on bars and `points.<id>.y` on a plane, the last two as numbers).

### `manipulate`

An authored state graph. The learner taps an operation; the display animates to the next state.

```json
{ "kind": "manipulate", "start": "s0", "target": "s3",
  "states": {
    "s0": { "tex": "2x + 3 = 11", "ops": [ { "label": "Subtract 3 from both sides", "to": "s1" }, { "label": "Divide both sides by 2", "to": "s0b", "why": "Dividing now leaves a fraction on the left; clear the 3 first." } ] },
    "s0b": { "tex": "x + \\tfrac{3}{2} = \\tfrac{11}{2}", "ops": [ { "label": "Subtract 3/2 from both sides", "to": "s3" } ] },
    "s1": { "tex": "2x = 8", "ops": [ { "label": "Divide both sides by 2", "to": "s3" } ] },
    "s3": { "tex": "x = 4" }
  } }
```

Any path reaching `target` is correct. An op with `why` is a recorded misstep (its `why` is shown on the next Check if the learner has not reached the target).

An op with `"reject": true` and a `why` (and no `to`) is refused in place: the chip shakes, its `why` shows under the chips and the state does not change, so a wrong step needs no dead-end state of its own. A `manipulate` whose states carry `canvas` patches is a canvas-bound widget for the explore rule.

A state may carry a `canvas` patch: as the learner steps through states, the screen's canvas takes each patch along the path (on top of the canvas as it opened), so each algebra step can animate the drawing, such as an elimination step on a `matrix`; Undo puts it back.

### `balance`

```json
{ "kind": "balance", "left": [ { "id": "x1", "kind": "unknown", "label": "x" }, { "id": "w3", "kind": "weight", "value": 3 } ], "right": [ { "id": "w7", "kind": "weight", "value": 7 } ],
  "moves": ["remove-both", "halve-both"], "target": { "left": ["unknown"], "right": [4] } }
```

`moves` may include `remove-both`, `halve-both`, `divide-both`, `remove-unknown-both`, `subtract-both`, `add-both`, `remove-item`. Keys returned: `unbalanced`, `unsolved`.

Signed pans, for `x - 3 = 8` or `7 - 3x = 22`: a weight may have a negative `value` (drawn dashed, lifting its pan) and an unknown block may carry `"coef"` (`-1`, `0.5`, `-3`; drawn as `−x`, `½x`, `−3x`). `subtract-both` and `add-both` take any amount, `divide-both` any non-zero number (negatives too), and after each move a pan shows one unknown block (the total coefficient) and one weight block (the total). A target `"unknown"` means $1x$ alone.

Several unknown kinds: give an unknown its own `label` and a hidden `value` (`{ "id": "y1", "kind": "unknown", "label": "y", "value": 2 }`); it weighs that value, moves keep the kinds apart, `remove-unknown-both` shows one chip per label, and a target names an unknown by its label (`"left": ["unknown", "y"]` is $x + y$; `"unknown"` is always the first unknown's label).

```json
{ "kind": "balance", "left": [ { "id": "w7", "kind": "weight", "value": 7 }, { "id": "x", "kind": "unknown", "coef": -3 } ], "right": [ { "id": "w22", "kind": "weight", "value": 22 } ],
  "moves": ["subtract-both", "divide-both"], "target": { "left": ["unknown"], "right": [-5] } }
``` The `target` must be reachable from the starting pans with the listed moves (at most six): the playthrough's correct answer is the shortest such sequence, found by the engine. For `drag-point` on one-dimensional canvases (number-line, circle) `target` is a number (x or angle) and `wrong[].region` may be `{ "x": [a,b] }` or `{ "angle": [a,b] }`; default `tol` is 0.25.

### `sketch`

```json
{ "kind": "sketch", "control": 4, "target": "max(x - 100, 0)", "xRange": [80, 120], "band": 2 }
```

The learner drags control points of a curve on the `plane` canvas; graded on sampled x against the target function within `band` (y units). The control points are evenly spaced over `xRange`; Show solution (and the playthrough) puts each one on the target curve, so choose `control` and `band` so that the smooth curve through those points stays inside the band (a kink between two control points can leave it).

### `code`

```json
{ "kind": "code", "language": "python", "starter": "def max_drawdown(prices):\n    ...\n", "examples": [ { "call": "max_drawdown([100, 90, 95])", "expect": "0.1" } ],
  "tests": [ { "call": "max_drawdown([100, 90, 95])", "expect": "0.1", "compare": "isclose" } ], "how": "Submit runs 8 hidden tests. Each answer is accepted when math.isclose(actual, expected, rel_tol=1e-9)." }
```

`compare` is `isclose`, `equal`, `fraction`, `stdout` or `raises` (both below). `isclose` and `equal` compare NumPy arrays, pandas Series and nested lists element by element (through `tolist()`), so `expect: "[[0.5, 1], [2, 3]]"` works for a 2 by 2 array. At most 15 tests. Tests run in the Pyodide worker with a 5 s budget each; `budget` on the widget (ms) adds to a run's limit, and code that imports numpy, pandas, scipy or matplotlib gets 30 s extra without one, so the first package load is not charged against the tests. Packages load from the code's own imports, in script mode too.

`isclose` also compares complex numbers: a function may return a `complex`, a NumPy complex scalar or array, and `expect` is a Python expression such as `(0.5-0.5j)` or `[1+1j, 2-2j]`; the test is `cmath.isclose` with the same `tol` (default relative 1e-9, absolute 1e-12). A real `expect` against a complex result compares as a complex number with imaginary part 0. Without this, split the value in the call (`[w.real, w.imag]`) as before.

**Tolerance and time per case.** A case may carry `"tol": { "rel": 1e-6 }` or `{ "abs": 0.005 }` (or both, either one alone means the other is 0) for `isclose`; the row reads "Expected 10.45 (within absolute 0.005)". Use it for simulations, scikit-learn scores and tiny values (`7.6e-24` with `{ "rel": 1e-6 }`), instead of rounding in the call. Each case has its own time limit: 5 s, plus the case's own `budget` (ms), else the widget's `caseBudget`, else the widget's `budget` again (or the 30 s that heavy imports get). Loading the code has 5 s plus `budget`. A case that runs past its limit is reported on its own row ("Stopped after 5 s on this test"), and the later cases did not run, so a quadratic attempt stops after one case instead of waiting for the whole run; give a fast-path case a small `budget` and a large input to catch slow but correct code. `solution` is the code Show solution puts in the editor, which the playthrough checks against the tests; give it on every code widget.

Any case may carry `setup`, a line of Python run just before `call` (`{ "setup": "prices = [100, 90, 95]", "call": "max_drawdown(prices)", "expect": "0.1" }`), so the call reads cleanly. `"compare": "raises"` passes when the call raises the named exception or a subclass of it: `{ "call": "parse_price('abc')", "compare": "raises", "expect": "ValueError" }`; the result reads "raised ValueError" or "no error, the value was ...". In script mode a raises case without `call` checks the whole program (with its `stdin`). `argv: ["prices.csv", "5"]` on a case runs the program as `python3 main.py prices.csv 5` (`sys.argv`), and puts the widget in script mode.

**Hidden code around the learner's (`prelude`, `postlude`).** `prelude` is Python run in the learner's namespace before their code, and `postlude` after it; neither shows in the editor, and the learner's line numbers stay their own. Use them for helpers and data the exercise needs, or a runner that reports on the learner's tests. The learner's source is available as `__learner_source__` (a string) to the prelude, the postlude and every test call and `setup`, with or without a prelude, so a postlude can write it to a file and run a tool on it, and a test can check it directly: `{ "call": "'sorted(' not in __learner_source__", "expect": "True" }`. A postlude flag works too (`NO_SORTED = 'sorted(' not in __learner_source__`, then a case on `NO_SORTED`). There is no shared tree helper library: a lesson that needs `Node`, `build` and `to_list` defines them in its prelude. Real pytest loads in the browser: this postlude runs the learner's tests and leaves the exit code in `RESULT` (0 when every test passes):

```json
"postlude": "import pytest as _pt\nopen('test_mine.py', 'w').write(__learner_source__)\nRESULT = int(_pt.main(['-q', '-p', 'no:cacheprovider', 'test_mine.py']))\n",
"tests": [{ "call": "RESULT", "expect": "0" }]
```

To check that the learner's tests catch planted bugs, the pytest course's level 2 screens share one postlude (copy it from `pytest/l5-empty-one-many.json`) that defines `run_tests()` (runs pytest on the learner's file and prints its report: an example `{ "call": "run_tests()", "expect": "0" }`), `outcome(fn=planted)` (`"passed"`, `"failed"` or `"no tests"`, with that function swapped into the test module, output hidden), `count(test="test_x", fixture="prices")` (collected test cases, parametrised rows counted) and `is_fixture(f)`. A hidden case then reads `{ "setup": "planted = lambda prices: ...", "call": "outcome(simple_returns=planted)", "expect": "'failed'" }`. Each pytest run takes about half a second once the wheel is loaded.

In script mode both run on every case, around the program. Every run starts in a fresh, empty working directory, so files written by one run are gone in the next. `isclose` needs a real number: the text `"0.05"` fails it. In Pyodide's NumPy (2.0.2), `np.linalg.solve` and `np.linalg.inv` return `nan` for an exactly singular matrix instead of raising `LinAlgError`, so a `compare: "raises"` case cannot rely on NumPy's own singular-matrix error: have the learner's code check `np.linalg.det` and raise itself.

The first run that imports a package (numpy, pandas, pytest) fetches it once; the results panel says "Loading numpy, pandas" meanwhile, and that time does not count against the tests' limit. pytest works (`pytest.approx`, `pytest.raises`): call test functions from a `setup` line or a `call`. Python's `sqlite3` works too, but `Connection.backup()` hangs in Pyodide: copy a database with `dst.executescript("".join(src.iterdump()))` instead. If the untouched starter itself stops with an error, Check says the starter is not finished yet and folds the traceback away.

**Programs that print (script mode).** For a program rather than a function, give a case `"compare": "stdout"` and the printed text as `expect`; `stdin` (optional) feeds `input()`, one line per call:

```json
"tests": [ { "compare": "stdout", "stdin": "250\n262.5\n", "expect": "Return: 5.00%\n" },
           { "compare": "stdout", "stdin": "100\n90\n", "expect": "Return: -10.00%\n" },
           { "stdin": "200\n210\n", "call": "ret", "expect": "0.05", "compare": "isclose" },
           { "stdin": "1\n2\n", "call": "len(printed)", "expect": "1" } ]
```

As soon as any example or test is a stdout case or has `stdin`, the widget is in script mode: the learner's code runs afresh for every case (with that case's `stdin`, or none), so `input()` works and nothing leaks from one case to the next. A stdout case with `"lines": true` passes when every line of `expect` appears in the output in order (other lines, such as timings, may come between), and `"match": "took \\d+ ms"` when that regular expression is found anywhere in the output (expect may then be left out). Otherwise a stdout case compares the whole printed text, whitespace-normalised (trailing spaces on each line and blank lines at the start and end are ignored); add `"exact": true` to compare character for character. `input()` prompts are not part of the output, so `expect` holds only what `print` wrote. A `call` case in script mode is evaluated after that run, in its namespace, where `printed` is also defined: the printed lines as a list (so `len(printed)` and `printed[-1]` make good follow-up tests). When the tests run out of `stdin` lines, `input()` raises `EOFError` and the row says so. Results show the input, the expected output and what the code printed. Outside script mode, Run examples also shows anything the code printed as it loaded. Do not read the harness frame (`sys._getframe`) to get at printed output; the validator warns about it.

#### C++ (`language: "cpp"`)

With `"language": "cpp"` the learner's code is real C++17, compiled in the browser by clang 21 (YoWASP Clang, `@yowasp/clang@21.1.4-3`, with wasi-libc and libc++) and run as WebAssembly. Each Check compiles once, then runs every case as its own process, so a crash in one test does not hide the others. A starter with `#include` must say `"language": "cpp"` (the validator checks it). The same case shapes as Python apply, with these differences:

- **Function mode** (cases with `call`). `call` is a C++ expression (`"mean({1.0, 2.0, 3.0})"`), or a function name with `args`, a list of JSON values that become C++ literals: a whole number is an `int` (`long long` above 2,147,483,647), a decimal is a `double`, `true`/`false` a `bool`, text a `std::string`, and a list a braced list that converts to the parameter's `std::vector` (nested lists to `std::vector<std::vector<double>>`). Where inference is ambiguous (an overload, a template, a whole number meant as a `double`), give `types`, one per argument: `{ "call": "mean", "args": [[-5]], "types": ["std::vector<double>"], "expect": -5, "compare": "isclose" }`. Supported argument and return types: `int`, `long long`, `double`, `bool`, `std::string`, `std::vector<int>`, `std::vector<double>`, `std::vector<std::string>`, `std::vector<std::vector<double>>` (also any integer or floating type, `char`, `std::pair`, and other containers as lists). `expect` is a JSON value, not source text: `2.5`, `true`, `"APPL"`, `[[1, 4], [2, 5]]`. `isclose` compares numbers as Python's does (relative 1e-9) and lists element by element; `equal` is exact. A `void` call returns nothing (test it through `setup` and a follow-up expression). `setup` is C++ statements run before the call, in the same scope: `{ "setup": "std::vector<double> xs(1000, 99.5);", "call": "mean(xs)", "expect": 99.5, "compare": "isclose" }`. A row shows the expression, the expected value and what came back, with its C++ type on a failure ("Expected 2.5, got 2 (int)"). A `main` the learner writes is renamed in function mode, so it never clashes with the tests.
- **Script mode** (a `stdout` case, `stdin`, `argv`, or a `raises` case without `call`): the program is compiled as it is, with its own `main`, and run once per case; `stdin` is what `std::cin` reads. `stdout` cases compare the printed text, whitespace-normalised, or character for character with `"exact": true`. A C++ script-mode case cannot also have `call` (there is no namespace to evaluate it in) or `setup`.
- **`"compare": "raises"`.** `expect` names an exception type, with or without `std::` (`"std::invalid_argument"`); a base class matches too (`"std::logic_error"`). Without `expect`, any abnormal end passes: an uncaught exception, a crash (`assert`, `abort`, a libc++ check) or a non-zero exit status (`return 1;` from `main`). A thrown exception that is not caught ends the program with g++'s message (`terminate called after throwing an instance of 'std::invalid_argument'` and `what():`).
- **`prelude` and `postlude`** are hidden C++ placed before and after the learner's code in the same file (a `struct` the exercise needs, a helper the tests call). The learner's line numbers stay their own: compiler messages name `main.cpp:LINE`, a failing test's call is reported as `test N`, and hidden code as `prelude.cpp` or `postlude.cpp`.
- **Compile errors** show clang's message under the editor (with the source line and caret), and no test runs; an untouched starter that does not compile gets the plain "not finished yet" sentence with the message folded away. Warnings about the learner's code are shown above the results when the code compiled.
- **Limits.** Compile time does not count against the tests (the results panel says "Compiling..."); each case has 5 s (`budget` adds milliseconds per case), after which the run is stopped and the remaining cases are not run, and the compiler survives. Output is cut at 200,000 characters. Flags: `-std=c++17 -O1`, libc++ in its debug hardening mode, so `v[10]` on a 3-element vector stops with "libc++ Hardening assertion ... vector[] index out of bounds" rather than reading garbage. The stack is 8 MB; an overflow or a bad pointer is reported as a crash. There is no file system, no threads and no network. Exceptions can be thrown but not caught: the sysroot's runtime has no unwinder, so a `throw` always ends the program as an uncaught exception would, and `catch` blocks never run. Do not set exercises that rely on `try`/`catch` (say so in the prose if exceptions come up). At `-O1` an endless loop with no side effects is removed by the compiler (C++ allows it), as on a desktop build. `#include <bits/stdc++.h>` does not exist (libc++, not libstdc++).
- **Tolerance, flags and variants (pass 7).** `tol: { "rel": r }` or `{ "abs": x }` on an `isclose` case, as in Python. `"flags": ["-Wall"]` on the widget adds compiler flags: `-W...` (warnings show above the results), `-O0` to `-O3` and `-Os` (replacing `-O1`), `-DNAME` or `-DNAME=v`, `-UNAME`, `-ffast-math`, `-std=c++14` or `c++20`; any flag other than a warning turns the precompiled header off, so such a Check compiles in a few seconds. A case's `"defines": { "BUGGY": 1 }` is compiled ahead of the prelude, once for every distinct set of defines, so a hidden pricer can `#ifdef BUGGY` and a learner's test is run against version A and version B.

- **Complex results.** A `std::complex<double>` (or `float`, or a vector of them) can be a function's result; write `expect` as `{ "re": 0.5, "im": -0.5 }`, or a list of those; a plain number means imaginary part 0. `isclose` compares the distance in the plane, `|actual - expected| <= max(rel * max(|actual|, |expected|), abs)` with the case's `tol` (default relative 1e-9, absolute 1e-12); `equal` compares both parts exactly. The failing row reads `(5,5)`, like `std::complex` output. With `"testkit": true`, `CHECK_CLOSE(a, b, tol)` accepts complex values too.
- **Compile checks.** A case `{ "compiles": "Connection b = a;", "setup": "Connection a;", "expect": false }` compiles that snippet in a function after the learner's code (and postlude); it passes when it does not compile (`expect: true`: when it does), and the row shows the first `error:` line. No program runs for it. Use it for a `private` member written from outside, a deleted copy, a missing `const`.
- **Checks the harness can add.** `"signature": "double total_value(const std::vector<double>&, const std::vector<double>&)"` checks the learner's function has that type (a wrong parameter type gets one plain sentence before clang's message). `"leakCheck": true` counts every `new` and `new[]`: a block never deleted, or deleted with the wrong form, ends the run with exit status 1 and a message on stderr ("Memory leak: 1 block(s) from new[] were never deleted"); allocations the compiler can see are pointless are optimised away, so test a leak that escapes (stored in a struct, returned). `"testkit": true` provides `TEST(name) { ... }`, `CHECK(cond)`, `CHECK_CLOSE(a, b, tol)`, `run_tests()` (prints `FAILED name: ...` lines and "k of n tests passed", returns the number of failing tests) and `test_count()`, so a case `{ "call": "run_tests()", "expect": 0 }` grades the learner's tests; `REQUIRE_THROWS` cannot exist without an unwinder. `"files": { "pricer.h": "...", "pricer.cpp": "..." }` adds hidden files compiled and linked with the learner's `main.cpp` (which may `#include "pricer.h"`), for a real two-file build and the linker errors that come with it; the learner still edits one file.
- **Output.** A stdout case may use `lines: true` or `match` as in Python, so a program can print timings beside graded lines. When a stdout case fails, what the program wrote to stderr is folded under the row. When a case runs past its limit, what it printed so far is shown under "Printed before the error". In function mode, a `call` that indexes or reads a member of a returned temporary (`sort_book(v)[0].price`) is copied before the temporary dies, so it no longer reads freed memory.
- **Runtime notes.** A range-for over a braced list (`for (double x : {1.0, 2.0})`) needs `#include <initializer_list>` (directly or through another header) in libc++. Pointers are 4 bytes (wasm32): `sizeof(void*)` is 4 and `sizeof(std::vector<double>)` is 12, against 8 and 24 on a 64-bit desktop, and printed stack addresses are near 0x7fffe0; say so in a lesson that prints sizes or addresses. Undefined behaviour does not trap (a null read returns what is at address 0, a dangling read the stale value, a double `delete` runs on) and when clang can see it the code may compile to `unreachable` and crash, so whether it crashes depends on inlining: never use `compare: "raises"` for undefined behaviour; show sanitiser output in a `console` instead (there is no AddressSanitizer). Clocks are coarse in the browser (`steady_clock` in about 100 µs steps, `system_clock` in 1 ms steps, because the app is not cross-origin isolated), so a timing exercise batches work. A compile that fails because the precompiled header could not open a later `#include` is retried without it, so a postlude may include its own headers.

- **First load.** The compiler is about 26 MB over the wire (102 MB unpacked: a 73 MB `llvm.core.wasm` and a 30 MB headers-and-libraries tar) from jsDelivr, fetched once per browser cache, and takes 10 to 40 s to download and start on a fast connection; the first compile after that is slower (about 5 to 14 s) while Chrome optimises the compiler. Then a Check compiles in 2 to 5 s, and in about 1 s once the starter's `#include` lines have a precompiled header, which a second compiler builds in the background in the first half-minute on a screen. Keep the leading `#include` lines of the starter the ones the solution needs, so the precompiled header matches. Running a small program takes milliseconds.

## 4. Canvases

The binding reference for every canvas kind is the engine's own documentation: `app/js/engine/canvas/README.md` (grid, tree, venn, number-line, boxes, area, balance, circle, table) and `app/js/engine/canvas/README-B.md` (plane, bars, distribution, scatter, series, walk, matrix, vectors, complex-map, graph, array, payoff, orderbook, space). Read the entry for a kind before using it; the table below is the summary and the READMEs win where they differ. Id conventions that differ by kind: grid and area ids are one-based (`r5c1`), table and matrix ids are zero-based (`r0c0`, `A-0-1`), scatter `p{i}` and walk `path{i}` are zero-based, bins are `b{i}`, array `c{i}` uses the displayed index.

`canvas: { "kind": ..., "params": {...}, "state": {...}, "enter": {...}, "controls": [...] }`. `enter` is a state patch applied 350 ms after the screen enters (use it for the "watch the space shrink" moment). Every kind also accepts `state.selected` (the current tap selection), `state.highlight` and `state.caption`. `params` fix the drawing; `state` is the initial state and the thing `explain.canvas`, `demonstrate.steps[].canvas` and `showWhy` patch. `controls` are explore-only sliders bound to params: `[{ "bind": "p", "min": 0, "max": 1, "step": 0.05, "label": "p", "start": 0.5, "format": "fraction" }]`. Where the canvas has its own binds (number-line: a point id moves that point; circle: `angle`; area: `split`, `split.rows`, `split.cols`, `grid`, `grid.rows`, `grid.cols`, `shade`) they are used; otherwise a plain `bind` sets `state.params[name]` and a dotted one such as `strike.c1` sets that state path. A control can also move one item of a list by id: `"bind": "points.p1.x"` (plane, number-line, any kind with `points`). On every kind a name the canvas does not know itself (not a number-line point, not the circle's `angle`, not an area `split`, `grid` or `shade`) is a free parameter in `state.params`, for a `derive` block to read. `start` is optional: given, it is the slider's opening value and it is applied to the canvas when the screen opens; left out, the slider opens at the bound value's current value (the point's x, the current split, the param), else at `min`. `format: "fraction"` shows the readout as a fraction (0.375 reads 3/8), `"percent"` as a percentage (37.5%); `decimals: 2` fixes the places shown whatever the step (sliders take it too). A bars canvas binds a category label to move that bar, or any other name to set `state.params[name]` for a `derive` block to read (one control driving every bar). `"scale": "log"` (with `0 < min < max`) moves the slider in powers of ten: stops at 1, 10, 100, 1000 (`perDecade: 3` adds stops between them, rounded to 3 significant figures) and the readout shows the value, not the exponent. `"stops": [1, 2, 4, 12, 52, 365]` moves a control through those values only (the readout shows the value); `"options": ["logistic", "k-NN, k = 3"]` is a categorical control, a row of chips that binds the index 0, 1, ... (put the names in the chips, not the caption); `"frames": [patch, patch, ...]` (with optional `frameLabels`) is a slider through authored state patches, each applied over the canvas as it opened (a key a frame leaves out goes back to its opening value), so "slide through the folds" is data rather than nested ternaries in `derive`. Controls work on every screen type, not only explore: on a problem, ladder or trap screen they move the canvas and grading never reads them, so a slice slider can sit beside the task on each screen of a ladder (each screen opens at its own `start`). `canvas.maxHeight: 220` (pixels, 120 or more) caps the drawing's height: it scales down, centred, so a `table` widget below a tall canvas stays in view on a laptop. Ids below are the highlightable element ids.

`derive` links values and captions to the state, re-evaluated after every patch, drag and control: `"derive": { "p2.x": "0.8 * p1.x", "caption": "Change: {{round((p1.x / 50 - 1) * 100, 1)}}%" }`. A target is an item property by id (`p2.x`), `values.<label>` on bars, `params.<name>`, `caption` or another state key; an expression uses item ids (`p1.x`), param names, top-level numbers and `values`; a string target fills each `{{expression}}`. The full function set (the same everywhere a derive runs):

| group | functions |
|---|---|
| arithmetic | `abs(v)`, `min(a, b, ...)`, `max(a, b, ...)`, `sqrt(v)`, `pow(a, b)`, `floor(v)`, `ceil(v)`, `sign(v)`, `round(v, places)` (places default 0), `hypot(a, b, ...)` |
| exponentials | `exp(v)`, `log(v)` and `ln(v)` (both natural), `log10(v)` |
| trigonometry (radians) | `sin cos tan asin acos atan`, `atan2(y, x)` |
| constants | `pi`, `e` |
| text for captions | `fixed(v, places)` ("3.50", trailing zeros kept), `money(v, symbol, places)` ("£1,234.50"; `money(v, "$")` for dollars) |
| sums and integrals | `sum(a, b, "term in k")` adds the term for whole k from a to b; `integral(a, b, "f(x)")` integrates numerically (Simpson, 400 strips); the formula is a quoted string in curve-formula syntax (`^` is a power there), and other values follow as name, value pairs: `integral(0, u, "a * x^2", "a", a)`; `fact(n)` is n! |
| tap selection | `selected` (the ids tapped so far, a list: `selected.length` counts them) and `total(selected)` (the sum of their numbers: a grid cell's shown text, a bar's height) |
| products and specials | `prod(a, b, "term in k")` (a running product), `lgamma(x)` (ln Γ), `erf(x)`, `Phi(x)` (the standard normal CDF); the same names work in curve formulas, where `prod(k, a, b, term)` is the product form of `sum` |
| matrices | `matmul(A, B)`, `matpow(P, k)` (k rounded), `vecmat(v, P)` (a row vector times P): `vecmat([1, 0], matpow(P, k))` is the chain's distribution after k steps |
| lookups | `params` (the canvas's params: `params.data[n]`) and every array in `params.params` by name (`data[n]`) |

Pass 7 adds to the function set (curve formulas too where they make sense): `erfc`, `normcdf(x, mu, sigma)` (alias `pnorm`), `normpdf` (alias `dnorm`), `qnorm(p, mu, sigma)` (aliases `PhiInv`, `NormInv`), all accurate to about 1e-14 relative (`Phi(-10)` is 7.62e-24); `solve(A, b)`, `inv(A)`, `transpose(A)`; `seq(a, b, step)`; list arithmetic `vadd`, `vsub`, `vmul`, `vscale(a, k)`, `cumsum`, `diff`, `rolling(a, w, "mean" | "sd" | "sum")`; seeded noise `randn(n, seed)` and `ar1(phi, n, seed, sigma)`; `obj("k", v, ...)` and `range(a, b)` to build an object (braces are not allowed). A single state object with an id (a plane's `area: { id: "A" }`) reads and writes by that id (`A.to`). A derive may write whole lists into state, so a series redraws from a slider (`"series.net.values": "cumsum(vsub(gross, vscale(traded, c)))"`) and a bars chart changes its categories (`"categories": "seq(0, n)"`).

`"let": { "pi": "vecmat([1, 0], matpow(P, k))" }` inside `derive` names intermediate values: they are worked out in order before the other rules, may be used by them (`"values.A": "pi[0]"`), and are never written to the state. On a `pair`, both sides' params are readable by name and the right side's win when the names clash, so give each side its own names (or read `left.a` and `right.a`). Outside quoted formulas `^` is JavaScript's bitwise XOR, not a power: write `pow(a, b)` or `a ** b` (the validator warns on `^` in a derive formula). A derive reads plain objects in state by name too (`riemann.n`, `line.m`, `transform.angle`) and an area's computed value as `values.<area id>`. Writing one component of an array keeps it an array: `"g.v.0": "a * 2"` changes the first entry of vector `g`, and `"g.v": "[a, b]"` sets the whole vector. Curve formulas (plane `expr`) may call `sum(k, 0, n, term)` for a partial sum with a slider on `n` (a Taylor polynomial) and `fact(k)`. Negative numbers, in captions and from `fixed` and `money`, print with the minus sign −. JavaScript's `(expr).toFixed(2)` and ternaries (`p1.x > 3 ? "high" : "low"`) work too; `=` and `;` are allowed only inside quoted strings (`p1.x > 3 ? "x = 3" : ""`). Details in README-B ("Linked state"). An explore screen whose only interaction is a point with `drag: true` is valid; pair it with `derive` for a live caption.

A `walk` canvas gives derive `values.stopped` (the mean of the walk at its stopping time), `values.stoppedSq`, `values.stoppedRatio`, `values.stoppedBankroll` (an overlay's mean at the stop; the name is `stopped` plus the overlay id), `values.runningMean` (list), `values.hits`, `values.hitsUp`, `values.hitsDown`, `values.tauMean` and `values.endMean` (the mean of the last step with no stopping), so a caption can read "{{fixed(values.stopped, 2)}}" beside sliders that move the barriers.

Pass 7 canvas options in brief (the READMEs have the details): tree `state.labels`, `state.values` (a value on any node), `state.dim`, `state.arrows`, `params.binary`; graph `lattice` (a recombining binomial lattice), `state.pointers`, `state.values`, KaTeX edge labels (edges are undirected unless `directed: true`); grid `mark` glyphs removed by `null` and centred with `pos: "centre"`, two-line cell text; plane `exprs` with `index`, `points` polylines, `steps`, `cells` regions, `hide` by group, `xAxis: "bottom"`, `xScale: "log"`, percent tick formats, `{y:.2f}` labels, `state.ci` (repeated confidence intervals); series `xValues`, `step`, sim `band`, `state.series`, `vlines`, tappable reference lines; bars catch-all `"4+"` categories, `state.categories`, `dataSets` with `index`; distribution `beta`; scatter groups, excluded points, more lines; array `steps`, `insert`, `remove`, labelled cells, `highlight.ranges`, tappable pointers; payoff legs in state, cash legs, several value curves; orderbook levels and quotes in state; boxes item `labels`, row drops, wrapped containers; console `compact`, `wrap`; number-line `tapIntervals`; pair `split`. `canvas.maxHeight` caps a table or console too (it scrolls).

| kind | params | state | ids |
|---|---|---|---|
| `grid` | `rows`, `cols`, `rowLabel`, `colLabel`, `rowHeads[]`, `colHeads[]`, `cells` (`"sum"`, `"pair"`, `"product"`, or a 2D array of strings), `compact`, `lattice: true` (points joined by streets, for lattice paths), `rowOffsets: [0, 0.25, 0.75]` (staggered rows) | `shade: { "<setName>": [ids] }` (sets are drawn with series slots in order; `{ "ids": [...], "colour": 3 }` picks one), `cells: { "r2c3": "5" }` (fills cells during an explanation), `paths: [{ "id": "route", "cells": [ids], "colour": 1 }]` (a route through the centres), `outline: "row5"|"col3"|"cross5"|[ids]`, `dim: [ids]`, `mark: { "<id>": "✓" }` | `r{i}c{j}`, path ids |
| `tree` | `levels: [{ "label": "First draw", "branches": [{ "id": "a", "label": "Red", "p": "3/5" }, ...] }]` or an explicit `nodes` tree with `children`, `leaves: { "<path>": "value" }`, `compact: true` (16 leaves fit), `rootLabel` (a labelled root pill) | `highlight: [paths]`, `shade: [paths]`, `show: "p"|"none"` , `collapse: [paths]`, `current: "a-b"` (a blue ring round that node) | branch paths like `a`, `a-b` |
| `venn` | `sets: ["A","B"]` or three, `labels`, `values: { "A": 20, "AB": 5, "B": 10, "none": 15 }`, `mode: "count"|"prob"` | `shade: [regions]`, `show: true|false` | `A`, `B`, `AB`, `C`, `AC`, `BC`, `ABC`, `none` |
| `number-line` | `min`, `max`, `step`, `labels` | `points: [{ "id": "p1", "x": 2.5, "label": "", "labelPos": "above", "drag": true }]` (a point is a plain dot unless `drag: true` or a drag-point widget moves it), `intervals: [{ "id": "i1", "from": 1, "to": 3, "open": [false,true], "labelPos": "below", "row": 1 }]` (`row` 0 sits on the axis, rows stack 16px apart; a side label on a ray goes above it at the edge), `arrows`; `colour` (series slot 1 to 6) on points and intervals, patchable (a drag handle stays manipulable blue); `labelPos` is `above`, `below`, `left` or `right` (default: above, or the side away from a jump arrow at that point; close labels stack); keyed patches `{ "points": { "p1": { "x": 3 } } }` work | point and interval ids; points are tappable for `tap-regions` |
| `boxes` | `containers: [{ "id": "urn", "label": "Urn", "items": [{ "id": "b1", "kind": "ball", "colour": 1, "label": "" }] }]`, `itemKind: ball|card|coin|slot|bag`, a container's `fill: "top"|"bottom"` (where its items start) (a `card` is as wide as its label, so file names fit; `bag`, alias `sealed`: a closed sack showing only its label, such as `"?"`; a coin shows H or T unless it has a `label`; without a `hand` container the band above the containers appears only while an item is drawn) | `draw: ["b1"]`, `move: { "b1": "hand" }`, `face: { "c1": "up" }`, `highlight` | item and container ids |
| `area` | `shape: "rect"|"square"|"circle"`, `grid: [rows, cols]` (a circle: `sectors`), `colSizes`, `rowSizes` (a negative size makes that strip's pieces subtracted: hatched with a dashed edge, for $(x + 5)(x - 2)$), `colLabels`, `rowLabels`, `labels` (edges `top`, `bottom`, `left`, `right`, and text on a piece keyed by cell id: `{ "c11": "$3n$" }`) | `shade: [cells or fraction]` (a half cell: `"c11/ul"`, `"c11/lr"`, `"c11/ur"`, `"c11/ll"`), `split`, `grid` (re-cuts the shape into a new grid), `diagonal: { "c11": "/" }` (or `"\\"`), `move: { "from": "c12", "to": "c31" }` (or a list: slides a copy of the piece, its place left empty), `colLabels`, `rowLabels`, `labels` (patchable), `point`; controls bind `split`, `grid` or `shade` | `c{i}{j}`, `c{i}-{j}` when either index is 10 or more |
| `balance` | `left`, `right` item lists as in the widget (signed weights and `coef` allowed), `x` | `left`, `right`, `params: { "x": 4 }` (the unknown's value: patchable, and a control can bind `x`) | item ids |
| `circle` | `radius`, `showSin`, `showCos`, `showTan`, `degrees: true|false`, `ticks`, `drag` (true: the point drags without a widget, for explore screens with a `derive` caption) | `angle`, `shade: "arc"|"sector"`, `drag` | `angle`, `sin`, `cos`, `tan`, `pt`, `arc`, `radius` |
| `plane` | `x: [min,max]`, `y: [min,max]`, `grid`, `axes: false` (a geometry figure: no axes, ticks or grid), `xTicks`/`yTicks: "integer"`, `xStep`/`yStep` (a tick and grid line at every multiple: 90 for degrees, 3 for months), `yScale: "log"` (with `money: "£"` for price ticks), `equal` (square units; with `height` the shorter range widens about its centre), `functions: [{ "id": "f", "expr": "x^2", "label": "f(x)", "domain": [a,b], "labelSide": "above|below" (alias `labelPos`), "labelOffset": [dx, dy], "labelAnchor": "start|end" }]` (labels keep clear of every curve and the axes; a `functions` patch by id keeps the authored `domain` unless it gives one), `params: { "a": 1 }` (usable in expr) | `points: [{ "id": "p1", "x": 1, "y": 1, "drag": true, "snap": 0.5, "label": "" }]`, `segments`, `tangent: { "f": "f", "x": 1, "side": "left|right", "lengthPx": 80 }` (at a corner of a piecewise function no tangent is drawn unless `side` picks a one-sided slope; `length` is in x units, `lengthPx` in pixels), `vlines: [{ "id": "v1", "x": 2, "label": "x = 2" }]`, `hlines: [{ "id": "h1", "y": 3 }]` (dashed reference lines), `polygons: [{ "id": "tri", "points": ["A", "B", "C"], "vertexLabels": ["A", "B", "C"], "colour": 2 }]` (filled shapes; points are ids or `[x, y]`), `angles: [{ "id": "th", "at": "B", "from": "A", "to": "C", "label": "$\\theta$", "right": false }]` (an arc, or a square mark with `right: true`), segment `labelOffset: [dx, dy]`, a point with `on: "f"` stays inside f's `domain`, points are tappable for `tap-regions`, `area: { "f": "f", "from": 0, "to": 2 }`, `riemann: { "f": "f", "from": 0, "to": 2, "n": 4, "rule": "left" }`, `vectors`, `params`, `highlight` | function, point, segment ids |
| `bars` | `categories: [...]` or `bins: { "min", "max", "width" }`, `yLabel`, `exact: [{ "x": "7", "y": 0.1667 }]`, `sim: { "trials": [10,100,1000], "outcome": "d6()+d6()", "seed": 7 }`, `showValues` with `decimals` or `money: "£"`, a category's own `colour` | `values: {cat: v}`, `highlight`, `ran: n` | category ids (`x7`; an object category `{ "id": "win", "label": "Win" }` keeps its own id) |
| `distribution` | `family`, `params: {...}`, `x: [min,max]`, `showMean`, `showSd` | `shade: { "from": a, "to": b }`, `params` | `mean`, `shade`, `x{k}` for pmf bars |
| `scatter` | `points: [[x,y],...]`, `x`, `y` labels, `fit: true` | `line: { "m": 1, "b": 0 }`, `residuals: true`, `highlight` | `p{i}`, `line` |
| `series` | `series: [{ "id": "px", "label": "Price", "values": [...] }]` (`null` leaves a gap), `yScale: "log"` (log-price chart, ticks at 1, 2, 5 times powers of ten), `x: "dates"|"index"`, `candles: false`, `money: "£"`, `decimals`; `state.drawdown: "money"` labels the absolute fall (for P&L that starts at zero) | `markers: [{ "id": "m1", "i": 30, "label": "peak" }]` (give `"y"` for a marker on a `null` gap), `shade: [{ "from": i, "to": j, "label": "drawdown" }]`, `window` | series and marker ids |
| `walk` | `steps`, `p`, `start`, `paths`, `drawn`, `barriers: [a,b]`, `lower`, `upper`, `stopAt`, `sim: { "seed": 1 }`, `model: "ou"` with `theta`, `mu`, `sigma`, `overlays: ["sq", "ratio", "bankroll"]` with `bankroll`, `stake`, `fraction`, `bet` | `run: n`, `showMean`, `showSpread`, `showHits`, `stopAtBarrier`, `showStopped`, `overlays`, `bet`, `highlight: [pathIndex]` | `path{i}`, `barrier-up`, `barrier-down`, `mean`, `mean-level`, `spread`, `stop-time`, `ov-{id}`, `stopped-{key}`, `stopped-ref` |
| `matrix` | `matrices: [{ "id": "A", "rows": [[1,2],[3,4]], "label": "A" }]`, `ops: ["×", "="]` | `highlight: { "A": { "rows": [0], "cols": [], "cells": [[0,1]] } }`, `pivot`, `rowOp: { "from": 0, "to": 1, "k": -3 }`, `cell` | `A-r0`, `A-c1`, `A-0-1` |
| `console` | `lines: ["$ pytest -q", "..F", ...]` (or `text` with newlines), `title`, `numbers: true` (line numbers) | `shade: { "<set>": [ids] }`, `tone: { "l3": "err"|"ok"|"muted" }`, `lines` (replace the text), `highlight`, `caption`; tap mode on lines | `l1`, `l2`, ... (one-based) |
| `vectors` | `x`, `y`, `vectors: [{ "id": "u", "v": [2,1], "label": "u", "labelPos": "end"|"mid"|"start" }]`, `points: [{ "id": "A", "x": 4, "y": 1, "label": "A", "labelPos": "ne" }]`, `grid` | `show: ["sum","projection","span","scale"]`, `scale: { "u": 2 }`, `drag: ["u"]` (origin-based vectors only), `basis`; tap mode on arrows and points | vector and point ids, `sum`, `proj` |
| `complex-map` | `f` (a formula in `z`: `+ - * / ^`, `i`, `pi`, `e`, `exp`, `log`, `sqrt`, `sin`, `cos`, `tan`, `sinh`, `cosh`, `tanh`, `conj`, `abs`, `arg`, `re`, `im`, `pow(a, b)`), `params: { "a": 1 }` (numbers usable in `f`, bound by controls), `x`, `y` (z-plane ranges, default `[-2, 2]`), `wx`, `wy` (w-plane ranges, default as `x`, `y`), `grid: "cartesian"|"polar"|"both"|"none"`, `gridStep`, `rStep`, `rays`, `unitCircle`, `curves: [{ "id", "z": "formula in t", "t": [from, to] }]`, `points`, `zLabel`, `wLabel`, `stack` | `f`, `grid`, `gridStep`, `rStep`, `rays`, `unitCircle` (patchable), `params`, `points: [{ "id": "p1", "x": 1, "y": 0.5, "label": "$z$", "drag": true }]` (`x`, `y` are the real and imaginary parts of z; its image f(z) is drawn in the w-plane), `curves`, `hide: [ids]` | `grid-x`, `grid-y`, `grid-r`, `grid-th`, `unit`, curve ids, point ids and `<id>-image` |
| `space` | `x`, `y`, `z` ranges (default -5 to 5), `equal` (equal units), `aspect: [a, b, c]`, `height` (240 to 640, default 420), `camera: { az, el, zoom }` (opening view, default az -60, el 25), `perspective` (0 to 1), `grid: "back"\|"floor"\|false`, `box`, `axes`, `ticks`, `axisLabels`, `params: { "a": 1 }` (usable in formulas), and the lists `points: [{ "id": "P", "p": [1, 2, 3], "label": "P", "drop": true }]` (or `at` a curve with `t`, or `on` a surface), `vectors: [{ "id": "u", "v": [1, 2, 3], "from": [0, 0, 0] \| pointId \| vectorId, "label": "$\\mathbf{u}$" }]`, `curves: [{ "id": "r", "x": "cos(t)", "y": "sin(t)", "z": "t / 4", "t": [0, 12.57] }]`, `lines` (polylines through `pts`), `surfaces: [{ "id": "s", "z": "x^2 - y^2", "x": [-2, 2], "y": [-2, 2], "n": 24 }]` (or parametric `x`, `y`, `z` in `u`, `v`), `planes: [{ "id": "cs", "span": ["u", "v"] }]` (or `normal` with `through` or `d`; a one-vector span is a line), `fields: [{ "id": "F", "F": ["-y", "x", "0"], "n": 5 }]` | `camera`, `show`, `hide` (ids; `axes`, `ticks`, `box`, `grid` too), `highlight`, `params`, and every list patched by id | item ids; tap mode on every object |
| `graph` | `nodes: [{ "id": "n1", "label": "A", "x": 0.2, "y": 0.3 }]`, `edges: [{ "from": "n1", "to": "n2", "w": 0.3, "directed": true }]`, `markov: true`, `layout: "ring"` (seats round a circle), `nodeRadius` (default: fits the longest label) | `visited: [ids]`, `current`, `highlight`, `distribution: { "n1": 0.5 }`, `labels: { "n1": "Alice" }`, `rotate: 1` (ring seats), `nodes`/`edges` patches (`{ "nodes": { "n4": { ... } } }` adds, `null` removes, both animate) | node and `e-n1-n2` ids |
| `array` | `cells: [5, 2, 9]`, `indexFrom: 0`, `mode: "array"|"stack"|"queue"|"linked"` | `pointers: [{ "id": "i", "at": 0, "label": "i" }]`, `highlight: { "range": [0,2] }`, `cells`, `swap: [i,j]` | `c{i}`, pointer ids |
| `payoff` | `legs: [{ "id": "c1", "type": "call"|"put"|"stock", "side": "long"|"short", "strike": 100, "premium": 3 }]`, `range: [80,120]`, `pl: true` | `strike: { "c1": 105 }`, `spot`, `highlight` | leg ids, `breakeven`, `spot` |
| `orderbook` | `bids: [[price, size]]`, `asks: [[price, size]]`, `depth` | `order: { "side": "buy", "size": 300 }`, `highlight: ["ask0"]`, `fills` | `bid{i}`, `ask{i}`, `spread` |
| `table` | `columns`, `rows`, `align` (a negative number, or text starting with one, prints with the minus sign −), `compact` (automatic above 6 columns) | `highlight: { "rows": [], "cols": [], "cells": [] }` | `r{i}`, `c{j}`, `r{i}c{j}` |
| `pair` | two canvases side by side: `left` and `right` (each `{ kind, params, state }`), `active` (the side canvas-bound widgets drive, default `left`), `stack: true` to stack them | patches take `{ "left": {...}, "right": {...}, "caption": "..." }` | either side's ids with a `left:` or `right:` prefix (`left:pt`, `right:P`); unprefixed ids reach both |

More options, each detailed in its README entry: plane `holes`, parametric and implicit curves (with `on` and `tangent`), hidden functions that still evaluate, point `tap: false` and `trace: true`, tangent `labelOffset`; series `title`, `dateFormat`, `fill: "below"`, a second y axis (`axis: 2`, `y2`), `margins`, marker `decimals`; bars `data` with a `binWidth` control and `truncate`; area `state.colSizes`/`rowSizes` (bindable `colSizes.0`), spanning labels `"c11-c16"`, `dim`; number-line arrow `side: "below"`; table `dim`; graph node `shape` and `tapEdges`; payoff `value` and `tangent` (delta); orderbook `spreadValue: false`; pair `tap: "sides"` and `shareMargins`; grid `revealAfterGrade`.

Added in integration pass 6 (README entries give the details): distribution families `hypergeometric` (`N`, `K`, `n`), `lognormal` (`mu`, `sigma`, with `showMedian`) and `discrete` (`values`, `probs`: a custom support); `cdf: true` draws the CDF (steps with closed and open dots); discrete axes follow the support as a slider moves `n` and tick every integer when there is room; `shade` may be a list (two tails, summed in the label), with bounds that are expressions in the params (`"mu - sigma"`) and `under: "<overlay id>"` to shade under an overlay curve; overlay params may be expressions (`"mu": "n * p"`) so an overlay follows the sliders; `observed: { x, label }` marker lines; `rug` (sticks at data values); `drag: true` gives shade handles without a widget. Bars: `groups` (two or more bars per category, a legend; a sim outcome `[X, Y]` fills them), `yScale: "log"`, `xAxis: "value"` with `state.transform: { a, b }` (aX + b slides along the axis), `state.cut: { at, side, colour, label }` (recolour every bar beyond a cut; bind `cut.at`), `hlines`, `curves: [{ id, expr, label, shade: { from, to } }]` over the bars (the expression reads params and `w`, the bin width), `showMean` and a draggable balance point `state.pivot` (with `drag: true`, or a drag-point target as a number). Simulations (bars `sim`, series `sim`): `outcome` reads params and `state.params` by name (a slider on n re-runs the seeded stream), `let: { xs: "sample(10, n())" }` binds names per trial, `filter` discards trials (the count says how many), and `sample`, `mean`, `var`, `varp`, `sd`, `sum`, `len` (of a list, or `mean(10, n())` for ten fresh draws) and `tstat(k)` are available; a series may be `sim: { outcome, n, running: "mean" | "varp" | "var" | "sd" | "sum" | "none" }` (a running statistic), with `xScale: "log"` and `xStep`, and controls bind `reveal`, `revealAt` (an index) and `markers.<id>.i` (a marker with `i: "reveal"` rides the reveal). Grid: `population: 1000` with `state.groups: [{ id, count, colour, label }]` (each group one tap target), `margins: true` (row and column sums outside the cells; `state.margins: false` hides them until a patch), set names in tap-regions `answer` and `among` (`cross2`), a dimmed blank cell greys. Tree: `state.p` and `state.leaves` patch probabilities and leaf values, first-level labels move off the root on fans of three. Table widget: a cell's `unit: "%"` (answer as a fraction, typed as a percentage) and `bind: "p.a-b"` (what the learner types is drawn on the canvas as they type; on a tree, tapping the branch focuses the cell; `bind: "cells.r1c2"` fills a grid cell). Plane: `zeroOutside: true` (a density is 0 past its domain), `rug: { x, on, sticks }`, `yAxis: "left"`, a long `xLabel` goes below the ticks (`xLabelPos`). Walk: `model: "markov"` (`states`, `P`, `start`), `xStep`, per-barrier hit counts (`{up}`, `{down}` in `hitsLabel`), and a control `{ "reseed": true, "label": "New paths" }`. Number-line `scale: "log"` and `"log-odds"` (with `format: "percent"`). Balance move `remove-unknown-part` (take E/2 from both pans). Scatter `sim: { n, rho, seed }` (a control on `rho` re-correlates the cloud; `values.r` is the sample correlation). Graph: edge `loopAngle`, node `valueSide`, and the frame narrows to a phone's column so labels stay 12px. Array `wrap`. Boxes `size: "large"` and a `door` item. Payoff: tap targets `strike-<leg>` and `breakeven`, `drag: "spot"`, `showTotal: false`, leg `labelAt` and `floor: false`. A capital I beside l, I or 1 in canvas text is drawn with serifs. The `slider` widget binds through the canvas exactly as `canvas.controls` do (a bars category moves its bar).

Added in integration pass 5 (README entries give the details): plane contour families (`{ "contour": "x^2 + y^2", "levels": [1, 4, 9] }`, each level labelled; `levelLabels: false`), a heat map (`{ "heat": "x*y", "range": [lo, hi] }`, drawn behind everything), `labelAvoid: false` on background curves, `labelAt` (a label held at a chosen x), `state.view: { "x": [..], "y": [..] }` and `state.zoom: { "at": "P", "scale": 4 }` (bindable `zoom`), `domain` ends that are parameter names or expressions (`["0", "b"]`), polar areas (`{ "polar": "1 + cos(theta)", "from": 0, "to": "pi" }`), sector polygons (`sector: { cx, cy, r1, r2, theta1, theta2 }`), polygon `glyph: true` (an F that shows orientation flips), `hidden: true` points (derive-driven vertices with no dot), `riemann` as a list with stacked sum labels, and tap targets on areas, polygons and Riemann rectangles (`riemann-0`); tangent `length` spans x units; tree `branching` (a control on `branching.1` sets how many branches each node of that level shows) and automatic label staggering on crowded trees; series `hlines: [{ "id", "y", "label", "dashed" }]`; bars `dim` (state, or `dim: true` on a category); grid `selected` and `total()` in derive, default shade colours that never match the tap-selection blue; scatter `curves` (an `expr`, parametric `x`/`y`/`t`, or `implicit`) and controls on `line.m`, `line.b`; vectors `angles`, chains drawn `from` other arrows to any depth, `lines` (several spans as bands), `segments` (no arrowheads), `head: false`, `lockTo` (a drag held to a line), `state.matrix` or `state.transform: { angle, shear, scale }` (a transformed grid, basis and unit square, bindable `m11`..`m22`, `angle`, `shear`, `scale`), distinct default colours; matrix highlight groups with colours (`{ "A": [{ "rows": [0], "colour": 2 }, { "cols": [1], "colour": 4 }] }`), `rowLabels`, `colLabels`, `scale` (a factor before the brackets), `bar: k` (an augmented bar before column k), KaTeX operators, `{{expr}}` live cells, widths measured from the rendered maths, and a pair of matrices that fits each side and stacks below 80% scale (`minScale` on any pair).

Engine breadth pass 2 (grading, items 429, 430, 433, 434, 437): an `expression` answer may be complex (`i`), a vector or a matrix, and may use `\min`, `\max`, a capital `N` or `D` and `\epsilon`; `order` takes `distractors`; `isclose` compares complex numbers in Python and C++ (section 3 has each).

Plane field layers (item 431; the plane README has every option): `field: { "id": "F", "P": "-y", "Q": "x" }` draws arrows of (P(x, y), Q(x, y)) on a grid, `slopeField: { "id": "S", "f": "x - y" }` short segments of slope dy/dx = f(x, y), and `trajectory: { "id": "T", "in": "F", "from": "P" }` traces the solution through a start by fixed-step RK4. Formulas use `x`, `y` and the plane's `params`, so a slider bound to a param redraws the field. `from` is the id of a point with `drag: true` (or one a `drag-point` widget moves): the curve redraws live as it moves, and `starts: [[x, y], ...]` draws fixed curves. Options: `normalise: true` (equal arrows), `colourBy: "magnitude"` with `range`, `grid`, `back: true` (also run backwards), `length`, `step`, `by: "arc"`, `maxSteps`. Arrow counts and steps are capped, so a field costs little on a phone. `derive` can read the forward end as `values.TEndX` and `values.TEndY`. Use `equal: true` when arrow angles must be true.

Engine breadth pass 2 (walk): overlay panels under the walk (`overlays`: `"sq"` for S_n^2 - n, `"ratio"` for (q/p)^S_n, `"bankroll"` with a bet rule, or `{ id, expr }` for any formula in `n`, `S`, `x`, `p`, `q`), the running average of the stopped value across seeded paths (`showStopped`), barriers that follow sliders (`lower`, `upper`) and a mean-reverting model (`model: "ou"`, sliders on `theta`, `mu`, `sigma`).

`vectors` and a matrix (item 435): `state.matrix: [[a, b], [c, d]]` (or `state.transform`) now acts on every vector, so one matrix moves all of them with the grid and the unit square; `fixed: true` on a vector keeps it still. A `derive` reads `matrix`, `m11` to `m22`, `det`, `trace` and `image.<id>` (the arrow as drawn), and may write `"matrix": "[[a, b], [c, d]]"` from sliders bound to params `a` to `d`. Dragging a head in the image plane stores the preimage. `complex-map` (item 432) draws a z-plane beside the image of a grid under f(z); a `derive` reads `p1.u` and `p1.v`, the real and imaginary parts of f at the point `p1`.

`space` (pass 8) is the 3D canvas: drag to rotate, arrow keys turn the view, a Reset view button returns it. Formulas are written as in `plane` (`x^2 - y^2`, `cos(t)`), with the variable named for the object (`t` for a curve, `x` and `y` for `z = f(x, y)`, `u` and `v` for a parametric surface, `x`, `y`, `z` for a field) and any name from `params.params` usable everywhere, so a slider (`bind: "a"`) redraws the picture live. Coordinates in `points`, `vectors` and `planes` may be formulas too (`"v": ["a", "b", "a + b"]`). `bind: "az"`, `"el"` and `"zoom"` turn the camera. `derive` reads items by id as usual (`u.v`), `camera.az`, and `values.P` for a point's resolved `[x, y, z]` (a point `on` a surface or `at` a curve included) and `values.u` for a vector's tip. Keep the picture light: the cells of all surfaces and planes together are held near 1,600 so dragging stays smooth on a phone. Give `equal: true` when the maths needs equal units (perpendicular vectors must look perpendicular), and leave a margin round the canvas on a phone, because a finger on the picture rotates it instead of scrolling.

A ladder may move between a table and a chart of the same numbers, or into or out of a `pair`; the validator warns only on other changes of canvas kind between ladder screens.

Every canvas accepts `state.highlight: [ids]` and `state.caption: "text"`. A `derive` block also runs in the Why? copy, after `explain.canvas` is applied, so derived points and captions match the explained state. On a `pair`, `derive` reads both sides (ids directly, or `left.p1` and `right.p1`) and writes `left:` or `right:` targets: `{ "right:P.y": "sin(angle * pi / 180)" }`; controls bind `left:angle` or `right:a`. Every patch (`state`, `explain.canvas`, `demonstrate.steps[].canvas`, a wrong answer's `canvas`) may change one item of a list by id: `{ "points": { "p2": { "x": 3 } } }` merges into `p2` and keeps the rest of the list. A new id adds an item, and `null` removes one: `{ "points": { "p3": null } }` (in the Why? copy too).

Two rendering limits to write around:

- Function expressions (plane `expr`, distribution and sketch targets) read like maths: `-x^2` is $-(x^2)$, `e` is Euler's number, `e^x` and `exp(x)` agree.
- Inline maths can sit inside bold: `**the mean $\\mu$**`.
- A bare `£` inside `$...$` renders in italic maths type. Write `\\pounds` or `\\text{£}` in the JSON (both draw the pound sign in the prose face) (for example `$\\text{£}12.50$`), or keep the amount outside the maths.
- Grid cell text (`params.cells` as a 2D array) is plain text and cannot hold KaTeX. Use Unicode where you need it: superscripts such as `2³`, `x²`, the minus sign `−`, `½`.

## 5. Quiz, level review, homework, exam and drill items

An item is a `problem` screen without hints: `{ "id", "difficulty", "skills": [...], "prose", "canvas", "question", "widget", "feedback", "explain" }`. Items in the quiz block of a lesson omit `skills` (they take the lesson's).

- **Quiz** (in the lesson file): 3 to 5 items, difficulty 2 to 3, one attempt each, no canvas interaction beyond static diagrams where possible (scaffold-free).
- **Level review** `review-<n>.json`: `{ "id": "review-1", "course", "level": 1, "items": [6 to 10 items] }`, difficulty 2 to 4, interleaving every lesson of the level.
- **Homework** `homework-<n>.json`: `{ "id", "course", "level", "dueDays": 7, "items": [6 to 12] }`, difficulty 3 to 5 with at least one 5, at least one `longform` item and at least one `code` item (code courses) or one `derive`-style `order`/`expression` item (maths courses). A `longform` item: `{ "kind": "longform", "prompt": "...", "model": "the full model answer in markdown with KaTeX", "rubric": [ { "points": 2, "text": "States the conditioning event" }, ... ] }` summing to 10. On the homework page the learner opens the model answer and the rubric with the Mark my answer button under the item; in a review, practice or redo set the Check button does it. Either way the working then locks and the learner ticks the rubric.
- **Topic exam** `exams/topic-<topic>.json`: `{ "id": "topic-1.5", "topic": "1.5", "name", "minutes": 60, "pass": 0.7, "skills": { "<skill>": "label" }, "items": [...] }`, 20 to 30 items at the 8.4 ramp (20% at 2, 50% at 3, 20% at 4, 10% at 5), every skill of the topic covered.
- **Stage exam** `exams/stage-<n>.json`: `{ "id": "stage-1", "stage": 1, "parts": [ { "kind": "paper", "name", "minutes", "pass", "items": [...] }, { "kind": "check", "name": "A ten-line Python script you wrote runs from the terminal" } ] }`.
- **Mock assessment** `exams/mock-<id>.json` (ENGINE-BACKLOG 453): a timed paper (or several, with self-ticked checks) that models a real online assessment or interview day. It is sat many times, so it earns no XP and keeps every attempt with a net score and a trend. It mixes topics on purpose, so the topic skill-coverage rule does not apply and `skills` on items is optional. Fields: `id` (`mock-` then kebab-case words, matching the file name), `name`, `style` (`trader`, `research`, `developer` or `strats`, which sets the colour), `models` (one plain line, up to 200 characters, saying what real test it models; shown as "Models ..." on the start card and on Review), optional `description`, optional `skills` (`{ id: name }` for the by-skill chart), and either `parts` (as a stage exam: papers and checks) or the fields of a single paper at the top level (`minutes`, `items`, and the paper fields below). Mocks are listed on Review under "Mock assessments" with the latest score, the best and a trend. Say "reported" on the intro for any format taken from candidate reports. `#exam/mock-<id>/<seed>` fixes the seed of generated items, for testing.
- **Paper fields** (on a mock paper, a stage-exam paper, or the top level of a topic exam; ENGINE-BACKLOG 450 and 451):
  - `scoring: { "right": 1, "wrong": -1, "blank": 0 }`: the marks for a right answer (above 0), a wrong one and an unanswered one (each 0 or negative). Default `1, 0, 0`. Marks may be fractions.
  - `pass` (a share of the most marks the paper can give, as before) or `passNet` (a net score, for example 55 for "80 in 8, pass on 55 net"); give one, not both. A mock paper needs one of them. `passNet` may not exceed the maximum.
  - `navigation: "forward"`: one question at a time, no navigator, no Mark, no Back, and no jumping ahead; each answer locks when the learner moves on. The default is `"free"`.
  - `skip: false`: the next question opens only once the current one is answered. With `navigation: "forward"` this is the no-return, no-skip test; with free navigation it only stops the learner moving on past an unanswered question (the validator warns). With `skip` left out on a forward paper, the button reads Skip on an unanswered question and the skipped question scores the blank mark.
  - The results page headlines the net score when any paper has wrong or blank marks (for example "6 of 14 net", "7 right, 3 wrong, 1 blank") and shows each question's marks. A paper with a short clock (under 20 minutes) turns amber for its last quarter instead of its last five minutes.
- **Generated items** (ENGINE-BACKLOG 452): an entry in a paper's `items` of the form `{ "generator": "arith", "mix": { "add": 1, "sub": 1, "mul": 1, "div": 1 }, "n": 80, "options": 4 }` expands, when the learner begins, to `n` single-choice items, in place among any authored items. The problems come from the Today warm-up generator and `content/warmup.json` (addition and multiplication, with subtraction and division as their reverses; the same problem never follows itself). `mix` is `{ operation: weight }` (all four equally if left out); a value may be `{ "weight": 1, "a": [2, 100], "b": [2, 100] }` to narrow the ranges, which go on `add` or `mul` and apply to their reverses. `options` is 2 to 6 answers (default 4). Each wrong option is a near miss: the reverse operation, a misplaced decimal point (times or over ten) or a slipped digit. Optional `difficulty` (default 3) and `skills`. `n` is 1 to 200. The seed is chosen per attempt, so a resat differs, and is stored on the attempt (`seed`). Generated items are for mock and stage exams (not topic exams) and never join the redo queue.
- **Timed sets** (ENGINE-BACKLOG 454, covering 129): `"timed": { "seconds": 480, "lockAtZero": true }` at the top level of a level review file shows a countdown and a live "Score n of m" in the set's header; the start card states the time. With `lockAtZero: true` the set ends at zero: an answer that is ready is checked, everything else counts as missed (it joins the redo queue as any miss does) and the summary says that time ran out. Without it (the default) the clock is a guide and the learner may carry on. `seconds` is 30 to 7200. `#practice/timed/<seconds>` runs a practice set against a locking clock (the Practice card on Review links to 8 minutes). The Interview practice deck does not take `timed` yet. Timed is not for homework (the validator refuses it) or exams (a paper already has `minutes`).
- **`tags` and `pace`** (ENGINE-BACKLOG 456 and 457). Both are optional on every kind of item (quiz, review, homework, exam, mock, bank) and on lesson screens; `pace` is also allowed on a drill file.
  - `tags`: a non-empty list of kebab-case family names, for example `["dice-ev"]`. The first tag is the item's family; any others only narrow it (at most four, no duplicates). A family is a kind of question (`dice-ev`, `fermi`, `coupon-collector`), not a skill. The validator refuses a non-list, an empty list, a name that is not kebab-case and a duplicate. The engine reads `tags` for two things: the **Interview practice** deck (a tagged quiz, review or homework item of a finished lesson joins the deck under its own schedule) and the **pace line** on results (slowest families). An item with no tag counts under its first skill, and a generated arithmetic item under `mental-arithmetic`.
  - `pace`: the seconds the question should take, a positive number (a warning above 1800). Nothing is graded by it. After a set, exam or deck, the results page says how many answered items took longer than their pace, and each question shows "34 s of 45 s pace".
- **Per-item timing** (ENGINE-BACKLOG 457). Seconds per item are measured in exams (topic, stage and mock) and in every set page (practice, weekly problems, level reviews, redo and the bank deck), and the running totals are kept for exams, practice and the bank deck (not for reviews, redo or homework): from when the question is shown to when it is checked in a set, and the time a question was open in an exam (moving back and forth adds up). The results page ends its note with one line, for example "Average 46 s a question, 6 min 06 s in all. Slowest families: regime-length 3 min 20 s, coupon-collector 70 s, dice-ev 18 s. Over pace: 1 of 8 (question 2, 3 min 20 s against 45 s)." Only answered questions count. The attempt of an exam keeps `itemSeconds` (one number per question), and `ZQ.state.timing.families` keeps a running count, seconds and over-pace count per family for a later view. Marks, XP, mastery and the pass mark never depend on time.
- **Interview question bank** `bank/<family>.json` (ENGINE-BACKLOG 456): a file of interview-style items that are not tied to a lesson. `{ "id": "<file name>", "name", "description" (optional), "items": [...] }`, 1 to 200 items; split a large file by family. Each item is an ordinary item (AUTHORING format above: `id`, `difficulty` 1 to 5, `question`, `widget`, `feedback`, `explain`; `skills` optional but, if given, real skill ids; `longform` allowed, `code` not) plus:
  - `tags`: required, the family first (the file name is not read, so one file may hold several families, as `bank/sample.json` does).
  - `role`: required, a list from `trader`, `research`, `developer`, `strats`: the roles that ask this kind of question.
  - `style`: required, one of `mental-maths`, `probability`, `brainteaser`, `market-making`, `statistics`, `finance`, `coding`, `behavioural` (another kebab-case word is a warning).
  - `source`: required, one plain line of up to 120 characters saying where the question comes from, for example "Original" or "Adapted from mm-games review 1". Shown under the question in the results.
  - `requires`: optional list of `"course/lesson-id"`. The item is drawn only when every named lesson is finished; the validator checks that each is a lesson of that course (written or not). The Review card says how many questions are still locked.
  - `pace`: optional, as above.
  The **Interview practice** card on Review (route `#bank`) deals a deck of 8: first the items whose schedule is due (oldest first), then new ones, taking one family at a time so families mix and no two neighbours share a family when it can be avoided. Each item has its own Leitner schedule in the learner's state (`ZQ.state.bank`): a new item starts in box 1; a right answer moves it up one box (1, 3, 7, then 30 days) and it returns after that many days; a miss sends it back to box 1, due in 1 day. A bank miss does not join the redo queue, so nothing is scheduled twice. Old saves have no bank data and load unchanged. The sample file is `content/bank/sample.json` (ten items adapted from level reviews, each answer checked twice); real banks are a content pass. Not built: SM-2 with a self-rated ease, folding in the weekly problems, `timed` on a deck, and a bank draw for exam papers (item E3).
- **Drill** `drills/<id>.json`: `{ "id", "name", "course", "skills", "difficulty", "brief": "markdown", "starter", "examples", "tests", "how", "solution" }` (the `code` widget fields plus a model solution shown after verification).

## 6. Voice and teaching rules

From `design-research.md` 9, binding:

- British English. No exclamation marks. No emoji. Sentences of at most 20 words.
- Second person for instructions, "we" for reasoning together.
- Puzzle first. Never state a rule before the learner has used it. Name a term only after it has been used.
- Derive rather than state. Every derivation line carries its justification. No "it can be shown".
- Every lesson has one trap (a `trap` screen) and one edge case somewhere in the ladder or quiz.
- Every distractor encodes one named misconception and its `why` names the learner's action.
- Explanations refer to the learner's action, three sentences at most, with a diagram state.
- Notation: random variables capitals, realisations lower case, vectors bold lower case, matrices bold capitals, `P(\cdot)`, `E[\cdot]`, `Var(\cdot)`, `\ln`, decimals in maths and percentages in prose only. Money is £ or $ consistently within a course.
- Transfer screens use real quant contexts: a bet, a price path, a portfolio, an order book, a dataset, a backtest, a signal.
- Honest about difficulty. Never praise the question. Never praise the learner beyond the sourced lines ("That's it.", "Correct.").
- Concreteness fades: the canvas is interactive early, static by the ladder's end, absent in the quiz where possible.
- Code lessons: explanations annotate only non-obvious lines; show the failing version beside the fix when the lesson is about a pitfall.

Sizing: a course has 3 to 5 levels of 4 to 6 lessons. Each level ends with a review and a homework. Size a course by its topic hours: about 60 h of topic per 12 lessons, within 12 to 30 lessons per course.

## 7. Validation rules (enforced by `tools/validate.mjs`)

Errors:

1. JSON parses; required fields present; ids kebab-case; lesson `id` matches the filename; `course` matches the folder.
2. Screens 8 to 12; at most one `title`; at most two non-task screens; `summary.ideas` has exactly 3; `quiz` has 3 to 5 items.
3. Every `problem`, `ladder`, `trap`, `transfer`, `derive` screen has `question`, `widget`, `feedback.correct`, `feedback.generic` and 1 to 3 hints in rung order.
4. Widget kinds and canvas kinds are known; required widget fields exist; `choice` has exactly one correct and every distractor has `why`; `multi` has at least one correct; `numeric` has a numeric `answer` and `tol`; `tap-regions` has `answer`, or `count` (a whole number no larger than `among`), and its `answer` and `among` ids exist in the canvas (for `grid`, `venn`, `area` with `c{i}{j}` or `c{i}-{j}` from 10 up, `table`, and `number-line` point ids); `drag-point` targets are `[x, y]`, a bare number on a number-line or circle, or `{ "on": f, "x": n }` naming a function of its plane, and `tol` is a number or `[dx, dy]`; a `pair` has a `left` and a `right` canvas, each checked as its own kind, and its ids carry `left:` or `right:`; list fields (`options`, `among`, `tokens`, `slots`, `lines`, `points`, `wrong`, `hints[].highlight` and list answers) are lists, and a field of the wrong shape is one error, never a crash; `expression` `form` is `expanded`, `factorised` or `simplified`; `place` in `boxes` mode names containers and items on its boxes canvas; `balance` `moves` are known and the `target` is reachable with them (the engine's own solver); `order` answer is a permutation of line ids; `place` slots accept known tokens; `manipulate` target is reachable from start; `code` has at least 3 tests, each a `call` with `expect` or a `compare: "stdout"` case whose `expect` is a string (`stdin` a string, `exact` a boolean, `argv` a list of strings), a `raises` case names an exception, `setup` is a string, and `printed` is used only in script mode. Canvas options checked too: a control's `scale` is `"log"` with `0 < min < max`; `canvas.maxHeight` is a number of 120 or more; series `hlines` is a list of `{ y }`; tree `state.branching` is a number, a list or an object; `sliders` has at least two sliders and an `answer` or a `check`; `order` `same` names real line ids; a `drag-point` `expr` target has `show`. `trade` (item 459): whole `seed` and `turns`, numeric `fair` and `value`, a counterparty (or list) of known type with its own fields (`scripted` has `trades`), cards inside the turns, exactly one of `benchmark` and `band`, and a `strategy` of one entry per turn that, played through the widget's own game, meets the target with no rule breaks (a warning when doing nothing already meets it); a `{{carry.name}}` reference needs an earlier screen with that `carry` (item 460).
5. Every `feedback.byKey` key is a key the widget can produce (this includes `form` for an `expression` with `form`, item ids for `place` in `boxes` mode, `too-few` and `too-many` for a `tap-regions` in count mode, and point ids for `drag-point`); every `hints[].highlight` id is a plausible id for the canvas kind.
6. `difficulty` 1 to 5 and within the range for the context; quiz items 2 to 3; review 2 to 4; homework 3 to 5 with one 5; exams at the ramp within ±10%.
7. `skills` exist in the course; every course skill is used by at least one lesson.
8. Copy rules: no `!` in prose, question or feedback; no emoji (plain symbols used as tokens are text, not emoji: ★ ☆ ● ○ ■ □ ▲ △ ▼ ◀ ▶ ◆ and the card suits ♠ ♥ ♦ ♣, unless written with the emoji selector U+FE0F); no "it can be shown"; no American spellings from a fixed list (color, center, favorite, analyze, optimize, behavior, modeling, labeled, math class... the validator ships the list).
9. KaTeX: every `$...$` is balanced; `\\` is escaped in JSON.
10. Strand (section 9): `strand` in `course.json` is "quant" or "pure"; `strandNote` is a non-empty string when `strand` is set, and an error without it.
11. Course: levels 3 to 5, lessons per level 4 to 6, every lesson file referenced exists or is listed in `--summary` as unwritten (warning, not error); `review` and `homework` files exist for every level (warning until written).

Warnings: prose over 60 words; a screen without a canvas in a `problem` before the ladder's end; a lesson with no `transfer`; a quiz with any interactive canvas.

Pass 7 rules. Errors: a case's `tol` that is not `{ rel, abs }` numbers; `lines` or `match` on a case that is not a stdout case, or a `match` that is not a regular expression; on C++ widgets, a flag outside the allowed set, `defines` that are not name to value, a compile check (`compiles`) with a `call` or a non-boolean `expect`, a malformed `signature` or `files`; `ordered` that is not a boolean or is combined with `count`; a refused `manipulate` step without its `why`; `place` in `mode: "array"` without an array canvas or with an `answer` that is not every cell id once; plane function entries with none of `expr`, `exprs` (with `index`), `x` and `y`, `implicit`, `contour`, `heat`, `points`, `steps` or `cells`, or with malformed ones; controls whose `stops`, `options` or `frames` are malformed. Warnings: an `explain.canvas`, an option's or `wrong[]` entry's `canvas`, or a control frame that holds a whole canvas (`kind` and `params`) instead of a state patch; an expression answer with a capital N or D (the maths engine reads them as its own functions); a C++ `expect` that is a number written as text, unless the case says `"text": true` (its call returns a `std::string`). Explore screens accept a `manipulate` whose states carry canvas patches, and `place` in `array` mode. Tap-regions answers on a plane may name polygons, angles, areas and segments; on a number-line, intervals with `tapIntervals`; a pair with a side whose ids the validator cannot list is not checked.

C++ widgets (`language: "cpp"`), the rules so far: at least 3 and at most 15 tests; `compare` is `isclose`, `equal`, `stdout` or `raises`; script mode (a stdout case, `stdin`, `argv`, or a whole-program `raises`) allows no `call` or `setup`; a value case needs `call` and a JSON `expect` (`isclose` needs numbers); `args` is a list of JSON values with the function name alone as `call`, and `types` one per argument; `budget` is 0 to 120,000 ms per case; `solution` and `how` are expected (warnings).

Engine pass 2 grading rules. Errors: `order.distractors` that is not a non-empty list of known line ids, each once; with `distractors`, an `order.answer` that is not a permutation of the other lines; a C++ value case `expect` that is not a number, a boolean, a string, a complex `{ re, im }` or a list of those. `byKey` keys: `length` on an `expression` whose answer is a vector or matrix; `left-out` on an `order` with `distractors`. The warning about a capital N or D in an expression answer is gone.

Engine breadth pass 2 canvas rules. Errors: a `plane` `field` without `P` and `Q`, a `slopeField` without `f`, a `trajectory` without `from` or `starts` or without a field layer to run in, `in` naming no layer, and `grid`, `spacing`, `length`, `maxArrows`, `colourBy`, `range`, `anchor`, `normalise`, `colour`, `step`, `back`, `by`, `maxSteps`, `arrow` or `dashed` of the wrong shape (warning: a string `from` or `starts` entry that is not a point id in `state.points`); on `vectors`, `state.matrix` that is not `[[n, n], [n, n]]`, `state.transform` with a non-number and a `fixed` that is not a boolean; on `complex-map`, `x`, `y`, `wx`, `wy` that are not `[min, max]`, `grid` outside `cartesian`, `polar`, `both`, `none`, `gridStep` or `rStep` not above 0, `rays` not a whole number, `unitCircle` or `stack` not booleans, a name in `params.params` that is not a number (or `[re, im]`) or is `z`, `i`, `e` or `pi`, an `f` or curve `z` that does not compile, a curve without `t: [from, to]`, a point without numeric `x` and `y`; on `walk`, an unknown `model`, a negative `theta`, `stopAt`, `stake`, `fraction`, `bankroll`, `maxBet`, `overlayHeight` or `drawn`, `lower` not below `upper`, a `bet` outside `fixed`, `double`, `fraction`, an overlay that is not `sq`, `ratio`, `bankroll` or an `expr` formula that parses, two overlays with one id, `state.overlays` or `state.showStopped` naming no overlay (warnings: `showStopped` without barriers or `stopAt`, or without several paths; overlays on a markov walk; `p` or `step` on a mean-reverting walk); on `space`, ranges, `aspect`, `height`, `perspective`, `grid`, `camera`, every list entry needing a unique string `id`, formulas that use a name outside their variables, the params and the curve-formula functions, and the shape of each object in `points`, `vectors`, `curves`, `lines`, `surfaces`, `planes` and `fields` (the README lists each).

Mock and timed rules (engine pass A). Errors: a mock file whose id is not `mock-` then kebab-case words, with no `style` from the four, no `models`, a `models` that is not one line of up to 200 characters, or a `topic` or `stage`; a paper without `minutes` or `items`, or (in a mock or stage exam) without `pass` or `passNet`; `scoring` with a key other than `right`, `wrong`, `blank`, a non-number, a `right` of 0 or less or a `wrong` or `blank` above 0; both `pass` and `passNet`, or a `passNet` above the most the paper can score; `navigation` other than `forward` or `free`; `skip` that is not a boolean; a generator entry with an unknown key, a generator other than `arith`, `n` outside 1 to 200, `options` outside 2 to 6, a `mix` naming an operation that `warmup.json` lacks, a bad weight or range, ranges on `sub` or `div`, or no operation with a weight; a generator in a topic exam; `timed` on homework, with a key other than `seconds` and `lockAtZero`, with `seconds` outside 30 to 7200 or a `lockAtZero` that is not a boolean. Warning: `skip: false` without `navigation: "forward"`.

Bank, tags and pace rules (engine pass B). Errors: `tags` that is not a non-empty list of kebab-case strings or holds a duplicate (on lesson screens, quiz, review, homework, exam, mock and bank items and drills); `pace` that is not a positive number (a warning over 1800); in `bank/<file>.json`: an id that is not the kebab-case file name, no `items`, a duplicate item id, a `code` item, a missing or empty `tags`, a missing `role` or a role outside `trader`, `research`, `developer`, `strats`, a missing or non-kebab `style` (a style outside the list is a warning), a missing, multi-line or over-120-character `source`, and a `requires` that is not a list of `course/lesson` references naming a lesson of that course. Copy rules apply to a bank item as to any item. The manifest lists `bank/*.json`.

## 8. A complete minimal example

See `content/courses/conditional/l3-shrinking.json` (the reference lesson, ported from the prototype) and `content/courses/conditional/course.json`.

## 9. Course strand: Pure maths and Quant

The maths breadth courses are tagged so the learner can tell what is needed to be hired from what is for the love of the subject. Two optional top-level fields in a course's `course.json`:

```json
"strand": "pure",
"strandNote": "Not needed to be hired. Research roles that hire maths PhDs, and reading proofs in papers."
```

- `strand` is `"quant"` or `"pure"`. Any other value is a validator error. A course with no `strand` is untagged and shows no badge (every course written before the breadth pass).
- `strandNote` names the roles in one or two plain sentences. It is required when `strand` is set, and an error without `strand`. It is the badge's detail: the tooltip, and the screen-reader text after the strand name.
- The app shows a "Pure maths" (violet) or "Quant" (amber) badge on the course card, the course page, the lesson start screen, and on a topic's chip row and topic exam chip (Learn and the exam list on Review). A topic or exam chip gets a badge only when every course in the topic carries the same strand; a mixed or partly untagged topic shows none.
- Topic targets: a topic's `exit` in `curriculum.json` shows as a "Target" line under the topic heading on Learn. A topic with no exam file in `content/exams/` shows "Topic exam, not written yet" (Learn and Review) instead of a button. A course with no written lessons opens its map as "Map only".
- Setting: You, Settings, Study plan, "Quant path only" (`settings.quantOnly`, saved with the other settings, off by default). When on, `ZQ.content.stages()` and `courses()` leave out pure courses and any topic whose courses are all pure, so Learn, Today, Review, the mastery map and the stage progress count ("n of m topics passed") skip them. `topic()`, `course()` and `stage()` still find everything, so a link, resume point or exam URL to a pure course keeps working. Stage hours still show the full curriculum figure. `ZQ.content.allStages()` and `allCourses()` ignore the setting.
- Passing a topic exam means the topic is "tested out": Today stops recommending that topic's courses and moves to the next topic, then the next stage, unless one of its lessons is open to resume. It is read from the saved exam attempts (`ZQ.content.topicPassed(id)`, `courseTestedOut(courseId)`), so nothing is stored per lesson, lesson `done` flags and progress stay as they were, and Learn still lists every lesson. A tested-out course is offered only when no other course has a written lesson left. Levels added to a topic after its exam was passed are therefore hidden from Today until the learner opens them on Learn. The Due queue is unchanged.
- For engine code: `ZQ.content.course(id)` carries `strand` (or `null`) and `strandNote`; `topicStrand(topic)` and `strandNoteOf(courseIds)` give a topic's strand and notes; `strandBadge(strand, note, cls)` returns the badge HTML.

## 10. Prep paths: "Interview prep" tags and the Prepare for page (ENGINE-BACKLOG 455)

Which lessons prepare for which assessment lives in one file, `app/content/prep.json`, not on the lessons. Firm facts go stale every cycle, so they are re-dated in one place; lesson ids never change; a path may name a lesson that is mapped in `course.json` but not written yet. Paths label lessons and list them in study order. They never unlock, lock or reorder anything.

```json
{
  "asOf": "2026-11-02",
  "paths": [
    { "id": "general", "name": "General interview prep", "kind": "general", "description": "One or two plain sentences.",
      "mocks": [],
      "steps": [
        { "ref": "mental", "priority": "must", "why": "One line, under 20 words." },
        { "ref": "puzzles/level-1", "priority": "must", "why": "..." },
        { "ref": "conditional/l3-shrinking", "priority": "should", "why": "..." } ] },
    { "id": "oa-trader", "name": "OA prep: trader", "kind": "stage", "stage": "oa", "track": "trader",
      "mocks": ["mock-oa-arith"], "steps": [] },
    { "id": "firm-optiver", "name": "Optiver", "kind": "firm", "track": "trader",
      "asOf": "2026-10", "source": "recruiting/l4-firm-by-firm", "reported": true,
      "mocks": ["mock-oa-arith"], "steps": [] }
  ]
}
```

- Top level: `asOf` (`YYYY-MM-DD` or `YYYY-MM`, required: when the mapping was last checked) and `paths`. No other fields.
- A path: `id` (kebab-case, unique), `name`, `kind`, optional `description`, optional `mocks`, `steps`, plus the fields of its kind. Unknown fields are errors.
  - `kind: "general"`: no `stage`, no `track`.
  - `kind: "stage"`: `stage` is `oa`, `interview` or `superday`, and `track` is `trader`, `research`, `strats` or `developer`, both required. One path per stage and track pair.
  - `kind: "firm"`: `asOf` (`YYYY-MM` or `YYYY-MM-DD`), `source` (a ref, usually the recruiting lesson the firm facts come from) and `reported: true` are required. `track` is optional.
- A step: `ref`, `priority`, `why`, and an optional `track` (for a firm that runs several roles; shown as a small role tag). Steps are in study order and the page shows them in that order.
  - `ref` is a course id (`mental`), a level (`puzzles/level-1`) or a lesson (`conditional/l3-shrinking`). A course or level expands to its lessons. A lesson that `course.json` lists counts even when its file is not written yet; the page shows it as "Not yet written".
  - `priority` is `must` or `should`.
  - `why` is one line of under 20 words, in the app's voice (British spelling, no exclamation marks, no em-dashes).
- `mocks` lists mock exam ids (`mock-` then kebab-case words). An id with no file yet is allowed; the page shows it as "Not yet written" and links the others to `#exam/<id>`.
- Validator errors: a `ref`, `source`, `stage` or `track` that does not resolve; a malformed id, date or mock id; a `why` of 20 words or more or with a copy-rule fault; a firm path without `asOf`, `source` or `reported: true`; a repeated ref or mock in one path; an unknown field; `stage` or `source` or `reported` on the wrong kind. Warnings: a firm path whose `asOf` is over 12 months old (re-check it and re-date), a path with no steps, a lesson that two steps of one path both cover. `node tools/validate.mjs --prep <file>` checks a scratch copy instead of `content/prep.json` and leaves the manifest alone. When `prep.json` is valid it is listed in `content/manifest.json`.
- Where it shows:
  - A lesson on any path gets an "Interview prep" chip on its course map node; a course with any such lesson gets the chip on its Learn card. Never more than one chip. The chip's tooltip and the node's detail (card on desktop, sheet on a phone) list the stages and firms, for example "General, OA, superday. Optiver, SIG (reported, October 2026)." with a link to the path.
  - Learn has a "Prepare for an assessment or a firm" link under its heading, and Review has the same link in the "Mock assessments" card. Both open `#prepare`; `#prepare/<path id>` opens one path.
  - The Prepare for page lets the learner pick General, a stage with a role, or a firm. A path shows each step with Must or Should, done, in progress, not started or not yet written, its `why` line, the lesson count, then its mocks. A firm path says "Reported formats, as of <month year>" under its title, with a pointer to its source.
  - Path names are in the Today search (kind "Prepare"), so "Optiver" or "OA" finds them.
- "Quant path only" is unchanged: it hides pure courses from Learn as before, and a step that points at a hidden course still opens its map.
- For engine code: `ZQ.content.prep()` is `{ asOf, paths }` (empty when there is no file); `prepPath(id)`, `prepSteps(path)` (each step with `lessons: [{ course, id, level, name, written }]`), `prepRefLessons(ref)`, `prepFor(course, lesson)` and `prepForCourse(course)` (the paths a lesson or course is on), `prepDetail(paths)` (the line above) and `prepChip(paths, cls)` (the chip markup, `''` for none). The page is `js/screens/prepare.js`, styled in `css/screens/prepare.css`; the chip is `.prep-chip` in `components.css`.
