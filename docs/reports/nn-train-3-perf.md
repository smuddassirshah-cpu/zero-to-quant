# nn-train level 3: performance task

- `homework-3.json` item 1 of 6, `h3-select`. Kind `code` (Python), difficulty 5.
- Objective (l9): "Show that weight decay is the ridge penalty, and choose its strength on validation loss." with l11's "Write inverted dropout and explain why the network is scaled at training time." The level matches the verb rule on l11 ("Write") and l12 ("Explain"); the brief names this task, kind `code`.
- Product: from a stub, `regularise_and_select(X_tr, y_tr, X_val, y_val, lams, ps, steps=300)`: for every pair of penalty and dropout rate, train a 1-16-1 tanh net by the stated recipe (full-batch Adam at 0.02, penalty on both weight matrices, `nt_ops_l3.dropout` on the hidden layer with its own generator), validate without dropout, and return the best pair and a dict of every pair's validation MSE. 5 hidden tests, 1 example: an exact 5-step grid (to 7 figures), one entry per pair, a planted clean sine (no regularisation must win), planted pure noise (the strongest penalty must win), and an exact 20-step run with dropout. No hints, no parts. `budget` 8,000 ms.
- Mutants (ENGINE-BACKLOG 1263): four, each first failing the test it names: dropout never applied (test 1), biases penalised (test 1), outputs scaled again at validation (test 1), the worst pair picked (test 3).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/nn-train python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences.
3. `ZQ_NUMBERS_STRICT=1 <venv>/bin/python docs/reports/nn-train-L3-numbers.py`: exit 0; it runs the model solution against all 5 tests, the starter (fails) and the four mutants. `node tools/grade-all.mjs --code --file content/courses/nn-train/homework-3.json --local-cdn <pkgs>`: 0 failures in Pyodide.
4. `node tools/playthrough.mjs --set nn-train/homework-3 --mobile --local-cdn <pkgs>` (desktop and 440 px): all passed, "1 performance starter fail".

- Overlapping screens: l9 screen 7 (`decayed_sgd_step`, `best_lambda` from recorded losses) and l11 screens 6 and 7 (`dropout_forward`, the op's backward). The task trains real nets under both regularisers from a blank start, holds the masks and starting weights fixed across pairs, and selects on validation; no lesson screen trains a net.
