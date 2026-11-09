# numpy-pandas level 2: performance task

- `homework-2.json` item 9 of 9, `h-fills-report`, appended. Kind `code`, difficulty 4.
- Objective: l5 "Build a Series and a DataFrame, and select by label and by position." (the only match).
- Tests: 13, 1 example. 13 planted slips fail: chained `fills[mask]["qty"]`, sorted index, `iloc` and `fills[a:b]` spans, span after `dropna`, last fill unconfirmed, largest id, price filled with 0, value before signing, NaN sum, caller's list mutated, span as a list. A loop route passes.

Gates:
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. Voice, `VOICE_BASE=app/content/courses/numpy-pandas python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/numpy-pandas-2-perf-numbers.py`: exit 0.
4. Playthrough, `node tools/playthrough.mjs --set numpy-pandas/homework-2 --local-cdn <pkgs>`, with and without `--mobile`, new manifest: All passed.

Freshness: `fresh-check --file` no hit. Grep: fill, trade id, broker, confirm, sell, side, `df[0]`, iloc.
Overlapping screens: l5 screens 3 to 6, 8 and 11, l7 screens 4 and 8, l8 screens 5, 6 and 9, `h-exposures`. New: whole-number ids out of order, so label and position disagree; signing by side; a span on an unsorted index; the last confirmed fill; inputs unchanged.

Backlog: 2 bullets.
