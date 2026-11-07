# game-theory L1 performance task

- File: `app/content/courses/game-theory/homework-1.json`, item `hw1-street-carts` appended (index 8).
- Kind: `code`. Objective: l1 "Write a two-player game as a payoff table and read each player's best reply." Lessons have no code, but this homework grades two code items.
- Task: `street_table` builds a coffee-cart location game (halfway homes split, repeated homes, a price each). `best_replies` returns every best reply of each player, ties kept, for any table.
- Overlap: l1 screens 2 and 8 turn a story into a table; screens 0, 1, 5 read best replies; `hw1-pure-nash` reads them from `A`, `B`. New: the location rules built in code, per-move reply lists, negative payoffs. No Nash part, since `hw1-pure-nash` grades it.
- Tests: 9 hidden, 2 examples. The starter fails all 9; 13 planted bugs each fail at least one.
- Freshness: grep coffee, cart, street, home, nearer, halfway, location, `best_repl`, `street_table`: no hit. `fresh-check --file`: none on the item.

## Gates
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/game-theory python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/python -I docs/reports/game-theory-1-perf-numbers.py`: 118 checks, exit 0.
4. `node tools/playthrough.mjs --set game-theory/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed.

Backlog: 0 bullets.
