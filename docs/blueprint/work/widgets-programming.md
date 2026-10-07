# Widget catalogue: programming (Python, tools, algorithms, C++, contests)

Blueprint work file, Stage 2 Phase 1. Draft 1, 6 October 2026.

**Scope.** Every interactive widget needed to teach curriculum items 1.1 Python (core language, NumPy, pandas, matplotlib), 1.2 Tools (Git and GitHub, the Linux command line, SQL, pytest), 1.8 Data structures and algorithms, 1.9 C++ and 2.4 Contests, at the depth a top quantitative programme expects, and to prepare for each item's exit test. Widgets that other clusters reuse are specified once here and flagged.

**Read for this file.** `docs/curriculum.md`; `docs/design-research.md` sections 2, 4, 5, 8, 9 and 10; the Stage 1 prototype (`css/tokens.css`, `js/core.js`, `js/data.js`, `js/screens/lesson.js`, `drill.js`, `drill-worker.js`, `exam.js`, `review.js`); the sibling catalogues `widgets-stage0.md` and `widgets-calc-linalg.md`; the owner's lesson-creator, maths-teaching, code-craft and project-forge skills with `engineering-floor.md` and `blueprint.md`; the Artifact `sample` and `db` contracts (version 0.2.69).

**Sources the lessons follow.** CS50P (Harvard) and Automate the Boring Stuff for the core language; Wes McKinney, Python for Data Analysis (3rd edition) for NumPy, pandas and matplotlib; MIT's The Missing Semester for the shell, Git and tooling; SQLBolt for SQL; the pytest documentation; Grokking Algorithms, the NeetCode 150 list and CLRS (reference) for 1.8; learncpp.com for 1.9; Codeforces practice conventions and Project Euler for 2.4. The content is recreated from general knowledge of these courses; no text is copied.

**Evidence tags**, as in the design research: [verified], [sourced], [inferred], [our choice], and [unverified] for anything not yet measured or confirmed.

**Numbering.** Course and lesson numbers (1.1.1 to 1.1.4, 1.2.1 to 1.2.5, 1.8.1 to 1.8.5, 1.9.1 to 1.9.4, 2.4.1, and L1, L2 inside them) are this catalogue's working outline, written to test coverage. The course-architecture blueprint owns the final outline; renumbering changes no widget.

---

## 0. Summary

- **68 specified entries: 61 new widgets and 7 extensions** of widgets that other catalogues already specify.
  - New: 4 primitives (`diff-view`, `array-strip`, `cell-grid`, `node-link`) and 57 composites.
  - Extended: the primitives `code-surface`, `text-terminal`, `stepper` (trace mode) and `value-table` (frame mode), and the Stage 0 composites `shell-sim`, `workspace-sim` and `setup-checklist`.
- **Priority.** 44 entries are P0 (everything 1.1 and 1.2 need, because the depth-first build runs to 1.5), 22 are P1 (1.8, 1.9 and two optional 1.2 lessons) and 2 are P2 (2.4). Several P0 widgets carry P1 or P2 modes, marked in their entries.
- **Generators.** 51 new widgets need seeded item generators; 5 more use seeds only to vary authored items (section 11).
- **Ownership.** This cluster owns `code-cell`, the code exercise widget that `widgets-calc-linalg.md` assigns to it. It absorbs Stage 0's `code-editor`. Stage 0 lessons configure `code-cell` with one Python file.
- **The organising rule** of this cluster: authored code runs at build time, learner code runs at runtime (decision 1). It is why nearly every lesson screen works in the Artifact whatever the WebAssembly probe finds.

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Where code runs | **Authored code runs at build time; learner code runs at runtime.** CI executes every authored snippet and ships its output, execution trace, result set, figure and compiler messages as data | Running authored code live on each device | Lesson screens then work on both targets regardless of the Artifact's WebAssembly verdict, start instantly, and cannot drift from what CI checked |
| 2 | Code exercises | One `code-cell` for Python, SQL, C++ and shell, with runner adapters behind one test protocol | A drill widget per language | One results view, one check type, one set of tutor hooks |
| 3 | Python in the Artifact | MicroPython with ulab for drills that CI tags as compatible, if WebAssembly is allowed; otherwise a handoff to the web app | Skulpt or Brython; our own interpreter; renaming Pyodide's archives to a served extension | Skulpt and Brython compile to JavaScript and run it through `eval` or `Function`, which a policy that blocks WebAssembly almost certainly blocks too [inferred]; an interpreter would be a second Python with its own bugs; renaming archives sidesteps a host restriction (section 13.1) |
| 4 | Execution traces | One `Trace` format (section 2.3), recorded by a `sys.settrace` recorder on CPython pinned to Pyodide's minor version at build time, and by the same module inside Pyodide at runtime | Hand-written traces; scraping a debugger | Identical traces from both sources, with stable object ids |
| 5 | Algorithm animations | Instrumented JavaScript generators (`algo-trace`), each paired with the Python source the learner sees. CI runs that Python under the recorder and requires the same output and the same sequence of (event, line) pairs | Hand-authored keyframes; Python-only traces | Random instances must be generated at runtime in the Artifact, where Python may be absent; CI keeps the two implementations honest |
| 6 | NumPy and pandas visuals | Small JavaScript semantic cores (`nd-core`, `frame-core`) for interactive manipulation, CI-checked against NumPy and pandas on generated cases | Calling pandas on every drag | A selection drag must redraw in one frame on a phone; Pyodide cannot answer that fast, and the Artifact may have no pandas at all |
| 7 | SQL | The official SQLite WebAssembly build on both targets; build-time result sets for authored queries; seed banks (section 11.1) when WebAssembly is unavailable | AlaSQL; our own SQL engine | SQLite is the dialect of Python's `sqlite3`, which learners use next; AlaSQL's semantics differ and it compiles queries with `Function` |
| 8 | Git | Our own `git-model`: the real object model (blobs, trees, commits, refs, index, reflog) with SHA-1 over a deterministic clock | isomorphic-git; a pointer-only toy | isomorphic-git does not implement rebase, cherry-pick or stash [unverified for its latest release]; a toy cannot show the three trees or a conflict |
| 9 | C++ | Concept widgets everywhere from build-time compiler output; drills on the web through in-browser Clang if a spike meets the budget, else through the proxy to Compiler Explorer; the 1.9 exit timing always runs locally | C++ drills inside the Artifact | The Artifact cannot hold a compiler sysroot without archives, and WebAssembly timings would misstate native speed |
| 10 | Grading efficiency | Two probes: a line-event budget under `sys.settrace`, and the time ratio between two input sizes measured beside the reference solution on the same device | Wall-clock alone; line counts alone | Wall-clock varies by device; line counts miss work done inside C built-ins such as `x in some_list` |
| 11 | Trees, graphs and memory diagrams | One `node-link` primitive with deterministic layouts (tidy tree, layered, fixed, circular, grid, outline, heap, row). Objects keep their positions across steps | A separate heap-diagram primitive; force-directed layout at runtime; Graphviz in WebAssembly | One renderer, one keyboard model, one set of tutor ids; determinism keeps consecutive steps comparable; no extra WebAssembly |
| 12 | Editor | Keep Stage 0's textarea-over-highlight `code-surface` through P1. Switch only if a measured trigger fires: files over 300 lines, highlighting over 2 ms per keystroke on the reference device, or a need for multiple cursors | CodeMirror 6 or Monaco now | The prototype proves the textarea on phones; Monaco does not support mobile browsers [sourced, Microsoft's stated support policy, recalled] |
| 13 | Many valid answers | Algorithms with ties (BFS, DFS, topological sort, Dijkstra with equal keys) are graded by predicates that accept any valid order, unless the lesson states a tie rule | Fixed expected orderings | A fixed answer punishes correct reasoning |
| 14 | Tutor and code | Bertie never edits code. Before a pass, the engine strips code blocks longer than 2 lines from hint replies. After a pass, Bertie can review the learner's code in the owner's code-craft format at a chosen depth | Tutor-applied fixes | Keeps "never the answer" mechanical and checkable |
| 15 | Phones | Every `code-cell` drill derives a Parsons version automatically from its reference solution, with mutant lines as distractors, offered below 768px | Blocking code drills on phones | Typing code on a phone is slow; a daily streak should not need a keyboard |
| 16 | Python version | Content must run on CPython 3.11 (the Stage 0 setup minimum) and on Pyodide's CPython. CI runs every reference solution on both | Pyodide's version only | Learners run the same code on their own machines |

### 0.2 Findings that shape the widgets

- **The 1.1 exit test is a finance computation.** Returns, annualised volatility and maximum drawdown from daily prices need `csv-inspector`, `time-series-lab` and `drawdown-lab` inside 1.1, not only in 1.7. `drawdown-lab` is shared with the finance cluster.
- **Two exits cannot be fully checked in the browser.** The 1.2 exit (a Git repository with a test) and the 1.9 exit (native timing of a C++ pricer) happen on the learner's machine. `setup-checklist` gains a project mode that verifies by pasted output, and on the web app by GitHub's public API (section 6.11).
- **"A fresh LeetCode medium in 30 minutes" needs unseen problems.** The 1.8 exit implies a held-out bank of at least 30 medium problems that practice never shows [our estimate]. This is a content requirement, but `problem-workbench` must support a held-out flag.
- **Interview patterns are a curriculum, not a list.** NeetCode 150's categories (arrays and hashing, two pointers, sliding window, stack, binary search, linked list, trees, tries, heaps, backtracking, graphs, advanced graphs, 1-D and 2-D dynamic programming, greedy, intervals, maths and geometry, bit manipulation) each need an action-first widget. Section 1.3 covers every category, and the coverage check at the end of section 1 maps each to its lessons.
- **The pandas version decides some lessons.** Copy-on-write and the string dtype changed defaults in pandas 3 [unverified: the exact pandas version Pyodide ships at build time]. Lessons on views, copies and chained assignment must be written against the pinned version, and CI fails if the pin moves without a content review.

---

## 1. Lesson map: what the learner does to get each idea

Each row is one lesson. "Act" is the hook: the action taken before any rule is read. "Check" is the main answer type. A lesson's Explore screen uses the same widgets in `explore` mode, with no check.

### 1.1 Python (1.1, 150 h; CS50P, Automate the Boring Stuff, McKinney)

**1.1.1 Python foundations** (32 lessons; builds on Stage 0's first scripts)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Names refer to objects | After `a = 5; b = a; a = 6`, then `x = [1]; y = x; x.append(2)`, drag each name's arrow to the object it refers to before stepping | code-tracer (predict), node-link (heap layout) | mapping |
| 2 | Integers, floor division, modulo, `**`; Python's ints never overflow | Predict `-7 // 2`, `-7 % 2` and `2 ** 100`; place the floor on a number line | predict-output, number-line | text, numeric |
| 3 | Floats are binary fractions | Type 0.1 and find the stored double; drag to its neighbours; explain `0.1 + 0.2 != 0.3`; use `math.isclose` | float-inspector | numeric with tolerance, choice |
| 4 | Rounding and money: `round(2.5)`, `Decimal` | Predict `round(0.5)`, `round(1.5)`, `round(2.5)`; switch to `Decimal` with an explicit rounding mode | float-inspector (decimal), predict-output | text |
| 5 | Strings: indexing, slicing, immutability | Drag slice handles on a character strip; the widget writes `s[2:7:2]`; then type slices and predict | array-strip (chars), predict-output | text, set |
| 6 | f-strings and the format mini-language | Toggle spec parts until `1234567.891` prints as `1,234,567.89` and `0.0731` as `7.31%` | format-lab | text |
| 7 | Booleans, truthiness, short-circuit `and`/`or` returning operands | Tap the lines that run; predict `0 or "x"` and `[] and f()` | code-tracer (tap executed lines), predict-output | set, text |
| 8 | Loops: `for` over iterables, `range` stops before `stop`, `while`, `break`, `continue`, loop `else` | Predict how many times a body runs; step the loop variable; order shuffled loop lines | code-tracer, parsons | numeric, ordering |
| 9 | Functions: `def`, `return` against `print`, `None` | Find the function that returns `None`; bind call arguments to parameters by dragging | code-tracer, token-tray (screen from primitives), code-cell | set, mapping, code |
| 10 | Default and keyword arguments; the mutable default trap | Call `append_to(1)` twice and predict the second result; watch the shared default list | code-tracer, predict-output | text |
| 11 | Scope and frames: local, enclosing, global, built-in; `UnboundLocalError` | Tap which `x` each line reads; read the error and find its cause | code-tracer (scope highlight), diagnostic-reader | mapping, set |
| 12 | Lists: mutation, aliasing, shallow and deep copies; `x = x.sort()` | Draw arrows after `b = a`, `b = a[:]` and `b = copy.deepcopy(a)` on a nested list | code-tracer (predict), predict-output | mapping, text |
| 13 | Tuples, unpacking, immutable containers holding mutable objects | Predict whether `t[0].append(1)` works when `t = ([],)` | code-tracer, predict-output | choice, text |
| 14 | Dictionaries: keys, lookup, `get`, counting, insertion order | Hash a key into a bucket; try a list as a key and read the error | hash-table (basic), diagnostic-reader | numeric, choice |
| 15 | Sets and membership cost | Race `x in list` against `x in set` as $n$ grows; count steps | complexity-lab (race), hash-table | choice, numeric |
| 16 | Nested data and JSON | Tap a value deep in a price feed; read off its path; type a path and see it light | json-explorer | text (path), set |
| 17 | Comprehensions | Assemble a comprehension from the parts of a loop; predict a nested comprehension's order | parsons, code-blanks, predict-output | ordering, code, text |
| 18 | Iterators and generators; laziness; exhaustion | Pull items one at a time through `map`, `filter` and a generator; predict a second `list(gen)` | pipeline-flow (iter), code-tracer (suspended frames) | text, choice |
| 19 | Functions as objects, `lambda`, `key=`, closures; late binding in loops | Sort records by a key you build; predict `[f() for f in fs]` for closures made in a loop | sort-lab (key), code-tracer (closure cells) | ordering, text |
| 20 | Stable sorts and multi-key sorting | Sort trades by symbol, then by time, two ways; spot which order keeps ties | sort-lab (key, stability) | ordering |
| 21 | Exceptions: reading tracebacks; `raise`; `try`/`except`/`else`/`finally`; catching too broadly | Tap the frame where the bug starts; predict which blocks run | diagnostic-reader, code-tracer (unwinding) | set, text |
| 22 | Files and paths: `open`, `with`, encodings, `pathlib`, the working directory | Run a script from the wrong folder and fix the path | workspace-sim, file-tree, code-cell | state, code |
| 23 | CSV by hand: `csv` module against `split(",")` | Find the rows that `split` breaks: quoted commas, empty fields | csv-inspector (csv module) | set, code |
| 24 | Modules, imports, `sys.path`; shadowing; `if __name__ == "__main__"` | A local `random.py` breaks `import random`: find which file wins | search-path (sys.path), diagnostic-reader | choice, ordering |
| 25 | Virtual environments, `pip` and `PATH` | Activate a venv and watch `which python3` change; install into the wrong interpreter and diagnose | search-path (PATH), shell-sim | state, choice |
| 26 | Command-line arguments: `sys.argv`, `argparse` | Run a script with arguments in the terminal; predict `sys.argv` | workspace-sim, shell-sim | text, state |
| 27 | Regular expressions | Write a pattern that matches every ticker on the left and nothing on the right | regex-lab | text (graded by match sets) |
| 28 | Classes: instances, attributes, methods, `self`, `__init__`, `__repr__` | Step through object creation; follow attribute lookup from instance to class | code-tracer, code-cell | mapping, code |
| 29 | Dunder methods, inheritance against composition, dataclasses | Make `Money` objects compare and print; predict method resolution | code-cell, code-tracer | code, text |
| 30 | Debugging: breakpoints, stepping, watches; `assert` | Set a breakpoint, read a value, find the line where the total goes wrong | code-tracer (debug) | numeric, set |
| 31 | Reading and explaining code | Match each block of a worked solution to its purpose; raise the depth to read line by line | code-annotator | mapping |
| 32 | Notebooks and reproducibility | Run notebook cells out of order, then "Restart and run all" and find what broke | code-cell (notebook) | choice, state |

**1.1.2 NumPy** (12 lessons; McKinney chapter 4)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Why arrays: one dtype, contiguous memory, vectorised operations | Race a Python loop against one array expression at $n = 10^3$ to $10^6$ | bench-lab (race), ndarray-lab | numeric, choice |
| 2 | Dtypes; `int64` wraps where Python ints do not; upcasting | Predict `np.int64(2**62) * 4` and `np.array([1, 2]) / 2` dtypes | ndarray-lab (dtype), predict-output | text |
| 3 | Shape and axes | Tap an axis to sum along it; predict the result's shape, with and without `keepdims` | ndarray-lab (axes) | text, choice |
| 4 | 2D indexing and slicing | Drag slice handles on both axes; the widget writes `a[1:, ::2]`; then type and predict | ndarray-lab (slice), cell-grid | text, set |
| 5 | Views, copies, strides; `reshape`, transpose | Change a value through a slice and watch the original change; see transpose swap strides on the buffer | ndarray-lab (memory) | choice, mapping |
| 6 | Boolean masks, `np.where`, fancy indexing returns copies | Build a mask by tapping a condition; predict which assignments change the original | ndarray-lab (mask) | set, choice |
| 7 | Broadcasting | Align shapes from the right; stretch size-1 dimensions; fix the $(n,)$ against $(n, 1)$ trap with `[:, None]` | broadcast-lab | text (shape), code |
| 8 | Reductions, `ddof=0` against `ddof=1` | Predict `std` with each `ddof`; explain which estimates a sample | ndarray-lab (reduce), predict-output | numeric |
| 9 | Random numbers: `default_rng`, seeds, reproducible simulation | Seed a random walk; reproduce a colleague's figure | code-cell, sim-runner | code |
| 10 | Matrix products: `@` against `*`; shape rules | Predict which products are legal and their shapes | broadcast-lab (matmul), matrix-multiply (calc-linalg) | text, choice |
| 11 | Vectorising a loop: `cumsum`, `diff`, `maximum.accumulate` | Rewrite a running-maximum loop as one call; pass a time-ratio test | code-cell (complexity test) | code |
| 12 | NaN propagation, `nan`-functions, summation order | Predict `np.mean([1, np.nan])`; sum $10^6$ copies of 0.1 three ways | float-inspector (summation), predict-output | text, numeric |

**1.1.3 pandas** (23 lessons; McKinney chapters 5 to 8, 10 and 11)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Series: values plus an index; alignment in arithmetic | Add two Series with different dates; tap the rows that become NaN | dataframe-lab (align) | set |
| 2 | DataFrame anatomy: columns, index, dtypes, `info`, `describe` | Tap the object-dtype column that should be numeric | dataframe-lab | set, choice |
| 3 | `[]`, `loc` and `iloc`; label slices include the end | Drag a selection rectangle and read the `loc` and `iloc` expressions; predict `df.loc["2024-01-02":"2024-01-04"]` row count | dataframe-lab (select) | text, numeric |
| 4 | Boolean filtering; `&`, `\|`, parentheses | Fix `df[df.a > 0 & df.b < 5]` and explain the error | dataframe-lab (filter), diagnostic-reader | code, choice |
| 5 | New columns; vectorised against `apply` against `iterrows` | Add a column three ways and race them | code-cell, bench-lab (race) | code, numeric |
| 6 | Missing data; forward fill is safe for prices, backward fill looks ahead | Fill gaps both ways and spot the value that came from the future | dataframe-lab (missing), time-series-lab | set, choice |
| 7 | Copy-on-write and chained assignment | Predict whether `df[df.a > 0]["b"] = 0` changes `df` under the pinned pandas | dataframe-lab (copy), predict-output | choice |
| 8 | `read_csv`: `parse_dates`, `index_col`, `thousands`, `na_values` | Toggle options until the dates parse and "1,234" becomes a number | csv-inspector (pandas) | code, set |
| 9 | Sorting, ranking, `value_counts`, duplicates | Rank returns with ties three ways; predict `rank(method="min")` | dataframe-lab (sort), sort-lab | ordering, numeric |
| 10 | GroupBy: split, apply, combine; `agg` against `transform` | Drag rows into groups by sector; predict the output shape of `agg` and `transform` | groupby-lab | mapping, text |
| 11 | Merge and join; duplicate keys multiply rows; `validate`, `indicator` | Draw the match lines; predict the row count before running | join-lab | numeric, set |
| 12 | `concat` and alignment of columns | Stack two frames with different columns; predict the shape | join-lab (concat) | text |
| 13 | Reshaping: `pivot`, `pivot_table`, `melt`, `stack`, `unstack`, MultiIndex | Drag column names into index, columns and values; predict the wide table | reshape-lab | mapping, text |
| 14 | Categoricals, `get_dummies`, `cut` against `qcut` | Bin returns into equal widths and into quantiles; compare counts | reshape-lab (dummies), number-line, marks | set, numeric |
| 15 | DatetimeIndex, date ranges, frequencies, business days | Generate trading days for a month; find the missing holiday | time-series-lab (dates) | set, text |
| 16 | `shift`, `pct_change`, log returns; look-ahead with `shift(-1)` | Slide a price column down one row; tap the return that used tomorrow's price | time-series-lab (shift), drawdown-lab | set, code |
| 17 | Resampling daily to weekly and monthly; OHLC | Drag the bin edges; predict which day labels the week under `label="right"` | time-series-lab (resample) | mapping, text |
| 18 | Rolling and expanding windows; `min_periods`; `center=True` leaks the future; `ewm` | Slide the window bracket; compare the weights of `rolling(20)` and `ewm(span=20)` | time-series-lab (rolling) | numeric, set |
| 19 | Time zones; New York close in London time across daylight saving | Convert a close timestamp on the two dates when the clocks change | time-series-lab (tz) | text |
| 20 | Volatility: standard deviation of returns, annualisation by $\sqrt{252}$ | Drag the window and read the annualised volatility; predict the effect of using prices instead of returns | drawdown-lab (vol) | numeric |
| 21 | Drawdown: running maximum, drawdown series, maximum drawdown and its dates | Drag peak and trough handles to the largest fall | drawdown-lab | point, numeric |
| 22 | Method chains | Order the stages of a cleaning pipeline; inspect each intermediate | pipeline-flow (pandas) | ordering, text |
| 23 | Memory and speed: dtypes, `category`, `memory_usage`; avoiding Python loops | Shrink a frame's memory by choosing dtypes | dataframe-lab (dtype), bench-lab | numeric |

**1.1.4 Plotting and the 1.1 exit project** (7 lessons; McKinney chapter 9)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Figure, Axes and Artists; pyplot against the object-oriented interface | Tap a code line to light its element, and tap an element to find its line | plot-workbench (anatomy) | mapping |
| 2 | Price lines with dates; labels, titles, direct labels against legends | Fill the blanks so the figure passes its checks | plot-workbench (build), code-cell (figure tests) | code |
| 3 | Log scale for prices | Toggle the scale; explain why equal percentage moves look equal | plot-workbench (fix) | choice, predicate |
| 4 | Histograms of returns; bins; a normal overlay shows fat tails | Change the bin count; find the bins that hold more than the normal predicts | plot-workbench, stat-chart (Stage 0) | set, choice |
| 5 | Subplots and shared axes: price, returns, drawdown stacked | Assemble a three-panel figure from code tokens | plot-workbench (build) | code |
| 6 | Misleading charts: truncated axes, dual axes, chosen windows | Fix three charts with toggles | plot-workbench (fix) | predicate |
| 7 | **Exit project**: prices CSV to returns, annualised volatility, maximum drawdown and plots, in-app then on your machine | Build it in the workspace against hidden tests, then run it locally and paste the output | workspace-sim, code-cell, drawdown-lab, setup-checklist (project) | code, state |

### 1.2 Tools (1.2, 40 h; The Missing Semester, SQLBolt, pytest documentation)

**1.2.1 The command line** (13 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Commands, arguments, flags, `man` and `--help`; quoting names with spaces | Fix `cp my file.csv data/` in the terminal | shell-sim | state |
| 2 | Streams: stdin, stdout, stderr; `>`, `>>`, `2>`, `/dev/null` | Send errors to one file and results to another | shell-sim, pipeline-flow (shell) | state |
| 3 | Pipes and text tools: `grep`, `sort`, `uniq -c`, `wc`, `head`, `tail`, `cut`, `tr` | Build a pipeline one stage at a time to find the most-traded symbol; inspect each intermediate | pipeline-flow (shell), shell-sim | state, ordering |
| 4 | Globbing is done by the shell; quoting stops it | Predict which files `*.csv` and `"*.csv"` reach | regex-lab (glob), shell-sim | set |
| 5 | `grep` with regular expressions over logs | Extract the error lines for one date | regex-lab, shell-sim | state |
| 6 | `sed` and `awk` essentials (P1 subset) | Replace a delimiter; sum a column | shell-sim (sed and awk), pipeline-flow | state |
| 7 | Permissions, `ls -l`, `chmod`, the shebang; "Permission denied" | Make a script runnable; set `640` by tapping bits | permission-bits, shell-sim | text, state |
| 8 | Environment variables and `PATH` | Reorder `PATH` so the venv's Python wins | search-path (PATH), shell-sim | ordering, state |
| 9 | Shell scripts: variables, `$1`, quoting, `for` over files, `if`, exit codes, `&&`, `set -euo pipefail` | Make a script that processes every CSV and stops on the first failure | shell-sim (script), code-cell (shell) | state |
| 10 | Processes and jobs: `ps`, `kill`, Ctrl+C, `&`, `jobs`, `fg` (P1) | Stop a runaway script; bring a job back | shell-sim (jobs) | state |
| 11 | Remote machines: `ssh`, `scp`, keys (P1) | Copy results from a simulated server | shell-sim (multi-host) | state |
| 12 | Editing in the terminal: `nano` (P0); Vim survival (P1) | Change one line of a config file and save | shell-sim (nano), vim-sim | state |
| 13 | Finding things: `find`, `xargs`, `grep -r` | Find every test file changed by a task | shell-sim | state |

**1.2.2 Git and GitHub** (14 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A commit is a snapshot with a parent | Commit three times and watch the graph grow | git-graph | state |
| 2 | The three trees: working directory, index, HEAD; `add`, `commit`, `status`, `diff`, `diff --staged` | Move a change between the three trees until `status` matches the target | git-graph (three trees), diff-view | state |
| 3 | Reading history: `log`, `show`, `diff A..B`, `blame` | Find the commit that changed a constant | git-graph, diff-view | set |
| 4 | Undoing: `restore`, `reset --soft/--mixed/--hard`, `revert`; which are safe after a push | Predict where each `reset` leaves the branch and the files | git-graph | state, choice |
| 5 | Branches are pointers; HEAD; detached HEAD | Make the graph match a target with branch and switch only | git-graph | state |
| 6 | Merging: fast-forward and three-way | Predict whether a merge makes a new commit | git-graph | state, choice |
| 7 | Conflicts | Resolve a conflict, then find the semantic conflict that only the tests catch | merge-conflict | code, state |
| 8 | Rebase, interactive rebase; new hashes; never rewrite shared history | Squash three commits; predict which hashes survive | git-graph (rebase) | state |
| 9 | Remotes: `clone`, `fetch`, `pull`, `push`; tracking branches; a rejected push | Recover from a rejected push without force | git-graph (remote) | state |
| 10 | GitHub flow: fork, branch, pull request, checks, review, merge | Take a change from branch to merged pull request | git-graph (remote, checks), code-review | state |
| 11 | Code review | Flag the bug, the missing test and the leaked key in a pull request | code-review | set |
| 12 | `.gitignore` and secrets; a committed secret is compromised | Write ignore rules; watch a key survive in history after deletion | regex-lab (gitignore), git-graph | set, choice |
| 13 | `git bisect` is binary search over commits | Find the bad commit in the fewest steps | git-graph (bisect) | numeric, state |
| 14 | `stash`, `cherry-pick`, `reflog` recovery | Recover a commit after `reset --hard` | git-graph | state |

**1.2.3 SQL** (16 lessons; SQLBolt plus quant extras)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Tables, rows, columns; `SELECT` | Predict the result grid of a query, then run it | predict-output (table), code-cell (SQL) | resultset |
| 2 | `WHERE`: comparisons, `AND`/`OR` precedence, `IN`, `BETWEEN`, `LIKE` | Write the filter that returns exactly the target rows | code-cell (SQL), pipeline-flow (SQL) | resultset |
| 3 | `ORDER BY`, `LIMIT`, `OFFSET`, `DISTINCT` | Fetch the third page of a ranking | code-cell (SQL) | resultset (ordered) |
| 4 | `NULL` and three-valued logic; `IS NULL`; `COUNT(*)` against `COUNT(col)` | Fill a truth table for `NULL`; predict two counts | value-table (screen from primitives), predict-output | set, numeric |
| 5 | Logical order of a query; why `WHERE` cannot see a `SELECT` alias | Order the clauses by when they run; inspect each intermediate table | pipeline-flow (SQL) | ordering |
| 6 | Aggregates, `GROUP BY`, `HAVING` against `WHERE` | Predict which filter removes rows before grouping | groupby-lab (SQL) | resultset, choice |
| 7 | Joins: inner, left, full; duplicate keys multiply rows; joins are not Venn diagrams | Draw match lines; predict the row count | join-lab (SQL) | numeric, resultset |
| 8 | Self-joins, anti-joins, `NOT EXISTS` | Find the days a stock did not trade | join-lab, code-cell (SQL) | resultset |
| 9 | Subqueries and `WITH` | Rewrite a nested query as named steps | pipeline-flow (SQL), code-cell | resultset |
| 10 | Window functions: `ROW_NUMBER`, `RANK`, `LAG` for returns, rolling `AVG ... OVER` | Compute daily returns per ticker without leaking across tickers | groupby-lab (window) | resultset |
| 11 | Dates as ISO strings; SQLite date functions | Group trades by month | code-cell (SQL) | resultset |
| 12 | `INSERT`, `UPDATE`, `DELETE`; an `UPDATE` without `WHERE`; transactions | Predict the table after each statement; roll back a mistake | predict-output (table), code-cell (SQL) | resultset, state |
| 13 | `CREATE TABLE`, types, primary and foreign keys, constraints; normalisation (P1) | Create a schema that rejects a bad row; split a wide table (P1) | code-cell (SQL), schema-builder | state |
| 14 | SQL from Python; parameters; injection | Type an input that turns a query into "return everything", then fix it | injection-lab, code-cell | text, code |
| 15 | SQL into pandas; where to aggregate | Load a query into a frame and match a pandas groupby | code-cell | code |
| 16 | Indexes and query plans (P2, optional) | Read `EXPLAIN QUERY PLAN` before and after an index | code-cell (SQL), tree-lab (b-tree) | choice |

**1.2.4 Testing with pytest** (12 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A test is an executable specification | Write two `assert`s that catch a broken function | mutant-hunter (intro) | learner tests |
| 2 | pytest discovery, running, reading the report, assertion introspection | Tap the line of the report that shows the wrong value | code-cell (pytest), diagnostic-reader (pytest) | set |
| 3 | What to test: boundaries, equivalence classes, empty and single inputs | Kill every mutant of a drawdown function | mutant-hunter | learner tests |
| 4 | Floats in tests: `pytest.approx`, relative and absolute tolerance | Make a test pass for a correct float result and fail for a wrong one | mutant-hunter, float-inspector | learner tests |
| 5 | `pytest.raises` with `match` | Test that bad input raises the right error | code-cell (pytest) | code |
| 6 | `@pytest.mark.parametrize` and test ids | Turn five copied tests into one | code-cell (pytest) | code |
| 7 | Fixtures, `yield` teardown, scopes, `tmp_path`, `conftest.py` | Predict the setup and teardown order of three tests | node-link and stepper (screen from primitives, build-time `--setup-show` data), code-cell | ordering, code |
| 8 | Test-driven development: red, green, refactor | Write the failing test first, then the code | code-cell (tests first) | code |
| 9 | Testing data code with small synthetic frames | Test `max_drawdown` on hand-made series | mutant-hunter | learner tests |
| 10 | Coverage and its limits (P1 overlay) | Reach full coverage and still leave a mutant alive | mutant-hunter (coverage) | choice |
| 11 | Property-based testing with Hypothesis (P1) | State a property that kills a mutant the examples miss | mutant-hunter (property), counterexample-lab | learner tests |
| 12 | Continuous integration: tests on every push | Read a failing check on a pull request and fix it | git-graph (checks), diagnostic-reader | state |

**1.2.5 Exit** (1 lesson)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | The 1.1 project in a Git repository with at least one test, pushed to GitHub | Rehearse in the workspace, then do it locally; paste `git log`, `pytest -q` and the repository URL | workspace-sim, setup-checklist (project) | state |

### 1.3 Data structures and algorithms (1.8, 250 h; Grokking Algorithms, NeetCode 150, CLRS as reference)

**1.8.1 Algorithmic thinking and complexity** (8 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Linear against binary search | Play guess-the-number with and without halving; count guesses for $n = 1{,}000$ | binary-search-lab (game), complexity-lab | numeric |
| 2 | Growth rates; dominant terms; constants matter only for small $n$ | Rank six functions by growth, then find the crossover where $100n$ loses to $n^2$ | complexity-lab (growth), token-tray | ordering, numeric |
| 3 | Counting steps in code | Predict the step count of nested and halving loops; compare with line-hit counts | complexity-lab (code), code-tracer (hits) | expression, choice |
| 4 | Best, worst, average; amortised cost | Append to a dynamic array and read the average copies per append | dynamic-array, complexity-lab | numeric, choice |
| 5 | Space complexity; recursion depth | Predict the deepest stack for a recursive sum | recursion-tree, complexity-lab | numeric |
| 6 | Constraints to a target complexity | For $n \le 2 \times 10^5$ and 1 second, pick the complexities that fit in Python and in C++ | complexity-lab (budget) | choice |
| 7 | Measuring complexity: time at $n$ and $2n$; log-log slope | Read an exponent off a log-log plot | complexity-lab (timing), bench-lab | numeric |
| 8 | Recurrences, recursion-tree cost, the master theorem | Fill the work per level of $T(n) = 2T(n/2) + n$ | recursion-tree (cost) | expression |

**1.8.2 Arrays, hashing and pointer patterns** (15 lessons; NeetCode arrays and hashing, two pointers, sliding window, binary search, intervals)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Arrays in memory; $O(1)$ index, $O(n)$ insert at the front | Insert at index 0 and count the shifts | array-strip, dynamic-array | numeric |
| 2 | Hash tables: hashing, buckets, collisions, load factor, resizing | Insert keys until a resize; predict the probes for a lookup | hash-table | numeric, choice |
| 3 | Hashing patterns: complement lookup, counting, grouping by signature | Solve two-sum with a dictionary; group anagrams by sorted key | hash-table, array-strip, code-cell | code |
| 4 | Prefix sums and products; difference arrays | Answer ten range-sum queries in $O(1)$ each; build product-except-self | range-query-lab | numeric, code |
| 5 | Two pointers from both ends; why moving the shorter side is safe | Move the pointers on a sorted array; watch the pair grid eliminate rows | pointer-walk (opposite, pair grid) | state, code |
| 6 | Three-sum, in-place dedupe, partitioning | Run the Dutch national flag partition by hand | pointer-walk (same direction, flag) | state, code |
| 7 | Fixed sliding window; best time to buy and sell | Slide a window; keep the running minimum price | pointer-walk (window) | numeric |
| 8 | Variable sliding window and its invariant | Grow and shrink a window with no repeated characters | pointer-walk (window), hash-table | state, code |
| 9 | Monotonic deque: sliding window maximum | Push and pop the deque by hand | stack-queue-lab (monotonic deque), pointer-walk | state, code |
| 10 | Binary search: invariants, half-open intervals, off-by-one; `bisect_left` against `bisect_right` | Move `lo` and `hi` as the algorithm would; find the infinite loop | binary-search-lab | state, code |
| 11 | Binary search on the answer | Find the smallest shipping capacity on a true/false strip | binary-search-lab (predicate) | numeric, code |
| 12 | Rotated arrays; searching a sorted matrix | Decide which half is sorted at each step | binary-search-lab (rotated, matrix) | choice, code |
| 13 | Sorting: insertion, merge, quick, heap, counting; stability; the $\Omega(n \log n)$ comparison bound | Be the algorithm for each sort; count comparisons on sorted and reversed input | sort-lab | ordering, numeric |
| 14 | Kadane's algorithm; maximum subarray | Track "best ending here" as the strip is scanned | dp-table (1D, running) | numeric |
| 15 | Intervals: merge, insert, non-overlapping (greedy by end), meeting rooms | Sweep a line across a timeline; merge as you go | interval-sweep | state, numeric |

**1.8.3 Linear structures** (11 lessons; NeetCode stack, linked list, heap)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Stacks: valid brackets, Reverse Polish evaluation, min stack | Push and pop while scanning a bracket string | stack-queue-lab | state, code |
| 2 | Monotonic stack: daily temperatures, largest rectangle in a histogram | Pop while the new bar is lower; read each popped bar's area | stack-queue-lab (monotonic), array-strip (bars) | numeric, code |
| 3 | Queues and deques; `deque` against `list.pop(0)`; ring buffers; a queue from two stacks | Run 10,000 pops both ways and compare steps | stack-queue-lab, complexity-lab | choice |
| 4 | Linked lists: nodes, pointers, traversal, insert, delete, the dummy head | Rewire arrows to delete a node without losing the tail | linked-list-lab | state |
| 5 | Reverse a linked list in place | Move `prev`, `curr` and `nxt` tags and rewire one arrow per step | linked-list-lab | state, code |
| 6 | Fast and slow pointers: middle, Floyd's cycle detection, find the duplicate | Predict where the pointers meet; derive why restarting finds the cycle start | linked-list-lab (cycle) | numeric |
| 7 | Merge two sorted lists; merge $k$ lists with a heap | Splice nodes from two lists into one | linked-list-lab, heap-lab | state, code |
| 8 | LRU cache: hash map plus doubly linked list | Process get and put calls; predict the evicted key | linked-list-lab (LRU) | state, code |
| 9 | Binary heaps: a complete tree stored in an array; sift up and down; `heapq` is a min-heap | Swap nodes to restore the heap after a push and a pop | heap-lab | state |
| 10 | Heapify in $O(n)$; heap sort | Heapify bottom-up and total the work per level | heap-lab | numeric |
| 11 | Top-$k$, $k$-way merge, two heaps for a running median | Keep a size-$k$ heap over a stream of returns | heap-lab | code |

**1.8.4 Trees and graphs** (15 lessons; NeetCode trees, tries, graphs, advanced graphs)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Tree vocabulary; recursion on trees | Annotate every node with its height, bottom-up | tree-lab (recursion) | numeric |
| 2 | Pre-, in- and post-order; level order | Tap nodes in visit order for each traversal | tree-lab (traversal) | ordering |
| 3 | Tree recursion patterns: invert, same tree, diameter, balanced, maximum path sum | Separate what a call returns from what it records globally | tree-lab (recursion), recursion-tree | numeric, code |
| 4 | Binary search trees: search, insert, delete; validating with bounds | Drag a key down the tree; validate a tree that fools the parent-only check | tree-lab (BST) | state, choice |
| 5 | Balance: sorted inserts make a list | Insert 1 to 7 in order and in a shuffled order; compare heights | tree-lab (balance) | numeric |
| 6 | Lowest common ancestor, $k$th smallest, build from traversals, serialise | Rebuild a tree from preorder and inorder | tree-lab (construct) | state, code |
| 7 | Tries | Insert words; count words with a prefix | tree-lab (trie) | numeric, code |
| 8 | Graph representations; directed and undirected; implicit graphs | Convert a drawing into an adjacency list and a matrix | graph-search (represent) | mapping, state |
| 9 | BFS: layers, shortest unweighted paths, multi-source BFS, grids | Pop the queue and colour each layer; read the distances | graph-search (BFS) | ordering, numeric |
| 10 | DFS: components, flood fill, cycle detection with three colours | Count islands on a grid; find the back edge | graph-search (DFS) | numeric, set |
| 11 | Topological sort: Kahn's algorithm and DFS post-order | Remove zero in-degree nodes in turn; detect an impossible schedule | graph-search (topo) | ordering |
| 12 | Union-find with union by rank and path compression | Union pairs and watch a find flatten its path | union-find | state, numeric |
| 13 | Dijkstra's algorithm; why negative edges break it | Settle nodes from the priority queue; find the graph where it fails | shortest-path | numeric, ordering |
| 14 | Bellman-Ford and the $k$-stops variant; minimum spanning trees by Prim and Kruskal | Relax every edge per round; pick edges for an MST | shortest-path (Bellman-Ford, MST), union-find | numeric, set |
| 15 | Eulerian paths: reconstruct an itinerary (optional) | Walk every edge once with Hierholzer's splice | graph-search (euler) | ordering |

**1.8.5 Recursion, dynamic programming, greedy, bits and method** (17 lessons; NeetCode backtracking, 1-D and 2-D DP, greedy, maths and geometry, bit manipulation)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Recursion: base case, call stack, call tree | Predict the number of calls for `fib(6)` | recursion-tree, code-tracer | numeric |
| 2 | Backtracking: subsets, permutations, combination sum; choose, explore, unchoose | Grow the state-space tree; cross out the branches that cannot succeed | recursion-tree (backtrack) | set, code |
| 3 | Constraint pruning: N-Queens, word search | Place queens; prune at the first conflict | recursion-tree (backtrack), cell-grid | numeric |
| 4 | Overlapping subproblems; memoisation turns a tree into a DAG | Tap repeated calls; watch the tree collapse | recursion-tree (memo) | numeric |
| 5 | Bottom-up tables: state, transition, order (house robber, coin change) | Fill the table cell by cell; tap the cells each cell reads | dp-table | numeric |
| 6 | Two-dimensional DP: grid paths, LCS, edit distance; reconstruction | Fill an edit-distance table; trace back the edits | dp-table (2D, reconstruct) | numeric, set |
| 7 | Knapsack and subset sum; rolling arrays; loop direction | Fill one row in the wrong direction and watch an item count twice | dp-table (space) | choice, code |
| 8 | State-machine DP: buying and selling with a cooldown | Fill three state rows; follow the transitions | dp-table (states) | numeric |
| 9 | Longest increasing subsequence: $O(n^2)$ and $O(n \log n)$ | Run patience sorting with binary search on the tops | dp-table, binary-search-lab | numeric |
| 10 | DP on strings: word break, palindromic substrings; interval DP (optional) | Fill the table by increasing length | dp-table | code |
| 11 | Greedy choices and exchange arguments; counterexamples | Break the greedy rule for coins $\{1, 3, 4\}$; prove earliest-end scheduling by swapping | counterexample-lab (greedy), interval-sweep (schedule) | text (input), set |
| 12 | Greedy classics: jump game, gas station, partition labels | Track the furthest reach while scanning | array-strip and stepper (screen from primitives), code-cell | code |
| 13 | Bits: binary, two's complement, XOR tricks, masks, counting bits, fast power | Flip bits to build a mask; find the single number by XOR | bit-lab | numeric, text |
| 14 | Matrix problems: rotate, spiral, set zeroes | Rotate by layers on a grid | cell-grid and stepper (screen from primitives) | state |
| 15 | The method: understand, examples, brute force, optimise, code, test, analyse | Work a medium through every stage | problem-workbench (guided) | code, free text |
| 16 | Stress testing a solution | Run brute force against your fast solution until they disagree | counterexample-lab (stress) | text (input) |
| 17 | Timed practice; the 150 problems; a fresh medium in 30 minutes | Solve under a clock | problem-workbench (timed) | code |

### 1.4 C++ (1.9, 140 h; learncpp.com)

**1.9.1 C++ foundations** (9 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Source to program: preprocess, compile, assemble, link | Drag files through the stages; match each error message to the stage that raised it | compile-pipeline | ordering, mapping |
| 2 | First program; compiling on your machine | Compile and run hello world locally; paste the output | code-cell (C++), setup-checklist (C++ toolchain) | stdout, state |
| 3 | Fundamental types and sizes; signed overflow is undefined, unsigned wraps | Count up past the maximum on a 4-bit wheel; predict `UINT_MAX + 1` | bit-lab (C++), memory-layout | numeric, choice |
| 4 | Initialisation, narrowing, `const`, `constexpr` | Predict which lines compile; read the narrowing error | predict-output (C++), diagnostic-reader (compiler) | set |
| 5 | Functions, pass by value, overloading | Step a call and see the copy in the new frame | code-tracer (C++) | mapping |
| 6 | Integer and floating division; conversions; signed and unsigned comparison | Predict `-1 < 1u` and `7 / 2 * 2.0` | predict-output (C++), bit-lab | text |
| 7 | Multiple files: headers, declarations and definitions, include guards, the one-definition rule, linker errors | Split a program across three files; fix "undefined reference" | compile-pipeline (multi-file), diagnostic-reader | set |
| 8 | Reading compiler errors, including template error walls | Tap the first error that matters in a 60-line report | diagnostic-reader (compiler) | set |
| 9 | Build tools: Make and CMake; incremental builds | Edit a header and tap every object that must rebuild | compile-pipeline (build graph) | set |

**1.9.2 Memory and objects** (14 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | The stack: frames, locals, lifetime by scope | Predict which variables exist at each line | code-tracer (C++) | set |
| 2 | References and `const` references; returning a reference to a local | Draw the alias; spot the dangling reference | code-tracer (C++) | mapping, choice |
| 3 | Pointers: addresses, dereference, `nullptr`, arithmetic over arrays | Predict addresses as a pointer walks an array of `double` | code-tracer (C++), memory-layout | numeric |
| 4 | Arrays: `std::array`, decay of C arrays; out of bounds is undefined | Read an AddressSanitizer report | array-strip (C++), diagnostic-reader (sanitizer) | set |
| 5 | Heap allocation: `new`, `delete`, leaks, double free, use after free | Step through and mark each block's fate | code-tracer (C++ heap) | set |
| 6 | Classes: members, constructors, initialiser lists, destructors, invariants | Write a class whose invariant survives every constructor | code-cell (C++) | code |
| 7 | RAII: destructors at scope exit, including during an exception | Predict the destructor order as an exception unwinds | ownership-lab, code-tracer (unwinding) | ordering |
| 8 | Copying: copy constructor and assignment; shallow copies of raw pointers | Copy an object that owns a buffer and watch the double free | ownership-lab | state |
| 9 | Moving: rvalues, `std::move`, moved-from state; the rules of zero, three and five | Move an owner and predict both objects' states | ownership-lab | state, choice |
| 10 | Smart pointers: `unique_ptr`, `shared_ptr` counts and cycles, `weak_ptr` | Predict `use_count`; break a leaking cycle with a `weak_ptr` | ownership-lab | numeric, state |
| 11 | Struct layout: alignment and padding | Reorder fields to shrink `sizeof` | memory-layout | numeric, state |
| 12 | Inheritance and virtual functions; vtables; slicing; virtual destructors | Follow a call through the vtable; predict which function runs | code-tracer (C++ vtable) | text |
| 13 | Lambdas and captures by value and by reference | Predict output when a captured reference outlives its object | code-tracer (C++), predict-output | text |
| 14 | Exceptions against error codes; `noexcept` | Choose the error strategy for a pricing function | choice (screen from primitives), code-cell | choice, code |

**1.9.3 The standard library and performance** (8 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | `std::vector`: size, capacity, reallocation, `reserve`, iterator invalidation | Push past capacity; watch an iterator dangle | dynamic-array (C++) | numeric, choice |
| 2 | Containers and their costs: `vector`, `deque`, `list`, `map`, `unordered_map`, `set`, `priority_queue` | Pick the container for five workloads | complexity-lab, hash-table, tree-lab, heap-lab (screens) | choice |
| 3 | Algorithms and iterators: `std::sort` with a comparator, strict weak ordering, `lower_bound`, `accumulate` | Find why a `<=` comparator crashes a sort | sort-lab (C++), code-cell (C++) | code, choice |
| 4 | Templates: instantiation and deduction | Predict which instantiations the compiler makes | code-surface side by side (screen from primitives), diagnostic-reader | choice |
| 5 | Cache locality: contiguous memory, row-major traversal | Traverse a matrix by rows and by columns; count cache lines loaded | memory-layout (cache), bench-lab | numeric |
| 6 | Benchmarking: optimisation levels, warm-up, repeats, variance, dead-code elimination | Spot the benchmark the compiler optimised away | bench-lab (rigorous) | choice, numeric |
| 7 | Testing C++ with doctest | Write `CHECK` and `REQUIRE` tests for a pricing function | code-cell (C++ tests) | code |
| 8 | Warnings and sanitizers: `-Wall -Wextra`, AddressSanitizer, UndefinedBehaviorSanitizer | Read three sanitizer reports and fix each bug | diagnostic-reader (sanitizer), code-cell (C++) | set, code |

**1.9.4 C++ for pricing** (3 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A binomial pricer in C++: one vector, backward induction | Trace the vector as each layer overwrites the last | binomial-tree (calc-linalg, P1), code-tracer (C++), code-cell (C++) | code |
| 2 | Floating-point accumulation order; `-ffast-math` | Sum the same terms in two orders and compare results | float-inspector (summation) | choice |
| 3 | **Exit**: rewrite the 1.7 pricer in C++ with tests and time it against Python | Build with tests; paste local timings; compute the speed-up with its spread | code-cell (C++), bench-lab (rigorous), setup-checklist (project) | code, numeric, state |

### 1.5 Contests (2.4, 140 h; Codeforces, Project Euler)

**2.4.1 Contest craft** (14 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | How contests run: divisions, scoring, penalties, verdicts, hacks, virtual contests, upsolving | Take a guided tour of a finished contest | contest-arena (tour) | choice |
| 2 | Reading a statement: constraints to complexity; edge cases from constraints; input formats | Pick the feasible complexity for five constraint sets | complexity-lab (budget), problem-workbench (contest) | choice |
| 3 | Fast input and Python pitfalls: `sys.stdin`, recursion limits, PyPy against CPython | Make a slow reader pass the time limit | code-cell (stdin tests), bench-lab | code |
| 4 | Implementation and simulation problems | Solve two Div. 3 A and B problems | problem-workbench (contest) | code |
| 5 | Constructive problems with a checker | Output any valid arrangement | code-cell (checker tests) | code |
| 6 | Number theory: divisibility, gcd, sieve, modular arithmetic, fast power, modular inverse, $\binom{n}{k} \bmod p$ | Cross out multiples on a sieve; cut squares from a rectangle to run Euclid's algorithm | number-theory-lab, bit-lab (fast power) | numeric, code |
| 7 | Range queries: prefix sums, difference arrays, Fenwick trees, segment trees | Tap the nodes a segment-tree query visits | range-query-lab (Fenwick, segment) | set, code |
| 8 | Binary search on the answer and two pointers under contest constraints | Solve a Div. 2 C | problem-workbench (contest) | code |
| 9 | Graphs at contest scale: iterative DFS, BFS and union-find on $2 \times 10^5$ nodes | Convert a recursive DFS that overflows the stack | graph-search, code-cell | code |
| 10 | Bitmask enumeration and bitmask DP | Enumerate subsets of 4 items as masks | bit-lab (subsets), dp-table | numeric |
| 11 | Stress testing and hacking | Break a submission with a crafted input, including a slow one | counterexample-lab (stress, hack) | text (input) |
| 12 | Virtual contest under time | Sit a two-hour set against a ghost scoreboard | contest-arena | code |
| 13 | Project Euler: maths with code | Solve with a numeric answer only | code-cell (answer) | numeric |
| 14 | Kaggle and trading competitions | Pointers to the ML cluster (Kaggle) and the finance cluster (IMC Prosperity style market games) | cross-cluster | none |

**Coverage check.** Every NeetCode 150 category maps to at least one lesson: arrays and hashing (1.8.2 L2, L3), two pointers (L5, L6), sliding window (L7 to L9), stack (1.8.3 L1, L2), binary search (1.8.2 L10 to L12), linked list (1.8.3 L4 to L8), trees (1.8.4 L1 to L6), tries (1.8.4 L7), heap (1.8.3 L9 to L11), backtracking (1.8.5 L2, L3), graphs (1.8.4 L8 to L12), advanced graphs (1.8.4 L13 to L15), 1-D DP (1.8.5 L4, L5, L9, L10), 2-D DP (1.8.5 L6 to L8), greedy (1.8.5 L11, L12), intervals (1.8.2 L15), maths and geometry (1.8.5 L13, L14), bit manipulation (1.8.5 L13).

---

## 2. Cluster contract

This catalogue follows the shared widget contract in `widgets-stage0.md` section 1 and `widgets-calc-linalg.md` section 2 (lifecycle, `describe`, ids, `highlight`, `annotate`, grading recolours answer objects only, show-why recipes, reduced motion, generators). Where those two differ, the engine blueprint decides and these specs adapt. This section states only what the programming cluster adds.

### 2.1 Names and reuse

Stage 0's reconciliation (its section 15.1) recommends the calculus and linear algebra names for shared primitives. This catalogue uses them.

| Used here | Also known as | Owner | Notes |
|---|---|---|---|
| `plot-2d`, `marks`, `drag-point`, `slider`, `stepper`, `region-select`, `token-tray`, `value-table`, `live-formula`, `sim-runner` | `plot-axes`, the three layers, `draggable-point`, `region-selector`, `data-table`, `tex-terms` (Stage 0) | engine (union of catalogues) | `stepper` gains a trace mode and `value-table` a frame mode here (section 3) |
| `choice`, `numeric-input`, `expression-input`, `free-response`, `derivation-steps` | `choice-cards`, `numeric-entry`, `expression-entry`, `derivation` (Stage 0) | engine | used unchanged |
| `number-line`, `speed-timer`, `keypad` | | Stage 0 | used unchanged |
| `code-surface`, `text-terminal` | | Stage 0 | extended here (section 3.5, 3.6) |
| `code-cell` | `code-editor` (Stage 0) | **this catalogue** | one widget; Stage 0 lessons configure it with one Python file |
| `file-tree`, `shell-sim`, `workspace-sim`, `setup-checklist`, `typing-trainer` | | Stage 0 | `shell-sim`, `workspace-sim` and `setup-checklist` gain 1.2 and project modes here (section 6) |
| `venn-diagram`, `stat-chart`, `modular-clock`, `factor-tree`, `place-value-chart` | | Stage 0 | reused for sets, histograms and number theory |
| `matrix-multiply`, `binomial-tree`, `path-simulator`, `matrix` | | calc-linalg | reused in 1.1.2 and 1.9.4; `matrix` should be built on `cell-grid` (section 3.3) |

### 2.2 Answers and checks

The shared `Answer` and `Check` unions stand. This cluster adds one answer type, one check kind, and the full `code` check.

```ts
// Answer additions
type Answer =
  | /* shared types */ ...
  | { type: 'table'; columns: string[]; rows: (string | number | null)[][] };   // a predicted SQL or pandas result

// Check additions
type Check =
  | /* shared kinds */ ...
  | { kind: 'resultset'; expect: { columns: string[]; rows: (string | number | null)[][] };
      ordered: boolean; floatTol?: number; ignoreColumnNames?: boolean }
  | { kind: 'text'; expect: string | string[];                         // predict-output; a list means any of
      compare: 'exact' | 'normalised-ws' | 'lines-unordered' | 'regex' }
  | { kind: 'code'; suite: CodeSuite };

interface CodeSuite {
  language: 'python' | 'sql' | 'cpp' | 'shell';
  tests: CodeTest[];
  timeLimitMs: number;                      // per run; default 5,000 (pytest 10,000; complexity 15,000)
  needs?: string[];                         // packages: 'numpy', 'pandas', 'matplotlib', 'pytest', 'hypothesis'
  runtimes?: ('pyodide' | 'micropython' | 'sqlite' | 'clang-wasm' | 'proxy' | 'local')[];   // set by CI tagging
}

type CodeTest =
  | { kind: 'call'; name: string; call: string; expect: string; compare: Compare; hidden?: boolean }
      // call and expect are Python (or C++) source evaluated after the suite prelude
  | { kind: 'stdout'; name: string; stdin?: string; argv?: string[]; files?: Record<string, string>;
      expect: string; compare: 'exact' | 'normalised-ws' | 'regex'; hidden?: boolean }
  | { kind: 'pytest'; name: string; file: string }                      // an authored test file run against learner code
  | { kind: 'learner-tests'; reference: string; mutants: Mutant[] }     // mutant-hunter: learner tests must pass the reference and kill every mutant
  | { kind: 'resultset'; name: string; expect: { columns: string[]; rows: unknown[][] } | { referenceQuery: string };
      ordered: boolean; floatTol?: number }
  | { kind: 'complexity'; name: string; gen: string; sizes: [number, number];
      maxTimeRatio: number; lineBudgetFactor?: number }                 // section 2.2.1
  | { kind: 'figure'; name: string; asserts: FigureAssert[] }           // matplotlib introspection
  | { kind: 'checker'; name: string; input: string; checker: string }   // constructive problems: authored Python judge
  | { kind: 'cpp'; name: string; testFile: string; framework: 'doctest' }
  | { kind: 'state'; name: string; predicate: string; args?: unknown }  // file system, Git or database state

type Compare = 'exact' | 'isclose' | 'allclose' | 'allclose-up-to-sign' | 'fraction'
             | 'frame-equal' | 'series-equal' | 'set-equal' | 'multiset-equal' | 'subspace';

type FigureAssert =
  | { axes: number; has: 'xlabel' | 'ylabel' | 'title' | 'legend' }
  | { axes: number; lines: { count?: number; ydataFrom?: string; label?: string } }
  | { axes: number; yscale?: 'linear' | 'log'; sharex?: boolean }
  | { figure: { naxes: number } };

interface Mutant { id: string; source: string; kind: string; distinguishingInput: string }   // built by mutant-forge (section 2.4)
```

**2.2.1 Efficiency tests.** A `complexity` test generates inputs at two sizes $n_1 < n_2$ from the seeded generator `gen`, then:

1. **Line budget.** It runs the learner's function under a `sys.settrace` line counter at $n_1$. It fails if the count exceeds `lineBudgetFactor` (default 4) times the reference solution's count at the same input. The tracer raises inside itself when the cap is reached, so a quadratic solution stops early instead of timing out.
2. **Time ratio.** It times the learner's and the reference solution at $n_2$, best of three, on the same device in the same run, and fails if the ratio exceeds `maxTimeRatio`. This catches work hidden inside C built-ins, which emits no line events.
3. **Message.** A failure reports the estimated exponent, $\log(t(n_2)/t(n_1)) / \log(n_2/n_1)$, in words: "Your solution grows like $n^{2.0}$; the target is $n \log n$."

Sizes are chosen per problem so the reference finishes within 300 ms at $n_2$ on the reference device [our choice]. Timer noise in Pyodide is [unverified]; the W-A1 spike measures the spread of the ratio over 50 runs and sets the default `maxTimeRatio` at the 99th percentile for a correct solution, plus a margin.

**2.2.2 Predicates this cluster registers.** Named, pure, unit-tested; content can name them and pass arguments, never supply code.

| Predicate | Used by |
|---|---|
| `graphMatches(target, { ignoreHashes })`, `headAt(ref)`, `fileContent(path, text)`, `branchContains(branch, commit)`, `remoteHas(ref, commit)`, `noConflictMarkers()` | `git-graph`, `merge-conflict` |
| `fsMatches(spec)`, `ranFrom(cwd, cmd)`, `outputContains(text)`, `modeEquals(path, octal)`, `resolves(name, dir)` | `shell-sim`, `workspace-sim`, `permission-bits`, `search-path` |
| `visitOrderValid({ algorithm, graph, start, tie })`, `topoOrderValid`, `mstValid`, `distancesEqual`, `validColouring` | `graph-search`, `shortest-path`, `union-find` |
| `isHeap`, `isBst`, `treeEquals`, `listShape(expected)`, `noLostNodes()` | `heap-lab`, `tree-lab`, `linked-list-lab` |
| `moveMatchesAlgorithm(algorithm)` | every "be the algorithm" mode |
| `outputsDiffer(input)`, `violates(property, input)`, `inputWithinConstraints(input)` | `counterexample-lab` |
| `inputEscapesLiteral(input)` | `injection-lab` |
| `matchesSets(pattern, { positives, negatives, groups })` | `regex-lab` |
| `pathSelects(path, nodeIds)` | `json-explorer` |
| `formatProduces(spec, cases)` | `format-lab` |
| `selectionEquals(expr, cells)` | `ndarray-lab`, `dataframe-lab` |
| `minimalPadding(struct)`, `ownershipState(spec)` | `memory-layout`, `ownership-lab` |
| `tableMatches(expected, { cells })`, `pathCells(cells)` | `dp-table` |
| `figureFixed(spec)` | `plot-workbench` |

### 2.3 Trace formats

**Code traces** drive `code-tracer`, `predict-output` show-why, `complexity-lab` line counts and the `stepper` trace mode.

```ts
interface Trace {
  language: 'python' | 'cpp' | 'pseudo';
  source: string;                         // exactly the code shown
  steps: TraceStep[];                     // at most 10,000; the recorder stops there and sets truncated
  truncated?: boolean;
  result: { stdout: string; error?: { type: string; message: string; line: number } };
  recorder: { name: 'py-settrace' | 'cpp-authored'; version: string; python?: string };   // e.g. python '3.12.7'
}

interface TraceStep {
  line: number;                           // the line about to run (the next line)
  event: 'line' | 'call' | 'return' | 'exception' | 'raise';
  stack: Frame[];                         // outermost first
  heap?: Record<ObjId, HeapObj>;          // full on keyframes (every 50th step), otherwise only changed objects
  freed?: ObjId[];                        // objects no longer reachable, or destroyed (C++)
  stdout?: string;                        // text appended at this step
  hits?: Record<number, number>;          // cumulative line-hit counts, on keyframes
  note?: string;                          // authored caption, at most 20 words
}

interface Frame { id: string; fn: string; line: number; locals: [string, Value][]; enclosing?: string; returning?: Value }
type Value = { prim: string; type: 'int' | 'float' | 'str' | 'bool' | 'None' | 'char' | 'double' | 'uninit' } | { ref: ObjId };
type ObjId = string;                      // 'o1', 'o2', ... in first-seen order, so ids are stable across runs

type HeapObj =
  | { kind: 'list' | 'tuple' | 'set' | 'frozenset'; items: Value[] }
  | { kind: 'dict'; entries: [Value, Value][] }
  | { kind: 'instance'; cls: string; attrs: [string, Value][] }
  | { kind: 'class'; name: string; bases: string[]; attrs: [string, Value][] }
  | { kind: 'function'; name: string; params: string[]; closure?: [string, Value][] }
  | { kind: 'generator'; fn: string; frame?: Frame; state: 'created' | 'suspended' | 'running' | 'closed' }
  | { kind: 'ndarray'; dtype: string; shape: number[]; preview: string }
  | { kind: 'cpp-block'; type: string; bytes: number; address: string; cells: Value[]; state: 'live' | 'freed' }
  | { kind: 'cpp-object'; type: string; address: string; fields: [string, Value][]; vptr?: string }
  | { kind: 'other'; repr: string };
```

- **Python recorder** [our choice]: a pure-Python module using `sys.settrace` that records frames, reachable objects and stdout. It renders small integers, floats, strings, booleans and `None` inline by default; a lesson can ask for "objects for everything" when teaching `is` against `==`. Objects are numbered in first-seen order, not by `id()`, so two runs give identical traces.
- **Pinning.** The build-time recorder runs on the same CPython minor version that the pinned Pyodide uses, so authored traces equal live traces.
- **C++ traces** are authored keyframes (`recorder: 'cpp-authored'`), because no in-browser C++ tracer exists in our stack. CI compiles every C++ snippet with Clang and GCC at `-std=c++20`, runs it, and requires its stdout to equal the trace's `result.stdout`. Snippets that demonstrate undefined behaviour also run under AddressSanitizer and UndefinedBehaviorSanitizer, and CI requires the expected report. Addresses are synthetic and deterministic: stack from `0x7ffc0000` downwards, heap from `0x55550000` upwards, aligned as the x86-64 System V ABI requires.

**Algorithm traces** drive the 1.8 composites.

```ts
interface AlgoTrace<S> {
  algorithm: string;                       // 'insertion-sort', 'bfs', 'dijkstra', ...
  input: unknown;
  source: { python: string; cpp?: string };   // the code the learner sees
  steps: { state: S; event: AlgoEvent; line: { python: number; cpp?: number }; note?: string }[];
  counters: Record<'compares' | 'swaps' | 'reads' | 'writes' | 'pushes' | 'pops' | 'calls', number[]>;   // cumulative per step
}
type AlgoEvent = { kind: 'compare' | 'swap' | 'write' | 'read' | 'push' | 'pop' | 'enqueue' | 'dequeue'
                       | 'visit' | 'discover' | 'finish' | 'relax' | 'settle' | 'union' | 'find'
                       | 'call' | 'return' | 'prune' | 'fill' | 'mark' | 'done';
                   ids: string[]; detail?: string };
```

- Every algorithm in `algo-trace` is a JavaScript generator that yields `AlgoEvent`s. It ships with the Python source it mirrors and a map from events to Python lines.
- **CI parity test** for each algorithm, over 1,000 seeded inputs: run the Python source under the recorder and the JavaScript generator on the same input. Both must give the same output, and the sequence of (event kind, Python line) at the instrumented lines must match.

### 2.4 Runtimes and services

| Service | Responsibility | Where it runs |
|---|---|---|
| `python-runner` (Stage 0, extended) | Worker-hosted Python. Adds: packages per suite (`needs`), notebook kernels with execution counts, pytest mode, matplotlib capture (Agg PNG plus SVG with artist ids), `complexity` probes, live tracing through the recorder, `argv`, files synced from `vfs`. Limits: 5 s per run by default, terminate and restart on timeout, 4,000 characters of output per stream | Web: Pyodide. Artifact: MicroPython with ulab if WebAssembly is allowed [unverified] |
| `trace-recorder` | The Python recorder in section 2.3 | CI (CPython pinned to Pyodide's minor version); Pyodide at runtime |
| `sql-runner` | SQLite in a worker: load a seeded database, run a query, return columns and rows (at most 1,000 rows shown), `EXPLAIN QUERY PLAN` | Both targets, from the official SQLite WebAssembly build served as the app's own `.wasm` file; replay and seed banks without WebAssembly |
| `cpp-runner` | Compile and run C++20 with doctest; flags; sanitizers where supported | Web: in-browser Clang (spike) or the proxy to Compiler Explorer; local paste verification on both targets |
| `shell-interpreter` (Stage 0 `shell-sim` engine, extended) | Bash subset over `vfs` (section 6.10) | Both, pure JavaScript |
| `git-model` | Git's object model and commands (section 6.1) | Both, pure JavaScript |
| `vfs` (Stage 0) | Virtual file system | Both |
| `nd-core` | NumPy semantics for shapes, strides, slicing, broadcasting, masks, reductions and small-array values, with `int64` through `BigInt64Array` and `float64` | Both, pure JavaScript; CI-checked against NumPy |
| `frame-core` | pandas semantics for the operations the widgets show: Index, Series, DataFrame, `loc`, `iloc`, masks, aligned arithmetic, `groupby` with `agg` and `transform`, `merge`, `concat`, `pivot`, `melt`, `stack`, `shift`, `pct_change`, `rolling`, `resample` (calendar frequencies), `ffill`, `dropna` | Both, pure JavaScript; CI-checked against pandas |
| `algo-trace` | Instrumented algorithm generators (section 2.3) | Both |
| `code-lex` | Incremental per-line tokenisers for Python, C++, SQL, shell, diff, regex, JSON and CSV; token ids for addressable code | Both |
| `mutant-forge` | Build-time mutation: operator swaps, boundary shifts, removed statements, changed constants, swapped arguments, loosened tolerances. Keeps a mutant only if a seeded fuzzer finds a distinguishing input, so no mutant is equivalent to the reference | CI |
| `seed-bank` | For generators whose items need a runtime the Artifact may lack (SQL, Python output prediction), CI precomputes 200 seeds per family and difficulty | CI; consumed on both |
| `price-series` | Seeded synthetic daily prices on a trading calendar: log-normal steps with GARCH(1,1)-style volatility clustering and rare jumps; CSV output with optional messiness (missing days, thousands separators, a bad row) | Both; shared with the finance cluster |
| `handoff` | Opens the same item in the web app with the learner's state compressed into the URL fragment (at most 8 KB; the fragment never reaches a server) | Artifact |

### 2.5 Visual rules for code and algorithms

These add to the shared visual rules (manipulable blue for learner-moved objects, series slots for given and derived data, grading recolours answer objects only, pear wash for tutor highlights).

**Code.** Source Code Pro in the code token on `--bg-sunken`, `--r-md` corners. Token colours follow Stage 0's `code-surface`: keywords `--code-keyword`, built-ins and C++ types `--code-deep`, strings `--fin-deep`, numbers `--prob-deep`, comments `--text-muted`, preprocessor lines `--text-secondary`. SQL keywords render upper case in `--code-keyword`.

**Execution markers.**

| Marker | Style | Meaning |
|---|---|---|
| Next line | Outlined ink arrow in the gutter, `--bg-hover` band across the line | about to run |
| Line just run | Solid ink arrow in the gutter | ran in the last step |
| Breakpoint | 10px `--manip` disc in the gutter (the learner sets it) | execution stops here |
| Changed value | 2px `--s2` underline and weight 600 for one step | this step changed it |
| Error line | `--fail-cross` wavy underline plus a cross icon and "error" in text | the line that raised |
| Line-hit count | Number in the gutter in caption type; a 4px bar whose length scales with the count, `--s6` | how often the line ran |

**Algorithm states.** Colour never carries a state alone; each has a pattern or glyph. Slot s1 is never used in a view with handles, because it sits too close to `--manip` (calc-linalg rule).

| State | Fill and stroke | Second cue | Examples |
|---|---|---|---|
| Default | `--bg-surface`, 1px `--line` | none | untouched cells |
| Active | 2px `--s2` stroke, `--s2` at 12% | caret above the cell | the pair being compared, the node being expanded |
| Frontier | 2px dashed `--s4` stroke | dashed border | in the queue, on the stack, inside the window |
| Done | `--s6` at 16% | 45° hatch | sorted region, visited, settled, filled DP cell |
| Ruled out | opacity 0.25 (`--out`) | strike-through on the value | eliminated pairs, pruned branches, discarded half |
| Special | 2px `--s5` ring | text label ("pivot", "root", "source") | pivot, root, source |
| Learner pointer | `--manip` caret marker with its name | the name, always shown | `i`, `j`, `lo`, `hi`, `slow`, `fast` |

**Pointers and references.** Arrows are 1.5px ink with 6px heads. A learner-drawn arrow is 2px `--manip` until graded. A dangling pointer is a dashed `--text-muted` arrow ending in a cross glyph and the word "dangling". Freed blocks are hatched with the label "freed".

**Diffs** [our choice, needs design sign-off]. Added lines take an `--s3` wash at 12% with a "+" glyph; removed lines an `--s2` wash at 12% with a "−" glyph. Diff lines are never answer objects, so they never take grading colours, and the glyphs carry the meaning for colour-blind readers.

### 2.6 Motion

- Direct manipulation is never tweened: dragged pointers, slice handles, arrows being drawn and window brackets follow the pointer every frame.
- Springs on release only: a pointer marker snaps to the nearest index with `spring-snap`; a dropped token or code line snaps into its slot.
- **Step animations are consequences.** When the learner presses Step, the change animates over 200 to 300 ms with `ease-standard`: two bars swap, a node moves from queue to visited, an arrow re-points. They only follow a learner action or Play.
- **Play** runs at 0.5 to 8 steps per second, set by a speed control; at speeds above 4 per second, steps cut without interpolation.
- **Show-why** for code uses three shared recipes: `divergence` (the tracer jumps to the first step whose output differs from the learner's prediction and highlights the variables that caused it), `alias` (both names pulse while the shared object changes), and `trace-failure` (the failing test's input runs through the learner's code in the tracer, web only).
- **Reduced motion.** Step changes cut; Play steps without interpolation; show-why becomes a before-and-after pair with a Play button; pulses become a static ring. Autoplay never starts by itself.

### 2.7 Accessibility

- **Code is text.** Editors are real textareas; read-only code is real text in `<pre>` with line ids, so screen readers read it and browsers find it.
- **Every structure has a table or list view.** Arrays and grids open as `value-table`; heaps as a list of names and the objects they refer to ("a → list o1 [1, 2]; b → list o1"); graphs as adjacency lists; trees as nested lists; diffs as lines prefixed "added" and "removed".
- **Steps are announced** on commit in one sentence: "Step 14 of 52. Line 6. total is 21." Never per frame during Play; during Play, one summary every 2 seconds.
- **Keyboard.** Widget-level keys are letters, never F-keys, which browsers reserve: N step over, S step into, O step out, B toggle a breakpoint, C continue, Left and Right step back and forward, Home and End jump to the ends of a trace. Inside the editor, these keys type; Escape then Tab leaves the editor, as in Stage 0.
- **Arrows without a mouse.** To draw a pointer, focus the source slot, press Enter, move through candidate targets with the arrow keys (each announced), and press Enter again. The two-tap path does the same on touch.
- **Colour.** Every state has a pattern or glyph (2.5). Diff lines have "+" and "−".

### 2.8 Tutor hooks for code widgets

Bertie (Brainy Bertie, the tutor's face) is the same on both targets; only the transport differs. The engine blueprint chooses between page tools (Stage 0's proposal) and a single JSON reply with ids (calc-linalg's proposal). Widgets here supply the same hooks to either.

- **`describe('brief')`** at most 300 characters; **`describe('full')`** at most 2 KB, excluding code.
- **`code()`** returns the code under discussion, numbered, at most 8 KB (about 200 lines), plus the last run: status, the first failing test's input, expected and actual values, and the error with its line.
- **Ids** follow `kind:name`: `line:12`, `tok:12:5`, `test:3`, `frame:main#1`, `var:main.total`, `obj:o4`, `cell:3`, `cell:2,5`, `node:7`, `edge:3-5`, `commit:a1b2c3d`, `ptr:lo`.
- **Suggestions are navigation only.** `suggest` may offer "Step to line 9", "Set a breakpoint on line 14", "Open test 3", "Trace this test", "Run the brute force". It never offers code edits.
- **Code guard.** Before the item passes, the engine strips any fenced code block longer than 2 lines from Bertie's reply and replaces it with "Bertie keeps the code for you to write." Bertie receives the learner's code and results, never the reference solution or hidden-test sources; it receives the names of hidden tests and their pass or fail status.
- **After a pass**, `code-cell` offers "Review my code". Bertie reviews in the owner's code-craft format at the depth the learner picks (1 to 5): complexity notes, inline rationale for non-obvious lines, a senior-developer paragraph from depth 2, and a plain-English translation whose granularity rises with depth.
- **"Explain this error"** sends the structured report from `diagnostic-reader` (error type, message, the frame in the learner's code, the code around it), not the raw text alone.
- **Unavailable** in quiz, homework and exam modes, as everywhere.

### 2.9 Performance

Budgets are the shared ones (reference device: a 2021 to 2022 mid-range Android phone; the engine blueprint fixes one model). Per pointer frame, P95: widget script 4 ms or less, style, layout and paint 6 ms or less. Cluster-specific limits:

| Item | Budget or cap |
|---|---|
| Trace length | 10,000 steps; heap keyframes every 50 steps; step render 4 ms or less |
| Heap diagram | 80 objects drawn; beyond that, containers collapse to summaries ("list of 1,000 ints") |
| `array-strip` | SVG up to 200 cells; Canvas 2D bars above, up to 5,000; 1,000 bars redraw in 2 ms or less |
| `cell-grid` | SVG up to 2,500 cells; Canvas 2D above, up to 250,000 |
| `node-link` | SVG up to 300 nodes; Canvas 2D above with an SVG layer for focused and hovered nodes; tidy-tree layout of 500 nodes in 1 ms or less |
| `value-table` frame mode | Virtualised: about 40 rows rendered; 100,000 rows scroll at 60 frames per second |
| Highlighting | Incremental by line: 2 ms or less per keystroke at 300 lines |
| Python start (web) | Pyodide preloads on the lesson title screen; the tangram loader shows after 400 ms; NumPy, pandas and matplotlib load only for suites that need them [cold-start times unverified, measured in W-A1] |
| Saved state | At most 32 KB per widget instance; code drafts at most 64 KB per item; traces are never saved, only re-derived |

### 2.10 Artifact and web

| Capability | Web app | Artifact, WebAssembly allowed | Artifact, WebAssembly blocked |
|---|---|---|---|
| Replayed traces, algorithm animations, Git, shell, `nd-core` and `frame-core` widgets | yes | yes | yes |
| Pure-Python drills | Pyodide | MicroPython, for drills CI tags compatible | handoff |
| NumPy drills | Pyodide | ulab, for tagged drills | handoff |
| pandas, matplotlib, pytest, Hypothesis drills | Pyodide | handoff; simple pytest drills run on MicroPython through a mini-pytest shim (plain `assert`, `raises`, `approx`, `parametrize`) | handoff |
| Live tracing of the learner's code | Pyodide recorder | MicroPython if built with `sys.settrace` [unverified]; otherwise handoff | handoff |
| SQL queries | SQLite WebAssembly | SQLite WebAssembly from the Artifact's own files | replay of authored queries; seed banks; free queries hand off |
| C++ drills | in-browser Clang or the proxy | handoff and local paste | handoff and local paste |
| Timing races | live | live where MicroPython can run both sides; otherwise recorded timings labelled with the device they were measured on | recorded timings |
| Tutor | proxy | `sample` capability | `sample` capability |
| Exporting a file (CSV, script) | Blob link | `downloads` capability, one file at a time | same |

- **CI tagging.** Every drill's reference solution runs on each runtime in CI. A drill whose output differs on MicroPython is tagged web-only. MicroPython lacks parts of the standard library that 1.1 uses (for example `csv`, `fractions`, `dataclasses`, `collections.Counter`) [unverified per module; CI decides].
- **Handoff.** An anchor to the web app with the item id and state in the fragment. Whether the Artifact host lets an anchor open an external page is [unverified]; the fallback shows the link as copyable text with a Copy button (Stage 0's rule).

### 2.11 Phones

- **Parsons alternative** (decision 15): below 768px, a `code-cell` drill offers "Build it from lines" beside "Type it". The Parsons version comes from the reference solution split at statement boundaries, with 1 to 3 distractor lines taken from `mutant-forge` mutants. An author can disable it for drills where line order is trivial.
- **Dense widgets** (frames, grids, diffs) scroll horizontally inside their own frame, never the page, with a sticky index column and header.
- **Symbol bar.** Every code input has Stage 0's symbol bar; C++ adds `<`, `>`, `;`, `{`, `}`, `&`, `*` and `::`; SQL adds `'`, `,`, `*` and `=`.

### 2.12 Learner code and safety

- Learner code runs only in a worker, never on the page: no DOM, no storage, no network beyond what the runtime itself loads. The page terminates the worker on timeout.
- **Honest limit.** Hidden tests ship to the device, so a determined learner can read them. Obfuscation is not worth its cost in a self-study app, and we say so in the drill help.
- Code sent to Bertie is the learner's own, sent on the learner's own account (Artifact) or through the owner's proxy (web). Pastes in `setup-checklist` are redacted for home paths before they go to the tutor (Stage 0's rule).

---

## 3. Primitives

Four new primitives, then four extensions to primitives that other catalogues specify. Build waves are named in section 12: W-A1 to W-A3 are P0 (1.1 core, 1.1 data, 1.2 tools), W-B1, W-B2 and W-C are P1 (1.8 and 1.9), W-D is P2 (2.4).

`array-strip` and `cell-grid` share one cell renderer and one overlay model (states, markers, ranges, arrows). They stay separate primitives because one-dimensional work needs things a grid does not: markers that sit between cells for half-open ranges, bar heights for sorting, and ring layouts for circular buffers.

### 3.1 `diff-view`: Diff view

**Primitive · P0 · W-A1.** Shows how one text differs from another: expected against actual output, a commit's changes, a pull request, a mutant against the reference, a failing version beside its fix (design research 9.4), and three-way merges.

- **Serves:** 1.1 (test failures, before-and-after refactors), 1.2.2 (Git diffs, `add -p`, pull requests, conflicts), 1.2.4 (mutants), 1.8 and 1.9 (bug fixes), 2.4 (expected against actual verdicts).
- **Uses:** `code-surface` (read-only, per side), the `code-lex` service, a Myers diff with a patience-diff pre-pass for code [our choice: patience anchors on unique lines and gives readable code diffs].
- **Interactions.**
  - Pointer: toggle unified or split (split only at 768px and wider); expand collapsed unchanged regions; tap a hunk to select it (staging, accepting, rejecting); tap a line's gutter to add a comment marker (review mode).
  - Keyboard: J and K move between hunks; Space selects a hunk; Enter on a line opens a comment; U toggles unified or split; E expands context.
- **State:** `{ view: 'unified' | 'split', expanded: string[], selectedHunks: string[], comments: { line: string; side: 'a' | 'b'; text: string; tag?: string }[] }`.
- **Answers:** `set` (selected hunks or flagged lines), `state` (comments with tags, graded by `code-review`).
- **Config:**
```ts
interface DiffViewConfig {
  a: string; b: string; base?: string;            // base enables three-way mode
  language: 'python' | 'cpp' | 'sql' | 'shell' | 'text' | 'csv';
  labels?: { a: string; b: string; base?: string };   // 'expected', 'actual'; 'ours', 'theirs'
  view?: 'unified' | 'split' | 'auto';
  context?: number;                                // unchanged lines kept around hunks, default 3
  intraline?: boolean;                             // character-level highlights inside changed lines
  hunkSelect?: boolean; comments?: boolean | { tags: string[] };
  whitespace?: 'show' | 'ignore-trailing';
}
```
- **Visual:** code token type; gutter with old and new line numbers; added lines `--s3` at 12% with "+", removed `--s2` at 12% with "−" (section 2.5); intra-line changes as a 2px underline in the same slot colour; hunk headers in caption type on `--bg-sunken`; a selected hunk has a 2px `--manip` left bar; comment markers are 20px `--manip` speech glyphs until graded.
- **Motion:** expanding context slides open over 150 ms; nothing else moves.
- **Reduced motion:** instant expansion.
- **Accessibility:** each line is prefixed in its accessible name ("added line 14: return total"); hunks are a list with a count ("Hunk 2 of 4, 3 lines removed, 5 added"); the split view keeps a reading order of old then new per hunk.
- **Tutor:** describe: "Diff expected against actual: 1 hunk, line 3 differs: expected '0.1542', actual '0.1541'." Ids: `hunk:<n>`, `line:a<n>`, `line:b<n>`.
- **Performance:** diff computed once on mount, in a worker above 2,000 lines; SVG-free DOM rows; at most 3,000 lines rendered with collapsed context.
- **Artifact / web:** identical.
- **Generator:** no.

### 3.2 `array-strip`: Array strip

**Primitive · P0 · W-A1.** A one-dimensional indexed sequence with pointer markers, ranges and per-cell states: lists, strings, bit patterns, bytes in memory, sorting bars, windows, prefix arrays, heap arrays and ring buffers.

- **Serves:** 1.1 (string and list slicing, `range`), 1.1.2 (1D arrays, the memory buffer under `ndarray-lab`), 1.8 (every array pattern, sorting, binary search, heaps, hashing buckets, prefix sums, dynamic arrays, bits), 1.9 (C arrays, bytes, vectors), 2.4.
- **Uses:** `drag-point` (marker handles on an x-only constraint), `token-tray` (cell swaps and reordering in by-hand modes).
- **Interactions.**
  - Pointer: drag a marker along the strip; it snaps to a cell or, for boundary markers, to a gap between cells (positions $0$ to $n$, so `hi = n` is reachable). Tap a cell to select or cycle its state. Drag a cell onto another to swap (by-hand sorting). Drag range handles to set `start:stop:step`. Double-tap a cell to edit its value.
  - Keyboard: Tab moves between markers and the strip; on a marker, Left and Right move one position, Home and End jump to the ends; on the strip, Left and Right move the cell cursor, Space selects, Enter edits, and X then a second cell swaps the two. The two-tap path swaps on touch.
- **State:** `{ values: (number | string)[], markers: Record<string, number>, ranges: Record<string, { start: number; stop: number; step: number }>, states: Record<number, CellState>, selected: number[] }`.
- **Answers:** `point` (marker positions), `set` (selected cells), `ordering` (values after by-hand moves), `text` (the slice expression the handles produce), `state`.
- **Config:**
```ts
interface ArrayStripConfig {
  values: (number | string)[];
  mode: 'cells' | 'chars' | 'bars' | 'bits' | 'bytes' | 'ring';
  orientation?: 'horizontal' | 'vertical';           // vertical for hash buckets and stacks
  indices?: 'positive' | 'negative' | 'both' | 'none' | { base: 'address'; start: number; stride: number };
  markers?: { id: string; label: string; at: number; kind: 'cell' | 'gap'; movable?: boolean;
              side?: 'above' | 'below'; constraint?: { min?: number; max?: number; leftOf?: string } }[];
  ranges?: { id: string; start: number; stop: number; step?: number; movable?: boolean; style: 'slice' | 'window' | 'region' }[];
  states?: Record<number, CellState>;
  editable?: boolean | number[]; swappable?: boolean;
  bits?: { width: 8 | 16 | 32 | 64; signed?: boolean; showPlaceValues?: boolean };
  link?: { to: string; map: 'heap-tree' | 'prefix' | 'same-index' };   // pairs with another widget's ids
  maxVisible?: number;                                // longer strips scroll inside the widget
}
type CellState = 'default' | 'active' | 'frontier' | 'done' | 'out' | 'special';
```
- **Visual:** cells 44px square (36px on phones, with 44px hit areas) in caption-to-body type with tabular figures; indices in caption type under the cells, negative indices above when `both`; markers are `--manip` carets with their names; a slice range is a `--manip-wash` band across the selected cells with a dot on each stepped cell; windows are a 2px dashed `--s4` bracket; bars mode draws bar heights in `--text-secondary` with states from section 2.5; bits mode shows place values ($2^7 \ldots 2^0$) above and a sign bit marked for signed widths; ring mode bends the strip into a circle with head and tail markers.
- **Motion:** marker drags are direct, with `spring-snap` on release. Swaps animate as a consequence (the two cells exchange along short arcs over 240 ms). Inserting at the front slides every later cell one place over 300 ms, which is the visual cost of $O(n)$.
- **Reduced motion:** swaps and shifts cut to the final state; the moved cells keep the "active" state for one step so the change stays visible.
- **Accessibility:** the strip is a `grid` with one row; cells read "index 3, value 17, active"; markers are sliders with `aria-valuetext` ("lo at index 2, before value 9"); the table view lists index, value and state.
- **Tutor:** describe: "Array [3, 8, 9, 12, 17] with lo at 1, hi at 5 (exclusive), mid at 3. Cells 0 ruled out." Ids: `cell:<i>`, `ptr:<id>`, `range:<id>`.
- **Performance:** SVG up to 200 cells; Canvas 2D bars from 200 to 5,000 cells with an SVG layer for markers; a drag updates one transform.
- **Artifact / web:** identical.
- **Generator:** no (composites generate).

### 3.3 `cell-grid`: Cell grid

**Primitive · P0 · W-A2.** A two-dimensional (and layered three-dimensional) lattice of cells where position carries meaning: NumPy arrays, DP tables, grid graphs, the sieve, the pair grid behind two pointers, prefix-sum rectangles, cache lines, and matrices for the rotate and spiral problems.

- **Serves:** 1.1.2 (2D and 3D arrays, slicing, masks, broadcasting), 1.8 (DP tables, grid BFS and DFS, islands, N-Queens, word search, matrix problems, the two-pointer pair grid, 2D prefix sums), 1.9 (row-major memory, cache lines), 2.4 (sieve).
- **Uses:** `region-select` (cell selection and painting), `drag-point` (row and column markers, rectangle handles).
- **Interactions.**
  - Pointer: tap a cell to select or cycle its state; drag across cells to paint a rectangle or a free set (as configured); drag rectangle handles for slices; drag row and column markers; tap a layer tab or the visible edge of a layer to bring it forward (3D); double-tap to edit a value.
  - Keyboard: the grid pattern with a roving tab stop. Arrows move; Shift+arrows extend a rectangle; Space selects or cycles; Enter edits; Page Up and Page Down move between layers; R and C jump to the row and column markers.
- **State:** `{ values: (number | string | null)[][][], states: Record<string, CellState>, selection: string[], rects: Record<string, [number, number, number, number]>, markers: Record<string, number>, layer: number }` (cell keys are `"r,c"` or `"l,r,c"`).
- **Answers:** `set` (cells), `state`, `point` (a cell or marker), `numeric` per cell through `multi` (DP fills), `text` (a slice expression from the rectangle handles).
- **Config:**
```ts
interface CellGridConfig {
  shape: [number, number] | [number, number, number];          // rows, columns, or layers, rows, columns
  values?: (number | string | null)[][] | (number | string | null)[][][];
  headers?: { rows?: string[]; cols?: string[]; layers?: string[]; corner?: string };
  indexLabels?: 'positive' | 'negative' | 'both' | 'none';
  states?: Record<string, CellState>;
  select?: 'none' | 'single' | 'multi' | 'rect' | 'paint';
  editable?: boolean | string[];
  markers?: { id: string; axis: 'row' | 'col'; at: number; label: string; movable?: boolean }[];
  rects?: { id: string; r0: number; c0: number; r1: number; c1: number; movable?: boolean; style: 'slice' | 'window' | 'region' }[];
  arrows?: { from: string; to: string; style?: 'dependency' | 'path' | 'move' }[];
  path?: string[];                                              // ordered cells drawn as a polyline
  heat?: { ramp: 'sequential' | 'diverging'; domain: [number, number] };
  cellSize?: number;                                            // px; default 40, 28 for dense grids
}
```
- **Visual:** cells with 1px `--line` borders on `--bg-surface`; headers in caption type, row headers right-aligned; values in tabular figures; heat fills from the sequential ramp `--seq-1` to `--seq-6` with the value always printed; dependency arrows 1.5px `--text-muted` drawn only for the focused cell (all at once becomes noise); paths 2.5px ink through cell centres; layers drawn as sheets offset 12px down and right, the front sheet opaque and the rest at 40%.
- **Motion:** paint and rectangle drags are direct. Bringing a layer forward slides it over 240 ms. Filling a cell during Play fades the value in over 150 ms.
- **Reduced motion:** layer changes and fills cut.
- **Accessibility:** a real `grid` with row and column headers; each cell reads "row 2, column 5, value 7, done"; dependency arrows are listed in the focused cell's description ("reads row 1 column 5 and row 2 column 4"); the table view is the grid itself as a `<table>`.
- **Tutor:** describe: "Grid 5 × 6 (DP table for edit distance 'kitten' to 'sitting'), 18 of 30 cells filled; focus at (3, 4) = 2." Ids: `cell:<r>,<c>`, `row:<r>`, `col:<c>`, `layer:<l>`, `rect:<id>`, `marker:<id>`.
- **Performance:** SVG up to 2,500 cells; Canvas 2D above with a DOM overlay for the focused cell; painting updates only touched cells.
- **Artifact / web:** identical.
- **Generator:** no.
- **Note for the engine:** calc-linalg's `matrix` primitive should be built on `cell-grid` with bracket styling and exact-fraction entries, so the two do not drift.

### 3.4 `node-link`: Node-link diagram

**Primitive · P0 · W-A1.** The one renderer for trees, graphs, DAGs and memory diagrams. Nodes and edges carry stable ids, states and labels; layouts are deterministic, and an object keeps its position from one step to the next.

- **Serves:** 1.1 (the heap layout behind `code-tracer`; the outline layout behind `json-explorer` and `search-path`), 1.2 (Git commit graphs, fixture graphs, pipelines), 1.8 (trees, BSTs, heaps, tries, graphs, union-find forests, recursion trees, DP dependency DAGs, linked lists), 1.9 (stack and heap diagrams, ownership, vtables, build graphs), 2.4 (segment trees). Other clusters: probability trees, Markov chains, binomial trees, neural networks.
- **Uses:** `drag-point` (node dragging in `fixed` layouts), `token-tray` (drop targets when a composite drags a token over nodes).
- **Layouts:**

| Layout | Algorithm | Used for |
|---|---|---|
| `tidy` | Reingold-Tilford in Buchheim's linear-time form; empty child slots reserved so a lone right child sits right | binary trees, recursion trees, tries, heaps-as-trees, segment trees |
| `layered` | Longest-path layering, then barycentre ordering with 4 sweeps; straight or orthogonal edges | DAGs: fixtures, build graphs, topological sort, DP subproblem DAGs |
| `git` | Commits on a time axis with one lane per branch; merges join lanes | `git-graph` |
| `fixed` | Authored or generated coordinates (generators run a force layout at build time, never at runtime) | general graphs, weighted graphs, grids of nodes |
| `circular` | Nodes on a circle in id order | small graphs, cycles, union-find before unions |
| `outline` | Indented, collapsible rows | JSON, file trees, `PATH` and `sys.path` |
| `heap` | Frames in a column on the left (outermost at the top), objects to the right in columns by reference depth; an object keeps its slot until freed | `code-tracer`, `ownership-lab` |
| `row` | A chain left to right, wrapping at the container edge | linked lists, queues of nodes |
| `forest` | Several tidy trees side by side | union-find, heaps during k-way merge |

- **Node shapes:** `circle` (graph vertex, 36px), `pill` (label), `record` (a header plus slots, each slot a port an edge can leave from: Python objects, linked-list nodes, frames, C++ objects), `cells` (a list or array object as a row of ports), `tag` (a small name label attached to a node: pointer variables such as `curr`).
- **Edges:** directed or undirected; from a node or a port; straight, curved or orthogonal; optional weight label; states; `dangling` (dashed, ending in a cross).
- **Interactions.**
  - Pointer: tap a node or edge to select it or cycle its state. Drag from a port or node to another node to draw an edge (or re-point an existing arrow when `rewire` is on). Drag a node in `fixed` layouts when allowed. Tap a weight to edit it. Expand and collapse in `outline`. Pan and pinch-zoom only when the content exceeds the frame.
  - Keyboard: Tab enters the diagram; arrows move focus spatially between nodes; Enter on a port starts an arrow, then arrows cycle candidate targets (each announced) and Enter drops; Delete removes a learner-made edge; E edits a weight; Space toggles selection; + and − expand and collapse in `outline`.
- **State:** `{ selected: string[], states: Record<string, string>, edges: { added: EdgeSpec[]; removed: string[]; rewired: Record<string, string> }, positions?: Record<string, [number, number]>, collapsed: string[] }`.
- **Answers:** `set` (nodes or edges), `ordering` (the order nodes were tapped), `mapping` (port to target, for arrows), `state`.
- **Config:**
```ts
interface NodeLinkConfig {
  nodes: { id: string; label?: string; tex?: string; shape?: 'circle' | 'pill' | 'record' | 'cells' | 'tag';
           slots?: { id: string; label?: string; value?: string }[];      // record and cells shapes
           parent?: string; order?: number; at?: [number, number]; state?: string; group?: string }[];
  edges: { id: string; from: string; to: string; fromPort?: string; directed?: boolean;
           weight?: number | string; state?: string; kind?: 'normal' | 'dangling' | 'alias' }[];
  layout: 'tidy' | 'layered' | 'git' | 'fixed' | 'circular' | 'outline' | 'heap' | 'row' | 'forest';
  layoutOptions?: { direction?: 'down' | 'right'; levelGap?: number; siblingGap?: number; sticky?: boolean };
  interact?: { select?: 'none' | 'node' | 'edge' | 'both'; drawEdges?: boolean; rewire?: boolean;
               moveNodes?: boolean; editWeights?: boolean; maxSelected?: number };
  states?: Record<string, { style: CellState; label: string }>;        // named states with text labels
}
```
- **Visual:** nodes on `--bg-surface` with 1.5px `--line-control` borders; records with a `--bg-sunken` header row; labels in caption-to-body type; edges 1.5px ink with 6px heads; weights in caption type on a `--bg-surface` chip; states from section 2.5; learner-drawn edges 2px `--manip`; tags are `--manip` when movable, ink when not.
- **Motion:** structure changes (insert, delete, rotation, rewire) reflow with FLIP over 300 ms using `ease-standard`, as a consequence of a learner action or step; a node being dragged follows the pointer directly; arrows being drawn follow the pointer directly.
- **Reduced motion:** reflows cut; the moved nodes keep the "active" state for one step.
- **Accessibility:** the diagram is a `group` with a structured text alternative (trees as nested lists, graphs as adjacency lists, heaps as name-to-object lists); each node is focusable with a name like "node 7, visited, neighbours 3, 5, 9"; arrows being drawn announce each candidate target.
- **Tutor:** describe gives node count, edge count, the selected and active nodes, and states by group: "Graph 9 nodes, 12 edges. Visited: A, B, D. Queue: E, F. Active: D." Ids: `node:<id>`, `edge:<id>`, `slot:<node>.<slot>`.
- **Performance:** SVG up to 300 nodes; above that, Canvas 2D for edges and unfocused nodes with SVG for focus and hover; layouts are computed only on structure change (tidy 500 nodes in 1 ms or less; layered 200 nodes in 5 ms or less); the `heap` layout is incremental so objects never jump between steps.
- **Artifact / web:** identical.
- **Generator:** no (composites generate graphs and trees).

### 3.5 `code-surface` (extended from Stage 0)

**Primitive · P0 · W-A1.** Stage 0's editing surface (textarea over a synchronised highlighted `<pre>`) stays.

- **Serves:** 0.4; every code-bearing screen in 1.1, 1.2, 1.8, 1.9 and 2.4, and code in other clusters' lessons.

This catalogue adds:

- **Languages:** Python, C++, SQL, shell, diff, JSON and CSV, through the shared `code-lex` tokenisers.
- **Read-only addressable mode:** every token gets an id (`tok:<line>:<col>`) and every line an id (`line:<n>`). Lines and tokens can be tapped (answers `set`), highlighted by the tutor and annotated. This mode replaces the textarea with plain text in `<pre>`, so it is cheap and screen-reader friendly.
- **Gutters:** line numbers, execution markers (next line, line just run), breakpoints, line-hit counts, coverage marks (P1) and diagnostics, as in section 2.5.
- **Inline slots:** placeholders inside a line, rendered as inline inputs or drop slots, for `code-blanks` and `format-lab`. A slot has a fixed width in characters, so filling it never reflows the line.
- **Inline callouts:** anchored notes for `code-annotator` and tutor annotations, shown beside the line on desktop and below it on phones.
- **Diagnostics:** wavy underline, cross icon and the message in text.
- **Symbol bars** per language (section 2.11).
- **Config additions:**
```ts
interface CodeSurfaceConfigAdditions {
  language: 'python' | 'cpp' | 'sql' | 'shell' | 'diff' | 'json' | 'csv' | 'text';
  mode: 'edit' | 'read' | 'read-addressable';
  gutters?: ('numbers' | 'exec' | 'breakpoints' | 'hits' | 'coverage' | 'diagnostics')[];
  selectable?: 'none' | 'lines' | 'tokens';
  slots?: { id: string; line: number; col: number; width: number; kind: 'text' | 'drop' | 'select'; options?: string[] }[];
  callouts?: { id: string; line: number; text: string; depth?: 1 | 2 | 3 | 4 | 5 }[];
  diagnostics?: { line: number; col?: number; severity: 'error' | 'warning' | 'note'; message: string }[];
}
```
- **Performance:** highlighting is incremental per line; a keystroke re-tokenises its line, and the following lines only while the lexer state at their start changes (open strings and comments).
- **Tutor:** ids gain `tok:<line>:<col>`. Describe: "Python, 18 lines, read-only; line 7 marked as the next line."
- **Artifact / web:** identical. **Generator:** no.
- **Everything else** as Stage 0 section 3.16.

### 3.6 `text-terminal` (extended from Stage 0)

**Primitive · P0 · W-A3.** Stage 0's terminal surface stays.

- **Serves:** 1.1 (consoles, `input()`), 1.2.1, 1.2.2 (Git output), 1.2.4 (pytest output), 1.9 (compiler output).
- **Config additions:** `{ ansi?: boolean; pager?: boolean; host?: string; signals?: boolean }`.

This catalogue adds:

- **ANSI colour subset** for tool output (Git, pytest, compilers): bold; red maps to `--fail-cross`, green to `--s3`, yellow to `--s2`, blue to `--code-keyword`. Tool output always carries its own words ("FAILED", "error:"), so colour is never the only cue.
- **Pager:** a simulated `less` (Space and B page, `/` searches, Q quits) for `git log`, `man` and long files.
- **Prompts per host** (`trader@research:~/project$`) for the simulated `ssh` (P1).
- **Signals:** Ctrl+C interrupts the running simulated program or Python run; Ctrl+Z suspends it (P1, with job control).
- **Live stdin** to a running Python program in `code-cell` (Stage 0 already supports `input()` prompts; the terminal now also streams output line by line as Pyodide prints).
- **Tutor:** ids gain `line:<n>` for scrollback lines, so Bertie can point at the error line in output.
- **Artifact / web:** identical. **Generator:** no.
- **Everything else** as Stage 0 section 3.17.

### 3.7 `stepper`: trace mode (extension)

**Primitive extension · P0 · W-A1.** The shared `stepper` walks a short list of captioned keyframes. Trace mode lets the same primitive drive long recorded executions (section 2.3) without a second stepping control.

- **Serves:** `code-tracer`; the `watch` mode of every 1.8 composite; 1.9 traces; long algorithms in other clusters (section 15.1).
- **Answers:** none of its own; prediction checkpoints embed their own checks, as in the shared stepper's predict mode.

- **Adds:**
  - a scrub slider over up to 10,000 steps, with tick marks for events of interest (output, exceptions, calls);
  - jumps by event kind: next compare, next swap, next call, next return, next output, next exception;
  - step over, step into and step out for code traces, computed from frame depth;
  - breakpoints on lines and on predicates (`lo > hi`, `len(stack) == 0`), evaluated on recorded state, never by running code;
  - "run to here" from a tapped line;
  - prediction checkpoints: Play and Next stop at authored steps until the learner answers (a value, the next line, an arrow);
  - speed from 0.5 to 8 steps per second;
  - "Jump to where `x` changes" from a watched variable.
- **State additions:** `{ breakpoints: { line?: number; predicate?: string }[], speed: number, watch: string[] }`.
- **Config additions:** `{ trace: Trace | AlgoTrace; checkpoints?: { step: number; predict: { prompt: string; input: InputConfig; check: Check } }[]; jumps?: AlgoEvent['kind'][] }`.
- **Keyboard:** the section 2.7 letter keys (N, S, O, B, C), Left and Right, Home and End, and the scrub slider's own arrow keys.
- **Accessibility:** a step change announces one sentence on commit; Play announces a summary every 2 seconds.
- **Tutor:** describe: "Step 31 of 140 (line 6, call depth 2). Paused at checkpoint 3." Ids: `step:<n>`, `bp:<line>`.
- **Visual:** the scrub slider sits under the step dots, with event ticks in caption type; breakpoints as 10px `--manip` discs on the slider and in the code gutter; the speed control is a segmented pill.
- **Motion:** scrubbing is direct; Play follows section 2.6.
- **Reduced motion:** section 2.6 (steps cut; Play without interpolation).
- **Artifact / web:** identical. **Generator:** no.
- **Everything else** as the shared `stepper` (calc-linalg section 3.8; Stage 0 section 3.10).
- **Performance:** seeking reconstructs state from the nearest keyframe plus at most 49 deltas, in 2 ms or less.

### 3.8 `value-table`: frame mode (extension)

**Primitive extension · P0 · W-A2.** The shared `value-table` shows records. Frame mode makes it a faithful DataFrame and SQL result view.

- **Serves:** 1.1.3 (every DataFrame), 1.2.3 (SQL results), `code-cell` results; later 1.6, 2.1 to 2.3.
- **State additions:** `{ selection?: Selection, scrollRow: number }`.

- **Adds:**
  - an index column, or up to three MultiIndex levels with merged cells for repeated outer labels;
  - a two-level column header for MultiIndex columns;
  - a dtype row under the header (`int64`, `float64`, `object`, `datetime64[ns]`, `category`, `bool`, `string`);
  - missing values rendered as muted italic `NaN`, `None`, `NaT` or `NULL` (SQL), never blank;
  - selection overlays: rows, columns and cells, with a learner overlay in `--manip-wash` and a derived overlay as a 2px `--s2` outline, so "what you selected" and "what that expression selects" can be compared;
  - a shape badge ("5 rows × 3 columns");
  - optional pandas-style truncation (first and last 5 rows with an ellipsis row);
  - virtualisation to 100,000 rows with a sticky header and index;
  - number columns right-aligned with tabular figures; dates in ISO form.
- **Config additions:** `{ frame: { index: { names: string[]; values: unknown[][] }; columns: { names: string[]; levels?: string[][] }; dtypes: string[]; data: unknown[][] }; overlays?: { learner?: Selection; derived?: Selection }; truncate?: boolean; nullStyle?: 'pandas' | 'sql' }`.
- **Answers:** `set` (cells, rows, columns), `table` (a predicted result typed into an empty frame).
- **Accessibility:** a real `<table>` with `scope` on index and header cells; the dtype row is part of each column's header name ("close, float64").
- **Tutor:** describe gives shape, dtypes, the first 5 rows as CSV and the overlays in words: "Selected rows 2024-01-03 to 2024-01-05, column 'close' (3 cells)."
- **Interactions:** grid keys as the shared primitive; Shift + arrows extend a cell selection; Ctrl or Cmd + C copies the selection as CSV.
- **Visual:** frame mode keeps the shared table style; overlays as described above.
- **Motion:** none. **Reduced motion:** nothing to change.
- **Artifact / web:** identical. **Generator:** no.
- **Everything else** as the shared `value-table` (calc-linalg section 3.13; Stage 0 section 3.12).
- **Performance:** about 40 rows in the DOM at any time; scroll handling reads no layout.

---

## 4. Composites: code and the Python language (1.1.1)

Each entry lists only what differs from the cluster contract (section 2) and the shared contract. "Uses" names the primitives and services a composite is built from.

### 4.1 `code-cell`: Code cell

**Composite · P0 · W-A1. Owned by this catalogue; replaces Stage 0's `code-editor`.** The code exercise: edit, Run against visible examples, Submit against hidden tests, read the results. One widget for Python, SQL, C++ and shell, in single-file, multi-file and notebook layouts.

- **Serves:** 0.4 (first scripts); every 1.1 drill; 1.2 (shell scripts, SQL, pytest); the 1.4 exit (least squares and PCA in NumPy, for calc-linalg); code drills in 1.5 to 3.x for other clusters; the 150 problems of 1.8; 1.9 drills; 2.4 submissions and Project Euler.
- **Uses:** `code-surface`, `text-terminal` (console and interactive stdin), `value-table` (results list; frame mode for SQL and DataFrame results), `diff-view` (expected against actual), `node-link` (outline layout for the SQL schema browser), `parsons` (phone alternative), and the `python-runner`, `sql-runner`, `cpp-runner`, `shell-interpreter`, `vfs` and `handoff` services.
- **Modes:** `drill` (a function checked by tests), `script` (stdout checked), `pytest` (the learner writes tests, run against their code), `sql` (a query checked by result set), `answer` (a numeric answer only, compared by hash: Project Euler), `checker` (an authored judge accepts any valid output: constructive problems).
- **Interactions.**
  - Run (Ctrl or Cmd + Enter) runs the visible examples and prints to the console. Submit (Ctrl or Cmd + Shift + Enter) runs the hidden suite, including efficiency and figure tests. Reset restores the starter code after a confirmation.
  - Multi-file: tabs above the editor; Alt + 1 to 9 switches files.
  - Notebook: Shift + Enter runs a cell and moves to the next; Restart kernel; Run all; execution counts `[n]` beside each cell; a "stale" mark on cells whose inputs changed since they ran.
  - "Trace this test" on a failing test opens `code-tracer` in live mode on that input (web; section 2.10).
  - Below 768px: "Build it from lines" switches to the Parsons alternative (section 2.11).
  - "Open on the web app" appears when the suite needs a runtime this target lacks.
  - After a pass: "Review my code" asks Bertie for a code-craft review at depth 1 to 5 (section 2.8).
- **Keyboard:** Ctrl or Cmd + Enter runs; Ctrl or Cmd + Shift + Enter submits; Alt + 1 to 9 switch files; Shift + Enter runs a notebook cell; Escape then Tab leaves the editor (Stage 0's rule); results, tests and buttons sit in the tab order, and Enter on a failing test opens its details.
- **State:** `{ files: Record<string, string>, active: string, cells?: { id: string; code: string; count?: number; output?: string; stale?: boolean }[], kernel?: { counter: number }, lastRun?: RunResult, status: 'idle' | 'loading' | 'running' | 'done' | 'error', attempts: number }`, with `RunResult = { kind: 'run' | 'submit'; tests: { name: string; status: 'pass' | 'fail' | 'error' | 'timeout' | 'skip'; input?: string; expected?: string; actual?: string; error?: string; stdout?: string; ms?: number }[]; stdout: string; figure?: { png?: string; svg?: string; alt: string }; resultset?: { columns: string[]; rows: unknown[][] }; complexity?: { exponent: number; lineRatio: number; timeRatio: number } }`.
- **Answers:** `code`. **Check:** `{ kind: 'code', suite }` (section 2.2).
- **Config:**
```ts
interface CodeCellConfig {
  language: 'python' | 'sql' | 'cpp' | 'shell';
  mode: 'drill' | 'script' | 'pytest' | 'sql' | 'answer' | 'checker';
  layout?: 'single' | 'files' | 'notebook';
  brief: string;                                   // Markdown with $...$; at most 120 words on screen, the rest behind "More"
  files: { path: string; starter: string; locked?: [number, number][]; readOnly?: boolean; hidden?: boolean }[];
  entry?: string;                                  // function name (drill) or file (script)
  examples: CodeTest[];                            // run on Run; visible
  suite: CodeSuite;                                // run on Submit; hidden
  db?: { schema: string; rows: string } | { generator: string; seed: number };          // SQL
  data?: Record<string, string | { generator: 'price-series'; seed: number; options?: unknown }>;   // files placed in vfs
  stdin?: 'tests' | 'interactive';
  parsons?: 'auto' | 'off' | { lines: string[]; distractors: string[] };
  review?: boolean;                                // default true
  answer?: { sha256: string; normalise: 'integer' | 'decimal-6' };   // answer mode
  heldOut?: boolean;                               // excluded from practice; used by the 1.8 exit
}
```
- **Visual:** the prototype drill's anatomy. Desktop: brief on the left (40%), code on the right, results under the code. Phones: tabs Brief, Code, Results. Results are a list with check or cross icons and the words "Passed" or "Failed". The first failure opens with its input, expected and actual values and a `diff-view`. The console is a `text-terminal`. A figure renders under the results with its alt text. SQL results show in `value-table` frame mode with `NULL` styling. An efficiency failure reads "Grows like $n^{2.0}$; target $n \log n$." Only the editor frame takes the screen's grading colours; test rows keep their icons.
- **Motion:** the tangram loader inside the Run button after 400 ms; results appear with an 80 ms stagger; the editor never moves.
- **Reduced motion:** no stagger.
- **Accessibility:** the result summary is announced ("3 of 4 examples passed; first failure: test 2, expected 0.25, got 0.2"); results form a list; figure alt text is generated from the figure's own objects ("Line chart, one line labelled close, x from 2 Jan 2024 to 31 Dec 2024, y from 92 to 131, y axis log scale").
- **Tutor:** describe: "Drill max_drawdown (Python). Last submit: 5 of 7 hidden tests passed; first failure 'flat prices': expected 0.0, got nan." `code()` gives numbered code and the last results. Ids: `line:<n>`, `test:<k>`, `file:<path>`, `cell:<k>`, `run`, `submit`. The code guard and post-pass review in section 2.8 apply.
- **Performance:** one worker per runtime; Pyodide preloaded on the title screen; runs limited to the suite's `timeLimitMs`; output capped at 4,000 characters per stream; SQL results capped at 1,000 rows; a C++ compile and run is budgeted at 20 s on the web [our choice; measured in the W-C spike].
- **Artifact / web:** the matrix in section 2.10. MicroPython-compatible Python drills run in the Artifact if WebAssembly is allowed; others hand off with the code in the URL fragment. SQL drills run on SQLite WebAssembly from the Artifact's own files. C++ drills hand off, or verify by local paste.
- **Generator:** yes. Seeded test inputs (each suite names a generator in its prelude); data files from `price-series`; the auto-Parsons alternative; `answer` mode values. Problems themselves are authored.

### 4.2 `code-tracer`: Code tracer

**Composite · P0 · W-A1 (Python). The C++ renderer is P1 · W-C.** Steps through code and shows the current line, the frames, the objects and the output. The learner predicts before stepping, sets breakpoints and watches like a debugger, and can see how many times each line ran. Its frames-and-objects layout follows the convention Python Tutor made familiar (Guo, 2013) [sourced, recalled].

- **Serves:** 1.1.1 L1, L7 to L13, L18, L19, L21, L28 to L30; 1.1.2 L5; 1.8 (recursion, linked lists, any code walk-through, line-hit counts in 1.8.1 L3); 1.9.1 L5; 1.9.2 L1 to L5, L7, L12, L13; 1.9.4 L1; optionally Stage 0's first programs.
- **Uses:** `code-surface` (read-addressable, with execution, breakpoint and hit gutters), `stepper` (trace mode), `node-link` (heap layout), `text-terminal` (read-only output), `value-table` (watch list), the `trace-recorder` service.
- **Modes:** `replay` (an authored trace), `live` (the learner's own code on a chosen input), `predict` (checkpoints that stop for a prediction), `debug` (breakpoints, watches, run to), `hits` (line-hit heat for complexity), `scope` (map each use of a name to the frame it resolves in).
- **Interactions.**
  - Pointer: step buttons; tap the gutter to toggle a breakpoint; tap a variable to add it to the watch list; tap an object to highlight every reference to it; in predict mode, drag a name's arrow to an object, type a value, or tap the next line; in scope mode, tap a name, then the frame it resolves in.
  - Keyboard: section 2.7 (N, S, O, B, C, Left, Right, Home, End). In the diagram, the `node-link` keyboard path draws predicted arrows.
- **State:** `{ step: number, mode: string, breakpoints: number[], watches: string[], predictions: Record<number, unknown>, showAllObjects: boolean }`.
- **Answers:** `mapping` (name to object; use to frame), `text` or `numeric` (a value at a step), `set` (lines that run; the buggy line), `ordering` (line sequence), `choice`.
- **Config:**
```ts
interface CodeTracerConfig {
  language: 'python' | 'cpp';
  source: string;
  trace?: Trace;                                   // authored; absent in live mode
  live?: { cell: string; test?: string };          // trace a code-cell's code on one test input
  mode: 'replay' | 'live' | 'predict' | 'debug' | 'hits' | 'scope';
  checkpoints?: { step: number; ask: 'arrow' | 'value' | 'next-line' | 'output'; target?: string; check: Check }[];
  inlinePrimitives?: boolean;                      // default true; false draws ints and strs as objects (teaching `is`)
  panels?: ('frames' | 'heap' | 'output' | 'watch')[];
  startAt?: number;
  showWhy?: Record<string, ShowWhy>;
}
```
- **Python rendering:** the Global frame at the top; locals in definition order; primitives inline; references as arrows; lists and tuples as `cells` nodes with index labels; dicts as two-column records; instances as records headed by their class name; class objects; functions with name and parameters, closures as a small record of cells; generators showing their suspended frame inside them; NumPy arrays summarised (dtype, shape, first values).
- **C++ rendering (P1):** values live inside their frame (`int x  5`); arrays inline and contiguous with addresses; pointers show the address and an arrow; a reference is a second name tag on the same box, with no arrow, because a reference is another name for the object; heap blocks on the right with type, size and address; freed blocks hatched; dangling pointers dashed with a cross; uninitialised values "?" with a dotted border; a destroyed object stays one step labelled "destroyed", then goes; polymorphic objects show `vptr` pointing at a vtable record of function slots.
- **Show-why keys:** `alias` (both names pulse while the shared object changes), `divergence` (jump to the first step where the learner's prediction and the trace disagree), `unwind` (frames peel off one at a time; in C++, destructor calls are listed), `late-binding` (every closure's arrow lands on the one shared cell), `copy-vs-alias` (a ghost copy appears beside the original for a slice, and does not for plain assignment).
- **Visual:** section 2.5. Desktop: code on the left (45%), frames and objects on the right, output below. Phones: code on top, collapsed to 8 lines around the next line; the diagram below; output behind a toggle.
- **Motion:** arrows re-point over 200 ms and new objects fade in over 150 ms as consequences of a step; freed objects fade out over 200 ms; predicted arrows follow the pointer directly.
- **Reduced motion:** all cuts; the changed parts keep the "changed" underline for one step.
- **Accessibility:** a text alternative per step ("Frames: global: a refers to o1, b refers to o1. Objects: o1 list [1, 2]."); each step announced on commit; the watch list is a table.
- **Tutor:** describe: "Step 12 of 40, line 5. Frame f: n = 3, acc refers to o2. Output so far: '1', '2'." Ids: `line:<n>`, `frame:<fn>#<k>`, `var:<frame>.<name>`, `obj:<id>`, `slot:<obj>.<i>`, `out:<n>`, `step:<n>`, `bp:<line>`. Suggestions: "Step to line 9", "Watch total".
- **Performance:** step render 4 ms or less; heap layout incremental; above 80 objects, containers collapse to summaries. Live tracing runs the learner's code under `sys.settrace`, which slows it by an order of magnitude or more [unverified factor in Pyodide], so live traces stop at 10,000 steps or 2 s.
- **Artifact / web:** replay works everywhere. Live mode needs Pyodide on the web; in the Artifact it needs MicroPython built with `sys.settrace` [unverified], otherwise it hands off.
- **Generator:** yes. Predict families for aliasing, copies, default arguments, closures, scope and generators, with seeded names and values; traces come from CI seed banks so the Artifact needs no Python.

### 4.3 `predict-output`: Predict the output

**Composite · P0 · W-A1.** "Act before you read" for code. The learner predicts what code prints, returns or produces, then Check compares the prediction with the recorded result. A wrong prediction plays `divergence`: the tracer opens at the step where reality and the prediction part ways.

- **Serves:** 1.1.1 L2, L4, L5, L7, L10, L12, L13, L17 to L19; 1.1.2 L2, L8, L12; 1.1.3 L7; 1.2.3 L1, L4, L12 (tables); 1.8 (algorithm outputs); 1.9.1 L4, L6; 1.9.2 L13; shell output in 1.2.1.
- **Uses:** `code-surface` (read), a monospace prediction field (`free-response` in code style), `value-table` frame mode (table predictions), `choice`, `diff-view` (prediction against actual), `code-tracer` (show-why).
- **Prediction kinds:** `stdout` (lines of text), `value` (a Python `repr`), `error` (an exception type and the line that raises), `table` (a SQL or pandas result: fill the cells, or give the row count and columns), `compiles` (C++: which lines compile), `choice`.
- **Interactions.** Type the prediction (or fill the table, tap lines, pick an option); Check; after grading, "Show the run" reveals the real output beside the prediction.
- **Keyboard:** The prediction field is a labelled textarea (Escape then Tab leaves it); table predictions use `value-table` grid keys; option and line choices take keys 1 to 9 or Space; Enter checks.
- **State:** `{ prediction: string | string[][] | number[] | string, revealed: boolean }`.
- **Answers:** `text`, `table`, `set`, `choice`. **Checks:** `text` (section 2.2), `resultset`, `set`, `choice`.
- **Config:**
```ts
interface PredictOutputConfig {
  language: 'python' | 'cpp' | 'sql' | 'shell';
  source: string;
  setup?: string;                                  // shown collapsed: imports, data
  predict: { kind: 'stdout' | 'value' | 'error' | 'table' | 'compiles' | 'choice'; options?: string[]; columns?: string[] };
  recorded: { stdout?: string; value?: string; error?: { type: string; line: number };
              table?: { columns: string[]; rows: unknown[][] }; compiles?: number[] };   // written by CI
  trace?: Trace;                                   // enables divergence (Python, authored C++)
  compare?: 'exact' | 'normalised-ws' | 'lines-unordered';
}
```
- **Visual:** code above; the prediction field below in the code token with line numbers; after grading, the actual output appears beside it in a `diff-view`. The prediction field is the answer object.
- **Motion:** the reveal fades in over 200 ms; `divergence` opens the tracer inline.
- **Reduced motion:** cuts.
- **Accessibility:** a labelled multi-line field; the reveal is announced ("Actual output has 3 lines; line 2 differs").
- **Tutor:** describe before grading: the code and "Learner predicts: ...", with the recorded output marked hidden. Ids: `line:<n>`, `pred:<n>`, `out:<n>`.
- **Performance:** trivial; no runtime, because the output is recorded.
- **Artifact / web:** identical. Generated items come from seed banks where Python is absent, and are computed live on the web.
- **Generator:** yes. Families per concept: integer division and modulo with negatives, slicing, aliasing, string methods, comprehension order, generator exhaustion, dict ordering, stable sorting, NumPy dtypes, pandas alignment, SQL `NULL` counts, C++ conversions; seeded values; outputs from CI or Pyodide.

### 4.4 `parsons`: Parsons problem

**Composite · P0 · W-A1.** Put shuffled lines of code in order and at the right indentation, leaving out distractors. Parsons problems (Parsons and Haden, 2006) take less time than writing the same code and gave similar gains on later tests in a study by Ericson and colleagues (2017) [sourced, recalled; check the citation before it appears in product copy]. It is also the phone alternative for every code drill (decision 15).

- **Serves:** 1.1.1 L8, L17; every `code-cell` drill on phones; 1.2 (shell scripts, SQL clauses); 1.8 (algorithm skeletons, such as the pointer updates that reverse a linked list); 1.9.
- **Uses:** `token-tray` (an ordered zone with indent levels), `code-surface` (line rendering), the `code-cell` runner (execution grading).
- **Interactions.**
  - Pointer: drag lines from the tray into the solution; drag sideways to indent, snapping to 4-space levels; two-tap on touch.
  - Keyboard: Space lifts, Up and Down move, Left and Right change indentation, Space drops, Escape cancels.
- **Adaptive help** after two not-yet results: merge two adjacent correct lines into one block, or remove one distractor and show why it was wrong. This follows Ericson's adaptive Parsons problems [our choice, informed by sourced research]. Mastery records that help was used.
- **State:** `{ placed: { line: string; indent: number }[], tray: string[], helped: number }`.
- **Answers:** `ordering` with indentation.
- **Check:** by execution where a runtime exists (assemble and run the suite, so any order that passes is right), otherwise by constraints (`A` before `B`; `C` at indent 2). Never one fixed order where several are valid.
- **Config:**
```ts
interface ParsonsConfig {
  language: 'python' | 'cpp' | 'sql' | 'shell';
  lines: { id: string; code: string; indent?: number }[];
  distractors?: { id: string; code: string; why: string }[];
  grading: { kind: 'execute'; suite: CodeSuite }
         | { kind: 'constraints'; before: [string, string][]; indent: Record<string, number>; acceptedOrders?: string[][] };
  indentation?: boolean;                           // two-dimensional Parsons; default true for Python
  fixedLines?: string[];                           // given in place, such as the def line
  adaptive?: boolean;
}
```
- **Visual:** lines are full-width lip-token chips in the code token; dotted indentation guides every 4 spaces; distractors look like real lines until graded. After grading, misplaced lines take the amber border and cross badge, kept correct lines dim, and a used distractor shows its `why`.
- **Motion:** drops snap with `spring-snap`; siblings slide over 200 ms.
- **Reduced motion:** instant placement.
- **Accessibility:** the solution is a list; each line reads "line 3 of 7, indent 2: total += x"; moves are announced.
- **Tutor:** describe: "Parsons: 5 of 7 lines placed. Order: L1, L3, L2, L4, L6. Indents: 0, 1, 1, 2, 1." Ids: `pline:<id>`, `slot:<n>`.
- **Performance:** trivial.
- **Artifact / web:** where no runtime exists, constraint grading. For auto-Parsons, CI enumerates the line orders that pass the tests (every permutation up to 9 lines; def-use analysis beyond) and ships them as `acceptedOrders`, so the Artifact grades without Python.
- **Generator:** yes. Auto-Parsons from any `code-cell` reference solution, with distractors from `mutant-forge`; seeded shuffles.

### 4.5 `code-blanks`: Code with blanks

**Composite · P0 · W-A1.** Complete code with gaps: type an expression, pick from a menu, or drag a token into the slot ("drag the right update into `lo = ...`"). Graded by running the completed code where possible, so any correct fill passes.

- **Serves:** 1.1 (comprehensions, slices, conditions, format specs); 1.1.2 L7 (`[:, None]`); 1.1.4 (plot code); 1.2 (Git commands, SQL clauses, pytest decorators); 1.8 (binary-search updates, DP transitions); 1.9 (`const` placement, `std::move`).
- **Uses:** `code-surface` (inline slots), `token-tray` (palette), `choice` (menu slots), the `code-cell` runner.
- **Interactions.** Tap a slot then a token, or drag; type into text slots; Tab moves between slots; Space lifts and drops tokens; Enter checks.
- **Keyboard:** Tab and Shift + Tab move between slots; in a drop slot, Space opens the palette, arrows choose and Space places; menu slots are native selects; Enter checks.
- **State:** `{ fills: Record<string, string> }`.
- **Answers:** `mapping` (slot to token) or `code` (the completed source).
- **Check:** by execution, or per slot with accepted alternatives; per-slot marks (green slots lock, amber slots reopen).
- **Config:**
```ts
interface CodeBlanksConfig {
  language: 'python' | 'cpp' | 'sql' | 'shell';
  template: string;                                // code with slots written ⟦id⟧
  slots: Record<string, { kind: 'text' | 'drop' | 'select'; width: number; options?: string[]; accept?: string[] }>;
  palette?: { id: string; code: string; copies?: number }[];   // includes distractor tokens
  grading: { kind: 'execute'; suite: CodeSuite } | { kind: 'per-slot' };
}
```
- **Visual:** slots are dashed inline boxes `width` characters wide; filled slots show `--manip` text until graded; the palette sits below as lip-token chips.
- **Motion:** drops snap with `spring-snap`.
- **Reduced motion:** instant.
- **Accessibility:** slots are labelled inputs or buttons ("blank 2 of 3, line 4").
- **Tutor:** describe: "line 4: if ⟦a: lo <= hi⟧: ...; line 6: lo = ⟦b: empty⟧." Ids: `slot:<id>`, `token:<id>`, `line:<n>`.
- **Performance:** trivial.
- **Artifact / web:** per-slot grading without a runtime; CI enumerates palette combinations (up to 512), runs each, and ships the accepted ones.
- **Generator:** yes. Slices that produce a target output; boolean conditions; format specs; SQL `WHERE` clauses; seeded values.

### 4.6 `code-annotator`: Annotated code

**Composite · P0 · W-A1.** The owner's code-craft format as an interactive worked example: code notes with complexity, inline rationale on non-obvious lines, the senior-developer paragraph and the plain-English translation, behind a depth control from 1 to 5. It is also an exercise: match blocks to purposes, or tap the line that makes the solution $O(n)$.

- **Serves:** 1.1.1 L31; every worked solution and Generalise screen with code in 1.1, 1.2, 1.8 and 1.9; Bertie's post-pass review renders here.
- **Uses:** `code-surface` (read-addressable, callouts, line and token selection), `slider` (discrete depth), `token-tray` (matching), `live-formula` (the complexity line), `region-select`.
- **Depth, as in code-craft:**

| Depth | Shows |
|---|---|
| 1 | One or two lines of notes (approach, time and space); inline notes; a one-line translation per block |
| 2 | Level 1 plus the senior-developer paragraph |
| 3 (default) | Fuller notes with the key trade-off; a full block-by-block translation |
| 4 | Level 3 plus segment-level translation of the non-obvious lines and expressions |
| 5 | A plain-English restatement of the problem and its sub-questions first; a line-by-line translation that covers each token's role |

- **Interactions.** The depth slider (also keys 1 to 5); tap a block bracket to open its translation; at depth 4 and 5, tap a line or token for its translation; in exercises, drag purpose cards onto blocks, or tap a line.
- **Keyboard:** Keys 1 to 5 set the depth; Tab moves through block brackets, then through lines and tokens at depth 4 and 5; Enter opens a translation; in matching, Space lifts a purpose card, arrows choose a block and Space drops.
- **State:** `{ depth: 1 | 2 | 3 | 4 | 5, open: string[], mapping?: Record<string, string>, selected?: string[] }`.
- **Answers:** `mapping`, `set`, `choice`.
- **Config:**
```ts
interface CodeAnnotatorConfig {
  language: 'python' | 'cpp' | 'sql' | 'shell';
  source: string;
  notes: { short: string; full: string };              // $...$ allowed
  inline: { line: number; text: string }[];            // only on non-obvious lines
  seniorDev: string;
  restatement?: { problem: string; subQuestions: string[] };   // depth 5
  blocks: { id: string; lines: [number, number]; purpose: string; translation: string }[];
  segments?: { line: number; cols?: [number, number]; text: string }[];   // depth 4
  tokens?: { line: number; col: number; len: number; text: string }[];    // depth 5
  depth?: 1 | 2 | 3 | 4 | 5;
  exercise?: { kind: 'match-blocks'; purposes: string[] } | { kind: 'find-line'; prompt: string; correct: number[] };
}
```
- **Visual:** block brackets in the gutter (2px `--s6`, labelled); inline notes as comment-coloured callouts; the senior-developer paragraph on a card with the overline "Senior developer"; the translation pane on the right on desktop and below on phones; the open block tinted `--bg-hover`.
- **Motion:** translations open over 150 ms.
- **Reduced motion:** instant.
- **Accessibility:** all text; the depth slider is a native range labelled "Depth 3: block by block".
- **Tutor:** describe: "Annotated solution, depth 3, 4 blocks; block 2 open." Ids: `block:<id>`, `line:<n>`, `tok:<l>:<c>`. In live mode, after a pass, Bertie returns the annotation in this config's shape for the learner's own code, and the engine checks every line reference before rendering it.
- **Performance:** trivial.
- **Artifact / web:** identical for authored annotations; live annotation needs the tutor.
- **Generator:** no.

### 4.7 `diagnostic-reader`: Diagnostic reader

**Composite · P0 · W-A1 for Python tracebacks, pytest, SQLite, bash and Git; P1 · W-C for compiler, linker and sanitizer reports.** Read error output: link each frame or diagnostic to its code, find the one that matters, say what it means.

- **Serves:** 1.1.1 L11, L14, L21, L24; 1.1.3 L4; 1.2 (pytest reports, SQL errors, shell errors, Git messages, CI logs); 1.9 (compiler errors, template walls, linker errors, sanitizer reports).
- **Uses:** `code-surface` (the report and the code, both read-addressable), `region-select` (tappable frames and diagnostics), `choice`.
- **Parsers:** Python tracebacks, including chained exceptions ("During handling of the above exception") and `raise ... from`; pytest failure reports (introspection lines, `E` lines, short summary); SQLite errors; bash errors; Git errors; GCC and Clang diagnostics (`file:line:col: severity: message`, notes, "In instantiation of", "required from"); linker errors ("undefined reference", "multiple definition"); AddressSanitizer and UndefinedBehaviorSanitizer reports (error kind, access, frames, allocation and free stacks).
- **Interactions.** Tap a frame and its code line lights, and the reverse; tap "the line that matters"; choose the plain-English meaning; toggle "My code only" to collapse library frames; collapse template instantiation chains.
- **Keyboard:** Tab enters the report; Up and Down move between frames or diagnostics; Enter jumps to the linked code line and Escape returns; Space marks the answer; M toggles "My code only".
- **State:** `{ selected: string[], mineOnly: boolean, meaning?: string }`.
- **Answers:** `set` (frames or diagnostics), `choice` (meaning), `mapping` (diagnostic to build stage, used by `compile-pipeline`).
- **Config:**
```ts
interface DiagnosticReaderConfig {
  format: 'python-traceback' | 'pytest' | 'sqlite' | 'bash' | 'git' | 'gcc' | 'clang' | 'linker' | 'asan' | 'ubsan';
  report: string;                                  // captured verbatim at build time, or from a live run
  code?: { path: string; source: string; language: string }[];
  task: 'find-origin' | 'find-first-error' | 'meaning' | 'link-frames' | 'explore';
  ownCode?: string[];                              // paths that count as the learner's code
  choices?: { id: string; text: string }[];
}
```
- **Visual:** the report in the terminal style with parsed rows: frames as tappable rows (file, line, function), the error line in weight 600, library frames muted; a connector from the selected frame to the code pane (side by side on desktop; "Jump to code" on phones).
- **Show-why keys:** `frame-link` (draw the connector and light the code line), `first-error` (dim every cascading error after the first), `cause-chain` (step through chained exceptions).
- **Motion:** the connector draws over 200 ms.
- **Reduced motion:** the connector appears at once.
- **Accessibility:** frames form a list ("frame 3 of 4: analysis.py, line 12, in max_drawdown"); the raw report stays available.
- **Tutor:** describe: "Python traceback, 4 frames (2 in learner code). ZeroDivisionError: division by zero at analysis.py:12 in max_drawdown." Ids: `frame:<n>`, `diag:<n>`, `line:<path>:<n>`. "Explain this error" sends this structure.
- **Performance:** parsing a 500-line report in 2 ms or less.
- **Artifact / web:** identical; live reports from `code-cell` runs are parsed the same way.
- **Generator:** yes (Python). Bug families (off-by-one `IndexError`, `KeyError`, `TypeError` from `None`, `AttributeError`, division by zero, shadowed module) with seeded code; reports captured in CI into seed banks.

### 4.8 `float-inspector`: Floating-point inspector

**Composite · P0 · W-A1.** What a float really stores, and the consequences: binary fractions, the gap between neighbouring doubles, comparisons with tolerance, cancellation, summation order, NaN and infinity, and decimal arithmetic for money.

- **Serves:** 1.1.1 L3, L4; 1.1.2 L12; 1.2.4 L4 (`pytest.approx`); 1.9.4 L2; other clusters: conditioning and numerical stability in 1.3, 1.4 and 1.6 (for example the unstable variance formula $E[X^2] - E[X]^2$).
- **Uses:** `array-strip` (bits mode, 64 or 32 cells grouped into sign, exponent and mantissa), `number-line` (representable neighbours), `live-formula`, `slider`, `value-table`, `numeric-input`.
- **Modes:** `bits`, `nearest` (type a decimal; see the stored double, its exact decimal expansion and the error), `neighbours` (the gap between adjacent doubles grows with magnitude; relative spacing $2^{-52}$), `compare` (`0.1 + 0.2 == 0.3`; `math.isclose` with relative and absolute tolerance), `cancel` ($(1 + x) - 1$ for small $x$; the two variance formulas), `sum` (left to right, sorted, pairwise as NumPy does, Kahan and `math.fsum`), `special` (NaN, infinities, $-0.0$; `nan != nan`; sorting with NaN), `decimal` (`Decimal` with a context precision and rounding mode; round half to even against half up).
- **Interactions.** Tap bits to flip them; type a decimal; drag along the neighbours line, snapping to representable values; slide the magnitude; in `sum`, slide $n$ and toggle the order.
- **Keyboard:** Bits form a roving group (Left and Right move, Space flips); the neighbours line is a slider (Left and Right step one representable value, Shift steps ten); number fields and sliders are native.
- **State:** `{ mode: string, bits: string, input: string, magnitude: number, order: string, n: number, width: 32 | 64 }`.
- **Answers:** `numeric` with tolerance (for example, the gap above $10^{16}$ is 2), `choice`, `set` (which comparisons are true), `text`.
- **Config:**
```ts
interface FloatInspectorConfig {
  mode: 'bits' | 'nearest' | 'neighbours' | 'compare' | 'cancel' | 'sum' | 'special' | 'decimal';
  width?: 32 | 64;
  value?: string;                                  // decimal string, e.g. '0.1'
  sum?: { terms: string; n: [number, number]; orders: ('naive' | 'sorted' | 'pairwise' | 'kahan' | 'fsum')[] };
  decimal?: { precision: number; rounding: 'ROUND_HALF_EVEN' | 'ROUND_HALF_UP' | 'ROUND_DOWN' };
  locked?: ('bits' | 'input' | 'magnitude')[];
}
```
- **Implementation:** exact decimal expansions with BigInt arithmetic (mantissa times a power of two); float32 through `Float32Array`; naive, sorted and Kahan sums computed in JavaScript, which shares IEEE 754 doubles with CPython; NumPy's pairwise sums are recorded from real NumPy in CI rather than reimplemented [our choice: its blocking details are an implementation detail we should not copy].
- **Visual:** the sign bit, exponent field and mantissa field take slots s2, s4 and s6 as labelled bands (direct labels, never colour alone); flipped bits are `--manip`; the neighbours line shows representable values as ticks with the typed value as a hollow ring between them.
- **Motion:** bit flips update the value directly; the magnitude slider is direct.
- **Reduced motion:** nothing to change.
- **Accessibility:** bits read as "bit 52, exponent, 1"; the value, its exact expansion and the error are text; the table view lists neighbours.
- **Tutor:** describe: "Double nearest 0.1 is 0.1000000000000000055511151231257827...; error 5.55e-18. Neighbours 0.09999999999999999 and 0.10000000000000002." Ids: `bit:<i>`, `field:sign`, `field:exponent`, `field:mantissa`, `tick:<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Nearest double to a decimal; gap at a magnitude; which comparisons hold; which summation order is closest; `Decimal` rounding outcomes.

### 4.9 `format-lab`: Format lab

**Composite · P0 · W-A1; C++ `std::format` mode P1.** Build format specifications and see the output change for several values at once: Python's format mini-language, `strftime` and `strptime` date codes, and `std::format`.

- **Serves:** 1.1.1 L6; 1.1.3 L15 and L19 (dates); 1.1.4 (axis labels); 1.9 (output formatting).
- **Uses:** `token-tray` (spec parts as chips: fill, align, sign, width, grouping, precision, type), `code-surface` (`f"{x:{spec}}"` shown live), `value-table` (values and their outputs), `numeric-input` (width and precision steppers).
- **Interactions.** Drag or tap chips into the spec slot; step width and precision; or type the spec directly. Every test value's output updates as the spec changes.
- **Keyboard:** Chips follow `token-tray` keys (Space lifts, arrows move, Space drops); the spec field accepts typing; Up and Down on the width and precision steppers change them by one.
- **State:** `{ spec: string }`.
- **Answers:** `text` (the spec), graded by `formatProduces(spec, cases)`, so any spec that produces the targets passes.
- **Config:** `{ mode: 'fstring' | 'strftime' | 'strptime' | 'cpp'; values: (number | string)[]; targets?: string[]; parts?: string[]; free?: boolean }`.
- **Implementation:** a JavaScript implementation of the mini-language for integers, floats, percentages and strings, and of the `strftime` codes that do not depend on the C library's locale (`%c` and `%x` are excluded). CI compares it with CPython on 10,000 random specs and values.
- **Visual:** chips in the code token; outputs in a table with the target column beside them; a mismatching row shows its target in muted text.
- **Motion:** none.
- **Reduced motion:** nothing to change.
- **Accessibility:** outputs are a table; the spec is a labelled field.
- **Tutor:** describe: "Spec ',.2f'; outputs: 1,234,567.89 / -0.07 / nan." Ids: `part:<name>`, `row:<i>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Target outputs from seeded values and specs.

### 4.10 `json-explorer`: Nested data explorer

**Composite · P0 · W-A1.** Navigate nested dictionaries and lists (an API response, a config file). Tap a value to get its access path; type a path to light its value; compare JSON with Python literals; flatten to a table.

- **Serves:** 1.1.1 L16; 1.1.3 (flattening records into frames); 1.2 (configuration files); 2.x project data feeds.
- **Uses:** `node-link` (outline layout), `code-surface` (raw JSON with token ids linked to nodes), `value-table` (the flattened view), a path field.
- **Interactions.** Expand and collapse; tap a node and its path appears with each segment linked; type a path and the value lights, or the error appears ("KeyError: 'Quotes'"); in collect mode, tap every value that `[q["bid"] for q in data["quotes"]]` would gather.
- **Path language:** Python subscript chains with string keys and integer indices (negatives allowed) and `.get(key, default)`; collect mode adds one comprehension over a list.
- **Keyboard:** The outline is a tree (Up and Down move, Right expands, Left collapses, Enter selects and writes the path); the path field evaluates on Enter.
- **State:** `{ expanded: string[], selected: string[], path: string }`.
- **Answers:** `text` (a path, graded by `pathSelects`), `set` (nodes), `choice`.
- **Config:** `{ data: unknown; source: 'json' | 'python'; task: 'path-of' | 'value-at' | 'collect' | 'json-vs-python' | 'flatten' | 'explore'; target?: string[] }`.
- **Visual:** outline rows with type badges (`dict`, `list`, `str`, `float`); keys in ink, values in the code token; the selected value `--manip-wash`; path segments as linked chips.
- **Motion:** expand and collapse over 150 ms.
- **Reduced motion:** instant.
- **Accessibility:** a `tree` with `aria-expanded`; each node reads "key bid, float, 101.25, path data, quotes, 0, bid".
- **Tutor:** describe: "JSON object, 3 top-level keys; selected data['quotes'][0]['bid'] = 101.25." Ids: `node:<path>`.
- **Performance:** at most 500 nodes rendered; larger data shows the first 50 items of each list with "and 950 more".
- **Artifact / web:** identical.
- **Generator:** yes. Seeded nested structures (depth up to 4, breadth up to 5) in market vocabulary (quotes, trades, positions) with target values.

### 4.11 `search-path`: Search path

**Composite · P0 · W-A1.** Ordered search where the first match wins: `PATH` for commands and `sys.path` for imports. Activating a venv puts its `bin` first; the script's own folder comes first in `sys.path`, so a local `random.py` hides the standard library; `pip` belongs to whichever Python it was installed with.

- **Serves:** 1.1.1 L24, L25; 1.2.1 L8; 1.9 (which compiler runs).
- **Uses:** `token-tray` (the ordered directory list), `node-link` (outline of each directory's contents), `text-terminal` (`which -a python3`, `python3 -c "import random; print(random.__file__)"`).
- **Modes:** `path` (shell commands), `syspath` (imports: script folder, `PYTHONPATH`, the standard library, each interpreter's `site-packages`), `pip` (two Pythons, two pips: which one installed the package).
- **Interactions.** Drag directories to reorder; toggle "Activate venv"; type a command or module name and the search walks the list top to bottom, stopping at the first match; before running, tap the directory you expect to win.
- **Keyboard:** Directories follow `token-tray` keys (Space lifts, Up and Down move, Space drops); V toggles the venv; the query runs on Enter; in prediction, Up and Down choose a directory and Space marks it.
- **State:** `{ order: string[], venv: boolean, query: string, prediction?: string }`.
- **Answers:** `choice` or `set` (the winning directory), `ordering` (an order that meets a goal), `state`.
- **Config:** `{ mode: 'path' | 'syspath' | 'pip'; dirs: { path: string; contents: string[]; kind?: 'venv' | 'system' | 'user' | 'project' }[]; query?: string; goal?: { name: string; mustResolveTo: string } }`.
- **Visual:** directories as lip-token rows; contents in outline under each; the walk highlights each directory in turn as "active" and the match as "special" with the label "found".
- **Motion:** the walk steps 80 ms per directory as a consequence of the query; dragging is direct.
- **Reduced motion:** the result appears with the checked directories marked.
- **Accessibility:** the list is ordered and announced ("python3 found in /home/you/project/.venv/bin, the first of 5 directories").
- **Tutor:** describe: "PATH order: .venv/bin, /usr/local/bin, /usr/bin. venv active. python3 resolves to .venv/bin/python3." Ids: `dir:<path>`, `file:<path>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Seeded `PATH` orders and installation locations; shadowing scenarios.

### 4.12 `pipeline-flow`: Pipeline flow

**Composite · P0 · W-A1 (iter), W-A2 (pandas), W-A3 (shell, SQL).** Data moving through stages, with every connector inspectable: shell pipes (lines of text), Python iterator chains (lazy, one item at a time), the logical order of a SQL query (tables), pandas method chains (frames).

- **Serves:** 1.1.1 L18; 1.1.3 L22; 1.2.1 L2, L3, L6; 1.2.3 L2, L5, L9.
- **Uses:** `token-tray` (stages), `node-link` (row or layered layout for stages; CTEs branch), `text-terminal` (read-only text at connectors), `value-table` frame mode (tables at connectors), `stepper` (pulls in iter mode), and the `shell-interpreter`, `sql-runner`, `frame-core` services.
- **Modes.**
  - `shell`: stages are commands; a connector shows the text flowing (the first 20 lines and the count); stderr branches off as a side channel.
  - `iter`: pressing `next()` on the consumer pulls one item through the chain, stage by stage; suspended stages are marked; a second pass over an exhausted generator yields nothing. Authored chains use recorded traces; generated ones use a JavaScript model of `map`, `filter`, `zip`, `enumerate`, `islice` and simple generator functions.
  - `sql`: clauses in logical order: `FROM` and `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, window functions, `SELECT`, `DISTINCT`, `ORDER BY`, `LIMIT`. Each connector holds the intermediate table, recorded at build time by running each prefix of the query in SQLite. An alias is shown to exist only from `SELECT` onwards.
  - `pandas`: each `.method()` result in a chain, from `frame-core` or recorded.
- **Interactions.** Tap a connector to inspect it; drag stages to reorder; add a stage from the palette; predict an intermediate (type text or fill a table); in iter mode, Step pulls one item.
- **Keyboard:** Tab moves between stages and connectors; Enter on a connector opens it; stages reorder with `token-tray` keys; N pulls the next item in iter mode; table predictions use grid keys.
- **State:** `{ stages: string[], inspected?: number, pulled: number, prediction?: unknown }`.
- **Answers:** `ordering`, `text`, `table`, `state` (the final output equals the target), `code` (the generated command or query).
- **Config:**
```ts
interface PipelineFlowConfig {
  mode: 'shell' | 'iter' | 'sql' | 'pandas';
  stages: { id: string; code: string; locked?: boolean }[];
  palette?: { id: string; code: string }[];
  input: string | { table: string } | { frame: string };     // file text, table name or frame id
  intermediates?: Record<string, unknown>;                   // recorded by CI for authored pipelines
  task: 'inspect' | 'order' | 'build' | 'predict-at' | 'explore';
  predictAt?: number;
  goal?: unknown;
}
```
- **Visual:** stages as lip-token chips in the code token, joined by connectors drawn as 2px ink pipes with a count badge ("14 lines", "6 rows"); the inspected connector opens a panel below; in iter mode the travelling item is a small `--s2` chip.
- **Motion:** in iter mode an item travels between stages over 200 ms per stage as a consequence of `next()`; reorders slide over 200 ms.
- **Reduced motion:** items appear at their destination; reorders cut.
- **Accessibility:** stages form a list; each connector's content is reachable as text or a table; pulls are announced ("next() returned 4; filter skipped 3").
- **Tutor:** describe: "Shell pipeline: grep ERROR log.txt | cut -d, -f2 | sort | uniq -c. Stage 3 output: 14 lines." Ids: `stage:<id>`, `pipe:<n>`.
- **Performance:** text connectors show 20 lines; tables use frame-mode virtualisation.
- **Artifact / web:** identical for shell, iter and recorded SQL; free SQL editing needs SQLite WebAssembly (section 2.10).
- **Generator:** yes. Shell pipeline goals over seeded logs and CSVs; clause-order items; iterator predictions.

### 4.13 `regex-lab`: Regex lab

**Composite · P0 · W-A1; step mode P1 · W-B1.** Regular expressions with live highlighting over test strings: match all the positives and none of the negatives, capture groups, greedy against lazy, anchors and flags. Explain mode labels each token; step mode shows the backtracking engine at work, including catastrophic backtracking. Glob mode covers shell globbing, `.gitignore` and `pathlib`.

- **Serves:** 1.1.1 L27; 1.2.1 L4, L5; 1.2.2 L12; 2.x data cleaning.
- **Uses:** `code-surface` (pattern editor with regex tokens; read-addressable in explain mode), `value-table` (test strings with match columns), `region-select` (predict which strings match), `token-tray` (build a pattern from pieces, for beginners), `array-strip` (chars mode for the step cursor).
- **Flavours:** Python `re` by default; POSIX ERE for `grep -E`. Patterns are translated to JavaScript `RegExp` for live highlighting where the two agree. Constructs JavaScript lacks, such as atomic groups and possessive quantifiers (added to Python's `re` in 3.11), are rejected in live mode with a message [our choice]. CI compares highlighting with CPython `re` on a corpus of 5,000 pattern and string pairs.
- **Glob mode:** our own matcher for `*`, `?`, `[...]` and `**`, and for `.gitignore` rules (a leading slash anchors, a trailing slash means directories only, `!` negates, the last matching rule wins). CI compares it with `git check-ignore` on a corpus.
- **Step mode (P1):** our own backtracking matcher for a subset (literals, classes, `.`, `*`, `+`, `?`, `{m,n}`, groups, alternation, anchors, lazy quantifiers) that yields its attempts. A step counter shows `(a+)+b` on a run of `a`s growing exponentially.
- **Interactions.** Type a pattern and matches light across the strings; toggle flags; tap a token to read its meaning; tap the strings you predict will match; in step mode, Step through attempts.
- **Keyboard:** The pattern field updates on every keystroke; Alt + I and Alt + M toggle the IGNORECASE and MULTILINE flags; Tab moves into the strings, where Space marks a predicted match; in explain mode, Left and Right move between pattern tokens; in step mode, N steps.
- **State:** `{ pattern: string, flags: string[], predicted?: string[], step?: number }`.
- **Answers:** `text` (the pattern), graded by `matchesSets(pattern, { positives, negatives, groups })`; `set` (predicted matches); `choice`.
- **Config:** `{ mode: 'golf' | 'predict' | 'groups' | 'explain' | 'step' | 'glob'; flavour?: 'python' | 'ere' | 'gitignore' | 'shell'; positives: string[]; negatives?: string[]; groups?: Record<string, string[]>; files?: string[]; pattern?: string }`.
- **Visual:** matched spans underlined 2px in `--s6` with a light wash; capture groups numbered with labels and slots s2, s4 and s5; non-matching strings that should match get a muted "missed" label after grading; the pattern's tokens are coloured by kind with a legend line of words.
- **Motion:** highlights update as you type; the step cursor moves as a consequence of Step.
- **Reduced motion:** nothing to change.
- **Accessibility:** each string reads "matches, group 1 '2024', group 2 '03'" or "no match"; explanations are a list.
- **Tutor:** describe: "Pattern ^[A-Z]{1,5}$, flags none; matches 7 of 8 positives (misses 'BRK.B'), 0 of 6 negatives." Ids: `ptok:<i>`, `str:<i>`, `group:<n>`.
- **Performance:** highlighting under 1 ms for 50 strings; live mode refuses patterns whose matching takes over 50 ms on any string, with a note pointing to step mode.
- **Artifact / web:** identical.
- **Generator:** yes. Golf sets built from seeded token lists (tickers, dates, prices, ISIN-like codes) where a reference pattern exists; predict-match sets.

### 4.14 `hash-table`: Hash table

**Composite · P0 (chaining, load factor, membership cost, hashability) · W-A1; P1 (open addressing, resizing cost, CPython's compact layout, adversarial keys) · W-B1.** How hashing turns a key into a bucket, why lookups are $O(1)$ on average and $O(n)$ at worst, why keys must not change, and what resizing costs.

- **Serves:** 1.1.1 L14, L15; 1.8.2 L2, L3, L8; 1.8.3 L8 (LRU); 1.9.3 L2 (`unordered_map`).
- **Uses:** `array-strip` (vertical buckets), `node-link` (row layout for chains), `live-formula` (`hash(key) mod m`), `slider` (table size $m$), `value-table` (the keys), `complexity-lab` (probe-count chart).
- **Hash functions:** `toy` (a visible polynomial hash with base 31, so learners can compute it), `python-int` (CPython hashes small integers to themselves; `hash(-1) == -2` as a curiosity), `python-str` (shown as an opaque value that changes per session, to teach hash randomisation and `PYTHONHASHSEED`, never presented as the real value).
- **Interactions.** Type a key and Insert: the hash and index appear and the key travels to its bucket. Lookup shows each probe. Tap a bucket to inspect it. Slide $m$. Toggle the collision strategy (P1). Before inserting, tap the bucket you expect. In the mutable-key demonstration, change a field of a key object and watch the lookup miss.
- **Keyboard:** The key field inserts on Enter and looks up on Shift + Enter; Up and Down move between buckets and Enter opens one; the size slider and strategy control are native; in prediction, digits type the bucket index.
- **State:** `{ m: number, strategy: 'chaining' | 'linear' | 'quadratic', entries: { key: string; value: string; bucket: number }[], tombstones: number[], probes: number[] }`.
- **Answers:** `numeric` (bucket index, probe count, load factor), `choice`, `set` (keys in a bucket), `state`.
- **Config:** `{ hash: 'toy' | 'python-int' | 'python-str'; m: number; strategy?: string; keys?: string[]; resizeAt?: number; task: 'insert' | 'lookup' | 'predict-bucket' | 'resize' | 'mutable-key' | 'explore'; language?: 'python' | 'cpp' }`.
- **Visual:** buckets numbered on the left; chains as rows of key chips; a load-factor gauge ($\alpha = n/m$) with the resize threshold marked; probes numbered in order on the buckets they touched.
- **Motion:** an inserted key travels to its bucket over 240 ms; a resize rehashes every key in a 600 ms sequence (each key to its new bucket); both are consequences of the learner's action.
- **Reduced motion:** keys appear in place; the resize shows before and after.
- **Accessibility:** buckets form a list ("bucket 3: AAPL, MSFT"); every insertion is announced with its hash and index.
- **Tutor:** describe: "Hash table m = 8, chaining, 6 keys, load factor 0.75. Bucket 3 holds 3 keys." Ids: `bucket:<i>`, `key:<k>`, `probe:<n>`.
- **Performance:** up to 64 buckets and 200 keys in SVG.
- **Artifact / web:** identical.
- **Generator:** yes. Seeded key sets with chosen collision patterns; predict-bucket and probe-count items; resize thresholds.

---

## 5. Composites: NumPy, pandas and plotting (1.1.2 to 1.1.4)

All of these run on the `nd-core` and `frame-core` JavaScript cores for interaction (decision 6), so they behave the same on both targets. Code drills that use the real libraries go through `code-cell`.

### 5.1 `ndarray-lab`: Array lab

**Composite · P0 · W-A2.** NumPy arrays as cells you can see: shape and axes, slicing, views against copies, strides and memory order, boolean masks and fancy indexing, dtypes, reductions and stacking.

- **Serves:** 1.1.2 L1 to L6, L8; 1.1.3 L23 (dtypes and memory); 1.4 (array thinking before matrices, for calc-linalg).
- **Uses:** `cell-grid` (the array, with layers for 3D), `array-strip` (bytes mode: the flat buffer with offsets), `drag-point` (slice handles), `slider` (step), `token-tray` (axis chips and condition chips), `live-formula` (shape, strides, offset), `code-surface` (the expression field).
- **Modes:** `axes` (tap an axis to reduce along it, with or without `keepdims`), `slice` (start, stop and step handles per axis; negative indices), `memory` (the buffer under the array; strides; a slice as a view sharing the buffer; transpose swapping strides; `reshape` refilling in C or Fortran order; `np.shares_memory`), `mask` (build a boolean grid from a condition; `np.where`; fancy indexing returns a copy), `dtype` (int64 wrap-around, float64, bool, upcasting in mixed operations), `reduce` (`sum`, `mean`, `std` with `ddof`, `argmax`, `cumsum`), `stack` (`concatenate`, `stack`, `vstack` along chosen axes).
- **Interactions.** Tap an axis arrow to reduce along it; drag slice rectangles and handles, and the expression writes itself; type an expression and its selection overlays the grid; tap a condition chip to make a mask; assign through a view or a mask and watch which grids change; tap a cell to see its buffer offset, $\sum_k i_k s_k$ in bytes; drag shape factors to reshape (12 into $3 \times 4$, $4 \times 3$, $2 \times 2 \times 3$).
- **Keyboard:** `cell-grid` keys (arrows; Shift + arrows extend the selection rectangle); A then a digit reduces along that axis; the expression field evaluates on Enter; slice handles are sliders; Space toggles a condition chip.
- **State:** `{ shape: number[], dtype: string, values: unknown, expr: string, rect?: number[], axis?: number, keepdims: boolean, mask?: boolean[], order: 'C' | 'F', views: { id: string; base: string; expr: string }[] }`.
- **Answers:** `text` (an expression, graded by `selectionEquals`; a shape tuple, normalised), `set` (cells), `choice` (view or copy; legal or error), `numeric` (an offset or a reduced value).
- **Config:**
```ts
interface NdarrayLabConfig {
  mode: 'axes' | 'slice' | 'memory' | 'mask' | 'dtype' | 'reduce' | 'stack';
  arrays: { id: string; shape: number[]; dtype: 'int64' | 'float64' | 'bool' | 'int8' | 'float32'; values?: unknown; fill?: 'arange' | 'random' }[];
  expr?: string;                                   // given expression to visualise
  target?: { cells?: string[]; shape?: number[] }; // for "write the expression" tasks
  editable?: ('expr' | 'handles' | 'shape' | 'order')[];
  showBuffer?: boolean; showStrides?: boolean;
}
```
- **Visual:** axis arrows labelled "axis 0" (down), "axis 1" (across), "axis 2" (into the layers); a shape badge `(3, 4)`; the buffer strip below with stride brackets; the learner's selection in `--manip-wash`; the expression's selection as a 2px `--s2` outline; a copy drawn as a separate grid with its own buffer, a view drawn sharing its parent's buffer.
- **Motion:** a reduction collapses the chosen axis (cells slide together and combine) over 400 ms as a consequence of the tap; reshape refills cells in buffer order over 400 ms.
- **Reduced motion:** before and after with Play.
- **Accessibility:** the grid's cell reads include indices and buffer offset; the expression and its result shape are announced.
- **Tutor:** describe: "int64 array, shape (3, 4). Selection a[1:, ::2]: 4 cells, a view of a (shares memory)." Ids: `cell:<r>,<c>`, `axis:<k>`, `buf:<i>`, `view:<id>`.
- **Performance:** SVG up to 2,500 cells; 3D shown for up to $4 \times 6 \times 6$.
- **Artifact / web:** identical.
- **Generator:** yes. Shapes and slice targets; reduction shapes; view or copy classification; dtype outcomes.

### 5.2 `broadcast-lab`: Broadcasting lab

**Composite · P0 · W-A2.** Broadcasting as a picture: shapes aligned from the right, size-1 dimensions stretched, the result shape, and the error when two dimensions disagree. Also matrix products and `keepdims`.

- **Serves:** 1.1.2 L7, L10; 1.4 and 1.6 (centring data matrices, covariance) for other clusters.
- **Uses:** `token-tray` (dimension tiles and `None` tokens), `cell-grid` (small example arrays), `live-formula` (result shape), `code-surface` with slots (fix mode), `choice`.
- **Modes:** `shapes`, `stretch`, `outer` (a column times a row becomes a table), `fix` (insert `[:, None]` or reshape so it works), `matmul` (inner dimensions must match; batch dimensions broadcast; `@` against `*`), `keepdims` (subtract column means works; subtract row means needs `keepdims=True` or `[:, None]`).
- **Interactions.** Drag `None` tokens into a shape to add an axis; predict the result shape; tap Broadcast and the size-1 dimensions stretch; in an error case, the clashing pair is highlighted.
- **Keyboard:** Tiles and `None` tokens follow `token-tray` keys; B runs Broadcast; the shape field accepts typing and Enter checks.
- **State:** `{ shapes: number[][], inserted: Record<string, number[]>, prediction?: string }`.
- **Answers:** `text` (a shape), `choice` (works or raises), `code` (the fixed expression), `mapping`.
- **Config:** `{ mode: 'shapes' | 'stretch' | 'outer' | 'fix' | 'matmul' | 'keepdims'; operands: { name: string; shape: number[]; values?: number[] }[]; op: '+' | '-' | '*' | '/' | '@'; task: 'predict-shape' | 'works' | 'fix' | 'explore' }`.
- **Visual:** dimension tiles right-aligned in columns, matched pairs joined by a plain ink link and clashing pairs by a cross glyph plus the word "mismatch"; stretched copies drawn as ghosts at 40%.
- **Motion:** stretching copies a size-1 row or column out across its new length over 400 ms after Broadcast.
- **Reduced motion:** before and after.
- **Accessibility:** alignment read column by column ("from the right: 4 and 4 match; 3 and 1 stretch to 3").
- **Tutor:** describe: "(3, 4) + (3,): aligned from the right, 4 against 3 mismatch." Ids: `dim:<operand>.<k>`, `result`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Random shape pairs at difficulty 1 to 4, with a set share of incompatible pairs and `keepdims` traps.

### 5.3 `dataframe-lab`: DataFrame lab

**Composite · P0 · W-A2.** pandas DataFrames: anatomy, selection with `[]`, `loc` and `iloc`, boolean filters, index alignment, missing data, chained assignment under copy-on-write, sorting and ranking, dtypes and memory, MultiIndex.

- **Serves:** 1.1.3 L1 to L7, L9, L23; 1.6 and 2.1 datasets for other clusters.
- **Uses:** `value-table` frame mode, `code-surface` (expression field), `token-tray` (condition chips with `&`, `|`, `~` and parentheses), the `frame-core` service.
- **Modes:** `anatomy`, `select`, `filter`, `align`, `missing`, `copy`, `sort`, `dtype`, `multiindex`.
- **Interactions.**
  - `select`: drag a rectangle and both `loc` and `iloc` expressions appear, showing that label slices include their end and position slices do not; or type an expression and its selection overlays the frame.
  - `filter`: build a condition from chips; the mask column appears beside the frame; the precedence trap (`df.a > 0 & df.b < 5`) shows its error.
  - `align`: two Series side by side; the result builds label by label, with NaN where a label is missing on one side.
  - `missing`: `dropna`, `fillna`, `ffill` and `bfill` buttons; values that `bfill` took from a later date are marked "from the future".
  - `copy`: run a chained assignment and see whether the original changed under the pinned pandas version.
- **Keyboard:** Grid keys on the frame; Shift + arrows extend a selection rectangle and the expressions update; the expression field evaluates on Enter; condition chips follow `token-tray` keys; operation buttons are in the tab order.
- **State:** `{ frame: string, expr: string, learnerSel?: Selection, ops: string[] }`.
- **Answers:** `text` (an expression, graded by `selectionEquals`), `set` (cells or rows), `numeric` (row counts), `choice`.
- **Config:** `{ mode: string; frames: Record<string, FrameSpec>; expr?: string; target?: Selection; allowed?: ('loc' | 'iloc' | '[]' | 'query')[]; pandasVersion: string }`.
- **Visual:** frame mode with learner and derived overlays (section 3.8); the mask column in `--s6` hatch for `True`; "from the future" values labelled in text with a clock glyph.
- **Motion:** alignment builds the result row by row over 300 ms as a consequence of Run; otherwise none.
- **Reduced motion:** the result appears at once.
- **Accessibility:** frame-mode table semantics; selections announced ("loc selects 3 rows, 1 column").
- **Tutor:** describe: "Frame prices 6 × 3 (date index). Learner selection rows 2024-01-03 to 2024-01-05, column close. Expression df.iloc[2:4, 0] selects 2 rows." Ids: `cell:<row>,<col>`, `row:<label>`, `col:<name>`.
- **Performance:** `frame-core` operations under 2 ms for frames up to 1,000 rows.
- **Artifact / web:** identical.
- **Generator:** yes. Seeded frames (prices, sectors, trades) with selection and filter targets; alignment pairs; missing-data patterns.

### 5.4 `groupby-lab`: Group-by lab

**Composite · P0 · W-A2 (pandas), W-A3 (SQL).** Split, apply, combine, shown as motion: rows sorted into groups, each group reduced, the results gathered. Covers `agg` against `transform` against `filter`, several keys, NaN keys, SQL `GROUP BY` with `HAVING` against `WHERE`, and window functions.

- **Serves:** 1.1.3 L10; 1.2.3 L6, L10; 2.3 alpha research (per-date cross-sections) for the finance cluster.
- **Uses:** `value-table` frame mode (source, groups, result), `token-tray` (key and aggregation chips), `stepper`, `code-surface`.
- **Modes:** `agg`, `transform`, `filter`, `multi-key`, `sql` (`WHERE` before grouping, `HAVING` after), `window` (`OVER (PARTITION BY ... ORDER BY ...)`, `LAG`, `ROW_NUMBER`, `ROWS BETWEEN 4 PRECEDING AND CURRENT ROW`; pandas `groupby().shift()` and `groupby().rolling()`).
- **Interactions.** Choose keys and aggregations by chip; Step through split, apply and combine; predict by dragging each row into its group, or by filling the result table; in window mode, tap a row to see its partition and frame.
- **The leak trap.** Daily returns computed with `shift` over a stacked multi-ticker table without grouping use ticker A's last price for ticker B's first return. Show-why `cross-boundary` highlights that row and the price it borrowed.
- **Keyboard:** Chips follow `token-tray` keys; N steps through split, apply and combine; to predict, focus a row, press Enter, choose its group with Up and Down, and press Enter; in window mode, Up and Down move between rows and the partition follows.
- **State:** `{ keys: string[], aggs: Record<string, string>, step: 'split' | 'apply' | 'combine' | 'done', mapping?: Record<string, string>, prediction?: unknown }`.
- **Answers:** `mapping` (row to group), `table`, `numeric`, `code` (SQL or pandas).
- **Config:** `{ mode: string; frame: FrameSpec; keys?: string[]; aggs?: Record<string, string>; dialect: 'pandas' | 'sql'; task: 'predict-groups' | 'predict-result' | 'write' | 'explore'; dropna?: boolean }`.
- **Visual:** group panels stacked, each headed by its key; rows carry their key as a chip; results in a final frame; window frames drawn as a dashed `--s4` bracket across the partition.
- **Motion:** rows slide into their group panels over 400 ms (split); each panel's aggregate fades in (apply); results gather into the output (combine). All follow Step or Play.
- **Reduced motion:** each stage shown as a static state with Play.
- **Accessibility:** groups read as lists ("group Tech: 3 rows, sum 412"); windows read per row ("row 5: partition AAPL, frame rows 1 to 5").
- **Tutor:** describe: "Group by sector, sum of value. Stage apply. 3 groups: Energy 2 rows, Tech 3 rows, Banks 2 rows." Ids: `row:<i>`, `group:<key>`, `agg:<key>.<col>`.
- **Performance:** up to 60 rows animated; larger frames skip the animation and show the result with group counts.
- **Artifact / web:** pandas mode identical; SQL mode needs SQLite for free queries (section 2.10).
- **Generator:** yes. Seeded trade and price tables; aggregation choices; window items; leak-trap variants.

### 5.5 `join-lab`: Join lab

**Composite · P0 · W-A2 (pandas), W-A3 (SQL).** Joins as matched rows, not Venn diagrams: lines join rows with equal keys, duplicate keys fan out and multiply rows, unmatched rows are kept or dropped by the join type, and missing values pad the gaps. Also anti-joins, semi-joins, `concat`, and pandas `validate` and `indicator`.

- **Serves:** 1.1.3 L11, L12; 1.2.3 L7, L8; 2.3 projects.
- **Uses:** `value-table` frame mode (left, right, result), `marks` segments on an overlay anchored to the tables' row positions (the match lines), `token-tray` (join type), `code-surface`.
- **Modes:** `join` (`inner`, `left`, `right`, `outer`, `cross`), `anti`, `semi`, `concat` (axis 0 and 1; column alignment), `validate` (`one_to_one`, `one_to_many`, `many_to_one`).
- **Interactions.** Drag from a left row to a right row to predict a match line; choose the join type; predict the result's row count; tap a result row to light its sources.
- **The NULL trap.** In SQL, a `NULL` key never matches; pandas `merge` matches NaN keys to each other [sourced: pandas documentation, recalled; CI confirms on the pinned version]. The widget shows both.
- **Keyboard:** To predict a match, focus a left row, press Enter, move through the right rows with Up and Down (each announced) and press Enter; Delete removes a predicted line; the join type is a native radio group; the count field takes digits.
- **State:** `{ how: string, predictedMatches: [number, number][], predictedCount?: number }`.
- **Answers:** `numeric` (row count: $\sum_k L_k R_k$ for inner joins over keys $k$), `set` (result rows), `mapping` (match lines), `resultset`, `code`.
- **Config:** `{ mode: string; left: FrameSpec; right: FrameSpec; on: string | string[]; how?: string; dialect: 'pandas' | 'sql'; task: 'predict-count' | 'draw-matches' | 'predict-result' | 'write' | 'explore' }`.
- **Visual:** the two tables side by side (stacked on phones, with lines drawn vertically); match lines 1.5px ink, learner lines `--manip`; unmatched rows labelled "no match"; padded cells as muted `NaN` or `NULL`.
- **Motion:** result rows assemble one by one over 300 ms after Run; drawing lines is direct.
- **Reduced motion:** the result appears at once.
- **Accessibility:** matches listed as text ("left row 2 (AAPL) matches right rows 1 and 4").
- **Tutor:** describe: "Left 5 rows, right 4 rows, inner join on ticker. Duplicate key MSFT on the right (2 rows). Learner predicted 5 rows." Ids: `lrow:<i>`, `rrow:<i>`, `res:<i>`, `match:<i>-<j>`.
- **Performance:** up to 40 rows per side with lines; larger tables hide lines and show counts by key.
- **Artifact / web:** as `groupby-lab`.
- **Generator:** yes. Seeded tables with duplicate keys, missing keys and null keys.

### 5.6 `reshape-lab`: Reshape lab

**Composite · P0 · W-A2.** Long and wide data: `pivot`, `pivot_table` (with an aggregation when keys repeat), `melt`, `stack` and `unstack` with MultiIndex levels, `get_dummies` and `crosstab`. Each source cell can be followed to its destination.

- **Serves:** 1.1.3 L13, L14; 2.3 projects (a returns matrix of dates by tickers).
- **Uses:** `value-table` frame mode (source and target), `token-tray` (slots for `index`, `columns`, `values`, `id_vars`, `value_vars`), `marks` (cell trajectories on an overlay), `stepper`.
- **Interactions.** Drag column names into slots, as in a spreadsheet pivot panel; predict the output shape; tap a source cell to see where it lands; a `pivot` with repeated keys raises its real error and offers `pivot_table`.
- **Keyboard:** Column chips follow `token-tray` keys into the slots; Enter on a source cell follows it to its destination; the shape field accepts typing.
- **State:** `{ op: string, slots: Record<string, string[]>, prediction?: string }`.
- **Answers:** `mapping` (slots), `text` (shape), `code`, `choice`.
- **Config:** `{ op: 'pivot' | 'pivot_table' | 'melt' | 'stack' | 'unstack' | 'get_dummies' | 'crosstab'; frame: FrameSpec; task: 'fill-slots' | 'predict-shape' | 'follow-cell' | 'write' | 'explore'; target?: FrameSpec }`.
- **Visual:** the source on the left, the target on the right; a followed cell carries an `--s2` ring to its destination.
- **Motion:** cells travel along curved paths over 600 ms when the reshape runs.
- **Reduced motion:** before and after, with the followed cell ringed in both.
- **Accessibility:** "Cell (2024-01-02, AAPL, close) moves to row 2024-01-02, column AAPL."
- **Tutor:** describe: "melt with id_vars [date], value_vars [AAPL, MSFT]; result 10 rows × 3 columns." Ids: `slot:<name>`, `src:<r>,<c>`, `dst:<r>,<c>`.
- **Performance:** animation for up to 60 cells; otherwise a static result.
- **Artifact / web:** identical.
- **Generator:** yes. Seeded long tables of date, ticker, field and value, with shape targets.

### 5.7 `time-series-lab`: Time series lab

**Composite · P0 · W-A2.** pandas time series on a real timeline: dates and frequencies, `shift` and returns, resampling and its labelling rules, rolling and exponentially weighted windows, time zones and daylight saving, and aligning two calendars.

- **Serves:** 1.1.3 L6, L15 to L20; 2.2 time series and 2.3 backtests for other clusters (look-ahead is the commonest backtest bug).
- **Uses:** `plot-2d` (a time axis), `marks` (lines, bars, a `band` for windows, candlesticks requested from the marks owner), `value-table` frame mode, `region-select` (window bracket), `slider` (shift, window length, span), the `frame-core` and `price-series` services.
- **Modes:** `dates` (`date_range`, frequency aliases, business days, a missing holiday), `shift` (move a column by $k$ rows; returns built live; `shift(-1)` borrows tomorrow), `resample` (bins drawn on the axis; `label` and `closed`; OHLC), `rolling` (drag the window; `min_periods`; `center=True` reaches into the future; `ewm` weights drawn beside `rolling` weights), `tz` (localise and convert; the two daylight-saving changes each year), `align` (two calendars, an outer join, then `ffill`).
- **Interactions.** Slide the shift from $-2$ to $+2$ and watch the column move against the dates; tap any return that used a future price; drag resample bin edges and toggle `label` and `closed`; drag the window bracket; convert timestamps by choosing zones.
- **Keyboard:** The shift, window and span sliders take arrow keys; the window bracket is a pair of sliders; table rows use grid keys and Space flags a row; zone and rule pickers are native selects.
- **State:** `{ mode: string, shift: number, rule?: string, label?: 'left' | 'right', closed?: 'left' | 'right', window?: number, center: boolean, minPeriods?: number, span?: number, tz?: string, flagged: string[] }`.
- **Answers:** `set` (rows), `numeric`, `mapping` (day to bin), `text` (a timestamp or rule).
- **Config:** `{ mode: string; series: { generator: 'price-series'; seed: number; days: number } | FrameSpec; task: string; pandasVersion: string }`. Frequency aliases follow the pinned pandas version (pandas 2.2 renamed month-end `M` to `ME`) [sourced, recalled; CI checks the alias table against the pin].
- **Visual:** the timeline with weekends and holidays as gaps marked by small ticks; windows as a dashed `--s4` band; future-leaking cells labelled "uses the future" with a clock glyph; weights as bars in s6.
- **Motion:** the shifted column slides over 200 ms per step; dragging the window is direct.
- **Reduced motion:** shifts cut.
- **Accessibility:** a table view with date, price, shifted price, return; window positions announced as date ranges.
- **Tutor:** describe: "Daily prices 2024-01-02 to 2024-03-28 (61 trading days). shift(-1) applied: 61 returns use the next day's price." Ids: `row:<date>`, `window`, `bin:<n>`.
- **Performance:** up to 2,000 points drawn in SVG; more on Canvas 2D.
- **Artifact / web:** identical.
- **Generator:** yes. `price-series` seeds; holiday calendars; window, resample and shift items.

### 5.8 `csv-inspector`: CSV inspector

**Composite · P0 · W-A1 (csv module), W-A2 (pandas).** The raw text of a CSV beside the table it becomes, with every option that changes the parse: quoted commas, headers, index columns, dates, thousands and decimal separators, missing-value strings, skipped rows, encodings.

- **Serves:** 1.1.1 L23; 1.1.3 L8; the 1.1 exit project.
- **Uses:** `code-surface` (raw text with delimiters, quotes and line ends as visible glyphs), `value-table` frame mode (the parse), `token-tray` or toggles (options), `code-blanks` (write the `read_csv` call).
- **Parser:** a JavaScript RFC 4180 parser with the pandas option subset (`sep`, `quotechar`, `header`, `index_col`, `usecols`, `parse_dates` for ISO and common day-first and month-first forms, `thousands`, `decimal`, `na_values`, `skiprows`, `dtype`). CI compares it with pandas on a corpus that includes every `price-series` messiness option.
- **Interactions.** Toggle options and the table reparses; tap a raw character to light its cell, and the reverse; tap cells that parsed wrongly; fill in the `read_csv` call.
- **Keyboard:** Options are native toggles and selects; in the raw text, arrows move by character and Enter lights that character's cell; in the table, Space marks a broken cell.
- **State:** `{ options: Record<string, unknown>, selected: string[] }`.
- **Answers:** `set` (broken cells), `code` (the call), `mapping`, `choice`.
- **Config:** `{ mode: 'csv-module' | 'pandas'; text: string | { generator: 'price-series'; seed: number; messiness: string[] }; options?: Record<string, unknown>; task: 'find-broken' | 'fix-options' | 'write-call' | 'explore' }`.
- **Visual:** delimiters as small `--s4` glyphs, quotes as `--s5`, line ends as a return glyph; wrongly typed cells marked with a cross icon and the word "text" or "NaN"; dtypes under each header.
- **Motion:** none.
- **Reduced motion:** nothing to change.
- **Accessibility:** the raw text is real text; each cell names its source line and column.
- **Tutor:** describe: "CSV 8 lines; options sep=',' header=0; column volume parsed as object (thousands separators)." Ids: `raw:<line>:<col>`, `cell:<r>,<c>`, `opt:<name>`.
- **Performance:** files up to 2,000 lines.
- **Artifact / web:** identical.
- **Generator:** yes. `price-series` CSVs with seeded messiness.

### 5.9 `drawdown-lab`: Returns, volatility and drawdown

**Composite · P0 · W-A2. Shared with the finance cluster (1.7, 2.3).** The 1.1 exit maths on a price path: simple and log returns, annualised volatility, the running maximum, the drawdown series and the maximum drawdown with its dates.

- **Serves:** 1.1.3 L16, L20, L21; the 1.1 exit; 1.7 and 2.3 (Sharpe, Calmar and drawdown reporting).
- **Uses:** `plot-2d` (two linked panels: price above on a linear or log scale, drawdown below), `marks` (the price path, the running maximum as a dashed line, the underwater region), `drag-point` (peak and trough handles constrained to the price path, the trough after the peak), `region-select` (a period bracket), `live-formula`, `value-table`.
- **Modes:** `returns` (simple against log; log returns add up to the log of the total return), `vol` (rolling standard deviation; annualising by $\sqrt{252}$; `ddof=1`), `drawdown`, `compare` (two paths with the same return and different drawdowns; Calmar ratio in P1, with the finance cluster).
- **Formulas shown live:** $r_t = P_t / P_{t-1} - 1$; $\ell_t = \ln(P_t / P_{t-1})$; $\sigma_{\text{ann}} = \sigma_{\text{daily}} \sqrt{252}$; $D_t = P_t / \max_{s \le t} P_s - 1$; $\text{MDD} = \min_t D_t$. The $\sqrt{252}$ rule assumes independent daily returns and 252 trading days a year; the screen says so.
- **Interactions.** Drag the peak and trough handles to the largest fall, with a live readout of $P_{\text{trough}} / P_{\text{peak}} - 1$; drag the period bracket for volatility; toggle the log scale.
- **Keyboard:** The peak and trough handles are sliders over trading days (Left and Right one day, Page Up and Page Down 20 days, Home and End the ends); the bracket is a pair of sliders; L toggles the log scale.
- **State:** `{ peak: number, trough: number, bracket?: [number, number], logScale: boolean, mode: string }`.
- **Answers:** `point` (peak and trough indices; metric `x`, tolerance 0 days), `numeric` (maximum drawdown, volatility, total return; absolute tolerance $10^{-4}$), `choice`.
- **Config:** `{ mode: string; series: { generator: 'price-series'; seed: number; days: number; drawdowns?: number } | number[]; dates?: string[]; task: 'find-mdd' | 'compute-vol' | 'compare' | 'explore' }`.
- **Visual:** price in ink; running maximum as a dashed `--s6` line; the underwater area in the diverging ramp's negative colour at 25% with its depth labelled; handles in `--manip`; graded handles recolour only themselves.
- **Show-why:** `true-mdd` slides ghost handles to the real peak and trough over 600 ms and shades the gap between the learner's fall and the true one.
- **Motion:** handles are direct; `spring-snap` to the nearest trading day on release.
- **Reduced motion:** ghosts appear in place.
- **Accessibility:** handles are sliders over trading days ("peak 14 March 2024, 131.20"); the table view lists date, price, running maximum and drawdown.
- **Tutor:** describe: "Price path 252 days. Learner peak 2024-03-14 (131.2), trough 2024-05-02 (112.9): fall -13.9%." Ids: `handle:peak`, `handle:trough`, `panel:price`, `panel:dd`.
- **Performance:** 2,520 points (ten years) in SVG paths; handle drags under 1 ms.
- **Artifact / web:** identical.
- **Generator:** yes. `price-series` seeds with controlled drawdown counts and depths.

### 5.10 `plot-workbench`: Plot workbench

**Composite · P0 · W-A2.** matplotlib's model (Figure, Axes, Artists) and plotting judgement. Code lines and figure elements are linked both ways; plots are built from code tokens; misleading charts are repaired with toggles.

- **Serves:** 1.1.4 L1 to L6; the 1.1 exit; plots in every later cluster's code drills.
- **Rendering:** matplotlib's own SVG. At build time CI runs the authored code with a recorder that tags each artist with the line that created it (`set_gid`), and saves SVG with text kept as text (`svg.fonttype = 'none'`). The widget shows that SVG and addresses its elements by id. Learner-built plots render live through Pyodide on the web; in the Artifact, CI precomputes every token combination up to 64, and larger spaces hand off.
- **Uses:** `code-surface` (read-addressable, linked to elements), `token-tray` and `code-blanks` (build), `choice` and toggles (fix), `value-table` (the data).
- **Modes:** `anatomy`, `build`, `fix` (log scale, y-axis from zero for bar charts, shared x axes, labels, removing a second y axis, aspect), `choose` (the chart type for a question and a dataset).
- **Interactions.** Tap a code line and its element lights; tap an element and its line lights; drag tokens or fill blanks, then Render; flip toggles to repair a chart.
- **Keyboard:** Tab moves through code lines, then through figure elements (each a button); Enter on either lights its partner; toggles are native and token slots follow `token-tray` keys; R renders.
- **State:** `{ mode: string, selected?: string, tokens?: string[], toggles?: Record<string, boolean | string> }`.
- **Answers:** `mapping` (line to element), `state` (graded by `figureFixed`), `code` (figure tests), `choice`.
- **Config:** `{ mode: string; code: string; svg?: string; artists?: { gid: string; line: number; kind: string }[]; data?: FrameSpec; toggles?: { id: string; label: string; options: string[] }[]; fixTarget?: Record<string, string> }`.
- **Visual:** the SVG inside the lesson frame on `--bg-surface`; a highlighted artist gets the pear focus wash and ink ring; code lines as in `code-surface`.
- **Motion:** none beyond highlights.
- **Reduced motion:** nothing to change.
- **Accessibility:** alt text from the artist list ("Axes 1: line 'close'; x label 'Date'; y label 'Price ($)'; log scale"); each artist is listed as a button linked to its line.
- **Tutor:** describe: "Figure with 2 axes; axes 1 has 1 line, no y label; axes 2 is a histogram with 40 bins." Ids: `artist:<gid>`, `line:<n>`.
- **Performance:** SVGs of 50 to 200 KB [estimate]; one figure per screen.
- **Artifact / web:** as in Rendering.
- **Generator:** yes, for `fix`: seeded data with seeded defects (truncated axis, misused dual axis, linear scale across decades, missing labels, too many series).

### 5.11 `bench-lab`: Benchmark lab

**Composite · P0 race mode · W-A2; rigorous and profile modes P1 · W-C.** Measuring speed honestly: races between implementations, then methodology (warm-up, repeats, spread, optimisation levels, dead-code elimination), the Python against C++ comparison for the 1.9 exit, and profiles.

- **Serves:** 1.1.2 L1; 1.1.3 L5, L23; 1.8.1 L7; 1.9.3 L5, L6; the 1.9 exit; 2.4.1 L3.
- **Uses:** `plot-2d` (log-log time against $n$; repeated timings as a dot strip), `marks` (scatter, bars, and an `icicle` mark requested from the marks owner for flame charts), `value-table`, `code-surface`, a paste field.
- **Modes.**
  - `race`: two or three implementations timed at growing $n$ (best of $k$ runs), with the speed-up. Live on the web; in the Artifact, live where MicroPython can run both sides, otherwise recorded timings labelled with the device they came from.
  - `rigorous` (P1): the distribution of 30 repeats; minimum, median and mean; coefficient of variation; the first-run warm-up; timer resolution; `-O0`, `-O2` and `-O3` results recorded on a reference machine; the benchmark the compiler deleted (an impossible 0 ns); the learner's pasted `hyperfine` or `timeit` output parsed into mean and spread, and the speed-up as a ratio with an interval from the spreads.
  - `profile` (P1): a `cProfile` table and an icicle chart, recorded for authored code or live on the web; sort by own time against cumulative time; tap the hot function.
- **Interactions.** Choose implementations and sizes, Run; drag the size slider; paste local output; tap a bar or a frame.
- **Keyboard:** Implementation toggles, the size slider and Run are native controls; the paste field is a textarea; in profile mode, Up and Down move through frames and Space marks the hot one.
- **State:** `{ mode: string, sizes: number[], results: Record<string, number[]>, pasted?: string }`.
- **Answers:** `numeric` (a speed-up within tolerance), `choice`, `set` (the hot function).
- **Config:** `{ mode: 'race' | 'rigorous' | 'profile'; impls: { id: string; label: string; code: string; language: 'python' | 'cpp' }[]; sizes?: number[]; recorded?: { device: string; times: Record<string, number[]> }; profile?: unknown; paste?: { format: 'hyperfine' | 'timeit' | 'pytest-benchmark' } }`.
- **Visual:** implementations take series slots s2, s3 and s6 with direct labels; the speed-up in the stat token; recorded timings carry a caption naming the device.
- **Motion:** points appear as timings arrive; that is data, not decoration.
- **Reduced motion:** results appear together when the run ends.
- **Accessibility:** table view of size, implementation and time; the speed-up announced.
- **Tutor:** describe: "Race: loop vs vectorised at n = 10^6: 410 ms vs 3.1 ms (132×), web Pyodide." Ids: `impl:<id>`, `point:<impl>.<n>`, `frame:<fn>`.
- **Performance:** timing runs in the Python worker; the page only plots.
- **Artifact / web:** as in Modes.
- **Generator:** yes, for speed-up arithmetic and reading-the-distribution items; races and profiles are authored.

---

## 6. Composites: tools (1.2)

### 6.1 `git-graph`: Git graph

**Composite · P0 · W-A3.** Git as a picture you can operate: the commit graph with branch labels and HEAD, the three trees (working directory, index, HEAD), a remote, and the goal graph of a puzzle drawn as a ghost. Commands are typed in a terminal or chosen with buttons. The puzzle format follows Learn Git Branching (Peter Cottle) [sourced, recalled], rebuilt on a real object model.

- **Serves:** 1.2.2 L1 to L6 and L8 to L14; 1.2.4 L12 (checks); the 1.2 exit rehearsal; every later project's Git habits.
- **Uses:** `node-link` (`git` layout), `diff-view` (commit diffs, `add -p` hunks), `text-terminal` (commands), `token-tray` (interactive rebase to-do list), `value-table` (log view), the `git-model` and `vfs` services.
- **`git-model`** [our choice]:
  - **Objects:** blobs, trees and commits, hashed with SHA-1 over Git's own object format, so identical content, author and time give real Git's hashes [inferred from the format]. A deterministic clock starts at a fixed epoch and adds 60 s per commit, so hashes are the same on every device. Hashes display as 7 characters.
  - **Refs:** branches, tags, symbolic or detached HEAD, remote-tracking refs, a reflog per ref, and the stash as commits under `refs/stash`.
  - **Index:** path to blob, with stage numbers 1 to 3 during conflicts.
  - **Commands:** `init`, `status`, `add` (with `-p` through `diff-view` hunks), `restore` (with `--staged`), `commit` (with `-m`, `--amend`), `log` (with `--oneline`, `--graph`, `--all`), `show`, `diff` (working, `--staged`, `A..B`), `branch` (with `-d`, `-f`), `switch` (with `-c`), `checkout` (including detached HEAD), `merge` (fast-forward, `--no-ff`, three-way with line-level conflicts by diff3), `rebase` (with `-i`: pick, reword, squash, fixup, drop, reorder; `--continue`, `--abort`), `cherry-pick`, `revert`, `reset` (`--soft`, `--mixed`, `--hard`), `stash` (push, pop, list), `tag`, `reflog`, `bisect` (start, good, bad, reset), `blame`, `clone`, `remote`, `fetch`, `pull` (merge or `--rebase`), `push` (rejects non-fast-forward; `--force-with-lease`).
  - **Not modelled:** submodules, worktrees, hooks, LFS, packfiles, and merge bases in criss-cross histories (content avoids them).
- **Views:** the graph; the three-trees panel (Working, Staging, HEAD columns listing files with state badges: untracked, modified, staged, deleted, conflicted); the remote panel (origin's own graph and refs); the terminal; the goal ghost.
- **Interactions.**
  - Type commands, or use buttons (Commit, Branch, Switch, Merge, Rebase, Reset) and tap target commits.
  - Drag a branch label to another commit (the same as `git branch -f` or `git reset`, named in the log).
  - Drag a file between the three-tree columns (the same as `add` or `restore`).
  - Tap a commit to see its diff with its parent; tap a file in an old commit to see it still exists in history.
  - Keyboard: the terminal, plus arrow navigation between commits in the graph and Enter to inspect.
- **Show-why keys:** `commit` (a node appears, the branch label moves), `reset` (the pointer moves back; then the index and the working columns update according to the mode, one after another), `merge` (a two-parent node), `rebase` (commits are copied with new hashes; the originals grey out as unreachable but stay in the reflog), `push-rejected` (the remote's extra commit lights), `history-is-permanent` (the deleted key file appears when an older commit is opened).
- **State:** the `git-model` repository (objects, refs, index, reflog), the `vfs` working tree, the remote repository, `{ bisect?: { good: string[]; bad: string[] } }`. Serialised flat, under 128 KB.
- **Answers:** `state` (predicates `graphMatches`, `headAt`, `fileContent`, `branchContains`, `remoteHas`), `text` (a command, judged by effect), `numeric` (bisect steps), `ordering` (a rebase to-do list).
- **Config:**
```ts
interface GitGraphConfig {
  repo: { commits: { id: string; parents: string[]; message: string; files: Record<string, string> }[];
          branches: Record<string, string>; head: string | { detached: string };
          index?: Record<string, string>; working?: Record<string, string | null> };
  remote?: { name: string; repo: GitGraphConfig['repo'] };
  goal?: { graph: GitGraphConfig['repo']; ignoreHashes: boolean; par?: number };   // par: fewest commands, computed in CI
  panels?: ('graph' | 'trees' | 'remote' | 'terminal' | 'log')[];
  input: 'terminal' | 'buttons' | 'both';
  allowed?: string[];                              // commands enabled on this screen
  checks?: Record<string, 'pass' | 'fail' | 'running'>;   // CI status per pushed commit
  bisect?: { badCommit: string };
}
```
- **Visual:** commits as 28px circles with short hashes; lanes per branch in series slots s2 to s6 (labelled, never colour alone); branch labels as pills, HEAD as an ink tag with an arrow; unreachable commits at 25% opacity; the goal as a dashed ghost; check badges on commits use icons and words ("tests passed", "tests failed"), not the grading colours.
- **Motion:** a new commit appears over 150 ms; labels slide to their new commit over 300 ms; rebased copies travel from the old base to the new over 500 ms. All are consequences of a command.
- **Reduced motion:** cuts, with the moved labels marked "moved" for one step.
- **Accessibility:** a log table (hash, message, parents, refs); every command's effect announced ("main moved from c4 to c5; working tree unchanged").
- **Tutor:** describe: "Repo: 7 commits; main at c4, feature at c6 (HEAD). Staged: report.py. Modified: analysis.py. Goal: feature rebased on main, par 2." Ids: `commit:<hash>`, `ref:<name>`, `file:<tree>:<path>`, `cmd`.
- **Performance:** up to 200 commits drawn, with long linear runs collapsed ("12 commits"); every command applies in under 5 ms.
- **Artifact / web:** identical.
- **Generator:** yes. Start and goal graphs reachable in $k$ commands, with the par found by breadth-first search over commands in CI; three-tree states; reset predictions; bisect ranges.

### 6.2 `merge-conflict`: Merge conflict

**Composite · P0 · W-A3.** Resolve a conflict in a three-way view, then run the tests, because a clean textual merge can still be wrong.

- **Serves:** 1.2.2 L7; the merge and rebase lessons that hit conflicts.
- **Uses:** `diff-view` (three-way: base, ours, theirs), `code-surface` (the editable result with markers), the `code-cell` runner (tests), `git-model` (the conflict comes from a real merge).
- **Interactions.** For each conflict hunk: Take ours, Take theirs, Take both, or Edit; toggle diff3 markers (the `|||||||` base section); Run tests; Mark resolved (the same as `git add`).
- **The semantic conflict lesson:** one branch renames a function, the other adds a call to the old name. Git merges without a conflict; the tests fail. Show-why `semantic` highlights the two changes that interact.
- **Keyboard:** J and K move between hunks; O, T and B take ours, theirs or both; E edits the hunk; R runs the tests; the result editor follows `code-surface` (Escape then Tab leaves).
- **State:** `{ result: string, choices: Record<string, 'ours' | 'theirs' | 'both' | 'edited'>, resolved: boolean }`.
- **Answers:** `code` (the resolved file passes the tests), `state` (`noConflictMarkers`), `set` (predict which hunks will conflict).
- **Config:** `{ base: string; ours: string; theirs: string; language: string; suite?: CodeSuite; markers?: 'merge' | 'diff3'; task: 'resolve' | 'predict-conflicts' | 'semantic' }`.
- **Visual:** three narrow panes above (stacked on phones), the result below; marker lines in muted text with labels "ours" and "theirs" in words.
- **Motion:** a chosen hunk replaces the markers over 150 ms.
- **Reduced motion:** instant.
- **Accessibility:** hunks as a list with their choices; markers read as "start of our version".
- **Tutor:** describe: "2 conflict hunks; hunk 1 resolved (ours), hunk 2 open. Tests not run." Ids: `hunk:<n>`, `line:<n>`, `test:<k>`.
- **Performance:** trivial.
- **Artifact / web:** test runs follow `code-cell` (section 2.10); without a runtime, recorded test outcomes for the offered choices (CI enumerates them).
- **Generator:** yes. Seeded code with two branches of edits, in conflicting and non-conflicting placements.

### 6.3 `code-review`: Code review

**Composite · P0 · W-A3.** A pull request to review: the description, commits, changed files and checks. The learner flags lines by category and decides whether to approve. Used again in 1.8 and 1.9 as "find the bug".

- **Serves:** 1.2.2 L10, L11; 1.8 and 1.9 bug hunts; 2.3 project hygiene.
- **Uses:** `diff-view` (comments mode with tags), `choice` (approve or request changes), `free-response` (comment text), `value-table` (files and checks).
- **Categories:** bug, missing test, naming, complexity, security (secrets, injection), style.
- **Interactions.** Tap a line's gutter to comment; choose a category; optionally write the comment; Approve or Request changes; Submit review.
- **Grading** [our choice]: each seeded defect has an accepted line range and category. The review passes when every must-find defect is flagged with its category and there are at most 2 flags on clean lines. Comment wording is optional and marked by Bertie's draft against a rubric, which the learner confirms.
- **Keyboard:** `diff-view` keys: J and K move between hunks, Up and Down between lines, Enter opens a comment with a category picker (keys 1 to 6); the decision is a native radio group.
- **State:** `{ comments: { line: string; tag: string; text?: string }[], decision?: 'approve' | 'request-changes' }`.
- **Answers:** `set` (lines with tags), `choice`, `text`.
- **Config:** `{ title: string; description: string; files: { path: string; before: string; after: string }[]; checks?: Record<string, 'pass' | 'fail'>; defects: { id: string; file: string; lines: [number, number]; tag: string; mustFind: boolean; explain: string }[] }`.
- **Visual:** a pull-request layout in the lesson frame (not GitHub's branding); comment markers `--manip` until graded; after grading, missed defects appear with the hint-indigo outline (a reveal, not a success).
- **Motion:** none beyond grading.
- **Reduced motion:** nothing to change.
- **Accessibility:** comments listed with file and line; defects explained in text after grading.
- **Tutor:** describe: "PR 'Add drawdown', 2 files, 41 changed lines; learner flagged 2 lines (bug, naming); decision none." Ids: `file:<path>`, `line:<path>:<n>`, `comment:<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Clean authored code with seeded defects from `mutant-forge` plus templates for leaked keys, injection and missing tests.

### 6.4 `permission-bits`: Permission bits

**Composite · P0 · W-A3.** Unix permissions as a $3 \times 3$ grid of read, write and execute for owner, group and others, with the octal digits, the `ls -l` string and symbolic `chmod` kept in step.

- **Serves:** 1.2.1 L7; 1.2.1 L9 (executable scripts).
- **Uses:** `region-select` (the 9 cells, plus special bits in P1), `live-formula` (octal), `text-terminal` (`ls -l`, `chmod`).
- **Interactions.** Tap cells to toggle bits; type an octal mode or a symbolic change (`u+x,go-w`) and the grid follows; switch between a file and a directory to see what `x` means for each (enter, rather than run).
- **Keyboard:** The grid is a roving group (arrows move, Space toggles); the octal and symbolic fields apply on Enter.
- **State:** `{ mode: number, kind: 'file' | 'directory', special?: number }`.
- **Answers:** `text` (octal or symbolic), `state` (`modeEquals`).
- **Config:** `{ start: string; target?: string; kind: 'file' | 'directory'; scenario?: 'not-executable' | 'cannot-enter' | 'private-key'; umask?: boolean }` (`umask` is P1).
- **Visual:** the grid with row labels "owner", "group", "others" and column labels "read", "write", "execute"; set bits in `--manip`; the octal digits beside each row; the `ls -l` string beneath in the code token.
- **Motion:** none.
- **Reduced motion:** nothing to change.
- **Accessibility:** each cell is a toggle ("group, write, off"); the mode is announced as "750, rwxr-x---".
- **Tutor:** describe: "Mode 640 (rw-r-----), file report.sh; scenario: not executable." Ids: `bit:<who>.<perm>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Target modes; symbolic transformations; scenario diagnoses.

### 6.5 `injection-lab`: Injection lab

**Composite · P0 · W-A3.** Why data must never become code. The learner types an input; the query or command it produces is tokenised, and every character that came from the input is marked. When the input escapes its literal, the structure changes, and the widget says so. With parameters, the input stays one literal whatever it contains. This is the engineering floor's rule (parameterised SQL, argument lists for subprocesses) taught by doing.

- **Serves:** 1.2.3 L14; 1.2.1 (shell quoting); every later project that touches a database or a subprocess.
- **Uses:** `code-surface` (read-addressable, with input-derived tokens marked), the `code-lex` SQL and shell tokenisers, `token-tray` (concatenate or parameters), the `sql-runner` service (web, or the Artifact with WebAssembly).
- **Modes:** `sql` (f-string or concatenation against `?` placeholders), `shell` (`subprocess.run(cmd, shell=True)` with a filename against an argument list).
- **Contexts per mode:** a string literal, a numeric context (no quotes needed: `1 OR 1=1`), a `LIKE` pattern, and an `ORDER BY` column name, which cannot be a parameter and needs an allow-list.
- **Interactions.** Type the input; toggle concatenate against parameters; Run.
- **Keyboard:** The input field updates the tokens on every keystroke; P toggles concatenation and parameters; Tab moves into the token list, read token by token.
- **State:** `{ input: string, method: 'concat' | 'params' | 'allow-list' }`.
- **Answers:** `text` (an input, graded by `inputEscapesLiteral`, and optionally "returns every row"), `choice` (the right fix per context), `code` (the fixed function passes tests).
- **Config:** `{ mode: 'sql' | 'shell'; template: string; context: 'string' | 'number' | 'like' | 'identifier'; db?: { schema: string; rows: string }; task: 'break-it' | 'fix-it' | 'choose-fix' }`.
- **Visual:** input-derived characters carry a hatched `--s2` underline labelled "from input"; when the structure changes, a banner with a warning icon reads "Your input changed the query's structure" and the new tokens are listed.
- **Motion:** none.
- **Reduced motion:** nothing to change.
- **Accessibility:** the token list is text ("keyword OR, from input"); the banner is announced.
- **Tutor:** describe: "SQL, string context, concatenation. Input \"x' OR '1'='1\" produced 3 tokens outside the literal." Ids: `tok:<i>`, `input`, `method`.
- **Performance:** tokenising under 1 ms.
- **Artifact / web:** the structural verdict is pure JavaScript and works everywhere; row results need SQLite.
- **Generator:** yes. Templates across contexts; seeded table contents.

### 6.6 `mutant-hunter`: Mutant hunter

**Composite · P0 · W-A3; coverage overlay and property mode P1 · W-B1.** Learn testing by killing bugs. The learner writes pytest tests for a specification; the tests must pass on the correct function and fail on each mutant, a version with one small deliberate bug. A kill board shows which mutants survive.

- **Serves:** 1.2.4 L1, L3, L4, L9 to L11; 1.8 (edge cases before submitting); 2.3 (testing project code).
- **Uses:** `code-cell` (pytest mode), `code-surface`, `diff-view` (a killed mutant against the reference), `value-table` (the board), the `mutant-forge` and `python-runner` services.
- **Mutants:** built in CI by `mutant-forge` from the reference: relational operators (`<` to `<=`), off-by-one in ranges and slices, changed return values, boundary handling (empty input, single element), swapped arguments, removed statements, loosened float tolerances. A mutant is kept only if a seeded fuzzer finds an input that tells it apart from the reference, so no mutant is unkillable. Each screen shows 4 to 8 mutants chosen by seed and difficulty.
- **Interactions.** Write tests; Run; the board updates (alive or killed, and by which test); a killed mutant opens its diff; after two not-yet results the hint ladder can show the kind of input a surviving mutant mishandles ("an empty list"), never the test.
- **Coverage overlay (P1):** lines the tests executed, shown in the gutter, with the lesson that full coverage can still leave a mutant alive.
- **Property mode (P1):** Hypothesis `@given` tests; a property that holds for the reference and fails for a mutant kills it.
- **Keyboard:** The test editor follows `code-surface`; Ctrl or Cmd + Enter runs; Tab moves into the board, where arrows move between cards and Enter opens a killed mutant's diff.
- **State:** `{ tests: string, board: Record<string, { alive: boolean; killedBy?: string }>, referencePasses: boolean }`.
- **Answers:** `code`, checked by a `learner-tests` test (all reference tests pass; every mutant killed).
- **Config:** `{ spec: string; signature: string; reference: string; mutants: Mutant[]; show: number; starterTests?: string; needs?: string[]; coverage?: boolean; property?: boolean }`.
- **Visual:** mutant cards in a grid, each with a bug glyph, "alive" or "killed" in words, and the killing test's name; the reference status line at the top ("Your tests pass on the correct function").
- **Motion:** a card flips to "killed" over 200 ms when a run completes.
- **Reduced motion:** the state changes without the flip.
- **Accessibility:** the board is a table; results announced ("4 of 6 mutants killed; reference passes").
- **Tutor:** describe: "6 mutants: 4 killed, 2 alive (kinds: boundary, tolerance). Reference passes. Learner has 5 tests." Ids: `mutant:<id>`, `test:<name>`, `line:<n>`. Bertie never sees mutant sources before they are killed.
- **Performance:** each run executes the learner's tests against 1 + $k$ implementations; budget 10 s in total.
- **Artifact / web:** web Pyodide; in the Artifact, MicroPython with the mini-pytest shim for compatible functions, otherwise handoff.
- **Generator:** yes. Mutant selection per seed and difficulty; specifications are authored.

### 6.7 `schema-builder`: Schema builder

**Composite · P1 · W-C (optional lesson 1.2.3 L13).** Design tables from one wide sheet: split columns into tables, pick primary keys, draw foreign keys, and see the update anomalies that normalisation removes.

- **Serves:** 1.2.3 L13; 2.3 project 4 (storing market data).
- **Uses:** `token-tray` (columns into table bins), `node-link` (tables as records with ports; foreign keys as edges), `value-table` (sample rows), `code-surface` (the generated `CREATE TABLE` statements).
- **Interactions.** Drag columns into tables; tap a key column; draw a foreign key from a column port to a table; press "Change a company name" to see an anomaly in the wide version and none in the normalised one.
- **Keyboard:** Column chips follow `token-tray` keys; foreign keys use `node-link`'s keyboard arrow path; K marks the focused column as part of the key.
- **State:** `{ tables: Record<string, { columns: string[]; pk: string[] }>, fks: [string, string][] }`.
- **Answers:** `state` (every non-key column depends on its table's key, using the functional dependencies the author declares), `code` (DDL).
- **Config:** `{ sheet: FrameSpec; dependencies: [string[], string][]; target?: unknown }`.
- **Visual:** tables as `node-link` records with key columns marked "key"; foreign keys as arrows from column ports; anomalies flagged with a warning icon and text.
- **Motion:** columns slide into tables with `spring-snap`; the anomaly demonstration changes one cell at a time over 300 ms.
- **Reduced motion:** instant placement; the anomaly shows before and after.
- **Accessibility:** tables listed as text with their keys and foreign keys; anomalies announced in words.
- **Tutor:** describe: "3 tables: trades(id, instrument_id, qty, price), instruments(id, symbol, company), ... FK trades.instrument_id to instruments.id." Ids: `table:<name>`, `col:<table>.<name>`, `fk:<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Seeded wide sheets with declared dependencies.

### 6.8 `vim-sim`: Vim survival

**Composite · P1 · W-C (optional lesson 1.2.1 L12).** Enough Vim to edit a file on a server: modes, movement, editing, saving and quitting.

- **Serves:** 1.2.1 L12 (optional); remote work in 2.3.
- **Uses:** `code-surface` (buffer display with a block cursor), `text-terminal` (the command line), `speed-timer` (golf mode).
- **Commands (about 30):** `h j k l w b e 0 $ gg G`, `i a I A o O`, `x dd yy p P u` and Ctrl+R, `dw cw`, `.`, `/pattern n N`, `:w :q :wq :q!`. Others show "not in this simulator".
- **Interactions.** A physical keyboard only; phones show "Needs a physical keyboard" and the lesson moves on.
- **State:** `{ buffer: string[], cursor: [number, number], mode: 'normal' | 'insert' | 'command', keys: number, saved: boolean }`.
- **Answers:** `state` (buffer equals the target and is saved), `numeric` (keystrokes against par).
- **Config:** `{ start: string; target: string; par?: number; allowed?: string[] }`.
- **Visual:** a mode indicator in words ("NORMAL", "INSERT") at the bottom; a keystroke log.
- **Motion, reduced motion:** none.
- **Accessibility:** mode changes announced; honest limit as in Stage 0's typing trainer: visual by design.
- **Tutor:** describe: "Mode NORMAL, cursor 3:5, 14 keystrokes, buffer differs from target on line 3." Ids: `line:<n>`, `mode`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Seeded edit tasks with par computed by search over the command subset.

### 6.9 `workspace-sim` (extended from Stage 0)

**Composite extension · P0 · W-A3.** Stage 0's three-pane workspace (tree, editor, terminal).

- **Serves:** 1.1.1 L22 and L26; the 1.1 exit rehearsal; 1.2.4; 1.2.5.
- **Config additions:** `{ git?: { init: boolean; remote?: boolean; ignore?: string[] }; goals: { kind: 'testsPass' | 'committed' | 'ignored' | 'pushed' | string; args?: unknown }[] }`.

It gains what the 1.1 and 1.2 exits rehearse:

- multi-folder projects (`src/`, `tests/`, `data/`) with `pytest -q` and `python -m src.analysis` in the terminal, run by `python-runner` on the `vfs` files;
- a compact Git panel (status and a short log) on `git-model`, sharing the same `vfs`, and respecting `.gitignore`;
- the editor is now `code-cell` in multi-file layout;
- new goal predicates: `testsPass()`, `committed(paths)`, `ignored(path)`, `pushed(branch)`.
- **Tutor:** describe adds the Git status line. **Artifact / web:** as `code-cell`.
- **Everything else** (interactions, keyboard, visual, motion, accessibility, performance) as Stage 0 section 10.5.

### 6.10 `shell-sim` (extended from Stage 0)

**Composite extension · P0 (with P1 parts) · W-A3.** Stage 0 lists the 1.2 commands; this entry fixes the language they run in.

- **Serves:** 1.1.1 L25 and L26; 1.2.1; 1.2.2 (Git); 1.2.4 (pytest in the terminal).
- **Config additions:** `{ dialect: 'bash-subset'; hosts?: Record<string, Record<string, 'dir' | string>>; features?: ('pipes' | 'scripts' | 'jobs' | 'ssh' | 'sed' | 'awk' | 'nano')[] }`.

- **Bash subset (P0)** in the `shell-interpreter` service:
  - words and quoting: single quotes literal, double quotes with `$var` and `$(...)` expansion, backslash escapes;
  - variables: assignment, `$x`, `${x}`, `$1` to `$9`, `$@`, `$#`, `$?`; `export`; arithmetic `$(( ))` with `+ - * / %`;
  - expansion order: tilde, parameter, command substitution, arithmetic, word splitting, then globbing with the `regex-lab` glob matcher;
  - pipes; redirections `>`, `>>`, `<`, `2>`, `2>&1`, `&>`; `&&`, `||`, `;`;
  - `if`, `elif`, `else` with `[ ]` and `test` (`-f -d -e -z -n = != -eq -ne -lt -le -gt -ge`); `for ... in ...; do ... done`; `while` capped at 10,000 iterations;
  - `set -e`, `set -u`, `set -o pipefail`; `exit n`; scripts with a shebang run as `./run.sh` after `chmod +x`; `source`.
- **Commands added (P0):** `grep` (`-i -v -n -c -E -r -l -o`), `sort` (`-n -r -k -t -u`), `uniq` (`-c -d`), `wc`, `head`, `tail`, `cut` (`-d -f`), `tr`, `find` (`-name -type -path`), `xargs` (`-n -I`), `tee`, `diff` (shown through `diff-view`), `chmod`, `ls -l` with modes, `basename`, `dirname`, `date` (fixed clock), `less`, `man` (authored pages), `nano` (a minimal full-screen editor: arrows, typing, Ctrl+O save, Ctrl+X exit), `python3 -m venv`, `pip install` (simulated into the venv's `site-packages`, with realistic output), `pytest` (real through `python-runner` where available, otherwise recorded output), `git` (through `git-model`).
- **P1:** functions; `sed` (`s///g`, `-n` with `p`, `-i`); `awk` (`-F`, `$n`, `NR`, `NF`, `pattern { action }`, accumulating variables, `END`); jobs (`&`, `jobs`, `fg`, `bg`, `kill`, `ps`) over simulated processes; `ssh` and `scp` between hosts that each have their own `vfs`.
- **Dialect** [our choice]: GNU coreutils behaviour and messages. One note in the `sed` lesson covers the macOS difference (`sed -i ''`).
- **Pipeline view:** "Show pipeline" opens the last pipeline in `pipeline-flow`.
- **Grading by effect,** as Stage 0.
- **Tutor:** describe adds the last pipeline's stage counts. **Generator:** adds data-wrangling goals over seeded logs and CSVs.
- **Artifact / web:** identical, except `python3` and `pytest`, which follow `code-cell`.
- **Everything else** (interactions, keyboard, visual, motion, accessibility, performance) as Stage 0 section 10.3.

### 6.11 `setup-checklist` (extended from Stage 0)

**Composite extension · P0 · W-A3 (P1 for the C++ items · W-C).** Stage 0's checklist verifies installs by pasted output. Project mode verifies the exits that happen on the learner's machine.

- **Serves:** the 1.1 exit; the 1.2 exit (1.2.5); 1.9.1 L2; the 1.9 exit.
- **Config additions:** `{ projectChecks: { id: 'exit-1.1' | 'exit-1.2' | 'cpp-toolchain' | 'exit-1.9'; seed?: number; repoUrl?: boolean }[] }`. **State additions:** `{ repoUrl?: string; parsed: Record<string, unknown> }`.

- **1.1 exit:** the app supplies a seeded prices CSV (through `downloads` in the Artifact, a Blob link on the web, or copyable text). The learner runs their script locally and pastes the output; the widget compares the returns, volatility and maximum drawdown with its own computation on the same file (tolerance $10^{-6}$).
- **1.2 exit:** paste `git log --oneline -n 5`, `git status` and `pytest -q`; the widget parses the commit count, a clean tree and "N passed" with N at least 1. On the web app, an optional public repository URL is checked through GitHub's REST API (repository, recent commits, a `tests` folder, and the latest check runs) [unverified: CORS on the check-runs endpoint; unauthenticated limit about 60 requests an hour]. The Artifact cannot reach GitHub, so it uses the pastes only.
- **1.9 toolchain (P1):** `g++ --version` at 11 or later, or `clang++ --version` at 14 or later, for C++20 [our choice]; `cmake --version` optional.
- **1.9 exit (P1):** paste the doctest summary ("test cases: n passed") and the timing output for `bench-lab`.
- **Privacy:** home paths redacted before anything reaches the tutor (Stage 0's rule); repository URLs are the learner's public data and are not sent anywhere except GitHub's API on the learner's request.
- **Honest limit:** paste verification proves the work was done, not who did it; the learner is the only person relying on it.
- **Tutor:** describe adds which exit items are verified; "I'm stuck" sends the redacted paste. **Generator:** seeded exit CSVs.
- **Everything else** (interactions, keyboard, visual, motion, accessibility, performance) as Stage 0 section 10.6.

---

## 7. Composites: data structures and algorithms (1.8)

**The 1.8 pattern.** Every algorithm composite in this section offers the same four ways in, so a lesson can move from acting to reading without changing widget:

- `be`: the learner performs each step (swap these two, move `lo`, pop the queue). Each move is checked by `moveMatchesAlgorithm`, which accepts any move the algorithm allows when there are ties. A wrong move plays the composite's show-why for that move, then restores the state before it. This is "act before you read" for algorithms.
- `predict`: the learner predicts the next state, a value at a checkpoint, or the final result.
- `watch`: `stepper` trace mode over an `algo-trace` run, with Play and the event jumps.
- `code`: the Python source beside the picture; the line for each event lights (section 2.3). In 1.9 and 2.4 a C++ tab shows the same algorithm.

Every composite shows counters (comparisons, swaps, pushes, calls) from the trace, because counting operations is how 1.8 talks about cost. `complexity-lab`, `sort-lab` and `hash-table` (section 4.14) are P0 because 1.1 needs their first modes; the rest of this section is P1.

### 7.1 `complexity-lab`: Complexity lab

**Composite · P0 (growth, race, code) · W-A1; P1 (budget, timing) · W-B1.** How cost grows with input size: comparing growth rates, counting steps in code, races between data structures, operation budgets from constraints, and measuring an exponent from timings.

- **Serves:** 1.1.1 L15; 1.8.1 L1 to L3, L6, L7; 1.8.3 L3; 1.9.3 L2; 2.4.1 L2.
- **Uses:** `plot-2d` (linear and log axes), `marks` (curves, points, a fitted line), `slider` ($n$, constants), `token-tray` (ranking), `code-surface` (hit gutter), `value-table`, `expression-input` (step-count formulas), `live-formula`, the `algo-trace` and `trace-recorder` services.
- **Modes.**
  - `growth`: curves for $1$, $\log n$, $\sqrt{n}$, $n$, $n \log n$, $n^2$, $n^3$, $2^n$ and $n!$; constants $c_1 f(n)$ against $c_2 g(n)$ on sliders to find the crossover; rank by dragging.
  - `race`: step counts for two structures doing the same job (list against set membership, `list.pop(0)` against `deque.popleft()`) as $n$ grows.
  - `code`: a snippet; predict its step count as a formula in $n$ or pick its class; then see line-hit counts recorded at $n = 1$ to $64$ with the fitted curve.
  - `budget` (P1): for $n$, a time limit and a language, mark which complexities fit, using about $10^7$ simple operations a second for CPython and $10^8$ to $10^9$ for optimised C++ [our estimate, stated as a rule of thumb on screen].
  - `timing` (P1): times at $n$, $2n$, $4n$ on a log-log plot; the slope estimates the exponent.
- **Interactions.** Drag sliders; drag function chips into order; type a formula; tap a complexity class; in `timing`, Run.
- **Keyboard:** Sliders take arrow keys; function chips follow `token-tray` keys; the formula field is an `expression-input`; class choices take keys 1 to 9; Run is a button.
- **State:** `{ mode: string, n: number, constants: Record<string, number>, ranking?: string[], formula?: string, picks?: string[] }`.
- **Answers:** `ordering` (growth ranking), `expression` (a step count such as $\frac{n(n-1)}{2}$, graded by `cas` equivalence over $n$), `choice` (a class), `numeric` (a crossover $n$; a slope within 0.15).
- **Config:** `{ mode: string; functions?: string[]; snippet?: { source: string; hits: Record<number, Record<number, number>> }; race?: { a: string; b: string; counts: Record<string, number[]> }; budget?: { n: number; seconds: number; language: 'python' | 'cpp' } }`.
- **Visual:** growth curves in slots s2 to s6 with direct labels; on a log $y$ axis the polynomials become straight lines, and the screen says so; hit counts as gutter bars.
- **Motion:** sliders are direct; nothing else moves.
- **Reduced motion:** nothing to change.
- **Accessibility:** the table view lists $n$ and each function's value; the ranking is a list.
- **Tutor:** describe: "Growth plot n from 1 to 1,000, log y. 100n and n^2 cross at n = 100. Learner ranking: log n, n, n log n, n^2, 2^n." Ids: `curve:<f>`, `slider:n`, `line:<n>`.
- **Performance:** curves sampled at 200 points each.
- **Artifact / web:** identical, except `timing`, which needs a runtime (recorded timings otherwise).
- **Generator:** yes. Snippets with nested, halving and doubling loops and dependent bounds; rankings; crossovers; budget items.

### 7.2 `sort-lab`: Sorting lab

**Composite · P0 (key and stability) · W-A1; P1 (algorithms) · W-B1.** Sorting with keys, then the algorithms themselves: insertion, selection, merge, quick (Lomuto and Hoare partitions), heap, counting and radix sort, stability, the comparison lower bound, and comparators in C++.

- **Serves:** 1.1.1 L19, L20; 1.1.3 L9; 1.8.2 L13; 1.9.3 L3.
- **Uses:** `array-strip` (bars or cards), `value-table` (records for key mode), `token-tray` (key chips), `node-link` (the decision tree for $n = 3$; merge sort's recursion tree), `stepper` (trace mode), `code-surface`, the `algo-trace` service.
- **Modes.**
  - `key` (P0): sort records with key functions built from chips (a field, a tuple of fields, a negated number for descending, `reverse=True`, `str.lower`); stability shown by sorting trades by time and then by symbol.
  - `be`, `predict`, `watch` (P1): the 1.8 pattern for each algorithm.
  - `compare` (P1): algorithms on the same input families (random, sorted, reversed, few distinct values, nearly sorted) with comparison and swap counters.
  - `stability` (P1): records tagged with their original positions; which algorithms keep ties in order.
  - `bound` (P1): the decision tree for 3 items has 6 leaves, so its height is at least $\lceil \log_2 6 \rceil = 3$; in general $\lceil \log_2 n! \rceil = \Theta(n \log n)$ comparisons.
  - `buckets` (P1): counting and radix sort.
  - `comparator` (P1, C++): a `<=` comparator breaks strict weak ordering, and `std::sort` may then crash or misbehave [sourced: undefined behaviour under the standard's requirements, recalled]; show-why explains with a pair that compares "less" both ways.
- **Interactions.** Key mode: drag chips to build the key, Run. Be mode: tap two cells to compare, drag to swap, or (merge) tap the smaller head to move it out; each move is checked.
- **Keyboard:** Key chips follow `token-tray` keys; in `be` mode, arrows move a cursor along the strip, C compares the cursor pair, X swaps it, and M moves the smaller head out during a merge; N steps in `watch` mode.
- **State:** `{ mode: string, values: unknown[], key?: string[], moves: { kind: string; i: number; j?: number }[], counters: Record<string, number> }`.
- **Answers:** `ordering`, `state` (moves), `numeric` (comparisons), `choice`, `set` (stable algorithms).
- **Config:** `{ mode: string; algorithm?: 'insertion' | 'selection' | 'merge' | 'quick-lomuto' | 'quick-hoare' | 'heap' | 'counting' | 'radix'; input: unknown[] | { family: string; n: number; seed: number }; records?: FrameSpec; language?: 'python' | 'cpp' }`.
- **Visual:** bars or cards with the section 2.5 states (active pair, sorted region "done", pivot "special"); comparison and swap counters in the stat token.
- **Show-why:** `wrong-swap` (the move reverses and the cell that should have moved pulses), `instability` (two equal records cross, with their original positions shown).
- **Motion:** swaps animate over 240 ms; merges move items down to the output row over 200 ms.
- **Reduced motion:** cuts.
- **Accessibility:** values as a list after each step ("3, 5, 8 sorted; 2 being inserted"); counters announced on commit.
- **Tutor:** describe: "Insertion sort, step 9 of 31. Sorted prefix [2, 3, 5, 8]; inserting 4 at index 4. Comparisons 12, swaps 7." Ids: `cell:<i>`, `rec:<id>`, `chip:<id>`, `node:<id>`.
- **Performance:** up to 1,000 bars on Canvas 2D at 8 steps a second.
- **Artifact / web:** identical.
- **Generator:** yes. Input families; key tasks over seeded records; stability puzzles.

### 7.3 `dynamic-array`: Dynamic array

**Composite · P1 · W-B1.** Why `append` is cheap on average: a buffer with spare capacity, reallocation when full, and the amortised cost. Front insertion shifts everything. In C++, reallocation leaves iterators, pointers and references dangling.

- **Serves:** 1.8.1 L4; 1.8.2 L1; 1.9.3 L1.
- **Uses:** `array-strip` (the old and new buffers during a copy), `plot-2d` with `marks` (cost per append and the running average), `slider` (growth factor), `live-formula` ($\frac{\text{total cost}}{n}$), the `algo-trace` service.
- **Modes:** `python` (list over-allocation, with sizes recorded from `sys.getsizeof` on the pinned CPython [the exact growth pattern is a CPython detail; recorded, not taught as a rule]), `cpp` (`size`, `capacity`, `reserve`, and dangling iterators after reallocation), `analysis` (growth factors 1.25, 1.5 and 2; the average cost per append tends to a constant, at most 3 for doubling).
- **Interactions.** Append, Insert at 0, Pop, Pop(0); slide the growth factor; in C++ mode, take an iterator to an element and append until it dangles.
- **Keyboard:** Operation buttons are in the tab order (A appends, I inserts at 0, P pops); the growth-factor slider takes arrow keys; Up and Down move between iterators in C++ mode.
- **State:** `{ size: number, capacity: number, factor: number, costs: number[], iterators: { id: string; index: number; valid: boolean }[] }`.
- **Answers:** `numeric` (copies after $n$ appends; average cost), `choice`, `point` (the append that triggers the next reallocation).
- **Config:** `{ mode: 'python' | 'cpp' | 'analysis'; capacity: number; factor: number; ops?: string[] }`.
- **Visual:** filled slots in ink, spare capacity as dashed empty slots; during reallocation the new buffer appears below and elements copy across; a dangling iterator is a dashed arrow ending in a cross, labelled "dangling".
- **Motion:** the copy runs element by element over at most 600 ms as a consequence of the append.
- **Reduced motion:** before and after.
- **Accessibility:** "size 8, capacity 8; append reallocated to capacity 16 and copied 8 elements".
- **Tutor:** describe: "C++ vector size 8, capacity 8; iterator it at index 3 (valid)." Ids: `slot:<i>`, `iter:<id>`, `bar:<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Append sequences, growth factors and capacities.

### 7.4 `pointer-walk`: Pointer walk

**Composite · P1 · W-B1.** Two pointers and sliding windows: pointers from both ends, fast and slow pointers on arrays, fixed and variable windows, three-way partitioning, and merging. An invariant panel states what each move keeps true, and the pair grid shows why a move is safe.

- **Serves:** 1.8.2 L5 to L9; 1.8.5 L12; 2.4.1 L8.
- **Uses:** `array-strip` (markers, window ranges, bars for heights), `cell-grid` (the pair grid: cell $(i, j)$ is the pair of indices; each pointer move rules out a row or a column), `hash-table` (character counts for variable windows), `live-formula` (best so far), `stepper` (trace mode), `code-surface`, the `algo-trace` service.
- **Modes:** `opposite` (sorted two-sum, palindrome, container with most water, trapping rain water), `same` (in-place dedupe, move zeroes, partition), `window-fixed` (maximum sum of $k$, moving average), `window-variable` (longest substring without repeats, minimum window substring, longest repeating character replacement), `flag` (Dutch national flag), `merge` (two sorted arrays), `pairs` (the pair grid on its own).
- **Interactions.** Be the algorithm: drag or arrow-key the pointers; in container-with-most-water, the move must be the shorter side; in windows, extend `right` and shrink `left` while the invariant fails.
- **Show-why:** `unsafe-skip` (the pair grid lights a pair the wrong move would skip that could be the best), `invariant-broken` (the panel's statement turns false and names the duplicate inside the window).
- **Keyboard:** Tab moves between pointers; Left and Right move the focused pointer one cell or gap; Enter commits the move for checking; G opens the pair grid.
- **State:** `{ pointers: Record<string, number>, best?: unknown, moves: string[] }`.
- **Answers:** `state` (moves), `numeric` (the result), `point` (final pointer positions), `choice`.
- **Config:** `{ mode: string; values: (number | string)[]; target?: number; k?: number; invariant: string; showPairs?: boolean }`.
- **Visual:** pointers as `--manip` carets; the window as a dashed `--s4` bracket; ruled-out cells at 25% opacity; the invariant as a sentence above the strip with a status word ("holds" or "broken") and a matching icon, never a grading colour.
- **Motion:** pointer drags direct with `spring-snap`; ruled-out rows in the pair grid fade over 200 ms.
- **Reduced motion:** cuts.
- **Accessibility:** pointers are sliders; the invariant is read on every commit.
- **Tutor:** describe: "Opposite pointers on [1, 3, 4, 6, 8, 11], target 10: lo 1 (3), hi 4 (8), sum 11 > 10. Pairs ruled out: 9 of 15." Ids: `ptr:<name>`, `cell:<i>`, `pair:<i>,<j>`, `invariant`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Arrays and strings per mode: sorted arrays with exactly one or no valid pair; height arrays; strings with planted repeats.

### 7.5 `range-query-lab`: Range query lab

**Composite · P1 (prefix, difference, 2D prefix) · W-B1; P2 (Fenwick, segment tree, sparse table) · W-D.** Answering many range queries fast: prefix sums and products, difference arrays for range updates, 2D prefix sums by inclusion-exclusion, then Fenwick and segment trees for contests.

- **Serves:** 1.8.2 L4; 2.4.1 L7.
- **Uses:** `array-strip` (the array and the prefix array of length $n + 1$), `cell-grid` (2D), `node-link` (segment tree in tidy layout), `bit-lab` (lowest set bit for Fenwick), `live-formula`, `stepper` (trace mode).
- **Modes.**
  - `prefix`: bracket $[l, r)$ and read $P[r] - P[l]$ from two arrows; product of the array except self from prefix and suffix strips.
  - `difference`: add $v$ on $[l, r)$ by writing $+v$ at $l$ and $-v$ at $r$; one prefix pass rebuilds the array.
  - `prefix-2d`: a rectangle sum from four corners.
  - `fenwick` (P2): each index's responsibility range drawn as a bar above it; update walks $i \mathrel{+}= i \mathbin{\&} (-i)$, query walks $i \mathrel{-}= i \mathbin{\&} (-i)$.
  - `segment` (P2): a query splits into $O(\log n)$ canonical nodes, which the learner taps; updates walk a root-to-leaf path; lazy propagation as an optional lesson.
- **Keyboard:** The bracket ends are sliders; Up and Down move between the array and the prefix strip; Space marks a cell or a tree node.
- **Interactions.** Drag the bracket ends; tap the two prefix cells that answer a query; apply a range update by choosing $l$, $r$ and $v$; in Fenwick and segment modes, tap the nodes a query or update visits, in order.
- **State:** `{ mode: string, bracket?: [number, number], updates: [number, number, number][], tapped: string[] }`.
- **Answers:** `numeric`, `set` (nodes visited), `state`.
- **Config:** `{ mode: string; values: number[] | number[][]; queries?: [number, number][]; updates?: [number, number, number][] }`.
- **Visual:** arrows from the bracket ends to the two prefix cells; responsibility ranges as thin bars above the array (Fenwick); visited tree nodes "active".
- **Motion:** arrows draw over 200 ms when the bracket is released; the bracket itself is direct.
- **Reduced motion:** arrows appear at once.
- **Accessibility:** each query is read as a sentence ("sum of indices 2 to 5 is P[6] minus P[2], 31 minus 4, 27"); the table view lists index, value and prefix.
- **Tutor:** describe: "Prefix array [0, 3, 4, 8, 9, 14, 23]; query [2, 5) = 14 - 4 = 10." Ids: `cell:<i>`, `pcell:<i>`, `node:<l>-<r>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Arrays, queries and updates.

### 7.6 `binary-search-lab`: Binary search lab

**Composite · P1 · W-B1.** Binary search done right: the invariant, closed and half-open conventions, updates that always shrink the range, `bisect_left` against `bisect_right`, searching a monotone predicate over an answer space, rotated arrays and sorted matrices.

- **Serves:** 1.8.1 L1; 1.8.2 L10 to L12; 1.8.5 L9 (LIS tops); 1.2.2 L13 (`git bisect`, by analogy); 2.4.1 L8.
- **Uses:** `array-strip`, `cell-grid` (matrix mode), `code-blanks` (update rules), `live-formula` (the invariant and `mid`), `stepper` (trace mode), the `algo-trace` service.
- **Modes:** `game` (guess the number from "higher" and "lower"; at most $\lceil \log_2 n \rceil$ guesses), `classic`, `conventions` (`[lo, hi]` against `[lo, hi)`; the infinite loop when `lo = mid` meets `mid = (lo + hi) // 2` with `hi = lo + 1`), `bounds` (duplicates; left and right insertion points), `predicate` (a strip of false then true values over capacities or speeds; find the first true), `rotated`, `matrix` (index $k$ maps to row $k \,//\, c$, column $k \bmod c$), `cpp` (P1: `lo + (hi - lo) / 2` avoids signed overflow).
- **Interactions.** Be the algorithm: set `mid`, then choose which half survives; or fill the update rules in code and Run on the trap inputs.
- **Show-why:** `stuck` (two iterations with the same `lo` and `hi` light, labelled "no progress"), `lost-answer` (the answer index falls outside the range after a wrong update).
- **Keyboard:** L, M and H focus `lo`, `mid` and `hi`; Left and Right move the focused marker; K keeps the left half and J the right; Enter commits.
- **State:** `{ lo: number, hi: number, mid?: number, history: [number, number, number][], convention: 'closed' | 'half-open' }`.
- **Answers:** `state`, `numeric` (the index or answer), `choice`, `code`.
- **Config:** `{ mode: string; values?: number[]; target?: number; predicate?: { label: string; values: boolean[]; domain: [number, number] }; convention?: 'closed' | 'half-open'; matrix?: number[][] }`.
- **Visual:** discarded halves ruled out at 25%; `lo`, `hi` and `mid` markers; the invariant written above ("the answer is in [lo, hi)").
- **Motion:** discarded halves fade over 200 ms.
- **Reduced motion:** cuts.
- **Accessibility:** each step read as "lo 4, hi 8, mid 6, value 17 > 13, keep left half".
- **Tutor:** describe: "Half-open search for 13 in 12 values: lo 4, hi 8, mid 6 (17). History: 3 steps." Ids: `ptr:lo`, `ptr:hi`, `ptr:mid`, `cell:<i>`, `invariant`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Sorted arrays with duplicates, absent targets, predicate problems (weights and days), rotations, matrices.

### 7.7 `stack-queue-lab`: Stacks and queues

**Composite · P1 · W-B1.** Stacks, queues, deques and ring buffers, and the patterns built on them: bracket matching, Reverse Polish evaluation, the min stack, monotonic stacks and deques, a queue from two stacks.

- **Serves:** 1.8.2 L9; 1.8.3 L1 to L3; graph BFS and DFS panels in 1.8.4.
- **Uses:** `array-strip` (vertical for stacks, horizontal for queues, ring mode), `token-tray` (items to push), `stepper` (trace mode), `complexity-lab` (the `list.pop(0)` race), the `algo-trace` service.
- **Modes:** `stack`, `brackets`, `rpn`, `min-stack`, `monotonic-stack` (next greater element, daily temperatures, largest rectangle in a histogram), `queue`, `deque`, `monotonic-deque` (sliding window maximum), `ring` (head and tail; telling full from empty), `two-stacks`.
- **Interactions.** Push and Pop buttons, or drag items; be the algorithm ("pop while the top is smaller than the new value"); predict the pop order.
- **Keyboard:** U pushes the focused input item and O pops; Enter steps in `be` mode; Up and Down read the stack or queue item by item.
- **State:** `{ mode: string, items: unknown[], head?: number, tail?: number, input?: unknown[], pos?: number, out: unknown[] }`.
- **Answers:** `state`, `ordering` (pop order), `numeric` (for example, days until warmer), `code`.
- **Config:** `{ mode: string; input?: string | number[]; capacity?: number; ops?: string[] }`.
- **Visual:** the stack grows upwards with "top" labelled; the queue runs left to right with "front" and "back"; popped items move to an output row.
- **Motion:** push and pop slide over 150 ms.
- **Reduced motion:** cuts.
- **Accessibility:** contents read bottom to top ("stack: (, [, {"); each operation announced.
- **Tutor:** describe: "Monotonic stack over temperatures [73, 74, 75, 71, 69, 72, 76]: at index 5 (72), stack holds indices 2, 3, 4." Ids: `item:<k>`, `in:<i>`, `out:<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical.
- **Generator:** yes. Bracket strings (balanced and not), RPN expressions, temperature series, histograms, operation sequences.

### 7.8 `linked-list-lab`: Linked list lab

**Composite · P1 · W-B1.** Nodes and pointers you rewire by hand: traversal, insertion and deletion with a dummy head, in-place reversal, fast and slow pointers, merging, the LRU cache, and copying a list with random pointers. A node nothing points to greys out as lost.

- **Serves:** 1.8.3 L4 to L8; 1.9.2 (pointers, for C++).
- **Uses:** `node-link` (row layout; record nodes with `val`, `next` and, when doubly linked, `prev`; tags for pointer variables), `hash-table` (LRU and copy panels), `stepper` (trace mode), `code-surface`, the `algo-trace` service.
- **Modes:** `basics`, `reverse`, `cycle` (Floyd: where `slow` and `fast` meet, then why restarting one pointer from the head finds the cycle's start), `merge`, `lru`, `random-copy`, `k-group` (optional).
- **Interactions.** Drag arrow heads to rewire `next`; drag pointer tags (`prev`, `curr`, `nxt`, `head`, `slow`, `fast`) onto nodes; the keyboard path is `node-link`'s.
- **Show-why:** `lost-node` (rewiring `curr.next` before saving `nxt` greys out the rest of the list, labelled "lost: nothing points here"), `cycle-meet` (the distances from the head and from the meeting point to the cycle start are marked equal).
- **Keyboard:** `node-link`'s arrow path rewires `next` (focus the slot, Enter, choose a node with the arrows, Enter); T then arrows moves a tag; Delete sets the focused pointer to `None`.
- **State:** `{ nodes: { id: string; val: unknown; next: string | null; prev?: string | null }[], tags: Record<string, string | null> }`.
- **Answers:** `state` (`listShape`, `noLostNodes`), `ordering` (the order of pointer assignments, as a Parsons task), `numeric`, `code`.
- **Config:** `{ mode: string; values: unknown[]; doubly?: boolean; cycleAt?: number; ops?: string[]; capacity?: number }`.
- **Visual:** nodes as records; arrows in ink, learner-rewired arrows `--manip` until graded; lost nodes at 25% with the label.
- **Motion:** a rewired arrow follows the pointer directly; the list reflows over 300 ms after a commit.
- **Reduced motion:** reflow cuts.
- **Accessibility:** the list read from `head` ("head to 3 to 7 to 9 to None; curr at 7"); lost nodes announced.
- **Tutor:** describe: "Singly linked list 1, 2, 3, 4. prev at 1, curr at 2, nxt at 3. 1.next is None; 2.next is 3." Ids: `node:<id>`, `slot:<id>.next`, `tag:<name>`.
- **Performance:** up to 30 nodes.
- **Artifact / web:** identical.
- **Generator:** yes. Lengths and values; cycle positions; LRU operation sequences; $k$ values.

### 7.9 `interval-sweep`: Interval sweep

**Composite · P1 · W-B1.** Intervals on a timeline: merging, inserting, the greedy that schedules the most non-overlapping intervals (by earliest end), the fewest removals, meeting rooms, and points that stab every interval. The exchange argument is shown by swapping one interval.

- **Serves:** 1.8.2 L15; 1.8.5 L11.
- **Uses:** `plot-2d` (time axis), `marks` (horizontal bars as a Gantt mark, requested from the marks owner), `drag-point` (the sweep line), `heap-lab` (a small panel of end times for rooms), `token-tray` (chosen intervals), `stepper` (trace mode), the `algo-trace` service.
- **Modes:** `merge`, `insert`, `schedule`, `min-removals`, `rooms`, `points`, `exchange` (take an optimal schedule, swap its first interval for the earliest-ending one, and see nothing else conflicts).
- **Interactions.** Drag the sweep line; tap intervals to choose; tap overlapping pairs to merge; toggle sorting by start or by end.
- **Keyboard:** The sweep line is a slider; Up and Down move between intervals and Space chooses one; M merges the focused interval with the next; S toggles the sort.
- **State:** `{ chosen: string[], merged?: [number, number][], sweep: number, sortBy: 'start' | 'end' }`.
- **Answers:** `set` (chosen intervals), `numeric` (count, rooms), `state` (the merged list).
- **Config:** `{ mode: string; intervals: { id: string; start: number; end: number; label?: string }[]; closed?: boolean }` (whether touching intervals overlap is stated per problem).
- **Visual:** intervals as rounded bars in slots by row; chosen bars `--manip`; conflicts marked with a cross glyph where they overlap.
- **Motion:** sorting reflows rows over 300 ms; the sweep line is direct.
- **Reduced motion:** cuts.
- **Accessibility:** intervals listed with start and end; overlaps announced.
- **Tutor:** describe: "8 intervals sorted by end. Chosen: [1, 3], [4, 6]. Sweep at 6." Ids: `iv:<id>`, `sweep`.
- **Performance:** up to 100 intervals.
- **Artifact / web:** identical.
- **Generator:** yes. Interval sets with controlled overlaps and unique optima where the task asks for "the" answer.

### 7.10 `bit-lab`: Bit lab

**Composite · P1 · W-B1 (P2 subset mode · W-D).** Integers as bits: binary and hexadecimal, two's complement, shifts and masks, the classic tricks, counting bits, fast exponentiation, fixed-width C++ integers against Python's unbounded ones, and bitmasks as subsets.

- **Serves:** 1.8.5 L13; 1.9.1 L3, L6; 2.4.1 L6, L10; Fenwick trees in `range-query-lab`.
- **Uses:** `array-strip` (bits mode), `region-select` (tap bits), `slider` (width), `live-formula`, `cell-grid` (the subsets table), `place-value-chart` (Stage 0, for the base-2 bridge).
- **Modes:** `binary`, `twos` (a 4-bit or 8-bit wheel: signed and unsigned readings; overflow wraps), `ops` (AND, OR, XOR, NOT, shifts; arithmetic against logical right shift), `tricks` ($x \mathbin{\&} (x - 1)$ clears the lowest set bit; $x \mathbin{\&} (-x)$ isolates it; XOR cancels pairs), `count` (popcount; `bits[i] = bits[i >> 1] + (i & 1)`), `power` (the exponent's bits drive square-and-multiply, with modular reduction), `subsets` (P2: masks as subsets; iterating submasks), `cpp` (fixed widths; unsigned wraps; signed overflow is undefined; `uint8_t + uint8_t` promotes to `int`), `python` (unbounded integers; negatives behave as if sign-extended forever; `~x == -x - 1`; `& 0xFFFFFFFF` emulates 32 bits).
- **Interactions.** Tap bits to flip; type a number in any base; slide the width; turn the two's complement wheel past the top.
- **Keyboard:** Bits form a roving group (Left and Right move, Space flips); the number field accepts any base with a prefix (`0b`, `0x`); the width is a native select; on the wheel, Left and Right turn one step.
- **State:** `{ mode: string, width: number, value: bigint, mask?: bigint, steps?: unknown[] }`.
- **Answers:** `text` (binary or hexadecimal), `numeric`, `state` (mask bits), `choice`.
- **Config:** `{ mode: string; width: 4 | 8 | 16 | 32 | 64; signed?: boolean; value?: string; target?: string; language?: 'python' | 'cpp' }`.
- **Visual:** bits in cells with place values above; the sign bit labelled; masks drawn as a second strip; results under a rule line, as in written arithmetic.
- **Motion:** the wheel turns with the drag; shifts slide bits one place over 150 ms per place.
- **Reduced motion:** shifts cut.
- **Accessibility:** "8-bit signed 11110110 is -10; unsigned 246".
- **Tutor:** describe: "8-bit value 0b10110100 (180 unsigned, -76 signed); mask 0b00001111; AND gives 0b00000100." Ids: `bit:<i>`, `mask:<i>`, `wheel`.
- **Performance:** trivial; BigInt for 64 bits.
- **Artifact / web:** identical.
- **Generator:** yes. Conversions, masks, tricks, overflow predictions, fast-power step counts.

### 7.11 `tree-lab`: Tree lab

**Composite · P1 · W-B2 (B-tree mode P2 · W-D).** Binary trees and their recursions, binary search trees, balance, construction from traversals, serialisation, lowest common ancestors and tries.

- **Serves:** 1.8.4 L1 to L7; 1.9.3 L2 (`std::map` as a balanced tree); 1.2.3 L16 (B-tree, P2).
- **Uses:** `node-link` (tidy layout), `array-strip` (traversal output, serialised arrays, the explicit stack or queue), `token-tray` (a key to insert), `cell-grid` (word-search board with a trie), `stepper` (trace mode), `code-surface`, the `algo-trace` service.
- **Modes:**
  - `traversal`: pre-order, in-order, post-order and level order; tap nodes in visit order; the stack or queue shows beside the tree.
  - `recursion`: values computed bottom-up (height, size, subtree sum); for the diameter and maximum path sum, each node shows two numbers, "returns" (to its parent) and "records" (the global best), because confusing them is the commonest bug.
  - `bst`: search paths; insert by dragging a key down, choosing left or right at each node; delete with its three cases (leaf, one child, two children through the in-order successor); validate with bounds, where each node carries its allowed interval $(low, high)$ and the parent-only check is shown failing on a deep violation.
  - `balance`: insert 1 to 7 in order (a list of height 7) and shuffled (height about 3); rotations as an optional demonstration.
  - `construct`: from pre-order and in-order: tap the root in pre-order, see it split in-order.
  - `serialise`: level order with nulls, and back.
  - `lca`: root-to-node paths and their last shared node.
  - `trie`: insert words; count words with a prefix; search a letter board.
  - `btree` (P2): nodes with several keys; a search path; why a database index is shallow.
- **Interactions.** Tap nodes in order; drag keys down; tap a node to delete; be the algorithm in each mode.
- **Show-why:** `parent-only-check` (the deep node that violates the ancestor's bound lights with its interval), `returns-vs-records` (the value a node records but must not return).
- **Keyboard:** `node-link` keys move between nodes; Space taps a node in visit order; when inserting, L and R choose a child and Enter descends; Delete removes the focused node in `bst` mode.
- **State:** `{ mode: string, nodes: { id: string; key: unknown; left: string | null; right: string | null }[], order: string[], annotations: Record<string, unknown> }`.
- **Answers:** `ordering`, `state` (`isBst`, `treeEquals`), `numeric` (height), `set`, `code`.
- **Config:** `{ mode: string; tree: unknown | { family: 'balanced' | 'skewed' | 'random' | 'bst-from-order'; n: number; seed: number }; keys?: unknown[]; words?: string[]; task: string }`.
- **Visual:** nodes as circles with keys; null children as small dashed stubs where they matter; intervals as caption labels under nodes in `bst` validate.
- **Motion:** structure changes reflow over 300 ms; a dragged key follows the pointer and snaps to a child slot.
- **Reduced motion:** cuts.
- **Accessibility:** nested-list text view; visit order announced as it grows.
- **Tutor:** describe: "BST of 9 keys, height 4. Inserting 13: path 20 to 10 to 15; learner at 15 choosing left." Ids: `node:<key>`, `slot:<key>.left`, `slot:<key>.right`.
- **Performance:** up to 63 nodes in SVG.
- **Artifact / web:** identical.
- **Generator:** yes. Random trees (5 to 31 nodes; balanced, skewed, random), BSTs from insertion orders, trie word lists, traversal pairs for construction.

### 7.12 `heap-lab`: Heap lab

**Composite · P1 · W-B1.** A binary heap as a tree and as an array at once: sift up after a push, sift down after a pop, bottom-up heapify in $O(n)$, heap sort, top-$k$, the running median with two heaps, and $k$-way merging.

- **Serves:** 1.8.3 L7, L9 to L11; 1.8.4 L13 and L14 (the priority queues inside Dijkstra and Prim); 1.9.3 L2 (`priority_queue`).
- **Uses:** `node-link` (tidy) and `array-strip` (linked by index: children of $i$ at $2i + 1$ and $2i + 2$, parent at $\lfloor (i - 1) / 2 \rfloor$), `stepper` (trace mode), `plot-2d` with `marks` (work per level), the `algo-trace` service.
- **Modes:** `push`, `pop` (the trap: sifting down towards the larger child of a min-heap), `heapify` (from the last parent backwards; total work $\sum_{h} \frac{n}{2^{h+1}} O(h) = O(n)$ shown as bars per level), `sort`, `top-k`, `median`, `k-merge`, `max-trick` (Python's `heapq` is a min-heap: push negated values).
- **Interactions.** Be the algorithm: tap the pair to swap; predict the array after an operation; predict pop order.
- **Show-why:** `wrong-child` (the swap with the larger child leaves a parent bigger than its other child, which lights).
- **Keyboard:** Arrows move between nodes (Up to the parent, Left and Right to the children); X swaps the focused node with its parent or the chosen child; the tree and the array share one focus.
- **State:** `{ mode: string, array: number[], kind: 'min' | 'max', swaps: [number, number][] }`.
- **Answers:** `state` (`isHeap` after each operation), `ordering` (pop order), `numeric` (swaps, total work), `code`.
- **Config:** `{ mode: string; kind: 'min' | 'max'; values: number[]; ops?: string[]; k?: number; stream?: number[] }`.
- **Visual:** the tree above, the array below, a hovered node lighting its cell and the reverse; the sift path "active".
- **Motion:** swaps animate in both views together over 240 ms.
- **Reduced motion:** cuts.
- **Accessibility:** the array read with parent and child relations ("index 1, value 5, children 9 and 7").
- **Tutor:** describe: "Min-heap [2, 5, 3, 9, 7, 8]; popping: 8 moved to root, comparing children 5 and 3." Ids: `node:<i>`, `cell:<i>`.
- **Performance:** up to 63 nodes.
- **Artifact / web:** identical.
- **Generator:** yes. Arrays, operation sequences and streams.

### 7.13 `graph-search`: Graph search

**Composite · P1 · W-B2.** Graphs and how to explore them: representations, BFS with layers and shortest unweighted paths, multi-source BFS, DFS with discovery and finish times, components and flood fill, cycle detection with three colours, topological sort, bipartite checks, and Eulerian paths.

- **Serves:** 1.8.4 L8 to L11, L15; 2.4.1 L9; Markov-chain and dependency graphs elsewhere.
- **Uses:** `node-link` (fixed, circular or layered layouts), `cell-grid` (grid graphs), `array-strip` (queue and stack panels), `value-table` (adjacency list and matrix), `stepper` (trace mode), `code-surface`, the `algo-trace` service.
- **Modes:** `represent` (fill an adjacency list or matrix from the drawing, or draw from a list), `bfs`, `multi-bfs`, `dfs` (recursive or with an explicit stack; edge classes tree, back, forward and cross in P1), `components`, `cycle`, `topo` (Kahn's in-degree counters and queue; DFS post-order reversed; a cycle makes it impossible), `bipartite`, `euler` (optional), `implicit` (neighbours generated on demand: word ladders, grid moves).
- **Interactions.** Be the algorithm: tap the next node to pop or visit; type distances into nodes; draw edges in `represent`. Any valid order is accepted unless the lesson sets a tie rule such as "visit neighbours in increasing label order" (decision 13).
- **Show-why:** `visited-too-late` (marking a node visited when it is popped rather than when it is pushed lets it enter the queue twice; the duplicate lights), `back-edge` (the grey-to-grey edge that proves a cycle).
- **Keyboard:** `node-link` keys move between nodes; Space taps the next node to visit or pop; digits type a distance into the focused node; in `represent`, the adjacency table uses grid keys.
- **State:** `{ mode: string, visited: string[], frontier: string[], dist: Record<string, number>, parent: Record<string, string>, colours: Record<string, 'white' | 'grey' | 'black'>, order: string[] }`.
- **Answers:** `ordering` (graded by `visitOrderValid` or `topoOrderValid`), `numeric` (distances, counts), `set` (a component, a cycle), `state` (a filled representation), `mapping`.
- **Config:** `{ mode: string; graph: { nodes: string[]; edges: [string, string][]; directed: boolean; at?: Record<string, [number, number]> } | { grid: string[] } | { words: string[]; start: string; end: string }; start?: string | string[]; tieRule?: 'label' | 'any' }`.
- **Visual:** frontier nodes dashed `--s4`; visited "done" with hatch; current "active"; BFS layers labelled with their distance; parent arrows drawn as a tree over the graph; DFS colours shown as white, grey and black with the words.
- **Motion:** nodes change state over 150 ms when stepped; the parent tree draws in as edges are used.
- **Reduced motion:** cuts.
- **Accessibility:** adjacency-list text view; each step read as "pop B, push E and F, distance 2".
- **Tutor:** describe: "Undirected graph 9 nodes, 12 edges. BFS from A: visited A, B, C; queue D, E; layer 2 in progress." Ids: `node:<id>`, `edge:<a>-<b>`, `cell:<r>,<c>`, `q:<k>`.
- **Performance:** up to 300 nodes in SVG; grids up to $50 \times 50$.
- **Artifact / web:** identical.
- **Generator:** yes. Graphs generated geometrically (points on a jittered grid, edges between near neighbours, so drawings are tidy without a runtime layout), DAGs, graphs with planted cycles, bipartite and non-bipartite graphs, island grids, word lists.

### 7.14 `shortest-path`: Shortest paths and spanning trees

**Composite · P1 · W-B2.** Weighted graphs: Dijkstra's algorithm with a priority queue, why negative edges break it, Bellman-Ford and its $k$-stops variant, and minimum spanning trees by Prim and Kruskal with the cut property.

- **Serves:** 1.8.4 L13, L14; 2.4.1 L9.
- **Uses:** `node-link` (fixed layout with weights), `heap-lab` (the priority queue panel), `union-find` (Kruskal's panel), `value-table` (distance table per round), `stepper` (trace mode), the `algo-trace` service.
- **Modes:** `dijkstra` (tentative distances; relaxations; settled set; stale queue entries skipped, as in the `heapq` approach), `negative` (a three-node counterexample where a node settles too early), `bellman-ford` (rounds; negative-cycle detection on round $n$; the $k$-stops variant must relax from a copy of the previous round, and the trap of updating in place lights), `prim`, `kruskal`, `cut` (choose a cut; its lightest crossing edge lies in a minimum spanning tree), `zero-one` (P2: 0-1 BFS with a deque).
- **Interactions.** Be the algorithm: pop the queue, relax edges by tapping them, settle nodes; in Kruskal, accept or reject each edge in weight order.
- **Show-why:** `settled-too-early`, `in-place-round`, `cycle-edge` (Kruskal's rejected edge with the cycle it would close).
- **Keyboard:** Arrows move between nodes; Tab moves through the focused node's edges; R relaxes the focused edge; S settles the focused node; in Kruskal, A accepts and X rejects the current edge.
- **State:** `{ mode: string, dist: Record<string, number>, settled: string[], queue: [number, string][], chosen: string[], round?: number }`.
- **Answers:** `numeric` (distances), `ordering` (settle order), `set` (tree or path edges, graded by `mstValid` or `distancesEqual`), `state`.
- **Config:** `{ mode: string; graph: { nodes: string[]; edges: [string, string, number][]; directed: boolean; at?: Record<string, [number, number]> }; source?: string; k?: number }`.
- **Visual:** weights on chips; relaxed edges pulse once; settled nodes "done"; chosen tree edges 3px ink.
- **Motion:** relaxations pulse over 300 ms as a consequence of a tap.
- **Reduced motion:** static ring for one step.
- **Accessibility:** a distance table after each step; relaxations read as "relax B to D: 7 + 2 = 9 < 12, update".
- **Tutor:** describe: "Dijkstra from A: settled A, C; queue (4, B), (9, D), (12, D stale)." Ids: `node:<id>`, `edge:<a>-<b>`, `pq:<k>`.
- **Performance:** up to 60 nodes.
- **Artifact / web:** identical.
- **Generator:** yes. Weighted geometric graphs with positive weights and unique shortest paths (or tie rules), negative-edge cases, distinct weights for a unique minimum spanning tree.

### 7.15 `union-find`: Union-find

**Composite · P1 · W-B2.** Disjoint sets as a forest and a parent array: union by rank or size, path compression, component counting, finding the redundant edge, and its role in Kruskal's algorithm.

- **Serves:** 1.8.4 L12, L14; 2.4.1 L9.
- **Uses:** `node-link` (forest layout), `array-strip` (parent and rank arrays, linked by index), `stepper` (trace mode), the `algo-trace` service.
- **Modes:** `naive` (arbitrary roots make tall trees), `rank`, `compress` (a find re-points every node on its path to the root), `components`, `redundant`.
- **Interactions.** Tap two nodes to union; tap a node to find (its path lights, then compresses); predict the parent array after a sequence.
- **Keyboard:** U, then two nodes chosen with the arrows and Enter, performs a union; F on a focused node runs find; the parent array uses grid keys for predictions.
- **State:** `{ parent: number[], rank: number[], log: string[] }`.
- **Answers:** `state` (the parent array), `numeric` (path length, component count), `set`.
- **Config:** `{ mode: string; n: number; ops?: ['union' | 'find', number, number?][] }`.
- **Visual:** roots marked "root"; a compressed path's new arrows drawn in ink over the old dashed ones for one step.
- **Motion:** compression re-points arrows over 300 ms.
- **Reduced motion:** cuts.
- **Accessibility:** the parent array as a table; finds read as "find 7: 7 to 4 to 1, root 1; compressed".
- **Tutor:** describe: "10 elements, 4 sets; parent [0, 0, 1, 3, 3, 5, 5, 5, 8, 8]." Ids: `node:<i>`, `cell:<i>`.
- **Performance:** up to 50 elements.
- **Artifact / web:** identical.
- **Generator:** yes. Operation sequences and graphs with a planted redundant edge.

### 7.16 `recursion-tree`: Recursion tree

**Composite · P1 · W-B2.** Recursion made visible: the call tree growing in execution order with the stack beside it, backtracking with pruning, memoisation collapsing repeated calls, divide and conquer, and the recursion-tree method for recurrences.

- **Serves:** 1.8.1 L5, L8; 1.8.4 L3; 1.8.5 L1 to L4; 1.8.2 L13 (merge sort and quicksort trees).
- **Uses:** `node-link` (tidy; layered for the DAG view), `array-strip` (the call stack), `value-table` (memo table), `cell-grid` (N-Queens and word-search boards), `live-formula` (per-level work and totals), `stepper` (trace mode), `code-surface`, the `algo-trace` service.
- **Modes:** `calls` (Fibonacci, factorial, fast power, list sum; return values bubble up), `backtrack` (subsets, permutations, combination sum, N-Queens, word search; edges labelled "choose", the return labelled "unchoose"; pruned branches ruled out; solutions marked "special"), `memo` (repeated subproblems share a label; with a memo, repeats become one-node lookups; the tree folds into a DAG), `divide` (merge sort splits and merges; quicksort's tree with a bad pivot), `cost` (work per node, sum per level, total; the three master theorem cases for $T(n) = aT(n/b) + f(n)$).
- **Interactions.** Step (calls appear depth-first); predict the number of calls; tap repeated subproblems; tap where to prune; fill per-level costs.
- **Show-why:** `exponential` (the repeated subtrees of `fib(5)` light in the same colour), `missing-base` (the tree keeps growing past the frame, labelled "no base case reached").
- **Keyboard:** N steps to the next call; arrows move between call nodes; Space marks a node as repeated or as a pruning point; level costs are numeric fields.
- **State:** `{ mode: string, step: number, tapped: string[], levelCosts?: string[] }`.
- **Answers:** `numeric` (calls, depth), `set` (repeated or pruned nodes), `expression` (a total cost), `ordering`.
- **Config:** `{ mode: string; fn: 'fib' | 'fact' | 'power' | 'subsets' | 'permutations' | 'combination-sum' | 'n-queens' | 'word-search' | 'merge-sort' | 'quicksort' | 'recurrence'; input: unknown; memo?: boolean; recurrence?: { a: number; b: number; f: string } }`.
- **Visual:** nodes labelled with their arguments (`fib(3)`); the current call "active"; the stack panel shows the root-to-current path; memo hits drawn as small stubs labelled "memo".
- **Motion:** new calls appear over 150 ms; returns travel up their edge over 200 ms.
- **Reduced motion:** cuts.
- **Accessibility:** the tree as nested lists with return values; the stack read top to bottom.
- **Tutor:** describe: "fib(6) without memo: 25 calls so far of 25; depth 6; fib(2) called 5 times." Ids: `call:<k>`, `frame:<k>`, `level:<d>`.
- **Performance:** at most 500 nodes drawn; deeper trees summarised per level ("level 7: 128 calls").
- **Artifact / web:** identical.
- **Generator:** yes. Inputs, backtracking instances (sets, targets, board sizes), recurrences.

### 7.17 `dp-table`: Dynamic programming table

**Composite · P1 · W-B2.** Dynamic programming as a table you fill: state, recurrence, fill order, dependencies, and reconstruction of the answer, in one and two dimensions, with state machines, rolling arrays and the top-down against bottom-up comparison.

- **Serves:** 1.8.2 L14; 1.8.5 L4 to L10; 2.4.1 L10.
- **Uses:** `cell-grid` (the table, with headers such as string characters, dependency arrows and paths), `array-strip` (1D tables), `live-formula` (the recurrence with numbers filled in), `node-link` (state-machine transitions; the subproblem DAG), `choice` (pick the recurrence), `stepper` (trace mode), `code-surface`, the `algo-trace` service.
- **Modes:** `1d` (climbing stairs, house robber, coin change for fewest coins and for number of ways, decode ways, word break, LIS in $O(n^2)$), `running` (Kadane: best ending here and best so far), `2d` (unique paths, LCS, edit distance, 0/1 knapsack, interleaving strings), `reconstruct` (trace the choices back from the final cell), `states` (several rows for several states, with the transition diagram; buying and selling with a cooldown), `space` (rolling arrays; the loop direction that separates 0/1 knapsack from unbounded), `interval` (optional; by increasing length), `order` (top-down memo order against bottom-up order on the same table).
- **Interactions.** Tap a cell and the cells it reads light with arrows while the recurrence fills in with their values; type cell values (be the algorithm), checked together with per-cell marks; choose the recurrence from candidates; tap the cells on an optimal path.
- **Show-why:** `wrong-dependency` (the cell the learner's value implies they read lights beside the ones the recurrence reads), `double-count` (filling a knapsack row left to right reads a cell already updated this row, so one item is used twice; the two reads light).
- **Keyboard:** `cell-grid` keys; Enter edits the focused cell and its dependencies light; Tab moves to the next cell in fill order; Space marks a cell on the reconstruction path; recurrence options take keys 1 to 9.
- **State:** `{ mode: string, cells: Record<string, string>, path: string[], recurrence?: string, filled: number }`.
- **Answers:** `numeric` per cell through `multi` (`tableMatches`), `set` (path cells, graded by `pathCells`, which accepts any optimal path unless the item asks for a tie rule), `choice`, `state`, `code`.
- **Config:** `{ mode: string; problem: string; input: unknown; prefilled?: string[]; editable?: string[]; recurrenceOptions?: { id: string; tex: string }[]; states?: { id: string; label: string }[] }`.
- **Visual:** headers in the code token; filled cells "done"; the focused cell "active"; its dependencies "frontier"; an optimal path as a 2.5px ink polyline.
- **Motion:** during Play, cells fill in order over 150 ms each; arrows draw for the focused cell only.
- **Reduced motion:** cells appear without fades.
- **Accessibility:** each cell names the cells it reads ("dp[3][4] = min(dp[2][4], dp[3][3], dp[2][3]) + 1 = 2"); the table view is the grid.
- **Tutor:** describe: "Edit distance 'kitten' to 'sitting': 7 × 8 table, 23 of 56 filled; focus (3, 4) = 2." Ids: `cell:<r>,<c>`, `row:<r>`, `col:<c>`, `state:<id>`.
- **Performance:** tables up to $30 \times 30$ in SVG.
- **Artifact / web:** identical.
- **Generator:** yes. Small inputs per family (strings up to 8 characters, amounts up to 30, up to 6 items), with unique optima where a single answer is asked for.

### 7.18 `counterexample-lab`: Counterexample lab

**Composite · P1 · W-B1 (hack mode P2 · W-D).** Break a claim by building an input. The learner edits an input until two procedures disagree, or a property fails: a greedy rule against the true optimum, buggy code against its specification, a false statement, the learner's own fast solution against brute force (stress testing), or someone else's contest submission (hacking).

- **Serves:** 1.2.4 L11; 1.8.5 L11, L16; 2.4.1 L11.
- **Uses:** an input editor chosen by input type (`array-strip` editable, a text field, `interval-sweep`, `node-link` with edge drawing and weights, number chips), `value-table` (outputs side by side), `diff-view`, the `algo-trace` and `python-runner` services.
- **Modes:** `greedy` (coin systems such as $\{1, 3, 4\}$ for 6; interval rules like shortest first; fractional against 0/1 knapsack), `bug` (an off-by-one binary search; a drawdown function that resets its running maximum), `claim` ("this sort is stable", "Dijkstra handles negative edges", "BFS finds shortest weighted paths"), `stress` (random small inputs from a generator run through brute force and the learner's solution until they disagree; the failing input shrinks by delta debugging to a minimal one), `hack` (P2: an input that makes a given submission wrong or too slow, judged by a line budget).
- **Interactions.** Edit the input; Run both; read the outputs side by side; Submit the counterexample. In `stress`, Start and Stop, with a counter of inputs tried.
- **Keyboard:** The input editor uses its primitive's keys (strip, text, intervals or graph); R runs both procedures; Enter submits the input; in `stress`, S starts and stops.
- **State:** `{ mode: string, input: unknown, outputs?: [unknown, unknown], tried?: number, shrunk?: unknown }`.
- **Answers:** `state` or `text` (the input), graded by `outputsDiffer` or `violates`, together with `inputWithinConstraints`.
- **Config:** `{ mode: string; inputType: 'array' | 'string' | 'intervals' | 'graph' | 'numbers'; constraints: Record<string, unknown>; candidate: string; reference: string; property?: string; generator?: string; language?: 'js-model' | 'python' }`.
- **Visual:** the two outputs in columns labelled "claim" and "truth" (or "yours" and "brute force"); a disagreement framed with a cross icon and the word "differs".
- **Motion:** none.
- **Reduced motion:** nothing to change.
- **Accessibility:** inputs and outputs as text; stress progress announced every 100 inputs.
- **Tutor:** describe: "Greedy coins {1, 3, 4}, amount 6: greedy 3 coins (4+1+1), optimal 2 (3+3). Learner input differs: yes." Ids: `input`, `out:candidate`, `out:reference`.
- **Performance:** authored pairs run as JavaScript models in microseconds; stress mode on Python runs 200 inputs a second or more on the web [unverified].
- **Artifact / web:** authored modes identical; `stress` and `hack` on learner code need a runtime.
- **Generator:** yes, for stress inputs; claims and candidates are authored.

### 7.19 `problem-workbench`: Problem workbench

**Composite · P1 · W-B1; interview mode P2 · W-D.** The practice surface for the 150 problems and for contests. It scaffolds the method interviewers look for, then fades the scaffolding: understand, examples, approach, code, test, submit, reflect.

- **Serves:** 1.8.5 L15 to L17; every 1.8 practice set; the 1.8 exit (150 problems; a fresh medium in 30 minutes); 2.4.1 L2, L4, L8, L12; 3.3 coding interviews (developer track).
- **Uses:** `code-cell`, `speed-timer`, `choice` (pattern and target complexity), `free-response` (restatement, plan, reflection), `value-table` (the examples table), `token-tray` (pattern chips), `diagnostic-reader`, `counterexample-lab` (stress a failing submission), `code-annotator` (the editorial after solving).
- **Stages:**
  1. Understand: restate the problem; inputs, outputs and constraints.
  2. Examples: add your own cases, including edge cases; the reference answers each one (live where a runtime exists; otherwise for a pre-computed list of suggested edge cases).
  3. Approach: choose the pattern or patterns, write a plan, choose the target complexity.
  4. Code, in `code-cell`.
  5. Test against the examples and your own cases.
  6. Submit to the hidden suite, including efficiency tests.
  7. Reflect: time and space complexity in words (rubric, with Bertie's draft mark), and a mistake tag (off-by-one, edge case, wrong pattern, too slow).
- **Modes:** `guided` (all stages, hints on), `practice` (stages optional), `timed` (a 30-minute clock, hints off; held-out problems for the exit), `contest` (Codeforces-style statement with stdin and stdout and several test cases; Python or C++), `interview` (P2: Bertie plays the interviewer, asks clarifying questions, asks for complexity and gives hints by rung; the learner thinks aloud in typed text; feedback against a rubric).
- **Interactions.** Move between stages with the rail or Next and Back; add rows to the examples table; tap pattern chips; code and test in `code-cell`; Submit; write the reflection; in timed mode, the clock runs from the first keystroke in stage 4 or after 3 minutes, whichever is first [our choice].
- **Keyboard:** Alt + Left and Alt + Right move between stages; the rail is a list of links; the examples table uses grid keys; chips follow `token-tray` keys; `code-cell` keys apply in stage 4.
- **State:** `{ stage: number, restatement?: string, cases: { input: string; expected?: string }[], patterns: string[], plan?: string, complexity?: string, submissions: { at: number; passed: number; total: number }[], reflection?: string, tags: string[], timer?: { startedAt: number } }`.
- **Answers:** `code` (the submission), `text` (reflection), `choice` (pattern, complexity).
- **Config:** `{ problem: { id: string; title: string; difficulty: 'easy' | 'medium' | 'hard'; statement: string; constraints: string; patterns: string[]; heldOut?: boolean }; cell: CodeCellConfig; mode: string; edgeCases?: { input: string; expected: string }[]; editorial?: CodeAnnotatorConfig; timeLimitMin?: number }`.
- **Visual:** a stage rail across the top (numbered steps with words); the active stage's panel below; the timer in the speed token in timed mode.
- **Motion:** stage changes cross-fade over 200 ms.
- **Reduced motion:** cut.
- **Accessibility:** the stage rail is a list of links with status words; the timer follows `speed-timer`'s rules.
- **Tutor:** describe: "Problem 'Top K Frequent Elements' (medium), stage 4 code. Patterns chosen: heap. Target O(n log k). Last run: 2 of 3 examples." Ids: `stage:<n>`, `case:<k>`, plus `code-cell` ids.
- **Performance:** as `code-cell`.
- **Artifact / web:** as `code-cell`; the solved-problem ledger syncs through `db`.
- **Generator:** test inputs only; problems are authored (150 or more for practice, plus at least 30 held-out mediums).

---

## 8. Composites: C++ (1.9)

Most of 1.9 runs on widgets already specified, in C++ modes. Three ideas need their own composites: the build pipeline, memory layout, and ownership.

| Widget | C++ mode | Priority |
|---|---|---|
| `code-cell` | `language: 'cpp'`, multi-file (`.h`, `.cpp`, `test.cpp`), doctest suites, flags panel, local paste verification | P1 |
| `code-tracer` | the C++ renderer (section 4.2) with authored, CI-verified traces | P1 |
| `diagnostic-reader` | `gcc`, `clang`, `linker`, `asan`, `ubsan` formats | P1 |
| `predict-output` | `language: 'cpp'`, including `compiles` predictions | P1 |
| `bench-lab` | `rigorous` and `profile` modes; the 1.9 exit timing | P1 |
| `dynamic-array` | `cpp` mode (capacity, `reserve`, iterator invalidation) | P1 |
| `bit-lab` | `cpp` mode (fixed widths, wrap-around, undefined signed overflow, promotion) | P1 |
| `sort-lab` | `comparator` mode (strict weak ordering) | P1 |
| `binary-search-lab` | `cpp` mode (overflow-safe midpoint) | P1 |
| `setup-checklist` | C++ toolchain and the 1.9 exit (section 6.11) | P1 |

**The `cpp-runner` spike (first task of W-C)** [our choice; every figure here is a budget to test, not a measurement]:

- Candidate: Clang compiled to WebAssembly with a WASI sysroot and libc++, in the line of Ben Smith's wasm-clang demonstration and the YoWASP Clang packages [sourced, recalled; sizes and C++20 support unverified].
- Pass criteria on the reference device: cached download of 60 MB or less; a 100-line program with `<vector>`, `<iostream>` and doctest compiles and runs cold in 20 s or less and warm in 5 s or less; C++20 accepted.
- Known gap: AddressSanitizer is not expected to work for a WASI target [unverified], so sanitizer lessons use recorded reports and local runs.
- **If the spike fails:** the web proxy forwards compile-and-run requests to Compiler Explorer's public API with execution enabled [sourced, recalled API shape; its terms for automated personal use must be confirmed before build], rate-limited to one request every 3 s, sending only the learner's code. C++ drills are then online-only on the web.
- **Always available:** local compilation with pasted output, because the 1.9 exit needs native timing anyway.
- **Test framework** [our choice]: doctest (single header, fast to compile, MIT licence). GoogleTest is the industry default but needs a build step and linking; one lesson names it.
- **Language standard** [our choice]: C++20, compiled with `-std=c++20 -Wall -Wextra -O2`; sanitizer lessons add `-fsanitize=address,undefined -g -O1`.

### 8.1 `compile-pipeline`: Compile pipeline

**Composite · P1 · W-C.** From source to program: the preprocessor expands includes and macros into a translation unit, the compiler turns each unit into an object file with defined and undefined symbols, and the linker joins objects and libraries. Also headers against sources, include guards, the one-definition rule, and incremental builds with Make or CMake.

- **Serves:** 1.9.1 L1, L2, L7 to L9; 1.9.3 L8 (flags).
- **Uses:** `node-link` (layered lanes: sources, preprocessor, compiler, linker, executable; the build dependency DAG), `token-tray` (files moved through stages; flags), `code-surface` (sources, expanded output, `nm` symbol listings), `diagnostic-reader` (errors), `value-table` (symbol tables).
- **Data:** recorded at build time with pinned GCC and Clang: expanded line counts (`g++ -E | wc -l`), symbol tables (`nm`), and every error message shown.
- **Modes:** `stages` (move files through; match an error message to the stage that raised it), `multi-file` (split a program into header and source; a function defined in a header included twice gives "multiple definition", fixed by `inline` or moving the definition), `build-graph` (edit a header and tap every object that must rebuild; timestamps shown), `flags` (what `-O2`, `-g`, `-Wall -Wextra`, `-std=c++20` and the sanitizers change), `cmake` (a minimal `CMakeLists.txt`: `add_executable`, `add_library`, `target_link_libraries`, `enable_testing`, `add_test`).
- **Interactions.** Drag files through stages; tap a symbol to follow it from "undefined" in one object to "defined" in another; tap objects to rebuild; drag flags onto the command.
- **Keyboard:** Files and flags follow `token-tray` keys; B builds; in symbol tables, Up and Down move and Enter follows a symbol to its definition; Space marks an object to rebuild.
- **State:** `{ mode: string, placements: Record<string, string>, tapped: string[], flags: string[] }`.
- **Answers:** `ordering`, `mapping` (error to stage), `set` (objects to rebuild; undefined symbols).
- **Config:** `{ mode: string; files: { path: string; source: string }[]; recorded: { expandedLines?: Record<string, number>; symbols?: Record<string, { defined: string[]; undefined: string[] }>; errors?: { stage: string; text: string }[] }; deps?: [string, string][]; edited?: string }`.
- **Visual:** lanes as columns with headers; files as chips; the translation unit's size as a bar ("iostream adds 34,000 lines" from the recorded count, never a remembered one); undefined symbols in muted italics, defined in ink.
- **Motion:** files move between lanes over 300 ms as a consequence of Build or a drag.
- **Reduced motion:** cuts.
- **Accessibility:** lanes as lists; symbols as tables; errors through `diagnostic-reader`.
- **Tutor:** describe: "3 sources, 2 headers. Linker stage: undefined reference to price(double) in main.o; defined nowhere." Ids: `file:<path>`, `stage:<name>`, `sym:<name>`, `obj:<path>`.
- **Performance:** trivial.
- **Artifact / web:** identical (all recorded).
- **Generator:** yes. Random include DAGs with "which objects rebuild" questions; error-to-stage items drawn from the recorded bank.

### 8.2 `memory-layout`: Memory layout

**Composite · P1 · W-C.** What objects look like in bytes: type sizes, alignment and padding, field order, endianness, arrays and address arithmetic, contiguous values against pointers to scattered objects, and cache lines.

- **Serves:** 1.9.1 L3; 1.9.2 L3, L11; 1.9.3 L5; 1.1.2 L1 by back-reference (P1 Python mode).
- **Uses:** `array-strip` (bytes mode with addresses), `token-tray` (reorder fields), `live-formula` (`sizeof`, `alignof`, offsets), `cell-grid` (a 2D array with 64-byte cache lines), `node-link` (pointer chasing).
- **ABI** [our choice]: x86-64 System V (LP64): `char` 1, `short` 2, `int` 4, `long` 8, `long long` 8, `float` 4, `double` 8, pointers 8, `bool` 1. One note covers Windows (LLP64), where `long` is 4 bytes.
- **Modes:** `sizes`, `struct` (drag fields to reorder; `sizeof` and padding update; the challenge is the smallest size, usually reached by decreasing alignment), `endian` (the bytes of an `int` in little-endian order), `array` (`&a[i]` equals base plus $i \cdot$ `sizeof(T)`), `pointers` (`std::vector<T>` against `std::vector<T*>`), `cache` (count cache lines loaded when a $1024 \times 1024$ `double` matrix is traversed by rows and by columns), `python` (P1: a list of floats is an array of pointers to separate float objects; a NumPy array is contiguous 8-byte doubles; sizes recorded from `sys.getsizeof`).
- **Interactions.** Drag fields; tap a byte to see which field owns it; switch traversal order; step the traversal and watch lines load.
- **Keyboard:** Fields follow `token-tray` keys (Up and Down move a field); in the byte strip, arrows move by byte; T toggles traversal order and N steps it.
- **State:** `{ mode: string, fields: string[], order: 'row' | 'column', loaded: number }`.
- **Answers:** `numeric` (`sizeof`, an offset, lines loaded), `state` (`minimalPadding`), `choice`.
- **Config:** `{ mode: string; struct?: { name: string; fields: { name: string; type: string }[] }; matrix?: { rows: number; cols: number; elem: number }; line?: number }`.
- **Visual:** bytes as narrow cells with addresses every 8 bytes; fields as bands in slots s2 to s6 with direct labels; padding hatched and labelled "padding"; cache lines as alternating bands with loaded lines "done".
- **Motion:** reordering slides fields over 200 ms; traversal steps are consequences of Step or Play.
- **Reduced motion:** cuts.
- **Accessibility:** a table of field, offset, size and alignment, plus total padding.
- **Tutor:** describe: "struct Quote { char side; double px; int qty; }: offsets 0, 8, 16; size 24; padding 11 bytes." Ids: `field:<name>`, `byte:<i>`, `line:<k>`.
- **Performance:** cache traversal uses counted lines, not per-element animation, above 4,096 elements.
- **Artifact / web:** identical.
- **Generator:** yes. Random structs with offset and size questions; traversal counts.

### 8.3 `ownership-lab`: Ownership lab

**Composite · P1 · W-C.** Who owns a resource and when it is released: raw `new` and `delete`, RAII, copying against moving, the rules of zero, three and five, `unique_ptr`, `shared_ptr` counts and cycles, and `weak_ptr`. The learner applies operations to a memory diagram and predicts the result.

- **Serves:** 1.9.2 L5, L7 to L10; 1.9.3 L1 (vectors of `unique_ptr`).
- **Uses:** `node-link` (heap layout: owners in frames on the left, heap blocks and control blocks on the right), `token-tray` (operations), `value-table` (the destructor log), `diagnostic-reader` (the sanitizer report for a double free), `code-surface` (the equivalent C++ for each operation).
- **Operations:** copy-construct, copy-assign, move-construct (`std::move`), move-assign, `reset`, `release`, `make_unique`, `make_shared`, assign `nullptr`, end of scope (locals destroyed in reverse order of declaration), `throw` (unwinding), `weak_ptr::lock`.
- **Modes:** `raw`, `raii`, `copy`, `move` (the moved-from object is "valid but unspecified", drawn hollow), `unique` (copying is a compile error, shown through `diagnostic-reader`), `shared` (strong and weak counts on the control block; a cycle leaks), `vector` (a vector of `unique_ptr` moving its elements on reallocation).
- **Interactions.** Choose an operation, then its target or targets; predict the state (draw arrows, type counts) before applying; order the destructor calls.
- **Show-why:** `leak` (blocks nothing owns are framed "leaked"), `double-free` (two owners delete one block; the second delete is marked and the recorded sanitizer report opens), `cycle` (after scope exit the two counts stay at 1).
- **Keyboard:** Operation chips follow `token-tray` keys; targets are chosen with `node-link`'s arrow path; counts are numeric fields; the destructor order is a `token-tray` list.
- **State:** `{ owners: { id: string; kind: string; target: string | null; frame: string }[], blocks: { id: string; strong?: number; weak?: number; alive: boolean }[], log: string[] }`.
- **Answers:** `state` (`ownershipState`), `numeric` (`use_count`), `ordering` (destructor order), `choice`.
- **Config:** `{ mode: string; start: { owners: unknown[]; blocks: unknown[] }; ops?: string[]; predictAfter?: number[]; program: string }`.
- **Data:** every authored scenario ships with its C++ program; CI compiles and runs it with sanitizers and checks the destructor log against the widget's.
- **Visual:** owner kinds labelled ("unique_ptr p", "raw q"); control blocks show "strong 2, weak 1"; leaked blocks hatched with the label; moved-from owners hollow with the label "moved-from".
- **Motion:** arrows transfer between owners over 300 ms; destroyed blocks fade over 200 ms.
- **Reduced motion:** cuts.
- **Accessibility:** owners and blocks as a table; each operation's effect announced ("p moved to q; p is now empty; block A owned by q").
- **Tutor:** describe: "Owners: shared_ptr a, b to block X (strong 2); weak_ptr w to X. Next: end of scope f." Ids: `owner:<id>`, `block:<id>`, `ctrl:<id>`, `op:<k>`.
- **Performance:** trivial.
- **Artifact / web:** identical (scenarios recorded).
- **Generator:** yes. Seeded operation sequences over a fixed set of owners, with predictions; each generated sequence is also emitted as C++ and checked in CI.

---

## 9. Composites: contests (2.4)

Contest practice reuses `problem-workbench` (contest mode), `code-cell`, `counterexample-lab` (stress and hack), `range-query-lab`, `bit-lab` and the graph composites. Two widgets are new.

**Problem content** [our choice]: contest problems are written originally in Codeforces style. Codeforces statements are copyrighted by their authors, so the app links to them for real practice and never copies them.

### 9.1 `contest-arena`: Contest arena

**Composite · P2 · W-D.** A virtual contest: a problem set under a clock, verdicts per submission, a scoreboard, an optional hacking phase, then editorials and an upsolve list.

- **Serves:** 2.4.1 L1, L12; the developer track's contest habit; 3.3 timed practice.
- **Uses:** `problem-workbench` (contest mode, one per problem), `code-cell`, `speed-timer`, `value-table` (scoreboard), `counterexample-lab` (hack mode), `code-annotator` (editorials).
- **Scoring:** Codeforces-style (points fall with time, a penalty per rejected submission) or ICPC-style (problems solved, then penalty minutes).
- **Verdicts:** Accepted; Wrong answer on test $k$; Time limit exceeded on test $k$; Runtime error; Compilation error. Memory limits are not modelled [our choice: Pyodide cannot measure them faithfully].
- **Fair time limits:** a calibration benchmark at the start measures the device; Python time limits scale by it, as judges multiply limits for Python [our choice; Pyodide's speed relative to native CPython is unverified].
- **Scoreboard:** "simulated rivals" whose solve times come from a seeded model of rating against problem difficulty, always labelled as simulated. After the contest, a performance estimate labelled "estimate, not a Codeforces rating".
- **Tour mode:** a finished contest replayed with commentary (2.4.1 L1).
- **Interactions.** Open a problem; submit; read verdicts; in the hacking phase, open a rival's (authored) submission and hack it; after the end, read editorials and add problems to the upsolve list (the Redo queue).
- **Keyboard:** The problem list is a list of links (keys A to F jump to a problem); `problem-workbench` and `code-cell` keys apply inside a problem; the scoreboard is a table.
- **State:** `{ startedAt: number, durationMs: number, submissions: { problem: string; at: number; verdict: string; test?: number }[], hacks: { target: string; ok: boolean }[], upsolve: string[] }`.
- **Answers:** `code` (per problem, through each problem's suite); `state`.
- **Config:** `{ problems: ProblemWorkbenchConfig[]; scoring: 'cf' | 'icpc'; durationMin: number; rivals: { count: number; seed: number }; hacking?: boolean; calibrate?: boolean }`.
- **Visual:** a problem list A to F with status words and icons; the scoreboard as a table with the learner's row tinted as Brilliant tints the current user in leagues (design research 2.4).
- **Motion:** scoreboard rows reorder over 300 ms when scores change.
- **Reduced motion:** cuts.
- **Accessibility:** the timer follows `speed-timer`; verdicts announced; the scoreboard is a table.
- **Tutor:** off during the contest (exam rules); on for editorials and upsolving.
- **Performance:** as `code-cell`; judging runs one submission at a time.
- **Artifact / web:** Python problems in the Artifact only if WebAssembly is allowed; C++ on the web.
- **Generator:** yes, for rival scoreboards and test inputs; problems are authored.

### 9.2 `number-theory-lab`: Number theory lab

**Composite · P2 · W-D.** The number theory contests use: the sieve, Euclid's algorithm as cutting squares from a rectangle, the extended algorithm and modular inverses, fast modular powers, modular arithmetic with negative numbers in Python and C++, and $\binom{n}{k} \bmod p$ from factorial tables.

- **Serves:** 2.4.1 L6; Project Euler items in 2.4.1 L13.
- **Uses:** `cell-grid` (the sieve), `plot-2d` with `marks` (the rectangle tiling), `value-table` (Euclid's steps and back-substitution), `live-formula`, `bit-lab` (power mode), `modular-clock` and `factor-tree` (Stage 0).
- **Modes:** `sieve` (cross out multiples of each prime from $p^2$; stop at $\sqrt{N}$), `euclid` (an $a \times b$ rectangle: remove the largest squares; the last square's side is $\gcd(a, b)$), `extended` (Bezout coefficients; inverses modulo $m$), `modpow`, `clock` (`-7 % 3` is 2 in Python and `-7 % 3` is -1 in C++), `ncr` (factorials and inverse factorials modulo a prime by Fermat's little theorem), `divisors`.
- **Interactions.** Tap primes to cross out their multiples; drag cuts in the rectangle; fill the table rows.
- **Keyboard:** The sieve uses `cell-grid` keys and Space crosses out the focused prime's multiples; in the rectangle, C cuts the largest square; table rows are numeric fields.
- **State:** `{ mode: string, crossed: number[], cuts: number[], rows: string[][] }`.
- **Answers:** `numeric`, `state`, `set`.
- **Config:** `{ mode: string; n?: number; a?: number; b?: number; m?: number; p?: number; k?: number }`.
- **Visual:** crossed cells "ruled out"; primes "done"; squares in the tiling in alternating slots with side lengths labelled.
- **Motion:** crossing a prime's multiples sweeps across the grid over 400 ms as a consequence of the tap.
- **Reduced motion:** cuts.
- **Accessibility:** "Crossed out multiples of 3 from 9: 9, 12, 15, ...; 25 primes below 100".
- **Tutor:** describe: "Sieve to 100: primes 2, 3, 5 done; next uncrossed 7." Ids: `cell:<n>`, `square:<k>`, `row:<k>`.
- **Performance:** sieve grids up to 1,000 cells in SVG.
- **Artifact / web:** identical.
- **Generator:** yes. Ranges, pairs, moduli, $n$ and $k$.

---

## 10. Screens built from primitives alone

These lesson screens need no composite. Each is a configuration of primitives, with data recorded at build time where code is involved.

| Screen | Lessons | Primitives | Check |
|---|---|---|---|
| Bind call arguments to parameters, including defaults, keywords, `*args` and `**kwargs` | 1.1.1 L9, L10 | `code-surface` (read), `token-tray` (arguments into parameter slots) | `mapping` |
| Integer division and modulo with negatives as floor jumps | 1.1.1 L2; 2.4.1 L6 | `number-line` (Stage 0), `numeric-input` | `numeric` |
| Operator precedence and evaluation order in Python | 1.1.1 L7 | `expression-tree` (Stage 0, Python mode) | `ordering` |
| Three-valued logic: fill the truth table for `TRUE`, `FALSE` and `NULL` | 1.2.3 L4 | `value-table` with `region-select` cycling three states | `set` |
| Fixture setup and teardown order | 1.2.4 L7 | `node-link` (layered fixture DAG), `stepper` over recorded `pytest --setup-show` output, `token-tray` (predicted order) | `ordering` |
| Binning with `cut` against `qcut` | 1.1.3 L14 | `number-line`, `marks` (bars), `numeric-input` | `numeric` |
| Pattern picker: which technique fits this statement | 1.8 practice | `choice` with pattern chips; items generated from the problem bank's tags | `choice` |
| Matrix rotation, spiral order, set zeroes | 1.8.5 L14 | `cell-grid`, `stepper` | `state` |
| Greedy scans: jump game, gas station, partition labels | 1.8.5 L12 | `array-strip` (markers), `stepper`, `numeric-input` | `numeric` |
| Which container for this workload | 1.9.3 L2 | `choice`, `value-table` (operation costs) | `choice` |
| Template instantiation | 1.9.3 L4 | two `code-surface`s side by side (the template and what the compiler generates for `int` and `double`), `choice` | `choice` |
| Exceptions against error codes | 1.9.2 L14 | `choice`, `free-response` | `choice`, `text` |
| Commit messages that explain why | 1.2.2 L1 | `free-response` with a rubric, Bertie's draft mark | `text` |

---

## 11. Generators

### 11.1 Contract

Generators follow Stage 0's contract (its section 12: a pure `generate(rng, difficulty)` with an independent `solve`, CI over 1,000 seeds per difficulty, distinct distractors from named misconceptions, at least 4 surface variants per family) with three additions:

```ts
interface GeneratorAdditions {
  runtime: 'js' | 'python' | 'sql' | 'cpp';     // what is needed to compute the item's answer
  parity?: 'numpy' | 'pandas' | 'python' | 're' | 'git' | 'sqlite';   // the real system CI compares against
  bank?: { size: number };                        // seed-bank size when runtime is not 'js' (default 200 per difficulty)
}
```

- **`runtime: 'js'`** items (algorithm instances, NumPy and pandas visuals, Git puzzles, bits, regex sets) generate on any device. CI checks each family against its `parity` system: `algo-trace` against the Python source under the recorder, `nd-core` against NumPy, `frame-core` against pandas, the regex translation against `re`, `git-model` against real Git (with `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` fixed so hashes compare), and the glob matcher against `git check-ignore`.
- **Other runtimes** (predicting Python output, SQL results, C++ compiler messages) generate live on the web when the runtime is present, and come from a seed bank precomputed in CI otherwise. The bank stores the full item, so the Artifact needs no runtime to grade it.
- **Seed policy** as Stage 0: the same seed for the Redo queue; fresh seeds for practice; fixed per learner and level for homework; fixed per sitting for exams.

### 11.2 Families by widget

| Widget | Families | Key constraints |
|---|---|---|
| `code-tracer` | aliasing; shallow and deep copies; mutable defaults; closures and late binding; scope and `UnboundLocalError`; generator exhaustion | at most 12 lines; at most 8 objects; names from a rotating vocabulary |
| `predict-output` | integer division and modulo; slicing; string methods; comprehension order; dict and set behaviour; stable sorts; NumPy dtypes; pandas alignment; SQL `NULL` counts; C++ conversions | outputs at most 6 lines; each family seeds 3 misconception distractors |
| `parsons` | auto-Parsons from any reference; algorithm skeletons | 4 to 12 lines; at most 3 distractors; accepted orders computed in CI |
| `code-blanks` | slices for a target output; conditions; format specs; SQL `WHERE` clauses; binary-search updates | at most 4 slots; at most 512 palette combinations |
| `diagnostic-reader` | `IndexError` off by one; `KeyError`; `TypeError` from `None`; `AttributeError`; division by zero; module shadowing | reports captured in CI; at most 6 frames |
| `float-inspector` | nearest double; gap at a magnitude; comparison truth; summation order; `Decimal` rounding | magnitudes from $10^{-8}$ to $10^{17}$ |
| `format-lab` | numbers to targets; percentages; alignment; dates | specs from the documented mini-language only |
| `json-explorer` | path to value; value at path; collect | depth up to 4; breadth up to 5 |
| `search-path` | which binary or module wins; reorder to a goal; shadowing | at most 6 directories |
| `pipeline-flow` | shell goals over logs and CSVs; clause order; iterator predictions; pandas chains | goals reachable in 5 stages or fewer |
| `regex-lab` | golf sets; predict matches; groups; gitignore rules | a reference pattern of 40 characters or fewer exists; strings 30 characters or fewer |
| `hash-table` | predict bucket; probe counts; resize point; collisions | $m$ up to 16 at difficulty 3 or below |
| `ndarray-lab` | slice to cells; cells to slice; reduction shapes; view or copy; dtypes | up to 3 dimensions; each axis up to 6 |
| `broadcast-lab` | result shape; compatible or not; fix with `None`; matmul shapes | 30% incompatible pairs at difficulty 2 and above |
| `dataframe-lab` | selection to expression and back; filters; alignment; missing data | frames up to $12 \times 5$ |
| `groupby-lab` | group membership; aggregates; `agg` against `transform`; window functions; the leak trap | up to 4 groups; up to 20 rows |
| `join-lab` | row counts; result rows; NULL and NaN keys | up to 8 rows a side; at most 2 duplicate keys |
| `reshape-lab` | slot assignment; output shape; follow a cell | up to 3 index or column fields |
| `time-series-lab` | shift and returns; resample labels; window positions; time-zone conversions | 20 to 60 trading days; real daylight-saving dates |
| `csv-inspector` | find broken cells; choose options; write the call | messiness from the `price-series` list |
| `drawdown-lab` | maximum drawdown; volatility; total return | 1 to 3 planted drawdowns of 5% to 40% |
| `plot-workbench` | fix a chart | one or two seeded defects per chart |
| `bench-lab` | speed-up arithmetic; reading spreads | ratios from recorded runs |
| `git-graph` | reach a goal graph; three-tree states; reset outcomes; bisect | par of 6 commands or fewer, found by search in CI |
| `merge-conflict` | resolve; predict conflicts; semantic conflicts | at most 3 hunks |
| `code-review` | seeded defects in clean code | 2 to 4 defects; at least 1 must-find |
| `permission-bits` | octal and symbolic; diagnoses | standard modes only |
| `injection-lab` | contexts: string, number, `LIKE`, identifier | one-line templates |
| `schema-builder` | normalise a wide sheet | up to 10 columns; up to 3 tables |
| `vim-sim` | edit to a target | par of 12 keystrokes or fewer |
| `complexity-lab` | loop snippets; rankings; crossovers; budgets | closed-form counts checked by `cas` |
| `sort-lab` | inputs by family; key tasks; stability puzzles | up to 12 items for `be` mode |
| `dynamic-array` | appends to reallocation; total copies | factors 1.25, 1.5, 2 |
| `pointer-walk` | per mode inputs | exactly one or no valid answer where a single answer is asked for |
| `range-query-lab` | queries and updates | arrays up to 16 |
| `binary-search-lab` | targets present and absent; duplicates; predicates; rotations | arrays up to 32 |
| `stack-queue-lab` | brackets; RPN; temperatures; histograms | lengths up to 14 |
| `linked-list-lab` | operation sequences; cycles; LRU traces | up to 10 nodes |
| `interval-sweep` | per mode sets | up to 10 intervals; unique optimum where asked |
| `bit-lab` | conversions; masks; tricks; overflow; fast power | widths 4 to 32 at difficulty 3 or below |
| `tree-lab` | traversals; BST operations; construction; tries | up to 31 nodes |
| `heap-lab` | operations; heapify; streams | up to 15 nodes |
| `graph-search` | BFS and DFS orders; components; topological orders; bipartite checks | 6 to 15 nodes; geometric layouts |
| `shortest-path` | distances; settle order; minimum spanning trees | positive integer weights up to 20; distinct weights for MST items |
| `union-find` | operation sequences; redundant edge | up to 12 elements |
| `recursion-tree` | call counts; pruning; recurrences | trees up to 60 nodes |
| `dp-table` | fills; paths; recurrences | tables up to $9 \times 9$ |
| `compile-pipeline` | rebuild sets; error to stage | include DAGs up to 8 files |
| `memory-layout` | sizes; offsets; reordering; cache lines | up to 6 fields |
| `ownership-lab` | operation sequences with predictions | up to 4 owners and 3 blocks; each emitted as C++ and checked |
| `number-theory-lab` | sieve; gcd; inverses; powers; $\binom{n}{k} \bmod p$ | $N$ up to 200; moduli up to 97 |

**Seeds that vary authored items:** `code-cell` (test inputs and data files), `mutant-hunter` (which mutants appear), `counterexample-lab` (stress inputs), `problem-workbench` (test inputs), `contest-arena` (rival scoreboards and test inputs); among the extended Stage 0 widgets, `workspace-sim` and `setup-checklist` (the exit CSV).

**Totals.** 51 new widgets have item generators; 5 more use seeds only to vary authored items. `shell-sim` gains families on top of Stage 0's.

---

## 12. Build order

The waves follow the depth-first lesson order. W-A1 starts once Stage 0's W2 has delivered `code-surface`, `text-terminal`, `file-tree`, `shell-sim`, `workspace-sim`, `setup-checklist` and the `vfs` and `python-runner` services. In `widgets-calc-linalg.md` terms, W-A1 to W-A3 are the 1.1 and 1.2 part of its wave A, and they finish before its wave B.

| Wave | Priority | Needed by | Widgets and services |
|---|---|---|---|
| W-A1 | P0 | 1.1.1 Python foundations | `diff-view`, `array-strip`, `node-link`; `code-surface` and `stepper` extensions; services `trace-recorder`, `code-lex`, `algo-trace` (core, sorting, hashing), `seed-bank`, `handoff`, `python-runner` additions; `code-cell`, `code-tracer` (Python), `predict-output`, `parsons`, `code-blanks`, `code-annotator`, `diagnostic-reader` (Python), `float-inspector`, `format-lab`, `json-explorer`, `search-path`, `pipeline-flow` (iter), `regex-lab`, `hash-table` (basic), `complexity-lab` (growth, race, code), `sort-lab` (key), `csv-inspector` (csv module). **Spikes:** Pyodide cold start and package loading on the reference device; complexity-test noise; MicroPython compatibility tagging and `sys.settrace` |
| W-A2 | P0 | 1.1.2 to 1.1.4 | `cell-grid`; `value-table` frame mode; services `nd-core`, `frame-core`, `price-series`; `ndarray-lab`, `broadcast-lab`, `dataframe-lab`, `groupby-lab` (pandas), `join-lab` (pandas), `reshape-lab`, `time-series-lab`, `csv-inspector` (pandas), `drawdown-lab`, `plot-workbench`, `bench-lab` (race), `pipeline-flow` (pandas) |
| W-A3 | P0 | 1.2 | `text-terminal` extension; services `git-model`, `sql-runner`, `mutant-forge`, `shell-interpreter` additions; `git-graph`, `merge-conflict`, `code-review`, `permission-bits`, `injection-lab`, `mutant-hunter`, `pipeline-flow` (shell, SQL), `groupby-lab` and `join-lab` (SQL), `diagnostic-reader` (pytest, SQLite, bash, Git); `shell-sim`, `workspace-sim` and `setup-checklist` extensions. **Spike:** pytest and Hypothesis inside Pyodide |
| W-B1 | P1 | 1.8.1 to 1.8.3, method | full `complexity-lab`, `sort-lab` and `hash-table`; `dynamic-array`, `pointer-walk`, `range-query-lab` (prefix family), `binary-search-lab`, `stack-queue-lab`, `linked-list-lab`, `heap-lab`, `interval-sweep`, `bit-lab`, `counterexample-lab`, `problem-workbench`; `regex-lab` step mode; `mutant-hunter` coverage and property modes |
| W-B2 | P1 | 1.8.4, 1.8.5 | `tree-lab`, `graph-search`, `shortest-path`, `union-find`, `recursion-tree`, `dp-table` |
| W-C | P1 | 1.9; optional 1.2 lessons | **`cpp-runner` spike first**; `code-cell` C++; `code-tracer` C++ renderer; `diagnostic-reader` compiler formats; `predict-output` C++; `compile-pipeline`, `memory-layout`, `ownership-lab`; `bench-lab` rigorous and profile; C++ modes of `dynamic-array`, `bit-lab`, `sort-lab`, `binary-search-lab` and `format-lab`; C++ items of `setup-checklist`; `schema-builder`, `vim-sim`; `shell-sim` P1 parts |
| W-D | P2 | 2.4 | `contest-arena`, `number-theory-lab`; `range-query-lab` Fenwick and segment trees; `bit-lab` subsets; `counterexample-lab` hack mode; `problem-workbench` interview mode; `tree-lab` B-tree; `shortest-path` 0-1 BFS |

**Gate per widget** (Stage 0's gate, plus this cluster's):

- the schema validates every example configuration in this file;
- every state round-trips through `getState` and `setState`;
- keyboard and two-tap paths reach every action;
- reduced-motion mode is checked;
- `describe` is snapshot-tested;
- frame budgets hold on the reference device;
- generators pass CI;
- **parity tests pass** for every JavaScript core the widget relies on (section 11.1);
- **runtime tags** are computed for every drill the widget hosts (section 2.10).

---

## 13. Rejected alternatives and open questions

### 13.1 Rejected

| Alternative | Why rejected |
|---|---|
| CodeMirror 6 or Monaco now | Size and a second editing model; the prototype's textarea already works on phones; Monaco does not support mobile browsers. Revisit only on the measured triggers in decision 12 |
| Embedding Python Tutor | It needs an iframe and network access, which the Artifact forbids, and it cannot follow our design tokens or check states. We use its frames-and-objects convention instead |
| Skulpt or Brython as the Artifact's Python | Both run generated JavaScript through `eval` or `Function`; a policy that blocks WebAssembly very likely blocks those too [inferred]; their semantics also differ from CPython |
| Writing our own Python interpreter | Months of work and a permanent second Python whose differences learners would absorb |
| Renaming Pyodide's `python_stdlib.zip` (or a Clang sysroot) to a served extension and loading it through `loadPyodide({ stdLibURL })` | It might work technically [unverified], but it sidesteps the host's served-type allow-list. Not adopted without the platform's explicit confirmation that this use is acceptable |
| isomorphic-git | No rebase, cherry-pick or stash [unverified for its latest release]; a file-system layer we do not need; and it would still need teaching hooks |
| AlaSQL or our own SQL engine | Semantics that differ from SQLite; AlaSQL compiles queries with `Function` |
| Force-directed layout at runtime; Graphviz in WebAssembly | Jitter and non-determinism between steps; an extra 2 MB WebAssembly dependency [estimate] |
| Hand-authored keyframes for algorithms | Error-prone and impossible for random instances |
| Grading efficiency by wall clock alone, or by line counts alone | Device variance; work hidden inside C built-ins (decision 10) |
| Remote judges (Judge0, Codeforces submission) | Network access the Artifact lacks, third-party terms, and accounts the learner does not need for practice |
| GitHub sign-in for pull-request exercises | It would make the app a Class C or D service under the engineering floor for no teaching gain; simulated pull requests plus a read-only public check suffice |
| Venn diagrams for joins | They describe sets of keys, not rows, and hide row multiplication; `join-lab` draws matched rows |
| Pseudocode-only algorithms | Learners interview in Python (and C++ for developer roles); the owner's code-craft skill defaults to Python |
| A separate heap-diagram primitive | Folded into `node-link` as the `heap` layout (decision 11) |
| A JavaScript re-implementation of matplotlib for figure anatomy | matplotlib's own SVG with artist ids is exact and cheaper |
| Live correctness hints in the editor | Turns a drill into a search for the green state (calc-linalg's rule); only syntax errors show as you type |
| Copying Codeforces or LeetCode statements | Copyright; problems are written originally and real platforms are linked |
| Real market data inside the app | Licences are unclear and `yfinance` breaks often (curriculum note); `price-series` is synthetic, and projects fetch real data locally |

### 13.2 Open questions

| # | Question | Status and effect |
|---|---|---|
| 1 | Does the Artifact's policy allow WebAssembly? | Probe running [unverified]. Decides whether Python drills, SQL and live tracing run in the Artifact or hand off; every widget is specified for both outcomes |
| 2 | Is MicroPython's WebAssembly build compiled with `sys.settrace`? | [unverified]. Decides live tracing and the line-budget efficiency probe in the Artifact |
| 3 | ulab and MicroPython standard-library coverage | [unverified]. CI tagging decides drill by drill |
| 4 | pytest and Hypothesis inside Pyodide (capture modes, plugins) | [unverified]. W-A3 spike; fallback is the mini-pytest shim on both targets |
| 5 | Pinned versions: Pyodide, its CPython, NumPy, pandas, matplotlib | To fix in W-A1. Copy-on-write, the string dtype and frequency aliases depend on the pandas pin; CI blocks a version change without content review |
| 6 | Timer noise for the time-ratio probe in Pyodide | [unverified]. W-A1 spike sets `maxTimeRatio` |
| 7 | Pyodide cold start and package loading on the reference device | [unverified]. Decides preload strategy |
| 8 | In-browser Clang size and speed; Compiler Explorer's terms for automated personal use | [unverified]. W-C spike; decides the web C++ path |
| 9 | GitHub REST API: CORS on check runs; unauthenticated rate limits | [unverified]. Only affects the optional repository check on the web |
| 10 | SQLite WebAssembly size; loading it from the Artifact's own files | [unverified size]; own-file fetches are allowed by the platform facts |
| 11 | Can an Artifact anchor open the web app? | [unverified]. Fallback: copyable link |
| 12 | Mark types this cluster needs from the `marks` owner: `icicle`, horizontal interval bars (Gantt), candlesticks | Engine decision; `bench-lab`, `interval-sweep`, `time-series-lab` and `plot-workbench` need them |
| 13 | Tutor transport (page tools or one JSON reply) | Engine decision; widget hooks are identical either way |
| 14 | Design sign-off: diff colours (s3 and s2 washes) and the algorithm state palette | Needed before W-A1 visuals are final |
| 15 | Content scale: 150 or more authored problems with tests, at least 30 held-out mediums, editorials | A content-plan question, not a widget one; `problem-workbench` supports it |
| 16 | The Parsons research citation (Ericson and colleagues, 2017) | [sourced, recalled]; verify before quoting in product copy |

---

## 14. All widgets

Kinds: **primitive** (a building block, also usable alone) and **composite** (assembled from primitives). "(ext)" marks an extension of a widget that another catalogue specifies. Generator: **yes** (item generators), **seeds** (seeds vary authored items), **no**.

| # | Id | Kind | Priority | Wave | Curriculum items | Generator |
|---|---|---|---|---|---|---|
| 1 | `diff-view` | primitive | P0 | W-A1 | 1.1, 1.2.2, 1.2.4, 1.8, 1.9, 2.4 | no |
| 2 | `array-strip` | primitive | P0 | W-A1 | 1.1.1, 1.1.2, 1.8, 1.9, 2.4 | no |
| 3 | `cell-grid` | primitive | P0 | W-A2 | 1.1.2, 1.8, 1.9, 2.4 | no |
| 4 | `node-link` | primitive | P0 | W-A1 | 1.1, 1.2, 1.8, 1.9, 2.4 | no |
| 5 | `code-surface` (ext) | primitive | P0 | W-A1 | 0.4, 1.1, 1.2, 1.8, 1.9, 2.4 | no |
| 6 | `text-terminal` (ext) | primitive | P0 | W-A3 | 1.1, 1.2, 1.9 | no |
| 7 | `stepper` trace mode (ext) | primitive | P0 | W-A1 | 1.1, 1.8, 1.9 | no |
| 8 | `value-table` frame mode (ext) | primitive | P0 | W-A2 | 1.1.3, 1.2.3 | no |
| 9 | `code-cell` | composite | P0 (C++ mode P1) | W-A1 | 0.4, 1.1, 1.2, 1.4 exit, 1.8, 1.9, 2.4 | seeds |
| 10 | `code-tracer` | composite | P0 (C++ renderer P1) | W-A1 | 1.1.1, 1.1.2, 1.8, 1.9 | yes |
| 11 | `predict-output` | composite | P0 (C++ P1) | W-A1 | 1.1, 1.2.1, 1.2.3, 1.8, 1.9 | yes |
| 12 | `parsons` | composite | P0 | W-A1 | 1.1, 1.2, 1.8, 1.9 | yes |
| 13 | `code-blanks` | composite | P0 | W-A1 | 1.1, 1.2, 1.8, 1.9 | yes |
| 14 | `code-annotator` | composite | P0 | W-A1 | 1.1, 1.2, 1.8, 1.9 | no |
| 15 | `diagnostic-reader` | composite | P0 (compiler formats P1) | W-A1 | 1.1, 1.2, 1.9 | yes |
| 16 | `float-inspector` | composite | P0 | W-A1 | 1.1.1, 1.1.2, 1.2.4, 1.9.4 | yes |
| 17 | `format-lab` | composite | P0 (C++ P1) | W-A1 | 1.1, 1.9 | yes |
| 18 | `json-explorer` | composite | P0 | W-A1 | 1.1 | yes |
| 19 | `search-path` | composite | P0 | W-A1 | 1.1.1, 1.2.1 | yes |
| 20 | `pipeline-flow` | composite | P0 | W-A1 to W-A3 | 1.1.1, 1.1.3, 1.2.1, 1.2.3 | yes |
| 21 | `regex-lab` | composite | P0 (step mode P1) | W-A1 | 1.1.1, 1.2.1, 1.2.2 | yes |
| 22 | `hash-table` | composite | P0 (full P1) | W-A1 | 1.1.1, 1.8.2, 1.8.3, 1.9.3 | yes |
| 23 | `ndarray-lab` | composite | P0 | W-A2 | 1.1.2, 1.1.3 | yes |
| 24 | `broadcast-lab` | composite | P0 | W-A2 | 1.1.2 | yes |
| 25 | `dataframe-lab` | composite | P0 | W-A2 | 1.1.3 | yes |
| 26 | `groupby-lab` | composite | P0 | W-A2, W-A3 | 1.1.3, 1.2.3 | yes |
| 27 | `join-lab` | composite | P0 | W-A2, W-A3 | 1.1.3, 1.2.3 | yes |
| 28 | `reshape-lab` | composite | P0 | W-A2 | 1.1.3 | yes |
| 29 | `time-series-lab` | composite | P0 | W-A2 | 1.1.3 | yes |
| 30 | `csv-inspector` | composite | P0 | W-A1, W-A2 | 1.1.1, 1.1.3, 1.1 exit | yes |
| 31 | `drawdown-lab` | composite | P0 | W-A2 | 1.1.3, 1.1 exit, 1.7, 2.3 | yes |
| 32 | `plot-workbench` | composite | P0 | W-A2 | 1.1.4, 1.1 exit | yes |
| 33 | `bench-lab` | composite | P0 race (rigorous, profile P1) | W-A2 | 1.1.2, 1.1.3, 1.8.1, 1.9.3, 1.9 exit, 2.4.1 | yes |
| 34 | `git-graph` | composite | P0 | W-A3 | 1.2.2, 1.2.4, 1.2 exit | yes |
| 35 | `merge-conflict` | composite | P0 | W-A3 | 1.2.2 | yes |
| 36 | `code-review` | composite | P0 | W-A3 | 1.2.2, 1.8, 1.9 | yes |
| 37 | `permission-bits` | composite | P0 | W-A3 | 1.2.1 | yes |
| 38 | `injection-lab` | composite | P0 | W-A3 | 1.2.3, 1.2.1 | yes |
| 39 | `mutant-hunter` | composite | P0 (coverage, property P1) | W-A3 | 1.2.4, 1.8 | seeds |
| 40 | `schema-builder` | composite | P1 | W-C | 1.2.3 | yes |
| 41 | `vim-sim` | composite | P1 | W-C | 1.2.1 | yes |
| 42 | `workspace-sim` (ext) | composite | P0 | W-A3 | 1.1 exit, 1.2, 1.2 exit | seeds |
| 43 | `shell-sim` (ext) | composite | P0 (jobs, ssh, sed, awk P1) | W-A3 | 1.2.1, 1.2.2 | yes |
| 44 | `setup-checklist` (ext) | composite | P0 (C++ items P1) | W-A3 | 1.1 exit, 1.2 exit, 1.9 exit | seeds |
| 45 | `complexity-lab` | composite | P0 (budget, timing P1) | W-A1 | 1.1.1, 1.8.1, 1.8.3, 1.9.3, 2.4.1 | yes |
| 46 | `sort-lab` | composite | P0 key mode (algorithms P1) | W-A1 | 1.1.1, 1.1.3, 1.8.2, 1.9.3 | yes |
| 47 | `dynamic-array` | composite | P1 | W-B1 | 1.8.1, 1.8.2, 1.9.3 | yes |
| 48 | `pointer-walk` | composite | P1 | W-B1 | 1.8.2, 1.8.5, 2.4.1 | yes |
| 49 | `range-query-lab` | composite | P1 (Fenwick, segment P2) | W-B1 | 1.8.2, 2.4.1 | yes |
| 50 | `binary-search-lab` | composite | P1 | W-B1 | 1.8.1, 1.8.2, 1.8.5, 2.4.1 | yes |
| 51 | `stack-queue-lab` | composite | P1 | W-B1 | 1.8.2, 1.8.3, 1.8.4 | yes |
| 52 | `linked-list-lab` | composite | P1 | W-B1 | 1.8.3 | yes |
| 53 | `interval-sweep` | composite | P1 | W-B1 | 1.8.2, 1.8.5 | yes |
| 54 | `bit-lab` | composite | P1 (subsets P2) | W-B1 | 1.8.5, 1.9.1, 2.4.1 | yes |
| 55 | `tree-lab` | composite | P1 (B-tree P2) | W-B2 | 1.8.4, 1.9.3, 1.2.3 | yes |
| 56 | `heap-lab` | composite | P1 | W-B1 | 1.8.3, 1.8.4, 1.9.3 | yes |
| 57 | `graph-search` | composite | P1 | W-B2 | 1.8.4, 2.4.1 | yes |
| 58 | `shortest-path` | composite | P1 (0-1 BFS P2) | W-B2 | 1.8.4, 2.4.1 | yes |
| 59 | `union-find` | composite | P1 | W-B2 | 1.8.4, 2.4.1 | yes |
| 60 | `recursion-tree` | composite | P1 | W-B2 | 1.8.1, 1.8.2, 1.8.4, 1.8.5 | yes |
| 61 | `dp-table` | composite | P1 | W-B2 | 1.8.2, 1.8.5, 2.4.1 | yes |
| 62 | `counterexample-lab` | composite | P1 (hack P2) | W-B1 | 1.2.4, 1.8.5, 2.4.1 | seeds |
| 63 | `problem-workbench` | composite | P1 (interview P2) | W-B1 | 1.8.5, 1.8 exit, 2.4.1, 3.3 | seeds |
| 64 | `compile-pipeline` | composite | P1 | W-C | 1.9.1, 1.9.3 | yes |
| 65 | `memory-layout` | composite | P1 | W-C | 1.9.1, 1.9.2, 1.9.3 | yes |
| 66 | `ownership-lab` | composite | P1 | W-C | 1.9.2, 1.9.3 | yes |
| 67 | `contest-arena` | composite | P2 | W-D | 2.4.1, 3.3 | seeds |
| 68 | `number-theory-lab` | composite | P2 | W-D | 2.4.1 | yes |

**Counts.** 68 entries: 61 new (4 primitives, 57 composites) and 7 extensions (4 primitives, 3 composites). By priority: 44 P0, 22 P1, 2 P2.

---

## 15. Cross-cluster needs

### 15.1 Primitives other clusters will need

1. **`node-link`**: probability and decision trees (1.5), Markov chains (1.5, with calc-linalg's `linear-dynamics`), binomial pricing trees (1.7), neural-network and computation graphs (2.1), and the layouts of Stage 0's `tree-diagram`, `factor-tree` and `expression-tree` and calc-linalg's `dependency-graph`, which could all share it.
2. **`cell-grid`**: calc-linalg's `matrix` (recommended to build on it), joint distribution tables (1.5), correlation and covariance heatmaps (1.6, 2.3), confusion matrices (2.1); Stage 0's `outcome-grid` and `times-table-grid` could share its renderer.
3. **`array-strip`**: sequences and sample paths as cells (0.3, 1.5), and the order-book ladder in 1.7 (price levels as a vertical strip with quantities as bars).
4. **`diff-view`**: any before-and-after text: derivation edits, model outputs, regression summaries before and after a change.
5. **`stepper` trace mode**: any long algorithm in other clusters (Gaussian elimination, Gram-Schmidt, backward induction, Newton iterations), recorded once and scrubbed.
6. **`value-table` frame mode**: every dataset in 1.6, 2.1, 2.2 and 2.3; statsmodels summary tables; backtest results.
7. **`code-surface`** (read-addressable) and **`code-cell`**: code in every cluster's lessons and every code drill (the 1.4 exit, the 1.6 regression in NumPy, the 1.7 binomial pricer in Python, 2.1 models, 2.3 projects).

### 15.2 Composites and services other clusters should reuse

| Widget or service | Other uses |
|---|---|
| `float-inspector` | Numerical stability and conditioning in 1.3, 1.4 and 1.6 |
| `drawdown-lab` | 1.7 and 2.3 performance reporting |
| `bench-lab` | Pricer and backtest performance in 1.7 and 2.3 |
| `counterexample-lab` | "Break the claim" items in probability (pairwise against mutual independence) and statistics |
| `pipeline-flow` | Machine-learning pipelines in 2.1 (fit on training data only; a P2 scikit-learn mode would show leakage at each stage) |
| `predict-output`, `parsons`, `code-blanks`, `code-annotator` | Every code-bearing lesson in every cluster |
| `price-series` | Finance (1.7, 2.3), statistics (1.6) and time series (2.2) |
| `trace-recorder`, `algo-trace` | Any algorithm another cluster animates |

### 15.3 What this catalogue needs from other clusters

| Need | Expected owner | Used in |
|---|---|---|
| `marks` types `icicle`, horizontal interval bars, candlesticks | engine (`marks`) | `bench-lab`, `interval-sweep`, `time-series-lab`, `plot-workbench` |
| `matrix-multiply`, `binomial-tree`, `sim-runner`, `path-simulator` | calc-linalg | 1.1.2 L9 and L10; 1.9.4 L1 |
| `number-line`, `stat-chart`, `expression-tree`, `modular-clock`, `factor-tree`, `place-value-chart`, `typing-trainer` (code mode) | Stage 0 | 1.1.1 L2 and L7; 1.1.4 L4; 2.4.1 L6; `bit-lab`; contest typing speed |
| Bertie's transport, face and annotation callouts; the code guard; `handoff`; `db` sync of code drafts and the solved-problem ledger | engine and tutor blueprint | every widget here |
| Market games in the style of IMC Prosperity | finance cluster | 2.4.1 L14 (trader track) |
| Kaggle-style tabular workflow | ML cluster | 2.4.1 L14 (researcher track) |
