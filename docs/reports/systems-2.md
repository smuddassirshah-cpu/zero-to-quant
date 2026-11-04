# Report: systems level 2 (Concurrency)

Author: content agent, 4 November 2026. Brief: `docs/briefs/systems.md` `## Level 2`, with the course context, shared runtime facts, engine limits, E items, code problems P-final-counts, P-lock-cycle and P-blocked-counts, and the number checks. Followed `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md` in full (section 4 `interleave`, section 5 "Follow-up parts", section 7 "Interleave rules"), `app/js/engine/canvas/README-B.md` (`interleave`) and the engine report `docs/reports/engine-pass-c-c.md`. This is the first level to use the `interleave` canvas in lessons.

## Files written

All in `app/content/courses/systems/` (plus `app/content/manifest.json`, rewritten by the validator).

| File | Screens or items | Quiz | Canvases and widgets |
|---|---:|---:|---|
| `l6-threads.json` | 9 screens (difficulty 1 to 3) | 4 | `console` listing with `tap-regions` (hook); `interleave` U1 explore (`multi`, outcomes found) and a tap of the shared steps; `console` with `table` (cost); trap `choice`; edge `choice` (reference capture); generalise; drill `table` (tags `thread-shared-state`, `thread-cost`, pace 480); transfer `numeric` 240 |
| `l7-data-races.json` | 11 screens | 4 | `interleave` U2 hook (tap `a1`, `b1`), explore, count; U3 ladder (`multi`); U4 ladder (`numeric` 4); trap on an x86 listing; edge (plain `bool` flag); generalise; drill `table` on the 924-schedule canvas (tag `race-outcomes`, pace 480); `code` P-final-counts; transfer on the position canvas (outcomes table) |
| `l8-locks-and-deadlock.json` | 12 screens | 4 | `interleave` U5 hook; U6 explore (tap `t1-2`, `t2-2`) and count; ring ladder (6 of 168); `graph` directed with `tapEdges` (tap `e-C-A`); cost `table`; trap on a `console` listing; edge: one lane locking `m` twice on `interleave`; generalise; drill `table` (tag `lock-order`, pace 480); `code` P-lock-cycle; transfer `table` (95, 105) |
| `l9-atomics.json` | 11 screens | 4 | `interleave` U8 hook; U9 explore (`multi`); store-buffer `console` with `choice`; U10 `multi` and swapped U10 ladder; cost `table`; trap on the atomic check-then-set canvas; edge `x = x + 1` canvas (`numeric` 4); generalise with a table of orders; drill `table` on U9 (tag `litmus`, pace 450); transfer `choice` on a hand-off listing |
| `l10-producer-consumer.json` | 10 screens | 4 | `interleave` U11 hook (tap `p2`) and explore (`numeric` 5); the fixed condition variable on `interleave` (`choice`); `order` with two distractors beside a `console`; bounded queue `array` with a `table`; trap `choice` (polling); edge `choice` (shutdown); generalise; drill `table` (tag `bounded-queue`, pace 450); transfer `numeric` 100% |
| `review-2.json` | 9 items, difficulty 2 to 4 | | the brief's nine items in order, each tagged and paced; items 3 and 6 carry static `interleave` canvases; item 9 carries `sy-concurrency` and `sy-memory` |
| `homework-2.json` | 7 items, difficulty 3 to 5 | | 1 `parts` numeric, multi, numeric, numeric (d4); 2 `code` P-blocked-counts (d3); 3 `parts` choice, numeric, choice, choice (d4); 4 `longform`, 10-point rubric and model (d5); 5 `order` with three distractors (d4); 6 `parts` multi, choice, numeric, choice (d5); 7 `numeric` 480 (d3) |

Every lesson: skills `sy-concurrency` (course.json), one trap, one edge case, a drill screen with a pace in its prose, a follow-up transfer, and no non-task screens (every generalise has a confirmation item). The cppreference thread-support pages are named once, in l6 screen 7, by title and kind. Every round figure is stated as an assumption where it is first used in a lesson. 11 `interleave` uses in 5 lessons (U1 to U11), plus the brief's other enumerated sets (position, atomic flag, `x = x + 1`, the 924-schedule drill, the fixed condition variable, the broken ring).

## Validator

`node tools/validate.mjs` from `app/`: 0 errors, 428 warnings, none from these seven files.

## Voice

`VOICE_BASE=<worktree>/app/content/courses/systems python3 docs/reviews/voice-scan.py`: 0 explanations over three sentences, 0 sentences over 20 words (5,557 scanned across the course). No exclamation marks, no em-dashes, no American spellings.

## Playthrough

From `app/`, all seven files in one run with `--local-cdn <scratchpad>/pkgs`, then again with `--mobile --shots` (390 px). Final runs after the last edit:

| File | Desktop | Mobile |
|---|---|---|
| l6-threads | ok, 13 checks, quiz 4/4 | ok |
| l7-data-races | ok, 15 checks (C++ compiled), quiz 4/4 | ok |
| l8-locks-and-deadlock | ok, 16 checks (C++ compiled), quiz 4/4 | ok |
| l9-atomics | ok, 15 checks, quiz 4/4 | ok |
| l10-producer-consumer | ok, 14 checks, quiz 4/4 | ok |
| review-2 | ok, recorded 9 of 9 | ok |
| homework-2 | ok, marked 7 of 7, 33 of 33 marks; parts checks ok | ok |

"All passed" each time (a `--why` desktop run also passed). Homework-2 was replayed at both widths after its last listing edit.

### The canvas in light and dark

`--shots` shows only the opening state, so I also used a scratch Playwright script (`<scratchpad>/systems-2/shots.mjs`) at 390 px in light and in dark: for every `interleave` screen of l6, l7, l8, l9 and l10 it shot the opening state, stepped the first enabled lane until the schedule ended, shot again, and opened the Why? sheet. No console errors. A second script (`probe.mjs`) read every derive caption before and after a schedule ("total is 36 after 6 of 6 steps.", "Deadlock: no lane can step.", "Finished: r1 = 0, r2 = 1.", "The consumer is awake."). What I saw and fixed:

- With three lanes, step ids from lane ids that end in a digit broke across lines ("t1-" then "3 unlock B"). The ring now uses lanes P, Q and R (ids `p1` to `r4`); two-lane U6 keeps T1 and T2, which fit.
- Long `console` lines were cut at 390 px. Every listing is now at most about 36 characters a line, `wrap` is on, and line numbers appear only on the three listings whose text names a line (l6 hook, l7 trap, l9 store buffer).
- The l10 bounded-queue `table` had four columns and lost its last one at 390 px; it is now two columns of six rows.
- Done steps, blocked lanes, the deadlock banner and the outcomes table read well in both themes. In a two-lane layout the order badge of a done step sits over the last word of a long step text ("store total from"); it stays readable (backlog bullet).

## C++ in the app (YoWASP clang 21, `-O1`, no exceptions)

Code is copied exactly from the brief (`cpp.py` in the scratchpad holds it). I adapted the coding-int L1 agent's `codecheck.mjs` to this worktree: it opens each code screen and the homework code item in the real app, Checks the untouched starter (one character added so it counts as engaged), then the model solution.

| Problem | Solution | Starter |
|---|---|---|
| P-final-counts (l7 screen 10) | 7 of 7 | passes 2 of 7 (fails 5, as the brief) |
| P-lock-cycle (l8 screen 11) | 12 of 12 | passes 6 of 12 (fails 6, as the brief) |
| P-blocked-counts (homework item 2) | 7 of 7 | passes 2 of 7 (fails 5, as the brief) |

Each Check took 1 to 4 s after the compiler loaded. Every hidden-test `expect` was also recomputed by an independent Python model (a memoised walk for `final_counts`, Kahn's algorithm for the cycle test, a list queue for `blocked_counts`) and asserted equal.

## Numbers

Every count of schedules or outcomes stated in the level is read from the canvas's own engine: `enum.js` loads `app/js/engine/canvas/interleave.js` and enumerates every `interleave` spec in the seven files (and the specs in `h.py`). Its output equals the brief's table and `docs/briefs/systems-scripts/level2/interleave.py` and `more.py`, which I also ran:

- U1 total 10 (9), 26 (9), 36 (2) of 20; U2 1 (18), 2 (2) of 20; U3 1 (1,404), 2 (270), 3 (6) of 1,680; U4 (20, 80) 2 and (20, 160) 4 of 6; U5 2 of 2 at 2; U6 complete 4, deadlock 2 of 6; ring 162 and 6 of 168; ring broken 142, none deadlock; one lane locking twice: deadlock 1 of 1; U8 2 (2) and three lanes 3 (6); U9 (0, 1) 1, (1, 0) 1, (1, 1) 4 of 6; U10 (0, 0) 1, (0, 42) 4, (1, 42) 1; swapped (0, 0) 2, (0, 42) 1, (1, 0) 1, (1, 42) 2; U11 awake 5, asleep forever 1 of 6; the fix 5, none asleep; position 200 (9), 300 (2), 600 (9) of 20; atomic check then set: 2 inside in 4 of 6; `x = x + 1` on an atomic: 1 in 4 of 6; drill 924 = 702 + 216 + 6.

Every other number was computed twice by `l2_checks.py` (method A floats or a closed form, method B Fractions or a brute-force count of distinct lane orders), 54 checks, 0 bad:

- l6: 3 cores, 7.8 GiB (7.8125), 512 MiB, 66,667 creations a second, 60 ms against 0.25 ms, 240 times; quiz 30%, 8 copies.
- l7: 20, 1,680, 924, 6 ($\binom{4}{2}$), 918, 90 ($6!/2!^3$), 70 ($\binom{8}{4}$), 369,600 interleavings for four threads.
- l8: 70 plain interleavings against 6 legal schedules; 0.1 s and 20 s (200 times); 6 = $3!$; £95 and £105; quiz 25 ms, 40%.
- l9: 0.02 s, 0.24 s, 4 ms of work (1 ms a core), 12 times; 0.667; quiz 120 ms, 2,000.
- l10: 1 ms worst, 0.5 ms average, 5,000 main-memory reads; tallies (1, 1, 2), (0, 1, 0), (2, 0, 0), (1, 1, 0), (1, 0, 2); 50 times; 12.5%; 100%; quiz 1 ms.
- review: 1.5 cores, 2 of 20, 2 of 6, 60 times. Homework: 20, 9, 300, 2 of 6, 0.667, 0.24 s against 0.5 ms, 480 times; longform 0.5 ms against 5 µs, 100 times.

## Where the canvas's deviations change what a lesson can claim

- `wait` does not take its lock back on waking. l10 screen 3 says so in its prose: "The real `wait` also takes `m` back before it returns; the canvas leaves that step out." The fixed program's count (5 schedules, none asleep) is the canvas's own, and the brief's.
- `notify` wakes every sleeper. l10 screen 3's explanation says the canvas's notify acts as `notify_all`. The two-consumer "if or while" case is taught from a `console` listing and an `order` widget, not stepped on the canvas.
- No store buffer. Every litmus statement on the canvas is worded "if steps run one at a time": l9 screens 2 and 4, review-2 item 7, homework-2 item 6 part a. The (0, 0) result comes from a `console` listing of a store-buffer run (l9 screen 3) and a `choice` (homework-2 item 6 part b), as the brief and the engine report say.
- The broken ring's "142 schedules, none deadlock" is stated in the l8 graph screen's explanation and comes from the engine's enumeration of that spec; that screen's canvas is the `graph`, so the line says "stepped as lanes", not "the canvas".

## Where the files differ from the brief

- Homework item order: the brief's item 2 (four-part position) is first and the code item second, because the playthrough's homework parts check still assumes the parts item is item 1 (L1 did the same). Items 3 to 7 keep the brief's order.
- l6: U1 is the explore screen (before the cost), then a tap of the four steps on `total` (loads and stores), where the brief's mark said "the three steps on `total` of either lane". The drill adds two cost rows (512 MiB, 66,667) to the brief's two snippets.
- l7: the drill asks 924, 6, 918 and a new case, 90 (three lanes of two steps); 702 and 216 cannot be counted by hand, so they are read from the canvas's table in the drill's explanation and reproduced by the code screen. The brief's other marks (U3 "the last stale load", U4 "the check that acts second") are hint highlights.
- l8: the explore screen is U6 with the brief's mark (the second lock step of each lane); the ring ladder asks the 6 deadlocks ($3!$) before the graph. The ring's lanes are P, Q and R for the 390 px layout. The self-deadlock edge is stepped on the canvas (one lane, `lock m` twice).
- l9: the store-buffer screen is a `console` listing (the canvas cannot show it). The trap uses the brief's atomic check-then-set enumeration (both enter in 4 of 6); the edge is `x = x + 1` (4 of 6 end at 1). U9's mark is not used; U10's is the explanation's highlight.
- l10: the bounded-queue worked example asks two runs by hand (capacity 2, PCCPPP; capacity 3, PPPCCCC) so the drill's runs stay new.
- Generalise screens of l6, l9 and l10 carry a short display formula, because the validator asks for KaTeX in a lesson with no `code` widget in a speed-track course (backlog bullet).

## Conventions

No seeded data and no data files. Lane registers are `r` (or `r1`, `r2` in litmus tests); litmus programs use `notation: "assign"`. Locks are capital letters or `m`. Every `interleave` canvas opens with an empty schedule; explanations patch `schedule` and `outcomes: true`. Scratch scripts (builders, checks, shot and probe scripts) are in `<scratchpad>/systems-2/`.

## course.json

No change proposed.

## Backlog

Eight bullets under "Raised later (systems L2, 4 Nov)" in `docs/BACKLOG-INBOX.md`: `wait` re-taking its lock; a `notify-one` op; a store buffer (by design, recorded); step ids breaking across lines in three lanes; the order badge over long step text; the generalise KaTeX rule for code-free lessons of a C++ course; `--shots` of a played schedule and the Why? sheet; and seconding the open homework parts check and starter check bullets.
