# sequence level 4: performance task

- `homework-4.json` item 8 of 8, `h-perf`. Kind `code` (Python), difficulty 5.
- Objective (l13): "Build a pre-norm transformer block from attention, a feed-forward net and layer normalisation." The level matches the verb rule on l13 ("Build") and l16 ("Run ... and train"); the brief puts the task on a whole causal language model built from that block, kind `code`.
- Product: from a stub (`def transformer_lm_forward(tokens, params, n_blocks, h): ...`), NumPy only, no shipped modules: token embeddings plus learned positions, the first `n_blocks` pre-norm blocks (layer norm, causal multi-head attention with biases, addition; layer norm, ReLU MLP, addition), the final layer norm and the unembedding. 8 hidden tests, 1 example: planted weights (vocabulary 7, context 6, width 8, three blocks, MLP 32) with 3, 2 and 0 blocks and with 2 and 4 heads, one token, a leak test (changing the last token moves no earlier logit), and the shipped reversal model (it must write 9 5 1 4 1 3 after 3 1 4 1 5 9). The expected values are checked in the number script against `seq_ops_l4.lm_logits`.
- Mutants (ENGINE-BACKLOG 1263): six, post-norm MLP (test 1), no positions (1), every block whatever `n_blocks` says (2), no final layer norm (1), no causal mask (1), scaling by $\sqrt d$ instead of $\sqrt{d/h}$ (1).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` or `[source-ban]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/sequence python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences.
3. `node tools/run-number-scripts.mjs --python <venv> --only sequence-L4`: passed; the numbers script runs the solution against all 8 tests, the starter (fails) and the six mutants. `node tools/grade-all.mjs --code --file content/courses/sequence/homework-4.json --local-cdn <pkgs>`: 0 failures.
4. `node tools/playthrough.mjs --set sequence/homework-4 [--mobile] --local-cdn <pkgs>`: all passed at both sizes, "1 performance starter fail".

- Overlapping screens: l13 screen 5 (`transformer_block` with the course ops), l16 screen 3 (`tiny_forward` with `seq_ops_l4.block`). The task joins embeddings, positions, a variable number of blocks and the head from a blank start in plain NumPy (attention, layer norm and the mask written by hand), tested with a leak test, one token, zero blocks and a second set of weights, which neither screen does.
