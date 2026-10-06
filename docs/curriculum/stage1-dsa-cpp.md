# Stage 1 detailed curriculum: 1.8 Data Structures and Algorithms, 1.9 C++, 2.4 Contests, and the Stage 1 exit test

Blueprint work file, Stage 2 Phase 1. Draft 1, 6 October 2026.

**Source of truth.** `docs/curriculum.md` for stages, topics, hours and exit tests. This file expands items 1.8 Data structures and algorithms (250 h), 1.9 C++ (140 h) and 2.4 Contests (140 h, Stage 2) into courses, levels, lessons, homework, papers, reading and verification; rebuilds the 1.8 and 1.9 exits and the whole Stage 1 exit test in the app; proposes a completion rule for 2.4, whose curriculum entry sets targets but no exit; and writes one lesson in full.

**Built on.** `docs/design-research.md` sections 5, 8, 9 and 10 (lesson anatomy, curriculum architecture, teaching style, critiques); `docs/blueprint/work/widgets-programming.md` (widget ids and modes, the `code` check and its efficiency tests, `problem-workbench`, `contest-arena`, the `cpp-runner` spike; its sections 1.3 to 1.5 are the working outline this file replaces); `docs/blueprint/work/content-format.md` revision 2 (ids, schema, screen types, checks, tutor fields, drills, verification); `docs/blueprint/work/assessment.md` draft 2 (the assessment ladder, paper kinds, exit parts `1.8.exit` and `1.9.exit`, the problem ledger in 11.5, contests in 11.6, the track rule for 1.9, decision 30 on code items and the two targets); `docs/blueprint/work/ai-tutor.md` draft 2 (Bertie's gate, code review, the code guard, the lockout); `docs/blueprint/work/bertie.md` draft 2 (states and who drives them); `docs/blueprint/work/arch-decision.md` (decision 15, Pyodide on both targets); `docs/blueprint/work/canon-gap.md` revision 2 (the resource canon for 1.8, 1.9 and 2.4, G17 on algorithms with proofs, G18 on software construction, P13 for developers, O1 on contest hours); the sibling files `docs/curriculum/stage1-python-tools.md` (1.1 and 1.2, whose lessons 21 and 28 preview recursion and complexity, and whose `recursion-tree`, `complexity-lab` and `sort-lab` modes this file extends), `stage1-probability.md` (indicators, Catalan numbers, optimal stopping), `stage1-linear-algebra.md` (matrix cost, the FFT) and the Stage 0 files; the owner's lesson-creator, maths-teaching, code-craft and project-forge skills.

**Tags.** Decisions sit in tables with the rejected alternative and the reason. [verified] marks an answer, count, output or diagnostic recomputed while writing this draft (section 0.6). [measured] marks a timing taken on the authoring container, never on a learner's device. [recalled] marks a fact from memory that I am confident of and did not verify here. [check] marks a resource detail (a chapter, lecture or problem-set number, a title, a licence, a URL path) to confirm before content cites it (`checked: false` in `Level.companion` until then). [our choice] marks a design decision without outside evidence. [unverified] marks a platform fact not yet measured. [mode to add] marks a widget mode `widgets-programming.md` does not yet list.

**At a glance.**

| Item | Hours | Courses | Levels | Lessons | Lesson hours | Homework sets | Summative paper | Estimates against hours |
|---|---|---|---|---|---|---|---|---|
| 1.8 Data structures and algorithms | 250 | 5 | 26 | 150 | 37.5 (15.0%) | 26 | `exm.algorithms`: 90 min, 22 items, 80 marks | 242.5 h (97.0%) |
| 1.9 C++ | 140 | 4 | 16 | 88 | 22.0 (15.7%) | 16 | `exm.cpp`: 90 min, 22 items, 80 marks, compiler-free | 134.5 h (96.1%) |
| 2.4 Contests | 140 | 4 | 15 | 84 | 21.0 (15.0%) | 15 | No topic exam (`assessment.md` 2.8); three Arena rounds | 137.5 h (98.2%) |
| **Total** | **530** | **13** | **57** | **322** | **80.5** | **57** | | **514.5 h** |

Exits: `1.8.exit` (150 problems on the ledger; 5 of the last 9 timed held-out mediums solved within 30 minutes) and `1.9.exit` (the 1.7 binomial pricer rewritten in C++ with doctest tests and timed against Python, pasted from the learner's machine) are rebuilt in section 4.4. The Stage 1 exit test, all nine topic exits with the track rule for 1.9, is rebuilt in section 4.5. 2.4 has no curriculum exit; section 4.3 proposes one for the owner.

---

## 0. Scope, decisions and conventions

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Unit of lesson time | **15 minutes per lesson, quiz included**, the unit of every other curriculum file | 10 or 12 minutes | One unit keeps hours tables comparable across the path; algorithm screens with a "be the algorithm" step take the upper end of design research 5.8's 10 to 15 minutes |
| 2 | 1.8 spine | **Grokking Algorithms, 2nd edition, as the first read (levels AC1 to AH6), then one problem list: the app's Problem Gym, which mirrors the 18 NeetCode 150 categories at NeetCode's counts with original problems, and the real NeetCode 150 on LeetCode as the logged outside list.** CLRS 4th edition is a reference only. MIT 6.006 (Spring 2020) is the lecture and theory thread that canon-gap G17 proposes inside the 250 hours | Striver's A2Z sheet (the curriculum's named alternative); CLRS or Skiena as the spine; 6.006 as the spine | The curriculum names Grokking first and NeetCode 150 as the list that "works well in Python, video solutions"; A2Z is larger and built around C++ and Java. Grokking is a first read, not a course, so the lessons carry the depth a top programme adds (proofs, amortised and expected analysis, lower bounds), and 6.006 is where that depth is taught at MIT |
| 3 | Language for 1.8 | **Python 3 throughout**, standard library only (`collections`, `heapq`, `bisect`, `itertools`, `functools`); C++ solutions accepted in the web app once 1.9 lesson 62 is done | C++ from the start; pseudocode only | The owner's code-craft skill defaults to Python; researcher interviews are in Python; Pyodide runs every 1.8 drill on both targets because none needs a package (`arch-decision.md` decision 15). Pseudocode cannot be tested |
| 4 | Courses for 1.8 | **Five courses: Algorithmic Cost (AC, 23 lessons), Arrays, Hashing and Pointers (AH, 33), Stacks, Lists and Heaps (SQ, 22), Trees and Graphs (TG, 31), Recursion, Dynamic Programming and Greedy (DP, 41)** | One course per NeetCode category (18 courses of 3 to 15 lessons); 6.006's unit order | The brief caps an item at five courses and design research 8.2 sets 20 to 45 lessons each. The order follows dependency: cost and recursion first (every later analysis uses them), then linear structures, then trees and graphs (which need recursion and queues), then dynamic programming (which needs all of them) |
| 5 | Theory depth | **Interview list plus proofs**: loop invariants, induction, the master theorem, amortised and expected analysis, the comparison lower bound, exchange arguments, cut property, NP-completeness in plain words. Every level's homework has a long-form proof or analysis | The list alone (NeetCode); CLRS-level proofs on every lesson | Interviews at top firms ask "why is it correct?" and "what is the expected cost?"; ML-lab work needs the analysis habit. Full CLRS rigour on every lesson would leave no time for the 150 problems the exit demands |
| 6 | Problem content | **Every problem is written originally, in our words and numbers, many in a market setting; the NeetCode problem with the same pattern is named as a pointer to its video solution.** No LeetCode or NeetCode statement is copied | Copying statements; linking only | Copyright (`widgets-programming.md` 13.1); a market setting carries the quant transfer; the pointer keeps the curriculum's "video solutions" benefit |
| 7 | The 150 counter | **In-app verified problems (Problem Gym and homework drills, each counted once) plus self-reported LeetCode problems, shown apart** (`assessment.md` 11.5). The hours plan reaches 168 verified problems: 78 homework drills and 90 Gym problems | Verified problems only; self-report only | The curriculum's 150 may be met on LeetCode; the app cannot see LeetCode, so self-report is labelled as such. A plan with 18 problems of slack absorbs problems left unsolved |
| 8 | Held-out timed bank | **40 original mediums, never shown in practice, homework or Bertie's picks, stratified over 12 pattern groups, each with a reference solution, a brute force, hidden tests and an efficiency test.** The exit window is 5 solved within 30 minutes in the last 9 attempts | 30 mediums (`widgets-programming.md` 0.2's floor); LeetCode's "random medium" | "Fresh" needs unseen problems; 9 attempts per window and resits need more than 30 to stay fresh; 40 allows four windows. LeetCode problems cannot be graded in the app |
| 9 | Efficiency grading | **A `complexity` test (line budget and time ratio, `widgets-programming.md` 2.2.1) on every drill whose pattern is the point**; the message names the measured exponent | Wall-clock limits alone | A correct $O(n^2)$ two-sum passes every functional test; the exit's "medium" implies the intended complexity |
| 10 | 1.9 spine | **learncpp.com** (free, kept current), with Stanford CS106L as the lecture parallel and Joshi's *C++ Design Patterns and Derivatives Pricing* (2nd edition) as the pricing-design reference; Stroustrup's *Programming: Principles and Practice Using C++* (3rd edition) as the paid alternative | Stroustrup as spine; Sams (the curriculum rejects it); Meyers first | The curriculum names learncpp or Stroustrup; learncpp is free on every device and has quizzes with solutions; Meyers "comes after a first book" |
| 11 | C++ standard and toolchain | **C++20; GCC 13 or later or Clang 17 or later on the learner's machine [check Clang's `<format>` support]; `-std=c++20 -Wall -Wextra -O2` for builds, `-fsanitize=address,undefined -g -O1` for checking; doctest for tests; CMake for projects.** C++23 features (`std::expected`, `std::print`) are named, never required | C++17; C++23 | C++20 adds concepts, ranges, `<=>`, `std::span` and `std::format`, all used in lessons. GCC 13.3 compiled every snippet here; Clang 18.1 with libstdc++ 13 lacked `std::expected` and `hardware_destructive_interference_size` [verified], so nothing depends on them |
| 12 | Where C++ runs | **Never in the Artifact.** Concept screens show build-time recordings: CI compiles and runs every authored snippet on GCC and Clang, with and without sanitisers, and ships outputs, diagnostics and sanitiser reports as data. Drills run in the web app through `cpp-runner` (the W-C spike) or on the learner's machine with paste-verify | C++ drills in the Artifact | `widgets-programming.md` decision 9 and `assessment.md` decision 30; a compiler sysroot needs archives the Artifact cannot serve, and WebAssembly timings misstate native speed |
| 13 | The 1.9 paper | **Compiler-free**: predict-output, compiles-or-not, find-the-bug, ownership state, layout, complexity and long-form items, plus code-blanks and Parsons items whose every accepted fill CI compiled and tested. It runs on both targets | A web-only paper with live compilation | A paper never splits across targets (`assessment.md` 3.3), and the web compile path is still a spike. Writing whole programs is assessed by homework and the 1.9 exit, on a real compiler |
| 14 | 1.9 and the tracks | **Every track takes the same 88 lessons; the track rule moves `1.9.exit` to the Stage 2 checklist for traders and researchers** (`assessment.md` 2.9). The developer track's "at least double these hours" is met by canon-gap P13 (150 h) plus a 1.9 developer reading list (section 5.2), not by more 1.9 lessons | Separate track versions of 1.9; doubling 1.9's lessons | The curriculum lets C++ "slip into Stage 2" for two tracks, which is a scheduling rule, not a content cut. P13 is where the developer's systems depth belongs |
| 15 | Courses for 1.9 | **Four courses: C++ Foundations (CB, 22), Memory and Ownership (CM, 24), Generic Code and the Standard Library (CL, 21), Performance and the Pricer (CP, 21)** | learncpp's 30 chapters as courses; one course | Four keeps each course inside 20 to 45 lessons and follows the dependency chain the exit needs: a program, then objects that own memory, then the library, then speed and the pricer |
| 16 | Courses for 2.4 | **Four courses: Contest Craft (KC, 21), Contest Mathematics (KM, 26), Contest Data Structures and Graphs (KS, 19), Contest Techniques: DP and Strings (KD, 18)**, taught from the Competitive Programmer's Handbook and the CSES Problem Set (canon-gap's 2.4 canon) on top of 1.8 | Contests as practice only, no lessons | Rating 1,400 needs techniques 1.8 does not teach: number theory, combinatorics, range-query trees, binary lifting, SCC, bitmask and digit DP, string algorithms |
| 17 | 2.4 assessment | **No topic exam** (`assessment.md` 2.8 lists 2.4 among topics closed by practice records); **three Arena rounds** (`contest-arena`, 2 hours, 6 problems) mark progress; a completion rule `2.4.exit` is **proposed for the owner** (section 4.3) | A timed topic paper; no completion rule | A contest is the native exam; the curriculum gives targets (one contest a week, rating 1,400 in the first year) but no exit, and `assessment.md` 11.6 keeps the rating a goal |
| 18 | Contest cadence and hours | **30 rated contests and 3 Arena rounds inside the 140 hours**, about two in every three weeks of Stage 2; the owner is asked to choose between this and more hours | One contest every week of Stage 2 (53 contests) | 53 contests at 2 hours plus 30 minutes of upsolving is 132.5 hours, leaving 7.5 hours for every lesson, homework set and reading. The curriculum's hours and its cadence conflict; section 0.5 item 4 asks the owner |
| 19 | 2.4 under canon-gap O1 | **A 36-lesson core** (section 1.3) that a 60-hour trader or researcher version keeps, marked in the tables | Cutting levels at random if O1 is accepted | O1 is proposed at priority 1; marking the core now means accepting it changes data, not content |
| 20 | When contests start | **Week 1 of Stage 2.** The curriculum's "once you have 100 problems behind you" is met by the Stage 1 exit (150) | Starting contests during 1.8 at 100 problems | `assessment.md` decision 25: no next-stage work before the stage exit. Lessons stay open, so a learner can start early with the recorded override |
| 21 | Display codes | **Two letters**: AC, AH, SQ, TG, DP (1.8); CB, CM, CL, CP (1.9); KC, KM, KS, KD (2.4) | Single letters | All 26 single letters are used by Stage 0 and Stage 1 files; `stage1-statistics-ts.md` already uses two letters. Ids never depend on display codes (`content-format.md` 4.1) |
| 22 | Quiz marks | **1 mark per quiz item, 4 items per lesson, Mastered at 3 of 4** | Marks by difficulty | `assessment.md` decision 26 |
| 23 | The sample lesson | **1.8 lesson 1, "What happens when the input doubles"** (section 7) | Lesson 24 (arrays in memory); 1.9 lesson 1 (source to program) | Every later analysis in 1.8, 1.9 and 2.4 asks how cost grows; the doubling ratio is the most concrete form of that question, and Stage 0 and 1.1 have not asked it (section 0.2) |
| 24 | The Stage 1 exit | **The nine topic exits as one checklist, with a diagnostic route for "sit the exit test first"** (`assessment.md` 7.2) and the map line's two headline bars shown first | A single Stage 1 paper | The curriculum's Stage 1 has no checklist of its own: the map line summarises the item exits. A single paper would duplicate three finals papers and a ledger |
| 25 | Recursion depth in the app | **Recursive drills cap their depth at 500 and say so in the statement; deep inputs ask for an iterative solution** | CPython's default limit of 1,000 | Pyodide runs Python on a WebAssembly stack whose usable depth on a phone is [unverified]; 500 leaves margin until W-B2's spike measures it (open item 6) |

### 0.2 What these items inherit, and do not repeat

| Idea | Taught in | 1.8, 1.9 or 2.4 does |
|---|---|---|
| Halving 1,000,000 names takes 20 checks; logarithms as counts | 0.3 G lesson 49 (screen 10, binary search); 0.2 lesson 108 (bisection); 1.2 lesson 18 (`git bisect`) | Lesson 1 asks how cost changes when the input doubles; lesson 46 starts binary search from a loop that hangs, not from the count |
| `range` counts, fenceposts, $\binom{n}{2}$ pairs in nested loops | 1.1 lessons 12 and 14 | Lesson 2 counts dependent, halving, harmonic and pointer loops as formulas |
| Single-pass running state; maximum drawdown; "maximum minus minimum ignores order" | 1.1 lesson 15 | Lesson 35 is the mirror image (the best trade); lesson 45 shows Kadane is lesson 35 on prefix sums |
| Key functions and the stability of Python's sort | 1.1 lesson 19 | Lessons 14 to 23 build the sorts themselves; lesson 21 uses comparators that are not keys |
| Recursion preview: 89 ways up 10 stairs, `RecursionError` near 1,000 frames | 1.1 lesson 21 | Lesson 8 opens on the Tower of Hanoi; lesson 116 memoises; lesson 5 measures frames and copying |
| Lists, copies, dicts, sets; `1`, `1.0` and `True` are one key; hashability | 1.1 lessons 22 to 26 | Lessons 25 to 29 open hash tables up: buckets, collisions, probing, tombstones, keys and encodings |
| Operation costs: `x in list`, `insert(0, x)`, `s += c`; de-duplicating with a set | 1.1 lesson 28 | Lesson 24 explains why indexing is $O(1)$ from addresses; lesson 4 explains amortised appends |
| Aliasing of a list appended to results | 1.1 lesson 1 | Lesson 110's trap is the same bug inside a backtracking search |
| pytest, property tests, mutants | 1.2 level T5 | Every 1.8 drill reuses `zqtest`; lesson 148 adds stress testing against a brute force |
| The four counting cases, $2^n$ subsets, $n!$ orders, Catalan numbers by reflection, the ballot problem | 0.3 lessons 98 to 102; 1.5 lesson 138 | Lessons 110, 111 and 115 generate the objects the counts count, and use the counts as tests |
| Indicators and linearity of expectation | 1.5 lessons 52 to 54 | Lesson 17 derives quicksort's expected comparisons with them; lesson 25 counts expected collisions |
| Optimal stopping by backward induction (the three-roll die game) | 1.5 lesson 151 | Lesson 131 explains backward induction on a recombining tree as dynamic programming, with a node count, not the die game |
| Elimination costs $n^3/3$; $(AB)C = A(BC)$; the FFT | 1.4 lessons 9, 16 and 76 | Lesson 127 chooses the cheapest bracketing by DP; lesson 13 solves the FFT's recurrence |
| Binomial pricing in Python, put-call parity, Black-Scholes | 1.7 (its curriculum file is still being written) | 1.9 level CP3 rewrites the 1.7 pricer and uses parity and convergence as tests; section 8 lists the interface 1.7 must expose |
| Simulation with standard errors; `price-series` | 1.1 level A3 | 1.9 lesson 65 writes the same estimator in C++ |
| Floating point: spacing, `0.1 + 0.2`, tolerance tests | 0.1 lesson 42; 1.1 lesson 4 | 1.9 lesson 64 adds summation order, Kahan, `-ffast-math`, subnormal numbers |

### 0.3 Conventions for every lesson

**Ids** follow `content-format.md` 4.1. Courses `crs.algcost`, `crs.arrayhash`, `crs.linear`, `crs.treesgraphs`, `crs.dynprog` (1.8); `crs.cppcore`, `crs.cppmemory`, `crs.cppstl`, `crs.cpppricing` (1.9); `crs.contestcraft`, `crs.contestmath`, `crs.contestds`, `crs.contestdp` (2.4). Levels `lvl.<course>.<slug>`, lessons `lsn.<course>.<slug>`, homework `set.<course>.<level-slug>`, practice `set.<course>.<level-slug>-practice`, Problem Gym sets `set.<course>.gym-<level-slug>`, labs `set.cpppricing.lab`, papers `exm.algorithms` and `exm.cpp`, Arena rounds `exm.contests.arena-1` to `-3` (kind `contest`, a request in section 8), projects `prj.alg.order-book` and `prj.cpp.mc-pricer`. Libraries use topic namespaces `alg` (1.8), `cpp` (1.9) and `cp` (2.4): `skl.alg.*`, `mc.cpp.*`, `gen.cp.*`, `drl.alg.*`. Topic ids `top.algorithms`, `top.cpp`, `top.contests`. The `#` column is the lesson's number within its topic.

**Every lesson** runs design research 8.3: a hook on a canvas, free manipulation, the name for what the learner just did, a ladder of 2 to 4 screens each adding one constraint, the trap, the rule stated as a description of the learner's own steps with one derived line the learner completes, a transfer screen where a true quant, ML or engineering context exists, the summary card, and a quiz of 4 items. From the owner's skills each lesson also carries the "why this exists" frame (`frame.why`), one common trap, at least one edge case (`edgeCases`), a worked example with a decision point where the naive route fails (`workedExample`), and a motivated leap on every creative step (`derive` screens with `leap: naive, fails, pointsTo`). In algorithm lessons these take set forms:

- **Manipulation before notation** is "be the algorithm" (`widgets-programming.md` section 7): the learner moves `lo` and `hi`, pops the queue, rewires a `next` arrow or fills a table cell before any pseudocode appears. A wrong move plays the widget's show-why and restores the state.
- **The worked example** runs the naive solution beside the fix on the same input, with the operation counters visible, so the decision point is a number the learner watches diverge.
- **Derive** is one of: a step-count formula, a recurrence's total, an expected count by indicators, a correctness proof put in order, or an exchange argument completed line by line.
- **Concreteness fades**: the canvas is full on the hook, shrinks to a strip on the ladder, and is absent from the last quiz item, which is code or a formula.

**In C++ lessons** the same anatomy holds with three additions: every snippet shown ran in CI on GCC and Clang (decision 12), so "predict the output" items have a recorded answer; undefined behaviour is never shown as having "an output", only as a sanitiser report or a compiler's assumption; and every lesson that writes code shows the warning flags that would have caught its trap.

**In contest lessons** the hook is a contest-style statement with constraints, and the first screen asks for the target complexity before any idea.

**Widgets** use `widgets-programming.md` section 14's ids and modes: `complexity-lab`, `sort-lab`, `dynamic-array`, `pointer-walk`, `range-query-lab`, `binary-search-lab`, `stack-queue-lab`, `linked-list-lab`, `interval-sweep`, `bit-lab`, `tree-lab`, `heap-lab`, `graph-search`, `shortest-path`, `union-find`, `recursion-tree`, `dp-table`, `counterexample-lab`, `problem-workbench`, `hash-table`, `memory-layout`, `compile-pipeline`, `ownership-lab`, `bench-lab`, `contest-arena`, `number-theory-lab`, the code family (`code-cell`, `code-tracer`, `predict-output`, `parsons`, `code-blanks`, `code-annotator`, `diagnostic-reader`, `float-inspector`, `format-lab`, `setup-checklist`), and the primitives (`array-strip`, `cell-grid`, `node-link`, `stepper`, `value-table`, `code-surface`). Shared inputs keep their shared names (`choice`, `numeric-input`, `expression-input`, `derivation-steps`, `token-tray`, `free-response`, `sim-runner`, `live-formula`, `plot-2d`). Element references in hints use `<widget id>/<kind>:<name>` (`content-format.md` 3.5).

**Runtime.** 1.8 and 2.4 Python drills declare `needs: []` and run in Pyodide on both targets. Lesson screens without live code run everywhere, because their traces and outputs are recorded in CI. C++ follows decision 12. 2.4 problems read standard input and write standard output (`code-cell` `stdout` tests), with time limits scaled by the device calibration of `contest-arena`.

**Bertie** follows `ai-tutor.md` 2.2: hints and lines after the lesson's first Check; Why? and "Explain another way" after a screen resolves; nothing on homework before submission; `away` during papers, timed mediums, Arena rounds and live contests. On code he never writes the learner's code before a pass (the code guard, `ai-tutor.md` 8.2); after a pass, "Review my code" returns the owner's code-craft format at the chosen depth (`ai-tutor.md` 2.8), which is where the complexity statement and the senior-dev paragraph live. Every task screen carries `tutor.focus`; no tutor field holds a value the screen's check accepts. The lesson player plays `surprised` on each trap reveal (`bertie.md` 5.3).

**Quiz item types** (`content-format.md` 3.4; letters are document shorthand, never stored): N numeric, X expression, C single choice, M multi-select, O order the steps or lines, S sort or match, T predict the output of code, K code with tests, E entry graded by behaviour, G reach a target state in an algorithm or simulator widget (a `predicate` such as `moveMatchesAlgorithm`, `isHeap`, `listShape`), R select a set of cells, nodes or edges, P a point on a canvas. Long-form items appear in homework and papers, never in quizzes. C and M stay at or below 40% of each course's quiz items (design research 10); section 2.4 counts them.

**Level review.** Every level ends with a Level review of 8 items at difficulty 2 to 4, up to 30% from earlier levels of the same course (`assessment.md` 2.4). Practice set, Gym set (1.8) and homework follow.

**Columns.** Objective is one measurable sentence. Hook is the opening puzzle, with its answer in brackets where it is a number or a short result. Trap is the misconception the trap screen is built around; Edge is the fringe case the lesson must show. Transfer screens are listed under each level table.

**Notation.** $n$ for input size, $\log$ for $\log_2$ unless a base is written, $\ln$ for the natural logarithm, $O$, $\Omega$ and $\Theta$ with their definitions from lesson 3, $T(n)$ for running time, $\alpha = n/m$ for a load factor, half-open ranges $[l, r)$ everywhere, zero-based indices, $V$ and $E$ for vertex and edge counts. Heights count edges (a leaf has height 0, the empty tree $-1$).

### 0.4 Summary of counts

| Item | Course | Code | Id | Levels | Lessons | Numbers | Lesson hours |
|---|---|---|---|---|---|---|---|
| 1.8 | Algorithmic Cost | AC | `crs.algcost` | 4 | 23 | 1 to 23 | 5.75 |
| 1.8 | Arrays, Hashing and Pointers | AH | `crs.arrayhash` | 6 | 33 | 24 to 56 | 8.25 |
| 1.8 | Stacks, Lists and Heaps | SQ | `crs.linear` | 4 | 22 | 57 to 78 | 5.5 |
| 1.8 | Trees and Graphs | TG | `crs.treesgraphs` | 5 | 31 | 79 to 109 | 7.75 |
| 1.8 | Recursion, Dynamic Programming and Greedy | DP | `crs.dynprog` | 7 | 41 | 110 to 150 | 10.25 |
| 1.9 | C++ Foundations | CB | `crs.cppcore` | 4 | 22 | 1 to 22 | 5.5 |
| 1.9 | Memory and Ownership | CM | `crs.cppmemory` | 4 | 24 | 23 to 46 | 6.0 |
| 1.9 | Generic Code and the Standard Library | CL | `crs.cppstl` | 4 | 21 | 47 to 67 | 5.25 |
| 1.9 | Performance and the Pricer | CP | `crs.cpppricing` | 4 | 21 | 68 to 88 | 5.25 |
| 2.4 | Contest Craft | KC | `crs.contestcraft` | 4 | 21 | 1 to 21 | 5.25 |
| 2.4 | Contest Mathematics | KM | `crs.contestmath` | 5 | 26 | 22 to 47 | 6.5 |
| 2.4 | Contest Data Structures and Graphs | KS | `crs.contestds` | 3 | 19 | 48 to 66 | 4.75 |
| 2.4 | Contest Techniques: DP and Strings | KD | `crs.contestdp` | 3 | 18 | 67 to 84 | 4.5 |
| | **Total** | | | **57** | **322** | | **80.5** |

Quiz items: 1,288 (4 per lesson). Section 2.4 gives the single and multiple choice shares per course.

### 0.5 Open items

| # | Item | Effect |
|---|---|---|
| 1 | The `cpp-runner` spike (in-browser Clang or the proxy to Compiler Explorer) has not run [unverified] | Decides whether 1.9 homework drills run in the web app or only on the learner's machine with paste-verify; both are specified, and the 1.9 paper needs neither (decision 13) |
| 2 | NeetCode 150's category counts (9, 5, 6, 7, 7, 11, 15, 3, 7, 9, 13, 6, 12, 11, 8, 6, 8, 7, summing to 150) are recalled [check against neetcode.io] | Sets the Problem Gym's per-category counts (section 3.4); a change moves Gym problems between levels, not lessons |
| 3 | The 1.7 binomial pricer's Python interface is not yet fixed (task in progress elsewhere) | The 1.9 exit compares against it; section 8 request 1 proposes the interface |
| 4 | **Owner decision:** 2.4 at 140 hours holds about 33 contests, not one a week for all of Stage 2 (decision 18) | Either accept 30 rated contests plus 3 Arena rounds, or raise 2.4 to about 190 hours for 53 contests |
| 5 | **Owner decision:** the proposed `2.4.exit` (section 4.3) | Without it, 2.4 has no completion state (`assessment.md` 2.12) |
| 6 | Usable recursion depth of Pyodide on the reference phone [unverified] | Decision 25's cap of 500; W-B2 measures it |
| 7 | Arena round paper kind `contest` is not among `assessment.md` 3.1's kinds | Section 8 request 2 |
| 8 | Resource details marked [check] in section 5, especially Grokking 2nd edition chapter numbers, 6.006 Spring 2020 lecture numbers, learncpp chapter numbers after its reorganisation, and CSES section names | Confirm before content cites them |
| 9 | Widget modes marked [mode to add] in section 2: `shortest-path` Floyd-Warshall, `pointer-walk` reach, `bit-lab` C++ precedence, `memory-layout` false-sharing, `range-query-lab` sparse table, `tree-lab` Euler tour and binary lifting, `graph-search` SCC, bridges and 2-SAT, `number-theory-lab` CRT and Grundy, `bench-lab` denormals | The widget owner confirms; until then those screens use primitives |

### 0.6 What was executed

All on 6 October 2026, in a scratch folder outside the repository [verified]:

- **Python.** CPython 3.11.15 with NumPy 2.4.6 and SymPy 1.14.0. Three scripts (about 900 lines) recomputed every number in the hooks of section 2, every homework example and reference solution in section 3, the paper items of section 4 that state numbers, and every value in the sample lesson: exact enumeration with `itertools` and `fractions` for counts and probabilities, brute force against each fast method on random inputs, and simulation only where it confirms an exact value (reservoir sampling, random BST heights). Pyodide was not available in this container; standard-library behaviour the items use is the same on Python 3.14 except built-in `sum` of floats, which no item here uses (`stage1-python-tools.md` 0.1 change 3).
- **C++.** GCC 13.3.0 and Clang 18.1.3 (with libstdc++ 13) on x86-64 Linux. Every type size, padding, conversion, diagnostic and sanitiser outcome quoted in the 1.9 tables was compiled and run, including: the signed-overflow loop that prints 31 at `-O0` and never ends at `-O2` on both compilers; `std::sort` with a `<=` comparator reading past the buffer under AddressSanitizer; a user-declared destructor turning a move into a copy; `-ffast-math` deleting Kahan compensation and making `std::isnan` false for a NaN; and a two-thread counter losing about 40% of its increments with ThreadSanitizer naming the race.
- **Timings** [measured] on an Intel Xeon at 2.1 GHz with 4 cores: the CRR pricer in pure Python, NumPy and C++ at $N$ from 1,000 to 10,000; row against column traversal of a $4096 \times 4096$ matrix; sorted insertion into `std::vector` against `std::list`; adjacent against padded atomic counters on 4 threads. They appear only as "on one machine" illustrations, never as answers.
- **Not executed:** anything needing a network (LeetCode, Codeforces, CSES), doctest (not installed; tests were written as plain asserts), Pyodide, and the in-browser C++ paths.

---

## 1. Item overview

### 1.1 1.8 Data structures and algorithms (250 h)

**Purpose in a quant or ML career.**

- **It is the developer interview and part of every other.** Developer interviews test algorithms and C++ (curriculum track table); researcher interviews include a coding round and a data take-home, and slow code fails a take-home on time.
- **Market data is large.** A day of US equity quotes runs to billions of messages [recalled]. Whether a feature is computed in $O(n)$ or $O(n^2)$, with a heap or a sort, decides whether a backtest runs overnight or not at all.
- **The structures are the products.** An order book is a pair of priority queues or ordered maps; a rolling maximum is a monotonic deque; a point-in-time join is a binary search; currency arbitrage is a negative cycle; a binomial pricer is dynamic programming on a recombining tree.
- **Proof habits transfer.** Loop invariants, exchange arguments and expected-cost analysis are the same reasoning ML researchers use for convergence and complexity claims in papers.
- **Thinking under a clock.** The exit's "fresh medium in 30 minutes" trains the decompose, try-small, test habit that interview rounds and live debugging reward.

**Learning outcomes.** At the end of 1.8 the learner can:

| # | Outcome | Measured by |
|---|---|---|
| DS-O1 | Predict how time and memory grow with input size for code of up to 15 lines, as an exact count or a $\Theta$ class, including amortised and recursive cases | 85% on difficulty-3 items; exam items 1 to 3 |
| DS-O2 | Prove an algorithm correct with a loop invariant, induction or an exchange argument, and analyse amortised and expected cost | Long-form at 7 of 10 in homework AC2, AC3, AH6, DP5; exam item 21 |
| DS-O3 | Solve divide-and-conquer recurrences with the recursion tree and the master theorem | 85% on difficulty-3 items; exam item 4 |
| DS-O4 | Implement and analyse insertion, merge, quick, heap, counting and radix sorts, quickselect and external merging, and explain the $\Omega(n \log n)$ comparison bound | Homework AC3, AC4; exam items 5 and 6 |
| DS-O5 | Build and analyse chained and open-addressed hash tables and apply hashing patterns, rolling hashes and randomised hashing | Homework AH1; exam item 7 |
| DS-O6 | Apply two pointers, sliding windows, monotonic deques, prefix sums, difference arrays, binary search on data and on answers, and interval sweeps | Problem Gym categories passed; exam items 8 to 11 |
| DS-O7 | Use stacks, queues, linked lists and heaps, including monotonic stacks, LRU caches, $k$-way merges, running medians and an order book | Homework SQ1 to SQ3; exam items 12 and 13 |
| DS-O8 | Traverse, construct and query binary trees, search trees and tries | Homework TG1, TG2; exam item 14 |
| DS-O9 | Model problems as graphs and solve them with BFS, DFS, topological sort, union-find, Dijkstra, Bellman-Ford, minimum spanning trees and Floyd-Warshall, including arbitrage detection | Homework TG3 to TG5; exam items 15 to 17 |
| DS-O10 | Design dynamic programmes (state, recurrence, order, base, answer), fill and reconstruct 1D and 2D tables, and decide when a greedy choice is provably right | Homework DP2 to DP5; exam items 18 to 20 |
| DS-O11 | Use bit manipulation, fast exponentiation and exact integer arithmetic | Homework DP6 |
| DS-O12 | Recognise problems that are NP-hard in general and choose pruning, meet in the middle or a stated heuristic | Homework DP7 |
| DS-O13 | Solve an unseen medium in 30 minutes, test it against a brute force, and explain it aloud | `1.8.exit` timed window; exam item 22 |
| DS-O14 | Solve 150 problems | `1.8.exit` ledger |

**Prerequisites.** 1.1 (Python, especially lessons 1, 12 to 28 and level A3) and 1.2 (Git, pytest; every Gym solution can live in the learner's repository). 0.3 counting (lessons 98 to 102), induction (0.3 lesson 132) and recurrences (0.3 lesson 42). 1.5 indicators (lessons 52 to 54), used by lessons 17 and 25. 1.4 lessons 9 and 76 (matrix products, the FFT), used by lessons 13 and 127. 1.7's binomial tree and order book, used as transfers by lessons 74 and 131. The curriculum places 1.8 after 1.3 to 1.7, so all of these are done.

**Hours budget (250 h).**

| Block | What | Hours | Share | Unit that carries the estimate |
|---|---|---|---|---|
| In-app lessons | 150 lessons at 15 minutes, quiz included | 37.5 | 15.0% | `Lesson.est` |
| In-app practice and redo | 26 level reviews of 8 items (6.5); 26 practice sets of generated items at 30 minutes (13.0); the Redo queue at 7 and 30 days (5.0) | 24.5 | 9.8% | Reviews: summed item `est`; practice: `set.<course>.<level>-practice`; redo: spent time only |
| Homework | 26 sets at about 2.5 hours (7 items each, 3 of them code drills that count on the ledger) | 65.0 | 26.0% | Homework `set.*` |
| Exams | `exm.algorithms` (90 min), one practice paper (90 min), reviewing both (60 min) | 4.0 | 1.6% | `exm.algorithms` minutes (1.5); practice paper and review: spent time only |
| External reading and lectures | Grokking Algorithms, whole book, first read (10.0); MIT 6.006 Spring 2020 selected lectures (12.0); 6.006 problem sets as the theory thread (14.0) | 36.0 | 14.4% | `Level.companion` hours (section 5.1) |
| Projects or drills | Problem Gym: 90 problems at about 40 minutes (60.0); timed held-out windows for the exit, 9 attempts with debriefs (9.0); the Order Book project (14.0) | 83.0 | 33.2% | Gym sets `set.<course>.gym-*`, kind `practice`; `1.8.exit` `estHours` 9; `prj.alg.order-book` milestone hours 14 |
| **Total** | | **250.0** | 100% | Estimates **242.5 h (97.0%)**; spent-only time 7.5 h |

Solving time (everything except 22 hours of reading and lectures) is 228 hours, 91%, above the curriculum's 60% floor. The ledger plan: 78 homework drills and 90 Gym problems give 168 verified problems against the exit's 150.

### 1.2 1.9 C++ (140 h)

**Purpose in a quant or ML career.**

- **Speed where it is paid for.** Pricing libraries, risk engines, execution systems and market data handlers at most trading firms are C++ [recalled]; the curriculum's developer track treats it as "the core skill".
- **Researchers hand code to developers.** A researcher who can read C++, write a correct kernel and bind it to Python is faster to production and easier to work with.
- **ML systems.** PyTorch's core, CUDA kernels and inference servers are C++ [recalled]; ML-lab engineers read it daily.
- **Discipline about memory and lifetime.** Ownership, undefined behaviour and cache behaviour are the questions quant developer interviews ask after algorithms (canon-gap G13 notes "why a vector beats a linked list").
- **The exit is a pricer.** Rewriting the 1.7 binomial pricer, with tests and an honest timing against Python, is the shape of real work: same numbers, faster, proven by tests.

**Learning outcomes.** At the end of 1.9 the learner can:

| # | Outcome | Measured by |
|---|---|---|
| CP-O1 | Build multi-file C++20 programs with CMake, explain each stage from source to executable, and fix compile and link errors from the first diagnostic | Homework CB1, CB3; exam items 1 and 2 |
| CP-O2 | Predict the results of integer and floating arithmetic, conversions and promotions, and name the undefined behaviours they risk | 85% on difficulty-3 items; exam items 3 and 4 |
| CP-O3 | Write functions with value, reference and const reference parameters, overloads and templates, choosing each deliberately | Homework CB3, CL1; exam item 5 |
| CP-O4 | Explain object lifetimes on the stack and heap, read AddressSanitizer and UndefinedBehaviorSanitizer reports, and fix the bug each names | Homework CM1, CP1; exam items 6 and 7 |
| CP-O5 | Design classes with invariants, constructors, `const` members, operators and RAII, and lay structs out to avoid padding | Homework CM2; exam items 8 and 9 |
| CP-O6 | Implement copy and move correctly, apply the rules of zero, three and five, and choose `unique_ptr`, `shared_ptr` or a value | Homework CM3; exam items 10 and 11 |
| CP-O7 | Use inheritance with virtual functions, lambdas, `std::optional` and `std::variant` to design a payoff and pricer interface | Homework CM4; exam item 12 |
| CP-O8 | Choose standard containers and algorithms by their costs, use iterators and ranges without invalidation bugs, and write valid comparators | Homework CL2, CL3; exam items 13 to 15 |
| CP-O9 | Generate random numbers reproducibly, reason about floating-point summation and fast-math, and write tested Monte Carlo and Black-Scholes code | Homework CL4; `prj.cpp.mc-pricer`; exam items 16 and 17 |
| CP-O10 | Measure performance honestly (optimisation levels, repeats, spread, dead code), and explain cache locality, allocation costs and subnormal numbers | Homework CP2; exam items 18 and 19 |
| CP-O11 | Write threaded code without data races and explain false sharing | Homework CP4; exam item 20 |
| CP-O12 | Rewrite the 1.7 binomial pricer in C++ with tests and time it against Python | `1.9.exit` (section 4.4) |

**Prerequisites.** 1.8 complete (data structures in Python first, so 1.9 teaches the language, not the algorithms); 1.1 and 1.2 (Git, tests, CI); 1.7's binomial pricer (the exit's starting point); 1.1 level A3 and 1.5 for Monte Carlo standard errors; 0.1 lesson 42 and 1.1 lesson 4 for floating point. No C or C++ is assumed.

**Hours budget (140 h).**

| Block | What | Hours | Share | Unit that carries the estimate |
|---|---|---|---|---|
| In-app lessons | 88 lessons at 15 minutes | 22.0 | 15.7% | `Lesson.est` |
| In-app practice and redo | 16 level reviews (4.0); 16 practice sets at 30 minutes (8.0); the Redo queue (3.0) | 15.0 | 10.7% | As 1.8; redo spent only |
| Homework | 16 sets at about 2.5 hours (7 items, 2 or 3 of them C++ drills) | 40.0 | 28.6% | Homework `set.*` |
| Exams | `exm.cpp` (90 min), one practice paper, reviewing both | 4.0 | 2.9% | `exm.cpp` minutes (1.5); the rest spent only |
| External reading and lectures | learncpp.com chapters with their quizzes (18.0); Stanford CS106L selected lectures (3.0); two conference talks and Drepper's memory paper sections on caches (2.0) | 23.0 | 16.4% | `Level.companion` hours (section 5.2) |
| Projects or drills | The 1.9 exit: the pricer in C++ with tests and timings (12.0); C++ Lab: 12 Gym problems re-solved in C++ at 1 hour (12.0); the Monte Carlo pricer project (12.0) | 36.0 | 25.7% | `1.9.exit` `estHours` 12; `set.cpppricing.lab` (kind `practice`) 12; `prj.cpp.mc-pricer` 12 |
| **Total** | | **140.0** | 100% | Estimates **134.5 h (96.1%)**; spent-only 5.5 h |

Solving time is 117 hours, 84%. C++ Lab problems are re-solves of Gym problems, so they do not add to the 1.8 ledger, which counts each problem once.

### 1.3 2.4 Contests (140 h, spread across Stage 2)

**Purpose in a quant or ML career.**

- **Developer hiring.** A rating helps developer applications (curriculum 2.4); contest problems are the hardest end of coding interviews.
- **Speed and accuracy under a clock.** Contests train reading, choosing, coding and debugging under time with an unforgiving judge, the same pressure as a live interview or a production incident.
- **Mathematics with code.** Number theory, combinatorics, expected values and game theory are the contest topics nearest to quant interview puzzles; Project Euler is maths with code by design.
- **Research and trading competitions.** Kaggle (researcher track) and firm-run trading competitions such as IMC Prosperity (trader track) are named by the curriculum and taught as their own lessons.
- **Honest scope.** The curriculum notes that rating-based shortlisting is mainly an Indian campus-hiring practice and that a rating counts for little in trader or researcher interviews. Lesson 1 says so, and canon-gap O1 proposes 60 hours outside the developer track.

**Learning outcomes.** At the end of 2.4 the learner can:

| # | Outcome | Measured by |
|---|---|---|
| CT-O1 | Read a contest statement, derive the target complexity from its constraints, and choose Python or C++ with fast input | Homework KC1; Arena round problem A and B solve rates |
| CT-O2 | Solve ad hoc, constructive, greedy, search and interactive problems at Codeforces Div. 2 A to C level | Arena rounds; homework KC2, KC3 |
| CT-O3 | Run a stress test and hack a wrong or slow solution | Homework KC4 |
| CT-O4 | Apply sieves, gcd and extended Euclid, modular inverses, combinatorics modulo a prime, CRT and matrix powers | Homework KM1 to KM3 |
| CT-O5 | Solve expected-value, probability-modulo-prime and impartial-game problems with linearity, DP and Sprague-Grundy | Homework KM4 |
| CT-O6 | Solve integer geometry problems exactly: orientation, polygon area, convex hull | Homework KM5 |
| CT-O7 | Use sparse tables, Fenwick and segment trees with lazy propagation, Euler tours, binary lifting, SCC, bridges, 2-SAT and flows | Homework KS1 to KS3 |
| CT-O8 | Use bitmask, digit, tree and interval DP, string hashing, prefix and Z functions, tries, meet in the middle and square-root techniques | Homework KD1 to KD3 |
| CT-O9 | Hold a weekly practice loop: contest, upsolve, log; reach the curriculum's first-year target of a 1,400 rating | Contest log (`assessment.md` 11.6); proposed `2.4.exit` |

**Prerequisites.** Stage 1 complete, in particular 1.8 (all of it) and, for C++ submissions, 1.9 through lesson 62. 1.5 for expected values and 1.4 for matrices (matrix powers, XOR bases over $\mathrm{GF}(2)$). The curriculum's "100 problems behind you" is met by the Stage 1 exit.

**Hours budget (140 h).**

| Block | What | Hours | Share | Unit that carries the estimate |
|---|---|---|---|---|
| In-app lessons | 84 lessons at 15 minutes | 21.0 | 15.0% | `Lesson.est` |
| In-app practice and redo | 15 level reviews (3.75); the Redo and upsolve queue (2.5) | 6.25 | 4.5% | Reviews: summed item `est`; redo spent only. Contests replace generated practice sets (decision 18) |
| Homework | 15 sets at about 1.5 hours (5 items: 3 or 4 contest problems and 1 long-form proof) | 22.5 | 16.1% | Homework `set.*` |
| Exams | Three Arena rounds of 2 hours plus 30 minutes of review | 7.5 | 5.4% | `exm.contests.arena-*` minutes plus review (proposed kind `contest`, section 8 request 2) |
| External reading and lectures | Competitive Programmer's Handbook chapters (5.5); USACO Guide modules and Codeforces EDU lessons (2.25) | 7.75 | 5.5% | `Level.companion` hours (section 5.3) |
| Projects or drills | 30 rated contests at 2 hours (60.0), each upsolved for 30 minutes (15.0) | 75.0 | 53.6% | Contest log entries (`assessment.md` 11.6), counted as earned when logged |
| **Total** | | **140.0** | 100% | Estimates **137.5 h (98.2%)**; spent-only 2.5 h |

**The 60-hour core if canon-gap O1 is accepted** (trader and researcher tracks). Lessons marked ◆ in section 2.3 form the core: all 21 of course KC, 11 of KM (levels KM1 and KM2) and 4 more (lessons 33, 38, 41 and 49), 36 lessons in all. Budget: lessons 9.0 h; 6 level reviews 1.5 h; 6 homework sets 9.0 h; two Arena rounds 5.0 h; reading 3.0 h; 12 contests with upsolving 30.0 h; redo 2.5 h; total 60.0 h. The developer track keeps all 84 lessons and 140 hours.

---

## 2. Courses

Lesson rows follow section 0.3. Every hook number in brackets was recomputed (section 0.6) unless tagged otherwise.

### 2.1 Item 1.8 Data structures and algorithms

#### Course AC: Algorithmic Cost (`crs.algcost`, 4 levels, 23 lessons)

How to say what an algorithm costs and why it is correct, before any data structure: growth under doubling, exact step counts, asymptotic notation, amortised and expected cost, recursion with its proofs, recurrences, and sorting as the worked case of all of them. Grokking chapters 1 to 4 run alongside; MIT 6.006 lectures 1, 3 and 5 are the lecture thread.

**Level AC1: How Cost Grows** (`lvl.algcost.growth`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | `lsn.algcost.doubling` What happens when the input doubles | Predict how the running time of a single loop, a pair loop and a halving loop changes when the input doubles, and name the growth law from the doubling ratio | A backtest takes 2 seconds on one year of 252 trading days. Three versions: scan each day once; compare every pair of days; binary-search each day in a sorted list. How long on two years? (4 s; 8 s; about 4.6 s) | `complexity-lab` (code, race), `code-tracer` (hit counts), `value-table` | Trap: "twice the data, twice the time" for every program (the pair loop's 31,626 comparisons become 126,756, a factor of 4.008). Edge: the halving loop adds one step (8 to 9) instead of multiplying; $n \log n$ grows by $2(1 + 1/\log_2 n)$, slightly more than 2; a fixed start-up cost hides growth at small $n$ | N, N, S, C |
| 2 | `lsn.algcost.counting-steps` Counting steps in code | Write the exact number of times the innermost line runs as a formula in $n$ for single, dependent nested, halving, harmonic and pointer loops, and reduce it to its leading term | `for i in range(n): for j in range(i):` runs the body how many times for $n = 1{,}000$? (499,500) And when the inner `while j < n` never resets `j`? (1,000) | `complexity-lab` (code), `code-tracer` (hits), `expression-input` | Trap: two nested loops are always $n^2$ (a pointer that never resets makes the pair $O(n)$ in total). Edge: `for j in range(i, n + 1, i)` inside `for i in range(1, n + 1)` runs $\sum \lfloor n/i \rfloor \approx n \ln n$ times (7,069 for $n = 1{,}000$); every formula must hold at $n = 0$ and $n = 1$ | X, N, X, C |
| 3 | `lsn.algcost.big-o` Big O, Omega and Theta | Prove or refute $f = O(g)$ by exhibiting constants $c$ and $n_0$, rank common growth rates, and find a crossover point | $100n$ steps against $n^2$ steps: which program is faster at $n = 50$, and from which $n$ is the other one faster? (the $100n$ program loses below 100 and wins above) | `complexity-lab` (growth), `token-tray` (ranking), `derivation-steps` | Trap: "$O$ is the exact growth" or "$O$ means the worst case" ($O$ is an upper bound on whichever case you choose to measure; $\Theta$ is tight). Edge: $2^{n+1} = O(2^n)$ but $4^n \ne O(2^n)$; the base of a logarithm only changes the constant; $100 n \log_2 n$ beats $n^2$ until $n = 997$ | S, N, C, N |
| 4 | `lsn.algcost.amortised` Worst case, average and amortised cost | Compute the total and average copying cost of $n$ appends to a doubling array, and separate amortised cost (over a sequence of operations) from average-case cost (over random inputs) | Append 1,025 prices to an array that starts with room for 1 and doubles when full. How many element copies in total? (2,047) | `dynamic-array` (analysis), `complexity-lab` | Trap: amortised $O(1)$ means every append is fast (the 1,025th append copies 1,024 elements; the bound is on the total). Edge: growing by a constant 10 slots makes $10^4$ appends cost 4,995,000 copies (quadratic); growing by a factor of 1.5 costs about 2.1 copies per append at $n = 10^6$ against 1.05 for doubling | N, C, N, M |
| 5 | `lsn.algcost.space` Space and the call stack | State the auxiliary space of an algorithm including recursion depth, and predict when a recursive Python function exceeds the recursion limit or copies quadratically | `total(xs)` returns `xs[0] + total(xs[1:])`. For 10,000 prices: how many frames at once, and how many elements copied in all? (10,000 frames, so it fails at the default limit; 49,995,000 copies) | `recursion-tree` (calls, stack panel), `complexity-lab` | Trap: "a recursive sum uses constant space" (one frame per element, and each slice copies the rest). Edge: CPython's default limit is 1,000 frames; Python does not eliminate tail calls; an index parameter removes the copying but not the frames | N, N, C, T |
| 6 | `lsn.algcost.budgets` From constraints to a target complexity | Turn an input bound and a time limit into the slowest complexity that fits, using about $10^7$ simple Python steps a second and $10^8$ to $10^9$ in compiled C++ | $n \le 2 \times 10^5$, 2 seconds, Python. Which of $n^2$, $n \sqrt{n}$, $n \log n$ and $n$ fit? ($n \log n$ and $n$; $n\sqrt{n}$ is about $9 \times 10^7$ steps) | `complexity-lab` (budget), `choice` | Trap: treating the rule of thumb as exact, or forgetting the factor of $q$ queries. Edge: $n \le 20$ invites $2^n$; $n \le 500$ invites $n^3$; a sum of $n$ over test cases bounded by $2 \times 10^5$ is a budget for the whole input [10^7 additions took 0.76 s on CPython 3.11, measured] | M, C, N, M |
| 7 | `lsn.algcost.measuring` Measuring growth | Estimate an exponent from timings at $n$, $2n$ and $4n$ on a log-log plot, and explain why one timing, or a loop with one built-in call, misleads | Timings 0.05 s, 0.20 s and 0.80 s at $n = 10^4$, $2 \times 10^4$ and $4 \times 10^4$: the exponent? (2) | `complexity-lab` (timing), `bench-lab` (race), `plot-2d` | Trap: one timing reveals the complexity; a one-line loop body such as `x in big_list` is constant time. Edge: timer noise at small $n$; start-up costs flatten the curve; cache effects make kinks (1.9 lesson 73) | N, C, N, P |

Transfer screens: lesson 1 sizes a backtest on ten years of minute bars; lesson 2 counts the pairs in a 500-stock correlation matrix against 3,000 stocks (124,750 against 4,498,500, 36 times as many); lesson 4 explains why appending ticks to a list stays cheap; lesson 6 reads a data vendor's file size as a complexity budget.

**Level AC2: Recursion and Proof** (`lvl.algcost.recursion`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 8 | `lsn.algcost.recursive-leap` Thinking recursively | Write a recursive solution by trusting the call on a smaller input, with a base case and progress towards it | Move a tower of 3 discs between pegs, one disc at a time, never a larger on a smaller. Moves for 3 discs? For 64? (7; $2^{64} - 1$) | `recursion-tree` (calls), `parsons`, `code-tracer` | Trap: tracing every call before believing the code (assume the smaller call works, exactly as an induction hypothesis does). Edge: two-term recursions need two base cases; shrinking by subtraction against halving; 1.1 lesson 21 is assumed | N, X, O, T |
| 9 | `lsn.algcost.induction-proofs` Proving recursive code correct | Prove a recursive function correct by strong induction and count its work, for fast exponentiation | `power(x, n)` squares `power(x, n // 2)` and multiplies once more when $n$ is odd. Correct for every $n \ge 0$? Multiplications for $n = 1{,}000$? (yes; 16, against 999 for a loop) | `derivation-steps` (order the proof), `recursion-tree` (power), `code-blanks` | Trap: two checked examples called a proof, or ordinary induction where the step uses $n // 2$ (strong induction). Edge: $n = 0$ is the base; negative $n$; the count is the number of binary digits plus the number of 1 bits | O, N, C, K |
| 10 | `lsn.algcost.loop-invariants` Loop invariants | State a loop invariant and prove initialisation, maintenance and termination, for insertion sort and a running maximum | After each pass of insertion sort on [5, 2, 4, 6, 1, 3], what is true of the first $i + 1$ elements? Fill the states after passes 1 to 5 | `sort-lab` (insertion, be), `derivation-steps` | Trap: an invariant that is true but useless at the end ("every element is an integer"). Edge: termination needs a quantity that falls every pass; the invariant must hold before the first pass, when the prefix has one element | G, O, C, M |
| 11 | `lsn.algcost.merge-sort` Divide and conquer: merge sort | Merge two sorted lists in linear time, build merge sort on it, and bound its comparisons | Merge the sorted hands [2, 5, 7] and [1, 3, 8, 9] by always taking the smaller front card. Comparisons at most? (6) | `sort-lab` (merge, be), `recursion-tree` (divide) | Trap: merging as "sort the concatenation" (that costs $n \log n$ again, not $n$); slicing copies at every level of a Python merge sort. Edge: taking from the left list on ties keeps merge sort stable; one list empties early | N, G, C, T |
| 12 | `lsn.algcost.recurrences` Recurrences and the recursion tree | Solve recurrences of the shapes $aT(n/b) + f(n)$ and $T(n - 1) + f(n)$ by summing work per level of the recursion tree | Merge sort on 1,024 items: fill in the work per level of $T(n) = 2T(n/2) + n$, then the total (1,024 per level, 10 levels, 10,240) | `recursion-tree` (cost), `expression-input` | Trap: "two recursive calls mean $2^n$" (it depends on how the input shrinks: $2T(n/2) + n$ is $n \log n$, $2T(n - 1) + 1$ is $2^n$). Edge: $T(n/2) + 1$ is $\log n$ (binary search); $T(n - 1) + n$ is $n^2$ (quicksort's worst case) | N, X, S, C |
| 13 | `lsn.algcost.master-theorem` The master theorem | Classify $T(n) = aT(n/b) + f(n)$ by comparing $f(n)$ with $n^{\log_b a}$, derived from the three shapes of the recursion tree | Multiplying two $n$-digit numbers by halves needs 4 half-size products, or 3 with Karatsuba's trick. How do the costs grow? ($n^2$ against $n^{\log_2 3} = n^{1.585}$) | `recursion-tree` (cost), `complexity-lab` (growth) | Trap: applying the basic theorem to $2T(n/2) + n \log n$ (it falls between the cases; the answer is $n \log^2 n$) or to $T(n - 1)$ recurrences. Edge: Strassen's 7 products give $n^{\log_2 7} = n^{2.807}$; 1.4 lesson 76's FFT is $2T(n/2) + n$ | S, X, C, N |

Transfer screens: lesson 9 counts the multiplications behind compounding a daily rate over 10,000 days; lesson 11 merges two exchanges' sorted trade tapes; lesson 13 explains why matrix multiplication libraries do not use Strassen at the sizes quants meet [recalled: numerical stability and constants].

**Level AC3: Sorting** (`lvl.algcost.sorting`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 14 | `lsn.algcost.insertion-selection` Insertion and selection sort | Perform both sorts by hand, count comparisons and swaps on sorted, reversed and random input, and relate insertion sort's work to the number of inversions | 1,000 timestamps arrive with only 5 pairs out of order. Which simple sort finishes in about 1,000 steps? (insertion sort) | `sort-lab` (be, compare) | Trap: insertion sort is always $n^2$ (it is $O(n + \text{inversions})$, so nearly sorted data is linear). Edge: selection sort always makes $\frac{n(n - 1)}{2}$ comparisons but at most $n - 1$ swaps, which matters when writes are expensive | C, N, G, M |
| 15 | `lsn.algcost.inversions` Counting inversions | Count a ranking's inversions in $O(n \log n)$ during merge sort, and use the count as a distance between two rankings | Two analysts rank five funds; relabelled against the first, the second reads [3, 1, 4, 5, 2]. How many of the 10 pairs do they order differently? (4) | `sort-lab` (merge, counters), `cell-grid` (pair grid) | Trap: counting only neighbours out of order, or the $O(n^2)$ pair loop on a million items. Edge: ties are not inversions; Kendall's tau is $1 - \frac{4 \times 4}{5 \times 4} = \frac15$ here | N, N, C, K |
| 16 | `lsn.algcost.quicksort` Quicksort and partitioning | Partition around a pivot with Lomuto's scheme and predict quicksort's cost for good and bad pivots | Quicksort [1, 2, ..., 8], always taking the first element as pivot. Comparisons? (28, every pair) | `sort-lab` (quick-lomuto, be), `recursion-tree` (divide) | Trap: quicksort is always $n \log n$ (sorted input with a first-element pivot gives $\frac{n(n - 1)}{2}$). Edge: many equal keys need a three-way partition; Hoare's scheme swaps less | N, G, C, T |
| 17 | `lsn.algcost.random-pivots` Expected cost by indicators | Derive quicksort's expected comparisons with random pivots, $2(n + 1)H_n - 4n$, from the chance $\frac{2}{j - i + 1}$ that the $i$th and $j$th smallest are ever compared | With random pivots on 10 distinct values, what is the chance that the smallest and largest are ever compared? ($\frac15$) | `recursion-tree` (quicksort), `derivation-steps`, `sim-runner` | Trap: "expected $n \log n$" means "on random inputs" (the randomness is in the pivots, so the bound holds for every input, an adversary's included). Edge: for $n = 4$ the exact expectation is $\frac{29}{6}$; the leading term $2n \ln n \approx 1.39 n \log_2 n$ is approached slowly (the ratio is 1.24 at $n = 10^6$) | N, O, X, C |
| 18 | `lsn.algcost.lower-bound` The comparison lower bound | Prove with a decision tree that any comparison sort needs $\lceil \log_2 n! \rceil$ comparisons in the worst case, and estimate $\log_2 n!$ | Can any method sort 3 items with at most 2 comparisons? (no: 6 orders need $\lceil \log_2 6 \rceil = 3$) | `sort-lab` (bound), `node-link` (decision tree), `derivation-steps` | Trap: "a cleverer comparison sort could beat $n \log n$". Edge: 4 items need 5 comparisons, 1,000 items 8,530; the bound says nothing about sorts that do not compare (lesson 19) | N, N, C, O |
| 19 | `lsn.algcost.linear-sorts` Sorting without comparisons | Sort integer keys with counting and radix sort, state their costs $O(n + k)$ and $O(d(n + b))$, and explain why radix sort needs a stable digit sort | Sort 1,000,000 trade sizes that are whole lots from 1 to 100. Faster than $n \log n$? (yes: count each size) | `sort-lab` (buckets) | Trap: counting sort is always linear (it is linear in $n + k$; keys up to $10^9$ make it worse than sorting). Edge: least-significant-digit radix sort fails with an unstable digit sort; keys of different lengths | C, N, O, M |

Transfer screens: lesson 14 repairs a slightly out-of-order tick file; lesson 15 measures how far a model's ranking of stocks is from the realised ranking; lesson 19 sorts trade sizes and price ticks, which are small integers.

**Level AC4: Selection and Order in Practice** (`lvl.algcost.ordering`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 20 | `lsn.algcost.quickselect` Selection without sorting | Find the $k$th smallest element in expected linear time with quickselect, and choose between sorting, a heap and quickselect | The median of 1,000,001 daily returns: must you sort them? (no: quickselect takes expected $O(n)$, about $(2 + 2\ln 2)n \approx 3.4n$ comparisons for the median) | `sort-lab` (quick, partition), `recursion-tree` | Trap: the median needs a full sort. Edge: median of medians gives worst-case $O(n)$ with a large constant; `heapq.nsmallest(k, xs)` is $O(n \log k)$; NumPy's `np.partition` uses introselect [recalled] | C, N, K, M |
| 21 | `lsn.algcost.custom-orders` Custom orders and comparators | Sort by a comparison that is not a key, with `functools.cmp_to_key`, and check that it is a valid order: irreflexive, transitive and consistent with equality | Arrange [3, 30, 34, 5, 9] to form the largest number ("9534330"). Why must "3" come before "30"? ("330" is larger than "303") | `sort-lab` (key), `code-blanks`, `counterexample-lab` (claim) | Trap: sorting by numeric value or by plain string order (both put 30 or 34 in the wrong place). Edge: a comparator that is not transitive makes the result depend on the algorithm (1.9 lesson 58 shows the crash); all zeros must print "0" | T, K, C, N |
| 22 | `lsn.algcost.sorting-first` Sorting as the first move | Recognise problems that sorting turns from quadratic into $n \log n$: duplicates, closest pair on a line, overlaps, matching | Do any two of 100,000 orders share a timestamp? Compare every pair, or sort and compare neighbours? (4,999,950,000 comparisons against about $1.7 \times 10^6$ for the sort plus 99,999) | `sort-lab`, `complexity-lab` (race), `code-cell` | Trap: sorting destroys information still needed (carry the original index with each item). Edge: a hash set answers "any duplicate?" in $O(n)$ but not "the closest pair" | M, N, K, C |
| 23 | `lsn.algcost.external-sorting` Sorting more than fits in memory | Plan an external merge sort for data larger than memory, and use partial or streaming sorts when only the top items or a merge are needed | Sort 200 GB of tick files on a machine with 16 GB of memory, sorting 10 GB at a time. Sorted runs, and merge passes? (20 runs; one 20-way merge with a heap) | `sort-lab` (merge), `heap-lab` (k-merge, preview) | Trap: "load it all and call sort". Edge: Python's sort (Timsort) is stable and detects existing runs, so already sorted data takes $O(n)$ [recalled]; `key=` is faster than `cmp_to_key` | N, N, C, O |

Transfer screens: lesson 20 computes a daily median spread; lesson 22 checks a trade file for duplicate fills; lesson 23 sorts a year of tick data, the first step of 2.3 project 4.

#### Course AH: Arrays, Hashing and Pointers (`crs.arrayhash`, 6 levels, 33 lessons)

The patterns that solve most array and string problems in linear or near-linear time: hash tables and what they cost, two pointers, sliding windows, prefix sums, binary search on data and on answers, and interval sweeps. It covers the NeetCode categories arrays and hashing, two pointers, sliding window, binary search and intervals. Grokking chapters 1 and 5 and 6.006 lectures 2 and 4 run alongside.

**Level AH1: Arrays and Hash Tables** (`lvl.arrayhash.hashing`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 24 | `lsn.arrayhash.array-memory` Arrays in memory | Compute an element's address from its index, explain why indexing is $O(1)$ and front insertion $O(n)$, and contrast a Python list (pointers) with a NumPy array (values) | An array of 8-byte floats starts at address 1,000. Where is element 37? (1,296) | `memory-layout` (array, python), `array-strip`, `dynamic-array` | Trap: a Python list stores its floats side by side (it stores pointers to separate float objects, one reason a loop over a list is slower than NumPy). Edge: deleting from the middle shifts the tail; 1.1 lesson 28's table of costs is assumed | N, C, M, N |
| 25 | `lsn.arrayhash.hash-tables` Hash tables and chaining | Insert keys into a chained hash table, compute the load factor $\alpha = n/m$, and derive the expected chain length $1 + \alpha$ for a lookup | 1,000 order ids hash uniformly into 10,000 buckets. Expected colliding pairs? ($\binom{1000}{2}/10{,}000 = 49.95$) How many buckets keep it below 1? (more than 499,500) | `hash-table` (chaining, predict-bucket), `live-formula` | Trap: hash lookups are $O(1)$ in the worst case (all keys in one bucket gives $O(n)$; the guarantee is on average under a good hash). Edge: resizing doubles the buckets and rehashes every key, amortised $O(1)$ per insert (lesson 4); the collision count is 1.5 lesson 54's indicator argument | N, N, C, M |
| 26 | `lsn.arrayhash.open-addressing` Open addressing | Insert, look up and delete under linear probing, explain clustering and tombstones, and predict how probe counts rise with the load factor | Key C was placed after colliding with key B. Delete B by emptying its slot, then look up C. What happens? (the search stops at the hole and reports C missing) | `hash-table` (linear, quadratic) | Trap: deleting by emptying the slot (mark a tombstone instead). Edge: a failed search under linear probing costs about $\frac12\left(1 + \frac{1}{(1 - \alpha)^2}\right)$ probes [recalled], 2.5 at $\alpha = 0.5$ and about 50 at 0.9 (a 20,011-slot simulation gave 2.5 and 43 [verified]); CPython's dict uses open addressing [recalled] | G, N, C, M |
| 27 | `lsn.arrayhash.hash-patterns` Hashing patterns: complements, counts, groups | Solve pair, count and grouping problems in one pass with a dictionary: complement lookup, frequency counts and grouping by a signature | 100,000 trades: two whose notionals sum to exactly £1,000,000? All pairs is about $5 \times 10^9$ checks; which one-pass method takes $10^5$? (look up each trade's complement in a dictionary of earlier notionals) | `hash-table`, `array-strip`, `code-cell` | Trap: storing the current value before looking up its complement (a £500,000 trade pairs with itself). Edge: duplicates; several valid pairs; grouping anagrams by sorted letters ($O(k \log k)$ per word) or by a 26-count tuple ($O(k)$) | T, K, C, K |
| 28 | `lsn.arrayhash.consecutive-runs` Sets and consecutive runs | Find the longest run of consecutive integers in $O(n)$ by scanning only from values whose predecessor is absent, and prove the total work is linear | Day numbers with a trade: [100, 4, 200, 1, 3, 2]. Longest run of consecutive days? (4: days 1 to 4) | `hash-table` (set), `array-strip`, `complexity-lab` (race) | Trap: scanning upwards from every value (quadratic on one long run), or assuming sorting is needed. Edge: duplicates; negative values; an empty list gives 0 | N, C, K, M |
| 29 | `lsn.arrayhash.keys-encodings` Designing keys and encodings | Build hashable keys for composite facts (tuples, frozensets, canonical forms) and design a string encoding that always decodes | Is a 9 × 9 grid a valid Sudoku? One set of keys such as `(r, d)`, `(c, d)` and `((r // 3, c // 3), d)` answers it. Then: join a list of strings into one string that always splits back, even when the strings contain commas | `hash-table`, `code-cell`, `counterexample-lab` (claim) | Trap: joining with a separator (["a,b"] and ["a", "b"] both become "a,b"; a length prefix such as `3#abc` cannot be confused). Edge: lists are not hashable; a canonical form must give equal objects identical keys | M, K, C, T |

Transfer screens: lesson 25 sizes a hash table for a day's order ids; lesson 27 reconciles trades against a target notional; lesson 29 encodes a list of option symbols into one message field.

**Level AH2: Two Pointers** (`lvl.arrayhash.pointers`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 30 | `lsn.arrayhash.opposite-pointers` Two pointers from both ends | Find a pair with a target sum in a sorted array in $O(n)$, and show on the pair grid that each move discards only pairs that cannot be the answer | Sorted strikes [80, 85, 90, 95, 100, 110, 120]: two summing to 195? (85 and 110, after 3 checks; the first move rules out all 6 pairs containing 120) | `pointer-walk` (opposite, pairs) | Trap: moving either pointer arbitrarily (the answer can be skipped). Edge: no pair exists; duplicates; a palindrome check that skips punctuation | G, N, C, K |
| 31 | `lsn.arrayhash.container-water` Moving the shorter side | Maximise $\min(h_i, h_j)(j - i)$ in $O(n)$ by always moving the shorter side, and prove the move safe with an exchange argument | Heights [1, 8, 6, 2, 5, 4, 8, 3, 7]: the largest container? (49, between the 8 at index 1 and the 7 at index 8) | `pointer-walk` (opposite, pairs) | Trap: moving the taller side, or both sides. Edge: equal heights (either move is safe); the argument is the exchange argument of greedy algorithms (lesson 133) | N, G, C, M |
| 32 | `lsn.arrayhash.three-sum` Three-sum and de-duplication | Find all distinct triples summing to zero in $O(n^2)$ by sorting and running two pointers from each first element, skipping duplicates | Daily P&L changes [-1, 0, 1, 2, -1, -4]: which distinct triples cancel out? ([-1, -1, 2] and [-1, 0, 1]) | `pointer-walk`, `code-cell` | Trap: three nested loops into a set of tuples ($O(n^3)$), or skipping the second pointer's duplicates before recording a triple. Edge: [0, 0, 0, 0] gives exactly one triple | O, K, C, T |
| 33 | `lsn.arrayhash.same-direction` Same-direction pointers and partitions | Compact, filter and partition arrays in place with a write pointer and a read pointer, including the three-way Dutch national flag partition | Order sides coded 0 (sell), 1 (cancel) and 2 (buy): sort [2, 0, 2, 1, 1, 0] in one pass with three pointers | `pointer-walk` (same, flag) | Trap: advancing the middle pointer after swapping with the high one (the swapped-in value is unexamined). Edge: all one value; quicksort's partition (lesson 16) is the two-way version | G, T, C, K |
| 34 | `lsn.arrayhash.trapping-water` Prefix maxima and trapped water | Compute the water held between bars as $\sum_i \min(L_i, R_i) - h_i$ with prefix and suffix maxima, then in $O(1)$ space with two pointers | Bars [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]: units of water? (6) | `pointer-walk` (opposite), `array-strip` (bars), `range-query-lab` (prefix) | Trap: bounding the water by the nearest taller bar instead of the tallest bar on each side. Edge: monotone bars hold nothing; the running maximum is 1.1 lesson 15's, and the area under a price's running maximum is this sum | N, G, C, K |

Transfer screens: lesson 30 pairs option strikes for a spread at a target width; lesson 32 finds three positions whose P&L nets to zero; lesson 34 measures the total "underwater" area of a fund's equity curve.

**Level AH3: Sliding Windows** (`lvl.arrayhash.windows`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 35 | `lsn.arrayhash.fixed-window` Fixed windows and the best single trade | Update a window statistic in $O(1)$ a step instead of recomputing it, and find the best buy-then-sell trade with a running minimum | Prices [7, 1, 5, 3, 6, 4]: best profit from one buy followed by one sell? (5). Then: twenty-day sums over 2,520 days, recomputed or updated? (50,020 additions against 5,020) | `pointer-walk` (window-fixed), `array-strip` | Trap: recomputing each window from scratch ($O(nk)$). Edge: $k > n$; prices that only fall give 0; this is 1.1 lesson 15's drawdown loop mirrored (the largest rise, not the largest fall) | N, N, C, K |
| 36 | `lsn.arrayhash.count-windows` Windows of counts | Decide whether a window is a rearrangement of a pattern by keeping count tables, updated in $O(1)$ a step | Every start of a scrambled "abc" in "cbaebabacd"? (indices 0 and 6) | `pointer-walk` (window-fixed), `hash-table` (counts) | Trap: sorting every window ($O(nk \log k)$). Edge: pattern longer than the text; tracking the number of matching letters avoids comparing 26 counts each step | N, R, C, K |
| 37 | `lsn.arrayhash.rolling-hash` Rolling hashes | Update a polynomial hash of a sliding window in $O(1)$ and find repeated substrings with it, confirming matches because hashes collide | Every 10-letter block that occurs more than once in a 100,000-letter symbol log, without comparing all pairs of blocks | `pointer-walk` (window-fixed), `hash-table`, `live-formula` | Trap: equal hashes mean equal strings (collisions happen: compare the substrings, or use two moduli). Edge: the window hash $\sum_i c_i b^{k - 1 - i} \bmod p$ rolls by removing the outgoing letter times $b^{k - 1}$; Python's unbounded integers hide the overflow C++ would hit | X, C, M, K |
| 38 | `lsn.arrayhash.variable-window` Variable windows and their invariant | Grow a window on the right and shrink it on the left while an invariant fails, for the longest substring without repeats and the longest run fixable by $k$ replacements | Longest stretch of "abcabcbb" with no repeated symbol? (3) In "abba"? (2, where a stale last-seen index bites) | `pointer-walk` (window-variable), `hash-table` | Trap: moving `left` back to a stale earlier position (always take the larger). Edge: for $k$ replacements a window is valid while its length minus its top count is at most $k$, and the top count need not decrease when shrinking ("AABABBA" with $k = 1$ gives 4) | N, N, C, K |
| 39 | `lsn.arrayhash.minimum-window` The minimum window | Find the shortest window holding every required item with multiplicity, expanding until valid and shrinking while still valid | Shortest stretch of "ADOBECODEBANC" containing A, B and C? ("BANC") | `pointer-walk` (window-variable), `hash-table` | Trap: shrinking with `if` instead of `while` (the window is not minimal). Edge: repeated requirements ("AA" needs two A's); no valid window returns "" | T, G, C, K |
| 40 | `lsn.arrayhash.monotonic-deque` The sliding window maximum | Keep the maximum of every window of size $k$ in $O(n)$ with a deque of indices whose values decrease | With $k = 3$ on [1, 3, -1, -3, 5, 3, 6, 7], the window maxima? ([3, 3, 5, 5, 6, 7]) | `stack-queue-lab` (monotonic-deque), `pointer-walk` | Trap: storing values instead of indices (the front's expiry cannot be detected), or a heap ($O(n \log n)$ with stale entries). Edge: equal values (pop with `<=` consistently); $k = 1$ | T, G, C, K |

Transfer screens: lesson 35 computes a 20-day moving average and the best trade of a year; lesson 37 finds repeated order patterns in a message log; lesson 40 computes a rolling 20-day high for a breakout rule, the same job pandas' `rolling(20).max()` does (1.1 course D).

**Level AH4: Prefix Sums** (`lvl.arrayhash.prefix`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 41 | `lsn.arrayhash.prefix-sums` Prefix sums and range queries | Answer any range-sum query in $O(1)$ after an $O(n)$ pass, with a prefix array of length $n + 1$ and half-open ranges | Daily P&L over 10 days and 10 questions "P&L from day $l$ to day $r$": add up each range, or subtract two prefix values? | `range-query-lab` (prefix, prefix-2d) | Trap: an inclusive range $[l, r]$ is $P[r] - P[l]$ (it is $P[r + 1] - P[l]$). Edge: empty ranges give 0; a rectangle sum from four corners of a 2D prefix table | N, X, C, K |
| 42 | `lsn.arrayhash.subarray-target` Prefix sums with a hash map | Count subarrays summing to $k$ in $O(n)$ by counting earlier prefix sums equal to the current one minus $k$ | Changes [1, 2, 3, -2, 2]: how many contiguous stretches sum to exactly 3? (4) | `range-query-lab` (prefix), `hash-table` | Trap: a sliding window (with negative values, shrinking no longer lowers the sum), or forgetting the empty prefix, `count[0] = 1`. Edge: $k = 0$ on [1, -1, 1, -1] gives 4 | N, C, K, T |
| 43 | `lsn.arrayhash.prefix-products` Prefix and suffix products | Compute each position's product of all the others without division, from prefix and suffix products | Growth factors [2, 0, 3, 4]: for each day, the growth over all other days? ([0, 24, 0, 0]) Why does "divide the total" fail? (a zero) | `range-query-lab` (prefix), `array-strip` | Trap: dividing the total product (breaks on zeros and loses precision). Edge: one zero leaves one non-zero answer; two zeros give all zeros | T, N, C, K |
| 44 | `lsn.arrayhash.difference-arrays` Difference arrays for range updates | Apply many range updates in $O(1)$ each by writing $+v$ at $l$ and $-v$ at $r$, then rebuild with one prefix pass | 1,000 block bookings each add seats over a range of a 365-day calendar. Update every day of every range, or mark the two ends? | `range-query-lab` (difference) | Trap: placing the closing $-v$ at $r$ for an inclusive range (it goes at $r + 1$). Edge: an update ending on the last day needs an array of length $n + 1$ | N, G, C, K |
| 45 | `lsn.arrayhash.kadane` The best stretch of returns | Find the maximum-sum contiguous subarray in $O(n)$, derived as the best single trade on the prefix-sum series | Daily returns in % [2, -3, 4, -1, 2, 1, -5, 4]: the best stretch to have held? (6%, days 3 to 6) Why is this lesson 35 in disguise? (the best trade on cumulative returns) | `range-query-lab` (prefix), `dp-table` (running) | Trap: restarting when the current element is negative (restart when the running sum is), or returning 0 for all-negative data when a non-empty stretch is required (the answer is the largest element: $-1$ for [-3, -1, -2]). Edge: whether the empty stretch is allowed is stated | N, C, X, K |

Transfer screens: lesson 41 answers P&L-between-dates queries for a dashboard; lesson 42 counts periods with a target cumulative return; lesson 45 finds a strategy's best holding period on log returns, which add over time (0.3 lesson 57).

**Level AH5: Binary Search** (`lvl.arrayhash.binsearch`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 46 | `lsn.arrayhash.binary-search-invariant` Binary search that always ends | Write binary search with an explicit invariant on a half-open range, and show every iteration shrinks the range | This search hangs on [3, 5] looking for 5: inside `while lo < hi`, it sets `mid = (lo + hi) // 2`, then `lo = mid` if `a[mid] < x`, else `hi = mid`. Why? (once `hi = lo + 1`, `mid = lo`, and `lo = mid` changes nothing) | `binary-search-lab` (conventions), `code-blanks` | Trap: mixing closed and half-open conventions. Edge: empty array; target absent; two elements; Stage 0's halving count (0.2 lesson 108, 0.3 G lesson 49) is assumed | T, G, C, K |
| 47 | `lsn.arrayhash.bounds` Lower and upper bounds | Use `bisect_left` and `bisect_right` for first and last positions, counts and as-of lookups in sorted timestamps | Quotes at 9:30, 9:31, 9:35 and 9:40. Which quote was live at 9:33? (the 9:31 quote, at `bisect_right(ts, t) - 1`) | `binary-search-lab` (bounds) | Trap: `bisect_right` returns the matching element's index (it returns the position after the last match). Edge: a time before the first quote; [1, 2, 2, 2, 3] gives bounds 1 and 4 for the value 2; pandas' `merge_asof` (1.1 course D) is this search | N, N, C, K |
| 48 | `lsn.arrayhash.answer-search` Binary search on the answer | Search a monotone yes-or-no predicate over the space of answers, with bounds chosen so the answer lies inside | Ship packages weighing 1 to 10 in order within 5 days: the smallest daily capacity? (15). Then: the volatility that makes a 1-year at-the-money call on 100 at 5% worth 12.00 (0.2411, after 23 halvings to a width of $10^{-6}$) | `binary-search-lab` (predicate) | Trap: a lower bound below the heaviest package, or a predicate that is not monotone. Edge: real-valued searches stop after a fixed number of halvings; the Black-Scholes call price rises with volatility, which is why bisection always finds implied volatility | N, N, C, K |
| 49 | `lsn.arrayhash.rotated-search` Rotated sorted arrays | Find the minimum of and search in a rotated sorted array in $O(\log n)$ by deciding which half is sorted | [4, 5, 6, 7, 0, 1, 2]: where is the smallest value? (index 4) | `binary-search-lab` (rotated) | Trap: comparing with `a[lo]` and stepping onto the wrong half when the range is not rotated. Edge: duplicates ([3, 1, 3, 3, 3]) force a linear worst case; an array that is not rotated | N, G, C, K |
| 50 | `lsn.arrayhash.matrix-search` Searching in two dimensions | Search a fully sorted matrix as one array of length $mn$, and a row- and column-sorted matrix by a staircase walk in $O(m + n)$ | Is 16 in a 4 × 4 matrix whose rows and columns are sorted? Start at the top-right corner and step left or down | `binary-search-lab` (matrix), `cell-grid` | Trap: treating a row- and column-sorted matrix as fully sorted. Edge: index $k$ is row $k \,//\, c$, column $k \bmod c$; empty rows | G, N, C, K |
| 51 | `lsn.arrayhash.median-two-arrays` Median of two sorted arrays | Find the median of two sorted arrays in $O(\log \min(m, n))$ by binary-searching a partition point | Sorted bid sizes [1, 3] and ask sizes [2]: the median without merging? (2) [1, 2] and [3, 4]? (2.5) | `binary-search-lab` (predicate), `array-strip` | Trap: binary-searching values rather than a partition index. Edge: one array empty; odd and even totals; $\pm\infty$ sentinels at the edges | N, N, C, K |

Transfer screens: lesson 47 is the point-in-time lookup behind every backtest join; lesson 48 computes implied volatility by bisection, which 2.3 project 3 needs; lesson 50 searches a sorted table of strikes and expiries.

**Level AH6: Intervals** (`lvl.arrayhash.intervals`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 52 | `lsn.arrayhash.merge-intervals` Merging intervals | Merge overlapping intervals after sorting by start, comparing each with the last merged interval | Trading halts [1, 3], [2, 6], [8, 10], [15, 18]: the merged halt periods? ([1, 6], [8, 10], [15, 18]) | `interval-sweep` (merge) | Trap: comparing with the previous input interval instead of the last merged one. Edge: whether touching intervals such as [1, 4] and [4, 5] merge is stated per problem (closed intervals: yes) | G, T, C, K |
| 53 | `lsn.arrayhash.insert-interval` Inserting an interval | Insert an interval into a sorted non-overlapping list in $O(n)$ in three phases: before, overlapping, after | Add the halt [4, 8] to [1, 2], [3, 5], [6, 7], [8, 10], [12, 16] (gives [1, 2], [3, 10], [12, 16]) | `interval-sweep` (insert) | Trap: stopping after the overlap phase and dropping the rest. Edge: the new interval before or after all others; an empty list | T, G, C, K |
| 54 | `lsn.arrayhash.interval-scheduling` Scheduling the most intervals | Choose the largest set of non-overlapping intervals by earliest end, and prove it optimal by an exchange argument | Five meeting requests for one room: does shortest first, earliest start or earliest end book the most? (earliest end) | `interval-sweep` (schedule, exchange), `counterexample-lab` (greedy) | Trap: shortest first or earliest start (each has a counterexample the learner builds). Edge: the fewest removals that leave no overlap is $n$ minus this maximum ([1, 2], [2, 3], [3, 4], [1, 3] needs 1) | C, R, O, K |
| 55 | `lsn.arrayhash.meeting-rooms` Counting overlaps with a sweep | Find the largest number of overlapping intervals with a sorted sweep of +1 and −1 events, or a heap of end times | Order lifetimes [0, 30], [5, 10], [15, 20]: the most orders live at once? (2) | `interval-sweep` (rooms), `heap-lab` (panel) | Trap: handling a start before an end at the same instant for half-open intervals ([1, 5) and [5, 10) then count 2 instead of 1). Edge: zero-length intervals; the peak is the number of rooms, desks or margin slots needed | N, C, O, K |
| 56 | `lsn.arrayhash.interval-queries` Answering interval queries offline | Answer many "narrowest interval containing $q$" queries by sorting queries and intervals and sweeping with a heap | Ten price bands and five query prices: the narrowest band containing each price | `interval-sweep` (points), `heap-lab` | Trap: scanning every interval for every query ($O(nq)$). Edge: answers must come back in the queries' original order (carry indices); no band containing a price gives $-1$ | G, C, M, K |

Transfer screens: lesson 52 merges exchange halts and maintenance windows; lesson 55 counts the peak number of open orders, which sets a risk limit; lesson 56 assigns prices to fee bands.

#### Course SQ: Stacks, Lists and Heaps (`crs.linear`, 4 levels, 22 lessons)

Linear structures and priority queues, and the randomised structures that streams need. It covers the NeetCode categories stack, linked list and heap, plus reservoir sampling, shuffling, universal hashing and Bloom filters from MIT 6.046J's randomisation lectures. Grokking chapters 2 and 6 (queues) and 6.006 lecture 8 (heaps) run alongside.

**Level SQ1: Stacks** (`lvl.linear.stacks`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 57 | `lsn.linear.stacks-brackets` Stacks and matching brackets | Check bracket nesting with a stack in $O(n)$, and explain why counting each bracket type fails | Is `{[()()]}(` balanced? Is `([)]`? (no; no) | `stack-queue-lab` (brackets) | Trap: counting opens and closes per type (`([)]` passes the count). Edge: a closing bracket with an empty stack; brackets left over at the end | C, G, T, K |
| 58 | `lsn.linear.evaluate-expressions` Evaluating expressions with a stack | Evaluate Reverse Polish notation and get operand order and integer division right | ["4", "13", "5", "/", "+"]? (6) ["7", "-3", "/"] with division truncating towards zero? (−2, where Python's `//` gives −3) | `stack-queue-lab` (rpn) | Trap: popping the operands in the wrong order for `-` and `/`, or `//` (floors) where the task truncates (`int(a / b)`). Edge: negative operand tokens such as "-11"; 1.1 lesson 3's `//` with negatives is assumed | T, T, C, K |
| 59 | `lsn.linear.min-stack` Augmented stacks | Support push, pop and get-minimum in $O(1)$ by storing the running minimum with each element | Track the lowest price among quotes pushed and popped on a stack. Why does one `min` variable fail? (after popping the minimum the previous one is lost) | `stack-queue-lab` (min-stack) | Trap: a single minimum variable. Edge: equal minima pushed twice must both be stored | G, T, C, K |
| 60 | `lsn.linear.monotonic-stack` Monotonic stacks | Find each position's next greater element in $O(n)$ with a stack of unresolved indices, and justify the amortised bound | Closes [100, 98, 97, 99, 101, 96, 102]: for each day, how many days until a higher close? ([4, 2, 1, 1, 2, 1, 0]) | `stack-queue-lab` (monotonic-stack) | Trap: "the nested `while` makes it $O(n^2)$" (each index is pushed and popped once, at most $2n$ operations). Edge: strictly greater against greater or equal; days with no higher close get 0 | N, G, C, K |
| 61 | `lsn.linear.largest-rectangle` The largest rectangle in a histogram | Compute the largest rectangle under a histogram in $O(n)$, taking each popped bar's width from the bar now below it on the stack | Bars [2, 1, 5, 6, 2, 3]: largest rectangle? (10) | `stack-queue-lab` (monotonic-stack), `array-strip` (bars) | Trap: taking the width from the popped index rather than the new stack top. Edge: increasing bars [1, 2, 3, 4, 5] need a final sentinel of height 0 (the answer is 9) | N, G, C, K |

Transfer screens: lesson 60 is "days until the price recovers above today's close", a drawdown-duration statistic; lesson 61 finds the longest period a portfolio stayed above each level.

**Level SQ2: Queues and Linked Lists** (`lvl.linear.lists`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 62 | `lsn.linear.queues-ring-buffers` Queues, deques and ring buffers | Build a queue from two stacks with amortised $O(1)$ operations, and a fixed ring buffer that tells full from empty | A ring buffer of 8 slots holds the latest ticks; head and tail both point to slot 3. Full or empty? (it cannot tell without a count or a spare slot) | `stack-queue-lab` (ring, two-stacks) | Trap: `head == tail` means empty (it also means full). Edge: one two-stack dequeue can cost $O(n)$ but each element moves at most once; `collections.deque` gives $O(1)$ at both ends | C, G, N, K |
| 63 | `lsn.linear.linked-list-basics` Linked lists and the dummy head | Traverse, insert and delete in a singly linked list, with a dummy head so the first node needs no special case | Delete every cancelled order from a list of 6, the first one included | `linked-list-lab` (basics) | Trap: rewiring `curr.next` before saving the rest of the list (the tail is lost). Edge: deleting the head; a one-node list; an empty list | G, O, C, K |
| 64 | `lsn.linear.reverse-list` Reversing a list in place | Reverse a singly linked list iteratively with three pointers and recursively, and state each version's extra space | Reverse 1 → 2 → 3 → 4 by moving the `prev`, `curr` and `nxt` tags | `linked-list-lab` (reverse) | Trap: returning `head` (now the last node) instead of `prev`. Edge: an empty list; the recursive version uses $O(n)$ stack | O, G, T, K |
| 65 | `lsn.linear.fast-slow` Fast and slow pointers | Find the middle and detect a cycle with Floyd's two speeds, and prove that restarting one pointer from the head finds the cycle's start | A tail of 3 nodes leads into a cycle of 5. After how many steps do the pointers meet, and how many more steps from the head reach the cycle's start? (5; 3) | `linked-list-lab` (cycle) | Trap: reading `fast.next.next` without checking `fast` and `fast.next`. Edge: a cycle starting at the head; the duplicate in [1, 3, 4, 2, 2], found by treating values as next pointers (2) | N, N, C, K |
| 66 | `lsn.linear.merge-reorder` Merging, splicing and gaps | Merge two sorted lists by splicing, remove the $n$th node from the end with a gap of $n$, and reorder a list from both ends | Remove the 2nd node from the end of 1 → 2 → 3 → 4 → 5 in one pass | `linked-list-lab` (merge) | Trap: a gap off by one (start the leading pointer $n$ steps ahead of a dummy). Edge: $n$ equal to the length removes the head, which the dummy handles | G, T, C, K |
| 67 | `lsn.linear.copy-random-list` Copying linked structures | Deep-copy a list whose nodes carry a random pointer, mapping old nodes to new ones in a dictionary | Copy 3 nodes whose `random` pointers point backwards and to themselves | `linked-list-lab` (random-copy), `hash-table` | Trap: copying `random` as the old node (the copy points back into the original: 1.1 lesson 23's shallow copy in another form). Edge: `random` is `None`; a node pointing to itself | G, C, M, K |
| 68 | `lsn.linear.lru-cache` The LRU cache | Build a least-recently-used cache with $O(1)$ get and put from a dictionary and a doubly linked list | Capacity 2: put 1, put 2, get 1, put 3, get 2, put 4, get 1, get 3, get 4. Which keys are evicted? (2, then 1) | `linked-list-lab` (lru), `hash-table` | Trap: a singly linked list (removing a middle node is $O(n)$), or not moving a key to the front when it is updated. Edge: capacity 1; `OrderedDict.move_to_end` does the same job | G, N, C, K |

Transfer screens: lesson 62 keeps the last $k$ ticks in a ring buffer; lesson 66 merges two sorted lists of fills; lesson 68 caches recent instrument reference data.

**Level SQ3: Heaps** (`lvl.linear.heaps`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 69 | `lsn.linear.binary-heap` Binary heaps | Push to and pop from a binary heap stored in an array, with parent $\lfloor (i - 1)/2 \rfloor$ and children $2i + 1$ and $2i + 2$ | Push 5, 3, 8, 1, 9, 2 into an empty min-heap. The array? ([1, 3, 2, 5, 9, 8]) | `heap-lab` (push, pop) | Trap: sifting down towards the larger child of a min-heap. Edge: a heap is not sorted (only the root is known); a heap of $10^6$ items has height 19 | T, G, C, N |
| 70 | `lsn.linear.heapify` Heapify in linear time | Build a heap bottom-up in $O(n)$ by summing the work per level, and sort with it | Heapify [9, 4, 7, 1, 8, 2, 6, 3, 5] (gives [1, 3, 2, 4, 8, 7, 6, 9, 5]). Why is this cheaper than nine pushes? | `heap-lab` (heapify, sort) | Trap: "heapify is $n \log n$" (most nodes sit near the bottom: $\sum_h \frac{n}{2^{h + 1}} h < n$). Edge: heap sort is in place but not stable | T, X, C, N |
| 71 | `lsn.linear.top-k` The top $k$ | Keep the $k$ largest of a stream in $O(n \log k)$ with a min-heap of size $k$, and compare with sorting and with bucket counts | The 10 largest trades among 50 million, without storing them all | `heap-lab` (top-k) | Trap: a max-heap for the $k$ largest (a min-heap of size $k$ evicts the smallest of the current top). Edge: the top $k$ most frequent symbols by bucket counts in $O(n)$; ties at the boundary | C, T, N, K |
| 72 | `lsn.linear.k-way-merge` Merging $k$ sorted streams | Merge $k$ sorted lists in $O(N \log k)$ with a heap of their heads | Merge three exchanges' timestamped trade feeds into one ordered tape | `heap-lab` (k-merge) | Trap: pushing records that cannot be compared (add a sequence number: `(ts, seq, record)`). Edge: empty feeds; `heapq.merge` is the library version | O, C, T, K |
| 73 | `lsn.linear.running-median` The running median | Keep the median of a stream with a max-heap of the lower half and a min-heap of the upper half | Spreads arrive 5, 15, 1, 3, 2, 8: the median after each? (5, 10, 5, 4, 3, 4) | `heap-lab` (median) | Trap: pushing to one heap without rebalancing, so the halves drift apart in size. Edge: even counts average the two tops; Python's `heapq` is a min-heap, so the lower half stores negated values | N, G, C, K |
| 74 | `lsn.linear.order-book` A limit order book from heaps | Keep the best bid and best ask with two heaps keyed by price and time, cancelling lazily | Bids and asks arrive and some are cancelled. Which order is best after each event? | `heap-lab` (max-trick), `value-table` | Trap: removing a cancelled order from inside a heap (`heapq` cannot find it in $O(\log n)$: mark it and discard it when it reaches the top). Edge: price-time priority needs (price, time) keys with bid prices negated; an order that crosses trades at once; 1.7 teaches the book itself | G, T, C, K |

Transfer screens: lesson 71 finds the day's largest trades; lesson 72 builds a consolidated tape; lesson 74 is the core of the Order Book project (`prj.alg.order-book`, section 3.4).

**Level SQ4: Randomised Structures and Streams** (`lvl.linear.random`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 75 | `lsn.linear.reservoir` Reservoir sampling | Sample $k$ items uniformly from a stream of unknown length in one pass, and prove by induction that each item ends in the sample with probability $\frac{k}{n}$ | Keep a uniform sample of 100 trades from a day's feed whose length is known only at the close | `sim-runner`, `derivation-steps`, `code-cell` | Trap: replacing with a fixed chance such as $\frac12$, or with $\frac1i$ when $k > 1$ (item $i$, counted from 1, enters with chance $\frac{k}{i}$). Edge: a stream shorter than $k$ | X, O, C, K |
| 76 | `lsn.linear.shuffling` Shuffling correctly | Shuffle with Fisher-Yates and prove by counting that "swap each position with any position" is biased | Shuffle 3 cards by swapping each position with a random one of all 3. Are the 6 orders equally likely? (no: 27 equally likely runs cannot split evenly into 6; three orders arise from 4 runs and three from 5) | `counterexample-lab` (claim), `sim-runner` | Trap: "every swap is random, so the result is uniform". Edge: Fisher-Yates draws $j$ from $[i, n)$; excluding $i$ itself gives only single cycles (Sattolo's algorithm) | N, C, M, K |
| 77 | `lsn.linear.universal-hashing` Hashing against an adversary | Explain why any fixed hash can be attacked, how a hash chosen at random from a universal family bounds collisions by $\frac1m$, and why Python randomises string hashes | An attacker sends 50,000 order ids chosen to land in one bucket. How long does each lookup take now? | `hash-table` (adversarial keys), `complexity-lab` (race) | Trap: "a good hash function is enough" (every fixed function has bad inputs; the protection is a random choice the attacker cannot see). Edge: `PYTHONHASHSEED` fixes the seed for reproducible runs; CPython hashes small integers to themselves, so integer keys are not randomised [recalled] | C, N, M, T |
| 78 | `lsn.linear.bloom-filters` Bloom filters | Size a Bloom filter for a target false-positive rate with $(1 - e^{-kn/m})^k$, and choose one where a set will not fit in memory | Screen 100 million order ids against a blocklist in 120 MB. With 10 bits per id and 7 hash functions, how often is a clean id flagged? (about 0.8%) | `bit-lab`, `live-formula`, `sim-runner` | Trap: a Bloom filter can miss a member (it never gives false negatives, only false positives). Edge: a plain Bloom filter cannot delete; the best $k$ is $\frac{m}{n} \ln 2 \approx 6.9$ at 10 bits per item | N, C, N, M |

Transfer screens: lesson 75 samples trades for a manual audit; lesson 76 shuffles a dataset before a train-test split (2.1); lesson 77 explains why a public-facing order gateway must not use a predictable hash; lesson 78 screens ids against a sanctions list.

#### Course TG: Trees and Graphs (`crs.treesgraphs`, 5 levels, 31 lessons)

Binary trees and their recursions, search trees, tries, graph traversal, weighted shortest paths, union-find, spanning trees, all-pairs paths and the graph models hidden in other problems. It covers the NeetCode categories trees, tries, graphs and advanced graphs. Grokking chapters 6 to 9 and 6.006 lectures 6, 7 and 9 to 14 run alongside.

**Level TG1: Binary Trees** (`lvl.treesgraphs.binary-trees`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 79 | `lsn.treesgraphs.tree-recursion` Trees and recursion on trees | Compute height, size and sums of a binary tree by combining the answers of the two subtrees | Annotate every node of a 9-node tree with its height, bottom-up | `tree-lab` (recursion) | Trap: mixing the two height conventions (the app counts edges: a leaf has height 0 and the empty tree $-1$). Edge: a skewed tree of 10,000 nodes overflows Python's recursion limit | N, G, C, K |
| 80 | `lsn.treesgraphs.traversals` Pre-order, in-order, post-order and level order | Produce all four traversal orders, implement level order with a queue that records level sizes, and in-order with an explicit stack | Tap a 7-node tree's nodes in each order. Which order prints a search tree in sorted order? (in-order) | `tree-lab` (traversal), `stack-queue-lab` | Trap: level order without recording each level's size (levels merge). Edge: iterative traversals avoid the recursion limit | O, O, C, K |
| 81 | `lsn.treesgraphs.returns-records` What a call returns and what it records | Separate the value a recursive call returns to its parent from the best value it records globally, for the diameter, balance and maximum path sum | The longest path between two nodes of a 7-node tree. Why is returning the path through each node wrong? (a parent can extend only one branch) | `tree-lab` (recursion: returns and records), `recursion-tree` | Trap: returning the path through the node. Edge: negative values in the maximum path sum (clip branches at 0); the balance check returns $-1$ to stop early | N, C, G, K |
| 82 | `lsn.treesgraphs.tree-comparison` Comparing and transforming trees | Decide whether two trees are equal, mirror images or one a subtree of the other, and invert a tree | Is a 3-node tree a subtree of a 7-node one? Compare serialisations: why must they include null markers? | `tree-lab` (serialise) | Trap: serialising without nulls (different shapes give the same string). Edge: equal values in different shapes; the empty tree is a subtree of every tree | C, T, M, K |
| 83 | `lsn.treesgraphs.construct-serialise` Building trees from traversals | Rebuild a tree from its pre-order and in-order traversals in $O(n)$ with a position map, and serialise and deserialise it | Pre-order [3, 9, 20, 15, 7], in-order [9, 3, 15, 20, 7]: draw the tree | `tree-lab` (construct, serialise) | Trap: searching the in-order list for each root ($O(n^2)$) instead of a dictionary of positions. Edge: duplicate values make the rebuild ambiguous; pre-order alone does not fix the shape | G, T, C, K |
| 84 | `lsn.treesgraphs.path-sums` Paths in trees | Count downward paths with a target sum in $O(n)$ with prefix sums on the root-to-node path, undoing counts on return | How many downward paths in a 10-node tree sum to 8? | `tree-lab` (recursion), `hash-table`, `range-query-lab` (prefix) | Trap: not decrementing a prefix count when the call returns (paths jump between branches). Edge: negative values; a one-node path; the right-side view and "good nodes" as quick variants | N, C, K, T |

Transfer screens: lesson 79 sums exposures up a fund-of-funds hierarchy; lesson 81 finds the longest chain in a dependency tree; lesson 84 counts sub-portfolios with a target P&L along a reporting tree.

**Level TG2: Search Trees and Tries** (`lvl.treesgraphs.search-trees`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 85 | `lsn.treesgraphs.bst-operations` Binary search trees | Search, insert and delete in a BST, including deleting a node with two children through its in-order successor | Delete the root of a 7-node BST. Which key replaces it? (its in-order successor) | `tree-lab` (bst) | Trap: replacing a node with two children by either child. Edge: deleting a leaf or a one-child node; equal keys need a stated rule | G, C, T, K |
| 86 | `lsn.treesgraphs.bst-validate` Validating and walking a BST | Validate a BST by passing an allowed interval down, find the $k$th smallest by an in-order walk, and find a lowest common ancestor by order | Every parent lies between its two children, yet 6 sits in the left subtree of 5. Valid? (no) | `tree-lab` (bst, lca) | Trap: checking each node only against its parent. Edge: start from $(-\infty, \infty)$; duplicate keys | C, N, G, K |
| 87 | `lsn.treesgraphs.balance` Balance | Show that inserting sorted keys turns a BST into a list, estimate a random BST's height, and explain how rotations restore balance | Insert 1 to 7 in order, then as 4, 2, 6, 1, 3, 5, 7. Levels? (7 against 3) For 1,000 keys in random order? (about 22 levels on average) | `tree-lab` (balance), `sim-runner` | Trap: "BST operations are $O(\log n)$" (only when the tree is balanced). Edge: a rotation preserves in-order; AVL trees keep height below about $1.44 \log_2 n$ [recalled] | N, N, C, M |
| 88 | `lsn.treesgraphs.ordered-maps` Ordered maps in practice | Choose between a sorted list with `bisect`, a balanced tree and a heap for an ordered set with inserts, deletes and nearest-key queries | Keep 100,000 price levels sorted while levels appear and vanish. Is `bisect.insort` $O(\log n)$? (the search is; the insert shifts the list, $O(n)$) | `tree-lab` (bst), `complexity-lab` (race) | Trap: `insort` is logarithmic. Edge: Python's standard library has no balanced tree (`sortedcontainers` is a third-party option); C++'s `std::map` is one (1.9 lesson 54); floor and ceiling queries | C, M, N, T |
| 89 | `lsn.treesgraphs.lca` Lowest common ancestors | Find the lowest common ancestor in any binary tree with one recursion that reports found nodes upwards | Two analysts in a 15-person reporting tree: their nearest common manager | `tree-lab` (lca) | Trap: using search-tree order on a tree that is not a BST. Edge: one node is the other's ancestor; a node absent from the tree | G, C, T, K |
| 90 | `lsn.treesgraphs.tries` Tries | Insert, search and count by prefix in a trie with an end-of-word mark, and support single-letter wildcards | How many of 12 ticker symbols start with "MS"? | `tree-lab` (trie) | Trap: no end-of-word mark ("app" is found after inserting only "apple"). Edge: the empty string; a wildcard branches into every child | N, C, G, K |

Transfer screens: lesson 88 keeps an order book's price levels ordered; lesson 90 autocompletes ticker symbols.

**Level TG3: Graphs and Traversal** (`lvl.treesgraphs.traversal`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 91 | `lsn.treesgraphs.graph-representations` Representing graphs | Convert a graph between drawing, edge list, adjacency list and matrix, and choose by density and the queries asked | 10,000 stocks with an edge where correlation exceeds 0.8, about 50,000 edges. Matrix or lists? (lists: $10^8$ cells against about $10^5$ entries) | `graph-search` (represent) | Trap: adding an undirected edge in one direction only. Edge: self-loops and parallel edges; degrees sum to twice the edge count; implicit graphs whose neighbours are computed | S, N, C, G |
| 92 | `lsn.treesgraphs.bfs` Breadth-first search | Run BFS for layers and shortest unweighted distances, marking nodes when they are queued | Fewest conversions from currency A to currency F on a 9-node graph of tradable pairs | `graph-search` (bfs) | Trap: marking a node visited when it is popped (it enters the queue twice). Edge: unreachable nodes stay at infinity; start equal to target | O, N, C, K |
| 93 | `lsn.treesgraphs.dfs` Depth-first search and components | Count connected components and flood-fill regions with DFS, recursively and with an explicit stack | Count the islands of land on a 4 × 5 grid (3) | `graph-search` (dfs, components), `cell-grid` | Trap: recursive DFS on a 1,000 × 1,000 grid in Python (a million-deep recursion: use a stack). Edge: whether diagonal cells touch is stated; the largest island's area | N, G, C, K |
| 94 | `lsn.treesgraphs.multi-source-bfs` Multi-source BFS | Compute each cell's distance from the nearest of many sources in one BFS by queueing all sources first | Rotting oranges: minutes until every orange on a 3 × 3 grid has rotted (4), or $-1$ if one cannot be reached | `graph-search` (multi-bfs), `cell-grid` | Trap: one BFS per source ($O(kV)$). Edge: unreachable cells; zero minutes when nothing is fresh | N, N, C, K |
| 95 | `lsn.treesgraphs.cycles` Detecting cycles | Detect cycles in undirected graphs (a visited neighbour that is not the parent) and directed graphs (an edge to a node still on the stack) | Four courses with prerequisites: can all be finished? If not, find the back edge | `graph-search` (cycle, dfs colours) | Trap: one `visited` set in a directed graph (an edge to a finished node looks like a cycle). Edge: self-loops; a connected graph with $n - 1$ edges is a tree | C, R, G, K |
| 96 | `lsn.treesgraphs.topological-sort` Topological sort | Order a DAG with Kahn's in-degree queue or reversed DFS finish times, and detect an impossible schedule | A nightly data job with steps 0 → 1, 0 → 2, 1 → 3, 2 → 3: every valid order? (two: 0, 1, 2, 3 and 0, 2, 1, 3) | `graph-search` (topo) | Trap: printing DFS finish order without reversing it. Edge: any valid order is accepted unless a tie rule is stated; fewer than $n$ nodes output means a cycle | O, N, C, K |
| 97 | `lsn.treesgraphs.bipartite-clone` Colouring, cloning and searching from the edges | Test bipartiteness by two-colouring, clone a graph with a dictionary of copies, and search backwards from borders | Can 6 traders be split into two desks so that each pair who must be separated sit apart? | `graph-search` (bipartite) | Trap: a search from every cell when one search from each border answers all cells (Pacific and Atlantic flow). Edge: a disconnected graph needs a new start per component; an odd cycle is never two-colourable | C, G, M, K |

Transfer screens: lesson 91 stores a correlation network; lesson 92 finds the fewest conversions between currencies; lesson 96 orders a nightly research pipeline; lesson 97 splits conflicting books across two desks.

**Level TG4: Weighted Graphs** (`lvl.treesgraphs.weighted`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 98 | `lsn.treesgraphs.dijkstra` Dijkstra's algorithm | Compute shortest paths with non-negative weights using a heap with lazy deletion of stale entries | The lowest-latency route for a market data packet across a 7-node network | `shortest-path` (dijkstra), `heap-lab` | Trap: settling a node when it is pushed rather than when it is popped. Edge: stale entries are skipped; unreachable nodes stay at infinity; the cost is $O((V + E) \log V)$ | O, N, C, K |
| 99 | `lsn.treesgraphs.dijkstra-correctness` Why Dijkstra works, and when it fails | Prove Dijkstra's greedy step by induction on the settled set, and build the three-node counterexample with a negative edge | A → B costs 2, A → C costs 3, C → B costs −2. What does Dijkstra report for B, and what is true? (2; 1) | `shortest-path` (negative), `derivation-steps` | Trap: adding a constant to every edge to remove negatives (it penalises paths with more edges, so the shortest path changes). Edge: zero-weight edges are fine; negative edges without cycles need Bellman-Ford | N, O, C, M |
| 100 | `lsn.treesgraphs.bellman-ford` Bellman-Ford and limited stops | Relax every edge $V - 1$ times, detect a negative cycle with one more round, and find the cheapest route with at most $k$ stops by relaxing from a copy of the previous round | The cheapest flight with at most 1 stop on a 4-city graph. Why does updating in place return a route with 2 stops? | `shortest-path` (bellman-ford) | Trap: updating in place in the $k$-stop version (one round can chain two edges). Edge: a negative cycle the source cannot reach does not matter; the cost is $O(VE)$ | N, G, C, K |
| 101 | `lsn.treesgraphs.currency-arbitrage` Currency arbitrage as a negative cycle | Turn exchange rates into weights $-\ln r$, so that a cycle whose rates multiply to more than 1 becomes a negative cycle, and find it with Bellman-Ford | USD → EUR at 0.92, EUR → GBP at 0.85, GBP → USD at 1.28: a profit loop? (yes: $0.92 \times 0.85 \times 1.28 = 1.00096$, a 0.096% gain before costs) | `shortest-path` (bellman-ford), `live-formula` | Trap: a "largest product" Dijkstra on the rates (a product above 1 behaves like a negative edge). Edge: a tolerance is needed because rounding pushes products of exactly 1 above 1; bid-ask spreads and fees remove nearly every such loop in practice | N, C, X, K |
| 102 | `lsn.treesgraphs.union-find` Union-find | Maintain components under edge additions with union by size and path compression, in near-constant amortised time | Add correlation links one at a time among 10 stocks. Clusters after each? Which link is the first redundant one? | `union-find` (rank, compress, redundant) | Trap: linking the two nodes instead of their roots. Edge: joining two nodes already together; path compression flattens the path for later finds; the inverse Ackermann bound is named, not proved | G, N, C, K |
| 103 | `lsn.treesgraphs.mst` Minimum spanning trees | Build a minimum spanning tree with Kruskal (sort and union-find) or Prim (heap), and prove the cut property | Cable 5 sites at points (0, 0), (2, 2), (3, 10), (5, 2), (7, 0) with Manhattan-distance costs: the cheapest network? (20) Then: the minimum spanning tree of 6 stocks with distance $\sqrt{2(1 - \rho)}$ | `shortest-path` (kruskal, prim, cut), `union-find` | Trap: the MST contains the shortest path between every pair (it does not). Edge: equal weights give several MSTs; a disconnected graph gives a forest; Mantegna's 1999 correlation tree is this construction [recalled citation] | N, R, C, K |

Transfer screens: lesson 98 routes market data; lesson 101 checks a matrix of quoted rates for arbitrage; lesson 102 groups stocks into correlation clusters; lesson 103 draws the correlation tree of a sector.

**Level TG5: Graph Techniques** (`lvl.treesgraphs.techniques`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 104 | `lsn.treesgraphs.dag-paths` Shortest and longest paths in a DAG | Find shortest and longest paths in a DAG in $O(V + E)$ by relaxing in topological order, and read off the critical path | A research pipeline of 6 tasks with durations and dependencies: the earliest finish time | `graph-search` (topo), `dp-table` (states) | Trap: longest paths by a negated Dijkstra on a graph with cycles (longest simple path is NP-hard in general). Edge: several sources; this is dynamic programming on a DAG (lesson 129) | N, R, C, K |
| 105 | `lsn.treesgraphs.state-space` Searching state spaces | Model a puzzle as an implicit graph of states and moves, search it with BFS, and halve the explored frontier with bidirectional search | "hit" to "cog", one letter at a time, through the list hot, dot, dog, lot, log, cog: fewest words? (5) | `graph-search` (implicit) | Trap: building edges by comparing every pair of words ($O(N^2 L)$) instead of generating each word's neighbours ($O(26 NL)$) or using wildcard buckets. Edge: a target missing from the list gives 0; forbidden states | N, C, M, K |
| 106 | `lsn.treesgraphs.minimax-paths` Bottleneck paths | Find the path whose largest weight is smallest, with Dijkstra on maximums or binary search plus BFS | Swim in rising water: the earliest time to cross a 5 × 5 grid of heights | `shortest-path` (dijkstra), `binary-search-lab` (predicate) | Trap: summing weights instead of taking the maximum. Edge: start equal to end; ties | N, C, G, K |
| 107 | `lsn.treesgraphs.all-pairs` All-pairs shortest paths | Compute all-pairs distances with Floyd-Warshall in $O(V^3)$ as a dynamic programme over intermediate nodes, and detect negative cycles on the diagonal | The best conversion rate between every pair of 5 currencies at once | `shortest-path` [mode to add: floyd-warshall], `cell-grid` (distance matrix) | Trap: putting the intermediate-node loop inside the other two (it must be outermost). Edge: a negative diagonal entry means a negative cycle; with non-negative weights on a sparse graph, $V$ runs of Dijkstra are faster | O, N, C, K |
| 108 | `lsn.treesgraphs.eulerian` Eulerian paths | Decide from degrees whether a path can use every edge once, and build it with Hierholzer's algorithm | Rebuild a trader's itinerary from a pile of 5 tickets, using each once, choosing the alphabetically smallest airport at each step | `graph-search` (euler) | Trap: a greedy depth-first walk that takes the smallest next airport gets stuck (append each airport on the way back, then reverse). Edge: repeated tickets on one route; a directed Eulerian path starts where out-degree exceeds in-degree by 1 | O, C, N, K |
| 109 | `lsn.treesgraphs.constraint-graphs` Graphs hidden in constraints | Build a graph from pairwise constraints, such as letter orders from a sorted dictionary in an unknown alphabet, and order it topologically | Words sorted in an unknown alphabet: wrt, wrf, er, ett, rftt. The letter order? ("wertf") | `graph-search` (topo) | Trap: missing the prefix rule ("abc" listed before "ab" is impossible). Edge: unconstrained letters can go anywhere; a cycle means no valid order | T, C, M, K |

Transfer screens: lesson 104 finds a research pipeline's critical path; lesson 107 computes best conversion rates between all currency pairs, the all-pairs form of lesson 101.

#### Course DP: Recursion, Dynamic Programming and Greedy (`crs.dynprog`, 7 levels, 41 lessons)

Search, then the two ways to avoid searching: remember subproblems (dynamic programming) or prove that one choice is always safe (greedy). Then bits and integer maths, what cannot be done fast, and the method for an unseen problem under a clock. It covers the NeetCode categories backtracking, 1-D and 2-D dynamic programming, greedy, maths and geometry and bit manipulation, plus the theory 6.006 lectures 15 to 19 and 6.046J's greedy and complexity lectures add. Grokking chapters 10 and 11 run alongside.

**Level DP1: Backtracking** (`lvl.dynprog.backtracking`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 110 | `lsn.dynprog.subsets` Subsets: choose or skip | Generate all $2^n$ subsets with a choose-or-skip recursion and with bitmasks, and skip duplicates after sorting | Every subset of three hedges (8), then of [1, 2, 2] without repeats (6) | `recursion-tree` (backtrack) | Trap: appending the working list itself to the results (every entry is one object, empty at the end: 1.1 lesson 1's aliasing again). Edge: the empty subset counts; duplicates are skipped by passing over equal neighbours at the same depth | N, T, C, K |
| 111 | `lsn.dynprog.permutations` Permutations | Generate permutations with a used-set, count them, and produce the next permutation in lexicographic order in place | The next arrangement after [1, 3, 5, 4, 2] in dictionary order? ([1, 4, 2, 3, 5]) | `recursion-tree` (permutations) | Trap: generating with duplicates and removing repeats afterwards ($n!$ work for few results). Edge: the last permutation wraps to the first ([3, 2, 1] to [1, 2, 3]); one empty permutation for $n = 0$ | T, N, C, K |
| 112 | `lsn.dynprog.combination-sum` Combination sums | Find all combinations reaching a target with and without reuse by passing a start index, and prune with sorting | Lot sizes [2, 3, 6, 7] reaching 7 lots, with reuse: which combinations? ([2, 2, 3] and [7]) | `recursion-tree` (combination-sum) | Trap: restarting from index 0 at every level (counts [2, 2, 3], [2, 3, 2] and [3, 2, 2] separately). Edge: target 0 gives one empty combination; sorting stops the loop once a candidate exceeds the remainder | R, T, C, K |
| 113 | `lsn.dynprog.n-queens` Pruning: N-Queens | Place $n$ queens using sets of used columns and diagonals ($r - c$ and $r + c$), and count how much pruning saves | Solutions for $n = 4$ and $n = 8$? (2 and 92) | `recursion-tree` (n-queens), `cell-grid` | Trap: checking conflicts only on a full board (searches $n^n$ boards). Edge: $n = 2$ and $n = 3$ have none; the counts for $n = 1$ to 8 are 1, 0, 0, 2, 10, 4, 40, 92 | N, G, C, K |
| 114 | `lsn.dynprog.grid-backtracking` Backtracking on grids and strings | Search a letter grid for a word by marking and unmarking cells, and split a string into palindromes | Is "ABCCED" spelled by adjacent cells of a 3 × 4 board? | `recursion-tree` (word-search), `cell-grid` | Trap: not unmarking a cell on return (later paths think it is used). Edge: a cell may not be reused; prune as soon as the next letter fails | G, C, M, K |
| 115 | `lsn.dynprog.generate-structures` Generating valid structures | Generate exactly the valid bracket sequences or keypad strings by tracking counts, and count them | Every balanced sequence of 3 bracket pairs (5); how many for 4? (14, the Catalan number of 1.5 lesson 138) | `recursion-tree` (backtrack) | Trap: generating all $2^{2n}$ strings and filtering (256 strings to keep 14 at $n = 4$). Edge: $n = 0$ gives one empty string; a closing bracket is allowed only while closes are fewer than opens | N, T, C, K |

Transfer screens: lesson 110 enumerates hedge subsets for a small portfolio; lesson 112 splits an order into allowed lot sizes; lesson 115 counts order sequences that never go short (the 1.5 ballot setting).

**Level DP2: From Recursion to Dynamic Programming** (`lvl.dynprog.foundations`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 116 | `lsn.dynprog.memoisation` Overlapping subproblems | Recognise repeated subproblems in a recursion tree and remove them with memoisation, turning exponential calls into linear | How many calls does the naive `fib(30)` make? (2,692,537) With a memo? (59 calls on 31 distinct subproblems) | `recursion-tree` (memo) | Trap: memoising on a list argument (unhashable) or on state that changes between calls. Edge: a deep memoised recursion still hits the recursion limit at $n = 10{,}000$; 1.1 lesson 21's stairs count is this recursion | N, N, C, K |
| 117 | `lsn.dynprog.bottom-up` Bottom-up tables | Define a state, a recurrence, a fill order and base cases, and fill the table from small to large, for the house robber | Collect fees from houses [2, 7, 9, 3, 1], never two neighbours: the best total? (12) | `dp-table` (1d) | Trap: base cases that do not match the state's meaning (with $dp[i]$ as "best from the first $i$ houses", $dp[0] = 0$ and $dp[1] = a_0$). Edge: one house; the table shrinks to two variables | N, X, C, K |
| 118 | `lsn.dynprog.coin-change` Coin change: fewest coins and counting ways | Compute the fewest coins for an amount and the number of combinations, and explain how loop order separates combinations from orderings | Coins {1, 3, 4}, amount 6: greedy uses 3 coins; the best? (2: 3 + 3). Ways to make 5 from {1, 2, 5}? (4 combinations, 9 orderings) | `dp-table` (1d), `counterexample-lab` (greedy) | Trap: the amount loop outside the coin loop when counting combinations (it counts orderings). Edge: amount 0 needs 0 coins; an unreachable amount returns $-1$; UK coins are canonical, so greedy is optimal for them (checked for every amount to £5.99) | N, N, C, K |
| 119 | `lsn.dynprog.decode-ways` Counting with constraints | Count the decodings of a digit string with a two-term recurrence that handles zeros | Ways to read "226" with A = 1 to Z = 26? (3) And "06"? (0) | `dp-table` (1d) | Trap: treating "0" as a letter, or "06" as 6. Edge: "10" and "20" read one way; long strings of 1s and 2s grow like the Fibonacci numbers | N, N, C, K |
| 120 | `lsn.dynprog.lis` Longest increasing subsequence | Find the LIS in $O(n^2)$ by DP and in $O(n \log n)$ with a tails array and binary search | Longest rising sequence of closes, not necessarily consecutive, in [10, 9, 2, 5, 3, 7, 101, 18]? (4) | `dp-table` (1d), `binary-search-lab` (LIS tops) | Trap: reading the tails array as the subsequence (it holds the right length, not in general a valid subsequence). Edge: strictly increasing uses `bisect_left`; non-decreasing uses `bisect_right` ([2, 2, 2] gives 1 against 3) | N, C, T, K |
| 121 | `lsn.dynprog.string-dp` Dynamic programming on strings | Decide word breaks with a prefix table, and count palindromic substrings by expanding around centres | Can "catsandog" be split into words from {cats, dog, sand, and, cat}? (no) | `dp-table` (1d) | Trap: greedy longest match (with {a, abc, b, cd}, "abcd" takes "abc" and fails, though "a", "b", "cd" works). Edge: "aaa" has 6 palindromic substrings; centres between letters give even lengths | N, C, N, K |

Transfer screens: lesson 118 makes a target lot size from allowed clip sizes; lesson 120 measures the longest run of rising closes; lesson 121 splits a concatenated symbol string into known tickers.

**Level DP3: Two-Dimensional DP** (`lvl.dynprog.two-d`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 122 | `lsn.dynprog.grid-paths` Paths through a grid | Count and optimise grid paths with a 2D table, with obstacles and costs | Moving only right or down on a 3 × 7 grid, how many paths? (28, which is $\binom{8}{2}$) With one obstacle? | `dp-table` (2d), `cell-grid` | Trap: forgetting that the first row and column have one path each, and none beyond an obstacle. Edge: an obstacle on the start; the binomial formula as a check | N, X, C, K |
| 123 | `lsn.dynprog.lcs` Longest common subsequence | Fill the LCS table over prefixes and trace back one longest subsequence | Trade-type sequences "abcde" and "ace": the longest common subsequence? (3) | `dp-table` (2d, reconstruct) | Trap: subsequence (gaps allowed) confused with substring (contiguous). Edge: an empty string; several optimal tracebacks | N, R, C, K |
| 124 | `lsn.dynprog.edit-distance` Edit distance | Compute the Levenshtein distance with insertions, deletions and replacements, and reconstruct the edits | "kitten" to "sitting": fewest edits? (3) | `dp-table` (2d, reconstruct) | Trap: an index off by one between string position $i - 1$ and table row $i$ (row $i$ means the first $i$ letters). Edge: the distance to the empty string is the other string's length | N, G, C, K |
| 125 | `lsn.dynprog.knapsack` Knapsack and subset sum | Solve 0/1 knapsack and subset sum with a capacity table, and with one row filled downwards | Weights [2, 3], values [3, 4], capacity 4: the best value? (4) The one-row table filled upwards says 6. Why? (it used the first item twice) | `dp-table` (space) | Trap: filling the one-row table upwards (that solves the unbounded knapsack). Edge: capacity 0; $O(nW)$ is pseudo-polynomial: exponential in the number of digits of $W$ (lesson 144) | N, C, T, K |
| 126 | `lsn.dynprog.trading-states` State-machine DP for trading | Model holding and not holding as states with transitions, for buying and selling with a cooldown, a fee, or at most $k$ round trips | Prices [1, 2, 3, 0, 2] with a one-day cooldown after each sale: the best profit? (3). With a fee of 2 on [1, 3, 2, 8, 4, 9]? (8) | `dp-table` (states) | Trap: allowing a buy the day after a sale, or a buy and sale on the same day. Edge: $k \ge n/2$ round trips is the unlimited case, the sum of every rise; the hindsight optimum bounds any real strategy's P&L on that path and is never itself a strategy | N, N, C, K |
| 127 | `lsn.dynprog.interval-dp` Interval DP | Choose the cheapest order to multiply a chain of matrices by DP over intervals of increasing length | Matrices of sizes 10 × 30, 30 × 5 and 5 × 60: which bracketing is cheaper, and by how much? ($(AB)C$: 4,500 multiplications against 27,000) | `dp-table` (interval) | Trap: choosing the first product greedily, or filling the table row by row (intervals must grow in length). Edge: one matrix costs 0; burst balloons chooses the last balloon in an interval, not the first (167 for [3, 1, 5, 8]) | N, O, C, K |

Transfer screens: lesson 124 fuzzy-matches security names against a reference list; lesson 126 bounds what any strategy could have made on a price path, a sanity check on backtests; lesson 127 orders a chain of covariance products (1.4).

**Level DP4: Designing Dynamic Programmes** (`lvl.dynprog.design`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 128 | `lsn.dynprog.subproblem-design` Designing the subproblem | Design a DP by naming subproblems (prefixes, suffixes, substrings, plus any extra state), relating them, ordering them, and stating the base and the original problem | Tile a 2 × 10 board with 1 × 2 dominoes: how many ways? (89) What state is enough? | `dp-table` (1d), `derivation-steps` | Trap: a subproblem missing state that the recurrence needs. Edge: the answer is not always the last cell (take the maximum over cells, as for the LIS); 6.006 teaches this as SRTBOT [check name and lecture] | N, O, C, K |
| 129 | `lsn.dynprog.dag-memo` DP is a path problem on a DAG | Recognise a DP's subproblems as the nodes of a DAG and solve it by memoised DFS, for the longest increasing path in a matrix | Longest strictly increasing path in [[9, 9, 4], [6, 6, 8], [2, 1, 1]]? (4) | `dp-table` (order), `graph-search` (topo) | Trap: adding a visited set against cycles (strictly increasing moves cannot cycle; the memo is enough). Edge: equal neighbours are not moves; the recombining tree of lesson 131 is the same idea | N, C, G, K |
| 130 | `lsn.dynprog.tree-dp` DP on trees | Return a pair of values from each subtree (take, skip) to solve the house robber on a tree | A tree of 7 houses: the best total without robbing a house and its parent | `tree-lab` (recursion), `dp-table` (states) | Trap: recomputing the grandchildren's answers at every node (exponential) instead of returning both values. Edge: one node | N, C, G, K |
| 131 | `lsn.dynprog.recombining-trees` Why a 100-step tree is cheap | Count a recombining binomial tree's nodes against its paths, and explain backward induction as DP over shared subproblems | A 100-step price tree has $2^{100}$ paths. How many node updates does backward induction make? (5,050) | `recursion-tree` (memo), `dp-table` (1d), `node-link` | Trap: thinking the pricer must follow every path. Edge: a path-dependent payoff breaks recombination and loses the saving; one vector of length $N + 1$ is all the memory needed, which the 1.9 exit's pricer uses | N, X, C, K |
| 132 | `lsn.dynprog.top-down-bottom-up` Top-down or bottom-up | Choose memoised recursion or a filled table by the states actually reached, the recursion limit and the space you can save, and reconstruct the choices from either | Fewest coins for 10,000 with {1, 5, 10}: which version runs in Python without `RecursionError`? (bottom-up) | `dp-table` (order) | Trap: "top-down is always slower". Edge: top-down skips unreachable states; bottom-up allows rolling arrays; reconstruction needs a choice table or a second pass | C, M, N, K |

Transfer screens: lesson 131 links 1.7's pricer to this course and prepares the 1.9 exit; lesson 130 aggregates a constraint over an organisation tree.

**Level DP5: Greedy Algorithms** (`lvl.dynprog.greedy`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 133 | `lsn.dynprog.greedy-exchange` Greedy choices and exchange arguments | Test a greedy rule with counterexamples, and prove a correct one by exchanging the first choice of an optimal solution | Three greedy rules (largest coin first for {1, 3, 4}; best value per weight for a fractional knapsack; the same for a 0/1 knapsack): which are always right? (only the fractional knapsack's) | `counterexample-lab` (greedy), `interval-sweep` (exchange) | Trap: trusting a greedy rule because it worked on the examples. Edge: lesson 54's earliest-end rule is the exchange argument's model case | M, G, C, O |
| 134 | `lsn.dynprog.jump-game` The furthest reach | Decide reachability and the fewest jumps with one pass that tracks the furthest reachable index, read as BFS by levels | Jumps [2, 3, 1, 1, 4]: fewest to reach the end? (2) Can [3, 2, 1, 0, 4] reach it? (no) | `pointer-walk` [mode to add: reach], `stepper` | Trap: an $O(n^2)$ DP when the greedy pass is $O(n)$. Edge: a zero at the start; a one-element array | N, C, G, K |
| 135 | `lsn.dynprog.gas-station` Gas stations and resets | Find the start of a circular route by resetting the start whenever the running tank goes negative, and prove it from the total | Fuel [1, 2, 3, 4, 5], costs [3, 4, 5, 1, 2]: where must you start? (station 3) | `array-strip` and `stepper` (screen from primitives) | Trap: trying every start ($O(n^2)$). Edge: total fuel below total cost means no start ($-1$ for [2, 3, 4] against [3, 4, 3]); the proof: a deficit reached at station $j$ rules out every start before $j$ | N, C, O, K |
| 136 | `lsn.dynprog.greedy-counting` Greedy with counts and last positions | Partition a string at last occurrences, and form consecutive runs from a count map | Split "ababcbacadefegdehijhklij" into the most parts with each letter in one part (sizes 9, 7, 8) | `array-strip`, `hash-table` | Trap: sorting the input (destroys the order the parts depend on). Edge: a single letter; forming straights must start from the smallest remaining card | T, C, M, K |
| 137 | `lsn.dynprog.huffman` Huffman coding | Build an optimal prefix code by repeatedly merging the two least frequent symbols, and compute its expected length | Message types in a feed: quotes 60%, trades 20%, cancels 12%, adds 5%, halts 3%. Bits per message with Huffman against 3 fixed bits? (1.68; the entropy is 1.64) | `heap-lab`, `tree-lab` | Trap: assigning codes by frequency rank, or splitting into halves of equal weight (not always optimal). Edge: a single symbol still needs a 1-bit code; ties give different codes of equal cost | N, G, C, K |

Transfer screens: lesson 135 decides where a circular settlement run can start; lesson 137 compresses a market data feed.

**Level DP6: Bits and Integer Maths** (`lvl.dynprog.bits-maths`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 138 | `lsn.dynprog.binary-twos` Binary and two's complement | Read and write integers in binary and two's complement at a fixed width, and predict Python's behaviour with unbounded integers | −10 as an 8-bit pattern? (11110110) `~5` in Python? (−6) | `bit-lab` (binary, twos, python) | Trap: `~x` flips 32 bits (in Python it is $-x - 1$: integers have no fixed width). Edge: `& 0xFF` reads the low byte; `bin(-5)` prints a sign and magnitude, `'-0b101'`, not two's complement | E, N, C, T |
| 139 | `lsn.dynprog.bit-tricks` Masks and XOR tricks | Test, set and clear bits with AND, OR and shifts, cancel pairs with XOR, and count set bits with $x \mathbin{\&} (x - 1)$ | Every trade id appears twice except one: find it in $O(1)$ extra space ([4, 1, 2, 1, 2] gives 4) | `bit-lab` (ops, tricks, count) | Trap: `-5 >> 1` is $-2$ (Python's right shift floors: it is $-3$). Edge: counting bits for 0 to $n$ with `bits[i] = bits[i >> 1] + (i & 1)`; the missing number by XOR | T, N, C, K |
| 140 | `lsn.dynprog.bit-arithmetic` Arithmetic with bits | Add two integers with XOR and carries, and emulate 32-bit overflow in Python with masks | Add 5 and 7 using only `^`, `&` and `<<`: how many rounds? (3) | `bit-lab` (ops, python) | Trap: the loop never ends for negative numbers in Python (the carry shifts left forever without a mask). Edge: reverse the bits of a 32-bit value; turn the masked result back into a signed value | N, C, T, K |
| 141 | `lsn.dynprog.fast-power` Fast exponentiation | Compute $x^n$ with $O(\log n)$ multiplications for negative and huge $n$, modular powers, and Fibonacci numbers by matrix powers | $F_{90}$ by repeated squaring of $\begin{pmatrix}1&1\\1&0\end{pmatrix}$: how many rounds of squaring? (7, one per binary digit of 90) | `bit-lab` (power), `matrix-multiply` | Trap: recursing on $n - 1$ ($O(n)$). Edge: $x^{-n} = (1/x)^n$; in fixed-width languages $-n$ overflows for the most negative $n$; Python's `pow(b, e, m)` | N, C, X, K |
| 142 | `lsn.dynprog.matrix-problems` Matrix manipulation | Rotate a square matrix in place (transpose, then reverse each row), walk it in a spiral, and zero rows and columns with $O(1)$ extra space | Rotate a 3 × 3 matrix a quarter turn clockwise without a second matrix | `cell-grid` and `stepper` (screen from primitives) | Trap: rotating cell by cell in one pass overwrites values still needed. Edge: a non-square matrix in the spiral; the first row and column as marker storage | G, T, C, K |
| 143 | `lsn.dynprog.integer-maths` Maths with integers | Solve digit and number problems exactly with integers: carries, long multiplication on strings, cycles in digit maps | Is 19 happy (repeat "sum of the squared digits" until 1 or a loop)? (yes) Is 2? (no) | `code-cell`, `predict-output` | Trap: floating point for integer problems (`int(2.3 * 100)` is 229). Edge: a carry out of the top digit (999 + 1); detecting the loop with a set or with Floyd (lesson 65) | T, N, C, K |

Transfer screens: lesson 139 packs order flags into one integer; lesson 141 computes modular hashes and compounding powers; lesson 143 converts prices to integer ticks exactly.

**Level DP7: Hard Problems and the Method** (`lvl.dynprog.method`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 144 | `lsn.dynprog.p-np` What cannot be done fast | Explain P, NP and NP-completeness in plain words, and recognise problems that are hard in general: subset sum, the travelling salesman, longest simple path | A subset of 60 trades whose P&L sums to exactly zero: how many subsets would brute force try? ($2^{60} \approx 1.15 \times 10^{18}$) | `complexity-lab` (growth), `choice` | Trap: NP means "not polynomial" (it means a proposed answer can be checked in polynomial time). Edge: knapsack's $O(nW)$ is pseudo-polynomial; small $n$ or small values keep hard problems practical | C, N, M, S |
| 145 | `lsn.dynprog.hard-in-practice` Coping with hard problems | Make an exponential search practical with pruning, meet in the middle and bitmask DP, and say when to accept a heuristic | 40 trades: a subset summing to zero from $2^{40} \approx 1.1 \times 10^{12}$ subsets, or two halves of $2^{20} \approx 10^6$ each? | `complexity-lab` (budget), `code-cell` | Trap: presenting a heuristic's answer as optimal. Edge: Held-Karp solves a 20-city tour in about $4 \times 10^8$ steps; greedy set cover is within a factor of about $\ln n$ of optimal [recalled] | N, C, M, K |
| 146 | `lsn.dynprog.problem-method` The method for an unseen problem | Work an unseen medium through understand, examples, brute force, optimise, code, test and analyse, writing each stage | An unseen medium in `problem-workbench` with every stage open | `problem-workbench` (guided) | Trap: coding before writing two examples and an edge case. Edge: the constraints often name the pattern; a correct brute force is both a test oracle and a fallback answer | O, M, C, K |
| 147 | `lsn.dynprog.pattern-signals` Reading the pattern from the statement | Map statement signals and constraints to candidate patterns, and keep two candidates until an example decides | Ten one-line statements: match each to its likely pattern (sorted input, contiguous range, "all combinations", "fewest steps", "top $k$", dependencies, intervals, "count the ways") | `token-tray` (pattern chips), `choice` | Trap: one keyword means one pattern ("subarray" is not always a sliding window: negative values break it, lesson 42). Edge: $n \le 20$ signals exponential search; $n \le 10^5$ rules out quadratic | S, M, C, S |
| 148 | `lsn.dynprog.stress-testing` Stress testing your own solution | Compare a fast solution with a brute force on many small random inputs, and shrink a failing case | A maximum-subarray solution passes the examples; a brute force disagrees on [-2]. Why? (it returns 0 for all-negative input) | `counterexample-lab` (stress) | Trap: random tests that never contain the edge structure (all negative values, duplicates, $n = 1$). Edge: the generator needs small values so that ties and collisions happen; seed every run so a failure reproduces (1.2's property tests) | G, C, M, K |
| 149 | `lsn.dynprog.interview-talk` Talking through a solution | Explain an approach, its complexity and its trade-offs in writing before and after coding, as an interviewer would mark it | Two transcripts of the same correct solution: which candidate would an interviewer pass, and why? | `problem-workbench` (guided, reflection), `free-response` | Trap: silence until the code works (interviewers mark the reasoning as it happens, curriculum 3.3). Edge: stating a brute force first and then improving it scores better than a silent optimum | C, M, O, S |
| 150 | `lsn.dynprog.timed-medium` A medium in 30 minutes | Plan 30 minutes (about 5 reading and examples, 5 approach, 15 code, 5 testing) and finish a medium in the style of the held-out bank under the clock | A timed medium in `problem-workbench` timed mode, with the plan on screen | `problem-workbench` (timed), `speed-timer` | Trap: perfecting the optimum while the clock runs out (submit a correct slower solution first when the constraints allow it). Edge: stuck at 15 minutes, write the brute force; the exit counts 5 solves in the last 9 timed attempts | O, C, M, K |

Transfer screens: lesson 144 explains why exact optimal rebalancing with lot sizes is hard; lesson 145 makes a 40-trade netting search feasible; lesson 149 rehearses the coding round of a developer interview.

### 2.2 Item 1.9 C++

Every output, diagnostic and sanitiser report quoted below was produced by GCC 13.3 or Clang 18.1 on x86-64 Linux (section 0.6); CI re-records them on the pinned compilers. Snippets that have undefined behaviour are shown only through a sanitiser report or a compiler's assumption, never as "the output".

#### Course CB: C++ Foundations (`crs.cppcore`, 4 levels, 22 lessons)

From a source file to a running, tested program: the build stages, static types and arithmetic, functions and files, and the first containers, algorithms and tests. learncpp chapters 0 to 13 and 16 run alongside; CS106L's first lectures are the parallel.

**Level CB1: From Source to Program** (`lvl.cppcore.build`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | `lsn.cppcore.source-to-program` Source to program | Name the four stages from source to executable (preprocess, compile, assemble, link) and match an error message to the stage that raised it | Four messages: "expected ';' before '}' token", "undefined reference to `price(double)'", "fatal error: pricer.h: No such file or directory", "multiple definition of `fee(double)'". Which stage raised each? (compiler; linker; preprocessor; linker) | `compile-pipeline` (stages), `diagnostic-reader` (compiler, linker) | Trap: "C++ runs line by line like Python", or compile and link errors are one kind. Edge: a program can compile and fail to link; `#include <iostream>` adds tens of thousands of lines to a translation unit (the recorded count is shown, never a remembered one) | S, C, O, M |
| 2 | `lsn.cppcore.toolchain` Your toolchain | Install a compiler, build and run a program from the terminal with warnings on, and paste the result | Build hello world with `g++ -std=c++20 -Wall -Wextra -O2 hello.cpp -o hello`, run `./hello`, paste `g++ --version` and the output | `setup-checklist` (cpp-toolchain), `code-cell` (C++), `text-terminal` | Trap: editing the source and running the old binary (a C++ program changes only when rebuilt). Edge: `main` without `return` returns 0; Windows learners use WSL or MSYS2 [recalled]; the GCC 13 or Clang 17 floor (decision 11) | G, O, C, T |
| 3 | `lsn.cppcore.static-types` Static types | Declare typed variables, say what the compiler checks before the program runs, and predict what `auto` deduces | `int qty = 10; qty = "ten";` works as a rebinding in Python. In C++? (a compile error: a string literal cannot become an `int`) | `predict-output` (compiles), `diagnostic-reader` (compiler) | Trap: a C++ variable can change type like a Python name. Edge: `auto half = 1 / 2;` is the `int` 0 [verified]; `auto` drops `const` and references | C, T, T, R |
| 4 | `lsn.cppcore.io-format` Input, output and formatting | Read input with `>>` and `std::getline`, and format output with `std::format` | Read a quantity with `cin >> n`, then a ticker with `getline`: the ticker comes back empty. Why? (the newline after the number is still in the stream [verified]) | `predict-output` (C++), `format-lab` (C++), `code-cell` | Trap: mixing `>>` and `getline` without discarding the newline. Edge: `std::format` follows Python's mini-language closely but has no `,` thousands separator (`"{:,}"` fails to compile [verified]); `std::endl` flushes the stream every line, `'\n'` does not | T, E, C, T |
| 5 | `lsn.cppcore.reading-errors` Reading compiler errors | Find the first error that matters in a long diagnostic and fix its cause, not its symptoms | A 60-line report after one missing semicolon and a bad template call: tap the line to fix first | `diagnostic-reader` (compiler) | Trap: fixing the last error first (later errors are often consequences of the first). Edge: a missing semicolon is reported on the following line; template errors print an instantiation stack, read from the first "required from here" [recalled] | R, C, O, M |

Transfer screens: lesson 1 reads a CI build log from a pricing library; lesson 4 prints a trade blotter with aligned columns.

**Level CB2: Types and Arithmetic** (`lvl.cppcore.types`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 6 | `lsn.cppcore.integer-types` Fixed-width integers | State the sizes and ranges of the integer types on a 64-bit platform and choose one that cannot overflow for a quantity | Nanoseconds in a day held in an `int`? (no: 86,400,000,000,000 against a maximum of 2,147,483,647) | `memory-layout` (sizes), `bit-lab` (cpp) | Trap: `int` is 64 bits on a 64-bit machine (it is 32 on mainstream platforms; `long` is 64 bits on Linux and macOS and 32 on Windows). Edge: `int64_t`, `uint32_t` from `<cstdint>`; `size_t` is 64 bits here [verified] | N, C, M, N |
| 7 | `lsn.cppcore.undefined-behaviour` Undefined behaviour | Explain why signed overflow is undefined, show the optimiser assuming it never happens, and catch it with UndefinedBehaviorSanitizer | `int count = 0; for (int i = 1; i > 0; i *= 2) ++count;` prints 31 at `-O0`. At `-O2`? (it never ends, on GCC 13 and on Clang 18 [verified]) | `diagnostic-reader` (ubsan), `predict-output` (C++), `bit-lab` (cpp) | Trap: "signed overflow wraps around" (unsigned arithmetic wraps; signed overflow is undefined, so the compiler may delete the `i > 0` test). Edge: `-fsanitize=undefined` reports "signed integer overflow: 1073741824 * 2 cannot be represented in type 'int'" [verified]; undefined code can work in one build and fail in the next | C, T, M, R |
| 8 | `lsn.cppcore.conversions` Conversions and promotions | Predict mixed signed and unsigned comparisons and small-integer arithmetic, and act on `-Wsign-compare` | `-1 < 1u`? (false: −1 converts to 4,294,967,295) `uint8_t a = 200, b = 100; auto c = a + b;` type and value? (`int`, 300) | `bit-lab` (cpp), `predict-output` (C++) | Trap: signed and unsigned comparisons behave like mathematics. Edge: `i < v.size() - 1` on an empty vector compares with 18,446,744,073,709,551,615 [verified]; 300 stored back in a `uint8_t` is 44 | T, T, C, N |
| 9 | `lsn.cppcore.division-floats` Division and floating point | Predict integer and floating division and remainder in C++, and contrast them with Python | `7 / 2 * 2.0`? (6) `-7 / 2` and `-7 % 3`? (−3 and −1, where Python gives −4 and 2 [verified]) | `predict-output` (C++), `number-line` (Stage 0) | Trap: carrying Python's floor division into C++ (C++ truncates towards zero). Edge: integer division by zero is undefined, floating division by zero gives infinity; `0.1 + 0.2 == 0.3` is false here too | T, T, C, N |
| 10 | `lsn.cppcore.initialisation` Initialisation, narrowing and const | Initialise with braces, predict which narrowing conversions are rejected, and mark values `const` or `constexpr` | Which compile: `int a{3.7};`, `int b = 3.7;`, `const double r{0.05};`? (the first fails: "narrowing conversion of '3.7000000000000002e+0' from 'double' to 'int'"; the second gives 3 [verified]) | `predict-output` (compiles), `diagnostic-reader` (compiler) | Trap: an uninitialised local is zero (its value is indeterminate and reading it is undefined). Edge: `Pricer p();` declares a function, not an object; GCC warns "empty parentheses were disambiguated as a function declaration" [verified] | R, C, T, T |
| 11 | `lsn.cppcore.enums-structs` Enums and structs | Model a trade with an `enum class` and a struct, initialise it with designated initialisers, and switch over every enumerator | Why does `enum class Side { Buy, Sell };` reject `if (side == 1)`? | `code-cell` (C++), `predict-output` | Trap: plain `enum` names leak into the enclosing scope and convert silently to `int`. Edge: `-Wswitch` warns when a `switch` misses an enumerator; designated initialisers must follow declaration order | C, T, M, K |

Transfer screens: lesson 6 sizes a timestamp field for exchange data; lesson 7 explains a production bug where a loop guard was optimised away; lesson 11 models an order record.

**Level CB3: Functions and Files** (`lvl.cppcore.functions`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 12 | `lsn.cppcore.control-flow` Control flow | Write `if`, `for`, range-`for`, `while` and `switch` correctly, and predict what a by-value range-`for` changes | `for (auto x : prices) x *= 1.1;` then print `prices[0]` (unchanged: `x` is a copy; `auto&` changes the vector [verified]) | `predict-output` (C++), `code-tracer` (C++) | Trap: `if (x = 5)` assigns (GCC: "suggest parentheses around assignment used as truth value" [verified]). Edge: a loop variable's scope ends with the loop; `switch` falls through without `break` | T, T, C, K |
| 13 | `lsn.cppcore.pass-by-value` Functions and pass by value | Step a call to show a by-value parameter is a copy in a new frame, and estimate the cost of copying a large argument | `void shock(std::vector<double> v) { v[0] *= 2; }` called on a book: does the caller's book change? (no, the opposite of Python's list) | `code-tracer` (C++), `memory-layout` | Trap: C++ parameters alias like Python names. Edge: passing a vector of a million doubles by value copies 8 MB per call | C, T, N, K |
| 14 | `lsn.cppcore.references` References and const references | Pass large arguments by `const&`, change a caller's variable through `&`, and spot a returned reference to a local | `int& bad() { int x = 42; return x; }` GCC says? ("reference to local variable 'x' returned" [verified]) | `code-tracer` (C++), `diagnostic-reader` | Trap: returning a reference to a local (it dangles when the frame ends). Edge: a reference must be initialised and cannot be re-seated; `const&` binds to a temporary | C, T, M, K |
| 15 | `lsn.cppcore.overloading` Overloading and default arguments | Predict which overload a call selects, recognise an ambiguous call, and put default arguments in the declaration | With `price(int)` and `price(double)`: which runs for `price(5)`, `price(5.0f)`, `price('a')` and `price(5L)`? (int; double; int; ambiguous: "call of overloaded 'price(long int)' is ambiguous" [verified]) | `predict-output` (compiles), `diagnostic-reader` | Trap: "the nearest-looking type wins" (`float` and `char` promote, but `long` converts equally well to both). Edge: default arguments go in the header's declaration only | T, C, S, T |
| 16 | `lsn.cppcore.headers-odr` Headers and the one-definition rule | Split a program into headers and sources, guard headers, and fix "multiple definition" and "undefined reference" | A header defines `double fee(double)` and two `.cpp` files include it. The linker? ("multiple definition of `fee(double)'" [verified]) | `compile-pipeline` (multi-file), `diagnostic-reader` (linker) | Trap: `#pragma once` prevents this (it stops a double include within one file, not definitions in two files: mark the function `inline` or move it to a source file). Edge: a declared, undefined function links only if never called; templates live in headers (lesson 48) | C, R, O, K |
| 17 | `lsn.cppcore.namespaces-cmake` Namespaces and CMake | Organise code in namespaces, keep `using namespace std;` out of headers, and build a small project with CMake | Edit `pricer.h` in a project of 4 sources. Which object files rebuild? (those whose sources include it, directly or indirectly) | `compile-pipeline` (build-graph, cmake) | Trap: `using namespace std;` in a header (every file that includes it inherits the names and their clashes). Edge: an anonymous namespace gives internal linkage; a minimal `CMakeLists.txt` needs `cmake_minimum_required`, `project` and `add_executable` | R, M, C, O |

Transfer screens: lesson 13 shows why a risk function that takes the whole book by value is slow; lesson 16 splits a pricer into a library and a command-line tool.

**Level CB4: First Containers, Algorithms and Tests** (`lvl.cppcore.containers`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 18 | `lsn.cppcore.vector-basics` `std::vector` basics | Build, index and iterate a `std::vector`, and choose between `[]` and `at` | `std::vector<int> v(3);` then `v[3]`? (undefined; AddressSanitizer: heap-buffer-overflow [verified]) `v.at(3)`? (throws `std::out_of_range`) | `dynamic-array` (cpp), `diagnostic-reader` (asan) | Trap: an out-of-range `[]` raises like Python's `IndexError` (it is undefined, unchecked). Edge: `v(3)` holds three zeros while `v{3}` holds one 3; `size()` is unsigned (lesson 8) | C, T, M, K |
| 19 | `lsn.cppcore.strings` `std::string` and `std::string_view` | Manipulate `std::string`, search with `find` and `npos`, and pass text as `std::string_view` without dangling | `std::string s = "Price: " + 42;` compiles. What does it hold? (not "Price: 42": the literal's pointer moves 42 bytes, past its end; GCC warns of array bounds and Clang that "adding 'int' to a string does not append to the string" [verified]) | `predict-output`, `diagnostic-reader` | Trap: `+` on a string literal appends. Edge: a `string_view` of a temporary `std::string` dangles (heap-use-after-free [verified]); `find` returns `std::string::npos` when absent | T, C, T, K |
| 20 | `lsn.cppcore.arrays` `std::array` and C arrays | Use `std::array`, explain how a C array decays to a pointer when passed, and take lengths safely | `void f(int arr[]) { return sizeof(arr); }` gives? (8, a pointer's size; GCC warns "'sizeof' on array function parameter 'arr' will return size of 'int*'" [verified]) | `memory-layout` (array), `diagnostic-reader` | Trap: `sizeof(arr) / sizeof(arr[0])` inside a function. Edge: `std::size` and `std::array::size()`; `arr[4]` of `int arr[4]` is a stack-buffer-overflow [verified] | N, C, T, K |
| 21 | `lsn.cppcore.first-algorithms` First algorithms | Use `std::sort`, `std::find`, `std::max_element` and `std::accumulate`, choosing the right initial value | `std::accumulate(v.begin(), v.end(), 0)` on four values of 0.5? (0: the `int` 0 makes every partial sum an `int` [verified]) | `predict-output` (C++), `code-cell` | Trap: the initial value's type is irrelevant (it is the sum's type: pass `0.0`). Edge: `max_element` on an empty range returns `end()`; ranges are half-open, as in 1.8 | T, C, M, K |
| 22 | `lsn.cppcore.doctest` Testing with doctest | Write doctest cases with `CHECK`, `REQUIRE` and `doctest::Approx`, and run them from CMake | `CHECK(price == 10.4506)` fails on a correct pricer. Why? (exact equality on a double) | `code-cell` (C++ tests), `mutant-hunter` [mode to add: cpp] | Trap: comparing doubles with `==`. Edge: `REQUIRE` stops the test case, `CHECK` continues; `doctest::Approx(x).epsilon(1e-9)` sets a relative tolerance [recalled API] | C, K, M, K |

Transfer screens: lesson 19 parses option symbols (1.1 lesson 7's OCC format) in C++; lesson 22 writes the first tests of the pricer that level CP3 completes.

#### Course CM: Memory and Ownership (`crs.cppmemory`, 4 levels, 24 lessons)

Where objects live and who frees them: the stack and the heap, pointers and references, layout, classes with invariants, RAII, copying and moving, smart pointers, and polymorphism for a pricing library's design. learncpp chapters 12, 14, 15, 19 to 25 and 27 run alongside; Joshi's book is the design reference for level CM4.

**Level CM1: The Memory Model** (`lvl.cppmemory.model`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 23 | `lsn.cppmemory.stack-lifetimes` The stack and lifetimes | Predict which objects exist at each line from scope, and the order in which their destructors run | Tap which of 4 locals exist at line 9 of a function with two nested blocks | `code-tracer` (C++), `ownership-lab` (raii) | Trap: a local lives until the function returns (it lives until its block ends). Edge: `static` locals live for the whole program; destruction runs in reverse order of construction | R, O, C, T |
| 24 | `lsn.cppmemory.pointers` Pointers | Use `&`, `*` and `nullptr`, and compute addresses as a pointer walks an array of `double` | `double px[4]` starts at 0x1000. Where does `px + 3` point? (0x1018) | `memory-layout` (array, pointers), `code-tracer` (C++) | Trap: `p + 1` adds one byte (it adds one element, 8 bytes here). Edge: `*p++` increments the pointer, not the value; dereferencing `nullptr` is undefined | N, T, C, N |
| 25 | `lsn.cppmemory.const-pointers` Pointers, references and const | Choose a pointer or a reference for a parameter, and read `const` placement right to left | Which can change: `const double* p`, `double* const q`, `const double* const r`? | `code-tracer`, `predict-output` (compiles) | Trap: `const double* p` makes `p` constant (it makes the value read-only through `p`). Edge: a pointer can be null and re-seated, a reference cannot | S, C, R, T |
| 26 | `lsn.cppmemory.heap` The heap: new and delete | Allocate and free on the heap, and name the outcome of a leak, a double free and a use after free | A function allocates an order array and returns early on an error. What leaks? | `code-tracer` (C++ heap), `ownership-lab` (raw), `diagnostic-reader` (asan) | Trap: `delete` on an array from `new[]` (it must be `delete[]`). Edge: AddressSanitizer reports "attempting double-free" and "heap-use-after-free" with the allocation and free stacks [verified]; LeakSanitizer reports leaks at exit | R, C, S, T |
| 27 | `lsn.cppmemory.sanitiser-reports` Reading sanitiser reports | Read AddressSanitizer and UndefinedBehaviorSanitizer reports to find the faulting line, the origin of the bad address and the kind of error | Three reports: heap-buffer-overflow, stack-use-after-scope, signed integer overflow. Tap the line each blames and name its fix | `diagnostic-reader` (asan, ubsan) | Trap: "it printed the right value, so the code is fine". Edge: sanitisers slow a program down, so timing runs never use them; a lambda's reference capture used after its scope is stack-use-after-scope [verified] | R, S, C, M |
| 28 | `lsn.cppmemory.struct-layout` Struct layout | Compute a struct's size, offsets and padding from alignment, and reorder fields to shrink it | `struct Quote { char side; double px; int qty; };` size? (24: offsets 0, 8, 16, 11 bytes of padding) As `double`, `int`, `char`? (16 [verified]) | `memory-layout` (struct) | Trap: `sizeof` is the sum of the members' sizes (13 here). Edge: a million quotes save 8 MB from the reorder; the same five trade fields take 24 or 40 bytes depending on order [verified] | N, N, G, C |

Transfer screens: lesson 26 traces a memory leak in a quote handler; lesson 28 lays out a market data message to fit two per cache line.

**Level CM2: Classes and Invariants** (`lvl.cppmemory.classes`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 29 | `lsn.cppmemory.classes-invariants` Classes and invariants | Write a class whose constructors establish an invariant and whose public interface keeps it | A `Price` type must never be negative. Where does the check live, and why not in every caller? | `code-cell` (C++), `code-review` | Trap: public data members (any caller can break the invariant). Edge: single-argument constructors should be `explicit` to block silent conversions | C, M, K, T |
| 30 | `lsn.cppmemory.member-init` Constructors and initialisation order | Write member initialiser lists and predict the order members initialise in | `Order(int lots) : lots_(lots), qty_(lots_ * 100)` with `qty_` declared first. `qty_` after `Order o(3)`? (indeterminate: `qty_` is set first, from an uninitialised `lots_`; this build printed 0; GCC warns `-Wreorder` and "is used uninitialized" [verified]) | `code-tracer` (C++), `diagnostic-reader` | Trap: members initialise in initialiser-list order (they follow declaration order). Edge: default member initialisers such as `int qty_ = 0;` | T, C, O, K |
| 31 | `lsn.cppmemory.const-members` Const member functions | Mark member functions `const`, explain why a `const&` can call only those, and use `mutable` sparingly | `void report(const Book& b) { b.total(); }` fails to compile. Why? (`total` is not `const`) | `diagnostic-reader` (compiler), `code-cell` | Trap: `const` is decoration (the compiler enforces it, and it spreads through interfaces). Edge: `const` and non-`const` overloads of `operator[]` | C, T, R, K |
| 32 | `lsn.cppmemory.operators` Operator overloading | Overload arithmetic, comparison and stream operators for a value type, using C++20's defaulted `<=>` | A `Money` type in integer pence: implement `+`, `==` and `<<`, then default `<=>` | `code-cell` (C++), `predict-output` | Trap: a `<` that disagrees with `==` (sorting and maps then misbehave). Edge: C++20 rewrites `a != b` from `==` and `a > b` from `<=>`; `operator<<` is a free function | K, T, C, M |
| 33 | `lsn.cppmemory.raii` RAII and stack unwinding | Tie each resource's release to a destructor, and predict destructor order when an exception unwinds the stack | A function opens a file, takes a lock and allocates a buffer, then throws. What is released, and in what order? (all three in reverse order, if each is held by an object) | `ownership-lab` (raii), `code-tracer` (unwinding) | Trap: cleanup code after the `throw` runs (only destructors run). Edge: a destructor that throws during unwinding calls `std::terminate` | O, C, M, K |
| 34 | `lsn.cppmemory.errors` Exceptions, error codes and optional | Choose exceptions, error codes or `std::optional` for a pricing function, and catch exceptions by reference | `catch (std::exception e)` on a `PricingError`: what does `e.what()` return? ("std::exception": the object was sliced; by reference it returns the derived message [verified]) | `predict-output` (C++), `code-cell` | Trap: catching by value. Edge: a `noexcept` function that throws calls `std::terminate`; `std::expected` (C++23) is named as the newer option | T, C, O, K |

Transfer screens: lesson 29 guards a notional type against negative values; lesson 32 builds a money type that cannot lose a penny (1.1 homework Y1 in C++); lesson 33 releases a market data connection on every exit path.

**Level CM3: Copying and Moving** (`lvl.cppmemory.ownership`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 35 | `lsn.cppmemory.copy-semantics` What a copy copies | Explain the default copy and show the double free when a class owns a raw pointer | Copy an `OrderBuffer` that owns `new double[n]`, then let both copies go out of scope. What happens? (both destructors delete one block: a double free) | `ownership-lab` (copy), `diagnostic-reader` (asan) | Trap: the default copy is deep (it copies the pointer, not the block). Edge: self-assignment must be safe | G, C, T, M |
| 36 | `lsn.cppmemory.rule-of-three` The rule of three and copy-and-swap | Implement a copy constructor, copy assignment and destructor that agree, with copy-and-swap | Write the three members of `OrderBuffer` so that copies are independent | `code-cell` (C++), `ownership-lab` | Trap: a destructor without the copy operations. Edge: copy-and-swap handles self-assignment and gives the strong exception guarantee | K, C, M, O |
| 37 | `lsn.cppmemory.move-semantics` Moving | Explain rvalues and what `std::move` does, and predict a moved-from object's state | `auto b = std::move(a);` for two vectors: what do `a` and `b` hold after? (`b` has the elements; `a` is valid but unspecified, in practice empty) | `ownership-lab` (move) | Trap: `std::move` moves (it only casts to an rvalue; the move constructor does the moving). Edge: `std::move` of a `const` object copies [verified] | C, T, T, G |
| 38 | `lsn.cppmemory.rule-of-five-zero` The rules of five and zero | Apply the rules of zero and five, and predict when the compiler generates move operations | A struct holding a buffer gets an empty user-declared destructor. Does `WithDtor b = std::move(a);` copy or move the buffer? (copy: a user-declared destructor suppresses the implicit move [verified]) | `ownership-lab`, `predict-output` (C++) | Trap: adding a destructor "for tidiness". Edge: `std::vector` moves elements on reallocation only through a `noexcept` move constructor; members that manage themselves (the rule of zero) are the default | T, C, M, K |
| 39 | `lsn.cppmemory.copy-elision` Returning objects | Predict when a return copies, moves or does neither, and avoid the pessimising move | `return std::move(local);` against `return local;` (the first prevents copy elision; GCC and Clang both warn `-Wpessimizing-move` [verified]) | `predict-output` (C++), `diagnostic-reader` | Trap: `std::move` on a return makes it faster. Edge: C++17 guarantees elision for returned temporaries; returning a parameter moves | C, T, M, S |
| 40 | `lsn.cppmemory.smart-pointers` Smart pointers | Choose `unique_ptr`, `shared_ptr` or a plain value, predict `use_count`, and break a cycle with `weak_ptr` | Two nodes hold `shared_ptr`s to each other and leave scope. Freed? (no: LeakSanitizer reports 64 bytes in 2 objects and neither destructor runs [verified]) | `ownership-lab` (unique, shared) | Trap: `shared_ptr` everywhere "to be safe" (it costs a control block and atomic counts, and cycles still leak). Edge: `make_unique` and `make_shared`; a `unique_ptr` can be moved, never copied | N, C, G, K |

Transfer screens: lesson 37 moves a large scenario matrix into a pricing job without copying; lesson 40 manages instrument objects shared by several books.

**Level CM4: Polymorphism and Design** (`lvl.cppmemory.design`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 41 | `lsn.cppmemory.inheritance-virtual` Inheritance and virtual functions | Dispatch through a virtual function, follow a call through the vtable, and mark overrides | `Base& b = call; b.price();` with and without `virtual` on `Base::price`: which runs? | `code-tracer` (C++ vtable), `predict-output` | Trap: forgetting `virtual` (the base version runs). Edge: `override` turns a mismatched signature into a compile error | T, C, T, K |
| 42 | `lsn.cppmemory.slicing` Slicing and virtual destructors | Recognise object slicing and when a class needs a virtual destructor | `Base sliced = call;` then `sliced.price()`? (the base price: 1.0, against 2.0 through a reference [verified]) | `ownership-lab`, `predict-output` (C++) | Trap: storing derived objects in `std::vector<Base>` (each is sliced; store `std::unique_ptr<Base>`). Edge: `delete` through a base pointer without a virtual destructor is undefined; `final` stops further overriding | T, C, M, T |
| 43 | `lsn.cppmemory.payoff-hierarchy` A payoff hierarchy | Design payoffs with an abstract base, concrete classes and a virtual `clone`, in Joshi's style | Add a digital call to a pricer that handles calls and puts. How many files change? (one new class, if the design is right) | `code-cell` (C++), `code-review` | Trap: a `switch` on an enum in every function (each new payoff edits them all). Edge: `clone` copies through a base pointer | C, M, K, O |
| 44 | `lsn.cppmemory.lambdas` Lambdas and captures | Write lambdas with value, reference and init captures, and predict when a capture outlives what it captured | A lambda captures a local by reference and is stored in a `std::function` that outlives it. AddressSanitizer? (stack-use-after-scope [verified]) | `code-tracer` (C++), `diagnostic-reader` | Trap: `[&]` everywhere (captures dangle when the lambda escapes). Edge: `mutable` lambdas; `std::function` costs an indirect call and may allocate | T, C, R, K |
| 45 | `lsn.cppmemory.variant-optional` `std::optional` and `std::variant` | Model "missing" and "one of several" with `std::optional` and `std::variant` with `std::visit`, instead of sentinels or inheritance | A quote is a price or "no market": `std::optional<double>` or a sentinel of −1? | `code-cell` (C++), `predict-output` | Trap: sentinel values such as −1 or `NaN` (they flow silently into arithmetic). Edge: `std::get` on the wrong alternative throws `std::bad_variant_access`; `std::visit` makes every case explicit | C, T, M, K |
| 46 | `lsn.cppmemory.static-dynamic` Run-time or compile-time polymorphism | Choose between virtual dispatch and a template parameter for a pricing engine, and build objects from configuration with a factory | One pricer, many payoffs: a virtual call per node of a 10,000-step tree, or a template parameter? | `code-cell` (C++), `bench-lab` (recorded) | Trap: design patterns for their own sake. Edge: templates remove the indirect call but grow the binary and compile time; a factory registry builds payoffs from names in a file | C, M, K, S |

Transfer screens: lesson 43 is the payoff design the Monte Carlo project uses; lesson 45 represents a missing quote; lesson 46 decides how a production pricer chooses its model.

#### Course CL: Generic Code and the Standard Library (`crs.cppstl`, 4 levels, 21 lessons)

Templates and concepts, the containers with their costs and invalidation rules, the algorithms and ranges, and the numerical tools a pricer needs: random numbers, floating-point care, Monte Carlo and Black-Scholes. learncpp chapters 11, 16 to 18, 20 and 26 run alongside; CS106L's container and template lectures are the parallel.

**Level CL1: Templates** (`lvl.cppstl.templates`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 47 | `lsn.cppstl.function-templates` Function templates | Write function templates and predict deduction and instantiation | `template <typename T> T mx(T a, T b)` called as `mx(1, 2.0)`: compiles? (no: "no matching function for call to 'mx(int, double)'" [verified]) | `predict-output` (compiles), `diagnostic-reader` | Trap: a template is compiled once, like a Python function (each set of argument types instantiates new code). Edge: `mx<double>(1, 2.0)` names the type | C, T, R, K |
| 48 | `lsn.cppstl.class-templates` Class templates | Write a class template with its members in the header, and fix the "undefined reference" from a template defined in a source file | `twice<T>` declared in a header and defined in a `.cpp`: the linker says? ("undefined reference to `int twice<int>(int)'" [verified]) | `compile-pipeline` (multi-file), `diagnostic-reader` (linker) | Trap: splitting a template like an ordinary function. Edge: class template argument deduction (`std::vector v{1, 2, 3}`) | C, R, T, K |
| 49 | `lsn.cppstl.concepts` Concepts | Constrain templates with C++20 concepts so that misuse gives one readable error | A `mean` template called on `std::string`: compare the errors with and without `requires std::floating_point<T>` | `diagnostic-reader` (compiler), `code-cell` | Trap: an unconstrained template is "more general" (it fails later, with longer errors). Edge: abbreviated templates with `auto` parameters | C, M, T, K |
| 50 | `lsn.cppstl.constexpr` Compile-time computation | Compute at compile time with `constexpr` and check facts with `static_assert` | Make the trading-day count `constexpr` and assert at compile time that $\sqrt{252}$ lies between 15 and 16 | `predict-output` (compiles), `code-cell` | Trap: `constexpr` forces compile-time evaluation (only where a constant is required; `consteval` forces it). Edge: `if constexpr` discards a branch per instantiation | C, T, T, K |
| 51 | `lsn.cppstl.generic-numerics` Numerical code on any floating type | Write numerical code templated on the floating type and use `std::numeric_limits` | Run one pricer with `float` and with `double`: how many digits agree with the reference? | `float-inspector` (C++), `code-cell` | Trap: `float` is accurate enough for pricing (about 7 significant digits; long sums drift). Edge: `std::numeric_limits<double>::epsilon()` is $2.22 \times 10^{-16}$ [verified] | N, C, M, K |

Transfer screens: lesson 49 constrains a statistics library to floating types; lesson 51 shows why GPU code chooses `float` deliberately and checks its error.

**Level CL2: Containers** (`lvl.cppstl.containers`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 52 | `lsn.cppstl.vector-capacity` Capacity and invalidation | Track size and capacity through `push_back`, use `reserve`, and predict iterator and reference invalidation | Capacities while 100 values are pushed? (1, 2, 4, ..., 128 on libstdc++ [verified]) A reference to `v[0]` taken before 10 pushes, read after? (heap-use-after-free [verified]) | `dynamic-array` (cpp) | Trap: pointers and references into a vector survive `push_back`. Edge: `reserve` prevents reallocation up to its size; other libraries grow by other factors (1.5 in MSVC [recalled]) | N, C, T, N |
| 53 | `lsn.cppstl.container-costs` Containers and their costs | Choose among `vector`, `deque`, `list`, `map`, `unordered_map`, `set` and `priority_queue` for five workloads, by cost and memory layout | Insert 50,000 values in sorted position after a linear search: `std::vector` or `std::list`? (vector: 0.29 s against 6.1 s on one machine [measured]) | `complexity-lab`, `memory-layout` (pointers), `bench-lab` (recorded) | Trap: a list wins at middle inserts because insertion is $O(1)$ (finding the position dominates, and contiguous memory makes the vector's search and shift fast). Edge: `unordered_map`'s worst case is linear; `deque` keeps references valid when pushing at either end | M, C, N, S |
| 54 | `lsn.cppstl.maps` Ordered and hashed maps | Use `std::map` and `std::unordered_map` without accidental inserts, and query an ordered map with `lower_bound` | `if (book[px] == 0)` on a map with no level at `px`: what happened to the map? (it gained an entry: `operator[]` inserts a default [verified]) | `tree-lab` (bst), `hash-table` (cpp) | Trap: `m[key]` to test presence. Edge: `contains` (C++20), `find`, `try_emplace`; a custom hash for a struct key; `lower_bound` finds the best level at or above a price | T, C, T, K |
| 55 | `lsn.cppstl.priority-queue-set` Heaps and multisets | Use `std::priority_queue`, a max-heap by default, and `std::multiset` for an order book, and erase exactly one element | `std::multiset{1, 2, 2, 2, 3}`: size after `erase(2)`? (2) After `erase(find(2))` instead? (4 [verified]) | `heap-lab` (cpp), `tree-lab` | Trap: `priority_queue` is a min-heap like Python's `heapq` (it is a max-heap; `std::greater<>` makes a min-heap). Edge: `erase(value)` removes every copy | N, N, C, K |
| 56 | `lsn.cppstl.iterators` Iterators and erasing safely | Use iterators over half-open ranges, erase while iterating correctly, and use `std::erase_if` | Remove every cancelled order inside a range-`for`. Why does it crash? (erasing invalidates the loop's iterator) | `code-tracer` (C++), `predict-output` | Trap: `v.erase(it)` inside a range-`for`. Edge: `std::erase_if(v, pred)` (C++20); `it = v.erase(it)` in a manual loop; reverse iterators | T, C, O, K |
| 57 | `lsn.cppstl.span-views` Views without copies | Pass contiguous data and text with `std::span` and `std::string_view`, and never return a view of a local | A function returns `std::span<double>` over a local vector. What does the caller read? (a dangling view) | `code-tracer` (C++), `diagnostic-reader` (asan) | Trap: a view owns its data. Edge: `std::span<const double>` for read-only access; one function then serves vectors, arrays and C arrays | C, T, M, K |

Transfer screens: lesson 53 picks the container for an order book's price levels; lesson 54 finds the best ask at or above a limit with `lower_bound`; lesson 55 rebuilds 1.8 lesson 74's book in C++.

**Level CL3: Algorithms** (`lvl.cppstl.algorithms`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 58 | `lsn.cppstl.sort-comparators` Sorting and comparators | Sort with comparators that are strict weak orderings, and sort by several keys with `std::tie` | `std::sort` with `return a <= b;` on 100 equal values. Fine? (it appeared to work, but AddressSanitizer reports a heap-buffer-overflow read in the partition loop, and `-D_GLIBCXX_DEBUG` rejects the comparator [verified]) | `sort-lab` (comparator), `diagnostic-reader` (asan) | Trap: `<=` as a comparator (a comparator must be irreflexive; with `<=` the partition runs past the end). Edge: `std::stable_sort` keeps ties in order; `std::tie(a.sym, a.ts) < std::tie(b.sym, b.ts)` | C, T, M, K |
| 59 | `lsn.cppstl.binary-search` Binary search in the library | Use `lower_bound`, `upper_bound` and `equal_range`, and compute a midpoint without overflow | `int mid = (lo + hi) / 2;` with `lo = 2,000,000,000` and `hi = 2,100,000,000`? (signed overflow; `lo + (hi - lo) / 2` gives 2,050,000,000 [verified]) | `binary-search-lab` (cpp), `predict-output` | Trap: `(lo + hi) / 2` is always safe. Edge: `std::midpoint` (C++20); the bounds match Python's `bisect_left` and `bisect_right` (1.8 lesson 47) | N, T, C, K |
| 60 | `lsn.cppstl.numeric` Numeric algorithms | Use `accumulate`, `inner_product`, `partial_sum` for prefix sums, `adjacent_difference` for changes, and `transform_reduce` | Prices to price changes with `adjacent_difference`, and cumulative P&L with `partial_sum` | `code-cell` (C++), `predict-output` | Trap: `std::reduce` gives `accumulate`'s floating result (it may reorder: on [1e16, 1, −1e16, 1] it gave 0.0 where `accumulate` gave 1.0 [verified]). Edge: `adjacent_difference` copies the first element unchanged | T, C, M, K |
| 61 | `lsn.cppstl.ranges` Ranges and views | Use C++20 ranges: `std::ranges::sort` with a projection and lazy views such as `filter` and `transform` | Sort trades by price with `std::ranges::sort(trades, {}, &Trade::px)` | `code-cell` (C++), `predict-output` | Trap: a view stores its results (views are lazy, recompute on each pass and can dangle). Edge: views compose with `\|`; range algorithms take the container itself | T, C, T, K |
| 62 | `lsn.cppstl.dsa-in-cpp` 1.8's patterns in C++ | Port hashing, BFS and Dijkstra to C++ with `unordered_map`, `queue` and `priority_queue<pair<long long, int>, vector<...>, greater<>>` | Two-sum on $10^5$ notionals up to $10^9$: why must the C++ sum be `long long`? ($2 \times 10^9$ exceeds 2,147,483,647) | `code-cell` (C++), `problem-workbench` (contest) | Trap: `int` for sums and products of large inputs. Edge: `greater<>` turns the max-heap into Dijkstra's min-heap; crafted keys can attack `unordered_map` (2.4 lesson 16) | N, C, M, K |

Transfer screens: lesson 58 sorts an order book by price then time; lesson 60 computes returns and cumulative P&L; lesson 62 opens the C++ Lab (section 3.4).

**Level CL4: Randomness and Numerics** (`lvl.cppstl.numerics`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 63 | `lsn.cppstl.random` Random numbers | Generate reproducible random numbers with `<random>` engines and distributions seeded explicitly | `std::mt19937` with its default seed: the 10,000th output? (4,123,659,995, fixed by the standard [verified]) Is `std::normal_distribution`'s output fixed too? (no: the algorithm differs between standard libraries [recalled]) | `sim-runner` (C++ recorded), `predict-output` | Trap: `rand() % n` (biased and weak) and seeding from the clock in tests. Edge: `std::mt19937_64`'s 10,000th output, 9,981,545,732,273,789,042, is fixed too [verified]; one engine per thread (lesson 87) | N, C, M, K |
| 64 | `lsn.cppstl.floating-point` Floating point and fast-math | Predict summation error, compensate with Kahan summation, and say what `-ffast-math` changes | Sum 0.1 ten million times: naive? (999,999.9998389754) Kahan? (1,000,000.0000000000) Kahan under `-ffast-math`? (999,999.9998389754 again: the compensation was optimised away [verified]) | `float-inspector` (summation), `predict-output` (C++) | Trap: `-ffast-math` is a free speed-up (it lets the compiler reorder sums, delete compensation and assume no NaN: `std::isnan` returned false for a NaN [verified]). Edge: `std::fma`; a reduction's order changes the last digits | T, T, C, N |
| 65 | `lsn.cppstl.monte-carlo` A Monte Carlo pricer | Write a Monte Carlo pricer for a European call under geometric Brownian motion with a standard error and antithetic draws | A 1-year at-the-money call on 100 at 5% and 20% volatility from $10^6$ paths: the estimate and its standard error, against 10.4506 | `code-cell` (C++), `sim-runner`, `plot-2d` | Trap: an estimate without its standard error, or one seed for every run when measuring the error. Edge: $S_T = S_0 e^{(r - \sigma^2/2)T + \sigma\sqrt{T}Z}$; antithetic pairs cut the variance for monotone payoffs | N, C, M, K |
| 66 | `lsn.cppstl.black-scholes` Black-Scholes in C++ | Implement Black-Scholes with the normal CDF as $\frac12 \operatorname{erfc}(-x/\sqrt2)$, accurate in the tails | $N(-10)$ by `0.5 * (1 + erf(x / sqrt(2)))` and by `0.5 * erfc(-x / sqrt(2))`? (0 against $7.6 \times 10^{-24}$ [verified]) | `float-inspector`, `code-cell` (C++) | Trap: the `erf` form (cancellation destroys the far tail). Edge: $T \to 0$ and $\sigma \to 0$ need explicit handling; put-call parity as a test | N, C, M, K |
| 67 | `lsn.cppstl.numerical-testing` Testing numerical code | Test numerical code with relative tolerances, properties and reference values | Which tests catch a pricer that swaps $d_1$ and $d_2$: put-call parity, monotonicity in strike, a reference value, or all three? | `code-cell` (C++ tests), `mutant-hunter` [mode to add: cpp] | Trap: tight absolute tolerances on large values. Edge: bounds such as $\max(S - Ke^{-rT}, 0) \le C \le S$ catch bugs a single reference value misses | M, C, K, S |

Transfer screens: lesson 63 makes a risk simulation reproducible for an audit; lesson 65 starts the Monte Carlo pricer project; lesson 66 prices deep out-of-the-money options without losing them to rounding.

#### Course CP: Performance and the Pricer (`crs.cpppricing`, 4 levels, 21 lessons)

The tools of a working C++ engineer, measured performance, the 1.9 exit's binomial pricer, and a first contact with threads. Drepper's paper on memory, two conference talks and the CS106L lectures on special members run alongside; canon-gap P13 continues this course for developers.

**Level CP1: Tools of a C++ Engineer** (`lvl.cpppricing.tools`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 68 | `lsn.cpppricing.warnings-sanitisers` Warnings and sanitisers | Build with warnings as errors during development and sanitisers during testing, and find real bugs among warnings | A project has 12 warnings under `-Wall -Wextra`. Which three hide real bugs? | `diagnostic-reader` (gcc, clang, asan, ubsan), `compile-pipeline` (flags) | Trap: silencing a warning with a cast. Edge: sanitisers slow a program severalfold [recalled], so timing runs never use them; `-fsanitize=thread` for races (lesson 86) | R, M, C, O |
| 69 | `lsn.cpppricing.debugger` Debugging with gdb or lldb | Run a program under a debugger: breakpoints, backtraces, stepping and watchpoints | A crash with no message: get a backtrace and the faulting line | `text-terminal` (recorded session), `code-tracer` | Trap: debugging an optimised build without `-g` (variables are "optimised out" and lines jump). Edge: core dumps; a watchpoint finds who changes a value | O, C, S, R |
| 70 | `lsn.cpppricing.cmake-projects` CMake projects | Structure a CMake project with a library, an executable and a test target, built in Debug and Release | A pricer built with no `CMAKE_BUILD_TYPE` is timed. Is it optimised? (no: with a single-configuration generator and no build type, no optimisation flag is added [recalled; check on the pinned CMake]) | `compile-pipeline` (cmake), `text-terminal` | Trap: timing a Debug build. Edge: `ctest` runs the test target; `target_compile_options` per target | C, O, E, K |
| 71 | `lsn.cpppricing.review` Reading and reviewing C++ | Review C++ against the C++ Core Guidelines (ownership, `const`, names, errors), and apply clang-format and clang-tidy | Review a 40-line pricer: mark the five problems a senior engineer would raise | `code-review` (C++), `code-annotator` | Trap: "it compiles and passes" is the bar. Edge: raw owning pointers, magic numbers, `using namespace std;` in a header | R, M, C, S |
| 72 | `lsn.cpppricing.python-bindings` Calling C++ from Python | Expose a C++ function to Python with pybind11, and decide where the language boundary should sit | Price 10,000 options: call C++ once per option, or once with all 10,000? (once: every crossing has a fixed cost) | `code-annotator` (recorded), `bench-lab` (recorded) | Trap: crossing the boundary inside a tight loop. Edge: NumPy arrays pass without copying through the buffer protocol; nanobind is a lighter alternative [recalled] | C, N, S, O |

Transfer screens: lesson 68 sets up a library's CI flags; lesson 72 is how a researcher's Python backtest calls a desk's C++ pricer.

**Level CP2: Performance** (`lvl.cpppricing.performance`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 73 | `lsn.cpppricing.cache-locality` Cache locality | Explain cache lines and predict how traversal order changes speed | Sum a 4096 × 4096 matrix of doubles by rows, then by columns. Ratio? (about 10 times slower by columns on one machine [measured]; the counted model: one line load per 8 elements against one per element) | `memory-layout` (cache), `bench-lab` (recorded) | Trap: equal big-O means equal speed. Edge: lines are 64 bytes; strides that are large powers of two can be worse still [recalled] | N, C, N, P |
| 74 | `lsn.cpppricing.vector-vs-list` Why a vector beats a list | Explain from pointer chasing and cache misses why a vector beats a linked list for most workloads | Sorted insertion of 10,000 and of 50,000 values: list against vector? (13 and 21 times slower for the list on one machine [measured]) | `bench-lab` (recorded), `memory-layout` (pointers) | Trap: "lists insert in $O(1)$, so they are faster". Edge: lists keep iterators valid and splice in $O(1)$, which sometimes decides | C, N, N, S |
| 75 | `lsn.cpppricing.benchmarking` Benchmarking honestly | Benchmark with the right optimisation level, warm-up, repeats, median and spread, and stop dead-code elimination | A benchmark reports 0 ns for a pricing loop. What happened? (the compiler removed work whose result was unused) | `bench-lab` (rigorous) | Trap: one run, or a result nobody reads. Edge: write results to a `volatile` sink or use Google Benchmark's `DoNotOptimize`; `-O0` against `-O2` was 11 times slower for the pricer at $N = 1{,}000$ [measured]; frequency scaling adds spread | C, N, R, O |
| 76 | `lsn.cpppricing.profiling` Profiling before optimising | Find the hot spot with a sampling profiler before changing code | A flame chart of a backtest: which function first? | `bench-lab` (profile), `code-annotator` | Trap: optimising the function you suspect. Edge: inlining hides frames; profile a Release build with `-g` | R, C, M, S |
| 77 | `lsn.cpppricing.allocation` Allocation costs | Remove allocations from hot loops with `reserve`, reuse and references, and explain the small-string optimisation | A function builds a `std::string` key for every tick. Where does the time go? (heap allocation for keys longer than 15 characters, libstdc++'s inline capacity [verified]) | `bench-lab` (recorded), `memory-layout` | Trap: allocation is free. Edge: pools and arenas; `string_view` keys avoid copies but must not dangle | N, C, T, K |
| 78 | `lsn.cpppricing.hidden-costs` Subnormal numbers and vectorisation | Recognise two hidden costs in numerical loops, subnormal numbers and loops the compiler cannot vectorise, and fix each | The pricer takes 0.0015 s at $N = 2{,}000$ and 0.49 s at $N = 10{,}000$: 25 times the work, 330 times the time. Why? (6.6% of the node values are subnormal, which this CPU handles slowly; flushing them to zero gave 0.039 s [measured]) | `bench-lab` [mode to add: denormals], `float-inspector` | Trap: `-ffast-math` as the fix (it flushes subnormals but also changes results, lesson 64; clamping values below $10^{-300}$ to zero is the targeted fix). Edge: aliasing blocks vectorisation (`__restrict`); a floating reduction vectorises only if reassociation is allowed | N, C, M, K |

Transfer screens: lesson 73 lays out a returns matrix for the risk loop's access pattern; lesson 78 is a real failure of naive binomial pricers at large $N$, met again in the exit.

**Level CP3: The Binomial Pricer in C++** (`lvl.cpppricing.pricer`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 79 | `lsn.cpppricing.binomial-design` Designing the pricer | Design the interface and data: an option struct, CRR parameters, and one vector of length $N + 1$ overwritten backwards | The whole tree or one vector? At $N = 10{,}000$ the tree holds 50,015,001 nodes, about 400 MB of doubles, against 80 KB for one vector | `code-tracer` (C++), `binomial-tree` (calc-linalg), `code-cell` (C++) | Trap: storing every node. Edge: $N = 1$ is one step (12.1623 for $S = K = 100$, $T = 1$, $r = 5\%$, $\sigma = 20\%$ [verified]); $u = e^{\sigma\sqrt{\Delta t}}$, $d = 1/u$, $q = \frac{e^{r\Delta t} - d}{u - d}$ | N, N, C, K |
| 80 | `lsn.cpppricing.binomial-tests` Tests first | Write tests before optimising: put-call parity in the tree, convergence to Black-Scholes, bounds, American against European | Which hold at $N = 1{,}000$ to $10^{-10}$: parity, equality with Black-Scholes, the American put above the European? (parity, to about $10^{-12}$; the American put, 6.0896, is above the European, 5.5715; Black-Scholes differs by 0.0020 [verified]) | `code-cell` (C++ tests), `mutant-hunter` [mode to add: cpp] | Trap: one hard-coded expected number. Edge: deep in- and out-of-the-money strikes; $N = 1$ | M, C, K, S |
| 81 | `lsn.cpppricing.american-exercise` American exercise | Add early exercise to the backward step as $\max(\text{continuation}, \text{intrinsic})$ at each node's own price | Where does the intrinsic value come from: the root price or the node's price? (the node's, $S u^j d^{i - j}$) | `code-tracer` (C++), `binomial-tree` | Trap: intrinsic value from the root price. Edge: an American call on a stock without dividends equals the European call; with $r = 0$ the American put equals the European put (both [verified]) | C, T, M, K |
| 82 | `lsn.cpppricing.timing-protocol` Timing against Python honestly | Time C++ and Python at the same $N$, with repeats, median and spread, and report a speed-up with an interval | At $N = 2{,}000$ on one machine: pure Python 0.166 s, NumPy 0.0079 s, C++ 0.0015 s [measured]. Which speed-up should the exit report, and against which Python? | `bench-lab` (rigorous) | Trap: a Debug C++ build against optimised NumPy, or Python's start-up inside a one-shot timing. Edge: report the speed-up against the learner's own 1.7 version, stating whether it uses loops or NumPy | N, C, N, O |
| 83 | `lsn.cpppricing.convergence` Convergence and odd-even oscillation | Measure the CRR price's convergence to Black-Scholes, see the odd-even oscillation, and average neighbours to reduce it | Errors at $N = 1{,}000$ and $1{,}001$? (−0.0020 and +0.0018 [verified]) | `plot-2d`, `code-cell` (C++) | Trap: the error falls steadily with $N$. Edge: at the money the error shrinks roughly like $1/N$ (−0.0020 at 1,000, −0.0010 at 2,000 [verified]); averaging $N$ and $N + 1$ cancels most of the oscillation | N, C, M, K |
| 84 | `lsn.cpppricing.exit-build` Building the exit | Assemble the exit repository (library, tests, benchmark target, README) and paste-verify it | What must the pasted output show? (the doctest summary with every case passing; both timings with repeats; compiler and flags) | `setup-checklist` (exit-1.9), `compile-pipeline` (cmake) | Trap: committing the build folder, or timing with sanitisers on. Edge: timings differ across machines and compilers; record both | O, M, C, S |

Transfer screens: the whole level is the 1.9 exit (section 4.4); lesson 83 is the convergence check a desk runs before trusting a tree pricer.

**Level CP4: First Contact with Concurrency** (`lvl.cpppricing.concurrency`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 85 | `lsn.cpppricing.threads` Threads and data races | Start and join threads with `std::jthread`, and explain why a data race is undefined behaviour | Two threads each add 1 to a shared `long` a million times. The result? (1,156,720 and 1,247,797 in two runs, not 2,000,000 [verified]) | `code-tracer` (C++ threads, recorded), `diagnostic-reader` (tsan) | Trap: `++counter` is one indivisible step (it is a load, an add and a store). Edge: ThreadSanitizer reports "data race" with both stacks [verified] | N, C, T, R |
| 86 | `lsn.cpppricing.mutex-atomic` Mutexes and atomics | Protect shared data with `std::mutex` and `std::lock_guard`, or a single variable with `std::atomic`, and avoid deadlock | Make the counter correct in two ways. Which is faster here? | `code-cell` (C++ recorded), `bench-lab` (recorded) | Trap: an `atomic` makes compound logic atomic (each operation is atomic; check-then-act is not). Edge: two locks taken in different orders deadlock; `std::scoped_lock` takes both safely | C, M, T, K |
| 87 | `lsn.cpppricing.parallel-monte-carlo` A parallel Monte Carlo pricer | Parallelise the Monte Carlo pricer with one engine per thread, distinct seeds and a final reduction | Four threads share one `std::mt19937`. Two problems? (a data race, and overlapping or correlated draws) | `code-cell` (C++ recorded), `sim-runner` | Trap: one shared engine. Edge: Amdahl's law caps the speed-up by the serial fraction; reproducible results need fixed per-thread seeds | M, C, N, K |
| 88 | `lsn.cpppricing.false-sharing` False sharing | Explain false sharing and fix it by padding per-thread data to a cache line | Four threads increment their own counters in one array: 1.47 s; padded to 64 bytes each: 0.14 s [measured]. Why? (the counters shared one cache line) | `memory-layout` [mode to add: false-sharing], `bench-lab` (recorded) | Trap: separate variables cannot interfere. Edge: `std::hardware_destructive_interference_size` is 64 on GCC 13 and absent from Clang 18 with libstdc++ 13 [verified]; the developer track continues in canon-gap P13 | N, C, M, S |

Transfer screens: lesson 87 runs a risk simulation across cores; lesson 88 explains a slow multi-threaded position aggregator. Level CP4 is core for the developer track and optional practice for the others, which still take its lessons because the paper samples them lightly (section 4.2).

### 2.3 Item 2.4 Contests

Lessons marked ◆ form the 36-lesson core kept if canon-gap O1 is accepted (section 1.3). Every problem is original and Codeforces-style (statement, constraints, input and output format, examples); real Codeforces, CSES and Project Euler problems are linked, never copied (`widgets-programming.md` 9).

#### Course KC: Contest Craft (`crs.contestcraft`, 4 levels, 21 lessons)

How contests work and how to practise for them: reading constraints, fast input, the ad hoc thinking behind most Div. 2 A to C problems, searching under contest limits, and the practice loop of stress tests, upsolving and virtual contests. It ends with the competitions the curriculum adds for each track. CPH chapters 1 to 6 and the USACO Guide's Bronze and Silver modules run alongside.

**Level KC1: How Contests Work** (`lvl.contestcraft.basics`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | ◆ `lsn.contestcraft.contest-formats` How contests run | Explain divisions, scoring, penalties, verdicts, hacks, virtual participation, upsolving and rating, and what a rating does and does not show | A guided replay of a finished Div. 2 round: why did the contestant who solved fewer problems rank higher? (fewer wrong submissions and earlier solves) | `contest-arena` (tour) | Trap: a rating measures skill at each problem (it measures results in timed contests against other people). Edge: divisions are set by rating bands [check current thresholds]; the curriculum's note that rating shortlists are mainly an Indian campus practice | C, N, S, O |
| 2 | ◆ `lsn.contestcraft.reading-statements` Reading a statement | Derive the target complexity from the constraints, including multiple test cases with a bounded sum of $n$, and list edge cases from the constraints | $t \le 10^4$ tests, each $n \le 2 \times 10^5$, the sum of $n$ at most $2 \times 10^5$: is $O(n \log n)$ per test fine? Is $O(n^2)$? (yes; no) | `complexity-lab` (budget), `problem-workbench` (contest) | Trap: per-test complexity without the sum guarantee (or resetting a $10^6$ array for each of $10^4$ tests). Edge: $n = 1$; values up to $10^9$ make sums exceed 32 bits | M, C, N, N |
| 3 | ◆ `lsn.contestcraft.python-speed` Python at contest speed | Make an $O(n)$ Python solution pass a time limit with buffered input, joined output, and iterative code | A correct Python solution gets "Time limit exceeded on test 9" although its loop is $O(n)$. What else costs time? (one `input()` and one `print()` per line) | `code-cell` (stdin tests), `bench-lab` (race) | Trap: only the algorithm matters (the constant factor of I/O dominates at $2 \times 10^5$ lines). Edge: `sys.stdin.buffer.read().split()`; recursion limits; PyPy is offered on Codeforces and is usually much faster for loops [recalled] | C, T, K, T |
| 4 | ◆ `lsn.contestcraft.cpp-template` A C++ contest template | Write a contest template with fast I/O, `long long` and debugging output, and know what each line does | $n \le 10^5$ values up to $10^5$: their pairwise product in an `int`? ($10^{10}$ overflows) | `code-cell` (C++), `diagnostic-reader` | Trap: `std::endl` in output loops (it flushes every line). Edge: `std::ios::sync_with_stdio(false); std::cin.tie(nullptr);`; `<bits/stdc++.h>` is a libstdc++ header, so it works with GCC and with Clang on Linux but not with MSVC [recalled] | T, C, M, K |
| 5 | ◆ `lsn.contestcraft.implementation` Implementation problems | Solve simulation and case-analysis problems by listing every case before coding | Simulate a queue of customers on a grid of service desks for 100 steps, with ties broken by desk number | `problem-workbench` (contest) | Trap: coding before listing the cases. Edge: $n = 1$; ties; the first and last steps | K, C, O, K |

Transfer screens: lesson 2 reads constraints as a production capacity estimate; lesson 3 is the same I/O cost that slows a Python market data parser.

**Level KC2: Ad Hoc Thinking** (`lvl.contestcraft.adhoc`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 6 | ◆ `lsn.contestcraft.invariants-parity` Invariants and parity | Find a quantity an operation cannot change, and use it to prove a target unreachable or to compute a cost | Chips at positions [2, 2, 2, 3, 3]: moving a chip by 2 is free, by 1 costs 1. Cheapest way to gather them? (2: move the two odd chips) | `counterexample-lab` (claim), `array-strip` | Trap: simulating moves instead of finding what never changes. Edge: parity of inversions decides whether swaps can sort; an invariant proves impossibility, not possibility | N, C, M, K |
| 7 | ◆ `lsn.contestcraft.frequency-mex` Frequency arrays and the MEX | Count with arrays indexed by value, and compute the MEX (smallest missing non-negative integer) | The MEX of [0, 1, 3, 4]? (2) | `array-strip`, `hash-table` | Trap: sorting when values are small (a count array is $O(n + V)$). Edge: the MEX of $n$ values is at most $n$, so values above $n$ can be ignored | N, C, K, T |
| 8 | ◆ `lsn.contestcraft.constructive` Constructive problems | Build any valid answer to a specification, prove it valid, and recognise impossible cases | A permutation of 1 to $n$ with no two neighbours differing by 1: for which $n$ does one exist? (every $n$ except 2 and 3: evens then odds, such as 2, 4, 1, 3) | `code-cell` (checker tests) | Trap: searching for "the" answer (any valid one is accepted). Edge: $n = 1$; output $-1$ exactly when impossible | R, K, C, M |
| 9 | ◆ `lsn.contestcraft.greedy-at-speed` Greedy proofs at contest speed | Find and justify a greedy rule in a few minutes with an exchange argument or a counterexample search | Pair dancers whose skill levels differ by at most 1: boys [1, 4, 6, 2], girls [5, 1, 5, 7, 9]. Most pairs? (3: sort both, match from the smallest) | `counterexample-lab` (greedy), `pointer-walk` | Trap: submitting an unproven greedy and burning penalties. Edge: ties; a brute force on small inputs checks the rule before submitting | N, C, O, K |
| 10 | ◆ `lsn.contestcraft.small-n` Brute force when $n$ is small | Recognise constraints that invite exhaustive search ($n \le 8$, $n \le 20$) and write it quickly and correctly | $n \le 8$: try all orders? (8! = 40,320) $n \le 20$: all subsets? ($2^{20} \approx 10^6$) | `complexity-lab` (budget), `code-cell` | Trap: dismissing brute force as too slow without computing the count. Edge: $n \le 40$ suggests meet in the middle (lesson 79) | N, M, C, K |
| 11 | ◆ `lsn.contestcraft.prefix-tricks` Prefix tricks at contest scale | Count subarrays with a property using prefix sums, prefix XOR and counts of earlier prefixes | Subarrays of [4, 2, 2, 6, 4] whose XOR is 6? (4) | `range-query-lab` (prefix), `hash-table` | Trap: an $O(n^2)$ scan over pairs of ends. Edge: the empty prefix counts once; prefix XOR works because $x \oplus x = 0$ | N, C, T, K |

Transfer screens: lesson 6 proves a rebalancing target unreachable from lot constraints; lesson 11 counts periods whose net signed volume cancels.

**Level KC3: Searching under Contest Limits** (`lvl.contestcraft.search`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 12 | ◆ `lsn.contestcraft.answer-search` Binary search on huge answers | Binary-search answers up to $10^{18}$ with checks that cannot overflow | $k$ machines take $t_i$ seconds per item: the least time to make $M = 10^9$ items? Check: $\sum \lfloor T / t_i \rfloor \ge M$ | `binary-search-lab` (predicate) | Trap: an overflowing check (stop summing once the total reaches $M$; `mid * mid` overflows `long long` near $10^{18}$). Edge: the answer at the upper bound | N, C, N, K |
| 13 | ◆ `lsn.contestcraft.pointers-scale` Two pointers and windows at scale | Count pairs and windows with two pointers on $2 \times 10^5$ values | Pairs $i < j$ with $a_i + a_j \le S$ in a sorted array, in $O(n)$ | `pointer-walk` (opposite) | Trap: counting each pair twice or including $i = j$. Edge: duplicates; all pairs qualify | N, G, C, K |
| 14 | ◆ `lsn.contestcraft.ternary-search` Ternary search | Find the maximum of a unimodal function by ternary search, and spot functions with flat stretches where it fails | Revenue $p(100 - p)$ over integer prices: the best price? (50, revenue 2,500) | `binary-search-lab` [mode to add: ternary], `plot-2d` | Trap: ternary search on a function with plateaus (it can discard the maximum). Edge: on integers, stop when the range is small and check every point; a convex function's minimum is also found by binary search on the slope | N, C, G, K |
| 15 | ◆ `lsn.contestcraft.interactive` Interactive problems | Solve problems where the judge answers queries, flushing output and staying within the query limit | Guess a number in $[1, 10^9]$ from "higher" or "lower" in at most 30 queries (the limit is $\lceil \log_2 10^9 \rceil = 30$) | `code-cell` [mode to add: interactive judge] | Trap: forgetting to flush after each query (the program and the judge both wait). Edge: adaptive judges that choose the answer as you ask; reading "-1" means stop at once | N, C, O, K |

Transfer screens: lesson 12 sizes a batch job's runtime; lesson 15 is the protocol pattern of a request-response market interface.

**Level KC4: Practice Discipline and Other Competitions** (`lvl.contestcraft.practice`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 16 | ◆ `lsn.contestcraft.stress-hack` Stress testing and hacking | Write a generator, a brute force and a comparison loop, and build inputs that break wrong or slow solutions, including hash-table attacks | Break a submission that sorts with a non-strict comparator, and another that uses `unordered_map` with default hashing | `counterexample-lab` (stress, hack) | Trap: random tests catch everything (they rarely hit the edge structure or the worst case). Edge: anti-hash inputs against `unordered_map` exist and are used in hacks [recalled]; a custom hash with a random seed defends against them | G, C, M, K |
| 17 | ◆ `lsn.contestcraft.debug-wa` Debugging a wrong answer under time | Find a wrong answer's cause quickly: re-read the statement, check overflow and edge cases, assert invariants | "Wrong answer on test 2" with every example passing: the five checks to run first | `diagnostic-reader`, `problem-workbench` (contest) | Trap: changing code at random. Edge: overflow is the commonest single cause in C++ [recalled]; output format (spaces, case) | O, M, C, S |
| 18 | ◆ `lsn.contestcraft.upsolving` Upsolving and editorials | Practise deliberately: try for 30 to 45 minutes before reading an editorial, then solve again from scratch a week later | A practice plan for the week after a contest with two unsolved problems | `contest-arena` (upsolve list) | Trap: reading the editorial at once, or never returning to the problem. Edge: problems rated about 200 above your rating give the most growth [recalled rule of thumb]; the Redo queue schedules the re-solve | O, C, M, S |
| 19 | ◆ `lsn.contestcraft.virtual-contest` Contest strategy | Plan a two-hour contest: read every problem, order by expected value, manage penalties, and use the last 15 minutes | A virtual round against the ghost scoreboard | `contest-arena` | Trap: sinking 90 minutes into problem C while B is unsolved. Edge: under Codeforces scoring, points fall with time, so early solves matter | O, C, M, K |
| 20 | ◆ `lsn.contestcraft.project-euler` Project Euler: maths with code | Solve number problems that reward maths over brute force, with exact integer arithmetic | The sum of all primes below 2,000,000, without testing each number by trial division | `number-theory-lab` (sieve), `code-cell` (answer) | Trap: floating point for large integers. Edge: answers above $2^{63}$ need Python or 128-bit integers; Project Euler asks solvers not to publish solutions to problems beyond the first hundred [recalled] | N, C, M, K |
| 21 | ◆ `lsn.contestcraft.kaggle-trading` Kaggle and trading competitions | Explain how Kaggle competitions and firm-run trading competitions are scored and won, and the overfitting traps of each | A leaderboard climber drops 300 places when the private leaderboard is revealed. Why? (they tuned to the public test sample) | `choice`, links to 2.1 and the finance cluster | Trap: chasing the public leaderboard (Kaggle) or fitting the sample days (trading competitions). Edge: IMC Prosperity-style rounds score P&L under position limits [check the current format]; the researcher and trader tracks take one of these instead of some contests | C, M, S, O |

Transfer screens: lesson 16 is how a desk tests a new pricer against a slow reference; lesson 21 maps directly onto 2.1's validation discipline and 3.3's market-making games.

#### Course KM: Contest Mathematics (`crs.contestmath`, 5 levels, 26 lessons)

Number theory, modular arithmetic, counting, probability, games and integer geometry as contests use them. CPH chapters 21 to 25 and 29 run alongside; `number-theory-lab` carries the arithmetic.

**Level KM1: Primes and Divisibility** (`lvl.contestmath.primes`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 22 | ◆ `lsn.contestmath.trial-division` Trial division and $\sqrt{n}$ | Test primality and list divisors by trial division up to $\sqrt{n}$, and say why the bound is enough | Is $10^9 + 7$ prime? How many trial divisions? (yes; at most 31,622) | `number-theory-lab` (divisors) | Trap: looping to $n$ or $n/2$. Edge: 1 is not prime; a perfect square's root is one divisor, not two | N, C, T, K |
| 23 | ◆ `lsn.contestmath.sieve` The sieve of Eratosthenes | Sieve primes up to $N$ in $O(N \log \log N)$, starting each prime's crossing at $p^2$, and build a smallest-prime-factor table | Primes below 100 and below $10^6$? (25 and 78,498) | `number-theory-lab` (sieve) | Trap: crossing out from $2p$ or sieving to $N$ for every prime (stop at $\sqrt{N}$). Edge: a smallest-prime-factor sieve factorises any number up to $N$ in $O(\log N)$ | N, N, C, K |
| 24 | ◆ `lsn.contestmath.divisor-functions` Factorisations and divisor functions | Count and sum divisors from a prime factorisation, as multiplicative functions | Divisors of $360 = 2^3 \cdot 3^2 \cdot 5$? (24; their sum is 1,170) | `number-theory-lab` (divisors), `factor-tree` (Stage 0) | Trap: adding exponents instead of multiplying $(e_i + 1)$. Edge: below $10^4$ the most divisors is 64, at 7,560; numbers below $10^9$ have at most 1,344 divisors [recalled] | N, N, C, K |
| 25 | ◆ `lsn.contestmath.euclid` Euclid's algorithm | Compute gcd and lcm with Euclid's algorithm, seen as cutting squares from a rectangle, and bound its steps | $\gcd(1071, 462)$? (21, in 3 steps) Tile a 21 × 8 rectangle with the largest squares: the last square's side? (1) | `number-theory-lab` (euclid) | Trap: $\mathrm{lcm}(a, b) = a \cdot b / \gcd$ overflows (divide first). Edge: $\gcd(a, 0) = a$; consecutive Fibonacci numbers are the worst case | N, N, C, K |
| 26 | ◆ `lsn.contestmath.extended-euclid` Extended Euclid and linear equations | Find integers $x, y$ with $ax + by = \gcd(a, b)$, and solve $ax + by = c$ or show it has no solution | $240x + 46y = 2$? ($x = -9$, $y = 47$) | `number-theory-lab` (extended) | Trap: expecting a solution when $\gcd(a, b)$ does not divide $c$. Edge: all solutions are $x + k\frac{b}{g}$, $y - k\frac{a}{g}$; negative coefficients | X, N, C, K |
| 27 | ◆ `lsn.contestmath.totient` Euler's totient | Compute $\varphi(n)$ from the factorisation and count integers coprime to $n$ | $\varphi(36)$? (12) $\varphi(97)$? (96) | `number-theory-lab` (divisors) | Trap: $\varphi(ab) = \varphi(a)\varphi(b)$ for any $a, b$ (only when coprime). Edge: a totient sieve gives $\varphi$ up to $N$ in one pass | N, N, C, K |

**Level KM2: Modular Arithmetic** (`lvl.contestmath.modular`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 28 | ◆ `lsn.contestmath.mod-rules` Working modulo $m$ | Add, subtract and multiply modulo $m$ without overflow, and normalise negative remainders | $-7 \bmod 3$ in Python and in C++? (2 and −1 [verified]) | `number-theory-lab` (clock), `modular-clock` (Stage 0) | Trap: `(a - b) % m` in C++ can be negative (use `((a - b) % m + m) % m`). Edge: products of two values below $10^9 + 7$ need 64 bits | T, T, C, K |
| 29 | ◆ `lsn.contestmath.mod-pow` Fast modular exponentiation and Fermat | Compute $a^e \bmod m$ in $O(\log e)$ and use Fermat's little theorem for prime moduli | $3^{-1} \bmod 11$ by Fermat as $3^{9} \bmod 11$? (4) | `number-theory-lab` (modpow), `bit-lab` (power) | Trap: computing $a^e$ first and reducing at the end. Edge: Fermat needs a prime modulus and $a \not\equiv 0$ | N, N, C, K |
| 30 | ◆ `lsn.contestmath.mod-inverse` Modular inverses and division | Divide modulo a prime with inverses, and modulo any $m$ with extended Euclid when the inverse exists | $2^{-1} \bmod 998{,}244{,}353$? (499,122,177) | `number-theory-lab` (extended, modpow) | Trap: dividing remainders as ordinary numbers. Edge: an inverse exists only when $\gcd(a, m) = 1$; 998,244,353 $= 119 \cdot 2^{23} + 1$ is prime [verified] | N, C, M, K |
| 31 | ◆ `lsn.contestmath.ncr-mod` $\binom{n}{k}$ modulo a prime | Precompute factorials and inverse factorials to answer $\binom{n}{k} \bmod p$ in $O(1)$ | $\binom{10^5}{5 \times 10^4} \bmod (10^9 + 7)$? (149,033,233) | `number-theory-lab` (ncr), `pascal-triangle` (Stage 0) | Trap: building Pascal's triangle to $10^5$ ($10^{10}$ cells). Edge: $k > n$ gives 0; compute inverse factorials downwards from one Fermat inverse | N, C, M, K |
| 32 | ◆ `lsn.contestmath.crt` The Chinese remainder theorem | Combine congruences with coprime moduli into one, and detect conflicting ones when moduli share factors | $x \equiv 2 \pmod 3$, $x \equiv 3 \pmod 5$, $x \equiv 2 \pmod 7$? ($x \equiv 23 \pmod{105}$) | `number-theory-lab` [mode to add: crt] | Trap: assuming a solution exists for non-coprime moduli. Edge: combine two congruences at a time with extended Euclid | N, C, M, K |

Transfer screens: lesson 29 is the arithmetic behind the rolling hashes of 1.8 lesson 37; lesson 31 counts paths in large lattices exactly.

**Level KM3: Counting** (`lvl.contestmath.counting`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 33 | ◆ `lsn.contestmath.contribution` Stars and bars, and counting by contribution | Count distributions with stars and bars, and sum over all subarrays or pairs by counting each element's contribution | 10 identical lots among 4 desks? (286; 84 if each desk gets one) Sum of the minimums of all subarrays of [3, 1, 2, 4]? (17) | `counting-slots` (Stage 0), `stack-queue-lab` (monotonic-stack) | Trap: enumerating every subarray ($O(n^2)$). Edge: each element is the minimum of (left span) × (right span) subarrays, with ties broken on one side only | N, N, C, K |
| 34 | `lsn.contestmath.inclusion-exclusion` Inclusion-exclusion over subsets | Count integers up to $N$ divisible by at least one of a set of primes by inclusion-exclusion over subsets | Integers up to $10^{18}$ divisible by 2, 3 or 5? (733,333,333,333,333,334) | `venn-diagram` (Stage 0), `bit-lab` [mode to add: subsets] | Trap: adding the three counts (overlaps counted twice). Edge: $2^k$ subsets for $k$ primes; signs alternate with subset size | N, C, X, K |
| 35 | `lsn.contestmath.catalan` Bracket sequences and Catalan numbers | Check bracket sequences by prefix balance and count them with $\frac{1}{n + 1}\binom{2n}{n} \bmod p$ | Balanced sequences of length 20, modulo $10^9 + 7$? (16,796) | `number-theory-lab` (ncr) | Trap: re-deriving the count by reflection each time (1.5 lesson 138 proved it). Edge: a sequence is balanced exactly when no prefix balance is negative and the total is 0 | N, C, M, K |
| 36 | `lsn.contestmath.pigeonhole` Pigeonhole and existence | Prove that a solution exists with the pigeonhole principle and find it with prefix sums modulo $n$ | Among any $n$ integers, some non-empty contiguous block has a sum divisible by $n$. Find one in [3, 1, 4, 1, 5] | `range-query-lab` (prefix), `hash-table` | Trap: searching all blocks ($O(n^2)$) when two equal prefix remainders name one at once. Edge: a zero prefix remainder is itself a block from the start | N, C, O, K |
| 37 | `lsn.contestmath.matrix-power` Matrix powers for linear recurrences | Compute the $n$th term of a linear recurrence in $O(k^3 \log n)$ by raising its companion matrix to a power modulo $p$ | $F_{10^{18}} \bmod (10^9 + 7)$? (209,783,453) | `matrix-multiply` (calc-linalg), `bit-lab` (power) | Trap: iterating $10^{18}$ steps. Edge: the matrix's order (row times column) and the index convention ($F_1 = F_2 = 1$) | N, C, M, K |


**Level KM4: Probability and Games** (`lvl.contestmath.games`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 38 | ◆ `lsn.contestmath.expected-linearity` Expected values by linearity | Compute expected counts in contest problems by summing indicator expectations | The expected number of inversions in a random permutation of 10 items? ($\frac{45}{2}$) | `indicator-board` (prob-stats), `cell-grid` (pair grid) | Trap: enumerating outcomes. Edge: linearity needs no independence (1.5 lesson 52); answers are often asked modulo a prime | N, C, X, K |
| 39 | `lsn.contestmath.prob-mod` Probabilities modulo a prime | Report a probability $\frac{p}{q}$ as $p \cdot q^{-1} \bmod M$, and compute it without fractions | $\frac13 \bmod 998{,}244{,}353$? (332,748,118) | `number-theory-lab` (modpow) | Trap: computing the decimal first. Edge: $q$ must not be a multiple of $M$; check by multiplying back | N, C, M, K |
| 40 | `lsn.contestmath.expected-dp` Expected-value DP | Compute expected steps and probabilities by DP over states | The expected number of fair-die rolls to reach a running total of at least 10? (about 3.32: exactly $\frac{33{,}495{,}175}{10{,}077{,}696}$) | `dp-table` (1d), `first-step-solver` (prob-stats) | Trap: averaging outcomes forward instead of conditioning on the first step. Edge: states that loop back need equations, not one pass | N, C, X, K |
| 41 | ◆ `lsn.contestmath.win-lose` Winning and losing positions | Classify positions of an impartial game as winning or losing by working back from the end | Take 1, 3 or 4 stones; whoever cannot move loses. Which piles up to 20 lose for the player to move? (0, 2, 7, 9, 14, 16: piles that are 0 or 2 modulo 7) | `dp-table` (1d), `game-lab` (prob-stats) | Trap: guessing a pattern from three values. Edge: a position is losing exactly when every move leads to a winning one | R, N, C, K |
| 42 | `lsn.contestmath.nim` Nim and XOR | Decide Nim by the XOR of the heap sizes and find a winning move | Heaps 3, 4, 5: who wins, and how? (the first player: take 2 from the heap of 3, leaving XOR 0) | `bit-lab` (ops), `game-lab` | Trap: the sum of the heaps decides. Edge: misère Nim differs only when every heap has size 1 [recalled] | N, C, G, K |
| 43 | `lsn.contestmath.sprague-grundy` Sprague-Grundy values | Compute Grundy values as the MEX of the options' values, and combine games by XOR | Take 1, 2 or 3 stones: the Grundy value of a pile of $n$? ($n \bmod 4$) | `dp-table` (1d), `number-theory-lab` [mode to add: grundy] | Trap: adding Grundy values (they combine by XOR). Edge: a Grundy value of 0 is a losing position; the MEX of lesson 7 | X, N, C, K |

Transfer screens: lesson 38 sets up the green book's expected-value questions (3.3); lesson 41 is the backward induction behind market-making game strategies.

**Level KM5: Integer Geometry** (`lvl.contestmath.geometry`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 44 | `lsn.contestmath.cross-product` Vectors and orientation | Decide left turn, right turn or collinear with an integer cross product | Are (0, 0), (1, 1) and (3, 3) collinear? (yes: the cross product is 0) | `geometry-board` (Stage 0), `plot-2d` | Trap: comparing slopes with division (division by zero, rounding). Edge: integer coordinates up to $10^9$ make products near $10^{18}$, which still fit in `long long` | N, C, M, K |
| 45 | `lsn.contestmath.polygon-area` Polygon area and lattice points | Compute polygon area with the shoelace formula and count lattice points with Pick's theorem | Triangle (0, 0), (5, 0), (2, 4): area, boundary points and interior points? (10; 8; 7) | `geometry-board` (Stage 0) | Trap: forgetting the absolute value or halving too early (work with twice the area in integers). Edge: boundary points on a segment are $\gcd(|\Delta x|, |\Delta y|)$ | N, N, C, K |
| 46 | `lsn.contestmath.convex-hull` Convex hull | Build a convex hull in $O(n \log n)$ with Andrew's monotone chain | The hull of (0, 0), (2, 1), (4, 0), (3, 3), (1, 2), (2, 4), (0, 3)? ((0, 0), (4, 0), (3, 3), (2, 4), (0, 3)) | `geometry-board` (Stage 0), `stepper` | Trap: keeping collinear points when the task excludes them (or the reverse): the sign test decides. Edge: all points collinear; duplicates | R, C, O, K |
| 47 | `lsn.contestmath.segments-precision` Segment intersection and precision | Test segment intersection with orientations, and keep geometry exact with integers | Do segments (0, 0) to (4, 4) and (0, 4) to (4, 0) cross? Do (0, 0) to (2, 2) and (3, 3) to (5, 5)? (yes; no) | `geometry-board` (Stage 0) | Trap: floating-point equality in geometry. Edge: touching and collinear overlapping segments need the special case | C, M, N, K |

Transfer screens: lesson 46 is the efficient frontier's convex shape seen as a hull of portfolios; lesson 45 measures areas on a payoff diagram.

#### Course KS: Contest Data Structures and Graphs (`crs.contestds`, 3 levels, 19 lessons)

The structures and graph algorithms that separate a 1,400 rating from 1,900: range-query trees, trees at scale, and graph connectivity, matching and flow. CPH chapters 9, 14 to 20 and 28 run alongside; the CSES sections "Range Queries", "Tree Algorithms" and "Graph Algorithms" supply the practice [check section names].

**Level KS1: Range Queries** (`lvl.contestds.ranges`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 48 | `lsn.contestds.sparse-table` Sparse tables | Answer range-minimum queries in $O(1)$ after $O(n \log n)$ preparation, from two overlapping power-of-two blocks | $2 \times 10^5$ values and $2 \times 10^5$ minimum queries: how many levels? (18) | `range-query-lab` [mode to add: sparse], `cell-grid` | Trap: using overlapping blocks for sums (overlap double-counts; it works only for idempotent operations such as min, max and gcd). Edge: no updates allowed | N, C, M, K |
| 49 | ◆ `lsn.contestds.fenwick` Fenwick trees | Update and prefix-query in $O(\log n)$ with a Fenwick tree, walking by the lowest set bit | Which ranges does index 12 cover, and what is `12 & -12`? (the 4 values at 9 to 12; 4) | `range-query-lab` (fenwick), `bit-lab` (tricks) | Trap: zero-based indices (the walk needs one-based). Edge: counting inversions in $O(n \log n)$ with a Fenwick tree over ranks | N, G, C, K |
| 50 | `lsn.contestds.segment-tree` Segment trees | Build a segment tree for point updates and range queries, and tap the $O(\log n)$ canonical nodes a query visits | Range sums with updates on $2 \times 10^5$ values: array size for a recursive tree? ($4n$) | `range-query-lab` (segment) | Trap: an array of size $2n$ for a recursive tree on any $n$ (use $4n$, or the iterative layout). Edge: identity values for min (infinity) and sum (0) | R, N, C, K |
| 51 | `lsn.contestds.lazy-propagation` Lazy propagation | Apply range updates and range queries in $O(\log n)$ by deferring updates in tags | Add 5 to every value in $[l, r)$, then query a sum overlapping it | `range-query-lab` (segment) | Trap: forgetting to push a tag down before visiting children. Edge: composing two kinds of update (assign and add) needs an order rule | G, C, M, K |
| 52 | `lsn.contestds.compression-offline` Coordinate compression and offline queries | Compress values up to $10^9$ to ranks, and answer queries in a convenient order instead of the given one | Count, for each of $2 \times 10^5$ values, how many earlier values are smaller, with values up to $10^9$ | `range-query-lab` (fenwick), `sort-lab` | Trap: a Fenwick tree of size $10^9$. Edge: equal values share a rank; answers return in the original order | N, C, M, K |
| 53 | `lsn.contestds.order-statistics` Order-statistic sets | Find the $k$th smallest and the rank of a value in a changing set, with a Fenwick tree over ranks or GCC's policy-based tree | The median of a multiset under $2 \times 10^5$ inserts and deletes | `tree-lab` (bst), `range-query-lab` (fenwick) | Trap: sorting after each change. Edge: `__gnu_pbds::tree` is GCC-only [recalled]; binary search on a Fenwick tree finds the $k$th element in $O(\log n)$ | C, N, M, K |

**Level KS2: Trees at Scale** (`lvl.contestds.trees`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 54 | `lsn.contestds.euler-tour` Euler tours | Flatten a tree by entry and exit times so every subtree becomes a contiguous range | Subtree sums with updates on a tree of $2 \times 10^5$ nodes: a Fenwick tree over entry times | `tree-lab` [mode to add: euler-tour], `range-query-lab` | Trap: recursive DFS on a path-shaped tree of $2 \times 10^5$ nodes (stack overflow: iterate). Edge: `tin[v] <= tin[u] < tout[v]` tests ancestry | O, C, N, K |
| 55 | `lsn.contestds.binary-lifting` Binary lifting and LCA | Precompute $2^k$-th ancestors and answer LCA and $k$th-ancestor queries in $O(\log n)$ | Levels of lifting for $2 \times 10^5$ nodes? (18) | `tree-lab` [mode to add: lifting] | Trap: lifting the deeper node past the shallower one's depth. Edge: equal nodes; distance $= d_u + d_v - 2d_{\mathrm{lca}}$ | N, G, C, K |
| 56 | `lsn.contestds.diameter-centre` Diameter and centre | Find a tree's diameter with two BFS passes and its centre from the diameter path | Why does the farthest node from any start lie at one end of a diameter? | `graph-search` (bfs), `tree-lab` | Trap: one BFS from the root. Edge: weighted trees need DFS with distances; the centre is one or two nodes | N, O, C, K |
| 57 | `lsn.contestds.rerooting` DP on trees and rerooting | Compute a value for every root in $O(n)$ by rerooting a subtree DP | The sum of distances from every node to all others in a tree of $2 \times 10^5$ nodes | `tree-lab` (recursion), `dp-table` (states) | Trap: one DFS per root ($O(n^2)$). Edge: moving the root across an edge changes the sum by $n - 2 \cdot \text{size}$ | N, C, X, K |
| 58 | `lsn.contestds.small-to-large` Small-to-large merging | Merge child sets into the largest one to get $O(n \log n)$ total work | Count distinct colours in every subtree | `tree-lab`, `hash-table` | Trap: merging into the parent's set each time ($O(n^2)$ on a path). Edge: each element moves $O(\log n)$ times because its set at least doubles | N, C, M, K |
| 59 | `lsn.contestds.functional-graphs` Functional graphs | Find cycles and $k$th successors in graphs where each node has one outgoing edge, with binary lifting | Where is a token after $10^{18}$ moves along "next" pointers on $2 \times 10^5$ nodes? | `graph-search` (implicit), `linked-list-lab` (cycle) | Trap: simulating $10^{18}$ steps. Edge: every component is a cycle with trees hanging into it; Floyd's method finds each cycle (1.8 lesson 65) | N, C, M, K |

**Level KS3: Graphs at Scale** (`lvl.contestds.graphs`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 60 | `lsn.contestds.traversal-scale` Traversals and union-find at contest scale | Run iterative DFS and BFS and union-find on $2 \times 10^5$ nodes within time, and process deletions offline in reverse | Remove edges one at a time and report components after each: process the removals backwards as additions | `graph-search` (dfs), `union-find` | Trap: recursion in Python or deep recursion in C++ without care. Edge: reversing deletions into unions; resetting arrays per test case in $O(n)$ | O, C, M, K |
| 61 | `lsn.contestds.state-dijkstra` Dijkstra with state and 0-1 BFS | Run Dijkstra on (node, state) pairs, and use a deque for 0 and 1 weights | The cheapest route when one edge may be used at half price | `shortest-path` (dijkstra, zero-one) | Trap: halving the cheapest edge of the shortest path afterwards. Edge: the state space is nodes × states; 0-1 BFS pushes 0-edges to the front | N, C, G, K |
| 62 | `lsn.contestds.scc` Strongly connected components | Find SCCs with Kosaraju's two passes or Tarjan's low-links, and condense the graph into a DAG | Which pairs of 8 traders can each reach the other through a chain of credit lines? | `graph-search` [mode to add: scc] | Trap: running undirected components on a directed graph. Edge: the condensation is a DAG, so DP runs on it | R, O, C, K |
| 63 | `lsn.contestds.bridges` Bridges and articulation points | Find edges and nodes whose removal disconnects the graph with low-link values | Which single link failure splits a 9-node network? | `graph-search` [mode to add: bridges] | Trap: parallel edges are not bridges (skip the parent edge by id, not by node). Edge: the root is an articulation point only with two or more DFS children | R, C, M, K |
| 64 | `lsn.contestds.two-sat` 2-SAT | Solve boolean constraints of two literals each with an implication graph and SCCs | Schedule 4 meetings, each in the morning or afternoon, with "not both in the morning" constraints | `graph-search` [mode to add: 2-SAT] | Trap: trying all $2^n$ assignments. Edge: unsatisfiable exactly when $x$ and $\neg x$ share an SCC | C, O, M, K |
| 65 | `lsn.contestds.matching` Bipartite matching | Find a maximum bipartite matching with augmenting paths (Kuhn's algorithm) | Assign 5 analysts to 5 coverage areas they know | `graph-search` (bipartite), `union-find` | Trap: greedy matching (it can block an augmenting path). Edge: König's theorem: maximum matching equals minimum vertex cover in bipartite graphs [recalled] | N, G, C, K |
| 66 | `lsn.contestds.max-flow` Maximum flow and minimum cut | Compute a maximum flow with Edmonds-Karp or Dinic and read off the minimum cut | The most data a network can carry from a feed to a gateway, and the cheapest set of links to cut | `shortest-path` [mode to add: flow] | Trap: forgetting reverse residual edges. Edge: max flow equals min cut; matching is flow with unit capacities | N, C, M, K |

Transfer screens: lesson 62 finds circular exposure among counterparties; lesson 63 finds single points of failure in a trading network; lesson 66 measures a network's capacity.

#### Course KD: Contest Techniques: DP and Strings (`crs.contestdp`, 3 levels, 18 lessons)

Dynamic programming beyond 1.8's tables, string algorithms, and the techniques for constraints that rule out the obvious: meet in the middle, square roots, Mo's algorithm, randomisation and linear algebra over $\mathrm{GF}(2)$. CPH chapters 10, 26 and 27 run alongside.

**Level KD1: DP Techniques** (`lvl.contestdp.dp`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 67 | `lsn.contestdp.bitmask-dp` Bitmask DP | Use subsets as bitmask states for assignment and travelling-salesman problems in $O(2^n n^2)$ | The shortest tour of 4 cities with distances 10, 15, 20, 35, 25, 30? (80) For 20 cities, steps? (about $4 \times 10^8$) | `dp-table` (states), `bit-lab` [mode to add: subsets] | Trap: $n = 25$ with $2^n n^2$ (about $2 \times 10^{10}$). Edge: iterate submasks with `s = (s - 1) & mask` | N, N, C, K |
| 68 | `lsn.contestdp.digit-dp` Digit DP | Count numbers up to $N$ with a digit property by DP over digits with a "tight" flag | Integers from 1 to 2,025 with no digit 7? (1,481) | `dp-table` (states) | Trap: forgetting the tight flag (counts numbers above $N$). Edge: leading zeros; ranges $[L, R]$ as $f(R) - f(L - 1)$ | N, C, M, K |
| 69 | `lsn.contestdp.knapsack-bitset` Knapsack variants and bitsets | Solve bounded and multiple knapsacks, and speed subset sum up 64 times with a bitset shift-or | Which sums from 0 to $10^5$ can 200 items make? With a bitset, how many word operations? | `dp-table` (space), `bit-lab` | Trap: splitting $k$ copies of an item into $k$ items (split into powers of two). Edge: `bitset |= bitset << w` | N, C, M, K |
| 70 | `lsn.contestdp.prefix-transitions` DP with prefix-sum transitions | Speed a DP whose transition sums a range of earlier states with prefix sums | Ways to climb $n = 10^5$ stairs taking 1 to $k$ steps at a time, modulo $10^9 + 7$, in $O(n)$ (for $n = 10$, $k = 3$: 274) | `dp-table` (1d), `range-query-lab` (prefix) | Trap: an $O(nk)$ inner loop. Edge: negative values after modular subtraction | N, C, X, K |
| 71 | `lsn.contestdp.interval-scale` Interval DP at contest scale | Fill interval DPs in $O(n^3)$ or better, and spot when an exchange argument reduces them | Merge adjacent piles [6, 4, 4, 6], each merge costing the merged total: the cheapest full merge? (40; merging the smallest neighbouring pair first costs 42) | `dp-table` (interval) | Trap: greedy merging of the two smallest adjacent piles. Edge: $n \le 400$ allows $O(n^3)$ | N, C, O, K |
| 72 | `lsn.contestdp.dp-optimisation` DP optimisation: monotone queues and the convex hull trick | Speed transitions of the form $\min_j (a_j x + b_j)$ with the convex hull trick, and sliding minima with a monotone deque | Why does a deque of lines with increasing slopes answer each query in amortised $O(1)$? | `dp-table`, `stack-queue-lab` (monotonic-deque) | Trap: using it without checking that slopes and queries are monotone. Edge: a Li Chao tree handles arbitrary order (stretch) [recalled] | C, M, O, K |


**Level KD2: Strings** (`lvl.contestdp.strings`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 73 | `lsn.contestdp.hashing-safely` Polynomial hashing, safely | Compare substrings in $O(1)$ with prefix hashes, using a random base and two moduli against anti-hash tests | A hash mod $2^{64}$ with base 131: do the Thue-Morse string of length 2,048 and its complement collide? (yes [verified]) | `hash-table`, `live-formula` | Trap: hashing modulo $2^{64}$ by letting integers overflow (Thue-Morse strings break it for any odd base [recalled theorem; verified for bases 31 and 131]). Edge: choose the base at random at run time | C, M, N, K |
| 74 | `lsn.contestdp.prefix-function` The prefix function and KMP | Compute the prefix function in $O(n)$ and use it for pattern matching and string periods | The prefix function of "abacaba"? ([0, 0, 1, 0, 1, 2, 3]) The period of "abcabcab"? (3) | `array-strip` (characters), `stepper` | Trap: restarting the match from scratch after a mismatch ($O(nm)$). Edge: matching pattern + "#" + text; a period $p$ divides the length only for full repetitions | T, N, C, K |
| 75 | `lsn.contestdp.z-function` The Z-function | Compute the Z-function in $O(n)$ and use it for matching and borders | Z of "aabxaab"? ([0, 1, 0, 0, 3, 1, 0]) | `array-strip`, `stepper` | Trap: forgetting to reuse the current $[l, r)$ box. Edge: $z[0]$ is defined as 0 by convention here | T, C, M, K |
| 76 | `lsn.contestdp.xor-trie` Binary tries for XOR | Find the maximum XOR of two numbers in $O(n \log V)$ with a trie over bits | Maximum XOR pair in [3, 10, 5, 25, 2, 8]? (28: 5 XOR 25) | `tree-lab` (trie), `bit-lab` | Trap: an $O(n^2)$ pair scan. Edge: fix the bit width (for example 30 bits) for every number | N, C, G, K |
| 77 | `lsn.contestdp.manacher` Palindromes in linear time | Find every palindromic substring centre's radius in $O(n)$ with Manacher's algorithm | The longest palindrome in a string of $10^6$ letters | `array-strip`, `stepper` | Trap: expanding around every centre ($O(n^2)$ worst case on "aaaa..."). Edge: insert separators to handle even lengths | N, C, M, K |
| 78 | `lsn.contestdp.suffix-structures` Suffix arrays in outline | Build a suffix array by doubling in $O(n \log^2 n)$ and read the LCP array's uses | Sort the suffixes of "banana" ([5, 3, 1, 0, 4, 2]) | `sort-lab`, `array-strip` | Trap: comparing suffixes character by character in a sort ($O(n^2 \log n)$). Edge: distinct substrings $= \sum (n - sa_i - lcp_i)$ | O, C, M, K |


**Level KD3: Techniques for Hard Constraints** (`lvl.contestdp.techniques`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 79 | `lsn.contestdp.meet-middle` Meet in the middle | Split an exponential search into two halves and join them by sorting or hashing | Subset sums of 40 items: $2^{40} \approx 1.1 \times 10^{12}$, or two lists of $2^{20} \approx 10^6$? | `complexity-lab` (budget), `binary-search-lab` | Trap: storing both halves' full subsets as lists of items (store sums). Edge: counting pairs with equal sums needs care with duplicates | N, C, M, K |
| 80 | `lsn.contestdp.sqrt-decomposition` Square-root decomposition | Split an array into blocks of about $\sqrt{n}$ for updates and queries in $O(\sqrt{n})$ | Range sums with point updates in blocks: block size for $n = 10^5$? (about 316) | `range-query-lab` (prefix), `cell-grid` | Trap: blocks that are too small or too large (the cost is $n/b + b$, smallest at $b = \sqrt{n}$). Edge: the last block may be shorter | N, X, C, K |
| 81 | `lsn.contestdp.mo` Mo's algorithm | Answer offline range queries by sorting them into blocks and moving two pointers | $n = q = 2 \times 10^5$: about how many pointer moves? ($(n + q)\sqrt{n} \approx 1.8 \times 10^8$) | `pointer-walk` (window-variable), `sort-lab` | Trap: answering queries in input order. Edge: add and remove must each be $O(1)$; alternate the right pointer's direction by block to save time | N, C, M, K |
| 82 | `lsn.contestdp.randomised` Randomised techniques | Use randomness to defeat worst cases: random pivots, random hash bases, random shuffles, and randomised checks | Why does shuffling the input before inserting into a hash map or a BST defeat a crafted test? | `counterexample-lab` (hack), `sim-runner` | Trap: `rand()` with a fixed seed (the hack still works). Edge: seed from a high-resolution clock in contests; Freivalds' check verifies a matrix product in $O(n^2)$ per trial [recalled] | C, M, N, K |
| 83 | `lsn.contestdp.xor-basis` XOR bases | Build a basis of numbers over $\mathrm{GF}(2)$ by Gaussian elimination on bits, and find the maximum subset XOR | The largest XOR of any subset of [9, 8, 5]? (13: 8 XOR 5) | `bit-lab`, `matrix` | Trap: greedy XOR of the largest numbers. Edge: the basis has at most 60 vectors for 60-bit values; this is 1.4's elimination with XOR as addition | N, C, G, K |
| 84 | `lsn.contestdp.offline-sweeps` Offline processing | Reorder queries and events to answer them with one sweep and a structure | For each query "how many values in $[l, r)$ are below $x$", sorted by $x$, with a Fenwick tree | `range-query-lab` (fenwick), `interval-sweep` | Trap: forcing an online structure when offline is allowed. Edge: return answers in the original order | N, C, O, K |

Transfer screens: lesson 79 searches 40 trades for a netting set (1.8 lesson 145 in contest form); lesson 83 is linear algebra over two elements, the structure behind some error-correcting codes [recalled].

### 2.4 Coverage check

**The curriculum's 1.8 cover list.**

| Cover item | Lessons |
|---|---|
| Complexity | 1 to 7, 12, 13, 17, 18, 144 |
| Arrays | 24, 30 to 45 |
| Hashing | 25 to 29, 37, 77, 78 |
| Two pointers | 30 to 34, 66 |
| Stacks | 57 to 61 |
| Queues | 62, 92, 94 |
| Linked lists | 63 to 68 |
| Binary search | 46 to 51, 120 |
| Trees | 79 to 90 |
| Heaps | 69 to 74, 98 |
| Graphs | 91 to 109 |
| Recursion | 5, 8 to 13, 110 to 115 |
| Dynamic programming | 116 to 132 |
| Greedy methods | 54, 133 to 137 |

**NeetCode 150 categories** (the Problem Gym mirrors them, section 3.4): arrays and hashing (24 to 29), two pointers (30 to 34), sliding window (35 to 40), stack (57 to 61), binary search (46 to 51), linked list (63 to 68), trees (79 to 89), tries (90), heap and priority queue (69 to 74), backtracking (110 to 115), graphs (91 to 97, 102), advanced graphs (98 to 101, 103 to 109), 1-D dynamic programming (116 to 121), 2-D dynamic programming (122 to 127), greedy (133 to 136, 45), intervals (52 to 56), maths and geometry (141 to 143), bit manipulation (138 to 140).

**What a top programme adds and where it sits** (MIT 6.006, 6.046J, CLRS): loop invariants and induction proofs (9, 10), recurrences and the master theorem (12, 13), amortised analysis (4, 60, 62), randomised algorithms and expected cost (17, 20, 75 to 77), the comparison lower bound and linear sorts (18, 19), external sorting (23), open addressing and universal hashing (26, 77), Bloom filters (78), balanced trees in outline (87, 88), cut property and MSTs (103), all-pairs paths (107), Eulerian paths (108), Huffman coding (137), NP-completeness and coping strategies (144, 145).

**The 1.9 exit and learncpp.** The exit's three demands (rewrite the pricer, tests, timing) are levels CP3 (79 to 84), CB4 (22) and CP2 (75, 82). learncpp's chapters map as: 0 to 3 (lessons 1 to 5, 17, 69); 4 to 6 (6 to 10); 7 and 8 (12, 17, 23); 9 (5, 34, 68); 10 (8); 11 (15, 47); 12 (14, 24, 25); 13 (11); 14 and 15 (29 to 32); 16 and 17 (18, 20, 52); 18 (21, 56, 58 to 61); 19 (26, 35); 20 (44); 21 (32); 22 (37 to 40); 23 to 25 (41 to 43, 46); 26 (48); 27 (33, 34); 28 (4) [check chapter numbers]. Beyond learncpp: sanitisers (7, 26, 27, 68), CMake (17, 70), doctest (22), performance (73 to 78), `<random>` and numerics (63 to 67), concurrency (85 to 88).

**2.4 against the Competitive Programmer's Handbook and the curriculum.** CPH chapters 1 to 6 (lessons 1 to 15), 7 and 8 (67 to 72), 9 (48 to 53), 10 (67, 76, 83), 11 to 13 (60, 61), 14 and 18 (54 to 59), 15 (60), 16 and 17 (62, 64), 19 (1.8 lesson 108), 20 (65, 66), 21 (22 to 32), 22 (33 to 36), 23 (37), 24 (38 to 40), 25 (41 to 43), 26 (73 to 78), 27 (80, 81), 28 (50, 51), 29 (44 to 47), 30 (84) [check chapter numbers]. The curriculum's additions: Kaggle and trading competitions (21), Project Euler (20).

**Quiz item types** (counted from the tables above by script; CI recounts from the lesson files).

| Course | Items | C | M | C and M share | N | K | T | G | O | Other (X, S, R, E, P) |
|---|---|---|---|---|---|---|---|---|---|---|
| AC | 92 | 22 | 8 | 32.6% | 30 | 5 | 5 | 4 | 7 | 11 |
| AH | 132 | 33 | 8 | 31.1% | 28 | 30 | 11 | 14 | 3 | 5 |
| SQ | 88 | 21 | 4 | 28.4% | 14 | 18 | 12 | 13 | 4 | 2 |
| TG | 124 | 31 | 7 | 30.6% | 25 | 27 | 7 | 14 | 8 | 5 |
| DP | 164 | 41 | 11 | 31.7% | 36 | 36 | 12 | 10 | 7 | 11 |
| CB | 88 | 22 | 10 | 36.4% | 6 | 9 | 25 | 1 | 4 | 11 |
| CM | 96 | 24 | 12 | 37.5% | 6 | 13 | 22 | 5 | 6 | 8 |
| CL | 84 | 21 | 11 | 38.1% | 12 | 18 | 18 | 0 | 1 | 3 |
| CP | 84 | 21 | 11 | 38.1% | 17 | 8 | 4 | 0 | 6 | 17 |
| KC | 84 | 21 | 11 | 38.1% | 13 | 17 | 5 | 3 | 8 | 6 |
| KM | 104 | 26 | 8 | 32.7% | 31 | 26 | 3 | 1 | 2 | 7 |
| KS | 76 | 19 | 10 | 38.2% | 14 | 19 | 0 | 5 | 5 | 4 |
| KD | 72 | 18 | 10 | 38.9% | 16 | 18 | 2 | 2 | 4 | 2 |
| **Total** | **1,288** | **320** | **121** | **34.2%** | | | | | | |

Every course stays under the 40% ceiling. The C++ courses lean on T (predict the output) because predicting what C++ does, including when it does not compile, is the skill those lessons teach.

**What 1.8, 1.9 and 2.4 leave to other items.**

| Topic | Where it is taught | Note |
|---|---|---|
| Computer systems: processes, virtual memory, networking, lock-free queues | canon-gap P13 (developer track) | 1.9 level CP4 is first contact only |
| Market microstructure, order types and matching rules | 1.7 (`stage1-finance-projects.md` course MK) | Lessons 74 and 55 implement a book; 1.7 explains it |
| Numerical linear algebra and conditioning | 1.4; canon-gap P3 | Lessons 13 and 127 count multiplications only |
| Probability proofs behind the randomised algorithms | 1.5 | Lessons 17, 25, 75 and 76 use indicators and induction |
| Machine learning systems in C++ | 2.1; canon-gap P14 | Lesson 72 shows the Python boundary |
| Formal proof technique as a subject | canon-gap P7 | 1.8 uses induction, invariants and exchange arguments as tools |
| Suffix automata, heavy-light decomposition, centroid decomposition, FFT in contests | Not covered | Above a 1,900 rating; Halim and Halim's CP4 is the stretch reading |

---

## 3. Homework blueprint per level

### 3.0 Rules for every set

- **Shape.** Issued when a level's last lesson is done, due in 7 days, marked on submission (`assessment.md` 2.5). **1.8 sets** hold 7 items in about 2.5 hours: 3 code drills (each a Problem Gym problem that counts once on the ledger when every hidden test passes), 3 auto-marked items (predict, trace, state, numeric or ordering) and 1 long-form item. **1.9 sets** hold 7 items in about 2.5 hours: 2 or 3 C++ drills, 3 or 4 auto-marked items (predict, compiles-or-not, sanitiser reading, layout) and 1 long-form item. **2.4 sets** hold 5 items in about 1.5 hours: 4 contest problems read from standard input, written to standard output, in Python or C++, and 1 long-form proof.
- **Difficulty.** Every item at difficulty 3 to 5. Seven-item sets: d3 ×3, d4 ×2, d5 ×2. Five-item sets: d3 ×2, d4 ×2, d5 ×1. At least one item at difficulty 5 in every set.
- **Long-form.** One per set, a `long-form` check with a 10-point rubric of five points of 2 marks (`content-format.md` 3.4): `genre: proof` for invariants, exchange arguments and induction; `genre: derivation` for expected and amortised costs; `genre: written` for a design rationale or a diagnosis. The learner self-marks with Bertie's per-point suggestion and quoted evidence (`ai-tutor.md` 2.7).
- **Code drills.** Each ships `drill.yaml`, `reference.py` (or `reference.cpp`), `starter`, `tests` (`zqtest` for Python; doctest for C++) and a `wrong/` folder whose files each name the misconception and the test they must fail (`content-format.md` 3.9). Every 1.8 drill whose pattern is the point carries a `complexity` test (decision 9). Python drills declare `needs: []` and run on both targets; C++ drills run in the web app through `cpp-runner` or locally with a pasted doctest summary (decision 12); 2.4 problems use `stdout` tests with several test cases per input file.
- **Bertie.** No tutor surface on any item until the set is submitted; after submission he explains, drafts long-form marks, and reviews passing code in the code-craft format (`ai-tutor.md` 2.2, 2.8).
- **Variants.** Generator slots are seeded per learner and level; drill families vary their data and constants by seed while the function to write stays fixed.

### 3.1 Item 1.8 Data structures and algorithms

| Level | Set | Items | Mix | Long-form (five points of 2 marks) | Code drills (ledger problems) | Generators |
|---|---|---|---|---|---|---|
| AC1 | `set.algcost.growth` | 7 | d3 ×3, d4 ×2, d5 ×2 | Prove $3n^2 + 10n\log_2 n + 7 = \Theta(n^2)$ with constants, and that $n \log n \ne O(n)$ | `drl.alg.fit-exponent`, `drl.alg.best-pair-gap`, `drl.alg.first-repeat-day` | `gen.alg.loop-count`, `gen.alg.growth-rank`, `gen.alg.doubling-ratio` |
| AC2 | `set.algcost.recursion` | 7 | as above | Fast exponentiation: correctness by strong induction and the multiplication bound | `drl.alg.hanoi-moves`, `drl.alg.fast-power`, `drl.alg.no-adjacent-ones` | `gen.alg.recurrence-total`, `gen.alg.master-case` |
| AC3 | `set.algcost.sorting` | 7 | as above | Randomised quicksort's expected comparisons, $2(n + 1)H_n - 4n$ | `drl.alg.count-inversions`, `drl.alg.three-way-quicksort`, `drl.alg.counting-sort` | `gen.alg.sort-trace`, `gen.alg.inversion-count`, `gen.alg.decision-bound` |
| AC4 | `set.algcost.ordering` | 7 | as above | Why the largest-number comparator is a valid order (it is a key in disguise) | `drl.alg.quickselect`, `drl.alg.largest-number`, `drl.alg.merge-runs` | `gen.alg.select-trace`, `gen.alg.external-runs` |
| AH1 | `set.arrayhash.hashing` | 7 | as above | Expected empty buckets and colliding pairs by indicators | `drl.alg.two-sum-notional`, `drl.alg.group-anagrams`, `drl.alg.longest-consecutive` | `gen.alg.hash-bucket`, `gen.alg.probe-count`, `gen.alg.load-factor` |
| AH2 | `set.arrayhash.pointers` | 7 | as above | Why moving the shorter side never discards the best container | `drl.alg.three-sum-closest`, `drl.alg.container-water`, `drl.alg.trap-water` | `gen.alg.pointer-moves`, `gen.alg.pair-grid` |
| AH3 | `set.arrayhash.windows` | 7 | as above | Exactly $k$ distinct as at-most-$k$ minus at-most-$(k - 1)$, and the window's amortised $O(n)$ | `drl.alg.longest-k-distinct`, `drl.alg.exactly-k-distinct`, `drl.alg.window-maximum` | `gen.alg.window-trace`, `gen.alg.deque-state` |
| AH4 | `set.arrayhash.prefix` | 7 | as above | Kadane's algorithm: an invariant and its proof | `drl.alg.rect-sum`, `drl.alg.subarray-sum-k`, `drl.alg.product-except-self` | `gen.alg.prefix-query`, `gen.alg.difference-apply` |
| AH5 | `set.arrayhash.binsearch` | 7 | as above | Binary search on the answer: the invariant, termination and the bounds | `drl.alg.isqrt`, `drl.alg.min-days-bouquets`, `drl.alg.rotated-search` | `gen.alg.bisect-bounds`, `gen.alg.search-trace` |
| AH6 | `set.arrayhash.intervals` | 7 | as above | Earliest end first is optimal: the exchange argument | `drl.alg.covered-length`, `drl.alg.min-removals`, `drl.alg.peak-overlap` | `gen.alg.interval-merge`, `gen.alg.sweep-count` |
| SQ1 | `set.linear.stacks` | 7 | as above | The monotonic stack makes at most $2n$ operations | `drl.alg.eval-rpn`, `drl.alg.days-to-higher`, `drl.alg.largest-rectangle` | `gen.alg.stack-trace`, `gen.alg.bracket-check` |
| SQ2 | `set.linear.lists` | 7 | as above | Floyd's cycle start: why restarting from the head works | `drl.alg.reverse-k-group`, `drl.alg.lru-cache`, `drl.alg.cycle-start` | `gen.alg.list-ops`, `gen.alg.lru-trace` |
| SQ3 | `set.linear.heaps` | 7 | as above | Heapify in $O(n)$: the sum over levels | `drl.alg.kth-largest-stream`, `drl.alg.merge-k-feeds`, `drl.alg.order-book-heaps` | `gen.alg.heap-array`, `gen.alg.median-trace` |
| SQ4 | `set.linear.random` | 7 | as above | Reservoir sampling is uniform: induction on the stream | `drl.alg.reservoir-k`, `drl.alg.fisher-yates`, `drl.alg.bloom-size` | `gen.alg.bloom-rate`, `gen.alg.shuffle-count` |
| TG1 | `set.treesgraphs.binary-trees` | 7 | as above | The diameter recursion: what is returned, what is recorded, and why it is correct | `drl.alg.tree-diameter`, `drl.alg.max-path-sum`, `drl.alg.build-from-traversals` | `gen.alg.traversal-order`, `gen.alg.tree-height` |
| TG2 | `set.treesgraphs.search-trees` | 7 | as above | Validating a BST with intervals: why it is correct and why the parent check fails | `drl.alg.validate-bst`, `drl.alg.trie-wildcard`, `drl.alg.kth-smallest-bst` | `gen.alg.bst-insert`, `gen.alg.bst-delete` |
| TG3 | `set.treesgraphs.traversal` | 7 | as above | BFS finds shortest unweighted distances: the layer invariant | `drl.alg.count-islands`, `drl.alg.course-order`, `drl.alg.rotting-grid` | `gen.alg.bfs-layers`, `gen.alg.topo-orders` |
| TG4 | `set.treesgraphs.weighted` | 7 | as above | Dijkstra's correctness, and the counterexample with a negative edge | `drl.alg.network-delay`, `drl.alg.find-arbitrage`, `drl.alg.cheapest-k-stops` | `gen.alg.dijkstra-trace`, `gen.alg.uf-parent` |
| TG5 | `set.treesgraphs.techniques` | 7 | as above | The cut property of minimum spanning trees | `drl.alg.floyd-warshall`, `drl.alg.word-ladder`, `drl.alg.alien-order` | `gen.alg.dag-longest`, `gen.alg.mst-weight` |
| DP1 | `set.dynprog.backtracking` | 7 | as above | Skipping equal neighbours at one depth lists each distinct subset once | `drl.alg.permute-unique`, `drl.alg.n-queens-count`, `drl.alg.combination-sum` | `gen.alg.backtrack-count` |
| DP2 | `set.dynprog.foundations` | 7 | as above | Loop order: combinations against orderings in coin counting | `drl.alg.coin-ways`, `drl.alg.decode-ways`, `drl.alg.lis-length` | `gen.alg.dp-fill-1d`, `gen.alg.memo-calls` |
| DP3 | `set.dynprog.two-d` | 7 | as above | The edit-distance recurrence: why three cases are enough | `drl.alg.edit-script`, `drl.alg.max-profit-k`, `drl.alg.matrix-chain` | `gen.alg.dp-fill-2d`, `gen.alg.knapsack-table` |
| DP4 | `set.dynprog.design` | 7 | as above | Backward induction's cost on a recombining tree, and what path dependence does to it | `drl.alg.rob-tree`, `drl.alg.longest-increasing-path`, `drl.alg.domino-tilings` | `gen.alg.state-design` |
| DP5 | `set.dynprog.greedy` | 7 | as above | Huffman's greedy choice by exchange | `drl.alg.min-jumps`, `drl.alg.gas-start`, `drl.alg.huffman-cost` | `gen.alg.greedy-counterexample` |
| DP6 | `set.dynprog.bits-maths` | 7 | as above | Two's complement: why $-x = \lnot x + 1$, and what Python does instead | `drl.alg.count-bits`, `drl.alg.fib-mod`, `drl.alg.add-without-plus` | `gen.alg.bit-ops`, `gen.alg.twos-read` |
| DP7 | `set.dynprog.method` | 7 | as above | A full method write-up for an unseen medium | `drl.alg.subarrays-divisible`, `drl.alg.stress-finder`, `drl.alg.zero-sum-subset` | `gen.alg.pattern-match` |

**Example problems, 1.8.** Every answer below was recomputed by brute force or exact arithmetic, and every reference solution was run against a brute force on random inputs (section 0.6). "Checks" lists cases the visible and hidden tests include.

**AC1, example 1 (difficulty 4, numeric and expression).** Exactly how many times does `work()` run, as a formula in $n$ and for $n = 1{,}000$ and $n = 1{,}024$?

```python
for i in range(n):
    j = 1
    while j < n:
        work()
        j *= 2
```

*Answer:* $n \lceil \log_2 n \rceil$ for $n \ge 1$: 10,000 for $n = 1{,}000$ and 10,240 for $n = 1{,}024$.
*Working:* the inner loop does not depend on $i$; it runs for $j = 1, 2, 4, \dots$ while $j < n$, that is $\lceil \log_2 n \rceil$ times (10 values from 1 to 512 for $n = 1{,}000$). Multiply by the $n$ passes of the outer loop. *Decision point:* reading "two loops" as $n^2$ gives 1,000,000; reading the inner loop as $\lfloor \log_2 n \rfloor + 1$ gives 11 per pass at $n = 1{,}024$, but $j = 1{,}024$ fails `j < n`.

**AC1, example 2 (difficulty 5, long-form proof).** Prove that $f(n) = 3n^2 + 10n\log_2 n + 7$ is $\Theta(n^2)$, giving constants, and prove that $n \log_2 n$ is not $O(n)$.

*Model answer:* (1) Lower bound: for $n \ge 1$, $f(n) \ge 3n^2$, so $f = \Omega(n^2)$ with $c = 3$, $n_0 = 1$. (2) Upper bound: for $n \ge 2$, $\log_2 n \le n$ and $7 \le 7n^2/4$, so $f(n) \le 3n^2 + 10n^2 + 2n^2 \le 15n^2$; any $c \ge 10$ also works from $n_0 = 2$ (the ratio $f(n)/n^2$ is 9.75 at $n = 2$ and falls). (3) Together these give $\Theta(n^2)$. (4) Suppose $n \log_2 n \le cn$ for all $n \ge n_0$; then $\log_2 n \le c$, which fails for $n > 2^c$. (5) So no constants exist: $n \log n$ grows strictly faster than $n$, although only by a slowly growing factor.
*Rubric (10):* 2 for the lower bound with constants; 2 for the upper bound with a justified $c$ and $n_0$; 2 for combining them correctly; 2 for the contradiction setup; 2 for concluding with the failing $n$.

**AC2, example 1 (difficulty 4, code).** Write `hanoi_moves(n, src="A", dst="C", via="B")` returning the list of moves `(from, to)` that transfers $n$ discs.

*Answer:*

```python
def hanoi_moves(n: int, src: str = "A", dst: str = "C", via: str = "B") -> list[tuple[str, str]]:
    if n < 0:
        raise ValueError("n must be non-negative")
    moves: list[tuple[str, str]] = []
    def go(k: int, a: str, b: str, c: str) -> None:   # move k discs from a to b using c
        if k == 0:
            return
        go(k - 1, a, c, b)          # clear the k-1 smaller discs onto the spare peg
        moves.append((a, b))         # move the largest
        go(k - 1, c, b, a)          # put the smaller discs back on top
    go(n, src, dst, via)
    return moves
```

*Checks:* `hanoi_moves(3)` has 7 moves starting `("A", "C"), ("A", "B"), ("C", "B")`; `len(hanoi_moves(10)) == 1023`; a hidden simulator replays every move for $n \le 12$ and asserts no larger disc ever lands on a smaller one and all discs end on the target; `hanoi_moves(0) == []`. *Decision point:* depth is $n$, so $n \le 20$ stays far inside the recursion cap (decision 25), while the output has $2^n - 1$ moves, which is why $n$ is capped.

**AC2, example 2 (difficulty 5, long-form proof).** `power(x, n)` returns 1 for $n = 0$; otherwise it computes `h = power(x, n // 2)`, then returns `h * h` if $n$ is even and `h * h * x` if odd. Prove it returns $x^n$ for every integer $n \ge 0$, and that it makes at most $2\lfloor \log_2 n \rfloor + 2$ multiplications for $n \ge 1$.

*Model answer:* (1) Claim $P(n)$: `power(x, n)` returns $x^n$. Base: $P(0)$ holds by the first line. (2) Strong induction: assume $P(k)$ for all $k < n$, with $n \ge 1$; then $\lfloor n/2 \rfloor < n$, so $h = x^{\lfloor n/2 \rfloor}$. (3) If $n$ is even, $h^2 = x^{2\lfloor n/2 \rfloor} = x^n$; if odd, $h^2 x = x^{2\lfloor n/2 \rfloor + 1} = x^n$. (4) Cost: let $M(n)$ count multiplications; $M(0) = 0$ and $M(n) = M(\lfloor n/2 \rfloor) + 1 + [n \text{ odd}]$, so each of the $\lfloor \log_2 n \rfloor + 1$ calls with $n \ge 1$ adds at most 2. (5) Hence $M(n) \le 2(\lfloor \log_2 n \rfloor + 1)$, and exactly the bit length plus the number of 1 bits (16 for $n = 1{,}000$), against $n - 1$ for a loop.
*Rubric (10):* 2 for the statement and base case; 2 for using strong induction and why $\lfloor n/2 \rfloor < n$; 2 for both parity cases; 2 for the cost recurrence; 2 for the bound and its count of calls.

**AC3, example 1 (difficulty 4, code).** Write `count_inversions(a)` returning the number of pairs $i < j$ with $a_i > a_j$, in $O(n \log n)$.

*Answer:*

```python
def count_inversions(a: list[int]) -> int:
    def sort_count(xs: list[int]) -> tuple[list[int], int]:
        if len(xs) <= 1:
            return xs, 0
        mid = len(xs) // 2
        left, x = sort_count(xs[:mid])
        right, y = sort_count(xs[mid:])
        merged, i, j, cross = [], 0, 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:          # <= keeps equal values from counting as inversions
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
                cross += len(left) - i       # every remaining left value is larger than right[j]
        merged += left[i:] + right[j:]
        return merged, x + y + cross
    return sort_count(list(a))[1]
```

*Checks:* [2, 4, 1, 3, 5] gives 3; [5, 4, 3, 2, 1] gives 10; [1, 1, 1] gives 0; 500 random arrays against the $O(n^2)$ count; a `complexity` test at $n = 2 \times 10^5$ that a quadratic count fails. *Decision point:* `<` in place of `<=` counts equal pairs as inversions; the `wrong/` folder holds that version.

**AC3, example 2 (difficulty 5, long-form derivation).** Quicksort picks pivots uniformly at random from distinct values. Derive the expected number of comparisons and give its value for $n = 4$.

*Model answer:* (1) Let $z_1 < \dots < z_n$ be the sorted values and $X_{ij}$ indicate that $z_i$ and $z_j$ are ever compared; comparisons happen only with a pivot, so each pair is compared at most once and $E[C] = \sum_{i < j} P(X_{ij} = 1)$. (2) $z_i$ and $z_j$ stay in one subarray until the first pivot drawn from $\{z_i, \dots, z_j\}$; they are compared exactly when that pivot is $z_i$ or $z_j$. (3) Each of the $j - i + 1$ values is equally likely to be first, so $P = \frac{2}{j - i + 1}$. (4) Summing over gaps $d = j - i$: $E[C] = \sum_{d=1}^{n-1} (n - d)\frac{2}{d + 1} = 2(n + 1)H_n - 4n$. (5) For $n = 4$: $10 \cdot \frac{25}{12} - 16 = \frac{29}{6}$; the leading term is $2n \ln n \approx 1.39 n\log_2 n$, and the bound holds for every input because the randomness is in the pivots.
*Rubric (10):* 2 for indicators and linearity; 2 for the "first pivot in the range" argument; 2 for the probability; 2 for the sum to the closed form; 2 for the $n = 4$ value and the "every input" remark.

**AC4, example 1 (difficulty 4, code).** Write `largest_number(nums)` returning, as a string, the largest number formed by concatenating the non-negative integers in some order.

*Answer:*

```python
from functools import cmp_to_key

def largest_number(nums: list[int]) -> str:
    def order(a: str, b: str) -> int:        # a goes first when a+b beats b+a
        return -1 if a + b > b + a else (1 if a + b < b + a else 0)
    joined = "".join(sorted(map(str, nums), key=cmp_to_key(order)))
    return "0" if joined[0] == "0" else joined   # all zeros print as a single 0
```

*Checks:* [3, 30, 34, 5, 9] gives "9534330"; [0, 0] gives "0"; [10, 2] gives "210"; [432, 43243] gives "43243432"; 200 random lists of up to 6 values against the maximum over all permutations. *Decision point:* sorting the strings in reverse plain order puts "30" before "3" and gives "9534303" [verified].

**AC4, example 2 (difficulty 5, long-form proof).** Prove that the comparator "a before b when $ab > ba$" (concatenation) is a valid strict weak order on positive integers, so sorting with it is well defined.

*Model answer:* (1) Write $\ell_a$ for the number of digits of $a$; concatenation is $ab = a \cdot 10^{\ell_b} + b$. (2) Then $ab > ba \iff a(10^{\ell_b} - 1) > b(10^{\ell_a} - 1)$. (3) Dividing by the positive $(10^{\ell_a} - 1)(10^{\ell_b} - 1)$: $ab > ba \iff \frac{a}{10^{\ell_a} - 1} > \frac{b}{10^{\ell_b} - 1}$. (4) So the comparator orders by the key $k(a) = \frac{a}{10^{\ell_a} - 1}$, and ordering by a real-valued key is irreflexive and transitive, with "neither before the other" meaning equal keys, an equivalence. (5) Hence the order is a strict weak order; equal keys (such as 3 and 33) can go in either order without changing the result.
*Rubric (10):* 2 for writing concatenation arithmetically; 2 for the rearrangement; 2 for the key; 2 for concluding transitivity and irreflexivity; 2 for the tie case.

**AH1, example 1 (difficulty 4, code).** Write `group_anagrams(words)` returning the groups of words that are anagrams of each other, each group sorted and the list of groups sorted, in $O(nk)$ for $n$ words of length $k$.

*Answer:*

```python
from collections import defaultdict

def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[tuple[int, ...], list[str]] = defaultdict(list)
    for w in words:
        counts = [0] * 26
        for ch in w:
            counts[ord(ch) - ord("a")] += 1     # a 26-count signature costs O(k), sorting costs O(k log k)
        groups[tuple(counts)].append(w)        # tuples are hashable, lists are not
    return sorted(sorted(g) for g in groups.values())
```

*Checks:* ["eat", "tea", "tan", "ate", "nat", "bat"] gives [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]; the empty string forms its own group; inputs are lower-case letters only (stated). *Decision point:* `tuple(counts)` is the key; `counts` itself raises `TypeError: unhashable type: 'list'`.

**AH1, example 2 (difficulty 5, long-form derivation).** $n$ keys hash independently and uniformly into $m$ buckets. Derive the expected number of empty buckets and of colliding pairs, and evaluate both for $n = m = 1{,}000$.

*Model answer:* (1) Let $E_b$ indicate that bucket $b$ is empty; $P(E_b) = (1 - \frac1m)^n$ because each key misses $b$ independently. (2) By linearity, the expected number of empty buckets is $m(1 - \frac1m)^n$. (3) Let $C_{ij}$ indicate that keys $i < j$ share a bucket; $P(C_{ij}) = \frac1m$, so the expected number of colliding pairs is $\binom{n}{2}\frac1m$. (4) At $n = m = 1{,}000$: $1{,}000 \times 0.999^{1000} \approx 367.7$ empty buckets (close to $m/e \approx 367.9$) and $499.5$ colliding pairs. (5) So even at load factor 1 about 37% of buckets are empty while others hold several keys; chains stay short on average ($1 + \alpha$), which is the hash table's guarantee.
*Rubric (10):* 2 for the empty-bucket indicator and its probability; 2 for linearity; 2 for the pair indicator; 2 for both numbers; 2 for the interpretation.

**AH2, example 1 (difficulty 4, code).** Write `three_sum_closest(nums, target)` returning the sum of three elements closest to `target` (ties to the smaller sum), in $O(n^2)$.

*Answer:*

```python
def three_sum_closest(nums: list[int], target: int) -> int:
    if len(nums) < 3:
        raise ValueError("need at least three numbers")
    a = sorted(nums)
    best = a[0] + a[1] + a[2]
    for i in range(len(a) - 2):
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if abs(s - target) < abs(best - target) or (abs(s - target) == abs(best - target) and s < best):
                best = s
            if s < target:
                lo += 1                      # a larger sum needs a larger middle value
            elif s > target:
                hi -= 1
            else:
                return s                     # exact hit cannot be beaten
    return best
```

*Checks:* [-1, 2, 1, -4] with target 1 gives 2; [0, 0, 0] with 1 gives 0; random arrays against the $O(n^3)$ brute force with the same tie rule; a `complexity` test at $n = 3{,}000$. *Decision point:* the tie rule must be stated, or two correct programs disagree.

**AH2, example 2 (difficulty 5, long-form proof).** In the container problem, with pointers $i < j$ and $h_i \le h_j$, prove that moving $i$ inwards discards no pair that could be better than the best found.

*Model answer:* (1) The pairs discarded by moving $i$ are $(i, k)$ for $i < k < j$. (2) For each, the width is $k - i < j - i$. (3) The height is $\min(h_i, h_k) \le h_i = \min(h_i, h_j)$. (4) So area$(i, k) <$ width $\times$ height of $(i, j)$, which has already been recorded. (5) Hence the best container is never discarded; each step removes a row of the pair grid, so the algorithm checks $n - 1$ pairs and is $O(n)$.
*Rubric (10):* 2 for naming the discarded pairs; 2 for width; 2 for height; 2 for the comparison with the recorded pair; 2 for the conclusion and the cost.

**AH3, example 1 (difficulty 4, code).** Write `exactly_k_distinct(a, k)` counting the subarrays with exactly $k$ distinct values, in $O(n)$.

*Answer:*

```python
from collections import Counter

def exactly_k_distinct(a: list[int], k: int) -> int:
    def at_most(m: int) -> int:              # subarrays with at most m distinct values
        if m < 0:
            return 0
        counts: Counter[int] = Counter()
        lo = total = 0
        for hi, x in enumerate(a):
            counts[x] += 1
            while len(counts) > m:           # shrink until the window is valid again
                counts[a[lo]] -= 1
                if counts[a[lo]] == 0:
                    del counts[a[lo]]
                lo += 1
            total += hi - lo + 1             # every subarray ending at hi and starting in [lo, hi]
        return total
    return at_most(k) - at_most(k - 1)
```

*Checks:* [1, 2, 1, 2, 3] with $k = 2$ gives 7; [1, 2, 1, 3, 4] with $k = 3$ gives 3; $k = 0$ gives 0; random arrays against brute force; a `complexity` test at $n = 2 \times 10^5$. *Decision point:* a single window cannot count "exactly $k$" directly, because a valid window can still shrink and stay valid.

**AH3, example 2 (difficulty 5, long-form).** Explain why "exactly $k$" equals at-most-$k$ minus at-most-$(k - 1)$, and prove that each `at_most` call runs in $O(n)$ although it contains a nested loop.

*Model answer:* (1) The subarrays with at most $k$ distinct values split into those with exactly $k$ and those with at most $k - 1$; subtracting leaves exactly $k$. (2) For a fixed right end `hi`, the valid left ends form an interval $[lo, hi]$, because removing elements from the left never adds distinct values. (3) So `hi - lo + 1` counts every valid subarray ending at `hi` once. (4) `lo` only increases and never passes $n$, so the inner `while` runs at most $n$ times in total across the whole loop. (5) Each element enters and leaves the counter once: $O(n)$ time and $O(k)$ space.
*Rubric (10):* 2 for the set split; 2 for the interval of left ends; 2 for the count per right end; 2 for the monotone pointer bound; 2 for the totals.

**AH4, example 1 (difficulty 4, code).** Write `rect_sum(grid, queries)` answering many inclusive rectangle-sum queries `(r1, c1, r2, c2)` in $O(1)$ each after $O(RC)$ preparation.

*Answer:*

```python
def rect_sum(grid: list[list[int]], queries: list[tuple[int, int, int, int]]) -> list[int]:
    R, C = len(grid), len(grid[0]) if grid else 0
    P = [[0] * (C + 1) for _ in range(R + 1)]          # P[r][c] = sum of grid[:r][:c]
    for r in range(R):
        for c in range(C):
            P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]
    return [P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]   # four corners
            for r1, c1, r2, c2 in queries]
```

*Checks:* on the 5 × 5 grid [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]], queries (2, 1, 4, 3), (1, 1, 2, 2) and (1, 2, 2, 4) give 8, 11 and 12; a single cell; the whole grid; random grids against direct sums. *Decision point:* the subtracted corner $P[r_1][c_1]$ was removed twice and must be added back once.

**AH4, example 2 (difficulty 5, long-form proof).** Prove Kadane's algorithm correct: `best_here = max(x, best_here + x)` and `best = max(best, best_here)` over a non-empty array return the maximum sum of a non-empty contiguous subarray.

*Model answer:* (1) Invariant: after reading $a_0, \dots, a_i$, `best_here` is the maximum sum of a subarray ending at $i$, and `best` the maximum over all subarrays ending at or before $i$. (2) Initialisation at $i = 0$: both equal $a_0$, the only subarray. (3) Maintenance: a subarray ending at $i + 1$ is either $[a_{i+1}]$ or a subarray ending at $i$ extended by $a_{i+1}$; the best of the second kind is `best_here` $+ a_{i+1}$, so the update is exactly the maximum of the two. (4) `best` then takes the maximum of the old best and the new ending sum, covering every subarray ending at or before $i + 1$. (5) At the end the invariant gives the answer; restarting when the running sum is negative is the same rule, and all-negative input returns the largest element ($-1$ for [-3, -1, -2]).
*Rubric (10):* 2 for a precise invariant; 2 for initialisation; 2 for the case split in maintenance; 2 for the `best` update; 2 for termination and the all-negative case.

**AH5, example 1 (difficulty 4, code).** Write `isqrt(x)` returning $\lfloor \sqrt{x} \rfloor$ for integers $0 \le x < 2^{63}$ without floating point.

*Answer:*

```python
def isqrt(x: int) -> int:
    if x < 0:
        raise ValueError("x must be non-negative")
    lo, hi = 0, x + 1                 # invariant: lo*lo <= x < hi*hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
    return lo
```

*Checks:* $10^{18}$ gives $10^9$; $2^{63} - 1$ gives 3,037,000,499 (equal to `math.isqrt`); 0 gives 0; 15 gives 3; every perfect square and its neighbours up to $10^6$. *Decision point:* `int(math.sqrt(x))` is wrong for large $x$ because a double has 53 bits of precision; the banned-call check rejects `math.sqrt` and `**0.5`.

**AH5, example 2 (difficulty 5, code).** Flowers bloom on the days in `bloom`. A bouquet needs `k` adjacent bloomed flowers. Write `min_days(bloom, m, k)` returning the first day on which `m` bouquets can be made, or $-1$.

*Answer:*

```python
def min_days(bloom: list[int], m: int, k: int) -> int:
    if m * k > len(bloom):
        return -1                                  # not enough flowers on any day
    def can(day: int) -> bool:                     # monotone: true from some day onwards
        made = run = 0
        for b in bloom:
            run = run + 1 if b <= day else 0
            if run == k:
                made, run = made + 1, 0
        return made >= m
    lo, hi = min(bloom), max(bloom)                # the answer lies in [lo, hi]
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

*Checks:* [1, 10, 3, 10, 2] with $m = 3$, $k = 1$ gives 3; with $k = 2$ gives $-1$; [7, 7, 7, 7, 12, 7, 7] with $m = 2$, $k = 3$ gives 12; random inputs against a scan over every day; a `complexity` test with days up to $10^9$. *Decision point:* searching the days themselves one by one is $O(n \cdot \max)$; the predicate's monotonicity is what licenses the binary search.

**AH6, example 1 (difficulty 4, code).** Write `covered_length(intervals)` returning the total length covered by the union of half-open intervals $[s, e)$.

*Answer:*

```python
def covered_length(intervals: list[tuple[int, int]]) -> int:
    total = 0
    cur_s = cur_e = None
    for s, e in sorted(intervals):
        if cur_e is None or s > cur_e:             # a gap: close the current block
            if cur_e is not None:
                total += cur_e - cur_s
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)                  # overlap or touch: extend the block
    if cur_e is not None:
        total += cur_e - cur_s
    return total
```

*Checks:* [(1, 3), (2, 6), (8, 10), (15, 18)] gives 10; an empty list gives 0; nested intervals; random lists against marking each unit. *Decision point:* adding every interval's length (here 2 + 4 + 2 + 3 = 11) double-counts the overlap [2, 3).

**AH6, example 2 (difficulty 5, long-form proof).** Prove that choosing intervals by earliest end, skipping any that overlap the last chosen, gives a largest set of non-overlapping intervals.

*Model answer:* (1) Let $g_1$ be the interval with the earliest end and $O$ any optimal schedule, sorted by end, with first interval $o_1$. (2) Since $g_1$ ends no later than $o_1$, every other interval of $O$ starts after $o_1$ ends, hence after $g_1$ ends. (3) So replacing $o_1$ by $g_1$ gives a schedule of the same size with no overlap: some optimal schedule starts with the greedy choice. (4) Removing $g_1$ and every interval overlapping it leaves a smaller instance of the same problem, on which the same argument applies (induction on the number of intervals). (5) Therefore greedy is optimal; shortest-first fails on [1, 5], [4, 7], [6, 10] (it picks [4, 7] alone where [1, 5] and [6, 10] fit).
*Rubric (10):* 2 for setting up the exchange; 2 for why the rest of $O$ still fits; 2 for the swapped schedule; 2 for the induction; 2 for the counterexample to another rule.

**SQ1, example 1 (difficulty 4, code).** Write `days_to_higher(closes)` returning, for each day, how many days until a strictly higher close (0 if none), in $O(n)$.

*Answer:*

```python
def days_to_higher(closes: list[float]) -> list[int]:
    ans = [0] * len(closes)
    stack: list[int] = []                    # indices still waiting for a higher close
    for i, px in enumerate(closes):
        while stack and closes[stack[-1]] < px:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans
```

*Checks:* [100, 98, 97, 99, 101, 96, 102] gives [4, 2, 1, 1, 2, 1, 0]; [73, 74, 75, 71, 69, 72, 76, 73] gives [1, 1, 4, 2, 1, 1, 0, 0]; equal closes are not higher; a `complexity` test on a falling series of $2 \times 10^5$ closes. *Decision point:* `<=` in the `while` treats an equal close as higher.

**SQ1, example 2 (difficulty 5, long-form).** Prove that the monotonic stack above performs at most $2n$ stack operations, although a `while` sits inside the `for`.

*Model answer:* (1) Each index is pushed exactly once, in its own iteration: $n$ pushes. (2) An index can be popped at most once, since it is never pushed again. (3) Every iteration of the inner `while` pops one index, so all the `while` iterations together number at most $n$. (4) The comparisons are at most one per pop plus one failing comparison per outer iteration, at most $2n$. (5) Hence the total work is $O(n)$: the nested loop is amortised over the whole run, the same argument as the sliding window's (AH3).
*Rubric (10):* 2 for counting pushes; 2 for "popped at most once"; 2 for bounding the inner iterations in total; 2 for the comparison count; 2 for naming it as an amortised bound.

**SQ2, example 1 (difficulty 4, code).** Write `reverse_k_group(head, k)` reversing each block of `k` nodes of a singly linked list in place, leaving a final short block unchanged.

*Answer:*

```python
class Node:
    def __init__(self, val, next=None):
        self.val, self.next = val, next

def reverse_k_group(head: "Node | None", k: int) -> "Node | None":
    dummy = Node(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):                        # find the k-th node of this block
            kth = kth.next
            if kth is None:
                return dummy.next                 # a short block stays as it is
        group_next = kth.next
        prev, curr = group_next, group_prev.next  # reverse the block, pointing its first node at group_next
        while curr is not group_next:
            curr.next, prev, curr = prev, curr, curr.next
        first = group_prev.next
        group_prev.next = kth                     # kth is now the block's head
        group_prev = first                        # the old first node is now its tail
```

*Checks:* 1 → 2 → 3 → 4 → 5 with $k = 2$ gives 2, 1, 4, 3, 5 and with $k = 3$ gives 3, 2, 1, 4, 5; $k = 1$ leaves the list; the hidden tests also assert that no new nodes were created (identity of node objects). *Decision point:* reversing without first checking that $k$ nodes remain reverses the final short block.

**SQ2, example 2 (difficulty 5, long-form proof).** A list has a tail of $\mu$ nodes before a cycle of $\lambda$ nodes. Slow moves 1 step and fast 2 steps from the head until they meet. Prove that a pointer from the head and a pointer from the meeting point, moving 1 step each, meet at the cycle's first node.

*Model answer:* (1) Let the meeting happen after $t$ steps; slow has walked $t$ and fast $2t$, both now in the cycle. (2) Fast is ahead by a whole number of laps: $2t - t = t \equiv 0 \pmod{\lambda}$. (3) Slow's position measured from the cycle start is $t - \mu$ (mod $\lambda$). (4) Walking $\mu$ more steps takes it to $t \equiv 0 \pmod{\lambda}$ from the start of the cycle, that is, the start itself; a pointer from the head reaches the start after exactly $\mu$ steps too. (5) So they first meet at the start, after $\mu$ steps; with $\mu = 3$, $\lambda = 5$ the pointers meet after 5 steps and the start is found 3 steps later [verified].
*Rubric (10):* 2 for the step counts; 2 for the multiple of $\lambda$; 2 for slow's offset; 2 for the $\mu$ further steps; 2 for the conclusion with the example.

**SQ3, example 1 (difficulty 4, code).** Write a class `KthLargest(k, nums)` whose `add(x)` returns the $k$th largest value seen so far, each call in $O(\log k)$.

*Answer:*

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]) -> None:
        if k < 1:
            raise ValueError("k must be at least 1")
        self.k, self.heap = k, []                    # a min-heap of the k largest so far
        for x in nums:
            self.add(x)

    def add(self, x: int) -> int:
        heapq.heappush(self.heap, x)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)                 # evict the smallest of the top k + 1
        return self.heap[0]                          # the k-th largest is the heap's minimum
```

*Checks:* `KthLargest(3, [4, 5, 8, 2])` then adding 3, 5, 10, 9, 4 returns 4, 5, 5, 8, 8; fewer than $k$ values so far is stated as never happening in the tests' calls; a `complexity` test over $10^5$ adds. *Decision point:* a max-heap of everything gives $O(\log n)$ per add and $O(n)$ memory.

**SQ3, example 2 (difficulty 5, long-form derivation).** Show that bottom-up heapify of $n = 2^{h+1} - 1$ items does fewer than $n$ swaps in the worst case, and explain why $n$ pushes can cost $\Theta(n \log n)$.

*Model answer:* (1) Heapify sifts down each internal node from the last parent to the root. (2) A node at height $j$ (distance to the leaves) moves at most $j$ levels, and there are $2^{h - j}$ nodes at height $j$. (3) Total swaps at most $\sum_{j=0}^{h} j \, 2^{h - j} = 2^h \sum_j \frac{j}{2^j} < 2^h \cdot 2 = 2^{h+1} < n + 1$. (4) Pushes instead sift up from the bottom, where most nodes are: pushing values in decreasing order into a min-heap makes every push climb to the root, and the last half of the pushes climb about $h$ levels each, $\Theta(n \log n)$ in total. (5) So build a heap from known data with `heapify`, and keep pushes for streams.
*Rubric (10):* 2 for the sift-down structure; 2 for nodes per height; 2 for the sum and its bound; 2 for the push contrast; 2 for the practical rule.

**SQ4, example 1 (difficulty 4, long-form proof).** Reservoir sampling keeps the first $k$ items; item $i > k$ (counted from 1) enters with probability $\frac{k}{i}$, replacing a uniformly chosen reservoir slot. Prove that after $n \ge k$ items every item is in the reservoir with probability $\frac{k}{n}$.

*Model answer:* (1) Claim: after $i \ge k$ items, each of them is in the reservoir with probability $\frac{k}{i}$. Base $i = k$: probability 1. (2) Step: item $i + 1$ enters with probability $\frac{k}{i + 1}$, as required for it. (3) An item already present stays unless the new item enters and picks its slot: probability $\frac{k}{i + 1} \cdot \frac1k = \frac{1}{i + 1}$. (4) So it remains with probability $\frac{k}{i}\left(1 - \frac{1}{i + 1}\right) = \frac{k}{i + 1}$. (5) By induction the claim holds at $n$; the stream's length need not be known in advance, and a simulation of 200,000 runs with $k = 2$, $n = 6$ gave every item between 0.332 and 0.334 against $\frac13$ [verified].
*Rubric (10):* 2 for the claim and base; 2 for the new item's chance; 2 for the eviction chance; 2 for the product; 2 for the conclusion.

**SQ4, example 2 (difficulty 5, numeric and code).** (a) Under "swap each position $i$ with a uniformly random position from all $n$", find the probability of each order of 3 cards. (b) Write `fisher_yates(a, rand_index)` where `rand_index(lo, hi)` returns an integer in $[lo, hi)$, and say how a test can prove uniformity for $n = 4$ without randomness.

*Answer:* (a) Three orders have probability $\frac{4}{27}$ and three have $\frac{5}{27}$ (27 equally likely choice sequences cannot split evenly into 6). (b)

```python
def fisher_yates(a: list, rand_index) -> list:
    a = list(a)
    for i in range(len(a) - 1):
        j = rand_index(i, len(a))       # j in [i, n): the remaining unplaced items
        a[i], a[j] = a[j], a[i]
    return a
```

*Checks:* the hidden test passes a `rand_index` that replays every possible sequence of choices (4 · 3 · 2 = 24 sequences for $n = 4$) and asserts each of the 24 orders appears exactly once [verified]; the naive version fails because 256 sequences cannot cover 24 orders equally. *Decision point:* drawing from $[i + 1, n)$ instead produces only single cycles (Sattolo).

**TG1, example 1 (difficulty 4, code).** Write `diameter(root)` returning the number of edges on the longest path between two nodes of a binary tree.

*Answer:*

```python
def diameter(root) -> int:
    best = 0
    def height(t) -> int:               # returns height in edges; empty tree is -1
        nonlocal best
        if t is None:
            return -1
        hl, hr = height(t.left), height(t.right)
        best = max(best, hl + hr + 2)   # records the path through t
        return 1 + max(hl, hr)          # returns only one branch to the parent
    height(root)
    return best
```

*Checks:* the tree 1 with children 2 (children 4, 5) and 3 gives 3; a single node gives 0; a path of 6 nodes gives 5; random trees against an all-pairs BFS; depth capped at 500 (decision 25). *Decision point:* returning `hl + hr + 2` to the parent lets a path turn twice.

**TG1, example 2 (difficulty 5, code).** Write `max_path_sum(root)` returning the largest sum of a non-empty path between any two nodes, with negative values allowed.

*Answer:*

```python
def max_path_sum(root) -> int:
    best = float("-inf")
    def gain(t) -> int:                         # best downward path starting at t, or 0 if negative
        nonlocal best
        if t is None:
            return 0
        left, right = max(0, gain(t.left)), max(0, gain(t.right))
        best = max(best, t.val + left + right)  # a path may bend at t
        return t.val + max(left, right)
    gain(root)
    return best
```

*Checks:* the tree −10 with children 9 and 20 (children 15, 7) gives 42; a single node −3 gives −3; 1 with children 2 and 3 gives 6; random trees against enumerating every pair's path. *Decision point:* initialising `best = 0` returns 0 for an all-negative tree, where a non-empty path must be negative.

**TG2, example 1 (difficulty 4, code).** Write `is_valid_bst(root)` checking strict ordering in every subtree.

*Answer:*

```python
def is_valid_bst(root) -> bool:
    stack = [(root, float("-inf"), float("inf"))]   # iterative: no recursion limit
    while stack:
        t, lo, hi = stack.pop()
        if t is None:
            continue
        if not (lo < t.val < hi):
            return False
        stack.append((t.left, lo, t.val))       # everything on the left is below t.val
        stack.append((t.right, t.val, hi))      # everything on the right is above it
    return True
```

*Checks:* 5 with children 1 and 4 (children 3, 6) is invalid; the tree 5, left 3 with right child 6, is invalid although every parent check passes; duplicates are invalid (strict rule stated); a skewed tree of 10,000 nodes runs without recursion. *Decision point:* comparing each node only with its parent accepts the second tree.

**TG2, example 2 (difficulty 5, long-form proof).** Prove that the interval check is correct: a binary tree is a BST exactly when every node's value lies strictly inside the interval passed down to it.

*Model answer:* (1) Define the interval of the root as $(-\infty, \infty)$ and pass $(lo, v)$ to the left child and $(v, hi)$ to the right child of a node with value $v$. (2) By induction on depth, a node's interval is exactly the set of values allowed by all its ancestors: going left from $v$ adds "below $v$", going right adds "above $v$". (3) If the tree is a BST, every node respects each ancestor, so it lies in its interval. (4) Conversely, if every node lies in its interval, every node respects every ancestor, which is the BST property. (5) The parent-only check enforces only the last of these constraints, so a deep node can violate a grandparent, as 6 under 3 under 5 does.
*Rubric (10):* 2 for the interval rule; 2 for the induction on depth; 2 for one direction; 2 for the other; 2 for the counterexample explained.

**TG3, example 1 (difficulty 4, code).** Write `course_order(n, prereqs)` returning one valid order of courses $0$ to $n - 1$ (pairs `(a, b)` mean $b$ before $a$), or `[]` if none exists.

*Answer:*

```python
from collections import deque

def course_order(n: int, prereqs: list[tuple[int, int]]) -> list[int]:
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in prereqs:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while q:
        v = q.popleft()
        order.append(v)
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    return order if len(order) == n else []      # a cycle leaves some courses unplaced
```

*Checks:* $n = 4$ with (1, 0), (2, 0), (3, 1), (3, 2): any of the two valid orders is accepted by `topoOrderValid`; a two-course cycle returns `[]`; no prerequisites returns any permutation; random DAGs with $2 \times 10^5$ edges. *Decision point:* returning `order` without the length check hides a cycle.

**TG3, example 2 (difficulty 5, long-form proof).** Prove that BFS from $s$ in an unweighted graph assigns every reachable node its shortest distance.

*Model answer:* (1) Invariant: the queue holds nodes in non-decreasing order of assigned distance, and its first and last differ by at most 1. (2) Initially it holds only $s$ at distance 0. (3) Popping $u$ at distance $d$ appends unvisited neighbours at $d + 1$, which keeps both properties. (4) Suppose some node $v$ got $d(v) > \delta(v)$, the true distance, and take such a $v$ with the smallest $\delta(v)$; its predecessor $u$ on a shortest path has $d(u) = \delta(u) = \delta(v) - 1$, and when $u$ was popped, $v$ was either queued then at $\delta(v)$ or already queued at a distance at most $d(u) + 1$ by the ordering. (5) Either way $d(v) \le \delta(v)$, a contradiction; and $d(v) \ge \delta(v)$ always, since every assignment follows a real path. Marking on push matters: marking on pop lets a node be queued twice.
*Rubric (10):* 2 for the invariant; 2 for maintaining it; 2 for the minimal counterexample; 2 for the contradiction; 2 for the lower bound and the marking remark.

**TG4, example 1 (difficulty 4, code).** Write `network_delay(times, n, k)`: directed edges `(u, v, w)` with $w \ge 0$; return the time for a signal from $k$ to reach all nodes $1$ to $n$, or $-1$.

*Answer:*

```python
import heapq
from collections import defaultdict

def network_delay(times: list[tuple[int, int, int]], n: int, k: int) -> int:
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    dist: dict[int, int] = {}
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in dist:
            continue                          # a stale entry: u was settled more cheaply
        dist[u] = d
        for v, w in graph[u]:
            if v not in dist:
                heapq.heappush(heap, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1
```

*Checks:* [(2, 1, 1), (2, 3, 1), (3, 4, 1)], $n = 4$, $k = 2$ gives 2; [(1, 2, 1)], $n = 2$, $k = 2$ gives $-1$; random graphs against Bellman-Ford; a `complexity` test with $10^5$ edges. *Decision point:* settling on push gives wrong answers when a later, cheaper path exists.

**TG4, example 2 (difficulty 5, code).** Write `find_arbitrage(rates, eps=1e-9)` where `rates[(a, b)]` converts one unit of `a` into `rates[(a, b)]` units of `b`; return a list of currencies forming a cycle whose rate product exceeds $1 + \varepsilon$, or `None`.

*Answer:*

```python
import math

def find_arbitrage(rates: dict[tuple[str, str], float], eps: float = 1e-9):
    nodes = sorted({a for a, _ in rates} | {b for _, b in rates})
    dist = {v: 0.0 for v in nodes}                    # a virtual source to every node
    pred = {v: None for v in nodes}
    edges = [(a, b, -math.log(r)) for (a, b), r in rates.items()]
    last = None
    for _ in range(len(nodes)):                       # one extra round detects a cycle
        last = None
        for a, b, w in edges:
            if dist[a] + w < dist[b] - eps:
                dist[b], pred[b], last = dist[a] + w, a, b
    if last is None:
        return None
    v = last
    for _ in range(len(nodes)):                       # step back into the cycle itself
        v = pred[v]
    cycle, u = [v], pred[v]
    while u != v:
        cycle.append(u)
        u = pred[u]
    cycle.reverse()
    return cycle + [cycle[0]]
```

*Checks:* with USD → EUR 0.92, EUR → USD 1.08, EUR → GBP 0.85, GBP → EUR 1.17, GBP → USD 1.28, USD → GBP 0.78, USD → JPY 150 and JPY → USD 0.00666, the returned cycle's product exceeds 1 and is USD, EUR, GBP, USD in some rotation ($0.92 \times 0.85 \times 1.28 = 1.00096$); a table of rates derived from one set of true prices returns `None`; the hidden test multiplies the returned rates itself. *Decision point:* without the tolerance, rounding in $-\ln r$ reports "arbitrage" in consistent tables.

**TG5, example 1 (difficulty 4, code).** Write `floyd_warshall(n, edges)` returning the matrix of shortest distances (infinity where unreachable) and a flag that is true when a negative cycle exists.

*Answer:*

```python
def floyd_warshall(n: int, edges: list[tuple[int, int, float]]):
    INF = float("inf")
    d = [[0.0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)                    # parallel edges keep the cheapest
    for k in range(n):                               # outermost: paths through 0..k only
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            row = d[i]
            for j in range(n):
                if dik + dk[j] < row[j]:
                    row[j] = dik + dk[j]
    return d, any(d[i][i] < 0 for i in range(n))
```

*Checks:* a 4-node graph against four Dijkstra runs; a 3-cycle with total weight $-1$ sets the flag; unreachable pairs stay infinite; random graphs against Bellman-Ford from every source. *Decision point:* the `k` loop inside the `i` and `j` loops is a different, wrong algorithm; the wrong file fails a 4-node case.

**TG5, example 2 (difficulty 5, long-form proof).** Prove the cut property: for any partition of the nodes into $S$ and $V \setminus S$, a lightest edge crossing the partition belongs to some minimum spanning tree.

*Model answer:* (1) Let $e = (u, v)$ be a lightest crossing edge and $T$ a minimum spanning tree; if $e \in T$ we are done. (2) Otherwise $T + e$ contains a cycle through $e$, which must cross the cut a second time at some edge $f$. (3) $w(e) \le w(f)$ because $e$ is a lightest crossing edge. (4) $T' = T + e - f$ is connected (the cycle is broken at $f$, not disconnected) with $n - 1$ edges, so it is a spanning tree with $w(T') \le w(T)$. (5) Hence $T'$ is a minimum spanning tree containing $e$; Kruskal's and Prim's choices are both lightest crossing edges of a cut, so both are correct.
*Rubric (10):* 2 for the setup; 2 for the cycle and the second crossing; 2 for the weight comparison; 2 for $T'$ being a spanning tree of no greater weight; 2 for applying it to both algorithms.

**DP1, example 1 (difficulty 4, code).** Write `permute_unique(nums)` returning all distinct permutations of a list that may contain duplicates, without generating duplicates.

*Answer:*

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    a = sorted(nums)
    used = [False] * len(a)
    out, cur = [], []
    def bt() -> None:
        if len(cur) == len(a):
            out.append(cur[:])                 # a copy: cur keeps changing
            return
        for i in range(len(a)):
            if used[i]:
                continue
            if i > 0 and a[i] == a[i - 1] and not used[i - 1]:
                continue                       # equal values are used left to right only
            used[i] = True; cur.append(a[i])
            bt()
            cur.pop(); used[i] = False
    bt()
    return out
```

*Checks:* [1, 1, 2] gives 3 permutations; [1, 2, 3] gives 6; [2, 2, 2] gives 1; random lists against `set(itertools.permutations(...))`; a line-budget test that a generate-then-deduplicate solution fails on [1] × 9 + [2]. *Decision point:* `out.append(cur)` returns the same list object every time, empty at the end.

**DP1, example 2 (difficulty 5, code).** Write `n_queens_count(n)` for $n \le 12$ within the drill's time limit.

*Answer:*

```python
def n_queens_count(n: int) -> int:
    count = 0
    def place(row: int, cols: int, diag1: int, diag2: int) -> None:   # bitmasks of attacked squares
        nonlocal count
        if row == n:
            count += 1
            return
        free = ~(cols | diag1 | diag2) & ((1 << n) - 1)
        while free:
            bit = free & -free                  # the lowest free column
            free -= bit
            place(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1)
    place(0, 0, 0, 0)
    return count
```

*Checks:* counts 1, 0, 0, 2, 10, 4, 40, 92 for $n = 1$ to 8, and 724 for $n = 10$ [verified]; $n = 12$ (14,200 [verified]) within the time limit. *Decision point:* checking a full board before pruning cannot finish $n = 10$.

**DP2, example 1 (difficulty 4, code).** Write `coin_ways(coins, amount)` counting the combinations (orders ignored) that make `amount`.

*Answer:*

```python
def coin_ways(coins: list[int], amount: int) -> int:
    ways = [1] + [0] * amount                 # ways[0] = 1: the empty combination
    for c in coins:                           # coins outside: each combination counted once
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount]
```

*Checks:* [1, 2, 5] and 5 give 4; [2] and 3 give 0; amount 0 gives 1; random cases against enumeration of multisets. *Decision point:* swapping the loops gives 9 for [1, 2, 5] and 5, the number of ordered sequences.

**DP2, example 2 (difficulty 5, long-form).** Explain why the loop order decides whether coin counting counts combinations or orderings, derive both counts for coins {1, 2, 5} and amount 5, and say which a cashier's problem needs.

*Model answer:* (1) With coins outside, after processing coin $c$ the table counts combinations using only the coins seen so far, so each combination is built in one canonical order (coins in list order). (2) With the amount outside, `ways[a]` sums over the last coin used, counting every ordered sequence separately. (3) Combinations of 5: {5}, {2, 2, 1}, {2, 1, 1, 1}, {1, 1, 1, 1, 1}: 4. (4) Orderings: $5$; $2{+}2{+}1$ in 3 orders; $2{+}1{+}1{+}1$ in 4 orders; $1{+}1{+}1{+}1{+}1$ once: $1 + 3 + 4 + 1 = 9$. (5) Paying a sum is a combination problem; counting sequences of trades or steps (climbing stairs) is an ordering problem.
*Rubric (10):* 2 for the coins-outside invariant; 2 for the amount-outside recurrence; 2 for the 4 combinations; 2 for the 9 orderings; 2 for the application.

**DP3, example 1 (difficulty 4, code).** Write `max_profit_k(prices, k)`: at most `k` buy-sell round trips, never holding more than one unit.

*Answer:*

```python
def max_profit_k(prices: list[float], k: int) -> float:
    if k == 0 or len(prices) < 2:
        return 0.0
    if 2 * k >= len(prices):                         # as good as unlimited: sum every rise
        return sum(max(0.0, b - a) for a, b in zip(prices, prices[1:]))
    buy = [float("-inf")] * (k + 1)                  # best cash after the j-th buy
    sell = [0.0] * (k + 1)                           # best cash after the j-th sell
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]
```

*Checks:* [3, 3, 5, 0, 0, 3, 1, 4] with $k = 2$ gives 6 and with $k = 1$ gives 4; [3, 2, 6, 5, 0, 3] with $k = 2$ gives 7; random inputs against brute force over choices; $k = 10^9$ on $10^5$ prices takes the shortcut. *Decision point:* without the shortcut, a huge $k$ makes the table $O(nk)$.

**DP3, example 2 (difficulty 5, long-form derivation).** Derive the edit-distance recurrence for $D[i][j]$, the distance between the first $i$ letters of $a$ and the first $j$ of $b$, and argue that the three cases cover every optimal edit sequence.

*Model answer:* (1) Consider an optimal alignment of $a_{1..i}$ and $b_{1..j}$ and look at its last column. (2) Either $a_i$ is deleted (cost $1 + D[i - 1][j]$), $b_j$ is inserted (cost $1 + D[i][j - 1]$), or $a_i$ is aligned with $b_j$ (cost $D[i - 1][j - 1]$ plus 0 if they match, 1 if replaced). (3) Every alignment's last column is one of these three, and the rest of the alignment is an alignment of the shorter prefixes, which must itself be optimal (optimal substructure). (4) So $D[i][j] = \min$ of the three, with $D[i][0] = i$ and $D[0][j] = j$. (5) "kitten" to "sitting" gives 3; the table has $(m + 1)(n + 1)$ cells, $O(mn)$ time, and a traceback recovers the edits.
*Rubric (10):* 2 for the last-column view; 2 for the three cases with costs; 2 for completeness and optimal substructure; 2 for base cases; 2 for the example and cost.

**DP4, example 1 (difficulty 4, code).** Write `rob_tree(root)` returning the largest sum of node values with no node and its parent both taken.

*Answer:*

```python
def rob_tree(root) -> int:
    def best(t) -> tuple[int, int]:           # (best if t is taken, best if t is skipped)
        if t is None:
            return 0, 0
        lt, ls = best(t.left)
        rt, rs = best(t.right)
        take = t.val + ls + rs                # children must be skipped
        skip = max(lt, ls) + max(rt, rs)      # children free either way
        return take, skip
    return max(best(root))
```

*Checks:* 3 with children 2 (right child 3) and 3 (right child 1) gives 7; 3 with children 4 (children 1, 3) and 5 (right child 1) gives 9; a single node; random trees against brute force over independent sets. *Decision point:* recomputing grandchildren's answers at each node is exponential; returning the pair makes it $O(n)$.

**DP4, example 2 (difficulty 5, long-form).** Explain why backward induction prices a European option on an $N$-step recombining binomial tree in $O(N^2)$ time and $O(N)$ memory, and why an Asian option on the running average destroys the saving.

*Model answer:* (1) After $i$ steps the price depends only on the number of up moves, so there are $i + 1$ nodes, not $2^i$ paths: the tree recombines. (2) Backward induction computes each node's value from its two children: $\sum_{i=0}^{N-1}(i + 1) = \frac{N(N + 1)}{2}$ updates (5,050 for $N = 100$) against $2^N$ paths. (3) Each level needs only the next level, so one array of length $N + 1$, overwritten in place, is enough. (4) An Asian payoff depends on the whole path's average, so two paths reaching the same node with different averages are different states; the state is (step, up moves, running sum), and the number of distinct running sums grows with the number of paths, far faster than $N$. (5) So path-dependent options need extra state, approximation on a grid of averages, or Monte Carlo (1.9 lesson 65).
*Rubric (10):* 2 for recombination; 2 for the update count; 2 for the one-array memory; 2 for why path dependence multiplies states; 2 for the remedies.

**DP5, example 1 (difficulty 4, code).** Write `min_jumps(nums)` returning the fewest jumps from index 0 to the last index, where `nums[i]` is the furthest jump from `i`; reaching the end is guaranteed.

*Answer:*

```python
def min_jumps(nums: list[int]) -> int:
    jumps, end, far = 0, 0, 0
    for i in range(len(nums) - 1):        # the last index needs no jump from it
        far = max(far, i + nums[i])       # furthest reach from the current layer
        if i == end:                      # the current layer is exhausted: jump
            jumps += 1
            end = far
    return jumps
```

*Checks:* [2, 3, 1, 1, 4] gives 2; [2, 3, 0, 1, 4] gives 2; a one-element list gives 0; random reachable inputs against BFS; a `complexity` test at $n = 2 \times 10^5$ that an $O(n^2)$ DP fails. *Decision point:* looping to `len(nums)` counts an extra jump when the last layer ends exactly at the final index.

**DP5, example 2 (difficulty 5, long-form proof).** Prove Huffman's greedy choice: some optimal prefix code has the two least frequent symbols as siblings at the greatest depth.

*Model answer:* (1) Take an optimal code tree $T$; it is full (every internal node has two children), otherwise a code could be shortened. (2) Let $a, b$ be the two least frequent symbols and $x, y$ siblings at the greatest depth in $T$. (3) Swapping $a$ with $x$ changes the cost by $(f_x - f_a)(d_a - d_x) \le 0$, because $f_a \le f_x$ and $d_a \le d_x$; the same for $b$ and $y$. (4) The swapped tree is still optimal and has $a, b$ as deepest siblings. (5) Merging them into one symbol of frequency $f_a + f_b$ reduces the problem by one symbol, and induction completes the proof that repeated merging is optimal; for frequencies 60, 20, 12, 5, 3 it gives 1.68 bits per symbol.
*Rubric (10):* 2 for fullness; 2 for choosing the deepest siblings; 2 for the swap cost; 2 for preserved optimality; 2 for the induction step.

**DP6, example 1 (difficulty 4, code).** Write `fib_mod(n, m)` returning $F_n \bmod m$ for $n$ up to $10^{18}$ in $O(\log n)$, with $F_0 = 0$, $F_1 = 1$.

*Answer:*

```python
def fib_mod(n: int, m: int) -> int:
    def mul(A, B):
        return [[(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % m, (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % m],
                [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % m, (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % m]]
    result, base = [[1 % m, 0], [0, 1 % m]], [[1, 1], [1, 0]]
    while n:                                  # square-and-multiply on the matrix
        if n & 1:
            result = mul(result, base)
        base = mul(base, base)
        n >>= 1
    return result[0][1]
```

*Checks:* $F_{10} \bmod 1000 = 55$; $F_{90}$ with a huge modulus is 2,880,067,194,370,816,120; $F_{10^{18}} \bmod (10^9 + 7) = 209{,}783{,}453$ [verified]; $m = 1$ gives 0. *Decision point:* iterating $n$ times cannot reach $10^{18}$.

**DP6, example 2 (difficulty 5, long-form).** Explain two's complement: why an 8-bit pattern of $-x$ equals the bits of $x$ flipped plus 1, why $-10$ is 11110110, and why Python's `~x` equals $-x - 1$ and `-5 >> 1` equals $-3$.

*Model answer:* (1) An $w$-bit two's complement pattern represents its unsigned value minus $2^w$ when the top bit is set, so $-x$ is stored as $2^w - x$. (2) Flipping every bit of $x$ gives $(2^w - 1) - x$; adding 1 gives $2^w - x$. (3) For $x = 10 = 00001010$: flipped is 11110101, plus 1 is 11110110 (246 unsigned, $-10$ signed). (4) Python integers have no width, behaving as if sign-extended forever, so `~x` is $-x - 1$ for every integer (the same identity with no wrap). (5) Python's `>>` is an arithmetic shift that floors: $-5 = \dots 11011$, shifted is $\dots 1101 = -3 = \lfloor -2.5 \rfloor$; masking with `& 0xFF` recovers fixed-width behaviour when needed.
*Rubric (10):* 2 for the meaning of a negative pattern; 2 for flip plus one; 2 for the worked $-10$; 2 for Python's `~`; 2 for the shift and masking.

**DP7, example 1 (difficulty 4, code).** Write `stress_finder(fast, brute, gen, trials)` that calls `gen(seed)` for seeds 0, 1, 2, ..., returns the first input on which `fast` and `brute` disagree, shrunk by removing single elements while the disagreement persists, or `None`.

*Answer:*

```python
def stress_finder(fast, brute, gen, trials: int = 10_000):
    for seed in range(trials):
        x = gen(seed)                                   # seeded, so a failure reproduces
        if fast(list(x)) != brute(list(x)):
            shrunk = list(x)
            changed = True
            while changed:                              # greedy one-element shrinking
                changed = False
                for i in range(len(shrunk)):
                    cand = shrunk[:i] + shrunk[i + 1:]
                    if cand and fast(list(cand)) != brute(list(cand)):
                        shrunk, changed = cand, True
                        break
            return shrunk
    return None
```

*Checks:* with a maximum-subarray `fast` that starts `best = 0` and a correct brute force, the finder returns a one-element negative list ([-4] for the tests' seeded generator [verified]); with a correct `fast` it returns `None`; functions receive copies so they cannot mutate the case. *Decision point:* without shrinking, the reported failure is a 30-element list that hides the cause.

**DP7, example 2 (difficulty 5, long-form, method).** Write the full method for this unseen medium: count the contiguous subarrays of an integer array whose sum is divisible by $k$ ($n \le 3 \times 10^4$, values may be negative).

*Model answer:* (1) Restatement and examples: [4, 5, 0, -2, -3, 1] with $k = 5$ has 7 such subarrays; edge cases: one element, all zeros, negative values. (2) Brute force: all $O(n^2)$ pairs of ends with running sums, about $4.5 \times 10^8$ steps at $n = 3 \times 10^4$, too slow in Python. (3) Insight: a subarray $(i, j]$ has sum $P_j - P_i$, divisible by $k$ exactly when $P_i \equiv P_j \pmod k$, so count equal prefix remainders. (4) Algorithm: a dictionary of remainder counts starting with $\{0: 1\}$; for each prefix add the count of its remainder, then increment it; Python's `%` is already non-negative for positive $k$, while C++ needs `((s % k) + k) % k`. (5) Analysis: $O(n)$ time, $O(\min(n, k))$ space; tested against the brute force on random small arrays including negatives.
*Rubric (10):* 2 for examples and edge cases; 2 for an honest brute force with its cost; 2 for the remainder insight; 2 for the algorithm including the empty prefix and negative remainders; 2 for complexity and testing.

### 3.2 Item 1.9 C++

| Level | Set | Items | Mix | Long-form (five points of 2 marks) | C++ drills | Generators |
|---|---|---|---|---|---|---|
| CB1 | `set.cppcore.build` | 7 | d3 ×3, d4 ×2, d5 ×2 | The four build stages, and how to fix "undefined reference" in a three-file program | `drl.cpp.argv-sum`, `drl.cpp.split-build` (local paste), `drl.cpp.fix-five-errors` | `gen.cpp.error-stage`, `gen.cpp.include-graph` |
| CB2 | `set.cppcore.types` | 7 | as above | Why the overflow loop changes with `-O2`, and two safe rewrites | `drl.cpp.mul-fits`, `drl.cpp.ticks-to-price`, `drl.cpp.python-mod` | `gen.cpp.arith-predict`, `gen.cpp.conversion-predict` |
| CB3 | `set.cppcore.functions` | 7 | as above | Value, reference or const reference: choose for five parameters and justify | `drl.cpp.vwap`, `drl.cpp.overload-format`, `drl.cpp.inline-header` | `gen.cpp.overload-pick`, `gen.cpp.rebuild-set` |
| CB4 | `set.cppcore.containers` | 7 | as above | Review a 6-line function with three bugs | `drl.cpp.simple-returns`, `drl.cpp.parse-occ`, `drl.cpp.pricer-tests` | `gen.cpp.vector-predict`, `gen.cpp.string-predict` |
| CM1 | `set.cppmemory.model` | 7 | as above | Read three sanitiser reports and explain each fix | `drl.cpp.raii-leak-fix`, `drl.cpp.pack-struct`, `drl.cpp.pointer-sum` | `gen.cpp.layout`, `gen.cpp.lifetime-predict` |
| CM2 | `set.cppmemory.classes` | 7 | as above | RAII and unwinding, with a file, a lock and a buffer | `drl.cpp.money`, `drl.cpp.price-invariant`, `drl.cpp.scoped-timer` | `gen.cpp.init-order`, `gen.cpp.dtor-order` |
| CM3 | `set.cppmemory.ownership` | 7 | as above | The rule of zero against the rule of five, with vector reallocation | `drl.cpp.buffer-five`, `drl.cpp.unique-book`, `drl.cpp.weak-cycle` | `gen.cpp.copy-move-predict`, `gen.cpp.use-count` |
| CM4 | `set.cppmemory.design` | 7 | as above | Virtual dispatch against templates for a pricer | `drl.cpp.payoff-clone`, `drl.cpp.variant-quote`, `drl.cpp.payoff-factory` | `gen.cpp.dispatch-predict` |
| CL1 | `set.cppstl.templates` | 7 | as above | What concepts change in error messages and in an API's contract | `drl.cpp.mean-concept`, `drl.cpp.matrix-template`, `drl.cpp.constexpr-table` | `gen.cpp.deduction-predict` |
| CL2 | `set.cppstl.containers` | 7 | as above | Containers for an order book, justified by costs and invalidation | `drl.cpp.book-levels`, `drl.cpp.erase-cancelled`, `drl.cpp.span-stats` | `gen.cpp.capacity-predict`, `gen.cpp.invalidation` |
| CL3 | `set.cppstl.algorithms` | 7 | as above | Strict weak ordering: why `<=` breaks `std::sort` | `drl.cpp.sort-trades`, `drl.cpp.dijkstra`, `drl.cpp.prefix-returns` | `gen.cpp.algo-predict` |
| CL4 | `set.cppstl.numerics` | 7 | as above | Kahan summation, `-ffast-math` and the right fix | `drl.cpp.mc-call`, `drl.cpp.bs-call`, `drl.cpp.kahan` | `gen.cpp.float-predict` |
| CP1 | `set.cpppricing.tools` | 7 | as above | A review of a 40-line pricer against the Core Guidelines | `drl.cpp.cmake-project` (local paste), `drl.cpp.debug-crash`, `drl.cpp.bind-pricer` (local, optional) | `gen.cpp.flag-effect` |
| CP2 | `set.cpppricing.performance` | 7 | as above | The subnormal slowdown: cause, measurement and fix | `drl.cpp.soa-sum`, `drl.cpp.reserve-hot-loop`, `drl.cpp.bench-harness` | `gen.cpp.cache-lines`, `gen.cpp.speedup-interval` |
| CP3 | `set.cpppricing.pricer` | 7 | as above | The exit's timing protocol and how to report a speed-up | `drl.cpp.crr-european`, `drl.cpp.crr-american`, `drl.cpp.crr-tests` | `gen.cpp.crr-small` |
| CP4 | `set.cpppricing.concurrency` | 7 | as above | Why a data race is undefined, and two fixes | `drl.cpp.atomic-counter`, `drl.cpp.parallel-mc`, `drl.cpp.padded-counters` | `gen.cpp.race-predict` |

**Example problems, 1.9.** Every reference solution below compiled warning-free with GCC 13.3 (`-std=c++20 -Wall -Wextra -O2`) and Clang 18.1, and passed its checks, also under `-fsanitize=address,undefined` (section 0.6). Tests are written in doctest form; here they ran as plain assertions because doctest was not installed.

**CB1, example 1 (difficulty 3, match).** Match each message to the stage that produced it: (a) "fatal error: quote.h: No such file or directory"; (b) "error: 'cout' is not a member of 'std'"; (c) "undefined reference to `vwap(...)'"; (d) "error: expected ';' before 'return'"; (e) "multiple definition of `fee(double)'"; (f) "#error unsupported platform".

*Answer:* (a) preprocessor; (b) compiler; (c) linker; (d) compiler; (e) linker; (f) preprocessor.
*Working:* the preprocessor handles `#include` and `#error`; the compiler checks one translation unit's syntax and names; the linker joins symbols across objects. *Decision point:* (b) looks like a missing file but is a compile error: the header that declares `std::cout` was never included, so the name is unknown.

**CB1, example 2 (difficulty 5, long-form).** `main.cpp` calls `double vwap(const std::vector<double>&, const std::vector<long long>&)`, declared in `vwap.h`; `vwap.cpp` defines it. The build `g++ main.cpp -o app` fails with "undefined reference to `vwap(...)`". Explain the four stages, why this error appears, and two correct fixes.

*Model answer:* (1) The preprocessor pastes `vwap.h` into `main.cpp`, so the compiler sees a declaration. (2) The compiler turns `main.cpp` into an object file in which `vwap` is an undefined symbol, which is legal: a declaration promises a definition elsewhere. (3) The assembler step produces machine code; the linker must then find a definition for every undefined symbol. (4) `vwap.cpp` was never compiled or linked, so no object defines `vwap`: the linker reports "undefined reference". (5) Fixes: compile both, `g++ main.cpp vwap.cpp -o app`, or add `vwap.cpp` to the executable's sources in CMake (`add_executable(app main.cpp vwap.cpp)` or a library linked with `target_link_libraries`); a mismatch between the declared and defined signatures gives the same message and is fixed by making them agree.
*Rubric (10):* 2 for the preprocessor's role; 2 for declarations creating undefined symbols; 2 for the linker's job; 2 for diagnosing the missing object; 2 for two fixes, including the signature mismatch.

**CB2, example 1 (difficulty 4, predict).** On x86-64 Linux with GCC 13, give the value (and type where asked) of: (a) `-1 < 1u`; (b) `sizeof(long)`; (c) `uint8_t a = 200, b = 100; a + b` (type and value); (d) `7 / 2 * 2.0`; (e) `-7 % 3`; (f) `static_cast<unsigned>(-1)`.

*Answer:* (a) `false` (0); (b) 8; (c) `int`, 300; (d) 6 (a `double`); (e) −1; (f) 4,294,967,295 [all verified].
*Working:* (a) −1 converts to `unsigned`, 4,294,967,295; (c) both operands promote to `int` before adding; (d) `7 / 2` is integer division, 3, then $3 \times 2.0$; (e) C++ truncates the quotient towards zero ($-2$), so the remainder takes the dividend's sign. *Decision point:* answering (e) with Python's 2 is the commonest error in this set.

**CB2, example 2 (difficulty 5, code).** Write `bool mul_fits(std::int64_t a, std::int64_t b, std::int64_t& out)` that stores $a \times b$ in `out` and returns `true` when it fits in 64 bits, and returns `false` otherwise, with no undefined behaviour on any input.

*Answer:*

```cpp
#include <cstdint>
#include <limits>

bool mul_fits(std::int64_t a, std::int64_t b, std::int64_t& out) {
    using L = std::numeric_limits<std::int64_t>;
    if (a == 0 || b == 0) { out = 0; return true; }
    if (a == -1) { if (b == L::min()) return false; out = -b; return true; }   // -MIN overflows
    if (b == -1) { if (a == L::min()) return false; out = -a; return true; }
    bool overflow = a > 0 ? (b > 0 ? a > L::max() / b : b < L::min() / a)    // check before multiplying:
                          : (b > 0 ? a < L::min() / b : b < L::max() / a);  // the check itself never overflows
    if (overflow) return false;
    out = a * b;
    return true;
}
```

*Checks:* `mul_fits(INT64_MAX, 2, x)` is false; `mul_fits(-1, INT64_MIN, x)` is false; `mul_fits(3, 4, x)` is true with 12; 200,000 random pairs agree with GCC's `__builtin_mul_overflow` [verified]; the hidden build uses `-fsanitize=undefined`. *Decision point:* multiplying first and testing the result afterwards is itself the undefined behaviour the function exists to avoid.

**CB3, example 1 (difficulty 4, code).** Write `double vwap(const std::vector<double>& px, const std::vector<long long>& qty)` returning the volume-weighted average price, throwing `std::invalid_argument` on mismatched sizes or zero total volume.

*Answer:*

```cpp
#include <stdexcept>
#include <vector>

double vwap(const std::vector<double>& px, const std::vector<long long>& qty) {
    if (px.size() != qty.size()) throw std::invalid_argument("size mismatch");
    long long volume = 0;                 // integer volume: exact
    double notional = 0.0;
    for (std::size_t i = 0; i < px.size(); ++i) {
        notional += px[i] * static_cast<double>(qty[i]);
        volume += qty[i];
    }
    if (volume == 0) throw std::invalid_argument("zero volume");
    return notional / static_cast<double>(volume);
}
```

*Checks:* `vwap({100, 101}, {100, 300})` is 100.75; sizes 2 and 3 throw; `vwap({1}, {0})` throws; a test passes 10 million fills to confirm no copy is made (`const&`). *Decision point:* taking the vectors by value compiles and passes every value test while copying both inputs on every call.

**CB3, example 2 (difficulty 5, long-form).** Choose value, reference or const reference for each parameter and justify: (a) a `double` spot price; (b) a `std::vector<double>` of $10^6$ path values read by a pricer; (c) a `std::vector<Fill>` that a function appends fills to; (d) a `std::string` ticker stored inside a new `Order`; (e) a small `struct Point { double x, y; }`.

*Model answer:* (1) (a) by value: a `double` is 8 bytes and copying it is cheaper than an indirection. (2) (b) by `const&` (or `std::span<const double>`): no copy of 8 MB and the function cannot modify it. (3) (c) by non-`const` reference: the caller's vector must change; a pointer works too but must not be null. (4) (d) by value and then `std::move` into the member: callers passing a temporary pay one move, callers passing an lvalue pay exactly the one copy that storing requires. (5) (e) by value: two doubles are cheaper to copy than to reference; the rule is "cheap to copy and not modified: by value; expensive and only read: `const&`; modified: `&`".
*Rubric (10):* 2 each for (a) with (e) together, (b), (c), (d), and the general rule stated.

**CB4, example 1 (difficulty 4, code).** Write `std::vector<double> simple_returns(const std::vector<double>& px)` returning $p_i / p_{i-1} - 1$ for $i \ge 1$, and an empty vector for fewer than 2 prices; write its doctest cases.

*Answer:*

```cpp
#include <vector>

std::vector<double> simple_returns(const std::vector<double>& px) {
    std::vector<double> r;
    if (px.size() < 2) return r;              // avoids px.size() - 1 wrapping round on an empty vector
    r.reserve(px.size() - 1);
    for (std::size_t i = 1; i < px.size(); ++i) r.push_back(px[i] / px[i - 1] - 1.0);
    return r;
}

// TEST_CASE("simple returns") {
//     auto r = simple_returns({100, 110, 99});
//     REQUIRE(r.size() == 2);
//     CHECK(r[0] == doctest::Approx(0.10));
//     CHECK(r[1] == doctest::Approx(-0.10));
//     CHECK(simple_returns({}).empty());
//     CHECK(simple_returns({100}).empty());
// }
```

*Checks:* the cases above; a $10^6$-price input under AddressSanitizer. *Decision point:* `for (size_t i = 0; i < px.size() - 1; ++i)` on an empty vector runs about $1.8 \times 10^{19}$ times and reads out of bounds.

**CB4, example 2 (difficulty 5, find the bugs).** Name the three bugs in this function, what each does on `{100, 110, 121}` and on `{}`, and the fix.

```cpp
double mean_return(const std::vector<double>& px) {
    std::vector<double> r;
    for (size_t i = 0; i < px.size() - 1; ++i) r.push_back(px[i + 1] / px[i] - 1);
    return std::accumulate(r.begin(), r.end(), 0) / r.size();
}
```

*Answer:* (1) `std::accumulate(..., 0)` sums in `int`, truncating each partial sum: on {100, 110, 121} it returns 0 instead of 0.1 [verified]; use `0.0`. (2) `px.size() - 1` wraps to 18,446,744,073,709,551,615 on an empty vector, so the loop reads out of bounds (undefined); guard with `if (px.size() < 2)`. (3) Dividing by `r.size()` when `r` is empty divides by zero (an `int` sum by a `size_t` zero is undefined); return NaN or throw by contract. *Decision point:* the function "works" on long inputs whose mean exceeds 1 in magnitude only by accident; tests with small returns expose bug 1 at once.

**CM1, example 1 (difficulty 4, numeric).** On x86-64 Linux, give `sizeof` and member offsets for `struct A { char side; double px; int qty; };`, `struct B { double px; int qty; char side; };` and `struct C { char a; int b; char c; };`, and reorder `struct T { char side; int64_t ts; bool aggr; double px; int32_t qty; };` to its smallest size.

*Answer:* A: 24 (offsets 0, 8, 16); B: 16 (0, 8, 12); C: 12 (0, 4, 8); T as written: 40; reordered as `int64_t ts; double px; int32_t qty; char side; bool aggr;`: 24 [verified].
*Working:* each member starts at a multiple of its alignment and the size rounds up to the largest alignment (8). *Decision point:* in A, `px` must start at 8, wasting 7 bytes after `side`, and the struct pads 4 bytes at the end; sorting by decreasing alignment removes both.

**CM1, example 2 (difficulty 5, long-form diagnosis).** For each report, say what happened and how to fix it: (a) "AddressSanitizer: heap-use-after-free" on a read through `int& first = v[0];` after ten `push_back` calls; (b) "AddressSanitizer: stack-use-after-scope" inside a lambda stored in a `std::function`; (c) "runtime error: signed integer overflow: 1073741824 * 2 cannot be represented in type 'int'".

*Model answer:* (1) (a) `push_back` reallocated the vector's buffer and freed the old one; `first` still points into the freed block. (2) Fix (a): take the reference after the pushes, store an index instead, or `reserve` enough capacity first. (3) (b) the lambda captured a local by reference, and the local's scope ended before the stored lambda ran; fix by capturing by value (`[local]`) or by giving the data a longer owner. (4) (c) a loop doubled an `int` past its maximum; signed overflow is undefined and the optimiser may assume it never happens; fix with a wider type (`int64_t`), an explicit bound check before multiplying, or `unsigned` if wrap-around is intended. (5) In all three the program may print plausible values in a normal build, which is why sanitisers run in CI on every test.
*Rubric (10):* 2 for (a)'s cause; 2 for (a)'s fixes; 2 for (b); 2 for (c); 2 for the CI point.

**CM2, example 1 (difficulty 4, code).** Write `class Money` holding integer pence with `explicit` construction, `+`, `-` and a defaulted `<=>`.

*Answer:*

```cpp
#include <compare>
#include <cstdint>

class Money {
public:
    explicit Money(std::int64_t pence) : p_(pence) {}       // explicit: no silent Money from an int
    std::int64_t pence() const { return p_; }
    friend Money operator+(Money a, Money b) { return Money(a.p_ + b.p_); }
    friend Money operator-(Money a, Money b) { return Money(a.p_ - b.p_); }
    friend auto operator<=>(const Money&, const Money&) = default;   // also gives ==
private:
    std::int64_t p_;
};
```

*Checks:* `Money(150) + Money(275)` is 425 pence; `Money(150) < Money(275)`; `Money(275) - Money(150) == Money(125)`; a compile-fail test: `Money m = 5;` must not compile. *Decision point:* storing pounds in a `double` reintroduces 1.1 lesson 4's rounding.

**CM2, example 2 (difficulty 5, long-form).** A function opens a file, locks a mutex and allocates a buffer, then calls a pricer that may throw. Explain how RAII guarantees all three are released, in which order, and what goes wrong without it.

*Model answer:* (1) RAII ties each resource to an object whose destructor releases it: `std::ofstream`, `std::lock_guard<std::mutex>`, `std::vector` or `std::unique_ptr<double[]>`. (2) When the pricer throws, the stack unwinds and every fully constructed local is destroyed. (3) Destruction runs in reverse order of construction: the buffer is freed, then the mutex unlocked, then the file closed. (4) With manual `fclose`, `unlock` and `delete` at the end of the function, a throw skips all three: the file stays open, the mutex stays locked (the next caller deadlocks) and the buffer leaks. (5) Destructors must not throw during unwinding, or `std::terminate` is called, so release functions report errors another way.
*Rubric (10):* 2 for the RAII principle with the three types; 2 for unwinding; 2 for the order; 2 for the failure without RAII, including the deadlock; 2 for the destructor rule.

**CM3, example 1 (difficulty 4, code).** Write `class Buffer` owning `new double[n]` with correct copy, move, assignment and destruction, a `noexcept` move constructor, and copy-and-swap.

*Answer:*

```cpp
#include <algorithm>
#include <cstddef>
#include <utility>

class Buffer {
public:
    explicit Buffer(std::size_t n) : n_(n), d_(n ? new double[n]() : nullptr) {}
    ~Buffer() { delete[] d_; }
    Buffer(const Buffer& o) : n_(o.n_), d_(o.n_ ? new double[o.n_] : nullptr) {
        std::copy(o.d_, o.d_ + n_, d_);                                   // deep copy
    }
    Buffer(Buffer&& o) noexcept : n_(std::exchange(o.n_, 0)), d_(std::exchange(o.d_, nullptr)) {}
    Buffer& operator=(Buffer o) noexcept { swap(o); return *this; }      // by value: copy or move, then swap
    void swap(Buffer& o) noexcept { std::swap(n_, o.n_); std::swap(d_, o.d_); }
    std::size_t size() const { return n_; }
    double& operator[](std::size_t i) { return d_[i]; }
private:
    std::size_t n_;
    double* d_;
};
static_assert(std::is_nothrow_move_constructible_v<Buffer>);
```

*Checks:* a copy is independent after writing to it; a moved-from buffer has size 0 and the target holds the data; self-assignment keeps the data; AddressSanitizer reports nothing; the `static_assert` compiles [all verified]. *Decision point:* without `noexcept` on the move constructor, `std::vector<Buffer>` copies every buffer when it reallocates.

**CM3, example 2 (difficulty 5, predict).** `Loud` prints "copy" or "move" from its copy and move constructors (the move is `noexcept`). `WithDtor` holds a `Loud` and declares an empty destructor; `NoDtor` holds a `Loud` and declares nothing. What does each line print?

```cpp
WithDtor a; WithDtor b = std::move(a);              // (1)
NoDtor c;   NoDtor d = std::move(c);                // (2)
const Loud cl; Loud m = std::move(cl);              // (3)
std::vector<Loud> v; v.reserve(1); v.emplace_back(); v.emplace_back();   // (4)
```

*Answer:* (1) "copy"; (2) "move"; (3) "copy"; (4) "move" (one line, when the second `emplace_back` reallocates) [verified].
*Working:* (1) a user-declared destructor suppresses the implicit move constructor, so the copy constructor is used; (2) the implicit move moves the member; (3) `std::move` of a `const` object gives a `const&&`, which binds only to the copy constructor; (4) reallocation moves the existing element because the move is `noexcept`. *Decision point:* (1) is the bug that "adding a destructor for tidiness" introduces.

**CM4, example 1 (difficulty 4, code).** Write an abstract `Payoff` with `operator()(double s)` and a virtual `clone()`, and `Call`, `Put` and `Digital` payoffs, so that a book of payoffs can be stored and copied through base pointers.

*Answer:*

```cpp
#include <algorithm>
#include <memory>

struct Payoff {
    virtual ~Payoff() = default;                                  // deleting through Payoff* is safe
    virtual double operator()(double s) const = 0;
    virtual std::unique_ptr<Payoff> clone() const = 0;            // a virtual copy constructor
};
struct Call final : Payoff {
    double k;
    explicit Call(double k) : k(k) {}
    double operator()(double s) const override { return std::max(s - k, 0.0); }
    std::unique_ptr<Payoff> clone() const override { return std::make_unique<Call>(*this); }
};
struct Put final : Payoff {
    double k;
    explicit Put(double k) : k(k) {}
    double operator()(double s) const override { return std::max(k - s, 0.0); }
    std::unique_ptr<Payoff> clone() const override { return std::make_unique<Put>(*this); }
};
struct Digital final : Payoff {
    double k;
    explicit Digital(double k) : k(k) {}
    double operator()(double s) const override { return s > k ? 1.0 : 0.0; }
    std::unique_ptr<Payoff> clone() const override { return std::make_unique<Digital>(*this); }
};
```

*Checks:* a `std::vector<std::unique_ptr<Payoff>>` holding all three; `Call(100)(120) == 20`, `Put(100)(90) == 10`, `Digital(100)(101) == 1`; a cloned call evaluates the same; AddressSanitizer clean [verified]. *Decision point:* `std::vector<Payoff>` cannot hold them (abstract), and a `std::vector` of a concrete base would slice.

**CM4, example 2 (difficulty 5, long-form).** A pricer evaluates a payoff at each of the $N + 1$ terminal nodes of a binomial tree and inside a Monte Carlo loop of $10^7$ paths. Compare a virtual `Payoff` with a template parameter `template <class P> double price(const P& payoff, ...)`, and recommend one for a library used by a desk that adds new payoffs weekly from configuration files.

*Model answer:* (1) Virtual dispatch costs an indirect call per evaluation and usually blocks inlining; templates let the compiler inline the payoff into the loop. (2) In a loop of $10^7$ simple evaluations the indirect call can matter; in a tree of $10^4$ terminal nodes it does not. (3) Templates fix the payoff type at compile time: every payoff must be known when the library is built, and each instantiation adds code and compile time. (4) Configuration-driven payoffs are chosen at run time, so they need a factory returning `std::unique_ptr<Payoff>`. (5) Recommendation: a virtual interface at the boundary (factory, configuration, storage) and, if profiling shows the hot loop matters, a template kernel instantiated for the few common payoffs and dispatched once per pricing call, not once per path.
*Rubric (10):* 2 for the cost of each; 2 for when it matters, with numbers; 2 for compile-time against run-time choice; 2 for the factory; 2 for the measured hybrid recommendation.

**CL1, example 1 (difficulty 4, code).** Write `mean` over a `std::span` of any floating type, constrained with a concept, and show that calling it on integers fails to compile with a constraint message.

*Answer:*

```cpp
#include <concepts>
#include <span>
#include <stdexcept>

template <std::floating_point T>
T mean(std::span<const T> xs) {
    if (xs.empty()) throw std::invalid_argument("empty");
    T sum = 0;
    for (T x : xs) sum += x;
    return sum / static_cast<T>(xs.size());
}
```

*Checks:* `mean<double>` of {1.0, 2.0, 4.5} is 2.5; `float` works; a compile-fail test with `std::vector<int>` must report "constraints not satisfied" rather than an error inside the body [verified for the success cases; the failing message is recorded per compiler in CI]. *Decision point:* without the constraint, `int` input compiles and silently returns a truncated mean.

**CL1, example 2 (difficulty 5, compiles or not).** With `template <typename T> T mx(T a, T b);` defined in a header, which of these compile and link? (a) `mx(1, 2.0)`; (b) `mx<double>(1, 2.0)`; (c) `std::vector v{1, 2, 3};`; (d) `int a{3.7};`; (e) `twice<int>` declared in a header, defined in `twice.cpp`, called from `main.cpp`.

*Answer:* (a) no: deduction gives `int` and `double` for one `T` ("no matching function"); (b) yes; (c) yes: class template argument deduction gives `std::vector<int>`; (d) no: narrowing in braces; (e) compiles but fails to link: "undefined reference to `int twice<int>(int)'" [all verified]. *Decision point:* (e) is the case learners call a compile error; the compiler accepted it because the declaration was visible.

**CL2, example 1 (difficulty 4, code).** Keep an order book's price levels with `std::map`: bids highest first, asks lowest first; add and remove quantity, report the best bid and ask, and the first ask at or above a price.

*Answer:*

```cpp
#include <cmath>
#include <functional>
#include <map>

struct Levels {
    std::map<double, long long, std::greater<>> bids;     // begin() is the highest bid
    std::map<double, long long> asks;                     // begin() is the lowest ask
    void add_bid(double px, long long q) { bids[px] += q; }
    void add_ask(double px, long long q) { asks[px] += q; }
    void remove_bid(double px, long long q) {
        auto it = bids.find(px);                          // find, never operator[]: no accidental insert
        if (it == bids.end()) return;
        if ((it->second -= q) <= 0) bids.erase(it);
    }
    double best_bid() const { return bids.empty() ? NAN : bids.begin()->first; }
    double best_ask() const { return asks.empty() ? NAN : asks.begin()->first; }
    double ask_at_or_above(double px) const {
        auto it = asks.lower_bound(px);
        return it == asks.end() ? NAN : it->first;
    }
};
```

*Checks:* bids at 99.5 and 100.0, asks at 100.5 and 101.0 give best bid 100.0, best ask 100.5, and 101.0 at or above 100.75; removing the 100.0 level leaves 99.5 [verified]; prices are ticks in the real drill (integers), here doubles for brevity. *Decision point:* `if (bids[px] == 0)` as an existence test inserts an empty level.

**CL2, example 2 (difficulty 5, predict with sanitisers).** What happens in each case? (a) `int& first = v[0];` then ten `push_back`s, then read `first`; (b) `std::map<std::string, int> m; if (m["x"] == 0) {}` then `m.size()`; (c) `std::multiset<int> s{1, 2, 2, 2, 3}; s.erase(2);` then `s.size()`; (d) the same set with `s.erase(s.find(2))`.

*Answer:* (a) undefined: AddressSanitizer reports heap-use-after-free; (b) 1: the lookup inserted "x"; (c) 2; (d) 4 [all verified]. *Decision point:* (c) and (d) differ because `erase(value)` removes every equal element and `erase(iterator)` removes one; an order book that cancels one order of a price with `erase(price)` cancels all of them.

**CL3, example 1 (difficulty 4, code).** Sort a vector of `Trade { std::string sym; long long ts; double px; }` by symbol, then time, with a valid comparator.

*Answer:*

```cpp
#include <algorithm>
#include <string>
#include <tuple>
#include <vector>

struct Trade { std::string sym; long long ts; double px; };

void sort_trades(std::vector<Trade>& trades) {
    std::sort(trades.begin(), trades.end(), [](const Trade& a, const Trade& b) {
        return std::tie(a.sym, a.ts) < std::tie(b.sym, b.ts);    // lexicographic and strict
    });
}
```

*Checks:* {MSFT 3, AAPL 2, MSFT 1, AAPL 5} sorts to AAPL 2, AAPL 5, MSFT 1, MSFT 3 [verified]; 10,000 random trades under `-D_GLIBCXX_DEBUG`, which checks the comparator. *Decision point:* `a.sym <= b.sym` style comparators break strict weak ordering; lesson 58's crash is in the `wrong/` folder.

**CL3, example 2 (difficulty 5, code).** Port 1.8's `network_delay` to C++ with `std::priority_queue` as a min-heap.

*Answer:*

```cpp
#include <functional>
#include <queue>
#include <tuple>
#include <utility>
#include <vector>

int network_delay(const std::vector<std::tuple<int, int, int>>& times, int n, int k) {
    std::vector<std::vector<std::pair<int, int>>> g(n + 1);
    for (auto [u, v, w] : times) g[u].push_back({v, w});
    std::vector<long long> dist(n + 1, -1);                  // -1: not settled
    std::priority_queue<std::pair<long long, int>, std::vector<std::pair<long long, int>>, std::greater<>> pq;
    pq.push({0, k});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (dist[u] != -1) continue;                         // stale entry
        dist[u] = d;
        for (auto [v, w] : g[u]) if (dist[v] == -1) pq.push({d + w, v});
    }
    long long best = 0;
    for (int v = 1; v <= n; ++v) { if (dist[v] == -1) return -1; best = std::max(best, dist[v]); }
    return static_cast<int>(best);
}
```

*Checks:* the 1.8 cases (2 and $-1$) [verified]; $2 \times 10^5$ edges in under the time limit on the web runner. *Decision point:* the default `priority_queue` is a max-heap, which turns Dijkstra into a search that settles the farthest node first.

**CL4, example 1 (difficulty 4, code).** Write `McResult mc_call(S, K, r, sigma, T, n, seed, antithetic)` returning a Monte Carlo price and standard error for a European call; test against Black-Scholes within 4 standard errors.

*Answer:*

```cpp
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <random>

struct McResult { double price, se; };

McResult mc_call(double S, double K, double r, double sigma, double T, long n, std::uint64_t seed, bool antithetic) {
    std::mt19937_64 eng(seed);
    std::normal_distribution<double> z(0.0, 1.0);
    const double drift = (r - 0.5 * sigma * sigma) * T, vol = sigma * std::sqrt(T), disc = std::exp(-r * T);
    const long m = antithetic ? n / 2 : n;                   // the same number of normal draws either way
    double sum = 0.0, sum2 = 0.0;
    for (long i = 0; i < m; ++i) {
        const double e = z(eng);
        double p = disc * std::max(S * std::exp(drift + vol * e) - K, 0.0);
        if (antithetic) p = 0.5 * (p + disc * std::max(S * std::exp(drift - vol * e) - K, 0.0));
        sum += p; sum2 += p * p;
    }
    const double mean = sum / m, var = (sum2 - m * mean * mean) / (m - 1);
    return {mean, std::sqrt(var / m)};
}
```

*Checks:* with $10^6$ draws and seed 42 on libstdc++, the plain estimate was 10.4723 (standard error 0.0147) and the antithetic 10.4499 (0.0104) against 10.4506 [verified]; the tests assert only "within 4 standard errors" and "antithetic error is smaller", because `normal_distribution`'s output differs between standard libraries. *Decision point:* asserting the exact estimate makes the test fail on another compiler with a correct program.

**CL4, example 2 (difficulty 5, long-form).** Summing 0.1 ten million times gave 999,999.9998389754 naively and exactly 1,000,000.0000000000 with Kahan summation at `-O2`, but the Kahan result fell back to the naive value with `-ffast-math`. Explain all three results and the right fix.

*Model answer:* (1) 0.1 is not exactly representable, and each addition to a large running sum rounds away low-order bits, so errors accumulate to about $1.6 \times 10^{-4}$ here. (2) Kahan summation keeps the lost low-order part in a compensation variable and feeds it back into the next addition. (3) The compensation is computed as `(t - s) - y`, which is zero in exact algebra; `-ffast-math` allows the compiler to apply exact-algebra rewrites, so it deletes the compensation. (4) `-ffast-math` also lets the compiler assume no NaN or infinity (`std::isnan` returned false for a NaN) and reorder reductions, so it changes results silently. (5) Fix: do not use `-ffast-math` for numerical code; if one hot loop needs vectorised reductions, enable only the specific flags for that file, or restructure into pairwise sums, and test results against a `long double` or exact reference.
*Rubric (10):* 2 for the naive error; 2 for how Kahan works; 2 for why fast-math deletes it; 2 for the other fast-math effects; 2 for the fix.

**CP1, example 1 (difficulty 4, select).** A build prints these warnings. Which three are real bugs? (a) `-Wunused-parameter` on `void log(int level)`; (b) `-Wreorder` on a constructor initialising `lots_` before `qty_`, with `qty_` declared first and computed from `lots_`; (c) `-Wsign-compare` in `for (int i = 0; i < v.size() - 1; ++i)`; (d) `-Wpessimizing-move` on `return std::move(local);`; (e) `-Wparentheses` on `if (side = Side::Buy)`; (f) `-Wshadow` on a local named like a member.

*Answer:* (b), (c) and (e) [each reproduced in lessons 30, 8 and 12, verified].
*Working:* (b) reads an uninitialised member; (c) wraps round on an empty vector; (e) assigns instead of comparing. (d) is a missed optimisation, (a) is noise, (f) is a readability risk worth fixing but not a bug here. *Decision point:* "fix all warnings" is the policy; "which ones are bugs" is the skill this item tests.

**CP1, example 2 (difficulty 5, local task).** Create a CMake project with a `pricer` library, a `price` executable and a `tests` target run by `ctest`; build Debug and Release in separate folders; paste `cmake --version`, the Release configure line, and `ctest --output-on-failure` from Release.

*Answer (checked by paste-verify):* the paste shows CMake 3.20 or later, a configure command with `-DCMAKE_BUILD_TYPE=Release` and a build folder distinct from Debug's, and `100% tests passed, 0 tests failed`. A minimal `CMakeLists.txt` the hint ladder can show after submission: `cmake_minimum_required(VERSION 3.20)`, `project(pricer CXX)`, `set(CMAKE_CXX_STANDARD 20)`, `add_library(pricer src/pricer.cpp)`, `target_include_directories(pricer PUBLIC include)`, `add_executable(price src/main.cpp)`, `target_link_libraries(price PRIVATE pricer)`, `enable_testing()`, `add_executable(tests tests/test_pricer.cpp)`, `target_link_libraries(tests PRIVATE pricer)`, `add_test(NAME tests COMMAND tests)`. *Decision point:* one build folder reused for both types leaves stale objects and mixes optimisation levels.

**CP2, example 1 (difficulty 4, numeric).** A $1024 \times 1024$ matrix of doubles (8 MB, larger than the cache) is stored row-major. Using 64-byte cache lines and assuming no line survives between uses in the column-order pass, how many line loads does a full sum take in row order and in column order?

*Answer:* row order: $\frac{1024 \times 1024 \times 8}{64} = 131{,}072$ loads; column order: 1,048,576 loads (one per element), 8 times as many.
*Working:* row order uses all 8 doubles of each line consecutively; column order steps 8 KB between elements, so each element needs its own line. *Decision point:* the measured ratio for a $4096 \times 4096$ matrix was about 10 [measured], close to the model's 8 plus prefetching and translation effects; the model explains the direction, the measurement gives the size.

**CP2, example 2 (difficulty 5, long-form).** The C++ CRR pricer took 0.0015 s at $N = 2{,}000$ and 0.49 s at $N = 10{,}000$. Explain why the time grew 330 times for 25 times the work, how to confirm the cause, and how to fix it without `-ffast-math`.

*Model answer:* (1) Expected scaling is quadratic: $N(N + 1)/2$ updates, 25 times more at $N = 10{,}000$, about 0.04 s. (2) Far out-of-the-money nodes carry values that shrink towards zero through repeated discounting and averaging, and many reach the subnormal range below about $2.2 \times 10^{-308}$; on many x86 processors arithmetic on subnormals is far slower than on normal numbers. (3) Confirm by counting subnormal results with `std::fpclassify` (6.6% here [measured]) and by timing with flush-to-zero enabled (0.039 s [measured]). (4) Fix by clamping values below a threshold such as $10^{-300}$ to zero, or by skipping nodes whose value is already zero; the price changes by far less than $10^{-10}$. (5) `-ffast-math` would also flush subnormals but changes other results (CL4), so it is the wrong fix; report the clamp in the README.
*Rubric (10):* 2 for the expected scaling; 2 for what subnormals are and where they arise; 2 for confirming by measurement; 2 for the targeted fix and its effect on the price; 2 for rejecting fast-math with a reason.

**CP3, example 1 (difficulty 4, code).** Write `double price_crr(double S0, double K, double r, double sigma, double T, int n, Kind kind)` for European options, overwriting one vector, with input checks; the interface mirrors 1.7's `price_crr`.

*Answer:*

```cpp
#include <algorithm>
#include <cmath>
#include <stdexcept>
#include <vector>

enum class Kind { Call, Put };

double price_crr(double S0, double K, double r, double sigma, double T, int n, Kind kind) {
    if (n < 1 || sigma <= 0 || T <= 0) throw std::invalid_argument("bad input");
    const double dt = T / n, u = std::exp(sigma * std::sqrt(dt)), d = 1.0 / u;
    const double disc = std::exp(-r * dt), q = (std::exp(r * dt) - d) / (u - d);
    auto pay = [&](double s) { return kind == Kind::Call ? std::max(s - K, 0.0) : std::max(K - s, 0.0); };
    std::vector<double> v(n + 1);                            // one vector: O(n) memory
    for (int j = 0; j <= n; ++j) v[j] = pay(S0 * std::pow(u, j) * std::pow(d, n - j));
    for (int i = n - 1; i >= 0; --i)
        for (int j = 0; j <= i; ++j) v[j] = disc * (q * v[j + 1] + (1 - q) * v[j]);
    return v[0];
}
```

*Checks:* $S_0 = K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$: $n = 1$ gives 12.1623; at $n = 1{,}000$ the call is 10.448584 and the put 5.571527, with call minus put equal to $100 - 100e^{-0.05}$ within $10^{-10}$ (the error was $2.3 \times 10^{-12}$); at $n = 2{,}000$ the call is within $2 \times 10^{-3}$ of 10.450584 [all verified]; bad inputs throw. *Decision point:* $q$ uses $e^{r\Delta t}$, not $1 + r\Delta t$; the simple-interest version passes parity but fails convergence.

**CP3, example 2 (difficulty 5, code).** Extend the pricer to American options and test it.

*Answer:* the backward loop becomes `v[j] = american ? std::max(cont, pay(S0 * std::pow(u, j) * std::pow(d, i - j))) : cont;` with `cont = disc * (q * v[j + 1] + (1 - q) * v[j])`, the intrinsic value taken at the node's own price.
*Checks:* the American put at $n = 1{,}000$ is 6.089595 against the European 5.571527; the American call equals the European call exactly for a stock without dividends; with $r = 0$ the American put equals the European put [all verified]. *Decision point:* computing the intrinsic value as `pay(S0)` (the root price) passes the call test, because early exercise is never optimal for that call, and fails the put test.

**CP4, example 1 (difficulty 4, predict and fix).** Two `std::thread`s each run `for (int i = 0; i < 1000000; ++i) ++counter;` on a shared `long counter`. What can the program print, what does ThreadSanitizer say, and what are two fixes?

*Answer:* any value up to 2,000,000; two runs printed 1,156,720 and 1,247,797 [verified]; ThreadSanitizer reports "data race" with both threads' stacks [verified]. Fixes: `std::atomic<long> counter` (with `fetch_add`), or a `std::mutex` with `std::lock_guard` around the increment; faster still, give each thread its own local count and add them once at the end. *Decision point:* the race is undefined behaviour, so "any value up to 2,000,000" is the honest answer, not a guaranteed lower bound.

**CP4, example 2 (difficulty 5, code).** Write `mc_parallel(threads, paths_per_thread, seed)` pricing the standard call with one engine per thread, seeded `seed + t`, so that the result is identical on every run for a given thread count.

*Answer:*

```cpp
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <numeric>
#include <random>
#include <thread>
#include <vector>

double mc_parallel(int threads, long paths, std::uint64_t seed) {
    std::vector<double> partial(threads, 0.0);
    std::vector<std::thread> pool;
    for (int t = 0; t < threads; ++t)
        pool.emplace_back([&, t] {
            std::mt19937_64 eng(seed + static_cast<std::uint64_t>(t));    // private engine
            std::normal_distribution<double> z(0.0, 1.0);
            const double drift = 0.05 - 0.5 * 0.2 * 0.2, disc = std::exp(-0.05);
            double s = 0.0;
            for (long i = 0; i < paths; ++i) s += disc * std::max(100.0 * std::exp(drift + 0.2 * z(eng)) - 100.0, 0.0);
            partial[t] = s;                                                 // one slot per thread: no race
        });
    for (auto& th : pool) th.join();
    return std::accumulate(partial.begin(), partial.end(), 0.0) / (static_cast<double>(threads) * paths);
}
```

*Checks:* two runs with 4 threads and 250,000 paths each returned the same 10.454538; ThreadSanitizer reports nothing [verified]; the hidden test also checks the result is within 4 standard errors of 10.4506. *Decision point:* the partial sums sit in adjacent doubles, so frequent writes would false-share (lesson 88); writing once per thread at the end avoids it.

### 3.3 Item 2.4 Contests

| Level | Set | Items | Mix | Long-form (five points of 2 marks) | Contest problems | Generators |
|---|---|---|---|---|---|---|
| KC1 | `set.contestcraft.basics` | 5 | d3 ×2, d4 ×2, d5 ×1 | From four constraint sets to target complexities, with reasons | `drl.cp.new-highs`, `drl.cp.fast-sum`, `drl.cp.queue-sim`, `drl.cp.multi-test-reset` | `gen.cp.budget` |
| KC2 | `set.contestcraft.adhoc` | 5 | as above | A parity invariant proves a target unreachable | `drl.cp.no-adjacent-perm`, `drl.cp.mex-queries`, `drl.cp.dance-pairs`, `drl.cp.xor-subarrays` | `gen.cp.invariant-claim` |
| KC3 | `set.contestcraft.search` | 5 | as above | Why ternary search fails on plateaus, and how to search integers safely | `drl.cp.machines`, `drl.cp.pair-count`, `drl.cp.guess-number` (interactive), `drl.cp.unimodal-peak` | `gen.cp.predicate-bounds` |
| KC4 | `set.contestcraft.practice` | 5 | as above | An upsolve log for one unsolved contest problem | `drl.cp.hack-overflow`, `drl.cp.prime-sum`, `drl.cp.stress-script`, `drl.cp.leaderboard-gap` | `gen.cp.hack-target` |
| KM1 | `set.contestmath.primes` | 5 | as above | Euclid's algorithm: correctness and the step bound | `drl.cp.divisor-count-sum`, `drl.cp.spf-factorise`, `drl.cp.diophantine`, `drl.cp.coprime-count` | `gen.cp.gcd-steps` |
| KM2 | `set.contestmath.modular` | 5 | as above | Fermat inverses: why the modulus must be prime, and what to do otherwise | `drl.cp.ncr-queries`, `drl.cp.mod-pow`, `drl.cp.crt-general`, `drl.cp.mod-normalise` | `gen.cp.mod-predict` |
| KM3 | `set.contestmath.counting` | 5 | as above | The contribution count for subarray minimums, with ties | `drl.cp.sum-subarray-mins`, `drl.cp.divisible-by-any`, `drl.cp.bracket-count`, `drl.cp.fib-huge` | `gen.cp.inclusion-exclusion` |
| KM4 | `set.contestmath.games` | 5 | as above | The Sprague-Grundy theorem applied to a sum of three games | `drl.cp.expected-rolls`, `drl.cp.subtraction-game`, `drl.cp.nim-move`, `drl.cp.game-sum` | `gen.cp.grundy` |
| KM5 | `set.contestmath.geometry` | 5 | as above | Pick's theorem and why geometry stays in integers | `drl.cp.polygon-area`, `drl.cp.convex-hull`, `drl.cp.segment-intersect`, `drl.cp.lattice-points` | `gen.cp.orientation` |
| KS1 | `set.contestds.ranges` | 5 | as above | Lazy propagation: why pushing tags down keeps every node correct | `drl.cp.fenwick-inversions`, `drl.cp.range-add-sum`, `drl.cp.rmq-sparse`, `drl.cp.kth-in-multiset` | `gen.cp.range-ops` |
| KS2 | `set.contestds.trees` | 5 | as above | Rerooting: the $n - 2 \cdot \text{size}$ update, derived | `drl.cp.subtree-sums`, `drl.cp.lca-queries`, `drl.cp.sum-distances`, `drl.cp.kth-successor` | `gen.cp.tree-queries` |
| KS3 | `set.contestds.graphs` | 5 | as above | Max flow equals min cut, on the set's network | `drl.cp.scc-count`, `drl.cp.bridges`, `drl.cp.two-sat`, `drl.cp.max-flow` | `gen.cp.graph-small` |
| KD1 | `set.contestdp.dp` | 5 | as above | Digit DP: the state, the tight flag and leading zeros | `drl.cp.assignment-bitmask`, `drl.cp.nondecreasing-digits`, `drl.cp.stairs-k`, `drl.cp.stone-merge` | `gen.cp.digit-count` |
| KD2 | `set.contestdp.strings` | 5 | as above | Why hashing modulo $2^{64}$ can be attacked, and the defence | `drl.cp.kmp-count`, `drl.cp.z-borders`, `drl.cp.distinct-substrings`, `drl.cp.max-xor-pair` | `gen.cp.prefix-function` |
| KD3 | `set.contestdp.techniques` | 5 | as above | Mo's algorithm: deriving $(n + q)\sqrt{n}$ | `drl.cp.mitm-subsets`, `drl.cp.xor-basis`, `drl.cp.mo-distinct`, `drl.cp.sqrt-blocks` | `gen.cp.block-size` |

**Example problems, 2.4.** Statements are written in Codeforces style; the functions below are the cores, wrapped by KC1's fast-input template in the real drills. Every answer was recomputed by brute force (section 0.6).

**KC1, example 1 (difficulty 3, contest).** $t$ test cases ($t \le 10^4$); each gives $n$ and $n$ prices ($\sum n \le 2 \times 10^5$). Print, per case, the number of days whose price is strictly higher than every earlier price (the first day counts).

*Answer:*

```python
import sys

def main() -> None:
    data = sys.stdin.buffer.read().split()          # one read: fast for 2 * 10^5 numbers
    t, pos, out = int(data[0]), 1, []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        best, count = None, 0
        for tok in data[pos:pos + n]:
            x = int(tok)
            if best is None or x > best:
                best, count = x, count + 1
        pos += n
        out.append(str(count))
    sys.stdout.write("\n".join(out) + "\n")          # one write, not one print per case

main()
```

*Checks:* input `2 / 5 / 3 1 4 1 5 / 3 / 7 7 7` prints 3 and 1 [verified]; $10^4$ cases of size 20 and one case of size $2 \times 10^5$ within the scaled time limit. *Decision point:* `input()` per line and `print` per case pass the examples and fail on the largest file.

**KC1, example 2 (difficulty 5, long-form).** For each constraint set, give the slowest complexity that fits a 2-second limit in Python and in C++, and one algorithm idea: (a) $n \le 18$; (b) $n \le 400$; (c) $n \le 2 \times 10^5$; (d) $n \le 10^{18}$ with one query.

*Model answer:* (1) The budget: about $2 \times 10^7$ simple steps in Python and $2 \times 10^8$ to $10^9$ in C++. (2) (a) $2^{18} \approx 2.6 \times 10^5$: $O(2^n \cdot n)$ fits both; bitmask search or bitmask DP. (3) (b) $400^3 = 6.4 \times 10^7$: $O(n^3)$ fits C++ and is risky in Python; interval DP or Floyd-Warshall. (4) (c) $O(n \log n)$, about $3.5 \times 10^6$: sorting, binary search, Fenwick trees; $O(n^2) = 4 \times 10^{10}$ fits neither. (5) (d) $O(\log n)$ or $O(\sqrt[3]{n})$ at most: a formula, binary search on the answer, or matrix powers; even $O(\sqrt{n}) = 10^9$ is too slow in Python.
*Rubric (10):* 2 for the budgets; 2 each for (a) to (d), counted as one point for the complexity and one for a fitting idea.

**KC2, example 1 (difficulty 4, constructive).** Given $n \le 10^5$, print a permutation of $1, \dots, n$ in which no two neighbours differ by exactly 1, or $-1$ if none exists.

*Answer:* print $-1$ for $n = 2$ and $n = 3$; otherwise print the even numbers in increasing order, then the odd numbers (for $n = 4$: 2 4 1 3).
*Working:* neighbours inside each half differ by 2; at the junction the last even number, $2\lfloor n/2 \rfloor$, meets 1, a difference of at least 3 once $n \ge 4$. For $n = 2, 3$ a brute force over all orders finds none [verified for $n \le 7$]. *Checks:* a checker verifies any valid answer (any order is accepted). *Decision point:* odds first fails at $n = 4$: 1 3 2 4 has 3 next to 2.

**KC2, example 2 (difficulty 5, long-form proof).** The numbers 1 to 10 are on a board. A move replaces any two numbers $a$ and $b$ with $|a - b|$. After nine moves one number remains. Can it be 0?

*Model answer:* (1) Look for a quantity a move cannot change: the parity of the sum. (2) A move removes $a + b$ and adds $|a - b|$; $a + b$ and $|a - b|$ differ by $2\min(a, b)$, an even number. (3) So the sum's parity never changes. (4) The starting sum is $1 + \dots + 10 = 55$, odd, so the last number is odd. (5) Hence it cannot be 0; the same argument shows that 1 to 9 (sum 45) also leaves an odd number, while 1 to 8 (sum 36) can end at 0 (a construction is a homework extension).
*Rubric (10):* 2 for choosing an invariant; 2 for the difference $2\min(a, b)$; 2 for "parity is invariant"; 2 for the starting sum; 2 for the conclusion.

**KC3, example 1 (difficulty 4, contest).** Machines take $t_i$ seconds per item and work in parallel. Find the least time to make $M$ items ($k \le 2 \times 10^5$, $t_i \le 10^9$, $M \le 10^9$).

*Answer:*

```python
def least_time(t: list[int], m: int) -> int:
    lo, hi = 0, min(t) * m                     # the fastest machine alone finishes by hi
    while lo < hi:
        mid = (lo + hi) // 2
        made = 0
        for x in t:
            made += mid // x
            if made >= m:                      # stop early: in C++ this also prevents overflow
                break
        if made >= m:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

*Checks:* $t = [3, 2, 5]$, $M = 10$ gives 10 (at 9 seconds only 8 items) [verified]; one machine; $M = 10^9$ with $t_i = 10^9$ (answer $10^{18}$, which needs `long long` in C++). *Decision point:* the upper bound $\max(t) \cdot M$ also works but $\min(t) \cdot M$ is tighter and still provably sufficient.

**KC3, example 2 (difficulty 5, interactive).** A secret integer lies in $[1, 10^9]$. Ask "? x" and the judge replies "<" if the secret is below $x$ and ">=" otherwise; answer with "! s" within 30 queries.

*Answer:*

```python
import sys

def main() -> None:
    lo, hi = 1, 10**9                          # invariant: lo <= secret <= hi
    while lo < hi:
        mid = (lo + hi + 1) // 2               # round up, or lo = mid can stall
        print(f"? {mid}", flush=True)          # flush, or both sides wait for ever
        reply = sys.stdin.readline().strip()
        if reply == "-1":
            return                             # the judge reports an error: stop at once
        if reply == ">=":
            lo = mid
        else:
            hi = mid - 1
    print(f"! {lo}", flush=True)

main()
```

*Checks:* a simulated judge with secrets 1, 2, $10^9$, $10^9 - 1$, $5 \times 10^8$ and 30 random values: always correct, at most 30 queries [verified]. *Decision point:* `mid = (lo + hi) // 2` with `lo = mid` loops for ever once `hi = lo + 1`; the first draft of this reference had that bug and the simulated judge caught it.

**KC4, example 1 (difficulty 4, hack).** A C++ submission reads $n \le 2 \times 10^5$ values up to $10^9$ into `int a[]` and prints their sum, stored in an `int`. Give the smallest input that breaks it, and the fix.

*Answer:* `3 / 1000000000 1000000000 1000000000`: the true sum $3 \times 10^9$ exceeds 2,147,483,647, so signed overflow occurs (undefined; typically a negative number is printed). Two values of $10^9$ already reach $2 \times 10^9 \le$ 2,147,483,647, which fits, so three is the smallest count. Fix: `long long sum`. *Checks:* `counterexample-lab` (hack) accepts any input that makes the submission's output differ from the reference within the constraints. *Decision point:* the values fit in `int` individually, which is why the bug survives the examples.

**KC4, example 2 (difficulty 5, maths with code).** Find the sum of all primes below 2,000,000 in under a second in Python.

*Answer:* 142,913,828,922 [verified], with a byte-array sieve:

```python
from math import isqrt

def prime_sum(limit: int) -> int:
    sieve = bytearray([1]) * limit
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(limit - 1) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytearray(len(range(p * p, limit, p)))   # cross out from p*p in one slice
    return sum(i for i in range(limit) if sieve[i])
```

*Decision point:* trial division of every number up to 2,000,000 takes minutes; the sieve's slice assignment runs in C. Project Euler's own rule is not to publish answers beyond its first hundred problems [recalled]; this one is problem 10, inside that range.

**KM1, example 1 (difficulty 4, contest).** Compute $\sum_{i=1}^{N} d(i)$, the total number of divisors of all integers up to $N \le 10^{12}$.

*Answer:*

```python
def divisor_count_sum(n: int) -> int:
    total, i = 0, 1
    while i <= n:
        q = n // i
        j = n // q                     # every i' in [i, j] has the same quotient q
        total += q * (j - i + 1)
        i = j + 1
    return total
```

*Checks:* $N = 10^6$ gives 13,970,034, equal to $\sum_i \lfloor N/i \rfloor$ by brute force [verified]; $N = 1$ gives 1; $N = 10^{12}$ in about $2\sqrt{N} = 2 \times 10^6$ iterations. *Decision point:* swapping the order of summation, $\sum_{i \le N} d(i) = \sum_{d \le N} \lfloor N/d \rfloor$, is the leap; grouping equal quotients takes it from $O(N)$ to $O(\sqrt{N})$.

**KM1, example 2 (difficulty 5, long-form proof).** Prove that $\gcd(a, b) = \gcd(b, a \bmod b)$ for $b > 0$, and that Euclid's algorithm halves the larger argument at least every two steps, so it takes $O(\log \min(a, b))$ steps.

*Model answer:* (1) Write $a = qb + r$ with $r = a \bmod b$. (2) Any common divisor of $a$ and $b$ divides $r = a - qb$; any common divisor of $b$ and $r$ divides $a = qb + r$. (3) So the two pairs have the same common divisors and the same greatest one. (4) Bound: after two steps the pair $(a, b)$ becomes $(r, b \bmod r)$; if $b \le a/2$ then $r < b \le a/2$, and if $b > a/2$ then $r = a - b < a/2$; either way the first argument at least halves. (5) Hence at most about $2\log_2 a$ steps; $\gcd(1071, 462) = 21$ takes 3 [verified], and consecutive Fibonacci numbers are the worst case.
*Rubric (10):* 2 for the division identity; 2 for each direction of the common-divisor argument (one point each); 2 for equality of gcds; 2 for the two-step halving; 2 for the bound and the worst case.

**KM2, example 1 (difficulty 4, contest).** Answer $q \le 2 \times 10^5$ queries of $\binom{n}{k} \bmod (10^9 + 7)$ with $n \le 10^5$.

*Answer:*

```python
MOD = 10**9 + 7

def make_ncr(nmax: int):
    fact = [1] * (nmax + 1)
    for i in range(1, nmax + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * (nmax + 1)
    inv[nmax] = pow(fact[nmax], MOD - 2, MOD)        # one Fermat inverse
    for i in range(nmax, 0, -1):
        inv[i - 1] = inv[i] * i % MOD                # then walk down
    return lambda n, k: 0 if k < 0 or k > n else fact[n] * inv[k] % MOD * inv[n - k] % MOD
```

*Checks:* $\binom{10^5}{5 \times 10^4} \bmod (10^9 + 7) = 149{,}033{,}233$; $\binom{5}{2} = 10$; $k > n$ gives 0 [verified]. *Decision point:* one `pow` per query costs $q \log p$; the precomputed inverse factorials cost one `pow` in total.

**KM2, example 2 (difficulty 5, contest).** Combine $x \equiv r_1 \pmod{m_1}$ and $x \equiv r_2 \pmod{m_2}$ with moduli that need not be coprime; report $x \bmod \mathrm{lcm}(m_1, m_2)$ or "no solution".

*Answer:*

```python
from math import gcd

def crt(r1: int, m1: int, r2: int, m2: int):
    g = gcd(m1, m2)
    if (r2 - r1) % g:
        return None                                   # the residues disagree modulo g
    l = m1 // g * m2
    t = (r2 - r1) // g * pow(m1 // g, -1, m2 // g) % (m2 // g)
    return (r1 + m1 * t) % l, l
```

*Checks:* $(2, 6)$ and $(8, 10)$ give $x \equiv 8 \pmod{30}$; $(1, 6)$ and $(2, 4)$ have no solution (odd against even); $(2, 3)$ and $(3, 5)$ give $8 \pmod{15}$ [verified]. *Decision point:* the textbook CRT formula assumes coprime moduli and returns a wrong answer, not an error, when they are not.

**KM3, example 1 (difficulty 4, contest).** Compute the sum of the minimums of all subarrays, modulo $10^9 + 7$, for $n \le 3 \times 10^5$.

*Answer:*

```python
def sum_subarray_mins(a: list[int], mod: int = 10**9 + 7) -> int:
    n = len(a)
    left, right, stack = [0] * n, [0] * n, []
    for i in range(n):                         # span back to the previous strictly smaller value
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        left[i] = i - (stack[-1] if stack else -1)
        stack.append(i)
    stack = []
    for i in range(n - 1, -1, -1):             # span forward to the next smaller-or-equal value
        while stack and a[stack[-1]] > a[i]:
            stack.pop()
        right[i] = (stack[-1] if stack else n) - i
        stack.append(i)
    return sum(a[i] * left[i] * right[i] for i in range(n)) % mod
```

*Checks:* [3, 1, 2, 4] gives 17; [11, 81, 94, 43, 3] gives 444; [2, 2, 2] gives 12; 300 random arrays against brute force [verified]. *Decision point:* using `>=` on both sides counts a subarray with tied minimums twice; the asymmetric pair (strict on one side) counts each once.

**KM3, example 2 (difficulty 5, long-form proof).** Prove that each subarray is counted exactly once in the sum above, including subarrays where the minimum value occurs several times.

*Model answer:* (1) Assign each subarray to the rightmost position of its minimum value. (2) Position $i$ is that rightmost minimum of $[l, r]$ exactly when every value in $[l, i)$ is at least $a_i$ and every value in $(i, r]$ is strictly greater than $a_i$. (3) The left pass pops while the stack top is $\ge a_i$, so it stops at $p$, the previous index with $a_p < a_i$; the first condition holds exactly for $l$ in $(p, i]$, which is left$_i = i - p$ choices. (4) The right pass pops while the stack top is $> a_i$, so it stops at $s$, the next index with $a_s \le a_i$; the second condition holds exactly for $r$ in $[i, s)$, which is right$_i = s - i$ choices. (5) Every subarray has exactly one rightmost minimum, so it is counted by exactly one $i$, exactly once, even when the minimum value repeats: on [2, 2, 2] the spans are left = [1, 2, 3] and right = [1, 1, 1], six subarrays in all, and the sum is $2 \times 6 = 12$. Summing $a_i \times$ left$_i \times$ right$_i$ therefore gives the total.
*Rubric (10):* 2 for the rightmost-minimum assignment; 2 for the left condition tied to the `>=` pop; 2 for the right condition tied to the `>` pop; 2 for the product count; 2 for the tie argument with an example.

**KM4, example 1 (difficulty 4, contest).** A fair die is rolled until the running total is at least $n$ ($n \le 10^6$). Print the expected number of rolls modulo 998,244,353.

*Answer:* $E(t) = 1 + \frac16 \sum_{k=1}^{6} E(t - k)$ for $t > 0$ and $E(t) = 0$ for $t \le 0$, computed with $\frac16$ as its modular inverse. For $n = 10$ the exact value is $\frac{33{,}495{,}175}{10{,}077{,}696} \approx 3.3237$, printed as 104,766,026 [verified].

```python
P = 998244353

def expected_rolls(n: int) -> int:
    inv6 = pow(6, P - 2, P)
    e = [0] * (n + 6)                         # e[t + 5] holds E(t); E(t) = 0 for t <= 0
    for t in range(1, n + 1):
        e[t + 5] = (1 + inv6 * sum(e[t + 5 - k] for k in range(1, 7))) % P
    return e[n + 5]
```

*Decision point:* computing the decimal and converting at the end is impossible: the judge wants $p \cdot q^{-1} \bmod P$, and the fraction's numerator has no small form.

**KM4, example 2 (difficulty 5, long-form).** Three games are played side by side; a move is made in one of them: a pile of 5 where a move takes 1 to 3 stones, a pile of 7 where a move takes 1, 3 or 4, and a Nim heap of 3. The player who cannot move loses. Who wins, and with which moves?

*Model answer:* (1) The Sprague-Grundy theorem: a sum of impartial games is losing exactly when the XOR of the components' Grundy values is 0. (2) Take 1 to 3: Grundy value $n \bmod 4$, so the pile of 5 has value 1. (3) Take 1, 3 or 4: values 0, 1, 0, 1, 2, 3, 2, 0, ... so the pile of 7 has value 0 (losing alone). (4) The Nim heap of 3 has value 3; the XOR is $1 \oplus 0 \oplus 3 = 2 \ne 0$, so the first player wins. (5) Winning moves make the XOR 0: reduce the Nim heap from 3 to 1, or take 2 stones from the pile of 5 (to 3 stones, value 3) [verified].
*Rubric (10):* 2 for the theorem; 2 for each component's value (with the sequence for the second); 2 for the XOR and verdict; 2 for both winning moves.

**KM5, example 1 (difficulty 4, contest).** For the polygon with vertices (0, 0), (6, 0), (6, 4), (3, 7), (0, 4), find its area, its boundary lattice points and its interior lattice points.

*Answer:* area 33; boundary points 20; interior points 24 [verified].
*Working:* the shoelace sum gives twice the area, 66; boundary points per edge are $\gcd(|\Delta x|, |\Delta y|)$: $6 + 4 + 3 + 3 + 4 = 20$; Pick's theorem $A = I + \frac{B}{2} - 1$ gives $I = 33 - 10 + 1 = 24$. *Decision point:* halving before subtracting in Pick's formula introduces a fraction; work with $2A = 2I + B - 2$ in integers.

**KM5, example 2 (difficulty 5, code).** Write `convex_hull(points)` returning the hull's vertices counter-clockwise from the lowest-leftmost point, excluding collinear points, for $n \le 2 \times 10^5$ integer points.

*Answer:*

```python
def convex_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    def cross(o, a, b) -> int:                    # > 0: a left turn from o -> a -> b
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:   # <= drops collinear points
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]
```

*Checks:* the lesson's seven points give (0, 0), (4, 0), (3, 3), (2, 4), (0, 3); three collinear points give the two ends; duplicates; random point sets against a gift-wrapping brute force [verified]. *Decision point:* `< 0` in place of `<= 0` keeps collinear points, which this statement excludes.

**KS1, example 1 (difficulty 4, contest).** Count inversions of an array of $n \le 2 \times 10^5$ values up to $10^9$ with a Fenwick tree.

*Answer:* compress the values to ranks, scan left to right, and add the number of earlier values greater than the current one, `k - prefix(rank + 1)`, then insert the rank. [8, 4, 2, 1, 3, 7, 5, 6] gives 13; [1, 1, 1] gives 0 [verified, against merge sort's count]. *Decision point:* a Fenwick tree indexed by raw values needs $10^9$ cells; compression first is the step learners skip.

**KS1, example 2 (difficulty 5, code).** Support range add and range sum on $n, q \le 2 \times 10^5$ with a lazy segment tree; on [1, 2, 3, 4, 5], after adding 10 to positions 1 to 3 (half-open $[1, 4)$), report the sums of $[0, 5)$, $[2, 4)$ and $[0, 1)$.

*Answer:* 45, 27 and 1 [verified]. The tree stores each node's sum and a pending addition; `apply(node, v)` adds $v \cdot \text{length}$ to the sum and $v$ to the tag; before visiting children, `push` applies the node's tag to both children and clears it; updates and queries recurse only into partially covered nodes, $O(\log n)$ each. *Decision point:* skipping `push` in queries returns stale child sums once an update has stopped at a parent.

**KS2, example 1 (difficulty 4, contest).** For a tree with edges (0, 1), (0, 2), (2, 3), (2, 4), (2, 5), give each node's sum of distances to all others, in $O(n)$ by rerooting.

*Answer:* [8, 12, 6, 10, 10, 10] [verified by BFS from every node].
*Working:* one DFS from 0 gives subtree sizes and $\text{ans}(0) = 8$; moving the root from parent $p$ to child $c$ brings $\text{size}(c)$ nodes one step closer and $n - \text{size}(c)$ one step farther: $\text{ans}(c) = \text{ans}(p) + n - 2\,\text{size}(c)$. For node 2, with subtree size 4: $8 + 6 - 8 = 6$. *Decision point:* $n$ BFS runs are $O(n^2)$, $4 \times 10^{10}$ steps at $n = 2 \times 10^5$.

**KS2, example 2 (difficulty 5, code).** Answer LCA queries with binary lifting on a rooted tree given by `parent` (the root is its own parent) and `depth`.

*Answer:* build `up[0] = parent` and `up[k][v] = up[k-1][up[k-1][v]]` for $k < \lceil \log_2 n \rceil$; to answer $(u, v)$, lift the deeper node by the depth difference using its binary digits, return if equal, then for $k$ from high to low lift both while `up[k][u] != up[k][v]`, and return `parent[u]`. On parent [0, 0, 0, 1, 1, 2, 2, 3] with depths [0, 1, 1, 2, 2, 2, 2, 3]: $\mathrm{lca}(7, 4) = 1$, $\mathrm{lca}(7, 6) = 0$, $\mathrm{lca}(3, 7) = 3$, $\mathrm{lca}(5, 6) = 2$ [verified]. *Decision point:* lifting both nodes while they are unequal overshoots past the LCA; the loop must lift only while their ancestors differ.

**KS3, example 1 (difficulty 4, contest).** Find the maximum flow from node 0 to node 5 with capacities 0→1: 10, 0→2: 10, 1→2: 2, 1→3: 4, 1→4: 8, 2→4: 9, 3→5: 10, 4→3: 6, 4→5: 10.

*Answer:* 19 [verified with Edmonds-Karp].
*Working:* after Edmonds-Karp stops, the nodes still reachable from 0 in the residual graph are $S = \{0, 2\}$. The edges leaving $S$ are 0→1 (10) and 2→4 (9), both saturated; 1→2 points into $S$ and does not count. The cut capacity is $10 + 9 = 19$, equal to the flow, which proves 19 is the maximum. A tempting wrong cut, $\{0, 1, 2\}$ against the rest, has capacity $4 + 8 + 9 = 21$. *Decision point:* without reverse residual edges the greedy path choice can get stuck below 19.

**KS3, example 2 (difficulty 5, contest).** Meetings $a$, $b$, $c$ are each morning (true) or afternoon (false), subject to: $a \lor b$, $\lnot a \lor c$, $\lnot b \lor \lnot c$, $b \lor c$. Find an assignment with 2-SAT or report none.

*Answer:* satisfiable; both $(a, b, c) = (\text{T}, \text{F}, \text{T})$ and $(\text{F}, \text{T}, \text{F})$ work, and any satisfying assignment is accepted [verified by brute force over 8 assignments].
*Working:* each clause $x \lor y$ adds the implications $\lnot x \Rightarrow y$ and $\lnot y \Rightarrow x$; no variable shares a strongly connected component with its negation, so a solution exists; assigning each variable true when its component comes later in topological order than its negation's gives one. *Decision point:* trying all $2^n$ assignments is fine for 3 variables and hopeless for $10^5$.

**KD1, example 1 (difficulty 4, contest).** Count integers in $[1, N]$ whose digits never decrease from left to right, for $N \le 10^{18}$.

*Answer:* digit DP over (position, last digit, tight, started): 54 for $N = 100$; 9 for $N = 9$; 4,686,824 for $N = 10^{18}$ [verified, and equal to $\binom{27}{9} - 1$, the count of non-decreasing strings of up to 18 digits, since $10^{18}$ itself is not counted]. *Decision point:* without the "started" flag, leading zeros count as digits and every number "starts with 0", which wrongly allows any first digit.

**KD1, example 2 (difficulty 5, code).** Assign $n \le 15$ analysts to $n$ coverage areas at least total cost, with costs [[9, 2, 7], [6, 4, 3], [5, 8, 1]] as the sample.

*Answer:* 9 (2 + 6 + 1) [verified]. `dp[mask]` is the least cost of giving the first $\mathrm{popcount}(mask)$ analysts the areas in `mask`; `dp[mask | 1 << j] = min(dp[mask | 1 << j], dp[mask] + cost[i][j])` with $i = \mathrm{popcount}(mask)$; $O(2^n n)$, about $4.9 \times 10^5$ steps at $n = 15$. *Decision point:* a state of (analyst, mask) is redundant, because the mask's size already says which analyst is next.

**KD2, example 1 (difficulty 4, contest).** Count the occurrences of a pattern in a text, overlapping allowed, for lengths up to $10^6$.

*Answer:* the prefix function of `pattern + "\x00" + text`, counting positions whose value equals the pattern's length: "abab" in "abababca" occurs 2 times; "aa" in "aaaa" 3 times [verified]. *Decision point:* `text.count(pattern)` counts non-overlapping occurrences (2 for "aa" in "aaaa").

**KD2, example 2 (difficulty 5, contest).** Count the distinct substrings of a string of length $n \le 5{,}000$.

*Answer:* with the suffix array $sa$ and the longest common prefixes $lcp$ of neighbouring suffixes, the count is $\sum_k (n - sa_k - lcp_k)$: "banana" has suffix array [5, 3, 1, 0, 4, 2] and 15 distinct substrings [verified by a set of all substrings]. *Decision point:* putting every substring in a set costs $O(n^3)$ characters of memory at $n = 5{,}000$; double hashing of substrings per length is the $O(n^2)$ alternative.

**KD3, example 1 (difficulty 4, contest).** Count the subsets of $n \le 40$ integers summing to a target.

*Answer:*

```python
from collections import Counter

def count_subsets(a: list[int], target: int) -> int:
    half = len(a) // 2
    def sums(xs: list[int]) -> list[int]:
        out = [0]
        for x in xs:
            out += [s + x for s in out]            # doubles: 2^len(xs) sums
        return out
    left = Counter(sums(a[:half]))                 # about 10^6 entries for 20 items
    return sum(left[target - s] for s in sums(a[half:]))
```

*Checks:* [5, 3, −2, 8, 1, −6] with target 6 gives 5 [verified against all 64 subsets]; the empty subset counts when the target is 0. *Decision point:* $2^{40} \approx 1.1 \times 10^{12}$ subsets against two lists of $2^{20}$.

**KD3, example 2 (difficulty 5, contest).** For values [12, 10, 6, 3], find the rank of their XOR basis, the number of distinct subset XORs and the maximum subset XOR.

*Answer:* rank 3, 8 distinct XORs, maximum 15 [verified]. Insert each value from its top bit down, reducing by existing basis vectors; 6 reduces to 0 because $12 \oplus 10 = 6$; the distinct XORs number $2^{\text{rank}}$; the maximum is built greedily from the top basis vector down, keeping each XOR that raises the value. *Decision point:* "XOR the largest values" gives $12 \oplus 10 \oplus 6 \oplus 3 = 3$, far from 15.

### 3.4 Problem Gym, labs and projects

**Problem Gym** (`set.<course>.gym-<level>`, kind `practice`). 180 original problems: 150 at NeetCode 150's category counts (open item 2) plus 30 quant-flavoured problems (VWAP, rolling statistics, a matching engine step, arbitrage, reservoir sampling, Kendall distance, drawdown durations, as-of joins, order-book replay, settlement netting). Difficulty: 40 easy, 115 medium, 25 hard [our choice]. Each ships a statement, constraints, examples, a reference, a brute force (the stress oracle), hidden tests with edge cases, a `complexity` test where the pattern is the point, a NeetCode pointer for its video solution, and an editorial in `code-annotator` that opens after a pass. 78 problems are homework drills (section 3.1); the other 102 sit in Gym sets after each level, of which the hours plan budgets 90. Every solved problem counts once on the ledger.

**Held-out timed bank** (`pool.alg.timed`, `heldOut: true`). 40 mediums, never served anywhere else, in 12 pattern groups: hashing; two pointers and windows; prefix sums; binary search; stacks and queues; linked lists; heaps; trees; graph search; weighted graphs and union-find; backtracking; dynamic programming and greedy. A timed attempt draws a group the learner has finished, never the same problem twice; the window is the last 9 attempts (section 4.4).

**Order Book project** (`prj.alg.order-book`, 14 hours, after level SQ3; the learner's own repository under the 1.2 rules).

| Milestone | Work | Evidence | Hours |
|---|---|---|---|
| 1 Specification and tests | Price-time priority, limit, market and cancel orders, partial fills; a reference implementation as a sorted list; property tests (no crossed book after any event, quantities conserved) | `repo-check`, `paste-verify` of `pytest -q` | 3 |
| 2 A heap book | Two heaps with lazy cancellation (lesson 74), a dictionary from order id to order | `paste-verify` of tests | 3 |
| 3 A level book | A dictionary of price levels holding FIFO queues, plus heaps of active prices (or `sortedcontainers`), $O(\log L)$ per event | `paste-verify` of tests | 3 |
| 4 Benchmark | $10^6$ seeded events through all three books at growing sizes; log-log exponents; a profile of the hot path | `paste-verify` of benchmark output | 3 |
| 5 Results note | What each design costs, where each fails, what a C++ version would change (1.9) | `results-note` at 7 of 10 | 2 |

**C++ Lab** (`set.cpppricing.lab`, kind `practice`, 12 drills at about 1 hour, after lesson 62): two-sum with `unordered_map`; sliding window maximum with `deque`; merge intervals with `sort`; LRU with `list` and `unordered_map`; $k$-way merge with `priority_queue`; top-$k$ frequent; islands by BFS; Dijkstra; union-find; LIS with `lower_bound`; edit distance; coin change. Each reuses a Gym problem's hidden tests through a C++ harness; they do not add to the ledger.

**Monte Carlo pricer project** (`prj.cpp.mc-pricer`, 12 hours, after level CL4).

| Milestone | Work | Evidence | Hours |
|---|---|---|---|
| 1 Paths and payoffs | GBM terminal prices; the payoff hierarchy of lesson 43; European call and put with standard errors | doctest summary pasted | 3 |
| 2 Variance reduction | Antithetic draws; a control variate using the terminal price, whose discounted mean is $S_0$; the standard error against the plain estimator | doctest summary; a table of errors | 3 |
| 3 Threads | Per-thread engines with fixed seeds (lesson 87); identical results across runs; ThreadSanitizer clean | pasted output | 3 |
| 4 Benchmark and note | Paths per second against a NumPy version; a results note on accuracy against time | `results-note` at 7 of 10 | 3 |

---

## 4. Topic exam blueprints and exit tests

Both topic papers use kind `topic` (`assessment.md` 3.1): one clock, 70% to pass, difficulty mix by marks 20/50/20/10 at levels 2/3/4/5, long-form at most 30% of marks, Bertie `away` from Start to submission, a 3-day resit with a remediation set (`assessment.md` 3.8), test-out allowed before the lessons (7.3). A paper's rules screen shows "56 of 80 to pass". 2.4 has no topic paper (`assessment.md` 2.8); its Arena rounds are in section 4.3.

### 4.1 Item 1.8: `exm.algorithms`

| Property | Value |
|---|---|
| Kind | `topic` |
| When | Unlocks after level DP7's homework is submitted, or at any time as a test-out or diagnostic sitting |
| Duration | 90 minutes, one clock, the 15-minute pause budget (`assessment.md` 3.4). Summed item estimates 62.5 minutes; 90 is 1.44 times that |
| Items | 22 items, 80 marks; items 1 to 20 short (3 or 4 marks), item 21 a long-form proof (10), item 22 a code item (8) |
| Runtime | Python standard library only (`needs: []`), so the paper runs on both targets; Python is loaded and warmed before the clock starts (`assessment.md` 3.3) |
| Calculator | The in-app basic calculator, for ratios and logarithms in items 1 to 4 |
| Aids | None. Item 22's statement lists the allowed imports (`collections`, `heapq`, `bisect`, `itertools`, `functools`, `math`) |
| Difficulty by marks | d2 16, d3 40, d4 16, d5 8 (20/50/20/10) |
| Long-form | 10 marks, 12.5% |
| Pass | 56 of 80 (70%) |
| Forms | 3 forms of equal marks; 56 marks (70%) come from generator slots, so 3 forms meet `assessment.md` 3.2 rule 3 |
| Exit role | Closes 1.8 with `1.8.exit` (section 4.4). The paper is not an instrument of `1.8.exit`, because the curriculum's exit line names only the ledger and the timed medium; the topic closes on both (`assessment.md` 2.8) |

| Q | Levels | What it tests | Format | Difficulty, marks | Min | Slot |
|---|---|---|---|---|---|---|
| 1 | AC1 | Exact count of the innermost line of a generated nest of up to three loops (dependent, halving, harmonic or pointer), as a formula and as a value at a stated $n$ | X, N | d2, 3 | 1.5 | `gen.alg.loop-count` |
| 2 | AC1 | From a doubling table of operation counts, name the growth law and predict the count at $4n$ | C, N | d2, 3 | 1.5 | `gen.alg.doubling` |
| 3 | AC1, SQ2 | Amortised cost: element copies made by a doubling dynamic array, or element transfers of a two-stack queue, over a generated sequence of operations | N | d3, 3 | 2 | `gen.alg.amortised` |
| 4 | AC2 | Solve a generated divide-and-conquer recurrence: a master-theorem case, or a recursion-tree sum when no case applies | X | d3, 3 | 2 | `gen.alg.recurrence` |
| 5 | AC3 | Reach the array after one Lomuto partition or one bottom-up merge pass on a generated array | G (`sort-lab`, `moveMatchesAlgorithm`) | d2, 3 | 1.5 | `gen.alg.sort-step` |
| 6 | AC4 | (a) after quickselect's first partition, the side that recurses and the rank sought there; (b) whether a two-key order needs a stable sort | N, C | d3, 3 | 2 | `gen.alg.select` |
| 7 | AH1 | Linear probing: the table and the probe count of a final lookup after generated inserts and one deletion with a tombstone | R, N | d3, 3 | 2 | `gen.alg.probing` |
| 8 | AH2 | Order the lines of a two-pointer solution (a pair sum on sorted prices, or an in-place partition) | O | d2, 3 | 1.5 | `pool.alg.exam-parsons` (12) |
| 9 | AH3 | The monotonic deque's contents after each step of a sliding-window maximum over generated prices | G (`stack-queue-lab`, deque) | d3, 3 | 2 | `gen.alg.deque` |
| 10 | AH4, AH6 | (a) answer two range-sum queries from a prefix array, or apply a difference array; (b) the total length of a union of generated intervals | N, N | d3, 3 | 2 | `gen.alg.prefix-intervals` |
| 11 | AH5 | Fill the three blanks of a binary search on the answer so that it terminates and returns the least feasible value on every input; CI ran each accepted fill against the tests | K (`code-blanks`) | d3, 3 | 2.5 | `pool.alg.exam-blanks` (10) |
| 12 | SQ1, SQ2 | (a) predict a monotonic stack's next-greater output; (b) predict the list printed by a reversal with one classic pointer bug | T, T | d2, 4 | 1.5 | `gen.alg.stack-list` |
| 13 | SQ3, SQ4 | (a) the heap array after generated pushes and pops; (b) a reservoir or running-median state after a short stream | G (`heap-lab`, exact array), N | d3, 3 | 2 | `gen.alg.heap-ops` |
| 14 | TG1, TG2 | (a) one traversal order of a generated tree; (b) the BST after deleting a node with two children | O, G (`tree-lab`) | d3, 3 | 2 | `gen.alg.tree` |
| 15 | TG3 | BFS distances from a source, or any valid topological order of a generated DAG (`isTopoOrder` accepts every valid order) | N, O | d3, 3 | 2 | `gen.alg.graph` |
| 16 | TG4 | Dijkstra on a graph with one negative edge: the distance it reports, the true distance, and the algorithm that gives the true one | N, N, C | d4, 3 | 2.5 | `gen.alg.neg-edge` |
| 17 | TG5 | Union-find with union by rank and path compression (parent array after operations), or Kruskal's tree weight, or the arbitrage cycle from log rates | N or R | d4, 3 | 2.5 | `gen.alg.dsu-mst` |
| 18 | DP1, DP2 | (a) the number of leaves of a pruned backtracking search; (b) a 1D DP value | N, N | d3, 3 | 2 | `gen.alg.dp1d` |
| 19 | DP3, DP4 | (a) fill the marked cells of an LCS, edit-distance or knapsack table; (b) select the cells of one optimal reconstruction | N, R (`dp-table`) | d3, 4 | 2.5 | `gen.alg.dp2d` |
| 20 | DP5 or DP6 | A counterexample to a greedy rule (graded by behaviour: greedy and the reference optimum disagree on it), or a bit-manipulation value | E or N | d3, 3 | 2 | `gen.alg.greedy-cx`, `gen.alg.bits` |
| 21 | AC2, TG3, TG4 or DP5 | A correctness proof by invariant, induction or exchange | Long-form, 10-point rubric | d4, 10 | 8 | `pool.alg.exam-proofs` (12, none used in homework) |
| 22 | DP7 and any pattern | An unseen medium in Python with hidden tests and a complexity test | K | d5, 8 | 15 | `pool.alg.exam-mediums` (16, disjoint from `pool.alg.timed`) |

**Totals.** 80 marks. d2: $3 + 3 + 3 + 3 + 4 = 16$ (Q1, 2, 5, 8, 12). d3: $12 \times 3 + 4 = 40$ (Q3, 4, 6, 7, 9, 10, 11, 13, 14, 15, 18, 19, 20, with Q19 at 4). d4: $3 + 3 + 10 = 16$ (Q16, 17, 21). d5: 8 (Q22). Generator slots: Q1 to Q7, Q9, Q10 and Q12 to Q20, 56 marks.

**Format mix by marks** (form A, where Q15 asks for distances, Q17 for a parent array and Q20 for a counterexample): numeric and expression 31; widget states, selections and orders (G, R, O) 18; code (K) 11; prediction (T) 4; choice parts (C) 3; behaviour (E) 3; long-form 10. Choice carries under 4% of marks, so a candidate who can recognise an algorithm but not run it does not pass.

**Coverage.** Every form tests 25 of the 26 levels (one of DP5 and DP6 rotates through Q20), above `assessment.md` 3.2's 80% rule. Every DS outcome except DS-O11 (bits, on alternate forms), DS-O12 (homework DP7) and DS-O14 (the ledger) appears on every form.

**Code marking (Q22).** 10 hidden tests: 6 functional (including empty, single-element and duplicate inputs), 2 at full size inside the time limit, 2 from the complexity test (a size ladder of $10^4$, $4 \times 10^4$, $1.6 \times 10^5$ whose time ratio must fit the intended class, `widgets-programming.md` 2.2.1). Marks $\lfloor 8p/10 \rfloor$ (`assessment.md` 3.5). An $O(n^2)$ answer passes the 6 functional tests and earns 4 of 8.

**Three slots worked in full.**

*Q16 (d4).* Directed edges S→A (2), S→B (5), B→A (−4), A→C (1). (a) What distance to C does Dijkstra report if it never updates a node after removing it from the queue? (b) What is the true shortest distance? (c) Which algorithm returns (b)?
Answer: (a) 3; (b) 2, along S→B→A→C; (c) Bellman-Ford [verified: both run]. Dijkstra removes A at distance 2 before B is processed, finalises C at 3, and the later relaxation through B→A (giving 1) arrives too late. Distractors for (c): "Dijkstra with a re-check at the end" (feedback: a single re-check finds the error but does not repair distances already propagated); "BFS" (feedback: BFS counts edges, not weights). Marks 1 + 1 + 1.

*Q21 (d4, one of the 12 proofs).* Prove that Dijkstra's algorithm returns the shortest distance to every reachable node when every edge weight is non-negative.
Model answer: (1) Invariant: when a node $u$ is removed from the queue, its label $d(u)$ equals the true distance $\delta(u)$; labels are never below true distances, because every label is the length of some path. (2) Suppose $u$ is the first node removed with $d(u) > \delta(u)$. Take a shortest path from $s$ to $u$ and let $y$ be its first node not yet removed, with predecessor $x$ removed. (3) $x$ was removed correctly, so $d(x) = \delta(x)$, and relaxing edge $x \to y$ set $d(y) \le \delta(x) + w(x, y) = \delta(y)$. (4) Weights are non-negative, so $\delta(y) \le \delta(u)$, giving $d(y) \le \delta(u) < d(u)$. (5) Then the queue would have removed $y$ before $u$, a contradiction; so every removed label is correct, and every reachable node is removed.
Rubric (10): 2 for the invariant and the upper-bound property (line 1); 2 for choosing the first wrong node and the first unremoved node on its shortest path (line 2); 2 for the relaxation step (line 3); 2 for using non-negativity, named (line 4); 2 for the contradiction and reachability (line 5). A proof that never uses non-negativity cannot score more than 6, because the claim is false without it (Q16 is the counterexample).

*Q22 (d5, one of the 16 mediums).* "Calm stretches." Given daily closes (up to $2 \times 10^5$ integers) and a limit $L \ge 0$, return the length of the longest run of consecutive days whose highest and lowest close differ by at most $L$ (0 for no days).
Reference: a sliding window with two monotonic deques (one for the maximum, one for the minimum), shrinking from the left while the spread exceeds $L$, $O(n)$. Checks: `[101, 103, 102, 106, 104, 105, 103, 99]` with $L = 3$ gives 4 (the run 106, 104, 105, 103); `[]` gives 0; `[5, 5, 5]` with $L = 0$ gives 3; 3,000 random small cases agree with a brute force; $n = 2 \times 10^5$ runs in 0.09 s in CPython [verified, measured]. Known-wrong solutions in CI: recomputing `max` and `min` of the window (passes the functional tests, fails the complexity test); a deque that pops on strict inequality only for the maximum (passes most tests, fails one with tied closes, which is test 5); shrinking by one step without re-reading both deque fronts (fails test 4).

### 4.2 Item 1.9: `exm.cpp`

| Property | Value |
|---|---|
| Kind | `topic` |
| When | Unlocks after level CP4's homework is submitted; test-out and diagnostic sittings allowed |
| Duration | 90 minutes, one clock. Summed item estimates 57.5 minutes; 90 is 1.57 times that |
| Items | 22 items, 80 marks: 20 short items (3 or 4 marks), item 21 a long-form design review (10), item 22 a long-form performance report (8) |
| Runtime | **Compiler-free** (decision 13): every snippet, output, diagnostic and sanitiser report on the paper was produced in CI on GCC and Clang and ships as data; code-blanks items accept only fills that CI compiled and tested. The paper runs on both targets |
| Calculator | The in-app basic calculator (Q9, Q17, Q19) |
| Aids | A one-page card of the fundamental type sizes and alignments on the reference platform (x86-64 Linux, LP64), so layout items test reasoning, not memory of a table |
| Difficulty by marks | d2 16, d3 40, d4 16, d5 8 |
| Long-form | 18 marks, 22.5% |
| Pass | 56 of 80 |
| Forms | **6 forms**: generated C++ items need a CI build per variant, so generator slots carry 26 marks (32.5%), and `assessment.md` 3.2 rule 3 then asks for at least 5 forms. Rejected: 3 forms with half the marks generated. Only some C++ families vary without changing what they teach (layouts, integer expressions, overload sets, constructor sequences, summation, cache models), and they carry 26 marks; sanitiser reports, multi-file build errors and design reviews are authored, and each generated variant is one more compiled and recorded build in CI |
| Exit role | Closes 1.9 with `1.9.exit`; on the Trader and Researcher tracks the paper still closes the topic's lessons in Stage 1 and the exit moves to Stage 2 (section 4.5) |

| Q | Levels | What it tests | Format | Difficulty, marks | Min | Slot |
|---|---|---|---|---|---|---|
| 1 | CB1 | For three recorded diagnostics, the stage that produced each: preprocessor, compiler, linker or run time | S | d2, 3 | 1.5 | `gen.cpp.stage-of-error` |
| 2 | CB1, CB3 | The first error of a recorded multi-file build (undefined reference, multiple definition, missing include or declaration) and the fix | C, E | d3, 3 | 2 | `pool.cpp.exam-build` (10) |
| 3 | CB2 | Predict the output of integer expressions: division and remainder of negatives, unsigned wrap-around, promotions, signed against unsigned comparison | T | d2, 3 | 1.5 | `gen.cpp.int-arith` |
| 4 | CB2, CM1 | Select every line with undefined behaviour (signed overflow, out-of-bounds index, uninitialised read, shift by the width or more) and name the flag or sanitiser that reports it | M | d3, 3 | 2 | `pool.cpp.exam-ub` (12) |
| 5 | CB3, CL1 | Which overload or template is called, or "does not compile: ambiguous", for four recorded calls | T | d3, 3 | 2 | `gen.cpp.overload` |
| 6 | CM1 | Which of four functions returns a dangling reference or pointer, matched to the report AddressSanitizer gives for it | S | d3, 3 | 2 | `pool.cpp.exam-lifetime` (10) |
| 7 | CM1 | Read an AddressSanitizer report (heap-use-after-free, heap-buffer-overflow, stack-use-after-return) and select the faulty line | R (`code-annotator`) | d3, 3 | 2 | `pool.cpp.exam-asan` (10) |
| 8 | CM2 | Complete a class that keeps an invariant: constructor validation, `const` member functions, one operator | K (`code-blanks`) | d3, 3 | 2 | `pool.cpp.exam-class` (8) |
| 9 | CM2 | `sizeof` a generated struct, and its size after reordering members to remove padding | N, N | d2, 3 | 1.5 | `gen.cpp.layout` |
| 10 | CM3 | The sequence of constructor calls (constructor, copy, move) printed by a recorded program | T | d3, 3 | 2 | `gen.cpp.special-members` |
| 11 | CM3 | For four ownership situations, choose a value, `unique_ptr`, `shared_ptr`, a reference or a non-owning raw pointer | S | d2, 3 | 1.5 | `pool.cpp.exam-ownership` (10) |
| 12 | CM4 | Virtual dispatch and slicing: predict the output | T | d3, 3 | 2 | `pool.cpp.exam-virtual` (10) |
| 13 | CL2 | Match five workloads to `vector`, `deque`, `list`, `map` or `unordered_map`, with the operation cost that decides | S | d2, 4 | 1.5 | `gen.cpp.container-choice` |
| 14 | CB4, CL2 | Iterator and reference invalidation: select the line where an iterator or reference dies, and the fix | R, C | d3, 3 | 2 | `pool.cpp.exam-invalidation` (10) |
| 15 | CL3 | Which comparators are strict weak orders, and what `<=` does inside `std::sort` (recorded AddressSanitizer report) | M | d3, 3 | 2 | `pool.cpp.exam-comparator` (8) |
| 16 | CL4 | Reproducible randomness: seeding, which outputs are portable across standard libraries (engines are, distributions are not), engines per thread | C | d3, 3 | 2 | `pool.cpp.exam-random` (8) |
| 17 | CL4, CP2 | Naive, Kahan and `std::reduce` sums of a generated sequence, and what `-ffast-math` changes | N, C | d3, 4 | 2 | `gen.cpp.float-sum` |
| 18 | CP1, CP2 | Select every flaw in a benchmark (Debug build, one run, unused result, timer around input and output, sanitisers on) | M | d3, 3 | 2 | `pool.cpp.exam-bench` (8) |
| 19 | CP2 | From a counted model, predict a time ratio (row against column traversal, vector against list) or the cause of a super-linear slowdown | N, C | d4, 3 | 3 | `gen.cpp.cache-model` |
| 20 | CP4 | The possible outputs of a two-thread program, and which fix makes a check-then-act correct | M, C | d4, 3 | 3 | `pool.cpp.exam-threads` (8) |
| 21 | CM3, CM4 | Review and redesign an ownership and interface snippet from a pricing library | Long-form, 10-point rubric | d4, 10 | 10 | `pool.cpp.exam-design` (8) |
| 22 | CP2, CP3 | From a timing report of C++ and Python pricers, write the honest claim and what is missing | Long-form, 10 points scaled to 8 | d5, 8 | 8 | `pool.cpp.exam-report` (6) |

**Totals.** 80 marks. d2: $3 + 3 + 3 + 3 + 4 = 16$ (Q1, 3, 9, 11, 13). d3: $12 \times 3 + 4 = 40$ (Q2, 4, 5, 6, 7, 8, 10, 12, 14, 15, 16, 17, 18, with Q17 at 4). d4: $3 + 3 + 10 = 16$ (Q19, 20, 21). d5: 8 (Q22). Generator slots Q1, 3, 5, 9, 10, 13, 17 and 19: 26 marks.

**Coverage.** Every form tests all 16 levels. Every CP outcome except CP-O12 (the exit) appears on every form. Pools hold at least 8 items so that 6 forms and six resits stay fresh (`assessment.md` 3.2 rule 4 applied to pools).

**Five slots worked in full** [all verified on GCC 13.3 and Clang 18.1 at `-O2`].

*Q3 (d2).* What does `std::cout << (-7 / 2) << ' ' << (-7 % 2) << ' ' << (7u > -1);` print?
Answer: `-3 -1 0`. Division truncates towards zero, the remainder takes the dividend's sign, and `-1` converts to `unsigned` 4,294,967,295, so `7u > -1` is false. GCC warns with `-Wsign-compare` under `-Wall -Wextra`; Clang 18 printed no warning for this line with the same flags [verified], which is why the lesson teaches the conversion, not the warning. Distractors: `-4 1 1` (feedback: that is Python's floor division and modulo); `-3 1 1` (feedback: the remainder keeps the dividend's sign in C++); `-3 -1 1` (feedback: the comparison happens in `unsigned`).

*Q9 (d2).* `struct Tick { char side; double price; int qty; char venue; };` What is `sizeof(Tick)`, and what is the smallest size after reordering the members?
Answer: 24 and 16 [verified]. `side` takes byte 0 and 7 bytes of padding align `price` to 8; `qty` takes bytes 16 to 19, `venue` byte 20, and 3 bytes of tail padding round the size to a multiple of 8. Ordered `double, int, char, char`, the members fill 14 bytes and the size rounds to 16. Hint ladder: (1) "Where must `price` start?" (2) "The struct's size is a multiple of its strictest alignment." (3) "Largest members first."

*Q10 (d3).* A type prints `ctor`, `copy` or `move` from its constructors (the move constructor is `noexcept`). What does this print?

```cpp
Noisy a;                          // line 1
Noisy b = a;                      // line 2
Noisy c = std::move(a);           // line 3
std::vector<Noisy> v; v.reserve(2);
v.push_back(b);                   // line 5
v.push_back(Noisy{});             // line 6
Noisy m = Noisy{};                // line 7
```

Answer: `ctor`, `copy`, `move`, `copy`, `ctor`, `move`, `ctor` [verified on both compilers]. Line 6 constructs a temporary and moves it in; line 7 is guaranteed copy elision since C++17, so only `ctor`. `reserve(2)` removes the reallocation that would otherwise add a move of the first element. Distractor `... copy, ctor, copy, ctor` (feedback: a temporary binds to `push_back(T&&)`, which moves).

*Q21 (d4, one of 8).* Review this class and redesign it.

```cpp
struct Payoff { virtual double operator()(double s) const = 0; ~Payoff() {} };
class Pricer {
public:
    explicit Pricer(Payoff* p) : payoff_(p) {}
    ~Pricer() { delete payoff_; }
    double intrinsic(double s) const { return (*payoff_)(s); }
private:
    Payoff* payoff_;
};
```

Model answer: (1) `Payoff`'s destructor is not virtual, so `delete payoff_` on a derived object is undefined behaviour; GCC warns `-Wdelete-non-virtual-dtor`, Clang `-Wdelete-abstract-non-virtual-dtor`, and AddressSanitizer reports `new-delete-type-mismatch` [verified]. (2) `Pricer` owns a raw pointer and declares a destructor but no copy operations, so `Pricer b = a;` copies the pointer and both destructors delete it; with the destructor made virtual, AddressSanitizer reports `heap-use-after-free` inside `Pricer::~Pricer`, because the second delete reads the freed object's virtual table [verified, GCC]. (3) A null pointer is accepted and dereferenced later. (4) Redesign: `virtual ~Payoff() = default;`; hold `std::unique_ptr<const Payoff>` taken by value in the constructor (ownership is visible at the call site, `std::make_unique<Call>(100)`), validate it is not null, and either delete copying (move-only `Pricer`) or add `virtual std::unique_ptr<Payoff> clone() const` for deep copies; or, if payoffs are immutable and shared, `std::shared_ptr<const Payoff>`. (5) The rule of zero: with a smart pointer member, `Pricer` declares no destructor and no copy or move operations of its own.
Rubric (10): 2 for the non-virtual destructor and its consequence; 2 for the double deletion through the implicit copy; 1 for the null check; 3 for a redesign with stated ownership (unique and move-only or cloned, or shared and immutable, with the reason); 2 for the rule of zero. A redesign that adds a hand-written copy constructor to the raw pointer scores at most 1 of the 3 redesign points.

*Q22 (d5, one of 6).* Medians of 7 runs for a CRR call ($S = K = 100$, $T = 1$, $r = 5\%$, $\sigma = 20\%$), one machine:

| $N$ | Pure Python loops | NumPy | C++ `-O2` |
|---|---|---|---|
| 1,000 | 0.0437 s | 0.0033 s | 0.00073 s |
| 2,000 | 0.177 s | 0.0081 s | 0.0017 s |
| 5,000 | not run | 0.0569 s | 0.0538 s |

A colleague writes "C++ is 60 times faster than Python." Write the honest claim, explain the 5,000 row, and list what the report must add.
Model answer: (1) Against pure Python the speed-up is 60 at $N = 1{,}000$ and about 100 at 2,000; against NumPy it is 4.5 and 4.8; the claim must name which Python. (2) From 2,000 to 5,000 the work grows by $6.25$ (the loop is $\Theta(N^2)$), but the C++ time grows by about 32 and NumPy's by 7: a cost has appeared that is not the arithmetic. (3) Deep in the tree the option values far out of the money fall below about $2.2 \times 10^{-308}$ and become subnormal numbers, which this CPU handles slowly; setting values below $10^{-300}$ to zero gave 0.0122 s at 5,000 with the same price to 9 decimal places [measured]. (4) The report must add the compiler, version and flags; the spread (minimum and maximum, not only the median); confirmation that every version prints the same price at each $N$; and what the timer includes. (5) A fair one-line claim: "On this machine, at $N$ from 1,000 to 2,000, the C++ loop is about 60 to 100 times faster than the same loop in Python and about 4.5 times faster than NumPy; from about 3,000 steps subnormal numbers slow both, and flushing them restores the ratio."
Rubric (10, scaled to 8 marks): 2 for naming both baselines with their ratios; 2 for comparing the growth with $N^2$; 2 for subnormal numbers as the cause with the fix; 2 for the missing items in (4); 2 for a claim that a reader could check. Answers that call the 5,000 row "noise" score 0 on points 2 and 3, because the spread in the source data (0.053 to 0.066 s for C++) is far smaller than the jump.

### 4.3 Item 2.4: Arena rounds and a proposed exit

**Arena rounds** (`exm.contests.arena-1`, `-2`, `-3`; proposed paper kind `contest`, section 8 request 2). Each round is a `contest-arena` sitting (`widgets-programming.md` 9.1): 120 minutes, 6 problems A to F in rising difficulty, ICPC-style scoring (problems solved, then penalty minutes: solve time plus 20 per rejected submission), Python or (web app, after 1.9 lesson 62) C++, a seeded scoreboard of simulated rivals, Bertie `away`, editorials and the upsolve list afterwards.

| Round | When | Problems (Codeforces Div. 2 equivalents, our estimate) | Levels drawn on | Expected for the 1,400 target |
|---|---|---|---|---|
| `arena-1` | After level KC4 (lesson 21) | A, A, B, B, C, C | KC1 to KC4 and all of 1.8 | 3 or more solved |
| `arena-2` | After level KM5 (lesson 47) | A, B, B, C, C, D | adds KM1 to KM5 | 3 or more |
| `arena-3` | After level KD3 (lesson 84) | A, B, C, C, D, E | every 2.4 level | 3 or more, with C solved |

Each problem has a reference solution in Python and C++, a brute force, a generator of tests, a checker where answers are not unique, and a Python time limit scaled by the device calibration; a Python reference must pass in under half the limit on the reference phone or the problem is web-only and the round says so on its rules screen [unverified: Pyodide speed on the phone, open item 6's spike measures it]. Rounds are progress markers, not gates: a round with fewer than 3 solved adds its unsolved problems to the upsolve queue and suggests the level whose lessons the misses used.

**Proposed `2.4.exit`** (owner decision, section 0.5 item 5). The curriculum gives targets (one contest a week once 100 problems are solved; a rating of 1,400 in the first year) and no exit; `assessment.md` 11.6 keeps both as goals. Without an exit 2.4 has no completion state. The proposal:

| Part | Gate | Confirm | Why this and not the rating |
|---|---|---|---|
| `2.4.exit` | (1) 30 contest log entries, each with its upsolve marked done (problems solved during the contest plus at least one more afterwards, or a note that none was within reach); (2) `arena-3` with at least 3 of 6 solved | None. The Codeforces rating stays a goal on the progress page, and on the developer track the planner shows "1,400 target: 1,312 now" from the learner's log | A rating depends on who else enters, moves with rating-system changes, and cannot be read by the Artifact (`assessment.md` 11.6: the API's cross-origin access is unverified). The practice record is what the hours buy and what the app can see. Rejected: rating 1,400 as a gate (it would leave a learner who did every hour "not complete" for reasons outside the curriculum) |

```ts
// proposed exit data for 2.4; needs 'contest-upsolved' in log-count's enum and kind 'contest' in the paper kinds (section 8)
{ id: '2.4.exit',
  text: 'Thirty contests entered and upsolved, and the third Arena round with at least three of six problems solved',
  gate: [ { kind: 'log-count', log: 'contest-upsolved', target: 30 },
          { kind: 'exam', exam: 'exm.contests.arena-3', pass: 0.5 } ],
  confirm: [],
  estHours: 2.5 }
```

`pass: 0.5` reads, under the `contest` kind, as 3 of 6 problems solved: the kind's score is problems solved over problems set, and penalty minutes only order the scoreboard [our choice]. `estHours` 2.5 is the third round and its review; the contests themselves are earned through their log entries (section 1.3). If canon-gap O1 is accepted, trader and researcher tracks take the 36-lesson core and a 60-hour budget with 12 contests and `arena-2`; the schema has no per-track instrument values, so that version is a second part `2.4.exit-core` selected by track (section 8 request 3). If the owner instead raises 2.4 to about 190 hours for one contest every week (decision 18), the target becomes 50.

### 4.4 The 1.8 and 1.9 exits, rebuilt

| Part | Curriculum line | Gate (in the app) | Confirm (logged) | Taught in | Runs on |
|---|---|---|---|---|---|
| `1.8.exit` | 150 problems solved, and a fresh LeetCode medium finished in 30 minutes more often than not | (1) the problem ledger at 150 (in-app verified and self-reported, shown apart, `assessment.md` 11.5); (2) timed held-out mediums from `pool.alg.timed`: at least 5 solved within 30 minutes in the last 9 timed attempts | None: the app cannot see LeetCode, and its held-out bank is the only source of mediums the learner has certainly not seen | All 26 levels; lesson 148 (stress testing), lessons 149 and 150 (the method and the timed window) | Both (Python); C++ attempts on the web app once 1.9 lesson 62 is done |
| `1.9.exit` | Rewrite the 1.7 binomial pricer in C++ with tests and time it against the Python version | `setup-checklist` paste-verify `exit-1.9`: the doctest summary, the prices and timings at three sizes, and the build line, checked against the app's own prices | None | CP3 (lessons 79 to 84) and CP2 (73 to 78) | Paste: both; the build and timings always run on the learner's machine |

```ts
// exit data, using assessment.md 2.10's ExitPart; no new instrument kinds
{ id: '1.8.exit',
  text: '150 problems solved, and a fresh LeetCode medium finished in 30 minutes more often than not',
  gate: [ { kind: 'counter', counter: 'algo-solved', target: 150 },
          { kind: 'timed-window', pool: 'pool.alg.timed', minutes: 30, solved: 5, of: 9 } ],
  confirm: [],
  estHours: 9 }

{ id: '1.9.exit',
  text: 'Rewrite the 1.7 binomial pricer in C++ with tests and time it against the Python version',
  gate: [ { kind: 'paste-verify', check: 'exit-1.9' } ],
  confirm: [],
  track: { deferTo: 2, tracks: ['trader', 'researcher'] },
  estHours: 12 }
```

**`1.8.exit`: the timed window.**

- **Reading "more often than not".** At least 5 of the last 9 attempts, a majority over a window long enough that one good day does not pass it and one bad day does not fail it [our choice; `assessment.md` 2.9 fixes 5 of 9]. Attempts before the ninth show "4 of 7 so far"; the part is met the first time a window of 9 holds 5 solves, and stays met.
- **An attempt.** `problem-workbench` timed mode: a problem the learner has never been served, drawn so that no two of any 9 consecutive attempts share a pattern group; a 30-minute clock that starts when the statement opens; Bertie `away`; `Run` on the visible examples allowed; submission runs the hidden tests and the complexity test. **Solved** means every hidden test passing, the complexity test included, within the 30 minutes. A submission at minute 34 that passes is recorded as "solved late", counts on the ledger, and is not a solve for the window.
- **The bank.** 40 mediums in 12 pattern groups (section 3.4), so four full windows stay fresh. When fewer than 9 unseen problems remain, the bank serves the least recently seen and the window screen says "this attempt reuses a problem you saw 41 days ago"; the content plan adds 12 mediums a year [our choice].
- **Abandoning.** Leaving before submitting records an unsolved attempt: the window measures finishing, and "fresh" means one look.
- **After each attempt.** The debrief opens Bertie in review mode, the reference solution, the code-craft review of the learner's code, and a 5-minute "what I would do differently" note that the next window's first screen shows. The 9 hours of `estHours` are 9 attempts of 30 minutes plus 30-minute debriefs.
- **The ledger.** "150 solved: 112 verified in the app, 38 self-reported" (`assessment.md` 11.5). Timed attempts that pass count on the ledger like any other problem. The planner shows the 168-problem plan (decision 7) and the gap.

**`1.9.exit`: the brief.**

1. **Starting point.** The learner's own 1.7 code: `price_tree(S0, K, u, d, R, n, kind)` and `price_crr(S0, K, r, sigma, T, n, kind)` from `drl.fin.exit-binomial` (`stage1-finance-projects.md` 4.1.3), and, if the learner wrote it in the Pricing Lab, the American variant of `trees.py`.
2. **The C++ library.** `include/pricer.hpp` declares `enum class Kind { Call, Put };` and the same two functions with the same argument order, `double` arithmetic, and `std::invalid_argument` where the Python raises `ValueError`. One `std::vector<double>` of length $n + 1$ overwritten backwards (lesson 79). An `american` flag, defaulting to European, is recommended and tested if present.
3. **Tests (doctest, at least 8 test cases)**, mirroring the 1.7 drill's hidden tests so that both versions are held to one standard:
   - the exact tree: $S_0 = 4$, $K = 5$, $u = 2$, $d = \frac12$, $R = \frac54$, $n = 3$ gives a call of $\frac{288}{125} = 2.304$ and a put of $\frac{108}{125} = 0.864$, to $10^{-12}$ in doubles [verified];
   - parity in 20 seeded trees, call minus put equal to $S_0 - KR^{-n}$ within $10^{-12}$;
   - convergence: `price_crr` at $n = 2{,}000$ within $2 \times 10^{-3}$ of Black-Scholes in the 1.7 drill's four cases (the at-the-money call is 10.449584 against 10.450584 [verified]);
   - one step: $n = 1$ with $S = K = 100$, $T = 1$, $r = 5\%$, $\sigma = 20\%$ gives 12.1623 (lesson 79) [verified];
   - inputs: $d \ge R$, $R \ge u$, $n < 1$ and $\sigma \le 0$ throw `std::invalid_argument`;
   - memory: $n = 20{,}000$ runs (one vector of 160 KB; the full tree would hold about 200 million nodes, 1.6 GB);
   - if American: the put at $n = 1{,}000$ is 6.089595, above the European 5.571527; the American call equals the European call; with $r = 0$ the American put equals the European put (all [verified]).
4. **The timing protocol** (lesson 82). A Release build (`-O2`, sanitisers off), `bench/bench.cpp` timing `price_crr` for the at-the-money call at $N$ = 1,000, 2,000 and 5,000 with 7 repeats each after one warm-up, reporting median, minimum and maximum; the learner's 1.7 Python function timed the same way with `time.perf_counter` in a separate script, stating whether it uses loops or NumPy. Both print the price at each $N$ to 9 decimal places.
5. **The paste.** Four blocks: the compiler line (`g++ --version` or `clang++ --version`) and the CMake build type; the doctest summary; the C++ timing table; the Python timing table. The README (not pasted) holds a one-paragraph interpretation in the format of `exm.cpp` Q22's model claim.

**What `exit-1.9` checks** (a request to `widgets-programming.md` 6.11, section 8 request 5):

| Check | Accepts | Why |
|---|---|---|
| Toolchain | GCC 13 or later, or Clang 17 or later, with `-std=c++20` or later | Decision 11; the widget's current floor (GCC 11, Clang 14) is lower than the lessons need |
| Build | `CMAKE_BUILD_TYPE=Release` or `RelWithDebInfo`, or flags containing `-O2` or `-O3`; no `-fsanitize` | A Debug or sanitised timing is the trap of lessons 70 and 84 |
| Tests | A doctest summary line with at least 8 test cases and 0 failed | The brief's minimum |
| Prices | At $N$ = 1,000, 2,000 and 5,000, the C++ and Python prices agree with the app's own CRR prices (10.448584104, 10.449583775 and 10.450183638 [verified]) to $10^{-9}$ | The checker recomputes, so a pasted table cannot be invented without running a correct pricer |
| Timings | 7 repeats per $N$ for each language, with median, minimum and maximum; the checker computes the speed-ups from the medians | A speed-up with a spread, not one run |
| Not checked | That C++ is faster | A learner whose C++ is slower at 5,000 has found lesson 78's subnormal numbers and explains them; the exit asks for an honest timing, not a particular result |

**What one machine gave** [measured, Intel Xeon 2.1 GHz, GCC 13.3, `-O2`, medians of 7]: at $N = 1{,}000$, C++ 0.00073 s, NumPy 0.0033 s, pure Python 0.0437 s; at 2,000, 0.0017, 0.0081 and 0.177 s; at 5,000, C++ 0.0538 s and NumPy 0.0569 s, both slowed by subnormal numbers, and C++ 0.0122 s with values below $10^{-300}$ set to zero, at the same price. These numbers appear in lessons 78 and 82 as one machine's illustration and are never an answer.

**Track rule.** On the Trader and Researcher tracks `1.9.exit` moves to the Stage 2 checklist (`track.deferTo: 2`); the 1.9 lessons and `exm.cpp` stay in Stage 1's order, so a trader who defers still meets C++ before Stage 2's projects, and the planner schedules the exit's 12 hours inside Stage 2's first 10 weeks [our choice].

### 4.5 The Stage 1 exit test, rebuilt

The curriculum gives Stage 1 no checklist of its own; its map line reads "University finals at 70% in calculus, linear algebra and probability; 150 algorithm problems solved", and each item has its own exit line. Stage 1 is therefore closed when all nine topics are closed, and a topic is closed by its topic paper together with its exit parts (`assessment.md` 2.8). The stage page shows the map line's two headline bars first (the three finals; 150 problems), then the nine topics.

| Topic | Topic paper | Exit part | Gate (in the app) | Confirm (logged) | `estHours` of the exit part | Runs on |
|---|---|---|---|---|---|---|
| 1.1 Python | `exm.python`, 90 min, 70% | `1.1.exit` | Capstone `drl.py.exit-capstone` on a seeded messy CSV, then `exit-1.1` paste-verify of the same script run locally | None | 10 | Both (pandas in the Artifact) |
| 1.2 Tools | `exm.tools`, 60 min, 70% | `1.2.exit` | `exit-1.2` paste-verify: `git log`, `git status`, `pytest -q` with at least 1 passed | None | 3 | Both (GitHub API on the web) |
| 1.3 Calculus | `exm.calc.finals` (inside the exit) | `1.3.exit` | `exm.calc.finals` at 70% and 70% on Section A; sets M1 to M4 submitted and redone | A real 18.01 final at 70%; the 18.02SC Unit 2 problem sets logged | 15 | Both |
| 1.4 Linear algebra | `exm.linalg` (inside the exit) | `1.4.exit` | `exm.linalg` at 70%; capstones `drl.linalg.exit-lstsq` and `drl.linalg.exit-pca` | A real 18.06 final at 70% | 11 | Both |
| 1.5 Probability | `exm.prob.finals` (inside the exit) | `1.5.exit` | `exm.prob.finals` at 70% | Two real Stat 110 finals at 70%, at least 3 days apart | 20 | Both |
| 1.6 Statistics | `exm.stats` (inside the exit) | `1.6.exit` | `exm.stats` at 70% with `slotMin` 0.7 on Q19; capstone `drl.stats.exit-ols` | None | 9.5 | Paper both; capstone where statsmodels ships |
| 1.7 Finance | `exm.fin` (inside the exit) | `1.7.exit` | `exm.fin` at 70% with `slotMin` 0.7 on Q4, Q5 and Q7; `drl.fin.exit-binomial` | None | 2 | Both |
| 1.8 Algorithms | `exm.algorithms`, 90 min, 70% | `1.8.exit` | Ledger at 150; 5 of the last 9 timed held-out mediums within 30 minutes | None | 9 | Both |
| 1.9 C++ | `exm.cpp`, 90 min, 70% | `1.9.exit` (Stage 2 on the Trader and Researcher tracks) | `exit-1.9` paste-verify | None | 12 | Paste both; build local |

Stage page line: "Stage 1 exit: 6 of 9 topics closed. Finals: 2 of 3 at 70%. Problems: 131 of 150."

**Sit it first: the diagnostic route** (`assessment.md` 7.2). On entering Stage 1, the stage page leads with "Sit the exit test first" when placement puts the learner past the stage's midpoint or the learner says they have studied this material; otherwise it is offered with its time. Every gate a newcomer can sit cold is listed in path order with its time:

| Order | Sitting | Time | What a fail produces |
|---|---|---|---|
| 1 | `exm.python`, then the 1.1 capstone drill | 1.5 h + about 1.5 h | Study list by 1.1 level |
| 2 | `exm.tools`; the 1.2 paste if a repository exists | 1 h + 0.25 h | Study list by 1.2 level |
| 3 | `exm.calc.finals` | 3 h | Section A and B skills below 60% |
| 4 | `exm.linalg`, then the two capstones | 3 h + about 2 h | By 1.4 level |
| 5 | `exm.prob.finals` | 3 h | By 1.5 level |
| 6 | `exm.stats`, then its capstone | 1.5 h + about 1.5 h | By 1.6 level |
| 7 | `exm.fin`, then `drl.fin.exit-binomial` | 1.5 h + about 1 h | By 1.7 level |
| 8 | `exm.algorithms`, then 3 timed held-out mediums | 1.5 h + 1.5 h | By 1.8 level; the 3 attempts count towards the first window |
| 9 | `exm.cpp`; the 1.9 paste if the learner already has a C++ pricer | 1.5 h | By 1.9 level |
| | **Total** | **about 25 hours**, in at least nine sittings | |

Rules for the route [our choice, within `assessment.md` 7.2]: each sitting is a diagnostic (no cool-down, no XP for a fail, full credit for a pass); a sitting can be taken in any order, but the page recommends path order because a learner who scores below 40% on `exm.python` will not pass the later code items and is told so ("Stop here and start at 1.1, level A1?"); confirm instruments (the real finals) come after their gates, as everywhere; the ledger's self-reported problems count from the first day, so a learner who has 150 LeetCode problems logs them before sitting step 8. A full pass of Stage 1 by diagnostics credits all 1,400 hours as **credited**, never as earned (`assessment.md` 7.4).

**What the rebuilt test changes.** Nothing in `assessment.md` 2.9's rows except three requests (section 8): `1.4.exit`'s `estHours` as 11 (already requested by `stage1-linear-algebra.md`), the `exit-1.9` check's details above, and a stage-level "headline bars" field so the map line's two bars can be shown without hard-coding them.

---

## 5. Reading and resource map per level

**Rules.** Each level's `companion` lists what to read, watch or solve outside the app, what to do with it, and its hours; the hours sum to the reading and lectures block of each hours budget (section 1). Chapter, lecture and problem-set numbers marked [check] are recalled and must be confirmed against the source before content cites them (`checked: false` until then). Paid books are never required: every level names a free route, and the paid book is the stated alternative. Problem-list videos (NeetCode) sit inside Gym hours, not here. Source ids are canon-gap's; ids marked † are new and listed in section 8.

**Resources.**

| Id | Resource | Licence and cost | Where | Role |
|---|---|---|---|---|
| `src.grokking` | Bhargava, *Grokking Algorithms*, 2nd edition (Manning 2024), 13 chapters [check: chapter list] | Paid | Manning | 1.8 first read (the curriculum's pick) |
| `src.mit-6006-2020` | MIT 6.006 Introduction to Algorithms, Spring 2020 (Demaine, Ku, Solomon): lecture videos, notes, problem sets with solutions | Free, CC BY-NC-SA 4.0 | https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ | 1.8 theory thread (canon-gap G17) |
| `src.neetcode150` | NeetCode 150 list and video solutions; problems on LeetCode | Free | https://neetcode.io/practice | The logged outside list; video pointers from Gym problems |
| `src.clrs-4e` | Cormen, Leiserson, Rivest, Stein, *Introduction to Algorithms*, 4th edition (MIT Press 2022) | Paid | | Reference only (the curriculum's ruling) |
| `src.mit-6046j-2015` | MIT 6.046J Design and Analysis of Algorithms, Spring 2015 | Free, CC BY-NC-SA | https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/ | Stretch: flows, randomised algorithms |
| `src.learncpp` | learncpp.com, chapters 0 to 28 with quizzes and solutions [check: chapter numbers after the site's reorganisation] | Free to read | https://www.learncpp.com/ | 1.9 spine (the curriculum's pick) |
| `src.stroustrup-ppp-3e` | Stroustrup, *Programming: Principles and Practice Using C++*, 3rd edition (2024) | Paid | | 1.9 paid alternative |
| `src.stanford-cs106l` | Stanford CS106L Standard C++ Programming: lecture slides and assignments | Free (public course site) | https://web.stanford.edu/class/cs106l/ [check: the current quarter's path] | Lecture parallel for modern idioms |
| `src.cppreference` † | cppreference.com | Free, CC BY-SA 3.0 and GFDL [check] | https://en.cppreference.com/ | Reference for `<random>`, `<numeric>`, `<thread>`, `<atomic>` |
| `src.cpp-core-guidelines` † | Stroustrup and Sutter (eds.), C++ Core Guidelines | Free | https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines | Review checklist (lesson 71) |
| `src.drepper-memory` † | Drepper, *What Every Programmer Should Know About Memory* (2007), sections 3 and 6 [recalled] | Free PDF | https://www.akkadia.org/drepper/cpumemory.pdf [check] | Caches, for level CP2 |
| `src.carruth-cppcon-2014` † | Carruth, "Efficiency with Algorithms, Performance with Data Structures", CppCon 2014 [recalled] | Free video | CppCon's YouTube channel [check: link] | Why contiguous data wins |
| `src.joshi-cpp-2e` | Joshi, *C++ Design Patterns and Derivatives Pricing*, 2nd edition (CUP 2008) | Paid | | Pricing design reference for CM4 and CP3 |
| `src.laaksonen-cph` | Laaksonen, *Competitive Programmer's Handbook*, 30 chapters [check: chapter numbers of the current PDF] | Free PDF | https://cses.fi/book/book.pdf | 2.4 text |
| `src.cses` | CSES Problem Set | Free | https://cses.fi/problemset/ | 2.4 problem list |
| `src.usaco-guide` | USACO Guide, Silver and Gold modules | Free | https://usaco.guide/ | Topic order and extra problems |
| `src.codeforces` | Codeforces contests, problemset and EDU courses | Free | https://codeforces.com/ (EDU: https://codeforces.com/edu/courses) | The curriculum's contest site |
| `src.project-euler` | Project Euler | Free | https://projecteuler.net/ | Maths with code (lesson 20) |
| `src.kaggle` † | Kaggle competitions | Free | https://www.kaggle.com/competitions | Researcher track (lesson 21) |
| `src.imc-prosperity` † | IMC Prosperity trading competition (annual) [check: dates and rules each year] | Free | https://prosperity.imc.com/ [check] | Trader track (lesson 21) |

### 5.1 Item 1.8 (36.0 hours: Grokking 10.0, 6.006 lectures 12.0, 6.006 problem sets 14.0)

| Level | Read, watch or solve | What to do | Hours |
|---|---|---|---|
| AC1 How Cost Grows | Grokking ch. 1 (binary search, big O) [check]; 6.006 lectures 1 (algorithms and computation) and 2 (data structures, dynamic arrays) [check] | Read Grokking after lesson 1; watch lecture 2 after lesson 4 and redo its amortised doubling argument on paper | 2.25 |
| AC2 Recursion and Proof | Grokking ch. 3 (recursion); 6.006 problem set on asymptotics and recurrences (problem set 1) [check] | Do the problem set's recurrence and proof parts after lesson 13, self-mark against the solutions, log wrong parts to the Redo queue | 2.75 |
| AC3 Sorting | Grokking ch. 2 (selection sort, arrays and linked lists) and ch. 4 (quicksort); 6.006 lecture 3 (sets and sorting) [check] | Trace Grokking's quicksort on the array of lesson 16's hook; watch lecture 3 before lesson 18 | 2.25 |
| AC4 Selection and Order | 6.006 lecture 5 (linear sorting) [check]; CLRS ch. 9 (medians and order statistics), reference only [check] | Watch lecture 5 before lesson 22; use CLRS 9.2 only if lesson 20's expected-cost argument is unclear | 0.75 |
| AH1 Arrays and Hash Tables | Grokking ch. 5 (hash tables); 6.006 lecture 4 (hashing) [check]; 6.006 problem set on hashing (problem set 2 or 3) [check] | Read after lesson 25; watch lecture 4 before lesson 26 (universal hashing); do the set's hashing parts | 3.5 |
| AH2 Two Pointers | None outside the app; NeetCode "Two Pointers" videos sit inside Gym hours | | 0 |
| AH3 Sliding Windows | None outside the app (NeetCode "Sliding Window") | | 0 |
| AH4 Prefix Sums | None outside the app | | 0 |
| AH5 Binary Search | Grokking ch. 1, second read of the binary-search section | Re-read after lesson 46 and find the off-by-one the book's version avoids | 0.25 |
| AH6 Intervals | None outside the app (NeetCode "Intervals") | | 0 |
| SQ1 Stacks | None outside the app (NeetCode "Stack") | | 0 |
| SQ2 Queues and Linked Lists | CLRS 10.1 to 10.2, reference only [check] | Optional | 0 |
| SQ3 Heaps | 6.006 lecture 8 (binary heaps) [check]; 6.006 problem set on heaps and priority queues [check] | Watch before lesson 71; do the set's heap parts after lesson 73 | 2.75 |
| SQ4 Randomised Structures | CLRS ch. 5 (probabilistic analysis), reference only | Optional, for lesson 75's proof | 0 |
| TG1 Binary Trees | Grokking ch. 7 (trees) [check: new in the 2nd edition]; 6.006 lecture 6 (binary trees, part 1) [check] | Read after lesson 79; watch before lesson 82 | 1.5 |
| TG2 Search Trees and Tries | Grokking ch. 8 (balanced trees) [check]; 6.006 lecture 7 (AVL trees) [check]; 6.006 problem set on binary trees and AVL [check] | Watch lecture 7 before lesson 87; do the set's rotation and augmentation parts | 3.5 |
| TG3 Graphs and Traversal | Grokking ch. 6 (breadth-first search); 6.006 lectures 9 (BFS) and 10 (DFS) [check]; 6.006 problem set on graph search [check] | Watch lecture 9 before lesson 93 and lecture 10 before lesson 95; do the set after lesson 98 | 4.25 |
| TG4 Weighted Graphs | Grokking ch. 9 (Dijkstra's algorithm); 6.006 lectures 12 (Bellman-Ford) and 13 (Dijkstra) [check]; 6.006 problem set on weighted shortest paths [check] | Read Grokking ch. 9 before lesson 99; watch both lectures; do the set after lesson 102 | 4.25 |
| TG5 Graph Techniques | CLRS ch. 19 (disjoint sets) and ch. 21 (minimum spanning trees), reference only [check] | Optional, for lessons 104 and 103's proofs | 0 |
| DP1 Backtracking | None outside the app (NeetCode "Backtracking") | | 0 |
| DP2 From Recursion to DP | Grokking ch. 11 (dynamic programming), first half; 6.006 lecture 15 (recursive algorithms, the SRTBOT framework) [check] | Read after lesson 116; watch lecture 15 and map its six steps to the app's five (state, recurrence, order, base, answer) | 1.5 |
| DP3 Two-Dimensional DP | Grokking ch. 11, second half (longest common substring and subsequence); 6.006 lecture 16 (DP subproblems) [check]; 6.006 dynamic-programming problem set [check] | Do the set after lesson 126; compare its subproblem definitions with yours before reading the solutions | 3.5 |
| DP4 Designing DPs | 6.006 lecture 17 (DP part 3) [check] | Watch before lesson 129 | 0.75 |
| DP5 Greedy Algorithms | Grokking ch. 10 (greedy algorithms, including the set-covering and NP-complete sections) [check] | Read after lesson 134; write one counterexample to a greedy rule from the chapter | 0.75 |
| DP6 Bits and Integer Maths | None outside the app (NeetCode "Bit Manipulation", "Math and Geometry") | | 0 |
| DP7 Hard Problems and the Method | Grokking ch. 12 (k-nearest neighbours) and ch. 13 (where to go next) [check]; 6.006 lecture 19 (complexity) [check] | Read for orientation; watch lecture 19 before lesson 144 | 1.5 |
| | **Total** | Grokking 10.0; lectures 16 at 0.75 = 12.0; problem sets 7 at 2.0 = 14.0 | **36.0** |

**Stretch, outside the hours.** 6.046J for flows and randomised algorithms (before 2.4's KS3); Skiena's *Algorithm Design Manual* part II as a catalogue; *Elements of Programming Interviews in Python* for interview depth. **Developer track.** Stanford CS106B with Roberts' *Programming Abstractions in C++* (`src.stanford-cs106b` †), read alongside 1.9 rather than 1.8.

### 5.2 Item 1.9 (23.0 hours: learncpp 18.0, CS106L 3.0, talks and Drepper 2.0)

| Level | Read, watch or solve | What to do | Hours |
|---|---|---|---|
| CB1 From Source to Program | learncpp ch. 0 (introduction, compiler setup, build configurations, warnings) and ch. 1 and 2 (basics, functions and files) [check] | Install the toolchain with ch. 0, then do every quiz in ch. 1 and 2 on your own compiler | 2.0 |
| CB2 Types and Arithmetic | learncpp ch. 4 to 6 (fundamental types, constants and strings, operators) and ch. 10 (type conversion) [check] | Do the quizzes; for each "what does this print" quiz, predict before compiling | 2.5 |
| CB3 Functions and Files | learncpp ch. 7 and 8 (scope, linkage, control flow) and ch. 11 (overloading and function templates) [check] | Do the quizzes; build one multi-file quiz answer with a header and two source files | 2.0 |
| CB4 First Containers and Tests | learncpp ch. 16 and 17 (`std::vector`, `std::array`) [check] | Do the quizzes; write doctest cases for one quiz solution | 1.5 |
| CM1 The Memory Model | learncpp ch. 12 (references and pointers) and ch. 19 (dynamic allocation) [check] | Do the quizzes, then run each solution under `-fsanitize=address,undefined` | 1.5 |
| CM2 Classes and Invariants | learncpp ch. 14 and 15 (classes) and ch. 21 (operator overloading) [check]; CS106L lecture on classes and RAII [check] | Do the quizzes; watch the lecture after lesson 31 | 2.25 |
| CM3 Copying and Moving | learncpp ch. 22 (move semantics and smart pointers) [check]; CS106L lecture on move semantics [check] | Do the quizzes; watch the lecture before lesson 37 | 2.25 |
| CM4 Polymorphism and Design | learncpp ch. 20 (lambdas), 23 to 25 (object relationships, inheritance, virtual functions) [check]; Joshi ch. 1 to 3, paid alternative [check] | Do the quizzes; optional: Joshi's payoff-class chapters against lesson 46's design | 1.5 |
| CL1 Templates | learncpp ch. 26 (class templates) [check]; CS106L lecture on templates and concepts [check] | Do the quizzes; watch the lecture before lesson 49 | 1.75 |
| CL2 Containers | learncpp ch. 18 (iterators and algorithms, first half) [check]; CS106L lecture on containers and iterators [check] | Do the quizzes; watch the lecture before lesson 52 | 1.75 |
| CL3 Algorithms | learncpp ch. 18, second half [check]; cppreference's `<algorithm>` page, the "Sorting operations" group | Do the quizzes; read the `std::sort` page's requirement on the comparator before lesson 60 | 0.5 |
| CL4 Randomness and Numerics | learncpp ch. 8, the random-number lessons (Mersenne Twister, seeding) [check]; cppreference `<random>` | Read before lesson 63; note which distributions the standard leaves implementation-defined | 0.5 |
| CP1 Tools of a C++ Engineer | learncpp ch. 27 (exceptions) [check]; C++ Core Guidelines sections P, I and R (philosophy, interfaces, resource management) | Do the quizzes; use the guidelines as lesson 71's review checklist | 0.5 |
| CP2 Performance | Drepper sections 3 (CPU caches) and 6 (what programmers can do) [recalled; check section numbers]; Carruth's CppCon 2014 talk [recalled] | Skim Drepper for the cache-line model before lesson 73; watch the talk before lesson 74 | 2.0 |
| CP3 The Binomial Pricer in C++ | Joshi ch. 8 (trees), paid alternative [check] | Optional: compare Joshi's tree class with your one-vector design | 0 |
| CP4 First Contact with Concurrency | cppreference `std::jthread`, `std::mutex`, `std::atomic` pages | Read the three pages' examples before lessons 85 and 86 | 0.5 |
| | **Total** | learncpp 18.0; CS106L 4 lectures at 0.75 = 3.0; Drepper and Carruth 2.0 | **23.0** |

The CS106L lectures' 3.0 hours sit inside the CM2, CM3, CL1 and CL2 rows (0.75 each); the cppreference pages in CL3, CL4 and CP4 are counted with learncpp's 18.0 because they replace learncpp chapters on those topics. learncpp hours per row: 2.0, 2.5, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 0.5, 0.5, 0.5, 0, 0, 0.5 (CP4's cppreference) = 18.0.

**Developer reading list** (decision 14; outside 1.9's hours, inside canon-gap P13's 150 hours if accepted): Stroustrup, *A Tour of C++*, 3rd edition; Meyers, *Effective Modern C++* (items on move semantics, smart pointers and lambdas); Williams, *C++ Concurrency in Action*, 2nd edition (the curriculum: "Williams matters only for developer roles"); Roberts, *Programming Abstractions in C++*. Meyers comes after learncpp, as the curriculum says.

### 5.3 Item 2.4 (7.75 hours: CPH 5.5, USACO Guide and Codeforces EDU 2.25)

| Level | Read, watch or solve | What to do | Hours |
|---|---|---|---|
| KC1 How Contests Work | CPH ch. 1 (introduction: input and output, number types, shortening code) [check] | Read before lesson 2; set up the fast-input template it describes in Python and C++ | 0.25 |
| KC2 Ad Hoc Thinking | CPH ch. 6 (greedy algorithms) [check] | Read after lesson 8; optional: two CSES "Sorting and Searching" problems, in Gym time | 0.25 |
| KC3 Searching under Contest Limits | CPH ch. 5 (complete search) [check]; Codeforces EDU "Binary search", step 1 [check] | Read before lesson 16; do the EDU step's practice problems | 1.0 |
| KC4 Practice Discipline and Other Competitions | Project Euler problems 1 to 10; one past IMC Prosperity round's write-up or one Kaggle competition overview, by track | Solve the Euler problems in Python; read the track's competition page before lesson 21 | 0 (inside lessons 20 and 21) |
| KM1 Primes and Divisibility | CPH ch. 21, sections on primes, factors and the sieve [check] | Read before lesson 23; optional: CSES "Counting Divisors" as upsolving | 0.5 |
| KM2 Modular Arithmetic | CPH ch. 21, sections on modular arithmetic and solving equations [check] | Read before lesson 29; derive Fermat's inverse from the chapter before lesson 30 | 0.25 |
| KM3 Counting | CPH ch. 22 (combinatorics) [check] | Read before lesson 33; optional: CSES "Binomial Coefficients" as upsolving | 0.5 |
| KM4 Probability and Games | CPH ch. 24 (probability) and 25 (game theory) [check] | Read ch. 25 before lesson 41 (Sprague-Grundy) | 0.5 |
| KM5 Integer Geometry | CPH ch. 29 (geometry) [check] | Read before lesson 44; check its cross-product orientation test against lesson 44's | 0.5 |
| KS1 Range Queries | CPH ch. 9 (range queries) [check]; Codeforces EDU "Segment Tree, part 1", step 1 [check] | Read before lesson 50; do the EDU step | 1.25 |
| KS2 Trees at Scale | CPH ch. 14 (tree algorithms) and 18 (tree queries) [check]; USACO Guide Gold "Euler Tour Technique" and Platinum "Binary Jumping" [check: module levels] | Read before lesson 55; use the guide's problems for upsolving | 1.0 |
| KS3 Graphs at Scale | CPH ch. 17 (strong connectivity) and 20 (flows and cuts) [check] | Read ch. 17 before lesson 60 and ch. 20 before lesson 65 | 0.5 |
| KD1 DP Techniques | CPH ch. 7 (dynamic programming) and 10 (bit manipulation, bitmask DP) [check]; USACO Guide Gold "Bitmask DP" [check] | Read ch. 10 before lesson 67; do two of the guide's problems | 1.0 |
| KD2 Strings | CPH ch. 26 (string algorithms) [check] | Read before lesson 73 | 0.25 |
| KD3 Techniques for Hard Constraints | CPH ch. 27 (square root algorithms) [check] | Read before lesson 80 | 0 (inside lesson 80) |
| | **Total** | CPH 5.5; USACO Guide and EDU 2.25 | **7.75** |

CPH hours per row: 0.25, 0.25, 0.5, 0, 0.5, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0 = 5.5. USACO Guide and EDU: KC3 0.5, KS1 0.75, KS2 0.5, KD1 0.5 = 2.25.

**Stretch, outside the hours.** Halim and Halim, *Competitive Programming 4*, for breadth; the full CSES Problem Set (300 problems [recalled]) as the long-run list after Stage 2. **Contest problems in the app** are original (decision 6); CSES and Codeforces problems are linked, never copied.

---

## 6. Verification approach

Every answer is machine-checked twice before it ships (`content-format.md` section 6): the declared or generated answer against an independent computation, then the runtime grader replayed on the correct answer, its accepted forms and every diagnosed wrong answer. Three rules are specific to these items:

1. **Whatever the learner sees run is what CI ran.** Python runs on Pyodide 314.0.7 in Node and on CPython 3.11, and the two recordings must agree (`stage1-python-tools.md` section 6). C++ runs on GCC 13 and Clang 17 or later on x86-64 Linux, each at `-O0` and `-O2` with `-Wall -Wextra`, again with `-fsanitize=address,undefined`, and threaded snippets with `-fsanitize=thread`.
2. **Algorithm traces are unique by construction.** Every algorithm widget fixes its tie-breaking (Dijkstra and Prim break ties by node id, BFS and DFS visit neighbours in ascending order, quicksort's pivot rule is stated), so a "be the algorithm" state has one correct value, and any state rule that accepts several answers (topological orders, optimal reconstructions) is a predicate, never a stored list.
3. **Timings are never answers.** A timing on a screen is a [measured] illustration with its machine, compiler and flags; the question asks for a count, a ratio from counts, or a cause.

### 6.1 Item families in 1.8

| Family | Lessons | Independent check (CI) | Second check | Runtime grading and accepted forms |
|---|---|---|---|---|
| Step counts and doubling ratios | 1 to 7, AC1 homework, exam Q1 to Q3 | `trace-recorder` line-hit counts at $n = 0$ to 64 and at every $n$ an item names | The closed form, checked by SymPy equivalence over $n$ and by exact integers at the named $n$ (lesson 1's 31,626, 126,756, 1,769 and 4,034 came from this check) | `expression` by `cas` equivalence; numeric exact |
| Recurrences | 12, 13, exam Q4 | Exact evaluation of $T(n)$ for $n = 2^k$, $k \le 20$, by memoised recursion | The master-theorem class or recursion-tree sum, compared by the ratio $T(2n)/T(n)$ at $k = 20$ | Expression; class by choice |
| Algorithm states (sorts, heaps, deques, trees, graphs, union-find, DP tables) | Every `sort-lab`, `heap-lab`, `stack-queue-lab`, `tree-lab`, `graph-search`, `shortest-path`, `union-find`, `dp-table` screen | A Python reference that logs every step | The widget's JavaScript `algo-trace` service must produce the same event log on 500 generated inputs per family, and each predicate (`moveMatchesAlgorithm`, `isHeap`, `isTopoOrder`, `isValidBST`, `isMST`) accepts every correct state and rejects every seeded wrong state | Predicate on state; reconstructions by predicate |
| Generators | Every `gen.alg.*` | A TypeScript generator | A Python verifier written from the specification without reading the TypeScript, enumerating the parameter box: admissibility, difficulty, answer and every misconception value agree (`content-format.md` 5.6) | As the family |
| Code drills | 78 homework drills, 102 Gym problems, the 12 C++ Lab re-solves | The reference passes every hidden test on both runtimes with `needs: []` | Every `wrong/` file fails the test it names; every kept mutant of the reference fails a hidden test; a brute force agrees with the reference on at least 2,000 random small inputs | `code` check; marks by tests passed |
| Complexity tests | Every drill whose pattern is the point (decision 9) | Line budget and time ratio on a size ladder (`widgets-programming.md` 2.2.1) | A planted slower solution fails and the reference passes in 50 of 50 runs on the reference device | Pass or fail, with the measured exponent in words |
| Recursion depth | Recursive drills and lessons (decision 25) | Tests run with the recursion limit set to 600 | Inputs deeper than 500 are generated only for drills that ask for an iterative solution, and the statement says so | As the drill |
| Held-out banks | `pool.alg.timed` (40), `pool.alg.exam-mediums` (16), `pool.alg.exam-proofs` (12) | Isolation lint: no item of a held-out pool appears in lessons, practice, homework, level reviews, redo variants or Bertie's picks (`assessment.md` 3.2 rule 5) | Pattern-group tags checked so that 9 consecutive window attempts can avoid repeating a group | As code items |
| Originality | Every problem statement (decision 6) | Titles compared with the NeetCode 150 and CSES title lists; an exact or near match fails the build | A reviewer confirms the statement, numbers and setting are ours; the named NeetCode pointer is a link, never text | Not graded |
| Probabilistic claims | 17, 20, 25, 63, 75 to 77 | Exact values by `fractions` and enumeration (quicksort's expected comparisons for $n = 4$, expected empty buckets) | Simulation within 4 standard errors for 20 seeds; the linear-probing formula and the simulation are both quoted where they differ (lesson 26) | Numeric with stated tolerance |

### 6.2 Item families in 1.9

| Family | Lessons | Independent check (CI) | Second check | Runtime grading and accepted forms |
|---|---|---|---|---|
| Predict the output | Every `predict-output` and `code-tracer` C++ screen; exam Q3, Q5, Q10, Q12 | Build and run on GCC and on Clang at `-O0` and `-O2` | All four recordings must agree; an item whose output differs between compilers or levels is rewritten, or states the compiler (exam Q3's warning, which GCC gives and Clang 18 did not) | `output` with normalised whitespace |
| Undefined behaviour | 9, 10, 26, 27, 68, exam Q4 | The sanitiser build must report the stated error kind at the stated line | The item never records an "output" for UB: the screen shows the sanitiser report or the compiler's assumption (the signed-overflow loop: 31 iterations at `-O0`, no end at `-O2` on both compilers) | Set of lines; matching to report kinds |
| Diagnostics | 2, 3, 17, exam Q1 and Q2 | The recorded first diagnostic of each compiler | The stage (preprocessor, compiler, linker) is derived from which tool printed it, not from its wording | Sort or choice |
| Layout and sizes | 33, exam Q9 | `sizeof`, `alignof` and `offsetof` printed by the build | `static_assert` of the stated values in the snippet itself, so a platform change fails the build | Numeric exact; the aids card states LP64 |
| Code-blanks and Parsons | Exam Q8; lessons with `code-blanks` | Each accepted fill compiled and run against the item's tests | Each rejected fill's failure recorded (compile error or failing test) and used as its feedback | Token match against the compiled set |
| Drills (web or local) | CB to CP homework, C++ Lab, `prj.cpp.mc-pricer` | doctest suites pass on GCC and Clang, Release and sanitised builds | `wrong/` files fail their named tests; a sanitiser finding in the reference fails the build | `code` check through `cpp-runner` on the web (open item 1), or paste-verify of the doctest summary |
| Floating point and randomness | 63 to 67, exam Q16 and Q17 | Recorded on both standard libraries where available (libstdc++; libc++ when the pinned Clang ships it) [check] | Engine outputs (`mt19937`'s 10,000th value 4,123,659,995) are fixed by the standard; distribution outputs are never answers because they are implementation-defined | Numeric; choice |
| Timings | 73 to 78, 82, 88 | `bench-lab` recordings with machine, compiler, flags and 7 repeats | Only ratios and causes are asked; any quoted time carries [measured] | Not graded as numbers |
| The exit paste | `exit-1.9` | The checker's CRR prices at $N$ = 1,000, 2,000 and 5,000 against a reference in exact-rounded doubles | Parsers tested on recorded real output of doctest, GCC, Clang and CMake on Linux, macOS and Windows (MSVC builds are accepted when the toolchain line says so [check: MSVC's C++20 flag text]) | `setup-checklist` check `exit-1.9` |

### 6.3 Item families in 2.4

| Family | Independent check (CI) | Second check | Grading |
|---|---|---|---|
| Contest problems | References in Python and C++, a brute force, an input generator and an input validator that enforces the stated constraints | The two references agree on all tests; the brute force agrees on at least 2,000 small inputs; the Python reference passes in under half the scaled time limit on the reference device, or the problem is marked web-only | `stdout` tests, or a checker where several answers are right (2-SAT assignments, any valid hull start) |
| Interactive problems | An interactor written apart from the reference | The reference and five wrong strategies (off-by-one midpoints, too many queries) run against it: `guess.py` answers every hidden number in at most 30 queries [verified] | Interactor verdicts |
| Number theory and counting | SymPy for primes, factorisations, inverses and CRT; exact `Fraction` values converted to $p \cdot q^{-1} \bmod 998{,}244{,}353$ | Brute force on small parameters (divisor sums, binomials modulo a prime, expected rolls) | Numeric exact |
| Geometry | Exact integer arithmetic only; no floating point in references | Hulls checked against a brute-force hull on 1,000 random small point sets, with collinear and duplicate points | Checker for vertex order and start |
| Arena rounds | Each problem passes the family above | Rival scoreboards replay identically from their seed | ICPC scoring |
| Long-form proofs | Model answers' numeric claims evaluated in code | Rubric anchoring, as below | Self-mark with Bertie's suggestion |

### 6.4 Long-form items and what running found

**Long-form items** are never auto-passed or auto-failed. CI evaluates every number in a model answer as arithmetic, runs any code in it, and checks rubric anchoring: every rubric point names the model-answer lines it marks, and every line is used by a point. Learners self-mark against the rubric with Bertie's per-point suggestion (`ai-tutor.md` 2.7), and the result stays provisional until confirmed (`assessment.md` 3.5).

**What running found while writing this draft** (all fixed in the text above):

| Draft claim | What running showed | Fixed in |
|---|---|---|
| A knapsack example for the one-row table trap | The draft's items gave the same best value whichever way the row was filled; weights [2, 3], values [3, 4] and capacity 4 separate them: 4 when the row is filled downwards (0/1), 6 when filled upwards (the first item used twice) [verified] | Lesson 125 |
| A full $N = 10{,}000$ tree holds 50,005,001 nodes | 50,015,001, about 400 MB | Lesson 79 |
| `x & 1 == 0` is a precedence trap in Python | It is not: Python's comparison binds more loosely than `&`. The Python trap became `-5 >> 1 == -3`; the precedence trap stays in C++ only | DP6, `bit-lab` [mode to add] |
| An interactive guessing reference | The first version used 31 queries and returned wrong answers; the fixed one uses `mid = (lo + hi + 1) // 2` and at most 30 | KC3 homework |
| `std::format("{:,}")` gives thousands separators | It does not compile: `std::format` has no `,` option | Lesson 4 of 1.9 (a verified fact) |
| The C++ pricer scales as $N^2$ | It did up to about 3,000 steps, then subnormal numbers made $N = 10{,}000$ take 0.49 s instead of about 0.04 s | Lesson 78, CP2 homework, `exm.cpp` Q22 |
| KS3's minimum cut | The first working named a cut of capacity 20; the cut that proves 19 is $\{0, 2\}$ | KS3 example 1 |
| KM3's tie argument | The model answer described the leftmost minimum while the code assigns each subarray to its rightmost minimum | KM3 example 2 |

---

## 7. Sample lesson in full: What happens when the input doubles

**Why this lesson.** It is the root of 1.8's dependency graph and the first question of 1.9 and 2.4 as well. Every later analysis (big O in lesson 3, amortised appends in lesson 4, recurrences in 12 and 13, every complexity test in every drill, the subnormal slowdown in 1.9 lesson 78, contest constraints in 2.4 lesson 2) asks how cost changes when the input grows. The doubling ratio is that question in its most concrete form: run it twice, divide. Stage 0 taught logarithms as counts and 1.1 timed `x in list`, but nothing so far has asked a learner to predict growth from code. It is written at the level an author hands to the YAML stage (`content-format.md` 3.7, 3.10 and 10): every screen, widget configuration in plain words, check, diagnosis, hint ladder, Why?, solution and tutor fields. Copy follows design research 9.2: second person, sentences of at most 20 words, no exclamation marks, a term named only after it has been used. Every count, ratio and recorded output below was computed by running the code [verified]; the two timings are [measured] and are marked as one machine's.

**What it inherits.** 0.3 lesson 49 counted halvings (1,024 layers from 10 folds); 1.1 lesson 12 counted loop runs; 1.1 lesson 28 showed that `x in list` scans the list. This lesson joins them: it counts a program's work at $n$ and at $2n$ and reads the law from the ratio.

**Rules that apply to every screen here.**

- **Hints** open after the lesson's first Check and climb Nudge, Point, Step; Show solution appears after two not-yet results on a screen (design research 5.4 and 5.5; `ai-tutor.md` 2.2).
- **Element references** use `<widget id>/<kind>:<name>`. Code lines are `code/line:1` onward (on screen 2, the three cards are `codeA`, `codeB` and `codeC`); `value-table` cells are `table/cell:<row>,<col>`; `cell-grid` cells are `grid/cell:<r>,<c>`; race lanes are `race/lane:A`, `race/lane:B`, `race/lane:C`.
- **Bertie** follows the lesson player (`bertie.md` 5.3): `correct` or `notyet` on grading, `surprised` on the trap reveal (screen 8), `celebrate` at the end.
- **Tutor fields** hold no value a screen's check accepts; numbers that are answers are described in words ("the four-fold count").
- **Runtime.** `needs: []`. No screen runs live code: every program is authored, and its hit counts and outputs are recorded in CI, so the lesson runs identically on both targets with Python never loaded.

### 7.1 Lesson header

| Field | Value |
|---|---|
| `id`, `rev`, `status` | `lsn.algcost.doubling`, 1, `draft` |
| `title` | What happens when the input doubles |
| Position | Course AC (Algorithmic Cost), level AC1 (How Cost Grows), lesson 1 of 7; 1.8 lesson 1 |
| `summaryLine` | Double the input and divide: the ratio of the two costs names how a program grows. |
| `frame.why` | Data only grows. A backtest that runs in 2 seconds on a year must still run on ten years, and a risk model built for 500 stocks will be asked for 3,000. Knowing how cost grows tells you, before you wait, whether the bigger run takes minutes or days. |
| `frame.before` | 0.3 lesson 49 counted how many halvings reach 1; 1.1 lesson 28 showed that `x in list` checks the items one by one. Here you use both to predict a program's time on twice the data. |
| `insight` | The work at $2n$ divided by the work at $n$ settles, as $n$ grows, at a number that names the program: 2 for one pass, 4 for every pair, 8 for every triple, and "one more step" for halving. |
| `introduces` | `skl.alg.doubling-ratio`, `skl.alg.growth-law`, `skl.alg.hidden-scan` |
| `uses`, `requires` | `skl.pre.log-definition` (0.3 lesson 49); the loop-count and operation-cost skills of 1.1 lessons 12 and 28 (ids as `stage1-python-tools.md` assigns them [check]) |
| `terms` | `gls.alg.doubling-ratio`, `gls.alg.growth-law`, `gls.alg.linear`, `gls.alg.quadratic`, `gls.alg.cubic`, `gls.alg.logarithmic` |
| Embargoed terms | "big O", "Theta" and "asymptotic" (lesson 3); "complexity" as a technical word (lesson 3); "amortised" (lesson 4); "n log n" as a name before screen 6 |
| Common trap | Twice the data means twice the time, even for a loop with a hidden scan inside (screen `dedupe`) |
| `edgeCases` | Small inputs blur the law: 4 to 8 days multiplies pairs by 4.67, not 4 (`pair-grid`, `exact-ratio`); a halving loop gains one step instead of multiplying (`halving`); a fixed start-up cost makes a linear program's ratio look below 2 (`start-up`); a pass of halving searches grows by a little more than 2 (`search-each`) |
| `workedExample` | `at: search-each`. Naive: "A loop inside a loop, like version B, so four times the work." Decision: "Ask whether the inner loop's length grows with $n$ or halves." |
| `est` | 14 minutes: 12 screens (about 10.5 minutes) and a 4-item quiz (about 3.5 minutes) |
| `needs` | `[]` |
| `sources` | `src.grokking` (`parallel-reading`: ch. 1, the big O section [check]); `src.mit-6006-2020` (`further`: lecture 1 [check]) |
| `art` | `ast.course-art.doubling`: Bertie holding a stopwatch beside a stack of paper that is twice as tall as the one beside it |

**Misconceptions this lesson diagnoses** (new library entries, `mc.alg.*`):

| Id | `belief`, as a learner would put it | `correction` |
|---|---|---|
| `mc.alg.double-means-double` | "Twice the data always takes twice the time." | Only a single pass doubles; the ratio depends on how the work is built from the input. |
| `mc.alg.nested-always-square` | "A loop inside a loop always quadruples." | Only if the inner loop's length grows with $n$; an inner loop that halves adds one step. |
| `mc.alg.log-doubles` | "Halving steps double when the input doubles." | Doubling the input adds one halving. |
| `mc.alg.one-loop-linear` | "One visible loop means the time doubles." | Built-in operations such as `in` on a list hide a loop of their own. |
| `mc.alg.fixed-cost-sublinear` | "A ratio below 2 means the program grows more slowly than the data." | A fixed start-up cost drags small-input ratios down; subtract it or measure larger sizes. |
| `mc.alg.exact-four` | "Pairs multiply by exactly 4." | By $4 + \frac{2}{n-1}$: close to 4 only for large $n$. |
| `mc.alg.pair-includes-self` | "A day is compared with itself." | A pair is two different days. |
| `mc.alg.ordered-pairs` | "Day 2 with day 5 and day 5 with day 2 are two comparisons." | One comparison per unordered pair. |
| `mc.alg.ratio-of-n` | "The doubling ratio is 2 because $n$ doubled." | The ratio divides the two costs, not the two inputs. |
| `mc.alg.square-for-all` | "Doubling multiplies every nested count by 4." | Each nested level multiplies by 2: triples give 8. |

**Screen map.**

| # | Id | Type | Task | Difficulty | Widgets | Est. |
|---|---|---|---|---|---|---|
| 1 | `title` | `title` | none | none | art only | 15 s |
| 2 | `backtest` | `problem` (the hook) | predict three versions' times on two years | 1 | `code` (three cards), `table` (`value-table`, three `choice` rows), `race` (`complexity-lab` race, after Check) | 60 s |
| 3 | `pair-grid` | `problem` (manipulate) | shade every pair of days, for 4 days then 8 | 1 | `grid` (`cell-grid`, paint), `numeric-input` | 70 s |
| 4 | `ratio` | `problem` (names the idea) | the doubling ratio at 1,000 days | 1 | `code` (`code-tracer`, hits), `table`, `numeric-input` | 55 s |
| 5 | `halving` | `ladder` | steps of a halving loop at 504 and 1,008 | 2 | `code` (hits), `numeric-input` (two parts) | 45 s |
| 6 | `search-each` | `ladder` (the worked example) | probes of $n$ binary searches at twice the days | 3 | `code` (hits), `race`, `numeric-input`, `choice` | 80 s |
| 7 | `start-up` | `ladder` (edge) | the law behind a table with a fixed cost | 2 | `table`, `plot` (`plot-2d`, after Check), `choice` | 55 s |
| 8 | `dedupe` | `trap` | one loop, a hidden scan | 2 | `code` (hits, after Check), `choice` | 50 s |
| 9 | `rule` | `generalise` | complete the ratio line; predict a triple count | 2 | `expression-input`, `table`, `numeric-input` | 55 s |
| 10 | `exact-ratio` | `derive` | derive the exact pair ratio | 3 | `derivation-steps` (fill), `expression-input`, `numeric-input` | 70 s |
| 11 | `universe` | `problem`, `context: quant` (the transfer) | correlation pairs for 500 and 3,000 stocks | 2 | `numeric-input` | 50 s |
| 12 | `summary` | `summary` | none | none | none | 20 s |

Two non-task screens, the limit of design research 5.8. Screen estimates total 625 seconds; the quiz adds about 3.5 minutes.

### 7.2 Screens

#### Screen 1: `title`

- **Prose:** "A program that is quick on today's data may crawl on next year's. This lesson asks one question of every program: what happens when the input doubles?"
- **Art:** `ast.course-art.doubling`.
- **Bertie:** `idle`. Chat is open with no answer key; hints do not exist yet.

#### Screen 2: `backtest` (`problem`, the hook, difficulty 1)

- **Skills:** `skl.alg.doubling-ratio`.
- **Prose:** "A backtest covers one year, 252 trading days. It could be written three ways, and each takes 2 seconds on one year. Next month it must cover two years."
- **Canvas:** `codeA`, `codeB` and `codeC`, three read-only cards side by side (stacked on phones):

```python
# A: look at each day once
for day in days:
    update(day)

# B: compare every pair of days
for i in range(len(days)):
    for j in range(i + 1, len(days)):
        compare(days[i], days[j])

# C: look each day up in a sorted list, by binary search
for day in days:
    find(sorted_days, day)
```

  `table`, a `value-table` with rows A, B and C and one column, "Two years", each cell a `choice` of four chips: "about 4 s", "between 4 and 5 s", "about 8 s", "about 16 s". A note under the cards: "Assume the time is all in the loops, and every basic step takes the same time." `race`, a `complexity-lab` in race mode with three lanes [mode to add: three lanes], hidden until Check; its recorded counts are A 252 and 504 steps, B 31,626 and 126,756 comparisons, C 1,769 and 4,034 probes, each converted to seconds at 2 s for one year.
- **Question:** "Predict each version's time on two years."
- **Check:** `multi`, three parts; correct A "about 4 s", B "about 8 s", C "between 4 and 5 s". The screen is correct when all three are.
- **Diagnose:**

| Part and answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| B, "about 4 s" | `mc.alg.double-means-double` | "Twice the days gives twice as many rows of comparisons, and each row is twice as long." | The race plays lane B: 31,626 comparisons become 126,756 |
| C, "about 8 s" | `mc.alg.nested-always-square` | "Each search halves the sorted list. Twice the days adds one step to a search; it does not double it." | The race plays lane C: 1,769 probes become 4,034 |
| C, "about 4 s" | `mc.alg.log-doubles` (near miss) | "Close. There are twice as many searches, and each is one step longer, so a little more than double." | Lane C, with probes per search shown: 7.0 and 8.0 |
| A, anything but "about 4 s" | `slip` | "Version A does one step per day. Twice the days, twice the steps." | Lane A |

- **Otherwise:** "For each version, ask how much more work a second year adds."
- **Reason (verdict chip):** "A: 4 s. B: 4 times the comparisons, 8 s. C: 2.28 times the probes, about 4.6 s."
- **Hints:** Nudge: "For each version, what does one extra year add to the work?" Point: "Version B compares each day with every later day. With twice the days, how many partners does each day have?" (highlights `codeB/line:3`). Step: "A does each day once, so 4 s. B has twice the days, each with twice the partners: about four times the work, 8 s. C has twice the searches, each one step longer: a little over 4 s."
- **Why?** Yours: "You saw that each version's work is built differently from the days." Shown: "A counts days, B counts pairs of days, C counts days times the steps of one search." Then: "Doubling multiplies those by 2, about 4, and a little over 2. The rest of this lesson turns that into a rule." `rep`: counting.
- **Solution (Show solution):** the race plays all three lanes; text: "Same 2 seconds today, three different futures: 4 s, 8 s and about 4.6 s."
- **Tutor:** focus: "How the count of basic steps changes, not the clock." Notes: "Most learners pick the doubled time for all three; treat that as the expected first answer. The next screen counts B by hand." Reps: counting; picture (the pair grid). Avoid: "big O", "complexity", "quadratic", "logarithmic".

#### Screen 3: `pair-grid` (`problem`, manipulation, difficulty 1)

- **Skills:** `skl.alg.doubling-ratio`.
- **Prose:** "Count version B's work by hand. A shaded square means one comparison of a day with a later day."
- **Canvas:** `grid`, a `cell-grid` of 8 by 8 (`select: 'paint'`), rows and columns labelled day 1 to day 8. Only cells above the diagonal are paintable; the diagonal and the cells below it are grey. Part 1 outlines the top-left 4-by-4 corner and locks the rest; part 2 unlocks all eight days and keeps part 1's shading.
- **Questions and checks:**
  - Part 1: "Shade every pair among days 1 to 4." Check: `set`, the six cells $(r, c)$ with $1 \le r < c \le 4$.
  - Part 2: "Now shade every pair among days 1 to 8. How many squares are shaded?" Check: `set`, the 28 cells with $r < c$; and `numeric` 28.
  - Part 3: "The days doubled from 4 to 8. By what factor did the pairs grow?" Check: `numeric`, $\frac{28}{6} = \frac{14}{3}$, accepted as `14/3` or a decimal from 4.6 to 4.7.
- **Diagnose:**

| Learner state | Misconception | Feedback line | Show-why |
|---|---|---|---|
| Tries to paint a diagonal cell | `mc.alg.pair-includes-self` | "A day is not compared with itself. A pair is two different days." | The cell flashes grey and stays unpainted |
| Paints a cell below the diagonal (part 2 shows a mirrored ghost) | `mc.alg.ordered-pairs` | "Day 2 with day 5 is the same comparison as day 5 with day 2. Each pair is shaded once, above the diagonal." | The ghost folds onto its mirror above the diagonal |
| Part 3: 2 | `mc.alg.double-means-double` | "The days doubled; the pairs went from 6 to 28." | Count both shaded regions aloud |
| Part 3: 4 | near miss (`mc.alg.exact-four`) | "Close: 28 over 6 is a bit more than 4. Screen 10 shows why." | None |

- **Otherwise:** "Start with day 1. How many later days can it meet?"
- **Reason:** "6 pairs for 4 days, 28 for 8: a factor of 14/3, about 4.67."
- **Hints:** Nudge: "Start with day 1. How many later days can it be compared with?" Point: "Inside the 4-day frame, row 1 has 3 squares and row 2 has 2." (highlights `grid/cell:1,2` to `grid/cell:1,4`). Step: "Rows give 3 + 2 + 1 = 6 for four days, and 7 + 6 + 5 + 4 + 3 + 2 + 1 = 28 for eight."
- **Why?** Shown: "Doubling added more than the old pairs again." Then: "The four new days brought 6 pairs among themselves and 16 pairs with the old days: the 4-by-4 block on the right. That block is why pairs grow faster than days." `rep`: picture.
- **Solution:** the grid paints itself row by row with running totals; text: "6, then 28. The new block of new-against-old pairs is the surprise."
- **Tutor:** focus: "Where the extra pairs come from." Notes: "If the learner counts 28 by formula, accept it and ask where the 16 new-against-old pairs sit in the grid." Reps: picture (the grid); counting by rows. Avoid: the formula $\binom{n}{2}$ (screen 10 derives it in this lesson's terms).

#### Screen 4: `ratio` (`problem`, naming the idea, difficulty 1)

- **Skills:** `skl.alg.growth-law`.
- **Prose:** "You just found a **doubling ratio**: the work at $2n$ divided by the work at $n$. Where it settles as $n$ grows names the program's **growth law**. Settling at 2 means the work grows in step with $n$: **linear**. Settling at 4 means it grows like $n^2$: **quadratic**."
- **Canvas:** `code`, a `code-tracer` in `hits` mode on version B, with line 3's recorded hit counts in a `table`:

| Days $n$ | 4 | 8 | 252 | 504 | 1,000 | 2,000 |
|---|---|---|---|---|---|---|
| Comparisons | 6 | 28 | 31,626 | 126,756 | 499,500 | 1,999,000 |
| Ratio to the column two to the left | | 4.667 | | 4.008 | | ? |

- **Question:** "What is the doubling ratio from 1,000 days to 2,000? Give three decimal places."
- **Check:** `numeric`, $\frac{1{,}999{,}000}{499{,}500} = \frac{3{,}998}{999} = 4.002$, tolerance 0.0005; the fraction is accepted.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| 2 or 2.000 | `mc.alg.ratio-of-n` | "That is 2,000 over 1,000, the days. The ratio divides the comparisons." | Highlight `table/cell:2,6` over `table/cell:2,5` |
| 0.250 | `slip` | "That is the small count over the large. Put the work at 2,000 days on top." | Same |
| 4 or 4.000 | near miss | "Round to three places: the ratio is a little above 4." | None |

- **Otherwise:** "Divide the comparisons at 2,000 days by the comparisons at 1,000."
- **Reason:** "4.002: the ratios run 4.667, 4.008, 4.002 and settle at 4."
- **Hints:** Nudge: "Which two numbers in the table does the ratio divide?" Point: "Divide this cell by the one to its left." (highlights `table/cell:2,6`). Step: "1,999,000 divided by 499,500 is 4.002, to three places."
- **Why?** Shown: "The ratio falls towards 4 as the days grow." Then: "So version B's law is quadratic. Read the law at large $n$: small inputs blur it, as 4.667 did." `rep`: numbers.
- **Solution:** the ratio cell fills; text: "4.002. The ratios settle at 4: quadratic."
- **Tutor:** focus: "Ratio of costs, read at large inputs." Notes: "This is the first named idea; ask the learner to say 'doubling ratio' in their own words." Reps: numbers; the grid. Avoid: "big O".

#### Screen 5: `halving` (`ladder`, difficulty 2)

- **Skills:** `skl.alg.growth-law`.
- **Constraint added:** a loop whose remaining work halves.
- **Prose:** "Version C's search halves what is left at every step. Here is halving on its own."
- **Canvas:** `code`, a `code-tracer` in `hits` mode with the recorded run for $n = 252$ (the values of `n` shown: 252, 126, 63, 31, 15, 7, 3, 1, 0; line 3 runs 8 times).

```python
steps = 0
while n > 0:
    n = n // 2
    steps += 1
```

- **Question:** "Line 3 ran 8 times for $n = 252$. How many times for $n = 504$? And for $n = 1{,}008$?"
- **Check:** `multi` of two `numeric` parts, exact: 9 and 10.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| 16 (then 32) | `mc.alg.log-doubles` | "Doubling $n$ does not double the halvings. The first step takes 504 to 252, then the old path runs again." | Play $n = 504$: the first value, then the eight values already on screen |
| 9, then 18 | `mc.alg.log-doubles` (second part) | "Each doubling adds one step: 9, then 10." | Play $n = 1{,}008$ |

- **Otherwise:** "Write the first value of `n` after one step, then reuse the 252 run."
- **Reason:** "504 halves to 252 in one step, then follows the 8 steps you saw: 9 in all, and 10 for 1,008."
- **Hints:** Nudge: "What is `n` after one step, starting from 504?" Point: "From 252 the loop runs exactly as the recording shows." (highlights `code/line:3`). Step: "504 becomes 252 after one step; 252 then takes 8 more. So 9, and 1,008 takes 10."
- **Why?** Shown: "Doubling $n$ added one step." Then: "The count is the number of halvings that bring $n$ to 0, which is $\lfloor \log_2 n \rfloor + 1$ for $n \ge 1$, the count 0.3 lesson 49 taught. A law that adds a step per doubling is **logarithmic**." `rep`: counting.
- **Solution:** both runs play; text: "One more halving per doubling: 9 and 10."
- **Tutor:** focus: "Halving adds, it does not multiply." Notes: "Link to 0.3's folding sheet if the learner needs it: ten folds give 1,024 layers." Reps: counting; the folding sheet. Avoid: the base-change rule.

#### Screen 6: `search-each` (`ladder`, the worked example, difficulty 3)

- **Skills:** `skl.alg.growth-law`.
- **Constraint added:** a halving loop inside a loop over all $n$.
- **Prose:** "Version C runs one binary search per day. The searches halve, but there are $n$ of them."
- **Canvas:** `code`, a `code-tracer` in `hits` mode, recorded for 252 days (line 5 runs 1,769 times); `race`, lane C only, hidden until Check.

```python
probes = 0
for day in days:                     # one search per day
    lo, hi = 0, len(days) - 1
    while lo <= hi:                  # each step halves [lo, hi]
        probes += 1
        mid = (lo + hi) // 2
        if days[mid] == day:
            break
        elif days[mid] < day:
            lo = mid + 1
        else:
            hi = mid - 1
```

- **Worked example panel** (shown before the question): a colleague's note reads "A loop inside a loop, like version B, so four times the work: 7,076 probes on two years." Beneath it: "Decision point: does the inner loop's length grow with $n$, or does it halve?"
- **Questions and checks:**
  - Part 1: "About how many probes does one search take on 252 days?" `numeric`, $1{,}769 / 252 = 7.02$; accepted 7.
  - Part 2: "On 504 days each search takes about one probe more. Estimate the total probes." `numeric`, accepted 4,000 to 4,100 (the recording is 4,034; $504 \times 8 = 4{,}032$).
  - Part 3: "So the two-year run takes about:" `choice` of 4.0 s, 4.6 s, 8 s; correct 4.6 s.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| Part 2: 7,076 | `mc.alg.nested-always-square` | "That holds if each search scans the list. It halves it, so each search grows by one probe, not by a factor of 2." | Lane C plays: 1,769 to 4,034 |
| Part 2: 3,538 | `mc.alg.double-means-double` | "That doubles the searches but keeps each one 7 probes long. Each is one probe longer on 504 days." | Probes per search shown: 7.0 then 8.0 |
| Part 3: 8 s | `mc.alg.nested-always-square` | "Four times the work would be 8 s; the work grew 2.28 times." | Lane C |
| Part 3: 4.0 s | near miss | "Close: the searches got longer as well as more numerous." | None |

- **Otherwise:** "Multiply the number of searches by the probes per search, at each size."
- **Reason:** "504 searches of about 8 probes: about 4,030 against 1,769, a ratio of 2.28, so about 4.6 s."
- **Hints:** Nudge: "How many searches are there, and how long is each?" Point: "Screen 5 showed what doubling does to one halving loop." (highlights `code/line:4`). Step: "Twice the searches, each one probe longer: $504 \times 8 = 4{,}032$, about 2.28 times 1,769, so about 4.6 s."
- **Why?** Shown: "$n$ searches of about $\log_2 n$ steps make about $n \log_2 n$ probes." Then: "Doubling multiplies $n \log_2 n$ by $2(1 + 1/\log_2 n)$: 2.25 at 252 days, and closer to 2 as $n$ grows. This law is called **$n \log n$**; sorting by comparisons lives here (lesson 18)." `rep`: algebra (the product).
- **Solution:** the race plays lane C with probes per search; text: "Not four times: 2.28 times. A halving inner loop adds one step per doubling."
- **Tutor:** focus: "The decision point: does the inner loop grow or halve?" Notes: "If the learner chose 8 s, point at the `while` condition and ask how the gap between `lo` and `hi` changes each step." Reps: algebra (searches times steps); the race. Avoid: "logarithmic factor" before the Why.

#### Screen 7: `start-up` (`ladder`, the edge case, difficulty 2)

- **Skills:** `skl.alg.growth-law`.
- **Constraint added:** a cost that does not depend on the input.
- **Prose:** "A colleague times another backtest at 1, 2, 4 and 8 years. This table is constructed for the lesson."
- **Canvas:** `table`:

| Years | 1 | 2 | 4 | 8 |
|---|---|---|---|---|
| Seconds | 2.0 | 2.5 | 3.5 | 5.5 |

  `plot`, a `plot-2d` of seconds against years, hidden until Check.
- **Question:** "Which describes this program?"
- **Input:** `choice`: a "It grows more slowly than the data: the ratios 1.25, 1.4 and 1.57 are all below 2"; b "Linear, plus a fixed 1.5 s that does not depend on the years"; c "Logarithmic: each doubling adds about the same time"; d "Quadratic". **Check:** correct b.
- **Diagnose:**

| Option | Misconception | Feedback line | Show-why |
|---|---|---|---|
| a | `mc.alg.fixed-cost-sublinear` | "The ratios are climbing towards 2. Take away a fixed 1.5 s and the rest is 0.5, 1.0, 2.0 and 4.0: exact doubling." | The plot appears: a straight line meeting the time axis at 1.5 s; the fixed part shades grey |
| c | `mc.alg.log-doubles` | "A logarithmic program adds the same time per doubling. Here the additions are 0.5, 1.0 and 2.0 s, and they double." | The differences appear between columns |
| d | `mc.alg.square-for-all` | "Quadratic would multiply the growing part by 4 per doubling; it multiplies by 2." | Same |

- **Otherwise:** "Look at the differences between columns."
- **Reason:** "A fixed 1.5 s plus 0.5 s per year: linear, with the fixed part hiding it at small sizes."
- **Hints:** Nudge: "How much time does each doubling add?" Point: "The additions are 0.5, 1.0 and 2.0 s." (highlights the table's second row). Step: "Subtract 1.5 s from every time: 0.5, 1.0, 2.0, 4.0. That doubles, so the growing part is linear."
- **Why?** Shown: "Loading data and libraries costs the same whatever the input." Then: "Subtract the fixed part, or measure at sizes large enough that it stops mattering. Every honest benchmark in 1.9 does one of the two." `rep`: graph.
- **Solution:** the plot appears with its intercept; text: "A straight line that starts at 1.5 s: linear plus a fixed cost."
- **Tutor:** focus: "Fixed costs blur small-input ratios." Notes: "In the Artifact, Python itself takes about 3 seconds to start (`spikes/README.md`); learners who time their own code will meet this." Reps: graph; subtraction. Avoid: "intercept" unless the learner uses it.

#### Screen 8: `dedupe` (`trap`, difficulty 2)

- **Skills:** `skl.alg.hidden-scan`.
- **Trap:** `{ mc: mc.alg.one-loop-linear, bait: a }`.
- **Prose:** "A cleaning step removes repeated trade ids. On 20,000 trades it takes 1.1 seconds. Most people get the next question wrong."
- **Canvas:** `code`, a `code-tracer` in `hits` mode; before Check it shows the code only.

```python
seen = []
for t in trade_ids:
    if t not in seen:
        seen.append(t)
```

- **Question:** "How long on 40,000 trades, all ids different?"
- **Input:** `choice`: a "about 2.2 s"; b "about 4.4 s"; c "about 1.2 s"; d "about 8.8 s". **Check:** correct b.
- **Diagnose:**

| Option | Misconception | Feedback line | Show-why |
|---|---|---|---|
| a | `mc.alg.one-loop-linear` | "There is a second loop inside `not in`: it compares `t` with every id already in `seen`, and `seen` grows with the trades." | The tracer expands line 3 into a virtual inner loop [mode to add: hidden-scan hits] and shows its counts: 199,990,000 comparisons at 20,000 trades, 799,980,000 at 40,000 |
| c | `mc.alg.log-doubles` | "Nothing here halves. Every new id is checked against every id before it." | Same |
| d | `mc.alg.square-for-all` | "Eight times would need a third loop. Two loops, both growing with $n$, give four times." | Same |

- **On reveal:** the lesson player plays Bertie's `surprised` one-shot.
- **Reason:** "`not in` scans `seen`, so the cleaner compares every pair of ids: four times the work, about 4.4 s."
- **Hints:** Nudge: "What does `t not in seen` do, step by step?" Point: "1.1 lesson 28 timed this line." (highlights `code/line:3`). Step: "`not in` compares `t` with each id in `seen`. Over the whole run that is every pair of ids, version B's count, so the time quadruples."
- **Why?** Shown: "The cleaner makes $\frac{n(n-1)}{2}$ comparisons: the pair count again." Then: "On one machine it took 1.06 s and 4.88 s [measured], a little over 4 times because the bigger list fits the cache less well. With a `set`, each lookup is one step (lesson 25) and both sizes ran in under 0.01 s." `rep`: counting.
- **Solution:** the virtual inner loop plays; text: "One visible loop, one hidden one. Count the hidden one."
- **Recording:** a wrong first try on a trap is expected; a revealed trap screen is recorded but does not enter the Redo queue (`assessment.md` 2.2).
- **Tutor:** focus: "Built-in operations can hide a loop." Notes: "Learners who did 1.1 lesson 28 may get this right; ask them which other built-ins scan (`list.index`, `list.remove`, `insert(0, x)`)." Reps: counting; the grid from screen 3. Avoid: "hash" before lesson 25.

#### Screen 9: `rule` (`generalise`, difficulty 2)

- **Skills:** `skl.alg.growth-law`.
- **Rule (prose):** "You found the laws by doubling the input and dividing. One pass doubled the work. Every pair multiplied it by about 4. Halving added one step. A pass of halving searches grew a little more than 2 times. In general, work that grows like $n^k$ is multiplied by $2^k$ when $n$ doubles."
- **Card on the screen:**

| Doubling ratio, at large $n$ | Growth law | You saw it in |
|---|---|---|
| 1, plus one step | logarithmic | the halving loop |
| 2 | linear | version A; the fixed-cost table, once the fixed part is removed |
| a little over 2 | $n \log n$ | version C |
| 4 | quadratic | version B; the cleaner |
| 8 | cubic | this screen |

- **Questions and checks:**
  - Part 1 (the derived line): "Complete the line: if the work is $c\,n^k$, the doubling ratio is $\dfrac{c\,(2n)^k}{c\,n^k} = \square$." `expression`, equivalent to $2^k$.
  - Part 2: "A risk check compares every triple of days: 161,700 triples for 100 days and 1,313,400 for 200. Predict the count for 400 days." `numeric`, within 3% of 10,586,800 (so $8 \times 1{,}313{,}400 = 10{,}507{,}200$ is accepted).
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| Part 1: $2k$ | `slip` | "$(2n)^k$ is $2^k n^k$: the 2 is raised to the power $k$, not multiplied by it." | Expand $(2n)^3$ as $2n \cdot 2n \cdot 2n$ |
| Part 2: about 5,250,000 | `mc.alg.square-for-all` | "Triples, not pairs: each of three nested choices doubles, so $2^3 = 8$." | The card's cubic row highlights |
| Part 2: about 2,630,000 | `mc.alg.double-means-double` | "That doubles the triples. Triples grow like $n^3$." | Same |

- **Otherwise:** "Find $k$ for triples, then use the line you completed."
- **Reason:** "$2^k$; triples have $k = 3$, so about 8 times: about 10.5 million, and the exact count is 10,586,800."
- **Hints:** Nudge: "How many nested choices make a triple?" Point: "Use the cubic row of the card." Step: "Triples grow like $n^3$, so doubling multiplies by 8: $8 \times 1{,}313{,}400 \approx 10.5$ million."
- **Why?** Shown: "The ratio is $2^k$, so the ratio names $k$." Then: "This is how a timing table becomes a law: double, divide, read off $k$. Lesson 3 gives the law a name and a proof." `rep`: algebra.
- **Solution:** the line fills and the table's third column appears; text: "$2^k$; for triples, 8."
- **Tutor:** focus: "The rule is the learner's own steps, written once." Notes: "If the learner recites the card, ask them to predict the ratio for a loop over every set of four days (16)." Reps: algebra; the card. Avoid: logarithms of the ratio (lesson 7's `timing` mode).

#### Screen 10: `exact-ratio` (`derive`, difficulty 3)

- **Skills:** `skl.alg.doubling-ratio`.
- **Prose:** "Your ratios for version B were 4.667, 4.008 and 4.002, never exactly 4. Derive the exact ratio."
- **Canvas:** `derivation-steps` in fill mode:
  1. Given: "Pairs among $n$ days: $P(n) = \dfrac{n(n-1)}{2}$" (from screen 3's rows: $(n-1) + (n-2) + \dots + 1$).
  2. "Pairs among $2n$ days: $P(2n) = \square$" (learner fills).
  3. "Ratio: $\dfrac{P(2n)}{P(n)} = \square$" (learner fills).
  4. Shown after Check: "At $n = 4$: $\dfrac{2 \times 7}{3} = \dfrac{14}{3}$, the 4.667 you counted."
- **Checks:** line 2, `expression` equivalent to $n(2n - 1)$; line 3, `expression` equivalent to $\dfrac{2(2n-1)}{n-1}$; part 2, "What does the ratio approach as $n$ grows?" `numeric` 4.
- **Leap** (maths-teaching, "motivate the leap"): naive: "Pairs grow like $n^2$, so the ratio is exactly 4." Fails: "At 4 days you counted 28 over 6, which is 4.67." Points to: "Write the count exactly, replace $n$ by $2n$, then divide. The $-1$ terms explain the gap, and they matter less as $n$ grows."
- **Diagnose:**

| Learner state | Misconception | Feedback line | Show-why |
|---|---|---|---|
| Line 2 as $2 \cdot \frac{n(n-1)}{2}$ | `mc.alg.double-means-double` | "Replace every $n$ by $2n$, including the one inside $n - 1$." | Substitute $n = 4$: 28 pairs, not 12 |
| Line 2 as $4 \cdot \frac{n(n-1)}{2}$ | `mc.alg.exact-four` | "That assumes the answer. Replace $n$ by $2n$ inside the formula." | Substitute $n = 4$: 28, not 24 |
| Line 3 as 4 | `mc.alg.exact-four` | "Divide the two expressions; the $-1$ terms do not cancel." | Evaluate at $n = 4$ |

- **Otherwise:** "Substitute $2n$ for $n$ everywhere in line 1."
- **Reason:** "$P(2n) = n(2n - 1)$ and the ratio is $\frac{2(2n-1)}{n-1}$, which tends to 4."
- **Hints:** Nudge: "What do you get when you put $2n$ in place of $n$ in $\frac{n(n-1)}{2}$?" Point: "$\frac{2n(2n-1)}{2}$; now simplify and divide by line 1." (highlights line 2). Step: "$P(2n) = n(2n-1)$. Dividing by $\frac{n(n-1)}{2}$ gives $\frac{2(2n-1)}{n-1}$."
- **Why?** Shown: "$\dfrac{2(2n-1)}{n-1} = 4 + \dfrac{2}{n-1}$." Then: "The ratio sits above 4 by $\frac{2}{n-1}$: 0.67 at 4 days, 0.008 at 252, 0.002 at 1,000. The law is the limit; the small-$n$ gap is the edge case." `rep`: algebra.
- **Solution:** the lines fill in turn; text: "Exact ratio $4 + \frac{2}{n-1}$: above 4, and closer as $n$ grows."
- **Verification chain:** SymPy simplifies $\frac{P(2n)}{P(n)} - \left(4 + \frac{2}{n-1}\right)$ to 0; the values 14/3, 1,006/251 and 3,998/999 equal the hit-count ratios of screens 3 and 4.
- **Tutor:** focus: "Why the ratios were never exactly 4." Notes: "Learners who wrote $n^2$ for the pair count can still finish: $\frac{(2n)^2}{n^2} = 4$ exactly is the large-$n$ version, which is the point." Reps: algebra; the grid's new block. Avoid: "binomial coefficient" (0.3 named it; not needed here).

#### Screen 11: `universe` (`problem`, `context: quant`, the transfer, difficulty 2)

- **Skills:** `skl.alg.growth-law`.
- **Prose:** "A risk model computes the correlation of every pair of stocks over the same history. For 500 stocks it takes 0.5 seconds. The universe grows to 3,000 stocks."
- **Question:** "About how long for 3,000 stocks?"
- **Input:** `numeric-input`, seconds. **Check:** `numeric`, accepted 17 to 19 (the pair counts are 124,750 and 4,498,500, a ratio of 36.06, so 18.03 s).
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| 3 | `mc.alg.double-means-double` | "That scales the stocks by 6. The work counts pairs of stocks." | Show the two pair counts |
| 36 | `slip` | "36 is the ratio of the pair counts. Multiply the 0.5 s by it." | None |
| 1 to 1.5 | `mc.alg.log-doubles` | "Nothing halves here; every stock meets every other." | Show the pair counts |

- **Otherwise:** "Count pairs at both sizes, then scale the 0.5 s."
- **Reason:** "Six times the stocks gives about $6^2 = 36$ times the pairs: about 18 s."
- **Hints:** Nudge: "Is the work counted in stocks or in pairs of stocks?" Point: "Pairs grow like $n^2$, and $n$ grew 6 times." Step: "$6^2 = 36$; $0.5 \times 36 = 18$ s. The exact pair ratio is 36.06."
- **Why?** Shown: "Multiplying $n$ by $m$ multiplies an $n^2$ cost by about $m^2$." Then: "The doubling rule is the case $m = 2$. Real systems compute the whole matrix as one product (1.4 lesson 9), and the pairs are still there, inside it." `rep`: algebra.
- **Solution:** text: "124,750 pairs become 4,498,500: 36 times, so about 18 s."
- **Tutor:** focus: "The law transfers to any scale factor." Notes: "If asked about memory: the matrix of 3,000 by 3,000 doubles is 72 MB." Reps: algebra; the grid. Avoid: covariance estimation detail (1.6).

#### Screen 12: `summary`

- **Three ideas:**
  1. Double the input and divide the costs: the ratio, read at large $n$, names the growth law: 2 linear, 4 quadratic, 8 cubic, $2^k$ for $n^k$, one more step for logarithmic, a little over 2 for $n \log n$.
  2. Count every basic step, including the loops hidden inside built-ins such as `in` on a list.
  3. Small inputs and fixed start-up costs blur the ratio; read it where they no longer matter.
- **Notebook card** (`crd.alg.doubling`): "Doubling ratio $= \text{cost}(2n) / \text{cost}(n)$. One pass: 2. Every pair: $4 + \frac{2}{n-1}$, so 4. Triples: 8. $n^k$: $2^k$. Halving: plus one step. $n$ searches that halve: about $2(1 + 1/\log_2 n)$. Hidden scans: `x in list`, `list.index`, `list.remove`, `insert(0, x)`."
- **Common trap line:** "Twice the data is not always twice the time: one hidden scan inside a loop makes it four times."
- **Bertie:** `celebrate` when the lesson completes.

### 7.3 Lesson quiz (4 items, 1 mark each, no hints, one attempt, Why? after each)

| # | Item | Type, difficulty | Correct and accepted | Diagnosed wrong answers | Why? |
|---|---|---|---|---|---|
| 1 | "A function compares every pair of 1,000 prices: 499,500 comparisons. How many for 2,000 prices?" | Numeric (N), 2 | 1,999,000, exact | 999,000 (`mc.alg.double-means-double`: "That doubles the comparisons; pairs grow faster."); 1,998,000 (`mc.alg.exact-four`: "Close: the ratio is $4 + \frac{2}{999}$, not exactly 4. Count $\frac{2{,}000 \times 1{,}999}{2}$.") | "$\frac{2{,}000 \times 1{,}999}{2} = 1{,}999{,}000$, which is 4.002 times 499,500." |
| 2 | "A halving loop runs 20 times on $n = 1{,}000{,}000$. How many times on $n = 4{,}000{,}000$?" | Numeric (N), 2 | 22 | 80 (`mc.alg.square-for-all`); 40 (`mc.alg.log-doubles`); 21 (`slip`: "$n$ doubled twice, so two more steps.") | "Each doubling adds one halving: 4,000,000 is 1,000,000 doubled twice, so 22." |
| 3 | Sort four tables of operation counts at $n$, $2n$ and $4n$ into linear, quadratic, cubic and logarithmic: P 5,000, 10,000, 20,000; Q 4,950, 19,900, 79,800; R 7, 8, 9; S 19,600, 161,700, 1,313,400 | Sort (S), 3; the mark needs all four | P linear; Q quadratic; R logarithmic; S cubic | Q as cubic (`mc.alg.square-for-all`: "Q's ratios are about 4, not 8."); R as linear (`mc.alg.log-doubles`: "R adds one per doubling.") | "Ratios: P 2 and 2; Q 4.02 and 4.01; R plus 1 each time; S 8.25 and 8.12." |
| 4 | "A colleague times a script on 1,000 rows (1.2 s) and 2,000 rows (1.3 s), and concludes that 1,000,000 rows will take under 2 s. Best reply?" (a) "Agreed: a ratio of 1.08 shows logarithmic growth." (b) "Most of the 1.2 s may be fixed start-up; time larger sizes or count the steps before extrapolating." (c) "It will take $1{,}000 \times 1.2 = 1{,}200$ s, since the rows grow 1,000 times." (d) "It will take $1.2 \times 1{,}000^2$ s, since every script is quadratic." | Single choice (C), 3 | b | a (`mc.alg.fixed-cost-sublinear`); c (`mc.alg.double-means-double`: "That assumes linear growth and scales the fixed part too."); d (`mc.alg.square-for-all`) | "Two small timings cannot separate a fixed cost from growth. Measure at sizes where the growing part dominates, or count the steps." |

**Marks and mastery.** Each item scores 1 mark; 3 of 4 marks the lesson Mastered (`assessment.md` decision 26). Wrong items join the Redo queue at 7 and 30 days. One of the four items is single choice, within the 40% ceiling. Bertie is available on each item once it is graded, for Why? and "Explain another way".

### 7.4 Verification for this lesson

| Claim | Check |
|---|---|
| `backtest`: counts and times | Line-hit counts recorded for versions A, B and C at 252 and 504 days: 252 and 504; 31,626 and 126,756; 1,769 and 4,034 probes (the search stops when it finds the day). Ratios 2, 4.008 and 2.280, so 4.0 s, 8.0 s and 4.56 s at 2 s a year [verified] |
| `pair-grid`: the grid | 6 cells above the diagonal for 4 days and 28 for 8; $\frac{28}{6} = \frac{14}{3}$ [verified] |
| `ratio`: the table | Counts at 4, 8, 252, 504, 1,000 and 2,000 days equal $\frac{n(n-1)}{2}$; $\frac{1{,}999{,}000}{499{,}500} = \frac{3{,}998}{999}$ [verified] |
| `halving` | Recorded steps 8, 9 and 10 for 252, 504 and 1,008; equal to $\lfloor \log_2 n \rfloor + 1$ [verified] |
| `search-each` | 1,769 probes at 252 days and 4,034 at 504; $2(1 + 1/\log_2 252) = 2.2507$ [verified] |
| `start-up` | The constructed table equals $1.5 + 0.5 \times \text{years}$ exactly; its ratios are 1.25, 1.4 and 1.571 |
| `dedupe` | Comparisons for distinct ids equal $\frac{n(n-1)}{2}$: 199,990,000 at 20,000 and 799,980,000 at 40,000 [verified]; timings 1.06 s and 4.88 s on CPython 3.11, Intel Xeon 2.1 GHz, medians of 3 [measured]; the set version under 0.01 s at both sizes [measured] |
| `rule` | $\binom{100}{3} = 161{,}700$, $\binom{200}{3} = 1{,}313{,}400$, $\binom{400}{3} = 10{,}586{,}800$; $8 \times 1{,}313{,}400$ lies within 0.8% [verified] |
| `exact-ratio` | SymPy: $P(2n) = n(2n-1)$ and $\frac{P(2n)}{P(n)} = 4 + \frac{2}{n-1}$; values at $n$ = 4, 252 and 1,000 match the recorded ratios [verified] |
| `universe` | $\binom{500}{2} = 124{,}750$, $\binom{3{,}000}{2} = 4{,}498{,}500$, ratio 36.06, $0.5 \times 36.06 = 18.03$ [verified]; $3{,}000^2 \times 8$ bytes is 72 MB |
| Quiz | Item 1: $\binom{2{,}000}{2} = 1{,}999{,}000$; item 2: halvings of $10^6$ and $4 \times 10^6$ are 20 and 22; item 3: $\binom{100}{2}, \binom{200}{2}, \binom{400}{2}$ = 4,950, 19,900, 79,800; halvings of 100, 200, 400 = 7, 8, 9; $\binom{50}{3}, \binom{100}{3}, \binom{200}{3}$ = 19,600, 161,700, 1,313,400 [verified]. Every diagnosed wrong answer differs from the correct one and from the others |
| Tutor fields and copy | The leak lint finds no accepted value in any tutor field. Copy lints (sentence length, banned words, British spelling, no em-dashes); every code span parses as Python; embargoed terms absent before their introduction ("quadratic" first appears on screen 4, "$n \log n$" on screen 6) |

### 7.5 What this lesson asks of the widgets

| Widget | Ask | Why |
|---|---|---|
| `complexity-lab` | Race mode with three lanes (it has two) [mode to add] | Screen 2 compares three versions |
| `code-tracer` | `hits` mode that expands a built-in scan (`in`, `index`, `remove`, `insert(0, x)`) into a virtual inner loop with its comparison count [mode to add: hidden-scan] | Screen 8's show-why; reused by lessons 24, 28 of 1.1 and 57 |
| `cell-grid` | Paint restricted to cells above the diagonal, with a mirrored ghost for cells below | Screen 3; reused by two-pointer pair grids (lesson 30) |

---

## 8. Open items and requests to the other papers

**Owner decisions.**

| # | Decision | Options | Recommendation |
|---|---|---|---|
| 1 | Contest cadence against 2.4's hours (decision 18) | 30 rated contests and 3 Arena rounds in 140 hours; or about 190 hours for one contest a week | 140 hours and 30 contests: the curriculum's hours are its budget, and its cadence reads as a habit to aim at |
| 2 | `2.4.exit` (section 4.3) | Adopt the proposal; adopt with the rating as a developer-track confirm; leave 2.4 without an exit | Adopt as proposed; a rating cannot be read by the app and depends on other entrants |
| 3 | canon-gap O1 (2.4 at 60 hours outside the developer track) | Accept, with the 36-lesson core marked ◆; reject | Accept: the curriculum itself says a rating "counts for little in trader or researcher interviews" |

**Requests.**

| # | To | Request |
|---|---|---|
| 1 | `stage1-finance-projects.md` (1.7) | Keep `price_tree(S0, K, u, d, R, n, kind)` and `price_crr(S0, K, r, sigma, T, n, kind)` with `kind` in {'call', 'put'} and `ValueError` on the drill's invalid inputs: the 1.9 exit mirrors them in C++ and its checker recomputes CRR prices with the same parameters. Name the Pricing Lab's American function `crr_american(S0, K, r, sigma, T, n, kind)` so the C++ `american` flag maps to it |
| 2 | `assessment.md` 3.1 | Add paper kind `contest`: 120 minutes, problems A to F, ICPC scoring, `pass` read as problems solved over problems set, Bertie away, editorials after; resit rules as `topic` |
| 3 | `assessment.md` 2.10 | Add `'contest-upsolved'` to `log-count`'s enum; and a way to select an exit part by track (`tracks` on `ExitPart`), so `2.4.exit-core` can serve canon-gap O1's tracks; and an optional stage-level `headline` list of exit parts, so the Stage 1 page can show the map line's two bars first |
| 4 | `assessment.md` 2.9 | Row `1.8.exit`: name `pool.alg.timed` (40 mediums) and `estHours` 9; row `1.9.exit`: `estHours` 12 and the check details of section 4.4 |
| 5 | `widgets-programming.md` 6.11 | `exit-1.9`: the checks of section 4.4 (prices at three sizes recomputed, 7 repeats, Release build, no sanitisers); raise the `cpp-toolchain` floor to GCC 13 or Clang 17 (decision 11) |
| 6 | `widgets-programming.md` | Modes marked [mode to add]: `shortest-path` Floyd-Warshall; `pointer-walk` reach; `bit-lab` C++ precedence; `memory-layout` false sharing; `range-query-lab` sparse table; `tree-lab` Euler tour and binary lifting; `graph-search` SCC, bridges and 2-SAT; `number-theory-lab` CRT and Grundy values; `bench-lab` denormals; `mutant-hunter` C++; `complexity-lab` three-lane race; `code-tracer` hidden-scan hits; `cell-grid` triangle paint (section 7.5) |
| 7 | `widgets-programming.md` 9.1 | `contest-arena`: ICPC penalty of 20 minutes per rejected submission; the "solved" count as the paper score; web-only problems flagged on the rules screen |
| 8 | `content-format.md` | Register the `pool.*` id namespace if it is not already one (`pool.alg.timed`, `pool.alg.exam-*`, `pool.cpp.exam-*`), and the new source ids marked † in section 5 |
| 9 | `canon-gap.md` | Add `src.cppreference`, `src.cpp-core-guidelines`, `src.drepper-memory`, `src.carruth-cppcon-2014`, `src.kaggle`, `src.imc-prosperity`; confirm NeetCode 150's category counts (section 0.5 item 2) |
| 10 | Spikes (`spikes/README.md`) | W-B2: usable recursion depth of Pyodide on the reference phone (decision 25); Pyodide's speed against CPython, which scales contest time limits; W-C: the `cpp-runner` spike, which decides where 1.9 drills run |
| 11 | Content review | Confirm every [check] in sections 2 and 5: Grokking 2nd edition chapter numbers, 6.006 Spring 2020 lecture and problem-set numbers, learncpp chapter numbers, CPH chapter numbers, CS106L lecture titles, Drepper section numbers, the CMake default-build-type behaviour in lesson 70 |

**Not executed here** (section 0.6): LeetCode, Codeforces and CSES (no network use), doctest itself (tests were written as plain asserts), Pyodide (CPython 3.11 stood in), and the in-browser C++ paths.
