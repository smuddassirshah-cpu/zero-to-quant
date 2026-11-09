# Critical review: can this app get a beginner a quant internship?

Reviewer: Fable 5.2, independent of the building sessions. Branch `claude/amazing-wright-d4mx7i` at `7078fac`, 9 Nov 2026. Read-only: no content, engine or tool file was edited. Evidence: `docs/reviews/critical-review-fable-5-2/` (`sampling.md`, `shots/`, `scripts/`).

Read `sampling.md` before trusting anything below. I read 12 of 1,214 lessons in full, sat one mock and most of one topic exam blind, and played four exams and two mocks through the UI. I did not read a complete route end to end, which the brief asked for. The verdict on content rests on a 1% sample plus the project's own audit statistics.

## Executive verdict

**No. Used as designed, the app will not by itself take a GCSE-entry beginner to a quant internship offer on any path, and there is no evidence yet that it takes anyone anywhere, because nobody has learned from it.** What it is: a well-made, mostly correct, interview-shaped practice spine of about 600 hours, sitting inside a 3,695-hour plan whose other 3,100 hours are outside reading that the app links to and never schedules or checks.

For a learner who already has A-level maths or better and a degree in progress, the trader, strats and researcher interview material is good enough to be a main preparation resource. That is a different claim from the one the owner asked about.

| Path | Can the app carry a total beginner to an offer? | For an already-numerate student, as interview prep | Confidence |
| --- | --- | --- | --- |
| Trader | No. Foundations too thin in-app; live games, spoken pressure and the CV screen are outside it | Strong. Content matches what OAs and trader rounds ask; the market-making simulator is real practice | Medium |
| Researcher | No. The role hires on degree and research record; the app cannot supply either | Good on statistics, ML questions and the open case; take-home practice is small | Medium to low |
| Developer | No, and this is the thinnest path: 35 drills against the 150 or more a coding screen needs | Adequate teaching, far too little volume until drill packs land | Medium |
| Strats | No. Widest route (548 lessons), same foundation problem | Good breadth; one OA mock and one superday mock | Low (least sampled) |
| Strats, derivatives | No. Not separately tested: its closure equals strats; `pdes` and `measure-prob` feed no mock | Unknown | Low |

What would change the verdict: (1) a pilot showing two or three real beginners retain Stage 0 and solve unseen problems; (2) the outside-study hours either built into the app or assigned and checked; (3) the concept audit finished on the 240 unaudited levels; (4) spoken, human-marked practice. Items 1 and 4 need people, not sessions.

## 1. Teaching quality

What I found is good. Lessons open with a concrete task before naming a rule, distractors carry the learner's actual slip ("You counted 2 marks, starting with the mark at 0"), each lesson has a trap screen and a transfer to a trading setting, and the voice is plain. `number-sense/l1` is as good a first fractions lesson as I have seen in software. `ito/l4-gbm` teaches mean against median with the right numbers ($\Phi(-0.3) = 0.3821$, $\Phi(0.1667) = 0.5662$, both recomputed). In roughly 150 items read or worked I found no wrong key.

- **1.1 Blocker. In-app volume cannot produce fluency from GCSE entry.** Authored lesson minutes sum to 286 hours (Stage 0: 42; Stage 1: 130; Stage 2: 49; Stage 3: 64). Algebra and precalculus, stored as 380 hours, are 100 lessons, about 22 hours. A beginner does not get from fractions to logarithms, trigonometric equations and binomial coefficients in 22 hours of twelve-minute lessons, however good. The plan knows this (each topic names Khan Academy, OpenStax, Blitzstein) but the app only prints a link on the topic card. No lesson, homework or gate refers to the outside work.
- **1.2 Major. Expected wrong statements remain.** The paused Fable audit found 12 `wrong` findings in 39 levels that had already passed a second read: 0.31 per level. If that rate held, the 240 unaudited levels hold about 74 (the log's own interval implies 40 to 130). Stages 0 and 1 are easier to get right, so the true figure is probably lower, but every route runs through them. `mm-games` and `recruiting`, both trader-critical, are not in the audit log at all.
- **1.3 Minor. Reasoning aloud is taught by recognition.** `recruiting/l12` has the learner tap the better transcript. Producing speech is left to self-marked `aloud` tasks.
- **1.4 Minor.** `stat-learning/l4` screen 5 cites "Lesson 9", against the session W rule that lesson numbers are never cited. `mm-games/l13` is titled "A full game with a partner" and is played against a script.

## 2. Figures and teaching aids

Canvases mostly teach. The area model in `equations/l3` (`shots/equations_l3-opening-brackets-lesson-03-ladder-440.png`), the unequal bar in `number-sense/l1` screen 7, the base-rate slider in `conditional/l8` and the 20 seeded paths with mean and median in `ito/l4` each carry the idea, and all were legible at 440 px. 81% of screens have a canvas; `table` and `plane` are 43% of them, so the variety is narrower than two dozen kinds suggests.

- **2.1 Minor, distracts.** `trig/l4` screen 3 draws a 30-60-90 triangle on a `plane` with axes ticked 0.5 to 3.0 that mean nothing (`shots/trig_l4-exact-values-lesson-03-problem.png`).
- **2.2 Minor, may mislead.** `mm-games/l6` screen 1 says "the dashed line is your average profit so far"; before any run the only dashed line is labelled "exact" at 0.167 on a "share of plays" axis (`shots/mm-games_l6-edge-lesson-01-explore-440.png`). I did not run the trials to see what appears after.
- **2.3 Minor.** `conditional/l8` screen 1 at 1280 x 860 hides the question under the action bar until scrolled.

## 3. Consolidation

Structure is sound: 4,710 quiz items, 2,512 review items, 2,478 homework items (275 long-form, 136 performance tasks), 29 topic exams at 70%, four stage exams, a redo queue at 7 and 30 days, Leitner-scheduled practice and bank decks. The homework I read (`conditional/homework-2`) is harder than its lessons and its numbers are right. `topic-1.5` is a fair, broad paper.

- **3.1 Major. Alternate mock versions are not unseen.** `mock-oa-sig-2` and `-3` are the same 17 templates in the same order with changed parameters (HH becomes HTH, larger face becomes smaller face, 3 tosses become 4). `docs/readiness.md` counts versions 2 and 3 as "unseen until sat". They test recall of version 1's methods.
- **3.2 Major. The hardest evidence is self-marked.** Performance tasks, long-form items, every spoken answer and the stage-exam checks are ticked by the learner against a rubric. A beginner cannot reliably judge "each line with its reason". These gate levels.
- **3.3 Major. Multiple choice where the real thing is open.** Four of six probability items in `mock-superday-trader` and eleven of seventeen in `mock-oa-sig` offer four options. Recognising 5.7 among four numbers is not producing it aloud.
- **3.4 Minor.** Reviews hold 8 to 10 items yet a review pass tests a learner out of a level (known: `review-size-audit.md`). The "GCSE Higher style paper" in `stage-0` is 20 one-step items with no geometry, statistics or multi-step problems; the label overstates it. Spaced practice reuses items the learner has seen and is opt-in. `topic-1.5` item 4 ("a friend says at least one is a 6") uses the announcement protocol the `conditional` course itself warns is ambiguous.

## 4. Path readiness

Closures (`closure.mjs`): trader 432 lessons in 32 courses; researcher 432 in 38; developer 227 in 17; strats and derivatives 548 in 44. Syllabus coverage against real screens is good for trader (expected value, conditioning, ruin, Kelly, market making, 80 in 8, sequences, brainteasers, game theory) and researcher (regression traps, multiple testing, ridge and lasso, leakage, an open case).

- **4.1 Blocker. The headline hours mislead.** Learn says "Trader route: 630 lessons, 1,804 h" (`shots/10-learn.png`). Those lessons are about 150 hours of authored time. A learner who finishes them has not done 1,804 hours of anything, and the app cannot tell whether the other 1,650 happened.
- **4.2 Major. Developer volume.** 35 drills (8 in the OA pool, from which the coding mock draws 2). HackerRank-style screens are passed by people who have solved hundreds. Drill packs 1 to 8 (120 more) are planned and unstarted. Drills are function-style only; no stdin parsing.
- **4.3 Major. Derivatives is a label, not a route.** Topic 3.2 stores 0 hours; no mock reaches `pdes` or `measure-prob`; `mock-superday-strats` itself says stochastic calculus appears "in older reports".
- **4.4 Major, outside the app.** `docs/curriculum.md` says a self-taught CV rarely clears the screen at top firms. Fifteen `recruiting` lessons do not change that. The app is honest here; the owner's question should be too.
- **4.5 Minor.** Every mock is locked behind its full closure ("90 things to finish", `shots/10-exam_mock_superday_trader.png`), so a learner cannot sit one cold as a diagnostic without switching strict prerequisites off.

## 5. Interview and OA preparation

Better than I expected. The `trade` widget runs a quoting game against a scripted counterparty with position limits and card reveals; `mock-oa-arith` generates 80 fresh items with negative marking; the coding mock holds out unseen problems; papers run on their own clocks, forward-only where the real test is. Formats are dated and sourced as "reported".

What it cannot do, and mostly says so: hear the learner (`mock-video` tells them to record on a phone), interrupt, push back, vary the counterparty, or mark reasoning. The readiness contract already requires three stranger-marked mocks and an external capstone before any role reads ready. That is the right rule and the app cannot satisfy it.

- **5.1 Major.** No in-app recording or playback, though the browser can do it locally. Self-marking a spoken answer from memory is close to worthless.
- **5.2 Major.** Scripted counterparties are learnable; after two sittings the game is known.

## 6. Production process

What works: worktree waves with one course per agent; a merge script with rules; gates that are scripts (validator, voice scan, number recompute, playthrough at two widths); a committed recompute script per level; findings seen three times becoming validator rules; readers who write their own solutions and plant slips; NEXT_PROMPT hand-offs with expected census figures. The state files agree with the census. This is disciplined work.

What lets errors through, and what is wasteful:

- **6.1 Blocker for the goal. The process has optimised internal consistency and never touched a learner.** 137 review files, 704 engine items, a tool that enumerates passing rubric tick sets, and zero observed learning. The pilot is parked as "post-completion, never ticked by a session". Everything in sections 1 to 5 about effectiveness is conjecture until it runs.
- **6.2 Major. The second read is the wrong check for concepts.** Same model family, same brief, same blind spots: the audit found 132 conceptual findings the second reads missed; at its 27-level mark only 4 of 94 had also been found by the earlier read. The mechanical gates catch arithmetic; the blind claim-ledger audit catches ideas. Running both in sequence on everything doubles cost.
- **6.3 Major. Document weight.** Each author is told to read `AUTHORING.md` in full: 212 KB, about 50,000 tokens before writing a word. `BACKLOG-INBOX.md` is 442 KB. Much of AUTHORING is validator-rule narrative no author needs.
- **6.4 Minor.** Audit order (Stages 2 and 3 first) follows difficulty, not use. `alpha` or `topology` being right matters less than `conditional` being right.
- **6.5 Minor.** Sonnet fix passes on conceptual findings were already overruled for audit fixes; make that the rule everywhere a key changes.

## Ten changes, ranked by value for the owner's goal

| # | Change | Effort |
| --- | --- | --- |
| 1 | (Declined by the user, 9 Nov: stays post-completion so it does not delay the build.) Run the pilot on Stage 0 topics 0.1 to 0.2 with one or two real beginners (the owner counts as one for interview courses). Record stalls, a one-week delayed test, one unseen problem | 2 to 3 weeks elapsed, human; half a session to prepare the protocol |
| 2 | Show in-app hours apart from outside-study hours on Learn, stage cards and `readiness.md`; stop presenting 1,804 h as the route | 1 engine agent, under a day |
| 3 | Resume the Fable audit in closure order: `mm-games`, `recruiting`, then topic 1.5, then the remaining trader and developer closures; optional Stage 2 and 3 courses last | 240 levels; several sessions |
| 4 | Make the outside work real: per level, a named chapter and problem range with a self-ticked log, or generated fluency drills for Stage 0 algebra in the manner of the arithmetic generator | Generator: 1 engine pass plus content; assignments: 1 wave |
| 5 | Drill packs for the developer route first (OA and coding-interview patterns, Python and C++), with a stdin-style variant; then the rest of Phase 4 | 4 content agents, 1 to 2 sessions |
| 6 | Rewrite mock versions 2 and 3 (`sig`, `trader`) on new templates; add a `fresh-check` rule for same-template items across versions | 4 content agents, 1 session |
| 7 | Local recording and playback beside the rubric for every `aloud` item and `mock-video` (MediaRecorder, nothing leaves the browser) | 1 engine agent, 1 to 2 days |
| 8 | Convert superday and SIG probability items from four options to numeric or long-form with follow-ups | 1 content agent |
| 9 | Replace the second read with the blind audit for all new content; split AUTHORING into an author's core (under 40 KB) and a rules reference | 1 session |
| 10 | Give derivatives its own mock reaching `ito`, `pdes` and `trees`, or drop the sub-route label; store real hours for 3.2 | 1 content agent plus second read |

## Why NEXT_PROMPT changes

Phase 4 stays first but starts with developer drill packs (4.2). The audit restart stays but is reordered by route use (6.4, 1.2). Two items are added ahead of bank part 2: the hours display (4.1) and fresh mock versions (3.1). The pilot was raised with the user and declined (9 Nov): it stays post-completion, PLAN 2c item 12, and adds nothing to the build. Finding 6.1 stands as a limit on what the finished app can claim, not as a task.
