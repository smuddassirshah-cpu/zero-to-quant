# Engine pass C, agent C: item 471 (E13 `interleave`)

## Status line (for the backlog's status block)

471. Done (E13, with E13-blocked-lanes and the systems brief requirements): `interleave` canvas (`js/engine/canvas/interleave.js`, `css/interleave.css`; HTML in the canvas wrapper, readable at 390 px in both themes). Fields: `params.lanes` (1 to 3 lanes, 8 steps a lane, 24 in all; `id`, `label`, `short`, `steps`, `regs`), `vars`, `locks`, `outcome` (variables, `"a.r1"`, `{ label, of }`), `endings` (renames complete, deadlock, asleep), `notation` (`words`, `assign`); steps `load add store set fetch-add lock unlock wait notify`, each with an optional `if` expression, or `ops: [...]` run as one step with `text`; `state.schedule` (lane ids stepped: the whole state), `state.outcomes` (`true`, `"found"`), `selected`, `highlight`, `caption`. A lane whose next step is a held lock is disabled and drawn blocked; no steppable lane ends `deadlock` (a lane blocked on a lock) or `asleep` (only sleepers left); a `wait` sleeps until a later `notify`. Tap mode marks steps (ids `a1`, `t1-2`). `values()` for derive: shared values, `ending`, `steps`, `order`, `outcome`, `regs`, `reached`, and the enumeration `outcomes`, `outcomeList`, `schedules`, `complete`, `deadlock`, `asleep` (memoised walk over states, cached per spec). Methods `step`, `play`, `finish`, `undo`, `reset`, `enabled`, `ending`, `outcomes`. Validator rules: lane count and size, ids unique, op and per-op fields, names in expressions, variables and locks exist, reserved variable names, `outcome` entries, `endings` keys, `notation`, `state.schedule` and `enter.schedule` replay legally, `state.outcomes`, enumeration under 200,000 states, unlock-without-lock warning, `tap-regions` ids checked against the step ids; an `explore` screen on this canvas needs no controls. Player: Start over and the tap hint know it. Gallery: five cards. Sample: `content/exams/mock-interleave-sample.json` (`"sample": true`). Files: `js/engine/canvas/interleave.js`, `css/interleave.css`, `index.html`, `js/engine/player.js` (two one-line edits), `js/screens/system.js`, `tools/validate.mjs`, `canvas/README-B.md`, `docs/AUTHORING.md` (section 4 and 7).

## What was built

The engine is the first half of `interleave.js` with no DOM. `tools/validate.mjs` loads it with `require` (as it does for `complex-map.js` and `trade.js`) so the validator replays `state.schedule` and runs the enumeration with the same code the learner meets. The second half is the canvas, built on `C.instance` like `table` and `console`.

- Stepping: each lane has a Step button (44 px high). A lane that cannot step (blocked on a lock, asleep, finished) has its button disabled and a status line: "Blocked: B is held by T2", "Asleep, waits for a notify", "Finished". Rows show done (solid, with a result such as `r = 0` or `bal = 20, cash = 160` and the order number in a dark badge), next (ringed), blocked (amber) and pending (dashed).
- History: an "Order: a1, b1, a2" line, Undo and Reset. The ending banner says who waits for what.
- Shared state: chips for each variable and each lock (`A held by T1`).
- Marking: step rows are `data-tap` rows, so `tap-regions` works unchanged (the Step buttons keep working in tap mode). Graded, reveal, highlight and flash states are spelled out in `interleave.css`.
- Outcomes table: `state.outcomes: true` lists every outcome with its schedule count and washes the row the current schedule reached; `"found"` lists only the outcomes the learner has finished at ("Outcomes found: 2 of 3").
- Walk of every schedule: a memoised recursion over `(pcs, vars, regs, locks, asleep)` counting schedules by outcome, cached per spec. All 20 programs in the check run below enumerate in under 5 ms.

## Acceptance criteria and how each was proven

The check script (scratchpad `il/uses.js`) builds every use in `docs/briefs/systems.md` and the "other enumerated sets" from `docs/briefs/systems-scripts/level2/` and prints the canvas engine's counts. Every count equals the brief's (and the Python enumeration in `interleave.py` and `more.py`):

| Brief | Canvas engine |
| --- | --- |
| U1 10 (9), 26 (9), 36 (2) of 20 | `total=10` 9, `total=26` 9, `total=36` 2 |
| U2 1 (18), 2 (2) of 20 | `x=1` 18, `x=2` 2 |
| U3 1 (1,404), 2 (270), 3 (6) of 1,680 | same |
| U4 (bal 20, cash 80) 2, (20, 160) 4 of 6 | same |
| U5 2 only, 2 schedules | `x=2` 2 |
| U6 complete 4, deadlock 2 of 6 | same |
| U7 same order 2; ring 162 and 6 of 168; ring broken 142, 0 | same (34,650 plain interleavings are never walked) |
| U8 2 (2); three lanes 3 (6) | same |
| U9 (0,1) 1, (1,0) 1, (1,1) 4; (0,0) 0 | same |
| U10 (0,0) 1, (0,42) 4, (1,42) 1; swapped (0,0) 2, (0,42) 1, (1,0) 1, (1,42) 2 | same |
| U11 awake 5, asleep forever 1 of 6; fix 5 schedules, 0 asleep | `awake` 5, `asleep forever` 1; fix 5 and 0 |
| position 500, +100 and -300: 200 (9), 300 (2), 600 (9) | same |
| both enter 4 of 6, one in 2 | `entered=2` 4, `entered=1` 2 |
| atomic `x = x + 1` as load and store: 1 in 4, 2 in 2 | same |
| two lanes, two increments each: 924 = 702 + 216 + 6 | same |

The criteria in the inbox, one by one:

- (a) Step set: load, add, store, fetch-add, lock, unlock, wait, notify, plus `set` (to compute a flag such as `ok` or `e`) and conditional steps through `if` on any op. Proven by the U4 and U11 enumerations above and by the sample items 4 and 3.
- (b) Blocked lanes: a lane whose next step locks a lock held by another lane is disabled (browser check: after `t1`, `t2` both Step buttons are `disabled`, a click on a blocked lane leaves the order unchanged, light and dark) and a schedule with no steppable lane ends "deadlock" (banner "Deadlock: no lane can step. T1 waits for B (held by T2); T2 waits for A (held by T1)."; U6 and U7 counts).
- (c) Wait: sleeps until a notify that begins after it, otherwise "asleep forever" (browser check `play(["c","p","p","c"])` returns `asleep`; U11 1 of 6; the "asleep forever" banner and lane state were inspected in the screenshots).
- (d) Marks: steps are tappable; sample item 1 (`answer: ["a1","b1"]`) and item 3 (`["p2"]`) play green through the set-mode hook, and a screenshot at 390 px shows the marked rows in manipulable blue. `values.outcomes` gives each reachable final including `deadlock` and `asleep` with its count (sample items 2, 4, 5 and 6 and the gallery caption "2 of 6 schedules deadlock.").
- (e) Up to 3 lanes of 4 steps with the enumeration cached: the canvas accepts 3 lanes of up to 8 steps (the U7 ring is 12 steps, the 924 drill 12). The result is memoised per spec in `cache` and reused by every `values()` call.

Playthrough, from `app/`, with `--local-cdn` set to the scratchpad `pkgs` folder:
- `node tools/playthrough.mjs --exam mock-interleave-sample`: 6 items, 6 of 6, passed; the mock checks (seed, clock at zero, attempts kept) pass. The same with `--shots <dir> --mobile`: passed, 390 px screenshots written.
- `node tools/playthrough.mjs --routes-only`: every route ok including `#system` (the gallery draws all five interleave cards with no console error), all bank and deck checks pass, "All passed".
- `node tools/playthrough.mjs --all`: see "Full run" below.
- `node tools/validate.mjs`: 0 errors (the 392 warnings are the existing ones; none is from this work).

Screenshots at 390 px, light and dark, inspected (scratchpad `il/out/`): gallery cards for the lost update (three lanes, `x=` table), the asleep-forever wait, the conditional steps and the deadlock; the drive of the deadlock card in dark mode; the exam item with marked steps in dark mode; the exam item at 390 px from the playthrough. Findings fixed: counts now read "1,680" rather than "1680". Nothing else needed changing: three lanes fit at about 110 px each, text wraps to two lines, the Step buttons stay 44 px high, and both themes show the dashed blocked and asleep lanes.

Validator rules were tested with a scratch file of 20 cases (mock-zz-bad, deleted afterwards): four lanes, no lanes, too many steps, unknown op, unknown variable, `store` with both `reg` and `value`, a malformed expression, an unknown name in `if`, a reserved variable name, a duplicate lane, an undeclared lock, an unknown `outcome` entry, a bad `endings` key, a bad `notation`, a schedule naming a missing lane, a schedule stepping a blocked lane, a bad `state.outcomes`, a `tap-regions` answer that is not a step id, an `unlock` with no `lock` (warning), and one good control. Each bad case gave the expected line and the good one gave none.

A runtime check of the instance contract (`il/api.mjs`, in a page): `play`, `finish`, `reset`, `undo`, `enabled`, `ending`, `highlight` (lane and step ids), `mark`, tap mode selection, `lock`, `clone` (static copy: no buttons, no bar, same schedule) and a `derive` caption reading `values.order`, `values.outcomes["asleep forever"]`, `values.schedules` and `values.reached`. No console errors.

## Sample and the course question

The sample is `app/content/exams/mock-interleave-sample.json`, a one-paper mock (`"sample": true`, `style: "developer"`), not a lesson. A lesson must be listed in a course's `course.json` and every folder under `content/courses/` must be a course, so a lesson used by no course cannot exist without inventing a course that the app would list; a mock exam has no such tie and its items take a `canvas`, a widget and `derive` exactly as lesson screens do. Its six items: a lost update (tap `a1` and `b1`), a deadlock (numeric 2, the canvas opens on the deadlocked schedule), an asleep-forever wait (tap the notify `p2`), a conditional step (U4, numeric 4), outcomes enumeration (three lanes, `values.outcomes['x=3']` in a derive caption, numeric 6), and the outcomes-found mode on the store-buffering test (numeric 4). The validator accepted the top-level `"sample": true` as it stands (it ignores unknown top-level keys), so no rule was added; agent A's flag will hide it from the exam list when it lands. The lesson-only paths (demonstrate steps, explore screens, Start over) are covered by the validator rules and the `explore` allowance, not by a playthrough; a level author's first lesson will be the first to exercise them (follow-up 1).

## Deviations from the brief and justifications

1. Parameter names are mine (the brief says so): `lanes[].steps[]` with `op` fields, `vars`, `outcome`, `endings`, `state.schedule`. The brief's words map directly: "load r from x" is `{ "op": "load", "reg": "r", "var": "x" }`; "store total from r" is `{ "op": "store", "var": "total", "reg": "r" }`; U9's `x = 1` is `{ "op": "store", "var": "x", "value": 1 }` (or `notation: "assign"` shows `x = 1`).
2. I added a `set` op (register = expression) because "check queue empty" (U11 `c1`) and "ok = r at least 80" (U4) compute a flag without touching shared state. The brief's conditional steps (`if ok: ...`, `c2 waits only if c1 saw an empty queue`) are `if` on any op, which covers them.
3. A step may hold several ops (`ops: [...]`) run as one indivisible step, as the brief's own enumeration does (U4's check is a load and a compare in one step; "cash out" shares the step with the store). `text` names such a step.
4. `wait` releases its `lock` only when it actually sleeps, and a woken lane does not take the lock again. This reproduces the brief's count of 5 schedules and 0 asleep for the fixed condition variable; an author who wants the re-take writes a `lock` step after the wait.
5. A `notify` wakes every sleeper (the brief's enumeration does the same). No `notify_one`.
6. A stuck schedule is `deadlock` if any lane is blocked on a held lock, else `asleep` (the brief's sentence is "no lane can step ends deadlock" and "a wait with no later notify ends asleep forever"; a sleeper that holds a lock another lane wants is a deadlock by the first rule).
7. U11's "awake" and "asleep forever" come from `outcome: []` with `endings: { "complete": "awake", "asleep": "asleep forever" }`; with the default `outcome` (every shared variable) the complete outcome is named by its values (`q=1`). `values.outcomes` keys for a finished schedule with values are `name=value, name=value`, so a derive reads `values.outcomes["x=1"]`.
8. Only steps are tappable marks (the brief says "tap-to-mark the racing step"). Lanes, variable chips and lock chips take `highlight` but not taps.
9. The store-buffer option (inbox E13 detail b) is not built; it was optional. `l9-atomics` teaches the (0, 0) outcome from a `choice`, as the brief says.
10. Limits are stated by the validator: 3 lanes, 8 steps a lane, 24 steps in all, 200,000 states. The brief's "up to 3 lanes of 4 steps (the U7 ring is 12 steps)" fits inside; the 924-schedule drill (two lanes of six steps) does too.
11. The sample is a mock exam, not a lesson (above).

## Shared files touched (small, localised)

- `app/index.html`: one `<link>` and one `<script>` line.
- `app/js/engine/player.js`: the tap hint ("Tap a step to mark it") and `movable` (so Start over shows) each take one clause.
- `app/js/screens/system.js`: one `CANVAS_SAMPLES` entry, one `CANVAS_ABOUT` entry and four `CANVAS_EXTRAS` cards.
- `app/tools/validate.mjs`: the `require` line, the `CANVASES` set, `authorMovable`, `regionIds`, and one `if (c.kind === 'interleave')` block in `checkCanvas`.
- `docs/AUTHORING.md`: a table row and a paragraph in section 4, a rules paragraph in section 7. `canvas/README-B.md`: a full `interleave` section with a worked example per acceptance criterion.
- `app/content/manifest.json` (regenerated by the validator, one new exam).

## Follow-ups

1. The first `systems` level 2 lesson will be the first to use `interleave` in lesson mode (demonstrate steps patching `schedule`, explore screens, hints with `highlight`). Please play it with `--shots --mobile` once it exists.
2. The validator replays `state.schedule` and `enter.schedule`, but not `schedule` in `explain.canvas`, `demonstrate.steps[].canvas`, hints or wrong-answer patches. An illegal schedule there is ignored at the first bad entry (with a console warning). A patch walker would need a shared patch visitor in the validator.
3. No widget grades a schedule ("make `x` end at 1"). The brief does not ask for one; the sample asks for marks and counts instead. If wanted, a `tap-regions`-style `schedule` answer would read `values.outcome`.
4. `playthrough.mjs --shots` shows the canvas at its opening state. A `canvas.finish()` call before the shot would show the ending banner; not added to keep the shared tool untouched.
5. The level author should state a count such as "of 168" only from `values.outcomes`; the brief's own table already agrees with every count above.

## Full run

The full `--all` run (every lesson, route, review, homework and exam) was sharded to finish in time: the 944 written lessons in three parallel `--lesson` runs, then `--sets --exams` (481 sets and exams, including `mock-interleave-sample`), then `--routes-only` (earlier, above). Every run ended "All passed" with no failure and no console error; none was re-run. `node tools/validate.mjs`: 0 errors.
