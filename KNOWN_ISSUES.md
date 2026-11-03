# KNOWN ISSUES

Open at migration (27 Oct 2026)
- A single `--all` run is too long for one browser and the 2-hour background limit (the browser closed after about 1,100 items); always split it into lessons, `--sets`, and `--exams` plus `--routes-only`.
- `docs/BACKLOG-INBOX.md` holds about 136 unnumbered engine bullets awaiting pass 7, plus about 42 from the seven gap levels (27 Oct).
- Gap briefs and Stage 3 briefs (`docs/briefs/gap-*.md`, `momentum-rep.md` and others) name scratchpad and pkgs paths from an older session; give agents the current paths.
- Topic exams 1.3, 1.4, 1.5 sit at the validator's 30-item cap (markov L5, 28 Oct, has no exam items; `docs/reports/markov-5.md` names candidates); gap items are packed into multi-part tables marked all or nothing, and the 1.3 curve sketch is typed, not tapped (inbox bullets ask for partial credit and compound items).
- Seven homework items have both prose and a hidden longform prompt (list in ENGINE-BACKLOG.md pass 6 note).
- Stage 1, 2 and 3 have no stage exams; topics 3.x have no topic exams.
- Learn header still says 3,100 hours (curriculum: 3,530; quant path 3,330), stage hours ignore "Quant path only", and the Paths view is unfiltered (ENGINE-BACKLOG item 428). Direct links to hidden pure courses still open.
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

Session B (4 Nov 2026)
- mock-oa-arith's 16 decimal, fraction and percentage items are fixed, so resits repeat them (inbox bullet asks E4 for those operations). Its start card's parts list squeezes at 390 px (engine, inbox).
- mock-oa-sig and mock-oa-trader are briefed but unwritten; E3 (fresh draws) and E15 (calculator) are not built.
- The 12-screen lesson cap pushed several brief drills into quizzes in brainteasers L2 and L3 (listed in their reports).
- Raw `git stash -u` while agents write untracked files hides their files for a moment; use `git pull --rebase --autostash` and stage the manifest entry by entry.
