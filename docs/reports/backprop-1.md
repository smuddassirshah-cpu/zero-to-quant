# backprop level 1 (The chain rule on a graph): report

## Files written

All in `app/content/courses/backprop/`, skill `bp-chain` throughout, £ for money.

| File | Screens / items | Code |
|---|---|---|
| `l1-expression-as-graph.json` | 9 screens, 3 quiz items | `forward_pass(a, b, c, f)` |
| `l2-local-derivatives.json` | 9 screens, 3 quiz items | none |
| `l3-multiplying-along-a-path.json` | 9 screens, 3 quiz items | none |
| `l4-every-gradient-by-hand.json` | 9 screens, 3 quiz items | `all_gradients(a, b, c, f)` |
| `review-1.json` | 10 items, difficulty 2 to 4, `pass: 0.8` | none (one `order`, one `expression`) |
| `homework-1.json` | 6 items, difficulty 3 to 5 (two at 5) | `grads_square_log` (4), `grad_of` (5); `order` item; performance task (derivation, longform, 10-point rubric) |
| `problems-1.json` | 3 problems, 12 parts, difficulty 3, 4, 5 | none |

Lesson shapes. l1: explore hook (four sliders drive the graph's values through `derive`), name by placing values into boxes (`place` with `onPlace` edges), forward table, a second expression with a power and an exponential, trap (a box that hides two operations), edge case (an input used twice), code, generalise, P&L transfer. l2: hook on the sum box, name the local derivative, product, one-input boxes, the course table, trap (output used for the other input), edge case (a constant input), generalise, bond transfer (limits l15's numbers). l3: nudge hook, frames slider walking back along the path, name gradient and backpropagation, $L$ against $a$ on a `plane` (slope 6), the other inputs, trap (adding along a path), edge case (a ReLU that is off), generalise (shared products), P&L attribution transfer. l4 (derive lesson): a fresh chain $L = (e^{wx + b})^2$ at $w = 2$, $x = 0.5$, $b = -1.5$; forward table, local-derivative table, the backward pass as an `order` screen with a distractor, two `expression` gradients, trap (a skipped box and a swapped product input), edge case (an input with no path), code, risk-report transfer (10,001 revaluations).

Graph canvas: computation graphs use the `graph` extension of engine item 1227 (`params.valueLines` with `state.values` and `state.values2`: forward value in ink, gradient as `g = ...` in slot 2), leaves as circles, one `rect` box per operation, `nodeRadius: 18`, laid out left to right. Edge width by weight is not needed in this level.

Generators: `/tmp/claude-0/-home-user-zero-to-quant/b2245dfe-6f55-570e-8d22-d9384c33129b/scratchpad/backprop-1/` (`common.py`, `gen1.py`, `gen1b.py`). Every code test `expect` is the model solution's own output.

## Gates

1. Validator: `node tools/validate.mjs` 0 errors (whole app); no backprop error. Remaining backprop warnings are advisory (`O2-long-sentence` on a few lines under 25 words, `O2-explain-answer` where the key is 0, the course map's unwritten later levels).
2. Voice: `VOICE_BASE=app/content/courses/backprop python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `docs/reports/backprop-L1-numbers.py` with the venv: 257 of 257 checks, exit 0. Route 1 is the rule (local derivatives along a path); route 2 is a central difference of the whole expression ($h = 10^{-6}$) or a direct recomputation. It runs `forward_pass`, `all_gradients`, `grads_square_log` and `grad_of` and checks every hidden-test expectation against central differences.
4. Playthrough: `node tools/playthrough.mjs --lesson backprop/l1..l4 --set backprop/review-1 --set backprop/homework-1 --problems backprop/problems-1 --local-cdn <pkgs> --mobile`: all passed at 1280 and 440 (each lesson 12 checks, quiz 3/3; review 10 of 10; homework 6 of 6, 29 of 29 marks, the longform marked by the button; problems 3 problems, 12 parts). Screenshots read; fixes made: derive parameter names (see backlog), node radius and layouts so value lines do not collide, short P&L node labels with the formulas in the caption.
5. Freshness: `fresh-check.mjs --file` on review-1, homework-1 and problems-1: 0 hits (two retold sentences in problems-1 reworded). `rubric-passes.mjs` on the performance item: rows 1 to 4 "can be left out: no", row 5 (optional) yes.

## Numbers stated (source: the numbers script)

- Course expression $L = (ab + c)f$ at $a = 1.5$, $b = -2$, $c = 4$, $f = -3$: $e = -3$, $d = 1$, $L = -3$; gradients 6, $-4.5$, $-3$, 1 ($\partial L/\partial e = \partial L/\partial d = -3$); a nudge of 0.01 in $a$ moves $L$ by 0.06; slider steps of 0.5 give 0, $-5.25$, $-4.5$, $-2.5$.
- $M = e^{xy} + z^2$ at $(0.5, 2, -1.5)$: 4.968282. Chain $L = (e^{wx+b})^2$: $p = 1$, $s = -0.5$, $q = 0.606531$, $L = 0.367879$, $2q = 1.213061$, $\partial L/\partial s = 0.735759$, $\partial L/\partial w = 0.367879$, $\partial L/\partial x = 1.471518$.
- Bond (limits l15): $P(0.05) = 95.67$, $P'(0.05) = -420.98$, 10 bp move $-0.421$. P&L book: returns 0.03 and $-0.02$, £5,000; $\partial(\text{P\&L})/\partial p_1 = 1{,}500$.
- Homework: $\partial V/\partial r = -409.37$ ($V = 81.87$); perf model $L = (e^{xy} - 1)^2$ at $(0.5, 0.8)$: $q = 1.491825$, $s = 0.491825$, $L = 0.241892$, $\partial L/\partial x = 1.173946$, $\partial L/\partial y = 0.733716$, nudge 0.011930 against 0.011739.
- Problems: 2, 4, 4, 0.08; $3\ln 2 = 2.0794$, 0.5, 1.5, 0.03 (exact 0.02985); £8,000, $-0.64$, $-6{,}400$, $-64$ (exact $-63.49$).

## Conventions

- Graph labels: leaves `a`, `b`, `c`, `f`; boxes `e = ab`, `d = e + c`, `L = df`. Canvas numbers use the minus sign U+2212; gradients show as `g = ...`.
- The l1 code function is `forward_pass`, not the brief's `forward`: `forward` is already a code name in `stat-learning/l17-a-small-network` (the brief bars reuse of a name of six or more characters).

## Proposed course.json change

None.

## Backlog

Three bullets under "Raised later (backprop level 1)" in `docs/BACKLOG-INBOX.md`.
