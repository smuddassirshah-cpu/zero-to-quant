# ml-int level 1: performance task

- `homework-1.json` item 7 of 7, `h7-derive-tanh-layer`. Kind `derivation` (self-marked longform, no starter, no hints, no parts), difficulty 5.
- Objective (l1): "Derive the gradients of a two-layer network by hand and explain each step aloud." The level matches the verb rule on l1 ("Derive"); the kind follows the verb.
- Product: from an empty box, the matrix-form gradients of a two-layer tanh network with squared loss for one example, $\partial L/\partial \mathbf{w}_2$ and $\partial L/\partial \mathbf{W}_1$, with a one-line reason per step. Rubric of five rows summing to 10; the first three rows (output gradient, last weights, tanh gate) are `required`; the bias gradients are marked optional in the prompt.
- Overlapping screens: l1 screens 2 to 6 work the same steps on a ReLU network with numbers, and screen 6 orders the matrix-form lines. The task changes the gate to tanh, adds biases, asks for the derivation from a blank box with reasons, and gives no lines to order. Homework item 1 (`mlp_backward`, code) checks the same gradients numerically on a batch.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; no `[ai-mutants]` or `[source-ban]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/ml-int python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans.
3. Numbers script: `node tools/run-number-scripts.mjs --python <venv>/bin/python --only ml-int-L1`: 1 passed (strict coverage, 0 uncovered).
4. Playthrough: `node tools/playthrough.mjs --set ml-int/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: all passed, both longform items marked through the button.
