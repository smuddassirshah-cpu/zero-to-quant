# momentum-rep level 1: performance task

- `homework-1.json` item 9 of 9, `h-ivol-plan`, appended. Kind `derivation`: the product is a written plan, not code or speech.
- Objective (l5): "Write a plan with data, steps and checks before any code." Setting: a plan for Ang, Hodrick, Xing and Zhang (2006), the idiosyncratic-volatility sort, summarised in the prompt.
- Rubric 3, 3, 3, 1: data and traps, steps, checks (all `required`); target and tolerance. `rubric-passes.mjs`: passes 1-2-3 and 1-2-3-4; no pass skips rows 1 to 3.
- Overlap: l5 screens 2, 3, 7 (JT plan), 10 (PLAN.md), quiz q1; l4 tolerance. New: daily regression window, caps dated at formation, Nasdaq from 1972, minimum days, factor-file vintage, codes as recorded, shuffled-score placebo.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/momentum-rep python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/momentum-rep-1-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set momentum-rep/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed; shots clean.

Freshness: `fresh-check.mjs --file` 0 hits; grep idiosyncratic, volatility, quintile, delist, survivor, point-in-time, Nasdaq, daily, Fama, Hodrick: hits read, none repeats the task.

Backlog: 0 new bullets.
