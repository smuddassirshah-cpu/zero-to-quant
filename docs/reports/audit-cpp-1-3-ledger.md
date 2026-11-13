# Claim ledger: cpp L1 to L3 (round 1 blind audit, 13 Nov 2026)

Scope: `app/content/courses/cpp/` lessons l1 to l13, review-1 to review-3, homework-1 to homework-3. Stage 1, full depth.

Basis shorthand. **run** = `docs/reports/cpp-L1-3-concepts.py` (g++ 13.3.0 and clang 18.1.3 on x86-64 Linux, libstdc++; **run-wasm** = the same script with `--wasm`, which uses the app's YoWASP clang 21.1.4, wasm32, libc++, `-O1`, hardening flags copied from `app/js/screens/cpp-worker.js`). **std** = ISO C++17 (N4659), section name in brackets; a paragraph number is given only for the handful of rules where it matters and was certain. **probe** = a one-off run recorded in the audit file, not kept in the script. Where wasm32 and the desk differ (`sizeof(long)` and `size_t` are 4 bytes, a vector object is 12 bytes) the row says so.

Paths: one row may cover several JSON paths that state the same claim; they are listed together. `why[id]` is `widget.options[...]` with that id; `byKey.x` is `feedback.byKey.x`.

Verdicts: correct, wrong, imprecise, misleading, unverified.

## l1-source-to-program.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] prose, answer l3, byKey.*, explain | `g++ main.cpp -o main` reads the text and writes the executable; `./main` never reads the source | correct | compile and link model, GCC manual "Overall Options"; run (every native check builds this way) |
| screens[1] answer ld, byKey.cc/obj/lib/exe, explain | compiler makes an object file with unresolved names; the linker joins it with the library; `g++` keeps the object only as a temporary | correct | std [lex.phases] phase 9; GCC manual; run l4 quiz2 (undefined reference comes from ld) |
| screens[2] key, why[1..3], byKey.new, explain | an edit reaches the executable only after a rebuild | correct | follows from the row above |
| screens[3].prose "Every C++ program starts in `int main()`" | execution starts in `main` | correct | std [basic.start.main]/1 (static initialisers aside) |
| screens[3].prose "every statement ends with `;`"; quiz[2] why (option 3) "Every C++ statement ends with `;`"; quiz[2].explain "a `;` at the end of every statement" | every statement ends with a semicolon | imprecise | std [stmt.block], [stmt.select], [stmt.iter]: a compound statement, and an `if` or `for` with a block, end with `}`; the lesson's own `int main() { }` and `if (signals = 0) { }` show it. Finding 7 |
| screens[3] solution, tests, hints, byKey.test-2, explain | `std::cout << "Hello, market" << '\n';` prints the line; `return 0` reports success | correct | run l1 s7 (same statement); std [basic.start.main]/5 |
| screens[4] prose, hints, byKey.test-2, explain | `std::cin >> x` skips whitespace, reads one word, converts to the type of `x`; line breaks and spaces are the same | correct | std [istream.formatted.arithmetic], [string.io]; l3 s5 solution runs on mixed layouts (author tests) |
| screens[4] byKey.test-3 | `12000` printed as `std::cout` prints a double | correct | default `%g`-style output, six significant digits: std [facet.num.put.virtuals] |
| screens[5] canvas, answer l5, explain | g++ reports the missing `;` at `main.cpp:5:5`, `expected ',' or ';' before 'std'` | correct | run l1 s5 (exact text and position) |
| screens[6] answer l4, byKey.l5, explain | the slip is on line 4; clang points at the end of line 4, `expected ';' at end of declaration` | correct | run l1 s6 (`main.cpp:4:25`) |
| screens[7] key, why[1..3], explain | a warning does not stop the build; `-Wall` adds warnings only; `main` returns 0 at its end, no other function does | correct | run l1 s7; std [basic.start.main]/5, [stmt.return] |
| screens[8] key 0, why[1..3], hints, byKey, explain, summary.trap | `if (signals = 0)` compiles, stores 0, tests false, prints 0; g++ silent without `-Wall`, clang warns by default | correct | run l1 s8 |
| screens[8].prose | an indented second line after a brace-less `if` compiles | correct | std [stmt.select]: only one statement is governed |
| screens[9] order | write, compile, link, run, return | correct | as rows above |
| screens[10].prose "g++ prints 232 lines" | length of the g++ 13 error for `std::cout << closes` | correct | probe: g++ 13.3.0 prints exactly 232 lines |
| screens[10].prose "Desks write pricers in C++ because compiled loops, such as a binomial tree, run many times faster than Python" | industry remark | unverified | no source given; the speed claim alone is uncontroversial |
| screens[10] answer l2, byKey.l5..l8, explain | the one `error:` line states the problem; notes list rejected candidates; no `<<` for a whole vector | correct | run l1 s10 |
| summary.ideas[0..2], formula | restatements | correct | rows above |
| quiz[0] key, why, explain | "not declared in this scope" with `did you mean 'price'?` is a typo of a name | correct | run l1 quiz0 |
| quiz[1] key, why | `-o pricer` names the executable; `./pricer` runs it | correct | GCC manual `-o` |
| quiz[2] key, why[print], why[cout] | `print("hi")` and bare `cout` do not compile with only `<iostream>` | correct | run l1 quiz2 |
| quiz[3] key, why | warnings stop neither compile nor link; no errors means a new executable | correct | run l1 s7 |
| screens[3..4].widget.how "about 26 MB", "10 to 15 s" | app timings | unverified | engine facts, outside a concept read |

## l2-fixed-types.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] key 3, wrong 3.5, 4, hints, byKey.py/round, explain | `int / int` is an `int`; 7 / 2 is 3; like Python `//` for positive numbers | correct | std [expr.mul]/4; run l2 s0 |
| screens[1].prose "An `int` is 4 bytes, 32 bits" | size of `int` | correct | implementation-defined (std [basic.fundamental]/2); 4 in the app (run-wasm) and on the desk; screens[2].explain states the caveat on the next screen |
| screens[1] key −2147483648, wrong nowrap/stick, byKey, explain | adding 1 three times to 2147483645 wraps to INT_MIN; "the standard calls it undefined, so never rely on it" | correct | std [expr]/4 (undefined); wrap value: run l2 s1 (`-fwrapv`); the explain states the hypothesis |
| screens[2] table | `int` 4 bytes ±2,147,483,647; `long long` 8, about ±9.2e18; `double` 8, about 15 significant digits; `bool` 1; `char` 1 | correct | run and run-wasm sizes; 2^63 = 9.22e18; DBL_DIG = 15 |
| screens[2].prose "every variable has a type fixed when you declare it ... The type sets the size in bytes, which `sizeof(int)` reports, and so the range" | static typing, `sizeof` | correct | std [basic.types], [expr.sizeof] |
| screens[2].question "A day's traded volume across all UK shares can pass 3 billion" | market figure | unverified | no source |
| screens[2] answer r1, byKey.r0/r2/r5, explain | 3 billion needs `long long`; a `double` holds it but integers add exactly; "sizes are as listed in this app; `sizeof` tells you on any machine" | correct | 3e9 > 2^31 − 1; std [basic.fundamental] |
| screens[3].prose "`auto` asks the compiler to give a variable the type of the value on the right"; summary.ideas[0] "`auto` copies the type of the value on the right" | deduction rule | imprecise | std [dcl.spec.auto] with [temp.deduct.call]/2: top-level `const` is dropped and no reference is ever deduced; run l2 s3 second check. Harmless at this screen, wrong habit once level 2 teaches references. Finding 8 |
| screens[3] key, why[1..3], byKey.d35, explain | `auto r = 7 / 2;` is `int` 3; `7.0 / 2` gives a `double` 3.5 | correct | run l2 s3 |
| screens[4] prose, starter, solution, tests, hints, byKey.test-1, explain | `(a + b) / 2` divides in `int`; `static_cast<double>(a) + b` converts first; `(a + b) / 2.0` still overflows | correct | run l2 s4; std [expr]/11 usual arithmetic conversions |
| screens[4].byKey.test-5 "In `int` that sum wraps negative before any division" | overflow result | correct | in practice (run l2 s4, `-fwrapv`: −2); formally undefined, said on screen 1 |
| screens[5] starter, solution, byKey.test-2, explain "C++ narrows it silently ... −2,144,967,296" | `long long` 2,150,000,000 stored in `int` | correct | run l2 s5; std [conv.integral]/3 implementation-defined in C++17, modulo 2^32 from C++20; 2150000000 − 2^32 = −2144967296 |
| screens[6] key −3, wrong −4, −3.5, 3, hints, byKey.floor/sign, explain | integer division truncates towards zero; Python `//` floors; they differ only for negative answers | correct | std [expr.mul]/4; run l2 s0 |
| screens[7] key 1998, why[1..3], hints, byKey.1999, explain, summary.trap | `19.99 * 100` is 1998.9999999999998; conversion to `int` truncates; `std::lround` gives 1999; 19.99 is stored slightly low | correct | run l2 s7; std [conv.fpint]/1; 19.99 as a double is 19.98999999999999843 |
| screens[7] why[3] "Only some warning flags mention it" | `-Wconversion` class of flags reports double to int | correct | GCC manual `-Wfloat-conversion` |
| screens[8] prose rule, key, why[1..3], explain | "an operation works in its operands' type, and one `double` makes it `double`"; `3.0 / 4` is 0.75; the other three give 0 | correct | std [expr]/11; run l2 s0 (integer promotion of small types not needed here) |
| screens[9].prose "Exchanges quote prices in whole ticks, and order books store them as integers" | industry remark | unverified | no source |
| screens[9] solution, tests, hints, byKey.test-2/3, explain | pence in `long long`, one division by `100.0` | correct | run l2 s9 |
| summary.ideas[1], formula, note | restatements | correct | rows above |
| summary.ideas[2] "`int` stops at 2,147,483,647 and wraps silently" | overflow behaviour as a rule | imprecise | std [expr]/4: undefined, the compiler may assume it never happens; the summary drops the hypothesis that screen 1 and quiz[2] state. Finding 6 |
| quiz[0] key 1, why, explain | `std::cout` prints a `bool` as 1 or 0 unless `std::boolalpha` | correct | run l2 quiz0; std [ostream.inserters.arithmetic] |
| quiz[1] key 8, wrong 4, 64, explain | `sizeof(long long)` is 8 | correct | run and run-wasm (at least 64 bits by std [basic.fundamental]; 8 on both platforms) |
| quiz[2] key ("in practice"), why, explain "Formally this is undefined behaviour" | wrap to INT_MIN | correct | as screens[1] |
| quiz[3] key 0, why, explain | `double share = 1 / 4;` is 0 | correct | run l2 quiz0 |

## l3-branches-and-loops.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] answer c1, c3, wrong first, byKey, explain | loop from 1 compares each close with the one before; `ups` is 2; braces mark the body | correct | hand trace 100, 104, 101, 106, 103 |
| screens[1] definition of drawdown, key 0.2, wrong 0.12 (from the first close), 0.1 (day 2), byKey.first, explain | (110 − 88) / 110 = 0.2; peak only rises | correct | arithmetic; standard definition (fall from the running peak) |
| screens[2] prose, key 5, wrong 6, 4, byKey, explain | start, test before every turn, step; `i` takes 1 to 5; equals Python `range(1, len(prices))` | correct | std [stmt.for] |
| screens[3].prose | `const std::vector<double>&` reads the caller's closes without copying | correct | std [dcl.init.ref] |
| screens[3] solution, tests, hints, byKey.test-6, byKey.error, explain | loop from 1 with `<`; `std::size_t` is the unsigned type `size()` returns | correct | author tests; std [vector.overview] `size_type` (it is `std::size_t` for the default allocator) |
| screens[3].byKey.test-2 "0 − 1 wraps to about 4 billion" | value of `size() - 1` on an empty vector | imprecise | run-wasm: 4,294,967,295 in the app; run l3 quiz2: about 1.8e19 on a 64-bit desk. Stated without "in this app". Finding 9 |
| screens[4] prose, solution, tests, byKey.test-1/4/6, explain | max drawdown by a running peak and a running worst; `for (double p : prices)` is Python `for p in prices` | correct | run l3 s4 (0.2, 0, 0.1, 0.5, 0.75); 0.4 = (100 − 60) / 100 is the stuck-peak slip |
| screens[5] solution, tests, byKey.test-1 ("9.75, you added n"), explain "prints 0.3 because `std::cout` shows six significant digits" | counting loop over input | correct | 3 + 6.75 = 9.75; run l3 quiz0 |
| screens[6] key, why[1..3], explain | `<=` reads `prices[3]`; "this app stops it, a normal build may read garbage"; only `at` checks and throws | correct | std [sequence.reqmts] (`[]` unchecked, `at` throws `out_of_range`), undefined by [res.on.arguments]; run-wasm l3 s6 (hardening stops it) |
| screens[7] prose, key, why, explain | a variable declared in the `for` ends with it; `continue`, `break` | correct | std [basic.scope.block], [stmt.jump]; run l3 s7 |
| screens[8] prose, starter, solution, byKey.test-1/3, explain | `switch` falls through without `break`; `default` takes the rest; silent unless `-Wimplicit-fallthrough` | correct | std [stmt.switch]/6; run l3 s8 (two checks) |
| summary.ideas, formula MDD, trap | restatements; MDD = max over t of (running max − p_t) / running max | correct | standard definition |
| quiz[0] key, why, explain | `0.1 + 0.2 == 0.3` is false; sum is 0.30000000000000004; compare with a tolerance | correct | run l3 quiz0 |
| quiz[1] key 6, wrong 5 | `i <= 5` from 0 is six turns | correct | run l3 quiz3 check |
| quiz[2] key, why[1..3], explain | `size() - 1` on an empty vector wraps to the maximum; `i + 1 < size()` is the fix | correct | std [basic.fundamental]/4 (unsigned arithmetic is modular); run l3 quiz2 |
| quiz[3] key 2, wrong 3, 4, byKey, explain | `break` before `++day` | correct | run l3 quiz3 |

## l4-functions-and-headers.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] key, why[1..3], hints, explain | a name must be declared before use; the compiler reads top to bottom; Python looks the name up at call time | correct | std [basic.scope.pdecl]; run l4 s0 (g++ wording) |
| screens[1] answer l4, byKey, explain; screens[2] prose, answer, wrong def, byKey, explain | declaration (name, types, `;`) against definition (adds the body, and declares too); parameter names optional in a declaration | correct | std [basic.def], [dcl.fct] |
| screens[1].prose "prints 0.158745" | 0.01 × √252 | correct | run l4 s1 |
| screens[3] prose, answer l11, byKey, explain | header holds declarations; each `.cpp` compiles alone; `#include` pastes text; the linker connects the call | correct | std [cpp.include], [lex.phases] |
| screens[4] prose, key 0.191, wrong 0.1587 (default), 3.65 (× 365), explain | a default argument fills in only when the argument is left out; 0.01 × √365 = 0.19105 | correct | std [dcl.fct.default]; run l4 s1 |
| screens[5] solution, tests, byKey.test-1/2/compile, explain | n closes give n − 1 simple returns, (today − yesterday) / yesterday; the definition must match the declaration | correct | arithmetic; (99 − 110) / 110 = −0.1 |
| screens[6] prose, byKey.compile, explain | the default is written once, in the declaration; repeating it is `redefinition of default argument` | correct | std [dcl.fct.default]/4; run l4 s6 |
| screens[6].explain "Annualising a daily volatility by √252 assumes 252 trading days a year" | convention | correct | square-root-of-time rule; it also assumes uncorrelated daily returns, which this C++ lesson need not carry |
| screens[7] key, why[1..3], byKey.ignored, explain, summary.trap | a body in a header included by two `.cpp` files is a `multiple definition` link error; `#pragma once` works per `.cpp`; fix by moving the body or `inline` | correct | std [basic.def.odr]/4, /6; run l4 s7 (two checks) |
| screens[8] key, why[1..3], explain | a default only in `returns.cpp` is invisible to `main.cpp`: compile error, too few arguments | correct | std [dcl.fct.default]/4; run l4 s8 |
| screens[9] key, why, byKey.hdr, explain | `.a` is linked in; `.so` loads when the program starts; header alone gives `undefined reference` | correct | GNU ld manual; run l4 quiz2 |
| summary.ideas[0..1], formula | restatements | correct | rows above |
| summary.ideas[2] "Exactly one definition per program" | one-definition rule | imprecise | std [basic.def.odr]/6: inline functions and templates may be defined in every translation unit. The lesson names `inline`; level 3 (l13 quiz[2]) then puts template bodies in headers with no word on why that is allowed. Finding 10 |
| quiz[0] key, why[1..3], explain | overload chosen by argument types; `mid(10001LL, 10002LL)` is 10001; prints `10001 100.015` | correct | std [over.match]; run l4 quiz0 |
| quiz[1] key, why[1..3], explain | `risk_free_rate` without `()` converts to `true` and prints 1; `(void)` and `(0)` in a call do not compile | correct | std [conv.func], [conv.bool]; run l4 quiz1 |
| quiz[2] key, why[1..3], explain | `undefined reference` from `ld`: `returns.cpp` missing from the command | correct | run l4 quiz2 |
| quiz[3] key 0, wrong 1 | one close gives no returns | correct | n − 1 |

## l5-value-or-reference.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] key 2, why[1..3], hints, explain | a `std::vector<double>` parameter is a copy; the caller's vector keeps size 2 | correct | std [expr.call]/4, [dcl.init]; run l5 s0 |
| screens[0].hints[2], explain "the copy is destroyed at the function's closing brace" | when a by-value parameter dies | correct | implementation-defined, std [expr.call]/4; true in the app (run-wasm info line), later on x86-64; see l9 screens[9] row |
| screens[1] prose, answer, byKey, explain; screens[2] prose | a variable is its object; `&` on the type makes a second name; a reference is another name for an existing object | correct | std [dcl.ref], [dcl.init.ref] |
| screens[2] key 997.5, why[unchanged/fee/zeros], explain | `balance -= fee` changes `cash`; `std::cout` prints 997.5 without trailing zeros | correct | run l5 s0 check |
| screens[3] key, why[value/ref/cvalue], explain | `const std::vector<double>&` shares without copying and forbids changes; `const` by value still copies | correct | std [dcl.init.ref], [dcl.type.cv] |
| screens[4] table timings "about 0.2 µs, 3 µs, 20 µs, 1 ms"; caption "a few nanoseconds" for `const&` | by-value copy cost in the app build | correct | probe (app compiler under node): 0.11, 1.6, 16 and 800 µs; 4 to 14 ns by reference. Same order of magnitude; machine dependent |
| screens[4] key 8 MB, wrong 8000000, 1, 64, byKey, explain | 1,000,000 × 8 bytes = 8 MB; 1,000 calls a second at 1 ms each fill the second | correct | arithmetic |
| screens[5] solution, tests, explain | sum of qty × px = 1913 by `const&` | correct | 485 + 180 + 1248 |
| screens[6] key 2, why, explain "The compiler cannot warn you: copying is legal" | `normalise` on a copy leaves the caller's weights | correct | run l5 s0 check; no compiler warning exists for this (clang-tidy aside) |
| screens[7] solution, tests, explain | `&` fixes it; dividing by a zero sum gives NaN or infinity; an empty vector sums to 0 | correct | IEEE 754 division; author tests |
| screens[8] prose "Returning a local by value is cheap. The compiler usually builds it in the caller's variable, and otherwise moves it. Either way no element is copied"; summary.ideas[2]; quiz[2] key, why, explain | copy elision or move on `return v;` | correct | std [class.copy.elision]/1, /3; run l5 s8 (0 copies) |
| screens[8] why[ref] "it rejects temporaries and `const` vectors"; explain "Small values such as `double` and `int` go by value" | binding rules; convention | correct | std [dcl.init.ref]/5; C++ Core Guidelines F.16 |
| screens[9] key `a = b;`, why[ba/tb/at], explain | three-line swap through references | correct | hand trace |
| screens[10] key, why, byKey, explain | read-only large object by `const&`, changed object by `&` | correct | Core Guidelines F.16, F.17 |
| summary.ideas[0..1], formula, trap | restatements; `const T&` also accepts temporaries | correct | std [dcl.init.ref]/5 |
| quiz[0] key 9, why, explain "There is no reference to a reference" | `int& r2 = r;` names `x` | correct | std [dcl.ref]/5; run l5 s0 check |
| quiz[1] key, why, explain | `apply_fee(100.0, 2.50)` does not compile; clang: "expects an lvalue for 1st argument" | correct | run l5 quiz1 |
| quiz[3] key, why | Python's shared mutable list is `std::vector<double>&` | correct | semantics above |

## l6-const.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] key, why[1..3], explain canvas | assigning to a `const double` is a compile error; clang text and positions 3:10, 2:18 | correct | std [dcl.type.cv]; run l6 s0 |
| screens[1] answer l4, wrong fee-too/copy, byKey, explain | only `px += fee` writes through the `const&`; clang text | correct | run l6 s1 |
| screens[2] key, why[all/fixed/temp], explain | a plain `std::vector<double>&` binds only to a non-const variable; clang says "would lose const qualifier" and "expects an lvalue"; `const&` takes all three | correct | std [dcl.init.ref]/5; run l6 s2 (four checks) |
| screens[3] prose, key (mid, bid), why[widen/ask], byKey, explain | a `const` object calls only `const` methods; its members are read only | correct | std [class.this], [expr.ref]; run l6 s3 (three checks) |
| screens[4] solution, tests, explain | `const Quote&` accepts a variable, a `const` object and a temporary; only `const` getters may be called | correct | author tests; rows above |
| screens[5] prose, answer l5, byKey.l3/l6, explain | `constexpr` needs the value while compiling; `const` may be set at run time; clang text | correct | std [dcl.constexpr]; run l6 s5 (two checks) |
| screens[6] prose, key 99, why, explain, summary.ideas[2], trap | `const&` restricts the name, not the object; `const int` and `int const` are the same | correct | std [dcl.type.cv]; run l6 s6 |
| screens[7] canvas, solution, hints, explain | clang text for `px[i] += fee` at 5:15; copy inside, return by value | correct | run l6 s7 |
| screens[9] order, explain; screens[10] table, hints, feedback.correct, explain; summary.formula | reading a declaration right to left; `const double*` against `double* const`; clang text | correct | std [dcl.ptr]; run l6 s10 (three checks) |
| screens[11] key, why[fast/lifetime/plainref], explain | `const Tick&`: no copy, no strategy can edit the tick; a reference does not extend the feed's object | correct | rows above. The feed that "reuses its buffer" is a scenario, not a claim |
| summary.ideas[0..1] | restatements | correct | rows above |
| quiz[0] key, why, explain | `const int` and `int const` are one type; position matters only around `*` | correct | std [dcl.type.cv] |
| quiz[1] key, why | run-time value fixed once: `const`, not `constexpr` | correct | std [dcl.constexpr] |
| quiz[2] key, why, explain clang text | write through `const Position&` does not compile | correct | run l6 quiz2 |
| quiz[3] key, why, explain "a temporary, which then lives until the call ends" | `const&` binds to a temporary | correct | std [class.temporary]/6.1: until the end of the full expression that contains the call |

## l7-addresses.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] prose, key 500, why, explain | `&qty` is the address; `*p = 500` writes `qty` | correct | std [expr.unary.op]; run l7 s0 |
| screens[1] answer c3, byKey, explain; screens[2] key 16, wrong 2, 8, 24, byKey, explain; screens[8] order; quiz[3] key 0x200C, why; summary.ideas[0], formula | pointer arithmetic counts whole elements: `p + k` moves `k * sizeof(T)` bytes | correct | std [expr.add]/4; run l7 s0 (16 and 12 bytes) |
| screens[3] prose "Reading or writing through it is undefined behaviour: a desk build usually dies with `Segmentation fault`" | null dereference | correct | std [expr.unary.op] with [basic.stc]; run l7 quiz0 (ASan SEGV on address 0) |
| screens[3] solution, tests, hints, byKey.test-5, explain "This browser build quietly writes to address 0 instead" | guard then write; app behaviour | correct | probe (app compiler): a write through null lands in address 0 and the program carries on |
| screens[4].prose "C code passes a range as two pointers" | attribution of the two-pointer range | imprecise | the usual C convention is a pointer and a count, as this lesson's own screens[9] (`const Level* levels, int n`) shows; the half-open pointer pair is the C++ iterator idiom (std [iterator.requirements.general]). Finding 12 |
| screens[4] solution, tests, hints, byKey.test-2/5, explain | `[begin, end)`: `end` is one past the last and never read; `v.begin()`, `v.end()` generalise it | correct | std [expr.add]/4 (one past the end is valid, not dereferenceable); author tests |
| screens[5] key, why[fine/alive/compile], byKey, explain | reading through a pointer to an object whose scope ended is undefined, whatever it prints; the app printed 101.25 | correct | std [basic.life]/6, [basic.stc.auto]; run-wasm l7 s5 |
| screens[6] canvas, answer l8, byKey, explain | g++ AddressSanitizer reports `stack-use-after-scope`, names `'bid'` and the reading line | correct | run l7 s6 |
| screens[7] key 0, why "two variables never share one" | `&a == &b` is false for two variables | correct | std [intro.object]/8: two objects with overlapping lifetimes that are not nested have distinct addresses |
| screens[9] key, why[le/first], explain | walk `[levels, levels + n)` with `++p`; `<=` reads one past | correct | rows above; sizeof(Level) is 16 (run and run-wasm) |
| screens[9] why[bytes] "jumps 16 levels and runs past `levels + n`" (byKey.bytes, "jumps 16 levels at a time", is correct) | effect of `p += sizeof(Level)` | imprecise | it does jump 16 levels a step, but when `n` is a multiple of 16 the loop ends exactly at `levels + n` having skipped 15 of every 16 levels: it does not always run past. Finding 13 |
| summary.ideas[1], note, trap | null and dangling reads are undefined; `end` is never read | correct | rows above |
| summary.ideas[2] "A desk build crashes on a null read" | certainty of the crash | imprecise | undefined behaviour gives no such promise (the trap line of the same summary says so); the screens say "usually". Finding 11 |
| quiz[0] key, why, explain "g++'s build dies with `Segmentation fault` (AddressSanitizer: SEGV on unknown address 0x000000000000)" | desk behaviour of a null read | correct | run l7 quiz0 |
| quiz[0].explain "In this browser ... a test run printed 1" | app behaviour | unverified | run-wasm: the read does not trap and prints a stray value; the exact digit depends on what sits at address 0 |
| quiz[1] key 7, why, explain | `**pp = 7` writes `x` | correct | run l7 s0 |
| quiz[2] key, why, explain clang text | returning `&x` compiles with a warning; the pointer dangles | correct | run l7 quiz2 |

## l8-stack-and-heap.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] prose "locals ... share one fixed region; here it is 8 MB", caption "here and on a typical Linux desk", key A, why, explain | a 16 MB local array overflows an 8 MB stack; the vector's elements live elsewhere; app says "memory access out of bounds" | correct | `cpp-worker.js` links with `stack-size=8388608`; Linux default `ulimit -s` is 8192 kB; run-wasm l8 s0 (two checks) |
| screens[0].explain, screens[3].explain, quiz[3].explain "a vector object is 12 bytes here and 24 on a 64-bit desk" | size of the vector object | correct | run-wasm (12), run l8 s3 (24) |
| screens[1] states, ops, explain | one frame per call; last in, first out; a local dies at its function's `}` | correct | std [basic.stc.auto]; 300 × 100 = 30000 |
| screens[2] prose, key, why, explain | `new` makes an object that lives until `delete`; copying a pointer copies the address | correct | std [basic.stc.dynamic], [expr.new], [expr.delete] |
| screens[3] prose, table, hints, explain | locals (also a pointer or a vector object) on the stack; what `new` makes and a vector's elements on the heap | correct | std [vector.overview] with the default allocator ([default.allocator]) |
| screens[4] prose, canvas, key 20, wrong 0.008, 20000000, 2.5, byKey, explain | a `new` with no `delete` leaks; LeakSanitizer reports 8000 bytes; 2,500 × 8,000 = 20 MB | correct | run l8 s4; arithmetic |
| screens[5] key, why[nothing/eight/free], byKey, explain canvas | `new[]` with plain `delete` is undefined; clang warns; ASan says alloc-dealloc-mismatch; `free` on `new[]` memory is undefined too; the app ran it silently | correct | std [expr.delete]/2; run l8 s5 (two checks); run-wasm l8 s5 |
| screens[6] prose "`new double[0]` is allowed: it returns a pointer you must not read through, but must still free", solution, byKey.test-1, explain; quiz[1] key, why, explain | zero-length array `new` | correct | std [expr.new]/7, [basic.stc.dynamic.allocation]/2; run l8 quiz1 |
| screens[7] prose, solution, explain | `std::vector<double> out(buf, buf + n)` copies the range; the buffer can then be freed; `out.data()` would avoid it | correct | std [vector.cons], [vector.data] |
| screens[8] prose "The stack is small, a few MB", key, why, explain | deep recursion overflows the stack; the app says "call stack exhausted" | correct | rows above; the string is in `app/js/screens/cpp-worker.js`; probe: 10,000,000 calls trap |
| screens[9] order, explain | the heap object outlives the frame that made it; after `delete q`, `q` dangles | correct | std [basic.stc.dynamic.safety], [expr.delete]/4 |
| screens[10] key, why[newdelete/leak], explain | a member vector sized once and reused | correct | design reasoning from rows above |
| screens[10] why[local] "In standard C++ an array's size must be known at compile time" | no variable-length arrays | correct | std [dcl.array]/1 (constant expression) |
| screens[10].explain "Desks preallocate lattices and buffers for exactly this reason" | industry remark | unverified | no source |
| screens[4].explain "In a server that runs for weeks, leaks like this end in an out-of-memory crash" | consequence of a steady leak | correct | follows from unbounded growth against finite memory |
| summary.ideas[0..1], formula, note, trap | restatements | correct | rows above |
| summary.ideas[2] "The browser build forgives mismatched or double deletes; a desk build with `-fsanitize=address` does not" | app and ASan behaviour | correct | run-wasm l8 s5; run (alloc-dealloc-mismatch, double-free) |
| quiz[0] key, why, explain g++ text | `delete` on a stack address is undefined; g++ warns "called on unallocated object 'price'" and the run aborts with `free(): invalid pointer` | correct | std [expr.delete]/2; run l8 quiz0 |
| quiz[2] key, why, explain | a local in `main` lives for the whole run | correct | std [basic.stc.auto] (objects with static storage are destroyed after `main` returns, not needed here) |
| quiz[3] key, why | a million-element local vector does not overflow the stack | correct | run-wasm l8 s0 program B |

## l9-owning-memory.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] prose, key, why[never/end/early], explain "That timing is guaranteed" | destructor runs at the end of the scope; output order | correct | std [basic.stc.auto], [stmt.dcl]/2; run l9 s0 |
| screens[0].prose "Python frees an object some time after the last name lets go" | Python lifetime | correct | Python language reference, Data model: objects are never explicitly destroyed and collection may be postponed |
| screens[1] answer l3, l9, wrong all, byKey, explain | two early returns skip the only `delete[]` | correct | hand trace of the listing |
| screens[2] prose (RAII), key, why, byKey, explain "early returns and `throw`s included" | a local's destructor runs on every path out | correct | std [stmt.jump]/2, [except.ctor] (for an exception that is caught; an uncaught one may skip unwinding, [except.terminate]) |
| screens[3] prose, solution, tests, byKey.test-3, explain | `std::unique_ptr` deletes in its destructor; `make_unique` creates object and owner | correct | std [unique.ptr.single.dtor], [unique.ptr.create] |
| screens[3].hints[2] "Remove `delete book;`, or the object would be freed twice" | effect of keeping `delete book;` | wrong | run l9 s3: `delete` on a `unique_ptr` does not compile (clang: "cannot delete expression of type"), so no double free can happen. Finding 2 |
| screens[4] prose, canvas, key, why[get/copy/deref], hints, explain | copying a `unique_ptr` is a compile error; `std::move` transfers ownership and leaves the source null; clang text | correct | std [unique.ptr.single.ctor] (source is null after the move); run l9 s4, run-wasm l9 s4 |
| screens[5] prose, solution, tests, explain | returning a `unique_ptr` hands ownership out; `nullptr` for none | correct | author tests; rows above |
| screens[6] key 3, wrong 1, 2, byKey, explain "A run printed 1, 3, 1" | `use_count()` | correct | std [util.smartptr.shared.obs]; run l9 s6 |
| screens[6].prose "Every copy changes the count with an atomic instruction" | cost of a `shared_ptr` copy | imprecise | true only in a threaded build: libstdc++ takes a non-atomic path in a single-threaded process (`__gnu_cxx::__is_single_threaded`), and the app's wasm32 libc++ has no threads. Finding 14 |
| screens[6].prose "which is why desks keep it out of hot paths"; screens[10] why[shared] | industry remark | unverified | no source |
| screens[7] key, why, explain | a `shared_ptr` cycle never reaches count 0; LeakSanitizer reports 64 bytes in 2 allocations; `weak_ptr` breaks it | correct | run l9 s7 (two checks) |
| screens[8] prose, key, why[delete/clear], explain | rule of zero: self-managing members need no destructor | correct | std [class.dtor]/9 (members destroyed after the body); Core Guidelines C.20 |
| screens[9] order o1 to o5, explain | output `open VOD`, `opened`, `hold 100`, `close VOD`, `1 after hold` | correct | run l9 s9 |
| screens[9].widget.lines[3] "`hold`'s parameter dies at its `}`" | when the parameter is destroyed | imprecise | std [expr.call]/4: implementation-defined, at the callee's return or at the end of the enclosing full expression. App build: at the `}` (run-wasm info). g++ and clang on x86-64: after the call, at the end of the statement (run info line). The printed order is the same. Finding 15 |
| screens[10] key, why[value/raw], hints, explain | a growing vector moves its elements, so pointers into it dangle; `vector<unique_ptr<Order>>` keeps each order at one address | correct | std [vector.capacity] (reallocation invalidates references and pointers) |
| summary.ideas, formula, note, trap | restatements | correct | rows above |
| quiz[0] key, why, explain | moved-from `unique_ptr` is null; prints `1 101.5` | correct | run l9 quiz0 |
| quiz[1] key, why, explain | `make_unique<double[]>(3)` zeroes the elements and frees with `delete[]` | correct | std [unique.ptr.create] (value-initialised), [unique.ptr.runtime]; run l9 quiz0 |
| quiz[2] key, why, explain | a raw pointer going out of scope frees nothing | correct | std [basic.stc.dynamic] |
| quiz[3] key, why, explain | `push_back(o)` copies; `std::move(o)` is needed | correct | run l9 quiz3 |

## l10-invariants.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] key −0.2, why, explain | a `struct`'s members are open; nothing checks the value; prints −0.2 | correct | run l10 s0 |
| screens[1] answer, byKey, explain; screens[2] prose, key, why, explain; summary.ideas[0] | `private` and `public`; a `struct` differs from a `class` only in default access; the compiler refuses the name `bid_` outside the class; clang text; Python's `_name` is a convention | correct | std [class.access], [class] (default access; also default base access); run l10 s2 |
| screens[3] prose, solution, tests, byKey, explain | the initialiser list builds members before the body; the body checks; `this` points at the object | correct | std [class.base.init]/13, [class.this] |
| screens[3].question "A failed check may `throw` or call `std::abort()`" | how a refused construction is reported in this app | correct | `docs/AUTHORING.md` `compare: "raises"`: an uncaught exception or `abort` ends the run abnormally |
| screens[4] key 11.5, wrong 11, 12, byKey, explain; summary.formula; quiz[3] key 5.2, wrong 5.5, 6 | weighted average price: (100 × 10 + 300 × 12) / 400 | correct | run l10 s5; average-cost convention |
| screens[5] prose "A buy moves the average; a sale does not", solution, tests, byKey.test-2/4/6/8, explain | average-cost position keeping; refuse before changing | correct | average-cost method (IAS 2 weighted average cost); run l10 s5 |
| screens[5].byKey.test-9 "the average becomes 0/0, which is NaN" | buy of 0 shares into a flat position | correct | run l10 s5 (isnan is 1) |
| screens[6] canvas, key, why[body/this/local], explain | a `const` member can only be initialised in the list; clang texts; a local of the same name leaves the first error | correct | std [class.base.init]/9, [dcl.init]; run l10 s6 (three checks) |
| screens[7] key −0.2, why, explain; summary.trap | a setter that stores without checking breaks the invariant | correct | hand trace; run l10 s0 (same arithmetic) |
| screens[8] prose (invariant: "a fact about the members that holds whenever outside code can look"), key, why, explain | where an invariant is kept; a `const` function cannot break it | correct | Core Guidelines C.2, C.40; std [class.this] (`mutable` and `const_cast` aside) |
| screens[9] prose, solution, tests, byKey, explain (state machine) | `enum class`; only `new` has transitions out | correct | std [dcl.enum]; hand trace of the tests |
| screens[9].explain "Exchange gateways rely on this: a late fill on a cancelled order really happens, and must be caught, not booked" | industry remark | unverified | no source. A fill that crosses a pending cancel request is normally a valid trade that must be booked, so the sentence needs a source or a narrower wording |
| summary.ideas[1..2] | restatements | correct | rows above |
| quiz[0] key, why, explain | a getter returning `double&` lets the caller write the private member | correct | std [dcl.ref]; same arithmetic as run l10 s0 |
| quiz[1] key `-0.19999999999998863`, why | Python output | correct | CPython 3.13: `100.4 - 100.6` |
| quiz[2] key, why, explain clang text | a `const Quote&` calls only `const` functions | correct | run l6 s3 (same diagnostic) |

## l11-creation-destruction.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] order, byKey, explain; screens[1] answer l6, byKey, explain; screens[2] order, byKey, explain; summary.formula | objects are destroyed in reverse order of construction, at the closing brace of their scope, whether used or not | correct | std [stmt.dcl]/2, [stmt.jump]/2; run l11 s0 |
| screens[0].explain "Python gives no such promise about when `__del__` runs" | Python lifetime | correct | Python language reference, `object.__del__` |
| screens[3] solution, tests, explain | scopes decide the output; "You never call a destructor yourself" | correct | run l11 s0 (same shape) |
| screens[4] prose, canvas, key, why[twenty/zero/error], explain | members are built in declaration order; clang `-Wall` gives both warnings; reading the unset `int` is undefined | correct | std [class.base.init]/13.3, [dcl.init]; run l11 s4 (two checks) |
| screens[5] key 2, wrong 1, 3, byKey, explain | `Logger b = a;` runs the implicit copy constructor; two destructors | correct | std [class.copy.ctor]; run l11 s5 |
| screens[6] prose, answer r1, r2, byKey, explain table | copy construction, copy assignment, move construction, move assignment | correct | std [dcl.init], [class.copy.assign]; `std::move` is a cast, [forward] |
| screens[7] prose "Declare one special member and the compiler may stop writing the others" | implicit special members | correct | std [class.copy.ctor], [class.copy.assign] |
| screens[7] solution, tests, byKey.test-2/5/12 | default copy and move of a vector member | correct | run l11 s7 (test-12 case prints 133) |
| screens[7].byKey.test-9 "A declared move constructor deletes the copy assignment" | implicit deletion | correct | std [class.copy.assign]; run l11 s7 |
| screens[7].byKey.test-10 "A declared copy constructor stops the compiler writing the move assignment" as the reason test 10 (`is_move_assignable`) fails | feedback names the cause of the failure | wrong | run l11 s7: with only a copy constructor declared, `is_move_assignable_v` is 1 (the implicit copy assignment takes the rvalue), so test 10 passes. Test 10 can be the first failure only when move assignment is deleted. Finding 3 |
| screens[7] canvas rows, explain "A moved-from vector is empty; for most other types the standard promises only a valid, unspecified state" | state of a moved-from vector | imprecise | std [lib.types.movedfrom], and [container.requirements.general]: after move assignment (the canvas row `b = std::move(a);` and hidden test 12) the source is only "valid but unspecified" (cppreference, `vector::operator=` (2)); emptiness is assured only after move construction. Empty in practice in both cases (run, run-wasm). Finding 16 |
| screens[8] key, why[deep/noctor/leak], explain | default copy of a raw owning pointer: both destructors `delete[]` one block, undefined | correct | std [expr.delete]/2 (double delete); run l11 s8 (ASan double-free) |
| screens[9] prose, key, why, explain; summary.ideas[2] | rule of zero against rule of five; a `unique_ptr` member makes the class move-only | correct | Core Guidelines C.20, C.21; run l11 s9 |
| screens[10] solution, tests, byKey, explain | move constructor leaves the source closed; copying deleted | correct | author tests; std [class.copy.ctor] |
| summary.ideas[0] "A temporary dies at the end of its full expression" | temporary lifetime | correct | std [class.temporary]/4 |
| summary.ideas[1], trap | restatements | correct | rows above |
| quiz[0] key, why, explain | `Logger("tmp");` is destroyed at the semicolon | correct | run l11 s5 |
| quiz[1] key 3, why, explain | `std::move` of a `const` object copies | correct | std [over.match.best]; run l11 quiz1 |
| quiz[2] key 0, why[one/two], explain "The compiler usually builds `grid` directly in `g`'s place; if not, it moves it" | return of a local | correct | std [class.copy.elision]/1, /3; run l5 s8 |
| quiz[2].feedback.correct "Returning a local by value never copies it" | "never" claim | imprecise | run: `return up ? a : b;` copies (1 copy), because the operand is not the name of a local ([class.copy.elision]/3); a `const` local or a type with no move constructor is copied too. Finding 4 |
| quiz[3] key, why, explain | declaration order, not list order; destruction reverses it | correct | run l11 quiz3 |

## l12-operators.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] canvas, key, why, explain; summary.formula | `fee + tax` needs an `operator+`; clang text; C++ spells `__add__` as `operator+` | correct | std [over.oper], [over.match.oper]; run l12 s0 |
| screens[1] answer r1, r2, r3, r5, byKey, explain | `to_string(p / 100) + "." + to_string(p % 100)` table: `£12.5`, `£12.0`, `£0.7`, `£-1.-50`; division and remainder round towards zero | correct | std [expr.mul]/4; run l12 s1 |
| screens[2] prose, solution, tests, byKey, explain | arithmetic operators return a new value; `str()` formats the absolute value; `£` is two bytes in UTF-8 | correct | run l12 s2; U+00A3 encodes as C2 A3 |
| screens[3] canvas, key, why, explain; summary.ideas[1] | a member operator has the object on the left; `3 * fee` needs a free function | correct | std [over.match.oper]; run l12 s3 |
| screens[4] prose, key, why, explain; summary.note; quiz[2] key, why, explain; review-3 items[2] | `operator<<` takes and returns `std::ostream&`; a stream cannot be copied | correct | std [ostream.cons] (copy constructor deleted); run l12 s4 |
| screens[5] key `1250 1250`, why, explain; summary.trap | a `+` that takes `Money&` writes into the left operand | correct | run l12 s5 |
| screens[6] key 0, why, explain | `0.1 + 0.2 == 0.3` is false; store whole pence | correct | run l12 s6 |
| screens[7] prose, solution, tests, byKey.test-5/7, explain | `std::sort` uses `<`, which must be strict; `==` should agree with it | correct | std [alg.sorting] (strict weak ordering) |
| screens[8] key, why[mut/void/unary] | shapes of the operators | correct | std [over.binary], [over.unary] |
| screens[9] prose, solution, tests, byKey, explain | price-time priority; `std::tie` compares field by field | correct | std [tuple.rel]; run l12 s9. Price-time priority is the standard rule of order-driven markets (Harris, *Trading and Exchanges*, ch. 6) |
| screens[9].explain "A matching engine's queue is exactly this order, kept by a sorted container" | industry remark | unverified | no source; many engines keep a FIFO queue per price level |
| summary.ideas[0] | restatement | correct | rows above |
| summary.ideas[2] "compare whole pence, never doubles" | comparison rule | imprecise | `<` on doubles orders them correctly (run l12 summary check, and l13's own `max_of` over doubles); the trap shown on screens[6] is `==`. Finding 17 |
| quiz[0] key `000`, why, explain | `<` and `==` on different fields disagree | correct | run l12 s6 |
| quiz[1] key, why, explain | no `operator+` for `Pnl` and `Quantity`; wrapper types make units part of the type | correct | run l12 quiz1 |
| quiz[3] key `-£7.50`, why | −375 × 2 formatted | correct | run l12 s2 |

## l13-templates.json

| path | claim | verdict | basis |
|---|---|---|---|
| screens[0] answer l6, l7, l8, byKey, explain | the two functions differ only where the element type is named | correct | reading of the listing |
| screens[1] prose, answer i, d, s, byKey, explain; summary.ideas[0], formula; quiz[1] key 3, wrong 4, 1; review-3 items[3] | one instantiation per type used, at compile time; none for unused types | correct | std [temp.inst] |
| screens[2] prose, solution, tests, byKey.test-2/7, explain; quiz[3] | `T{}` is 0 for numbers and `""` for a string; `+=` adds or joins | correct | std [dcl.init] (value-initialisation); run l13 quiz0 check |
| screens[3] canvas, key, why[same/int/two], explain; summary.ideas[1] | every argument must deduce the same `T`; naming `T` stops deduction; clang note text | correct | std [temp.deduct.call], [temp.deduct]; run l13 s3 (three checks) |
| screens[4] prose "compiled again for every type you sort", answer l5, l20, byKey, explain | read the first `error:` and the line that names your file | correct | std [temp.inst]; the diagnostic shape matches libc++ (run l13 s5 gives the same "invalid operands" form) |
| screens[4].prose "The real message runs to 359 lines" | length of the clang and libc++ output | unverified | no local libc++ outside the app; the app itself caps errors with `-ferror-limit=10` |
| screens[5] key, why, explain; summary.ideas[1] | a class template's member function is instantiated only when used; `Series<std::string>` builds until `mean()` is called | correct | std [temp.inst]; run l13 s5 (two checks) |
| screens[6] key 2000, why[exact/round/error], explain | `T mean()` with `T = int`: 4001 / 2 is 2000; a negative total becomes a huge unsigned number before the division; return `double` | correct | std [expr]/11.5.3; run l13 s6 (2000; the unsigned quotient is huge), run-wasm (2147483645 in the app) |
| screens[7] prose, key 12345, wrong 123, 1.2345, explain | a number as a template parameter; `FixedPoint<2>` and `FixedPoint<4>` are different types; `std::array<double, 5>` | correct | std [temp.param], [array.overview] |
| screens[8] prose, key, why, explain "with no run-time cost" | `std::vector<double>` and `std::vector<int>` are two classes from one template; no run-time type check | correct | std [temp.spec]; "no run-time cost" read as no run-time dispatch |
| screens[9] solution, tests, byKey, explain | rolling window; erasing the front shifts the rest | correct | run l13 s9; std [vector.modifiers] (linear in the elements after the erased one) |
| summary.ideas[2], trap | restatements | correct | rows above |
| quiz[0] key `"VOD"` | maximum of the four tickers under `<` | correct | run l13 quiz0 |
| quiz[0] why[long] "V comes after L", why[error] "`std::string` has `<`, alphabetical order", feedback, explain "compares alphabetically" | meaning of `<` on strings | imprecise | std [string.operators] with [char.traits.specializations.char]: lexicographic by character code, so every capital sorts before every lower-case letter ("Zebra" < "apple", run l13 quiz0 check). True for these all-capital tickers only. Finding 5 |
| quiz[2] key, why, explain, feedback | a template defined only in `stats.cpp` gives an undefined reference; put template definitions in the header | correct | std [temp] (definition must be visible at the point of instantiation); run l13 quiz2. The missing link to level 1's one-body rule is finding 10 |

## review-1.json

| path | claim | verdict | basis |
|---|---|---|---|
| items[0] key, why, explain | a warning does not stop the build | correct | run l1 s7 |
| items[1] key 0, wrong 0.75, explain | `double share = qty / lots;` is 0 | correct | run l2 quiz0 |
| items[2] key 4, wrong 7, 5 | `i` takes 3, 5, 7, 9 | correct | run l3 quiz3 check |
| items[3] key (undef, multi), why, explain | which messages come from the linker | correct | run l4 s7, l4 quiz2, l1 s6, l4 s0 |
| items[4] key −1294967296 ("in practice"), wrong 3000000000, 2147483647, 1294967296, byKey, explain | 3,000,000,000 − 2^32 | correct | run l2 s1 (`-fwrapv`); the question says "in practice" |
| items[5] solution, tests, byKey | strictly below `-limit` | correct | hand check of the five tests |
| items[6] key, why | `annualise()` does not compile; `annualise(1)` converts the `int` | correct | std [dcl.fct.default], [conv.fpint] |
| items[7] key −2, wrong −3, −2.25, 2, byKey, explain | `-9 / 4` truncates to −2; Python floors to −3 | correct | run l2 s0 |

## review-2.json

| path | claim | verdict | basis |
|---|---|---|---|
| items[0] key, why, explain | swap by value changes copies only | correct | std [expr.call]/4 |
| items[1] key (size, read, copy), why[push] | what compiles through a `const` reference | correct | std [vector.capacity], [vector.modifiers] (`push_back` is not `const`) |
| items[2] key 80, wrong 5, 40, explain 0x4050 | 5 × 16 bytes | correct | run l7 s0 (sizeof(Level) 16); 0x50 = 80 |
| items[3] key (local, twice), why[zero/at], explain | dead-local read and double delete are undefined; `new double[0]` and `at` are defined; ASan says "double-free" | correct | std [basic.life], [expr.delete]/4, [sequence.reqmts]; run review-2 r-which-ub |
| items[4] key 6, wrong 5, 4 | `main` plus `depth(4)` to `depth(0)` | correct | count (before any inlining) |
| items[5] key, why, explain | a vector of `unique_ptr` deletes its positions at the inner brace | correct | std [vector.cons] destructor, [unique.ptr.single.dtor] |
| items[6] solution, tests, explain | `balances` by `&`, `rates` by `const&`; 100 × 1.1 × 1.1 = 121 | correct | arithmetic; a temporary binds only to `const&` |
| items[7] key, why | readers are `const`; the `const` on a parameter is about the argument | correct | std [class.this] |

## review-3.json

| path | claim | verdict | basis |
|---|---|---|---|
| items[0] key, why[after/none/wrongside], explain | check before storing; `a >= bid_` refuses every valid ask and accepts every crossed one | correct | case check: valid means a > bid, refused; crossed means a < bid, accepted |
| items[1] order, byKey, explain | members in declaration order, then the body; destructor body, then members in reverse | correct | std [class.base.init]/13, [class.dtor]/9; run l11 quiz3 check |
| items[2] key, why | `operator<<` signature; as a member the `Quote` would be on the left | correct | run l12 s4; std [over.match.oper] |
| items[4] solution, tests, explain | refuse a negative limit in both doors; `allows` checks both sides | correct | hand check of the tests |
| items[5] solution, tests, explain | `+` refuses mixed currencies; `==` compares both fields | correct | hand check |
| items[6] key, why[copy/assign/constmove], explain | a `unique_ptr` member: moves only; moving from `const` asks for the deleted copy | correct | run l11 s9 |
| items[7] solution, tests, explain | sort, reverse, resize when `n` is smaller; by-value parameter leaves the caller's vector | correct | hand check; tickers are all capitals, so VOD, LLOY |
| items[8] key, why[both/ask/price] | bids: `std::tie(b.price, a.time) < std::tie(a.price, b.time)` | correct | run review-3 r-bid-priority (D, C, A, B) |

## homework-1.json

| path | claim | verdict | basis |
|---|---|---|---|
| items[0] order, same, explain | two compiles in either order, one link, then run | correct | separate compilation |
| items[1] prose, solution, tests, byKey, explain | `getline`, `find`, `std::stod`; skip lines without a comma; `std::stod` throws on non-numeric text; 24.00% and 25.00% | correct | std [string.conversions]; run homework-1 h-csv-drawdown |
| items[2] solution, tests, byKey | strict `<` and `>` leave the edges to hold | correct | hand check; the edge values are exact in binary |
| items[3] solution, tests, byKey, explain | each `int` fill converts to `long long` before adding | correct | std [expr]/11 |
| items[4] prose g++ text, key, why, explain | comparing `int` with `size()` converts the `int` to unsigned; a negative `int` turns huge | correct | std [expr]/11.5.3; run homework-1 h-signedness |
| items[5] key 28, wrong 29, explain | `0.29 * 100` is 28.999999999999996; `std::lround` gives 29 | correct | run l2 s7 |
| items[6].model (volume, average, why Python hid both, fixes, unit tests, `-fsanitize=undefined`), rubric[0..4] | wrap by 2^32, "Signed overflow is undefined behaviour"; integer division before the conversion; `(double)(a / b)` does not help | correct | run l2 s1, homework-1 h-port-note (UBSan reports the overflow) |
| items[6].model "Building with `-Wall -Wconversion` also flags the implicit conversions"; rubric[5] "or warning and sanitiser flags" | a compiler warning catches these two bugs | wrong | run homework-1 h-port-note: g++ 13 and clang 18 print nothing for the snippet with `-Wall -Wconversion` (nor with `-Wextra`, nor clang `-Weverything`, probe): `int` to `double` loses nothing, and the overflow involves no conversion. Finding 1 |
| items[7] key, why[guard/one/order], explain | one body in one `.cpp`, or `inline` | correct | run l4 s7 |
| items[8] prose (tick rule), solution, tests, explain | uptick +1, downtick −1, zero tick keeps the last sign, first trade 0; total in `long long` | correct | tick test of Lee and Ready (1991), *Journal of Finance* 46(2); run homework-1 h-tick-rule (all keys, including 8970232795) |

## homework-2.json

| path | claim | verdict | basis |
|---|---|---|---|
| items[0] solution, tests, byKey.test-1, explain | `Position& p` in the inner loop; £275 spent | correct | −370 + 95 = −275 |
| items[1] solution, tests, byKey.test-4, explain | VWAP = Σ qty × px / Σ qty; 121,485 / 1,200 = 101.2375 | correct | run homework-2 check; standard definition |
| items[2] order, explain "In one `+` expression the two calls could run in either order; two lines fix it" | frames; evaluation order of operands | correct | std [intro.execution] (operands unsequenced; function calls not interleaved); run (prints 7.5) |
| items[3] key (bid, depth), why | which methods are `const` | correct | as review-2 items[7] |
| items[4] key 40.08, wrong 40, 0.004008, 40080000 | 10,000 × 501 × 8 bytes | correct | arithmetic |
| items[5] key (null, mismatch, twice), why[at/zero], explain | which snippets are undefined; ASan names SEGV, alloc-dealloc-mismatch, double-free | correct | run l7 quiz0, l8 s5, review-2 r-which-ub |
| items[6] key, why, explain | `push_back` on a full vector reallocates; `first` dangles; ASan heap-use-after-free | correct | std [vector.capacity], [vector.modifiers]; run homework-2 h-realloc |
| items[6].explain "in this browser it printed 2.93699e-306" | stray value in the app | unverified | run-wasm info line printed 2.8974e-306 here: a stray number of that kind, not that number |
| items[7].model (a) to (e), rubric | by-value copy; `<=` reads past the end, undefined, "vector[] index out of bounds" in the app; `&best` dangles; `add_fee` changes a copy; raw owning pointer against `unique_ptr`; `std::optional` | correct | run-wasm l3 s6; run l7 quiz2; rows of l5, l7, l9 |

## homework-3.json

| path | claim | verdict | basis |
|---|---|---|---|
| items[0] order, byKey, explain | the temporary dies at its semicolon; named objects at their braces | correct | run l11 s5 |
| items[1] key 52.25, wrong 51.7143, 53 | (150 × 51 + 50 × 56) / 200 | correct | run l10 s5 (52.25); 18100 / 350 = 51.714 |
| items[2] solution, tests, explain | sale P&L = q (p − average); realised total £300 | correct | 150 × 4 − 150 × 2 = 300; average-cost method |
| items[3] solution, tests, explain | `Fixed<Places>`: a different `Places` is a different type, so `+` on mixed types does not compile | correct | std [temp.type], [temp.deduct.call] |
| items[4] key, why[default/nodtor/constptr], explain | a vector member makes the copy safe | correct | run l11 s8 and rows of l11 |
| items[5] solution, tests, explain | book invariant; `std::sort` with `operator<`, reversed for bids | correct | hand check of the tests |
| items[6].model (a) to (e), rubric | invariants, rule of zero, `operator<<`, money in integer pence, throw before changing | correct | rows of l10 to l12 |
| items[7] spec, solution, tests, explain | `SessionRange<T>`: `+=` returns `*this` by reference, `+` works on a copy, `width` through `double` is exact for `int` ends | correct | run homework-3 h-session-range; a double holds every integer up to 2^53 |
