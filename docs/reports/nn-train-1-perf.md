# nn-train level 1: performance task

- `homework-1.json` item 1 of 6, `h1-optimizer`. Kind `code` (Python), difficulty 5.
- Objective (l2, l3): "Write momentum and show how it speeds descent along a long, narrow valley." and "Write Adam with its bias correction, and say what each moment estimate does." The level matches the verb rule on l2 and l3 ("Write") and l4 ("Build"); the brief puts the task on the optimisers, kind `code`.
- Product: from a stub `make_optimizer(name, **settings)`, an object whose `step(params, grads)` returns new parameter arrays for `"sgd"`, `"momentum"` and `"adam"`, keeping its own state (velocity; two moments and a step count). 10 hidden tests, 1 example: exact SGD and momentum iterates on the bowl $\tfrac12(x^2 + 10y^2)$ (given $\beta$ and the default 0.9), Adam on the bowl to $10^{-9}$, Adam on the loss times 1,000 (same path to $10^{-6}$), a coordinate whose gradient is always 0, two instances with separate state, `ValueError` for an unknown name, inputs left unchanged, and Adam on two arrays of different shapes with its own $\beta_1$, $\beta_2$. No hints, no parts.
- Mutants (ENGINE-BACKLOG 1263): five, each first failing the test it names: Adam without bias correction (test 4), momentum that never stores its velocity (test 2), Adam's step count never advanced (test 4), state kept on the class so two optimisers share it (test 7), SGD updating in place (test 9).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/nn-train python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans.
3. `ZQ_NUMBERS_STRICT=1 <venv>/bin/python docs/reports/nn-train-L1-numbers.py`: exit 0; it runs the model solution against all 10 tests, the starter (fails) and the five mutants. `node tools/grade-all.mjs --code --file content/courses/nn-train/homework-1.json --local-cdn <pkgs>`: 0 failures in Pyodide.
4. `node tools/playthrough.mjs --set nn-train/homework-1 --mobile --local-cdn <pkgs>` (desktop and 440 px): all passed, "1 performance starter fail" as required.

- Overlapping screens: l2 screen 7 (`momentum_step`, `run_momentum`, `best_heavy_ball` on a single array) and l3 screen 7 (`adam_step` on lists, `adam_first_step_size`) write each update as a function. The task asks for all three behind one interface, from a blank start, with state kept per object, defaults, an error for an unknown name, and the scale and zero-gradient behaviour tested.
