# git level 3: performance task

- Item: `h-ignore-options-repo`, `homework-3.json` index 8, appended. Kind: `code` (Python); the learner writes `.gitignore` lines in `GITIGNORE`. Prelude and postlude carry `ignored(path)`, Git's matching rules.
- Matched objective: l12 "Write a `.gitignore` for data, outputs, the virtual environment and keys, and check it works".
- Tests: 14 hidden, 2 examples. Starter fails 7. Fifteen planted wrong files fail, including `data/` with `!data/README.md`, `*.parquet`, unanchored `figures/` and `.env*`. Three other correct files pass.

Overlapping screens: l12 screens[1], [2], [3], [7], quiz `q-pattern-name`, `q-env-example`; l3 screens[7], quiz `q-star-csv`, `q-keep-out`; homework-1 `hw-plan-repo`, `hw-ignore-list`. New parts: `!` inside an ignored folder, `/figures/` against `docs/figures/`, `.env.local`, nested caches, files added later.

Freshness grep: parquet, figures, ipynb, checkpoint, .env.local, pricer, heston, fixtures, notebook, docs/, `!data`, __pycache__, .venv, check-ignore.

## Gates

1. Validator (`node tools/validate.mjs`): 0 errors.
2. Voice (`VOICE_BASE=app/content/courses/git python3 docs/reviews/voice-scan.py 35`): 0 and 0.
3. Numbers script (`python3 docs/reports/git-3-perf-numbers.py`): exit 0; every test through the shipped matcher and a real Git repository, plus 250 random files, 0 mismatches.
4. Playthrough (`node tools/playthrough.mjs --set git/homework-3 --local-cdn <pkgs>`, with and without `--mobile`): All passed. No item flagged too wide.
