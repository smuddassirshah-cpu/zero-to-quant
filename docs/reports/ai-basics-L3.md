# ai-basics level 3 (One neuron): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l9-weighted-vote.json` | 10 screens (problem, explore graph with tap-to-switch inputs and a live sum, problem, 3 ladder incl. a table widget, trap, ladder, generalise, transfer), 13 min | 3 |
| `l10-firing-or-not.json` | 10 screens (problem tap the bars above 0, problem, ladder bars with a bias slider, 2 ladder, trap, code `weighted_sum`, code `fires`, generalise, transfer), 13 min | 3 |
| `l11-and-or.json` | 11 screens (problem `sliders` on a plane: make AND, problem table, 4 ladder, trap, ladder edge case, code `truth_table`, generalise, transfer), 14 min | 3 |
| `l12-xor-needs-two.json` | 9 screens (explore plane: try XOR, derive `order` proof with a distractor and `after` rules, problem two-layer table, ladder count, trap, ladder search count, code `xor_net`, generalise, transfer), 15 min | 3 |
| `review-3.json` | 10 items, difficulty 2 to 4, `pass: 0.8`, every item `ab-neuron` | |
| `homework-3.json` | 7 items, difficulty 3 to 5: code `exactly_two` two-layer (5), code `my_neuron` from a table (4), order with a distractor (3), numeric (3), numeric count of AND biases (4), choice (4), longform "explaining XOR" (5) | |
| `problems-3.json` | 3 chained problems, 15 parts: alert neuron (3; l9, l10), AND to OR (4; l10, l11), scaled XOR network (5; l9, l10, l12) | |

Stage 0, so no performance task. Threshold neurons only (fires when the sum is greater than 0); no ReLU, sigmoid or tanh. The graph's `edgeWidth` (the A3 extension, now in the engine) draws edge width and sign; `valueLines` was not needed.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. Warnings left on level 3 files: four "point hint usually highlights the canvas" and four "problem screen without a canvas" (text-only and code screens). None on review, homework or problems.
2. `voice-scan.py 35 --summary` on the course folder: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `docs/reports/ai-basics-L3-numbers.py` (venv): exit 0, 12,042 of 12,042 checks (every sum twice, the 9,261-neuron grid, 20,000 random neurons for the proof's conclusion). The 39 "check by hand" lines were read.
4. Playthrough with `--local-cdn`, desktop and `--mobile`, with `--why`: l9 13 checks, l10 13, l11 14, l12 12 (quizzes 3/3); review-3 10 of 10; homework-3 7 of 7, longform marked by the button; problems-3 15 parts, 25 typed slips routed. `grade-all.mjs --code`: 72 widgets and 6 code widgets, 0 failures. `fresh-check.mjs --file problems-3.json`: 0 hits; one same-course `chain-union` warning (parts 3 to 5 of the scaled XOR problem follow a review item and l12's count), kept: the network, weights and questions are new.

Screenshots read at 1280 and 440. The two-layer graph's crossing edge labels sat on top of each other at 440, so each neuron's weights and bias moved into its value line ("w 2, 2; b −1") and the edges keep their width and dash by sign.

## Numbers (each sum twice: products in exact fractions, and the bias plus the weights of the inputs that are 1)

- Umbrella neuron (2, 3, −1, bias −2.5): sums −2.5, −3.5, 0.5, −0.5, −0.5, −1.5, 2.5, 1.5; fires on (0, 1, 0), (1, 1, 0), (1, 1, 1). Bias −0.4: 6 fire. Bias −2: (1, 0, 0) and (0, 1, 1) sum to exactly 0 and do not fire. Smallest whole bias that always fires: 2 (bias 1 leaves the bag alone at exactly 0).
- AND (2, 2, −3), OR (2, 2, −1), NAND (−2, −2, 3), NOT (−2, 1), at least two of three (1, 1, 1, −1.5: 4 patterns), 5, 5, −7 is AND, 2, 2, −2 is AND under "> 0" and OR under ">= 0".
- XOR = AND(OR, NAND), checked on all four inputs; 9 numbers; the grid search tries $21^3 = 9261$ neurons and finds none.
- Transfers: credit score 23; fund score 0.04 (fires). Review: 0, −0.5, 2 fire, bias −4 for AND with 3, 3, NAND sum −1, 11 numbers, 2 fire after the bias change. Homework: exactly-two network (1, 1, 1, −1.5), (1, 1, 1, −2.5), output (2, −2, −1) on all eight inputs; 0.5; biases −5, −4, −3 for AND with 3, 3. Problems: alert sums with 3 firing, the weight change to −2 drops (1, 1, 1) to exactly 0; AND to OR by the bias alone; the scaled network (3, 3, −2), (−3, −3, 4), (3, 3, −5) is XOR, and an output bias of −2 makes it say 1 everywhere.
- Fresh against `stat-learning` l17: no ReLU, no corner set with its weights, no 4, −8, −2 output.

## Conventions

Inputs listed as (cloudy, rain forecast, bag) and corners in the order (0, 0), (0, 1), (1, 0), (1, 1). A neuron fires when its sum is greater than 0. "Numbers the network learns" is used for parameters, with one pointer to `stat-learning` l17.

## Proposed course.json change

None.
