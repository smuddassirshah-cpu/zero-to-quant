# Topic 0.4 exam: computer basics

File: `app/content/exams/topic-0.4.json` (id `topic-0.4`, 45 minutes, pass 0.7). Minutes follow `examMinutes` in `learn.js`: topic 0.4 is 40 h, at most 60 h, so 45.
Generator and checks: `scratchpad/exam-0.3-0.5/` (`gen04.py` builds the file and the code tests, `code04.json` holds the code items, `codecheck.py` runs solutions, starters and wrong versions, `shell/` holds the bash runs of the terminal traces).

## Shape

20 items, interleaving the two courses (terminal, first-python). The brief asked for 16 to 22; the validator requires at least 20 for a topic exam.

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 4 | 20% | 20% |
| 3 | 10 | 50% | 50% |
| 4 | 4 | 20% | 20% |
| 5 | 2 | 10% | 10% |

Widgets: 8 choice, 6 numeric, 3 code, 2 tap-regions (folder tree, script console), 1 multi. The terminal items are read-and-trace, as the course teaches them; the Python items include three code items, as the first-python course does.

| # | id | d | skills | widget / canvas | answer |
|---|---|---|---|---|---|
| 1 | e-typing-speed | 2 | tm-typing | numeric | 70 wpm |
| 2 | e-three-operators | 2 | fp-values | choice | `3.5 3 8` |
| 3 | e-header-line | 2 | tm-shell | numeric | 40 |
| 4 | e-rename-pdf | 2 | tm-files | choice | still PDF bytes |
| 5 | e-curly-quotes | 3 | tm-setup | choice | curly quotes from a word processor |
| 6 | e-up-two | 3 | tm-files | tap-regions on tree | `/home/sam/fx/eurusd.csv` |
| 7 | e-two-greps | 3 | tm-shell | numeric | 4 |
| 8 | e-wrong-folder | 3 | tm-files, tm-shell | choice | `cd backtest`, then `python3 run.py` |
| 9 | e-range-step | 3 | fp-control | numeric | 21 |
| 10 | e-slice-format | 3 | fp-values | choice | `VOD: £72.46` |
| 11 | e-list-update | 3 | fp-lists | choice | `-2 4` |
| 12 | e-print-or-return | 3 | fp-functions | choice | `25.0` then `None` |
| 13 | e-code-band | 3 | fp-control, fp-lists | code | `days_outside` |
| 14 | e-text-number | 3 | fp-values | choice | `25.0 12 12.50` |
| 15 | e-move-wildcard | 4 | tm-shell, tm-files | numeric | 4 |
| 16 | e-tap-cause | 4 | fp-functions, tm-setup | tap-regions on console | line 6 |
| 17 | e-code-biggest-move | 4 | fp-functions, fp-lists | code | `biggest_move(path)` |
| 18 | e-path-search | 4 | tm-shell, tm-setup | multi | `git`, `/usr/bin/pytest` |
| 19 | e-redirect-trace | 5 | tm-shell | numeric | 5 |
| 20 | e-code-daily-returns | 5 | fp-values, fp-control, tm-setup | code (script mode, stdin) | stdout |

Skills: all 8 of the topic are covered: tm-typing 1, tm-files 4, tm-shell 6, tm-setup 4, fp-values 4, fp-control 3, fp-lists 3, fp-functions 3.

Fresh against the courses: the course has `up_days`, `max_drawdown`, `largest`, `close_from_row` and a hard-coded `returns.py`, so the code items are new problems: closes outside a band (edges inside), the biggest absolute move read from a CSV file (header, trailing blank line, any path), and a terminal script that reads a count and closes from stdin, prints returns and the best day (ties to the earlier day, `Best: none`). A first draft of `qty * 2` after `input()` matched first-python l4 and was replaced by the `float`, `int` and `+` item.

## Code items (CPython harness `codecheck.py`, plus the app's Pyodide worker in the playthrough)

| item | tests | solution | starter | wrong versions (each fails) |
|---|---|---|---|---|
| e-code-band | 8 | 8/8 | fails (2 of 8) | `<=`/`>=` edges (test 2), below only (test 1) |
| e-code-biggest-move | 8 | 8/8 | fails (3 of 8) | no `abs` (test 2), no blank-line skip (test 5), fixed file name (test 6), header kept (test 1) |
| e-code-daily-returns | 7 | 7/7 | fails all | best starts at 0 (test 6), `>=` on ties (test 5), no `Best: none` (test 3) |

Each `byKey` test line names the test that the matching wrong version fails first. Expected values come from the solution and from a second method (offset counting for the 1,000-close band, `csv` plus `zip` for the moves, a list-based rewrite for the script's output).

## Numbers computed twice

`gen04.py` asserts each: 1,050 ÷ 5 ÷ 3 = 70 both ways round; `range(3, 15, 4)` sums to 21; the `grep BA | grep buy` count (4), the `mv *2024*` listing (4) and the redirect trace (5) by Python list filters, and all three again in real bash (`shell/`). The printed outputs of items 2, 10, 11, 12 and 14 and the two error messages (curly quote, `str` minus `float`) were produced by running the code in Python 3.13.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors, no warning for this file.
- Copy lint (`lint.py`): no `!`, no em or en dash, no sentence of 20 words or more, no American spellings; explanations at most three sentences.
- `playthrough.mjs --exam topic-0.4 --local-cdn <pkgs>`: 20 of 20, passed, desktop and `--mobile` (the three code solutions pass in the worker).
- Screenshots reviewed (`scratchpad/exam-0.3-0.5/shots04`). Fixes made from them: the folder tree lost a level and its extra leaf so it reads on a phone; the traceback's last line, cut off at the block's edge, is repeated below it as wrapping inline code.

## Engine notes

In `docs/BACKLOG-INBOX.md`: the validator's 20-item floor for short topics, the tree canvas's fixed frame on phones, fenced text blocks that cannot wrap.
