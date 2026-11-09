# terminal level 3: performance task

- `homework-3.json` item 9 of 9, `h-perf-trade-script`, appended. Kind `code`, difficulty 5.
- Matched objective (l12-first-script): "Write a short Python script and run it with `python3` from its folder".
- Product: `trade.py` from a one-comment stub, in the course's script-mode widget. A £10 fee each way gives cost 500, proceeds 510, profit 10, return 0.02. The run commands go in comments; a hidden postlude follows each `cd` and `python3` from `/home/sam`.
- 10 tests, 0 examples; 21 planted bugs each fail a test, 8 correct variants pass.

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/terminal python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/terminal-3-perf-numbers.py`: numbers script exits 0 (95 checks; fractions, and a real bash and `python3` run).
4. `node tools/playthrough.mjs --set terminal/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed; starter fails.

Freshness: `fresh-check.mjs --file`: no hit on this item; fee, proceeds, profit: not in the course.

Overlapping screens: l12 screens 1, 2, 8, 9 and quiz 2, l10 screen 8, homework-3 `h-returns-script`, `h-stage0-machine` (c). New: a blank file, fees on both legs, run commands graded by following them.

Backlog: 2 bullets.
