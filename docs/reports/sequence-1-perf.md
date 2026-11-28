# sequence level 1: performance task

- `homework-1.json` item 8 of 8, `h-perf`. Kind `code` (Python), difficulty 5.
- Objective (l1): "Write a linear recurrent net and match it to an AR(1), then add a tanh." The level matches the verb rule on l1 ("Write"), l3 ("Explain") and l4 ("Write"); the brief puts the task on backprop through time by hand, kind `code`.
- Product: from a stub, `rnn_bptt(x, y, params)` for a tanh recurrent net with a linear readout, returning the loss and the gradients of `Wx`, `Wh`, `b`, `Wy`, `by` by a hand-written backward pass through time. 10 hidden tests, 1 example: the loss and all gradients on a planted 3-step net, a central-difference check of the learner's own loss on a 6-step net (relative error under $10^{-6}$), three gradient arrays of that net, a one-step series, a 20-step series, and a `zq_no('autograd', 'Tensor', 'grad_check')` ban. Expected values are the autograd's (the number script checks the reference against `autograd.py` on four nets). No hints, no parts.
- Mutants (ENGINE-BACKLOG 1263): four, each first failing test 2: no tanh slope, no gradient carried back from later steps (the "last step only" bug of l2), `Wh` paired with the new state, the $1/T$ dropped.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` or `[source-ban]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/sequence python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences.
3. `node tools/run-number-scripts.mjs --python <venv> --only sequence-L1`: passed; the numbers script runs the solution against all 10 tests, the starter (fails) and the four mutants. `node tools/grade-all.mjs --code --file content/courses/sequence/homework-1.json --local-cdn <pkgs>`: 0 failures.
4. `node tools/playthrough.mjs --set sequence/homework-1 [--mobile] --local-cdn <pkgs>`: all passed at both sizes, "1 performance starter fail".

- Overlapping screens: l2 screen 3 (`bptt_grad` with the autograd) and homework item 2 (`linear_bptt`, the scalar derivative carried forward). The task asks for the full matrix backward pass by hand, with the tanh slopes, the carried gradient and every parameter, which no screen does.
