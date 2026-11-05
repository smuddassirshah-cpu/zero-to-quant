# Zero-to-Quant: second review, consolidation and course-correction brief

```yaml
document_type: consolidated_second_review_and_course_correction
repository: smuddassirshah-cpu/zero-to-quant
branch: claude/amazing-wright-d4mx7i
reviewed_commit: f9a4545573e3c2a5ba4ffd1e2d2a79610ebe4b4a
head_at_review: f9a4545573e3c2a5ba4ffd1e2d2a79610ebe4b4a   # identical to the first review's snapshot; no divergence
review_date: 2026-11-05
consolidates: zero-to-quant-curriculum-review-agent-brief.md (first review, same commit)
review_mode: read_only
repository_mutations_performed: none        # git status clean after the review
clone_status: shallow clone of the branch succeeded
validator_run: yes, on a scratchpad copy of app/ only (0 errors, 610 warnings); the repo copy of manifest.json was not touched
playthrough_run: no
evidence_base: all 79 course maps; curriculum.json and manifest.json; every authored lesson (1054), review (244), homework (245), exam (41) and bank (21) file parsed by script; prereq.js, state.js, review.js, longform.js, today.js, learn.js, prepare.js, exam.js, player.js read; state files and docs read
sampling_note: the quiz-format and duration findings below are exhaustive counts, not samples
```

Receiving agent: this file is a brief, not an authorisation. Act on it only under the user's then-current instruction. Verify each line against HEAD before changing anything. Preserve the three categories used throughout: observed source fact, educational judgement, proposed remedy.

## 1. Verdict

The first review's primary conclusion stands and is strengthened. The app is a strong teaching framework whose evidence of learning is weak: every mechanism that marks a learner as having "met" or "mastered" something is either a short recognition quiz, a 70% review, a self-tick, or a topic exam that unlocks far more than it tests. The first review inferred this from a 46-lesson sample. The counts below show it is structural and complete.

Second conclusion, new here: the project's own state files are not a reliable record. Dates run ahead of the clock, KNOWN_ISSUES carries stale figures, and PLAN.md already lists several of the first review's findings as known. A course correction must start by making the state files tell the truth, or the next twenty sessions will keep closing tasks that are not closed.

Third conclusion: breadth expansion (2b pure maths, remaining 2a mocks, drill packs) should pause until assessment validity is fixed. Adding 160 more lessons to a system that cannot tell guided completion from independent competence adds cost without adding evidence.

## 2. Disposition of the first review's findings

| ID | Disposition | What the second review found |
|---|---|---|
| F01 Readiness not operationalised by role | Confirmed | `today.js:85` `currentCourse` picks by curriculum order and start stage only; no role input. `docs/curriculum.md:292` upgrades finance basics from optional to required for traders and researchers. `prep.json` has 23 role and firm paths but Today ignores them. |
| F02 Dependencies larger than the competence they protect | Partially confirmed; partly a recorded user decision | Edges verified exactly (`coding-int/L1` needs `graphs-dp/L4, algo-think/L3, contests/L3`; `systems/L1` needs `cpp-pricing/L3`). Closures recomputed: trader superday 107 levels, 35 courses, 470 lessons; researcher superday and quant-data OA 89 levels, 32 courses, 375 lessons; coding OA 38 levels, 16 courses, 163 lessons. `DECISIONS.md:78` records that the user chose a solid foundation and kept these closures. The remedy therefore narrows to edge-level rationale and targeted diagnostics, not to shrinking the map. The trader closure pulling in `ds`, `graphs-dp`, `algo-think`, `contests`, `integrals` and `multivar` has no written rationale and should get one or be cut. |
| F03 Advanced content depends on unwritten prerequisites | Confirmed | `pdes/L1` requires `odes/L4`; `pdes/L3` requires `numerics/L4`; both courses have 0 of 18 and 0 of 17 lessons. Under Strict mode (default on, `state.js:40`) an unwritten level can never be met (`prereq.js:86-93`), so the PDE route is unreachable without switching Strict off. 21 further `requires` edges point into unwritten courses; the validator warns on 23 (`"has no written lesson yet"`). |
| F04 Quiz format does not assess the stated performance | Confirmed, upgraded from sample to exhaustive | Across all 1054 lessons the quiz block holds 4136 items: 2189 `choice`, 1895 `numeric`, 27 `multi`, 20 `expression`, 4 `order`, 1 `table`. Zero `code`, zero `longform`. 556 lessons contain `code` screens; none of them feed `mastered`. This is by design: `docs/AUTHORING.md:489` defines a quiz as 3 to 5 scaffold-free short items and `:529` bars `parts` from quizzes. Objective verbs across lessons include `write` 72, `derive` 34, `prove` 34, `build` 50, `explain` 102; none is assessed at lesson level. |
| F05 Aggregate passes and self-marking overstate evidence | Confirmed, with three sharper facts (N01 to N03) | All eight sub-points verified: `MASTERY = 0.8` (`state.js:15`); `quizFinished` queues no redo when mastered (`state.js:235-249`); test-out draws 6 of a review's 8 to 10 items at 70% (`review.js:672-718`, `prereq.js:22-23`); topic pass meets every level of the topic (`prereq.js:86-93`); longform passes at 7 self-ticked points (`longform.js:11`); `mock-oa-code` passes at 0.5 and draws from the 8 `oa` drills the library lists (4 at difficulty 3, 4 at difficulty 4, so each sitting shows a quarter of the pool); only `stage-0.json` exists. |
| F06 Guided projects do not establish independence | Confirmed | `alpha/l16-research-note.json` supplies the pipeline and asks for gaps to be filled; `momentum-rep` is 5 of 15, `pairs-rep` 0 of 15. No mechanism records an out-of-app project. |
| F07 Short-lesson packaging strains advanced learning | Confirmed and quantified | Every one of 1054 lessons carries `minutes` between 11 and 15 (median 14). 13 lessons state a different duration in their opening prose by 5 minutes or more, 10 of them in `research-int`, `coding-int` and `contests`: `coding-int/l15` 13 vs 60, `contests/l13` 15 vs 60, `research-int/l14` 15 vs 50, `research-int/l3` 15 vs 35. The interview courses are the ones squeezed hardest. |
| F08 Explanatory precision | Confirmed; three further examples found (N05) | Both cited lines verified verbatim (`ito/l1:904`, `pdes/l1:1194`). |
| F09 Workload representations disagree | Confirmed; KNOWN_ISSUES is itself stale on this | Sum of topic hours 555/1650/940/550 = 3695; stored stage hours 515/1400/800/550 = 3265; `learn.js:154` sums the stored fields. `KNOWN_ISSUES.md:10` still says the header reads 3,100 against a curriculum of 3,530. Three different totals in three places. |

## 3. New findings (second review)

### N01. Self-marked and verified results are indistinguishable in the skill model

Type: verified implementation fact. Priority: P0, part of F05.

`state.js:97` `rate()` updates each skill's Elo and mastery points from `ok` alone. A longform item ticked to 7 of 10 by the learner arrives as `ok: true` with no flag. The You screen's mastery map (`you.js:103-144`) therefore reports self-assessment as mastery. `homeworkSubmitted` stores `selfMarks` as an aggregate only; the per-item results carry no provenance. The mock "checks" (`no-lookup`, `game-aloud` requiring a real counterparty, `story-aloud`) are the same class of evidence: a tick box.

Acceptance: every graded result carries a provenance field (`auto`, `self`, `external`); the mastery map, prerequisite met rule and any readiness summary either exclude `self` or display it separately; a self-tick never counts toward a prerequisite.

### N02. The review pass is the main "met" mechanism and is lower than the quiz bar

Type: verified implementation fact. Priority: P0, part of F05.

No review file sets `pass`, so every review passes at the default 0.7 (`prereq.js:22`, `state.js:256`). Reviews hold 8 to 10 items (66 at 8, 121 at 9, 56 at 10), so a level is met at 6 of 8, 7 of 9 or 7 of 10, once, and `passed` is sticky (`state.js:267`). A level with no review is met by finishing its lessons (`prereq.js:86-93`), and a lesson is finished after every screen has been checked or revealed (`player.js:758-764`); the Solve button is available on every screen including code. So the lowest path to "met" is: reveal every screen, score 80% on 4 recognition items, score 70% on 9 review items.

Acceptance: met requires an essential-skill floor (each skill in the level at or above a stated share), not an aggregate; a lesson in which more than a stated share of screens was revealed does not count as done for prerequisite purposes; the review pass share is set per level in the file, not defaulted.

### N03. Topic exams unlock far more than they test

Type: verified data fact. Priority: P0, part of F05.

A pass is 70% of at most 30 items (`exam.js:97` default; every topic exam sets 0.7). What that pass meets: topic 1.5 (probability, the single most interview-relevant topic) 21 right of 30 meets 22 levels and 99 lessons; topic 3.3 (interview) 21 of 30 meets 19 levels and 96 lessons; topic 1.3 21 of 30 meets 17 levels and 69 lessons; topic 0.3 18 of 25 meets 12 levels and 52 lessons. The validator caps topic exams at 30 items, so this cannot be fixed by adding items.

Acceptance: a topic pass meets a level only when that level's skills were each covered and answered at a stated floor; or the topic pass stops being a met rule and becomes a badge.

### N04. Prep paths advertise mocks that do not exist; two roles have no superday mock at all

Type: verified data fact. Priority: P1, part of F01.

`prep.json` references 15 mock ids with no file: `mock-video` (general, oa-research, oa-strats and four firm paths), `mock-oa-strats`, `mock-superday-strats`, `mock-superday-developer`, `mock-oa-code-hard`. `prepare.js:116-122` renders these as "Not yet written", so there is no dead link, but the developer and strats roles have no final-round mock and no path has a behavioural mock. Pair with F01: the role contract must say which mocks exist.

### N05. Three further precision defects in interview-critical summaries

Type: specific mathematical findings. Priority: P1, part of F08.

- `ito/l13-martingale-or-not.json:1044`: "A smooth f(t, W_t) is a martingale exactly when its drift f_t + ½f_xx is zero." Zero drift gives a local martingale; the lesson never mentions integrability or the word "local". An interviewer will ask.
- `ito/l17-derivation-aloud.json:882,883,900`: "The equation holds for any claim." The Black-Scholes equation as derived holds for European claims on one underlying with payoff at T; path-dependent and American claims need more. The lesson's objective is a five-minute spoken derivation, so this is exactly the follow-up a panel would use. The file mentions none of European, American, Asian, barrier or path-dependent.
- `random-vars/l5-long-run-average.json:4030`: "Averaging the values without their chances agrees with E[X] only when the pmf is symmetric." False: it agrees for any uniform pmf (values 0, 1, 10 at a third each). The word "only" is wrong.

Acceptance as F08: a separate mathematical read of every `summary` in ito, measure-prob, pdes, markov, limits-thm, random-vars and research-int, checking each "only", "exactly when", "any", "always", "never" against a counterexample search. The script that produced this list is trivial (grep those words in `summary.ideas`, `summary.trap`, `summary.formula.note`); it returned about 180 candidate lines in 21 courses.

### N06. The state files do not tell the truth

Type: verified process fact. Priority: P0, precondition for everything else.

- Session labels run ahead of the clock: PLAN.md and PROGRESS.md carry "done 6 Nov" against a HEAD committed 5 Nov 03:05 UTC; `KNOWN_ISSUES.md:85` admits the container clock read 3 Nov while labels ran to 6 Nov. Any "as of" claim in these files is unreliable.
- `KNOWN_ISSUES.md:10` quotes an hours header (3,100) and curriculum total (3,530) that match nothing in the current source (3,265 and 3,695).
- PLAN.md has duplicated tick lists (section 3 repeats 2a; section 4 item "topic-0.1 to 0.5" is ticked and its text says "never written"). Several items are ticked with a parenthetical saying part of the work is still open.
- `KNOWN_ISSUES.md:9` still says topics 3.x have no topic exams; 3.2, 3.3 and 3.5 now do.

Acceptance: one pass that reconciles PLAN, PROGRESS, KNOWN_ISSUES against source by script (lesson counts, exam list, hours), stamps every state-file date from `git log`, removes the duplicate tick lists, and records this review's findings as open items with their ids.

### N07. The authoring standard itself forbids the assessment the objectives need

Type: observed source fact, root cause of F04. Priority: P0.

`docs/AUTHORING.md:489` ("Quiz: 3 to 5 items, difficulty 2 to 3, one attempt each, scaffold-free") and `:529` ("never a quiz item") mean no content agent can write a lesson whose mastery depends on code, proof or explanation, however the objective is worded. Fixing lessons one at a time will not help while the standard produces the defect. The fix is a standard change first (a `demonstrate` block or a per-level performance task whose pass is required for `mastered` or for met), then content.

### N08. Drill verification is the only independent coding evidence, and it is outside the met rule

Type: observed source fact. Priority: P1, part of F04 and F06.

`state.js:421` records a drill as `verified: true` only when its hidden tests pass. That is the one place the app holds an auto-graded, unseen-input coding result. It feeds no prerequisite, no mastery map cell and no readiness summary. 35 non-sample drills exist (10 `ci-`, 6 `rq-`, 3 `sy-`, 8 `oa`, 8 untagged). Reuse it: a coding level's met rule could require k verified drills from its pack.

## 4. Course-correction order

Dependency-ordered. Each item names the acceptance evidence and who can produce it. Nothing here is closed by adding lesson files, raising thresholds, changing copy, or rerunning authored-answer playthroughs.

| # | Work | Closes | Acceptance evidence | Who |
|---|---|---|---|---|
| 1 | State-file reconciliation (N06). Script `app/tools/` or `docs/reviews/` that prints lesson, review, homework, exam, drill, bank counts and hours from source; PLAN, PROGRESS, KNOWN_ISSUES corrected to it; dates from `git log`; this review's ids entered as open items. | N06, F09 part | Script output equals the figures in section 2 of the first review; no state-file figure disagrees with source. | Agent |
| 2 | Readiness contract per role (F01, N04). One file `docs/readiness.md` or `content/readiness.json`: for trader, researcher, developer, strats and derivatives, the independent tasks that count, the required, recommended and optional courses, the mocks that exist and the ones that do not. Today reads the chosen role. | F01, N04, F09 part | A fresh profile with role = trader is never shown `graphs-dp` as next work unless the contract lists it as required; the Learn header shows one total that equals the contract's sum for that role. | Agent writes; user signs off the contract |
| 3 | Result provenance (N01). `results[]` rows carry `how: auto, self, external`; `rate()` stores Elo per provenance or excludes `self`; You shows self-marked separately; prerequisite met ignores `self`. | N01, F05.5 | A homework with only longform items cannot change a prerequisite or a mastery-map cell; the You screen labels it. | Agent |
| 4 | Met rule rewrite (N02, N03, F05.1 to .4). Essential-skill floor per level; revealed-screen cap for `done`; topic pass meets a level only on covered skills; missed quiz items always queue; per-level `pass` written into every review file. | F05.1 to .4, N02, N03 | Unit tests on `prereq.js` and `state.js` for each rule; playthrough `--routes-only` still green; a scripted learner who reveals every screen and scores 4 of 5 on quizzes ends with zero levels met. | Agent |
| 5 | Authoring standard change (N07). Add a per-level performance task kind (code with hidden tests, proof or derivation from a blank start with external mark, spoken prompt with external rubric) that the met rule can require. Document in AUTHORING section 5 and 11 before any content uses it. Scope decided 5 Nov (see the course-correction prompt, "Performance tasks"): verb rule, not every level; about 110 written levels; Stage 0 excluded except the two code courses; the validator applies the rule from objectives. | F04 root cause | Validator accepts and checks the new kind and errors on a rule-matched level without one; the met rule can reference it; one level in each of `coding-int`, `ito`, `proof` and `research-int` carries one as a pilot. | Agent |
| 6 | Holdout and resit integrity (F05.6, .7). `mock-oa-code` draws from a pack the library hides until sat, or unseen-first by solved state; every mock that has fixed versions names all versions in `prep.json`; pass marks reconciled with the curriculum's own criterion (two problems in 60 minutes) and the file says whether the mark is illustrative. | F05.6, F05.7 | A learner who has verified all 8 `oa` drills sees a "previously seen" label on the mock; sitting the mock twice never repeats a problem while the pool allows. | Agent |
| 7 | Dependency rationale pass (F02, F03). Every `requires` edge that crosses courses gets a one-line reason in `course.json` (`why`); edges without a defensible reason are cut or replaced by a diagnostic; the trader closure is re-run and reported; routes into `odes` and `numerics` are either authored or marked as route limitations on Learn and Prepare. | F02, F03 | Closure report in `docs/reports/`; no edge without `why`; Learn shows "route limited: X unwritten" on pdes. | Agent; user decides whether `odes` and `numerics` are written before 2b |
| 8 | Independent capstone (F06, N08). A capstone record per role: repo link, reviewer, date, rerun-from-clean result, defence notes. Research route's capstone is the replication course or an explicitly equivalent external project. Drill verification counts toward coding levels. | F06, N08 | The readiness summary cannot show "ready" without a capstone record marked `external`. | Agent builds the record; a human reviewer fills it |
| 9 | Precision read (F08, N05). Scripted candidate list over `summary` fields in the seven courses named in N05; each candidate judged with a counterexample attempt; fixes applied with the fix-pass rule (grep the old value). | F08, N05 | `docs/reviews/review-precision-3.2.md` with one row per candidate; the five known lines fixed. | Agent with a maths second reader |
| 10 | Duration honesty (F07). Lessons whose prose duration disagrees with `minutes` get a `session` field (`short`, `workshop`, `project`) and a true estimate; the validator warns on disagreement. | F07 | Zero disagreements over 5 minutes; interview courses show workshop length on their cards. | Agent |
| 11 | Workload single source (F09). One function computes hours per lesson, level, topic, stage and role from the contract in item 2; `curriculum.json` stage `hours` removed or derived; `docs/curriculum.md` quotes the script. | F09 | Learn header, stage cards, curriculum.md and prep paths agree to the hour. | Agent |
| 12 | Pilot (first review section 6, item 7). Two to three GCSE-entry learners through Stage 0 and one interview path; observe stalls, delayed retention, an unseen problem, an explanation aloud, one out-of-app task. | All, as evidence | A written pilot report; no end-to-end effectiveness claim before it exists. | Human |

Freeze until items 1 to 5 are done: no new 2b pure-maths levels, no new drill packs, no new mocks except as pilots for item 5. Appended levels already briefed (trees L4, cpp L5) may continue because they are interview-critical and small.

## 5. Constraints for the receiving agent

- Read-only passes must not run `node tools/validate.mjs` inside the repo: it rewrites `content/manifest.json`. Copy `app/` to the scratchpad first, as this review did.
- Do not trust dates in PLAN, PROGRESS, KNOWN_ISSUES or `docs/reviews/answers-*.md`. Use `git log`.
- Do not cite "0 errors" as evidence of correctness. The validator checks schema and keys, not definitions, generalisations or whether a quiz measures an objective.
- Do not reduce F02 to "turn Strict off". `DECISIONS.md:78` records the user's choice; the remedy is rationale per edge and diagnostics, not removing gates.
- Never rename or remove a lesson id (`CLAUDE.md`); progress keys on it. Add fields and levels instead.
- Keep the first review's strengths S01 to S04 intact: concrete foundations, the lesson shape, the probability and research-hygiene content.
- Every number in this file was computed from source at the reviewed commit by script. The scripts are reproducible from the descriptions in section 3; re-run them at HEAD before quoting a figure.

## 6. Evidence index

Engine: `app/js/state.js:15,40,97,235-249,256-268,421`; `app/js/prereq.js:22-23,75-93`; `app/js/screens/review.js:672-718`; `app/js/engine/widgets/longform.js:11`; `app/js/engine/player.js:758-764`; `app/js/screens/today.js:85`; `app/js/screens/learn.js:154`; `app/js/screens/prepare.js:116-122`; `app/js/screens/exam.js:97`.

Content: `app/content/curriculum.json` (stage and topic hours); `app/content/prep.json` (mock ids); `app/content/exams/*.json`; `app/content/drills/oa-*.json`; `app/content/courses/{coding-int,systems,pdes,ito,measure-prob}/course.json` (`requires`); `app/content/courses/ito/l1-walk-to-bm.json:904`; `ito/l13-martingale-or-not.json:1044`; `ito/l17-derivation-aloud.json:882-900`; `pdes/l1-equations-in-two-variables.json:1194`; `random-vars/l5-long-run-average.json:4030`.

Docs and state: `docs/AUTHORING.md:28,489,529`; `docs/curriculum.md:292`; `DECISIONS.md:78`; `KNOWN_ISSUES.md:9,10,85,106`; `PLAN.md` sections 2a, 2b, 3, 4.

First review: `zero-to-quant-curriculum-review-agent-brief.md`, sections 2 to 8, including its external references E01 to E05, which this review did not re-verify.

## Verification at HEAD

```yaml
verified_on: 2026-11-05
head: 1e67d6f4bf7d6e6fee339592b6481a9e8dd0a116   # 8 commits after f9a4545
divergence: cpp level 5 fix pass (cpp l19 to l23, review-5, homework-5), exam topic-1.9, cpp briefs, state files; no file under app/js changed
method: engine lines read at HEAD; content figures from app/tools/census.mjs and docs/reviews/verify-course-correction.py; validator run on a scratchpad copy of app/ (0 errors, 610 warnings)
repository_mutations: this section, the two scripts, state files (see PLAN 2c item 1)
```

Categories kept apart: **Fact** (observed at HEAD), **Judgement** (educational reading), **Remedy** (the review's proposal; unchanged unless stated).

| ID | Disposition | Evidence at HEAD |
|---|---|---|
| F01 | Confirmed, sharper | Fact: `app/js/screens/today.js:85-93` `currentCourse` uses resume, `startStage`, curriculum order and tested-out state only. `state.js:20` `TRACKS` is Trader, Researcher, Developer, Undecided; `profile.track` is validated and echoed (`state.js:485,555`) and read by no screen for routing. There is no strats or derivatives role at all, so the five-role contract in item 2 needs new track values. `docs/curriculum.md:292` and 23 prep paths confirmed. |
| F02 | Partially confirmed (as the review says) | Fact: `coding-int/L1` requires `graphs-dp/L4, algo-think/L3, contests/L3`; `coding-int/L4` requires `coding-int/L3, contests/L4`; `systems/L1` requires `cpp-pricing/L3`. Closures reproduced exactly with implicit previous-level edges and `lessonRequires`: trader superday 107 levels, 35 courses, 470 mapped lessons (includes ds, graphs-dp, algo-think, contests, integrals, multivar); research superday and quant-data OA 89, 32, 375; mock-oa-code 38, 16, 163; L1 closures research-int 61, systems 55, coding-int 27, puzzles 27, brainteasers 7, matching `DECISIONS.md:78`. Judgement: the user's decision stands; the missing piece is a written reason per edge. |
| F03 | Confirmed | Fact: `pdes/L1` requires `odes/L4, ito/L3`; `pdes/L3` requires `pdes/L2, numerics/L4`; odes 0/18, numerics 0/17. Mechanism: `prereq.js:87-92` meets an unreviewed level only when every mapped lesson is written and finished; no topic-1.11, topic-2.5, stage-1 or stage-2 exam exists; test-out of such a level returns "no written review to test out with. Finish its lessons instead" (`screens/review.js:690`), which is impossible. Validator on the copy: 23 "has no written lesson yet" warnings, 21 besides the two pdes edges. Counting implicit previous-level edges gives 30, of which only the two pdes edges leave a written level. |
| F04 | Confirmed, exhaustive | Fact: 1054 lessons, 4136 quiz items: choice 2189, numeric 1895, multi 27, expression 20, order 4, table 1; no code, no longform. 556 lessons have a code screen. `mastered` is the quiz share only (`state.js:246-248`). Objective first words: write 72, derive 34, prove 34, build 50, explain 102 (also implement 16, design 5, justify 1). `docs/AUTHORING.md:489` and `:529` verbatim. |
| F05 | Confirmed, all eight | Fact: 1 `state.js:15`. 2 `state.js:249` queues no redo when mastered. 3 `prereq.js:23` `TESTOUT_N = 6`; need `ceil(6 x 0.7) = 5` (`review.js:700`); unseen-first within the review (`review.js:695`). 4 `prereq.js:89`. 5 `longform.js:11` `PASS = 7`, and `longform.js:28` tells the learner "your mastery map trusts this mark". 6 `mock-oa-code` paper `pass: 0.5`, description "You pass the paper with one problem of the two". 7 eight `oa` drills, 4 at difficulty 3 and 4 at 4, all Python; the paper draws one of each. 8 `stage-0.json` is the only stage exam. |
| F06 | Confirmed | Fact: `alpha/l16-research-note.json:899` "fill the four gaps"; momentum-rep 5/15, pairs-rep 0/15; no state field or screen records an out-of-app project (`grep capstone app/js` is empty). |
| F07 | Confirmed in substance; count not reproduced | Fact: `minutes` 11 to 15, median 14, all 1054. The four cited pairs reproduce (coding-int/l15 13 vs 60, contests/l13 15 vs 60, research-int/l14 15 vs 50, research-int/l3 15 vs 35); coding-int/l19's objective is a 45-minute round in a 15-minute lesson. A narrow pattern finds 8 lessons, a broad one 24 with puzzle numbers mixed in; neither gives 13. Item 10's validator rule must define the pattern. |
| F08 | Confirmed | Fact: `ito/l1-walk-to-bm.json:904` "anything bigger blows it up"; `pdes/l1-equations-in-two-variables.json:1194` verbatim. Judgement as the first review. |
| F09 | Confirmed | Fact: stored stage hours 515, 1400, 800, 550 = 3265; summed topic hours 555, 1650, 940, 550 = 3695 (census); `learn.js:154` sums stored fields; `KNOWN_ISSUES.md:10` quoted 3,100 and 3,530 (corrected this session). |
| N01 | Confirmed | Fact: `state.js:97-106` `rate()` takes `ok` only; `homeworkSubmitted` keeps `selfMarks` as one aggregate (`state.js:285-295`); 259 `longform` widgets, all in homework (0 in lessons, 0 in reviews). Self-ticked mock checks exist: `no-lookup` in three mocks, `story-aloud` (research superday), `game-aloud` (trader superday). |
| N02 | Partially confirmed; the gap is wider than stated | Fact: 243 reviews, none sets `pass` (sizes 8: 66, 9: 121, 10: 56); default `prereq.js:22`; sticky `state.js:267-268`. Disputed detail: the "lowest path" is wrong twice. (a) The "no review, finish the lessons" path (`prereq.js:91`) is vacuous at HEAD: every fully written level has a written review. (b) Quiz mastery is not on the met path at all: `itemLocked` (`prereq.js:127-135`) locks a review only through its level's `requires`, not lesson completion, so a learner can sit the review cold and meet the level at 6 of 8, 7 of 9 or 7 of 10 with no lesson opened; test-out meets it at 5 of 6 from the same review. Revealed screens go to Redo (`player.js:766`) and the lesson still counts done (`player.js:864`, any quiz score). Remedy adjustment: the revealed-screen cap bites only on lesson references (`prereq.js:100-104` needs done and mastered) and on progress figures; the essential-skill floor on the review is the part that changes met. |
| N03 | Confirmed, exact | Fact: every topic exam passes at 0.7. 0.3: 18 of 25 meets 12 levels, 52 lessons; 1.3: 21 of 30, 17 and 69; 1.5: 21 of 30, 22 and 99; 3.3: 21 of 30, 19 and 96 (`prereq.js:89`). |
| N04 | Confirmed; wording corrected | Fact: five distinct missing mock ids (mock-video, mock-superday-strats, mock-oa-strats, mock-oa-code-hard, mock-superday-developer) in 15 references (7, 4, 2, 1, 1). `prepare.js:116-122` renders "Not yet written". |
| N05 | Confirmed; candidate count not reproduced | Fact: `ito/l13:1044` "exactly when"; the file has neither "local" nor "integrab". `ito/l17` "any claim" at 860, 882, 883, 884, 900; none of European, American, Asian, barrier, path-dependent appears. `random-vars/l5:4030`: values 0, 1, 10 at a third each give 11/3 both ways, so "only" is false. The grep over `summary.ideas`, `trap` and `formula.note` gives 69 lines in the seven named courses and 636 in 70 courses; "about 180 in 21 courses" matches neither. Item 9 starts from the 69. |
| N06 | Confirmed, with the real dates | Fact from first-add commits (UTC): sessions B, C and D, labelled 4, 5 and 6 Nov, committed on 3 Nov (mock-oa-arith 05:49, mock-oa-sig 13:22, topic-3.3 21:30); session E ran 3 Nov 21:30 to 4 Nov 00:28. ito L1, puzzles L1 and mental-pressure L1, logged under 2 Nov, committed 29 Oct. The clock note is `KNOWN_ISSUES.md:86`, not `:85` (session J added lines; `:53` and `:110` likewise for the operating model's `:52` and `:109`). PLAN duplicate lists and the ticked "never written" line confirmed. `KNOWN_ISSUES.md:9` stale: topic exams 3.2, 3.3, 3.5 exist. |
| N07 | Confirmed | Fact: `AUTHORING.md:489, 529`; the validator also refuses `longform` in reviews (`KNOWN_ISSUES.md:51`). Sizing of the decided rule reproduces exactly from lesson-file `objectives`: 111 written levels (Stage 1 63, Stage 2 22, Stage 3 22, Stage 0 4 in first-python and terminal; 21 of the Stage 3 ones in interview courses). From `course.json` `lessonObjectives` it gives 83, so item 5's validator rule must read the lesson files. |
| N08 | Confirmed | Fact: `state.js:419-421`; 35 non-sample drills (ci 10, rq 6, sy 3, oa 8, untagged 8); `prereq.js` never reads `drills`; You shows a verified count only (`you.js:71,304`). |

Net: no finding is already fixed or disputed outright. Two figures are wrong in the review (N02's lowest path, N04's "15 ids"), two counts do not reproduce (F07's 13, N05's 180), and one sizing depends on which objectives the validator reads (N07). Re-run `python3 -I docs/reviews/verify-course-correction.py` and `node app/tools/census.mjs` before quoting any figure.
