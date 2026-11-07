# puzzles level 4: performance task retrofit

- File: `app/content/courses/puzzles/homework-4.json`. Appended `hw4-kelly-draw`, item 10 of 10 (index 9). Nothing converted; the cap is 12.
- Kind: `derivation`, difficulty 5, skills `pz-games`, `pz-expectation`, no tags.
- Objective: l21 "Derive the Kelly fraction for a repeated favourable bet."
- Fresh setting: a draw-no-bet market (win at 6 to 5, draw refunded, loss), so $f^* = (pb - q)/(b(p + q))$. The course already derives evens (l21) and $b$ to 1 (`hw4-kelly-order`). The model justifies every line, including the SLLN step, $g'' < 0$ and existence via $g'(0)$. It gives $4/15$, $0.0319$, and $-0.0060$ at twice Kelly.
- Rubric: 2, 3 (required: $g$ and $f^*$), 2 (maximum), 2 (numbers), 1 (twice Kelly).
- Gates: (1) `cd app && node tools/validate.mjs`: 0 errors, the expected perf-pending warning. Manifest restored. (2) `VOICE_BASE=app/content/courses/puzzles python3 docs/reviews/voice-scan.py 35`: 0 and 0. (3) `python3 docs/reports/puzzles-4-perf-numbers.py`: 84 checks, exit 0. (4) `node tools/playthrough.mjs --set puzzles/homework-4 --local-cdn <pkgs>`: all passed, with and without `--mobile`. After marking, no display equation scrolls at 440 px (scratch shot).
- Freshness: grepped draw, push, refund, 6 to 5, 4/15, 0.45. `fresh-check.mjs --file` at the loose setting gives no hit on item 9.
