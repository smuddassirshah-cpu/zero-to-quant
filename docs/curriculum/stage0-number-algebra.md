# Stage 0 detailed curriculum: 0.1 Number and 0.2 Algebra

Blueprint work file, Stage 2 Phase 1. Draft 2, 6 October 2026.

**Source of truth.** `docs/curriculum.md` for stages, topics, hours and exit tests. This file expands items 0.1 (60 h) and 0.2 (180 h) into courses, levels, lessons, homework, exams and reading.

**Built on.** `docs/design-research.md` sections 5, 8 and 9 (lesson anatomy, curriculum architecture, teaching style); `docs/blueprint/work/widgets-stage0.md` (widget catalogue and generator families); `docs/CONTENT-FORMAT.md` revision 2 (ids, schema, screen types, checks, verification); `docs/ASSESSMENT.md` draft 2 (assessment ladder, homework, papers, exit parts, earned hours); `docs/AI-TUTOR.md` draft 2 (Bertie's availability and tutor fields); `docs/ARCHITECTURE.md` (Python runtime); `docs/blueprint/work/canon-gap.md` section 6 (source ids); the sibling file `docs/curriculum/stage0-precalc-computing.md` (0.3 to 0.5 and the Stage 0 exit papers); `spikes/README.md`; the owner's lesson-creator, maths-teaching, code-craft and project-forge skills.

**Draft 2** keeps every lesson number, id, level code and section number of draft 1, because `stage0-precalc-computing.md`, `ASSESSMENT.md` and `CONTENT-FORMAT.md` cite them. Section 0 lists what changed and why.

**Tags.** [our choice] marks a design decision without outside evidence. [check] marks a resource detail (a chapter number, a unit title, a lecture number) that I recall but could not confirm from this environment; confirm it before the content cites it (`checked: false` in `Level.companion` until then). [searched] marks a detail confirmed by a web search on 6 October 2026. khanacademy.org and corbettmaths.com were blocked by this environment's network proxy, so every Khan unit title and Corbettmaths topic name below is [check] unless marked otherwise.

**Answers.** Every numeric and symbolic answer in sections 2, 3 and 7 (lesson hooks, traps and edge cases with a value, all 54 example homework problems, the sample lesson) was recomputed on 6 October 2026 with Python 3.11, `fractions` and SymPy 1.14: exact arithmetic, `solve`, `factor`, `div`, `solve_univariate_inequality`, brute-force enumeration for the digit puzzle and the cash-machine screen, and float runs for the floating-point claims. A second verification pass on the same day (section 9) found one false float claim, one muddled trap and two consistency slips, now fixed. The script is a scratch check, not repository code: `zqverify` replaces it at build stage (CONTENT-FORMAT.md section 6).

**At a glance.**

| Item | Hours | Courses | Levels | Lessons | Lesson hours | Homework sets | Topic exam |
|---|---|---|---|---|---|---|---|
| 0.1 Number | 60 | 2 | 8 | 42 | 10.5 (17.5%) | 8 | 75 min, 22 items, 60 marks |
| 0.2 Algebra | 180 | 4 | 19 | 111 | 27.75 (15.4%) | 19 | 90 min, 25 items, 80 marks |
| Total | 240 | 6 | 27 | 153 | 38.25 | 27 | 2 |

---

## 0. What draft 2 changed, and why

| # | Change | Sections | Source |
|---|---|---|---|
| 1 | **Python runs on Pyodide on both targets.** Draft 1 wrote every drill for MicroPython in the Artifact. The owner dropped MicroPython after the iPhone spike; every drill here is standard library only (`needs: []`), so it runs wherever Python loads, and a device that cannot load Pyodide hands the item to the web app with a result code | 1.0 decision 12, 3.0, 3.3, 6 | `ARCHITECTURE.md` decision 15; `ASSESSMENT.md` decision 30; `spikes/README.md` (Python ready at 2.8 s on the owner's iPhone) |
| 2 | **A conflict with the brief, resolved by measurement.** The brief says Pyodide cannot run in the Artifact and that WebAssembly there was unmeasured. The spike measured both on the owner's iPhone: every probe passed except service workers, and a repackaged Pyodide loaded NumPy and pandas. This file follows the measurement, as the sibling papers do. Nothing in 0.1 or 0.2 depends on the answer, because no drill needs a package | 3.0 | `spikes/README.md`; `CONTENT-FORMAT.md` 0.3 |
| 3 | **Mastered at 75%.** Quiz items carry 1 mark each, so a four-item quiz is Mastered at 3 of 4. Draft 1's sample quiz had a 2-mark sort and an 80% bar | 2.0, 7.3 | `ASSESSMENT.md` decision 26 |
| 4 | **Widget names follow the reconciliation** that `CONTENT-FORMAT.md` section 1 adopted: `choice`, `numeric-input`, `expression-input`, `derivation-steps`, `code-cell`, `value-table`, `region-select`, `drag-point`, `sketch-pad`. Composite ids are unchanged | 2 | `CONTENT-FORMAT.md` 1; `widgets-stage0.md` 15.1 |
| 5 | **Three widgets are no longer used** (`stat-chart` in lesson 47, `matrix-grid` in lesson 53, `payoff-builder` in lesson 93) and **four move to an earlier wave**: `counting-slots` to W1; `scatter-fit`, `dot-plot-stats` and `complex-plane` to W2. Depth-first content reaches them before 0.3 does | 1.0 decision 16, 8 | `widgets-stage0.md` 13 (waves); `widgets-finance-games.md` (`payoff-builder` is P1) |
| 6 | **GCSE geometry and statistics live in 0.3** (course S and level C5), as the sibling file decided, pending the owner. Section 4.3 now maps every 0.1 and 0.2 question of the in-app `gcse` paper to its lessons, which closes the sibling's open item 1 | 1.0, 2.3, 4.3 | `stage0-precalc-computing.md` decision 2, 4.4, open item 1 |
| 7 | **The hours budget maps onto estimate units.** CI requires each topic's estimates to sum to within 10% of its curriculum hours. Each block now names the unit that carries its estimate; the sums are 56.75 of 60 h (94.6%) and 169.5 of 180 h (94.2%). This needs two small schema rules, requested in section 8 | 1.1, 1.2, 5, 8 | `ASSESSMENT.md` 8.7; `CONTENT-FORMAT.md` 3.8, 6.7 |
| 8 | **Reading map carries hours and source ids.** Every row has the hours that become its `Level.companion` entry, and every resource has a `src.*` id (canon-gap.md's where they exist) and a licence, because only CC BY sources may be adapted | 5 | `CONTENT-FORMAT.md` 3.2 (`Companion`), 9.4; `canon-gap.md` 6 |
| 9 | **Resource corrections**: Book of Proof's URL (the VCU page, not GitHub); Street-Fighting Mathematics is MIT OCW 18.098, January IAP 2008; The Art of Insight is MIT OCW RES.6-011; Lockdown Math episode 1 is "The simpler quadratic formula"; Welch Labs' series has 13 parts; the MAT page is `maths.ox.ac.uk/r/mat`; recent UKMT papers are free and older ones are sold; Khan's rational functions sit in Precalculus, not Algebra 2 | 5 | Web searches, 6 October 2026 [searched] |
| 10 | **Sample lesson rewritten to the revision 2 schema**: element references in `widget/kind:name` form, a `tutor` block (`focus`, `notes`, `reps`, `avoid`) on every task screen with no accepted value in it, `why.rep`, the Show solution text, hints that open after the lesson's first Check, Bertie's `surprised` one-shot on the trap reveal | 7 | `CONTENT-FORMAT.md` 3.5, 3.7, 3.10, decision 17; `AI-TUTOR.md` 2.2; `BERTIE.md` 5.3 |
| 11 | **Topic exit parts** `0.1.exit` and `0.2.exit`, because the schema's `Topic.exit` needs at least one: the topic exam at 70%, with the paper-review time as `estHours` | 4.3 | `CONTENT-FORMAT.md` 3.2 (`Topic`) |
| 12 | **Fixes**: lesson 38's trap was written as the correct fact; lesson 76's floating-point edge now names data that fails ($10^9 + 0.1$, $10^9 + 0.2$, $10^9 + 0.3$ give $-1024$); a boundary table with 0.3 and a "considered and left out" list are added | 2.1, 2.2, 2.3 | Second reading; float runs |

---

## 1. Item overview

### 1.0 Scope, boundaries and decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Unit of lesson time | **15 minutes per lesson, quiz included** (about 12 minutes of screens and 3 of quiz) | 10 minutes; screens only | Design research 5.8 sets 10 to 15 minutes of screens; the quiz is part of the sitting. Counting the upper end keeps the hours budget honest. The sibling file uses the same unit |
| 2 | Courses for 0.1 | **Two courses of 21 lessons**: How Numbers Work, then Proportion, Powers and Precision | One course per cover-list word (8 courses of 3 to 6 lessons) | Design research 8.2 sets 20 to 45 lessons per course; eight tiny courses would fragment the course map and the level reviews |
| 3 | Courses for 0.2 | **Four courses** (34, 20, 33 and 24 lessons): Expressions and Equations; Lines and Linear Systems; Quadratics and Polynomials; Functions and Graphs | Five courses; the curriculum's seven cover words as courses | Four is the schema's ceiling per topic (`CONTENT-FORMAT.md` 3.1: 1 to 4 courses) and matches the dependency chain: manipulation, then lines, then quadratics, then functions |
| 4 | Order | **Depth-first in curriculum order** (owner's decision): 0.1 courses W then P; 0.2 courses E, L, Q, F | Interleaving number and algebra | The owner chose depth-first. Spacing still happens: level reviews draw up to 30% of their items from earlier levels (ASSESSMENT.md 2.4), and the Redo queue returns misses at 7 and 30 days |
| 5 | Product rule for counting | **Taught in 0.1** (lesson 13), with factor counting as its payoff | Wait for 0.3 counting | GCSE content N5 is Number; counting factors from a prime factorisation needs it; it gives 0.3 a running start |
| 6 | Sigma notation | **Taught in 0.2** (lesson 16) and used again in Q4 | Leave to 0.3 series | Every statistics and ML formula in Stage 1 uses $\sum$ and subscripts; the variance identity and least squares in Q4 need it |
| 7 | Optimisation without calculus | **A whole level (Q4)**: revenue, fencing, least squares in one dimension, the variance identity, AM-GM | Optimisation only in 1.3 | Completing the square is the first optimiser a quant meets; "the mean minimises squared error" is the seed of regression and of ML loss functions |
| 8 | Complex numbers | **Rectangular form in 0.2 (level Q6)**; polar form, De Moivre and roots of unity stay in 0.3 (T6) | All in 0.3 | Khan Academy Algebra 2 teaches them; the discriminant raises them; the Khan Precalculus challenge assumes them (sibling decision 3) |
| 9 | Rational functions and conics | **Rational functions (lesson 99) and circles (lesson 72) in 0.2**; holes, oblique asymptotes and partial fractions (0.3 R3) and the other conics (0.3 R4) stay in 0.3 | All in 0.3 | GCSE Higher needs the circle and its tangent; the Khan Precalculus challenge needs rational functions |
| 10 | Quant transfer | **One transfer screen per lesson where a true finance, data or interview context exists**, at least one per level | A transfer screen in every lesson | Forced contexts teach nothing; place value meets an FX pip, simultaneous equations meet replication, quadratics meet least squares |
| 11 | Exams | **Non-calculator** for both topic exams | Calculator allowed | The Stage 0 exit is a GCSE Higher non-calculator paper; exact forms (surds, fractions) test understanding that a calculator hides |
| 12 | Code in Stage 0 | **One small code drill per homework from the first level**, scaffolded to the learner's 0.4 progress; one project in 0.2. **Standard library only** (`fractions`, `math`, `cmath`, `decimal`), `needs: []` | No code until 1.1; NumPy from 0.2 | 0.4 runs alongside from week 1 (curriculum); checking maths in code from day one is the habit item 1.1 assumes. With no packages, every drill runs on Pyodide in the Artifact and on the web (`ARCHITECTURE.md` decision 15) and Python alone was ready in 2.8 s on the owner's iPhone, against 5.1 s with NumPy and pandas (`spikes/README.md`) |
| 13 | Sample lesson | **0.1 lesson 1, What a digit is worth** | Equations as balance (0.2 lesson 18); fractions as numbers (0.1 lesson 17) | It is the root of the dependency graph: decimals, standard form, rounding, binary and long multiplication all rest on it, and it is the first lesson the depth-first build ships |
| 14 | Hours and estimates | **Every block of the hours budget names the unit that carries its estimate** (lesson minutes, set item estimates, paper minutes, companion hours, exit `estHours`, project milestones). Redo and practice papers are spent time only | Leaving the mapping to the build | CI fails a topic whose estimates miss its curriculum hours by more than 10% (`CONTENT-FORMAT.md` 6.7). The mapping is a content decision, so it is made here |
| 15 | Quiz marks | **1 mark per quiz item**, 4 items per lesson unless stated, Mastered at 3 of 4 | The schema default (marks equal difficulty) | With the default a quiz of difficulties 2, 2, 3, 3 has 10 marks, and one slip on a difficulty-3 item costs more than one on a difficulty-2 item; the Mastered rule is about slips, not weights |
| 16 | Widgets the depth-first order pulls forward | **`counting-slots` into wave W1; `scatter-fit`, `dot-plot-stats` (mean and deviation marks only) and `complex-plane` into W2.** `stat-chart`, `matrix-grid` and `payoff-builder` are not used: `graph-explorer` and `value-table` cover those screens | Building 0.2 lessons that wait for wave W3; using `payoff-builder`, a P1 finance widget | `widgets-stage0.md` 13 put these in W3 for 0.3 and statistics. 0.2 reaches them first because content goes depth-first in curriculum order |

**What 0.1 and 0.2 leave to other items.**

| Topic | Where it is taught | Note |
|---|---|---|
| Exponential functions in depth, logarithms, $e$ | 0.3 course G | 0.2 teaches the shape of $y = a^x$ and linear against exponential growth only |
| Trigonometry, vectors, binomial expansion, counting beyond the product rule, series sums, limits, matrices | 0.3 | 0.2 lesson 53 previews a $3 \times 3$ system as a table of coefficients, nothing more |
| Polar form of complex numbers, conic sections other than the circle | 0.3 levels T6 and R4 | See decisions 8 and 9 |
| Logic, contrapositive, induction | 0.3 levels R1 and R2 | 0.1 lesson 41 and homework P4, and 0.2 lessons 17 and 22, give the first proofs: contradiction, direct algebraic proof, counterexample |
| GCSE geometry and measures; GCSE statistics and probability | 0.3 course S and level C5 | `stage0-precalc-computing.md` decision 2, about 40 of 0.3's 200 hours, **pending the owner's confirmation**. Without them the GCSE exit paper's 80% bar is close to unreachable |

### 1.1 0.1 Number (60 h)

**Purpose in a quant or ML career.**

- **Interview arithmetic.** Trading firms test speed and accuracy cold: Zetamac sprints (120 seconds by default), Optiver's "80 in 8" (80 questions in 8 minutes, with a penalty for each wrong answer [searched, candidate reports]) and probability answers given as fractions. Converting $\tfrac{3}{8} = 0.375 = 37.5\%$ without thought, multiplying fractions and cancelling first are the raw material of every later interview round.
- **Market quantities.** Prices move in basis points and pips; rates change by percentage points; returns compound and do not add (+50% then −50% leaves 75%); a portfolio's return is a weighted average; an average speed or an average rate is not the plain mean. Every one of these is a 0.1 lesson.
- **Sanity checks.** Standard form, orders of magnitude, rounding, estimation and error bounds are how a researcher notices that a model's output, a P&L figure or a latency is wrong by a factor of 1,000 before anyone else does.
- **Number theory for puzzles and code.** Remainders, cycles and divisibility appear in brain-teaser rounds and return in 1.8 (hashing, modular arithmetic in algorithms).
- **How computers store numbers.** $0.1 + 0.2 \ne 0.3$ in floating point; ML and pricing code fails silently when this is not understood.
- **First proofs.** The irrationality of $\sqrt{2}$ and Euclid's infinitude of primes are the learner's first proofs by contradiction, the habit the Stage 1 finals assume.

**Learning outcomes.** At the end of 0.1 the learner can, without a calculator unless stated:

| # | Outcome | Measured by |
|---|---|---|
| N-O1 | Add, subtract, multiply and divide integers, decimals and fractions, including mixed numbers and negatives, with written methods | 90% on fresh difficulty-3 items in practice; topic exam section A |
| N-O2 | Apply the order of operations and the commutative, associative and distributive laws, and give a counterexample for an operation that is not commutative or associative | Lesson quizzes 9 and 10 Mastered; exam item 8 |
| N-O3 | Find prime factorisations, HCF and LCM (by primes and by Euclid's algorithm), count factors, and use divisibility tests and remainder cycles | 85% on difficulty-3 items; the difficulty-5 items of homework W3 |
| N-O4 | Convert between fractions, terminating and recurring decimals and percentages, and predict from the denominator whether a decimal terminates | 85% on difficulty-3 items |
| N-O5 | Solve percentage change, reverse percentage, compound interest and percentage-point problems using multipliers | 85% on difficulty-3 items; exam items 14 and 15 |
| N-O6 | Solve ratio, direct and inverse proportion, rate and unit-conversion problems, and compute weighted averages and average rates | 85% on difficulty-3 items |
| N-O7 | Evaluate integer, zero, negative and fractional powers, simplify surds and rationalise denominators, and calculate in standard form | 85% on difficulty-3 items |
| N-O8 | Round to decimal places and significant figures, estimate, write error intervals and compute bounds of sums, differences, products and quotients | 80% on difficulty-3 and 4 items |
| N-O9 | Produce a Fermi estimate with stated factor ranges that lands within a factor of 3 of the reference value | 2 of 3 estimates within a factor of 3 in homework P4 |
| N-O10 | Write the proofs that $\sqrt{2}$ is irrational and that there are infinitely many primes | 7 of 10 or better on the rubric |
| N-O11 | Explain why $0.1 + 0.2 \ne 0.3$ in Python and test floats with a tolerance | Code drill P4 passes; quiz item |

**Prerequisites.** None beyond the curriculum's zero: reading English, using a browser and doing arithmetic with a calculator. 0.4 (Computer basics) and 0.5 (Mental arithmetic) run alongside from the first week; 0.1's code drills assume only what 0.4 has reached (section 3.0).

**Hours budget (60 h).**

| Block | What | Hours | Share | Unit that carries the estimate |
|---|---|---|---|---|
| In-app lessons | 42 lessons at 15 minutes, quiz included | 10.5 | 17.5% | `Lesson.est` |
| In-app practice and redo | 8 level reviews of 8 items (2.0); 8 fluency sets, one per level, of generated items (8.0); the Redo queue at 7 and 30 days (2.0) | 12.0 | 20.0% | Reviews: summed item `est`. Fluency sets: `set.<course>.<level>-fluency`, kind `practice`. Redo: spent time, no estimate |
| Homework | 8 sets at about 2 hours | 16.0 | 26.7% | Homework `set.*`, summed item `est` |
| Exams | The topic exam (75 min), one practice paper (75 min), reviewing both (30 min) | 3.0 | 5.0% | Exam minutes (1.25); practice paper: spent time; review: `0.1.exit` `estHours` 0.5 |
| External reading and lectures | Videos and reading 5.0 h; outside problem sheets (Corbettmaths, Khan unit tests, OpenStax exercises) 10.0 h | 15.0 | 25.0% | `Level.companion` hours (section 5.1) |
| Projects or drills | Number Lab: 7 code drills of 30 minutes beyond homework | 3.5 | 5.8% | `set.numwork.lab` and `set.propprec.lab`, kind `practice`, drill slots |
| **Total** | | **60.0** | 100% | Estimates: **56.75 h (94.6%)**; spent-only time 3.25 h |

Solving time (everything except the 5 hours of videos and reading) is 55 hours, 92%, above the curriculum's 60% floor.

### 1.2 0.2 Algebra (180 h)

**Purpose in a quant or ML career.**

- **The language of every later item.** Calculus, linear algebra, probability, statistics, ML and pricing are written in algebra. Fluency here decides how fast every Stage 1 item goes.
- **Linear systems lead to linear algebra and pricing.** Elimination on a $3 \times 3$ system is Gaussian elimination (1.4). Replicating a payoff with a share and a bond is a $2 \times 2$ system and the whole idea of the binomial model (1.7) and of no-arbitrage pricing.
- **Quadratics are the first optimiser.** Completing the square finds a minimum without calculus. The number that minimises squared error is the mean, which is the seed of least squares (1.4, 1.6) and of ML loss functions (2.1). The sum-of-squares identity is the variance shortcut (1.5) and its numerical trap. $(a - b)^2 \ge 0$ gives AM-GM, a staple of interview inequalities.
- **Functions and graphs.** Distributions (1.5) are functions; inverse functions become inverse CDFs and quantiles; transformations become standardisation and feature scaling (2.1); piecewise functions become option payoffs (1.7); even and odd symmetry recurs in Fourier analysis and in symmetric distributions.
- **Numerical thinking.** Iteration, bisection, chords and trapezia are the first root-finders, derivatives and integrals; root-finding returns as implied volatility in Stage 2 project 3.
- **Interview algebra.** Sum and product of roots, symmetric functions of roots, absolute-value inequalities, quick factorisation and "show that" arguments are asked directly at interview.

**Learning outcomes.** At the end of 0.2 the learner can, without a calculator:

| # | Outcome | Measured by |
|---|---|---|
| A-O1 | Expand, factorise (including $ax^2 + bx + c$, the difference of two squares and substitution) and simplify algebraic fractions | 85% on fresh difficulty-3 items |
| A-O2 | Use index laws with integer and fractional powers, subscripts and $\sum$ notation | 85% on difficulty-3 items |
| A-O3 | Write a short algebraic proof of a statement about integers and disprove a false identity with a counterexample | 7 of 10 on the rubric |
| A-O4 | Solve linear equations and inequalities (including absolute value and two-variable regions), and change the subject of a formula, including when the subject appears twice | 85% on difficulty-3 items |
| A-O5 | Find and interpret the equation, gradient, intercepts, midpoint, distance, parallels and perpendiculars of straight lines, and read rates from graphs | 85% on difficulty-3 items |
| A-O6 | Solve $2 \times 2$ and $3 \times 3$ linear systems by elimination and substitution, classify degenerate systems, and replicate a two-state payoff | 85% on difficulty-3 items; replication homework item |
| A-O7 | Solve quadratics by factorising, completing the square and the formula; derive the formula; use the discriminant and the sum and product of roots | 85% on difficulty-3 items; derivation at 7 of 10 |
| A-O8 | Sketch quadratics, cubics, reciprocals, exponentials, rational functions and circles from their features, and solve quadratic inequalities and line-curve systems | 80% on difficulty-3 items |
| A-O9 | Optimise a quadratic model and prove that the mean minimises squared error | Homework Q4 items; exam item 15 |
| A-O10 | Divide polynomials, apply the factor and remainder theorems and solve cubics | 85% on difficulty-3 items |
| A-O11 | Do arithmetic with complex numbers in the form $a + bi$ and solve any real quadratic | 85% on difficulty-3 items |
| A-O12 | Use function notation, domain and range, composition, inverses and graph transformations | 85% on difficulty-3 items |
| A-O13 | Solve equations graphically, by iteration and by bisection, estimate gradients with chords and areas with trapezia, and reject extraneous roots | 80% on difficulty-3 items; project tests pass |

**Prerequisites.** 0.1 complete, especially levels W2 (negatives), W4 (fractions) and P3 (powers and surds). 0.4 alongside: the code drills in course E need variables, arithmetic and `print`; from course L they need `def`, `if` and `for` (Automate the Boring Stuff chapters 1 to 3, which 0.4 names). 0.5 alongside.

**Hours budget (180 h).**

| Block | What | Hours | Share | Unit that carries the estimate |
|---|---|---|---|---|
| In-app lessons | 111 lessons at 15 minutes, quiz included | 27.75 | 15.4% | `Lesson.est` |
| In-app practice and redo | 19 level reviews of 8 items (4.75); 19 fluency sets of generated items at 75 minutes (23.75); the Redo queue (7.5) | 36.0 | 20.0% | Reviews: summed item `est`. Fluency sets: kind `practice`. Redo: spent time |
| Homework | 19 sets at about 2.5 hours | 47.5 | 26.4% | Homework `set.*` |
| Exams | The topic exam (90 min), two practice papers (90 min each), reviewing them (90 min) | 6.0 | 3.3% | Exam minutes (1.5); practice papers: spent time; review: `0.2.exit` `estHours` 1.5 |
| External reading and lectures | Videos and reading 16.0 h; outside problem sheets (Corbettmaths, Khan unit tests, OpenStax exercises) 30.75 h | 46.75 | 26.0% | `Level.companion` hours (section 5.2) |
| Projects or drills | Project: Root-finder toolkit (10 h); Algebra Lab: 12 code drills of 30 minutes beyond homework (6 h) | 16.0 | 8.9% | `prj.alg.root-finder` milestone hours (request R2, section 8); four lab sets of kind `practice` |
| **Total** | | **180.0** | 100% | Estimates: **169.5 h (94.2%)**; spent-only time 10.5 h |

Solving time is 164 hours, 91%.

**Why redo and practice papers carry no estimate.** A redo is a second attempt at an item whose first attempt already earned its hours, and a practice paper is assembled on demand from the practice pool (ASSESSMENT.md 3.2). Counting either as earned would credit the same hours twice. The pace factor absorbs them (ASSESSMENT.md 8.7), and both stay inside CI's 10% band.

---

## 2. Courses

### 2.0 Conventions for every lesson below

**Ids** follow CONTENT-FORMAT.md section 4.1: `crs.<course>`, `lvl.<course>.<level>`, `lsn.<course>.<slug>`, `set.<course>.<level>` for homework, `set.<course>.<level>-fluency` for the fluency set, `exm.<topic>` for the topic exam. Libraries use the topic namespaces `num` (0.1) and `alg` (0.2): `skl.num.*`, `mc.num.*`, `gen.num.*`, `drl.num.*`, `skl.alg.*`, `mc.alg.*`, `gen.alg.*`, `drl.alg.*`. Topic ids are `top.number` and `top.algebra`. The `#` column is the lesson's number within its topic; display numbers are computed from position and never stored.

**Display codes.** Courses carry a letter: W (How Numbers Work), P (Proportion, Powers and Precision), E (Expressions and Equations), L (Lines and Linear Systems), Q (Quadratics and Polynomials), F (Functions and Graphs). Level W3 is the third level of course W. The sibling file's letters (S, G, T, C, R, K, B, Y, A) do not clash.

**Every lesson** runs the design research 8.3 sequence: hook on a canvas, free manipulation, the name for what the learner just did, a ladder of 2 to 4 screens adding one constraint each, the trap, the rule stated as a description of the learner's own steps with at least one derived line the learner completes, a transfer screen where a true quant context exists, the summary card, then the quiz. From the owner's skills, every lesson also carries: the "why this exists" frame (`frame.why`), one common trap (a `trap` screen), at least one edge case (`edgeCases`), one worked example with a decision point where the naive route fails (`workedExample`), and derivations the learner completes rather than reads, with `leap` (naive, fails, points to) wherever the step is a creative one. Lessons have 8 to 12 screens, at most 2 without a task (title and summary).

**Widgets.** Names follow `CONTENT-FORMAT.md` section 1, which adopted `widgets-stage0.md` 15.1: `choice`, `numeric-input`, `expression-input`, `derivation-steps`, `free-response`, `code-cell`, `value-table`, `region-select`, `drag-point`, `sketch-pad`. Every other id is the `widgets-stage0.md` section 14 id. The engine paper fixes final names; a rename is mechanical, because content names widgets only by `type`.

**Quiz item types.** Letters are shorthand in this document only; `CONTENT-FORMAT.md` 3.4 maps them to check kinds: N numeric (`numeric`), X expression (`expression`), C single choice and M multi-select (`choice`, `select: one` or `many`), O order the steps (`ordering`), S sort or match (`mapping`), I interval or solution set (`interval` or `set`), P point or curve on a graph (`point` or `curve`), T predict the output of code (`output`). Long-form items appear in homework and exams, never in quizzes. Every quiz item carries 1 mark; a four-item quiz is Mastered at 3 of 4 (decision 15; ASSESSMENT.md decision 26).

**Choice items stay under the ceiling.** Single and multiple choice must stay at or below 40% of a course's quiz items (design research 10). Counted from the tables below:

| Course | Quiz items | C | M | C and M share |
|---|---|---|---|---|
| W How Numbers Work | 84 | 21 | 3 | 29% |
| P Proportion, Powers and Precision | 84 | 22 | 4 | 31% |
| E Expressions and Equations | 136 | 33 | 6 | 29% |
| L Lines and Linear Systems | 80 | 24 | 4 | 35% |
| Q Quadratics and Polynomials | 132 | 33 | 1 | 26% |
| F Functions and Graphs | 96 | 25 | 6 | 32% |

**Level review.** Every level ends with a Level review of 8 items at difficulty 2 to 4, interleaved, with up to 30% drawn from due cards of earlier levels of the same course (ASSESSMENT.md 2.4). The fluency set (practice, generated, about 60 minutes in 0.1 and 75 in 0.2) and the homework follow (section 3).

**Columns.** Objective is one measurable sentence. Hook is the puzzle the lesson opens with. Trap is the misconception the trap screen is built around; Edge is the fringe case the lesson must show. Transfer screens are listed under each level table.

### 2.1 Item 0.1 Number

#### Course W: How Numbers Work (`crs.numwork`, 4 levels, 21 lessons)

What a number is and how the four operations really work: place value, negatives, the laws of arithmetic, primes and remainders, fractions. The course replaces calculator dependence with understanding, which is what the non-calculator exit paper and every interview arithmetic round test.

**Level W1: Place value and calculation** (`lvl.numwork.place-value`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | `lsn.numwork.digit-worth` What a digit is worth | State the value of any digit in a whole number or decimal, order decimals, and predict multiplying or dividing by 10, 100 or 1,000 as a shift of digits | Make £305 from £100 notes, £10 notes and £1 coins using as few as possible | `place-value-chart`, `number-line` (zoom lens), `choice`, `numeric-input`, `derivation-steps` | Trap: "to multiply by 10, add a zero" gives $2.5 \times 10 = 2.50$. Edge: trailing zeros after the point change nothing ($3.5 = 3.50$); zeros between digits change everything ($3.05 \ne 3.5$) | N, N, O, C |
| 2 | `lsn.numwork.add-subtract` Adding and subtracting by exchange | Add and subtract whole numbers and decimals with the column method, explaining every carry and exchange as regrouping ten of one column into one of the next | $4{,}003 - 1{,}267$: why must the method borrow across two zeros? | `place-value-chart` (regroup), `written-method` | Trap: subtracting the smaller digit from the larger in every column ($52 - 38 = 26$). Edge: decimals with unequal lengths ($3.4 + 1.25$) need the points aligned, not the right-hand digits | N, N, N, C |
| 3 | `lsn.numwork.multiply-area` Multiplication as area | Multiply multi-digit whole numbers by splitting them by place value on a grid and justify long multiplication as the same partial products | Work out $23 \times 47$ using only facts up to $10 \times 10$ | `area-model`, `written-method` | Trap: multiplying matching parts only, $20 \times 40 + 3 \times 7 = 821$ (correct 1,081). Edge: the placeholder zero in the second row of long multiplication is a tens column, not decoration | N, N, N, C |
| 4 | `lsn.numwork.divide` Division: sharing, grouping and long division | Divide by one- and two-digit numbers with long division and report the remainder as a whole number, a fraction or a decimal as the context requires | 317 people, coaches of 52 seats: how many coaches? The calculator says 6.096 | `bar-model`, `written-method` | Trap: writing $6$ remainder $5$ as $6.5$. Edge: the context decides rounding: 7 coaches, but 6 full boxes | N, N, C, N |
| 5 | `lsn.numwork.decimal-calc` Multiplying and dividing decimals | Multiply and divide decimals without a calculator by scaling to whole numbers and back, and predict whether the result is larger or smaller than the start | Is $0.2 \times 0.3$ equal to 0.6, 0.06 or 6? | `area-model` (unit square in tenths), `place-value-chart` (shift) | Trap: "multiplying makes bigger, dividing makes smaller" fails below 1. Edge: $7.2 \div 0.08$ becomes $720 \div 8$ by scaling both numbers by 100, which leaves a quotient unchanged | N, N, C, N |

Transfer screens: lesson 1 reads an FX quote to the pip ($0.0001$); lesson 5 prices 0.3 of a share lot.

**Level W2: Negative numbers and the laws of arithmetic** (`lvl.numwork.negatives`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 6 | `lsn.numwork.below-zero` Below zero: direction and distance | Place and order positive and negative numbers on a number line and find the distance between two numbers as $\lvert a - b \rvert$ | At 6 a.m. it was $-7$ °C and at noon $4$ °C. How much warmer was noon? | `number-line` (jumps) | Trap: $-7 > -3$ "because 7 > 3". Edge: the distance between two negatives, $\lvert -7 - (-3) \rvert = 4$, is positive | S, N, N, C |
| 7 | `lsn.numwork.add-negatives` Adding and subtracting negatives | Add and subtract any integers using zero pairs, and explain why subtracting a negative equals adding its opposite | An account shows $-£40$; the bank removes a $-£15$ charge made in error. What is the balance? | `algebra-tiles` (signed counters), `number-line` (jumps) | Trap: "two minuses make a plus" applied to addition, $-5 + (-3) = 8$. Edge: $0 - (-a) = a$; removing a debt is a gain | N, N, N, C |
| 8 | `lsn.numwork.multiply-negatives` Multiplying and dividing negatives | Multiply and divide signed numbers and derive $(-1) \times (-1) = 1$ from the distributive law | Continue the pattern $3 \times (-2) = -6$, $2 \times (-2) = -4$, $1 \times (-2) = -2$, $0 \times (-2) = 0$: what is $(-1) \times (-2)$? | `number-line` (scale and reflect operators), `derivation-steps` | Trap: $(-3)^2 = -9$. Edge: the pattern argument suggests the rule; the distributive-law argument proves it, because the rule is forced if arithmetic's laws are to keep holding | N, N, O, C |
| 9 | `lsn.numwork.order-ops` Order of operations | Evaluate expressions with brackets, powers, roots, the four operations and fraction bars in the conventional order, and read $-3^2$ correctly | Two calculators disagree on $6 \div 2(1 + 2)$. Which convention decides, and how would you write it so that nobody can misread it? | `expression-tree` | Trap: $-3^2 = 9$; working strictly left to right, $2 + 3 \times 4 = 20$. Edge: a fraction bar groups its top and bottom like brackets; $6 \div 2(1+2)$ is ambiguous notation, so professionals write $\frac{6}{2(1+2)}$ or $\frac{6}{2}(1+2)$ | N, N, C, N |
| 10 | `lsn.numwork.laws` The laws of arithmetic | Reorganise calculations with the commutative, associative and distributive laws, and give counterexamples showing subtraction and division are neither commutative nor associative | Compute $25 \times 37 \times 4$ in five seconds | `expression-tree` (rearrange), `area-model` | Trap: distributing over a product, $2 \times (3 \times 4) = (2 \times 3)(2 \times 4)$. Edge: $12 \div (2 + 4) \ne 12 \div 2 + 12 \div 4$: division distributes from the right over a sum, $(2 + 4) \div 12 = \frac{2}{12} + \frac{4}{12}$, never from the left | C, N, M, N |

Transfer screens: lesson 7 runs a signed P&L ledger; lesson 10 splits $48 \times 25$ the way an interviewer expects.

**Level W3: Factors, primes and counting** (`lvl.numwork.primes`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 11 | `lsn.numwork.factors-primes` Factors, multiples and primes | List all factors of a number up to 200 in pairs, decide primality by testing primes up to its square root, and explain why 1 is not prime | In how many ways can 24 chairs stand in a rectangle? And 23? | `area-model` (array mode), `choice` | Trap: 1 counted as prime; 91 looks prime ($7 \times 13$). Edge: testing stops at $\sqrt{n}$ because factors pair up across it; a perfect square has an unpaired factor, so an odd number of factors | M, N, C, N |
| 12 | `lsn.numwork.prime-factorisation` Prime factorisation | Write any whole number up to 10,000 as a product of prime powers and use it to test divisibility and to find square and cube roots of perfect powers | Two people factorise 360 with different trees. Must they reach the same primes? | `factor-tree`, `expression-input` | Trap: stopping at a composite leaf ($360 = 2 \times 2 \times 90$). Edge: uniqueness of factorisation is why 1 is not prime; if it were, $6 = 2 \times 3 = 1 \times 2 \times 3$ would break uniqueness | X, N, C, N |
| 13 | `lsn.numwork.product-rule` Listing systematically and the product rule | Count outcomes by systematic listing and by the product rule, and count the factors of a number from its prime factorisation | How many factors does 360 have? Listing them takes a while; is there a shortcut? | `counting-slots`, `factor-tree`, `region-select` | Trap: adding the choices instead of multiplying; using $3 \times 2 \times 1$ for $2^3 \times 3^2 \times 5$ instead of $(3+1)(2+1)(1+1) = 24$. Edge: a choice of "none of this prime" is the exponent 0, which is where the $+1$ comes from | N, N, N, C |
| 14 | `lsn.numwork.hcf-lcm` Highest common factor and lowest common multiple | Find the HCF and LCM of two or three numbers from prime factorisations and by Euclid's algorithm, and use $\text{HCF}(a, b) \times \text{LCM}(a, b) = ab$ | Two buses leave together, one every 12 minutes and one every 18. When do they next leave together? | `venn-diagram`, `factor-tree`, `written-method` (Euclid's steps) | Trap: answering with the HCF (6 minutes) or the product (216 minutes). Edge: the product identity fails for three numbers: $\text{HCF}(2,4,8) \times \text{LCM}(2,4,8) = 16 \ne 64$ | N, N, C, N |
| 15 | `lsn.numwork.divisibility` Divisibility tests and why they work | Apply tests for 2, 3, 4, 5, 6, 8, 9 and 11 and prove the digit-sum test for 9 from place value | Is 7,425,846 divisible by 9? Decide in ten seconds | `place-value-chart` (remainder view), `derivation-steps` | Trap: divisible by 4 and by 6 means divisible by 24 (12 is a counterexample). Edge: the digit-sum test works for 3 and 9 because $10$ leaves remainder 1; it fails for 7 because $10$ leaves remainder 3 | M, C, O, N |
| 16 | `lsn.numwork.remainders` Remainders and cycles | Compute remainders of sums, products and powers by working with remainders only, and find the last digit of a large power from its cycle | What is the last digit of $3^{100}$? | `modular-clock`, `value-table` (cycle) | Trap: off by one in the cycle: $100 = 4 \times 25$ leaves remainder 0, which is position 4 (last digit 1), not position 0. Edge: cycles need not start at once: $2^n \bmod 12$ runs 2, 4, 8, 4, 8, ... | N, N, N, C |

Transfer screens: lesson 13 counts four-digit PINs and order types; lesson 16 is the interview "last digit" question and a day-of-the-week calculation.

**Level W4: Fractions** (`lvl.numwork.fractions`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 17 | `lsn.numwork.fractions-numbers` Fractions are numbers | Represent a fraction as part of a whole, as a point on the number line and as a division, and convert between improper fractions and mixed numbers | Three pizzas are shared equally by four people. How much does each get, and where is that on the number line? | `bar-model`, `number-line` | Trap: a fraction as two unrelated whole numbers ("3/4 is 3 and 4"). Edge: $\frac{a}{b} = a \div b$ makes $\frac{a}{0}$ meaningless, and $\frac{0}{b} = 0$ | P, C, N, X |
| 18 | `lsn.numwork.equivalent` Equivalent fractions and comparing | Generate equivalent fractions, simplify with the HCF, and order fractions by common denominators or cross-multiplication | Which is bigger, $\frac{5}{8}$ or $\frac{3}{5}$, and by how much? | `bar-model` (refine), `number-line` | Trap: a bigger denominator means a bigger fraction. Edge: adding the same number to top and bottom changes the value ($\frac{2}{3} \to \frac{3}{4}$) and moves it towards 1 | S, X, C, N |
| 19 | `lsn.numwork.add-fractions` Adding and subtracting fractions | Add and subtract fractions and mixed numbers by refining to a common denominator, and explain why adding tops and bottoms fails | A recipe needs $\frac{1}{3}$ cup then $\frac{1}{4}$ cup more. A friend says that is $\frac{2}{7}$ cup. Can that be right? | `bar-model`, `number-line` | Trap: $\frac{a}{b} + \frac{c}{d} = \frac{a + c}{b + d}$, which gives an answer smaller than $\frac{1}{3}$. Edge: that "mediant" is the right way to pool success rates (2 of 3 and 1 of 4 make 3 of 7), which is where Simpson's paradox later comes from | X, X, C, N |
| 20 | `lsn.numwork.multiply-fractions` Multiplying fractions | Multiply fractions and mixed numbers, read "of" as multiplication, and cancel common factors before multiplying | $\frac{2}{3}$ of a field is planted and $\frac{3}{4}$ of the planted part is wheat. What fraction of the field is wheat? | `area-model` (fraction mode) | Trap: multiplying mixed numbers part by part, $2\frac{1}{2} \times 3\frac{1}{2} = 6\frac{1}{4}$ (correct $8\frac{3}{4}$). Edge: multiplying by a fraction below 1 makes a positive number smaller | X, X, N, C |
| 21 | `lsn.numwork.divide-fractions` Dividing fractions | Divide by a fraction, derive "multiply by the reciprocal" from the meaning of division, and predict when a quotient exceeds the number divided | How many $\frac{3}{4}$-metre pieces can be cut from 2 metres of rope? | `bar-model` (tape), `number-line`, `derivation-steps` | Trap: inverting the wrong fraction, $2 \div \frac{3}{4} = \frac{3}{8}$. Edge: $2 \div \frac{3}{4} = 2\frac{2}{3}$, but only 2 whole pieces can be cut; the context decides | X, N, C, X |

Transfer screens: lesson 19 pools two traders' hit rates (the mediant, correctly used); lesson 20 is "a fraction of a fraction" in a fund's holdings.

#### Course P: Proportion, Powers and Precision (`crs.propprec`, 4 levels, 21 lessons)

Multiplicative thinking (percentages, ratio, rates), powers and roots, and the honesty of numbers: rounding, bounds, estimation, irrationality and floating point. Most finance arithmetic lives in this course.

**Level P1: Decimals and percentages** (`lvl.propprec.percent`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 22 | `lsn.propprec.fraction-decimal` Fractions to decimals | Convert fractions to decimals by division, predict from the denominator's prime factors whether the decimal terminates, and find a recurring cycle by tracking remainders | Why does $\frac{1}{8}$ stop at 0.125 while $\frac{1}{3}$ and $\frac{1}{7}$ go on forever? | `written-method` (remainder tracker), `factor-tree` | Trap: "large denominators recur": $\frac{1}{20} = 0.05$ terminates. Edge: simplify first: $\frac{3}{6}$ terminates although $6 = 2 \times 3$; a cycle can be no longer than the denominator minus one ($\frac{1}{7}$ has 6 digits) | M, N, N, C |
| 23 | `lsn.propprec.recurring` Recurring decimals as fractions | Convert any recurring decimal to a fraction in lowest terms by shifting and subtracting, and justify $0.\dot{9} = 1$ | Is $0.999\ldots$ (nines forever) less than 1? If so, by how much? | `derivation-steps` (complete the line), `expression-input` | Trap: $0.1\dot{6}$ treated as $\frac{16}{99}$; the non-recurring part needs its own shift. Edge: $0.\dot{9} = 1$ exactly; some numbers have two decimal expansions | X, X, O, C |
| 24 | `lsn.propprec.percent` Percentages: parts per hundred | Convert between fractions, decimals and percentages, find a percentage of an amount mentally, and express one quantity as a percentage of another | Which is more, 35% of 60 or 60% of 35? | `region-select` (percent grid), `double-number-line` | Trap: $5\% = 0.5$. Edge: percentages above 100% (a 250% return) and $x\%$ of $y$ always equals $y\%$ of $x$ | N, N, C, N |
| 25 | `lsn.propprec.percent-change` Percentage change and multipliers | Apply a percentage change as one multiplier, compute a percentage change from old and new values, and reverse a multiplier to find an original value | A jacket costs £84 after a 30% discount. What was the original price? | `double-number-line`, `bar-model`, `multiplier-chain` | Trap: adding 30% back ($84 \times 1.3 = £109.20$; correct £120). Edge: percentage change is measured from the old value, so a fall from 120 to 84 is 30% but a rise from 84 to 120 is about 42.9% | N, N, N, C |
| 26 | `lsn.propprec.repeated-change` Repeated change and compound interest | Chain percentage changes as multipliers, compute compound growth and depreciation with $P(1 + r)^n$, and distinguish percentage points from percentages | A share rises 50% one day and falls 50% the next. Are you back where you started? | `multiplier-chain`, `graph-explorer` (simple against compound), `value-table` | Trap: changes add ($+50 - 50 = 0$). Edge: a rate rising from 4% to 5% is up 1 percentage point and up 25%; 1 basis point is $0.01\%$ | N, N, C, N |

Transfer screens: lesson 24 reads a fund's fee as basis points; lesson 26 is the decay of a fund that doubles each day's move.

**Level P2: Ratio, rates and proportion** (`lvl.propprec.ratio`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 27 | `lsn.propprec.ratio` Ratio and sharing | Simplify ratios, divide a quantity in a given ratio, and convert between part-to-part ratios and part-to-whole fractions | £56,000 profit is split between partners in the ratio $3 : 5$. One says she gets $\frac{3}{5}$ of it. Is she right? | `bar-model` (tape) | Trap: $3 : 5$ read as $\frac{3}{5}$ of the whole (correct $\frac{3}{8}$). Edge: ratios with units must share units first ($40\text{ cm} : 2\text{ m} = 1 : 5$); map scales such as $1 : 25{,}000$ | N, N, C, X |
| 28 | `lsn.propprec.direct-proportion` Direct proportion and unit rates | Solve direct proportion problems by unit rate and by scaling, compare value for money, and recognise a proportional relationship as $y = kx$ | Which is better value: 450 g for £2.79 or 750 g for £4.50? | `double-number-line`, `graph-explorer` ($y = kx$) | Trap: additive reasoning ("150 g more for 45p more"). Edge: grams per penny and pence per gram both work, but "better" is the larger of one and the smaller of the other | N, C, N, X |
| 29 | `lsn.propprec.inverse-proportion` Inverse proportion | Recognise inverse proportion as a constant product, solve problems with $y = \frac{k}{x}$, and explain why doubling one quantity halves the other | 6 workers take 10 days to build a wall. How long would 4 workers take? | `area-model` (constant-area rectangle), `graph-explorer` ($y = \frac{k}{x}$) | Trap: treating it as direct proportion ($6\frac{2}{3}$ days; correct 15). Edge: the model assumes workers never get in each other's way; it breaks for 1,000 workers | N, N, C, M |
| 30 | `lsn.propprec.rates-units` Rates, compound measures and units | Convert units, including area, volume and compound units, by chaining conversion fractions until units cancel, and use speed, density and pressure | A car does 30 metres per second. Is that faster than 100 km/h? | `unit-chain` | Trap: $1\text{ m}^2 = 100\text{ cm}^2$ (correct 10,000). Edge: exchange-rate chains: a round trip through a bid-offer spread loses money | N, N, N, C |
| 31 | `lsn.propprec.averaging-rates` Averaging rates and weighted averages | Compute weighted averages, including portfolio returns and the average speed of a round trip, and explain why the plain mean of two speeds is usually wrong | You drive to a town at 30 mph and back at 60 mph. What was your average speed? | `bar-model`, `double-number-line`, `value-table` | Trap: averaging the rates ($45$ mph; correct 40). Edge: averaging over equal times, not equal distances, does give 45 | N, N, N, C |

Transfer screens: lesson 30 converts a quote between currencies through the spread; lesson 31 computes a 60/40 portfolio's return and a volume-weighted average price.

**Level P3: Powers and roots** (`lvl.propprec.powers`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 32 | `lsn.propprec.index-laws` Powers and the index laws | Write repeated products in index form and derive the multiplication, division and power-of-a-power laws by counting factors | Is $2^{10}$ about a thousand or a million? And $2^{10} \times 2^{10}$? | `expression-tree` (expand powers), `expression-input` | Trap: $2^3 \times 2^4 = 4^7$. Edge: the laws need the same base; $2^3 \times 3^2$ does not combine | X, X, N, C |
| 33 | `lsn.propprec.zero-negative-index` Zero and negative indices | Evaluate zero and negative powers, justify $a^0 = 1$ and $a^{-n} = \frac{1}{a^n}$ by extending the halving pattern, and say why $0^0$ and $0^{-1}$ need care | $2^3 = 8$, $2^2 = 4$, $2^1 = 2$. Continue: what are $2^0$ and $2^{-1}$? | `value-table` (pattern), `number-line` (scale operator) | Trap: $2^{-3} = -8$; $5^0 = 0$. Edge: $0^{-1}$ would be $\frac{1}{0}$; $0^0$ is left undefined in school maths though computing conventions set it to 1 | N, N, X, C |
| 34 | `lsn.propprec.roots-fractional` Roots and fractional indices | Evaluate square, cube and $n$th roots, read $a^{\frac{1}{n}}$ and $a^{\frac{m}{n}}$ as roots and powers, and bracket non-perfect roots between integers | What number times itself gives 30? Between which whole numbers must it lie? | `area-model` (square mode), `slider`, `number-line` | Trap: $8^{\frac{2}{3}} = 8 \times \frac{2}{3}$. Edge: $\sqrt{9} = 3$, not $\pm 3$ (the symbol means the principal root); $\sqrt[3]{-8} = -2$ exists but $\sqrt{-4}$ is not a real number | N, N, C, N |
| 35 | `lsn.propprec.surds` Surds | Simplify surds by extracting square factors, multiply and divide them, and rationalise denominators including $\frac{1}{a + \sqrt{b}}$ | A square has area $72\text{ cm}^2$. Write its side exactly and as simply as possible | `factor-tree`, `equation-workbench`, `expression-input` | Trap: $\sqrt{a + b} = \sqrt{a} + \sqrt{b}$ ($\sqrt{9 + 16} \ne 7$). Edge: $\sqrt{ab} = \sqrt{a}\sqrt{b}$ only for non-negative $a, b$ | X, X, X, C |
| 36 | `lsn.propprec.standard-form` Standard form | Write numbers as $A \times 10^n$ with $1 \le A < 10$, calculate with them without a calculator, and compare orders of magnitude | A day has 86,400 seconds. How many microseconds is that, in standard form? | `place-value-chart` (shift), `number-line` (log scale) | Trap: leaving $12 \times 10^9$ unnormalised, or adding exponents when adding numbers. Edge: $3 \times 10^4 + 2 \times 10^3 = 3.2 \times 10^4$, not $5 \times 10^7$ | X, N, C, N |

Transfer screens: lesson 32 is $2^{10} \approx 10^3$ as the engineer's rule for memory sizes; lesson 36 compares exchange latencies in microseconds and nanoseconds.

**Level P4: Precision, estimation and the real numbers** (`lvl.propprec.precision`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 37 | `lsn.propprec.rounding` Rounding: decimal places and significant figures | Round to a given number of decimal places or significant figures, including across zeros, and choose an accuracy that suits the context | Round 0.0030495 to 3 significant figures | `number-line` (rounding bins, lens) | Trap: counting leading zeros as significant; rounding in stages ($0.0449 \to 0.045 \to 0.05$; correct $0.04$). Edge: a trailing zero can be significant: 2.50 m claims more precision than 2.5 m | N, N, C, N |
| 38 | `lsn.propprec.estimation` Estimation and checking | Estimate by rounding each number to one significant figure, say whether the estimate is over or under, and use estimates to catch errors | Without a calculator, is $\frac{48.7 \times 0.52}{0.098}$ about 2.5, 25, 250 or 2,500? | `number-line` (log scale), `choice` | Trap: "rounding up gives an overestimate". For a divisor it is the reverse: rounding 0.098 up to 0.1 shrinks the quotient, and the numerator's roundings (48.7 up, 0.52 down) net to 25, just under 25.32, so the estimate $\frac{50 \times 0.5}{0.1} = 250$ is below the true value, about 258.4. Edge: rounding $0.098$ to $0.1$ is fine; rounding $0.4$ to $0$ destroys the estimate | C, N, C, N |
| 39 | `lsn.propprec.bounds` Error intervals and bounds | Write error intervals for rounded and truncated values and compute upper and lower bounds of sums, differences, products and quotients | A length is 12 cm to the nearest cm and a time is 4.0 s to 1 d.p. What is the greatest possible average speed? | `number-line` (intervals), `bounds-explorer` | Trap: upper bound of a difference as upper minus upper; of a quotient as upper over upper. Edge: when a quantity appears twice in a formula, its bounds cannot be chosen independently (homework P4) | I, N, N, C |
| 40 | `lsn.propprec.fermi` Fermi estimation and orders of magnitude | Break an unknown quantity into estimable factors, give each a range, and combine them into an order-of-magnitude estimate with a stated uncertainty | How many piano tuners work in London? | `fermi-estimator`, `number-line` (log scale) | Trap: false precision (answering 1,247); averaging bounds arithmetically instead of geometrically. Edge: factor errors partly cancel, so an estimate built from five factors each within $\times 2$ typically lands within about $\times 2.5$ of the truth, far from the worst case of $\times 32$ | N, C, N, M |
| 41 | `lsn.propprec.irrational` Rational and irrational numbers | Classify numbers as natural, integer, rational or irrational, and reconstruct the proof by contradiction that $\sqrt{2}$ is irrational | Find a fraction whose square is exactly 2. Try $\frac{7}{5}$, $\frac{17}{12}$, $\frac{41}{29}$ | `derivation-steps` (order mode), `free-response`, `value-table` | Trap: "irrational means a long decimal" ($\frac{1}{7}$ recurs and is rational); $\pi = \frac{22}{7}$. Edge: the sum of two irrationals can be rational: $\sqrt{2} + (-\sqrt{2}) = 0$ | M, O, C, S |
| 42 | `lsn.propprec.binary-float` Binary and how computers store numbers | Convert between binary and decimal, explain from the denominator rule why 0.1 has no finite binary expansion, and predict why $0.1 + 0.2 \ne 0.3$ in floating point | Type `0.1 + 0.2` into Python. Why is the answer not 0.3? | `place-value-chart` (base mode), `code-cell` (predict output) | Trap: "the computer made a mistake". Edge: $0.5$, $0.25$ and $0.375$ are stored exactly, because their denominators are powers of 2; test floats with a tolerance (`math.isclose`), never `==` | N, N, C, T |

Transfer screens: lesson 39 bounds a Sharpe-ratio-style quotient from rounded inputs; lesson 40 is the classic interview estimate; lesson 42 shows a cumulative P&L drifting by summing floats.

### 2.2 Item 0.2 Algebra

#### Course E: Expressions and Equations (`crs.expreq`, 6 levels, 34 lessons)

Letters as numbers, the rules for moving them, and the first equations and inequalities. Every manipulation is first done to a picture (tiles, rectangles, balances, trees) and only then to symbols.

**Level E1: Letters for numbers** (`lvl.expreq.letters`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | `lsn.expreq.letters` Letters stand for numbers | Write a general rule for a growing pattern using a letter, and distinguish a letter as an unknown from a letter as a variable | One square takes 4 matchsticks, two squares in a row take 7, three take 10. How many for 100 squares? | `function-machine`, `value-table`, `token-tray` | Trap: a letter as an object ("$3a$ means 3 apples"); a term-to-term rule ("add 3") that cannot jump to the 100th term. Edge: $3n + 1$ and $4 + 3(n - 1)$ look different and are the same rule | X, N, C, X |
| 2 | `lsn.expreq.writing` Writing expressions | Translate between words and expressions using the conventions for products, powers and quotients | There are $s$ students and $p$ professors, six students for every professor. Write the equation | `card-sort` (words to expressions), `expression-input` | Trap: the reversal $6s = p$ (correct $s = 6p$). Edge: "5 less than $x$" is $x - 5$ but "$x$ less than 5" is $5 - x$ | S, X, X, C |
| 3 | `lsn.expreq.substitution` Substitution | Evaluate expressions for given values, including negatives and fractions, respecting the order of operations | If $x = -3$, is $-x^2$ equal to 9 or $-9$? And $(-x)^2$? | `expression-tree` (substitute), `function-machine` | Trap: $-x^2 = 9$ at $x = -3$; $2x = 25$ at $x = 5$. Edge: substituting a negative always goes in brackets: $x^2$ at $x = -3$ is $(-3)^2 = 9$ | N, N, N, C |
| 4 | `lsn.expreq.like-terms` Collecting like terms | Simplify by collecting like terms, identifying terms by their whole variable part including powers | Simplify $3x + 2y - x + 5y$. Is $3x^2 + 2x$ equal to $5x^3$? | `algebra-tiles` | Trap: combining unlike terms ($x + x^2 = 2x^3$, $3x + 2y = 5xy$). Edge: $xy$ and $yx$ are like terms; $3x^2y$ and $3xy^2$ are not | X, X, M, X |
| 5 | `lsn.expreq.multiply-terms` Multiplying and dividing terms | Multiply and divide single terms by applying the index laws to each letter separately | A rectangle is $3x$ by $4x$. Is its area $12x$, $7x$ or $12x^2$? | `area-model` (symbolic), `expression-input` | Trap: $3x \times 4x = 12x$; $(2x^3)^2 = 2x^6$. Edge: $x^2y^3$ does not combine further; different letters are different bases | X, X, X, C |
| 6 | `lsn.expreq.identity` Expressions, equations, formulae and identities | Classify statements as expressions, equations, formulae or identities, test a claimed identity by substitution, and disprove a false one with one counterexample | Is $(a + b)^2 = a^2 + b^2$? Test $a = 1, b = 0$. Then $a = b = 1$ | `card-sort`, `function-machine`, `numeric-input` | Trap: one confirming example "proves" an identity ($a = 1, b = 0$ works). Edge: $x + 1 = 3$ holds for one value, $2(x + 1) \equiv 2x + 2$ for every value, $x + 1 = x + 2$ for none | S, C, N, M |

Transfer screens: lesson 1 writes a day's commission as a formula in the number of trades; lesson 6 makes the point that a strategy that worked once is an example, not a proof.

**Level E2: Brackets and factorising** (`lvl.expreq.brackets`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 7 | `lsn.expreq.expand-single` Expanding a bracket | Expand a single bracket, including negative multipliers, and explain expansion as the area of a split rectangle | A rectangle is 5 wide and $x + 3$ long. Write its area in two ways | `area-model` (symbolic), `algebra-tiles` | Trap: $-(x - 3) = -x - 3$; $2(x + 3) = 2x + 3$. Edge: $-2(3 - x) = -6 + 2x$; the sign belongs to the multiplier | X, X, X, C |
| 8 | `lsn.expreq.factorise-common` Factorising out a common factor | Factorise by taking out the highest common factor, including letters and brackets, and check by expanding | Write $6x^2 + 9x$ as a single product. How many ways can you find, and which is "fully" factorised? | `algebra-tiles` (rectangle), `expression-input` | Trap: stopping at $3(2x^2 + 3x)$; $4x + 4 = 4(x)$. Edge: a common factor can be a bracket, $x(a + b) + 3(a + b) = (x + 3)(a + b)$, or negative, $-2x - 6 = -2(x + 3)$ | X, X, C, X |
| 9 | `lsn.expreq.double-brackets` Expanding double brackets | Expand products of two binomials with the area grid and show why $(a + b)^2 \ne a^2 + b^2$ | A square photo of side $x$ gets a border 2 wide all round. What is the new area? | `area-model` (symbolic), `algebra-tiles` | Trap: $(x + 4)^2 = x^2 + 16$. Edge: $(x - 4)(x + 4)$ has no middle term, because the two cross terms cancel | X, X, X, C |
| 10 | `lsn.expreq.special-products` Special products | Expand perfect squares and the difference of two squares on sight and use them for mental arithmetic | Compute $49 \times 51$ and $98^2$ in your head | `area-model` (cut and move), `expression-input` | Trap: $(x - 3)^2 = x^2 - 9$ or $x^2 - 6x - 9$. Edge: $(a - b)^2 = (b - a)^2$; squaring hides the order | N, N, X, X |
| 11 | `lsn.expreq.longer-products` Products of three brackets and longer | Expand products of three binomials and of longer polynomials, predicting the number of terms before collecting | Expand $(x + 1)(x + 2)(x + 3)$. Before you start: how many terms appear before collecting? | `area-model` (symbolic, two passes), `expression-input` | Trap: missing a pair of terms; sign slips with negatives. Edge: $(x + 1)^3$ has coefficients 1, 3, 3, 1, a first look at Pascal's triangle (0.3) | X, X, N, C |

Transfer screens: lesson 10 is the interview mental-arithmetic trick ($103 \times 97 = 10{,}000 - 9$).

**Level E3: Algebraic fractions, indices, sums and proof** (`lvl.expreq.fractions-proof`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 12 | `lsn.expreq.simplify-fractions` Simplifying algebraic fractions | Simplify algebraic fractions by factorising top and bottom and cancelling common factors, stating the excluded values | Is $\frac{x + 3}{3}$ equal to $x + 1$? Try $x = 3$ | `equation-workbench`, `expression-input` | Trap: cancelling terms instead of factors. Edge: $\frac{2x + 6}{x^2 + 3x} = \frac{2}{x}$ only for $x \ne -3$; the simplified form is defined at $-3$ and the original is not | X, X, C, X |
| 13 | `lsn.expreq.add-fractions` Adding and subtracting algebraic fractions | Add and subtract algebraic fractions over a lowest common denominator and simplify | Simplify $\frac{1}{x} + \frac{1}{x + 1}$ and check your answer at $x = 1$ | `equation-workbench`, `bar-model` (common partition, as in 0.1) | Trap: $\frac{1}{x} + \frac{1}{y} = \frac{2}{x + y}$. Edge: subtracting a two-term numerator, $\frac{1}{x} - \frac{x - 1}{x} = \frac{2 - x}{x}$; the minus reaches both terms | X, X, X, C |
| 14 | `lsn.expreq.multiply-fractions` Multiplying and dividing algebraic fractions | Multiply and divide algebraic fractions by factorising fully first and cancelling | Simplify $\frac{4x}{x + 1} \div \frac{2x^2}{3x + 3}$ | `equation-workbench`, `expression-input` | Trap: inverting the first fraction; cancelling across a plus sign. Edge: the excluded values include those that make the divisor zero ($x \ne 0$ as well as $x \ne -1$) | X, X, C, X |
| 15 | `lsn.expreq.index-letters` Index laws with letters | Simplify expressions with integer and fractional indices, writing answers with positive indices or as roots as asked | Simplify $(8x^6)^{\frac{1}{3}}$ and $\frac{x^{\frac{1}{2}} \cdot x^{\frac{3}{2}}}{x^{-1}}$ | `expression-tree`, `expression-input` | Trap: $(8x^6)^{\frac{1}{3}} = 8x^2$; $x^{-1} = -x$. Edge: $(x^2)^{\frac{1}{2}} = \lvert x \rvert$, not $x$ | X, X, X, C |
| 16 | `lsn.expreq.sigma` Subscripts and sigma notation | Read and write sums with subscripts and $\sum$, evaluate them, and use $\sum (a x_i + b) = a \sum x_i + nb$ | Five daily returns are 2, $-1$, 3, 0 and 1 (in %). Write their mean in one line of notation that would also work for 5,000 days | `value-table` (with a sum row), `expression-input` | Trap: $\sum x_i^2 = \left(\sum x_i\right)^2$; $\sum_{i=1}^{n} c = c$ (correct $nc$). Edge: $\sum_{i=1}^{n} (x_i - \bar{x}) = 0$ for every data set; deviations from the mean always cancel | N, N, C, X |
| 17 | `lsn.expreq.proof` Algebraic proof | Prove simple statements about integers by writing even, odd and consecutive numbers as $2n$, $2n + 1$ and $n, n + 1, n + 2$ | Add any three consecutive whole numbers. Is the total always a multiple of 3? Always a multiple of 6? | `derivation-steps`, `free-response`, `numeric-input` | Trap: checking examples is not proof; writing two different odd numbers both as $2n + 1$. Edge: $n^2 + n + 41$ is prime for $n = 0$ to $39$ and fails at $n = 40$ ($1{,}681 = 41^2$) | O, C, N, M |

Transfer screens: lesson 16 writes a portfolio return as $\sum_i w_i r_i$ and runs the "deviations sum to zero" check every data scientist uses on a fresh data set.

**Level E4: Linear equations** (`lvl.expreq.linear`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 18 | `lsn.expreq.balance` Equations as balance | Solve one- and two-step linear equations by doing the same to both sides, and check by substitution | Three identical boxes and four 1 kg weights balance 19 kg. How heavy is a box? | `balance-scale`, `function-machine` (inverse) | Trap: undoing in the wrong order ($3x + 4 = 19 \Rightarrow x = \frac{19}{3} - 4$). Edge: solutions can be negative or fractional, which the balance cannot show; that is why we move to symbols | N, N, N, C |
| 19 | `lsn.expreq.both-sides` Unknowns on both sides | Solve linear equations with the unknown on both sides by removing the smaller unknown term from both sides | Five boxes and 2 kg balance two boxes and 14 kg. What does a box weigh? | `balance-scale`, `equation-workbench` | Trap: moving a term across without changing its sign ($5x + 2 = 2x + 14 \Rightarrow 7x = 12$). Edge: $3 - 2x = x + 9$ has the negative solution $x = -2$ | N, N, N, C |
| 20 | `lsn.expreq.brackets-fractions` Equations with brackets and fractions | Solve linear equations with brackets and fractions by expanding and multiplying every term by the lowest common denominator | Solve $\frac{x}{3} + \frac{x}{4} = 7$ | `equation-workbench` | Trap: multiplying only some terms by the denominator. Edge: in $\frac{x - 2}{3} - \frac{x + 1}{2}$ the minus applies to the whole second numerator | N, N, N, C |
| 21 | `lsn.expreq.forming` Forming equations from words | Translate a word problem into a linear equation with a tape diagram, solve it and interpret the answer | A bat and a ball cost £1.10. The bat costs £1.00 more than the ball. How much is the ball? | `bar-model` (tape), `equation-workbench` | Trap: the intuitive 10p (correct 5p). Edge: an answer can solve the equation and fail the story (a negative number of people) | N, N, X, C |
| 22 | `lsn.expreq.no-solution` No solution, every solution, and dividing by zero | Recognise equations with no solution or every solution, and find the illegal step in an argument that divides by something that can be zero | A "proof" that $2 = 1$: let $a = b$; then $a^2 = ab$, $a^2 - b^2 = ab - b^2$, $(a + b)(a - b) = b(a - b)$, $a + b = b$, $2b = b$, $2 = 1$. Which line is illegal? | `derivation-steps` (find the bad line), `equation-workbench` | Trap: dividing $x^2 = 3x$ by $x$ and losing $x = 0$. Edge: $2(x + 3) = 2x + 6$ is solved by every $x$; $2x + 3 = 2x + 5$ by none | C, I, C, N |
| 23 | `lsn.expreq.linear-models` Linear models: cost, revenue and break-even | Build linear cost and revenue models from fixed and variable parts, find the break-even point, and interpret slope and intercept | A market-data feed costs £2,000 a month plus £0.50 per thousand messages; a rival charges £5,000 flat. At what volume do they cost the same? | `graph-explorer`, `equation-workbench` | Trap: reading break-even as the point where cost is zero. Edge: a break-even point at a negative volume means one option is always cheaper | N, X, N, C |

Transfer screens: lesson 21 is the best-known item of Frederick's cognitive reflection test (2005), the kind of question that rewards checking an intuitive answer; lesson 23 is a data-vendor decision.

**Level E5: Formulae and changing the subject** (`lvl.expreq.formulae`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 24 | `lsn.expreq.substitute-formulae` Using formulae | Substitute values into formulae with units, including negative and fractional values, and check the units of the result | Convert $-40$ °C to Fahrenheit with $F = \frac{9}{5}C + 32$. What do you notice? | `function-machine`, `unit-chain` | Trap: the order of operations inside a formula ($\frac{9}{5C}$ instead of $\frac{9}{5} \times C$). Edge: mixed units (minutes against hours) give a number with no meaning | N, N, N, C |
| 25 | `lsn.expreq.change-subject` Changing the subject | Rearrange a formula whose new subject appears once by undoing its operations from the outside in | Rearrange $F = \frac{9}{5}C + 32$ to give $C$, then check it with $-40$ | `expression-tree` (solve mode), `equation-workbench` | Trap: undoing in the wrong order ($C = \frac{5F}{9} - 32$). Edge: a rearrangement describes the same relation, so every known pair must still satisfy it; that is a free self-check | X, X, X, C |
| 26 | `lsn.expreq.subject-twice` When the subject appears twice | Rearrange formulae whose new subject appears in more than one term by collecting those terms and factorising | Make $x$ the subject of $ax + b = cx + d$. When does your answer fail? | `equation-workbench` | Trap: dividing by the subject. Edge: if $a = c$ the formula $x = \frac{d - b}{a - c}$ fails: no solution, or every $x$ | X, X, C, X |
| 27 | `lsn.expreq.powers-roots-formulae` Formulae with powers and roots | Rearrange formulae involving squares, square roots and reciprocals, choosing the sign of a root from the context | A pendulum's period is $T = 2\pi\sqrt{\frac{l}{g}}$. Make $l$ the subject | `expression-tree` (solve mode), `equation-workbench` | Trap: squaring only part of one side. Edge: $A = \pi r^2$ gives $r = \sqrt{\frac{A}{\pi}}$ with no $\pm$, because a radius is never negative | X, X, C, N |
| 28 | `lsn.expreq.dimensions` Checking formulae with units | Use units to reject an impossible formula and to predict the form of an unknown one | A student claims distance travelled is $d = \frac{v}{t}$. Without numbers, how do you know it is wrong? | `unit-chain`, `card-sort` | Trap: "the units match, so the formula is right" ($d = 2vt$ has correct units and the wrong constant). Edge: the method finds $T \propto \sqrt{\frac{l}{g}}$ but can never find the $2\pi$ | M, C, X, N |

Transfer screens: lesson 28 checks the units of an annualised figure (a daily return times 252 days is a return; a daily volatility scales with $\sqrt{252}$, a fact 1.5 proves).

**Level E6: Inequalities** (`lvl.expreq.inequalities`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 29 | `lsn.expreq.inequality-notation` Inequalities, intervals and sets | Show inequalities on a number line, in interval notation and in set notation, and list the integers satisfying a double inequality | A note pays out if an index ends above 100 but not above 120. Mark every value that pays | `number-line` (intervals), `card-sort` | Trap: open and closed ends confused; for $-2 < n \le 3$ including $-2$ or excluding 3. Edge: $(a, b]$ with $a > b$ is empty | I, N, S, C |
| 30 | `lsn.expreq.solve-inequalities` Solving linear inequalities | Solve linear inequalities and explain from the number line why multiplying or dividing by a negative reverses the sign | If $3 < 5$, is $-3 < -5$? | `number-line` (reflect), `balance-scale` (tilted), `equation-workbench` (solution strip) | Trap: not reversing when dividing by a negative; reversing when subtracting. Edge: you cannot multiply both sides by $x$ unless you know its sign | I, I, C, N |
| 31 | `lsn.expreq.compound-inequalities` Double and compound inequalities | Solve double inequalities and combine conditions with "and" and "or" as intersections and unions of intervals | Solve $-3 < 2x + 1 \le 7$ in one go | `number-line` (intervals), `card-sort` | Trap: treating "or" as "and". Edge: "$x < 2$ or $x > 5$" cannot be written as one double inequality; $5 < x < 2$ is empty | I, I, C, I |
| 32 | `lsn.expreq.absolute-value` Absolute value equations and inequalities | Solve equations and inequalities in $\lvert x - a \rvert$ by reading them as distances from $a$ on the number line | A fill must be within 0.05 of the quoted price 101.20. Write every acceptable fill as one inequality | `number-line` (distance), `equation-workbench` | Trap: $\lvert x - 3 \rvert = 5$ giving only $x = 8$; $\lvert x \rvert > 4$ written as $-4 < x < 4$. Edge: $\lvert x - 3 \rvert = -1$ has no solution | I, I, N, C |
| 33 | `lsn.expreq.two-variable-inequalities` Inequalities in two variables | Shade the region satisfying several linear inequalities and find the corner that maximises a linear objective | Cakes take 1 hour and £4 of ingredients; pies take 2 hours and £2. With 10 hours and £28, and profits of £5 and £4, what mix earns most? | `inequality-regions`, `graph-explorer` | Trap: shading the wrong side; checking only the corners on the axes. Edge: when the best corner is not a whole number, the best whole-number plan need not be the nearest whole point | P, C, N, M |
| 34 | `lsn.expreq.reasoning-inequalities` Reasoning with inequalities | Decide which operations preserve an inequality (adding, multiplying by a positive, squaring non-negatives, reciprocals of same-sign numbers) and justify each with an argument or a counterexample | If $a < b$, must $a^2 < b^2$? Must $\frac{1}{a} > \frac{1}{b}$? | `number-line`, `card-sort` (always, sometimes, never) | Trap: squaring both sides with negatives ($-3 < 2$ but $9 > 4$). Edge: reciprocals reverse only for numbers of the same sign ($-1 < 2$ and $-1 < \frac{1}{2}$) | S, N, C, M |

Transfer screens: lesson 32 is a tolerance band on a fill price; lesson 33 allocates capital under a risk budget, the first linear programme.

#### Course L: Lines and Linear Systems (`crs.lines`, 3 levels, 20 lessons)

The graph of an equation, gradient as a rate, and systems of linear equations up to three unknowns. It ends with the first piece of finance theory: pricing by replication.

**Level L1: Coordinates and straight lines** (`lvl.lines.straight`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 35 | `lsn.lines.coordinates` Coordinates and the graph of an equation | Plot points in four quadrants from a table and explain that a graph is the set of all points whose coordinates satisfy its equation | Which of $(2, 5)$, $(-1, -1)$ and $(3, 6)$ lie on $y = 2x + 1$, without drawing anything? | `graph-explorer` (points with linked table), `value-table` | Trap: $(x, y)$ read as $(y, x)$; the plotted points mistaken for the whole graph. Edge: $x = 3$ is a line too, though it has no $y$ in it | P, M, N, C |
| 36 | `lsn.lines.gradient` Gradient | Compute a gradient from any two points as change in $y$ over change in $x$, and interpret its sign and size | One ramp rises 3 m over 12 m, another 1 m over 5 m. Which is steeper? | `graph-explorer` (slope triangle), `drag-point` | Trap: run over rise; subtracting coordinates in a different order on top and bottom. Edge: a vertical line has no gradient; a horizontal line has gradient 0 | N, N, C, N |
| 37 | `lsn.lines.y-mx-c` The equation $y = mx + c$ | Read the gradient and $y$-intercept from $y = mx + c$ and from rearranged forms, and sketch the line | Drag the line until it passes through $(0, 3)$ with gradient $-2$. Which equation appears? | `graph-explorer`, `slider` | Trap: $y = 3 - 2x$ read as $m = 3$; $2y = 4x + 6$ read as $m = 4$. Edge: $x = 4$ cannot be written as $y = mx + c$ | N, N, P, C |
| 38 | `lsn.lines.line-equation` Finding the equation of a line | Find a line's equation from a point and a gradient, or from two points, using $y - y_1 = m(x - x_1)$, and convert between forms | A line passes through $(2, 7)$ and $(5, 13)$. Where does it cross the $y$-axis? | `graph-explorer`, `equation-workbench` | Trap: taking $c$ as a given point's $y$-coordinate. Edge: two points with the same $x$ give a vertical line, so the gradient formula divides by zero | X, X, N, C |
| 39 | `lsn.lines.parallel-perpendicular` Parallel and perpendicular lines | Identify parallel lines by equal gradients and derive $m_1 m_2 = -1$ for perpendicular lines by rotating a slope triangle | Rotate a line of gradient $\frac{2}{3}$ through a quarter turn. What is the new gradient? | `graph-explorer` (rotate), `derivation-steps` | Trap: the perpendicular gradient as $-\frac{2}{3}$ or $\frac{3}{2}$. Edge: horizontal and vertical lines are perpendicular, yet $m_1 m_2 = -1$ cannot be applied | N, X, C, M |
| 40 | `lsn.lines.midpoint-distance` Midpoint and distance | Find the midpoint and length of a segment from its endpoints, deriving the distance formula from Pythagoras | How far is $(-1, 2)$ from $(5, 10)$ as the crow flies? | `graph-explorer` (right-triangle overlay) | Trap: midpoint as $\frac{x_2 - x_1}{2}$; adding before squaring. Edge: the order of the points does not matter, because squaring removes the sign | N, N, X, C |
| 41 | `lsn.lines.sequences` Arithmetic sequences and the $n$th term | Find and use the $n$th term of an arithmetic sequence and explain it as a linear function of whole numbers | Is 500 a term of $7, 13, 19, 25, \ldots$? | `value-table`, `graph-explorer` (discrete points) | Trap: $n$th term written $n + 6$. Edge: a decreasing sequence $20, 17, 14, \ldots$ is $23 - 3n$; its graph is points on a line, not the line | X, N, C, N |

Transfer screens: lesson 36 reads a price chart's slope as pounds per day; lesson 41 is a linear fee schedule by trade count.

**Level L2: Linear graphs in the world** (`lvl.lines.models`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 42 | `lsn.lines.rate-of-change` Gradient as a rate of change | Interpret a linear graph's gradient and intercept, with units, in context | A phone plan's cost graph passes through $(0, 12)$ and $(300, 27)$ (minutes, £). What do 12 and the gradient mean? | `graph-explorer`, `unit-chain` | Trap: a gradient with no units. Edge: a negative gradient is a rate of decrease (depreciation in £ per year) | N, C, N, C |
| 43 | `lsn.lines.motion-graphs` Distance-time and speed-time graphs | Read speed from a distance-time gradient and distance from the area under a speed-time graph, using trapezia for straight pieces | A car goes from 0 to 20 m/s in 10 s, then cruises for 30 s. How far does it go? | `graph-explorer` (trapezia overlay) | Trap: a distance-time graph's height read as speed. Edge: a flat distance-time piece means stopped; a flat speed-time piece means steady speed | N, N, C, N |
| 44 | `lsn.lines.piecewise-linear` Piecewise linear graphs: tariffs and tax bands | Build and read piecewise linear functions and distinguish a marginal rate from an average rate | Income tax is 0% on the first £10,000 and 20% above it (a stylised schedule). Can a pay rise ever leave you with less after tax? | `graph-explorer`, `value-table` | Trap: all income taxed at the top marginal rate. Edge: the tax graph is continuous with kinks, so take-home pay never falls; a cliff-edge benefit withdrawal (a jump) can make it fall | N, N, C, N |
| 45 | `lsn.lines.proportional-graphs` Proportional or just linear? | Decide from a table, graph or equation whether a relationship is proportional ($y = kx$) or linear with an intercept | A taxi charges £3 plus £2 per mile. Does a 10-mile trip cost twice a 5-mile trip? | `graph-explorer`, `double-number-line` | Trap: every straight line is a proportion. Edge: Celsius to Fahrenheit is linear but not proportional, so 20 °C is not "twice as hot" as 10 °C | M, C, N, C |
| 46 | `lsn.lines.fit-line` Fitting a line to data | Fit a line by eye to a scatter, compute residuals, and explain why extrapolation far beyond the data is unsafe | Drag a line through 12 points so that the total area of the squares on the residuals is as small as you can make it | `scatter-fit`, `graph-explorer` | Trap: forcing the line through the origin, or through the first and last points. Edge: one outlier can drag a squared-error line a long way | N, C, P, C |
| 47 | `lsn.lines.reading-graphs` Reading graphs critically | Detect misleading choices (truncated axes, unequal scales, cumulative against per-period values) and read a logarithmic price axis | Two charts of the same share price: one looks like a crash, the other like a wobble. Which axis choice does it? | `graph-explorer` (axis controls: truncated and log axes, per-period and cumulative views) | Trap: judging a change by its height on a truncated axis. Edge: on a logarithmic axis equal percentage moves look equal, so steady 10% growth is a straight line | C, N, M, N |

Transfer screens: lesson 44 previews option payoffs (a kink at the strike, in F1); lesson 46 is the first regression line (1.6); lesson 47 reads a long-run index chart.

**Level L3: Simultaneous linear equations** (`lvl.lines.systems`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 48 | `lsn.lines.two-unknowns` Two equations, two unknowns | Explain why one linear equation in two unknowns has infinitely many solutions and find the unique solution of two as the intersection of their lines | Two coffees and a croissant cost £8.10; one coffee and two croissants cost £7.20. What does each cost? | `graph-explorer`, `value-table` (guess table) | Trap: thinking one equation is enough. Edge: the solutions of one equation form a whole line; the second equation picks one point on it | P, N, C, N |
| 49 | `lsn.lines.elimination` Elimination | Solve a pair of equations by scaling and adding or subtracting to eliminate one unknown, and explain why the new equation's line passes through the same intersection | Solve $3x + 2y = 16$ and $5x - 2y = 8$ in two moves | `equation-stack`, `graph-explorer` | Trap: subtracting when the signs call for adding; scaling one side of an equation only. Edge: any combination of the two equations is a new line through the same point, which is why elimination cannot lose the solution | N, N, N, C |
| 50 | `lsn.lines.substitution` Substitution | Solve a system by substitution and choose between substitution and elimination from the form of the equations | $y = 2x - 1$ and $3x + 4y = 18$: which method is quicker here? | `equation-stack` (substitute), `equation-workbench` | Trap: substituting without brackets ($3x + 4 \cdot 2x - 1$). Edge: substitute for the variable with coefficient 1 to avoid fractions | N, N, C, N |
| 51 | `lsn.lines.forming-systems` Forming simultaneous equations | Model a two-quantity word problem as a pair of linear equations, solve, and check against the story | A fund holds a bond yielding 3% and a share yielding 7%. £10,000 in total earns £540 a year. How much is in each? | `bar-model`, `equation-stack` | Trap: percentages as whole numbers ($3b + 7s = 540$). Edge: check that both amounts are non-negative before reporting | X, N, N, C |
| 52 | `lsn.lines.special-systems` No solution and infinitely many | Classify a system as having one, none or infinitely many solutions from its gradients and intercepts and from $ad - bc$ | Solve $2x + 3y = 6$ and $4x + 6y = 15$. What happens, and what do the lines look like? | `graph-explorer`, `equation-stack` | Trap: reading $0 = 3$ as "$x = 0$". Edge: $ad - bc = 0$ for $ax + by = e$, $cx + dy = f$ signals no solution or infinitely many, never exactly one | S, C, N, C |
| 53 | `lsn.lines.three-unknowns` Three equations, three unknowns | Solve a $3 \times 3$ system by systematic elimination to triangular form and back substitution | One share each of A, B and C is worth £6; two of A and one of C, less one of B, £3; one of A and two of B, less one of C, £2. Price each share | `equation-stack` (three variables), `value-table` (the coefficients as a table, the preview of a matrix) | Trap: eliminating a different unknown from each pair, so two equations in the same two unknowns never appear. Edge: three planes can meet in a point, along a line, or not at all | N, N, O, C |
| 54 | `lsn.lines.replication` Replicating a payoff | Find the holdings of a share and a bond that replicate a payoff in two future states by solving a $2 \times 2$ system, and price the payoff by no-arbitrage | A share costs £100 and will be worth £120 or £90. A bond costs £100 and pays £105. A contract pays £20 if the share goes up and nothing if it goes down. What should it cost? | `equation-stack`, `graph-explorer` | Trap: pricing by expected payoff with guessed real-world probabilities. Edge: the bond holding is negative (borrowing), which is allowed; the answer, £$\frac{200}{21} \approx 9.52$, does not depend on how likely the up move is | N, N, C, X |

Transfer screens: lesson 51 is a portfolio's income; lesson 53 previews Gaussian elimination (1.4); lesson 54 is the one-period binomial model (1.7).

#### Course Q: Quadratics and Polynomials (`crs.quadpoly`, 6 levels, 33 lessons)

Factorising, completing the square, the formula and its derivation, parabolas and circles, optimisation without calculus, polynomials and complex numbers.

**Level Q1: Factorising quadratics** (`lvl.quadpoly.factorising`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 55 | `lsn.quadpoly.factorise-simple` Factorising $x^2 + bx + c$ | Factorise monic quadratics by finding two numbers with the right sum and product, and confirm by arranging tiles into a rectangle | Arrange one $x^2$ tile, seven $x$ tiles and twelve unit tiles into one rectangle. What are its sides? | `algebra-tiles`, `expression-input` | Trap: $x^2 - x - 12 = (x - 3)(x + 4)$ (correct $(x - 4)(x + 3)$). Edge: $x^2 + 5x + 7$ has no integer pair; not every quadratic factorises over the integers | X, X, X, C |
| 56 | `lsn.quadpoly.factorise-general` Factorising $ax^2 + bx + c$ | Factorise non-monic quadratics by splitting the middle term using the product $ac$, and explain why the method works | Factorise $6x^2 + 11x - 10$. Guessing takes a while; is there a system? | `algebra-tiles`, `area-model` (symbolic), `expression-input` | Trap: forgetting $a$ when testing pairs. Edge: take out a common factor first: $4x^2 + 10x + 4 = 2(2x + 1)(x + 2)$ | X, X, X, C |
| 57 | `lsn.quadpoly.difference-squares` Difference of two squares and perfect squares | Recognise and factorise $a^2 - b^2$ and perfect-square trinomials, including in disguise | Factorise $x^4 - 1$ completely | `area-model` (cut and move), `expression-input` | Trap: $x^2 + 9 = (x + 3)(x - 3)$; stopping at $(x^2 + 1)(x^2 - 1)$. Edge: $x^2 + 9$ does not factorise over the real numbers | X, X, C, X |
| 58 | `lsn.quadpoly.solve-factorising` Solving by factorising | Solve quadratics by rearranging to zero, factorising and applying the zero-product property, and explain why the right side must be zero | Solve $(x - 2)(x - 3) = 6$. Are 8 and 9 the answers? | `equation-workbench`, `graph-explorer` | Trap: setting each factor equal to 6. Edge: dividing $x^2 = 5x$ by $x$ loses the root $x = 0$ | I, I, C, N |
| 59 | `lsn.quadpoly.quadratic-contexts` Quadratic equations from contexts | Form a quadratic from an area, number or motion problem, solve it, and reject solutions that make no sense | A lawn is 3 m longer than it is wide and has area $40\text{ m}^2$. How wide is it? | `area-model`, `equation-workbench` | Trap: keeping the negative root. Edge: sometimes both roots are valid (a ball passes a given height going up and coming down) | N, X, N, C |
| 60 | `lsn.quadpoly.factorise-fully` Factorising fully and quadratics in disguise | Factorise completely, use substitution for quadratics in $x^2$, and simplify algebraic fractions with quadratic parts | Solve $x^4 - 5x^2 + 4 = 0$ | `equation-workbench`, `expression-input` | Trap: forgetting to undo the substitution, or losing the negative roots. Edge: $\frac{x^2 - 9}{x^2 + 5x + 6} = \frac{x - 3}{x + 2}$ only for $x \ne -3$ | I, X, X, C |

Transfer screens: lesson 59 finds the break-even volumes of a profit model in which selling more forces the price down, so profit is quadratic in volume.

**Level Q2: Completing the square and the formula** (`lvl.quadpoly.formula`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 61 | `lsn.quadpoly.complete-square` Completing the square | Rewrite $x^2 + bx + c$ as $\left(x + \frac{b}{2}\right)^2 + q$ by completing a square of tiles, and extend to $ax^2 + bx + c$ | One $x^2$ tile and six $x$ tiles: arrange them into as much of a square as you can. How many unit tiles complete it? | `algebra-tiles` (complete the square), `area-model` (symbolic) | Trap: $x^2 + 6x = (x + 3)^2$, forgetting the $-9$. Edge: odd $b$ gives fractions: $x^2 + 5x = \left(x + \frac{5}{2}\right)^2 - \frac{25}{4}$ | X, X, X, C |
| 62 | `lsn.quadpoly.vertex-form` Vertex form and the minimum value | Read the minimum or maximum and the turning point of a quadratic from its completed-square form, and explain why a square is never negative | What is the smallest value $x^2 - 6x + 11$ can take, and for which $x$? | `graph-explorer` (vertex form), `slider` | Trap: turning point at $(-3, 2)$. Edge: with a negative leading coefficient the turning point is a maximum | N, P, X, C |
| 63 | `lsn.quadpoly.solve-complete-square` Solving by completing the square | Solve quadratics by completing the square, giving exact surd answers and both roots | $x^2 + 6x + 2 = 0$ does not factorise. Solve it exactly | `equation-workbench` | Trap: taking only the positive square root. Edge: $(x + 3)^2 = -2$ has no real solution | X, X, I, C |
| 64 | `lsn.quadpoly.formula` Deriving the quadratic formula | Derive the quadratic formula by completing the square on $ax^2 + bx + c = 0$ and use it on any quadratic | Completing the square worked for $x^2 + 6x + 2 = 0$. Can we do it once, for every quadratic at the same time? | `derivation-steps` (predict each line), `equation-workbench` | Trap: dividing only the root by $2a$; the sign of $-b$ when $b$ is negative. Edge: $\sqrt{4a^2} = 2\lvert a \rvert$, and the $\pm$ absorbs the sign, so the formula holds for negative $a$ | O, X, N, C |
| 65 | `lsn.quadpoly.discriminant` The discriminant | Use $b^2 - 4ac$ to decide how many real roots a quadratic has and find parameter values that give equal roots | Drag $k$ to lift the parabola $y = x^2 - 4x + k$. At what $k$ do the two roots merge? | `graph-explorer`, `slider` | Trap: computing $b^2$ as negative when $b$ is negative. Edge: "no real roots" is not "no roots" (Q6) | S, N, I, C |
| 66 | `lsn.quadpoly.choose-method` Choosing a method | Choose the most efficient method (inspection, factorising, completing the square, formula, graph) for a quadratic and justify the choice | Four quadratics, one minute. Which would you never use the formula on? | `card-sort`, `equation-workbench` | Trap: always reaching for the formula. Edge: $x^2 - 49 = 0$ and $x(x - 3) = 0$ need no method at all | S, X, N, C |

Transfer screens: lesson 62 is the minimum of a cost curve; lesson 64 links to 3Blue1Brown's "simpler quadratic formula" (roots as $m \pm d$) for the curious.

**Level Q3: Quadratic graphs, circles and systems** (`lvl.quadpoly.graphs`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 67 | `lsn.quadpoly.parabola-family` The parabola family | Describe how $a$, $h$ and $k$ in $y = a(x - h)^2 + k$ change a parabola and identify its axis of symmetry | Drag $a$, $h$ and $k$ until the parabola passes through three given points | `graph-explorer` (vertex form), `slider` | Trap: $(x - 3)^2$ moves left. Edge: three points with different $x$ values, not on one line, fix exactly one parabola | P, C, N, M |
| 68 | `lsn.quadpoly.sketch-quadratic` Sketching quadratics from features | Sketch any quadratic from its roots, $y$-intercept, turning point and axis $x = -\frac{b}{2a}$ | Sketch $y = 2x^2 - 8x + 6$ without a table of values | `sketch-pad`, `graph-explorer` | Trap: the axis at $x = \frac{b}{2a}$. Edge: with no real roots, sketch from the vertex, the $y$-intercept and its mirror image | P, N, N, C |
| 69 | `lsn.quadpoly.roots-coefficients` Roots and coefficients | Use the sum $-\frac{b}{a}$ and product $\frac{c}{a}$ of the roots to check answers, build quadratics with given roots, and evaluate symmetric expressions of the roots without solving | The roots of $x^2 - 7x + 3 = 0$ are $\alpha$ and $\beta$. Find $\alpha^2 + \beta^2$ without finding $\alpha$ or $\beta$ | `equation-workbench`, `derivation-steps`, `graph-explorer` | Trap: the sum of the roots as $b$; $\alpha^2 + \beta^2 = (\alpha + \beta)^2$. Edge: the method works even when the roots are not real | N, X, N, C |
| 70 | `lsn.quadpoly.quadratic-inequalities` Quadratic inequalities | Solve quadratic inequalities from the roots and the sign of the quadratic, read from its graph or a sign chart | For which $x$ is $x^2 < 9$? A classmate writes $x < \pm 3$. What could that even mean? | `sign-chart`, `graph-explorer` | Trap: $x < \pm 3$; $(x - 1)(x - 4) > 0$ answered as $1 < x < 4$. Edge: $x^2 + 1 > 0$ for every $x$; $x^2 \le 0$ only at $x = 0$ | I, I, C, I |
| 71 | `lsn.quadpoly.linear-quadratic` Where a line meets a curve | Solve a line-and-quadratic system by substitution and use the discriminant to decide whether the line misses, touches or cuts the curve | For which $c$ does $y = 2x + c$ touch $y = x^2$? | `equation-stack` (substitute), `graph-explorer` | Trap: forgetting the $y$ values, or pairing them with the wrong $x$. Edge: a vertical line always meets $y = f(x)$ exactly once | N, I, C, N |
| 72 | `lsn.quadpoly.circles` Circles | Write and read $(x - a)^2 + (y - b)^2 = r^2$, find the centre and radius by completing the square, and find the tangent at a point from the perpendicular radius | Is $(5, 3)$ inside, on or outside the circle $x^2 + y^2 - 4x + 2y = 20$? | `graph-explorer` (circle family, tangent), `equation-workbench` | Trap: radius 25 instead of 5; centre $(-2, 1)$ instead of $(2, -1)$. Edge: $x^2 + y^2 + 2x + 10 = 0$ is no circle at all ($r^2 = -9$) | N, X, C, X |

Transfer screens: lesson 69 is a staple interview manipulation; lesson 72 is the GCSE tangent question.

**Level Q4: Optimising with quadratics** (`lvl.quadpoly.optimising`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 73 | `lsn.quadpoly.revenue` Maximising revenue | Build a quadratic revenue model from a linear demand rule and find the revenue-maximising price by completing the square | At £10 a ticket you sell 500; each £1 rise loses 20 sales. What price maximises takings? | `graph-explorer`, `value-table`, `slider` | Trap: maximising sales instead of revenue. Edge: if the best price lies outside the allowed range, the best allowed price is at the boundary | N, N, X, C |
| 74 | `lsn.quadpoly.max-area` Fixed fence, largest area | Show by completing the square that a fixed perimeter encloses the most area as a square, and solve fencing problems with a wall | 40 m of fence and a long wall for one side: what is the largest rectangle you can enclose? | `graph-explorer`, `area-model`, `slider` | Trap: "the answer is always a square" (with the wall it is 10 m by 20 m). Edge: without the wall, the square wins | N, N, C, N |
| 75 | `lsn.quadpoly.least-squares-1d` The number that best fits a list | Show by completing the square that $\sum (x_i - c)^2$ is smallest when $c$ is the mean, and compute the minimum | Measurements 2, 3, 5, 7, 8. Which single number $c$ makes $\sum (x_i - c)^2$ as small as possible? | `slider`, `graph-explorer` (loss parabola), `dot-plot-stats` | Trap: the median minimises squared error (it minimises absolute error). Edge: with absolute error and an even count, every point between the two middle values is a minimiser | N, N, C, X |
| 76 | `lsn.quadpoly.variance-identity` Spread: the sum-of-squares identity | Derive $\sum (x_i - \bar{x})^2 = \sum x_i^2 - n\bar{x}^2$ with sigma algebra and use it to compute a spread | Compute $\sum (x_i - \bar{x})^2$ for 2, 3, 5, 7, 8 two ways. Which would a computer prefer for a million numbers, and is it always safe? | `value-table`, `derivation-steps`, `code-cell` | Trap: dropping the $n$ ($\sum x_i^2 - \bar{x}^2$). Edge: for $10^9 + 0.1$, $10^9 + 0.2$, $10^9 + 0.3$ the shortcut subtracts two nearly equal numbers near $3 \times 10^{18}$ and Python returns $-1024$; the true value is $0.02$ | N, O, X, C |
| 77 | `lsn.quadpoly.never-negative` Squares are never negative: AM-GM | Prove $\frac{a + b}{2} \ge \sqrt{ab}$ for non-negative $a$ and $b$ from $(\sqrt{a} - \sqrt{b})^2 \ge 0$, state the equality case, and use it to find minima | For positive $x$, how small can $x + \frac{1}{x}$ get? | `derivation-steps`, `graph-explorer`, `area-model` (four rectangles in a square) | Trap: ignoring the positivity condition ($x = -1$ gives $-2$). Edge: equality holds only when $a = b$; checking that case is part of the proof | N, O, C, N |

Transfer screens: lesson 75 is least squares and ML's squared-error loss in one dimension; lesson 76 is the variance shortcut (1.5) and its numerical trap, which NumPy's `var` avoids by subtracting the mean first; lesson 77 is the inequality behind many interview "minimise" questions.

**Level Q5: Polynomials** (`lvl.quadpoly.polynomials`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 78 | `lsn.quadpoly.polynomial-arithmetic` Polynomials and their arithmetic | Add, subtract and multiply polynomials, state degree and leading coefficient, and find one coefficient of a product without full expansion | What is the coefficient of $x^3$ in $(2x^2 - x + 3)(x^2 + 4x - 1)$, without expanding everything? | `area-model` (polynomial grid), `expression-input` | Trap: degree of a product as the product of the degrees. Edge: leading terms can cancel in a sum, lowering the degree | N, X, N, C |
| 79 | `lsn.quadpoly.polynomial-division` Polynomial division | Divide a polynomial by a linear or quadratic divisor with long division, writing $f(x) = d(x)q(x) + r(x)$ | Divide $x^3 - 2x^2 - 5x + 6$ by $x - 3$, step by step beside the long division $1{,}326 \div 13$ | `written-method` (polynomial division) | Trap: missing placeholder terms when dividing $x^3 + 1$. Edge: the remainder's degree is always below the divisor's | X, X, C, N |
| 80 | `lsn.quadpoly.factor-theorem` The factor and remainder theorems | Derive the remainder theorem from $f(x) = (x - a)q(x) + r$ and use it to find remainders and factors without dividing | What is the remainder when $x^{100} + 1$ is divided by $x + 1$? | `derivation-steps`, `graph-explorer` (slider testing candidate roots) | Trap: evaluating at $1$ instead of $-1$ for the divisor $x + 1$. Edge: for the divisor $2x - 1$, evaluate at $\frac{1}{2}$ | N, N, C, N |
| 81 | `lsn.quadpoly.cubics` Solving cubic equations | Find a first root of a cubic from the candidates $\pm\frac{p}{q}$, factorise completely and solve | Solve $2x^3 - 3x^2 - 11x + 6 = 0$ | `written-method`, `graph-explorer`, `equation-workbench` | Trap: testing only whole-number candidates when the leading coefficient is not 1 (missing $\frac{1}{2}$). Edge: a real cubic always has at least one real root; the other two may be complex | I, X, C, N |
| 82 | `lsn.quadpoly.polynomial-graphs` Polynomial graphs: roots, multiplicity and end behaviour | Sketch a factorised polynomial from its roots, their multiplicities and the sign of its leading term, and match polynomials to graphs | Sketch $y = (x + 2)(x - 1)^2$. Does the graph cross the axis at 1? | `sketch-pad`, `graph-explorer`, `card-sort` | Trap: every root is a crossing. Edge: a triple root crosses and flattens, like $y = x^3$ at 0 | S, P, C, N |
| 83 | `lsn.quadpoly.finite-differences` Finding the rule: finite differences | Find the $n$th term of a quadratic sequence from constant second differences and explain why constant $k$th differences mean a degree-$k$ rule | Find the $n$th term of $3, 8, 15, 24, 35, \ldots$, then of the triangular numbers $1, 3, 6, 10, \ldots$ | `value-table` (difference rows), `equation-workbench` | Trap: the coefficient of $n^2$ equal to the second difference (it is half). Edge: three terms fit many rules: $1, 2, 4$ continues as 8 for $2^{n-1}$ but as 7 for $\frac{n^2 - n + 2}{2}$ | X, X, N, C |

Transfer screens: lesson 78 multiplies $(x + x^2 + \cdots + x^6)$ by itself and reads the coefficients as the number of ways to roll each total with two dice, the counting trick 1.5 reuses; lesson 83 shows why "what comes next" puzzles need a stated rule.

**Level Q6: Complex numbers** (`lvl.quadpoly.complex`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 84 | `lsn.quadpoly.meet-i` When the discriminant is negative | Define $i$ by $i^2 = -1$, write square roots of negative numbers with $i$, and solve quadratics with a negative discriminant | In 1545 Cardano looked for two numbers that add to 10 and multiply to 40. Try it | `graph-explorer` (parabola above the axis), `equation-workbench` | Trap: $\sqrt{-4} \times \sqrt{-9} = \sqrt{36} = 6$ (correct $-6$). Edge: $\sqrt{a}\sqrt{b} = \sqrt{ab}$ fails when both are negative, the rule's limit flagged in 0.1 lesson 35 | X, X, C, N |
| 85 | `lsn.quadpoly.complex-arithmetic` Arithmetic with complex numbers | Add, subtract, multiply and divide complex numbers in the form $a + bi$, dividing with the conjugate | Compute $(2 + 3i)(4 - i)$ and $\frac{1}{2 + 3i}$ | `expression-input`, `complex-plane` | Trap: multiplying part by part ($8 - 3i$). Edge: $z\bar{z} = a^2 + b^2$ is real and never negative, which is why the conjugate clears a denominator | X, X, X, C |
| 86 | `lsn.quadpoly.complex-plane` The complex plane | Plot complex numbers as points, read addition as vector addition, find the modulus, and see multiplication by $i$ as a quarter turn | Multiply $3 + 2i$ by $i$, then by $i$ again, and again. Plot each result. What shape appears? | `complex-plane` | Trap: $\lvert 3 + 4i \rvert = 7$; $i$ turning clockwise. Edge: complex numbers have no order; "$3 + 2i > 1 + i$" means nothing | P, N, C, X |
| 87 | `lsn.quadpoly.conjugate-roots` Complex roots come in pairs | Show that the non-real roots of a real quadratic are conjugates, check them with the sum and product, and build a real quadratic from one complex root | One root of a real quadratic is $3 + 2i$. Find the quadratic | `complex-plane`, `equation-workbench` | Trap: the other root as $-(3 + 2i)$; the product as $9 - 4 = 5$. Edge: with non-real coefficients the pairing fails: $z^2 - iz = 0$ has roots 0 and $i$ | X, N, C, X |

Transfer screens: lesson 86 previews rotation, which returns in 1.4 (eigenvalues) and in signal processing.

#### Course F: Functions and Graphs (`crs.funcs`, 4 levels, 24 lessons)

Functions as objects: notation, domain and range, composition and inverses, a gallery of graph shapes, transformations, and numerical ways to solve equations and to measure rates and areas. The last level previews calculus without its notation.

**Level F1: Functions** (`lvl.funcs.functions`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 88 | `lsn.funcs.what-is-function` What a function is | Decide whether a rule, table, mapping or graph defines a function (exactly one output per input) and apply the vertical line test | A vending machine gives a random snack each time you press B4. Is it a function? | `function-machine`, `card-sort`, `graph-explorer` | Trap: many-to-one is "not a function" (it is); a circle is a function (it is not). Edge: a constant function sends every input to the same output and is still a function | S, M, C, P |
| 89 | `lsn.funcs.notation` Function notation | Evaluate and interpret $f(a)$, $f(a + h)$, $f(x) + k$ and $f(kx)$, and solve $f(x) = c$ | If $f(x) = x^2 - 3x$, are $f(x + 1)$ and $f(x) + 1$ the same? | `function-machine`, `expression-input` | Trap: $f(x + 1) = f(x) + f(1)$; $f(2x) = 2f(x)$. Edge: for a linear $f(x) = mx$ the trap rules happen to hold, which is exactly what makes a function linear | N, X, X, C |
| 90 | `lsn.funcs.domain-range` Domain and range | Find a function's natural domain from the operations it uses and its range from its graph or completed square, in interval notation | Feed $-4$, 0 and 9 into the machine $f(x) = \frac{1}{\sqrt{x}}$. Which inputs are rejected, and why? | `function-machine`, `graph-explorer`, `number-line` (intervals) | Trap: including 0 in the domain of $\frac{1}{\sqrt{x}}$; the range of $x^2 + 1$ as every real number. Edge: a context can shrink the domain (a price or a height cannot be negative) | I, I, C, I |
| 91 | `lsn.funcs.composition` Composite functions | Form and evaluate $f(g(x))$, show that order matters, and split a given function into a composition | A price is converted from dollars to pounds and then 20% VAT is added. Does the order matter? What if a £5 fee replaces the VAT? | `function-machine` (compose), `expression-input` | Trap: $fg(x)$ read as $f(x) \times g(x)$, or $f$ applied first. Edge: the domain of $f(g(x))$ drops every $x$ whose $g(x)$ is outside $f$'s domain: $\sqrt{x - 4}$ needs $x \ge 4$ | N, X, X, C |
| 92 | `lsn.funcs.inverse` Inverse functions | Find the inverse of a one-to-one function by reversing its steps or swapping and solving, sketch it as a reflection in $y = x$, and restrict a domain so an inverse exists | Celsius to Fahrenheit is $f(C) = \frac{9}{5}C + 32$. Build the machine that goes back | `function-machine` (inverse), `graph-explorer` (reflect in $y = x$) | Trap: $f^{-1}(x) = \frac{1}{f(x)}$. Edge: $x^2$ has no inverse on all real numbers; restricted to $x \ge 0$ its inverse is $\sqrt{x}$ | X, P, C, X |
| 93 | `lsn.funcs.modulus-piecewise` Piecewise functions and the modulus | Evaluate and graph piecewise functions, including $\lvert x \rvert$ and $\max(x - K, 0)$, and solve equations involving them | A call option pays $\max(S - 100, 0)$ at expiry. Sketch the payoff for prices from 50 to 150 | `graph-explorer` (piecewise mode, draggable strike), `sketch-pad` | Trap: the payoff going negative below the strike; $\lvert x - 2 \rvert$ shifted the wrong way. Edge: $\lvert x \rvert = \sqrt{x^2}$ and $\lvert a + b \rvert \le \lvert a \rvert + \lvert b \rvert$ | P, N, I, C |

Transfer screens: lesson 92 previews quantiles as an inverse (1.5); lesson 93 is the hockey-stick payoff (1.7).

**Level F2: A gallery of graphs** (`lvl.funcs.gallery`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 94 | `lsn.funcs.cubic-graphs` Cubic graphs | Recognise and sketch cubics from their roots and leading coefficient, including $y = x^3$ and its translations | Which of four sketches could be $y = x(x - 2)(x + 3)$? | `sketch-pad`, `card-sort`, `graph-explorer` | Trap: a cubic with a negative leading coefficient drawn rising on the right. Edge: $y = x^3$ is flat at 0 but has no turning point there | S, P, N, C |
| 95 | `lsn.funcs.reciprocal-graphs` Reciprocal graphs and asymptotes | Sketch $y = \frac{k}{x}$ and $y = \frac{k}{x^2}$, identify their asymptotes, and link them to inverse proportion | As $x$ moves towards 0 from the right, what happens to $\frac{1}{x}$? From the left? | `graph-explorer`, `value-table` | Trap: the curve crossing its asymptote at 0; $\frac{1}{x^2}$ drawn negative for negative $x$. Edge: $y = \frac{1}{x}$ is its own inverse, so its graph is symmetric in $y = x$ | P, C, N, M |
| 96 | `lsn.funcs.proportion-powers` Proportion with powers | Set up and solve $y = kx^n$ and $y = \frac{k}{x^n}$ from one data pair and predict the effect of scaling $x$ | Braking distance is proportional to the square of speed. If speed doubles, what happens to braking distance? | `graph-explorer`, `double-number-line`, `value-table` | Trap: doubling $x$ doubles $y$ for $y \propto x^2$. Edge: for $y \propto \sqrt{x}$, doubling $x$ multiplies $y$ by $\sqrt{2}$ | N, N, X, C |
| 97 | `lsn.funcs.exponential-graphs` Exponential graphs | Sketch $y = a^x$ for $a > 1$ and $0 < a < 1$, state the intercept and asymptote, and model growth and decay with $y = A b^x$ | A bacterium doubles every hour, starting from one. When does the count first pass 1,000? | `graph-explorer`, `multiplier-chain` | Trap: the graph crossing the $x$-axis; $2^x$ confused with $x^2$. Edge: $2^x$ and $x^2$ meet at $x = 2$, at $x = 4$ and once for a negative $x$ | P, N, C, M |
| 98 | `lsn.funcs.linear-vs-exponential` Linear against exponential growth | Tell arithmetic (constant difference) from geometric (constant ratio) sequences in a table and show that exponential growth eventually overtakes any linear growth | Offer A: £1,000 a day for 30 days. Offer B: 1p on day 1, doubling every day. Which do you take? | `multiplier-chain`, `graph-explorer`, `value-table` | Trap: the early leader wins (A leads for most of the month; B ends above £10 million in total). Edge: growth of 0.5% a day overtakes any fixed daily increment eventually | S, N, C, N |
| 99 | `lsn.funcs.rational-functions` Rational functions | Find the vertical and horizontal asymptotes and the intercepts of $y = \frac{ax + b}{cx + d}$, and tell an asymptote from a hole | Plot $y = \frac{x + 1}{x - 2}$. Where does it blow up, and what does it settle to far away? | `graph-explorer`, `value-table` | Trap: the horizontal asymptote taken as $y = 0$; $\frac{x^2 - 4}{x - 2}$ given an asymptote at 2 (it has a hole). Edge: a curve may cross its horizontal asymptote: $y = \frac{x}{x^2 + 1}$ crosses $y = 0$ at the origin | N, N, C, P |
| 100 | `lsn.funcs.match-graphs` Recognising graphs | Match equations to graphs by testing intercepts, asymptotes, symmetry, end behaviour and sign, and choose a model family for a data set | Eight graphs, eight equations: match them without plotting | `card-sort` (match), `graph-explorer` | Trap: matching on one feature. Edge: two equations can share intercepts and asymptotes; test one more point | S, S, C, M |

Transfer screens: lesson 98 is compounding against simple interest over a career; lesson 100 chooses linear, quadratic or exponential models for three short data sets.

**Level F3: Transformations and symmetry** (`lvl.funcs.transformations`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 101 | `lsn.funcs.translations` Translations | Sketch $y = f(x) + a$ and $y = f(x + a)$ from the graph of $f$ and explain why the inside change moves the graph left for positive $a$ | Drag the parabola 3 units right. Which formula appears, $(x + 3)^2$ or $(x - 3)^2$? | `graph-explorer` (parent ghost, curve drag) | Trap: $f(x + 3)$ moves right. Edge: for a line, a horizontal shift can equal a vertical one: $y = 2x + 1$ moved right 1 is $y = 2x - 1$, the same as moving it down 2 | P, X, C, N |
| 102 | `lsn.funcs.stretches-reflections` Stretches and reflections | Sketch $af(x)$, $f(ax)$, $-f(x)$ and $f(-x)$ and describe each as a stretch or reflection with its factor and axis | Squash $y = x^2$ towards the $y$-axis by a factor 2. Is it $(2x)^2$ or $\left(\frac{x}{2}\right)^2$? | `graph-explorer` | Trap: $f(2x)$ as a horizontal stretch by 2 (it is a squeeze by $\frac{1}{2}$). Edge: for $y = x^2$, a horizontal squeeze by $\frac{1}{2}$ equals a vertical stretch by 4 | P, C, X, M |
| 103 | `lsn.funcs.combining-transformations` Combining transformations | Apply two or more transformations in a stated order, show that order can matter, and describe a vertex-form quadratic as transformations of $y = x^2$ | Stretch $y = x^2$ vertically by 2 then shift it up 3, or shift then stretch. Same curve? | `graph-explorer`, `function-machine` (compose) | Trap: ignoring order ($2x^2 + 3$ against $2x^2 + 6$). Edge: $f(2x + 6)$ is a left shift of 6 followed by a squeeze, or a squeeze followed by a left shift of 3 | P, O, X, C |
| 104 | `lsn.funcs.even-odd` Even and odd functions | Test whether a function is even, odd or neither from $f(-x)$ and from its graph's symmetry, and predict the parity of sums and products | Is $f(x) = x^3 - x$ symmetric about the $y$-axis, about the origin, or neither? | `graph-explorer` (reflect), `card-sort` | Trap: every function is even or odd; $x^3 + 1$ is odd. Edge: $f(x) = 0$ is both even and odd | S, C, M, N |
| 105 | `lsn.funcs.rescaling-data` Rescaling data: units and standard scores | Predict how the mean and spread of data change under $y = ax + b$ and convert values to standard scores $z = \frac{x - \bar{x}}{s}$ | Daily highs have mean 20 °C and spread 5 °C. What are the mean and spread in Fahrenheit? | `dot-plot-stats`, `graph-explorer`, `slider` | Trap: adding 32 changes the spread; the spread scales by $a^2$ (that is the variance). Edge: $a = -1$ flips the data and leaves the spread unchanged, because spread scales by $\lvert a \rvert$ | N, N, C, N |

Transfer screens: lesson 105 is feature standardisation before fitting a model (2.1) and z-scores in 1.5.

**Level F4: Solving equations with graphs, iteration and rates** (`lvl.funcs.solving`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 106 | `lsn.funcs.graphical-solutions` Solving equations graphically | Solve $f(x) = g(x)$ approximately from intersections and choose the line to draw on a given graph to solve a new equation | The graph of $y = x^2 - 2x$ is drawn. Which straight line would you add to solve $x^2 - 3x - 1 = 0$? | `graph-explorer` | Trap: reading the $y$-coordinates as solutions. Edge: a tangent line gives a repeated root, which a graph cannot tell from two close roots | X, N, C, N |
| 107 | `lsn.funcs.iteration` Iteration | Rearrange $f(x) = 0$ as $x = g(x)$, run $x_{n+1} = g(x_n)$, and use a cobweb diagram to predict convergence or divergence | Start at 1 and repeatedly add 2 and take the square root. Where does it settle, and why that number? | `iteration-cobweb`, `value-table` | Trap: every rearrangement converges. Edge: $x = x^2 - 2$ has the same fixed point 2, but the iteration runs away from it, because the curve is steeper than $y = x$ there | N, N, C, N |
| 108 | `lsn.funcs.bisection` Change of sign and bisection | Locate a root by a change of sign, halve the interval to a stated accuracy, and recognise when a sign change misleads | $x^3 + x - 3 = 0$ has a root between 1 and 2. Pin it to 2 decimal places in as few evaluations as possible | `graph-explorer`, `value-table`, `code-cell` | Trap: a sign change across an asymptote ($\frac{1}{x}$ on $[-1, 1]$) taken as a root. Edge: a double root shows no sign change at all | N, C, N, T |
| 109 | `lsn.funcs.chords-tangents` Gradient of a curve | Estimate the gradient of a curve at a point from shrinking chords and from a drawn tangent, and read it as an instantaneous rate | On $y = x^2$, the chord from $x = 1$ to $x = 1 + h$ has some gradient. Slide $h$ towards 0. What does it approach? | `graph-explorer` (chord and tangent overlays), `slider`, `value-table` | Trap: putting $h = 0$ straight in ($\frac{0}{0}$). Edge: at the corner of $\lvert x \rvert$ chords from the left and right give $-1$ and $1$, so there is no single gradient | N, X, N, C |
| 110 | `lsn.funcs.area-trapezia` Area under a curve | Estimate the area under a curve with trapezia, decide from the curve's shape whether the estimate is too big or too small, and interpret the area | Speed is $v = t^2$ for $0 \le t \le 4$. Estimate the distance with 4 trapezia. Too much or too little? | `graph-explorer` (trapezia overlay), `slider` | Trap: counting the end heights twice; judging over or under from whether the curve rises. Edge: for a curve that bends downwards, trapezia underestimate | N, C, N, C |
| 111 | `lsn.funcs.extraneous` Equations that lie: radical and rational equations | Solve equations with square roots and algebraic fractions, check every candidate in the original, and explain where extraneous roots come from | Solve $\sqrt{x + 3} = x - 3$ | `equation-workbench`, `graph-explorer` | Trap: keeping $x = 1$, which solves the squared equation only. Edge: clearing fractions can add a root too: $\frac{x^2 - 1}{x - 1} = 2$ leads to $x = 1$, which is excluded, so there is no solution | I, I, C, N |

Transfer screens: lesson 108 is the method that finds implied volatility in Stage 2 project 3; lesson 109 is the derivative (1.3) before its notation; lesson 110 is the integral (1.3) and the trapezium rule used in numerical pricing.

### 2.3 Coverage check

**The curriculum's cover lists.**

| Item | Cover term | Lessons |
|---|---|---|
| 0.1 | Fractions | 17 to 21, 22, 23 |
| 0.1 | Decimals | 1, 2, 5, 22, 23, 42 |
| 0.1 | Percentages | 24 to 26 |
| 0.1 | Ratio | 27 to 31 |
| 0.1 | Negatives | 6 to 8 |
| 0.1 | Powers | 32 to 34, 36 |
| 0.1 | Roots | 34, 35, 41 |
| 0.1 | Estimation | 38, 39, 40 |
| 0.1 | Added for a top programme | place value and written methods (1 to 5), laws of arithmetic (10), primes, counting and remainders (11 to 16), rounding and bounds (37, 39), irrationality proof (41), binary and floating point (42), weighted averages and average rates (31) |
| 0.2 | Expressions | 1 to 17 |
| 0.2 | Linear equations | 18 to 28 |
| 0.2 | Inequalities | 29 to 34, 70 |
| 0.2 | Simultaneous equations | 48 to 54, 71 |
| 0.2 | Quadratics | 55 to 77 |
| 0.2 | Functions | 88 to 93, 101 to 105 |
| 0.2 | Graphs | 35 to 47, 67 to 72, 82, 94 to 100, 106 to 110 |
| 0.2 | Added for a top programme | sigma notation (16), proof (17, 22), dimensional analysis (28), linear programming (33), replication (54), optimisation and least squares (73 to 77), polynomials and finite differences (78 to 83), complex numbers (84 to 87), rescaling data (105), numerical methods (107, 108), rates and areas (109, 110), extraneous roots (111) |

**GCSE Higher content** (DfE subject content 2013 codes; N11, N16, A25, R12, R15 and R16 confirmed by search [searched], the rest recalled [check]). Number (N), Algebra (A) and Ratio, proportion and rates of change (R) carry 65% of the in-app `gcse` paper's marks (52 of 80, `stage0-precalc-computing.md` 4.4) and all of it is taught here, except R12.

| Codes | Lessons |
|---|---|
| N1 to N3 (ordering, four operations, order of operations) | 0.1: 1 to 10, 17 to 21 |
| N4, N5 (primes, HCF, LCM, product rule for counting) | 0.1: 11 to 14, 13 |
| N6 to N9 (powers, roots, surds, standard form) | 0.1: 32 to 36 |
| N10 to N12 (terminating and recurring decimals, fractions in ratio problems, fractions and percentages as operators) | 0.1: 22 to 25, 27 |
| N13 to N16 (units, estimation, rounding, bounds) | 0.1: 30, 37 to 39 |
| A1 to A7 (notation, substitution, vocabulary, manipulation, formulae, identities and proof, functions) | 0.2: 1 to 17, 24 to 28, 88 to 92 |
| A8 to A10 (coordinates, straight lines, parallel and perpendicular) | 0.2: 35 to 40 |
| A11 to A13 (quadratic features, graph shapes, translations and reflections) | 0.2: 62, 67, 68, 94 to 97, 101, 102 |
| A14, A15 (real-life graphs, gradients and areas of non-linear graphs) | 0.2: 42 to 44, 109, 110 |
| A16 (circle at the origin and its tangent) | 0.2: 72 |
| A17 to A20 (linear, quadratic and simultaneous equations, iteration) | 0.2: 18 to 21, 48 to 51, 58 to 66, 71, 107 |
| A21 (forming equations) | 0.2: 21, 51, 59 |
| A22 (inequalities in one and two variables, quadratic inequalities, set notation) | 0.2: 29 to 33, 70 |
| A23 to A25 (sequences, $n$th terms of linear and quadratic sequences) | 0.2: 41, 83, 98. A24's triangular, square, cube and Fibonacci-type sequences were taught nowhere: they enter homework L1 through `gen.alg.special-sequences` (recognise, continue, give a term) and lesson 83's hook offers the triangular numbers as a second quadratic sequence |
| R1 to R8 (units, scale, one quantity as a fraction of another, ratio, ratio and fractions, ratio and linear functions) | 0.1: 17, 24, 27, 28, 30 |
| R9 (percentages, original value, simple interest) | 0.1: 24 to 26 |
| R10, R13, R14 (direct and inverse proportion, graphs of proportion) | 0.1: 28, 29; 0.2: 45, 95, 96 |
| R11 (compound units) | 0.1: 30 |
| R12 (similarity and scale factors) | Not here: 0.3 course S (`stage0-precalc-computing.md` decision 2, pending the owner) |
| R15 (instantaneous and average rate of change) | 0.2: 42, 109 |
| R16 (growth, decay, compound interest, iterative processes) | 0.1: 26; 0.2: 97, 98, 107 |

**Boundary with 0.3** (`stage0-precalc-computing.md` 0.2 lists what 0.3 inherits; this table fixes the topics its open item 1 left open).

| Topic | Taught here | 0.3 does |
|---|---|---|
| $n$th term of an arithmetic sequence | 0.2 lesson 41 | G1 recaps it in its hook; the sibling's `gcse` question 3 should cite lesson 41 |
| $n$th term of a quadratic sequence (GCSE A25) | 0.2 lesson 83, by second differences | Its lesson 41 becomes a recap, and the freed 15 minutes go to practice (the sibling's open item 1, first branch) |
| Constant ratio against constant difference | 0.2 lesson 98, from tables | G1 names geometric sequences and G5 sums them |
| Iteration and bisection | 0.2 lessons 107 and 108 (course F, level F4) | G1 lesson 43 uses cobwebs for convergence; R5 lesson 146 connects bisection to the intermediate value theorem |
| Graphs of $\lvert x \rvert$ and piecewise functions | 0.2 lessons 32 and 93 | Used in R3 and R5 |
| Gradient of a curve and area under it, by chords and trapezia | 0.2 lessons 43, 109, 110 | R5 turns the shrinking chord into a limit |

**Considered and left out** [our choice].

| Topic | Where it goes instead | Why not here |
|---|---|---|
| Logarithms | 0.3 course G | They need exponential functions first; 0.1 lesson 36's log-scale number line and 0.2 lesson 47's log price axis only prepare them |
| Mathematical induction | 0.3 level R2 | It proves statements about sums, which need 0.3's series first |
| The Cauchy-Schwarz inequality | 1.4 (inner products) | AM-GM (lesson 77) is the one inequality an algebra course can prove fully from $(a - b)^2 \ge 0$; Cauchy-Schwarz is clearest with vectors |
| Matrices beyond a table of coefficients | 0.3 level T5, then 1.4 | Lesson 53 shows the table so that 1.4's $A\mathbf{x} = \mathbf{b}$ is a new notation for a known act |
| Modular arithmetic as a field of study | 1.8 and puzzles in 3.3 | Lesson 16 teaches remainder arithmetic as a tool, which is all 0.1 needs |

---

## 3. Homework blueprint per level

### 3.0 Rules for every set

- **Shape.** 7 to 10 items (ASSESSMENT.md allows 6 to 12), issued when a level's last lesson is done, due in 7 days, no grading before submission, never a gate (ASSESSMENT.md 2.5). About 2 hours in 0.1 and 2.5 hours in 0.2, as summed item estimates.
- **Difficulty.** Every item is at difficulty 3 to 5, with at least two at 5 in every set (design research 8.4 asks for at least one).
- **Long-form.** At least one item per set is a `long-form` check (CONTENT-FORMAT.md 3.4) with `genre` proof, derivation or written, a model answer in numbered lines, and a rubric of five points of 2 marks (10 in all, as the schema requires). After submission the learner self-marks each point; Bertie drafts a mark per point with a verbatim quote as evidence (`marking: tutor-draft`, AI-TUTOR.md 2.7), and the learner accepts or changes every point. A long-form item counts as correct at 6 of 10 (ASSESSMENT.md 3.6).
- **Code.** One code drill per set, scaffolded to the learner's 0.4 progress: in W1 and W2 the learner predicts output and edits one line; from W3 they complete a function from a skeleton; from course E they write small functions against visible examples, with hidden tests at submission. Every 0.1 and 0.2 drill uses the Python standard library only (`fractions`, `math`, `cmath`, `decimal`) and declares `needs: []`, so it runs on Pyodide in the Artifact and in the web app alike (ARCHITECTURE.md decision 15). On a device that cannot load Python, the item shows "Run this one in the web app" with its drill id and seed, and accepts the pasted result code (ASSESSMENT.md 2.5).
- **Calculator.** Non-calculator unless an item is marked [calc], matching the exit paper.
- **Variants.** Generated items are seeded when the set is issued (ASSESSMENT.md 2.5), so a returning learner sees the same set; the generator families are listed per set. Homework draws from the practice reserve, never from the exam reserve (ASSESSMENT.md 3.2 rule 5).
- **Fluency sets.** Beside each homework set the level has one fluency set (`set.<course>.<level>-fluency`, kind `practice`): 15 to 20 generated items at difficulty 2 and 3 across the level's skills, about 60 minutes in 0.1 and 75 in 0.2, no long-form, no hints. They are where the 85% and 90% outcome bars of section 1 are measured.

### 3.1 Item 0.1 Number

| Level | Set | Items | Difficulty mix | Long-form item (rubric: five points of 2 marks) | Code drill | Generators |
|---|---|---|---|---|---|---|
| W1 | `set.numwork.place-value` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why long multiplication works (split, distributive law, partial products, placeholder zero, diagnose a dropped zero) | `drl.num.divmod-check`: predict, then check, long divisions with `//`, `%` and `divmod` | `gen.num.long-multiplication`, `gen.num.long-division`, `gen.num.decimal-scale` |
| W2 | `set.numwork.negatives` | 8 | d3 ×3, d4 ×3, d5 ×2 | Prove $(-a)(-b) = ab$ from the laws of arithmetic | `drl.num.precedence`: predict Python's values of `-3**2`, `2+3*4`, `6/2*(1+2)`, then explain each | `gen.num.signed-arith`, `gen.num.order-of-operations` |
| W3 | `set.numwork.primes` | 9 | d3 ×3, d4 ×4, d5 ×2 | Prove the digit-sum test for 9 and show why it fails for 7 | `drl.num.count-factors`: `count_factors(n)` by trial division up to $\sqrt{n}$, checked against the prime-power formula | `gen.num.factorise`, `gen.num.hcf-lcm`, `gen.num.count-factors`, `gen.num.last-digit` |
| W4 | `set.numwork.fractions` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why dividing by a fraction multiplies by its reciprocal, two ways | `drl.num.fractions`: check fraction answers with `fractions.Fraction` and show the mediant trap | `gen.num.fraction-ops`, `gen.num.fraction-word` |
| P1 | `set.propprec.percent` | 9 | d3 ×3, d4 ×4, d5 ×2 | Prove that $\frac{1}{n}$ terminates when $n = 2^a 5^b$, and sketch why it recurs otherwise | `drl.num.cycle-length`: `cycle_length(n)` by tracking long-division remainders | `gen.num.recurring-to-fraction`, `gen.num.reverse-percent`, `gen.num.compound` |
| P2 | `set.propprec.ratio` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why the average speed of a round trip is not the mean of the two speeds | `drl.num.unit-convert`: multiply a chain of conversion fractions, test 30 m/s to km/h | `gen.num.ratio-share`, `gen.num.ratio-change`, `gen.num.best-buy`, `gen.num.inverse-proportion`, `gen.num.units` |
| P3 | `set.propprec.powers` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why $a^0 = 1$ and $a^{-n} = \frac{1}{a^n}$ are forced by the index laws, and why $0^0$ is left undefined | `drl.num.simplify-sqrt`: `simplify_sqrt(n)` returns $(a, b)$ with $\sqrt{n} = a\sqrt{b}$ | `gen.num.index-laws`, `gen.num.surds`, `gen.num.standard-form` |
| P4 | `set.propprec.precision` | 10 | d3 ×3, d4 ×4, d5 ×3 | Euclid's proof that there are infinitely many primes | `drl.num.binary-float`: `to_binary(n)`; show that adding 0.1 ten times is not exactly 1.0 and fix the test with `math.isclose` | `gen.num.rounding`, `gen.num.bounds`, `gen.num.estimate`, `fermi-estimator` seeds |

**Example problems, 0.1.**

**W1, example 1 (difficulty 4).** Without a calculator, find $3.06 \times 4.7$ and $13.5 \div 0.06$.
*Answer:* $14.382$ and $225$.
*Working:* $3.06 \times 4.7 = \frac{306 \times 47}{1000}$ and $306 \times 47 = 12{,}240 + 2{,}142 = 14{,}382$, so $14.382$. Scaling both numbers of a division by 100 leaves the quotient unchanged: $13.5 \div 0.06 = 1{,}350 \div 6 = 225$. Estimate check: $3 \times 5 = 15$; $13.5 \div 0.06 \approx 12 \div 0.06 = 200$.

**W1, example 2 (difficulty 5).** Find the four-digit number $ABCD$ (digits $A, B, C, D$) with $4 \times ABCD = DCBA$.
*Answer:* $2{,}178$ ($2{,}178 \times 4 = 8{,}712$).
*Working:* $4 \times ABCD < 10{,}000$, so $A \le 2$. $DCBA$ is a multiple of 4, so its last digit $A$ is even: $A = 2$. Then $4D$ ends in 2, so $D$ is 3 or 8, and $D \ge 4A = 8$ gives $D = 8$. Writing place values: $4(2000 + 100B + 10C + 8) = 8000 + 100C + 10B + 2$, which simplifies to $390B + 30 = 60C$, that is $13B + 1 = 2C$. $B$ must be odd and $C \le 9$, so $B = 1$, $C = 7$.

**W2, example 1 (difficulty 4).** Evaluate $\dfrac{-3^2 + (-2)^3}{(-1)^5 \times (4 - 7)}$.
*Answer:* $-\frac{17}{3}$.
*Working:* $-3^2 = -9$ (the power binds before the minus), $(-2)^3 = -8$, so the top is $-17$. The bottom is $(-1) \times (-3) = 3$.

**W2, example 2 (difficulty 5, long-form).** Using only the distributive law, $x \times 0 = 0$, and the definition of $-x$ as the number with $x + (-x) = 0$, prove that $(-a)(-b) = ab$.
*Model answer:* (1) $(-a)b + ab = (-a + a)b = 0 \times b = 0$, so $(-a)b$ is the number that adds to $ab$ to give 0: $(-a)b = -(ab)$. (2) $(-a)(-b) + (-a)b = (-a)(-b + b) = (-a) \times 0 = 0$, so $(-a)(-b) = -\big((-a)b\big) = -\big(-(ab)\big)$. (3) Since $-(ab) + ab = 0$, the number that adds to $-(ab)$ to give 0 is $ab$, so $(-a)(-b) = ab$. (4) Each "the number that adds to give 0" step uses the fact that this number is unique: if $y + x = 0$ and $z + x = 0$ then $y = z$.
*Rubric (10):* 2 for combining $(-a)b + ab$ with the distributive law; 2 for concluding $(-a)b = -(ab)$; 2 for the second distributive step to $(-a) \times 0 = 0$; 2 for reaching $ab$ through $-(-(ab))$; 2 for naming the justification of every line, including uniqueness of the negative.

**W3, example 1 (difficulty 5).** Find the last two digits of $7^{2026}$.
*Answer:* 49.
*Working:* Work with remainders on division by 100. $7^2 = 49$, $7^4 = 49^2 = 2{,}401$, which leaves 1. So powers of 7 repeat every 4 steps in their last two digits. $2026 = 4 \times 506 + 2$, so $7^{2026}$ leaves the same remainder as $7^2 = 49$.

**W3, example 2 (difficulty 4, long-form).** Prove that $n = 1000a + 100b + 10c + d$ is divisible by 9 exactly when $a + b + c + d$ is, and explain why the same argument gives no test for 7.
*Model answer:* (1) $n - (a + b + c + d) = 999a + 99b + 9c$. (2) This equals $9(111a + 11b + c)$, a multiple of 9. (3) Two numbers that differ by a multiple of 9 leave the same remainder on division by 9, so $n$ is divisible by 9 if and only if its digit sum is; both directions follow. (4) The key fact is that 10, 100 and 1,000 each leave remainder 1 on division by 9. (5) On division by 7 they leave 3, 2 and 6, so $n$ minus its digit sum need not be a multiple of 7: 16 has digit sum 7 but is not divisible by 7.
*Rubric (10):* 2 for line 1; 2 for factorising out 9; 2 for the same-remainder argument in both directions; 2 for identifying "each power of 10 leaves remainder 1" as the reason; 2 for the explanation and a counterexample for 7.

**W4, example 1 (difficulty 4).** Calculate $2\frac{2}{3} \div 1\frac{1}{9} - \frac{3}{5}$.
*Answer:* $\frac{9}{5} = 1\frac{4}{5}$.
*Working:* $\frac{8}{3} \div \frac{10}{9} = \frac{8}{3} \times \frac{9}{10} = \frac{72}{30} = \frac{12}{5}$, and $\frac{12}{5} - \frac{3}{5} = \frac{9}{5}$.

**W4, example 2 (difficulty 5, long-form).** Explain why "to divide by a fraction, multiply by its reciprocal" works, using $2 \div \frac{3}{4}$, in two ways: (a) by counting how many $\frac{3}{4}$ fit into 2; (b) from the fact that division undoes multiplication. Then decide whether $\frac{a}{b} \div \frac{c}{d} = \frac{a \div c}{b \div d}$ is also true.
*Model answer:* (a) In quarters, $2 = \frac{8}{4}$ and $\frac{3}{4}$ is 3 quarters; 8 quarters hold 3 quarters $\frac{8}{3}$ times, and $2 \times \frac{4}{3} = \frac{8}{3}$. (b) $2 \div \frac{3}{4} = q$ means $q \times \frac{3}{4} = 2$; multiplying both sides by $\frac{4}{3}$ gives $q = 2 \times \frac{4}{3}$. (c) $\frac{a \div c}{b \div d} = \frac{a}{c} \times \frac{d}{b} = \frac{ad}{bc}$, which equals $\frac{a}{b} \times \frac{d}{c}$, so the rule is also true whenever $b, c, d \ne 0$; check: $\frac{6}{8} \div \frac{3}{4} = \frac{6 \div 3}{8 \div 4} = \frac{2}{2} = 1$.
*Rubric (10):* 2 for the common-unit argument; 2 for reaching $\frac{8}{3}$; 2 for the inverse-operation argument; 2 for the algebra in (c); 2 for stating the non-zero conditions and a numerical check.

**P1, example 1 (difficulty 4).** Write $0.2\dot{4}\dot{5}$ (that is, $0.2454545\ldots$) as a fraction in lowest terms.
*Answer:* $\frac{27}{110}$.
*Working:* Let $x = 0.24545\ldots$ Then $10x = 2.4545\ldots$ and $1000x = 245.4545\ldots$; subtracting, $990x = 243$, so $x = \frac{243}{990} = \frac{27}{110}$. Check: $27 \div 110 = 0.24545\ldots$ The decision point is shifting by 10 first, to move the non-recurring 2 past the point.

**P1, example 2 (difficulty 5) [calc].** £1,000 is invested at 8% a year compound. (a) After how many whole years does it first more than double? (b) A rival pays 10% simple interest a year. From which year is the compound account ahead?
*Answer:* (a) 10 years. (b) From year 7.
*Working:* (a) $1.08^9 = 1.99900\ldots$, just short of 2, and $1.08^{10} = 2.15892\ldots$ The "rule of 72" estimate of $\frac{72}{8} = 9$ years is close but, here, a year early; the exact check matters. (b) Compare $1.08^n$ with $1 + 0.1n$: $1.08^6 = 1.5869 < 1.6$ but $1.08^7 = 1.7138 > 1.7$.

**P2, example 1 (difficulty 4).** The ratio of boys to girls in a club is $3 : 5$. After 6 more boys join, the ratio is $1 : 1$. How many girls are there?
*Answer:* 15.
*Working:* Let the unit be $k$: boys $3k$, girls $5k$. Then $3k + 6 = 5k$, so $k = 3$ and there are 15 girls (9 boys before, 15 after).

**P2, example 2 (difficulty 5, long-form).** A cyclist climbs a hill at 12 km/h and comes back down the same road at 36 km/h. Find the average speed for the round trip and explain in words why it is not 24 km/h, and why it sits closer to the slower speed.
*Model answer:* (1) Take the road as 36 km (any length works). (2) Up takes 3 hours, down takes 1 hour. (3) Average speed is total distance over total time, $\frac{72}{4} = 18$ km/h. (4) The plain mean of 24 would be right only if equal *times* were spent at each speed; here three times as long is spent at the slow speed, so the slow speed carries three times the weight: $\frac{3 \times 12 + 1 \times 36}{4} = 18$. (5) In general the round-trip average is $\frac{2uv}{u + v}$, always at most $\frac{u + v}{2}$, with equality only when $u = v$.
*Rubric (10):* 2 for a correct distance and the times; 2 for total distance over total time; 2 for 18 km/h; 2 for the time-weighting explanation; 2 for the general form or for stating when the plain mean would be right.

**P3, example 1 (difficulty 4).** Simplify $\frac{\sqrt{50} + \sqrt{18}}{\sqrt{8}}$, and rationalise $\frac{4}{3 - \sqrt{5}}$.
*Answer:* $4$ and $3 + \sqrt{5}$.
*Working:* $\sqrt{50} = 5\sqrt{2}$, $\sqrt{18} = 3\sqrt{2}$, $\sqrt{8} = 2\sqrt{2}$, so the fraction is $\frac{8\sqrt{2}}{2\sqrt{2}} = 4$. Multiply top and bottom by $3 + \sqrt{5}$: $\frac{4(3 + \sqrt{5})}{9 - 5} = 3 + \sqrt{5}$.

**P3, example 2 (difficulty 5).** Without a calculator, put in increasing order: $2^{100}$, $3^{60}$, $5^{40}$, $10^{30}$.
*Answer:* $5^{40} < 3^{60} < 10^{30} < 2^{100}$.
*Working:* Write each as a 20th power: $2^{100} = 32^{20}$, $3^{60} = 27^{20}$, $5^{40} = 25^{20}$, $10^{30} = (10^{1.5})^{20} = (\sqrt{1000})^{20}$, and $\sqrt{1000}$ lies between 31 and 32 because $31^2 = 961$ and $32^2 = 1{,}024$. The leap is to make the exponents equal so that only the bases need comparing.

**P4, example 1 (difficulty 5).** $a = 6.3$ and $b = 2.4$, each correct to 1 decimal place. Find the upper bound of $\frac{a}{a - b}$.
*Answer:* $\frac{6.25}{3.8} = \frac{125}{76} \approx 1.6447$.
*Working:* $a$ appears twice, so its two appearances cannot take different values. Write $\frac{a}{a - b} = \frac{1}{1 - \frac{b}{a}}$: it grows as $\frac{b}{a}$ grows, so take $b$ largest (2.45) and $a$ smallest (6.25), giving $\frac{6.25}{3.80}$. The naive answer $\frac{6.35}{6.25 - 2.45} \approx 1.671$ uses $a = 6.35$ on top and $a = 6.25$ below at the same time, which no real value of $a$ allows.

**P4, example 2 (difficulty 5, long-form).** Prove that there are infinitely many primes.
*Model answer:* (1) Suppose there are only finitely many, $p_1, p_2, \ldots, p_k$. (2) Let $N = p_1 p_2 \cdots p_k + 1$. (3) Dividing $N$ by any $p_i$ leaves remainder 1, so no $p_i$ divides $N$. (4) $N > 1$, so $N$ has at least one prime factor (prime factorisation, lesson 12), and that prime is not on the list. (5) This contradicts the assumption, so the primes never run out. Note: $N$ need not itself be prime: $2 \times 3 \times 5 \times 7 \times 11 \times 13 + 1 = 30{,}031 = 59 \times 509$.
*Rubric (10):* 2 for the assumption; 2 for constructing $N$; 2 for the remainder-1 argument; 2 for using that $N$ has a prime factor; 2 for the conclusion and for not claiming $N$ is prime.

### 3.2 Item 0.2 Algebra

| Level | Set | Items | Difficulty mix | Long-form item (rubric: five points of 2 marks) | Code drill | Generators |
|---|---|---|---|---|---|---|
| E1 | `set.expreq.letters` | 8 | d3 ×3, d4 ×3, d5 ×2 | Identity or not: three claims, a counterexample each, and why one counterexample suffices | `drl.alg.is-identity`: compare two expressions at 1,000 random points and return a counterexample or None | `gen.alg.substitute`, `gen.alg.like-terms`, `gen.alg.pattern-rule` |
| E2 | `set.expreq.brackets` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why $(a + b)^2 = a^2 + 2ab + b^2$, with an area diagram, and when $(a + b)^2 = a^2 + b^2$ does hold ($ab = 0$) | `drl.alg.expand-check`: test the learner's expansions numerically | `gen.alg.expand`, `gen.alg.factorise-common`, `gen.alg.special-products` |
| E3 | `set.expreq.fractions-proof` | 9 | d3 ×3, d4 ×4, d5 ×2 | The product of four consecutive integers is one less than a square | `drl.alg.mean-deviation`: `mean(xs)`; check that deviations sum to 0 within a tolerance; sum of squares two ways | `gen.alg.alg-fractions`, `gen.alg.index-letters`, `gen.alg.sigma-eval` |
| E4 | `set.expreq.linear` | 8 | d3 ×3, d4 ×3, d5 ×2 | Find and explain the illegal step in the "$2 = 1$" proof and in a solution that divides $x^2 = 3x$ by $x$ | `drl.alg.solve-linear`: `solve_linear(a, b, c, d)` for $ax + b = cx + d$, returning a `Fraction`, `"none"` or `"all"` | `gen.alg.linear-equation`, `gen.alg.linear-fractions`, `gen.alg.word-linear` |
| E5 | `set.expreq.formulae` | 8 | d3 ×3, d4 ×3, d5 ×2 | The pendulum by dimensional analysis | `drl.alg.round-trip`: a formula and its rearrangement must recover every input at 100 points | `gen.alg.change-subject`, `gen.alg.subject-twice` |
| E6 | `set.expreq.inequalities` | 9 | d3 ×3, d4 ×4, d5 ×2 | Why multiplying by a negative reverses an inequality: a number-line argument and an algebraic one | `drl.alg.lp-grid`: test every whole-number plan in a region and return the best | `gen.alg.linear-inequality`, `gen.alg.abs-inequality`, `gen.alg.lp-region` |
| L1 | `set.lines.straight` | 8 | d3 ×3, d4 ×3, d5 ×2 | Prove $m_1 m_2 = -1$ by rotating a slope triangle | `drl.alg.line-through`: `line_through(p, q)` with `Fraction`s, handling vertical lines | `gen.alg.line-two-points`, `gen.alg.perpendicular`, `gen.alg.nth-term-linear`, `gen.alg.special-sequences` |
| L2 | `set.lines.models` | 8 | d3 ×3, d4 ×3, d5 ×2 | Marginal against average rate, and why a banded schedule never cuts take-home pay | `drl.alg.tax`: piecewise `tax(income)` and average rate | `gen.alg.rate-graph`, `gen.alg.motion-graph`, `gen.alg.piecewise-tariff` |
| L3 | `set.lines.systems` | 9 | d3 ×3, d4 ×4, d5 ×2 | Why $2x + 3y = 6$ and $4x + 6y = 15$ have no solution, geometrically and algebraically, and which $c$ in $4x + 6y = c$ gives infinitely many | `drl.alg.solve-2x2`: Cramer's rule with `Fraction`s, detecting $ad - bc = 0$ | `gen.alg.system-2x2`, `gen.alg.system-3x3`, `gen.alg.system-word`, `gen.alg.replication` |
| Q1 | `set.quadpoly.factorising` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why the zero-product property needs zero on one side, using $(x - 2)(x - 3) = 6$ | `drl.alg.factor-pair`: find integers with sum $b$ and product $c$, or report none | `gen.alg.factorise-quadratic`, `gen.alg.solve-quadratic-factor` |
| Q2 | `set.quadpoly.formula` | 8 | d3 ×3, d4 ×3, d5 ×2 | Derive the quadratic formula, justifying every line | `drl.alg.solve-quadratic`: real roots by cases of the discriminant, exact when it is a perfect square | `gen.alg.complete-square`, `gen.alg.quadratic-formula`, `gen.alg.discriminant-k` |
| Q3 | `set.quadpoly.graphs` | 9 | d3 ×3, d4 ×4, d5 ×2 | The tangent to $x^2 + y^2 = 25$ at $(3, 4)$ two ways: perpendicular radius, and a repeated root ($3x + 4y = 25$) | `drl.alg.line-meets-parabola`: classify misses, touches or cuts | `gen.alg.quadratic-sketch`, `gen.alg.vieta`, `gen.alg.quadratic-inequality`, `gen.alg.circle` |
| Q4 | `set.quadpoly.optimising` | 8 | d3 ×3, d4 ×3, d5 ×2 | The square has the largest area for a given perimeter, two ways | `drl.alg.variance-two-ways`: the shortcut returns $-1024$ on $10^9 + 0.1$, $10^9 + 0.2$, $10^9 + 0.3$; the two-pass method returns $0.0199999857$, which is $0.02$ to 6 significant figures and exact for the stored doubles to 11 (each input is already off by up to $6 \times 10^{-8}$, half the $1.2 \times 10^{-7}$ spacing of doubles near $10^9$), so the test compares to $0.02$ with `rel_tol=1e-5` | `gen.alg.revenue-max`, `gen.alg.fence`, `gen.alg.least-squares-1d` |
| Q5 | `set.quadpoly.polynomials` | 9 | d3 ×3, d4 ×4, d5 ×2 | Prove the remainder theorem and explain why a linear divisor leaves a constant remainder | `drl.alg.poly-divide`: divide coefficient lists, returning quotient and remainder | `gen.alg.poly-divide`, `gen.alg.factor-theorem`, `gen.alg.cubic-roots`, `gen.alg.quadratic-sequence` |
| Q6 | `set.quadpoly.complex` | 7 | d3 ×2, d4 ×3, d5 ×2 | Why the non-real roots of a real quadratic are conjugates, and a counterexample with non-real coefficients | `drl.alg.complex-roots`: quadratic roots with `complex` and `cmath.sqrt` | `gen.alg.complex-arith`, `gen.alg.complex-quadratic` |
| F1 | `set.funcs.functions` | 8 | d3 ×3, d4 ×3, d5 ×2 | Why $x^2$ has no inverse on all real numbers, and two different inverses from two restricted domains | `drl.alg.compose`: `compose(f, g)` returns a function; show $f \circ g \ne g \circ f$ | `gen.alg.function-eval`, `gen.alg.domain-range`, `gen.alg.compose`, `gen.alg.inverse` |
| F2 | `set.funcs.gallery` | 8 | d3 ×3, d4 ×3, d5 ×2 | A hole against a vertical asymptote: $\frac{x^2 - 4}{x - 2}$ against $\frac{x + 2}{x - 2}$ | `drl.alg.growth-table`: print day, linear total and doubling total until the second passes the first | `gen.alg.proportion-power`, `gen.alg.rational-features`, `gen.alg.graph-match` |
| F3 | `set.funcs.transformations` | 8 | d3 ×3, d4 ×3, d5 ×2 | Every function on the real numbers is an even function plus an odd function | `drl.alg.transform`: `transform(f, a, b, c, d)` returns $x \mapsto a f(bx + c) + d$, tested on known points | `gen.alg.transform-point`, `gen.alg.transform-sketch`, `gen.alg.parity` |
| F4 | `set.funcs.solving` | 10 | d3 ×3, d4 ×4, d5 ×3 | Chord gradients of $x^2$ and $x^3$ and why $h = 0$ cannot be put in directly | `drl.alg.bisection`: `bisection(f, lo, hi, tol)` with a step count checked against $\lceil \log_2 \frac{\text{width}}{\text{tol}} \rceil$ | `gen.alg.graphical-line`, `gen.alg.iteration`, `gen.alg.trapezia`, `gen.alg.radical-equation` |

**Example problems, 0.2.**

**E1, example 1 (difficulty 4).** A phone costs £$p$ and a case costs £12 less than a third of the phone's price. Write and simplify an expression for the cost of 3 phones and 1 case, and evaluate it when $p = 450$.
*Answer:* $\frac{10p}{3} - 12$; £1,488.
*Working:* case $= \frac{p}{3} - 12$; total $= 3p + \frac{p}{3} - 12 = \frac{10p}{3} - 12$; at $p = 450$: $1{,}500 - 12 = 1{,}488$.

**E1, example 2 (difficulty 5, long-form).** Decide whether each claim holds for all allowed values, and justify: (a) $(a + b)^2 = a^2 + b^2$; (b) $\frac{a}{b} + \frac{b}{a} \ge 2$ for all non-zero $a, b$; (c) $2^n > n^2$ for every whole number $n \ge 1$. Explain why one counterexample settles each.
*Model answer:* (a) False: $a = b = 1$ gives $4 \ne 2$. (b) False: $a = 1$, $b = -1$ gives $-2$. (It is true when $a$ and $b$ have the same sign, which Q4 proves.) (c) False: $n = 3$ gives $8 < 9$ (and $n = 2, 4$ give equality). A claim about *all* values is broken by one value where it fails; no number of examples where it works can establish it.
*Rubric (10):* 2 each for a correct, checked counterexample to (a), (b) and (c) (6); 2 for noting the cases where (b) and (c) do hold; 2 for the general principle about "for all" claims.

**E2, example 1 (difficulty 4).** Expand and simplify $(2x - 3)(x + 4) - (x - 2)^2$.
*Answer:* $x^2 + 9x - 16$.
*Working:* $(2x^2 + 5x - 12) - (x^2 - 4x + 4)$; the minus reaches every term of the second bracket.

**E2, example 2 (difficulty 5).** Show that $(n^2 + n + 1)^2 - (n^2 - n + 1)^2 = 4n(n^2 + 1)$.
*Answer and working:* Use $A^2 - B^2 = (A - B)(A + B)$ with $A = n^2 + n + 1$ and $B = n^2 - n + 1$: $A - B = 2n$ and $A + B = 2n^2 + 2$, so the difference is $2n \times 2(n^2 + 1) = 4n(n^2 + 1)$. The decision point: expanding both squares works but takes four times as long; spotting the difference of two squares is the leap.

**E3, example 1 (difficulty 4).** Simplify $\frac{3}{x - 2} - \frac{2}{x + 1}$ and state the excluded values.
*Answer:* $\frac{x + 7}{(x - 2)(x + 1)}$, with $x \ne 2$ and $x \ne -1$.
*Working:* $\frac{3(x + 1) - 2(x - 2)}{(x - 2)(x + 1)} = \frac{3x + 3 - 2x + 4}{(x - 2)(x + 1)}$.

**E3, example 2 (difficulty 5, long-form).** Prove that the product of four consecutive integers is always one less than a perfect square.
*Model answer:* (1) Write them as $n, n + 1, n + 2, n + 3$. (2) Pair the outer and inner factors: $n(n + 3) = n^2 + 3n$ and $(n + 1)(n + 2) = n^2 + 3n + 2$. (3) Let $m = n^2 + 3n$; the product is $m(m + 2) = m^2 + 2m$. (4) So the product plus 1 is $m^2 + 2m + 1 = (m + 1)^2 = (n^2 + 3n + 1)^2$. (5) Check: $1 \times 2 \times 3 \times 4 = 24 = 5^2 - 1$, and $n^2 + 3n + 1 = 5$ at $n = 1$.
*Rubric (10):* 2 for the general representation; 2 for the outer and inner pairing (the leap); 2 for the substitution; 2 for recognising the perfect square; 2 for the conclusion with a numerical check.

**E4, example 1 (difficulty 4).** Solve $\frac{2x - 1}{3} - \frac{x + 2}{4} = 1$.
*Answer:* $x = \frac{22}{5}$.
*Working:* Multiply every term by 12: $4(2x - 1) - 3(x + 2) = 12$, so $8x - 4 - 3x - 6 = 12$ and $5x = 22$.

**E4, example 2 (difficulty 5).** A trader invests a sum in a share. When the price has risen 20% she sells half her holding; she sells the rest after the price falls 10% from that higher level. Her total profit is £560. How much did she invest?
*Answer:* £4,000.
*Working:* Let $I$ be the sum. The first half sells for $0.5I \times 1.2 = 0.6I$; the second for $0.5I \times 1.2 \times 0.9 = 0.54I$. Profit $= 1.14I - I = 0.14I = 560$.

**E5, example 1 (difficulty 4).** Make $x$ the subject of $y = \frac{2x + 3}{x - 1}$.
*Answer:* $x = \frac{y + 3}{y - 2}$, for $y \ne 2$.
*Working:* $y(x - 1) = 2x + 3$, so $xy - 2x = y + 3$ and $x(y - 2) = y + 3$. The subject appears twice, so collect and factorise. The excluded $y = 2$ is a value the original never takes (lesson 99 explains why).

**E5, example 2 (difficulty 5, long-form).** A pendulum's period $T$ (s) depends only on its length $l$ (m), gravity $g$ (m s$^{-2}$) and the bob's mass $m$ (kg). Use units to show $T \propto \sqrt{\frac{l}{g}}$, explain why $m$ cannot appear, and say what the method cannot tell you.
*Model answer:* (1) Suppose $T = C\, l^{\alpha} g^{\beta} m^{\gamma}$ with $C$ a pure number. (2) Units: $\text{s} = \text{m}^{\alpha} (\text{m s}^{-2})^{\beta} \text{kg}^{\gamma}$. (3) Matching kg: $\gamma = 0$; s: $1 = -2\beta$; m: $\alpha + \beta = 0$; so $\beta = -\frac{1}{2}$ and $\alpha = \frac{1}{2}$. (4) Mass is the only quantity carrying kg, so nothing can cancel it: it must be absent. (5) The method cannot find $C$ (it is $2\pi$) and cannot see dimensionless quantities such as the swing angle, on which large swings do depend.
*Rubric (10):* 2 for the power-law set-up; 2 for the unit equations; 2 for solving the exponents; 2 for the argument about mass; 2 for both limitations.

**E6, example 1 (difficulty 4).** Solve $\lvert 2x - 3 \rvert \le 7$ and $\lvert x + 1 \rvert > 4$, and list the integers that satisfy both.
*Answer:* $-2 \le x \le 5$; $x < -5$ or $x > 3$; integers 4 and 5.
*Working:* $-7 \le 2x - 3 \le 7$ gives $-2 \le x \le 5$. $x + 1 > 4$ or $x + 1 < -4$ gives $x > 3$ or $x < -5$. The overlap is $3 < x \le 5$.

**E6, example 2 (difficulty 5).** A fund can hold bond A (yield 4%, risk score 2 per £1,000) and bond B (yield 6%, risk score 5 per £1,000). It has £100,000 and a total risk budget of 350. How much should it hold of each to maximise yield?
*Answer:* £50,000 in each, yielding £5,000 a year.
*Working:* In thousands, $a + b \le 100$, $2a + 5b \le 350$, $a, b \ge 0$; maximise $40a + 60b$ (pounds). The corners are $(0, 0)$, $(100, 0)$ worth 4,000, $(0, 70)$ worth 4,200, and the intersection of the two limits, $2(100 - b) + 5b = 350$, so $b = 50$, $a = 50$, worth 5,000. A linear objective is largest at a corner of the region, so the intersection wins.

**L1, example 1 (difficulty 4).** Find the line through $(-2, 5)$ perpendicular to $3x - 4y = 12$, and where it meets the $x$-axis.
*Answer:* $4x + 3y = 7$ (that is, $y = -\frac{4}{3}x + \frac{7}{3}$), meeting the axis at $\left(\frac{7}{4}, 0\right)$.
*Working:* $3x - 4y = 12$ has gradient $\frac{3}{4}$, so the perpendicular has $-\frac{4}{3}$; $y - 5 = -\frac{4}{3}(x + 2)$. Check: $4(-2) + 3(5) = 7$.

**L1, example 2 (difficulty 5, long-form).** Prove that two non-vertical, non-horizontal lines with gradients $m_1$ and $m_2$ are perpendicular exactly when $m_1 m_2 = -1$.
*Model answer:* (1) A line of gradient $m$ has a slope triangle with run 1 and rise $m$. (2) Rotating it a quarter turn anticlockwise turns the run into a rise and the rise into a run pointing backwards: run $-m$, rise 1 (the rotated triangle is congruent). (3) The rotated line's gradient is $\frac{1}{-m} = -\frac{1}{m}$. (4) So a line is perpendicular to the first exactly when its gradient is $-\frac{1}{m_1}$, that is $m_1 m_2 = -1$. (5) The argument needs $m_1 \ne 0$; horizontal and vertical lines are perpendicular but have no product to form.
*Rubric (10):* 2 for the slope triangle; 2 for the rotation with its justification; 2 for the new gradient; 2 for the conclusion in both directions; 2 for the exceptions.

**L2, example 1 (difficulty 4).** A taxi charges £3.20 plus £1.80 a mile; a rival charges £5 plus £1.50 a mile. For which distances is the rival cheaper?
*Answer:* More than 6 miles.
*Working:* $5 + 1.5d < 3.2 + 1.8d$ gives $1.8 < 0.3d$, so $d > 6$.

**L2, example 2 (difficulty 5).** Stylised tax: 0% on income up to £10,000, 20% on income between £10,000 and £40,000, 40% above £40,000. (a) Write the tax $T(x)$ as a piecewise function. (b) Find the average tax rate on £50,000. (c) At what income is the average rate exactly 20%?
*Answer:* (a) $T(x) = 0$ for $x \le 10{,}000$; $0.2(x - 10{,}000)$ for $10{,}000 < x \le 40{,}000$; $6{,}000 + 0.4(x - 40{,}000)$ for $x > 40{,}000$. (b) $T = 10{,}000$, so 20%. (c) £50,000.
*Working:* (c) In the middle band the average $\frac{0.2(x - 10{,}000)}{x}$ is always below 20%; in the top band $6{,}000 + 0.4(x - 40{,}000) = 0.2x$ gives $x = 50{,}000$, consistent with (b).

**L3, example 1 (difficulty 4).** Solve $4x - 3y = 18$ and $6x + 5y = -11$.
*Answer:* $x = \frac{3}{2}$, $y = -4$.
*Working:* Scale to $12x - 9y = 54$ and $12x + 10y = -22$; subtracting gives $-19y = 76$. Check in the second equation: $9 - 20 = -11$.

**L3, example 2 (difficulty 5).** A share costs £50 and will be worth £60 or £40 in a year; cash earns nothing. A put option pays $\max(45 - S, 0)$. Find the portfolio of shares and cash that replicates the put, and the put's price.
*Answer:* Short $\frac{1}{4}$ of a share and hold £15 cash; price £2.50.
*Working:* Holding $\Delta$ shares and $B$ cash: up, $60\Delta + B = 0$; down, $40\Delta + B = 5$. Subtracting, $20\Delta = -5$, so $\Delta = -\frac{1}{4}$ and $B = 15$. Today's cost is $50 \times \left(-\frac{1}{4}\right) + 15 = 2.50$. No probability of the up move was needed.

**Q1, example 1 (difficulty 4).** Solve $6x^2 - x - 15 = 0$ by factorising.
*Answer:* $x = \frac{5}{3}$ or $x = -\frac{3}{2}$.
*Working:* $ac = -90$; the pair $9$ and $-10$ splits the middle: $6x^2 + 9x - 10x - 15 = 3x(2x + 3) - 5(2x + 3) = (3x - 5)(2x + 3)$.

**Q1, example 2 (difficulty 5).** Simplify $\frac{2x^2 + 5x - 3}{x^2 + 2x - 3} \div \frac{4x^2 - 1}{x^2 - 1}$ and state every excluded value.
*Answer:* $\frac{x + 1}{2x + 1}$, for $x \ne -3, -1, 1, \frac{1}{2}, -\frac{1}{2}$.
*Working:* Factorise: $\frac{(2x - 1)(x + 3)}{(x + 3)(x - 1)} \times \frac{(x - 1)(x + 1)}{(2x - 1)(2x + 1)}$. Exclusions come from both denominators ($-3, 1, -1$) and from the divisor being zero ($\pm\frac{1}{2}$).

**Q2, example 1 (difficulty 4).** Write $2x^2 - 12x + 23$ as $a(x - h)^2 + k$, state its minimum, and solve $2x^2 - 12x + 23 = 25$ exactly.
*Answer:* $2(x - 3)^2 + 5$; minimum 5 at $x = 3$; $x = 3 \pm \sqrt{10}$.
*Working:* $2(x^2 - 6x) + 23 = 2\left((x - 3)^2 - 9\right) + 23$. Then $(x - 3)^2 = 10$.

**Q2, example 2 (difficulty 5, long-form).** Derive the formula for the roots of $ax^2 + bx + c = 0$ ($a \ne 0$), justifying every line.
*Model answer:* (1) Divide by $a$ (allowed since $a \ne 0$) so the square can be completed with a single $x^2$: $x^2 + \frac{b}{a}x + \frac{c}{a} = 0$. (2) Complete the square: $\left(x + \frac{b}{2a}\right)^2 - \frac{b^2}{4a^2} + \frac{c}{a} = 0$. (3) Isolate the square over a common denominator: $\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}$. (4) Take square roots: $x + \frac{b}{2a} = \pm\frac{\sqrt{b^2 - 4ac}}{2\lvert a \rvert}$, and since the $\pm$ already covers both signs, $2\lvert a \rvert$ may be written $2a$. (5) So $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$, with real roots exactly when $b^2 - 4ac \ge 0$.
*Rubric (10):* 2 for dividing by $a$ with its reason; 2 for completing the square correctly; 2 for the common denominator $4a^2$; 2 for the $\pm$ and the $\lvert a \rvert$ point; 2 for the final formula and the condition for real roots.

**Q3, example 1 (difficulty 4).** For which $k$ does $x^2 + kx + 9 = 0$ have two distinct real roots?
*Answer:* $k < -6$ or $k > 6$.
*Working:* $k^2 - 36 > 0$, a quadratic inequality in $k$ that is positive outside its roots $\pm 6$.

**Q3, example 2 (difficulty 5).** The roots of $2x^2 - 6x + 3 = 0$ are $\alpha$ and $\beta$. Find a quadratic with integer coefficients whose roots are $\alpha^2$ and $\beta^2$.
*Answer:* $4x^2 - 24x + 9 = 0$.
*Working:* $\alpha + \beta = 3$ and $\alpha\beta = \frac{3}{2}$. Then $\alpha^2 + \beta^2 = (\alpha + \beta)^2 - 2\alpha\beta = 6$ and $\alpha^2\beta^2 = \frac{9}{4}$, so $x^2 - 6x + \frac{9}{4} = 0$; multiply by 4.

**Q4, example 1 (difficulty 4).** For the data 1, 4, 6, 9, find the smallest value of $\sum (x_i - c)^2$ and check it equals $\sum x_i^2 - 4\bar{x}^2$.
*Answer:* 34, at $c = \bar{x} = 5$.
*Working:* Deviations $-4, -1, 1, 4$ give $16 + 1 + 1 + 16 = 34$. $\sum x_i^2 = 1 + 16 + 36 + 81 = 134$ and $4 \times 25 = 100$.

**Q4, example 2 (difficulty 5, long-form).** Prove that, among rectangles with perimeter $P$, the square has the largest area, first by completing the square and then by AM-GM.
*Model answer:* (1) Sides $x$ and $\frac{P}{2} - x$ with $0 < x < \frac{P}{2}$; area $A = x\left(\frac{P}{2} - x\right)$. (2) $A = -\left(x - \frac{P}{4}\right)^2 + \frac{P^2}{16}$. (3) A square is never negative, so $A \le \frac{P^2}{16}$, with equality only at $x = \frac{P}{4}$, when both sides are $\frac{P}{4}$: a square. (4) AM-GM: for positive sides $x, y$ with $x + y = \frac{P}{2}$, $\sqrt{xy} \le \frac{x + y}{2} = \frac{P}{4}$, so $xy \le \frac{P^2}{16}$. (5) Equality in AM-GM needs $x = y$: the square again.
*Rubric (10):* 2 for the set-up; 2 for completing the square; 2 for the maximum and its equality case; 2 for the AM-GM route; 2 for stating positivity and both equality conditions.

**Q5, example 1 (difficulty 4).** $f(x) = x^3 + ax^2 + bx - 6$ leaves remainder $-12$ when divided by $x - 1$, and $x + 2$ is a factor. Find $a$ and $b$ and factorise $f$ fully.
*Answer:* $a = 0$, $b = -7$; $f(x) = (x + 2)(x + 1)(x - 3)$.
*Working:* $f(1) = a + b - 5 = -12$ and $f(-2) = 4a - 2b - 14 = 0$, so $a + b = -7$ and $2a - b = 7$; adding gives $a = 0$. Dividing $x^3 - 7x - 6$ by $x + 2$ gives $x^2 - 2x - 3 = (x + 1)(x - 3)$.

**Q5, example 2 (difficulty 5).** Find the remainder when $x^{50}$ is divided by $x^2 - 1$.
*Answer:* 1.
*Working:* The remainder has degree below 2: $x^{50} = (x^2 - 1)q(x) + px + r$. At $x = 1$: $1 = p + r$. At $x = -1$: $1 = -p + r$. So $p = 0$, $r = 1$. The leap is evaluating at the divisor's roots, where $q(x)$ vanishes from view.

**Q6, example 1 (difficulty 4).** Solve $z^2 - 4z + 13 = 0$ and check the sum and product of the roots.
*Answer:* $z = 2 \pm 3i$; sum 4, product 13.
*Working:* $z = \frac{4 \pm \sqrt{16 - 52}}{2} = \frac{4 \pm 6i}{2}$. Sum $= 4 = -\frac{b}{a}$; product $= 4 + 9 = 13 = \frac{c}{a}$.

**Q6, example 2 (difficulty 5).** Find every complex $z$ with $z^2 = 3 + 4i$.
*Answer:* $z = 2 + i$ or $z = -2 - i$.
*Working:* Let $z = a + bi$: $a^2 - b^2 = 3$ and $2ab = 4$. Substituting $b = \frac{2}{a}$: $a^4 - 3a^2 - 4 = 0$, a quadratic in $a^2$: $(a^2 - 4)(a^2 + 1) = 0$. $a$ is real, so $a^2 = 4$, $a = \pm 2$, $b = \pm 1$ with matching signs. Check: $(2 + i)^2 = 4 + 4i - 1$.

**F1, example 1 (difficulty 4).** $f(x) = 2x - 3$ and $g(x) = x^2 + 1$. Solve $f(g(x)) = g(f(x))$.
*Answer:* $x = 3 \pm \frac{\sqrt{14}}{2}$.
*Working:* $f(g(x)) = 2x^2 - 1$ and $g(f(x)) = 4x^2 - 12x + 10$, so $2x^2 - 12x + 11 = 0$ and $x = \frac{12 \pm \sqrt{56}}{4}$.

**F1, example 2 (difficulty 5).** $f(x) = x^2 - 4x + 7$ for $x \ge 2$. Find $f^{-1}$ with its domain and range, and solve $f(x) = f^{-1}(x)$.
*Answer:* $f^{-1}(x) = 2 + \sqrt{x - 3}$, domain $x \ge 3$, range $f^{-1}(x) \ge 2$. The equation has no solution.
*Working:* $f(x) = (x - 2)^2 + 3$, increasing on $x \ge 2$ with range $[3, \infty)$. For an increasing function the graphs of $f$ and $f^{-1}$ can meet only on $y = x$ (if $f(a) = f^{-1}(a) = b$ with $b > a$, applying $f$ to $b > a$ gives $f(b) > f(a) = b$, yet $f(b) = a < b$; $b < a$ fails the same way). $f(x) = x$ means $x^2 - 5x + 7 = 0$, whose discriminant is $-3$. The decision point: solving $f(x) = f^{-1}(x)$ head-on squares a square root and invites extraneous roots; the symmetry argument avoids it.

**F2, example 1 (difficulty 4).** $y$ is inversely proportional to $x^2$, and $y = 5$ when $x = 4$. Find $y$ when $x = 10$, and $x$ when $y = 20$.
*Answer:* $y = 0.8$; $x = \pm 2$ (2 if $x$ is a length).
*Working:* $y = \frac{k}{x^2}$ with $k = 80$.

**F2, example 2 (difficulty 5).** For $y = \frac{2x - 1}{x + 3}$, give the asymptotes, intercepts and range, then solve $\frac{2x - 1}{x + 3} > 1$.
*Answer:* $x = -3$ and $y = 2$; intercepts $\left(\frac{1}{2}, 0\right)$ and $\left(0, -\frac{1}{3}\right)$; range: every real number except 2; the inequality holds for $x < -3$ or $x > 4$.
*Working:* Do not multiply through by $x + 3$, whose sign is unknown. Instead $\frac{2x - 1}{x + 3} - 1 = \frac{x - 4}{x + 3} > 0$, positive when top and bottom share a sign.

**F3, example 1 (difficulty 4).** $y = f(x)$ has a minimum at $(2, -5)$. Give the corresponding point of (a) $f(x - 3) + 1$, (b) $2f(x)$, (c) $f(2x)$, (d) $-f(x)$.
*Answer:* (a) minimum $(5, -4)$; (b) minimum $(2, -10)$; (c) minimum $(1, -5)$; (d) maximum $(2, 5)$.

**F3, example 2 (difficulty 5, long-form).** Prove that every function $f$ defined on all real numbers is the sum of an even function and an odd function, and find them for $f(x) = x^3 + x^2 + 1$.
*Model answer:* (1) Define $g(x) = \frac{f(x) + f(-x)}{2}$ and $h(x) = \frac{f(x) - f(-x)}{2}$. (2) $g(-x) = \frac{f(-x) + f(x)}{2} = g(x)$, so $g$ is even. (3) $h(-x) = \frac{f(-x) - f(x)}{2} = -h(x)$, so $h$ is odd. (4) $g(x) + h(x) = f(x)$. (5) For $x^3 + x^2 + 1$: $g(x) = x^2 + 1$, $h(x) = x^3$. The leap is averaging $f$ with its mirror image, motivated by asking what is left unchanged by $x \to -x$.
*Rubric (10):* 2 for the definitions; 2 for proving $g$ even; 2 for proving $h$ odd; 2 for the sum; 2 for the worked example.

**F4, example 1 (difficulty 4).** Show that $x^3 - 3x - 1 = 0$ has a root between 1 and 2, then use $x_{n+1} = \sqrt[3]{3x_n + 1}$ with $x_0 = 2$ to find it to 3 decimal places.
*Answer:* 1.879.
*Working:* $f(1) = -3 < 0 < 1 = f(2)$. Iterates: 1.912931, 1.888835, 1.882057, 1.880141, 1.879599, 1.879446, 1.879402. Stop when two iterates agree to 3 d.p. ($x_6$ and $x_7$ both round to 1.879); $x_5$ rounds to 1.880, the trap for stopping early. Confirm with a sign change: $f(1.8785) < 0 < f(1.8795)$.

**F4, example 2 (difficulty 5, long-form).** Show that the chord of $y = x^2$ from $x = a$ to $x = a + h$ has gradient $2a + h$, explain what happens as $h$ approaches 0 and why $h = 0$ cannot simply be substituted, then do the same for $y = x^3$.
*Model answer:* (1) Gradient $= \frac{(a + h)^2 - a^2}{h} = \frac{2ah + h^2}{h}$. (2) For $h \ne 0$ this is $2a + h$. (3) As $h$ shrinks the chords approach the tangent and the gradient approaches $2a$. (4) Putting $h = 0$ into the original fraction gives $\frac{0}{0}$, which means nothing; cancelling is only allowed because $h \ne 0$, so we take the value the gradients approach, not the value at $h = 0$. (5) For $x^3$: $\frac{(a + h)^3 - a^3}{h} = 3a^2 + 3ah + h^2 \to 3a^2$.
*Rubric (10):* 2 for the chord fraction; 2 for simplifying with $h \ne 0$; 2 for the limiting gradient; 2 for the $\frac{0}{0}$ explanation; 2 for the cubic.

### 3.3 Drills and the 0.2 project

Lab drills are optional practice beyond homework, unlocked level by level, each about 30 minutes, standard library only. They sit in practice sets of drill slots so that their time carries an estimate (section 1).

**Number Lab (0.1, 3.5 h).** `set.numwork.lab`: `drl.num.place-value-shift` (multiply and divide by powers of 10 with strings and floats, and see where floats drift), `drl.num.euclid` (HCF by Euclid's algorithm, counting steps), `drl.num.last-digits` (`pow(a, n, m)` against the cycle method). `set.propprec.lab`: `drl.num.fraction-to-decimal` (long division digit by digit, detecting the cycle), `drl.num.compound-table` (a year-by-year compound and simple interest table), `drl.num.sqrt-bracket` (bracket $\sqrt{n}$ by integer search, then by halving), `drl.num.fermi-ranges` (multiply factor ranges and report a geometric mean).

**Algebra Lab (0.2, 6 h).** `set.expreq.lab`: numeric identity probing, a linear solver, sigma helpers. `set.lines.lab`: the line through two points with `Fraction`s; $2 \times 2$ and $3 \times 3$ elimination with `Fraction`. `set.quadpoly.lab`: a quadratic solver, polynomial evaluation by Horner's rule, polynomial division on coefficient lists, complex roots with `cmath`. `set.funcs.lab`: function composition and inverses, fixed-point iteration, the trapezium rule.

**Project: Root-finder toolkit** (`prj.alg.root-finder`, kind `toolkit`, 10 h, after level F4). One Python module, standard library only, with a `zqtest` suite. Milestones and hours:

| Milestone | Evidence | Hours |
|---|---|---|
| `solve_linear(a, b)` and `solve_quadratic(a, b, c)`: exact roots when they are rational, floats otherwise, complex roots when the discriminant is negative; the cancellation-safe form $x_1 = \frac{-b - \operatorname{sign}(b)\sqrt{D}}{2a}$, $x_2 = \frac{c}{a x_1}$, with a test that the textbook formula fails on $x^2 + 10^8 x + 1 = 0$ (it returns $-7.45 \times 10^{-9}$ for the root $-1.00 \times 10^{-8}$, a 25% error) | Drill `drl.alg.prj-quadratic`, hidden tests | 3.0 |
| `bisection(f, lo, hi, tol)`, `fixed_point(g, x0, tol, max_iter)` and `secant(f, x0, x1, tol)` (a chord method that needs no derivative), each returning the root and the number of evaluations | Drill `drl.alg.prj-iterative`, hidden tests | 4.0 |
| A one-page results note: evaluation counts for the same three equations by each method; one case where fixed-point iteration diverges and why (the cobweb picture); one case where bisection is fooled by a sign change at an asymptote | Long-form item, `genre: results-note`, 10-point rubric | 3.0 |

Acceptance: every hidden test passes on CPython and Pyodide; the note answers its three questions and scores 7 of 10 or better. The project is not an exit part: 0.2's exit is its topic exam (section 4.3).

---

## 4. Topic exam blueprint

Both papers are the `topic` kind of the exam engine (ASSESSMENT.md 3.1 to 3.8):

- **Conditions.** Timed, no hints, Bertie away app-wide from Start to submission (`away` state), one sitting, no calculator anywhere in the app while the paper is open. Sections share the paper's clock, can be visited in any order, and show a suggested split on the rules screen.
- **Forms.** 3 forms of equal marks, each within 5 percentage points of the declared difficulty mix; 85% of each form's marks come from generator slots drawing on the exam reserve (the rule asks for 50%), and the reserve holds at least $6 \times 3 \times$ count admissible points per generator slot, so six sittings stay fresh. Held-out items never appear in practice, homework, reviews or Bertie's practice picks.
- **Difficulty mix by marks:** 20% at difficulty 2, 50% at 3, 20% at 4, 10% at 5. **Long-form** at most 30% of marks (here 7% and 10%). **Pass mark** 70%, computed exactly on fractions.
- **Timing.** Summed item estimates are 50 minutes (0.1) and 60 minutes (0.2), so the durations follow the 1.5 times rule of ASSESSMENT.md 3.1.
- **After a fail:** a 3-day cool-down and a remediation set of at most 30 items on the skills below 60%. After a pass: a retention sitting from the reserve is offered 30 days later and never changes completion.
- **Test out.** Either paper can be sat before its topic's lessons; a pass credits the topic's hours as tested out (ASSESSMENT.md 7.3).

### 4.1 `exm.number`: 0.1 Number

**Duration** 75 minutes. **Marks** 60. **Items** 22. **Calculator** none. **Pass** 42 of 60.
**Format mix by marks:** numeric 43 (72%), exact expression or fraction 8 (13%), multi-select 3 (5%), sort 2 (3%), long-form 4 (7%).
**Difficulty mix by marks:** d2 12 (20%), d3 30 (50%), d4 12 (20%), d5 6 (10%).

| # | Section | Level | Skill | Format | Difficulty | Marks | Source |
|---|---|---|---|---|---|---|---|
| 1 | A Fluency (25 min) | W1 | Multiply and divide by powers of 10; order decimals | Numeric | 2 | 2 | `gen.num.decimal-scale` |
| 2 | A | W1 | Long multiplication, 3 digits by 2 | Numeric | 2 | 2 | `gen.num.long-multiplication` |
| 3 | A | W1 | Divide a decimal by a decimal | Numeric | 3 | 3 | `gen.num.decimal-scale` |
| 4 | A | W2 | Signed numbers and the order of operations, including $-a^2$ | Numeric | 2 | 2 | `gen.num.order-of-operations` |
| 5 | A | W4 | Mixed-number division and subtraction | Exact fraction | 2 | 2 | `gen.num.fraction-ops` |
| 6 | A | P3 | Zero, negative and fractional indices | Numeric | 2 | 2 | `gen.num.index-laws` |
| 7 | A | P1 | Fraction, decimal and percentage conversion; percentage of an amount | Numeric (2 parts) | 3 | 3 | `gen.num.fdp` |
| 8 | A | W2 | Which expressions equal $48 \times 25$ (laws of arithmetic) | Multi-select | 3 | 3 | held-out pool |
| 9 | A | P4 | Round to 1 significant figure and estimate a calculation | Numeric | 2 | 2 | `gen.num.estimate` |
| 10 | B Reasoning (50 min) | W3 | HCF or LCM in context (buses, tiles) | Numeric | 3 | 3 | `gen.num.hcf-lcm` |
| 11 | B | W3 | Count the factors of a number from its prime factorisation | Numeric | 3 | 3 | `gen.num.count-factors` |
| 12 | B | W4 | Fraction word problem ("of", or how many pieces fit) | Numeric | 3 | 3 | `gen.num.fraction-word` |
| 13 | B | P1 | Recurring decimal to a fraction in lowest terms (method shown as a part) | Exact fraction (2 parts) | 3 | 3 | `gen.num.recurring-to-fraction` |
| 14 | B | P1 | Reverse percentage | Numeric | 3 | 3 | `gen.num.reverse-percent` |
| 15 | B | P1 | Successive changes and percentage points | Numeric (2 parts) | 3 | 3 | `gen.num.compound` |
| 16 | B | P2 | Average speed or weighted average, with a unit conversion | Numeric | 3 | 3 | `gen.num.average-rate` |
| 17 | B | P3 | Simplify a surd expression and rationalise $\frac{k}{a + \sqrt{b}}$ | Exact expression (2 parts) | 4 | 3 | `gen.num.surds` |
| 18 | B | W3 | Last one or two digits of a large power | Numeric | 4 | 3 | `gen.num.last-digit` |
| 19 | B | P2 | Ratio that changes after a transfer (GCSE style) | Numeric | 4 | 3 | `gen.num.ratio-change` |
| 20 | B | P4 | Upper or lower bound of a quotient or difference | Numeric | 4 | 3 | `gen.num.bounds` |
| 21 | B | P4 | Prove that $\sqrt{3}$ is irrational (or that $\sqrt{2} + 1$ is) | Long-form, 10-point rubric scaled to 4 | 5 | 4 | held-out pool, 3 variants |
| 22 | B | P3 | Order four large powers without a calculator | Sort | 5 | 2 | held-out pool |

Marks by level: W1 7, W2 5, W3 9, W4 5, P1 12, P2 6, P3 7, P4 9. Every level carries at least 5 marks; P1 carries most because percentages are the most examined and most used number skill.

### 4.2 `exm.algebra`: 0.2 Algebra

**Duration** 90 minutes. **Marks** 80. **Items** 25. **Calculator** none (answers in exact form). **Pass** 56 of 80.
**Format mix by marks:** expression 28 (35%), numeric 26 (32.5%), interval or solution set 13 (16%), point or curve 3 (4%), sort or match 2 (2.5%), long-form 8 (10%).
**Difficulty mix by marks:** d2 16 (20%), d3 40 (50%), d4 16 (20%), d5 8 (10%).

| # | Section | Level | Skill | Format | Difficulty | Marks | Source |
|---|---|---|---|---|---|---|---|
| 1 | A Expressions and equations (27 min) | E2 | Expand and simplify; factorise fully | Expression (2 parts) | 2 | 4 | `gen.alg.expand`, `gen.alg.factorise-common` |
| 2 | A | E3 | Add or subtract algebraic fractions | Expression | 3 | 3 | `gen.alg.alg-fractions` |
| 3 | A | E3 | Fractional and negative indices with letters | Expression | 2 | 2 | `gen.alg.index-letters` |
| 4 | A | E4 | Linear equation with fractions | Numeric | 3 | 3 | `gen.alg.linear-fractions` |
| 5 | A | E5 | Change the subject when it appears twice | Expression | 3 | 3 | `gen.alg.subject-twice` |
| 6 | A | E6 | Linear and absolute-value inequalities, with the integer solutions | Interval (2 parts) | 3 | 3 | `gen.alg.abs-inequality` |
| 7 | A | E3 | Algebraic proof about consecutive or odd integers | Long-form, scaled to 4 | 4 | 4 | held-out pool, 4 variants |
| 8 | A | E6 | Optimum of a linear objective on a region | Numeric | 4 | 2 | `gen.alg.lp-region` |
| 9 | B Lines and systems (18 min) | L1 | Line through two points; perpendicular through a point and its intercept | Expression (2 parts: d2 2, d3 3) | 2 and 3 | 5 | `gen.alg.line-two-points`, `gen.alg.perpendicular` |
| 10 | B | L2 | Rate of change with units, or distance from a speed-time graph | Numeric | 3 | 3 | `gen.alg.motion-graph` |
| 11 | B | L3 | Solve a $2 \times 2$ system | Numeric pair | 2 | 2 | `gen.alg.system-2x2` |
| 12 | B | L3 | Form and solve a system from words | Numeric | 3 | 3 | `gen.alg.system-word` |
| 13 | B | L3 | Replicate a two-state payoff, or solve a $3 \times 3$ system | Numeric | 4 | 3 | `gen.alg.replication`, `gen.alg.system-3x3` |
| 14 | C Quadratics and polynomials (27 min) | Q1 | Solve by factorising | Solution set | 2 | 2 | `gen.alg.solve-quadratic-factor` |
| 15 | C | Q4 | Optimise a quadratic model by completing the square (revenue, area or squared error) | Numeric (2 parts) | 3 | 3 | `gen.alg.revenue-max`, `gen.alg.least-squares-1d` |
| 16 | C | Q2 | Exact roots by the formula | Solution set | 3 | 3 | `gen.alg.quadratic-formula` |
| 17 | C | Q2, Q3 | Discriminant condition on a parameter; a quadratic inequality | Interval (2 parts) | 3 | 5 | `gen.alg.discriminant-k`, `gen.alg.quadratic-inequality` |
| 18 | C | Q6 | Complex roots of a real quadratic | Expression set | 3 | 3 | `gen.alg.complex-quadratic` |
| 19 | C | Q5 | Factor and remainder theorems: find a coefficient, then factorise a cubic | Expression (2 parts) | 4 | 4 | `gen.alg.factor-theorem` |
| 20 | C | Q3 | A symmetric function of the roots, or a quadratic with transformed roots | Numeric or expression | 5 | 4 | held-out pool |
| 21 | D Functions and graphs (18 min) | F1 | Composite, inverse and domain | Expression and interval (3 parts) | 2 | 4 | `gen.alg.compose`, `gen.alg.inverse`, `gen.alg.domain-range` |
| 22 | D | F3 | Image of a turning point under transformations | Point | 3 | 3 | `gen.alg.transform-point` |
| 23 | D | F2 | Match three equations to graphs (asymptotes, roots, shape) | Match | 3 | 2 | `gen.alg.graph-match` |
| 24 | D | F4 | Run an iteration to 3 d.p. and say whether another rearrangement converges | Numeric (2 parts) | 4 | 3 | `gen.alg.iteration` |
| 25 | D | F4 | Explain an extraneous root and solve a radical equation correctly | Long-form, scaled to 4 | 5 | 4 | held-out pool, 3 variants |

Marks by course: E 24 (30%), L 16 (20%), Q 24 (30%), F 16 (20%), matching the courses' share of lessons and their weight in GCSE and Khan Algebra papers.

### 4.3 Exit-test mapping

The curriculum sets no exit line for 0.1 or 0.2 on their own; Stage 0 closes with four checkboxes (curriculum.md). The schema still needs one exit part per topic (`Topic.exit`, at least one), so each topic's exit part is its own topic exam:

| Exit part | Gate | Confirm | `estHours` |
|---|---|---|---|
| `0.1.exit` | `exm.number` at 70% | None | 0.5 (reviewing the sittings) |
| `0.2.exit` | `exm.algebra` at 70% | None | 1.5 (reviewing the sittings) |

The two topic papers then do a second job: they rehearse, and their held-out pools feed, the Number, Ratio and Algebra content of the Stage 0 exit papers that the sibling file rebuilds (`stage0-precalc-computing.md` 4.4).

**`s0.gcse`, the GCSE-style Paper 1** (80 marks, 90 minutes, non-calculator, at 80%). 52 of its 80 marks come from 0.1 and 0.2: Number 12, Ratio, proportion and rates of change 16, Algebra 24. Geometry (16) and Probability and statistics (12) come from 0.3 courses S and C. Every 0.1 and 0.2 question of the sibling's paper, with the lessons that teach it:

| Q | Strand | Content | Marks | Taught in (this file) |
|---|---|---|---|---|
| 1 | Number | Fraction and mixed-number arithmetic | 2 | W4, lessons 19 to 21 |
| 2 | Number | Standard form calculation | 3 | P3, lesson 36 |
| 3 | Algebra | Expand and simplify; $n$th term of a linear sequence | 4 | E2, lessons 7 to 11; L1, lesson 41 (the sibling cites 0.3 G1, which recaps it) |
| 4 | Ratio | Percentage change and best buy | 4 | P1, lesson 25; P2, lesson 28 |
| 7 | Number | Index laws with negative and fractional indices | 3 | P3, lessons 32 to 34 |
| 8 | Algebra | Linear equation with fractions | 3 | E4, lesson 20 |
| 9 | Algebra | Simultaneous equations, one quadratic or both linear | 3 | L3, lessons 49 to 51; Q3, lesson 71 |
| 10 | Algebra | Quadratics: factorise, complete the square, turning point | 4 | Q1, lessons 55 to 58; Q2, lessons 61 and 62 |
| 11 | Ratio | Sharing in a ratio with a given difference | 3 | P2, lesson 27 |
| 12 | Ratio | Direct or inverse proportion with a formula | 3 | P2, lessons 28 and 29; F2, lesson 96 |
| 13 | Ratio | Compound growth or depreciation with multipliers | 3 | P1, lesson 26 (0.3 G2 adds frequency and $e$) |
| 18 | Number | Surds: simplify and rationalise a denominator | 2 | P3, lesson 35 |
| 19 | Algebra | Algebraic proof about integers | 3 | E3, lesson 17 |
| 20 | Algebra | Composite and inverse functions | 3 | F1, lessons 91 and 92 |
| 21 | Ratio | Gradient of a curve at a point, or area under a velocity-time graph | 3 | L2, lesson 43; F4, lessons 109 and 110 |
| 24 | Number | Recurring decimal to fraction, with the algebraic argument | 2 | P1, lesson 23 |
| 25 | Algebra | Intersection of a line and a circle | 4 | Q3, lessons 71 and 72 |

Totals: Number 12, Ratio 16, Algebra 24, which match the sibling's strand weights.

**`s0.precalc`, the Precalculus challenge** (30 items at 85%). 0.2 supplies the three composite-and-inverse items, drawn from course F's generators (`gen.alg.compose`, `gen.alg.inverse`, `gen.alg.domain-range`), and the foundations that 0.3 extends: complex numbers in rectangular form (Q6, lessons 84 to 87; 0.3 T6), rational functions (lesson 99; 0.3 R3), the circle (lesson 72; 0.3 R4).

**`s0.zetamac` and `s0.script`.** Indirect only: 0.1's number facts and fraction-decimal fluency feed 0.5, and the homework drills give practice at running Python, which 0.4 closes.

**Rehearsal inside the topic exams.** Section B of `exm.number` and sections A and C of `exm.algebra` use GCSE Paper 1 conventions (command words "work out", "show that", "give your answer in its simplest form"; exact answers; no calculator; the intermediate result asked for as its own part where a GCSE mark scheme would give a method mark), so a pass is also practice for `s0.gcse`.

**Optional confirmation** [our recommendation, not a curriculum line]: after passing each topic exam, sit the Khan Academy course challenges of the curriculum's chosen resources (Pre-algebra after 0.1; Algebra 1 and Algebra 2 after 0.2) and log them as outside work; they are not exit instruments, because the instrument union names only the Precalculus challenge. Do not spend real GCSE past papers here: the `s0.gcse` confirm needs an unseen one. Use topic-sorted past-paper questions (Maths Genie, Physics and Maths Tutor) for practice instead.

---

## 5. Reading and resource map per level

**How to use this map.** The app's lessons and homework are the spine. Outside resources fill three roles: a second explanation when a quiz shows a gap (watch or read), more problems (attempt), and stretch (top-programme material). Every budgeted row becomes a `Level.companion` entry (`src`, `loc`, `exercises`, `hours`, `checked: false` until a person confirms the location), and the planner schedules it as outside work (ASSESSMENT.md 8.7, 11). Rows marked **stretch** carry no hours: they are optional, so the budget does not depend on them. Budgeted hours sum to 15.0 for 0.1 and 46.75 for 0.2, the external block of section 1.

**Licences.** Only CC BY sources may be adapted into items (CONTENT-FORMAT.md 9.4); everything else is cited, never copied. Of the sources below only OpenStax's algebra books (CC BY 4.0) are adaptable; OpenStax Calculus is CC BY-NC-SA 4.0 and OpenIntro Statistics is CC BY-SA 3.0, so both are cite-only [searched].

**Resources** (free unless marked paid):

| Id | Resource | Licence | Link |
|---|---|---|---|
| `src.khan-prealgebra` | Khan Academy, Arithmetic and Pre-algebra (the curriculum's 0.1 choice) | Copyright, free | https://www.khanacademy.org/math/arithmetic, https://www.khanacademy.org/math/pre-algebra |
| `src.khan-algebra` | Khan Academy, Algebra 1 and Algebra 2 (the curriculum's 0.2 choice) | Copyright, free | https://www.khanacademy.org/math/algebra, https://www.khanacademy.org/math/algebra2 |
| `src.khan-precalc` | Khan Academy, Precalculus (its rational functions unit only, for lesson 99) | Copyright, free | https://www.khanacademy.org/math/precalculus |
| `src.khan-finance` | Khan Academy, Finance and Capital Markets, the Interest and debt unit ("Introduction to interest", compound interest, $e$ and compounding) [searched, secondary listings] | Copyright, free | https://www.khanacademy.org/economics-finance-domain/core-finance [check URL] |
| `src.corbettmaths` | Corbettmaths: GCSE videos, Practice Questions, textbook exercises and 5-a-day (the curriculum's UK route) | Copyright, free | https://corbettmaths.com/contents/ |
| `src.mathsgenie`, `src.pmt` | Maths Genie and Physics and Maths Tutor: past GCSE questions sorted by topic | Copyright, free | https://www.mathsgenie.co.uk, https://www.physicsandmathstutor.com |
| `src.openstax-prealgebra-2e` | OpenStax, Prealgebra 2e | CC BY 4.0 | https://openstax.org/details/books/prealgebra-2e |
| `src.openstax-elementary-algebra-2e` | OpenStax, Elementary Algebra 2e | CC BY 4.0 | https://openstax.org/details/books/elementary-algebra-2e |
| `src.openstax-intermediate-algebra-2e` | OpenStax, Intermediate Algebra 2e | CC BY 4.0 | https://openstax.org/details/books/intermediate-algebra-2e |
| `src.openstax-college-algebra-2e` | OpenStax, College Algebra 2e | CC BY 4.0 | https://openstax.org/details/books/college-algebra-2e |
| `src.openstax-calculus` | OpenStax, Calculus Volume 1 (Herman and Strang) | CC BY-NC-SA 4.0 [searched] | https://openstax.org/details/books/calculus-volume-1 |
| `src.hammack-proof-3e` | Richard Hammack, Book of Proof, 3rd edition (2018) | CC BY-NC-ND 4.0 [searched] | https://www.people.vcu.edu/~rhammack/BookOfProof/ [searched] |
| `src.mcs-2017` | Lehman, Leighton and Meyer, Mathematics for Computer Science (2017 revision), the MIT 6.042J text | CC BY-SA 3.0 [searched] | https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/ |
| `src.mahajan-street-fighting` | Sanjoy Mahajan, Street-Fighting Mathematics (MIT Press 2010); MIT OCW 18.098, January IAP 2008 | CC BY-NC-SA 3.0 US [searched] | https://ocw.mit.edu/courses/18-098-street-fighting-mathematics-january-iap-2008/ [searched] |
| `src.mahajan-art-of-insight` | Sanjoy Mahajan, The Art of Insight in Science and Engineering (MIT Press 2014); MIT OCW RES.6-011 | CC BY-NC-SA 4.0 [searched] | https://ocw.mit.edu/courses/res-6-011-the-art-of-insight-in-science-and-engineering-mastering-complexity-fall-2014/ [searched] |
| `src.python-docs-float` | Python tutorial, "Floating-Point Arithmetic: Issues and Limitations" | PSF licence | https://docs.python.org/3/tutorial/floatingpoint.html |
| `src.goldberg-1991` | David Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic", ACM Computing Surveys 23(1), 1991 | Copyright | Reference only |
| `src.cs50x` | Harvard CS50x 2026: Week 0, Scratch (binary and representation), Week 1, C (floating-point imprecision, integer overflow) [searched] | CC BY-NC-SA [check] | https://cs50.harvard.edu/x/ |
| `src.mit-1806` | Gilbert Strang, MIT OCW 18.06 Linear Algebra, Spring 2010, video lectures | CC BY-NC-SA | https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/ |
| `src.3b1b-lockdown` | 3Blue1Brown, Lockdown Math (2020); episode 1 is "The simpler quadratic formula" [searched] | Copyright, free | https://www.3blue1brown.com/lessons/ldm-quadratic [searched] |
| `src.3b1b-calculus` | 3Blue1Brown, Essence of Calculus (the curriculum's 1.3 intuition series) | Copyright, free | https://www.3blue1brown.com/topics/calculus |
| `src.welch-imaginary` | Welch Labs, Imaginary Numbers Are Real (13 parts [searched]) | Copyright, free | YouTube, Welch Labs channel |
| `src.openintro-4e` | Diez, Çetinkaya-Rundel and Barr, OpenIntro Statistics, 4th edition | CC BY-SA 3.0 [searched] | https://www.openintro.org/book/os/ |
| `src.blitzstein-hwang-2019` | Blitzstein and Hwang, Introduction to Probability, 2nd edition (the curriculum's 1.5 text) | Free online, copyright | https://projects.iq.harvard.edu/stat110 [check URL] |
| `src.numpy-var` | NumPy documentation, `numpy.var` | BSD | https://numpy.org/doc/stable/reference/generated/numpy.var.html |
| `src.frederick-2005` | Shane Frederick, "Cognitive Reflection and Decision Making", Journal of Economic Perspectives 19(4), 25 to 42, 2005, doi 10.1257/089533005775196732 [searched] | Copyright, free from the journal | https://www.aeaweb.org/articles?id=10.1257/089533005775196732 |
| `src.tlmaths` | TLMaths (Jack Brown): A-level videos by specification section [searched] | Copyright, free | https://www.tlmaths.com [searched] |
| `src.ukmt-challenges` | UK Mathematics Trust: Junior and Intermediate Mathematical Challenge papers with solutions; recent papers free, older ones sold [searched] | Copyright | https://www.ukmt.org.uk |
| `src.mat-papers` | Oxford Mathematics Admissions Test: past papers and solutions from 2010 [searched] | Copyright, free | https://www.maths.ox.ac.uk/r/mat [searched] |
| `src.nrich` | NRICH (University of Cambridge), secondary tasks | Copyright, free | https://nrich.maths.org |
| `src.aops-prealgebra`, `src.aops-intro-algebra` (paid) | Art of Problem Solving: Prealgebra (Patrick, Rusczyk, Boppana) and Introduction to Algebra (Rusczyk); Alcumus (free adaptive problems) | Copyright | https://artofproblemsolving.com |
| `src.gelfand-shen-algebra` (paid) | I. M. Gelfand and A. Shen, Algebra (Birkhäuser 1993, reprinted) | Copyright | Publisher page |
| `src.edexcel-pure` (paid) | Pearson Edexcel AS and A level Mathematics, Pure Mathematics Year 1/AS and Year 2 | Copyright | Publisher page |
| `src.huff-lie` (paid) | Darrell Huff, How to Lie with Statistics (1954) | Copyright | Any edition |
| `src.shreve-1` (paid) | Steven Shreve, Stochastic Calculus for Finance I: The Binomial Asset Pricing Model (Springer 2004) | Copyright | Publisher page |

Khan unit titles, Corbettmaths topic names, AoPS and Edexcel chapter numbers and OpenStax section numbers below are as I recall them [check each against the live resource before the content cites it]. OpenStax section numbers are recalled from the 2e editions and are consistent with each book's table of contents as I know it; Edexcel Pure Year 2 chapter 10 (Numerical methods) I hold with high confidence; Street-Fighting chapters 1 (Dimensions) and 4 (Pictorial proofs) and OpenIntro section 8.1 (Fitting a line, residuals, and correlation) are confirmed [searched].

### 5.1 Item 0.1 Number

| Level | Resource and location | What to do | Hours |
|---|---|---|---|
| W1 | Khan Arithmetic: place value, multi-digit addition and subtraction, multiplication, division, and decimal units | Watch only the videos for skills your lesson quiz flagged; take each unit test to Proficient | 0.5 |
| W1 | Corbettmaths: Place Value, Multiplying and Dividing by 10, 100, 1000, Long Multiplication, Long Division, Decimals (multiplying, dividing) | Attempt all Practice Questions for each topic; mark with the answers | 0.5 |
| W1 | OS Prealgebra 1.1 to 1.5 and 5.1, 5.2 | Read 1.4, 1.5 and 5.2; attempt the odd-numbered exercises of 1.5 and 5.2 (answers at the back) | 0.5 |
| W1 | Gelfand and Shen, the opening sections on the decimal system and the multiplication and division algorithms [check section titles] | **Stretch**: read and attempt every problem in those sections | |
| W2 | Khan Pre-algebra: the two negative numbers units; Exponents intro and order of operations | Unit tests to Proficient | 0.5 |
| W2 | Corbettmaths: Negative Numbers (adding, subtracting, multiplying, dividing), Order of Operations (BIDMAS) | All Practice Questions | 0.5 |
| W2 | OS Prealgebra 3.1 to 3.4 and 7.2 to 7.4 | Read 7.2 to 7.4 (the laws); odd-numbered exercises of 3.4 and 7.3 | 0.5 |
| W2 | AoPS Prealgebra ch. 1, Properties of Arithmetic (paid) | **Stretch**: the chapter's review and challenge problems | |
| W3 | Khan Pre-algebra: Factors and multiples | Unit test to Proficient | 0.5 |
| W3 | Corbettmaths: Factors, Multiples, Primes, Product of Primes, HCF and LCM, Product Rule for Counting | All Practice Questions | 1.0 |
| W3 | OS Prealgebra 2.4, 2.5 | Odd-numbered exercises | 0.5 |
| W3 | MCS ch. 9, Number Theory: divisibility, the greatest common divisor and Euclid's algorithm, modular arithmetic [check: chapter 9 in the 2017 PDF as recalled; the LibreTexts copy numbers it 8 within Part II] | **Stretch**: read the divisibility and gcd sections; attempt 3 class problems | |
| W3 | UKMT Junior Mathematical Challenge | **Stretch**: the number-theory questions among 16 to 25 of two recent papers | |
| W4 | Khan Arithmetic: fractions units; Pre-algebra fraction word problems | Unit tests to Proficient | 0.5 |
| W4 | Corbettmaths: Equivalent Fractions, Simplifying, Ordering, Adding, Subtracting, Multiplying and Dividing Fractions, Mixed Numbers, Fractions of Amounts | All Practice Questions; 5 days of Higher 5-a-day | 1.0 |
| W4 | OS Prealgebra 4.1 to 4.7 | Read 4.2 (multiply and divide); odd-numbered exercises of 4.5 and 4.6 | 0.5 |
| W4 | AoPS Prealgebra ch. 4, Fractions (paid) | **Stretch**: challenge problems | |
| P1 | Khan Pre-algebra: Percentages; Percent and rational number word problems | Unit tests to Proficient | 0.5 |
| P1 | Corbettmaths: Fractions to Decimals, Recurring Decimals to Fractions, Percentages of an Amount, Percentage Change, Reverse Percentages, Compound Interest, Depreciation | All Practice Questions | 1.0 |
| P1 | OS Prealgebra 5.3, 6.1 to 6.4 | Odd-numbered exercises of 6.2 and 6.4 | 0.25 |
| P1 | Khan Finance and Capital Markets: the interest and compounding videos | Watch two videos as a preview of 1.7 | 0.25 |
| P2 | Khan Pre-algebra: Ratios and rates; Proportional relationships | Unit tests to Proficient | 0.5 |
| P2 | Corbettmaths: Ratio (simplifying, sharing, problem solving), Best Buys, Direct and Inverse Proportion, Speed Distance Time, Density, Pressure, Converting Units (including area and volume), Exchange Rates | All Practice Questions | 1.0 |
| P2 | OS Prealgebra 5.6, 6.5, 7.5 | Odd-numbered exercises of 6.5 | 0.5 |
| P2 | Art of Insight, the chapter "Proportional reasoning" (chapter 4 [check]) | **Stretch**: read the first two sections | |
| P3 | Khan Pre-algebra: Roots, exponents and scientific notation; Algebra 1: Exponents and radicals | Unit tests to Proficient | 0.5 |
| P3 | Corbettmaths: Index Laws, Negative and Fractional Indices, Surds (simplifying, rationalising), Standard Form (calculating) | All Practice Questions | 1.0 |
| P3 | OS Prealgebra 5.7, 10.2, 10.5; OS Elementary 9.1 to 9.5 | Odd-numbered exercises of 9.2 and 9.5 | 0.5 |
| P3 | UKMT Intermediate Mathematical Challenge | **Stretch**: powers and surds questions from two papers | |
| P4 | Corbettmaths: Rounding (decimal places, significant figures), Estimation, Error Intervals, Upper and Lower Bounds | All Practice Questions | 0.5 |
| P4 | Khan Algebra 1: Irrational numbers | Unit test to Proficient | 0.25 |
| P4 | Book of Proof ch. 6, Proof by Contradiction | Read the proofs that $\sqrt{2}$ is irrational and that there are infinitely many primes; attempt 3 odd-numbered exercises | 0.5 |
| P4 | Python floating-point tutorial; CS50x Week 0, the binary segment | Read the tutorial in full (15 minutes); watch the segment | 0.5 |
| P4 | Art of Insight ch. 1, Divide and Conquer | Read; redo its first estimate yourself before reading the answer | 0.25 |
| P4 | MCS ch. 1, Proofs, the proof-by-contradiction section [check section number] | **Stretch**: read | |
| P4 | Goldberg (1991) | Reference only: read the rounding-error introduction when 1.1 needs it | |

Budgeted hours by level: W1 1.5, W2 1.5, W3 2.0, W4 2.0, P1 2.0, P2 2.0, P3 2.0, P4 2.0; total 15.0.

### 5.2 Item 0.2 Algebra

| Level | Resource and location | What to do | Hours |
|---|---|---|---|
| E1 | Khan Algebra 1: Algebra foundations | Unit test to Proficient | 0.75 |
| E1 | Corbettmaths: Algebraic Notation, Substitution, Collecting Like Terms, Expressions, Equations, Formulae and Identities | All Practice Questions | 0.75 |
| E1 | OS Elementary 1.2, 6.2 | Odd-numbered exercises of 1.2 and 6.2 | 0.75 |
| E1 | AoPS Introduction to Algebra ch. 1 and 2 (paid) | **Stretch**: review problems | |
| E2 | Khan Algebra 1: Quadratics: Multiplying and factoring (the multiplying binomials lessons) | Practise the multiplying skills to Proficient | 0.5 |
| E2 | Corbettmaths: Expanding Brackets (single, double, triple), Factorising (common factor) | All Practice Questions | 1.0 |
| E2 | OS Elementary 6.3, 6.4, 7.1 | Odd-numbered exercises of 6.4 and 7.1 | 0.75 |
| E2 | Gelfand and Shen, the sections on the square of a sum and the difference of squares (paid) | **Stretch**: every problem in those sections | |
| E3 | Corbettmaths: Algebraic Fractions (simplifying, adding, multiplying, dividing), Index Laws (algebraic), Algebraic Proof | All Practice Questions | 1.0 |
| E3 | OS Elementary 8.1 to 8.4; OS College Algebra 9.4, Series and Their Notations | Odd-numbered exercises of 8.4; read the sigma examples in 9.4 | 0.75 |
| E3 | Book of Proof ch. 4, Direct Proof | Read the definitions of even and odd and the first examples; attempt 4 exercises | 0.75 |
| E3 | MAT past papers, question 1 multiple-choice parts on algebraic manipulation | **Stretch**: 5 parts, untimed | |
| E4 | Khan Algebra 1: Solving equations and inequalities | Unit test to Proficient | 0.75 |
| E4 | Corbettmaths: Solving Equations (all types), Forming and Solving Equations | All Practice Questions | 1.0 |
| E4 | OS Elementary 2.1 to 2.5, 3.1 | Odd-numbered exercises of 2.5 and 3.1 | 0.5 |
| E4 | Frederick (2005) | Read the first section: the three questions and why intuition fails | 0.25 |
| E5 | Khan Algebra 1: Working with units; the rearranging-formulas lessons | Unit test to Proficient | 0.5 |
| E5 | Corbettmaths: Formulae (substitution), Changing the Subject | All Practice Questions | 0.75 |
| E5 | OS Elementary 2.6 | Odd-numbered exercises | 0.25 |
| E5 | Street-Fighting ch. 1, Dimensions | Read; do the pendulum and drag examples yourself before reading the solutions | 0.5 |
| E6 | Khan Algebra 1: Inequalities (systems and graphs); Absolute value and piecewise functions | Unit tests to Proficient | 0.75 |
| E6 | Corbettmaths: Inequalities (number line, solving, regions), Set Notation | All Practice Questions | 1.0 |
| E6 | OS Intermediate 2.5 to 2.7, 4.7 | Odd-numbered exercises of 2.6 and 2.7 | 0.75 |
| E6 | AoPS Introduction to Algebra, Introduction to Inequalities chapter (paid) | **Stretch**: challenge problems | |
| L1 | Khan Algebra 1: Linear equations and graphs; Forms of linear equations; Sequences | Unit tests to Proficient | 1.0 |
| L1 | Corbettmaths: Coordinates, Gradient, $y = mx + c$, Equation of a Line, Parallel and Perpendicular Lines, Midpoint, nth Term | All Practice Questions | 1.0 |
| L1 | OS Elementary 4.1 to 4.6 | Odd-numbered exercises of 4.5 and 4.6 | 0.75 |
| L1 | Edexcel Pure Year 1 ch. 5, Straight line graphs (paid); TLMaths, coordinate geometry of straight lines | **Stretch**: the chapter's mixed exercise | |
| L2 | Corbettmaths: Real Life Graphs, Distance-Time Graphs, Velocity-Time Graphs, Area under a graph | All Practice Questions | 1.25 |
| L2 | OS Intermediate 3.1 to 3.3 | Odd-numbered exercises of 3.2 | 0.5 |
| L2 | OpenIntro Statistics section 8.1, Fitting a line, residuals, and correlation [searched] | Read as a preview of 1.6 | 0.5 |
| L2 | Huff, How to Lie with Statistics, ch. 5, "The Gee-Whiz Graph" (paid) | **Stretch**: read (10 minutes) | |
| L3 | Khan Algebra 1: Systems of equations | Unit test to Proficient | 0.75 |
| L3 | Corbettmaths: Simultaneous Equations (elimination, substitution, graphical, forming) | All Practice Questions | 0.75 |
| L3 | OS Elementary 5.1 to 5.5; OS Intermediate 4.4 (three variables), 4.6 (determinants) | Odd-numbered exercises of 5.4 and 4.4 | 0.75 |
| L3 | MIT 18.06 lecture 1, "The geometry of linear equations" | Watch after lesson 49; pause at each system and predict the picture | 0.75 |
| L3 | MIT 18.06 lecture 2, "Elimination with matrices"; Shreve I ch. 1, the one-period binomial model (paid) | **Stretch**: lecture 2 after lesson 53; Shreve after lesson 54, comparing its replication with yours | |
| Q1 | Khan Algebra 1: Quadratics: Multiplying and factoring; Quadratic functions and equations (solving by factoring) | Unit tests to Proficient | 0.75 |
| Q1 | Corbettmaths: Factorising Quadratics ($a = 1$ and $a > 1$), Difference of Two Squares, Solving Quadratics by Factorising | All Practice Questions | 1.0 |
| Q1 | OS Elementary 7.2 to 7.6 | Odd-numbered exercises of 7.3 and 7.6 | 0.75 |
| Q1 | AoPS Introduction to Algebra, Quadratic Equations Part 1 and Special Factorizations (paid) | **Stretch**: challenge problems | |
| Q2 | Khan Algebra 1: Quadratic functions and equations (completing the square, the formula, the discriminant) | Unit test to Proficient | 0.5 |
| Q2 | Corbettmaths: Completing the Square, Quadratic Formula, Turning Points | All Practice Questions | 0.75 |
| Q2 | OS Elementary 10.1 to 10.3; OS Intermediate 9.1 to 9.4 | Odd-numbered exercises of 10.3 and 9.4 | 0.5 |
| Q2 | 3Blue1Brown Lockdown Math episode 1, "The simpler quadratic formula" | Watch after lesson 64; answer each live question before the reveal | 0.75 |
| Q3 | Khan Algebra 1: Quadratic functions and equations (graphs and features) | Practise the graphing skills to Proficient | 0.5 |
| Q3 | Corbettmaths: Quadratic Graphs, Quadratic Inequalities, Simultaneous Equations (non-linear), Equation of a Circle, Equation of a Tangent to a Circle | All Practice Questions | 1.25 |
| Q3 | OS Intermediate 9.6 to 9.8, 11.1; OS College Algebra 5.1 | Odd-numbered exercises of 9.8 and 11.1 | 1.0 |
| Q3 | Edexcel Pure Year 1 ch. 2, 3 and 6, Circles (paid); MAT question 1 parts on quadratics and roots | **Stretch**: mixed exercises; 5 MAT parts | |
| Q4 | OS College Algebra 5.1, the maximum and minimum applications | Odd-numbered application exercises | 0.75 |
| Q4 | Street-Fighting ch. 4, Pictorial Proofs (the arithmetic and geometric mean picture) | Read; reproduce the picture for $(a + b)^2 \ge 4ab$ | 0.75 |
| Q4 | NumPy documentation for `numpy.var` | Read the Notes: it computes variance from deviations from the mean, lesson 76's safe form | 0.25 |
| Q4 | Blitzstein and Hwang 4.6, Variance [check section number] | Preview of 1.5: read the definition and the identity $\text{Var}(X) = E(X^2) - (EX)^2$ only | 0.5 |
| Q4 | Gelfand and Shen, the sections on the maximum and minimum of a quadratic and on arithmetic and geometric means (paid) | **Stretch**: every problem in those sections | |
| Q5 | Khan Algebra 2: Polynomial arithmetic; Polynomial division; Polynomial factorization; Polynomial graphs | Unit tests to Proficient | 0.75 |
| Q5 | Corbettmaths: Quadratic Sequences (nth term) | All Practice Questions | 0.25 |
| Q5 | TLMaths: algebraic division and the factor theorem | Watch if lesson 80's quiz was not Mastered | 0.5 |
| Q5 | OS College Algebra 5.2 to 5.5 | Odd-numbered exercises of 5.4 and 5.5 | 1.0 |
| Q5 | Edexcel Pure Year 1 ch. 7, Algebraic methods (paid) | **Stretch**: mixed exercise | |
| Q6 | Khan Algebra 2: Complex numbers | Unit test to Proficient | 1.0 |
| Q6 | OS College Algebra 2.4; OS Intermediate 8.8 | Odd-numbered exercises of 2.4 | 0.75 |
| Q6 | Welch Labs, Imaginary Numbers Are Real, parts 1 to 5 | Watch for the history behind lesson 84 | 0.5 |
| Q6 | AoPS Introduction to Algebra, Complex Numbers chapter (paid) | **Stretch**: challenge problems | |
| F1 | Khan Algebra 1: Functions; Algebra 2: the composition and inverse lessons | Unit tests to Proficient | 0.75 |
| F1 | Corbettmaths: Function Notation, Composite Functions, Inverse Functions | All Practice Questions | 0.75 |
| F1 | OS College Algebra 3.1 to 3.4, 3.6, 3.7 | Odd-numbered exercises of 3.4 and 3.7 | 1.0 |
| F1 | Edexcel Pure Year 2 ch. 2, Functions and graphs (paid) | **Stretch**: mixed exercise | |
| F2 | Khan Algebra 1: Exponential growth and decay; Khan Precalculus: Rational functions | Practise to Proficient | 0.75 |
| F2 | Corbettmaths: Cubic, Reciprocal and Exponential Graphs, Recognising Graphs, Direct and Inverse Proportion (algebraic) | All Practice Questions | 1.0 |
| F2 | OS College Algebra 5.6, 5.8, 6.1 | Odd-numbered exercises of 5.6 | 0.75 |
| F2 | Edexcel Pure Year 1 ch. 4, Graphs and transformations, first half (paid) | **Stretch** | |
| F3 | Khan Algebra 2: Transformations of functions | Unit test to Proficient | 0.5 |
| F3 | Corbettmaths: Transformations of Graphs | All Practice Questions | 0.5 |
| F3 | OS College Algebra 3.5 | Odd-numbered exercises | 0.5 |
| F3 | OpenIntro Statistics ch. 4, the standardising (Z-score) subsection [check] | Read as a preview of 1.5 | 0.5 |
| F4 | Corbettmaths: Iteration, Gradient of a Curve, Area under a graph [searched: these titles exist] | All Practice Questions | 1.0 |
| F4 | TLMaths, A-level numerical methods: locating roots and iteration | Watch the locating-roots videos; attempt their examples first | 0.5 |
| F4 | OpenStax Calculus Volume 1, section 2.1, A Preview of Calculus | Read: secants approaching a tangent, and areas by rectangles | 0.75 |
| F4 | 3Blue1Brown, Essence of Calculus chapters 1 and 2 | Watch (the curriculum names this series for 1.3; here it previews it) | 0.75 |
| F4 | Edexcel Pure Year 2 ch. 10, Numerical methods (paid) | **Stretch**: locating roots and iteration exercises | |

Budgeted hours by level: E1 2.25, E2 2.25, E3 2.5, E4 2.5, E5 2.0, E6 2.5, L1 2.75, L2 2.25, L3 3.0, Q1 2.5, Q2 2.5, Q3 2.75, Q4 2.25, Q5 2.5, Q6 2.25, F1 2.5, F2 2.5, F3 2.0, F4 3.0; total 46.75.

**Throughout 0.2 (stretch).** AoPS Alcumus on the Introduction to Algebra topics, 20 problems a week; NRICH secondary algebra tasks for open problems.

---

## 6. Verification approach

Every answer in these two topics is machine-checked twice before it ships (CONTENT-FORMAT.md section 6): the declared answer, or the TypeScript generator's answer, against an independent Python computation, and then the runtime grader is replayed on the correct answer, its accepted forms and every diagnosed wrong answer. The table says what the independent side and the second check are for each family. "Fraction" means Python's exact `fractions.Fraction`; "probe" means evaluation at 20 random points of the declared domain with mpmath at 50 digits; SymPy runs in CI only.

### 6.1 Item families in 0.1

| Family | Lessons | Independent check (CI) | Second check | Runtime grading and accepted forms |
|---|---|---|---|---|
| Place value, written methods, decimal arithmetic, order of operations | 1 to 10 | Evaluate the expression tree with `Fraction` | `decimal.Decimal` at 50 digits; for long-division items, the digit-by-digit algorithm with remainders | Numeric, exact; accepted forms include trailing zeros (30.5, 30.50) and, where asked, fractions |
| Signed numbers and laws of arithmetic | 6 to 10 | `Fraction` evaluation of every option | For "which are equal" items, every option compared pairwise; no two distractors equal | Multi-select scored per option in homework, all-or-nothing in quizzes |
| Primes, factors, HCF, LCM, factor counts | 11 to 14 | SymPy `factorint`, `divisors`, `igcd`, `ilcm` | Brute-force trial division and enumeration up to $10^6$ | Numeric exact; prime-power forms by structural check (primes ascending, exponents) |
| Product-rule counting | 13 | Product of choice counts | Exhaustive enumeration of the outcome space | Numeric exact |
| Divisibility, remainders, last digits | 15, 16 | `pow(a, n, m)` | Cycle detection by iteration, stopping at the first repeated state | Numeric exact |
| Fractions and mixed numbers | 17 to 21 | `Fraction` | Decimal evaluation to 30 digits | Exact fraction or equivalent (8/3, 2 2/3, 16/6 accepted unless "simplest form" is asked, which a structural test checks) |
| Terminating and recurring decimals | 22, 23 | `Fraction`, and the denominator test ($2^a 5^b$ after cancelling) | Long division by remainders to find the cycle; the cycle must reproduce the fraction | Exact fraction; recurring notation parsed by `num-parse` |
| Percentages, multipliers, compound growth | 24 to 26 | `Fraction` multipliers; reverse items checked by applying the forward change to the answer | Float recomputation must sit within one hundredth of the tolerance | Numeric; money to the penny with a stated rounding rule; percentage and decimal forms both accepted where the question allows |
| Ratio, proportion, rates, units | 27 to 31 | `Fraction`; unit chains through the `unit-algebra` service's dimension vectors (the result's dimension must equal the target's) | Recompute by the unit-rate method and by scaling; both must agree | Numeric with unit; accepted unit symbols listed per item |
| Powers, roots, surds, standard form | 32 to 36 | SymPy `simplify`, `nsimplify`, `radsimp` | Probe numerically; "simplest surd" means $a\sqrt{b}$ with $b$ square-free (checked by `factorint`), "rationalised" means no root in a denominator, standard form means $1 \le A < 10$ | Expression equivalence plus the structural form test |
| Rounding, significant figures, error intervals | 37, 39 | `Decimal.quantize` with an explicit rounding mode | Brute force: round every number on a fine grid of the interval and confirm the interval's ends | Numeric to the stated precision; intervals with open and closed ends compared exactly |
| Bounds of computed quantities | 39 | Evaluate at every corner of the input box with `Fraction` | Check monotonicity in each input with SymPy's derivative sign over the box, which catches a variable that appears twice (homework P4) | Numeric exact or to the stated precision |
| Estimation | 38 | The exact value and each 1-significant-figure rounding | The estimate must be the declared one and must lie within a factor of 2 of the exact value | Numeric within the declared estimate's tolerance |
| Fermi estimates | 40 | The product of the learner's factor values is recomputed; the reference value carries a cited source | The accepted range (a factor of 3 either side of the reference) must contain the sourced value | Log-range check; factors graded for plausibility only in homework rubric points |
| Proofs ($\sqrt{2}$, primes, digit sums, $(-a)(-b)$) | 8, 15, 41; homework | Ordering items: the declared order satisfies every `before` pair; numeric claims in the model answer ($30{,}031 = 59 \times 509$) checked as arithmetic claims | Rubric anchoring: every rubric point names model-answer lines, every line is used | Ordering graded per line; long-form self-marked against the rubric with Bertie's suggestion |
| Binary and floating point | 42 | `int(s, 2)`, `bin(n)` | Python's own float results recorded on CPython and on Pyodide; any difference between the two fails CI, because both targets run Pyodide (`ARCHITECTURE.md` decision 15) | Numeric exact; predicted-output items compare text |

### 6.2 Item families in 0.2

| Family | Lessons | Independent check (CI) | Second check | Runtime grading and accepted forms |
|---|---|---|---|---|
| Expressions: substitute, collect, expand, factorise | 1 to 11 | SymPy `expand`, `factor`, `simplify(a - b) == 0` | Probe at 20 points; for "factorise fully", compare `factor_list` (irreducible factors over the integers and the content) | Compute Engine parse, 8-point probing in the declared domain, plus the structural test for the required form (CONTENT-FORMAT.md decision 10) |
| Algebraic fractions | 12 to 14, 60 | SymPy `cancel`, `together` | The excluded values: every zero of every denominator, including a divisor's numerator, compared with the author's list as a set | Expression equivalence with the domain restriction; excluded values as a set item |
| Index laws with letters | 15 | SymPy with `positive=True` only where the item states $x > 0$ | Probe at negative points when no assumption is stated, which catches $\sqrt{x^2} = x$ | As expressions |
| Sigma notation and the variance identity | 16, 76 | SymPy `summation` on symbolic sums | Random integer data sets evaluated both ways with `Fraction` | Numeric or expression |
| Algebraic proof and "show that" | 17, 22; homework | Derivation chains: every bound line equal to the first (CONTENT-FORMAT.md 6.8), for example $n(n + 1)(n + 2)(n + 3) + 1 = (n^2 + 3n + 1)^2$ | Rubric anchoring | Ordering items graded per line; long-form self-marked with Bertie's suggestion |
| Linear equations, formulae and subjects | 18 to 27 | SymPy `solveset` over the reals; "no solution" and "every $x$" as `EmptySet` and `Reals` | Substitute the answer back with exact arithmetic; for rearrangements, compose the formula with its rearrangement and probe for the identity | Numeric or expression; rearrangements accepted in any equivalent form |
| Dimensional analysis | 28 | Exponents from a linear system in SymPy `linsolve` | Dimension vectors from `unit-algebra` | Expression for exponents; multi-select for consistency |
| Inequalities in one variable (linear, compound, absolute value, quadratic) | 29 to 32, 34, 70 | SymPy `solve_univariate_inequality` returning an exact `Interval` or `Union` | Sampling 10,000 points across and at the endpoints; integer lists by enumeration | Interval check with open and closed ends; set notation and interval notation both parsed |
| Regions and linear programming | 33 | Vertices as exact intersections with `Fraction`; feasibility checked against every constraint; optimum over vertices | Brute-force integer grid for whole-number variants | Region by predicate on sample points; optimum numeric |
| Straight lines, midpoints, distances | 35 to 40 | `Fraction` gradients and intercepts; SymPy for exact distances | Point-on-line checks for every given point; perpendicular gradients multiply to $-1$ | Expression (any equivalent form of the line), numeric |
| Sequences and finite differences | 41, 83 | Closed form against the listed terms for $n = 1$ to 20 | Difference table recomputed independently | Expression in $n$ |
| Graph readings: rates, motion, tariffs, tax | 42 to 45 | Exact gradients and areas from the piecewise-linear data with `Fraction` | Numeric integration of the same data | Numeric with units |
| Fitting a line by eye | 46 | NumPy `lstsq` gives the least-squares minimum on the seeded data | The learner's sum of squared residuals must be within the item's tolerance (for example 15%) of that minimum | Curve check with tolerance |
| Linear systems ($2 \times 2$, $3 \times 3$, degenerate) | 48 to 53 | SymPy `linsolve` | Gaussian elimination with `Fraction` written separately; classification by the ranks of the coefficient and augmented matrices | Numeric tuple; classification as a choice |
| Replication pricing | 54; homework L3 | Solve the replication system exactly | Risk-neutral formula $q = \frac{R - d}{u - d}$ must give the same price | Numeric |
| Quadratics: factorise, complete the square, formula, discriminant, roots and coefficients | 55 to 69 | SymPy `factor`, `solveset` over reals and complexes, `discriminant` | Vieta: the roots' sum and product equal $-\frac{b}{a}$ and $\frac{c}{a}$; vertex by completing the square equals $-\frac{b}{2a}$ | Solution sets; vertex form by structural test; exact surds |
| Quadratic graphs and circles | 67, 68, 71, 72 | SymPy for intercepts, vertex, centre and radius; tangency by a zero discriminant | Points substituted exactly | Curve and point checks with tolerance; features listed per item |
| Optimisation with quadratics | 73 to 77 | Vertex by completing the square in SymPy | Dense grid search over the allowed range, which also catches a boundary optimum | Numeric |
| Polynomials: arithmetic, division, factor theorem, cubics, graphs | 78 to 82 | SymPy `div`, `rem`, `factor`, `roots` | Rational-root candidates enumerated; remainders by evaluation $f(a)$ | Expression, solution set, curve |
| Complex numbers | 84 to 87 | SymPy with `I`, `expand`, `conjugate`, `Abs` | Python `complex` arithmetic | Expression with $i$; points on the complex plane |
| Functions: evaluation, domain, range, composition, inverse | 88 to 92 | SymPy `continuous_domain` and `function_range`; `solve` for inverses | $f(f^{-1}(x)) = x$ probed across the stated domain | Expression and interval |
| Piecewise and modulus | 93 | SymPy `Piecewise` evaluated at each piece's boundary | Sampling on both sides of every kink | Curve and numeric |
| Graph shapes, asymptotes, matching | 94 to 100 | SymPy `limit` for asymptotes; roots and intercepts exactly | Sampled sketches compared to the target within a band | Card-sort mapping; curve band with features |
| Transformations, parity, rescaling | 101 to 105 | Apply the transformation symbolically and compare | Mapped points checked exactly; $f(-x) \mp f(x)$ simplifies to 0 | Expression, point, numeric |
| Iteration | 107 | Iterate in mpmath at 50 digits; fixed point by `nsolve`; convergence predicted from $\lvert g'(x^*) \rvert < 1$ | Float iteration as the learner's calculator would do it; the rounded answer must be stable for 3 further iterates | Numeric to the stated precision |
| Bisection | 108 | Midpoints and signs with `Fraction` | Step count against $\left\lceil \log_2 \frac{\text{width}}{\text{tol}} \right\rceil$ | Numeric; predicted output for the code item |
| Chords, tangents, trapezia | 109, 110 | SymPy `limit` and exact trapezium sums | Over or under from the sign of the second derivative on the interval (SymPy), never shown to the learner | Numeric or expression |
| Radical and rational equations | 111 | Candidates from the cleared equation; each substituted into the original exactly | The extraneous list must equal the author's | Solution set |

### 6.3 Code drills, generators and long-form items

- **Code drills.** Each drill ships `reference.py`, `starter.py`, `tests.py` (the `zqtest` library) and a `wrong/` folder of known-wrong solutions, each naming the misconception it encodes and the test it must fail: for example `count_factors` testing divisors only up to $\frac{n}{2}$ (slow but right, so it must fail the time limit), `solve_quadratic` dividing only the root by $2a$, `bisection` that stops on an asymptote. CI runs every reference, every wrong solution and every mutant on CPython and on Pyodide (CONTENT-FORMAT.md 6.11); every drill in this file declares `needs: []` (standard library only).
- **Generators.** Each family above is a TypeScript generator with a Python verifier written from its specification without reading the TypeScript; CI enumerates the whole parameter box and requires agreement on admissibility, difficulty, answer and every misconception value (CONTENT-FORMAT.md 5.6), plus the tidy-number bounds of widgets-stage0.md 12.2.
- **Long-form items.** Never auto-passed or auto-failed. CI checks the model answer (its bindable lines as derivation chains, its numbers as arithmetic claims) and the rubric's anchoring. The learner's mark is their own, with Bertie's per-point suggestion and evidence quote shown beside it.

---

## 7. Sample lesson in full: What a digit is worth

**Why this lesson.** It is the root of the whole dependency graph: decimals, written methods, standard form, rounding, bounds, binary and floating point all rest on place value. It is also the first lesson the depth-first build ships, so it doubles as the engine's first real content. It is written at the level of detail an author hands to the YAML stage (CONTENT-FORMAT.md sections 3.7, 3.10 and 10): every screen, widget configuration in plain words, check, accepted forms, diagnosis, hint ladder, Why?, Show solution text and tutor fields. Copy follows design research 9.2: second person, sentences of at most 20 words, no exclamation marks, a term named only after it has been used.

**Rules that apply to every screen here.**

- **Hints** open after the lesson's first Check, anywhere in the lesson (design research 5.5; AI-TUTOR.md 2.2), and climb Nudge, Point, Step. Show solution appears after two not-yet results on a screen (design research 5.4).
- **Element references** use `<widget id>/<kind>:<name>` (CONTENT-FORMAT.md decision 17). The place-value chart's columns are `col:thousands`, `col:hundreds`, `col:tens`, `col:ones`, `col:tenths`, `col:hundredths`, `col:thousandths` and `col:ten-thousandths`; in the money skin the headers read £100, £10, £1, 10p and 1p, but the ids stay the place names.
- **Bertie's face** follows the lesson player (BERTIE.md 5.3): `correct` or `notyet` on grading, `surprised` on the trap reveal (screen 6), `celebrate` when the lesson completes. During a problem only the quiet states play.
- **Tutor fields** carry no value that a screen's check accepts (CONTENT-FORMAT.md 3.10, the leak lint). On screen 10, where the accepted boxes include ten, one and a tenth, the tutor fields spell numbers in words so that the lint cannot mistake a phrase for an answer.

### 7.1 Lesson header

| Field | Value |
|---|---|
| `id`, `rev`, `status` | `lsn.numwork.digit-worth`, 1, `draft` |
| `title` | What a digit is worth |
| Position | Course W (How Numbers Work), level W1, lesson 1 of 5; 0.1 lesson 1 |
| `summaryLine` | A digit's worth depends on its column, and multiplying by 10 moves every digit one column left. |
| `frame.why` | With only ten symbols we could name only ten numbers. Columns let the same ten digits name every number, and they turn multiplying by 10 into a shift instead of a calculation. |
| `frame.before` | This is the first lesson of the path. |
| `insight` | Each column is worth ten times the one to its right, so multiplying by 10 moves every digit one column left while the point stays still. |
| `introduces` | `skl.num.place-value`, `skl.num.decimal-place-value`, `skl.num.shift-by-ten`, `skl.num.compare-decimals` |
| `uses`, `requires` | none |
| `terms` | `gls.num.digit`, `gls.num.place-value`, `gls.num.column-value`, `gls.num.decimal-point`, `gls.num.tenth`, `gls.num.hundredth`, `gls.num.placeholder-zero`, `gls.num.pip` |
| Common trap | "To multiply by 10, add a zero" (screen `times10`, then the summary's trap line) |
| `edgeCases` | A zero between digits holds a column open (`fewest`, `zeros`); a zero at the end after the point changes nothing (`zeros`); dividing can open an empty column that needs a placeholder zero, $4.7 \div 100 = 0.047$ (`rule`) |
| `workedExample` | `at: times10`. Naive: "Add a zero, giving 3.050." Decision: "Decide what moves. Every digit moves one column left; nothing is added on." |
| `est` | 15 minutes, the budget unit of decision 1: 12 screens estimated at 600 seconds, a 4-item quiz at about 3 minutes, and about 2 minutes for hints, Why? panels and second tries. Draft 2 said 13, which would have left `Lesson.est` short of section 1.1's 10.5 h |
| `sources` | `src.khan-prealgebra` (`parallel-reading`, Arithmetic, the place value units [check unit titles]); `src.openstax-prealgebra-2e` (`parallel-reading`, sections 1.1 and 5.1) |
| `art` | `ast.course-art.place-value`: Bertie holding a £1 coin in one hand and a 1p coin in the other |

**Misconceptions this lesson diagnoses** (new library entries, `mc.num.*`). Sources for the decimal misconceptions, cited on the library entries: Resnick, Nesher, Leonard, Magone, Omanson and Peled, "Conceptual bases of arithmetic errors: the case of decimal fractions", Journal for Research in Mathematics Education 20(1), 8 to 27, 1989 [searched]; Steinle and Stacey, "The incidence of misconceptions of decimal notation amongst students in Grades 5 to 10", in Kanes, Goos and Warren (eds), Teaching Mathematics in New Times, Proceedings of MERGA 21, vol. 2, 548 to 555, 1998 [searched]. Steinle and Stacey test exactly this lesson's task, choosing the larger of two decimals, and describe the longer-is-larger thinking.

| Id | `belief`, as a learner would put it | `correction` |
|---|---|---|
| `mc.num.face-value` | "The 7 in 4,725 is worth 7." | A digit's worth is the digit times its column's value. |
| `mc.num.column-miscount` | "The 7 is in the tens." | Count columns from the ones column outwards. |
| `mc.num.no-exchange` | "Thirty £10 notes is a fine way to write 300." | Ten of one column make one of the next; the digits record the fewest pieces. |
| `mc.num.drop-placeholder` | "305 and 35 are the same digits, so the zero does not matter." | A zero between digits holds a column open and keeps other digits in place. |
| `mc.num.add-a-zero` | "To multiply by 10, write a 0 on the end." | Multiplying by 10 moves every digit one column left; a 0 appears on the end only for whole numbers. |
| `mc.num.shift-whole-part-only` | "Multiplying by 10 moves the whole-number part; the decimals stay." | Every part grows ten times, so every digit moves. |
| `mc.num.shift-count` | "Dividing by 100 moves one place." | $\times$ or $\div$ 10, 100, 1,000 move digits 1, 2, 3 columns. |
| `mc.num.wrong-direction` | "Dividing moves the digits left." | Dividing makes pieces smaller, so digits move right. |
| `mc.num.longer-is-larger` | "0.45 is bigger than 0.5 because 45 is bigger than 5." | Compare column by column from the left; length does not matter. |
| `mc.num.round-then-compare` | "0.45 rounds to 0.5, so they are equal." | Rounding changes a number; equality needs every column to match. |
| `mc.num.trailing-zero-matters` | "3.50 is bigger than 3.5." | A final zero after the point moves no digit and changes no value. |
| `mc.num.unit-slip` | "The 5 in £3.05 is worth 5." | Right in pence; the question asks for pounds. |

**Screen map.**

| # | Id | Type | Task | Difficulty | Widgets | Est. |
|---|---|---|---|---|---|---|
| 1 | `title` | `title` | none | none | art only | 15 s |
| 2 | `fewest` | `problem` (the hook) | build £305 from the fewest pieces | 1 | `place-value-chart` (input by `answer:`) | 75 s |
| 3 | `columns` | `problem` (names the idea) | the worth of a digit | 1 | `place-value-chart`, `numeric-input` | 45 s |
| 4 | `pence` | `ladder` | a digit after the point | 2 | `place-value-chart`, `numeric-input` | 50 s |
| 5 | `times10` | `ladder` (the worked example) | predict $3.05 \times 10$ | 2 | `place-value-chart`, `numeric-input` | 60 s |
| 6 | `bigger` | `trap` | 0.45 against 0.5 | 2 | `choice`, `number-line` | 40 s |
| 7 | `order` | `ladder` | place four decimals on a line | 2 | `number-line` (input by `answer:`) | 75 s |
| 8 | `zeros` | `problem` (the edge case) | which zeros matter | 2 | `choice` (many), `place-value-chart` | 50 s |
| 9 | `rule` | `generalise` | $4.7 \div 100$ | 2 | `place-value-chart`, `numeric-input` | 50 s |
| 10 | `why-shift` | `derive` | complete the line that proves the shift | 3 | `derivation-steps` | 70 s |
| 11 | `pips` | `problem`, `context: quant` (the transfer) | count pips | 2 | `place-value-chart`, `numeric-input` | 50 s |
| 12 | `summary` | `summary` | none | none | none | 20 s |

Two non-task screens (title and summary), the limit of design research 5.8. Screen estimates total 600 seconds; the quiz adds about 3 minutes.

### 7.2 Screens

#### Screen 1: `title`

- **Prose:** "The digit 5 can be worth five pounds or five pence. Where it sits decides which."
- **Art:** `ast.course-art.place-value`.
- **Bertie:** `idle`. Chat is open with no answer key, as on an explore screen (AI-TUTOR.md 2.2); hints do not exist yet.

#### Screen 2: `fewest` (`problem`, the hook, difficulty 1)

- **Skills:** `skl.num.place-value`.
- **Prose:** "A cash machine pays out £100 notes, £10 notes and £1 coins. It always uses as few pieces as it can."
- **Canvas:** `chart`, a `place-value-chart` in money skin. Three columns headed £100, £10 and £1, left to right, start empty. A tray below holds unlimited pieces of each kind. Drag a piece into its column, or tap the piece and then the column; drag a piece out to remove it. Exchange is on demand: a column holding ten or more pieces shows a "Swap 10 for 1" chip that merges ten pieces into one piece in the next column left (300 ms). A live readout under the chart shows the total in pounds and the number of pieces. No digits are shown yet. The chart is the graded widget (`answer: chart`).
- **Question:** "Make exactly £305 using as few notes and coins as possible."
- **Check:** `predicate` `pv-fewest-pieces` with `{ total: 305 }`: correct when the chart's total is 305 and its piece count equals the minimum for 305. The minimum is three £100 notes, no £10 notes and five £1 coins: 8 pieces.
- **Diagnose:**

| Learner state | Misconception | Feedback line | Show-why |
|---|---|---|---|
| Total £305 with more than 8 pieces | `mc.num.no-exchange` | "That makes £305 with {{chart.pieces}} pieces. Ten £10 notes can be swapped for one £100 note." | Pulse `chart/col:tens`; play one swap |
| Total £35 (three £10 notes, five £1 coins) | `mc.num.drop-placeholder` | "That is £35. In 305 the 3 sits in the hundreds column, so it means three £100 notes." | Highlight `chart/col:hundreds` |
| Total £350 | `mc.num.drop-placeholder` | "That is £350: the five pieces went into the £10 column. In 305 the 0 says there are no £10 notes." | Highlight `chart/col:tens` |

- **Otherwise:** "Your total is £{{chart.total}}. Add or remove pieces until it reads £305."
- **Reason (verdict chip):** "Three £100 notes, no £10 notes and five £1 coins: 8 pieces."
- **Hints:** Nudge: "What is the biggest piece you can use, and how many of them fit into £305?" Point: "Three £100 notes make £300. What is left over?" (highlights `chart/col:hundreds`). Step: "Use three £100 notes. That leaves £5: no £10 notes and five £1 coins."
- **Why?** Yours: "You used three £100 notes, no £10 notes and five £1 coins." Shown: "The fewest pieces are three £100 notes, no £10 notes and five £1 coins." Then: "Those counts are the digits of 305. The 0 says there are no £10 notes, and it keeps the 3 in the hundreds column." `rep`: money.
- **Solution (Show solution):** the chart fills with three £100 notes and five £1 coins; text: "Biggest pieces first: three £100 notes leave £5, which needs no £10 notes and five £1 coins."
- **After a correct answer or a reveal:** the digits 3, 0 and 5 fade in under the columns. Concreteness starts to fade here.
- **Tutor:** focus: "The counts of each piece are the digits." Notes: "Learners who fill the £10 column with thirty notes have not met exchange; ask what ten £10 notes are worth." Reps: money; counting pieces. Avoid: "place value", "column value" (embargoed until screen 3).

#### Screen 3: `columns` (`problem`, naming the idea, difficulty 1)

- **Skills:** `skl.num.place-value`.
- **Prose:** "Each column is worth ten times the column to its right. A digit says how many of that column you have. This is place value: $305 = 3 \times 100 + 0 \times 10 + 5 \times 1$."
- **Canvas:** `chart`, a `place-value-chart` in blocks skin: big cubes (thousands), flats (hundreds), rods (tens) and small cubes (ones), with the digits of 4,725 under the blocks. Tapping a column header shows its worth ("one flat is 100"). Display only.
- **Input:** `n`, a `numeric-input`, integers.
- **Question:** "What is the 7 in 4,725 worth?"
- **Check:** `numeric`, exact. **Correct:** 700. **Accepted:** 700 and 700.0.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| 7 | `mc.num.face-value` | "That is the digit itself. Its worth depends on its column, and the 7 is in the hundreds column." | Highlight `chart/col:hundreds` |
| 70 | `mc.num.column-miscount` | "That would be 7 tens. Count the columns from the right: ones, tens, hundreds." | Number the columns from the right |
| 7,000 | `mc.num.column-miscount` | "That would be 7 thousands. The 4 is in the thousands; the 7 is one column to its right." | Same |

- **Otherwise:** "Find the 7's column, then multiply the 7 by what one block in that column is worth."
- **Reason:** "The 7 is in the hundreds column, so it is worth $7 \times 100 = 700$."
- **Hints:** Nudge: "Which column is the 7 in? Count from the right." Point: "This column holds the 7. What is one block here worth?" (highlights `chart/col:hundreds`). Step: "From the right: 5 ones, 2 tens, 7 hundreds. Multiply the 7 by the worth of one flat."
- **Why?** Yours: "You read the 7 as 7 hundreds." Shown: "The 7 is in the hundreds column." Then: "A digit's worth is the digit times its column's value." `rep`: blocks.
- **Solution:** "The 7 is the third digit from the right, the hundreds column: $7 \times 100 = 700$."
- **Tutor:** focus: "Worth equals digit times column value." Notes: "An answer of 7 is face value; ask what one flat is worth." Reps: blocks; money from screen 2. Avoid: powers of ten written as $10^2$ (taught in P3).

#### Screen 4: `pence` (`ladder`, difficulty 2)

- **Constraint:** "The columns carry on past the point."
- **Skills:** `skl.num.decimal-place-value`.
- **Prose:** "Split £1 into ten 10p coins, and 10p into ten 1p coins. The columns carry on past the decimal point: tenths of a pound, then hundredths."
- **Canvas:** `chart`, `from: fewest/chart`, with columns £10, £1, then the point, then 10p and 1p, "tenths" and "hundredths" under the last two headers. It shows £3.05: three £1 coins, no 10p coins, five 1p coins. Display only.
- **Input:** `n`, a `numeric-input` with a £ prefix, decimals allowed.
- **Question:** "In £3.05, what is the 5 worth, in pounds?"
- **Check:** `numeric`, exact. **Correct:** $\frac{1}{20}$, written 0.05. **Accepted:** 0.05, .05, 0.050, 5/100, 1/20.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| 0.5 | `mc.num.drop-placeholder` | "£0.50 is fifty pence. The 0 in the tenths column pushes the 5 one column further right." | Highlight `chart/col:tenths` |
| 5 | `mc.num.unit-slip` | "Five pence is right. In pounds it is less than £1, because 100 pennies make £1." | Show 100 pennies merging into £1 |
| 0.005 | `mc.num.column-miscount` | "That is five thousandths of a pound. Count the columns after the point: tenths, then hundredths." | Number the columns after the point |

- **Otherwise:** "Count how many pennies make a pound, then write five pennies as part of a pound."
- **Reason:** "The 5 is in the hundredths column: five pennies, or £0.05."
- **Hints:** Nudge: "How many pennies make £1?" Point: "The 5 sits in this column. What is one coin here worth in pounds?" (highlights `chart/col:hundredths`). Step: "One penny is $\frac{1}{100}$ of a pound. Write five of them as a decimal of a pound."
- **Why?** Yours: "You read the 5 as 5 hundredths of a pound." Shown: "The 5 is 5 hundredths of a pound." Then: "Each step to the right divides a piece's worth by 10: £1, then £0.10, then £0.01." `rep`: money.
- **Solution:** "One penny is $\frac{1}{100}$ of a pound, so five pennies are $\frac{5}{100} = £0.05$."
- **Tutor:** focus: "The ten-times pattern continues past the point." Notes: "An answer of 5 means the learner is thinking in pence; confirm that, then ask for pounds." Reps: coins; splitting a pound. Avoid: "decimal places" as a counting rule.

#### Screen 5: `times10` (`ladder`, the worked example, difficulty 2)

- **Constraint:** "Every piece becomes ten times bigger."
- **Skills:** `skl.num.shift-by-ten`.
- **Prose:** "Now multiply £3.05 by 10. Every coin becomes a coin worth ten times as much: each £1 becomes £10, each 1p becomes 10p."
- **Canvas:** `chart`, `from: pence/chart`, plus a "×10" operator (`chart/op:times-10`) that is locked until Check, so the learner predicts first. On a correct answer or a reveal it plays: every piece grows and slides one column left over 600 ms, while the point stays fixed.
- **Input:** `n`, a `numeric-input`, decimals allowed.
- **Question:** "What is $3.05 \times 10$?"
- **Check:** `numeric`, exact. **Correct:** $\frac{61}{2}$, written 30.5. **Accepted:** 30.5, 30.50, 61/2.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| 3.050 | `mc.num.add-a-zero` | "A zero on the end after the point changes nothing: 3.050 is still 3.05. Multiplying by 10 must make it bigger." | Play the ×10 animation |
| 30.05 | `mc.num.shift-whole-part-only` | "You moved the pounds but not the pence. Every coin grows, so the pence move left too." | Play the animation with `chart/col:hundredths` highlighted |
| 305 | `mc.num.shift-count` | "That is $\times 100$: each digit moved two columns. $\times 10$ moves each digit one column." | Play the animation once |
| 3.5 | `mc.num.drop-placeholder` | "That only removes the 0. Every digit has to move one column left." | Play the animation |

- **Otherwise:** "Grow each coin by ten times, one column at a time, then read the new amount."
- **Reason:** "Every digit moved one column left: 3 tens, 0 ones, 5 tenths."
- **Hints:** Nudge: "If every coin becomes ten times bigger, what does a 1p coin become?" Point: "Each 1p becomes 10p. Which column do these five coins move to?" (highlights `chart/col:hundredths`). Step: "Three £1 coins become three £10 notes. Five 1p coins become five 10p coins. Read the total."
- **Why?** Yours: "You moved every digit one column left." Shown: "Every digit moves one column left." Then: "Nothing was added: the same digits, each now worth ten times as much. 'Add a zero' only looks right for whole numbers." `rep`: the ×10 animation.
- **Solution:** the animation plays; text: "Three £1 coins become three £10 notes and five 1p coins become five 10p coins: £30.50, which is 30.5."
- **Worked example record:** naive: "Add a zero: 3.050." Decision: "Decide what moves. Every digit moves one column left; nothing is added on."
- **Tutor:** focus: "Multiplying by 10 is a shift of digits, not appending a zero." Notes: "Learners taught 'move the decimal point' get the right answer here; both pictures agree, but the point-moving picture fails on whole numbers, where the point is invisible." Reps: coins growing; the shift animation. Avoid: "move the decimal point".

#### Screen 6: `bigger` (`trap`, difficulty 2)

- **Trap:** `{ mc: mc.num.longer-is-larger, bait: a }`.
- **Skills:** `skl.num.compare-decimals`.
- **Prose:** "Two decimals. Most people get this wrong the first time."
- **Canvas:** `line`, a `number-line` from 0 to 1, hidden until Check. After Check it appears with both numbers marked and the stretch from 0.4 to 0.5 magnified (`line/span:0.4-0.5`).
- **Input:** `cards`, a `choice`, three cards: a "0.45"; b "0.5"; c "They are equal".
- **Question:** "Which is bigger?"
- **Check:** `choice`, `select: one`. **Correct:** b.
- **Diagnose (inline on the options):**

| Option | Misconception | Feedback line | Show-why |
|---|---|---|---|
| a 0.45 | `mc.num.longer-is-larger` | "That reads 45 and 5 as whole numbers. But 0.5 has 5 tenths and 0.45 has only 4." | Show `line`; zoom on `line/span:0.4-0.5` |
| c Equal | `mc.num.round-then-compare` | "0.45 rounds to 0.5, but rounding changes a number. 0.5 is 50 hundredths; 0.45 is 45." | Show `line` with both points |

- **Reason:** "0.5 has 5 tenths; 0.45 has only 4."
- **Hints:** Nudge: "How many tenths does each number have?" Point: "Compare these two digits first." (highlights the tenths digit on `cards/option:a` and `cards/option:b`). Step: "Write 0.5 as 0.50. Now compare 50 hundredths with 45 hundredths."
- **Why?** Shown: "0.5 is 5 tenths, which is 50 hundredths; 0.45 is 45 hundredths." Then: "Compare decimals column by column from the left, like words in a dictionary. Length does not matter." `rep`: number line.
- **Solution:** the number line appears with 0.45 just left of 0.5; text: "0.5 has 5 tenths and 0.45 has 4, so 0.5 is bigger by 0.05."
- **On the reveal:** Bertie plays `surprised` once. A wrong first try is expected on a trap; a revealed trap is recorded but does not enter the Redo queue (ASSESSMENT.md 2.2).
- **Tutor:** focus: "Comparison goes column by column from the left." Notes: "Many adults hold the longer-is-larger belief from reading decimals as whole numbers; it survives into price comparisons." Reps: number line; money (50p against 45p). Avoid: offering "pad with zeros" as a rule before the learner has seen why it works.

#### Screen 7: `order` (`ladder`, difficulty 2)

- **Constraint:** "Four numbers on one line."
- **Skills:** `skl.num.compare-decimals`.
- **Prose:** "Place each number on the line from 0 to 1. Drag the lens over a tenth to see its hundredths."
- **Canvas:** `line`, a `number-line` from 0 to 1 with ticks every 0.1 and a zoom lens (`line/lens:main`) that magnifies one tenth into ten hundredths; a second level magnifies one hundredth into thousandths. Four tokens in a tray: 0.5, 0.45, 0.405, 0.054. A token snaps when dropped within half a minor tick of the visible scale. Below the line, the tokens list themselves in the order they stand. The line is the graded widget (`answer: line`).
- **Question:** "Drag each number to its place on the line."
- **Check:** `point`, one per token, tolerance half a hundredth at the base scale and half a thousandth inside the lens; meeting all four puts them in the order $0.054 < 0.405 < 0.45 < 0.5$.
- **Diagnose:**

| Learner state | Misconception | Feedback line | Show-why |
|---|---|---|---|
| Order 0.5, 0.45, 0.054, 0.405 | `mc.num.longer-is-larger` | "You have ordered them like whole numbers: 5, 45, 54, 405. Compare tenths first." | Highlight each token's tenths digit |
| 0.054 placed between 0.5 and 0.6 | `mc.num.drop-placeholder` | "0.054 has 0 tenths, so it is less than 0.1. Drag the lens over the first tenth." | Pulse `line/span:0-0.1` |
| 0.405 right of 0.45 | `mc.num.longer-is-larger` | "0.405 and 0.45 both have 4 tenths. Then compare hundredths: 0 against 5." | Lens on `line/span:0.4-0.5` |

- **Otherwise:** "Some tokens are not at their values yet. Zoom in to place them precisely."
- **Reason:** "From smallest: 0.054, 0.405, 0.45, 0.5."
- **Hints:** Nudge: "Which number is less than one tenth?" Point: "This is the first tenth of the line, from 0 to 0.1." (highlights `line/span:0-0.1`). Step: "Tenths first: one token has 5, two have 4, one has 0. Hundredths break the tie between the two with 4."
- **Why?** Yours: "You placed each number by its tenths, then by its hundredths." Shown: "Each number sits by its tenths first, then its hundredths." Then: "Each comparison was settled by the first column where the numbers differ." `rep`: number line with lens.
- **Solution:** the tokens glide to their places; text: "Tenths first (0, 4, 4, 5), then hundredths to separate 0.405 from 0.45."
- **Tutor:** focus: "A position on the line is what the digits mean." Notes: "Learners who stall usually have not opened the lens; suggest it before any rule." Reps: number line; lens. Avoid: none.

#### Screen 8: `zeros` (`problem`, the edge case, difficulty 2)

- **Skills:** `skl.num.decimal-place-value`.
- **Prose:** "Some zeros change a number and some change nothing."
- **Canvas:** `chart`, a `place-value-chart` in plain skin, display only, showing 3.5. Tapping an option lays that number into the chart directly under 3.5, so the columns can be compared.
- **Input:** `cards`, a `choice` with `select: many`, five cards: a "3.50"; b "3.05"; c "03.5"; d "3.500"; e "35.0". The question hides the count.
- **Question:** "Which of these are equal to 3.5? Select all that apply."
- **Check:** `choice`, `select: many`. **Correct:** a, c, d.
- **Diagnose:**

| Learner state | Misconception | Feedback line | Show-why |
|---|---|---|---|
| b selected | `mc.num.drop-placeholder` | "3.05 is 3 ones and 5 hundredths. Its 0 holds the tenths column empty and pushes the 5 right." | Lay 3.05 under 3.5 |
| e selected | `mc.num.shift-count` | "35.0 is thirty-five: every digit sits one column further left than in 3.5." | Lay 35.0 under 3.5 |
| a or d not selected | `mc.num.trailing-zero-matters` | "A zero at the end, after the point, moves no digit: 3.50 is 3.5." | Lay 3.50 under 3.5 |
| c not selected | `slip: true` | "A zero before the first digit moves nothing either: 03.5 is 3.5." | Lay 03.5 under 3.5 |

- **Reason:** "3.50, 03.5 and 3.500 all have 3 ones and 5 tenths, like 3.5."
- **Hints:** Nudge: "Does each zero push another digit into a new column?" Point: "This zero sits between the point and the 5. Where does that leave the 5?" (highlights the 0 on `cards/option:b`). Step: "A zero changes a value only when it pushes other digits to new columns. Check each card against the chart."
- **Why?** Shown: "Only 3.05 and 35.0 put a digit in a different column from 3.5." Then: "A zero between digits holds a column open; a zero at the end after the point changes nothing. In measurement, 2.50 m does claim more precision than 2.5 m; lesson 37 returns to that." `rep`: stacked charts.
- **Solution:** each card lays itself under 3.5 in turn; text: "Three cards keep 3 ones and 5 tenths. 3.05 moves the 5 right; 35.0 moves both digits left."
- **Tutor:** focus: "A zero matters only when it moves another digit." Notes: "Value and precision are different questions; a trailing zero is ordinary in prices." Reps: stacked charts. Avoid: "significant figures" (P4).

#### Screen 9: `rule` (`generalise`, difficulty 2)

- **Skills:** `skl.num.shift-by-ten`.
- **Rule (prose):** "You made every piece ten times bigger, and every digit moved one column left. That is all multiplying by 10 does. Dividing by 10 moves every digit one column right. The point stays still; the digits move."
- **Tex:** $\times 10$: one column left. $\times 100$: two columns left. $\div 10$: one column right. $\div 100$: two columns right.
- **Canvas:** `chart`, a `place-value-chart`, plain skin, showing 4.7, with ÷10 and ÷100 operators (`chart/op:divide-10`, `chart/op:divide-100`) that play after Check.
- **Input:** `n`, a `numeric-input`.
- **Question:** "What is $4.7 \div 100$?"
- **Check:** `numeric`, exact. **Correct:** $\frac{47}{1000}$, written 0.047. **Accepted:** 0.047, .047, 47/1000.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| 0.47 | `mc.num.shift-count` | "That is $\div 10$. Dividing by 100 moves every digit two columns right." | Play ÷10, then ÷10 again |
| 470 | `mc.num.wrong-direction` | "That multiplies by 100. Dividing makes pieces smaller, so the digits move right." | Play ÷100 |
| 0.0047 | `mc.num.shift-count` | "That moved the digits three columns. Dividing by 100 moves them two." | Play ÷100 |

- **Otherwise:** "Dividing by 100 makes every piece a hundred times smaller: each digit moves two columns right. Fill any empty column with 0."
- **Reason:** "4 ones become 4 hundredths and 7 tenths become 7 thousandths: 0.047."
- **Hints:** Nudge: "Which way do digits move when you divide, and how many columns for 100?" Point: "The 4 is in the ones column. Which column is two to its right?" (highlights `chart/col:ones`). Step: "The 4 moves to the hundredths and the 7 to the thousandths. The tenths column is left empty, so it needs a 0."
- **Why?** Yours: "You moved both digits two columns right." Shown: "Both digits move two columns right." Then: "The 0 after the point is a placeholder you have to write, because the tenths column is empty." `rep`: the ÷100 animation.
- **Solution:** ÷100 plays; text: "Two columns right: 4 hundredths and 7 thousandths, with a placeholder 0 in the tenths: 0.047."
- **Tutor:** focus: "The rule describes the shift the learner has watched three times." Notes: "A missing placeholder is the usual slip here; point at the empty tenths column rather than restating the rule." Reps: shift animation. Avoid: "count the decimal places".

#### Screen 10: `why-shift` (`derive`, difficulty 3)

- **Skills:** `skl.num.shift-by-ten`, `skl.num.place-value`.
- **Prose:** "Why must every digit move? Write 3.05 by its columns, then multiply by 10."
- **Input:** `deriv`, a `derivation-steps` in complete-the-line mode: three lines, each with its justification on the right (below the line on mobile), three boxes in line 2 (`deriv/box:l2-a`, `deriv/box:l2-b`, `deriv/box:l2-c`):

$$
\begin{aligned}
3.05 &= 3 \times 1 + 0 \times \tfrac{1}{10} + 5 \times \tfrac{1}{100} && \text{place value}\\
10 \times 3.05 &= 3 \times \square + 0 \times \square + 5 \times \square && \text{every part times 10}\\
&= 30.5 && \text{3 tens, 0 ones, 5 tenths}
\end{aligned}
$$

- **Question:** "Fill in the three boxes."
- **Check:** `parts` of three `numeric` checks, exact. **Correct:** 10, 1 and $\frac{1}{10}$. **Accepted:** 10; 1; 1/10 or 0.1. Green parts lock and amber parts reopen (design research 5.4).
- **Leap** (maths-teaching, "motivate the leap"): naive: "Multiply only the first part by 10." Fails: "That gives $30 + 0.05 = 30.05$, the wrong answer from screen 5: the pence did not grow." Points to: "The whole number is ten times bigger, so every part of it must be. Lesson 10 names this the distributive law."
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| 10, $\frac{1}{10}$, $\frac{1}{100}$ | `mc.num.shift-whole-part-only` | "You multiplied only the first part. Every part of 3.05 must become ten times bigger." | Highlight `deriv/line:l1`'s three column values |
| 100, 10, 1 | `mc.num.shift-count` | "Each of those is multiplied by 100. Multiply each column value by 10 once." | Same |

- **Otherwise:** "Multiply each column value by 10: $1 \times 10$, $\frac{1}{10} \times 10$ and $\frac{1}{100} \times 10$."
- **Reason:** "Each column value becomes the next one up: 1 becomes 10, $\frac{1}{10}$ becomes 1, $\frac{1}{100}$ becomes $\frac{1}{10}$."
- **Hints:** Nudge: "What is each column value in line 1 when multiplied by 10?" Point: the three column values in line 1 (highlights `deriv/line:l1`). Step: "Work out $1 \times 10$, then $\frac{1}{10} \times 10$, then $\frac{1}{100} \times 10$."
- **Why?** Yours: "You multiplied every column value by 10." Shown: "Every column value is multiplied by 10." Then: "Each became the value of the column to its left. So each digit now sits one column further left: the shift is forced, not a trick." `rep`: the derivation, line by line.
- **Solution:** the boxes fill; text: "$1 \times 10 = 10$, $\frac{1}{10} \times 10 = 1$ and $\frac{1}{100} \times 10 = \frac{1}{10}$, so $10 \times 3.05 = 30 + 0 + \frac{5}{10} = 30.5$."
- **Verify:** `chain` over lines `l1` and `l3`: line 1 evaluates to $\frac{61}{20}$, line 3 to $\frac{61}{2}$, and line 2 with the boxes filled equals ten times line 1.
- **Tutor** (numbers in words, see the rules above): focus: "This is the proof behind the rule." Notes: "Learners who fill the boxes with the original column values have multiplied nothing; ask what happens to one penny when it becomes ten times bigger." Reps: the derivation; coins. Avoid: "distributive law" as a known term (embargoed until lesson 10).

#### Screen 11: `pips` (`problem`, `context: quant`, the transfer, difficulty 2)

- **Skills:** `skl.num.decimal-place-value`.
- **Prose:** "Currency prices are quoted to four decimal places. Traders count moves in pips: one pip is one unit in the fourth decimal place, 0.0001."
- **Canvas:** `chart`, a `place-value-chart`, plain skin, columns ones, tenths, hundredths, thousandths and ten-thousandths; the last column is also headed "pip". It shows 1.0842 above 1.0857.
- **Input:** `n`, a `numeric-input`, integers.
- **Question:** "EUR/USD moves from 1.0842 to 1.0857. How many pips did it move?"
- **Check:** `numeric`, exact. **Correct:** 15. **Accepted:** 15.
- **Diagnose:**

| Answer | Misconception | Feedback line | Show-why |
|---|---|---|---|
| 0.0015 | `mc.num.unit-slip` | "0.0015 is the price change. Each pip is 0.0001, so count how many of those it holds." | Highlight `chart/col:ten-thousandths` |
| 1.5 | `mc.num.column-miscount` | "That counts in thousandths. A pip is a ten-thousandth." | Number the columns after the point |
| 150 | `mc.num.column-miscount` | "That counts in a column beyond the pip. A pip is the fourth decimal place." | Same |

- **Otherwise:** "Subtract the two prices, then count the result in ten-thousandths."
- **Reason:** "$1.0857 - 1.0842 = 0.0015$, which is 15 ten-thousandths: 15 pips."
- **Hints:** Nudge: "What is the change in the price itself?" Point: "Only these two columns differ." (highlights `chart/col:thousandths` and `chart/col:ten-thousandths`). Step: "Subtract: $1.0857 - 1.0842 = 0.0015$. Now count it in units of 0.0001."
- **Why?** Shown: "The move is 0.0015, a whole number of units of 0.0001." Then: "Counting in pips lets traders talk in whole numbers. It is place value with one column renamed. For yen pairs the pip is the second decimal place." `rep`: chart with the pip column.
- **Solution:** the differing digits light up; text: "$0.0015 = 15 \times 0.0001$: 15 pips."
- **Tutor:** focus: "A pip is place value with one column renamed." Notes: "Some platforms quote a fifth decimal place, a tenth of a pip; mention it only if the learner asks." Reps: chart; a currency quote. Avoid: "basis point" (taught in lesson 24).

#### Screen 12: `summary`

- **Ideas** (exactly three):
  1. A digit's worth is the digit times its column's value; each column is worth ten times the one to its right.
  2. Multiplying by 10 moves every digit one column left and dividing moves them right; the point stays still.
  3. Compare decimals column by column from the left; length does not matter.
- **Card** (`crd.num.place-value`, `derivedIn: why-shift`): title "Place value and the shift"; tex: "$305 = 3 \times 100 + 0 \times 10 + 5 \times 1$ and $3.05 = 3 \times 1 + 0 \times \tfrac{1}{10} + 5 \times \tfrac{1}{100}$. Multiplying by 10, 100 or 1,000 moves every digit 1, 2 or 3 columns left; dividing moves them right."
- **Trap:** "Do not 'add a zero' to multiply by 10: $2.5 \times 10 = 25$, not 2.50."
- **Bertie:** `celebrate` once the lesson completes, then the recap and practice offers (AI-TUTOR.md 2.2, end of lesson row).

### 7.3 Lesson quiz (4 items, 1 mark each, no hints, one attempt, Why? after each)

| # | Id | Item | Type, difficulty | Correct and accepted | Diagnosed wrong answers | Why? |
|---|---|---|---|---|---|---|
| 1 | `itm.numwork.digit-worth-q1` | "What is the 6 in 52.068 worth?" | N, 2 | 0.06; also 6/100, .06 | 6 (`mc.num.face-value`); 0.6 (`mc.num.drop-placeholder`: "The 0 in the tenths column pushes the 6 to the hundredths."); 0.006 (`mc.num.column-miscount`) | "The 6 is in the hundredths column, so it is worth $6 \times \frac{1}{100} = 0.06$." |
| 2 | `itm.numwork.digit-worth-q2` | "What is $0.307 \times 1000$?" | N, 2 | 307 | 0.307000 (`mc.num.add-a-zero`); 30.7 (`mc.num.shift-count`); 3,070 (`mc.num.shift-count`) | "$\times 1000$ moves every digit three columns left: 3 hundreds, 0 tens, 7 ones." |
| 3 | `itm.numwork.digit-worth-q3` | "Put in order, smallest first: 2.1, 2.09, 2.101, 2.0999." | O, 3 (`ordering`, exact order) | 2.09, 2.0999, 2.1, 2.101 | 2.1, 2.09, 2.101, 2.0999 (`mc.num.longer-is-larger`: the decimal parts read as 1, 9, 101, 999) | "All have 2 ones. 2.09 and 2.0999 have 0 tenths, so they come first, and 2.0999 has more thousandths. 2.1 and 2.101 differ first in the thousandths." |
| 4 | `itm.numwork.digit-worth-q4` | "A share price moves from £101.25 to £101.4. Which is true?" Options: a "It rose by 15p"; b "It fell, because 4 is less than 25"; c "It rose by 0.15p"; d "It rose by £1.50" | C, 3 | a | b (`mc.num.longer-is-larger`); c (`mc.num.unit-slip`: "0.15 is in pounds; in pence it is 15p."); d (`mc.num.shift-count`) | "$101.40 - 101.25 = 0.15$ pounds, which is 15p. Compare tenths first: 4 tenths is more than 2." |

**Marks and mastery.** Each item scores 1 mark (decision 15). 3 of 4 on the first completion marks the lesson Mastered (ASSESSMENT.md decision 26); wrong items join the Redo queue at 7 and 30 days. Every item's `use` is `[quiz, practice, review]`, so a missed item can return as practice.

### 7.4 Verification for this lesson

| Claim | Check |
|---|---|
| `fewest`: 8 is the fewest pieces for £305, at $(3, 0, 5)$ | Exhaustive search over counts of £100, £10 and £1 pieces totalling 305 [run]; the predicate's Python twin agrees on fixture states |
| `columns`, `pence`, quiz 1: digit worths | `Fraction` evaluation of digit times column value |
| `times10`, `rule`, quiz 2: shifts | `Fraction`: $3.05 \times 10 = \frac{61}{2}$, $4.7 \div 100 = \frac{47}{1000}$, $0.307 \times 1000 = 307$ [run]; every diagnosed answer differs from the correct one and from each other |
| `bigger`, `order`, `zeros`, quiz 3: comparisons | Exact comparison of `Fraction`s [run]; the diagnosed whole-number order is recomputed by reading the decimal digits as integers |
| `why-shift`: the derivation | Derivation chain: lines 1 and 3 evaluate to $\frac{61}{20}$ and $\frac{61}{2}$, and line 2 with the boxes filled equals 10 times line 1 |
| `pips`, quiz 4: market moves | `Fraction`: $\frac{1.0857 - 1.0842}{0.0001} = 15$ and $101.40 - 101.25 = 0.15$ [run] |
| Tutor fields | The leak lint grades every number in each screen's tutor fields with that screen's check; none is accepted (screen 10 spells its numbers in words) |
| References | Every element reference resolves against its widget's `targets(config)`: 31 references to 19 elements of `chart`, `line`, `cards` and `deriv` [counted] |
| Copy | Copy lints (sentence length, banned words, British spelling, no em-dashes); every `$...$` arithmetic claim evaluated; KaTeX renders in strict mode |

[run] marks a claim recomputed by this draft's scratch script.

---

## 8. Open items and requests to the other papers

**Owner decisions.**

| # | Item | Effect |
|---|---|---|
| O1 | Confirm GCSE geometry and statistics inside 0.3 (`stage0-precalc-computing.md` decision 2) | Nothing in this file changes either way; section 4.3's 52 marks from 0.1 and 0.2 stand. If they move into 0.2 instead, 0.2 gains about 40 h and a fifth course, which the schema's ceiling of 4 courses per topic forbids, so a new topic would be needed |
| O2 | Banned-word exemption for glossary terms (`CONTENT-FORMAT.md` 13, item 11) | Not needed here: no 0.1 or 0.2 term contains a banned word |

**Requests.**

| # | To | Request | Why |
|---|---|---|---|
| R1 | `ASSESSMENT.md` 8.7 | A practice set authored per level (`ItemSet` kind `practice`: the fluency sets and the lab sets) counts as earned when every slot has been attempted once | CI already counts set estimates (`CONTENT-FORMAT.md` 3.8), but 8.7's list of earned units names only homework. Without R1 the 31.75 h of fluency sets and 9.5 h of lab drills in 0.1 and 0.2 are estimated but never earned, and the forecast overstates what is left |
| R2 | `CONTENT-FORMAT.md` 3.8, 6.7 | Project milestone hours (`Project.milestones[].hours`) join the topic sum CI checks | `prj.alg.root-finder` carries 10 of 0.2's hours; without it the 0.2 estimates fall to 159.5 h (88.6%), outside the 10% band |
| R3 | `widgets-stage0.md` 13 | Move `counting-slots` to wave W1 and `scatter-fit`, `dot-plot-stats` (mean and deviation marks) and `complex-plane` to W2 | Depth-first content reaches lessons 13, 46, 75, 85 to 87 and 105 before any 0.3 lesson |
| R4 | `widgets-stage0.md` 5.1 | `place-value-chart` exposes `targets()` ids `col:<place>`, `op:times-10`, `op:times-100`, `op:divide-10`, `op:divide-100`, `tray:<place>`, `chip:swap-<place>`, and a `pv-fewest-pieces` predicate with a Python twin | The sample lesson references them (section 7) |
| R5 | `widgets-stage0.md` 3.2 | `number-line` exposes `span:<from>-<to>`, `token:<value>` and `lens:main` | Same |
| R6 | `stage0-precalc-computing.md` 4.4 and 0.5 | Cite 0.2 lesson 41 for the linear $n$th term (`gcse` question 3) and 0.2 lessons 43, 109 and 110 for question 21; close open item 1 with section 2.3's boundary table | Their table cites "0.3 G1" and "0.2 (A-O13)" because this file's lesson numbers were not final |

**Unverified details.**

| # | Item | Status |
|---|---|---|
| U1 | Khan Academy unit titles and Corbettmaths topic names in section 5 | [check]: both sites were blocked by this environment's network proxy; Corbettmaths' "Iteration", "Gradient of a Curve" and "Area under a graph" were confirmed by search |
| U2 | OpenStax section numbers, AoPS and Edexcel chapter numbers, MCS chapter and section numbers, Blitzstein and Hwang section 4.6, OpenIntro chapter 4's z-score subsection, Art of Insight chapter 4's title, Gelfand and Shen section titles | [check] against the books before `checked: true`. OpenIntro 8.1 and Street-Fighting chapters 1 and 4 are now [searched] |
| U3 | Licence of CS50x | [check]; Street-Fighting (CC BY-NC-SA 3.0 US), MCS (CC BY-SA 3.0), OpenStax Calculus (CC BY-NC-SA 4.0) and OpenIntro (CC BY-SA 3.0) are now [searched]. None is adapted here |
| U4 | Citations for the decimal misconceptions | Resolved: both confirmed with pages [searched] |
| U5 | DfE GCSE subject content codes in section 2.3 | N11, N16, A25, R12, R15 and R16 [searched]; the other codes are recalled [check] against the published document (gov.uk and the boards' sites were blocked by this environment's proxy) |
| U6 | The floating-point claims (0.1 + 0.2, the variance shortcut returning $-1024$ and the two-pass result $0.0199999857$, the 25% error of the textbook quadratic formula on $x^2 + 10^8 x + 1 = 0$) | Measured on CPython 3.11 here; Pyodide uses the same IEEE 754 doubles, and CI records both (section 6.1) |

---

## 9. Verification log

Second pass, 6 October 2026: every answer in sections 2, 3 and 7 recomputed with Python 3.11, `fractions` and SymPy 1.14 (all 54 homework examples, every hook, trap and edge value with a number in it, the sample lesson's checks and diagnoses, the 31 element references); hours, exam marks, format and difficulty mixes and the choice-item shares re-summed; 15 web searches on citations.

| # | Where | Change | Evidence |
|---|---|---|---|
| 1 | 3.2, Q4 code drill; U6 | **False claim fixed.** The two-pass variance of $10^9 + 0.1$, $10^9 + 0.2$, $10^9 + 0.3$ returns $0.0199999857$, not "0.02 to 8 significant figures": it is $0.02$ to 6 figures and exact for the stored doubles, whose inputs already carry rounding error. The test now uses `rel_tol=1e-5` | CPython run; exact `Fraction` sum over the stored doubles gives $0.01999998569489$ |
| 2 | 2.1, lesson 38 | **Trap rewritten.** It reasoned about a divisor rounded down, but 0.098 is rounded up; the trap is now "rounding up gives an overestimate", reversed for a divisor | $48.7 \times 0.52 \div 0.098 = 258.4$; estimate 250 |
| 3 | 2.1, lesson 1 quiz column | "N, N, S, C" corrected to "N, N, O, C" to match the sample quiz (item 3 is an ordering item); choice shares unchanged | Section 7.3 |
| 4 | 7.1, `est` | 13 minutes raised to 15, the unit decision 1 and section 1.1 budget on | Section 1.1 hours |
| 5 | 1.1 | Zetamac and Optiver's 80 in 8 separated: they are different tests | [searched] |
| 6 | 2.3 | GCSE N11 (fractions in ratio problems) mapped to lesson 27; R1 to R8 widened to lessons 17, 24, 28; A24's triangular, square, cube and Fibonacci-type sequences, taught nowhere, added to homework L1 (`gen.alg.special-sequences`) and lesson 83's hook; "Powers" cover row includes lesson 34 | DfE codes [searched in part] |
| 7 | 5, resources and 7.1 | Confirmed and completed: Resnick et al. 1989 (pages 8 to 27); Steinle and Stacey 1998 (MERGA 21, full reference); Frederick 2005 (pages, DOI and article URL); licences of MCS, OpenIntro, OpenStax Calculus and Street-Fighting; OpenIntro 8.1 title; CS50x 2026 week numbering (Week 0 binary, Week 1 floating point) | [searched] |
| 8 | 5 | Kept as [check]: Khan URLs and unit titles, MCS chapter 9 (LibreTexts numbers it 8), Blitzstein and Hwang 4.6, Art of Insight chapter 4, Gelfand and Shen sections, AoPS and Edexcel chapters, CS50x licence, the remaining GCSE codes | Searches inconclusive or sites blocked |

Checked and correct, unchanged: hours (60.0 and 180.0; estimates 56.75 h and 169.5 h; reading maps 15.0 h and 46.75 h by level); exam totals (60 and 80 marks, every format, difficulty, level and course split); course choice shares (26% to 35%, under 40%); lesson and level counts; the `s0.gcse` strand totals (12, 16, 24, matching the sibling); every curriculum cover term for 0.1 and 0.2 is taught. No invented citation was found, so nothing was deleted.
