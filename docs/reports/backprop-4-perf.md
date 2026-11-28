# backprop level 4: performance task

- `homework-4.json` item 6 of 6, `h-perf-autograd`. Kind `code` (Python), difficulty 5.
- Objective (l16): "Build an array autograd in NumPy and check it against central differences to relative error $10^{-6}$ in float64." The level matches the verb rule first on l13 ("Derive"), but its exit is code, so the brief makes the task `code` on the l16 objective ("Build").
- Product: from a stub of empty methods, `Tensor` with `+`, `*` (both broadcasting and taking plain numbers), `@`, `sum(axis=None, keepdims=False)`, `tanh()` and an iterative `backward()`, plus the function `cross_entropy(logits, targets)`, to the contract's signatures. `unbroadcast` is loaded in the prelude. 8 hidden tests, 1 example: a tensor used twice (`(w * w + w).sum()`, gradient $2w + 1$); three fresh seeded networks (seeds 51 to 53: a broadcast bias with a tanh layer; two hidden layers with a `(1, 4)` row bias; one weight used twice) checked by a postlude central-difference checker below $10^{-6}$ in float64; the loss of equal logits ($\ln 4 = 1.386294$); logits near 1000 (0.417030); `ValueError` for a loss of size 2; a chain 5,000 operations deep (a recursive `backward` fails it). No hints, no parts. `budget: 4000`.
- Mutants (ENGINE-BACKLOG 1263): four, each failing the test it names: no division by $n$ in the fused backward (test 2), `=` instead of `+=` in `*` (test 1), a recursive `backward` (test 8), no row maximum taken out (test 6).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/backprop python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 explanations over three sentences.
3. `<venv>/bin/python docs/reports/backprop-L4-numbers.py`: exit 0 (326 of 326); it runs the model solution against all 8 tests, the starter (fails) and the four mutants. `node tools/grade-all.mjs --code --file content/courses/backprop/homework-4.json --local-cdn <pkgs>`: 0 failures in Pyodide.
4. `node tools/playthrough.mjs --set backprop/homework-4 --local-cdn <pkgs> --mobile` (desktop and 440 px): all passed, "1 performance starter fail" as required.

- Overlapping screens: l16 screens 3, 5 and 9 build the same class step by step on the course data and on seeds 20 to 23. The task joins them from one empty stub, drops the scaffolding (no `__add__` given, no step order), and checks on fresh networks (seeds 51 to 53, a row bias of shape `(1, 4)`, two hidden layers). fresh-check reports the code names `Tensor`, `cross_entropy` and `backward` as shared with l16 for that reason; they are the contract's names.
