# Stage 0 detailed curriculum: 0.3 Precalculus, 0.4 Computer basics, 0.5 Mental arithmetic, and the Stage 0 exit test

Blueprint work file, Stage 2 Phase 1. Draft 2, 6 October 2026.

**Source of truth.** `docs/curriculum.md` for stages, topics, hours and exit tests. This file expands items 0.3 (200 h), 0.4 (40 h) and 0.5 (20 h) into courses, levels, lessons, homework, exams and reading, and rebuilds the Stage 0 exit test in the app.

**Draft 2** (same day) keeps every section number and every 0.3 lesson number of draft 1, because `ASSESSMENT.md`, `canon-gap.md`, `stage1-calculus.md`, `stage1-linear-algebra.md` and `stage1-probability.md` cite them (0.3 lessons 33 to 38, 59, 87 to 92, 98 to 106, 112, 116, 121, 135, 136, 142 and 144). It reconciles this file with what was written after draft 1: the final 0.1 and 0.2 lesson lists in `stage0-number-algebra.md`, against which seventeen 0.3 lessons repeated earlier teaching and now extend it instead; `ARCHITECTURE.md` (Pyodide on both targets, MicroPython dropped); `ASSESSMENT.md` draft 2 (the `topic` paper kind, Mastered at 75%); `CONTENT-FORMAT.md` revision 2 (tutor fields, element references, `needs`); `canon-gap.md` revision 2 (source ids, the 2026 Missing Semester); `BERTIE.md` (states and placements); and `spikes/README.md`. It also fixes a level that broke the 4-to-7-lesson rule. Section 0.6 lists every change and its reason.

> **Revision 2 of `docs/PLAN.md`, 7 October 2026: the Artifact publishing rule** (owner correction 5; added by the plan's second review round). These rows win over anything below that reads otherwise, the earlier review's rows included; content agents are briefed from them, and CI enforces them on the lesson files.
>
> | Where | Was | Now |
> |---|---|---|
> | The conflict with the brief; 0.1 decision 9; draft 2 change 2; 3.0, 3.2, 4.4, 6; open item 7 | Pyodide 314.0.7 on both targets; the standard library, NumPy and pandas in the Artifact; which further packages ship in the Artifact build left open | **No Python, SQL or C++ in the Artifact.** The Artifact publishes only files built from this repository's own sources (`docs/PLAN.md` 4.3), so no Pyodide, SQLite or compiler ships there. Every drill and every code item (K items, code screens, Labs, capstones, projects) runs in Pyodide 314.0.7 on the web app, or on CPython 3.12 on the learner's machine where this file says so; in the Artifact it shows its starter code, recorded output and the web-app link, and returns by result code (`docs/ASSESSMENT.md` 14.3). A lesson screen or quiz item whose widget runs learner code resolves as `read` in the Artifact and is finished in the web app (`docs/PLAN.md` 4.3, live-code screens). Lessons are otherwise unaffected: authored code runs at build time and ships as recorded output, and every number a widget shows comes from our own JavaScript models. Maths renders as MathML in the Artifact. Wherever this file says a drill, Lab, capstone, project or paper with code runs "on both targets" or "in the Artifact", or that Pyodide, NumPy or pandas run in the Artifact, read "in the web app"; the iPhone run of Pyodide inside an Artifact (`spikes/README.md`) is a record, not adopted, and where this file calls the brief's "Pyodide cannot run in the Artifact" a conflict, the brief's outcome now holds by the publishing rule |
> | Papers and exits | Drills and the Precalc Lab on both targets | **A paper with any code item is sat in the web app** (`docs/ASSESSMENT.md` 3.3; `docs/AI-TUTOR.md` 2.12); a paper whose items need no runtime (predicted output, recorded traces and outputs) plays on both targets. An exit part that needs a drill, Lab or capstone has that part done in the web app. Every 0.3, 0.4 and 0.5 homework drill, the 0.4 course Y code screens and the Precalc Lab (part 3 with NumPy and matplotlib included) run in the web app |
> | CI parity | CPython against Pyodide justified by "both targets run Pyodide" | **CI parity is CPython 3.12 (`tools/py/uv.lock`) against Pyodide 314.0.7 on the web app**: Pyodide grades every drill there, and CPython 3.12 is the learner's own floor, so any difference between them fails CI. Runs recorded on CPython 3.11 stand as records and are rerun at `docs/PLAN.md` stage 26 |
> | Open item 7 | Whether matplotlib ships in the Artifact build | **Closed by the rule**: nothing ships; Precalc Lab part 3 runs in the web app and returns by result code |

**Built on.** `docs/design-research.md` sections 5, 8 and 9 (lesson anatomy, curriculum architecture, teaching style); `docs/blueprint/work/widgets-stage0.md` (widget ids, generator families); `docs/blueprint/work/widgets-programming.md` (code widgets); `docs/blueprint/work/widgets-calc-linalg.md` (shared maths widgets); `docs/CONTENT-FORMAT.md` revision 2 (ids, screen types, checks, tutor fields, verification); `docs/ASSESSMENT.md` draft 2 (assessment ladder, homework, paper kinds, exit parts, the Daily 10); `docs/AI-TUTOR.md` (Bertie's availability and marking); `docs/ARCHITECTURE.md` (the Python runtime on both targets); `docs/BERTIE.md` (the mascot's states); `docs/blueprint/work/canon-gap.md` revision 2 (the resource canon and its `src.*` ids); `spikes/README.md`; the sibling file `docs/curriculum/stage0-number-algebra.md` (0.1 and 0.2, whose boundaries this file respects); the owner's lesson-creator, maths-teaching, code-craft and project-forge skills.

**Tags.** [our choice] marks a design decision. [check] marks a resource detail (a chapter number, a unit title, a lecture number, a paper code) that I recall but could not confirm from this environment; confirm it before the content cites it. [recalled] marks a platform fact from memory, not measured here. [measured] marks a fact read from a measurement recorded in this repository.

**Answers.** Every numeric answer in sections 2, 3, 4 and 7 was recomputed on 6 October 2026 with Python 3.11 and SymPy 1.14 (exact fractions, symbolic limits, sums and partial fractions, brute-force enumeration for counting); draft 2 re-ran the draft 1 checks and added the new items'.

**A conflict with the brief.** The brief for this file says Pyodide cannot run in the Artifact and that WebAssembly there was still being measured. `spikes/README.md` records both as measured on the owner's iPhone on 6 October 2026: every probe check passed except service workers, and a repackaged Pyodide 314.0.7 loaded NumPy and pandas and computed correctly [measured]. `ARCHITECTURE.md` decision 15 then put Pyodide on both targets and records the owner dropping MicroPython. This file follows the measurement and the owner's decision. The brief's fallback still holds for any device that cannot load Python: the drill hands off to the web app and returns by result code (`ASSESSMENT.md` 14.3).

**At a glance.**

| Item | Hours | Courses | Levels | Lessons | Lesson hours | Homework sets | Topic exam |
|---|---|---|---|---|---|---|---|
| 0.3 Precalculus | 200 | 5 | 29 | 146 | 36.5 (18.25%) | 29 | 90 min, 24 items, 80 marks, two timed sections (non-calculator, then calculator) |
| 0.4 Computer basics | 40 | 3 | 7 | 31 | 7.75 (19.4%) | 7 | None (ASSESSMENT.md 2.8); exit part `s0.script` closes it, after an ungated 30-minute practical rehearsal |
| 0.5 Mental arithmetic | 20 | 1 | 4 | 16 | 4.0 (20.0%) | 4 | None (ASSESSMENT.md 2.8); exit part `s0.zetamac` closes it, after an ungated benchmark sitting |
| Total | 260 | 9 | 40 | 193 | 48.25 | 40 | 1 |

Stage 0 exit test: four parts, rebuilt in section 4.4 (`s0.gcse`, `s0.precalc`, `s0.zetamac`, `s0.script`).

---

## 0. Scope, decisions and conventions

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Unit of lesson time | **15 minutes per lesson, quiz included**, the same unit as the 0.1 and 0.2 file | 10 or 12 minutes | One unit across Stage 0 keeps the hours tables comparable; design research 5.8 allows 10 to 15 minutes of screens and the quiz is part of the sitting |
| 2 | GCSE geometry and statistics | **Inside 0.3**: Shape and Space (course S, levels S1 to S5) before trigonometry, and Data and Statistics (level C5) beside probability. They cost about 40 of 0.3's 200 hours | Extra hours on top of Stage 0 (540 h); placing them in 0.2 | The GCSE exit paper weights Geometry and measures at about 20% and Probability and statistics at about 15% (ASSESSMENT.md 2.11); without them 80% is close to unreachable. The 0.1 and 0.2 file (draft 2) places them here too, pending the owner. Trigonometry and counting build on them, so 0.3 is their natural home. **Owner decision requested**: confirm, or move them and add 40 h to Stage 0 |
| 3 | Khan Academy Precalculus units outside the cover list | **Taught in 0.3**: matrices (T5), complex numbers in polar form (T6), rational functions in depth (R3), conic sections other than the circle (R4), limits and continuity (R5) | Changing the exit instrument to ignore those units | The exit is the Khan course challenge at 85%; its units are listed in ASSESSMENT.md 2.11 [sourced, secondary; check against the live course]. Rectangular complex numbers, rational functions and circles are already in 0.2 (sibling decisions 8 and 9), so 0.3 extends rather than repeats them |
| 4 | Courses for 0.3 | **Five courses**: S Shape and Space (38 lessons), G Growth (27), T Circles, Waves and Rotations (32), C Counting, Chance and Data (26), R Proof, Limits and Curves (23) | One course per cover-list word (six to nine thin courses); four courses | Design research 8.2 sets 20 to 45 lessons per course and sketches 1 to 4 courses per topic; this blueprint's brief allows 1 to 5, and no schema or CI rule caps the count (`Topic.courses` in CONTENT-FORMAT.md 3.2 has no maximum). Five keeps every course inside 20 to 45 lessons; four would push one past 45. Each course is one dependency chain with a single story |
| 5 | Course order | **S, G, T, C, R** | Curriculum cover-list order (exponentials first) | S finishes GCSE geometry and triangle trigonometry and gives vectors; G needs only 0.2's functions; T needs S (triangles, vectors), G ($e$, for Euler's formula) and 0.2's transformations; C is independent but its binomial and counting feed 1.5; R ends on limits because 1.3 Calculus is the next maths item in Stage 1 |
| 6 | Proof | **Logic, contrapositive, contradiction and induction in R1 and R2**, building on 0.1 (irrationality of $\sqrt{2}$, infinitely many primes) and 0.2 (algebraic proof) | Proof left to Stage 1 | The 18.01, 18.06 and Stat 110 finals in Stage 1 assume a learner can read and write a proof; induction proves the series formulas of G5 |
| 7 | Degrees and radians | **Degrees in course S** (GCSE convention); **radians from T1 onwards**, introduced as a lesson, and used in every calculus-facing item | Radians from the start | The GCSE paper is in degrees; calculus needs radians, and the switch deserves its own hook (lesson 66) |
| 8 | Calculators | Lesson screens mark calculator use per screen. Course S is taught for the non-calculator GCSE paper (exact values, estimation). The 0.3 topic exam has a non-calculator section A and a calculator section B | A calculator everywhere | The Stage 0 exit has one non-calculator paper and one challenge that allows a calculator [check Khan's calculator rule] |
| 9 | Code in 0.3 | **One code drill in every homework set**, standard library only (`math`, `fractions`, `itertools`, `random`, `statistics`, `cmath`), so every drill declares `needs: []` and runs under Pyodide in the web app (revision 2 header row); NumPy and matplotlib only in the Precalc Lab project's part 3 | No code until 1.1; NumPy from 0.3 onwards | 0.4 is finished by the time 0.3 starts (it runs alongside from week 1); checking maths in code is the habit 1.1 assumes. The standard library keeps the first Python load on a phone to the core and `stdlib` groups, and NumPy is 1.1's to teach |
| 10 | Terminal on Windows | **POSIX commands in `shell-sim`; Windows learners use PowerShell for the 0.4 exit**, whose aliases cover `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `rm` and `cat` (`ni` replaces `touch`) [recalled]; WSL2 waits for 1.2 | WSL2 now; Git Bash | WSL2 needs virtualisation and admin rights, a large first hurdle; the exit needs only a folder, a file and `python`. 1.2 (The Missing Semester) needs a real Unix shell and installs WSL2 there |
| 11 | Python version | **The current python.org release, minimum 3.12** (raised from 3.11 by the `docs/PLAN.md` review, conflict 19). At the time of writing that is 3.14: 3.15.0 was scheduled for 1 October 2026 (PEP 790), a third release candidate came out on 2 October, and the final release moved to 9 October 2026 [searched: python.org release page]; confirm which release is current when the lesson ships. The in-app runtime is Pyodide 314.0.7, which is Python 3.14.2 [measured: `spikes/README.md`] | Pinning one version | Matches `widgets-programming.md` decision 16: CI runs every reference solution on CPython 3.12 and on Pyodide's CPython, so whatever the learner installs runs the same code |
| 12 | Typing bar | **35 words per minute at 95% accuracy on prose, 25 on Python code text**, an outcome, not an exit gate | No bar; a gate | The curriculum names touch typing but sets no bar; the widget catalogue proposes 35 at 95% [our choice]. Code text is slower because of symbols |
| 13 | Zetamac format | **Defaults as recalled**: addition $(2..100) + (2..100)$, subtraction as addition reversed, multiplication $(2..12) \times (2..100)$, division as multiplication reversed, 120 seconds (addition, multiplication and the 120-second default confirmed by secondary sources, quant-preparation guides that describe the defaults [searched, secondary]; arithmetic.zetamac.com itself was not reachable from this environment, so subtraction and division as the reverses stay [check]; widgets-stage0.md 16.5) | Two-digit by two-digit products as the core | The exit is Zetamac on default settings, so 0.5 drills $12 \times 87$ and $1{,}044 \div 12$ first; two-digit by two-digit products follow for interviews |
| 14 | Topic exams for 0.4 and 0.5 | **None**, as ASSESSMENT.md 2.8 rules; each has an ungated rehearsal | A timed theory paper | Their curriculum exits are a practical and a score; a written paper would test the wrong thing |
| 15 | Stage 0 exit hours | **Charged to 0.3's exam block** (11.5 h includes the in-app GCSE-style paper, one real paper, the in-app challenge and the real Khan challenge) | A separate block | The curriculum's Stage 0 hours (500) are fully allocated to the five items; the exit is sat at the end of 0.3 |
| 16 | Sample lesson | **G lesson 49, "Logarithms count multiplications"** | Radians (lesson 66); the multiplication principle (lesson 98) | It is the concept the later path leans on most (log returns in 1.1 and 1.7, log-likelihood in 1.6, $O(\log n)$ in 1.8, log scales everywhere) and the one most often learnt as a rule without meaning |
| 17 | Overlap with 0.2 (new in draft 2) | **Where the final 0.2 lesson list teaches an idea, 0.3 extends it and never re-teaches it.** Seventeen draft 1 lessons changed, because 0.1 or 0.2 already teaches arithmetic $n$th terms, finite differences, cobwebs, exponential graphs and $y = Ab^x$ models, sigma linearity, the hole of a rational function, reading a log axis, fitting a line by eye, misleading charts, the complex plane's quarter turn, the $n^2 + n + 41$ counterexample and extraneous roots from squaring, and because four hooks or edges repeated 0.1 or 0.2 (section 0.2 lists each lesson with its new content). Lesson numbers are unchanged | Keeping the draft 1 lessons as recaps | A lesson the learner has already done is 15 minutes of the 200 hours spent twice, and a repeated hook kills the surprise a hook depends on (design research 9). Recaps happen anyway: level reviews draw 30% from earlier levels and the Redo queue returns misses |
| 18 | Level A4's size (new in draft 2) | **Four lessons**: a lesson on placing the decimal point in products and quotients joins A4, so 0.5 has 16 lessons (4.0 h, 20%) | Three lessons, as in draft 1 | Every level has 4 to 7 lessons (design research 8.2, and this blueprint's brief). The added lesson is also the commonest item type in the 80-in-8 test after the four operations ($0.3 \times 0.07$, $4.2 \div 0.06$) [recalled from interview reports] |
| 19 | 0.3 topic exam size (new in draft 2) | **80 marks in 90 minutes**, long-form items scaled from their 10-mark rubrics to 8 marks | Draft 1's 100 marks | The `topic` paper kind allows 40 to 80 marks (`ASSESSMENT.md` 3.1); the sibling 0.2 paper is 80 marks in 90 minutes and scales rubrics the same way |

### 0.2 What 0.3 inherits from 0.1 and 0.2, and does not repeat

Checked against the final lesson lists of `stage0-number-algebra.md` (0.1 lessons 1 to 42, 0.2 lessons 1 to 111). "0.1 lesson 26" means lesson 26 of item 0.1 in that file.

| Topic | Taught in | 0.3 does |
|---|---|---|
| Index laws, zero, negative and fractional indices | 0.1 lessons 32 to 34 | G2 lesson 44 extends them to real exponents |
| Compound interest with multipliers; +50% then −50% | 0.1 lesson 26 | G2 adds compounding frequency, effective rates and $e$; G4 lesson 57 opens on a four-year fund instead of the 0.1 hook |
| Recurring decimals to fractions | 0.1 lesson 23 | G5 lesson 63 proves the method with a geometric series |
| Fermi estimates, the geometric mean of bounds | 0.1 lesson 40 | G4 lesson 55 explains why the geometric mean is the midpoint on a log axis |
| Binary floating point | 0.1 lesson 42 | G4 lesson 59 adds underflow and log-sum-exp |
| $\sqrt{2}$ irrational, infinitely many primes | 0.1 lesson 41 and homework P4 | R1 adds contrapositive, quantifiers and $\log_2 3$ irrational |
| Product rule for counting; counting factors | 0.1 lesson 13 | C1 starts from permutations, recapping it in the hook |
| Sigma notation and $\sum (a x_i + b) = a\sum x_i + nb$ | 0.2 lesson 16 | G5 lesson 60 adds index shifts and double sums |
| Algebraic proof; the $n^2 + n + 41$ counterexample | 0.2 lesson 17 | R1 formalises logic; lesson 125 opens on the circle-regions pattern instead |
| Arithmetic sequences and the $n$th term | 0.2 lesson 41 | G1 lesson 39 recaps it as one case of explicit and recursive rules |
| Quadratic sequences by finite differences | 0.2 lesson 83 | Not repeated; G1 spends the lesson on two-term recurrences (lesson 42) |
| Midpoint and distance in the plane | 0.2 lesson 40 | S3 lesson 11 extends to three and $n$ dimensions |
| Fitting a line by eye, residuals; reading graphs critically, truncated and log axes | 0.2 lessons 46 and 47 | C5 lesson 122 spends its time on correlation and causation; lesson 123 on bias; G4 lesson 55 on computing with log axes |
| The mean minimises squared error; the sum-of-squares identity; AM-GM | 0.2 lessons 75 to 77 | C5 lesson 118 uses lesson 75 as its edge case |
| Rescaling data and standard scores | 0.2 lesson 105 | C5 assumes it |
| Function notation, domain, range, composition, inverses, even and odd functions, graph transformations | 0.2 lessons 88 to 92, 101 to 104 | Used throughout; inverse functions return as logs (G3) and inverse trig (T3); T1 lesson 69 applies parity to sine and cosine |
| Exponential graphs, $y = Ab^x$ models, linear against exponential growth | 0.2 lessons 97 and 98 | G2 lessons 44 and 45 start where they stop: what $b^x$ means between whole numbers, and converting rates between periods |
| Polynomial division, factor and remainder theorems, sum and product of roots | 0.2 lessons 69, 79, 80 | Used in R3 (oblique asymptotes) and T6 (complex roots) |
| Complex numbers in rectangular form; the complex plane; conjugate roots | 0.2 lessons 84 to 87 | T6 lesson 93 starts from distance on the Argand diagram (loci), then polar form, De Moivre, roots of unity, Euler preview |
| Reciprocal graphs; rational functions with vertical, horizontal asymptotes and holes | 0.2 lessons 95 and 99 | R3 lesson 133 adds oblique asymptotes, multiplicity and full sketches; then rational inequalities and partial fractions |
| Extraneous roots from squaring and clearing fractions | 0.2 lesson 111 | R1 lesson 128 uses a dissection paradox as its edge case instead |
| The circle and its tangent | 0.2 lesson 72 | S5 adds the circle theorems; R4 adds the other conics |
| Iteration and cobwebs; change of sign and bisection | 0.2 lessons 107 and 108 | G1 lesson 43 recaps the fixed-point test inside limits of sequences; R5 lesson 146 connects bisection to the intermediate value theorem |
| Gradient of a curve by shrinking chords; area by trapezia | 0.2 lessons 109 and 110 | R5 builds limits on lesson 109's $\frac{0}{0}$ |

### 0.3 Conventions for every lesson

**Ids** follow CONTENT-FORMAT.md section 4.1. Courses: `crs.shape`, `crs.growth`, `crs.waves`, `crs.chance`, `crs.rigour` (0.3); `crs.keys`, `crs.bench`, `crs.firstpy` (0.4); `crs.speed` (0.5). Levels `lvl.<course>.<slug>`, lessons `lsn.<course>.<slug>`, homework `set.<course>.<level-slug>`, topic exam `exm.pre.topic`. Libraries use the topic namespaces `pre` (0.3), `comp` (0.4) and `ment` (0.5): `skl.pre.*`, `mc.pre.*`, `gen.pre.*`, `drl.pre.*`. The `#` column is the lesson's number within its topic; display numbers are computed from position and never stored.

**Display codes.** Courses carry a letter that does not clash with 0.1 and 0.2 (W, P, E, L, Q, F): S Shape and Space, G Growth, T Circles, Waves and Rotations, C Counting, Chance and Data, R Proof, Limits and Curves; K Keyboard Fluency, B Workbench, Y First Programs in Python; A Arithmetic at Speed. Level T3 is the third level of course T.

**Every lesson** runs the design research 8.3 sequence: a hook on a canvas, free manipulation, the name for what the learner just did, a ladder of 2 to 4 screens adding one constraint each, the trap, the rule stated as a description of the learner's own steps with at least one derived line the learner completes, a transfer screen where a true quant, data or computing context exists, the summary card, then a quiz of 3 to 5 items. From the owner's skills, every lesson also carries the "why this exists" frame, one common trap, at least one edge case, a worked example with a decision point where the naive route fails, and a motivated leap wherever a creative step appears (`derive` screens carry `leap: naive, fails, pointsTo`).

**Widgets** use the ids in widgets-stage0.md section 14, with the primitive and input names of its 15.1 reconciliation, which CONTENT-FORMAT.md section 1 and the sibling file adopted: `choice`, `numeric-input`, `expression-input`, `derivation-steps`, `code-cell`, `value-table`, `region-select`, `drag-point`, `sketch-pad`. Composite ids are unchanged (`geometry-board`, `multiplier-chain`, `vector-plane`, `linear-map`, `matrix-grid`, `sign-chart` and the rest); where 15.1 folds a composite into a calculus counterpart (`vector-plane` into `vector-combo` and `projection-lab`, `linear-map` into `transform-grid`), the compiler's alias map applies and these plans do not change. From the other catalogues: `predict-output`, `parsons`, `code-tracer` and `diagnostic-reader` (widgets-programming.md) and `matrix-multiply`, `determinant-lab`, `series-explorer` and `limit-explorer` (widgets-calc-linalg.md).

**Quiz item types** (CONTENT-FORMAT.md 3.4 maps each letter to a check kind; the letters are shorthand in these documents and are never stored), the same letters as the 0.1 and 0.2 file plus five for this file's items: N numeric, X expression, C single choice, M multi-select, O order the steps, S sort or match, I interval or solution set, P point or curve on a graph, T predict the output of code; **A** matrix entry, **R** region or set selection on a canvas (grid cells, Venn regions), **K** code with tests, **H** shell or path task graded by its effect, **W** typed passage graded on speed and accuracy, **Z** timed speed set. R keeps its region meaning, as in `stage1-calculus.md` and `stage1-probability.md`; CONTENT-FORMAT.md 12.4 asks `stage1-python-tools.md` to move its result-table letter to Q. Long-form items appear in homework and exams, never in quizzes. Single and multiple choice stay at or below 40% of a course's quiz items (design research 10).

**Mastery and feedback.** A lesson is Mastered at 75% of its quiz marks on the first completion (ASSESSMENT.md decision 26): 3 of 4, 4 of 5. Every graded screen carries the CONTENT-FORMAT.md 3.3 feedback set: a `reason` line for a correct answer, `diagnose` lines tied to misconception ids, an `otherwise` line, the three-rung hint ladder (nudge, point, step), and a Why? of at most three sentences with its representation (`why.rep`). Every task screen carries `tutor.focus` (CONTENT-FORMAT.md 3.10), and no tutor field may contain a value the screen accepts. Hint and Why? highlights name elements as `<widget id>/<kind>:<name>` (CONTENT-FORMAT.md 3.5).

**Bertie** follows AI-TUTOR.md 2.2: hints and Bertie's lines open after the lesson's first Check, Why? and "Explain another way" after a screen is resolved, nothing on homework until the set is submitted, he is unavailable during the Daily 10 and every speed run, and `away` app-wide during every timed paper and while a homework item is open. On a trap screen's reveal the lesson player plays his `surprised` one-shot (BERTIE.md 5.3); energetic states never play during a problem.

**Level review.** Every level ends with a Level review of 8 items at difficulty 2 to 4, interleaved, with up to 30% drawn from earlier levels of the same course (ASSESSMENT.md 2.4). Homework follows (section 3).

**Columns.** Objective is one measurable sentence. Hook is the puzzle the lesson opens with. Trap is the misconception the trap screen is built around; Edge is the fringe case the lesson must show.

### 0.4 Summary of counts

| Item | Course | Code | Levels | Lessons | Lesson numbers |
|---|---|---|---|---|---|
| 0.3 | Shape and Space | S | 8 | 38 | 1 to 38 |
| 0.3 | Growth: Sequences, Series, Exponentials and Logarithms | G | 5 | 27 | 39 to 65 |
| 0.3 | Circles, Waves and Rotations | T | 6 | 32 | 66 to 97 |
| 0.3 | Counting, Chance and Data | C | 5 | 26 | 98 to 123 |
| 0.3 | Proof, Limits and Curves | R | 5 | 23 | 124 to 146 |
| 0.4 | Keyboard Fluency | K | 2 | 8 | 1 to 8 |
| 0.4 | Workbench: Files, Terminal and Editor | B | 3 | 13 | 9 to 21 |
| 0.4 | First Programs in Python | Y | 2 | 10 | 22 to 31 |
| 0.5 | Arithmetic at Speed | A | 4 | 16 | 1 to 16 |

### 0.5 Open items

| # | Item | Effect |
|---|---|---|
| 1 | Owner decision on GCSE geometry and statistics in 0.3 (decision 2; ASSESSMENT.md 18, item 15a) | If moved out, courses S1 to S5 and level C5 move with their 29 lessons, and 0.3 frees about 40 h |
| 2 | Owner decision on the Khan Academy units taught in 0.3 (decision 3; ASSESSMENT.md 18, item 15b) | If declined, levels T5, T6 (polar form), R3 (beyond 0.2), R4 (beyond the circle) and R5 move to 1.3 and 1.4 openings, and the `s0.precalc` gate loses those slots |
| 3 | Khan Academy Precalculus unit list, question count and calculator rule for the course challenge. Partly closed: the course description found by search names complex numbers, composite functions, trigonometric functions, vectors, matrices, conic sections, probability and combinatorics, and two optional units, series and limits and continuity (unit 10) [searched, secondary]; rational functions as a unit, the question count and the calculator rule remain [check] | Shapes `s0.precalc`'s blueprint (section 4.4); khanacademy.org itself was not reachable from this environment |
| 4 | Closed by search on 6 October 2026: GCSE Higher assessment objective weights are AO1 40%, AO2 30%, AO3 30% (AQA 8300 scheme of assessment and the boards' common weights [searched]); OCR's Higher non-calculator paper is J560/05 (Paper 5), 100 marks in 1 hour 30 minutes [searched: OCR examiners' reports and past papers] | Shapes `s0.gcse`; AQA and Edexcel Paper 1 at 80 marks in 90 minutes is sourced in ASSESSMENT.md 0.2 |
| 5 | Zetamac default ranges (decision 13) | Configuration only |
| 6 | The 0.4 homework drill slot before Python is taught (section 3.0) | ASSESSMENT.md 2.1 asks every homework for one code drill; sets K1, B1 and B2 come before any Python, so a state task graded by effect fills the slot. ASSESSMENT.md needs one line allowing it for 0.4 |
| 7 | **Closed by the publishing rule** (revision 2 header row). Was: whether matplotlib ships in the Artifact build | Nothing ships there: Precalc Lab part 3 runs in the web app and returns by result code |
| 8 | Automate the Boring Stuff edition: the 3rd edition (2025) splits the 2nd edition's first three chapters into four: 1 Python Basics, 2 if-else and Flow Control, 3 Loops, 4 Functions [searched: automatetheboringstuff.com/3e] | Section 5.2 cites the free 2nd edition's chapters 1 to 3; if the owner prefers the 3rd, its chapters 1 to 4 cover the same ground. Whether every 3rd-edition chapter is free to read online [check] |
| 9 | Resource details marked [check] in section 5 | Confirm before content cites them |

**Follow-ups for other files** (notes; this file edits none of them):

| File | Note |
|---|---|
| `stage0-number-algebra.md` 2.3, boundary with 0.3 | That table expects 0.3 lesson 41 to become a recap with practice time. Draft 2 here spends the quadratic-sequence lesson on new content instead: lesson 41 teaches first-order recurrences, lesson 42 two-term recurrences, and lesson 43 recaps cobwebs inside limits of sequences (section 0.2). Its request R6 is done: `gcse` questions 3 and 21 now cite 0.2 lessons 41, 43, 109 and 110 (section 4.4) |
| `stage1-python-tools.md` quiz letters | R means region selection in four curriculum files; the result table could become Q (CONTENT-FORMAT.md 12.4) |
| `ASSESSMENT.md` 2.1 | The homework rule "at least 1 code drill" needs an exception for 0.4 sets before Python (open item 6) |
| `CONTENT-FORMAT.md` 3.4 | The quiz-letter table can drop the R clash once `stage1-python-tools.md` moves to Q |
| `widgets-stage0.md` 5.9, 6.6 | `multiplier-chain` tile mode and the `graph-explorer` reflect toggle (section 7.5) |
| `widgets-stage0.md` 9.4, 9.13, 7.1 | `sequence-lab`: explicit and recursive views side by side, an index-origin toggle (lesson 39), a two-term mode with a ratio row (lesson 42) and a tolerance band (lesson 43). `complex-plane`: a locus tracer with region shading (lesson 93). `geometry-board`: points on a circle with a region counter (lesson 125) and a dissection preset for the $64 = 65$ paradox (lesson 128) |
| `ASSESSMENT.md` 18, item 15 | Open items 1 and 2 here are its items 15a and 15b |
| `stage0-number-algebra.md` 8, item O1 | "The schema's ceiling of 4 courses per topic" is design research 8.2's sketch, not a schema rule: `Topic.courses` has no maximum, and 0.3 has five courses under this blueprint's brief |

### 0.6 What draft 2 changed, and why

| # | Change | Sections | Source |
|---|---|---|---|
| 1 | **Seventeen 0.3 lessons stop repeating 0.1 and 0.2.** Lessons 39 and 41 to 45, 49 (its hook), 55, 57, 60, 93, 118, 122, 123, 125, 128, 133 and 143 now extend the earlier lesson instead of re-teaching it: two-term recurrences replace quadratic sequences, limits of sequences replace cobwebs, double sums replace sigma linearity, Argand loci replace the quarter turn, oblique asymptotes and multiplicity replace holes, and fresh hooks or edges replace four repeated ones. Lesson numbers, level codes and the cited lessons (33 to 38, 59, 87 to 92, 98 to 106, 112, 116, 121, 135, 136, 142, 144) are unchanged; five 0.3 lesson ids are new and `lsn.growth.recurrences` moves from lesson 42 to 41, none of them yet published | 0.1 decision 17, 0.2, 2.1, 3.1 (G1, R3), 5.1 | `stage0-number-algebra.md` lesson lists |
| 2 | **Python runs on Pyodide** (on the web app only since revision 2: header row). Every drill declares `needs: []` (standard library); Precalc Lab part 3 declares NumPy and matplotlib; MicroPython is gone | 0, 0.1 decision 9, 3.0, 3.2, 4.4, 6 | `ARCHITECTURE.md` decision 15; `ASSESSMENT.md` decision 30; `spikes/README.md` |
| 3 | **Level A4 has four lessons** (a decimal-point lesson joins it), so every level has 4 to 7; 0.5 has 16 lessons and its Daily 10 share falls by 15 minutes | 0.1 decision 18, 1.3, 2.3, 3.4 | The brief's level rule; design research 8.2 |
| 4 | **The 0.3 topic exam is 80 marks**, the `topic` kind's ceiling; long-form items scale to 8; the slot table was re-totalled by script | 0.1 decision 19, 4.1 | `ASSESSMENT.md` 3.1; the sibling's 0.2 paper |
| 5 | **Mastered at 75%**, the feedback fields, `tutor.focus` on every task screen, element references in `widget/kind:name` form, and Bertie's states | 0.3, 7 | `ASSESSMENT.md` decision 26; `CONTENT-FORMAT.md` 3.3, 3.5, 3.10; `AI-TUTOR.md` 2.2; `BERTIE.md` 5.3 |
| 6 | **Widget names follow the reconciliation** (`choice`, `numeric-input`, `expression-input`, `derivation-steps`, `code-cell`, `value-table`, `region-select`, `drag-point`, `sketch-pad`); composite ids unchanged | 0.3, 2 | `CONTENT-FORMAT.md` 1; the sibling file |
| 7 | **The sample lesson is rewritten to the revision 2 schema**: a paper-folding hook (draft 1's bacterium repeated 0.2 lesson 97's hook), course art in place of a Bertie prop, reason lines, `otherwise` lines, `why.rep`, solution lines, tutor blocks with no accepted value, Bertie's `surprised` on the trap reveal, a verification table and the widget requests it implies | 7 | `CONTENT-FORMAT.md` 3.3, 3.7, 3.10, 10; `BERTIE.md` 5.3, 7 |
| 8 | **Source ids, licences and companion hours** for the reading map; the 2026 Missing Semester as the 0.4 lecture parallel; A-level papers and the STEP Support Programme as problem and stretch rows; external 0.3 hours become 47.5 (practice 39.75) so that the per-level companion rule sums exactly | 1.1, 5 | `canon-gap.md` 6 and 8.3; `CONTENT-FORMAT.md` 3.8 |
| 9 | **A GCSE geometry, probability and statistics code map**, matching the sibling's map of Number, Algebra and Ratio | 2.1 | The sibling file's 2.3 |
| 10 | **0.4 homework drill slots before Python** are tasks graded by effect; K2 gains a transcribe-and-run code drill | 3.0, 3.3; open item 6 | `ASSESSMENT.md` 2.1 |
| 11 | **Boundary citations fixed**: `gcse` questions 3, 9, 10, 20, 21 and 25 cite 0.2 levels and lessons; the boundary open item is closed | 0.5, 4.4 | The sibling's request R6 |
| 12 | **Fixes**: lesson 45 now names the per-period conversion trap; the Kepler fit is reported as about 1.499 with its data source to confirm; the 0.5 benchmark is a `speed-drill` session, not an exam-engine paper, with a timed mixed set at the 20/50/20/10 mix | 2.1, 3.2, 4.3 | Re-runs on 6 October 2026; `ASSESSMENT.md` 3.1 |
| 13 | **Two discrepancies recorded rather than guessed**: ASSESSMENT.md 2.11's Khan unit list has polynomials where this file has trigonometry (section 4.4 gives the swap if the live course agrees with it); design research 8.2's "1 to 4 courses per topic" against this blueprint's brief of 1 to 5 (decision 4) | 0.1 decision 4, 4.4 | Re-reading the sources |

---

## 1. Item overview

### 1.1 0.3 Precalculus (200 h)

**Purpose in a quant or ML career.**

- **Logarithms and exponentials are the native language of finance and ML.** Prices compound, so returns are analysed as log returns, which add over time; volatility scales with $\sqrt{t}$; interest is quoted with compounding conventions that differ by market; likelihoods are products, so every fitting routine maximises a log-likelihood; cross-entropy loss is a log; algorithm costs are $O(\log n)$ and $O(n \log n)$. A researcher who cannot move between $e^x$, $\ln x$ and log scales without thinking is slowed at every step of 1.1, 1.6, 1.7, 1.8 and 2.1.
- **Series are pricing.** A bond, a mortgage, an annuity and a perpetuity are geometric series; present value is discounting term by term. The expected number of trials until a first success is $\sum k r^{k-1}$. Telescoping and index shifts recur in every probability and algorithm proof.
- **Counting is the first half of probability.** Interviews open with "how many ways" and "what is the chance" questions built on permutations, combinations, inclusion-exclusion, the pigeonhole principle and derangements. Binomial coefficients are the paths of a binomial option-pricing tree (1.7) and the probabilities of the binomial distribution (1.5).
- **Trigonometry, vectors, matrices and complex numbers are the doorway to linear algebra and signal processing.** The dot product is correlation and cosine similarity; a projection is the seed of least squares (1.4); a matrix is a linear map; a determinant is an area scale factor; $e^{i\theta}$ powers Fourier analysis and characteristic functions; sinusoids model seasonality (2.2). The cosine rule has the same shape as the variance of a two-asset portfolio.
- **Proof and limits make Stage 1 readable.** MIT 18.01 and 18.06 and Harvard Stat 110 finals expect proofs by induction and contradiction and a working idea of a limit.
- **The GCSE content closes the Stage 0 exit.** Geometry, measures and statistics are 35% of a GCSE Higher paper.

**Learning outcomes.** At the end of 0.3 the learner can:

| # | Outcome | Measured by |
|---|---|---|
| P-O1 | Find unknown angles and lengths using angle facts, polygon sums, circle theorems, congruence and similarity, giving a named reason for every step | 85% on fresh difficulty-3 items; the geometry part of the GCSE-style paper at 80% |
| P-O2 | Compute perimeters, areas, surface areas and volumes of circles, sectors, prisms, cylinders, pyramids, cones, spheres and frustums, and apply length, area and volume scale factors | 85% on difficulty-3 items |
| P-O3 | Solve right-angled and general triangles (trigonometric ratios, exact values, the sine and cosine rules including the ambiguous case, $\tfrac{1}{2}ab\sin C$, 3D problems), and derive the exact values and both rules | 85% on difficulty-3 items; derivations at 7 of 10 on the rubric |
| P-O4 | Use vectors in two and three dimensions: arithmetic, geometric proof, magnitude and direction, the dot product, projections and cosine similarity | 85% on difficulty-3 items; vector proof at 7 of 10 |
| P-O5 | Move between explicit and recursive rules for sequences, solve first-order recurrences by their fixed point and two-term linear recurrences by their characteristic equation, decide convergence and find limits of sequences, and sum arithmetic, geometric, telescoping, double and arithmetico-geometric sums, including sums to infinity with their convergence condition | 85% on difficulty-3 items; the Fibonacci closed form at 7 of 10 |
| P-O6 | Model with exponentials and logarithms: growth and decay rates, half-lives, compounding frequency, $e$ and continuous growth, the log laws, change of base, exponential equations, log scales, linearisation, simple against log returns | 85% on difficulty-3 items; Precalc Lab part 3 tests pass |
| P-O7 | Price cash flows: present value, annuities, perpetuities and loan payments | 85% on difficulty-3 items; Precalc Lab part 1 tests pass |
| P-O8 | Evaluate, graph, transform and model trigonometric functions in radians; prove identities; solve equations in a range; use compound-angle, double-angle and $R\sin(x + \alpha)$ forms and small-angle approximations | 85% on difficulty-3 items; identity proofs at 7 of 10 |
| P-O9 | Multiply, invert and interpret $2 \times 2$ matrices as transformations, compute determinants as signed area scale factors, and solve $2 \times 2$ systems | 85% on difficulty-3 items |
| P-O10 | Sketch loci and regions on the Argand diagram, and work with complex numbers in modulus-argument form: multiply and divide, apply De Moivre's theorem, find roots of unity, and explain $e^{i\theta}$ as rotation | 85% on difficulty-3 items |
| P-O11 | Count arrangements and selections (permutations, combinations, repeated objects, circular arrangements, restrictions, stars and bars, inclusion-exclusion, the pigeonhole principle, derangements) and choose the model from the wording | 85% on difficulty-3 items; both difficulty-5 items of homework C2 correct |
| P-O12 | Expand $(a + b)^n$, find any coefficient, prove binomial identities by counting, and use the binomial series for small-$x$ approximations with its validity condition | 85% on difficulty-3 items |
| P-O13 | Compute probabilities with sample spaces, Venn diagrams, tree diagrams and counting, including conditional probability and sampling without replacement | 85% on difficulty-3 items |
| P-O14 | Summarise and compare data with averages, spread, cumulative frequency, box plots, histograms with unequal widths and scatter graphs, and critique samples and charts | 85% on difficulty-3 items; the statistics part of the GCSE-style paper at 80% |
| P-O15 | Write proofs by direct argument, cases, contrapositive, contradiction and induction, and locate the flaw in a broken proof | 7 of 10 on rubric items in homework R1 and R2 and exam item B11 |
| P-O16 | Sketch rational functions from their intercepts, vertical and oblique asymptotes and the multiplicity of each factor, solve rational inequalities with sign charts, decompose into partial fractions and sum telescoping series | 85% on difficulty-3 items |
| P-O17 | Derive conics from focus-directrix and two-focus definitions, put second-degree equations into standard form, and work with parametric curves | 85% on difficulty-3 items |
| P-O18 | Evaluate limits from tables, graphs and algebra, including one-sided limits and limits at infinity, and use continuity and the intermediate value theorem | 85% on difficulty-3 items |

**Prerequisites.** 0.1 and 0.2 complete, especially 0.1 level P3 (powers and roots), 0.2 course F (functions, inverses, transformations), course Q (quadratics, polynomials, complex numbers in rectangular form) and lesson 16 (sigma notation). 0.4 complete for the code drills (variables, `if`, `for`, `while`, functions). 0.5 alongside as the Daily 10.

**Hours budget (200 h).**

| Block | What | Hours | Share |
|---|---|---|---|
| In-app lessons | 146 lessons at 15 minutes, quiz included | 36.5 | 18.25% |
| In-app practice and redo | Generated practice, 29 level reviews (about 15 minutes each, 7.25 h), Redo queue at 7 and 30 days | 39.75 | 19.9% |
| Homework | 29 sets at about 1 hour 45 minutes | 50.75 | 25.4% |
| Exams | Two practice topic papers (90 min each), the topic exam (90 min), the in-app Precalculus challenge (60 min) and the real Khan course challenge (about 60 min [check]), the in-app GCSE-style paper and one real GCSE Higher Paper 1 (90 min each), marking and review (2 h) | 11.5 | 5.75% |
| External reading and lectures | The levels' companion work (section 5.0): videos and reading 18.0 h; external problem sets 29.5 h (Khan unit exercises and unit tests, OpenStax section exercises, Corbettmaths exercises, TLMaths exam questions and A-level Pure past-paper questions, Stat 110 Strategic Practice 1; Underground Mathematics, Isaac Maths and the STEP Support Programme foundation modules for stretch) | 47.5 | 23.75% |
| Projects or drills | Precalc Lab project in three parts (10 h, section 3.2); 8 extra code drills of 30 minutes beyond homework (4 h) | 14.0 | 7.0% |
| **Total** | | **200.0** | 100% |

Solving time (everything except the 18 hours of videos and reading) is 182 hours, 91%, above the curriculum's 60% floor. About 40 of the 200 hours are GCSE-only content (S1 to S5 and C5, 29 lessons and their homework), which is decision 2.

### 1.2 0.4 Computer basics (40 h)

**Purpose in a quant or ML career.**

- **Every later item is done at a keyboard.** Code, notes, queries and interview take-homes are typed. At 15 words per minute a 30-minute coding interview loses a third of its time to the keys; at 40 words per minute with correct symbols, attention goes to the problem.
- **The file system and the terminal are where data and code live.** Research means files of prices, scripts, results and logs, organised so that a run can be repeated. Every quant tool (Git, Python environments, compilers, cloud machines, schedulers) is driven from a terminal; 1.2 assumes it.
- **Installing software safely is a skill.** Wrong Python versions, a PATH that points somewhere else and code run from the wrong folder cause most beginner failures in 1.1. Diagnosing them is taught here, once, properly.
- **A first program is the start of checking maths in code.** From 0.1 onwards every homework set has a small code drill; 0.4 supplies the Python that makes those drills possible.

**Learning outcomes.**

| # | Outcome | Measured by |
|---|---|---|
| C-O1 | Touch type at 35 words per minute with 95% accuracy on unseen prose and 25 words per minute on Python code text, without looking at the keys | `typing-trainer` benchmark: median of three 2-minute runs |
| C-O2 | Use the editing shortcuts of their operating system (copy, cut, paste, undo, redo, select all, save, find, word-wise movement and selection) | Shortcut drill at 90% within the time limit |
| C-O3 | Explain files, extensions, folders, and absolute and relative paths, and organise a project folder with names that work in a terminal | Quiz items at 80%; homework B1 |
| C-O4 | Navigate, create, copy, move and delete with `pwd`, `ls`, `cd`, `mkdir`, `touch`, `cp`, `mv`, `rm`, read help, reuse history, and use wildcards, redirection and pipes | Shell tasks graded by effect at 90% |
| C-O5 | Install Python (3.12 or later) and VS Code from official sources, verify the versions from a terminal, and diagnose "command not found" | `setup-checklist` paste-verify |
| C-O6 | Write and run Python scripts using expressions, types, variables, `input` and `print`, `if`, `for`, `while`, functions and `try`/`except`, and read a traceback from the bottom up | Code drills with hidden tests at 80% |
| C-O7 | Make a folder, write a ten-line Python script in it and run it from the terminal | Exit part `s0.script` (section 4.4) |

**Prerequisites.** None beyond the curriculum's zero. 0.4 runs alongside 0.1 from the first week. Courses K and B need nothing; course Y assumes 0.1's level W2 (negatives) for its arithmetic examples.

**Hours budget (40 h).**

| Block | What | Hours | Share |
|---|---|---|---|
| In-app lessons | 31 lessons at 15 minutes, quiz included | 7.75 | 19.4% |
| In-app practice and redo | `typing-trainer` sessions (40 of 15 minutes, 10 h; keybr.com sessions logged count the same), shell and code practice (2 h), 7 level reviews (1.75 h) | 13.75 | 34.4% |
| Homework | 7 sets at about 45 minutes | 5.25 | 13.1% |
| Exams and exit | Typing benchmark (15 min), the practical rehearsal (30 min), the `s0.script` exit on the learner's own machine (30 min) | 1.25 | 3.1% |
| External reading and lectures | Automate the Boring Stuff introduction and chapters 1 to 3, typing every example (4 h, or CS50P lectures 0 to 3 in its place); The Missing Semester (2026) lecture 1 (1 h); The Linux Command Line chapters 1 to 4 (1.5 h) | 6.5 | 16.3% |
| Projects or drills | Three mini-projects on the learner's own machine: organise a study folder from the terminal (1.5 h), a bill-splitter script (2 h), a times-table quiz script that feeds 0.5 (2 h) | 5.5 | 13.8% |
| **Total** | | **40.0** | 100% |

Solving and practising time is 33.5 hours, 84%.

### 1.3 0.5 Mental arithmetic (20 h)

**Purpose in a quant or ML career.**

- **It is tested directly.** Trading firms screen with timed arithmetic: Zetamac-style runs and 80 questions in 8 minutes (curriculum 3.3; ASSESSMENT.md decision 16). The Stage 0 bar is 25 on Zetamac; Stage 3 asks for 50.
- **It is tested indirectly in every live round.** Market-making games, expected-value bets and probability questions are answered aloud; slow arithmetic loses the thread and the interviewer's confidence.
- **It is a sanity check on every model.** A researcher who can multiply and estimate in the head notices a P&L, a volatility or a latency that is wrong by a factor of 10 before the meeting ends.

**Learning outcomes.**

| # | Outcome | Measured by |
|---|---|---|
| M-O1 | Recall every product up to $12 \times 12$ within 2 seconds at 98% accuracy | `speed-drill` fact model: every fact's median time under 2 s over the last 14 days |
| M-O2 | Add and subtract two-digit numbers within 3 seconds and three-digit numbers within 6 seconds, using left-to-right addition, compensation and counting up | Timed decks at 95% accuracy |
| M-O3 | Multiply a number from 2 to 12 by a number from 2 to 100 within 4 seconds, divide the reverse within 4 seconds, and multiply two two-digit numbers within 10 seconds | Timed decks at 95% accuracy |
| M-O4 | Convert fractions with denominators up to 12 to three decimal places within 3 seconds, place the decimal point in products and quotients of decimals within 4 seconds, compute percentages and percentage changes, and estimate products and quotients within 10% | Timed decks at 90% accuracy |
| M-O5 | Explain every shortcut used as an algebraic identity | Long-form items at 7 of 10 |
| M-O6 | Score 25 or more on Zetamac default settings | Exit part `s0.zetamac` (section 4.4) |

**Prerequisites.** 0.1 level W1 (place value) by lesson 3; 0.2 lesson 10 (special products) before A3 lessons 11 and 12; 0.1 level W4 (fractions) and level P1 (decimals and percentages) before level A4. 0.5 runs alongside from the first week; its lessons are released in step with 0.1 and 0.2, so a strategy never arrives before the number sense or identity it rests on.

**Hours budget (20 h).**

| Block | What | Hours | Share |
|---|---|---|---|
| In-app lessons | 16 lessons at 15 minutes, quiz included | 4.0 | 20.0% |
| In-app practice and redo | The Daily 10 (ASSESSMENT.md section 9): 66 days of 10 minutes | 11.0 | 55.0% |
| Homework | 4 sets at about 30 minutes | 2.0 | 10.0% |
| Exams and exit | A 30-minute benchmark sitting: three cold runs and a preview of the 80-in-8 format; the 7-day exit window itself sits inside the Daily 10 | 0.5 | 2.5% |
| External reading and lectures | Benjamin and Shermer, Secrets of Mental Math, chapters 1 to 4 (1.5 h) | 1.5 | 7.5% |
| Projects or drills | A personal drill script in Python (from 0.4 level Y2), and 10 logged runs on the real Zetamac site | 1.0 | 5.0% |
| **Total** | | **20.0** | 100% |

After these 20 hours the Daily 10 continues as the Mental block of every weekly plan (ASSESSMENT.md decision 13); those minutes belong to the later items' plans, not to 0.5.

---
## 2. Courses

### 2.1 Item 0.3 Precalculus

#### Course S: Shape and Space (`crs.shape`, 8 levels, 38 lessons)

The geometry a GCSE Higher paper tests, rebuilt from reasons rather than rules, then the trigonometry of triangles and the vectors that carry it into linear algebra. Every angle is found with a named reason, every formula is derived by cutting, sliding or similarity, and every level ends with something a quant uses: Euclidean distance, decision boundaries, the cosine rule as portfolio variance, cosine similarity.

**Level S1: Angles and polygons** (`lvl.shape.angles`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | `lsn.shape.angle-facts` Angle facts and parallel lines | Find unknown angles using angles on a line, at a point and vertically opposite, and alternate, corresponding and co-interior angles, naming the reason for each step | Two parallel rails, one slanted bar, one angle marked $63°$. How many of the other seven angles can you fill in without measuring? | `geometry-board` (parallel-lines preset; drag the transversal), `numeric-input`, `card-sort` | Trap: "alternate angles are equal" used when the lines are not parallel. Edge: co-interior angles add to $180°$; they are equal only when both are $90°$ | N, N, S, C |
| 2 | `lsn.shape.triangle-sum` Why a triangle's angles make $180°$ | Prove the angle sum of a triangle with a line through one vertex parallel to the opposite side, and use it with the exterior-angle theorem | Tear the three corners off a paper triangle and line them up: a straight line. Every time? | `geometry-board` (drag vertices; live angle readouts), `derivation-steps` | Trap: "I measured five triangles" offered as proof. Edge: on a sphere a triangle with a vertex at the North Pole and two on the equator has three right angles, so the proof must use the parallel line, which a sphere does not have | N, O, N, C |
| 3 | `lsn.shape.polygons` Polygons: interior and exterior angles, quadrilaterals | Derive the interior sum $(n - 2) \times 180°$ and the exterior sum $360°$, solve for $n$ from a regular polygon's angle, and classify quadrilaterals by sides, angles and diagonals | Walk round a pentagon-shaped park, turning at each corner. How far have you turned when you are back at the start? | `geometry-board` (polygon walk with turning arrows), `numeric-input`, `card-sort` | Trap: $n \times 180°$; dividing the interior sum by $n$ for an irregular polygon. Edge: no regular polygon has exterior angle $25°$, because $360 \div 25$ is not whole; a reflex corner turns the walker backwards, a negative exterior angle | N, N, S, N |
| 4 | `lsn.shape.bearings` Bearings | Give and use three-figure bearings, find back bearings, and combine bearings with parallel-line facts | A ship sails from A to B on a bearing of $070°$. What bearing takes it straight back? | `geometry-board` (north lines, compass rose), `numeric-input`, `drag-point` | Trap: measuring anticlockwise, or from the north line at the wrong point. Edge: the back bearing is the bearing plus or minus $180°$, whichever stays in $000°$ to $360°$ | N, N, P, C |

Transfer screens: none forced. This level serves the GCSE paper and the trigonometry of S6 and S7.

**Level S2: Area and volume** (`lvl.shape.measure`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 5 | `lsn.shape.area-rearrange` Area by cutting and rearranging | Derive the areas of the parallelogram, triangle and trapezium by dissection and use them for compound shapes | A parallelogram and a rectangle share a base and a height. Which has more area? Cut one and slide | `geometry-board` (cut and slide), `numeric-input`, `expression-input` | Trap: the slant side used as the height. Edge: a parallelogram sheared far over needs several cuts, yet its area never changes (Cavalieri's principle, met again in 1.3) | N, N, X, C |
| 6 | `lsn.shape.circles` Circles: $\pi$, circumference and area | Define $\pi$ as circumference over diameter, derive $A = \pi r^2$ by unrolling sectors into a near-rectangle, and give exact answers in terms of $\pi$ | How many diameters fit round a circle's edge? Roll a wheel one turn and count | `geometry-board` (rolling circle; sector rearrangement with a sector-count slider), `expression-input` | Trap: radius and diameter swapped; $(2r)^2$ for $2r^2$. Edge: doubling the radius doubles the circumference but quadruples the area | X, N, C, N |
| 7 | `lsn.shape.arcs-sectors` Arcs and sectors | Compute arc lengths, sector areas and sector perimeters as fractions of a circle, and work backwards to an angle or a radius | A $40°$ slice of a 30 cm pizza: how long is its crust? | `geometry-board` (sector with angle and radius sliders), `numeric-input` | Trap: a sector's perimeter without its two radii. Edge: a reflex sector (more than half the pizza) uses the same fraction | N, N, X, N |
| 8 | `lsn.shape.prisms` Prisms, cylinders, nets, plans and elevations | Compute volumes as cross-section times length and surface areas from nets, and draw plans and elevations of solids | Two cans: one twice as tall, one twice as wide. Which holds more? | `solid-viewer` (unfold to a net; plan and elevation views), `numeric-input` | Trap: doubling the radius doubles the volume (it quadruples it). Edge: $1\text{ m}^3 = 1{,}000{,}000\text{ cm}^3$, not 100 | N, N, C, P |
| 9 | `lsn.shape.cones-spheres` Pyramids, cones, spheres and frustums | Use $V = \tfrac{1}{3}Ah$ for pyramids and cones and the sphere formulas, and find frustum volumes as a large cone minus a similar small one | How many cones of water fill a cylinder with the same base and height? | `solid-viewer` (pour animation; three pyramids filling a cube), `numeric-input` | Trap: slant height used in the volume; the diameter used in the sphere formula. Edge: three congruent square pyramids assemble into a cube, which is why the $\tfrac{1}{3}$ is exact | N, N, N, C |

Transfer screens: lesson 8 sizes a storage tank; lesson 9 asks how much a 10% larger ball weighs (scale factor $1.1^3 = 1.331$).

**Level S3: Pythagoras, congruence and similarity** (`lvl.shape.triangles`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 10 | `lsn.shape.pythagoras` Pythagoras' theorem | Prove $a^2 + b^2 = c^2$ by rearranging four copies of a right triangle in a square, and use the theorem and its converse to find lengths and test for right angles | A tilted square sits inside a $7 \times 7$ square, leaving four triangles with legs 3 and 4. What is the tilted square's area? | `geometry-board` (four-triangle rearrangement), `derivation-steps`, `numeric-input` | Trap: adding the squares when finding a shorter side; applying it to a triangle with no right angle. Edge: triples such as $(5, 12, 13)$ and their multiples; the converse decides right angles | N, N, C, O |
| 11 | `lsn.shape.distance-3d` Distance in coordinates and in three dimensions | Extend 0.2 lesson 40's distance formula to three dimensions and to the space diagonal of a cuboid by applying Pythagoras twice, then to $n$ coordinates | Will a 1.2 m umbrella fit inside a closed $1.0 \times 0.6 \times 0.3$ m box? (Not lying on the base, whose diagonal is about 1.166 m; only corner to corner, about 1.204 m) | `solid-viewer`, `vector-plane` (coordinate mode), `numeric-input` | Trap: the face diagonal taken as the answer; adding lengths instead of squares. Edge: $\sqrt{a^2 + b^2 + c^2}$ extends to any number of dimensions, the Euclidean distance between data points | N, N, X, N |
| 12 | `lsn.shape.congruence` Congruent triangles | Decide congruence with SSS, SAS, ASA or AAS and RHS, and show with a construction why SSA fails | Given two sides and a non-included angle, build a triangle. Can you build two different ones? | `geometry-board` (rigid rods and a hinge), `card-sort`, `derivation-steps` | Trap: AAA treated as congruence (it gives similarity only); SSA accepted. Edge: SSA does fix the triangle when the given angle is a right angle (that is RHS) or when the side opposite it is the longer given side | S, C, M, O |
| 13 | `lsn.shape.similarity` Similar shapes and scale factors | Identify similar triangles by equal angles, find the scale factor and use it for missing lengths, including nested triangles | A 1.8 m person casts a 2.4 m shadow when a tree casts a 16 m shadow. How tall is the tree? | `geometry-board` (linked enlargement), `double-number-line`, `numeric-input` | Trap: additive reasoning ("the tree's shadow is 13.6 m longer, so the tree is 13.6 m taller": 15.4 m instead of 12 m); matching non-corresponding sides. Edge: all circles are similar, but not all rectangles; nested triangles share an angle, so the sides to match are whole sides, not pieces | N, N, C, N |
| 14 | `lsn.shape.area-volume-scale` Area and volume scale factors | Apply $k$, $k^2$ and $k^3$ to lengths, areas and volumes, and work backwards from an area or volume ratio to a length ratio | A 1:20 model car needs 5 ml of paint. How much does the real car need? | `solid-viewer` (scaling with unit cubes), `numeric-input` | Trap: using $k$ for area or volume (100 ml instead of 2 litres). Edge: an area ratio of $9 : 16$ means lengths $3 : 4$ and volumes $27 : 64$; unit conversion $1\text{ m}^2 = 10{,}000\text{ cm}^2$ is the same idea | N, N, N, C |

Transfer screens: lesson 11 computes the Euclidean distance between two customers described by three features, the measure behind nearest-neighbour methods (2.1).

**Level S4: Transformations and constructions** (`lvl.shape.transform`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 15 | `lsn.shape.isometries` Translations, reflections and rotations | Perform and fully describe translations by a vector, reflections in a line and rotations by centre, angle and direction | Shape A lands exactly on shape B. Find one move that does it | `geometry-board` (transform tools), `vector-plane` (lattice), `choice` | Trap: a rotation described without its centre; reflecting in $y = x$ by negating instead of swapping. Edge: two reflections in parallel lines make a translation; in crossing lines, a rotation | S, P, C, N |
| 16 | `lsn.shape.enlargement` Enlargement, including fractional and negative scale factors | Enlarge a shape from a centre by any scale factor and find the centre and scale factor of a given enlargement | Shine a torch through a cut-out onto a wall. What happens to the shadow as the torch moves? | `geometry-board` (rays from the centre; scale slider from $-3$ to $3$) | Trap: measuring from the origin instead of the given centre; "scale factor $\tfrac{1}{2}$ makes it bigger". Edge: scale factor $-1$ is a rotation of $180°$; angles never change, lengths multiply by $\lvert k \rvert$ | P, N, C, P |
| 17 | `lsn.shape.combined-transforms` Combining transformations and invariance | Combine transformations, describe the single equivalent where one exists, and find invariant points and lines | Reflect in $x = 1$, then in $x = 4$. What single move is that? | `geometry-board` (sequence builder), `vector-plane` | Trap: order does not matter (rotate then translate differs from translate then rotate). Edge: invariant points lie on mirror lines and at centres of rotation; a translation has none | C, P, M, N |
| 18 | `lsn.shape.constructions-loci` Constructions and loci | Construct perpendicular bisectors, angle bisectors and perpendiculars with compasses and straight edge, and shade regions defined by distance conditions | A phone mast must be nearer town A than town B and within 5 km of the road. Where can it go? | `geometry-board` (compass and straight-edge tools), `region-select` | Trap: "equidistant from two points" drawn as a circle (it is the perpendicular bisector); a fixed distance from a segment drawn without rounded ends. Edge: equidistant from two crossing lines is a pair of angle bisectors | R, C, P, M |

Transfer screens: lesson 18 shows the perpendicular bisector as the decision boundary of a one-nearest-neighbour classifier with two training points; lesson 17 previews the matrices of level T5.

**Level S5: Circle theorems** (`lvl.shape.circle-theorems`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 19 | `lsn.shape.centre-angle` The angle at the centre | Prove that the angle at the centre is twice the angle at the circumference, using isosceles triangles, and apply it | Drag point P round the circle. The angle APB never changes. Why? | `geometry-board` (circle-theorem preset; draggable P), `derivation-steps` | Trap: applying the theorem to angles that stand on different arcs. Edge: when P crosses to the minor arc, the centre angle is reflex, and the proof needs the subtraction case | N, N, O, C |
| 20 | `lsn.shape.same-segment` Angles in the same segment and in a semicircle | Derive that angles on the same arc are equal and that the angle in a semicircle is $90°$, and use their converses | Where can a footballer stand so that the goal looks equally wide? | `geometry-board` | Trap: angles on opposite arcs treated as equal (they add to $180°$). Edge: the semicircle theorem is the centre-angle theorem with $180°$ at the centre; a right angle standing on a chord makes that chord a diameter | N, N, C, M |
| 21 | `lsn.shape.cyclic-quads` Cyclic quadrilaterals | Prove that opposite angles of a cyclic quadrilateral add to $180°$ and combine it with the other theorems | Can every quadrilateral be drawn with its four corners on one circle? Try a rhombus that is not a square | `geometry-board` | Trap: any quadrilateral in a circle diagram assumed cyclic (all four corners must be on the circle). Edge: a rectangle is always cyclic, a non-square rhombus never is; the exterior angle equals the interior opposite angle | N, C, N, M |
| 22 | `lsn.shape.tangents` Tangents and the alternate segment theorem | Use radius perpendicular to tangent, equal tangents from an external point, and the alternate segment theorem | Two tangents from one point to a circle: are they always the same length? | `geometry-board` (tangent tool) | Trap: the alternate segment theorem applied to the wrong segment. Edge: it is the same-segment theorem in the limit as one chord turns into the tangent | N, N, C, N |
| 23 | `lsn.shape.geometric-proof` Writing a geometric proof | Write a chain of statements, each with a named reason, and prove an unseen result from the theorems | Prove that the perpendicular from the centre to a chord bisects the chord | `derivation-steps` (order mode with reason cards), `geometry-board`, `free-response` | Trap: using the result being proved; "it looks like $90°$". Edge: a diagram drawn special (isosceles, symmetric) hides the general case; drag it to a scruffy one first | O, S, C, O |

Transfer screens: none forced; this level trains the reason-giving that every later proof needs.

**Level S6: Right-angled trigonometry** (`lvl.shape.right-trig`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 24 | `lsn.shape.tan-ratio` Tangent: one ratio for every similar triangle | Explain from similarity why opposite over adjacent depends only on the angle, and use $\tan$ to find a side | Two ramps at the same angle, one long and one short. Measure rise over run for both | `geometry-board` (angle fixed, scale slider), `value-table`, `numeric-input` | Trap: the ratio changes with the size of the triangle. Edge: $\tan 45° = 1$; $\tan$ grows without bound as the angle nears $90°$ | N, N, C, N |
| 25 | `lsn.shape.sohcahtoa` Sine, cosine and choosing the ratio | Label hypotenuse, opposite and adjacent relative to an angle, choose the ratio linking the known and unknown sides, and solve | A 5 m ladder makes $70°$ with the ground. How high does it reach? | `geometry-board`, `card-sort` (which ratio?), `equation-workbench` | Trap: labels taken from the wrong angle; dividing when the unknown is on top ($5 \div \sin 70°$ instead of $5 \sin 70°$). Edge: a side longer than the hypotenuse is a red flag, because sine and cosine of an acute angle are below 1 | S, N, N, C |
| 26 | `lsn.shape.finding-angles` Finding angles with inverse functions | Use inverse sine, cosine and tangent to find angles, and explain why $\sin^{-1}$ needs an input between $-1$ and $1$ | A ramp rises 1 m over 12 m. What angle is that? | `geometry-board`, `function-machine` (inverse), `numeric-input` | Trap: $\sin^{-1} x$ read as $\frac{1}{\sin x}$; a calculator left in radian mode. Edge: $\sin^{-1}(1.2)$ has no answer, because no right triangle has an opposite side longer than its hypotenuse | N, N, C, M |
| 27 | `lsn.shape.exact-values` Exact values from two triangles | Derive sine, cosine and tangent of $30°$, $45°$ and $60°$ from the half-square and the half-equilateral triangle and use them without a calculator | Without a calculator, find the height of an equilateral triangle with side 2 | `geometry-board` (half-square, half-equilateral), `expression-input` | Trap: $\sin 60° = \sqrt{3}$ (the halving lost); $\sin 30°$ and $\cos 30°$ swapped. Edge: $\sin 0° = 0$, $\cos 0° = 1$, $\tan 90°$ undefined; $\sin \theta = \cos(90° - \theta)$ | X, X, C, X |
| 28 | `lsn.shape.trig-3d` Elevation, depression and three-dimensional problems | Solve multi-step problems with angles of elevation and depression, and find the angle between a line and a plane | From the top of a 40 m cliff a boat is at a $12°$ angle of depression. How far away is it? | `solid-viewer` (cuboid with a diagonal and its projection), `geometry-board`, `numeric-input` | Trap: the angle of depression placed inside the triangle at the wrong corner; the angle to a plane measured to an edge instead of to the projection. Edge: depression from A to B equals elevation from B to A (alternate angles) | N, N, C, N |

Transfer screens: lesson 24 identifies the gradient of a line as $\tan$ of its angle with the $x$-axis, which 1.3 uses for every tangent line.

**Level S7: Any triangle** (`lvl.shape.any-triangle`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 29 | `lsn.shape.area-sine` Area $= \tfrac{1}{2}ab\sin C$ | Derive the area formula from an altitude and use it, including solving for an angle from an area | Sides of 8 cm and 5 cm are hinged together. Which hinge angle makes the biggest triangle? | `geometry-board` (hinge slider; area readout), `graph-explorer` (area against angle) | Trap: an angle that is not between the two sides used. Edge: $\theta$ and $180° - \theta$ give the same area, so an area fixes two triangles; the maximum is at $90°$ | N, N, C, N |
| 30 | `lsn.shape.sine-rule` The sine rule and the ambiguous case | Derive the sine rule from two expressions for one altitude, use it for sides and angles, and decide whether the data fit zero, one or two triangles | Given two sides and a non-included angle, the free side swings and can hit the base line twice | `geometry-board` (SSA swing), `derivation-steps`, `numeric-input` | Trap: keeping only the calculator's acute angle from $\sin^{-1}$. Edge: $180° - \theta$ may also fit; if the swinging side is shorter than the altitude there is no triangle (the SSA failure of lesson 12, now counted) | N, N, M, O |
| 31 | `lsn.shape.cosine-rule` The cosine rule | Derive $c^2 = a^2 + b^2 - 2ab\cos C$ from Pythagoras with an altitude, covering obtuse angles, and use it for a side from SAS or an angle from SSS | Two hikers leave one point on paths $40°$ apart and walk 3 km and 5 km. How far apart are they? | `geometry-board` (hinge with altitude), `derivation-steps`, `numeric-input` | Trap: $(a^2 + b^2 - 2ab)\cos C$ computed as one bracket. Edge: at $90°$ the rule is Pythagoras; for an obtuse $C$, $\cos C < 0$ and the side is longer than Pythagoras predicts | N, N, X, C |
| 32 | `lsn.shape.choose-rule` Choosing the rule: multi-step triangle problems | Choose between right-angled trigonometry, the sine rule, the cosine rule and the area formula from the data given, and solve two-triangle and bearings problems | A surveyor knows two angles and the distance between two posts. How far is the island from each? | `card-sort` (data pattern to rule), `geometry-board`, `numeric-input` | Trap: rounding at every step so the error grows. Edge: three angles and no side fix the shape but not the size | S, N, N, C |

Transfer screens: lesson 31 sets the cosine rule beside the variance of a two-asset portfolio, $\sigma_p^2 = \sigma_1^2 + \sigma_2^2 + 2\rho\sigma_1\sigma_2$ (each $\sigma$ already multiplied by its weight): the same shape, with the correlation $\rho$ playing the part of the cosine of the angle between the two vectors placed tail to tail. The sign flips because the cosine rule uses the triangle's interior angle, which is $180°$ minus that angle.

**Level S8: Vectors** (`lvl.shape.vectors`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 33 | `lsn.shape.vectors-journeys` Vectors as journeys | Represent displacements as column vectors and arrows, add them tip to tail, and subtract by adding the negative | A drone flies $\binom{3}{1}$, then $\binom{-1}{4}$. Where does it end, and what single flight does the same? | `vector-plane` (lattice; tip to tail), `expression-input` (column vector) | Trap: adding tail to tail; $\vec{AB}$ written as $\mathbf{a} - \mathbf{b}$ instead of $\mathbf{b} - \mathbf{a}$. Edge: the zero vector; either order of addition gives the same result (the parallelogram) | X, P, N, C |
| 34 | `lsn.shape.scalar-multiples` Scalar multiples and parallel vectors | Multiply vectors by scalars, and test for parallel lines and collinear points using "one vector is a multiple of the other" | Is the path $\binom{6}{-4}$ parallel to $\binom{-9}{6}$? | `vector-plane`, `slider` (scalar) | Trap: a negative multiple judged not parallel (it is parallel and reversed). Edge: collinear points need a shared point as well as parallel vectors | C, N, M, X |
| 35 | `lsn.shape.vector-proof` Vector geometry proofs | Express vectors in a figure in two base vectors, find midpoints and ratio points, and prove parallel and collinear results | Join the midpoints of the sides of any quadrilateral. Why is the result always a parallelogram? | `vector-plane` (base vectors $\mathbf{a}$, $\mathbf{b}$), `derivation-steps`, `geometry-board` | Trap: the point dividing AB in the ratio $2 : 1$ placed at $\tfrac{1}{3}$ or $\tfrac{1}{2}$ of the way from A (it is $\tfrac{2}{3}$). Edge: the midpoint parallelogram appears even for a non-convex quadrilateral | X, X, O, C |
| 36 | `lsn.shape.magnitude-direction` Magnitude, direction and components | Compute magnitude and direction, convert between components and magnitude-direction form with sine and cosine, and form unit vectors | A boat heads north at 8 km/h in a current flowing east at 3 km/h. How fast, and in which direction, does it really move? | `vector-plane` (components overlay), `numeric-input` | Trap: magnitude as $x + y$; direction from $\tan^{-1}(y/x)$ with no thought for the quadrant. Edge: $\binom{-3}{-4}$ and $\binom{3}{4}$ give the same $\tan^{-1}$; the zero vector has no unit vector | N, N, X, C |
| 37 | `lsn.shape.dot-product` The dot product | Compute $\mathbf{a} \cdot \mathbf{b}$ from components, derive $\mathbf{a} \cdot \mathbf{b} = \lvert \mathbf{a} \rvert \lvert \mathbf{b} \rvert \cos\theta$ from the cosine rule, and test for perpendicular vectors | Are $\binom{3}{1}$ and $\binom{-1}{3}$ perpendicular? Measure, then compute $3 \times (-1) + 1 \times 3$ | `vector-plane` (projection overlay), `derivation-steps` | Trap: the dot product treated as a vector; magnitudes multiplied without the cosine. Edge: a negative dot product means an obtuse angle; $\mathbf{a} \cdot \mathbf{a} = \lvert \mathbf{a} \rvert^2$ | N, N, C, O |
| 38 | `lsn.shape.projection-3d` Projections, 3D vectors and cosine similarity | Extend vectors to three dimensions with $\mathbf{i}$, $\mathbf{j}$, $\mathbf{k}$, compute the projection of one vector on another, and compute the cosine similarity of two data vectors | Three shopping baskets as vectors of (apples, bread, coffee). Which basket is most like basket A? | `vector-plane` (3D mode), `value-table`, `numeric-input` | Trap: distance and cosine similarity expected to agree (a big and a small basket with the same mix are far apart but have similarity 1). Edge: cosine similarity is undefined for the zero vector | N, N, C, N |

Transfer screens: lesson 37 reads correlation as a cosine between centred data vectors (1.5, 1.6); lesson 38 uses cosine similarity as recommender systems and text embeddings do, and calls the projection "the seed of least squares" (1.4).

#### Course G: Growth: Sequences, Series, Exponentials and Logarithms (`crs.growth`, 5 levels, 27 lessons)

One story: adding the same amount each step (arithmetic sequences), multiplying by the same factor each step (geometric sequences and exponentials), counting the multiplications (logarithms), and adding up what accumulates (series). It ends at present value, the first pricing formula, and at the sums that 1.5 needs for expectations.

**Level G1: Sequences and recurrences** (`lvl.growth.sequences`, 5 lessons)

0.2 lesson 41 taught arithmetic $n$th terms, lesson 83 quadratic sequences by finite differences and lesson 107 iteration with cobwebs. G1 starts from there: rules that define a sequence from its own past, the two-term recurrences behind Fibonacci and gambler's ruin, and what "tends to" means.

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 39 | `lsn.growth.sequence-rules` Explicit and recursive rules | Write the same sequence as an explicit rule $u_n = f(n)$ and as a recursive rule $u_{n+1} = g(u_n)$ with a starting value, and convert between them for arithmetic and geometric sequences, with the index starting at 0 or at 1 | A gym costs £40 to join and £25 a month. One friend writes $u_n = 40 + 25n$, another $u_n = 15 + 25n$. Both say they are right. Can they be? | `sequence-lab` (explicit and recursive views side by side; index-origin toggle), `value-table`, `expression-input` | Trap: mixing index origins, so the rule is off by one term (Python lists start at 0, many textbooks at 1). Edge: a recursive rule needs a starting value, and two starting values give two different sequences from one rule | X, X, C, N |
| 40 | `lsn.growth.geometric-seq` Geometric sequences | Find and use the $n$th term $ar^{n-1}$, including negative and fractional ratios, and tell a constant ratio from a constant difference in data | A ball bounces to 60% of its previous height, starting from 2 m. How high is the fifth bounce? | `sequence-lab` (ratio slider), `multiplier-chain` | Trap: $ar^n$ (the index origin again); a ratio confused with a difference. Edge: a negative $r$ alternates signs; finding $n$ from a term needs logarithms (a forward pointer to G3) | X, N, C, N |
| 41 | `lsn.growth.recurrences` First-order recurrences and their fixed points | Generate terms from $u_{n+1} = au_n + b$, classify the behaviour (growing, shrinking to a limit, oscillating), and find the closed form by shifting to the fixed point $L = \frac{b}{1 - a}$ | A loan of £10,000 grows by 1% a month and £200 is repaid each month. What happens to it, and when is it cleared? | `sequence-lab` (recurrence mode), `value-table`, `derivation-steps` | Trap: finding $u_n$ by putting $n$ into the rule $g$. Edge: repaying exactly £100 a month (the interest) leaves the balance frozen forever; less than £100 and it grows | N, C, S, X |
| 42 | `lsn.growth.two-term` Two-term recurrences: Fibonacci and the golden ratio | Solve $u_{n+2} = pu_{n+1} + qu_n$ by trying $u_n = r^n$, combine the two roots of $r^2 = pr + q$ to fit two starting values, and show that consecutive Fibonacci ratios approach $\varphi = \frac{1 + \sqrt{5}}{2}$ | How many ways can you climb 10 stairs taking one or two steps at a time? (89) | `sequence-lab` (two-term mode; ratio row), `derivation-steps`, `graph-explorer` (ratios against $n$) | Trap: one power $r^n$ expected to fit both starting values (it takes a combination $A r_1^n + B r_2^n$); counting the stairs from the wrong starting case. Edge: a repeated root $r$ gives $(A + Bn)r^n$; since $\lvert \psi \rvert < 1$ for $\psi = \frac{1 - \sqrt{5}}{2}$, the $n$th Fibonacci number is the whole number nearest $\frac{\varphi^n}{\sqrt{5}}$ | N, X, O, C |
| 43 | `lsn.growth.sequence-limits` What "tends to" means | Decide whether a sequence converges, find limits of $r^n$, $\frac{1}{n}$ and ratios of polynomials in $n$, and find how far out a sequence stays within a given distance of its limit | $u_n = \frac{3n + 1}{n + 2}$. Work it out at $n = 10$, 100 and 1,000. Where is it heading, and from which $n$ on is it less than 0.001 from there? (from $n = 4{,}999$, since the gap is $\frac{5}{n + 2}$) | `sequence-lab` (tolerance band), `value-table`, `iteration-cobweb` (recap of 0.2 lesson 107) | Trap: "it keeps getting closer to 4, so its limit is 4" ($u_n$ gets closer to 4 for ever and its limit is 3). Edge: $(-1)^n$ has no limit; $r^n \to 0$ exactly when $\lvert r \rvert < 1$; if a recurrence converges, its limit solves $L = g(L)$, but a fixed point does not make it converge ($u_{n+1} = 2u_n - 1$ from $u_1 = 2$) | N, C, M, N |

Transfer screens: lesson 41 is a loan amortisation and the balance of a savings plan; lesson 42 names two-term recurrences as the form of gambler's ruin (1.5) and of the running time of recursive algorithms (1.8); lesson 43 is the convergence test every iterative fitting routine in ML applies.

**Level G2: Exponential functions** (`lvl.growth.exponentials`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 44 | `lsn.growth.real-exponents` What $b^x$ means between whole numbers | Explain how $b^x$ is defined for rational $x$ from roots and powers and for irrational $x$ by squeezing between rational exponents, and justify why the base must be positive (0.2 lesson 97 sketched the graph; this lesson fills it in) | $2^3 = 8$ and $2^4 = 16$. What should $2^{3.5}$ be? And $2^\pi$? | `graph-explorer` (dots to a curve; zoom), `multiplier-chain` (partial tiles), `value-table` (squeezing $2^{3.14}$, $2^{3.141}$, ...) | Trap: $2^{3.5} = 12$, halfway by adding. Edge: the base must be positive: $(-8)^{1/3} = -2$ but $(-8)^{1/2}$ is not real, and $(-8)^{2/6}$ would equal $\sqrt[6]{64} = 2$, so a negative base gives answers that depend on how the fraction is written; $b = 1$ is flat | N, C, P, M |
| 45 | `lsn.growth.growth-decay` Rates over different periods: doubling time and half-life | Convert a growth or decay factor between periods ($b_{\text{month}} = b_{\text{year}}^{1/12}$), and between a percentage rate, a doubling time and a half-life, building on 0.2 lesson 97's $y = Ab^t$ | A drug's level halves every 6 hours. What fraction remains after a day? After 15 hours? What is the hourly factor? | `multiplier-chain`, `graph-explorer` | Trap: a monthly rate taken as the annual rate divided by 12 for a factor (a 12% annual factor is $1.12^{1/12} \approx 1.0095$ a month, not $1.01$); a rate of 5% read as $b = 0.05$. Edge: the half-life is the same whenever you start the clock (exponential decay forgets its past) | X, N, N, C |
| 46 | `lsn.growth.compounding` Compounding frequency and the effective rate | Compute balances with compounding $n$ times a year and convert nominal rates to effective annual rates | 12% a year paid monthly, or 12.5% paid once a year: which is better? | `multiplier-chain` (compounding mode), `value-table` | Trap: "1% a month is 12% a year" (it is 12.68%). Edge: compounding more often always helps but by less and less: 12% compounded daily is about 12.75%, and no frequency passes $e^{0.12} - 1 \approx 12.750\%$ | N, N, C, N |
| 47 | `lsn.growth.e-number` The number $e$ | Show that $(1 + \tfrac{1}{n})^n$ settles at a limit $e \approx 2.718$, and use continuous compounding $A = Pe^{rt}$ | A bank pays 100% a year. Paid yearly, £1 becomes £2. Paid daily? Every second? Is there a ceiling? | `multiplier-chain` (compounding to the limit), `value-table`, `graph-explorer` | Trap: "the power grows, so it goes to infinity", or "$\tfrac{1}{n}$ goes to 0, so it goes to 1". Edge: the two pulls balance exactly, and the balance point is irrational | N, C, N, X |
| 48 | `lsn.growth.ex-slope` $e^x$: the function that is its own gradient | Estimate gradients of $b^x$ with tangent lines, see that each gradient is a fixed multiple of the height, and identify $e$ as the base where the multiple is 1 | On $y = 2^x$ the tangent gradient is about 0.69 at $x = 0$ and about 5.5 at $x = 3$. What is the pattern? | `graph-explorer` (tangent overlay; base slider) | Trap: the gradient of $2^x$ written as $x \cdot 2^{x-1}$, the power rule misapplied. Edge: for $0 < b < 1$ the multiple is negative; the multiple turns out to be $\ln b$ (lesson 54) | N, C, N, M |

Transfer screens: lesson 46 reads AER and APR on a real loan advert; lesson 47 matches continuous compounding to the convention in Hull's chapter on interest rates (section 5).

**Level G3: Logarithms** (`lvl.growth.logarithms`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 49 | `lsn.growth.log-as-count` Logarithms count multiplications (written in full in section 7) | Evaluate $\log_b x$ by counting multiplications by $b$ that take 1 to $x$, including zero, negative and non-whole counts, and explain why $\log_b x$ is undefined for $x \le 0$ | Fold a sheet of paper in half again and again. How many folds give 1,024 layers? | `multiplier-chain` (tile mode), `graph-explorer`, `derivation-steps`, `numeric-input`, `choice` | Trap: $\log_{10} 0.001 = 3$ (shrinking counted as growing). Edge: $\log_b 1 = 0$; no count reaches 0 or a negative number | N, N, C, M, N |
| 50 | `lsn.growth.log-graph` The logarithm as an inverse function | Sketch $y = \log_b x$ as the reflection of $y = b^x$ in $y = x$ and state its domain, range, intercept and asymptote | $(5, 32)$ lies on $y = 2^x$. Name a point on $y = \log_2 x$ without calculating | `graph-explorer` (reflect in $y = x$), `function-machine` (inverse pipeline) | Trap: a horizontal asymptote for $\log x$ (it is vertical, at $x = 0$); "log levels off" (it is unbounded, just slow). Edge: $\log_2 x$ reaches 100 only at $x = 2^{100}$ | P, N, C, M |
| 51 | `lsn.growth.log-laws` The laws of logarithms | Derive $\log(xy) = \log x + \log y$, $\log(x/y) = \log x - \log y$ and $\log(x^k) = k\log x$ from the index laws, and use them to combine and split expressions | Multiply $8 \times 32$ using only addition and a table of powers of 2 | `slide-rule`, `derivation-steps`, `expression-input` | Trap: $\log(x + y) = \log x + \log y$; $(\log x)^2 = 2\log x$. Edge: $\log(x^2) = 2\log\lvert x \rvert$ when $x$ may be negative | X, X, C, O |
| 52 | `lsn.growth.change-of-base` Change of base | Derive $\log_b x = \frac{\log_a x}{\log_a b}$ and evaluate any logarithm with a calculator's $\ln$ or $\log$ key | Your calculator has only $\log_{10}$ and $\ln$. Find $\log_2 100$ | `slide-rule` (two scales in different bases), `derivation-steps`, `numeric-input` | Trap: $\frac{\log 100}{\log 2}$ simplified to $\log 100 - \log 2$. Edge: $\log_b a \times \log_a b = 1$; logs in different bases are proportional, so a log chart looks the same in any base | N, X, C, N |
| 53 | `lsn.growth.exp-equations` Solving exponential equations | Solve $a^x = b$, equations with exponentials on both sides, and quadratics in $e^x$ or $2^x$, rejecting impossible roots | £1,000 grows at 4% a year. When does it first pass £1,500? | `equation-workbench`, `graph-explorer` (intersection) | Trap: taking logs of a sum term by term; dividing an inequality by $\ln$ of a number below 1 without reversing it. Edge: $e^{2x} - 5e^x + 6 = 0$ gives $e^x = 2$ or $3$, but $e^x = -1$ would have to be rejected | N, X, N, I |
| 54 | `lsn.growth.natural-log` The natural logarithm and continuous growth | Use $\ln$ as the inverse of $e^x$ to solve continuous growth and decay problems, and rewrite any $a^x$ as $e^{x\ln a}$ | A population grows continuously at 3% a year. How long until it doubles? | `graph-explorer`, `equation-workbench` | Trap: $\frac{\ln x}{\ln y} = \ln\frac{x}{y}$. Edge: $a^x = e^{x\ln a}$, so the gradient multiple of lesson 48 is $\ln a$; the rule of 72 comes from $\frac{\ln 2}{r} \approx \frac{0.69}{r}$ with a little extra for annual compounding | N, X, N, C |

Transfer screens: lesson 51 shows why slide rules and log tables made multiplication fast for 350 years; lesson 52 compares bits and nats ($\log_2$ against $\ln$ in information theory); lesson 53 derives the doubling time of £1,000 at 4% (17.7 years, so 18 whole years).

**Level G4: Modelling with exponentials and logarithms** (`lvl.growth.modelling`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 55 | `lsn.growth.log-scales` Computing with log scales | Convert between a position on a log axis and its value with $\log_{10}$, find the geometric midpoint of two values, and read log scales in the wild (decibels, pH, earthquake magnitudes, log price charts), extending 0.2 lesson 47's reading of a log axis | On a log chart a share sits 30% of the way from the 100 line to the 1,000 line. What is the price? (about 200) | `graph-explorer` (log axis toggle; position readout), `number-line` (log scale) | Trap: the midpoint of 1 and 100 on a log scale is 50 (it is 10, the geometric mean, as in 0.1 lesson 40's Fermi bounds). Edge: zero and negatives have no place on a log axis; every 3 dB is about a doubling of power, because $\log_{10} 2 \approx 0.301$ | N, N, C, P |
| 56 | `lsn.growth.linearising` Straightening data with logarithms | Fit $y = ab^x$ by plotting $\log y$ against $x$, and $y = ax^n$ by plotting $\log y$ against $\log x$, and read $a$, $b$ and $n$ from the line | Eight data points curve upwards. Exponential or power law? | `scatter-fit` (log axes), `value-table`, `equation-workbench` | Trap: reading the intercept of the $\log y$ line as $a$ (it is $\log a$). Edge: straight on log-log means a power law, straight on semi-log means an exponential, straight on neither means neither | N, N, C, X |
| 57 | `lsn.growth.log-returns` Simple returns and log returns | Compute simple and log returns, show that log returns add across periods while simple returns compound, and convert between them | A fund returns $+60\%$, $-30\%$, $+60\%$, $-30\%$ in four years: an average of 15% a year. What did £100 become? (£125.44, not £174.90) | `multiplier-chain` (log panel), `value-table`, `numeric-input` | Trap: the average of simple returns taken as the growth rate. Edge: for small $r$, $\ln(1 + r) \approx r$; a return of $-100\%$ has log return $-\infty$ | N, N, C, N |
| 58 | `lsn.growth.growth-hierarchy` Who wins: logarithms, powers, exponentials, factorials | Rank $\log n$, $n^k$, $b^n$ and $n!$ by eventual size and justify the ranking with ratios | Algorithm A takes $n^2$ steps, B takes $2^n$, C takes $100\,n\log_2 n$. Which is fastest at $n = 10$? At $n = 1{,}000$? | `graph-explorer` (log $y$-axis; race mode), `value-table` | Trap: judging by small $n$ ($n^2$ beats $100\,n\log_2 n$ for small $n$). Edge: $n^{100}$ does lose to $1.01^n$, but only at astronomically large $n$ | S, C, N, M |
| 59 | `lsn.growth.log-underflow` Logarithms against underflow | Turn a product of many small probabilities into a sum of logarithms and explain why software works with log-likelihoods | Multiply 0.01 by itself 400 times in Python. You get 0.0. Is the true answer 0? | `predict-output`, `code-cell`, `slide-rule`, `numeric-input` | Trap: "the computer's answer is right, just small" (it underflowed: the true value is $10^{-800}$). Edge: adding probabilities stored as logs needs the log-sum-exp shift by the largest term | T, N, C, X |

Transfer screens: lesson 55 uses log price charts; lesson 56 fits a power law to trade sizes; lesson 57 is the computation the 1.1 exit asks for; lesson 58 is big-O for 1.8; lesson 59 is the log-likelihood of 1.6 and the cross-entropy loss of 2.1.

**Level G5: Series** (`lvl.growth.series`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 60 | `lsn.growth.sigma-algebra` Index shifts and double sums | Shift the index of a sum, split and reverse sums, and evaluate double sums, using $\sum_i \sum_j a_i b_j = \left(\sum_i a_i\right)\left(\sum_j b_j\right)$ and telling it apart from $\sum_k a_k b_k$ (0.2 lesson 16 gave the notation and linearity) | Add up all 100 entries of the $10 \times 10$ multiplication table. Row by row, or all at once? (3,025) | `sum-visualiser` (sigma mode; grid of terms), `expression-input` | Trap: $\sum_k a_k b_k = \sum_k a_k \sum_k b_k$; an index shift that changes the limits but not the summand. Edge: an empty sum is 0; the sum over pairs $i < j$ does not factor, but equals $\frac{1}{2}\left[\left(\sum a_i\right)^2 - \sum a_i^2\right]$, the identity behind the variance of a sum (1.5) | X, N, C, X |
| 61 | `lsn.growth.arithmetic-series` Arithmetic series | Derive $S_n = \frac{n}{2}(2a + (n - 1)d)$ by pairing the series with its reverse, and solve for $n$, $a$ or $d$ | Add $1 + 2 + \dots + 100$ in under a minute | `sum-visualiser` (staircase and its rotated copy) | Trap: $n(a + l)$ without the half; counting the terms from 3 to 50 as 47 (it is 48). Edge: solving for $n$ gives a quadratic whose negative root is rejected | N, X, N, C |
| 62 | `lsn.growth.geometric-series` Geometric series | Derive $S_n = \frac{a(1 - r^n)}{1 - r}$ by shifting and subtracting, and use it | One grain of rice on the first square of a chessboard, doubling each square. How many grains in all? | `sum-visualiser` (shift and subtract), `derivation-steps` | Trap: $r^{n-1}$ or $r^{n+1}$ in the numerator; using the formula when $r = 1$. Edge: $r = 1$ gives $na$; the forms with $1 - r$ and $r - 1$ are the same formula | N, X, O, N |
| 63 | `lsn.growth.infinite-series` Sums to infinity | Decide when a geometric series converges, compute $S_\infty = \frac{a}{1 - r}$, and prove 0.1 lesson 23's method for turning recurring decimals into fractions | Walk halfway to the wall, then half of what is left, forever. Do you reach it? How far do you walk? | `sum-visualiser` (square fill), `series-explorer` (partial sums), `slider` ($r$) | Trap: "infinitely many positive terms must add to infinity"; applying $\frac{a}{1-r}$ at $r = -1$. Edge: $0.999\ldots = 1$; $1 - 1 + 1 - \dots$ has no sum | N, C, X, M |
| 64 | `lsn.growth.present-value` Present value, annuities and perpetuities | Discount future cash flows, sum annuity and perpetuity payments as geometric series, and compute a loan's level payment | £10,000 now, or £1,000 a year for 12 years at 5%? | `sum-visualiser`, `multiplier-chain` (discounting), `value-table` | Trap: adding future payments without discounting (£12,000 against a true value of £8,863). Edge: a perpetuity of £$C$ a year at rate $r$ is worth $\frac{C}{r}$; a growing perpetuity $\frac{C}{r - g}$ needs $g < r$ | N, N, C, N |
| 65 | `lsn.growth.telescoping` Telescoping sums and $\sum k r^k$ | Evaluate telescoping sums and the arithmetico-geometric sum $\sum k r^{k-1}$ by shifting and subtracting | $\frac{1}{1 \times 2} + \frac{1}{2 \times 3} + \dots + \frac{1}{99 \times 100}$ | `sum-visualiser` (cancellation view), `derivation-steps` | Trap: missing the surviving end terms. Edge: $\sum_{k \ge 1} k r^{k-1} = \frac{1}{(1 - r)^2}$ for $\lvert r \rvert < 1$, which gives the expected number of rolls until a six: 6 | N, X, O, N |

Transfer screens: lesson 64 prices a bond's coupons and a mortgage; lesson 65 is the expectation of the geometric distribution, met again in 1.5.

#### Course T: Circles, Waves and Rotations (`crs.waves`, 6 levels, 32 lessons)

Trigonometry moves from triangles to the circle: angles in radians, sine and cosine as coordinates, waves as circles unrolled in time. Identities and compound angles follow, then the two great uses of rotation: matrices, which turn the plane, and complex numbers, which multiply by turning. The course ends where Euler's formula joins the exponentials of course G to the circle.

**Level T1: Radians and the unit circle** (`lvl.waves.unit-circle`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 66 | `lsn.waves.radians` Radians | Convert between degrees and radians and explain one radian as the angle whose arc equals the radius | Wrap pieces of string as long as the radius round a circle. How many fit? | `unit-circle` (string wrap) | Trap: "$\pi = 180$" ($\pi$ radians is $180°$; $\pi$ is a number). Edge: one radian is about $57.3°$; radians carry no unit, which is why calculus uses them | N, X, C, N |
| 67 | `lsn.waves.arc-sector-radians` Arc length and sector area in radians | Derive $s = r\theta$ and $A = \tfrac{1}{2}r^2\theta$, and find segment areas | A 50 cm wiper sweeps 2 radians; its rubber covers the outer 30 cm. What area does it clean? | `unit-circle`, `geometry-board` (segment) | Trap: degrees put into $s = r\theta$. Edge: segment area $\tfrac{1}{2}r^2(\theta - \sin\theta)$ is tiny for small $\theta$ | N, N, X, N |
| 68 | `lsn.waves.sin-cos-circle` Sine and cosine for any angle | Define $\cos\theta$ and $\sin\theta$ as the coordinates of the point at angle $\theta$ on the unit circle, agreeing with right-triangle ratios for acute angles | SOHCAHTOA says nothing about $150°$, yet a calculator gives $\sin 150° = 0.5$. Where does that come from? | `unit-circle` (drag the point; coordinate readouts) | Trap: "sine of an angle over $90°$ does not exist" or "is always positive". Edge: negative angles and angles over $2\pi$ wrap round; $\sin$ and $\cos$ never leave $[-1, 1]$ | N, C, P, N |
| 69 | `lsn.waves.quadrants` Signs, symmetries and related angles | Use the circle's reflections to write $\sin$, $\cos$ and $\tan$ of any angle through an acute angle with the right sign | Without a calculator: $\sin 210°$ and $\cos(-60°)$ | `unit-circle` (reflection overlays) | Trap: a memorised quadrant rule misapplied to negative angles. Edge: $\sin(\pi - \theta) = \sin\theta$; $\cos(-\theta) = \cos\theta$ (even), $\sin(-\theta) = -\sin\theta$ (odd) | X, X, M, C |
| 70 | `lsn.waves.tan-slope` Tangent as a slope, and exact values round the circle | Define $\tan\theta = \frac{\sin\theta}{\cos\theta}$ as the slope of the radius, find where it is undefined, and give exact values at multiples of $\frac{\pi}{6}$ and $\frac{\pi}{4}$ | What is the slope of the radius at $60°$? At $90°$? | `unit-circle` (tangent-line overlay) | Trap: $\tan 90° = 1$ or $0$. Edge: $\tan$ repeats every $\pi$, not every $2\pi$ | X, C, X, N |

Transfer screens: lesson 68 converts a 2D direction into components with $\cos$ and $\sin$ (the `atan2` and polar coordinates of code).

**Level T2: Waves** (`lvl.waves.graphs`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 71 | `lsn.waves.unroll` From circle to wave | Sketch $y = \sin x$, $\cos x$ and $\tan x$ over several periods, marking zeros, maxima and asymptotes, by unrolling the circle | Track the height of a seat on a turning big wheel against time | `circle-to-wave`, `sketch-pad` | Trap: $\cos$ drawn as $\sin$ shifted the wrong way. Edge: $\cos x = \sin(x + \frac{\pi}{2})$; $\tan$ has asymptotes at odd multiples of $\frac{\pi}{2}$ | P, C, M, N |
| 72 | `lsn.waves.amplitude` Amplitude and midline | Set and read the amplitude and midline in $y = A\sin x + D$, including from a maximum and a minimum | A tide runs between 1.2 m and 5.6 m. Write its height as a sine wave | `circle-to-wave` ($A$ and $D$ sliders), `graph-explorer` | Trap: amplitude taken as the maximum (it is half of maximum minus minimum). Edge: a negative $A$ reflects the wave; the amplitude is $\lvert A \rvert$ | N, X, P, C |
| 73 | `lsn.waves.period` Period and frequency | Relate $B$ in $\sin(Bx)$ to the period $\frac{2\pi}{B}$ and the frequency, and choose $B$ for a given period | The wheel turns twice as fast. What happens to the graph? | `circle-to-wave` (speed), `graph-explorer` | Trap: period $= B$ or $2\pi B$. Edge: in degrees the period is $\frac{360°}{B}$; a negative $B$ reflects | N, X, C, P |
| 74 | `lsn.waves.phase` Phase shift and the full sinusoid | Build $y = A\sin(B(x - C)) + D$ to match a target wave, reading the shift correctly when $B \ne 1$ | Match the target wave with four sliders | `circle-to-wave` (four sliders, target overlay) | Trap: $\sin(2x - \frac{\pi}{3})$ read as a shift of $\frac{\pi}{3}$ (it is $\frac{\pi}{6}$). Edge: a phase shift is never unique: add any whole period | X, N, P, C |
| 75 | `lsn.waves.periodic-models` Modelling periodic data | Fit a sinusoid to periodic data from its maximum, minimum, period and the time of a peak, and use it to predict | London has about 7.8 hours of daylight in December and 16.6 in June. When does a day reach 12 hours? | `scatter-fit`, `graph-explorer`, `value-table` | Trap: an off-by-one month index shifts every prediction; "periodic, so sinusoidal". Edge: real seasonal data is periodic but not a pure sine, and the residuals show the gap | X, N, N, C |

Transfer screens: lesson 75 is seasonality, the periodic component that time-series models remove (2.2).

**Level T3: Identities and equations** (`lvl.waves.identities`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 76 | `lsn.waves.pythagorean-identity` $\sin^2\theta + \cos^2\theta = 1$ | Derive the identity from the unit circle and use it with $\tan\theta = \frac{\sin\theta}{\cos\theta}$ to find one ratio from another | $\sin\theta = \frac{3}{5}$ and $\theta$ is obtuse. Find $\cos\theta$ without finding $\theta$ | `unit-circle` (right triangle inside), `derivation-steps` | Trap: the sign of $\cos$ ignored; $\sin^2\theta$ read as $\sin(\theta^2)$. Edge: an identity holds for every $\theta$; an equation holds for some | X, X, C, N |
| 77 | `lsn.waves.reciprocal` Secant, cosecant and cotangent | Define $\sec$, $\operatorname{cosec}$ and $\cot$, sketch them, and derive $1 + \tan^2\theta = \sec^2\theta$ and $1 + \cot^2\theta = \operatorname{cosec}^2\theta$ | Divide $\sin^2\theta + \cos^2\theta = 1$ by $\cos^2\theta$. What appears? | `graph-explorer` (reciprocal overlay), `derivation-steps` | Trap: $\sec = \frac{1}{\sin}$; $\sec\theta$ confused with $\cos^{-1}\theta$. Edge: $\sec$ is never strictly between $-1$ and $1$ | X, C, O, P |
| 78 | `lsn.waves.proving-identities` Proving identities | Prove identities by transforming one side into the other, and explain why matching graphs or a few test angles are not a proof | Two expressions draw identical graphs on screen. Are they equal everywhere? | `equation-workbench` (identity mode), `graph-explorer` (overlay), `derivation-steps` | Trap: working on both sides at once and "cancelling across the equals", which assumes the result; dividing by something that can be 0. Edge: an identity can fail at isolated points where one side is undefined | O, O, C, X |
| 79 | `lsn.waves.solve-in-range` Solving trigonometric equations in a range | Find every solution of $\sin x = k$, $\cos x = k$ and $\tan x = k$ in an interval from the principal value and the circle's symmetry | $\sin x = 0.5$. The calculator says $30°$. How many solutions between $0°$ and $720°$? | `unit-circle` (horizontal-line overlay), `graph-explorer` (line meets wave) | Trap: stopping at the calculator's one answer. Edge: $k$ outside $[-1, 1]$ gives none; $k = \pm 1$ gives one per turn | I, N, C, I |
| 80 | `lsn.waves.harder-equations` Multiple angles and quadratics in sine | Solve $\sin 2x = k$, $\cos(x - \alpha) = k$ and quadratics in $\sin x$ or $\cos x$ in a range, widening the range for the transformed angle | $2\sin^2 x - \sin x - 1 = 0$. How many solutions in $[0, 2\pi)$? | `equation-workbench`, `graph-explorer` | Trap: dividing by $\sin x$ and losing the solutions of $\sin x = 0$; forgetting to double the range for $2x$. Edge: replacing $\cos^2 x$ by $1 - \sin^2 x$ turns two functions into one | I, I, C, N |
| 81 | `lsn.waves.inverse-trig` Inverse trigonometric functions | Define $\arcsin$, $\arccos$ and $\arctan$ on restricted domains, state their ranges, and sketch them | $\sin(\sin^{-1} 0.3) = 0.3$. Is $\sin^{-1}(\sin 3) = 3$? | `graph-explorer` (domain handles; reflect in $y = x$), `function-machine` | Trap: $\sin^{-1}(\sin x) = x$ for every $x$ (it is $\pi - 3 \approx 0.14$ here). Edge: $\arctan$ has range $(-\frac{\pi}{2}, \frac{\pi}{2})$, so code uses `atan2` to get a vector's direction in the right quadrant | N, P, C, M |

Transfer screens: lesson 81 uses `math.atan2` for the direction of a 2D vector.

**Level T4: Compound angles** (`lvl.waves.compound`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 82 | `lsn.waves.sin-sum` $\sin(A + B)$ | Show that $\sin(A + B) \ne \sin A + \sin B$ and derive $\sin(A + B) = \sin A\cos B + \cos A\sin B$ from a rectangle built round two stacked right triangles | $\sin 30° + \sin 60° \approx 1.37$. Can that be $\sin 90°$? | `geometry-board` (keyframed construction), `stepper`, `derivation-steps` | Trap: $\sin(A + B) = \sin A + \sin B$. Edge: $B = A$ gives $\sin 2A = 2\sin A\cos A$; replacing $B$ by $-B$ gives the subtraction formula through odd and even symmetry | X, N, O, C |
| 83 | `lsn.waves.cos-tan-sum` $\cos(A \pm B)$ and $\tan(A \pm B)$ | Derive $\cos(A \pm B)$ (also from the dot product of two unit vectors, lesson 37) and $\tan(A \pm B)$, and use them for exact values such as $\cos 75°$ | Find $\cos 75°$ exactly from $45°$ and $30°$ | `derivation-steps`, `vector-plane` (two unit vectors), `expression-input` | Trap: the sign in $\cos(A + B) = \cos A\cos B - \sin A\sin B$. Edge: $\tan(A + B)$ is undefined exactly when $\tan A\tan B = 1$, which for acute angles means $A + B = 90°$ | X, X, C, N |
| 84 | `lsn.waves.double-angle` Double-angle formulae | Derive $\sin 2A$, the three forms of $\cos 2A$ and $\tan 2A$, and choose the form that solves an equation or removes a square | Rearrange $\cos 2\theta = 1 - 2\sin^2\theta$ to write $\sin^2\theta$ without a square | `derivation-steps`, `equation-workbench`, `graph-explorer` | Trap: $\sin 2A = 2\sin A$; choosing a $\cos 2A$ form that leaves two functions. Edge: $\sin^2\theta = \frac{1 - \cos 2\theta}{2}$ turns a square into a wave of double frequency, which is why a sine wave's mean square is half its squared amplitude | X, I, C, X |
| 85 | `lsn.waves.r-form` Adding waves: $a\sin x + b\cos x = R\sin(x + \alpha)$ | Write $a\sin x + b\cos x$ as one sinusoid, find $R$ and $\alpha$, and use the form for maxima, minima and equations | Two speakers play one note slightly out of step. What does the sum look like? | `circle-to-wave` (phasor mode), `derivation-steps` | Trap: $R = a + b$; $\alpha$ from the wrong ratio for the expansion used. Edge: waves of different frequencies do not add to one sinusoid | N, X, N, C |
| 86 | `lsn.waves.small-angles` Small-angle approximations | Use $\sin\theta \approx \theta$, $\tan\theta \approx \theta$ and $\cos\theta \approx 1 - \frac{\theta^2}{2}$ for small $\theta$ in radians, and judge the error | At 0.1 radians, $\sin\theta = 0.0998$. Coincidence? | `graph-explorer` (zoom to the origin), `value-table` (error table) | Trap: degrees used; $\cos\theta \approx 1 - \theta$. Edge: the relative error of $\sin\theta \approx \theta$ is about $\frac{\theta^2}{6}$, under 1% up to about 0.24 radians ($14°$) | N, N, C, X |

Transfer screens: lesson 86 names these as the first terms of Taylor series (1.3).

**Level T5: Matrices** (`lvl.waves.matrices`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 87 | `lsn.waves.matrix-arrays` Matrices as arrays | Read entries by row and column, add matrices and multiply by scalars, transpose, and state when each operation is defined | Two shops' sales of three products on two days: the total for both shops in one step | `matrix-grid`, `value-table` | Trap: adding matrices of different shapes; $a_{ij}$ read column first. Edge: the zero matrix; the transpose swaps rows and columns | A, N, C, N |
| 88 | `lsn.waves.matrix-multiply` Matrix multiplication | Multiply matrices row by column, predict the product's shape, and show by example that $AB \ne BA$ | A price list times a shopping list gives a bill. Two shops and three shoppers: every bill at once | `matrix-grid` (row and column highlight), `matrix-multiply` | Trap: multiplying entry by entry; assuming $AB = BA$. Edge: $AB$ defined while $BA$ is not; $AB = 0$ with neither factor zero | A, N, C, M |
| 89 | `lsn.waves.matrix-transform` Matrices as transformations | Find the image of a point under a $2 \times 2$ matrix and read the matrix from the images of $(1, 0)$ and $(0, 1)$ | Drag the tips of $\hat{\imath}$ and $\hat{\jmath}$. The whole grid follows. Where does $(2, 3)$ go? | `linear-map`, `matrix-grid` | Trap: images written as rows instead of columns. Edge: lines stay lines and the origin stays put, so a translation is not a $2 \times 2$ matrix map | A, P, C, N |
| 90 | `lsn.waves.rotation-matrix` Rotations, reflections and composition | Derive the rotation matrix from the unit circle and confirm it with the compound-angle formulas, write reflection, enlargement and shear matrices, and compose maps in the right order | Rotate by $30°$, then by $45°$. One matrix for both? | `linear-map`, `unit-circle`, `derivation-steps` | Trap: $BA$ read as "do $B$ first" (it means $A$ first). Edge: rotations about the origin commute with each other; a rotation and a reflection usually do not | A, A, C, O |
| 91 | `lsn.waves.determinant` Determinants: the area scale factor | Compute $ad - bc$, interpret it as the signed area scale factor, and identify singular matrices | The unit square becomes a parallelogram. What is its area? | `linear-map` (area readout), `determinant-lab` | Trap: $ad + bc$; a negative determinant read as "negative area" (it means the map flips orientation). Edge: determinant 0 squashes the plane onto a line or a point; $\det(AB) = \det A \det B$ | N, C, N, M |
| 92 | `lsn.waves.inverse-systems` Inverses and solving linear systems | Find the inverse of a $2 \times 2$ matrix, use it to solve a $2 \times 2$ system, and recognise when no unique solution exists | Which matrix sends the transformed grid back where it started? | `matrix-grid`, `linear-map`, `equation-stack` | Trap: inverting entry by entry; $(AB)^{-1} = A^{-1}B^{-1}$ (it is $B^{-1}A^{-1}$). Edge: a singular system has no solution or infinitely many (0.2's parallel and coincident lines) | A, N, C, N |

Transfer screens: lesson 88 values a portfolio as holdings times prices; lesson 92 solves 0.2's two-state replication portfolio with an inverse matrix and previews a Markov transition matrix (1.5).

**Level T6: Complex numbers in polar form** (`lvl.waves.complex`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 93 | `lsn.waves.argand-loci` Distance on the Argand diagram | Read $\lvert z - w \rvert$ as the distance between $z$ and $w$, and sketch and describe the loci $\lvert z - a \rvert = r$, $\lvert z - a \rvert = \lvert z - b \rvert$ and $\arg(z - a) = \theta$ and the regions they bound, building on 0.2 lessons 84 to 87 | Mark five complex numbers $z$ with $\lvert z - 3 - 4i \rvert = 5$. What shape do they make, and does it pass through 0? | `complex-plane` (locus tracer; region shading), `region-select` | Trap: $\lvert z - 3 - 4i \rvert = 5$ read as centred at $-3 - 4i$; $\lvert a + bi \rvert = a + b$. Edge: $\lvert z - a \rvert = \lvert z - b \rvert$ is the perpendicular bisector of S4 lesson 18; $\lvert z \rvert^2 = z\bar{z}$, which is why dividing works by multiplying by the conjugate | P, R, C, X |
| 94 | `lsn.waves.mod-arg` Modulus-argument form | Convert between $a + bi$ and $r(\cos\theta + i\sin\theta)$, choosing the principal argument in $(-\pi, \pi]$ by quadrant | $-1 - i$ has modulus $\sqrt{2}$. What is its argument? The calculator's $\tan^{-1}$ says $45°$ | `complex-plane` (rays and circles) | Trap: the argument read straight from $\tan^{-1}\frac{b}{a}$. Edge: 0 has no argument; the principal range is a convention | X, N, C, N |
| 95 | `lsn.waves.multiply-rotate` Multiplication rotates and scales | Show with the compound-angle formulas that multiplying complex numbers multiplies the moduli and adds the arguments, and multiply and divide in polar form | Multiply by $1 + i$ three times. Predict the size and direction before computing | `complex-plane`, `derivation-steps` | Trap: arguments multiplied. Edge: multiplying by $i$ is the $90°$ rotation matrix $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ of lesson 90 | N, X, O, C |
| 96 | `lsn.waves.de-moivre-roots` De Moivre's theorem and roots of unity | Compute powers with De Moivre's theorem and find the $n$ nth roots of a complex number as equally spaced points on a circle | Find every $z$ with $z^3 = 1$. There are three. Where are they? | `complex-plane` (roots of unity; $n$ slider) | Trap: only the real cube root. Edge: the $n$ roots of unity add to 0; the roots of $z^n = w$ lie on a circle of radius $\lvert w \rvert^{1/n}$ | X, N, C, P |
| 97 | `lsn.waves.euler-preview` Euler's formula, previewed | Explain $e^{i\theta} = \cos\theta + i\sin\theta$ as the one sensible meaning for an exponential that turns instead of grows, and rewrite polar form with it | $e^{a+b} = e^a e^b$ turns adding into multiplying. Which function of $\theta$ turns adding angles into multiplying rotations? | `complex-plane` (compounding $(1 + \frac{i\theta}{n})^n$), `multiplier-chain` | Trap: "$e^{i\pi} = -1$, so $e$ is negative". Edge: $(1 + \frac{i\theta}{n})^n$ lands on the unit circle at angle $\theta$ as $n$ grows: the same limit as lesson 47's compounding, turned sideways | X, N, C, M |

Transfer screens: lesson 96 places roots of unity as the frequencies of the discrete Fourier transform; lesson 97 names $e^{i\theta}$ in Fourier analysis and characteristic functions (Stage 1 and 2).

#### Course C: Counting, Chance and Data (`crs.chance`, 5 levels, 26 lessons)

Counting without listing, then probability as counting with a denominator, then the binomial theorem that joins them, then the GCSE statistics a Higher paper tests. It hands 1.5 a learner who already shrinks sample spaces, counts by complement and distrusts a confident chart.

**Level C1: Counting arrangements** (`lvl.chance.arrangements`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 98 | `lsn.chance.permutations` Arrangements and factorials | Count ordered arrangements of $n$ objects and of $r$ from $n$, derive $\frac{n!}{(n - r)!}$ from the product rule (0.1 lesson 13), and explain $0! = 1$ | In how many orders can 8 runners finish? How many different podiums (gold, silver, bronze)? | `counting-slots`, `tree-diagram` (count mode) | Trap: adding the choices; $n^r$ when objects cannot repeat. Edge: $0! = 1$ makes $\frac{n!}{(n - n)!} = n!$ work; $70!$ already exceeds $10^{100}$ | N, N, C, X |
| 99 | `lsn.chance.combinations` Combinations | Derive $\binom{n}{r} = \frac{n!}{r!(n - r)!}$ by collapsing the $r!$ orders of each selection, and decide from the wording whether order matters | A committee of 3 from 8 people: how many? The same as the number of podiums? | `counting-slots` (collapse mode), `pascal-triangle` | Trap: arrangements counted where order does not matter, and the reverse. Edge: $\binom{n}{r} = \binom{n}{n - r}$, because choosing who is in chooses who is out | N, C, X, N |
| 100 | `lsn.chance.repeats-circles` Repeated objects and circular arrangements | Count arrangements with repeated objects as $\frac{n!}{a!\,b!\cdots}$ and circular arrangements as $(n - 1)!$ | How many different arrangements of the letters of MISSISSIPPI are there? | `counting-slots` (identical tokens), `card-sort` | Trap: dividing by the wrong factorials; rotations of a round table counted as different. Edge: a necklace that can also be flipped over divides by 2 again (for 3 or more beads) | N, N, C, N |
| 101 | `lsn.chance.restrictions` Restrictions and the complement | Count with "together" (glue the items), "apart" (gaps or complement) and "at least one" (complement) restrictions | Five people in a row; Ann and Ben refuse to sit together. How many seatings? | `counting-slots` (glue tokens), `venn-diagram` | Trap: "at least one" counted as "pick one, then anything", which counts some cases twice. Edge: the complement is often the only practical route | N, N, C, N |
| 102 | `lsn.chance.four-cases` Order and replacement: the four cases | Classify a selection by whether order matters and whether repetition is allowed, and count each case, including stars and bars $\binom{n + r - 1}{r}$ | Three scoops from five flavours, repeats allowed, order ignored: how many cones? | `counting-slots` (stars-and-bars mode), `card-sort` | Trap: $\frac{n^r}{r!}$ for unordered selections with repetition, which is not even a whole number in general. Edge: stars and bars also counts non-negative whole solutions of $x_1 + \dots + x_n = r$ | S, N, N, C |

Transfer screens: lesson 98 counts order-book priority sequences; lesson 102 counts ways to split 10 identical lots across 4 funds.

**Level C2: Counting principles** (`lvl.chance.principles`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 103 | `lsn.chance.inclusion-exclusion` Inclusion-exclusion | Count unions of two and three sets with inclusion-exclusion and check the count region by region on a Venn diagram | How many numbers from 1 to 1,000 are divisible by 3, 5 or 7? (543) | `venn-diagram` (three sets with counts), `numeric-input` | Trap: subtracting the triple overlap (it is added back). Edge: the alternating pattern continues for any number of sets | N, N, C, N |
| 104 | `lsn.chance.pigeonhole` The pigeonhole principle | Prove existence statements with the pigeonhole principle, including the general form $\lceil \frac{n}{k} \rceil$ | In a room of 367 people, must two share a birthday? With 23? | `token-tray` (boxes and tokens), `free-response` | Trap: expecting the principle to say which box; "must" confused with "likely" (23 people is the birthday problem, lesson 117). Edge: choosing the boxes is the creative step: five points in a unit square, four small squares, so two points lie within $\frac{\sqrt{2}}{2}$ | N, C, M, O |
| 105 | `lsn.chance.bijections` Counting by bijection: lattice paths | Count lattice paths as words of R and U moves, and count one set by pairing it one to one with another | How many shortest routes along a $6 \times 4$ grid of streets from one corner to the opposite one? | `pascal-triangle` (lattice mode), `counting-slots` | Trap: $6 \times 4 = 24$. Edge: with a blocked junction, subtract the paths through it | N, N, C, N |
| 106 | `lsn.chance.derangements` Derangements | Count derangements with inclusion-exclusion and see the fraction settle at $\frac{1}{e}$ | Five people hand in their hats and get them back at random. What is the chance nobody gets their own? | `counting-slots`, `trial-simulator`, `value-table` | Trap: $(\frac{4}{5})^5 \approx 0.328$, treating the events as independent (the answer is $\frac{44}{120} \approx 0.367$). Edge: $\frac{D_n}{n!} \to \frac{1}{e} \approx 0.368$ so fast that the answer barely depends on $n$ beyond 5 | N, N, C, N |

Transfer screens: lesson 105 counts the paths to each node of a binomial pricing tree (1.7); lesson 106 is the Secret Santa interview question.

**Level C3: The binomial theorem** (`lvl.chance.binomial`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 107 | `lsn.chance.pascal` Pascal's triangle | Build Pascal's triangle by adding, identify its entries as $\binom{n}{k}$, and prove Pascal's rule $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$ by counting | Count the lattice paths to every junction of a grid. What numbers appear? | `pascal-triangle` | Trap: rows and positions counted from 1 instead of 0. Edge: row sums are powers of 2; the triangle's odd entries make the Sierpinski pattern | N, X, C, N |
| 108 | `lsn.chance.binomial-expansion` Expanding $(a + b)^n$ | Expand $(a + b)^n$ by choosing $a$ or $b$ from each bracket, and explain why $a^{n-k}b^k$ has coefficient $\binom{n}{k}$ | Expand $(a + b)^3$ by listing all eight words of $a$s and $b$s. Group them | `binomial-expander`, `pascal-triangle` | Trap: $(a + b)^n = a^n + b^n$. Edge: $(a - b)^n$ alternates signs; $n = 0$ gives 1 | X, X, C, N |
| 109 | `lsn.chance.binomial-terms` Particular terms and coefficients | Find a named term or coefficient of $(p + qx)^n$, including negative and fractional coefficients and the term independent of $x$ | What is the coefficient of $x^3$ in $(2 - 3x)^7$? ($-15{,}120$) | `binomial-expander` (term picker), `expression-input` | Trap: forgetting to raise $-3$ to the third power or 2 to the fourth; dropping the sign. Edge: in $(x + \frac{1}{x^2})^9$ the constant term needs $9 - 3k = 0$, so $k = 3$ | N, N, X, C |
| 110 | `lsn.chance.binomial-identities` Binomial identities and combinatorial proof | Prove $\sum_k \binom{n}{k} = 2^n$, symmetry, Pascal's rule and the hockey-stick identity by counting one set two ways and by substituting into the binomial theorem | Add the entries of each row of Pascal's triangle. Why powers of 2? | `pascal-triangle` (highlight sums), `derivation-steps`, `free-response` | Trap: "proof" by checking a few rows. Edge: $\sum_k (-1)^k \binom{n}{k} = 0$ for $n \ge 1$ (put $a = 1$, $b = -1$): a set has as many even-sized subsets as odd-sized ones | O, N, C, M |
| 111 | `lsn.chance.binomial-approx` Approximations and the binomial series | Use $(1 + x)^n \approx 1 + nx + \frac{n(n - 1)}{2}x^2$ for small $x$, and expand $(1 + x)^n$ for rational $n$ with the validity condition $\lvert x \rvert < 1$ | Estimate $1.01^{10}$ in your head. Then $\sqrt{1.02}$ | `binomial-expander` (truncation against the curve), `graph-explorer` | Trap: using the series outside $\lvert x \rvert < 1$; expanding $(2 + x)^{-1}$ without first taking out the 2, which changes the condition to $\lvert x \rvert < 2$. Edge: for whole $n$ the series stops; for any other $n$ it never does | N, X, I, C |

Transfer screens: lesson 111 uses $(1 + r)^n \approx 1 + nr$ for small returns and previews Bernoulli's inequality (lesson 131); lesson 107 previews the binomial distribution of 1.5.

**Level C4: Probability** (`lvl.chance.probability`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 112 | `lsn.chance.equally-likely` Probability from equally likely outcomes | List a sample space, compute a probability as favourable over total for equally likely outcomes, and place it on the 0 to 1 scale | Two dice: is a total of 7 or a total of 8 more likely? | `outcome-grid`, `number-line` (probability scale) | Trap: the totals 2 to 12 treated as 11 equally likely outcomes. Edge: probability 0 means impossible here; in continuous settings (1.5) a probability-0 event can happen | N, R, C, N |
| 113 | `lsn.chance.relative-frequency` Relative frequency and expected frequency | Record experiments in frequency trees, estimate a probability from a relative frequency, compute expected frequencies, and explain why estimates settle as trials grow | A drawing pin lands point up 37 times in 100 throws. What is the probability? Would you bet after 10 throws? | `trial-simulator` (predict first), `value-table` | Trap: the gambler's fallacy ("after five heads a tail is due"). Edge: the spread of the estimate shrinks like $\frac{1}{\sqrt{n}}$, so 100 times the trials buys 10 times the precision | N, N, C, M |
| 114 | `lsn.chance.venn-addition` Venn diagrams and the addition rule | Use set notation and Venn diagrams to compute $P(A \cup B) = P(A) + P(B) - P(A \cap B)$, complements and mutually exclusive events | 60% of a class study maths, 45% physics, 30% both. What fraction study neither? | `venn-diagram`, `region-select` | Trap: adding without removing the overlap (a total over 1 is the warning). Edge: mutually exclusive events are not independent (unless one has probability 0) | R, N, N, C |
| 115 | `lsn.chance.trees` Tree diagrams, independence and replacement | Build two- and three-stage tree diagrams, multiply along branches, add across them, and change the probabilities when drawing without replacement | A bag has 5 red and 3 blue counters. Two are taken without replacement. What is the chance they differ in colour? | `tree-diagram`, `trial-simulator` | Trap: keeping the first draw's probabilities for the second; adding along a branch. Edge: $P(\text{at least one}) = 1 - P(\text{none})$; independence means $P(A \cap B) = P(A)P(B)$, a fact to check, not assume | N, N, M, C |
| 116 | `lsn.chance.conditional` Conditional probability | Compute $P(A \mid B)$ from two-way tables, Venn diagrams and trees by shrinking the sample space to $B$ | Roll two dice. Given that at least one shows a 5, what is the chance the total is 10? | `outcome-grid` (condition shrink), `venn-diagram`, `tree-diagram` | Trap: $P(A \mid B)$ taken as $P(B \mid A)$; "at least one 5" read as "the first die is 5". Edge: a condition can raise, lower or leave a probability unchanged, and unchanged is independence | N, R, C, N |
| 117 | `lsn.chance.counting-probability` Probability by counting | Compute probabilities in card, committee and birthday problems using permutations and combinations, matching ordered or unordered counts top and bottom | In a room of 23 people, is a shared birthday more or less likely than not? | `counting-slots`, `trial-simulator`, `graph-explorer` (probability against $n$) | Trap: $\frac{23}{365}$; an ordered count on top over an unordered count below. Edge: the probability passes 50% at 23 people and 99% at 57 | N, N, C, N |

Transfer screens: lesson 116 is the GCSE-level precursor of the 1.5 lesson "Shrinking the sample space"; lesson 117 counts hash collisions (1.8).

**Level C5: Data and statistics** (`lvl.chance.data`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 118 | `lsn.chance.averages` Averages and spread | Compute mean, median, mode and range, explain the mean as the balance point, and choose the average that resists outliers | Ten employees earn £30,000 and the owner earns £1,000,000. What is the "average" salary? | `dot-plot-stats` (fulcrum), `numeric-input` | Trap: the median of unsorted data; the mean assumed typical. Edge: the mean is the number that minimises squared deviations (0.2 lesson 75) and the median the number that minimises absolute deviations, so "which average" is a choice of how errors are penalised; a data set can have no mode or several | N, N, C, M |
| 119 | `lsn.chance.grouped-data` Frequency tables, charts and grouped data | Compute a mean from a frequency table, estimate a mean from grouped data with midpoints, find the modal and median classes, and read pie charts, time-series graphs and frequency polygons | Commute times in 10-minute classes. Estimate the mean | `value-table`, `stat-chart` (frequency polygon, pie, time series) | Trap: dividing $\sum fx$ by the number of classes; using class widths instead of midpoints. Edge: the estimate can miss the true mean; an open-ended class needs an assumed width | N, N, C, N |
| 120 | `lsn.chance.cumulative-box` Cumulative frequency, quartiles and box plots | Draw and read cumulative frequency graphs, find the median and quartiles, draw box plots, and compare distributions by median and interquartile range | Two classes' test results: which did better, and which was more consistent? | `stat-chart` (cumulative frequency, box plot), `dot-plot-stats` | Trap: plotting at class midpoints instead of upper boundaries; comparing ranges instead of interquartile ranges. Edge: quartile conventions differ ($\frac{n+1}{4}$, $\frac{n}{4}$, software interpolation), so every item states its convention | N, N, P, C |
| 121 | `lsn.chance.histograms` Histograms with unequal widths | Draw and read histograms with frequency density, where area is frequency | Ages grouped 0 to 10, 10 to 20, 20 to 50 and 50 to 100. A bar chart makes the last group look huge. Fix it | `stat-chart` (histogram with area tiles) | Trap: bar height taken as frequency. Edge: a frequency density histogram, scaled to total area 1, is the ancestor of the probability density function (1.5) | N, N, P, C |
| 122 | `lsn.chance.scatter-correlation` Scatter graphs, correlation and causation | Describe correlation by direction and strength, interpolate from a line of best fit through the mean point (0.2 lesson 46 fitted lines by eye), and explain three non-causal sources of correlation: a confounder, reverse causation and coincidence in many comparisons | Ice-cream sales and drownings rise together. Should ice cream be banned? | `scatter-fit`, `value-table` | Trap: causation read from correlation; extrapolating far outside the data. Edge: zero linear correlation can hide a perfect curved relationship ($y = x^2$ on symmetric $x$); among 100 pairs of unrelated random series, a few correlate strongly by chance | C, P, N, M |
| 123 | `lsn.chance.sampling-bias` Sampling and bias | Identify biased samples (self-selection, non-response, survivorship), use simple random and stratified sampling, and estimate a population by capture-recapture | An online poll finds that 70% of people own a smartphone. What is wrong with it? | `trial-simulator` (sampling from a population), `stat-chart`, `double-number-line` | Trap: "a bigger sample fixes bias" (it shrinks noise, not bias). Edge: capture-recapture assumes a closed, well-mixed population; a fund league table that lists only funds still open overstates average returns (survivorship) | M, N, C, S |

Transfer screens: lesson 122 warns about spurious correlations in backtests (Stage 2); lesson 123 shows survivorship bias in fund performance tables.

#### Course R: Proof, Limits and Curves (`crs.rigour`, 5 levels, 23 lessons)

The bridge to university mathematics: logic and the main proof methods, induction, the rational functions and partial fractions that calculus integrates, the conics and parametric curves it differentiates, and limits, the idea every derivative is built on. It ends where 1.3 Calculus begins.

**Level R1: Logic and proof** (`lvl.rigour.logic`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 124 | `lsn.rigour.implication` Statements and implication | Distinguish a statement from its converse and contrapositive, and use $\Rightarrow$, $\Leftarrow$, $\Leftrightarrow$, "necessary" and "sufficient" correctly | "If it rains, the pitch is wet." The pitch is wet. Did it rain? | `card-sort` (statement, converse, contrapositive), `venn-diagram` (subset view), `choice` | Trap: affirming the consequent (assuming the converse). Edge: an implication with a false premise counts as true (vacuous truth) | S, M, C, O |
| 125 | `lsn.rigour.quantifiers` Quantifiers, negation and counterexamples | Write and negate statements with "for all" and "there exists", and disprove a universal claim with one counterexample | Put $n$ points on a circle and join every pair. The regions number 1, 2, 4, 8, 16 for $n = 1$ to 5. Is it 32 for $n = 6$? (It is 31) | `geometry-board` (points on a circle; region counter), `value-table`, `choice` | Trap: negating "all are" as "none are"; five examples offered as proof of a universal. Edge: the true count is $\binom{n}{4} + \binom{n}{2} + 1$, which agrees with $2^{n-1}$ for $n \le 5$ and never again | C, N, S, M |
| 126 | `lsn.rigour.direct-cases` Direct proof, cases and exhaustion | Write direct proofs and proofs by cases (odd and even, remainders on division by 3), building on 0.2 lesson 17 | Prove that $n^3 - n$ is always divisible by 6 | `derivation-steps`, `free-response` | Trap: proving one case only; algebra that starts from the conclusion. Edge: exhaustion is valid when the cases are finite and cover everything | O, O, C, M |
| 127 | `lsn.rigour.contrapositive-contradiction` Contrapositive and contradiction | Prove statements by contrapositive and by contradiction, including that $\log_2 3$ is irrational | Is $\log_2 3$ a fraction? Suppose $2^{p/q} = 3$ | `derivation-steps`, `free-response` | Trap: proving the converse instead of the contrapositive; a contradiction proof that never states what it assumes. Edge: the $\log_2 3$ proof ends on parity ($2^p$ even, $3^q$ odd), a contradiction 0.1's $\sqrt{2}$ proof did not need | O, C, O, M |
| 128 | `lsn.rigour.broken-proofs` Spotting broken proofs | Locate the faulty step in invalid arguments: division by zero, circular reasoning, false generalisation, and a picture taken as a proof | A "proof" that $1 = 2$. Find the line that breaks | `derivation-steps` (find-the-flaw mode), `card-sort`, `geometry-board` (dissection) | Trap: accepting a step because it "looks algebraic". Edge: four pieces of an $8 \times 8$ square seem to rearrange into a $5 \times 13$ rectangle, "proving" $64 = 65$; the pieces' slopes $\frac{3}{8}$ and $\frac{2}{5}$ differ, so the long diagonal is a thin parallelogram of area 1 (squaring both sides, 0.2 lesson 111's flaw, appears in the quiz) | C, C, S, O |

Transfer screens: none forced; this level is what makes the Stage 1 finals readable.

**Level R2: Proof by induction** (`lvl.rigour.induction`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 129 | `lsn.rigour.induction-idea` The domino principle | State the base case and the inductive step and explain why both are needed | Dominoes: if each one falls when the one before falls, do they all fall? | `induction-chain` | Trap: proving the step and skipping the base case. Edge: "$n^2 + n$ is odd" has a valid step ($k^2 + k$ odd forces $(k+1)^2 + (k+1)$ odd) and is false for every $n$, because no base case holds | C, O, M, C |
| 130 | `lsn.rigour.induction-sums` Induction for sums | Prove summation formulas such as $\sum_{k=1}^{n} k^2 = \frac{n(n + 1)(2n + 1)}{6}$ by induction | Guess a formula for $1 + 3 + 5 + \dots + (2n - 1)$ from the first few values, then prove it | `induction-chain`, `sum-visualiser` (odd numbers as square borders), `derivation-steps` | Trap: writing the $k + 1$ statement and "working backwards" to the hypothesis. Edge: induction proves a formula but does not find it; the picture found it | O, X, O, C |
| 131 | `lsn.rigour.induction-divisibility` Induction for divisibility and inequalities | Prove divisibility results such as $3 \mid 4^n + 5$ and inequalities such as Bernoulli's $(1 + x)^n \ge 1 + nx$ for $x \ge -1$ by induction | $4^n + 5$: always a multiple of 3? Prove it | `induction-chain`, `derivation-steps` | Trap: the hypothesis used in the wrong form; Bernoulli's inequality applied with $x < -1$. Edge: $2^n > n^2$ is true at $n = 1$, false at $n = 2, 3, 4$ and true from $n = 5$ on, so the base case is $n = 5$, where the unbroken run begins, not the first $n$ that happens to work | O, O, N, C |
| 132 | `lsn.rigour.induction-recurrences` Recurrences, strong induction, and where induction fails | Prove closed forms of recurrences by induction (including strong induction) and identify flawed induction arguments | "All horses are the same colour." Find the broken step | `induction-chain`, `derivation-steps` | Trap: missing that the step from $n = 1$ to $n = 2$ fails because the two groups do not overlap. Edge: strong induction proves the Fibonacci bound $F_n < 2^n$ | O, C, O, M |

Transfer screens: lesson 132 proves the closed form of the G1 loan recurrence; induction returns in 1.8 as the correctness proof of recursive algorithms.

**Level R3: Rational functions and partial fractions** (`lvl.rigour.rational`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 133 | `lsn.rigour.rational-sketching` Sketching rational functions: oblique asymptotes and multiplicity | Find oblique asymptotes by polynomial division, decide the behaviour on each side of a vertical asymptote from the multiplicity of the factor, and sketch a rational function from its intercepts, asymptotes and sign chart (0.2 lesson 99 met vertical and horizontal asymptotes and holes) | Far from the origin, $y = \frac{x^2 + 1}{x - 1}$ looks like a straight line, but not a horizontal one. Which line? ($y = x + 1$) | `graph-explorer` (asymptote overlays; zoom out), `sign-chart`, `equation-workbench` (division) | Trap: the horizontal-asymptote rule applied when the numerator's degree is higher. Edge: at a squared factor such as $\frac{1}{(x - 2)^2}$ the graph goes the same way on both sides of the asymptote; at a single factor it changes sign | N, P, C, X |
| 134 | `lsn.rigour.rational-inequalities` Rational inequalities | Solve rational inequalities with sign charts, never multiplying by an expression of unknown sign | Solve $\frac{x + 2}{x - 3} > 1$. A friend multiplies both sides by $x - 3$ and concludes every $x$ works. Test $x = 0$ | `sign-chart`, `graph-explorer`, `number-line` | Trap: multiplying by a denominator of unknown sign. Edge: points where the expression is undefined are never solutions, even with $\ge$ | I, I, C, I |
| 135 | `lsn.rigour.partial-fractions` Partial fractions | Split proper rational functions with distinct and repeated linear factors into partial fractions by substitution and by comparing coefficients | Work out $\frac{1}{x - 1} - \frac{1}{x + 1}$. Now run it backwards | `equation-workbench`, `expression-input` | Trap: decomposing an improper fraction without dividing first; one term only for a repeated factor. Edge: the cover-up method finds each coefficient of a distinct factor in seconds | X, X, C, N |
| 136 | `lsn.rigour.partial-fractions-sums` Partial fractions at work: telescoping | Use partial fractions to sum series such as $\sum \frac{2}{k(k + 2)}$ and to prepare integrands for 1.3 | $\sum_{k=1}^{n} \frac{2}{k(k + 2)}$: what happens as $n$ grows? ($\frac{3}{2}$) | `sum-visualiser` (cancellation), `series-explorer` | Trap: assuming neighbours cancel when the gap is 2 (two terms survive at each end). Edge: $\sum \frac{1}{k}$ diverges although its terms go to 0, so telescoping is not a test of convergence | N, X, C, N |

Transfer screens: lesson 135 prepares the integrals of 1.3; lesson 136 reuses G5's telescoping.

**Level R4: Conics and parametric curves** (`lvl.rigour.conics`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 137 | `lsn.rigour.parabola-focus` The parabola as a conic | Derive $y^2 = 4ax$ from a focus $(a, 0)$ and directrix $x = -a$, and explain the reflective property | Satellite dishes are parabolic. Why does every incoming ray hit one point? | `geometry-board` (conic-locus preset), `graph-explorer` | Trap: the focus placed on the curve. Edge: every parabola is similar to every other; only the scale differs | X, N, C, P |
| 138 | `lsn.rigour.ellipse` The ellipse | Construct an ellipse with two pins and a loop of string, derive $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$, and find the foci and axes | Pin a loop of string at two points and trace with a pencil | `geometry-board` (two-pin string), `graph-explorer` (implicit curves) | Trap: $c^2 = a^2 + b^2$ (for an ellipse $c^2 = a^2 - b^2$). Edge: a circle is an ellipse whose foci coincide; planets orbit with the Sun at one focus | N, X, C, P |
| 139 | `lsn.rigour.hyperbola` The hyperbola | Define the hyperbola by a constant difference of distances, derive $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$, and find its asymptotes | Two microphones hear a bang 1 millisecond apart. Where can the bang have been? | `geometry-board`, `graph-explorer` | Trap: asymptotes $y = \pm\frac{a}{b}x$ instead of $\pm\frac{b}{a}x$. Edge: $y = \frac{1}{x}$ is a hyperbola turned through $45°$ | X, N, C, P |
| 140 | `lsn.rigour.identify-conics` Identifying conics by completing the square | Put second-degree equations without an $xy$ term into standard form and name the conic, its centre and its key features | $4x^2 + 9y^2 - 16x + 18y - 11 = 0$: what curve is this? | `equation-workbench`, `graph-explorer` | Trap: sign slips when completing the square with a coefficient outside the bracket. Edge: degenerate cases: a point, a pair of lines, or nothing at all ($x^2 + y^2 + 1 = 0$) | C, X, N, M |
| 141 | `lsn.rigour.parametric` Parametric curves | Plot curves given by $x = f(t)$, $y = g(t)$, eliminate the parameter, and parametrise circles and ellipses | A point moves with $x = \cos t$, $y = \sin t$. Then $x = 3\cos t$, $y = 2\sin t$. Then $x = t^2$, $y = t^3$ | `graph-explorer` (parametric curves; $t$ slider) | Trap: eliminating the parameter loses the direction and the domain ($x = \sin^2 t$, $y = \cos^2 t$ traces only the segment of $x + y = 1$ in the first quadrant). Edge: one curve can be traced by different parametrisations at different speeds | P, X, C, N |

Transfer screens: lesson 141 draws a 2D random walk and a price-volume path as parametric curves in time.

**Level R5: Limits and continuity** (`lvl.rigour.limits`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 142 | `lsn.rigour.approach` Approaching a value | Estimate limits from tables and graphs, including for functions undefined at the point | $\frac{\sin x}{x}$ at $x = 0$ is $\frac{0}{0}$. What happens as $x$ approaches 0? | `graph-explorer` (approach overlay), `value-table`, `limit-explorer` (light mode) | Trap: the limit taken as the value at the point; "$\frac{0}{0}$, so no limit". Edge: a table can mislead: $\sin\frac{\pi}{x}$ at $x = 1, \frac{1}{2}, \frac{1}{3}, \dots$ gives all zeros, yet there is no limit | N, N, C, M |
| 143 | `lsn.rigour.one-sided` One-sided limits and when limits fail | Compute one-sided limits and classify failures as jumps, infinite limits or oscillation | The floor function at $x = 2$: what happens from the left and from the right? | `graph-explorer` (approach from each side), `choice` | Trap: "both one-sided limits exist, so the limit exists" (they must also agree). Edge: $e^{1/x}$ tends to $+\infty$ from the right of 0 and to 0 from the left: one side infinite, the other finite; "the limit is infinity" describes how a limit fails | N, C, M, S |
| 144 | `lsn.rigour.limit-algebra` Limit laws and algebraic techniques | Evaluate limits with the limit laws, factorising, rationalising, and the standard limit $\frac{\sin x}{x} \to 1$ | $\lim_{x \to 4} \frac{\sqrt{x} - 2}{x - 4}$ ($\frac{1}{4}$) | `equation-workbench`, `graph-explorer` | Trap: stopping at $\frac{0}{0}$, or declaring $\frac{0}{0} = 1$. Edge: $(1 + \frac{1}{n})^n$ is a "$1^\infty$" form whose limit is $e$ (lesson 47) | N, N, X, C |
| 145 | `lsn.rigour.limits-infinity` Limits at infinity and dominant terms | Find limits as $x \to \pm\infty$ of rational and exponential expressions by dividing by the dominant term | Evaluate $\frac{3x^2 + 5}{x^2 - 2x}$ at $x = 1{,}000{,}000$ | `graph-explorer` (zoom out), `value-table` | Trap: "$\frac{\infty}{\infty} = 1$" and "$\infty - \infty = 0$". Edge: $\sqrt{x^2 + x} - x \to \frac{1}{2}$, not 0 | N, N, C, N |
| 146 | `lsn.rigour.continuity-ivt` Continuity and the intermediate value theorem | Decide continuity at a point with the three conditions, and use the intermediate value theorem to prove that a root exists | You climb a mountain from 8 am to 4 pm and come down the same path from 8 am to 4 pm the next day. Were you at the same height at the same time on both days? | `graph-explorer`, `sign-chart` | Trap: "a sign change means a root" ($\frac{1}{x}$ changes sign with no root, because it is not continuous). Edge: the theorem says a root exists, not where; 0.2's bisection finds it | M, C, N, O |

Transfer screens: lesson 146 connects bisection to finding an implied volatility (Stage 2 project 3); lesson 144 is the first derivative in disguise, $\frac{d}{dx}\sqrt{x}$ at $x = 4$.

**Coverage check for 0.3.** Curriculum cover list: exponentials and logarithms (G2 to G4), trigonometry (S6, S7, T1 to T4), sequences and series (G1, G5), binomial expansion (C3), vectors (S8), counting with permutations and combinations (C1, C2). Khan Academy Precalculus units as listed in ASSESSMENT.md 2.11: complex numbers (0.2 Q6, T6), polynomials (0.2 Q, R3), composite and inverse functions (0.2 F, with G3 and T3 as inverse pairs), rational functions (0.2, R3), conic sections (0.2 circle, R4), matrices (T5), vectors (S8), probability and combinatorics (C1 to C4), series (G5), limits and continuity (R5). GCSE Higher geometry and measures: S1 to S8 and T2 (trigonometric graphs in degrees as well as radians); GCSE probability and statistics: C4, C5 and 0.1 lesson 13. Added for a top programme: proof methods and induction (R1, R2), growth hierarchy and underflow (G4), present value (G5), Euler's formula (T6), cosine similarity and projection (S8).

**GCSE Higher geometry, probability and statistics content** (DfE subject content 2013 codes, as the sibling file maps N, A and R [check the code list against the published document]):

| Codes | Content | Lessons |
|---|---|---|
| G1, G3, G4 | Conventions; angle facts, parallel lines, triangle and polygon sums; special quadrilaterals | 1 to 3 |
| G2 | Ruler-and-compass constructions, loci, shortest distance to a line | 18 |
| G5, G6, G19 | Congruence criteria; deriving results and simple proofs; similarity with lengths, areas and volumes | 12 to 14, 23 |
| G7, G8, G24 | Transformations including fractional and negative enlargement; combinations and invariance; translations as vectors | 15 to 17, 33 |
| G9, G10 | Circle vocabulary; the circle theorems and their proofs | 6, 7, 19 to 23 |
| G11 | Geometry on coordinate axes | 0.2 lessons 35 to 40, 72; 0.3 lesson 11 |
| G12, G13 | Properties of solids; plans and elevations | 8 |
| G14, G15 | Units of measure; scale drawings, maps and bearings | 0.1 lesson 30, 0.1 level P2; 0.3 lesson 4 |
| G16, G17, G18 | Areas and volumes of plane shapes, prisms, cylinders, spheres, pyramids, cones and composite solids; arcs and sectors | 5 to 9 |
| G20, G21 | Pythagoras and the trigonometric ratios in two and three dimensions; exact values | 10, 11, 24 to 28 |
| G22, G23 | Sine and cosine rules; area $\frac{1}{2}ab\sin C$ | 29 to 32 |
| G25 | Vector arithmetic and vector proofs | 33 to 35 |
| P1 to P5 | Frequency trees, expected outcomes, relative frequency, exhaustive and exclusive events, the effect of sample size | 112 to 114 |
| P6 to P9 | Systematic listing, possibility spaces, combined and dependent events, conditional probability from tables, trees and Venn diagrams | 0.1 lesson 13; 0.3 lessons 112, 114 to 116 |
| S1, S5 | Sampling and its limits; describing a population | 123 |
| S2, S3 | Tables and charts for categorical and time-series data; histograms with unequal widths; cumulative frequency | 119 to 121 |
| S4 | Comparing distributions with box plots, averages, quartiles and interquartile range | 118 to 120 |
| S6 | Scatter graphs, correlation and causation, lines of best fit, interpolation and extrapolation | 0.2 lesson 46; 0.3 lesson 122 |
| R12 | Similarity and scale factors (the item the sibling file left to a geometry course) | 13, 14 |

### 2.2 Item 0.4 Computer basics

0.4 runs alongside 0.1 from the first week. The three courses can interleave: the planner releases K1 in week 1, B1 in week 2, and Y1 once B2 is done, because a first script needs a folder and a terminal. Lessons that teach something done on the learner's own machine (installing, the exit) use `setup-checklist` with paste-verify, so the app checks what really happened, not what was clicked.

#### Course K: Keyboard Fluency (`crs.keys`, 2 levels, 8 lessons)

Touch typing as a skill built by graded drills, with accuracy first and speed following, then the symbols that code needs and the shortcuts that save hours. Each lesson is short teaching plus a long drill; the daily typing practice lives in practice, not in lessons.

**Level K1: The home row and technique** (`lvl.keys.home-row`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | `lsn.keys.home-row` Home position and the home row | Find the home row by touch from the bumps on F and J, and type the home-row letters at 10 words per minute with 95% accuracy without looking | Type one sentence while watching only the screen. How many errors? | `typing-trainer` (home row only; hand overlay), `speed-timer` | Trap: staying with two-finger hunting because it is faster today (it plateaus, and every look down costs a context switch). Edge: AZERTY and QWERTZ layouts; the trainer reads the layout the operating system reports | W, W, C |
| 2 | `lsn.keys.top-row` Reaching up: the top row | Add the top row with the correct finger for each key and return to home after every reach, at 12 words per minute | Type "were quiet types" with eyes on the screen | `typing-trainer` (top row unlocked) | Trap: moving the whole hand instead of one finger. Edge: T and Y are index-finger stretches, the commonest source of swaps | W, W, C |
| 3 | `lsn.keys.bottom-row` Reaching down: the bottom row | Add the bottom row and type every letter at 15 words per minute with 95% accuracy | Type "zinc box, calm vamp" | `typing-trainer` (all letters) | Trap: the little finger abandoned for Z and the ring finger for X. Edge: B is the index finger's longest reach, from F, not J | W, W, C |
| 4 | `lsn.keys.rhythm` Rhythm, accuracy and the plateau | Type mixed prose at 20 words per minute with 95% accuracy at an even rhythm, and explain why speed follows accuracy | Two typists: 60 words per minute with 10% errors, or 40 with 1%. Who finishes a 500-word email first, corrections included? | `typing-trainer` (metronome; error heat map) | Trap: pushing speed while errors climb. Edge: each error costs two extra keystrokes (the wrong key and the backspace) plus the pause to notice it, so at a 10% error rate a sixth of all keystrokes are waste before the pauses are counted | W, N, C |

**Level K2: Every key, and the shortcuts** (`lvl.keys.all-keys`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 5 | `lsn.keys.shift-punctuation` Capitals and punctuation | Use the Shift key of the opposite hand for capitals and type punctuation by touch | Type "Hello, World." Which Shift did you press? | `typing-trainer` (shift drills) | Trap: same-hand Shift, which strains and slows. Edge: Caps Lock for capitals breaks rhythm and causes "hELLO" | W, W, C |
| 6 | `lsn.keys.numbers` The number row and the numeric keypad | Type digits by touch at 15 words per minute and choose between the number row and the keypad | Type 3.14159 26535 89793 without looking | `typing-trainer` (digits) | Trap: looking down for every digit. Edge: laptops without a keypad; the trainer adapts its drills to the keyboard present | W, W, N |
| 7 | `lsn.keys.code-symbols` Code symbols: brackets, quotes and operators | Type Python's symbols, `() [] {} : = == _ " ' # + - * / < >`, at 20 words per minute on code text | Type `print(f"{x**2:.3f}")` | `typing-trainer` (code mode) | Trap: curly "smart" quotes pasted from a word processor, which Python rejects. Edge: UK and US layouts place `"` and `@` differently and the UK `#` key sits beside Enter [check against the trainer's layout tables] | W, C, W |
| 8 | `lsn.keys.shortcuts` Editing shortcuts | Use copy, cut, paste, undo, redo, select all, save, find, and word-wise movement and selection with the right modifier for the operating system | Move this paragraph to the end without touching the mouse | `typing-trainer` (shortcuts mode) | Trap: Ctrl on macOS (it is Cmd); redo as Ctrl+Y on Windows but Cmd+Shift+Z on macOS. Edge: Ctrl+C in a terminal stops the running program instead of copying | S, C, M |

#### Course B: Workbench: Files, Terminal and Editor (`crs.bench`, 3 levels, 13 lessons)

Where code and data live, how to move around without a mouse, how to install tools without breaking anything, and the edit, save, run loop. `shell-sim` shows every command's effect on a `file-tree` beside it, and tasks are graded by the final state of the file system, not by keystrokes.

**Level B1: Files and folders** (`lvl.bench.files`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 9 | `lsn.bench.files` What a file is | Explain a file as named bytes whose extension tells programs how to read it, and turn on visible extensions in the operating system | Rename `notes.txt` to `notes.py`. What changed inside the file? | `file-tree`, `choice` | Trap: the extension changes the contents (it changes only which program opens it). Edge: `invoice.pdf.exe` disguised by hidden extensions, a common attack | C, S, H |
| 10 | `lsn.bench.folders-paths` Folders and paths | Navigate a folder tree and write absolute and relative paths with `~`, `.` and `..` | Give directions to one file from two different starting folders | `file-tree` ("you are here" pin), `token-tray` (build a path) | Trap: a relative path written from the wrong starting folder; Windows `\` against `/`. Edge: `..` at the root stays at the root; a file has one absolute path but many relative ones | H, H, C |
| 11 | `lsn.bench.file-manager` Working with the file manager | Create, rename, move, copy and delete files and folders in the operating system's file manager, show hidden files, and find where downloads land | Where did the file you just downloaded go? | `file-tree`, `setup-checklist` (per operating system) | Trap: working inside a zip file or the Downloads folder without extracting or moving the files. Edge: hidden "dot" files exist to keep settings out of the way | H, H, C |
| 12 | `lsn.bench.naming` Naming and organising files | Name files and folders so that terminals and code handle them (no spaces, consistent case, dates as YYYY-MM-DD) and lay out a project folder | Sort these by name: `report-2026-1-10`, `report-2026-10-1`, `report-2026-2-3`. What order appears? | `file-tree`, `card-sort` | Trap: spaces in names, which break unquoted commands; `Data.csv` and `data.csv` are different files on Linux but not on default macOS or Windows. Edge: ISO dates sort correctly as text | S, C, H |

**Level B2: The terminal** (`lvl.bench.terminal`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 13 | `lsn.bench.where-am-i` The prompt, `pwd` and `ls` | Open a terminal, read the prompt, and use `pwd` and `ls` (with `-a` and `-l`) to see where you are and what is there | A window with a blinking cursor and no buttons. Find out where you are | `shell-sim`, `file-tree` (linked) | Trap: typing shell commands at Python's `>>>` prompt. Edge: hidden files appear only with `ls -a` | H, C, T |
| 14 | `lsn.bench.cd` Moving around with `cd` | Change folders with `cd` using absolute and relative paths, `~`, `..` and tab completion | Get from your home folder to `projects/zero-to-quant/week1` in as few keystrokes as possible | `shell-sim`, `file-tree` | Trap: `cd` into a name with a space, unquoted. Edge: `cd` alone goes home; `cd -` goes back to the previous folder | H, H, C |
| 15 | `lsn.bench.make-move-delete` Making, copying, moving and deleting | Use `mkdir`, `touch`, `cp`, `mv` and `rm` (with `-r` for folders) to build and rearrange a tree, and explain why `rm` has no undo | Build this project layout using only the keyboard | `shell-sim`, `file-tree` | Trap: `rm` skips the recycle bin; `mv` overwrites an existing file silently. Edge: `mv` also renames; copying a folder needs `cp -r` | H, H, T, C |
| 16 | `lsn.bench.help-history` Flags, help and history | Read a command's help (`--help`, `man`), use flags, and reuse commands with history and tab completion | How do you list files by size, largest first? Find out without a search engine | `shell-sim`, `text-terminal` | Trap: pasting commands from the web unread (the `sudo rm -rf` warning). Edge: Ctrl+C cancels, `q` leaves `man`, Ctrl+R searches history | H, T, C |
| 17 | `lsn.bench.redirect-pipes` Wildcards, redirection and pipes | Use `*`, `>`, `>>` and `\|` to select files, save output and chain commands | Count the `.py` files in a folder in one line | `shell-sim`, `file-tree` | Trap: `>` overwrites (use `>>` to append); `rm *.py` deletes every match. Edge: the shell expands `*` before the command runs, so `ls *.csv` in an empty folder behaves differently across shells | H, T, C, H |

**Level B3: Installing tools and the editor** (`lvl.bench.tools`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 18 | `lsn.bench.install-safely` Installing software safely | Install software from official sources, check what was downloaded, and explain administrator rights and updates | Two download buttons on one page; one is an advert. Which is real? | `setup-checklist`, `choice` | Trap: installers from adverts or mirror sites; clicking through operating-system warnings. Edge: package managers (winget, Homebrew, apt) as the safer route | M, S, C |
| 19 | `lsn.bench.install-python` Installing Python and the PATH | Install Python 3.12 or later, verify the version from the terminal, and fix "command not found" by understanding PATH | You installed Python. The terminal says `python: command not found`. Why? | `setup-checklist` (per operating system, paste-verify), `shell-sim` (PATH demonstration) | Trap: on Windows, the unticked "Add python.exe to PATH" box and the Microsoft Store stub; on macOS and Linux, `python` against `python3`. Edge: two Pythons installed at once; `which python3`, `where python` or `py -0` shows which one runs | H, T, C |
| 20 | `lsn.bench.vscode` VS Code: open a folder, not a file | Install VS Code and its Python extension, open a project folder, use the integrated terminal and select the interpreter | Running a script from VS Code gives "No such file". Which folder is the terminal in? | `workspace-sim`, `setup-checklist` | Trap: opening a single file, so the terminal starts elsewhere; an unsaved file (the dot on its tab) runs the old version. Edge: Restricted Mode for folders not yet trusted | C, H, S |
| 21 | `lsn.bench.editor-workflow` The edit, save, run loop and editor shortcuts | Run the loop of edit, save, run, read the error, fix, in the integrated terminal, and use comment-line, go-to-line, find and multi-cursor | Line 7 has an error. Jump there without scrolling | `workspace-sim`, `code-cell`, `typing-trainer` (editor shortcuts) | Trap: running before saving; fixing the line the message names when the real mistake is on the line before. Edge: turning on auto-save | H, S, C |

#### Course Y: First Programs in Python (`crs.firstpy`, 2 levels, 10 lessons)

Automate the Boring Stuff chapters 1 to 3, taught by predicting before running. Every lesson has a predict-the-output screen, a Parsons or fill-the-blank screen for phones, and a small drill with hidden tests. Python proper is 1.1; this course gives just enough for 0.1 to 0.3's code drills and the exit script.

**Level Y1: Values, variables and decisions** (`lvl.firstpy.values`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 22 | `lsn.firstpy.expressions` Python as a calculator | Evaluate arithmetic expressions in the interactive prompt, including `//`, `%` and `**`, and predict their values and types | What does `7 / 2` give? `7 // 2`? `-7 // 2`? | `code-cell` (prompt mode), `expression-tree` (Python mode), `predict-output` | Trap: `^` for powers (it is bitwise XOR: `2 ^ 3` is 1); `-7 // 2` is $-4$ because `//` rounds down. Edge: `0.1 + 0.2` (0.1 lesson 42) | T, T, N, C |
| 23 | `lsn.firstpy.types` Values and types: `int`, `float`, `str` | Identify types, convert with `int()`, `float()` and `str()`, and predict the errors that mixing them causes | What does `"5" + 5` do? | `predict-output`, `diagnostic-reader`, `code-cell` | Trap: `int("3.7")` fails; `int(3.7)` truncates to 3 rather than rounding. Edge: `"5" * 3` is `"555"` | T, T, C, M |
| 24 | `lsn.firstpy.variables` Variables and assignment | Assign and reassign variables, trace their values line by line, and read `x = x + 1` as an update, not an equation | `a = 1`, `b = a`, `a = 2`. What is `b`? | `code-tracer`, `code-cell` | Trap: `=` read as mathematical equality; a name used before it is assigned (`NameError`). Edge: swapping needs a temporary or `a, b = b, a` | T, T, C, K |
| 25 | `lsn.firstpy.print-input` `print`, `input` and a first script | Write a script that reads input, converts it, prints formatted output with f-strings, and runs from the terminal | Write a script that asks your name and age and prints the year you turn 100 | `workspace-sim`, `code-cell` | Trap: `input()` returns text, so `age + 1` fails. Edge: `f"{x:.2f}"` rounds only for display; the stored value is unchanged | K, T, C |
| 26 | `lsn.firstpy.if` Comparisons, booleans and `if` | Write `if`, `elif` and `else` blocks with comparisons and `and`, `or`, `not`, and predict which branch runs | A shop gives 10% off over £50 and 20% off over £100. Write the rule | `code-cell`, `code-tracer`, `parsons` | Trap: testing "over £50" before "over £100", so the second branch never runs; `=` inside a condition; indentation errors. Edge: `0.1 + 0.2 == 0.3` is `False`, so floats are compared with `math.isclose` | T, K, O, C |

**Level Y2: Loops, functions and errors** (`lvl.firstpy.loops`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 27 | `lsn.firstpy.for-range` `for` loops and `range` | Use `for` with `range(start, stop, step)` and accumulate a running total | Add the numbers 1 to 100 with a loop | `code-tracer`, `code-cell` | Trap: `range(1, 100)` stops at 99. Edge: `range(10, 0, -1)` counts down; an empty range runs zero times | T, K, N, C |
| 28 | `lsn.firstpy.while` `while` loops and `break` | Write `while` loops whose condition eventually becomes false, and stop early with `break` | How many years until £1,000 at 5% has doubled? Loop until it does | `code-tracer`, `code-cell` | Trap: an infinite loop because nothing changes the condition (Ctrl+C stops it). Edge: `while True:` with `break`; the answer, 15 years, is what one line of logarithms gives in 0.3 lesson 53 | T, K, C |
| 29 | `lsn.firstpy.functions` Functions: `def`, parameters and `return` | Define functions with parameters and return values, call them, and tell `return` from `print` | VAT is computed in five places in one script. Write it once | `code-cell`, `function-machine`, `code-tracer` | Trap: `print` instead of `return`, so the caller gets `None`; calling without parentheses. Edge: default parameter values; a function with no `return` gives `None` | T, K, C, M |
| 30 | `lsn.firstpy.errors` Reading errors and tracebacks | Read a traceback from the bottom up, name `SyntaxError`, `NameError`, `TypeError`, `ValueError`, `ZeroDivisionError` and `IndentationError`, and handle bad input with `try` and `except` | The script crashed with nine red lines. Which line is the problem? | `diagnostic-reader`, `code-cell` | Trap: reading the top line first; a bare `except:` that hides every error. Edge: the reported line can come after the real mistake (an unclosed bracket on the line before) | S, T, K |
| 31 | `lsn.firstpy.ten-line-script` Your ten-line script (exit rehearsal) | Make a folder, write a script of at least ten lines using input, a decision, a loop and a function, and run it from the terminal | Write `split.py`, which splits a restaurant bill with a tip between friends (seeded amounts) | `workspace-sim`, `setup-checklist` (exit preview) | Trap: running from the wrong folder ("No such file or directory"). Edge: a text editor that saves `split.py.txt` | K, H, C |

**Coverage check for 0.4.** Curriculum cover list: touch typing (K1, K2), files and folders (B1), installing software (B3), the terminal (B2), a code editor (B3 lessons 20 and 21); the curriculum's resource "first three chapters of Automate the Boring Stuff" (Y1, Y2). Added: editing shortcuts, safe installation and PATH, reading tracebacks, the exit rehearsal.

### 2.3 Item 0.5 Mental arithmetic

#### Course A: Arithmetic at Speed (`crs.speed`, 4 levels, 16 lessons)

Strategies first, each one shown as an identity on an area model or a number line, then drilled to automatic. Lessons are released in step with 0.1, so a strategy never arrives before the number sense it rests on. The Daily 10 (ASSESSMENT.md section 9) carries the practice; lessons teach the moves.

**Level A1: Tables and the Zetamac format** (`lvl.speed.tables`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | `lsn.speed.format` The daily run: format, scoring and technique | Complete a 120-second Zetamac-format run, state the scoring and default ranges, and use auto-advance (no Enter key) | How many correct answers can you give in 120 seconds right now? (your baseline) | `speed-drill`, `speed-timer`, `keypad` | Trap: pressing Enter or rechecking each answer (the next question appears the moment the answer is right) [recalled]. Edge: a phone keypad slows everyone, so the exit counts keyboard runs only | Z, C, N |
| 2 | `lsn.speed.tables-grid` Times tables to 12: the grid folds in half | Recall every product to $12 \times 12$ within 2 seconds, using commutativity to halve the facts and anchors ($\times 10$, $\times 5$, $\times 9$, $\times 11$) for many of the rest | How many facts are in the $12 \times 12$ table? How many must you actually learn? | `times-table-grid` (heat map), `speed-drill` (deck) | Trap: the classic swaps, $7 \times 8 = 54$ and $6 \times 8 = 42$. Edge: commutativity leaves 78 distinct facts of 144 cells, and the anchors (with doubling for $\times 2$) leave 21 hard facts among 3, 4, 6, 7, 8 and 12 | Z, N, N |
| 3 | `lsn.speed.times-two-digit` Twelve times anything up to 100 | Multiply a number from 2 to 12 by a number from 2 to 100 by splitting the larger by place value | $7 \times 86$ in under 4 seconds | `strategy-trainer` (area model), `speed-drill` | Trap: losing the tens product while working out the units. Edge: split the other way when easier: $9 \times 86 = 860 - 86 = 774$ | Z, N, N |
| 4 | `lsn.speed.division-facts` Division as a missing factor | Answer Zetamac divisions by asking "what times this gives that", using an estimate first | $1{,}044 \div 12$ | `strategy-trainer`, `speed-drill` | Trap: long division in the head. Edge: Zetamac divisions always come out whole, so $1{,}044 \div 12 \approx 87$ can be checked in one multiplication | Z, N, N |

**Level A2: Adding and subtracting fast** (`lvl.speed.add-sub`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 5 | `lsn.speed.left-to-right` Adding from the left | Add two two-digit numbers left to right, tens then units, within 2 seconds | $47 + 38$: do you start with $7 + 8$? | `strategy-trainer` (number-line jumps), `speed-drill` | Trap: the written right-to-left method run in the head, holding carries. Edge: three-digit sums such as $247 + 386$ | Z, N, N |
| 6 | `lsn.speed.compensation` Rounding and compensating | Add and subtract near-multiples of 10 by rounding and correcting | $156 - 98$ | `strategy-trainer`, `speed-drill` | Trap: correcting in the wrong direction. Edge: subtracting 98 is subtracting 100 and adding 2 back | Z, N, N |
| 7 | `lsn.speed.counting-up` Subtraction by counting up | Subtract by finding the gap on a number line, counting up from the smaller number | $1{,}000 - 637$ | `strategy-trainer` (number line), `speed-drill` | Trap: borrowing across zeros in the head. Edge: complements to 1,000: every digit to 9 and the last to 10 ($637 \to 363$), which fails when the last digit is 0 | Z, N, N |
| 8 | `lsn.speed.chains` Running totals and chains | Keep a running total through four to six additions and subtractions | Trades: $+37$, $+48$, $-19$, $+26$, $-55$. Net position? | `speed-drill` (chain deck), `strategy-trainer` | Trap: losing the total halfway (say it under your breath). Edge: pairing terms that make round numbers first, when allowed to see the whole chain | Z, N, N |

**Level A3: Multiplying beyond the tables** (`lvl.speed.multiply`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 9 | `lsn.speed.place-value-tricks` $\times 5$, $\times 25$, $\times 9$ and $\times 11$ | Multiply by 5 as $\times 10 \div 2$, by 25 as $\times 100 \div 4$, by 9 as $\times 10 - \times 1$, and by 11 by adding neighbouring digits | $48 \times 25$ in 3 seconds | `strategy-trainer`, `speed-drill` | Trap: $11 \times 78$ written as 7158 (the middle 15 must carry: 858). Edge: the $\times 11$ rule works because $11 = 10 + 1$ | Z, N, N |
| 10 | `lsn.speed.two-by-two` Two-digit by two-digit | Multiply two two-digit numbers in under 10 seconds by splitting one factor and holding the partial products | $34 \times 27$ | `strategy-trainer` (area model), `speed-drill` | Trap: $30 \times 20 + 4 \times 7$, missing the cross terms (0.1 lesson 3's trap returns). Edge: pick the split that makes easy partials: $34 \times 27 = 34 \times 30 - 34 \times 3$ | Z, N, N |
| 11 | `lsn.speed.difference-squares` Difference of squares | Use $(a - b)(a + b) = a^2 - b^2$ (0.2 lesson 10) with squares to 30 to multiply numbers spaced evenly around a round number | $37 \times 43$ in under 5 seconds | `strategy-trainer` (area-model rearrangement), `speed-drill` | Trap: $40^2 - 3$ (it is $40^2 - 3^2 = 1{,}591$). Edge: it needs an even difference between the factors; $46 \times 54 = 2{,}500 - 16$ | Z, N, N |
| 12 | `lsn.speed.squaring` Squaring quickly | Square numbers ending in 5 ($n5^2$ is $n(n + 1)$ followed by 25), numbers near 50 and 100, and any two-digit number by $(a + b)^2 = a^2 + 2ab + b^2$ | $45^2$, then $103^2$ | `strategy-trainer`, `speed-drill` | Trap: $(a + b)^2 = a^2 + b^2$, the missing $2ab$ (0.2 lesson 10). Edge: $98^2 = 10{,}000 - 400 + 4 = 9{,}604$ | Z, N, N |

**Level A4: Fractions, decimals, percentages and estimates** (`lvl.speed.fractions`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 13 | `lsn.speed.fraction-anchors` Fraction and decimal anchors | Convert fractions with denominators 2 to 12, 16, 20 and 25 to decimals within 3 seconds from anchors: eighths, sixths, sevenths, ninths, elevenths and twelfths | $\frac{5}{8}$, $\frac{3}{7}$ and $\frac{7}{12}$ as decimals, fast | `speed-drill` (fractions deck), `strategy-trainer` | Trap: $\frac{1}{7} = 0.17$ (it is $0.142857\ldots$); $\frac{1}{6} = 0.16$. Edge: every seventh cycles through the digits 142857, starting at a different point | Z, N, N |
| 14 | `lsn.speed.decimal-point` Placing the decimal point | Multiply and divide decimals mentally by working with whole numbers and powers of ten, then placing the point by estimate, within 4 seconds | $0.4 \times 0.06$, then $3.6 \div 0.09$ (0.024 and 40) | `strategy-trainer` (place-value slider), `speed-drill` (decimals deck), `number-line` (log scale) | Trap: counting decimal places for a quotient as for a product ($3.6 \div 0.09$ answered 0.004: three decimal places, as for $3.6 \times 0.09$). Edge: dividing by a number below 1 makes the answer bigger; scale both numbers by the same power of ten first ($3.6 \div 0.09 = 360 \div 9$) | Z, N, N |
| 15 | `lsn.speed.percentages` Percentages at speed | Compute $x\%$ of $y$, percentage changes and reverse percentages mentally, using $x\%$ of $y$ equals $y\%$ of $x$ | 16% of 25 | `speed-drill`, `strategy-trainer` | Trap: a 20% rise then a 20% fall taken to return to the start (it leaves 96%). Edge: 8% of 50 is 50% of 8, which is 4 | Z, N, N |
| 16 | `lsn.speed.estimation` Estimation and sanity checks | Give answers within a stated tolerance by rounding to one or two significant figures, and catch order-of-magnitude errors | $387 \times 0.049$: nearer 2, 20 or 200? | `speed-drill` (estimation deck), `fermi-estimator` | Trap: rounding both factors the same way so the errors add. Edge: round one up and the other down so the errors cancel | Z, N, C |

**Coverage check for 0.5.** Curriculum cover list: times tables to 12 (A1), two-digit addition and subtraction (A2), two-digit multiplication (A1 lesson 3, A3), fractions to decimals (A4 lesson 13). Added: the Zetamac format and division (A1), chains (A2 lesson 8, the 80-in-8 format's multi-step items), decimals, percentages and estimation (A4 lessons 14 to 16).

---

## 3. Homework blueprint per level

### 3.0 Rules for every set

- **Issue, due and marking** follow ASSESSMENT.md 2.5: issued when the level's last lesson is done, due 7 days later, no feedback before submission, code items run their visible examples freely and their hidden tests at submission, long-form items self-marked against the rubric with Bertie's suggested mark beside the learner's.
- **0.3 sets.** Levels of 4 or 5 lessons get **8 items: 3 at difficulty 3, 3 at difficulty 4, 2 at difficulty 5**. Levels of 6 lessons get **10 items: 4 at difficulty 3, 4 at difficulty 4, 2 at difficulty 5**. Exactly one long-form item (a derivation, proof or written explanation with a 10-point rubric, usually difficulty 4) and exactly one code drill (difficulty 3 or 4) sit inside those counts. At least half the items are generator slots, so a redo is a fresh variant. At most two choice items per set. Expected time about 1 hour 45 minutes.
- **0.4 sets.** 6 items: 2 at difficulty 3, 3 at difficulty 4, 1 at difficulty 5, with one long-form written explanation and one drill. From set K2 on, the drill is a code drill with hidden tests (in K2 a transcribe-and-run drill, which tests typing accuracy on code text and needs no Python knowledge). Sets K1, B1 and B2 come before any Python, so their drill slot holds a task graded by its effect: a typing run in `typing-trainer`, or a file-system task whose final state is checked in `shell-sim` (open item 6). About 45 minutes.
- **0.5 sets.** 6 items: three timed sets (two at difficulty 3, one at 4), one long-form proof of a shortcut (difficulty 4), one small code drill (difficulty 4), and one timed challenge at difficulty 5. About 30 minutes.
- **Long-form marking.** Every rubric has 4 to 10 points totalling 10 marks, and each point names the model-answer lines that evidence it (CONTENT-FORMAT.md 3.4). 7 of 10 is the bar wherever an outcome cites a rubric.
- **Code drills** list their hidden-test cases here so CI can check that the reference solution passes and each known-wrong solution fails its named test (CONTENT-FORMAT.md 3.9). All 0.3, 0.4 and 0.5 drills use the standard library only and declare `needs: []`, so they run under Pyodide in the Artifact and in the web app alike (ARCHITECTURE.md decision 15); only the Precalc Lab project's part 3 declares `needs: [numpy, matplotlib]` (section 3.2). A device that cannot load Python hands the drill to the web app with its id and seed and takes the result back as a result code (ASSESSMENT.md 2.5, 14.3).

Below, each level gives its set id, item mix, long-form item, code drill, and two example problems in full: example A is the long-form item with its model answer and rubric, example B a difficulty-5 item with its worked answer.

### 3.1 0.3 Precalculus

**S1 Angles and polygons** (`set.shape.angles`). 8 items (3 d3, 3 d4, 2 d5). Long-form: the polygon angle sums. Code drill `drl.pre.polygon-angles` (d3): `interior_angle(n)` returns the interior angle of a regular $n$-gon in degrees as a `Fraction`; `sides_from_interior(angle)` returns $n$ or `None`. Hidden tests: $n = 3$ gives 60; $n = 360$ gives 179; an interior angle of $179$ gives 360; an exterior angle of $25°$ (interior $155°$) gives `None`; $n = 2$ raises `ValueError`.

- *Example A (long-form, d4).* Prove that the interior angles of a convex $n$-sided polygon add to $(n - 2) \times 180°$, and deduce that its exterior angles add to $360°$.
  *Model answer.* (1) From one vertex, draw diagonals to the $n - 3$ vertices that are not its neighbours. (2) These split the polygon into $n - 2$ triangles, because each diagonal adds one triangle to the first. (3) The polygon is convex, so every diagonal lies inside it and the triangles' angles together make up exactly the polygon's interior angles. (4) Each triangle's angles add to $180°$, so the interior sum is $(n - 2) \times 180°$. (5) At each vertex the interior and exterior angles lie on a straight line, so they add to $180°$; over $n$ vertices they add to $180n°$. (6) Exterior sum $= 180n - 180(n - 2) = 360°$.
  *Rubric (10).* 2: the $n - 2$ triangles, with the count justified (lines 1, 2). 1: convexity named as the reason the triangles fill the polygon exactly (line 3). 2: the triangle sum cited and multiplied (line 4). 2: interior plus exterior equals $180°$, with the reason "angles on a straight line" (line 5). 2: the subtraction to $360°$ (line 6). 1: a closing sentence stating what was proved.
- *Example B (d5).* Three regular polygons with $a \le b \le c$ sides meet at a point, filling the space around it with no gaps or overlaps. Show that $\frac{1}{a} + \frac{1}{b} + \frac{1}{c} = \frac{1}{2}$, and find every solution.
  *Answer.* A regular $n$-gon's interior angle is $180° - \frac{360°}{n}$. Three of them make $360°$: $540 - 360(\frac{1}{a} + \frac{1}{b} + \frac{1}{c}) = 360$, so $\frac{1}{a} + \frac{1}{b} + \frac{1}{c} = \frac{1}{2}$. Since $\frac{3}{a} \ge \frac{1}{2}$, $a \le 6$, and $a \ge 3$. Working through $a = 3, 4, 5, 6$ gives exactly ten triples: $(3, 7, 42)$, $(3, 8, 24)$, $(3, 9, 18)$, $(3, 10, 15)$, $(3, 12, 12)$, $(4, 5, 20)$, $(4, 6, 12)$, $(4, 8, 8)$, $(5, 5, 10)$, $(6, 6, 6)$. Decision point: guessing stops at the familiar tilings; the bound $a \le 6$ is what makes the list provably complete.

**S2 Area and volume** (`set.shape.measure`). 8 items (3 d3, 3 d4, 2 d5). Long-form: the frustum fraction. Code drill `drl.pre.lattice-pi` (d3): `lattice_points(r)` counts integer points $(x, y)$ with $x^2 + y^2 \le r^2$; `pi_estimate(r)` returns `lattice_points(r) / r**2`. Hidden tests: $r = 1$ gives 5; $r = 10$ gives 317; $r = 100$ gives 31,417, an estimate within 0.01% of $\pi$; $r = 0$ raises `ValueError`.

- *Example A (long-form, d4).* A cone is cut by a plane parallel to its base, a fraction $t$ of the way down from the apex ($0 < t < 1$). Show that the bottom piece (the frustum) holds a fraction $1 - t^3$ of the cone's volume, and state the fraction when the cut is halfway down.
  *Model answer.* (1) The small cone cut off at the top has the same apex angle as the whole cone, so it is similar to it. (2) Its height is $t$ times the whole height, so the length scale factor is $t$. (3) Volumes scale by the cube of the length scale factor, so the small cone has $t^3$ of the volume. (4) The frustum is the whole cone minus the small cone: $1 - t^3$. (5) Halfway down, $t = \frac{1}{2}$, so the frustum holds $1 - \frac{1}{8} = \frac{7}{8}$. (6) Check: as $t \to 1$ the frustum vanishes and as $t \to 0$ it becomes the whole cone.
  *Rubric (10).* 2: similarity stated with a reason (line 1). 2: length scale factor $t$ (line 2). 3: volume factor $t^3$, with "cube of the length factor" named (line 3). 1: subtraction (line 4). 1: $\frac{7}{8}$ (line 5). 1: a limiting-case check (line 6).
- *Example B (d5).* Water stands 5 cm deep in a cylinder of radius 4 cm. A solid ball of radius 3 cm is dropped in. Find the new depth, and check the assumption your method makes.
  *Answer.* Assume the ball is fully under water. Its volume is $\frac{4}{3}\pi \times 27 = 36\pi$; spread over the cross-section $16\pi$ it raises the water by $\frac{36\pi}{16\pi} = 2.25$ cm, to 7.25 cm. Check: the ball's top is 6 cm above the bottom and $7.25 > 6$, so it is submerged and the assumption holds. Decision point: with only 1 cm of water the same method gives $1 + 2.25 = 3.25 < 6$, which contradicts the assumption; the honest answer there needs the volume of a spherical cap, which waits for 1.3.

**S3 Pythagoras, congruence and similarity** (`set.shape.triangles`). 8 items (3 d3, 3 d4, 2 d5). Long-form: a proof of Pythagoras' theorem. Code drill `drl.pre.triples` (d3): `primitive_triples(limit)` returns every primitive triple $(a, b, c)$ with $a < b$, $c \le$ `limit`, sorted. Hidden tests: `limit = 5` gives `[(3, 4, 5)]`; `limit = 100` gives 16 triples, each with $\gcd(a, b) = 1$ and $a^2 + b^2 = c^2$; `limit = 4` gives `[]`.

- *Example A (long-form, d4).* Prove Pythagoras' theorem by placing four copies of a right triangle with legs $a$, $b$ and hypotenuse $c$ inside a square of side $a + b$.
  *Model answer.* (1) Place the four triangles in the corners of the $(a + b)$ square, each with its legs along two sides. (2) The inner quadrilateral has four sides of length $c$. (3) At each of its corners the two acute angles of the triangles add to $90°$ (the triangle's angles add to $180°$ and one is $90°$), and with the inner corner they make a straight line, so each inner corner is $90°$: the inner shape is a square of area $c^2$. (4) Big square area $= (a + b)^2 = a^2 + 2ab + b^2$. (5) It also equals $c^2 + 4 \times \frac{1}{2}ab = c^2 + 2ab$. (6) Equating: $a^2 + b^2 = c^2$.
  *Rubric (10).* 1: the arrangement (line 1). 1: inner sides equal $c$ (line 2). 3: the inner corners proved to be right angles, with reasons (line 3); the most-missed point. 2: the two area expressions (lines 4, 5). 2: the equation and simplification (line 6). 1: no step assumed from the diagram's appearance.
- *Example B (d5).* An ant walks on the outside of a closed $3 \times 4 \times 12$ cm box from one corner to the diagonally opposite corner. What is the shortest route?
  *Answer.* Unfold two adjacent faces into a flat rectangle; the route is a straight line across it. The three unfoldings give $\sqrt{(3 + 4)^2 + 12^2} = \sqrt{193} \approx 13.89$, $\sqrt{(3 + 12)^2 + 4^2} = \sqrt{241} \approx 15.52$ and $\sqrt{(4 + 12)^2 + 3^2} = \sqrt{265} \approx 16.28$. Shortest: $\sqrt{193} \approx 13.9$ cm, when the two shorter edges are added. Decision point: the space diagonal ($13$ cm) is shorter but goes through the box, and the naive "along the edges" route ($19$ cm) is far longer.

**S4 Transformations and constructions** (`set.shape.transform`). 8 items (3 d3, 3 d4, 2 d5). Long-form: two reflections make a translation. Code drill `drl.pre.transform-points` (d4): `rotate90cw(p, centre)` and `enlarge(p, centre, k)` with `k` a `Fraction`. Hidden tests: rotating four times returns every point; the centre is invariant; `enlarge` with $k = -1$ equals two quarter-turns; $k = 0$ sends every point to the centre.

- *Example A (long-form, d4).* Prove that reflecting in the line $x = a$ and then in the line $x = b$ is a translation, and find its vector.
  *Model answer.* (1) Reflection in $x = a$ keeps $y$ and sends $x$ to $2a - x$, because the mirror is halfway between a point and its image. (2) Reflection in $x = b$ sends $x$ to $2b - x$. (3) Doing the first and then the second: $x \mapsto 2b - (2a - x) = x + 2(b - a)$, and $y$ is unchanged. (4) Every point moves by the same vector $\binom{2(b - a)}{0}$, so the composition is a translation, perpendicular to the mirrors, by twice the distance between them, in the direction from the first mirror to the second. (5) Doing them in the other order gives $\binom{2(a - b)}{0}$: order matters.
  *Rubric (10).* 2: formula for one reflection with the reason (line 1). 1: second reflection (line 2). 3: composition computed in the right order (line 3). 2: conclusion that the move is a translation, with its vector described in words (line 4). 2: the reversed order (line 5).
- *Example B (d5).* A rotation of $90°$ clockwise about $(1, 2)$ is followed by a rotation of $90°$ clockwise about $(3, 0)$. Show that the result is a single rotation and find its centre and angle.
  *Answer.* The first rotation sends $(x, y)$ to $(y - 1, 3 - x)$; the second sends $(x, y)$ to $(y + 3, 3 - x)$. Composing: $(x, y) \mapsto (6 - x, 4 - y)$. That is a rotation of $180°$ about the fixed point, where $6 - x = x$ and $4 - y = y$: the centre is $(3, 2)$. Decision point: adding the angles ($90° + 90° = 180°$) is right, but averaging the centres ($(2, 1)$) is not; only the fixed-point equation finds the centre.

**S5 Circle theorems** (`set.shape.circle-theorems`). 8 items (3 d3, 3 d4, 2 d5). Long-form: the angle at the centre, both cases. Code drill `drl.pre.concyclic` (d4): `circumcentre(p, q, r)` returns the centre as a pair of `Fraction`s by intersecting two perpendicular bisectors; `concyclic(p, q, r, s)` returns a boolean. Hidden tests: $(1, 0), (0, 1), (-1, 0), (0, -1)$ concyclic; three collinear points raise `ValueError`; a rectangle's corners are concyclic; a non-square rhombus's are not.

- *Example A (long-form, d4).* Prove that the angle subtended by an arc at the centre is twice the angle it subtends at any point on the remaining part of the circle. Treat the case where the centre lies inside the angle at the circumference and the case where it lies outside.
  *Model answer.* Let the arc be AB, the centre O and the point P. (1) Draw the diameter through P, meeting the circle again at Q. (2) OA = OP (radii), so triangle OAP is isosceles and $\angle OAP = \angle OPA = x$. (3) The exterior angle of triangle OAP at O is $\angle AOQ = 2x$. (4) Likewise with OB = OP: $\angle OPB = y$ and $\angle BOQ = 2y$. (5) Centre inside: $\angle APB = x + y$ and $\angle AOB = 2x + 2y = 2\angle APB$. (6) Centre outside (A and B on the same side of PQ): $\angle APB = y - x$ and $\angle AOB = 2y - 2x$, so the result holds again.
  *Rubric (10).* 1: the construction (line 1). 2: isosceles triangle with the reason "radii" (line 2). 2: exterior angle of a triangle (line 3). 1: second triangle (line 4). 2: inside case (line 5). 2: outside case by subtraction (line 6).
- *Example B (d5).* TA and TB are tangents from T to a circle with centre O, and $\angle ATB = 50°$. C is a point on the major arc AB. Find $\angle ACB$, giving a reason for each step. Then find $\angle AC'B$ for a point C' on the minor arc.
  *Answer.* $\angle OAT = \angle OBT = 90°$ (radius meets tangent at right angles). The angles of quadrilateral OATB add to $360°$, so $\angle AOB = 360° - 90° - 90° - 50° = 130°$. The angle at the circumference is half the angle at the centre: $\angle ACB = 65°$. ACBC' is a cyclic quadrilateral, so $\angle AC'B = 180° - 65° = 115°$. Decision point: the minor-arc point is where learners copy $65°$; the reflex angle at the centre ($230°$) gives $115°$ directly and confirms it.

**S6 Right-angled trigonometry** (`set.shape.right-trig`). 8 items (3 d3, 3 d4, 2 d5). Long-form: the exact values. Code drill `drl.pre.clinometer` (d3): `height_from_two_sightings(d, alpha_deg, beta_deg)` returns $h = \frac{d\tan\alpha\tan\beta}{\tan\beta - \tan\alpha}$. Hidden tests: $(40, 30, 60)$ gives $20\sqrt{3} \approx 34.641$; $\alpha \ge \beta$ raises `ValueError`; the known-wrong solution that forgets `math.radians` fails the first test.

- *Example A (long-form, d4).* Derive the exact values of $\sin$, $\cos$ and $\tan$ of $30°$, $45°$ and $60°$ without a calculator.
  *Model answer.* (1) Halve a square of side 1 along a diagonal: a right triangle with legs 1, 1, angles $45°$, and hypotenuse $\sqrt{2}$ by Pythagoras. (2) So $\sin 45° = \cos 45° = \frac{1}{\sqrt{2}} = \frac{\sqrt{2}}{2}$ and $\tan 45° = 1$. (3) Halve an equilateral triangle of side 2 by an altitude: a right triangle with hypotenuse 2, short side 1 (half the base), angles $30°$ and $60°$. (4) The altitude is $\sqrt{2^2 - 1^2} = \sqrt{3}$. (5) Opposite $30°$ is the side 1: $\sin 30° = \frac{1}{2}$, $\cos 30° = \frac{\sqrt{3}}{2}$, $\tan 30° = \frac{1}{\sqrt{3}}$. (6) Opposite $60°$ is $\sqrt{3}$: $\sin 60° = \frac{\sqrt{3}}{2}$, $\cos 60° = \frac{1}{2}$, $\tan 60° = \sqrt{3}$.
  *Rubric (10).* 2: the half-square triangle and its hypotenuse (line 1). 1: the $45°$ values (line 2). 2: the half-equilateral triangle with the reason the short side is 1 (line 3). 1: the altitude (line 4). 2: the $30°$ values with sides correctly matched (line 5). 2: the $60°$ values (line 6).
- *Example B (d5).* A vertical mast stands at corner O of a horizontal rectangular field OABC with OA = 40 m and OC = 30 m. From B, the corner opposite O, the angle of elevation of the top of the mast is $30°$. (a) Find the mast's height exactly. (b) Find the angle of elevation of the top from M, the midpoint of CB.
  *Answer.* (a) OB $= \sqrt{40^2 + 30^2} = 50$ m, so $h = 50\tan 30° = \frac{50}{\sqrt{3}} = \frac{50\sqrt{3}}{3} \approx 28.87$ m. (b) Put O at the origin, A at $(40, 0)$, C at $(0, 30)$, so M $= (20, 30)$ and OM $= \sqrt{20^2 + 30^2} = 10\sqrt{13} \approx 36.06$ m. Then $\tan\theta = \frac{50/\sqrt{3}}{10\sqrt{13}} = \frac{5}{\sqrt{39}}$, so $\theta \approx 38.7°$. Decision point: the angle at M lives in the vertical triangle through M, O and the top of the mast, so the horizontal distance OM is needed first; using MB or MC builds the wrong triangle.

**S7 Any triangle** (`set.shape.any-triangle`). 8 items (3 d3, 3 d4, 2 d5). Long-form: the cosine rule. Code drill `drl.pre.ssa-triangles` (d5): `solve_ssa(a, b, A_deg)`, where side $a$ is opposite angle $A$, returns a list of 0, 1 or 2 triangles, each as `(c, B_deg, C_deg)`. Hidden tests: no triangle when $a < b\sin A$; one when $a = b\sin A$ (a right angle at B); two when $b\sin A < a < b$ with $A$ acute; one when $a \ge b$; obtuse $A$ with $a \le b$ gives none.

- *Example A (long-form, d4).* Derive the cosine rule $c^2 = a^2 + b^2 - 2ab\cos C$ for a triangle with an acute angle C and for one with an obtuse angle C.
  *Model answer.* Let C be at the origin, CA along the positive $x$-axis with A $= (b, 0)$, and B $= (a\cos C, a\sin C)$. (1) This places B correctly for any angle C from $0°$ to $180°$, because $(\cos C, \sin C)$ is the unit-circle point at angle C. (2) $c^2 = AB^2 = (a\cos C - b)^2 + (a\sin C)^2$ by the distance formula. (3) Expand: $a^2\cos^2 C - 2ab\cos C + b^2 + a^2\sin^2 C$. (4) Use $\sin^2 C + \cos^2 C = 1$: $c^2 = a^2 + b^2 - 2ab\cos C$. (5) For obtuse C, $\cos C < 0$ and the same algebra holds, so no separate case is needed; the classical altitude proof does need one, because the foot of the altitude falls outside the triangle. (6) At $C = 90°$ the rule is Pythagoras.
  *Rubric (10).* 2: coordinates set up with a reason (line 1). 2: distance formula (line 2). 2: expansion (line 3). 2: identity used (line 4). 1: obtuse case addressed explicitly (line 5). 1: the $90°$ check (line 6). An altitude proof that covers both cases earns full marks against the same points.
- *Example B (d5).* In triangle ABC, AB = 10, AC = 7 and $\angle ABC = 40°$. Find every possible length of BC.
  *Answer.* Let BC $= x$. The cosine rule at B: $7^2 = 10^2 + x^2 - 20x\cos 40°$, so $x^2 - (20\cos 40°)x + 51 = 0$, that is $x^2 - 15.321x + 51 = 0$. Then $x = \frac{15.321 \pm \sqrt{234.73 - 204}}{2}$, so $x \approx 10.43$ or $x \approx 4.89$. Both are positive, so two triangles exist; equivalently $\sin C = \frac{10\sin 40°}{7} \approx 0.918$ gives $C \approx 66.7°$ or $113.3°$. Decision point: the sine-rule route with only the calculator's $66.7°$ loses the second triangle; the quadratic shows both at once.

**S8 Vectors** (`set.shape.vectors`). 10 items (4 d3, 4 d4, 2 d5). Long-form: the midpoint parallelogram. Code drill `drl.pre.cosine-similarity` (d3): `dot`, `norm` and `cosine_similarity(u, v)` for equal-length lists; `most_similar(target, candidates)` returns the index of the best match. Hidden tests: parallel vectors give 1; perpendicular give 0; opposite give $-1$; a scaled copy of the target wins even when another candidate is nearer in distance; a zero vector raises `ValueError`; unequal lengths raise `ValueError`.

- *Example A (long-form, d4).* ABCD is any quadrilateral and P, Q, R, S are the midpoints of AB, BC, CD and DA. Prove with vectors that PQRS is a parallelogram.
  *Model answer.* Let A, B, C, D have position vectors $\mathbf{a}$, $\mathbf{b}$, $\mathbf{c}$, $\mathbf{d}$. (1) $\mathbf{p} = \frac{1}{2}(\mathbf{a} + \mathbf{b})$, $\mathbf{q} = \frac{1}{2}(\mathbf{b} + \mathbf{c})$, $\mathbf{r} = \frac{1}{2}(\mathbf{c} + \mathbf{d})$, $\mathbf{s} = \frac{1}{2}(\mathbf{d} + \mathbf{a})$. (2) $\vec{PQ} = \mathbf{q} - \mathbf{p} = \frac{1}{2}(\mathbf{c} - \mathbf{a})$. (3) $\vec{SR} = \mathbf{r} - \mathbf{s} = \frac{1}{2}(\mathbf{c} - \mathbf{a})$. (4) $\vec{PQ} = \vec{SR}$, so PQ and SR are parallel and equal in length. (5) A quadrilateral with one pair of opposite sides parallel and equal is a parallelogram. (6) Both are half of the diagonal $\vec{AC}$, which explains why: the shape inherits its sides from the diagonals.
  *Rubric (10).* 2: midpoint vectors (line 1). 2: $\vec{PQ}$ as a difference in the right order (line 2). 2: $\vec{SR}$ (line 3). 2: equal vectors interpreted as parallel and equal (line 4). 1: the parallelogram criterion named (line 5). 1: the link to the diagonal (line 6).
- *Example B (d5).* In triangle OAB, $\vec{OA} = \mathbf{a}$ and $\vec{OB} = \mathbf{b}$. P lies on OA with OP : PA $= 2 : 1$, and Q is the midpoint of AB. The lines OQ and BP meet at X. Find $\vec{OX}$ and the ratio BX : XP.
  *Answer.* $\vec{OQ} = \frac{1}{2}(\mathbf{a} + \mathbf{b})$, so $\vec{OX} = \lambda \cdot \frac{1}{2}(\mathbf{a} + \mathbf{b})$. On BP, $\vec{OX} = \mathbf{b} + \mu(\frac{2}{3}\mathbf{a} - \mathbf{b}) = \frac{2\mu}{3}\mathbf{a} + (1 - \mu)\mathbf{b}$. Since $\mathbf{a}$ and $\mathbf{b}$ are not parallel, compare coefficients: $\frac{\lambda}{2} = \frac{2\mu}{3}$ and $\frac{\lambda}{2} = 1 - \mu$, so $\mu = \frac{3}{5}$ and $\lambda = \frac{4}{5}$. Hence $\vec{OX} = \frac{2}{5}(\mathbf{a} + \mathbf{b})$ and BX : XP $= \mu : (1 - \mu) = 3 : 2$. Decision point: the step "compare coefficients" is valid only because $\mathbf{a}$ and $\mathbf{b}$ are not parallel; saying so is part of the answer.

**G1 Sequences and recurrences** (`set.growth.sequences`). 8 items (3 d3, 3 d4, 2 d5). Long-form: the closed form of the Fibonacci numbers. Code drill `drl.pre.stairs` (d4): `climbs(n)` returns the number of ways to climb $n$ stairs in steps of one or two, by a loop over exact integers; `binet_round(n)` returns the same count from $\frac{\varphi^{n+1}}{\sqrt{5}}$ rounded, in floating point; `first_disagreement(limit)` returns the first $n$ where they differ. Hidden tests: `climbs(0) == 1`, `climbs(1) == 1`, `climbs(10) == 89`; `climbs(90) == 4660046610375530309` exactly; `first_disagreement(200) == 70` (the float formula first fails at $F_{71} \approx 3.1 \times 10^{14}$: the relative error of about $10^{-16}$ in $\varphi$ grows roughly $n$-fold under the power, and there the absolute error passes $\frac{1}{2}$); the known-wrong solution that recurses without memoisation fails the 2-second per-test limit at $n = 35$, about 30 million calls.

- *Example A (long-form, d4).* The Fibonacci numbers satisfy $F_0 = 0$, $F_1 = 1$ and $F_{n+2} = F_{n+1} + F_n$. Show that $F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}$, where $\varphi = \frac{1 + \sqrt{5}}{2}$ and $\psi = \frac{1 - \sqrt{5}}{2}$, and deduce that $F_n$ is the whole number nearest $\frac{\varphi^n}{\sqrt{5}}$.
  *Model answer.* (1) Try $u_n = r^n$ with $r \ne 0$: the recurrence becomes $r^{n+2} = r^{n+1} + r^n$, so $r^2 = r + 1$, whose roots are $\varphi$ and $\psi$. (2) If two sequences satisfy the recurrence, so does any combination $A\varphi^n + B\psi^n$, because the recurrence is linear: each side of it is a sum of the two sequences' sides. (3) Fit the starting values: $n = 0$ gives $A + B = 0$; $n = 1$ gives $A\varphi + B\psi = 1$. (4) So $A(\varphi - \psi) = 1$, and $\varphi - \psi = \sqrt{5}$, giving $A = \frac{1}{\sqrt{5}}$ and $B = -\frac{1}{\sqrt{5}}$. (5) A recurrence that uses the two previous terms, with two starting values, fixes every term (by strong induction), so this formula is $F_n$ for every $n$. (6) $\lvert \psi \rvert \approx 0.618 < 1$, so $\left\lvert \frac{\psi^n}{\sqrt{5}} \right\rvert < \frac{1}{\sqrt{5}} < \frac{1}{2}$ for every $n \ge 0$, and $F_n$, a whole number, lies within $\frac{1}{2}$ of $\frac{\varphi^n}{\sqrt{5}}$.
  *Rubric (10).* 2: the trial $r^n$ and the equation $r^2 = r + 1$ (line 1). 2: linearity named as the reason combinations work (line 2). 2: the two equations from the starting values (line 3). 1: $A$ and $B$ (line 4). 2: why the formula is the sequence, not merely a solution (line 5). 1: the nearest-integer deduction with the bound (line 6).
- *Example B (d5).* A savings account starts at £0. At the start of each month £100 is paid in, and at the end of the month 0.5% interest is added. Write a recurrence for the balance $u_n$ after $n$ months, find its fixed point, and use it to find a closed form and the balance after 10 years.
  *Answer.* $u_{n+1} = 1.005(u_n + 100)$, $u_0 = 0$. The fixed point solves $L = 1.005L + 100.5$, so $L = -20{,}100$. Then $u_{n+1} - L = 1.005(u_n - L)$, so $u_n - L = 1.005^n(u_0 - L)$ and $u_n = 20{,}100(1.005^n - 1)$. After 120 months: $20{,}100 \times (1.005^{120} - 1) \approx$ £16,469.87. Decision point: the fixed point is negative and repels, so it is no limit at all; it is still the key to the closed form, because shifting by it turns the recurrence into a geometric sequence.

**G2 Exponential functions** (`set.growth.exponentials`). 8 items (3 d3, 3 d4, 2 d5). Long-form: why $(1 + \frac{1}{n})^n$ settles. Code drill `drl.pre.compounding` (d3): `balance(P, r, n, t)`, `effective_rate(r, n)` and `continuous_balance(P, r, t)`. Hidden tests: `effective_rate(0.12, 12)` $\approx 0.126825$; `effective_rate(0.12, 1) = 0.12`; balances increase with $n$ and stay below the continuous balance; $n = 0$ raises `ValueError`.

- *Example A (long-form, d4).* A bank pays 100% interest a year, compounded $n$ times. Explain, with evidence, why the year-end value of £1, $(1 + \frac{1}{n})^n$, neither grows without bound nor tends to 1 as $n$ grows.
  *Model answer.* (1) Table: $n = 1$: 2; $n = 2$: 2.25; $n = 12$: 2.613; $n = 365$: 2.7146; $n = 10^6$: 2.71828. (2) It increases: compounding more often pays interest on interest sooner and never takes any away. (3) The increases shrink fast (0.25, then about 0.36 over the next ten steps, then about 0.1 over the next 353). (4) "The exponent grows, so it explodes" fails: the base $1 + \frac{1}{n}$ falls towards 1 at the same time. (5) "The base tends to 1, so the value tends to 1" fails: the exponent grows at the same time. (6) The two pulls balance at a limit, $e \approx 2.71828$; a proof that the values stay below 3 comes in C3 (binomial expansion), set there as a difficulty-5 item.
  *Rubric (10).* 2: a table with at least four values including a large $n$ (line 1). 2: the increasing argument in words (line 2). 1: shrinking increments (line 3). 2: the "explodes" argument named and rebutted (line 4). 2: the "tends to 1" argument named and rebutted (line 5). 1: the conclusion with the value of $e$ (line 6).
- *Example B (d5).* Account A pays 6% a year nominal, compounded monthly. Account B pays 5.9% a year compounded continuously. Which has the higher effective annual rate, and by how many basis points?
  *Answer.* A: $1.005^{12} - 1 \approx 6.168\%$. B: $e^{0.059} - 1 \approx 6.078\%$. A is higher by about 9.0 basis points. Decision point: comparing the headline rates (6% against 5.9%) or treating continuous compounding as automatically best both mislead; only effective rates compare.

**G3 Logarithms** (`set.growth.logarithms`). 10 items (4 d3, 4 d4, 2 d5). Long-form: deriving the log laws. Code drill `drl.pre.int-log` (d3): `int_log(x, b)` returns the largest whole $k$ with $b^k \le x$ by repeated multiplication, for whole $x \ge 1$, $b \ge 2$. Hidden tests: `int_log(1000, 10) == 3` (the known-wrong solution `int(math.log(1000, 10))` gives 2, because `math.log(1000, 10)` is `2.9999999999999996`); `int_log(1, 7) == 0`; `int_log(1023, 2) == 9`; `int_log(1024, 2) == 10`; $x = 0$ raises `ValueError`.

- *Example A (long-form, d4).* Derive the laws $\log_b(xy) = \log_b x + \log_b y$, $\log_b(\frac{x}{y}) = \log_b x - \log_b y$ and $\log_b(x^k) = k\log_b x$ from the index laws, for $x, y > 0$.
  *Model answer.* (1) Let $m = \log_b x$ and $n = \log_b y$, so $b^m = x$ and $b^n = y$ by definition. (2) $xy = b^m b^n = b^{m+n}$ by the index law for products. (3) So $\log_b(xy) = m + n$. (4) $\frac{x}{y} = \frac{b^m}{b^n} = b^{m-n}$, so $\log_b\frac{x}{y} = m - n$. (5) $x^k = (b^m)^k = b^{mk}$, so $\log_b(x^k) = km$. (6) The conditions $x, y > 0$ are needed because only positive numbers have logarithms.
  *Rubric (10).* 2: definitions written as exponentials (line 1). 2: product law (lines 2, 3). 2: quotient law (line 4). 2: power law (line 5). 1: index laws named at each step. 1: the domain condition (line 6).
- *Example B (d5).* Solve exactly: (a) $2^{x+1} = 3^{x-1}$; (b) $4^x - 3 \cdot 2^{x+1} + 8 = 0$.
  *Answer.* (a) Take logs: $(x + 1)\ln 2 = (x - 1)\ln 3$, so $x(\ln 3 - \ln 2) = \ln 2 + \ln 3$ and $x = \frac{\ln 6}{\ln 1.5} \approx 4.419$. (b) Let $y = 2^x$, so $4^x = y^2$ and $3 \cdot 2^{x+1} = 6y$: $y^2 - 6y + 8 = 0$, $y = 2$ or $4$, so $x = 1$ or $x = 2$. Decision point: in (b) taking logs at once is impossible because of the sum; spotting the hidden quadratic is the step.

**G4 Modelling with exponentials and logarithms** (`set.growth.modelling`). 8 items (3 d3, 3 d4, 2 d5). Long-form: averages of returns. Code drill `drl.pre.loglinear-fit` (d4): `fit_exponential(xs, ys)` returns $(a, b)$ for $y = ab^x$ by fitting a line to $(x, \ln y)$ with the provided `fit_line` helper. Hidden tests: exact data from $3 \times 1.5^x$ recovers $a = 3$, $b = 1.5$ to $10^{-9}$; noisy data recovers $b$ to $10^{-2}$; a zero or negative $y$ raises `ValueError`.

- *Example A (long-form, d4).* A fund returns $+25\%$, $-20\%$, $+25\%$, $-20\%$ in four years. A colleague reports "an average return of 2.5% a year". Explain in writing what is wrong, compute the right measures, and say why log returns avoid the problem.
  *Model answer.* (1) The arithmetic mean of the simple returns is $\frac{0.25 - 0.2 + 0.25 - 0.2}{4} = 2.5\%$. (2) The money compounds: $1.25 \times 0.8 \times 1.25 \times 0.8 = 1.00$, so the fund ended where it started. (3) The annual growth rate that gives the same end value is the geometric mean: $1.00^{1/4} - 1 = 0\%$. (4) The arithmetic mean overstates growth whenever returns vary, because a fall of $r$ hurts more than a rise of $r$ helps. (5) Log returns: $\ln 1.25 + \ln 0.8 + \ln 1.25 + \ln 0.8 = 0$; they add across years, so their average is the true growth rate in log terms. (6) Report the geometric mean or the mean log return for growth; the arithmetic mean answers a different question (the expected one-year return).
  *Rubric (10).* 1: arithmetic mean (line 1). 2: compounding to the end value (line 2). 2: geometric mean (line 3). 2: the reason in words (line 4). 2: log returns computed and their additivity named (line 5). 1: the recommendation (line 6).
- *Example B (d5).* Prove that a price which rises by a fraction $r$ and then falls by $r$ (or the reverse) always ends lower, for $0 < r < 1$. Find $r$ if the pair of moves loses 4%.
  *Answer.* $(1 + r)(1 - r) = 1 - r^2 < 1$ for every $r \ne 0$, in either order because multiplication commutes. $1 - r^2 = 0.96$ gives $r = 0.2$: a 20% rise and a 20% fall lose 4%. Decision point: the loss is $r^2$, so small moves lose almost nothing and large moves lose a lot; this is the seed of "volatility drag" in 1.7.

**G5 Series** (`set.growth.series`). 10 items (4 d3, 4 d4, 2 d5). Long-form: the geometric series and its sum to infinity. Code drill `drl.pre.annuity` (d4): `payment(L, r, n)` and `amortisation(L, r, n)` returning rows of (month, interest, principal, balance). Hidden tests: the final balance is within $10^{-6}$ of 0; $r = 0$ gives $\frac{L}{n}$; `payment(200000, 0.004, 300)` $\approx 1145.99$; interest falls and principal rises month by month.

- *Example A (long-form, d4).* Derive the sum of the first $n$ terms of a geometric series with first term $a$ and ratio $r \ne 1$, state the sum when $r = 1$, and find the condition under which the sum to infinity exists, with its value.
  *Model answer.* (1) $S_n = a + ar + \dots + ar^{n-1}$. (2) $rS_n = ar + ar^2 + \dots + ar^n$. (3) Subtracting, every middle term cancels: $S_n - rS_n = a - ar^n$. (4) For $r \ne 1$, divide by $1 - r$: $S_n = \frac{a(1 - r^n)}{1 - r}$. (5) For $r = 1$ every term is $a$, so $S_n = na$; the formula would divide by zero. (6) As $n \to \infty$, $r^n \to 0$ exactly when $\lvert r \rvert < 1$, giving $S_\infty = \frac{a}{1 - r}$; for $\lvert r \rvert \ge 1$ (with $a \ne 0$) the terms do not shrink to 0 and there is no finite sum.
  *Rubric (10).* 1: the series written (line 1). 2: the shifted copy (line 2). 2: cancellation (line 3). 1: division with the condition $r \ne 1$ (line 4). 1: the $r = 1$ case (line 5). 3: the convergence condition with a reason, and the value (line 6).
- *Example B (d5).* A £200,000 mortgage is repaid in equal monthly payments over 25 years at 0.4% interest a month. Find the payment and the total interest paid.
  *Answer.* The loan equals the present value of the 300 payments: $200{,}000 = P\sum_{k=1}^{300} 1.004^{-k} = P \cdot \frac{1 - 1.004^{-300}}{0.004}$. So $P = \frac{200{,}000 \times 0.004}{1 - 1.004^{-300}} \approx$ £1,145.99. Total paid $\approx 300 \times 1{,}145.99 =$ £343,797; total interest $\approx$ £143,797 (£143,798.18 with the unrounded payment). Decision point: $\frac{200{,}000}{300} \times 1.004$ or "simple interest on the whole loan for 25 years" both ignore that the balance falls as it is repaid.

**T1 Radians and the unit circle** (`set.waves.unit-circle`). 8 items (3 d3, 3 d4, 2 d5). Long-form: symmetries of the circle. Code drill `drl.pre.related-angle` (d3): `related(angle_deg)` returns `(quadrant, reference_angle, sin_sign, cos_sign)`. Hidden tests: $210°$ gives quadrant 3, reference $30°$, signs $(-, -)$; $-60°$ behaves as $300°$; $750°$ behaves as $30°$; axis angles ($90°$, $180°$) return quadrant `None` with signs that include 0.

- *Example A (long-form, d4).* Using the unit circle, explain why $\sin(\pi - \theta) = \sin\theta$, $\cos(\pi - \theta) = -\cos\theta$, $\sin(-\theta) = -\sin\theta$ and $\cos(-\theta) = \cos\theta$ for every $\theta$.
  *Model answer.* (1) The point at angle $\theta$ is $(\cos\theta, \sin\theta)$ by definition. (2) The point at $\pi - \theta$ is the reflection of that point in the $y$-axis, because turning $\pi$ and then back $\theta$ mirrors the turn of $\theta$ from the other side. (3) Reflecting in the $y$-axis keeps $y$ and negates $x$, so $\sin(\pi - \theta) = \sin\theta$ and $\cos(\pi - \theta) = -\cos\theta$. (4) The point at $-\theta$ is the reflection in the $x$-axis (the same turn clockwise). (5) That keeps $x$ and negates $y$: $\cos(-\theta) = \cos\theta$, $\sin(-\theta) = -\sin\theta$. (6) None of this depends on $\theta$ being acute, which is the point of defining the functions on the circle.
  *Rubric (10).* 1: the definition (line 1). 2: the $y$-axis reflection identified with a reason (line 2). 2: the two results (line 3). 2: the $x$-axis reflection (line 4). 2: the two results (line 5). 1: generality (line 6).
- *Example B (d5).* A chord AB of a circle of radius 6 cm subtends $\frac{2\pi}{3}$ at the centre. Find exactly the area and the perimeter of the minor segment.
  *Answer.* Sector area $\frac{1}{2} \times 36 \times \frac{2\pi}{3} = 12\pi$. Triangle area $\frac{1}{2} \times 36 \times \sin\frac{2\pi}{3} = 9\sqrt{3}$. Segment area $12\pi - 9\sqrt{3} \approx 22.11$ cm². Arc $6 \times \frac{2\pi}{3} = 4\pi$; chord $2 \times 6\sin\frac{\pi}{3} = 6\sqrt{3}$; perimeter $4\pi + 6\sqrt{3} \approx 22.96$ cm. Decision point: the chord needs the half-angle in a right triangle (or the cosine rule); the arc formula alone gives only the curved part.

**T2 Waves** (`set.waves.graphs`). 8 items (3 d3, 3 d4, 2 d5). Long-form: reading the phase shift. Code drill `drl.pre.sinusoid` (d3): `fit_sinusoid(max_val, min_val, period, peak_time)` returns $(A, B, C, D)$ for $y = A\sin(B(t - C)) + D$. Hidden tests: the fitted curve passes through the peak at `peak_time` and the trough half a period later; `min_val > max_val` raises `ValueError`; the period is $\frac{2\pi}{B}$ to $10^{-12}$.

- *Example A (long-form, d4).* Explain the difference between $y = \sin(2x - \frac{\pi}{3})$ and $y = \sin 2x - \frac{\pi}{3}$, and find the horizontal shift of the first from $y = \sin 2x$.
  *Model answer.* (1) In $\sin 2x - \frac{\pi}{3}$ the $\frac{\pi}{3}$ is subtracted after the sine: the wave $\sin 2x$ moves down by $\frac{\pi}{3}$, a change of midline. (2) In $\sin(2x - \frac{\pi}{3})$ it is subtracted from the input. (3) Factor the input: $2x - \frac{\pi}{3} = 2(x - \frac{\pi}{6})$. (4) Replacing $x$ by $x - \frac{\pi}{6}$ moves a graph right by $\frac{\pi}{6}$ (0.2's horizontal-shift rule). (5) So the shift is $\frac{\pi}{6}$, not $\frac{\pi}{3}$: the stretch by $\frac{1}{2}$ also squeezes the shift. (6) Check: the first peak of $\sin(2x - \frac{\pi}{3})$ is where $2x - \frac{\pi}{3} = \frac{\pi}{2}$, at $x = \frac{5\pi}{12}$, which is $\frac{\pi}{6}$ right of $\sin 2x$'s first peak at $\frac{\pi}{4}$.
  *Rubric (10).* 2: the outside subtraction as a vertical move (line 1). 1: the inside subtraction located (line 2). 2: factoring (line 3). 2: direction of the shift with a reason (line 4). 2: the value $\frac{\pi}{6}$ with the explanation (line 5). 1: a numerical check (line 6).
- *Example B (d5).* The tide height in metres $t$ hours after midnight is $h(t) = 3.4 + 2.2\sin(\frac{\pi(t - 2)}{6.2})$. A boat needs at least 4.5 m. Between which times from midnight to noon can it pass?
  *Answer.* $h \ge 4.5$ means $\sin(\frac{\pi(t - 2)}{6.2}) \ge 0.5$, so $\frac{\pi(t - 2)}{6.2} \in [\frac{\pi}{6}, \frac{5\pi}{6}]$ (plus whole turns). That gives $t - 2 \in [1.033, 5.167]$, so $t \in [3.033, 7.167]$: about 03:02 to 07:10. The next window opens at about $t = 15.4$ and the previous one closed before midnight, so there is one window. Decision point: the period is 12.4 hours, not 12, so "the same window 12 hours later" is wrong by 24 minutes.

**T3 Identities and equations** (`set.waves.identities`). 10 items (4 d3, 4 d4, 2 d5). Long-form: an identity and where it fails. Code drill `drl.pre.trig-solve` (d4): `solve_sin(B, C, k, lo, hi)` returns every $x$ in $[lo, hi)$ with $\sin(Bx + C) = k$ from the principal value and the symmetry $\pi - \theta$. Hidden tests: $\sin x = 0.5$ on $[0, 4\pi)$ gives 4 solutions; $k = 1$ gives one per period; $\lvert k \rvert > 1$ gives `[]`; results agree with a dense sign-change scan to $10^{-9}$.

- *Example A (long-form, d4).* Prove that $\frac{1 - \cos\theta}{\sin\theta} = \frac{\sin\theta}{1 + \cos\theta}$ wherever both sides are defined, and state exactly where the identity fails.
  *Model answer.* (1) Work on the left side only. (2) Multiply top and bottom by $1 + \cos\theta$, which is non-zero wherever $\sin\theta \ne 0$ (if $\cos\theta = -1$ then $\sin\theta = 0$). (3) Numerator: $(1 - \cos\theta)(1 + \cos\theta) = 1 - \cos^2\theta = \sin^2\theta$. (4) So the left side is $\frac{\sin^2\theta}{\sin\theta(1 + \cos\theta)} = \frac{\sin\theta}{1 + \cos\theta}$, cancelling $\sin\theta \ne 0$. (5) The left side is undefined where $\sin\theta = 0$, that is at $\theta = k\pi$. (6) At $\theta = 2k\pi$ the right side equals 0 while the left is undefined; at $\theta = (2k + 1)\pi$ both are undefined. So the identity holds for all $\theta \ne k\pi$.
  *Rubric (10).* 1: one side transformed, never both (line 1). 2: the multiplier with its non-zero condition (line 2). 2: difference of squares and the Pythagorean identity (line 3). 2: the cancellation with its condition (line 4). 2: where the left side fails (line 5). 1: the behaviour of the right side there (line 6).
- *Example B (d5).* Solve $2\cos^2 x + 3\sin x = 3$ for $0 \le x < 2\pi$.
  *Answer.* Replace $\cos^2 x$ by $1 - \sin^2 x$: $2 - 2\sin^2 x + 3\sin x - 3 = 0$, so $2\sin^2 x - 3\sin x + 1 = 0$ and $(2\sin x - 1)(\sin x - 1) = 0$. Then $\sin x = \frac{1}{2}$ gives $x = \frac{\pi}{6}, \frac{5\pi}{6}$, and $\sin x = 1$ gives $x = \frac{\pi}{2}$. Three solutions. Decision point: leaving both $\cos$ and $\sin$ in the equation stalls; the identity reduces it to one unknown.

**T4 Compound angles** (`set.waves.compound`). 8 items (3 d3, 3 d4, 2 d5). Long-form: compound angles from the dot product. Code drill `drl.pre.r-form` (d3): `r_form(a, b)` returns $(R, \alpha)$ with $a\sin x + b\cos x = R\sin(x + \alpha)$, $\alpha$ in $(-\pi, \pi]$, using `math.atan2`. Hidden tests: $(3, 4)$ gives $(5, 0.9273)$; negative $a$ or $b$ in each quadrant reproduces the original function at 50 sample points to $10^{-12}$; $(0, 0)$ raises `ValueError`.

- *Example A (long-form, d4).* Derive $\cos(A - B) = \cos A\cos B + \sin A\sin B$ from the dot product of two unit vectors, then deduce $\cos(A + B)$ and $\sin(A + B)$.
  *Model answer.* (1) Let $\mathbf{u} = (\cos A, \sin A)$ and $\mathbf{v} = (\cos B, \sin B)$, unit vectors at angles $A$ and $B$. (2) The angle between them is $A - B$, so $\mathbf{u} \cdot \mathbf{v} = 1 \times 1 \times \cos(A - B)$ (lesson 37). (3) In components, $\mathbf{u} \cdot \mathbf{v} = \cos A\cos B + \sin A\sin B$. (4) Equating gives $\cos(A - B)$. (5) Replace $B$ by $-B$ and use $\cos(-B) = \cos B$, $\sin(-B) = -\sin B$: $\cos(A + B) = \cos A\cos B - \sin A\sin B$. (6) $\sin(A + B) = \cos(\frac{\pi}{2} - A - B) = \cos((\frac{\pi}{2} - A) - B)$, and expanding with line 4 and the co-function identities gives $\sin A\cos B + \cos A\sin B$.
  *Rubric (10).* 1: the two unit vectors (line 1). 2: the geometric dot product with the angle $A - B$ justified (line 2). 1: the component dot product (line 3). 1: equating (line 4). 2: the $+B$ version via odd and even (line 5). 3: $\sin(A + B)$ via the co-function step (line 6).
- *Example B (d5).* Find the maximum value of $3\sin x + 4\cos x + 2$ and the smallest positive $x$ where it occurs. Then solve $3\sin x + 4\cos x = 2.5$ for $0 \le x < 2\pi$.
  *Answer.* $3\sin x + 4\cos x = 5\sin(x + \alpha)$ with $\tan\alpha = \frac{4}{3}$, $\alpha \approx 0.9273$. Maximum $5 + 2 = 7$ where $x + \alpha = \frac{\pi}{2}$, so $x \approx 0.6435$. For the equation, $\sin(x + \alpha) = 0.5$, so $x + \alpha = \frac{\pi}{6}$ or $\frac{5\pi}{6}$ plus whole turns; within the range, $x \approx 1.691$ and $x \approx 5.880$ (the second from $\frac{\pi}{6} - \alpha + 2\pi$). Decision point: $\frac{\pi}{6} - \alpha$ is negative, and adding $2\pi$ to it is the step most answers miss.

**T5 Matrices** (`set.waves.matrices`). 10 items (4 d3, 4 d4, 2 d5). Long-form: columns, and the order of composition. Code drill `drl.pre.mat2` (d3): `mul(A, B)`, `det(A)` and `inv(A)` for $2 \times 2$ matrices of `Fraction`s. Hidden tests: `mul(A, inv(A))` is the identity; `det(mul(A, B)) == det(A) * det(B)`; a singular matrix raises `ValueError`; a pair with `mul(A, B) != mul(B, A)`.

- *Example A (long-form, d4).* Explain why the columns of a $2 \times 2$ matrix are the images of $(1, 0)$ and $(0, 1)$, and why the matrix $BA$ means "apply $A$ first, then $B$".
  *Model answer.* (1) $\begin{pmatrix} a & b \\ c & d \end{pmatrix}\begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} a \\ c \end{pmatrix}$, the first column; $(0, 1)$ gives the second. (2) Any point is $x(1, 0) + y(0, 1)$, and a matrix map respects sums and multiples, so the image is $x$ times the first column plus $y$ times the second: knowing the two images fixes the whole map. (3) Applying $A$ to $\mathbf{v}$ gives $A\mathbf{v}$; applying $B$ to that gives $B(A\mathbf{v})$. (4) Matrix multiplication is defined so that $B(A\mathbf{v}) = (BA)\mathbf{v}$. (5) So in $BA$ the matrix nearest the vector, $A$, acts first, as with functions: $f(g(x))$ applies $g$ first. (6) Example: rotate $90°$ anticlockwise, then reflect in the $x$-axis, has matrix $\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} = \begin{pmatrix} 0 & -1 \\ -1 & 0 \end{pmatrix}$, a reflection in $y = -x$; the other order gives the reflection in $y = x$.
  *Rubric (10).* 2: the column computation (line 1). 2: linearity explains why two images suffice (line 2). 2: composition written as nested application (lines 3, 4). 2: the order rule with the function analogy (line 5). 2: a worked example showing the orders differ (line 6).
- *Example B (d5).* For $A = \begin{pmatrix} 3 & 1 \\ -2 & 0 \end{pmatrix}$, find every line through the origin that $A$ maps onto itself, and describe what $A$ does along each.
  *Answer.* A line through the origin is mapped to itself when $A\mathbf{v} = \lambda\mathbf{v}$ for a direction $\mathbf{v}$. Then $(A - \lambda I)\mathbf{v} = \mathbf{0}$ with $\mathbf{v} \ne \mathbf{0}$, so $\det(A - \lambda I) = 0$: $(3 - \lambda)(-\lambda) + 2 = \lambda^2 - 3\lambda + 2 = 0$, so $\lambda = 1$ or $2$. For $\lambda = 2$: $\mathbf{v} = (1, -1)$, the line $y = -x$, stretched by 2. For $\lambda = 1$: $\mathbf{v} = (1, -2)$, the line $y = -2x$, every point fixed. Decision point: trying lines one by one never ends; asking when $A - \lambda I$ is singular turns the search into a quadratic. This is the first eigenvalue problem, met properly in 1.4.

**T6 Complex numbers in polar form** (`set.waves.complex`). 8 items (3 d3, 3 d4, 2 d5). Long-form: multiplication in polar form. Code drill `drl.pre.roots` (d3): `nth_roots(w, n)` with `cmath`. Hidden tests: `nth_roots(1, 3)` sums to 0 within $10^{-12}$; each root raised to $n$ returns `w` within $10^{-9}$; the roots have equal moduli $\lvert w \rvert^{1/n}$; $n = 0$ raises `ValueError`.

- *Example A (long-form, d4).* Prove that if $z_1 = r_1(\cos\theta_1 + i\sin\theta_1)$ and $z_2 = r_2(\cos\theta_2 + i\sin\theta_2)$ then $z_1z_2 = r_1r_2(\cos(\theta_1 + \theta_2) + i\sin(\theta_1 + \theta_2))$, and deduce the rule for $\frac{z_1}{z_2}$.
  *Model answer.* (1) Multiply out: $z_1z_2 = r_1r_2[(\cos\theta_1\cos\theta_2 - \sin\theta_1\sin\theta_2) + i(\sin\theta_1\cos\theta_2 + \cos\theta_1\sin\theta_2)]$, using $i^2 = -1$. (2) The real part is $\cos(\theta_1 + \theta_2)$ by the compound-angle formula. (3) The imaginary part is $\sin(\theta_1 + \theta_2)$. (4) So moduli multiply and arguments add. (5) For division, $w = \frac{z_1}{z_2}$ satisfies $wz_2 = z_1$, so $\lvert w \rvert r_2 = r_1$ and $\arg w + \theta_2 = \theta_1$: moduli divide and arguments subtract (with $r_2 \ne 0$). (6) The argument of the result may need $2\pi$ added or subtracted to return to the principal range.
  *Rubric (10).* 2: expansion with $i^2 = -1$ (line 1). 2: real part identified (line 2). 2: imaginary part identified (line 3). 1: the conclusion in words (line 4). 2: the division rule derived, not assumed (line 5). 1: the principal-range remark (line 6).
- *Example B (d5).* Solve $z^4 = -16$, plot the solutions, and show that they add to 0.
  *Answer.* $-16 = 16(\cos\pi + i\sin\pi)$. The roots have modulus $16^{1/4} = 2$ and arguments $\frac{\pi + 2k\pi}{4}$ for $k = 0, 1, 2, 3$: $\frac{\pi}{4}, \frac{3\pi}{4}, \frac{5\pi}{4}, \frac{7\pi}{4}$. So $z = \pm\sqrt{2} \pm \sqrt{2}i$ (all four sign choices), the corners of a square. They come in pairs $z$ and $-z$, so they add to 0. Decision point: "$z^2 = \pm 4i$" works but is slower; seeing the four roots as a square on a circle gives both the answer and the sum.

**C1 Counting arrangements** (`set.chance.arrangements`). 8 items (3 d3, 3 d4, 2 d5). Long-form: why the combination formula works. Code drill `drl.pre.count-brute` (d3): `arrangements_formula(word)` uses the multinomial formula; `arrangements_brute(word)` counts distinct permutations with `itertools` (words up to 8 letters). Hidden tests: BANANA gives 60 both ways; MISSISSIPPI gives 34,650 by formula; a word of distinct letters gives $n!$; the empty word gives 1.

- *Example A (long-form, d4).* Explain why the number of ways to choose $r$ objects from $n$, ignoring order, is $\binom{n}{r} = \frac{n!}{r!(n - r)!}$, and why $\binom{n}{r} = \binom{n}{n - r}$.
  *Model answer.* (1) The number of ordered selections of $r$ from $n$ is $n(n - 1)\cdots(n - r + 1) = \frac{n!}{(n - r)!}$ by the product rule. (2) Each unordered selection appears in that list $r!$ times, once for each order of its $r$ members. (3) So the ordered count is $r!$ times the unordered count, and dividing gives $\frac{n!}{r!(n - r)!}$. (4) The formula is symmetric in $r$ and $n - r$. (5) The reason: choosing the $r$ who are in is the same act as choosing the $n - r$ who are out, a one-to-one pairing of the two kinds of choice. (6) Check: $\binom{8}{3} = \frac{8 \times 7 \times 6}{6} = 56 = \binom{8}{5}$.
  *Rubric (10).* 2: ordered count (line 1). 3: every unordered selection counted $r!$ times, with the reason (line 2); the key idea. 1: division (line 3). 1: symmetry seen in the formula (line 4). 2: the pairing argument (line 5). 1: a check (line 6).
- *Example B (d5).* How many arrangements of the letters of BANANA have no two A's next to each other?
  *Answer.* Arrange the other letters B, N, N first: $\frac{3!}{2!} = 3$ ways. They leave 4 gaps (before, between and after), and the three A's must go in three different gaps: $\binom{4}{3} = 4$ ways. Total $3 \times 4 = 12$, out of 60 arrangements in all. Decision point: subtracting "some A's adjacent" from 60 needs inclusion-exclusion over overlapping pairs; placing the A's into gaps avoids it.

**C2 Counting principles** (`set.chance.principles`). 8 items (3 d3, 3 d4, 2 d5). Long-form: a pigeonhole proof. Code drill `drl.pre.derangements` (d4): `derangements_brute(n)` for $n \le 8$, `derangements_ie(n)` by inclusion-exclusion, and `derangements_rec(n)` by $D_n = (n - 1)(D_{n-1} + D_{n-2})$. Hidden tests: all three agree for $n = 0$ to 8; $D_5 = 44$; $D_8 = 14{,}833$; $\frac{D_{10}}{10!}$ is within $10^{-7}$ of $\frac{1}{e}$.

- *Example A (long-form, d4).* Prove that among any five points in a square of side 1, two are at most $\frac{\sqrt{2}}{2}$ apart.
  *Model answer.* (1) Divide the square into four squares of side $\frac{1}{2}$ by joining the midpoints of opposite sides. (2) Five points, four small squares: by the pigeonhole principle some small square holds at least two points (points on a shared edge may be assigned to either square). (3) Two points in one closed square of side $\frac{1}{2}$ are at most its diagonal apart. (4) That diagonal is $\sqrt{(\frac{1}{2})^2 + (\frac{1}{2})^2} = \frac{\sqrt{2}}{2}$. (5) So two of the points are within $\frac{\sqrt{2}}{2}$. (6) The bound is sharp: four corners and the centre have smallest distance exactly $\frac{\sqrt{2}}{2}$.
  *Rubric (10).* 2: the four boxes (line 1). 2: the principle applied with the count (line 2). 2: maximum distance in a box (line 3). 2: the diagonal computed (line 4). 1: conclusion (line 5). 1: sharpness example (line 6).
- *Example B (d5).* How many integers from 1 to 1,000 are divisible by none of 2, 3 and 5?
  *Answer.* Divisible by 2, 3, 5: 500, 333, 200. By 6, 10, 15: 166, 100, 66. By 30: 33. Divisible by at least one: $500 + 333 + 200 - 166 - 100 - 66 + 33 = 734$. By none: $1{,}000 - 734 = 266$. Decision point: $\lfloor \frac{1000}{3} \rfloor = 333$, not 333.3, and the floors must be taken before adding.

**C3 The binomial theorem** (`set.chance.binomial`). 8 items (3 d3, 3 d4, 2 d5); the second difficulty-5 item proves $(1 + \frac{1}{n})^n < 3$ from the binomial expansion, closing the promise of G2's long-form. Long-form: the row sums of Pascal's triangle. Code drill `drl.pre.pascal` (d3): `row(n)` built by adding, and `coefficient(p, q, n, k)` for $x^k$ in $(p + qx)^n$ with `Fraction`s. Hidden tests: `row(n)` matches `math.comb` for $n \le 30$; `coefficient(2, -3, 7, 3) == -15120`; $k > n$ gives 0.

- *Example A (long-form, d4).* Prove $\sum_{k=0}^{n}\binom{n}{k} = 2^n$ in two ways: from the binomial theorem, and by counting subsets.
  *Model answer.* (1) The binomial theorem: $(a + b)^n = \sum_k \binom{n}{k}a^{n-k}b^k$. (2) Put $a = b = 1$: $2^n = \sum_k \binom{n}{k}$. (3) Counting: a set of $n$ elements has $2^n$ subsets, because each element is in or out, two choices each, by the product rule. (4) Sorting the subsets by size, there are $\binom{n}{k}$ of size $k$. (5) Adding over sizes counts every subset once, so $\sum_k \binom{n}{k} = 2^n$. (6) The second proof explains the first: expanding $(1 + 1)^n$ is choosing, for each bracket, "in" or "out".
  *Rubric (10).* 1: theorem stated (line 1). 2: substitution (line 2). 2: $2^n$ subsets with the product rule (line 3). 2: subsets of size $k$ counted by $\binom{n}{k}$ (line 4). 2: the sum counts each subset once (line 5). 1: the link (line 6).
- *Example B (d5).* Find the term independent of $x$ in $(2x^2 - \frac{1}{x})^9$.
  *Answer.* The general term is $\binom{9}{k}(2x^2)^{9-k}(-\frac{1}{x})^k = \binom{9}{k}2^{9-k}(-1)^k x^{18 - 3k}$. Independent of $x$ when $18 - 3k = 0$, so $k = 6$: $\binom{9}{6} \times 2^3 \times (-1)^6 = 84 \times 8 = 672$. Decision point: the power of $x$ must be collected from both factors before solving; reading it from one factor gives $k = 3$ or $k = 9$.

**C4 Probability** (`set.chance.probability`). 10 items (4 d3, 4 d4, 2 d5). Long-form: a test result and its reverse. Code drill `drl.pre.simulate-check` (d4): `simulate(event, condition, trials, seed)` estimates $P(\text{event} \mid \text{condition})$ for two dice and reports the estimate with its standard error. Hidden tests: with seed 4226 and $10^5$ trials the estimate of $P(\text{total } 10 \mid \text{at least one } 5)$ lies within 4 standard errors of $\frac{1}{11}$; an impossible condition raises `ZeroDivisionError`; the same seed gives the same result.

- *Example A (long-form, d4).* A disease affects 1% of people. A test detects it in 99% of people who have it and wrongly flags 5% of people who do not. Someone tests positive. Find the probability that they have the disease, and explain in writing why it is so far from 99%.
  *Model answer.* (1) Take 10,000 people: 100 have the disease, 9,900 do not. (2) Of the 100, 99 test positive. (3) Of the 9,900, 5% test positive: 495. (4) Positives: $99 + 495 = 594$, of whom 99 are ill: $P(\text{ill} \mid +) = \frac{99}{594} = \frac{1}{6} \approx 16.7\%$. (5) The 99% is $P(+ \mid \text{ill})$, the reverse conditional. (6) The healthy group is 99 times bigger, so its small false-positive rate produces five times as many positives as the true cases: the condition shrinks the sample space to the positives, and most of them are healthy.
  *Rubric (10).* 2: a natural-frequency table or tree (line 1). 1: true positives (line 2). 2: false positives (line 3). 2: the conditional probability (line 4). 1: the reverse conditional named (line 5). 2: the explanation in words using base rates (line 6).
- *Example B (d5).* A bag holds 4 red and 6 blue counters. Three are drawn without replacement. Find $P(\text{at least one red})$ and $P(\text{exactly two red} \mid \text{at least one red})$.
  *Answer.* $P(\text{no red}) = \frac{\binom{6}{3}}{\binom{10}{3}} = \frac{20}{120} = \frac{1}{6}$, so $P(\text{at least one red}) = \frac{5}{6}$. $P(\text{exactly two red}) = \frac{\binom{4}{2}\binom{6}{1}}{120} = \frac{36}{120} = \frac{3}{10}$. Since "exactly two red" lies inside "at least one red", the conditional probability is $\frac{3/10}{5/6} = \frac{9}{25}$. Decision point: the intersection is the smaller event itself, which is easy to miss when applying the formula mechanically.

**C5 Data and statistics** (`set.chance.data`). 10 items (4 d3, 4 d4, 2 d5). Long-form: comparing two distributions. Code drill `drl.pre.summary-stats` (d3): `five_number(data, method)` with `method` either `"gcse"` (median and quartiles at positions $\frac{n+1}{2}$, $\frac{n+1}{4}$, $\frac{3(n+1)}{4}$ with linear interpolation) or `"inclusive"` (matching `statistics.quantiles(method="inclusive")`). Hidden tests: both methods agree on the median; they differ on quartiles for $n = 10$ and the test names the difference; an empty list raises `ValueError`.

- *Example A (long-form, d4).* Two classes sat the same test. Class A: minimum 22, lower quartile 48, median 61, upper quartile 70, maximum 98. Class B: minimum 35, lower quartile 52, median 58, upper quartile 63, maximum 71. Compare the two distributions in context.
  *Model answer.* (1) Class A's median (61) is higher than class B's (58), so a typical student in A scored a little higher. (2) Class A's interquartile range is $70 - 48 = 22$ and class B's is $63 - 52 = 11$, so the middle half of B is twice as consistent. (3) A's range (76) against B's (36) points the same way but depends on two single students. (4) A has the weakest and the strongest students. (5) Conclusion in context: A did slightly better on average, B was much more consistent. (6) A median difference of 3 marks with spreads this size may not be meaningful; deciding that needs the methods of 1.6.
  *Rubric (10).* 2: medians compared in context (line 1). 3: interquartile ranges computed and compared in context (line 2). 1: why range is weaker (line 3). 1: extremes (line 4). 2: a two-part conclusion in context (line 5). 1: caution about the size of the difference (line 6).
- *Example B (d5).* A histogram shows times $t$ minutes with classes $0 \le t < 10$ (frequency density 1.2), $10 \le t < 15$ (4.0), $15 \le t < 30$ (2.0) and $30 \le t < 60$ (0.5). Find the total frequency and estimate the median and the mean.
  *Answer.* Frequencies are density times width: 12, 20, 30, 15; total 77. The median is the $38.5$th value: the cumulative totals are 12, 32, 62, so it lies in the third class, $15 + \frac{38.5 - 32}{30} \times 15 = 18.25$ minutes. Mean estimate from midpoints 5, 12.5, 22.5, 45: $\frac{60 + 250 + 675 + 675}{77} = \frac{1660}{77} \approx 21.6$ minutes. Decision point: reading bar heights as frequencies gives a total of 7.7, which is impossible for counts.

**R1 Logic and proof** (`set.rigour.logic`). 8 items (3 d3, 3 d4, 2 d5). Long-form: $\log_2 3$ is irrational. Code drill `drl.pre.counterexample` (d3): `first_counterexample(claim, start, stop)` returns the first integer in the range where `claim(n)` is false, or `None`. Hidden tests: "$n^2 + n + 41$ is prime" fails first at 40; "$2^n > n^2$" from 5 to 1,000 returns `None`; "$n^2 - n + 41$ is prime" fails first at 41.

- *Example A (long-form, d4).* Prove that $\log_2 3$ is irrational.
  *Model answer.* (1) Suppose, for contradiction, that $\log_2 3 = \frac{p}{q}$ with $p$, $q$ whole numbers and $q > 0$. (2) Since $3 > 1$, $\log_2 3 > 0$, so $p > 0$. (3) By definition $2^{p/q} = 3$, and raising both sides to the power $q$ gives $2^p = 3^q$. (4) The left side is even because $p \ge 1$. (5) The right side is odd, as a product of odd numbers. (6) An even number cannot equal an odd one: contradiction, so $\log_2 3$ is irrational.
  *Rubric (10).* 2: the assumption stated precisely (line 1). 1: sign of $p$ (line 2). 2: conversion to $2^p = 3^q$ (line 3). 2: parity of each side with reasons (lines 4, 5). 2: the contradiction and conclusion (line 6). 1: the proof never assumes lowest terms, because it does not need them.
- *Example B (d5).* Prove that for every integer $n$, $n^2$ leaves remainder 0 or 1 on division by 4. Hence prove that no integer of the form $4k + 3$ is a sum of two squares.
  *Answer.* Cases: $n = 2m$ gives $n^2 = 4m^2$, remainder 0; $n = 2m + 1$ gives $n^2 = 4(m^2 + m) + 1$, remainder 1. A sum of two squares therefore leaves remainder $0 + 0$, $0 + 1$ or $1 + 1$, that is 0, 1 or 2, never 3. Decision point: trying sums of squares one by one never proves "no"; working with remainders turns infinitely many cases into four.

**R2 Proof by induction** (`set.rigour.induction`). 8 items (3 d3, 3 d4, 2 d5). Long-form: the sum of cubes. Code drill `drl.pre.check-formula` (d3): `first_failure(formula, brute, n_max)` compares a claimed closed form with a brute-force sum for $n = 1$ to `n_max` in exact integers. Hidden tests: the sum of cubes passes to $n = 10{,}000$; $\frac{n(n+1)(2n+1)}{6}$ passes for squares; a wrong formula fails first at the documented $n$; the docstring states that passing is evidence, not proof.

- *Example A (long-form, d4).* Prove by induction that $\sum_{k=1}^{n} k^3 = \left(\frac{n(n + 1)}{2}\right)^2$ for every $n \ge 1$.
  *Model answer.* (1) Base case $n = 1$: left side 1, right side $1^2 = 1$. (2) Hypothesis: suppose the formula holds for $n = m$. (3) Then $\sum_{k=1}^{m+1}k^3 = \frac{m^2(m + 1)^2}{4} + (m + 1)^3$. (4) $= \frac{(m + 1)^2}{4}(m^2 + 4m + 4) = \frac{(m + 1)^2(m + 2)^2}{4}$. (5) That is the formula with $n = m + 1$. (6) Since it holds for 1 and each case implies the next, it holds for every $n \ge 1$.
  *Rubric (10).* 2: base case (line 1). 1: hypothesis stated for a general $m$ (line 2). 2: the next sum written using the hypothesis (line 3). 3: algebra to the target form (line 4). 1: matching the target (line 5). 1: conclusion sentence (line 6).
- *Example B (d5).* Prove that $2^n > n^2$ for every integer $n \ge 5$, and explain why the induction cannot start at $n = 3$.
  *Answer.* Base: $2^5 = 32 > 25$. Step: if $2^m > m^2$ with $m \ge 5$, then $2^{m+1} = 2 \cdot 2^m > 2m^2$, and $2m^2 \ge (m + 1)^2$ because $m^2 - 2m - 1 = (m - 1)^2 - 2 \ge 14 > 0$ for $m \ge 5$. So $2^{m+1} > (m + 1)^2$. At $n = 3$ the claim is false ($8 < 9$) and at $n = 4$ it fails too ($16 = 16$, not greater). It is true at $n = 1$, but the step fails at $m = 1$ and $m = 2$ (there $(m - 1)^2 - 2 < 0$), so no base case below 5 starts a chain the step can carry. Decision point: the step itself works from $m = 3$, which tempts a start there; a valid step is worthless without a true base.

**R3 Rational functions and partial fractions** (`set.rigour.rational`). 8 items (3 d3, 3 d4, 2 d5). Long-form: an oblique asymptote and which side the curve lies on. Code drill `drl.pre.telescoping` (d3): `partial_sum(n)` adds $\sum_{k=1}^{n}\frac{1}{k(k + 1)(k + 2)}$ in `Fraction`s; `closed_form(n)` returns $\frac{n(n + 3)}{4(n + 1)(n + 2)}$. Hidden tests: equal for $n = 1$ to 200; `partial_sum(1) == Fraction(1, 6)`; the limit check $\lvert \frac{1}{4} - \text{closed\_form}(10^6) \rvert < 10^{-12}$.

- *Example A (long-form, d4).* Show that $f(x) = \frac{2x^2 - 3x + 4}{x - 2}$ has the oblique asymptote $y = 2x + 1$, and decide on which side of it the curve lies for large positive and large negative $x$. Explain why a rational function whose numerator has degree one more than its denominator always has an oblique asymptote.
  *Model answer.* (1) Divide: $2x^2 - 3x + 4 = (x - 2)(2x + 1) + 6$, checked by expanding $(x - 2)(2x + 1) = 2x^2 - 3x - 2$. (2) So $f(x) = 2x + 1 + \frac{6}{x - 2}$ for every $x \ne 2$. (3) As $x \to \pm\infty$, $\frac{6}{x - 2} \to 0$, so the vertical gap between $f(x)$ and $2x + 1$ shrinks to 0: $y = 2x + 1$ is an asymptote. (4) For $x > 2$ the remainder term $\frac{6}{x - 2}$ is positive, so the curve lies above the line; for $x < 2$ it is negative, so the curve lies below. (5) In general, dividing $p(x)$ by $q(x)$ with $\deg p = \deg q + 1$ gives a linear quotient $mx + c$ and a remainder $r(x)$ of lower degree than $q(x)$. (6) Then $f(x) = mx + c + \frac{r(x)}{q(x)}$, and $\frac{r(x)}{q(x)} \to 0$ because its denominator has the higher degree, so $y = mx + c$ is the asymptote; a horizontal asymptote is the case $m = 0$.
  *Rubric (10).* 2: the division with a check (line 1). 1: the rewritten form with $x \ne 2$ (line 2). 2: the vanishing remainder term and the conclusion (line 3). 2: both sides decided from the sign of the remainder term (line 4). 2: the general division with the degree condition (line 5). 1: why the remainder fraction vanishes, and the link to horizontal asymptotes (line 6).
- *Example B (d5).* Find $\sum_{k=1}^{n}\frac{1}{k(k + 1)(k + 2)}$ and its limit as $n \to \infty$.
  *Answer.* Partial fractions in pairs: $\frac{1}{k(k + 1)(k + 2)} = \frac{1}{2}\left(\frac{1}{k(k + 1)} - \frac{1}{(k + 1)(k + 2)}\right)$. The sum telescopes: $\frac{1}{2}\left(\frac{1}{2} - \frac{1}{(n + 1)(n + 2)}\right) = \frac{n(n + 3)}{4(n + 1)(n + 2)}$, which tends to $\frac{1}{4}$. Decision point: splitting into three single fractions $\frac{1}{2k} - \frac{1}{k + 1} + \frac{1}{2(k + 2)}$ also works but hides the cancellation; grouping into a difference of consecutive terms shows it at once.

**R4 Conics and parametric curves** (`set.rigour.conics`). 8 items (3 d3, 3 d4, 2 d5). Long-form: the ellipse equation. Code drill `drl.pre.classify-conic` (d4): `classify(A, C, D, E, F)` for $Ax^2 + Cy^2 + Dx + Ey + F = 0$ returns the type, centre and semi-axes, including the degenerate cases. Hidden tests: $(4, 9, -16, 18, -11)$ gives an ellipse with centre $(2, -1)$ and semi-axes 3 and 2; $(1, 1, 0, 0, 1)$ gives "empty"; $(1, -1, 0, 0, 0)$ gives "pair of lines"; $(0, 1, -4, 0, 0)$ gives a parabola.

- *Example A (long-form, d4).* Derive the equation of the set of points whose distances from $F_1 = (-c, 0)$ and $F_2 = (c, 0)$ add to $2a$, where $a > c > 0$.
  *Model answer.* (1) $\sqrt{(x + c)^2 + y^2} + \sqrt{(x - c)^2 + y^2} = 2a$. (2) Move one root across and square: $(x + c)^2 + y^2 = 4a^2 - 4a\sqrt{(x - c)^2 + y^2} + (x - c)^2 + y^2$. (3) Simplify: $4cx - 4a^2 = -4a\sqrt{(x - c)^2 + y^2}$, so $a\sqrt{(x - c)^2 + y^2} = a^2 - cx$. (4) Square again: $a^2(x^2 - 2cx + c^2 + y^2) = a^4 - 2a^2cx + c^2x^2$, so $(a^2 - c^2)x^2 + a^2y^2 = a^2(a^2 - c^2)$. (5) Let $b^2 = a^2 - c^2 > 0$ and divide: $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$. (6) Squaring can add points, so check: every point of this curve has $\lvert x \rvert \le a$, so $a^2 - cx > 0$ and the steps reverse; no impostors.
  *Rubric (10).* 1: the defining equation (line 1). 2: isolate and square (line 2). 1: simplify (line 3). 2: second squaring and collection (line 4). 2: $b^2$ introduced with its sign (line 5). 2: the reversibility check (line 6).
- *Example B (d5).* Find the curve of points whose distance from $(4, 0)$ is half their distance from the line $x = 16$. Identify it fully.
  *Answer.* $\sqrt{(x - 4)^2 + y^2} = \frac{1}{2}\lvert x - 16 \rvert$. Square and multiply by 4: $4(x^2 - 8x + 16 + y^2) = x^2 - 32x + 256$, so $3x^2 + 4y^2 = 192$ and $\frac{x^2}{64} + \frac{y^2}{48} = 1$. An ellipse with centre the origin, semi-axes $a = 8$ and $b = 4\sqrt{3}$, foci $(\pm 4, 0)$ (since $c^2 = 64 - 48 = 16$) and eccentricity $\frac{1}{2}$. Decision point: the focus-directrix definition with ratio below 1 gives an ellipse; ratio 1 would give a parabola, above 1 a hyperbola.

**R5 Limits and continuity** (`set.rigour.limits`). 8 items (3 d3, 3 d4, 2 d5). Long-form: $\frac{\sin x}{x} \to 1$. Code drill `drl.pre.limit-table` (d4): `table(f, a, ks)` evaluates $f(a \pm 10^{-k})$; learners compare $\frac{1 - \cos x}{x^2}$ with the rewritten $\frac{2\sin^2(x/2)}{x^2}$. Hidden tests: at $x = 10^{-8}$ the first form returns 0.0 in floating point while the rewrite returns 0.5 to $10^{-12}$; the function documents why (cancellation in $1 - \cos x$).

- *Example A (long-form, d4).* Show that $\lim_{x \to 0}\frac{\sin x}{x} = 1$, using areas in the unit circle.
  *Model answer.* (1) Take $0 < x < \frac{\pi}{2}$, O the centre, A $= (1, 0)$, P the point at angle $x$, and T where the tangent at A meets OP extended. (2) Triangle OAP $\subset$ sector OAP $\subset$ triangle OAT, so their areas satisfy $\frac{1}{2}\sin x \le \frac{1}{2}x \le \frac{1}{2}\tan x$. (3) Divide by $\frac{1}{2}\sin x > 0$: $1 \le \frac{x}{\sin x} \le \frac{1}{\cos x}$, so $\cos x \le \frac{\sin x}{x} \le 1$. (4) As $x \to 0^+$, $\cos x \to 1$, so $\frac{\sin x}{x}$ is squeezed to 1. (5) $\frac{\sin x}{x}$ is even, so the left-hand limit is the same. (6) The proof uses radians: the sector area $\frac{1}{2}x$ is true only when $x$ is in radians.
  *Rubric (10).* 1: the figure (line 1). 3: the three areas and the containment (line 2). 2: the inequality rearranged correctly (line 3). 2: the squeeze (line 4). 1: the negative side (line 5). 1: why radians (line 6).
- *Example B (d5).* Find $\lim_{x \to \infty}\left(\sqrt{x^2 + 3x} - x\right)$ and $\lim_{x \to 0}\frac{\sqrt{1 + x} - \sqrt{1 - x}}{x}$.
  *Answer.* First: multiply by $\frac{\sqrt{x^2 + 3x} + x}{\sqrt{x^2 + 3x} + x}$ to get $\frac{3x}{\sqrt{x^2 + 3x} + x} = \frac{3}{\sqrt{1 + 3/x} + 1} \to \frac{3}{2}$. Second: multiply by the conjugate to get $\frac{2x}{x(\sqrt{1 + x} + \sqrt{1 - x})} = \frac{2}{\sqrt{1 + x} + \sqrt{1 - x}} \to 1$. Decision point: "$\infty - \infty = 0$" gives 0 for the first; the conjugate turns the difference into a quotient whose dominant terms can be compared.

### 3.2 The Precalc Lab project (0.3, 10 hours)

Three small, tested pieces of code that check the course's mathematics against computation. Each part is a folder with a README, a script and a test file of plain `assert` checks (pytest arrives in 1.2), done in the app's code workspace on either target or on the learner's machine. Parts 1 and 2 declare `needs: []`. Part 3 declares `needs: [numpy, matplotlib]`: NumPy runs in the Artifact [measured: `spikes/README.md`]; matplotlib runs there only if its load group fits the Artifact's Python budget (ARCHITECTURE.md 6.2.5, decided at stage E8), and otherwise the plotting step opens in the web app and returns by result code (open item 7). The fits themselves are written with the standard library's `statistics.linear_regression` first, then checked against `numpy.polyfit`, so the learner meets the least-squares line before the library call.

| Part | After | Hours | Brief | Tests |
|---|---|---|---|---|
| 1. Loans and annuities | G5 | 3 | `payment`, `amortisation`, `pv_annuity`, `pv_perpetuity`; write the amortisation table of the G5 mortgage to CSV; compare monthly and annual compounding | Final balance within £0.01 of 0; $r = 0$ case; $\text{pv\_annuity} \to \text{pv\_perpetuity}$ as $n$ grows; the G5 example's £1,145.99 |
| 2. Counting checker | C4 | 3.5 | For ten formulas (permutations, combinations, multinomial, circular, stars and bars, inclusion-exclusion, derangements, lattice paths, birthday, without-replacement draws), compare the formula with brute-force enumeration for small $n$, and three probabilities with a seeded simulation reported with $\pm 3$ standard errors; a half-page results note on which check is proof and which is evidence | Every formula equals enumeration for $n \le 8$; each simulation lies within its stated band |
| 3. Straighten the curve | G4 and C5 | 3.5 | Fit Kepler's third law to the eight planets (semi-major axis in AU, period in years) on log-log axes, and fit an exponential to a synthetic price index on semi-log axes; plot both with matplotlib; report the exponent and growth rate | Kepler exponent $1.50 \pm 0.01$ (a least-squares fit of $\ln P$ on $\ln a$ gives 1.498 with the NASA planetary fact sheet's rounded values, distance in $10^6$ km and period in days, and 1.499 with precise sidereal periods and semi-major axes; both pass [check the data source the content ships]); price-index growth rate recovered to $10^{-2}$; a negative or zero value raises `ValueError` before any logarithm |

### 3.3 0.4 Computer basics

**K1 The home row and technique** (`set.keys.home-row`). 6 items: a 2-minute home-row passage at 15 words per minute and 95% (d3); a 2-minute all-letters passage at 15 (d3); a 1-minute accuracy run at 98% (d4); five logged practice sessions of 10 minutes (d4); the long-form (d4); 20 words per minute at 95% on unseen prose (d5), which fills the drill slot (section 3.0), because no Python has been taught in week 1.

- *Example A (long-form, d4).* A friend wants to reach 50 words per minute quickly and practises by typing as fast as possible, ignoring errors. Explain in writing why that is slower than practising accuracy first.
  *Model answer.* (1) Every error costs two extra keystrokes (the wrong key and the backspace) plus a pause to notice it. (2) Practising fast with errors repeats wrong finger movements, so the errors become habits. (3) Speed comes from movements that no longer need checking, which only correct repetitions build. (4) Accuracy at a steady rhythm first, then speed in small steps, keeps the error rate low while speed rises. (5) A concrete plan: hold 95% accuracy, raise the target by 2 words per minute only after three sessions above it. (6) The trainer's heat map shows which keys cause the errors, so practice targets them.
  *Rubric (10).* 2: the cost of an error (line 1). 2: habit formation (line 2). 2: what speed is made of (line 3). 2: the order of priorities (line 4). 1: a concrete plan (line 5). 1: targeted practice (line 6).
- *Example B (d5).* In a 2-minute run you produce 500 correct characters, pressing 560 keys: 500 correct, 30 wrong and 30 backspaces. (a) Compute speed (correct characters $\div 5 \div$ minutes) and accuracy (correct keystrokes $\div$ all keystrokes). (b) Which raises speed more: typing 10% faster at the same error rate, or halving the errors at the same keystroke rate? (c) Above what error rate would halving errors win?
  *Answer.* (a) $\frac{500}{5 \times 2} = 50$ words per minute; accuracy $\frac{500}{560} \approx 89.3\%$. (b) With $e = 0.06$ errors per correct character, each correct character costs $1 + 2e = 1.12$ keystrokes at 280 keystrokes a minute. 10% faster: $\frac{308}{1.12 \times 5} = 55$ words per minute. Halved errors: $\frac{280}{1.06 \times 5} \approx 52.8$. Speed wins here. (c) Halving errors wins when $1 + 2e > 1.1(1 + e)$, that is $e > \frac{1}{9} \approx 11\%$. Decision point: the honest arithmetic says raw speed sometimes pays; the case for accuracy first is about the habits that let speed rise at all (example A), not this one-off trade.

**K2 Every key, and the shortcuts** (`set.keys.all-keys`). 6 items: a number passage at 15 words per minute (d3); a transcribe-and-run code drill `drl.comp.transcribe` (d3): type a given eight-line program into `code-cell` exactly and run it, with hidden tests comparing its printed output and flagging any curly quote, missing bracket or wrong case; a shortcut drill at 90% inside the time limit (d4); a symbols accuracy run at 97% (d4); the long-form (d4); 25 words per minute at 95% on unseen Python code text (d5).

- *Example A (long-form, d4).* A script copied from a word processor fails with `SyntaxError: invalid character '“' (U+201C)`. Explain what happened and how to avoid it.
  *Model answer.* (1) Word processors replace straight quotes `"` with curly "smart" quotes as you type. (2) Python accepts only straight quotes as string delimiters. (3) The error names the character and its code (U+201C, a left double quotation mark), which identifies the cause. (4) Fix: retype the quotes in a code editor, or replace them with find and replace. (5) Avoid: write code only in a code editor, and paste from documents as plain text. (6) The same happens with long dashes and non-breaking spaces copied from web pages.
  *Rubric (10).* 2: smart quotes (line 1). 2: why Python rejects them (line 2). 1: reading the error (line 3). 2: the fix (line 4). 2: prevention (line 5). 1: other characters (line 6).
- *Example B (d5).* Replace this mouse sequence with keyboard shortcuts on your operating system: select the word to the left of the cursor, cut it, move to the end of the line, paste it, save.
  *Answer.* Windows and Linux: Ctrl+Shift+Left, Ctrl+X, End, Ctrl+V, Ctrl+S. macOS: Option+Shift+Left, Cmd+X, Cmd+Right, Cmd+V, Cmd+S. Graded by effect in `typing-trainer`'s shortcuts mode, so any sequence producing the same text and a saved file passes. Decision point: on macOS, Ctrl+Left moves between desktops in many set-ups, and the End key goes to the end of the document in some editors.

**B1 Files and folders** (`set.bench.files`). 6 items: two path-writing tasks (d3); a naming card sort (d4); a file-manager task on the learner's machine, verified by a pasted listing (d4; the drill slot); the long-form (d4); a relative-path puzzle (d5).

- *Example A (long-form, d4).* Explain the difference between an absolute and a relative path, with one example of each from your own computer, and say when each is the better choice.
  *Model answer.* (1) An absolute path starts at the root (`/` on macOS and Linux, a drive such as `C:\` on Windows) and names every folder down to the file. (2) A relative path starts from the current folder and may use `..` to go up. (3) Examples from the learner's machine (checked for form). (4) Absolute paths always find the same file but break when a project moves to another computer or user. (5) Relative paths inside a project keep working when the whole project folder moves. (6) So code inside a project should use paths relative to the project, and one-off commands can use absolute paths.
  *Rubric (10).* 2: absolute defined (line 1). 2: relative defined, with `..` (line 2). 2: two correct personal examples (line 3). 2: the trade-off (lines 4, 5). 2: the recommendation (line 6).
- *Example B (d5).* The tree contains `/home/ana/projects/q1/analysis.py` and `/home/ana/data/prices.csv`. (a) From `/home/ana/projects/q1`, give a relative and an absolute path to `prices.csv`. (b) From `/home/ana/data`, give a relative path to the folder `q1`. (c) `analysis.py` opens `"data/prices.csv"`. From which folder must it be run for that to work?
  *Answer.* (a) `../../data/prices.csv`; `/home/ana/data/prices.csv` (or `~/data/prices.csv` for Ana). (b) `../projects/q1`. (c) From `/home/ana`, because a relative path in code is resolved against the folder the program is run from, not the folder the script lives in. Decision point: part (c) is the error behind most "file not found" messages in 1.1.

**B2 The terminal** (`set.bench.terminal`). 6 items: two navigation tasks graded by the final working folder (d3); a build-the-tree task graded by the final tree (d4; the drill slot); a predict-the-output item on `ls -a` (d4); the long-form (d4); a multi-step tidy-up graded by effect (d5).

- *Example A (long-form, d4).* Explain why `rm` and `mv` are dangerous for beginners, and three habits that prevent losing work.
  *Model answer.* (1) `rm` deletes without a recycle bin, so there is no undo. (2) `rm -r` deletes whole folders, and a wildcard like `*` can match far more than intended. (3) `mv` onto an existing file name replaces that file silently. (4) Habit: run `ls` with the same pattern first, to see exactly what will be matched. (5) Habit: use `-i` (ask before each removal or overwrite) while learning. (6) Habit: keep work under version control (1.2) or backed up, so a mistake is recoverable.
  *Rubric (10).* 2: `rm` permanence (line 1). 1: recursion and wildcards (line 2). 2: silent overwrite by `mv` (line 3). 2: preview with `ls` (line 4). 2: `-i` (line 5). 1: backups or version control (line 6).
- *Example B (d5).* The folder `week1` contains `downloads/` (holding `a.csv`, `b.csv`, `notes.txt`), `main.py` and `util.py`. From inside `week1`, produce: `data/raw/a.csv` and `data/raw/b.csv` moved from `downloads`; `notes/README.txt` containing the line `raw data from week 1`; and `count.txt` containing the number of `.py` files in `week1`. Leave `downloads/notes.txt` where it is.
  *Answer.* One correct sequence: `mkdir -p data/raw notes`; `mv downloads/*.csv data/raw/`; `echo "raw data from week 1" > notes/README.txt`; `ls *.py | wc -l > count.txt`. Graded by the final tree and file contents, so any correct sequence passes; the grader trims whitespace because `wc -l` pads its output on macOS. Decision point: `mv downloads/* data/raw/` would also move `notes.txt`.

**B3 Installing tools and the editor** (`set.bench.tools`). 6 items: paste-verify `python3 --version` (or `py --version`) and `code --version` (d3); paste-verify the output of a one-line script run from the VS Code terminal (d3); a PATH diagnosis from a pasted transcript (d4); the long-form (d4); interpreter selection in VS Code, verified by pasted `sys.executable` (d4); the two-Pythons problem (d5).

- *Example A (long-form, d4).* After installing Python, a friend's terminal says `python: command not found`. Write the diagnosis you would walk them through.
  *Model answer.* (1) The shell looks for commands in the folders listed in PATH; "not found" means no folder on PATH holds a program called `python`. (2) On macOS and Linux the command is often `python3`; try it first. (3) On Windows, try the launcher `py`; if that works, Python is installed but not on PATH, because the "Add python.exe to PATH" box was not ticked. (4) Fix on Windows: rerun the installer, choose Modify, and tick the PATH option; then open a new terminal, because PATH is read when a terminal starts. (5) Check with `where python` (Windows) or `which python3` (macOS and Linux). (6) Avoid the Microsoft Store stub, which prints a message or opens the Store instead of running Python.
  *Rubric (10).* 2: PATH explained (line 1). 2: `python3` (line 2). 2: `py` and the installer box (line 3). 2: the fix including a new terminal (line 4). 1: verification (line 5). 1: the Store stub (line 6).
- *Example B (d5).* `pip install requests` succeeds, but `python3 script.py` fails with `ModuleNotFoundError: No module named 'requests'`. Explain and fix.
  *Answer.* Two Pythons are installed, and the `pip` on PATH belongs to a different one from the `python3` that runs the script. Check with `python3 -c "import sys; print(sys.executable)"` and `pip --version`, which prints the Python it belongs to. Fix: install with the same interpreter, `python3 -m pip install requests`, and in VS Code select that interpreter. Decision point: reinstalling Python adds a third copy; `python -m pip` removes the ambiguity for good.

**Y1 Values, variables and decisions** (`set.firstpy.values`). 6 items: two predict-the-output items (d3); a Parsons problem (d4); a drill with hidden tests (d4); the long-form (d4); the difficulty-5 drill below.

- *Example A (long-form, d4).* Explain the difference between `x = x + 1` in Python and the equation $x = x + 1$ in mathematics.
  *Model answer.* (1) In mathematics, $x = x + 1$ is a claim that two values are equal; subtracting $x$ gives $0 = 1$, so no number satisfies it. (2) In Python, `=` is assignment: evaluate the right side, then make the name on the left refer to the result. (3) So `x = x + 1` reads the current value of `x`, adds 1, and rebinds `x` to the new value. (4) It needs `x` to exist already, otherwise `NameError`. (5) Python's equality test is `==`, which returns `True` or `False`. (6) Trace: `x = 3`, then `x = x + 1` leaves `x` as 4.
  *Rubric (10).* 2: mathematical meaning (line 1). 2: assignment (line 2). 2: the evaluation order (line 3). 1: `NameError` (line 4). 2: `==` (line 5). 1: a trace (line 6).
- *Example B (d5, drill `drl.comp.price-change`).* Write `describe_change(old, new)` returning `"up 12.50%"`, `"down 3.10%"` or `"flat"`, with two decimal places, and raising `ValueError` if `old` is not positive.
  *Answer and tests.* Compute `pct = (new - old) / old * 100`; return `"flat"` if `pct == 0`, else `f"up {pct:.2f}%"` or `f"down {abs(pct):.2f}%"`. Hidden tests: `(80, 90)` gives `"up 12.50%"`; `(100, 96.9)` gives `"down 3.10%"` (the float is $-3.0999\ldots$ and formats correctly); `(50, 50)` gives `"flat"`; `(0, 5)` and `(-1, 5)` raise `ValueError`. Decision point: testing `old == 0` misses negative prices; the guard is `old <= 0`.

**Y2 Loops, functions and errors** (`set.firstpy.loops`). 6 items: a predict-the-output item on `range` (d3); a traceback-reading item (d3); a `for` drill (d4); the long-form (d4); a `try`/`except` input drill (d4); the difficulty-5 drill below.

- *Example A (long-form, d4).* Explain the difference between `return` and `print` in a function, with an example where using `print` breaks a program.
  *Model answer.* (1) `print` shows a value on the screen and gives nothing back to the caller. (2) `return` hands a value back to the caller and ends the function. (3) A function without `return` gives back `None`. (4) Example: `def vat(p): print(p * 0.2)`; then `total = 100 + vat(100)` prints 20.0 and fails with `TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'`. (5) With `return p * 0.2` the sum is 120.0. (6) Rule: compute with `return`, and print only at the edge of the program.
  *Rubric (10).* 2: `print` (line 1). 2: `return` (line 2). 1: `None` (line 3). 3: a breaking example with its error (line 4). 1: the fix (line 5). 1: the rule (line 6).
- *Example B (d5, drill `drl.comp.years-to-double`).* Write `years_to_double(rate)` that uses a `while` loop to return the number of whole years for money to at least double at an annual rate `rate`, raising `ValueError` for `rate <= 0`.
  *Answer and tests.* Start `value = 1.0`, `years = 0`; while `value < 2`: multiply by `1 + rate` and add one year. Hidden tests: `0.05` gives 15; `0.07` gives 11; `1.0` gives 1; `0` and `-0.1` raise `ValueError` (without the guard the loop never ends). Decision point: `value <= 2` instead of `value < 2` returns 2 for `rate = 1.0`.

### 3.4 0.5 Mental arithmetic

**A1 Tables and the Zetamac format** (`set.speed.tables`). 6 items: a 60-second tables set (d3); a 60-second $(2..12) \times (2..100)$ set (d3); a 60-second division set (d4); the long-form (d4); code drill `drl.ment.drill-maker` (d4): `make_question(rng)` returns a Zetamac-format multiplication or division question; hidden tests check operand ranges over 10,000 seeded draws and that every division has a whole answer; the challenge (d5).

- *Example A (long-form, d4).* Show how each of $6 \times 7$, $6 \times 8$, $7 \times 8$ and $8 \times 9$ can be derived in one step from an easier fact, and name the law that justifies each step.
  *Model answer.* (1) $6 \times 7 = 6 \times 6 + 6 = 42$ (distributive law: $6 \times (6 + 1)$). (2) $6 \times 8 = 2 \times (3 \times 8) = 48$ (associative law; doubling 24). (3) $7 \times 8 = 7 \times 7 + 7 = 56$ (distributive). (4) $8 \times 9 = 8 \times 10 - 8 = 72$ (distributive, with subtraction). (5) Each derivation turns an unknown fact into a known one plus or minus a small step. (6) The point is speed in the drill: derive slowly at first, and the derived fact becomes recalled within days.
  *Rubric (10).* 2 each for lines 1 to 4 (each with the law named). 1: the general idea (line 5). 1: the practice plan (line 6).
- *Example B (d5).* Compute $12 \times 97$ and $1{,}140 \div 12$, each within 6 seconds, and write the split you used.
  *Answer.* $12 \times 97 = 12 \times 100 - 12 \times 3 = 1{,}200 - 36 = 1{,}164$. $1{,}140 \div 12$: $12 \times 95 = 1{,}140$ (from $12 \times 100 - 12 \times 5$), so 95. Decision point: splitting 97 as $90 + 7$ also works but holds more digits; rounding up and subtracting is faster for numbers just below a hundred.

**A2 Adding and subtracting fast** (`set.speed.add-sub`). 6 items: a 60-second two-digit addition set (d3); a 60-second subtraction set (d3); a chains set (d4); the long-form (d4); code drill `drl.ment.complement` (d4): `complement_1000(n)` by the digit rule, with the case of a final 0 handled; tests on all $n$ from 1 to 999 against `1000 - n`; the challenge (d5).

- *Example A (long-form, d4).* Prove that for a three-digit number with digits $a$, $b$, $c$ and $c \ne 0$, its complement to 1,000 has digits $9 - a$, $9 - b$, $10 - c$, and fix the rule for $c = 0$.
  *Model answer.* (1) $999 - (100a + 10b + c) = 100(9 - a) + 10(9 - b) + (9 - c)$, and each bracket is a digit from 0 to 9, so no borrowing occurs. (2) Adding 1 gives $1{,}000 - n$. (3) When $c \ne 0$, $9 - c \le 8$, so adding 1 makes the last digit $10 - c$ with no carry. (4) So the digits are $9 - a$, $9 - b$, $10 - c$. (5) When $c = 0$ the rule would give a last "digit" of 10; instead, complement the two-digit number $10a + b$ to 100 and append the 0. (6) Example: $1{,}000 - 630 = 370$ because $100 - 63 = 37$.
  *Rubric (10).* 3: the subtraction from 999 with no borrowing (line 1). 1: adding 1 (line 2). 2: no carry when $c \ne 0$ (line 3). 1: conclusion (line 4). 2: the $c = 0$ case (line 5). 1: an example (line 6).
- *Example B (d5).* Keep a running total, without writing, within 15 seconds: $64 + 27 - 38 + 95 - 46 + 17 - 59 + 33$.
  *Answer.* Running totals 91, 53, 148, 102, 119, 60, 93: the answer is 93. Decision point: saying each running total under your breath keeps the place; trying to hold all the numbers and add at the end fails beyond four terms.

**A3 Multiplying beyond the tables** (`set.speed.multiply`). 6 items: a 60-second $\times 5$, $\times 25$, $\times 9$, $\times 11$ set (d3); a two-digit by two-digit set (d3); a squares set (d4); the long-form (d4); code drill `drl.ment.square-trick` (d4): `square_ending_5(n)` by the rule, tested against `n * n` for every two- and three-digit number ending in 5; the challenge (d5).

- *Example A (long-form, d4).* Prove the rule for squaring a number ending in 5: $(10n + 5)^2$ is $n(n + 1)$ followed by 25.
  *Model answer.* (1) $(10n + 5)^2 = 100n^2 + 100n + 25$ (expanding $(a + b)^2$). (2) $= 100n(n + 1) + 25$. (3) Multiplying by 100 shifts $n(n + 1)$ two places left. (4) Since $25 < 100$, the last two digits are exactly 25 with no carry. (5) So the square is $n(n + 1)$ followed by 25. (6) Examples: $65^2$: $6 \times 7 = 42$, so 4,225; $115^2$: $11 \times 12 = 132$, so 13,225.
  *Rubric (10).* 3: expansion (line 1). 2: factorising (line 2). 2: place value meaning (line 3). 1: no carry (line 4). 1: conclusion (line 5). 1: examples (line 6).
- *Example B (d5).* Compute $63 \times 67$, $998 \times 1{,}002$ and $85^2$, each within 6 seconds.
  *Answer.* $63 \times 67 = 65^2 - 2^2 = 4{,}225 - 4 = 4{,}221$. $998 \times 1{,}002 = 1{,}000^2 - 2^2 = 999{,}996$. $85^2 = 8 \times 9$ followed by 25 $= 7{,}225$. Decision point: spotting the common midpoint (65 and 1,000) is the step; once seen, each is one subtraction.

**A4 Fractions, decimals, percentages and estimates** (`set.speed.fractions`). 6 items: a 60-second fractions-to-decimals set (d3); a 60-second set mixing decimal products and quotients with percentages (d3); an estimation set within 10% (d4); the long-form (d4); code drill `drl.ment.sevenths` (d4): `seventh(k)` returns the first 12 decimal digits of $\frac{k}{7}$ by long division with remainders, tested against the cycle 142857 starting at the right point for $k = 1$ to 6; the challenge (d5).

- *Example A (long-form, d4).* Explain why $\frac{1}{7}$ has a repeating cycle of six digits, and why $\frac{2}{7}, \dots, \frac{6}{7}$ use the same six digits in the same cyclic order.
  *Model answer.* (1) Long division of 1 by 7 produces a remainder at each step, always one of 1 to 6 (0 would end the division, which never happens because 7 does not divide a power of 10). (2) Once a remainder repeats, the digits repeat from there. (3) For $\frac{1}{7}$ the remainders run 1, 3, 2, 6, 4, 5, then 1 again: all six appear, so the cycle has length 6: $0.\overline{142857}$. (4) Dividing $k$ by 7 is the same process started at remainder $k$. (5) Every remainder 1 to 6 already lies on the cycle, so $\frac{k}{7}$ joins it at a different point and produces the same digits from there. (6) Example: $\frac{3}{7}$ starts at remainder 3, the second step of the cycle, giving $0.\overline{428571}$.
  *Rubric (10).* 2: possible remainders (line 1). 2: repetition (line 2). 2: the actual cycle (line 3). 2: starting at remainder $k$ (line 4). 1: same digits (line 5). 1: example (line 6).
- *Example B (d5).* Estimate $\frac{0.0487 \times 6{,}130}{2.9}$ to within 10% in under 10 seconds, showing your rounding.
  *Answer.* $\frac{0.05 \times 6{,}000}{3} = 100$. The exact value is about 102.9, so the estimate is within 3%. Decision point: rounding 0.0487 up and 6,130 down lets the errors partly cancel; rounding both up would have compounded them.

---

## 4. Topic exam blueprint and the Stage 0 exit test

### 4.1 0.3 Precalculus topic exam (`exm.pre.topic`)

Kind `topic` (ASSESSMENT.md 3.1): timed, no hints, Bertie away app-wide (AI-TUTOR.md 2.12), one sitting, resits after a 3-day cool-down and a remediation set on the failed skills (ASSESSMENT.md decision 5). It can be sat before the lessons to test out of 0.3 (ASSESSMENT.md 7.3).

| Property | Value |
|---|---|
| Duration | 90 minutes in two timed sections (ASSESSMENT.md decision 27): **A**, non-calculator, 40 minutes, 32 marks; **B**, calculator allowed (the in-app scientific calculator, locked during A), 50 minutes, 48 marks. Section A closes for good when its time ends or the learner finishes it |
| Items | 24 items, **80 marks**; multi-part items mark per part, the intermediate result asked as its own part so that a slip in the last step keeps the earlier marks |
| Difficulty mix, by marks | 16 at d2 (20%), 40 at d3 (50%), 16 at d4 (20%), 8 at d5 (10%) |
| Format mix, by marks | Numeric 28; mixed numeric with a short choice, reason or interval part 10; expression 14; interval or solution set 6; matrix 3; point on a graph 3; long-form 16 (20%, under the kind's 30% ceiling), each a 10-point rubric scaled to 8 marks. Choice appears only inside mixed items (at most 2 marks) |
| Pass mark | 70%: 56 of 80. No section bar |
| Forms | At least 3 parallel forms with equal marks; 60 of 80 marks come from generator slots (75%, above ASSESSMENT.md 3.2's 50% floor), so a resit never repeats a parameter point; the three authored pools hold at least six items each |
| Practice | Two practice papers built from the practice pool, never from the exam reserve |

**Slots.**

| Slot | Section | Level | Skill | Format | Difficulty | Marks |
|---|---|---|---|---|---|---|
| A1 | A | S6 | Exact trigonometric values in a right triangle | X | 2 | 2 |
| A2 | A | S5 | Circle-theorem angle chase, each step with its named reason (authored pool) | N + S | 3 | 4 |
| A3 | A | S8 | Ratio point or collinearity with vectors | X | 3 | 3 |
| A4 | A | G3 | Simplify with the log laws | X | 2 | 2 |
| A5 | A | G3 | Exponential equation hiding a quadratic | I | 3 | 3 |
| A6 | A | G5 | Sum to infinity or recurring decimal | X | 2 | 2 |
| A7 | A | T1 | Related angles, exact values | X | 2 | 2 |
| A8 | A | T3 | Trigonometric equation in a range | I | 3 | 3 |
| A9 | A | C3 | A coefficient in a binomial expansion | N | 3 | 3 |
| A10 | A | C1 | Counting with a restriction | N | 3 | 3 |
| A11 | A | R5 | A limit by factorising or rationalising | N | 2 | 2 |
| A12 | A | R3 | Partial fractions | X | 3 | 3 |
| B1 | B | S7 | Ambiguous-case triangle: every possible side | N (two parts) | 4 | 4 |
| B2 | B | S2, S3 | Frustum or similar solids | N | 3 | 3 |
| B3 | B | S8 | Angle between vectors by the dot product | N | 3 | 3 |
| B4 | B | G2 | Effective annual rates compared | N + C | 3 | 3 |
| B5 | B | G5 | Loan payment or annuity value | N | 4 | 4 |
| B6 | B | T4 | $R\sin(x + \alpha)$: maximum and an equation | N + I | 3 | 3 |
| B7 | B | T5 | Matrix image, determinant and inverse | A | 3 | 3 |
| B8 | B | T6 | Roots of a complex number on the Argand diagram | P | 2 | 3 |
| B9 | B | C4 | Conditional probability without replacement | N | 3 | 3 |
| B10 | B | C5 | Histogram: total, median and mean estimate | N | 2 | 3 |
| B11 | B | R2 | Proof by induction: a sum, a divisibility or an inequality (authored pool) | Long-form, scaled to 8 | 5 | 8 |
| B12 | B | G4, C4 or T4 by form | Written explanation, rotating: log against simple returns; $P(A \mid B)$ against $P(B \mid A)$; $\cos(A - B)$ from the dot product (authored pool) | Long-form, scaled to 8 | 4 | 8 |

**Checks on the table.** Section A: 32 marks (d2 10, d3 22). Section B: 48 marks (d2 6, d3 18, d4 16, d5 8). Marks by course: S 19, G 14, T 14, C 12, R 13, plus B12's 8 for G, C or T by form. Against the courses' shares of 0.3's lessons (S 26%, G 18.5%, T 22%, C 18%, R 15.5%, which on 80 marks is about 21, 15, 17.5, 14 and 12.5), the fixed slots sit within 4 marks of every share, and the course B12 rotates to sits up to 8 marks above its share on that form. The over-weight is deliberate: the three explanations are what a quant is asked to say aloud, and a paper that tests them only by calculation would miss them.

**Topic exit part.** The schema needs at least one exit part per topic (`CONTENT-FORMAT.md` 3.2, `Topic.exit`), and the sibling file gives 0.1 and 0.2 one each (`stage0-number-algebra.md` 4.3). 0.3's is its topic exam, on the same pattern; 0.4 and 0.5 are closed by the stage parts `s0.script` and `s0.zetamac` (sections 4.2 and 4.3). Its `estHours` comes out of the 2 hours of marking and review already in the Exams block of 1.1, not on top of them.

| Exit part | Gate | Confirm | `estHours` |
|---|---|---|---|
| `0.3.exit` | `exm.pre.topic` at 70% | None | 1.0 (reviewing the topic exam and the two practice papers) |

### 4.2 0.4 Computer basics: no topic exam; practical rehearsal (ungated)

ASSESSMENT.md 2.8 closes 0.4 with its exit part, `s0.script`. Before the learner spends that on their own machine, the app offers an ungated **practical rehearsal** (`exm.comp.practical`): 30 minutes, 10 tasks, 20 marks, in `shell-sim`, `workspace-sim` and `code-cell`, graded by effect and by hidden tests. Difficulty by marks follows the topic-exam mix (4 at d2, 10 at d3, 4 at d4, 2 at d5). The planner recommends `s0.script` once the rehearsal reaches 70%.

| Task | Skill | Format | Difficulty | Marks |
|---|---|---|---|---|
| 1 | Navigate to a named folder and show the working directory | H | 2 | 2 |
| 2 | Write the relative path between two files in a tree | H | 2 | 2 |
| 3 | Build a given folder layout | H | 3 | 2 |
| 4 | Move and rename files with a wildcard, leaving one file alone | H | 3 | 2 |
| 5 | Predict the output of a five-line script | T | 3 | 2 |
| 6 | Fix a script that fails because `input()` returns text | K | 3 | 2 |
| 7 | Run a script from the right folder and save its output with `>` | H | 3 | 2 |
| 8 | Write a function with a loop that passes hidden tests | K | 4 | 2 |
| 9 | Diagnose a pasted "command not found" transcript and give the fix | H | 4 | 2 |
| 10 | The ten-line script task on a fresh seed, end to end in `workspace-sim` | K | 5 | 2 |

The typing outcome C-O1 is measured separately by the `typing-trainer` benchmark (median of three 2-minute runs) and is not part of the Stage 0 exit.

### 4.3 0.5 Mental arithmetic: no topic exam; benchmark sitting (ungated)

0.5 closes with `s0.zetamac`. Its instrument is a score, so the topic-exam difficulty mix does not apply: Zetamac's default ranges fix the item distribution (decision 13). An ungated 30-minute benchmark sitting, offered every four weeks, records the following. It is a `speed-drill` session, not an exam-engine paper, because speed formats keep their own timers inside the widget (ASSESSMENT.md 3.1); it shares the integrity record, and Bertie is unavailable throughout.

| Part | Format | Time | Recorded |
|---|---|---|---|
| Three cold runs | Zetamac defaults, physical keyboard, auto-advance | 3 × 120 s | The median score, the target being 25 |
| Fact scan | The 78 distinct products to $12 \times 12$, once each, shuffled | about 3 min | Each fact's response time; facts with a median above 2 s go to the targeted deck of the Daily 10 (ASSESSMENT.md 9.4) |
| Mixed set | 40 items: 10 each of decimals, fractions to decimals, percentages and two-digit by two-digit products, at the d2 to d5 mix 8, 20, 8, 4 | 8 min | Accuracy and median time per type |
| 80-in-8 preview | Multiple choice, minus 1 per wrong answer, no skipping (ASSESSMENT.md decision 16) | 8 min | Net score, recorded but not targeted until Stage 3 |

A benchmark has no pass mark; it tells the planner which decks the Daily 10 should weight next.

### 4.4 The Stage 0 exit test, rebuilt in the app

The curriculum closes Stage 0 with four checkboxes. ASSESSMENT.md 2.9 turns each into an exit part with an in-app gate and, where the curriculum names a real paper, a logged confirmation. "Sit each stage's exit test first": every part can be attempted before the stage's lessons, and passing all four skips the stage.

| Part | Curriculum line | Gate (in the app) | Confirm (logged) | Taught in |
|---|---|---|---|---|
| `s0.gcse` | A GCSE Higher non-calculator past paper, timed, at 80% or better | GCSE-style Paper 1 (kind `gcse`) at 80% | One real Higher Paper 1, timed at 90 minutes, self-marked with the board's mark scheme, at 80% | 0.1, 0.2, 0.3 courses S and C |
| `s0.precalc` | Khan Academy Precalculus course challenge at 85% or better | Precalculus challenge (kind `challenge`) at 85% | The Khan Academy course challenge result at 85% | 0.2 course F, 0.3 |
| `s0.zetamac` | Zetamac score of 25 or more on default settings | Median of the last 7 days' cold scores, physical keyboard, at least 5 runs, at 25 or more | None: the in-app run is the Zetamac format | 0.5 |
| `s0.script` | Make a folder, write a ten-line Python script in it and run it from the terminal | `setup-checklist` paste-verify | None | 0.4 |

**`s0.gcse`: the GCSE-style Paper 1.**

- **Format.** 80 marks, 90 minutes, non-calculator, 26 questions in rising order of demand, as on a real Higher Paper 1 (AQA 8300/1H and Edexcel 1MA1/1H are 80 marks in 90 minutes [sourced: ASSESSMENT.md 0.2]).
- **Content by marks**, following Ofqual's Higher-tier weightings (ASSESSMENT.md 2.11): Number 12 (15%), Algebra 24 (30%), Ratio, proportion and rates of change 16 (20%), Geometry and measures 16 (20%), Probability and statistics 12 (15%).
- **Assessment objectives**, by marks: AO1 (use and apply standard techniques) 32, AO2 (reason, interpret and communicate) 24, AO3 (solve problems) 24, matching the Higher weights of 40%, 30% and 30% [searched: AQA 8300 scheme of assessment].
- **Marking like a mark scheme.** Method marks become intermediate answer fields in multi-part items, accuracy marks grade the final field, and "show that" or proof parts are short long-form items with 2- to 4-point rubrics. Diagrams carry the "not drawn accurately" flag and are built by `geometry-board` in read-only mode, so no answer can be measured off the screen.
- **Difficulty by marks:** 18 at d2, 36 at d3, 17 at d4, 9 at d5 (about 22%, 45%, 21%, 11%), a real paper's ramp rather than the topic-exam mix.
- **Forms.** At least 5 forms, or at least half the marks from generators (ASSESSMENT.md decision 4). Resits after a 7-day cool-down.

| Q | Strand | Content | Taught in | Difficulty | Marks |
|---|---|---|---|---|---|
| 1 | Number | Fraction and mixed-number arithmetic | 0.1 W4 | 2 | 2 |
| 2 | Number | Standard form calculation | 0.1 P3 | 2 | 3 |
| 3 | Algebra | Expand and simplify; nth term of a linear sequence | 0.2 E2, L1 (lesson 41) | 2 | 4 |
| 4 | Ratio | Percentage change and best buy | 0.1 P1, P2 | 2 | 4 |
| 5 | Geometry | Angles in polygons with reasons | 0.3 S1 | 2 | 3 |
| 6 | Probability and statistics | Venn diagram or two-way table probability | 0.3 C4 | 2 | 2 |
| 7 | Number | Index laws with negative and fractional indices | 0.1 P3 | 3 | 3 |
| 8 | Algebra | Linear equation with fractions | 0.2 E4 | 3 | 3 |
| 9 | Algebra | Simultaneous equations, one quadratic or both linear | 0.2 L3, Q3 | 3 | 3 |
| 10 | Algebra | Quadratics: factorise, complete the square, turning point | 0.2 Q1, Q2 | 3 | 4 |
| 11 | Ratio | Sharing in a ratio with a given difference | 0.1 P2 | 3 | 3 |
| 12 | Ratio | Direct or inverse proportion with a formula | 0.1 P2 | 3 | 3 |
| 13 | Ratio | Compound growth or depreciation with multipliers | 0.1 P1; 0.3 G2 | 3 | 3 |
| 14 | Geometry | Compound area or volume (cone, sphere, sector) in terms of $\pi$ | 0.3 S2 | 3 | 4 |
| 15 | Geometry | Pythagoras and exact trigonometric values | 0.3 S3, S6 | 3 | 3 |
| 16 | Probability and statistics | Histogram with unequal widths | 0.3 C5 | 3 | 4 |
| 17 | Probability and statistics | Tree diagram without replacement | 0.3 C4 | 3 | 3 |
| 18 | Number | Surds: simplify and rationalise a denominator | 0.1 P3 | 4 | 2 |
| 19 | Algebra | Algebraic proof about integers | 0.2 E3 | 4 | 3 |
| 20 | Algebra | Composite and inverse functions | 0.2 F1 | 4 | 3 |
| 21 | Ratio | Gradient of a curve at a point or area under a velocity-time graph | 0.2 L2, F4 (lessons 43, 109, 110) | 4 | 3 |
| 22 | Geometry | Circle-theorem proof with reasons | 0.3 S5 | 4 | 3 |
| 23 | Probability and statistics | Conditional probability from a table or a Venn diagram | 0.3 C4 | 4 | 3 |
| 24 | Number | Recurring decimal to fraction, with the algebraic argument | 0.1 P1 | 5 | 2 |
| 25 | Algebra | Intersection of a line and a circle | 0.2 Q3 (lessons 71, 72) | 5 | 4 |
| 26 | Geometry | Vector proof of collinearity | 0.3 S8 | 5 | 3 |

The "Taught in" column was checked against the final level lists of `stage0-number-algebra.md`.

**Confirm.** One real Higher Paper 1, from any board and series, sat timed at 90 minutes and self-marked against the board's published mark scheme, logged at 80% or better. OCR's Higher non-calculator paper is J560/05 (Paper 5), 100 marks in 1 hour 30 minutes [searched], so it is logged as a percentage (80 of 100). Real past papers are single-use: the planner offers the confirm only after the in-app paper is passed (ASSESSMENT.md decision 1). 80% on a Higher paper typically sits around grade 8 or above, depending on the series' boundaries [check].

**`s0.precalc`: the Precalculus challenge.**

- **Model.** Khan Academy's course challenge: roughly 30 questions drawn from across the course's units [check the count], untimed on Khan [check], with some items offering an on-screen calculator [check].
- **Ours.** 30 one-mark items, 60 minutes (a generous limit that stops a sitting spreading over days), calculator allowed on items flagged for it. Three items from each of ten units: composite and inverse functions (drawn from 0.2 course F's generators), trigonometry, complex numbers, rational functions, conic sections, vectors, matrices, probability and combinatorics, series, limits and continuity. A search on 6 October 2026 found the course description naming every one of these except rational functions, with series and limits as optional units and limits as unit 10 [searched, secondary]; rational functions stay [check]. ASSESSMENT.md 2.11's search summary names polynomials and no trigonometry unit; the search here found that list only on an older listing, so it looks out of date, and the trigonometry slots stand. If the live course turns out to have a polynomials unit in place of rational functions, those three slots draw from 0.2 course Q's generators instead, and 0.3 loses nothing (open item 3).
- **Difficulty by items:** 12 at d2, 15 at d3, 3 at d4, the level of Khan's unit tests.
- **Formats:** numeric and expression entry at least 60% of items; single choice at most 40%, as Khan's items are often multiple choice; graph items where Khan uses them.
- **Pass:** 85%, that is 26 of 30.
- **Confirm:** the learner sits the real course challenge on khanacademy.org and logs the percentage, labelled self-reported (ASSESSMENT.md decision 18).

**`s0.zetamac`: the arithmetic score.** The Daily 10's cold 120-second run is the instrument (ASSESSMENT.md decision 15), on the defaults of decision 13. The part is met when the median of the last 7 study days' cold scores, on a physical keyboard, with at least 5 runs in the window, is 25 or more. Runs on the real Zetamac site may be logged as practice; they do not count, because the app cannot see them.

**`s0.script`: the script that runs.** A seeded task in `setup-checklist`, done on the learner's own machine:

1. Make a folder named `zq-exit-<word>` (the seed picks the word).
2. In it, write `<name>.py` with at least ten non-blank, non-comment lines that reads input, uses a function, a loop and an `if`, and prints the seeded expected output for the seeded inputs. Example: `split.py` takes a bill of £86.40, a 10% tip and 3 people, and prints `Each pays £31.68`.
3. Run it from the terminal and paste four things: the output of `pwd` (or `Get-Location` in PowerShell), of `ls` (or `dir`), the script's text, and the terminal transcript of `python3 split.py` (or `py split.py`) including `python3 --version`.

The checker confirms that the path ends in the seeded folder name, the listing contains the file, the script has at least ten qualifying lines and parses as Python (with `ast.parse` in the in-app Pyodide worker; on a device that cannot load Python, by a tokeniser check), the command in the transcript names that file, the printed output matches the seeded expectation, and the Python version is 3.12 or later. CI tests the parser against fixture transcripts from macOS zsh, Linux bash and Windows PowerShell. A pasted transcript could be invented; the learner is the only stakeholder (ASSESSMENT.md principle 6), so the check guards against honest mistakes, which are the common case: the wrong folder, an unsaved file, `split.py.txt`.

---

## 5. Reading and resource map per level

### 5.0 How to use this map

- **One primary resource per topic** (curriculum rule 1). For 0.3 the primary route is **Khan Academy Precalculus** (with its sibling courses for geometry, trigonometry and statistics); the UK route is **TLMaths** A-level videos with **Corbettmaths** for GCSE geometry and statistics; the one-book option is **Serge Lang, Basic Mathematics**. The learner picks one route at the start of 0.3; the other columns are optional. **OpenStax Precalculus 2e** is the problem bank for every route, because it is free, complete and has answers to odd-numbered exercises.
- **University resources** (MIT OpenCourseWare, Harvard Stat 110, Strang, 3Blue1Brown, Hammack's Book of Proof, Euclid in Joyce's edition) add the depth a top programme expects. They are listed where they teach this level's idea better than the primary route, or preview the Stage 1 item it feeds.
- **Problems over reading** (rule 2). Every entry says what to do. External time is budgeted at 18 hours of watching and reading and 29.5 hours of external problems for 0.3 (section 1.1). Each level's companion work (`Level.companion`, CONTENT-FORMAT.md 3.8) is **1.25 h for a level of 4 lessons, 1.625 h for 5 and 2.0 h for 6** (6, 16 and 7 levels: 47.5 h in all), about three-eighths watching and reading and five-eighths problems. A level's companion is the chosen route's row, the problem-bank row and at most one university row; rows marked stretch are optional and outside the budget.
- **[check]** marks a chapter, section, lecture or unit title recalled but not confirmed from this environment. Lang's chapter numbers and titles below were confirmed by search against the Springer reprint's contents (chapters 1 to 17 and the Interlude, On Logic and Mathematical Expressions) [searched]; section-level details inside a chapter are not checked.

**Links** (free unless stated). Khan Academy: https://www.khanacademy.org/math/precalculus, https://www.khanacademy.org/math/geometry, https://www.khanacademy.org/math/trigonometry, https://www.khanacademy.org/math/algebra2, https://www.khanacademy.org/math/statistics-probability. TLMaths: https://www.tlmaths.com. Corbettmaths: https://corbettmaths.com/contents/. OpenStax Precalculus 2e: https://openstax.org/details/books/precalculus-2e. OpenStax Calculus Volume 1: https://openstax.org/details/books/calculus-volume-1. Euclid's Elements, D. E. Joyce (Clark University): https://mathcs.clarku.edu/~djoyce/elements/elements.html. Book of Proof, Richard Hammack: https://www.people.vcu.edu/~rhammack/BookOfProof/ (the sibling file's search confirmed this page). MIT 6.042J Mathematics for Computer Science (Fall 2010 videos): https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/. MIT 18.06 Linear Algebra (Spring 2010): https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/. MIT RES.18-005 Highlights of Calculus: https://ocw.mit.edu/courses/res-18-005-highlights-of-calculus-spring-2010/. Harvard Stat 110 and the Blitzstein and Hwang book: https://stat110.hsites.harvard.edu (the course site has moved from projects.iq.harvard.edu; Strategic Practice sets 1 to 10 are at /strategic-practice-problems) [searched]. 3Blue1Brown: https://www.3blue1brown.com/topics/linear-algebra and https://www.3blue1brown.com/topics/calculus. OpenIntro Statistics: https://www.openintro.org/book/os/. Underground Mathematics (Cambridge): https://undergroundmathematics.org. NRICH: https://nrich.maths.org. STEP Support Programme (Cambridge): https://maths.org/step/ (also served at https://step.maths.org; 25 foundation modules) [searched]. Isaac Maths (Cambridge): https://isaacmaths.org [check]. A-level Mathematics past papers and mark schemes: each board's website (Pearson Edexcel, AQA, OCR). Paid books cited: Lang, Basic Mathematics; Strang, Introduction to Linear Algebra; Hull, Options, Futures, and Other Derivatives; Cormen, Leiserson, Rivest and Stein (CLRS); Graham, Knuth and Patashnik, Concrete Mathematics; Gelfand and Saul, Trigonometry; Needham, Visual Complex Analysis; Benjamin and Shermer, Secrets of Mental Math.

**Source ids and licences** (`content/sources.yaml`, CONTENT-FORMAT.md 3.2 and 9.4). Ids are `canon-gap.md` revision 2's where it has one; ids marked † are proposed here. Only CC BY works may be adapted (`problem-adapted`); every other source is cited and mirrored (`problem-inspired`), never copied.

| Resource | Id | Role (`Citation.use`) | Licence |
|---|---|---|---|
| Khan Academy Precalculus; its Geometry, Trigonometry, Algebra 2 and Statistics and Probability courses | `src.khan-precalc`; `src.khan-geometry` †, `src.khan-trig` †, `src.khan-algebra`, `src.khan-stats` † | `basis` (Khan route) | Cite only |
| TLMaths A-level Pure and Further Maths videos | `src.tlmaths` † | `basis` (UK route) | Cite only |
| Lang, *Basic Mathematics* | `src.lang-basic-math` | `basis` (one-book route) | Cite only |
| Corbettmaths videos, Textbook Exercises and 5-a-day | `src.corbettmaths` | `problem-inspired` | Cite only |
| OpenStax, *Precalculus 2e* | `src.openstax-precalc-2e` | `problem-adapted` | CC BY 4.0 [searched by canon-gap.md] |
| OpenStax, *Calculus Volume 1* | `src.openstax-calculus` | `parallel-reading` | CC BY-NC-SA 4.0: cite only |
| A-level Mathematics Pure papers; GCSE Higher papers | `src.alevel-papers`, `src.gcse-papers` | `problem-inspired`; the real GCSE paper is the `s0.gcse` confirm | The boards' terms: cite only |
| Euclid, *Elements*, D. E. Joyce's online edition | `src.euclid-joyce` † | `further` | Cite only |
| Hammack, *Book of Proof*, 3rd ed | `src.hammack-proof-3e` | `parallel-reading` | Free to read; cite only |
| MIT 6.042J, 18.06, RES.18-005 (OpenCourseWare) | `src.mit-6042j`, `src.mit-1806`, `src.mit-res18005` † | `parallel-reading` | CC BY-NC-SA: cite only |
| Harvard Stat 110; Blitzstein and Hwang | `src.stat110-2013`, `src.blitzstein-hwang-2019` | `parallel-reading`; Strategic Practice 1 `problem-inspired` | Cite only |
| Strang, *Introduction to Linear Algebra*, 6th ed | `src.strang-ila-6e` | `further` | Paid; cite only |
| 3Blue1Brown, Essence of Calculus; Essence of Linear Algebra | `src.3b1b-calculus`, `src.3b1b-linalg` † | `parallel-reading` | Cite only |
| Hull, *Options, Futures, and Other Derivatives*, 11th ed | `src.hull-ofod-11e` | `further` | Paid; cite only |
| CLRS, 4th ed; Tsay, *Analysis of Financial Time Series*, 3rd ed | `src.clrs-4e`, `src.tsay-afts-3e` | `further` | Paid; cite only |
| OpenIntro Statistics, 4th ed | `src.openintro-4e` | `parallel-reading` | Free; cite only [check licence] |
| Gelfand and Saul, *Trigonometry*; Gelfand, Glagoleva and Shnol, *Functions and Graphs* | `src.gelfand-trig`, `src.gelfand-functions` | `further` | Paid; cite only |
| Graham, Knuth and Patashnik, *Concrete Mathematics*, 2nd ed; Needham, *Visual Complex Analysis*; Patrick, *Introduction to Counting and Probability* (AoPS) | `src.concrete-math-2e` †, `src.needham-vca` †, `src.aops-intro-counting` † | `further` | Paid; cite only |
| Underground Mathematics; Isaac Maths; STEP Support Programme; NRICH | `src.underground-maths`, `src.isaac-maths`, `src.step-support`, `src.nrich` † | `further` | Free; cite only |
| Sweigart, *Automate the Boring Stuff with Python* | `src.sweigart-atbs` | `basis` (0.4) | Free online to read; cite only |
| The Missing Semester (MIT), 2026 and 2020 | `src.missing-semester-2026`, `src.missing-semester-2020` | `parallel-reading` | Cite only |
| Shotts, *The Linux Command Line*, 2nd ed | `src.shotts-tlcl` | `parallel-reading` | Free PDF from the author; cite only [check licence] |
| Harvard CS50P; CS50x | `src.cs50p`, `src.cs50x` | `parallel-reading` | Cite only |
| Python documentation; VS Code documentation; Microsoft and Apple shortcut pages | `src.python-docs` †, `src.vscode-docs` †, `src.ms-shortcuts` †, `src.apple-shortcuts` † | `parallel-reading` | Cite only |
| keybr.com; Zetamac | `src.keybr`, `src.zetamac` | practice tools | Not content |
| Benjamin and Shermer, *Secrets of Mental Math* | `src.benjamin-mental-math` | `further` (0.5) | Paid; cite only |

### 5.1 0.3 Precalculus

**Course S: Shape and Space**

| Level | Resource and section | What to do |
|---|---|---|
| S1 | Corbettmaths videos and Textbook Exercises: angles in parallel lines, angles in polygons, bearings [check titles] | Watch each; do the Textbook Exercise for each topic |
| S1 | Euclid, Elements, Book I, Propositions 29 (parallel lines) and 32 (angle sum and exterior angle), Joyce's edition | Read both proofs and compare with lesson 2's |
| S1 | Lang, Basic Mathematics, chapter 5 (Distance and Angles) | Read; attempt the exercises on angles |
| S2 | Corbettmaths: area of a trapezium, circles, sectors, volume and surface area of prisms, cylinders, cones, spheres and frustums, plans and elevations | Watch; do every Textbook Exercise; one Corbettmaths 5-a-day Higher sheet per week during S1 to S5 |
| S2 | Khan Academy High school geometry, unit Solid geometry [check] | Exercises to Proficient |
| S2 | Lang, chapter 7 (Area and Applications) | Read the circle sections; attempt the exercises |
| S3 | Euclid, Book I, Propositions 4, 8 and 26 (SAS, SSS, ASA and AAS) and 47 (Pythagoras), with Joyce's commentary | Read; note where Euclid's figure for I.47 differs from lesson 10's rearrangement |
| S3 | Khan Academy High school geometry, units Congruence and Similarity [check] | Exercises to Proficient; unit tests |
| S3 | Corbettmaths: Pythagoras, Pythagoras in 3D, congruent triangles, similar shapes (lengths, areas, volumes) | Textbook Exercises |
| S4 | Khan Academy High school geometry, units Performing transformations and Transformation properties and proofs [check] | Exercises to Proficient |
| S4 | Corbettmaths: reflections, rotations, translations, enlargements (fractional and negative), constructions, loci | Textbook Exercises |
| S4 | Lang, chapter 6 (Isometries) | Read; attempt the exercises |
| S5 | Euclid, Book III, Propositions 20, 21, 22, 31 and 32 (centre angle, same segment, cyclic quadrilateral, semicircle, alternate segment) [check numbering] | Read each proof; write one in your own words with reasons |
| S5 | Khan Academy High school geometry, unit Circles [check]; Corbettmaths circle theorems and circle theorem proofs [check titles] | Exercises; every proof question |
| S6 | Khan Academy Trigonometry, unit Right triangles and trigonometry [check] | Exercises to Proficient; unit test |
| S6 | OpenStax Precalculus 2e, section 5.4 (Right Triangle Trigonometry) | Read; odd-numbered section exercises |
| S6 | Corbettmaths: trigonometry, exact trigonometric values, 3D trigonometry, angles of elevation and depression | Textbook Exercises |
| S7 | Khan Academy Trigonometry, unit Non-right triangles and trigonometry [check] | Exercises to Proficient |
| S7 | OpenStax 2e, sections 8.1 and 8.2 (Law of Sines, Law of Cosines) | Odd-numbered exercises, including every ambiguous-case exercise |
| S7 | TLMaths A-level Pure Year 1, Trigonometry section (sine rule, cosine rule, area, ambiguous case) [check section letter] | Watch; do the linked exam questions |
| S8 | Khan Academy Precalculus, unit Vectors [check]; Corbettmaths vectors (GCSE proofs) | Exercises; every Corbettmaths proof question |
| S8 | OpenStax 2e, section 8.8 (Vectors) | Odd-numbered exercises |
| S8 | Strang, Introduction to Linear Algebra, 6th ed, sections 1.1 (Vectors and Linear Combinations) and 1.2 (Lengths and Angles from Dot Products) [check the 6th edition's titles] (stretch) | Read; attempt the section problems that do not use matrices |
| S8 | 3Blue1Brown, Essence of Linear Algebra, chapters 1 (Vectors) and 9 (Dot products and duality) [check chapter number] | Watch |
| S8 | TLMaths A-level Pure, Vectors section (2D in Year 1, 3D in Year 2) [check] | Watch; exam questions |

**Course G: Growth**

| Level | Resource and section | What to do |
|---|---|---|
| G1 | OpenStax 2e, sections 11.1 (Sequences and Their Notations), 11.2 (Arithmetic Sequences), 11.3 (Geometric Sequences) | Odd-numbered exercises |
| G1 | TLMaths A-level Pure Year 2, Sequences and Series section (recurrence relations; increasing, decreasing, periodic) [check] | Watch; exam questions |
| G1 | MIT 6.042J (Fall 2010), lecture 15 (Linear Recurrences) [searched: OCW calendar]; the course text Mathematics for Computer Science, the section on linear recurrences and the Fibonacci characteristic equation [check section] | Watch the first half, on Fibonacci; attempt two recitation problems on two-term recurrences |
| G1 | Concrete Mathematics, section 6.6 (Fibonacci Numbers) [check] (stretch) | Read the closed form and the identities; attempt two warm-ups |
| G2 | Khan Academy Algebra 2, unit Exponential models [check]; Khan Academy Finance and capital markets, unit Interest and debt (compound interest, $e$ and continuous compounding) [check] | Exercises; watch the continuous-compounding videos |
| G2 | OpenStax 2e, sections 4.1 (Exponential Functions) and 4.2 (Graphs of Exponential Functions) | Odd-numbered exercises |
| G2 | 3Blue1Brown, Essence of Calculus, chapter 5, "What's so special about Euler's number e?" [check title] | Watch after lesson 48 |
| G2 | MIT RES.18-005 Highlights of Calculus (Strang), "The Exponential Function" [check title; the series' other titles were confirmed by search] | Watch |
| G2 | Hull, Options, Futures, and Other Derivatives, chapter 4 (Interest Rates), the section on measuring interest rates and compounding frequency [check edition and section] | Read; reproduce its table of compounding frequencies in code |
| G3 | Khan Academy Algebra 2, unit Logarithms [check] | Exercises to Proficient; unit test |
| G3 | OpenStax 2e, sections 4.3 to 4.6 (logarithmic functions, graphs, properties, equations) | Odd-numbered exercises |
| G3 | TLMaths A-level Pure, Exponentials and Logarithms section [check] | Watch; exam questions |
| G3 | MIT RES.18-005, "Inverse Functions $f^{-1}(y)$ and the Logarithm $x = \ln y$" [searched] | Watch |
| G4 | OpenStax 2e, sections 4.7 (Exponential and Logarithmic Models) and 4.8 (Fitting Exponential Models to Data) | Odd-numbered exercises |
| G4 | TLMaths, Exponentials and Logarithms: using logarithms to reduce $y = ab^x$ and $y = ax^n$ to straight lines [check] | Watch; exam questions |
| G4 | MIT RES.18-005, "Growth Rate and Log Graphs" [searched] | Watch |
| G4 | CLRS, chapter 3 (Characterizing Running Times in the 4th edition; Growth of Functions in the 3rd), the subsection on standard notations and common functions [check] | Read the logarithm and exponential parts only |
| G4 | Tsay, Analysis of Financial Time Series, section 1.1 (asset returns: simple and log returns) [check] | Read; it is the 2.2 text, met early |
| G5 | Khan Academy Precalculus, unit Series [check] | Exercises to Proficient; unit test |
| G5 | OpenStax 2e, section 11.4 (Series and Their Notations, including annuities) | Odd-numbered exercises |
| G5 | MIT 6.042J (Fall 2010), lectures 12 (Sums) [check number] and 13 (Sums and Asymptotics) [searched: OCW calendar]; the course text Mathematics for Computer Science, chapter on sums, which opens with the value of an annuity [check chapter] | Watch; attempt the annuity and perpetuity problems |
| G5 | Concrete Mathematics, chapter 2 (Sums), sections 2.1 to 2.3 (stretch) | Read; attempt the warm-ups |
| G5 | Lang, chapter 16 (Induction and Summations), the geometric series section | Read; exercises |

**Course T: Circles, Waves and Rotations**

| Level | Resource and section | What to do |
|---|---|---|
| T1 | Khan Academy Trigonometry, unit Trigonometric functions (radians, the unit circle) [check] | Exercises to Proficient |
| T1 | OpenStax 2e, sections 5.1 (Angles), 5.2 (Unit Circle), 5.3 (The Other Trigonometric Functions) | Odd-numbered exercises |
| T1 | TLMaths A-level Pure Year 2, Trigonometry: radians, arc length, sector area [check] | Watch; exam questions |
| T1 | Lang, chapter 11 (Trigonometry), sections on radian measure and on sine and cosine | Read; exercises |
| T2 | OpenStax 2e, sections 6.1 and 6.2 (graphs of the trigonometric functions) and 7.6 (Modeling with Trigonometric Functions) | Odd-numbered exercises, including every modelling exercise in 7.6 |
| T2 | Khan Academy Precalculus or Trigonometry, sinusoidal models [check] | Exercises |
| T3 | Khan Academy Trigonometry, unit Trigonometric equations and identities [check] | Exercises to Proficient |
| T3 | OpenStax 2e, sections 6.3 (Inverse Trigonometric Functions), 7.1 (Solving Trigonometric Equations with Identities) and 7.5 (Solving Trigonometric Equations) | Odd-numbered exercises |
| T3 | TLMaths A-level Pure Year 2, Trigonometry: sec, cosec, cot, identities, solving equations [check] | Watch; exam questions |
| T4 | OpenStax 2e, sections 7.2 (Sum and Difference Identities) and 7.3 (Double-Angle, Half-Angle, and Reduction Formulas) | Odd-numbered exercises |
| T4 | TLMaths A-level Pure Year 2, Trigonometry: compound angles, $R\sin(x + \alpha)$, small-angle approximations [check] | Watch; exam questions |
| T4 | Gelfand and Saul, Trigonometry, the chapter on addition formulas [check chapter] (stretch) | Read; attempt its problems |
| T5 | Khan Academy Precalculus, unit Matrices [check] | Exercises to Proficient; unit test |
| T5 | 3Blue1Brown, Essence of Linear Algebra, chapters 3 to 7 (linear transformations, composition, 3D, determinant, inverses) | Watch before lessons 89 to 92 |
| T5 | MIT 18.06 (Spring 2010), lectures 1 (The geometry of linear equations) and 3 (Multiplication and inverse matrices) [check numbers] | Watch: a first look at the 1.4 course |
| T5 | OpenStax 2e, sections 9.5 (Matrices and Matrix Operations), 9.7 (Solving Systems with Inverses) and 9.8 (Cramer's Rule) | Odd-numbered exercises on $2 \times 2$ matrices |
| T5 | Lang, chapters 14 (Mappings) and 17 (Determinants) | Read the $2 \times 2$ parts; exercises |
| T6 | Khan Academy Precalculus, unit Complex numbers [check] | Exercises to Proficient; unit test |
| T6 | OpenStax 2e, section 8.5 (Polar Form of Complex Numbers) | Odd-numbered exercises |
| T6 | TLMaths A-level Further Maths, Core Pure: complex numbers (loci in the Argand diagram, modulus-argument form, De Moivre, roots of unity) [check] | Watch; Further Maths Core Pure exam questions on loci and roots |
| T6 | Lang, chapter 15 (Complex Numbers) | Read; exercises |
| T6 | 3Blue1Brown, "e to the pi i, in 3.14 minutes, using dynamics" [check title] | Watch after lesson 97 |
| T6 | Needham, Visual Complex Analysis, chapter 1 (stretch) | Read the geometry of multiplication |

**Course C: Counting, Chance and Data**

| Level | Resource and section | What to do |
|---|---|---|
| C1 | Khan Academy Statistics and probability, unit Counting, permutations, and combinations [check] | Exercises to Proficient |
| C1 | OpenStax 2e, section 11.5 (Counting Principles) | Odd-numbered exercises |
| C1 | Harvard Stat 110, lecture 1 (Probability and Counting); Blitzstein and Hwang, Introduction to Probability, chapter 1, the sections on how to count [check section numbers] | Watch; read; attempt the chapter 1 counting exercises with solutions available on the book site |
| C1 | MIT 6.042J (Fall 2010), lecture 16 (Counting Rules I) [searched: OCW calendar]; the course text's chapter on cardinality rules [check] | Watch; attempt the recitation problems |
| C2 | MIT 6.042J (Fall 2010), lecture 17 (Counting Rules II: pigeonhole, inclusion-exclusion) [check] | Watch; recitation problems |
| C2 | Hammack, Book of Proof, chapter 3 (Counting), the inclusion-exclusion section | Odd-numbered exercises (solutions in the book) |
| C2 | Harvard Stat 110, lecture 3 (Birthday Problem, Properties of Probability), whose inclusion-exclusion treatment reaches the matching problem [check] | Watch; Strategic Practice 1 |
| C2 | Art of Problem Solving, Introduction to Counting and Probability (Patrick), the chapters on overcounting and on the pigeonhole principle [check] (stretch) | Attempt the chapter's challenge problems |
| C3 | OpenStax 2e, section 11.6 (Binomial Theorem) | Odd-numbered exercises |
| C3 | TLMaths A-level Pure, Binomial expansion (natural $n$ in Year 1; rational $n$ and validity in Year 2) [check] | Watch; exam questions |
| C3 | Harvard Stat 110, lecture 2 (Story Proofs, Axioms of Probability); Blitzstein and Hwang, chapter 1, story proofs [check section] | Watch; reproduce two story proofs |
| C3 | Concrete Mathematics, chapter 5 (Binomial Coefficients), section 5.1 (stretch) | Read; attempt the warm-ups |
| C4 | Khan Academy Statistics and probability, unit Probability [check] | Exercises to Proficient |
| C4 | Corbettmaths: Venn diagrams, tree diagrams, conditional probability, relative frequency | Textbook Exercises |
| C4 | OpenStax 2e, section 11.7 (Probability) | Odd-numbered exercises |
| C4 | Harvard Stat 110, lecture 4 (Conditional Probability) [check] | Watch: the bridge to 1.5 |
| C5 | Khan Academy Statistics and probability, units on displaying, comparing and summarising quantitative data, bivariate data and study design [check unit titles] | Exercises to Proficient |
| C5 | Corbettmaths: averages from frequency tables, cumulative frequency, box plots, histograms, scatter graphs, sampling, capture-recapture | Textbook Exercises |
| C5 | OpenIntro Statistics, sections 1.3 (sampling principles and strategies) and 2.1 (examining numerical data) [check] | Read; odd-numbered exercises |

**Course R: Proof, Limits and Curves**

| Level | Resource and section | What to do |
|---|---|---|
| R1 | Hammack, Book of Proof, chapters 2 (Logic), 4 (Direct Proof), 5 (Contrapositive Proof), 6 (Proof by Contradiction) and 9 (Disproof) | Read; odd-numbered exercises (solutions in the book) |
| R1 | MIT 6.042J (Fall 2010), lecture 1 (Introduction and Proofs); the course text's chapters on proofs and logical formulas [check] | Watch; recitation problems |
| R1 | TLMaths A-level Pure, Proof section (deduction, exhaustion, counterexample; contradiction in Year 2) [check] | Watch; exam questions |
| R1 | Lang, Interlude, "On Logic and Mathematical Expressions" (between chapters 4 and 5) [searched] | Read |
| R2 | Hammack, chapter 10 (Mathematical Induction) | Odd-numbered exercises |
| R2 | MIT 6.042J (Fall 2010), lectures 2 (Induction) and 3 (Strong Induction) | Watch; recitation problems |
| R2 | Lang, chapter 16 (Induction and Summations) | Exercises |
| R3 | Khan Academy Precalculus, unit Rational functions [check] | Exercises to Proficient |
| R3 | OpenStax 2e, sections 3.7 (Rational Functions) and 9.4 (Partial Fractions) | Odd-numbered exercises |
| R3 | TLMaths A-level Pure Year 2, Algebra and Functions: partial fractions [check] | Watch; exam questions |
| R4 | Khan Academy Precalculus, unit Conic sections [check] | Exercises to Proficient; unit test |
| R4 | OpenStax 2e, sections 10.1 (The Ellipse), 10.2 (The Hyperbola), 10.3 (The Parabola), 8.6 and 8.7 (Parametric Equations) | Odd-numbered exercises |
| R4 | TLMaths A-level Pure Year 2, Coordinate Geometry: parametric equations [check] | Watch; exam questions |
| R4 | Lang, chapter 12 (Some Analytic Geometry) | Read the conic sections; exercises |
| R5 | Khan Academy Precalculus, unit Limits and continuity [check] | Exercises to Proficient; unit test |
| R5 | OpenStax Calculus Volume 1, sections 2.1 to 2.4 (A Preview of Calculus; The Limit of a Function; The Limit Laws; Continuity) | Read; odd-numbered exercises. This is the 1.3 text, met early |
| R5 | 3Blue1Brown, Essence of Calculus, chapter 7 (limits) [check]; MIT RES.18-005, "Limits and Continuous Functions" [searched] | Watch |

**Problems and stretch for every course.** A-level Pure past-paper questions on the level's topic (from the boards' papers, sorted by topic on TLMaths) are the problem row for the UK route, timed at about 1.2 minutes per mark, the papers' own rate. For learners finishing homework early: Underground Mathematics, Isaac Maths and NRICH problems tagged with the level's topic, one a week, and from course G onwards the STEP Support Programme's foundation modules, which need only A-level Pure and come with hints and solutions. They train the unfamiliar, multi-step problem solving that admissions tests for top UK mathematics courses (MAT, STEP) reward [our judgement]. Stretch work is outside the hours budget and counts as logged outside work (ASSESSMENT.md 11).

### 5.2 0.4 Computer basics

| Level | Resource and section | What to do |
|---|---|---|
| K1, K2 | keybr.com (https://www.keybr.com) | Practise there or in `typing-trainer`; log sessions, which count towards practice hours |
| K2 | Microsoft support, "Keyboard shortcuts in Windows"; Apple support, "Mac keyboard shortcuts" | Read the editing sections for your operating system; make your own one-page list |
| B1 | Automate the Boring Stuff (2nd edition, free online at https://automatetheboringstuff.com), chapter 9, the opening section on files and file paths | Read only that section now; the Python in it comes in 1.1 |
| B1 | The Linux Command Line (Shotts, free at https://linuxcommand.org/tlcl.php), chapter 2 (Navigation) [check] | Read; absolute and relative pathnames |
| B2 | MIT, The Missing Semester (2026 edition), lecture 1, "Course Overview + Introduction to the Shell" (https://missing.csail.mit.edu/2026/course-shell/) [searched]; the 2020 lecture 1, "Course overview + the shell" (https://missing.csail.mit.edu/2020/course-shell/), is the fallback | Watch one of the two; do its exercises on your own machine (Windows learners: those needing a Unix shell wait for 1.2, which installs WSL2) |
| B2 | The Linux Command Line, chapters 1 to 4 and 6 (the shell, navigation, exploring the system, manipulating files, redirection) [check] | Read; type every command |
| B3 | Automate the Boring Stuff, Introduction, "Downloading and Installing Python" | Follow it on your machine |
| B3 | Python documentation, "Using Python on Windows" and "Using Python on macOS" (https://docs.python.org/3/using/) | Read the installation and PATH parts for your system |
| B3 | VS Code documentation, "Getting Started with Python in VS Code" (https://code.visualstudio.com/docs/python/python-tutorial) | Follow it end to end |
| Y1 | Automate the Boring Stuff, chapters 1 (Python Basics) and 2 (Flow Control) | Type every example; answer the practice questions at each chapter's end. The 3rd edition (May 2025 [searched by canon-gap.md]) reorganised its early chapters: 1 Python Basics, 2 if-else and Flow Control, 3 Loops, 4 Functions, which cover what the 2nd edition's chapters 1 to 3 do [searched: automatetheboringstuff.com/3e]; the free 2nd edition is the reference here (open item 8) |
| Y1 | Harvard CS50P (https://cs50.harvard.edu/python/), lectures 0 (Functions, Variables) and 1 (Conditionals) | Watch; problem set 0 is optional |
| Y1 | Python tutorial, section 3, "An Informal Introduction to Python" (https://docs.python.org/3/tutorial/) | Read; try every example at the prompt |
| Y2 | Automate the Boring Stuff, chapter 3 (Functions) | Type every example; practice questions; the Collatz practice project |
| Y2 | CS50P, lectures 2 (Loops) and 3 (Exceptions) | Watch |
| Y2 | Python tutorial, section 4 (More Control Flow Tools), up to and including defining functions [check subsection numbers] | Read |

### 5.3 0.5 Mental arithmetic

| Level | Resource and section | What to do |
|---|---|---|
| A1 to A4 | Zetamac, https://arithmetic.zetamac.com, default settings | Ten logged runs across the four weeks, as a check that the in-app format matches the real site |
| A1, A3 | Benjamin and Shermer, Secrets of Mental Math, chapters 2 ("Products of a Misspent Youth: Basic Multiplication") and 3 ("New and Improved Products: Intermediate Multiplication") [searched]; the squaring sections [check which chapter] | Read; attempt the chapter exercises in your head |
| A2 | Secrets of Mental Math, chapter 1 ("A Little Give and Take: Mental Addition and Subtraction") [searched] | Read; exercises |
| A4 | Secrets of Mental Math, chapter 4 ("Divide and Conquer: Mental Division") [searched]; its fraction and decimal sections [check]; chapter 5 ("Good Enough: The Art of 'Guesstimation'") is the optional companion to lesson 16 | Read; exercises |

---

## 6. Verification approach

Every auto-marked item has two independent implementations of its answer (CONTENT-FORMAT.md 6.2): the TypeScript generator that builds the item and a Python verifier written from the generator's plain-language `semantics`, without reading the TypeScript, run in CI under `tools/zqverify` (pinned SymPy, NumPy, mpmath). CI also replays every listed distractor through the runtime grader and requires it to be marked wrong with its intended diagnosis. The table says, for each family of items in this file, how the answer is computed in CI and how the learner's answer is checked at runtime.

| Family | Items | CI: second implementation | Runtime check | Traps the check must catch |
|---|---|---|---|---|
| Angle facts, polygons, bearings | S1 | Exact rational arithmetic on degrees; polygon generators assert $\frac{360}{n}$ is whole for regular polygons | `numeric` exact; bearings normalised to $[0, 360)$ and shown with three figures | A generated diagram must agree with its numbers: the construction graph (widgets-stage0.md decision 5) is evaluated and every labelled angle compared with the stated value to $10^{-9}$ |
| Lengths, areas, volumes | S2, S3, S7 | SymPy exact forms ($\pi$, surds) and NumPy float evaluation, compared to $10^{-12}$ | `expression` (equivalence by canonical form plus 8-point numeric probing) when an exact form is asked; `numeric` with a 3-significant-figure tolerance otherwise | Required forms ("in terms of $\pi$", "simplest surd") are structural tests separate from equivalence |
| Congruence, similarity, transformations | S3, S4 | Coordinates under SymPy rational arithmetic; transformations applied as exact affine maps | `point` exact on lattice points; `choice` for criteria; transformation descriptions as structured fields (type, centre, angle, direction, vector, factor) | A rotation described without its centre is incomplete, not wrong: the structured fields make "missing" checkable |
| Circle theorems and geometric proofs | S5, S8 proofs, R1 | Model-answer lines checked by SymPy where algebraic; the authored reason list checked against the theorem catalogue | `ordering` with `before` pairs for proof steps (any valid order passes) and reason cards by `mapping`; long-form by rubric | Distractor reasons that are true statements but do not justify the step |
| Trigonometric values and identities | S6, T1, T3, T4 | SymPy `simplify(lhs - rhs) == 0` plus probing at 8 random points that avoid singularities; SymPy `singularities` lists where an identity fails | `expression` equivalence for values; identity proofs by `derivation-steps` step checks (each line equivalent to the last on the stated domain) | A "proof" that cancels a factor that can be 0 must fail the domain check |
| Trigonometric equations in a range | T3, T4, S7 (ambiguous case) | SymPy `solveset` on the interval, cross-checked by a dense sign-change scan in mpmath at 50 digits; the count of solutions must agree | `set` of numbers with tolerance $10^{-3}$, order-free; missing and extra solutions diagnosed separately | The calculator's single principal value; a range doubled for $2x$ but not shifted |
| Exponentials and logarithms | G2, G3, G4 | SymPy `solve` with domain filtering; every rejected root (such as $e^x = -1$) asserted to fail substitution; floats by mpmath | `numeric` with relative tolerance $10^{-4}$, or `expression` for exact forms such as $\frac{\ln 6}{\ln 1.5}$ | The `int(math.log(1000, 10)) == 2` trap in drills; logs of non-positive numbers |
| Sequences, recurrences and series | G1, G5, R2, R3 | Exact `Fraction` partial sums compared with SymPy `summation` closed forms for $n = 1$ to 200; recurrence closed forms (first-order by the fixed-point shift, two-term by the characteristic equation) checked against the recurrence iterated in exact integers or SymPy surds for $n = 0$ to 200, with SymPy `rsolve` as a third check; sequence limits and the tolerance index $N$ by SymPy `limit` and exact search; sums to infinity by SymPy `limit`, asserted only when $\lvert r \rvert < 1$ | `expression` for nth terms and closed forms (equivalence on integer $n \ge 0$, with the item's index origin stated); `numeric` exact rationals for sums | An off-by-one nth term passes at one $n$ and fails at others, so probing uses at least five integer points; an index-origin slip ($u_0$ against $u_1$) is a diagnosed misconception, not a generic wrong answer |
| Finance (present value, annuities, loans) | G2, G5, Precalc Lab part 1 | Closed form in Python `Fraction` or `Decimal`, and an independent month-by-month amortisation whose final balance must be within £0.005 of 0 | `numeric` to the penny or to 3 significant figures as the item states; rates in basis points to 0.1 | Discounting the first payment when it is paid today; mixing monthly and annual rates |
| Vectors and matrices | S8, T5 | SymPy `Matrix` exact rational operations; eigenvectors in T5's d5 item by `eigenvects`; NumPy cross-check for float items | `matrix` exact by default; `expression` per component for column vectors; `angle` items numeric | Rows against columns in a transformation matrix; $BA$ against $AB$ |
| Complex numbers | T6 | SymPy exact roots (`roots`, `polar`), `cmath` floats; root sets compared as multisets to $10^{-9}$; loci as SymPy sets: a drawn locus is sampled at 64 points, each tested against the locus equation, and region answers compared as sets of grid cells | `point` on the Argand plane with tolerance; `expression` for $a + bi$ and $re^{i\theta}$ forms; argument checked in $(-\pi, \pi]$ | The principal argument out of range; a missing root |
| Counting | C1, C2, C3 | **Exact enumeration** with `itertools` for every generated instance small enough (up to $10^6$ objects), compared with the formula; for larger instances, the formula against SymPy `binomial`, `factorial`, `subfactorial` and a recurrence | `numeric` exact integer | The ordered-against-unordered mismatch; inclusion-exclusion sign errors; a formula correct only for distinct objects |
| Probability | C4, C2 (derangements) | Exact enumeration of the sample space with `Fraction`; a seeded simulation of $10^6$ trials as a third, sanity-only check that must land within 4 standard errors | `numeric` with exact fractions accepted, decimals to $10^{-4}$, and the $[0, 1]$ nudge | $P(A \mid B)$ against $P(B \mid A)$; "at least one" against "the first" |
| Binomial expansion and series | C3 | SymPy `expand` and `coeff`; `series` for rational powers with the validity interval from the singularity | `numeric` for coefficients; `expression` for truncated series; `interval` for validity | Coefficients not raised to the power; the factor taken out before the expansion |
| Statistics | C5 | Python `statistics` and exact `Fraction` frequencies; every quartile item declares its convention (GCSE $\frac{n+1}{4}$ interpolation, or cumulative-frequency reading at $\frac{n}{4}$), and CI computes it both ways so that items where conventions disagree by more than the tolerance say which one they use | `numeric` with a tolerance matched to graph reading (half a small square) for graph items, exact for table items | Plotting at midpoints instead of class boundaries; bar height as frequency |
| Rational functions, conics, limits | R3, R4, R5 | SymPy `apart` for partial fractions; `limit` with `dir='+'` and `dir='-'`; conic classification by completing the square in SymPy and by the sign pattern of the quadratic coefficients | `expression` for decompositions and standard forms; `numeric` for limits, with "does not exist" and $\pm\infty$ as answer options | A hole reported as an asymptote; one-sided limits that disagree |
| Long-form items | every set and the exams | CI checks the model answer's algebraic lines with SymPy (each line equivalent to the last under the stated assumptions) and that each rubric point names model lines that exist (CONTENT-FORMAT.md 6.8) | Self-marking against the rubric with Bertie's suggested mark and evidence quote beside it (AI-TUTOR.md 2.7); the learner's mark counts | Rubric points that no line of the model answer evidences |
| Code drills | every set, Precalc Lab | `zqtest` suites run against `reference.py` on CPython 3.12 and on Pyodide 314.0.7's CPython 3.14 (ARCHITECTURE.md decision 15); CI checks that each drill's declared `needs` covers its imports; every `wrong/*.py` must fail the test it names | Visible examples on Run; hidden tests at submission; the first failing test mapped to a diagnosis | Float formatting (`f"{x:.2f}"` on half-pennies); `math.log` rounding; infinite loops (per-test time limits) |
| Shell and file tasks | B1, B2, 0.4 rehearsal | The reference command sequence and every known-wrong sequence replayed in the `shell-sim` engine; the web CI also replays them in a real `bash` container to confirm that the simulator's semantics match for every command taught | Graded by effect: predicates on the final virtual file system (paths exist, contents equal after trimming whitespace, working folder), never by keystrokes | `mv downloads/*` moving a file that should stay; `wc -l` padding on macOS |
| Paste-verify | B3, `s0.script` | Parser tests on fixture transcripts from macOS zsh, Linux bash and Windows PowerShell, including deliberate faults (wrong folder, `.py.txt`, Python 3.9) | Structured checks listed in section 4.4 | A transcript from the Python prompt instead of the shell |
| Typing | K1, K2 | Unit tests of the speed and accuracy functions on recorded keystroke logs with known answers | Speed = correct characters $\div 5 \div$ minutes; accuracy = correct keystrokes $\div$ all keystrokes, backspaces included | Pasted text (the trainer blocks paste and flags keystroke timings faster than 20 ms apart) |
| Mental arithmetic | A1 to A4, `s0.zetamac` | Generators checked against the Zetamac defaults by a chi-square test on 100,000 seeded operand draws; every division asserted whole; answers exact integers or decimals with stated places | Exact match, auto-advance on a correct answer; times from `performance.now()` per item | Leading zeros, a trailing decimal point, and a minus sign typed as an en dash on some keyboards are normalised before comparison |

**What verification cannot prove** (CONTENT-FORMAT.md 6.13): that a hook is engaging, that a trap catches the misconception it targets, or that a long-form rubric rewards understanding rather than vocabulary. Those are checked by the owner's review of each level before release and by item statistics after it: a trap screen that fewer than 30% of learners fall into, or a distractor nobody picks, is flagged for rewriting.

---

## 7. Sample lesson in full: "Logarithms count multiplications"

**Why this lesson.** Decision 16: the logarithm is the concept the rest of the path leans on most (log returns in 1.1 and 1.7, log-likelihood in 1.6, $O(\log n)$ in 1.8, log scales in every chart), and the one most often learnt as a button on a calculator. This lesson defines it as a count before any notation appears, and every later G3 lesson (the graph, the laws, change of base, equations) is a consequence of that count.

### 7.1 Lesson header

| Field | Value |
|---|---|
| Id | `lsn.growth.log-as-count` (course G, level G3, lesson 49 of 0.3) |
| Length | 11 screens (1 title, 1 summary, 9 tasks) and a quiz of 5 one-mark items; `est: { minutes: 15 }`, about 12 minutes of screens and 3 of quiz |
| Requires | 0.1 lessons 32 to 34 (index laws) and 0.2 lesson 97 (exponential graphs), with skill ids as `stage0-number-algebra.md` names them; 0.3 lessons 44 (what $b^x$ means between whole numbers) and 45 (rates over different periods) |
| Introduces | `skl.pre.log-definition`, `skl.pre.log-noninteger`, `skl.pre.log-domain`, `skl.pre.log-product-law` |
| Terms | `gls.pre.logarithm`, `gls.pre.log-base`; embargoed for Bertie until screen 4 (CONTENT-FORMAT.md 3.10) |
| Frame (`frame.why`) | "An exponent answers one question: what do $n$ multiplications by $b$ give? Real questions often run the other way: how many doublings, how many halvings, how many years of growth. Without a name for that count, every such question needs trial and error." |
| Before (`frame.before`) | "So far you have computed powers: $2^{10}$, $1.05^{12}$, $10^{-3}$. Today the power is the unknown." |
| Insight (the aha line) | A logarithm is a count of multiplications, and counts add when numbers multiply |
| Misconceptions | `mc.pre.log-value-not-count`, `mc.pre.log-off-by-one`, `mc.pre.log-as-division`, `mc.pre.log-base-as-answer`, `mc.pre.log-wrong-base`, `mc.pre.log-linear-between`, `mc.pre.log-shrink-positive`, `mc.pre.log-of-zero-infinite`, `mc.pre.inverse-as-reciprocal`, `mc.pre.log-product-multiplies` |
| Edge cases (`edgeCases`) | $\log_b 1 = 0$ for every base (at `edges`); no count reaches 0 or a negative number, so $\log_b x$ needs $x > 0$ (at `edges`); base 1 never moves, so it cannot be a base (at `summary`) |
| Worked example with a decision point (`workedExample`) | At `between`. Naive: interpolate in a straight line between 64 and 128 and answer 6.56. Decision: a partial tile multiplies rather than adds, so the count must be read where the chain's value reaches 100, which gives 6.64 |
| Trap | `shrink`: $\log_{10} 0.001$, bait 3 |
| Transfer | `binary-search`: binary search over a million names |
| Sources | `src.khan-precalc`, unit on logarithms [check], `parallel-reading`; `src.openstax-precalc-2e`, sec. 4.3 (Logarithmic Functions), `problem-adapted`; `src.tlmaths`, Exponentials and Logarithms [check], `parallel-reading`; `src.mit-res18005`, "Inverse Functions $f^{-1}(y)$ and the Logarithm $x = \ln y$" [searched], `further` |
| Art | `ast.course-art.growth-chain` (a row of ×2 tiles climbing a log axis); course art, not Bertie, who appears only in his own slots (BERTIE.md 7) |
| Lesson-wide tutor guidance | Avoid "logarithm" and "log" before screen 4 (the embargo); do not mention calculator log keys, which arrive in lesson 52; never state a count on a screen before the learner's first Check there |

**The widget.** Every screen but 8 uses `multiplier-chain` in **tile mode**, a configuration this lesson asks the Stage 0 catalogue to add (section 7.5): a start value; a palette of tile types (×2, ×3, ×10, ÷2, ÷10); a chain the learner builds by tapping or dragging tiles from the palette, where each tile multiplies the running value; the running value printed under each tile and plotted on a logarithmic axis, so equal tiles take equal steps; an optional target line; a maximum chain length; an optional partial tile whose exponent is set with a slider; a "Glue" action that joins two chains; and a halving mode with a rounded-up readout. Its element ids, in CONTENT-FORMAT.md 3.5's `kind:name` form, are `row:tiles`, `tile:<k>`, `value:<k>`, `value:last`, `palette:<tile>`, `target:line`, `slider:partial`, `joint:glue` and `axis:log`. On every screen the widget's content id is `chain`, so a hint points at `chain/row:tiles`.

### 7.2 Screens

---

**Screen 1. Title** (`title`, id `title`)

- **Prose:** "An exponent tells you what you get after so many multiplications. Today we ask the question backwards."
- **Art:** `ast.course-art.growth-chain`.

---

**Screen 2. The hook** (`problem`, id `hook`; opens as free manipulation, and the question appears once the learner has placed a first tile: `continueWhen: chain.tiles >= 1`)

- **Prose:** "Fold a sheet of paper in half and it has 2 layers. Fold it again and it has 4."
- **Widget:** `multiplier-chain`, tile mode. Start value 1, labelled "layers". Palette: one tile type, "×2", labelled "fold", unlimited. Target line at 1,024, labelled "1,024 layers". The running value appears under each tile; the number of tiles is not shown, so the learner has to count them. At most 15 tiles; a chain that passes the target shows its last value in amber, and the last tile can be removed.
- **Question:** "How many folds give 1,024 layers?"
- **Answer input:** `numeric-input`, whole number, unit "folds".
- **Correct:** 10. **Reason** (verdict chip): "Ten ×2 tiles take 1 to 1,024."

| Wrong answer | Misconception | Feedback line |
|---|---|---|
| 512 | `mc.pre.log-value-not-count` | "512 is a number of layers, the value one fold before the end. The question asks how many folds." |
| 11 | `mc.pre.log-off-by-one` | "Your chain shows 11 numbers, from 1 to 1,024, but the folds are the tiles between them. Count the tiles." |
| 9 | slip | "After 9 folds the chain shows 512. One more fold is needed." |
| `otherwise` | | "Count the ×2 tiles in your chain: each one is a fold." |

- **Hints.** Nudge: "Each fold is one ×2 tile. Are you counting tiles or reading values?" Point: "The tiles are the folds; the numbers under them are layers", highlighting `chain/row:tiles` and `chain/value:last`. Step: "After 1 fold: 2 layers. After 2 folds: 4. After 3 folds: 8. Keep going until the chain reaches 1,024, and count the tiles."
- **Why?** (`rep: count`) Yours: "You multiplied by 2 ten times: $2^{10} = 1{,}024$." Shown: "Ten multiplications by 2 take 1 to 1,024: $2^{10} = 1{,}024$." Then: "The answer is the number of multiplications, not a value on the chain. That count gets a name in two screens."
- **Solution line:** "1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1,024: ten ×2 tiles."
- **Tutor.** Focus: "Count the multiplications, not the values they produce." Notes: "A learner who types 512 has read the last value before the target; ask what the question counts. A learner who types 11 has counted numbers, not gaps between them." Reps: `count`, `picture`. Avoid: "logarithm", "log".

---

**Screen 3. A different tile** (`ladder`, id `tens`; widget `from: hook/chain`)

- **Constraint:** "Same chain, new tile: each one multiplies by 10."
- **Widget:** the screen 2 chain with the palette changed to "×10", the unit label removed and the target line at 1,000,000.
- **Question:** "How many ×10 tiles take 1 to 1,000,000?"
- **Answer input:** `numeric-input`, whole number.
- **Correct:** 6. **Reason:** "Each ×10 tile adds one zero, and 1,000,000 has six."

| Wrong answer | Misconception | Feedback line |
|---|---|---|
| 7 | `mc.pre.log-off-by-one` | "1,000,000 has 7 digits, but the count is the number of zeros: each ×10 adds one zero to 1." |
| 100,000 | `mc.pre.log-value-not-count` | "That is the value before the last tile. We are counting tiles." |
| 5 | slip | "$10^5 = 100{,}000$: one tile short." |
| `otherwise` | | "Watch what each ×10 tile does to the number, and count the tiles." |

- **Hints.** Nudge: "What does one ×10 tile do to the number of zeros?" Point: "Watch the zeros grow", highlighting `chain/value:last`. Step: "1 to 10 to 100 takes two tiles and makes two zeros. How many zeros does 1,000,000 have?"
- **Why?** (`rep: count`) Yours: "Each ×10 adds one zero, and 1,000,000 has six, so six tiles: $10^6 = 1{,}000{,}000$." Then: "Counting zeros works only for ×10 tiles. Counting tiles works for every tile."
- **Solution line:** "$10^6 = 1{,}000{,}000$: six ×10 tiles."
- **Tutor.** Focus: "The same count, with a different tile." Notes: "Learners who count digits answer one too many; ask how many digits 1 itself has." Reps: `count`, `picture`. Avoid: "logarithm", "log".

---

**Screen 4. The name** (`generalise`, id `name`)

- **Prose:** "You have been answering one question: how many multiplications by $b$ take 1 to $x$? That count is the **logarithm of $x$ to base $b$**, written $\log_b x$."
- **Rule** (`rule`, `tex`): $\log_b x = n$ exactly when $b^n = x$. Examples beside it: $\log_2 1{,}024 = 10$ because $2^{10} = 1{,}024$; $\log_{10} 1{,}000{,}000 = 6$ because $10^6 = 1{,}000{,}000$. The rule describes what the learner did on screens 2 and 3; the examples are their own answers.
- **Widget:** `multiplier-chain` with "×3" tiles and no target line. Concreteness is fading: the learner may use the chain or not.
- **Question:** "What is $\log_3 81$?"
- **Answer input:** `numeric-input`.
- **Correct:** 4. **Reason:** "Four ×3 tiles reach 81."

| Wrong answer | Misconception | Feedback line |
|---|---|---|
| 27 | `mc.pre.log-as-division` | "27 is $81 \div 3$, one division. $\log_3 81$ counts how many ×3 tiles reach 81." |
| 3 | `mc.pre.log-base-as-answer` | "3 is the base, the size of each tile. The answer is how many tiles." |
| 5 | `mc.pre.log-off-by-one` | "1, 3, 9, 27, 81 is five numbers but four tiles." |
| 9 | slip | "Two ×3 tiles reach 9. Keep going to 81." |
| `otherwise` | | "Build the chain with ×3 tiles and count them." |

- **Hints.** Nudge: "How many ×3 tiles reach 81?" Point: "This is the only tile you need", highlighting `chain/palette:x3`. Step: "3, then 9, then 27. One more tile?"
- **Why?** (`rep: algebra`) Yours: "$3 \times 3 \times 3 \times 3 = 81$: four multiplications by 3, so $\log_3 81 = 4$." Then: "The definition is a sentence about counting. A calculator key comes later, and only computes this count."
- **Solution line:** "$3^4 = 81$, so $\log_3 81 = 4$."
- **Tutor.** Focus: "The name for the count: $\log_b x$ is how many ×$b$ tiles take 1 to $x$." Notes: "Learners who divide once, or answer with the base, have not yet tied the symbol to the tiles; send them back to the chain." Reps: `count`, `algebra`.

---

**Screen 5. Between the tiles** (`ladder`, id `between`, two parts; the lesson's worked example with a decision point)

- **Constraint:** "Not every target lands on a tile."
- **Widget:** `multiplier-chain` with "×2" tiles and the target line at 100. Six tiles read 64; seven read 128 (amber, past the target). Part (b) unlocks a **partial tile**: a final tile "×$2^t$" whose exponent $t$ is set by a `slider` from 0 to 1 in steps of 0.01. The readout shows the running value, rounded to the nearest whole number, and the total count $6 + t$.
- **Part (a) question:** "$\log_2 100$ lies between which two whole numbers?" (`choice`)

| Option | Correct? | Misconception | Feedback line |
|---|---|---|---|
| 6 and 7 | yes | | "Six tiles reach 64 and seven reach 128, so 100 needs a count between." |
| 50 and 51 | no | `mc.pre.log-as-division` | "50 is $100 \div 2$, one division. Count tiles: six reach 64 and seven reach 128." |
| 1 and 2 | no | `mc.pre.log-wrong-base` | "That counts ×10 tiles: $\log_{10} 100 = 2$. ×2 tiles are smaller, so you need more of them." |
| 9 and 10 | no | slip | "$2^9 = 512$ is already past 100." |

- **Part (b) question:** "Drag the partial tile until the chain reaches 100. What is $\log_2 100$, to 2 decimal places?" (`numeric-input`)
- **Correct:** 6.64, accepted from 6.62 to 6.66 (the readout shows 100 for $t = 0.64$ and $t = 0.65$; the true value is $6.6439$). **Reason:** "A partial tile of $\times 2^{0.64} \approx 1.56$ takes 64 to 100."

| Wrong answer | Misconception | Feedback line |
|---|---|---|
| 6.5 | `mc.pre.log-linear-between` | "Half a ×2 tile multiplies by $\sqrt{2} \approx 1.41$, which takes 64 to about 90.5, not 100." |
| 6.56 | `mc.pre.log-linear-between` | "6.56 is where 100 would sit if the values from 64 to 128 were evenly spaced. A partial tile multiplies, so they are not: drag until the value reads 100." |
| `otherwise` | | "Drag the slider until the running value reads 100, then read the count." |

- **Hints.** Nudge: "Does the partial tile add to 64 or multiply it?" Point: "The slider sets the partial tile; watch the value, not the slider's position", highlighting `chain/slider:partial` and `chain/value:last`. Step: "At $t = 0.5$ the chain reads about 90.5. You need a little more."
- **Why?** (`rep: picture`) Yours: "The partial tile $\times 2^{0.64} \approx 1.56$ takes 64 to 100, so $\log_2 100 \approx 6.64$." Then: "Most logarithms are not whole numbers, and the count still means something: 6.64 doublings take 1 to 100."
- **Solution line:** "$2^6 = 64$ and $2^{0.64} \approx 1.558$, so $2^{6.64} \approx 99.7$, which the readout rounds to 100."
- **Tutor.** Focus: "A count can be a fraction of a tile, and a partial tile still multiplies." Notes: "Learners who interpolate in a straight line have the right instinct and the wrong model; ask what one partial tile does to 64." Reps: `picture`, `count`, `algebra`.

The decision point is part (b): the straight-line estimate between 64 and 128 is the method that served on every linear scale so far, and the log axis shows why it fails. Equal tiles are equal steps on that axis, and 100 sits 64% of the way along the step from 64 to 128, not the 56% that spacing the values evenly gives, because a partial tile multiplies.

---

**Screen 6. Shrinking** (`trap`, id `shrink`, `trap: { mc: mc.pre.log-shrink-positive, bait: 3 }`)

- **Prose:** "Now tiles can shrink as well. A ÷10 tile undoes a ×10 tile."
- **Widget:** `multiplier-chain` with "×10" and "÷10" tiles and the target line at 0.001; the logarithmic axis keeps the small target visible.
- **Question:** "What is $\log_{10} 0.001$?"
- **Answer input:** `numeric-input`; the keypad shows the minus key.
- **Correct:** $-3$. **Reason:** "Three ÷10 tiles, each counting $-1$."

| Wrong answer | Misconception | Feedback line |
|---|---|---|
| 3 (the bait) | `mc.pre.log-shrink-positive` | "Three tiles, yes, but they were ÷10 tiles. Check: $10^3 = 1{,}000$, not 0.001. A tile that undoes a ×10 counts as $-1$." |
| 0.001 | `mc.pre.log-value-not-count` | "That is the target. The logarithm is the count of tiles." |
| $-2$ | slip | "0.001 has two zeros after the point, but it takes three ÷10 tiles: 1, 0.1, 0.01, 0.001." |
| 0 | slip | "Zero tiles leave you at 1." |
| `otherwise` | | "Build the chain with ÷10 tiles, and remember each one counts as $-1$." |

- **Hints.** Nudge: "Is $10^3$ equal to 0.001? Which power of 10 is?" Point: "These tiles shrink the value", highlighting `chain/palette:div10`. Step: "$10^{-1} = 0.1$ and $10^{-2} = 0.01$. Continue the pattern."
- **Why?** (`rep: algebra`) Shown: "$10^{-3} = \frac{1}{1{,}000} = 0.001$, so $\log_{10} 0.001 = -3$." Then: "With a base above 1, every number between 0 and 1 has a negative logarithm: you must shrink to reach it."
- **Solution line:** "1, 0.1, 0.01, 0.001: three ÷10 tiles, a count of $-3$."
- **On reveal:** the lesson player plays Bertie's `surprised` one-shot (BERTIE.md 5.3). A revealed trap screen does not enter the Redo queue (ASSESSMENT.md 2.2).
- **Tutor.** Focus: "Shrinking counts as negative." Notes: "Most learners answer 3; the screen exists to be failed once. After the miss, ask what $10^3$ is." Reps: `algebra`, `count`. Avoid: "negative exponent" before the first Check.

---

**Screen 7. Two edges** (`ladder`, id `edges`, two parts)

- **Constraint:** "Two edge cases."
- **Part (a) question:** "What is $\log_7 1$?" (`numeric-input`, with a ×7 chain available.) **Correct:** 0. **Reason:** "No tiles at all leave the chain at 1."

| Wrong answer | Misconception | Feedback line |
|---|---|---|
| 1 | `mc.pre.log-value-not-count` | "1 is where the chain starts. How many tiles do you need to stay there?" |
| 7 | slip | "One ×7 tile reaches 7, not 1." |
| `otherwise` | | "How many tiles does the chain need to stay where it starts?" |

- **Part (b) widget:** the chain with ÷10 tiles and a target line at 0. Each tile shrinks the value tenfold (0.1, 0.01, and on to $10^{-12}$); the chain never touches the line.
- **Part (b) question:** "How many tiles take 1 to 0?" (`choice`)

| Option | Correct? | Misconception | Feedback line |
|---|---|---|---|
| No count works | yes | | "Every tile keeps the value positive, so 0 is out of reach." |
| 0 tiles | no | slip | "Zero tiles leave you at 1." |
| Infinitely many ÷10 tiles | no | `mc.pre.log-of-zero-infinite` | "The chain gets as close to 0 as you like, but no number of tiles reaches it, and 'infinitely many' is not a count. So $\log_{10} 0$ is undefined." |
| $-10$ tiles | no | slip | "$10^{-10} = 0.0000000001$: tiny, but not 0." |

- **Hints.** Nudge: "Can multiplying a positive number by 10 or by 0.1 ever give exactly 0?" Point: "Look at the gap that never closes", highlighting `chain/value:last` and `chain/target:line`. Step: "Every tile keeps the value positive, so 0, and every negative number, are out of reach."
- **Why?** (`rep: picture`) Yours: "Multiplying a positive number by positive factors never reaches 0 or a negative number, so $\log_b x$ exists only for $x > 0$, and $\log_b 1 = 0$ for every base." Then: "In Python, `math.log(0)` raises a `ValueError` for exactly this reason."
- **Solution line:** "(a) $7^0 = 1$, so $\log_7 1 = 0$. (b) No power of 10 is 0, so $\log_{10} 0$ is undefined."
- **Tutor.** Focus: "Zero tiles is a count; reaching zero is impossible." Notes: "'Infinitely many' is the instinct of a learner who has met limits informally; agree that the chain approaches 0, and ask whether any finite chain lands on it." Reps: `picture`, `algebra`.

---

**Screen 8. Swapping input and output** (`problem`, id `inverse`; opens in explore mode until the swap toggle has been used once)

- **Prose:** "Each count gives a point: (count, value) on the exponential, and (value, count) on the logarithm."
- **Widget:** `graph-explorer` (content id `plot`) showing $y = 2^x$ with a draggable point that displays its coordinates. A "Swap" toggle reflects the point and the whole curve in the dashed line $y = x$, drawing $y = \log_2 x$. Element ids: `curve:exp`, `curve:log`, `line:y-eq-x`, `point:p`, `control:swap`.
- **Question:** "$(5, 32)$ lies on $y = 2^x$. Which point must lie on $y = \log_2 x$?" (`choice`)
- **Reason** (for the correct option): "The logarithm takes the value 32 and returns the count 5."

| Option | Correct? | Misconception | Feedback line |
|---|---|---|---|
| $(32, 5)$ | yes | | "$\log_2 32 = 5$: the input is the value, the output is the count." |
| $(5, 32)$ | no | slip | "That point is on $y = 2^x$. The logarithm takes 32 and returns the count, 5." |
| $(\frac{1}{32}, 5)$ | no | `mc.pre.inverse-as-reciprocal` | "$\frac{1}{32}$ is a reciprocal. An inverse function undoes; it does not turn a number upside down." |
| $(5, \frac{1}{32})$ | no | `mc.pre.inverse-as-reciprocal` | "$\frac{1}{32} = 2^{-5}$ is on $y = 2^{-x}$, the reflection in the $y$-axis, not in $y = x$." |

- **Hints.** Nudge: "On the log graph, the input is a value and the output is a count. Which number here is the count?" Point: "Reflect the point in this line", highlighting `plot/line:y-eq-x` and `plot/point:p`. Step: "$\log_2 32$ asks how many ×2 tiles reach 32."
- **Why?** (`rep: picture`) Yours: "$\log_2 32 = 5$ because $2^5 = 32$. Undoing the exponential swaps input and output, which reflects its graph in $y = x$." Then: "Lesson 50 studies this graph; its domain is $x > 0$, the edge from the last screen."
- **Solution line:** "Swap the coordinates: $(32, 5)$."
- **Tutor.** Focus: "The logarithm undoes the exponential, so their graphs are mirror images in $y = x$." Notes: "0.2 lesson 92 taught inverses as swapped pairs; learners who pick a reciprocal are reading $^{-1}$ as a power." Reps: `picture`, `algebra`.

---

**Screen 9. Why logarithms were invented** (`derive`, id `product-law`, two parts)

- **Leap** (`leap`). Naive: multiply the numbers directly. Fails: multiplying $7.31 \times 2.84$ by hand, or a thousand probabilities in a model, is slow and error-prone, and in a computer the product of a thousand small probabilities underflows to 0 (lesson 59). Points to: if every number came with its count, adding counts would replace multiplying numbers.
- **Prose:** "In 1614 John Napier published tables built on one observation. Find it."
- **Widget:** `multiplier-chain` in split view. Chain A has three ×2 tiles and reaches 8; chain B has five ×2 tiles and reaches 32. A "Glue" action appends chain B's tiles to the end of chain A.
- **Part (a) question:** "Glue chain B onto chain A. How many tiles does the result have, and what value does it reach?" Two `numeric-input` fields. **Correct:** 8 tiles; value 256. **Reason:** "Gluing adds the tile counts and multiplies the values."

| Wrong answer | Misconception | Feedback line |
|---|---|---|
| 15 tiles | `mc.pre.log-product-multiplies` | "Gluing puts the tiles end to end: $3 + 5$, not $3 \times 5$." |
| value 40 | slip | "$8 + 32$ adds the values. The glued chain carries on multiplying from 8, so it reaches $8 \times 32$." |
| `otherwise` | | "Count the glued chain's tiles, then read its last value." |

- **Part (b):** `derivation-steps` (content id `d`) in fill mode.
  1. Let $\log_b x = m$ and $\log_b y = n$, so $b^m = x$ and $b^n = y$. (definition)
  2. $xy = b^m \cdot b^n = $ **[slot A]** (index law)
  3. So $\log_b(xy) = $ **[slot B]** $= \log_b x + \log_b y$. (definition again)
- **Correct:** slot A $b^{m+n}$; slot B $m + n$. **Reason:** "The product's count is the sum of the counts."

| Wrong answer | Misconception | Feedback line |
|---|---|---|
| Slot A $b^{mn}$ | `mc.pre.log-product-multiplies` | "Multiplying powers of one base adds the exponents: $2^3 \cdot 2^5 = 2^8$, the 8 tiles you just counted." |
| Slot B $mn$ | `mc.pre.log-product-multiplies` | "The glued chain had $3 + 5$ tiles. Counts add." |
| `otherwise` | | "Write $b^m \cdot b^n$ as one power of $b$, using the index law from 0.1." |

- **Hints.** Nudge: "When you glue two chains, do the tile counts add or multiply?" Point: "Count across the joint", highlighting `chain/joint:glue` and `d/line:2`. Step: "Write $2^3 \times 2^5$ as a row of 2s and count them."
- **Why?** (`rep: picture`) Yours: "Gluing two chains adds their tile counts, and the glued chain reaches the product of their values. That is the product law: counts add when numbers multiply." Then: "It is why products of probabilities become sums of log-probabilities in every model you will fit (lesson 59, then 1.6)."
- **Solution line:** "$b^m \cdot b^n = b^{m+n}$, so $\log_b(xy) = m + n = \log_b x + \log_b y$."
- **Tutor.** Focus: "Why logarithms turn multiplying into adding." Notes: "The leap is the point of the screen: if a learner asks why anyone would want this, the slide rule in lesson 51 and the underflow in lesson 59 are the two answers." Reps: `picture`, `algebra`, `analogy`.

---

**Screen 10. Transfer: binary search** (`problem`, id `binary-search`)

- **Prose:** "A sorted list holds 1,000,000 names. Each check of the middle name rules out half of what is left."
- **Widget:** `multiplier-chain` in halving mode: start 1,000,000, "÷2" tiles, a readout of "names still possible" rounded up, and a target line at 1.
- **Question:** "At most how many checks until only one name is left?"
- **Answer input:** `numeric-input`. **Correct:** 20. **Reason:** "$2^{20} = 1{,}048{,}576$ is the first power of 2 past a million."

| Wrong answer | Misconception | Feedback line |
|---|---|---|
| 19 | slip | "$2^{19} = 524{,}288$, less than 1,000,000. After 19 halvings up to 2 names can remain." |
| 500,000 | `mc.pre.log-value-not-count` | "That is what one check leaves. We are counting checks." |
| 6 | `mc.pre.log-wrong-base` | "6 is $\log_{10} 1{,}000{,}000$: right idea, wrong tile. Each check halves, so the tiles are ÷2." |
| 1,000,000 | linear search (slip) | "That checks every name in turn. Halving is far faster." |
| `otherwise` | | "Count the ÷2 tiles until the readout shows 1." |

- **Hints.** Nudge: "Which power of 2 is just above 1,000,000?" Point: "Use the readout, which rounds up", highlighting `chain/value:last`. Step: "$2^{10} = 1{,}024 \approx 10^3$, so $(2^{10})^2 \approx (10^3)^2 = 10^6$."
- **Why?** (`rep: count`) Yours: "$\log_2 1{,}000{,}000 \approx 19.93$, so 20 halvings always leave one name." Then: "A list a thousand times longer needs only about 10 more checks. That is why $O(\log n)$ algorithms scale (1.8)."
- **Solution line:** "$2^{19} < 10^6 < 2^{20}$, so 20 checks."
- **Tutor.** Focus: "A logarithm counts halvings as well as doublings." Notes: "Learners who answer 19 have found the power just below a million; ask what the readout shows after 19 checks." Reps: `count`, `code`.

---

**Screen 11. Summary** (`summary`, id `summary`)

- **Ideas** (exactly three).
  1. $\log_b x$ counts the multiplications by $b$ that take 1 to $x$: $\log_b x = n$ exactly when $b^n = x$.
  2. Counts can be zero ($x = 1$), negative ($0 < x < 1$, for $b > 1$) or fractional. No count reaches $x \le 0$, so the logarithm is undefined there.
  3. Counts add when numbers multiply: $\log_b(xy) = \log_b x + \log_b y$.
- **Card** (`crd.pre.log-definition`, saved to the Notebook). $\log_b x = n \iff b^n = x$; defined for $x > 0$, with base $b > 0$ and $b \ne 1$ (×1 tiles never move); $\log_b 1 = 0$; $\log_b b = 1$; $\log_b(xy) = \log_b x + \log_b y$.
- **Trap.** "$\log_{10} 0.001$ is $-3$, not 3: shrinking counts as negative."

### 7.3 Lesson quiz (5 items, 1 mark each, difficulty 2 to 3, one attempt each, no hints, Why? after each)

| # | Item | Type | Difficulty | Correct | Diagnosed wrong answers | Why? |
|---|---|---|---|---|---|---|
| Q1 | $\log_5 125$ | N | 2 | 3 | 25 (`mc.pre.log-as-division`: $125 \div 5$); 4 (`mc.pre.log-off-by-one`); 5 (`mc.pre.log-base-as-answer`) | "$5 \times 5 \times 5 = 125$: three ×5 tiles." |
| Q2 | $\log_2 \frac{1}{8}$ | N | 2 | $-3$ | 3 (`mc.pre.log-shrink-positive`); 0.125 (`mc.pre.log-value-not-count`) | "$2^{-3} = \frac{1}{8}$: three ÷2 tiles, each counting $-1$." |
| Q3 | $\log_{10} 50$ lies between | C | 3 | 1 and 2 | 0 and 1 ("$10^1 = 10$ is below 50, so the count is above 1"); 5 and 6 (`mc.pre.log-as-division`: $50 \div 10 = 5$); 2 and 3 (`mc.pre.log-off-by-one`: "50 has two digits, but one ×10 tile reaches 10 and two reach 100, so the count is between 1 and 2") | "$10^1 = 10$ and $10^2 = 100$, and 50 lies between them." |
| Q4 | Which are undefined? $\log_2 0$; $\log_3(-9)$; $\log_{10} 1$; $\log_5 \frac{1}{25}$ | M | 3 | $\log_2 0$ and $\log_3(-9)$ | Selecting $\log_{10} 1$ ("zero tiles: $\log_{10} 1 = 0$, a good count"); selecting $\log_5 \frac{1}{25}$ ("two ÷5 tiles: $-2$") | "No chain of positive factors reaches 0 or a negative number." |
| Q5 | Given $\log_2 3 \approx 1.585$, find $\log_2 12$ (accepted $3.585 \pm 0.001$) | N | 3 | 3.585 | 3.17 (`mc.pre.log-product-multiplies`: "$\log_2 3 \times \log_2 4 = 1.585 \times 2$ multiplies the counts; counts add"); 6.34 ("$4 \times 1.585$ is $4\log_2 3 = \log_2 81$: the 4 is a factor of 12, not a power of 3"); 19.02 ($12 \times 1.585$); 4.585 ("that is $\log_2 24$: $12 = 3 \times 4$, and $\log_2 4 = 2$") | "$12 = 3 \times 4$, so $\log_2 12 = \log_2 3 + \log_2 4 = 1.585 + 2 = 3.585$." |

Single and multiple choice: 2 of 5 items (40%, at the ceiling). The quiz creates the FSRS cards for `skl.pre.log-definition` and its siblings (ASSESSMENT.md 5.3). Mastered needs 75% of the marks on the first completion (ASSESSMENT.md decision 26), which on five one-mark items means 4 of 5; any wrong item joins the Redo queue as a fresh generated variant at the same level (`gen.pre.log-integer`, `gen.pre.log-between`, `gen.pre.log-product`).

### 7.4 Verification for this lesson

| Value on the screens | Check in CI |
|---|---|
| $2^{10} = 1{,}024$; $10^6$; $3^4 = 81$; $2^3 \cdot 2^5 = 2^8 = 256$; $10^{-3} = 0.001$; $7^0 = 1$ | Exact integer and `Fraction` arithmetic in `zqverify` |
| $\log_2 100 = 6.6439$; $2^{0.64} = 1.5583$; $64 \times 2^{0.64} = 99.73$ and $64 \times 2^{0.65} = 100.43$, both shown as 100; the accepted band 6.62 to 6.66 | mpmath at 30 digits; CI asserts that every slider value whose rounded readout is 100 lies inside the accepted band, and that 6.5 and 6.56 lie outside it |
| The straight-line estimate $6 + \frac{36}{64} = 6.5625$; $64\sqrt{2} = 90.51$ | `Fraction` and mpmath |
| $2^{19} = 524{,}288$, $2^{20} = 1{,}048{,}576$, $\log_2 10^6 = 19.93$, and $\lceil 10^6 / 2^{19} \rceil = 2$ names left after 19 checks | Exact integers; a simulated halving with ceiling division |
| Q5: $\log_2 12 = 3.58496$; distractors $1.585 \times 2 = 3.17$, $4 \times 1.585 = 6.34$, $12 \times 1.585 = 19.02$, $\log_2 24 = 4.58496$ | mpmath; grader replay requires each distractor to be marked wrong with its named diagnosis (CONTENT-FORMAT.md 6.6) |
| No tutor field holds an accepted value (10, 6, 4, 6.64, $-3$, 0, $(32, 5)$, 8 and 256, 20, the slot answers) | The compiler's tutor leak lint (CONTENT-FORMAT.md 3.10) |
| Every element reference (`chain/row:tiles`, `chain/slider:partial`, `plot/line:y-eq-x`, `d/line:2` and the rest) | Resolved against each widget's `targets(config)` (CONTENT-FORMAT.md 12.1), which needs the tile-mode ids of section 7.5 |

### 7.5 What this lesson asks of the widget library

| To | Request | Why |
|---|---|---|
| `widgets-stage0.md` 5.9, `multiplier-chain` | A **tile mode**: integer and partial tiles from a palette (×$b$ and ÷$b$), a logarithmic value axis, a target line, a maximum length, a partial tile driven by a slider, a split view with a Glue action, and a halving mode with a rounded-up readout; `targets()` ids `row:tiles`, `tile:<k>`, `value:<k>`, `value:last`, `palette:<tile>`, `target:line`, `slider:partial`, `joint:glue`, `axis:log`; a `chain-length` predicate with a Python twin | The catalogue's percentage mode has none of these; lessons 40, 49 to 51 and 57 use them |
| `widgets-stage0.md` 6.6, `graph-explorer` | A reflect-in-$y = x$ toggle with the ids `control:swap`, `line:y-eq-x`, `curve:<name>` and `point:<name>` | Screen 8 here; lessons 50 and 81 reuse it |

---

## Verification log (6 October 2026, source and correctness pass)

Every answer in the section 3 example problems, the section 4 exam and exit tables, the section 7 sample lesson, and the numeric hooks, traps and edges of section 2 was recomputed with Python 3.11 and SymPy 1.14 (exact fractions, brute-force enumeration, symbolic limits). Hours were re-summed: 0.3 is 200.0, 0.4 is 40.0 and 0.5 is 20.0, matching `curriculum.md`; the 47.5 companion hours, the 80-mark exam slot table (32 + 48, difficulty 16/40/16/8, format 80) and the 80-mark GCSE-style table (strands 12/24/16/16/12) all re-total. Every item of the curriculum's Cover lists for 0.3, 0.4 and 0.5, and every exit line, is taught by a named level; no gap was found. Fifteen web searches checked citations.

**Corrected.**

| Where | Was | Now |
|---|---|---|
| Lesson 11 hook | "fit flat" in the box, whose answer is no | "fit inside", with both diagonals (1.166 m, 1.204 m) |
| Lesson 13 trap | A garbled additive-reasoning sentence | The additive answer stated: 15.4 m instead of 12 m |
| Lesson 43 hook | "within 0.001", which at $n = 4{,}998$ is exactly 0.001 | "less than 0.001", so $n = 4{,}999$ is right |
| Lesson 131 edge | "the first true one", but $n = 1$ is true | The base case is $n = 5$, where the unbroken run begins |
| A4 lesson 14 trap | Decimal places counted as for a product gave "0.4" | They give 0.004 |
| G5 example B | £343,798 and £143,798 from $300 \times 1{,}145.99$ | £343,797 and £143,797 (£143,798.18 unrounded) |
| R2 example B | "no earlier base case exists", but $n = 1$ is true | The step fails at $m = 1, 2$, so no base below 5 starts a chain |
| Precalc Lab part 3 | Kepler fit "about 1.499" | 1.498 on the fact sheet's rounded values, 1.499 on precise ones |
| Sample lesson, screen 5 note | Argued from "more than half", which the straight-line estimate also gives | 64% of the log step against the straight line's 56% |
| Sample quiz Q3 | Distractor "25 and 26" tagged `log-as-division` for $50 \div 2$, not division by the base | "2 and 3", `log-off-by-one` (digit counting, screen 3's slip) |
| Sample quiz Q5 | 6.34 tagged `log-product-multiplies`, but multiplying the counts gives $1.585 \times 2 = 3.17$ | 3.17 carries that tag; 6.34 has its own line ($4\log_2 3 = \log_2 81$); section 7.4 lists 3.17 |

**Confirmed by search and re-tagged.** Python 3.15.0 final moved to 9 October 2026 after rc3 on 2 October (decision 11). Zetamac's addition, multiplication and 120-second defaults (secondary sources; the site was blocked, so subtraction and division stay [check]). GCSE Higher AO weights 40/30/30 and OCR J560/05, 100 marks in 90 minutes (open item 4 closed). Khan Precalculus topics, including trigonometry, so the trigonometry slots of `s0.precalc` stand; rational functions stay [check]. MIT 6.042J (Fall 2010) lectures 13, 15 and 16. RES.18-005 titles for the logarithm, log graphs and limits videos. Lang's chapter list and Interlude. The Stat 110 site's new address (stat110.hsites.harvard.edu). The 2026 Missing Semester lecture 1 title and address. Automate the Boring Stuff 3rd edition chapters 1 to 4. STEP Support Programme address. Secrets of Mental Math chapters 1 to 4.

**Still [check].** Khan's challenge question count and calculator rule; Zetamac subtraction and division; 6.042J lectures 12 and 17; RES.18-005 "The Exponential Function"; Euclid Book III numbering; Isaac Maths address; TLMaths section letters; Khan unit titles in section 5.1; 3Blue1Brown chapter numbers; Strang 6th edition titles; OpenIntro and Shotts licences; whether the ATBS 3rd edition is free online; the grade that 80% buys on a real Higher paper. Nothing invented was found, so nothing was deleted.
