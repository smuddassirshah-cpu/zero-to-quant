# cnn level 1: performance task

- `homework-1.json` item 1 of 8, `h-perf-conv2d`. Kind `code` (Python), difficulty 5.
- Objective (l3): "Write a two-dimensional convolution and apply edge kernels to a small image." The level matches the verb rule on l1 and l3 ("Write"), so the task is `code`.
- Product: from an empty stub, `conv2d(img, kernels, bias)` for an input of shape `(c_in, n, n)` and filters of shape `(c_out, c_in, k, k)`, unflipped, valid positions, one bias per filter, returning `(c_out, n - k + 1, n - k + 1)`. 7 hidden tests, 1 example: two seeded multi-channel cases (seeds 41 and 42, 3 by 3 and 2 by 2 filters) against a loop-free `einsum` reference, the shape, a 1 by 1 kernel (channel mixing only), a kernel the size of the image (one output, 122), the 7 from l3 with the vertical-edge kernel, and a bias alone (zero kernels). No hints, no parts.
- Mutants (ENGINE-BACKLOG 1263): four, each first failing test 1: no bias, only the first input channel summed, flipped kernels, one position short on each side.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` warning on cnn files.
2. `VOICE_BASE=app/content/courses/cnn python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 explanations over three sentences.
3. `<venv>/bin/python docs/reports/cnn-L1-numbers.py`: exit 0; it runs the model solution against all 7 tests, the starter (fails) and the four mutants. `node tools/grade-all.mjs --code --file content/courses/cnn/homework-1.json --local-cdn <pkgs>`: 0 failures in Pyodide.
4. `node tools/playthrough.mjs --set cnn/homework-1 --local-cdn <pkgs> --mobile` (desktop and 440 px): all passed, "1 performance starter fail" as required.

- Overlapping screens: l3 screens 8 and 9 (`conv2d_valid`, one channel and one kernel; `conv2d_multi`, a stack of kernels on one channel). The task adds input channels summed inside each filter, a bias per filter and the two edge cases, from an empty stub with no helper defined.
