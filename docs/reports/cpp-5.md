# Report: cpp level 5, "C++ questions at interview"

## Files (all in `app/content/courses/cpp/`)

| File | Screens | Quiz / items | Code screens |
| --- | --- | --- | --- |
| `l19-moving-not-copying.json` | 10 | 5 | P-move-buffer (screen 6) |
| `l20-rule-of-five.json` | 10 | 4 | P-copy-samples (screen 6) |
| `l21-virtual-dispatch.json` | 11 | 4 | P-hand-vtable (screen 6) |
| `l22-undefined-behaviour.json` | 11 | 4 | P-add-overflows (screen 5) |
| `l23-own-smart-pointer.json` | 10 | 4 | P-unique-ptr (screen 3), P-shared-ptr (screen 6) |
| `review-5.json` | 10 items (difficulty 2 to 4) | | |
| `homework-5.json` | 9 items (difficulty 4 and 5; two `parts`, two `longform`, two `code`, one `order`) | | P-scope-guard, P-vec |

Code widgets are generated from `docs/briefs/cpp-scripts/P-*_starter.cpp`, `_solution.cpp` and `_tests.json` (nothing retyped); only `compare` was added to each test (`isclose` for doubles, else `equal`). Generators live in the scratchpad folder `cpp-5`.

## Checks

- Validator: 0 errors (about 610 warnings, none new beyond those below: point hints on `place` and `order` screens, one ladder canvas change in l19 and l21, one canvas-less `place` problem in l22).
- Playthrough (local CDN): every lesson, `review-5` and `homework-5` passes at desktop, `--mobile` (440) and `--tablet` (1032 and 1376). Screenshots were read for the graph screens (l19 2, l21 2, l23 1 and 7), the `place` screen, the table screens and the homework table; the l21 graph was redrawn after a phone overlap.
- App toolchain (`cpp-scripts/app_toolchain/run.mjs`, c++17, clang 21 + libc++): solutions fail 0 tests; starters fail P-move-buffer 9 of 15, P-copy-samples 11 of 13, P-hand-vtable 6 of 11, P-add-overflows 7 of 13, P-unique-ptr 14 of 15, P-shared-ptr 14 of 15, P-scope-guard 8 of 12, P-vec 11 of 15.
- After merging engine items 518 to 520: P-copy-samples `delete-first-no-guard` now fails 1 of 13 (the `a = a` test, "expected 3 got 0", reading poison); P-move-buffer `move-ctor-forgets-null` fails 7 of 15 and `move-assign-forgets-null` 6 of 15, each with "Memory error: a block was deleted twice."
- `facts_l19.cpp` through the app's clang 21: copies and moves identical to the brief (1 and 0; 0 and 1; elision 0; `const` copies; 7 moves, 0 copies for four pushes; 1 copy and 2 moves with a non-`noexcept` move; `make_moved` 1 move, `make_named` 0). No difference.

## Numbers and sources

8,000,000 bytes and 0.8 ms (1,000,000 x 8 B at 10 GB/s), 7 moves, 1 copy and 2 moves, 8 and 16 byte `Buffer`, sizes 8, 12, 16, 24 (wasm32 `static_assert`s, `wasm_sizes.cpp`), 4,294,967,295, £21,474,836.47, £42,949,672.95, 2,500,000,000 pence, 400,000, 200,000 and 10 ms (200,000 x 50 ns = 10,000,000 ns), 1,000 x 1,000 x 8 = 8,000,000 bytes: from `number_checks.py` and by hand, as in the brief's "Number checks".

## Choices and deviations

- l21 screen 3 shows the 8-byte `B` in the question and the 12-byte `D` only in the explanation, so the picture does not give the answer away.
- l19 screen 6 uses an `array` of the four `Buffer` fields (before and after the move) rather than a table, so the ladder keeps one canvas kind with screens 4 and 5.
- Meyers and the Core Guidelines are named once (l19 screen 9), cppreference once (l20 screen 9). The l20 `a = a` text never says it exposes a delete-first assignment (brief note), although the engine item now makes the test catch it.
- Voice: no em-dashes or exclamation marks; learner-facing sentences were kept short by hand, not by a checker.

## Proposed `course.json` change

None.

## Engine limitations

Six bullets in `docs/BACKLOG-INBOX.md` under "cpp L5 (5 Nov)".
