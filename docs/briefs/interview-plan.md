# Interview plan: closing the gaps to quant internship offers

Planner's design for PLAN.md tasks 40 to 47, from `docs/briefs/interview-gaps.md`. The goal is an app that is enough on its own to pass the online assessments and final rounds reported at Two Sigma, JP Morgan, Jane Street, Citadel and Citadel Securities, Optiver, SIG, IMC, HRT, Goldman Sachs and Morgan Stanley strats. Each item is judged against the reported questions in the gap analysis and against the topic 3.3 exit line in `docs/curriculum.md` (80% of Zhou's probability chapter cold; Zetamac 50 or more; ten mock interviews).

Priorities: **[Must]** is needed to pass at least one firm type's process; **[Should]** raises the pass rate or serves one role track; **[Could]** is polish. Effort is in content levels: one level is one authoring session of 4 to 6 lessons plus `review-n` and `homework-n`.

## Shape of the plan

No existing lesson id, level, exam, review, homework or progress record changes. Six new courses and six appended levels; twelve mock exams; an interview question bank and drill packs; twenty engine bullets.

| Item | Where | Levels | Lessons | Priority |
| --- | --- | --- | --- | --- |
| `recruiting`, Getting the Internship (new) | new topic 0.7 | 3 | 15 | [Must] |
| `brainteasers`, Logic and Brainteasers (new) | 3.3 | 3 | 16 | [Must] |
| `coding-int`, Coding Interviews (new) | new topic 3.5 | 4 | 19 | [Must] |
| `research-int`, Research Interviews (new) | 3.5 | 4 | 20 | [Must] (researcher track) |
| `game-theory`, Games, Auctions and Poker (new) | 3.3 | 3 | 15 | [Should] |
| `systems`, Systems for Developer Interviews (new) | 3.5 | 4 | 18 | [Should] ([Must] for developer track) |
| `puzzles` level 5, Puzzles firms keep asking | 3.3 | 1 | 6 | [Must] |
| `mm-games` level 4, Trading games firms run | 3.3 | 1 | 5 | [Must] |
| `mental-pressure` level 4, Assessment batteries | 3.3 | 1 | 5 | [Must] |
| `trees` level 4, Options at interview | 1.7 | 1 | 6 | [Must] (trader and strats) |
| `ito` level 4, Stochastic calculus at interview | 3.2 | 1 | 5 | [Should] ([Must] for strats and JP Morgan QR) |
| `cpp` level 5, C++ questions at interview | 1.9 | 1 | 5 | [Should] ([Must] for developer track) |
| **Total new** | | **27** | **135** | |
| Mock OAs and mock superdays | `content/exams/mock-*.json` | 12 exams, about 10 sessions | | 6 [Must], 5 [Should], 1 [Could] |
| Interview question bank | `content/bank/` | about 400 items, 8 sessions | | 200 [Must], 200 [Should] |
| Coding drill packs | `content/drills/` | 120 drills, 8 sessions | | 60 [Must], 60 [Should] |

Already planned and unwritten, and in scope here: `puzzles` L1 to L4, `mm-games` L1 to L3, `mental-pressure` L1 to L3, `ito` L1 to L3 (13 levels). Section (a) lists what to add to their briefs.

## Decisions

- **Topics.** `recruiting` goes in a new topic **0.7, Getting hired** (track `speed`, about 15 hours), so the calendar is visible from the first week: postings open about a year before the internship. The role-specific courses go in a new topic **3.5, Interviews by role** (track `speed`, about 150 hours): `coding-int`, `research-int`, `systems`. `brainteasers` and `game-theory` join 3.3 after the existing three. Splitting keeps `topic-3.3.json` to five courses' skills; one topic for all eight would need an exam covering about 33 skills. This is the main session's call (see Questions).
- **Skills.** New courses declare new skills with unused prefixes: `rk` (recruiting), `bz` (brainteasers), `gm` (game-theory), `ci` (coding-int), `rq` (research-int), `sy` (systems). Appended levels use only their course's existing skills, so `topic-1.7.json`, `topic-1.9.json` and the planned 3.2 and 3.3 exams need no new skill rows for them (the rule in `gaps-plan.md`).
- **Appended levels, not new courses, for trees, cpp and ito.** Options rules of thumb need Black-Scholes, which arrives in `trees` l10, so they go in `trees` level 4 (not `options`, which comes before `trees` in topic 1.7). C++ interview depth extends `cpp` because it uses the same runtime and skills. Systems topics with no C++ runtime support (threads, kernel, network) go in the new `systems` course.
- **Firm facts.** Lessons name firms and their reported formats in plain text, with an "as reported in" date and a source line, never logos or firm styling. Formats change every cycle, so every firm fact sits in `recruiting` l4 and the mock exam descriptions, not scattered through maths lessons. Other courses say "trading firms" or "banks".
- **Mocks are their own exam kind.** Mock OAs and superdays are `exams/mock-<id>.json`, not topic exams: they mix topics and skills on purpose and are sat many times. They need engine support (bullets E1 to E5) before they are fully faithful; until then they ship as fixed-item versions in the stage-exam format.
- **Speed is the main new demand.** Most committed content is at the reported difficulty; the gap is speed, volume and the live form. So the plan spends its effort on banks, timed formats and aloud practice more than on new mathematics.
- **Citations.** "Builds on" lines cite lessons by course and id from the `course.json` maps (checked against the maps on 29 October 2026). Lessons marked (unwritten) exist in a map but have no file yet.

## (a) Additions to the existing unwritten briefs

### `docs/briefs/puzzles.md`

- **All levels [Must].** Add a pace to each lesson's drill prose (about 3 minutes a puzzle, as interviews allow) and one "follow-up" screen per lesson: the same puzzle extended the way interviewers extend it (n-sided dice, three players, a cost per roll). Tag every drill and homework item with its family name in a `tags` field, so the bank (E7) can draw from them later.
- **L1 (being written now: do not disturb the agent).** Its homework already has a spoken-answer `longform`. Add nothing to L1; the follow-up and tag rules start at L2, and L5 l30 retrofits L1's families.
- **L2.** Put the drunkard's walk "reach A before B" (reported at Citadel) in l10's drill, citing `markov` l8-which-end. Put the frog that jumps one or two steps (reported at Jane Street) in l12's transfer as a recursion, citing `graphs-dp` l13-climbing-stairs.
- **L3.** l17-buffon: name it as reported in bank final rounds (GS) in the hook, without naming the firm in the screen.
- **L4.** l19-who-wins: add "would you rather go first or second" games (reported at Jane Street) as worked puzzle 3. l24-mixed-set: raise it to 20 unlabelled puzzles in three OA styles (short calculation, multi-stage, strategic), so it also seeds the bank and `mock-oa-sig`.
- **New level 5** (section c).

### `docs/briefs/mm-games.md`

- **All levels [Must].** Every game screen keeps a running ledger (trades, position, P&L at the fair value) in a `table` canvas, and at least one drill per lesson asks for the P&L. Interviewers ask for it after every trade.
- **L1 l4-fermi.** Add a follow-up screen where the interviewer trades on the Fermi number, joining l4 to l5, as IMC and Optiver report.
- **L3 l12-thinking-aloud.** Add a spoken `longform` (a full game narrated, 10-point rubric), which becomes a `speak` item once E10 exists.
- **L3 l13-full-game.** Write it so that it can move to the trading-game widget (E12) without changing its numbers: a seeded script of counterparty actions, one per turn.
- **New level 4** (section c).

### `docs/briefs/mental-pressure.md`

- **L3 l9-eighty-in-eight [Must], a correction.** The brief teaches "skip and return". Reported 80-in-8 sittings are four-option multiple choice, +1 right and −1 wrong, with no skipping. Teach both formats: skip and return when the test allows it, and the guessing rule of level 4 l13 when it does not. State the reported pass line as about 50 to 60 net, marked as reported.
- **L3 l12-mock-test.** Make the 80 items four-option multiple choice with near-miss distractors (a slipped digit, a misplaced point, the reverse operation), so the same script can generate `mock-oa-arith` versions.
- **L1 l1-towards-fifty.** Name the two targets plainly: Zetamac 50 (the 3.3 exit) and 80 in 8 at about 55 net (reported), and link the Today warm-up.
- **New level 4** (section c).

### `docs/briefs/ito.md`

- **L2 l8-fair-games [Should].** Add $W_t^3$ to the classification drill (drift $3W_t$, so not a martingale; $W_t^3 - 3tW_t$ is one), as reported at JP Morgan QR. Level 4 l13 builds on it.
- **L3 l9-bs-pde.** End with a timed spoken derivation (`longform`, 5 minutes, rubric), the form strats interviews use.
- **Strand note.** Keep `ito` optional (topic 3.2 has hours 0), but its course card should say "Needed for strats and desk quant interviews (banks), rarely for trading firms".
- **New level 4** (section c).

## (b) New courses

### `recruiting` (topic 0.7): Getting the Internship [Must]

- **Track:** `speed`. **Hours:** 15. **Levels:** 3, 15 lessons. No maths prerequisites; sit L1 in Stage 0 and L2 to L3 four months before applying.
- **Skills:** `rk-landscape` Roles, firms and the calendar; `rk-apply` Applications and CVs; `rk-assess` Assessments and video interviews; `rk-behave` Behavioural answers; `rk-offer` Offers and setbacks.
- **Widgets:** `choice`, `order` (calendar steps), `tap-regions` (a CV with weak lines to tap), `table`, and `longform` for every written artefact (the CV, the stories, the "why us" answer), self-marked against a rubric. Homework produces real documents the learner keeps.
- **Builds on:** nothing for L1. L2 cites the projects `backtest` l16-results-note, `alpha` l16-research-note, `opt-dash` l16-assembling and `momentum-rep` l15-replication-note (unwritten).

#### recruiting level 1: The landscape

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-three-roles` | Trader, researcher, developer | Tell the three quant roles apart by their daily work and by what their interviews test. | `rk-landscape` |
| `l2-kinds-of-firm` | Banks, funds and trading firms | Compare bank strats and research desks, hedge funds and trading firms as places to intern. | `rk-landscape` |
| `l3-the-calendar` | The recruiting calendar | Place each step of a summer internship cycle on a calendar, from postings in July to offers in winter. | `rk-landscape` |
| `l4-firm-by-firm` | What each firm's process looks like | Read a firm's reported process and list the assessments and rounds to prepare for. | `rk-landscape`, `rk-assess` |
| `l5-a-target-list` | Building a target list | Choose firms and roles that fit your track, region and timeline, including first-year and diversity programmes. | `rk-landscape`, `rk-apply` |

l4 carries the firm table from `interview-gaps.md` section 1, dated, with its sources, as tap-to-open rows; it is the one place firm formats live.

#### recruiting level 2: The application

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l6-one-page-cv` | A one-page CV | Write a one-page CV whose every line shows a skill an interviewer can test. | `rk-apply` |
| `l7-projects-that-count` | Projects that count | Turn a finished project into a CV entry and a two-minute account with numbers. | `rk-apply`, `rk-behave` |
| `l8-why-this-firm` | Why this firm, why this role | Answer "why trading" and "why us" with specific, true reasons. | `rk-apply`, `rk-behave` |
| `l9-sitting-an-assessment` | Sitting an online assessment | Prepare for proctoring, retake rules, timing and the environment before an assessment starts. | `rk-assess` |
| `l10-recorded-video` | Recorded video interviews | Answer a recorded question in two minutes after thirty seconds of preparation. | `rk-assess`, `rk-behave` |

#### recruiting level 3: Interviews and after

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l11-stories-that-answer` | Stories that answer behavioural questions | Build six stories in situation, task, action and result form that cover the common behavioural questions. | `rk-behave` |
| `l12-reasoning-aloud` | Reasoning aloud | Narrate a solution so an interviewer can follow, check and steer it. | `rk-behave`, `rk-assess` |
| `l13-the-final-round` | The final round | Plan a final-round day: pacing, recovering from a bad round and the questions to ask. | `rk-assess`, `rk-behave` |
| `l14-offers-and-deadlines` | Offers, deadlines and return offers | Handle an offer with a deadline, compare offers, and turn an internship into a return offer. | `rk-offer` |
| `l15-after-a-rejection` | After a rejection | Use feedback, reapplication waits and off-cycle roles after a rejection. | `rk-offer` |

### `brainteasers` (topic 3.3): Logic and Brainteasers [Must]

- **Track:** `speed`. **Hours:** 40. **Levels:** 3, 16 lessons. **Prerequisites:** proof L3 to L4 (contradiction, induction), counting-chance L2, graphs-dp L3.
- **Skills:** `bz-invariant` Invariants and parity; `bz-search` Weighing and search; `bz-strategy` Strategy and common knowledge; `bz-quick` Quick reasoning.
- **Lesson shape:** as `puzzles`: method after use, three worked teasers of rising difficulty, a trap built on the blurted answer, a drill of three to five, a follow-up screen, a pace in the prose.
- **Builds on:** contests l8-invariants, l5-modulo; proof l12-contradiction, l13-induction; counting-chance l5-in-stages; graphs-dp l12-remembering; mental l8-squaring; puzzles l5-hats and l19-who-wins (unwritten).

#### brainteasers level 1: Invariants and counting arguments

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-what-stays-the-same` | What stays the same | Solve a puzzle by finding a quantity that no move can change. | `bz-invariant` |
| `l2-colouring-boards` | Colouring arguments | Prove a tiling or a route impossible by colouring the board. | `bz-invariant` |
| `l3-pigeonhole` | The pigeonhole principle | Force a coincidence by counting boxes and objects. | `bz-invariant` |
| `l4-weighing-coins` | Weighing coins | Find a fake coin in the fewest weighings by splitting into three groups. | `bz-search` |
| `l5-ropes-and-jugs` | Ropes, timers and jugs | Measure a time or a volume with tools built to measure something else. | `bz-search` |

#### brainteasers level 2: Strategy and logic

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l6-back-from-the-end` | Working back from the end | Solve pirate and voting puzzles by backward induction from the smallest case. | `bz-strategy` |
| `l7-hat-strategies` | Hats and shared strategies | Design a team strategy for hat-colour puzzles using parity. | `bz-strategy`, `bz-invariant` |
| `l8-prisoners-and-boxes` | Prisoners and boxes | Use the cycle-following strategy and find its chance of success. | `bz-strategy` |
| `l9-egg-drop` | Dropping eggs | Minimise the worst case of a two-egg search with triangle numbers, then by dynamic programming. | `bz-search` |
| `l10-what-they-know` | What everyone knows | Reason about common knowledge in islander and muddy-children puzzles by induction. | `bz-strategy` |
| `l11-crossings-and-schedules` | Crossings and schedules | Find the fastest bridge or river crossing and prove that nothing beats it. | `bz-search` |

#### brainteasers level 3: Quick reasoning

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l12-clocks-and-trains` | Clocks, trains and rates | Solve clock-angle and meeting problems in one line of algebra. | `bz-quick` |
| `l13-digits-and-remainders` | Digits and remainders | Find last digits and test divisibility with modular arithmetic. | `bz-quick` |
| `l14-sums-in-one-line` | Sums in one line | Sum series and counts fast by pairing, telescoping and counting twice. | `bz-quick` |
| `l15-numbers-to-know` | Numbers to know | Estimate √2, e, ln 2, π² and powers of 2 to two figures, and use the rule of 72. | `bz-quick` |
| `l16-mixed-set` | A mixed brainteaser set | Solve an unlabelled set of brainteasers in interview order at a stated pace. | all four |

Numbers to check twice in the brief: 12 coins in 3 weighings (27 outcomes cover 24 cases); two eggs and 100 floors need 14 drops; 100 prisoners succeed with chance $1 - (H_{100} - H_{50}) \approx 0.3118$ (computed once here).

### `coding-int` (topic 3.5): Coding Interviews [Must]

- **Track:** `speed`. **Hours:** 60, plus the drill packs. **Levels:** 4, 19 lessons. **Prerequisites:** ds L1 to L4, graphs-dp L1 to L4, contests L1 (stress testing).
- **Skills:** `ci-patterns` Further patterns; `ci-strings` Strings and simulation; `ci-design` Design in code; `ci-timed` Solving under time.
- **Code:** Python by default; every level has at least one C++ `code` screen with the same tests, for developer-track learners. Homework difficulty 5 items are LeetCode medium to hard.
- **Builds on:** ds l6-sliding-window, l10-next-greater, l11-first-in-first-out, l12-nodes-and-pointers, l17-always-the-smallest, l18-order-book-heaps; algo-think l11-sorting-by-hand, l14-best-step-now; contests l4-stress-testing, l11-bitmasks, l14-which-first, l15-debugging-under-time; micro l1-bids-and-asks, l3-the-queue; py-found l12-data-with-behaviour.

#### coding-int level 1: Patterns still to learn

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-merging-intervals` | Merging intervals | Sort and merge intervals, and count overlaps with a sweep. | `ci-patterns` |
| `l2-prefix-trees` | Prefix trees | Build a trie and use it for prefix search and word lookups. | `ci-patterns` |
| `l3-window-maximum` | The maximum of a sliding window | Keep a monotonic deque to find every window's maximum in linear time. | `ci-patterns` |
| `l4-top-k` | The k largest and the running median | Use a size-k heap and two heaps for top-k and streaming medians. | `ci-patterns` |
| `l5-bit-tricks` | Bit tricks at interview | Use XOR, masks and shifts for the classic bit problems. | `ci-patterns` |

#### coding-int level 2: Strings and simulation

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l6-anagrams-and-palindromes` | Anagrams and palindromes | Solve string questions with counts, two pointers and expanding centres. | `ci-strings` |
| `l7-parsing-with-a-stack` | Parsing with a stack | Evaluate and decode nested expressions with a stack. | `ci-strings` |
| `l8-simulating-the-rules` | Simulating the rules | Turn a long rule statement into a correct simulation, as online assessments often ask. | `ci-strings`, `ci-timed` |
| `l9-grids-and-matrices` | Grids and matrices | Traverse, rotate and flood-fill a matrix without off-by-one errors. | `ci-strings` |
| `l10-matching-engine` | A matching engine | Simulate price-time priority matching of limit and market orders. | `ci-strings`, `ci-design` |

#### coding-int level 3: Design in code

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l11-lru-cache` | A least recently used cache | Combine a hash map and a linked list for constant-time get and put. | `ci-design` |
| `l12-file-system` | An in-memory file system | Design classes for a small file system with paths, folders and files. | `ci-design` |
| `l13-requirements-change` | When the requirements change | Extend working code when the interviewer adds a requirement part-way. | `ci-design`, `ci-timed` |
| `l14-rate-limiter` | Counting events in a time window | Design a sliding-window counter and a rate limiter for timestamped events. | `ci-design` |

#### coding-int level 4: Under the clock

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l15-reading-an-assessment` | Reading an online assessment | Triage an assessment's problems and plan the minutes before writing code. | `ci-timed` |
| `l16-edge-cases-first` | Edge cases first | List edge cases and write tests before the solution. | `ci-timed` |
| `l17-two-in-sixty` | Two problems in sixty minutes | Solve two medium problems inside 60 minutes, with a plan for partial credit. | `ci-timed` |
| `l18-talking-while-coding` | Talking while you code | Explain the plan and its trade-offs aloud while writing the code. | `ci-timed` |
| `l19-a-live-round` | A live coding round | Work a 45-minute live problem with two follow-ups. | `ci-timed`, `ci-design` |

**Drill packs (volume) [Must 1 to 4, Should 5 to 8].** Eight packs of 15 drills in `content/drills/`, one authoring session each, tagged by pattern and difficulty (2 to 5), every drill with hidden tests, a model solution and notes: (1) arrays and hashing, (2) two pointers and windows, (3) stacks, queues and binary search, (4) trees, tries and heaps, (5) graphs, (6) one-dimensional DP, (7) two-dimensional DP and backtracking, (8) intervals, greedy, bits and simulation. With the 1.8 and contests content this reaches the 150 problems of the 1.8 exit line. Packs 6 to 8 also in C++ once E8 lands.

### `research-int` (topic 3.5): Research Interviews [Must for the researcher track]

- **Track:** `speed`. **Hours:** 50. **Levels:** 4, 20 lessons. **Prerequisites:** regression L1 to L3, eigen L2, stat-learning L1 to L3, validation L1 to L3, numpy-pandas L3.
- **Skills:** `rq-stats` Statistics questions; `rq-linalg` Linear algebra questions; `rq-ml` Machine learning questions; `rq-case` The open case; `rq-data` Data tasks.
- **Builds on:** regression l2-slope-formula, l3-how-much-explained, l10-collinearity, l11-assumptions-fail; eigen l7-covariance-psd, l11-principal-components; estimation l3-right-target, l6-maximising; testing l3-p-value, l6-power, l10-correcting; stat-learning l3-bias-variance, l7-shrinking, l8-setting-to-zero; ensembles l6-random-forest, l8-which-features, l11-gradient-boosting; validation l5-shuffling-lies, l7-purging, l9-knows-the-answer; fin-ml l8-hidden-look-ahead; numpy-pandas l12-split-apply-combine; least-squares l8-qr, l10-normal-equations.

#### research-int level 1: Statistics and linear algebra questions

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-two-regressions` | Regress y on x, then x on y | Relate the two slopes and R² to the correlation, and say what duplicating the data changes. | `rq-stats` |
| `l2-correlation-limits` | What correlations can be | Find the range of a third correlation from two others, using a positive semidefinite matrix. | `rq-stats`, `rq-linalg` |
| `l3-estimators-on-the-spot` | Estimators on the spot | Derive a quick estimator with its bias and variance at a whiteboard. | `rq-stats` |
| `l4-tests-in-words` | Tests in plain words | Explain a p-value, power and a multiple-testing correction without jargon. | `rq-stats` |
| `l5-matrices-on-the-spot` | Matrices on the spot | Find eigenvalues of special matrices (all-ones, rank one, projections) by reasoning, not computing. | `rq-linalg` |

#### research-int level 2: Machine learning questions

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l6-bias-variance-aloud` | Bias and variance, aloud | Explain the bias-variance trade-off with a picture and a finance example. | `rq-ml` |
| `l7-ridge-against-lasso` | Ridge against lasso | Explain why the lasso sets coefficients to zero and when each penalty fits. | `rq-ml` |
| `l8-tree-questions` | Questions about trees and boosting | Answer the standard questions on splits, bagging, boosting and feature importance. | `rq-ml` |
| `l9-pca-questions` | Questions about PCA | Explain what principal components are, how to choose how many, and when they mislead. | `rq-ml`, `rq-linalg` |
| `l10-weak-signals` | Learning when the signal is weak | Explain why prediction in finance differs: low signal to noise, changing regimes and leakage. | `rq-ml` |

#### research-int level 3: The open case

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l11-framing-the-question` | Framing an open question | Turn "predict tomorrow's futures price" into a target, a horizon and a loss. | `rq-case` |
| `l12-features-and-data` | Features and data | Propose features and data sources, and name the leakage each could bring. | `rq-case` |
| `l13-baseline-first` | A baseline first | Fit and beat a simple baseline before anything clever. | `rq-case`, `rq-ml` |
| `l14-house-price-case` | The house price case | Work a full prediction case on a dataset, answering the interviewer's follow-ups. | `rq-case` |
| `l15-presenting-a-result` | Presenting a result | Report a result with its uncertainty, its failure modes and the next step. | `rq-case` |

#### research-int level 4: Data tasks and take-homes

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l16-interpolating` | Interpolating a series | Write a linear interpolator that handles gaps, edges and unsorted input. | `rq-data` |
| `l17-regression-by-group` | A regression for every group | Fit one regression per group in pandas and collect the coefficients. | `rq-data` |
| `l18-updating-a-fit` | Updating a fit as data arrives | Update a least-squares fit cheaply when a row arrives or leaves. | `rq-data`, `rq-linalg` |
| `l19-timed-data-task` | A timed data task | Clean, analyse and model a dataset inside a time limit. | `rq-data`, `rq-case` |
| `l20-writing-a-take-home` | Writing up a take-home | Write a take-home report that a reviewer can check and rerun. | `rq-case` |

L4 mirrors the reported Two Sigma OA tasks without copying them; data comes from seeded generators in the brief until E14 allows data files.

### `game-theory` (topic 3.3): Games, Auctions and Poker [Should]

- **Track:** `speed`. **Hours:** 35. **Levels:** 3, 15 lessons. **Prerequisites:** random-vars L2, conditional L2, equations (simultaneous equations).
- **Skills:** `gm-normal` Games in a table; `gm-mixed` Mixed strategies; `gm-sequential` Sequential games; `gm-auction` Auctions; `gm-poker` Poker and betting decisions.
- **Builds on:** random-vars l6-fair-price; graphs-dp l17-dice-stopping; micro l11-adverse-selection; markov l19-optional-stopping; puzzles l19-who-wins and l21-kelly (unwritten).

#### game-theory level 1: Games in a table

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-payoff-tables` | Payoff tables | Write a two-player game as a payoff table and read each player's best reply. | `gm-normal` |
| `l2-dominated-moves` | Moves no one should play | Remove dominated strategies until the game is small. | `gm-normal` |
| `l3-nash-equilibrium` | Nash equilibrium | Find the pure equilibria and say why neither player wants to move. | `gm-normal` |
| `l4-mixing` | Mixing to be unpredictable | Find a mixed equilibrium by making the opponent indifferent. | `gm-mixed` |
| `l5-zero-sum` | Zero-sum games and minimax | Value a zero-sum game by its minimax mixed strategy. | `gm-mixed` |

#### game-theory level 2: Sequential games and auctions

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l6-game-trees` | Games in a tree | Solve a sequential game by backward induction and spot threats nobody would carry out. | `gm-sequential` |
| `l7-guess-two-thirds` | Guess two thirds of the average | Iterate best replies and see why real players stop early. | `gm-sequential`, `gm-normal` |
| `l8-sealed-bids` | Sealed-bid auctions | Compare first-price and second-price auctions and bid well in each. | `gm-auction` |
| `l9-winners-curse` | The winner's curse | Shade a bid for a common-value prize, because winning is bad news. | `gm-auction` |
| `l10-splitting-a-pie` | Splitting a pie | Solve ultimatum and alternating-offer bargaining games. | `gm-sequential` |

#### game-theory level 3: Poker and decisions

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l11-pot-odds` | Pot odds | Call or fold by comparing your chance of winning with the price of the call. | `gm-poker` |
| `l12-ranges` | Ranges, not hands | Estimate your chance of winning against a range of hands. | `gm-poker` |
| `l13-toy-poker` | A toy poker game | Find the best bluffing and calling frequencies in a three-card poker game. | `gm-poker`, `gm-mixed` |
| `l14-value-of-information` | What information is worth | Price information as the expected gain from deciding after seeing it. | `gm-poker` |
| `l15-sizing-and-risk` | Sizing bets and risk | Compare expected value, expected log wealth and risk of ruin when sizing a bet. | `gm-poker` |

Number to check twice: the reported pot-odds call (30% to win, £100 in the pot, a £50 bet) needs 50/200 = 25% to break even, so it is a call.

### `systems` (topic 3.5): Systems for Developer Interviews [Should; Must for the developer track]

- **Track:** `speed` (strand `quant`, strandNote "Developer and low-latency roles"). **Hours:** 40. **Levels:** 4, 18 lessons. **Prerequisites:** cpp L1 to L4, cpp-pricing L3, cpp level 5 (below).
- **Skills:** `sy-memory` Memory and the machine; `sy-concurrency` Concurrency; `sy-os` Operating systems and networks; `sy-latency` Low-latency design.
- **Runtime note:** the C++ runtime has no threads, sockets or file system (AUTHORING section 3). Concurrency and OS lessons use listings, an interleaving canvas (E13) and single-threaded code that models the behaviour. Level 4 code runs.
- **Builds on:** cpp l7-addresses, l8-stack-and-heap, l9-owning-memory, l14-vector; cpp-pricing l9-timing, l10-memory-layout, l11-optimisation-flags; ds l11-first-in-first-out; micro l1-bids-and-asks.

#### systems level 1: Memory and the machine

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-latency-numbers` | Numbers every programmer should know | Order the costs of a register, cache, memory, disk and network access by powers of ten. | `sy-memory` |
| `l2-caches` | How caches work | Predict cache misses from an access pattern and a line size. | `sy-memory` |
| `l3-virtual-memory` | Virtual memory | Explain pages, the TLB and a page fault, and what each costs. | `sy-memory`, `sy-os` |
| `l4-object-layout` | Alignment and object layout | Work out a struct's size and padding, and reorder its fields to shrink it. | `sy-memory` |
| `l5-branches` | Branches and prediction | Explain branch prediction and remove a branch from a hot loop. | `sy-memory`, `sy-latency` |

#### systems level 2: Concurrency

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l6-threads` | Threads and what they share | Say what threads share and what each one owns. | `sy-concurrency` |
| `l7-data-races` | Data races | Find a data race by stepping two threads through an interleaving. | `sy-concurrency` |
| `l8-locks-and-deadlock` | Mutexes and deadlock | Protect shared data with a mutex and avoid deadlock by fixing the lock order. | `sy-concurrency` |
| `l9-atomics` | Atomics and memory order | Use an atomic counter and say what each memory order guarantees. | `sy-concurrency` |
| `l10-producer-consumer` | A producer and a consumer | Pass work between threads with a queue and a condition variable. | `sy-concurrency` |

#### systems level 3: Operating systems and networks

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l11-processes` | Processes and system calls | Explain a process, a system call and a context switch, and what each costs. | `sy-os` |
| `l12-files-and-sockets` | Files and sockets | Follow a read from a socket through the kernel into user space. | `sy-os` |
| `l13-tcp-and-udp` | TCP, UDP and multicast | Choose between TCP, UDP and multicast for orders and for market data. | `sy-os`, `sy-latency` |
| `l14-messages-on-the-wire` | Messages on the wire | Encode a market data message in a fixed binary layout and parse it back. | `sy-os`, `sy-latency` |

#### systems level 4: Low-latency C++

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l15-no-allocation` | No allocation on the hot path | Remove allocations from a hot path and write a pool allocator. | `sy-latency`, `sy-memory` |
| `l16-ring-buffer` | A ring buffer | Build a fixed-size single-producer, single-consumer ring buffer. | `sy-latency`, `sy-concurrency` |
| `l17-measuring-latency` | Measuring latency | Measure latency percentiles and say why the mean misleads. | `sy-latency` |
| `l18-feed-handler` | Designing a feed handler | Design a market data handler end to end and defend each choice aloud. | `sy-latency`, `sy-os` |

## (c) New levels appended to existing courses

### `puzzles` level 5: Puzzles firms keep asking [Must]

Skills: existing `pz-*` only. Builds on: puzzles L1 to L4 (unwritten), conditional l18-monty-hall, limits-thm l17-smallest-and-largest, estimation l3-right-target, markov l7-how-long.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l25-fair-from-biased` | A fair coin from a biased one | Make a fair bit from a biased coin and find the expected number of flips. | `pz-expectation`, `pz-symmetry` |
| `l26-estimating-n` | Estimating how many there are | Estimate a population size from serial numbers seen, and correct the maximum's bias. | `pz-conditioning`, `pz-expectation` |
| `l27-given-the-total` | Conditioning on a total | Find chances and expectations for dice and cards given their total or their maximum. | `pz-conditioning` |
| `l28-duels` | Duels and truels | Find each player's chance of winning a turn-based shooting game, and the best first move. | `pz-recursion`, `pz-games` |
| `l29-random-chords` | When "random" needs a definition | Show how the answer depends on how "random" is defined, with Bertrand's chord and the two envelopes. | `pz-geometry`, `pz-symmetry` |
| `l30-follow-ups` | The follow-up question | Extend a solved puzzle the way interviewers do: n-sided dice, more players, a cost per roll. | all six |

### `mm-games` level 4: Trading games firms run [Must]

Skills: existing `mg-*`. Builds on: mm-games L1 to L3 (unwritten), micro l2-walking-the-book, options l9-put-call-parity, puzzles l21-kelly (unwritten).

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l14-quoting-an-interval` | Quoting an interval | Give a 90% range for an unknown quantity, and score ranges by width and hit rate. | `mg-fair` |
| `l15-arbitrage-in-a-book` | Arbitrage in a set of quotes | Find profitable combinations of buys and sells in a set of quotes, fast. | `mg-quote` |
| `l16-several-contracts` | Several contracts on one outcome | Make consistent markets on several contracts tied to one die, and trade the mispricing between them. | `mg-fair`, `mg-quote` |
| `l17-options-on-a-game` | Options on a game | Quote calls, puts and straddles on a dice sum, and keep them consistent by parity. | `mg-quote`, `mg-risk` |
| `l18-betting-board` | A betting board with a bankroll | Track P&L and size bets across a board of bets under a bankroll limit. | `mg-risk` |

### `mental-pressure` level 4: Assessment batteries [Must]

Skills: existing `mp-*`. Builds on: mental-pressure L1 to L3 (unwritten), counting-chance l10-birthday, conditional l9-natural-frequencies, limits-thm l7-bell-curve.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l13-negative-marking` | Guessing when wrong answers cost | Decide when to answer, guess or skip when a wrong answer costs a point. | `mp-formats` |
| `l14-ranking-likelihoods` | Ranking likelihoods fast | Rank three events by probability within seconds, using benchmarks rather than exact sums. | `mp-estimate` |
| `l15-probability-at-speed` | Probability at speed | Answer short probability questions at about two minutes each, without a calculator. | `mp-formats`, `mp-fractions` |
| `l16-harder-sequences` | Harder sequences | Find the rule in interleaved, two-step and digit-based sequences. | `mp-formats` |
| `l17-full-battery` | A full assessment battery | Sit arithmetic, sequences and probability sections in a row at test pace. | `mp-formats` |

Number to check twice: with four options and −1 for a wrong answer, a blind guess is worth −0.5, a guess after removing one option −1/3, after removing two 0.

### `trees` level 4: Options at interview [Must for trader and strats]

Skills: existing `tp-*`. Builds on: options l9-put-call-parity, l10-bounds, l11-exercise-early, l12-how-price-responds; trees l10-black-scholes, l11-implied-vol, l12-delta-hedging; opt-dash l10-smile, l14-greek-profiles; markov l11-reflection.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l13-rules-of-thumb` | Rules of thumb for option prices | Estimate an at-the-money option as about 0.4σ√T times the spot, and check it against Black-Scholes. | `tp-bs` |
| `l14-greeks-by-shape` | The Greeks by shape | Sketch delta, gamma, vega and theta against spot and time, and sign them for common positions. | `tp-bs` |
| `l15-digitals` | Digital options and call spreads | Price a digital as a tight call spread and as $e^{-rT}N(d_2)$. | `tp-riskneutral`, `tp-bs` |
| `l16-the-smile` | The volatility smile | Read a smile and say what it implies about the risk-neutral distribution. | `tp-bs` |
| `l17-which-is-cheaper` | Which option is cheaper? | Rank exotic and vanilla options by price without computing them (Asian, barrier, lookback, American). | `tp-riskneutral`, `tp-multistep` |
| `l18-gamma-and-hedging` | Gamma and the hedged P&L | Explain a delta-hedged option's P&L as gamma times realised minus implied variance. | `tp-bs` |

Number to check twice: at spot 100, σ = 20%, T = 1 and r = 0, the rule gives 8.00 against a Black-Scholes price of 7.9656 (computed once here).

### `ito` level 4: Stochastic calculus at interview [Should; Must for strats and JP Morgan QR]

Skills: existing `it-*`. Builds on: ito L1 to L3 (unwritten), markov l8-which-end, l19-optional-stopping, l11-reflection.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l13-martingale-or-not` | Martingale or not? | Decide whether a function of Brownian motion is a martingale, and add the term that makes it one. | `it-martingale`, `it-calculus` |
| `l14-hitting-and-exit` | Hitting levels and exit times | Find the chance Brownian motion hits a before −b, with and without drift, and the expected exit time. | `it-bm`, `it-martingale` |
| `l15-moments-quickly` | Moments and integrals quickly | Compute moments of Brownian motion and the mean and variance of simple Itô integrals by the isometry. | `it-calculus` |
| `l16-pricing-in-a-minute` | Pricing questions in a minute | Answer quick risk-neutral pricing questions: a forward, a digital, a power payoff. | `it-pricing` |
| `l17-derivation-aloud` | A derivation aloud | Derive the Black-Scholes equation aloud inside five minutes, justifying each step. | `it-pricing` |

### `cpp` level 5: C++ questions at interview [Should; Must for the developer track]

Skills: existing `cp-*`. Builds on: cpp l9-owning-memory, l11-creation-destruction, l12-operators, l13-templates; cpp-pricing l5-payoff-classes, l11-optimisation-flags.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l19-moving-not-copying` | Moving instead of copying | Explain move semantics, write a move constructor, and say when a move happens. | `cp-memory`, `cp-classes` |
| `l20-rule-of-five` | The rule of five | Decide which special members a class needs and write them correctly. | `cp-classes` |
| `l21-virtual-dispatch` | How virtual functions work | Explain the vtable, object slicing and why a base class needs a virtual destructor. | `cp-classes` |
| `l22-undefined-behaviour` | Undefined behaviour | Spot undefined behaviour in short snippets and say what the compiler may do with it. | `cp-basics`, `cp-memory` |
| `l23-own-smart-pointer` | Writing your own smart pointer | Implement a minimal unique pointer and a reference-counted pointer. | `cp-memory` |

## (d) New exams

All are `content/exams/mock-<id>.json` (E5). Timed where the real ones are timed; formats follow the reported ones in `interview-gaps.md` and say "reported" on their intro screen. Each OA mock ships in three versions (fixed items) until E3 draws fresh items per sitting. Superdays use the stage-exam shape: papers plus self-ticked checks.

| Exam | Models | Format | Needs | Effort | Priority |
| --- | --- | --- | --- | --- | --- |
| `mock-oa-arith` | Optiver 80 in 8 | 80 four-option arithmetic items, 8 minutes, +1 and −1, forward only, no calculator; pass 55 net | E1, E2, E4 | 0.5 | [Must] |
| `mock-oa-trader` | Optiver, IMC, Citadel Securities batteries | Papers: sequences (15 in 25 min); probability at speed (15 in 30 min); likelihood ranking and intervals (10 in 10 min) | E1, E2 | 1 | [Must] |
| `mock-oa-sig` | SIG Quantitative Evaluation | 17 items in 60 minutes, calculator allowed, rising from quick expected values to multi-stage Bayes and ruin | E15 (or "use a calculator" in the intro) | 0.5 | [Must] |
| `mock-oa-code` | JP Morgan QR, Two Sigma SWE, GS fundamentals | 2 coding problems in 60 minutes, Python, four versions | E3 for fresh draws | 1 | [Must] |
| `mock-superday-trader` | Jane Street, Optiver, SIG, IMC, Citadel Securities finals | Papers: probability and expected value (45 min, 6 items with 2 spoken `longform`); mental maths and Fermi (15 min); market-making game (30 min, scripted until E12). Checks: a "why trading" answer recorded and self-marked; a full game played aloud with a partner | E10, E12 | 1 | [Must] |
| `mock-superday-research` | Two Sigma, Citadel, JP Morgan QR finals | Papers: probability and statistics (45 min); ML questions (30 min); coding (45 min, 2 problems); the open case (45 min, `longform` with rubric). Check: a behavioural story told aloud | E10, E14 | 1 | [Must] |
| `mock-oa-code-hard` | HRT, Citadel SWE | 3 problems in 90 minutes, Python or C++ | E8 | 1 | [Should] |
| `mock-oa-strats` | GS strats | Papers: coding fundamentals (30 min); maths, 8 multiple choice on calculus, linear algebra and probability (22 min) | none | 0.5 | [Should] |
| `mock-oa-quant-data` | MS IED quant finance, Two Sigma QR | 120 minutes: 10 statistics and applied-maths items (some `multi`), then 2 to 3 Python data tasks | E14 | 1 | [Should] |
| `mock-superday-developer` | HRT, Two Sigma QD, Jane Street SWE | Papers: coding (2 × 45 min, the second with a requirement added); C++ and systems (45 min); design (45 min, `longform`) | E8, E11 | 1 | [Should] |
| `mock-superday-strats` | GS and MS strats, JP Morgan QR markets | Papers: probability (30 min); derivatives and stochastic calculus (45 min); coding (45 min) | none | 1 | [Should] |
| `mock-video` | HireVue rounds | 3 behavioural questions, 30 s to prepare and 2 minutes to answer each, self-marked rubric | E9, E10 | 0.5 | [Could] |

Topic exams: `topic-3.3.json` (already in PLAN task 45) covers puzzles, mm-games, mental-pressure, brainteasers and game-theory skills; add `topic-3.5.json` [Should] for coding-int, research-int and systems; topic 0.7 has no exam (its homework is the real CV and stories).

## (e) Non-maths content for a self-contained app

- **Recruiting timeline and firm processes [Must]:** `recruiting` L1 (l3 calendar, l4 firm table with sources and an "as reported" date, l5 target list). The firm table is reviewed every cycle (E19).
- **Application strategy and CV [Must]:** `recruiting` L2 (l6 CV, l7 projects, l8 why this firm). Its homework yields a one-page CV and three "why us" paragraphs, self-marked against rubrics.
- **Assessments and video interviews [Must]:** `recruiting` l9 and l10, then `mock-video`.
- **Behavioural answers [Must]:** `recruiting` l11 (six stories), plus a bank family `behavioural` of about 30 questions as spoken `longform` items with rubrics (why trading, a failure, a decision with incomplete information, teamwork, a disagreement, a project you owned).
- **Reasoning aloud [Must]:** `recruiting` l12 teaches it once; mm-games l12, coding-int l18, ito l17 and the superday mocks practise it.
- **Offers and setbacks [Should]:** `recruiting` l14 and l15.
- **An application tracker [Could]:** E16.

## (f) Engine needs (ready for `docs/BACKLOG-INBOX.md`; not added there)

Checked first: `app/js/screens/exam.js` (timer per paper, one attempt, navigator with marking, fixed items, fraction pass mark, stage papers and checks, `longform` and `code` items allowed), `app/js/screens/drill.js` (9 Python drills, hidden tests, no timer), `app/js/screens/review.js` and `app/js/engine/select.js` (practice sets of 8 from finished lessons' quiz and review items, weighted by skill mastery with a skill-level Leitner of 1, 3, 7 and 30 days; a redo queue with two intervals; three weekly 1.5 problems), `app/js/screens/today.js` (120 s typed arithmetic warm-up), `docs/AUTHORING.md` sections 3 to 5 (`longform` rubric self-marking; C++ with no threads or catchable exceptions; fresh empty working directory per Python run), and ENGINE-BACKLOG 129 (timed table sets, deferred).

Raised later (interview plan):

- [Must] E1. `exam.js` scoring: every item counts +1 right and 0 otherwise, and the pass mark is a fraction. Wanted: per paper `scoring: { "right": 1, "wrong": -1, "blank": 0 }` and `passNet`, with the net score on the results screen. For `mock-oa-arith` (reported 80 in 8 format). Workaround: none faithful; the intro asks the learner to subtract wrong answers.
- [Must] E2. `exam.js` navigation: the navigator lets the learner go back and mark items. Wanted: `navigation: "forward"` on a paper (one item at a time, no return; `skip: false` forbids moving on without an answer). For the reported no-skip arithmetic and sequence tests. Workaround: honour system in the intro.
- [Must] E3. Exam item banks: a paper's `items` are fixed, so a resat mock repeats itself. Wanted: `draw: [ { "from": "bank/<family>", "tags": [...], "difficulty": [3, 4], "n": 5 } ]` resolved per attempt with a stored seed, items seen recorded, fresh items preferred. Workaround: three fixed versions per mock.
- [Must] E4. Generated exam items: the warm-up generator (`content/warmup.json`) feeds only Today's typed rounds. Wanted: `{ "generator": "arith", "mix": {...}, "n": 80, "options": 4 }` in a paper, with near-miss distractors (slipped digit, misplaced point, reverse operation), seeded per attempt. Workaround: pre-generated items in three versions.
- [Must] E5. A mock exam kind: only `topic-*` and `stage-*` exams exist, and topic exams must cover their topic's skills. Wanted: `exams/mock-*.json` with `style` (trader, research, developer, strats) and `models` (one plain line), listed on Review under "Mock assessments", exempt from the skill-coverage rule, every attempt kept with a score trend. Workaround: stage-exam format under a placeholder id.
- [Must] E6. Timed sets outside exams: lessons, reviews and practice have no clock (ENGINE-BACKLOG 129, deferred). Wanted: `timed: { "seconds": 480, "lockAtZero": true }` on a review, practice or bank deck, with a countdown and a live score, generalising item 129. Workaround: pace stated in prose.
- [Must] E7. Interview question bank with item-level spacing: practice draws only from finished lessons' quiz and review items and schedules by skill; the redo queue holds only misses. Wanted: `content/bank/<family>.json` (the AUTHORING item format plus `tags`: role, style, family, `source`), an "Interview practice" deck on Review that schedules each item (Leitner 1, 3, 7, 30 days, or SM-2 with a self-rated ease), mixes families, and folds the weekly problems into it after topic 3.3 starts. Workaround: level reviews and homework only.
- [Must] E8. Drill library: drills are Python only, untimed and unfiltered. Wanted: `language: "cpp"` drills through the C++ runner the `code` widget already uses, filters by pattern and difficulty on `#drill`, a stopwatch on each drill, and a "session" of two drills in 60 minutes with one countdown. Workaround: C++ problems as lesson `code` screens.
- [Should] E9. Per-item timing: no time is recorded per item. Wanted: seconds per item logged in exams, practice and bank decks; an optional `pace` (seconds) on an item; a results line naming the slowest families. Workaround: the exam's total time only.
- [Should] E10. Spoken answers: `longform` is written, then self-marked. Wanted: `mode: "speak"` with a preparation timer (for example 30 s), an answer timer (for example 120 s), optional local audio recording with playback (MediaRecorder, never uploaded, deletable), then the existing rubric self-mark; usable in bank decks and superday papers. Workaround: the learner speaks aloud, then ticks the rubric.
- [Should] E11. Follow-up parts: an item asks one question. Wanted: `parts: [...]` on an item, each revealed after the previous answer is checked, graded per part, so an interviewer's follow-ups can be modelled outside lessons (lessons have `ladder`). Workaround: a `table` widget with several cells, all visible at once.
- [Should] E12. Trading-game widget: mm-games quotes are `sliders` graded by `check` against a script. Wanted: a `trade` widget over the `orderbook` canvas: each turn the learner sets bid, ask and size; a seeded counterparty (noise, informed or scripted) trades; cards reveal on a schedule; position limits apply; a ledger shows position and P&L; the grade is final P&L against a benchmark plus rule breaks. Workaround: scripted turns with fixed trades.
- [Should] E13. Concurrency canvas: the C++ runtime has no threads. Wanted: an `interleave` canvas showing two or three threads' operations as steppable lanes over shared variables, with tap-to-mark the racing step and a `derive` of the final value. Workaround: `order` and `table` screens on listings.
- [Should] E14. Data files for code items: every Python run starts in an empty directory, so datasets must be inline in `prelude`. Wanted: `data: { "houses.csv": "content/data/houses.csv" }` on a `code` widget, copied into the working directory before each run (size cap stated). Workaround: seeded generators in `prelude`.
- [Could] E15. Calculator panel: `calculator: true` on a paper opens a basic calculator (the reported SIG test allows one). Workaround: the intro says to use one.
- [Could] E16. Application tracker on You: firms, roles, deadlines, stage and notes in the state document, exported with it. Workaround: a `recruiting` homework table.
- [Could] E17. Role filter: optional `roles` in `course.json` (trader, researcher, developer, strats) and a Study plan setting like `settings.quantOnly`, so Learn and Today can follow one track.
- [Could] E18. Readiness view: per role, bank coverage by family, the latest mock scores and pace against targets, on You.
- [Could] E19. Freshness: `asOf` and `sources` fields on lessons that state firm facts, shown under the lesson title, with a validator warning after 12 months.
- [Could] E20. Attention games like Zap-N: not planned; the reported games are proprietary and short. `recruiting` l9 describes them.

## (g) Order of work

Effort in levels. "Engine" items go to engine agents in parallel with content; content never waits for [Could] engine items.

| Phase | Work | Content levels | Other sessions |
| --- | --- | --- | --- |
| 0. Fast track (start now) | `recruiting` L1 to L2; `mental-pressure` L1 to L4; `puzzles` L1 to L2 (L1 in progress); engine E1, E2, E4, E5, E6; `mock-oa-arith`, `mock-oa-trader`, `mock-oa-sig` | 8 | 2 exam sessions; engine pass |
| 1. Trader core | `puzzles` L3 to L5; `brainteasers` L1 to L3; `mm-games` L1 to L4; `recruiting` L3; bank part 1 (200 items: probability, brainteasers, mental, market making, behavioural); engine E7, E9, E10 | 11 | 4 bank sessions; `mock-superday-trader` |
| 2. Coding and research core | `coding-int` L1 to L4; `research-int` L1 to L4; `trees` L4; drill packs 1 to 4; engine E3, E8, E11, E14 | 9 | 4 drill sessions; `mock-oa-code`, `mock-superday-research` |
| 3. Track depth | `game-theory` L1 to L3; `ito` L1 to L4; `cpp` L5; `systems` L1 to L4; bank part 2; drill packs 5 to 8; engine E12, E13 | 12 | 8 sessions; the five [Should] mocks; `topic-3.3`, `topic-3.5` |

Totals: **40 content levels** (27 new plus 13 already planned), about **26 other sessions** (12 exams in about 10, the bank in 8, drill packs in 8), and E1 to E14 as engine work. The [Must] subset is 28 levels: recruiting 3, brainteasers 3, coding-int 4, research-int 4, puzzles 5, mm-games 4, mental-pressure 4 and trees L4 1. Ten of the 28 are already planned (puzzles L1 to L4, mm-games L1 to L3, mental-pressure L1 to L3).

Second readers: PLAN task 47 (fix pass 1.9, reader and fix 1.8, then 2.1) stays; add readers for `puzzles` and `mental-pressure` after phase 1, because their numbers are the ones candidates will be marked on.

**Existing unwritten levels: which matter for these interviews.**

| Course and levels | Verdict | Why |
| --- | --- | --- |
| `puzzles` L1 to L4, `mm-games` L1 to L3, `mental-pressure` L1 to L3 | [Must] | The core of every trading-firm process and part of every bank's. |
| `ito` L1 to L3 | [Should] ([Must] for strats and JP Morgan QR) | Stochastic calculus is reported at JP Morgan QR and MS strats, rarely at trading firms. |
| `numerics` L1 (floating point) and L4 (Monte Carlo, finite differences) | [Should] | Developer floating-point questions; strats and desk-quant pricing questions. |
| `stat-models` L1 (GLMs, logistic) and L4 (Bayesian, MCMC) | [Should] for researchers | Logistic regression and conjugate priors come up in research rounds. |
| `momentum-rep`, `pairs-rep` (3.1) | [Should] for researchers | A finished replication is the strongest CV project for research roles and feeds `recruiting` l7. |
| `convex` L3 to L4 (KKT, gradient descent) | [Could] | Occasional optimisation questions in research and ML rounds. |
| `numerics` L2 to L3, `stat-models` L2 to L3, `convex` L1 to L2 | [Could] | Rarely asked of interns. |
| `odes` L1 (l5-mean-reversion) | [Could] | A rates-desk talking point only. |
| `complex`, `vector-calc`, `odes` L2 to L4, `measure-prob`, `pdes`, `algebra`, `topology`, `analysis` L4 to L5, `linear-maps` L3 to L4 | Not for these interviews | None of the reported processes test them at intern level. Keep them for the pure strand and for PhD research roles. |

## Left out

- Zap-N style attention games (E20): proprietary, short and not trainable in the same form.
- kdb+/q (one MS strats mention): niche; the SQL and pandas courses carry the ideas.
- System design at senior-engineer scale: intern developer rounds are coding and object design; `coding-int` L3 and `systems` l18 cover the intern form.
- A separate `options` interview course: `trees` L4 holds it, because it needs Black-Scholes.
- Copying reported questions word for word: every bank and mock item is our own wording and numbers, as the `puzzles` brief already requires.

## Questions for the user or main session

1. **Which cycle?** Today is 29 October 2026. Summer 2027 postings opened in July and August 2026 and many close or fill in the coming weeks. If you are applying this cycle, apply now, and the fast track (phase 0) is the priority; if summer 2028 is the realistic target, phases 0 to 3 can run in order.
2. **Region.** UK and European cycles add spring weeks and insight days for first-years and off-cycle internships; US cycles do not. Which should `recruiting` l3 and l5 lead with?
3. **Track.** Trader, researcher, developer or strats? Phases 2 and 3 can be reordered to put your track first.
4. **Topics.** New topics 0.7 and 3.5 (this plan), or everything under 3.3?
5. **Audio.** E10 records spoken answers locally in the browser. Is microphone use acceptable?

## User decisions (29 October 2026)

- **Cycle: both.** Apply opportunistically for summer 2027 now while building for 2028. Phase 0 (fast track) runs first.
- **Region: UK and Europe first.** `recruiting` l3 and l5 lead with the London cycle (spring weeks, insight days, off-cycle internships, £ figures); the US cycle follows as a comparison.
- **Tracks: trader and researcher first.** After phase 1, phase 2 runs `research-int` L1 to L4 before `coding-int` L1 to L4; `trees` L4 stays. Developer and strats depth (`systems`, `cpp` L5, `ito` L4, `mock-superday-developer`, `mock-superday-strats`, `mock-oa-code-hard`) move to a final phase 4, after `game-theory`, bank part 2 and the research mocks.
- **Audio: not wanted.** E10 is dropped. Spoken answers stay as `longform` items: the learner answers aloud, then ticks the rubric. A preparation or answer countdown may use E6 timers; no recording.
- **Topics (main session's call):** new topics 0.7 (Getting hired) and 3.5 (Interviews by role), as this plan proposes.
