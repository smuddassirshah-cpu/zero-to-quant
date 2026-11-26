# Concept audit, round 2: terminal levels 1 to 3 (terminal-1-3-r2)

Blind read of every file of `terminal` at commit 70b1dc4f: 12 lessons, 3 reviews, 3 homeworks (216 screens, quiz questions and items). Stage 0, reduced ledger depth, with a row for every graded key, wrong option, slip, stated rule and command claim. The ledger and the findings below were written before any earlier read was opened.

- Ledger: `docs/reports/audit-terminal-1-3-r2-ledger.md`, 1281 rows: correct 1271, wrong 0, imprecise 4, misleading 6, unverified 0.
- Script: `docs/reports/terminal-L1-3-concepts-r2.py`, 191 checks. It exits 1 at this commit: the two failing checks are findings 1 and 3 and stay failing until the content changes. Same result under CPython 3.13.18 (venv) and 3.12.

## How each claim was checked

- Shell: every command in the course was run in a temporary folder in bash 5.2.21, and in zsh 5.9 wherever the course speaks of zsh or a Mac (the `cd` error wording, `command not found`, globbing, built-ins, the PATH search, `RM_STAR_SILENT`). GNU coreutils and grep supplied `ls`, `mv`, `cp`, `rm`, `mkdir`, `head`, `wc`, `sort`.
- Tab completion: interactive bash and zsh driven through a pty. `cd pro` plus Tab gives `cd projects/` in both. With `data.csv` and `data_old.csv`, one Tab fills `data` and lists nothing in both; the list comes on the next Tab in zsh and on the second in bash. With nothing to fill, zsh lists at once and bash on the second press. Both statements in the course (l5 screen 8, review-2 `rv-tab-two`) hold.
- "A window reads its PATH once": an interactive bash started from an rc file, the rc file then changed, a second bash started. The first still fails to find the program; the second runs it.
- Python: outputs, byte counts and error messages run in CPython 3.11, 3.12 and 3.13. All six tracebacks quoted in the course match character for character, caret lines included. `ZeroDivisionError: float division by zero` is the wording up to 3.13.
- Code widgets: 89 programs (starters, solutions, the three mutants and natural wrong or alternative answers) graded under the page's Pyodide 0.27.7 through `app/tools/code-runner.mjs`. The one `test-N` line (l12 screen 6) is correct: the starter, all three mutants and two more natural slips fail test 1 first.
- Not run: macOS itself. The Mac wordings (`mkdir: data: File exists`, `rm: data: is a directory`, `ls --help` refused, Finder's `Cmd Shift .`) are from the BSD sources and Apple's documentation; `ls` collation in an `en_US` locale (only the C locale is installed here); PowerShell; VS Code. Each such row names its source in the ledger.

## Findings

No `wrong`. Five findings, all minor.

1. l12-first-script.json | screens[3].widget (question, starter, solution, examples, tests) | misleading · minor | The task is a 2% fall, and the hidden tests accept `price = price - 2`. With a start price of 100.00, taking 2 off and taking 2% off give the same number, so a learner who reads a percentage as points is told the answer is right. The explain line says the test on `price` "checks the sum was really done". | Graded under Pyodide: `price = 100.00 / price = price - 2 / print(price)` passes all three tests (the concepts script check `l12 s3 hidden tests reject 'price - 2'` fails). Basis: a wrong program that passes every test. | Use a start price that separates the two. In `starter` and `solution` change `price = 100.00` to `price = 250.00`. Question: "Change one number so the script prints the price after a 2% fall: `245.0`." Set `examples[0].expect` and `tests[0].expect` to `"245.0\n"` and `tests[1].expect` to `"245.0"`. Checked under Pyodide: 250.0 × 0.98 prints `245.0` and 250.0 × 1.04 prints `260.0`; the solution passes, the starter fails test 1, `price - 2` fails test 1, printing 245.0 without computing it fails test 2. Hints, feedback and explain need no change. Add a mutant so the grader keeps the guard: `{ "source": "price = 250.00\nprice = price - 2\nprint(price)\n", "test": 1, "symptom": "takes 2 off instead of 2%: prints 248.0" }`. `docs/reports/terminal-L3-numbers.py` and `terminal-L1-3-concepts.py` state the old figures and need the same change.

2. l7-looking-inside.json | screens[3].explain.text (and the output shown in screens[8].prose) | imprecise · minor | "wc prints `7 prices.csv`" is the GNU and POSIX output. The course has put Ana on a Mac since l5 and quotes Mac wordings for `cd`, `mkdir` and `rm`. BSD `wc` pads the count to a column, so her terminal prints `       7 prices.csv`. | GNU run: `7 prices.csv`. BSD `wc.c` prints each count with `" %7ju"`. POSIX XCU wc specifies `"%d %s\n"`, which macOS does not follow here. | screens[3].explain.text: "wc prints `7 prices.csv`: seven lines, then the file name; a Mac pads the number with spaces. The header is one of them. So the file holds 7 − 1 = 6 price rows."

3. homework-3.json | items[8].widget.postlude (`_runs`, test 10) | imprecise · minor | The test follows the `cd` and `python3` commands in the comment lines, but splits a line only at `&&` and `;`. A learner who writes the two commands in one sentence is told something false. | Graded under Pyodide: `# In a new terminal type cd desk then python3 trade.py` gives "no comment line runs python3"; `# cd desk, then python3 trade.py` gives "cd desk, from /home/sam: no such folder". Both comment lines give the right commands in the right order. | In the postlude replace `_re.split(r"&&|;", _s.lstrip("#"))` with `_re.split(r"&&|;|,|\bthen\b|\band\b", _s.lstrip("#"))`. Checked under Pyodide with the change: the three one-line forms pass, the solution passes, a run with no `cd`, a `cd Desk` and a script with no command comment still fail test 10 with a true report.

4. homework-1.json | items[6].question | imprecise · minor | "The first three return a path to `spx-daily.csv`" does not say which kind. An absolute path is a correct path from `src`, and test 2 refuses it; the only hint is in the generic feedback. | Graded under Pyodide: `from_src()` returning `/home/ana/project/data/spx-daily.csv` fails test 2. | Question: "Complete the four functions. The first two return a relative path to `spx-daily.csv`, the third an absolute one."

5. l12-first-script.json screens[2], [3], [9]; homework-3.json items[5], [8] | feedback.byKey.error | misleading · minor | Five lines begin "Your script stopped with an error". The key `error` fires only when the script cannot load, that is on a SyntaxError. A script that does stop while running (a NameError from a misspelt name, a TypeError from `"Change: " + change`) gets key `test-1` and the generic line, which on screen 10 says "Compare what you printed with the expected text, character by character" to a learner whose script printed nothing. Screen 6 of l12 already has the right pattern. | Graded under Pyodide: on l12 screens[2] and [9] a NameError and a TypeError both give `key=test-1`; an unclosed quote or bracket gives `key=error`. Basis: `docs/AUTHORING.md`, engine pass 7 package 1, item 2. | Reword each `error` line to open as screen 6 does, and add a `test-1` line. l12 screens[2] `error`: "Your script cannot start: Python found a slip in the typing before it ran. Read the last line of the message, then check the quotes and brackets." `test-1`: "Test 1 compares what your script printed with the two lines asked for. If it stopped with an error, read the last line of the message first." l12 screens[3] `error`: "Your script cannot start: Python found a slip in the typing before it ran. Read the last line of the message, then compare with the starting script." l12 screens[9] `error`: "Your script cannot start: Python found a slip in the typing before it ran. Read the last line of the message, then the line number." `test-1`: "Test 1 compares your two printed lines with `Change: 12.5` and `Return: 0.05`. If the script stopped with an error, read its last line, then the line number." homework-3 items[5] and items[8] `error`: "Your script cannot start: Python found a slip in the typing before it ran. Read the last line of the message, then the line it names." items[5] `test-1`: "Test 1 compares your two printed lines with the expected ones. If the script stopped with an error, read the message from the bottom: what went wrong, then which line." items[8] `test-1`: "Test 1 looks for the four labels in order. If the script stopped with an error, read the message from the bottom: what went wrong, then which line." A mutant for l12 screens[9] that first fails test 1: the solution with `change = Friday - monday`.

## Read and left alone

- `~` is taught as a shell shortcut, with the Python caveat and `os.path.expanduser` (l5 screen 6, summary, quiz). The rule "absolute exactly when the first character is `/`" (l3) no longer clashes with it. Run in bash and in Python.
- "Every file sits in exactly one folder", "the command is always the first word" and "the shell opens folder 1 first every time" are Stage 0 models. Hard links, `VAR=x cmd` and the shell's remembered locations change no key in the course.
- "`ls` prints names, not paths" (l5 screen 3, a `why` line) is true for a folder operand, which is the case on screen.
- `grep AAPL prices.csv > prices.csv` (review-2): GNU grep also prints "input file is also the output". The file is empty either way, as the item says.
- homework-3 model (d) shows the traceback as CPython 3.13 prints it; 3.12 adds one caret line under the call. The model says "yours may differ".
- The S&P 500 closes for 2 to 14 January 2014 and the March 2024 AAPL and MSFT closes match the published figures; 2,516 days from 2014 is ten years of sessions.

## Tool results

- Validator: 0 errors.
- `node tools/run-number-scripts.mjs --only terminal`: 5 scripts, 5 passed, before and after this audit's files were added (the runner does not pick up concepts scripts).
- `python docs/reports/terminal-L1-3-concepts-r2.py`: 191 checks, 2 failed (findings 1 and 3), exit 1.
- `node tools/grade-all.mjs --file <each of the 18 files>`: 0 failures in every file. `--code` on l12 and the three homeworks: 0 failures.
- No playthrough, as the brief says.

## Overlap with earlier reads

Read after the ledger and findings 1 to 5 were written: `docs/reviews/audit-terminal-1-3.md` (round 1: 13 findings, its fix pass, its platform table), `docs/reviews/review-terminal-1-3.md` (38 findings, 21 of them conceptual, and its fix pass), the terminal rows of `review-perf-retrofit-14.md` (TM1-1, TM1-2 and its note on `_runs`) and the terminal bullets of `docs/BACKLOG-INBOX.md`. The other reviews that name terminal (`review-git-1-3`, `review-first-python-1-3`, `review-prereq-mapping`, `review-exam-second-item-stage0`) hold no conceptual finding on a terminal file.

| Conceptual findings | Count |
|---|---|
| Found by this audit only | 3 (findings 1, 4, 5) |
| Found by the earlier reads only | 36 (round 1 findings 1 to 13; review-terminal-1-3 findings 1 to 21; perf-retrofit TM1-1, TM1-2) |
| Found by both (same defect) | 2 (findings 2 and 3) |

New `wrong` in this round: 0.

- Finding 2 (BSD `wc` padding): round 1 listed it in its GNU against BSD table ("BSD pads the number with spaces; same fields") and held it. It is raised here as minor because the lesson prints the exact output of a Mac it has named.
- Finding 3 (`_runs` and two commands in one comment line): round 1 sent the same defect to the inbox as a note, with `# cd desk, then python3 trade.py` as its example, and it was not fixed. The fix given here is tested; round 1's other route, a sentence in `how` saying each command needs its own comment line, would also close it.
- Finding 5 is the class of round 1 finding 13, on the five lines that round left alone as "worded for any error". The lines are true when shown; the defect is that the common run-time errors never reach them.
- All 36 earlier findings are fixed at this commit and the fixed text holds under this round's runs. Round 1 rested the zsh half of the Tab wording on the manual; this round ran it in zsh 5.9 through a pty and it holds. The two round 1 `wrong` (homework-3 `h-folders-opened` explain; l5 screens[9] explain) read correctly now.
