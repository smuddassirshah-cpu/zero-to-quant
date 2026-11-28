# nn-train level 4: performance task

- `homework-4.json` item 1 of 8, `h4-report`. Kind `code` (Python), difficulty 5.
- Objective (l16): "Compare two training set-ups across seeds with a paired test and a confidence interval.", with l15's "Build a training log that records everything a rerun needs, and audit one." and l14's "Design an ablation that removes one change at a time, and read which change mattered." The level matches the verb rule on l14 ("Design") and l15 ("Build"); the brief names this task, kind `code`.
- Product: from a stub, `experiment_report(results, baseline, changes)`: for each change, pair its runs with the baseline's by seed (common seeds only), and return the mean difference, its 95% $t$ interval and whether $|t|$ beats the two-sided Bonferroni cut-off across all the changes. 8 hidden tests, 1 example: a planted report with two real and two null effects (`plant(seed, effects)` in the prelude, standard-library `random`), its verdicts, a borderline effect ($t = -2.61$) that survives alone and fails among five changes, our ablation from `nn-train-seeds.json` (Adam's removal misses the corrected bar; layer norm's and dropout's pass), missing seeds listed out of order, six seeds, and a second borderline effect ($t = -2.99$). No hints, no parts. `budget` 2,000 ms; every case under 10 ms in CPython.
- Mutants (ENGINE-BACKLOG 1263): four, each first failing the test it names: no Bonferroni correction (test 4), a one-sided correction (test 5), the interval widened to the corrected level (test 1), pairing by list position (test 6).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no `[ai-mutants]` or `[source-ban]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/nn-train python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences.
3. Numbers script `docs/reports/nn-train-L4-numbers.py`, run by `node tools/run-number-scripts.mjs --python <venv> --only nn-train-L4`: passed (422 of 422 checks, strict coverage 0 uncovered); it runs the model solution against all 8 tests, the starter (fails) and the four mutants, and recomputes the report on our ablation. `node tools/grade-all.mjs --code --file content/courses/nn-train/homework-4.json --local-cdn <pkgs>`: 0 failures in Pyodide.
4. `node tools/playthrough.mjs --set nn-train/homework-4 --mobile --local-cdn <pkgs>` (desktop and 440 px): all passed, "1 performance starter fail".

- Overlapping screens: l16 screen 10 (`paired_t`, `compare_configs`: one pair of set-ups, no correction) and l14 screen 10 (`ablation_table`: means and sds, no test). The task combines pairing, the interval and a multiple-testing verdict across several changes from a blank start; no lesson screen corrects for several comparisons in code.
