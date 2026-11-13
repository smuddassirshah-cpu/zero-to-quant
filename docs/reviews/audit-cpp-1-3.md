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

Filled after the WIP commit; see the section at the end.
