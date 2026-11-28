# gpt level 5: performance task

`homework-5.json`, `h-memory-plan`, item 1 of 6. Kind `code` (Python).

Matched objective: l19-what-fits "Build a memory budget for training and for inference." (also l18 "Write bf16 rounding and explain where low precision loses information." and l20 "Code a KV cache for the tiny GPT and compute its size for a large model.", whose verbs match the rule).

Task: from a one-line stub, `memory_plan(config, mode)` returns the bytes of weights, gradients, optimiser state and KV cache for `mode` `'train'` or `'infer'`. The learner counts parameters from the configuration (level 4's count: embeddings, blocks with biases and norms, final norm, untied head with its bias), multiplies by the bytes each part keeps (Adam's two moments plus a master copy for training), and sizes the cache ($2LdTbB$) for inference.

Tests: 8 hidden, 2 examples, compared exactly. Training and inference plans for the tiny GPT (float64, Adam, no master copy), the untied 7B-like configuration and the tied GPT-2 small; the 7B-like cache at a batch of 16; GPT-2 with an untied head. Mutants (6): a cache counted in training (test 1), tied and untied swapped (test 1), keys without values (test 2), no master copy (test 3), a tied head given a bias (test 5), the batch ignored (test 7). Each first fails its named test, and each of those tests has a `byKey` line.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/gpt/ python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 explanations over three sentences.
3. Numbers script: `node tools/run-number-scripts.mjs --python <venv> --only gpt-L5`: passed (strict coverage).
4. Playthrough: `node tools/playthrough.mjs --set gpt/homework-5 --mobile --why --local-cdn <pkgs>`: passed at desktop and 440 px, the performance starter fails; `grade-all.mjs --file ... --code --strict-feedback`: 0 failures.

Overlapping screens: l19-what-fits screens[6] (`training_bytes`, `inference_bytes`, which take per-parameter sizes as arguments) and l20-the-kv-cache screens[9] (`kv_cache_bytes`). New here: the parameter count from a configuration, tied against untied heads, both modes in one function, and a dict of four parts.
