# Stage 2 detailed curriculum: 2.2c Research method and statistical honesty

Blueprint work file, Stage 2 Phase 1. Draft 1, 7 October 2026.

**Source of truth.** `docs/curriculum.md` for stages, items, hours and exit tests, as amended by the owner's decisions at Blueprint review (7 October 2026), which adopted canon-gap proposal P1 as **item 2.2c, Research method and statistical honesty: 35 hours, Stage 2, immediately before 2.3 Projects, all tracks**. `docs/curriculum.md` has no line for 2.2c yet; until it does, this file proposes the item's text and rebuilds its exit (section 4.3) from `docs/blueprint/work/canon-gap.md` section G4 ("Exit") and the 2.2c resource canon in its section 6. This file expands 2.2c into courses, levels, lessons, homework, the topic exam and reading, rebuilds the exit in the app, and writes one lesson in full.

> **Binding owner decisions (7 October 2026).** These lines win over anything below that reads otherwise.
>
> | Decision | What it means for this file |
> |---|---|
> | P1 adopted: 35 h, item 2.2c, Stage 2, immediately before 2.3, all tracks; Stage 2 also gains 2.0a, 2.0b and 2.1b; P8 and P5 to P16 not adopted | The order is 2.0a, 2.0b, 2.1, 2.1b, 2.2, **2.2c**, 2.3, with 2.4 alongside. Nothing here assumes P5's dependent-data inference or P11's econometrics: the Newey-West and block-bootstrap tools this item needs are taught or recapped here (lessons 2 and 3) |
> | Correction 5: the Artifact publishes only files generated from this repository; no Python, no SQLite, no KaTeX fonts in the Artifact | **Every 2.2c code drill runs in Pyodide on the web app, or on CPython 3.12 on the learner's machine.** In the Artifact a drill screen shows the web-app link and accepts the result code. No lesson screen runs Python: lesson code is read-only (`predict-output`, `code-review`), quizzes use predict-the-output items (T), never code-with-tests items (K), and every number on a lesson screen comes from our own JavaScript models or from fixtures computed in CI. The exit audit and the pre-registration run on both targets; the exit drill runs on the web app. Maths renders as MathML in the Artifact |
> | Bertie confirmed as drawn, with the hair made less spiky: rounded, fuzzy, soft cloud-like tufts | Art notes in section 7 describe his hair as soft cloud-like tufts, never points |
> | Build order (a): engine and every P0 widget batch before content; content depth-first from 0.1 | 2.2c's one new widget and its modes (section 8) are P2, first used in Stage 2, and are briefed with the P2 waves |
> | Section 12 defaults: sealed answer key as recommended; outside marker and reviewer, paid; reliance check on | The audit's planted defects are sealed like an answer key (decision 12); the paid reviewer spot-checks 5 lessons of each course (`docs/PLAN.md` 12 decision 10) |

**Built on.** `docs/blueprint/work/canon-gap.md` (G4, sections 5.1, 6 and 8.2: what P1 still adds once the item files' first passes are counted); `docs/CURRICULUM.md` (index, conventions and the review's notes on skill grain and the Python floor); `docs/curriculum/stage1-probability.md`, the model for this file's structure and depth, and the most recent siblings `stage2-deep-learning.md` and `stage2-numerics-optimisation.md`; the sibling files whose lessons 2.2c builds on and must not repeat: `stage1-statistics-ts.md` (1.6 lessons 19, 38 to 42, 55 and 56; 2.2 levels SM1 and SM2, lessons 21 and 42), `stage2-ml-papers.md` (2.1 levels FD1, FD2 and FD6, lesson 151; 3.1 levels MP1, MP2, WS1 and WS2), `stage1-python-tools.md` (1.1 lesson 94 and level D3), `stage1-finance-projects.md` (1.7 lesson 19 and level MK3; 2.3 course RM, whose levels RM3 to RM5 and RM7 its decision 20 gives to P1: section 0.6); `docs/WIDGETS.md` (widget ids) and `docs/PLAN.md` 3.2 (scenes) and 12 (what P1 asks of the build); `docs/CONTENT-FORMAT.md` (ids, screen types, items, drills, verification); `docs/ASSESSMENT.md` (the ladder, the `topic` paper kind, the exit-part schema of 2.10, homework rules of 2.5, skills at level grain in 4.1); `docs/AI-TUTOR.md` (Bertie's modes and the exam gate); the owner's lesson-creator, maths-teaching, code-craft and project-forge skills.

**Tags.** [our choice] marks a design decision without outside evidence. [searched] marks a fact confirmed by web search: by canon-gap on 6 October 2026 (Arnott, Harvey and Markowitz 2019 in the Journal of Financial Data Science 1(1); the probability of backtest overfitting in the Journal of Computational Finance 20(4), 2017), or by this file's verification pass on 7 October 2026 (the verification log at the end lists each). [recalled] marks a fact from memory that I am confident of but did not verify here, chiefly figures quoted from papers (McLean and Pontiff's 26% and 58%, Simmons and others' 61%, Shumway's delisting returns, the replication shares of Hou, Xue and Zhang and of Jensen, Kelly and Pedersen, Recht and others' accuracy drops). [check] marks a resource detail (a chapter, section or exercise number, a template's current questions) recalled but not confirmed; confirm it before content cites it. [simulated] marks a number from a seeded simulation, shown as context or used to set a tolerance, never graded. [mode to add] marks a widget mode `docs/WIDGETS.md` does not list; [new] marks a new widget (section 8). No paper figure tagged [recalled] is ever an answer key: where a lesson computes with one, the stem states it as an input.

**Answers.** Every numeric answer in sections 2 (hooks that state a number), 3, 4 and 7 was recomputed on 7 October 2026 with Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, SymPy 1.14.0 and mpmath 1.3.0: exact fractions for prices, positions, counts and probabilities, SciPy's normal and bivariate-normal functions for Sharpe-ratio statistics and sequential looks, numerical integration for exact expected maxima and the significance filter, brute-force enumeration for CSCV splits and Shapley orders, and seeded simulation only to set drill tolerances. The project's floor is CPython 3.12; these runs are a record and are repeated at `docs/PLAN.md` stage 26 (`docs/CURRICULUM.md` review note 4).

**At a glance.**

| Item | Hours | Courses | Levels | Lessons | Lesson hours | Homework sets | Topic exam |
|---|---|---|---|---|---|---|---|
| 2.2c Research method and statistical honesty | 35 | 3 | 6 | 32 | 8.0 (22.9%) | 6 | `exm.research`, topic kind, 75 min, 14 items, 60 marks, 24 long-form, pass 70%, `slotMin` 0.7 on Q14 |

2.2c exit (`2.2c.exit`, proposed): audit a supplied backtest with five planted defects and find at least four; write a one-page pre-registration for project 2 before touching its data; report a deflated Sharpe ratio and a block-bootstrap interval for the audited strategy's Sharpe ratio once its defects are fixed; and pass `exm.research` (section 4.3). From then on every Stage 2 results note that reports a Sharpe ratio passes the P1 checklist (section 4.4).

---

## 0. Scope, decisions and conventions

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Unit of lesson time | **15 minutes per lesson, quiz included**, as every sibling file | 10 or 12 minutes | One unit across the path keeps hours tables comparable (`docs/CURRICULUM.md`, writing conventions) |
| 2 | What 2.2c takes from 2.3's course RM | **The inference, selection and writing levels move here, re-cut** (`stage1-finance-projects.md` decision 20 gave RM3 to RM5 and RM7 to P1). 17 lessons move with new ids: 2.3 lessons 14 to 19, 21 to 24, 30 and 37 to 41, and RM1's lesson 2 (hypothesis first). **7 retire as duplicates** of lessons every track now takes before 2.2c: 13 (1.6 lesson 19, same hook), 20 (1.6 lesson 42 and 2.1 lesson 144), 25 to 28 (2.1 lessons 117 to 122) and 29 (2.1 lesson 146). RM1, RM2, RM6 and RM8 stay in 2.3. Section 0.6 maps every id | (a) Moving RM3 to RM5 and RM7 whole, 23 lessons; (b) leaving them in 2.3 and teaching P1's additions beside them | (a) would teach walk-forward, purging, embargo and CPCV a second time and the expected maximum a third time, inside 35 hours; (b) would teach the Sharpe ratio's uncertainty and selection twice, once in 2.2c and once in 2.3. Ids are free to change: no lesson file exists, and `CONTENT-FORMAT.md` 4.1 makes the course the lesson's namespace, so a lesson that changes course changes id, as `docs/CURRICULUM.md` fix 2 did for 93 lessons. RM1's lesson 2 moves because the exit's pre-registration is written at the end of 2.2c, before 2.3 starts |
| 3 | Course structure | **Three courses on canon-gap G4's hour blocks**, ordered judge, audit, report: IS Is It Real? Inference and Selection (honest inference, and the selection half of backtest pathologies); AU Auditing Other People's Results (the backtest audit, and what survives in the published record); RP Reporting and Pre-registration (writing, and the protocol for the next study) | Four courses, one per block (two would hold 5 lessons each, too short to carry a homework rhythm); one course of six levels | The order follows the work: judge one result and many, audit someone else's, then report your own and plan the next. The item ends on the pre-registration because the exit's pre-registration is the learner's first act of 2.3. Section 1.4 sets the hours against canon-gap's split |
| 4 | Spine and checklist | **López de Prado, *Advances in Financial Machine Learning* (Wiley 2018) chapters 11 to 14** as spine (`src.afml-2018`, `basis`); **Arnott, Harvey and Markowitz (2019)** as the checklist the audit is scored against (`parallel-reading`); the canon-gap reading pack of method papers for each level (section 5) | A statistics-errors textbook as spine (Reinhart's *Statistics Done Wrong*, kept as stretch) | No textbook owns the topic (canon-gap G4). AFML is already 2.1's finance text, so the learner owns it; its chapter 11 ("The Dangers of Backtesting") holds the backtest sins and, in 11.6 "Strategy Selection", the CSCV method; chapter 14 ("Backtest Statistics") holds the PSR and the DSR in 14.7.2 and 14.7.3 [searched] |
| 5 | Place and tracks | **After 2.2 on every track; immediately before 2.3 on the researcher and trader tracks.** The developer track's order (`ASSESSMENT.md` 8.9: projects, then 2.1, then 2.2) puts 2.3 first, so there 2.2c follows 2.2 and comes before the developer's third project (alpha research, the first that tests a trading hypothesis); projects 1 and 4 keep 2.3's original note predicates. **Every track takes every lesson** | 2.2c before 2.1 on the developer track | 2.2c builds on 2.1's validation and leakage levels and 2.2's autocorrelation (section 1.3); taught before them it would need their content first. The owner adopted P1 for all tracks |
| 6 | Code and runtimes | **Owner correction 5.** Every drill runs in Pyodide (NumPy 2.4.6, pandas 3.0.2) on the web app, or on CPython 3.12 with `tools/py/uv.lock` locally; in the Artifact it hands off and returns by result code (`ASSESSMENT.md` 2.5 and 14.3). Lesson screens compute in JavaScript (`@zq/models/research`, section 8.3) with Python parity tests; quizzes use T items, never K items | Python on lesson screens | The Artifact has no Python under the publishing rule; a 15-minute lesson must not depend on a second app |
| 7 | What may be graded | **Never a simulated estimate.** Bootstrap intervals, null distributions and pipeline error rates appear on screens as fixture runs (computed in CI on a stored seed) or as predictions made before a run. A drill may grade a seeded estimate only against the reference implementation within a band CI measures as 4 seed-to-seed standard deviations (section 6, rule 2) | A tolerance on a resampled number chosen by eye | A tolerance chosen by eye fails honest learners on unlucky seeds or is too wide to teach |
| 8 | Data | **Synthetic panels with planted truths** from `market-gen` (2.3 decision 16) for every audit and inference exercise: delistings, splits, dividends, costs and effects whose true sizes CI knows. Real data appears only on the learner's machine, in 2.3's projects | Real price data in exercises | A planted truth makes an audit gradable ("the survivorship bias was 1.2 points a year") and keeps licensed data out of both targets |
| 9 | Figures from papers | **Context, never an answer.** Where arithmetic uses a published figure (McLean and Pontiff's 58%), the stem states it as an input; a lint forbids any accepted answer or distractor from depending on a figure tagged [recalled] | Grading recall of published numbers | The figures are [recalled], and what the lesson teaches is the arithmetic and the judgement, not the digits |
| 10 | Notation | $\widehat{SR}$ for an estimated Sharpe ratio **per period** unless the word "annual" is written; $T$ the number of periods; $q$ periods per year; $\gamma_3$ skewness and $\gamma_4$ kurtosis (not excess: 3 for a normal), as Bailey and López de Prado write them; $N$ the number of trials and $V$ the variance of the trials' Sharpe ratios; $\Phi$ and $\phi$ the standard normal distribution and density; $\gamma = 0.5772$ the Euler-Mascheroni constant; $\rho_k$ autocorrelations. Every screen that converts units says so once | Annual units inside the formulas | The commonest error in this material is mixing per-period and annual Sharpe ratios inside $\frac12\widehat{SR}^2$ (lesson 5's edge); fixing the convention removes it |
| 11 | Transfer screens | **A quant and an ML-lab context in every level** | Finance only | The same failures have other names in ML labs: test-set reuse, benchmark contamination, seed cherry-picking, missing error bars, leakage (canon-gap G4, "Why it matters"). The project's aim includes ML-lab-calibre thinking |
| 12 | Bertie | Built in from lesson 1: every screen carries `tutor.focus`, `tutor.notes` and `tutor.avoid` (`CONTENT-FORMAT.md` 3.10); in the Artifact through the `sample` capability, on the web app through the proxy; away during `exm.research` and the exit audit (`AI-TUTOR.md` 2.12). **Research-method rules**: he never names, locates or hints at a planted defect (the defects are sealed like an answer key); he never states a Sharpe statistic, interval or count before the screen's Check; he never writes or completes a pre-registration, results note or drill; on a pre-registration he gives his suggested rubric mark only after the learner's own self-mark. Guidance he prefers to statements: "what could the strategy have known at that moment?", "how many things were tried before this one?", "what would this number be on pure noise?" | | The audit and the pre-registration are the learner's evidence for the exit |
| 13 | Sample lesson | **Lesson 13, "Look-ahead in disguise"** (`lsn.audit.look-ahead-disguised`), in full in section 7 | Lesson 7 (the deflated Sharpe ratio); lesson 19 (why many findings are false) | Look-ahead is the first of the exit's five defects and the one most often hidden behind a correct-looking lag. The lesson gives the auditor a black-box test that does not require reading every line, and carries the one trap every learner meets: a lagged signal can still be computed from the future |
| 14 | Display codes | **IS, AU, RP** | One letter | None appears among the sibling files' codes [checked against `docs/CURRICULUM.md` section 1 and the 2.0a, 2.0b and 2.1b files]; ids do not depend on them |
| 15 | Topic exam and exit | **`exm.research`, topic kind**, with `slotMin` 0.7 on its writing slot; the exit adds the audit, the pre-registration and the honest-Sharpe drill (section 4.3) | A project as the whole exit | `ASSESSMENT.md` 2.8 gives every topic a paper unless its exit is a project; canon-gap's exit is three tasks, none of them a project |
| 16 | Homework size and time | **6 items a set**: 2 analysis items at difficulty 3, the code drill (difficulty 3 or 4), the long-form item (difficulty 4), 1 analysis item at difficulty 4 and 1 item at difficulty 5, **about 130 minutes** by `ASSESSMENT.md`'s per-difficulty estimates (d3 10 minutes, d4 20, d5 40, long-form 30, a code drill 20). Two items a set (one at difficulty 3 and the difficulty-4 analysis item) are interleaved "which tool?" items from earlier levels and topics (33%: the 25 to 30% rule rounds to 2 of 6) | 2.3's 6 items at 90 minutes; 2.1b's 8 or 10 items | 2.3's sets were the moved levels' sets and kept its shape; 90 minutes understated them by `ASSESSMENT.md`'s own estimates. Six sets of 130 minutes fit the 35 hours (section 1.4) |
| 17 | New widgets | **One new widget, `bias-audit`** (a scene, P2), and 12 modes on existing widgets (section 8). **`forking-paths` is not built**: lesson 32's garden of forking paths is a `garden` mode of `multiple-testing`, which already owns 1.6 lesson 41's forking mode | `forking-paths` as a separate widget, as `docs/PLAN.md` 12 lists for P1 | The garden is the forking model (the minimum $p$ over analyses of one data set) with its analyses laid out as a tree that `node-link` already draws; `docs/WIDGETS.md` decision 15 covers canon-gap's proposals with modes of existing widgets wherever a mode can do the job, and here one can |
| 18 | The P1 checklist | **Four `results-note` predicates** (`prereg-before-data`, `bias-audit-section`, `deflated-sharpe`, `bootstrap-interval`) required on every later results note that reports a Sharpe ratio: 2.3 project kinds `backtest`, `alpha` and `bot`, and 3.1's `replication` (section 4.4) | The checklist on 2.2c's own work only | Canon-gap 4.4 and `ASSESSMENT.md` 2.9 express the P1 exit change as `notePredicates`; without it the habits stop at the item's end |

### 0.2 What 2.2c inherits, and does not repeat

| Topic | Taught in | 2.2c does |
|---|---|---|
| The Sharpe ratio's standard error $\sqrt{(1 + \frac12 SR^2)/T}$ by the delta method | 1.6 lesson 19 | Lesson 1's first screen recaps it in one screen and moves to the PSR and the minimum track record; 2.3's lesson 13, which taught it again with the same hook, retires (decision 2) |
| The family-wise error rate, Bonferroni and Holm, Benjamini-Hochberg, forking paths, the best of $N$ noise strategies and the $t > 3$ hurdle | 1.6 lessons 38 to 42 | Lessons 7, 9 and 11 turn them into the DSR, the reality check and a pipeline's measured error rate; lesson 32 lays the forking paths out as a garden on one data set |
| HC and HAC standard errors | 1.6 lessons 55 and 56 | Lesson 2 applies Newey-West to overlapping returns and Lo's $\eta(q)$ to annualisation |
| Look-ahead bias and correct shifts; point-in-time joins with `merge_asof` | 1.1 lesson 94, level D3 | Lesson 13 tests for look-ahead from outside the code, in disguises a shift does not fix |
| Splits, adjustment factors and total return | 1.7 lesson 19 | Lesson 15 audits them in someone else's backtest, where an unadjusted split correlates with the signal |
| Spreads, costs and what trading costs | 1.7 level MK3 | Lesson 16 rebuilds a missing cost line from turnover and gives the break-even cost |
| Time-ordered splits, walk-forward, overlapping labels, purging, embargo, CPCV | 2.1 lessons 117 to 122 (and 2.2 lesson 21) | Not repeated: 2.3's lessons 25 to 28 retire (decision 2). Lesson 17 asks an audited report for its walk-forward figure |
| Leakage taxonomy, known-at times, pipeline leakage, target leakage, survivorship in ML, leak detection | 2.1 lessons 123 to 128 | Lessons 13 and 14 turn them into audit checks on a finance backtest |
| The best of $N$ models, leaderboards, one look at the hold-out, a research protocol | 2.1 lessons 144 to 147 | Lessons 6, 7, 22 and 30 deepen them; 2.3's lessons 20 and 29 retire |
| The capstone's results note | 2.1 lesson 151 | Lesson 24 holds the note to a sceptic's standard and moves the rubric that every later note uses |
| Test-set contamination and the sampling error of a validation loss | 2.1b lesson 79 | Lesson 22 adds paired tests between models and new test sets |
| Autocorrelation, stationarity, why returns; pairs without look-ahead (a full-sample hedge ratio) | 2.2 levels SM1 and SM2, lesson 42 | Lessons 2, 3 and 13 use them |
| Monte Carlo standard errors and seeds | 1.1 level A3; 2.0a course MO | Lessons 4 and 11 and the bootstrap drills state their Monte Carlo error |
| Reading papers, reproduction against replication, the replication ledger, the factor zoo, Hou, Xue and Zhang, Jensen, Kelly and Pedersen, the survival ratio | 3.1 levels MP1, MP2, WS1 and WS2 (Stage 3, later) | Not taught here. 2.2c's published-record level (AU2) teaches the mechanisms that shrink published effects and their ML forms; 3.1 then recaps lessons 19 to 21, 29 and 30 instead of 2.3's (request 4) |

### 0.3 Conventions for every lesson

**Ids** follow `CONTENT-FORMAT.md` 4.1. Topic `top.research-method` (full words, `docs/CURRICULUM.md` decision 1); library namespace `research` (`skl.research.*`, `mc.research.*`, `gen.research.*`, `drl.research.*`, `gls.research.*`), which no sibling uses. Courses `crs.inference` (IS), `crs.audit` (AU), `crs.reporting` (RP); levels `lvl.<course>.<slug>`, lessons `lsn.<course>.<slug>`, items `itm.<course>.<slug>`, homework `set.<course>.<level-slug>`, topic exam `exm.research`, exit part `2.2c.exit` (a working label fixed at first publish). None of these ids exists in any other file [checked by search on 7 October 2026]. The `#` column is the lesson's number within 2.2c (1 to 32); display numbers are computed from position and never stored.

**Every lesson** runs the design research 8.3 sequence: a hook on a canvas, free manipulation, the name for what the learner just did, a ladder of 2 to 4 screens adding one constraint each, the trap, the rule stated as a description of the learner's own steps with at least one derived line the learner completes, a transfer screen, the summary card, then a quiz of 4 items (5 where a production item is added). From the owner's skills, every lesson also carries the "why this exists" frame, one common trap, at least one edge case, a worked example with a decision point where the naive route fails, and a motivated leap wherever a creative step appears (`derive` screens carry `leap: naive, fails, pointsTo`). Research method adds two rules [our choice]:

- **Every number about a strategy says what it is measured against, over what period, and in what units** (per period or annual; gross or net; in sample, walk-forward or held out).
- **Every claim on a screen shows its uncertainty** (a standard error, an interval, a trial count), so the learner never sees a bare Sharpe ratio after lesson 1.

In this item the sequence's parts take particular forms. *Manipulation before notation* means dragging a future price and watching yesterday's position move, toggling a defect and watching the equity line fall, sliding the number of trials until a Sharpe ratio stops being significant, or adding seeds until two methods' error bars overlap. *The worked example's decision point* is usually a choice between two procedures that both look right: read every line or run a black-box test; fix defects one at a time or average over orders; count the shortlist or count every trial; compare best runs or compare at equal budget. *Derive* means completing a line of a variance, a hurdle, a test's boundary or a test length.

**Widgets** use the ids of `docs/WIDGETS.md`: the projects composites of its section 5.19 (`backtest-lab`, `sharpe-lab`, `results-note`, `paper-trader`, `signal-lab`), the ML composites of 5.17 (`overfit-lab`, `ml-workbench`, `time-cv-lab`, `leakage-detective`, `cluster-lab`), the statistics composites of 5.13 (`multiple-testing`, `test-lab`, `viva`, `summary-table`), the probability composites of 5.12 (`sampling-lab`, `icon-array`, `contingency-table`, `dist-explorer`), `time-series-lab` and `drawdown-lab` (5.8), `share-lab` (5.14), `code-review` (5.9), `mock-interview` (5.22), the code composites (`predict-output`, `code-cell` in homework only), and the shared primitives and inputs (`plot-2d`, `marks`, `slider`, `stepper`, `value-table`, `live-formula`, `node-link`, `sim-runner`, `token-tray`, `choice`, `numeric-input`, `expression-input`, `derivation-steps`, `card-sort`, `free-response`). One new widget, `bias-audit` [new], carries the audit (section 8). A mode a widget does not yet list is marked [mode to add].

**Quiz item types** (`CONTENT-FORMAT.md` 3.4), the letters of the siblings: N numeric, X expression, C single choice, M multi-select, O order the steps, S sort or match, I interval, P point or curve on a canvas, R region selection, A matrix or vector entry, T predict the output of shown code, and **W**, the short production item `ASSESSMENT.md` 2.3 adds to every lesson whose objective begins Derive, Prove or Show (2 to 4 lines or two sentences, 3-point rubric). Lessons 2, 20 and 31 carry a W item as their fifth. No K item appears in a quiz (decision 6). Long-form items appear in homework and the exam only. Single and multiple choice stay at or below 40% of each course's quiz items (section 0.4).

**Skills.** Each level lists its skills at level grain (`ASSESSMENT.md` 4.1): 4 to 7 a level, each introduced by one lesson, never more than 2 a lesson; finer distinctions (the add-one rule of an empirical $p$-value, the boundary of a perturbation) are step tags. Skill ids are `skl.research.<verb-phrase>`.

**Misconceptions.** Every `mc.research.*` id in the tables is new and joins the register. Where a lesson meets an error a sibling already registered (`mc.stats.more-tests-same-error`, `mc.stats.p-hacking-is-harmless`, `mc.ml.unlogged-trials-do-not-count`, `mc.ml.survivors-represent-the-market`), the tables use that id.

**Level review.** Every level ends with a Level review of 8 items at difficulty 2 to 4, interleaved, with up to 30% drawn from earlier levels of the course (`ASSESSMENT.md` 2.4). The homework set follows (section 3).

**Columns.** Objective is one measurable sentence. Hook is the problem the lesson opens with, its answer in brackets where it is a number. Trap names the misconception the trap screen is built around, with its id; Edge is the fringe case the lesson must show. Quiz lists the item types in order.

### 0.4 Summary of counts

| Course | Code | Id | Levels | Lessons | Lesson numbers | Lesson hours | Spine and papers |
|---|---|---|---|---|---|---|---|
| Is It Real? Inference and Selection | IS | `crs.inference` | 2 | 11 | 1 to 11 | 2.75 | AFML ch. 11, 13, 14; Lo (2002); Bailey and López de Prado (2012, 2014); Bailey and others (2017); White (2000); Harvey, Liu and Zhu (2016) |
| Auditing Other People's Results | AU | `crs.audit` | 2 | 12 | 12 to 23 | 3.0 | AFML ch. 11; Arnott, Harvey and Markowitz (2019); Ioannidis (2005); Gelman and Carlin (2014); McLean and Pontiff (2016); Recht and others (2019); Kapoor and Narayanan (2023); Henderson and others (2018); Dodge and others (2019) |
| Reporting and Pre-registration | RP | `crs.reporting` | 2 | 9 | 24 to 32 | 2.25 | Arnott, Harvey and Markowitz (2019); Nosek and others (2018); Simmons, Nelson and Simonsohn (2011); Gelman and Loken (2014) |
| **Total** | | | **6** | **32** | | **8.0** | |

Quiz items: 131 in the tables below (4 per lesson, and a W item in lessons 2, 20 and 31). Single and multiple choice are 49 of the 128 items other than W, 38.3%, and at most 39% in any course (IS 17 of 44, 38.6%; AU 18 of 48, 37.5%; RP 14 of 36, 38.9%) [counted from the tables by script; CI recounts from the lesson files]. All three courses (9 to 12 lessons) sit below design research 8.2's guide of 20 to 45 lessons, accepted [our choice]: 35 hours hold 32 lessons, and `docs/CURRICULUM.md` 1 already lists 22 courses outside the guide, which is not a schema rule. 17 of the 32 lessons are moved from 2.3 (section 0.6); 15 are new.

### 0.5 Open items and requests to other papers

| # | Item | Effect | Who decides |
|---|---|---|---|
| 1 | Figures quoted from papers [recalled]: McLean and Pontiff's 26% lower out of sample and 58% lower after publication; Simmons and others' 61% false-positive rate from four flexibilities together; Shumway's average performance-delisting return near $-30\%$; Hou, Xue and Zhang's share of anomalies failing $t \ge 1.96$ (about two thirds); Recht and others' ImageNet accuracy drops (about 11 to 14 points). Kapoor and Narayanan's count of affected papers (294 across 17 fields) is now [searched] | Context lines only (decision 9); a wrong figure changes a sentence, never a grade | A person with the papers, before the lessons citing them are written |
| 2 | AFML section numbers still unconfirmed: which section of chapter 11 lists the seven sins (recalled as 11.2, "Mission Impossible: The Flawless Backtest") and chapter 13's section numbers. Confirmed by search on 7 October 2026: 11.1 to 11.6 by title, 11.6 "Strategy Selection", 14.7.1 to 14.7.4 (the Sharpe ratio, the PSR, the DSR, efficiency statistics). Whether AFML's end-of-chapter exercises have public solutions: none official found by search | Reading table; lessons cite topics, not numbers | A person with the book |
| 3 | The `rubric` instrument over an auto-marked item: the exit audit (`itm.audit.exit-findings`) is marked automatically out of 10, not self-marked | `ASSESSMENT.md` 2.10 must accept an auto-marked mark as "confirmed", or add an `item-mark` instrument | `ASSESSMENT.md` owner |
| 4 | Speed of the stationary bootstrap in Pyodide: 5,000 resamples of about 3,000 days in the exit drill, which needs index generation vectorised in NumPy, not a Python loop over days [unverified] | If a 2023 laptop misses a 2-minute budget, the drill drops to 2,000 resamples and its tolerance widens to 0.15 (4 seed-to-seed standard deviations at that size [simulated]) | Measured when the drill is built |
| 5 | The developer track's Stage 2 order in `content/plan.yaml` (decision 5) | 2.2c must be inserted after 2.2 and before the developer's alpha project | `ASSESSMENT.md` 8.9 owner; the owner |
| 6 | The exam's aids: a formula card and normal quantiles in the in-app calculator (section 4.1) | If the calculator lacks $\Phi^{-1}$, the card prints a short table of normal quantiles | `ASSESSMENT.md` 3.1 owner |
| 7 | MathML rendering of the DSR and PSR fractions on the owner's iPhone (correction 5's spike) | If they misrender, those screens show the formulas in `live-formula`'s slotted form | Stage 2 spike |
| 8 | Track for the exit pre-registration: "project 2" on tracks whose plan has no alpha project | The pre-registration is written for the first 2.3 project on the learner's plan that tests a trading hypothesis (`alpha`, else `bot`, else the strategy evaluation of `backtest`) | Owner; `ASSESSMENT.md` 8.9 `projectOrder` |

**Requests to other papers.**

| # | Paper | Request |
|---|---|---|
| 1 | `docs/curriculum.md` (owner) | Add 2.2c's line under Stage 2 with the exit text of section 4.3 |
| 2 | `docs/CURRICULUM.md` | Add 2.2c to sections 1 to 3 (3 courses, 6 levels, 32 lessons, 8.0 lesson hours; the hours table of section 1.4 with its estimate mapping; prerequisites 2.1, 2.2, 1.6, 1.7) and remove the moved and retired lessons from 2.3's rows |
| 3 | `docs/curriculum/stage1-finance-projects.md` | Apply section 0.6: remove 2.3 lessons 2, 13 to 30 and 37 to 41 (24 lessons) and levels RM3, RM4, RM5 and RM7; renumber 2.3; return the hours (24 lessons, 4 sets, 4 level reviews: about 13 hours) to projects; move outcomes PJ-O3, PJ-O4 and PJ-O7 to 2.2c (RS-O1, RS-O2, RS-O5) and retire PJ-O5 (2.1's); replace `exm.proj.methods` Q2 and Q3 with BT and AR items (2.2c's paper now examines them); RM1 lessons 4 and 5 and BT4 lessons 66 to 71 recap 2.2c lessons 13 to 17 in one screen each and spend their time on building the point-in-time universe and the engine's guards; BT4 lesson 70 and BT6 lesson 82 add a one-screen walk-forward recap (2.1 lesson 118) for developer-track learners who reach BT before 2.1; project 2's Blueprint milestone reuses the locked 2.2c pre-registration (1.5 of its 8 hours return to Build); the four P1 note predicates join the `backtest`, `alpha` and `bot` projects (section 4.4) |
| 4 | `docs/curriculum/stage2-ml-papers.md` | 3.1 lesson 9 recaps 2.2c lessons 29 and 30 (it recapped 2.3 lesson 2); lesson 95 recaps 2.2c lesson 21; lessons 25 and 106 and the 0.2 row naming "2.3 RM3 to RM7" cite 2.2c; `prj.papers.replication` gains the four P1 note predicates; 2.1 lessons 144 to 147 and 151 add forward pointers to 2.2c lessons 6, 7, 22, 30 and 24 |
| 5 | `docs/curriculum/stage1-statistics-ts.md` | 1.6 lessons 19, 41 and 42 add forward pointers to 2.2c lessons 1, 32 and 7 |
| 6 | `docs/WIDGETS.md` | Add `bias-audit` (section 8.1) and the modes of section 8.2; move the first uses of `sharpe-lab`, `backtest-lab`, `paper-trader` and `mock-interview` from 2.3 to 2.2c (section 8.3); record that `forking-paths` is the `garden` mode of `multiple-testing` (decision 17) |
| 7 | `docs/ASSESSMENT.md` | Exit row `2.2c.exit` (section 4.3, `estHours: 5.75`); paper data for `exm.research` with `slotMin: { q14: 0.7 }`; the four note predicates of section 4.4 and the Stage 2 exit change of 2.9; open item 3; the developer-track order (open item 5) |
| 8 | `docs/AI-TUTOR.md` | Decision 12's research-method rules; Bertie off during `itm.audit.exit-findings`; the pre-registration's mark order (self-mark first) |
| 9 | `docs/PLAN.md` 12 | P1's row: new widget `bias-audit` only (decision 17); Python `numpy-pandas` on the web app only (correction 5) |
| 10 | `docs/blueprint/work/canon-gap.md` and `content/sources.yaml` | Existing ids used: `src.afml-2018`, `src.arnott-harvey-markowitz-2019`, `src.hlz-2016`, `src.dsr-2014`, `src.pbo`, `src.bailey-2014-charlatanism`, `src.white-2000`, `src.lo-2002`, `src.mclean-pontiff-2016`, `src.hxz-2020`, `src.jkp-2023`, `src.ioannidis-2005`, `src.simmons-2011`, `src.gelman-loken-2014`, `src.henderson-2018`, `src.recht-2019`, `src.dodge-2019`, `src.kapoor-narayanan-2023`, `src.reinhart-sdw`, `src.chan-qt-2e`. New, `checked: false` until confirmed: `src.bailey-lopezdeprado-2012`, `src.politis-romano-1994`, `src.hansen-2005`, `src.sullivan-timmermann-white-1999`, `src.getmansky-lo-makarov-2004`, `src.shumway-1997`, `src.novy-marx-velikov-2016`, `src.luo-2014-seven-sins`, `src.gelman-carlin-2014`, `src.harvey-2017`, `src.bouthillier-2021`, `src.pineau-2021`, `src.nosek-2018`. The verification pass confirmed the bibliographic details of `src.bailey-lopezdeprado-2012`, `src.shumway-1997`, `src.bouthillier-2021` and `src.pineau-2021` by search, so those four may enter as `checked: true` |

### 0.6 Lessons moved from 2.3, and lessons retired

Moved lessons keep their objective and substance; their rows in section 2 are rewritten for 2.2c's place in the path (new recaps, fresh hooks where the old one repeated a sibling, skills at level grain). Retired ids were never written to a lesson file, so retiring them needs no migration (`CONTENT-FORMAT.md` 4.1: only a published id is immutable).

| 2.3 # | 2.3 id | Disposition | 2.2c id | 2.2c # |
|---|---|---|---|---|
| 2 | `lsn.method.hypothesis-first` | Moves (RM1 keeps 5 lessons) | `lsn.reporting.hypothesis-first` | 29 |
| 13 | `lsn.method.sharpe-standard-error` | Retires: 1.6 lesson 19, same hook; recapped on lesson 1's first screen | | |
| 14 | `lsn.method.minimum-track-record` | Moves | `lsn.inference.track-record` | 1 |
| 15 | `lsn.method.autocorrelation-hac` | Moves | `lsn.inference.autocorrelation` | 2 |
| 16 | `lsn.method.block-bootstrap` | Moves | `lsn.inference.block-bootstrap` | 3 |
| 17 | `lsn.method.random-entry-null` | Moves | `lsn.inference.matched-null` | 4 |
| 18 | `lsn.method.regime-stability` | Moves | `lsn.inference.decay-or-noise` | 5 |
| 19 | `lsn.method.trial-ledger` | Moves | `lsn.inference.trial-ledger` | 6 |
| 20 | `lsn.method.expected-max-sharpe` | Retires: 1.6 lesson 42 and 2.1 lesson 144; its formula with the Euler-Mascheroni term joins lesson 7 | | |
| 21 | `lsn.method.deflated-sharpe` | Moves | `lsn.inference.deflated-sharpe` | 7 |
| 22 | `lsn.method.pbo-cscv` | Moves | `lsn.inference.pbo-cscv` | 8 |
| 23 | `lsn.method.reality-check` | Moves | `lsn.inference.reality-check` | 9 |
| 24 | `lsn.method.parameter-plateaus` | Moves | `lsn.inference.plateaus` | 10 |
| 25 | `lsn.method.time-splits` | Retires: 2.1 lesson 117, 2.2 lesson 21 | | |
| 26 | `lsn.method.walk-forward` | Retires: 2.1 lesson 118 | | |
| 27 | `lsn.method.purge-embargo` | Retires: 2.1 lessons 120 and 121 | | |
| 28 | `lsn.method.cpcv` | Retires: 2.1 lesson 122 | | |
| 29 | `lsn.method.one-look` | Retires: 2.1 lesson 146; the lock is lesson 30 here | | |
| 30 | `lsn.method.out-of-sample-decay` | Moves | `lsn.audit.post-publication` | 21 |
| 37 | `lsn.method.results-note` | Moves | `lsn.reporting.results-note` | 24 |
| 38 | `lsn.method.honest-charts` | Moves | `lsn.reporting.honest-charts` | 25 |
| 39 | `lsn.method.negative-results` | Moves | `lsn.reporting.negative-results` | 26 |
| 40 | `lsn.method.readme-dual-register` | Moves | `lsn.reporting.readme-two-registers` | 27 |
| 41 | `lsn.method.defence` | Moves | `lsn.reporting.defence` | 28 |

Levels: `lvl.method.inference` becomes `lvl.inference.one-result`; `lvl.method.selection` becomes `lvl.inference.selection`; `lvl.method.writing` becomes `lvl.reporting.writing`; `lvl.method.validation` retires. Sets: `set.method.inference`, `set.method.selection`, `set.method.validation` and `set.method.writing` are replaced by 2.2c's six sets (section 3). Drills: `drl.proj.block-bootstrap` becomes `drl.research.stationary-bootstrap`, `drl.proj.deflated-sharpe` becomes `drl.research.deflated-sharpe`, `drl.proj.metrics-consistency` becomes `drl.research.note-consistency`, and `drl.proj.purged-kfold` retires (2.1's `drl.ml.purged-kfold` holds the same task).

---

## 1. Item overview

### 1.1 Purpose in a quant and ML-lab career

- **It is the job.** A quant researcher's value is the false discoveries they do not ship. Harvey, Liu and Zhu (2016) argue that a new factor needs a $t$-statistic above about 3.0, not 2.0; McLean and Pontiff (2016) find anomaly returns lower out of sample and lower again after publication; Bailey and López de Prado's deflated Sharpe ratio adjusts a result for the number of trials behind it (canon-gap G4). A researcher who cannot say how many things were tried, what the held-out period showed and what a result would look like on noise is not trusted with capital.
- **ML labs run the same discipline under other names.** Test-set reuse, benchmark contamination, seed cherry-picking, missing error bars and leakage (Kapoor and Narayanan 2023; Henderson and others 2018; Recht and others 2019; Dodge and others 2019) are selection and look-ahead in another field. An ML-lab interviewer asks "how many seeds?", "was the comparison at equal tuning budget?" and "is that gap larger than the test set's sampling error?"; course IS and level AU2 answer them with numbers.
- **The audit is a daily task.** Quants spend more time checking other people's backtests (a colleague's, a vendor's, a paper's) than writing their own. Level AU1 gives an order of work and a test for each defect class, so a one-day audit finds the defects that matter first and states each one's effect.
- **The curriculum's own exits depend on it.** 2.3 asks for three projects, each with a results note that says what failed; 3.1 asks how much of a published effect survived. Without a pre-registration, a trial count, a deflated Sharpe ratio and an interval, those notes cannot be told apart from marketing. The P1 checklist (section 4.4) keeps the habits in force after the item ends.
- **A self-taught learner has no supervisor.** Research method is taught inside dissertations and capstones, not as a named course (canon-gap 2.2, point 9); the app has to be the supervisor, and the audit, the pre-registration and the checklist are how it supervises.

### 1.2 Learning outcomes

At the end of 2.2c the learner can:

| # | Outcome | Measured by |
|---|---|---|
| RS-O1 | Quantify one strategy's uncertainty: the probabilistic Sharpe ratio and the minimum track record with skewness and kurtosis, annualisation under autocorrelation, a stationary-bootstrap interval, a matched null and a sub-period test | 85% on fresh difficulty-3 items; exam Q1, Q2, Q5; homework IS1 long-form at 7 of 10 |
| RS-O2 | Correct for selection: the trial ledger and the effective number of trials, the expected maximum of $N$ trials, the deflated Sharpe ratio, PBO by CSCV, the reality check, parameter surfaces, and a pipeline's error rates measured on noise | Exam Q7, Q8, Q13; homework IS2 long-form at 7 of 10; `drl.research.exit-honest-sharpe` |
| RS-O3 | Audit a backtest someone else wrote: triage by warning signs, look-ahead by the future-perturbation test, the universe, price adjustments, costs and capacity, in-sample choices, and the attribution of interacting defects in an audit report | Exam Q3, Q6, Q9, Q10, Q12; homework AU1 long-form at 7 of 10; the exit audit at 8 of 10 |
| RS-O4 | Read the published record: the share of findings that are true, the significance filter's exaggeration, a post-publication haircut, a benchmark gap's paired error, and comparisons at equal budget over seeds | Exam Q4, Q11; homework AU2 long-form at 7 of 10 |
| RS-O5 | Write and defend results: a one-page note a sceptic accepts, honest charts, a failure section, a two-register README, and answers under questioning | Exam Q14 at 7 of 10 (`slotMin`); homework RP1 long-form at 7 of 10; every later results note's P1 checklist |
| RS-O6 | Pre-register: a falsifiable hypothesis with a mechanism, a locked one-page plan with a decision rule, the test length and power, and exploration kept apart from confirmation | Exam Q11 (power variant); homework RP2 long-form at 7 of 10; the exit pre-registration at 7 of 10 |
| RS-O7 | Pass the 2.2c exit | `exm.research` at 70% with Q14 at 7 of 10; the audit at 8 of 10; the pre-registration at 7 of 10; the honest-Sharpe drill (section 4.3) |

### 1.3 Prerequisites

- **2.1 Machine learning**, especially level FD1 (validation through time, lessons 117 to 122), FD2 (leakage, lessons 123 to 128), FD6 (overfitting by search, lessons 144 to 147) and lesson 151 (the capstone's results note).
- **2.2 Time series**, levels SM1 and SM2 (returns, stationarity, autocorrelation), lesson 21 (leakage in time series) and lesson 42 (pairs without look-ahead).
- **1.6 Statistics**, lessons 19 (the Sharpe ratio's standard error), 38 to 42 (many tests at once) and 55 and 56 (HC and HAC errors); **1.5 Probability** for normal tails and order statistics; **1.7 Finance basics**, lesson 19 (splits and total return) and level MK3 (costs); **1.1 Python**, lesson 94 (look-ahead) and level D3 (point-in-time joins); **1.2 Tools** for the drills' tests; **2.0a** course MO for Monte Carlo error.
- **Alongside**: 2.4 Contests runs across Stage 2 in the Build block; the Daily 10 and the weekly probability problems continue.

**Feeds.** 2.3 (every project that tests a hypothesis starts from 2.2c's pre-registration and ends with a note that passes the P1 checklist; BT4 and RM1 recap the audit lessons), 3.1 (every replication uses the pre-registration and the checklist; WS2 recaps level AU2), 3.3 (level TR1's statistics questions, TR3's ML-lab depth and the project round of IV4's mock interviews).

### 1.4 Hours budget (35 h)

| Block | What | Hours | Share | Unit that carries the estimate |
|---|---|---|---|---|
| In-app lessons | 32 lessons at 15 minutes, quiz included | 8.0 | 22.9% | `Lesson.est` |
| In-app practice and redo | 6 level reviews of 8 items at about 15 minutes (1.5); the Redo queue at 7 and 30 days (0.75) | 2.25 | 6.4% | Reviews: summed item `est`. Redo: spent time, no estimate |
| Homework | 6 sets of 6 items at about 130 minutes each (decision 16) | 13.0 | 37.1% | Homework `set.*`, summed item `est` |
| Exams | `exm.research` (1.25); one practice paper of the same shape (1.25); reviewing both (0.5) | 3.0 | 8.6% | `exm.research` minutes (1.25); the practice paper and both reviews (1.75): spent time |
| External reading | The reading pack by section (section 5): IS1 0.75, IS2 1.0, AU1 0.75, AU2 1.0, RP1 0.25, RP2 0.5 | 4.25 | 12.1% | `Level.companion` hours |
| Exit work | The audit, `itm.audit.exit-findings` (2.0); the pre-registration, `itm.reporting.exit-prereg` (1.5); the honest-Sharpe drill, `drl.research.exit-honest-sharpe` (1.0) (section 3.2) | 4.5 | 12.9% | Item and drill `est` |
| **Total** | | **35.0** | 100% | Estimates: **32.5 h (92.9%)**; spent-only time 2.5 h |

**The estimate sum.** Lessons 8.0, level reviews 1.5, homework 13.0, `exm.research` 1.25, companion 4.25 and exit work 4.5 make 32.5 h, inside CI's 10% rule (`CONTENT-FORMAT.md` 6.7). The Redo queue (0.75 h), the practice paper (1.25 h) and the two reviews (0.5 h) are spent time only, as in `stage1-linear-algebra.md` 1.4. `2.2c.exit` `estHours` (5.75: exit work 4.5 and `exm.research` 1.25) is the planner's display figure and is not added again.

**Against canon-gap's split** (G4: honest inference 6, backtest pathologies 14, replication and reproducibility 10, writing 5). By level, counting lessons, review, homework, reading and the exit work each level feeds: IS1 4.4 h (honest inference); IS2 5.9 h and AU1 6.9 h (pathologies, 12.8 h, including the exit audit and drill); AU2 4.7 h and RP2 5.4 h (the published record and the protocol, 10.1 h, including the pre-registration); RP1 3.9 h (writing); exams and redo 3.75 h. Writing is 1 hour lighter than canon-gap's estimate because 2.1 lesson 151 already teaches the results note; inference is lighter because 1.6 lesson 19 teaches the standard error.

Solving time (everything except the 4.25 hours of reading and the non-task screens of lessons, about 2 hours) is 28.75 hours, 82%, above the curriculum's 60% floor (rule 2).

**Pace.** About 3.5 weeks at the curriculum's 15-hour week (`ASSESSMENT.md` 8.3): the Main block (9 h) carries lessons, practice, homework, exams and reading (30.5 h, 3.4 weeks); the Build block (3 h) carries the exit work (4.5 h, 1.5 weeks) beside 2.4 contests. The pre-registration is written in the last week, so it is locked days before 2.3's project 2 opens its data.

---

## 2. Courses

Three courses, 6 levels, 32 lessons. Each level is 4 to 7 lessons, then a Level review (8 items) and a homework set (section 3). Every exercise runs on synthetic data with planted truths (decision 8).

### Course IS: Is It Real? Inference and Selection (`crs.inference`, 2 levels, 11 lessons)

How much one strategy's numbers can tell, and how much the search that found it inflated them. The course takes a Sharpe ratio from a point to a distribution (its uncertainty with skewness, kurtosis and autocorrelation, an interval by the block bootstrap, a null that keeps everything but the timing, a test across sub-periods), then counts the trials behind it and deflates it: the trial ledger, the expected maximum of $N$ trials, the deflated Sharpe ratio, PBO by CSCV, the reality check, parameter surfaces, and a pipeline's error rate measured on noise. Spine: AFML chapter 14 (backtest statistics, the PSR and the DSR in 14.7.2 and 14.7.3), chapter 11 (strategy selection, 11.6) [searched] and chapter 13 (backtesting on synthetic data) [check sections]; Lo (2002); Bailey and López de Prado (2012, 2014); Bailey, Borwein, López de Prado and Zhu (2017); White (2000); Harvey, Liu and Zhu (2016). It recaps 1.6 lessons 19 and 38 to 42 and 2.1 lessons 144 and 146 in one screen each.

**Level IS1: How sure is one result?** (`lvl.inference.one-result`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 1 | `lsn.inference.track-record` How long a record? The probabilistic Sharpe ratio | Compute the probabilistic Sharpe ratio $\Phi\left(\frac{(\widehat{SR} - SR^*)\sqrt{T - 1}}{\sqrt{1 - \gamma_3\widehat{SR} + \frac{\gamma_4 - 1}{4}\widehat{SR}^2}}\right)$ against a benchmark $SR^*$ and the minimum track record length, in per-period units (from 2.3 lesson 14; its first screen recaps 1.6 lesson 19) | Three years of daily returns with annual Sharpe 1.0: 1.6 lesson 19 gave a standard error of 0.58. How many years of daily data before you can be 95% sure (one-sided) that a strategy with annual Sharpe 0.5 has a true Sharpe above 0? (2,730 days, about 10.8 years) | `sharpe-lab` (PSR, years), `live-formula` | Trap: a Sharpe ratio of 1 over three years is proof (`mc.research.one-sharpe-is-proof`); its PSR against 0 is 0.958, and against a benchmark of annual 0.5 only 0.81. Edge: negative skew and fat tails raise the bar through $-\gamma_3\widehat{SR}$ and $\frac{\gamma_4 - 1}4\widehat{SR}^2$, which matter only when the per-period Sharpe ratio is large: a monthly strategy notices them, a daily one barely does (homework IS1 example B) | N, N, C, X |
| 2 | `lsn.inference.autocorrelation` Autocorrelated returns: annualising honestly | Derive the variance of a $q$-period sum from the autocorrelations, annualise a Sharpe ratio with Lo's $\eta(q) = \frac{q}{\sqrt{q + 2\sum_{k=1}^{q-1}(q - k)\rho_k}}$, and use Newey-West errors for a mean of overlapping returns (from 2.3 lesson 15; recapping 1.6 lesson 56) | A smoothed, illiquid fund's monthly returns have autocorrelations $0.3^k$ and monthly Sharpe 0.25. Is $0.25\sqrt{12} = 0.87$ its annual Sharpe? (No: $\eta(12) = 2.61$, so 0.65; $\sqrt{12}$ overstates it by a third) | `sharpe-lab` (annualise), `time-series-lab` (acf), `derivation-steps` | Trap: multiplying by $\sqrt q$ whatever the dependence (`mc.research.sqrt-q-always`), including for overlapping monthly returns built from daily data. Edge: negative autocorrelation (a mean-reverting book) makes $\sqrt{12}$ understate: $\eta(12) = 4.17$ at $\rho_k = (-0.2)^k$ | X, N, C, M, W |
| 3 | `lsn.inference.block-bootstrap` The block bootstrap for a Sharpe ratio | Build a stationary-bootstrap interval for a Sharpe ratio, explain why resampling single days understates the uncertainty of dependent returns, and report the mean block length with the interval (from 2.3 lesson 16) | Daily returns follow an AR(1) with coefficient 0.4. A bootstrap that resamples single days gives an interval for the mean return. Too narrow by what factor? ($\sqrt{1.4/0.6} = 1.53$) | `sampling-lab` (bootstrap, stationary blocks [mode to add]), `time-series-lab` | Trap: the plain bootstrap for a time series (`mc.research.iid-bootstrap-for-series`). Edge: the block length is a choice to report and vary; volatility clustering widens a Sharpe ratio's interval even when returns are uncorrelated, because the squares are dependent | N, C, P, S |
| 4 | `lsn.inference.matched-null` Does it beat chance? Nulls with the same exposure | Build a null distribution from random entries or circularly shifted signals that match holding period, turnover and market exposure, and compute an empirical $p$-value with the add-one rule (from 2.3 lesson 17) | A moving-average rule earns Sharpe 0.6. Of 1,000 random-entry strategies with its holding period and exposure, 120 beat it. $p$-value? ($\frac{121}{1{,}001} = 0.121$) | `paper-trader` (null), `backtest-lab` | Trap: testing against zero when a long-biased rule rides a rising market (`mc.research.zero-is-the-null`). Edge: a null keeps what the claim does not credit (exposure, turnover, volatility clustering) and destroys only the timing; shuffling days destroys clustering too and is too easy to beat; add one to numerator and denominator so $p$ is never 0 | N, C, M, S |
| 5 | `lsn.inference.decay-or-noise` Decay or noise? Sub-periods compared | Compare sub-period Sharpe ratios against their sampling error, test all of them together with $Q = \sum_i\frac{(\widehat{SR}_i - \overline{SR})^2}{\mathrm{SE}_i^2}$ against $\chi^2_{k-1}$, and decide between decay and noise (from 2.3 lesson 18) | Annual Sharpe by decade from daily data: 1.4, 0.2 and $-0.3$; each decade's standard error is about 0.32. Decay or noise? (First against last is 3.8 standard errors apart; all three together give $Q = 14.9$ on 2 degrees of freedom, $p = 0.0006$, or $Q = 15.2$ and $p = 0.0005$ with the unrounded errors of 0.317: decay) | `sharpe-lab` (sub-periods [mode to add]), `backtest-lab` (holdout) | Trap: testing the best decade against the worst after looking (`mc.research.compare-chosen-extremes`): that comparison is itself a selection, which is why the joint test exists. Edge: putting the annual Sharpe ratio into $\frac12\widehat{SR}^2$ gives 0.45 for the first decade's error; with daily data the term uses the daily ratio and is negligible, so 0.32 is right | N, N, C, O |

Skills: `skl.research.compute-psr-and-track-record` (1), `skl.research.annualise-under-autocorrelation` (2), `skl.research.block-bootstrap-a-sharpe` (3), `skl.research.build-a-matched-null` (4), `skl.research.test-subperiod-stability` (5).

Transfer screens: lesson 2 is why hedge-fund indices of illiquid assets look safer than they are (Getmansky, Lo and Makarov 2004 [recalled]); lesson 3's interval is the uncertainty line of every later results note; lesson 4 is the ML lab's random baseline with the same label distribution; lesson 5 applied to a model's validation score by year separates a drifting world from a noisy metric.

Then the Level review and homework `set.inference.one-result`.

**Level IS2: Many trials, one winner** (`lvl.inference.selection`, 6 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 6 | `lsn.inference.trial-ledger` Counting what you tried: the trial ledger | Log every configuration tested, cluster correlated variants into effectively independent trials, and report both counts with the result (from 2.3 lesson 19) | You tried 5 look-back windows, 4 holding periods and 3 universes. How many trials do you report? (60, and the effective number after clustering) | `ml-workbench` (ledger), `cluster-lab` (correlation) | Trap: reporting only the final specification (`mc.ml.unlogged-trials-do-not-count`). Edge: a variant only looked at on a chart counts; two variants with return correlation 0.95 are nearly one trial | N, C, M, S |
| 7 | `lsn.inference.deflated-sharpe` The deflated Sharpe ratio | Compute the expected maximum Sharpe ratio of $N$ unskilled trials, $SR_0 = \sqrt V\left[(1 - \gamma)\Phi^{-1}\left(1 - \frac1N\right) + \gamma\Phi^{-1}\left(1 - \frac1{Ne}\right)\right]$, and the deflated Sharpe ratio, the PSR against $SR_0$ (from 2.3 lessons 20 and 21; 1.6 lesson 42 gave the idea) | The best of 50 trials has annual Sharpe 1.5 over 4 years of daily data, skewness $-0.5$, kurtosis 5; the trials' annual Sharpe ratios have variance 0.25. Significant? (The hurdle is an annual 1.14; DSR 0.76, below 0.95, although the plain PSR is 0.998) | `sharpe-lab` (deflated), `overfit-lab` (zoo) | Trap: $N$ taken as the number of final candidates (`mc.research.n-is-the-shortlist`). Edge: the hurdle grows with the trials' spread, so wild trials cost more; the approximation slightly overstates the exact expected maximum of 50 normals (2.28 against 2.25) | N, N, C, M |
| 8 | `lsn.inference.pbo-cscv` The probability of backtest overfitting | Compute PBO by combinatorially symmetric cross-validation from a matrix of trial returns by block, and read the distribution of the out-of-sample rank logits (from 2.3 lesson 22) | 16 blocks give $\binom{16}{8} = 12{,}870$ ways to split them in half; in 8,500 the in-sample winner ranks below the median out of sample. PBO? (0.66) | `overfit-lab` (CSCV) | Trap: one train-test split is enough evidence (`mc.research.one-split-suffices`). Edge: PBO near 0.5 means selection added nothing, above 0.5 that it did harm; blocks must be long enough that serial dependence does not leak across them | N, O, C, N |
| 9 | `lsn.inference.reality-check` White's reality check and the $t > 3$ hurdle | Test whether the best of many strategies beats a benchmark with a bootstrap of the maximum, and compare the answer with Bonferroni and with Harvey, Liu and Zhu's hurdle (from 2.3 lesson 23) | The best of 200 strategies has $t = 2.8$. Significant? (No: Bonferroni needs 3.48 one-sided at 5%; alone, its $p$ of 0.0026 times 200 is 0.51) | `multiple-testing` (strategy zoo), `sharpe-lab` (haircut) | Trap: Bonferroni on highly correlated strategies taken as the answer (`mc.research.bonferroni-for-correlated`): it is too strict there, which the reality check's bootstrap of the maximum repairs. Edge: Hansen's test for superior predictive ability (2005) removes the power lost to poor strategies in the set; Sullivan, Timmermann and White (1999) ran the reality check over thousands of technical rules [recalled] | C, N, M, S |
| 10 | `lsn.inference.plateaus` Parameter sweeps: plateaus against spikes | Read a parameter heat map, prefer plateaus to spikes, and fix the selection rule before running the sweep (from 2.3 lesson 24) | A moving-average grid on a simulated random walk: the best cell has Sharpe 1.4, its neighbours average $-0.2$. Real? (No: an isolated spike on noise; a random walk has no edge to find) | `overfit-lab` (sweep) | Trap: picking the best cell (`mc.research.best-cell-is-the-answer`). Edge: a plateau can still be one overfit choice made a level up (the universe, the start date), which the ledger must count | C, P, O, S |
| 11 | `lsn.inference.pipeline-on-noise` Run the whole pipeline on noise | Measure a research pipeline's false-positive rate by running it, selection step included, on synthetic data with no effect, with the rate's binomial interval, and its power on data with a planted effect (AFML chapter 13's idea) | Your pipeline tries 20 correlated signals and reports the best if its $p < 0.05$. On 200 noise data sets it reports a "discovery" 58 times. Its false-positive rate, with a 95% interval? (0.29, from 0.23 to 0.35 by the normal approximation; the exact Clopper-Pearson interval is 0.23 to 0.36) | `sim-runner`, `multiple-testing` (strategy zoo), `value-table` | Trap: each test's 5% is the pipeline's 5% (`mc.stats.more-tests-same-error`). Edge: 20 independent tests would give $1 - 0.95^{20} = 0.64$; correlated signals give fewer false alarms, which is why the measured rate, not the formula, is reported; a planted effect of known size gives the power lesson 31 needs | N, C, M, S |

Skills: `skl.research.count-effective-trials` (6), `skl.research.deflate-a-sharpe` (7), `skl.research.estimate-pbo` (8), `skl.research.test-the-best-of-many` (9), `skl.research.read-a-parameter-surface` (10), `skl.research.measure-pipeline-error-rates` (11).

Transfer screens: lessons 6 and 7 are the arithmetic of hyperparameter search and test-set reuse in ML benchmarks (2.1 lesson 144); lesson 9's reality check is the right test of "our model beats 30 baselines"; lesson 11 is how a lab validates an evaluation harness before trusting it: run it on a model that cannot be better and count how often it says it is.

Then the Level review and homework `set.inference.selection`.

### Course AU: Auditing Other People's Results (`crs.audit`, 2 levels, 12 lessons)

The same discipline turned outwards. Level AU1 teaches the audit the exit sets: an order of work, a test for each of the five defect classes (look-ahead, survivorship, price adjustments, costs, in-sample choices), the attribution of defects that interact, and a report that states each defect's effect. Level AU2 reads the evidence on how often published results hold up, in finance and in ML, through the mechanisms that shrink them: low prior odds, the significance filter, decay after publication, reused benchmarks and unequal budgets. Spine: AFML chapter 11, "The Dangers of Backtesting", 11.2 to 11.5 [searched headings] (with Luo and others' seven sins of quantitative investing as it lists them [recalled]); Arnott, Harvey and Markowitz (2019) as the checklist; Ioannidis (2005); Gelman and Carlin (2014); McLean and Pontiff (2016); Recht and others (2019); Kapoor and Narayanan (2023); Henderson and others (2018); Dodge and others (2019). The factor zoo and the replication method stay in 3.1 (section 0.2).

**Level AU1: The backtest audit** (`lvl.audit.backtest`, 7 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 12 | `lsn.audit.triage` Where to look first | Triage a backtest report by its warning signs (a simple rule above Sharpe 2, a smooth equity line, a high hit rate, no costs, returns from a few days, no held-out period, no trial count) and order the audit's checks by expected damage and cost to test | Five one-paragraph reports and one day: "Sharpe 3.2, daily rule, costs not modelled"; "0.9 after costs, 0.6 held out, 22 trials"; "Sharpe 1.8, 94% of months positive"; "Sharpe 1.4, half the return from 6 days"; "Sharpe 1.1, look-back optimised, no held-out period". Order them for the audit (the cost-free daily rule, then the 94% of positive months, then the six days, then the optimised look-back; the second report last) | `bias-audit` (triage) [new], `card-sort` | Trap: auditing the code line by line from the top (`mc.research.audit-top-down`), which spends the day where defects are least likely. Edge: some genuine strategies (market making, very short horizons) do have high Sharpe ratios, with low capacity to match; a high Sharpe calls for an explanation, not a verdict | O, S, C, M |
| 13 | `lsn.audit.look-ahead-disguised` Look-ahead in disguise | Detect look-ahead in a backtest you did not write with the future-perturbation test, and name its disguise: a full-sample statistic, a centred window, backward fill, a hedge ratio or scaler fitted on all the data (recapping 1.1 lesson 94) | Two versions of one rule hold a share tomorrow when today's close is below the average close: version F averages all ten days, version E only the days so far, and both lag the signal by a day. F makes £12 on three trades, all winners; E makes £4; holding throughout makes £0. Which backtest can be trusted? (E only: F's average contains the future) | `backtest-lab` (perturb [mode to add]), `code-review`, `card-sort` | Trap: a lagged signal cannot read the future (`mc.research.shift-means-no-look-ahead`). Edge: the test changes only prices after day $t$ and compares only positions decided on or before $t$; changing day $t$ itself flags honest rules; inputs that are not prices (index membership, restated accounts) need their own perturbation | C, S, N, T |
| 14 | `lsn.audit.universe` The universe: survivorship and today's facts | Audit a universe for survivorship and selection by today's facts (today's index members, "shares with ten years of history"), count names by date, and estimate the bias from missing delisting returns (recapping 2.1 lesson 127) | Each year 4% of a small-cap universe delists for poor performance, with an average delisting return of $-30\%$. A backtest that silently drops those names overstates an equal-weighted long book by about how much a year? (1.2 percentage points) | `leakage-detective` (universe), `backtest-lab` (bias: universe), `plot-2d` (names by date) | Trap: a constant count of names shows a clean universe (`mc.research.constant-count-is-clean`): 500 names on every date of a 20-year backtest of "the index" is usually today's 500. Edge: a takeover delisting is good news and a bankruptcy bad, so the bias depends on the mix (Shumway 1997 found performance delistings near $-30\%$ [recalled]; Shumway and Warther 1999 put Nasdaq's missing performance-delisting returns near $-55\%$ [searched]); in a long-short book it can go either way | N, C, O, S |
| 15 | `lsn.audit.adjusted-prices` Prices that never traded: splits, dividends and adjustment | Find corporate-action defects: returns from unadjusted closes across splits, dividends counted twice, and back-adjusted price levels in price filters (recapping 1.7 lesson 19) | A share closes at 80.00, splits 2-for-1 overnight and closes at 40.60. Return from raw closes? ($-49.25\%$.) The true return? ($+1.5\%$) | `share-lab` (split), `backtest-lab` (bias: adjustment [mode to add]), `value-table` | Trap: an unadjusted split only adds noise (`mc.research.splits-are-noise`): firms split after their price has risen, so a rule that shorts recent winners holds splitting shares on split days and books each 2-for-1 split as a 50% gain. Edge: adjusted closes already include dividends, so adding the cash again counts the yield twice every year; back-adjusted levels in a "price above 5 dollars" filter select on prices that never traded | N, N, C, M |
| 16 | `lsn.audit.missing-costs` Costs and capacity: the missing-cost defect | Rebuild the cost drag from turnover and cost per unit traded, compute the net Sharpe ratio and the break-even cost, and compare it with realistic costs for the universe (recapping 1.7 level MK3) | A rule earns 12% a year gross with 10% volatility, trading 50% of its book a day counting buys and sells, in shares costing 5 basis points per unit traded. Net Sharpe? (0.57: the drag is 6.3% a year.) Break-even cost? (9.5 basis points) | `backtest-lab` (costs), `slider` | Trap: costs are small because each trade is cheap (`mc.research.cheap-trades-cheap-strategy`): turnover multiplies them 126 times a year here. Edge: costs rise with size through impact, so a backtest must state its account size; costs concentrate on the days the strategy trades most, which are often the stressed days with the widest spreads (Novy-Marx and Velikov 2016 [recalled]) | N, N, C, P |
| 17 | `lsn.audit.in-sample-choices` Parameters chosen on the period they are judged on | Spot parameters and design choices fixed on the evaluation period (a look-back, a start date, a universe, "standard" settings), estimate their selection effect as the best of $N$, and ask for the walk-forward or held-out figure (recapping 2.1 lessons 118 and 146) | The report says "look-back 37 days" and shows a 10-year Sharpe of 0.9. You learn 50 look-backs were tried. What would the best of 50 unskilled look-backs show over 10 years? (About 0.71: 2.25 standard errors of $1/\sqrt{10} = 0.316$) | `overfit-lab` (sweep), `backtest-lab` (holdout) | Trap: settings "from the literature" are not choices (`mc.research.literature-defaults-are-free`): someone else chose them in sample, on data that overlaps yours. Edge: a start date just after a crash is a parameter too; ask for the result from every start year | N, C, M, S |
| 18 | `lsn.audit.attribution-report` Interacting defects and the audit report | Attribute a Sharpe ratio's inflation to interacting defects by averaging each fix's effect over the orders of fixing (the Shapley split), and write the audit report: location, evidence, mechanism, effect, fix and how the fix was checked | With two defects the Sharpe is 2.1; fixing A alone gives 1.2, fixing B alone 1.5, fixing both 0.3. How much is A's fault? (1.05: 0.9 if fixed first, 1.2 if fixed second; B's is 0.75; together 1.8) | `bias-audit` (attribution) [new], `results-note` (audit report [mode to add]) | Trap: the effects of fixes add up, so each can be measured alone (`mc.research.fix-effects-add`): measured alone they sum to 1.5, not the 1.8 that disappears. Edge: a false finding costs as much credibility as a missed one; limitations (one market, assumed costs) are not defects and have their own section | N, N, O, M |

Skills: `skl.research.triage-a-backtest` (12), `skl.research.detect-look-ahead` (13), `skl.research.audit-the-universe` (14), `skl.research.audit-price-adjustments` (15), `skl.research.audit-costs` (16), `skl.research.audit-in-sample-choices` (17), `skl.research.attribute-and-report-defects` (18).

Transfer screens: lesson 13's test is the check for 2.1 lesson 125's pipeline leak (a scaler fitted on every row) and for any ML evaluation: change the test rows and confirm the training transform does not move; lesson 14's universe is a benchmark built from images that survived a quality filter; lesson 18's report is the form of an ML conference's reproducibility report.

Then the Level review and homework `set.audit.backtest`.

**Level AU2: What survives: the published record** (`lvl.audit.literature`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 19 | `lsn.audit.false-findings` Why many published findings are false | Compute the share of significant findings that are true (the positive predictive value) from the share of true hypotheses, the power and the significance level, and show how bias lowers it (Ioannidis 2005) | Of 1,000 hypotheses tested, 100 are true; tests have power 0.8 at the 5% level. What share of the "discoveries" are true? (0.64: 80 true against 45 false.) With power 0.2? (0.31) | `icon-array` (FDR, bias [mode to add]), `contingency-table` | Trap: $p < 0.05$ means a 95% chance the finding is true (`mc.research.p-is-probability-true`). Edge: a field of long shots (1 in 100 true, power 0.5) gets fewer than one true discovery in ten; Ioannidis's bias $u = 0.2$ turns a PPV of 0.5 into 0.2 | N, N, C, M |
| 20 | `lsn.audit.significance-filter` The significance filter exaggerates | Show that conditioning on significance exaggerates a true effect when power is low, and compute the power, the expected significant estimate and the exaggeration ratio (Gelman and Carlin 2014) | A strategy's true annual Sharpe is 0.3; it is tested on 5 years of data (standard error $1/\sqrt5 = 0.447$) at one-sided 5%. If it passes, what Sharpe will be reported on average? (0.97, more than three times the truth; power is 0.17) | `test-lab` (significance filter [mode to add]), `dist-explorer` (truncated normal) | Trap: a significant estimate is an accurate one (`mc.research.significant-means-accurate`). Edge: in two-sided tests of tiny effects the filter also flips signs: a true 0.1 passes with the wrong sign 26% of the time | N, N, C, M, W |
| 21 | `lsn.audit.post-publication` After publication: what to plan on | Shrink a published or backtested return towards what live trading delivers, using the evidence on anomalies out of sample and after publication (from 2.3 lesson 30) | A published anomaly earned 0.8% a month in its paper. Suppose, as McLean and Pontiff (2016) report [recalled], returns are 58% lower after publication. Plan on what? ($0.8\times 0.42 = 0.34\%$ a month) | `sharpe-lab` (haircut), `multiple-testing` (zoo-timeline) | Trap: live performance equals the backtest (`mc.research.live-equals-backtest`). Edge: part of the decay is arbitrage by readers, which says the effect was real; part is lesson 20's filter, which says it was smaller all along; 3.1 lesson 95 estimates the decay itself | N, C, O, S |
| 22 | `lsn.audit.benchmark-reuse` Benchmarks reused: gaps, leaderboards and new test sets | Judge a gap between two models on a shared test set by a paired test (McNemar), and explain test-set reuse, contamination and leakage as the ML forms of selection and look-ahead (Recht and others 2019; Kapoor and Narayanan 2023; recapping 2.1 lesson 145 and 2.1b lesson 79) | Two models score 76.3% and 76.0% on the same 10,000 test images; they disagree on 600, 315 to 285 in the first's favour. Is the gap real? ($z = \frac{30}{\sqrt{600}} = 1.22$, $p = 0.22$: no) | `overfit-lab` (leaderboard), `contingency-table` (paired [mode to add]) | Trap: a gap on a famous benchmark is real because the test set is large (`mc.research.leaderboard-gap-is-real`). Edge: pairing helps: the unpaired standard error of the gap is 0.60 points, the paired one 0.24; a test set rebuilt by the original recipe can be harder, lowering every score without any overfitting, which is how Recht and others read their own drops [recalled] | N, C, M, S |
| 23 | `lsn.audit.seeds-and-budgets` Seeds, budgets and error bars | Compare methods at equal tuning budgets and over several seeds, computing the expected best validation score of $n$ trials (Dodge and others 2019) and reporting the spread across seeds (Henderson and others 2018) | Two methods have identical scores over their settings, uniform from 0.70 to 0.80. Method A gets 50 tuning trials and method B 5. Expected best score of each? (0.798 against 0.783: A "wins" by budget alone) | `overfit-lab` (zoo), `dist-explorer` (maximum of $n$ [mode to add]) | Trap: the best run is the method's performance (`mc.research.best-seed-is-the-method`). Edge: paired seeds (each seed run by both methods) cancel shared noise; a difference smaller than the seed spread needs more seeds, not a sharper claim (Bouthillier and others 2021 [recalled]) | N, N, C, S |

Skills: `skl.research.compute-ppv` (19), `skl.research.correct-for-the-significance-filter` (20), `skl.research.haircut-a-published-effect` (21), `skl.research.judge-a-benchmark-gap` (22), `skl.research.compare-at-equal-budget` (23).

Transfer screens: lessons 19 and 20 are why a first backtest of a published idea should expect less, and why an ML paper's best ablation is rerun on fresh seeds before anyone builds on it; lesson 22 is a reviewer's first question about any leaderboard claim; lesson 23 applies to a desk comparing two vendors' signals tuned by different teams.

Then the Level review and homework `set.audit.literature`.

### Course RP: Reporting and Pre-registration (`crs.reporting`, 2 levels, 9 lessons)

The learner's own evidence. Level RP1 writes and defends results so that a sceptic can check every claim: the note, the charts, the failures, the README and the defence. Level RP2 writes, before the data, the plan that makes the next note credible: a falsifiable hypothesis, a locked pre-registration with a decision rule, a test long enough to decide it, and a line between exploring and confirming. It ends with the exit's pre-registration for project 2. Spine: Arnott, Harvey and Markowitz (2019), the protocol's categories on research motivation, multiple testing and statistical methods, and research culture [research culture searched; the other names recalled: check]; Nosek and others (2018); Simmons, Nelson and Simonsohn (2011); Gelman and Loken (2014). It recaps 2.1 lesson 151 and 1.6 lesson 41.

**Level RP1: Writing and defending results** (`lvl.reporting.writing`, 5 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 24 | `lsn.reporting.results-note` The note a sceptic accepts | Write a one-page results note whose headline is the held-out net result with its uncertainty and trial count, with what failed and the limitations, every number matching the metrics file (from 2.3 lesson 37, building on 2.1 lesson 151) | Two notes on one backtest: one leads with "Sharpe 2.1"; the other with "0.8 after costs, 0.5 held out, deflated Sharpe 0.62 after 40 trials, one variant failed". Which earns the interview? (The second) | `results-note` (guided) | Trap: leading with the best in-sample number (`mc.research.lead-with-best-number`). Edge: a note longer than a page is a note nobody reads (`results-note` flags 500 words); a held-out figure worse than the in-sample one is normal and is reported as it is | O, M, C, S |
| 25 | `lsn.reporting.honest-charts` Honest charts for performance | Draw equity on a log scale with a drawdown panel, a benchmark, costs and the held-out boundary, and spot misleading choices (from 2.3 lesson 38) | A strategy doubles from 1 to 2 in its first ten years and from 2 to 4 in the next ten. On a linear scale, which decade looks better? (The second, though the growth rates are equal; on a log scale both rise by the same height) | `plot-2d` (log axis), `drawdown-lab` (compare) | Trap: linear scales for compounded wealth (`mc.research.linear-scale-for-wealth`). Edge: a start date chosen after a crash, a truncated axis and a gross-only line each mislead without a single wrong number | C, O, P, S |
| 26 | `lsn.reporting.negative-results` Reporting what failed | Write a failure section naming each failed variant, why it failed and what it rules out, keeping research failures apart from bugs (from 2.3 lesson 39) | "Momentum with a one-month skip failed after costs." Useful or embarrassing? (Useful: it bounds the cost at which the idea works) | `results-note`, `free-response` | Trap: vague failures such as "some variants underperformed" (`mc.research.vague-failures`). Edge: a failure caused by a bug is not a result: fix it, rerun and report the fix; failed variants count in the trial ledger | M, C, S, O |
| 27 | `lsn.reporting.readme-two-registers` The README in two registers | Write a README a layman can follow and an interviewer can probe line by line, every claim backed by a test, a benchmark or a document (from 2.3 lesson 40; project-forge Phase 3) | The README says "fast, accurate backtester". What does the interviewer ask next? (How fast, measured how; accurate against what) | `free-response`, `card-sort` | Trap: adjectives in place of evidence (`mc.research.adjectives-as-evidence`). Edge: a limitations section raises credibility; the "reproducing these results" section (one command, a pinned environment, a data manifest) is built in 2.3 level RM6 | S, M, S, O |
| 28 | `lsn.reporting.defence` Defending a result under questioning | Answer the standard follow-ups (what would make this wrong, how much was in sample, how many trials, costs, capacity, what failed) concisely and with numbers (from 2.3 lesson 41) | "Your Sharpe is 1.2. Why should I believe it?" | `viva`, `mock-interview` (project) | Trap: defending the number instead of the method (`mc.research.defend-the-number`). Edge: "I don't know, and here is how I would find out" scores better than a guess; naming the weakest point first is a strength | C, M, S, O |

Skills: `skl.research.write-a-results-note` (24), `skl.research.draw-honest-performance-charts` (25), `skl.research.report-negative-results` (26), `skl.research.write-a-two-register-readme` (27), `skl.research.defend-a-result` (28).

Transfer screens: lesson 24's note is an ML paper's results section with the seeds and the tuning budget in the first paragraph; lesson 28 is the project round of a quant interview and the question period of a lab's research review.

Then the Level review and homework `set.reporting.writing`.

**Level RP2: Pre-registration** (`lvl.reporting.preregistration`, 4 lessons)

| # | Lesson | Objective | Hook | Widgets | Trap and edge case | Quiz |
|---|---|---|---|---|---|---|
| 29 | `lsn.reporting.hypothesis-first` Hypothesis first: a mechanism and a falsifier | Write a falsifiable hypothesis with an economic mechanism (a risk premium, a behavioural bias, a structural constraint), a test and a result that would refute it, before seeing data (from 2.3 lesson 2) | "Shares that went up keep going up." Turn it into a claim that data could prove wrong | `token-tray` (hypothesis builder), `free-response` | Trap: writing the hypothesis after the backtest (`mc.research.hypothesis-after-results`). Edge: a claim with no mechanism can still be true but needs far more evidence (lessons 19 and 20); "it works in some markets" is not falsifiable until the markets are named | S, C, S, O |
| 30 | `lsn.reporting.preregistration` The pre-registration and the lock | Write a one-page pre-registration (hypothesis, data and universe, signal, metrics, held-out period, decision rule, allowed variants, trial budget) and lock it before the data is opened, so the app records the order (Nosek and others 2018; Arnott, Harvey and Markowitz 2019) | You lock a plan naming 2019 to 2024 as the held-out period, then find 2019 was unlike any year before it. What may you change, and how? (Nothing silently: a dated deviation note, with the locked analysis still reported) | `results-note` (pre-registration [mode to add]), `backtest-lab` (holdout lock) | Trap: a pre-registration forbids exploring (`mc.research.prereg-forbids-exploring`): exploration is allowed, labelled and kept off the held-out data. Edge: the lock records when the plan was fixed and when the data was first opened; a plan locked after the data was opened is a description, not a pre-registration | O, M, C, S |
| 31 | `lsn.reporting.power-before-data` How long must the test be? | Derive the years of data a one-sided test of a Sharpe ratio needs at a chosen power, $T \approx \left(\frac{z_{1-\alpha} + z_{1-\beta}}{SR}\right)^2$ years with $SR$ annual, and the power a planned held-out period actually has | A strategy you believe has annual Sharpe 0.5: how many years does a one-sided 5% test need for 80% power? (24.7.) What power does a 5-year held-out period give? (0.30) | `test-lab` (power curve), `sharpe-lab` (years), `slider` | Trap: a held-out period long enough to look at is long enough to test (`mc.research.short-holdout-is-a-test`). Edge: Sharpe 1.0 needs 6.2 years and 2.0 about 1.5; looking twice on the way (after 5 and 10 years) at 5% each time raises the false-positive rate to 8% (homework RP2 example B) | X, N, N, C, W |
| 32 | `lsn.reporting.exploration` Exploration, confirmation and forking paths | Keep exploratory and confirmatory analysis apart, count the forking paths an unplanned analysis takes, and keep a deviations log (Simmons, Nelson and Simonsohn 2011; Gelman and Loken 2014; recapping 1.6 lesson 41) | One noise data set, four analysis choices with two options each (outlier rule, control, subgroup, horizon): 16 analyses. How likely is at least one "significant" at 5%? (At most $1 - 0.95^{16} = 0.56$ if the 16 were independent; less, because they share data; the garden shows the rate for this data) | `multiple-testing` (garden [mode to add]), `node-link` | Trap: no fishing happened because only one analysis was run (`mc.stats.p-hacking-is-harmless`): the paths not taken were rejected after seeing the data. Edge: Simmons and others found four common flexibilities together pushed a nominal 5% to about 61% [recalled]; a deviations log keeps the confirmatory result honest without forbidding change | N, C, M, S |

Skills: `skl.research.state-a-falsifiable-hypothesis` (29), `skl.research.write-and-lock-a-preregistration` (30), `skl.research.size-a-test-before-data` (31), `skl.research.separate-exploration-from-confirmation` (32).

Transfer screens: lesson 30's plan is the exit's pre-registration for project 2, and the same lock keeps an ML lab's held-out evaluation set untouched until the final run; lesson 31's arithmetic sizes an A/B test of a desk tool or a model launch.

Then the Level review and homework `set.reporting.preregistration`, and the exit work (section 3.2).

### Coverage checks

**canon-gap G4's "Missing" list**, by where each is taught: stating a hypothesis before looking (29); pre-registration (30, the exit); data-snooping corrections: White's reality check (9), the deflated Sharpe ratio (7), the probability of backtest overfitting (8); survivorship (14), look-ahead (13) and point-in-time data (13, 14); corporate actions (15); how often published anomalies replicate (19 to 21, and 3.1 WS2 for the replication studies themselves); reproducible pipelines (2.3 level RM6, which stays in 2.3; 27 names the README section it builds); a results note a sceptic would accept (24 to 28).

**canon-gap G4's exit**: the five planted defects map to lessons 13 (look-ahead), 14 (survivorship), 15 (unadjusted splits), 17 (in-sample parameter choice) and 16 (missing costs); the pre-registration to 29 to 31; the deflated Sharpe ratio to 7 and the block-bootstrap interval to 3.

**Choice items** (C and M) per course, from the tables: IS 17 of 44; AU 18 of 48; RP 14 of 36 [counted; section 0.4].

---

## 3. Homework blueprint per level

### 3.0 Rules for every set

- **Issue, due and marking** follow `ASSESSMENT.md` 2.5: issued when the level's last lesson is done, due 7 days later, no feedback before submission; code items run their visible examples freely and their hidden tests at submission; long-form items are self-marked against the rubric with Bertie's suggested mark and evidence quote beside the learner's (`AI-TUTOR.md` 2.7).
- **Size and mix** (decision 16). **6 items**: 2 analysis items at difficulty 3, the code drill (difficulty 3 or 4), the long-form item (difficulty 4), 1 analysis item at difficulty 4 and 1 item at difficulty 5; about **130 minutes**. 2.2c: 6 sets, 36 items, 13.0 hours.
- **Inside every set:** exactly one long-form item (a derivation, a written audit or an explanation with a 10-point rubric) and exactly one code drill; 2 of the 6 items interleaved from earlier levels and topics, unlabelled, both "which tool?" problems (`ASSESSMENT.md` 2.5); at least half the items generator slots, so a redo is a fresh variant; at most one choice item. Analysis items run on a seeded `market-gen` panel whose true parameters the checker knows (decision 8).
- **Long-form marking.** Every rubric has 4 to 10 points totalling 10 marks, and each point names the model-answer lines that evidence it (`CONTENT-FORMAT.md` 3.4). 7 of 10 is the bar wherever an outcome cites a rubric.
- **Code drills run on the web app or the learner's machine** (decision 6). Each declares `needs` (`[]` for the standard library, `[numpy]` or `[numpy, pandas]` otherwise); in the Artifact its screen shows the handoff link with the drill id and seed and accepts the result code (`ASSESSMENT.md` 14.3). Hidden tests are listed here so CI can check that the reference passes and each known-wrong solution fails its named test (`CONTENT-FORMAT.md` 3.9). Floating-point answers use `zqtest`'s `isclose` with relative tolerance $10^{-9}$ unless a test states another; randomness uses `zq_rng` with a fixed seed; a test on a resampled quantity compares with the reference implementation within a band CI measures (decision 7). No drill may import a library that does the drill's task (`arch`'s bootstrap, `mlfinlab`): an import scan is a hidden test.
- **Generators** named per level are `gen.research.*` families with tidy answers by construction: Sharpe ratios whose per-period values give quantiles to three figures, trial counts and variances that keep the DSR away from 0.95 by at least 0.03 (so rounding never flips a verdict), price paths in whole pounds, and performance matrices with no ties in any in-sample winner or its out-of-sample rank.

Each level below gives its set id, long-form item, code drill with its hidden tests and known-wrong solutions, generators, and two example problems in full: **example A** is the long-form item with its model answer (numbered lines) and rubric; **example B** is the difficulty-5 item with its worked answer and its decision point.

### 3.1 The six sets

**IS1 How sure is one result?** (`set.inference.one-result`). Long-form: the variance of a dependent mean and the block bootstrap. Code drill `drl.research.stationary-bootstrap` (d4, `needs: [numpy]`): `sharpe_ci(returns, mean_block, n_boot, seed, periods=252, level=0.95)` returning the percentile interval of the annualised Sharpe ratio under the stationary bootstrap (Politis and Romano 1994): blocks start at uniform random days, have geometric lengths with mean `mean_block`, and wrap round the end. Hidden tests: the same seed returns the same interval; on a seeded IID normal fixture of 1,000 days the interval's width is within 15% of the delta-method width $2\times 1.96\sqrt{(1 + \frac12\widehat{SR}^2)/T}\sqrt{252}$ [simulated: ratios 0.93 to 1.03 over 20 seeds]; on a seeded AR(1) fixture with coefficient 0.4 the interval with `mean_block=20` is wider than with `mean_block=1` [simulated: ratios 1.16 to 1.70 over 20 seeds]; `mean_block=1` reproduces the ordinary bootstrap's distribution; `mean_block < 1` raises `ValueError`. Known-wrong: resampling single days whatever `mean_block` (passes the IID test, fails the AR(1) test with a ratio of exactly 1); blocks that stop at the series' end instead of wrapping (fails a test that every day is drawn equally often, within 4 standard errors over 200,000 draws). Generators: `gen.research.psr`, `gen.research.min-track-record`, `gen.research.lo-eta`, `gen.research.ar1-variance-factor`, `gen.research.empirical-p`, `gen.research.subperiod-chi2`.

- *Example A (long-form, d4).* Returns are $r_t = \mu + x_t$ with $x_t = \phi x_{t-1} + \varepsilon_t$ stationary. (a) Show that for large $T$, $\mathrm{Var}(\bar r) \approx \frac{\sigma_x^2}{T}\cdot\frac{1 + \phi}{1 - \phi}$. (b) Explain why a bootstrap that resamples single days understates the uncertainty of $\bar r$ and of the Sharpe ratio, and by what factor when $\phi = 0.4$. (c) Explain how the stationary bootstrap repairs this and what its mean block length trades off. (d) Say what you report.
  *Model answer.* (1) $\mathrm{Var}(\bar r) = \frac1{T^2}\sum_{s,t}\mathrm{Cov}(x_s, x_t) = \frac{\sigma_x^2}T\left[1 + 2\sum_{k=1}^{T-1}\left(1 - \frac kT\right)\rho_k\right]$. (2) For an AR(1), $\rho_k = \phi^k$; as $T\to\infty$ the bracket tends to $1 + 2\sum_{k\ge 1}\phi^k = 1 + \frac{2\phi}{1 - \phi} = \frac{1 + \phi}{1 - \phi}$. (3) Resampling single days draws them independently, so the bootstrap's variance of the mean is about $\frac{\sigma_x^2}T$: it reproduces the IID formula and loses the bracket. (4) For $\phi = 0.4$ the bracket is $\frac{1.4}{0.6} = 2.33$, so the standard error and the interval's width are too small by $\sqrt{2.33} = 1.53$. (5) The Sharpe ratio's numerator is the mean, so its interval is too narrow by about the same factor; volatility clustering adds dependence in the squares, which moves the denominator too. (6) The stationary bootstrap draws runs of consecutive days with geometric lengths of mean $b$, starting at random days and wrapping round the end, so dependence inside a run survives and the resampled series is itself stationary. (7) Short runs break the dependence (intervals too narrow); long runs leave few distinct runs (noisy intervals, biased in short samples); $b$ should cover the lags at which autocorrelation is material. (8) Report the interval, the method, $b$, and the interval at half and double $b$, so a reader sees it is not an artefact of one choice.
  *Rubric (10).* 2: the variance of the mean with the autocovariance sum (line 1). 2: the AR(1) limit (line 2), the creative step. 1: why single-day resampling gives the IID variance (line 3). 1: the factor 1.53 (line 4). 1: the Sharpe ratio (line 5). 2: the stationary bootstrap and its trade-off (lines 6, 7). 1: what is reported (line 8).
- *Example B (d5).* A monthly strategy has annual Sharpe 1.0 (monthly $\widehat{SR} = 0.2887$), skewness $-1.5$ and kurtosis 9. (a) Find the minimum track record for 95% one-sided confidence that the true Sharpe exceeds 0, and compare it with normal returns. (b) Find the PSR against 0 of a 5-year record. (c) Explain why the same skewness and kurtosis barely matter for a daily strategy with the same annual Sharpe.
  *Answer.* (a) $1 + \left[1 - \gamma_3\widehat{SR} + \frac{\gamma_4 - 1}4\widehat{SR}^2\right]\left(\frac{1.645}{\widehat{SR}}\right)^2 = 1 + [1 + 0.433 + 0.167]\times 32.47 = 52.9$ months, 4.4 years; for normal returns $1 + 1.042\times 32.47 = 34.8$ months, 2.9 years. (b) $T = 60$: $\Phi\left(\frac{0.2887\sqrt{59}}{\sqrt{1.600}}\right) = \Phi(1.75) = 0.960$; normal: $\Phi(2.17) = 0.985$. (c) Daily $\widehat{SR} = 0.063$: the skewness term is $1.5\times 0.063 = 0.09$ and the kurtosis term $2\times 0.063^2 = 0.008$, against 0.43 and 0.17 monthly. Decision point: the naive route plugs the annual 1.0 into the bracket and gets nonsense, or ignores the bracket and promises a monthly investor a 2.9-year wait that is really 4.4; the penalty scales with the per-period Sharpe ratio, so it is large exactly for low-frequency strategies.

**IS2 Many trials, one winner** (`set.inference.selection`). Long-form: a deflated Sharpe ratio, its inputs and a verdict. Code drill `drl.research.deflated-sharpe` (d4, `needs: []`, the standard library's `statistics.NormalDist`): `expected_max_sr(n_trials, var_trials)` and `dsr(sr, T, skew, kurt, n_trials, var_trials, units="per-period")`. Hidden tests: lesson 7's inputs (per-day Sharpe $1.5/\sqrt{252}$, $T = 1{,}008$, skewness $-0.5$, kurtosis 5, $N = 50$, $V = 0.25/252$) give 0.7592 within $10^{-3}$; `expected_max_sr(50, 1.0)` gives 2.2763 within $10^{-4}$; `n_trials=1` sets the hurdle to 0, so `dsr` equals the PSR against 0; the DSR falls strictly as `n_trials` goes 2, 10, 100, 1,000; any `units` other than `"per-period"` raises. Known-wrong: a hurdle without the Euler-Mascheroni term, $\sqrt V\,\Phi^{-1}(1 - \frac1N)$, gives 0.821 and fails test 1; annual inputs passed as per-period fail test 1 by a wide margin. Generators: `gen.research.trial-count`, `gen.research.expected-max`, `gen.research.dsr`, `gen.research.cscv-small`, `gen.research.bonferroni-hurdle`, `gen.research.pipeline-fpr`.

- *Example A (long-form, d4).* A colleague reports the best of 40 configurations of a trend rule: annual Sharpe 1.2 over 5 years of daily data, skewness $-0.3$, kurtosis 4. The 40 trials' annual Sharpe ratios have variance 0.16. (a) Find the expected maximum annual Sharpe of 40 unskilled trials. (b) Find the deflated Sharpe ratio. (c) Recompute it as if the colleague had reported 5 trials, and as if clustering showed 12 effective trials. (d) Explain why discarded trials count and why $V$ enters. (e) Give a verdict.
  *Model answer.* (1) $E[\max Z]\approx(1 - 0.5772)\Phi^{-1}(1 - \frac1{40}) + 0.5772\,\Phi^{-1}(1 - \frac1{40e}) = 2.19$. (2) The hurdle is $\sqrt V\times 2.19 = 0.4\times 2.19 = 0.88$ annual, $0.88/\sqrt{252} = 0.055$ per day. (3) Per day $\widehat{SR} = 1.2/\sqrt{252} = 0.0756$ and $T = 1{,}260$, so $\mathrm{DSR} = \Phi\left(\frac{(0.0756 - 0.0552)\sqrt{1259}}{\sqrt{1 + 0.3\times 0.0756 + \frac34\times 0.0756^2}}\right) = 0.76$. (4) With $N = 5$ the hurdle is 0.48 and the DSR 0.94; with $N = 12$ the hurdle is 0.67 and the DSR 0.88. (5) A trial looked at and dropped was selected against as surely as one run in full, so it raises the expected maximum; reporting 5 makes the result look nearly significant. (6) $V$ scales the hurdle because trials that vary widely produce a higher best by chance. (7) Clustering correlated trials lowers $N$ honestly; it is not a licence to count only the survivors. (8) Verdict: under any honest count the DSR is below 0.95; the result is suggestive and needs a held-out test, not a launch.
  *Rubric (10).* 1: the expected maximum (line 1). 1: the hurdle in both units (line 2). 2: the DSR with per-period inputs (line 3). 2: both recomputations (line 4). 1: discarded trials (line 5). 1: the role of $V$ (line 6). 1: clustering (line 7). 1: the verdict (line 8).
- *Example B (d5).* Four strategies' mean returns in four blocks (rows blocks, columns A, B, C, D): block 1: 0.9, 0.2, 0.3, 0.1; block 2: 0.7, 0.4, 0.1, 0.2; block 3: $-0.6$, 0.3, 0.4, 0.2; block 4: $-0.4$, 0.1, 0.5, 0.3. Compute PBO by CSCV and say what it means.
  *Answer.* Six ways to choose two blocks in sample. For each, the in-sample winner, its out-of-sample rank among four (1 worst), and $\lambda = \ln\frac{\omega}{1 - \omega}$ with $\omega = \frac{\text{rank}}5$: blocks $\{1, 2\}$: A, rank 1, $\lambda = -1.39$; $\{1, 3\}$: C, rank 4, $+1.39$; $\{1, 4\}$: C, rank 3, $+0.41$; $\{2, 3\}$: B, rank 1, $-1.39$; $\{2, 4\}$: C, rank 4, $+1.39$; $\{3, 4\}$: C, rank 2, $-0.41$. PBO is the share with $\lambda < 0$: $\frac36 = 0.5$. No split has a tie for its in-sample winner or at the winner's out-of-sample rank. Decision point: selecting by in-sample performance did no better than choosing at random; a single split on blocks 1 and 2 would have chosen A, the strategy that is worst out of sample.

**AU1 The backtest audit** (`set.audit.backtest`). Long-form: an audit finding. Code drill `drl.research.perturbation-test` (d3, `needs: [numpy, pandas]`): `reads_the_future(strategy, prices, t, n_draws=5, seed=0)` returning `True` if any position decided on or before index `t` changes when every price after `t` is multiplied by seeded lognormal noise, comparing positions exactly. Hidden tests: an expanding-mean rule returns `False` for every `t`; a full-sample-mean rule returns `True`; a centred 3-day window returns `True`; a rule built on `bfill()` of a gappy series returns `True` at a gap; a rule using `shift(-1)` returns `True`; `t` at the last index returns `False`. Known-wrong: perturbing from `t` inclusive (flags the expanding-mean rule and fails test 1). Generators: `gen.research.delisting-bias`, `gen.research.adjusted-return`, `gen.research.cost-drag`, `gen.research.best-of-n-lookbacks`, `gen.research.shapley-two`, `gen.research.perturb-count`.

- *Example A (long-form, d4).* A short-term reversal strategy (long the week's worst 10% of a large-cap universe, short the best 10%) is backtested on unadjusted closing prices. Over 5 years its short book held 12 shares through 2-for-1 splits, each at a weight of 1% of equity. Write the audit finding: (a) location and evidence; (b) mechanism and direction; (c) the effect on the annual return; (d) the fix and how to check it; (e) what else the defect may have touched.
  *Model answer.* (1) Location: the return calculation `close / close.shift(1) - 1` and the loader that reads raw closes. (2) Evidence: 12 one-day returns near $-50\%$ in short positions, each on a date in the split records. (3) Mechanism: a 2-for-1 split halves the price without changing value; on raw closes it shows as a $-50\%$ day, which a short position books as a gain of half its weight. (4) Direction: upwards, and not random: firms split after large rises, which is when a reversal rule shorts them, so the defect is correlated with the signal. (5) Effect: $12\times 0.5\% = 6\%$ of equity over 5 years, about 1.2 percentage points a year, before any trades the fake moves triggered. (6) Fix: returns from split-adjusted closes, or raw closes divided by the split factor on the ex-date; dividends as cash on the ex-date, and not also inside adjusted prices. (7) Check: rerun; the 12 days now show ordinary returns; a test asserts that no daily return below $-45\%$ coincides with a split record; a buy-and-hold of one splitting share matches the vendor's total-return series. (8) Related: the signal also saw the fake $-50\%$ moves, so entries on the day after each split are rechecked; any price filter on back-adjusted levels is checked too.
  *Rubric (10).* 1: location (line 1). 1: evidence (line 2). 2: mechanism (line 3). 2: direction, with the reason it correlates with the signal (line 4), the creative step. 1: effect (line 5). 2: fix and check (lines 6, 7). 1: related effects (line 8).
- *Example B (d5).* A backtest has three defects: look-ahead (L), survivorship (S) and missing costs (C). Its Sharpe ratio after fixing each set of defects is: none fixed 2.4; L 1.5; S 2.0; C 1.6; L and S 1.1; L and C 0.6; S and C 1.3; all three 0.2. (a) Give each defect's effect if it is fixed first. (b) Give each one's effect if it is fixed last. (c) Give each one's Shapley share. (d) Say what the report states.
  *Answer.* (a) Fixed first: L 0.9, S 0.4, C 0.8, summing to 2.1. (b) Fixed last: L $1.3 - 0.2 = 1.1$, S $0.6 - 0.2 = 0.4$, C $1.1 - 0.2 = 0.9$, summing to 2.4. (c) Averaging each defect's effect over the six orders of fixing: L $\frac{59}{60} = 0.98$, S $\frac{23}{60} = 0.38$, C $\frac56 = 0.83$, summing to exactly $2.4 - 0.2 = 2.2$. (d) The report gives the honest Sharpe ratio (0.2), the Shapley shares, and the note that L and C interact: each one's effect is larger once the other is fixed (L 1.0 after C against 0.9 first; C 0.9 after L against 0.8 first), so whichever is fixed first has its own effect understated. Decision point: no single order of fixing is the right one, and both one-order answers misstate the total; averaging over orders is the only split whose parts add up and treat the defects alike.

**AU2 What survives: the published record** (`set.audit.literature`). Long-form: a planning number for a newly published signal. Code drill `drl.research.significance-filter` (d3, `needs: []`): `filter_stats(true_effect, se, alpha=0.05, sided=1)` returning the power, the expected estimate given significance, the exaggeration ratio and, for `sided=2`, the probability of a wrong sign given significance. Hidden tests: lesson 20's case (0.3, $1/\sqrt5$) gives power 0.1650 and expected significant estimate 0.9728 within $10^{-4}$; a true effect of 0 gives power equal to `alpha` one-sided; a true effect of 10 standard errors gives a ratio within $10^{-3}$ of 1; `sided=2` with 0.1 and 0.447 gives a wrong-sign rate of 0.260 within $10^{-3}$; a non-positive `se` raises. Known-wrong: the two-sided critical value $1.96\,se$ in a one-sided test (fails test 1). Generators: `gen.research.ppv`, `gen.research.ppv-bias`, `gen.research.type-m`, `gen.research.haircut`, `gen.research.mcnemar`, `gen.research.budget-max`.

- *Example A (long-form, d4).* A paper reports a new long-short signal with annual Sharpe 0.9 over 10 years ($t = 2.85$). Suppose that in this literature 1 in 5 tested signals is real, a real signal's true annual Sharpe is 0.4, and tests are one-sided at 5%. (a) Find the test's power for a real signal and the share of significant signals that are real. (b) Find the average reported Sharpe of a real signal that passes. (c) Using the reported 0.9 itself, find the probability this signal is real and the Sharpe ratio to plan on. (d) Apply a 30% post-publication decay and say what you would do before trading it.
  *Model answer.* (1) The standard error is $1/\sqrt{10} = 0.316$ and the critical Sharpe $1.645\times 0.316 = 0.52$. (2) Power $= P(\mathcal N(0.4, 0.316^2) > 0.52) = 0.35$. (3) Share real among significant: $\frac{0.2\times 0.35}{0.2\times 0.35 + 0.8\times 0.05} = 0.64$. (4) A real signal that passes reports on average $0.4 + 0.316\frac{\phi(0.38)}{1 - \Phi(0.38)} = 0.73$: the filter alone nearly doubles it. (5) The estimate 0.9 is $\frac{\phi((0.9 - 0.4)/0.316)}{\phi(0.9/0.316)} = 16.4$ times as likely under a real signal as under noise, so the odds $\frac14$ become 4.1 and the probability real is 0.80. (6) Plan on $0.80\times 0.4 = 0.32$, about a third of the reported 0.9. (7) A 30% decay after publication leaves about 0.23. (8) Before trading: replicate it on data after the paper's sample, pre-registered (lesson 30), at a size that the held-out test's power can justify.
  *Rubric (10).* 1: standard error and critical value (line 1). 1: power (line 2). 1: the share real (line 3). 2: the filter's expected estimate (line 4). 2: the likelihood ratio and posterior (line 5), the creative step. 1: the planning number (line 6). 1: decay (line 7). 1: what to do (line 8).
- *Example B (d5).* Ioannidis's positive predictive value with pre-study odds $R$, power $1 - \beta$, level $\alpha$ and bias $u$ is $\frac{(1 - \beta)R + u\beta R}{R + \alpha - \beta R + u - u\alpha + u\beta R}$. With $R = 0.1$ and $\alpha = 0.05$: (a) find the PPV at power 0.5 with no bias and with $u = 0.2$; (b) which helps more from there, raising power to 0.8 or halving the bias to 0.1?
  *Answer.* (a) No bias: $\frac{0.05}{0.1 + 0.05 - 0.05} = 0.50$. With $u = 0.2$: $\frac{0.05 + 0.01}{0.1 + 0.05 - 0.05 + 0.2 - 0.01 + 0.01} = \frac{0.06}{0.30} = 0.20$. (b) Power 0.8 with $u = 0.2$: 0.26; power 0.5 with $u = 0.1$: 0.275. Halving the bias helps slightly more, and costs no data. Decision point: the naive fix for unreliable findings is bigger samples; when analyses are reported selectively, cutting the selection (pre-registration, a full trial ledger) does as much for less.

**RP1 Writing and defending results** (`set.reporting.writing`). Long-form: a results note from a metrics file; its rubric is the results-note rubric every later note is marked against. Code drill `drl.research.note-consistency` (d3, `needs: []`): `check_note(text, metrics, rel_tol=0.01)` returning each number in the text that matches no metric, or matches one only outside the tolerance; percentages compare with fractions ("12%" with 0.12); years and dates are ignored. Hidden tests: a note with two planted mismatches returns exactly those two; "12%" matches 0.12; "2019" is not flagged; an empty note returns no findings; a number matching two metrics is not flagged. Known-wrong: exact string matching flags "0.86" against 0.8612 and fails the tolerance test. Generators: `gen.research.log-scale-height`, `gen.research.note-mismatch`, plus interleaved slots from `gen.research.dsr` and `gen.research.cost-drag`.

- *Example A (long-form, d4).* From this metrics file, write the one-page results note. Short-term reversal in European large caps; gross Sharpe 1.4; net 0.7 at 4 basis points per side; held-out period 2019 to 2024, net Sharpe 0.4 with a 95% stationary-bootstrap interval from $-0.5$ to 1.3 (mean block 10 days); 28 trials logged, 9 effective after clustering; DSR 0.41; break-even cost 7 basis points; maximum drawdown 18%; failed: the value-weighted version (net Sharpe 0.1) and the 10-day window (net $-0.2$).
  *Model answer.* (1) Question: does one-week reversal earn a premium in European large caps after costs? (2) Data: a point-in-time universe with delistings, its source and dates, the held-out period 2019 to 2024 named in a pre-registration and opened once. (3) Method: the signal, deciles, weekly rebalancing, costs at 4 basis points per side, 28 trials (9 effective). (4) Headline: held-out net Sharpe 0.4, interval $-0.5$ to 1.3; in-sample net 0.7, gross 1.4. (5) Verdict: the DSR is 0.41 after 28 trials, and the held-out interval includes 0, so the evidence does not support the effect. (6) Failures: value-weighting cut the net Sharpe to 0.1, which suggests the effect lives in the smaller names; the 10-day window lost money. (7) Costs and capacity: break-even 7 basis points against an assumed 4, so a small rise in costs removes the result; drawdown 18%. (8) Limitations and next steps: one region, assumed costs; measure costs from quote data and test the effect in the smallest third separately, pre-registered.
  *Rubric (10).* 1: question (line 1). 1: data and the held-out period (line 2). 1: method with both trial counts (line 3). 2: the held-out net result first, with its interval (line 4). 2: an honest verdict from the DSR and the interval (line 5). 2: failures, specifically, with what they rule out (line 6). 1: costs, capacity, limitations and next steps (lines 7, 8).
- *Example B (d5).* Find six problems in this note and say which number would fix each: "Our machine-learning strategy delivers a Sharpe ratio of 2.6 (2010 to 2024) with 74% accuracy. We tuned the model carefully. Drawdowns were minimal (see chart). It has zero correlation with the market. The approach is ready for production."
  *Answer.* (1) A Sharpe of 2.6 for a daily equity model is a bug until shown otherwise: give the held-out figure and the trial count (lessons 7, 12). (2) 74% accuracy against what base rate? In a rising market most days go up: give the base rate and a calibrated score. (3) "Tuned carefully": on which data? Give the tuning budget and the walk-forward or held-out result (lesson 17). (4) "Minimal drawdowns (see chart)": give the maximum drawdown and its dates, on a log scale (lesson 25). (5) "Zero correlation with the market": give the beta and factor regression with standard errors. (6) "Ready for production": give costs, turnover, break-even cost and capacity (lesson 16). Also missing: uncertainty and failures. Decision point: every sentence makes a claim without the number that would test it; the fix is to replace each adjective with the statistic it stands for, not to soften the adjectives.

**RP2 Pre-registration** (`set.reporting.preregistration`). Long-form: a pre-registration; its rubric is the exit's pre-registration rubric (section 3.2.3). Code drill `drl.research.test-length` (d3, `needs: []`): `years_needed(sr_annual, alpha=0.05, power=0.8, periods=252, skew=0, kurt=3)` from the per-period PSR formula, $T = 1 + \left[1 - \gamma_3 SR + \frac{\gamma_4 - 1}4 SR^2\right]\left(\frac{z_{1-\alpha} + z_{1-\beta}}{SR}\right)^2$ periods with $SR$ per period (lesson 1's minimum track record with the power term added; the leading 1 is the PSR's $T - 1$), divided by `periods`; and `power_of(years, sr_annual, alpha=0.05, periods=252, skew=0, kurt=3)`, $\Phi\left(\frac{SR\sqrt{T - 1}}{\sqrt{1 - \gamma_3 SR + \frac{\gamma_4 - 1}4 SR^2}} - z_{1-\alpha}\right)$. Hidden tests: `years_needed(0.5)` gives 24.75 within 0.01; `power_of(5, 0.5)` gives 0.299 within $10^{-3}$; `years_needed(1.0)` gives 6.20 within 0.01; monthly (`periods=12`) with skewness $-1.5$ and kurtosis 9 needs 9.97 years against 6.52 for normal monthly returns, within 0.01; `power_of(5, 0)` equals `alpha`. Known-wrong: the two-sided critical value (31.4 years; fails test 1); dropping the leading 1 passes the daily tests and fails the monthly one (9.89 and 6.44 years). Generators: `gen.research.power-years`, `gen.research.power-of-holdout`, `gen.research.two-looks`, `gen.research.garden-count`.

- *Example A (long-form, d4).* Write a one-page pre-registration for "post-earnings-announcement drift in European large caps", with the held-out period's power stated.
  *Model answer.* (1) Hypothesis and mechanism: shares with large positive earnings surprises outperform those with large negative surprises over the next 60 trading days, because investors under-react to earnings news. (2) Falsifier: a held-out long-short spread whose one-sided test fails at 5% after costs, or a spread confined to the most expensive decile to trade. (3) Universe and data: the largest 600 European shares on each date from point-in-time membership, delisted names with their delisting returns, announcement dates and consensus estimates as first reported, sources and licences named, raw downloads cached with a hash manifest. (4) Signal and timing: the standardised unexpected earnings, entered at the open of the second trading day after the announcement (the first day the information is surely public). (5) Portfolio and costs: terciles, value-weighted, held 60 days, costs at 3, 6 and 10 basis points per side. (6) Metrics: mean spread with Newey-West $t$, net Sharpe at each cost, the trial ledger and DSR, a stationary-bootstrap interval with its block length. (7) Periods: training 2005 to 2016; held-out 2017 to 2024, opened once, after this plan is locked. (8) Power: at a believed annual Sharpe of 0.6, 8 held-out years give power $\Phi(0.6\sqrt8 - 1.645) = 0.52$; stated, so a null result is read as weak evidence, not a refutation. (9) Decision rule: report the held-out result whatever it is; call the hypothesis supported only if the held-out net Sharpe at 6 basis points passes the one-sided 5% test. (10) Variants and budget: 40-day and 90-day holds and equal weights, declared now; anything else is a logged new trial; deviations go in a dated log.
  *Rubric (10)*, the pre-registration rubric of section 3.2.3: 2: hypothesis with a mechanism and a falsifier (lines 1, 2). 1: point-in-time universe and data (line 3). 1: the exact signal and timing, with the reason for the entry day (line 4). 1: metrics with costs, ledger, DSR and interval (lines 5, 6). 2: the held-out period fixed in advance and the decision rule (lines 7, 9). 1: the power stated (line 8). 1: the variants and the trial budget (line 10). 1: the deviations log and the promise to report the result whatever it is (lines 9, 10).
- *Example B (d5).* A researcher plans to test a strategy after 5 years and again after 10, each time rejecting "no edge" if the one-sided $z$ exceeds 1.645. (a) Under the null, what is the chance of a false rejection at either look? ($z_5$ and $z_{10}$ have correlation $\sqrt{5/10}$.) (b) What common boundary at both looks restores 5% overall? (c) At a true annual Sharpe of 0.5, compare the power of the two-look design at that boundary with a single test at 10 years.
  *Answer.* (a) $1 - P(z_5\le 1.645, z_{10}\le 1.645)$ with correlation 0.707 is 0.080, by the bivariate normal distribution. (b) 1.875. (c) The $z$ means are $0.5\sqrt5 = 1.12$ and $0.5\sqrt{10} = 1.58$; the two-look power is 0.43, the single look's $\Phi(1.58 - 1.645) = 0.47$. Decision point: looking twice is allowed when it is planned and paid for with a higher boundary; looking twice at the same 1.645 is optional stopping and quietly raises the false-positive rate by 60%.

### 3.2 The exit work (4.5 hours)

#### 3.2.1 The audit (`itm.audit.exit-findings`, 2.0 hours, both targets)

**The fixture.** A supplied research repository, read-only in `bias-audit` (exit mode) through its embedded `code-review`: a README, a 300-line Python backtest in five modules, a data dictionary, a metrics file and a one-page results note claiming an annual Sharpe of 1.9 for a weekly cross-sectional reversal strategy on a synthetic universe of 400 shares over 12 years from `market-gen`, with delistings, splits and dividends planted. Five defects are planted, one per class: **look-ahead** (the signal is $z$-scored with each share's full-sample mean and standard deviation), **survivorship** (the universe keeps only names alive on the last date), **unadjusted splits** (returns from raw closes), **in-sample parameter choice** (the look-back is the best of 30 on the full period and no held-out section exists; the note says "a 7-day look-back performed best") and **missing costs** (turnover of 35% a day with costs set to zero; the note says "costs are negligible"). Two decoys look suspicious and are correct: a `shift(1)` before trading, and dividends handled through a total-return series. CI computes the strategy's Sharpe ratio under every one of the $2^5 = 32$ combinations of fixed defects and stores them in the fixture.

**The task.** For each finding the learner taps its location (a line range, a data field or a note sentence), chooses its class from the audit taxonomy, and may add evidence and an effect estimate in words. Bertie is away.

**Marking (10 marks, automatic).** For each planted defect: 1 mark for a location inside the defect's marked span, 1 for the right class. Each finding that matches no planted defect costs 1 mark (a decoy flagged is a false finding), with the total floored at 0. **Bar: 8 of 10** (four defects found and placed with no false finding, or all five with up to two). Effect estimates are not marked; after submission the widget shows each defect's true effect and its Shapley share beside the learner's estimate.

#### 3.2.2 The honest-Sharpe drill (`drl.research.exit-honest-sharpe`, 1.0 hour, web app)

After the audit is submitted, the learner receives the corrected strategy's daily returns (the fixture with all five defects fixed) and its trial ledger (35 trials: the 30 look-backs and 5 signal variants, each with its annual Sharpe ratio). `honest_sharpe(returns, ledger_sharpes, mean_block=10, n_boot=5000, seed)` returns the annual Sharpe ratio, the deflated Sharpe ratio with $N$ and $V$ from the ledger, and a stationary-bootstrap 95% interval. Hidden tests: the Sharpe ratio, skewness and kurtosis match the reference to $10^{-9}$; the DSR matches the reference to $10^{-6}$ (it is a deterministic formula); each interval endpoint lies within 0.10 of the reference's at 5,000 resamples (the band is 4 seed-to-seed standard deviations, about 0.024 each [simulated, rechecked in CI on the fixture]); the same seed reproduces the interval; inputs in annual units raise. Runs on the web app or locally; in the Artifact the screen hands off and accepts the result code.

#### 3.2.3 The pre-registration (`itm.reporting.exit-prereg`, 1.5 hours, both targets)

Written in `results-note` pre-registration mode for 2.3's project 2 (alpha research), or, on a plan without it, for the first 2.3 project that tests a trading hypothesis (open item 8). Self-marked against the rubric below, then shown Bertie's suggested mark and evidence quotes (`AI-TUTOR.md` 2.7); the confirmed mark must reach 7 of 10. **Locking** fixes the text, records the time, and is allowed only before the project's data-download milestone is recorded (`setup-checklist` project mode); the project's `prereg-before-data` predicate checks the order later (section 4.4).

**The pre-registration rubric (10)**, used here, in homework RP2 and in every later project's plan: 2: a hypothesis with a mechanism and a falsifier; 1: a point-in-time universe and data with sources and licences; 1: the exact signal and its timing, with the reason for the entry time; 1: metrics including costs, the trial ledger, the DSR and a block-bootstrap interval; 2: the held-out period fixed in advance, opened once, and a decision rule stated before the data; 1: the held-out period's power at the believed effect; 1: the variants allowed and the trial budget; 1: a deviations log and what will be reported whatever the result.

---

## 4. Topic exam blueprint and the 2.2c exit test

### 4.1 `exm.research`: 2.2c Research method and statistical honesty

| Field | Value |
|---|---|
| Kind | `topic` (`ASSESSMENT.md` 3.1): timed, one sitting, no hints, Bertie away app-wide (`AI-TUTOR.md` 2.12), resits after the cool-down of `ASSESSMENT.md` 3.8 |
| Duration | 75 minutes (1.5 times the summed item estimates of 50 minutes) |
| Items | 14 |
| Marks | 60; pass 42 (70%) |
| Difficulty by marks | d2 12 (20%), d3 30 (50%), d4 12 (20%), d5 6 (10%) |
| Long-form | Q12 to Q14, 24 marks (40%, the kind's target) |
| Choice items | none; Q6 is a match (S), 3 marks |
| Exit slot | `slotMin: { q14: 0.7 }` |
| Aids | A formula card (the PSR and minimum track record, the expected maximum with the Euler-Mascheroni term, the DSR, Lo's $\eta(q)$, the PPV, the test length) and the in-app scientific calculator with $\Phi$ and $\Phi^{-1}$ (open item 6) [our choice: the paper tests use and judgement, not recall of constants]. No code runs |
| Forms | At least 3, equal marks; each form's difficulty mix within 5 percentage points; 33 of 60 marks (55%) from generator slots; each long-form pool holds 6 versions; slot order shuffled per sitting, two unlabelled slots per form drawn from the whole topic at difficulty 3 to 4, and no stem names its method (`ASSESSMENT.md` 3.2) |
| Practice | One practice paper of the same shape from the practice pool, never the exam reserve |
| Runs on | Both targets: no item needs Python |

| Slot | Skills | Format | Marks | Difficulty | Source | Minutes |
|---|---|---|---|---|---|---|
| Q1 | The PSR against a benchmark, or a minimum track record | N | 3 | 2 | `gen.research.psr`, `gen.research.min-track-record` | 2 |
| Q2 | An empirical $p$-value from a matched null | N | 3 | 2 | `gen.research.empirical-p` | 2 |
| Q3 | A split-adjusted return, or a dividend counted twice | N | 3 | 2 | `gen.research.adjusted-return` | 2 |
| Q4 | The share of discoveries that are true | N | 3 | 2 | `gen.research.ppv` | 2 |
| Q5 | Lo's $\eta(q)$, or the AR(1) factor for a bootstrap interval | N | 3 | 3 | `gen.research.lo-eta`, `gen.research.ar1-variance-factor` | 2 |
| Q6 | Match five symptoms to the defects that cause them | S | 3 | 3 | pool `itm.audit.symptom-match` | 2 |
| Q7 | A deflated Sharpe ratio | N | 3 | 4 | `gen.research.dsr` | 3 |
| Q8 | PBO from a small performance matrix | N | 3 | 4 | `gen.research.cscv-small` | 3 |
| Q9 | A cost drag, net Sharpe and break-even cost | N | 3 | 4 | `gen.research.cost-drag` | 3 |
| Q10 | The Shapley split of two interacting defects | N | 3 | 4 | `gen.research.shapley-two` | 3 |
| Q11 | The significance filter (power and the expected significant estimate), or a test length and a held-out period's power | N (two parts) | 6 | 5 | `gen.research.type-m`, `gen.research.power-years` | 6 |
| Q12 | **Audit a described backtest** | long-form (written) | 8 | 3 | pool `itm.audit.exam-audit` (6 versions) | 7 |
| Q13 | **Deflate a reported result and explain why every trial counts** | long-form (derivation and explanation) | 8 | 3 | pool `itm.inference.exam-dsr` (6 versions) | 7 |
| Q14 | **Exit slot: critique a results note and write the verdict a sceptic accepts** | long-form (written) | 8 | 3 | pool `itm.reporting.exam-verdict` (6 versions) | 6 |

**Totals.** Marks $3\times 10 + 6 + 3\times 8 = 60$. By difficulty: d2 $3\times 4 = 12$; d3 $3 + 3 + 24 = 30$; d4 $3\times 4 = 12$; d5 6. Generator slots carry 33 marks (all but Q6 and the three long-form pools). Minutes $2\times 6 + 3\times 4 + 6 + 7 + 7 + 6 = 50$. Coverage: every form covers all six levels: IS1 through Q1, Q2 and Q5; IS2 through Q7, Q8 and Q13; AU1 through Q3, Q6, Q9, Q10 and Q12; AU2 through Q4 and Q11's first variant; RP1 through Q14; RP2 through Q11's second variant on rotating forms, and for every learner through homework RP2 and the exit pre-registration. Applied items with a named trap or edge case (Q3, Q6, Q9, Q10, Q12 to Q14) carry 36 marks, 60%, above the kind's 30%.

### 4.2 The three long-form slots in full (specimen versions)

**Q12 (specimen): audit a described backtest.** "A backtest buys, each January from 2000 to 2024, the 20 shares with the lowest price-to-book ratio among today's S&P 500 members, using book value from fiscal years ending the previous December and the vendor's adjusted closing prices. It reports an annual Sharpe ratio of 1.3 with no costs. The author says a few value definitions were tried. Name four defects, the direction each pushes the result, the test that would confirm each, and the fix."

*Model answer.* (1) Survivorship and today's facts: today's members exclude names that fell out of the index and include names that joined after rising, so the result is pushed up; confirm by counting members by date against a point-in-time list; fix with point-in-time membership and delisting returns. (2) Look-ahead in accounts: December fiscal-year accounts are published around February or March, so a January decision cannot know them; the result is likely pushed up if the signal works; confirm by perturbing book values before their release dates (or by checking release dates); fix by using each figure from its release date, as first reported. (3) Selection: "a few" definitions is a trial count of unknown size; the result is pushed up by the expected maximum; confirm by asking for the ledger; fix by reporting the DSR with every definition counted, and a held-out period. (4) Costs: an annual rebalance of 20 names has modest turnover, so the push is upwards but small; confirm with turnover and a break-even cost; fix by charging costs. (5) Price data: adjusted closes are right for returns; if dividends were also added as cash, the yield is counted twice; confirm by comparing a buy-and-hold with a total-return index. (6) Ranked by likely size: survivorship and the accounting look-ahead first, selection next, costs last, because an annual rebalance of 20 names trades little.
*Rubric (10).* For each of four defects (lines 1 to 5, any four), 2: 1 for the defect with its direction, 1 for a test and a fix. 2: the ranking with its reason (line 6). Common losses: "survivorship" named without saying which way it pushes; costs called the largest problem in an annual strategy; no test proposed for the accounting dates.

**Q13 (specimen): deflate a result and explain why every trial counts.** "The best of 25 trials has annual Sharpe 0.9 over 6 years of daily data, with normal returns; the trials' annual Sharpe ratios have standard deviation 0.4. (a) Compute the expected maximum of 25 unskilled trials and the hurdle. (b) Compute the DSR and the PSR against 0. (c) Explain why trials dropped early still count and why the trials' spread enters. (d) Give the verdict."

*Model answer.* (1) $E[\max Z]\approx(1 - 0.5772)\Phi^{-1}(0.96) + 0.5772\,\Phi^{-1}(1 - \frac1{25e}) = 2.00$. (2) Hurdle $0.4\times 2.00 = 0.80$ annual, $0.050$ per day. (3) $\widehat{SR} = 0.9/\sqrt{252} = 0.0567$ per day, $T = 1{,}512$. (4) $\mathrm{DSR} = \Phi\left(\frac{(0.0567 - 0.0503)\sqrt{1511}}{\sqrt{1 + \frac12\times 0.0567^2}}\right) = \Phi(0.25) = 0.60$; the PSR against 0 is 0.986. (5) A dropped trial was selected against as surely as a finished one: it raised the best result's expected value, so leaving it out lowers the hurdle. (6) The spread scales the hurdle: the more the trials differ, the higher the best one lands by chance. (7) Verdict: 0.60 is far below 0.95; the PSR's 0.986 answers a different question (is one pre-specified strategy positive?), not the one asked of a winner.
*Rubric (10).* 2: the expected maximum (line 1). 1: the hurdle in both units (line 2). 3: the DSR with per-period inputs, and the PSR (lines 3, 4). 1: dropped trials (line 5). 1: the spread (line 6). 2: the verdict, with why the PSR is the wrong number here (line 7). Common losses: annual Sharpe ratios inside the formula; the PSR reported as the answer.

**Q14 (specimen, exit slot): critique a results note.** "A note reads: 'Our pairs strategy earned an annual Sharpe of 1.7 from 2012 to 2024 (t = 5.9). Hedge ratios were estimated by regression on each pair's full history. We report the best 20 of 300 pairs screened. Costs of 1 basis point per side are included. Returns were positive in 11 of 13 years.' Write the three most serious problems with their likely effect, then write the two-sentence verdict a sceptic would accept, stating what evidence would change it."

*Model answer.* (1) Look-ahead: hedge ratios fitted on each pair's full history use the future, the defect of 2.2 lesson 42; the in-sample spread is mean-reverting by construction, so the Sharpe ratio is pushed up, possibly most of it. (2) Selection: the best 20 of 300 pairs were chosen on the same data, so the reported Sharpe ratio is near the expected maximum of many trials; the $t$ of 5.9 ignores 300 trials and the overlap of pairs. (3) Costs: 1 basis point per side on two legs of frequent trades is below what most pairs cost, and short borrow is not mentioned. (4) "11 of 13 years positive" adds little: years are not independent trials of a selected strategy. (5) Verdict: "As reported, the result cannot be told apart from selection and look-ahead; it is no evidence of a tradable edge. It would become evidence if hedge ratios estimated on a formation window only, applied to all 300 pairs with realistic costs, produced a positive held-out Sharpe with a deflated Sharpe ratio above 0.95."
*Rubric (10).* 3: look-ahead in the hedge ratio, with its direction (line 1). 3: selection, with why the $t$ is wrong (line 2). 1: costs and borrow (line 3). 1: why the year count adds little (line 4). 2: a two-sentence verdict that is calibrated and names the evidence that would change it (line 5). Common losses: a verdict that softens adjectives instead of naming the test; selection described without the number of pairs.

### 4.3 The 2.2c exit, rebuilt in the app

Proposed curriculum line (decision 15; `docs/curriculum.md` has none yet), from canon-gap G4's exit: **"Audit a supplied backtest with five planted defects (look-ahead, survivorship, unadjusted splits, in-sample parameter choice, missing costs) and find at least four; write a one-page pre-registration for project 2 before touching its data; report a deflated Sharpe ratio and a block-bootstrap interval for a strategy's Sharpe ratio."** Canon-gap wrote "for the project's Sharpe"; the project is built in 2.3, after this item closes, so the exit reports them for the audited strategy once its defects are fixed, and the P1 checklist (section 4.4) requires them of the project's own note.

| Curriculum phrase | Instrument | Bar |
|---|---|---|
| "Audit a supplied backtest with five planted defects and find at least four" | `itm.audit.exit-findings` (section 3.2.1) | 8 of 10 (four found and placed with no false finding) |
| "write a one-page pre-registration for project 2 before touching its data" | `itm.reporting.exit-prereg` (section 3.2.3), locked before the project's data milestone | 7 of 10, and locked |
| "report a deflated Sharpe ratio and a block-bootstrap interval" | `drl.research.exit-honest-sharpe` (section 3.2.2) | Every hidden test passes |
| (topic closure) | `exm.research` | 70%, with Q14 at 7 of 10 in some sitting or an `exit-item` sitting of the slot |

```yaml
# exit part data (ASSESSMENT.md 2.10 schema)
id: 2.2c.exit
text: Audit a supplied backtest with five planted defects and find at least four; write a one-page pre-registration for project 2 before touching its data; report a deflated Sharpe ratio and a block-bootstrap interval for a strategy's Sharpe ratio
gate:
  - { kind: exam, exam: exm.research, pass: 0.7, slotMin: { q14: 0.7 } }
  - { kind: rubric, items: [itm.audit.exit-findings], minPoints: 8 }    # auto-marked out of 10 (open item 3)
  - { kind: rubric, items: [itm.reporting.exit-prereg], minPoints: 7 }  # self-marked, Bertie's suggestion beside it
  - { kind: drill, drills: [drl.research.exit-honest-sharpe] }
confirm: []
estHours: 5.75       # exit work 4.5, exm.research 1.25
```

**Runs on:** the paper, the audit and the pre-registration on both targets; the drill on the web app (Pyodide) or the learner's machine (CPython 3.12), returning to the Artifact by result code (decision 6). **Order and test-out:** a learner may sit `exm.research` and do the audit and the drill before the lessons (`ASSESSMENT.md` 7.3); passing them with the pre-registration credits the item's lesson hours as tested out. The pre-registration cannot be tested out: it is written for the learner's own next project.

### 4.4 The P1 checklist for later results notes

Canon-gap 4.4's Stage 2 exit change ("each note passes the P1 checklist") becomes four `results-note` predicates, added to the `project` instruments of `2.3.exit` and `3.1.exit` through `notePredicates` (`ASSESSMENT.md` 2.10), for every project whose note reports a strategy's Sharpe ratio: kinds `backtest` (its strategy-evaluation section), `alpha`, `bot` and `replication` [our choice; `options` and `market-data` notes are exempt because they test no trading hypothesis].

| Predicate | Passes when |
|---|---|
| `prereg-before-data` | The note links a locked pre-registration whose lock time precedes the project's first data-download milestone, and lists every deviation with its date |
| `bias-audit-section` | The note has an audit section naming, for each of the five defect classes of level AU1, the check that was run and its result |
| `deflated-sharpe` | The note reports the trial count, the effective count and the deflated Sharpe ratio, matching the project's run records within `metrics-consistent`'s tolerance |
| `bootstrap-interval` | The note reports a block-bootstrap interval for the headline Sharpe ratio with its mean block length, matching the metrics file |

On the developer track, projects 1 and 4 built before 2.2c keep 2.3's original predicates (decision 5); the checklist applies from the alpha project on.

---

## 5. Reading and resource map per level

### 5.0 How to use this map

- **One primary resource** (curriculum rule 1): AFML chapters 11 to 14 are the spine, Arnott, Harvey and Markowitz (2019) the checklist; each level's papers are read **by section**, not cover to cover, and only the sections named.
- **Read after the level's lessons, before its homework.** The lessons give the picture and the trap; the papers give the original argument and its evidence.
- **No lecture column.** No university programme teaches research method as a named course (canon-gap 2.2, point 9); the reading pack replaces lectures, and no talk is assigned.
- **Problems over reading** (rule 2). No public problem set with solutions exists for this topic (canon-gap's solutions table: "None: the app's audit exercises are its own"). AFML's end-of-chapter exercises for chapters 11 and 14 are `problem-inspired` sources (no official solutions found by search [check]); the app writes and verifies every exercise it grades (`CONTENT-FORMAT.md` decision 7).
- **Citation roles** follow canon-gap 0.4: spine `basis`, checklist and papers `parallel-reading`, AFML's exercises `problem-inspired`, stretch `further`. Every work here is under copyright: cited and linked, never adapted (`CONTENT-FORMAT.md` 9.4).
- **Section numbers** for AFML (2018 edition): 11.1 to 11.6 and 14.7.1 to 14.7.4 confirmed by search on 7 October 2026 [searched]; chapter 13's numbers and the seven sins' place in chapter 11 remain [check]; papers' sections are named by their content where the numbering is uncertain.
- **Companion hours per level** (section 1.4's 4.25 h): IS1 0.75, IS2 1.0, AU1 0.75, AU2 1.0, RP1 0.25, RP2 0.5.

**Links** (free unless stated). López de Prado, *Advances in Financial Machine Learning* (Wiley 2018, paid; the learner owns it from 2.1). Arnott, Harvey and Markowitz, "A Backtesting Protocol in the Era of Machine Learning", SSRN abstract 3275654 [searched]. Ioannidis (2005), PLoS Medicine, open access [recalled]. Recht, Roelofs, Schmidt and Shankar (2019), arXiv 1902.10811 [recalled]. Henderson and others (2018), AAAI 2018, arXiv 1709.06560 [searched]. Dodge and others (2019), arXiv 1909.03004 [recalled]. Kapoor and Narayanan (2023), Patterns 4(9), article 100804, open access, and arXiv 2207.07048 [searched]. Pineau and others (2021), JMLR 22(164), free at jmlr.org/papers/v22/20-303.html and as arXiv 2003.12206 [searched]. Bouthillier and others (2021), MLSys 2021, arXiv 2103.03098 [searched]. Nosek, Ebersole, DeHaven and Mellor (2018), PNAS, open access [recalled]. Gelman and Loken (2014), American Scientist, free on the magazine's site [recalled]. Reinhart, *Statistics Done Wrong* (No Starch 2015, 12 chapters [searched]; a free online version at statisticsdonewrong.com [recalled]). The finance journal papers (Lo 2002; Bailey and López de Prado 2012, 2014; Bailey and others 2014, 2017; White 2000; Harvey, Liu and Zhu 2016; McLean and Pontiff 2016) are paid in their journals and most have SSRN versions [check per paper].

### 5.1 Course IS: Is It Real? Inference and Selection

AFML section numbers in this table: 14.7.1 to 14.7.3 and 11.6 [searched]; chapter 13's [check].

| Level | Spine (AFML) | Papers (by section) | Problems | Stretch |
|---|---|---|---|---|
| IS1 | Chapter 14, the efficiency statistics: the Sharpe ratio and the probabilistic Sharpe ratio (14.7.1, 14.7.2) | Lo, "The Statistics of Sharpe Ratios" (FAJ 58(4), 2002), whole: the standard error under IID and dependent returns, and $\eta(q)$; Bailey and López de Prado, "The Sharpe Ratio Efficient Frontier" (Journal of Risk 15(2), 3 to 44, 2012) [searched], the sections defining the PSR and the minimum track record length | AFML chapter 14's exercises on the Sharpe ratio and the PSR (problem-inspired); homework IS1 | Politis and Romano, "The Stationary Bootstrap" (JASA 89, 1994) sections 1 and 2; Getmansky, Lo and Makarov, "An Econometric Model of Serial Correlation and Illiquidity in Hedge Fund Returns" (JFE 74(3), 2004) [recalled], the introduction and the smoothing model |
| IS2 | Chapter 14, the deflated Sharpe ratio (14.7.3); chapter 11, strategy selection by CSCV (11.6) [searched]; chapter 13's opening sections on backtesting on synthetic data [check] | Bailey and López de Prado, "The Deflated Sharpe Ratio" (JPM 40(5), 94 to 107, 2014) [searched], sections 1 to 3; Bailey, Borwein, López de Prado and Zhu, "The Probability of Backtest Overfitting" (Journal of Computational Finance 20(4), 2017) [searched], the CSCV procedure; the same authors' "Pseudo-Mathematics and Financial Charlatanism" (Notices of the AMS 61(5), 458 to 471, 2014) [searched], whole; White, "A Reality Check for Data Snooping" (Econometrica 68(5), 2000), section 1 and the test's statement; Harvey, Liu and Zhu (RFS 29(1), 2016), the introduction and the section that derives the $t$ hurdle | AFML chapter 11's and 14's exercises on PBO and the DSR (problem-inspired); homework IS2 | Hansen, "A Test for Superior Predictive Ability" (JBES 23(4), 2005) [recalled]; Sullivan, Timmermann and White, "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap" (JF 54(5), 1999) [recalled], sections 1 to 3; Harvey, "The Scientific Outlook in Financial Economics" (JF 72(4), 2017) [recalled], the sections on $p$-hacking |

### 5.2 Course AU: Auditing Other People's Results

| Level | Spine and checklist | Papers (by section) | Problems | Stretch |
|---|---|---|---|---|
| AU1 | AFML chapter 11, "The Dangers of Backtesting", 11.2 to 11.5: "Mission Impossible: The Flawless Backtest", "Even If Your Backtest Is Flawless, It Is Probably Wrong", "Backtesting Is Not a Research Tool" and "A Few General Recommendations" [searched headings], with the seven sins of quantitative investing it quotes from Luo and others (Deutsche Bank, 2014) [recalled, placed in 11.2: check]; Arnott, Harvey and Markowitz (2019), whole: its protocol's seven categories (research motivation; multiple testing and statistical methods; data and sample choice; cross-validation; model dynamics; model complexity; research culture [recalled names; research culture and model complexity confirmed by search]), of which data and sample choice, cross-validation and model dynamics, with its questions on transaction costs, are the audit's checklist [check where the cost questions sit] | Chan, *Quantitative Trading*, 2nd ed (Wiley 2021), chapter 3, "Backtesting", and its section "Common Backtesting Pitfalls to Avoid" [searched] | Homework AU1; the exit audit | Shumway, "The Delisting Bias in CRSP Data" (JF 52(1), 327 to 340, 1997) [searched], the introduction and the delisting-return estimates; Novy-Marx and Velikov, "A Taxonomy of Anomalies and Their Trading Costs" (RFS 29(1), 2016) [recalled], sections 1 and 2; Kapoor and Narayanan (2023), the leakage taxonomy, as the ML analogue |
| AU2 | | Ioannidis, "Why Most Published Research Findings Are False" (PLoS Medicine 2(8), 2005), whole; Gelman and Carlin, "Beyond Power Calculations: Assessing Type S (Sign) and Type M (Magnitude) Errors" (Perspectives on Psychological Science 9(6), 2014) [recalled], the definitions and the worked example; McLean and Pontiff, "Does Academic Research Destroy Stock Return Predictability?" (JF 71(1), 2016), the introduction and main results; Recht and others (ICML 2019), sections 1 to 3; Kapoor and Narayanan, "Leakage and the Reproducibility Crisis in Machine-Learning-Based Science" (Patterns 4(9), 2023) [searched], whole; Henderson and others, "Deep Reinforcement Learning That Matters" (AAAI 2018) [searched], the sections on random seeds and trials and on reporting evaluation metrics [recalled titles; check]; Dodge and others, "Show Your Work" (EMNLP 2019), sections 1 to 3 | Homework AU2 | Hou, Xue and Zhang, "Replicating Anomalies" (RFS 33(5), 2020) and Jensen, Kelly and Pedersen, "Is There a Replication Crisis in Finance?" (JF 78(5), 2023), introductions only, as previews of 3.1 level WS2; Bouthillier and others, "Accounting for Variance in Machine Learning Benchmarks" (MLSys 2021, arXiv 2103.03098) [searched]; Reinhart, chapter 2, "Statistical Power and Underpowered Statistics", and chapter 4, "The p Value and the Base Rate Fallacy" [searched] |

### 5.3 Course RP: Reporting and Pre-registration

| Level | Spine and checklist | Papers (by section) | Problems | Stretch |
|---|---|---|---|---|
| RP1 | Arnott, Harvey and Markowitz (2019), the research-culture category of the protocol [searched] | 2.1 lesson 151's note, recapped in lesson 24 (no new reading) | Homework RP1 | Pineau and others, "Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)" (JMLR 22(164), 2021, free) [searched], the checklist; Reinhart, chapter 12, "What Can Be Done?" [searched] |
| RP2 | Arnott, Harvey and Markowitz (2019), the categories on research motivation and on multiple testing and statistical methods [recalled names; check] | Nosek and others, "The Preregistration Revolution" (PNAS 115(11), 2018) [recalled], whole; Simmons, Nelson and Simonsohn, "False-Positive Psychology" (Psychological Science 22(11), 2011), whole, with its requirements for authors; Gelman and Loken, "The Statistical Crisis in Science" (American Scientist 102(6), 2014), whole | Homework RP2; the exit pre-registration; the AsPredicted pre-registration form (aspredicted.org, free; nine questions, designed by Simmons, Nelson and Simonsohn [searched]) read as a model of brevity [check the questions' current wording] | Reinhart, chapter 9, "Researcher Freedom: Good Vibrations?" [searched] |

---

## 6. Verification approach

Every graded answer is computed twice, by two implementations that share no code (`CONTENT-FORMAT.md` 6.2): the item's generator or widget model in TypeScript (`@zq/models/research`, section 8.3), and the Python verifier `zqverify` run in CI on CPython 3.12 with the pinned stack, written from the generator's plain-language `semantics`. Disagreement fails the build. Research method adds four rules of its own [our choice]:

1. **Planted truths are re-derived, not trusted.** Every fixture with a planted defect or effect is regenerated by `market-gen` from its seed, and the reference backtester measures each planted defect's effect by switching it off; the audit fixture's 32-combination table (section 3.2.1) is recomputed on every build, and a fixture whose stored table drifts fails.
2. **A resampled number is never an answer key.** Bootstrap intervals, null distributions and pipeline error rates on screens are fixture replays. A drill compares a learner's resampled output with the reference implementation within a band equal to 4 seed-to-seed standard deviations measured over at least 20 seeds on CPython and on Pyodide; every known-wrong solution must fall outside the band, or the drill's configuration changes.
3. **The perturbation test is run on every rule.** Every strategy in every fixture, lesson and drill is put through the future-perturbation test of lesson 13 in CI: rules meant to be honest must pass, rules carrying planted look-ahead must fail, at every decision date.
4. **Paper figures stay context.** A lint fails any accepted answer, distractor value or hidden test that references a figure tagged [recalled] (decision 9).

| Family | Items | CI: second implementation and checks | Runtime check | Traps the check must catch |
|---|---|---|---|---|
| Sharpe-ratio statistics (PSR, minimum track record, $\eta(q)$, the sub-period $\chi^2$) | IS1, Q1, Q5 | SciPy's normal functions against mpmath at 30 digits; $\eta(q)$ by direct summation against the variance of simulated $q$-period sums (within 4 standard errors, never graded) | `numeric` with stated tolerance | Annual Sharpe ratios in per-period formulas; non-excess and excess kurtosis confused |
| Bootstraps and nulls | IS1, lessons 3, 4, 11, the bootstrap drills | Rule 2's bands; the stationary bootstrap's index distribution checked uniform over days (wrapping) in 200,000 draws; empirical $p$-values checked to use the add-one rule | Drill hidden tests | Single-day resampling; blocks truncated at the end; $p = 0$ |
| Expected maxima and the DSR | IS2, Q7, Q13, the exit drill | The Bailey-López de Prado approximation against the exact expected maximum of $N$ normals by numerical integration (the gap is stated on screens, never graded); the DSR against a second implementation from the PSR | `numeric` | The missing Euler-Mascheroni term; $N$ counted as the shortlist |
| CSCV and PBO | IS2, Q8, homework IS2 example B | Brute-force enumeration of every half-split against the generator's count; generators reject matrices with ties in a winner or its rank | `numeric` | Ranks counted from the top; ties broken silently |
| Multiple-testing thresholds | Lessons 9, 11, 32 | SciPy quantiles; the garden's false-positive rate for each fixture data set recomputed by running all its analyses | `numeric` | Two-sided quantiles in one-sided tests; independence assumed for correlated analyses |
| Audit fixtures and the perturbation test | AU1, Q6, Q12, the exit audit | Rules 1 and 3; each decoy shown to be correct by the same tests; every location span checked to contain the defect's lines and nothing a decoy owns | `set` and `mapping` against the sealed defect list | A decoy flagged as a defect; a span that also covers an honest line |
| Price adjustments and costs | Lessons 15, 16, Q3, Q9 | Exact rational arithmetic on split factors, dividends and turnover; break-even costs solved exactly | `numeric` | Counting one side of each trade; dividends inside adjusted prices and added again |
| Attribution | Lesson 18, Q10, homework AU1 example B | Shapley values by enumerating every order against the subset formula, in exact fractions | `numeric` | One order's effects reported as the split |
| PPV, the significance filter and paired tests | AU2, Q4, Q11 | Exact fractions for PPV with and without bias; the truncated-normal mean in closed form against numerical integration and a $10^6$-draw simulation (within 4 standard errors, never graded); McNemar's statistic from the counts | `numeric` | $p$ read as the probability a finding is true; unpaired errors for a paired comparison |
| Budgets and seeds | Lesson 23 | The expected maximum of $n$ uniforms, $a + (b - a)\frac{n}{n + 1}$, exactly, against order-statistic integration | `numeric` | Comparing best runs at unequal budgets |
| Test length, power and sequential looks | Lesson 31, Q11, homework RP2 example B | Closed forms against the per-period PSR solved numerically; bivariate-normal probabilities by SciPy against Genz's algorithm in mpmath and a seeded simulation; the restoring boundary by root-finding | `numeric` | One-sided and two-sided quantiles confused; looks treated as independent |
| Code shown in quizzes | Lesson 13 Q4 and other T items | The shown code executed on CPython and on Pyodide; its printed output is the answer | `output` | Off-by-one slices in a perturbation; floating-point equality |
| Long-form items | Every set; Q12 to Q14 | Each model-answer line's arithmetic checked by SymPy or exact fractions; each rubric point names lines that exist (`CONTENT-FORMAT.md` 6.8) | Self-marking with Bertie's suggested mark and evidence quote | Rubric points no line evidences |
| The pre-registration | Homework RP2, the exit | A gold set of 12 pre-registrations marked by the paid reviewer (`docs/PLAN.md` 12 decision 10) against which Bertie's suggested marks are calibrated before release; the lock's order against the project's data milestone checked from the event log | Rubric self-mark with the lock rule | A plan locked after the data was opened; a decision rule that names no threshold |
| Citations | Sections 1, 2 and 5 | `sources.yaml` entries with `checked: false`; CI lists every unchecked citation content cites | | An AFML section number cited as fact (open item 2) |
| Copy | Every learner-facing string | Lints: British spelling, no em dashes, the banned-word list with the technical-term allow-list (`docs/PLAN.md` 12 decision 8), the tutor-field leak check (`CONTENT-FORMAT.md` 3.10) | | A planted defect named in a tutor field |

**Verified while writing this file** [verified]: every numeric hook in section 2, every example in section 3, every exam total and specimen in section 4, and every value in section 7. Notable checks: the minimum track record of 2,730 days for annual Sharpe 0.5 and the PSR of 0.958 and 0.81; $\eta(12) = 2.61$ and 4.17; the AR(1) factor 1.53; the decade test ($Q = 14.9$, $p = 0.0006$ at the stem's rounded 0.32; $Q = 15.2$, $p = 0.0005$ at the unrounded 0.317, the annual standard error from daily data); the DSR of 0.759 (lesson 7), 0.763, 0.945 and 0.881 (homework IS2 example A) and 0.598 (Q13), with the approximate expected maximum against the exact integral (2.276 against 2.249 for $N = 50$); the CSCV example's six splits and PBO of 0.5; the Shapley shares $\frac{59}{60}$, $\frac{23}{60}$ and $\frac56$; the PPVs 0.64, 0.31, 0.092, 0.50, 0.20, 0.26 and 0.275; the significance filter's power 0.165, expected estimate 0.973 and two-sided wrong-sign rate 0.260; McNemar's $z = 1.22$; the test lengths 24.75, 6.20, 6.52 and 9.97 years (with the PSR's leading 1; 24.74, 6.19, 6.44 and 9.89 without it); the two-look false-positive rate of 0.080, the boundary 1.875 and the powers 0.43 and 0.47; the sample lesson's prices, averages, positions, perturbation and P&L in exact fractions, and Q4's printed output on CPython. The bootstrap drill's thresholds were set from 20-seed simulations [simulated]. The scripts live in the session scratchpad, not in the repository; the fixture pipeline regenerates every value in CI.

**What verification cannot prove** (`CONTENT-FORMAT.md` 6.13): that a hook is engaging, that a trap catches the misconception it targets, that the audit's decoys are as tempting as real defects, or that a rubric rewards judgement rather than vocabulary. The owner's review of each level before release and the paid reviewer's spot checks cover the first three; item statistics afterwards flag a decoy nobody flags or a trap fewer than 30% of learners fall into.

---

## 7. Sample lesson in full: "Look-ahead in disguise"

**Why this lesson** (decision 13). Look-ahead is the first of the exit's five defects and the one a careful author most often hides from themselves, because the obvious guard (lagging the signal) is present and the leak is somewhere else: in a statistic computed over the whole sample. 1.1 lesson 94 taught the shift; 2.1 lessons 124 and 125 taught known-at times and pipeline leakage. This lesson turns them into an auditor's tool that does not depend on reading every line: change the future and see whether the past moves.

### 7.1 Lesson header

| Field | Value |
|---|---|
| Id | `lsn.audit.look-ahead-disguised` (course AU, level AU1, lesson 13 of 2.2c) |
| Length | 12 screens (1 title, 1 explore, 1 summary, 9 tasks) and a quiz of 4 items; about 11 minutes of screens and 4 of quiz |
| Requires | 1.1 lesson 94 (look-ahead and correct shifts); 2.1 lessons 124 (known-at times) and 125 (pipeline leakage); 2.2 lesson 42 (a full-sample hedge ratio) helps and is not required |
| Introduces | `skl.research.detect-look-ahead`; step tags `full-sample-statistic`, `centred-window`, `backward-fill`, `fitted-on-all-data`, `non-price-input`, `perturbation-boundary`; terms "future-perturbation test" (embargoed for Bertie until screen 4) and "look-ahead in disguise" (until screen 5) |
| Frame (why it exists) | An auditor has a day and a 300-line backtest written by someone else. Reading every line for a missing lag finds the careless leaks and misses the careful ones, because a lag can be present while the signal it lags was computed from the future. A test that treats the backtest as a black box finds both |
| Insight (the aha line) | A position decided on day $t$ may depend only on what was known by day $t$. So change everything after day $t$: if any position on or before day $t$ moves, the backtest is reading the future, wherever the leak is hidden |
| Misconceptions | `mc.research.shift-means-no-look-ahead` (the bait of screen 5), `mc.research.best-result-most-careful`, `mc.research.short-sample-explains-it`, `mc.research.perturbed-days-only`, `mc.research.perturb-from-t`, `mc.research.prices-are-the-only-input`, `mc.research.scaler-is-harmless`, `mc.research.cumsum-is-full-sample` (all [new]) |
| Worked example with a decision point | Screen 7: six snippets from an unfamiliar backtest, each with a correct lag. Reading for the lag passes all six; running the test fails four. The decision: read the code or test the behaviour |
| Derivation | Screen 8 (`derive` with `leap`): the test's two boundaries, completed by the learner: perturb days $t + 1$ to the end; compare positions on days 1 to $t$ |
| Trap and edge cases | Trap: screen 5 (a lag means no look-ahead). Edges: screen 8 (perturbing day $t$ itself raises a false alarm on an honest rule), screen 9 (inputs that are not prices need their own perturbation) |
| Transfer | Screen 10: a scaler fitted on every row before cross-validation (2.1 lesson 125) fails the same test |
| Sources | AFML chapter 11 on look-ahead among the seven sins (recalled as 11.2 [check section]); Arnott, Harvey and Markowitz (2019), the data and sample choice category [recalled name; check]; 1.1 lesson 94 |
| Lesson-wide tutor guidance | Do not say "perturbation test" before screen 4 or "disguise" before screen 5; never state 102.4, the changed days $\{1, 3, 5, 6\}$, £8, or which snippets pass (£12 and £4 are given in the hook's prose), before the Check of the screen that asks for them; prefer "what could the rule have known on that day?", "which prices went into that average?" and "if tomorrow's price were different, would today's decision change?" to statements; never call a learner's honest rule wrong because it earns less |

**The data**, fixed and shown on every canvas as a table and as a price chart drawn by `plot-2d` (values as text; colour never the only carrier of meaning). Rule F holds the share for the next day when today's close is below the average of all ten closes; rule E holds it when today's close is below the average of the closes so far. Both decide at the close and hold from that close to the next one (lesson simplification: trading at the closing price; 2.3 level BT1 uses the next open). P&L is per share, in pounds.

| Day | Close | Average used by F | Average used by E | F holds next day | E holds next day |
|---|---|---|---|---|---|
| 1 | 100 | 100 | 100.00 | no | no |
| 2 | 98 | 100 | 99.00 | yes | yes |
| 3 | 102 | 100 | 100.00 | no | no |
| 4 | 106 | 100 | 101.50 | no | no |
| 5 | 102 | 100 | 101.60 | no | no |
| 6 | 100 | 100 | 101.33 | no | yes |
| 7 | 96 | 100 | 100.57 | yes | yes |
| 8 | 100 | 100 | 100.50 | no | yes |
| 9 | 96 | 100 | 100.00 | yes | yes |
| 10 | 100 | | | | |

F holds over days 2 to 3, 7 to 8 and 9 to 10: $+4 + 4 + 4 = £12$, three trades, three winners. E holds over days 2 to 3, 6 to 7, 7 to 8, 8 to 9 and 9 to 10: $+4 - 4 + 4 - 4 + 4 = £4$. Holding throughout: $100 - 100 = £0$. Held in the widget's `secret()` until each screen's Check: F's perturbed average 102.4; changed positions $\{1, 3, 5, 6\}$; the defect's effect £8.

### 7.2 Screens

---

**Screen 1. Title** (`title`)

- **Heading:** Look-ahead in disguise
- **Prose:** "A backtest can read the future without a single missing lag. Here is a test that finds it without reading every line."
- **Art:** Bertie holding a magnifying glass over a price chart with a sticky note reading "Sharpe 3.1"; his soft, rounded hair puffs out in cloud-like tufts on both sides of his head, his moustache drooping as he squints.
- **Action:** Continue.

---

**Screen 2. The hook** (`problem`, id `hook`, `predictFirst`)

- **Prose:** "Two versions of one rule: hold the share tomorrow when today's close is below the average close. Version F averages all ten days; version E averages only the days so far. Both lag the signal by one day before trading. Over ten days F makes £12 on three trades, all winners; E makes £4; holding the share throughout makes £0."
- **Widget:** `backtest-lab` in perturb mode [mode to add], read-only: the ten-day price chart with F's and E's holding days marked as bands, and each rule's two lines of code in `code-review`: F `avg = px.mean(); sig = (px < avg).shift(1)`; E `avg = px.expanding().mean(); sig = (px < avg).shift(1)`. The perturb handles are hidden until Check.
- **Question:** "Which backtest can you trust?"
- **Answer input:** `choice`, four cards.
- **Correct:** B.

| Option | Correct? | Misconception | Feedback |
|---|---|---|---|
| A. F only: it makes more and never loses | no | `mc.research.best-result-most-careful` | "Three winners out of three is a warning sign, not a credential (lesson 12). Look at what F's average contains on day 2." |
| B. E only | yes | | "Yes. Hold on to the reason; the next screen lets you test it." |
| C. Both: each lags its signal by a day | no | `mc.research.shift-means-no-look-ahead` | "Both have the lag. The lag fixes when a signal is traded, not what it was computed from. Which days' closes go into F's average?" |
| D. Neither: ten days prove nothing | no | `mc.research.short-sample-explains-it` | "Ten days prove nothing about skill, true. The question is different: could each £ have been earned at the time? One of the two could not." |

- **Hints.** Nudge: "On day 2, which closes has the market shown so far?" Point: highlights days 1 and 2 on the chart, then all ten days under F's average. Step: "F's average on day 2 is 100, the mean of all ten closes, eight of them still in the future. E's is 99, the mean of days 1 and 2."
- **Why?** Yours: "E only." Then: "F decides on day 2 with an average built from days 3 to 10. Nothing in its code is lagged wrongly, and still it reads the future."
- **Tutor.** Focus: what each average contains on a given day. Notes: most learners choose B on instinct but cannot say why, or choose C because the code has a shift; screen 5 is built for C. Reps: table, chart. Avoid: "perturb", "disguise"; the numbers 102.4 and 8.

---

**Screen 3. Change the future** (`explore`, id `perturb`)

- **Prose:** "Drag any price from day 7 to day 10 up or down. Watch the holding decisions on days 1 to 6."
- **Widget:** `backtest-lab` perturb mode: handles on the closes of days 7 to 10 (steps of £1, range $\pm$£10); below the chart, two rows of six cells, "F decides" and "E decides" for days 1 to 6, each cell showing hold or not and outlined when it differs from the original; a readout "decisions on days 1 to 6 changed: F $k$, E $m$".
- **Continue when:** at least one handle has moved and the learner has returned it or moved another.
- **Graded:** nothing.
- **Tutor.** Focus: E's row never changes, however far the future moves; F's row changes as soon as the average crosses one of the early closes. Notes: if the learner moves prices only downwards, suggest an upward move: any rise flips F's days 1 and 6 at once (both close at 100, and the average rises above 100), while falls change nothing on days 1 to 6 until they total £20 (the average reaches 98 and day 2 flips). Reps: picture, table. Avoid: naming the test.

---

**Screen 4. The future-perturbation test** (`problem`, id `name`)

- **Prose:** "What you just did is the **future-perturbation test**: change everything after a day and see whether any decision on or before that day moves. Do it exactly: add £6 to every close from day 7 on."
- **Widget:** `backtest-lab` perturb mode with a "+£6 from day 7" button; F's row of days 1 to 6 becomes tappable.
- **Question:** "Which of F's decisions on days 1 to 6 change?"
- **Answer input:** `card-sort` as a tap-to-select set over days 1 to 6.
- **Correct:** days 1, 3, 5 and 6.

| Wrong answer | Misconception | Feedback |
|---|---|---|
| none | `mc.research.shift-means-no-look-ahead` | "Recompute F's average with the new closes: $\frac{1000 + 24}{10}$. Is 100 still above it?" |
| days 7 to 10 | `mc.research.perturbed-days-only` | "Those are the days you changed; of course they move. The test looks at the days you did not change." |
| days 1, 3 and 5 | slip | "Check day 6: its close is 100 and the new average is 102.4." |
| anything else | (otherwise) | "The new average is 102.4. Which of the closes on days 1 to 6 are now below it, that were not below 100?" |

- **Hints.** Nudge: "What is F's average after the change?" Point: highlights the average line moving from 100 to 102.4. Step: "Days 1, 3, 5 and 6 close at 100, 102, 102 and 100: all below 102.4 and none below 100, so all four flip to hold."
- **Why?** Yours: "Days 1, 3, 5 and 6." Then: "Four decisions made on days 1 to 6 changed when only days 7 to 10 changed. F reads the future. E's row did not move: E passes."
- **Tutor.** Focus: the test's verdict comes from behaviour, not from reading the code. Notes: the slip on day 6 is common; it is the boundary case. Avoid: the word "disguise".

---

**Screen 5. But the signal is lagged** (`trap`, id `lag`, `trap: { mc: mc.research.shift-means-no-look-ahead, bait: A }`)

- **Prose:** "F's author replies: 'Every signal is shifted by one day before it is traded, so the backtest cannot use tomorrow's information.'"
- **Widget:** F's two lines of code in `code-review`, read-only, with `.shift(1)` highlighted.
- **Question:** "Is the shift enough?"
- **Answer input:** `choice`, four cards.
- **Correct:** B.

| Option | Correct? | Misconception | Feedback |
|---|---|---|---|
| A. Yes: shifting the signal is exactly what prevents look-ahead (the bait) | no | `mc.research.shift-means-no-look-ahead` | "The shift moves the signal one day later. But the signal on day 2 already contained days 3 to 10, through `px.mean()`. Shifting a leaked number delivers the leak a day later." |
| B. No: the shift fixes when the signal is used, not what it was computed from | yes | | "Yes. This is **look-ahead in disguise**: the lag is right and the input is wrong." |
| C. Yes, if the shift were two days instead of one | no | `mc.research.shift-means-no-look-ahead` | "Any shift leaves `px.mean()` unchanged: it is the same number, built from all ten days, on every day." |
| D. No, but only because ten days are too few to tell | no | `mc.research.short-sample-explains-it` | "The leak has nothing to do with the sample's length: with ten years, `px.mean()` would contain ten years of future." |

- **Hints.** Nudge: "On day 2, what number does `px.mean()` return?" Point: highlights `px.mean()`. Step: "`px.mean()` is one number, the mean of all ten closes; every day's signal compares with it, including day 2's."
- **Why?** Shown: "A lag answers 'when was the signal used?'; look-ahead asks 'what went into it?'. The disguise is a correct answer to the first question."
- **Self-explanation prompt** (unmarked, `ASSESSMENT.md` 2.2): "In one sentence: why does the shift not help F?"
- **Tutor.** Notes: most learners who chose C on screen 2 choose A here; the screen exists to be failed once. Avoid: "expanding", which is E's fix and screen 11's.

---

**Screen 6. Where the line moves** (`ladder`, id `average`, constraint "The number behind the decision")

- **Prose:** "The test flipped four decisions. Find the number that moved them."
- **Widget:** `value-table` with F's average before and after the change, the after cell empty; the chart with both average lines.
- **Question:** "After adding £6 to days 7 to 10, what average does F compare every day with?"
- **Answer input:** `numeric-input`.
- **Correct:** 102.4.

| Wrong answer | Misconception | Feedback |
|---|---|---|
| 100 | `mc.research.shift-means-no-look-ahead` | "That is the old average. F's average includes days 7 to 10, which now total £24 more." |
| 106 | slip | "The £24 is spread over ten days, not added once." |
| 100.6 | slip | "That adds £6 once. Each of the four days gains £6: £24 in all, so the new total is 1,024." |
| anything else | (otherwise) | "New total: $1000 + 4\times 6 = 1024$. Divide by the ten days." |

- **Hints.** Nudge: "What was the total of the ten closes before the change?" Point: highlights the total, 1,000. Step: "$\frac{1000 + 24}{10} = 102.4$."
- **Why?** Yours: "102.4." Then: "One number built from all ten days moved every early decision that sat near it. That is why a full-sample statistic is the commonest disguise."
- **Tutor.** Focus: the shared number behind all of F's decisions. Reps: arithmetic, table.

---

**Screen 7. Read the code, or run the test?** (`ladder`, id `snippets`, constraint "Six snippets, each with a lag", worked example with a decision point)

- **Prose:** "You are auditing a 300-line backtest by someone else. Six snippets compute its signals; every one lags its signal before trading. Reading for a missing lag passes all six. Sort them by what the perturbation test would say."
- **Widget:** `card-sort` with two bins, "passes" and "fails", and six cards of code, each with a one-line description shown on long-press:
  - a. `avg = px.expanding().mean(); sig = (px < avg).shift(1)`
  - b. `z = (px - px.mean()) / px.std(); sig = (z < -1).shift(1)`
  - c. `avg = px.rolling(5, center=True).mean(); sig = (px < avg).shift(1)`
  - d. `px = px.bfill(); sig = (px.pct_change() < -0.05).shift(1)`
  - e. `beta = np.polyfit(x, y, 1)[0]; sig = (y - beta * x > 2).shift(1)`
  - f. `avg = px.rolling(20).mean(); sig = (px < avg).shift(1)`
- **Correct:** passes a and f; fails b, c, d and e.

| Wrong answer | Misconception | Feedback |
|---|---|---|
| b in "passes" | `mc.research.shift-means-no-look-ahead` | "`px.mean()` and `px.std()` cover every day, future included: F's disguise with a $z$-score on top." |
| c in "passes" | `mc.research.shift-means-no-look-ahead` | "A centred window of 5 uses the two days after each day. Change those and today's average moves." |
| d in "passes" | `mc.research.shift-means-no-look-ahead` | "`bfill()` fills a gap with the next known price, from the future. The test catches it on the day of the gap." |
| e in "passes" | `mc.research.shift-means-no-look-ahead` | "`polyfit` over all of `x` and `y` fits the hedge ratio to the whole history, the defect of 2.2 lesson 42." |
| a or f in "fails" | (overcorrection) | "This one uses only days up to today: an expanding or a trailing window. Change the future and its decisions stay put." |

- **Hints.** Nudge: "For each card: which days does the number before `.shift(1)` use?" Point: highlights `mean()`, `center=True`, `bfill()` and `polyfit` in turn. Step: "Only `expanding()` and a trailing `rolling(20)` stop at today. The other four each use some day after today."
- **Why?** Yours: the sorted bins. Then: "The decision point: reading for the lag passed all six; asking what each number contains failed four. The test asks that question for you, for every line at once, including lines you never open."
- **Tutor.** Focus: the four disguises by name: full-sample statistic, centred window, backward fill, fitted on all data. Notes: `bfill` is the one learners miss most. Avoid: telling the learner which bin a card belongs in before Check.

---

**Screen 8. The test, exactly** (`derive`, id `rule`, `leap: { naive, fails, pointsTo }`)

- **Prose:** "Write the test so that it can be run on any backtest, at any day $t$."
- **Widget:** `derivation-steps` in fill mode:
  1. "Run the backtest; record every decision on days 1 to $t$."
  2. "Change every price on days $\boxed{\phantom{0}}$ to the last day."
  3. "Run it again on the changed prices."
  4. "If any decision on days $\boxed{\phantom{0}}$ moved, the backtest reads the future."
- **Leap** (shown after Check, as the decision point):
  - *Naive:* "Change day $t$ too, to be safe: more change, more chance to catch a leak."
  - *Fails:* "Run it on E at $t = 6$ with day 6 changed as well: E's day-6 average becomes 102.33 and its close 106, so E's day-6 decision flips from hold to not. E is honest; the test has raised a false alarm, because a decision on day 6 is allowed to use day 6's close."
  - *Points to:* "Change only what was unknown on day $t$: days $t + 1$ onwards. Compare every decision up to and including day $t$."
- **Answer input:** two `expression-input` boxes.
- **Correct:** $t + 1$; 1 to $t$.

| Wrong answer | Misconception | Feedback |
|---|---|---|
| $t$ in box 1 | `mc.research.perturb-from-t` | "Then day $t$'s own close changes, and an honest rule's day-$t$ decision may move. Which prices were unknown on day $t$?" |
| "$t + 1$ to the end" in box 2 | `mc.research.perturbed-days-only` | "Those decisions are allowed to move. The test is about the days you did not change." |
| "$t$ only" in box 2 | slip | "A leak may show on any earlier day (F's changed on days 1, 3, 5 and 6). Compare them all." |
| anything else | (otherwise) | "Change what was unknown on day $t$; compare what was decided by day $t$." |

- **Hints.** Nudge: "Which prices could a decision on day $t$ legitimately use?" Point: highlights day $t$ on the chart. Step: "Day $t$'s close is known when day $t$'s decision is made; days $t + 1$ onwards are not. So change $t + 1$ onwards and compare days 1 to $t$."
- **Why?** Yours: "Change days $t + 1$ to the end; compare days 1 to $t$." Then: "That is the whole test. Run it at many values of $t$ with several random changes, and a leak anywhere in the code shows up as a moved decision."
- **Tutor.** Focus: the two boundaries. Notes: the naive answer is a sensible instinct; credit it before showing the false alarm. Avoid: calling the inclusive version "wrong" without the E example.

---

**Screen 9. Inputs that are not prices** (`ladder`, id `inputs`, constraint "Other inputs have dates too")

- **Prose:** "The test changes future prices. Some leaks do not live in prices."
- **Widget:** `card-sort` as multi-select over four defect cards, each with a one-line example.
- **Question:** "Which of these can a test that changes only future prices miss?"
- **Answer input:** multi-select.
- **Correct:** A and B.

| Option | Correct? | Misconception | Feedback |
|---|---|---|---|
| A. The universe is today's index members | yes | | "Membership is a separate input: changing prices leaves it as it is. Perturb the membership file by date, or rebuild it point in time (lesson 14)." |
| B. December accounts are used from 1 January, though published in March | yes | | "Accounts are their own input with their own dates. Perturb each value after its release date, or join on release dates (2.1 lesson 124)." |
| C. A full-sample $z$-score of prices | no (caught) | `mc.research.prices-are-the-only-input` | "This one the price test catches: the $z$-score moves when future prices move." |
| D. A centred moving average of prices | no (caught) | `mc.research.prices-are-the-only-input` | "Caught: the centred window reads tomorrow's price." |

- **Hints.** Nudge: "Which of these leaks would still be there if every future price stayed exactly the same?" Step: "Membership lists and accounting figures carry their own dates; the price test never touches them."
- **Why?** Yours: "A and B." Then: "Perturb every input that has a date: prices, accounts by release date, membership lists, corporate-action files. One test per input."
- **Tutor.** Focus: the test's reach is the inputs it changes. Reps: list.

---

**Screen 10. The same test in a lab** (`ladder`, id `transfer`, constraint "A model pipeline")

- **Prose:** "A colleague standardises every feature with a scaler fitted on all rows, then runs cross-validation (2.1 lesson 125). Run the same test: change only the test fold's rows."
- **Widget:** `leakage-detective` in pipeline mode, read-only, with the scaler step and a "change the test rows" toggle; the training rows' transformed values shown in a `value-table`.
- **Question:** "When you change only the test rows, do the transformed training rows move?"
- **Answer input:** `choice`, two cards.
- **Correct:** "Yes: the scaler's mean and spread include the test rows."

| Option | Correct? | Misconception | Feedback |
|---|---|---|---|
| Yes: the scaler's mean and spread include the test rows | yes | | "Yes. Training saw a summary of the test data: the pipeline reads the future in exactly F's way." |
| No: a scaler only rescales, it learns nothing | no | `mc.research.scaler-is-harmless` | "It learns a mean and a spread, from every row it was fitted on. Toggle the test rows and watch the training values." |

- **Why?** Shown: "The test is the same in a lab: change what the model must not know, and check that nothing it was trained on moves. Fitting the scaler inside each fold passes."
- **Tutor.** Focus: the same defect in an ML pipeline. Avoid: "data leakage" as a vague label; name what moved.

---

**Screen 11. How much did the future earn?** (`ladder`, id `effect`, constraint "Size the defect")

- **Prose:** "An audit reports the effect, not only the defect (lesson 18). Replace F's full-sample average with the average so far: that is rule E."
- **Widget:** `backtest-lab` with a "fix: average so far" toggle; P&L readouts for F, the fixed rule and holding throughout.
- **Question:** "How much of F's £12 did the defect produce?"
- **Answer input:** `numeric-input`, pounds.
- **Correct:** 8.

| Wrong answer | Misconception | Feedback |
|---|---|---|
| 12 | slip | "The fixed rule still makes £4; only the difference is the defect's." |
| 4 | slip | "£4 is what the honest rule makes. The defect's share is what disappears when you fix it." |
| anything else | (otherwise) | "F made £12; the fixed rule, E, makes £4." |

- **Hints.** Nudge: "What does the rule make once the average uses only the past?" Step: "$12 - 4 = 8$: two thirds of F's P&L came from the future, and its perfect record (three wins of three) becomes three wins in five."
- **Why?** Yours: "£8." Then: "Report it this way: 'Look-ahead through a full-sample average in `signal.py`; P&L falls from £12 to £4 when fixed; checked by the perturbation test at every day.'"
- **Tutor.** Focus: the fix and the effect, together. Notes: some learners object that £4 over ten days is still good; agree that ten days say nothing about skill (screen 2, option D), and that the audit's job here was only to remove what could not have been earned.

---

**Screen 12. Summary** (`summary`)

- **Ideas:**
  1. "A lag fixes when a signal is used; look-ahead is about what the signal was computed from. A correct lag can carry a leaked signal."
  2. "The future-perturbation test: change every input after day $t$, rerun, and check that no decision on days 1 to $t$ moved. It needs no reading of the code."
  3. "Disguises it catches: full-sample statistics, centred windows, backward fill, anything fitted on all the data. Inputs other than prices (membership, accounts) need their own perturbation."
- **Trap:** "Trusting the shift: `(px < px.mean()).shift(1)` is lagged and still reads the future."
- **Card** (saved to the Notebook): "Perturb days $t + 1$ to the end of every dated input; compare decisions on days 1 to $t$; any change means look-ahead."

### 7.3 Lesson quiz (4 items, 1 mark each, difficulty 2 to 3, one attempt each, no hints, Why? after each)

| # | Item | Type | Difficulty | Correct | Diagnosed wrong answers | Why? |
|---|---|---|---|---|---|---|
| Q1 | A signal is `(px < px.mean()).shift(1)`. What does the shift fix, and what does it leave? | C | 2 | It fixes when the signal is traded; it leaves an average built from future prices | "It removes all look-ahead" (`mc.research.shift-means-no-look-ahead`); "It adds look-ahead" (slip); "Nothing: shifts are only for alignment" (slip) | "The shift moves the decision a day later. `px.mean()` is still the mean of every day, future included." |
| Q2 | Sort into "passes the perturbation test" and "fails": `px.ewm(span=10).mean()`; `(px - px.min()) / (px.max() - px.min())`; `px.interpolate()` on a series with gaps; `px.shift(1).rolling(10).mean()` | S | 3 | Passes: the exponentially weighted mean and the shifted rolling mean. Fails: the min-max scaling and the interpolation | Min-max in "passes" (`mc.research.shift-means-no-look-ahead`: full-sample minimum and maximum); interpolation in "passes" (`mc.research.shift-means-no-look-ahead`: linear interpolation uses the next known value) | "An exponentially weighted mean uses only the past. A full-sample minimum and maximum, and an interpolation across a gap, each use a later price." |
| Q3 | Closes on days 1 to 5: 50, 52, 48, 51, 49. Rule F holds the next day when the close is below the average of all five. Add 10 to day 5's close. How many of F's decisions on days 1 to 4 change? | N | 3 | 2 | 0 (`mc.research.shift-means-no-look-ahead`); 1 (slip: day 4 only, or day 1 only); 4 (overcorrection: every decision assumed to move once the average moves) | "The average rises from 50 to 52. Day 1 (50) and day 4 (51) now fall below it; day 2 (52) is not below 52; day 3 was already below." |
| Q4 | What does this print? `import numpy as np` / `p = np.array([50., 52., 48., 51., 49.])` / `def positions(p):` / `    avg = np.cumsum(p) / np.arange(1, len(p) + 1)` / `    return (p < avg).astype(int)[:-1]` / `q = p.copy()` / `q[4] += 10` / `print((positions(p) != positions(q)).sum())` | T | 3 | `0` | `2` (`mc.research.cumsum-is-full-sample`: reading the average so far as the average of all five days); `1` (slip) | "`np.cumsum(p) / np.arange(...)` is the average so far, so day $t$'s decision uses days 1 to $t$ only. Changing day 5 cannot move decisions on days 1 to 4: the rule passes." |

The quiz creates the FSRS card for `skl.research.detect-look-ahead` (Q1 to Q4); the step tags `full-sample-statistic` (Q1, Q2, Q3), `backward-fill` (Q2's interpolation edge) and `perturbation-boundary` (Q3, Q4) feed the level review. Passed: at least 3 of 4 on the first completion (`ASSESSMENT.md` 2.3, decision 26); any wrong item joins the Redo queue as a fresh variant from `gen.research.perturb-count` or the snippet pool `itm.audit.snippet-sort`. Choice items: 1 of 4.

### 7.4 Verification for this lesson

Recomputed on 7 October 2026 [verified], in exact fractions: the ten closes' total 1,000 and average 100; E's averages so far ($100, 99, 100, 101.5, 101.6, 101.\overline{3}, 100.57, 100.5, 100$); F's decisions (hold after days 2, 7 and 9) and P&L £12; E's decisions (hold after days 2, 6, 7, 8 and 9) and P&L £4; holding throughout £0; after adding £6 to days 7 to 10, F's average $\frac{1024}{10} = 102.4$ and its changed decisions on days 1, 3, 5 and 6, with E's decisions on days 1 to 6 unchanged; the inclusive perturbation (days 6 to 10) flipping E's day-6 decision (average $\frac{614}{6} = 102.33$, close 106); the defect's effect $12 - 4 = 8$; Q3's average 52 and two changed decisions; Q4's printed `0`, by running the code on CPython. CI adds: each snippet of screen 7 and Q2 executed on a seeded series and put through the perturbation test (rule 3 of section 6), confirming each "passes" and "fails"; every distractor replayed through the grader with its diagnosis; every number in the tutor fields checked against each screen's Check so none leaks an answer (`CONTENT-FORMAT.md` 3.10).

### 7.5 What this lesson asks of the widget library

- `backtest-lab` perturb mode [mode to add]: handles on future closes, the per-day decision rows for two rules with changed cells outlined, a "+£$k$ from day $d$" button, a fix toggle with P&L readouts, and a table view of every state for screen readers.
- `code-review` read-only with a highlighted token (screens 2, 5); `card-sort` with code cards and long-press descriptions (screens 7, 9); `derivation-steps` fill mode with a `leap` block (screen 8); `leakage-detective` pipeline mode with a "change the test rows" toggle (screen 10); `predict-output` for Q4.
- No widget on these screens runs Python or a simulation: every value is an exact computation on the fixed ten-day series (decision 6).

---

## 8. New widgets this item needs

One new widget, P2 (`docs/WIDGETS.md` decision 10: first needed in Stage 2), and 12 modes added to existing widgets. It is built with the P2 waves (`docs/WIDGETS.md` 7.4), after the engine and the P0 batches (owner decision 1), in the `projects` cluster beside `backtest-lab`. Every on-screen number comes from `derive` (`docs/PLAN.md` 3.2 rule 2), as fixture lookups or exact computations in `@zq/models/research`.

### 8.1 The new widget

| Id | Purpose | Tier, kind | First use | Size | Composes | Answers |
|---|---|---|---|---|---|---|
| `bias-audit` | Audit a backtest someone else wrote. **Triage mode**: one-paragraph reports with warning-sign chips to order (lesson 12). **Audit mode**: a read-only repository (README, modules, data dictionary, metrics, results note) in an embedded `code-review`; the learner taps a location (line range, data field or note sentence), picks a class from the audit taxonomy, and adds evidence and an effect estimate; a findings ledger lists them (homework AU1). **Attribution mode**: a table of the Sharpe ratio under every combination of fixed defects, each defect's effect fixed first, fixed last and averaged over orders, with the Shapley bar chart (lesson 18). **Exit mode**: audit mode with Bertie away, automatic marking against the sealed defect list (2 marks a defect, 1 off a false finding), and, after submission, the true effects beside the learner's estimates | composite, **scene** with embeds (`docs/PLAN.md` 3.2 rule 5: `code-review` and `backtest-lab` as embedded controlled components). None of rule 3's bespoke reasons holds: findings are taps and inputs, not free editing; effects are fixture lookups, not a service with its own state machine. If `scene.ts` crosses rule 4's 400-line cap, attribution mode splits into a preset | 2.2c lesson 12 (also 18, homework AU1, the exit) | L | `code-review`, `backtest-lab`, `card-sort`, `choice`, `free-response`, `numeric-input`, `value-table`, `plot-2d` (`bars`) | `set`, `mapping`, `ordering`, `numeric`, `state` |

**AI hooks, in brief.** Targets `report:<k>`, `chip:<sign>`, `file:<path>`, `line:<path>:<n>`, `field:<name>`, `sentence:<k>`, `finding:<k>`, `class:<id>`, `cell:<subset>`, `bar:<defect>`; describe, e.g. "Audit of 'Weekly reversal, Sharpe 1.9'. Findings: 3 (look-ahead in signal.py lines 41 to 47; universe in universe.py line 12; costs in the note, sentence 4). Time used 54 of 120 minutes."; secret: the planted defects, their spans and their effects, sealed like an answer key (`docs/PLAN.md` 12 decision 5) and withheld from Bertie entirely in exit mode; tryable: none in exit mode. **Accessibility**: the repository is navigable by file and line with the keyboard; every finding is announced with its location and class; the attribution table and chart have a table view. **Reduced motion**: static.

### 8.2 Modes added to existing widgets

| Widget | Mode | First use | Note |
|---|---|---|---|
| `sampling-lab` | Stationary block bootstrap for a series, with the mean block length as a slider and intervals at two lengths side by side | 3 | Fixture runs on screens; live resampling only below 2,000 draws |
| `sharpe-lab` | Sub-periods with each period's standard error and the joint $\chi^2$ test | 5 | Beside its PSR, years, deflated and haircut modes |
| `backtest-lab` | Perturb: future-price handles, per-day decision rows for two rules, "+£$k$ from day $d$", a fix toggle | 13 | Section 7.5 |
| `backtest-lab` | Bias: adjustment (returns from raw against adjusted closes across splits; dividends counted twice) | 15 | Joins the existing universe and look-ahead bias toggles |
| `icon-array` | Ioannidis's bias $u$ in FDR mode | 19 | FDR mode is P1 (1.6 lesson 40) |
| `test-lab` | Significance filter: the sampling distribution with the significant region shaded, the conditional mean, power, the exaggeration ratio and the wrong-sign rate | 20 | Its power curve already exists |
| `contingency-table` | Paired comparison of two classifiers on one test set, with McNemar's statistic | 22 | |
| `dist-explorer` | The distribution of the maximum of $n$ draws, with its mean | 23 | Also used by lesson 7's exact-against-approximate edge |
| `results-note` | Audit report template (finding, location, evidence, mechanism, effect, fix, check) | 18 | Homework AU1 and the exit |
| `results-note` | Pre-registration template with the lock: the lock time, the project's data-milestone time and a dated deviations log | 30 | The exit pre-registration and every later project plan |
| `multiple-testing` | Garden: analysis choices drawn as a tree with `node-link`, each leaf an analysis of one fixture data set with its $p$-value, and the garden's false-positive rate across fixture data sets | 32 | Replaces `docs/PLAN.md` 12's `forking-paths` (decision 17) |
| `code-cell` | The `zq_research` prelude for homework and exit drills: seeded `market-gen` fixtures, the trial-ledger loader, `isclose` bands for resampled outputs, and the import scan | homework IS1 | Web app only (decision 6); in the Artifact the cell shows the handoff link |

### 8.3 Services and first-use changes

- **`@zq/models/research`** (pure TypeScript, parity-tested against `zqverify`): PSR and minimum track record, $\eta(q)$, expected maxima and the DSR, CSCV enumeration for small matrices, Shapley attribution, PPV with bias, the significance filter, McNemar, test length and power, and the bivariate-normal probability for two looks. Built with the first 2.2c wave; `sharpe-lab`'s existing PSR and deflated modes call it.
- **First uses move earlier** because 2.2c now precedes 2.3: `sharpe-lab` (from 2.3 lesson 7 to 2.2c lesson 1), `backtest-lab` (from 2.3 lesson 4 to 2.2c lesson 4), `paper-trader` (from 2.3 to 2.2c lesson 4) and `mock-interview` (from 2.3 lesson 41 to 2.2c lesson 28). All stay P2; they join the wave briefed before 2.2c instead of the 2.3 wave (request 6).
- **Not built:** `forking-paths` (decision 17).

---

## Verification log (7 October 2026, author's pass)

**Answers recomputed** (Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, SymPy 1.14.0, mpmath 1.3.0; exact fractions where rational): every numeric hook in section 2, both examples of every set in section 3, the exam totals and specimen lines in section 4, and every value in section 7. The project's floor is CPython 3.12; these runs are a record, repeated at `docs/PLAN.md` stage 26.

**Changed while writing.**
- The disposition of 2.3's research-method lessons: a first plan moved RM3 to RM5 and RM7 whole, as `stage1-finance-projects.md` decision 20 says; reading 2.1's level FD1 and lessons 144 to 146 showed that 7 of those 23 lessons repeat lessons every track now takes before 2.2c, so they retire (decision 2, section 0.6).
- A lesson on the replication standards of Hou, Xue and Zhang against Jensen, Kelly and Pedersen was drafted for level AU2 and removed after reading 3.1 lessons 96 and 97, which teach exactly that; lesson 11 (running the whole pipeline on noise) took its place.
- Lesson 5's standard errors: a first draft put the annual Sharpe ratio into $\frac12\widehat{SR}^2$ and got 0.45 for the first decade; with the daily ratio the term is negligible and every decade's error is 0.317, which is what 2.3's original lesson had. The mistake became the lesson's edge.
- Lesson 11's hook first used 20 independent tests, which gives 0.64 and repeats 1.6 lesson 38's hook exactly; it now reports a measured rate (58 of 200) with its interval, and the independent case is the edge.
- The bootstrap drill's AR(1) test first required the block interval to be 25% wider than the single-day one; a 20-seed simulation gave ratios from 1.16 to 1.70, so a correct implementation could fail on an unlucky fixture. The test now requires "wider", which the known-wrong solution fails with a ratio of exactly 1.
- The sample lesson's prices were chosen by an exact search over ten-day integer paths with mean 100 for one where the full-sample rule wins every trade, the honest version earns less, holding earns nothing, and the perturbation flips several early decisions while leaving the honest rule's untouched.
- Homework AU2 example A first planned on the PPV alone (0.64 of 0.4); using the reported estimate's likelihood ratio (16.4) gives a probability real of 0.80 and a planning Sharpe of 0.32, and that refinement became the item's creative step.

**Counts.** 3 courses, 6 levels, 32 lessons numbered 1 to 32 without gaps, ids unique and unused elsewhere [searched]; levels of 4 to 7 lessons; 131 quiz items (128 plus 3 production items), 49 of the 128 choice items (38.3%, at most 38.9% per course); 6 homework sets, 36 items; hours sum to 35.0 with estimates of 32.5 h (92.9%); exam marks 60 with the declared difficulty mix; 17 lessons moved from 2.3 and 7 retired, 24 removed from 2.3 in all [counted by script].

**Not checked, tags kept.** AFML section and exercise numbers; the headings of Arnott, Harvey and Markowitz (2019); the paper figures listed in open item 1; arXiv numbers; the AsPredicted form's current questions; Reinhart's chapter numbers; the Pyodide speed of the exit drill (open item 4). Nothing was found to be invented, so nothing was deleted.

## Verification log (7 October 2026, source and correctness verifier)

**Answers recomputed** with Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, pandas 3.0.6, exact fractions where rational: every hook in section 2, both examples of every set and every drill's stated test value in section 3, the exam totals and the Q13 specimen in section 4, and every value and distractor in section 7, including the snippets of screen 7 and quiz Q2 put through the perturbation test on seeded series and Q4's code run on CPython. Confirmed unchanged: the PSR 0.958 and 0.81, 2,730 days; $\eta(12) = 2.61$ and 4.17; 1.53; 0.121; the DSR 0.759 and PSR 0.998 (no-Euler-Mascheroni variant 0.821); 2.2763 against the exact 2.2491; PBO 0.66 and the CSCV example's six splits (no ties); Bonferroni 3.48; 0.29 and 0.64; 1.2 points; $-49.25\%$ and $+1.5\%$; 0.57 and 9.5 basis points; the Shapley splits 1.05 and 0.75, and $\frac{59}{60}$, $\frac{23}{60}$, $\frac56$; every PPV; power 0.165, 0.973 and 0.260; $z = 1.22$, 0.60 and 0.24 points; 0.798 and 0.783; 0.56; IS1 example B (52.9 and 34.8 months, 0.960 and 0.985); IS2 example A (2.19, 0.76, 0.94, 0.88); AU2 example A (0.35, 0.64, 0.73, 16.4, 0.80, 0.32, 0.23); RP2 examples A (0.52) and B (0.080, 1.875, 0.43, 0.47, confirmed by a $2\times 10^6$-draw simulation); Q13 (2.00, 0.60, 0.986); the exam's 60 marks, difficulty mix, 33 generator marks and 50 minutes; the sample lesson's £12, £4, £0, 102.4, $\{1, 3, 5, 6\}$, 102.33 and £8; Q3's 2 and Q4's `0`. An independent 20-seed run of the bootstrap drill's fixtures gave IID width ratios 0.96 to 1.03 and AR(1) ratios 1.17 to 1.99, consistent with the tests as written [simulated].

**Corrected.**
- Lesson 5's hook stated standard errors of 0.32 but answered $Q = 15.2$, which needs the unrounded 0.317; at 0.32, $Q = 14.9$ and $p = 0.0006$. Both are now given.
- Lesson 20's hook stated a standard error of 0.45; its answers (power 0.17, 0.97) need $1/\sqrt5 = 0.447$ (0.45 gives 0.98). The stem now states 0.447.
- Lesson 11's interval (0.23 to 0.35) is the normal approximation; the stem now says so and gives the exact interval, 0.23 to 0.36.
- `drl.research.test-length`: the stated values (24.74, 6.19, 9.89, 6.44) dropped the PSR's leading 1, which lesson 1 and homework IS1 example B keep; with it they are 24.75, 6.20, 9.97 and 6.52, and the monthly test would have failed a correct implementation. The formula is now written out, and the variant without the 1 is a named known-wrong. Section 6's list follows.
- Sample lesson, screen 3's tutor note claimed F's row changes only for large moves; any upward move of one price flips days 1 and 6 at once, and falls need a total of £20. Rewritten.
- Quiz Q3's distractor 4 was tagged `mc.research.perturbed-days-only`, which predicts 0 here, not 4; retagged as an overcorrection.
- The lesson-wide tutor guidance forbade stating £12 and £4, which the hook's prose states; removed from the list.
- Homework AU1 example B's report line said fixing either interacting defect first understates the other; it understates itself (L 0.9 first against 1.0 after C; C 0.8 against 0.9). Rewritten with the numbers.
- Pace: the Main block needs 3.4 weeks, so "about 3 weeks" became "about 3.5 weeks".

**Hours and scope.** The budget sums to 35.0 h (8.0, 2.25, 13.0, 3.0, 4.25, 4.5), estimates to 32.5 h, each set to 130 minutes, and the canon-gap split by level to 35.0 h. Every topic of canon-gap G4's "Missing" list and exit is taught: lessons 7 to 9, 13 to 17, 19 to 21, 24 to 30 and the exit work; reproducible pipelines (environments, seeds, data versions) are taught in 2.3 level RM6, lessons 31 to 36, which stays in 2.3, as the coverage check says. Quiz counts recounted: 131 items, choice 49 of 128 (IS 17 of 44, AU 18 of 48, RP 14 of 36). The 0.6 mapping matches `stage1-finance-projects.md`'s lesson numbers.

**Citations (15 searches).** Confirmed [searched]: AFML 11.1 to 11.6 by title, 11.6 "Strategy Selection", 14.7.1 to 14.7.4; Bailey and López de Prado, Journal of Risk 15(2), 3 to 44 (2012); the DSR, JPM 40(5), 94 to 107; "Pseudo-Mathematics", Notices of the AMS 61(5), 458 to 471; Kapoor and Narayanan, Patterns (2023), 294 papers in 17 fields, arXiv 2207.07048; Henderson and others, AAAI 2018, arXiv 1709.06560; Pineau and others, JMLR 22(164), free; Bouthillier and others, MLSys 2021, arXiv 2103.03098; Reinhart's 12 chapters (2, 4, 9 and 12 now cited by number and title); Chan, 2nd ed (2021), chapter 3 "Backtesting" with "Common Backtesting Pitfalls to Avoid"; Shumway, JF 52(1), 327 to 340; AsPredicted's nine questions; the protocol's research-culture and model-complexity categories. Corrected: AU1's AFML range (11.3 to 11.5 became 11.2 to 11.5, since the flawless-backtest section is 11.2) and the protocol's "costs" heading, which is not one of its seven categories. Added: Shumway and Warther (1999), Nasdaq near $-55\%$. Still [check]: the seven sins' placement in 11.2; chapter 13's section numbers; the protocol's other category names and where its cost questions sit; Henderson's section titles; public AFML solutions (none official found); AsPredicted's current wording. Not searched, kept [recalled]: Dodge and Recht arXiv numbers and the remaining journal volumes. Nothing was found to be invented, so nothing was deleted.
