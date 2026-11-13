# Concept audit: cpp L1 to L3 (round 1, blind)

Date: 13 Nov 2026. Reader: Fable, blind to `docs/reviews/review-1.9.md` and the author reports until the ledger and findings were committed.

Scope: `app/content/courses/cpp/` lessons l1 to l13, `review-1` to `review-3`, `homework-1` to `homework-3` (levels 1 to 3 of `course.json`). Stage 1, topic 1.9, full ledger depth.

- Ledger: `docs/reports/audit-cpp-1-3-ledger.md`, 290 rows: 262 correct, 3 wrong, 14 imprecise, 0 misleading, 11 unverified.
- Script: `docs/reports/cpp-L1-3-concepts.py`, 123 native checks (g++ 13.3.0, clang 18.1.3, x86-64, libstdc++) and 10 more with `--wasm <pkgs>`, which compiles with the app's own YoWASP clang 21.1.4 and flags and runs under `node:wasi`.
- Findings: 17. By severity: 3 wrong, 14 imprecise, 0 misleading. By tag: 1 serious, 16 minor.

## Method

Every screen, quiz item, review item and homework item was read in full: prose, keys, each `wrong[]` value and option against its feedback, hints, explains, model answers and rubrics. Code-behaviour claims were compiled and run. Quoted compiler messages were reproduced: the g++ ones with g++ 13, the clang ones with clang 18, and the libc++ ones with the app compiler. Claims about "this browser build" were run with the app's compiler, flags and 8 MB stack. Anything else was judged from ISO C++17 (N4659), cited by section.

Where the desk and the app differ, the audit used both:

| fact | x86-64 desk | app (wasm32) |
|---|---|---|
| `sizeof(long)`, `sizeof(std::size_t)` | 8, 8 | 4, 4 |
| `sizeof(std::vector<double>)` | 24 | 12 |
| `size() - 1` on an empty vector | about 1.8 × 10¹⁹ | 4,294,967,295 |
| by-value parameter destroyed | after the call, at the end of the full expression | at the callee's `}` |
| null read, dangling read, mismatched or double `delete` | crash or sanitiser report | run on silently |
| `[]` past the end of a vector | silent read | stopped by libc++ hardening |

The particular-care list of the prompt, and what was found:

- Undefined, unspecified, implementation-defined. The course separates them correctly wherever it names them: signed overflow, null and dangling reads, mismatched and double `delete`, the out-of-range `[]` are all called undefined; the order of two calls in one `+` is called "either order" (unspecified). Three places state an outcome of undefined behaviour as a rule (findings 6, 11) or an implementation-defined point as fixed (finding 15).
- Integer overflow, division, conversions. All keys right. `-7 / 2`, `-9 / 4`, `-150 % 100`, `19.99 * 100`, `0.29 * 100`, the narrowing to −2,144,967,296 and both wrap values were run.
- Value and reference semantics, copies, lifetimes. Keys right. One "never copies" claim is too strong (finding 4); one feedback line names a wrong cause (finding 3).
- `const`, initialisation. No error found. Every quoted diagnostic was reproduced.
- "Always" claims about `sizeof`, evaluation order, performance. `sizeof` figures carry "in this app" once, on l2 screens[2]. The timing table on l5 screens[4] was re-measured with the app compiler and agrees within a factor of two.
- Exceptions. The app compiles `throw` and ends the run on an uncaught exception (`docs/AUTHORING.md`, `compare: "raises"`). The content only ever uses a throw as "the program stops", and says "`throw` or call `std::abort()`". No screen in levels 1 to 3 claims that a `catch` works. No finding.

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `homework-1.json` | `items[6].model` (last paragraph) and `items[6].rubric[5].text` | **wrong, serious** | The model answer says "Building with `-Wall -Wconversion` also flags the implicit conversions", and the rubric gives the point for "warning and sanitiser flags". No warning fires. A learner is told, and marked right for saying, that a compiler flag catches the two bugs of the item. | Run (`homework-1 h-port-note`): g++ 13.3.0 and clang 18.1.3 print nothing for the snippet with `-Wall -Wconversion`. Probe: nothing with `-Wall -Wextra -Wconversion -Wpedantic` either, and clang `-Weverything` reports only a missing prototype. Reason: `int` to `double` is value-preserving, so `-Wconversion` has nothing to say, and the overflow line contains no conversion at all. `-fsanitize=undefined` does report the overflow, and `clang-tidy -checks=bugprone-integer-division` flags line 7 (both run). | In `model`, replace "Building with `-Wall -Wconversion` also flags the implicit conversions. A sanitiser build (`-fsanitize=undefined`) reports the overflow at run time." with: "Compiler warnings do not help: `-Wall -Wextra -Wconversion` prints nothing for either line, because `int` to `double` loses nothing. A sanitiser build (`-fsanitize=undefined`) reports the overflow at run time, and clang-tidy's `bugprone-integer-division` check flags the division." Replace `rubric[5].text` with: "Names a way to catch each sooner: a unit test with large or odd values, a sanitiser build for the overflow, or clang-tidy for the division".

2. `l9-owning-memory.json` | `screens[3].hints[2].text` | **wrong, minor** | "Remove `delete book;`, or the object would be freed twice." With `auto book = std::make_unique<Book>();` the line `delete book;` does not compile, so nothing is freed twice. | Run (`l9 s3 hint 3`): clang "cannot delete expression of type 'std::unique_ptr<int>'"; g++ "type 'class std::unique_ptr<int>' argument given to 'delete', expected pointer". Std [expr.delete]/1: the operand must be a pointer or convert to one, and `unique_ptr` has no such conversion. | "With `make_unique`, both `return` lines free the `Book`. Delete the line `delete book;` as well: a `unique_ptr` cannot be passed to `delete`, so it would no longer compile."

3. `l11-creation-destruction.json` | `screens[7].feedback.byKey.test-10` | **wrong, minor** | "Test 10 moves into an existing buffer. A declared copy constructor stops the compiler writing the move assignment." Test 10 is `std::is_move_assignable_v<Buffer>`. With a declared copy constructor and no move assignment, that trait is true, because the implicit copy assignment accepts the rvalue. So the named mistake makes test 10 pass, not fail (it is test 12 that then fails, and its own line says so correctly). | Run (`l11 s7 feedback test-10`): `is_move_assignable_v<CopyCtorOnly>` is 1. Run (`test-12` case): with copy constructor, move constructor and copy assignment declared, the trait is still 1 and the "move" copies (prints 133). Std [class.copy.assign]: a move assignment is not declared implicitly when a copy constructor is user-declared; overload resolution then picks the copy assignment. | "Test 10 asks whether one `Buffer` can be move-assigned to another. Declare `Buffer& operator=(Buffer&&) = default;`."

4. `l11-creation-destruction.json` | `quiz[2].feedback.correct` | **imprecise, minor** | "Returning a local by value never copies it." True for `return grid;` with a movable type, which is the case shown. False as a rule. | Run (`l11 quiz2 feedback`): `T pick(bool up) { T a, b; return up ? a : b; }` makes 1 copy, although `T` has a move constructor. Std [class.copy.elision]/3: the move applies only when the operand is the name of a local object; a conditional expression is not one. A `const` local, or a type with no move constructor, is copied too. | "`return grid;` does not copy a movable local: it is built in place or moved."

5. `l13-templates.json` | `quiz[0].widget.options[1].why`, `quiz[0].widget.options[3].why`, `quiz[0].feedback.correct`, `quiz[0].feedback.generic`, `quiz[0].explain.text` | **imprecise, minor** | `<` on `std::string` is called "alphabetical order" five times. It compares character codes, so every capital sorts before every lower-case letter. The key (VOD) is right because the tickers are all capitals. | Run (`l13 quiz0 calls std::string <`): `"Zebra" < "apple"` and `"VOD" < "bp"` are both true. Std [string.operators], [char.traits.specializations.char]: lexicographic comparison of `char` values. | options[1].why: "`<` on strings compares character by character from the left, not by length. V comes after L." options[3].why: "`std::string` has `<`, which compares character by character, so the template compiles for it." feedback.correct: "V is the latest first letter, so VOD is the maximum." feedback.generic: "Not quite right. `<` on strings compares character by character from the left." explain.text: "For `std::string`, `best < x` compares character codes from the left. For all-capital tickers that is alphabetical order, so the maximum is VOD. Lower-case letters sort after every capital."

6. `l2-fixed-types.json` | `summary.ideas[2]` | **imprecise, minor** | "`int` stops at 2,147,483,647 and wraps silently". `screens[1].explain` and `quiz[2]` of the lesson say it is undefined and "in practice"; the summary, which is what is carried away, states the wrap as the rule. | Std [expr]/4: overflow of a signed type is undefined. The wrap value is what unoptimised two's-complement code does (run with `-fwrapv`). | "`int` stops at 2,147,483,647. Going past it is undefined behaviour, and in practice the value wraps silently; counts, volumes and pence totals belong in `long long`."

7. `l1-source-to-program.json` | `screens[3].prose`, `quiz[2].widget.options[2].why`, `quiz[2].explain.text` | **imprecise, minor** | "every statement ends with `;`" (three times, twice with "every"). A block, and an `if`, `for` or function body in braces, do not; the same lesson shows `int main() { ... }` and `if (signals = 0) { ... }` with no `;` after the brace. | Std [stmt.block], [stmt.select], [stmt.iter]. | screens[3].prose, third sentence: "`'\n'` ends the line, and a statement such as this one ends with `;`." options[2].why: "This statement has no `;` at its end, so it never ends." explain.text: "C++ needs the full name `std::cout`, and a statement like this one ends with `;`. `print` is a Python habit."

8. `l2-fixed-types.json` | `screens[3].prose`, `summary.ideas[0]` | **imprecise, minor** | "`auto` copies the type of the value on the right." Right for the values of level 1. From level 2 on it is a trap: `auto` never deduces a reference and drops a top-level `const`, so `auto a = r;` with `int& r` is a separate `int`. Nothing in levels 2 or 3 says so. | Run (`l2 s3 and summary`): `auto d = c;` with `const int c` is `int`; `auto a = r; a = 9;` leaves the referred object at 5. Std [dcl.spec.auto] with [temp.deduct.call]. | summary.ideas[0]: "Every variable has a fixed type, which sets its size (`sizeof`) and range. `auto` takes the type of the value on the right and makes a new copy; it never makes a reference by itself."

9. `l3-branches-and-loops.json` | `screens[3].feedback.byKey.test-2` | **imprecise, minor** | "0 − 1 wraps to about 4 billion." True in the app, where `std::size_t` is 32 bits; about 1.8 × 10¹⁹ on a 64-bit desk. | Run-wasm: 4,294,967,295. Run (`l3 quiz2`): the 64-bit maximum. | "The empty vector broke it. If you wrote `i < prices.size() - 1`, note that `size()` is unsigned: 0 − 1 wraps to its largest value, about 4 billion in this app. Start at 1 and test `i < prices.size()` instead."

10. `l4-functions-and-headers.json` | `summary.ideas[2]`; `l13-templates.json` | `quiz[2].explain.text` | **imprecise, minor** | Level 1 leaves the rule "Exactly one definition per program: a body in a header ... is a linker error". Level 3 then says "Put template definitions in the header" and never says why that does not break the level 1 rule. | Std [basic.def.odr]/6: an inline function or a template may be defined in more than one translation unit. Run (`l4 s7` inline check; `l13 quiz2 and l4 summary`): a template body in a header included by two `.cpp` files links cleanly. | l4 summary.ideas[2]: "One definition per program for an ordinary function: a body in a header included by two `.cpp` files is a linker error, unless it is marked `inline`." l13 quiz[2].explain.text: "An instantiation is written where the body and the type meet. Here they never meet, so the linker finds no `sum_of<double>`. Put template definitions in the header: unlike an ordinary function, a template body may appear in every `.cpp` that includes it."

11. `l7-addresses.json` | `summary.ideas[2]` | **imprecise, minor** | "A desk build crashes on a null read." The screens say "usually", and the trap line of the same summary says undefined behaviour "is not a crash you can rely on". | Std [expr.unary.op] with the definition of undefined behaviour, [defns.undefined]. | "This browser build is forgiving: null reads and dangling reads often print stale numbers. A desk build usually crashes on a null read. A dangling read may print a stale number there too; `-fsanitize=address` names the line."

12. `l7-addresses.json` | `screens[4].prose` | **imprecise, minor** | "C code passes a range as two pointers". The common C convention is a pointer and a count, which is what the C SDK on screens[9] of this lesson uses. The half-open pair is the C++ iterator idiom. | Std [iterator.requirements.general] (ranges `[i, j)`); the lesson's own `on_book(const Level* levels, int n)`. | First sentence: "A range can be passed as two pointers: `begin` at the first element, and `end` one *past* the last."

13. `l7-addresses.json` | `screens[9].widget.options[3].why` | **imprecise, minor** | "jumps 16 levels and runs past `levels + n`". It runs past only when `n` is not a multiple of 16; otherwise the loop ends cleanly and silently sums one level in sixteen. | Hand trace with `n = 32`: `p` takes `levels`, `levels + 16`, then equals `levels + 32` and stops. | "`++p` already moves one whole `Level`. Adding `sizeof(Level)`, 16, jumps 16 levels at a time: it skips most levels and can step over `levels + n`."

14. `l9-owning-memory.json` | `screens[6].prose` | **imprecise, minor** | "Every copy changes the count with an atomic instruction". Only in a threaded build. | libstdc++ `ext/atomicity.h`: `__atomic_add_dispatch` takes a plain increment when `__is_single_threaded()`; libc++ uses atomics only when built with threads, and the app's wasm32 build has none. | Third sentence: "Every copy updates the count, with an atomic instruction in a threaded program, which is why desks keep it out of hot paths."

15. `l9-owning-memory.json` | `screens[9].widget.lines[3].text` | **imprecise, minor** | "`hold`'s parameter dies at its `}`". Implementation-defined. True in the app; with g++ and clang on x86-64 the parameter lives to the end of the caller's statement. The printed order of the item is the same either way, so the key stands. | Std [expr.call]/4. Run (info line): `(hold(std::move(p)), std::cout << "same statement\n");` prints `same statement` before `close VOD` on x86-64 and after it in the app. | "`close VOD`: `hold`'s parameter was the only owner, and it dies when the call is over, so the destructor runs"

16. `l11-creation-destruction.json` | `screens[7].explain.text` (second sentence) | **imprecise, minor** | "A moved-from vector is empty; for most other types the standard promises only a valid, unspecified state." The canvas row and hidden test 12 move-assign. After move assignment the standard gives a vector the same "valid but unspecified" promise as any other type; it is empty in every implementation checked. | cppreference, `std::vector::operator=` (2): "other is in a valid but unspecified state afterwards"; std [lib.types.movedfrom]. Run and run-wasm: empty after both kinds of move. | "A vector that was moved from is empty in practice. For move assignment the standard promises only a valid, unspecified state, as it does for most other types."

17. `l12-operators.json` | `summary.ideas[2]` | **imprecise, minor** | "compare whole pence, never doubles". The trap taught on screens[6] is `==`. `<` on doubles is sound, and the course itself sorts and takes maxima of doubles (l13 `max_of`, review-3 `top_n`). | Run (`l12 summary`): `std::sort` on doubles orders them. IEEE 754 comparison is exact; only equality after rounding is unreliable. | "`<` must be strict and agree with `==`; test equality on whole pence, never on doubles. `operator<<` takes and returns `std::ostream&` so output chains."

## Unverified rows (not passes)

Industry or market remarks with no source:

- `l1` screens[10].prose: desks write pricers in C++ because compiled loops run many times faster than Python.
- `l2` screens[2].question: a day's volume across all UK shares can pass 3 billion.
- `l2` screens[9].prose: order books store prices as integer ticks.
- `l8` screens[10].explain: desks preallocate lattices and buffers.
- `l9` screens[6].prose and screens[10] why[shared]: desks keep `shared_ptr` out of hot paths.
- `l10` screens[9].explain: "a late fill on a cancelled order really happens, and must be caught, not booked". This one also reads oddly: a fill that crosses a pending cancel request is normally a valid trade and has to be booked. It needs a source or a narrower wording, for example "a fill reported after the cancel was confirmed".
- `l12` screens[9].explain: a matching engine keeps "exactly this order" in a sorted container.

Environment figures that could not be reproduced exactly:

- `l7` quiz[0].explain "a test run printed 1"; `homework-2` items[6].explain "it printed 2.93699e-306". The app build does print a stray value in each case (2.8974e-306 here for the second); the digits depend on memory layout.
- `l13` screens[4].prose "359 lines" (clang with libc++ on a desk; no such toolchain here).
- `l1` `widget.how` download size and compile times.

## Gates

- `node tools/validate.mjs`: 0 errors (4531 warnings); `content/manifest.json` unchanged.
- Number scripts: `docs/reports/cpp-1-perf-numbers.py` exit 0; `docs/reports/cpp-3-perf-numbers.py` exit 0. No number script exists for level 2.
- `node tools/grade-all.mjs --file` on review-1, review-2, review-3, homework-1, homework-2, homework-3: 0 failures each.
- `python3 docs/reports/cpp-L1-3-concepts.py --wasm <pkgs>`: exit 1, 133 checks, 6 failing lines, which are findings 1 (two lines, one per compiler), 2, 3, 4 and 5. Each failing check is tied to its sentence in the content, so it passes once the sentence is gone. Without `--wasm`: 123 checks, the same 6 fail.
- No playthrough was run: no content was changed.

## Overlap with the earlier read

Read after the WIP commit `48e7870b`: `docs/reviews/review-1.9.md`, section "cpp", the lines for l1 to l13, review-1 to review-3 and homework-1 to homework-3. Its fix pass had already been applied to the text this audit read.

Conceptual findings of the earlier review in this scope: 15. They are l1 screens[8] (Python habits that compile), l1 screens[1] (object file kept as a temporary), l3 screens[7] (braces in the pattern block), l3 screens[8] (fall-through warning), l4 screens[4] (slip value 3.66), l4 quiz (function name prints 1, not an address), l5 screens[8] and quiz (NRVO not guaranteed), l7 summary.ideas[2] (dangling read on a desk build), l11 screens[7] (declared special members suppress the assignments), l11 screens[7] explain (moved-from vector), l13 screens[6] (negative total), l13 screens[9] (constructor from a count), homework-1 items[4] (`double` index compiles), homework-2 items[2] (order of the two calls is unspecified), homework-3 items[1] (slip value 51.875). Not counted as conceptual: transcript wording, sentence counts, mutation gaps in hidden tests, and the test count in l10 screens[5] `how`.

| | count |
|---|---|
| found by this audit only | 17 |
| found by the earlier review only | 15 |
| found by both | 0 |

Reading of the table. All 15 earlier findings were fixed before this audit, and each fix was re-checked here as a ledger row and found correct, so a blind read of the fixed text could not find them again. The zero in "both" therefore does not measure this audit's miss rate; the 17 in "audit only" does measure what one second read left behind.

Two of the 17 sit on sentences the earlier fix pass wrote, and are counted as audit only because the review did not raise them:

- Finding 11 (`l7` summary.ideas[2]): the review replaced "A desk build crashes" for both reads with "A desk build crashes on a null read; ...". The certainty about the null read is what remains.
- Finding 16 (`l11` screens[7] explain): the sentence "A moved-from vector is empty; ..." is the review's own replacement text. It holds for move construction; the screen and test 12 also move-assign.

New `wrong` findings that no earlier read found: **3** (findings 1, 2 and 3). One is serious (finding 1). A search of `docs/reviews/review-1.9.md` and of the author reports `docs/reports/cpp-2.md` and `cpp-3.md` for "Wconversion", "freed twice" and "test-10" finds none of them.

Convergence rule: three new `wrong` in three levels is above the limit of one, so the course needs another blind audit after the fix pass.

## Fix pass

Fixer: Opus, 13 Nov 2026. Every replacement sentence was checked by a run of my own: g++ 13.3.0 and clang 18.1.3 on x86-64, and the app's YoWASP clang 21.1.4 (wasm32, libc++, `-O1`, `-fno-exceptions`, app flags) under `node:wasi`, driven as in `docs/reports/cpp-L1-3-concepts.py`. Content strings only; no key, `wrong[]` value, slip value, tolerance, starter, solution or hidden test changed.

| # | file and path | status | basis |
|---|---|---|---|
| 1 | homework-1 items[6].model, rubric[5].text | fixed | Compiled the item's code (as a function with a caller) with `-Wall -Wconversion`, `-Wall -Wextra -Wconversion -Wpedantic`, `+ -Wsign-conversion -Wfloat-conversion -Wdouble-promotion`, and `-O2 ... -Wstrict-overflow=5`: 0 warnings on both compilers; clang `-Weverything` gives only `-Wmissing-prototypes`. `-fsanitize=undefined` printed "signed integer overflow: 1500000000 + 1500000000 cannot be represented in type 'int'" at line 6; clang-tidy 18 `bugprone-integer-division` flagged line 8 ("result of integer division used in a floating point context"). The model now says warning flags print nothing, then names the sanitiser and clang-tidy; the rubric point names test, sanitiser or clang-tidy. |
| 2 | l9 screens[3].hints[2].text | fixed differently | App compiler on the starter with `make_unique` and the kept `delete book;`: "error: cannot delete expression of type 'unique_ptr<Book>'". New text: remove it too, because `delete` needs a raw pointer and the line does not compile ([expr.delete]/1). Same meaning as the audit's text, shorter wording. |
| 3 | l11 screens[7].feedback.byKey.test-10 | fixed differently | App compiler with the widget's tests: copy ctor only, and copy+move ctor+copy assign, both give test 9 = 1 and test 10 = 1 (test 12 gets 33, not 30, so test-12's line is right); a move-ctor-only class fails to compile at test 1; `operator=(Buffer&&) = delete` gives test 9 = 1, test 10 = 0. So the only way test 10 is the first failure is a deleted move assignment, and the line now names that and the `= default` fix. |
| 4 | l11 quiz[2].feedback.correct | fixed | Audit text. Run: `return up ? a : b;` made 1 copy; `return grid;` made 0 ([class.copy.elision]/3). |
| 5 | l13 quiz[0] options[1], options[3] why, feedback, explain | fixed | Run: `"Zebra" < "apple"` and `"VOD" < "bp"` are both true. Audit text, except the explain's last sentence says "In ASCII", since the order of letters is the execution character set's. |
| 6 | l2 summary.ideas[2] | fixed | [expr]/4; wrap value with `-fwrapv` in the script. Text says undefined, and "usually" wraps in practice. |
| 7 | l1 screens[3].prose, quiz[2] options[2].why, explain | fixed differently | A compound statement has no `;` ([stmt.block]). Prose and explain use the audit text; the option's why now says the missing `;` gives a compiler error (both compilers: "expected ';'"), instead of "it never ends". |
| 8 | l2 summary.ideas[0] | fixed differently | Run: `auto a = r;` with `int& r` is a separate `int`; `auto d = c;` with `const int c` is `int`. Shorter text: "makes a new, separate variable, never a reference". Prose screens[3] left: "the type of the value" is right, since a value has no reference type. |
| 9 | l3 screens[3].feedback.byKey.test-2 | fixed | wasm: `v.size() - 1` is 4,294,967,295; native: 2^64 − 1, about 1.8 × 10¹⁹. |
| 10 | l4 summary.ideas[2]; l13 quiz[2].explain | fixed | [basic.def.odr]/6. Runs: two `.cpp` files including an `inline` body link; a template body in a header included by two `.cpp` files links. |
| 11 | l7 summary.ideas[2] | fixed | "usually" added; matches screens and the trap line. |
| 12 | l7 screens[4].prose | fixed | Audit text; the lesson's own C SDK uses pointer and count. |
| 13 | l7 screens[9] options[3].why | fixed | Hand trace: n = 32 visits `levels`, `levels + 16`, stops; n = 20 steps from `levels + 16` to `levels + 32`, past the end. `sizeof(Level)` is 16 on both targets (script). |
| 14 | l9 screens[6].prose | fixed differently | Measured (g++ -O1, libstdc++, by-value call): 1.2 ns per `shared_ptr` copy single-threaded, 15 ns once a thread has run, 0.26 ns for a raw pointer. Text: the update is atomic in a threaded program, so a copy costs more than a raw pointer copy. The unsourced "why desks keep it out of hot paths" is gone (unverified row). |
| 15 | l9 screens[9].widget.lines[3].text | fixed | Audit text: "dies when the call is over" holds on both targets ([expr.call]/4 leaves the exact point to the implementation). Script info line: app destroys at `}`, x86-64 at the end of the full expression. Key unchanged. |
| 16 | l11 screens[7].explain.text | fixed differently | Moved-from vectors empty after construction and assignment, native and wasm (script). [lib.types.movedfrom] applies to move assignment, and the allocator-aware container table says nothing about `rv` after `a = rv`. Text: "empty in practice; after move assignment the standard promises only a valid, unspecified state" (one sentence, keeping the explain at three). |
| 17 | l12 summary.ideas[2] | fixed | Run: `std::sort` on doubles orders them; only `==` after rounding is the trap (l12 screens[6]). |

Unverified rows:

| row | status | basis |
|---|---|---|
| l1 screens[10].prose, pricers in C++ | fixed differently | Rewritten without the claim about desks: "C++ suits pricers: a compiled loop, such as a binomial tree, runs many times faster than the same loop in plain Python." Measured: a 3,000-step CRR tree took 0.235 s in CPython, 0.005 to 0.010 s in g++ -O1, about 0.01 s in the app build: 24 to 50 times. |
| l1 widget.how "about 26 MB", "10 to 15 s" | not applied | Size verified: gzip of bundle.js, llvm-resources.tar and llvm.core.wasm is 26.4 MB, as `docs/ENGINE-BACKLOG.md` states. The time is network-bound (a cold local compile took 2.9 s) and the same `how` sentence sits in about 70 widgets in all five levels: an engine-owned string for the orchestrator to raise, not a level 1 to 3 content fix. |
| l2 screens[2].question, 3 billion UK volume | fixed | Now a stated hypothetical: "Suppose a day's traded volume across a market comes to 3 billion shares." |
| l2 screens[9].prose, order books store ticks as integers | fixed | Tick part sourced: MiFID II tick size regime (Commission Delegated Regulation (EU) 2017/588, RTS 11, kept in UK law) makes share prices multiples of the tick. The book claim is now a possibility: "a program can store each price as an integer number of ticks". |
| l8 screens[10].explain, desks preallocate | fixed | Replaced by advice that follows from the screen: "So allocate a lattice or buffer once, before the loop, and reuse it." |
| l9 screens[6].prose, screens[10] why[shared] | fixed | See finding 14; why[shared] now says "every copy of a `shared_ptr` updates the count" (script: use_count 1, 3, 1). |
| l10 screens[9].explain, late fill | fixed | Now stated as the model's rule: "In this model a cancel is final: a later fill is an error to catch, not a trade to book." No claim about real gateways. |
| l12 screens[9].explain, matching engine container | fixed | Now: "Sorted by this `<`, the asks line up in the order price-time priority fills them." Script: B, C, A. |
| l7 quiz[0].explain "a test run printed 1" | fixed | App compiler, my run: the null read printed 0 and exited 0. Text: the read returns whatever `int` sits there; a test run with this app's compiler printed 0. Script check updated to expect 0. |
| homework-2 items[6].explain "2.93699e-306" | fixed | App compiler, my run and the audit's: 2.8974e-306. Text now quotes that value as one test run. New wasm check. |
| l13 screens[4].prose "359 lines" | fixed | App compiler on the screen's code: 235 lines of diagnostics at the app's `-ferror-limit=10`, 376 at `-ferror-limit=20`. Prose now "runs to hundreds of lines"; the console's "... 335 more lines ..." is now "... hundreds more lines ...". New wasm check (at least 200 lines). |

Script changes (`docs/reports/cpp-L1-3-concepts.py`): the six refuted-claim checks now report "[sentence no longer in the content]". New checks: `-Wall -Wextra -Wconversion` silent on the h-port-note code (both compilers), a deleted move assignment failing test 10 with test 9 passing, and under `--wasm` the null read printing 0, the h-realloc value 2.8974e-306, the template-error length, and the kept `delete book;` compile error. The l7 quiz0 wasm check now expects 0.

Gates: validator 0 errors, 4531 warnings, the same set as before the fix pass; `content/manifest.json` unchanged. `cpp-L1-3-concepts.py`: 126 checks, 0 failed; with `--wasm`: 139 checks, 0 failed. `cpp-1-perf-numbers.py` and `cpp-3-perf-numbers.py` exit 0. Voice scan 35: 0 over three sentences, 0 over 35 words. Playthrough with `--local-cdn`, desktop and `--mobile`, all passed: lessons l1, l2, l3, l4, l7, l8, l9, l10, l11, l12, l13; sets homework-1, homework-2 (l3 and l10 replayed after their last edit). No code widget's starter, solution or tests changed, so no re-grade was needed.

## Fix-pass read

Reader: fresh Fable reader, audit session 11. Diff read: `git diff 0f851e88~1 0f851e88 -- app/content/courses/cpp/` (13 files, 36 changed strings). The audit, its ledger and the fixer's notes were not read.

Tools used for the runs: g++ 13.3.0 (x86-64, libstdc++), clang++ 18.1.3, clang-tidy 18.1.3 (installed), and the app's compiler, YoWASP clang 21.1.4 (wasm32, libc++, `-O1`, the app's hardening flags, `-fno-exceptions`) under `node:wasi`. "wasm" below means that build. Every row was hand-checked; rows that state an output, a diagnostic or a test result were also compiled and run.

Verdicts: 35 correct, 1 imprecise (minor), 0 wrong, 0 misleading, 0 unverified.

| # | File | JSON path | New text (short) | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | homework-1 | items.6.model | "Warning flags do not help: g++ and clang print nothing ... even with `-Wall -Wextra -Wconversion`. A sanitiser build (`-fsanitize=undefined`) reports the overflow at run time, and clang-tidy's `bugprone-integer-division` check flags the division." | correct | Run. The prompt's snippet (with `std::vector<int> fills`, `int n_fills`) under `-Wall -Wextra -Wconversion`: g++ 13, clang 18 and wasm clang 21 all print nothing. `g++ -fsanitize=undefined`: "runtime error: signed integer overflow: 1500000000 + 1500000000 cannot be represented in type 'int'". `clang-tidy -checks='-*,bugprone-integer-division'`: "result of integer division used in a floating point context; possible loss of precision [bugprone-integer-division]" on the `avg` line. The check is not in clang-tidy's default set (a default run prints nothing); the text names the check, so it is right. Fix code run: 10000002 gives 2500000.5; both "would not help" forms give 2500000. |
| 2 | homework-1 | items.6.rubric.5.text | "a unit test with large or odd values, a sanitiser build for the overflow, or clang-tidy for the division" | correct | Agrees with row 1 and with the model answer; each tool is paired with the fault it was run against. |
| 3 | homework-2 | items.6.explain.text | "with this app's compiler a test run printed 2.8974e-306, and AddressSanitizer reports heap-use-after-free on line 4" | correct | Run. wasm printed `2.8974e-306`. `g++ -fsanitize=address`: "heap-use-after-free", READ at the `std::cout << first` line, which is line 4 of the shown snippet. Worded as one build's output, and the keyed option says "Anything". |
| 4 | l1 | screens.3.prose | "a statement like this one ends with `;`" | correct | True of an expression statement; no longer claims every statement (a compound statement or `if` does not end in `;`). |
| 5 | l1 | screens.10.prose | "C++ suits pricers: a compiled loop, such as a binomial tree, runs many times faster than the same loop in plain Python." | correct | Run: a 2,000-step binomial tree took 0.0009 s in g++ `-O1` and 0.18 s in CPython, about 200 times. "232 lines" (unchanged) recounted: g++ 13 prints 232. |
| 6 | l1 | quiz.2.widget.options.2.why | "A statement like this one must end with `;`. Without it, the compiler reports an error." | correct | Run: g++ "expected ';' before 'return'", clang and wasm "expected ';' after expression". The keyed line compiles on all three; the other two options fail as their `why` says. |
| 7 | l1 | quiz.2.explain.text | "C++ needs the full name `std::cout`, and a statement like this one ends with `;`." | correct | As rows 4 and 6; `cout` alone: "use of undeclared identifier 'cout'". |
| 8 | l10 | screens.9.explain.text | "In this model a cancel is final: a later fill is an error to catch, not a trade to book." | correct | Agrees with the prose ("A filled or cancelled order accepts nothing more") and with hidden test 7 (cancel, then fill, must raise). Claims nothing about real gateways. |
| 9 | l11 | screens.7.feedback.byKey.test-10 | "Test 10 asks whether one `Buffer` can be move-assigned to another, and a deleted move assignment says no. Write `Buffer& operator=(Buffer&&) = default;`." | correct | Run, 11 submissions against the 12 hidden tests on g++, clang and wasm (same result on all three). Move assignment `= delete` with the other three defaulted: passes tests 1 to 9, first failure is test 10. Move assignment simply omitted: test 10 passes (the copy assignment serves) and the first failure is test 12, whose own line covers it. Copy and move constructors only: first failure is test 9. Copy constructor only: test 5. Nothing declared: all pass. Test 10 is `std::is_move_assignable_v<Buffer>`, so "asks whether" is exact. See note A. |
| 10 | l11 | screens.7.explain.text | "A moved-from vector is empty in practice; after move assignment the standard promises only a valid, unspecified state." | correct | "Unspecified" is the right word: [lib.types.movedfrom] says "valid but unspecified state". Run: `size()` is 0 after move construction and after move assignment on libstdc++ and on the app's libc++. Agrees with tests 5 and 12, which expect 0. |
| 11 | l11 | quiz.2.feedback.correct | "`return grid;` does not copy a movable local: it is built in place or moved." | correct | [class.copy.elision]: named return value optimisation, else an implicit move. Run with a counting `Lattice`: 0 copies and 0 moves normally; 0 copies and 1 move with `-fno-elide-constructors` (g++ and clang); 0 and 0 on wasm. Key 0 agrees. |
| 12 | l12 | screens.9.explain.text | "Sorted by this `<`, the asks line up in the order price-time priority fills them." | correct | Run: the solution sorts the example book to B, C, A, the caption's order. Lowest price first, then earliest time, is the prose's definition. |
| 13 | l12 | summary.ideas.2 | "test equality on whole pence, never on doubles" | correct | Integer comparison is exact; `==` on computed doubles is not reliable (the l2 trap: `19.99 * 100` converts to 1998, run). |
| 14 | l13 | screens.4.prose | "The real message runs to hundreds of lines" | correct | Run: the screen's program on the app's compiler prints 235 lines at the app's error limit of 10 and 376 at clang's default limit of 20, the command the canvas shows. |
| 15 | l13 | screens.4.canvas.params.lines.22 | "... hundreds more lines ..." | correct | As row 14: about 350 of the 376 lines follow those shown. |
| 16 | l13 | quiz.0.widget.options.1.why | "`<` on strings compares character by character from the left, not by length. V comes after L." | correct | [string.compare] is lexicographic via `char_traits::compare`. Run: `"AZ" < "AZN"` is true only because a prefix sorts first; `max_of` returns VOD. |
| 17 | l13 | quiz.0.widget.options.3.why | "`std::string` has `<`, which compares character by character, so the template compiles for it." | correct | Run: compiles and returns VOD on g++ and wasm. |
| 18 | l13 | quiz.0.feedback.correct | "V is the latest first letter, so VOD is the maximum." | correct | First letters B, A, V, L; V (86) is the largest code. |
| 19 | l13 | quiz.0.feedback.generic | "`<` on strings compares character by character from the left." | correct | As row 16. |
| 20 | l13 | quiz.0.explain.text | "compares character codes from the left. For all-capital tickers that is alphabetical order, so the maximum is VOD. In ASCII every capital sorts before every lower-case letter." | correct | Run: 'A' 65, 'Z' 90, 'a' 97, 'z' 122; `"Z" < "a"` and `"VOD" < "Vod"` are both true. |
| 21 | l13 | quiz.2.explain.text | "Put template definitions in the header: unlike an ordinary function, a template body may appear in every `.cpp` that includes it." | correct | [basic.def.odr] allows one definition of a template per translation unit. Run: the quiz's layout gives "undefined reference to `double sum_of<double>(...)`"; a template body in a header included by two `.cpp` files links and runs; an ordinary function body there gives "multiple definition of `twice(double)`". |
| 22 | l2 | screens.2.question | "Suppose a day's traded volume across a market comes to 3 billion shares." | correct | A supposition, no longer a claim about UK volume. 3,000,000,000 exceeds 2,147,483,647 and fits `long long`; key `r1` and the hints agree. |
| 23 | l2 | screens.9.prose | "Exchanges quote prices in whole ticks, so a program can store each price as an integer number of ticks. Integers add and compare exactly." | correct | Prices are multiples of the tick size, so a tick count is an integer. Agrees with the `long long` pence signature and the 1e-9 tests. |
| 24 | l2 | summary.ideas.0 | "`auto` takes the type of the value on the right and makes a new, separate variable, never a reference." | correct | [dcl.type.auto.deduct]: plain `auto` deduces as a by-value template parameter. Run: `auto a = r;` from an `int&` is `int`, not a reference; writing `a` leaves `x` at 5. |
| 25 | l2 | summary.ideas.2 | "`int` stops at 2,147,483,647. Going past it is undefined behaviour, and in practice the value usually wraps silently" | correct | Signed overflow is undefined ([expr.pre]); the right term. Run: `INT_MAX + 1` printed −2147483648 on g++ and wasm, and UBSan reports it. "In practice ... usually" is the right strength. |
| 26 | l3 | screens.3.feedback.byKey.test-2 | "With `i < prices.size() - 1`, 0 − 1 wraps, since `size()` is unsigned: about 4 billion here, 1.8 × 10¹⁹ on a 64-bit desk." | imprecise (minor) | The numbers are right. Run: on an empty vector `size() - 1` is 4294967295 on wasm (`size_t` 4 bytes) and 18446744073709551615 on x86-64. Unsigned wrap is defined, and the text does not call it undefined. The named mistake passes test 1 and stops on test 2 (hardened `vector[]` trap), so the key is reachable. The fault is the word: "a 64-bit desk" is not a term the learner has met by lesson 3 ("desk build" first appears in l7, and "desk" elsewhere means a trading desk). See finding 1. |
| 27 | l4 | summary.ideas.2 | "One definition per program for an ordinary function: a body in a header included by two `.cpp` files is a linker error, unless it is marked `inline`." | correct | [basic.def.odr]. Run: "multiple definition of `twice(double)`" without `inline`; links and runs with it. The trap's `#pragma once` claim (unchanged) also reproduced. |
| 28 | l7 | screens.4.prose | "A range can be passed as two pointers" | correct | Matches the prelude's `max_via_pointer(v.data(), v.data() + v.size())`. No longer attributes the idiom to C code only. |
| 29 | l7 | screens.9.widget.options.3.why | "Adding `sizeof(Level)`, 16, jumps 16 levels at a time: it skips most levels and can step over `levels + n`." | correct | Run: `sizeof(Level)` is 16 on x86-64 and on wasm. With n = 33 a 16-step walk visits 3 of 33 levels (total 51, not 561), and with `!=` it passes `levels + 33` without equalling it. Agrees with the byKey line. |
| 30 | l7 | summary.ideas.2 | "A desk build usually crashes on a null read." | correct | Run: g++ at `-O0` and `-O1` dies with SIGSEGV; clang 18 at `-O1` on the same Linux machine printed a stray number and exited 0. So "usually" is needed and right. |
| 31 | l7 | quiz.0.explain.text | "In this browser, address 0 is ordinary memory, so the read returns whatever `int` sits there; a test run with this app's compiler printed 0. Neither is a promise" | correct | Run: wasm printed `0` and exited 0; g++ gives `Segmentation fault`; ASan prints "SEGV on unknown address 0x000000000000". Worded as what one build printed, with "Neither is a promise", and the key names undefined behaviour. |
| 32 | l8 | screens.10.explain.text | "So allocate a lattice or buffer once, before the loop, and reuse it." | correct | Follows from the two sentences before it and matches the keyed option. Advice, with no claim about what desks do. |
| 33 | l9 | screens.3.hints.2.text | "Remove `delete book;` too: `delete` needs a raw pointer, so with a `unique_ptr` that line does not compile." | correct | Run: the starter with only the `make_unique` line changed. g++: "type 'class std::unique_ptr<Book, ...>' argument given to 'delete', expected pointer". clang and wasm: "cannot delete expression of type 'unique_ptr<Book>'". [expr.delete] needs a pointer or a class with a non-explicit conversion to one; `unique_ptr` has none. |
| 34 | l9 | screens.6.prose | "Every copy updates the count, atomically in a threaded program. So a copy costs more than copying a raw pointer." | correct | [util.smartptr.shared]: use-count changes must not race. libstdc++ skips the atomic instruction in a single-threaded process, so "in a threaded program" is exact. Run: `use_count()` printed 1, 3, 1, the key and the explain line. |
| 35 | l9 | screens.9.widget.lines.3.text | "`hold`'s parameter was the only owner, and it dies when the call is over, so the destructor runs" | correct | Run: g++, clang and wasm each print open VOD, opened, hold 100, close VOD, 1 after hold. "When the call is over" is true under both choices [expr.call] allows for a parameter's end (it is implementation-defined whether at return or at the end of the full expression), so the text claims no more than the standard does. |
| 36 | l9 | screens.10.widget.options.2.why | "every copy of a `shared_ptr` updates the count" | correct | As row 34; the "hot path" claim is gone. |

Terms. Undefined behaviour is named for signed overflow (rows 1, 25), the null read (row 31) and, by the keyed option, the dangling reference (row 3): all correct. "Unspecified" is used once, for the moved-from state (row 10): correct. No changed string uses "implementation-defined"; the one place it applies (row 35) is worded so as not to need it. Unsigned wrap (row 26) is not called undefined: correct. Every output shown after undefined behaviour (rows 3, 25, 31) is worded as what a run or this build printed.

### Findings

1. **minor, imprecise** `l3-branches-and-loops.json` `screens.3.feedback.byKey.test-2`: "a 64-bit desk" uses "desk" for a machine four lessons before the course introduces "desk build". Paste-ready replacement (numbers re-run: 4294967295 on the app's build, 18446744073709551615 on x86-64; longest sentence 27 words):

   `The empty vector broke it. With \`i < prices.size() - 1\`, 0 − 1 wraps, since \`size()\` is unsigned: about 4 billion here, 1.8 × 10¹⁹ on a 64-bit machine. Start at 1 and test \`i < prices.size()\` instead.`

### Notes (no change asked for)

- A. l11 test 10: one other submission reaches this line. A move assignment written as `= default` but placed under `private:` also passes tests 1 to 9 and fails test 10 (run on all three compilers). The line then names the wrong cause, though its remedy still points at the right member. It is a contrived submission, so the row stays correct.
- B. Row 1 holds for the declarations the prompt implies (`int` fills, `int n_fills`). If `n_fills` were `fills.size()`, `-Wconversion` does speak (run: g++ "conversion from 'long unsigned int' to 'double' may change value", clang `-Wsign-conversion`), but about the conversion and not about the lost fraction or the overflow.
