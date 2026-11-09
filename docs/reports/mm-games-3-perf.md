# mm-games level 3: performance task retrofit

- `app/content/courses/mm-games/homework-3.json`, item `h-coin-dice-aloud`, index 11 (12 of 12; nothing converted).
- Kind `aloud`: `seconds` 300, `think` 30, three follow-ups, difficulty 5.
- Objective: l12 "Explain each quote as you make it", level 3's only verb-rule match.
- Task: a coin picks two or four dice. The learner quotes through three trades and three reveals, saying each fair value, width and skew.
- Rubric 2, 3, 3, 1, 1. Rows 1 to 4 required: quote with fair value, update after information, reasons for width and skew, position and P&L (the prompt asks for it). `rubric-passes.mjs`: one minimal pass, rows 1, 2, 3, 4.
- Overlapping screens: l12 screens 3, 6, 7 and 9 and `h-narrated-game` lay out spoken quotes on dice and cards. New: the coin-mixed game, the coin's 3.5 swing in fair value, a width held up by the hidden coin, the seen-coin bound 7 at 14. `fresh-check.mjs --file`: 0 hits. Grep: four dice, coin, flip, heads, cannot see, near 7, sees the, quote strings.
- Gates:
  1. `cd app && node tools/validate.mjs`: 0 errors; manifest restored.
  2. `VOICE_BASE=app/content/courses/mm-games python3 docs/reviews/voice-scan.py 35`: 0 and 0.
  3. `python3 docs/reports/mm-games-3-perf-numbers.py`: 99 checks, exit 0.
  4. `node tools/playthrough.mjs --set mm-games/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: all passed.
