# ml-int level 3: performance task

- `homework-3.json` item 1 of 6, `h1-case-report`. Kind `code` (Python, pandas), difficulty 5.
- Objective (l11): "Build a simulated panel where a network beats boosting, and name the data shapes that cause it." The level matches the verb rule on l11 ("Build"); the kind is `code`. The task builds the case's evidence table from the supplied panel results.
- Product: from a stub, `case_report(df)` on the rows of `case.csv`: for each world and seed, each model's out-of-sample $R^2$ from the day sums, the paired $t$ of network minus boosting over the 150 test days, and the decision rule's verdict ("network" at $t \le -2$, "boosting" at $t \ge 2$, otherwise "no change"). 7 hidden tests, 1 example: the four verdicts, world A seed 0's three $R^2$, the four $t$ values and world B seed 1's $R^2$ (each to $10^{-6}$), the keys, a one-run subset, and a planted tie. `budget` 15000 ms for the pandas load. No hints, no parts.
- Mutants (ENGINE-BACKLOG 1263): four, each first failing the test it names: the sign of $t$ read backwards (test 1), no no-change band (test 1), a mean of daily $R^2$ instead of day sums (test 2), the sd dividing by $n$ (test 3).
- Overlapping screens: l9 screen 9 (`r2_out_of_sample`, `r2_from_days`) and l10 screen 9 (`paired_day_test`) compute the pieces on one run each; l12 states the decision rule. The task joins them over every world and seed, from a blank start, with the verdict.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; no `[ai-mutants]` or `[source-ban]` warning on the level's files.
2. `VOICE_BASE=app/content/courses/ml-int python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans.
3. Numbers script: `node tools/run-number-scripts.mjs --python <venv>/bin/python --only ml-int-L3`: 1 passed (strict coverage); it refits every model with scikit-learn 1.6.1, checks the file, and runs the solution, starter and mutants through ZQ_LIB.
4. Playthrough: `node tools/playthrough.mjs --set ml-int/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the performance starter fails as required. `grade-all.mjs --code --strict-feedback`: 0 failures.
