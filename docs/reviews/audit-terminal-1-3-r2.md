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

## Fix pass

Opus fixer, from commit 05489751. Every program named below was submitted under the page's Pyodide 0.27.7 through `app/tools/code-runner.mjs`; the key and first failing test are the runner's.

1. l12 screens[3] | fixed differently | Basis: under rule 4 the three existing tests, starter and solution stay; one hidden test is added, `run_from(250.00)` expecting 245.0 (isclose), where a hidden postlude reruns the learner's script with its first `price = <number>` set to 250.0, output suppressed. 250 × 0.98 = 245 and 250 − 0.02 × 250 = 245; 250 − 2 = 248. Submitted: solution passes; `* (1 - 0.02)`, `*= 0.98`, `price - price * 0.02`, `* 98 / 100` and `price = 100` pass; starter fails test 1; `price - 2`, `price -= 2`, `price - 2.0`, `price = 98.0` and line 1 `100.00 - 2` fail test 4 only. New `test-4` line (2 off or typing 98 is right only from 100), `test-1` line, `how` names test 4, explain's third sentence now says what test 4 does. Seven `mutants` (four on test 4, three on test 1). `terminal-L3-numbers.py` and the round 1 script need no change, as the 98.0 figures stand.
2. l7 screens[3].explain | fixed | Basis: FreeBSD and Apple text_cmds `wc.c` print each count as `" %7ju"`, so macOS shows `       7 prices.csv`; GNU prints `7 prices.csv`. The explain now says a Mac pads the number with spaces first (two sentences); the key 7 is unchanged.
3. homework-3 items[8] `_runs` | fixed | Basis: the split now takes `&&|;|,|\bthen\b|\band\b`. Graded: the solution and 11 right forms pass test 10 (`cd desk then python3 trade.py` in a sentence, `cd desk, then ...`, `cd ~/desk, ...`, `... and ...`, `&&`, `;`, two lines, absolute `cd`, `$ ` prompts, `Run: ... then ...`, `python3.12`); nine wrong forms fail test 10 only, each with a true report (no `cd`, `cd ~/Desk` on two lines or one, `python` on two lines or one, no command line, `python3 desk/trade.py`, the two commands in the wrong order, `python3` with no name).
4. homework-1 items[6].question | fixed | Basis: tests 1, 2 and 4 compare with relative strings and test 3 with the absolute one (`equal`), so an absolute path from `src` fails test 2. Question: the first two return a relative path, the third an absolute one, the fourth a relative path to the results folder.
5. five `byKey.error` lines | fixed | Basis: submitted, a NameError, a TypeError and an endless loop all give `test-1`; an unclosed quote or bracket and a missing comma give `error`. Each `error` line now opens "Your script cannot start: Python found a slip in the typing before it ran", and each widget has a `test-1` line that covers both a wrong print and a script that stopped. Mutants on test 1: l12 s2 four (`print(hello)`, `Print`, capitals, order), l12 s9 four (`Friday - monday`, `"Change: " + change`, `Ret`, lower-case label), homework-3 items[5] four (`Old`, text + number, no `f`, no `* 100`), items[8] four (`"Cost: " + cost`, `Buy`, `Profit =`, labels out of order).

Gates: validator 0 errors; voice scan 35: 0 and 0; `terminal-L1-3-concepts-r2.py` 191 checks, 0 failed, exit 0 (no check re-pointed); `terminal-L1-3-concepts.py` 168 OK, exit 0; `run-number-scripts --only terminal` 5 of 5; `grade-all --code` on the four files, 8 code widgets, 0 failures (mutants included); playthrough of l12, l7, homework-1 and homework-3, desktop and `--mobile`, all passed.

## Fix-pass read

Fresh reader, blind to this file and to the course's scripts until the rows below were written. Read: `git show 48fb4124 -- app/content/courses` (four files). Runs are under the page's Pyodide 0.27.7 through `tools/code-runner.mjs` (the page's harness and worker grader): 151 submissions of my own, none of them the committed mutants. `grade-all.mjs --code` on the four files: 8 code widgets, 0 failures (so all 23 mutants first fail the test they name).

| # | file | JSON path | claim | verdict | basis |
|---|---|---|---|---|---|
| 1 | homework-1 | items[6].question | Functions 1 and 2 return a relative path to the file, 3 an absolute one, 4 a relative path to the results folder | correct | The four keys are `data/spx-daily.csv`, `../data/spx-daily.csv`, `/home/ana/project/data/spx-daily.csv`, `../results`: resolved by hand from each stated folder. An absolute path no longer satisfies the wording of 1 or 2. `./data/...` is also relative but `./` is not taught in L1 to L4 and `how` says the string must match exactly |
| 2 | l7-looking-inside | screens[3].explain.text | `wc -l` prints `7 prices.csv`; a Mac pads the number with spaces first; 7 − 1 = 6 rows | correct | Apple `text_cmds` `wc/wc.c`: `xo_emit_h(xop, " {:lines/%7ju/%ju}", linect)` then `" {:filename/%s}\n"`, so macOS prints `       7 prices.csv`. GNU coreutils prints `7 prices.csv` for one file. Seven lines in the canvas table, one header |
| 3 | l12-first-script | screens[2].feedback.byKey.test-1 | Test 1 compares the output with `hello` and `Ready to code`; a NameError comes from missing quotes or a capital in `print` | correct | Run: `print(ready)`, `PRINT(...)` give NameError and key test-1; `print("hello", "Ready to code")`, lower-case `r`, trailing full stop give test-1 |
| 4 | l12-first-script | screens[2].feedback.byKey.error | The `error` key means the script cannot start (a slip found before it ran); check quotes and brackets | correct | Run: unclosed quote, unquoted words, unclosed bracket, stray indent all give key `error` with a SyntaxError or IndentationError and no output. Every runtime error I tried (NameError, TypeError, ZeroDivisionError, ModuleNotFoundError, EOFError, a 5 s timeout) gives `test-N`, never `error` |
| 5 | l12-first-script | screens[2].widget.mutants (4) | Each first fails test 1, with the stated symptom | correct | `grade-all --code` 0 failures; symptoms read against the sources |
| 6 | l12-first-script | screens[3].widget.tests[3] | `run_from(250.00)` is 245.0 | correct | 250 × 0.98 = 245; also 250 − 2% of 250 = 250 − 5 = 245. Run: model solution gives actual `245.0` and passes all four; the starter fails (test-1, prints 104.0) |
| 7 | l12-first-script | screens[3].widget.postlude | `run_from` reruns the script with the first `price = <number>` set to the start, and returns the final `price` | correct | Run. Pass: `price - price * 0.02`, `price * (1 - 0.02)`, `*= 0.98`, `0.98 * price`, `price * 98 / 100`, `.98`, no spaces, `price = 100`, `price = 100.0`, one-line `price = 100.00 * 0.98`, a leading comment, a trailing comment, no final newline. Fail at test 4: `price - 2` (248.0), `price - 2.00`, `price -= 2`, `price = 98.00` on line 2 (98.0), one-line `price = 98.0` (250.0), `price * 1.04 - 6` (254.0). Residual, not natural under "Change one number": a first line rewritten as `+100.00`, `float(100)`, `1e2` or under another name fails test 4 with a correct 2% line |
| 8 | l12-first-script | screens[3].widget.how | Tests 2 and 3 look at `price` and the printed lines; test 4 reruns from 250.00 | correct | Matches `tests[1..3]` |
| 9 | l12-first-script | screens[3].widget.mutants (7) | Four fail test 4 first, three test 1, with the stated values | correct | `grade-all --code`; `price * 0,98` prints `(0.0, 98)` (run); 250 − 2 = 248; `100.00 - 2` becomes `250.0 - 2` = 248 |
| 10 | l12-first-script | screens[3].feedback.byKey.test-1 | Test 1 expected 98.0; the script may have stopped with an error | correct | Run: `* 0.02` (2.0), `* 0.8` (80.0), `/ 1.02` (98.039...), integer `price = 98` (prints `98`), `prise` and `Print` NameErrors all give test-1 |
| 11 | l12-first-script | screens[3].feedback.byKey.test-4 | From 250.00 a 2% fall gives 245.0; taking 2 off or typing 98 is right only from 100 | correct | x − 2 = 0.98x only at x = 100; a constant 98 equals 0.98x only at x = 100. Run: `price - 2` and `price -= 2` give key test-4 with 248.0; typed `98.0` gives test-4 |
| 12 | l12-first-script | screens[3].feedback.byKey.error | Cannot start; compare with the starting script | correct | Run: `print(price` and `0.98.` give key `error`, SyntaxError |
| 13 | l12-first-script | screens[3].explain.text | Test 4 reruns from 250.00, where 98% is 245.0 and taking 2 off gives 248.0 | correct | 0.98 × 250 = 245; 250 − 2 = 248; run as row 7 |
| 14 | l12-first-script | screens[9].widget.mutants (4) | Each first fails test 1 | correct | `grade-all --code` |
| 15 | l12-first-script | screens[9].feedback.byKey.test-1 | Test 1 compares the two lines with `Change: 12.5` and `Return: 0.05` | correct | 262.50 − 250.00 = 12.5; 12.5 ÷ 250 = 0.05. Run: `"Change:" + str(change)`, bare numbers, `change / friday` (0.0476...), reversed change, `Monday` and `chnage` NameErrors all give test-1 |
| 16 | l12-first-script | screens[9].feedback.byKey.error | Cannot start; read the last line, then the line number | correct | Run: unclosed quote and an uncommented step line give key `error`. Note for the engine, not the content: the page's message carries a first frame `line 7, in <module>` that is the harness's own, above the true `line 6` |
| 17 | homework-3 | items[5].widget.mutants (4) | Each first fails test 1; `{r1:.2f}%` prints 0.04% | correct | `grade-all --code`; 0.04 to two decimals is 0.04 |
| 18 | homework-3 | items[5].feedback.byKey.test-1 | Test 1 compares the two lines with `Day 1: 4.00%` and `Day 2: -2.00%` | correct | 4 ÷ 100 = 0.04; −2.08 ÷ 104 = −0.02. Run: `.1f`, commas with no format, no `%`, one line only, `/ new` (3.85%), no brackets, a percent returned and multiplied again (400.00%), `odl` and `R1` NameErrors all give test-1 |
| 19 | homework-3 | items[5].feedback.byKey.error | Cannot start; read the last line, then the line it names | correct | Run: unclosed quote, unindented `return`, unclosed bracket give key `error` |
| 20 | homework-3 | items[8].widget.postlude (`_runs` split) | Commands in one comment line are split at `,`, `then` and `and`, and each report is true | imprecise (minor) | Run, 50 comment headers. All 16 plain right forms return `ok`; all 19 wrong forms fail with a true report (`cd desk, cd desk, python3 trade.py` passes, and it does run: the second `cd` fails and leaves the shell in `desk`). But a right header in backticks, quotes or brackets, or joined by `AND`, returns `no comment line runs python3`, which is false. So does one line joined by `followed by`, `before`, `->` or a single pipe, where the rest of the line is read as arguments to `cd`. Fix below |
| 21 | homework-3 | items[8].widget.mutants (4) | Each first fails test 1 | correct | `grade-all --code`; `Profit` stored then `profit` read gives NameError (run) |
| 22 | homework-3 | items[8].feedback.byKey.test-1 | Test 1 looks for the four labels in order | correct | The test's `match` is `Cost:…Proceeds:…Profit:…Return:`. Run: no Return line, lower-case labels, Profit before Proceeds, no colons, bare numbers, `Fee` NameError, NameError on the last print, ZeroDivisionError all give test-1; right labels with the fee forgotten give test-2 |
| 23 | homework-3 | items[8].feedback.byKey.error | Cannot start; read the last line, then the line it names | correct | Run: `£12.25`, unclosed bracket, uncommented `cd ~/desk` give key `error` |

Counts: 23 rows; correct 22, imprecise 1 (minor), wrong 0, misleading 0, unverified 0.

### Fix for row 20 (homework-3 `items[8].widget.postlude`, inside `_runs`)

Replace the split line

```python
        for _seg in _re.split(r"&&|;|,|\bthen\b|\band\b", _s.lstrip("#")):
```

with

```python
        for _seg in _re.split(r"&&|;|,|\bthen\b|\band\b", _re.sub(r"[`\"'()]", " ", _s.lstrip("#")), flags=_re.I):
```

and, in the `cd` branch, add after the `else: _last = "cd " + ... ": no such folder"` line, at the indent of `if _to in _DIRS:`

```python
                if any(_a.startswith("python") for _a in _args[1:]):
                    _last = "put python3 on its own comment line, below the cd line"
```

Basis: run in CPython against the committed postlude on 23 headers. The backtick, quote, bracket and `AND` forms then return `ok`; the `followed by`, `before`, `->`, `|` and `&` forms report the new line; every plain right form still returns `ok`, every wrong form keeps its report, and the model solution returns `ok`. Add one mutant per new branch if the fixer applies it.

Notes, no verdict: (a) in l12 `screens[3]`, a script that ends with `exit()` fails test 4 with `name 'run_from' is not defined`, since the postlude never runs; not a Stage 0 coding. (b) the spurious harness frame in a SyntaxError message (row 16) is an engine item.

## Fix-pass follow-up (Opus)

Opus fixer, from commit 56950689. Every header below was submitted under the page's Pyodide 0.27.7 through `app/tools/code-runner.mjs`, with the model solution's body below it; shell claims were run in bash. Runs and scripts: `scratchpad/fix-term-3/` (`mk.py`, `mine.py`, `sub.mjs`, `exit.py`, `syn.mjs`).

1. Row 20 (homework-3 `items[8]` `_runs`) | fixed differently | Basis: the reader's two lines applied, plus two changes my own headers showed were needed. (a) A quote just before `~` is kept (`[`\"'()](?!~)`): with the reader's line, `# cd "~/desk"` then `# python3 trade.py` returned `ok`, but bash does not swap a quoted `~` (`cd: ~/desk: No such file or directory`, then python3 looks in `/home/sam`). It now reports `python3 trade.py from /home/sam looks for /home/sam/trade.py`, which is what happens. (b) The mirror of the reader's cd branch: `# Run python3 trade.py after cd desk` reported the `/home/sam/trade.py` path, read in the written order; it now reports `put cd on its own comment line, above the python3 line`. Results: the reader's 23 headers give the reader's expected result each (10 right forms `ok`, 5 joined forms the new cd line, 8 wrong forms their old report). My 10: `First cd ~/desk, Then ...`, single quotes, `THEN`, `(cd desk && python3 trade.py)` (a bash subshell, it runs) pass; quoted `~`, `cd Desk followed by ...`, `&& python trade.py`, `cd ..`, `after`, backticks joined by `->` fail test 10 only, each report true. The model solution passes all ten tests; the starter fails test 1 first, as before; the four existing mutants still fail test 1 first. Three mutants added on test 10 (`followed by`, `after`, quoted `~`).
2. Note (a), l12 `screens[3]` and `exit()` | recorded in BACKLOG-INBOX | Basis: run. The harness wraps the learner's code and the postlude in one `except SystemExit`, so the postlude never runs; with `except SystemExit` around `run_from`'s `exec` the solution plus `exit()` still fails test 4 with the NameError. The same helper as a prelude with that guard passes it, which is more than a one-line change; no content edit.
3. Note (b), SyntaxError harness frame | recorded in BACKLOG-INBOX | Basis: run. `print("Return:" ret)` on line 9 of l12 `screens[9]` gives `File "solution.py", line 7, in <module>` above the true line 9.

Script: `terminal-L1-3-concepts.py`'s NOTE check on `cd "desk"` encoded the old refusal and was re-pointed (docstring says so): `cd "desk"` is now accepted and a quoted `~` refused.

Gates: validator 0 errors; voice scan 35 on homework-3: 0 and 0; `terminal-L1-3-concepts-r2.py` 191 checks, 0 failed; `terminal-L1-3-concepts.py` 168 OK, exit 0; `run-number-scripts --only terminal` 5 of 5; `grade-all --code --file homework-3` 2 code widgets, 0 failures (mutants included); playthrough of homework-3 desktop and `--mobile`, all passed.

## Orchestrator note

The Opus follow-up (230a7372) changed hidden checker code in homework-3 items[8] (`_runs`) and added one learner report string ("put cd on its own comment line, above the python3 line"). The orchestrator read the diff; the fixer ran 33 headers under Pyodide with true reports and checked the quoted `~` case in bash. No further fix-pass read was run. The l12 `exit()` edge and the SyntaxError frame note are in docs/BACKLOG-INBOX.md.
