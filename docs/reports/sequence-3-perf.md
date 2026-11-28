# sequence level 3: performance task

- `homework-3.json` item 8 of 8, `h-perf`. Kind `code` (Python), difficulty 5.
- Objective (l11): "Write multi-head attention by splitting and joining the model width." The level matches the verb rule on l9 ("Write"), l10 ("Build"), l11 ("Write") and l12 ("Explain"); the brief puts the task on causal multi-head self-attention with positions, kind `code`.
- Product: from a stub, `causal_mha_forward(X, params, h)`: learned positions added to the embeddings, projections, a split into $h$ heads, scaled attention with a causal mask in every head, the heads joined and mixed by $\mathbf W_O$. 9 hidden tests, 1 example: outputs for 2, 4, 1 and 8 heads on planted data, a 5-token width-12 case with 3 heads, one token, two leak tests (changing token 6, and token 3, moves only its own and later outputs), and a case with the positions zeroed on a reversed input. Expected values are checked in the number script against an explicit loop over heads and positions. No hints, no parts.
- Mutants (ENGINE-BACKLOG 1263): five, each first failing test 1: no causal mask, no positions, scaling by $\sqrt d$ instead of $\sqrt{d/h}$, a split without the transpose, the diagonal masked too.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` or `[source-ban]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/sequence python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences.
3. `node tools/run-number-scripts.mjs --python <venv> --only sequence-L3`: passed; the numbers script runs the solution against all 9 tests, the starter (fails) and the five mutants. `node tools/grade-all.mjs --code --file content/courses/sequence/homework-3.json --local-cdn <pkgs>`: 0 failures.
4. `node tools/playthrough.mjs --set sequence/homework-3 [--mobile] --local-cdn <pkgs>`: all passed at both sizes, "1 performance starter fail".

- Overlapping screens: l11 screen 6 (`multi_head_attention` with a mask argument, no positions) and l12 screen 7 (`add_positions`). The task joins them with the causal mask built in, from a blank start, and is tested with the leak tests, one token and heads of width 1, which neither screen does.
