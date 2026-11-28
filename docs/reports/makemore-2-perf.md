# makemore level 2: performance task

- `homework-2.json` item 7 of 7, `h-perf`. Kind `code` (Python), difficulty 4.
- Objective (l7): "Build the forward pass of an embedding, a tanh hidden layer and a softmax output, and count its parameters." The level matches the verb rule on l5 and l7 ("Build"); the brief puts the task on the l7 objective, kind `code`.
- Product: from a stub of three empty functions, `mlp_forward(params, X)` (logits for any block, embedding and hidden size), `mlp_loss(params, X, Y)` (mean cross-entropy in nats by log-sum-exp) and `n_params(block, emb, hidden, vocab)`. 6 hidden tests, 1 example: the parameter count for two sizes (6,097 and 22,059), a planted model of block 2, embedding 3, hidden 4 and 5 symbols (its output shape, and its loss within 1e-9), and the supplied trained weights (`makemore-mlp.json`) on the dev rows, below the bigram's 2.4514 and equal to 2.1609 to 4 places. No hints, no parts. `budget: 4000`.
- Mutants (ENGINE-BACKLOG 1263): four, each first failing the test it names: `W1` sized without the block (test 1), no tanh (test 4), the loss summed (test 4), biases left out of the count (test 1).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/makemore python3 docs/reviews/voice-scan.py 35 --summary`: 0 over 35 words, 0 lesson ids in code spans.
3. `<venv>/bin/python docs/reports/makemore-L2-numbers.py`: exit 0 (205 of 205); it runs the model solution against all 6 tests, the starter (fails) and the four mutants. `node tools/grade-all.mjs --code --file content/courses/makemore/homework-2.json --local-cdn <pkgs>`: 0 failures in Pyodide.
4. `node tools/playthrough.mjs --set makemore/homework-2 --mobile --local-cdn <pkgs>` (desktop and 440 px): all passed, "1 performance starter fail" as required.

- Overlapping screens: l7 screen 10 (`mlp_forward` with a planted and a seeded model) and screen 11 (`mlp_dev_loss` with `mlp_forward` given) build the two halves on the course sizes, and screen 3 counts the course model's weights in a table. The task asks for all three from an empty stub, for any sizes, on a new planted model (5 symbols, block 2), and adds the general count formula.
