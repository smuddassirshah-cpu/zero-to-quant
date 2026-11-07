# coint level 1: performance task (perf retrofit)

- `coint/homework-1.json`, `h-spurious-aloud`, index 9, appended (9 items before, cap 12).
- `aloud`: 180 s, think 30, `lockAtZero`, three follow-ups, difficulty 5.
- Objective: l1 "Explain why the t statistic and $R^2$ mislead when both series are I(1)". Chosen over l4: interviewers probe spurious regression first, and l4 screen 11 already asks l4's question.
- Rubric 2, 3, 2, 2, 1; rows 1 to 4 (conditions, $t$, $R^2$, remedy) required. `rubric-passes.mjs`: passing sets {1,2,3,4}, {1,2,3,4,5}.
- Overlap: l1 screens 3, 6, 7, 8, 10, 11, `q-longer`, `h-longform`. New: why $\hat\beta$ never settles while se shrinks, why $R^2$ stays random, scale invariance, drift, cointegrated $t$, a day-late copier; new setting and figures.
- Gates: `node tools/validate.mjs` 0 errors; `VOICE_BASE=app/content/courses/coint python3 docs/reviews/voice-scan.py 35` 0 and 0; `venv/bin/python -I docs/reports/coint-1-perf-numbers.py` exit 0, 64 checks; `node tools/playthrough.mjs --set coint/homework-1 --local-cdn <pkgs>` All passed, with and without `--mobile`.
- Freshness: `fresh-check --file` clean on the item; grep copper, software, 38.7, 0.60, 91.9, 48.0, 9.4%, eleven, long-run, day late, rescal, n^2, straight line.
- Backlog: 1 bullet.
