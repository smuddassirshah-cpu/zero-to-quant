# nn-train level 2: performance task

- `homework-2.json` item 1 of 6, `h2-ln-backward`. Kind `code` (Python), difficulty 5.
- Objective (l8): "Write layer normalisation with its backward pass, and say when it is preferred to batch normalisation." The level matches the verb rule on l5 ("Explain"), l6 ("Derive"), l7 and l8 ("Write"); the brief puts the task on l8's backward pass, kind `code`.
- Product: from a stub, `layernorm_backward(x, gamma, dout, eps)` in NumPy for any leading shape, returning the gradients for `x`, `gamma` and `beta`. 8 hidden tests, 1 example: all three gradients on a seeded (3, 5) batch to $10^{-9}$, a central-difference error below $10^{-6}$ on that batch and on a (2, 2, 4) array (computed in the test by a loaded helper), the sums over two leading axes, a single vector, a vector of equal features (saved by $\epsilon$), and a case whose input gradient is exactly 0. No hints, no parts.
- Mutants (ENGINE-BACKLOG 1263): five, each first failing the test it names: the mean and scale treated as constants (test 1), the scale's path dropped (test 1), gamma's gradient summed over the first axis only (test 5), the variance divided by $D - 1$ (test 1), sums over the batch axis instead of the features (test 1).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/nn-train python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences.
3. `ZQ_NUMBERS_STRICT=1 <venv>/bin/python docs/reports/nn-train-L2-numbers.py`: exit 0; it runs the model solution against all 8 tests, the starter (fails) and the five mutants. `node tools/grade-all.mjs --code --file content/courses/nn-train/homework-2.json --local-cdn <pkgs>`: 0 failures in Pyodide.
4. `node tools/playthrough.mjs --set nn-train/homework-2 --mobile --local-cdn <pkgs>` (desktop and 440 px): all passed, "1 performance starter fail".

- Overlapping screens: l8 screen 3 (the backward derived as an `order` item) and screen 6 (`layernorm` as an autograd op, checked by `grad_check`). The task asks for the backward as a plain NumPy function from a blank start, with all three gradients returned, any leading shape, and the equal-features and zero-gradient cases tested.
