# Concept audit, round 2 (blind): cpp L1 to L3

Course `cpp` (C++ Foundations, topic 1.9, Stage 1). Files: l1 to l13, review-1 to review-3, homework-1 to homework-3.
Ledger: `docs/reports/audit-cpp-1-3-r2-ledger.md`. Script: `docs/reports/cpp-L1-3-r2-concepts.py`, with its driver `docs/reports/cpp-L1-3-r2-zq.mjs`.
Auditor: Fable, round 2, fresh reader. Audited at `271eaf06`.

## Result in one paragraph

No `serious` finding. 15 findings, all `minor`: 3 `wrong` (findings 1, 2 and 12), 12 `imprecise`, 0 `misleading`. The three `wrong` are a prose line that is false for one of its five snippets, and two feedback lines whose diagnosis is false for every submission that can reach them. Six of the twelve `imprecise` are feedback lines that name a mistake which the grader sends to another test or key. Every other claim about what code prints, what compiles and what a compiler says held when it was compiled and run.

## Method

- Every string of the 19 files read in full, then every code-behaviour claim compiled and run. 369 checks: 323 under the app's own compiler (YoWASP clang 21.1.4, wasm32, libc++, `-O1`, the app's flags, harness, exception runtime and WASI shim), 23 on local g++ 13.3 and clang 18.1 (x86-64 Linux), 23 in CPython.
- All 47 code widgets: the solution passes every hidden test and the starter fails (94 of the checks).
- Every `feedback.byKey` `test-N` line: a submission with the named mistake was written and graded, and the key the grader gives was compared with N. Lines that name no mistake (they restate what the test expects) were checked against the starter. Every slip value was recomputed from its named mistake.
- Every compiler message quoted in a canvas or a `why` was reproduced with the compiler and flags it names.
- Wasm32 differences were looked for at each `sizeof` and size claim. None is misstated: the content gives 12 and 24 bytes for a vector object, and "about 4 billion here, 1.8 × 10¹⁹ on a 64-bit machine" for `size() - 1`.
- Undefined behaviour: every sentence that says what a run printed is worded as what one build printed. Runs reproduced them: the dangling read printed 101.25, the null read printed 0, the mismatched and the double `delete` ran silently, the 16 MB local array stopped with "memory access out of bounds".

### Blind rule: one slip, stated plainly

To find the helper that calls the wasm compiler I read lines 120 to 170 of `docs/reports/cpp-L1-3-concepts.py`. That window also showed nine check lines for l1, which name no finding. A `grep` for `wasm` in the same file printed four more check lines. One of them says a by-value parameter outlives the call to the end of the full expression. Finding 5 below is on that subject, so it is not an independent discovery and I count it as found by an earlier read whatever the earlier files say. Nothing else of the earlier reads was opened before the commit of this file and the ledger.

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `homework-2.json` | `items[5].prose` | wrong, minor | "Each snippet ran in this browser build without stopping." One of the five did not. | Check `h2.i5.at`: `std::vector<double> v(3); double y = v.at(5);` ends the run with `terminate called after throwing an instance of 'std::out_of_range'`, exit status 134. The four others ran to the end (checks `h2.i5.null`, `.mismatch`, `.twice`, `.zero`). The item's own `why` for that option says `at` throws. | Replace the prose with: `This browser build stopped only one of these five snippets, with a reported error.`

2. `l13-templates.json` | `screens[2].feedback.byKey.test-2` | wrong, minor | "If you got 0, the total was an `int`: declare it as `T`." An `int` total can never give 0 here: it does not compile. | Check `l13.s2.fb-test-2`: with `int total = 0;` the hidden `std::string` test instantiates `int += std::string`, and the grader's key is `compile`, whose line says nothing about the total's type. A `double` total fails the same way. | Delete `byKey.test-2`. Replace `byKey.compile` with: `The compiler stopped. Check that `template <typename T>` comes right before the function and that it returns `T`. A total declared `int` or `double` cannot hold a `std::string`: declare it as `T`.`

3. `l13-templates.json` | `screens[7].widget.wrong[0]` (`two`) | imprecise, minor | The slip value is 123, with tolerance 0, and its line says "You used two places". Two places give 123.45 by the arithmetic of the hint. | 1.2345 × 10² = 123.45 (check `l13.s7.slip-two`). 123 is right only for a learner who also drops the .45 to make whole units. One who types 123.45 gets the generic line. | Set `"value": 123.45, "tol": { "abs": 0.5 }`, which takes 123.45 and a truncated 123. The band, 122.95 to 123.95, is clear of the key 12345 and of the slip 1.2345.

4. `l9-owning-memory.json` | `screens[2].explain.text` | imprecise, minor | "its destructor runs at every exit, early returns and `throw`s included". True only when the exception is caught. | C++17 [except.handle]/9: with no matching handler, `std::terminate` is called and whether the stack is unwound is implementation-defined. In this app a `throw` ends the run at once and no destructor runs (check `l9.s2.throw-runs-destructor`: the guard's destructor printed nothing). [except.ctor]/1 gives the guarantee for a caught exception. | `` `notional` owns its heap buffer, and its destructor runs at every exit: each `return`, and a `throw` that some caller catches. The `delete[]` line is gone, so it cannot be forgotten. That is RAII: lifetime of the owner equals lifetime of the resource. ``

5. `l5-value-or-reference.json` | `screens[0].hints[2]`, `screens[0].explain.text`, `screens[6].explain.text`; `l9-owning-memory.json` | `screens[9].hints[2]`, `screens[9].explain.text`; `homework-2.json` | `items[7].model`, part (c) | imprecise, minor | A by-value parameter is said to be destroyed "at the function's closing brace". The standard leaves the moment to the implementation, and for the vector of l5 it is not what this build does. | C++17 [expr.call]/4: it is implementation-defined whether a parameter's lifetime ends when the function returns or at the end of the enclosing full-expression. On this build, and on g++ and clang desk builds, a copied class parameter is destroyed at the end of the calling full-expression (checks `l5.s0.param-lifetime` and `-desk`: `copy body rest-of-expression destroyed`; check `l5.s0.vector-param`: the same for a `std::vector` passed by value in the app). The sentence is true only where the callee destroys its parameters, as the Microsoft ABI does. The `unique_ptr` parameter of l9 is destroyed in the callee on this build (check `l9.s9.param-lifetime`), not on a desk g++ build. No output shown on these screens changes. The order line of l9 `screens[9]` already says "when the call is over". | l5 `screens[0].hints[2]`: `` `costs` is built as a copy of `mine`. `push_back` grows the copy, which is destroyed when the call is over. `mine` keeps its two prices. `` l5 `screens[0].explain.text`: `` `costs` is a separate vector, copied from `mine` when the call starts. `push_back` grows that copy, and the copy is destroyed when the call is over. So `mine.size()` is still 2. `` l5 `screens[6].explain.text`: `` `normalise` divided its own copy, `{0.2, 0.3, 0.5}`, and that copy died when the call was over. The caller's `w` is untouched, so `w[0]` prints 2. The compiler cannot warn you: copying is legal. `` l9 `screens[9].hints[2]`: `` Created, owned by `main`, moved into `hold`, destroyed when the call to `hold` is over, and `main`'s `p` is left null. `` l9 `screens[9].explain.text`: `` After `std::move(p)`, `hold`'s parameter is the only owner, so the position closes when the call is over, before `main` carries on. `main`'s `p` is null and prints 1. A test run printed exactly these five lines. `` homework-2 model (c), second sentence: `` The fee is added to the copy, which dies when the call is over, so the caller sees nothing. ``

6. `l13-templates.json` | `screens[4].canvas.params.lines` (and `prose`) | imprecise, minor | The transcript is headed `$ clang++ -std=c++17 main.cpp`, but its lines 7 to 12 (`strict_weak_ordering_check.h:43:31`, `sort.h:939:8`) appear only when libc++'s debug checks are on. | Check `l13.s4.sort-error` fails: built as the command says, and in the app, the notes after the error run through `sift_down.h:47:32`, `make_heap.h:39:12`, `partial_sort.h` and `sort.h:934:10`. Check `l13.s4.sort-error-debug` holds: with `-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG` every quoted line appears, in 364 lines. The two lines the learner taps, the first `error:` and the `main.cpp:11:10` note, exist in every build (check `l13.s4.two-lines`). | Last sentence of the prose: `The real message runs to hundreds of lines; here are the first lines, from a build with the library's debug checks on.`

7. `l13-templates.json` | `screens[9].explain.text` | imprecise, minor | "level 4's containers do it in constant time". No level 4 file teaches a container that removes its front in constant time. | Check `l13.s9.deque`: l14 to l18, review-4 and homework-4 never name `std::deque`, `std::queue` or `pop_front` (a text search only; level 4 was not read). Level 4's sequence container is `std::vector`, whose front erase is linear ([vector.modifiers]). `std::deque::pop_front` is constant ([deque.modifiers]). | Last sentence: `Erasing the front shifts $n$ values, which is fine for small windows; a `std::deque` removes its front in constant time.`

8. `l3-branches-and-loops.json` | `screens[3].feedback.byKey.error`; `homework-1.json` | `items[1].feedback.byKey.error` | imprecise, minor | Both lines begin "The program stopped". The grader never gives the key `error` for a program that stops, so neither line is shown. | `cpp-grade.js` line 736: the key is `error` only when the runner itself fails; a test whose run stops is a failed row, key `test-N`. Check `l3.s3.fb-error`: the `<=` loop stops on test 1 with "vector[] index out of bounds" and the key is `test-1`, which has no line. In homework-1 the same advice is already in `test-6` (check `h1.i1.fb-test-6`). | l3: rename the key `error` to `test-1`, with: `Test 1 has five closes. If the program stopped with index out of bounds, your loop read past the last close: test `i < prices.size()`, not `<=`.` homework-1: delete `byKey.error`.

9. `l1-source-to-program.json` | `screens[3].feedback.byKey.test-2` | imprecise, minor | "Check the comma, the capital H and the `'\n'` at the end." A wrong comma or capital never reaches test 2. | Check `l1.s3.comma`: `Hello market` fails test 1, key `test-1`. Only the line end, or a space before it, passes test 1 and fails the exact test 2 (checks `l1.s3.fb-test-2`, `l1.s3.trailing-space`). | `The words match but not every character. Check that the line ends with `'\n'`, with no space before it.`

10. `l1-source-to-program.json` | `screens[4].feedback.byKey.test-3` | imprecise, minor | "do not fix the decimal places" sits on test 3, but fixed decimals fail test 1. | Check `l1.s4.fb-test-3`: `std::fixed << std::setprecision(2)` prints `Price: 72.50`, key `test-1`. | Rename the key to `test-1`, with: `Test 1 expects `Ticker: VOD`, then `Price: 72.5`. If your price shows as `72.50`, leave the number as `std::cout` prints it.`

11. `l3-branches-and-loops.json` | `screens[4].feedback.byKey.test-6` and `.test-4` | imprecise, minor | "If you got 0.4, your peak stayed at 100" and "If you got −0.1, subtract the other way": both mistakes fail test 1 first. | Checks `l3.s4.fb-test-6` and `.fb-test-4`: a peak stuck at the first close gives 0.12 on test 1; `(p - peak) / peak` gives −0.2 on test 1 (or 0, when the worst is kept with `>`). | `test-1`: `Test 1 should give 0.2: from 110 to 88. If you got 0.12, your peak stayed at 100. If you got −0.2 or 0, subtract the other way: `peak - p`.` `test-6`: `In `100, 80, 120, 60` the worst fall is from the new peak 120 down to 60: 0.5.` `test-4`: `A fall from 100 to 90 is 0.1, a positive fraction.`

12. `l4-functions-and-headers.json` | `screens[5].feedback.byKey.test-2` | wrong, minor | "If the program stopped, your loop read `prices[i - 1]` with `i` at 0." A loop with `i` at 0 stops on test 1, so whenever this line is shown its diagnosis is false. The loop that does stop later, `i < prices.size() - 1`, stops on test 3, which has no line. | Checks `l4.s5.fb-test-2` (key `test-1`, "vector[] index out of bounds" on test 1) and `l4.s5.minus-one-bound` (key `test-3`). A program that passes test 1 and stops on test 2 read some other index, for example `prices[1]` in a `do`-`while` from 1. | `test-2`: `One close has no day before it, so the list must be empty.` `test-1`: `From 110 to 99 is (99 − 110) / 110 = −0.1. Divide by yesterday's close, not today's. If the program stopped, your loop read `prices[i - 1]` with `i` at 0.` Add `test-3`: `The empty vector broke it. `prices.size() - 1` wraps when the size is 0: start at 1 and test `i < prices.size()`.`

13. `l7-addresses.json` | `screens[4].feedback.byKey.test-5` and `.test-2` | imprecise, minor | `test-5` says "stop before `end`", but a loop that reads `*end` passes test 5 and fails test 2, where the line blames a best that starts at 0. | Check `l7.s4.fb-test-5`: with `p <= end` test 5 reads `xs[3]`, which is 2, and still returns 4; test 2 reads one past the vector's buffer and returned 1.285 × 10⁻³⁰⁹ in this run, key `test-2`. | `test-2`: `All three values are negative. If you got 0, your best started at 0: start from `*begin`. If you got another number, your loop read `*end`: stop at `p != end`.` `test-5`: `The range is `xs[1]` and `xs[2]`, so the answer is 4. A 9 means the walk began before `begin`.`

14. `l12-operators.json` | `screens[9].feedback.byKey.test-4` | imprecise, minor | "Compare prices before times" sits on test 4, but comparing time first fails test 1. | Check `l12.s9.fb-test-4`: `std::tie(a.time, a.price) < std::tie(b.time, b.price)` gives C, A, B on test 1, key `test-1`. | `test-1`: `Test 1 expects B, C, A. B has the lowest price; C and A tie on price, and C arrived first. If you got C, A, B, you compared times before prices.` Delete `test-4`.

15. `l8-stack-and-heap.json` | `screens[7].prose` | imprecise, minor | "Exchange feeds often have a C interface" is an unsourced remark about industry practice (ledger verdict `unverified`). | No source is given and none was found for "often". The teaching does not depend on it. | `Some exchange feeds have a C interface: you hand over a buffer and the feed fills it.`

### Ledger rows that are `unverified` and not findings

- `homework-2.json` `items[6].explain.text`: "a test run printed 2.8974e-306". The same snippet printed 2.93542e-306 in my run under the same compiler (check `h2.i6.realloc`). The sentence claims one run, not a guarantee, so it stands. If the fixer wants a figure that any run supports: `a test run printed a stray number near 3e-306`.

### Observations, not findings

- l3 `screens[5]`: the prose says "When `n` is 0 the loop must never run". A `do`-`while` that runs once passes every test, because the failed read adds 0 (check `l3.s5.do-while`). The test cannot tell; no sentence is false.
- l11 `screens[10]`: with the move constructor declared, leaving out both `= delete` lines passes every test, because the copy is then implicitly deleted (check `l11.s10.no-delete`). The `test-8` line is reached only by a hand-written copy constructor (check `l11.s10.fb-test-8`). No sentence is false.
- l5 `screens[4]`: the timing table says 0.2 µs, 3 µs, 20 µs and 1 ms. Two runs under node gave 0.1 to 0.3, 1.7 to 3.4, 35 to 43 and 1,170 to 1,520 µs. I count "about" as holding.
- l13 `screens[4]`: an explicit `-ferror-limit=20` prints "21 errors generated."; the default limit prints 20, as the screen shows (local clang 18).

## Gates

- `node tools/validate.mjs`: 0 errors, 4,536 warnings; `content/manifest.json` unchanged.
- `docs/reports/cpp-1-perf-numbers.py`: exit 0. `docs/reports/cpp-3-perf-numbers.py`: exit 0. (Run, not opened. No `cpp-L*-numbers.py` exists.)
- `node tools/grade-all.mjs --file` on review-1, review-2, review-3, homework-1, homework-2, homework-3: 0 failures each, exit 0.
- `python3 docs/reports/cpp-L1-3-r2-concepts.py --wasm <pkgs>`: 369 checks, 352 hold, 17 fail, exit 1. The 17 are the checks behind findings 1 to 14 (finding 15 has none). With `--recorded` the exit code is 0 when exactly those 17 fail. The script takes about two minutes with `--jobs 6`; each job holds a copy of the compiler in memory, so use `--jobs 4` or fewer on a small machine.
- No playthrough: no content was changed.

## Overlap table

Read after the WIP commit `d05d45a3`: `docs/reviews/review-1.9.md` (section "cpp", the lines for l1 to l13, review-1 to review-3 and homework-1 to homework-3, and its fix pass), `docs/reviews/audit-cpp-1-3.md` (round 1 audit, its fix pass and its fix-pass read) and `docs/reports/audit-cpp-1-3-ledger.md`.

Conceptual findings of the earlier reads in this scope: 33. That is 15 from review-1.9 (the count the round 1 audit made), 17 from the round 1 audit and 1 from its fix-pass read.

| | count |
|---|---|
| found by this audit only | 14 |
| found by the earlier reads only | 32 |
| found by both | 1 |

The one in "both" is finding 5. Round 1 finding 15 raised the same rule, [expr.call]/4, on one line of l9 `screens[9]`, and its fix changed that line only. The sentences listed in finding 5 were left, and I had also seen a line of the round 1 script on the subject before my commit (see "Blind rule" above). So it is counted as found by both, not as new.

What the earlier reads said about the 14:

- A search of the three earlier files for "Each snippet", "total was an", "byKey.error", "level 4's containers", "often have a C" and the six `byKey.test-N` paths of findings 9 to 14 finds none of them as a finding.
- The round 1 ledger passed four of these rows as `correct`. l9 `screens[2]` "`throw`s included": it noted "for an exception that is caught" and passed the row (finding 4). l3 `screens[3]` `byKey.error`: passed in a grouped row (finding 8). l13 `screens[7]` "wrong 123": passed in a grouped row (finding 3). l4 `screens[5]` `byKey.test-2`: passed in a grouped row on arithmetic alone (finding 12).
- The round 1 ledger also passed l5 `screens[0]` "destroyed at the function's closing brace" as "true in the app". The run here shows otherwise: in the app a `std::vector` passed by value is destroyed after the rest of the calling expression (check `l5.s0.vector-param`). Only the `unique_ptr` parameter of l9 is destroyed in the callee on this build.
- Finding 6 is drift, not a miss. review-1.9 found that the first 22 lines of the l13 transcript matched the app's compiler character for character. The engine has since moved libc++ from the debug to the extensive hardening mode (`cpp-worker.js`, ENGINE-BACKLOG 599), and the notes changed with it.
- Round 1 finding 3 (l11 `test-10`) was of the same class as findings 2 and 9 to 14: a `test-N` line whose named mistake does not fail test N. Round 1 found one; this read, which graded a submission for every such line, found seven more lines (in findings 2, 10, 11, 12, 13 and 14), and the unreachable key of finding 8.

New `wrong` findings that no earlier read found: **3** (findings 1, 2 and 12). All three are `minor`. None changes a definition, a rule of the language, a graded key or a method.

Convergence rule: three new `wrong` in three levels is above the limit of one, so by the rule as written the course needs another blind audit after the fix pass. Stated plainly for whoever decides: the three are one false sentence about what the browser build did (`at` stops the run) and two feedback lines with a false diagnosis. The count of `wrong` about C++ itself, in 2,145 ledger rows, is zero.

## Inbox bullets

Appended to `docs/BACKLOG-INBOX.md` under `Raised later (audit cpp):` (three bullets): the unreachable `byKey.error` key on C++ code widgets; a no-browser grader for C++ widgets and a rule for `test-N` feedback routing (the finding class has now been seen eight times in two rounds); console transcripts that go stale when the engine's compiler flags change.

## Fix pass

Fixer: Opus, worktree branch `worktree-agent-adf099dd8f125a86c`. Every fix below rests on my own runs through the auditor's harness (`cpp-L1-3-r2-zq.mjs`: the app's `cpp-grade.js` helpers, `cpp-worker.js` runtime and flags, YoWASP clang 21.1.4, wasm32, libc++, `-O1`), a desk g++ build, or the standard. Content strings only; no test, starter or solution changed.

### Which key the grader shows (`app/js/engine/widgets/cpp-grade.js`, `grade()` and `runCases()`; `player.js` line 111)

- Compile or link error: key `compile`. An untouched starter that does not build gets `compile` too, so its byKey line shows.
- A program that stops on test N (libc++ hardening trap, uncaught exception with status 134, non-zero exit such as the leak checker's status 1): that row fails; the key is `test-N` of the first failing row.
- Wrong output or value on test N: key `test-N` of the first failing row.
- Time-out on test N: that row gets the "Stopped after" error and later rows "Not run"; key `test-N`.
- `error` only when the runner itself fails (it never answers, or the compiler is still loading). No learner's program reaches it.
- The player shows `feedback.byKey[key]` if present, else the grader's own line.

### Findings

1. fixed differently. The five snippets as written: the null read printed 0 (exit 0); `delete` on `new[]` ran (exit 0, a compile warning); the double `delete` ran (exit 0); `new double[0]` ran (exit 0); `v.at(5)` stopped with "terminate called after throwing an instance of 'std::out_of_range'", status 134. Prose: "In this browser build four of these snippets ran to the end, and one stopped with an error message." The explain's "the null read gave a stray number" became "gave 0", as the run printed.
2. fixed differently. `byKey.test-2` deleted. An `int` or `double` total gives key `compile` with "invalid operands to binary expression ('int' and 'const std::string')" (and `'double'`). The compile line keeps its two sentences and adds: "If it says `invalid operands` next to `std::string`, your total is not a `T`: declare it as `T`." The kept sentences checked: returning `int` and leaving out the `template` line both give `compile`.
3. fixed. Slip `two` is now 123.45 with tolerance 0.5. Computed twice: 1.2345 × 100 = 123.45; the band 122.95 to 123.95 holds 123.45 and a truncated 123, and excludes the key 12345 and the `raw` band 1.2344 to 1.2346. Slip value and tolerance changed.
4. fixed. [except.ctor]/1 destroys automatic objects on the way to a handler; [except.handle]/9 leaves unwinding implementation-defined when there is none. Desk g++: a caught throw prints the guard's `freed` before `caught`. The app: an uncaught throw ends the run and prints nothing.
5. fixed. C++17 [expr.call]/4: a parameter's lifetime ends when the callee returns or at the end of the full-expression, implementation-defined. Every call on these screens is a whole statement (`add_fee(mine);`, `normalise(w);`, `hold(std::move(p));`), so both moments fall before the next statement. Runs: the copy is destroyed before `next` in the app and on g++ and clang. The six sentences as the auditor wrote them.
6. fixed. With `_LIBCPP_HARDENING_MODE_DEBUG` every quoted line appears; with the checks off the `strict_weak_ordering_check.h` and `sort.h:939` lines do not. The prose now ends "from a build with the library's debug checks on."
7. fixed. [sequence.reqmts], optional operations: `pop_front` is constant time for `deque`. A search of level 4's files finds no `std::deque`, `std::queue` or `pop_front`.
8. fixed differently. l3 `error` renamed `test-1`: "Test 1 has five closes and two up days. If the program stopped with index out of bounds, your loop read outside the vector: start at 1 and test `i < prices.size()`, not `<=`." "Outside", not "past the last close": a loop from 0 reading `prices[i - 1]` also stops on test 1. homework-1 `error` deleted; its advice is in `test-6` (checked).
9. fixed differently. Test 2 is the exact compare. A missing `'\n'`, a trailing space and an extra blank line each pass test 1 and fail test 2; a missing comma or a lower-case h fails test 1; `std::endl` passes. Line: "The words match but not every character. Test 2 compares exactly: one `'\n'` at the end, no space before it and no blank line after."
10. fixed. Key renamed `test-1` with the auditor's text: fixed decimals fail test 1 with `Price: 72.50`, and the starter also lands on `test-1`. No natural mistake reaches test 3 (`setprecision(5)` passes all four).
11. fixed differently. One `test-1` line covers all three slips, each graded: "Test 1 should give 0.2: from 110 to 88. If you got 0.12, you measured from the first close, not the highest so far. If you got −0.2 or 0, check the sign: the fall is `peak - p`." A fixed peak gives 0.12; `p - peak` gives −0.2 (worst kept by `<`) or 0 (kept by `>`). `test-4` and `test-6` now name no cause.
12. fixed differently. `test-1` gets the "`i` at 0" sentence (stops on test 1, checked). `test-2`: "If the program stopped, your loop read `prices[1]`, past the only close: test `i < prices.size()` before each turn." A `do`-`while` from 1 passes test 1 and stops on test 2 with index out of bounds. `test-3` added as the auditor wrote it; `size() - 1` stops on test 3.
13. fixed differently. `test-2`: "... If you got some other number, your loop may have read `*end`: stop at `p != end`." The read past the end is undefined, hence "may". `test-5` names no cause: "Test 5 passes the range `xs + 1` to `xs + 3`: the values 1 and 4, so the answer is 4."
14. fixed differently. `test-1`: "Test 1 expects B, C, A: B is cheapest, and C arrived before A at the same price. If you got C, A, B, you compared times first; if B, A, C, you broke no tie on `time`." Time first gives C, A, B; price only gives B, A, C. `test-4` deleted: `queue` sorts with `operator<`, so a wrong `<` fails test 1 first.
15. fixed differently. No source for "often" or for "some"; written as a hypothetical: "Say a market-data feed has a C interface: you hand over a buffer and the feed fills it."

Ledger `unverified` rows: l8 `screens[7].prose` is finding 15. homework-2 `items[6].explain`: the round 1 build printed 2.8974e-306 and this harness 2.93542e-306, so the sentence now says "a test run printed about 2.9e-306", true of both.

### Sweep: every `feedback.byKey` line on the 47 code widgets of L1 to L3

79 lines checked: 13 rewritten, 3 deleted, 1 added, so 77 now. For each `test-N` line a submission with the named mistake was graded and its key compared with N; lines that name no mistake were checked against what the test holds; compile lines against the clang message for each mistake they name. Each is a check in `cpp-L1-3-r2-concepts.py` (ids `fx.*` and the audit's `*.fb-*`).

| widget | lines | result |
|---|---|---|
| l1 s3 | compile; test-2 | compile: a missing `;` gives `main.cpp:4:41: error`. test-2 rewritten (finding 9) |
| l1 s4 | test-2; test-3 | test-2: `getline` passes test 1, fails test 2. test-3 became test-1 (finding 10) |
| l2 s4 | test-1; test-5 | the starter gives 3 on test 1; `(a + b) / 2.0` passes 1 to 4 and gives −1 on test 5 |
| l2 s5 | test-2 | the starter gives −2,144,967,296 on test 2 |
| l2 s9 | test-2; test-3 | `int` pence gives 12,949,672.96 on test 2 (−3,000,000,000 pence checked); `/ 100` gives 0 on test 3 |
| l3 s3 | test-2; test-6; error | `size() - 1` stops on test 2 (4,294,967,295 here); `>=` fails test 6; error became test-1 (finding 8) |
| l3 s4 | test-1; test-4; test-6 | rewritten (finding 11) |
| l3 s5 | test-1; test-2 | starting at `n` prints 9.75 on test 1; test-2 describes the test |
| l3 s8 | test-1; test-3 | the starter gives Cboe 3 on LLCT; no `default` fails test 3 |
| l4 s5 | compile; test-1; test-2 | compile rewritten from runs: by value gives `ambiguous`, `&` without `const` gives `undefined symbol`, another return type gives `previous declaration`. test-1 and test-2 rewritten, test-3 added (finding 12) |
| l4 s6 | compile; test-1 | `= 252` twice gives "redefinition of default argument"; `* days` gives 2.52 on test 1; 0.01 × √252 = 0.1587 |
| l6 s4 | compile | the starter, `q.ask_` (private) and `Quote&` (static assertion) all give compile |
| l6 s7 | compile | the starter's `px[i] +=` gives compile |
| l7 s3 | test-5 | no null guard fails test 5 only |
| l7 s4 | test-2; test-5 | rewritten (finding 13); a best at 0 gives 0 on test 2 |
| l8 s6 | test-1 | `delete px` prints the right sum and fails test 1 with the leak check, status 1 |
| l9 s3 | test-3 | the starter fails test 3 only |
| l9 s5 | test-4 | no check for 0 fails test 4 |
| l10 s3 | compile; test-4; test-5 | the starter gives "no member named 'mid'", no `const` gives "not marked const", no `spread` gives "no member named 'spread'"; no check fails 4; `>` fails 5 |
| l10 s5 | test-2, 4, 6, 8, 9 | each named mistake fails exactly its test; (100 × 10 + 300 × 12) / 400 = 11.5 |
| l10 s9 | test-4, 7, 8, 9 | each named mistake fails exactly its test |
| l11 s3 | compile; test-1 | `void ~Logger()` and `~Logger(int)` give compile; no inner braces fails test 1 |
| l11 s7 | test-2, 5, 9, 10, 12 | each named mistake fails exactly its test |
| l11 s10 | test-1, 2, 8 | each named mistake fails exactly its test |
| l12 s2 | compile; test-2; test-8 | the starter and `operator*(Money, Money)` give "invalid operands"; no padding fails 2; no absolute value fails 8 |
| l12 s7 | test-5; test-7 | `<=` fails 5; the venue in `==` fails 7 |
| l12 s9 | test-1; test-4 | test-1 rewritten, test-4 deleted (finding 14) |
| l13 s2 | compile; test-2; test-7 | compile rewritten, test-2 deleted (finding 2); `T total = 0` stops on test 7 |
| l13 s9 | test-2, 7, 8 | each named mistake fails exactly its test |
| review-1 i5 | test-1; test-3 | `limit` for `-limit` gives 4 on test 1; `<=` fails test 3 |
| homework-1 i1 | test-2, 4, 6; error | a first close read before the loop stops on 2; a worst reset at each peak fails 4; no comma skip stops on 6; error deleted (finding 8) |
| homework-1 i2 | test-1, 4, 5 | the starter and swapped buy and sell fail 1; `<=` fails 4; `>=` fails 5 |
| homework-1 i3 | test-3 | an `int` total gives −294,967,296 on test 3 |
| homework-2 i0 | test-1 | `for (Position p : book)` fails test 1 |
| homework-2 i1 | test-4 | an `int` total fails test 4 |

The other 12 code widgets have no byKey lines. Numeric slips: all 61 `wrong[]` values in the 19 files recomputed from the mistake each line names; one changed (finding 3).

### Scripts

- `cpp-L1-3-r2-concepts.py --wasm <pkgs> --jobs 4`: 423 checks, 0 fail, exit 0. `EXPECTED_FAIL` is now empty. The 17 failing checks were rewritten to state what the content now says (key `test-1` or `compile`, the new slip band, statement-call lifetime, the qualified prose). Added: a desk check for a caught throw, an expression-lifetime observation, the literal null snippet, a rule that no code widget keeps a key other than `compile` or `test-N`, key lists for the 8 widgets whose keys changed, and 42 more `fx.*` sweep checks (54 checks added in all).
- `cpp-L1-3-concepts.py`: 126 checks without `--wasm`, 139 with, 0 failed. One check changed: the h-realloc figure is accepted between 2.85e-306 and 2.95e-306.
- `cpp-1-perf-numbers.py` and `cpp-3-perf-numbers.py`: exit 0.

### Gates

Validator 0 errors, `content/manifest.json` unchanged. Voice scan 35: 0 and 0. Playthrough green, desktop and `--mobile`: l1, l3, l4, l5, l7, l8, l9, l12, l13, homework-1, homework-2.
