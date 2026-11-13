# Concept audit, round 3: cpp levels 1 to 3 (blind)

Scope: `app/content/courses/cpp/`, lessons l1 to l13, review-1 to review-3 and homework-1 to homework-3 (19 files, Stage 1, topic 1.9). Read blind: no earlier review, audit, report or concepts script of this course was opened before the ledger and the findings below were committed (WIP commit), except the permitted driver `docs/reports/cpp-L1-3-r2-zq.mjs`.

## Method

- Every string of the 19 files was read and judged: prose, canvases, keys, wrong options, slips, hints, feedback lines, explains, summaries, model answers and rubrics. The ledger has 2,532 rows.
- Every code-behaviour claim was compiled and run. The app's own compiler and grader (YoWASP clang 21.1.4, wasm32, libc++, `-O1`, hardening on, no exceptions) ran through the driver; g++ 13.3, clang++ 18.1, AddressSanitizer, UBSan and clang-tidy ran locally where the content quotes them. `docs/reports/cpp-L1-3-r3-concepts.py` holds 245 checks.
- All 47 code widgets: the solution passes and the starter fails under the app grader (94 gradings).
- Every `feedback.byKey` line was checked. For a `test-N` line that names a mistake, the mistaken submission was written, compiled and graded: it passes tests 1 to N−1 and fails test N in every case (64 graded submissions). Every `compile` line that quotes a message was checked against a submission that produces it (10 graded submissions). Slip values were recomputed by hand.
- Positional keys on console and table canvases (`lN`, `rN`, `cN`) were checked against the line each lands on.
- wasm32 differences noted and found stated correctly in the content: `sizeof(long)` and `sizeof(std::size_t)` are 4, a `std::vector` object is 12 bytes (24 on x86-64), `size() - 1` on an empty vector is 4,294,967,295.

## Verdict counts (ledger)

2,532 rows: 2,515 `correct`, 1 `wrong`, 11 `imprecise` (8 findings), 0 `misleading`, 5 `unverified`.

## Findings

Severity counts: 1 `wrong` (minor), 8 `imprecise` (all minor), 0 `misleading`. Serious: 0. Minor: 9.

1. `l13-templates.json` | `screens[4].feedback.byKey.l7` | wrong, minor | The line says "That is a library file's path, an `instantiation` note", but line 7 of the canvas is the caret line under the first error (`|            ~~~~~ ^ ~~~~~`). The first instantiation note is line 8 (`strict_weak_ordering_check.h:43:31: note: in instantiation ...`), which has no feedback of its own. | Console canvases number lines from 1 (`app/js/engine/canvas/console.js`, `l${k + 1}`); the canvas has the error on line 5, its source line on 6, the caret on 7 and the first note on 8. Check `l13.s4 every byKey line that says "instantiation note" sits on a note line` fails on `l7`. | Rename the key `l7` to `l8`, text unchanged: "That is a library file's path, an `instantiation` note. The cause is in the first `error:` line."

2. `l7-addresses.json` | `screens[3].explain.text` | imprecise, minor | "This browser build quietly writes to address 0 instead" is true only when the compiler cannot see that the pointer is null. For `bump(nullptr)`, the call on the canvas and in hidden test 5, the app build did not write quietly. | App compiler runs: `bump(nullptr)` with the unguarded body stopped with a trap (`unreachable`), and in the grader test 5 ended with "The program ended with exit status 3". With `int* volatile q = nullptr; bump(q);` the run printed that address 0 grew by 1 and exited 0. Both are in the concepts script (the two `NOTE finding 2` checks). Undefined behaviour, [expr.unary.op]. | Replace the last two sentences: "The guard matters: a desk build usually crashes on `*p` with `p` null. In this browser, one test run wrote to address 0 without complaint and another stopped with an error: undefined behaviour promises neither."

3. `l3-branches-and-loops.json` | `screens[7].widget.options[1].why` | imprecise, minor | The option "It prints 5" is explained as "That is Python, where the loop variable outlives the loop." Python does keep the variable, but `for i in range(5)` leaves it at 4, not 5. A learner with the Python habit picks 4 and is told nothing about Python; one who picks 5 is told that 5 is the Python answer. | CPython: after `for i in range(5): pass`, `i` is 4. A C++ `int i` declared before the loop holds 5 afterwards (run, `NOTE finding 3`). | `options[1].why`: "That is what an `int i` declared before the loop would hold: the test fails at 5. Here `i` ends with the `for`." `options[2].why`: "That is Python, where the loop variable outlives the loop and keeps its last value, 4. In C++ `i` ends with the `for`."

4. `l4-functions-and-headers.json` | `screens[4].hints[2]` and `screens[4].widget.accept` | imprecise, minor | The hint gives √365 as 19.105 and the accept line shows the product as 0.19105. A learner who rounds the 0.19105 they are shown to 4 decimal places gets 0.1911, which the key (0.191, tolerance 0.00006) rejects. The true value rounds down. | √365 = 19.104973 and 0.01 × √365 = 0.1910497, so 4 decimal places is 0.1910 (`NOTE finding 4`). | `hints[2]`: "$0.01 \times \sqrt{365} = 0.01 \times 19.10497$." `widget.accept`: "0.1910 (0.01 × √365 = 0.1910497)".

5. `l3-branches-and-loops.json` | `screens[6].explain.text` | imprecise, minor | "a normal build reads whatever memory is there" states one outcome of undefined behaviour as fact. The correct option on the same screen says "may read garbage". | [vector.access]: `v[n]` with `n >= size()` is undefined. | Second sentence: "This app's library checks `[]` and stops the program; in a normal build the read is undefined, and it may return whatever memory is there."

6. `homework-2.json` | `items[7].model`, part (a) | imprecise, minor | "A normal desk build silently reads whatever follows the buffer and adds it to the total" has the same fault as finding 5. The item's own rubric says "may silently add garbage". | [vector.access], as finding 5. The app's hardening message quoted in the same paragraph was run and is right. | "A normal desk build may silently read whatever follows the buffer and add it to the total."

7. `l10-invariants.json` | `summary.ideas[2]` and `screens[6].hints[2]` | imprecise, minor | "A `const` member can only get its value there" (the initialiser list). A default written at the member's declaration also gives a `const` member its value, and screens[5] of this lesson uses that syntax (`int qty_ = 0;`). | [class.mem] default member initialisers; `class Limit { const double max_ = 5e6; ... }` with a constructor that names no initialiser compiles (check `l10 summary: a const member can also take a default member initialiser`). | `summary.ideas[2]`: "Members are built in the initialiser list, before the constructor's body runs. A `const` member must get its value there or from a default written at its declaration; the body is too late." `screens[6].hints[2]`: "Members are built in the initialiser list, before the body. A `const` member cannot be assigned in the body, so give it its value in the list."

8. `l11-creation-destruction.json` | `screens[1].feedback.byKey.l5` | imprecise, minor | "That is the last line that uses `b`." Line 5 is `std::cout << "work\n";`, which does not use `b`; line 4 is the only line that names it. | The canvas listing: line 4 declares `b`, line 5 prints, line 6 closes the block. | "That is the last line inside the block. C++ does not track uses: `b` lives until its scope's closing brace."

9. `l12-operators.json` | `screens[4].prose` (first sentence) and `screens[8].prose` | imprecise, minor | "Python prints an object through `__repr__`." `print` calls `str()`, which uses `__str__` and falls back to `__repr__` only when the class has no `__str__`. `__str__` is the closer match for `operator<<`. | Python language reference, data model 3.3.1 (`object.__str__`, `object.__repr__`). | `screens[4].prose`, first sentence: "Python's `print` shows an object through `__str__`, or `__repr__` when the class has no `__str__`." `screens[8].prose`: change "`__repr__` becomes `operator<<`" to "`__str__` becomes `operator<<`".

## Unverified rows (not findings)

Five unsourced frequency or usage remarks are `unverified`: `l1` screens[7] explain (warnings "often point at a real bug"), `review-1` items[0] explain ("often means a forgotten step in a P&L"), `l6` screens[4] explain ("a feed handler would flag"), `l9` quiz[1] explain ("still the usual choice") and `l9` quiz[3] options[1] why ("are common"). None changes a definition, method or graded answer.

## Checked with particular care, and found correct

- Undefined against unspecified against implementation-defined: signed overflow is called undefined and every wrapped value is worded "in practice" or as a build's output (`l2` screens[1], quiz[2], `review-1` items[4]); the narrowing of 2,150,000,000 into `int` is described as silent narrowing, not as undefined (`l2` screens[5]); the order of the two calls in one `+` is said to be either (`homework-2` items[2]); a moved-from vector after move assignment is "valid, unspecified" (`l11` screens[7]).
- Output after undefined behaviour: `l7` screens[5] (101.25), `l7` quiz[0] (0), `l8` screens[5] and quiz[0], `review-2` items[3], `homework-2` items[5] and items[6] (2.9e-306) are each worded as what this build printed, and each was reproduced under the app compiler.
- Quoted diagnostics: every g++ line (13.3, including the 232-line count in `l1` screens[10]), every clang line with its line and column, the linker lines, the AddressSanitizer and LeakSanitizer reports (8,000 bytes in 1 object; 64 bytes in 2 allocations) and the libc++ template error in `l13` screens[4] (reproduced with the library's debug mode and clang's default error limit) match a run.
- Special members: `l11` screens[7] feedback for tests 5, 9, 10 and 12 each names the declaration set that fails first at that test; `l11` screens[10] test 8 is reached only by an explicitly defaulted copy beside a correct move.
- Exceptions: the content says `at()` throws `std::out_of_range`, which is the standard's rule; in the app the run stops and the grader names the exception type. `raises` tests accept `throw` and `std::abort()` alike (`l10` screens[3], run).

## Gates

- `node tools/validate.mjs`: 0 errors (4,537 warnings); `content/manifest.json` unchanged.
- `node tools/grade-all.mjs --file` on review-1, review-2, review-3, homework-1, homework-2, homework-3: 0 failures each, exit 0.
- `docs/reports/cpp-1-perf-numbers.py`: exit 0. `docs/reports/cpp-3-perf-numbers.py`: exit 0.
- `docs/reports/cpp-L1-3-r3-concepts.py`: 244 of 245 checks agree, exit 1. The one failing check is finding 1 and stays failing until the key is moved.

## Overlap table

Read after the WIP commit `68f44fa5`: `docs/reviews/review-1.9.md` (section "cpp", the lines for l1 to l13, review-1 to review-3 and homework-1 to homework-3, and its fix pass), `docs/reviews/audit-cpp-1-3.md` (round 1 audit, fix pass and fix-pass read) and `docs/reviews/audit-cpp-1-3-r2.md` (round 2 audit, fix pass and fix-pass read).

Conceptual findings of the earlier reads in this scope: 49. That is 15 from review-1.9, 17 from the round 1 audit, 1 from its fix-pass read, 14 new in the round 2 audit (its fifteenth was already counted as found by both) and 2 from the round 2 fix-pass read.

| | count |
|---|---|
| found by this audit only | 9 |
| found by the earlier reads only | 49 |
| found by both | 0 |

What the earlier reads said about the 9:

- A search of the three files for the paths and wording of findings 1 to 9 ("byKey.l7", "quietly", "That is Python", "19.105", "whatever memory", "whatever follows", "only get its value", "last line that uses", "`__repr__`") finds none of them as a finding.
- Finding 1 is not a fixer's slip. `git show ab4375ed:app/content/courses/cpp/l13-templates.json` has the same 25 console lines and the same key `l7` on the caret line: the key has been one line off since the lesson was written. review-1.9, round 1 and round 2 each checked this transcript against a compiler (line counts, the debug-mode notes) and none checked the keys against the lines.
- Finding 2 sits beside a row the round 1 fix-pass read passed: `l7` quiz[0] ("a test run with this app's compiler printed 0"), which is worded as one run and is right. The sentence in `screens[3]` makes the general claim and was not tested with the literal `bump(nullptr)` call.
- Finding 4 sits on a slip that review-1.9 corrected (3.66 to 3.65, its finding on `l4` screens[4]); its fix-pass note quotes "0.01√365 = 0.19105" without noticing that the value rounds to 0.1910 only at more digits.
- Earlier fixes re-read here as ledger rows and found correct include: `l13` screens[4] prose ("from a build with the library's debug checks on", reproduced), `l9` screens[2] ("a `throw` that some caller catches"), `l4` screens[5] `test-1`, `test-2` and `test-3` lines (each graded), `l12` screens[9] `test-1` (both named outputs reproduced), `l11` screens[7] tests 5, 9, 10 and 12 (each graded), `homework-2` items[5] prose (four ran, one stopped).

New `wrong` findings that no earlier read found: **1** (finding 1, minor). It is a feedback line attached to the wrong console line. The count of `wrong` about C++ itself in 2,532 ledger rows is zero.

Convergence rule: one new `wrong` in three levels is at the limit of "at most one", so this round meets the rule, subject to the fix-pass read of the nine fixes.

## Inbox bullets

Three bullets appended to `docs/BACKLOG-INBOX.md` under `Raised later (audit cpp):`: a validator report of positional `byKey` keys beside their lines; the node driver ending with status 0 and no output when its first compile carries extra flags; a `mutants` list on code widgets to keep the 74 graded submissions with the content.
