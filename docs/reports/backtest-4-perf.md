# backtest L4: performance task

- `homework-4.json`, item `h-reversal-note`, index 8 (9 of 9). Added; nothing converted.
- Objective (l16): "Write a one-page results note, including what failed."
- Kind `derivation`, not `data`. A `data` task needs a file under `app/content/data/`, which is outside this agent's course folder. So the run's output is a `table` canvas plus the prompt, and the learner writes the note in an empty box (self-marked, no scaffold).
- Study: a reversal rule new to the course, 30 settings, a first run filled at the close, a £1m desk size. The model works out drag, standard errors, the 0.78 bar, impact (10 bp), net −0.39 at £1m and capacity near £0.37m.
- Rubric 2, 2, 2, 3, 1. "What failed" (3) is `required`.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/backtest python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/backtest-4-perf-numbers.py`: 37 checks, exit 0, each figure by two routes.
4. `node tools/playthrough.mjs --set backtest/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: All passed. A full-height 440 px shot of the marked model fits.

Freshness: reversal, `2.043`, `£1m book`, `£90m`. Only stock decimals and r-gap's 1,003 recur; `fresh-check --file` 0 hits.
