# first-python level 2: performance task

- `homework-2.json` item 10 of 10, `h-split-bill`, appended. Kind `code`, difficulty 4.
- Matched objective (l5): "Write comparisons with `<`, `<=`, `==` and `!=`, and read their boolean values." (l8 "Build..." also matches.)
- Product: the body of `split_bill(prices, people)`: text prices, 12.5% for 6 or more people, each share returned. `def` and `return` are given, as on every level 2 code screen.
- Tests: 8 hidden, 1 example. Twelve planted slips fail, among them text left unconverted, `int()`, `//`, `> 6`, a missed price, printing the share.

Gates (`<pkgs>` is the scratchpad folder):
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. Voice, `VOICE_BASE=app/content/courses/first-python python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `python3 -I docs/reports/first-python-2-perf-numbers.py`: exit 0.
4. Playthrough, `node tools/playthrough.mjs --set first-python/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed, starter fails; shots clean, no older item flagged.

Freshness: `fresh-check.mjs --file` 0 hits. Grep: bill, share, service, people, group, split, 12.5.

- Overlapping screens: l7 screens 2, 6 and 8, l5 screens 7 and 9, l4 screens 3 and 4, l1 screens 2 to 4, homework-2 `h-first-breach`. New: converting each entry in the loop, a group-size edge at 6, the share.

Backlog: 1 bullet.
