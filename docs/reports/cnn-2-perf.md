# cnn level 2: performance task

- `homework-2.json` item 1 of 7, `h-perf-conv-layer`. Kind `code` (Python), difficulty 5.
- Objective (l8): "Build im2col so that a convolution becomes one matrix product, and check it against the loop." The level matches the verb rule on l5 ("Derive"), l6 ("Write") and l8 ("Build"); its exit is code, so the task is `code` on the l8 objective.
- Product: from an empty stub, `conv_layer_forward_backward(x, W, b, stride, pad, dout)` by im2col for one image `(C, H, W)` and filters `(F, C, k, k)`: the output `(F, oh, ow)` and the gradients `dx`, `dW`, `db` of the sum of output times `dout`. 8 hidden tests, 1 example, on planted seeded inputs (seeds 91 to 93): the forward pass against loops; `dW`, `db` and `dx` against central differences (a hidden prelude holds a loop forward and a difference helper), at stride 1 with padding 1 (overlapping patches), stride 2 with padding 1, and stride 2 with no overlap; the four shapes. No hints, no parts. `budget: 4000`.
- Mutants (ENGINE-BACKLOG 1263): four, each first failing the test it names: col2im that overwrites (test 4), the bias gradient summed over filters (test 3), patches put back at stride 1 (test 5), the weight gradient transposed before the reshape (test 2).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` warning on cnn files.
2. `VOICE_BASE=app/content/courses/cnn python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 explanations over three sentences.
3. `<venv>/bin/python docs/reports/cnn-L2-numbers.py`: exit 0; it runs the model solution against all 8 tests, the starter (fails) and the four mutants. `node tools/grade-all.mjs --code --file content/courses/cnn/homework-2.json --local-cdn <pkgs>`: 0 failures in Pyodide.
4. `node tools/playthrough.mjs --set cnn/homework-2 --local-cdn <pkgs> --mobile` (desktop and 440 px): all passed, "1 performance starter fail" as required.

- Overlapping screens: l8 screens 8 to 10 (`im2col`, `conv2d_im2col` forward with `im2col` given, `col2im` alone) and l5 screen 10 (stride and padding by loops). The task joins forward and backward from one empty stub with no helper given, adds the weight and bias gradients, and checks against central differences rather than against a supplied function.
