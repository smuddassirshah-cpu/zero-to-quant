# py-found level 1: performance task

- `homework-1.json` item 10 of 10, `h-overnight-gaps`, appended. Kind `code`, difficulty 4.
- Matched objective (l4): "Write list comprehensions, with and without a condition".
- Product: `overnight_gaps(days, limit)` returns `(gaps, flagged)`, opens against previous closes and the dates gapping more than `limit` either way.
- Tests: 10 hidden, 1 example. Twelve planted slips fail, among them divide by the open, no `abs`, the day before, a `days[-1]` wrap, `>=`, an empty list, `.append`.

Gates (exact commands; `<pkgs>` is the scratchpad folder):
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, plus the expected perf-pending warning.
2. Voice, `VOICE_BASE=app/content/courses/py-found python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `python3 -I docs/reports/py-found-1-perf-numbers.py`: exit 0.
4. Playthrough, `node tools/playthrough.mjs --set py-found/homework-1 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed, starter fails; shots clean.

Freshness: `fresh-check.mjs --file` no hit. Grep: overnight, gap, open, `abs(`, `zip(`.

- Overlapping screens: l3 screen 7, l4 screens 2 to 4, review-1 `r-up-days`, homework-1 `h-k-day-returns`, `h-csv-best-worst`. New: neighbouring records' two fields, a two-way flag, two lists.

Backlog: 0 bullets.
