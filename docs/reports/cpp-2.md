# cpp level 2 ("References and memory"): report

## Files written

All in `app/content/courses/cpp/`. Lesson ids, names, objectives and skills follow `course.json`. Money is in £, and every `how` warns about the first compiler load (about 26 MB, 10 to 15 s for the first compile, 1 to 3 s after).

- `l5-value-or-reference.json`: 11 screens, 4 quiz items, skills `cp-references` and `cp-basics`.
  - Canvases: a Python console as the contrast, a `boxes` drag of names onto objects, `graph` names-and-objects, and a `table` of copy cost against size, measured in this browser (about 1 ms to copy a million doubles).
  - Code: `total_value(const&, const&)`, with a hidden `static_assert` on the signature, and a fix of `normalise` that is missing its `&`.
  - Also: a `swap` derive, and a risk-engine transfer.
- `l6-const.json`: 12 screens, 4 quiz items, skill `cp-references`.
  - Screens: a `const` reassignment with the clang error, a tap on the lines that break a `const&` promise, why a plain `&` rejects temporaries and `const` objects, `const` objects and methods, and `constexpr` against `const`.
  - Code: `spread(const Quote&)`, with a hidden `Quote` that has `const` getters, and a fix that copies before changing a `const&`.
  - The trap shows `const` is a view, not a freeze. Also: a right-to-left reading derive, the `const` pointer table and a market-data callback transfer.
- `l7-addresses.json`: 10 screens, 4 quiz items, skills `cp-memory` and `cp-references`.
  - Screens: `&` and `*`, pointer arithmetic on an `array` and a `number-line` of addresses, and an order derive of `*(p + 2)`.
  - Code: `bump(int*)`. Its null test reads address 0, because a null write does not crash here. Also `max_via_pointer(begin, end)`, called through a hidden `max_of(vector)`.
  - Undefined behaviour: the use-after-scope trap ("it printed 101.25"), then a `console` of real AddressSanitizer output to read.
  - Also: a C-SDK pointer-pair transfer.
- `l8-stack-and-heap.json`: 11 screens, 4 quiz items, skill `cp-memory`.
  - Screens: a 16 MB local array overflowing the 8 MB stack against a vector, and the call stack stepped frame by frame (`manipulate` on an `array` stack).
  - Then: `new` on a `graph` with stack and heap lanes, a stack-or-heap `table` to fill, a LeakSanitizer `console`, and the `delete`/`delete[]` trap.
  - Code: a script-mode `new double[n]` sum and a function-mode `read_ticks` built from a C-style buffer. Both have a hidden leak checker: counting `operator new[]`/`delete[]`, with exit status 1 at exit.
  - Also: a lifetime order derive, and a pricer-lattice transfer.
- `l9-owning-memory.json`: 11 screens, 4 quiz items, skill `cp-memory`.
  - Screens: destructor timing, a tap on the leaking returns, and RAII with a vector.
  - Code: convert to `make_unique`, where a hidden `Book::live` counter must reach 0 on the capped path. Also `open_position` returning a `unique_ptr`, tested through `->`, including the moved-from null.
  - Also: the `unique_ptr` copy error read from clang, the `shared_ptr` count, the cycle-leak trap, the rule of zero, an order derive of a `unique_ptr` through a call, and an order-book ownership transfer.
- `review-2.json`: 8 items, difficulty 2 to 4, covering all five lessons; one is a code item (`accrue`).
- `homework-2.json`: 8 items, difficulty 3 to 5.
  - Code: `apply_fills(std::vector<Position>&, const std::vector<Fill>&)` at difficulty 4, and a difficulty-5 VWAP script. The script reads orders from stdin into a vector, skips cancels and prints `QTY` and `VWAP` to 4 decimals or `n/a`. One test has 2.5 billion shares, and `vwap` must take `const std::vector<Order>&` (`static_assert`).
  - One `order` item: the stack frames of a nested option-pricing call.
  - Others: `const` methods, leak MB, which snippets are undefined behaviour, and a reference invalidated by `push_back`.
  - One difficulty-5 `longform` review of a colleague's signatures and ownership, with a 10-point rubric and a full model answer.

Every expected value in a C++ test came from running the solution through the app's own harness. I used `cpp-grade.js` `unit()` with a Node copy of `cpp-worker.js`: same flags, runtime and WASI shim; scripts are in my scratchpad folder `cpp-2`. Each starter was also run, and each fails at least one test. The browser playthrough then ran every solution a second time.

## Validator

`node app/tools/validate.mjs`: 0 errors in my files. There are 6 warnings in them:

- 4 ladder screens that change canvas kind.
- 2 point hints whose canvas has nothing useful to highlight.

The remaining warnings, and 1 error (in `stat-learning/l8-setting-to-zero.json`), belong to other courses.

## Playthrough

Run with `--local-cdn …/scratchpad/pkgs`, after the last edit. Every check passed and there were no console errors.

| File | Checks | Quiz or marks | Time |
|---|---|---|---|
| l5-value-or-reference | 15 | quiz 4/4 | 147 s, including the compiler load |
| l6-const | 16 | quiz 4/4 | 33 s |
| l7-addresses | 14 | quiz 4/4 | 21 s |
| l8-stack-and-heap | 15 | quiz 4/4 | 39 s |
| l9-owning-memory | 15 | quiz 4/4 | 55 s |
| review-2 | 8 of 8 | | |
| homework-2 | 8 of 8 | 37 of 37 marks | |

I read the screenshots, with Why? sheets, and fixed what they showed:

- Squashed `graph` drawings: I now set `nodeRadius` 20 and `height` 220 to 240.
- Sanitiser, clang and leak-report lines that scrolled off the column: I trimmed them to about 54 characters and say so in the prose.
- An `-fsanitize` flag that wrapped at its hyphen.
- The l8 hook's wording on the stack, and its code. The code now fills and prints, so the array cannot be optimised away; I re-verified the crash in the browser runtime and natively.
- A long starter comment in the VWAP item.

## course.json

No change proposed.

## What the runtime did for each undefined-behaviour probe

All runs used the app's flags: `-O1` with libc++ debug hardening, wasm32 with `--stack-first` and an 8 MB stack.

| Probe | What happened |
|---|---|
| `*nullptr` read | No trap. It returned the int at address 0 (1 in one run, 0 in another). |
| Null write | No trap. The write succeeded. |
| Null dereference that clang can see after inlining, or `*` on an empty `unique_ptr` | Trap ("unreachable"). The same code behind a non-inlined call returned 0. |
| Pointer or reference to a dead local, or a use-after-scope | Stale 101.25. After another call reused the slot, 7. clang warns `-Wreturn-stack-address`. |
| Use after `delete` | Stale 101.25. |
| Double `delete`, `delete[]` twice, or `delete` of a stack object | Silent, exit status 0. |
| `delete` on memory from `new[]` | Silent at run time; clang warns `-Wmismatched-new-delete`. |
| Leak | Silent. |
| Reference into a vector after a reallocating `push_back` | Printed 2.93699e-306. |
| Raw array read out of bounds | Garbage (1.67792e+243). |
| `std::vector[]` out of bounds | Libc++ hardening trap, deterministic. |
| `std::vector::at` out of bounds | Uncaught `std::out_of_range`, deterministic. |
| Failed `assert` | Deterministic crash. |
| A 16 MB local array | "memory access out of bounds", deterministic. A 1,000,000-double (8 MB) local array fits. |
| Recursion 10,000,000 deep, frames with a local buffer | "call stack exhausted". |

The lessons therefore teach undefined behaviour as "the compiler may do anything; the browser build is forgiving; a desk build is not". They show real g++ `-fsanitize=address` output captured on Linux in `console` canvases:

- stack-use-after-scope, heap-use-after-free and double-free;
- alloc-dealloc-mismatch and bad-free;
- SEGV on address 0;
- LeakSanitizer, including the `shared_ptr` cycle.

`compare: "raises"` is not used for any undefined behaviour. Leaks and `delete`/`delete[]` mismatches are tested through the hidden counting allocator instead.

## Engine and runtime limitations

These are 8 bullets under "Raised later (cpp level 2):" in `docs/BACKLOG-INBOX.md`:

- no sanitiser, so undefined behaviour never traps;
- crashes from undefined behaviour depend on inlining;
- 4-byte pointers;
- no built-in leak check;
- no signature check;
- `graph` padding tied to `nodeRadius`;
- `manipulate` not accepted on explore screens;
- no wrapping in `console` lines.
