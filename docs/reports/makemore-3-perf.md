# makemore level 3: performance task

- `homework-3.json` item 7 of 7, `h-perf`. Kind `code` (Python), difficulty 4.
- Objective (l9): "Write a sampler that draws names letter by letter from a model with a seeded generator." The level matches the verb rule on l9 ("Write"); the brief puts the task on that objective, kind `code`.
- Product: from a stub of two empty functions, `sample_names(prob_fn, n, seed, T)` (n names from one `np.random.default_rng(seed)`, chances raised to $1/T$ and rescaled, the course rule `searchsorted(cumsum(p), u, side="right")` capped at 26, stop at the end mark or 20 letters) and `dev_loss(prob_fn, words)` (average $-\ln p$ in nats with a context of three). 7 hidden tests, 1 example: the planted `toy` model at two seeds and two temperatures (exact strings), the trained MLP at seed 7 and temperatures 1 and 0.5 (mora, sarlee, daniyahsa; ken, arah, halee), a model that never ends (the 20-letter cap), the loss of `toy` on two names (1.206043), and the MLP's loss on the first 500 dev names below the bigram's 2.4514. No hints, no parts. `budget: 8000`.
- Mutants (ENGINE-BACKLOG 1263): four, each first failing the test it names: power $T$ instead of $1/T$ (test 2), a fresh generator for every name (test 1), no length cap (test 5), bits for nats (test 6).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/makemore python3 docs/reviews/voice-scan.py 35 --summary`: 0 over 35 words, 0 lesson ids in code spans.
3. `<venv>/bin/python docs/reports/makemore-L3-numbers.py`: exit 0 (162 of 162); it runs the model solution against all 7 tests, the starter (fails) and the four mutants. `node tools/grade-all.mjs --code --file content/courses/makemore/homework-3.json --local-cdn <pkgs>`: 0 failures in Pyodide.
4. `node tools/playthrough.mjs --set makemore/homework-3 --mobile --local-cdn <pkgs>` (desktop and 440 px): all passed, "1 performance starter fail" as required.

- Overlapping screens: l9 screen 9 (`sample_name` for one name, no temperature) and l12 screen 8 (`softmax_t` on logits). The task asks for many names from one generator with a temperature applied to chances (not logits), plus the loss, from an empty stub and under new names; the MLP samples it must reproduce are those l12 shows as recorded output.
