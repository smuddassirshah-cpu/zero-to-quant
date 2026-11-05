# Topic 1.9 exam extension: second-reader findings

Scope: the five new items of `app/content/exams/topic-1.9.json` (e-const-move, e-vector-growth, e-ub-which, e-virtual-dtor, e-code-clone-basket) and the exam-level changes (30 items, 75 minutes, ramp). Read: `docs/AUTHORING.md`, `docs/briefs/cpp.md` "Exam topic-1.9 extension", `docs/reports/exam-1.9-ext.md`, cpp l19 to l23 and `review-5`.
Method: every snippet compiled and run with `clang++ -std=c++17 -O1 -fno-exceptions` and `g++` (same flags); the vector snippet and the clone-basket item also run in the app toolchain (YoWASP clang 21, libc++ debug hardening, `-fno-exceptions`) with the app's own `unit()` builder. For clone-basket the exam file's own starter, solution and 11 tests were loaded (not the brief's scripts) and four mutants and one alternative form of my own were added. Layout screenshots at 440, 1032 and 1376. Voice scan on a scratch copy.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching or testing issue; note = style.

Counts: 0 errors, 4 warnings, 5 notes. Answers: 5 of 5 keys match native g++ and clang. One key (e-vector-growth) does not match the app's own toolchain (warning 1).

## Answers, run independently

| item | key | g++ | clang (libstdc++) | app toolchain (libc++, no exceptions) |
| --- | --- | --- | --- | --- |
| e-const-move | 3 | 3 | 3 | 3 |
| e-vector-growth | 3 copies | 3 copies, 4 moves, capacity 1, 2, 4, 4 | same | 0 copies, 7 moves (see warning 1) |
| e-ub-which | zero-div, const-cast, wrong-delete | `s[s.size()]` is 0, `unsigned char` wraps to 0 | same | same |
| e-virtual-dtor | `~Derived` runs, `gone` 1 | 1 | 1 | 1 |
| e-code-clone-basket | solution passes, starter fails | n/a | n/a | solution 0 of 11 fail, starter 9 of 11 fail |

UB rules for e-ub-which (C++17): `5 / n` with `n == 0` is [expr.mul]/4; writing through `const_cast` to an object defined `const` is [dcl.type.cv]/4; `delete` on a `new[]` block is [expr.delete]/2; `s[s.size()]` is defined and returns `charT()` ([string.access]); unsigned arithmetic wraps modulo 2^N ([basic.fundamental]/2), and `++b` on an `unsigned char` converts back to 0. e-virtual-dtor is defined because `make_shared<Derived>` stores a deleter for `Derived` and the conversion to `shared_ptr<Base>` keeps the control block ([util.smartptr.shared.const]).

## e-vector-growth

- app/content/exams/topic-1.9.json | e-vector-growth (also l19 screen "A move that can throw") | warning | The key 3 is right for every library that honours `move_if_noexcept`, and the prose rightly calls the growth factor a library choice. But the app's own compiler (libc++ with `-fno-exceptions`) treats every move as non-throwing, so a learner who pastes the snippet into any C++ code widget sees `copies 0 moves 7` and the key looks wrong. g++/libstdc++ prints 3 and 4 even with `-fno-exceptions`. The l19 screen makes the same claim. | Add one sentence to the explanation (and to the l19 explain): "Built without exceptions, as the code widgets here are, libc++ moves anyway, so a run here prints 0 copies." Also add a KNOWN_ISSUES line.
- app/content/exams/topic-1.9.json | e-vector-growth feedback | note | `generic` covers 1, 2, 5 and 6 (plausible slips: counting only the first growth, or counting growth at the fifth push). Fine for a 90 s item. | Optional: a `wrong` value 1 with "That is the first growth only. The vector grows again at the third push."

## e-ub-which

- app/content/exams/topic-1.9.json | e-ub-which explain | warning | "Defined does not mean useful, but it cannot break the program" is not true as a general claim: a defined line can still be a logic bug. | "Defined means the standard fixes the result. It may still be a bug."
- app/content/exams/topic-1.9.json | e-ub-which feedback | warning | Under-selection teaches nothing: a learner who ticks only the division and misses `const_cast` and the mismatched `delete` (the two instructive lines) gets the generic line only. `byKey` has entries for the two false-positive options but none for the two correct options. | Add `byKey` lines for `const-cast` ("A `const` object may sit in read-only memory. The compiler may also assume it never changes.") and `wrong-delete` ("`new[]` stores a count that `delete` ignores. Pair `new[]` with `delete[]`.").
- app/content/exams/topic-1.9.json | e-ub-which | note | The multi widget lists code blocks as options; at 440 the five blocks fit with no clipping. Prose "None of them is optimised away" is fine, but it is an odd reassurance to a beginner. | Optional: drop it, since the question already asks about the standard, not the compiler.

## e-const-move, e-virtual-dtor

- app/content/exams/topic-1.9.json | e-const-move | note | The question is sound and each `why` names the slip. The explain says "A move constructor takes `Order&&`, which cannot bind to a const object". Correct. | None.
- app/content/exams/topic-1.9.json | e-virtual-dtor explain | note | "counter block" is the course term (l23, review-5); the standard and most references say "control block". A learner reading elsewhere will not recognise it. | Say "control block (the counter block)" once, here or in l23.
- app/content/exams/topic-1.9.json | e-virtual-dtor | note | Overlaps one option of review-5 `r5-virtual-dtor` (`shared`), as the report says. It is a recall of the same fact at difficulty 4. Acceptable as the brief specifies it. | None.

## e-code-clone-basket

Grading checked in the app toolchain with the exam file's own code (prelude, starter, solution and the 11 tests all identical to the brief scripts):

| variant | result |
| --- | --- |
| starter | 9 of 11 fail |
| solution | 0 of 11 fail |
| my alternative correct form (`if (market > limit) return 0.0;`, `unique_ptr<Basket>(new Basket)`, indexed loop) | 0 of 11 fail, passes |
| `market < limit` instead of `<=` | 1 fail (test at exactly 2.5) |
| `Limit::clone` returns a `Market` | 2 fail |
| `Limit::clone` and `Basket::clone` leak a block (kept in a global) | 3 fail by `leakCheck` |
| `Basket::clone` steals the children from the original (via `const_cast`) | 0 fail, not caught |

- app/content/exams/topic-1.9.json | e-code-clone-basket tests | warning | No test checks that the original is unchanged after `clone()`. A clone that moves the children out of `*this` passes all 11 tests. It is contrived (it needs a `const_cast`), but "the copy shares nothing" is the point of the item and the original's cost is never read after cloning. | Add a test with the 500 basket: setup as test 8 and `b.cost(2.0)` expecting 500. The count goes to 12 (limit is 15). Update `how` to "12 hidden tests".
- app/content/exams/topic-1.9.json | e-code-clone-basket starter | warning | Layout: comments on lines 4, 5 and 8 and the `clone()` on line 15 run past 70 columns. At 440, 1032 and 1376 the editor clips them (they scroll sideways); line 4 of the prose-duplicating comment is cut at "a cop" at 440. The editor also shows only 18 lines, so the TODO lines are below the fold at all three widths. | Wrap the two-line comment at about 60 columns (or drop it: the prose already says the same). Move the `// pounds to buy...` comment above line 8. Let `Market::clone` break across two lines.
- app/content/exams/topic-1.9.json | e-code-clone-basket prose | note | The prose and the first starter comment say the same thing twice ("clone() returns a copy of the same dynamic type"). | Keep it in the prose only.
- app/content/exams/topic-1.9.json | e-code-clone-basket pace | note | 600 s for this item is fair: a learner needs three small classes and one loop. The solution is about 20 lines. | None.

## Layout

`node tools/playthrough.mjs --exam topic-1.9 --shots ... --mobile --tablet --local-cdn ...`: all 30 items scored, passed, no errors. Screenshots looked at for items 6, 19, 20, 26 and 27 at 440; item 27 at 1032 and 1376.

- Items 6, 19, 20 and 26: no clipping at 440. Code blocks wrap or fit, the multi options stack, the numeric box is visible.
- Item 27 (code): see the starter warning above. Nothing else clips; the question navigator at 1032 and 1376 shows all 30 numbers on 8 rows with no overflow.

## Voice

`VOICE_BASE=<scratch> python3 docs/reviews/voice-scan.py --summary`: 0 explanations over three sentences; 632 sentences scanned, 0 over 20 words. No em-dashes, no exclamation marks in the file; no American spellings among the new items ("optimised", "behaviour", "unspecified" are British). No firm named. Money is not used.

## Balance

Skills over 30 items: cp-classes 6, cp-basics 4, cp-memory 4, cp-stl 4, cp-references 2, cp-build 2 (cpp: 22), and cx-numeric 2, cx-pricers 2, cx-perf 2, cx-testing 2 (8). Difficulty 6, 14, 7, 3 at 2, 3, 4, 5 (20%, 47%, 23%, 10%), inside the validator ramp.

- app/content/exams/topic-1.9.json | exam-level | warning | Levels 1 to 4 are fairly covered but level 1 is thin and level 5 now holds 5 of 22 cpp items (23%) against its 5 of 23 lessons. By skill: level 1 (types, control, functions, build) has `cp-basics` 3 and `cp-build` 2, level 2 has `cp-references` 2 and `cp-memory` 4 (one is level 5), level 3 has `cp-classes` 6 and level 4 has `cp-stl` 4. Level 5 items are all about move, virtual and UB; nothing tests l20 (rule of five) or l23 (own smart pointer) directly. | Acceptable for a first extension. For a later pass swap one `cp-classes` level 3 item for a rule-of-five item, or note in the brief that l20 and l23 are covered only through `e-code-credit-line` and `e-code-clone-basket`.
- app/content/exams/topic-1.9.json | minutes | note | 75 minutes for 30 items is 2.5 min an item, in line with 1.7 (70 for 30), 3.3 (75 for 30) and 1.8 (60 for 28, four code items). With seven code items, five of them difficulty 3 or 4, and two at difficulty 5, the code load is the highest in the 1.x exams (1.8 has 4). If the code items take 6 minutes each (42) and the 23 others 1.5 (35), the paper comes to 77 minutes, so 75 is tight but fair; 80 would be comfortable. | Keep 75; revisit after the first learners finish.
- app/content/exams/topic-1.9.json | ordering | note | The ramp order is right: e-const-move (2) at question 6; e-vector-growth, e-ub-which at 19 and 20; e-virtual-dtor and e-code-clone-basket at 26 and 27. | None.

## Summary of fixes wanted

1. Warning: add the libc++ no-exceptions note to e-vector-growth explain and l19.
2. Warning: add a "the original still holds its orders" test to e-code-clone-basket (12 tests).
3. Warning: shorten the long starter comment lines so they do not clip at 440, 1032 and 1376.
4. Warning: soften "cannot break the program" and add `byKey` for the two missed UB lines in e-ub-which.
