# gpt level 2: performance task

`homework-2.json`, `h-gpt-loss`, item 1 of 6. Kind `code` (Python).

Matched objective: l7-next-character "Code the GPT forward pass in NumPy and match reference logits." (also l6 "Write a loader for supplied weights ..." and l8 "Build a sampler ...").

Task: `gpt_loss(weights, text)`, the mean next-character loss in nats of the tiny GPT on a text of 2 to 33 characters, from a stub starter (`def gpt_loss(weights, text): ...`). The prelude loads the supplied weights (`W`) and gives `VOCAB`; the learner writes the embedding, the pre-norm block with 4 masked heads, the final layer norm, the head and the shifted cross-entropy.

Tests: 8 hidden, 2 examples. Four 33-character validation windows, a speaker's line, a two-character text (T = 1), a run of one letter and `$3 X` (characters the training slice never holds), each against the `gpt_ops_l2` reference to $10^{-9}$ relative. Mutants (ENGINE-BACKLOG 1263): no causal mask, targets equal to inputs (off-by-one), scaling by the width instead of the head width, positions never added; each first fails test 1.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/gpt/ python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 explanations over three sentences.
3. Numbers script: `node tools/run-number-scripts.mjs --python <venv> --only gpt-L2`: passed (strict coverage).
4. Playthrough: `node tools/playthrough.mjs --set gpt/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails; `grade-all.mjs --file ... --code`: 0 failures (solution, starter, mutants).

Overlapping screens: l7-next-character screens[4] (`causal_mask`, `forward`) and screens[6] (`loss`). New here: the whole pass and its loss in one function from a blank start, from text rather than ids, and a one-position text.
