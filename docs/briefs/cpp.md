Levels 1 to 4 of `cpp` predate briefs; this file starts at level 5.

## Level 5

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `cpp` ("C++ Foundations", topic 1.9), level 5 ("C++ questions at interview"): lessons `l19-moving-not-copying`, `l20-rule-of-five`, `l21-virtual-dispatch`, `l22-undefined-behaviour`, `l23-own-smart-pointer`, plus `review-5.json` and `homework-5.json`, in `app/content/courses/cpp/`.

Follow `docs/LEVEL-BRIEF.md` exactly (read it first) and `docs/AUTHORING.md` in full, including the C++ addendum to section 3 (`code`), `parts`, `longform` and the voice rules. Use the ids, names and objectives in `app/content/courses/cpp/course.json` exactly: the level, its five lessons, `review-5` and `homework-5` are already on the map, so do not edit `course.json`. Skills are the existing `cp-*` ids only (no new skill row, so `topic-1.9.json` needs none): l19 `cp-memory` and `cp-classes`; l20 `cp-classes`; l21 `cp-classes`; l22 `cp-basics` and `cp-memory`; l23 `cp-memory`. Use £ for money. Priority [Should], and [Must] for the developer track (`docs/briefs/interview-plan.md`, "`cpp` level 5").

### Context

- What the learner has. All of `cpp` levels 1 to 4, and `cpp-pricing` l5 and l11 are recommended (the plan lists them as "builds on"). Read these before writing, for voice, harness conventions and, above all, what is already taught so that you extend it and never repeat it:
  - `cpp` l9-owning-memory: `std::unique_ptr`, `std::shared_ptr`, RAII, the rule of zero named, a cycle trap. l23 builds the two pointers from scratch, so do not re-teach what they do; teach how.
  - `cpp` l11-creation-destruction: scopes, constructor and destructor order, the copy and move constructor table, `= default` for four members, a raw-pointer double free (`Prices`, the trap), a `Connection` with a move constructor and a hidden `disconnects` counter in a `prelude`, and "the rule of zero or the rule of five". l19 and l20 are the interview depth on top: when a move happens, what it costs, what the compiler writes, and what to say aloud. Do not re-run the `Prices` double free as a puzzle (cite it: "the l11 bug"); l20 makes the learner write the fix.
  - `cpp` l12-operators and l13-templates: value types with operators, and class templates (`Series<T>`). l23 uses `template <typename T>` classes.
  - `cpp-pricing` l5-payoff-classes: the whole base-class story already told: `class Payoff` with `virtual ~Payoff() = default`, `override`, a trap on a missing `override`, "Copied into the base" (slicing by value), a straddle built from a call and a put, and `const Payoff&` pricers. l21 is the machinery under it (vtable, layout, why slicing happens, why a non-virtual destructor is undefined, what a constructor sees) and a hand-built vtable. Never ask the learner to write `Call` and `Put` as a task again.
  - `cpp-pricing` l11-optimisation-flags: signed overflow is undefined, with `x + 1 < x` giving 1 at `-O0` and 0 at `-O2`. l22 may recall it in one line and must not use `x + 1 < x` as a puzzle. It adds the catalogue, the null check deleted after a dereference, sanitisers, and the learner writing a check that is itself defined.
- Reference text: Meyers, "Effective Modern C++" (items on `std::move`, special member functions and smart pointers) and the C++ Core Guidelines (rules C.20 and C.21 for zero and five, C.35 and C.67 for virtual destructors) as free-to-read guidance; name them once, in l19, by title only. A free online reference such as cppreference.com is named once, in l20. Never quote them.
- Shape of the level. Each lesson follows the interview shape: a puzzle first, the mechanism named by what the learner just did, a ladder, one trap on the misconception candidates blurt, one edge case, a `generalise` that states the rule as a code pattern, a `derive` (`order` with a flawed distractor) where the lesson has a sequence, and a `transfer` that is the follow-up an interviewer asks next, with a desk number. Every lesson has one or two `code` screens with the starter, solution and hidden tests given under "Code problems" below. Quant contexts: a position book, fills, a `Payoff` book, a feed handle, pence as integers, a vector of a million prices.
- Interview framing. Candidates report these as spoken questions: "what does `std::move` do", "when is the move constructor called", "what is the rule of five", "why must a base class destructor be virtual", "what is a vtable", "what is undefined behaviour, give three examples", "write a `unique_ptr`", "implement `shared_ptr`". Name no firm in any screen. Each lesson ends with the sentence the learner could say aloud, in the `generalise` or `transfer` screen, not graded.
- Every code screen below is verified by the scripts in `docs/briefs/cpp-scripts/` (see "Code problems"); copy starters, solutions and tests exactly, then have the app's own checker confirm each (`node tools/playthrough.mjs --lesson cpp/<id> --local-cdn <pkgs>`).

### Runtime facts that bind

- C++ runs in the browser in YoWASP clang 21 (WebAssembly, libc++ in debug hardening, `-std=c++17 -O1`, no exceptions caught, no threads, no sanitisers). Pointers and `size_t` are 4 bytes (wasm32) and 8 on a desktop: say so on any screen that prints or states a size (l19, l21, l22). `double` is aligned to 8 on both.
- Undefined behaviour does not trap and cannot be shown by running it: a null read returns what is at address 0, a dangling read the stale value, and clang may compile code it can see is undefined to `unreachable`. Never use `compare: "raises"` for it. l22 is therefore read-and-judge: every question shows code (and, where it helps, output from a desk machine or the compiler's own assembly) and asks the learner to judge. Say so in l22 screen 1, in one sentence. The one `code` screen in l22 (`add_overflows`) is safe: the learner's solution never overflows, and the starter fails whatever the compiler does with its undefined line (it compares the sum after the addition, which is false under wrap-around and under folding alike). A learner's own post-check solution is another matter: whether it fails depends on the optimiser (it fails 7 of 13 in this app's clang 21 at `-O1`, which folds the check, and passes under g++ 13 at `-O1`), so the hidden tests double as an optimiser test and no failing row is promised for every undefined solution.
- Each hidden test runs as its own process, so a crash fails only that test.
- A test must never rely on reading freed memory, or on the allocator noticing a double free (the app's allocator, wasi dlmalloc, frees twice silently, and `leakCheck` counts only blocks never freed or freed with the wrong form). Every slip is caught by an observation the test makes on live memory: an accessor (`data()` is null), a size, a count (`alloc_count()`, `Tracked::live`, `Counted::live`), or a hidden type that records its own life (`Counted` keeps a table of live addresses and counts a copy or move made from a destroyed source, without reading it). Where no such observation exists the slip is listed as not caught and waits on a [Must] item ("Raised later (cpp L5 brief, 5 Nov)" in `docs/BACKLOG-INBOX.md`): the delete-first assignment of P-copy-samples. Every problem was re-run in the app's own toolchain (clang 21, libc++, the app's `unit()` and `leakCheck`), not only natively; see "Code problems".
- `allocCheck: true` gives `alloc_count()` and `reset_alloc_count()`: a test reads `alloc_count()` as its last expression after `reset_alloc_count()` in its `setup`, so a real move (no allocation) differs from a copy (one). `leakCheck: true` ends a test with exit status 1 if a `new` or `new[]` block is never freed or is freed with the wrong form; the two flags coexist (AUTHORING, C++ addendum). Use `allocCheck` only where a test reads `alloc_count()` (the validator warns otherwise). Each of the nine code problems states its flags under "Code problems".
- A hidden `prelude` type `Tracked` or `Counted` counts live objects, copies and moves with `static inline int` members (C++17). The counters count what happens, so a "move that really copies" is caught by a number, not by reading the code.
- No `try` or `catch`: a `throw` ends the program. l20 mentions the exception-safety reason for "allocate before you delete" in one sentence and says that this app cannot show it.
- Move and growth counts. The standard does not fix the growth rule: libc++ and libstdc++ double the capacity and MSVC grows it by 1.5, so say "this library grows its capacity 1, 2, 4, 8" wherever a count depends on it (l19 S4 and S5, exam `e-vector-growth`). Here `std::vector` grows from capacity 0 to 1, 2, 4, 8 and relocates with `std::move_if_noexcept`: four `push_back(Tracked(i))` do 7 moves and no copy; with a move constructor that is not `noexcept`, two pushes do 1 copy and 2 moves, and four pushes 3 copies and 4 moves. I checked these natively with g++ 13.3 and clang++ 18.1 on libstdc++ (`cpp-scripts/facts_l19.cpp`, `facts_misc.cpp`), with a model (`cpp-scripts/number_checks.py`) and in the app's own toolchain (YoWASP clang 21 with libc++; the second reader's run of `facts_l19.cpp` and `facts_misc.cpp` printed identical counts). Before stating them in a lesson, run `facts_l19.cpp` once through the app's own compiler again (a scratch `code` screen in your scratchpad copy with a `stdout` case) and report any difference. The `Vec` homework item does not depend on the library: it grows by its own rule.
- Sizes on wasm32 were checked with `static_assert` on `clang++ --target=wasm32-unknown-wasi` (`cpp-scripts/wasm_sizes.cpp`): a class with one virtual function and an `int` is 8 bytes (16 on a desktop); two virtual functions add no bytes; a derived class with two more `int`s is 12 (16); `struct Quote { virtual double mid() const; double bid, ask; }` is 24 on both (here 4 for the pointer, 4 of padding, 16; on a desktop 8 and 16).
- The compiler's own output in l22 (`first`, `grows`, `wraps`, `sign`) was produced with `clang++ --target=wasm32-unknown-wasi -O1 -S` (`cpp-scripts/ub_asm.cpp`): `grows` returns `i32.const 1`, `wraps` returns `i32.const 0`, `first` is one `i32.load` and no null test, `sign` returns `i32.const 1` for every input. The sanitiser lines in l22 are from `g++ -fsanitize=undefined` on a desk machine (`cpp-scripts/ub_facts.cpp`); say "on a desk machine, not in this app", and never say what this app's clang 21 prints.
- Engine limits to write around: a `derive` screen takes only `expression`, `order` or `choice`; `longform` is accepted only in homework and exams; `table` widgets and canvases of five or more columns turn compact at 390 px, so a `table` canvas of five columns is the limit, but a `table` widget with editable cells overflows a 390 px phone from the fourth column (`docs/BACKLOG-INBOX.md`), so keep widget tables to four columns with one-word cells and `compact: true`, and check the `--mobile` playthrough; grid and array cell text is plain text; table ids are zero-based (`r0c1`), console line ids one-based (`l1`); set `shuffle: true` on every `choice` and `multi` except ordered options; a `table` cell's own `wrong` id cannot carry a `byKey` line (the validator rejects it, already raised in `docs/BACKLOG-INBOX.md`), so write `byKey` lines on cell ids (`r1c1`) only and describe the slip in the text.

### Widgets and canvases (each field confirmed)

Checked against `docs/AUTHORING.md` and `app/js/engine/canvas/README.md`, `README-B.md`; where the field is in code, the file is named.

- `console` (README.md): `params.lines`, `title`, `numbers: true`, `wrap: true`, `compact: true`; `state.tone` (`err`, `ok`, `muted`) and `state.shade` per line id (`l1`...); tap target for `tap-regions` by line id. Used for listings, counter output, compiler and sanitiser output.
- `table` (README.md): `params.columns`, `rows` (cells may be `{ "edit": true }`), `align`, `tap: "rows"` (row ids `r0`...), `state.highlight` as `{ "rows": [..] }`, `state.dim`. The generated-members table in l20 is a `table` canvas; the same grid as a `table` widget (AUTHORING, `table`) takes text cells graded as text, `accept` for other spellings.
- `graph` (README-B.md): nodes with `shape: "pill" | "rect"`, `x` and `y` from 0 to 1, `edges` with `directed: true` and `label`, `state.nodes` and `state.edges` as maps keyed by id (a new id adds, `null` removes; used for the copy-or-move frames and the call path; a node can be `dashed`, `highlight`ed, `visited` or `current`, and no state greys it), `state.values` under a node, `state.labels`, `state.pointers`, `tapEdges`; node ids and `e-from-to` are tap targets, in order with `tap-regions` `ordered: true` (`app/js/engine/widgets/tap-regions.js`).
- `array` (README-B.md): `params.cells` (text allowed), `wrap`, `state.highlight.ranges` (a list of `{ range, label, colour }`, used for byte fields; it is in `app/js/engine/canvas/array.js` but README-B documents only the single `highlight: { range, label }`, so it is raised in `docs/BACKLOG-INBOX.md`; if it is still undocumented when you write, use the single `range` three times through `frames`), `state.cells` for the growth frames, `indexFrom`.
- `pair` (README.md): `stack: true`, `active`, `left` and `right` canvases; use sparingly (a listing beside a table).
- Explore controls (AUTHORING section 4): `controls: [{ "frames": [patch, ...], "frameLabels": [...] }]` is a slider through authored state patches (each applied over the canvas as it opened), so a step-through is data. Used in l19 screen 2, l20 screen 2 and l23 screen 1.
- Widgets: `choice`, `multi`, `numeric` (`wrong[]` with `id`, `value`, `tol`), `tap-regions` (`answer`, `wrong[].set`, `countWord`, `ordered: true`), `place` (`mode: "assign"`, `tokens`, `slots` with `accepts`), `order` (`lines`, `answer`, `distractors` with a `why` on each, `same`), `table` widget (text cells, `accept`), `code` with `language: "cpp"`, `prelude`, `postlude`, `allocCheck`, `leakCheck`, `compiles` cases (a snippet that must not compile, with its own `setup`), `examples`, `tests` (3 to 15), `solution`, `how`; `longform` and `parts` in homework (and `parts` in a review).
- Not used, and why: `trade`, `manipulate`, `balance`, `sketch` (nothing to draw), `orderbook`, `interleave` (no threads).

### Lessons

Every lesson: 8 to 12 screens, at most one `title` and at most two non-task screens, difficulty 1 up to 3 across the screens, `summary` (three ideas, a code pattern as the formula, one trap line), 3 to 5 quiz items at difficulty 2 to 3 with static canvases or none, a `minutes` of 13 to 15, tags on every screen as listed. Screen lists give type, difficulty, canvas and widget, then the key, then the slips (the wrong options, each with the `why` that names what the learner did). Keep prose under 60 words a screen and explanations under three sentences, with a canvas patch where a canvas exists. The sentence for the interview is in the `generalise` screen as a comment line in the code block.

#### l19-moving-not-copying: "Moving instead of copying" (`cp-memory`, `cp-classes`; 15 minutes; tags `move-semantics`, `copy-vs-move`, `noexcept-move`, `moved-from`, `sink-argument`)

Objective (course.json): "Explain move semantics, write a move constructor, and say when a move happens." Method: a copy duplicates what an object owns; a move takes it from an object that is about to go, and the compiler picks a move only when the source is an rvalue (a temporary, or something you cast with `std::move`). Say in one line that `Type&&` was met in l11.

- S1 (problem, d1, hook): `console` with line numbers: `Tracked a(1);`, `Tracked b = a;`, `Tracked c = std::move(a);`, `Tracked d = make();`, `take(b);`, `take(std::move(b));`, `take(Tracked(2));`, `v.push_back(c);` (a note line says `make()` returns `Tracked(1)` by value, `take` takes `Tracked` by value, `v` is a reserved `std::vector<Tracked>`). "Tap every line that copies." Key `l2`, `l5`, `l8`. Cite l11: it already tapped the lines that run the copy constructor, so line 2 is the familiar anchor and the new cases are the move (line 3), the returned temporary (line 4), by-value arguments (lines 5 to 7) and `push_back` (line 8). Slips: `with-make` [l2, l4, l5, l8] "You counted the return from `make()` as a copy. Since C++17 a returned temporary is built straight into `d`."; `with-temp` [l2, l5, l7, l8] "`Tracked(2)` is a temporary, built straight into the parameter."; `with-move` [l2, l3, l5, l8] "Line 3 moves: it takes the block and writes none of the data." Explain shows the counts: copy, move, neither, copy, move, neither, copy (from `cpp-scripts/facts_l19.cpp`).
- S2 (explore, d1): `graph` with `frames` control (`frameLabels` "a owns the block", "b = a: copy", "b = std::move(a): move"). Nodes `a`, `b` (pills) and `blk` (rect "1,000,000 doubles"); frame 2 adds a second block under `b` (edge `b` to `blk2`); frame 3 removes `a`'s edge and points `b` at `blk`, with `a` relabelled "a (empty)". Question (numeric): "How many of the 1,000,000 doubles does the move copy?" Key 0. Slip `all` (1000000): "You counted the copy. A move hands over the block and writes none of the doubles." Explain: the copy writes 8,000,000 bytes, about 0.8 ms at 10 GB/s (a round figure); the move writes a pointer and a size, 8 bytes here and 16 on a desktop. Name the type on the screen: `a` and `b` are `Buffer`s (the l11 class: a pointer and a size) holding 1,000,000 doubles. A `std::vector<double>` move writes three pointers (12 bytes here, 24 on a desktop), so do not give 8 and 16 for a vector.
- S3 (problem, d2, names it): `console` of two counter lines, `std::move(a);` alone gives `copies=0 moves=0` and `Tracked b = std::move(a);` gives `copies=0 moves=1`. "What does `std::move(a)` do by itself?" (choice). Key: nothing at run time; it casts `a` to an rvalue reference so a move can be chosen. Slips: `moves` "You read the name literally. The move constructor does the moving; `std::move` only allows it."; `deletes` "`a` is still alive and still destroyed at the end of its scope."; `copies-flag` "There is no flag on the object; the choice is made from the cast's type." Introduce the term "moved-from" here: valid, safe to destroy, value not promised.
- S4 (ladder, d2): `array` with `frames` showing capacity 1, 2, 4, 4 as four pushes run. "Four `v.push_back(Tracked(i))` into an empty vector, `Tracked`'s move constructor `noexcept`. How many copies and how many moves?" (`table` widget, two numeric cells). Key copies 0, moves 7 (4 pushes plus 1 and 2 relocated when it grew at pushes 2 and 3). Say on the screen: "This library grows its capacity 1, 2, 4, 8. The growth factor is a library choice." Slips, as `byKey` on the cell id `r0c1` (moves): "You counted the four pushes. Growth also moves the old elements: 1 at the second push, 2 at the third."; copies cell `r0c0`: "A vector with a `noexcept` move moves its old elements; it does not copy them."
- S5 (ladder, d3): same `array`. "Now `Tracked`'s move constructor is not marked `noexcept`. Two pushes of `Tracked(i)`: what runs?" Key `1 copy, 2 moves`. Say again that this library grows its capacity 1, 2, 4, 8. Slips: `all-move` (0 copies, 3 moves) "You assumed `vector` always moves. It moves only if the move cannot throw; otherwise it copies, so a failure leaves the old block whole."; `all-copy` (3 copies) "The pushes still move from the temporaries; only the relocation copies."; `two-two` (2 copies, 1 move) "The relocation copies one element, and both pushes move." Name `std::move_if_noexcept` once.
- S6 (ladder, d3): `code`, P-move-buffer (below). Starter has copy members only, so `std::move(a)` silently copies.
- S7 (trap, d3): `console`: `const Order c = make_order();` `Order d = std::move(c);` with `Order` holding a `std::vector<Fill>` of 1,000,000 fills. "What runs?" Key: the copy constructor. Slips: `move` "`std::move` always moves. It yields a `const Order&&`, and the move constructor takes `Order&&`, not const."; `error` "It compiles: a `const Order&&` binds to the copy constructor's `const Order&`."; `ub` "Nothing here is undefined. It is a plain copy of 1,000,000 fills."
- S8 (problem, d3, edge case): "Select all that apply: which are always valid on a moved-from `std::vector<int> v`?" Key: destroy it, assign a new vector to it, call `v.clear()`. Slips: `index` (`v[0] = 1;`) "A moved-from vector may be empty. Nothing promises an element."; `back` (`v.back()`) "`back()` needs a non-empty vector; a moved-from one may be empty." Say: the library promises a valid but unspecified state; your own classes decide, as `Buffer` leaves size 0.
- S9 (generalise, d2): code block with the two moves (constructor, assignment) from the solution and the comment line "A move takes the block from something about to go, and leaves it empty and safe to destroy." One confirmation (choice): "What must a move constructor leave behind in the source?" Key: a valid object that is safe to destroy. Slips: `intact` "Then both objects own the block and it is freed twice."; `deleted` "The source is destroyed later; its destructor must still be safe."
- S10 (transfer, d3): `table` widget, prose: `void set_prices(std::vector<double> p) { prices_ = std::move(p); }` and `history`, a vector of 1,000,000 doubles. "How many doubles are copied by each call?" Rows `set_prices(history);` 1,000,000; `set_prices(std::move(history));` 0; `set_prices(load());` 0. Slip on the first cell (`r0c1`): "You counted two copies. The parameter is the copy; the assignment into the member is a move." Close: "Take it by value and move it in, so one function serves both callers." (the "sink" idiom).
- Quiz (5, d2 to 3): (1) `std::move` is a cast (`choice`, distractors as S3). (2) `take(a); take(std::move(a)); take(Tracked(3));` copies? (`numeric`, key 1; slip 3 "You counted every call"). (3) why a vector copies on growth when the move can throw (`choice`). (4) which constructor runs for `const T c; T d = std::move(c);` (`choice`). (5) "A function ends with `return std::move(t);` for a local `t`. What does the `std::move` do?" (`choice`): it blocks copy elision, so a move runs where a plain `return t;` runs none (`facts_l19.cpp`: `make_moved` 1 move, `make_named` 0). Slips: `faster` "A returned local is already treated as an rvalue, and elision builds it in place for free."; `needed` "The compiler moves a returned local without being asked."

#### l20-rule-of-five: "The rule of five" (`cp-classes`; 15 minutes; tags `rule-of-five`, `special-members`, `rule-of-zero`, `self-assignment`, `copy-assignment`)

Objective: "Decide which special members a class needs and write them correctly." Method: declare any of the destructor, the copy members or the move members and the compiler stops guessing: know exactly what it still writes, and choose between none (rule of zero) and all five. The l11 "rule of five" sentence is the starting point; this lesson is the table behind it and the code that gets it right.

- S1 (problem, d1, hook): `table` canvas with `tap: "rows"`, columns `line`, `compiles?` (second column empty), rows `Fill b = a;`, `Fill b = std::move(a);`, `b = a;`, `b = std::move(a);`. Prose: `Fill` has a constructor from a string and a move constructor, nothing else. "Tap every line that compiles." Key `r1`. Slips: `all` [r0..r3] "You expected the compiler to write the rest. Declaring a move constructor deletes the copy members and writes no assignment."; `copies` [r0, r2] "Copying is deleted once you declare a move constructor."; `moves` [r1, r3] "No move assignment is written for you; it must be declared."
- S2 (explore, d1): the full table (below) as a `table` canvas, with a `frames` control that highlights one row at a time (`state.highlight: { "rows": [k] }`, `frameLabels` the seven class names). Observation (numeric): "In how many of the six rows that declare something does `b = std::move(a)` really move?" Key 2 (a move assignment, and all five). Slip `one` (1): "All five defaulted moves, and so does a lone move assignment."
  The table (produced by `cpp-scripts/special_members.cpp`, identical under g++ and clang++; `error` means it does not compile):

  | you declare | `b(a)` | `b(std::move(a))` | `b = a` | `b = std::move(a)` |
  | --- | --- | --- | --- | --- |
  | nothing | copy | move | copy | move |
  | a destructor | copy | copy | copy | copy |
  | a copy constructor | copy | copy | copy | copy |
  | a copy assignment | copy | copy | copy | copy |
  | a move constructor | error | move | error | error |
  | a move assignment | error | error | error | move |
  | all five, defaulted | copy | move | copy | move |

  Say once, in prose, that the copies written for you after a destructor or a copy member are deprecated: the language still writes them, and compilers can warn. Say too that `error` means the line selects a deleted function: the copy members are declared and deleted, not absent.
- S3 (problem, d2): `table` widget over a `console` listing of four classes (nothing declared, a destructor, a copy constructor, a move constructor, each holding a `std::string` and a `std::vector<Fill>`). Fill the `b(std::move(a))` column: move, copy, copy, move (text cells, `accept` "mv", "moves" for move and "copies" for copy). `byKey` on `r1c1`: "A destructor stops the move being written, so `std::move(a)` falls back to the copy, silently."; on `r2c1`: "A declared copy constructor also stops the move; moves fall back to the copy."; on `r3c1`: "A move constructor is the one thing you wrote, so it runs."
- S4 (ladder, d2, defaulted moves): the rule of zero is taught in l9 and l11, so it is not a screen here; it is one quiz item below, as interview recall. This screen is the new case: `struct Pos { std::string sym; std::vector<int> lots; Pos(Pos&&) = default; Pos(const Pos&) = default; };` beside `struct Pos3 { ...same members...; Pos3(Pos3&& o) : sym(std::move(o.sym)), lots(std::move(o.lots)) {} };`. "Is the move constructor `noexcept`?" (`table` widget, two cells, text `yes` or `no`, `accept` "noexcept" for yes, "not" for no). Key: `Pos` yes, `Pos3` no. Slips, `byKey` on the cell ids: `r1c1` (`Pos3`, said yes) "A hand-written move is `noexcept` only if you write it. Nothing is deduced."; `r0c1` (`Pos`, said no) "A defaulted move is `noexcept` when every member's move is, and the move of `std::string` and `std::vector` is." Explain: this is why `= default` is the safe way to write a move, and `std::vector<Pos>` still moves on growth. Checked natively (`cpp-scripts/facts_fixpass.cpp`: 1 and 0).
- S5 (derive, d3, `order` with `distractors`): the lines of a copy assignment for `Samples` (a raw `double*` and a size): `if (this != &other) {`, "allocate a fresh block of `other.size_` doubles", "copy `other`'s doubles into it", "`delete[]` the old block", "point `data_` at the fresh block and set `size_`", `return *this;`. Distractors: `d1` "`delete[]` the old block first, then allocate" (why: "In `a = a` you would copy from a block you just freed. If `new` failed, the object would point at freed memory."), `d2` "`data_ = other.data_;`" (why: "That copies the address, so two objects own one block, the l11 bug."). Say, in one sentence, that on a desk machine a failing `new` throws and the order keeps the old data; this app cannot catch it.
- S6 (ladder, d3): `code`, P-copy-samples (below): the class has a destructor and both move members; the copy members are the shallow ones, and the learner makes them true copies. The tests check the copy, the counts and the leak. They do not catch a delete-first assignment (see the problem's notes), so the screen's explain must not promise that `a = a` exposes it.
- S7 (trap, d3): prose: `struct Book { std::vector<Fill> fills; ~Book() { log("closed"); } };` and `books.push_back(std::move(b));` with 1,000,000 fills in `b` and `books` reserved (a full `books` would also relocate its old `Book`s by copy). "How many `Fill` objects are copied?" Key 1,000,000: the destructor stopped the implicit move, so the copy runs. Slips: `zero` "You reasoned about the members, which are movable. The class decides, and it has no move constructor."; `moves` "There is no move constructor to run."; `error` "It compiles: the copy constructor is still written (deprecated, but written)."
- S8 (problem, d3, edge case): `struct Order { std::unique_ptr<Fill> fill; ~Order() {} };`. "Does `Order b = std::move(a);` compile?" Key: no. Say in the explain that the copy constructor exists (it is declared for you, and defined as deleted because `unique_ptr` cannot be copied), no move constructor is declared, and overload resolution picks the deleted copy constructor for `std::move(a)`: a deleted function is chosen, not absent. Slips: `yes` "You expected the move from the `unique_ptr` member. The destructor suppressed the move."; `copy` "The copy constructor is selected, and it is deleted because `unique_ptr` cannot be copied."; `warn` "It is an error, not a warning: the only candidate is the deleted copy constructor." Checked natively (`cpp-scripts/facts_misc.cpp`: `is_move_constructible` is false; clang says "call to implicitly-deleted copy constructor").
- S9 (generalise, d2): code block: the five signatures with `noexcept` on the moves, and one comment line citing l9 and l11 for the rule of zero (`struct Fills { std::vector<Fill> v; std::string venue; };`: "Own through members and declare nothing, or declare all five."). The confirmation is the new idea, what a declared destructor does to the moves (choice): "`struct Book { std::vector<Fill> fills; ~Book(); };` What does `b2 = std::move(b1)` do to the fills?" Key: copies them (a declared destructor stops the moves being written, and the copy assignment is still written). Slips: `moves` "The vector member is movable, but the class decides, and `Book` has no move assignment."; `error` "It compiles: the copy assignment is still written, though deprecated."
- S10 (transfer, d3): "Which of these needs hand-written special members?" Options: `PositionBook { std::vector<Position>, std::string }`; `Quote { double bid, ask; std::string venue; }`; `FeedHandle { int fd; }` closed in its destructor (key); `OrderBook { std::map<int, Order> }`. Slips name the habit: `vector` "A vector already owns its memory correctly."; `string`; `map`. Explain: only a class that owns a raw resource (a file descriptor, a socket, a raw pointer) needs them, and then you delete the copy and write the move, as in l11's `Connection`.
- Quiz (4): (1) the table lookup for a class that declares only a copy constructor, `b = std::move(a)` (`choice`: copy). (2) rule of zero in one line (`choice`; interview recall of l9 and l11, the only place l20 asks it). (3) why `if (this != &other)` in assignment (`choice`; slip "to save time": "It is for correctness: `a = a` would free the block it is about to copy from"). (4) a class with a `unique_ptr` and no declared members: copyable? movable? (`choice`: movable, not copyable).

#### l21-virtual-dispatch: "How virtual functions work" (`cp-classes`; 15 minutes; tags `virtual-dispatch`, `vtable`, `object-slicing`, `virtual-destructor`, `constructor-dispatch`)

Objective: "Explain the vtable, object slicing and why a base class needs a virtual destructor." Method: a class with virtual functions has one table of function pointers; each object carries a pointer to its class's table; a call through a base pointer follows that pointer, so the dynamic type decides. cpp-pricing l5 showed that it works; this lesson shows how, and what it costs.

- S1 (problem, d1, hook): `console`: `struct Tick { int px; };` and `struct VTick { int px; virtual int level() const; };` with a line "sizeof(Tick) is 4; sizeof(VTick) is 8 here (16 on a desktop)". "Where do the extra bytes in `VTick` go?" Key: a hidden pointer to the class's table of functions. Slips: `code` "A copy of `level`'s code in every object. Code is stored once, in the class, not in each object."; `padding` "`px` and the pointer are 4 bytes each here, so there is no padding to blame."; `name` "Type information sits in the table, not in each object."
- S2 (explore, d1): `graph`: `p` (pill "p: Payoff*"), `obj` (rect "Call object: vptr, strike"), `ctab` (rect "Call's table"), `ptab` (rect "Put's table"), `cfn` (rect "Call::value"), `pfn` (rect "Put::value"); edges `p` to `obj`, `obj` to `ctab` (label "vptr"), `ctab` to `cfn` (label "slot 0"), `ptab` to `pfn`. "`p` points at a `Call`. Tap, in order, what `p->value(110)` visits: the object, its table, the function." `tap-regions`, `ordered: true`, key `obj`, `ctab`, `cfn`. Slips: `skip` [obj, cfn] "There is no pointer from the object to the function. The call goes through the table."; `put` [obj, ptab, pfn] "The object's own vptr leads to its class's table, the Call table."
- S3 (problem, d2): `array` of 12 byte cells with `highlight.ranges` labelled `vptr` (0 to 3), `x` (4 to 7), `y` (8 to 11). Prose: `struct B { int x; virtual void f(); }; struct D : B { int y; void f() override; };`. "What is `sizeof(D)` here?" Key 12. Slips: `8` "You counted the two ints. The pointer is a real field."; `16` "That is the desktop answer; its pointer is 8 bytes. Here it is 4."
- S4 (ladder, d2): `struct Quote { virtual double mid() const; double bid, ask; };`. "Two doubles are 16 bytes. What is `sizeof(Quote)` here?" Key 24. Slips: `20` "4 for the pointer and 16: you left out the padding. A double starts on a multiple of 8, so 4 bytes are skipped."; `16` "You left out the pointer." Explain: 24 on a desktop too, for another reason (8 for the pointer, no padding). Layout sizes checked in `cpp-scripts/wasm_sizes.cpp`.
- S5 (ladder, d3): `console`: `Call c(100); Payoff q = c;` (slicing; `Payoff` is the concrete base of cpp-pricing l5's older library, with a non-pure `value`). "Which table does `q`'s vptr point to?" (choice). Key: Payoff's: the copy is a `Payoff`, and its constructor sets `Payoff`'s vptr. Slips: `calls` "You assumed the copy brings the vptr along. It does not: each constructor sets its own class's table."; `none` "`q` is a whole object with its own vptr." Name: object slicing: the `Call` part is cut off. One line: cpp-pricing l5 passed `Payoff&` for this reason.
- S6 (ladder, d3): `code`, P-hand-vtable: the table of function pointers, built by hand, with `value_of` as what the compiler writes for `p->value(spot)`.
- S7 (trap, d3): `console`: `struct Base { ~Base() {} }; struct Derived : Base { std::vector<double> v; ~Derived() {} };` `Base* p = new Derived; delete p;`. "What does the standard say about `delete p`?" Key: undefined behaviour; typically `~Derived` never runs and the vector leaks. Slips: `defined-leak` "You think only `~Base` runs by rule. The rule is that it is undefined, so anything may happen."; `smart` "`delete` does not look at the heap block to find the real type."; `error` "It compiles; the compiler cannot know the dynamic type here." Fix: `virtual ~Base() = default;` (4 extra bytes an object, as S1).
- S8 (problem, d3, edge case): `Base` has a `std::string who` member set by `who = name();` in its constructor, `name()` is virtual and returns "Base", `Derived` overrides it to return "Derived"; `Derived d;`. "What does `d.who` hold, where `who = name()` ran in `Base`'s constructor?" Key `"Base"`. Slips: `derived` "While `Base` is being built, the object is a `Base`. Its vptr points at `Base`'s table, and `Derived`'s part does not exist yet."; `crash` "It is well defined; the call goes to `Base::name`." Checked natively (`facts_misc.cpp`).
- S9 (derive, d2, `order` with a distractor): the steps of `p->value(110)`: load the object's vptr; index the table at the slot for `value`; call that function with `p` as `this`. Distractor: "search `Call`'s members by name at run time" (why: "No search: the slot number is fixed when the class is compiled. A call costs two loads and an indirect jump."). The two loads are dependent: the object's vptr, then the table slot.
- S10 (generalise, d2): prose and a code block stating the pattern (`virtual ~Base() = default; virtual double f() const = 0;` in the base, `override` in each derived class, `unique_ptr<Base>` or `Base&`, never by value); confirmation (choice): "A call `p->f()` runs the function of the object's real type when?" Key: `f` is virtual and `p` is a pointer or reference. Slip: `always` "A non-virtual `f` is chosen by the pointer's type. An object passed by value is a base object." In the explain add one line, the link to l20: a base with `virtual ~Base() = default;` declares a destructor, so its moves are not written, which suits a polymorphic base (Core Guidelines C.67: copy through `clone()`, not through a base reference), and `clone()` in the exam's P-clone-basket copies the derived class.
- S11 (transfer, d3): "A pricer calls `payoff->value(spot)` 10,000,000 times in a loop over a book of calls only. Which change removes the table lookup?" Key: make the pricer a template on the payoff type (compile-time dispatch, `template <class P> double price(const P& p, ...)`), keeping the virtual version for mixed books. Slips: `inline` "`inline` does not tell the compiler which function a call through a base pointer reaches."; `final` "`final` on every class helps only when the compiler can see the exact type."; `fewer-calls` "Removing a lookup is the point; calling less is a different change." Explain: a virtual call costs two dependent loads (the vptr, then the slot) and an indirect call, and usually stops inlining, because the compiler does not know the target. A compiler devirtualises a call whenever it can prove the dynamic type (a local object, a `final` class, whole-program optimisation), so say "usually", never "never". With one known type, a template gives the same code with no lookup (links to `cpp` l13).
- Quiz (4): (1) `sizeof` of a class with one virtual and one `int` here (`numeric` 8; slip 4). (2) what `override` buys (`choice`: a compile error if nothing is overridden). (3) a pure virtual function and an abstract class (`choice`). (4) slicing: `std::vector<Payoff>` holding calls (`choice`).

#### l22-undefined-behaviour: "Undefined behaviour" (`cp-basics`, `cp-memory`; 15 minutes; tags `undefined-behaviour`, `optimiser-assumptions`, `signed-overflow`, `defined-vs-undefined`, `sanitisers`)

Objective: "Spot undefined behaviour in short snippets and say what the compiler may do with it." Method: undefined behaviour is not "a bug that crashes": the standard puts no limit on the whole run, so the compiler assumes it never happens and may delete checks, return garbage or crash. This lesson is read-and-judge by design, and says so on screen 1.

- S1 (problem, d1, hook): `console`: a four-line `first(int* p)` that reads `*p` and then tests `p == nullptr`, and the compiler's wasm output (`first(int*):` then `local.get 0` and `i32.load 0`, no comparison). Prose: "This app never runs undefined behaviour: whatever happens is allowed, so the answer could differ by build. These screens show code and compiler output, and you judge." "Why is there no null test in the output?" Key: it had already read `*p`, so it assumed `p` is not null. Slips: `drops-ifs` "It dropped one comparison it could prove, not every `if`."; `bug` "A program that breaks the rules has no wrong answer, so this is not a compiler bug."; `never-null` "`nullptr` is a real value; the compiler assumed it away only after the read."
- S2 (explore, d1): `console` with line numbers, eight lines: `int a[3] = {1, 2, 3};`, `unsigned u = 0;`, `u = u - 1;`, `int s = a[3];`, `int x;`, `int y = x + 1;`, `int big = 2147483647;`, `big = big + 1;`. "Tap every line with undefined behaviour." Key `l4`, `l6`, `l8`. Slips: `with-unsigned` [l3, l4, l6, l8] "Unsigned arithmetic wraps by definition: `u - 1` is 4,294,967,295. Only signed overflow is undefined."; `no-uninit` [l4, l8] "Reading `x` before it is set is undefined, not just a garbage value." (Say "in the standard this app uses": C++26 makes it erroneous behaviour instead.); `no-index` [l6, l8] "`a[3]` is one past the end of a 3-element array."
- S3 (problem, d2): `place` (`mode: "assign"`), nine chips in three slots (defined; implementation-defined or unspecified; undefined): `UINT_MAX + 1u` (defined: 0); `-7 / 2` (defined: -3, towards zero since C++11); `sizeof(long)` (implementation-defined: 4 here, 8 on a desktop); `char c = -1; c < 0` (implementation-defined: depends on whether plain `char` is signed); `f(g(), h())` which runs first (unspecified); `INT_MAX + 1` (undefined); `v[3]` on a 3-element vector (undefined); `int x; return x;` (undefined); `1 << 32` for an `int` (undefined). `byKey` per token id with the rule in one sentence.
- S4 (ladder, d2): `console` of three `g++ -fsanitize=undefined` lines (from `cpp-scripts/ub_facts.cpp`): `runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'`, `runtime error: index 3 out of bounds for type 'int [3]'`, `runtime error: load of null pointer of type 'volatile int'`, with a note "desk machine, not this app". "Which flag turns these reports on?" Key `-fsanitize=undefined`. Slips: `wall` "`-Wall` warns at compile time. It cannot see values that only exist at run time."; `o0` "A lower optimisation level changes what happens; it does not report anything."; `debug` "`-g` adds line numbers to reports but turns none on." Also name `-fsanitize=address` for memory errors; this app compiles with libc++ hardening on, which stops an out-of-range `vector` index but cannot see an overflow or a null read.
- S5 (ladder, d3): `code`, P-add-overflows: write the check so the addition never overflows; the starter compares the sum after the overflow. Explain: this app's compiler removes a check made after the addition; another build might not, which is the point.
- S6 (trap, d3): "`int x = INT_MAX; int y = x + 1;` What value does `y` hold?" Key: no value is promised: the program has undefined behaviour. Slips: `wrap` "The hardware wraps. C++ does not promise to pass that on."; `big` "There is no larger `int` to hold 2,147,483,648."; `error` "It compiles, and the compiler may warn if it can see the constants." Recap in one line that cpp-pricing l11 showed `x + 1 < x` flip between `-O0` and `-O2`.
- S7 (problem, d3, edge case): "`v` is an empty `std::vector<int>`. What does `v.size() - 1` equal here?" (numeric) Key 4,294,967,295: `size()` is unsigned and `size_t` is 4 bytes here (18,446,744,073,709,551,615 on a desktop); defined, and the classic reason a loop `for (size_t i = v.size() - 1; i >= 0; --i)` never ends. Slip `minus-one` (-1): "`size()` is unsigned, so the subtraction wraps."
- S8 (derive, d3, `order` with a distractor): the lines of `add_overflows` for positive `b`: "if `b > 0`", "the sum overflows exactly when `a > INT_MAX - b`", "otherwise it overflows exactly when `a < INT_MIN - b`". Distractor: "compute `a + b` and compare it with `a`" (why: "The addition has already overflowed, so there is nothing defined left to compare.").
- S9 (ladder, d3): "Which comparator makes `std::sort` undefined?" (choice) Key `[](int a, int b) { return a <= b; }` (not a strict weak ordering: equal elements compare as less, and the algorithm may run off the end). Slips: `less` (`a < b`) "Plain `<` is the model."; `greater` (`a > b`) "A descending sort is fine: `>` is a strict ordering."; `abs` (`std::abs(a) < std::abs(b)`) "Ties are allowed: equivalent elements compare false both ways."
- S10 (generalise, d2): code block of the defensive pattern (`if (b > 0) return a > INT_MAX - b;`) and the rule "check before you do it, never after"; confirmation (choice): "Your tests pass and the sanitiser is silent. Is the code free of undefined behaviour?" Key: only for the inputs run, on that build. Slips: `yes` "Undefined behaviour belongs to the code for any input it can meet, and testing only samples inputs."
- S11 (transfer, d3): "A desk sums fill values in pence in an `int`. 5,000 fills of £5,000 are £25,000,000, that is 2,500,000,000 pence. What type should the total be?" Key `std::int64_t` (`long long`): an `int` holds up to 2,147,483,647 pence (£21,474,836.47), and a signed overflow is undefined. Slips: `unsigned` "It doubles the range to £42,949,672.95 and wraps silently."; `double` "It is exact for whole pence up to 2^53 but sums of money belong in integers."; `check-after` "A check after the addition runs too late, as in S5."
- Quiz (4): (1) signed against unsigned overflow (`choice`). (2) which compile flag finds undefined behaviour at run time (`choice`). (3) `INT_MAX` pence in pounds (`numeric`, unit £, key 21474836.47, `accept` "£21,474,836.47"). (4) the S2 idea on a new snippet: `int a[4]; a[4] = 0;` (`choice`).

#### l23-own-smart-pointer: "Writing your own smart pointer" (`cp-memory`; 15 minutes; tags `smart-pointer`, `unique-ptr`, `shared-ptr`, `reference-count`, `control-block`)

Objective: "Implement a minimal unique pointer and a reference-counted pointer." Method: a smart pointer is a class whose destructor frees what it owns; unique means copying is deleted and moving transfers; shared means a count that all owners share, and the last owner frees. l9 used them; here they are built, so the rules of l19 and l20 meet in one class.

- S1 (explore, d1, the build, not the count; l9 already asks `use_count`): `graph` with a `frames` control (`frameLabels`: "1 a made", "2 b = a", "3 c = b", "4 c ends", "5 b ends", "6 a ends"): `a`, `b`, `c` (pills) pointing to `obj` (rect "Tracked(1)") and a `cnt` node, both added at frame 1 and labelled "new"; later frames add or remove only edges. At frame 6 `obj` is `{ "dashed": true, "label": "Tracked(1) deleted" }`. "How many times does `new` run across these six steps?" (numeric). Key 2 (the object and the counter, both at step 1; a copy makes none). Slip `three` (3): "A copy shares the counter that already exists. It does not make one." Checked in `facts_misc.cpp` (2 allocations for `shared_ptr(new T)`).
- S2 (problem, d2, the mechanism): `graph`: after `a`, `b = a`, `c = b`, "How many counters exist on the heap?" (numeric) Key 1. Slip `three` (3): "If each pointer kept its own count, no pointer would know when the others had gone. One counter is shared."
- S3 (ladder, d3): `code`, P-unique-ptr.
- S4 (ladder, d3): `choice`: "A `std::unique_ptr<int>` is one pointer wide and a `std::shared_ptr<int>` is two. Why?" Key: the shared one also points at the counter block. Slips: `count-inside` "A count inside each pointer would not be shared between copies."; `deleter` "The deleter lives in the counter block, not in each pointer."; `align` "Padding does not double a pointer." Checked natively on a desktop (`facts_misc.cpp`: 1 and 2 pointers); here the sizes are 4 and 8 bytes; say "two pointers" and not a byte count unless you add "here" and "on a desktop" as in l21.
- S5 (derive, d3, `order` with a distractor): the lines of `SharedPtr`'s copy assignment: "add one to `other`'s count", "drop this pointer's own count: subtract one, and at zero delete the object and the counter", "copy `ptr_` and `count_` from `other`". Distractor: "drop this pointer's own count first, then add one to `other`'s" (why: "For `a = a` the count falls to zero and the object is deleted. Then you add to a freed counter.").
- S6 (ladder, d3): `code`, P-shared-ptr.
- S7 (trap, d3): `graph` with two counters: `Tracked* raw = new Tracked(1); SharedPtr<Tracked> a(raw); SharedPtr<Tracked> b(raw);`. "What happens at the end of the block?" Key: each pointer made its own counter, both reach zero, and the object is deleted twice: undefined behaviour. Slips: `two` "You gave the count as 2. Each constructor from a raw pointer starts its own count at 1."; `leak` "It is freed, twice; not never."; `once` "The counters do not know about each other." Rule: make a shared owner from `make_shared` or copy an existing `shared_ptr`, never from the same raw pointer twice.
- S8 (problem, d3, edge case): "In `operator=`, why add to the other count before dropping your own?" (choice) Key: `a = a`: the count could fall to zero and free the object before it is taken again. In the explain add "the next questions" an interviewer asks: is it thread safe (the count is atomic, the pointee is not), what is `weak_ptr` (a handle that does not add to the count) and what is `enable_shared_from_this`. Slips: `speed` "Order makes no speed difference."; `atomic` "The real count is atomic, ours is not, and that is unrelated to the order."
- S9 (generalise, d2): code block with the two classes' member lists in comments (`unique: one owner, move only, no overhead`; `shared: a count, copy cheap, last owner frees`). "Prefer `unique_ptr`" is the l9 rule: cite it, do not re-teach it. The new confirmation is the cost (choice): "What does copying a `shared_ptr` cost that moving one does not?" Key: an atomic add to the count (a move takes the pointers and leaves the count alone). Slips: `allocation` "A copy shares the existing counter. It allocates nothing."; `nothing` "Every copy adds one to a shared count, and the add is atomic."
- S10 (transfer, d3): `table` widget, three numeric cells. "A feed handler makes 200,000 messages a second as `std::shared_ptr<Message>(new Message)`. How many allocations a second? With `std::make_shared<Message>()`? At 50 ns an allocation (a round figure), how many milliseconds a second does the change save?" Keys 400,000; 200,000; 10. Slips, as `byKey` on cell ids: `r0c1` "That is the make_shared count. `new` gives one allocation for the object and one for the counter."; `r2c1` (wrong value 10,000): "200,000 allocations at 50 ns is 10,000,000 ns, which is 10 ms." Checked natively (`facts_misc.cpp`: 2 allocations against 1) and in `number_checks.py`.
- Quiz (4): (1) copying a `unique_ptr` (`choice`: compile error, copying deleted). (2) `use_count` after `auto a = ...; auto b = a; { auto c = a; }` (`numeric`, key 2). (3) the allocations for `make_shared` against `shared_ptr(new T)` (`numeric`, key 1; slip 2). (4) which of `release()` and `reset()` deletes the object (`choice`: `reset`).

#### review-5 (`review-5.json`, 10 items, difficulty 2 to 4, two per lesson, tags and `pace` in seconds, `skills` as the lesson)

1. (l19, `numeric`, d3, `copy-vs-move`, 60) `take(a); take(std::move(a)); take(Tracked(3));` copies? 1.
2. (l19, `choice`, d4, `noexcept-move`, 75) why a vector copies on growth when the move is not `noexcept`; key: to keep the old block whole if a move throws.
3. (l20, `multi`, d4, `special-members`, 90) `struct Order { std::unique_ptr<Fill> fill; ~Order() {} };` "Select all that apply: which lines compile?": `Order a;` (key), `Order b = std::move(a);` (no), `Order c = a;` (no), `a = std::move(b);` (no). Slips name the rule.
4. (l20, `choice`, d3, `defaulted-moves`, 60) `struct Pos { std::string sym; std::vector<int> lots; Pos(Pos&&) = default; Pos(const Pos&) = default; };` "Is `std::is_nothrow_move_constructible_v<Pos>` true?" Key yes: a defaulted move is `noexcept` when its members' moves are. Slips: `no` "You expected `= default` to be cautious. It is `noexcept` when every member's move is."; `write-it` "Only a hand-written move needs `noexcept` written. A defaulted one is deduced." (The rule of zero is no longer a review item: l9 and l11 teach it, and l20 recalls it once in the quiz.)
5. (l21, `numeric`, d3, `vtable`, 60) `struct Q { virtual double mid() const; double bid, ask; };` here: 24.
6. (l21, `multi`, d4, `virtual-destructor`, 90) "Select all that apply: which need `Base`'s destructor to be virtual?" `delete` of a `Derived` through a `Base*` (key); a `std::unique_ptr<Base>` holding a `Derived` (key); a `std::shared_ptr<Base>` made from `std::make_shared<Derived>()` (no: the counter block remembers `Derived`'s deleter; checked in `facts_misc.cpp`); a `Derived` on the stack (no).
7. (l22, `multi`, d3, `defined-vs-undefined`, 75) "Select all that apply: which are undefined?": `unsigned u = 0; --u;` (no); `int a[4]; a[4] = 1;` (yes); `int x = INT_MAX; ++x;` (yes); `v.at(5)` on a 3-element vector (no: it throws, which ends the program here); `int y; int z = y;` (yes).
8. (l22, `numeric`, d2, `signed-overflow`, 45) `INT_MAX` pence in pounds: 21474836.47 (unit £, `accept` "£21,474,836.47").
9. (l23, `numeric`, d3, `reference-count`, 45) `SharedPtr a(new T); auto b = a; { auto c = b; }` then `a.use_count()`: 2.
10. (l23, `choice`, d4, `control-block`, 75) two `SharedPtr` made from one raw pointer: double delete.

Check coverage: every lesson twice; skills: items 1 and 2 `cp-memory`, `cp-classes`; 3 to 6 `cp-classes`; 7 and 8 `cp-basics` (8 also `cp-memory`); 9 and 10 `cp-memory`.

#### homework-5 (`homework-5.json`, 9 items, difficulty 3 to 5; E11 `parts` on item 3 and item 7; `tags`, `pace` and `skills` on every item)

1. (d4, `code`, P-scope-guard, l19 and l20, `scope-guard`, `cp-memory` `cp-classes`) interview recall of the l11 `Connection` (destructor, copying deleted, a move constructor that leaves the old object inert, so the duty runs once), now with a `std::function` callback. Say "the l11 `Connection` with a callback" in the prompt. The new part is the `std::vector<ScopeGuard>` growth test, where `ran` must reach exactly 3: relocation moves a guard and never runs its callback.
2. (d5, `code`, P-vec, l19 to l23, `vec-from-scratch`, `cp-memory` `cp-classes`) a growing array from raw storage: allocation count, moves on growth, copy and move members, `push_back(v[0])`, and copy assignment safe for `a = a`.
3. (d4, `parts`, l19, `sink-argument`, `cp-classes`) the interviewer's follow-ups on a setter: (a) `numeric`: doubles copied by `set_prices(history)` when `set_prices(std::vector<double> p) { prices_ = std::move(p); }` and `history` has 1,000,000 doubles, 1,000,000; (b) `numeric`: the same with `set_prices(std::move(history))`, 0; (c) `choice`: which signature is best for a setter that keeps its argument: by value then move (key; the explain adds "Two overloads, `const T&` and `T&&`, avoid the extra move and can reuse the member's capacity; by value is the short version"), `const std::vector<double>&` only (slip: "copies even when the caller is finished with it"), `std::vector<double>&&` only (slip: "callers with an lvalue cannot call it"), `std::vector<double>&` (slip: "it cannot take a temporary and it lets the callee change the caller's data").
4. (d4, `order` with `distractors`, l23, `shared-ptr-assign`, `cp-memory`) the move assignment of `SharedPtr` in order: guard `this != &other`, drop own count, take the pointer and counter, empty the source; distractors: "leave the source's count unchanged and point both at it" (why: "Both would drop the count: it falls by two for one owner."), "drop own count after taking the new pointer" (why: "You would drop the count of the object you just took.").
5. (d4, `table` widget, l20, `special-members`, `cp-classes`) for four classes that declare, in turn, a copy assignment, a move assignment, a move constructor and a destructor, fill the cells for `b(std::move(a))`, `b = a` and `b = std::move(a)` (twelve text cells; four columns in all: `you declare`, `b(std::move(a))`, `b = a`, `b = std::move(a)`, with `compact: true` and one-word cells (`copy`, `move`, `error`); three editable columns on a phone is the layout `docs/BACKLOG-INBOX.md` says overflows, so check the `--mobile` playthrough and, if the last column is off screen, split it into two tables of two classes each). Key by row: copy assignment: copy, copy, copy; move assignment: error, error, move; move constructor: move, error, error; destructor: copy, copy, copy (the l20 table). `byKey` on cell ids only.
6. (d4, `multi`, l22, `defined-vs-undefined`, `cp-basics` `cp-memory`) six new snippets, "Select all that apply: which are undefined?": `std::vector<int> v{1, 2, 3}; for (int x : v) if (x == 2) v.push_back(4);` (yes: iterator invalidation); `int a = INT_MIN; int b = -a;` (yes); `unsigned u = 1u << 31;` (no); `char buf[4]; buf[4] = 0;` (yes); `int* p = new int(1); delete p; delete p;` (yes); `int n = 7; n = n / 2;` (no).
7. (d4, `parts`, l21, `virtual-dispatch`, `cp-classes`) (a) `numeric`: `sizeof` of `struct B { virtual void f(); double x; };` here, 16 (4 for the pointer, 4 padding, 8); (b) `choice`: `Payoff q = call;` copies the `Call` and `q.value(110)` runs `Payoff`'s version: the vptr of the copy is `Payoff`'s (key); (c) `multi`: "Select all that apply: which fixes the slice?" a `std::vector<std::unique_ptr<Payoff>>` (key), a `std::vector<const Payoff*>` over objects that outlive it (key), a `std::vector<Payoff>` with `reserve` (slip), a `std::vector<Payoff&>` (slip: "references cannot be stored in a vector").
8. (d5, `longform`, l19 and l20, `move-semantics`, `cp-memory` `cp-classes`) "Say aloud, in three minutes: what `std::move` does, when a move happens, why a move constructor should be `noexcept`, and what the rule of five and the rule of zero ask you to do." Model answer: `std::move` is a cast to an rvalue reference, so a move constructor can be chosen; a move happens when the source is an rvalue (a temporary, a returned local, a `std::move` cast) and a move constructor exists and is not hidden by a declared destructor or copy member; a move takes the resource and leaves a valid, destroyable, empty source; `noexcept` matters because `std::vector` grows with `move_if_noexcept`, so a throwing move means a copy of every element on growth (1,000 `Buffer`s of 1,000 doubles: each growth copies 8 MB instead of moving 1,000 pointers); a `const` object cannot be moved, so `std::move(c)` copies; rule of zero: own through members and declare nothing; rule of five: if you declare any of the five, decide all five, delete the copy and write the moves for a class that owns a raw resource; the one-sentence close. Rubric 10: `std::move` is only a cast 2; when a move happens, with the const and the rvalue cases 2; what a move leaves behind 1; `noexcept` and vector growth with a figure 2; rule of zero 1; rule of five and the silent copy after a destructor 2.
9. (d5, `longform`, l21 and l22, `virtual-dispatch`, `cp-classes` `cp-basics`) "Say aloud, in three minutes, what happens for `Base* p = new Derived; p->f(); delete p;` when `Base`'s destructor is not virtual, and what undefined behaviour means for a quant who ships code." Model answer: the vptr and table path for `p->f()` when `f` is virtual; `delete p` through a base pointer with a non-virtual destructor is undefined, in practice only `~Base` runs and `Derived`'s members leak; fix with `virtual ~Base() = default`; the cost (4 bytes an object here, two loads and an indirect call a call, and usually no inlining when the compiler cannot see the dynamic type); slicing; undefined behaviour means the standard places no limit on the run, so the optimiser assumes it never happens (the deleted null check, the deleted overflow check); signed overflow, out-of-range index, uninitialised read, dangling pointer; the desk practice: sanitisers in tests, check before the operation, wider types for money (`std::int64_t` pence). Rubric 10: the dispatch path 2; the non-virtual destructor and what it does 2; the fix and its cost 1; slicing 1; what undefined behaviour permits and why the optimiser deletes checks 2; three examples 1; desk practice 1.

Coverage: every lesson appears; items 1 and 2 carry code (two `code` items, one at difficulty 5); items 8 and 9 are `longform` (each rubric sums to 10); `order` in item 4; `parts` in items 3 and 7.

### Number checks

Every number in this section (8,000,000 bytes, also 1,000 x 1,000 x 8 for the growth copy; 0.8 ms; 7 moves; 1 copy and 2 moves; 3 and 4; 15 moves and 11 allocations in `Vec`; 12, 24 and 16 bytes; £21,474,836.47; 4,294,967,295; 2,500,000,000 pence; 400,000, 200,000 and 10 ms) is computed twice: once by `cpp-scripts/number_checks.py` (a model that shares no code with the C++) and once natively or in the hidden tests, as listed under "Number checks" at the end of this file. The hidden tests' expected values come from the independent Python model in the same scripts folder or from a hand derivation stated beside each test.

### Scratchpad, files and report

- Use only your own subfolder `cpp-5` under the scratchpad folder your session lists, for generators, screenshots and notes. The browser playthrough in this sandbox needs `--local-cdn <pkgs>` (the `pkgs` folder named in the orchestrator prompt; build it with `bash app/tools/fetch-local-cdn.sh <pkgs>` if missing). The C++ screens need YoWASP clang in that folder.
- Do not edit any file outside `app/content/courses/cpp/` (only `l19-...` to `l23-...`, `review-5.json` and `homework-5.json`), and never `course.json`, other levels' files, engine files, the exam files or docs other than the report and the inbox. The validator rewrites `content/manifest.json`; that is expected. Another agent extends `app/content/exams/topic-1.9.json` (next section). Do not run git write commands.
- Report in `docs/reports/cpp-5.md` as `docs/LEVEL-BRIEF.md` says, and add every engine or canvas limitation that bent an idea to `docs/BACKLOG-INBOX.md` under `Raised later (cpp level 5):`. Hand back no more than six lines.

### Acceptance

- `node tools/validate.mjs` from `app/`: 0 errors. The nine hidden-test problems are copied from "Code problems" exactly and each passes in the app: starter fails, solution passes (`node tools/playthrough.mjs --lesson cpp/<id> --local-cdn <pkgs>`, also `--set cpp/review-5` and `--set cpp/homework-5`), each with and without `--mobile` and with `--tablet`; the l22 code screen's starter fails whatever the compiler does.
- l22 contains no screen that depends on running undefined behaviour, and its first screen says that the app does not run it. Every sanitiser line is labelled "desk machine"; every compiler-output line is labelled with its target (wasm32, `-O1`).
- l19 screen 4 and 5 counts match the app's own compiler (run `cpp-scripts/facts_l19.cpp` through it once); a difference is reported, not papered over.
- No screen uses `x + 1 < x` as a puzzle, writes `Call` and `Put` as a task, or re-runs the l11 `Prices` double free as a puzzle.
- Each lesson has 8 to 12 screens, at most two non-task screens, 3 to 5 quiz items; review-5 has 10 items and homework-5 has 9; every `choice` and `multi` has `shuffle: true`; every distractor has a `why` that names the learner's action; every stated number is in "Number checks".
- Voice: British English, no exclamation marks, no em-dashes, sentences under 20 words, explanations of at most three sentences, £ for money, no firm named.

## Exam topic-1.9 extension

A separate exam agent, after level 5 has landed, extends `app/content/exams/topic-1.9.json` (25 items, 60 minutes, pass 0.7; the cap is 30). It adds five items that cover cpp level 5, edits no lesson file, and leaves the existing 25 items and ids untouched. The exam's `skills` map already holds every `cp-*` skill, so it needs no new row.

Balance. Today the ramp is 5, 12, 5 and 3 items at difficulty 2, 3, 4 and 5 (20%, 48%, 20%, 12%). The five new items are one at difficulty 2, two at 3 and two at 4, giving 6, 14, 7 and 3 of 30 (20%, 47%, 23% and 10%), inside the validator's ramp of 20, 50, 20 and 10 per cent plus or minus 10. By kind: three `choice` or `multi`, one `numeric`, one `code`; the exam then has 7 `code` items of 30 and one `longform`. Minutes: 60 to 75. By the paces in the table the four short items take 60 + 90 + 90 + 90 = 330 s (5.5 minutes) and the code item 600 s (10 minutes): 15.5 minutes in all, so the extra 15 minutes keeps the pace the exam had. The existing 25 items carry neither `tags` nor `pace`; the five new ones carry both (the validator accepts either). Set `"minutes": 75` and leave `pass` at 0.7.

Skills. The existing 25 items hold 4 `cp-classes`, 3 `cp-basics`, 3 `cp-memory`, 3 `cp-stl`, 2 `cp-references` and 2 `cp-build`. The five new items add one each to `cp-memory`, `cp-stl` and `cp-basics` and two to `cp-classes` (6 of 30, 20%), so `cp-classes` does not run away. The new items do not repeat a lesson screen: `e-virtual-dtor` is the reversal (a `shared_ptr<Base>` from `make_shared<Derived>` is defined) and `e-ub-which` uses five lines that appear nowhere in l22, the review or the homework.

Order. The file runs in rising difficulty; insert each new item at its difficulty band: `e-const-move` after `e-link-stage`; `e-vector-growth` and `e-ub-which` after `e-code-credit-line`; `e-virtual-dtor` and `e-code-clone-basket` after `e-code-rank-fills`. Every item has `id`, `difficulty`, `skills` (one id, below), `tags` (kebab-case, family first), `pace` (seconds), `title`, `prose`, `question`, `widget`, `feedback` (with `byKey` lines that name the slip), `explain` (at most three sentences). Voice as AUTHORING; no firm named.

| id | type | difficulty | skills | tags | pace |
| --- | --- | --- | --- | --- | --- |
| `e-const-move` | `choice` | 2 | `cp-memory` | `move-semantics` | 60 |
| `e-vector-growth` | `numeric` | 3 | `cp-stl` | `noexcept-move` | 90 |
| `e-ub-which` | `multi` | 3 | `cp-basics` | `defined-vs-undefined` | 90 |
| `e-virtual-dtor` | `choice` | 4 | `cp-classes` | `virtual-destructor` | 90 |
| `e-code-clone-basket` | `code` (C++) | 4 | `cp-classes` | `clone-idiom` | 600 |

1. `e-const-move` (l19, `choice`, key the copy). Prose: `struct Order { std::string id; std::vector<int> fills; };` then `const Order a{"A1", {1, 2, 3}};` and `Order b = std::move(a);`. Question: "What is `a.fills.size()` afterwards?" Key `3` (the copy constructor ran: `std::move(a)` is a `const Order&&`, which a move constructor cannot take). Slips: `0` "You assumed `std::move` always empties its argument. A const object cannot be moved from, so a copy ran."; `error` "It compiles: a const rvalue binds to the copy constructor's `const Order&`."; `unspecified` "A moved-from object is unspecified only if a move ran. None did." Shuffle on.
2. `e-vector-growth` (l19, `numeric`, key 3, `tol` abs 0). Prose: a `Fill` with a copy constructor and a move constructor that is not `noexcept`; four `v.push_back(Fill(i))` on an empty `std::vector<Fill>`, and the line "This library grows its capacity 1, 2, 4, 8; the growth factor is a library choice." Question: "In all, how many times does the copy constructor run?" Key 3 (capacity 1, 2, 4: it grows at the second and third push and relocates 1 and 2 elements by copy; each push moves from its temporary, 4 moves). Slips (`wrong[]`): `zero` (0) "You assumed a vector always moves on growth. With a move that may throw it copies."; `four` (4) "The pushes move from the temporaries; the copies come from growth."; `seven` (7) "That adds the 4 pushes' moves to the 3 copies. Only copies were asked." Model: `cpp-scripts/number_checks.py` (3 copies and 4 moves) and `facts_misc.cpp`.
3. `e-ub-which` (l22, `multi`, "Select all that apply: which lines have undefined behaviour?"). Five lines not used in l22, the review or the homework. Options: `int n = 0; int r = 5 / n;` (key: division by zero); `std::string s = "ab"; char c = s[s.size()];` (no: reading the terminating null is defined, `c` is 0); `const int k = 3; const_cast<int&>(k) = 4;` (key: modifying an object defined `const`); `int* p = new int[2]; delete p;` (key: the wrong form of `delete`); `unsigned char b = 255; ++b;` (no: unsigned arithmetic wraps, `b` is 0). Slips: `size` "Reading `s[s.size()]` is allowed and gives the null character."; `unsigned` "Unsigned arithmetic wraps by definition.". Checked natively (`cpp-scripts/facts_fixpass.cpp` for the two defined lines).
4. `e-virtual-dtor` (l21, `choice`, key `~Derived` runs: a reversal of l21 S7, which used a raw `delete`). Prose: `struct Base { ~Base() {} }; struct Derived : Base { std::vector<double> v; ~Derived() { ++gone; } };` `std::shared_ptr<Base> p = std::make_shared<Derived>(); p.reset();`. Question: "`Base`'s destructor is not virtual. What happens at `p.reset()`?" Key: `~Derived` runs and `gone` is 1: the counter block remembers the real type's deleter, so this is defined. Slips: `base-only` "You applied the raw `delete` rule. A `shared_ptr` made by `make_shared<Derived>` stores the deleter for `Derived`."; `ub` "Undefined behaviour is for `delete` through a `Base*`. Here the deleter was chosen when the pointer was made."; `leak` "The vector is freed, because `~Derived` runs." Explain: the safe habit is still a virtual destructor, because a `unique_ptr<Base>` or a raw `delete` has no such memory. Checked natively (`cpp-scripts/facts_misc.cpp` and `facts_fixpass.cpp`: `gone` is 1).
5. `e-code-clone-basket` (l21 and l9, `code`, C++). Brief: "An `Order` is an interface with `cost(double market)` and `clone()`. `Market` is written. Write `Limit`, which buys only when the market is at most its limit, and `Basket`, which holds orders of any kind and deep-copies them in `clone()`." Widget: P-clone-basket under "Code problems": 11 hidden tests, `tests` as given, `leakCheck: true` (no `allocCheck`), `how`: "Submit runs 11 hidden tests. Costs are compared with `isclose`."

Acceptance for the exam agent: `node tools/validate.mjs` 0 errors (ramp, 30 items, one `code` widget with 3 to 15 tests); `node tools/playthrough.mjs --exam topic-1.9 --local-cdn <pkgs>` plays all 30 items right (and with `--mobile` and `--tablet`); the starter of item 5 fails and its solution passes in the app; a second reader checks the keys against `cpp-scripts/` and records it in `docs/reviews/review-exam-1.9-cpp5.md`.

## Code problems

Nine problems with hidden tests: six in lessons (l19 to l23, two in l23), two in `homework-5` and one in the exam extension. Each is in `docs/briefs/cpp-scripts/` as `<id>_starter.cpp`, `<id>_solution.cpp` and `<id>_tests.json`, produced from `problems_*.py` by `run_all.py`. `harness.py` mimics the app's function mode: a hidden prelude, the learner's code, a hidden postlude, then one block per test (the `setup`, then the `call` as a value), each run as its own process; it adds a counter header for `allocCheck` and a live-block count per test for `leakCheck`; a `compiles` case is a `-fsanitize`-free `-fsyntax-only` compile of the snippet in a function after the code. Every starter compiles and fails; every solution passes all tests with g++ 13.3 and clang++ 18.1 at `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`, and is clean under `-fsanitize=undefined` with g++ (the clang sanitiser runtime is not installed here). Native runs are not enough: the app's allocator frees a block twice without complaint and leaves freed memory readable, where glibc aborts, so a slip that only the native allocator catches is not caught. Every problem is therefore also run in the app's own toolchain (`app_toolchain/`, results in `results_app.txt`) and a slip counts as caught only if the app run fails a test. No test reads freed memory or relies on the allocator noticing a mistake. Expected values come from a hand derivation or the independent model in `number_checks.py`; the harness reports a test as failed when it fails, crashes or times out.

Every starter fails at least 6 of its tests in every run listed below, so the first Check shows a real list of red rows.

### P-move-buffer

Where: `l19-moving-not-copying`, screen 6 (ladder), a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 15 hidden tests (function mode, `compare: "equal"` for integers, booleans and strings, `isclose` for doubles). Flags: allocCheck: true, leakCheck: true. `examples` are the first two tests.

`how`: "Submit runs 15 hidden tests. `alloc_count()` counts calls to `operator new` and `new[]` since the last reset, so a move that copies shows as 1 instead of 0; a block never freed fails its test. A moved-from buffer must report size 0 and `data()` null."

Hidden `prelude`:

```cpp
#include <utility>
#include <vector>
#include <type_traits>
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
// A buffer of doubles on the heap. It copies correctly already.
// Add a move constructor and a move assignment: each takes the other buffer's block
// and leaves it empty (size 0, data() null). Neither may allocate, and both must be noexcept.
// The move assignment must be safe for `a = std::move(a)`.
class Buffer {
public:
    Buffer(int n, double x) : size_(n), data_(new double[n]) {
        for (int i = 0; i < n; ++i) data_[i] = x;
    }
    Buffer(const Buffer& other) : size_(other.size_), data_(new double[other.size_]) {
        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];
    }
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            double* fresh = new double[other.size_];
            for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i];
            delete[] data_;
            data_ = fresh;
            size_ = other.size_;
        }
        return *this;
    }
    ~Buffer() { delete[] data_; }

    // TODO: Buffer(Buffer&& other) noexcept
    // TODO: Buffer& operator=(Buffer&& other) noexcept

    int size() const { return size_; }
    double get(int i) const { return data_[i]; }
    const double* data() const { return data_; }

private:
    int size_;
    double* data_;
};
```

Reference solution:

```cpp
// A buffer of doubles on the heap. It copies correctly already.
// Add a move constructor and a move assignment: each takes the other buffer's block
// and leaves it empty (size 0, data() null). Neither may allocate, and both must be noexcept.
// The move assignment must be safe for `a = std::move(a)`.
class Buffer {
public:
    Buffer(int n, double x) : size_(n), data_(new double[n]) {
        for (int i = 0; i < n; ++i) data_[i] = x;
    }
    Buffer(const Buffer& other) : size_(other.size_), data_(new double[other.size_]) {
        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];
    }
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            double* fresh = new double[other.size_];
            for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i];
            delete[] data_;
            data_ = fresh;
            size_ = other.size_;
        }
        return *this;
    }
    ~Buffer() { delete[] data_; }

    Buffer(Buffer&& other) noexcept : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

    int size() const { return size_; }
    double get(int i) const { return data_[i]; }
    const double* data() const { return data_; }

private:
    int size_;
    double* data_;
};
```

Hidden tests (`setup` then `call`, with its `expect`):

- `Buffer a(3, 1.5); Buffer b = std::move(a); b.size()` expects `3` (`equal`)
- `Buffer a(3, 1.5); Buffer b = std::move(a); a.size()` expects `0` (`equal`)
- `Buffer a(3, 1.5); Buffer b = std::move(a); b.get(2)` expects `1.5` (`isclose`)
- `Buffer a(1000, 2.0); reset_alloc_count(); Buffer b = std::move(a); alloc_count()` expects `0` (`equal`)
- `Buffer a(4, 1.0); Buffer b(2, 9.0); b = std::move(a); b.size()` expects `4` (`equal`)
- `Buffer a(4, 1.0); Buffer b(2, 9.0); b = std::move(a); a.size()` expects `0` (`equal`)
- `Buffer a(1000, 2.0); Buffer b(2, 9.0); reset_alloc_count(); b = std::move(a); alloc_count()` expects `0` (`equal`)
- `Buffer a(3, 4.0); Buffer& r = a; a = std::move(r); a.size()` expects `3` (`equal`)
- `Buffer a(3, 1.5); Buffer b = std::move(a); a.data() == nullptr` expects `true` (`equal`)
- `Buffer a(4, 1.0); Buffer b(2, 9.0); b = std::move(a); a.data() == nullptr` expects `true` (`equal`)
- `std::is_nothrow_move_constructible_v<Buffer>` expects `true` (`equal`)
- `std::is_nothrow_move_assignable_v<Buffer>` expects `true` (`equal`)
- `std::vector<Buffer> v; v.reserve(2); v.push_back(Buffer(100, 1.0)); v.push_back(Buffer(100, 2.0)); reset_alloc_count(); v.push_back(Buffer(100, 3.0)); alloc_count()` expects `2` (`equal`)
- `Buffer a(3, 1.0); Buffer b = std::move(a); a = Buffer(2, 7.0); a.get(1)` expects `7.0` (`isclose`)
- `Buffer a(4, 1.0); Buffer b(2, 9.0); b = std::move(a); b.get(3)` expects `1.0` (`isclose`)

Note: Extends the l11 `Buffer(int n, double x)` (say "the l11 `Buffer`" in the prose): l11 asked for `= default` moves, here the learner writes them. The commonest slip, a move that zeroes the size but leaves the pointer set (so two buffers `delete[]` one block), is caught by the two `data() == nullptr` tests, not by the allocator: the app's allocator frees twice silently, and `leakCheck` does not see a double free. The starter comment says the move assignment must be safe for `a = std::move(a)`. A test of `std::vector<Buffer>` growth reads the allocation count: 2 with a `noexcept` move (the new block and the temporary), 4 when the move is not `noexcept` (the two old elements are copied) and 5 when there is no move at all (checked by `check_growth_allocs.py`).

Checked by `docs/briefs/cpp-scripts/run_all.py` (each test as its own process, as the app runs them; `-O1 -fno-exceptions`):

```text
[P-move-buffer] solution g++ c++17: 0 of 15 failed OK
[P-move-buffer] solution clang++ c++17: 0 of 15 failed OK
[P-move-buffer] solution g++ c++20: 0 of 15 failed OK
[P-move-buffer] solution clang++ c++20: 0 of 15 failed OK
[P-move-buffer] starter g++ c++17: 9 of 15 failed OK
[P-move-buffer] starter clang++ c++17: 9 of 15 failed OK
[P-move-buffer] starter g++ c++20: 9 of 15 failed OK
[P-move-buffer] starter clang++ c++20: 9 of 15 failed OK
[P-move-buffer] solution under -fsanitize=undefined g++ c++17: 0 of 15 failed OK
[P-move-buffer] solution under -fsanitize=undefined g++ c++20: 0 of 15 failed OK
```

Plausible learner slips (mutants of the solution), each failing at least one test in every native compiler and standard (caught 28 of 28 runs): `assign-leaks-old-block`, `move-assign-forgets-null`, `move-ctor-forgets-null`, `move-that-copies`, `no-noexcept`, `no-self-guard`, `source-not-emptied`.

Checked in the app's own toolchain (`cpp-scripts/app_toolchain/`: YoWASP clang 21, libc++ in debug hardening, the app's own `unit()` from `cpp-grade.js`, its `leakCheck` and `allocCheck` wrappers, one process per test, `-std=c++17` and `-std=c++20` at `-O1`), `results_app.txt`:

```text
[P-move-buffer] c++17 solution: 0 of 15 failed  OK
[P-move-buffer] c++17 starter: 9 of 15 failed  OK
[P-move-buffer] c++17 mut:no-noexcept: 3 of 15 failed  caught
[P-move-buffer] c++17 mut:assign-leaks-old-block: 5 of 15 failed  caught
[P-move-buffer] c++17 mut:no-self-guard: 1 of 15 failed  caught
[P-move-buffer] c++17 mut:source-not-emptied: 2 of 15 failed  caught
[P-move-buffer] c++17 mut:move-ctor-forgets-null: 1 of 15 failed  caught
[P-move-buffer] c++17 mut:move-assign-forgets-null: 1 of 15 failed  caught
[P-move-buffer] c++17 mut:move-that-copies: 3 of 15 failed  caught
[P-move-buffer] c++20 solution: 0 of 15 failed  OK
[P-move-buffer] c++20 starter: 9 of 15 failed  OK
[P-move-buffer] c++20 mut:no-noexcept: 3 of 15 failed  caught
[P-move-buffer] c++20 mut:assign-leaks-old-block: 5 of 15 failed  caught
[P-move-buffer] c++20 mut:no-self-guard: 1 of 15 failed  caught
[P-move-buffer] c++20 mut:source-not-emptied: 2 of 15 failed  caught
[P-move-buffer] c++20 mut:move-ctor-forgets-null: 1 of 15 failed  caught
[P-move-buffer] c++20 mut:move-assign-forgets-null: 1 of 15 failed  caught
[P-move-buffer] c++20 mut:move-that-copies: 3 of 15 failed  caught
```

### P-copy-samples

Where: `l20-rule-of-five`, screen 6 (ladder), a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 13 hidden tests (function mode, `compare: "equal"` for integers, booleans and strings, `isclose` for doubles). Flags: allocCheck: true, leakCheck: true. `examples` are the first two tests.

`how`: "Submit runs 13 hidden tests. `alloc_count()` counts calls to `operator new` and `new[]`: a copy must allocate once. A block never freed fails its test."

Hidden `prelude`:

```cpp
#include <utility>
#include <type_traits>
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <utility>

// Samples owns a heap array of doubles. The destructor and the two move members are done.
// The copy constructor and copy assignment are wrong: they copy the pointer, so two objects
// would free one block. Make each a true copy of the doubles.
// Copy assignment must free the old block, be safe for `a = a`, and return *this.
class Samples {
public:
    Samples(int n, double x) : size_(n), data_(new double[n]) {
        for (int i = 0; i < n; ++i) data_[i] = x;
    }
    ~Samples() { delete[] data_; }
    Samples(Samples&& other) noexcept : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }
    Samples& operator=(Samples&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

    // TODO: copy the doubles, not the pointer
    Samples(const Samples& other) : size_(other.size_), data_(other.data_) {}
    // TODO: free the old block, copy the doubles, guard against a = a, return *this
    Samples& operator=(const Samples& other) {
        size_ = other.size_;
        data_ = other.data_;
        return *this;
    }

    int size() const { return size_; }
    double get(int i) const { return data_[i]; }
    void set(int i, double x) { data_[i] = x; }

private:
    int size_;
    double* data_;
};
```

Reference solution:

```cpp
#include <utility>

// Samples owns a heap array of doubles. The destructor and the two move members are done.
// The copy constructor and copy assignment are wrong: they copy the pointer, so two objects
// would free one block. Make each a true copy of the doubles.
// Copy assignment must free the old block, be safe for `a = a`, and return *this.
class Samples {
public:
    Samples(int n, double x) : size_(n), data_(new double[n]) {
        for (int i = 0; i < n; ++i) data_[i] = x;
    }
    ~Samples() { delete[] data_; }
    Samples(Samples&& other) noexcept : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }
    Samples& operator=(Samples&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

    Samples(const Samples& other) : size_(other.size_), data_(new double[other.size_]) {
        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];
    }
    Samples& operator=(const Samples& other) {
        if (this != &other) {
            double* fresh = new double[other.size_];
            for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i];
            delete[] data_;
            data_ = fresh;
            size_ = other.size_;
        }
        return *this;
    }

    int size() const { return size_; }
    double get(int i) const { return data_[i]; }
    void set(int i, double x) { data_[i] = x; }

private:
    int size_;
    double* data_;
};
```

Hidden tests (`setup` then `call`, with its `expect`):

- `Samples a(3, 1.5); Samples b = a; b.set(0, 9.0); a.get(0)` expects `1.5` (`isclose`)
- `Samples a(3, 1.5); Samples b = a; b.set(0, 9.0); b.get(0)` expects `9.0` (`isclose`)
- `Samples a(3, 1.5); Samples b = a; b.size()` expects `3` (`equal`)
- `Samples a(3, 1.5); Samples b = a; b.get(2)` expects `1.5` (`isclose`)
- `Samples a(1000, 0.5); reset_alloc_count(); Samples b = a; alloc_count()` expects `1` (`equal`)
- `Samples a(3, 1.5); Samples b(2, 0.0); b = a; b.set(1, 7.0); a.get(1)` expects `1.5` (`isclose`)
- `Samples a(3, 1.5); Samples b(2, 0.0); b = a; b.size()` expects `3` (`equal`)
- `Samples a(1000, 0.5); Samples b(2, 0.0); reset_alloc_count(); b = a; alloc_count()` expects `1` (`equal`)
- `Samples a(10, 1.5); Samples& r = a; a = r; a.get(0) + a.get(1)` expects `3.0` (`isclose`)
- `Samples a(2, 1.0); Samples b(5, 2.0); Samples c(1, 3.0); c = b = a; c.size()` expects `2` (`equal`)
- `Samples a(0, 0.0); Samples b = a; b.size()` expects `0` (`equal`)
- `Samples a(3, 1.5); Samples b = std::move(a); a.size()` expects `0` (`equal`)
- `Samples a(5, 2.5); Samples b(1, 0.0); b = a; b.get(4)` expects `2.5` (`isclose`)

Note: WAITING ON AN ENGINE ITEM. A delete-first assignment (`delete[] data_; data_ = new double[n]; copy from other`) misbehaves only for `a = a`, by reading the block it has just freed. No test can make that read deterministic: the app's allocator leaves the old contents in place, so the copy usually succeeds and the slip passes 13 of 13 in the app (it was caught natively only because glibc overwrote the block). The `a = a` test therefore stays as a well-defined check that a correct solution keeps its data, and the slip is listed as not caught. It needs the harness to poison freed blocks or to expose the order of `new` and `delete`: the [Must] under "Raised later (cpp L5 brief, 5 Nov)" in `docs/BACKLOG-INBOX.md`. Do not describe `a = a` to the learner as exposing delete-first.

Checked by `docs/briefs/cpp-scripts/run_all.py` (each test as its own process, as the app runs them; `-O1 -fno-exceptions`):

```text
[P-copy-samples] solution g++ c++17: 0 of 13 failed OK
[P-copy-samples] solution clang++ c++17: 0 of 13 failed OK
[P-copy-samples] solution g++ c++20: 0 of 13 failed OK
[P-copy-samples] solution clang++ c++20: 0 of 13 failed OK
[P-copy-samples] starter g++ c++17: 11 of 13 failed OK
[P-copy-samples] starter clang++ c++17: 11 of 13 failed OK
[P-copy-samples] starter g++ c++20: 11 of 13 failed OK
[P-copy-samples] starter clang++ c++20: 11 of 13 failed OK
[P-copy-samples] solution under -fsanitize=undefined g++ c++17: 0 of 13 failed OK
[P-copy-samples] solution under -fsanitize=undefined g++ c++20: 0 of 13 failed OK
```

Plausible learner slips (mutants of the solution), each failing at least one test in every native compiler and standard (caught 16 of 16 runs): `assign-copies-twice`, `assign-leaks-old-block`, `assign-shallow-only`, `ctor-copies-size-only`.

Known gap, not counted as caught: `delete-first-no-guard` (see the note above; it waits on the [Must] in `docs/BACKLOG-INBOX.md`).

Checked in the app's own toolchain (`cpp-scripts/app_toolchain/`: YoWASP clang 21, libc++ in debug hardening, the app's own `unit()` from `cpp-grade.js`, its `leakCheck` and `allocCheck` wrappers, one process per test, `-std=c++17` and `-std=c++20` at `-O1`), `results_app.txt`:

```text
[P-copy-samples] c++17 solution: 0 of 13 failed  OK
[P-copy-samples] c++17 starter: 7 of 13 failed  OK
[P-copy-samples] c++17 mut:assign-leaks-old-block: 5 of 13 failed  caught
[P-copy-samples] c++17 mut:assign-copies-twice: 1 of 13 failed  caught
[P-copy-samples] c++17 mut:ctor-copies-size-only: 1 of 13 failed  caught
[P-copy-samples] c++17 mut:assign-shallow-only: 2 of 13 failed  caught
[P-copy-samples] c++17 unc:delete-first-no-guard: 0 of 13 failed  not caught (known gap)
[P-copy-samples] c++20 solution: 0 of 13 failed  OK
[P-copy-samples] c++20 starter: 7 of 13 failed  OK
[P-copy-samples] c++20 mut:assign-leaks-old-block: 5 of 13 failed  caught
[P-copy-samples] c++20 mut:assign-copies-twice: 1 of 13 failed  caught
[P-copy-samples] c++20 mut:ctor-copies-size-only: 1 of 13 failed  caught
[P-copy-samples] c++20 mut:assign-shallow-only: 2 of 13 failed  caught
[P-copy-samples] c++20 unc:delete-first-no-guard: 0 of 13 failed  not caught (known gap)
```

### P-hand-vtable

Where: `l21-virtual-dispatch`, screen 6 (ladder), a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 11 hidden tests (function mode, `compare: "equal"` for integers, booleans and strings, `isclose` for doubles). Flags: leakCheck: true. `examples` are the first two tests.

`how`: "Submit runs 11 hidden tests. Each call goes through the object's own table; two objects of one kind must share one table."

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <algorithm>

// A virtual call by hand. Every Payoff holds a pointer to a table of functions,
// as the compiler arranges for a class with virtual functions.
struct Payoff;
struct PayoffTable {
    double (*value)(const Payoff* self, double spot);
};
struct Payoff {
    const PayoffTable* table;    // the "vptr": which table this object uses
    double strike;
};

// What `p->value(spot)` compiles to: find the object's table, call the function in it.
double value_of(const Payoff* p, double spot) {
    return 0.0;    // TODO
}

// TODO: the three functions: call max(spot - strike, 0), put max(strike - spot, 0),
// digital 1 if spot > strike else 0.
double call_value(const Payoff* self, double spot) { return 0.0; }
double put_value(const Payoff* self, double spot) { return 0.0; }
double digital_value(const Payoff* self, double spot) { return 0.0; }

// TODO: one table per kind, shared by every object of that kind.
const PayoffTable call_table = { nullptr };
const PayoffTable put_table = { nullptr };
const PayoffTable digital_table = { nullptr };

// TODO: each maker builds a Payoff that points at the right table.
Payoff make_call(double strike) { return Payoff{ nullptr, strike }; }
Payoff make_put(double strike) { return Payoff{ nullptr, strike }; }
Payoff make_digital(double strike) { return Payoff{ nullptr, strike }; }
```

Reference solution:

```cpp
#include <algorithm>

// A virtual call by hand. Every Payoff holds a pointer to a table of functions,
// as the compiler arranges for a class with virtual functions.
struct Payoff;
struct PayoffTable {
    double (*value)(const Payoff* self, double spot);
};
struct Payoff {
    const PayoffTable* table;    // the "vptr": which table this object uses
    double strike;
};

// What `p->value(spot)` compiles to: find the object's table, call the function in it.
double value_of(const Payoff* p, double spot) {
    return p->table->value(p, spot);
}

double call_value(const Payoff* self, double spot) { return std::max(spot - self->strike, 0.0); }
double put_value(const Payoff* self, double spot) { return std::max(self->strike - spot, 0.0); }
double digital_value(const Payoff* self, double spot) { return spot > self->strike ? 1.0 : 0.0; }

const PayoffTable call_table = { call_value };
const PayoffTable put_table = { put_value };
const PayoffTable digital_table = { digital_value };

Payoff make_call(double strike) { return Payoff{ &call_table, strike }; }
Payoff make_put(double strike) { return Payoff{ &put_table, strike }; }
Payoff make_digital(double strike) { return Payoff{ &digital_table, strike }; }
```

Hidden tests (`setup` then `call`, with its `expect`):

- `Payoff c = make_call(100); value_of(&c, 110.0)` expects `10.0` (`isclose`)
- `Payoff c = make_call(100); value_of(&c, 90.0)` expects `0.0` (`isclose`)
- `Payoff p = make_put(100); value_of(&p, 90.0)` expects `10.0` (`isclose`)
- `Payoff p = make_put(100); value_of(&p, 110.0)` expects `0.0` (`isclose`)
- `Payoff d = make_digital(100); value_of(&d, 101.0)` expects `1.0` (`isclose`)
- `Payoff d = make_digital(100); value_of(&d, 100.0)` expects `0.0` (`isclose`)
- `Payoff c = make_call(80); value_of(&c, 100.0)` expects `20.0` (`isclose`)
- `Payoff a = make_call(100); Payoff b = make_call(90); a.table == b.table` expects `true` (`equal`)
- `Payoff a = make_call(100); Payoff b = make_put(100); a.table != b.table` expects `true` (`equal`)
- `Payoff c = make_call(100); Payoff p = make_put(100); Payoff d = make_digital(100); const Payoff* book[3] = {&c, &p, &d}; double total = 0.0; for (const Payoff* x : book) total += value_of(x, 105.0); total` expects `6.0` (`isclose`)
- `Payoff d = make_digital(100); value_of(&d, 99.0)` expects `0.0` (`isclose`)

Note: Function mode; the tests build the objects in `setup`.

Checked by `docs/briefs/cpp-scripts/run_all.py` (each test as its own process, as the app runs them; `-O1 -fno-exceptions`):

```text
[P-hand-vtable] solution g++ c++17: 0 of 11 failed OK
[P-hand-vtable] solution clang++ c++17: 0 of 11 failed OK
[P-hand-vtable] solution g++ c++20: 0 of 11 failed OK
[P-hand-vtable] solution clang++ c++20: 0 of 11 failed OK
[P-hand-vtable] starter g++ c++17: 6 of 11 failed OK
[P-hand-vtable] starter clang++ c++17: 6 of 11 failed OK
[P-hand-vtable] starter g++ c++20: 6 of 11 failed OK
[P-hand-vtable] starter clang++ c++20: 6 of 11 failed OK
[P-hand-vtable] solution under -fsanitize=undefined g++ c++17: 0 of 11 failed OK
[P-hand-vtable] solution under -fsanitize=undefined g++ c++20: 0 of 11 failed OK
```

Plausible learner slips (mutants of the solution), each failing at least one test in every native compiler and standard (caught 20 of 20 runs): `a-new-table-per-object`, `digital-priced-as-call`, `digital-uses-greater-or-equal`, `tables-swapped`, `value_of-passes-the-wrong-spot`.

Checked in the app's own toolchain (`cpp-scripts/app_toolchain/`: YoWASP clang 21, libc++ in debug hardening, the app's own `unit()` from `cpp-grade.js`, its `leakCheck` and `allocCheck` wrappers, one process per test, `-std=c++17` and `-std=c++20` at `-O1`), `results_app.txt`:

```text
[P-hand-vtable] c++17 solution: 0 of 11 failed  OK
[P-hand-vtable] c++17 starter: 6 of 11 failed  OK
[P-hand-vtable] c++17 mut:value_of-passes-the-wrong-spot: 5 of 11 failed  caught
[P-hand-vtable] c++17 mut:tables-swapped: 5 of 11 failed  caught
[P-hand-vtable] c++17 mut:digital-priced-as-call: 1 of 11 failed  caught
[P-hand-vtable] c++17 mut:a-new-table-per-object: 6 of 11 failed  caught
[P-hand-vtable] c++17 mut:digital-uses-greater-or-equal: 1 of 11 failed  caught
[P-hand-vtable] c++20 solution: 0 of 11 failed  OK
[P-hand-vtable] c++20 starter: 6 of 11 failed  OK
[P-hand-vtable] c++20 mut:value_of-passes-the-wrong-spot: 5 of 11 failed  caught
[P-hand-vtable] c++20 mut:tables-swapped: 5 of 11 failed  caught
[P-hand-vtable] c++20 mut:digital-priced-as-call: 1 of 11 failed  caught
[P-hand-vtable] c++20 mut:a-new-table-per-object: 6 of 11 failed  caught
[P-hand-vtable] c++20 mut:digital-uses-greater-or-equal: 1 of 11 failed  caught
```

### P-add-overflows

Where: `l22-undefined-behaviour`, screen 5 (ladder), a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 13 hidden tests (function mode, `compare: "equal"` for integers, booleans and strings, `isclose` for doubles). Flags: none. `examples` are the first two tests.

`how`: "Submit runs 13 hidden tests. Each answer is `true` when `a + b` does not fit in an `int`, and every test uses values the correct check handles without overflowing."

Hidden `prelude`:

```cpp
#include <climits>
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <climits>

// Return true if a + b does not fit in an int. The check itself must never overflow.
bool add_overflows(int a, int b) {
    return a + b > INT_MAX;    // TODO: this looks at the sum after it has already overflowed
}
```

Reference solution:

```cpp
#include <climits>

// Return true if a + b does not fit in an int. The check itself must never overflow.
bool add_overflows(int a, int b) {
    if (b > 0) return a > INT_MAX - b;
    return a < INT_MIN - b;
}
```

Hidden tests (`setup` then `call`, with its `expect`):

- `add_overflows(INT_MAX, 1)` expects `true` (`equal`)
- `add_overflows(INT_MAX, 0)` expects `false` (`equal`)
- `add_overflows(INT_MIN, -1)` expects `true` (`equal`)
- `add_overflows(INT_MIN, 0)` expects `false` (`equal`)
- `add_overflows(2000000000, 2000000000)` expects `true` (`equal`)
- `add_overflows(1000, 2000)` expects `false` (`equal`)
- `add_overflows(-2000000000, -2000000000)` expects `true` (`equal`)
- `add_overflows(INT_MAX, -1)` expects `false` (`equal`)
- `add_overflows(INT_MIN, 1)` expects `false` (`equal`)
- `add_overflows(1073741824, 1073741824)` expects `true` (`equal`)
- `add_overflows(1073741823, 1073741824)` expects `false` (`equal`)
- `add_overflows(INT_MAX, INT_MAX)` expects `true` (`equal`)
- `add_overflows(INT_MIN, INT_MIN)` expects `true` (`equal`)

Note: Do not set `compare: "raises"`. Tests only use `INT_MAX`, `INT_MIN` and nearby values; a widening solution (`long long` sum) passes too, which is checked. The starter fails whatever the compiler does with its undefined line. A learner's post-check solution (`int s = a + b; return (b > 0 && s < a) || (b < 0 && s > a);`) is another matter: it fails 7 of 13 in the app (clang 21 `-O1` folds the check) and passes 13 of 13 under g++ 13 `-O1`. Whether an undefined solution is caught depends on the optimiser, so the hidden tests double as an optimiser test: say so in the author's notes and in l22 S5's explain, and promise no failing row for every undefined solution.

Checked by `docs/briefs/cpp-scripts/run_all.py` (each test as its own process, as the app runs them; `-O1 -fno-exceptions`):

```text
[P-add-overflows] solution g++ c++17: 0 of 13 failed OK
[P-add-overflows] solution clang++ c++17: 0 of 13 failed OK
[P-add-overflows] solution g++ c++20: 0 of 13 failed OK
[P-add-overflows] solution clang++ c++20: 0 of 13 failed OK
[P-add-overflows] starter g++ c++17: 7 of 13 failed OK
[P-add-overflows] starter clang++ c++17: 7 of 13 failed OK
[P-add-overflows] starter g++ c++20: 7 of 13 failed OK
[P-add-overflows] starter clang++ c++20: 7 of 13 failed OK
[P-add-overflows] alt solution widen-to-64-bit g++ c++17: 0 of 13 failed OK
[P-add-overflows] alt solution widen-to-64-bit clang++ c++17: 0 of 13 failed OK
[P-add-overflows] alt solution widen-to-64-bit g++ c++20: 0 of 13 failed OK
[P-add-overflows] alt solution widen-to-64-bit clang++ c++20: 0 of 13 failed OK
[P-add-overflows] solution under -fsanitize=undefined g++ c++17: 0 of 13 failed OK
[P-add-overflows] solution under -fsanitize=undefined g++ c++20: 0 of 13 failed OK
```

Plausible learner slips (mutants of the solution), each failing at least one test in every native compiler and standard (caught 12 of 12 runs): `off-by-one`, `only-checks-the-top`, `unsigned-wrap-guess`.

Checked in the app's own toolchain (`cpp-scripts/app_toolchain/`: YoWASP clang 21, libc++ in debug hardening, the app's own `unit()` from `cpp-grade.js`, its `leakCheck` and `allocCheck` wrappers, one process per test, `-std=c++17` and `-std=c++20` at `-O1`), `results_app.txt`:

```text
[P-add-overflows] c++17 solution: 0 of 13 failed  OK
[P-add-overflows] c++17 starter: 7 of 13 failed  OK
[P-add-overflows] c++17 mut:only-checks-the-top: 3 of 13 failed  caught
[P-add-overflows] c++17 mut:off-by-one: 1 of 13 failed  caught
[P-add-overflows] c++17 mut:unsigned-wrap-guess: 5 of 13 failed  caught
[P-add-overflows] c++17 alt:widen-to-64-bit: 0 of 13 failed  OK
[P-add-overflows] c++20 solution: 0 of 13 failed  OK
[P-add-overflows] c++20 starter: 7 of 13 failed  OK
[P-add-overflows] c++20 mut:only-checks-the-top: 3 of 13 failed  caught
[P-add-overflows] c++20 mut:off-by-one: 1 of 13 failed  caught
[P-add-overflows] c++20 mut:unsigned-wrap-guess: 5 of 13 failed  caught
[P-add-overflows] c++20 alt:widen-to-64-bit: 0 of 13 failed  OK
```

### P-unique-ptr

Where: `l23-own-smart-pointer`, screen 3 (ladder), a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 15 hidden tests (function mode, `compare: "equal"` for integers, booleans and strings, `isclose` for doubles). Flags: leakCheck: true. `examples` are the first two tests.

`how`: "Submit runs 15 hidden tests. A hidden `Tracked` type counts live objects, so an object deleted twice or never shows in the count; two compile checks fail if copying is allowed."

Hidden `prelude`:

```cpp
#include <utility>
#include <vector>
#include <type_traits>

// Hidden: counts how many Tracked objects are alive.
struct Tracked {
    static inline int live = 0;
    int v;
    explicit Tracked(int x) : v(x) { ++live; }
    ~Tracked() { --live; }
};
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
// A minimal unique pointer. It owns one heap object, or nothing.
// Write: the destructor; copying deleted; a move constructor and move assignment that
// transfer ownership and leave the source empty; release(); reset().
// The move assignment must be safe for `a = std::move(a)`.
template <typename T>
class UniquePtr {
public:
    UniquePtr() = default;
    explicit UniquePtr(T* p) : ptr_(p) {}

    // TODO: destructor
    // TODO: delete copying; write the move constructor and move assignment

    T* get() const { return ptr_; }
    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }
    explicit operator bool() const { return ptr_ != nullptr; }

    T* release() { return nullptr; }                 // TODO: give up ownership, do not delete
    void reset(T* p = nullptr) { (void)p; }          // TODO: delete the current object, then own p

private:
    T* ptr_ = nullptr;
};
```

Reference solution:

```cpp
// A minimal unique pointer. It owns one heap object, or nothing.
// Write: the destructor; copying deleted; a move constructor and move assignment that
// transfer ownership and leave the source empty; release(); reset().
// The move assignment must be safe for `a = std::move(a)`.
template <typename T>
class UniquePtr {
public:
    UniquePtr() = default;
    explicit UniquePtr(T* p) : ptr_(p) {}

    ~UniquePtr() { delete ptr_; }
    UniquePtr(const UniquePtr&) = delete;
    UniquePtr& operator=(const UniquePtr&) = delete;
    UniquePtr(UniquePtr&& other) noexcept : ptr_(other.ptr_) { other.ptr_ = nullptr; }
    UniquePtr& operator=(UniquePtr&& other) noexcept {
        if (this != &other) {
            delete ptr_;
            ptr_ = other.ptr_;
            other.ptr_ = nullptr;
        }
        return *this;
    }

    T* get() const { return ptr_; }
    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }
    explicit operator bool() const { return ptr_ != nullptr; }

    T* release() {
        T* p = ptr_;
        ptr_ = nullptr;
        return p;
    }
    void reset(T* p = nullptr) {
        T* old = ptr_;
        ptr_ = p;
        delete old;
    }

private:
    T* ptr_ = nullptr;
};
```

Hidden tests (`setup` then `call`, with its `expect`):

- `{ UniquePtr<Tracked> p(new Tracked(5)); } Tracked::live` expects `0` (`equal`)
- `UniquePtr<Tracked> p(new Tracked(5)); p->v + (*p).v` expects `10` (`equal`)
- `UniquePtr<Tracked> a(new Tracked(1)); UniquePtr<Tracked> b = std::move(a); b->v` expects `1` (`equal`)
- `UniquePtr<Tracked> a(new Tracked(1)); UniquePtr<Tracked> b = std::move(a); a.get() == nullptr` expects `true` (`equal`)
- `{ UniquePtr<Tracked> a(new Tracked(1)); UniquePtr<Tracked> b = std::move(a); } Tracked::live` expects `0` (`equal`)
- compiles: `UniquePtr<Tracked> b = a;` (with `UniquePtr<Tracked> a;`) expects `false` (it must not compile)
- compiles: `UniquePtr<Tracked> b; b = a;` (with `UniquePtr<Tracked> a;`) expects `false` (it must not compile)
- `UniquePtr<Tracked> a(new Tracked(3)); Tracked* raw = a.release(); int live_after = Tracked::live; delete raw; live_after` expects `1` (`equal`)
- `UniquePtr<Tracked> a(new Tracked(3)); Tracked* raw = a.release(); delete raw; a.get() == nullptr` expects `true` (`equal`)
- `UniquePtr<Tracked> a(new Tracked(1)); a.reset(new Tracked(2)); Tracked::live * 10 + a->v` expects `12` (`equal`)
- `UniquePtr<Tracked> a(new Tracked(1)); a.reset(); Tracked::live` expects `0` (`equal`)
- `UniquePtr<Tracked> a(new Tracked(1)); UniquePtr<Tracked> b(new Tracked(2)); b = std::move(a); Tracked::live` expects `1` (`equal`)
- `UniquePtr<Tracked> a(new Tracked(4)); UniquePtr<Tracked>& r = a; a = std::move(r); a.get() != nullptr` expects `true` (`equal`)
- `std::is_nothrow_move_constructible_v<UniquePtr<Tracked>>` expects `true` (`equal`)
- `UniquePtr<Tracked> p; UniquePtr<Tracked> q(new Tracked(1)); (p ? 10 : 0) + (q ? 1 : 0)` expects `1` (`equal`)

Note: Two of the 15 are `compiles` cases (they pass when the snippet does not compile). A file with an unrelated compile error shows that error and no rows, so the `how` must not say the checks "confirm" anything on such a file. The starter comment says the move assignment must be safe for `a = std::move(a)`; the self-move test reads the pointer value (non-null), never freed memory.

Checked by `docs/briefs/cpp-scripts/run_all.py` (each test as its own process, as the app runs them; `-O1 -fno-exceptions`):

```text
[P-unique-ptr] solution g++ c++17: 0 of 15 failed OK
[P-unique-ptr] solution clang++ c++17: 0 of 15 failed OK
[P-unique-ptr] solution g++ c++20: 0 of 15 failed OK
[P-unique-ptr] solution clang++ c++20: 0 of 15 failed OK
[P-unique-ptr] starter g++ c++17: 11 of 15 failed OK
[P-unique-ptr] starter clang++ c++17: 14 of 15 failed OK
[P-unique-ptr] starter g++ c++20: 11 of 15 failed OK
[P-unique-ptr] starter clang++ c++20: 14 of 15 failed OK
[P-unique-ptr] solution under -fsanitize=undefined g++ c++17: 0 of 15 failed OK
[P-unique-ptr] solution under -fsanitize=undefined g++ c++20: 0 of 15 failed OK
```

Plausible learner slips (mutants of the solution), each failing at least one test in every native compiler and standard (caught 32 of 32 runs): `copy-not-deleted`, `move-assign-leaks-old`, `move-assign-no-self-guard`, `move-does-not-empty-source`, `move-not-noexcept`, `no-destructor`, `release-deletes`, `reset-leaks-old`.

Checked in the app's own toolchain (`cpp-scripts/app_toolchain/`: YoWASP clang 21, libc++ in debug hardening, the app's own `unit()` from `cpp-grade.js`, its `leakCheck` and `allocCheck` wrappers, one process per test, `-std=c++17` and `-std=c++20` at `-O1`), `results_app.txt`:

```text
[P-unique-ptr] c++17 solution: 0 of 15 failed  OK
[P-unique-ptr] c++17 starter: 14 of 15 failed  OK
[P-unique-ptr] c++17 mut:no-destructor: 9 of 15 failed  caught
[P-unique-ptr] c++17 mut:move-does-not-empty-source: 2 of 15 failed  caught
[P-unique-ptr] c++17 mut:copy-not-deleted: 2 of 15 failed  caught
[P-unique-ptr] c++17 mut:release-deletes: 1 of 15 failed  caught
[P-unique-ptr] c++17 mut:reset-leaks-old: 2 of 15 failed  caught
[P-unique-ptr] c++17 mut:move-assign-leaks-old: 1 of 15 failed  caught
[P-unique-ptr] c++17 mut:move-assign-no-self-guard: 1 of 15 failed  caught
[P-unique-ptr] c++17 mut:move-not-noexcept: 1 of 15 failed  caught
[P-unique-ptr] c++20 solution: 0 of 15 failed  OK
[P-unique-ptr] c++20 starter: 14 of 15 failed  OK
[P-unique-ptr] c++20 mut:no-destructor: 9 of 15 failed  caught
[P-unique-ptr] c++20 mut:move-does-not-empty-source: 2 of 15 failed  caught
[P-unique-ptr] c++20 mut:copy-not-deleted: 2 of 15 failed  caught
[P-unique-ptr] c++20 mut:release-deletes: 1 of 15 failed  caught
[P-unique-ptr] c++20 mut:reset-leaks-old: 2 of 15 failed  caught
[P-unique-ptr] c++20 mut:move-assign-leaks-old: 1 of 15 failed  caught
[P-unique-ptr] c++20 mut:move-assign-no-self-guard: 1 of 15 failed  caught
[P-unique-ptr] c++20 mut:move-not-noexcept: 1 of 15 failed  caught
```

### P-shared-ptr

Where: `l23-own-smart-pointer`, screen 6 (ladder), a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 15 hidden tests (function mode, `compare: "equal"` for integers, booleans and strings, `isclose` for doubles). Flags: leakCheck: true. `examples` are the first two tests.

`how`: "Submit runs 15 hidden tests. A hidden `Tracked` type counts live objects; `leakCheck` also fails a test whose counter block is never freed."

Hidden `prelude`:

```cpp
#include <utility>
#include <vector>
#include <type_traits>

// Hidden: counts how many Tracked objects are alive.
struct Tracked {
    static inline int live = 0;
    int v;
    explicit Tracked(int x) : v(x) { ++live; }
    ~Tracked() { --live; }
};
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
// A minimal reference-counted pointer. All owners share one heap counter next to the object.
// The object is deleted, and the counter freed, when the last owner goes.
// Write: the copy and move members and the destructor. use_count() is 0 for an empty pointer.
template <typename T>
class SharedPtr {
public:
    SharedPtr() = default;
    explicit SharedPtr(T* p) : ptr_(p), count_(p ? new long(1) : nullptr) {}

    // TODO: copy constructor: share the object and add one to the count
    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) {}
    // TODO: copy assignment: let go of the old object, share the new one
    SharedPtr& operator=(const SharedPtr& other) {
        ptr_ = other.ptr_;
        count_ = other.count_;
        return *this;
    }
    // TODO: move constructor and move assignment (noexcept): take over, leave the source empty
    // TODO: destructor: subtract one; at zero delete the object and the counter
    ~SharedPtr() {}

    long use_count() const { return count_ ? *count_ : 0; }
    T* get() const { return ptr_; }
    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }

private:
    T* ptr_ = nullptr;
    long* count_ = nullptr;
};
```

Reference solution:

```cpp
// A minimal reference-counted pointer. All owners share one heap counter next to the object.
// The object is deleted, and the counter freed, when the last owner goes.
// Write: the copy and move members and the destructor. use_count() is 0 for an empty pointer.
template <typename T>
class SharedPtr {
public:
    SharedPtr() = default;
    explicit SharedPtr(T* p) : ptr_(p), count_(p ? new long(1) : nullptr) {}

    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) {
        if (count_) ++*count_;
    }
    SharedPtr& operator=(const SharedPtr& other) {
        if (count_ != other.count_) {
            if (other.count_) ++*other.count_;
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
        }
        return *this;
    }
    SharedPtr(SharedPtr&& other) noexcept : ptr_(other.ptr_), count_(other.count_) {
        other.ptr_ = nullptr;
        other.count_ = nullptr;
    }
    SharedPtr& operator=(SharedPtr&& other) noexcept {
        if (this != &other) {
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
            other.ptr_ = nullptr;
            other.count_ = nullptr;
        }
        return *this;
    }
    ~SharedPtr() { drop(); }

    long use_count() const { return count_ ? *count_ : 0; }
    T* get() const { return ptr_; }
    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }

private:
    void drop() {
        if (count_ && --*count_ == 0) {
            delete ptr_;
            delete count_;
        }
        ptr_ = nullptr;
        count_ = nullptr;
    }
    T* ptr_ = nullptr;
    long* count_ = nullptr;
};
```

Hidden tests (`setup` then `call`, with its `expect`):

- `{ SharedPtr<Tracked> a(new Tracked(1)); } Tracked::live` expects `0` (`equal`)
- `SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b = a; a.use_count()` expects `2` (`equal`)
- `SharedPtr<Tracked> a(new Tracked(1)); { SharedPtr<Tracked> b = a; SharedPtr<Tracked> c = b; } a.use_count() * 10 + Tracked::live` expects `11` (`equal`)
- `{ SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b = a; } Tracked::live` expects `0` (`equal`)
- `SharedPtr<Tracked> a(new Tracked(1)); { SharedPtr<Tracked> b = a; } Tracked::live` expects `1` (`equal`)
- `SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b(new Tracked(2)); b = a; Tracked::live * 10 + a.use_count()` expects `12` (`equal`)
- `SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked>& r = a; a = r; Tracked::live * 10 + a.use_count()` expects `11` (`equal`)
- `SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b = std::move(a); b.use_count() * 10 + a.use_count()` expects `10` (`equal`)
- `{ SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b = std::move(a); } Tracked::live` expects `0` (`equal`)
- `SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b(new Tracked(2)); b = std::move(a); Tracked::live * 10 + b.use_count()` expects `11` (`equal`)
- `SharedPtr<Tracked> p; p.use_count() * 10 + (p.get() == nullptr ? 1 : 0)` expects `1` (`equal`)
- `SharedPtr<Tracked> a(new Tracked(8)); SharedPtr<Tracked> b = a; b->v + (*a).v` expects `16` (`equal`)
- `SharedPtr<Tracked> a(new Tracked(1)); std::vector<SharedPtr<Tracked>> v(5, a); a.use_count()` expects `6` (`equal`)
- `SharedPtr<Tracked> a(new Tracked(1)); { std::vector<SharedPtr<Tracked>> v(5, a); } a.use_count() * 10 + Tracked::live` expects `11` (`equal`)
- `std::is_nothrow_move_constructible_v<SharedPtr<Tracked>>` expects `true` (`equal`)

Note: The counter is a heap `long` shared by all owners (`new long(1)` is already in the starter's constructor).

Checked by `docs/briefs/cpp-scripts/run_all.py` (each test as its own process, as the app runs them; `-O1 -fno-exceptions`):

```text
[P-shared-ptr] solution g++ c++17: 0 of 15 failed OK
[P-shared-ptr] solution clang++ c++17: 0 of 15 failed OK
[P-shared-ptr] solution g++ c++20: 0 of 15 failed OK
[P-shared-ptr] solution clang++ c++20: 0 of 15 failed OK
[P-shared-ptr] starter g++ c++17: 14 of 15 failed OK
[P-shared-ptr] starter clang++ c++17: 14 of 15 failed OK
[P-shared-ptr] starter g++ c++20: 14 of 15 failed OK
[P-shared-ptr] starter clang++ c++20: 14 of 15 failed OK
[P-shared-ptr] solution under -fsanitize=undefined g++ c++17: 0 of 15 failed OK
[P-shared-ptr] solution under -fsanitize=undefined g++ c++20: 0 of 15 failed OK
```

Plausible learner slips (mutants of the solution), each failing at least one test in every native compiler and standard (caught 32 of 32 runs): `assign-decrements-first`, `assign-keeps-old`, `copy-does-not-count`, `counter-leaks`, `destructor-always-deletes`, `destructor-never-frees`, `move-copies-count`, `move-not-noexcept`.

Checked in the app's own toolchain (`cpp-scripts/app_toolchain/`: YoWASP clang 21, libc++ in debug hardening, the app's own `unit()` from `cpp-grade.js`, its `leakCheck` and `allocCheck` wrappers, one process per test, `-std=c++17` and `-std=c++20` at `-O1`), `results_app.txt`:

```text
[P-shared-ptr] c++17 solution: 0 of 15 failed  OK
[P-shared-ptr] c++17 starter: 14 of 15 failed  OK
[P-shared-ptr] c++17 mut:copy-does-not-count: 5 of 15 failed  caught
[P-shared-ptr] c++17 mut:destructor-never-frees: 13 of 15 failed  caught
[P-shared-ptr] c++17 mut:destructor-always-deletes: 13 of 15 failed  caught
[P-shared-ptr] c++17 mut:counter-leaks: 13 of 15 failed  caught
[P-shared-ptr] c++17 mut:assign-decrements-first: 1 of 15 failed  caught
[P-shared-ptr] c++17 mut:assign-keeps-old: 1 of 15 failed  caught
[P-shared-ptr] c++17 mut:move-copies-count: 1 of 15 failed  caught
[P-shared-ptr] c++17 mut:move-not-noexcept: 1 of 15 failed  caught
[P-shared-ptr] c++20 solution: 0 of 15 failed  OK
[P-shared-ptr] c++20 starter: 14 of 15 failed  OK
[P-shared-ptr] c++20 mut:copy-does-not-count: 5 of 15 failed  caught
[P-shared-ptr] c++20 mut:destructor-never-frees: 13 of 15 failed  caught
[P-shared-ptr] c++20 mut:destructor-always-deletes: 13 of 15 failed  caught
[P-shared-ptr] c++20 mut:counter-leaks: 13 of 15 failed  caught
[P-shared-ptr] c++20 mut:assign-decrements-first: 1 of 15 failed  caught
[P-shared-ptr] c++20 mut:assign-keeps-old: 1 of 15 failed  caught
[P-shared-ptr] c++20 mut:move-copies-count: 1 of 15 failed  caught
[P-shared-ptr] c++20 mut:move-not-noexcept: 1 of 15 failed  caught
```

### P-scope-guard

Where: `homework-5`, item 1, a `code` item, difficulty 4. Widget `code`, `language: "cpp"`, 12 hidden tests (function mode, `compare: "equal"` for integers, booleans and strings, `isclose` for doubles). Flags: leakCheck: true. `examples` are the first two tests.

`how`: "Submit runs 12 hidden tests. The callbacks write to a hidden counter and a hidden string; two compile checks fail if copying or assignment is allowed."

Hidden `prelude`:

```cpp
#include <functional>
#include <string>
#include <utility>
#include <vector>
#include <type_traits>

// Hidden: the callbacks the tests hand to a guard write here.
int ran = 0;
std::string trace;
```

Hidden `postlude`:

```cpp

// Hidden: a factory that returns a guard by value.
ScopeGuard make_guard() { return ScopeGuard([] { ++ran; }); }
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <functional>
#include <utility>

// A scope guard runs a callback once, when it goes out of scope, unless it was dismissed.
// Write: the destructor, dismiss(), copying deleted, a noexcept move constructor that
// hands the duty to the new guard (the old one must do nothing), and assignment deleted.
class ScopeGuard {
public:
    explicit ScopeGuard(std::function<void()> f) : f_(std::move(f)), active_(true) {}
    // TODO: destructor
    void dismiss() {}                    // TODO: the callback will not run
    // TODO: copying deleted; move constructor; assignment deleted

private:
    std::function<void()> f_;
    bool active_;
};
```

Reference solution:

```cpp
#include <functional>
#include <utility>

// A scope guard runs a callback once, when it goes out of scope, unless it was dismissed.
// Write: the destructor, dismiss(), copying deleted, a noexcept move constructor that
// hands the duty to the new guard (the old one must do nothing), and assignment deleted.
class ScopeGuard {
public:
    explicit ScopeGuard(std::function<void()> f) : f_(std::move(f)), active_(true) {}
    ~ScopeGuard() {
        if (active_) f_();
    }
    void dismiss() { active_ = false; }

    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
    ScopeGuard(ScopeGuard&& other) noexcept : f_(std::move(other.f_)), active_(other.active_) {
        other.active_ = false;
    }
    ScopeGuard& operator=(ScopeGuard&&) = delete;

private:
    std::function<void()> f_;
    bool active_;
};
```

Hidden tests (`setup` then `call`, with its `expect`):

- `{ ScopeGuard g([] { ++ran; }); } ran` expects `1` (`equal`)
- `{ ScopeGuard g([] { ++ran; }); g.dismiss(); } ran` expects `0` (`equal`)
- `{ ScopeGuard a([] { ++ran; }); ScopeGuard b = std::move(a); } ran` expects `1` (`equal`)
- `{ ScopeGuard a([] { ++ran; }); ScopeGuard b = std::move(a); b.dismiss(); } ran` expects `0` (`equal`)
- `{ ScopeGuard a([] { trace += 'a'; }); ScopeGuard b([] { trace += 'b'; }); } trace` expects `"ba"` (`equal`)
- `{ ScopeGuard g = make_guard(); } ran` expects `1` (`equal`)
- `{ std::vector<ScopeGuard> v; v.push_back(ScopeGuard([] { ++ran; })); v.push_back(ScopeGuard([] { ++ran; })); v.push_back(ScopeGuard([] { ++ran; })); } ran` expects `3` (`equal`)
- `int inside = -1; { ScopeGuard g([] { ++ran; }); inside = ran; } inside * 10 + ran` expects `1` (`equal`)
- compiles: `ScopeGuard b = a;` (with `ScopeGuard a([] {});`) expects `false` (it must not compile)
- compiles: `ScopeGuard b([] {}); b = std::move(a);` (with `ScopeGuard a([] {});`) expects `false` (it must not compile)
- `std::is_nothrow_move_constructible_v<ScopeGuard>` expects `true` (`equal`)
- `{ ScopeGuard a([] { ++ran; }); a.dismiss(); ScopeGuard b = std::move(a); } ran` expects `0` (`equal`)

Note: `postlude` holds `make_guard()`, which returns a guard by value. Two of the 12 are `compiles` cases. This is interview recall of the l11 `Connection` (destructor, copying deleted, an inert moved-from object) with a `std::function` callback; the prompt says so, and the new part is the `std::vector<ScopeGuard>` growth test.

Checked by `docs/briefs/cpp-scripts/run_all.py` (each test as its own process, as the app runs them; `-O1 -fno-exceptions`):

```text
[P-scope-guard] solution g++ c++17: 0 of 12 failed OK
[P-scope-guard] solution clang++ c++17: 0 of 12 failed OK
[P-scope-guard] solution g++ c++20: 0 of 12 failed OK
[P-scope-guard] solution clang++ c++20: 0 of 12 failed OK
[P-scope-guard] starter g++ c++17: 8 of 12 failed OK
[P-scope-guard] starter clang++ c++17: 8 of 12 failed OK
[P-scope-guard] starter g++ c++20: 8 of 12 failed OK
[P-scope-guard] starter clang++ c++20: 8 of 12 failed OK
[P-scope-guard] solution under -fsanitize=undefined g++ c++17: 0 of 12 failed OK
[P-scope-guard] solution under -fsanitize=undefined g++ c++20: 0 of 12 failed OK
```

Plausible learner slips (mutants of the solution), each failing at least one test in every native compiler and standard (caught 20 of 20 runs): `always-runs`, `assignment-allowed`, `copy-allowed`, `dismiss-does-nothing`, `move-leaves-source-active`.

Checked in the app's own toolchain (`cpp-scripts/app_toolchain/`: YoWASP clang 21, libc++ in debug hardening, the app's own `unit()` from `cpp-grade.js`, its `leakCheck` and `allocCheck` wrappers, one process per test, `-std=c++17` and `-std=c++20` at `-O1`), `results_app.txt`:

```text
[P-scope-guard] c++17 solution: 0 of 12 failed  OK
[P-scope-guard] c++17 starter: 8 of 12 failed  OK
[P-scope-guard] c++17 mut:move-leaves-source-active: 3 of 12 failed  caught
[P-scope-guard] c++17 mut:dismiss-does-nothing: 3 of 12 failed  caught
[P-scope-guard] c++17 mut:always-runs: 5 of 12 failed  caught
[P-scope-guard] c++17 mut:assignment-allowed: 1 of 12 failed  caught
[P-scope-guard] c++17 mut:copy-allowed: 1 of 12 failed  caught
[P-scope-guard] c++20 solution: 0 of 12 failed  OK
[P-scope-guard] c++20 starter: 8 of 12 failed  OK
[P-scope-guard] c++20 mut:move-leaves-source-active: 3 of 12 failed  caught
[P-scope-guard] c++20 mut:dismiss-does-nothing: 3 of 12 failed  caught
[P-scope-guard] c++20 mut:always-runs: 5 of 12 failed  caught
[P-scope-guard] c++20 mut:assignment-allowed: 1 of 12 failed  caught
[P-scope-guard] c++20 mut:copy-allowed: 1 of 12 failed  caught
```

### P-vec

Where: `homework-5`, item 2, a `code` item, difficulty 5. Widget `code`, `language: "cpp"`, 15 hidden tests (function mode, `compare: "equal"` for integers, booleans and strings, `isclose` for doubles). Flags: allocCheck: true, leakCheck: true. `examples` are the first two tests.

`how`: "Submit runs 15 hidden tests. `alloc_count()` counts calls to `operator new` and `new[]`: 1,000 pushes must allocate 11 times. A hidden `Counted` type counts copies, moves and live objects, and counts any copy or move made from a destroyed object (`Counted::bad`)."

Hidden `prelude`:

```cpp
#include <cstdint>
#include <utility>
#include <type_traits>

// Hidden: counts copies, moves and live objects. It has no assignment operators and no default constructor.
// It also keeps a table of the addresses of its live objects (no heap use). A copy or move whose source
// is not in the table was made from a destroyed object: it is counted in `bad` and never reads the source.
struct Counted {
    static inline int copies = 0, moves = 0, live = 0, bad = 0;
    static inline std::uintptr_t table[64] = {};
    static bool is_live(const Counted* p) {
        for (std::uintptr_t a : table) if (a == reinterpret_cast<std::uintptr_t>(p)) return true;
        return false;
    }
    static void add(const Counted* p) {
        for (std::uintptr_t& a : table) if (a == 0) { a = reinterpret_cast<std::uintptr_t>(p); return; }
    }
    static void drop(const Counted* p) {
        for (std::uintptr_t& a : table) if (a == reinterpret_cast<std::uintptr_t>(p)) { a = 0; return; }
    }
    int v;
    Counted(int x) : v(x) { ++live; add(this); }
    Counted(const Counted& o) : v(-2) { ++copies; ++live; add(this); if (is_live(&o)) v = o.v; else ++bad; }
    Counted(Counted&& o) noexcept : v(-2) { ++moves; ++live; add(this); if (is_live(&o)) { v = o.v; o.v = -1; } else ++bad; }
    Counted& operator=(const Counted&) = delete;
    Counted& operator=(Counted&&) = delete;
    ~Counted() { --live; drop(this); }
};
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <cstddef>
#include <new>
#include <utility>

// A growing array of T. T need not be default constructible or assignable, so keep raw
// storage from ::operator new and build elements in it with placement new.
// Growth: capacity 0 to start (no allocation), 1 on the first push, then doubling.
// push_back must work when its argument lives inside the vector (v.push_back(v[0])).
// Copy assignment must be safe for `a = a`.
// Write both push_back overloads, or share a helper: a template parameter `U&&` accepts both,
// and std::forward<U>(x) passes it on as a copy or a move.
// Growth moves elements if T's move constructor is noexcept (std::move_if_noexcept).
template <typename T>
class Vec {
public:
    Vec() = default;
    // TODO: destructor (destroy every element, then free the block)
    // TODO: copy constructor and copy assignment
    // TODO: move constructor and move assignment (noexcept)
    void push_back(const T& x) { (void)x; }       // TODO
    void push_back(T&& x) { (void)x; }            // TODO

    std::size_t size() const { return size_; }
    std::size_t capacity() const { return cap_; }
    T& operator[](std::size_t i) { return data_[i]; }
    const T& operator[](std::size_t i) const { return data_[i]; }

private:
    std::size_t size_ = 0;
    std::size_t cap_ = 0;
    T* data_ = nullptr;
};
```

Reference solution:

```cpp
#include <cstddef>
#include <new>
#include <utility>

// A growing array of T. T need not be default constructible or assignable, so keep raw
// storage from ::operator new and build elements in it with placement new.
// Growth: capacity 0 to start (no allocation), 1 on the first push, then doubling.
// push_back must work when its argument lives inside the vector (v.push_back(v[0])).
// Copy assignment must be safe for `a = a`.
// Write both push_back overloads, or share a helper: a template parameter `U&&` accepts both,
// and std::forward<U>(x) passes it on as a copy or a move.
// Growth moves elements if T's move constructor is noexcept (std::move_if_noexcept).
template <typename T>
class Vec {
public:
    Vec() = default;
    ~Vec() { destroy(); }

    Vec(const Vec& other) : size_(other.size_), cap_(other.size_), data_(allocate(other.size_)) {
        for (std::size_t i = 0; i < size_; ++i) new (data_ + i) T(other.data_[i]);
    }
    Vec& operator=(const Vec& other) {
        if (this != &other) {
            Vec copy(other);
            swap(copy);
        }
        return *this;
    }
    Vec(Vec&& other) noexcept : size_(other.size_), cap_(other.cap_), data_(other.data_) {
        other.size_ = 0;
        other.cap_ = 0;
        other.data_ = nullptr;
    }
    Vec& operator=(Vec&& other) noexcept {
        if (this != &other) {
            destroy();
            size_ = other.size_;
            cap_ = other.cap_;
            data_ = other.data_;
            other.size_ = 0;
            other.cap_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

    void push_back(const T& x) { emplace(x); }
    void push_back(T&& x) { emplace(std::move(x)); }

    std::size_t size() const { return size_; }
    std::size_t capacity() const { return cap_; }
    T& operator[](std::size_t i) { return data_[i]; }
    const T& operator[](std::size_t i) const { return data_[i]; }

private:
    static T* allocate(std::size_t n) {
        return n ? static_cast<T*>(::operator new(n * sizeof(T))) : nullptr;
    }
    void destroy() {
        for (std::size_t i = 0; i < size_; ++i) data_[i].~T();
        ::operator delete(data_);
        size_ = 0;
        cap_ = 0;
        data_ = nullptr;
    }
    void swap(Vec& o) {
        std::swap(size_, o.size_);
        std::swap(cap_, o.cap_);
        std::swap(data_, o.data_);
    }
    template <typename U>
    void emplace(U&& x) {
        if (size_ == cap_) {
            std::size_t new_cap = cap_ ? cap_ * 2 : 1;
            T* fresh = allocate(new_cap);
            new (fresh + size_) T(std::forward<U>(x));      // x may live in the old block, so build it first
            for (std::size_t i = 0; i < size_; ++i) {
                new (fresh + i) T(std::move_if_noexcept(data_[i]));
                data_[i].~T();
            }
            ::operator delete(data_);
            data_ = fresh;
            cap_ = new_cap;
        } else {
            new (data_ + size_) T(std::forward<U>(x));
        }
        ++size_;
    }

    std::size_t size_ = 0;
    std::size_t cap_ = 0;
    T* data_ = nullptr;
};
```

Hidden tests (`setup` then `call`, with its `expect`):

- `Vec<int> v; for (int i = 0; i < 1000; ++i) v.push_back(i); v.size() * 10000 + v.capacity()` expects `10001024` (`equal`)
- `Vec<int> v; for (int i = 0; i < 1000; ++i) v.push_back(i); v[0] + v[500] + v[999]` expects `1499` (`equal`)
- `Vec<int> v; reset_alloc_count(); for (int i = 0; i < 1000; ++i) v.push_back(i); alloc_count()` expects `11` (`equal`)
- `reset_alloc_count(); Vec<int> v; alloc_count() * 10 + v.capacity()` expects `0` (`equal`)
- `{ Vec<Counted> v; for (int i = 0; i < 8; ++i) v.push_back(Counted(i)); } Counted::copies * 100 + Counted::moves` expects `15` (`equal`)
- `{ Vec<Counted> v; for (int i = 0; i < 5; ++i) v.push_back(Counted(i)); } Counted::live` expects `0` (`equal`)
- `Vec<int> a; a.push_back(1); a.push_back(2); Vec<int> b = a; b[0] = 9; a[0] * 10 + b[0]` expects `19` (`equal`)
- `Vec<Counted> a; for (int i = 0; i < 4; ++i) a.push_back(Counted(i)); int before = Counted::copies; Vec<Counted> b = a; Counted::copies - before` expects `4` (`equal`)
- `Vec<int> a; for (int i = 0; i < 100; ++i) a.push_back(i); reset_alloc_count(); Vec<int> b = std::move(a); alloc_count()` expects `0` (`equal`)
- `Vec<int> a; for (int i = 0; i < 100; ++i) a.push_back(i); Vec<int> b = std::move(a); a.size() * 1000 + b.size()` expects `100` (`equal`)
- `Vec<int> a; a.push_back(5); Vec<int> b; b.push_back(1); b.push_back(2); b = a; b.size() * 10 + b[0]` expects `15` (`equal`)
- `Vec<int> a; a.push_back(5); Vec<int> b; b.push_back(1); b = std::move(a); b.size() * 10 + b[0] + a.size() * 100` expects `15` (`equal`)
- `Vec<int> a; a.push_back(5); a.push_back(6); Vec<int>& r = a; a = r; a.size() * 10 + a[1]` expects `26` (`equal`)
- `Vec<Counted> v; v.push_back(Counted(7)); v.push_back(v[0]); Counted::bad * 100 + v[1].v` expects `7` (`equal`)
- `std::is_nothrow_move_constructible_v<Vec<int>>` expects `true` (`equal`)

Note: `Counted` has no default constructor and no assignment, which forces raw storage and placement new. It keeps a table of the addresses of its live objects (no heap use) and never reads a source that is not in the table, so `v.push_back(v[0])` is tested by `Counted::bad` and the copied value, with no read of freed memory: a growth that destroys the old elements before copying the argument gives `bad` 1 and fails. The starter comment tells the learner that copy assignment must be safe for `a = a` and that a template `U&&` helper can serve both `push_back` overloads.

Checked by `docs/briefs/cpp-scripts/run_all.py` (each test as its own process, as the app runs them; `-O1 -fno-exceptions`):

```text
[P-vec] solution g++ c++17: 0 of 15 failed OK
[P-vec] solution clang++ c++17: 0 of 15 failed OK
[P-vec] solution g++ c++20: 0 of 15 failed OK
[P-vec] solution clang++ c++20: 0 of 15 failed OK
[P-vec] starter g++ c++17: 11 of 15 failed OK
[P-vec] starter clang++ c++17: 11 of 15 failed OK
[P-vec] starter g++ c++20: 11 of 15 failed OK
[P-vec] starter clang++ c++20: 11 of 15 failed OK
[P-vec] solution under -fsanitize=undefined g++ c++17: 0 of 15 failed OK
[P-vec] solution under -fsanitize=undefined g++ c++20: 0 of 15 failed OK
```

Plausible learner slips (mutants of the solution), each failing at least one test in every native compiler and standard (caught 28 of 28 runs): `copies-on-growth`, `copy-assign-leaks`, `forgets-to-destroy`, `frees-before-building-new`, `grows-by-one`, `move-leaves-source-owning`, `move-not-noexcept`.

Checked in the app's own toolchain (`cpp-scripts/app_toolchain/`: YoWASP clang 21, libc++ in debug hardening, the app's own `unit()` from `cpp-grade.js`, its `leakCheck` and `allocCheck` wrappers, one process per test, `-std=c++17` and `-std=c++20` at `-O1`), `results_app.txt`:

```text
[P-vec] c++17 solution: 0 of 15 failed  OK
[P-vec] c++17 starter: 11 of 15 failed  OK
[P-vec] c++17 mut:grows-by-one: 3 of 15 failed  caught
[P-vec] c++17 mut:copies-on-growth: 1 of 15 failed  caught
[P-vec] c++17 mut:forgets-to-destroy: 1 of 15 failed  caught
[P-vec] c++17 mut:frees-before-building-new: 1 of 15 failed  caught
[P-vec] c++17 mut:move-leaves-source-owning: 2 of 15 failed  caught
[P-vec] c++17 mut:move-not-noexcept: 1 of 15 failed  caught
[P-vec] c++17 mut:copy-assign-leaks: 1 of 15 failed  caught
[P-vec] c++20 solution: 0 of 15 failed  OK
[P-vec] c++20 starter: 11 of 15 failed  OK
[P-vec] c++20 mut:grows-by-one: 3 of 15 failed  caught
[P-vec] c++20 mut:copies-on-growth: 1 of 15 failed  caught
[P-vec] c++20 mut:forgets-to-destroy: 1 of 15 failed  caught
[P-vec] c++20 mut:frees-before-building-new: 1 of 15 failed  caught
[P-vec] c++20 mut:move-leaves-source-owning: 2 of 15 failed  caught
[P-vec] c++20 mut:move-not-noexcept: 1 of 15 failed  caught
[P-vec] c++20 mut:copy-assign-leaks: 1 of 15 failed  caught
```

### P-clone-basket

Where: exam item `e-code-clone-basket` (see the exam section), a `code` item, difficulty 4. Widget `code`, `language: "cpp"`, 11 hidden tests (function mode, `compare: "equal"` for integers, booleans and strings, `isclose` for doubles). Flags: leakCheck: true. `examples` are the first two tests.

`how`: "Submit runs 11 hidden tests. Costs are compared with `isclose`."

Hidden `prelude`:

```cpp
#include <type_traits>
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <memory>
#include <vector>

// Order is an interface. clone() returns a copy of the same dynamic type, so an
// Order can be copied through a base pointer without slicing. Market is written for you.
struct Order {
    virtual ~Order() = default;
    virtual double cost(double market) const = 0;      // pounds to buy at this market price
    virtual std::unique_ptr<Order> clone() const = 0;
};

struct Market : Order {
    explicit Market(int q) : qty(q) {}
    double cost(double market) const override { return qty * market; }
    std::unique_ptr<Order> clone() const override { return std::make_unique<Market>(*this); }
    int qty;
};

// TODO: Limit(q, px): buys q shares only if the market price is at most px,
// so cost is q * market then, and 0 when the market is above px. clone() returns a Limit.
struct Limit : Order {
    Limit(int q, double px) : qty(q), limit(px) {}
    double cost(double) const override { return 0.0; }
    std::unique_ptr<Order> clone() const override { return nullptr; }
    int qty;
    double limit;
};

// TODO: Basket: holds orders of any kind. cost() is the sum of their costs.
// clone() returns a Basket holding a clone of each child (a deep copy).
struct Basket : Order {
    void add(std::unique_ptr<Order> o) { (void)o; }
    double cost(double) const override { return 0.0; }
    std::unique_ptr<Order> clone() const override { return nullptr; }
    std::vector<std::unique_ptr<Order>> kids;
};
```

Reference solution:

```cpp
#include <memory>
#include <vector>

// Order is an interface. clone() returns a copy of the same dynamic type, so an
// Order can be copied through a base pointer without slicing. Market is written for you.
struct Order {
    virtual ~Order() = default;
    virtual double cost(double market) const = 0;      // pounds to buy at this market price
    virtual std::unique_ptr<Order> clone() const = 0;
};

struct Market : Order {
    explicit Market(int q) : qty(q) {}
    double cost(double market) const override { return qty * market; }
    std::unique_ptr<Order> clone() const override { return std::make_unique<Market>(*this); }
    int qty;
};

struct Limit : Order {
    Limit(int q, double px) : qty(q), limit(px) {}
    double cost(double market) const override { return market <= limit ? qty * market : 0.0; }
    std::unique_ptr<Order> clone() const override { return std::make_unique<Limit>(*this); }
    int qty;
    double limit;
};

struct Basket : Order {
    void add(std::unique_ptr<Order> o) { kids.push_back(std::move(o)); }
    double cost(double market) const override {
        double total = 0.0;
        for (const auto& k : kids) total += k->cost(market);
        return total;
    }
    std::unique_ptr<Order> clone() const override {
        auto copy = std::make_unique<Basket>();
        for (const auto& k : kids) copy->add(k->clone());
        return copy;
    }
    std::vector<std::unique_ptr<Order>> kids;
};
```

Hidden tests (`setup` then `call`, with its `expect`):

- `Limit l(100, 2.5); l.cost(2.0)` expects `200.0` (`isclose`)
- `Limit l(100, 2.5); l.cost(3.0)` expects `0.0` (`isclose`)
- `Limit l(100, 2.5); l.cost(2.5)` expects `250.0` (`isclose`)
- `Limit l(100, 2.5); std::unique_ptr<Order> q = l.clone(); q->cost(2.0)` expects `200.0` (`isclose`)
- `Limit l(100, 2.5); std::unique_ptr<Order> q = l.clone(); q->cost(3.0)` expects `0.0` (`isclose`)
- `Basket b; b.add(std::make_unique<Market>(100)); b.add(std::make_unique<Limit>(150, 2.5)); b.cost(2.0)` expects `500.0` (`isclose`)
- `Basket b; b.add(std::make_unique<Market>(100)); b.add(std::make_unique<Limit>(150, 2.5)); b.cost(3.0)` expects `300.0` (`isclose`)
- `Basket b; b.add(std::make_unique<Market>(100)); b.add(std::make_unique<Limit>(150, 2.5)); std::unique_ptr<Order> c = b.clone(); c->cost(2.0)` expects `500.0` (`isclose`)
- `Basket b; b.add(std::make_unique<Market>(100)); b.add(std::make_unique<Limit>(150, 2.5)); std::unique_ptr<Order> c = b.clone(); b.add(std::make_unique<Market>(1000)); c->cost(2.0)` expects `500.0` (`isclose`)
- `Basket inner; inner.add(std::make_unique<Limit>(10, 2.5)); inner.add(std::make_unique<Market>(100)); Basket outer; outer.add(inner.clone()); outer.add(std::make_unique<Market>(0)); std::unique_ptr<Order> c = outer.clone(); inner.add(std::make_unique<Market>(5)); c->cost(3.0)` expects `300.0` (`isclose`)
- `std::is_abstract_v<Basket>` expects `false` (`equal`)

Note: Function mode. `leakCheck` is on so that a raw `new` that is never deleted is caught (every owner in a normal solution is a `unique_ptr`). Tests that clone and then change the original check that the copy is deep.

Checked by `docs/briefs/cpp-scripts/run_all.py` (each test as its own process, as the app runs them; `-O1 -fno-exceptions`):

```text
[P-clone-basket] solution g++ c++17: 0 of 11 failed OK
[P-clone-basket] solution clang++ c++17: 0 of 11 failed OK
[P-clone-basket] solution g++ c++20: 0 of 11 failed OK
[P-clone-basket] solution clang++ c++20: 0 of 11 failed OK
[P-clone-basket] starter g++ c++17: 9 of 11 failed OK
[P-clone-basket] starter clang++ c++17: 9 of 11 failed OK
[P-clone-basket] starter g++ c++20: 9 of 11 failed OK
[P-clone-basket] starter clang++ c++20: 9 of 11 failed OK
[P-clone-basket] solution under -fsanitize=undefined g++ c++17: 0 of 11 failed OK
[P-clone-basket] solution under -fsanitize=undefined g++ c++20: 0 of 11 failed OK
```

Plausible learner slips (mutants of the solution), each failing at least one test in every native compiler and standard (caught 20 of 20 runs): `basket-clone-is-shallow-sliced`, `basket-clone-shares-nothing-but-is-empty`, `basket-cost-forgets-children`, `limit-clone-forgets-limit`, `limit-fills-above-its-limit`.

Checked in the app's own toolchain (`cpp-scripts/app_toolchain/`: YoWASP clang 21, libc++ in debug hardening, the app's own `unit()` from `cpp-grade.js`, its `leakCheck` and `allocCheck` wrappers, one process per test, `-std=c++17` and `-std=c++20` at `-O1`), `results_app.txt`:

```text
[P-clone-basket] c++17 solution: 0 of 11 failed  OK
[P-clone-basket] c++17 starter: 9 of 11 failed  OK
[P-clone-basket] c++17 mut:limit-clone-forgets-limit: 2 of 11 failed  caught
[P-clone-basket] c++17 mut:limit-fills-above-its-limit: 4 of 11 failed  caught
[P-clone-basket] c++17 mut:basket-clone-is-shallow-sliced: 3 of 11 failed  caught
[P-clone-basket] c++17 mut:basket-clone-shares-nothing-but-is-empty: 3 of 11 failed  caught
[P-clone-basket] c++17 mut:basket-cost-forgets-children: 5 of 11 failed  caught
[P-clone-basket] c++20 solution: 0 of 11 failed  OK
[P-clone-basket] c++20 starter: 9 of 11 failed  OK
[P-clone-basket] c++20 mut:limit-clone-forgets-limit: 2 of 11 failed  caught
[P-clone-basket] c++20 mut:limit-fills-above-its-limit: 4 of 11 failed  caught
[P-clone-basket] c++20 mut:basket-clone-is-shallow-sliced: 3 of 11 failed  caught
[P-clone-basket] c++20 mut:basket-clone-shares-nothing-but-is-empty: 3 of 11 failed  caught
[P-clone-basket] c++20 mut:basket-cost-forgets-children: 5 of 11 failed  caught
```

## Number checks

Every figure in the lessons, review, homework and exam is computed twice. Source 1 is `cpp-scripts/number_checks.py`, a Python model that shares no code with the C++ (output below); source 2 is the native run or the hidden test named beside it.

```text
ok  1,000,000 doubles in bytes: 8000000
ok  copy time at 10 GB/s, ms: 4/5
ok  1,000 Buffers of 1,000 doubles, bytes copied per growth (homework 8): 8000000
ok  a vector move writes three pointers, bytes here (wasm32): 12
ok  a vector move writes three pointers, bytes on a desktop: 24
ok  pointer and size moved, bytes here (wasm32): 8
ok  pointer and size moved, bytes on a desktop: 16
ok  4 pushes, noexcept move: (copies, moves): (0, 7)
ok  2 pushes, move not noexcept: (copies, moves): (1, 2)
ok  3 pushes, move not noexcept: (copies, moves): (3, 3)
ok  4 pushes, move not noexcept: (copies, moves): (3, 4)
ok  8 pushes, noexcept move: moves (P-vec, Counted): (0, 15)
ok  1000 pushes: (allocations, capacity) (P-vec): (11, 1024)
ok  size * 10000 + capacity after 1000 pushes: 10001024
ok  set_prices(lvalue): doubles copied: 1000000
ok  set_prices(lvalue) counted wrongly as copy plus assign: 2000000
ok  D {vptr, int, int} on wasm32: 12
ok  Quote {vptr, double, double} on wasm32: 24
ok  OneVirtual {vptr, int} on wasm32: 8
ok  D {vptr, int, int} on desktop: 16
ok  Quote {vptr, double, double} on desktop: 24
ok  OneVirtual {vptr, int} on desktop: 16
ok  PlainQuote {double, double}: 16
ok  B {vptr, double} on wasm32 (homework 7a): 16
ok  Tick {int} (l21 hook): 4
ok  INT_MAX in pence as pounds: 2147483647/100
   as text: 21,474,836.47
ok  INT_MAX pence, pounds text: £21,474,836.47
ok  £25,000,000 in pence: 2500000000
ok  £25,000,000 exceeds INT_MAX: True
ok  5,000 fills of £5,000, pounds: 25000000
ok  UINT_MAX pence, pounds text: £42,949,672.95
ok  int64 max pence, pounds text: £92,233,720,368,547,758.07
ok  0 - 1 as unsigned 32-bit (v.size() - 1, empty, wasm32): 4294967295
ok  0 - 1 as unsigned 64-bit (desktop): 18446744073709551615
ok  2^30 + 2^30 overflows int: True
ok  2^30 - 1 + 2^30 equals INT_MAX exactly: 2147483647
ok  shared_ptr<T>(new T): allocations a second: 400000
ok  make_shared: allocations a second: 200000
ok  saved allocations a second at 50 ns, ms: 10
ok  that is a share of one core, per cent: 1
ALL NUMBERS OK
```

Second sources, run natively with g++ 13.3 and clang++ 18.1 (libstdc++; see the runtime-facts note about libc++):

- Copy and move counts in l19 and the exam: `cpp-scripts/facts_l19.cpp` prints copies and moves for sixteen snippets (identical under both compilers: `Tracked b = a;` 1 copy; `Tracked b = std::move(a);` 1 move; `std::move(a);` alone 0 and 0; `make()` 0 and 0; `return std::move(t)` 1 move; a `const` source 1 copy; `take(a)` 1 copy; `take(std::move(a))` 1 move; `take(Tracked(1))` 0 and 0; four pushes with a `noexcept` move 0 copies and 7 moves; two pushes with a throwing move 1 copy and 2 moves). `facts_misc.cpp` checks 3 copies and 4 moves for four pushes with a throwing move.
- The special-members table in l20: `cpp-scripts/special_members.cpp` prints it (same under both compilers); the l20 and homework keys are read from it.
- Layout facts in l21: `cpp-scripts/wasm_sizes.cpp` compiles with `clang++ --target=wasm32-unknown-wasi -fsyntax-only` (pointer 4; one virtual and an `int` 8; two virtuals still 8; derived with two `int`s 12; `Quote` 24); the same file fails five static assertions on a 64-bit target, as the lesson says (16, 16 and so on).
- Undefined-behaviour facts in l22: `ub_asm.cpp` (wasm32 `-O1` output, and x86-64) and `ub_facts.cpp` (the sanitiser lines; the unsigned wrap prints 0).
- Smart-pointer facts in l23: `facts_misc.cpp` counts allocations (`shared_ptr<int>(new int)` 2, `make_shared<int>` 1) and sizes (`unique_ptr` one pointer, `shared_ptr` two); the `Vec` counts (11 allocations, capacity 1,024, 15 moves) are tested by P-vec and modelled in `number_checks.py`.
- Fix-pass facts: `cpp-scripts/facts_fixpass.cpp` prints `1 0` (a defaulted move is `noexcept`, a hand-written one without the keyword is not: l20 S4 and review 4), `order move 0 copy 0` (l20 S8: `is_move_constructible` is false because the deleted copy constructor is chosen), `gone 1` (`e-virtual-dtor`: `shared_ptr<Base>` from `make_shared<Derived>` runs `~Derived`), `c=0` and `b=0` (the two defined lines of `e-ub-which`). The homework 8 growth copy, 1,000 x 1,000 x 8 = 8,000,000 bytes, is in `number_checks.py`.
- Exam: 3 copies for four pushes with a throwing move (model and native); the three `e-ub-which` keys by rule.
