# Assessment, mastery, scheduling and motivation

> **Appendix to `docs/PLAN.md`.** Moved from `docs/blueprint/work/assessment.md` on 7 October 2026 and tidied for the blueprint. Section numbers are unchanged, so citations elsewhere still resolve. `docs/PLAN.md` wins where the two differ; this file wins over the widget catalogues and the working papers in `docs/blueprint/work/`. Tidied in place:
>
> | Where | Was | Now |
> |---|---|---|
> | 15.2 item 6 | C++ code possibly sent to Compiler Explorer through the proxy | Dropped: C++ code never leaves the device |
> | 0.3, 17 (runtime tags) | Waiting for the content format's next revision | Settled: `CONTENT-FORMAT.md` decision 18 as tidied removes the tags |
> | Stage names A1 to A15 | This file's numbering | Kept; `docs/PLAN.md` section 11 maps them to its stages |
> | 2.9 (`1.2.exit`), 11.4, 11.6, 15.2 item 5, 18 item 9 | GitHub and Codeforces API lookups on the web app | Withdrawn: paste-verify and manual entries on both targets (`docs/PLAN.md` conflict 5) |

> **Revised by the `docs/PLAN.md` review, 7 October 2026** (its section 13 lists the findings). Section numbers are unchanged.
>
> | Where | Was | Now |
> |---|---|---|
> | Decision 6, 3.5, 2.9, 11.8 | The learner's confirmed long-form mark counts in a gate; real papers self-marked with no evidence | Blind self-marking first; a gate counts $\min(\text{learner}, \text{Bertie})$ per rubric point, with a disputed list resolved by a fresh exit-item sitting; with the tutor off, gate marks stay provisional; real papers are sat typed in the app and marked by Bertie against the official solutions; a `human-mark` confirm on the 1.3 to 1.6 exits |
> | 4.1, 4.3, 5.2, 6.5, 13.6 | 1 or 2 skills a lesson on 1,550 lessons | Skills at level grain (3 to 8 a level, about 1,500 on the path), `introduces` at most 2, step tags with no card, a card budget per topic; load and volumes rerun for 2,044 counted lessons |
> | 10.3 to 10.5, 11.9, decision 17 | Warm Mosteller and Zhou problems in Stages 1 and 2; "recognised and re-solved" counted as cold | `original` problems only before 3.3, `imitates` tags with a CI check, "seen" leaves both counts; warm mode is Bertie after grading; one cold problem a week from 1.5, two from Stage 2 |
> | 3.2, 3.7, 3.8, 7.2, 7.3 | A fixed slot map; unlimited diagnostic sittings; model answers on every result screen; pools of six | Slot order shuffled per form, no method named in a stem, cross-method pools of at least 12, two unlabelled slots per form; one diagnostic sitting per paper; model answers withheld for held-out items after a fail; retention sittings at 3 and 12 months and cumulative Stage 1 and Stage 2 papers |
> | 2.3 to 2.5, 6.3, 8.5 | Nothing inside an item holds the learner back; homework from one level; recognition quizzes; the same prompt as a long-form redo | A planner soft gate per level; homework 25 to 30% from earlier levels and topics, with "which tool?" items from 1.5; a production item on every Prove, Derive or Show lesson; long-form siblings |
> | 5.4, 5.6, decision 26 | Only difficulty 3 maintained; one "Mastered" word for two things | A `core-interview` tier (0.5, 1.5 and the interview patterns, 1.6 on the researcher track) held at 0.90 with stretch cards at 0.80; the lesson star is "Passed" |
> | 3.1 `topic` kind | Long-form at most 30% of marks | Long-form at least 30%, target 40%; at least 30% of marks on applied items with a named trap or edge case; rubrics carry a `consequence` line |
> | 2.7 | Five items credit any skip; retake next day | Two items per skipped level (5 to 20, one at difficulty 4 per level); 3-day cool-down after a second fail |
> | 8.7, 8.8 | Earned hours reach only the estimate share; no reliance figures | Earned hours scale by each item's estimate share; reliance figures, the marking calibration score and the 20% reliance check in the weekly review |
> | 18 item 1, 19 A2 | `db` size probe in A2, writing until `quota_exceeded` | Bounded probe in `docs/PLAN.md` stage 2 |

Blueprint work file, Stage 2 Phase 1. Draft 2, 6 October 2026.

**Draft 2** (same day) keeps every section number of draft 1, because `CONTENT-FORMAT.md`, `AI-TUTOR.md`, `ARCHITECTURE.md` and the seven curriculum files in `docs/curriculum/` cite them. It reconciles this file with the papers written after draft 1 (those four, `canon-gap.md`, `BERTIE.md`) and with `spikes/README.md`; re-reads the `db`, `user` and `downloads` contracts in full, which changes what the friends board can promise; re-runs the FSRS measurements; and fixes four defects found on a second reading. Section 0.4 lists every change and its reason.

**Scope.** Everything that decides what the learner is tested on, how a result becomes knowledge about the learner, what comes back for review and when, how a week is planned against the path (3,100 hours today), and what keeps the learner going without lying to them. For one learner (the owner), and for a few friends later through a shared Artifact. Input to `docs/PLAN.md`: the assessment and progress components, their data model, the privacy block and the execution stages.

**Read for this file.** `docs/curriculum.md` (exit tests, weekly rhythm, rules); `docs/design-research.md` sections 5.4 to 5.9, 6, 7.2 to 7.6, 8.2 to 8.4 and 10; the Stage 1 prototype (`js/screens/exam.js`, `review.js`, `today.js`, `you.js`, `onboarding.js`, `js/data.js`); the sibling work files `CONTENT-FORMAT.md` (sections 3.8, 4.3 to 4.5, 5.4, 7.7, 7.9), `AI-TUTOR.md` (sections 0, 2.2, 2.7, 2.9, 2.12), `widgets-stage0.md` 11.1 to 11.3, `widgets-programming.md` 6.11 and the problem workbench, `widgets-finance-games.md` 8.1 and 8.6; the `db`, `user` and `downloads` capability contracts (version 0.2.69); the owner's lesson-creator skill (final-test protocol) and the project-forge engineering floor. Draft 2 adds `ARCHITECTURE.md` (decisions 10, 11, 14, 15, 26, 27 and section 4.7), `canon-gap.md` (sections 0, 4.4, 5.2), `BERTIE.md` (section 5 states), `CONTENT-FORMAT.md` revision 2 (sections 0.3, 3.2, 5.4), the seven curriculum files (their exit rebuilds, exam blueprints and requests to this file) and `spikes/README.md`.

**Evidence tags**, as in the siblings: [measured] for values measured while writing this file (section 0.2); [sourced] for facts read in a cited source; [our choice] for decisions without outside evidence; [inferred] for deductions; [unverified] for facts not yet checked; [recalled, unverified] for general knowledge not re-checked here. Untagged statements are design rules this file sets.

**How to read it.** Section 0 lists every decision, what this file changes in earlier documents and what draft 2 changed. Section 1 states the principles. Sections 2 and 3 are the assessment ladder and the exam engine. Sections 4 to 6 are the skill graph, the mastery model and the Redo queue. Section 7 is placement and test-out. Section 8 is the weekly plan and progress against the path. Sections 9 to 11 are the daily mental arithmetic, the weekly probability problems and work done outside the app. Section 12 is motivation. Sections 13 to 15 are the data model, export and import, and privacy. Sections 16 to 19 are tests, needs from the other papers, open questions and build stages.

---

## 0. Decisions in brief

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | How an exit test is satisfied | **In-app papers gate; real papers confirm.** Every curriculum exit line becomes one exit part with a named instrument. Where the curriculum names a real paper (GCSE Higher, Khan Academy course challenge, MIT 18.01 and 18.06 finals, Stat 110 finals, Zhou's probability chapter), the learner first passes our fresh in-app paper, then sits the real one and logs it, self-marked against the official scheme | In-app papers only; real papers only | Real past papers are finite and single-use: each can be sat cold once. Our papers are unlimited and fresh, but they are our recreation and could drift from the real standard. Passing ours first spends a real paper only when the learner is likely ready, and the real paper calibrates ours |
| 2 | Homework marking | **Marked when the set is submitted**; no feedback per item before then; code items run their visible examples freely and their hidden tests at submission | Instant feedback per item, as in lessons | A problem sheet tests what the learner can do unaided over a week. Item-by-item feedback turns it into retry-until-green, which the design research names as a critique (section 10) |
| 3 | Exam clock | **Wall-clock timer that survives a reload**, one pause budget of 15 minutes per paper, recorded on the attempt | A timer that pauses whenever the app closes; no pause at all | A crash or a closed tab must not void a three-hour paper; a doorbell is real life. Recording the pause keeps the record honest without enforcement theatre |
| 4 | Fresh resits | **The freshest form plus unseen generator variants from the exam reserve**; CI requires at least 50% of a paper's marks from generator slots, or at least 5 forms | Three fixed forms (the prototype's "new paper next time") | With three fixed forms, a fourth sitting repeats a paper. Generator slots never repeat a parameter point the learner has seen |
| 5 | After a failed paper | **Cool-down (3 days for topic exams, 7 for stage papers) and a remediation set** on the failed skills; the resit unlocks when both are done | Immediate resits; a fixed number of attempts | The curriculum's rule 3: "Marks under the bar mean more problems, not a new book." A short cool-down stops paper shopping; no attempt limit, because the learner is the only stakeholder |
| 6 | Long-form marks in a gate | **The learner marks each rubric point blind; Bertie's marks then appear; a gate counts $\min(\text{learner}, \text{Bertie})$ per point.** A point the learner holds above Bertie goes on a disputed list, resolved by a fresh exit-item sitting on that slot. With the tutor off or failed, a gate's long-form marks stay provisional until Bertie or a person marks them. Outside gates (homework, practice) the learner's final mark after seeing Bertie's counts, with the gap kept as a calibration score. A person marks one finals-style sitting per Stage 1 maths topic (`human-mark`, 2.10) (revised by the `docs/PLAN.md` review) | The learner's confirmed mark (draft 2: "the pass stands"); Bertie's mark alone as the record | Novices over-mark their own proofs [recalled: self-assessment literature], and 40 of the 1.5 paper's 100 marks are long-form, so a self-marked gate could pass with 30 of the 60 auto-marked marks. The lower mark cannot be raised by either party alone; the disputed list and the fresh sitting give an honest learner a way out; the external mark calibrates both |
| 7 | Mastery model | **FSRS-6 (via `ts-fsrs` 5.4.2) per skill and difficulty band**, three bands (core 1 to 2, standard 3, stretch 4 to 5), run with fuzz and short-term learning steps off; due dates computed by this file's tiers, not by the library | Elo; BKT; IRT; Leitner boxes (design research 8.4's provisional pick) | The only family built to fit one learner's own history (its optimiser runs on a single person's reviews); it models forgetting, which a four-year path needs most; bands give it the difficulty axis Elo would otherwise supply. Fuzz would break the fold's determinism, and the library's default 1- and 10-minute learning steps assume flashcards seen several times a day [measured, section 0.2]. Full comparison in section 5.1 |
| 8 | What the mastery map shows | **The chance of solving a fresh standard (difficulty 3) item on the skill today**, as a percentage | An abstract score; points | A number with a testable meaning: the calibration report (section 5.9) checks it against outcomes |
| 9 | Review load | **Retention tiers (0.90 active, 0.85 recent, 0.80 dormant, floor 0.70), plus a `core-interview` tier held at 0.90 for the rest of the path with its stretch cards at 0.80; a weekly load balancer that lowers non-core dormant retention first; redo and organic attempts count as reviews; implicit repetition through `encompasses` edges; review may borrow up to 1 hour a week from Main** | One desired retention for everything; an unbounded queue; letting interview-level skill decay | Rerun by the review at level grain (about 1,500 standard cards plus 124 stretch cards): flat 0.90 needs about 3.2 h a week over the last half-year at 15 h a week; the tiers with the core-interview holds need 2.3 h, plus about 0.5 h of older redo, against a 2 h block with 1 h of borrowing [simulated, section 6.5] |
| 10 | Mastery points against XP | **MP is a ledger of first-try success in unscaffolded work; XP is activity; neither drives the model** | Design research 6.2: "MP drives the per-skill mastery map and review scheduling" | Points only go up; a memory model must be able to go down. Driving scheduling from a ledger would hide forgetting |
| 11 | Redo queue | **Wrong first tries in quizzes, level reviews, homework, exams, weekly problems and textbook sets, plus revealed lesson screens; due 7 and 30 days after the miss; a miss restarts the cycle; generated items come back as a fresh variant at the same level** | Every wrong lesson screen; the identical problem every time | Trap screens are built to be failed and would flood the queue. A variant tests the method, not the remembered answer; authored items without a generator repeat as they are |
| 12 | Placement | **Two short adaptive ladders (maths, at most 10 items; code, at most 4) that set priors only**; completion comes only from exams and exit parts | Placement that marks topics complete | A 10-minute diagnostic cannot carry the weight of a 90-minute paper. Priors with short stabilities get verified by the first reviews |
| 13 | Weekly plan | **Blocks from weekly hours: Mental fixed at 1 h (0.5 h under 8 h a week); Build and Review are the rest times 3/14 and 2/14, each rounded to the nearest quarter hour; Main takes what is left**; alongside items (0.4, 0.5, 1.7, 2.4) take shares in proportion to their hours; track orders are content data | A fixed 9/3/2/1 at every pace | The curriculum gives 9/3/2/1 at 15 h; mental arithmetic is 10 minutes a day whatever the pace. Rounding two blocks and giving the remainder to Main makes the blocks always sum to the goal (draft 1's table did not, section 8.1) |
| 14 | Progress against the path | **Earned curriculum hours** (estimates of completed units) against **spent hours** (measured in-app time plus logged outside work); the ratio is the learner's pace factor and drives the forecast. **The path's length is the learner's track total**, read from curriculum data: 3,100 h today, 3,300 to 3,905 h if the owner accepts `canon-gap.md`'s proposals | Percentage of lessons done; a fixed 3,100 | The curriculum's unit is the hour, and about 83% of the path's hours happen outside lesson screens (textbooks, homework, projects) [counted: lesson time is 17% of the 1,470 hours the seven curriculum files have planned so far]. Tracks are data (`CONTENT-FORMAT.md` 0.3 change 9), and their totals already differ by up to 250 h under the proposals |
| 15 | Mental arithmetic | **"Daily 10"**: a cold 120-second Zetamac-format run (the day's official score), a 3-minute targeted deck, a second run, a 2-minute chain or estimation deck, a summary. The exit counts the **median of the last 7 days' cold scores on a physical keyboard** (at least 5 runs) | Best single score | One lucky run is not a skill. Interview tests are taken on a computer [inferred] |
| 16 | 80-in-8 | **Multiple choice, minus 1 per wrong answer, no skipping, no going back** as the default configuration; free entry as a practice variant; target net 55, then 70 | The Stage 0 catalogue's free entry with Skip | The most commonly reported Optiver format and pass line [sourced from a search summary of quantvault.org and quantt.co.uk; unverified with the firm]. It stays configuration |
| 17 | Weekly probability problems | **Three a week from the start of 1.5: one consolidation, one new pattern, one stretch, all `original` problems before 3.3**; warm mode is hints after a first attempt and Bertie after grading; one of the three is cold from the start of 1.5 and two from Stage 2; all cold in Stage 3 (revised by the `docs/PLAN.md` review) | Random draws; warm until 3.3; recreated book problems before 3.3 | Interleaves patterns, keeps the new one inside what the learner has been taught, fades support towards the cold interview, and keeps the books the 3.3 exit counts unseen |
| 18 | Work outside the app | **Honest self-report with up to 3 evidence links, labelled "self-reported" everywhere**; it earns XP (capped) and hours, can create redo items and satisfy external exit parts; it never earns MP and never updates the mastery model | Ignoring outside work; treating it as verified | The textbook problem sets are most of the curriculum's hours. Keeping them out of MP and the model keeps both calibrated against marked outcomes |
| 19 | Leagues | **No league for one learner.** A **ghost race** against the learner's own recent weeks, ranked on MP. A **friends board** only in a shared Artifact with at least 2 opted-in people who can write to it: weekly MP and hours, no tiers, no demotion. It is a P2 feature, because on a personal plan a friend can save anything only as an Editor invited by email, which also lets them publish the app (section 12.5) | Design research 6.2's 30-person Greek-letter leagues (also in the approved prototype); simulated rivals | A single-user app has nobody to place in a league of 30; simulated rivals would be fiction presented as competition. Beating your own usual week is true and still motivating. The board's cost is an access grant, not code, so it waits until a friend actually joins |
| 20 | Source of truth for progress | **An append-only event log**; every other progress structure is derived by a deterministic fold and can be rebuilt | Mutable progress documents | Merging two devices or two targets becomes a set union; a model change (grade mapping, retention tiers, FSRS version) becomes a rebuild instead of a migration |
| 21 | Writers in the Artifact `db` | **Every document has exactly one writing device**: per-device log chunks and snapshots; a lease for drafts; one writing tab per device, elected with Web Locks (`ARCHITECTURE.md` decision 26) | Shared progress documents; a device id per tab | The store is last-writer-wins with no transactions [sourced: `db.d.ts`]. Single-writer documents cannot lose each other's events; two tabs sharing a device id would collide on `seq` |
| 22 | Sync between the Artifact and the web app | **A sync file with a union merge**: by default only the events the other side has not acknowledged (about 40 KB a week), with a full backup on request; a short **result code** carries a single attempt back to the Artifact when a drill had to run on the web app (C++, a package the Artifact does not ship, or a device that cannot load Python) | A sync server; manual re-entry; full exports every time | The Artifact can reach no host but its own files [sourced: platform facts in the brief], and the web app has no access to the Artifact's `db`. A union of event sets is safe to repeat. A full export reaches about 20 MB after four years (section 13.6), too large to paste on a phone; a week's delta is not |
| 23 | Learning record export | **One self-contained HTML record, plus the CSV tables in one zip** built with `fflate` (already shipped for log packs), through the `downloads` capability | A PDF built in the browser; one download prompt per CSV | `html`, `csv` and `zip` are on the allow-list's second group [sourced: `downloads.d.ts`]; each save asks the viewer once, so one zip beats four prompts; HTML prints from any browser outside the Artifact; no PDF library ships |
| 24 | Study day | **A day runs from 04:00 to 04:00 local**, configurable from 00:00 to 06:00; weeks start Monday 04:00 | Local midnight (design research 6.2, inferred) | A session from 23:30 to 00:30 belongs to one study day; Anki uses the same default [recalled, unverified] |
| 25 | The "no exit test, no next stage" rule | **The planner never schedules the next stage's main work before the exit is passed**; lessons stay open (no locks, design research 7.4), and starting one asks once and records an override | Hard locks | The rule is the owner's; the planner is where it bites. Locks would contradict the approved course map and the "Jump here" flow |
| 26 | When a lesson counts as Passed | **75% of the quiz's marks on the first completion**: 3 of 4, 4 of 5, 3 of 3. The star reads "Passed"; "Mastered" is kept for the delayed FSRS state of section 5.6, and the lesson node shows its first delayed review's result (renamed by the `docs/PLAN.md` review) | 80% (design research 8.2); calling the star "Mastered" | At 80% a four-item quiz needs a perfect score. An immediate quiz measures performance, not learning [recalled: Soderstrom and Bjork 2015], so one word for both would tell the learner they have learned what they have only just seen |
| 27 | Sections inside a paper | **A section may carry its own clock, calculator rule and pass bar.** A timed section closes for good when its time ends or the learner moves on; untimed sections share the paper's clock with a suggested split; a paper passes only when its total and every section bar pass | One clock, one calculator rule and one pass mark per paper | The 0.3 topic exam runs a 40-minute non-calculator section before a calculator section (`stage0-precalc-computing.md` 4.1); the 1.3 paper needs 70% on its 18.01 half as well as overall (`stage1-calculus.md` decision 12) |
| 28 | An exit item inside a paper | **An exit may set a bar on one slot of a paper (`slotMin`), met by any sitting of that paper; a missed slot bar can be retaken alone as an exit-item sitting**: a fresh item from the same pool, the slot's share of the paper's time, Bertie away, a 3-day cool-down | Re-sitting the whole paper for one answer; an untimed take-home | The 1.6, 2.1 and 2.2 exits ask for an explanation at 7 of 10 that the curriculum files put inside the topic exam (`stage1-statistics-ts.md` S8 and T8). Re-sitting a 90-minute paper because one 10-mark answer scored 6 is out of proportion; an untimed retake would lower the bar |
| 29 | Problem sets named by an exit | **Instrument kind `sets`**: named homework sets submitted, and every item below full marks redone correctly once | Logging the real problem sets only | The 1.3 exit names the 18.02 problem sets (`stage1-calculus.md` open item 2). Our sets on the same skills can be checked in the app; the real sets still confirm |
| 30 | Code items and the two targets | **A code item runs wherever the target can provide its runtime**: the drill's `needs` against what the build ships (`ARCHITECTURE.md` decision 15). Python with NumPy and pandas runs in the Artifact; C++ drills never do; anything the Artifact cannot run hands off to the web app and returns by result code | Draft 1: every NumPy or pandas item hands off from the Artifact | The owner's iPhone ran Pyodide 314.0.7 with NumPy 2.4.6 and pandas 3.0.2 inside the Artifact, ready in 5.1 s [sourced: `spikes/README.md`] |
| 31 | Where progress rests in the Artifact | **IndexedDB first, the `db` store as the sync replica, and a setting that turns the replica off** ("Keep my progress on this device only") | `db` only; browser storage only | The owner chose `db` so progress follows the learner across devices; the brief's privacy line says nothing leaves the device except tutor calls. Both hold when the replica is a switch the learner controls and the screen says plainly what rests on claude.ai (section 15.2) |
| 32 | Shared-data rules in the Artifact | **The root is readable at Contributor and writable by the owner only; each viewer writes only their own subtree and their own board entry** | The default root rule, under which every Contributor writes any shared document | The app reads one shared path, `board`. Nothing else should be writable by a friend, and the rule costs nothing [sourced: rule grammar in `db.d.ts`] |

### 0.2 What was executed

**Draft 1**, on 6 October 2026, in a scratch folder outside the repository [measured]:

- `ts-fsrs` 5.4.2 (MIT, published 3 October 2026) installed from npm. It reports "using FSRS-6.0", ships 21 default weights and a default decay $w_{20} = 0.1542$, and implements the forgetting curve $R(t) = \left(1 + \phi\,\frac{t}{S}\right)^{-w_{20}}$ with $\phi = 0.9^{-1/w_{20}} - 1$, so $R(S) = 0.9$.
- 20,000 synthetic attempt events (three quarters with a question snapshot) measured 488 bytes each as JSON and 77 bytes each gzipped (6.3 times). The synthetic text reuses a small vocabulary, so this ratio is an upper bound; section 13.6 plans with 3 times.

**Draft 2**, same day, in a fresh scratch folder with `ts-fsrs` 5.4.2 on Node 22.22 [measured]:

- **Configuration matters.** With the library's defaults, a new card graded Good is due again in 10 minutes, because short-term learning steps (1 and 10 minutes) are on. With `generatorParameters({ enable_fuzz: false, enable_short_term: false })`, first reviews give stabilities of 0.21 days (Again), 1.29 (Hard), 2.31 (Good) and 8.30 (Easy), with intervals of 1, 2, 3 and 8 days; a second Good three days after a first Good gives a stability of 13.8 days. Section 5.2 fixes that configuration.
- **Reviews per card.** A self-consistent simulation (the first review Good; each later outcome drawn from the model's own retrievability at the review; fuzz off; 4,000 cards per setting) counted the reviews after the first over 4 years: 12.7 at retention 0.90, 10.6 at 0.85, 8.8 at 0.80, 6.5 at 0.70. Draft 1 reported 13.2, 10.3, 8.5 and 6.1 without recording its seed or first-review rule; the differences are of the size those two explain. Draft 2's runs use a fixed linear congruential generator (seed 12345 here, 777 for the path runs).
- **Path load.** 1,500 standard cards created evenly over the path, reviews counted after each card's first 90 days (earlier reviews are assumed to come from organic in-topic work: quizzes, level reviews, homework, the topic exam), 3 minutes a review. Results in section 6.5. The script ran in 1.3 s.
- **Counts from the curriculum files** [counted from the documents]: the seven files plan 998 lessons in 186 levels for 1,470 of the curriculum's hours (0.68 lessons and 0.13 levels per hour), 4 quiz items per lesson, homework of 7 to 9 items per level. Sections 6.5 and 13.6 extrapolate from these instead of draft 1's 1,500 to 2,500 lessons.
- **Contracts read in full**: `db.d.ts`, `user.d.ts`, `downloads.d.ts` and `claude.d.ts` (version 0.2.69). New facts used here: an artifact's store is erased when the artifact is deleted; outside viewers never write; an Editor invited by email from outside the organisation writes only while the artifact is not shared by link, and may have no viewer id; `can()` resolves `null` for a viewer from outside the organisation; `zip` is on the downloads allow-list's second group; ordinary saves have no size limit short of 200 MiB on Android [all sourced].

Searches on 6 October 2026 confirmed: GCSE Higher Paper 1 is 80 marks in 1 hour 30 minutes, non-calculator [sourced: Pearson Edexcel 1MA1 summaries]; Higher tier weightings are prescribed by Ofqual and common to all boards, with Algebra 27 to 33% and Geometry and measures 17 to 23% [sourced: search summaries of AQA 8300 subject content]; ts-fsrs implements FSRS-6 with an optimiser available through `@open-spaced-repetition/binding` and `fsrs-browser` [sourced: npm and repository summaries]. The Zetamac, Khan Academy and AQA pages were blocked by the egress proxy, so those facts stay [recalled, unverified].

### 0.3 What this file changes in earlier documents

| Document | Was | Now | Why |
|---|---|---|---|
| `design-research.md` 6.2, prototype `you.js` | Opt-in leagues of 30 in ten Greek-letter tiers | Ghost race; friends board without tiers (section 12.4) | Decision 19 |
| `design-research.md` 6.2 | MP drives the mastery map and scheduling | FSRS drives both; MP is a ledger (section 5.10) | Decision 10 |
| `design-research.md` 8.4, `AI-TUTOR.md` 2.11 fallback | "Elo-style skill score with Leitner intervals of 1, 3, 7 and 30 days" | FSRS-6 per skill and band (section 5) | Decision 7 |
| `design-research.md` 6.2 | Streak day boundary at local midnight | 04:00 local (section 12.1) | Decision 24 |
| `design-research.md` 7.5 | "A downloadable PDF record" | HTML record plus CSV (section 14.4) | Decision 23 |
| `widgets-stage0.md` 11.1 | 80-in-8 with Enter and Skip | Multiple choice, minus 1, no skip, as configuration (section 9.2) | Decision 16 |
| `CONTENT-FORMAT.md` 4.3 | "Every attempt stores a snapshot" | Snapshots for attempts the learner can revisit outside the lesson: quiz, level review, homework, exam, check, weekly, redo, and revealed lesson screens. Correct lesson screens and practice store references only | Size: about 12,000 lesson-screen attempts over the path would carry snapshots nobody reads (section 13.6) |
| `CONTENT-FORMAT.md` 3.2 `Skill` | `requires` only | Adds `encompasses` with weights (section 4.2) | Implicit repetition needs to know which prerequisites a skill exercises, not only which it needs |
| `CONTENT-FORMAT.md` 3.2 `ExitPart` | `external: self-report \| paste-verify \| repo-check` | A full `instrument` union (section 2.10) | Every curriculum exit line needs a named, testable instrument |
| `design-research.md` 8.2 | Lesson quiz at 80% marks the lesson Mastered | 75% (section 2.3) | Decision 26 |
| `CONTENT-FORMAT.md` 3.2 `Exam`, `ExamForm` | Sections with a title and optional minutes; one calculator rule per paper | Sections gain `id` and an optional `calculator`; the paper gains `sectionPass` and `aids` (formula cards); item parts may declare `followThrough` (section 3.1) | Decision 27; the 1.4 and 1.5 papers' follow-through marking and formula card (`stage1-linear-algebra.md` 4.1, `stage1-probability.md` 4.1) |
| `CONTENT-FORMAT.md` 3.2 `Instrument` | Twelve kinds | Adds `sets`; `exam` gains `slotMin`; `rubric` gains `count`; `project` gains `notePredicates` (section 2.10) | Decisions 28 and 29; the `canon-gap.md` 4.4 exit proposals |
| `CONTENT-FORMAT.md` 3.2 `RuntimeTag`, `widgets-programming.md` 2.10 | `micropython-ok` decides what the Artifact runs | The engine's runtime check against `needs` decides (decision 30); a device that cannot load Pyodide hands off, because `ARCHITECTURE.md` decision 15 records the owner dropping MicroPython | `ARCHITECTURE.md` 0.3 drops the tag; `CONTENT-FORMAT.md` revision 2 still lists it, which that paper's next revision settles |
| `stage1-linear-algebra.md` 4.1 | Finals-style paper resit after 3 days | 7 days, as for every finals-style paper (section 3.8) and as the 1.3 and 1.5 files state | One rule per paper kind |

### 0.4 What draft 2 changed, and why

| # | Change | Sections | Source |
|---|---|---|---|
| 1 | Code items run in the Artifact when the build ships their runtime; hand-off and result codes narrow to C++, packages the Artifact does not ship, and devices that cannot load Python | 2.5, 2.9, 3.3, 14.3; decision 30 | `spikes/README.md`; `ARCHITECTURE.md` decision 15 |
| 2 | Paper sections with their own clock, calculator and pass bar; exit bars on single slots with a standalone retake; the `sets` instrument; formula cards as aids; follow-through marking | 2.9, 2.10, 3.1, 3.4, 3.5, 3.6, 3.8; decisions 27 to 29 | Requests in `stage1-calculus.md` (open item 2), `stage1-statistics-ts.md` (section 1, requests), `stage1-linear-algebra.md` 4.1, `stage1-probability.md` 4.1, `stage0-precalc-computing.md` 4.1 |
| 3 | Exit rows for 1.3, 1.4, 1.5, 1.6 and 2.2 updated to the curriculum files, with their `estHours` | 2.9 | The same files |
| 4 | `ExitPart` ids admit digits and dots; tracks are names, not an enum | 2.10 | `CONTENT-FORMAT.md` 0.3 change 5 |
| 5 | The path's length is the learner's track total; `canon-gap.md`'s proposed exit changes are shown to fit the instrument union | 2.9, 2.10, 8.7, 8.9; decision 14 | `canon-gap.md` 4.4 and 5.2; `CONTENT-FORMAT.md` 0.3 change 9 |
| 6 | The friends board is P2 and honest about access; the root of the shared store is locked; deleting the Artifact erases everyone's progress, so the release process never deletes it | 12.5, 13.4, 15.5; decisions 19, 32 | `db.d.ts`, `user.d.ts` read in full |
| 7 | A switch keeps Artifact progress on the device only | 15.2; decision 31 | The brief's privacy line against the owner's `db` decision |
| 8 | One writing tab per device | 13.7 | `ARCHITECTURE.md` decision 26 |
| 9 | `ts-fsrs` configuration fixed (fuzz and short-term steps off); FSRS measurements re-run with a recorded seed | 0.2, 5.2, 6.5 | Re-measured; the default configuration schedules a new card 10 minutes out |
| 10 | Sync files carry only unacknowledged events by default; the learning record is one HTML file and one zip | 14.1, 14.2, 14.4; decisions 22, 23 | Size: a full export reaches about 20 MB |
| 11 | **Defect:** the block table of section 8.1 did not sum to the goal at 5 and 25 hours | 8.1; decision 13 | Recomputed by script |
| 12 | **Defect:** "80% marks the lesson Mastered" meant a perfect score on the four-item quizzes the curriculum files actually set | 2.1, 2.3, 3.6; decision 26 | Counted quiz lengths |
| 13 | **Defect:** redo load and event volumes assumed 2,000 lessons and 400 levels; the curriculum files point to about 1,550 and 285 | 6.5, 13.6 | Counted from the curriculum files |
| 14 | **Defect:** section 2.11 listed Stage 0 content gaps that `stage0-precalc-computing.md` decisions 2 and 3 have since closed (pending the owner's confirmation) | 2.11 | That file |
| 15 | A route that sends C++ code to Compiler Explorer through the proxy is listed among what leaves the device | 15.2 | `widgets-programming.md` decision 9 |
| 16 | Bertie's `celebrate` and `away` states are named where papers start and pass | 3.3, 3.7 | `BERTIE.md` section 5 |

**A conflict with the brief.** The brief for this file states that Pyodide cannot run in the Artifact because the host serves no archives, and that WebAssembly in the Artifact was still being measured. `spikes/README.md` records both as measured on the owner's iPhone on 6 October 2026: every probe check passed except service workers, and a repackaged Pyodide (archives split into JSON maps and `.wasm` files, reassembled in a worker) loaded NumPy and pandas and computed a drawdown correctly. This file follows the measurement, as `CONTENT-FORMAT.md` revision 2 and `ARCHITECTURE.md` do. Both of the brief's outcomes remain covered: everything the Artifact cannot run hands off to the web app and comes back by result code (section 14.3).

---

## 1. Principles

1. **Measure honestly.** Every number on screen has a stated meaning and a test that could prove it wrong. Mastery is a calibrated probability, readiness is an expected score, progress is in curriculum hours, self-reported work says so.
2. **In-app papers gate; real papers confirm** (decision 1).
3. **Evidence attaches to skills, not items** (`CONTENT-FORMAT.md` 4.3), so it survives content edits.
4. **What the learner was told is recorded; what the model believes is derived.** XP and MP awards are stored on the event at the moment they were shown. Mastery, schedules and readiness are recomputed from events and may change when the model improves.
5. **No penalties, no pretending.** Wrong answers never cost XP, streaks or MP (design research 5.7). Nothing is hidden either: a failed paper, an overdue homework set and a review debt are shown plainly, with the next action.
6. **The learner is the only stakeholder.** Integrity measures are records, not enforcement: the app logs pauses, hidden tabs and tutor calls; it does not proctor.

---

## 2. The assessment ladder

### 2.1 Overview

| Layer | When | Format | Help | Attempts | Pass rule | Feeds |
|---|---|---|---|---|---|---|
| Lesson screen | inside a lesson | one task on a canvas | hint ladder after this screen's first Check or 90 s of active input (`trap` screens after a first Check only); Bertie per `AI-TUTOR.md` 2.2 | unlimited; Show solution after 2 | none | XP; Redo only if revealed |
| Lesson quiz | end of every lesson | 3 to 5 items, difficulty 2 to 3; one short production item on a Prove, Derive or Show lesson | none until graded | one per item | 75% marks the lesson Passed; never blocks | XP, MP, FSRS (creates cards), Redo |
| Practice | on demand | generated sets of 5 to 10 | none (help-enabled practice is a later option) | one per item | none | XP (capped), FSRS |
| Level review | after the level's lessons | 6 to 10 items, difficulty 2 to 4, interleaved, up to 30% from earlier levels and courses | none until graded | one per item | the planner's soft gate (section 8.5): at least 70% here or 60% on the homework before the next level enters Main | XP, MP, FSRS, Redo |
| Homework | issued at the end of each level, due in 7 days | 6 to 12 problems: at least 1 long-form, 1 code drill, 1 at difficulty 5; 25 to 30% from earlier levels and topics, unlabelled | none until submitted | answers editable until submission | score recorded; the soft gate as above | XP, MP, FSRS, Redo |
| Level check | before "Jump here" | 2 items per skipped level, 5 to 20 in all, at least 1 at difficulty 4 per level | none | one; 3-day cool-down after a second fail | 80% of marks credits the skipped lessons | MP, FSRS, credited hours |
| Topic exam | after the topic's levels, or first to test out | timed paper, 45 to 90 minutes (finals-style 180) | none; Bertie away app-wide | one sitting; resits after cool-down | 70% (curriculum bars where named) | XP, MP, FSRS, Redo, topic completion |
| Exit parts | after the topic exam | real papers, capstone drills, projects, counters | per instrument | per instrument | per curriculum line | topic and stage completion |
| Stage exit | when every part is met | the curriculum's checklist, rebuilt in section 2.9 | as parts | as parts | all parts | stage completion |

Two habits run beside the ladder: the Daily 10 (section 9) and the three weekly probability problems from 1.5 (section 10). The Redo queue (section 6) runs underneath everything. Retention sittings (section 3.8) return to every passed topic paper at 3 and 12 months.

### 2.2 Lesson screens

Formative only. Retries are unlimited and free (design research 5.4). Hints open per screen: after this screen's first Check or 90 seconds of active input, and on `trap` screens only after a first Check (`docs/PLAN.md` 6.5). Every `trap` and `generalise` screen ends with a one-sentence self-explanation prompt, unmarked and self-rated (`CONTENT-FORMAT.md` 9.3 rule 38). A screen's first try earns 15 XP, a later success 5, a revealed screen 0. Lesson screens never update the mastery model: they are scaffolded, and the learner met the idea seconds ago. A revealed screen (Show solution) adds its item to the Redo queue, except `trap` screens, whose purpose is the failure; a revealed trap is still recorded.

### 2.3 Lesson quiz

- 3 to 5 items in the scaffold-free style (design research 5.9), one attempt each, "Why?" after each item, Bertie available after each item is graded (`AI-TUTOR.md` 2.2).
- **Each quiz checks its objective's verb.** A lesson whose objective begins Prove, Derive or Show has one short production item: a 2 to 4 line proof or a two-sentence explanation in `free-response`, marked against a 3-point rubric (blind self-mark, then Bertie's, section 3.5), which counts towards Passed. Order-the-steps (O) items on proof lessons become "write the missing step" items. CI rule 9.3.15 checks it (`CONTENT-FORMAT.md`).
- **Passed**: at least 75% of quiz marks on the first completion, so one slip is allowed on the usual four-item quiz and none on a three-item quiz (decision 26). The test is exact: earned $\geq 0.75 \times$ maximum, in fractions. The course-map node gets its "Passed" star, and later shows the result of the skill's first delayed review. A later retake from Practice can earn the star; it earns no XP.
- The quiz is the usual moment a skill's FSRS card is created (section 5.3).
- Wrong items join the Redo queue.

### 2.4 Level review

- Unlocks when every lesson in the level is done. 6 to 10 items (`Level.review.count`), difficulty 2 to 4, interleaved across the level's skills. Up to 30% of the items come from due standard cards of earlier levels and earlier courses, so the review is also spaced practice.
- No pass mark, but it feeds the planner's soft gate (section 8.5). The first completion earns full XP; later runs count as practice.
- Misses join the Redo queue. The redo also serves as the skill's card review when it falls due (section 6.4, rule 4), so the skill is not tested twice.

### 2.5 Homework

**Issue.** A level's homework set is issued when its last lesson is completed, or earlier on request ("Open homework now"). Issuing fixes the instance: generator slots receive seeds (consecutive seeds, skipping repeated parameter points, `CONTENT-FORMAT.md` 5.4), and the instance is recorded as an event.

**Due.** 7 days after issue, at the end of that study day. Overdue sets stay open and submittable; an on-time submission earns 20 XP extra, a late one simply does not. After 21 days overdue the set leaves Today's Due card and waits under Review, Homework, Overdue, so Today never nags indefinitely.

**Working.** No item is graded before submission. Answers are saved as drafts (section 13.4) and can be changed freely. Numeric and expression items show the parse preview and nudges (unparseable, wrong form) without a verdict. Code items run their visible examples as often as the learner likes (`Run`); hidden tests run once, at submission. Long-form items are written in the free-response editor.

**Submission.** "Submit set" lists unanswered items and asks once. On submit:

1. Every auto-marked item is graded. Code items run their hidden suites (section 3.5 for partial marks).
2. Long-form items go to marking: the learner self-marks against the rubric, with Bertie's per-point suggestion and evidence quote when the tutor is on (`CONTENT-FORMAT.md` 7.7, `AI-TUTOR.md` 2.7).
3. The set's score is shown with worked solutions, accepted-answer rules and diagnoses per item. Bertie opens for review modes.
4. Wrong items (below full marks on a single-mark item; below 60% of marks on a multi-part or long-form item) join the Redo queue.

**Interleaving.** 25 to 30% of every set's items come from earlier levels and earlier topics: due or fading standard cards at difficulty 3 to 4, unlabelled, in mixed order with the level's own items. From 1.5 onwards, at least two items per set are "which tool?" problems whose method differs from the level's. Interleaved practice of mathematics trains tool choice, which blocked practice does poorly [recalled: Rohrer and Taylor 2007 and later classroom trials].

**Soft gate, no lock.** Homework never locks anything. With the level review it feeds the planner's soft gate (section 8.5), the topic readiness view and the exam remediation logic.

**Code items on either target.** A code item runs wherever the target can provide its runtime (decision 30): the engine compares the drill's `needs` with what this build ships and whether Python loaded on this device. Python with NumPy and pandas runs in the Artifact [sourced: `spikes/README.md`]; whether SciPy, statsmodels and scikit-learn ship in the Artifact is a per-course budget decision in `ARCHITECTURE.md` [unverified until that paper fixes it]; C++ never runs there. When the target cannot run an item, the item shows "Run this one in the web app" with the drill id and seed, and accepts a pasted result code (section 14.3). The set can be submitted with that item pending; the item is marked when the code arrives and counts as unanswered if none arrives within the 7 days after submission.

### 2.6 Practice

Generated on demand: "Practise this level", "Weakest skills" (lowest standard-band mastery among learned skills), "More like this" (from a resolved screen, or Bertie's pick per `AI-TUTOR.md` 2.11). Items come from the practice pool, never from the exam reserve. One attempt per item, no hints, "Why?" after each. First-try correct earns 10 XP, capped at 300 XP a day from practice; practice never earns MP and never creates redo items (as in the prototype `review.js`), but it updates FSRS cards like any unscaffolded attempt.

### 2.7 Level check

Offered before "Jump here" on the course map (design research 7.4). Two items per skipped level, at least 5 and at most 20 in all, with at least one item at difficulty 4 for each skipped level and the rest at difficulty 3, drawn from the levels' practice pools. 80% of the marks credits every skipped lesson in that course as "Skipped by check" (credited hours, section 7.4). Below that, the jump still happens (design research: skipping the check still allows the jump), and nothing is credited. A failed check can be retaken a day later with fresh items; after a second failed check, the next waits 3 days (revised by the `docs/PLAN.md` review: five items could credit up to 43 lessons).

### 2.8 Topic exam

One per topic, in-app, timed, no help (section 3). It closes the topic together with the topic's exit parts. It can be sat before the topic's lessons to test out (section 7.3). Topics 1.3, 1.4 and 1.5 use the finals-style kind (section 3.1); the others use the standard topic kind. Topics whose curriculum exit is a project or a practice record (0.4, 0.5, 2.3, 2.4, 3.1, 3.3) have no topic exam; their exit parts close them.

### 2.9 The exit tests, rebuilt

Each curriculum checkbox or exit line is one exit part. "Gate" is the instrument that must be passed in the app; "Confirm" is the real-world instrument the learner logs. Bars are the curriculum's.

**Stage 0** (closed by its four checkboxes; topics 0.1 to 0.3 also have in-app topic exams at 70%).

| Part | Curriculum line | Gate (in-app) | Confirm (logged) | Runs on |
|---|---|---|---|---|
| `s0.gcse` | A GCSE Higher non-calculator past paper, timed, at 80% or better | GCSE-style Paper 1 (kind `gcse`, section 3.1) at 80% | One real Higher Paper 1 from any board and series, timed at 90 minutes, self-marked with the board's mark scheme, at 80% | Both |
| `s0.precalc` | Khan Academy Precalculus course challenge at 85% or better | Precalculus challenge (kind `challenge`) at 85% | The Khan Academy course challenge result, at 85% | Both |
| `s0.zetamac` | Zetamac score of 25 or more on default settings | Median of the last 7 days' cold scores, physical keyboard, at least 5 runs, at 25 or more | None: the in-app run is the Zetamac format | Both |
| `s0.script` | Make a folder, write a ten-line Python script and run it from the terminal | `setup-checklist` paste-verify: `pwd`, `ls`, the script's text (at least 10 lines) and its output from the learner's own terminal | None | Both |

**Stage 1** (closed when every topic exit is met; 1.9 by track).

| Part | Curriculum line | Gate | Confirm | Runs on |
|---|---|---|---|---|
| `1.1.exit` | From a CSV of daily prices, compute returns, annualised volatility and maximum drawdown, and plot them | Capstone drill on a seeded, messy CSV (hidden tests at $10^{-6}$, three figure assertions), then `setup-checklist` project mode: the same script run locally, output pasted and compared (`stage1-python-tools.md` decision 16) | None | Both (pandas runs in the Artifact) |
| `1.2.exit` | The 1.1 project is in a Git repository with at least one test | Paste-verify of `git log --oneline -n 5`, `git status`, `pytest -q` (at least 1 passed); repository URL (kept as text; the GitHub API check is withdrawn by `docs/PLAN.md` conflict 5, so the paste-verify is the check on both targets). Met once, then policed weekly by the Build block's commit check (section 8.2; `stage1-python-tools.md` decision 17) | None | Both |
| `1.3.exit` | The MIT 18.01 final at 70%, plus the 18.02 problem sets on partial derivatives and Lagrange multipliers | (1) `exm.calc.finals`, whose own pass needs 70% overall and 70% on Section A, the 18.01 half (decision 27); (2) `sets`: homework sets M1 to M4 submitted, and every item below full marks redone correctly once (decision 29) | (1) A real 18.01 final, sat typed in the app at its printed length under its printed aids, marked by the gate rule against MIT's solutions, at 70%; (2) the 18.02SC Unit 2 problem sets, Parts A to C, logged as done, wrong problems in the Redo queue; (3) `human-mark`: one sitting of `exm.calc.finals` marked by a person. `estHours` 15 | Both |
| `1.4.exit` | The 18.06 final at 70%, and least squares and PCA written in NumPy from the matrix operations | `exm.linalg` at 70%; capstone drills `drl.linalg.exit-lstsq` (Cholesky normal equations and Householder QR, the factorisations written by the learner, banned calls checked on the syntax tree) and `drl.linalg.exit-pca` (PCA from the SVD) | One real 18.06 final at 70%, sat typed and marked by the gate rule, in the order `stage1-linear-algebra.md` 4.3 gives once the public finals are checked; `human-mark` on one sitting of `exm.linalg`. `estHours` 13 | Both [the 2-second timing test on Pyodide is unverified on a phone] |
| `1.5.exit` | Two Stat 110 past finals at 70% | `exm.prob.finals` at 70% | Two real Stat 110 finals, each sat typed in the app at its printed length under its own printed rules (`aids`), marked by the gate rule against Harvard's solutions, each at 70%; the second offered no sooner than 3 days after the first; `human-mark` on one sitting of `exm.prob.finals`. `estHours` 20 | Both |
| `1.6.exit` | Fit a linear regression in NumPy, match the statsmodels output, and explain every number in its summary table | `exm.stats` at 70% with `slotMin` 0.7 on Q19, "explain the table" (decision 28); capstone `drl.stats.exit-ols` (every field of the summary against stored statsmodels values) | `human-mark` on one sitting of `exm.stats`; no public paper tests "match statsmodels". `estHours` 9.5 | Paper: both; drill: wherever statsmodels ships |
| `1.7.exit` | Explain a limit order book, the bid-ask spread, and market against limit orders; derive put-call parity; price a European option on a binomial tree in Python | Topic exam at 70% with `slotMin` 0.7 on its two explanation slots and its derivation slot; a binomial-pricer drill | None | Both (standard library and NumPy) |
| `1.8.exit` | 150 problems solved, and a fresh LeetCode medium finished in 30 minutes more often than not | Problem ledger at 150 (in-app verified plus self-reported, shown separately, section 11.5); timed held-out mediums: at least 5 solved within 30 minutes in the last 9 timed attempts | None | Both (Python); C++ solutions on the web app |
| `1.9.exit` | Rewrite the 1.7 binomial pricer in C++ with tests and time it against the Python version | Paste-verify of the doctest summary and both timings (`widgets-programming.md` 6.11) | None | Both (paste); timings always local |
| `s1.cumulative` (review addition) | None in `curriculum.md`: added so no Stage 1 maths topic goes unexamined after its own exam | The Stage 1 cumulative paper (section 3.8): 180 minutes, unlabelled, across calculus, linear algebra, probability and statistics, at 70% | None | Both |

Track rule: on the Trader and Researcher tracks, `1.9.exit` moves to the Stage 2 checklist (curriculum 1.9: "traders and researchers can let C++ slip into Stage 2").

**Stage 2** (closed by its map line and the topic exits).

| Part | Curriculum line | Gate | Confirm | Runs on |
|---|---|---|---|---|
| `2.1.exit` | One tabular prediction problem end to end with time-ordered cross-validation; explain leakage, regularisation and the bias-variance trade-off without notes | `ml-workbench` capstone passing its pipeline and leakage audits; the 2.1 topic exam at 70% with `slotMin` 0.7 on its three closed-book explanation slots | Optional: the learner's own repository | Web app unless scikit-learn ships in the Artifact |
| `2.2.exit` | Test a pair of price series for cointegration, and explain why models are fitted to returns and not prices | `exm.ts` at 70% with `slotMin` 0.7 on Q15, "why returns, not prices"; capstone `drl.ts.exit-coint` on generated pairs whose cointegration is known | None. `estHours` 5.0 | Paper: both; drill: wherever statsmodels ships |
| `2.3.exit` | Three finished projects, each with tests and a written results note | Three project records marked finished (section 11.4) | The repositories themselves | Both |
| `s2.cumulative` (review addition) | None in `curriculum.md`: a delayed cumulative check before interview preparation | The Stage 2 cumulative paper (section 3.8): 180 minutes, unlabelled, across 2.1, 2.2 and the Stage 1 maths, at 70% | None | Both |

**Stage 3.**

| Part | Curriculum line | Gate | Confirm | Runs on |
|---|---|---|---|---|
| `3.1.exit` | One replication on GitHub with an out-of-sample extension and a plain note on how much of the effect survived | Project record of kind `replication` marked finished, with the results note's `oos-section` predicate passing | The repository | Both |
| `3.3.zhou` | 80% of the probability chapter in Zhou solved cold | In-app cold set of recreated green-book-style problems (kind `cold-set`) at 80% | `puzzle-workbench` book-log of the chapter in the learner's own copy: solved cold on at least 80% of the chapter's problems | Both |
| `3.3.zetamac` | Zetamac at 50 or more | 7-day median of cold scores at 50 or more (keyboard, at least 5 runs) | None | Both |
| `3.3.mocks` | Ten mock interviews done, at least three with a stranger | `mock-interview` log: ten mocks with a human partner, rubric marked, at least three with partner type "stranger" (self-declared) | The log is the evidence | Both |

Mocks with Bertie are practice and do not count towards the ten: "at least three with a stranger" reads as a count of mocks with people, and the exit exists to rehearse a live human interview [our reading of the curriculum; the owner can change it in one line of exit data].

**If the owner accepts `canon-gap.md`'s proposals**, its section 4.4 exit changes need no new machinery, only exit data:

| Proposal | Exit change | Expressed as |
|---|---|---|
| P7 Proof and discrete mathematics | A proof portfolio | `rubric` over the topic's proof pool with `count` (for example 8 proofs, each at 7 of 10 or better) |
| P8 Differential equations | A unit exam | `exam` at 70%, kind `topic` |
| P1 Research method | Each Stage 2 results note passes the P1 checklist (pre-registration, bias audit, deflated Sharpe ratio, bootstrap interval) | `project` with `notePredicates` naming the `results-note` predicates for those four sections |
| P2 Stochastic processes | Zhou chapter 4 at 80% and chapter 5 at 70% | Two `book-log` instruments |
| P2, P5 | Extra problems in the 1.5 and 1.6 exits | Slots in the finals-style and topic papers; no schema change |

New topics bring their own topic exams and exit parts. Display numbers come from position, so inserting 1.4b or 2.0a renumbers nothing stored (`CONTENT-FORMAT.md` 4.1).

### 2.10 Exit part schema

The content schema's `ExitPart` (`CONTENT-FORMAT.md` 3.2) becomes the block below. Draft 2 takes revision 2's two syntax fixes (an id pattern that admits `1.9.exit` and `s0.gcse`, and track names in place of a fixed enum) and adds four things: `slotMin` on `exam` (decision 28), `count` on `rubric` (the P7 proof portfolio), `notePredicates` on `project` (the P1 checklist), and the `sets` kind (decision 29).

```ts
const Fraction = z.number().min(0.5).max(1);
const Instrument = z.discriminatedUnion('kind', [
  z.object({ kind: z.literal('exam'), exam: Id('exm'), pass: Fraction,
             slotMin: z.record(LocalId, Fraction).optional() }).strict(),        // per-slot bars, met by any sitting or an exit-item sitting
  z.object({ kind: z.literal('drill'), drills: z.array(Id('drl')).min(1) }).strict(),
  z.object({ kind: z.literal('rubric'), items: z.array(Id('itm')).min(1), minPoints: z.number().int().min(1).max(10),
             count: z.number().int().positive().optional() }).strict(),          // default: every listed item
  z.object({ kind: z.literal('sets'), sets: z.array(Id('set')).min(1), rule: z.literal('submitted-and-redone') }).strict(),
  z.object({ kind: z.literal('paste-verify'), check: z.enum(['s0-script', 'exit-1.1', 'exit-1.2', 'cpp-toolchain', 'exit-1.9']) }).strict(),
  z.object({ kind: z.literal('real-paper'), paper: z.enum(['gcse-higher-p1', 'khan-precalc-challenge', 'mit-1801-final', 'mit-1806-final', 'stat110-final']),
             count: z.number().int().min(1).max(3).default(1), pass: z.number().min(0.5).max(1), timedMinutes: z.number().int().optional() }).strict(),
  z.object({ kind: z.literal('problem-sets'), refs: z.array(z.string().max(80)).min(1) }).strict(),          // 18.02 sets
  z.object({ kind: z.literal('counter'), counter: z.enum(['algo-solved']), target: z.number().int().positive() }).strict(),
  z.object({ kind: z.literal('timed-window'), pool: z.string(), minutes: z.number().int(), solved: z.number().int(), of: z.number().int() }).strict(),
  z.object({ kind: z.literal('median'), metric: z.enum(['zetamac-cold']), days: z.number().int(), minRuns: z.number().int(), target: z.number() }).strict(),
  z.object({ kind: z.literal('book-log'), book: z.enum(['zhou']), chapter: z.string(), share: z.number().min(0).max(1) }).strict(),
  z.object({ kind: z.literal('log-count'), log: z.enum(['mock-human', 'mock-stranger']), target: z.number().int().positive() }).strict(),
  z.object({ kind: z.literal('project'), projectKind: z.string().regex(/^[a-z][a-z0-9-]*$/), count: z.number().int().positive(),
             notePredicates: z.array(z.string().max(40)).default([]) }).strict(),   // extra results-note predicates that must pass
  z.object({ kind: z.literal('human-mark'), exam: Id('exm'), count: z.number().int().min(1).default(1) }).strict(),
                                                   // a sitting of this paper marked by a person (review addition)
]);
const TrackName = z.string().regex(/^[a-z][a-z-]{1,23}$/);    // the last segment of a trk.* id
const ExitPart = z.object({ id: z.string().regex(/^[0-9a-z][0-9a-z.-]{0,31}$/), text: Prose,
  gate: z.array(Instrument).min(1), confirm: z.array(Instrument).default([]),
  track: z.object({ deferTo: z.number().int().min(1).max(3), tracks: z.array(TrackName).min(1) }).strict().optional(),
  estHours: z.number().positive() }).strict();
```

An exit part is met when every `gate` and every `confirm` instrument is satisfied. Its status is derived from events (section 13.3) and shown on the topic and stage pages as a checklist: "Stage 0 exit: 3 of 4 parts".

**When each instrument is satisfied:**

| Kind | Satisfied when |
|---|---|
| `exam` | some sitting passed the paper (its own pass, including section bars, section 3.6) at or above `pass`; and, for each slot in `slotMin`, some sitting or exit-item sitting of this paper scored at least that fraction on the slot |
| `drill` | every listed drill has a submission with every hidden test passing |
| `rubric` | at least `count` (default all) of the listed items have a confirmed mark of `minPoints` or more |
| `sets` | every listed set is submitted, and every item that scored below full marks has a later correct redo |
| `paste-verify` | the named check accepted a paste |
| `real-paper` | `count` logged real papers of that kind, from different series, each at `pass` or better (section 11.8) |
| `problem-sets` | every listed reference is logged done |
| `counter`, `timed-window`, `median`, `book-log`, `log-count` | the rules of sections 11.5, 9.3, 11.9 and 11.7 |
| `project` | `count` projects of that kind are finished (section 11.4), with every `notePredicates` entry passing on their results notes |
| `human-mark` | `count` sittings of the paper carry a logged mark by a person (marker type self-declared: study partner, tutor or paid marker; the marker's per-question marks entered by the learner). The result screen shows the app's gate mark beside it; a gap above 10 percentage points adds the paper to the content-gap report as "in-app marking may be miscalibrated" |

### 2.11 Content gaps the rebuilt exits expose

Rebuilding the exits against the real papers showed two places where the curriculum's cover lists did not reach the bar the curriculum sets. Draft 1 raised them; `stage0-precalc-computing.md` has since closed both, subject to the owner's confirmation:

1. **GCSE geometry and statistics.** A Higher paper weights Geometry and measures at 17 to 23% and Probability and statistics at about 12 to 18% [sourced: Ofqual weightings via search summaries], and the Stage 0 cover lists named neither. **Closed by** that file's decision 2: course S (Shape and Space) and level C5 (Data and Statistics) inside 0.3, about 40 of its 200 hours. The `gcse` paper is built to Ofqual's weightings (that file's section 4.4).
2. **Khan Academy Precalculus units.** The course covers complex numbers, polynomials, composite and inverse functions, rational functions, conic sections, matrices, vectors, probability and combinatorics, series, and limits [sourced: search summary; unit list not checked against the live course]; the 0.3 cover list named several of them nowhere. **Closed by** that file's decision 3: levels T5, T6, R3, R4 and R5 teach them.

One conflict stays open in Stage 2: the curriculum's track table gives the Trader track "one project" while the Stage 2 exit asks for three. The planner follows the exit (three) and orders the options dashboard first on the Trader track. [Decision needed from the owner.]

### 2.12 Completion states

| Unit | Done | Mastered or complete |
|---|---|---|
| Lesson | every screen completed and the quiz attempted | Passed: quiz at 75% or better on the first completion (the star); Mastered applies to skills only (section 5.6) |
| Level | every lesson done, level review done, homework submitted | n/a |
| Course | every level done | n/a |
| Topic | n/a | topic exam passed (or tested out) and every topic exit part met |
| Stage | n/a | every stage exit part met |

"Skipped by check" and "Tested out" are distinct states shown on the course map with their own glyphs; they count as credited, not earned, hours (section 7.4).

---

## 3. The exam engine

One engine runs every timed, help-free paper: topic exams, finals-style papers, the Stage 0 papers, cold sets, level checks and placement. The prototype `exam.js` (rules screen, navigator, mark-to-revisit, timer, submit confirmation, result screen) is the reference for the screens; this section fixes the rules behind them.

### 3.1 Paper kinds

| Kind | Used for | Minutes | Marks | Items | Calculator | Code | Long-form | Pass |
|---|---|---|---|---|---|---|---|---|
| `topic` | topic exams other than 1.3 to 1.5 | 45 to 90 (about 1.5 times the summed item estimates) | 40 to 80 | 12 to 25, mixed formats, difficulty mix 20/50/20/10 at levels 2/3/4/5 (design research 8.4); at least 30% of marks on applied items that contain a named trap or edge case | per paper or per section | allowed | at least 30% of marks, target 40% (the lesson-creator final test: about 30% short answer, 40% long-form, 30% applied) | 70% |
| `finals` | 1.3 calculus, 1.4 linear algebra, 1.5 probability | 180 | 100 | 10 or 11 multi-part questions in the style of MIT 18.01, MIT 18.06 and Stat 110 finals [recalled, unverified: 3 hours each]; 1.3 in two sections on one clock | none: answers in exact form | none (code lives in the capstones) | at least 40% of marks (proofs, derivations, explanations) | 70%; 1.3 also 70% on Section A |
| `gcse` | `s0.gcse` | 90 | 80 | 26 questions in rising difficulty, mostly multi-part, built to Ofqual's Higher weightings (`stage0-precalc-computing.md` 4.4) | none | none | "show that" questions as rubric items | 80% |
| `challenge` | `s0.precalc` | 60 | 30 | 30 single-mark items across the precalculus units (section 2.11) | basic | none | none | 85% |
| `cold-set` | `3.3.zhou` gate | 90 | 20 problems, 1 mark each | recreated green-book-style problems from the held-out bank | none | none | none (answers only, as in an interview) | 80% |
| `level-check` | "Jump here" | about 3 per skipped level | 5 to 20 | 2 per skipped level | per course | no | no | 80% |
| `placement` | onboarding | about 12 | adaptive | at most 14 | basic | no | no | none |
| `exit-item` | a missed `slotMin` bar (decision 28) | the slot's share of the paper's minutes, rounded up to 5 | the slot's marks | 1, fresh from the slot's pool | as the paper | as the paper | as the slot | the `slotMin` bar |

**Sections.** A form is a list of sections (`CONTENT-FORMAT.md` 3.2). Each section may set its own `minutes`, `calculator` and pass bar (`sectionPass` on the paper, keyed by section id):

- **Timed sections** run in order. A section closes for good when its minutes end or when the learner taps "Finish section A" and confirms; its answers are then final and the next section's clock starts. Unused minutes are not carried over. The 0.3 topic exam uses this: Section A, 40 minutes without a calculator; Section B, 50 minutes with the in-app scientific calculator.
- **Untimed sections** share the paper's single clock, can be visited in any order, and show a suggested split on the rules screen (1.3: Section A 125 minutes, Section B 55).
- **Section bars** are part of the paper's own pass: 1.3 passes at 70 of 100 overall and 49 of Section A's 70.

**Aids.** A paper may list formula cards (`aids`), shown in a sheet during the sitting; nothing else from the Notebook is reachable. The 1.5 paper's card holds the table of distributions and nothing more (`stage1-probability.md` 4.1).

**Follow-through.** A part that declares `followThrough` is graded against the learner's own answer to the part it names, where the item's grader can recompute it (`stage1-linear-algebra.md` 4.1), so one slip costs one part.

The speed formats (Zetamac, 80-in-8) and the 1.8 timed medium have their own timers inside their widgets (`speed-drill`, `problem-workbench` timed mode) and their own rules (sections 9 and 11.5); they share the integrity record (section 3.9) but not the navigator.

**GCSE method marks.** Real GCSE marking awards method marks for working. The `gcse` paper approximates them two ways: multi-part questions ask for the intermediate result as its own part (so a correct method with a slip in the last step keeps its earlier marks), and "show that" questions are long-form items with a rubric. This is stricter than a human examiner on unusual but valid methods, which is why the real paper confirms (decision 1).

### 3.2 Forms and fresh variants

A paper is a list of forms (`Exam.forms`, at least 3, `CONTENT-FORMAT.md` 3.8). Each form is a list of slots: fixed items, generator slots, pool slots. A slot names what a question must cover, never the method: the serving order of slots is shuffled per sitting (`hash32(attemptId, 'order')`, sections kept), item stems never name the method (a lint warns on each topic's method terms, the reviewer decides), long-form pools are built across methods (a variance question solvable by indicators, by Eve's law or by a generating function), and two slots per form are unlabelled: drawn from the whole topic's pool at difficulty 3 to 4, at the marks of the slot they replace. The same rule holds for the 1.3 and 1.4 papers and for difficulty-5 homework items. Choosing the tool for an unlabelled story is what real finals and interviews test (revised by the `docs/PLAN.md` review).

**Choosing what to serve:**

```
servePaper(exam, learner, attemptId):
  for each form f:
    seenMarks(f) = marks of f's fixed items the learner has seen anywhere (any sitting, practice, homework)
  choose f with the least seenMarks; ties: fewest previous sittings of f, then form order
  for each generator slot (gen, level, count):
    draw from gen's exam reserve at that level, excluding parameter points the learner has seen;
    seed = hash32(attemptId, slotIndex, k), stepping k until an unseen point is found (at most 64 steps);
    the seed picks a point of the reserve's admissible index as CONTENT-FORMAT.md 5.4 specifies
  for each pool slot (skills, difficulty, heldOut: true, count):
    draw unseen held-out items first, then the least recently seen
  if any slot had to serve a seen item: the rules screen says so ("3 of 25 questions are ones you have seen before")
  record the served paper (form id, items, generator ids, versions, levels, seeds) in the exam-start event
```

**Content rules (CI, for `CONTENT-FORMAT.md` section 6):**

1. Forms of one paper have equal total marks, and each form's difficulty mix is within 5 percentage points of the declared mix at every level.
2. Every skill of the topic appears in at least one form; every form covers at least 80% of the topic's levels.
3. Either at least 50% of each form's marks come from generator slots, or the paper has at least 5 forms.
4. Reserve capacity: for every generator slot, the reserve at that level holds at least $6 \times$ (forms $\times$ count) admissible points, so six sittings stay fresh; every long-form pool slot holds at least 12 held-out items.
5. Held-out items and reserve points never appear in practice, homework, level reviews, redo variants or Bertie's practice picks (`CONTENT-FORMAT.md` 5.4).
6. A held-out long-form item whose model answer has been shown to the learner is retired from that learner's pool (section 3.7).
7. No two forms of a paper serve the same slot order, and every form has two unlabelled slots.

**Practice papers.** "Practice paper" builds a paper of the same shape from the practice pool (never the reserve), timed or untimed. It records attempts in the `practice` context, affects no completion and no cool-down, and earns practice XP.

### 3.3 Before the clock starts

The rules screen (prototype `exam.js`) shows: minutes, number of questions, total marks, pass mark in marks ("56 of 80") and any section bar ("and 49 of Section A's 70"), sections with their minutes and calculator rules, aids, "Bertie is out of the room for this paper" (Bertie in his `away` state, `BERTIE.md` section 5), the seen-items warning if any, and, for papers on an exit, an attestation:

> I will sit this paper under exam conditions: no other tabs or devices; aids and calculator as stated above.

The aids line comes from the paper's own `aids` data (formula cards, a page of notes, none), so a paper that allows notes says so and one that allows none says "no notes".

Start is enabled when:

- the attestation is ticked (exit papers only);
- the paper's runtime is ready: if any item is a code item, Python and the packages its items need are loaded and warmed before the clock starts ("Preparing Python"). On the owner's iPhone in the Artifact, Python was ready at 2.8 s and NumPy with pandas at 5.1 s; in Chromium, 3.0 s and 8.5 s [sourced: `spikes/README.md`];
- this device holds the paper's lease (section 13.7). Another device sees "This paper is in progress on your other device" and a read-only clock;
- the paper is not in cool-down (section 3.8).

On a target that cannot run one of the paper's code items (decision 30: a C++ item, a package the Artifact does not ship, or Python that failed to load on this device), the rules screen shows "Sit this paper in the web app" instead of Start. A paper is never split across targets: the timer, the tutor lockout and the integrity record live in one place.

### 3.4 During the paper

- **Clock.** `endsAt = startedAt + minutes + pausedTotal`, wall-clock. The countdown shows minutes and seconds in tabular figures; the screen reader announces 30, 10, 5 and 1 minutes left (the prototype announces 5). Closing the app does not stop the clock. Reopening before `endsAt` resumes at the current question; reopening after it auto-submits the saved answers.
- **Pause.** "I've been interrupted" pauses the clock and hides the paper (questions and answers are removed from the screen, not blurred), so a pause cannot buy thinking time. The total pause budget is 15 minutes a paper; when it runs out the clock resumes by itself. Every pause is recorded with its start and length.
- **Navigator.** A grid of question squares: answered, not answered, answer does not parse, marked to revisit, current (prototype). Any question can be opened in any order inside the open sections. A timed section shows its own countdown beside the paper's, and its squares grey out when it closes (section 3.1, Sections); "Finish section" lists its unanswered and marked questions first.
- **Saving.** Every answer change is saved to the local draft at once and to the `db` draft document at most every 10 seconds (section 13.4). Losing the connection changes nothing on screen except a "Saved on this device" chip.
- **Tab visibility.** Leaving the tab is recorded (count and total time), never punished. Exams are long; real life happens.
- **Tutor.** Off app-wide from Start to submission (`AI-TUTOR.md` 2.12); the paste guard covers chat elsewhere.
- **Code items.** `Run` executes the visible examples with the drill's time limit; hidden tests run at submission.
- **Long-form items.** Typed with inline maths; the `scratch-pad` ink layer is allowed and never marked.
- **Calculator.** When the current section's rule (or the paper's, if the section sets none) allows one, the in-app basic or scientific calculator opens in a sheet. For `none`, no calculator exists in the app while that section is open; a physical one is covered by the attestation.
- **Aids.** The paper's formula cards open in a sheet from the top bar; the Notebook and search are closed until submission.

### 3.5 Submission and marking

"Submit paper" lists unanswered and marked-to-revisit questions and asks once. Time running out submits automatically.

| Item type | Marking |
|---|---|
| Choice, numeric, expression, set, ordering and the other auto-graded checks | The runtime grader (`CONTENT-FORMAT.md` 7); multi-part items marked per part |
| Code | Hidden and visible tests run; marks $= \lfloor m \cdot p / n \rfloor$ for $p$ of $n$ tests passed on an item worth $m$; a test that exceeds its time limit fails |
| Long-form | Rubric of up to 10 points, scaled to the item's marks: $m \cdot \text{points} / 10$. Self-mark with Bertie's suggestion per point (`AI-TUTOR.md` 2.7, tier `complex` for proofs and derivations) |

- Totals are kept as exact fractions. The pass test is total $\geq$ pass $\times$ maximum and, for each section bar, section total $\geq$ bar $\times$ section maximum, computed exactly; only the display rounds (to one decimal place). Exit `slotMin` bars are recorded per slot on the result and never change the paper's own pass.
- Follow-through parts are marked after the part they depend on, against the learner's own answer to it.
- The result is **provisional** until every long-form item is confirmed. Auto-marked parts show at once.
- **Gate marking** (decision 6). The learner marks every rubric point blind; Bertie's marks then appear beside them; the paper counts $\min(\text{learner}, \text{Bertie})$ per point. Points where the learner's mark is higher are listed as **disputed**: the learner may accept the lower mark, or sit a fresh exit-item sitting on that slot (3-day cool-down, as decision 28), whose own gate mark replaces the slot's. The result never reads "self-marked pass" any more, because a learner's mark alone cannot raise a gate.
- If the tutor is off or fails, long-form marks in a gate stay **provisional** ("Pass pending marking") until Bertie or a person marks them; outside gates the learner's self-mark counts and the result says so.

### 3.6 Pass marks

| Paper | Pass mark | Source |
|---|---|---|
| Topic exam | 70% | design research 8.2 |
| Finals-style 1.3, 1.4, 1.5 | 70%; 1.3 also 70% on Section A | curriculum exits; `stage1-calculus.md` decision 12 |
| Lesson quiz (the Passed star, not a gate) | 75% | decision 26 |
| Exit-item sitting | the exit's `slotMin`, 70% in every current exit | curriculum exits as rebuilt in section 2.9 |
| GCSE-style Paper 1 | 80% | curriculum Stage 0 exit |
| Precalculus challenge | 85% | curriculum Stage 0 exit |
| Cold set (3.3) | 80% | curriculum 3.3 exit |
| Long-form exit items (1.6, 1.7, 2.1, 2.2) | 7 of 10 each | [our choice]: the owner's lesson-creator skill marks long answers out of 10; 7 allows one missing point and one imprecision. The prototype's 6 of 10 (`review.js`) stays the bar for counting an ordinary long-form item as correct |
| Level check | 80% of marks | [our choice] |

### 3.7 The result screen

As the prototype's `#exam-result`: score and pass mark (and section bars), a pass stamp (design research 4.7: count-up, stamp on spring-snap; the only particles are Bertie's own `celebrate` one-shot at 160 px, `BERTIE.md` section 5) or a plain "Not yet" heading with Bertie back to `idle`, time used, pauses, then:

- **By skill:** marks earned against marks available per skill, sorted weakest first, each with its current mastery.
- **By question:** the learner's answer, the accepted-answer rule, the worked solution and the diagnosis line; time spent on the question. After a **fail**, held-out long-form pool items show per-skill results and the rubric points missed, not the model answer, so the pool stays unseen for the resit; after a pass the model answers show and those items retire from the learner's pool. Every long-form rubric's `consequence` line ("would fail in production because", `CONTENT-FORMAT.md` 3.4) shows under the points missed.
- **Next:** on a pass, the topic's remaining exit parts, including any `slotMin` bar this sitting missed ("Q19 scored 6 of 10; the exit asks for 7. Retake it alone from Friday."); on a fail, the remediation set and the date the resit opens.
- **Bertie** opens in review modes; the recap (`AI-TUTOR.md` 2.9) runs on request.

Items that meet the Redo rule of section 6.1 join the Redo queue. Every item updates its skill's cards (section 5.3).

### 3.8 Resits, cool-downs and remediation

| Paper | After a fail | After abandoning | After a pass |
|---|---|---|---|
| Topic exam (`topic`) | 3 days and the remediation set | 24 hours; the items served are burned (counted as seen) | Practice sittings at any time; **retention sittings** scheduled about 3 and 12 months after the pass: a 60 to 90 minute form at difficulty 3 to 4 from the reserve. Below 60% the topic goes back into Main as remediation and its completion reopens in the planner until a later retention sitting reaches 60% |
| Finals-style, GCSE-style, precalculus challenge, cold set | 7 days and the remediation set | 24 hours; items burned | As above |
| Cumulative papers (review addition) | 7 days and the remediation set | 24 hours | A **Stage 1 cumulative paper** (180 minutes, unlabelled, calculus, linear algebra, probability and statistics) is part of the Stage 1 exit; a **Stage 2 cumulative paper** (180 minutes, ML, time series and the Stage 1 maths) must pass before 3.3 starts |
| Level check | 1 day | 1 day | n/a |
| Exit-item sitting | 3 days and a remediation set of 3 items on the slot's skills | 24 hours; the item is burned | The exit item is met; no further sittings |
| Diagnostic sitting (the first sitting of a topic exam or stage paper, before that topic's or stage's lessons) | none, once: one diagnostic sitting per topic paper and per stage paper | none | A pass counts in full |

There is no limit on the number of sittings, but only the first sitting of each paper is a diagnostic: every later sitting, before or after the lessons, carries the normal cool-down and remediation. Every sitting is in the record.

**Remediation set**, built when a fail is marked:

1. For each skill whose marks share in the paper is below 60%: 3 practice items, 2 in the band where marks were lost and 1 a band lower.
2. For each `requires` parent of those skills whose standard mastery is below 70%: 2 items.
3. At most 30 items, interleaved, never from the exam reserve.
4. The skills' `exercises` citations (section 4.2) appear beside the set as optional textbook work, logged as outside work.

The set is done when every item has been attempted. It asks for problems, not marks: marks are the resit's job (curriculum rule 3).

### 3.9 The integrity record

Stored on every sitting of every timed paper and speed format:

```ts
interface Integrity {
  startedAt: number; endsAt: number; submittedAt: number; auto: boolean;   // auto: submitted by time-up
  pauses: { at: number; ms: number }[];
  hidden: { count: number; ms: number };
  device: string; input: 'keyboard' | 'touch' | 'mixed';
  calculator: 'none' | 'basic' | 'scientific' | 'any'; attested: boolean;
  tutorCalls: number;                                // must be 0 (AI-TUTOR.md 2.12)
  target: 'artifact' | 'web';
  runtime?: 'pyodide';                               // with its version in appRelease
  sections?: { id: string; closedAt: number; auto: boolean }[];
  form: string; served: string;                      // served-paper hash (section 3.2)
  appRelease: string; contentRelease: string;
}
```

The record is shown on the result screen and in the learning record (section 14.4). Nothing in it voids a paper except the speed formats' hidden-tab rule (section 9.2).

### 3.10 State machine

```
not-ready ──(prerequisites of 3.3 met)──► ready
ready ──Start (lease held, runtime warm, attested)──► in-progress
in-progress ──"I've been interrupted"──► paused ──resume or budget spent──► in-progress
in-progress ──timed section ends or "Finish section"──► in-progress (next section; the closed one is final)
in-progress ──Leave, confirmed──► abandoned ──24 h──► ready
in-progress ──Submit, or now ≥ endsAt──► submitted
submitted ──auto-marking──► marking (long-form items pending)
marking ──every long-form item confirmed──► marked
marking ──gate long-form marks lack Bertie or a person (tutor off)──► provisional ──marked by Bertie or a person──► marked
marked ──pass──► passed
marked ──fail──► cool-down ──(days elapsed) and (remediation done)──► ready
```

The state is derived from events (section 13.3), so every device and every target shows the same state after sync.

---

## 4. The skill graph

### 4.1 What a skill is

A skill is a method the learner can be asked to apply to a fresh problem and can be told to practise. Three tests:

1. An exam item at difficulty 3 can test it alone.
2. It has at least one generator, or at least 6 authored items across the three bands.
3. Its name is an action: "Condition by counting outcomes", not "Conditional probability".

**Granularity: a skill is an examinable method at level grain.** 3 to 8 skills per level; `Lesson.introduces` holds at most 2 (`CONTENT-FORMAT.md` 3.2). Finer distinctions a lesson teaches ("orderings of a multiset" inside "count equally likely outcomes") are **step tags** on screens and items: they drive diagnosis, hints, the content-gap report and the redo variant choice, and they create no FSRS card. The path's 377 counted levels (`docs/CURRICULUM.md` 0.1) at about 4 skills each give about 1,500 skills [counted levels; skills per level our choice]; at about 50,000 unscaffolded attempts over the path (section 13.6) that is about 33 pieces of evidence per skill. The review found every sample lesson in the item files introducing 3 or 4 skills, which at 2,044 lessons would mean about 7,600 skills, about 1,140 hours of maintenance over the path and 5 or 6 pieces of evidence per skill [simulated, section 6.5]; those lists are re-cut to at most 2 skills plus step tags before any lesson file is written.

**Interview patterns** (`skl.interview.*`: symmetry, linearity of expectation, indicator variables, first-step analysis, conditioning on the first event, order statistics, geometric probability, optional stopping, expected value of a game, Kelly sizing) are skills with `pattern: true`. The weekly problems (section 10) select by them.

Mental arithmetic facts are not skills; they have their own fact model (section 9.4).

### 4.2 Schema

The `Skill` schema in `CONTENT-FORMAT.md` 3.2 gains three fields:

```ts
export const Skill = z.object({
  id: Id('skl'), name: z.string().max(80), topic: Id('top'), description: Prose,
  requires: z.array(Id('skl')).default([]),                       // needed before this skill can be learned
  encompasses: z.array(z.object({ id: Id('skl'), w: z.number().min(0.1).max(1) }).strict()).default([]),
                                                                  // exercised as a component every time this skill is used
  exercises: z.array(Citation).default([]),                       // textbook exercises for remediation and companion work
  pattern: z.boolean().default(false),                            // an interview pattern (section 10)
}).strict();
```

- **`requires`** says what must be known first. It drives placement inference, priors, remediation and the "learn next" frontier.
- **`encompasses`** says what is practised implicitly, and how much: solving a quadratic by formula exercises "evaluate an expression" fully ($w = 1$); Bayes' rule exercises "multiply fractions" partly ($w = 0.5$). It drives implicit repetition (section 5.5). The default is empty, which is conservative: no implicit credit until an author asserts it.

### 4.3 Rules checked in CI

1. `requires` is acyclic.
2. A `requires` edge points to a skill in the same topic or an earlier one in curriculum order, or in a declared alongside topic (1.7 may require 1.3 to 1.6 skills learned so far).
3. Every `encompasses` target is in the transitive closure of `requires`.
4. A redundant `requires` edge (implied by a longer path) is a warning, not an error.
5. Every skill is tagged on at least one quiz item and appears in at least one exam pool or form.
6. Every skill has a generator or at least 6 items spread over at least two bands.
7. **Card budget:** a level introduces at most 8 skills, and a topic at most $5 \times$ its levels (a warning above $4 \times$); a lesson introduces at most 2. A step tag never names a skill id.

The compiler emits one `skills-<stage>.json` per stage: nodes, both edge lists, and each skill's generators and item counts per band.

### 4.4 Uses

| Use | Edges | Section |
|---|---|---|
| Placement inference | `requires` closure below a passed anchor | 7.1 |
| Priors for unseen skills in readiness | `requires` parents' mastery | 5.7 |
| Remediation after a failed paper | `requires` parents | 3.8 |
| Implicit repetition | `encompasses` | 5.5 |
| "Learn next" frontier for practice and the planner | skills without cards whose `requires` parents all have standard mastery of at least 70% | 2.6, 8.4 |
| Lesson-start check | if a lesson's required skills include one with standard mastery below 60%, offer a 2-item warm-up before the lesson (skippable) | 6.4 |

---

## 5. The mastery model

### 5.1 The choice

| Model | Works for one learner | Models forgetting | Models difficulty | Schedules reviews | Needs population data | Verdict |
|---|---|---|---|---|---|---|
| Elo for learner modelling (Pelánek, 2016, *Computers and Education*) [recalled, unverified] | Partly: item difficulties are learned from many learners; with one learner they stay at their authored values and Elo becomes a fixed-step logistic update | No (later extensions add it) | Yes, continuously | No | For item difficulty | Rejected as the primary model |
| Bayesian Knowledge Tracing (Corbett and Anderson, 1995) [recalled, unverified] | No: its four parameters per skill are fitted across learners; defaults are guesses | No, in the standard form | No | No | Yes | Rejected |
| Item response theory (Rasch, 2PL) | No: item parameters need calibration samples | No | Yes | No | Yes | Rejected |
| Leitner boxes at 1, 3, 7, 30 days | Yes | Fixed steps, not personal | No | Yes | No | Rejected; kept only as the fallback in 5.9 |
| **FSRS-6** (open-spaced-repetition, `ts-fsrs` 5.4.2) | **Yes: its optimiser fits 21 parameters to one person's review history** | **Yes: a power-law forgetting curve per card** | **Through cards per difficulty band** | **Yes** | **No: defaults come from large flashcard datasets; personal parameters replace them** | **Chosen** |

Two further reasons:

- **The path is four years long.** The costliest failure is forgetting Stage 0 algebra by Stage 3, not misjudging today's ability by a few points. A memory model addresses the costliest failure directly.
- **Precedent.** Math Academy runs spaced repetition over a hierarchical maths knowledge graph and credits implicit practice down "encompassing" edges (Fractional Implicit Repetition) [sourced: justinmath.com, mathacademy.com, via search summaries]. Sections 4.2 and 5.5 adopt that idea in a simplified form.

**The risk, stated.** FSRS was built and benchmarked on flashcard recall. Applying it to "can solve a fresh problem of this kind" is an inference [inferred]. Three things contain the risk: the personal optimiser (5.9), the calibration report that tests every mastery number against outcomes (5.9), and the fallback to fixed intervals if the model predicts worse than a constant.

### 5.2 Cards

One FSRS card per skill per band, created on first evidence:

| Band | Item difficulty | Scheduled? | Used for |
|---|---|---|---|
| `core` | 1 and 2 | no | the map's "Learning" state; readiness for easy slots |
| `std` | 3 | **yes** | the mastery number; the review schedule; readiness |
| `stretch` | 4 and 5 | no | the stretch star; readiness for hard slots; stretch practice |

Only standard cards are scheduled, with one exception. Core and stretch cards are updated whenever evidence arrives and decay like any card; core is implied by standard and never queued. **Stretch cards of `core-interview` topics are scheduled** at 0.80 retention and served at difficulty 4, because interview and finals readiness sits at difficulty 4 to 5 (section 5.4). Other stretch cards stay growth, not maintenance.

Card state is `ts-fsrs`'s `Card` (stability, difficulty, last review, reps, lapses, state) plus `successes` and an implicit-credit accumulator. Cards are derived state (section 13.3); the event log holds the evidence.

**Library configuration**, fixed and tested (section 16): `fsrs(generatorParameters({ enable_fuzz: false, enable_short_term: false }))`, with the default weights until the optimiser replaces them (section 5.9). Each review calls `next(card, reviewTime, rating)` with the review's own timestamp; the library's own `due` and `scheduled_days` are ignored, because due dates come from the tiers of section 5.4. With these settings a first Good gives a stability of 2.31 days and a first Again 0.21 days [measured, section 0.2]. Fuzz is off because the fold must give byte-identical state on every device; short-term steps are off because a card is reviewed at most once a study day (section 5.3).

### 5.3 What counts as a review

**Counted:** the first try at an item in an unscaffolded context: lesson quiz, practice, level review, Redo, homework, exam (all kinds), level check, weekly problem, timed medium.

**Not counted:** lesson screens; later tries at the same item; attempts after a hint was opened; single-choice items with fewer than 4 options (the guess rate is too high); speed formats (facts have their own model); outside work (decision 18).

**One review per card per study day:** the day's first counted attempt for that skill and band. Later attempts that day still earn XP and MP.

**Card:** the item's primary skill (first in `skills`) and the band of the item's difficulty. Secondary skills receive implicit credit (5.5) at $w = 0.5$ on a success.

**Grade:**

| Outcome | Grade |
|---|---|
| Wrong, or below 60% of marks on a multi-part or code item | Again |
| Long-form at 6 or 7 of 10; multi-part at 60% to 99% of marks; correct with the learner's self-rating "hard" (weekly problems) | Hard |
| Correct; long-form at 8 or more | Good |
| Correct, in at most half the item's estimated time, and the card's last grade was not Again | Easy |

**Stretch misses are not lapses.** A wrong answer on a stretch item when the skill's stretch card does not exist yet creates the stretch card with Again; it never touches the standard card. A miss at difficulty 5 is information about the frontier, not evidence of forgetting.

### 5.4 Scheduling

A standard card is due when its retrievability falls to the desired retention $r$ of its tier. From the FSRS-6 curve [measured: `ts-fsrs` source, section 0.2]:

$$R(t) = \left(1 + \phi\,\frac{t}{S}\right)^{-w_{20}}, \qquad \phi = 0.9^{-1/w_{20}} - 1, \qquad t^*(r) = \frac{S}{\phi}\left(r^{-1/w_{20}} - 1\right)$$

so the due date is `lastReview + t*(r)`. Due dates are computed when read, never stored, so a tier change moves them at once.

| Tier | Skills | Desired retention $r$ |
|---|---|---|
| `active` | the current main item and alongside items; any topic the learner pins (for example probability during interview preparation) | 0.90 |
| `recent` | topics completed within the last 365 days, and every topic of the current stage | 0.85 |
| `dormant` | everything else | 0.80, lowered by the balancer to no less than 0.70 |
| `core-interview` | topics marked `coreInterview: true` in curriculum data: 0.5, 1.5 and the interview patterns (`skl.interview.*`) on every track, 1.6 on the researcher track | 0.90 for standard cards for the rest of the path; stretch cards 0.80 at difficulty 4; never lowered by the balancer |

**Load balancer.** Each Monday, and after a tier change:

```
budget   = 4 × (review block hours + borrow allowance) × 60 minutes
demand(r) = minutes of Redo items due in the next 28 days, except those counted towards Main (section 6.5)
          + Σ over standard cards due in the next 28 days at tier retentions (dormant at r) × item minutes
r = 0.80
while demand(r) > budget and r > 0.70:  r = r - 0.025
while demand(r) < 0.7 × budget and r < 0.80:  r = r + 0.025
dormant retention = r            # non-core dormant cards only; core-interview cards keep their 0.90 and 0.80
```

Item minutes are the generator's or item's estimate, 3 minutes when unknown [our choice]. The chosen $r$ is shown under You, Stats ("Older topics are kept at 78% recall to fit your review time").

### 5.5 Implicit repetition

When a counted review of skill $s$ is graded Good or Easy:

- each `encompasses` edge $(p, w)$ of $s$ adds $w$ to $p$'s standard-card accumulator; on a multi-skill item, each secondary skill gets $w = 0.5$;
- if a prerequisite's accumulator reaches 1, or reaches 0.5 while its standard card is due within 7 days, the fold applies a Good review to that card at that moment and resets the accumulator;
- implicit reviews do not propagate further, and failures never propagate. A wrong answer on Bayes' rule says nothing reliable about fraction arithmetic; a diagnosis can still tag a prerequisite misconception explicitly.

The review composer (section 6.4) also prefers a due card whose review would implicitly cover other due cards, the "knock-out" idea in Math Academy's FIRe [sourced, as above].

### 5.6 The mastery number and the map

**Mastery of skill $s$ now** $= P(s, \text{std}, \text{now})$ from section 5.7, shown as a percentage: "82%: we estimate an 82% chance you would solve a fresh, typical question on this skill today."

| Map state | Rule |
|---|---|
| Not started | no card |
| Learning | cards exist; no standard card, or fewer than 2 successful standard reviews |
| Practised | standard mastery at least 70% and at least 2 successes |
| Mastered | standard stability at least 21 days and at least 3 successes |
| Fading (an outline on the cell) | Mastered, but standard mastery now below 75% |
| Stretch star | stretch card retrievability at least 80% |

Cells are shaded by the mastery number on the single-hue sequential ramp (design research 2.6), with a table view. The topic row shows the mean of its skills' mastery, weighted by each skill's share of the topic exam blueprint.

### 5.7 The probability model and the readiness forecast

**Probability of solving a fresh item** on skill $s$ at difficulty $d$ at time $t$, with $b = \text{band}(d)$:

1. If card $(s, b)$ exists: $P = R_{s,b}(t)$.
2. Else, if a card exists in a higher band $b'' > b$: $P = R_{s,b''}(t)$. Solving harder items implies the easier ones.
3. Else, if a card exists in a lower band $b' < b$: $P = 0.6^{\,b - b'} \cdot R_{s,b'}(t)$ [our choice: 0.6 per band].
4. Else: $P = 0.25$ if every `requires` parent has standard mastery of at least 80%, otherwise $P = 0.10$ [our choice].
5. For a single-choice item with $k$ options: $P \leftarrow \max(P, 1/k)$.

**Readiness for a paper** at time $t$ (now, or a date the learner sets): the paper's slots $j$ have marks $m_j$, primary skill $s_j$ (pool slots average over their skills) and difficulty $d_j$. Let $p_j = P(s_j, d_j, t)$, $M = \sum_j m_j$ and $\theta$ the pass fraction.

$$\mu = \sum_j m_j\,p_j, \qquad \sigma^2 = \sum_j m_j^2\,p_j(1 - p_j), \qquad P(\text{pass}) \approx 1 - \Phi\!\left(\frac{\theta M - 0.5 - \mu}{\sigma}\right)$$

The exam card shows "Expected score 74%. Chance of passing about 65%." with the three weakest skills and a "Practise these" button. The planner suggests sitting when $P(\text{pass}) \geq 0.7$ and every level is done; the learner can sit at any time.

The normal approximation treats items as independent and long-form items as all-or-nothing, which overstates the variance for long-form-heavy papers [inferred]. The calibration report (5.9) records every forecast against the result.

### 5.8 Priors

Evidence that is not an ordinary review sets a card directly:

| Source | Card set | Stability $S$ | Difficulty $D$ |
|---|---|---|---|
| Placement: anchor skill passed | standard card, one Good review dated $S$ days ago (so $R = 0.9$ now) | 21 days | 5 |
| Placement: skill inferred through the `requires` closure of a passed anchor | standard card, as above | 7 days | 5 |
| Level check passed | standard cards of the skipped lessons' skills | 7 days | 5 |
| Topic exam or test-out | none: every exam item is an ordinary counted review | n/a | n/a |

Short stabilities on inferred skills mean the first reviews arrive within a week and check the inference cheaply.

### 5.9 Personal parameters and calibration

- **Optimiser.** After 1,000 counted standard-card reviews, and then monthly, the web app runs the FSRS optimiser in a Web Worker (`fsrs-browser` or `@open-spaced-repetition/binding`, WebAssembly) [unverified: bundle size and speed on the owner's laptop]. New parameters are adopted only if they lower log loss by at least 2% on the most recent 20% of reviews, held out. Adoption is a settings event, so the Artifact receives the parameters with the next import; the Artifact never runs the optimiser.
- **Calibration report** (You, Stats): a 10-bin reliability chart of predicted $R$ against outcomes for counted standard reviews, with counts per bin and log loss against a baseline that always predicts the learner's overall success rate; and a table of every paper's forecast expected score against its actual score.
- **Fallback.** If, after 1,000 reviews, the model's log loss is worse than the baseline's, scheduling switches to fixed intervals of 3, 7, 21, 60 and 150 days, the map shows the recent success rate per skill, and You says so plainly. The next optimiser run that beats the baseline switches back.
- **Model upgrades.** A new FSRS version or parameter set is a rebuild of derived state from the log (section 13.3), not a migration.

### 5.10 Mastery points and XP

| | XP | MP |
|---|---|---|
| Measures | activity | first-try success in unscaffolded work |
| Goes down? | never | never |
| Drives the model or the schedule? | no | no |
| Shown | top bar during lessons; lesson-complete screen | header chip; ghost race; friends board; weekly review |

Tables in sections 12.2 and 12.3. The mastery map and every schedule come from section 5's model; points are a record of effort and accuracy, kept separate so that neither can hide forgetting.

---

## 6. The Redo queue and review sessions

### 6.1 What enters the Redo queue

The curriculum's rule: "Redo every problem you got wrong, one week later and one month later."

| Source | Enters when |
|---|---|
| Lesson quiz | an item is wrong |
| Homework, topic exam, finals-style, GCSE-style and challenge papers, cold sets | a single-mark item is wrong, or a multi-part, code or long-form item earns less than 60% of its marks |
| Weekly probability problem | wrong, or self-rated "failed" |
| Lesson screen | revealed with Show solution (not `trap` screens) |
| Timed medium (1.8) and virtual contests | an unsolved problem (the contest arena's upsolve list) |
| Mock interview | each item the debrief flags (`widgets-finance-games.md` 8.6) |
| Textbook problem sets logged outside the app | each problem the learner marks wrong (section 11.2) |
| Level review | an item is wrong |
| Practice, level check, placement | never: the skill's cards handle them (section 2.6) |

One entry per source item: a new miss on an item already queued restarts that entry's cycle instead of adding a second entry.

### 6.2 Dates

With $D_0$ the study day of the miss and $D_1$ the study day the first redo was done:

| Step | Due on study day | If right | If wrong |
|---|---|---|---|
| First redo | $D_0 + 7$ | second redo scheduled | the cycle restarts from this day |
| Second redo | $\max(D_0 + 30,\ D_1 + 14)$ | the entry leaves the queue | the cycle restarts from this day |

- The 14-day floor stops a late first redo from putting the second one days later.
- Entries never expire. Overdue entries sort first, oldest first. An entry more than 21 days overdue shows its age on Today ("3 redo problems are over three weeks late").
- Every in-app redo is a counted review for its skill's card (section 5.3). A repeated authored item can grade at most Good, because the learner may remember the answer.

### 6.3 What comes back

| Original | Redo |
|---|---|
| A generator instance | A fresh variant: same generator and level, a new seed, never a parameter point the learner has seen, never the exam reserve |
| An authored item | The same item at its current `rev` (`CONTENT-FORMAT.md` 4.4 covers revisions and retirement) |
| A code drill | The same drill from its starter code, not the learner's last attempt |
| A long-form item | Its **sibling**: the same skill in a different story (`Item.sibling`, required on every long-form homework and paper item, `CONTENT-FORMAT.md` 3.2), with a blank editor, marked against its rubric. An item with no sibling (outside homework and papers) returns as itself and its review grade is capped at Hard, because the learner has read its model answer |
| A textbook problem | The reference ("Blitzstein and Hwang, exercise 2.12"); the learner redoes it in the book and marks it right or wrong, labelled self-reported; no card update |

### 6.4 The daily review session

Today's Review card ("Review: 6 due, about 18 minutes") opens one interleaved session.

**Daily budget** = the week's Review block in minutes divided by the planned study days (6 by default): 20 minutes at 15 hours a week. The learner can always continue past it.

**Order of filling:**

1. Redo entries due, overdue first, then by due date. Entries whose skill belongs to the current main item are counted towards Main, not Review (section 6.5).
2. Standard cards due in the `active` tier, lowest retrievability first.
3. Standard cards due in the other tiers. Among those, prefer a card whose skill `encompasses` other due cards (its implicit credit may clear them), then the lowest retrievability.
4. A due card with a Redo entry due within 7 days is not served separately: the redo covers it.

**Item for a card review:** a generator variant at difficulty 3 from the practice pool, at a parameter point the learner has not seen; otherwise a bank item with `use: review` not seen in the last 60 days; otherwise the least recently seen. Never the exam reserve or held-out items.

**Interleaving:** never two consecutive items with the same primary skill; alternate topics where the queue allows.

**Lesson-start warm-up** (section 4.4) uses the same machinery and counts as review time.

When nothing is due: "Nothing due today." with an optional "Practise your weakest skills" button (practice, not review).

### 6.5 Load: measured and budgeted

**Maintenance reviews** (scheduled reviews after a card's first 90 days; earlier reviews are assumed to come from organic in-topic work), simulated with FSRS-6 default weights through `ts-fsrs` 5.4.2 with fuzz and short-term steps off, the first review Good, each later outcome drawn from the model's own retrievability, 3 minutes a standard review and 5 minutes a stretch review, seed 777, path weeks $= 3{,}100 / H$. **Rerun by the `docs/PLAN.md` review on 7 October 2026** [simulated]: draft 2's run is reproduced within 4%, then repeated at level grain with cards created across each item's own span (4 per level over the 377 counted levels), and with the `core-interview` tier of section 5.4:

| Setting (15 h a week unless stated) | Cards | Total hours | Mean h a week | Last 26 weeks | Highest 4-week mean |
|---|---|---|---|---|---|
| Draft 2 reproduced: 1,500 cards evenly, tiers 0.90 / 0.85 / 0.80 by card age | 1,500 | 219 | 1.06 | 1.65 | 1.94 |
| Flat 0.90, 1,500 cards | 1,500 | 380 | 1.84 | 3.16 | 3.85 |
| Level grain, tiers | 1,508 | 233 | 1.13 | 1.69 | 2.09 |
| Level grain, tiers 0.90 / 0.80 / 0.70 | 1,508 | 164 | 0.79 | 0.99 | 1.25 |
| **Level grain with `core-interview` (0.5, 1.5): standard 0.90 for life, stretch 0.80 (chosen)** | **1,632** | **299** | **1.45** | **2.32** | **2.71** |
| As chosen, non-core dormant lowered to 0.75 by the balancer | 1,632 | 280 | 1.36 | 2.28 | 2.63 |
| As chosen, plus 1.6 (researcher track) | 1,692 | 323 | 1.56 | 2.79 | 3.03 |
| As chosen, 10 h a week (310 weeks) | 1,632 | 405 | 1.31 | 1.85 | 2.61 |
| As chosen, 25 h a week (124 weeks) | 1,632 | 198 | 1.60 | 2.40 | 2.77 |
| The sample lessons' grain: 3.75 skills a lesson, 2,044 lessons | 7,665 | 1,140 | 5.52 | 9.04 | 9.91 |

Implicit repetition (section 5.5) will lower every figure by an amount that depends on how many `encompasses` edges authors write; it was not simulated. Topics added by `canon-gap.md` add cards in proportion to their levels.

**Redo load** [inferred: counts from `docs/CURRICULUM.md` 0.1 for the 2,044 counted lessons; error shares assumed]:

| Source | Attempts over the path | Share wrong (assumed) | Misses |
|---|---|---|---|
| Lesson quizzes (2,044 lessons, 4 items) | 8,180 | 15% | 1,230 |
| Level reviews (377 levels, 8 items) | 3,020 | 20% | 600 |
| Homework (373 sets, 8 items) | 2,980 | 30% | 890 |
| Papers (about 50 sittings with retention and cumulative papers, 22 items) | 1,100 | 25% | 280 |
| Weekly problems (about 170 weeks, 3 a week) | 510 | 40% | 200 |
| Revealed lesson screens (about 12,300 task screens) | 12,300 | 5% | 610 |
| **In-app total** | | | **about 3,800** |

With two redos per miss and a restart on about a quarter of first redos and a sixth of second redos, each miss costs $E$ redo attempts, where $E = 1 + \tfrac14 E + \tfrac34\left(1 + \tfrac16 E\right)$, so $E = 2.8$: about 10,700 attempts, or about 450 hours at 2.5 minutes, about 1.75 hours a week on average at 15 hours a week. Textbook problem sets add their own redos on top, in the book.

**Finding.** Most redo is current-topic work: a 7-day redo almost always falls inside the topic being studied, and a 30-day redo does in the long topics. Taking two thirds of redo as current-topic [assumed], the Review block holds about 0.6 h of older redo plus maintenance of 1.45 h a week on average and 2.3 h in the last half-year: about 2.05 h on average and 2.9 h late, against a 2-hour block. The curriculum's 9/3/2/1 split therefore fits on average with a little borrowing and needs nearly the full hour of borrowing late in the path; on the researcher track with 1.6 held as core-interview it exceeds it by about 0.4 h. Three rules absorb the excess:

1. **Redo of current-topic problems counts as Main.** Re-solving last week's probability problems while studying probability is main-subject work. Review holds older material.
2. **Review may borrow from Main** when the week's review demand exceeds the block: up to 1 hour a week by default (Settings: off, up to 1 h, up to 2 h). Redo and review are solving, so the 60% rule is unaffected.
3. **The load balancer** (section 5.4) lowers non-core dormant retention to as little as 0.70 before any borrowing beyond the setting is proposed; core-interview cards are never lowered.

Anything still over the budget is shown as review debt with its minutes; nothing is dropped silently. The forecast (section 8.7) absorbs the cost through the pace factor. The weekly review shows the real load from week one, which replaces these assumptions. [Decision for the owner, `docs/PLAN.md` 12 decision 9: keep 9/3/2/1 with borrowing (recommended), or move to 8/3/3/1, from Stage 2 on the researcher track.]

---

## 7. Placement and test-out

### 7.1 Onboarding placement

Replaces design research 7.6 step 4's "5 to 8 adaptive problems" with two ladders, at most 14 items and about 12 minutes. No feedback during, a summary at the end (design research 7.6), Bertie off, untimed on screen but timed for the record.

**Maths ladder:** 16 anchor skills in curriculum order, two items each at difficulty 3.

| # | Anchor | Topic | # | Anchor | Topic |
|---|---|---|---|---|---|
| 1 | Fraction arithmetic | 0.1 | 9 | Trigonometric ratios and identities | 0.3 |
| 2 | Percentages and ratio | 0.1 | 10 | Sequences and series | 0.3 |
| 3 | Powers, roots and standard form | 0.1 | 11 | Binomial expansion and counting | 0.3 |
| 4 | Linear equations | 0.2 | 12 | Vectors | 0.3 |
| 5 | Simultaneous equations | 0.2 | 13 | Derivatives and optimisation | 1.3 |
| 6 | Quadratics | 0.2 | 14 | Integrals and areas | 1.3 |
| 7 | Functions and graphs | 0.2 | 15 | Matrices and linear systems | 1.4 |
| 8 | Exponentials and logarithms | 0.3 | 16 | Conditional probability | 1.5 |

```
lo = 1; hi = 16; passed = 0; asked = 0
while lo ≤ hi and asked + 3 ≤ 10:
  k = ⌊(lo + hi) / 2⌋
  ask 2 items on anchor k (asked += 2); if exactly 1 is right, ask a third (asked += 1)
  if at least 2 right: passed = max(passed, k); lo = k + 1
  else: hi = k - 1
```

**Code ladder:** four anchors, one item each, stopping at the first miss: (1) files, folders and the terminal (choice); (2) predict the output of a short loop with a condition; (3) write a three-line function on a list (runs on any runtime, including none: graded by predicted outputs for given inputs); (4) predict the result of a NumPy or pandas expression.

**Outcome.**

- The suggested start is the first topic containing an anchor above `passed`. Topics below it are offered for test-out (section 7.3).
- Priors: anchors at or below `passed` and the `requires` closure below them get standard cards (section 5.8); anchors above get nothing.
- Placement never marks anything complete. Only papers and exit parts do.
- It can be re-run from Settings; a re-run adds priors only where no card exists, and never removes evidence.

### 7.2 Stage entry: sit the exit test first

The curriculum: "Sit each stage's exit test first. Pass it and you skip the stage. Fail it and you have a list of what to study." On entering a stage (at onboarding, or when the previous stage closes) the stage page leads with "Sit the exit test first", listing the gate instruments and their total time.

- **Recommended** when the placement anchor lies beyond the stage's midpoint or the learner says they have studied this material before; otherwise shown as optional with its time ("about 3 hours").
- The first sitting of a stage paper before the stage's lessons is a **diagnostic sitting**: no cool-down, no XP for a fail (a diagnostic is a measurement, not study), full credit for a pass. There is one diagnostic sitting per stage paper; any later sitting carries the normal cool-down and remediation (section 3.8).
- A failed diagnostic produces the study list: every skill below 60% of its marks, grouped by level, with "Start at 0.2, Level 3" as the action.
- Confirm instruments (real papers) come after the gates, as everywhere.

### 7.3 Topic test-out

Any topic exam can be sat before its lessons.

- **Pass:** the topic exam part is met; every lesson in the topic shows "Tested out"; their hours are credited (7.4); the topic's remaining exit parts appear as the next actions.
- **Fail:** the first such sitting is the topic's one diagnostic sitting (no cool-down); a second sitting before or after the lessons carries the normal cool-down and remediation. Levels whose skills scored at least 80% of their marks are marked "Suggested skip": the learner can take each level's check to skip it, or study it. Result screens after a fail withhold held-out long-form model answers (section 3.7), so the pool stays fresh for the resit.

### 7.4 Credited hours

Tested-out and skipped units keep their estimated hours as **credited**, separate from **earned**. Progress shows both ("Earned 412 h, credited 60 h"); the forecast removes credited hours from what remains; spent hours are never credited.

---

## 8. The weekly plan and progress against the path

### 8.1 Blocks from weekly hours

The curriculum's 15-hour week is Main 9, Build 3, Review 2, Mental 1. For any goal $H$ (3 to 40 hours; presets 5, 10, 15, 25):

- Mental $= 1$ hour (six days of 10 minutes), or 0.5 hours when $H < 8$.
- With $R = H - \text{Mental}$: Build $= q(3R/14)$ and Review $= q(2R/14)$, where $q$ rounds to the nearest quarter hour (halves up); Main $= R - \text{Build} - \text{Review}$.
- The blocks therefore always sum to $H$, and at 15 hours they are exactly the curriculum's 9/3/2/1. Draft 1 rounded all three blocks and its table did not sum at 5 and 25 hours.

| Goal | Main | Build | Review | Mental |
|---|---|---|---|---|
| 5 h | 2.75 | 1.0 | 0.75 | 0.5 (Daily 5) |
| 10 h | 5.75 | 2.0 | 1.25 | 1.0 |
| 15 h | 9.0 | 3.0 | 2.0 | 1.0 |
| 25 h | 15.25 | 5.25 | 3.5 | 1.0 |

[Computed by script, section 0.2.] Review may borrow from Main (section 6.5).

### 8.2 What each block holds

| Stage | Main | Build | Mental |
|---|---|---|---|
| 0 | 0.1, then 0.2, then 0.3 (whose courses S and C carry the GCSE geometry and statistics, section 2.11) | 0.4 until its exit part is met; then the code companions of the current maths level (short Python checks of the maths, one optional drill per level from 0.2 onwards) | The 0.5 course's six lessons in the first weeks, then the Daily 10 |
| 1 | The current numbered item, 1.1 to 1.9 in order; 1.7 alongside 1.3 to 1.6; the weekly probability problems from 1.5 (0.75 h) | Code companions for the current topic, committed to the learner's own repository every week (curriculum: "From Stage 1, something is committed every week"); the 1.1 and 1.2 exit projects | Daily 10 |
| 2 | The track's order of its Stage 2 topics (section 8.9: 2.1, 2.2 and 2.3 today; the proposed 2.0a to 2.2c if accepted) | 2.4 contests (one a week, once 100 algorithm problems are solved) and project code | Daily 10; one 80-in-8 a week |
| 3 | 3.1, then 3.3 (3.2 optional, its hours not counted) | The replication project | Daily 10; two 80-in-8 a week |

**Weekly commit (from Stage 1).** The Build block is marked done for the week when a commit is logged: a paste of `git log -1 --format='%h %cd %s'` checked for a date inside the week, or a self-reported repository link. Once `1.2.exit` is met, the weekly review asks for this every week (`stage1-python-tools.md` decision 17); a missed week is listed, never penalised.

### 8.3 Alongside items

An alongside item $A$ running beside main items $B_1, \dots, B_k$ takes the share $f = h_A / (h_A + \sum_i h_{B_i})$ of the block it lives in, where $h$ are curriculum hours.

| Item | Lives in | Runs beside | Share at 15 h a week |
|---|---|---|---|
| 0.4 Computer basics (40 h) | Build | from week 1 | all of Build until done (about 13 weeks) |
| 0.5 Mental arithmetic (20 h) | Mental | from week 1 | all of Mental |
| 1.7 Finance basics (100 h) | Main | 1.3 to 1.6 (720 h) | $100/820 \approx 12\%$ of Main, about 1.1 h a week |
| 2.4 Contests (140 h) | Build | the whole of Stage 2 | up to 2.5 h of Build a week |
| Weekly probability problems | Main | from 1.5 to the end | 0.75 h a week |

### 8.4 Sessions and the 60% rule

Main is cut into sessions: 3-hour sessions when Main is at least 6 hours (the curriculum's "three 3-hour sessions"), otherwise 1.5-hour sessions. Each session's agenda is filled from the current item's next-up sequence:

1. lessons not yet done (their estimates);
2. the level review and homework items when a level's lessons are done;
3. the level's **companion work** from content: textbook sections and exercises from the topic's one resource, with estimated hours (section 17);
4. exam preparation (practice on the three weakest skills of the coming paper) when the topic exam is next;
5. outstanding exit work of the previous item (section 8.5).

Each agenda keeps at least 60% of its minutes on solving. Today shows the agenda as a suggestion: "Session 2 of 3: Conditional Probability lessons 4 to 6 (35 min), Blitzstein and Hwang 2.4 exercises 18 to 30 (1 h 40 min), Homework 2 items 1 to 4 (45 min)."

**The 60% rule** (curriculum rule 2). Solving: graded in-app work (task screens, items, drills, papers, weekly problems, speed formats) and outside work of kinds `problem-set`, `contest`, `mock`, `project-work` and `algo-problem`. Reading: lesson non-task screens and outside `reading`, `video` and `lecture`. The share over the last 28 days shows on the weekly review; below 60%, Today says so ("Problems were 48% of your study this month; the curriculum asks for 60%") and next week's agendas swap companion reading for exercises until the share recovers.

### 8.5 Order inside a stage and between stages

- **Inside a stage.** Main moves to the next numbered item when the current item's topic exam is passed (or, for items without one, when its exit parts are met). Outstanding exit work of earlier items (real papers, problem-set logs, counters) gets one Main session a week until met.
- **Inside an item: the soft gate per level** (revised by the `docs/PLAN.md` review; consistent with decision 25, so nothing locks). The next level's lessons enter Main only when the current level review scored at least 70%, or its homework at least 60%, or a remediation set built as in section 3.8 on the level's weak skills has been done. Until then the agenda leads with that remediation, and the course map says "Ready when level H2 is secure". Opening the next level anyway asks once and records an override, which the weekly review lists, as the stage rule does. This is the owner's lesson-creator rule "never move to the next module until the quick check is passed", applied at level grain.
- **Between stages.** The planner never puts the next stage's work into Main or Build before the current stage's exit is met (curriculum rule 3), except the 1.9 track deferral. Lessons of later stages stay open (no locks); opening the first one asks once, "The curriculum's rule is no exit test, no next stage. Open anyway?", and records an override that the weekly review lists.

### 8.6 Measuring time

- **In-app:** active time per unit: seconds with the app visible and an input within the previous 120 seconds [our choice]. Papers count wall-clock minus pauses.
- **Outside:** the learner's own minutes per log entry (section 11).
- **Block attribution:** current-item lessons, items, homework, papers, weekly problems and current-topic redos go to Main; other redos and review sessions to Review; code companions, projects and contests to Build; speed formats to Mental. Outside entries go by kind and topic.

### 8.7 Earned hours, pace and forecast

- **Estimates.** Every unit carries an estimate: lessons (their minutes), level reviews and homework (summed item estimates), companion work (content), papers (their minutes), exit parts (`estHours`). CI checks that each topic's estimates sum to within 10% of its curriculum hours (section 17).
- **Earned** = estimates of completed units (lesson completed, level review done, homework submitted, companion work logged done, topic exam passed, exit part met), **scaled per item by its estimate share**: an item's earned hours are (estimates completed / the item's estimate total) $\times$ its curriculum hours, so a completed item reads 100% of its hours even though redo and spent-only work carry no estimates (revised by the `docs/PLAN.md` review).
- **Credited** = estimates of tested-out and skipped units (section 7.4).
- **Spent** = in-app active time, paper time and outside minutes.
- **Mapped spent** = spent minus habit time. The curriculum says its two habits "are not on the map": the Daily 10 once 0.5's 20 hours are earned, and the weekly probability problems, count as spent hours and appear in the weekly review, but leave the pace factor alone. Without this, the Daily 10 alone would make every learner look about 7% slower than they are.
- **Path length** $P$ = the curriculum hours of every topic the learner's track marks core, read from curriculum data (`CONTENT-FORMAT.md` 3.2 `Track`): 3,100 hours on every track today; 3,655 to 3,905 if the owner accepts every `canon-gap.md` proposal. Electives the learner adds join $P$ when added.
- **Pace factor** $k$ = mapped spent / earned over the last 8 weeks (1.0 until 20 hours are earned).
- **Forecast**: remaining $= P - \text{earned} - \text{credited}$ (and the same per stage); weeks left $=$ remaining $\times\, k / \bar h$, where $\bar h$ is the mean weekly mapped hours over the last 4 weeks, or the goal minus the Mental block before 4 weeks of data.

Shown on You and in the weekly review: "Earned 412 h of 3,100 (13%), credited 60 h, mapped 455 h: pace factor 1.10. At your last 4 weeks' 13.2 mapped hours a week: Stage 1 exit around January 2029, the whole path around December 2030. At your 15 h goal (14 mapped): December 2028 and September 2030." [Example figures, computed from the formulas from a start on 6 October 2026.]

### 8.8 The weekly review

Opens on the first visit of a new week (Monday 04:00 local), and from You at any time:

- last week's hours by block against the plan, with borrowing shown;
- solving share over 28 days;
- MP against the ghost (section 12.4);
- redo done and still due; review debt if any;
- papers sat and exit parts met; overrides of the stage rule;
- next week's plan with **Accept** or **Adjust** (goal hours, pinned topics, a planned break);
- **reliance figures** (`AI-TUTOR.md` 9.7): the share of screens resolved after a tutor reply, the hint-before-attempt rate, and per skill the gap between assisted screen success and unassisted quiz and redo success; the marking **calibration score** (mean gap between the learner's blind marks and Bertie's, section 3.5); and, while the reliance check is on (`docs/PLAN.md` 12 decision 11), the 30-day redo success on skills where Bertie was switched off against the rest.

Bertie's weekly recap is a P1 addition using `AI-TUTOR.md` 2.9's recap mode with the week's record as input.

### 8.9 Plan data

Track orders, alongside rules and block homes are content, in `content/plan.yaml`, validated by the content schema:

```yaml
zq: 1
stages:
  - stage: 2
    order:
      researcher: [top.ml, top.ts, top.projects]       # 2.1, 2.2, 2.3 (projects 1, 2, then one more)
      trader:     [top.ts, top.ml, top.projects]       # projects: options dashboard first
      developer:  [top.projects, top.ml, top.ts]       # projects 1 and 4 in C++ first
    projectOrder:
      researcher: [backtest, alpha, options]
      trader:     [options, backtest, alpha]
      developer:  [backtest, market-data, alpha]
alongside:
  - { item: top.finance-basics, block: main, beside: [top.calculus, top.linalg, top.probability, top.statistics] }
  - { item: top.contests, block: build, beside: stage-2, capHoursPerWeek: 2.5, startsWhen: 'algo-solved >= 100' }
  - { item: top.computer-basics, block: build, beside: stage-0 }
  - { item: top.mental-arithmetic, block: mental, beside: stage-0 }
habits:
  weeklyProbability: { from: top.probability, hoursPerWeek: 0.75 }
deferrals:
  - { exitPart: '1.9.exit', toStage: 2, tracks: [trader, researcher] }
```

The orders above are proposals from the curriculum's track table; the owner edits them as data. Track keys are track names (the last segment of a `trk.*` id, `CONTENT-FORMAT.md` 3.2), so a fourth track (`canon-gap.md` P14) or a new Stage 2 item (2.0a to 2.2c) is a data change: which topics a track holds lives in the curriculum file's `Track` entries; the order in which the planner serves them lives here.

---

## 9. Daily mental arithmetic

The curriculum asks for 10 minutes a day from the first week, Zetamac 25 to leave Stage 0, Zetamac 50 and the 80-in-8 format for Stage 3. The widgets are `speed-drill`, `strategy-trainer` and `times-table-grid` (`widgets-stage0.md` 11.1 to 11.3); this section sets the routine, the targets and the record.

### 9.1 The Daily 10

| Step | Minutes | Widget | What it is for |
|---|---|---|---|
| 1. Cold run | 2 | `speed-drill`, Zetamac format | **The day's official score.** First thing, no warm-up, as in a test |
| 2. Targeted deck | 3 | `strategy-trainer` practise phase on the 12 weakest facts (section 9.4), with feedback and the strategy shown after a miss | Fix the slow facts |
| 3. Second run | 2 | `speed-drill`, Zetamac format | Practice score; shows the warm effect |
| 4. Stage deck | 2 | `speed-drill` deck: Stage 0 and 1, fractions to decimals, squares, percentages, estimation; Stage 2 and 3, decimals and missing-operand items in the 80-in-8 style; chain mode once a week | Breadth beyond Zetamac |
| 5. Summary | 1 | end screen | Cold score against the 7-day median and target, the slowest facts, the trend |

- **Daily 5** (goals under 8 hours): steps 1, a 2-minute step 2, and 5.
- **First weeks of Stage 0:** the 0.5 course's six lessons replace steps 2 and 4 until they are done; the cold run starts on day 1, so the baseline is recorded.
- **Tutor:** after the session only (`widgets-stage0.md` 11.1).

### 9.2 Formats

**Zetamac** (defaults [recalled, unverified: the site is blocked from here]): addition 2 to 100 plus 2 to 100; subtraction as additions in reverse; multiplication 2 to 12 times 2 to 100; division as multiplications in reverse; 120 seconds; a correct answer is accepted the moment it is typed; the score is the number correct. The ranges are configuration.

**80-in-8** (default configuration, from the most commonly reported Optiver format [sourced from search summaries of quantvault.org and quantt.co.uk; unverified with the firm]):

| Setting | Default |
|---|---|
| Items, time | 80 items, 480 seconds |
| Answer | multiple choice, 5 options [our choice: option count unverified]; distractors from common slips (a power of ten, a transposed digit, a sign, the wrong operation), so guessing has negative expected value under the penalty |
| Scoring | $+1$ correct, $-1$ wrong; net score shown |
| Navigation | no skipping, no going back |
| Content | integers, decimals and fractions; direct ("373 + 57") and missing-operand ("66 × ? = 138.6") |
| Practice variant | free entry, Skip allowed (the Stage 0 catalogue's original design) |
| Goal | net 55 (a commonly reported pass line), then 70 [same sources; unverified] |

**Run rules for both:** a hidden tab voids the run (`widgets-stage0.md` 11.1); untimed mode never counts and says so; the input device is recorded. Touch runs count for the streak, XP and the practice chart; exit metrics use physical-keyboard runs only, because firm tests are taken on a computer [inferred].

### 9.3 Targets and exit rules

- **Zetamac exit** (`s0.zetamac` at 25, `3.3.zetamac` at 50): the median of the cold scores from the last 7 study days (one per day), keyboard only, with at least 5 such days. One lucky run never passes; a bad day never fails a run of good ones.
- **80-in-8 goal:** the median net score of the last 5 sittings at 55 or more. Not a curriculum exit; shown as a goal and an achievement.
- **The chart** (You, Stats): daily cold scores as dots, the 7-day median as a line, horizontal lines at 25 and 50, and the date each milestone (25, 30, 35, 40, 45, 50) was first reached by the median.

### 9.4 The fact model

| Key family | Keys |
|---|---|
| Multiplication facts | $a \times b$ for $2 \le a \le b \le 12$ (66 keys), plus `a × two-digit` for each $a$ from 2 to 12 (11 keys) |
| Division | the reverse of each multiplication key |
| Addition and subtraction | by shape: digits of each operand (1 and 1, 2 and 1, 2 and 2) and whether it carries or borrows (12 keys) |
| Decks | fraction-to-decimal anchors (halves to twelfths), squares to 30, common percentages |

Per key: an exponentially weighted mean latency of correct answers ($\alpha = 0.2$), errors among the last 20, and the last time seen. **Weakest** = the highest latency $\times (1 + 2 \times \text{error rate})$ among keys seen at least 3 times; two of every 12 targeted items explore keys seen fewer than 3 times. The model is derived from the per-item records inside each run's event and feeds `times-table-grid`'s heat map.

### 9.5 Across the stages

| Stage | Daily | Weekly |
|---|---|---|
| 0 | 0.5 course, then the Daily 10 at Zetamac defaults | none |
| 1 | Daily 10; stage deck adds estimation | one chain session |
| 2 | Daily 10; stage deck in the 80-in-8 style | one 80-in-8 sitting replaces a Daily 10 |
| 3 | Daily 10 | two 80-in-8 sittings; an "interview day" option runs two cold runs at different times of day |

---

## 10. The weekly probability problems

The curriculum: "three interview-style probability problems a week from item 1.5 onwards". The widget is `puzzle-workbench` (`widgets-finance-games.md` 8.1); the bank is its `problem-bank` service.

### 10.1 Cadence

- Starts on the Monday after the learner completes the first lesson of 1.5, and runs to the end of the path. If the owner adopts the earlier habit (`docs/PLAN.md` 12 decision 12), one `original` problem a week runs from 0.3 level C4, built on 0.3 course C, rising to three at 1.5.
- Three problems are released at the start of each study week (Monday 04:00 local), aiming to be done by Sunday. About 15 minutes each: 0.75 hours of Main.
- **Carry-over:** unfinished problems stay open into the next week. At most 6 are open at once: a new week releases only as many as fit. A problem open for more than 14 days moves to "Skipped", where it stays available, with no XP, streak or redo effect.

### 10.2 The bank

Each problem carries: its pattern skills (`pattern: true`, section 4.1), the topic skills it needs, a difficulty from 1 to 5, a source tag (`mosteller`, `zhou`, `crack`, `joshi`, `jane-street-guide`, `original`), for every recreated problem an `imitates` reference naming the book problem it follows (`zhou-4.12`, `mosteller-17`), a held-out flag (held-out problems serve only cold sets), an exact answer, a worked solution with alternatives, diagnosed wrong answers and a linked widget configuration. Recreated problems are cited "after Mosteller, problem 1" and never copied (`widgets-finance-games.md` decision 9). Parametrised families (waiting times for patterns, gambler's ruin, dice and card expectations, geometric probability, order statistics, coupon collecting, optimal stopping) have exact solvers and simulation checks in CI.

### 10.3 Selection

```
taught(p)     = every topic skill p needs has at least one card
eligible(p)   = taught(p) and p never attempted and not held out
level(pat)    = highest difficulty with at least 2 of the last 3 attempts on that pattern solved; 2 if none
books(stage)  = stage 1: original · stage 2: original · stage 3: original, jane-street-guide, then crack (joshi on the Developer track)
                # no problem that imitates Zhou chapters 4 or 5, or any Mosteller, Crack or Joshi problem, is eligible before 3.3;
                # imitations of Zhou chapters 4 and 5 serve only the held-out cold set, never the weekly bank

consolidation = a pattern attempted before with a success rate below 80% (else the least recently practised), at level(pat)
new           = an eligible pattern never attempted, at difficulty 2
stretch       = any eligible pattern at level(pat) + 1
rules         = three different patterns; no pattern used in the previous 2 weeks except in the consolidation slot;
                prefer books(stage), then any book; ties broken by hash32(weekId, problemId)
```

The week's three are recorded in a `weekly-assign` event on first open. Selection is seeded by the week id, so two devices that open the week before syncing usually pick the same three; if they differ, the fold keeps the earliest event.

### 10.4 Modes

| Stages | Mode | Rules |
|---|---|---|
| 1 and 2 | `weekly` (warm) | Hints after the first attempt, and from Stage 1 only after the learner writes a one-line plan; Bertie after grading (decision 17); "See the picture" after solving or the third hint; the first try is what counts for MP and the card |
| From 1.5: one of the three each week; from Stage 2: two | `cold` | A visible clock, no hints, no Bertie, one attempt, the plan spoken aloud through `voice-capture` where the device allows (a P1 primitive, built with the 1.7 wave, which runs before 1.5), then the full solution (`puzzle-workbench` cold mode) |
| 3 | `cold` | All three cold |

From Stage 2, sealed tutor calls are capped at 20 a day, shown to the learner ("Bertie: 14 of 20 today"), so support fades as the path nears the interview.

After each problem the learner rates it easy, hard or failed. "Failed" or a wrong first try adds it to the Redo queue; "hard" grades the card Hard (section 5.3).

### 10.5 The road to the 3.3 exit

The weekly habit builds towards `3.3.zhou` through patterns, not book problems: before 3.3 every weekly problem is `original`, so the learner meets each Zhou-style pattern in new stories and meets the books themselves cold, in the curriculum's 3.3 order (Mosteller, then Zhou, then Crack, then Joshi), through the book-log. The exit then asks for the cold set in the app and the book-log of the real chapter (section 11.9).

---

## 11. Work outside the app

Most of the path's hours happen in textbooks, on the learner's own machine and with other people. The app records that work honestly so the plan, the hours and the exits can see it.

### 11.1 Rules

1. **Self-report is labelled self-report** everywhere it appears: the log, the hours bar ("of which 6.5 h self-reported"), the exit checklist, the learning record.
2. **Evidence is optional and cheap:** up to 3 links (a repository, a scanned script, a Codeforces profile) and a note. The app never fetches or opens a link by itself; the Artifact cannot.
3. **Outside work never earns MP and never updates the mastery model.** Both stay calibrated against marked outcomes.
4. **Nothing is invented.** A count the app cannot see (the number of problems in a Zhou chapter, a Codeforces rating) is entered by the learner once and shown as entered.

### 11.2 The log entry

```ts
const OutsideEntry = z.object({
  id: z.string(), date: z.iso.date(), minutes: z.number().int().min(1).max(720),
  kind: z.enum(['problem-set', 'reading', 'video', 'lecture', 'project-work', 'algo-problem',
                'contest', 'competition', 'mock', 'real-paper', 'book-log', 'other']),
  topic: Id('top').optional(),
  source: z.union([Id('src'), z.string().max(120)]).optional(),     // a content source id or free text
  ref: z.string().max(80).optional(),                                // "Chapter 2, exercises 1 to 20"
  done: z.array(z.string().max(40)).max(200).default([]),            // problem references
  wrong: z.array(z.string().max(40)).max(200).default([]),           // each becomes an outside Redo entry
  score: z.tuple([z.number().min(0), z.number().positive()]).optional(),
  links: z.array(z.url({ protocol: /^https?$/ }).max(500)).max(3).default([]),
  note: z.string().max(2000).optional(),
  attest: z.boolean().default(false),                                // required for entries that satisfy an exit part
  exitPart: z.string().optional(),
}).strict();
```

Problem references accept ranges ("1-20" expands to 20 references) and lists. Every field is validated at entry and again on import (section 14.2). Edits and deletions are events of their own; history keeps both.

**Quick log** from Today: "I did outside work" opens a three-field sheet (kind, minutes, topic) with "More" for the rest. Companion work suggested by the plan pre-fills source and reference.

### 11.3 What outside work feeds

| Feeds | How |
|---|---|
| Spent hours and blocks | always (section 8.6) |
| XP | 30 per hour, at most 120 a day, labelled self-reported |
| Streak | 30 minutes or more qualifies the day (section 12.1) |
| Redo queue | each `wrong` reference of a `problem-set` |
| Earned hours | companion work marked done (section 8.7) |
| Exit parts | real papers, problem-set refs, projects, mocks, the book-log |
| Friends board | hours (shown as total hours, the self-reported part included) |
| MP, mastery model | never |

### 11.4 Projects

```ts
const Project = z.object({                                            // the learner's record; the brief is content (CONTENT-FORMAT.md 3.2, prj.*)
  id: z.string(), prj: Id('prj').optional(),                           // absent for a project of the learner's own
  kind: z.string().regex(/^[a-z][a-z0-9-]*$/),                         // matches the content Project.kind and the instrument's projectKind
  title: z.string().max(80), repoUrl: z.url({ protocol: /^https$/ }).optional(),
  milestones: z.array(z.object({ id: z.string(), done: z.boolean(), evidence: z.enum(['paste', 'link', 'self']), at: z.number().optional() }).strict()),
  tests: z.object({ passed: z.number().int().min(0), at: z.number() }).strict().optional(),   // parsed from a pasted `pytest -q`
  note: z.string().optional(),                                       // the results-note attempt id
  status: z.enum(['planned', 'active', 'finished', 'dropped']),
}).strict();
```

**Finished** means all four of: a repository URL; tests passing, from a pasted `pytest -q` summary with at least one passed and none failed (paste-verify, `widgets-programming.md` 6.11); a README (attested); and a results note written in `results-note` and marked at 7 of 10 or better with its `sections-complete` and `metrics-consistent` predicates passing (`widgets-finance-games.md` 7.11), which includes the section on what failed (curriculum 2.3). Replications (3.1) also need the note's out-of-sample section, and an exit's `notePredicates` (the P1 checklist, if accepted) add their own sections. The repository URL is stored as text and never fetched; the pastes are the check on both targets (`docs/PLAN.md` conflict 5).

### 11.5 The algorithm problem ledger

- **In-app verified:** each `problem-workbench` problem solved with every hidden test passing, counted once per problem.
- **Self-reported:** LeetCode, NeetCode or other judge problems logged as `algo-problem` entries with the problem URL; the URL path is the identity, so a problem counts once; a submission link is optional evidence.
- **The 150 counter** sums both and shows them apart: "150 solved: 92 verified in the app, 58 self-reported."
- **Timed mediums** for `1.8.exit` use only the app's held-out bank (at least 30 mediums, `widgets-programming.md`), because "fresh" needs problems the learner has never seen.

### 11.6 Contests and competitions

- **Codeforces:** a handle, then one `contest` entry per contest (date, contest, problems solved, rating after). Entries are manual on both targets: the web app's Codeforces API lookup is withdrawn (`docs/PLAN.md` conflict 5), which keeps the CSP's only outside host the tutor proxy. The curriculum's targets show as goals: one contest a week once 100 problems are solved, a rating of 1,400 in the first year of Stage 2. Neither is an exit.
- **Kaggle, IMC Prosperity, Project Euler:** `competition` entries with a link and a result line.
- The in-app `contest-arena` (`widgets-programming.md` 9.1) keeps its own record, labelled "simulated rivals" and "estimate, not a Codeforces rating".

### 11.7 Mock interviews

The `mock-interview` log (`widgets-finance-games.md` 8.6) records each mock: date, rounds, partner type (Bertie, friend, stranger; self-declared), rubric marks with evidence, transcript reference. The exit counts human mocks only (section 2.9). Bertie mocks count as practice, earn XP and fill the Redo queue from their debriefs.

### 11.8 Real papers

```ts
const RealPaper = OutsideEntry.extend({
  kind: z.literal('real-paper'),
  paper: z.enum(['gcse-higher-p1', 'khan-precalc-challenge', 'mit-1801-final', 'mit-1806-final', 'stat110-final']),
  series: z.string().min(3).max(80),                 // "Edexcel June 2023 1H", "Stat 110 Fall 2019 final"
  timedMinutes: z.number().int().optional(),          // the time actually taken
  score: z.tuple([z.number().min(0), z.number().positive()]),
  markedWith: z.literal('official-scheme'),
  attest: z.literal(true),
});
```

- A series counts once, so two Stat 110 finals must be two different series.
- **Aids per paper.** `RealPaper` gains `aids: z.string().max(200)`, filled from the paper's printed rules (for a Stat 110 final, for example, "four double-sided pages of your own notes; no calculator" [check per paper]). The attestation reads: "I sat this paper timed, under its printed rules (aids: …), and typed my working as I went."
- **Sitting.** The paper is sat in the app's long-form editor under its own timer, typed (handwritten marking is P1 and needs image input, which the owner's iPhone view lacks [measured, `spikes/README.md`]). After the timer, the learner pastes the official solution for each question; Bertie marks the typed working against it, and the confirm counts $\min(\text{learner}, \text{Bertie})$ per question as in decision 6. With the tutor off, the confirm stays provisional.
- **Reserved papers.** At the start of 1.5 (and of 1.3 and 1.4) the planner names the reserved real finals and lists the files the learner must not open, because Stat 110's practice finals sit beside the Strategic Practice sets used for homework.
- The entry opens with the paper's expected time (GCSE 90 minutes; MIT and Stat 110 finals 180 [recalled, unverified]).
- **Calibration of our papers:** the app stores each real score beside the learner's latest in-app score on the matching paper. A gap of more than 15 percentage points adds the paper to the content-gap report (`AI-TUTOR.md` 2.10) as "in-app paper may be miscalibrated".

### 11.9 The book-log

`puzzle-workbench` book-log mode (`widgets-finance-games.md` 8.1). For `3.3.zhou` the learner enters the number of problems in the chapter from their own copy once ("this chapter has N problems in my edition"), then logs each problem by reference with its outcome: solved cold, solved with a hint, failed, or **seen** (recognised from earlier). A seen problem leaves both the numerator and the denominator: the part is met when problems solved cold reach 80% of N minus the seen ones, and the record shows how many were seen. Recognising a problem met with hints earlier is recall, not cold solving (revised by the `docs/PLAN.md` review). No problem text is stored.

---

## 12. Motivation

### 12.1 Streaks, rest days and breaks

Design research 6.2 is adopted with these settings:

- **A study day** runs from 04:00 to 04:00 local (configurable 00:00 to 06:00). Each event stores its timezone offset; a day is the local date at the event, computed with that offset, so travel never loses a day.
- **A day qualifies** with any of: a lesson completed; 3 graded first tries in any context; a homework set submitted; a paper sat; the Daily 10 (or Daily 5) completed; 30 minutes or more of outside work logged for that day (self-reported, labelled).
- **The bolt** is a grey outline until the day qualifies, then pear (design research 6.2).
- **Rest days:** one earned per 7 qualifying days, at most 2 held, applied automatically, never expiring.
- **Weekly mode:** the goal is $N$ of 7 days ($N$ from 3 to 7); days beyond the target can miss.
- **Planned breaks:** up to 14 days a year, booked at least one day ahead; they neither break nor extend the streak, and the ghost race skips those weeks.
- **Streak off** hides every streak surface.
- **Multiple devices:** the streak is computed from the merged event log, so a lesson on the phone and a paper on the laptop count for the same day.

### 12.2 XP

| Source | XP | Notes |
|---|---|---|
| Lesson task screen, first try | 15 | the sourced Brilliant value (design research 6.1) |
| Lesson task screen, after a retry | 5 | |
| Lesson task screen, after Show solution | 0 | |
| Lesson completed | 20 | first completion only |
| Perfect lesson | +15 | every task screen first try (design research 6.2) |
| Quiz item correct | 15 | |
| Level review item correct | 15 | first completion of that review; later runs as practice |
| Practice item correct first try | 10 | at most 300 a day from practice |
| Redo correct (in-app or outside) | 10 | |
| Homework submitted | 50, plus 5 per correct item, plus 20 if on time | |
| Weekly problem | 30 solved, 10 attempted | |
| Daily 10 or Daily 5 completed | 20 | once a day |
| New personal best (cold Zetamac or 80-in-8 net) | 10 | |
| Paper sat (topic, finals, GCSE-style, challenge, cold set) | 50; plus 200 on a pass | diagnostic sittings earn only the pass bonus |
| Exit-item sitting | 20; plus 50 on reaching the bar | |
| Stage exit met | 1,000 | |
| Outside work | 30 per hour, at most 120 a day | self-reported |
| Project milestone (paste-verified) | 100; project finished 500 | |
| Mock interview logged with rubric marks | 100 | |
| Level check, placement | 0 | diagnostics |
| Repeating completed content | 0 | |

XP awards are stored on the event that earned them (principle 4).

### 12.3 Mastery points

| Source | MP |
|---|---|
| First try in a quiz, level review, homework, paper, level check or weekly problem | $\operatorname{round}(d \times f)$: item difficulty $d$ times the fraction $f$ of its marks earned |
| Redo correct (in-app) | $d$ |
| Lesson screens, practice, placement, outside work | 0 |

A typical week at 15 hours earns a few hundred MP [inferred]. MP is shown as a header chip, in the ghost race and on the friends board.

### 12.4 The ghost race (replaces leagues)

A single learner has nobody to rank against. Simulated rivals would be fiction shown as competition, and a league of one is a progress bar. The ghost race uses the only true comparison available: the learner's own recent weeks.

- **The metric is MP**, not XP (XP rewards volume; hours already have the weekly goal bar).
- **Ghosts:** "Your usual" is the median MP of the last 4 complete weeks that had at least one qualifying day and no planned break; "Your best" is the highest weekly MP in the last 12 weeks.
- **Pace:** each ghost has a cumulative curve by day of the week (the median, or the best week's, curve), so mid-week the race is fair: "Thursday: 184 MP. Your usual Thursday: 160. Your best week: 305 by Sunday."
- **Display:** one bar on the Today streak card and on You: the learner's marker, the usual ghost, the best ghost, days left. No sounds, no "losing" copy; beating the usual week shows a tick in the weekly review.
- **Starts** after 2 complete weeks; before that the card shows MP this week alone.
- **Off** with the leagues switch (renamed "Ghost race and friends board").

### 12.5 The friends board (shared Artifact only)

When friends open the same Artifact, each keeps a private store under `data/users/<id>/` (section 13.4). A board exists only when at least 2 people on the Artifact have opted in. **Priority P2**: built when a friend actually joins, because the access it needs is the hard part, not the code.

**Who can take part** [sourced: `db.d.ts`, `user.d.ts`]. Saving anything, the friend's own progress included, needs write access to the Artifact's store:

| The owner's plan and the friend | Can the friend save progress and join the board? |
|---|---|
| Team or Enterprise, friend in the same organisation, shared at Contributor or above | Yes |
| Any plan, friend outside the organisation invited **by email as an Editor**, artifact **not** also shared by public link | Yes, with two costs: an Editor can also publish new versions of the app, so only invite someone trusted with it; and an outside Editor "may have" no viewer id, in which case there is no private subtree and the friend runs browser-only |
| Any plan, friend reached through a public link or invited as Viewer or Commenter | No: outside viewers never write. The friend can still use the app with browser-only progress and no board |

On a personal plan the second row is the only route, and the owner's account appears to be a personal one [inferred]. Whether the share menu offers email Editor invitations on the owner's plan is [unverified]. A friend who cannot write is told plainly: "This copy of Zero to Quant cannot save your progress. Ask the owner to invite you as an Editor, or use the web app."

- **Shown:** rank by MP this week, MP, hours this week, a tick for beating your own usual week. Medals for ranks 1 to 3 only when 4 or more people take part. No tiers, no promotion, no demotion: a group of friends needs none of it.
- **Week:** resets Monday 03:00 UTC (one instant for everyone, as design research 6.2 sourced from Brilliant). The week id is the ISO week of the UTC time minus 3 hours.
- **Data:** each participant writes one shared document, `board/<their id>`: `{ week: '2026-W41', mp, hours, beatUsual, stage, updatedAt }`, about 200 bytes, at most once every 10 minutes and only when a value changes. Nothing else leaves the private store.
- **Access rules** (`db` capability; the whole rule set of the Artifact, decision 32):

```js
capabilities: {
  db: { rules: [
    { path: '', read: 'interact', write: 'owner' },          // nothing else is shared; only the owner writes outside the paths below
    { path: 'data/users/{self}', write: 'interact' },        // each person's private progress (siblings stay invisible, the owner included)
    { path: 'board', read: 'interact', write: 'owner' },     // everyone who can write reads the board; only the owner can clean it up
    { path: 'board/{self}', write: 'interact' },             // each person writes only their own entry
  ] },
  user: { scopes: ['profile'] },                             // names resolved at render, never stored
  // sample (AI-TUTOR.md) and downloads (section 14) are declared beside these
}
```

Locking the root also locks every subtree below it unless a deeper rule reopens it, which is why `data/users/{self}` is declared [sourced: `db.d.ts`, which warns that a locked root alone stops everyone below that level writing their own subtree]. A rule at the prefix of a `{self}` rule must set both levels, as `board` does. The owner meets every level, so these rules never limit the owner's own progress.

- **Names** come from `user.profiles()` at render time; only ids are stored (`user.d.ts`: store only ids). Names are set with `textContent`.
- **Opting out** deletes the person's board document at once.
- **Honest limit:** MP is computed on each person's device, so a determined friend could write any number to their own entry. Accepted for a group of friends, and stated on the board's info sheet.

### 12.6 Achievements

Competence only, at most 12 (design research 6.2):

| # | Achievement | Rule |
|---|---|---|
| 1 | Stage 0 complete | every Stage 0 exit part met |
| 2 | Stage 1 complete | every Stage 1 exit part met |
| 3 | Stage 2 complete | every Stage 2 exit part met |
| 4 | Stage 3 complete | every Stage 3 exit part met |
| 5 | First topic exam | first topic exam passed |
| 6 | Zetamac 25 | the 7-day median reaches 25 |
| 7 | Zetamac 50 | the 7-day median reaches 50 |
| 8 | 80 in 8 | the 5-sitting median net score reaches 55 |
| 9 | 150 problems | the ledger reaches 150 |
| 10 | 100 verified drills | 100 distinct code drills passed in the app |
| 11 | Shipped | first project finished (section 11.4) |
| 12 | A year of problems | 52 weeks with all three weekly problems attempted |

### 12.7 Copy and celebration rules

- Celebrations follow design research 4.7: lesson complete, perfect lesson, paper passed (the stamp), stage complete. Bertie acts them out at boundaries only, in the states `BERTIE.md` section 5 defines: `celebrate` on lesson complete and paper passed, `streak` when the count changes, `sleeping` on a rest day ("Rest day. Your streak is safe."), `away` during papers and open homework items. His `celebrate` squares are the only particles anywhere; nothing plays during a problem.
- Every number states what it counts: "MP this week", "of which 6.5 h self-reported", "self-marked pass".
- Never guilt: no "Don't lose your streak", no sad faces, no countdown pressure (design research 6.2). An overdue item is named with its next action and time cost: "Homework 4 is 3 days late. About 50 minutes left in it."
- Failure is information: "Not yet: 62%. The pass mark is 70%. Your remediation set has 18 problems; the resit opens on Friday."

---

## 13. The progress data model

### 13.1 Principle

Progress is an **append-only log of events**. Every other structure (lesson progress, cards, the Redo queue, streaks, XP and MP totals, hours, exit status, the plan) is **derived** by a deterministic fold over the log. Three consequences decide the design:

1. **Merging is a set union.** Two devices, or the Artifact and the web app, each hold a set of events with globally unique ids. Union them and fold: the result is the same whichever side merges first, and merging twice changes nothing.
2. **The model can change without a migration.** A new grade mapping, new retention tiers or a new FSRS version is a rebuild from the same events.
3. **Every document has one writer.** Each device appends only its own events, so the `db` store's last-writer-wins behaviour [sourced: `db.d.ts`] can never drop another device's work.

### 13.2 Events

```ts
interface Envelope {
  id: string;        // `${t.toString(36)}-${dev}-${seq.toString(36)}`: time-sortable, unique per device
  t: number;         // device clock, epoch milliseconds
  tz: number;        // minutes east of UTC at the event (study days, section 12.1)
  dev: string;       // 8 random base-36 characters, generated at first run on this install
  seq: number;       // per-device counter, strictly increasing
  rel: string;       // content release (CONTENT-FORMAT.md 4.5)
  app: string;       // app release
  v: 1;              // event format version
}
```

| Kind | Payload (main fields) | Written when |
|---|---|---|
| `att` | `ctx` (lesson, quiz, practice, review, redo, homework, exam, check, placement, weekly, timed), `ref` (lesson and screen, item, `{gen, v, level, seed}`, drill, set instance, paper attempt, redo entry), `try`, `ans` (at most 2 KB; code at most 16 KB), `verdict`, `marks` as `[earned, max]`, `ms` (active), `hints`, `skills`, `d`, `mc` (diagnosis id), `snap` (section 0.3 rule), `xp`, `mp` | each graded attempt |
| `lsn` | lesson id, `rev`, `op` (start, screen, complete), screen id, `perfect` | lesson progress |
| `hw` | `op` (issue, submit), instance id, set id and `rev`, seeds, due day, late | homework life cycle |
| `exam` | `op` (start, pause, resume, hidden, section, leave, submit), attempt id, exam id (and slot, for an exit-item sitting), served paper, integrity fields (section 3.9) | paper life cycle |
| `mark` | attempt id, the learner's points per rubric point, Bertie's points, changed point ids | a long-form mark confirmed |
| `ment` | format, seed, score, correct, wrong, device input, duration, voided reason, per-item records `[question, entered, ok, ms]` | each speed run |
| `weekly` | `op` (assign, rate), week id, problem ids, rating | weekly problems |
| `out` | `op` (create, edit, delete), an outside entry (section 11.2) or real paper (11.8) | outside work |
| `proj` | `op` (create, update), project fields (11.4) | projects |
| `paste` | check id, parsed fields, a redacted copy of the paste (at most 4 KB, home paths removed) | paste-verify |
| `time` | `ctx`, `ref`, `ms`, `kind` (solving or reading), block | leaving a unit |
| `prior` | source (placement, level check), cards set (section 5.8) | priors |
| `set` | key, value (settings, adopted FSRS parameters, goals, pins, breaks) | a setting changes |
| `plan` | `op` (accept, adjust, override), details | weekly plan and stage-rule overrides |
| `import` | source, kind (full, sync or result code), devices, event count, file hash, the file's `have` map | an import completes |

### 13.3 Derived state

```
state = fold(dedupe(events) sorted by (t, id), migrations, content bundles, rules version)
```

The fold builds: lesson progress and completion states; homework instances and their status; paper states (section 3.10); FSRS cards (section 5); the Redo queue (section 6); generator seen-sets; the fact model (9.4); streak, rest days and breaks; XP and MP totals and weekly series; hours by block and week; earned, credited and spent hours; exit-part status; the ghost curves; achievements; the current plan.

**Properties, each a test (section 16):**

- deterministic: the same event set gives byte-identical state;
- order-independent: any arrival order of the same set gives the same state;
- idempotent: duplicates (same id) are ignored;
- incremental equals rebuild: applying events one by one to a snapshot gives the state a full rebuild gives.

**Late events.** An event that sorts before the newest folded event (another device's work arriving after sync, or an import) cannot simply be appended: the worker re-folds from the newest snapshot that precedes it, or from the start if none does, and swaps the result in when done.

**Budget** [our choice, measured in stage A1]: a full rebuild of a synthetic four-year log (about 86,000 events; about 110,000 on a 3,905-hour track) in under 3 seconds in a Web Worker on the owner's phone; an incremental event in under 2 ms on the main thread.

**Clocks.** Events sort by device time. A device whose clock is wrong by hours can misplace its events in a study day; accepted, because the alternative (a server clock) does not exist in either target. Paper timers use `performance.now()` between visible moments and wall-clock time across reloads, and a backwards clock jump never adds time.

**Snapshots** store derived state with its basis (the highest `seq` folded per device) so a start does not replay the whole log.

### 13.4 The Artifact store

Per viewer, under the private subtree that the `db` capability keeps invisible to every other viewer, the Artifact's owner included [sourced: `db.d.ts`]:

| Path | Documents | Writer | Size cap |
|---|---|---|---|
| `data/users/<uid>/meta` | 1 | the first device, under a lease, once | 1 KiB |
| `data/users/<uid>/log/chunks/<dev>-o<seq>` | 1 per device: the open chunk | that device | 48 KiB plain JSON, at most 200 events |
| `data/users/<uid>/log/chunks/<dev>-s<seq>` | sealed plain chunks waiting to be packed (at most 8) | that device | 48 KiB |
| `data/users/<uid>/log/chunks/<dev>-p<seq>` | packs: 8 or more sealed chunks, gzip then base64 | that device | 192 KiB |
| `data/users/<uid>/log/chunks/<dev>-i<hash>` | imported packs (section 14.2) | the importing device | 192 KiB |
| `data/users/<uid>/state/snapshots/<dev>-<part>` | derived state, gzip then base64, in parts | that device | 192 KiB a part |
| `data/users/<uid>/work/drafts/<instance>` | answers in progress: homework sets, papers, long-form text | the device holding the lease | 64 KiB |
| `board/<uid>` | the friends board entry (opt-in) | that viewer | 1 KiB |

Every chunk document carries top-level fields `dev`, `seqFrom`, `seqTo` and `n` so a start can query only what is newer than its snapshot (`where('dev', '==', d).where('seqTo', '>', basis[d])`). Path parity follows `db.d.ts`: documents at 4 or 6 segments, collections at 5.

**Write cadence:** the open chunk at most every 5 seconds, and at once when a unit completes or the page becomes hidden; a chunk seals at 200 events or 48 KiB; when 8 sealed chunks exist the device writes a pack, waits for the write to resolve, then deletes the 8 (readers deduplicate during the window, so a crash in between is harmless); a snapshot at most hourly, after 500 new events, or when the page hides after 50; drafts every 10 seconds while typing and on blur; the board entry at most every 10 minutes and only on change. Every write awaits the previous write to the same document (`db.d.ts`: one write at a time per document).

**Subscriptions:** the chunks of other devices (one query per known device, at most 4 devices before falling back to a refresh every 60 seconds), the open draft when a homework set or paper is open, and the board while it is on screen. Well inside the 64 allowed.

**Outbox:** each event is written to the local IndexedDB mirror first and its id to an outbox; the id leaves the outbox when the chunk write that carries it resolves, so a failed write loses nothing while the browser keeps its storage. The outbox is bounded only by the device's storage quota; months offline fit [inferred from section 13.6's yearly volume], and the "Saved on this device" chip says how many events wait.

**Lifetime of the store** [sourced: `db.d.ts`]: it survives reloads, republishes and sessions, and it is **erased when the artifact is deleted**. Every learner's progress, the owner's included, lives in it. So a release always republishes to the same URL (`ARCHITECTURE.md` decision 17) and nothing in the release process may delete the Artifact; "start again" means "Delete my progress" (section 15.4), never deleting the Artifact. The weekly backup reminder (section 14.1) covers the rest.

**Device-only mode** (decision 31): Settings, Data, "Keep my progress on this device only" stops every `db` write and subscription and runs on the IndexedDB mirror alone, with the browser-only banner. Turning it off again uploads the mirror's events as import packs (section 14.2), so nothing is lost either way.

### 13.5 The web app store and the interface

The web app keeps the same events and snapshots in IndexedDB (`zq` database: `events` keyed by id with an index on `t`, `snapshot`, `drafts`). It asks for persistent storage (`navigator.storage.persist()`) on first run; if refused, the weekly review reminds the learner to export a backup.

Both targets use one interface:

```ts
interface ProgressStore {
  append(events: Ev[]): Promise<void>;                      // durable locally on resolve; queued for the remote where one exists
  load(): Promise<{ snapshot?: Snapshot; events: Ev[] }>;    // the newest snapshot and the events after its basis
  subscribe(onEvents: (evs: Ev[]) => void): () => void;     // other devices' events (Artifact); a no-op on the web
  saveSnapshot(s: Snapshot): Promise<void>;
  draft(id: string): Promise<DraftHandle>;                   // lease-held on the Artifact
  exportAll(): Promise<Blob>;                                // full backup (section 14.1)
  exportSince(peer: 'artifact' | 'web'): Promise<Blob>;      // sync file: events that peer has not acknowledged
  importFile(text: string): Promise<ImportReport>;           // validated in the data worker (ARCHITECTURE.md decision 10)
}
```

Implementations, at the paths `ARCHITECTURE.md` 4.2 fixes: `DbStore` (`platform/artifact/db-store.ts`, with an `IdbStore` mirror for fast and offline starts), `IdbStore` (`platform/web/idb-store.ts`), `MemoryStore` (`platform/shared/memory-store.ts`, tests and private windows). When the Artifact gives no `db`, no user id, or no write access, or the learner chose device-only mode, it runs on `IdbStore` alone with a standing banner: "Progress is saved in this browser only. Export it regularly." Write access is decided by trying: `user.can('data.write')` speaks for shared documents only and resolves `null` for a viewer from outside the organisation [sourced: `user.d.ts`], so the store attempts its first chunk write and falls back on `invalid_argument`.

### 13.6 Volumes

Estimates for one learner over the whole path [inferred from the counts in sections 0.2 and 6.5; sizes from section 0.2]. Recomputed by the `docs/PLAN.md` review for the 2,148 lessons of `docs/CURRICULUM.md` (2,044 counted plus 3.2's 104), which scales the lesson-driven rows of draft 2's 1,550-lesson model by about 1.39:

| Events | Count | Mean size (JSON) | Total |
|---|---|---|---|
| Lesson screen attempts (about 12,900 task screens, 1.3 tries each; no snapshot) | 16,600 | 250 B | 4.2 MB |
| Quiz, level review, homework, paper, check, weekly, redo and review-session attempts (with snapshot) | 36,000 | 700 B | 25 MB |
| Practice attempts (no snapshot) | 13,900 | 250 B | 3.5 MB |
| Code answers (drills in any context) | 4,200 | 3 KB | 12.6 MB |
| Speed runs with per-item records (four a study day) | 5,000 | 1.5 KB | 7.5 MB |
| Time events | 20,000 | 120 B | 2.4 MB |
| Everything else | 10,000 | 300 B | 3 MB |
| **Total** | **about 106,000** | | **about 58 MB** |

Unscaffolded attempts (rows two and three) total about 50,000, the figure section 4.1 uses. At a planned 3 times compression and base64's 4/3, the log is about 26 MB in about 140 packs over the path (about 5 MB after the first year). The snapshot is about 1.2 MB of JSON (about 1,630 scheduled cards plus core and stretch cards, 2,148 lessons, about 55,000 seen parameter points, the Redo queue, the fact model, weekly series), about 400 KB packed, in 2 or 3 parts. **Documents per learner:** about 170 to 190, against the database's 25,000 [sourced: `db.d.ts`]. Every document stays under the 256 KiB limit by construction. A longer track (up to 3,905 hours) scales these by at most 1.26. The synthetic learner (`tests/synthetic/`) generates this volume, and the fold's 3-second rebuild budget on the iPhone is set against it (`docs/PLAN.md` 3.1).

**Unknown:** the total size cap of one artifact's database [unverified: `db.d.ts` names the cap but not its value]. If it turns out smaller than (participants $\times$ 30 MB, the 26 MB log plus snapshot and drafts), the fallback is a checkpoint: freeze a full snapshot as a base, export packs older than 18 months to a file the learner keeps, and delete them from the store. It is specified here and built only if the bounded probe of `docs/PLAN.md` stage 2 shows it is needed.

### 13.7 Several devices

- **Device ids** live in `localStorage` and IndexedDB. A wiped device gets a new id, which is harmless: it is just another writer.
- **Tabs.** Two tabs on one device share its device id, so only one may write. The tabs elect a writer with the Web Locks API (`ARCHITECTURE.md` decision 26): the lock holder runs the `AppendQueue` and the `db` writes; other tabs read, follow the log through the mirror, and show "Open in another tab" with **Use here**, which asks the holder to release the lock. A paper or homework draft open in a reading tab is read-only.
- **Drafts and papers** use `acquire` leases (60-second TTL, renewed every 20 seconds while open). Another device shows the work read-only, "Open on your other device", with "Take over", which waits for the lease to expire and then acquires it. A paper's clock lives in its events, so every device shows the same time left.
- **Settings:** the latest `set` event by `(t, id)` wins, per key.
- **"First one wins" facts** (the week's problem assignment, a homework issue): the earliest event by `(t, id)`.

### 13.8 Failure behaviour

| Failure | Behaviour |
|---|---|
| A `db` call rejects `unavailable` | Retry once after a random 0.5 to 1.5 s; then keep the events in the outbox and retry with backoff (2, 4, 8 s up to 60 s). A "Saved on this device" chip shows until the outbox empties |
| `resource_exhausted` | Double the write-coalescing interval, up to 60 s; never tighten the loop |
| `quota_exceeded` | Stop creating documents; keep writing the open chunk while possible; show "Your progress store is full" with Export and the checkpoint option |
| `invalid_argument` | A programming error: keep the events in the outbox, record it locally, show "Could not save. Export your progress now." |
| `revoked`, `not_granted`, a null namespace or user id, or `can('data.write')` false | Switch to `IdbStore` with the browser-only banner |
| IndexedDB unavailable (some private windows) | `MemoryStore` with the banner "Nothing will be kept after this tab closes", and Export offered |
| An event fails its schema on load (corrupt, or from a newer app) | Skip it, keep it raw in a quarantine list, show "3 records could not be read. Update the app." |
| A snapshot in an older format | Ignore it and rebuild from events |
| An import file fails validation | Reject it with the first error; write nothing |

### 13.9 Content migrations and the log

Stored events are never rewritten. The fold applies `content/migrations.yaml` (`CONTENT-FORMAT.md` 4.5) as it reads:

- **rename:** events naming the old id are read with the new one;
- **merge:** the reviews of every merged skill replay into one card in time order, same-day duplicates collapsing to the first;
- **split:** each new skill's card replays the old skill's reviews;
- **retire:** Redo entries move to `replacedBy` or a generator instance on the same skill and level, as `CONTENT-FORMAT.md` 4.4 specifies.

Event format changes bump `v`; readers upgrade old events in memory.

---

## 14. Export, import and handoff

### 14.1 The export file

```ts
interface ExportFile {
  format: 'zq-progress'; v: 1;
  kind: 'full' | 'sync';                       // full backup, or only what the peer has not acknowledged
  exportedAt: number; app: string; contentRelease: string;
  source: 'artifact' | 'web';
  have: Record<string, number>;                // per device id: the largest n such that this side holds that device's events 1..n
  devices: { dev: string; maxSeq: number; first: number; last: number }[];
  packs: { dev: string; seqFrom: number; seqTo: number; enc: 'gzip-b64'; data: string }[];   // at most 1,500 events a pack
  drafts: { id: string; data: unknown }[];                                                       // open homework and long-form drafts
  sha256: string;                                                                                // over the canonical JSON of all fields above
}
```

- **Two kinds.** A **full** backup carries every event. A **sync** file carries, for each device, the events above what the peer target last said it holds: each side stores the `have` map from the last file it imported from the other side, and `exportSince(peer)` packs every event with `seq > peerHave[dev]` (all of them for a device the peer has never mentioned). A sync file therefore acknowledges as it travels. On import each side keeps, per device, the larger of its stored and the received `have` value, so a file sent twice, or an older file arriving after a newer one, only repeats events the union ignores and never moves an acknowledgement backwards. Before the first file from a peer arrives, a sync file equals a full backup.
- **Sizes**: a week of study is about 400 events, about 40 KB as a sync file, small enough to paste on a phone [inferred: section 13.6's volumes over about 220 weeks, at draft 1's measured 77 gzipped bytes an event, base64 included]. A full backup is about 5 MB after a year and about 20 MB after four [inferred, section 13.6].
- No viewer id, name or email: viewer ids are scoped to an organisation and mean nothing elsewhere [sourced: `user.d.ts`].
- File names `zero-to-quant-sync-YYYY-MM-DD.json` and `zero-to-quant-backup-YYYY-MM-DD.json`. The Artifact saves through `downloads.save` (`json` is on the allow-list's first group, and ordinary saves have no size limit short of 200 MiB in the Android app [sourced: `downloads.d.ts`]); the web app through a Blob link. Both also offer "Copy sync text" for the paste route.
- The weekly review reminds the learner to sync when this side holds events the other target has not acknowledged and the last sync is 14 or more days old, and to take a full backup every 4 weeks.

### 14.2 Import and merge

1. **Choose:** a file picker or drag and drop; or paste the file's text (sync files on phones) [unverified: whether the Artifact frame allows a file picker; the paste path works regardless for sync files, and a full backup restores on the web app first].
2. **Validate** in the data worker with the classic zod schemas (`ARCHITECTURE.md` decision 10), before anything is written: at most 64 MB; `format`, `v` and `kind` known; the hash matches; every pack decodes (gunzip through `fflate`, with an output cap of 256 MB); every event passes the event schema, including the string caps of section 11.2; at most 1,000,000 events.
3. **Report:** "Adds 1,204 events from 2 devices (web app), 28 September to 6 October. 0 conflicts." A conflict (same id, different content) should never happen; the existing event wins and the count is shown.
4. **Write:** the Artifact writes import packs `chunks/<dev>-i<hash>`, where the hash is of the pack's data, so importing the same file twice writes the same documents; the web app adds events to IndexedDB.
5. **Rebuild** derived state, save a snapshot, append an `import` event, and merge the file's `have` map into this side's knowledge of the peer (per device, the larger value).

Import never deletes. "Replace all progress with this file" is a separate action that first offers an export of the current data and then requires typing REPLACE. Drafts import only where no local draft with that id exists.

### 14.3 Result codes

A code item the Artifact cannot run (decision 30: a C++ drill, a package the Artifact does not ship, or Python that failed to load on this device) is done on the web app, and its result travels back as a short code rather than a sync file. The Artifact shows the web app's address with the drill id, homework instance, slot and seed in the URL fragment, as copyable text and as a link [unverified: whether a link to another host opens from the Artifact frame]:

- **Format:** `ZQR1.` + base64url(deflate(the attempt event with its `time` and `mark` events)) + `.` + CRC-32 in hexadecimal; typically 300 to 800 characters [inferred].
- **Where:** the web app's drill screen shows "Copy result code" after a submission that came from an Artifact handoff; the Artifact item shows "Paste result code".
- **Checks:** checksum; schema; the `ref` matches the handoff (drill id, homework instance, slot, seed); not already present.
- **Merge:** as an import (union by id); the item shows "Run on the web app".
- **Honest limit:** the checksum catches copying errors, not forgery. A browser holds no secret to sign with (engineering floor: client code holds no secrets), and the learner is the only one relying on the result.

### 14.4 The learning record

- **HTML:** one self-contained file, inline CSS and no scripts: the learner's name as they typed it; stages and topics completed with dates; every paper sat with score, pass mark, date, integrity summary and any "self-marked" flag; exit parts with their instruments and evidence links as text; verified drills; projects with repository links; earned, credited and spent hours with the self-reported share. It ends: "This record is produced by a personal learning app. It is not an accredited qualification. Self-reported items are marked as such." (design research 10).
- **CSV:** `papers.csv`, `outside-work.csv`, `redo.csv`, `weekly-hours.csv`, `exit-parts.csv`, packed into one `zero-to-quant-tables-YYYY-MM-DD.zip` with `fflate`, so the learner confirms one save, not five.
- **In the Artifact** both go through `downloads.save`. `html`, `csv` and `zip` are in the allow-list's second group, which a platform can switch off [sourced: `downloads.d.ts`]; on `extension_not_enabled` the app says that format is unavailable here and stops, as the contract asks, and the web app's record is the alternative. On `declined` nothing is retried.

---

## 15. Privacy

### 15.1 What is held

| Category | Examples | Where it rests | Who can read it | Kept |
|---|---|---|---|---|
| Learning record | attempts, answers, code, long-form text, timings, marks, cards | Both targets: IndexedDB on the device first. Artifact, unless device-only mode is on: also the viewer's private `db` subtree on claude.ai | the learner only; in the Artifact not even its owner [sourced: `db.d.ts`] | until the learner deletes it, or until the Artifact itself is deleted, which erases its store |
| Outside work | log entries, notes, evidence links, real-paper scores, projects | as above | the learner | until deleted |
| Mock interview transcripts | text only (`widgets-finance-games.md` 2.12, the `speech` service: the app keeps text, never audio) | as above | the learner | until deleted |
| Settings and device data | goals, pins, breaks, random device ids, timezone offsets | as above | the learner | until deleted |
| Tutor records | marking results, recaps, diagnosis ids, usage counts (`AI-TUTOR.md` decision 20) | as above | the learner | until deleted |
| Friends board entry | week, MP, hours, beat-usual tick, stage, viewer id | Artifact shared path `board/<uid>` | everyone on that Artifact at Contributor level or above | until opt-out or deletion |

Held nowhere: email addresses, names (resolved at render from `user.profiles()`), location, analytics, telemetry, third-party trackers.

### 15.2 What leaves the device

The brief's rule is "local-first, nothing leaves the device except to Claude when the tutor is used". The owner's own decision to sync Artifact progress through `db` is the one exception, and the app states it rather than hiding it:

1. **In the Artifact, unless device-only mode is on**, progress is copied to the Artifact's database on claude.ai, inside the learner's private subtree. It leaves the device for the platform that hosts the app and the tutor, under the learner's own account; that is the cost of syncing between devices without a server of our own. Settings, Data says so in one line: "Your progress is saved on this device and copied to this app's private storage on claude.ai so it follows you between devices. Turn this off to keep it on this device only." Device-only mode (decision 31) makes the brief's rule hold literally, at the price of no sync between devices except by sync file.
2. **Tutor calls**, when the learner uses Bertie: through `sample` on the viewer's own Claude account in the Artifact, or through the tutor proxy to the Claude API on the web app, carrying the context `AI-TUTOR.md` section 4 specifies (the screen, the learner's answer or working), never the progress log.
3. **The friends board entry**, when opted in.
4. **Sync files, backups and result codes**, when the learner saves or copies them.
5. **Withdrawn:** the web app's GitHub and Codeforces API lookups (`docs/PLAN.md` conflict 5). Repository URLs and handles are stored as text and never fetched.
6. **C++ drills send nothing.** `docs/PLAN.md` drops the Compiler Explorer route: C++ runs through in-browser Clang on the web app if the 1.9 spike passes, otherwise on the learner's machine with pasted output, so learner code never leaves the device.

Nothing else. Neither target sends telemetry (`ARCHITECTURE.md` decision 27); the tutor proxy logs no learner content (`AI-TUTOR.md` 6.3.9).

### 15.3 Untrusted text

Everything the learner types or imports (notes, links, problem references, imported events) and everything friends write (board entries) is rendered with `textContent`, or through the KaTeX renderer for maths, never `innerHTML` (the single-sink rule in `CONTENT-FORMAT.md` 12.2). Links show as text with their host. On the web app they open through an anchor with `rel="noopener noreferrer"`; the Artifact shows them as copyable text [unverified: whether a link to another host opens from the Artifact frame]. Imported files pass section 14.2's validation before any field is used. Board entries are validated (week format, numbers in range) before they render.

### 15.4 Deletion

"Delete my progress" (You, Settings, Data) offers a backup first, then asks the learner to type DELETE. The Artifact lists and deletes every document in the learner's subtree one by one (deleting a document does not delete documents below it [sourced: `db.d.ts`]) and the board entry, then clears its local mirror; the web app deletes its IndexedDB database. It cannot be undone, and the screen says so. Deleting the Artifact itself would erase every viewer's progress at once, which is why the release process never does (section 13.4).

### 15.5 Friends and access levels

- **Writing needs the right level.** A friend can save progress only at `interact` or above: a Contributor in the owner's organisation (Team or Enterprise), or an Editor invited by email from outside it while the Artifact is not shared by link [sourced: `db.d.ts`]. Outside viewers never write. Section 12.5 sets out what each case means and what the app tells the friend.
- **Deciding by trying.** `user.can('data.write')` speaks for shared documents and resolves `null` for viewers from outside the organisation [sourced: `user.d.ts`], so the app attempts its first private write and falls back to browser-only mode on `invalid_argument`, with the banner and the message of section 12.5.
- **What the owner sees.** Nothing of a friend's progress, answers or tutor records: only their opt-in board entries. The `{self}` rule keeps each subtree private from the owner too [sourced: `db.d.ts`].
- **What a friend can write.** Only their own subtree and their own board entry (decision 32). An Editor friend can, however, publish a new version of the app itself; that is a property of the Editor level, not of our rules, and the owner should invite as Editor only people trusted with the app.

---

## 16. Tests

Every component's definition of done in section 19 includes its tests from this list.

| Area | Tests |
|---|---|
| Fold and log | Property tests over random event streams (fast-check): determinism, order independence, idempotence under duplicates, incremental equals rebuild; a synthetic whole-path learner (about 106,000 events, section 13.6, and a 3,905-hour variant) for the rebuild time budget and the document count and size budget |
| Stores | `DbStore` against a fake `db` that enforces 256 KiB, path parity, last-writer-wins, the error codes and the rule set of section 12.5 (a second viewer's write outside its subtree and board entry rejects); outbox replay after each error code; pack compaction with a crash injected between pack write and chunk delete; two simulated devices appending concurrently lose nothing; two tabs on one device elect one writer, and "Use here" moves it without losing a queued event; device-only mode off, then on again, uploads the mirror without duplicates |
| Export and import | Round trip from each target to the other, full and sync; a sync file holds exactly the events above the peer's last `have`; sync files applied twice or out of order change nothing; re-import is idempotent; rejection cases (oversized, bad hash, unknown format or kind, schema failure, a gzip bomb past the output cap, a `javascript:` link, a 3 KB note); the REPLACE path |
| Result codes | Round trip; checksum failure; wrong drill or seed; duplicate |
| FSRS integration | `ts-fsrs` pinned at 5.4.2 and configured as section 5.2 says (a test fails if fuzz or short-term steps are on: a first Good must give stability 2.31 days); golden card states for fixed review sequences; band routing; the grade table of section 5.3 case by case; one review per card per study day; retention tiers move due dates at once; the load balancer reaches its bounds |
| Implicit repetition | Accumulator arithmetic; due-within-7-days rule; no propagation beyond one edge; failures do not propagate |
| Readiness | Hand-computed $\mu$, $\sigma$ and $P(\text{pass})$ on small papers; prior rules 1 to 5 of section 5.7 |
| Redo | The date table of section 6.2 with late first redos, misses at each step, the 14-day floor, duplicate misses merging; variant selection never repeats a seen point or touches the reserve |
| Exam engine | Fake clock: time-up auto-submit, resume after reload, pause budget exhaustion, a backwards clock jump; timed sections closing on time and on "Finish section", with the calculator present only where allowed; form choice by freshness; the seen-items warning; exact-fraction pass at the boundary (69.99% fails, 70% passes); a 1.3 paper at 72 overall and 48 of 70 in Section A fails; follow-through marking; code partial marks; the self-marked-pass label; a missed `slotMin` bar offered as an exit-item sitting after 3 days; cool-down and remediation unlock; abandon rules; lease takeover; "Sit this paper in the web app" exactly when the runtime check fails |
| Homework | Issue seeding without repeated points; submission marking; late and overdue states; pending web-app items resolved by result code |
| Lesson quiz | Passed at 3 of 4, 4 of 5 and 3 of 3; not at 2 of 3 or 3 of 5; a Prove, Derive or Show lesson's production item counts |
| Gate marking | The lower mark per point counts; Bertie's marks hidden until every point is self-marked; a disputed point resolved by an exit-item sitting; provisional state with the tutor off |
| Soft gate and interleaving | The next level enters Main only after its condition or a remediation set, with an override recorded; a homework instance's earlier-level share and "which tool?" items |
| Retention sittings | Scheduled at 3 and 12 months; below 60% reopens the topic; one diagnostic sitting per paper |
| Streaks and XP | Study day at 04:00 across timezone changes; each qualifying route; rest-day earning and auto-use; weekly mode; planned breaks; every XP and MP table row |
| Planner | The block table of section 8.1 for 5, 10, 15 and 25 hours, and blocks summing to the goal for every quarter hour from 3 to 40; alongside shares; the stage rule and the 1.9 deferral; the 60% swap; habit time excluded from the pace factor; path length read from a track (3,100 and a 3,655-hour fixture); the forecast on synthetic histories |
| Mental arithmetic | 7-day median rule with touch runs excluded; voided runs; 80-in-8 scoring; weakest-fact selection |
| Weekly problems | Eligibility; the three-slot rule; carry-over cap; same assignment on two devices from the same week seed |
| Exit parts | Each instrument kind satisfied and not satisfied, including `sets` (an item below full marks without a correct redo blocks it), `slotMin` met in a later sitting, `rubric` with `count`, and `project` with `notePredicates`; real-paper series uniqueness; the counter's verified and self-reported split; every exit row of section 2.9 parses as data |
| Privacy | The board document holds only its allowed fields; no name or email in any stored document; device-only mode makes no `db` call (a spy on the fake); untrusted text never reaches `innerHTML` (lint plus a DOM test) |

---

## 17. What this file needs from the other papers

**From the content format (`CONTENT-FORMAT.md`):**

Done in revision 2: `Skill` fields and CI rules (sections 4.2, 4.3); the instrument union with the id and track-name fixes; `Level.companion`; the hours and exam CI rules; `content/plan.yaml`; the snapshot rule. Still needed, from draft 2:

- **Instrument union** (section 2.10): `slotMin` on `exam`, `count` on `rubric`, `notePredicates` on `project`, and the `sets` kind.
- **Exams** (section 3.1): `ExamForm.sections[].id` (a `LocalId`) and an optional per-section `calculator`; `Exam.sectionPass` (section id to fraction) and `Exam.aids` (formula card ids); `kind` gains `exit-item`; item parts may declare `followThrough: <part id>`, and the grader marks such a part against the learner's own earlier answer.
- **Runtime tags**: the engine's runtime check against `needs` decides where a drill runs (decision 30); `micropython-ok` and `ulab-ok` have no remaining use once `ARCHITECTURE.md` drops MicroPython.
- CI: every `slotMin` key names a slot that exists on every form of the paper; every `sets` instrument names sets of the same topic.

**From the engine paper (`ARCHITECTURE.md`):**

- The `ProgressStore` interface and the event envelope (sections 13.2 and 13.5), including `exportSince`; the outbox, device ids, lease helpers and the Web Locks writer election (decision 26, adopted in section 13.7).
- An active-time tracker (section 8.6) and a clock service that computes study days from `t` and `tz`.
- The fold running in the data worker, with snapshots (decision 11, adopted).
- A runtime availability query, `canRun(needs, target)`, answering from `engine/python/budget.ts` and whether Python loaded on this device; the exam rules screen, homework items and the handoff read it.
- The per-course Artifact package budget (SciPy, statsmodels, scikit-learn), which decides the "Runs on" column of section 2.9 for 1.6, 2.1 and 2.2.
- A release process that only ever republishes the Artifact to its URL and never deletes it (section 13.4).

**From the curriculum files:**

- `stage1-linear-algebra.md` 4.1: resit after 7 days, not 3, as every finals-style paper (section 0.3).
- `stage1-statistics-ts.md`, `stage1-calculus.md`, `stage1-probability.md`: their exit data already matches section 2.9; the slot ids `Q19` and `Q15` become `slotMin` keys.

**From the tutor paper (`AI-TUTOR.md`):**

- Gate rows for weekly problems (as a lesson screen), level checks and placement (off).
- Long-form marking after paper submission at the `complex` tier; the recap after papers; the P1 weekly recap.
- Content-gap report entries for real-paper calibration gaps (section 11.8).
- The `tutorCalls` counter on every paper attempt.

**From the widget catalogues:**

- `speed-drill`: the 80-in-8 configuration of section 9.2 and per-item records in its result.
- `puzzle-workbench`: the selection hook of section 10.3 and the easy, hard or failed rating.
- `problem-workbench`: timed results with the held-out flag.
- `setup-checklist`, `results-note`, `mock-interview`, `contest-arena`: results emitted as the events of section 13.2.

---

## 18. Open questions and unverified items

| # | Item | Status and effect |
|---|---|---|
| 1 | The total size cap of one artifact's database | [unverified]. The bounded probe of `docs/PLAN.md` stage 2 writes paced 192 KiB documents up to a 60 MB ceiling, records success or the cap, and deletes its data. A cap at or above 30 MB times the expected participants means the checkpoint of section 13.6 is not built |
| 2 | Whether the Artifact frame allows a file picker, and whether links to other hosts open | [unverified]. The paste path (sync files of about 40 KB a week) and copyable links work either way; a full backup restores on the web app if the picker is blocked |
| 3 | Zetamac's default ranges | [recalled, unverified]; configuration, so a correction costs no code |
| 4 | 80-in-8 details (option count, penalty, skipping, pass lines) | From secondary sources via search summaries [unverified with the firm]; configuration |
| 5 | Khan Academy's precalculus units and course challenge format | Search summary only [unverified]; shapes `s0.precalc` (`stage0-precalc-computing.md` open item 3) |
| 6 | Durations of MIT 18.01, MIT 18.06 and Stat 110 finals, and how many past finals with solutions are public | [recalled, unverified]. `1.5.exit` needs two Stat 110 finals; if fewer than three are public, resits of the confirm step run out |
| 7 | FSRS on problem-solving skills | [inferred]. Contained by the optimiser, the calibration report and the fallback (section 5.9) |
| 8 | `fsrs-browser` or the WebAssembly binding: size and speed | [unverified]; the optimiser is P1 and runs only on the web app |
| 9 | Codeforces API cross-origin access | **Closed**: the lookup is withdrawn (`docs/PLAN.md` conflict 5); manual entry |
| 10 | The effect of implicit repetition on review load | Not simulated; depends on how many `encompasses` edges authors write |
| 11 | Redo volume | [inferred] from assumed error rates (section 6.5); the weekly review shows the real figure from week one |
| 12 | Which of SciPy, statsmodels and scikit-learn ship in the Artifact | [unverified]; `ARCHITECTURE.md` sets the per-course budget. Decides "Runs on" for 1.6, 2.1 and 2.2; the handoff covers either answer |
| 13 | Whether the owner's plan offers email invitations at Editor level, and whether an outside Editor gets a viewer id | [unverified; `db.d.ts` says "where the share menu offers that level" and that such an Editor "may have" no id]. Decides whether the P2 friends board can exist on a personal plan; a probe with one invited friend settles it |
| 14 | Pyodide on a phone for the 1.4 capstone's 2-second test ($m = 10{,}000$, $n = 50$) | [unverified]; `stage1-linear-algebra.md` open item 9 raises the limit if needed |
| 15 | Owner decisions | (a) confirm GCSE geometry and statistics inside 0.3 (`stage0-precalc-computing.md` decision 2); (b) confirm the Khan units taught in 0.3 (its decision 3); (c) one project or three on the Trader track; (d) 9/3/2/1 with borrowing (recommended), or 8/3/3/1 from Stage 1; (e) whether mocks with Bertie count towards the ten; (f) the `canon-gap.md` exit changes, which section 2.9 shows fit without new machinery |

---

## 19. Build stages

For `docs/PLAN.md` section 11. Each stage is one review gate and testable alone. Engine, widget, content and tutor stages interleave; dependencies are named.

| Stage | Deliverable | Depends on | Done when |
|---|---|---|---|
| A1 | Event envelope and schemas; the `AppendQueue`; the fold framework with snapshots; `MemoryStore`; the synthetic whole-path learner generator (`docs/PLAN.md` stage 9a, before the player) | engine core | The property tests of section 16 pass; the `AppendQueue` contract suite passes; a full rebuild of the synthetic learner meets the time budget on the reference phone |
| A2 | `IdbStore`, `DbStore` with chunks, packs, snapshots, outbox, leases and failure behaviour; the Web Locks writer election; device-only mode; the Artifact's `db` rule set (section 12.5) | A1; the `db` and `user` capabilities; the size probe's result (`docs/PLAN.md` stage 2) | The fake-`db` test suite and A1's `AppendQueue` contract suite pass; two-device and two-tab concurrency lose nothing |
| A3 | Full backups and sync files with `have` acknowledgement, import, REPLACE, result codes, the handoff link | A2 | Round trips between targets, full and sync; every rejection case; idempotent and order-free re-import |
| A4 | Time tracking, streaks, rest days, breaks, XP and MP ledgers, achievements | A1 | Section 16's streak and points tests; Today and You read only derived state |
| A5 | Skill graph loading; FSRS cards by band; grade mapping; retention tiers; implicit repetition; mastery numbers and map states; readiness | A1; content C8 (skills compiled) | Golden card states; readiness hand checks; the mastery map renders from the synthetic learner |
| A6 | Redo queue, review composer, load balancer, lesson-start warm-up | A5 | The date table; variant rules; the composer's budget and interleaving on synthetic queues |
| A7 | Quiz, level review, practice and homework flows (drafts, submission, marking, long-form hook, pending web-app items) | A5, A6; lesson player; content C3 and C10 | A level's quiz, review and homework run end to end on both targets with recorded tutor replies |
| A8 | Exam engine: kinds (with `exit-item`), forms and freshness, sections with their own clocks, calculators and bars, aids, follow-through marking, rules screen, clock and pause, navigator, marking, results, cool-downs, remediation, integrity, the runtime check | A7; the content-format exam fields of section 17 | The exam tests of section 16 with a fake clock; the 0.3 topic exam (two timed sections), the 1.3 finals-style paper (a section bar) and the GCSE-style paper sat end to end |
| A9 | Placement, stage-entry diagnostics, test-out, level checks, credited hours | A8 | The ladder algorithm on scripted answer sequences; priors written as specified |
| A10 | Exit parts and the outside-work log: every instrument kind (with `sets`, `slotMin`, `rubric` counts and note predicates), real papers, problem sets, projects, ledgers, book-log, mock log | A3, A8 | Every instrument kind satisfied and not satisfied in tests; Stage 0's checklist and the 1.3 exit complete on scripted learners |
| A11 | Planner: blocks, alongside shares, sessions, the 60% rule, the stage rule, earned, credited and mapped hours, track path length and forecast, the weekly review | A4, A6, A10; content `plan.yaml` and `Track` data | The planner tests; a 15-hour week for a Stage 1 learner matches the curriculum's 9/3/2/1 |
| A12 | Daily 10 and Daily 5 orchestration, fact model, Zetamac and 80-in-8 rules, mental charts | A4; `speed-drill`, `strategy-trainer` | The median exit rule; voiding; weakest-fact selection |
| A13 | Weekly probability problems scheduler | A5, A6; `puzzle-workbench`, `problem-bank` | Selection and carry-over tests; three weeks of assignments for a scripted 1.5 learner |
| A14 | Ghost race (P0); friends board (P2: opt-in, rendering, the access probe of section 18 item 13) | A4, A2 | Ghost curves on synthetic histories; board document field allow-list; two simulated viewers see each other's entries and not each other's subtrees; a viewer without write access gets the browser-only path and the message of section 15.5 |
| A15 | Learning record (HTML, CSV zip), calibration report, and the FSRS optimiser on the web app (P1) | A5, A8, A10 | The record renders every section from the synthetic learner; the zip opens with five valid CSV files; the optimiser adopts parameters only under the 2% rule |

Security work sits in the stage that creates the exposure: input validation of outside entries in A10, import validation in A3, board rules and rendering in A14, untrusted-text rendering in every stage that shows learner text.
