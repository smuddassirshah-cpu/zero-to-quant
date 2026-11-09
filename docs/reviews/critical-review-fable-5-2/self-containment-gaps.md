# Self-containment gaps, topic by topic

Companion to `../critical-review-fable-5-2.md`. Question: what must be added for the app to teach each topic with no outside book, course or site. Fable 5.2, 9 Nov 2026. Read-only; nothing in `app/` changed.

## Basis and limits

- Read: every course's level names, lesson titles and skills (all 1,214 titles, `scripts/topic-stats.py --titles`), per-topic counts (`scripts/topic-stats.py`), and a term search of lesson files for each suspected hole. Lessons read in full are still the 12 in `sampling.md`.
- So "missing" below means: absent from titles and skills, and the search found no lesson or almost none. An author must open the nearest lessons before writing, in case an idea is taught under another name.
- The outside syllabus is the one named on each topic card, judged from my knowledge of it, not re-read.

## A correction to the review

The review said the foundations lack practice volume and quoted authored minutes (22 hours for algebra and precalculus). That understates the app. Counted as graded items, the volume is respectable: 843 in Algebra, 928 in Precalculus, 1,270 in Calculus, 1,796 in Probability, 50 to 80 per skill everywhere. A beginner will take two or three times the authored minutes.

The real shortfall is narrower and more fixable:

1. **Independent practice per technique is about 8 items.** A lesson gives about 10 hinted screens, then 3 to 5 quiz items and its share of a review and a homework: 7 to 9 unhinted items per lesson in every topic. One lesson is one technique (the product rule, partial fractions, completing the square). A textbook gives 30 to 60 exercises for each. Procedural skills need that repetition; conceptual ones do not.
2. **No reference text.** Explanations stop at three sentences. Nothing states a definition, a theorem and two full worked examples for looking up later.
3. **Few chained problems.** Multi-step items are 3% of Stage 0 items (91 of 3,457) and 3% in Calculus (34 of 1,270).
4. **Review of mastered material is optional and reuses seen items.**
5. **Long work is self-marked.**
6. **Some syllabus holes**, listed per topic below. Fewer than I expected: the course maps follow the named books closely.

## Cross-cutting additions

| Id | Addition | What it is | Size |
| --- | --- | --- | --- |
| G | Generated fluency sets | Extend the `arith` generator idea to parametric families (expand, factorise, solve, index and log laws, exact trig values, differentiate, integrate, row-reduce, a binomial or normal probability). A "Fluency" set per procedural lesson: 20 fresh items, typed answers, pass at 90%, repeatable. Also feeds review with unseen items | Engine: one pass for the generator framework and expression answers. Content: about 90 families (list by topic below) |
| R | Reference page per level | Definitions, results, two worked examples in full, common errors, reachable from the lesson, the Notebook and search. Seeded from the existing lesson summaries | 279 pages; one engine item for the page and its search |
| M | Chained problems | Three to five multi-part problems per level with each intermediate answer graded (the `parts` shape already exists) | About 150 maths, probability and statistics levels, 500 to 700 items |
| C | Scheduled cumulative review | A weekly mixed set drawn from every met level, generated or held-out items first, shown on Today as due work, not opt-in | Engine: one item on `select.js` and Today. Content: comes from G and M |
| A | Auto-graded parts in long work | Each performance task and long-form item gets its checkable results (final expression, numbers) as graded parts; the rubric keeps only the reasoning rows | 136 performance tasks, 275 long-form items; retrofit by batch |
| P | Real projects in the app | Project sessions (the `project` kind exists, 0 are written): one long build per project course on the data in `content/data`, hidden tests on the outputs, a results note marked on graded figures | 5 to 7 projects (2.3 and 3.1), each a workshop series |
| D | Drill volume | Independent problems with hidden tests, by pattern | Topics 1.8, 1.9, 2.4 and 3.5; about 200 in all, of which 120 are already planned |

## Per topic

Columns: lessons and graded items now; unhinted share of items that make the learner produce an answer (number, expression, code, table) and not choose one; what the named resource gives that the app does not; what to add.

| Topic | Now | Produce share | The outside resource still supplies | Add |
| --- | --- | --- | --- | --- |
| 0.1 Number | 27 lessons, 480 items | 65% | Drill volume on the four operations with fractions, decimals, negatives. Missing content: factors, multiples and primes as a taught idea; surds; units and basic measures (area, perimeter, circumference: 1 lesson mentions them); averages and reading charts | G (10 families), R, M. One new level "Factors, measures and averages" (about 5 lessons) |
| 0.2 Algebra | 48, 843 | 51% | Most of the repetition. Missing: algebraic fractions (0 lessons), surds and rationalising (0), polynomial division and the factor theorem (0 below Stage 3), circles in coordinates (0), a line meeting a curve | G (15 families: collect, expand, factorise, solve linear, rearrange, simultaneous, quadratics three ways). One new level "Algebraic fractions and polynomials" (5 to 6 lessons). R, M |
| 0.3 Precalculus | 52, 928 | 59% | Repetition on logs and trig. Thin: inverse trig functions, reciprocal trig, sketching rational functions, proof by identities | G (12 families). Two or three lessons in `trig` and `functions`. R, M |
| 0.4 Computer basics | 24, 430 | 37% | Typing practice (keybr) and a real shell: the terminal course is read and traced, not typed | An in-browser shell emulator for a small file tree (engine, already deferred as item 150), then convert the trace screens. More free-writing code items: 67 code items in 24 lessons is low for first programming |
| 0.5 Mental arithmetic | 12, 220 plus the generator | 82% | Nothing essential; Zetamac is duplicated by the warm-up | Nothing. This topic is self-contained |
| 0.6 Proof | 15, 277 | 32% | Writing proofs and having them read. Missing: relations and equivalence classes, strong induction, cardinality (met later in `analysis`) | A. Proof items as ordered or fill-the-gap derivations with graded steps; 2 lessons. R |
| 0.7 Getting hired | 15, 279 | 38% | Current dates and firm facts; a reader for the CV | Cannot be self-contained. Keep the `asOf` dates; add recording for stories (review change 7) |
| 1.1 Python | 42, 762, 7 drills | 44% | CS50P's problem sets: whole programs written from a blank file. Missing: debugging as a skill, virtual environments and packages, regular expressions | D: 30 small-program drills. One level "Debugging and environments" (4 lessons). R |
| 1.2 Tools | 36, 628 | 41% | A real git repository and shell. SQL and pytest run for real in Pyodide and are in better shape | The shell emulator from 0.4 with git on top, or state plainly that git needs the learner's machine. R |
| 1.3 Calculus | 69, 1,270 | 69% | Exercise sets for every differentiation and integration technique (integration by parts appears in 1 lesson file). Missing: hyperbolic functions, arc length, curve sketching beyond one lesson | G (15 families: each rule, chain, implicit, substitution, parts, partial fractions, definite integrals, Taylor coefficients). M (optimisation and related-rates problems). R |
| 1.4 Linear algebra | 53, 986 | 58% | Strang's problem sets, mainly hand computation and short proofs | G (8 families: products, elimination, inverse, determinant, eigenvalues of 2 by 2 and 3 by 3, projection, least squares). R. Coverage is complete for the purpose |
| 1.5 Probability | 99, 1,796, 1 drill | 68% | Blitzstein's 600 exercises, especially story and symmetry problems. Coverage is complete | M first (this is where chained problems matter most), then 150 held-out problems for cumulative review. G (6 families: counting, binomial, normal, Bayes tables, chains). R |
| 1.6 Statistics | 35, 660 | 62% | Theory the app skips: sufficiency, Fisher information and the Cramér-Rao bound, method of moments, likelihood-ratio tests (0 lessons each); chi-squared tests are mentioned, not taught | One level "Theory of estimation and tests" (5 to 6 lessons) in `estimation` or `testing`; one lesson on chi-squared tests. G (5 families), M, R |
| 1.7 Finance basics | 55, 1,018 | 64% | Little. Not seen in titles: swaps, the yield curve, foreign exchange forwards | 3 to 4 lessons in `markets`. R |
| 1.8 Data structures and algorithms | 49, 880, 0 drills | 49% | The practice: this topic has no drill of its own. 135 code items are mostly inside guided lessons | D: 60 drills by pattern (arrays, hashing, pointers, stacks, trees, heaps, graphs, DP), easy to medium, before `coding-int`. Stdin variant. R |
| 1.9 C++ | 35, 644, 0 in topic (5 C++ drills in 3.5) | 37% | learncpp's breadth and a real toolchain. Thin: inheritance (1 lesson), iterators, strings and streams; CMake is read, not run | D: 25 C++ drills. 3 to 4 lessons. State on the course page what needs a local compiler. R |
| 1.10 Analysis, linear maps | 43, 850 | 47% | Proof writing with a reader | A. Not on any quant route; lowest priority |
| 1.11 Complex, vector calculus, ODEs | 43, 823 | 61% | Problem sets | G (6 families: complex arithmetic, separable and linear ODEs, characteristic equation). R. Low priority except `odes` |
| 2.1 Machine learning | 50, 951 | 44% | ISLP's labs on real data sets. Missing: support vector machines (0), clustering (0), neural networks (3 mentions), splines and additive models | One level "Other learners" (5 lessons: SVM, clustering, a small neural network, splines). P: one lab per level on a real table. R |
| 2.2 Time series | 36, 722 | 55% | Missing: seasonality, state-space models and the Kalman filter (0), vector autoregression | 3 to 4 lessons. R |
| 2.3 Projects | 48, 912 | 55% | The projects. 400 stored hours are 12 authored hours; the "project" is taught in twelve-minute lessons and built, if at all, outside the app. `capstones.json` holds placeholder reviews | P: three real in-app projects (backtester, signal study, option pricer set) with tested outputs. This is the largest single hole in Stage 2 |
| 2.4 Contests | 16, 311, 0 drills | 45% | Codeforces itself: hundreds of timed problems with a judge | D: 30 contest-style drills with stdin and time limits; a timed set of 4. Or keep it as the one honestly external topic |
| 2.5 Numerics, convex | 34, 618 | 59% | Trefethen's linear algebra core is thin here: QR, SVD and conditioning live in 1.4, iterative solvers are absent | 2 to 3 lessons. R |
| 2.6 Statistical modelling | 18, 317 | 57% | Worked data analyses | P: one analysis lab. R |
| 3.1 Research papers | 29, 501 | 54% | The papers and the data. The replication is described in lessons, not carried out | P: each replication as a tested project on bundled data |
| 3.2 Stochastic calculus | 46, 861 | 69% | Shreve's exercises; hours stored as 0 | M, R, real hours. A mock for the derivatives route (review change 10) |
| 3.3 Interview preparation | 96, 1,754, bank 200 | 75% | A second and third source of unseen problems (the green book has about 200) | Bank part 2 (planned), fresh mock versions (review change 6), open-answer items (change 8) |
| 3.4 Pure mathematics | 30, 564 | 41% | Proof writing | A. Lowest priority |
| 3.5 Interviews by role | 57, 1,050, 27 drills | 64% | LeetCode's volume | D: the planned packs, developer first |

## Order of work, by value

1. **G, the generator framework and the Stage 0 and calculus families.** It fixes repetition, feeds cumulative review with unseen items, and costs no per-item authoring or second read. Highest value for a beginner.
2. **C, cumulative review on Today.** One engine item once G exists.
3. **M for topics 1.5, 1.3, 0.2, 0.3.** Chained problems are what every exam and interview actually sets.
4. **D for 1.8, then 3.5, 1.1, 1.9.** Without it the developer route is not self-contained in any sense.
5. **R, starting with Stage 0 and 1.** Mostly assembly from summaries plus worked examples.
6. **Syllabus holes:** 0.2 algebraic fractions and polynomials, 0.1 factors and measures, 1.6 theory, 2.1 other learners. About 30 lessons.
7. **P, the projects.** Largest effort per unit; needed only for researcher and strats.
8. **A, auto-graded parts.** Retrofit alongside any batch that touches those files.

What stays outside whatever is added: a human listener for spoken answers and proofs, a real shell and compiler unless emulated, and current recruiting facts.
