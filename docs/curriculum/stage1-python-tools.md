# Stage 1 detailed curriculum: 1.1 Python and 1.2 Tools

Blueprint work file, Stage 2 Phase 1. Draft 2, 6 October 2026.

**Source of truth.** `docs/curriculum.md` for stages, topics, hours and exit tests. This file expands items 1.1 Python (150 h) and 1.2 Tools (40 h) into courses, levels, lessons, homework, exams, reading and verification, rebuilds both exit tests in the app, and writes one lesson in full.

**Built on.** `docs/design-research.md` sections 5, 8, 9 and 10 (lesson anatomy, curriculum architecture, teaching style, critiques); `docs/blueprint/work/widgets-programming.md` (widget ids, runtimes, the `code` check, trace formats; its section 1 is the working outline this file replaces); `docs/CONTENT-FORMAT.md` revision 2 (ids, schema, screen types, checks, tutor fields, element references, drills, verification); `docs/ASSESSMENT.md` draft 2 (assessment ladder, homework and paper rules, the rows `1.1.exit` and `1.2.exit`, earned hours, decision 30 on code items and the two targets); `docs/AI-TUTOR.md` draft 2 (Bertie's gate, code review and the code guard); `docs/BERTIE.md` draft 2 (states and who drives them); `docs/ARCHITECTURE.md` (decision 15, Pyodide on both targets; section 6.3, load groups); `docs/blueprint/work/canon-gap.md` revision 2 (the resource canon and source ids for 1.1 and 1.2, the 2026 Missing Semester); the Stage 0 files `docs/curriculum/stage0-number-algebra.md` and `docs/curriculum/stage0-precalc-computing.md` draft 2 (the final 0.1 to 0.4 lesson lists, which 1.1 and 1.2 extend and do not repeat); `spikes/README.md`; the owner's lesson-creator, maths-teaching, code-craft and project-forge skills.

**Draft 2** keeps every section number, lesson number, id and level code of draft 1, because `ASSESSMENT.md`, `canon-gap.md`, `stage1-linear-algebra.md` (lesson 67), `stage1-probability.md` (level A3, lesson 73) and `stage1-statistics-ts.md` (lessons 63, 93 and 94) cite them. Section 0 lists every change and its reason.

**Tags.** Decisions sit in tables with the rejected alternative and the reason. [measured] marks a behaviour run while writing this draft (section 0.2). [searched] marks a resource detail confirmed by a web search on 6 October 2026. [check] marks a resource detail (a chapter or lecture number, a problem-set name, a URL path) that I recall but could not confirm from this environment, whose network proxy blocked cs50.harvard.edu, missing.csail.mit.edu, sqlbolt.com and wesmckinney.com; confirm it before the content cites it (`checked: false` in `Level.companion` until then). [our choice] marks a design decision without outside evidence. [unverified] marks a platform fact not yet measured.

> **Revised by the `docs/PLAN.md` review, 7 October 2026.** These lines win over the rest of this file where they differ; content agents are briefed from them, and CI enforces them on the lesson files.
>
> | Where | Was | Now |
> |---|---|---|
> | Decision 11, sections 0.2 and 6, project Trade Ledger | CPython 3.11 is the learner floor and the CI interpreter | **CPython 3.12** with `tools/py/uv.lock` (NumPy 2.4.6, pandas 3.0.2, SciPy 1.18.0, matplotlib 3.10.8, the Pyodide pins); SciPy 1.18.0 does not install on 3.11 and the soft deadline needs `sys.monitoring` (`PLAN.md` conflict 19). The 3.11.15 runs recorded in this file stand as records of what was checked on 6 October; the reruns happen at `PLAN.md` stage 26 |
> | Section 0.2 disagreement, lesson 66, `drl.py.lab-float-sum` | Built-in `sum([0.1] * 10**6)` differs between the floor and Pyodide | It no longer differs: CPython 3.12.3 gives `100000.0`, as 3.14 does [measured, 7 October 2026]; the plain loop, Kahan's loop and `math.fsum` comparison is unchanged |
> | Section 6 message table | "float division by zero" (3.11) against "division by zero" (3.14) | Unchanged on the new floor: 3.12.3 still prints "float division by zero" [measured]; the section 6 rule stands: predict-output items that end in an exception ask for its type, never its message |
> | Skills, runtime tags | Sample lessons list 3 or 4 skills in `introduces`; any CI runtime tag | At most 2 skills introduced a lesson, the rest as step tags (`ASSESSMENT.md` 4.1); runtime tags are void, `needs` decides where code runs (`CONTENT-FORMAT.md` decision 18) |

**At a glance.**

| Item | Hours | Courses | Levels | Lessons | Lesson hours | Homework sets | Topic exam | Estimates against hours |
|---|---|---|---|---|---|---|---|---|
| 1.1 Python | 150 | 4 | 19 | 107 | 26.75 (17.8%) | 19 | 90 min, 24 items, 80 marks | 142.25 h (94.8%) |
| 1.2 Tools | 40 | 1 | 7 | 32 | 8.0 (20.0%) | 7 | 60 min, 18 items, 50 marks | 37.5 h (93.75%) |
| Total | 190 | 5 | 26 | 139 | 34.75 | 26 | 2 | 179.75 h |

---

## 0. What draft 2 changed, and why

### 0.1 Changes

| # | Change | Sections | Source |
|---|---|---|---|
| 1 | **Python runs on Pyodide on both targets.** Draft 1 tagged every code screen `micropython-ok`, `ulab-ok` or `web` and sent NumPy and pandas work from the Artifact to the web app. Draft 2 drops the tags: every drill declares `needs` (the packages it imports), and a code item runs wherever the build ships its runtime. The Artifact runs the standard library, NumPy and pandas [sourced: the owner's iPhone, `spikes/README.md`]; matplotlib, SciPy and pytest sit in load groups whose place in the Artifact budget is measured at stage E8 (`ARCHITECTURE.md` 6.3.3) [unverified], and `tzdata` is in no load group yet (section 8, request 9). An item whose `needs` the build does not ship hands off to the web app and comes back by result code | 1.0 decisions 12 and 14, 2.0, 3.0, 3.3, 4, 6 | `ARCHITECTURE.md` decision 15; `ASSESSMENT.md` decision 30 |
| 2 | **A conflict with the brief, resolved by measurement.** The brief says Pyodide cannot run in the Artifact and that WebAssembly there was unmeasured. The spike measured both on the owner's iPhone: every probe passed except service workers, and a repackaged Pyodide loaded NumPy and pandas and computed a drawdown. This file follows the measurement, as every sibling paper now does. The brief's second outcome stays covered: what the Artifact cannot run hands off | 0.2, 2.0 | `spikes/README.md`; `CONTENT-FORMAT.md` 0.3; `ASSESSMENT.md` 0.4 |
| 3 | **Three runtime differences found by running every claim on Pyodide** (section 0.2): WebAssembly has no floating-point status flags, so in the app NumPy gives no overflow, divide or invalid warnings, and `linalg.solve`, `inv` and `cholesky` return `nan` on a singular or indefinite matrix instead of raising `LinAlgError`; Python 3.12 and later compensate rounding in built-in `sum` of floats, so lesson 66's drifting sum now needs a hand-written loop; and one error message and two warnings differ between Python 3.11 and 3.14. Lessons 66 and 67 teach the differences as edge cases (lesson 57's warning on integer scalar overflow still appears in the app, because NumPy checks it in software); no item relies on a floating-point warning or on `LinAlgError`; every authored output is recorded on both runtimes | 2.1 (lessons 34, 35, 66, 67), 3.3, 6, 8 | [measured] |
| 4 | **Overlap with Stage 0 removed.** The final 0.1 to 0.4 lesson lists, written after draft 1, teach 26 ideas that draft 1 also used, among them `//` and `%` with negatives, `int("3.7")`, `a = 1; b = a; a = 2`, `print` against `return`, the `elif` order trap, `range` stopping early, doubling £1,000 at 5%, bottom-up tracebacks, the bare `except`, the terminal basics, PATH, `0.1 + 0.2`, simple against log returns, log underflow, the four counting cases, the $1/\sqrt{n}$ spread and truncated and log axes. Twenty lesson rows (17 in 1.1, 3 in 1.2) change their hook, trap or edge, and homework D4's first example is replaced, so that 1.1 and 1.2 extend Stage 0 and never re-teach it (section 1.0, second table). Lesson numbers and ids are unchanged | 1.0, 2.1, 2.2, 7 | `stage0-precalc-computing.md` 2.2 (0.4 courses B and Y), 2.1 (0.3 lessons 55 to 59, 98 to 123); `stage0-number-algebra.md` (0.1 lesson 42, 0.2 lesson 47) |
| 5 | **Mastered at 75%, 1 mark per quiz item.** A four-item quiz is Mastered at 3 of 4. Draft 1's sample quiz had a 2-mark sort and an 80% bar | 2.0, 7.3 | `ASSESSMENT.md` decision 26; `stage0-number-algebra.md` decision 15 |
| 6 | **The result-table quiz letter moves from R to Q**, because R means region selection in four other curriculum files | 2.0, 2.1, 2.2, 2.3 | `CONTENT-FORMAT.md` 3.4 and 12.4; `stage0-precalc-computing.md` 0.3 |
| 7 | **The hours budget maps onto estimate units.** Every block names the unit that carries its estimate (lesson minutes, set and paper estimates, `Level.companion` hours, exit `estHours`, project milestones); redo time and the practice paper are spent time only. The sums are 142.25 of 150 h (94.8%) and 37.5 of 40 h (93.75%), inside CI's 10% band | 1.1, 1.2, 5 | `ASSESSMENT.md` 8.7; `CONTENT-FORMAT.md` 3.8, 6.7 |
| 8 | **The reading map carries hours, source ids and licences.** Every row has the hours that become its `Level.companion` entry, and every resource has a `src.*` id (canon-gap.md's where they exist, 31 new ones requested in section 8) and a licence, because only CC BY sources may be adapted | 5, 8 | `CONTENT-FORMAT.md` 3.2 (`Companion`), 9.4; `canon-gap.md` 6 |
| 9 | **Resource corrections.** The 1.2 lecture spine is The Missing Semester 2026 (nine lectures, titles [searched]), with the 2020 lectures it dropped; McKinney's 3rd edition numbers NumPy's sections 4.1 ndarray, 4.2 pseudorandom number generation, 4.3 ufuncs, 4.4 array-oriented programming, 4.6 linear algebra, 4.7 random walks (corrected in the verification pass: draft 2 had the 2nd edition's order), and chapter 11 runs 11.1 to 11.7 [searched]; the book was written for pandas 1.4 [searched], so the reading rows flag where the pinned pandas 3 differs | 2.3, 5 | Web searches, 6 October 2026 |
| 10 | **Widgets the depth-first order reaches first.** 1.1 and 1.2 are built before 1.3 to 1.8, so `recursion-tree` (a 1.8 widget, P1), `path-simulator` (1.5), `matrix-multiply` (1.4), `mutant-hunter` property mode and `shell-sim` job, remote and `awk` modes move into the waves that ship with these lessons. `payoff-builder`, `vim-sim`, `schema-builder` and `counterexample-lab` are no longer used: `plot-2d`, `text-terminal`, `code-cell` and `mutant-hunter` cover those screens | 1.0 decision 19, 2.1, 2.2 | `widgets-programming.md` 14 (priorities and waves); `widgets-calc-linalg.md` 0 |
| 11 | **Measured package facts for 1.1 and 1.2** in Pyodide 314.0.7: `sqlite3` imports in the core with SQLite 3.39.0; `zoneinfo` needs the `tzdata` package (2025.3 in the lock); Hypothesis is not in the lock at all, so the property-based testing lesson needs the app to ship Hypothesis's pure-Python wheel or it hands off (request in section 8) | 1.0 decisions 23 and 24, 2.2 (lessons 24, 31, 32), 6.2, 8 | [measured: `pyodide-lock.json` and imports] |
| 12 | **Exams and exits follow the runtime.** `exm.python` needs only the standard library, NumPy and pandas, so it runs on both targets; `exm.tools` runs on both, its one pytest item limited to the `zqtest` subset; `1.1.exit` needs matplotlib for its figure tests and `1.2.exit` is a paste on any device. Both exits carry `estHours` | 4 | `ASSESSMENT.md` 2.9, 2.10, 3.1 |
| 13 | **Sample lesson rewritten to the revision 2 schema**: element references in `widget/kind:name` form, a `tutor` block (`focus`, `notes`, `reps`, `avoid`) on every task screen with no accepted value in it, `why.rep`, Show solution text, hints after the lesson's first Check, Bertie's `surprised` one-shot on the trap reveal, a screen estimate column. Screen 6 no longer repeats 0.4 lesson 24: it asks for the objects, not the printed value | 7 | `CONTENT-FORMAT.md` 3.5, 3.7, 3.10, decision 17; `AI-TUTOR.md` 2.2; `BERTIE.md` 5.3 |
| 14 | **Fixes found on a second reading**: draft 1 cited 0.4 lessons 5 and 6 for the terminal (now 0.4 lessons 13 to 17); it claimed its course letters clash with no Stage 0 letter (Y, B, A and T do; decision 22); lesson 87 said a text key and a number key "match nothing" (pandas 3 raises `ValueError`); lesson 21 of 1.2 said comparing with 0 always needs `abs` (`pytest.approx` has a default absolute tolerance of $10^{-12}$); homework D4 example 1 repeated 0.3 lesson 57; lesson 105 called pandas 3 text columns "object strings" (they are the `str` dtype) | 1.0, 2.1, 2.2, 3.1 | [measured]; the Stage 0 files |

### 0.2 What was executed

All on 6 October 2026, in a scratch folder outside the repository [measured]:

- **Two Python runtimes.** CPython 3.11.15 with NumPy 2.4.6, pandas 3.0.6, SciPy 1.17.1, matplotlib 3.11.2 and pytest 9.1.1 (the learner floor), and Pyodide 314.0.7 (Python 3.14.2, NumPy 2.4.6, pandas 3.0.2, the app's runtime on both targets) loaded in Node 22.22 from the `pyodide` npm package and the spike's wheels. Hypothesis 6.168.5 was installed in a separate CPython environment for the property tests.
- **Every claim checked.** Five scripts (about 900 lines) and six short probes recomputed every predicted output, numeric answer, trap value and edge value in sections 2 and 7, every 1.1 homework example and reference solution in section 3, and the exam and exit numbers in section 4. Core-language, NumPy and pandas checks ran on both runtimes; SciPy, matplotlib and `zoneinfo` checks ran on CPython only, because the scratch folder had no Pyodide wheels for them. 1.2's shell examples ran in GNU bash 5.2.21, its Git examples in Git 2.43.0 with fixed author and committer, its SQL examples through Python's `sqlite3` on SQLite 3.45.1 and on Pyodide's SQLite 3.39.0, its pytest example against four mutants, and its drawdown properties under Hypothesis.
- **Disagreements found and resolved.** Two checks failed on Pyodide and passed on CPython: built-in `sum([0.1] * 10**6)` is `100000.0` on Python 3.14 (`100000.00000133288` on 3.11), and `np.linalg.solve` of a singular matrix returns `[nan nan]` with no exception. Follow-up probes showed no NumPy floating-point warnings at all in Pyodide (divide, overflow and invalid), `np.seterr(divide="raise")` raising nothing, `cholesky` of an indefinite matrix returning `nan`, integer scalar overflow still warning (it is checked in software), and Python 3.14 printing "division by zero" where 3.11 prints "float division by zero", warning on `return` inside `finally`, and warning that `datetime.utcnow()` is deprecated. Section 0.1 change 3 says what the lessons do about each.
- **Lock-file facts.** `pyodide-lock.json` (357 packages): `pytest` 9.0.2, `tzdata` 2025.3, `matplotlib` 3.10.8, `scipy` 1.18.0 present; `hypothesis` absent; `sqlite3` not a package, because it imports from the core.

The scripts are scratch checks, not repository code: `zqverify` and the drill runners replace them at build stage (`CONTENT-FORMAT.md` section 6).

---

## 1. Item overview

### 1.0 Scope, boundaries and decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Unit of lesson time | **15 minutes per lesson, quiz included**, as in Stage 0 | 10 minutes; screens only | One rule for every budget in the app. Code screens with a run or a step-through take longer than a tap, so the upper end is the honest figure |
| 2 | Spine for the core language | **CS50P** as the one core resource (the curriculum offers CS50P or Automate the Boring Stuff); Automate the Boring Stuff as the second explanation; MIT 6.100L as the university-grade lecture parallel | Automate the Boring Stuff as spine; 6.100L as spine | Curriculum rule 1 asks for one resource. CS50P has auto-checked problem sets (rule 2, problems over reading) and covers exceptions, tests, regular expressions and classes. Automate the Boring Stuff is task-led and thin on the model of names, scope and errors, and 0.4 already used its first chapters. 6.100L is excellent but its problem sets lean towards algorithms, which is 1.8's job |
| 3 | Courses for 1.1 | **Four courses**: Thinking in Python (28 lessons), Building Real Programs (27), Arrays and Simulation (20), Data, Time Series and Charts (32) | McKinney's chapters as courses; one Python course and one data course | Four is the content-format ceiling per topic. The split follows the dependency chain (the object model, then programs, then arrays, then frames) and keeps every course inside the 20 to 45 lessons of design research 8.2 |
| 4 | Courses for 1.2 | **One course, Tools of the Trade**, 7 levels, 32 lessons | Four courses (shell, Git, testing, SQL) of 6 to 10 lessons; two courses of 16 | Each tool alone sits below the 20-lesson floor of design research 8.2. Levels still give each tool its own review and homework, and one course map shows the whole toolbox |
| 5 | Order inside 1.2 | **Shell, Git, testing, SQL** | The curriculum's cover order (Git, shell, SQL, pytest) | Git on the command line needs the shell. Testing next means the 1.2 exit (a repository with a test) is reachable at the end of level T5. Nothing else in 1.2 needs SQL, so it comes last |
| 6 | Where testing lives | **Reading tests in 1.1, writing them in 1.2.** Every 1.1 drill shows visible tests and runs hidden ones (`zqtest`); `assert` is taught in lesson 36. pytest, test design, fixtures and Hypothesis are 1.2 level T5 | pytest in 1.1, where CS50P lecture 5 puts it | The curriculum puts pytest in 1.2. A learner who has read 100 test reports in 1.1 writes better tests in 1.2 |
| 7 | Recursion and complexity in 1.1 | **One lesson each** (21, 28) as working previews; 1.8 owns both | None; a full level of each | Frames make recursion a natural end to the call-stack level. Container costs decide everyday choices (a list or a set) long before 1.8 |
| 8 | Simulation inside 1.1 | **A whole level (A3, 7 lessons)**: seeds, Monte Carlo with standard errors, vectorised simulation, random walks, price paths, an expected payoff, SciPy as a checker | Leaving simulation to 1.5 | The curriculum puts Python first "so that every maths topic after it can be checked in code"; 1.5 checks every probability by simulation. Canon-gap P3 asks for Monte Carlo literacy early. Results the maths has not yet proved (the $\sigma/\sqrt{n}$ law, the lognormal mean) are observed here and tagged for proof in 1.5 (its lessons 86, 97 and 116) and 1.6 |
| 9 | Standard deviation before 1.6 | **Taught operationally from its definition** in lessons 63, 70 and 97, tagged "proved in 1.5 and 1.6" | Waiting for 1.6 | The 1.1 exit needs annualised volatility. The definition is 0.2 algebra (sigma notation, lesson 16; the variance identity, lesson 76) |
| 10 | SciPy | **One lesson (75)** | None; a level | The curriculum names NumPy, pandas and matplotlib. SciPy's `stats`, `optimize` and `integrate` are used from 1.3 onwards as checkers, so one tour suffices here |
| 11 | Versions | **Content runs on two Pythons: CPython 3.11, the learner floor (0.3 decision 11), and Pyodide 314.0.7 (Python 3.14.2), the app's runtime.** The pandas pin is Pyodide's 3.0.2; copy-on-write (lesson 81), the `str` dtype (lessons 77, 105), the `pct_change` default (lesson 93) and the floating-point flags of WebAssembly (lessons 66, 67) are taught as version facts | Version-free lessons; CPython only | pandas 1.4 (McKinney), 2 and 3 differ in exactly the places the lessons teach, and the two Pythons differ in `sum` of floats and three messages [measured]. CI fails a lesson whose recorded output differs between the runtimes unless the lesson teaches the difference, and a Pyodide bump reruns every recorded output (`ARCHITECTURE.md` 3.4) |
| 12 | The two targets | **Every screen and item declares what it needs; it runs wherever the build ships that.** Screens without live code run everywhere, because authored code runs at build time and ships as recorded traces and outputs. Code screens and drills declare `needs` (`[]`, `[numpy]`, `[numpy, pandas]`, `[matplotlib]`, `[scipy]`, `[pytest]`, `[hypothesis]`, `[tzdata]`); SQL screens use the SQLite worker; shell and Git screens are JavaScript simulators. Below 768 px every code screen also offers its Parsons version | Draft 1's MicroPython tags; separate Artifact content | `ARCHITECTURE.md` decision 15 and `ASSESSMENT.md` decision 30. NumPy and pandas ran inside the Artifact on the owner's iPhone in 5.1 s [sourced: `spikes/README.md`], so courses A and D no longer hand off; only matplotlib, SciPy and the testing packages wait on the E8 budget measurement, and time-zone items wait on `tzdata` joining a load group (section 8, request 9) |
| 13 | Quant transfer | **One transfer screen per lesson where a true finance or data context exists**, at least one per level | A finance context forced into every lesson | As Stage 0 decision 10. Python has many honest finance contexts (prices, trades, option symbols, order books, P&L) and they run through every course |
| 14 | Exams | **`exm.python`**: 90 minutes, code items, needs the standard library, NumPy and pandas only, so it runs on both targets. **`exm.tools`**: 60 minutes, runs on both (simulators in JavaScript, SQL in the SQLite worker, its one pytest item in the `zqtest` subset) | One combined paper; papers without code; papers with matplotlib or SciPy items | Code is the subject. A paper never splits across targets (`ASSESSMENT.md` 3.3); keeping both papers inside the measured Artifact runtime means neither depends on the E8 budget |
| 15 | Sample lesson | **1.1 lesson 1, Names and objects** | 1.2 lesson 9, A commit is a snapshot; 1.1 lesson 64, Vectorising loops | It is the root of 1.1's dependency graph: aliasing, copies, default arguments, closures, NumPy views and pandas copy-on-write are one idea. It is the first Stage 1 lesson the depth-first build ships, and it replaces the box picture that 0.4 lesson 24 left in place |
| 16 | 1.1 exit rebuild | **Capstone drill on a seeded, messy CSV** with hidden tests at $10^{-6}$ and three figure assertions, then the same script run locally with its output pasted and compared | In-app only; local only | `ASSESSMENT.md` 2.9. The exit is about real files on a real machine; the in-app drill makes the conventions checkable first |
| 17 | 1.2 exit habit | **The exit is met once, then policed weekly**: the weekly review asks for the latest commit link of the week's Build block | Exit met once and forgotten | The curriculum's exit says "Everything you build from here on is too", and rule 4 says everything goes on GitHub from 1.2 onwards (`ASSESSMENT.md` 8.2) |
| 18 | Overlap with Stage 0 (new in draft 2) | **Where the final 0.1 to 0.4 lesson lists teach an idea, 1.1 and 1.2 extend it and never re-teach it.** The second table below lists each idea, where Stage 0 teaches it and what 1.1 or 1.2 does instead | Keeping draft 1's lessons as recaps | A repeated hook kills the surprise a hook depends on, and a lesson the learner has already done is 15 minutes spent twice. Recaps happen anyway: level reviews draw 30% from earlier levels, and the Redo queue returns misses |
| 19 | Widgets the depth-first order pulls forward (new in draft 2) | **`recursion-tree` (lessons 21, 33), `path-simulator` random-walk and price modes (72, 73), `matrix-multiply` (67), `mutant-hunter` property mode (1.2 lesson 24) and `shell-sim` job, remote and `awk` modes (1.2 lessons 3, 8) ship with these lessons.** `payoff-builder` (lesson 74), `vim-sim` (1.2 lesson 8), `schema-builder` (1.2 lesson 31) and `counterexample-lab` (1.2 lesson 24) are not used; `plot-2d`, a `text-terminal` recording, `code-cell` and `mutant-hunter` cover their screens. `bench-lab`'s profile mode stays P1: lesson 68 shows a profile recorded at build time in `value-table` | Waiting for 1.3 to 1.8 to build their widgets; using every planned widget | Content goes depth-first in curriculum order (the owner's decision), so 1.1 and 1.2 are the first lessons to reach these widgets. Four of them would be built for one screen each, where a primitive does the job |
| 20 | Hours and estimates (new in draft 2) | **Every block of the hours budget names the unit that carries its estimate**; redo and the practice paper are spent time only | Leaving the mapping to the build | CI fails a topic whose estimates miss its curriculum hours by more than 10% (`CONTENT-FORMAT.md` 6.7). The mapping is a content decision |
| 21 | Quiz marks (new in draft 2) | **1 mark per quiz item**, 4 items per lesson, Mastered at 3 of 4 | Marks equal to difficulty; multi-mark sorts | `ASSESSMENT.md` decision 26; the Mastered rule is about slips, not weights (Stage 0 decision 15) |
| 22 | Display codes (new in draft 2) | **Kept: Y, B, A, D and T.** The app always shows a level code with its topic number ("1.1 B3"), so 0.4's Y and B, 0.5's A and 0.3's T cannot be confused on screen | Two-letter codes, as `stage1-statistics-ts.md` uses | Other files cite "1.1 level A3", and draft 2 keeps every level code. Single letters are exhausted across Stage 0 and Stage 1, and ids, which progress refers to, never depend on display codes (`CONTENT-FORMAT.md` 4.1). Open item 3 asks the owner whether to move every file to two letters at once |
| 23 | Testing packages in the app (new in draft 2) | **Learner-written tests in lessons and homework run under real pytest (`needs: [pytest]`, the `testing` load group); the exam item uses the `zqtest` subset (plain `assert`, `approx`, `raises`, `parametrize`); Hypothesis is shipped by the app as its own pure-Python wheel** | The `zqtest` subset everywhere; Hypothesis only on the learner's machine | Fixtures, `tmp_path` and `monkeypatch` (lesson 22) need real pytest, which is in Pyodide's lock (9.0.2). Hypothesis is not in the lock [measured] but is pure Python, and its two dependencies (`attrs`, `sortedcontainers`) are; until `ARCHITECTURE.md` accepts the wheel, lesson 24's live screen hands off (section 8, request 1) |
| 24 | SQLite versions (new in draft 2) | **Every SQL item runs in CI on two builds: the SQL worker's (`@sqlite.org/sqlite-wasm` 3.53.4) and Pyodide's `sqlite3` (SQLite 3.39.0)**, and uses nothing newer than 3.39 | One SQLite build | Lessons 25 to 31 run in the SQL worker; lesson 32 and homework T7 run SQL from Python, which is Pyodide's SQLite [measured: 3.39.0]. Window functions (3.25), `STRICT` tables (3.37) and `RIGHT JOIN` (3.39) are all inside 3.39 [recalled] |

**What 1.1 and 1.2 leave to other items.**

| Topic | Where it is taught | Note |
|---|---|---|
| Algorithm design, complexity analysis, recursion in depth, data structures | 1.8 | Lessons 21 and 28 are previews; `complexity-lab` and `recursion-tree` return there |
| Proofs of the simulation facts ($\sigma/\sqrt{n}$, the central limit theorem, lognormal moments, the ruin formula) | 1.5, 1.6 | Observed in level A3, proved in 1.5 lessons 43, 86, 97 and 116 |
| Floating point as a theory (conditioning, backward error), variance reduction beyond antithetic pairs, quasi-random numbers | Canon-gap P3 (2.0a), if the owner accepts it | Lessons 4, 66 and 74 give the first contact P3 assumes |
| Option pricing theory | 1.7 | Lesson 74 estimates an expected payoff and checks it against a formula that it states without derivation |
| Least squares and regression | 1.4, 1.6 | Lesson 67 introduces `solve` and `lstsq` as tools |
| scikit-learn, pipelines, leakage in machine learning | 2.1 | Lesson 94 (look-ahead bias) plants the habit |
| Time series models (ARMA, GARCH, cointegration) | 2.2 | Lesson 97 names where the $\sqrt{252}$ rule fails |
| The advanced data model, descriptors, metaclasses, `asyncio`, concurrency | Stage 2 (Fluent Python, as the curriculum says); canon-gap P13 on the developer track | Lesson 68 teaches measurement, not parallelism |
| Web APIs at scale, scraping, databases in production, Docker | 2.3 project 4 | Lesson 41 reads JSON from a file; one optional local drill calls a public API |
| Vim beyond survival, build systems (`make`), containers, cryptography, agentic coding | Not covered | The Missing Semester lectures on editors, metaprogramming, security (2020) and agentic coding (2026) are optional stretch reading |
| C++ | 1.9 | |

**What 1.1 and 1.2 take from Stage 0, and do not repeat** (new in draft 2). Checked against the final lesson lists of `stage0-number-algebra.md` and `stage0-precalc-computing.md` draft 2. "0.4 lesson 24" means lesson 24 of item 0.4.

| Idea | Taught in | 1.1 or 1.2 does |
|---|---|---|
| `//`, `%` and `**`; `-7 // 2` is $-4$; `^` is not a power | 0.4 lesson 22 | Lesson 3 opens on the sign of `%` (clock arithmetic backwards in time) and the identity that ties `//` to `%` |
| `int()`, `float()`, `str()`; `int("3.7")` fails; `"5" * 3` | 0.4 lesson 23 | Lesson 2 is about types belonging to objects, not names, and converting messy text (`" 12\n"`, `"1_000"`, `"1,000"`) |
| `a = 1; b = a; a = 2` leaves `b` at 1 | 0.4 lesson 24 | Lesson 1 replaces the box picture with names and arrows; its screen 6 asks which objects exist, not what prints |
| f-strings with `:.2f` round only for display | 0.4 lesson 25 | Lesson 9's trap moves to rounded rows that do not add up to the rounded total |
| `if`, `elif`, `else`; testing "over £50" before "over £100" | 0.4 lesson 26 | Lesson 11's edge moves to the truthiness of `nan`, 0 and empty containers |
| `range(1, 100)` stops at 99; running totals | 0.4 lesson 27 | Lesson 12 becomes fenceposts ($n$ prices give $n - 1$ returns) and the count formula for `range` |
| `while` with `break`; doubling £1,000 at 5% | 0.4 lesson 28 | Lesson 12 drops the doubling hook; lesson 13 adds the loop's `else` |
| `print` against `return`; a function without `return` gives `None` | 0.4 lesson 29 | Lesson 16 becomes function contracts: the `None` that one path returns, crashing far away, and tuples as several results |
| Reading a traceback from the bottom; a bare `except:` hides errors | 0.4 lesson 30 | Lesson 34's trap: the bottom frame is not always where the bug is. Lesson 35's trap: a `try` that covers too much |
| `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `rm`, help, history, `*`, `>`, `>>`, `\|`; the shell expands `*` | 0.4 lessons 13 to 17 | 1.2 level T1 starts from word splitting and quoting, standard error, text-tool pipelines and `find`; lesson 4's trap moves to unquoted patterns handed to `find` |
| Installing Python, PATH, two Pythons, `which` | 0.4 lesson 19 | 1.2 lesson 6 opens on `export` and child processes; 1.1 lesson 46 on `python -m pip` and environments |
| VS Code opens a folder; its terminal can start elsewhere | 0.4 lesson 20 | 1.1 lesson 39 anchors paths to the script with `Path(__file__)` |
| Binary fractions; `0.1 + 0.2 != 0.3`; test with a tolerance | 0.1 lesson 42; 0.4 lesson 26 edge | Lesson 4 is about relative precision, the spacing of floats (`math.ulp`), absolute against relative tolerance, `inf` and `nan` |
| Rounding to decimal places and significant figures | 0.1 lesson 37 | Lesson 5 is Python's round-half-to-even and the stored value behind it |
| Simple and log returns; log returns add over time | 0.3 lesson 57 | Lesson 93 is the pandas mechanics and the cross-section rule: a portfolio averages simple returns, not log returns |
| Log underflow; log-sum-exp named | 0.3 lesson 59 | Lesson 66 and homework A2 implement and derive log-sum-exp in NumPy |
| Permutations, combinations, the four cases | 0.3 lessons 98 to 102 | Lesson 31 maps the four cases onto `product`, `permutations`, `combinations` and `combinations_with_replacement` |
| Two-dice sample spaces | 0.3 lesson 112 | Lesson 14's hook moves to dates and prices; dice stay only as lesson 70's simulation target |
| The spread of a relative frequency shrinks like $1/\sqrt{n}$ | 0.3 lesson 113 | Lesson 70's trap moves to printed digits: a simulated estimate is not as precise as it looks |
| The birthday problem at 23 | 0.3 lesson 117 | Homework A3's birthday drill checks a simulation against the known product |
| Truncated axes, log axes, log price charts | 0.2 lesson 47; 0.3 lesson 55 | Lesson 100's trap moves to rebasing; lesson 103's to dual axes |
| Quartile conventions differ | 0.3 lesson 120 | Lesson 65 names NumPy's default (linear interpolation) as one of them |
| Frequency density histograms | 0.3 lesson 121 | Lesson 101 overlays a density on `density=True` |
| Survivorship bias | 0.3 lesson 123 | Lesson 103 uses it as an edge in a fund chart |
| Bisection and its step count | 0.2 lesson 108 | 1.2 lesson 18 applies it to `git bisect` |
| Standard scores | 0.2 lesson 105 | The A2 lab drill standardises columns by broadcasting |

### 1.1 1.1 Python (150 h)

**Purpose in a quant or ML career.**

- **The working language of research.** Quant research and ML teams write Python, and researcher interviews include "a data take-home" (curriculum track table), which in practice means NumPy and pandas under time pressure.
- **The costly bugs are model-of-Python bugs.** Aliasing, mutable defaults, float equality, naive timestamps, chained assignment and a misplaced `shift` do not crash; they corrupt a backtest quietly. The courses are built around these failure points.
- **Every later item is checked in code.** 1.3 numerics; the 1.4 exit (least squares and PCA in NumPy); 1.5 simulation; the 1.6 exit (regression in NumPy matched to statsmodels); the 1.7 exit (a binomial pricer in Python); 1.8's 150 problems.
- **Simulation is the quant's calculator.** A Monte Carlo estimate with an honest error bar checks an interview answer when the algebra stalls and prices what has no closed form.
- **Data hygiene is most of the job.** Real prices come with splits, holidays, time zones, missing days and vendor errors. Look-ahead bias is the most expensive single bug in the field, and 1.1 teaches it before any model exists to hide it.
- **Communication.** Readable code and honest charts are what a reviewer or interviewer sees first.

**Learning outcomes.** At the end of 1.1 the learner can:

| # | Outcome | Measured by |
|---|---|---|
| PY-O1 | Predict the state of names and objects through assignment, mutation, rebinding, function calls and copies, for code of up to 15 lines | 85% on fresh difficulty-3 predict-output items; exam items 2 and 5 |
| PY-O2 | Choose among `int`, `float`, `Decimal`, `Fraction` and integer pence for a task, compare floats with a stated tolerance, and predict Python's rounding | 85% on difficulty-3 items; homework Y1 |
| PY-O3 | Slice, parse, format and encode text, including option symbols, money strings and non-ASCII files | 85% on difficulty-3 items |
| PY-O4 | Write functions with positional, keyword, default and variadic parameters; explain scope, closures and recursion; avoid the mutable default | Lesson quizzes 16 to 21 Mastered (3 of 4); exam item 5 |
| PY-O5 | Choose among list, tuple, dict, set, `deque`, `Counter` and `defaultdict` for a task and state the cost of their core operations | 85% on difficulty-3 items; exam item 6 |
| PY-O6 | Build lazy pipelines with iterators, generators, comprehensions and `itertools`, and predict exhaustion | 85% on difficulty-3 items |
| PY-O7 | Read a multi-frame traceback, handle and raise specific exceptions, and debug by hypothesis and minimal reproduction | Homework B2; exam items 9 and 13 |
| PY-O8 | Read and write text, CSV and JSON files; parse with regular expressions; do date arithmetic across time zones and daylight saving; build a command-line program | 85% on difficulty-3 items; homework B3 |
| PY-O9 | Set up a virtual environment, organise modules, reproduce a notebook from a clean restart, and write code a reviewer can read | Homework B4; long-form at 7 of 10 |
| PY-O10 | Design small classes with special methods, dataclasses, invariants and type hints, and decompose a specification into functions and classes | Trade Ledger project tests pass; exam item 11 |
| PY-O11 | Predict NumPy shapes, dtypes, views and broadcasting; vectorise loops; handle NaN and floating-point error; solve linear systems | 85% on difficulty-3 items; exam items 14 to 16 |
| PY-O12 | Write a seeded Monte Carlo simulation, attach a standard error, size it for a target error, and check it against an exact value | Homework A3; exam items 17 and 18 |
| PY-O13 | Load, clean, select, group, merge (including point-in-time joins) and reshape tabular data in pandas | 85% on difficulty-3 items; exam items 19 to 21 |
| PY-O14 | Compute simple and log returns, resample, roll windows, annualise volatility, and measure drawdowns, with no look-ahead | Exam items 22 to 24; the exit capstone |
| PY-O15 | Build honest multi-panel figures with matplotlib and diagnose a misleading chart | Homework D5; figure assertions in the exit capstone |
| PY-O16 | From a CSV of daily prices, compute returns, annualised volatility and maximum drawdown and plot them, on the learner's own machine | `1.1.exit` (section 4.3) |

**Prerequisites.** Stage 0 complete, in particular:

- **0.4** (Computer basics): course B (files, the terminal in lessons 13 to 17, installing Python and PATH in lesson 19, VS Code in lessons 20 and 21) and course Y (lessons 22 to 31: expressions, types, variables, `print` and `input`, `if`, `for`, `while`, functions, tracebacks, the ten-line script), which follow Automate the Boring Stuff chapters 1 to 3. 1.1 assumes the learner has run scripts from a terminal, and replaces 0.4's box picture of variables in its first lesson.
- **0.1** lessons 37 (rounding) and 42 (binary floating point); **0.2** lessons 16 (sigma notation), 47 (reading graphs critically), 75 and 76 (the mean minimises squared error; the variance identity), 105 (standard scores), 107 and 108 (iteration and bisection, met again as loops).
- **0.3**: lessons 55 to 59 (log scales, log returns, log underflow), 98 to 102 (counting, which `itertools` makes concrete), 112 to 117 (probability by counting and by relative frequency, which level A3 simulates) and 118 to 123 (averages, quartiles, histograms, sampling bias).
- 0.5 continues as the Daily 10. 1.1 runs before 1.3 to 1.6, so statistical ideas appear as definitions and simulations, tagged where 1.5 or 1.6 proves them.

**Hours budget (150 h).**

| Block | What | Hours | Share | Unit that carries the estimate |
|---|---|---|---|---|
| In-app lessons | 107 lessons at 15 minutes, quiz included | 26.75 | 17.8% | `Lesson.est` |
| In-app practice and redo | 19 level reviews of 8 items (4.75); 19 practice sets of generated items, one per level, about 45 minutes each (14.25); the Redo queue at 7 and 30 days (5.25) | 24.25 | 16.2% | Reviews: summed item `est`. Practice sets: `set.<course>.<level>-practice`, kind `practice`. Redo: spent time, no estimate |
| Homework | 19 sets at about 2 hours | 38.0 | 25.3% | Homework `set.*`, summed item `est` |
| Exams | The topic exam (90 min), one practice paper (90 min), reviewing both (60 min) | 4.0 | 2.7% | `exm.python` minutes (1.5); practice paper and review: spent time |
| External reading and lectures | Videos and reading 16.0 h (selected CS50P lectures, McKinney chapters 4 to 11, MIT 6.100L lectures, documentation pages); external problems 14.0 h (CS50P problem sets 0 to 4 and 6 to 8, Python Data Science Handbook exercises, one McKinney case study) | 30.0 | 20.0% | `Level.companion` hours (section 5.1) |
| Projects or drills | The exit capstone and local run (10 h); the Trade Ledger project (6 h); Python Lab: 22 drills of 30 minutes (11 h) | 27.0 | 18.0% | `1.1.exit` `estHours` 10; `prj.py.trade-ledger` milestone hours 6; four lab sets (`set.pythink.lab`, `set.pybuild.lab`, `set.arrays.lab`, `set.dataframes.lab`), kind `practice`, 11 |
| **Total** | | **150.0** | 100% | Estimates: **142.25 h (94.8%)**; spent-only time 7.75 h |

Solving time (everything except the 16 hours of videos and reading) is 134 hours, 89%, above the curriculum's 60% floor.

**Why redo and the practice paper carry no estimate.** A redo is a second attempt at an item whose first attempt already earned its hours, and a practice paper is assembled on demand from the practice pool (`ASSESSMENT.md` 3.2). Counting either as earned would credit the same hours twice. The pace factor absorbs them (`ASSESSMENT.md` 8.7).

### 1.2 1.2 Tools (40 h)

**Purpose in a quant or ML career.**

- **Every quant job uses all four** (the curriculum's reason for adding the item). Research code lives in Git, runs on Linux machines, reads from SQL databases and is guarded by tests.
- **Reproducibility.** A result that cannot be rerun from a commit is not a result. The 1.2 exit and curriculum rule 4 (everything on GitHub from 1.2 onwards) make the habit permanent.
- **Remote machines.** Long backtests and model fits run on servers over SSH and must survive a dropped connection.
- **SQL is how data arrives.** Trade, position and market data sit in relational tables. Window functions compute returns per instrument; joins that ignore time leak the future.
- **Tests as specifications.** A drawdown or P&L function with good tests can be refactored and reviewed with confidence; property-based tests find the inputs nobody imagined.
- **Security hygiene.** A key pushed to a public repository must be treated as stolen; a query built from strings is an injection waiting for an input.

**Learning outcomes.** At the end of 1.2 the learner can:

| # | Outcome | Measured by |
|---|---|---|
| TL-O1 | Navigate and change a file system from the shell, quote arguments, redirect streams and compose pipelines that answer a question about a text file | 85% on difficulty-3 state and predict items; exam items 1 to 3 |
| TL-O2 | Write a shell script that stops on the first failure, set permissions and environment variables, control processes and work on a remote machine | Homework T2 script passes its tests; exam items 4 and 5 |
| TL-O3 | Explain commits as snapshots, branches as pointers and the three trees, and predict `status` and `diff` after any sequence of commands | 85% on difficulty-3 items; exam item 6 |
| TL-O4 | Merge, resolve textual and semantic conflicts, rebase a private branch, push and pull without force, review a pull request, keep secrets out of history and recover lost commits | Homework T4; exam items 8 to 11 |
| TL-O5 | Write pytest tests that kill every mutant of a function, using partitions, boundaries, `approx`, `raises`, `parametrize`, fixtures and one property-based test | Homework T5; exam items 12 to 14 |
| TL-O6 | Write SQL with filters, `NULL` handling, grouping, joins, common table expressions and window functions | 85% on difficulty-3 result-set items; exam items 15 to 17 |
| TL-O7 | Create constrained tables, change data inside transactions, and query from Python with parameters | Homework T7; exam item 18 |
| TL-O8 | Put the 1.1 project in a GitHub repository with at least one passing test, and run its tests in CI on every push | `1.2.exit` (section 4.3) for the repository and test; the CI check is recommended, not gated |

**Prerequisites.** 1.1 complete. Specifically: courses Y and B for every Python drill; lessons 39 and 44 (files, paths, command-line programs) for the shell; lessons 46 and 47 (environments, reproducibility) for Git; course D for testing data code (1.2 lesson 23) and for SQL into pandas (lesson 32). 0.4 lessons 13 to 17 (the terminal, wildcards, redirection and pipes) and 19 (PATH) are assumed; level T1 checks them in its hooks and never re-teaches them.

**Hours budget (40 h).**

| Block | What | Hours | Share | Unit that carries the estimate |
|---|---|---|---|---|
| In-app lessons | 32 lessons at 15 minutes, quiz included | 8.0 | 20.0% | `Lesson.est` |
| In-app practice and redo | 7 level reviews of 8 items (1.75); 7 practice sets of 30 minutes (3.5); the Redo queue (1.0) | 6.25 | 15.6% | Reviews: summed item `est`. Practice sets: `set.toolkit.<level>-practice`, kind `practice`. Redo: spent time |
| Homework | 7 sets at about 1.5 hours | 10.5 | 26.25% | Homework `set.*` |
| Exams | The topic exam (60 min), one practice paper (60 min), reviewing both (30 min) | 2.5 | 6.25% | `exm.tools` minutes (1.0); practice paper and review: spent time |
| External reading and lectures | Videos and reading 4.75 h (The Missing Semester 2026 lectures 1, 2 and 5, with 2020 lecture 2 for shell scripting; Pro Git chapters 2 and 3; the pytest and SQLite documentation); external exercises 3.5 h (Software Carpentry's Unix Shell, OverTheWire Bandit levels 6 to 10, Learn Git Branching, CS50P problem set 5, SQLBolt lessons 1 to 18) | 8.25 | 20.6% | `Level.companion` hours (section 5.2) |
| Projects or drills | The exit: the 1.1 project as a GitHub repository with tests and a CI check (3.0 h); Tools Lab: 3 drills of 30 minutes (1.5 h) | 4.5 | 11.25% | `1.2.exit` `estHours` 3.0; `set.toolkit.lab`, kind `practice`, 1.5 |
| **Total** | | **40.0** | 100% | Estimates: **37.5 h (93.75%)**; spent-only time 2.5 h |

Solving time is 35.25 hours, 88%.

---

## 2. Courses

### 2.0 Conventions for every lesson below

**Ids** follow CONTENT-FORMAT.md section 4.1: `crs.<course>`, `lvl.<course>.<level>`, `lsn.<course>.<slug>`, `set.<course>.<level>` for homework, `set.<course>.<level>-practice` for the practice set, `set.<course>.lab` for lab drills, `exm.python` and `exm.tools` for the topic exams, `prj.<topic>.<name>` for projects (as Stage 0's `prj.alg.root-finder`). Libraries use the topic namespaces `py` (1.1) and `tools` (1.2): `skl.py.*`, `mc.py.*`, `gen.py.*`, `drl.py.*`, `skl.tools.*`, `mc.tools.*`, `gen.tools.*`, `drl.tools.*`. Topic ids are `top.python` and `top.tools`. The `#` column is the lesson's number within its topic; display numbers are computed from position and never stored.

**Display codes.** Courses carry a letter: Y (Thinking in Python), B (Building Real Programs), A (Arrays and Simulation), D (Data, Time Series and Charts), T (Tools of the Trade). Level B3 is the third level of course B. Y, B, A and T repeat Stage 0 letters (0.4's Y and B, 0.5's A, 0.3's T), so the app always prints a level code with its topic number, "1.1 B3" (decision 22).

**Every lesson** runs the design research 8.3 sequence: hook on a canvas, free manipulation, the name for what the learner just did, a ladder of 2 to 4 screens adding one constraint each, the trap, the rule stated as a description of the learner's own steps, a transfer screen where a true quant context exists, the summary card, then a quiz of 4 items. From the owner's skills, every lesson also carries the "why this exists" frame (`frame.why`), one common trap (a `trap` screen), at least one edge case (`edgeCases`), one worked example with a decision point where the naive route fails (`workedExample`), and a derivation the learner completes, with `leap` (naive, fails, points to) wherever the step is a creative one. Lessons have 8 to 12 screens, at most 2 without a task. In a programming lesson these take particular forms:

- **Manipulation before notation** means predicting an output, stepping a trace, dragging a name's arrow, sliding a slice handle, tapping an axis, or moving a window bracket, before any rule or syntax summary appears.
- **The worked example** is a short program whose naive version fails; the failing version runs beside the fix, as design research 9.4 sets for code.
- **Derive** means one of three things: ordering the steps Python takes (how `+=` works on a list), completing a trace table, or deriving a formula the code uses ($\sqrt{252}$ in lesson 97, the $\sigma/\sqrt{n}$ error in lesson 70, the count of `range` in lesson 12, the step count of bisection in 1.2 lesson 18).

**Widgets** use the ids in widgets-programming.md section 14 and the shared names of CONTENT-FORMAT.md section 1 (`choice`, `numeric-input`, `derivation-steps`, `code-cell`, `plot-2d`, `sim-runner`, `value-table`). Widgets from other catalogues keep their owners' ids: `number-line`, `venn-diagram`, `modular-clock`, `counting-slots`, `stat-chart` (Stage 0, built by the time 0.3 ships); `matrix-multiply`, `path-simulator` (calculus and linear algebra, pulled forward by decision 19). A widget mode that widgets-programming.md does not yet list is marked [mode to add]. Hint and Why? highlights name elements as `<widget id>/<kind>:<name>` (CONTENT-FORMAT.md 3.5): `code/line:3`, `heap/node:o1`, `grid/cell:2,3`.

**Runtime.** Every code screen and drill declares `needs` (decision 12). Lesson screens without live code run on both targets, because their code runs in CI and ships as recorded traces, outputs, result sets and figures. CI records every authored output on **both** Pyodide 314.0.7 and CPython 3.11; a difference fails the build unless the screen is tagged with it and teaches it (decision 11). Where a build cannot provide an item's `needs`, the item shows "Run this one in the web app" with the drill id and seed and accepts a result code (`ASSESSMENT.md` 2.5, 14.3); a lesson screen offers its Parsons version instead, so the lesson can still be finished on a phone.

**Bertie** is built in from the first lesson, following `AI-TUTOR.md` 2.2: hints and his lines open after the lesson's first Check; Why? and "Explain another way" after a screen is resolved; nothing on homework until the set is submitted; `away` during every timed paper. Every task screen carries `tutor.focus`, and `tutor.notes`, `tutor.reps` and `tutor.avoid` where they help (CONTENT-FORMAT.md 3.10); no tutor field contains a value the screen's check accepts. On code screens he never edits code: before a pass the code guard replaces any code block longer than 2 lines in his replies (`AI-TUTOR.md` 8.2), and after a pass "Review my code" returns a review in the owner's code-craft format at the depth the learner picks (`AI-TUTOR.md` 2.8). On a trap screen's reveal the lesson player plays his `surprised` one-shot (`BERTIE.md` 5.3).

**Quiz item types.** Stage 0's letters (CONTENT-FORMAT.md 3.4): N numeric, X expression, C single choice, M multi-select, O order the steps or lines, S sort or match, I interval, P point on a chart, T predict the output of code, K write code that passes tests. This file adds three:

| Letter | Type | Check kind |
|---|---|---|
| E | Entry graded by behaviour: a slice, path, shape, glob, pattern, command or format spec, graded by what it selects or produces, so any equivalent entry is accepted | `predicate` (`selection-equals`, `format-produces`, `matches-sets`), or `output` with `compare: regex` |
| Q | Result table: predict or produce the rows of a SQL query or a pandas expression (draft 1's R; R means region selection elsewhere) | `resultset` |
| G | Reach a target state in a simulator: files in `shell-sim`, a commit graph in `git-graph`, a project in `workspace-sim` (Stage 0's H is the same check for 0.4's shell tasks) | `predicate` on the widget's state |

K in a quiz is at most 8 lines, its tests run once on Submit, and on phones its Parsons version is offered (widgets-programming decision 15). Long-form items appear in homework and exams, never in quizzes. Single and multiple choice (C and M) stay at or below 40% of each course's quiz items (design research 10); section 2.3 counts them.

**Mastery and feedback.** Every quiz item carries 1 mark; a four-item quiz is Mastered at 3 of 4 (decision 21). Every graded screen carries the CONTENT-FORMAT.md 3.3 feedback set: a `reason` line for a correct answer, `diagnose` lines tied to misconception ids, an `otherwise` line, the three-rung hint ladder (nudge, point, step), and a Why? of at most three sentences with its representation (`why.rep`: picture, count, algebra, analogy, simulation or code).

**Level review.** Every level ends with a Level review of 8 items at difficulty 2 to 4, interleaved, with up to 30% drawn from earlier levels of the same course (ASSESSMENT.md 2.4). The practice set and the homework follow (section 3).

**Columns.** Objective is one measurable sentence. Hook is the puzzle the lesson opens with. Trap is the misconception the trap screen is built around; Edge is the fringe case the lesson must show. Transfer screens are listed under each level table.

### 2.1 Item 1.1 Python

#### Course Y: Thinking in Python (`crs.pythink`, 5 levels, 28 lessons)

The model Python actually runs: names bound to objects, numbers as the machine stores them, text, control flow, functions and frames, and the core collections with their costs. Every lesson is driven by prediction: the learner says what code will do, then watches a recorded trace prove or refute it. It replaces 0.4's "variables are boxes" picture in its first lesson.

**Level Y1: Objects, names and numbers** (`lvl.pythink.objects`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | `lsn.pythink.names-objects` Names and objects | Predict the state of names and objects after any sequence of assignments, in-place changes and function calls, and decide whether two names share one object with `is` against `==` | `prices = [100, 101, 102]; backup = prices; prices.append(99)`. What does `print(backup)` show? | `code-tracer` (predict), `node-link` (heap), `predict-output`, `choice`, `derivation-steps` (order) | Trap: assignment copies, and so does passing an argument. Edge: `x = x + [3]` builds a new list while `x += [3]` extends the shared one; ints cannot change, so sharing them is harmless, which is why 0.4 lesson 24's box picture worked for numbers (screen 6 asks which objects exist) [verified] | T, T, S, C |
| 2 | `lsn.pythink.types` Types belong to objects | Name the type of any expression's result with `type` and `isinstance`, explain that a type belongs to the object and not to the name, convert messy text to numbers explicitly, and predict which mixed-type operations raise `TypeError` | `x = "12"`, then `x = int(x)`, then `x = x / 4`. What is `type(x)` after each line? In a spreadsheet a column has one type. Does the name `x`? | `code-tracer` (objects with type tags), `predict-output`, `diagnostic-reader` | Trap: a name has a fixed type, like a spreadsheet column (the name has none; it names a `str`, then an `int`, then a `float`). Edge: `bool` is a kind of `int`, so `True + True == 2` and `isinstance(True, int)` is `True`; `bool("False")` is `True`; `int(" 12\n")` and `int("1_000")` succeed but `int("1,000")` raises (lesson 8 cleans it); `int(-3.7)` truncates to $-3$ where `//` floors (lesson 3). 0.4 lesson 23's conversions are assumed [verified] | T, T, M, C |
| 3 | `lsn.pythink.integers` Integers: remainders and no overflow | Evaluate `//`, `%` and `divmod` on negative operands from the rule $a = bq + r$ with $0 \le r < b$ for $b > 0$, use `%` for clock and calendar arithmetic in either direction, and explain why Python integers never overflow | A trade at 22:00 settles 30 hours later, and a margin call came 30 hours before 05:00. Python gives `(22 + 30) % 24` as 4 and `(5 - 30) % 24` as 23; the same remainder in C or JavaScript gives $-1$. Which is right for a clock, and why do they differ? | `modular-clock`, `number-line` (floor), `predict-output` | Trap: `%` keeps the sign of the left operand, as in C and JavaScript (in Python the remainder takes the sign of the divisor: `-25 % 24` is 23 and `25 % -24` is $-23$). Edge: 0.4 lesson 22's `-7 // 2 == -4` is the same rule seen from the quotient, because `(a // b) * b + a % b == a`; `math.fmod(-25, 24)` is $-1.0$, the C convention; `2**100` is exact, but `float(2**1024)` raises `OverflowError`; `pow(a, b, m)` keeps huge powers small [verified] | N, N, T, C |
| 4 | `lsn.pythink.floats` Floats: relative precision and special values | Predict where a float loses information from its 53-bit significand (the gap between neighbouring floats grows with size), compare floats with `math.isclose` choosing relative and absolute tolerances, and predict the behaviour of `inf` and `nan` | `1e15 + 1 == 1e15` is `False`, but `1e16 + 1 == 1e16` is `True`. Somewhere between them a float stops seeing a whole 1. Where, and why there? | `float-inspector` (bits and neighbours), `number-line` (float spacing) [mode to add], `predict-output` | Trap: floats are accurate to about $10^{-16}$ in absolute terms (the error is relative, about 16 significant digits: the gap between floats is $2^{-52} \approx 2.2 \times 10^{-16}$ at 1 and 2.0 at $10^{16}$, and whole numbers stop being exact at $2^{53} \approx 9.007 \times 10^{15}$). Edge: `math.isclose(1e-12, 0)` is `False` because the default absolute tolerance is 0; `nan != nan`; ten additions of 0.1 give 0.9999999999999999, so `while x != 1.0: x += 0.1` never stops; 0.1 lesson 42's binary fractions are assumed [verified] | C, T, N, M |
| 5 | `lsn.pythink.exact-money` Rounding and exact arithmetic | Predict `round` under round-half-to-even, and choose between `float`, `Decimal`, `Fraction` and integer pence for a money or probability calculation, with a reason | `round(2.5)` is 2, `round(3.5)` is 4 and `round(2.675, 2)` is 2.67. Is Python broken? | `float-inspector` (decimal mode), `predict-output`, `choice` | Trap: `Decimal(0.1)` built from a float inherits the float's error; build it from the string `"0.1"`. Edge: 2.675 is stored as 2.67499999999999982236431605997495353221893310546875 [verified], so it rounds down; half-to-even removes the upward bias in sums of rounded amounts | T, T, C, M |
| 6 | `lsn.pythink.expressions` Operators and evaluation order | Evaluate compound expressions using precedence, associativity and chained comparisons, and rewrite an ambiguous expression with brackets | What do `-2 ** 2`, `2 ** 3 ** 2` and `1 < 3 > 2` give? | `expression-tree` (Python mode), `predict-output` | Trap: `-2 ** 2` is 4 (it is $-4$: `**` binds tighter than the minus). Edge: `**` groups from the right, so `2 ** 3 ** 2` is 512; `a < b < c` means `a < b and b < c` with `b` evaluated once; `/` always returns a float | T, T, N, C |

Transfer screens: lesson 1 stress-tests a copy of a position book; lesson 3 finds a settlement hour and a margin-call hour with `%`; lesson 4 shows a P&L reconciliation failing an `==` check by $10^{-12}$; lesson 5 splits a coupon payment exactly in pence.

**Level Y2: Text** (`lvl.pythink.text`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 7 | `lsn.pythink.strings-slices` Strings, indexing and slicing | Write the index or slice that extracts any substring, including negative indices and steps, and explain why slices are half-open | An option symbol `AAPL250117C00150000`: pull out the expiry, the type and the strike | `array-strip` (characters), `predict-output` | Trap: `s[2:5]` includes index 5. Edge: the root has variable length, so the fields are sliced from the end (`s[-15:-9]`, `s[-9]`, `s[-8:]`) [verified]; an out-of-range slice returns `""` silently while an out-of-range index raises; strings are immutable | E, T, T, C |
| 8 | `lsn.pythink.string-methods` String methods and building text | Clean and parse a line of text with `strip`, `split`, `join`, `replace` and `startswith`, and build long strings with `join` | A broker export holds `"  1,234.50 GBP "`. Turn it into the number 1234.5 | `predict-output`, `code-blanks`, `complexity-lab` (race of `+=` against `join`) | Trap: `s.strip()` on its own line changes nothing; methods return new strings. Edge: `"a,,b".split(",")` keeps the empty field but `"a  b".split()` collapses runs of spaces; `"".split(",")` is `['']` while `"".split()` is `[]` [verified] | T, T, K, C |
| 9 | `lsn.pythink.formatting` f-strings and the format mini-language | Write format specifications for width, alignment, decimal places, thousands separators, signs and percentages, and use `!r` and `=` when debugging | Print a P&L table where 1234567.891 shows as `1,234,567.89`, $-0.0731$ as `-7.31%`, and the columns line up | `format-lab`, `predict-output` | Trap: if every row is rounded correctly, the rounded rows add up to the rounded total (three rows of a third of £1 show as 0.33 each beside a total of 1.00; state the rounding, or allocate the pennies as homework Y1 does). Edge: `f"{0.125:.2f}"` gives `0.12` because 0.125 is exact and ties go to even; `f"{x=}"` prints the expression with its value; 0.4 lesson 25's "rounding is for display only" is assumed [verified] | E, T, T, C |
| 10 | `lsn.pythink.unicode-bytes` Text, bytes and encodings | Distinguish `str` from `bytes`, encode and decode with UTF-8, and diagnose a `UnicodeDecodeError` or garbled text in a data file | A price file opened on another machine shows `Â£100` instead of `£100`. What happened? | `array-strip` (bytes mode) [mode to add], `diagnostic-reader`, `predict-output` | Trap: one character is one byte (`len("£")` is 1, its UTF-8 encoding is 2 bytes; decoding those bytes as Latin-1 gives `Â£`) [verified]. Edge: `"café"` can be 4 or 5 code points, so equal-looking strings compare unequal until normalised with `unicodedata.normalize("NFC", s)` [verified]; Excel's `utf-8-sig` byte-order mark | N, C, T, M |

Transfer screens: lesson 7 parses option symbols in the OCC format; lesson 8 cleans a broker's money strings; lesson 9 formats a risk report; lesson 10 repairs a vendor file with a £ sign.

**Level Y3: Control flow** (`lvl.pythink.control`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 11 | `lsn.pythink.conditions` Conditions and truthiness | Write `if`/`elif`/`else` chains whose branches are exclusive and complete, predict the truthiness of any value, and predict the operand `and` and `or` return | An order check reads `if side == "buy" or "sell":` and accepts every order, including "hold". Why? | `code-tracer` (tap executed lines), `predict-output` | Trap: `side == "buy" or "sell"` tests two things (it is `(side == "buy") or "sell"`, and a non-empty string is always truthy). Edge: `qty or 100` replaces a genuine 0 with 100; `float("nan")` is truthy, so `if price:` lets a missing price through; `0`, `0.0`, `""`, `[]`, `{}` and `None` are falsy; 0.4 lesson 26's branch-order trap is assumed [verified] | T, T, C, M |
| 12 | `lsn.pythink.loops` Loops, ranges and fenceposts | Predict how many times a `for` or `while` body runs, using $\max\left(0, \left\lceil \frac{\text{stop} - \text{start}}{\text{step}} \right\rceil\right)$ for `range`, and avoid fencepost errors between items and the gaps between them | A file holds 252 daily closes. How many daily returns are there, and which `range` visits each one once? Then: how many times does `for i in range(2, 20, 3)` run, and what is the last `i`? | `array-strip` (posts and gaps), `code-tracer`, `parsons`, `derivation-steps` | Trap: $n$ prices give $n$ returns (they give $n - 1$: a return lives in the gap between two prices, like a fence panel between posts). Edge: `range(10, 0)` is empty without a step of $-1$; changing the loop variable inside a `for` does not change the next value; the derive screen builds the count formula from the last value reached. Answers: 251 returns, from `range(1, 252)`; 6 runs, last `i` 17. 0.4 lessons 27 and 28 are assumed [verified] | N, N, O, T |
| 13 | `lsn.pythink.loop-control` Searching with break, continue and else | Write a search loop that stops at the first match and reports "not found" correctly, using `break` and the loop's `else` clause | Find the first day a price closes below the stop-loss level, or say there was none. The first draft prints "not found" on every day | `code-tracer`, `parsons`, `code-cell` | Trap: a loop's `else` runs "when the body never ran" (it runs when the loop was not broken). Edge: `else` also runs for an empty sequence; `continue` in a `while` loop can skip the increment and loop forever | T, O, K, C |
| 14 | `lsn.pythink.pairs` Looping over pairs: zip, enumerate and nested loops | Iterate over indices and values with `enumerate`, over parallel sequences with `zip`, and over all pairs with nested loops, and count the iterations of each | `for i in range(len(closes)): print(dates[i], closes[i + 1] - closes[i])` crashes with `IndexError` on the last day. Rewrite it so it cannot run off the end | `code-tracer`, `cell-grid` (iteration space), `predict-output` | Trap: `zip` checks that its inputs line up (it stops silently at the shorter one, so dates and prices drift out of step; `zip(..., strict=True)` raises instead). Edge: `zip(dates[1:], closes, closes[1:])` pairs each change with its later date; `for j in range(i + 1, n)` visits $\binom{n}{2}$ pairs (0.3 lesson 99), the loop behind a correlation matrix's upper triangle [verified] | N, T, N, C |
| 15 | `lsn.pythink.accumulators` Accumulators and running state | Write a single-pass loop that keeps running state (total, maximum, count, previous value), and compute a maximum drawdown from a list of prices | Prices 100, 120, 90, 110, 80, 130: what is the largest fall from a peak? | `code-tracer` (watches), `value-table`, `array-strip` (bars) | Trap: maximum minus minimum ignores order; the minimum may come before the maximum. Edge: initialising a running maximum to 0 fails for negative series (start from the first element); an empty list needs a decision. Answer: $\frac{120 - 80}{120} = \frac{1}{3}$ | N, T, K, C |

Transfer screens: lesson 13 finds the first stop-loss breach; lesson 14 lines up dates with price changes and lists every pair of stocks for a correlation check; lesson 15 computes a maximum drawdown, one of the three 1.1 exit quantities.

**Level Y4: Functions** (`lvl.pythink.functions`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 16 | `lsn.pythink.def-return` Function contracts: return values and None | Write functions whose docstring states inputs, output and errors, predict the value of every path through a function including the implicit `None`, and return several results as one tuple | `sharpe(r)` returns `m / s`, but its first line is `if len(r) < 2: return`. A report halves every fund's Sharpe ratio and crashes on one fund with `TypeError: unsupported operand type(s) for /: 'NoneType' and 'int'`. Which path did that fund take, and where should the error have been raised? | `code-tracer` (frames, paths highlighted), `predict-output`, `code-cell` | Trap: a path without a value returns 0, or fails at once (it returns `None`, and the crash appears later, in the caller). Edge: a `return` inside a loop ends the function on the first pass; `return m, s` returns one tuple the caller can unpack; 0.4 lesson 29's `print` against `return` appears only as a quiz distractor; lesson 36 finishes the story by raising at the boundary [verified] | T, C, K, T |
| 17 | `lsn.pythink.arguments` Arguments and the mutable default | Bind call arguments to parameters for any mix of positional, keyword, default, `*args`, `**kwargs` and keyword-only parameters, and avoid the mutable default | `def add_trade(t, book=[]): book.append(t); return book`. Call it twice with different trades. What does the second call return? | `token-tray` (argument binding), `code-tracer`, `predict-output` | Trap: a default is evaluated at each call (it is evaluated once, when `def` runs, so `book=[]` is shared). Edge: the `None` sentinel pattern; a positional argument after a keyword argument is a `SyntaxError`; `f(*xs)` unpacks | S, T, T, C |
| 18 | `lsn.pythink.scope-frames` Scope and the call stack | Determine which binding each name refers to under the local, enclosing, global and built-in rule, and explain an `UnboundLocalError` from the code that caused it | `count = 0` then `def bump(): count += 1` raises `UnboundLocalError`, yet `def show(): print(count)` works. Why? | `code-tracer` (scope highlight), `diagnostic-reader` | Trap: a name is local only from the line it is assigned (an assignment anywhere in a function makes it local throughout). Edge: `sum = 0` shadows the built-in and breaks a later `sum(xs)`; changing a global list needs no `global` | S, C, T, M |
| 19 | `lsn.pythink.key-functions` Functions as values: key functions and sorting | Pass functions as arguments, write `lambda` key functions, and sort records by several keys using the stability of Python's sort | Sort trades by symbol and, within a symbol, by time, using two sorts. Which sort goes first? | `sort-lab` (key, stability), `predict-output`, `code-cell` | Trap: sort by the main key first (the last sort decides the main order, so sort by time first, then by symbol). Edge: `sorted` returns a new list while `.sort()` returns `None`; a tuple key `(t.sym, -t.qty)` sorts descending on quantity; `max(..., key=...)` returns the first maximum | O, T, K, C |
| 20 | `lsn.pythink.closures` Closures and late binding | Predict the values captured by functions made in a loop, and write a closure that keeps private state with `nonlocal` | `fs = [lambda: i for i in range(3)]`; `[f() for f in fs]` gives `[2, 2, 2]`. Why not `[0, 1, 2]`? | `code-tracer` (closure cells), `predict-output` | Trap: a closure captures the value at creation (it captures the variable, read when called). Edge: `lambda i=i: i` freezes the value; a counter factory needs `nonlocal` to rebind | T, T, C, K |
| 21 | `lsn.pythink.recursion` Recursion and the call stack | Trace a recursive function's frames, identify its base case and its progress towards it, and predict when it exceeds the recursion limit | How many ways can you climb 10 stairs taking 1 or 2 at a time? The recursive answer is short, but slow for 40 stairs. Why? | `recursion-tree`, `code-tracer`, `predict-output` | Trap: a base case that is never reached, giving `RecursionError`; recomputing the same subproblems. Edge: CPython's default limit is about 1,000 frames, so a recursive sum of 10,000 items fails where a loop succeeds. Answers: 89 ways; calls grow like the Fibonacci numbers | N, N, T, C |

Transfer screens: lesson 17 books trades into a blotter; lesson 19 sorts that blotter; lesson 21 counts the up-down paths of a price over 10 steps, a preview of the binomial tree in 1.7. Lesson 21 is a working preview; 1.8 owns recursion, and `recursion-tree` is pulled forward for it (decision 19).

**Level Y5: Collections** (`lvl.pythink.collections`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 22 | `lsn.pythink.lists` Lists: changing in place | Distinguish list methods that change the list from operations that build a new one, and predict aliasing in nested lists built with `*` | `grid = [[0] * 3] * 3; grid[0][0] = 1`. Print `grid` | `code-tracer` (predict), `node-link` (heap), `predict-output` | Trap: `x = x.sort()` keeps the sorted list (it sets `x` to `None`); `[[0] * 3] * 3` makes three references to one row. Edge: `list.remove` removes only the first match | T, S, T, C |
| 23 | `lsn.pythink.copies` Copies: shallow and deep | Predict which changes show through after `b = a`, `a[:]`, `list(a)`, `copy.copy(a)` and `copy.deepcopy(a)` on nested lists, and choose the right copy | A scenario copies a book `[["AAPL", 100], ["MSFT", 50]]` with `scenario = base[:]` and shocks a quantity. The base book changes. Why? | `node-link` (heap), `code-tracer`, `predict-output` | Trap: a slice copy is independent all the way down (it copies only the outer list). Edge: removing items while iterating skips some: `[-1, -2, 3]` with `remove` on negatives leaves `[-2, 3]` [verified] | S, T, T, M |
| 24 | `lsn.pythink.tuples` Tuples and unpacking | Use tuples as fixed records, unpack them in assignments, loops and returns (including `*rest`), and predict when a tuple's contents can still change | Swap two variables in one line with `a, b = b, a`. How does it work with no temporary? | `code-tracer`, `node-link`, `predict-output` | Trap: a tuple's contents can never change (a list inside it can). Edge: `t[0] += [2]` on `t = ([1], 2)` extends the list and then raises `TypeError` [verified]; `(1)` is an int and `(1,)` a tuple | T, C, T, E |
| 25 | `lsn.pythink.dicts` Dictionaries: lookup by key | Build, read and update dictionaries, use `get`, `setdefault` and counting patterns, and explain why keys must be hashable | Count each trader's trades in a list of 10,000. Then try `[sym, date]` as a key | `hash-table` (basic), `diagnostic-reader`, `predict-output` | Trap: `d[k]` returns `None` for a missing key (it raises `KeyError`). Edge: `1`, `1.0` and `True` are the same key, so `{1: "a", 1.0: "b", True: "c"}` is `{1: 'c'}` [verified]; dicts keep insertion order; changing a dict's size while iterating raises `RuntimeError` | N, T, C, K |
| 26 | `lsn.pythink.sets` Sets and fast membership | Use sets for membership, de-duplication and set algebra, and predict when a set beats a list as the collection grows | Which tickers are on both the index list and your watchlist? Then: checking 10,000 orders against a 100,000-name restricted list takes minutes. Why? | `venn-diagram`, `complexity-lab` (race), `hash-table` | Trap: `{}` is an empty set (it is an empty dict). Edge: `set("AAPL")` is the set of letters; sets have no order to rely on; `frozenset` can be a key | M, C, N, T |
| 27 | `lsn.pythink.comprehensions` Comprehensions | Translate between loops and list, dict and set comprehensions with filters and nested loops, and keep a loop where a comprehension would hide side effects | Turn the six-line loop that keeps the positive returns into one line | `parsons`, `code-blanks`, `predict-output` | Trap: confusing the filter `[x for x in xs if x > 0]` with the conditional `[x if x > 0 else 0 for x in xs]`. Edge: nested comprehensions read left to right like nested loops; the loop variable does not leak | O, T, K, C |
| 28 | `lsn.pythink.costs` What operations cost | Predict how the running time of common list, dict, set and string operations grows with size, and rewrite a quadratic loop as a linear one | De-duplicating 100,000 trade ids with `if x not in seen_list` takes minutes; with a set, milliseconds. Count the comparisons | `complexity-lab`, `bench-lab` (race), `code-cell` (complexity test) | Trap: a one-line loop body is cheap (`x in a_list`, `insert(0, x)` and `s += c` each hide work proportional to the size). Edge: `append` is constant time on average despite occasional resizing; `v in d.values()` is a linear scan | C, M, N, K |

Transfer screens: lesson 23 stress-tests a nested book; lesson 25 counts trades per trader; lesson 26 screens orders against a restricted list; lesson 28 de-duplicates trade ids. Lesson 28 is a working preview; 1.8 owns complexity.

#### Course B: Building Real Programs (`crs.pybuild`, 5 levels, 27 lessons)

From snippets to programs that read real files, fail loudly and usefully, run from the command line, live in modules and environments, and model their domain with classes. The course ends with the decomposition of a real specification, a first-in-first-out trade ledger, which the Trade Ledger project then extends.

**Level B1: Iteration and functional tools** (`lvl.pybuild.iteration`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 29 | `lsn.pybuild.iterators` The iteration protocol | Explain a `for` loop in terms of `iter` and `next`, distinguish iterables from iterators, and predict the result of reusing an exhausted iterator | `pairs = zip(dates, prices)`; `list(pairs)` shows the pairs and a second `list(pairs)` shows `[]`. Where did they go? | `pipeline-flow` (iter), `code-tracer`, `predict-output` | Trap: `zip`, `map`, `filter`, files and generators can be read twice (they are single-use). Edge: `x in an_iterator` consumes it up to the match; a list is iterable but `next([1, 2])` raises `TypeError` | T, T, C, M |
| 30 | `lsn.pybuild.generators` Generators and lazy pipelines | Write generator functions and generator expressions, chain them into a lazy pipeline, and predict when each value is computed | Sum the squared returns in a 50-million-line tick file without running out of memory | `pipeline-flow` (iter), `code-tracer` (suspended frames), `predict-output` | Trap: calling a generator function runs its body (it returns a generator; the body runs on `next`). Edge: `sum(x * x for x in xs)` needs no extra brackets; summing the same generator twice gives 52 then 0 for `[3, 1, 4, 1, 5]` [verified] | T, O, T, C |
| 31 | `lsn.pybuild.itertools` itertools: combining iterators | Use `product`, `permutations`, `combinations`, `combinations_with_replacement`, `accumulate`, `islice`, `chain` and `groupby` in place of hand-written loops, matching each combinatoric generator to one of 0.3's four counting cases | Three nested loops over 10 stocks print 1,000 "baskets of three", with repeats like (A, A, B) and reorderings like (B, A, C). 0.3 counted 120 baskets. Which `itertools` call yields exactly those 120, and which yield the 1,000, the 720 and the 220? | `counting-slots`, `predict-output`, `code-cell` | Trap: `groupby` groups all equal keys (it groups consecutive ones, so unsorted input splits groups: `"aabba"` gives three groups). Edge: `accumulate(xs, max)` is a running maximum; $\binom{50}{25} \approx 1.26 \times 10^{14}$, so take the first few with `islice` and never list them all. Answers: `product(..., repeat=3)` 1,000, `permutations` 720, `combinations` 120, `combinations_with_replacement` 220 [verified] | N, N, T, K |
| 32 | `lsn.pybuild.collections` collections: Counter, defaultdict, deque, namedtuple | Choose among `Counter`, `defaultdict`, `deque` and `namedtuple` for a counting, grouping, queueing or record task, and predict their behaviour on missing keys and full queues | Keep the last 20 prices for a moving average as each new price arrives. `list.pop(0)` works; why is it slow, and what is better? | `array-strip` (ring), `hash-table`, `predict-output` | Trap: reading a missing key from a `defaultdict` changes nothing (it inserts the key). Edge: `Counter` subtraction drops counts that fall to zero or below [verified]; `deque(maxlen=20)` discards from the far end without warning | C, T, T, K |
| 33 | `lsn.pybuild.decorators` Decorators and caching | Write a decorator that wraps a function (timing or counting calls) with `functools.wraps`, and apply `lru_cache` to make an exponential recursion linear | The stairs function of lesson 21 takes seconds for 35 stairs. One line above it makes it instant. What did the line do? | `recursion-tree` (memo), `code-tracer`, `code-cell` | Trap: `lru_cache` works on any function (unhashable arguments raise `TypeError`, and caching a function with side effects or randomness returns stale results). Edge: `@dec` is exactly `f = dec(f)`; without `wraps` the name and docstring are lost; `partial` freezes arguments | T, N, C, K |

Transfer screens: lesson 30 streams a tick file; lesson 31 counts portfolios and computes a running high with `accumulate`; lesson 32 keeps a rolling window of prices.

**Level B2: Errors and debugging** (`lvl.pybuild.errors`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 34 | `lsn.pybuild.tracebacks` Reading tracebacks | Locate the failing line and the root cause in a multi-frame traceback, and name the exception each common mistake raises | A 20-line traceback ends in `KeyError: 'close'` deep inside pandas, but the bug is in your code. Which frame do you read first? | `diagnostic-reader`, `code-tracer` (unwinding) | Trap: the last frame printed is where the bug is (it is where the error was raised; the bug is usually in the deepest frame that belongs to your own files, and sometimes in the data that reached it). Edge: chained exceptions ("During handling of the above exception, another exception occurred"): the first is the root cause; messages change between versions ("float division by zero" on Python 3.11, "division by zero" on 3.14), so read the exception type first; 0.4 lesson 30's bottom-up reading is assumed [verified] | S, C, M, S |
| 35 | `lsn.pybuild.try-except` Handling exceptions | Write `try`/`except`/`else`/`finally` blocks whose `try` covers only the line that can fail and whose `except` names only the expected exception, and predict which blocks run in every case | A price parser wraps 15 lines in `try: ... except KeyError: return {}`. A misspelt column name now returns an empty report, though the file is fine. Which line raised the `KeyError`? | `code-tracer` (unwinding), `predict-output`, `code-cell` | Trap: a wide `try` block is safer (it also catches the same exception type from lines it was never meant to guard; keep the `try` to the line that can fail and put the rest in `else`). Edge: `finally` runs after a `return`; a `return` inside `finally` replaces the exception, and Python 3.14 warns about it; `else` runs only when nothing was raised; 0.4 lesson 30's rule against a bare `except:` is assumed [verified] | O, T, C, K |
| 36 | `lsn.pybuild.raising` Raising errors and validating input | Raise exceptions with informative messages at a function's boundary, define a custom exception class, and choose between `raise`, `assert` and a sentinel return | `annualised_vol([])` returns 0.0 and a risk report shows a portfolio with no risk. What should it have done? | `code-cell`, `choice`, `diagnostic-reader` | Trap: `assert` for input validation (it is removed under `python -O`); sentinels such as `-1` or `0` that callers misread. Edge: `raise ... from err` keeps the cause; check-first (look before you leap) against try-first (easier to ask forgiveness) when a file can vanish between the check and the use | C, M, K, C |
| 37 | `lsn.pybuild.debugging` Debugging systematically | Find a bug by stating a hypothesis, setting a breakpoint, inspecting values and shrinking the input to a minimal failing case; log instead of printing | Your average daily return is 0.0019; a colleague's spreadsheet says 0.0025 for the same data. Find the line where the two part | `code-tracer` (debug), `value-table` | Trap: changing code at random until the number looks right. Edge: a bug that vanishes when a `print` is added, here because the `print` consumed an iterator; `logging` levels let diagnostic output stay in the code switched off | N, S, C, O |
| 38 | `lsn.pybuild.context-managers` Context managers and cleanup | Use `with` to guarantee cleanup, say what happens to an open file when an exception is raised inside the block, and write a context manager with `contextlib` | A script opens 10,000 files in a loop and dies with "Too many open files". Fix it with one keyword | `code-tracer` (unwinding), `code-cell` | Trap: `f.close()` on the last line always runs (not after an exception). Edge: a `with` block makes no new scope; a `timer()` context manager built with `@contextmanager` and `try`/`finally` | T, C, K, O |

Transfer screens: lesson 36 validates order input at an API boundary; lesson 37 reconciles a P&L mismatch with a colleague's spreadsheet.

**Level B3: Files and the outside world** (`lvl.pybuild.files`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 39 | `lsn.pybuild.files-paths` Files and paths | Read and write text files with `open` and `pathlib`, resolve relative paths against the working directory, anchor a script's data paths to the script itself, and choose modes and encodings deliberately | `python analysis/report.py`, run from the project folder, reads `data/prices.csv`. A scheduler runs the same script from your home folder and it fails. Make it work from anywhere without writing your home path into the code | `workspace-sim`, `file-tree`, `code-cell` | Trap: relative paths are relative to the script's folder (they are relative to the current working directory). Edge: `Path(__file__).resolve().parent / "data"`; mode `"w"` empties the file the moment it opens; read a huge file line by line; pass `encoding="utf-8"`, because the default differs between Windows and Linux [recalled]. 0.4 lessons 20 and 31 (running from the wrong folder) are assumed | E, C, T, G |
| 40 | `lsn.pybuild.csv` Reading CSV files correctly | Parse CSV with the `csv` module, including quoted fields and missing values, convert fields to the right types, and write CSV other programs read | `2024-03-01,"Smith, J",1,250.00` splits into 5 fields with `split(",")`. How many fields does it really have? | `csv-inspector` (csv module), `code-cell` | Trap: `line.split(",")`. Edge: every field arrives as a string and a missing value as `""`; write with `newline=""` or Windows shows blank lines; `"1,234"` needs cleaning before `float` | N, M, K, C |
| 41 | `lsn.pybuild.json` JSON and nested data | Load, navigate, transform and save nested JSON, writing the access path to any value and handling missing keys | An exchange returns an order book as nested JSON. Write the path to the best bid price | `json-explorer`, `code-cell` | Trap: a dict round-trips through JSON unchanged (integer keys come back as strings). Edge: `NaN` is not valid JSON though Python writes it by default; `datetime` is not serialisable; prices sent as strings keep exact decimals | E, T, C, K |
| 42 | `lsn.pybuild.datetime` Dates, times and time zones | Do arithmetic with `date`, `datetime` and `timedelta`, parse and format ISO 8601, and convert aware times between zones across daylight-saving changes | New York closes at 16:00 local time. What time is that in London on 7, 10 and 31 March 2025? | `time-series-lab` (tz), `number-line` (time axis), `predict-output` | Trap: a fixed five-hour offset (the gap is 4 hours between the US and UK clock changes: 21:00, 20:00 and 21:00 London time) [verified]. Edge: comparing naive with aware times raises `TypeError`; 01:30 on the autumn change day happens twice (`fold`); `datetime.utcnow()` returns a naive time and is deprecated from Python 3.12 | E, N, C, T |
| 43 | `lsn.pybuild.regex` Regular expressions | Write a pattern that matches every positive example and no negative one using classes, quantifiers, anchors and groups, and extract fields with groups | Pull the side, size, ticker and price out of 1,000 chat lines like `bought 200 AAPL @ 189.50` | `regex-lab` | Trap: greedy `.*` takes too much; `re.search` without anchors accepts junk around a match (validate with `re.fullmatch`). Edge: raw strings (`r"\d"`); `.` does not match a newline; parse CSV with `csv`, not a regex | E, E, T, C |
| 44 | `lsn.pybuild.cli` Programs on the command line | Build a script that reads arguments with `argparse`, reads and writes standard streams, returns a meaningful exit code, and runs only when executed directly | `python vol.py prices.csv --window 20` prints an annualised volatility. What turns those words into variables? | `workspace-sim`, `shell-sim`, `code-cell` | Trap: top-level code runs only when the file is run (it also runs on import, which is why `if __name__ == "__main__":` exists). Edge: `sys.argv[0]` is the script; `type=int` in `argparse`; `sys.exit(1)` against an uncaught exception | T, G, C, K |

Transfer screens: lesson 41 reads an order book; lesson 42 converts the New York close across the daylight-saving gap; lesson 43 parses trader chat; lesson 44 builds a volatility command-line tool.

**Level B4: Modules, environments and readable code** (`lvl.pybuild.modules`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 45 | `lsn.pybuild.imports` Modules, packages and imports | Predict which file an `import` loads from the search path, organise code into a package, and diagnose shadowing | You save `random.py` in your project and `random.randint` stops existing. Why? | `search-path` (sys.path), `diagnostic-reader`, `file-tree` | Trap: naming a file after a library module. Edge: a module runs once per process (cached in `sys.modules`), so a notebook needs a restart or `importlib.reload` after an edit; `from x import *` hides where names come from; circular imports | O, C, T, M |
| 46 | `lsn.pybuild.venv` Virtual environments and dependencies | Create and activate a virtual environment, install packages into the right interpreter, and pin versions so another machine reproduces the environment | `pip install pandas` succeeds and `import pandas` then fails. Two Pythons, one `pip` | `search-path` (PATH), `shell-sim` | Trap: `pip` installs for the `python` you run (it may belong to another interpreter; use `python -m pip`). Edge: unpinned versions change behaviour silently (pandas 2 to 3, lesson 81); never commit the environment folder | O, C, G, M |
| 47 | `lsn.pybuild.notebooks` Notebooks and reproducibility | Identify hidden state in a notebook run out of order, and restructure an analysis so "restart and run all" reproduces every number | A notebook shows a Sharpe ratio of 2.1. "Restart and run all" gives 0.4. Which cell order produced 2.1? | `code-cell` (notebook), `predict-output` | Trap: trusting outputs in a notebook that has been edited since they ran. Edge: unseeded randomness; a data file changed on disk; a function deleted from a cell that still lives in memory | O, C, M, C |
| 48 | `lsn.pybuild.readable-code` Readable code: style, names and documentation | Rewrite a working but unreadable function to PEP 8 with descriptive names, a docstring, small functions and named constants, and use a formatter and a linter | Two versions of one volatility function. Which would you approve in a code review, and why? | `code-annotator`, `diff-view` | Trap: comments that restate the code instead of giving the reason. Edge: `TRADING_DAYS = 252` as a named constant; a linter catches unused names and shadowed built-ins; a formatter ends arguments about layout | S, M, C, O |

Transfer screens: lesson 47 reproduces a colleague's backtest; lesson 48 reviews a volatility function.

**Level B5: Objects and types** (`lvl.pybuild.objects`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 49 | `lsn.pybuild.classes` Classes and instances | Define a class with `__init__`, attributes and methods, trace attribute lookup from instance to class, and predict the effect of class attributes | Two `Position` objects made from one class share `trades = []` written at class level. Every trade appears in both | `code-tracer` (objects), `node-link` (heap), `code-cell` | Trap: a list written in the class body belongs to each instance (it is shared by all of them). Edge: assigning `self.x` creates an instance attribute that hides the class attribute; `self` is only the first parameter's conventional name | S, T, K, C |
| 50 | `lsn.pybuild.special-methods` Special methods | Implement `__repr__`, `__eq__`, `__hash__`, `__lt__` and arithmetic special methods so objects print, compare, sort and add correctly | `Money(5, "GBP") == Money(5, "GBP")` is `False`, and `print` shows `<__main__.Money object at 0x...>`. Make them behave | `code-cell`, `predict-output` | Trap: defining `__eq__` alone keeps instances hashable (it removes `__hash__`, so they cannot go in a set); adding GBP to USD without complaint. Edge: return `NotImplemented` for unsupported types rather than raising; `__radd__` so `sum()` can start from 0 | T, C, K, M |
| 51 | `lsn.pybuild.dataclasses` Dataclasses for records | Define records with `@dataclass`, including `frozen`, `order` and `field(default_factory=...)`, and predict the generated `__init__`, `__repr__` and `__eq__` | A 25-line `Trade` class shrinks to 6 lines. What did the decorator write for you? | `code-annotator`, `predict-output`, `code-cell` | Trap: `holdings: list = []` in a dataclass (it raises `ValueError` and asks for `default_factory`) [verified]. Edge: `frozen=True` makes instances hashable, though a list inside can still change; a field without a default cannot follow one with a default | T, C, K, C |
| 52 | `lsn.pybuild.inheritance` Inheritance, composition and interfaces | Choose between inheritance and composition for a design, call a parent method with `super()`, and write code that depends on an interface (duck typing or `Protocol`) | An `Option` and a `Stock` both need `value(price)` so a `Portfolio` can total them. A common base class, or not? | `node-link` (class diagram) [mode to add], `code-cell`, `choice` | Trap: inheriting for code reuse without an "is a" relation (a portfolio is not a list). Edge: overriding `__init__` without `super().__init__()` leaves attributes missing; `abc.ABC` with `@abstractmethod` refuses to build an incomplete class; method resolution order with two parents | C, T, K, M |
| 53 | `lsn.pybuild.properties` Properties and invariants | Protect a class invariant with validation in `__init__` and `@property`, and explain the leading-underscore convention | A `Portfolio` must never hold negative cash, yet `p.cash = -1e6` succeeds. Stop it without changing any caller | `code-cell`, `code-tracer` | Trap: validating in `__init__` only, while attributes can be reassigned later. Edge: a property without a setter is read-only (`AttributeError` on assignment) [verified]; a computed property (market value) never goes stale; Python has no truly private attributes | T, C, K, C |
| 54 | `lsn.pybuild.type-hints` Type hints and static checking | Annotate functions and classes with `list[float]`, `dict[str, int]`, `X \| None`, unions and `Callable`, and read a type checker's error to find a bug before running | `def mean(xs: list[float]) -> float` is called with a dict and fails in production at 2 a.m. A checker would have flagged it at your desk. How? | `diagnostic-reader` (mypy) [mode to add], `code-annotator`, `code-cell` | Trap: hints are enforced at run time (they are not). Edge: `X \| None` forces the `None` case to be handled; `Any` switches checking off; a checker accepts an `int` where a `float` is expected | C, M, T, E |
| 55 | `lsn.pybuild.design` Designing a program: a trade ledger | Decompose a specification into functions and classes, implement first-in-first-out matching of buys and sells with a `deque`, and test it on hand-worked cases | Buy 100 at £10, buy 100 at £12, sell 150 at £13. What is the realised profit under first in, first out? | `array-strip` (queue of lots), `code-cell`, `parsons` | Trap: averaging the cost (that gives £300, a legitimate convention but not FIFO, which gives $100 \times 3 + 50 \times 1 = £350$). Edge: a sale larger than the position must raise; partial lots; fees reduce realised profit | N, N, O, K |

Transfer screens: lesson 50 refuses to add pounds to dollars; lesson 53 enforces a cash invariant; lesson 55 computes FIFO realised profit, the core of the Trade Ledger project.

#### Course A: Arrays and Simulation (`crs.arrays`, 3 levels, 20 lessons)

NumPy as the language of numerical work, and simulation as the quant's calculator. The course follows McKinney chapter 4 and appendix A for arrays, then adds what a quantitative programme expects and McKinney leaves out: floating-point care in arrays, matrix arithmetic, measured performance, and seeded Monte Carlo with error bars.

**Level A1: Arrays** (`lvl.arrays.ndarray`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 56 | `lsn.arrays.why-arrays` Why arrays | Explain how an array's single dtype and contiguous memory let one expression replace a Python loop, and estimate the speed-up at a given size | Compute the returns of 1,000,000 prices with a loop and with one array expression. Race them | `bench-lab` (race), `ndarray-lab` | Trap: NumPy is faster at every size (for 10 numbers a list wins on call overhead). Edge: an array of Python objects (`dtype=object`) loses the speed; converting a list to an array inside a loop | C, N, M, T |
| 57 | `lsn.arrays.dtypes` Creating arrays and dtypes | Create arrays with `array`, `arange`, `linspace`, `zeros` and `full`, predict dtypes and shapes, and spot integer overflow and float-step surprises | `np.arange(1, 1.3, 0.1)` has four elements, the last 1.3000000000000003. And `np.array([2**62]) * 4` prints `[0]` [verified] | `ndarray-lab` (dtype), `predict-output` | Trap: NumPy integers grow like Python's (`int64` wraps silently in arrays; a NumPy scalar at least warns). Edge: `arange` with a float step (prefer `linspace`); `np.array([1, 2]) / 2` is float; mixing numbers and strings makes a string array | T, T, N, C |
| 58 | `lsn.arrays.shape-axes` Shape, axes and reductions | Predict the shape after `reshape`, reductions along an axis (with and without `keepdims`) and transposition for arrays of up to three dimensions | A 252 × 500 array holds a year of daily returns for 500 stocks. Is `r.mean(axis=0)` each day's average or each stock's? | `ndarray-lab` (axes), `cell-grid` | Trap: `axis=0` means "along each row" (it collapses the rows, giving one value per column: each stock's mean). Edge: `reshape(-1)` infers one dimension; `keepdims=True` keeps shape (1, 500) for broadcasting back | E, E, C, N |
| 59 | `lsn.arrays.indexing` Indexing and slicing in two dimensions | Write indexing expressions that select any row, column, block or strided sub-grid of a 2D array, and predict each result's shape | From the returns array, take the last 20 days of the first 10 stocks, and every fifth day of stock 3 | `ndarray-lab` (slice), `cell-grid` | Trap: `a[:, 3]` has shape (252, 1) (an integer index drops the dimension: (252,)); `a[:, [3]]` keeps it [verified]. Edge: negative steps; `a[1][2]` against `a[1, 2]` | E, E, E, C |
| 60 | `lsn.arrays.views-copies` Views, copies and memory | Predict whether an operation returns a view or a copy and whether writing through it changes the original | `window = prices[10:20]; window[:] = 0`. What happened to `prices`? Now do the same with a list | `ndarray-lab` (memory), `node-link` | Trap: NumPy slices copy like list slices (they are views) [verified]. Edge: `reshape` returns a view unless the data is not contiguous, as after a transpose [verified with `np.shares_memory`]; a small view keeps a huge array alive | C, T, M, S |
| 61 | `lsn.arrays.masks` Boolean masks and fancy indexing | Select and change elements with masks combined by `&`, `\|` and `~`, use `np.where` and `np.clip`, and predict which indexing forms return copies | Cap every daily return above +10% or below −10% in one line | `ndarray-lab` (mask), `predict-output` | Trap: `(r > 0) and (r < 0.1)` (it raises "truth value of an array ... is ambiguous") [verified]; `r > 0 & r < 0.1` binds wrongly without brackets. Edge: `r[mask] = 0` changes `r` but `r[mask][0] = 1` does not [verified]; the mean of an empty selection is `nan` with a warning | E, T, C, K |

Transfer screens: lesson 56 computes a million returns; lesson 58 reads a returns matrix of 500 stocks; lesson 61 winsorises returns.

**Level A2: Computing with arrays** (`lvl.arrays.compute`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 62 | `lsn.arrays.broadcasting` Broadcasting | Decide whether two shapes broadcast and predict the result shape by aligning from the right, and use broadcasting to demean columns or build outer products | Subtract each stock's mean return from its column of the 252 × 500 matrix with no loop. Then subtract each day's mean instead | `broadcast-lab` | Trap: (252, 500) minus a (252,) array works (it fails; it needs shape (252, 1), from `[:, None]` or `keepdims=True`). Edge: (n,) against (n, 1) silently builds an n × n matrix; broadcasting can create large temporaries | E, E, C, K |
| 63 | `lsn.arrays.reductions` Universal functions and summary statistics | Apply element-wise functions and reductions (`sum`, `mean`, `std`, `argmax`, `cumsum`) along chosen axes, and choose `ddof` for the population or the sample standard deviation | `np.std([1, 2, 3, 4])` gives 1.118 but pandas gives 1.291 for the same data. Which is wrong? | `ndarray-lab` (reduce), `predict-output`, `derivation-steps` | Trap: one of them is a bug (NumPy defaults to `ddof=0`, pandas to `ddof=1`: $\sqrt{1.25} = 1.118$ against $\sqrt{5/3} = 1.291$) [verified]. Edge: `argmax` returns the first maximum; the mean of an int array is a float. Standard deviation is defined here as $s = \sqrt{\frac{1}{n - d}\sum (x_i - \bar{x})^2}$ with $d$ the `ddof`; 1.6 proves why $d = 1$ removes bias | N, N, C, T |
| 64 | `lsn.arrays.vectorise` Vectorising loops | Rewrite running-total, running-maximum, difference and conditional loops as `cumsum`, `maximum.accumulate`, `diff` and `where`, and confirm both versions agree | Your drawdown loop from lesson 15 takes 2 seconds on ten years of minute bars. Write it in three NumPy calls | `code-cell` (complexity test), `array-strip` (bars), `bench-lab` | Trap: `np.vectorize` vectorises (it is a loop in disguise). Edge: `np.diff` returns one fewer element, so returns and dates must be realigned; drawdown is `p / np.maximum.accumulate(p) - 1` | K, T, E, C |
| 65 | `lsn.arrays.sort-search` Sorting, searching and quantiles | Use `sort`, `argsort`, `searchsorted`, `percentile` and `quantile` to rank, locate and estimate quantiles, and state the interpolation rule used | What is the 5% worst daily P&L in 1,000 days (a historical value-at-risk)? Sort and count, then ask NumPy | `array-strip` (sorted bars), `number-line`, `predict-output` | Trap: `argsort` returns ranks (it returns the indices that sort; ranks are `argsort` of `argsort`) [verified]. Edge: the default quantile interpolates, so the 5% quantile of `0..999` is 49.95, not an observed value [verified]; `searchsorted` with `side="left"` or `"right"` on ties | T, N, C, E |
| 66 | `lsn.arrays.nan-float` Missing values and floating point in arrays | Predict how `nan` spreads through arithmetic and reductions, use `nan`-aware functions, choose a summation that limits rounding error, compute $\log \sum e^{x_i}$ without overflow, and test results with `np.isfinite` instead of waiting for a warning | `np.mean([1.0, np.nan, 3.0])` is `nan`. And which is closest to 100,000: a `for` loop adding 0.1 a million times, `np.sum` of the same, or `math.fsum`? | `float-inspector` (summation), `predict-output` | Trap: `x == np.nan` finds missing values (it is always `False`; use `np.isnan`). Edge: the loop drifts to 100000.00000133288, `np.sum` (pairwise) gives 100000.00000000003 and `math.fsum` exactly 100000.0; built-in `sum` gives 100000.0 on Python 3.12 and later, which compensate, but the loop's value on 3.11; `np.exp(1000)` is `inf`, so subtract the maximum first (log-sum-exp, 0.3 lesson 59, used by every softmax in 2.1); NumPy warns about the overflow on your machine but cannot in the app, because WebAssembly has no floating-point flags [verified on both runtimes] | T, T, C, N |
| 67 | `lsn.arrays.linalg` Matrix arithmetic in NumPy | Distinguish `@` from `*`, predict the shape of matrix products, solve a linear system with `solve` rather than an explicit inverse, and check that the result is finite before trusting it | A portfolio has weights $\mathbf{w}$ and covariance matrix $\mathbf{\Sigma}$. Which computes its variance $\mathbf{w}^\top \mathbf{\Sigma} \mathbf{w}$: `w * S * w`, `w @ S @ w` or `S @ w @ w`? | `broadcast-lab` (matmul), `matrix-multiply`, `predict-output` | Trap: `*` is matrix multiplication (it is element-wise). Edge: a 1-D array has no row or column orientation, so `w @ S @ w` works; `inv(A) @ b` is slower and less accurate than `solve(A, b)`; a singular matrix raises `LinAlgError` in NumPy on your machine but returns `[nan nan]` silently in the app's WebAssembly NumPy, so test `np.isfinite` or the condition number; `lstsq` returns in 1.4 and 1.6 [verified on both runtimes] | E, C, N, T |
| 68 | `lsn.arrays.speed` Measuring and improving speed | Measure code with `timeit` and a profiler, find the part that dominates the run time, and decide whether vectorising, a better algorithm or neither is worth doing | A backtest takes 40 minutes. Rewriting the signal in NumPy saved 30 seconds. Where did the other 39 minutes go? | `bench-lab` (race; profile mode is P1), `code-cell` | Trap: optimising before measuring; timing one run. Edge: Amdahl's law: speeding up a fraction $p$ of the work by a factor $s$ gives an overall speed-up of $\frac{1}{(1 - p) + p/s}$, so a $10\times$ gain on 5% of the work saves at most 4.5%; `float32` halves memory at the cost of precision | N, C, O, M |

Transfer screens: lesson 62 demeans a returns matrix; lesson 65 computes historical value-at-risk; lesson 67 computes portfolio variance (homework A2 builds $\mathbf{\Sigma}$ from volatilities and correlations); lesson 68 profiles a backtest.

**Level A3: Randomness and simulation** (`lvl.arrays.simulation`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 69 | `lsn.arrays.random-seeds` Random numbers and reproducibility | Generate random numbers with `random` and `numpy.random.default_rng`, seed them so a result reproduces exactly, and give parallel simulations independent streams | Two colleagues run "the same" simulation and get different answers; you rerun yours and get a third. Make all three agree | `sim-runner`, `code-cell`, `predict-output` | Trap: seeding inside the loop (it restarts the stream, so every iteration draws the same numbers). Edge: pseudo-random means deterministic; mixing the legacy `np.random.seed` with `Generator` objects; `SeedSequence.spawn` for parallel streams; `secrets`, never `random`, for anything security-related | T, C, M, K |
| 70 | `lsn.arrays.monte-carlo` Monte Carlo estimates and their error | Estimate a probability or an expectation by simulation, attach a standard error, report only the digits it supports, and predict how many trials a target error needs | Estimate the chance that two dice total 8 with 100 rolls, then 10,000. Each run prints six decimal places. How many of them can you trust? | `sim-runner`, `plot-2d` (convergence), `numeric-input`, `derivation-steps` | Trap: a simulated estimate is as precise as the digits it prints (at 10,000 rolls the standard error of the estimate of $\frac{5}{36}$ is $\sqrt{p(1 - p)/n} \approx 0.0035$, so only the second decimal place is settled). Edge: the $1/\sqrt{n}$ law of 0.3 lesson 113 means 100 times the trials for 10 times the precision; a rare event needs its relative error, $\sqrt{(1 - p)/(np)}$, which asks for about $10^6$ trials to reach 10% at $p = 10^{-4}$. The learner derives $\text{Var}(\bar{X}) = \sigma^2/n$ from the variance of a sum of independent draws, stated here and proved in 1.5 lesson 97 [verified] | N, N, C, N |
| 71 | `lsn.arrays.vectorised-sim` From a simulation loop to arrays | Rewrite a loop-based simulation as operations on a trials × steps array, and check that both versions agree statistically | Simulating 100,000 games of "roll until a six" with a `while` loop is slow. How can arrays simulate games of different lengths? | `code-cell`, `bench-lab`, `cell-grid` | Trap: with the same seed, the array version reproduces the loop's numbers (draw order differs; only the distributions agree). Edge: unequal lengths: simulate a fixed maximum and mask, or draw from the geometric distribution directly; memory of trials × steps | C, K, N, M |
| 72 | `lsn.arrays.random-walks` Random walks and the gambler's ruin | Simulate many random walks as cumulative sums of steps, estimate hitting probabilities and times, and compare them with the exact formula | Start with £10 and bet £1 on fair coin flips until you have £20 or £0. What is the chance of reaching £20, and how many flips does it take on average? | `path-simulator`, `sim-runner`, `plot-2d` | Trap: after a losing streak a win is due. Edge: with a fair coin the answers are $\frac{1}{2}$ and $10 \times 10 = 100$ flips; with $p = 0.49$ the chance of reaching £20 falls to $\frac{1 - (q/p)^{10}}{1 - (q/p)^{20}} \approx 0.401$ [verified]; doubling after each loss wins small amounts often and loses everything rarely | N, N, C, M |
| 73 | `lsn.arrays.price-paths` Simulating price paths | Simulate price paths by compounding random log-returns, explain why prices are modelled multiplicatively, and read the distribution of final prices | Log-returns with mean 0 and volatility 20% a year: is the average price in a year above, below or equal to today's? Simulate 100,000 paths and compare the mean with the median | `path-simulator`, `sim-runner`, `stat-chart` | Trap: zero average log-return means the average price stays put (the mean is $S_0 e^{\sigma^2/2} \approx 1.0202 S_0$ while the median is $S_0$) [verified]. Edge: adding normal price changes lets prices go negative; daily volatility is $\sigma/\sqrt{252}$; most paths end below the mean | C, N, C, K |
| 74 | `lsn.arrays.expected-payoff` Estimating an expected payoff | Estimate the expected payoff of a call-style contract by simulation with a 95% confidence interval, and check it against an exact value | A contract pays $\max(S - 100, 0)$ in a year, with $S = 100\,e^{-\sigma^2/2 + \sigma Z}$: lesson 73's paths with the log drift $-\sigma^2/2$ that keeps the mean price at 100. What is it worth on average, and how sure are you? | `plot-2d` (the payoff $\max(S - 100, 0)$ over the simulated prices), `sim-runner`, `numeric-input` | Trap: building the interval from the standard deviation of the payoffs (use the standard error, $s/\sqrt{n}$). Edge: most payoffs are 0, so the estimate is noisy; pairing each draw $Z$ with $-Z$ (antithetic variates) cuts the error. The exact value for $S_0 = K = 100$, $\sigma = 0.2$ is $7.9656$ from a formula stated here and derived in 1.7; with lesson 73's zero-mean log returns unchanged it would be $9.0962$, so the drift must be stated [verified] | N, N, C, M |
| 75 | `lsn.arrays.scipy` The scientific stack: SciPy | Use `scipy.stats` for distribution functions and quantiles, `scipy.optimize` for root-finding and minimisation, and `scipy.integrate.quad` for integrals, each to check a simulation | Your simulation says $P(Z > 2) \approx 0.0231$. What is the exact value, and which $z$ has 1% above it? | `code-cell`, `plot-2d`, `numeric-input` | Trap: confusing `cdf`, `pdf` and `ppf`; passing the variance as `scale` (it is the standard deviation). Edge: `brentq` needs a sign change on its bracket; `minimize` finds a local minimum from its start. Answers: 0.02275 and 2.3263 [verified] | N, N, C, T |

Transfer screens: lesson 72 is the gambler's ruin with a house edge; lesson 73 simulates lognormal prices; lesson 74 values an option-style payoff; lesson 75 checks a tail probability.

#### Course D: Data, Time Series and Charts (`crs.dataframes`, 6 levels, 32 lessons)

pandas for real, messy financial data, then plotting, then the 1.1 exit. It follows McKinney chapters 5 to 11 (written for pandas 1.4; the lessons teach the pinned pandas 3.0.2 where they differ, section 5) and adds the financial-data discipline a research desk expects: point-in-time joins, look-ahead bias, calendars, splits, and honest charts.

**Level D1: Series and DataFrames** (`lvl.dataframes.basics`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 76 | `lsn.dataframes.series-alignment` Series: values with an index | Create Series with an index, predict the result of arithmetic between Series by label alignment, and locate the `NaN`s alignment introduces | Two price Series, one missing a holiday. `a - b` gives `NaN` on that date. Why not subtract position by position? | `dataframe-lab` (align) | Trap: arithmetic is positional, as in NumPy (it aligns on labels, and the result's index is the sorted union) [verified]. Edge: duplicate labels multiply rows; `.to_numpy()` drops the index and lets misaligned data through; `add(fill_value=0)` [verified] | M, T, C, N |
| 77 | `lsn.dataframes.anatomy` DataFrame anatomy | Inspect a DataFrame's shape, columns, index and dtypes with `info`, `describe` and `head`, and identify columns whose dtype is wrong | `df["volume"].sum()` returns a long string of digits instead of a number. What does `df.dtypes` show? | `dataframe-lab`, `value-table` (frame) | Trap: a column that looks numeric is numeric (a text column, the `str` dtype in pandas 3, concatenates on `sum`: `"100"` and `"250"` give `"100250"`) [verified]. Edge: `describe` skips non-numeric columns without saying so; an integer column with one missing value becomes `float64` unless a nullable dtype is used | M, K, T, N |
| 78 | `lsn.dataframes.selection` Selecting with loc and iloc | Select rows and columns by label with `loc` and by position with `iloc`, and predict the row count of label slices, which include their end | `df.loc["2024-01-02":"2024-01-04"]` returns 3 rows while `df.iloc[0:2]` returns 2. Why do the slices disagree? | `dataframe-lab` (select) | Trap: label slices exclude the end, like Python's (they include it). Edge: `df["a"]` is a Series and `df[["a"]]` a DataFrame; `df[0]` looks up a column named 0; `df.loc["2024-03"]` selects a whole month | N, E, E, C |
| 79 | `lsn.dataframes.filtering` Filtering rows | Filter rows with boolean conditions combined by `&`, `\|` and `~` with brackets, and with `isin`, `between` and `query` | `df[df.ret > 0 & df.vol < 0.3]` raises an error. Fix it and explain the error | `dataframe-lab` (filter), `diagnostic-reader` | Trap: `&` binds after `>` (it binds first, so brackets are needed). Edge: a missing value fails both `r > 0` and the "not positive" test `r <= 0`, yet passes `~(r > 0)` [verified], so the two "complements" differ | K, M, C, E |
| 80 | `lsn.dataframes.new-columns` New columns: vectorised, apply and loops | Add derived columns with vectorised expressions, `np.where`, `np.select` and `assign`, and explain when `apply` and `iterrows` are still the right tool | Add a notional column (price times quantity) to a million trades three ways. Race them | `code-cell`, `bench-lab` (race) | Trap: `iterrows` is a fine default (it is slow and turns each row into an object-dtype Series, losing types). Edge: `apply(axis=1)` for logic with no vector form; `np.select` for several conditions | K, N, C, T |
| 81 | `lsn.dataframes.copy-on-write` Copies, views and chained assignment | Predict whether an assignment changes the original DataFrame under the pinned pandas, and write single-step `loc` assignments that always do | `df[df.qty > 0]["price"] = 0` runs. Did any price change? | `dataframe-lab` (copy), `predict-output` | Trap: chained assignment writes to `df` (under copy-on-write it never does; pandas 3 warns with `ChainedAssignmentError`) [verified]. Edge: `df.loc[df.qty > 0, "price"] = 0` is the one correct form [verified]; older tutorials show `SettingWithCopyWarning` and pandas 2 behaviour | C, T, K, C |

Transfer screens: lesson 76 subtracts two price series across a holiday; lesson 78 selects a trading month; lesson 80 computes trade notionals.

**Level D2: Loading and cleaning** (`lvl.dataframes.cleaning`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 82 | `lsn.dataframes.read-csv` Loading data with read_csv | Load a messy CSV into correctly typed columns with `parse_dates`, `index_col`, `thousands`, `na_values`, `dtype` and `encoding`, after inspecting the raw text | A vendor file has dates like `03/04/2024`, prices like `"1,234.5"` and `n/a` for missing. Load it right first time | `csv-inspector` (pandas), `dataframe-lab` | Trap: `03/04/2024` parses as you meant (it may become 4 March or 3 April; give `format="%d/%m/%Y"`). Edge: identifiers with leading zeros lose them unless read as strings; `to_csv` writes the index as an extra unnamed column | M, C, K, T |
| 83 | `lsn.dataframes.missing` Missing data | Detect, count and treat missing values with `isna`, `dropna`, `fillna`, `ffill` and `interpolate`, and justify each choice by what the gap means | A price series has one gap from a holiday and five days from a vendor outage. Should both be filled the same way? | `dataframe-lab` (missing), `time-series-lab` | Trap: backward fill and interpolation are safe (both use future values). Edge: forward-filling prices is safe but filling missing returns with 0 claims a flat day; `dropna()` on a wide frame drops any row with any gap and can delete most of the data | M, C, N, C |
| 84 | `lsn.dataframes.clean-types` Cleaning text, types and duplicates | Clean string columns with `.str`, convert types with `to_numeric(errors="coerce")` and `to_datetime`, and remove exact and near duplicates | One ticker column holds `AAPL`, `aapl ` and `AAPL.O`. How many distinct stocks are there? | `dataframe-lab`, `code-cell` | Trap: `errors="coerce"` cleans the data (it hides bad rows as `NaN`; count them before and after). Edge: duplicate index labels against duplicate rows; `keep="first"` or `"last"` | N, K, C, M |
| 85 | `lsn.dataframes.sort-rank` Sorting, ranking and counting | Sort by several columns, rank with each tie method, and summarise categories with `value_counts` and `nlargest` | Ten funds are ranked by return and two tie for third. Do they get 3 and 4, both 3, or both 3.5? | `dataframe-lab` (sort), `sort-lab` | Trap: ties get the next ranks in order (the default method is `"average"`: 2.5 and 2.5 for `[5, 3, 3, 1]` ranked high to low) [verified]. Edge: `method="min"` gives competition ranks; `ascending=False` for "best is 1"; the default single-column sort is not guaranteed stable, so pass `kind="stable"` when ties must keep their order | N, O, Q, T |

Transfer screens: lesson 82 loads a vendor price file; lesson 83 treats an outage gap; lesson 85 ranks funds.

**Level D3: Combining and reshaping** (`lvl.dataframes.combine`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 86 | `lsn.dataframes.groupby` Group-by: split, apply, combine | Compute per-group summaries with `groupby` and `agg`, per-row group statistics with `transform`, and predict each result's shape | Average return per sector, then each stock's return minus its sector's average | `groupby-lab` | Trap: `agg` when `transform` is needed (one row per group cannot sit beside one row per stock). Edge: missing group keys are dropped by default; `size` counts rows while `count` skips missing values | E, T, C, K |
| 87 | `lsn.dataframes.merge` Merging and joining tables | Merge two tables on keys with each `how`, predict the row count, and use `validate` and `indicator` to catch duplicate keys and unmatched rows | Merging 1,000 trades with a 500-row reference table returns 1,210 rows. Where did the extra 210 come from? | `join-lab` | Trap: a merge never adds rows (duplicate keys in the lookup table multiply them) [verified in homework D3]. Edge: a key stored as text in one table and as a number in the other raises `ValueError` in pandas 3, while text keys `"7"` and `"007"` match nothing [verified]; overlapping column names gain `_x` and `_y` | N, N, C, K |
| 88 | `lsn.dataframes.merge-asof` Point-in-time joins | Join each trade to the latest quote at or before its time with `merge_asof`, and explain why an exact or nearest join leaks the future | Attach to each trade the bid and ask in force when it happened. Trades and quotes never share a timestamp | `join-lab` (asof) [mode to add], `time-series-lab` | Trap: `direction="nearest"` (it can pick a quote from after the trade). Edge: both frames sorted on the key; `by="ticker"`; `tolerance` refuses stale quotes; company accounts must be joined on their publication date, not the period they describe | S, C, M, T |
| 89 | `lsn.dataframes.concat` Stacking and aligning frames | Stack frames vertically and side by side with `concat`, and predict the shape and the `NaN`s produced by mismatched columns or indexes | Combine twelve monthly files; one spells a column `Close` and the rest `close` | `join-lab` (concat) | Trap: `concat` matches columns by position (it matches by name, so the misspelling makes two half-empty columns). Edge: vertical `concat` repeats index labels (`ignore_index=True`); `axis=1` aligns on the index as an outer join | E, T, Q, M |
| 90 | `lsn.dataframes.reshape` Long and wide: pivot, melt, stack | Convert between long (one row per date and ticker) and wide (one column per ticker) layouts with `pivot`, `pivot_table`, `melt`, `stack` and `unstack` | A long table of (date, ticker, close) for three stocks: make the wide price matrix a correlation matrix needs | `reshape-lab` | Trap: `pivot` and `pivot_table` are interchangeable (`pivot` raises on a duplicate pair; `pivot_table` silently averages it). Edge: a (date, ticker) MultiIndex panel and `xs`; one observation per row as the tidy layout | E, S, C, T |
| 91 | `lsn.dataframes.binning` Binning, categories and quantile portfolios | Bin values with `cut` and `qcut`, encode categories with `get_dummies`, and assign stocks to quantile groups within each date | Each month, split 500 stocks into five groups by last month's return and compare next month's average returns | `reshape-lab` (dummies), `number-line`, `groupby-lab` | Trap: `qcut` over the whole panel (it mixes periods; bin within each date). Edge: equal-width bins with outliers put nearly every stock in one bin; many ties produce duplicate edges; `drop_first` avoids the dummy-variable trap of 1.6 | N, C, K, M |

Transfer screens: lesson 86 computes sector-neutral returns; lesson 88 attaches quotes to trades; lesson 91 builds momentum quintiles, the seed of Stage 2 project 2.

**Level D4: Time series** (`lvl.dataframes.timeseries`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 92 | `lsn.dataframes.dates` Dates, calendars and frequencies | Build a `DatetimeIndex`, generate business-day ranges, select by date strings, convert time zones, and find missing trading days against a calendar | Your file has 250 rows for 2024, but the New York Stock Exchange traded on 252 days. Which are missing? | `time-series-lab` (dates) | Trap: business days are trading days (2024 has 262 weekdays [verified] and 10 exchange holidays). Edge: `tz_localize` attaches a zone while `tz_convert` moves between zones; annualising with calendar days | N, M, Q, E |
| 93 | `lsn.dataframes.returns` Returns in pandas: across time and across assets | Compute simple and log returns from a price Series with `pct_change`, `shift` and `np.log`, aggregate them over time (log returns add, simple returns compound) and across a portfolio (simple returns average by weight), and handle the missing values at the start and at gaps | A portfolio holds two stocks 50/50. Today one returns $+20\%$ and the other $-20\%$. Is the portfolio's return 0%, or the average of the two log returns, $-2.04\%$? | `time-series-lab` (shift), `value-table`, `numeric-input` | Trap: log returns average across assets the way they add over time (a portfolio's return is the weighted average of simple returns, 0% here; averaging $\ln 1.2$ and $\ln 0.8$ gives $-2.04\%$). Edge: 0.3 lesson 57's rules (log returns add over time; $\ln(1 + r) \approx r$ for small $r$) are assumed; the first return is always missing; under pandas 3, `pct_change` no longer pads gaps, so one missing price gives two missing returns [verified] | N, N, C, M |
| 94 | `lsn.dataframes.look-ahead` Look-ahead bias | Identify every operation in a backtest that uses information unavailable at decision time, and fix each with a correct shift | "Buy when today's return is positive, and earn today's return" backtests beautifully. Find the bug | `time-series-lab` (shift), `pipeline-flow` (pandas), `code-annotator` | Trap: signal and return on the same row. Edge: `shift(-1)` used to build a feature; backward fill; a centred rolling window; scaling with the whole sample's mean; a universe of today's survivors. On homework D4's series the same-day rule makes +9.28% and the honest one loses 3.94% [verified] | M, C, K, S |
| 95 | `lsn.dataframes.resample` Resampling to new frequencies | Convert daily data to weekly and monthly with `resample`, choosing the right aggregation for prices, returns and volumes, and predict the bin labels | Monthly returns from daily prices: the mean of daily returns, their sum, or the month's last price against the previous month's? | `time-series-lab` (resample) | Trap: monthly price is the mean of daily prices; monthly return is the sum of daily returns. Edge: `"W-FRI"` labels weeks by their Friday and `"ME"` labels months by their last day; McKinney's `"M"`, written for pandas 1.4, raises `ValueError` under pandas 3 [verified]; upsampling creates gaps; OHLC bars | C, T, E, K |
| 96 | `lsn.dataframes.rolling` Rolling and expanding windows | Compute rolling and expanding statistics with chosen windows and `min_periods`, compare simple and exponential weights, and predict the first non-missing row | A 20-day moving average: on which row does the first value appear, and what does `ewm(span=20)` weight differently? | `time-series-lab` (rolling) | Trap: `center=True` is harmless (it uses future data). Edge: a window of 20 rows against `"20D"`, which counts calendar days; the first full 20-row window ends on row 19 (counting from 0) [verified]; `span=20` means $\alpha = \frac{2}{21} \approx 0.0952$ | N, N, C, T |
| 97 | `lsn.dataframes.volatility` Volatility and annualisation | Compute daily volatility from returns, annualise it with $\sqrt{252}$, and derive why the square root appears | Daily returns have a standard deviation of 1.2%. Is the annual volatility $1.2\% \times 252 = 302\%$, or something else? | `drawdown-lab` (vol), `numeric-input`, `derivation-steps` | Trap: multiplying by 252; taking the standard deviation of prices. Edge: the learner derives $\text{Var}\left(\sum_{t=1}^{T} r_t\right) = T\sigma^2$ for independent returns, so volatility scales by $\sqrt{T}$: $1.2\% \times \sqrt{252} = 19.05\%$ [verified]. The rule fails when returns are autocorrelated or volatility clusters (2.2); annualising a mean uses 252, not $\sqrt{252}$ | N, N, C, O |
| 98 | `lsn.dataframes.drawdown` Drawdowns | Compute the drawdown series, the maximum drawdown and its peak, trough and recovery dates from prices or compounded returns | Two funds both returned 10% a year; one fell 50% on the way. Find each fund's worst peak-to-trough fall | `drawdown-lab` | Trap: building wealth with `cumsum` of simple returns (compound with `cumprod` of $1 + r$). Edge: a drawdown not yet recovered has no recovery date; drawdown is a fraction of the peak, so it can never exceed 100% | N, E, C, P |

Transfer screens: lesson 92 checks a calendar; lesson 93 computes a 50/50 portfolio's daily return; lesson 94 audits a backtest; lesson 97 annualises volatility; lesson 98 compares two funds' drawdowns. Lessons 93, 97 and 98 are the three exit quantities.

**Level D5: Plotting and communicating** (`lvl.dataframes.plotting`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 99 | `lsn.dataframes.figure-axes` Figures and Axes | Map each element of a matplotlib figure to the object that draws it, and build figures with the object-oriented interface | Tap the y-axis label of a chart and find the line of code that made it | `plot-workbench` (anatomy) | Trap: `plt.title` titles the panel you mean (it titles the current Axes, usually the last one made). Edge: `fig, ax = plt.subplots()`; `savefig` with `dpi` and `bbox_inches="tight"`; close figures made in a loop | S, C, K, M |
| 100 | `lsn.dataframes.line-charts` Price charts and scales | Plot price series against dates with labels and units, rebase several series to 100, and choose a log scale when comparing percentage moves | A share priced near 200 dollars and one near 5 dollars on one price axis from 2015 to 2024: the cheap one is a flat line along the bottom. Which did better? | `plot-workbench` (fix), `plot-2d` | Trap: comparing assets on raw prices of different sizes (rebase both to 100 at a common start, then compare). Edge: on a log scale equal vertical distances are equal percentage moves (0.2 lesson 47, 0.3 lesson 55), built with `ax.set_yscale("log")`; date ticks with `matplotlib.dates`; rebasing at another start date changes the picture, which lesson 103 exploits | C, K, C, M |
| 101 | `lsn.dataframes.histograms` Distributions of returns | Plot a histogram of returns with a justified bin count, overlay a normal density with matched mean and variance, and identify fat tails | A normal model predicts about 0.48 days beyond 4 standard deviations in 30 years of trading. How many does the seeded index series show? | `plot-workbench`, `stat-chart` | Trap: one bin count shows the truth (too few hides the tails; too many shows noise). Edge: overlay a density on `density=True`, not on counts; tails read best on a log y-axis. The 0.48 is $2 \times P(Z > 4) \times 30 \times 252$ [verified]; the lesson uses `price-series` data with jumps, not a claim about any real index | N, P, M, T |
| 102 | `lsn.dataframes.subplots` Multi-panel figures | Build a figure of stacked panels with shared x-axes showing price, returns and drawdown, with consistent labels | Three separate charts of price, returns and drawdown: line up the crash in all three | `plot-workbench` (build), `code-cell` (figure tests) | Trap: panels without `sharex` (the dates drift apart). Edge: `layout="constrained"`; height ratios that give the price panel more room | K, O, C, M |
| 103 | `lsn.dataframes.honest-charts` Honest charts | Diagnose dual axes, chosen start dates, truncated axes and survivorship in a chart, and fix each | A fund's brochure chart "beats the market". Find three ways it misleads | `plot-workbench` (fix) | Trap: two series that move together on a dual-axis chart are related (each axis is scaled separately, so any two rising series can be drawn on top of each other). Edge: a truncated bar axis (0.2 lesson 47) makes small gaps look large; a start date at a market low flatters every strategy; a league table of surviving funds overstates their average (0.3 lesson 123); a log scale is honest when labelled | M, P, S, C |

Transfer screens: lesson 100 rebases funds to 100; lesson 101 shows fat tails; lesson 102 builds the exit figure; lesson 103 critiques a fund brochure.

**Level D6: Workflow and the exit** (`lvl.dataframes.workflow`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 104 | `lsn.dataframes.method-chains` Readable pandas: method chains | Rewrite a sequence of in-place edits as a method chain with `assign`, `pipe` and `query`, and inspect each intermediate result | A 30-line cleaning script reassigns `df` twelve times; running one notebook cell twice corrupts the data. Rewrite it so rerunning is harmless | `pipeline-flow` (pandas), `code-cell` | Trap: `inplace=True` saves memory (it rarely does, and it breaks chaining). Edge: a long chain is hard to debug; a `pipe` step that logs the shape | O, K, C, T |
| 105 | `lsn.dataframes.performance` Speed and memory in pandas | Reduce a DataFrame's memory with suitable dtypes and categoricals, and replace a row loop with a vectorised or group-wise operation | A 10-million-row trade file takes 4 GB in memory. Get it under 1 GB without dropping a column | `dataframe-lab` (dtype), `bench-lab` | Trap: leaving a text column with few distinct values as text (pandas 3's `str` dtype stores every string; `category` stores the 3,000 tickers once plus integer codes, 12 to 20 times smaller on 200,000 rows) [verified on both runtimes]. Edge: `float32` keeps about 7 significant digits, so 12345.67 is stored as 12345.669921875 [verified]; six `float64` columns of 10 million rows take 480 MB and `float32` 240 MB | N, C, M, K |
| 106 | `lsn.dataframes.case-study` A cleaning case study | Take a raw multi-file price dataset with a split, missing days and bad rows through inspection, cleaning and validation, recording each decision | A stock "falls 75% in a day" in your data. A crash, or a 4-for-1 split? | `csv-inspector`, `dataframe-lab`, `time-series-lab` | Trap: computing returns on unadjusted prices across a split. Edge: dividends (adjusted close against close); validation checks: positive prices, unique dates, a sorted index, no gaps longer than the calendar allows | C, M, N, O |
| 107 | `lsn.dataframes.exit-project` The exit project: returns, volatility and drawdown | From a CSV of daily prices, compute returns, annualised volatility and maximum drawdown, plot them, and pass hidden tests in the app before running the same script locally | The 1.1 exit, done once in the app with the conventions spelled out, then alone on your machine | `workspace-sim`, `code-cell`, `drawdown-lab`, `setup-checklist` (project) | Trap: everything from the course at once: a gap, a mis-parsed date, $\sqrt{252}$, compounding, the first `NaN` return. Edge: the seeded file has thousands separators, a missing day and a duplicated row (section 4.3) | N, N, N, K |

Transfer screens: lesson 105 shrinks a trade file; lesson 106 detects a split; lesson 107 is the exit.

### 2.2 Item 1.2 Tools

#### Course T: Tools of the Trade (`crs.toolkit`, 7 levels, 32 lessons)

The four tools every quant job uses: the shell, Git and GitHub, testing with pytest, and SQL. Each is taught on a faithful simulator first (`shell-sim`, `git-graph`, the SQLite runner, `mutant-hunter`), then on the learner's own machine through `setup-checklist` paste-verify items in homework. The course ends with the 1.2 exit.

**Level T1: The shell** (`lvl.toolkit.shell`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | `lsn.toolkit.commands` Commands, words and quoting | Read a command line as the shell does: split it into words at unquoted spaces, then into a program, options and arguments; quote with single and double quotes; and find a command's options with `--help` and `man` | `cp my file.csv data/` fails with two errors. Why two? | `shell-sim`, `file-tree`, `token-tray` (words) | Trap: the shell sees `my file.csv` as one name (unquoted spaces split it into two arguments, `my` and `file.csv`, and `cp` reports both missing). Edge: `-rf` is `-r -f`; `--` ends the options, so a file called `-n` can be named; single quotes stop `$HOME` from expanding and double quotes do not; 0.4 lessons 13 to 16 (navigation, help, history) are assumed [verified in bash] | G, C, E, M |
| 2 | `lsn.toolkit.streams` Streams and redirection | Redirect standard output and standard error separately and together, to files or `/dev/null`, and predict what reaches the screen from the order in which the shell sets up redirections (0.4 lesson 17's `>` and `>>` are assumed) | A nightly job's log file is empty, yet the screen filled with errors. Where did they go? | `shell-sim`, `pipeline-flow` (shell) | Trap: `>` captures everything (it captures stream 1 only; errors are stream 2). Edge: `sort data.csv > data.csv` empties the file before `sort` reads it; `cmd > out 2>&1` and `cmd 2>&1 > out` differ | G, T, C, M |
| 3 | `lsn.toolkit.pipes` Pipes and text tools | Build a pipeline from `cut`, `grep`, `sort`, `uniq -c`, `wc`, `head` and `tail` that answers a question about a text file, inspecting each stage | Which ticker traded most often in a 2-million-line trade log? Answer in one line | `pipeline-flow` (shell), `shell-sim` | Trap: `uniq` counts every duplicate (only adjacent ones, so sort first). Edge: `sort` compares text, so numbers need `-n`; the header line pollutes counts (`tail -n +2`); `awk -F, 'NR>1 {s += $3} END {print s}'` sums a column [verified] | O, G, T, E |
| 4 | `lsn.toolkit.globs` Wildcards, quoting and finding files | Predict which files a glob matches, stop expansion with quotes, find files by name and age with `find`, and act on them with `-exec` or `xargs` | `ls *.csv` lists three files, `ls "*.csv"` fails, and `find . -name *.csv` finds one file in one folder and every CSV in another. Why? | `regex-lab` (glob), `shell-sim` | Trap: a pattern needs quotes only when it contains spaces (unquoted, `*.csv` is expanded by the shell in the current folder before `find` runs, so `find` receives file names, not the pattern; write `find . -name '*.csv'`). Edge: a glob matching nothing is passed on literally by bash; `*` skips hidden files; names with spaces need `-print0` with `xargs -0`; 0.4 lesson 17's "the shell expands `*`" is assumed [verified in bash] | E, M, G, C |

Transfer screens: lesson 3 finds the most-traded ticker in a trade log; lesson 4 finds every result file written by last night's run.

**Level T2: Working in the shell** (`lvl.toolkit.shell-work`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 5 | `lsn.toolkit.permissions` Permissions and executable scripts | Read permission strings from `ls -l`, set them with `chmod` in symbolic and octal form, and make a script executable with a shebang | `./run_backtest.sh` says "Permission denied" though you wrote the file. Fix it | `permission-bits`, `shell-sim` | Trap: `sudo` or `chmod 777` fixes it (fix the mode or the owner instead). Edge: a directory needs `x` to be entered; `640` is `rw-r-----`; `#!/usr/bin/env python3` finds the interpreter on `PATH` | E, N, G, C |
| 6 | `lsn.toolkit.env-path` Environment variables and PATH | Read and set environment variables for one command and for a session, explain which processes inherit them, and predict which program runs from the order of `PATH` | You type `API_KEY=abc123`. `echo $API_KEY` prints it, but `python fetch.py` reads `os.environ.get("API_KEY")` as `None`. Why? | `search-path` (PATH), `shell-sim` | Trap: a variable set without `export` reaches child processes (it stays in the shell; `export` passes it on). Edge: `VAR=x cmd` sets it for one command only; editing `PATH` in one terminal changes no other, and only a startup file (`~/.bashrc`, `~/.zshrc`) makes it last; `which -a` lists every candidate (0.4 lesson 19); keep keys in the environment or a git-ignored `.env`, never in code [verified in bash] | O, G, T, M |
| 7 | `lsn.toolkit.scripts` Shell scripts and exit codes | Write a script with variables, arguments, a `for` loop over files, tests on exit codes and `set -euo pipefail`, and predict where it stops on a failure | A script processes 30 daily files. File 12 is corrupt, the script carries on, and the morning report is built from 29 good files and one empty one. Make it stop | `shell-sim` (script), `code-cell` (shell) | Trap: unquoted `$file` (breaks on spaces); a script carries on after a failed command unless told otherwise. Edge: a pipeline's status is the last command's, hence `pipefail`; under `set -e`, `((count++))` stops the script when `count` is 0, so write `count=$((count + 1))` [verified in homework T2] | G, T, C, O |
| 8 | `lsn.toolkit.processes-remote` Processes, jobs and remote machines | List, background, foreground and stop processes, run commands and copy files on a remote machine with `ssh` and `scp` using keys, and edit a file in the terminal | A backtest launched over SSH dies when your laptop sleeps. How do you keep it running? | `shell-sim` (jobs and remote modes, decision 19), `text-terminal` (a recorded `nano` and Vim session) | Trap: closing the terminal leaves its jobs running (they receive a hang-up signal). Edge: `nohup` or `tmux`; `kill` before `kill -9`; a private key never leaves your machine; `nano`, and enough Vim to quit (`Esc`, `:wq`) | G, C, O, M |

Transfer screens: lesson 6 fixes a research machine's `PATH`; lesson 7 hardens a nightly data job; lesson 8 runs a backtest on a server.

**Level T3: Git foundations** (`lvl.toolkit.git-basics`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 9 | `lsn.toolkit.commits` A commit is a snapshot | Describe a commit as a snapshot of the whole project with a parent, an author, a message and an id, and build a history by committing | You have `model_v2_final.py` and `model_v3_really_final.py`. What would you need to replace them? | `git-graph` | Trap: a commit stores only the changes (it stores a snapshot; diffs are computed). Edge: the id is a hash of the contents, the parent and the metadata, so rewriting one commit changes every later id; `git init` creates `.git` | G, C, M, S |
| 10 | `lsn.toolkit.three-trees` Working tree, index and HEAD | Move changes between the working tree, the index and `HEAD` with `add`, `commit`, `restore` and `restore --staged`, and predict `status`, `diff` and `diff --staged` | You changed two files but want to commit one. How does Git know which? | `git-graph` (three trees), `diff-view` | Trap: `git diff` shows staged changes (it compares the working tree with the index). Edge: a file edited after `add` is both staged and modified (`MM`), and `git rm --cached` stages a deletion while keeping the file (`D ` and `??`) [verified]; `commit -a` skips new files | G, T, C, S |
| 11 | `lsn.toolkit.history` Reading history | Find when and why a line changed with `log`, `show`, `diff A..B`, `log -S` and `blame`, and write commit messages that make this easy | The annualisation constant changed from 252 to 365 last month and every risk number jumped. Find the commit and its author | `git-graph`, `diff-view` | Trap: messages like "fix" (they make history useless). Edge: `git log -S "365"` finds the commit that added or removed the text; `blame` shows the last change to a line, not its first author | G, E, C, M |
| 12 | `lsn.toolkit.branches` Branches and HEAD | Create and switch branches, explain a branch as a movable pointer to a commit, and predict what moves on each commit | Try a risky change to the signal without disturbing the working version. Make the graph match a target using only `branch`, `switch` and `commit` | `git-graph` | Trap: a branch is a copy of the files. Edge: a detached `HEAD`: commits made there are lost unless a branch points at them; switching with uncommitted changes | G, S, C, G |
| 13 | `lsn.toolkit.undo` Undoing safely | Choose among `restore`, `reset --soft`, `reset --mixed`, `reset --hard` and `revert` for a given mistake, and say which are safe after a push | You committed to the wrong branch; separately, a bug you committed is already on the shared branch. Which tool for each? | `git-graph` | Trap: `reset --hard` is a safe undo (it discards uncommitted work for good). Edge: `revert` adds a commit that undoes another, so it is the safe choice for shared history; resetting a pushed branch forces everyone else to repair theirs | S, G, C, T |

Transfer screens: lesson 11 traces a changed risk constant; lesson 13 reverts a bad commit on a shared research branch.

**Level T4: Git collaboration** (`lvl.toolkit.git-collab`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 14 | `lsn.toolkit.merging` Merging and conflicts | Predict whether a merge fast-forwards or makes a merge commit, resolve a textual conflict, and catch a semantic conflict with the tests | You and a colleague both edited the volatility function. Merge her branch into yours | `git-graph`, `merge-conflict` | Trap: keeping one side of a conflict without reading both; no textual conflict means correct code (a semantic conflict: she renamed a function you call). Edge: a fast-forward makes no new commit | G, K, C, M |
| 15 | `lsn.toolkit.remotes` Remotes, push and pull | Clone, fetch, pull and push, explain remote-tracking branches, and recover from a rejected push without force | `git push` is rejected: "fetch first". Your colleague pushed while you worked. What now? | `git-graph` (remote) | Trap: `git push --force` (it can delete a colleague's commits). Edge: `pull` is `fetch` plus a merge or rebase; `origin/main` is your local record of the remote, updated only by `fetch`; `--force-with-lease` | G, O, C, M |
| 16 | `lsn.toolkit.rebase` Rebasing and tidying history | Rebase a private branch onto an updated `main`, squash commits with an interactive rebase, and explain why rewritten commits get new ids | Your branch has seven commits called "wip". Turn them into one clean commit before review | `git-graph` (rebase) | Trap: rebasing commits others have already pulled. Edge: conflicts during a rebase are resolved one commit at a time; `rebase --abort` returns to the start | G, C, T, S |
| 17 | `lsn.toolkit.github-flow` Pull requests and code review | Take a change from branch to merged pull request with passing checks, and review a pull request for bugs, missing tests and leaked secrets | Review a 40-line pull request to the drawdown function. Find the off-by-one, the missing test and the API key | `code-review`, `git-graph` (remote, checks) | Trap: approving because the checks are green (the tests may not cover the change). Edge: forks against branches; small pull requests get better reviews; read the tests first | M, S, C, G |
| 18 | `lsn.toolkit.secrets-recovery` Ignoring files, secrets and recovery | Write `.gitignore` rules for data, environments and secrets, explain why a committed secret must be revoked, recover lost commits with `reflog`, and find a bad commit with `bisect` | You delete `api_key.txt` in a new commit. Is the key safe? | `regex-lab` (gitignore), `git-graph` (bisect) | Trap: deleting the file removes the key (it stays in history; revoke the key). Edge: `.gitignore` does not affect files already tracked (`git rm --cached`); `bisect` finds one bad commit among 1,000 in $\lceil \log_2 1000 \rceil = 10$ tests, the bisection of 0.2 lesson 108; `stash` | M, C, N, G |

Transfer screens: lesson 14 merges two edits to a risk function; lesson 17 reviews a change to the drawdown code; lesson 18 bisects a change that broke a backtest.

**Level T5: Testing with pytest** (`lvl.toolkit.testing`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 19 | `lsn.toolkit.first-tests` Tests as executable specifications | Write test functions with plain `assert` that pytest discovers and runs, and read pytest's report to find the wrong value | `annualised_vol` has a bug that reached a client report. Write two asserts that would have caught it | `mutant-hunter` (intro), `code-cell` (pytest), `diagnostic-reader` (pytest) | Trap: computing the expected value by calling the function under test. Edge: discovery needs `test_*.py` files and `test_` functions; a test with no assert always passes; pytest shows both sides of a failed `==` | K, S, C, M |
| 20 | `lsn.toolkit.test-cases` Choosing test cases | Partition a function's inputs into classes with boundaries, choose a minimal set of cases that kills every mutant, and write them as one `parametrize` table with readable ids | Kill every mutant of `max_drawdown` with as few tests as you can | `mutant-hunter`, `code-cell` (pytest) | Trap: testing only typical values. Edge: empty input, one price, all equal, rising only, a new peak after a drawdown; stacked `parametrize` decorators give the cross product | K, M, C, N |
| 21 | `lsn.toolkit.approx-raises` Floats and errors in tests | Test float results with `pytest.approx` and a justified tolerance, and test that bad input raises the right exception with `pytest.raises(..., match=...)` | `assert vol(r) == 0.1905` fails for a correct function. Make it pass for correct code and still fail for wrong code | `mutant-hunter`, `float-inspector` | Trap: a tolerance so loose it passes a bug (`rel=0.1`). Edge: `approx` defaults to a relative tolerance of $10^{-6}$ and an absolute one of $10^{-12}$, so near 0 only the absolute one acts and must be set to the size the result can honestly reach [verified with pytest 9.1]; a `raises` block can pass because a different line raised the same type, so keep it to one line and use `match` | K, C, N, M |
| 22 | `lsn.toolkit.fixtures` Fixtures and test data | Share setup through fixtures with the right scope, clean up with `yield`, and use `tmp_path` and `monkeypatch` for code that writes files or reads the environment | Ten tests build the same price DataFrame. One test changes it, and another fails only when run after it. Why? | `node-link` and `stepper` (setup order, build-time `--setup-show` data), `code-cell` | Trap: a module-scoped mutable fixture (state leaks between tests). Edge: tests must pass in any order; `conftest.py` shares fixtures; `tmp_path` gives each test its own folder | O, T, K, M |
| 23 | `lsn.toolkit.tdd-data` Test-driven development and testing data code | Write a failing test first, make it pass with the simplest code, refactor, and test data functions on small hand-made frames | Build `rolling_sharpe` test first from three numbers worked by hand | `code-cell` (tests first), `mutant-hunter` | Trap: writing tests after the code to match whatever it outputs. Edge: `pd.testing.assert_frame_equal` checks dtypes and the index too; random data in tests must be seeded or avoided | O, K, C, M |
| 24 | `lsn.toolkit.properties-ci` Property-based tests and continuous integration | State a property that must hold for every input and test it with Hypothesis, and read and fix a failing CI check on a pull request | A drawdown function measures every fall from the series' overall maximum. Five hand-picked inputs pass. Hypothesis breaks it in two seconds and shrinks the failure to `[1.0, 2.0]`. What is wrong with that input, or with the function? | `mutant-hunter` (property mode, decision 19), `git-graph` (checks), `diagnostic-reader` | Trap: a property that restates the implementation. Edge: shrinking finds a minimal case (`[1.0, 2.0]` only rises, so its drawdown is 0, yet the planted bug reports 0.5); drawdown properties: $0 \le \text{MDD} < 1$ for positive prices, scaling every price leaves it unchanged, appending a new high leaves it unchanged, and a non-increasing series has $\text{MDD} = 1 - \frac{\min}{\max}$; CI runs the tests on every push in a clean environment; the live screen needs Hypothesis (decision 23) [verified with Hypothesis 6.168] | M, K, C, G |

Transfer screens: lesson 19 catches a volatility bug; lesson 20 tests the drawdown function; lesson 23 builds a rolling Sharpe ratio test first. After this level the learner can meet the 1.2 exit (section 4.3).

**Level T6: SQL queries** (`lvl.toolkit.sql-query`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 25 | `lsn.toolkit.select-where` SELECT, WHERE and ORDER BY | Write queries that select columns, filter rows with comparisons, `AND`, `OR`, `IN`, `BETWEEN` and `LIKE`, and sort and limit the result | List the ten largest AAPL trades in March from a trades table | `code-cell` (SQL), `predict-output` (table) | Trap: `sym = 'A' OR sym = 'B' AND qty > 100` reads left to right (`AND` binds first). Edge: `BETWEEN` includes both ends, which matters for timestamps; ISO dates compare correctly as text; `LIMIT` without `ORDER BY` returns arbitrary rows | Q, K, C, T |
| 26 | `lsn.toolkit.null` NULL and three-valued logic | Predict the result of comparisons, filters and aggregates involving `NULL`, and use `IS NULL`, `COALESCE` and `COUNT(*)` against `COUNT(col)` correctly | `WHERE px <> 189.4` returns 5 of 8 trades and `WHERE px = 189.4` returns 2. Where is the eighth? | `value-table` (truth table), `predict-output` | Trap: `= NULL` finds missing values (it is never true). Edge: `NOT IN` against a list containing `NULL` returns nothing [verified]; `AVG` skips `NULL`s; `NULL`s form one group in `GROUP BY` | N, Q, T, C |
| 27 | `lsn.toolkit.group-by` Aggregates, GROUP BY and HAVING | Compute grouped aggregates, filter groups with `HAVING` and rows with `WHERE`, and order a query's clauses by when they run | Which traders averaged more than 1,000 shares a trade in March? Try putting the condition in `WHERE` | `groupby-lab` (SQL), `pipeline-flow` (SQL) | Trap: `WHERE` can use aggregates and `SELECT` aliases (it runs before grouping: the logical order is `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `ORDER BY`). Edge: SQLite accepts a bare column outside `GROUP BY` and returns a value from some row of the group, where most databases refuse; `COUNT(DISTINCT ...)` | O, K, C, Q |
| 28 | `lsn.toolkit.joins` Joins | Combine tables with inner and left joins, predict the row count with duplicate keys and unmatched rows, and find rows with no match with `NOT EXISTS` | Join trades to a securities table: some trades vanish with an inner join. Which, and why? | `join-lab` (SQL) | Trap: a condition on the right table in `WHERE` keeps a left join's unmatched rows (it removes them; move it into `ON`: 6 rows against 8 in homework T6's data) [verified]. Edge: many-to-many keys multiply rows; a self-join pairs consecutive days | N, Q, C, K |

Transfer screens: lesson 25 queries a trades table; lesson 27 summarises traders; lesson 28 finds securities never traded.

**Level T7: SQL for analysis and change** (`lvl.toolkit.sql-analysis`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 29 | `lsn.toolkit.subqueries-cte` Subqueries and WITH | Break a multi-step question into named steps with `WITH`, and use scalar, `IN` and `EXISTS` subqueries | Which stocks closed above their own 2024 average on the year's last trading day? | `pipeline-flow` (SQL), `code-cell` (SQL) | Trap: a scalar subquery that returns several rows. Edge: each named step of a `WITH` can be run and checked alone; `NOT IN` against `NOT EXISTS` when `NULL`s are present | Q, K, O, C |
| 30 | `lsn.toolkit.window-functions` Window functions | Compute per-row results over partitions with `ROW_NUMBER`, `RANK`, `LAG` and a windowed `AVG`, including daily returns per ticker | Compute each stock's daily return in SQL without MSFT's first day using AAPL's last close | `groupby-lab` (window) | Trap: leaving out `PARTITION BY` (returns leak across tickers: MSFT's first return comes out as −49.98% [verified]). Edge: `LAG` needs `ORDER BY` inside `OVER`; `RANK`, `DENSE_RANK` and `ROW_NUMBER` differ on ties; the default frame of a running `SUM` | Q, K, C, N |
| 31 | `lsn.toolkit.changing-data` Creating and changing tables safely | Create tables with types, keys and constraints, insert, update and delete rows inside transactions, and roll back a mistake | `UPDATE trades SET px = 0` ran without a `WHERE`. Undo it | `code-cell` (SQL), `predict-output` (table) | Trap: `UPDATE` and `DELETE` without `WHERE`; assuming every statement can be undone (only inside an open transaction). Edge: `PRIMARY KEY` and `UNIQUE` reject duplicates; SQLite enforces foreign keys only after `PRAGMA foreign_keys = ON`; without `STRICT`, a text value can land in an integer column | Q, C, K, M |
| 32 | `lsn.toolkit.sql-python` SQL from Python and injection | Query SQLite from Python with parameters, load results into pandas, decide whether to aggregate in SQL or in pandas, and show why string-built queries are injectable | A search box runs `f"SELECT * FROM trades WHERE trader = '{name}'"`. Type a name that returns every trader's trades | `injection-lab`, `code-cell` | Trap: f-strings or `%` to build SQL. Edge: the input `x' OR '1'='1` returns all 8 rows while the parameterised query returns none [verified]; parameters cannot stand for table names; aggregating in the database moves less data; Python's `sqlite3` opens a transaction before an `INSERT` or `UPDATE`, so a script that never calls `commit()` loses its writes when the connection closes [verified on SQLite 3.39 and 3.45] | E, K, C, M |

Transfer screens: lesson 29 compares closes with yearly averages; lesson 30 computes returns per ticker; lesson 32 hardens a trade-search tool.

### 2.3 Coverage check

**1.1: the curriculum's chosen resources and exit.** Item 1.1 has no cover list; its "Use" line (CS50P, then McKinney for NumPy, pandas and matplotlib) and its exit define the scope.

| Source unit | Lessons |
|---|---|
| CS50P lecture 0, Functions and Variables | 1, 2, 6, 16, 17 |
| CS50P lecture 1, Conditionals | 11 |
| CS50P lecture 2, Loops | 12 to 15, 25 |
| CS50P lecture 3, Exceptions | 34 to 36 |
| CS50P lecture 4, Libraries | 45, 46, 69, 41 (JSON from an API, read from a file here) |
| CS50P lecture 5, Unit Tests | Every drill's test reports; 36 (`assert`); 1.2 level T5 |
| CS50P lecture 6, File I/O | 39, 40, 38 |
| CS50P lecture 7, Regular Expressions | 43 |
| CS50P lecture 8, Object-Oriented Programming | 49 to 53 |
| CS50P lecture 9, Et Cetera (sets, globals, constants, type hints, docstrings, argparse, unpacking, `*args`, `map`, comprehensions, `filter`, dict comprehensions, `enumerate`, generators) | 26, 18, 48, 54, 44, 24, 17, 27, 29, 30, 14 |
| McKinney ch. 2 and 3 (language basics, built-in data structures, functions, files) | Course Y; 39, 47 |
| McKinney ch. 4 and appendix A (NumPy) | 56 to 67; 69 and 72 (sections 4.2 and 4.7) |
| McKinney ch. 5 (pandas data structures) | 76 to 81 |
| McKinney ch. 6 (loading and storage) | 82, 41 |
| McKinney ch. 7 (cleaning) | 83, 84, 91 |
| McKinney ch. 8 (join, combine, reshape) | 87 to 90 |
| McKinney ch. 9 (plotting) | 99 to 103 |
| McKinney ch. 10 (aggregation and group operations) | 86, 91 |
| McKinney ch. 11 (time series) | 92 to 98 |
| McKinney ch. 12 (modelling libraries: statsmodels, scikit-learn) and ch. 13 (data analysis examples) | Ch. 12 is left to 1.6 (statsmodels, matched in the 1.6 exit, section 1.1) and 2.1 (scikit-learn, section 1.0); one ch. 13 example is level D6's companion problem |
| The 1.1 exit: returns, annualised volatility, maximum drawdown, plots | 93, 97, 98, 102, 107 (with 15, 64 and 82 on the way) |
| Added for a top programme | the object model and aliasing (1, 22 to 24), exact arithmetic and rounding (3 to 5), Unicode (10), closures and decorators (20, 33), recursion and costs as previews (21, 28), iterators and `itertools` (29 to 32), debugging and context managers (37, 38), dates and time zones (42), environments and reproducibility (46, 47), readable code and type hints (48, 54), program design (55), floating point in arrays and log-sum-exp (66), matrix arithmetic (67), measured performance (68), simulation with error bars (69 to 75), point-in-time joins (88), look-ahead bias (94), honest charts (103), memory (105), a split in real data (106) |

**1.2: the curriculum's cover list.**

| Cover term | Lessons |
|---|---|
| Git and GitHub | 9 to 18, 24 (CI) |
| The Linux command line | 1 to 8 |
| SQL basics | 25 to 32 |
| Testing with pytest | 19 to 24 |
| Added for a top programme | permissions and `PATH` (5, 6), safe scripts (7), remote work (8), recovery and `bisect` (13, 18), code review (17), secrets hygiene (18), property-based testing and CI (24), window functions (30), transactions and constraints (31), SQL injection (32) |

**The Missing Semester lectures.** The 2026 edition's titles and order are [searched]; how far each lecture's content matches the lessons is [check] until someone watches them.

| Edition and lecture | Lessons |
|---|---|
| 2026, 1 Course Overview + Introduction to the Shell | 0.4 level B2; 1.2 lessons 1 to 4 |
| 2026, 2 Command-line Environment | 1.2 lessons 5, 6 and 8 |
| 2026, 3 Development Environment and Tools | 1.1 lessons 46 and 48 (editor, linter, formatter) [check content] |
| 2026, 4 Debugging and Profiling | 1.1 lessons 37 and 68 |
| 2026, 5 Version Control and Git | 1.2 lessons 9 to 18 |
| 2026, 6 Packaging and Shipping Code | 1.1 lesson 46; 1.2 lesson 24 (CI) [check content] |
| 2026, 7 Agentic Coding | Not covered; stretch |
| 2026, 8 Beyond the Code | Not covered; stretch [check content] |
| 2026, 9 Code Quality | 1.1 lesson 48; 1.2 level T5 [check content] |
| 2020, 2 Shell Tools and Scripting (dropped in 2026) | 1.2 lessons 3, 4 and 7 |
| 2020, 3 Editors (Vim) | 1.2 lesson 8 (survival only) |
| 2020, 4 Data Wrangling | 1.2 lesson 3 (`sed` and `awk` in its ladder); 1.1 lesson 43 |
| 2020, 8 Metaprogramming | 1.2 lesson 24 (CI); build systems not covered |
| 2020, 9 Security and Cryptography | 1.2 lessons 9 (hashes) and 18 (secrets) |

**SQLBolt lessons.** Lessons 1 to 5 (SELECT, constraints, filtering and sorting, review): 25. Lessons 6 and 7 (inner and outer joins): 28. Lesson 8 (NULLs): 26. Lesson 9 (expressions): 25, 27. Lessons 10 to 12 (aggregates, order of execution): 27. Lessons 13 to 18 (insert, update, delete, create, alter, drop): 31. SQLBolt's subquery and set-operation topics: 29. Window functions (30) and injection (32) are beyond SQLBolt. Lesson titles are as recalled [check]; sqlbolt.com was blocked from this environment.

**Choice items in quizzes.** Single and multiple choice (C and M) as a share of each course's quiz items, counted from the tables above, against design research 10's ceiling of 40%:

| Course | Lessons | Quiz items | C | M | Share | Most common other types |
|---|---|---|---|---|---|---|
| Y Thinking in Python | 28 | 112 | 26 | 9 | 31.3% | T 41, N 15, K 9 |
| B Building Real Programs | 27 | 108 | 29 | 11 | 37.0% | T 22, K 15, O 9 |
| A Arrays and Simulation | 20 | 80 | 21 | 7 | 35.0% | N 20, T 13, E 11 |
| D Data, Time Series and Charts | 32 | 128 | 29 | 19 | 37.5% | N 24, K 17, T 14 |
| T Tools of the Trade | 32 | 128 | 29 | 19 | 37.5% | G 20, K 14, T 10 |

Every course is under the ceiling. Predict-output (T) carries course Y because prediction is how that course teaches; reach-a-state (G) carries course T because the tools are learned by doing.

---

## 3. Homework blueprint per level

### 3.0 Rules for every set

- **Shape.** Issued when a level's last lesson is done, due in 7 days, marked on submission (ASSESSMENT.md 2.5). 1.1 sets hold 7 to 9 items, usually 8: three or four code drills, three auto-marked items (predict-output, numeric, result table or entry) and one long-form item; about 2 hours. 1.2 sets hold 7 items: two or three simulator or code tasks, one SQL or pytest item where the level teaches it, one long-form item and one local task on the learner's own machine; about 1.5 hours.
- **Difficulty.** Every item at difficulty 3 to 5. Eight-item sets: d3 ×3, d4 ×3, d5 ×2. Seven-item sets: d3 ×3, d4 ×2, d5 ×2 in 1.2, and d3 ×2, d4 ×3, d5 ×2 in 1.1. The nine-item set: d3 ×3, d4 ×4, d5 ×2.
- **Long-form.** At least one per set, a `long-form` check with a 10-point rubric of five points of 2 marks (CONTENT-FORMAT.md 3.4): `genre: written` for a diagnosis, a design rationale or a code review, `genre: derivation` for $\sqrt{T}$, $\sigma/\sqrt{n}$ or log-sum-exp, `genre: proof` for a loop invariant. The learner self-marks with Bertie's per-point suggestion and a verbatim quote as evidence (AI-TUTOR.md 2.7).
- **Code drills.** Each drill ships `drill.yaml` (with `needs`), `reference.py`, `starter.py`, `tests.py` (`zqtest`) and a `wrong/` folder of known-wrong solutions, each naming the misconception it encodes and the test it must fail (CONTENT-FORMAT.md 3.9). Visible examples run as often as the learner likes; hidden tests run once, at submission. A drill runs wherever the build ships its `needs`; elsewhere it shows "Run this one in the web app" and accepts a result code, and the set can be submitted with it pending (ASSESSMENT.md 2.5). Course Y and B drills need only the standard library, course A drills NumPy, course D drills NumPy and pandas, so every 1.1 set runs in the Artifact today except D5's figure drills (matplotlib) and B3's time-zone items (`tzdata`), until those join a load group (section 8). Below 768 px every drill offers its Parsons version.
- **Local tasks.** From level B3 one item per 1.1 set, and in every 1.2 set, is done on the learner's own machine and verified by pasting output into `setup-checklist` (paste-verify, home paths redacted). These items rehearse the two exits.
- **Bertie.** No tutor surface on any item until the set is submitted (AI-TUTOR.md 2.2, 2.12); the paste guard blocks chat that reproduces an open item (AI-TUTOR.md 8.3). After submission he explains, drafts long-form marks with the learner, and reviews passing code in the owner's code-craft format at the depth the learner picks (AI-TUTOR.md 2.8).
- **Variants.** Generated items are seeded per learner and level, so a returning learner sees the same set; the generator families are listed per set. Predict-output generators draw from CI-recorded seed banks, so neither target needs Python to grade them (widgets-programming 2.4, `seed-bank`).

### 3.1 Item 1.1 Python

| Level | Set | Items | Difficulty mix | Long-form item (rubric: five points of 2 marks) | Code drills | Generators |
|---|---|---|---|---|---|---|
| Y1 | `set.pythink.objects` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why `round(2.675, 2)` is 2.67, from the stored value, and how a payments system should store and round money | `drl.py.allocate-pence`, `drl.py.close-enough` (re-implement `math.isclose`, including `inf` and `nan`), `drl.py.parse-money` (`"£1,234.56"` to integer pence and back) | `gen.py.alias-trace`, `gen.py.predict-numeric`, `gen.py.float-repr` |
| Y2 | `set.pythink.text` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why `len("café")` can be 4 or 5, why the two forms compare unequal, and how to make a name lookup immune | `drl.py.parse-occ`, `drl.py.normalise-ticker`, `drl.py.format-pnl-table` | `gen.py.slice-predict`, `gen.py.format-spec`, `gen.py.split-predict` |
| Y3 | `set.pythink.control` | 8 | d3 ×3, d4 ×3, d5 ×2 | A loop invariant for the drawdown loop: what holds after each pass, and why the loop therefore returns the maximum drawdown | `drl.py.max-drawdown-loop`, `drl.py.first-breach`, `drl.py.longest-streak` | `gen.py.loop-count`, `gen.py.range-predict`, `gen.py.truthiness` |
| Y4 | `set.pythink.functions` | 8 | d3 ×3, d4 ×3, d5 ×2 | The mutable default, from the moment `def` runs, the `None` sentinel fix, and the rare case where a shared default is intended (a cache) | `drl.py.make-ewma`, `drl.py.sort-blotter`, `drl.py.count-paths` | `gen.py.arg-binding`, `gen.py.scope-predict`, `gen.py.closure-predict` |
| Y5 | `set.pythink.collections` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why de-duplicating with a list is quadratic and with a set linear, with counts at $n = 100{,}000$, and what set membership requires and costs | `drl.py.group-trades`, `drl.py.dedupe-ordered` (complexity test), `drl.py.restricted-check` | `gen.py.copy-predict`, `gen.py.dict-predict`, `gen.py.complexity-classify` |
| B1 | `set.pybuild.iteration` | 8 | d3 ×3, d4 ×3, d5 ×2 | Lazy against eager: memory and time for summing squares over 50 million lines, and two ways laziness bites (exhaustion, deferred errors) | `drl.py.rolling-mean-gen`, `drl.py.chunked`, `drl.py.count-calls` (decorator) | `gen.py.iter-predict`, `gen.py.itertools-count` |
| B2 | `set.pybuild.errors` | 8 | d3 ×3, d4 ×3, d5 ×2 | Review of a function wrapped in a bare `except`: three harms, the rewrite, and when catching broadly is right | `drl.py.safe-parse`, `drl.py.validate-order` (custom exception), `drl.py.timer-context` | `gen.py.exception-flow`, `gen.py.traceback-locate` |
| B3 | `set.pybuild.files` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why the New York close moves between 20:00 and 21:00 London time, and why code must convert by date (inside example 2) | `drl.py.parse-trade-line`, `drl.py.csv-totals`, `drl.py.order-book-json`; local task: run `vol.py prices.csv --window 20` from your terminal and paste the output | `gen.py.regex-sets`, `gen.py.tz-convert`, `gen.py.json-path` |
| B4 | `set.pybuild.modules` | 8 | d3 ×3, d4 ×3, d5 ×2 | Reproducing a colleague's Sharpe ratio exactly: what to pin, seed and record, and a layout that guarantees it | `drl.py.refactor-vol` (readable rewrite, judged by tests and a lint check), `drl.py.package-layout` (`workspace-sim`); local task: create a virtual environment, install a pinned NumPy and paste `python -m pip freeze` | `gen.py.import-resolve`, `gen.py.path-order` |
| B5 | `set.pybuild.objects` | 8 | d3 ×3, d4 ×3, d5 ×2 | Composition against inheritance for `Stock`, `Option` and `Portfolio`, with a `Protocol`, and why a portfolio should not subclass `list` | `drl.py.money`, `drl.py.portfolio-invariant`, `drl.py.fifo-match` | `gen.py.class-attr-predict`, `gen.py.dataclass-predict` |
| A1 | `set.arrays.ndarray` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why NumPy slices are views and list slices copies: the memory argument and one bug each choice invites | `drl.py.winsorise`, `drl.py.returns-np`, `drl.py.select-block` | `gen.py.shape-predict`, `gen.py.view-or-copy`, `gen.py.dtype-predict` |
| A2 | `set.arrays.compute` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why `solve` beats `inv`: work, rounding error and the singular case (with the log-sum-exp derivation inside example 2) | `drl.py.logsumexp`, `drl.py.drawdown-np` (complexity test), `drl.py.portfolio-vol` | `gen.py.broadcast-shape`, `gen.py.reduction-predict`, `gen.py.quantile-predict` |
| A3 | `set.arrays.simulation` | 8 | d3 ×3, d4 ×3, d5 ×2 | Derive why Monte Carlo error falls like $1/\sqrt{n}$ and size a simulation for a target error | `drl.py.ruin-sim`, `drl.py.mc-call`, `drl.py.birthday-sim` | `gen.py.se-trials`, `gen.py.ruin-exact` |
| D1 | `set.dataframes.basics` | 8 | d3 ×3, d4 ×3, d5 ×2 | Label alignment against positional arithmetic, with a P&L case where `.to_numpy()` is silently wrong | `drl.py.align-pnl`, `drl.py.notional-columns`, `drl.py.cap-positions` (single-step `loc`) | `gen.py.align-predict`, `gen.py.loc-iloc-count` |
| D2 | `set.dataframes.cleaning` | 8 | d3 ×3, d4 ×3, d5 ×2 | Forward fill, backward fill, interpolate, leave or drop: choose for three kinds of gap and name any look-ahead | `drl.py.load-closes`, `drl.py.clean-tickers`, `drl.py.rank-funds` | `gen.py.read-csv-options`, `gen.py.missing-predict`, `gen.py.rank-ties` |
| D3 | `set.dataframes.combine` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why `merge_asof` with `direction="backward"` is the only point-in-time join among the three directions, with a timeline | `drl.py.sector-features`, `drl.py.quotes-asof`, `drl.py.wide-prices` | `gen.py.merge-count`, `gen.py.groupby-shape`, `gen.py.pivot-predict` |
| D4 | `set.dataframes.timeseries` | 9 | d3 ×3, d4 ×4, d5 ×2 | Derive the $\sqrt{252}$ rule, state its assumptions, and describe two ways real returns break it | `drl.py.strategy-returns`, `drl.py.monthly-returns`, `drl.py.rolling-vol`, `drl.py.drawdown-dates` | `gen.py.returns-numeric`, `gen.py.resample-label`, `gen.py.annualise` |
| D5 | `set.dataframes.plotting` | 7 | d3 ×2, d4 ×3, d5 ×2 | Critique a misleading fund chart and specify the honest version | `drl.py.exit-figure` (figure assertions), `drl.py.rebased-chart`, `drl.py.return-histogram` | `gen.py.figure-anatomy` |
| D6 | `set.dataframes.workflow` | 8 | d3 ×3, d4 ×3, d5 ×2 | A cleaning log for the case-study dataset: each decision, its reason, and how it was validated | `drl.py.summarise-series`, `drl.py.shrink-frame`, `drl.py.detect-split`; local task: run your exit script on your machine and paste its printed summary | `gen.py.memory-numeric`, `gen.py.chain-order` |

**Example problems, 1.1.** Every predicted output and reference solution below was run on CPython 3.11.15 (NumPy 2.4.6, pandas 3.0.6) and on Pyodide 314.0.7 (Python 3.14.2, NumPy 2.4.6, pandas 3.0.2), and agreed [verified]; B3 example 2 (`zoneinfo`) and D5 example 1 (matplotlib) ran on CPython only. "Checks" lists the cases the visible and hidden tests include.

**Y1, example 1 (difficulty 4, predict).** Predict the three lines.

```python
print(-7 // 2, -7 % 2, 7 // -2, divmod(-7, 2))
print(int(-3.7), round(-2.5), round(0.125, 2))
print(0.1 * 3 == 0.3, abs(0.1 * 3 - 0.3) < 1e-9)
```

*Answer:* `-4 1 -4 (-4, 1)`, then `-3 -2 0.12`, then `False True`.
*Working:* `//` rounds down (towards $-\infty$) and `%` is defined so that `(a // b) * b + a % b == a`: $(-4)(2) + 1 = -7$. `7 // -2` is $\lfloor -3.5 \rfloor = -4$. `int` truncates towards zero. `round` sends an exact half to the even neighbour: $-2.5 \to -2$; 0.125 is $\frac{1}{8}$, stored exactly, so it is a true tie and goes to 0.12. $0.1 \times 3$ is stored as 0.30000000000000004, so `==` fails and the tolerance test passes.

**Y1, example 2 (difficulty 5, code).** Write `allocate(total, weights)` that splits `total` pence in proportion to non-negative integer `weights`, returning whole pence that sum exactly to `total`, each within 1p of its exact share, by the largest-remainder method with ties going to the earlier position. Raise `ValueError` for a negative total, a negative weight, or weights summing to 0.

*Answer:*

```python
def allocate(total: int, weights: list[int]) -> list[int]:
    if total < 0 or any(w < 0 for w in weights) or sum(weights) == 0:
        raise ValueError("need total >= 0 and non-negative weights with a positive sum")
    W = sum(weights)
    shares = [total * w // W for w in weights]      # exact integer floors
    short = total - sum(shares)                      # pence still to hand out, fewer than len(weights)
    order = sorted(range(len(weights)), key=lambda i: (-(total * weights[i] % W), i))
    for i in order[:short]:                          # largest remainders first, ties to the earlier index
        shares[i] += 1
    return shares
```

*Checks:* `allocate(100, [1, 1, 1]) == [34, 33, 33]`; `allocate(10, [1, 2, 3]) == [2, 3, 5]`; `allocate(7, [0, 1, 1]) == [0, 4, 3]`; hidden: 1,000 random cases sum to `total` with every share within 1 of `total * w / W`, zero weights get 0, and the three errors.
*Decision point:* computing `total * w / W` in floats and rounding each share gives 33 + 33 + 33 = 99 for the first case. Integer floors plus remainders cannot lose a penny.

**Y2, example 1 (difficulty 4, code).** Write `parse_occ(symbol)` for OCC option symbols: a root of up to 6 characters (padded to 6 with spaces in the 21-character form, or unpadded), then `YYMMDD`, then `C` or `P`, then the strike times 1,000 in 8 digits. Return `(root, expiry, kind, strike)` with a `date` and a `Decimal`; raise `ValueError` for anything else.

*Answer:*

```python
from datetime import date
from decimal import Decimal

def parse_occ(symbol: str) -> tuple[str, date, str, Decimal]:
    s = symbol.rstrip()
    if len(s) < 16:
        raise ValueError(f"too short for an OCC symbol: {symbol!r}")
    root, ymd, kind, strike = s[:-15].strip(), s[-15:-9], s[-9], s[-8:]   # fixed widths from the right
    if not root or kind not in ("C", "P") or not (ymd.isdigit() and strike.isdigit()):
        raise ValueError(f"not an OCC symbol: {symbol!r}")
    expiry = date(2000 + int(ymd[:2]), int(ymd[2:4]), int(ymd[4:]))
    return root, expiry, kind, Decimal(strike) / 1000
```

*Checks:* `"AAPL  250117C00150000"` gives `("AAPL", date(2025, 1, 17), "C", Decimal("150"))`; `"SPXW  241220P05900000"` gives a strike of 5900; `"F     250321C00012500"` gives root `F` and strike 12.5; a 13-month date raises from `date`, which the hidden test expects as `ValueError`.
*Decision point:* slicing from the start (`s[4:10]`) works only for an unpadded symbol with a 4-character root (`AAPL250117C00150000`, `SPXW241220P05900000`) and fails for every padded symbol and for roots such as F; the fields have fixed widths only from the right.

**Y2, example 2 (difficulty 5, long-form).** Explain why `len("café")` can be 4 or 5, why two such strings can print identically yet compare unequal, and how you would make a lookup of company names immune to this.

*Model answer:* (1) A `str` is a sequence of Unicode code points, not of visible characters. (2) "é" can be one code point, U+00E9, or two: "e" followed by the combining acute accent U+0301, which makes the word 5 code points long. (3) `==` compares code points, so the two forms are unequal although they are drawn identically. (4) Normalisation maps equivalent sequences to one form: after `unicodedata.normalize("NFC", s)` both are 4 code points and equal. (5) Normalise (and, if case should not matter, `casefold`) every key at the boundary where text enters the program: file reads, user input and API responses, after decoding bytes with the right codec.
*Rubric (10):* 2 for code points against visible characters; 2 for the two encodings of "é"; 2 for why `==` fails; 2 for NFC normalisation; 2 for normalising at the input boundary.

**Y3, example 1 (difficulty 4, predict).** What does this print?

```python
n, i = 0, 10
while i > 1:
    i = i // 2 if i % 2 == 0 else 3 * i + 1
    n += 1
print(n, i)
```

*Answer:* `6 1`. *Working:* $i$ runs 10, 5, 16, 8, 4, 2, 1: six updates before `i > 1` fails.

**Y3, example 2 (difficulty 5, code).** Write `max_drawdown(prices)` in one pass, returning `(mdd, peak, trough)`: the largest fall from a running peak as a fraction of that peak, and the indices of the first such peak and trough. Return `(0.0, 0, 0)` when prices never fall; raise `ValueError` for an empty list or a non-positive price.

*Answer:*

```python
def max_drawdown(prices: list[float]) -> tuple[float, int, int]:
    if not prices:
        raise ValueError("empty price list")
    if any(p <= 0 for p in prices):
        raise ValueError("prices must be positive")
    peak_i, best = 0, (0.0, 0, 0)
    for i, p in enumerate(prices):
        if p > prices[peak_i]:
            peak_i = i                               # a new running peak
        dd = (prices[peak_i] - p) / prices[peak_i]
        if dd > best[0]:                             # strict, so the first maximal drawdown is kept
            best = (dd, peak_i, i)
    return best
```

*Checks:* `[100, 120, 90, 110, 80, 130]` gives `(1/3, 1, 4)`; `[1, 2, 3]` gives `(0.0, 0, 0)`; `[100, 50, 100, 50]` gives `(0.5, 0, 1)`; hidden tests compare with `isclose(rel_tol=1e-12)` and include a complexity test whose line budget fails a nested loop.
*Decision point:* `max(prices) - min(prices)` says 50 on the first series, but the 130 comes after the 80; the true fall is 40 from 120.

**Y4, example 1 (difficulty 4, predict).**

```python
def f(x, acc=[]):
    acc.append(x)
    return acc
a = f(1)
b = f(2)
c = f(3, [])
print(a, b, c, a is b)
```

*Answer:* `[1, 2] [1, 2] [3] True`. *Working:* the default list is built once, when `def` runs. Calls 1 and 2 append to that one list and return it, so `a` and `b` are the same object; call 3 brings its own list.

**Y4, example 2 (difficulty 5, code).** Write `make_ewma(alpha)` returning a function `update(x)` that returns the exponentially weighted moving average so far: the first value starts it, then $m \leftarrow \alpha x + (1 - \alpha) m$. Raise `ValueError` unless $0 < \alpha \le 1$. Two averages made by two calls must not share state.

*Answer:*

```python
def make_ewma(alpha: float):
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")
    state = None
    def update(x: float) -> float:
        nonlocal state                               # rebinding an enclosing name needs nonlocal
        state = x if state is None else alpha * x + (1 - alpha) * state
        return state
    return update
```

*Checks:* with $\alpha = 0.5$ the inputs 10, 20, 20 give 10, 15.0, 17.5; two averages fed 1 then 3, and 100, give 1, 2.0 and 100; $\alpha = 1$ returns the latest value; 0 and 1.5 raise.
*Decision point:* a module-level `state` passes the first check and fails the independence check.

**Y5, example 1 (difficulty 4, predict).**

```python
grid = [[0] * 2] * 2
grid[0][0] = 5
t = ([1], 2)
try:
    t[0] += [3]
except TypeError:
    pass
d = {1: "a", 1.0: "b", True: "c"}
print(grid, t, d)
```

*Answer:* `[[5, 0], [5, 0]] ([1, 3], 2) {1: 'c'}`. *Working:* both rows are one list. `t[0] += [3]` extends the list in place, then fails to store the result back into the tuple, so the change survives the error. `1`, `1.0` and `True` are equal and hash equally, so they are one key, keeping its first spelling and its last value.

**Y5, example 2 (difficulty 5, long-form).** A colleague removes duplicate trade ids with `if x not in seen: seen.append(x)` on a list. Explain why this is slow, estimate the comparisons for 100,000 unique ids, give the set version's cost, and state what set members need and what a set costs.

*Model answer:* (1) `x not in seen` on a list compares `x` with each stored item in turn: up to $k$ comparisons when $k$ ids are stored. (2) For $n$ unique ids that is $0 + 1 + \cdots + (n - 1) = \frac{n(n - 1)}{2} \approx 5 \times 10^9$ comparisons at $n = 10^5$: quadratic. (3) A set hashes `x` to a bucket and compares it only with the few items there, constant time on average, so the pass is about $n$ steps: linear. (4) Members must be hashable, with a hash that never changes while stored, which is why lists cannot be members. (5) Costs: more memory per item than a list, no order to rely on (use `dict.fromkeys(ids)` to de-duplicate keeping first-seen order), and a linear worst case per lookup if many hashes collide.
*Rubric (10):* 2 for the per-lookup scan; 2 for $\frac{n(n-1)}{2}$ and its size; 2 for hashing and average constant time; 2 for hashability and why lists fail; 2 for two costs or the order-keeping alternative.

**B1, example 1 (difficulty 4, predict).**

```python
from itertools import accumulate, groupby
xs = [3, 1, 4, 1, 5]
it = iter(xs)
print(next(it), list(it), list(it))
print(list(accumulate(xs, max)))
print([(k, len(list(g))) for k, g in groupby("aabba")])
gen = (x * x for x in xs)
print(sum(gen), sum(gen))
```

*Answer:* `3 [1, 4, 1, 5] []`, then `[3, 3, 4, 4, 5]`, then `[('a', 2), ('b', 2), ('a', 1)]`, then `52 0`. *Working:* an iterator is used up once; `accumulate` with `max` is a running maximum; `groupby` groups consecutive keys only; the second `sum` meets an exhausted generator.

**B1, example 2 (difficulty 5, code).** Write `rolling_mean(iterable, n)` that lazily yields the mean of the last `n` values once `n` have arrived, with constant work per value, working on an endless input. It must raise `ValueError` for `n < 1` at the moment it is called.

*Answer:*

```python
from collections import deque

def rolling_mean(iterable, n: int):
    if n < 1:
        raise ValueError("n must be at least 1")    # checked now, in an ordinary function
    return _rolling(iterable, n)

def _rolling(iterable, n):
    window, total = deque(), 0.0
    for x in iterable:
        window.append(x)
        total += x
        if len(window) > n:
            total -= window.popleft()               # constant time at the left end, unlike list.pop(0)
        if len(window) == n:
            yield total / n
```

*Checks:* `list(rolling_mean([1, 2, 3, 4, 5], 3)) == [2.0, 3.0, 4.0]`; the first four values from `rolling_mean(itertools.count(), 2)` are 0.5, 1.5, 2.5, 3.5; fewer than `n` values yield nothing; hidden: $10^5$ random values agree with a direct mean within `rel_tol=1e-9`.
*Decision point:* with the check inside the generator function itself, `rolling_mean(xs, 0)` raises nothing until the first `next` [verified], so a test that expects the error at the call fails. The body of a generator function runs only when values are requested.

**B2, example 1 (difficulty 4, predict).**

```python
def f(x):
    try:
        r = 10 / x
    except ZeroDivisionError:
        print("A")
        return -1
    else:
        print("B")
        return r
    finally:
        print("C")
print(f(0))
print(f(5))
```

*Answer:* six lines: `A`, `C`, `-1`, `B`, `C`, `2.0`. *Working:* `finally` runs after the return value is computed and before the function exits, so `C` prints before the caller prints the value.

**B2, example 2 (difficulty 5, long-form).** A colleague writes:

```python
def load_prices(path):
    try:
        rows = read_rows(path)
        return {r["date"]: float(r["close"]) for r in rows}
    except:
        return {}
```

Give three distinct ways the bare `except` makes failures worse, rewrite the error handling, and say when catching broadly is right.

*Model answer:* (1) It hides bugs in the code itself: a misspelt name (`NameError`) or a wrong key returns `{}` as though the file were empty. (2) It turns an error into wrong data: an empty dict flows into a report that shows no prices, so the failure surfaces far from its cause, if at all. (3) A bare `except` also catches `KeyboardInterrupt` and `SystemExit`, so Ctrl+C cannot stop a long run. (4) Rewrite: catch only what this function can handle. Let `FileNotFoundError` propagate, or re-raise it with the path in the message; turn a bad row into `ValueError` naming the row and use `raise ... from err` to keep the cause; let everything else propagate. (5) Catching broadly is right only at a program's outer boundary, such as a scheduler or a request loop, where the handler logs the full traceback and reports the failure, never continuing silently.
*Rubric (10):* 2 for each distinct harm, up to three; 2 for a rewrite that catches specific exceptions and keeps the cause; 2 for the outer-boundary rule with logging.

**B3, example 1 (difficulty 4, code).** Write `parse_trade_line(line)` for chat lines such as `bought 200 AAPL @ 189.50` and `sold 1,500 msft @ 410`. Return `(side, qty, ticker, price)` with side `"buy"` or `"sell"`, an `int` quantity, an upper-case ticker of 1 to 5 letters and a `Decimal` price; return `None` for anything else, including extra words.

*Answer:*

```python
import re
from decimal import Decimal

PATTERN = re.compile(
    r"\s*(bought|sold)\s+(\d{1,3}(?:,\d{3})+|\d+)\s+([A-Za-z]{1,5})\s*@\s*(\d+(?:\.\d+)?)\s*",
    re.IGNORECASE,
)

def parse_trade_line(line: str):
    m = PATTERN.fullmatch(line)                     # fullmatch: nothing before or after
    if m is None:
        return None
    verb, qty, ticker, price = m.groups()
    side = "buy" if verb.lower() == "bought" else "sell"
    return side, int(qty.replace(",", "")), ticker.upper(), Decimal(price)
```

*Checks:* the two examples give `("buy", 200, "AAPL", Decimal("189.50"))` and `("sell", 1500, "MSFT", Decimal("410"))`; `Bought 12 F@12.5` parses; `bought 1,234,567 X @ 2` gives 1234567; `sold 1,50 X @ 1`, `bought 200 AAPL @ 189.50 thanks` and `sold 1500 BRK.B @ 1` give `None`.
*Decision point:* `re.search` accepts the line ending "thanks", because a match need not cover the whole line; `fullmatch` rejects it [verified].

**B3, example 2 (difficulty 5, numeric and explanation).** A US-listed stock closes at 16:00 New York time. Give the London clock time of the close on 7 March, 14 March, 4 April, 31 October and 7 November 2025, and the UTC time on 31 October. Then explain why code must convert by date, not by a fixed offset.

*Answer:* 21:00, 20:00, 21:00, 20:00, 21:00; 20:00 UTC on 31 October [verified with `zoneinfo`].
*Working:* New York is 5 hours behind UTC in winter and 4 in summer; London is on UTC in winter and 1 hour ahead in summer. In 2025 the US changed on 9 March and 2 November and the UK on 30 March and 26 October (the rules "second Sunday of March, first Sunday of November" and "last Sundays of March and October"). Between the two spring changes and between the two autumn changes the gap is 4 hours, not 5. A fixed offset is wrong for about four weeks a year (three in March, one around the start of November), so a job scheduled "at 21:00 London, after the US close" runs an hour after the close in those weeks, and one moved to 20:30 to catch them runs before the close for the rest of the year. Convert aware times: `datetime(2025, 3, 14, 16, tzinfo=ZoneInfo("America/New_York")).astimezone(ZoneInfo("Europe/London"))`.
*Marks:* 1 per correct time (6); 2 for the two rules and the gap windows; 2 for the consequence and the `zoneinfo` conversion.

**B4, example 1 (difficulty 4, diagnosis).** A folder holds `main.py` (`import random` then `print(random.randint(1, 6))`) and `random.py` (`def shuffle_book(book): ...`). `python main.py` fails with `AttributeError: module 'random' has no attribute 'randint'`. Explain, and give two fixes.

*Answer:* when Python runs a script, the script's folder is first on the module search path (`sys.path[0]`), so `import random` loads the local `random.py`, which has no `randint`. Fixes: rename the file (for example `book_tools.py`) and delete the stale `__pycache__`; or put project modules in a package so their names are qualified (`from zq.book_tools import shuffle_book`). `python -c "import random; print(random.__file__)"` run in that folder shows which file loaded.

**B4, example 2 (difficulty 5, long-form).** A colleague's notebook reports a Sharpe ratio of 2.1. You must reproduce it exactly next month. List what must be pinned, seeded and recorded, and design a project layout that guarantees reproduction.

*Model answer:* (1) Code: the exact commit, with the notebook's logic moved into modules the notebook imports, so no cell holds hidden state. (2) Environment: the Python version and every package pinned (a lock file or `pip freeze` output) and installed into a fresh virtual environment. (3) Data: input files identified by a content hash or a dated snapshot; vendors revise history (corrections, adjustments), so the same ticker is not the same data next month. (4) Randomness: one recorded seed feeding `default_rng(seed)` objects passed down explicitly, never global state. (5) Execution: a clean "restart and run all", ideally as a script run in CI that writes the Sharpe ratio to a results file and a test that compares it with 2.1 within a stated tolerance.
*Rubric (10):* 2 per element: code at a commit with logic in modules; a pinned environment; a hashed data snapshot; recorded seeds; a clean-run check.

**B5, example 1 (difficulty 4, code).** Write a frozen dataclass `Money(amount: Decimal, currency: str)` whose `+` adds amounts in the same currency, raises `ValueError` for different currencies, works with `sum()`, and returns `NotImplemented` for other types.

*Answer:*

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)                             # frozen: immutable and hashable
class Money:
    amount: Decimal
    currency: str

    def __add__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise ValueError(f"cannot add {self.currency} and {other.currency}")
            return Money(self.amount + other.amount, self.currency)
        if other == 0:                              # sum() starts from 0
            return self
        return NotImplemented                       # Python then raises a clear TypeError

    __radd__ = __add__
```

*Checks:* `sum([Money(Decimal("1.10"), "GBP"), Money(Decimal("2.20"), "GBP")]) == Money(Decimal("3.30"), "GBP")`; GBP plus USD raises `ValueError`; `Money(...) + 5` raises `TypeError`; `{Money(Decimal("1"), "GBP"), Money(Decimal("1.0"), "GBP")}` has one member, because equal `Decimal`s hash equally.

**B5, example 2 (difficulty 5, code).** Write `Portfolio(cash)` with `buy(sym, qty, px)`, read-only properties `cash` and `positions` (a copy), and `value(prices)` and `weights(prices)`. Cash must never go negative; quantities and prices must be positive.

*Answer:*

```python
class Portfolio:
    def __init__(self, cash: float):
        if cash < 0:
            raise ValueError("cash must be non-negative")
        self._cash = cash
        self._positions: dict[str, int] = {}

    @property
    def cash(self) -> float:                        # no setter: p.cash = -1 raises AttributeError
        return self._cash

    @property
    def positions(self) -> dict[str, int]:
        return dict(self._positions)                # a copy, so callers cannot break the invariant

    def buy(self, sym: str, qty: int, px: float) -> None:
        if qty <= 0 or px <= 0:
            raise ValueError("qty and px must be positive")
        cost = qty * px
        if cost > self._cash:
            raise ValueError("insufficient cash")
        self._cash -= cost
        self._positions[sym] = self._positions.get(sym, 0) + qty

    def value(self, prices: dict[str, float]) -> float:
        return self._cash + sum(q * prices[s] for s, q in self._positions.items())

    def weights(self, prices: dict[str, float]) -> dict[str, float]:
        v = self.value(prices)
        return {s: q * prices[s] / v for s, q in self._positions.items()}
```

*Checks:* from 10,000, buying 10 AAPL at 190 and 5 MSFT at 400 leaves cash 6,100, and at prices 200 and 410 the value is 10,150; `p.cash = -1` raises `AttributeError`; `p.positions["X"] = 1` leaves the portfolio unchanged; a purchase beyond the cash raises.
*Decision point:* returning `self._positions` itself would let a caller add a position without paying for it.

**A1, example 1 (difficulty 4, predict).**

```python
import numpy as np
a = np.arange(12).reshape(3, 4)
print(a[:, 1].shape, a[:, [1]].shape, a[1:, ::2].shape)
print(a.sum(axis=0).shape, a.sum(axis=1, keepdims=True).shape)
print((a / 2).dtype, np.array([2**62]) * 4)
```

*Answer:* `(3,) (3, 1) (2, 2)`, then `(4,) (3, 1)`, then `float64 [0]`. *Working:* an integer index drops its axis and a list index keeps it; `axis=0` collapses the three rows, leaving four values; $2^{62} \times 4 = 2^{64}$ wraps to 0 in `int64` without any warning for an array.

**A1, example 2 (difficulty 5, code).** Write `winsorise(r, lo_q, hi_q)` for a 2-D array of returns (days × stocks): clip each column at its own quantiles, ignoring `NaN` when computing them and leaving `NaN` in place; return a new array and leave the input unchanged.

*Answer:*

```python
import numpy as np

def winsorise(r, lo_q: float = 0.01, hi_q: float = 0.99) -> np.ndarray:
    r = np.asarray(r, dtype=float)
    lo = np.nanquantile(r, lo_q, axis=0)            # one bound per column, NaN ignored
    hi = np.nanquantile(r, hi_q, axis=0)
    return np.clip(r, lo, hi)                       # (n, k) against (k,) broadcasts; NaN stays NaN; new array
```

*Checks:* columns `[1, 2, 3, 100]` and `[10, 20, nan, 40]` with quantiles 0 and 0.5 become `[1, 2, 2.5, 2.5]` and `[10, 20, nan, 20]`; the input equals a saved copy afterwards and shares no memory with the result.
*Decision point:* `np.quantile` without the `nan` prefix returns `nan` bounds for any column with a gap and wipes that column; one quantile over the whole array mixes stocks with different volatilities.

**A2, example 1 (difficulty 4, numeric).** Three assets have weights $\mathbf{w} = (0.5, 0.3, 0.2)$, annual volatilities $(20\%, 10\%, 30\%)$ and correlations $\rho_{12} = 0.5$, $\rho_{13} = 0.2$, $\rho_{23} = -0.1$. Build $\mathbf{\Sigma}$ with $\Sigma_{ij} = \sigma_i \sigma_j \rho_{ij}$ in one NumPy expression and compute the portfolio volatility.

*Answer:* $\mathbf{\Sigma} = \begin{pmatrix} 0.04 & 0.01 & 0.012 \\ 0.01 & 0.01 & -0.003 \\ 0.012 & -0.003 & 0.09 \end{pmatrix}$, $\mathbf{w}^\top \mathbf{\Sigma} \mathbf{w} = 0.01954$ and volatility $\sqrt{0.01954} = 13.98\%$.
*Working:* `S = np.outer(vol, vol) * C` builds every $\sigma_i \sigma_j$ and multiplies element-wise by the correlation matrix; then `w @ S @ w`. By hand: $0.25(0.04) + 0.09(0.01) + 0.04(0.09) + 2[0.15(0.01) + 0.1(0.012) + 0.06(-0.003)] = 0.0145 + 0.00504$.
*Decision point:* `np.outer(vol, vol) @ C` is a matrix product and gives a different, meaningless matrix.

**A2, example 2 (difficulty 5, code and derivation).** Write `logsumexp(x)` returning $\ln \sum_i e^{x_i}$ for a 1-D array without overflow or underflow, returning `-inf` when every entry is `-inf`, and raising `ValueError` for an empty array. Derive the identity it uses.

*Answer:*

```python
import numpy as np

def logsumexp(x) -> float:
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        raise ValueError("empty input")
    m = x.max()
    if np.isinf(m):                                 # all -inf: the shift x - m would give nan
        return float(m)
    return float(m + np.log(np.exp(x - m).sum()))   # each exp(x - m) <= 1 and one equals 1
```

*Derivation:* $\ln \sum_i e^{x_i} = \ln\left(e^{m} \sum_i e^{x_i - m}\right) = m + \ln \sum_i e^{x_i - m}$. With $m = \max_i x_i$ the largest term is $e^0 = 1$, so the sum lies in $[1, n]$: it cannot overflow, and its logarithm is finite.
*Checks:* `[1000, 1000]` gives $1000 + \ln 2 = 1000.6931\ldots$ where the naive formula gives `inf`; `[-1000, -1000]` gives $-1000 + \ln 2$ where the naive formula gives `-inf`; `[0, 0, 0]` gives $\ln 3$; `[-inf, -inf]` gives `-inf`.

**A3, example 1 (difficulty 4, numeric).** A gambler starts with £10 and bets £1 at a time, winning each bet with probability $p = 0.49$, until reaching £20 or £0. (a) Using $P(\text{reach } N \text{ from } i) = \frac{1 - (q/p)^i}{1 - (q/p)^N}$ with $q = 1 - p$, find the probability of reaching £20. (b) A simulation of 10,000 games gives 0.389. Find its standard error and say whether it agrees with (a).

*Answer:* (a) 0.4013. (b) $\sqrt{0.4013 \times 0.5987 / 10{,}000} = 0.0049$; the simulation sits $\frac{0.389 - 0.4013}{0.0049} \approx -2.5$ standard errors away, outside the usual $\pm 2$ band, so suspect a bug (often an off-by-one in the stopping rule) before blaming luck.
*Note:* the formula is stated here; 1.5 derives it by first-step analysis.

**A3, example 2 (difficulty 5, code).** Write `mc_call(s0, k, sigma, n, seed, antithetic=False)` that simulates $S = S_0 e^{-\sigma^2/2 + \sigma Z}$ with $Z \sim N(0, 1)$ and returns the estimated $E[\max(S - K, 0)]$ and its standard error. With `antithetic=True`, use $n/2$ pairs $(Z, -Z)$ and the standard error of the pair averages.

*Answer:*

```python
import math
import numpy as np

def _payoff(z, s0, k, sigma):
    return np.maximum(s0 * np.exp(-sigma**2 / 2 + sigma * z) - k, 0.0)

def mc_call(s0, k, sigma, n, seed, antithetic=False):
    rng = np.random.default_rng(seed)
    if antithetic:
        z = rng.standard_normal(n // 2)
        pairs = (_payoff(z, s0, k, sigma) + _payoff(-z, s0, k, sigma)) / 2   # pairs are independent
        return pairs.mean(), pairs.std(ddof=1) / math.sqrt(n // 2)
    pay = _payoff(rng.standard_normal(n), s0, k, sigma)
    return pay.mean(), pay.std(ddof=1) / math.sqrt(n)
```

*Checks:* with $S_0 = K = 100$, $\sigma = 0.2$, $n = 100{,}000$ and seed 42: plain $7.951 \pm 0.042$, antithetic $7.981 \pm 0.033$, against the exact 7.9656; across seeds 0 to 19 every estimate is within 4 standard errors of the exact value; the same seed reproduces the same numbers.
*Decision point:* treating the $n$ antithetic payoffs as $n$ independent draws gives a standard error of 0.0418, overstating it and hiding the gain, because the two members of a pair are negatively correlated; the pair averages are the independent samples.

**D1, example 1 (difficulty 4, predict).**

```python
import pandas as pd
a = pd.Series([1.0, 2.0, 3.0], index=["x", "y", "z"])
b = pd.Series([10.0, 20.0], index=["y", "w"])
print((a + b).to_dict())
print(a.add(b, fill_value=0).to_dict())
print(len(a.loc["x":"y"]), len(a.iloc[0:1]))
```

*Answer:* `{'w': nan, 'x': nan, 'y': 12.0, 'z': nan}`, then `{'w': 20.0, 'x': 1.0, 'y': 12.0, 'z': 3.0}`, then `2 1`. *Working:* arithmetic aligns on the sorted union of labels and only `y` is in both; `fill_value` treats a missing side as 0; the label slice includes its end.

**D1, example 2 (difficulty 5, long-form).** Explain label alignment and how it differs from NumPy's positional arithmetic. Describe a P&L calculation where `.to_numpy()` gives a wrong answer with no error, and how to make it fail loudly instead.

*Model answer:* (1) Arithmetic between Series matches values by index label, producing the union of labels and `NaN` where a label is on one side only; NumPy matches by position and only checks shapes. (2) Positions indexed AAPL, MSFT, TSLA and prices indexed MSFT, AAPL, TSLA: `positions * prices` aligns and is right, while `positions.to_numpy() * prices.to_numpy()` multiplies AAPL's quantity by MSFT's price. (3) If one side lacks a ticker and holds another in its place, lengths still match and the wrong pairs are multiplied silently. (4) Fail loudly: keep the index; assert `positions.index.equals(prices.index)`, or `prices.reindex(positions.index)` followed by a check that nothing is missing; never drop to arrays before aligning. (5) Alignment has its own trap: a `NaN` from a missing price silently drops out of `sum()`, so count missing values before summing.
*Rubric (10):* 2 for alignment by label with union and `NaN`; 2 for positional matching in NumPy; 2 for a concrete wrong-pair scenario; 2 for a loud check; 2 for the `NaN`-in-`sum` caveat.

**D2, example 1 (difficulty 4, code).** Write `load_closes(text)` for a vendor CSV with header `Date,Close,Volume`, day-first dates (`02/01/2024`), quoted thousands separators (`"1,234.50"`), `n/a` for missing values and possibly repeated rows. Return the closes as a `float` Series on a sorted `DatetimeIndex`, with exact duplicate rows removed, missing values as `NaN`, and `ValueError` if two different rows share a date.

*Answer:*

```python
import io
import pandas as pd

def load_closes(text: str) -> pd.Series:
    df = pd.read_csv(io.StringIO(text), thousands=",", na_values=["n/a"])
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")   # never let day and month be guessed
    df = df.drop_duplicates().set_index("Date").sort_index()
    if df.index.has_duplicates:
        raise ValueError("conflicting rows for the same date")
    return df["Close"].astype(float)
```

*Checks:* on the five-line sample (2 to 5 January 2024, missing on the 3rd, the 4th repeated) the result is 1234.50, `NaN`, 1240.00, 1251.25; a sample with two different closes on one date raises.
*Decision point:* without `format`, `03/04/2024` may be read month first; without `thousands=","` the column stays text.

**D2, example 2 (difficulty 5, long-form).** For each gap, choose forward fill, backward fill, interpolation, leaving `NaN`, or dropping the row, and justify: (a) a price missing on an exchange holiday in a multi-market dataset; (b) five days of prices missing in a vendor outage, in a backtest; (c) a missing daily return in a P&L series.

*Model answer:* (a) Forward fill the price: nothing traded, so the last price is the price, and a zero return that day is true. (b) Leave the gap (or exclude those days): forward filling invents five flat days and understates volatility, while interpolation and backward fill use prices from after the gap that nobody on those days could know; a backtest should not trade on data that did not exist. (c) Do not fill with 0 unless the book was flat: a missing P&L is unknown, not zero; rebuild it from positions and prices, or mark the day missing and report how many days were excluded. (d) The general rule: a fill may only use what was knowable at that time. (e) Whatever the choice, count and log the gaps, because a silent fill changes every statistic downstream.
*Rubric (10):* 2 each for (a), (b) with the look-ahead argument, (c), the knowable-at-the-time rule, and counting and logging.

**D3, example 1 (difficulty 4, numeric).** A trades table has 1,000 rows. A reference table has one row per ticker, except 20 tickers listed twice. Those 20 tickers account for 240 trades, and 30 trades have tickers missing from the reference table. How many rows does an inner merge on ticker return, and a left merge? What do `validate="many_to_one"` and `indicator=True` show?

*Answer:* inner 1,210, left 1,240 [verified on a constructed frame]. *Working:* 970 trades match; the 240 on duplicated tickers each match twice, adding 240 rows: $970 + 240 = 1{,}210$; the left merge also keeps the 30 unmatched rows. `validate="many_to_one"` raises `MergeError` because the right-hand keys are not unique; `indicator=True` adds a `_merge` column with 30 rows marked `left_only`.

**D3, example 2 (difficulty 5, code).** Given a long frame with columns `date`, `ticker`, `sector`, `ret`, write `add_features(df, q)` returning a copy with `ret_sn` (each return minus its sector's mean on that date) and `bucket` (the stock's quantile group within its date, 1 to `q` from low to high, ties broken by order of appearance).

*Answer:*

```python
import pandas as pd

def add_features(df: pd.DataFrame, q: int = 5) -> pd.DataFrame:
    out = df.copy()
    sector_mean = out.groupby(["date", "sector"])["ret"].transform("mean")   # one value per row
    out["ret_sn"] = out["ret"] - sector_mean
    out["bucket"] = out.groupby("date")["ret"].transform(
        lambda r: pd.qcut(r.rank(method="first"), q, labels=False) + 1    # within each date
    )
    return out
```

*Checks:* on the 12-row sample (two dates, two sectors of three stocks, $q = 3$) the first date's sector-neutral returns are $-0.02$, 0 and $0.02$ in each sector, and the buckets are D and E in 1, A and F in 2, B and C in 3.
*Decision point:* `qcut` on the raw returns raises on duplicate edges when returns tie, which ranking first prevents; `agg("mean")` instead of `transform` returns one row per (date, sector) and cannot be subtracted row by row.

**D4, example 1 (difficulty 4, numeric).** A portfolio holds two stocks and is rebalanced to weights 0.6 and 0.4 at every close. Their simple daily returns are $+5\%$ and $-10\%$ on day 1, then $-2\%$ and $+4\%$ on day 2. (a) Give the portfolio's simple return each day. (b) Give its two-day return. (c) If instead the portfolio is bought at 60/40 and held, what is the two-day return? (d) What does weighting the two stocks' log returns give for day 1, and why is it wrong?

*Answer:* (a) $0.6(0.05) + 0.4(-0.10) = -1.0\%$, and $0.6(-0.02) + 0.4(0.04) = +0.4\%$. (b) $(0.99)(1.004) - 1 = -0.604\%$. (c) $0.6(1.05)(0.98) + 0.4(0.90)(1.04) - 1 = 0.6174 + 0.3744 - 1 = -0.82\%$. (d) $\exp\left(0.6 \ln 1.05 + 0.4 \ln 0.90\right) - 1 = -1.279\%$, not $-1.0\%$ [verified].
*Working:* a portfolio's value is the weighted sum of its holdings' values, so its simple return is the weighted average of simple returns. A logarithm does not pass through a sum, so log returns add correctly over time for one asset (0.3 lesson 57) but do not average across assets at one time. Without rebalancing the weights drift (after day 1 stock A is $\frac{0.63}{0.99} \approx 64\%$ of the book), which is why (b) and (c) differ.
*Decision point:* $\sum_i w_i \ln(1 + r_i) \le \ln\left(1 + \sum_i w_i r_i\right)$ because $\ln$ is concave (Jensen's inequality, proved in 1.5), so the weighted log average always understates the portfolio's return, here by 0.28 percentage points.

**D4, example 2 (difficulty 5, code).** This backtest has look-ahead:

```python
ret = prices.pct_change()
signal = np.sign(ret)
strategy = (signal * ret).fillna(0)
```

Write `strategy_returns(prices)` that trades on yesterday's signal, and report both versions' total returns on the closes 100, 101, 99, 100, 102, 101, 103.

*Answer:*

```python
import numpy as np
import pandas as pd

def strategy_returns(prices: pd.Series) -> pd.Series:
    ret = prices.pct_change()
    signal = np.sign(ret)                           # known at today's close
    position = signal.shift(1)                      # held from the next day: decisions use only the past
    return (position * ret).fillna(0)
```

*Checks:* the look-ahead version compounds to $+9.28\%$ and the honest one to $-3.94\%$; the first two honest returns are 0; a perturbation test changes one future price and confirms no earlier strategy return moves.
*Decision point:* $\text{sign}(r_t) \cdot r_t = |r_t|$, so the same-row version earns the size of every move. A strategy that earns the absolute value of every return is impossible; that impossibility is the general smell test for look-ahead.

**D5, example 1 (difficulty 4, code with figure assertions).** Write `exit_figure(close)` returning a matplotlib `Figure` with three stacked panels sharing the x-axis: price on a log scale, daily returns, and drawdown, each with a y-label, and a title on the top panel.

*Answer:*

```python
import matplotlib.pyplot as plt
import pandas as pd

def exit_figure(close: pd.Series):
    ret = close.pct_change()
    dd = close / close.cummax() - 1
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(9, 8),
                                        height_ratios=[2, 1, 1], layout="constrained")
    ax1.plot(close.index, close.to_numpy())
    ax1.set_yscale("log")
    ax1.set_ylabel("Price (log scale)")
    ax1.set_title("Price, daily returns and drawdown")
    ax2.plot(ret.index, ret.to_numpy(), linewidth=0.8)
    ax2.set_ylabel("Daily return")
    ax3.fill_between(dd.index, dd.to_numpy(), 0)
    ax3.set_ylabel("Drawdown")
    return fig
```

*Figure assertions:* three Axes; the first has a log y-scale; every Axes has a y-label; the first and third share the x-axis; the first line's y-data equals the closes [verified with matplotlib on the Agg backend].
*Decision point:* `plt.title(...)` after building the panels titles the last panel, not the first.

**D5, example 2 (difficulty 5, long-form).** A brochure plots a fund's value on a left axis running from 95 to 130 and a technology index on a right axis, from March 2009 to today, and says the fund "keeps pace with technology at a fraction of the risk". Identify the ways the chart misleads and specify the honest version.

*Model answer:* (1) Dual axes: each axis is scaled independently, so any two rising series can be made to overlap; the "keeping pace" is drawn, not measured. (2) The left axis starts at 95, which magnifies the fund's moves; growth comparisons need both series rebased to 100 on one shared axis, logarithmic for long periods. (3) The start date, March 2009, is the bottom of the financial crisis for equities, flattering any equity strategy; results should be shown from several start dates or the full history. (4) "A fraction of the risk" needs a risk measure the chart does not show: report annualised volatility and maximum drawdown for both over the same period. (5) The honest version: both rebased to 100 at a stated, justified start, one log axis, labelled units and source, and a table of annualised return, volatility and maximum drawdown.
*Rubric (10):* 2 each for dual axes, the truncated axis, the start date, the unsupported risk claim, and a complete honest specification.

**D6, example 1 (difficulty 4, numeric).** A trade file has 10 million rows: six `float64` columns, an `int64` quantity, and a ticker column of 3,000 distinct strings stored as Python objects. (a) How much memory do the six float columns take as `float64`, and as `float32`? (b) What is 12345.67 after a round trip through `float32`? (c) Which change saves memory safely?

*Answer:* (a) $10^7 \times 6 \times 8 = 480$ MB, and 240 MB as `float32`. (b) 12345.669921875: `float32` keeps about 7 significant digits, so this price still rounds back to 12345.67, but from $2^{17} = 131{,}072$ upwards a single price can no longer hold the penny (131072.01 comes back as 131072.015625, which rounds to 131072.02), and sums of millions of `float32` values drift long before that [verified]. (c) The ticker column as `category` (integer codes plus 3,000 strings) is safe and usually the largest saving; `float32` is acceptable for returns used in plots, not for prices or P&L that must reconcile to the penny.

**D6, example 2 (difficulty 5, code).** Write `summarise(close, periods=252)` returning a dict with `ann_vol` (the sample standard deviation of simple returns times $\sqrt{\text{periods}}$), `max_dd` (a positive fraction), `peak`, `trough`, and `recovery` (the first date at or above the peak after the trough, or `None`). Drop missing closes first; raise `ValueError` for fewer than 3 prices or any non-positive price.

*Answer:*

```python
import math
import pandas as pd

def summarise(close: pd.Series, periods: int = 252) -> dict:
    close = close.dropna()
    if len(close) < 3 or (close <= 0).any():
        raise ValueError("need at least 3 positive prices")
    ret = close.pct_change().dropna()
    dd = close / close.cummax() - 1
    trough = dd.idxmin()
    peak = close.loc[:trough].idxmax()              # the peak this drawdown fell from
    after = close.loc[trough:]
    recovered = after[after >= close.loc[peak]]
    return {
        "ann_vol": ret.std(ddof=1) * math.sqrt(periods),
        "max_dd": -dd.min(),
        "peak": peak,
        "trough": trough,
        "recovery": recovered.index[0] if len(recovered) else None,
    }
```

*Checks:* closes 100, 120, 90, 110, 80, 130, 125 on business days from 1 January 2024 give `max_dd` $\frac{1}{3}$, peak 2 January, trough 5 January, recovery 8 January; ending at 100 and 115 instead gives no recovery.
*Decision point:* `close.idxmax()` over the whole series returns the later 130, not the 120 the drawdown fell from.

### 3.2 Item 1.2 Tools

| Level | Set | Items | Difficulty mix | Long-form item (rubric: five points of 2 marks) | Code and state drills | Generators |
|---|---|---|---|---|---|---|
| T1 | `set.toolkit.shell` | 7 | d3 ×3, d4 ×2, d5 ×2 | What happens, step by step, in `grep -c ERROR *.log > summary.txt 2>&1`, including the no-match case | `drl.tools.pipeline-answer` (a pipeline graded on its output), `drl.tools.find-results`; local task: paste `pwd`, `ls -la` and one pipeline's output from your machine | `gen.tools.pipeline-predict`, `gen.tools.glob-match`, `gen.tools.redirect-predict` |
| T2 | `set.toolkit.shell-work` | 7 | d3 ×3, d4 ×2, d5 ×2 | What `set -euo pipefail` does, letter by letter, and one case where `-e` surprises | `drl.tools.daily-script`, `drl.tools.path-fix` (state); local task: make a script executable with a shebang and paste `ls -l` and its output | `gen.tools.chmod-octal`, `gen.tools.path-resolve` |
| T3 | `set.toolkit.git-basics` | 7 | d3 ×3, d4 ×2, d5 ×2 | A forced push after `reset --hard HEAD~2`: what happened, how to recover, what to do instead | `drl.tools.commit-msg-lint` (Python: subject length, blank line, imperative mood check), three `git-graph` targets; local task: `git init`, three commits, paste `git log --oneline` | `gen.tools.status-predict`, `gen.tools.graph-target`, `gen.tools.undo-match` |
| T4 | `set.toolkit.git-collab` | 7 | d3 ×3, d4 ×2, d5 ×2 | A key was pushed to a public repository: the order of actions, and why deleting the file is not enough | `drl.tools.secret-scan`, a `merge-conflict` kata with a semantic conflict; local task: push a branch to GitHub and open a pull request, paste its URL | `gen.tools.merge-kind`, `gen.tools.bisect-steps`, `gen.tools.gitignore-match` |
| T5 | `set.toolkit.testing` | 7 | d3 ×3, d4 ×2, d5 ×2 | A test plan for `max_drawdown`: partitions, boundaries, a property, and what each catches | `drl.tools.vol-tests` (learner tests against mutants), `drl.tools.fixture-cleanup`, `drl.tools.property-mdd`; local task: run `pytest -q` on the 1.1 project and paste the summary | `gen.tools.mutant-kill`, `gen.tools.approx-tol` |
| T6 | `set.toolkit.sql-query` | 7 | d3 ×3, d4 ×2, d5 ×2 | Three-valued logic: why `NOT IN` against a list holding `NULL` returns nothing, with the truth table | `drl.tools.sql-traders`, `drl.tools.sql-never-traded`; local task: open a SQLite file with the `sqlite3` shell and paste one query's output | `gen.tools.sql-predict`, `gen.tools.null-predict`, `gen.tools.join-count` |
| T7 | `set.toolkit.sql-analysis` | 7 | d3 ×3, d4 ×2, d5 ×2 | SQL or pandas: where to aggregate a 50-million-row trades table, and why parameters stop injection | `drl.tools.sql-returns` (window function), `drl.tools.trades-for` (Python with parameters); local task: load a CSV into SQLite and query it from Python | `gen.tools.window-predict`, `gen.tools.cte-order` |

**Example problems, 1.2.** Shell examples ran in GNU bash 5.2.21, Git examples in Git 2.43.0, SQL examples through Python's `sqlite3` on SQLite 3.45.1 and on Pyodide's SQLite 3.39.0, and the pytest example with pytest 9.1.1 against its four mutants [verified].

**T1, example 1 (difficulty 4, predict).** `trades.csv` has the header `time,sym,qty,px` and seven rows whose symbols are AAPL, MSFT, AAPL, TSLA, MSFT, AAPL, aapl. Predict the output of:

```bash
cut -d, -f2 trades.csv | tail -n +2 | sort | uniq -c | sort -rn | head -n 2
```

*Answer:* `3 AAPL` then `2 MSFT`, each count right-aligned by `uniq -c`. *Working:* `cut` keeps field 2; `tail -n +2` drops the header; `sort` makes equal names adjacent; `uniq -c` counts each run; `sort -rn` orders the counts from high to low. The lower-case `aapl` is a separate symbol with count 1: a data-quality finding, not a shell bug.

**T1, example 2 (difficulty 5, long-form).** Explain, step by step, what happens when you run `grep -c ERROR *.log > summary.txt 2>&1` in a folder holding `a.log` and `b.log`, and what changes when the folder holds no `.log` files.

*Model answer:* (1) The shell, not `grep`, expands `*.log` into the sorted matching names, so `grep` receives `-c`, `ERROR`, `a.log`, `b.log`. (2) The shell sets up redirections before `grep` starts, left to right: `> summary.txt` opens and empties the file as standard output, then `2>&1` points standard error at the same file. (3) With several files `grep -c` prints `name:count` per file, for example `a.log:1` and `b.log:2`. (4) With no match, bash passes the pattern `*.log` on literally; `grep` cannot open a file of that name, its error message goes into `summary.txt`, not to the screen, and its exit status is 2. (5) Writing `2>&1 > summary.txt` instead sends errors to the terminal, because `2>&1` copies wherever standard output pointed at that moment; `shopt -s nullglob`, or a check that files exist, avoids the literal pattern.
*Rubric (10):* 2 for expansion by the shell before the program runs; 2 for left-to-right redirection with both streams in the file; 2 for the per-file count format; 2 for the no-match behaviour and where the error goes; 2 for redirection order or a `nullglob` fix.

**T2, example 1 (difficulty 4, numeric).** `ls -l backtest.sh` shows `-rwxr-x---`. (a) Give the octal mode. (b) After `chmod g+w,o+r backtest.sh`, give the new string and octal mode. (c) Can a user outside the owner's group now run `./backtest.sh`?

*Answer:* (a) 750. (b) `-rwxrwxr--`, 774. (c) No: others have `r--`, so they can read the file but not execute it; `bash backtest.sh` would still work for them, because then only read permission is needed. *Working:* each triple sums read 4, write 2 and execute 1.

**T2, example 2 (difficulty 5, code).** Write `daily.sh` that runs `python3 clean.py "$f"` for every `data/*.csv`, stops at the first failure with a non-zero status, and otherwise prints `processed N files`.

*Answer:*

```bash
#!/usr/bin/env bash
set -euo pipefail                  # stop on any error, on unset variables, and on failures inside pipes

count=0
for f in data/*.csv; do
    python3 clean.py "$f"          # quoted, so a name with a space stays one argument
    count=$((count + 1))           # not ((count++)): that returns status 1 when count is 0, and -e exits
done
echo "processed $count files"
```

*Checks:* with a corrupt second file the script prints the first file's line and the error, then exits with status 1; with good files only it prints `processed 2 files` and exits 0; the simulator's hidden tests add a file name with a space and an empty folder.
*Decision point:* in an empty folder the loop runs once with the literal `data/*.csv`, which `clean.py` cannot open, so the script fails [verified]. Add `shopt -s nullglob` if "no files" should succeed, or test for files first if it should be an error.

**T3, example 1 (difficulty 4, predict).** In an empty folder:

```bash
git init
echo a > x; echo b > y
git add x y; git commit -m "init"
echo a2 > x; git add x; echo a3 > x
echo c > z
git rm --cached y
git status --short
```

*Answer:*

```
MM x
D  y
?? y
?? z
```

*Working:* the first column compares the index with `HEAD`, the second the working tree with the index. `x` was staged as `a2` and then changed to `a3`, so it differs in both. `git rm --cached y` stages the deletion and leaves the file on disk, where it is now untracked. `z` was never added.

**T3, example 2 (difficulty 5, long-form).** A colleague ran `git reset --hard HEAD~2` on `main` after pushing two commits, then `git push --force`. Explain what happened locally and on the remote, how to recover the commits, and what should have been done instead.

*Model answer:* (1) Locally, `main` moved back two commits and the index and working tree were overwritten to match, destroying any uncommitted work for good. (2) The two commits still exist as objects and are listed in the reflog, so `git reflog` shows the old tip. (3) The forced push moved the remote `main` back too; anyone who had pulled still has the commits and now sees a diverged history. (4) Recovery: find the old tip in the reflog or in a colleague's clone, point `main` at it again (`git reset --hard <old tip>` on a clean tree) and push with `--force-with-lease`, telling the team first. (5) Instead, on a shared branch, undo with `git revert` for each commit, which adds new commits and needs no force; keep `reset` and other history rewrites for private branches.
*Rubric (10):* 2 for the local effect including lost uncommitted work; 2 for the reflog; 2 for the effect on collaborators; 2 for a correct recovery; 2 for `revert` as the right tool.

**T4, example 1 (difficulty 4, numeric and state).** (a) A test passes at a January tag and fails on today's `main`, with 1,000 commits between them. At most how many test runs does `git bisect` need, and why? (b) `main` has not moved since `feature` branched from it. Does `git merge feature` on `main` create a merge commit?

*Answer:* (a) 10. Each test halves the candidates and $2^{10} = 1{,}024 \ge 1{,}000$, so $\lceil \log_2 1000 \rceil = 10$: the bisection of 0.2 lesson 108 applied to history. A test that sometimes fails on a good commit breaks the halving, so make it deterministic first. (b) No. `main` is an ancestor of `feature`, so Git moves the pointer forward (a fast-forward) and creates no commit, unless `--no-ff` is given.

**T4, example 2 (difficulty 5, code).** Write `scan_diff(diff_text)` returning `(line_number, kind)` for every added line of a unified diff (starting with `+` but not `+++`) that contains an AWS-style access key id (`AKIA` and 16 upper-case letters or digits), a private-key header, or a string of at least 20 characters assigned to a name such as `api_key`, `secret`, `token` or `password`.

*Answer:*

```python
import re

RULES = [
    ("aws-access-key-id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("assigned-secret", re.compile(
        r"""(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*["'][^"'\s]{20,}["']""")),
]

def scan_diff(diff_text: str) -> list[tuple[int, str]]:
    hits = []
    for n, line in enumerate(diff_text.splitlines(), start=1):
        if not line.startswith("+") or line.startswith("+++"):
            continue                                # added lines only; "+++" is the file header
        for kind, pattern in RULES:
            if pattern.search(line):
                hits.append((n, kind))
    return hits
```

*Checks:* on a 9-line diff that removes an environment lookup and adds `API_KEY = "sk_live_51HxQ2eZvKYlo2C8fA9b"` (an invented value) on line 7, `aws = "AKIAIOSFODNN7EXAMPLE"` on line 8 and `# token = "short"` on line 9, the result is `[(7, "assigned-secret"), (8, "aws-access-key-id")]`. `AKIAIOSFODNN7EXAMPLE` is the example key in AWS's own documentation [searched]. The removed line is ignored because a removal cannot leak anything new.
*Decision point:* a scanner is the last line of defence, not the fix; a key already pushed must be revoked, because history keeps it.

**T5, example 1 (difficulty 4, learner tests).** `annualised_vol(returns, periods=252)` returns the sample standard deviation times $\sqrt{\text{periods}}$ and raises `ValueError` containing "at least two" for fewer than two returns. Write tests that pass on it and kill these mutants: (m1) the population standard deviation; (m2) multiplying by `periods` instead of its square root; (m3) ignoring `periods` and always using 252.

*Answer:*

```python
import math
import pytest
from vol import annualised_vol

def test_known_value_uses_sample_sd_and_sqrt_time():
    # returns 0.01 and -0.01: sample sd = sqrt(0.0002 / 1) = 0.01 * sqrt(2), worked by hand
    expected = 0.01 * math.sqrt(2) * math.sqrt(252)
    assert annualised_vol([0.01, -0.01]) == pytest.approx(expected, rel=1e-12)

def test_periods_scale_with_square_root():
    r = [0.02, -0.01, 0.005, 0.0]
    assert annualised_vol(r, periods=4) == pytest.approx(2 * annualised_vol(r, periods=1), rel=1e-12)

def test_constant_returns_have_zero_vol():
    assert annualised_vol([0.003] * 5) == pytest.approx(0.0, abs=1e-15)

@pytest.mark.parametrize("bad", [[], [0.01]])
def test_too_few_returns_raise(bad):
    with pytest.raises(ValueError, match="at least two"):
        annualised_vol(bad)
```

*Checks:* all five tests pass on the reference; m1 fails the first test, m2 fails two, m3 fails the second. A fourth mutant, checking `len(returns) < 1` instead of `< 2`, survives: `statistics.stdev` raises its own `StatisticsError`, a subclass of `ValueError` whose message also says "at least two", so the mutant behaves identically and `mutant-forge` discards it as equivalent.
*Decision point:* every expected value is worked by hand from the definition, never computed by calling the function under test.

**T5, example 2 (difficulty 5, long-form).** Write a test plan for `max_drawdown(prices)` (1.1 lesson 15): the input partitions, the boundary cases, at least two properties for Hypothesis, and what each would catch.

*Model answer:* (1) Partitions: non-decreasing series (answer 0); one drawdown; several drawdowns where the largest is not the first; a drawdown from a later, higher peak; invalid input (empty, zero or negative prices). (2) Boundaries: one price; two equal prices; a fall to the last element with no recovery; tied peaks, where the documented convention picks the first. (3) Hand-worked values: `[100, 120, 90, 110, 80, 130]` gives $\frac{1}{3}$ at indices 1 and 4, which catches max-minus-min and a peak reset to the global maximum. (4) Properties for any list of positive prices: $0 \le \text{mdd} < 1$; multiplying every price by a positive constant leaves it unchanged; appending a new all-time high leaves it unchanged; for a non-increasing series it equals $1 - \frac{\min}{\max}$. Hypothesis generates lists of positive floats and shrinks a failure to a minimal case. (5) Mapping: properties catch peak-reset and division errors on unusual inputs; invalid-input tests catch silent zeros; the tie test pins the convention.
*Rubric (10):* 2 for partitions; 2 for boundaries; 2 for hand-worked values; 2 for two valid properties; 2 for mapping tests to the bugs they catch.

**T6, example 1 (difficulty 4, result set).** The `trades` table holds (1, ana, AAPL, 100, 189.5), (2, ana, MSFT, 50, 410.0), (3, ben, AAPL, 200, NULL), (4, ben, TSLA, 10, 250.0), (5, ana, AAPL, 300, 189.4), (6, cal, MSFT, 75, 410.2), (7, ben, AAPL, 20, 189.4), (8, cal, NULL, 40, 100.0) as (id, trader, sym, qty, px). Predict:

```sql
SELECT trader, COUNT(*) AS n, COUNT(px) AS n_px, SUM(qty * px) AS notional
FROM trades
WHERE sym <> 'TSLA'
GROUP BY trader
HAVING COUNT(*) >= 2
ORDER BY trader;
```

*Answer:* `(ana, 3, 3, 96270.0)` and `(ben, 2, 1, 3788.0)`. *Working:* for row 8, `NULL <> 'TSLA'` is unknown, not true, so `WHERE` drops it and cal keeps one row, failing `HAVING`. Ben's row 3 counts in `COUNT(*)` but not `COUNT(px)`, and its `NULL` notional is skipped by `SUM`.

**T6, example 2 (difficulty 5, SQL).** With the same `trades` and a `securities(sym, name, sector)` table holding AAPL, MSFT, TSLA and NVDA, write (a) for each trader with at least 3 trades, the number of distinct symbols and the largest single notional, largest first; (b) the securities never traded, correct even though `trades.sym` contains a `NULL`.

*Answer:*

```sql
-- (a)
SELECT trader, COUNT(DISTINCT sym) AS n_syms, MAX(qty * px) AS max_notional
FROM trades
GROUP BY trader
HAVING COUNT(*) >= 3
ORDER BY max_notional DESC;

-- (b)
SELECT s.sym
FROM securities AS s
WHERE NOT EXISTS (SELECT 1 FROM trades AS t WHERE t.sym = s.sym);
```

*Results:* (a) `(ana, 2, 56820.0)` and `(ben, 2, 3788.0)`; (b) `NVDA`. The tempting `WHERE sym NOT IN (SELECT sym FROM trades)` returns no rows at all, because `'NVDA' NOT IN (..., NULL)` is unknown.

**T7, example 1 (difficulty 4, result set).** `closes(sym, d, close)` holds AAPL at 100, 102, 99.96 and MSFT at 50, 49, 49.49 on 2, 3 and 4 January 2024. Predict the result of the query below, and the one row that changes if `PARTITION BY sym ORDER BY d` inside `OVER` becomes `ORDER BY sym, d`.

```sql
SELECT sym, d, ROUND(close / LAG(close) OVER (PARTITION BY sym ORDER BY d) - 1, 4) AS ret
FROM closes
ORDER BY sym, d;
```

*Answer:* AAPL: `NULL`, 0.02, −0.02; MSFT: `NULL`, −0.02, 0.01. Without the partition, MSFT's first row becomes −0.4998: its close divided by AAPL's last close.

**T7, example 2 (difficulty 5, code).** Write `trades_for(conn, trader)` returning a pandas DataFrame of one trader's trades from SQLite, safe against injection, and show what the f-string version returns for the input `x' OR '1'='1`.

*Answer:*

```python
import sqlite3
import pandas as pd

def trades_for(conn: sqlite3.Connection, trader: str) -> pd.DataFrame:
    return pd.read_sql_query(
        "SELECT * FROM trades WHERE trader = ? ORDER BY id",
        conn,
        params=(trader,),                           # the value travels separately from the SQL text
    )
```

*Checks:* `trades_for(conn, "ana")` returns rows 1, 2 and 5; the injection input returns no rows; the f-string version, `f"SELECT * FROM trades WHERE trader = '{name}'"`, returns all 8 rows, because the input closes the quote and appends a condition that is always true. Parameters cannot stand for table or column names; those must come from a fixed list in the code.

### 3.3 Drills and projects

**Python Lab (1.1, 11 h).** Twenty-two 30-minute drills beyond homework, unlocked level by level, in four lab sets of kind `practice` (`set.pythink.lab`, `set.pybuild.lab`, `set.arrays.lab`, `set.dataframes.lab`):

| Level | Drills |
|---|---|
| Y1 | `drl.py.lab-settlement-hour` (hours and days with `divmod`, forwards and backwards in time), `drl.py.lab-float-sum` (a plain loop, Kahan's compensated loop and `math.fsum` compared on a million additions; the learner then explains why built-in `sum` agrees with `fsum` on Python 3.12 and later but with the loop on 3.11) |
| Y2 | `drl.py.lab-isin-check` (validate an ISIN check digit) |
| Y3 | `drl.py.lab-up-streaks` (longest run of up days), `drl.py.lab-years-to-double` (a `while` loop against the rule of 72, at ten rates rather than 0.4's one) |
| Y4 | `drl.py.lab-compose` (compose any number of functions), `drl.py.lab-lattice-paths` (memoised count of up-down paths ending above a level) |
| Y5 | `drl.py.lab-group-by-key`, `drl.py.lab-top-k` (the $k$ largest positions without sorting everything) |
| B1 | `drl.py.lab-pairwise` (a generator of consecutive pairs) |
| B2 | `drl.py.lab-retry` (a retry decorator that catches only named exceptions) |
| B3 | `drl.py.lab-log-levels` (count log lines by level with a regex), `drl.py.lab-business-days` (business days between two dates given a holiday list) |
| B5 | `drl.py.lab-vector` (a 2-D vector class with operators and `__repr__`) |
| A1 | `drl.py.lab-returns-matrix` |
| A2 | `drl.py.lab-zscore-columns` (0.2 lesson 105's standard scores, by broadcasting), `drl.py.lab-covariance` (from demeaned returns, checked against `np.cov`) |
| A3 | `drl.py.lab-birthday` (simulation against the exact product of 0.3 lesson 117), `drl.py.lab-pi-estimate` (with a standard error), `drl.py.lab-coupon-collector` |
| D | `drl.py.lab-ohlc` (daily to weekly bars), `drl.py.lab-calendar-gaps` |

**Project: Trade Ledger** (`prj.py.trade-ledger`, 6 h, after level B5). A package `ledger/`, standard library only (`needs: []`), so it runs on both targets and on the learner's own Python 3.11:

- `Trade` (frozen dataclass), `Ledger` with first-in-first-out matching per symbol, fees, realised and unrealised P&L, and a `LedgerError` for overselling and malformed input.
- CSV input through the `csv` module with row-numbered validation errors; prices from a JSON file; a command-line entry point (`python -m ledger trades.csv --prices prices.json`) that exits with status 1 on bad input.
- Type hints throughout, checked with a type checker on the learner's machine; a `zqtest` suite built from hand-worked cases, including lesson 55's £350.
- A results note of one page answering three questions: realised P&L on the supplied file under FIFO against average cost, and why they differ; how fees change it; what the program does on an oversell and why.
- Milestones and hours (CONTENT-FORMAT.md 3.8): the model and matching, 2.5 h; input, output and the command line, 2 h; the note, 1.5 h. Acceptance: the hidden tests pass on both runtimes; the note answers its three questions. In 1.2 this package is a candidate for the learner's first repository.

**Exit capstone** (`drl.py.exit-capstone` and the paste-verify `exit-1.1`, 10 h, after lesson 107). Specified in section 4.3; its hours are `1.1.exit`'s `estHours`.

**Tools Lab (1.2, 1.5 h, `set.toolkit.lab`).** `drl.tools.lab-bandit-log` (OverTheWire Bandit levels 0 to 5, with the commands used recorded and paste-verified), `drl.tools.lab-git-katas` (five target graphs in `git-graph`, in the style of Learn Git Branching), `drl.tools.lab-sql-puzzles` (five puzzles on a seeded trades database).

**The repository exit** (`prj.tools.repo`, 3 h, after level T5). The 1.2 exit, specified in section 4.3; its hours are `1.2.exit`'s `estHours`.

---

## 4. Topic exam blueprint

Both papers use the `topic` kind of the exam engine (ASSESSMENT.md 3.1): timed, no hints, no Bertie, one sitting, at least 3 parallel forms with at least 50% of marks from generator slots drawing on the exam reserve, a 3-day cool-down and a remediation set after a fail. Either paper can be sat first to test out of its topic (ASSESSMENT.md 7.3). Difficulty mix by marks: 20% at difficulty 2, 50% at 3, 20% at 4, 10% at 5. Pass mark 70%.

**Code in an exam.** Code items show visible examples that can be run; hidden tests run at submission and score $\lfloor m p / n \rfloor$ for $p$ of $n$ tests passed on an item worth $m$ (ASSESSMENT.md 3.5). Code items come from held-out drill families: the function to write is fixed per family, while its data, constants and test values vary by seed, so they count towards the generator share. Predict-output items show code that cannot be run: the scratch cell is disabled while such an item is open, and the attestation covers outside interpreters.

### 4.1 `exm.python`: 1.1 Python

**Duration** 90 minutes. **Marks** 80. **Items** 24. **Calculator** none needed; the scratch Python cell is available on code items only. **Pass** 56 of 80. **Runs on** both targets: every item needs only the standard library, NumPy and pandas (decision 14).
**Format mix by marks:** code 21 (26%), predict output 17 (21%), numeric 19 (24%), result table 4 (5%), multi-select 7 (9%), order 3 (4%), single choice 2 (3%), long-form 7 (9%).
**Difficulty mix by marks:** d2 16 (20%), d3 40 (50%), d4 16 (20%), d5 8 (10%).

| # | Section | Level | Skill | Format | Difficulty | Marks | Source |
|---|---|---|---|---|---|---|---|
| 1 | A Core language (20 min) | Y1 | Integer division and modulo with negatives, `round`, float equality | Predict output | 2 | 3 | `gen.py.predict-numeric` |
| 2 | A | Y1, Y5 | Aliasing, rebinding and in-place change, including through a function call | Predict output | 2 | 3 | `gen.py.alias-trace` |
| 3 | A | Y2 | Slices with negative indices and steps; one format specification | Predict output | 2 | 2 | `gen.py.slice-predict`, `gen.py.format-spec` |
| 4 | A | Y3 | Iteration count and final state of a `while` loop | Numeric (2 parts) | 3 | 3 | `gen.py.loop-count` |
| 5 | A | Y4 | Mutable default, scope and a closure made in a loop | Predict output | 3 | 3 | `gen.py.closure-predict`, `gen.py.arg-binding` |
| 6 | A | Y5 | Which operations grow with the collection's size | Multi-select | 3 | 3 | `gen.py.complexity-classify` |
| 7 | A | Y5 | Code: group records by key and return sorted summaries | Code | 3 | 4 | held-out drill family `gen.py.exam-group` |
| 8 | B Programs (20 min) | B1 | Iterator exhaustion and generator laziness | Predict output | 3 | 3 | `gen.py.iter-predict` |
| 9 | B | B2 | The lines `try`, `except`, `else` and `finally` print for two inputs | Order | 3 | 3 | `gen.py.exception-flow` |
| 10 | B | B3 | Code: parse lines with a regular expression, or convert times across zones | Code | 3 | 4 | held-out drill families `gen.py.exam-parse`, `gen.py.exam-tz` |
| 11 | B | B5 | Code: a frozen dataclass with arithmetic and validation | Code | 4 | 4 | held-out drill family `gen.py.exam-record` |
| 12 | B | B4 | Diagnose an import that loads the wrong module | Single choice | 2 | 2 | held-out pool, 4 variants |
| 13 | B | B2 | Review a function's error handling: harms, rewrite, boundary rule | Long-form, 10-point rubric scaled to 4 | 4 | 4 | held-out pool, 3 variants |
| 14 | C Arrays and simulation (20 min) | A1 | Shapes after indexing and reductions; view or copy | Predict output | 2 | 3 | `gen.py.shape-predict`, `gen.py.view-or-copy` |
| 15 | C | A2 | `ddof` and a broadcasting result | Numeric | 3 | 3 | `gen.py.reduction-predict`, `gen.py.broadcast-shape` |
| 16 | C | A2 | Code: vectorise a running-state loop under a time-ratio test | Code | 4 | 4 | held-out drill family `gen.py.exam-vectorise` |
| 17 | C | A3 | Standard error of a simulated proportion; trials needed for a target error | Numeric (2 parts) | 3 | 4 | `gen.py.se-trials` |
| 18 | C | A3 | Design a simulation to a stated error, justifying $1/\sqrt{n}$ | Long-form, scaled to 3 | 5 | 3 | held-out pool, 3 variants |
| 19 | D Data and time series (30 min) | D1 | Label alignment; `loc` against `iloc` row counts | Numeric (2 parts) | 2 | 3 | `gen.py.align-predict`, `gen.py.loc-iloc-count` |
| 20 | D | D3 | Merge row counts with duplicate and missing keys | Numeric | 3 | 3 | `gen.py.merge-count` |
| 21 | D | D3 | `agg` against `transform`: the resulting table | Result table | 3 | 4 | `gen.py.groupby-shape` |
| 22 | D | D4 | Select every line of a backtest that uses future information | Multi-select | 4 | 4 | held-out pool, 5 variants |
| 23 | D | D4 | Total return from simple and log returns; annual from daily volatility | Numeric (2 parts) | 3 | 3 | `gen.py.returns-numeric`, `gen.py.annualise` |
| 24 | D | D4 | Code: returns, annualised volatility and maximum drawdown with dates from a price Series | Code | 5 | 5 | held-out drill family `gen.py.exam-summary` |

Marks by course: Y 21 (26%), B 20 (25%), A 17 (21%), D 22 (28%), close to the courses' shares of lessons (26%, 25%, 19%, 30%). Generator slots outside the code families carry 46 marks (58%); the code families add 21 and the held-out pools 13.

### 4.2 `exm.tools`: 1.2 Tools

**Duration** 60 minutes. **Marks** 50. **Items** 18. **Calculator** none. **Pass** 35 of 50. **Runs on** both targets: shell and Git items in their JavaScript simulators, SQL items in the SQLite worker, and item 12 under the `zqtest` subset of pytest (plain `assert`, `approx`, `raises`, `parametrize`) on Pyodide's core, so the paper needs no load group beyond the standard library (decisions 14 and 23).
**Format mix by marks:** code 17 (34%), reach a state 7 (14%), predict output 5 (10%), entry 4 (8%), result table 3 (6%), match 3 (6%), order 2 (4%), numeric 2 (4%), single choice 2 (4%), long-form 5 (10%).
**Difficulty mix by marks:** d2 10 (20%), d3 25 (50%), d4 10 (20%), d5 5 (10%).

| # | Section | Level | Skill | Format | Difficulty | Marks | Source |
|---|---|---|---|---|---|---|---|
| 1 | A Shell (14 min) | T1 | Fix a command that breaks on a name with spaces | Reach a state (`shell-sim`) | 2 | 2 | `gen.tools.quote-fix` |
| 2 | A | T1 | Where each stream goes under a given redirection | Predict output | 2 | 2 | `gen.tools.redirect-predict` |
| 3 | A | T1 | Build a pipeline that answers a question about a log | Reach a state (graded on output) | 3 | 3 | `gen.tools.pipeline-task` |
| 4 | A | T2 | Octal and symbolic permissions; who can run the file | Entry | 3 | 2 | `gen.tools.chmod-octal` |
| 5 | A | T2 | Code: a script that loops over files and stops on the first failure | Code (shell) | 3 | 3 | held-out drill family `gen.tools.exam-script` |
| 6 | B Git (18 min) | T3 | `git status --short` after a command sequence | Predict output | 3 | 3 | `gen.tools.status-predict` |
| 7 | B | T3 | Reach a target graph with `branch`, `switch` and `commit` | Reach a state (`git-graph`) | 2 | 2 | `gen.tools.graph-target` |
| 8 | B | T3 | Match each mistake to `restore`, `reset` or `revert` | Match | 3 | 3 | `gen.tools.undo-match` |
| 9 | B | T4 | Resolve a merge so the tests pass, including a semantic conflict | Code (`merge-conflict`) | 4 | 4 | held-out pool, 4 variants |
| 10 | B | T4 | Order the commands that recover from a rejected push without force | Order | 3 | 2 | `gen.tools.push-recovery` |
| 11 | B | T4 | Maximum `bisect` steps for a given history | Numeric | 3 | 2 | `gen.tools.bisect-steps` |
| 12 | C Testing (12 min) | T5 | Write tests that pass on a reference and kill every mutant | Code (learner tests) | 4 | 3 | held-out drill family `gen.tools.exam-mutants` |
| 13 | C | T5 | Choose the right `approx` tolerance or `raises` usage | Single choice | 2 | 2 | `gen.tools.approx-tol` |
| 14 | C | T5 | A test plan: partitions, boundaries, properties | Long-form, 10-point rubric scaled to 5 | 5 | 5 | held-out pool, 3 variants |
| 15 | D SQL (16 min) | T6 | Predict a grouped result with `NULL`s | Result table | 3 | 3 | `gen.tools.null-predict` |
| 16 | D | T6 | Write a query with a join, grouping and `HAVING` | Code (SQL) | 3 | 4 | held-out drill family `gen.tools.exam-sql` |
| 17 | D | T7 | Write a window-function query for returns per ticker | Code (SQL) | 4 | 3 | held-out drill family `gen.tools.exam-window` |
| 18 | D | T7 | Type an input that injects into a string-built query | Entry | 2 | 2 | `gen.tools.injection` |

Marks by tool: shell 12 (24%), Git 16 (32%), testing 10 (20%), SQL 12 (24%), matching the lesson shares (25%, 31%, 19%, 25%). Generator slots outside the code families carry 28 marks (56%).

### 4.3 Exit-test mapping

The curriculum sets an exit line for each item. Both are rebuilt in the app as ASSESSMENT.md 2.9 defines them (`1.1.exit`, `1.2.exit`), with the details below. Neither exit is a timed paper, so they sit outside the exam engine and the topic exams do not replace them. A topic is complete when its exam is passed and its exit part is met (ASSESSMENT.md 2.12).

**`1.1.exit`: "From a CSV of daily prices, compute returns, annualised volatility and maximum drawdown, and plot them."**

| Part | Instrument | Detail |
|---|---|---|
| Brief | Shown in lesson 107 and in the drill | The conventions are fixed so that answers are checkable: simple daily returns from closes; sample standard deviation (`ddof=1`) times $\sqrt{252}$; maximum drawdown on closes as a positive fraction with its peak and trough dates; missing closes dropped, never filled, and the count of dropped rows reported; numbers printed to 6 decimal places and dates in ISO format |
| Input | `price-series` seeded file | About 1,260 rows (five years of trading days) with columns `Date`, `Close`, `Volume`. The clean variant has ISO dates; the messy variant has day-first dates, quoted thousands separators, `n/a` on one day, one exact duplicate row and rows out of order. No splits: the curriculum asks for "a CSV of daily prices", and adjusting for splits is lesson 106's subject, not the exit's [our choice] |
| Gate 1: capstone drill | `drl.py.exit-capstone`, `needs: [numpy, pandas, matplotlib]`: in the Artifact once matplotlib's load group ships there (open item 1), otherwise on the web app, returning by result code | Functions `load_prices(path)`, `daily_returns(close)`, `annualised_vol(returns, periods=252)`, `max_drawdown(close)` returning `(mdd, peak, trough)`, `make_figure(close)` and `main(argv)`. Hidden tests: every function on the clean and messy files at relative tolerance $10^{-6}$; a reordered file gives identical answers; constant prices give volatility 0 and drawdown 0; fewer than 3 prices raise `ValueError`; figure assertions as in homework D5 (three Axes, log scale on the first, shared x, y-labels, first line equal to the closes) |
| Gate 2: local run | `setup-checklist` paste-verify `exit-1.1` | The learner downloads a fresh seeded file (in the Artifact through the `downloads` capability), runs `python exit.py prices.csv` on their own machine, and pastes the printed summary and the `ls -l report.png` line. The app recomputes the four numbers from the same seed and compares at $10^{-6}$. Home paths are redacted before anything reaches Bertie |
| Help | Bertie | Locked until the first submission of gate 1, as for homework; unlocked for gate 2, which is about getting a local setup to work and is not an assessment of knowledge |
| Pass | Both gates | Gate 1 all hidden tests; gate 2 the four numbers match. `estHours` 10 |

**`1.2.exit`: "The 1.1 project is in a Git repository with at least one test. Everything you build from here on is too."**

| Part | Instrument | Detail |
|---|---|---|
| Rehearsal | `workspace-sim` and `git-graph` | Lesson 24's final screen and homework T5 rehearse the sequence: `git init`, `.gitignore`, a first commit, `tests/test_exit.py`, `pytest -q`, a second commit, push |
| Gate | `setup-checklist` paste-verify `exit-1.2` | Pasted from the learner's machine: `git log --oneline -n 5` (at least 2 commits), `git ls-files` (the exit script and at least one `test_*.py`), `git status` (clean), `pytest -q` (at least 1 passed, 0 failed), and the repository URL |
| Web check | GitHub API, web app only | The latest commit in the pasted log exists on the remote, and a `test_*.py` file is present. In the Artifact the paste stands alone (ASSESSMENT.md 2.9) |
| Expected content | Not gated [our choice] | Tests for `annualised_vol` and `max_drawdown` with hand-worked values (homework T5); a `.gitignore` excluding environments, downloaded data and secrets (lesson 18); a README saying how to run it; a CI workflow running pytest on every push (lesson 24). The checklist shows these as "recommended" ticks, because the curriculum's bar is one test and a stricter gate would be our invention |
| Habit | Weekly review (decision 17) | From the week 1.2 is passed, the weekly review asks for the link to the latest commit from the week's Build block. A missing link shows as a gap in the review, never as a failed exit |
| Pass | The gate | Reachable after level T5; `estHours` 3 (`prj.tools.repo`) |

**Rehearsal inside the topic exams.** `exm.python` item 24 is a timed, smaller version of the 1.1 capstone; `exm.tools` items 6, 12 and 16 rehearse the Git, testing and SQL steps the learner meets at work. A pass on either paper does not meet its exit, and an exit does not replace the paper: the paper closes the topic's knowledge, the exit proves the work on a real machine.

---

## 5. Reading and resource map per level

**How to use this map.** The app's lessons and homework are the spine. External resources play three roles: a second explanation when a quiz shows a gap (watch or read), extra problems (attempt), and stretch (top-programme material). Curriculum rule 1 (one resource per topic) is kept: CS50P and McKinney are the spine for 1.1, The Missing Semester and SQLBolt for 1.2; everything else is a targeted second explanation or stretch.

**Hours.** Each row's hours become its `Level.companion` entry (CONTENT-FORMAT.md 3.2), counted as earned when the learner logs the row done (ASSESSMENT.md 8.7, 11). The rows with hours sum to section 1's external budget: 30.0 h for 1.1 (16.0 h of videos and reading, 14.0 h of problems) and 8.25 h for 1.2 (4.75 h and 3.5 h). Rows at 0 h are conditional ("if the quiz is below 3 of 4") or stretch: optional, logged as spent time, never part of the estimate. Hours are my estimates for a learner meeting the material for the first time [our choice].

**McKinney and pandas 3.** McKinney's 3rd edition was written for pandas 1.4 [searched]. Where the pinned pandas 3.0.2 behaves differently, the lesson teaches the pinned behaviour and the reading row warns: copy-on-write and chained assignment (lesson 81), the `str` dtype for text (lessons 77, 105), `pct_change` without padding (lesson 93), and the frequency aliases `"ME"` and `"YE"`, because `"M"` and `"Y"` now raise `ValueError` (lesson 95) [verified].

**Resources, ids and licences** (all free unless marked paid). Ids come from `canon-gap.md` section 6 where it has them; ids marked † are new and requested in section 8. Licences are [recalled] unless marked; only CC BY material may be adapted (`problem-adapted`), everything else is cited (CONTENT-FORMAT.md 9.4).

| Short name | Resource | Id | Licence and use | Link |
|---|---|---|---|---|
| CS50P | Harvard, CS50's Introduction to Programming with Python (David Malan): lectures 0 to 9 and problem sets (the curriculum's choice) | `src.cs50p` | CC BY-NC-SA 4.0; cite | https://cs50.harvard.edu/python/ [check the current year's path] |
| ATBS | Al Sweigart, Automate the Boring Stuff with Python; the 3rd edition (No Starch, 2025) [searched] reorganised its chapters; chapter numbers below are the free 2nd edition's | `src.sweigart-atbs` | CC BY-NC-SA 3.0 (online edition); cite | https://automatetheboringstuff.com |
| MIT 6.100L | MIT OpenCourseWare 6.100L, Introduction to CS and Programming Using Python, Fall 2022 (Ana Bell) [searched] | `src.mit-6100l-2022` | CC BY-NC-SA 4.0; cite | https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/ |
| Guttag (paid) | John Guttag, Introduction to Computation and Programming Using Python, 3rd edition (MIT Press, 2021) | `src.guttag-2021` | Paid; cite | Publisher page |
| MIT 6.0002 | MIT OpenCourseWare 6.0002, Introduction to Computational Thinking and Data Science, Fall 2016 | `src.mit-60002-2016` † | CC BY-NC-SA 4.0; cite | https://ocw.mit.edu/courses/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/ |
| Composing Programs | John DeNero, Composing Programs, the text of Berkeley's CS 61A | `src.composing-programs` † | CC BY-SA 3.0; cite | https://www.composingprograms.com |
| Python Tutor | Philip Guo's execution visualiser | `src.python-tutor` † | Tool | https://pythontutor.com |
| Python docs | The Python Tutorial; the HOWTOs (Sorting, Unicode, Regular Expressions, Functional Programming, Logging, Argparse); the library reference | `src.python-docs` †; the floating-point chapter is `src.python-docs-float` | PSF documentation licence; cite | https://docs.python.org/3/ |
| Batchelder | Ned Batchelder, "Facts and myths about Python names and values" (PyCon 2015 talk and article) | `src.batchelder-names` † | Author's copyright; cite | https://nedbatchelder.com/text/names.html |
| PEP 8 | Style Guide for Python Code | `src.pep8` † | Public domain; cite | https://peps.python.org/pep-0008/ |
| McKinney | Wes McKinney, Python for Data Analysis, 3rd edition (O'Reilly, August 2022 [searched]), free online (the curriculum's choice) | `src.mckinney-pda-3e` | CC BY-NC-ND 4.0 (open edition); cite | https://wesmckinney.com/book/ |
| PDSH | Jake VanderPlas, Python Data Science Handbook (1st edition free online; 2nd edition 2022, paid) | `src.vanderplas-pdsh-2e` | Text CC BY-NC-ND 3.0, code MIT (1st edition); cite | https://jakevdp.github.io/PythonDataScienceHandbook/ |
| NumPy, pandas, matplotlib, SciPy docs | User guides of each library | `src.numpy-docs` †, `src.pandas-docs` †, `src.matplotlib-docs` †, `src.scipy-docs` † | BSD-style project licences; cite | https://numpy.org/doc/stable/user/, https://pandas.pydata.org/docs/user_guide/, https://matplotlib.org/stable/users/, https://docs.scipy.org/doc/scipy/tutorial/ |
| QuantEcon | Thomas Sargent and John Stachurski, Python Programming for Economics and Finance | `src.quantecon-python` † | CC BY-SA 4.0 [check]; cite | https://python-programming.quantecon.org |
| Rougier | Nicolas Rougier, From Python to Numpy (free online) | `src.rougier-numpy` † | CC BY-NC-SA 4.0; cite | https://www.labri.fr/perso/nrougier/from-python-to-numpy/ [check URL] |
| Wilke | Claus Wilke, Fundamentals of Data Visualization (free online) | `src.wilke-dataviz` † | CC BY-NC-ND 4.0; cite | https://clauswilke.com/dataviz/ |
| Goldberg | David Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic", ACM Computing Surveys, 1991 | `src.goldberg-1991` | ACM copyright; cite | ACM Digital Library [check a stable free URL] |
| Hull (paid) | John Hull, Options, Futures, and Other Derivatives, 11th edition (the curriculum's 1.7 text) | `src.hull-ofod-11e` | Paid; cite | Publisher page |
| Cont | Rama Cont, "Empirical properties of asset returns: stylized facts and statistical issues", Quantitative Finance 1(2), 2001 | `src.cont-2001` | Journal copyright; cite | Journal page [check for a free author copy] |
| Bailey et al. | David Bailey, Jonathan Borwein, Marcos López de Prado and Qiji Jim Zhu, "Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance", Notices of the AMS, May 2014 [searched] | `src.bailey-2014-charlatanism` | Free to read; cite | https://www.ams.org/notices/201405/rnoti-p458.pdf [searched] |
| Glasserman (paid) | Paul Glasserman, Monte Carlo Methods in Financial Engineering (Springer, 2003) | `src.glasserman-mc` | Paid; cite | Publisher page |
| Stat 110 | Harvard Stat 110, Probability (Joe Blitzstein), recorded lectures (filmed in autumn 2011 [searched]) | `src.stat110-2013` | Free to watch; cite | https://stat110.hsites.harvard.edu [searched] |
| Huff (paid) | Darrell Huff, How to Lie with Statistics (1954) | `src.huff-lie` † | Paid; cite | Any edition |
| Missing Semester | MIT, The Missing Semester of Your CS Education: the 2026 edition (nine lectures: Course Overview + Introduction to the Shell; Command-line Environment; Development Environment and Tools; Debugging and Profiling; Version Control and Git; Packaging and Shipping Code; Agentic Coding; Beyond the Code; Code Quality [searched]) and the 2020 edition for the lectures 2026 dropped | `src.missing-semester-2026`, `src.missing-semester-2020` | CC BY-NC-SA 4.0; cite | https://missing.csail.mit.edu/2026/, https://missing.csail.mit.edu/2020/ |
| Pro Git | Scott Chacon and Ben Straub, Pro Git, 2nd edition (free) | `src.pro-git-2e` | CC BY-NC-SA 3.0; cite | https://git-scm.com/book/en/v2 |
| Learn Git Branching | Interactive Git exercises | `src.learn-git-branching` † | MIT (code); tool | https://learngitbranching.js.org |
| TLCL | William Shotts, The Linux Command Line, 2nd edition (free PDF) | `src.shotts-tlcl` | CC BY-NC-ND 3.0; cite | https://linuxcommand.org/tlcl.php |
| Bandit | OverTheWire, Bandit wargame | `src.bandit` † | Free; tool | https://overthewire.org/wargames/bandit/ |
| explainshell, ShellCheck | Command explainer; shell-script linter | `src.explainshell` †, `src.shellcheck` † | GPL tools | https://explainshell.com, https://www.shellcheck.net |
| Software Carpentry | The Unix Shell; Version Control with Git; Databases and SQL | `src.swc-shell` †, `src.swc-git` †, `src.swc-sql` † | CC BY 4.0: adaptable | https://swcarpentry.github.io/shell-novice/, https://swcarpentry.github.io/git-novice/, https://swcarpentry.github.io/sql-novice-survey/ |
| SQLBolt | Interactive SQL lessons (the curriculum's choice) | `src.sqlbolt` | All rights reserved; cite | https://sqlbolt.com |
| SQLZoo | Interactive SQL tutorials | `src.sqlzoo` † | Cite | https://sqlzoo.net |
| CS50 SQL | Harvard, CS50's Introduction to Databases with SQL | `src.cs50-sql` † | CC BY-NC-SA 4.0; cite | https://cs50.harvard.edu/sql/ [check the current year's path] |
| CMU 15-445 | Andy Pavlo, Database Systems, recorded lectures | `src.cmu-15445` | Free to watch; cite | https://15445.courses.cs.cmu.edu [check the term] |
| SQLite docs | Datatypes, STRICT tables, window functions, foreign keys | `src.sqlite-docs` † | Public domain | https://www.sqlite.org/docs.html |
| OWASP | SQL Injection Prevention Cheat Sheet | `src.owasp-sqli` † | CC BY-SA 4.0; cite | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html |
| pytest, Hypothesis docs | pytest documentation; Hypothesis documentation | `src.pytest-docs` †, `src.hypothesis-docs` † | MIT; MPL-2.0; cite | https://docs.pytest.org, https://hypothesis.readthedocs.io |
| Okken (paid) | Brian Okken, Python Testing with pytest, 2nd edition (Pragmatic Bookshelf, 2022) | `src.okken-pytest-2e` | Paid; cite | Publisher page |
| MIT software construction | MIT 6.102 (formerly 6.031 and 6.005), Software Construction, readings on testing, specifications, code review and version control [searched in canon-gap] | `src.mit-software-construction` | CC BY-SA 4.0 [check]; cite | https://web.mit.edu/6.102/www/ [check the current term's path] |
| SWE at Google | Titus Winters, Tom Manshreck and Hyrum Wright, Software Engineering at Google (free online) | `src.swe-at-google` † | CC BY-NC-ND 4.0; cite | https://abseil.io/resources/swe-book |
| Beams | Chris Beams, "How to Write a Git Commit Message" | `src.beams-commit` † | Author's copyright; cite | https://cbea.ms/git-commit/ |
| GitHub Docs | GitHub flow; pull requests; building and testing Python with GitHub Actions; removing sensitive data | `src.github-docs` † | CC BY 4.0: adaptable | https://docs.github.com |

Confirmed by search on 6 October 2026: MIT 6.100L lectures 5, 6, 8, 11 and 13, MIT 6.0002 lecture 6 and Stat 110 lecture 7 (OCW and course pages); CS50P problem-set names for sets 0, 2, 3, 4, 5, 6, 7 and 8 (secondary sources: solution repositories, so the names hold for recent years but not necessarily for the current one); McKinney 4.1 to 4.7, 6.1 and 7.1 to 7.5. Still as I recall them [check each against the live resource before the content cites it]: the other 6.100L lecture numbers, chapter numbers for ATBS, TLCL, Wilke and Okken, McKinney's appendix A sections, and Pro Git section numbers.

### 5.1 Item 1.1 Python

| Level | Resource and location | What to do | Hours |
|---|---|---|---|
| Y1 | CS50P lecture 0, Functions and Variables (the variables, integers and floats segments) | Watch | 0.5 |
| Y1 | CS50P problem set 0: Indoor Voice, Playback Speed, Making Faces, Einstein, Tip Calculator [searched, secondary] | Attempt all five | 1.0 |
| Y1 | Batchelder, names and values | Read after lesson 1; replay his examples in Python Tutor | 0.25 |
| Y1 | Python tutorial 3.1.1 (numbers) and the floating-point chapter (`src.python-docs-float`) | Read both | 0.25 |
| Y1 | MIT 6.100L lecture 5, Floats and Approximation Methods [searched] | Watch only if lesson 4's quiz is below 3 of 4 | 0 |
| Y1 | Goldberg 1991, the opening sections on rounding error | Stretch: read; reference for lessons 4 and 66 | 0 |
| Y2 | CS50P problem set 2: camelCase, Just setting up my twttr, Vanity Plates [twttr and Vanity Plates searched, secondary; camelCase check] | Attempt all three | 1.0 |
| Y2 | Python docs, `string` module, "Format Specification Mini-Language" | Read; run every example | 0.25 |
| Y2 | Python Unicode HOWTO, the first two sections | Read after lesson 10 | 0.25 |
| Y2 | ATBS chapter 6, Manipulating Strings | Second explanation if a quiz is below 3 of 4 | 0 |
| Y3 | CS50P lectures 1 and 2, Conditionals and Loops (the segments on `elif`, `match`, and loops over lists and dicts) | Watch | 0.75 |
| Y3 | CS50P problem set 1: Deep Thought, Home Federal Savings Bank, File Extensions, Math Interpreter, Meal Time [check names; Deep Thought searched, secondary] | Attempt any three | 1.0 |
| Y3 | MIT 6.100L lectures 3 (iteration), 4 (guess-and-check) and 6 (Bisection Search) and problem set 1 [lecture 6 searched; lectures 3 and 4 and the problem set check] | Stretch | 0 |
| Y3 | Composing Programs 1.5, Control | Stretch: read | 0 |
| Y4 | Composing Programs 1.3 (Defining New Functions, with environment diagrams) and 1.6 (Higher-Order Functions) | Read both; draw two environment diagrams by hand and check them in Python Tutor | 0.75 |
| Y4 | Python Sorting HOWTO | Read the key-function and stability sections | 0.25 |
| Y4 | MIT 6.100L problem set 2 [check its topic] | Attempt | 1.0 |
| Y4 | MIT 6.100L lecture 8, functions as objects [searched], and the neighbouring lectures on decomposition and lambda [check numbers]; CS50P lecture 9's segments on `*args`, `**kwargs` and `global` | Watch one if lesson 17, 18 or 20's quiz is below 3 of 4 | 0 |
| Y4 | MIT 6.100L lectures on recursion [check numbers]; Composing Programs 1.7 | Stretch after lesson 21; 1.8 returns to both | 0 |
| Y5 | CS50P problem set 3: Fuel Gauge, Felipe's Taqueria, Grocery List, Outdated [last three searched, secondary; Fuel Gauge check] | Attempt all four | 1.0 |
| Y5 | Python tutorial chapter 5, Data Structures | Read 5.1 to 5.6 | 0.5 |
| Y5 | MIT 6.100L lecture 11, Aliasing and Cloning [searched] | Watch after lesson 23 | 0.25 |
| Y5 | ATBS chapters 4 and 5, Lists and Dictionaries; Composing Programs 2.4, Mutable Data | Second explanation; stretch | 0 |
| B1 | CS50P lecture 9, the iterator and generator segments | Watch | 0.25 |
| B1 | Python Functional Programming HOWTO (iterators, generators, `itertools`) | Read | 0.5 |
| B1 | Python docs, `itertools` recipes and `functools.lru_cache` | Try three recipes; time `lru_cache` on lesson 21's stairs | 0.5 |
| B1 | Composing Programs 4.2, Implicit Sequences | Stretch: read | 0 |
| B2 | CS50P lecture 3, Exceptions | Watch | 0.25 |
| B2 | Python tutorial chapter 8, Errors and Exceptions; Logging HOWTO, basic tutorial | Read both | 0.25 |
| B2 | Missing Semester 2026 lecture 4, Debugging and Profiling (the debugging half) | Watch | 0.25 |
| B2 | ATBS chapter 11, Debugging [check the chapter number] | Attempt its practice questions | 0.5 |
| B2 | MIT 6.100L lecture 13, Exceptions and Assertions [searched, secondary] | Watch only if lesson 35 or 36's quiz is below 3 of 4 | 0 |
| B3 | CS50P lectures 6 and 7, File I/O and Regular Expressions | Watch | 0.5 |
| B3 | CS50P problem sets 6 (Lines of Code, Pizza Py, Scourgify) and 7 (NUMB3RS, Working 9 to 5, Response Validation) [searched, secondary] | Attempt four of the six | 1.5 |
| B3 | Python Regular Expression HOWTO; Argparse tutorial | Read the HOWTO; work through the tutorial | 0.25 |
| B3 | Python docs, `csv`, `json`, `datetime` and `zoneinfo` | Read each module's introduction and examples | 0.25 |
| B3 | McKinney 6.1, Reading and Writing Data in Text Format [searched]; ATBS chapters on regular expressions, files, CSV and JSON [check numbers] | Preview of D2; second explanation | 0 |
| B4 | CS50P lecture 4, Libraries | Watch | 0.25 |
| B4 | CS50P problem set 4: Emojize, Adieu Adieu, Guessing Game, Little Professor [searched, secondary] | Attempt all four | 1.0 |
| B4 | Python tutorial chapters 6 (Modules) and 12 (Virtual Environments and Packages) | Read | 0.25 |
| B4 | PEP 8, naming conventions and code layout | Read | 0.25 |
| B4 | Missing Semester 2026 lectures 3 (Development Environment and Tools) and 6 (Packaging and Shipping Code); QuantEcon's lecture on writing good code [check title] | Stretch | 0 |
| B5 | CS50P lecture 8, Object-Oriented Programming | Watch | 0.5 |
| B5 | CS50P problem set 8: Seasons of Love, Cookie Jar [searched, secondary] | Attempt both | 1.0 |
| B5 | Python tutorial chapter 9, Classes (9.3 to 9.5); the `dataclasses` docs; mypy "Getting started" | Read | 0.25 |
| B5 | MIT 6.100L lectures on classes and inheritance [check numbers]; QuantEcon's two object-oriented programming lectures; Composing Programs 2.5 to 2.7 | Second explanation; stretch | 0 |
| A1 | McKinney 4.1, The NumPy ndarray [searched]; appendix A, ndarray internals and reshaping [check sections] | Read 4.1; the appendix after lesson 60 | 0.75 |
| A1 | NumPy docs, "the absolute basics for beginners" and "Copies and views" | Read | 0.25 |
| A1 | PDSH 2.1 to 2.3, 2.6 and 2.7 (data types, array basics, ufuncs, masks, fancy indexing) | Run every cell and change one input per cell | 0.5 |
| A1 | Rougier, the anatomy-of-an-array chapter [check number] | Stretch | 0 |
| A2 | McKinney 4.3 (universal functions), 4.4 (array-oriented programming) and 4.6 (linear algebra) [searched] | Read | 0.5 |
| A2 | NumPy docs, Broadcasting | Read in full; redo the examples | 0.25 |
| A2 | PDSH 2.4, 2.5 and 2.8 (aggregations, broadcasting, sorting) | Run every cell and change one input per cell | 0.5 |
| A2 | Missing Semester 2026 lecture 4 (the profiling half); 3Blue1Brown, Essence of Linear Algebra, the chapter on matrix multiplication | After lesson 68; preview of 1.4 after lesson 67 | 0 |
| A3 | McKinney 4.2 (pseudorandom number generation) and 4.7 (random walks) [searched] | Read | 0.25 |
| A3 | McKinney 4.7's random-walk example | Extend it to 1,000 walks and estimate a first-passage time with a standard error | 0.5 |
| A3 | MIT 6.0002 lecture 6, Monte Carlo Simulation [searched] | Watch | 0.5 |
| A3 | NumPy docs, Random Generator and parallel random number generation | Read | 0.25 |
| A3 | Stat 110 lecture 7, Gambler's Ruin and Random Variables [searched]; SciPy docs, the `stats` and `optimize` tutorials | Preview of 1.5 after lesson 72; reference for lesson 75 | 0 |
| A3 | Guttag, the chapters on random walks and Monte Carlo simulation [check numbers] (paid); Glasserman, chapter 1 and the antithetic-variates section of chapter 4 [check] (paid) | Stretch | 0 |
| D1 | McKinney chapter 5 (5.1 to 5.3) | Read in full; mark the two places pandas 3 differs (copy-on-write, the `str` dtype) | 0.75 |
| D1 | pandas docs: 10 minutes to pandas; Copy-on-Write | Read | 0.25 |
| D1 | PDSH 3.1 to 3.3 | Run every cell and change one input per cell | 0.5 |
| D1 | QuantEcon, the pandas lecture | Stretch | 0 |
| D2 | McKinney 6.1 and 7.1 to 7.5 [searched] | Read | 0.75 |
| D2 | pandas docs: Working with missing data; the `read_csv` reference | Read | 0.25 |
| D2 | PDSH 3.4 (missing values) and 3.10 (vectorised string operations) | Run every cell and change one input per cell | 0.5 |
| D3 | McKinney chapters 8 and 10 | Read | 0.75 |
| D3 | pandas docs: Merge, join, concatenate and compare (including `merge_asof`); Group by; Reshaping and pivot tables | Read | 0.25 |
| D3 | PDSH 3.5 to 3.9 | Run every cell and change one input per cell | 0.5 |
| D3 | QuantEcon, the pandas lecture on panel data [check title] | Stretch | 0 |
| D4 | McKinney chapter 11 (11.1 to 11.7) [searched] | Read in full; rewrite its `"M"` and `"Y"` frequencies as `"ME"` and `"YE"` | 0.75 |
| D4 | Bailey et al. 2014 | Read the first two sections after lesson 94 [check sections] | 0.25 |
| D4 | PDSH 3.11, working with time series [check section] | Run every cell, with pandas 3 aliases | 0.5 |
| D4 | pandas docs: Time series and date functionality; Windowing operations | Reference while working | 0 |
| D4 | Hull, the section on estimating volatility from historical data [check chapter for the 11th edition] (paid); Cont 2001, the list of stylised facts | Stretch: compare Hull's log-return estimator with lesson 97's simple returns | 0 |
| D5 | McKinney chapter 9 | Read | 0.5 |
| D5 | Matplotlib docs, Quick start guide (anatomy of a figure; the two interfaces) | Read | 0.25 |
| D5 | Wilke, the chapters on histograms and density plots and on proportional ink [check numbers] | Read both | 0.25 |
| D5 | PDSH chapter 4: simple line plots, histograms, multiple subplots | Run every cell and change one input per cell | 0.5 |
| D5 | Huff, chapter 5, "The Gee-Whiz Graph" (paid) | Stretch (10 minutes) | 0 |
| D6 | pandas docs: Scaling to large datasets | Read the first sections | 0.25 |
| D6 | McKinney chapter 13, data analysis examples | Work through one example | 0.5 |

Per level: Y1 2.0, Y2 1.5, Y3 1.75, Y4 2.0, Y5 1.75, B1 1.25, B2 1.25, B3 2.5, B4 1.75, B5 1.75, A1 1.5, A2 1.25, A3 1.5, D1 1.5, D2 1.5, D3 1.5, D4 1.5, D5 1.5, D6 0.75. Total 30.0 h.

### 5.2 Item 1.2 Tools

| Level | Resource and location | What to do | Hours |
|---|---|---|---|
| T1 | Missing Semester 2026 lecture 1, Course Overview + Introduction to the Shell [searched] | Watch; do its exercises | 0.75 |
| T1 | TLCL chapters 6 and 7 (redirection; seeing the world as the shell sees it) [check numbers] | Read | 0.25 |
| T1 | Software Carpentry, The Unix Shell: pipes and filters, loops, finding things | Work through the exercises | 0.5 |
| T1 | explainshell | Use on every unfamiliar command line | 0 |
| T2 | Missing Semester 2026 lecture 2, Command-line Environment [searched] | Watch | 0.5 |
| T2 | Missing Semester 2020 lecture 2, Shell Tools and Scripting (the scripting half; 2026 dropped it) | Watch | 0.25 |
| T2 | OverTheWire Bandit levels 6 to 10 (levels 0 to 5 are the Tools Lab) | Attempt | 0.5 |
| T2 | TLCL chapters 9 (permissions) and 11 (the environment) [check numbers]; ShellCheck | Second explanation; run ShellCheck on every script you write | 0 |
| T2 | Missing Semester 2020 lecture 3, Editors (Vim) | Stretch | 0 |
| T3 | Missing Semester 2026 lecture 5, Version Control and Git [searched] | Watch in full: it teaches Git's data model first, as this level does [check content] | 0.75 |
| T3 | Pro Git 1.3 (What is Git?), 2.1 to 2.4 (Git basics, undoing things) and 3.1 (branches in a nutshell) | Read | 0.5 |
| T3 | Learn Git Branching, the introduction sequence | Complete | 0.5 |
| T3 | Beams, "How to Write a Git Commit Message"; Pro Git 7.7, Reset Demystified | Read with lessons 11 and 13 | 0 |
| T4 | Pro Git 2.5 (remotes), 3.2 (merging), 3.5 (remote branches) and 3.6 (rebasing) | Read | 0.5 |
| T4 | Learn Git Branching, the ramping-up and remote sequences | Complete | 0.5 |
| T4 | GitHub Docs: GitHub flow; About pull requests; removing sensitive data [check title]; Pro Git 7.10, Debugging with Git | Reference for lessons 17 and 18 | 0 |
| T4 | SWE at Google, the code review chapter [check number] | Stretch | 0 |
| T5 | CS50P lecture 5, Unit Tests | Watch | 0.25 |
| T5 | pytest docs: Get started; assertions; fixtures; parametrize; `tmp_path`; `pytest.approx` | Read | 0.25 |
| T5 | CS50P problem set 5: Testing my twttr, Back to the Bank, Re-requesting a Vanity Plate, Refueling [Back to the Bank and Refueling searched, secondary; the other two check] | Attempt all four | 0.5 |
| T5 | MIT 6.102 reading on testing (partitioning and boundaries) [check]; Hypothesis quickstart; GitHub Docs, building and testing Python with GitHub Actions | Stretch; with lesson 24; before the exit | 0 |
| T5 | Okken, chapters 1 to 5 (paid); SWE at Google, the testing chapters [check numbers]; Missing Semester 2026 lecture 9, Code Quality | Stretch | 0 |
| T6 | SQLite docs, Datatypes In SQLite | Read sections 1 to 3 | 0.25 |
| T6 | SQLBolt lessons 1 to 12 [check titles] | Complete every exercise | 0.75 |
| T6 | CS50 SQL lecture 0 (querying) [check]; SQLZoo: SELECT basics, SUM and COUNT, JOIN, Using NULL [check tutorial names] | Second explanation; extra problems | 0 |
| T6 | CMU 15-445 lecture 2 (modern SQL) [check] | Stretch | 0 |
| T7 | SQLite docs, window functions | Read the opening sections; redo the examples | 0.25 |
| T7 | OWASP SQL Injection Prevention Cheat Sheet | Read the primary defences | 0.25 |
| T7 | SQLBolt lessons 13 to 18 and the subqueries topic [check titles] | Complete | 0.25 |
| T7 | Python `sqlite3` docs, the how-to on placeholders; Software Carpentry, Databases and SQL; Composing Programs 4.3, Declarative Programming [check] | Reference; second explanation; stretch | 0 |

Per level: T1 1.5, T2 1.25, T3 1.75, T4 1.0, T5 1.0, T6 1.0, T7 0.75. Total 8.25 h.

---

## 6. Verification approach

Every answer is machine-checked twice before it ships (CONTENT-FORMAT.md section 6): the declared answer, or the generator's answer, against an independent computation, and then the runtime grader is replayed on the correct answer, its accepted forms and every diagnosed wrong answer. Programming adds two rules that maths does not need. First, whatever the learner sees run must be what CI ran: authored code runs at build time and its output, trace, result set or figure ships as data (widgets-programming decision 1). Second, **CI runs it twice, on Pyodide 314.0.7 in Node (the same WebAssembly build both targets load) and on CPython 3.11 (the learner floor)**, and the two recordings must agree. Draft 2's own checks found three kinds of disagreement, which the build now looks for on every item:

| Difference [measured] | Where it bites | Rule |
|---|---|---|
| WebAssembly has no floating-point status flags: no NumPy divide, overflow or invalid warnings; `np.seterr(..., "raise")` raises nothing; `linalg.solve`, `inv` and `cholesky` return `nan` where CPython's NumPy raises `LinAlgError` | Lessons 57, 61, 66, 67; homework A2; every 1.4 drill that factorises a matrix | No item's answer may be a NumPy floating-point warning or a `LinAlgError` from a singular matrix. Reference solutions and hidden tests check `np.isfinite`, `matrix_rank` or the condition number explicitly; the lessons teach the difference as an edge case |
| Built-in `sum` of floats is compensated from Python 3.12 (Neumaier summation) | Lesson 66; the Y1 lab drill on summation | Rounding-error demonstrations use an explicit loop; any item showing `sum` of floats states the version |
| Messages and warnings differ: "float division by zero" (3.11) against "division by zero" (3.14); 3.14 warns on `return` inside `finally` and on `datetime.utcnow()` | Lessons 34, 35, 42; any predict-output item ending in an error | Predict-output items that end in an exception ask for the exception type, never the message; lessons that show a message show the in-app (3.14) text and say that older Pythons word it differently |

### 6.1 Item families in 1.1

| Family | Lessons | Independent check (CI) | Second check | Runtime grading and accepted forms |
|---|---|---|---|---|
| Predict the output (core Python) | Courses Y and B | Run the snippet on Pyodide 314.0.7 and on CPython 3.11; record standard output and any exception | The two recordings must match (the table above); each snippet also runs under three `PYTHONHASHSEED` values and must print the same thing, which rejects snippets whose output depends on the order of a set of strings or on `id` | `output` check with normalised whitespace; alternative spellings only where Python itself has them (none by default) |
| Traces and heap diagrams | 1, 5, 6, 12 to 24, 29, 30, 33 to 35, 49 | `trace-recorder` under `sys.settrace` on the pinned CPython | The trace's final output equals the predict-output recording; alias sets and object counts derived from the trace's heap equal the author's declared arrows | `mapping` check per arrow; a screen's object count as a numeric |
| Numbers, floats and rounding | 2 to 6, 63, 66 | `fractions.Fraction` and `decimal.Decimal` at 50 digits; `float.hex`, `math.ulp` and `struct.pack` for stored values | Float results recomputed with `math.fsum` and compared within one unit in the last place; every quoted decimal expansion (2.67499999999999982236431605997495353221893310546875) regenerated from `Decimal(float)` | Numeric exact, or with the tolerance the item states |
| Format specifications | 9 | `format(value, spec)` on both runtimes for every target string | The `format-produces` predicate run in CI against Python's output for every case and every accepted spec | Entry graded by behaviour: any spec that produces all target strings |
| Slices, paths and shapes typed by the learner | 7, 39, 58, 59, 61, 78 | Evaluate the expression on the item's object in Python | The same expression through the JavaScript slicer or `nd-core` must select the same cells | `selection-equals`, so `s[-15:-9]` and `s[4:10]` are both accepted where they select the same characters |
| Regular expressions and globs | 43; 1.2 lessons 4 and 18 | Python's `re` (and `fnmatch` for globs) on the positive and negative sets | The runtime engine is JavaScript's: CI runs every authored and model pattern through both and rejects items whose sets differ; features that differ between the two (lookbehind of variable width, `\Z`, possessive quantifiers) are banned from items | `matches-sets` on hidden positives and negatives as well as the visible ones |
| Dates and time zones | 42, 92, homework B3 | `zoneinfo` with the `tzdata` package pinned to Pyodide's (2025.3), on both runtimes, never the system's zone files | The widget's time-zone data must give the same offset at every instant an item uses; CI fails if the two `tzdata` versions differ | Text or numeric |
| Code drills | Every `code` screen and drill | The reference passes every test on both runtimes, with its declared `needs` and nothing more | Every `wrong/` solution fails the test it names; every kept `mutant-forge` mutant of the reference fails at least one hidden test | `code` check; partial marks in homework and exams by tests passed |
| Efficiency tests | 28, 64, homework Y3 and Y5 | Line budget and time ratio as widgets-programming 2.2.1 | A planted quadratic solution must fail and the reference pass in 50 of 50 runs on the reference device | Pass or fail, with the estimated exponent in words |
| NumPy semantics in widgets | Course A | `nd-core` against NumPy on generated cases per operation family (shapes, strides, slicing, broadcasting, masks, reductions, `int64` wraparound) | Dtypes and shapes compared as well as values | Shape entries, numeric, selection |
| pandas semantics in widgets | Course D | `frame-core` against the pinned pandas 3.0.2 on generated frames | `assert_frame_equal`: index, dtypes and missing-value positions compared, not only values; CPython's pandas 3.0.6 must agree | Result table, `frame-equal` |
| Simulation | 69 to 75, homework A3 | Exact values from closed forms or SciPy: $\frac{5}{36}$, the gambler's-ruin formula, $S_0 e^{\sigma^2/2}$, the stated call formula (7.9656), `norm.sf(2)` | The reference simulation lands within 4 standard errors of the exact value for 20 seeds; any item quoting a seeded number records it from Python (NumPy's `default_rng` gives the same stream on both runtimes [verified for seed 42]), and the widget's JavaScript generator never claims to reproduce it | Numeric with a tolerance stated in standard errors, or exact where the item asks for the formula's value |
| Figures | 99 to 102, 107, homework D5 | matplotlib introspection (`FigureAssert`) on the reference on the Agg backend, on CPython and on Pyodide's matplotlib 3.10.8 (not yet run there: open item 2) | A deliberately wrong figure (no log scale, unshared axes, a missing label) must fail each assertion it breaks | Figure check |
| Money and allocation | Homework Y1 | Exact integer arithmetic | Brute force over all small totals and weights | Code tests |
| Long-form items | Homework and exams | Numeric claims in the model answer evaluated as arithmetic; code in the model answer run | Rubric anchoring: every rubric point names model-answer lines and every line is used | Self-marked against the rubric with Bertie's per-point suggestion |

### 6.2 Item families in 1.2

| Family | Lessons | Independent check (CI) | Second check | Runtime grading and accepted forms |
|---|---|---|---|---|
| Shell state and output | 1 to 8 | Every authored command sequence and model answer run in real bash in a container holding the same initial files | `shell-interpreter`'s files, modes, standard output, standard error and exit status must equal bash's; a command outside the supported subset fails the build | `predicate` on state (`fs-matches`, `output-contains`, `mode-equals`), so any command line that reaches the target state is accepted |
| Pipelines graded on output | 3, homework T1 | The model pipeline's output in bash | Two independent model pipelines (for example `sort \| uniq -c` and an `awk` count) must agree on the seeded file | Output compared after normalising leading spaces |
| Git graphs and states | 9 to 18 | Each command script replayed with real Git in a temporary repository with fixed author, committer and dates | `git-model`'s graph, refs, index and file contents compared with Git's; hashes compared only where the model encodes objects exactly as Git does, otherwise `graph-matches` with `ignoreHashes` | `predicate` with `graph-matches`, `head-at`, `branch-contains` |
| Status and diff predictions | 10, homework T3 | Real `git status --short` and `git diff --stat` | `git-model`'s rendering of the same state | Text, lines compared as a set where Git's order is not part of the lesson |
| SQL | 25 to 32 | SQLite through Python's `sqlite3` on Pyodide (3.39.0) and in the SQL worker's build (3.53.4) | The same question answered in pandas on the same data gives the same rows | `resultset`, ordered only when `ORDER BY` is part of the task; floats within $10^{-9}$ |
| Tests written by the learner | 19 to 24 | The model test file passes on the reference under real pytest | Each kept mutant has a distinguishing input found by a seeded fuzzer; equivalent mutants are discarded, as the `len(returns) < 1` mutant of homework T5 is | `learner-tests`: pass on the reference, kill every mutant |
| Properties | 24, homework T5 | The model properties pass on the reference under Hypothesis with a fixed seed | A planted bug (peak reset to the overall maximum) must be found and shrunk to a two-element list | Property tests as learner tests |
| Injection | 32 | `sqlite3` runs the string-built query with the learner's input and must return rows beyond the target's | The parameterised version returns none for the same input | `input-escapes-literal` |
| Permissions | 5 | `chmod` then `stat -c %a` in the container | `permission-bits` model on the same operations | Entry or numeric |
| Bisect counts | 18 | $\lceil \log_2 n \rceil$ | `git bisect run` on a generated linear history, counting steps | Numeric |
| Paste-verify (local tasks and exits) | Homework, both exits | Parsers tested on recorded real output from Linux, macOS and Windows (Git Bash and PowerShell) terminals | Redaction of home paths tested on the same recordings | `setup-checklist` checks per item |

### 6.3 Code drills, generators and long-form items

- **Code drills.** Each drill ships `drill.yaml` (with `needs`), `reference.py`, `starter.py`, `tests.py` (`zqtest`) and a `wrong/` folder, each wrong file naming its misconception and the test it must fail: for example `max_drawdown` as maximum minus minimum, `rolling_mean` with the check inside the generator, `allocate` with float rounding, `strategy_returns` with the same-row signal, `winsorise` with `np.quantile` instead of `np.nanquantile`. CI runs every reference and every wrong file on both runtimes (CONTENT-FORMAT.md 6.11). Shell, SQL and pytest drills follow the same layout with their own runners.
- **Generators.** Each family above is a TypeScript generator with a Python verifier written from its specification without reading the TypeScript; CI enumerates the parameter box and requires agreement on admissibility, difficulty, answer and every misconception value (CONTENT-FORMAT.md 5.6). Predict-output families draw from CI-recorded seed banks (200 seeds per family and difficulty), so either target grades them without starting Python.
- **Long-form items.** Never auto-passed or auto-failed. CI checks the model answer's code and arithmetic and the rubric's anchoring; the learner marks their own answer with Bertie's per-point suggestion and quoted evidence beside it.

---

## 7. Sample lesson in full: Names and objects

**Why this lesson.** It is the root of 1.1's dependency graph. Aliasing (lessons 22 and 23), the mutable default (17), closures (20), copies of nested data (23), `+=` on tuples (24), class attributes (49), NumPy views (60) and pandas copy-on-write (81) are all one idea: a name refers to an object, and assignment never copies. It is the first Stage 1 lesson the depth-first build ships, so it doubles as the first content for the programming widgets (`code-tracer`, `node-link`, `predict-output`). It is written at the level of detail an author hands to the YAML stage (CONTENT-FORMAT.md sections 3.7, 3.10 and 10): every screen, widget configuration in plain words, check, accepted forms, diagnosis, hint ladder, Why?, Show solution text and tutor fields. Copy follows design research 9.2: second person, sentences of at most 20 words, no exclamation marks, a term named only after it has been used. Every output below was recorded on CPython 3.11.15 and Pyodide 314.0.7 (Python 3.14.2) and agreed [verified].

**What it inherits from 0.4.** 0.4 lesson 24 taught `a = 1`, `b = a`, `a = 2` leaving `b` at 1, with a box for each variable. That picture predicts ints correctly and lists wrongly. This lesson keeps 0.4's result and replaces its reason.

**Rules that apply to every screen here.**

- **Hints** open after the lesson's first Check, anywhere in the lesson (design research 5.5; AI-TUTOR.md 2.2), and climb Nudge, Point, Step. Show solution appears after two not-yet results on a screen (design research 5.4).
- **Element references** use `<widget id>/<kind>:<name>` (CONTENT-FORMAT.md decision 17). The code panel's lines are `code/line:1` to `code/line:N`; in the heap panel each object is `heap/node:o1`, `heap/node:o2` in creation order, each name tag is `heap/name:<name>`, and each arrow is `heap/edge:<name>`. Two-program screens use `codeA` and `codeB`. These kinds follow `node-link`'s heap layout and `code-tracer`'s `targets(config)`; the compiler checks every one.
- **Bertie's face** follows the lesson player (BERTIE.md 5.3): `correct` or `notyet` on grading, `surprised` on the trap reveal (screen 8), `celebrate` when the lesson completes. During a problem only the quiet states play.
- **Tutor fields** carry no value that a screen's check accepts (CONTENT-FORMAT.md 3.10, the leak lint). Where the accepted answer is a printed list, the notes describe it in words ("the list with the late print added").
- **Runtime.** `needs: []`. No screen runs live code: every program is authored, and its trace and output are recorded in CI on both runtimes, so the lesson runs identically on both targets with Python never loaded.

### 7.1 Lesson header

| Field | Value |
|---|---|
| `id`, `rev`, `status` | `lsn.pythink.names-objects`, 1, `draft` |
| `title` | Names and objects |
| Position | Course Y (Thinking in Python), level Y1, lesson 1 of 6; 1.1 lesson 1 |
| `summaryLine` | A name is a label on an object; assignment moves labels and never copies objects. |
| `frame.why` | Programs share data. A risk check, a pricer and a report may all use one list of positions. Python lets many names refer to one object so that sharing costs nothing; the price is that a change made through one name is seen through all of them. |
| `frame.before` | 0.4 lesson 24 taught `x = 5` as "put 5 in the box called x". That picture works for numbers and fails for lists; this lesson replaces it. |
| `insight` | `b = a` puts a second label on the same object. Changing the object shows through every label; building a new object moves only one label. |
| `introduces` | `skl.py.name-binding`, `skl.py.alias-mutation`, `skl.py.rebind-vs-mutate`, `skl.py.identity-equality` |
| `uses`, `requires` | `skl.comp.variables` (0.4 lesson 24), `skl.comp.functions` (0.4 lesson 29) |
| `terms` | `gls.py.name`, `gls.py.object`, `gls.py.binding`, `gls.py.alias`, `gls.py.identity`, `gls.py.mutable`, `gls.py.immutable` |
| Embargoed terms | "reference" and "pointer" (never used: arrows carry the idea), "shallow copy" and "deep copy" (lesson 23), "dunder" and `__iadd__` (lesson 50), "pass by reference" and "pass by value" (never used: both mislead in Python) |
| Common trap | Assignment copies, and so does passing an argument (screen `stress`, then the summary's trap line) |
| `edgeCases` | A list written out afresh is a new object, so `is` is `False` although `==` is `True` (`labels`); an int cannot change, so `a = a + 1` builds a new object and sharing ints is harmless (`ints`); `+=` changes a list in place but builds a new int (`plus-equals`, `why-iadd`); a copy made with `list(base)` is a new outer list whose items are the same objects (`book-copy`) |
| `workedExample` | `at: plus-equals`. Naive: "`x += [3]` is shorthand for `x = x + [3]`, so both programs print `[1, 2]`." Decision: "Ask whether the operation changes the existing object or builds a new one." |
| `est` | 13 minutes: 12 screens (605 seconds, about 10 minutes) and a 4-item quiz (about 3 minutes); the hours budget still counts 15, decision 1's upper end |
| `needs` | `[]` |
| `sources` | `src.batchelder-names` (`parallel-reading`); `src.python-docs` (`parallel-reading`: Language Reference 3.1 "Objects, values and types", 4.2 "Naming and binding", 7.2.1 "Augmented assignment statements" [7.2.1 searched; 3.1 and 4.2 check]); `src.composing-programs` (`further`, 2.4 Mutable Data); `src.python-tutor` (`parallel-reading`: its arrow diagrams); `src.sorva-2013` † (`further`: Juha Sorva, "Notional Machines and Introductory Programming Education", ACM Transactions on Computing Education 13, article 8, 2013 [searched], on novices' models of variables) |
| `art` | `ast.course-art.names-objects`: Bertie holding two luggage tags tied by strings to one suitcase |

**Misconceptions this lesson diagnoses** (new library entries, `mc.py.*`):

| Id | `belief`, as a learner would put it | `correction` |
|---|---|---|
| `mc.py.assign-copies` | "`backup = prices` makes a copy of the list." | Assignment binds a second name to the same object; nothing is copied. |
| `mc.py.rebind-moves-alias` | "Reassigning `prices` drags `backup` along with it." | Rebinding moves one label; other labels stay on the old object. |
| `mc.py.alias-overgeneralised` | "`b = a` shares, so `a = a + 1` moves `b` too." | `a + 1` builds a new object and only `a` moves to it. |
| `mc.py.int-changed-in-place` | "`a = a + 1` changes the 5 into a 6." | An int cannot change; `a + 1` builds a new int, and the 5 is still there for `b`. |
| `mc.py.augmented-is-rebinding` | "`x += y` always means `x = x + y`." | For a list, `+=` extends the existing object in place. |
| `mc.py.plus-mutates` | "`x = x + [3]` changes the list `y` also refers to." | `x + [3]` builds a new list; only `x` moves to it. |
| `mc.py.call-copies` | "A function gets its own copy of the list I pass in." | The parameter is one more name for the caller's object. |
| `mc.py.local-means-private` | "The name is local, so the object is private to the function." | A local name can refer to a shared object. |
| `mc.py.is-means-equal` | "`is` and `==` mean the same thing." | `==` compares values; `is` asks whether two names share one object. |
| `mc.py.literal-same-object` | "Writing the same list twice gives the same object." | Each list display builds a new object when it runs. |
| `mc.py.wrap-copies` | "`[base]` is a copy of `base`." | It is a new one-item list whose item is the old list. |

**Screen map.**

| # | Id | Type | Task | Difficulty | Widgets | Est. |
|---|---|---|---|---|---|---|
| 1 | `title` | `title` | none | none | art only | 15 s |
| 2 | `predict` | `problem` (the hook) | predict `print(backup)` | 1 | `code` (`code-tracer`, predict), `choice` | 50 s |
| 3 | `arrows` | `problem` (manipulate) | draw each name's arrow | 1 | `code`, `heap` (`node-link`, draw mode, the graded widget) | 70 s |
| 4 | `labels` | `problem` (names the idea) | which comparisons are `True` | 1 | `heap`, `choice` (many) | 55 s |
| 5 | `rebind` | `ladder` | rebinding one name | 2 | `code` (predict), `predict-output` | 45 s |
| 6 | `ints` | `ladder` | the objects behind 0.4's result | 2 | `code` (objects for everything), `heap` (draw), `choice`; two parts | 60 s |
| 7 | `plus-equals` | `ladder` (the worked example) | two programs, one character apart | 3 | `codeA`, `codeB`, `predict-output` (two parts) | 75 s |
| 8 | `stress` | `trap` | a function changes its argument | 2 | `code` (frames), `choice` | 50 s |
| 9 | `rule` | `generalise` | apply both rules in order | 2 | `heap` (after Check only), `predict-output` | 50 s |
| 10 | `why-iadd` | `derive` | order Python's steps for `x += [3]` | 3 | `derivation-steps` (order) | 60 s |
| 11 | `book-copy` | `problem`, `context: quant` (the transfer) | make a real copy of a position book | 2 | `choice` (many), `heap` | 55 s |
| 12 | `summary` | `summary` | none | none | none | 20 s |

Two non-task screens (title and summary), the limit of design research 5.8. Screen estimates total 605 seconds; the quiz adds about 3 minutes.

### 7.2 Screens

#### Screen 1: `title`

- **Prose:** "Two spreadsheets can show the same numbers. One may be a copy; the other may be the same file, open twice. Python makes the same distinction."
- **Art:** `ast.course-art.names-objects`.
- **Bertie:** `idle`. Chat is open with no answer key, as on an explore screen (AI-TUTOR.md 2.2); hints do not exist yet.

#### Screen 2: `predict` (`problem`, the hook, difficulty 1)

- **Skills:** `skl.py.alias-mutation`.
- **Prose:** "A risk script keeps a backup of today's prices, then adds a late print."
- **Canvas:** `code`, a `code-tracer` in predict mode showing the program below. Step is locked until Check, and the heap panel is hidden, so the learner commits to a prediction first. On Check the panel opens and the recorded trace plays.

```python
prices = [100, 101, 102]
backup = prices
prices.append(99)
print(backup)
```

- **Question:** "What does line 4 print?"
- **Input:** `choice`, three cards: a `[100, 101, 102]`; b `[100, 101, 102, 99]`; c "An error". **Check:** `choice`, correct b.
- **Diagnose:**

| Option | Misconception | Feedback line | Show-why |
|---|---|---|---|
| a | `mc.py.assign-copies` | "That would be right if line 2 copied the list. It did not: `backup` and `prices` name one list." | Play lines 1 to 4 with the heap open: at line 2 a second arrow lands on the existing list; at line 3 the list grows under both arrows |
| c | `slip` | "Nothing here raises. `append` is a list method, and `backup` got its value on line 2." | Play the trace |

- **Reason (verdict chip):** "Line 2 gave the list a second name, so line 3's append shows through `backup`."
- **Hints:** Nudge: "How many lists does this code build? Look for the square brackets that make one." Point: "Line 2 has no square brackets. Does it build anything?" (highlights `code/line:2`). Step: "Only line 1 builds a list. Line 2 makes `backup` name that same list, so line 3 changes the list both names refer to."
- **Why?** Yours: "You saw that line 2 builds no new list." Shown: "Line 2 builds no new list; it gives the existing one a second name." Then: "So the append on line 3 changes the one list, and both names show it." `rep`: picture.
- **Solution (Show solution):** the heap opens and the trace plays to the end; text: "One list, two names. The append changes that list, so `backup` shows the late print too."
- **Tutor:** focus: "How many objects the code builds, not a rule." Notes: "Most adults choose the unchanged list, because spreadsheets and 0.4's box picture copy values; treat it as the expected answer, not a failure." Reps: picture (arrows); counting objects. Avoid: "alias", "mutable", "reference".

#### Screen 3: `arrows` (`problem`, manipulation, difficulty 1)

- **Skills:** `skl.py.name-binding`.
- **Prose:** "Python keeps names and objects apart. Step through the code. After the last line, draw every name's arrow to the object it names."
- **Canvas:** `code`, the same program in a `code-tracer` with Step unlocked; `heap`, a `node-link` in heap layout and draw mode, the graded widget (`answer: heap`). Names sit in a frame panel on the left as tags; objects appear on the right as boxes when the recorded trace creates them. Line 1 creates the list `heap/node:o1` (a box of three cells); line 2 creates nothing; line 3 adds a fourth cell. Beside the heap sits a faded "copy?" box, `heap/node:ghost`, holding `[100, 101, 102]`, which a learner can attach an arrow to. Drawing: drag from a tag to a box, or tap the tag and then the box; keyboard: focus the tag, Enter, arrow keys to choose, Enter.
- **Question:** "Step to the end, then draw both arrows."
- **Check:** `mapping`: `name:prices → node:o1`, `name:backup → node:o1`.
- **Diagnose:**

| Learner state | Misconception | Feedback line | Show-why |
|---|---|---|---|
| `backup` on the faded copy | `mc.py.assign-copies` | "No line built a second list, so this copy does not exist. Line 2 points `backup` at the list `prices` already names." | The copy box fades out; the arrow slides to `heap/node:o1` |
| `backup` with no arrow | `slip` | "Every name names exactly one object. Which object did line 2 give to `backup`?" | Pulse `code/line:2` |

- **Otherwise:** "Each name needs one arrow. Step again and watch which boxes appear."
- **Reason:** "One list, two names: both arrows end on the same box."
- **Hints:** Nudge: "How many list boxes did stepping create?" Point: "This is the only list in memory." (highlights `heap/node:o1`). Step: "Line 1 built the list and pointed `prices` at it. Line 2 pointed `backup` at the same list. Draw both arrows to it."
- **Why?** Yours: "You drew both arrows to the one list." Shown: "Both arrows end on the one list." Then: "Names live in one place and objects in another. An assignment draws an arrow; it never duplicates a box." `rep`: picture.
- **Solution:** both arrows animate onto `heap/node:o1`; text: "Only line 1 built a list, so both names must point at it."
- **After a correct answer or a reveal:** the faded copy box disappears. Concreteness fades from here: on screens 5, 7 and 9 the heap is shown only after Check.
- **Tutor:** focus: "Assignment draws an arrow." Notes: "Learners who know Python Tutor will recognise the picture; let them use its vocabulary of frames and objects." Reps: picture. Avoid: memory addresses, `id()` numbers.

#### Screen 4: `labels` (`problem`, naming the idea, difficulty 1)

- **Skills:** `skl.py.identity-equality`.
- **Prose:** "You drew Python's model. A **name** is a label. An **object** is the value itself, with a type and an identity. `name = expression` works out the expression's object, then **binds** the name to it. Two names bound to one object are **aliases**. `==` asks whether two values are equal; `is` asks whether two names are bound to the same object."
- **Canvas:** `heap`, `from: arrows/heap`, display only. Tapping an option draws, beside the heap, any new object that option's expression would build.
- **Question:** "After the three lines, which are `True`? Select all that apply."
- **Input:** `choice`, `select: many`: a `prices == backup`; b `prices is backup`; c `backup == [100, 101, 102, 99]`; d `backup is [100, 101, 102, 99]`. **Check:** correct a, b and c.
- **Diagnose:**

| Learner state | Misconception | Feedback line | Show-why |
|---|---|---|---|
| d selected | `mc.py.literal-same-object` | "The list written on the right is built fresh when the comparison runs. It equals `backup` but is a different object." | A new box with equal contents appears beside `heap/node:o1`, with its own outline |
| b not selected | `mc.py.is-means-equal` | "Both arrows end on one box, so `prices is backup` is `True`." | Pulse `heap/edge:prices` and `heap/edge:backup` |
| c not selected | `slip` | "`backup` holds 100, 101, 102 and 99 in that order, so `==` is `True`." | Highlight the four cells of `heap/node:o1` |

- **Otherwise:** "For each option, ask: same values, or same box?"
- **Reason:** "a and b: one object, two names. c: equal values. d: a fresh list is a different object."
- **Hints:** Nudge: "For each option, ask: same values, or same box?" Point: "Option d builds a list when it runs. Is that the box the arrows point at?" (highlights option d). Step: "`==` compares contents, so a and c are `True`. `is` compares boxes: a and b share one box; d's list is a new box."
- **Why?** Shown: "a, b and c are `True`; d is `False`." Then: "Use `==` to compare values. Use `is` almost only to test for `None`, as in `if result is None:`. Whether two equal numbers share a box is a detail of the interpreter, and Python warns if you write `x is 1000`." `rep`: picture.
- **Solution:** options a, b and c tick in turn, with d's fresh box drawn beside the heap; text: "Same values for a and c; the same box for a and b; a new box for d."
- **Tutor:** focus: "`==` against `is`." Notes: "If asked about `id()`, say it returns a number unique to the object while the object exists; no addresses." Reps: picture; analogy (two copies of a report against one report with two readers). Avoid: the small-integer cache unless the learner raises it.

#### Screen 5: `rebind` (`ladder`, difficulty 2)

- **Skills:** `skl.py.rebind-vs-mutate`.
- **Constraint:** the name moves; the object does not change.
- **Prose:** "Now line 3 builds a new list instead of changing the old one."
- **Canvas:** `code`, a `code-tracer` in predict mode. The heap shows the state after line 2 (both arrows on one list); Step is locked until Check.

```python
prices = [100, 101, 102]
backup = prices
prices = [1, 2, 3]
print(backup)
```

- **Question:** "What does line 4 print?"
- **Input:** `predict-output`. **Check:** `output`, normalised whitespace, correct `[100, 101, 102]`.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| `[1, 2, 3]` | `mc.py.rebind-moves-alias` | "Line 3 builds a new list and moves only the `prices` arrow to it. `backup` still names the old list." | Play line 3: a new box appears and only `heap/edge:prices` swings to it |

- **Otherwise:** "Run line 3 in your head: it builds a list, then moves one arrow."
- **Reason:** "Line 3 moved the `prices` arrow to a new list; `backup` was not touched."
- **Hints:** Nudge: "Does line 3 change the old list, or build a new one?" Point: "The square brackets on line 3 build a list. Whose arrow moves to it?" (highlights `code/line:3`). Step: "Line 3 builds a new three-item list and binds `prices` to it. `backup` still names the original prices."
- **Why?** Yours: "You moved only the `prices` arrow." Shown: "Only the `prices` arrow moves." Then: "An assignment moves the arrow of the name on its left, and no other." `rep`: picture.
- **Solution:** the trace plays line 3; text: "A new list for `prices`; `backup` keeps the old one."
- **Tutor:** focus: "Rebinding against changing." Notes: "A learner who answers correctly here may still hold the box model; screen 6 tests it." Reps: picture. Avoid: "mutable" (introduced on the next screen).

#### Screen 6: `ints` (`ladder`, difficulty 2)

- **Skills:** `skl.py.rebind-vs-mutate`.
- **Constraint:** an object that cannot change.
- **Prose:** "0.4 lesson 24 showed that `b` keeps its value here, and the box picture predicted it. Now draw the objects and find out why."
- **Canvas:** `code`, a `code-tracer` with "objects for everything" on and Step unlocked, so 5 and 6 appear as boxes (`heap/node:o1` for 5, `heap/node:o2` for 6, created on line 3); `heap`, a `node-link` in draw mode. A faded box `heap/node:ghost` reads "5, overwritten as 6".

```python
a = 5
b = a
a = a + 1
print(b)
```

- **Question:** two parts. Part 1: "Step to the end and draw both arrows." Part 2: "Did line 3 change any object?"
- **Input:** part 1, `heap` (mapping); part 2, `choice`: a "Yes: the 5 became a 6"; b "No: it built a new object, 6, and moved `a`"; c "Yes: it changed both names". **Check:** `parts`. Part 1 `mapping`: `name:a → node:o2`, `name:b → node:o1`. Part 2 correct b. A correct part locks (design research 5.4).
- **Diagnose:**

| Learner state | Misconception | Feedback line | Show-why |
|---|---|---|---|
| Part 1: both arrows on `node:o2` | `mc.py.alias-overgeneralised` | "Line 3 moves only `a`. `b` was bound on line 2 and nothing has moved it since." | Play line 3: the 6 box appears and only `heap/edge:a` swings to it |
| Part 1: an arrow on the ghost box | `mc.py.int-changed-in-place` | "No line edits the 5. `a + 1` builds a new int, 6, and line 3 binds `a` to it." | The ghost fades; the 5 box stays, still under `b` |
| Part 2: a | `mc.py.int-changed-in-place` | "The 5 is still there: `b` names it. A new object, 6, appeared on line 3." | Pulse `heap/node:o1` and `heap/node:o2` |
| Part 2: c | `mc.py.alias-overgeneralised` | "Only the name on the left of `=` moves." | Pulse `heap/edge:a` |

- **Otherwise:** "Two boxes exist after line 3. Which name labels which?"
- **Reason:** "Line 3 built a new int and moved `a`; `b` still names the 5, which never changed."
- **Hints:** Nudge: "How many int boxes are there after line 3?" Point: "This box appeared on line 3. Which name moved to it?" (highlights `heap/node:o2`). Step: "`a + 1` built a new int, 6. Line 3 bound `a` to it. `b` still names the 5, and no object changed."
- **Why?** Shown: "`a` names the new 6; `b` still names the 5." Then: "Ints, floats, strings and tuples are **immutable**: no operation changes them, so sharing them is always safe. Lists, dicts and sets are **mutable**, which is why sharing them matters, and why the box picture worked for 0.4's numbers." `rep`: picture.
- **Solution:** the arrows animate to their boxes and part 2 selects b; text: "Two objects, each with one name. The 5 was never touched."
- **Tutor:** focus: "Immutability is why the box picture seemed to work for numbers." Notes: "A learner who still holds the box model often draws an arrow on the ghost; ask what line 3's right-hand side builds before the name moves." Reps: picture; analogy (a price ticket replaced, not rewritten). Avoid: the small-integer cache.

#### Screen 7: `plus-equals` (`ladder`, the worked example, difficulty 3)

- **Skills:** `skl.py.rebind-vs-mutate`, `skl.py.alias-mutation`.
- **Constraint:** the same-looking update, written two ways.
- **Prose:** "These two programs differ by one character. Predict both outputs before stepping."
- **Canvas:** `codeA` and `codeB`, two `code-tracer`s side by side (stacked below 768 px), each in predict mode.

  Program A:

```python
x = [1, 2]
y = x
x = x + [3]
print(y)
```

  Program B:

```python
x = [1, 2]
y = x
x += [3]
print(y)
```

- **Question:** "What does each program print?"
- **Input:** `predict-output`, two parts, each graded on its own (a correct part locks). **Check:** `parts`: A `[1, 2]`; B `[1, 2, 3]`.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| B `[1, 2]` | `mc.py.augmented-is-rebinding` | "For a list, `+=` asks the list to extend itself, so the one list both names share grows." | Play program B: the list gains a cell and both arrows stay put |
| A `[1, 2, 3]` | `mc.py.plus-mutates` | "`x + [3]` builds a new list. Only `x` moves to it; `y` keeps the old one." | Play program A: a new box appears and only `x` moves |

- **Otherwise:** "For each program, decide whether line 3 builds a list or changes one."
- **Worked example record:** naive: "`x += [3]` is shorthand for `x = x + [3]`, so both print `[1, 2]`." Decision: "Ask whether the operation changes the existing object or builds a new one. `+` builds; a list's `+=` changes it in place."
- **Reason:** "Program A built a new list for `x`; program B extended the shared list."
- **Hints:** Nudge: "In each program, is a new list built, or is the existing list changed?" Point: "Compare line 3 of the two programs." (highlights `codeA/line:3` and `codeB/line:3`). Step: "In A, `x + [3]` builds a new list and only `x` moves, so `y` keeps the two-item list. In B, `+=` extends the list `y` also names, so `y` shows three items."
- **Why?** Yours: "You separated building from changing." Shown: "A builds a new list; B changes the shared one." Then: "`x += y` first asks the object to update itself. A list can, so it does; an int cannot, so for ints `+=` builds a new object, as on screen 6." `rep`: picture.
- **Solution:** both traces play side by side; text: "A: new list, `y` unchanged. B: same list, extended, so `y` sees it."
- **Tutor:** focus: "Building against changing." Notes: "The hardest screen of the lesson; for a stuck learner, offer a third program using `x.extend([3])`, which behaves like B." Reps: picture; code (the `extend` variant). Avoid: `__iadd__` (screen 10 shows the mechanism without the name).

#### Screen 8: `stress` (`trap`, difficulty 2)

- **Skills:** `skl.py.alias-mutation`.
- **Trap:** `{ mc: mc.py.call-copies, bait: a }`.
- **Prose:** "A stress test zeroes the first position. Most people get this wrong the first time."
- **Canvas:** `code`, a `code-tracer` with the frame panel (module frame and call frame); before Check it shows code only.

```python
def stress(book):
    book[0] = 0
    return book

base = [100, 50]
shocked = stress(base)
print(base)
```

- **Question:** "What does the last line print?"
- **Input:** `choice`: a `[100, 50]`; b `[0, 50]`; c "An error, because `book` is local to the function". **Check:** correct b.
- **Diagnose:**

| Option | Misconception | Feedback line | Show-why |
|---|---|---|---|
| a | `mc.py.call-copies` | "Calling the function binds the parameter `book` to the caller's list, exactly like `book = base`. Line 2 changes that one list." | Play the call: two frames appear, `base` in one and `book` in the other, both arrows on one list; line 2 zeroes its first cell |
| c | `mc.py.local-means-private` | "The name `book` is local, but the object it names is the caller's list. A local name can name a shared object." | Same |

- **On reveal:** the lesson player plays Bertie's `surprised` one-shot (BERTIE.md 5.3).
- **Reason:** "`book` and `base` name one list, so `book[0] = 0` changes `base`."
- **Hints:** Nudge: "When `stress(base)` runs, what does `book` name?" Point: "The call does what this line would do: `book = base`." (highlights `code/line:6`). Step: "The call binds `book` to the list `base` names. `book[0] = 0` changes that list, so `print(base)` shows the zeroed book; `shocked` is a third name for it."
- **Why?** Shown: "`base`, `book` and `shocked` all name one list." Then: "Passing an argument is an assignment to the parameter. A function that changes a list it receives changes the caller's list, so build a new list inside it when that is not what you want." `rep`: picture.
- **Solution:** the call plays with both frames; text: "Three names, one list. The stress test changed the base case."
- **Recording:** a wrong first try on a trap is expected; a revealed trap screen is recorded but does not enter the Redo queue (ASSESSMENT.md 2.2).
- **Tutor:** focus: "Parameter binding is assignment." Notes: "In risk code this exact bug corrupts the base case of a scenario run; say so only if the learner asks why it matters." Reps: picture (two frames); analogy (handing a colleague the original file, not a photocopy). Avoid: "pass by reference" and "pass by value"; the accurate phrase "pass by assignment" may be used if the learner asks.

#### Screen 9: `rule` (`generalise`, difficulty 2)

- **Skills:** `skl.py.rebind-vs-mutate`.
- **Rule (prose):** "You saw three things. Assignment, including passing an argument, binds a name to an object and never copies. A change made to an object shows through every name bound to it. Building a new object and assigning it moves one name only."
- **Card on the screen:**

| Changes the object (every alias sees it) | Builds a new object (one name moves) |
|---|---|
| `xs.append(v)`, `xs[i] = v`, `xs += ys` on a list, `d[k] = v` | `xs = xs + ys`, `xs = sorted(xs)`, `a = a + 1`, `s = s.upper()` |

- **Canvas:** `code` (predict mode); `heap`, which appears only after Check (concreteness fading).

```python
a = [1, 2]
b = a
b.append(3)
b = [9]
print(a)
```

- **Question:** "What does line 5 print?"
- **Input:** `predict-output`. **Check:** `output`, correct `[1, 2, 3]`.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| `[9]` | `mc.py.rebind-moves-alias` | "Line 4 moves only `b`. `a` still names the list that line 3 changed." | Play lines 3 and 4 |
| `[1, 2]` | `mc.py.assign-copies` | "Line 2 made `b` a second name for `a`'s list, so line 3's append changed it." | Play lines 2 and 3 |

- **Otherwise:** "Sort each line into 'changes an object' or 'moves a name', then run them in order."
- **Reason:** "Line 3 changed the shared list; line 4 moved only `b`."
- **Hints:** Nudge: "Sort each line into 'changes an object' or 'moves a name'." Point: "Line 3 changes; line 4 moves. Which one affects `a`?" (highlights `code/line:3` and `code/line:4`). Step: "After line 3 the shared list has three items. Line 4 moves `b` to a new one-item list. `a` still names the three-item list."
- **Why?** Yours: "You applied both rules in order." Shown: "Line 3 changed the shared list and line 4 moved `b` alone." Then: "Every surprise in this lesson came from one question: does this line change an object, or move a name?" `rep`: picture.
- **Solution:** the heap appears and the trace plays lines 2 to 5; text: "Change, then move: `a` keeps the changed list."
- **Tutor:** focus: "The rule describes what the learner has already done four times." Notes: "If the learner recites the card without the picture, ask them to draw line 4's arrow." Reps: picture; the card's two columns. Avoid: "reference".

#### Screen 10: `why-iadd` (`derive`, difficulty 3)

- **Skills:** `skl.py.rebind-vs-mutate`.
- **Prose:** "Why does `+=` change a list but not an int? Put Python's steps for `x += [3]` in order."
- **Canvas:** `derivation-steps` in order mode: five cards, four that belong and one distractor.
  1. "Look up the object that `x` names."
  2. "Ask that object to add `[3]` to itself, in place."
  3. "The list extends itself and hands itself back."
  4. "Bind `x` to the object handed back, which is the same list."
  - Distractor: "Copy the list so that `x` has its own version."
- **Question:** "Order the steps. One card does not belong."
- **Check:** `ordering` with `before` pairs (1 before 2, 2 before 3, 3 before 4) and `exclude: [distractor]`.
- **Leap** (maths-teaching, "motivate the leap"): naive: "`x += y` means `x = x + y`." Fails: "That predicts the two-item list for program B on screen 7, and it printed three items." Points to: "`+=` first asks the object to update itself. Only when it cannot, as for an int, a string or a tuple, does Python fall back to building `x + y`."
- **Diagnose:**

| Learner state | Misconception | Feedback line | Show-why |
|---|---|---|---|
| Distractor included | `mc.py.assign-copies` | "No step copies anything. If Python copied, `y` would not have changed on screen 7." | Replay screen 7's program B |
| Steps 3 and 4 swapped | `slip` | "Python can rebind `x` only once the in-place add has handed the list back." | Highlight cards 3 and 4 |

- **Otherwise:** "Start with finding the object, and end with the name."
- **Reason:** "Look up the object, ask it to extend itself, it hands itself back, bind `x` to the same list."
- **Hints:** Nudge: "Which comes first: finding the object, or changing it?" Point: "This card copies. Did anything on screen 7 copy?" (highlights the distractor). Step: "Find the object, ask it to extend, it hands itself back, bind `x` to it. No copy is made."
- **Why?** Shown: "Python looks up the list, asks it to extend itself, gets the same list back and binds `x` to it." Then: "For an int, step 2 has nothing to ask, so Python computes `x + 1` as a new object and binds `x` to that. The final rebinding step is also why `t[0] += [3]` on a list inside a tuple extends the list and then raises an error: lesson 24 shows it." `rep`: algebra (the ordered steps).
- **Solution:** the cards slide into order and the distractor greys out; text: "Find, ask, hand back, rebind. Nothing is copied."
- **Verification chain:** the order matches the language reference's description of augmented assignment, and CI records on both runtimes that `id(x)` is unchanged by `x += [3]` for a list and changed by `x += 1` for an int.
- **Tutor:** focus: "The mechanism behind screen 7." Notes: "Learners who placed the distractor usually still believe in a hidden copy; replay screen 7 rather than explaining again." Reps: algebra (ordered steps); picture. Avoid: special-method names (lesson 50).

#### Screen 11: `book-copy` (`problem`, `context: quant`, the transfer, difficulty 2)

- **Skills:** `skl.py.alias-mutation`.
- **Prose:** "A risk report runs a stress scenario on a copy of the position book, so the base case stays intact."
- **Canvas:** `heap`, a `node-link`: tapping an option draws the heap that option produces.

```python
base = [100, 50, 25]          # shares held in three stocks
stressed = ...                # your choice
stressed[0] = 0               # the stress: sell the first stock
```

- **Question:** "Which choices make `stressed` a separate list with the same three positions, so line 3 leaves `base` unchanged? Select all that apply."
- **Input:** `choice`, `select: many`: a `base`; b `base.copy()`; c `list(base)`; d `base[:]`; e `[base]`. **Check:** correct b, c and d.
- **Diagnose:**

| Learner state | Misconception | Feedback line | Show-why |
|---|---|---|---|
| a selected | `mc.py.assign-copies` | "That is a second name for the same list, so line 3 would zero the base case." | Draw two arrows on one list; zero its first cell |
| e selected | `mc.py.wrap-copies` | "`[base]` builds a list with one item: the book itself. It has one position, not three." | Draw the outer one-item list with an arrow to the book |
| b, c or d missing | `slip` | "`base.copy()`, `list(base)` and `base[:]` each build a new list with the same items." | Draw the new list beside the old one |

- **Otherwise:** "For each option, ask whether it builds a new list or only adds a name."
- **Reason:** "b, c and d each build a new list holding the same three numbers."
- **Hints:** Nudge: "Which options build a new list, and which only add a name?" Point: "Option a has no call and no brackets after `base`." (highlights option a). Step: "`base.copy()`, `list(base)` and `base[:]` build new lists with the same items. `base` alone is an alias; `[base]` is a one-item list holding the book."
- **Why?** Shown: "b, c and d build new lists with the same three numbers." Then: "Each copies the outer list only: its items are the same objects as before. For numbers that is enough. For a book of nested lists such as `[["AAPL", 100]]`, the inner lists would still be shared; lesson 23 shows the fix." `rep`: picture.
- **Solution:** options b, c and d tick, each drawing its new list; text: "Three ways to build a new list; one alias; one wrapper."
- **Tutor:** focus: "Making a copy on purpose." Notes: "`copy.deepcopy` belongs to lesson 23; mention it only if asked." Reps: picture; analogy (photocopying the book before marking it up). Avoid: "shallow" and "deep" (lesson 23).

#### Screen 12: `summary`

- **Three ideas:**
  1. A name is a label bound to an object. Assignment, including passing an argument, binds and never copies.
  2. Changing a mutable object shows through every name bound to it; building a new object moves one name only.
  3. `==` compares values; `is` asks whether two names share one object, and belongs almost only in `x is None`.
- **Notebook card** (`crd.py.names-objects`): "`b = a`: two names, one object. Changes the object: `xs.append(v)`, `xs[i] = v`, `xs += ys` (lists), `d[k] = v`. Builds a new object: `xs = xs + ys`, `a = a + 1`, `sorted(xs)`. Copy a list: `xs.copy()`, `list(xs)`, `xs[:]`."
- **Common trap line:** "`b = a` does not copy, and neither does a function call: `stress(base)` can change `base`."
- **Bertie:** `celebrate` when the lesson completes.

### 7.3 Lesson quiz (4 items, 1 mark each, no hints, one attempt, Why? after each)

| # | Item | Type, difficulty | Correct and accepted | Diagnosed wrong answers | Why? |
|---|---|---|---|---|---|
| 1 | "What does this print?" `a = [1, 2, 3]`, `b = a`, `a[0] = 99`, `print(b[0])` | Predict output (T), 2 | `99` | `1` (`mc.py.assign-copies`: "`b = a` made a second name, not a copy.") | "`a[0] = 99` changed the one list both names refer to." |
| 2 | "What does this print?" `s = "abc"`, `t = s`, `s = s + "d"`, `print(t)` | Predict output (T), 2 | `abc` | `abcd` (`mc.py.alias-overgeneralised`: "Strings are immutable: `s + "d"` builds a new string and moves only `s`.") | "`t` still names the original string; `s` names a new one." |
| 3 | After `x = [0]`, `y = [0]`, `z = x`, `z.append(1)`, sort each expression into True or False: `x is z`, `x is y`, `x == y`, `y == [0]` | Sort (S), 3; the mark needs all four cards right | True: `x is z`, `y == [0]`. False: `x is y`, `x == y` | `x is y` in True (`mc.py.literal-same-object`: "Two list displays build two objects."); `x == y` in True (`mc.py.assign-copies`: "`z = x` shares `x`'s list, so the append changed `x` to `[0, 1]`.") | "`z` and `x` name one list, now `[0, 1]`; `y` is a separate list still holding `[0]`." |
| 4 | "Which function returns the demeaned values without changing the caller's list?" (a) loops `xs[i] -= m` over `xs` and returns `xs`; (b) returns `[x - m for x in xs]`; (c) sets `ys = xs`, loops `ys[i] -= m` and returns `ys`; (d) loops `for x in xs: x -= m` and returns `xs` (each computes `m = sum(xs) / len(xs)` first) | Single choice (C), 3 | b | a (`mc.py.call-copies`: "`xs` is the caller's list, so the loop changes it."); c (`mc.py.assign-copies`: "`ys = xs` is a second name for the caller's list."); d (`mc.py.alias-overgeneralised`: "`x -= m` moves the loop name `x` to a new float; the list never changes, so the function returns the original values.") | "Only b builds a new list; a and c change the caller's list, and d changes nothing." |

**Marks and mastery.** Each item scores 1 mark; 3 of 4 marks the lesson Mastered (ASSESSMENT.md decision 26). Wrong items join the Redo queue at 7 and 30 days (ASSESSMENT.md 2.3). Choice items are 1 of 4, within the 40% ceiling. Bertie is available on each item once it is graded, for Why? and "Explain another way" (AI-TUTOR.md 2.2).

### 7.4 Verification for this lesson

| Claim | Check |
|---|---|
| `predict`, `arrows`, `labels`: outputs, object count and arrows | The snippet's recorded trace: one list object created, both names bound to it after line 2; `print(backup)` outputs `[100, 101, 102, 99]` on CPython 3.11 and Pyodide 314.0.7 [verified] |
| `labels`: the four comparisons | Each expression evaluated after the three lines: `True`, `True`, `True`, `False` [verified] |
| `rebind`, `rule`: outputs | Recorded outputs `[100, 101, 102]` and `[1, 2, 3]`; every diagnosed wrong answer differs from the correct one and from each other [verified] |
| `ints`: the objects | After line 3, `b` is the same object as before line 3 (`id` unchanged) and `a` is a different object holding 6, on both runtimes [verified] |
| `plus-equals`: both programs | Recorded outputs `[1, 2]` and `[1, 2, 3]`; `id(x)` before and after line 3 differs in A and is equal in B [verified] |
| `stress`: the trap | Recorded output `[0, 50]`; `shocked is base` is `True` [verified] |
| `why-iadd`: the order | The declared order satisfies every `before` pair; the distractor is excluded; the `id` checks confirm no copy for a list and a new object for an int [verified] |
| `book-copy`: the options | Each option executed with line 3: `base` is unchanged for b, c and d, changed for a; e yields a one-item list whose item is `base` [verified] |
| `labels` Why?: the warning | Compiling `x is 1000` emits a `SyntaxWarning` on Python 3.11 and 3.14 [verified] |
| Quiz items | Recorded outputs `99` and `abc`; item 3's four expressions evaluate to `True`, `False`, `False`, `True`; item 4's four functions run on `[1.0, 2.0, 3.0]`: only (b) returns `[-1.0, 0.0, 1.0]` with the caller's list unchanged, and (d) returns the list unchanged [verified] |
| Tutor fields | The leak lint finds no accepted value in any `tutor` field: printed lists are described in words |
| Copy | Copy lints (sentence length, banned words, British spelling, no em-dashes); every code span parses as Python; embargoed terms absent from screens before their introduction; "mutable" first appears on screen 6, after which it is used |

---

## 8. Open items and requests to the other papers

**Open items.**

| # | Item | Effect |
|---|---|---|
| 1 | Which load groups fit the Artifact's Python budget (`ARCHITECTURE.md` 6.2.5, measured at stage E8): `matplotlib`, `scipy-statsmodels`, `testing` | If `matplotlib` does not fit, the D5 code screens, homework D5 and the `1.1.exit` capstone hand off to the web app; if `testing` does not, 1.2 lessons 19 to 24 and homework T5 do. Neither topic exam is affected (decision 14) |
| 2 | matplotlib 3.10.8 and the `tzdata` package inside Pyodide | Figure assertions and time-zone answers were verified on CPython only (section 0.2); CI must run them on Pyodide before lessons 42, 92 and 99 to 107 ship |
| 3 | Display codes (decision 22) | The owner may prefer two-letter codes in every file at once, as `stage1-statistics-ts.md` proposes; ids do not change either way |
| 4 | The Missing Semester 2026 lecture contents | Titles are [searched]; which lecture covers editors, linters, packaging and CI is [check], so the section 2.3 and 5.2 rows for lectures 3, 6, 8 and 9 may move |
| 5 | CS50P's current-year paths (problem-set names now confirmed by secondary sources, section 5); McKinney's appendix A section numbers; the remaining MIT 6.100L lecture numbers; the 3rd edition of Automate the Boring Stuff | Resource rows marked [check] (section 5); `Level.companion` carries `checked: false` until confirmed |
| 6 | Licences in section 5 are [recalled] | Only Software Carpentry and GitHub Docs are marked adaptable (CC BY 4.0); confirm both before any item is `problem-adapted` from them |

**Requests to other papers** (this file edits none of them).

| # | Paper | Request |
|---|---|---|
| 1 | `ARCHITECTURE.md` 6.3.3 | Hypothesis is not in Pyodide 314.0.7's lock [measured], although the `testing` load group names it. Ship its pure-Python wheel (it needs `attrs` and `sortedcontainers`, both in the lock) as the app's own file, checked by SHA-256 like the others, or drop it from the group and let 1.2 lesson 24 hand off |
| 2 | `ARCHITECTURE.md` 6.3; `CONTENT-FORMAT.md` 6.11; widgets-programming 2.4 | Record authored outputs on Pyodide in Node as well as CPython, and fail on differences (section 6, first table). The three classes found here (no floating-point flags in WebAssembly, compensated `sum` from Python 3.12, changed messages) will recur in every Python course |
| 3 | `stage1-linear-algebra.md` (the `1.4.exit` capstones, Cholesky and QR) | In the app, `np.linalg.cholesky` of an indefinite matrix and `solve` of a singular one return `nan` instead of raising `LinAlgError` [measured on Pyodide 314.0.7]. Hidden tests that expect `LinAlgError` will fail on both targets; test `np.isfinite` instead, or have the learner's code check the pivots |
| 4 | `stage1-statistics-ts.md`, `stage1-calculus.md`, `stage1-probability.md` | Any lesson that shows a NumPy or SciPy warning (overflow, divide by zero, invalid value) will not see it in the app; show the recorded CPython warning and say so, or check `np.isfinite` |
| 5 | `CONTENT-FORMAT.md` 3.4 | The R letter clash is gone: result tables are Q in this file |
| 6 | `canon-gap.md` section 6 and `content/sources.yaml` | Add the 31 new source ids marked † in sections 5 and 7: `src.mit-60002-2016`, `src.composing-programs`, `src.python-tutor`, `src.python-docs`, `src.batchelder-names`, `src.pep8`, `src.numpy-docs`, `src.pandas-docs`, `src.matplotlib-docs`, `src.scipy-docs`, `src.quantecon-python`, `src.rougier-numpy`, `src.wilke-dataviz`, `src.huff-lie`, `src.learn-git-branching`, `src.bandit`, `src.explainshell`, `src.shellcheck`, `src.swc-shell`, `src.swc-git`, `src.swc-sql`, `src.sqlzoo`, `src.cs50-sql`, `src.sqlite-docs`, `src.owasp-sqli`, `src.pytest-docs`, `src.hypothesis-docs`, `src.swe-at-google`, `src.beams-commit`, `src.github-docs`, `src.sorva-2013` |
| 7 | `ASSESSMENT.md` 2.9 | Add `estHours` to the rows `1.1.exit` (10) and `1.2.exit` (3); note that `1.1.exit`'s capstone needs matplotlib, so its "Both" depends on open item 1 |
| 8 | `widgets-programming.md` 14 | Move `recursion-tree` and the `mutant-hunter` property mode, and `shell-sim`'s job, remote and `awk` modes, into the waves that ship 1.1 and 1.2 (decision 19); add a float-spacing mode to `number-line` (lesson 4) |
| 9 | `ARCHITECTURE.md` 6.3.3 | Add the `tzdata` package (2025.3 in the lock) to the `numpy-pandas` load group: in Pyodide `zoneinfo.ZoneInfo("America/New_York")` raises `ZoneInfoNotFoundError` until `tzdata` is loaded, and so does pandas 3's `pd.Timestamp(..., tz="America/New_York")`, because pandas 3 uses `zoneinfo` [measured]. The spike's group ships `pytz`, which pandas 3 no longer uses by default. Lessons 42 and 92 and homework B3 need it |

---

## 9. Verification log

Source and correctness pass, 6 October 2026, on CPython 3.11.15 (NumPy 2.4.6, pandas 3.0.6, SciPy 1.17.1), pytest 9.1.1, Hypothesis 6.168.5, GNU bash 5.2.21, Git 2.43.0 and SQLite 3.45.1. Pyodide was not rerun in this pass.

**Recomputed and correct.** Every answer, check value and decision point in the 1.1 and 1.2 homework examples (section 3), including the four T5 mutants, the T2 script in an empty folder, `git status --short` in T3 and every SQL result; the exam blueprints' totals, format mixes, difficulty mixes, course shares and generator shares (section 4); every screen, diagnosis, distractor and quiz item of the sample lesson (section 7), including the `x is 1000` warning; spot checks of numbers in the course tables (lessons 3 to 7, 12, 15, 21, 23, 30, 31, 42, 55, 57, 63, 65, 68, 70, 72, 73, 75, 85, 92, 93, 95 to 97, 101, 105; 1.2 lessons 18, 26, 28, 30, 32). Not checkable here: D3 example 2's bucket letters (its 12-row sample is not in the file) and the matplotlib figure assertions (no matplotlib installed).

**Hours.** 1.1 sums to 150.0 h (estimates 142.25 h) and 1.2 to 40.0 h (estimates 37.5 h); the reading maps sum to 30.0 h (16.0 reading, 14.0 problems) and 8.25 h (4.75 and 3.5), and every per-level subtotal matches. The 1.2 cover list (Git and GitHub, the command line, SQL basics, pytest) is fully taught.

**Changed.**

| Where | Was | Now | Why |
|---|---|---|---|
| Lesson 74 | $S$ "simulated as in lesson 73" with exact value 7.9656 | $S = 100\,e^{-\sigma^2/2 + \sigma Z}$ stated; 9.0962 named as the zero-drift value | Lesson 73's zero-mean log returns give $E[\max(S - 100, 0)] = 9.0962$; 7.9656 needs the drift $-\sigma^2/2$, as homework A3 example 2 already uses |
| Homework Y2 example 1, decision point | `s[4:10]` "works for AAPL and fails for F and SPXW" | Works only for unpadded 4-character roots, AAPL and SPXW alike | On the padded symbols in the checks it fails for AAPL too, and unpadded SPXW works |
| Homework B3 example 2, working | A fixed offset is wrong "about three weeks a year" | About four weeks (21 days in March, 7 around the start of November); the 20:30 sentence made unambiguous | 9 to 29 March and 26 October to 1 November 2025 |
| Homework D6 example 1 (b) | Penny prices "above about 10,000 lose their last digit" | A single price keeps the penny up to $2^{17} = 131{,}072$; sums drift earlier | 12345.669921875 rounds back to 12345.67; the first failure is 131072.01 |
| Sample lesson `est` | 14 minutes, screens "about 11 minutes" | 13 minutes, screens 605 s (about 10 minutes); budget still counts 15 | The screen estimates sum to 605 s |
| Section 0.1 change 9, section 2.3, section 5.1 rows A2 and A3 | McKinney 3rd edition 4.2 ufuncs, 4.3 array-oriented, 4.5 linear algebra, 4.6 pseudorandom | 4.2 pseudorandom, 4.3 ufuncs, 4.4 array-oriented, 4.6 linear algebra, 4.7 random walks | Draft 2 had the 2nd edition's order [searched] |
| Section 2.3 | No row for McKinney chapters 12 and 13 | Row added: chapter 12 left to 1.6 and 2.1, chapter 13 used in D6 | Coverage of the curriculum's resource was silent on two chapters |
| Section 5 | [check] on MIT 6.100L lectures 5, 6, 8, 11, 13; MIT 6.0002 lecture 6; Stat 110 lecture 7 and URL; CS50P sets 2 to 8; McKinney 6.1 and 7.1 to 7.5; the Bailey et al. URL | Numbers, titles and URL filled in and tagged [searched] or [searched, secondary] | Confirmed by search; CS50P names come from solution repositories, so they are tagged secondary |
| Sample lesson `sources` | Sorva "13(2), 2013 [check citation]"; Language Reference sections all [check] | Sorva "13, article 8, 2013 [searched]"; 7.2.1 [searched], 3.1 and 4.2 still [check] | Search confirmed the volume and article number and the augmented-assignment section |
| Homework T4 example 2 | AWS example key [check] | [searched] | AWS documentation uses `AKIAIOSFODNN7EXAMPLE` |
| Section 8, open item 5 | Lists CS50P names and McKinney chapters 6 and 7 as unconfirmed | Narrowed to CS50P paths, McKinney appendix A, the remaining 6.100L lectures and ATBS 3rd edition | Those items are now confirmed |

**Confirmed by search, unchanged.** The Missing Semester 2026 lecture list and order (nine lectures, 12 to 23 January 2026).

**Still [check].** Hull 11th edition's chapter for historical volatility (one search was inconclusive); ATBS, TLCL, Wilke, Okken, SWE at Google and Rougier chapter numbers; Pro Git section numbers; McKinney appendix A; MIT 6.100L lectures 3, 4, 7, 9 and the recursion and class lectures; licences marked [recalled]; Language Reference 3.1 and 4.2. Nothing was found to be invented; no citation was deleted.
