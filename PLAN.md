# PLAN

Goal: a single-user, Brilliant-style interactive teaching app (vanilla JS, static, `app/`) that takes a learner from zero to quant-interview ready across Stages 0 to 3 of `docs/curriculum.md`. Every lesson is JSON content played by the engine, validated by `app/tools/validate.mjs` and played end to end by `app/tools/playthrough.mjs`. Done means: every course map level written, every topic and stage exam written, every topic second-read and fixed, the engine backlog inbox integrated, `validate.mjs` at 0 errors and `playthrough.mjs --all` green, and `docs/PLAN.md` section 13 satisfied.

Design documents live in `docs/` (`PLAN.md` there is the product design, not this checklist). Briefs for every unwritten level are in `docs/briefs/`. Conventions are in `CLAUDE.md`.

## Tasks (one per session; tick when committed)

### 0. Triage
- [x] Triage work left in flight on 27 Oct: arma L3 and opt-dash L4 lessons green with reports; garch l5, l9, coint l1, contests l1 kept (`docs/reports/triage-27oct.md`); nothing removed. Pass 7 left no status block; its edits sit in WIP commits; full playthrough 663 of ~1,050 ok, 0 failures, before a container restart stopped it.
- [x] Triage 2 (27 Oct): coint L3, contests L2, L3, L4 green with reports (`docs/reports/coint-3.md`, `contests-2.md` to `contests-4.md`); nothing removed.
- [x] Triage 3 (27 Oct): exams topic-2.1 to topic-2.4 written, green and reported (`docs/reports/exam-2.1.md` to `exam-2.4.md`).
- [x] Full playthrough green with `--local-cdn` (27 Oct): all 739 lessons and 354 sets in the first run; all 19 exams and every route in split re-runs (`--exams`, `--routes-only`); topic-1.3 no longer closes the browser when exams run alone.

### 1. Stage 2 content (brief: `docs/briefs/<course>.md`, section `## Level n`)
- [x] garch L2
- [x] garch L3
- [x] coint L1
- [x] coint L2
- [x] coint L3 (triage 2)
- [x] opt-dash L4
- [x] contests L1
- [x] contests L2 (triage 2)
- [x] contests L3 (triage 2)
- [x] contests L4 (triage 2)

### 2. Stage 1 gap levels (briefs: `docs/briefs/gap-<course>.md`; plan in `docs/briefs/gaps-plan.md`)
- [x] limits L5
- [x] integrals L4
- [x] multivar L5 (brief's 10% target under a 50% cap was infeasible, max 9.5%; transfer uses long-only at 10% and a 45% cap at 9%)
- [x] eigen L4
- [x] random-vars L5
- [x] limits-thm L4
- [x] markov L4
- [x] Extend exams topic-1.3, topic-1.4, topic-1.5 with items for the new levels (each now 30 items, the validator cap; reports `docs/reports/exam-1.3-gap.md`, `exam-1.4-gap.md`, `exam-1.5-gap.md`)

### 2a. Interview readiness (user priority, 29 Oct; runs before everything else)
Goal: the app is a complete, self-contained resource for passing quant internship online assessments and superdays (Two Sigma, JP Morgan, trading firms, bank strats). Plan: `docs/briefs/interview-plan.md` (phases 0 to 4; user decisions at its end: UK first, trader and researcher tracks first, no audio). Pure maths levels in 2b wait until this section is done.
- [x] Interview gap analysis and plan (`docs/briefs/interview-gaps.md`, `interview-plan.md`; 27 new levels, 12 mocks, a 400-item bank, 120 drills; engine bullets E1 to E19 in the inbox, E10 and E20 dropped)
- [x] Course maps and curriculum entries (stage 0 515 h, stage 3 550 h; full path 3,695 h): new courses `recruiting` (topic 0.7), `brainteasers`, `game-theory` (3.3), `coding-int`, `research-int`, `systems` (topic 3.5); appended levels puzzles L5, mm-games L4, mental-pressure L4, trees L4, ito L4, cpp L5; validate 0 errors
- [x] Engine pass A (items 450 to 454; `docs/reports/engine-interview-a.md`; sample `exams/mock-sample.json`): E1 net scoring, E2 forward-only papers, E4 generated arithmetic items, E5 mock exam kind, E6 timed sets (number from 450 in ENGINE-BACKLOG; document in AUTHORING.md)
- [x] Briefs: recruiting, brainteasers; revise puzzles, mm-games, mental-pressure, ito briefs per plan section (a) (plus new sections puzzles L5, mm-games L4, mental-pressure L4, ito L4)

Order (user decisions, 2 Nov; supersedes the phase order below, whose lines stay as the checklist).
Rules: finish one section at a time. A section is a topic: every level (lessons, review, homework), its topic exam, a second read and fix pass, and a green playthrough of the topic. Within a topic, finish one course before the next. Write a mock as soon as its content is complete. Commit each level when green (usage caps); a section closes with a commit that includes its exam.

Part G, gaps first: complete courses already started and write the exams their topics allow, before any course with no lessons is begun.
1. Prep tags: engine pass, then mapping (started this session).
2. Exam topic-0.6 (lessons complete).
3. recruiting L3; exam topic-0.7; extend stage-0 to cover topics 0.6 and 0.7 if it does not.
4. mental-pressure L3, L4; mock-oa-arith.
5. puzzles L3 to L5; mock-oa-sig, mock-oa-trader.
6. mm-games L2 to L4 (engine pass D first if L4 needs E12).
7. ito L2 to L4.
8. trees L4, extend exam topic-1.7; cpp L5, extend exam topic-1.9.
9. momentum-rep L2, L3.
10. analysis L5, linear-maps L4 (Pure maths, reversing the Pure-waits rule for started courses); exam topic-1.10.
11. Second reads and fix passes for finished topics with none (0.1 to 0.7, 1.1, 1.2, 1.8, 1.10, 2.1 to 2.4), interview-critical first: 0.5, 0.7, 1.8, 2.1.

Part N, new courses, topic by topic, after Part G:
1. Topic 3.3: brainteasers, game-theory (brief first); exam topic-3.3; mock-superday-trader; second reads.
2. Topic 3.5: briefs; research-int, coding-int, systems (engine passes B and C when needed); researcher, developer and strats mocks; exam topic-3.5.
3. Topic 3.2: measure-prob, pdes; exam topic-3.2.
4. Topic 3.1: pairs-rep; exam topic-3.1.
5. Then 2b and the rest (1.11, 2.5, 2.6, 3.4), then stage exams 1 to 3.

Phase 0, fast track
- [x] puzzles L1 (`docs/reports/puzzles-1.md`; 6 lessons, review-1, homework-1; 6 inbox bullets)
- [x] mental-pressure L1 (`docs/reports/mental-pressure-1.md`; 4 lessons, review-1, homework-1; 5 inbox bullets)
- [x] mental-pressure L2 (`docs/reports/mental-pressure-2.md`; 4 lessons, review-2, homework-2; 5 inbox bullets)
- [ ] mental-pressure L3
- [ ] mental-pressure L4: Assessment batteries
- [x] puzzles L2 (`docs/reports/puzzles-2.md`; 6 lessons, review-2, homework-2; 8 inbox bullets)
- [x] recruiting L1: The landscape (`docs/reports/recruiting-1.md`; 5 lessons, review-1, homework-1 with a dated target list; 5 inbox bullets)
- [x] recruiting L2: The application (`docs/reports/recruiting-2.md`; 5 lessons, review-2, homework-2; 5 inbox bullets)
- [ ] Exams: mock-oa-arith, mock-oa-trader, mock-oa-sig
- [ ] Prep tags, engine (ENGINE-BACKLOG 455; brief `docs/briefs/prep-tags.md`): `content/prep.json` schema, validator, one chip per lesson, a "Prepare for" page (user request, 2 Nov)
- [ ] Prep tags, mapping: general, stage-by-track and ten firm paths in `content/prep.json`

Phase 1, trader core
- [ ] puzzles L3
- [ ] puzzles L4
- [ ] puzzles L5: Puzzles firms keep asking
- [ ] brainteasers L1: Invariants and counting arguments
- [ ] brainteasers L2: Strategy and logic
- [ ] brainteasers L3: Quick reasoning
- [x] mm-games L1 (`docs/reports/mm-games-1.md`; 4 lessons, review-1, homework-1; 6 inbox bullets)
- [ ] mm-games L2
- [ ] mm-games L3
- [ ] mm-games L4: Trading games firms run
- [ ] recruiting L3: Interviews and after
- [ ] Engine pass B: E7 question bank with item spacing, E9 per-item timing
- [ ] Bank part 1 (200 items: probability, brainteasers, mental, market making, behavioural), in four sessions
- [ ] Exam: mock-superday-trader
- [ ] Second readers and fix passes: puzzles, mental-pressure

Phase 2, researcher core
- [ ] Briefs: research-int, coding-int, game-theory, systems, trees L4, cpp L5 (puzzles L5, mm-games L4, mental-pressure L4, ito L4 are in their briefs)
- [ ] research-int L1: Statistics and linear algebra questions
- [ ] research-int L2: Machine learning questions
- [ ] research-int L3: The open case
- [ ] research-int L4: Data tasks and take-homes
- [ ] coding-int L1: Patterns still to learn
- [ ] coding-int L2: Strings and simulation
- [ ] coding-int L3: Design in code
- [ ] coding-int L4: Under the clock
- [ ] trees L4: Options at interview
- [ ] Engine pass C: E3 exam item banks, E8 drill library (C++, timed), E11 follow-up parts, E14 data files
- [ ] Drill packs 1 to 4 (60 drills)
- [ ] Exams: mock-oa-code, mock-superday-research, mock-oa-quant-data
- [ ] Second readers and fix passes for interview-critical topics: fix pass 1.9, reader and fix 1.8, then 2.1

Phase 3, trader and researcher depth
- [ ] game-theory L1: Games in a table
- [ ] game-theory L2: Sequential games and auctions
- [ ] game-theory L3: Poker and decisions
- [x] ito L1 (`docs/reports/ito-1.md`; 4 lessons, review-1, homework-1; 7 inbox bullets)
- [ ] ito L2
- [ ] ito L3
- [ ] Engine pass D: E12 trading-game widget
- [ ] Bank part 2 (200 items)
- [ ] Exams: topic-3.3, topic-3.2 (ito part)

Phase 4, developer and strats depth
- [ ] ito L4: Stochastic calculus at interview
- [ ] cpp L5: C++ questions at interview
- [ ] systems L1 to L4 (one line per level when started)
- [ ] Engine: E13 concurrency canvas; [Could] items E15 to E19
- [ ] Drill packs 5 to 8 (60 drills)
- [ ] Exams: mock-oa-code-hard, mock-oa-strats, mock-superday-developer, mock-superday-strats, mock-video, topic-3.5

### 2b. Maths breadth pass (user request, 27 Oct; runs after 2a, before the rest of task 3)
Fills seven gaps against a traditional maths degree, now written into `docs/curriculum.md`: proof (0.6), analysis and proof-based linear algebra (1.10), complex numbers, vector calculus and ODEs (1.11), numerical methods and optimisation (2.5), statistical modelling (2.6), measure theory and PDEs (added to 3.2), pure mathematics (3.4, optional), plus a 1.5 gap level (Poisson process, martingales, optional stopping). Suggested courses: `proof`; `analysis`, `linear-maps`; `complex`, `vector-calc`, `odes`; `numerics`, `convex`; `stat-models`; `measure-prob`, `pdes`; `algebra`, `topology`; a new markov level.
- [x] Breadth plan: `docs/briefs/breadth-plan.md` (49 levels, 218 lessons in 13 new courses plus markov L5; validator accepts `strand` but ignores it) (pattern `docs/briefs/gaps-plan.md`): per course the levels, lesson ids, titles, objectives, prerequisites and the existing lessons each builds on; write the `course.json` maps and add topics 0.6, 1.10, 1.11, 2.5, 2.6, 3.4 (and the 3.2 courses) to `app/content/curriculum.json`; the markov gap level appended to `markov/course.json`; every new `course.json` carries `strand` (`"quant"` or `"pure"`, per the tags in `docs/curriculum.md`; vector calculus is `pure`, complex numbers and ODEs `quant`) and `strandNote` (the roles, e.g. "Desk quant"); validate at 0 errors with the new lessons shown as unwritten; replace the level placeholder below with one line per level, each marked [Quant] or [Pure maths]
- [x] Engine: (report `docs/reports/engine-breadth.md`; items 424 to 428; stage hours and Paths view not yet filtered, item 428) the Learn screen shows the new topics with targets (`app/js/screens/learn.js`), exams list them, nothing throws on an empty course; validator accepts and checks `strand`; a "Pure maths" or "Quant" badge (with `strandNote`) on course cards, the lesson start screen, topic chips and exam chips, distinct in both themes; untagged courses show no badge (core path); a "Quant path only" setting hides pure courses and drops them from stage-exam gating; document in AUTHORING.md
- [x] Briefs for 0.6, 1.10, 1.11 courses and the markov gap level (`docs/briefs/proof.md`, `analysis.md`, `linear-maps.md`, `complex.md`, `vector-calc.md`, `odes.md`, `gap-markov-2.md`; 7 briefs, 23 levels, 107 lessons)
- [x] Engine: breadth visuals and complex grading (report `docs/reports/engine-breadth-2.md`; items 429 to 437 done, follow-ups 438 to 448; new canvases `complex-map` and `space`) (user request, 27 Oct; inbox section "Raised later (breadth briefs ...)", numbered from 429): complex values graded by real and imaginary parts in `expression` and in code `isclose` (Python and C++); vector answers in one `expression`; `order` distractor lines; `plane` vector-field and slope-field layers and trajectories traced from a dragged start; a complex-mapping canvas; `vectors` matrix state readable by `derive` and applied to every vector; `walk` overlays, slider-bound barriers and a mean-reverting mode; a rotatable 3D canvas (item 241). If the 3D canvas overruns, split it into its own item
- [x] Brief revision (28 Oct; remaining limits cite items 438 to 448): replace every engine fallback in the seven breadth briefs (`proof`, `analysis`, `linear-maps`, `complex`, `vector-calc`, `odes`, `gap-markov-2.md`) with the new features, so no level ships a static or reduced visual
- [x] Briefs for 2.5, 2.6, 3.2 additions and 3.4 courses (`numerics`, `convex`, `stat-models`, `measure-prob`, `pdes`, `algebra`, `topology`; 26 levels, 111 lessons; 15 inbox bullets)
- [x] proof L1: Statements and logic [Pure maths] (`docs/reports/proof-1.md`; 5 inbox bullets)
- [x] proof L2: Sets and functions [Pure maths] (`docs/reports/proof-2.md`; 4 inbox bullets, one a `place` grading bug)
- [x] proof L3: Proof methods [Pure maths] (`docs/reports/proof-3.md`; 4 inbox bullets; proof course complete)
- [x] markov L5: Martingales and stopping [Quant] (`docs/reports/markov-5.md`; 5 inbox bullets; topic-1.5 exam at cap, not extended)
- [x] analysis L1: The real numbers [Pure maths] (`docs/reports/analysis-1.md`, written afterwards; 163 numbers rechecked, one text fix in l1)
- [x] analysis L2: Sequences [Pure maths] (`docs/reports/analysis-2.md`, written afterwards; 170 numbers rechecked, two text fixes in l7)
- [x] analysis L3: Series [Pure maths] (`docs/reports/analysis-3.md`; 4 lessons, review-3 9 items, homework-3 9 items; 5 inbox bullets)
- [x] analysis L4: Continuity and the derivative [Pure maths] (`docs/reports/analysis-4.md`; 5 lessons, review-4 8 items, homework-4 9 items; 3 inbox bullets; two brief numbers corrected)
- [ ] analysis L5: Integration and metric spaces [Pure maths]
- [x] linear-maps L1: Vector spaces [Pure maths] (`docs/reports/linear-maps-1.md`; 5 inbox bullets)
- [x] linear-maps L2: Linear maps [Pure maths] (`docs/reports/linear-maps-2.md`; 3 inbox bullets; l9 starter passes 4 of 6 hidden tests)
- [x] linear-maps L3: Duality and inner products [Pure maths] (`docs/reports/linear-maps-3.md`; 5 lessons, review-3, homework-3; 3 inbox bullets)
- [ ] linear-maps L4: Operators [Pure maths]
- [ ] complex L1: The complex plane [Quant]
- [ ] complex L2: Complex functions [Quant]
- [ ] complex L3: Integrals and Fourier [Quant]
- [ ] vector-calc L1: Fields and line integrals [Pure maths]
- [ ] vector-calc L2: Green’s theorem [Pure maths]
- [ ] vector-calc L3: Surfaces and space [Pure maths]
- [ ] odes L1: First-order equations [Quant]
- [ ] odes L2: Second-order equations [Quant]
- [ ] odes L3: Systems and stability [Quant]
- [ ] odes L4: Transforms and numerical solution [Quant]
- [ ] numerics L1: Errors [Quant]
- [ ] numerics L2: Equations and curves [Quant]
- [ ] numerics L3: Integrals and time steps [Quant]
- [ ] numerics L4: One option, three ways [Quant]
- [ ] convex L1: Convexity [Quant]
- [ ] convex L2: Linear programmes [Quant]
- [ ] convex L3: Duality and KKT [Quant]
- [ ] convex L4: Algorithms [Quant]
- [ ] stat-models L1: Generalised linear models [Quant]
- [ ] stat-models L2: Experiments [Quant]
- [ ] stat-models L3: Without the assumptions [Quant]
- [ ] stat-models L4: Bayesian models [Quant]
- [ ] measure-prob L1: Measures [Quant]
- [ ] measure-prob L2: Integration [Quant]
- [ ] measure-prob L3: Information and martingales [Quant]
- [ ] measure-prob L4: Changing measure [Quant]
- [ ] pdes L1: The heat equation [Quant]
- [ ] pdes L2: Separation and Fourier series [Quant]
- [ ] pdes L3: Pricing equations [Quant]
- [ ] algebra L1: Groups [Pure maths]
- [ ] algebra L2: Inside a group [Pure maths]
- [ ] algebra L3: Maps between groups [Pure maths]
- [ ] algebra L4: Rings and fields [Pure maths]
- [ ] topology L1: Metric spaces revisited [Pure maths]
- [ ] topology L2: Topological spaces [Pure maths]
- [ ] topology L3: Compact and complete [Pure maths]

### 3. Stage 3 content (briefs in `docs/briefs/`; puzzles, mm-games, mental-pressure and ito lines are duplicated in 2a: tick both)
- [x] momentum-rep L1 (look-ahead bug gives 17.06% a month, not the brief's 15%; `docs/reports/momentum-rep-1.md`)
- [ ] momentum-rep L2
- [ ] momentum-rep L3
- [ ] pairs-rep L1
- [ ] pairs-rep L2
- [ ] pairs-rep L3
- [x] ito L1 (`docs/reports/ito-1.md`; 4 lessons, review-1, homework-1; 7 inbox bullets)
- [ ] ito L2
- [ ] ito L3
- [x] puzzles L1 (`docs/reports/puzzles-1.md`; 6 lessons, review-1, homework-1; 6 inbox bullets)
- [x] puzzles L2 (`docs/reports/puzzles-2.md`; 6 lessons, review-2, homework-2; 8 inbox bullets)
- [ ] puzzles L3
- [ ] puzzles L4
- [x] mm-games L1 (`docs/reports/mm-games-1.md`; 4 lessons, review-1, homework-1; 6 inbox bullets)
- [ ] mm-games L2
- [ ] mm-games L3
- [x] mental-pressure L1 (`docs/reports/mental-pressure-1.md`; 4 lessons, review-1, homework-1; 5 inbox bullets)
- [x] mental-pressure L2 (`docs/reports/mental-pressure-2.md`; 4 lessons, review-2, homework-2; 5 inbox bullets)
- [ ] mental-pressure L3

### 4. Exams (pattern: `app/content/exams/topic-1.7.json`; brief pattern in `docs/reports/exam-1.8.md`)
- [x] topic-0.1 to topic-0.5 (Stage 0 topic exams; never written, the Learn screen shows them as unwritten; pattern topic-1.1.json, items from the Stage 0 courses of each topic)
- [x] topic-1.9 (cpp, cpp-pricing; the 1.9 review proposes coverage)
- [x] topic-2.1 (stat-learning, validation, ensembles, fin-ml)
- [x] topic-2.2 (arma, garch, coint)
- [x] topic-2.3 (backtest, alpha, opt-dash)
- [x] topic-2.4 (contests)
- [ ] topic-3.1 (momentum-rep, pairs-rep)
- [ ] topic-3.2 (ito)
- [ ] topic-3.3 (puzzles, mm-games, mental-pressure)
- [ ] Breadth exams: topic-0.6, topic-1.10, topic-1.11, topic-2.5, topic-2.6, topic-3.4; topic-3.2 covers ito, measure-prob and pdes; topic-1.5 is at the 30-item cap, so the markov gap level packs into multi-part items
- [ ] stage-1, stage-2, stage-3 exams (pattern: `app/content/exams/stage-0.json`)

### 5. Second readers and fix passes (reader pattern: `docs/reviews/review-1.5.md`; fix pattern: its `## Fix pass` section)
- [ ] Second reader 1.8 (was in flight; no file yet) then fix pass 1.8
- [ ] Fix pass 1.9 (second reader 1.9 is complete in `docs/reviews/review-1.9.md`)
- [ ] Second reader 2.1 then fix pass
- [ ] Second reader 2.2 then fix pass
- [ ] Second reader 2.3 and 2.4 then fix pass
- [ ] Second reader 3.1 to 3.3 then fix pass
- [ ] Second readers and fix passes for the breadth topics 0.6, 1.10, 1.11, 2.5, 2.6, 3.2 additions, 3.4
- [ ] Fix the seven homework items with both prose and a hidden longform prompt (list in `docs/ENGINE-BACKLOG.md`, pass 6 content note)

### 6. Engine
- [ ] Engine pass 7: backlog items 340 to 422 plus `docs/BACKLOG-INBOX.md` (was in flight; status block "Seventh pass" may be partial). Number inbox bullets from 424, clear the inbox, document in AUTHORING.md and canvas READMEs
- [ ] Engine pass 8: whatever the inbox holds after Stage 2 and 3 content lands
- [ ] Full `playthrough.mjs --all --local-cdn <pkgs>` green; `validate.mjs` 0 errors; System gallery renders in both themes

### 7. Finalise
- [ ] Getting started: `app/README.md` and `README.md` describe clone, `app/run.sh`, first load (jsDelivr for Pyodide, MathLive, Compute Engine, YoWASP clang), the self-host fallback in `app/vendor/`
- [ ] Check `docs/PLAN.md` section 13 (definition of done) item by item; record gaps in KNOWN_ISSUES.md
- [ ] Final report to the user; create `DONE`

## Completed
- [x] Stage 0 content (163 lessons, 76 sets, stage exam)
- [x] Stage 1 original content: all 426 lessons and 204 sets of topics 1.1 to 1.9
- [x] Exams topic-1.1 to topic-1.8
- [x] Second readers and fix passes for topics 1.3, 1.4, 1.5, 1.6, 1.7
- [x] Gap-pass plan: seven new levels added to course maps, briefs written
- [x] Stage 2: stat-learning, validation, ensembles, fin-ml, backtest complete; arma L1, alpha L1, L2, opt-dash L1, garch L1
- [x] Briefs for every remaining course and level
- [x] Engine passes 1 to 6; C++ runtime (clang in WebAssembly); Python via Pyodide with scikit-learn and statsmodels
