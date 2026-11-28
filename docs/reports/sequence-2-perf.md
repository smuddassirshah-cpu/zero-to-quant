# sequence level 2: performance task

- `homework-2.json` item 8 of 8, `h-perf`. Kind `code` (Python), difficulty 5.
- Objective (l7): "Write attention with query, key and value matrices, and check its shapes." The level matches the verb rule on l6 ("Build"), l7 ("Write") and l8 ("Derive"); the brief puts the task on the backward pass of scaled dot-product attention, kind `code`.
- Product: from a stub, `attention_backward(Q, K, V, dout)` returning $\partial L/\partial\mathbf Q$, $\partial L/\partial\mathbf K$ and $\partial L/\partial\mathbf V$ of $\operatorname{softmax}(\mathbf Q\mathbf K^\top/\sqrt d)\mathbf V$ by hand. 9 hidden tests, 1 example: all three gradients on a planted 2-query case, each gradient on a 3-query, 5-key case, a central-difference check on that case (relative error under $10^{-6}$), one key, scores in the hundreds (values and finiteness), and a `zq_no('autograd', 'Tensor', 'grad_check')` ban. Expected values are the autograd's (the number script checks the reference against `autograd.py` with `seq_ops_l2.py` on four cases). No hints, no parts.
- Mutants (ENGINE-BACKLOG 1263): five: the softmax Jacobian's second term left out (test 1), the $1/\sqrt d$ forgotten on the way back (test 1), $\mathbf A$ for $\mathbf A^\top$ in $\mathbf dV$ (test 1), no maximum subtracted (test 7), the Jacobian term summed down the columns (test 1).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` or `[source-ban]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/sequence python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences.
3. `node tools/run-number-scripts.mjs --python <venv> --only sequence-L2`: passed; the numbers script runs the solution against all 9 tests, the starter (fails) and the five mutants. `node tools/grade-all.mjs --code --file content/courses/sequence/homework-2.json --local-cdn <pkgs>`: 0 failures.
4. `node tools/playthrough.mjs --set sequence/homework-2 [--mobile] --local-cdn <pkgs>`: all passed at both sizes, "1 performance starter fail".

- Overlapping screens: l7 screen 7 (`attention_autograd`, the same gradients by the autograd) and homework item 6 (the softmax Jacobian as an `order` item). The task asks for the whole backward pass by hand, with the $\sqrt d$ scaling, one key and large scores, which no screen does.
