# makemore level 1: performance task

- `homework-1.json` item 7 of 7, `h-perf`. Kind `code` (Python), difficulty 4.
- Objective (l1): "Build the 27 by 27 table of letter pairs from a list of names." The level matches the verb rule on l1 ("Build") and l2 ("Derive"); the brief puts the task on the l1 objective, kind `code`.
- Product: from a stub of two empty functions, `bigram_model(words, alpha)` (count every pair with both marks, add `alpha`, divide each row by its own total) and `avg_nll(P, words)` (average $-\ln P_{ab}$ in nats, `math.inf` for a chance of 0). 7 hidden tests, 1 example: a planted list with alpha 0, a planted list with alpha 1 (a 3 by 3 corner, exact to 6 places), a count from the training names (`P[n, end]` with alpha 0), the dev loss with add-one counts from the training names (2.4514 to 4 places), an unseen dev pair (tzvi gives `math.inf`), a list whose pairs are all certain (loss 0), and rows summing to 1 within 1e-12 at alpha 0.5. No hints, no parts. `budget: 8000`.
- Mutants (ENGINE-BACKLOG 1263): five, each first failing the test it names: whole-table normalising (test 1), alpha left out of the row total (test 2), bits for nats (test 4), an unseen pair skipped (test 5), no end mark (test 1).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/makemore python3 docs/reviews/voice-scan.py 35 --summary`: 0 over 35 words, 0 lesson ids in code spans.
3. `<venv>/bin/python docs/reports/makemore-L1-numbers.py`: exit 0 (375 of 375); it runs the model solution against all 7 tests, the starter (fails) and the five mutants. `node tools/grade-all.mjs --code --file content/courses/makemore/homework-1.json --local-cdn <pkgs>`: 0 failures in Pyodide.
4. `node tools/playthrough.mjs --set makemore/homework-1 --mobile --local-cdn <pkgs>` (desktop and 440 px): all passed, "1 performance starter fail" as required.

- Overlapping screens: l1 screen 10 (`bigram_counts`), l2 screen 11 (`bigram_probs`, `nll`) and l3 screen 9 (`loss_report`) build the pieces with helpers given (`index`, `counts`, `N_train`). The task joins counting, smoothing and the loss from an empty stub with no helpers, under new names, and adds the alpha-0.5 row check.
