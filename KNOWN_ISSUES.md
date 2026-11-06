# KNOWN ISSUES

Open at migration (27 Oct 2026)
- A single `--all` run is too long for one browser and the 2-hour background limit (the browser closed after about 1,100 items); always split it into lessons, `--sets`, and `--exams` plus `--routes-only`.
- `docs/BACKLOG-INBOX.md` holds about 136 unnumbered engine bullets awaiting pass 7, plus about 42 from the seven gap levels (27 Oct).
- Gap briefs and Stage 3 briefs (`docs/briefs/gap-*.md`, `momentum-rep.md` and others) name scratchpad and pkgs paths from an older session; give agents the current paths.
- Topic exams 1.3, 1.4, 1.5 sit at the validator's 30-item cap (markov L5, 28 Oct, has no exam items; `docs/reports/markov-5.md` names candidates); gap items are packed into multi-part tables marked all or nothing, and the 1.3 curve sketch is typed, not tapped (inbox bullets ask for partial credit and compound items).
- Seven homework items have both prose and a hidden longform prompt (list in ENGINE-BACKLOG.md pass 6 note).
- [Superseded 5 Nov, census] Stage 1, 2 and 3 have no stage exams; topics 3.x have no topic exams. Now: stage-0 is the only stage exam; topic exams 3.2, 3.3 and 3.5 exist; topics 0.6, 1.10, 1.11, 2.5, 2.6, 3.1 and 3.4 have none.
- [Corrected 5 Nov, census: the 3,100 and 3,530 figures are superseded] The Learn header sums stored stage hours, 3,265 (515, 1,400, 800, 550); topic hours sum to 3,695 (555, 1,650, 940, 550), the figure `docs/curriculum.md` quotes (review F09, 2c item 11). Stage hours ignore "Quant path only", and the Paths view is unfiltered (ENGINE-BACKLOG item 428). Direct links to hidden pure courses still open.
- A bare `i` in an `expression` answer is now the imaginary unit (item 446); only `markov/homework-3` used it as an index and it still passes. `drill.js` keeps a float-only `isclose` (item 447).
- `space` canvas: no 3D dragging of points or vectors yet, flat arrowheads, per-piece painter's order (large interpenetrating surfaces can sort wrongly); items 438 to 444.
- Sandbox CPython lacks SciPy and SymPy; brief-writers installed them (SymPy system-wide, SciPy by `pip --target` in the scratchpad). The `pkgs` local CDN is rebuilt per session (a container restart keeps the scratchpad).

- Item 449: a topic exam passed before new levels joined that topic (markov L5 in 1.5) hides those levels from Today; they stay on Learn. No full `--all` playthrough has run since item 449 (validator 0 errors, `--routes-only`, exam topic-0.1 and number-sense l1 green).
- The 28 Oct breadth briefs name that session's scratchpad (`.../a8ff8d32-.../scratchpad/pkgs`, `pylib`); give agents the current session's paths. Brief numbers were checked with SciPy 1.18.1, but Pyodide ships SciPy 1.14.1: agents confirm `linprog` (HiGHS) and avoid `res.multipliers` and solver message text.

Engine gotchas
- `unit: "%"` on a numeric widget divides the typed value by 100: store the fraction.
- `fmtNum` rounds numeric answers to 6 decimal places, so answers below 1e-6 must be rescaled in the prose.
- `__learner_source__` is visible to tests only when a prelude or postlude exists.
- `expression` tests free symbols only from 0.3 to 3, so `\min(1, \varepsilon/5)` grades the same as `\varepsilon/5`; a cap whose switch lies outside that range needs `choice`. (Capital `N` is now an ordinary symbol, item 437.)
- Code cases: a 5 s limit per case (plus `budget` or 30 s for heavy imports), reported against the case that hit it; `isclose` has a fixed 1e-12 tolerance (C++) or rel 1e-9 (Python); no per-test `tol` yet.
- A shared generator line `import numpy as np, pandas as pd` loads numpy only in the worker; write separate import lines.
- `graph` edges draw undirected unless `directed` is set, against README-B.
- `tree` canvas: the limits listed here before pass 7 are fixed (binary mode and the rest; see `README.md`); recombining lattices are still drawn with `graph` rectangles.
- `grid`: a `null` in a `mark` patch prints "null".
- `plane`: `derive` cannot target an `area` by id (use `area.to`); no `erf`/Phi in curve formulas before pass 7.
- Set-mode playthrough is flaky while other agents write files in the same folder; re-run alone before treating a failure as real.
- Pyodide first loads: scikit-learn 20 to 40 s, statsmodels 20 to 40 s; every `how` on such screens says so.

C++ runtime
- Compiles at `-O1`, asserts on, no `-Wall`, one file only, no `try`/`catch` (no unwinder; a `throw` ends the program).
- Precompiled-header bug: a later `#include` of a new header can fail depending on timing; put headers in the hidden setup code.
- Undefined behaviour never traps in WebAssembly (null reads, use after free, double delete run silently); lessons show native sanitiser output instead.
- libc++ `std::normal_distribution` draws differ from libstdc++ and NumPy; expected values come from the app runtime.
- `std::chrono::steady_clock` ticks every 100 µs in Chromium; timings are illustrative, never graded.
- A range-for over a braced list needs `<initializer_list>` included.
- Vector growth with a move that is not `noexcept`: the app (no `-fno-exceptions` flag) copies on growth as the standard says (four pushes: 3 copies and 4 moves). A desktop build with libc++ and an explicit `-fno-exceptions` moves anyway (0 copies, 7 moves), so a learner who pastes l19 or exam `e-vector-growth` code there sees 0. The explains no longer mention that build, since the app cannot show it.

Process
- Claude Code's Write tool refuses a subagent write to any `.md` file whose name starts with `report`, `summary`, `findings` or `analysis` (a built-in filename rule with no setting). Only the `analysis` course's reports are hit. User decision (29 Oct): the agent returns the report as text and the main session saves `docs/reports/analysis-<n>.md`; no workaround. analysis-1.md to analysis-3.md were saved this way.
- Session and weekly usage caps stop every agent mid-task; work is saved on disk, so checkpoint-commit, then resume or triage.
- Validator warnings are mostly "ladder changes canvas kind" and "not yet written"; only errors block.
- jsDelivr is blocked in cloud sandboxes; build the local CDN with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` (40 s, 870 MB) and pass `--local-cdn`.
- Script-mode `sys.stdin` has no `.buffer`; contests lessons use `sys.stdin.read()`.

Interview pass (2 Nov 2026)
- Engine item 454 (`timed` with `lockAtZero` on reviews and practice) is not exercised by any content file, so playthrough does not cover it until a review carries `timed`; it passed only on a scratch copy.
- Recruiting firm facts (deadlines, formats, pay) are dated October and November 2026, some from third-party guides; they go stale every cycle (engine item E19 proposes `asOf` and a staleness warning). JP Morgan's reported 1 November 2026 close has passed.
- The validator refuses `longform` in reviews, contrary to AUTHORING section 5; spoken-answer practice sits in homework only (inbox bullet).
- Level 1 sections of the puzzles, mm-games, mental-pressure and ito briefs still name an old scratchpad; give agents current paths.
- A weekly usage limit stopped eight agents at once on 29 Oct; all resumed from disk on 2 Nov with no loss. Checkpoint-commit before long parallel runs.
- The mental-pressure L3 brief (l12) says net scoring (E1) is not built; engine pass A built it for mock exams (`exams/mock-*.json`, AUTHORING sections 5 and 7). Lessons still cannot net-score a learner's own answers, so l12's sample-candidate review stands; follow AUTHORING where the brief is out of date.
- Topic 0.7 (2 Nov): the exam's `--why` results screenshot goes blank after item 21, so the two longform model answers were never seen rendered; the l11 coverage table still scrolls about 20 px sideways at 390 px; the rail handle covering a question line is deferred to the inbox.
- Session branches: this session worked on `claude/recruiting-l3-game-theory-nvxp1s`, rebased on `claude/amazing-wright-d4mx7i` before each push; it is a fast-forward of that branch until the prep-tags session pushes more.

Second-read pass (3 Nov 2026)
- Raw-source checks that ban a name (for example a sort or a library call) also trip on that name inside a comment or string. Fixed for the sort bans in ds and algo-think; still present in ds l17, eigen l17 and homework-4, contests l5, l6 and l11, and exams topic-1.4 and topic-2.4. Fix in those topics' second reads.
- Exam items were replaced in topic-0.5 (four items) and topic-1.8 (two items); attempts sat before 3 Nov no longer line up item by item with the new papers. Lesson ids and progress are unaffected.
- Topics not yet second-read probably carry the same voice debt as 2.1; run `docs/reviews/voice-scan.py` on each before closing it.

Session B (3 Nov 2026, label 4 Nov)
- mock-oa-arith's 16 decimal, fraction and percentage items are fixed, so resits repeat them (inbox bullet asks E4 for those operations). Its start card's parts list squeezes at 390 px (engine, inbox).
- mock-oa-sig and mock-oa-trader ship three fixed versions each (3 Nov); resits repeat items until E3 (fresh draws); E15 (calculator) is not built. `prep.json` names version 1 only, so versions 2 and 3 are reachable from the exams list, not from prep. [5 Nov: versions grouped in Prepare via `versionOf`, ENGINE-BACKLOG 547.]
- The 12-screen lesson cap pushed several brief drills into quizzes in brainteasers L2 and L3 (listed in their reports).
- Raw `git stash -u` while agents write untracked files hides their files for a moment; use `git pull --rebase --autostash` and stage the manifest entry by entry.

Session A (3 Nov 2026)
- `voice-scan.py` with a relative `VOICE_BASE` scanned 0 files and reported a pass until 3 Nov (fixed: it resolves the path and exits on an empty folder). The topic 3.3 voice debt (mental-pressure, puzzles, mm-games) was cleared on 3 Nov: all five courses scan 0 and 0.
- Second read pending for limits L5, multivar L5 and eigen L4 (written after their topics' reads); markov L5 has no topic-1.5 exam items; 25 levels are covered by the exam only through skills shared with earlier levels (list in `docs/reports/stage-status-2026-11-03.md`).
- `carry` values are lost if a lesson is reopened part-way; the `trade` widget cannot quote one side at a limit, run limit 0, hedge or take liquidity, or open with a carried position (engine pass D follow-ups 2 to 5).
- The `file-finder` agent may not write `.md` reports; the main session saved the stage status report from its scratchpad output.

Session C (3 Nov 2026, label 5 Nov)
- Multi-paper mock results show "Pass mark NaN%" on every mock-oa-trader paper under +1, 0, 0 scoring with `passNet` (engine, inbox bullet). Scores and pass verdicts are correct; only the line is wrong.
- Voice debt outside this session's files: exams topic-1.2 and mock-trade-sample still flag long sentences (mm-games l4-fermi cleared 3 Nov).
- The validator does not flag overlapping numeric `wrong` ranges (inbox bullet from mock-oa-sig).

Session D (3 Nov 2026, label 6 Nov)
- Bank: the validator does not catch a misspelt family tag, and every bank `pace` stays at 180 s or less because `--routes-only` expects exactly one item over pace after a 200 s answer. `--bank` (462) answers right only and ignores `--mobile` (inbox).
- `content/prep.json` lists no topic exams, so topic-3.3 is reachable from Exams only (`docs/reports/exam-3.3.md` says where it would go). Puzzles L5, mental-pressure L3 and L4 and mm-games L3 and L4 are covered in topic-3.3 only through skills shared with earlier levels.
- game-theory poker cards draw their labels at about 8.6 px at 390 px because `.cv-svg text { font-size: 13px }` overrides the size `boxes.js` sets (engine, inbox); captions list the cards on six screens in l11 and l12.
- mental-pressure l12's paper is seed 80 plus 31 hand-swapped distractors (fix pass, 3 Nov); re-running the L3 generator script would undo them.
- Table cells' own `wrong[]` ids still cannot be `byKey` keys; mm-games l8 and mental-pressure l2 to l4 key on `r{i}c{j}` (inbox, several votes).
- [Resolved 5 Nov] Dates: the container clock read 3 Nov while the state files run 3, 4, 5 and 6 Nov as session labels. State-file dates are now restamped from `git log`. File names keep the old labels: `docs/reviews/answers-2026-11-04.md` (session B), `answers-2026-11-05.md` (session C) and `answers-2026-11-06.md` (session D) were all committed on 3 Nov.

Session E (3 to 4 Nov 2026)
- Five bank ids describe older numbers after the answer-check fix pass and stay unchanged (progress keys on them): `semicircle-seven-points` (nine points), `cycle-following-two-hundred-boxes` (100 prisoners), `waiting-for-hh-three-losing-days` (four days), `fair-from-biased-quarter-coin` (coin 1/5), `hats-mod-k-six-prisoners` (family `hats-simultaneous`).
- The interview results list shows one identical question line for all 30 behavioural items (engine, inbox "Bank second read (4 Nov)").
- Behavioural rubric lines that judge delivery (pace, tone) stay compound until spoken mode (E10).

Topic 3.5 briefs (4 Nov)
- Brief code was checked natively (g++ 13.3, clang++ 18.1, CPython), not in YoWASP clang 21 or Pyodide. Level agents must run every starter and solution in the app once. coding-int's slow-but-correct starters fail by time only natively (about 6.5 s and 10.7 s at the brief's n); confirm in the browser.
- `docs/briefs/systems-scripts/cpp/problems_l4*.py` and `appendix_cpp.md` predate `allocCheck`; the brief is the source for P-pool, P-format-price, P-latency-hist and P-handler (`systems-scripts/alloc/README.md`).
- The clone is shallow, so git ahead and behind counts against other branches are unreliable; compare trees instead.


Engine pass C and first topic 3.5 levels (4 Nov)
- `interleave` (471): a `wait` does not re-take its lock on waking, `notify` wakes every sleeper, and there is no store buffer. systems l9 and l10 word their claims to match ("if steps run one at a time"; the real `wait` re-takes the lock); the (0, 0) store-buffering result is taught from a listing.
- `allocCheck` (470) compiles with `-fno-builtin` because clang 21 at `-O1` deleted a visible `new`/`delete` pair, and skips the precompiled header, so a Check on such an item is a few seconds slower.
- `isclose` and `equal` in Python `code` still do not compare a pandas DataFrame or treat NaN as equal to NaN; the research-int brief works round it (`tolist()`, `np.isnan`). Levels 3 and 4 should confirm they need nothing more.
- The homework `parts` item sits first in systems homework-1 and homework-2, research-int homework-1 and homework-2, because the old playthrough check needed it there (fixed in 479); the order is harmless and was left.
- 537 validator warnings (4 Nov, after topic 3.5): mostly "a point hint usually highlights the canvas" and ladder canvas-kind warnings in research-int, plus 30 "reference to a level with no written lesson" from the `requires` mapping (23 at 1e67d6f, census 5 Nov; 610 warnings in all). None is an error; the topic 3.5 second reads did not clear the style warnings.
- Drill pattern vocabulary has 21 slugs (472 added nine for packs 2 to 8 beyond the 12 the briefs named); drill packs are id prefixes (`ci-`, `rq-`, `sy-`) or an optional `pack` field (473).
- `stale-local-backup` is a local-only branch holding the container's out-of-date copy of amazing-wright from session start; it has nothing unique and is not pushed.
- Gating (4 Nov, engine pass E): mock-oa-code draws from the eight `oa` drills, which the drill library also lists, so a learner can practise the mock's problems first; the description asks them not to open the pack. Fix needs an engine `language` filter on `draw` and unseen-first draws by solved state (inbox). Interview closures are large under Strict mode (DECISIONS "Interview closures under Strict mode").
- Playthrough limits seen in topic 3.5: it never runs code starters (authors confirm starters fail by script), it does not run the code tests inside some homework `parts` items (systems homework-4 histogram, checked with g++). The intermittent `rq-clean-frame-py` and `rq-group-slopes-py` failures were an engine bug, fixed in ENGINE-BACKLOG 500: the drill runner counted pandas loading against the 5 s limit, so a slow load timed the model solution out.
- coding-int (fix pass): no per-screen language skip in the engine (a C++ screen cannot be skipped by a Python learner), and the `orderbook` canvas labels are small at 390 px; both in the inbox.
- ito L2 (topic 3.2) was not started in session H: the 5-hour usage limit was hit once mid-session.

Session I (4 Nov 2026, topic 3.2)
- measure-prob L1 leans on countability (analysis l5, a Pure course), but AUTHORING 11 forbids a Pure course gating a Quant one, so L1 has no such `requires` and no recap screen. Decide: a recap screen in l1, or relax the rule.
- 606 validator warnings: item 515 added 66 (per cent values above 1, mostly `wrong` values whose accept text does not show the matching number); not triaged.
- `expression` with a declared function: `f(x)+1` graded against itself is false (no numeric value); predates session I.
- `table` returns a matched cell `wrong[]` id before the cell id, so `r{i}c{j}` feedback never shows while a `wrong[]` entry matches; ito L3, L4 and measure-prob L4 moved slips into cell-id lines. The validator still rejects cell `wrong[]` ids as `byKey` keys.
- pdes l12 s7: the "slope -2" label still sits on its line (judged acceptable). Canvas screens can run under the bottom bar at 1376 until scrolled (inbox).
- Playthrough runs in Chromium at the device sizes, not WebKit; touch, Safari and the C++ compiler's memory on an iPhone are untested on real devices.
- Reviews are capped at 10 items by the validator, while test-out of a required level wants 12 or more (inbox [Should]).
- The whole-app `--tablet` pass was not run at close (several hours at three extra widths); topic 3.2 files and the exam were run with `--mobile --tablet` during the session.
- (closed S, ENGINE-BACKLOG 570: the check missed a drawn first item with parts) `--exams` under four parallel shards: the `mock-sample-draw` timed check failed once ("timed out with one answer per paper but scored 0") and passed when re-run alone; treat as load flakiness unless it repeats.
- Five more per cent keys at or below 1 (garch l4, numpy-pandas l12, py-found l16, random-vars l19, random-vars review-5) were stored as per cents; fixed, and item 516 now errors on them.

Session J (5 Nov 2026, PLAN 2a item 7)
- CLAUDE.md says C++ runs with "no exceptions", but `app/js/screens/cpp-worker.js` passes no `-fno-exceptions` (flags `-std=c++17 -O1`, libc++ hardening debug); a throw still cannot be caught in the wasm build. Left for the user to correct.
- Another session (session_01E26gTN3...) pushed to this branch during session J (desktop split record, per cent batch); both rebased cleanly. Two sessions on one branch risk state-file conflicts.
- Deferred from the trees L4 and cpp L5 fix passes: l14 s4 "0.000" tick label; array canvases in a tall band at 440 px ([Should]); fenced prose code blocks have no wrap switch ([Could]); topic-1.9 thin on cpp level 1, and l20 and l23 untested directly.
- The 606 to 610 validator warnings were not triaged (4 added this session are deliberate ladder canvas-kind changes in trees l16 and l18).

Course correction review (5 Nov 2026; `docs/reviews/review-course-correction.md`, verified at 1e67d6f; PLAN 2c)
Open review ids (none is fixed at HEAD; closure only on the review's acceptance evidence):
- F01 (2c item 2): Today ignores role; `profile.track` is stored but unread; no strats or derivatives track exists.
- F02 (item 7): cross-course `requires` edges carry no reason; trader superday closure 107 levels, 35 courses, 470 lessons.
- F03 (item 7): pdes/L1 and pdes/L3 depend on unwritten odes/L4 and numerics/L4; unreachable under Strict.
- F04, N07 (item 5): no lesson quiz holds code or longform; AUTHORING 489 and 529 produce the defect.
- F05, N02, N03 (item 4): met is a 70% review share with no skill floor; a review can be sat cold; a 21 of 30 topic pass meets up to 22 levels.
- F05.6, F05.7 (item 6): closed 5 Nov (ENGINE-BACKLOG 546, 547). Left open: the `oa` pool is 8, so a fifth sitting repeats, and a learner who verified all 8 gets only labelled repeats; no hidden holdout pack exists. The mock draws difficulty 3 and 4, while the curriculum exit says "two medium".
- F05.8: only stage-0 has a stage exam (PLAN 4, stage exams line).
- F06, N08 (item 8): no out-of-app capstone record; verified drills feed no met rule.
- F07 (item 10): `minutes` 11 to 15 everywhere; interview lessons state 25 to 60 minutes in prose.
- F08, N05 (item 9): closed S. 78 candidates (69 with the five-word set), user ruled as maths reader; 3 False, 14 Loose and the five known lines fixed (`docs/reviews/review-precision-3.2.md`). Residue: the trigger words miss bare universals ("Zero drift means a martingale"), and only seven courses were read; 636 candidate lines exist across 70 courses.
- F09 (item 11): hours 3,265 stored against 3,695 summed.
- N01: closed by 2c item 3 (5 Nov). Residue: Elo and MP in saves from before provenance still include earlier self ticks (cannot be split). Old attempts on the 25 `selfExams` meet nothing unless already in `prereq.met`.
- `--exam mock-superday-research` times out in `waitForFunction`, identically on HEAD before item 3; not investigated. Full `--all` (about 3 hours) not run for item 3; `--routes-only`, 15 longform topic exams, three homework sets and `mock-superday-trader` passed.
- N04 (item 2): prep.json names five mocks with no file (15 references); no developer or strats final-round mock.
- N06: closed by 2c item 1 (5 Nov).
- Pilot (item 12) and the precision reader (item 9) need humans; capstone reviewer (item 8) and the odes and numerics decision (item 7) need the user.
Process found this session:
- The review's line references to KNOWN_ISSUES are one line early at HEAD (`:86` dates, `:53` weekly cap, `:110` session H).
- CLAUDE.md "Models" still says implementation subagents run on Sonnet, while `content-author` and second readers run on Opus (operating model 2.5 keeps them there).
- `app/tools/merge-wave.sh` is named in SESSION PROTOCOL 3 but not written yet (2c O1); merge by DECISIONS "Parallel worktree merges" until it exists.

- Readiness contract (2c item 2): edges from required trader courses into optional `graphs-dp` and `contests` (brainteasers L2, L3; game-theory L2), and strats `coding-int` into `contests`, `numerics` into `opt-dash`, are advisory by role, not cut. Item 7 still owes a `why` per edge; under Undecided they still block.
- Readiness contract (signed off 5 Nov): trader required set is 442 lessons, 1,214 h; Learn shows 630 lessons, 1,804 h. The old superday closure was 470 lessons, so the required route is only 6% shorter; most of it is Stage 0 (193 lessons). Accepted by the user as drafted.
- Readiness contract: topics 3.2 and 3.4 store 0 hours, so derivatives sub-route hours are understated (item 11).
- `playthrough --routes-only` without `--local-cdn` fails `#drill (filters)` on HTTP 404 `/vendor/yowasp-clang/bundle.js` in cloud sandboxes, before and after 2c item 2 (checked at e210324). With `--local-cdn` it is green.

- (5 Nov) `playthrough.mjs --all --routes-only` fails one check, "samples: #you shows the sample ..." (sample exam names in You exam history after sample mocks are played); reproduced at 41a0f75 with `--exam mock-sample --routes-only`, so it predates item 4. `--routes-only` alone is green. Owner: engine (You screen exam history).
- (5 Nov) O2 warnings on current content: 1,484 in all; O2-no-slip and O2-explain-answer sample at about 70% precision, so treat their hits as candidates, not findings (`docs/reports/engine-pass-o2.md`).

- (5 Nov, closed: user ruled practice-only, DECISIONS "Performance tasks in force") Was an open user decision, review-perf-pilots Q1: the proof L3 performance task gates met on a Stage 0 level the verb rule excludes (DECISIONS "Performance tasks in force").
- (5 Nov) ENGINE-BACKLOG 533 (per-case run time), 536 (follow-ups as their own step), 537 (aloud clock reading stored) deferred.
- (5 Nov) `docs/reports/coding-int-1-perf.md` describes the pre-fix task (`count_prefix`); the fix pass replaced it (add, remove, has, longest_listed, count_match). The review's Fix pass section is current.
- Session P (5 Nov): `playthrough.mjs --all --local-cdn` runs over two hours and its single browser closes after about 786 items ("Target page, context or browser has been closed"); every later item throws. coint/l12, backtest/l9, proof/homework-3 and topic-3.5 pass alone. Engine item in the inbox.

Session Q (5 Nov, PLAN 2c items 7, 10, 11):
- (item 7, updated S) After session S the pdes route reaches only odes L4 and numerics L4 unwritten (pdes/L2 reaches none). Was: (R) The pdes route reaches unwritten `complex` L1, `odes` L1 to L2 and `numerics` L4; the user put complex L1 in the before-2b set (DECISIONS "Capstones and route scope"); pdes stays "Route limited" until all are written.
- (item 7, closed R) Trader closure lever taken by the user: trader superday closure 422 lessons, 96 levels, 32 courses.
- (item 7, closed S: 25 sampled in `docs/reviews/review-diagnostic-why.md`, ten auditor-voice lines rewritten; DOM test `test-check-first.mjs`, 572) The 23 diagnostic `why` lines and most kept ones are the Sonnet draft, reviewed by closure impact and sampling, not line by line; a second reader should sample them. No DOM test of the "Check first" card.
- (item 7) `systems/L1` closure fell from 231 to 17 lessons (now cpp L1, L2 and terminal); accepted on the draft's evidence that systems teaches its ideas itself.
- (shard, 550) The relaunch does not cover a browser close during the routes block or `--bank`/`--drill` runs; routes run in shard 1 only.
- (session Q close, 5 Nov) Full `--all --shard i/4 --local-cdn` at 1ff7793: shards 2, 3, 4 all passed, 0 relaunches; shard 1 items all passed, its route checks failed `#bank` and samples because they ran on the played profile. Fixed in a0ea613 (fresh profile before the routes); `--all --shard 1/300` then green on both.
- (5 Nov, fixed in 9c70a04: fixture moved to brainteasers L3 and `contests/L2`, and the shadowed `readiness.status` restored) Since d9c1c40 (trader lever, item 8 session) `--routes-only` fails `gating` desktop and mobile: "trader: brainteasers L2 shows no advisory note for graphs-dp/L3" and "Developer: brainteasers L2 should still lock while graphs-dp/L3 is unmet". The check uses that edge as its role-advisory example and it is now `gate: false`; the check needs another example edge. Owner: the item 8 session (engine).
- (item 8) Capstone records are empty: no role can show "ready" until the user, as reviewer, fills `app/content/capstones.json` (AUTHORING section 15). The oa-drill rule maps every oa drill to coding-int's lowest gated code level (L1); an optional `level` on a drill overrides, none set.
- (closed S: `lint-dup-keys.mjs`, 571, 0 findings in app/js) (item 8) The engine pass shadowed `readiness.status(course, role)` with the role verdict, silently disabling advisory edges; caught by the gating playthrough after the fixture moved off a diagnostic edge, fixed as `roleState`. A duplicate-key lint on `content.js` objects would catch the class.
- (closed S, 570: 12 of 12 desktop, 3 of 3 mobile) (item 8, session R) `--exam mock-sample-draw` is intermittent at HEAD: 2 failures in 9 runs ("timed out with one answer per paper but scored 0"), 0 in 5 at d9c1c40 (pre-engine). The check calls `answerCorrect()` then `setRemaining(0)` with no wait, so the answer can miss the commit; item 8 touches no exam code, so likely timing, not proven. Engine item: wait for the answer to register before zeroing the clock, then re-measure.

Session S (5 to 6 Nov, PLAN 2c item 9 and the odes, numerics, complex wave):
- Protocol 6 threshold met: three second reads (odes, complex, numerics) found the author's number-recompute script never reads the lesson JSON, so prose claims, wrong-option values and `why` texts go unchecked; most errors sat there. Raised in BACKLOG-INBOX for a validator or script rule before the next wave.
- The odes brief's claim that critical damping (b = 4) settles fastest is false: b = 3 enters a 5% band at 1.56 against 2.37 (2.8% overshoot); l9 says so, the brief is unchanged.
- complex L2's `docs/briefs/complex.md` complex-step error figure was measured against a double; corrected to 4e-15 (all 16 figures).


Session T (6 Nov, waves 1 to 3):
- Git ref drift: the session opened detached at the origin tip 84a8143; the local `claude/amazing-wright-d4mx7i` ref points at 3bc7ee8, a stale pre-squash line (50 ahead, 77 behind, unrelated histories; origin holds all its files with newer content). Moving the ref was refused by the auto-mode classifier, so the session worked detached and pushed `HEAD:claude/amazing-wright-d4mx7i`. The local ref is left as it was; the next session can do the same, or the user can reset that ref.
- Fixed: `validate.mjs` ended with `process.exit()`, truncating large piped stdout, so `merge-wave.sh` sometimes read no error count ("validator failed errors"). Now `process.exitCode`.
- 577 (log ticks in `plane`): playthrough green; rendered labels not eyeballed.
- odes L4 review is capped at 10 items by the brief; numerics L3 requires odes/L4, so a 12-item review would cut repeated test-outs (AUTHORING section 11). Open for the user.
- convex l9 screens[6] (added in the fix pass) warns "a problem screen without a canvas before the ladder ends"; not fixed.
- momentum-rep `nw_t_by_hand` starter passes the lag-0 test (fails the others); pairs-rep l2 and l5 starters pass one test by construction.
- complex L3 brief: l9 table cells "graded as expression" cannot be built (cells are text with an accept list).
- Deferred engine items: `scatter` drag points have no `lockX` (stat-models); `space` curves cannot show direction (vector-calc L3); `derive` captions lack `sci()` (second sighting, convex L4); 19 wrong-versus-wrong overlap warnings remain (rule 581 companion, warning only).
- (open, user) Under Strict, `prereq.js` `advisory()` makes every reference into a course optional for the role non-blocking, including a course's implicit in-course chain: momentum-rep L2 opens before L1 is met for a trader profile. Decide whether in-course references stay blocking (ENGINE-BACKLOG 583 design note).
- Session T shards ran at 77ec3b3; later merges (vector-calc L3 and topic-3.1 fix passes, 583) were played through in their own passes and by `--routes-only` at ff41b0f; shard 1 rerun at ff41b0f started at close (result in PROGRESS if it finished).
- The validator warning count rose to about 2,277 (rule 581 companion overlaps, new O2 hits in new levels); errors 0.
