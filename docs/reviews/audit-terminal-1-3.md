# Concept audit: terminal, levels 1 to 3 (round 1, blind)

Commit read: aaef9c55. Files: the twelve lessons, `review-1` to `review-3`, `homework-1` to `homework-3` (the course has no `problems-*` or `fluency-*` files). Stage 0, reduced ledger depth, with a row for every graded key, wrong option, slip, stated rule and every claim about what a command does or prints.

- Ledger: `docs/reports/audit-terminal-1-3-ledger.md`, 876 rows: 859 correct, 15 imprecise, 2 wrong, 0 misleading, 0 unverified.
- Concepts script: `docs/reports/terminal-L1-3-concepts.py`, 162 checks run in bash 5.2.21 with GNU coreutils 9.4 and Python 3.13.18 in temporary folders. 154 pass. 8 fail, each a finding below. Exit 1.
- Sources: POSIX (IEEE Std 1003.1-2017; XBD base definitions, XCU shell and utilities), the Bash reference manual, the GNU coreutils manual, the zsh manual, the Python documentation and devguide.

## The simulated terminal

There is none. The course uses only the grid, tree, graph, table and array canvases; `app/js/engine/canvas/console.js` is never referenced by a terminal file, and the code widgets run Python in Pyodide, not a shell. `l1-home-row` screens[0] says so in its first sentence ("the app has no real shell"), and `l12-first-script` screens[2] says its editor "stands in for" the file and that Check runs it "as `python3 hello.py` would". Both statements are true. Every shell exchange in the course is therefore a printed transcript, which is why each one was replayed in a real shell for this audit.

## GNU against BSD and bash against zsh

The course quotes macOS (zsh, BSD tools) wording and says when Linux differs. Checked against the manuals, with the behaviour run on GNU:

| Claim | Where | Verdict |
|---|---|---|
| zsh `cd: not a directory: data/prices.csv`; bash says `Not a directory` | l5 screens[6] | right; the lesson says "On a Mac" |
| `mkdir: data: File exists` on a Mac, "Linux words the error differently" | l6 screens[4] | right (GNU: `cannot create directory 'data': File exists`) |
| `rm: data: is a directory` on a Mac, `Is a directory` on Linux | l6 screens[5] | right |
| Tab lists matches at once in zsh, on a second press in bash | l5 screens[7], review-2 items[5] | right (zsh AUTO_LIST) |
| `ls --help` works on Linux, not on a Mac | l8 screens[8] | right |
| `ls` prints `Downloads  data  notes.txt  projects` | l5 screens[2] | right for macOS byte order; GNU `ls` in an en_US locale prints `data` first. Not a finding: Ana is on a Mac |
| `wc -l` prints `7 prices.csv` | l7 screens[3] | BSD pads the number with spaces; same fields |
| `rm * .csv` deletes at once | homework-2 items[3] | bash only: finding 2 |
| `sed -i`, `date` | not used in the course | nothing to check |

Not taught, so nothing to audit: quoting and word splitting beyond "a space splits a name in two", `2>`, exit status, `&&` and `||`, `chmod`. The permissions column appears once, in the `ls -l` table, unexplained (finding 6).

## Findings

1. `l5-where-am-i.json` | screens[5].explain, screens[9].explain, summary.formula.note, quiz[3].feedback.correct | imprecise, serious | The lesson defines a path that starts with `~` as absolute. `l3-paths` screens[5] has just taught "a path is absolute exactly when its first character is `/`". `~` is not part of a path: the shell replaces it before the command runs, and nothing else does. A learner who carries "`~` paths are absolute and work from anywhere" into level 3 writes `open("~/data/prices.csv")` in a script and gets a file-not-found error. | POSIX XBD 3.2 (an absolute pathname begins with a slash); XCU 2.6.1 and Bash manual 3.5.2 (tilde expansion is done by the shell, on an unquoted word start only). Run: `os.path.isabs('~/data')` is False and `open('~/data/prices.csv')` raises `FileNotFoundError` from a folder where `ls ~/data` works; `ls "~/Downloads"` fails too (concepts script, L5 lines). | Paste-ready:
   - screens[5].prose, after the first sentence, add: "Only the shell understands it: inside a Python script, write the path in full."
   - screens[5].explain, third sentence: "The shell swaps a leading ~ for /Users/ana before cd runs, so a ~ path means the same place from any folder."
   - screens[9].explain, first sentence: "The shell swaps ~ for your home folder, so the path works from any folder."
   - summary.formula.note: "A path that starts with / is absolute. The shell swaps a leading ~ for your home folder, so both work from anywhere in the terminal."
   - quiz[3].feedback.correct: "The shell swaps ~ for your home folder, wherever you are."
   - objectives[1]: "Read a relative path with `..` and a home path with `~` from any folder."
   The key of quiz[3] (`~/data`) stays right.

2. `homework-2.json` | items[3] (`hw-stray-space`), options[right] and explain | imprecise, minor | The key says `rm * .csv` deletes all three files at once. That is bash. In zsh, the macOS default shell that this level quotes for its error messages, `rm` with a lone `*` first asks `zsh: sure you want to delete all 4 files in /Users/ana/x [yn]?` and deletes only on `y`. No option describes that, so a Mac learner who knows it has no right answer. | zsh manual 16.2.6: `RM_STAR_SILENT` ("do not query the user before executing `rm *` or `rm path/*`") is unset by default. The bash behaviour is confirmed by run (concepts script, H2 line). | prose, replace "Your thumb slips:" with "Your shell is bash, and your thumb slips:". explain, add as the last sentence in place of the current one: "zsh on a Mac asks before a lone star; bash does not, so list the matches with ls before any rm with a wildcard."

3. `homework-3.json` | items[1] (`h-folders-opened`), explain | wrong, minor | "Only a command that is not found makes it open all five." A command found in the fifth folder also makes the shell open all five. | The search rule of `l11-command-not-found` screens[6]; POSIX XCU 2.9.1.4. Concepts script, H3 FINDING line. | "The shell opens folder 1, 2 and 3 and finds nothing, then finds `pytest` in folder 4 and stops. It opens all five only when the name is in the last folder or in none."

4. `l10-code-editor.json` | screens[3].canvas.state.caption | imprecise, minor | The caption reads "The pasted line, byte by byte" over 15 cells. Two screens earlier the learner was told one cell is one byte. A curly quote is three bytes in UTF-8, so this line is 15 characters and 19 bytes. | `len('print(“hello”)\n'.encode('utf-8')) == 19` (concepts script, L10 FINDING line); Unicode Standard 3.9, table 3-6 (U+0800 to U+FFFF take three bytes). | caption: "The pasted line, character by character"

5. `l6-making-things.json` | screens[2].prose, summary.ideas[1] | imprecise, minor | "The star ... stands for any characters, even none" and "`*.csv` stands for every name that ends in .csv". A star never matches a leading dot, so the hidden `.prices.csv` of `review-1` items[8] is skipped by `ls *.csv`, `mv *.csv` and `rm *.csv`. | Bash manual 3.5.8 and POSIX XCU 2.13.3 (a leading period must be matched explicitly). Run: `echo *.csv` beside `.prices.csv` prints only `prices.csv` (concepts script, L6 FINDING line). | screens[2].prose, after the first sentence add: "It skips hidden names, the ones that start with a dot." summary.ideas[1]: "A wildcard like `*.csv` stands for every name that ends in .csv, hidden names apart."

6. `l8-options-and-help.json` | screens[0].canvas (columns and state.caption) | imprecise, minor | The table is captioned "The output of ls -l data, one line per file" and has five columns. Real `ls -l` prints a `total` line first, and a link count and a group between the columns shown. A learner comparing with their own terminal sees two unexplained columns and an extra line. | POSIX XCU ls, `-l` output format (mode, links, owner, group, size, date, name); run: one more line than there are files, and 9 fields a line (concepts script, L8 FINDING line). | caption: "The main columns of ls -l data. Your terminal also prints a total line, a link count and a group."

7. `l11-command-not-found.json` | screens[5].explain | imprecise, minor | "Window A's copy is from before the install, so it can never find Python." The copy belongs to that shell, which can change it; a full path also works, as the previous screen taught. | POSIX XBD 8.1 (the environment is copied at exec); run: the same shell finds the program after `PATH=<folder>:$PATH` (concepts script, L11 FINDING line). | "Window A's copy is from before the install, so it goes on missing Python until that copy changes. A new window is the simple way."

8. `l11-command-not-found.json` | screens[0].explain | imprecise, minor | "The shell does this hunt for every command you type." Built-in commands are not searched for. `cd`, `pwd` and `echo`, all taught in this course (echo on the next screen), are built in. | POSIX XCU 2.9.1.4 (built-ins and functions come before the PATH search); run: with an empty PATH, `cd / && pwd && echo ok` still works (concepts script, L11 FINDING line). | "The shell does this hunt for every program you run. A few commands, such as cd and echo, are built into the shell and need no hunt. It takes microseconds." If three sentences must stay three, drop "It takes microseconds."

9. `l9-installing-python.json` | screens[9].prose and canvas; `review-3.json` items[7].prose | imprecise, minor | "The old one needs pandas 1.5; the new one needs pandas 2.2", on Ana's Python 3.12.4 (review-3: "Both run on the same Python"). pandas 1.5 has no build for Python 3.12, so the pictured `.venv` cannot be made with the commands shown. | `pip download pandas==1.5.3 --python-version 3.12 --only-binary=:all:` and the same for 2.0.3: no matching distribution; 2.1.1 and 2.2.3 download (run 2026-11-26). pandas 2.1.1 release notes: first release with Python 3.12 support. | Replace "pandas 1.5" with "pandas 2.1" in l9 screens[9].prose, in its two canvas labels, and in review-3 items[7].prose. No key changes.

10. `l5-where-am-i.json` | screens[9].explain | wrong, minor | "`ls ../../Downloads` also works, but only from backtest." It works from every folder two levels below home. The quiz of the same lesson words the same idea correctly ("works only from a folder one level below home"). | Run from `~/projects/other` (concepts script, L5 FINDING line). | "`ls ../../Downloads` also works, but only from a folder two levels below home."

11. `l7-looking-inside.json` | screens[1].prose (and quiz[2] options[same].why, "It matches the letters exactly as typed") | imprecise, minor | grep is taught as searching for "the text". Its search text is a regular expression. One lesson earlier the learner met the shell's `*`; in grep a star means something else, and a dot matches any character. The lesson's own advice, "pick search text that can only appear where you mean it", fails for a price such as `179.66`. | POSIX XCU grep (basic regular expressions, XBD 9.3). Run: `grep 179.66` matches the line `179x66` (concepts script, L7 note line). | screens[1].prose, after "It looks for the text anywhere in each line." add: "Letters, digits and hyphens match themselves. A dot or a star means something special to grep, so leave them out of search text for now."

12. `l6-making-things.json` | screens[8].feedback.byKey.mk | imprecise, minor | "In your home folder, data already exists, so mkdir would refuse." The item does not say the terminal starts at home, nor that home holds a `data` folder. The general fault of the wrong order is that `data` is made in the wrong place. | The item's prose; run: `mkdir data` succeeds wherever no `data` exists (concepts script, L6 lines). | "You made data before moving into backtest. mkdir makes the folder wherever the terminal is, so data would land in the wrong place."

13. `l12-first-script.json` | screens[5].feedback.byKey.error | imprecise, minor | "Your script still stops with an error. Read its last line: which name is not defined?" The page shows an `error` line only when the script cannot start, which means a syntax error. A script that stops on a NameError, the case this screen is about, is keyed `test-1` and gets the generic line. So this line appears only when no name is undefined. | Run through `app/tools/code-runner.mjs` (the page's harness, Pyodide 0.27.7): the starter (NameError) keys `test-1`; the same script with an unclosed bracket keys `error`; a ZeroDivisionError in screens[9] keys `test-1`. The engine limit is already in `docs/BACKLOG-INBOX.md` under audit first-python, finding 2. The other four `error` lines of the course are worded for any error and stay true. | "Your script cannot start: Python found a slip in the typing before it ran. Read the last line of the message, then check the quotes and brackets."

Severity count: 2 wrong, 11 imprecise, 0 misleading. Serious 1 (finding 1), minor 12.

## What was checked and held

- Every key, wrong option and slip: 142 choice, multi and numeric widgets pass `grade-all`; the tap, order and place keys were derived by hand from the canvases and, where a command is involved, by run.
- All shell transcripts of levels 2 and 3 replayed: `ls`, `cd`, `pwd`, `~`, `..`, `mv`, `cp`, `mkdir`, `rm`, `rm -r`, globs, `grep`, `head`, `wc`, `sort`, `>`, `>>`, pipes, redirect onto the input file, option bundling, PATH order, a command with a slash, `command not found`.
- Every Python message quoted (SyntaxError for a curly quote, `can't open file`, NameError with its suggestion, ZeroDivisionError, TypeError with its caret line, the two-frame traceback of the homework-3 model) matches a real run, line for line, under Python 3.13; the wording is the same in 3.12.
- Code widgets (nine, all Python): there are no `feedback.byKey.test-N` lines in this course, only five `error` lines; four are worded for any error and one is not (finding 13). Every solution passes and every starter fails under Pyodide (`grade-all --code`) and under CPython. Obvious wrong programs are refused: `(new - old) / new` fails `daily_return`; `text.count("")` fails `wc_l`; a trade script run as `python3 desk/trade.py` fails `_runs()`.
- Numbers: WPM and minutes saved, bytes in a file, version order, 2,516 trading days for 2014 to 2023, the S&P 500 closes of January 2014, trade cost £500, proceeds £510, return 0.02.

## Overlap with earlier reads

Read after the ledger and findings 1 to 13 were written: `docs/reviews/review-terminal-1-3.md` (38 findings and its fix pass), and the terminal rows of `review-perf-retrofit-14.md` (TM1-1, TM1-2). The other files that name terminal (`review-git-1-3`, `review-first-python-1-3`, `review-prereq-mapping`, `review-exam-second-item-stage0`) hold no conceptual finding on a terminal file.

| Conceptual findings | Count |
|---|---|
| Found by this audit only | 13 |
| Found by the earlier reads only | 23 (review-terminal-1-3 findings 1 to 21, all `wrong` or `misleading`; perf-retrofit TM1-1 and TM1-2) |
| Found by both (same defect) | 0 |

All 23 earlier findings are fixed at this commit, and the fixed text was re-run here and holds (for example the `two-gt` and `reversed` lines of l7 screens[7], the `ls -C` layout of review-2 items[1], the Tab wording, the regenerated tracebacks). None of this audit's 13 was seen before; 2 are new `wrong` (findings 3 and 10). Nearest misses: the earlier finding 21 touched homework-2 items[3] for the length of its key, not for zsh (finding 2); earlier findings 17 and 18 rewrote l9 screens[8] and [9] without meeting the pandas and Python 3.12 clash (finding 9); perf-retrofit noted that `_runs()` refuses `cd "$HOME/desk"` and judged it out of scope, as this audit does.

## Checks run

- `cd app && node tools/validate.mjs`: 0 errors.
- `node tools/run-number-scripts.mjs --only terminal`: 5 of 5 passed, exit 0.
- `node tools/grade-all.mjs --file <each of the 18 files> --local-cdn <pkgs>`: 142 widgets, 0 failures. With `--code` on the four files that hold code: 9 Python widgets run, 0 failures.
- `python docs/reports/terminal-L1-3-concepts.py`: 154 OK, 8 FAIL (findings 1, 3, 4, 5, 6, 7, 8, 10), exit 1. Findings 2 and 9 rest on the zsh manual and a `pip download` run, finding 11 on a passing note line, finding 12 on the item's own prose, finding 13 on the node run named there.
- The author's number scripts (`terminal-L1-numbers.py` to `L3`, the two perf scripts) were run, not read, before the findings were written.
- No playthrough, as the auditor rules say.

## Fix pass

Opus fixer, from commit 21641674. Every command below was run in bash 5.2 (and zsh 5.9 where named) in a scratch folder before the text was written.

1. Fixed (wider than the paste-ready text). Basis: `echo ~/data` prints the home path in bash and zsh, `ls "~/data"` fails, and in Python `os.path.isabs('~/data')` is False, `open('~/data/prices.csv')` raises FileNotFoundError and `os.path.expanduser('~/data')` gives the absolute path. l5 objectives[1] ("a home path with `~`"), screens[5].prose ("a shell shortcut"), screens[5].explain (the shell swaps ~ for the absolute /Users/ana before cd runs; Python does not, use the full path or `os.path.expanduser`), screens[8].explain (the audit missed "the absolute `cd ~/data`"), screens[9].explain, summary.formula.note and quiz[3].feedback.correct. Key of quiz[3] and the id `q-absolute` unchanged.
2. Fixed. Basis: in bash `rm * .csv` expands to every name plus `.csv` (deletes the three files, refuses charts, reports `.csv`; the concepts H2 check runs it); in an interactive zsh 5.9 under a pty it asks `zsh: sure you want to delete all 4 files in ... [yn]?` and, on n, runs nothing. The course otherwise quotes zsh on a Mac, so the item now says "Your shell is bash, the usual one on Linux", and the explain says zsh on a Mac would ask first. Key unchanged.
3. Fixed. Basis: strace of bash with five PATH folders: a name in folder 4 stats folders 1 to 4, a name in folder 5 stats 1 to 5, a missing name stats 1 to 5. Explain: "It opens all five only when the name is in folder 5 or in none of them." Key 4 unchanged.
4. Fixed. Basis: `len('print(“hello”)\n')` is 15 characters and 19 UTF-8 bytes, and the array has 15 cells. Caption "The pasted line, character by character".
5. Fixed. Basis: beside `.prices.csv`, `echo *.csv` prints only `prices.csv` in bash and zsh (POSIX XCU 2.13.3, leading period). l6 screens[2].prose and summary.ideas[1] say hidden names are skipped.
6. Fixed. Basis: GNU `ls -l` on four files prints five lines, the first `total N`, then 9 fields a line (mode, links, owner, group, size, three date fields, name); BSD `ls -l` has the same total line and columns. Caption names the total line, link count and group.
7. Fixed. Basis: in one bash, `PATH=/nonexist; python3` gives command not found, then `PATH=<folder>:$PATH; python3` runs it. Explain: "typing python3 there goes on failing until that copy changes. A new window is the simple fix." Key unchanged.
8. Fixed. Basis: `type cd echo pwd` says shell builtin in bash and zsh; with `PATH=`, `cd / && pwd && echo ok` works and `ls` gives 127. Explain: every program you run; cd and echo are built in and need no hunt. "It takes microseconds" dropped to keep three sentences.
9. Fixed. Basis: PyPI JSON for pandas: 1.5.3, 2.0.3 and 2.1.0 have no cp312 file; 2.1.1, 2.1.4 and 2.2.3 have cp312 wheels. "pandas 1.5" becomes "pandas 2.1" in l9 screens[9].prose, its one canvas label and review-3 items[7].prose (pip picks the newest 2.1.x, which has a 3.12 wheel). No key changes.
10. Fixed. Basis: `ls ../../Downloads` works from `~/projects/other` and fails from `~/data`. Explain: "only from a folder two levels below home".
11. Fixed. Basis: `grep 179.66` matches `179x66`, `grep 'a*'` matches every line, `grep 03-04` matches the literal date only (BRE, POSIX XBD 9.3). l7 screens[1].prose adds that letters, digits and hyphens match themselves and a dot or a star is special. quiz[2] `same` why ("matches the letters exactly as typed") is about case and stays true for letters; unchanged.
12. Fixed. Basis: `mkdir data` in a folder with no `data` makes it there; the item never says where the terminal starts. byKey `mk`: mkdir makes the folder wherever the terminal is, so data would land where you started, not in backtest.
13. Fixed. Basis: through `tools/code-runner.mjs` (Pyodide 0.27.7), the starter and three NameError codings (Monday on line 2; line 3 as `Friday - Monday`; `fridy` on line 1) and a sign slip all key `test-1`; an unclosed bracket and a stray quote key `error`. The NameError line moved to a new `byKey.test-1` (worded so it is also true for a wrong value); `byKey.error` now speaks of a script that cannot start. The three NameError codings added as `mutants` (test 1). No test, key or solution changed.

Concepts script: the eight FINDING checks encoded the old wording; each is re-pointed to the fixed text with the same run now asserting the true behaviour, and checks for findings 2, 9, 11, 12 and 13 were added (docstring says so). 168 OK, 0 FAIL, exit 0.

Gates on the eleven edited files: validator 0 errors; voice-scan 35: 0 and 0; `run-number-scripts --only terminal` 5 of 5; `grade-all --code --file` (11 files): 91 widgets, 7 Python code widgets with mutants, 0 failures; playthrough desktop and `--mobile` of l5 to l12, homework-2, homework-3 and review-3: all passed (22 runs).
