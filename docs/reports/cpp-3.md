# cpp level 3 ("Classes"): report

## Files written

All in `app/content/courses/cpp/`. Lesson ids, names, objectives and skills follow `course.json` (`cp-classes` throughout; `cp-references` and `cp-memory` where a lesson leans on level 2). Money is in £, prices and P&L in integer pence wherever they are compared, and every `how` warns about the first compiler load (about 26 MB; first compile 10 to 15 s, later 1 to 3 s).

- `l10-invariants.json`: 10 screens, 4 quiz items, skills `cp-classes`, `cp-references`.
  - Hook: a public `struct Quote` crossed by a typo (prints `-0.2`, nothing objects). Explore: drag members of `Quote` into "only Quote's own functions" or "any code" (`boxes`). Name: the clang `'bid_' is a private member` error (`pair` of source and terminal), with the Python `_bid` contrast.
  - Code: `class Quote` with a checked constructor, `mid() const`, `spread() const` (6 tests; a crossed quote and a locked quote, bid equal to ask, are refused: decided and said on the screen). Weighted average by hand (`numeric`), then `Position::buy`/`sell` (10 tests: weighted average, sale leaves the average, flat position resets to 0, no shorts, no zero-share buy).
  - Initialiser list taught through the real `const` member error; trap: a setter that skips the check (failing version beside the fix); generalise: the four places an invariant is kept.
  - Transfer: an order state machine (`graph`): new, filled, cancelled; no fill on a cancelled order, no overfill (11 tests). Quiz: non-const reference getter, Python underscore, non-`const` method on a `const&`, weighted average after a sale.
- `l11-creation-destruction.json`: 11 screens, 4 quiz items, skills `cp-classes`, `cp-memory`.
  - Order the `open`/`close` messages of a `Logger` (reverse construction), tap the brace where `b` dies, order a two-scope program (edge case: `c` is never used and still closes), then produce that order in a script-mode program (4 stdin runs, one exact).
  - Declaration-order initialisation through clang's `-Wreorder-ctor` and `-Wuninitialized` warnings; an implicit copy constructor (two `close a` lines); a `table` tap of which lines run the copy constructor against copy assignment, move constructor and move assignment.
  - Code: `Buffer` owning `std::vector<double>` with `= default` copy and move (8 tests: deep copy, moved-from source empty, a million-double move, `std::is_copy_constructible_v`).
  - Trap: a raw-pointer class with the default copy (double delete) on a `graph`; generalise: rule of zero against rule of five.
  - Transfer: a market-data `Connection` with deleted copy and a move constructor that leaves the source closed; a hidden counter checks each venue is disconnected exactly once, and two tests ask the type traits whether it can be copied or moved (9 tests).
  - Quiz: a temporary dies at its semicolon, `std::move` on a `const` object copies, a lattice returned from a factory is never copied, members open in declaration order.
- `l12-operators.json`: 10 screens, 4 quiz items, skills `cp-classes`, `cp-references`.
  - Hook: `fee + tax` does not build (`__add__` against `operator+`). Explore: tap the pence values a naive `str()` prints wrongly (1205, 1200, 7 and −150).
  - Code: `Money::str()` (`£12.34`, `-£1.50`), `operator+`, `operator*(Money, int)` (11 tests, edge case negative money).
  - Member against free (`3 * fee`), `operator<<` taking and returning `std::ostream&`, trap: a `+` that mutates its left operand, `==` on doubles (`0.1 + 0.2`).
  - Code: `operator<` and a consistent `operator==` for `Price` in pence, tested by a hidden `std::sort` (8 tests).
  - Transfer: price-time priority for resting asks with `std::tie`, tested by sorting a small book (7 tests). Quiz: `<` disagreeing with `==`, `Pnl + Quantity` refused at compile time, `std::ostream` by value, negative money times 2.
- `l13-templates.json`: 10 screens, 4 quiz items, skill `cp-classes`.
  - Hook: tap the lines that differ between `int` and `double` versions of `max_of`. Explore: tap the instantiations a program needs on a `graph` (int, double, string; not char or long).
  - Code: `sum_of<T>` with `T{}` (7 tests over `int`, `double`, `long long`, `std::string`; edge case empty vector).
  - Deduction conflict (`bigger(3, 2.5)`), the real 359-line `std::sort` error on `Quote` (tap the first `error:` and the `main.cpp` note), a class template whose `mean` is never compiled for `std::string` (edge case), trap: `T mean()` on `Series<int>` gives 2000 for 4001 / 2, and `FixedPoint<4>` as a non-type parameter.
  - Generalise: function, class and number templates, `auto` and `decltype` in one sentence, the standard library as templates.
  - Transfer: `Window<T>` rolling mean for prices and volumes (9 tests, empty window and size 0 refused). Quiz: maximum of tickers, instantiation count, template defined in a `.cpp` (link error), empty sums.
- `review-3.json`: 9 items, difficulty 2 to 4, all four lessons: `set_ask` drafts, member and constructor order (`order`), `operator<<` signature, instantiation count, a `RiskLimit` that cannot be set negative (code), `Money` with currencies refusing GBP + USD (code, `raises`), a move-only `Pricer`, a `top_n<T>` template (code), bid-side price-time `std::tie`.
- `homework-3.json`: 7 items, difficulty 3 to 5.
  - `order`: messages of a nested scope with a temporary. `numeric`: average price through buys and a sale.
  - Code: `Position` with realised P&L (difficulty 4, 10 tests), `Fixed<Places>` with `str()` and `operator+` (difficulty 4, 8 tests), and the difficulty-5 `Book`: `Level` with `operator<`, `add` merging and sorting levels, `best_bid`, `best_ask`, `spread`, `depth`, `size_at`, and a no-crossing invariant (15 tests, five `raises`).
  - A choice on fixing the raw-pointer class, and a difficulty-5 `longform` design of a desk `Position` class (invariants, special members, operators, money and errors) with a 10-point rubric and a full model answer.

Every C++ expected value was checked twice: natively (g++, a copy of the app's harness taken from `cpp-grade.js`) and by the browser playthrough, which compiles each `solution` with the app's clang 21 runtime and runs every test. Every starter was also run and fails at least one test. Compiler and runtime messages shown in `console` canvases were produced by YoWASP clang 21 with libc++, the app's compiler, run under Node. Generators and checkers are in the scratchpad folder `cpp-3`.

## Validator

`node app/tools/validate.mjs`: 0 errors overall. My files carry 7 warnings, all on homework item `h-fixed`: `Fixed::str()` returns text such as `"12.34"`, which the validator mistakes for a number written in quotes. They are false positives (see the backlog inbox).

## Playthrough

`node app/tools/playthrough.mjs --local-cdn <scratchpad>/pkgs --shots <scratchpad>/cpp-3/shots`:

- `cpp/l10-invariants`: ok, 14 checks, quiz 4/4.
- `cpp/l11-creation-destruction`: ok, 15 checks, quiz 4/4.
- `cpp/l12-operators`: ok, 14 checks, quiz 4/4, after a fix. Screen 8 at first failed with key `compile` when played after other lessons. The cause is a runtime bug: once a precompiled header exists for the leading includes, an `#include` later in the unit (here in the postlude) fails with "cannot open file ... Out of memory". The fix was to move the postlude's `<algorithm>` and `<vector>` into the prelude's leading includes. Every level 3 widget was then recompiled under a PCH in Node, and all compile.
- `cpp/review-3`: ok, 9 of 9 recorded. `cpp/homework-3`: ok, 7 of 7 marked right, 33 of 33 marks.

Screenshots of every screen and item were checked. Changes made from them: the explore cards in l10 were reflowed and shortened, the state-machine nodes became pills so "cancelled" is not cut off, and l12's question now says the expected minus sign is a plain `-` (the table shows a typographic minus).

## Proposed change to course.json

None.

## Engine and runtime limitations

Six bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (cpp level 3):": the PCH include bug, the validator's numeric-text warning, no `catch`, no compile-must-fail case, `boxes` card widths for code labels, and no `-Wall` for learner code.
