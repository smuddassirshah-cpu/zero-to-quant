# first-python level 3: performance task

- `homework-3.json` item 9 of 9, `h-contract-cost`, appended. Kind `code`, difficulty 4.
- Matched objective (l12): "Write a short script that projects savings with a function and a loop". Here it projects a cost, a setting no lesson uses.
- Product: `contract_cost(fee, rise, years)` on text inputs, returning the total, plus a printed 2-year line.
- Tests: 7 hidden (6 calls, 1 printed line), 1 example. Fifteen planted slips fail: unconverted text, `int()`, printing not returning, `//`, a range off by one, and more.

Gates (`<pkgs>` is the scratchpad folder):
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. Voice, `VOICE_BASE=app/content/courses/first-python python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `python3 -I docs/reports/first-python-3-perf-numbers.py`: exit 0.
4. Playthrough, `node tools/playthrough.mjs --set first-python/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed, starter fails; shots clean, no older item flagged.

Freshness: `fresh-check.mjs --file` no hit on this item. Grep: contract, phone, rise, month, fee.

- Overlapping screens: l12 screens 0, 2, 3, 4, 7 and 9, l10 screen 6, l9 screens 7 and 8, review-3 `r-compound`, homework-3 `h-deposits`. New: a payment total while the fee grows, a percentage as text, the printed call.

Backlog: 1 bullet.
