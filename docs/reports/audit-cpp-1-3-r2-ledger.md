# Claim ledger: cpp L1 to L3, round 2 blind audit

Audit: `docs/reviews/audit-cpp-1-3-r2.md`. Script: `docs/reports/cpp-L1-3-r2-concepts.py` (driver `cpp-L1-3-r2-zq.mjs`).
Scope: l1 to l13, review-1 to review-3, homework-1 to homework-3 (19 files). Stage 1, so full depth.

2145 rows: 2121 correct, 19 imprecise, 3 wrong, 2 unverified.

## How the rows were made, stated plainly

- I read every string of the 19 files once, in full, and judged each line as I read it. Every claim about what code prints, what compiles, what a compiler says or what a test catches was then compiled and run: 366 checks, of which 320 use the app's own compiler, harness, exception runtime and WASI shim, 23 use local g++ 13.3 and clang 18.1 on x86-64 Linux, and 23 are arithmetic in CPython 3.
- The table below is written out by a small script from the content, one row per claim-bearing string: prose, canvas transcript, graded key, each wrong option with its `why`, each slip value with its feedback line, each hint, each feedback line, each explanation, each summary line, each paragraph of a longform model answer and each rubric line.
- The basis column is recorded per screen or item: the named checks that cover that screen, and the standard section, source or derivation for what a run cannot show. A row whose verdict is not `correct` has its own basis, written by hand.
- A hint or feedback line that only restates its screen's result carries the screen's basis. That is the one place where a verdict was not given a line of its own, and it is why the count of `correct` rows is large.
- Section numbers of the standard are those of C++17 (N4659). Wasm32 differences are noted where they matter: `sizeof(long)` and `sizeof(std::size_t)` are 4, a `std::vector` object is 12 bytes.
- The `how` line of the code widgets (compiler download size and time) is out of scope, as the brief says.

Verdicts: `correct`, `wrong` (false as stated), `imprecise` (true only under an unstated hypothesis), `misleading`, `unverified`.

## l1-source-to-program.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | In Python you run the source file itself: `python3 main.py`. Here is a C++ session in a terminal. The folder … | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].canvas` | canvas (console): {"lines": ["$ ls", "main.cpp", "$ g++ -std=c++17 main.cpp -o main", "$ ls", "main main.cpp"… | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].widget.answer` | KEY: Tap the command that turns `main.cpp` into a program the machine can run. -> ["l3"] | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].hints[0]` | Which command makes a new file appear in the folder? | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].hints[1]` | Compare the two `ls` listings, before and after. | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].hints[2]` | The file `main` appears after line 3, so line 3 made it. | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].feedback.correct` | `g++` read the text and wrote a new file, `main`. | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].feedback.byKey.l6` | You tapped the command that runs the program. By then `main` already existed: the `ls` on line 4 shows it. | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].feedback.byKey.l7` | That is the program's output. Something had to build the program before it could print. | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].feedback.byKey.l1` | `ls` only lists the folder. Compare its two listings to see what changed between them. | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].feedback.byKey.l4` | `ls` only lists the folder. The command before it is the one that made `main`. | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[0].explain.text` | `g++` is a **compiler**. It read `main.cpp` and wrote `main`, a file of machine instructions. `./main` runs t… | correct | read off the console: `main` appears after line 3; g++ is a compiler (GCC manual, ch. 3 Invoking GCC) |
| `screens[1].prose` | Inside that one `g++` command are two steps, drawn here. The program uses `std::cout` to print, yet you never… | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[1].canvas` | canvas (graph): {"nodes": [{"id": "src", "label": "main.cpp", "x": 0.08, "y": 0.25, "shape": "rect"}, {"id": … | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[1].widget.answer` | KEY: Tap the step where the library's printing code joins your code. -> ["ld"] | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[1].hints[0]` | Follow the arrow that leaves the library box. | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[1].hints[1]` | The library's arrow ends at one step. | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[1].feedback.correct` | The linker joins `main.o` and the library into one file. | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[1].feedback.byKey.cc` | The compiler sees only your file. `#include <iostream>` tells it `std::cout` exists, but the printing code it… | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[1].feedback.byKey.lib` | That box holds the printing code, but it does nothing by itself. Find the step its arrow points to. | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[1].feedback.byKey.exe` | That is the finished program, after the join. | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[1].feedback.byKey.obj` | `main.o` is your code alone, with a gap where `std::cout` goes. | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[1].explain.text` | The **compiler** turns `main.cpp` into an **object file**, `main.o`: machine code with gaps for names defined… | correct | GCC manual 3.2 Overall Options: compile to an object file, then link; the driver keeps the object as a temporary |
| `screens[2].prose` | So the **compiler** makes an **object file** and the **linker** makes the **executable**. Python reads `main.… | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].canvas` | canvas (graph): {"nodes": [{"id": "src", "label": "main.cpp", "x": 0.08, "y": 0.25, "shape": "rect"}, {"id": … | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].widget.options[0]` | KEY: You type `./main` without running `g++` again. What prints? -> `Hello, market` | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].widget.options[1]` | not: `Hello, desk` / why: You expected `./main` to read `main.cpp`, as `python3` reads `main.py`. The executa… | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].widget.options[2]` | not: An error saying the source has changed / why: Nothing checks the source when `./main` runs. The old exec… | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].widget.options[3]` | not: Nothing, because saving deletes `main` / why: Saving changes only `main.cpp`. The executable stays exact… | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].hints[0]` | Which box does `./main` run? | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].hints[1]` | The edit changed this box only. | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].hints[2]` | `main` was built from the old text. Nothing has rebuilt it. | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].feedback.correct` | The executable still holds the old text. | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].feedback.byKey.new` | You expected `./main` to read `main.cpp`, as `python3` reads `main.py`. It runs the executable, which was bui… | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[2].explain.text` | `./main` runs the executable, which was built from the old text. The edit reaches it only when you compile ag… | correct | derivation: `./main` executes the file built before the edit; nothing reads `main.cpp` at run time |
| `screens[3].prose` | Every C++ program starts in `int main()`. `#include <iostream>` brings in `std::cout`, and `<<` sends text to… | correct | checks l1.s3.fb-test-2, l1.s3.comma, l1.s3.trailing-space |
| `screens[3].canvas` | canvas (console): {"lines": ["$ g++ -std=c++17 main.cpp -o main", "$ ./main", "Hello, market"], "title": "Wha… | correct | checks l1.s3.fb-test-2, l1.s3.comma, l1.s3.trailing-space |
| `screens[3].widget.solution` | code: Write the program that prints `Hello, market` on its own line. (3 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l1.s3.fb-test-2, l1.s3.comma, l1.s3.trailing-space |
| `screens[3].hints[0]` | Start the line with `std::cout <<`. | correct | checks l1.s3.fb-test-2, l1.s3.comma, l1.s3.trailing-space |
| `screens[3].hints[1]` | The text goes in double quotes; the line end is `'\n'`. | correct | checks l1.s3.fb-test-2, l1.s3.comma, l1.s3.trailing-space |
| `screens[3].hints[2]` | `std::cout << "Hello, market" << '\n';` inside `main`, before `return 0;`. | correct | checks l1.s3.fb-test-2, l1.s3.comma, l1.s3.trailing-space |
| `screens[3].feedback.correct` | That is a complete C++ program. | correct | checks l1.s3.fb-test-2, l1.s3.comma, l1.s3.trailing-space |
| `screens[3].feedback.byKey.compile` | The compiler stopped. Read the first `error:` line under the editor: it names the line and the column. | correct | checks l1.s3.fb-test-2, l1.s3.comma, l1.s3.trailing-space |
| `screens[3].feedback.byKey.test-2` | The words match but not every character. Check the comma, the capital H and the `'\n'` at the end. | imprecise | check l1.s3.comma: a wrong comma or capital fails test 1 (key test-1); only the line end reaches test 2 (checks l1.s3.fb-test-2, l1.s3.trailing-space); finding 9 |
| `screens[3].explain.text` | `std::cout` is the screen, and `<<` pushes each piece onto it in order. `return 0;` tells the shell the progr… | correct | checks l1.s3.fb-test-2, l1.s3.comma, l1.s3.trailing-space |
| `screens[4].prose` | `std::cin >> x` reads the next word typed into `x`, skipping spaces and line breaks. Unlike Python's `input()… | correct | checks l1.s4.fb-test-2, l1.s4.fb-test-3 |
| `screens[4].canvas` | canvas (console): {"lines": ["$ ./main", "VOD", "72.5", "Ticker: VOD", "Price: 72.5"], "title": "What it shou… | correct | checks l1.s4.fb-test-2, l1.s4.fb-test-3 |
| `screens[4].widget.solution` | code: Read a ticker and a price with `std::cin`, then print them on two lines as shown. (4 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l1.s4.fb-test-2, l1.s4.fb-test-3 |
| `screens[4].hints[0]` | One `std::cin` line can read both: `std::cin >> ticker >> price;`. | correct | checks l1.s4.fb-test-2, l1.s4.fb-test-3 |
| `screens[4].hints[1]` | Test 2 types both on one line. `>>` skips the space for you. | correct | checks l1.s4.fb-test-2, l1.s4.fb-test-3 |
| `screens[4].hints[2]` | Then two `std::cout` lines, each ending with `'\n'`. | correct | checks l1.s4.fb-test-2, l1.s4.fb-test-3 |
| `screens[4].feedback.correct` | `>>` read a word, then a number, and converted it. | correct | checks l1.s4.fb-test-2, l1.s4.fb-test-3 |
| `screens[4].feedback.byKey.test-2` | Test 2 types `BARC 215.35` on one line. `std::cin >>` stops at the space, so read twice with `>>`, not a whol… | correct | checks l1.s4.fb-test-2, l1.s4.fb-test-3 |
| `screens[4].feedback.byKey.test-3` | Test 3 expects `12000`. Leave the number as `std::cout` prints it; do not fix the decimal places. | imprecise | check l1.s4.fb-test-3: fixed decimals print 72.50 and fail test 1; finding 10 |
| `screens[4].explain.text` | `std::cin >> ticker >> price;` reads a word into the `std::string`, then converts the next word into the `dou… | correct | checks l1.s4.fb-test-2, l1.s4.fb-test-3 |
| `screens[5].prose` | You forget a semicolon and build. g++ prints an error in the shape `file:line:column: error: message`. | correct | check l1.s5.gxx-semicolon |
| `screens[5].canvas` | canvas (pair): {"left": {"kind": "console", "params": {"title": "Terminal", "lines": ["$ g++ -std=c++17 main.… | correct | check l1.s5.gxx-semicolon |
| `screens[5].widget.answer` | KEY: Tap the line of `main.cpp` that the error names. -> ["l5"] | correct | check l1.s5.gxx-semicolon |
| `screens[5].hints[0]` | Read the number straight after `main.cpp:` in the error line. | correct | check l1.s5.gxx-semicolon |
| `screens[5].hints[1]` | That error line is marked red. | correct | check l1.s5.gxx-semicolon |
| `screens[5].hints[2]` | `main.cpp:5:5` means line 5, column 5. | correct | check l1.s5.gxx-semicolon |
| `screens[5].feedback.correct` | The error names line 5, column 5. | correct | check l1.s5.gxx-semicolon |
| `screens[5].feedback.byKey.l4` | That is where the slip is, and we come to it next. The error itself names line 5: read the number after `main… | correct | check l1.s5.gxx-semicolon |
| `screens[5].feedback.byKey.l6` | The error names line 5. Read the first number after `main.cpp:`. | correct | check l1.s5.gxx-semicolon |
| `screens[5].explain.text` | `main.cpp:5:5` is the file, then line 5, then column 5. g++ also prints that line with a caret under the colu… | correct | check l1.s5.gxx-semicolon |
| `screens[6].prose` | Same error. Line 5 looks perfectly fine, though: it is the same `std::cout` line that worked before. | correct | check l1.s6.clang-semicolon |
| `screens[6].canvas` | canvas (pair): {"left": {"kind": "console", "params": {"title": "Terminal", "lines": ["$ g++ -std=c++17 main.… | correct | check l1.s6.clang-semicolon |
| `screens[6].widget.answer` | KEY: Tap the line you must change to fix the build. -> ["l4"] | correct | check l1.s6.clang-semicolon |
| `screens[6].hints[0]` | The message says what it expected: `','` or `';'`. | correct | check l1.s6.clang-semicolon |
| `screens[6].hints[1]` | Look at how the line above line 5 ends. | correct | check l1.s6.clang-semicolon |
| `screens[6].hints[2]` | `double price = 101.5` never ends, so the compiler read on into line 5. | correct | check l1.s6.clang-semicolon |
| `screens[6].feedback.correct` | Line 4 is missing its `;`. | correct | check l1.s6.clang-semicolon |
| `screens[6].feedback.byKey.l5` | Line 5 is where g++ noticed, not where the slip is. The declaration on line 4 never ended, so the compiler re… | correct | check l1.s6.clang-semicolon |
| `screens[6].explain.text` | g++ reports where it got confused, often the line after the slip. Clang, the compiler in this app, points at … | correct | check l1.s6.clang-semicolon |
| `screens[7].prose` | This time `main.cpp` has no `return 0;`, and you build with `-Wall`, which asks for extra warnings. ```cpp #i… | correct | check l1.s7.wall-unused |
| `screens[7].canvas` | canvas (console): {"lines": ["$ g++ -std=c++17 -Wall main.cpp -o main", "main.cpp: In function 'int main()':"… | correct | check l1.s7.wall-unused |
| `screens[7].widget.options[0]` | KEY: What happened? -> It built and ran: a warning is advice, and `main` returns 0 by itself | correct | check l1.s7.wall-unused |
| `screens[7].widget.options[1]` | not: It did not build, because of the warning / why: You read `warning` as `error`. Only an error stops the b… | correct | check l1.s7.wall-unused |
| `screens[7].widget.options[2]` | not: It built, but `main` returns a random exit code / why: `main` is the one function where reaching the end… | correct | check l1.s7.wall-unused |
| `screens[7].widget.options[3]` | not: It built only because `-Wall` was given / why: `-Wall` asks for more warnings. It never makes a build su… | correct | check l1.s7.wall-unused |
| `screens[7].hints[0]` | Is there an `error:` anywhere in the output? | correct | check l1.s7.wall-unused |
| `screens[7].hints[1]` | Line 6 tries to run the program. | correct | check l1.s7.wall-unused |
| `screens[7].feedback.correct` | A warning flags something odd; it does not stop the build. | correct | check l1.s7.wall-unused |
| `screens[7].feedback.byKey.nobuild` | You read `warning` as `error`. Only an error stops the build, and line 6 shows `./main` running. | correct | check l1.s7.wall-unused |
| `screens[7].explain.text` | g++ built `main` despite the warning, which only says `qty` is never used. `main` may end without `return 0;`… | correct | check l1.s7.wall-unused |
| `screens[8].prose` | Most Python habits stop the build: a missing `;` or `print(...)`. Two do not: an indented second line after `… | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].canvas` | canvas (console): {"lines": ["$ g++ -std=c++17 main.cpp -o main", "$ ./main", "?"], "title": "Terminal"} | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].widget.options[0]` | KEY: What does it print? -> `0` | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].widget.options[1]` | not: `3` / why: You read `=` as `==`. The test is false, so `flat` is skipped, but `=` still stored 0 in `sig… | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].widget.options[2]` | not: `flat`, then `0` / why: `signals = 0` has the value 0, and 0 counts as false. The body of the `if` never… | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].widget.options[3]` | not: Nothing: it does not compile / why: In Python, `if signals = 0:` is a syntax error. C++ accepts an assig… | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].hints[0]` | In C++, `=` always stores a value, even inside `if ( )`. | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].hints[1]` | After `signals = 0`, what does `signals` hold? That is what line 3 shows. | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].hints[2]` | The condition's value is 0, which is false, and `signals` is now 0. | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].feedback.correct` | The `if` stored 0 and then tested it. | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].feedback.byKey.three` | You read `=` as `==`. The condition stored 0 in `signals`, so the last line prints 0. | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].feedback.byKey.noc` | You expected the Python rule. C++ accepts an assignment as a condition, so this builds and runs. | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].explain.text` | `signals = 0` stores 0 and has the value 0, which is false. The test was meant to be `signals == 0`. Clang wa… | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[8].explain.canvas.lines` | explain canvas: ["$ g++ -std=c++17 main.cpp -o main", "$ ./main", "0"] | correct | checks l1.s8.assign-in-if, l1.s8.gxx-silent |
| `screens[9].prose` | Put the life of a C++ program in order, from typing it to the shell hearing it finished. | correct | GCC manual 3.2; ISO C++17 (N4659) [basic.start.main]/5 (return from main is the exit status) |
| `screens[9].canvas` | canvas (graph): {"nodes": [{"id": "src", "label": "main.cpp", "x": 0.08, "y": 0.25, "shape": "rect"}, {"id": … | correct | GCC manual 3.2; ISO C++17 (N4659) [basic.start.main]/5 (return from main is the exit status) |
| `screens[9].widget.answer` | KEY order: You write and save `main.cpp` > The compiler turns it into `main.o`, with gaps for `std::cout` > T… | correct | GCC manual 3.2; ISO C++17 (N4659) [basic.start.main]/5 (return from main is the exit status) |
| `screens[9].hints[0]` | Nothing can run until the executable exists. | correct | GCC manual 3.2; ISO C++17 (N4659) [basic.start.main]/5 (return from main is the exit status) |
| `screens[9].hints[1]` | The object file comes before the executable. | correct | GCC manual 3.2; ISO C++17 (N4659) [basic.start.main]/5 (return from main is the exit status) |
| `screens[9].hints[2]` | Write, compile, link, run, return. | correct | GCC manual 3.2; ISO C++17 (N4659) [basic.start.main]/5 (return from main is the exit status) |
| `screens[9].feedback.correct` | Write, compile, link, run, return. | correct | GCC manual 3.2; ISO C++17 (N4659) [basic.start.main]/5 (return from main is the exit status) |
| `screens[9].explain.text` | The diagram is the order: source, compiler, object file, linker, executable. Running comes last, and `main`'s… | correct | GCC manual 3.2; ISO C++17 (N4659) [basic.start.main]/5 (return from main is the exit status) |
| `screens[10].prose` | C++ suits pricers: a compiled loop, such as a binomial tree, runs many times faster than the same loop in pla… | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].canvas` | canvas (console): {"lines": ["main.cpp: In function 'int main()':", "main.cpp:6:15: error: no match for 'oper… | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].widget.answer` | KEY: Tap the line that says, in words, what went wrong. -> ["l2"] | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].hints[0]` | Skip every line that says `note:`. | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].hints[1]` | Only one line says `error:`. | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].hints[2]` | Read it as: there is no `<<` that takes a stream on the left and a vector on the right. | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].feedback.correct` | No `<<` exists for a stream and a whole vector. | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].feedback.byKey.l6` | You picked a `note:`. Notes list every `<<` the compiler tried and rejected; the problem is stated once, in t… | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].feedback.byKey.l7` | You picked a `note:`. Notes list every `<<` the compiler tried and rejected; the problem is stated once, in t… | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].feedback.byKey.l8` | You picked a `note:`. The notes only list rejected candidates. Read the `error:` line instead. | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].feedback.byKey.l5` | That line says which header the notes come from. The problem itself is in the `error:` line. | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `screens[10].explain.text` | In words: `std::cout` has no `<<` for a whole `std::vector<double>`, so loop and print each close. The notes … | correct | checks l1.s10.vector-error, l1.s10.compiled-loop |
| `quiz[0].prose` | ```text main.cpp:5:18: error: 'pirce' was not declared in this scope; did you mean 'price'? 5 / std::cout << … | correct | check l1.q0.did-you-mean |
| `quiz[0].widget.options[0]` | KEY: What is the fix? -> Change `pirce` to `price` on line 5 | correct | check l1.q0.did-you-mean |
| `quiz[0].widget.options[1]` | not: Declare a new variable `pirce` above line 5 / why: That silences the error but prints a different, new v… | correct | check l1.q0.did-you-mean |
| `quiz[0].widget.options[2]` | not: Add `#include <pirce>` / why: Headers bring in library names. `pirce` is a misspelling of your own varia… | correct | check l1.q0.did-you-mean |
| `quiz[0].widget.options[3]` | not: Add a semicolon to line 4 / why: A missing semicolon gives `expected ';'`. This message says a name is u… | correct | check l1.q0.did-you-mean |
| `quiz[0].feedback.correct` | A typo in a name: the compiler even suggests the fix. | correct | check l1.q0.did-you-mean |
| `quiz[0].explain.text` | "Not declared in this scope" means the compiler has never met that name. Here it is a typo, and the compiler … | correct | check l1.q0.did-you-mean |
| `quiz[1].prose` | You build with `g++ -std=c++17 prices.cpp -o pricer`. | correct | GCC manual 3.2: `-o file` names the output; shell: `./name` runs a file in the current folder |
| `quiz[1].widget.options[0]` | KEY: Which command runs the program? -> `./pricer` | correct | GCC manual 3.2: `-o file` names the output; shell: `./name` runs a file in the current folder |
| `quiz[1].widget.options[1]` | not: `./prices.cpp` / why: `prices.cpp` is the source text. The machine runs the executable that `-o` named. | correct | GCC manual 3.2: `-o file` names the output; shell: `./name` runs a file in the current folder |
| `quiz[1].widget.options[2]` | not: `python3 pricer` / why: `pricer` is machine code, not Python. Run it directly with `./`. | correct | GCC manual 3.2: `-o file` names the output; shell: `./name` runs a file in the current folder |
| `quiz[1].widget.options[3]` | not: `g++ pricer` / why: `g++` builds programs; it does not run them. | correct | GCC manual 3.2: `-o file` names the output; shell: `./name` runs a file in the current folder |
| `quiz[1].feedback.correct` | `-o pricer` named the executable. | correct | GCC manual 3.2: `-o file` names the output; shell: `./name` runs a file in the current folder |
| `quiz[1].explain.text` | `-o pricer` tells g++ to call the executable `pricer`. `./` means "in this folder", so `./pricer` runs it. | correct | GCC manual 3.2: `-o file` names the output; shell: `./name` runs a file in the current folder |
| `quiz[2].prose` | The program starts with `#include <iostream>` and nothing else above `main`. | correct | checks l1.q2.no-std, l1.q2.print |
| `quiz[2].widget.options[0]` | KEY: Which line, inside `main`, compiles? -> `std::cout << "hi" << '\n';` | correct | checks l1.q2.no-std, l1.q2.print |
| `quiz[2].widget.options[1]` | not: `print("hi")` / why: That is Python. C++ has no `print` function here; it uses `std::cout <<`. | correct | checks l1.q2.no-std, l1.q2.print |
| `quiz[2].widget.options[2]` | not: `std::cout << "hi" << '\n'` / why: A statement like this one must end with `;`. Without it, the compiler… | correct | checks l1.q2.no-std, l1.q2.print |
| `quiz[2].widget.options[3]` | not: `cout << "hi" << '\n';` / why: `cout` lives inside `std`. Without `std::` the compiler does not know the… | correct | checks l1.q2.no-std, l1.q2.print |
| `quiz[2].feedback.correct` | `std::`, `<<` and a closing `;`. | correct | checks l1.q2.no-std, l1.q2.print |
| `quiz[2].explain.text` | C++ needs the full name `std::cout`, and a statement like this one ends with `;`. `print` is a Python habit. | correct | checks l1.q2.no-std, l1.q2.print |
| `quiz[3].prose` | A build prints two warnings and no errors. | correct | check l1.s7.wall-unused (a build with a warning still writes the executable) |
| `quiz[3].widget.options[0]` | KEY: Is there a new executable? -> Yes: warnings do not stop the build | correct | check l1.s7.wall-unused (a build with a warning still writes the executable) |
| `quiz[3].widget.options[1]` | not: No: any warning stops the build / why: You read warnings as errors. Only an `error:` line stops the buil… | correct | check l1.s7.wall-unused (a build with a warning still writes the executable) |
| `quiz[3].widget.options[2]` | not: Only an object file, with no executable / why: Warnings stop neither step. Both compile and link finish. | correct | check l1.s7.wall-unused (a build with a warning still writes the executable) |
| `quiz[3].widget.options[3]` | not: No, the old executable is kept / why: With no errors, the linker writes a new executable over the old on… | correct | check l1.s7.wall-unused (a build with a warning still writes the executable) |
| `quiz[3].feedback.correct` | Only errors stop a build. | correct | check l1.s7.wall-unused (a build with a warning still writes the executable) |
| `quiz[3].explain.text` | A warning is advice about code that compiles; the build still finishes. An error means there is no new execut… | correct | check l1.s7.wall-unused (a build with a warning still writes the executable) |
| `summary.ideas[0]` | A C++ program is built before it runs: the compiler makes an object file and the linker makes the executable. | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | `./main` runs the executable, so every edit needs a fresh build. | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | Read `file:line:column: error:`, then check the named line and the one above it. Warnings do not stop a build. | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \texttt{main.cpp} \xrightarrow{\text{compile}} \texttt{main.o} \xrightarrow{\text{link}} \texttt{main} / `g++… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | `if (x = 0)` compiles: it stores 0 and tests false. Comparison is `==`. | correct | restates the lesson: see the rows of the screens it summarises |

## l2-fixed-types.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | In Python, `7 / 2` is 3.5. Here is the same sum in C++. ```cpp int a = 7; int b = 2; std::cout << a / b << '\… | correct | check l2.types (7 / 2 prints 3); ISO C++17 (N4659) [expr.mul]/4 |
| `screens[0].canvas` | canvas (number-line): {"min": 0, "max": 5, "step": 0.5, "labels": 2} | correct | check l2.types (7 / 2 prints 3); ISO C++17 (N4659) [expr.mul]/4 |
| `screens[0].widget.answer` | KEY: What does the C++ program print? -> 3 (3) | correct | check l2.types (7 / 2 prints 3); ISO C++17 (N4659) [expr.mul]/4 |
| `screens[0].widget.wrong[0]` | slip py = 3.5: You divided as Python's `/` does. In C++, two `int`s give an `int`, so the fraction is dropped. | correct | check l2.types (7 / 2 prints 3); ISO C++17 (N4659) [expr.mul]/4 |
| `screens[0].widget.wrong[1]` | slip round = 4: You rounded 3.5 up. C++ does not round here; it drops the fraction. | correct | check l2.types (7 / 2 prints 3); ISO C++17 (N4659) [expr.mul]/4 |
| `screens[0].hints[0]` | `a` and `b` are both declared `int`. | correct | check l2.types (7 / 2 prints 3); ISO C++17 (N4659) [expr.mul]/4 |
| `screens[0].hints[1]` | An `int` holds whole numbers only, and so does `int / int`. | correct | check l2.types (7 / 2 prints 3); ISO C++17 (N4659) [expr.mul]/4 |
| `screens[0].hints[2]` | The exact answer 3.5 loses its fractional part. | correct | check l2.types (7 / 2 prints 3); ISO C++17 (N4659) [expr.mul]/4 |
| `screens[0].feedback.correct` | `int / int` gives an `int`: the .5 is dropped. | correct | check l2.types (7 / 2 prints 3); ISO C++17 (N4659) [expr.mul]/4 |
| `screens[0].explain.text` | Each variable was declared `int`, so `a / b` is worked out in whole numbers. 3.5 loses its .5 and becomes 3. … | correct | check l2.types (7 / 2 prints 3); ISO C++17 (N4659) [expr.mul]/4 |
| `screens[1].prose` | An `int` is 4 bytes, 32 bits, shown here a byte per box. It starts as `int count = 2147483645;`. Slide to add… | correct | check l2.s1.wrap; slider arithmetic: (2147483645 + 3) / 0 = -2147483648 |
| `screens[1].canvas` | canvas (array): {"cells": ["01111111", "11111111", "11111111", "11111101"], "showIndex": false} | correct | check l2.s1.wrap; slider arithmetic: (2147483645 + 3) / 0 = -2147483648 |
| `screens[1].widget.answer` | KEY: What does `count` hold after you add 1 three times? -> -2147483648 (−2147483648) | correct | check l2.s1.wrap; slider arithmetic: (2147483645 + 3) / 0 = -2147483648 |
| `screens[1].widget.wrong[0]` | slip nowrap = 2147483648: That is the true sum, but an `int` cannot hold it. Slide to 3: the top bit flips an… | correct | check l2.s1.wrap; slider arithmetic: (2147483645 + 3) / 0 = -2147483648 |
| `screens[1].widget.wrong[1]` | slip stick = 2147483647: That is the value after two additions, the largest an `int` holds. The third one doe… | correct | check l2.s1.wrap; slider arithmetic: (2147483645 + 3) / 0 = -2147483648 |
| `screens[1].hints[0]` | Slide to 3 and read the caption. | correct | check l2.s1.wrap; slider arithmetic: (2147483645 + 3) / 0 = -2147483648 |
| `screens[1].feedback.correct` | It wrapped round to the most negative `int`. | correct | check l2.s1.wrap; slider arithmetic: (2147483645 + 3) / 0 = -2147483648 |
| `screens[1].explain.text` | 2,147,483,647 is `0111...1`, the largest `int`. Adding 1 carries into the top bit, which marks a negative num… | correct | check l2.s1.wrap; slider arithmetic: (2147483645 + 3) / 0 = -2147483648 |
| `screens[2].prose` | In C++ every variable has a **type** fixed when you declare it, as in `int qty = 500;`, and it never changes.… | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[2].canvas` | canvas (table): {"columns": ["Type", "sizeof", "Holds"], "rows": [["`int`", "4", "−2,147,483,648 to 2,147,483… | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[2].widget.answer` | KEY: Suppose a day's traded volume across a market comes to 3 billion shares. Tap the type that should count … | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[2].hints[0]` | Compare 3 billion with the range of `int`. | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[2].hints[1]` | `int` stops near 2.1 billion. | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[2].hints[2]` | A whole-number count above that needs 8 bytes. | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[2].feedback.correct` | `long long` counts to about 9.2 × 10¹⁸, exactly. | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[2].feedback.byKey.r0` | 3 billion is above `int`'s limit of 2,147,483,647, so the counter would wrap negative, as on the last screen. | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[2].feedback.byKey.r2` | A `double` holds 3 billion, but a count is a whole number. An integer type adds exactly, every time. | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[2].feedback.byKey.r5` | A `std::string` holds text. You cannot add 1 to it as a counter. | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[2].explain.text` | A volume is a whole number that can pass 2.1 billion, so it needs the 8-byte `long long`. A `double` would ho… | correct | check l2.types (sizes on this build); ISO C++17 (N4659) [basic.fundamental]; 3e9 > 2,147,483,647 |
| `screens[3].prose` | `auto` asks the compiler to give a variable the type of the value on the right. It is still fixed, just not t… | correct | check l2.s3.auto |
| `screens[3].canvas` | canvas (table): {"columns": ["Type", "sizeof", "Holds"], "rows": [["`int`", "4", "−2,147,483,648 to 2,147,483… | correct | check l2.s3.auto |
| `screens[3].widget.options[0]` | KEY: What type does `r` get, and what value? -> `int`, holding 3 | correct | check l2.s3.auto |
| `screens[3].widget.options[1]` | not: `double`, holding 3.5 / why: You let `auto` pick the type of the true answer. It copies the type of `7 /… | correct | check l2.s3.auto |
| `screens[3].widget.options[2]` | not: `double`, holding 3.0 / why: Nothing on the right is a `double`. `7` and `2` are both `int` literals. | correct | check l2.s3.auto |
| `screens[3].widget.options[3]` | not: A type called `auto`, holding 3 / why: `auto` is not a type of its own. The compiler replaces it with th… | correct | check l2.s3.auto |
| `screens[3].hints[0]` | What is the type of `7 / 2` on its own? | correct | check l2.s3.auto |
| `screens[3].hints[1]` | `7` and `2` are written without a decimal point. | correct | check l2.s3.auto |
| `screens[3].hints[2]` | `int / int` is an `int`, so `r` is an `int` holding 3. | correct | check l2.s3.auto |
| `screens[3].feedback.correct` | `auto` copies the type of `7 / 2`: `int`. | correct | check l2.s3.auto |
| `screens[3].feedback.byKey.d35` | You let `auto` pick the type of the true answer. It copies the type of the expression, `int / int`, so 3. | correct | check l2.s3.auto |
| `screens[3].explain.text` | `7 / 2` is an `int` expression with value 3, so `auto r` becomes `int r`. Write `auto r = 7.0 / 2;` and `r` i… | correct | check l2.s3.auto |
| `screens[4].prose` | This function compiles and is wrong: `average(3, 4)` returns 3. The division happens between two `int`s, befo… | correct | checks l2.s4.fb-test-1, l2.s4.fb-test-5 |
| `screens[4].canvas` | canvas (table): {"columns": ["Type", "sizeof", "Holds"], "rows": [["`int`", "4", "−2,147,483,648 to 2,147,483… | correct | checks l2.s4.fb-test-1, l2.s4.fb-test-5 |
| `screens[4].widget.solution` | code: Fix `average` so that `average(3, 4)` is 3.5. (6 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l2.s4.fb-test-1, l2.s4.fb-test-5 |
| `screens[4].hints[0]` | Make one side of the division a `double` before dividing. | correct | checks l2.s4.fb-test-1, l2.s4.fb-test-5 |
| `screens[4].hints[1]` | Test 5 adds 2,147,483,647 to itself. Where does that sum live? | correct | checks l2.s4.fb-test-1, l2.s4.fb-test-5 |
| `screens[4].hints[2]` | `return (static_cast<double>(a) + b) / 2;` converts before the addition, so nothing overflows. | correct | checks l2.s4.fb-test-1, l2.s4.fb-test-5 |
| `screens[4].feedback.correct` | Converting first makes every step a `double` step. | correct | checks l2.s4.fb-test-1, l2.s4.fb-test-5 |
| `screens[4].feedback.byKey.test-1` | `average(3, 4)` came back as 3: `(a + b) / 2` divides two `int`s, and only then is 3 turned into 3.0. | correct | checks l2.s4.fb-test-1, l2.s4.fb-test-5 |
| `screens[4].feedback.byKey.test-5` | Test 5 adds 2,147,483,647 to itself. In `int` that sum wraps negative before any division. Convert before add… | correct | checks l2.s4.fb-test-1, l2.s4.fb-test-5 |
| `screens[4].explain.text` | Once `a` is a `double`, `a + b` and the division are done in `double`, so nothing is dropped and nothing wrap… | correct | checks l2.s4.fb-test-1, l2.s4.fb-test-5 |
| `screens[5].prose` | Prices here are whole pence. This function passes small orders and fails a big one: 20,000 shares at 107,500p… | correct | checks l2.s5.fb-test-2, l2.s5.narrow |
| `screens[5].canvas` | canvas (table): {"columns": ["Type", "sizeof", "Holds"], "rows": [["`int`", "4", "−2,147,483,648 to 2,147,483… | correct | checks l2.s5.fb-test-2, l2.s5.narrow |
| `screens[5].widget.solution` | code: Fix `shares_value` so that it returns the order's value in pence for any size. (5 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l2.s5.fb-test-2, l2.s5.narrow |
| `screens[5].hints[0]` | The multiplication is fine. Where does its result go? | correct | checks l2.s5.fb-test-2, l2.s5.narrow |
| `screens[5].hints[1]` | `int value` holds at most 2,147,483,647. | correct | checks l2.s5.fb-test-2, l2.s5.narrow |
| `screens[5].hints[2]` | Declare `long long value`, or return `qty * pence` directly. | correct | checks l2.s5.fb-test-2, l2.s5.narrow |
| `screens[5].feedback.correct` | A `long long` result needs a `long long` to hold it. | correct | checks l2.s5.fb-test-2, l2.s5.narrow |
| `screens[5].feedback.byKey.test-2` | 2,150,000,000 does not fit in `int value`, so it was squeezed in and came out negative. Store it in a `long l… | correct | checks l2.s5.fb-test-2, l2.s5.narrow |
| `screens[5].explain.text` | `qty * pence` is worked out in `long long`, then stored in an `int` that cannot hold it. C++ narrows it silen… | correct | checks l2.s5.fb-test-2, l2.s5.narrow |
| `screens[6].prose` | Python's `//` rounds down, so `-7 // 2` is −4. C++ integer division does something else. ```cpp std::cout << … | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[6].canvas` | canvas (table): {"columns": ["Expression", "Python", "C++"], "rows": [["`7 / 2` (`//` in Python)", "3", "3"],… | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[6].widget.answer` | KEY: What does the C++ line print? -> -3 (−3) | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[6].widget.wrong[0]` | slip floor = -4: You rounded down, as Python's `//` does. C++ truncates towards zero, so −3.5 becomes −3. | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[6].widget.wrong[1]` | slip exact = -3.5: Both sides are `int`, so the answer is a whole number. | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[6].widget.wrong[2]` | slip sign = 3: A negative number divided by a positive one is negative. C++ truncates −3.5 towards zero to −3… | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[6].hints[0]` | C++ drops the fraction, whatever the sign. | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[6].hints[1]` | −3.5 without its fraction is which whole number? | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[6].hints[2]` | Dropping .5 from −3.5 moves towards zero: −3. | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[6].feedback.correct` | C++ drops the fraction, towards zero. | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[6].explain.text` | C++ integer division truncates towards zero: 3.5 becomes 3 and −3.5 becomes −3. Python's `//` floors, so the … | correct | check l2.types (-7 / 2 prints -3); ISO C++17 (N4659) [expr.mul]/4 (truncation towards zero); Python floors: -7 // 2 == -4 |
| `screens[7].prose` | A fill price arrives as a `double` in pounds, and the ledger wants whole pence. ```cpp double price = 19.99; … | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].canvas` | canvas (number-line): {"min": 1998, "max": 2000, "step": 0.5, "labels": 2} | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].widget.options[0]` | KEY: What does `pence` hold? -> 1998 | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].widget.options[1]` | not: 1999 / why: You did the sum on paper. `19.99 * 100` is stored as 1998.9999999999998, and turning a `doub… | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].widget.options[2]` | not: 19 / why: The multiplication happens first, in `double`. Only its result is cut down to an `int`. | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].widget.options[3]` | not: It does not compile / why: C++ converts a `double` to an `int` silently. Only some warning flags mention… | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].hints[0]` | 19.99 has no exact binary form, like 0.1 in Python. | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].hints[1]` | Is `19.99 * 100` stored a little above or a little below 1999? | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].hints[2]` | It is 1998.9999999999998, and the conversion to `int` drops everything after the point. | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].feedback.correct` | Truncation turns 1998.9999999999998 into 1998. | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].feedback.byKey.1999` | You expected rounding. Assigning a `double` to an `int` drops the fraction, and `19.99 * 100` is 1998.9999999… | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[7].explain.text` | `19.99` is stored slightly low, so `price * 100` is 1998.9999999999998. Assigning it to an `int` truncates to… | correct | checks l2.s7.1999, l2.s7.pence |
| `screens[8].prose` | Every result you met follows one rule: an operation works in its operands' type, and one `double` makes it `d… | correct | check l2.types (0.75, 0, 0, 0 for the four options) |
| `screens[8].widget.options[0]` | KEY: Which expression gives 0.75? -> `3.0 / 4` | correct | check l2.types (0.75, 0, 0, 0 for the four options) |
| `screens[8].widget.options[1]` | not: `3 / 4` / why: Both are `int`, so the answer is 0. | correct | check l2.types (0.75, 0, 0, 0 for the four options) |
| `screens[8].widget.options[2]` | not: `3 / 4 * 1.0` / why: The division runs first, in `int`, and gives 0. Multiplying by 1.0 afterwards keeps… | correct | check l2.types (0.75, 0, 0, 0 for the four options) |
| `screens[8].widget.options[3]` | not: `static_cast<double>(3 / 4)` / why: That converts after dividing. `3 / 4` is already 0, so you get 0.0. | correct | check l2.types (0.75, 0, 0, 0 for the four options) |
| `screens[8].hints[0]` | Find where the first `double` appears, and whether the division has already happened. | correct | check l2.types (0.75, 0, 0, 0 for the four options) |
| `screens[8].feedback.correct` | The `double` is there before the division. | correct | check l2.types (0.75, 0, 0, 0 for the four options) |
| `screens[8].explain.text` | `3.0` is a `double`, so `3.0 / 4` divides in `double` and gives 0.75. Every other option divides two `int`s f… | correct | check l2.types (0.75, 0, 0, 0 for the four options) |
| `screens[9].prose` | Exchanges quote prices in whole ticks, so a program can store each price as an integer number of ticks. Integ… | correct | checks l2.s9.fb-test-3, l2.s9.fb-test-2; tick sizes: MiFID II RTS 11 (tick size regime); integers add exactly |
| `screens[9].canvas` | canvas (table): {"columns": ["Buy (p)", "Sell (p)", "Shares", "P&L (£)"], "rows": [["10,150", "10,225", "4,00… | correct | checks l2.s9.fb-test-3, l2.s9.fb-test-2; tick sizes: MiFID II RTS 11 (tick size regime); integers add exactly |
| `screens[9].widget.solution` | code: Write `pnl_pounds(buy_pence, sell_pence, qty)`: the profit in pounds on buying and then selling `qty` s… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l2.s9.fb-test-3, l2.s9.fb-test-2; tick sizes: MiFID II RTS 11 (tick size regime); integers add exactly |
| `screens[9].hints[0]` | Work out the pence first: the change per share times the shares. | correct | checks l2.s9.fb-test-3, l2.s9.fb-test-2; tick sizes: MiFID II RTS 11 (tick size regime); integers add exactly |
| `screens[9].hints[1]` | Row 2 is −3,000,000,000 pence. Which type holds that? | correct | checks l2.s9.fb-test-3, l2.s9.fb-test-2; tick sizes: MiFID II RTS 11 (tick size regime); integers add exactly |
| `screens[9].hints[2]` | `long long pence = (sell_pence - buy_pence) * qty;` then `return pence / 100.0;`. | correct | checks l2.s9.fb-test-3, l2.s9.fb-test-2; tick sizes: MiFID II RTS 11 (tick size regime); integers add exactly |
| `screens[9].feedback.correct` | Exact pence, then one conversion to pounds. | correct | checks l2.s9.fb-test-3, l2.s9.fb-test-2; tick sizes: MiFID II RTS 11 (tick size regime); integers add exactly |
| `screens[9].feedback.byKey.test-3` | A 1p profit came back wrong. If you got 0, you divided by `100`, an `int`: write `100.0`. | correct | checks l2.s9.fb-test-3, l2.s9.fb-test-2; tick sizes: MiFID II RTS 11 (tick size regime); integers add exactly |
| `screens[9].feedback.byKey.test-2` | Test 2 is −3,000,000,000 pence. If it came back positive or small, an `int` held it on the way. Keep it in `l… | correct | checks l2.s9.fb-test-3, l2.s9.fb-test-2; tick sizes: MiFID II RTS 11 (tick size regime); integers add exactly |
| `screens[9].explain.text` | The pence sum is exact in `long long`, even at three billion. Dividing by `100.0` makes the last step a `doub… | correct | checks l2.s9.fb-test-3, l2.s9.fb-test-2; tick sizes: MiFID II RTS 11 (tick size regime); integers add exactly |
| `quiz[0].prose` | ```cpp bool up = 101.5 > 100.0; std::cout << up << '\n'; ``` | correct | check l2.q0.bool |
| `quiz[0].widget.options[0]` | KEY: What does it print? -> `1` | correct | check l2.q0.bool |
| `quiz[0].widget.options[1]` | not: `true` / why: `std::cout` prints a `bool` as 1 or 0 unless you ask for words with `std::boolalpha`. | correct | check l2.q0.bool |
| `quiz[0].widget.options[2]` | not: `True` / why: That is Python's spelling. C++ prints the number 1. | correct | check l2.q0.bool |
| `quiz[0].widget.options[3]` | not: `101.5` / why: `up` holds the result of the comparison, not a price. | correct | check l2.q0.bool |
| `quiz[0].feedback.correct` | A `bool` prints as 1 or 0. | correct | check l2.q0.bool |
| `quiz[0].explain.text` | The comparison is true, so `up` is `true`, and `std::cout` prints `true` as 1. Write `std::cout << std::boola… | correct | check l2.q0.bool |
| `quiz[1].widget.answer` | KEY: How many bytes does `sizeof(long long)` report? -> 8 (8) | correct | check l2.types (sizeof(long long) is 8) |
| `quiz[1].widget.wrong[0]` | slip four = 4: 4 bytes is an `int`. `long long` is twice the size. | correct | check l2.types (sizeof(long long) is 8) |
| `quiz[1].widget.wrong[1]` | slip bits = 64: 64 is the number of bits. `sizeof` counts bytes. | correct | check l2.types (sizeof(long long) is 8) |
| `quiz[1].feedback.correct` | 8 bytes, 64 bits. | correct | check l2.types (sizeof(long long) is 8) |
| `quiz[1].explain.text` | A `long long` is 8 bytes, or 64 bits, so it reaches about 9.2 × 10¹⁸. An `int` is 4 bytes. | correct | check l2.types (sizeof(long long) is 8) |
| `quiz[2].prose` | ```cpp int ticks = 2147483647; ticks = ticks + 1; ``` | correct | check l2.s1.wrap (this build); ISO C++17 (N4659) [expr]/4 (overflow is undefined) |
| `quiz[2].widget.options[0]` | KEY: What does `ticks` hold, in practice? -> −2,147,483,648 | correct | check l2.s1.wrap (this build); ISO C++17 (N4659) [expr]/4 (overflow is undefined) |
| `quiz[2].widget.options[1]` | not: 2,147,483,648 / why: That number does not fit in an `int`. The result wraps round instead. | correct | check l2.s1.wrap (this build); ISO C++17 (N4659) [expr]/4 (overflow is undefined) |
| `quiz[2].widget.options[2]` | not: 2,147,483,647 / why: C++ does not stop at the limit; adding 1 carries into the sign bit. | correct | check l2.s1.wrap (this build); ISO C++17 (N4659) [expr]/4 (overflow is undefined) |
| `quiz[2].widget.options[3]` | not: The program stops with an error / why: Nothing checks for overflow at run time. It happens silently. | correct | check l2.s1.wrap (this build); ISO C++17 (N4659) [expr]/4 (overflow is undefined) |
| `quiz[2].feedback.correct` | It wraps to the most negative `int`. | correct | check l2.s1.wrap (this build); ISO C++17 (N4659) [expr]/4 (overflow is undefined) |
| `quiz[2].explain.text` | The carry lands in the sign bit, so the value wraps to −2,147,483,648. Formally this is undefined behaviour, … | correct | check l2.s1.wrap (this build); ISO C++17 (N4659) [expr]/4 (overflow is undefined) |
| `quiz[3].prose` | ```cpp double share = 1 / 4; ``` | correct | check l2.q3.quarter |
| `quiz[3].widget.options[0]` | KEY: What does `share` hold? -> 0 | correct | check l2.q3.quarter |
| `quiz[3].widget.options[1]` | not: 0.25 / why: The type on the left does not reach the right. `1 / 4` is worked out in `int` first. | correct | check l2.q3.quarter |
| `quiz[3].widget.options[2]` | not: It does not compile / why: Storing an `int` in a `double` is allowed and silent. | correct | check l2.q3.quarter |
| `quiz[3].widget.options[3]` | not: 1 / why: `int` division drops the fraction of 0.25; it does not round up. | correct | check l2.q3.quarter |
| `quiz[3].feedback.correct` | `1 / 4` is 0 before `share` ever sees it. | correct | check l2.q3.quarter |
| `quiz[3].explain.text` | `1 / 4` divides two `int`s and gives 0, which is then stored as 0.0. Write `1.0 / 4` to get 0.25. | correct | check l2.q3.quarter |
| `summary.ideas[0]` | Every variable has a fixed type, which sets its size (`sizeof`) and range. `auto` takes the type of the value… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | An operation works in its operands' type: `int / int` drops the fraction, towards zero, and one `double` make… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | `int` stops at 2,147,483,647. Going past it is undefined behaviour, and in practice the value usually wraps s… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | 7 / 2 = 3, \quad -7 / 2 = -3, \quad 7.0 / 2 = 3.5 / Convert with `static_cast<double>(x)` before dividing, no… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | `int pence = 19.99 * 100;` is 1998: the `double` is a hair low and the conversion truncates. | correct | restates the lesson: see the rows of the screens it summarises |

## l3-branches-and-loops.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | Five closes and a C++ loop over them. Read it as you would Python. ```cpp int ups = 0; for (int i = 1; i < 5;… | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].canvas` | canvas (array): {"cells": [100, 104, 101, 106, 103], "showIndex": true} | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].widget.answer` | KEY: Tap every close that adds 1 to `ups`. -> ["c1", "c3"] | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].widget.wrong[0]` | slip set first = ["c1", "c2", "c3", "c4"]: You compared every close with the first one, 100. The loop compare… | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].hints[0]` | `i` runs 1, 2, 3, 4. Each turn compares `prices[i]` with the close before it. | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].hints[1]` | Index 2 holds 101. What came the day before? | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].hints[2]` | 104 beats 100 and 106 beats 101. The others fell. | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].feedback.correct` | Day 1 and day 3 beat the close before them. | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].feedback.byKey.c0` | The loop starts at `i = 1`, so index 0 is never counted itself; it is only the day before index 1. | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].feedback.byKey.c2` | 101 is below 104, the close before it, so that day fell. | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].feedback.byKey.c4` | 103 is below 106, the close before it, so that day fell. | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[0].explain.text` | The loop runs `i` from 1 while `i < 5`, adding 1 each turn with `++i`. Days 1 and 3 beat their neighbour, so … | correct | derivation: 104 > 100 and 106 > 101; 101 < 104 and 103 < 106; ups = 2 |
| `screens[1].prose` | A backtest tracks the **drawdown**: the close's fall below its peak so far, as a fraction of that peak. Slide… | correct | check l3.s1.drawdown; drawdown: Bacon, Practical Portfolio Performance Measurement and Attribution, ch. 4 (maximum drawdown from a running peak) |
| `screens[1].canvas` | canvas (array): {"cells": [100, 110, 99, 105, 88, 95], "showIndex": true} | correct | check l3.s1.drawdown; drawdown: Bacon, Practical Portfolio Performance Measurement and Attribution, ch. 4 (maximum drawdown from a running peak) |
| `screens[1].widget.answer` | KEY: What is the largest drawdown you see, in %? -> 0.2 (20%) | correct | check l3.s1.drawdown; drawdown: Bacon, Practical Portfolio Performance Measurement and Attribution, ch. 4 (maximum drawdown from a running peak) |
| `screens[1].widget.wrong[0]` | slip start = 0.12: You measured from the first close, 100. Drawdown is measured from the highest close so far… | correct | check l3.s1.drawdown; drawdown: Bacon, Practical Portfolio Performance Measurement and Attribution, ch. 4 (maximum drawdown from a running peak) |
| `screens[1].widget.wrong[1]` | slip first = 0.1: That is the fall to day 2. Day 4 falls further below the same peak. | correct | check l3.s1.drawdown; drawdown: Bacon, Practical Portfolio Performance Measurement and Attribution, ch. 4 (maximum drawdown from a running peak) |
| `screens[1].hints[0]` | Stop on each day and read the caption. Which day is lowest against its peak? | correct | check l3.s1.drawdown; drawdown: Bacon, Practical Portfolio Performance Measurement and Attribution, ch. 4 (maximum drawdown from a running peak) |
| `screens[1].feedback.correct` | From the 110 peak down to 88 is a fall of 20%. | correct | check l3.s1.drawdown; drawdown: Bacon, Practical Portfolio Performance Measurement and Attribution, ch. 4 (maximum drawdown from a running peak) |
| `screens[1].explain.text` | The peak only ever moves up: 100, then 110, where it stays. Day 4 closes at 88, which is $(110 - 88) / 110 = … | correct | check l3.s1.drawdown; drawdown: Bacon, Practical Portfolio Performance Measurement and Attribution, ch. 4 (maximum drawdown from a running peak) |
| `screens[2].prose` | A C++ `for` has three parts: a start `int i = 1`, a test `i < prices.size()` and a step `++i`. The test is ch… | correct | derivation: i = 1..5 pass i < 6: five turns |
| `screens[2].canvas` | canvas (array): {"cells": [100, 110, 99, 105, 88, 95], "showIndex": true} | correct | derivation: i = 1..5 pass i < 6: five turns |
| `screens[2].widget.answer` | KEY: How many times does the body run? -> 5 (5) | correct | derivation: i = 1..5 pass i < 6: five turns |
| `screens[2].widget.wrong[0]` | slip six = 6: You counted every close. The loop starts at 1, so index 0 is skipped. | correct | derivation: i = 1..5 pass i < 6: five turns |
| `screens[2].widget.wrong[1]` | slip four = 4: The test is `i < 6`, so 5 still passes. The loop stops only when `i` reaches 6. | correct | derivation: i = 1..5 pass i < 6: five turns |
| `screens[2].hints[0]` | List the values of `i` that pass the test. | correct | derivation: i = 1..5 pass i < 6: five turns |
| `screens[2].hints[1]` | `i` starts at index 1, not 0. | correct | derivation: i = 1..5 pass i < 6: five turns |
| `screens[2].hints[2]` | `i` is 1, 2, 3, 4, 5; at 6 the test fails. | correct | derivation: i = 1..5 pass i < 6: five turns |
| `screens[2].feedback.correct` | `i` takes 1 to 5: five turns. | correct | derivation: i = 1..5 pass i < 6: five turns |
| `screens[2].explain.text` | The test runs before each turn: 1 to 5 pass and 6 fails, so five turns. Starting at 1 gives every close a day… | correct | derivation: i = 1..5 pass i < 6: five turns |
| `screens[3].prose` | `const std::vector<double>&` hands the function the caller's closes to read, without copying them; level 2 ex… | correct | checks l3.s3.fb-test-2, l3.s3.fb-test-6, l3.s3.fb-error, l3.s3.size-minus-1 |
| `screens[3].canvas` | canvas (array): {"cells": [100, 104, 101, 106, 103], "showIndex": true} | correct | checks l3.s3.fb-test-2, l3.s3.fb-test-6, l3.s3.fb-error, l3.s3.size-minus-1 |
| `screens[3].widget.solution` | code: Write `count_up_days(prices)`: how many closes beat the close before them. (6 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l3.s3.fb-test-2, l3.s3.fb-test-6, l3.s3.fb-error, l3.s3.size-minus-1 |
| `screens[3].hints[0]` | Start the loop at index 1, as on the last screen. | correct | checks l3.s3.fb-test-2, l3.s3.fb-test-6, l3.s3.fb-error, l3.s3.size-minus-1 |
| `screens[3].hints[1]` | Test 2 is empty. Does your loop run at all when `prices.size()` is 0? | correct | checks l3.s3.fb-test-2, l3.s3.fb-test-6, l3.s3.fb-error, l3.s3.size-minus-1 |
| `screens[3].hints[2]` | `for (std::size_t i = 1; i < prices.size(); ++i)` with `if (prices[i] > prices[i - 1]) ++ups;`. | correct | checks l3.s3.fb-test-2, l3.s3.fb-test-6, l3.s3.fb-error, l3.s3.size-minus-1 |
| `screens[3].feedback.correct` | Start at 1, stop before `size()`. | correct | checks l3.s3.fb-test-2, l3.s3.fb-test-6, l3.s3.fb-error, l3.s3.size-minus-1 |
| `screens[3].feedback.byKey.test-2` | The empty vector broke it. With `i < prices.size() - 1`, 0 − 1 wraps, since `size()` is unsigned: about 4 bil… | correct | checks l3.s3.fb-test-2, l3.s3.fb-test-6, l3.s3.fb-error, l3.s3.size-minus-1 |
| `screens[3].feedback.byKey.test-6` | Three equal closes are not up days. Use `>`, not `>=`. | correct | checks l3.s3.fb-test-2, l3.s3.fb-test-6, l3.s3.fb-error, l3.s3.size-minus-1 |
| `screens[3].feedback.byKey.error` | The program stopped. If the message says index out of bounds, your loop read past the last close: test `i < p… | imprecise | check l3.s3.fb-error: a run that stops gets the key test-1 (cpp-grade.js line 736: `error` only when the runner itself fails); finding 8 |
| `screens[3].explain.text` | Starting at 1 means every `prices[i - 1]` exists, and on an empty or one-close vector the loop never runs. `s… | correct | checks l3.s3.fb-test-2, l3.s3.fb-test-6, l3.s3.fb-error, l3.s3.size-minus-1 |
| `screens[4].prose` | Now the drawdown you slid through. `for (double p : prices)` visits each close in turn, like Python's `for p … | correct | checks l3.s4.fb-test-6, l3.s4.fb-test-4, l3.s4.fb-test-1 |
| `screens[4].canvas` | canvas (array): {"cells": [100, 110, 99, 105, 88, 95], "showIndex": true} | correct | checks l3.s4.fb-test-6, l3.s4.fb-test-4, l3.s4.fb-test-1 |
| `screens[4].widget.solution` | code: Write `max_drawdown(prices)`. (7 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l3.s4.fb-test-6, l3.s4.fb-test-4, l3.s4.fb-test-1 |
| `screens[4].hints[0]` | Two variables carry across the loop: the peak so far and the worst fall so far. | correct | checks l3.s4.fb-test-6, l3.s4.fb-test-4, l3.s4.fb-test-1 |
| `screens[4].hints[1]` | Update the peak before you measure today's fall. | correct | checks l3.s4.fb-test-6, l3.s4.fb-test-4, l3.s4.fb-test-1 |
| `screens[4].hints[2]` | Inside the loop: raise `peak` if `p` is higher, then `double fall = (peak - p) / peak;` and keep the larger o… | correct | checks l3.s4.fb-test-6, l3.s4.fb-test-4, l3.s4.fb-test-1 |
| `screens[4].feedback.correct` | A running peak and a running worst: one pass. | correct | checks l3.s4.fb-test-6, l3.s4.fb-test-4, l3.s4.fb-test-1 |
| `screens[4].feedback.byKey.test-6` | In `100, 80, 120, 60` the worst fall is from the new peak 120 down to 60: 0.5. If you got 0.4, your peak stay… | imprecise | check l3.s4.fb-test-6: a peak stuck at 100 gives 0.12 on test 1 (key test-1); finding 11 |
| `screens[4].feedback.byKey.test-1` | Test 1 should give 0.2: from 110 to 88. Measure each fall from the highest close so far, not from the first. | correct | checks l3.s4.fb-test-6, l3.s4.fb-test-4, l3.s4.fb-test-1 |
| `screens[4].feedback.byKey.test-4` | A fall from 100 to 90 is 0.1, a positive fraction. If you got −0.1, subtract the other way: `peak - p`. | imprecise | check l3.s4.fb-test-4: subtracting the other way gives -0.2 on test 1 (key test-1); finding 11 |
| `screens[4].explain.text` | The peak only rises, so one variable holds it. Each close's fall is measured against it, and the worst fall i… | correct | checks l3.s4.fb-test-6, l3.s4.fb-test-4, l3.s4.fb-test-1 |
| `screens[5].prose` | A program reads how many numbers follow, then the numbers. Loop `n` times with `std::cin >>` inside. Print th… | correct | checks l3.s5.fb-test-1, l3.s5.do-while, l3.s5.six-digits |
| `screens[5].canvas` | canvas (array): {"cells": ["3", "1.5", "2.25", "3"], "showIndex": false} | correct | checks l3.s5.fb-test-1, l3.s5.do-while, l3.s5.six-digits |
| `screens[5].widget.solution` | code: Complete the program so it prints the sum of the `n` numbers. (5 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l3.s5.fb-test-1, l3.s5.do-while, l3.s5.six-digits |
| `screens[5].hints[0]` | You know how many numbers to read, so a counting `for` fits. | correct | checks l3.s5.fb-test-1, l3.s5.do-while, l3.s5.six-digits |
| `screens[5].hints[1]` | Read one number per turn into a fresh `double x`. | correct | checks l3.s5.fb-test-1, l3.s5.do-while, l3.s5.six-digits |
| `screens[5].hints[2]` | `for (int i = 0; i < n; ++i) { double x; std::cin >> x; total += x; }` | correct | checks l3.s5.fb-test-1, l3.s5.do-while, l3.s5.six-digits |
| `screens[5].feedback.correct` | `n` turns, one read per turn. | correct | checks l3.s5.fb-test-1, l3.s5.do-while, l3.s5.six-digits |
| `screens[5].feedback.byKey.test-1` | The sum of 1.5, 2.25 and 3 is 6.75. If you got 9.75, you added `n` itself: it was already read before the loo… | correct | checks l3.s5.fb-test-1, l3.s5.do-while, l3.s5.six-digits |
| `screens[5].feedback.byKey.test-2` | With `n` = 0 the loop must not run, and the sum is 0. | correct | checks l3.s5.fb-test-1, l3.s5.do-while, l3.s5.six-digits |
| `screens[5].explain.text` | `for (int i = 0; i < n; ++i)` runs exactly `n` times, and zero times when `n` is 0. `std::cin >>` does not ca… | correct | checks l3.s5.fb-test-1, l3.s5.do-while, l3.s5.six-digits |
| `screens[6].prose` | In Python, `range(len(prices))` stops for you. In C++ you write the test yourself. ```cpp double last = 0; fo… | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].canvas` | canvas (array): {"cells": [101.2, 102.5, 99.8], "showIndex": true} | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].widget.options[0]` | KEY: With these three closes, what happens? -> It reads `prices[3]`, past the end: this app stops it, a norma… | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].widget.options[1]` | not: `last` ends as 99.8 / why: You read `<=` as `<`. The loop also runs with `i = 3`, and there is no `price… | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].widget.options[2]` | not: It throws `std::out_of_range` / why: Only `prices.at(i)` checks the index and throws. `prices[i]` does n… | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].widget.options[3]` | not: It does not compile / why: The compiler does not know how many closes there will be. This compiles clean… | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].hints[0]` | List the values of `i` for which `i <= 3` is true. | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].hints[1]` | The valid indices are 0, 1 and 2. | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].hints[2]` | `i` reaches 3, and `prices[3]` is one past the last close. | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].feedback.correct` | `<=` runs one turn too many. | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].feedback.byKey.last` | You read `<=` as `<`. With `<=`, `i` also takes 3, and `prices[3]` is past the end. | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[6].explain.text` | Indices run from 0 to `size() - 1`, so the test must be `i < prices.size()`. This app's library checks `[]` a… | correct | checks l3.s6.past-end, l3.s6.at-throws |
| `screens[7].prose` | The loops you wrote, in one place. ```cpp for (std::size_t i = 1; i < xs.size(); ++i) // by index for (double… | correct | check l3.s7.scope |
| `screens[7].widget.options[0]` | KEY: After `for (int i = 0; i < 5; ++i) { }` comes `std::cout << i;`. What happens? -> It does not compile: `… | correct | check l3.s7.scope |
| `screens[7].widget.options[1]` | not: It prints 5 / why: That is Python, where the loop variable outlives the loop. In C++ `i` ends with the `… | correct | check l3.s7.scope |
| `screens[7].widget.options[2]` | not: It prints 4 / why: 4 is the last value the body saw, but `i` no longer exists after the loop. | correct | check l3.s7.scope |
| `screens[7].widget.options[3]` | not: It prints 0 / why: `i` is not reset; it is gone. The compiler reports an undeclared name. | correct | check l3.s7.scope |
| `screens[7].hints[0]` | Where was `i` declared? | correct | check l3.s7.scope |
| `screens[7].feedback.correct` | `i` belongs to the loop. | correct | check l3.s7.scope |
| `screens[7].explain.text` | `int i` is declared inside the `for`, so it ends with the loop and `i` is undeclared on the next line. Declar… | correct | check l3.s7.scope |
| `screens[8].prose` | Each of a day's fills arrives as a letter: `L` for the LSE, `C` for Cboe, `T` for Turquoise. Any other letter… | correct | checks l3.s8.fb-test-1, l3.s8.fb-test-3, l3.s8.fallthrough-silent, l3.s8.fallthrough-flag, l3.s8.gxx-fallthrough |
| `screens[8].canvas` | canvas (array): {"cells": ["L", "X", "C", "L", "L", "T", "A"], "showIndex": true} | correct | checks l3.s8.fb-test-1, l3.s8.fb-test-3, l3.s8.fallthrough-silent, l3.s8.fallthrough-flag, l3.s8.gxx-fallthrough |
| `screens[8].widget.solution` | code: Fix and finish `fills_by_venue`: return the counts for LSE, Cboe, Turquoise and other, in that order. (… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l3.s8.fb-test-1, l3.s8.fb-test-3, l3.s8.fallthrough-silent, l3.s8.fallthrough-flag, l3.s8.gxx-fallthrough |
| `screens[8].hints[0]` | Run the starter on `L` in your head. Which counts go up? | correct | checks l3.s8.fb-test-1, l3.s8.fb-test-3, l3.s8.fallthrough-silent, l3.s8.fallthrough-flag, l3.s8.gxx-fallthrough |
| `screens[8].hints[1]` | Every `case` needs a `break` at its end. | correct | checks l3.s8.fb-test-1, l3.s8.fb-test-3, l3.s8.fallthrough-silent, l3.s8.fallthrough-flag, l3.s8.gxx-fallthrough |
| `screens[8].hints[2]` | Add `break;` after `++counts[0]`, a `case 'T':`, and `default: ++counts[3]; break;`. | correct | checks l3.s8.fb-test-1, l3.s8.fb-test-3, l3.s8.fallthrough-silent, l3.s8.fallthrough-flag, l3.s8.gxx-fallthrough |
| `screens[8].feedback.correct` | Each case ends with `break`, and `default` takes the rest. | correct | checks l3.s8.fb-test-1, l3.s8.fb-test-3, l3.s8.fallthrough-silent, l3.s8.fallthrough-flag, l3.s8.gxx-fallthrough |
| `screens[8].feedback.byKey.test-1` | `LLCT` should give 2, 1, 1, 0. If Cboe came out as 3, each `L` fell through into the `C` case: add `break;`. | correct | checks l3.s8.fb-test-1, l3.s8.fb-test-3, l3.s8.fallthrough-silent, l3.s8.fallthrough-flag, l3.s8.gxx-fallthrough |
| `screens[8].feedback.byKey.test-3` | `X` and `A` belong in the fourth count. A `default:` case catches every letter no other case names. | correct | checks l3.s8.fb-test-1, l3.s8.fb-test-3, l3.s8.fallthrough-silent, l3.s8.fallthrough-flag, l3.s8.gxx-fallthrough |
| `screens[8].explain.text` | Without `break`, the `L` case ran on into the `C` case, so every LSE fill also counted as Cboe. `default` cat… | correct | checks l3.s8.fb-test-1, l3.s8.fb-test-3, l3.s8.fallthrough-silent, l3.s8.fallthrough-flag, l3.s8.gxx-fallthrough |
| `quiz[0].prose` | ```cpp if (0.1 + 0.2 == 0.3) { std::cout << "equal\n"; } else { std::cout << "different\n"; } ``` | correct | checks l3.q0.double-eq, l3.q0.repr |
| `quiz[0].widget.options[0]` | KEY: What does it print? -> `different` | correct | checks l3.q0.double-eq, l3.q0.repr |
| `quiz[0].widget.options[1]` | not: `equal` / why: You did the sum on paper. A `double` stores 0.1 and 0.2 slightly off, so the sum is 0.300… | correct | checks l3.q0.double-eq, l3.q0.repr |
| `quiz[0].widget.options[2]` | not: Nothing: `==` cannot compare doubles / why: `==` compiles for doubles. It compares them exactly, which i… | correct | checks l3.q0.double-eq, l3.q0.repr |
| `quiz[0].feedback.correct` | The sum is a hair above 0.3. | correct | checks l3.q0.double-eq, l3.q0.repr |
| `quiz[0].explain.text` | C++ doubles behave like Python floats: `0.1 + 0.2` is 0.30000000000000004. Compare with a tolerance, such as … | correct | checks l3.q0.double-eq, l3.q0.repr |
| `quiz[1].prose` | ```cpp int turns = 0; for (int i = 0; i <= 5; ++i) { ++turns; } ``` | correct | derivation: i = 0..5 inclusive: six turns |
| `quiz[1].widget.answer` | KEY: What is `turns` at the end? -> 6 (6) | correct | derivation: i = 0..5 inclusive: six turns |
| `quiz[1].widget.wrong[0]` | slip five = 5: With `<=`, 5 also passes the test. `i` takes 0, 1, 2, 3, 4 and 5. | correct | derivation: i = 0..5 inclusive: six turns |
| `quiz[1].feedback.correct` | 0 to 5 inclusive is six turns. | correct | derivation: i = 0..5 inclusive: six turns |
| `quiz[1].explain.text` | `i` runs 0, 1, 2, 3, 4, 5: six values, because `<=` lets 5 through. | correct | derivation: i = 0..5 inclusive: six turns |
| `quiz[2].prose` | ```cpp std::vector<double> prices; // empty for (std::size_t i = 0; i < prices.size() - 1; ++i) { std::cout <… | correct | check l3.q2.empty-minus-one |
| `quiz[2].widget.options[0]` | KEY: What happens? -> `prices.size() - 1` wraps to a huge number, so the loop reads past the end | correct | check l3.q2.empty-minus-one |
| `quiz[2].widget.options[1]` | not: The loop never runs, because 0 − 1 is −1 / why: `size()` returns an unsigned `std::size_t`, which cannot… | correct | check l3.q2.empty-minus-one |
| `quiz[2].widget.options[2]` | not: The loop runs once, with `i = 0` / why: The test `0 < 0 - 1` is the question. In unsigned arithmetic 0 −… | correct | check l3.q2.empty-minus-one |
| `quiz[2].widget.options[3]` | not: It does not compile / why: It compiles cleanly. The compiler cannot know the vector will be empty when t… | correct | check l3.q2.empty-minus-one |
| `quiz[2].feedback.correct` | Unsigned 0 − 1 is not −1. | correct | check l3.q2.empty-minus-one |
| `quiz[2].explain.text` | `size()` is a `std::size_t`, which has no negatives, so 0 − 1 wraps to its maximum. The loop then indexes an … | correct | check l3.q2.empty-minus-one |
| `quiz[3].prose` | A stop-loss sells once a close falls below 95. ```cpp int day = 0; for (double p : {101.0, 97.5, 94.0, 92.0, … | correct | check l3.q3.stop-loss |
| `quiz[3].widget.answer` | KEY: What is `day` at the end? -> 2 (2) | correct | check l3.q3.stop-loss |
| `quiz[3].widget.wrong[0]` | slip count = 3: You counted the trigger day too. `break` runs before `++day` on that turn. | correct | check l3.q3.stop-loss |
| `quiz[3].widget.wrong[1]` | slip idx = 4: `break` leaves the loop; the later closes are never visited. | correct | check l3.q3.stop-loss |
| `quiz[3].feedback.correct` | 94.0 triggers the stop on the third close, before `++day`. | correct | check l3.q3.stop-loss |
| `quiz[3].explain.text` | 101.0 and 97.5 pass and add 1 each. 94.0 is below 95, so `break` leaves the loop before `++day`. `day` is 2, … | correct | check l3.q3.stop-loss |
| `summary.ideas[0]` | `for (std::size_t i = 1; i < xs.size(); ++i)` names a start, a test checked before each turn, and a step; `fo… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | Braces mark the body, and a variable declared in a loop ends with it. | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | A `switch` picks a `case` by value and falls through to the next case unless it hits `break`. | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \text{MDD} = \max_t \dfrac{\max_{s \le t} p_s - p_t}{\max_{s \le t} p_s} / One pass: keep the running peak an… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | `i <= prices.size()` runs one turn too many and reads past the end; the test is `i < prices.size()`. | correct | restates the lesson: see the rows of the screens it summarises |

## l4-functions-and-headers.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | In Python a function can sit below the code that calls it. It only has to exist when the call runs. Here is t… | correct | check l4.s0.not-declared |
| `screens[0].canvas` | canvas (pair): {"left": {"kind": "console", "params": {"title": "Terminal", "lines": ["$ g++ -std=c++17 main.… | correct | check l4.s0.not-declared |
| `screens[0].widget.options[0]` | KEY: Why does the build fail? -> The compiler reads from the top and has not met `annualise` by line 5 | correct | check l4.s0.not-declared |
| `screens[0].widget.options[1]` | not: `annualise` is misspelt on line 5 / why: Lines 5 and 8 spell it the same way. The name is right; it arri… | correct | check l4.s0.not-declared |
| `screens[0].widget.options[2]` | not: `main` must be the last function in the file / why: `main` can sit anywhere. What matters is that each n… | correct | check l4.s0.not-declared |
| `screens[0].widget.options[3]` | not: The linker cannot find the body of `annualise` / why: This is a compiler error, `main.cpp:5:18`. The lin… | correct | check l4.s0.not-declared |
| `screens[0].hints[0]` | The compiler reads the file once, from top to bottom. | correct | check l4.s0.not-declared |
| `screens[0].hints[1]` | At line 5, which lines has it read? | correct | check l4.s0.not-declared |
| `screens[0].hints[2]` | It has seen lines 1 to 4, and `annualise` first appears on line 8. | correct | check l4.s0.not-declared |
| `screens[0].feedback.correct` | At line 5 the compiler has never heard of `annualise`. | correct | check l4.s0.not-declared |
| `screens[0].feedback.byKey.spell` | Lines 5 and 8 spell it the same way. The problem is order: line 5 comes first. | correct | check l4.s0.not-declared |
| `screens[0].explain.text` | The compiler reads top to bottom, and every name must be known before it is used. At line 5, `annualise` is s… | correct | check l4.s0.not-declared |
| `screens[1].prose` | This version builds and prints 0.158745, with the function still at the bottom. One line was added. | correct | check l4.s1.declared |
| `screens[1].canvas` | canvas (console): {"lines": ["#include <cmath>", "#include <iostream>", "", "double annualise(double daily_vo… | correct | check l4.s1.declared |
| `screens[1].widget.answer` | KEY: Tap the line that lets line 7 call `annualise`. -> ["l4"] | correct | check l4.s1.declared |
| `screens[1].hints[0]` | Compare with the last screen. Which line is new? | correct | check l4.s1.declared |
| `screens[1].hints[1]` | It sits above `main` and ends with `;`, not a body. | correct | check l4.s1.declared |
| `screens[1].feedback.correct` | Line 4 announces the function before `main` uses it. | correct | check l4.s1.declared |
| `screens[1].feedback.byKey.l10` | That line starts the body, but the compiler reaches it only after line 7. Something above `main` must announc… | correct | check l4.s1.declared |
| `screens[1].feedback.byKey.l1` | `<cmath>` brings in `std::sqrt`, which the body uses. It says nothing about `annualise`. | correct | check l4.s1.declared |
| `screens[1].explain.text` | Line 4 is a **declaration**: the name, the return type and the parameter types, ending in `;`. Lines 10 to 12… | correct | check l4.s1.declared |
| `screens[2].prose` | A **declaration** gives a function's name and types and ends with `;`. A **definition** adds the body in brac… | correct | ISO C++17 (N4659) [basic.def]/2 (a declaration without a body is not a definition); [dcl.fct]/11 (parameter names optional) |
| `screens[2].canvas` | canvas (console): {"lines": ["double annualise(double daily_vol, int days);", "int count_up_days(const std::v… | correct | ISO C++17 (N4659) [basic.def]/2 (a declaration without a body is not a definition); [dcl.fct]/11 (parameter names optional) |
| `screens[2].widget.answer` | KEY: Tap every line that only declares a function, with no body. -> ["l1", "l2"] | correct | ISO C++17 (N4659) [basic.def]/2 (a declaration without a body is not a definition); [dcl.fct]/11 (parameter names optional) |
| `screens[2].widget.wrong[0]` | slip set def = ["l1", "l2", "l3"]: Line 3 has a body in braces, so it is a definition. It declares `half` too… | correct | ISO C++17 (N4659) [basic.def]/2 (a declaration without a body is not a definition); [dcl.fct]/11 (parameter names optional) |
| `screens[2].hints[0]` | Look for braces. | correct | ISO C++17 (N4659) [basic.def]/2 (a declaration without a body is not a definition); [dcl.fct]/11 (parameter names optional) |
| `screens[2].hints[1]` | Line 3 has a body in `{ }`. | correct | ISO C++17 (N4659) [basic.def]/2 (a declaration without a body is not a definition); [dcl.fct]/11 (parameter names optional) |
| `screens[2].hints[2]` | Lines 1 and 2 end in `;` with no body; line 4 is a variable. | correct | ISO C++17 (N4659) [basic.def]/2 (a declaration without a body is not a definition); [dcl.fct]/11 (parameter names optional) |
| `screens[2].feedback.correct` | Lines 1 and 2: types and a semicolon, no body. | correct | ISO C++17 (N4659) [basic.def]/2 (a declaration without a body is not a definition); [dcl.fct]/11 (parameter names optional) |
| `screens[2].feedback.byKey.l4` | `double rate = 0.04;` is a variable with a value, not a function. | correct | ISO C++17 (N4659) [basic.def]/2 (a declaration without a body is not a definition); [dcl.fct]/11 (parameter names optional) |
| `screens[2].explain.text` | Lines 1 and 2 promise functions without bodies. Line 3 is a definition, and line 4 a variable. Parameter name… | correct | ISO C++17 (N4659) [basic.def]/2 (a declaration without a body is not a definition); [dcl.fct]/11 (parameter names optional) |
| `screens[3].prose` | Real projects split the work. `returns.h`, a **header**, holds declarations; `returns.cpp` holds the definiti… | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[3].canvas` | canvas (console): {"lines": ["// returns.h", "#pragma once", "#include <vector>", "std::vector<double> simple… | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[3].widget.answer` | KEY: `main.cpp` calls `annualise(0.01)`. Tap the line whose body runs. -> ["l11"] | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[3].hints[0]` | Which file holds bodies? | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[3].hints[1]` | Look under `// returns.cpp`. | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[3].hints[2]` | Line 11 is the only `annualise` with braces. | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[3].feedback.correct` | The body lives in `returns.cpp`, line 11. | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[3].feedback.byKey.l5` | Line 5 only declares `annualise`; it has no body. It tells `main.cpp` the call is legal, and the linker finds… | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[3].feedback.byKey.l16` | That is the call itself. Its body is elsewhere. | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[3].feedback.byKey.l15` | `#include "returns.h"` pastes in the declarations, not the bodies. | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[3].explain.text` | `#include "returns.h"` pastes the header's text into `main.cpp`, so the compiler sees the declaration and acc… | correct | check l4.s7.multiple-definition and l4.q2.undefined-reference (each .cpp compiled alone, linker joins); 0.01 * sqrt(252) = 0.158745 (check l4.s1.declared) |
| `screens[4].prose` | Line 5 says `int days = 252`: a **default argument**. A call that leaves `days` out gets 252, which is why `a… | correct | check l4.s4.annualise; check l4.s4.annualise; square-root-of-time rule: Hull, Options, Futures and Other Derivatives, ch. 15.4 (252 trading days) |
| `screens[4].canvas` | canvas (console): {"lines": ["// returns.h", "#pragma once", "#include <vector>", "std::vector<double> simple… | correct | check l4.s4.annualise; check l4.s4.annualise; square-root-of-time rule: Hull, Options, Futures and Other Derivatives, ch. 15.4 (252 trading days) |
| `screens[4].widget.answer` | KEY: What does `annualise(0.01, 365)` return, to 4 decimal places? -> 0.191 (0.1910 (0.01 × √365 = 0.19105)) | correct | check l4.s4.annualise; check l4.s4.annualise; square-root-of-time rule: Hull, Options, Futures and Other Derivatives, ch. 15.4 (252 trading days) |
| `screens[4].widget.wrong[0]` | slip default = 0.1587: That is the default, 252. Passing 365 replaces it. | correct | check l4.s4.annualise; check l4.s4.annualise; square-root-of-time rule: Hull, Options, Futures and Other Derivatives, ch. 15.4 (252 trading days) |
| `screens[4].widget.wrong[1]` | slip sum = 3.65: You multiplied by 365. Annualising multiplies by the square root of the days. | correct | check l4.s4.annualise; check l4.s4.annualise; square-root-of-time rule: Hull, Options, Futures and Other Derivatives, ch. 15.4 (252 trading days) |
| `screens[4].hints[0]` | The second argument replaces the default. | correct | check l4.s4.annualise; check l4.s4.annualise; square-root-of-time rule: Hull, Options, Futures and Other Derivatives, ch. 15.4 (252 trading days) |
| `screens[4].hints[1]` | Line 11 computes `daily_vol * std::sqrt(days)`. | correct | check l4.s4.annualise; check l4.s4.annualise; square-root-of-time rule: Hull, Options, Futures and Other Derivatives, ch. 15.4 (252 trading days) |
| `screens[4].hints[2]` | $0.01 \times \sqrt{365} = 0.01 \times 19.105$. | correct | check l4.s4.annualise; check l4.s4.annualise; square-root-of-time rule: Hull, Options, Futures and Other Derivatives, ch. 15.4 (252 trading days) |
| `screens[4].feedback.correct` | 365 replaces 252: $0.01\sqrt{365} \approx 0.1910$. | correct | check l4.s4.annualise; check l4.s4.annualise; square-root-of-time rule: Hull, Options, Futures and Other Derivatives, ch. 15.4 (252 trading days) |
| `screens[4].explain.text` | A default fills in only when the call leaves that argument out. Here `days` is 365, so the result is $0.01 \t… | correct | check l4.s4.annualise; check l4.s4.annualise; square-root-of-time rule: Hull, Options, Futures and Other Derivatives, ch. 15.4 (252 trading days) |
| `screens[5].prose` | The header line is hidden above your code, as `#include "returns.h"` would paste it. Write the definition. `o… | correct | checks l4.s5.fb-test-2, l4.s5.fb-test-1, l4.s5.minus-one-bound |
| `screens[5].canvas` | canvas (console): {"lines": ["// returns.h", "#pragma once", "#include <vector>", "std::vector<double> simple… | correct | checks l4.s5.fb-test-2, l4.s5.fb-test-1, l4.s5.minus-one-bound |
| `screens[5].widget.solution` | code: Define `simple_returns(prices)`: each day's return after the first, `(today - yesterday) / yesterday`. … | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l4.s5.fb-test-2, l4.s5.fb-test-1, l4.s5.minus-one-bound |
| `screens[5].hints[0]` | Loop from index 1, as in `count_up_days`. | correct | checks l4.s5.fb-test-2, l4.s5.fb-test-1, l4.s5.minus-one-bound |
| `screens[5].hints[1]` | The signature must match the declaration on line 4 exactly. | correct | checks l4.s5.fb-test-2, l4.s5.fb-test-1, l4.s5.minus-one-bound |
| `screens[5].hints[2]` | `out.push_back((prices[i] - prices[i - 1]) / prices[i - 1]);` for `i` from 1 while `i < prices.size()`. | correct | checks l4.s5.fb-test-2, l4.s5.fb-test-1, l4.s5.minus-one-bound |
| `screens[5].feedback.correct` | n closes give n − 1 returns. | correct | checks l4.s5.fb-test-2, l4.s5.fb-test-1, l4.s5.minus-one-bound |
| `screens[5].feedback.byKey.test-2` | One close has no day before it, so the list must be empty. If the program stopped, your loop read `prices[i -… | imprecise | check l4.s5.fb-test-2: a loop from index 0 stops on test 1; check l4.s5.minus-one-bound: the size() - 1 loop stops on test 3, which has no line; finding 12 |
| `screens[5].feedback.byKey.test-1` | From 110 to 99 is (99 − 110) / 110 = −0.1. Divide by yesterday's close, not today's. | correct | checks l4.s5.fb-test-2, l4.s5.fb-test-1, l4.s5.minus-one-bound |
| `screens[5].feedback.byKey.compile` | If the error mentions a declaration, make your first line match `returns.h` exactly, including `const` and `&… | correct | checks l4.s5.fb-test-2, l4.s5.fb-test-1, l4.s5.minus-one-bound |
| `screens[5].explain.text` | Starting at index 1 gives each return a yesterday, so one close or none gives an empty list. Your definition … | correct | checks l4.s5.fb-test-2, l4.s5.fb-test-1, l4.s5.minus-one-bound |
| `screens[6].prose` | The hidden header declares `double annualise(double daily_vol, int days = 252);`. A default argument is writt… | correct | checks l4.s6.tests, l4.s6.fb-compile; Hull ch. 15.4 (252 trading days) |
| `screens[6].canvas` | canvas (console): {"lines": ["// returns.h", "#pragma once", "#include <vector>", "std::vector<double> simple… | correct | checks l4.s6.tests, l4.s6.fb-compile; Hull ch. 15.4 (252 trading days) |
| `screens[6].widget.solution` | code: Define `annualise`: the daily volatility times the square root of `days`. (6 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l4.s6.tests, l4.s6.fb-compile; Hull ch. 15.4 (252 trading days) |
| `screens[6].hints[0]` | `std::sqrt` from `<cmath>` takes a square root. | correct | checks l4.s6.tests, l4.s6.fb-compile; Hull ch. 15.4 (252 trading days) |
| `screens[6].hints[1]` | The default is already in the header on line 5. | correct | checks l4.s6.tests, l4.s6.fb-compile; Hull ch. 15.4 (252 trading days) |
| `screens[6].hints[2]` | `return daily_vol * std::sqrt(days);` and no `= 252` in your line. | correct | checks l4.s6.tests, l4.s6.fb-compile; Hull ch. 15.4 (252 trading days) |
| `screens[6].feedback.correct` | The header holds the default; the definition holds the body. | correct | checks l4.s6.tests, l4.s6.fb-compile; Hull ch. 15.4 (252 trading days) |
| `screens[6].feedback.byKey.compile` | If the message says `redefinition of default argument`, delete `= 252` from your definition: the default live… | correct | checks l4.s6.tests, l4.s6.fb-compile; Hull ch. 15.4 (252 trading days) |
| `screens[6].feedback.byKey.test-1` | `annualise(0.01)` should be 0.01 × √252 ≈ 0.1587. Multiply by the square root of `days`. | correct | checks l4.s6.tests, l4.s6.fb-compile; Hull ch. 15.4 (252 trading days) |
| `screens[6].explain.text` | Callers see only the header, so the default must be there for `annualise(0.01)` to compile in their files. Th… | correct | checks l4.s6.tests, l4.s6.fb-compile; Hull ch. 15.4 (252 trading days) |
| `screens[7].prose` | To save a file, someone puts a body in `returns.h`. Both `main.cpp` and `pricer.cpp` include it. ```cpp // re… | correct | check l4.s7.multiple-definition |
| `screens[7].canvas` | canvas (console): {"lines": ["$ g++ -std=c++17 main.cpp pricer.cpp -o backtest", "/usr/bin/ld: /tmp/ccg6pEss.… | correct | check l4.s7.multiple-definition |
| `screens[7].widget.options[0]` | KEY: The header has `#pragma once`. Why does the build still fail? -> Each `.cpp` file gets its own copy of t… | correct | check l4.s7.multiple-definition |
| `screens[7].widget.options[1]` | not: g++ ignores `#pragma once` / why: g++ honours it. It stops one `.cpp` file including the header twice, w… | correct | check l4.s7.multiple-definition |
| `screens[7].widget.options[2]` | not: The compiler should have caught it, so it is a compiler bug / why: Each file was compiled alone and look… | correct | check l4.s7.multiple-definition |
| `screens[7].widget.options[3]` | not: `simple_return` clashes with a standard library name / why: The message names `main.cpp` and `pricer.cpp… | correct | check l4.s7.multiple-definition |
| `screens[7].hints[0]` | `#pragma once` works within one `.cpp` file. | correct | check l4.s7.multiple-definition |
| `screens[7].hints[1]` | Line 3 names two object files, one from each `.cpp`. | correct | check l4.s7.multiple-definition |
| `screens[7].hints[2]` | Each `.cpp` pasted the header, body and all, so each object file defines `simple_return`. | correct | check l4.s7.multiple-definition |
| `screens[7].feedback.correct` | One body per program: in a `.cpp`, not a header. | correct | check l4.s7.multiple-definition |
| `screens[7].feedback.byKey.ignored` | You expected `#pragma once` to cover the whole program. It covers one `.cpp` at a time, and each of the two p… | correct | check l4.s7.multiple-definition |
| `screens[7].explain.text` | `#include` pastes the header into each `.cpp`, so `main.o` and `pricer.o` both contain the body. `#pragma onc… | correct | check l4.s7.multiple-definition |
| `screens[8].prose` | The pattern you used: ```cpp // returns.h: declarations, defaults, #pragma once double annualise(double daily… | correct | check l4.s8.default-in-definition |
| `screens[8].widget.options[0]` | KEY: A teammate adds `int days = 252` to the definition in `returns.cpp` only, and removes it from the header… | correct | check l4.s8.default-in-definition |
| `screens[8].widget.options[1]` | not: It still returns 0.158745 / why: `main.cpp` is compiled from the header alone. It never sees `returns.cp… | correct | check l4.s8.default-in-definition |
| `screens[8].widget.options[2]` | not: It compiles, and `days` is 0 / why: C++ never invents a value for a missing argument. Without a visible … | correct | check l4.s8.default-in-definition |
| `screens[8].widget.options[3]` | not: It compiles, but the linker fails / why: The problem appears earlier: the compiler rejects a call with t… | correct | check l4.s8.default-in-definition |
| `screens[8].hints[0]` | When `main.cpp` is compiled, which files does the compiler read? | correct | check l4.s8.default-in-definition |
| `screens[8].feedback.correct` | Callers see the header, so defaults go there. | correct | check l4.s8.default-in-definition |
| `screens[8].explain.text` | `main.cpp` is compiled with only the header's text, so it sees a function that needs two arguments. The call … | correct | check l4.s8.default-in-definition |
| `screens[9].prose` | A vendor sells a fast volatility library. You receive `fastvol.h` and `libfastvol.a`, a file of compiled obje… | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].canvas` | canvas (graph): {"directed": true, "height": 280, "nodes": [{"id": "h", "label": "fastvol.h", "x": 0.1, "y": … | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].widget.options[0]` | KEY: What does each file do in your build? -> The header lets your code compile; the `.a` is joined in by the… | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].widget.options[1]` | not: You compile `libfastvol.a` with g++ first / why: It is already compiled object code. There is nothing le… | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].widget.options[2]` | not: The header is enough; the `.a` is optional / why: The header holds only declarations. Without the `.a`, … | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].widget.options[3]` | not: You `#include` both files / why: `#include` pastes text. The `.a` is machine code, so it goes to the lin… | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].hints[0]` | Which file holds declarations, and which holds compiled bodies? | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].hints[1]` | Follow each file's arrow. | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].hints[2]` | Headers feed the compiler; compiled bodies feed the linker. | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].feedback.correct` | Declarations to the compiler, compiled code to the linker. | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].feedback.byKey.hdr` | The header only promises the functions exist. Without the `.a`, the linker cannot find their bodies: `undefin… | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `screens[9].explain.text` | A library ships declarations in a header and bodies already compiled. A `.a` is joined in at link time; a `.s… | correct | GNU ld manual: static archives (.a) are linked in, shared objects (.so) are loaded by the dynamic loader at start; check l4.q2.undefined-reference |
| `quiz[0].prose` | Two functions share a name: an **overload**. The compiler picks one by the argument types. ```cpp double mid(… | correct | check l4.q0.overload |
| `quiz[0].widget.options[0]` | KEY: What does it print? -> `10001 100.015` | correct | check l4.q0.overload |
| `quiz[0].widget.options[1]` | not: `10001.5 100.015` / why: `10001LL` and `10002LL` are `long long`, so the `long long` version runs, and i… | correct | check l4.q0.overload |
| `quiz[0].widget.options[2]` | not: Nothing: two functions cannot share a name / why: That is true in Python, where the second `def` replace… | correct | check l4.q0.overload |
| `quiz[0].widget.options[3]` | not: `10001 100` / why: The `double` version runs for `100.01` and `100.02`, so the result keeps its fraction… | correct | check l4.q0.overload |
| `quiz[0].feedback.correct` | Ticks in `long long`, prices in `double`. | correct | check l4.q0.overload |
| `quiz[0].explain.text` | `mid(10001LL, 10002LL)` matches the `long long` version: 20003 / 2 is 10001 in integer division. `mid(100.01,… | correct | check l4.q0.overload |
| `quiz[1].prose` | ```cpp double risk_free_rate() { return 0.04; } ``` | correct | checks l4.q1.no-brackets, l4.q1.void-call, l4.q1.extra-arg |
| `quiz[1].widget.options[0]` | KEY: Which line prints 0.04? -> `std::cout << risk_free_rate() << '\n';` | correct | checks l4.q1.no-brackets, l4.q1.void-call, l4.q1.extra-arg |
| `quiz[1].widget.options[1]` | not: `std::cout << risk_free_rate << '\n';` / why: Without `()` you name the function without calling it. It … | correct | checks l4.q1.no-brackets, l4.q1.void-call, l4.q1.extra-arg |
| `quiz[1].widget.options[2]` | not: `std::cout << risk_free_rate(void) << '\n';` / why: `void` can appear in a declaration's empty list, but… | correct | checks l4.q1.no-brackets, l4.q1.void-call, l4.q1.extra-arg |
| `quiz[1].widget.options[3]` | not: `std::cout << risk_free_rate(0) << '\n';` / why: The function takes no arguments, so passing one is a co… | correct | checks l4.q1.no-brackets, l4.q1.void-call, l4.q1.extra-arg |
| `quiz[1].feedback.correct` | Empty brackets call a function with no parameters. | correct | checks l4.q1.no-brackets, l4.q1.void-call, l4.q1.extra-arg |
| `quiz[1].explain.text` | A function with no parameters is still called with `()`. Without them you refer to the function itself rather… | correct | checks l4.q1.no-brackets, l4.q1.void-call, l4.q1.extra-arg |
| `quiz[2].prose` | ```text $ g++ -std=c++17 main.cpp -o backtest /usr/bin/ld: /tmp/ccR5tWb1.o: in function `main': main.cpp:(.te… | correct | check l4.q2.undefined-reference |
| `quiz[2].widget.options[0]` | KEY: What is wrong? -> `returns.cpp` is missing from the command, so no body was linked | correct | check l4.q2.undefined-reference |
| `quiz[2].widget.options[1]` | not: `main.cpp` forgot `#include "returns.h"` / why: Then the compiler would have stopped with `not declared`… | correct | check l4.q2.undefined-reference |
| `quiz[2].widget.options[2]` | not: `annualise` is misspelt in `main.cpp` / why: A misspelt call would fail to compile. The linker is lookin… | correct | check l4.q2.undefined-reference |
| `quiz[2].widget.options[3]` | not: The default argument is missing / why: The message names `annualise(double, int)`, so the call compiled … | correct | check l4.q2.undefined-reference |
| `quiz[2].feedback.correct` | Declared, called, never defined in the build. | correct | check l4.q2.undefined-reference |
| `quiz[2].explain.text` | `ld` is the linker. `main.o` calls `annualise`, but no object file in this build defines it. Add `returns.cpp… | correct | check l4.q2.undefined-reference |
| `quiz[3].prose` | `simple_returns` from this lesson is called with one close: `simple_returns({101.5})`. | correct | solution run (widget l4 screens.5, test 2: one close gives []) |
| `quiz[3].widget.answer` | KEY: How many returns does it give back? -> 0 (0) | correct | solution run (widget l4 screens.5, test 2: one close gives []) |
| `quiz[3].widget.wrong[0]` | slip one = 1: A return compares two closes. With one close there is no yesterday, so the list is empty. | correct | solution run (widget l4 screens.5, test 2: one close gives []) |
| `quiz[3].feedback.correct` | No day before it, so no return. | correct | solution run (widget l4 screens.5, test 2: one close gives []) |
| `quiz[3].explain.text` | n closes give n − 1 returns, so one close gives none. The loop from index 1 never runs. | correct | solution run (widget l4 screens.5, test 2: one close gives []) |
| `summary.ideas[0]` | A name must be declared before it is used. A declaration gives the types and ends in `;`; a definition adds t… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | A header holds declarations and defaults; each `.cpp` compiles alone, and the linker joins the object files. | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | One definition per program for an ordinary function: a body in a header included by two `.cpp` files is a lin… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \texttt{main.cpp} \to \texttt{main.o},\quad \texttt{returns.cpp} \to \texttt{returns.o},\quad \text{link} \to… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | `#pragma once` stops one file including a header twice; it does not stop two `.cpp` files each getting a body. | correct | restates the lesson: see the rows of the screens it summarises |

## l5-value-or-reference.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | In Python, a function that appends to the list you pass changes your list, as the session above shows. Here i… | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[0].canvas` | canvas (console): {"lines": [">>> def add_fee(costs):", "... costs.append(1.50)", ">>> mine = [250.00, 120.00… | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[0].widget.options[0]` | KEY: What does the C++ program print? -> `2` | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[0].widget.options[1]` | not: `3` / why: You read it as Python, where the call shares the list. In C++ `costs` is a new vector, copied… | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[0].widget.options[2]` | not: `0` / why: `costs` starts as a full copy of `mine`, and nothing ever empties `mine`. | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[0].widget.options[3]` | not: It does not compile / why: It compiles. A parameter of type `std::vector<double>` simply receives a copy… | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[0].hints[0]` | Is `costs` the caller's vector, or a vector of its own? | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[0].hints[1]` | Look at the parameter type. It has no `&` or anything else after the type. | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[0].hints[2]` | `costs` is built as a copy of `mine`. `push_back` grows the copy, which is destroyed at the closing brace. `m… | imprecise | checks l5.s0.param-lifetime(-desk): the copy is destroyed at the end of the calling full-expression on this build and on g++ and clang; ISO C++17 (N4659) [expr.call]/4 leaves the choice to the implementation; finding 5 |
| `screens[0].feedback.correct` | The copy grew; `mine` did not. | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[0].feedback.byKey.three` | You read it as Python, where the call shares the list. In C++ `costs` is a new vector, copied from `mine`. | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[0].explain.text` | `costs` is a separate vector, copied from `mine` when the call starts. `push_back` grows that copy, and the c… | imprecise | checks l5.s0.param-lifetime(-desk): the copy is destroyed at the end of the calling full-expression on this build and on g++ and clang; ISO C++17 (N4659) [expr.call]/4 leaves the choice to the implementation; finding 5 |
| `screens[0].explain.canvas.lines` | explain canvas: ["main: mine = {250.00, 120.00}", "add_fee: costs = {250.00, 120.00, 1.50} (a copy)", "after … | correct | checks l5.s0.copy, l5.s0.param-lifetime, l5.s0.param-lifetime-desk |
| `screens[1].prose` | In C++ a variable *is* its object: a box in memory. Adding `&` to the type makes a second name for a box that… | correct | check l5.s1.alias |
| `screens[1].canvas` | canvas (boxes): {"itemKind": "card", "containers": [{"id": "names", "label": "Names", "kind": "box", "items":… | correct | check l5.s1.alias |
| `screens[1].widget.answer` | KEY: {"big": ["mine", "alias"], "small": ["copy"]} | correct | check l5.s1.alias |
| `screens[1].hints[0]` | Which line builds a second vector? The other names share the first one. | correct | check l5.s1.alias |
| `screens[1].hints[1]` | `copy` has no `&`, so it is a new box. | correct | check l5.s1.alias |
| `screens[1].hints[2]` | `mine` and `alias` name the box that `push_back` grew. `copy` names its own box, still `{250, 120}`. | correct | check l5.s1.alias |
| `screens[1].feedback.correct` | `mine` and `alias` name one box; `copy` is its own. | correct | check l5.s1.alias |
| `screens[1].feedback.byKey.mine` | `mine` is the box the vector was built in, and the `push_back` through `alias` grew it. | correct | check l5.s1.alias |
| `screens[1].feedback.byKey.alias` | `alias` was declared with `&`, so it names the box `mine` already names. No new vector is made. | correct | check l5.s1.alias |
| `screens[1].feedback.byKey.copy` | `copy` has no `&`, so it is a new box, filled with `mine`'s two prices before the push. | correct | check l5.s1.alias |
| `screens[1].explain.text` | `alias` is a second name for `mine`'s box, so pushing through `alias` grew that box. `copy` is its own box, c… | correct | check l5.s1.alias |
| `screens[2].prose` | A name declared with `&` is a **reference**: another name for an object that already exists. A reference para… | correct | check l5.s2.ref |
| `screens[2].canvas` | canvas (graph): {"height": 240, "nodeRadius": 20, "nodes": [{"id": "cash", "label": "cash", "x": 0.12, "y": 0… | correct | check l5.s2.ref |
| `screens[2].widget.options[0]` | KEY: What does it print? -> `997.5` | correct | check l5.s2.ref |
| `screens[2].widget.options[1]` | not: `1000` / why: That is what happens without the `&`. Here `balance` is another name for `cash`, so `balan… | correct | check l5.s2.ref |
| `screens[2].widget.options[2]` | not: `2.5` / why: `balance -= fee` subtracts the fee from the balance. It does not replace the balance with t… | correct | check l5.s2.ref |
| `screens[2].widget.options[3]` | not: `997.50` / why: The value is right, but `std::cout` prints a `double` without trailing zeros unless you … | correct | check l5.s2.ref |
| `screens[2].hints[0]` | Is `balance` a copy of `cash`, or another name for it? | correct | check l5.s2.ref |
| `screens[2].hints[1]` | Both `cash` and `balance` point at the same box. | correct | check l5.s2.ref |
| `screens[2].hints[2]` | `balance -= fee` changes the one `double` that both names share: 1000 minus 2.5 is 997.5. | correct | check l5.s2.ref |
| `screens[2].feedback.correct` | `balance` is `cash` under another name. | correct | check l5.s2.ref |
| `screens[2].feedback.byKey.unchanged` | That is what happens without the `&`. Here `balance` is another name for `cash`, so `cash` changes. | correct | check l5.s2.ref |
| `screens[2].explain.text` | `balance` is a reference, so it names the same `double` as `cash`. Subtracting 2.50 through `balance` changes… | correct | check l5.s2.ref |
| `screens[3].prose` | `prices` holds 1,000,000 prices, and `mean` only reads them. We want `v` to be a second name for `prices`, an… | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].canvas` | canvas (graph): {"height": 220, "nodeRadius": 20, "nodes": [{"id": "prices", "label": "prices", "x": 0.15, "y… | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].widget.options[0]` | KEY: Which signature should `mean` have? -> `double mean(const std::vector<double>& v)` | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].widget.options[1]` | not: `double mean(std::vector<double> v)` / why: That builds a second box and copies all 1,000,000 prices int… | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].widget.options[2]` | not: `double mean(std::vector<double>& v)` / why: That shares the box, but it lets `mean` change the prices, … | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].widget.options[3]` | not: `double mean(const std::vector<double> v)` / why: `const` stops changes, but without `&` this is still a… | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].hints[0]` | Two things are needed: no copy, and no changes. | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].hints[1]` | `&` gives the sharing. What gives the read only part? | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].hints[2]` | `const std::vector<double>&` is a reference, so nothing is copied, and `const` makes `v` read only. | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].feedback.correct` | Shared and read only. | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].feedback.byKey.value` | That copies all 1,000,000 prices into `v` on every call. | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].feedback.byKey.cvalue` | Without `&` this is still a copy, even if it is a read-only one. | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[3].explain.text` | `const std::vector<double>& v` makes `v` a second name for `prices`, so nothing is copied. `const` means the … | correct | ISO C++17 (N4659) [dcl.ref], [dcl.init.ref]; a by-value parameter copies (check l5.s0.copy) |
| `screens[4].prose` | A `double` takes 8 bytes. Passing a vector by value copies every element into a new buffer. The table shows t… | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[4].canvas` | canvas (table): {"columns": ["Prices", "Bytes copied", "Time per by-value call"], "rows": [["1,000", "8,000",… | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[4].widget.answer` | KEY: How many megabytes does one by-value call copy for 1,000,000 prices? Take 1 MB as 1,000,000 bytes. -> 8 … | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[4].widget.wrong[0]` | slip bytes = 8000000: That is the count in bytes. Divide by 1,000,000 to get megabytes. | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[4].widget.wrong[1]` | slip one = 1: That counts one byte per price. A `double` takes 8. | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[4].widget.wrong[2]` | slip bits = 64: You multiplied by 64, the bits in a `double`. Count bytes: 8 each. | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[4].hints[0]` | Each price is 8 bytes. How many bytes is a million of them? | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[4].hints[1]` | Follow the column: each row multiplies the number of prices by 8. | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[4].hints[2]` | 1,000,000 times 8 bytes is 8,000,000 bytes, which is 8 MB. | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[4].feedback.correct` | 8 MB on every call. | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[4].explain.text` | Each of the 1,000,000 prices takes 8 bytes, so a by-value call copies 8,000,000 bytes, which is 8 MB. Here th… | correct | checks l5.s4.timings, l5.s4.mb; check l5.s4.timings (node, same compiler): 0.1 to 0.3, 1.7 to 3.4, 35 to 43, 1170 to 1520 microseconds over two runs |
| `screens[5].prose` | A book holds share quantities and their prices in £, one entry per stock. Its value is the sum of quantity ti… | correct | check l5.s5.book |
| `screens[5].canvas` | canvas (console): {"lines": ["qty = {100, 250, 40}", "px = {4.85, 0.72, 31.20}", "", "100 x 4.85 = 485.00", "… | correct | check l5.s5.book |
| `screens[5].widget.solution` | code: Write `double total_value(...)` with both vectors passed by `const` reference. (5 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; check l5.s5.book |
| `screens[5].hints[0]` | Start with the signature: two `const std::vector<double>&` parameters, returning `double`. | correct | check l5.s5.book |
| `screens[5].hints[1]` | Loop over the indices with `std::size_t i` from 0 to `qty.size()`. | correct | check l5.s5.book |
| `screens[5].hints[2]` | Set `double total = 0;`, add `qty[i] * px[i]` for each `i`, then `return total;`. An empty book returns 0. | correct | check l5.s5.book |
| `screens[5].feedback.correct` | Both vectors are read in place; nothing is copied. | correct | check l5.s5.book |
| `screens[5].explain.text` | `const std::vector<double>&` hands the function the caller's vectors without copying them. The loop only read… | correct | check l5.s5.book |
| `screens[6].prose` | A colleague wants weights that add up to 1. Their function works on its own copy without anyone noticing. ```… | correct | check l5.s6.normalise |
| `screens[6].canvas` | canvas (graph): {"height": 220, "nodeRadius": 20, "nodes": [{"id": "cw", "label": "caller's w", "x": 0.2, "y"… | correct | check l5.s6.normalise |
| `screens[6].widget.options[0]` | KEY: What does it print? -> `2` | correct | check l5.s6.normalise |
| `screens[6].widget.options[1]` | not: `0.2` / why: You assumed the call changes the caller's vector. Without `&`, `normalise` divides its own … | correct | check l5.s6.normalise |
| `screens[6].widget.options[2]` | not: It does not compile / why: It compiles cleanly. Taking a vector by value is legal; it just copies. | correct | check l5.s6.normalise |
| `screens[6].widget.options[3]` | not: `1` / why: `w[0]` is the first weight, 2, and nothing changed it in the caller. | correct | check l5.s6.normalise |
| `screens[6].hints[0]` | Which box does `x /= sum` divide? | correct | check l5.s6.normalise |
| `screens[6].hints[1]` | `normalise`'s `w` is a separate box. | correct | check l5.s6.normalise |
| `screens[6].hints[2]` | The parameter has no `&`, so the division happens in the copy. The caller's `w[0]` is still 2. | correct | check l5.s6.normalise |
| `screens[6].feedback.correct` | The copy was normalised; the caller's weights were not. | correct | check l5.s6.normalise |
| `screens[6].feedback.byKey.fifth` | You assumed the call changes the caller's vector. Without `&`, `normalise` divides its own copy, which is the… | correct | check l5.s6.normalise |
| `screens[6].explain.text` | `normalise` divided its own copy, `{0.2, 0.3, 0.5}`, and that copy died at the closing brace. The caller's `w… | imprecise | checks l5.s0.param-lifetime(-desk): the copy is destroyed at the end of the calling full-expression on this build and on g++ and clang; ISO C++17 (N4659) [expr.call]/4 leaves the choice to the implementation; finding 5 |
| `screens[7].prose` | Fix `normalise` so it changes the caller's weights. Weights may be negative (a short position). If the weight… | correct | check l5.s7.nan |
| `screens[7].widget.solution` | code: Fix `normalise`. (6 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; check l5.s7.nan |
| `screens[7].hints[0]` | Two fixes: the parameter type, and the case where the sum is 0. | correct | check l5.s7.nan |
| `screens[7].hints[1]` | Add `&` after the type so `w` names the caller's vector. | correct | check l5.s7.nan |
| `screens[7].hints[2]` | Write `std::vector<double>& w`. After summing, `if (sum == 0) return;` before dividing. | correct | check l5.s7.nan |
| `screens[7].feedback.correct` | The caller's weights now add up to 1. | correct | check l5.s7.nan |
| `screens[7].explain.text` | With `std::vector<double>& w`, every `x /= sum` divides the caller's own weights. The early `return` avoids d… | correct | check l5.s7.nan |
| `screens[8].prose` | Each parameter type says what the function will do with your object. ```cpp void f(std::vector<double> v); //… | correct | check l5.q2.return-no-copy; ISO C++17 (N4659) [class.copy.elision]; [dcl.init.ref]/5 (a plain reference rejects temporaries and const objects, checks l6.s2.*) |
| `screens[8].widget.options[0]` | KEY: A function reads 1,000,000 prices and returns their mean. Which parameter fits? -> `const std::vector<do… | correct | check l5.q2.return-no-copy; ISO C++17 (N4659) [class.copy.elision]; [dcl.init.ref]/5 (a plain reference rejects temporaries and const objects, checks l6.s2.*) |
| `screens[8].widget.options[1]` | not: `std::vector<double> prices` / why: That copies 8 MB on every call, only to read it. | correct | check l5.q2.return-no-copy; ISO C++17 (N4659) [class.copy.elision]; [dcl.init.ref]/5 (a plain reference rejects temporaries and const objects, checks l6.s2.*) |
| `screens[8].widget.options[2]` | not: `std::vector<double>& prices` / why: That compiles, but it claims the function may change the prices, an… | correct | check l5.q2.return-no-copy; ISO C++17 (N4659) [class.copy.elision]; [dcl.init.ref]/5 (a plain reference rejects temporaries and const objects, checks l6.s2.*) |
| `screens[8].feedback.correct` | Read only, and no copy. | correct | check l5.q2.return-no-copy; ISO C++17 (N4659) [class.copy.elision]; [dcl.init.ref]/5 (a plain reference rejects temporaries and const objects, checks l6.s2.*) |
| `screens[8].explain.text` | A function that only reads a large object takes it by `const&`. Small values such as `double` and `int` go by… | correct | check l5.q2.return-no-copy; ISO C++17 (N4659) [class.copy.elision]; [dcl.init.ref]/5 (a plain reference rejects temporaries and const objects, checks l6.s2.*) |
| `screens[9].prose` | Two reference parameters let one function change two of the caller's variables. Here `a` and `b` are the call… | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[9].widget.options[0]` | KEY: Which line completes `swap_px`? -> `a = b;` | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[9].widget.options[1]` | not: `b = a;` / why: That copies `a` into `b`, so the old `b` is lost and both end up as the old `a`. | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[9].widget.options[2]` | not: `t = b;` / why: `t` holds the old `a`. Overwriting it loses that value, and `a` never changes. | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[9].widget.options[3]` | not: `a = t;` / why: `t` is a copy of `a`, so this writes `a` back into itself and changes nothing. | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[9].hints[0]` | After the first line, `t` keeps the old `a`. What should `a` become? | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[9].hints[1]` | Each line has one job: save `a`, then overwrite `a`, then fill `b`. | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[9].hints[2]` | `a` should take `b`'s value, which is safe because `t` saved the old `a`. Then `b = t` finishes the swap. | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[9].feedback.correct` | Save, overwrite, fill. | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[9].feedback.byKey.ba` | That copies `a` into `b` before `b` is saved, so the old `b` is lost. | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[9].explain.text` | Line 1 saves the old `a` in `t`. Line 2 overwrites `a` with `b`, which is safe because `t` holds the old valu… | correct | derivation: t = a; a = b; b = t swaps; the three other lines traced by hand |
| `screens[10].prose` | A risk engine revalues a desk 1,000 times a second. The order book has 50,000 price levels and is only read. … | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].widget.options[0]` | KEY: Which signature should `revalue` have? -> `void revalue(const OrderBook& book, std::vector<Position>& po… | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].widget.options[1]` | not: `void revalue(OrderBook book, std::vector<Position> pos)` / why: That copies the whole book 1,000 times … | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].widget.options[2]` | not: `void revalue(OrderBook& book, const std::vector<Position>& pos)` / why: The `const` is on the wrong arg… | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].widget.options[3]` | not: `void revalue(const OrderBook book, std::vector<Position>& pos)` / why: The positions are right, but `co… | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].hints[0]` | Ask two questions per argument: is it large, and does the function change it? | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].hints[1]` | The book is large and read only. The positions are changed and must reach the caller. | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].hints[2]` | Book: `const OrderBook&`. Positions: `std::vector<Position>&`. | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].feedback.correct` | Read the book in place; change the positions in place. | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].feedback.byKey.copies` | Both arguments are copied, so the P&L updates are lost. | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].feedback.byKey.swapped` | The `const` belongs on the book, which is only read. | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `screens[10].explain.text` | The book is large and only read, so `const OrderBook&` shares it at no cost. The positions must change for th… | correct | derivation from checks l5.s0.copy and l6.s1.px (a copy loses updates; const forbids writes) |
| `quiz[0].prose` | ```cpp int x = 5; int& r = x; int& r2 = r; r2 = 9; std::cout << x << "\n"; ``` | correct | check l5.q0.ref-ref |
| `quiz[0].widget.options[0]` | KEY: What does it print? -> `9` | correct | check l5.q0.ref-ref |
| `quiz[0].widget.options[1]` | not: `5` / why: You read `r2` as a copy of `r`. A reference made from a reference names the same object, `x`. | correct | check l5.q0.ref-ref |
| `quiz[0].widget.options[2]` | not: It does not compile / why: `int& r2 = r;` is fine: `r` is just another name for `x`, so `r2` is a third … | correct | check l5.q0.ref-ref |
| `quiz[0].feedback.correct` | Three names, one `int`. | correct | check l5.q0.ref-ref |
| `quiz[0].explain.text` | `r` names `x`, so `int& r2 = r;` makes `r2` name `x` too. There is no reference to a reference: `r2 = 9` writ… | correct | check l5.q0.ref-ref |
| `quiz[1].prose` | ```cpp void apply_fee(double& balance, double fee) { balance -= fee; } int main() { apply_fee(100.0, 2.50); }… | correct | check l5.q1.temporary |
| `quiz[1].widget.options[0]` | KEY: What happens when you build this? -> It does not compile: a plain `double&` cannot bind to the temporary… | correct | check l5.q1.temporary |
| `quiz[1].widget.options[1]` | not: It prints nothing and runs / why: A non-const reference must name a real variable. `100.0` is a temporar… | correct | check l5.q1.temporary |
| `quiz[1].widget.options[2]` | not: It compiles and changes a hidden copy / why: C++ will not make a hidden copy for a plain `&`. That is ex… | correct | check l5.q1.temporary |
| `quiz[1].feedback.correct` | A plain reference needs a variable to change. | correct | check l5.q1.temporary |
| `quiz[1].explain.text` | `apply_fee` promises to change its first argument, so the argument must be a variable. clang says "expects an… | correct | check l5.q1.temporary |
| `quiz[2].prose` | ```cpp std::vector<double> make_prices(int n) { std::vector<double> v(n, 100.0); return v; } std::vector<doub… | correct | check l5.q2.return-no-copy |
| `quiz[2].widget.options[0]` | KEY: How many times are the 1,000,000 prices copied when `make_prices` returns? -> None: the vector is built … | correct | check l5.q2.return-no-copy |
| `quiz[2].widget.options[1]` | not: Once, from `v` into `px` / why: That was the worry before copy elision. The compiler builds `v` in `px`,… | correct | check l5.q2.return-no-copy |
| `quiz[2].widget.options[2]` | not: Twice, into a temporary and then into `px` / why: The compiler removes both copies. A returned local vec… | correct | check l5.q2.return-no-copy |
| `quiz[2].feedback.correct` | Return by value freely. | correct | check l5.q2.return-no-copy |
| `quiz[2].explain.text` | The compiler usually builds `v` in the caller's `px` from the start; when it does not, it moves `v`. Either w… | correct | check l5.q2.return-no-copy |
| `quiz[3].widget.options[0]` | KEY: Which C++ parameter behaves like Python's `def add(costs): costs.append(1.5)`? -> `std::vector<double>& … | correct | checks l5.s0.copy, l5.s1.alias, r2.i1.push |
| `quiz[3].widget.options[1]` | not: `std::vector<double> costs` / why: That is C++'s default, a copy. Python's call shares the caller's list. | correct | checks l5.s0.copy, l5.s1.alias, r2.i1.push |
| `quiz[3].widget.options[2]` | not: `const std::vector<double>& costs` / why: It shares, but `const` forbids `push_back`, so the append woul… | correct | checks l5.s0.copy, l5.s1.alias, r2.i1.push |
| `quiz[3].feedback.correct` | A plain reference shares and allows changes, as Python does. | correct | checks l5.s0.copy, l5.s1.alias, r2.i1.push |
| `quiz[3].explain.text` | A Python call shares the caller's list and may change it. In C++ that needs `&` without `const`. Without the … | correct | checks l5.s0.copy, l5.s1.alias, r2.i1.push |
| `summary.ideas[0]` | A C++ variable is its object. Passing by value gives the function its own copy; `T&` passes a second name for… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | `const T&` shares without copying and promises not to change; it also accepts temporaries such as `{1.0, 2.0}… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | Return results by value: the compiler builds them in the caller's variable, so a returned vector is not copie… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \texttt{T} \to \text{copy}, \qquad \texttt{const T\&} \to \text{read}, \qquad \texttt{T\&} \to \text{change} … | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | Forgetting `&` compiles cleanly: the function changes its own copy and the caller sees nothing. | correct | restates the lesson: see the rows of the screens it summarises |

## l6-const.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A tick is the smallest price step an exchange allows. In Python a name can always be pointed at a new value. … | correct | check l6.s0.const-assign |
| `screens[0].canvas` | canvas (console): {"lines": ["int main() {", " const double tick = 0.01;", " tick = 0.05;", "}"], "title": "m… | correct | check l6.s0.const-assign |
| `screens[0].widget.options[0]` | KEY: What happens when you build `main.cpp`? -> The compiler rejects line 3 | correct | check l6.s0.const-assign |
| `screens[0].widget.options[1]` | not: It builds, and `tick` ends as 0.05 / why: That is the Python habit of rebinding a name. `const` forbids … | correct | check l6.s0.const-assign |
| `screens[0].widget.options[2]` | not: It builds, and line 3 is ignored, so `tick` stays 0.01 / why: C++ never ignores a line silently. Breakin… | correct | check l6.s0.const-assign |
| `screens[0].widget.options[3]` | not: It builds, then stops with an error when line 3 runs / why: `const` is checked by the compiler, before t… | correct | check l6.s0.const-assign |
| `screens[0].hints[0]` | When is `const` checked: while compiling, or while running? | correct | check l6.s0.const-assign |
| `screens[0].hints[1]` | Line 3 assigns to `tick`, which line 2 declared `const`. | correct | check l6.s0.const-assign |
| `screens[0].hints[2]` | The compiler checks every assignment against the type. `const double` cannot be assigned, so the build fails … | correct | check l6.s0.const-assign |
| `screens[0].feedback.correct` | The build stops at line 3. | correct | check l6.s0.const-assign |
| `screens[0].feedback.byKey.five` | That is the Python habit of rebinding a name. `const` forbids any assignment after the declaration. | correct | check l6.s0.const-assign |
| `screens[0].explain.text` | The compiler checks every assignment against the variable's type. `tick` is a `const double`, so line 3 is a … | correct | check l6.s0.const-assign |
| `screens[0].explain.canvas.lines` | explain canvas: ["main.cpp:3:10: error: cannot assign to variable 'tick'", " with const-qualified type 'const… | correct | check l6.s0.const-assign |
| `screens[1].prose` | `const double& px` makes `px` a read-only name for the caller's price. The other parameter, `fee`, is a plain… | correct | check l6.s1.px |
| `screens[1].canvas` | canvas (console): {"lines": ["double with_fee(const double& px, double fee) {", " double out = px;", " out +=… | correct | check l6.s1.px |
| `screens[1].widget.answer` | KEY: Tap every line the compiler rejects. -> ["l4"] | correct | check l6.s1.px |
| `screens[1].widget.wrong[0]` | slip set fee-too = ["l4", "l5"]: `fee` has no `const`: it is the function's own copy, so `fee = 0` is allowed… | correct | check l6.s1.px |
| `screens[1].widget.wrong[1]` | slip set copy = ["l3", "l4"]: `out` is a new `double` copied from `px`. Changing the copy is fine; only line … | correct | check l6.s1.px |
| `screens[1].hints[0]` | Which lines assign to something? Of those, which name is `const`? | correct | check l6.s1.px |
| `screens[1].hints[1]` | Only `px` carries `const`. `out` is a new local copy. | correct | check l6.s1.px |
| `screens[1].hints[2]` | Line 4 writes through `px`, which is read only. Lines 3 and 5 change `out` and `fee`, which are ordinary copi… | correct | check l6.s1.px |
| `screens[1].feedback.correct` | Only line 4 writes through the `const` name. | correct | check l6.s1.px |
| `screens[1].feedback.byKey.l2` | Line 2 reads `px` to copy it. Reading is what `const` allows. | correct | check l6.s1.px |
| `screens[1].feedback.byKey.l5` | `fee` has no `const`, so line 5 is allowed. | correct | check l6.s1.px |
| `screens[1].explain.text` | Line 4 is the only write through `px`. Clang says "cannot assign to variable 'px' with const-qualified type '… | correct | check l6.s1.px |
| `screens[2].prose` | A `const` reference parameter is a **const reference**: the function may read the caller's object but never c… | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].canvas` | canvas (console): {"lines": ["double mean(std::vector<double>& v);", "", "std::vector<double> prices{101.5, 9… | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].widget.options[0]` | KEY: With this plain `std::vector<double>&`, which calls compile? -> Only `mean(prices)` | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].widget.options[1]` | not: All three / why: A plain reference may change its object. So the compiler refuses a temporary, which has… | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].widget.options[2]` | not: `mean(prices)` and `mean(fixed)` / why: `fixed` is `const`. Binding a plain reference to it would let `m… | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].widget.options[3]` | not: `mean(prices)` and `mean({101.5, 99.0})` / why: `{101.5, 99.0}` is a temporary. A plain reference must n… | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].hints[0]` | A plain reference says the function might change the argument. Which arguments must not be changed, or cannot… | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].hints[1]` | `fixed` is `const`, and `{101.5, 99.0}` is a temporary with no name. | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].hints[2]` | Only `prices` is a non-const variable. Adding `const` to the parameter makes all three calls compile. | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].feedback.correct` | Only a non-const variable binds to a plain reference. | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].feedback.byKey.all` | A plain reference may change its object, so it refuses the temporary and the `const` vector. | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].explain.text` | A plain reference may change its argument, so it accepts only a non-const variable. With `const std::vector<d… | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[2].explain.canvas.lines` | explain canvas: ["double mean(const std::vector<double>& v);", "", "std::vector<double> prices{101.5, 99.0};"… | correct | checks l6.s2.prices, l6.s2.temporary, l6.s2.fixed, l6.s2.const-ref |
| `screens[3].prose` | `const` after a method's parameter list promises the method does not change the object. A `const` object may … | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].canvas` | canvas (console): {"lines": ["struct Quote {", " double bid, ask;", " double mid() const { return (bid + ask)… | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].widget.options[0]` | KEY: Select all that apply: which lines compile? -> `double m = q.mid();` | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].widget.options[1]` | KEY: Select all that apply: which lines compile? -> `double b = q.bid;` | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].widget.options[2]` | not: `q.widen(0.01);` / why: `widen` is not marked `const`, so a `const Quote` cannot call it. clang: "functi… | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].widget.options[3]` | not: `q.ask = 100.05;` / why: `q` is `const`, so every member is read only, and assigning to `q.ask` is an er… | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].hints[0]` | Reading is always allowed. Which lines would change `q`? | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].hints[1]` | Line 3 has `const` after `()`; line 4 does not. | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].hints[2]` | `mid()` is a `const` method and reading `q.bid` is fine. `widen` and the assignment would change `q`, so both… | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].feedback.correct` | A `const` object reads and calls `const` methods only. | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].feedback.byKey.widen` | `widen` is not marked `const`, so a `const Quote` cannot call it, even before it runs. | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[3].explain.text` | `q.mid()` compiles because `mid` is marked `const`, and reading `q.bid` is always fine. `q.widen(0.01)` fails… | correct | checks l6.s3.ok, l6.s3.widen, l6.s3.ask |
| `screens[4].prose` | The data in `Quote` is private: read it through the `const` getters `bid()` and `ask()`. The starter breaks t… | correct | widget run: solution passes, starter does not compile (private members, non-const parameter); checks l6.s2.* |
| `screens[4].canvas` | canvas (console): {"lines": ["class Quote {", "public:", " Quote(double bid, double ask);", " double bid() co… | correct | widget run: solution passes, starter does not compile (private members, non-const parameter); checks l6.s2.* |
| `screens[4].widget.solution` | code: Fix `spread(q)`: the ask minus the bid, for any `Quote`, including a `const` one or a temporary. (5 hid… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; widget run: solution passes, starter does not compile (private members, non-const parameter); checks l6.s2.* |
| `screens[4].hints[0]` | Two fixes: the parameter type, and how the prices are read. | correct | widget run: solution passes, starter does not compile (private members, non-const parameter); checks l6.s2.* |
| `screens[4].hints[1]` | `bid_` and `ask_` are private. The getters are `bid()` and `ask()`, with brackets. | correct | widget run: solution passes, starter does not compile (private members, non-const parameter); checks l6.s2.* |
| `screens[4].hints[2]` | Write `double spread(const Quote& q) { return q.ask() - q.bid(); }`. The getters are `const`, so a `const Quo… | correct | widget run: solution passes, starter does not compile (private members, non-const parameter); checks l6.s2.* |
| `screens[4].feedback.correct` | Read only, and it accepts any `Quote`. | correct | widget run: solution passes, starter does not compile (private members, non-const parameter); checks l6.s2.* |
| `screens[4].feedback.byKey.compile` | Read the compiler's first error. Private members are reached through `q.ask()` and `q.bid()`, and the paramet… | correct | widget run: solution passes, starter does not compile (private members, non-const parameter); checks l6.s2.* |
| `screens[4].explain.text` | `const Quote&` accepts a variable, a `const` quote and a temporary, without copying. Inside, only `const` met… | correct | widget run: solution passes, starter does not compile (private members, non-const parameter); checks l6.s2.* |
| `screens[5].prose` | `constexpr` asks for more than `const`: the value must be known while compiling. The compiler can then fold i… | correct | checks l6.s5.constexpr, l6.s5.rest |
| `screens[5].canvas` | canvas (console): {"lines": ["constexpr int lot_size = 100;", "constexpr double tick = 0.01;", "constexpr dou… | correct | checks l6.s5.constexpr, l6.s5.rest |
| `screens[5].widget.answer` | KEY: Tap the line the compiler rejects. -> ["l5"] | correct | checks l6.s5.constexpr, l6.s5.rest |
| `screens[5].hints[0]` | Which values could the compiler work out without running anything? | correct | checks l6.s5.constexpr, l6.s5.rest |
| `screens[5].hints[1]` | `read_tick()` runs only when the program starts. | correct | checks l6.s5.constexpr, l6.s5.rest |
| `screens[5].hints[2]` | Line 5 asks for a compile-time value from a run-time call. Line 6 is fine: `const` only forbids changes later. | correct | checks l6.s5.constexpr, l6.s5.rest |
| `screens[5].feedback.correct` | A `constexpr` value cannot come from a run-time call. | correct | checks l6.s5.constexpr, l6.s5.rest |
| `screens[5].feedback.byKey.l6` | Line 6 uses `const`, which only forbids later changes. Its value may come from a run-time call. | correct | checks l6.s5.constexpr, l6.s5.rest |
| `screens[5].feedback.byKey.l3` | `tick * lot_size` uses two `constexpr` values, so the compiler can multiply them itself. | correct | checks l6.s5.constexpr, l6.s5.rest |
| `screens[5].explain.text` | Line 5 is rejected: "constexpr variable 'live_tick' must be initialized by a constant expression". Lines 1 to… | correct | checks l6.s5.constexpr, l6.s5.rest |
| `screens[6].prose` | `view` is a read-only name for `px`. (`const int x` and `int const x` mean the same; the place of `const` is … | correct | check l6.s6.view |
| `screens[6].canvas` | canvas (graph): {"height": 220, "nodeRadius": 20, "nodes": [{"id": "px", "label": "px", "x": 0.15, "y": 0.2, … | correct | check l6.s6.view |
| `screens[6].widget.options[0]` | KEY: What does it print? -> `99` | correct | check l6.s6.view |
| `screens[6].widget.options[1]` | not: `100` / why: You treated `const` as freezing the vector. It only stops changes made through `view`; `px`… | correct | check l6.s6.view |
| `screens[6].widget.options[2]` | not: It does not compile / why: `px` is not `const`, so `px[0] = 99.0` is allowed. Only writes through `view`… | correct | check l6.s6.view |
| `screens[6].hints[0]` | How many vectors are there? | correct | check l6.s6.view |
| `screens[6].hints[1]` | `view` and `px` name the same box. | correct | check l6.s6.view |
| `screens[6].hints[2]` | `px[0] = 99.0` changes the one vector. `view[0]` reads that vector, so it prints 99. | correct | check l6.s6.view |
| `screens[6].feedback.correct` | `const` limited `view`, not the vector. | correct | check l6.s6.view |
| `screens[6].feedback.byKey.hundred` | You treated `const` as freezing the vector. It only stops changes made through `view`; `px` changed it. | correct | check l6.s6.view |
| `screens[6].explain.text` | There is one vector with two names. `const` restricts the name `view`, so `view[0] = 1` would not compile, bu… | correct | check l6.s6.view |
| `screens[7].prose` | This function does not compile: it writes through a `const` reference. Keep the promise to the caller. Make y… | correct | check l6.s7.starter-error |
| `screens[7].canvas` | canvas (console): {"lines": ["main.cpp:5:15: error: cannot assign to return value", " because function 'opera… | correct | check l6.s7.starter-error |
| `screens[7].widget.solution` | code: Fix `with_fees`: return the prices with `fee` added to each; leave the caller's vector unchanged. (5 hi… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; check l6.s7.starter-error |
| `screens[7].hints[0]` | You may not change `px`. What may you change? | correct | check l6.s7.starter-error |
| `screens[7].hints[1]` | A local `std::vector<double> out = px;` is your own copy. | correct | check l6.s7.starter-error |
| `screens[7].hints[2]` | Copy into `out`, add `fee` to each `out[i]`, and `return out;`. Returning it is free: copy elision. | correct | check l6.s7.starter-error |
| `screens[7].feedback.correct` | One deliberate copy, and the caller's prices are untouched. | correct | check l6.s7.starter-error |
| `screens[7].feedback.byKey.compile` | The parameter must stay `const std::vector<double>&`. Change a local copy instead of `px`. | correct | check l6.s7.starter-error |
| `screens[7].explain.text` | `std::vector<double> out = px;` is the one copy this function needs, and it is yours to change. The caller's … | correct | check l6.s7.starter-error |
| `screens[8].prose` | Every `const` you used is a promise the compiler checks. ```cpp const double tick = 0.01; // never reassigned… | correct | check l6.s3.widen, l6.s3.ok; ISO C++17 (N4659) [class.this], [class.mfct.non-static]/5 |
| `screens[8].widget.options[0]` | KEY: A `const Quote q` can call which of its methods? -> Only those marked `const` | correct | check l6.s3.widen, l6.s3.ok; ISO C++17 (N4659) [class.this], [class.mfct.non-static]/5 |
| `screens[8].widget.options[1]` | not: All of them / why: A method without `const` may change the object, so the compiler stops a `const` objec… | correct | check l6.s3.widen, l6.s3.ok; ISO C++17 (N4659) [class.this], [class.mfct.non-static]/5 |
| `screens[8].widget.options[2]` | not: None of them: it can only read members / why: Methods marked `const` are allowed, and getters such as `b… | correct | check l6.s3.widen, l6.s3.ok; ISO C++17 (N4659) [class.this], [class.mfct.non-static]/5 |
| `screens[8].feedback.correct` | Only methods that promise not to change it. | correct | check l6.s3.widen, l6.s3.ok; ISO C++17 (N4659) [class.this], [class.mfct.non-static]/5 |
| `screens[8].explain.text` | A `const` object can read its members and call `const` methods. Mark every method that does not change the ob… | correct | check l6.s3.widen, l6.s3.ok; ISO C++17 (N4659) [class.this], [class.mfct.non-static]/5 |
| `screens[9].prose` | The next lesson builds pointers: `double* p` holds the address of a `double`, and `*p` is the `double` there.… | correct | ISO C++17 (N4659) [dcl.ptr]/1; checks l6.s10.* |
| `screens[9].widget.answer` | KEY order: `p` is: start at the name > a `const`: the `const` next to `p` fixes `p` itself > pointer to: the … | correct | ISO C++17 (N4659) [dcl.ptr]/1; checks l6.s10.* |
| `screens[9].hints[0]` | Start at the name and move left one piece at a time. | correct | ISO C++17 (N4659) [dcl.ptr]/1; checks l6.s10.* |
| `screens[9].hints[1]` | Directly left of `p` is `const`; left of that is `*`. | correct | ISO C++17 (N4659) [dcl.ptr]/1; checks l6.s10.* |
| `screens[9].hints[2]` | `p` is a `const` pointer to a `const double`: neither `p` nor `*p` can change. | correct | ISO C++17 (N4659) [dcl.ptr]/1; checks l6.s10.* |
| `screens[9].feedback.correct` | A `const` pointer to a `const double`. | correct | ISO C++17 (N4659) [dcl.ptr]/1; checks l6.s10.* |
| `screens[9].feedback.byKey.cd` | The type pointed at is the last thing you reach, at the far left. | correct | ISO C++17 (N4659) [dcl.ptr]/1; checks l6.s10.* |
| `screens[9].explain.text` | From the name: `p` is `const`, then `*` makes it a pointer, then `const double` is what it points at. So `p` … | correct | ISO C++17 (N4659) [dcl.ptr]/1; checks l6.s10.* |
| `screens[10].prose` | Use the right-to-left reading. A `const` next to the name fixes the pointer; a `const` next to `double` fixes… | correct | checks l6.s10.ptr-to-const, l6.s10.const-ptr, l6.s10.both |
| `screens[10].widget.rows` | KEY table: [["`double* p`", "Yes", "Yes"], ["`const double* p`", "No", "Yes"], ["`double* const p`", "Yes", "… | correct | checks l6.s10.ptr-to-const, l6.s10.const-ptr, l6.s10.both |
| `screens[10].hints[0]` | Read each declaration from `p` leftwards. | correct | checks l6.s10.ptr-to-const, l6.s10.const-ptr, l6.s10.both |
| `screens[10].hints[1]` | `const double* p`: `p` is a pointer to a `const double`. The pointer itself is not `const`. | correct | checks l6.s10.ptr-to-const, l6.s10.const-ptr, l6.s10.both |
| `screens[10].hints[2]` | Row 2: No, Yes. Row 3: `p` is a `const` pointer to `double`: Yes, No. Row 4: No, No. | correct | checks l6.s10.ptr-to-const, l6.s10.const-ptr, l6.s10.both |
| `screens[10].feedback.correct` | `const` binds to what sits on its left, or to its right when nothing is on its left. | correct | checks l6.s10.ptr-to-const, l6.s10.const-ptr, l6.s10.both |
| `screens[10].explain.text` | `const double* p` is a pointer to read-only values: `*p = 3` fails, `p = &y` is fine. `double* const p` is th… | correct | checks l6.s10.ptr-to-const, l6.s10.const-ptr, l6.s10.both |
| `screens[11].prose` | A feed handler calls every strategy for each tick, 2 million times a second. ```cpp struct Tick { std::string… | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `screens[11].widget.options[0]` | KEY: Why does the callback take `const Tick&`? -> No copy per call, and no strategy can change the tick the n… | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `screens[11].widget.options[1]` | not: `const` makes the compiler run strategies in parallel / why: `const` says nothing about threads. It forb… | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `screens[11].widget.options[2]` | not: `const&` keeps the tick alive after the callback returns / why: The feed owns the tick and may reuse it … | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `screens[11].widget.options[3]` | not: A plain `Tick&` would copy the tick / why: A plain reference copies nothing either. It would let a strat… | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `screens[11].hints[0]` | Two costs matter here: copying, and one strategy breaking another. | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `screens[11].hints[1]` | Each tick goes to many strategies in turn. | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `screens[11].hints[2]` | `&` avoids copying the string and three numbers. `const` stops one strategy editing the tick the next one rea… | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `screens[11].feedback.correct` | Shared, read only, and cheap. | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `screens[11].feedback.byKey.plainref` | A plain reference avoids the copy too, but any strategy could change the tick for the others. | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `screens[11].explain.text` | `&` means the handler passes its own tick without copying the symbol string. `const` means no strategy can ed… | correct | derivation: a reference copies nothing; const forbids writes (checks l6.s1.px, l6.s6.view) |
| `quiz[0].widget.options[0]` | KEY: Which declarations make `lots` read only? -> Both `const int lots = 5;` and `int const lots = 5;` | correct | check l6.q0.east-west |
| `quiz[0].widget.options[1]` | not: Only `const int lots = 5;` / why: `const` may sit either side of `int`; both lines declare the same type. | correct | check l6.q0.east-west |
| `quiz[0].widget.options[2]` | not: Only `int const lots = 5;` / why: `const int` and `int const` are the same type, so both are read only. | correct | check l6.q0.east-west |
| `quiz[0].feedback.correct` | Same type, two spellings. | correct | check l6.q0.east-west |
| `quiz[0].explain.text` | For a plain type, `const int` and `int const` mean the same. The position matters only around a `*`, where it… | correct | check l6.q0.east-west |
| `quiz[1].widget.options[0]` | KEY: A desk reads its risk limits from `desk.ini` once, at start-up, and never changes them. Which declaratio… | correct | check l6.s5.constexpr and l6.s5.rest |
| `quiz[1].widget.options[1]` | not: `constexpr Limits limits = load_limits("desk.ini");` / why: `constexpr` needs the value while compiling,… | correct | check l6.s5.constexpr and l6.s5.rest |
| `quiz[1].widget.options[2]` | not: `Limits limits = load_limits("desk.ini");` / why: That works, but nothing stops a later line changing th… | correct | check l6.s5.constexpr and l6.s5.rest |
| `quiz[1].feedback.correct` | Set once at start-up, then read only. | correct | check l6.s5.constexpr and l6.s5.rest |
| `quiz[1].explain.text` | The limits are known only when the program runs, so `constexpr` is impossible. `const` fixes them after that … | correct | check l6.s5.constexpr and l6.s5.rest |
| `quiz[2].prose` | ```cpp struct Position { int qty; }; void report(const Position& p) { p.qty = 0; } ``` | correct | check l6.q2.report |
| `quiz[2].widget.options[0]` | KEY: What happens when you build this? -> It does not compile: `p` is a `const` reference | correct | check l6.q2.report |
| `quiz[2].widget.options[1]` | not: It compiles and sets the caller's quantity to 0 / why: That would need a plain `Position&`. The `const` … | correct | check l6.q2.report |
| `quiz[2].widget.options[2]` | not: It compiles and changes a local copy / why: `const Position&` is not a copy. The compiler simply refuses… | correct | check l6.q2.report |
| `quiz[2].feedback.correct` | The promise is checked at compile time. | correct | check l6.q2.report |
| `quiz[2].explain.text` | clang says "cannot assign to variable 'p' with const-qualified type 'const Position &'". A reporting function… | correct | check l6.q2.report |
| `quiz[3].widget.options[0]` | KEY: `double total(const std::vector<double>& v);` Does `total({1.0, 2.0})` compile? -> Yes: a `const` refere… | correct | check l6.q3.temp |
| `quiz[3].widget.options[1]` | not: No: a reference needs a named variable / why: That is the rule for a plain `T&`. A `const&` promises not… | correct | check l6.q3.temp |
| `quiz[3].feedback.correct` | `const&` accepts temporaries. | correct | check l6.q3.temp |
| `quiz[3].explain.text` | A `const` reference may bind to a temporary, which then lives until the call ends. That is why `const&` param… | correct | check l6.q3.temp |
| `summary.ideas[0]` | `const` is a promise the compiler checks. A `const` variable is never reassigned, and a `const&` parameter is… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | A `const` reference accepts variables, `const` objects and temporaries; a `const` object can call only method… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | `const` restricts one name, not the object: another name may still change it. `constexpr` also demands the va… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \texttt{const double* const p} \quad\to\quad p \text{ is a const pointer to a const double} / Start at the na… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | A `const&` view is not a frozen copy: if the object changes through another name, the view sees the change. | correct | restates the lesson: see the rows of the screens it summarises |

## l7-addresses.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | Every object sits at an **address**, a numbered place in memory. `&qty` gives `qty`'s address, and `int* p` h… | correct | check l7.s0.write-through |
| `screens[0].canvas` | canvas (graph): {"height": 230, "nodeRadius": 20, "nodes": [{"id": "qty", "label": "qty", "x": 0.12, "y": 0.2… | correct | check l7.s0.write-through |
| `screens[0].widget.options[0]` | KEY: What does it print? -> `500` | correct | check l7.s0.write-through |
| `screens[0].widget.options[1]` | not: `300` / why: You read `*p = 500` as changing `p`. The `*` means the `int` that `p` points at, which is `… | correct | check l7.s0.write-through |
| `screens[0].widget.options[2]` | not: `0x1000` / why: Printing `qty` prints its value. Its address would be `&qty`. | correct | check l7.s0.write-through |
| `screens[0].widget.options[3]` | not: It does not compile / why: `*p = 500` is the normal way to write through a pointer, so it compiles. | correct | check l7.s0.write-through |
| `screens[0].hints[0]` | What does the `*` in `*p = 500` refer to: the pointer, or what it points at? | correct | check l7.s0.write-through |
| `screens[0].hints[1]` | Follow the dashed arrow from `p`'s box. | correct | check l7.s0.write-through |
| `screens[0].hints[2]` | `*p` is the `int` at the address `p` holds, which is `qty`. Writing 500 there changes `qty`. | correct | check l7.s0.write-through |
| `screens[0].feedback.correct` | `*p` is `qty`. | correct | check l7.s0.write-through |
| `screens[0].feedback.byKey.three` | You read `*p = 500` as changing `p`. The `*` reaches the `int` that `p` points at, which is `qty`. | correct | check l7.s0.write-through |
| `screens[0].explain.text` | `p` holds `qty`'s address, so `*p` reaches `qty` itself. Writing 500 through `*p` changes `qty`. `p`'s own bo… | correct | check l7.s0.write-through |
| `screens[1].prose` | A pointer can hold the address of a vector element. Adding a whole number moves it along the elements. ```cpp… | correct | check l7.s1.arith |
| `screens[1].canvas` | canvas (array): {"cells": ["101.50", "101.25", "101.75", "102.00"]} | correct | check l7.s1.arith |
| `screens[1].widget.answer` | KEY: Tap the price that `*(p + 2)` reads. -> ["c3"] | correct | check l7.s1.arith |
| `screens[1].hints[0]` | Where does `p` start? | correct | check l7.s1.arith |
| `screens[1].hints[1]` | `p` starts at index 1. | correct | check l7.s1.arith |
| `screens[1].hints[2]` | `p + 2` is two elements on from index 1, which is index 3. `*` reads the price there. | correct | check l7.s1.arith |
| `screens[1].feedback.correct` | Two elements on from `px[1]` is `px[3]`. | correct | check l7.s1.arith |
| `screens[1].feedback.byKey.c2` | That is `*(p + 1)`. Move two elements from `px[1]`. | correct | check l7.s1.arith |
| `screens[1].feedback.byKey.c1` | That is `*p` itself. `p + 2` moves two elements on. | correct | check l7.s1.arith |
| `screens[1].feedback.byKey.c0` | `p` starts at `px[1]`, not `px[0]`. Count two on from there. | correct | check l7.s1.arith |
| `screens[1].explain.text` | `p` points at `px[1]`, so `p + 2` points at `px[3]`, and `*(p + 2)` reads 102.00. Pointer arithmetic counts w… | correct | check l7.s1.arith |
| `screens[2].prose` | `&x` is the **address of** `x`. `double* p` is a **pointer**: a variable holding an address. `*p` **dereferen… | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[2].canvas` | canvas (number-line): {"min": 0, "max": 32, "step": 8, "labels": [{"x": 0, "text": "0x1000"}, {"x": 8, "text"… | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[2].widget.answer` | KEY: How many bytes past `p`'s address is the address `p + 2` holds? -> 16 (16 bytes: 2 elements of 8 bytes e… | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[2].widget.wrong[0]` | slip two = 2: You counted elements. The address moves by 2 elements times 8 bytes. | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[2].widget.wrong[1]` | slip eight = 8: That is one element, `p + 1`. | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[2].widget.wrong[2]` | slip twentyfour = 24: That is the distance from `px[0]`. Measure from `p`, which starts at `px[1]`. | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[2].hints[0]` | `p + 2` moves two elements. How big is one element? | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[2].hints[1]` | `px[1]` and `px[3]` are two steps apart on the line. | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[2].hints[2]` | Each `double` is 8 bytes, so two elements are 16 bytes: 0x1008 + 16 = 0x1018. | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[2].feedback.correct` | `p + 2` moves 2 × 8 bytes. | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[2].explain.text` | `p + 2` moves two whole `double`s, and each is 8 bytes, so the address grows by 16: from 0x1008 to 0x1018. Th… | correct | check l7.s1.arith (16 bytes); 0x1008 + 16 = 0x1018 (check l7.q3.hex) |
| `screens[3].prose` | `nullptr` is the pointer that points at nothing. Reading or writing through it is **undefined behaviour**: a … | correct | checks l7.s3.fb-test-5, l7.s3.null-write |
| `screens[3].canvas` | canvas (console): {"lines": ["int fills = 7;", "bump(&fills); // fills is now 8", "bump(nullptr); // does not… | correct | checks l7.s3.fb-test-5, l7.s3.null-write |
| `screens[3].widget.solution` | code: Write `void bump(int* p)`: add 1 to the `int` that `p` points at, and do nothing when `p` is `nullptr`.… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l7.s3.fb-test-5, l7.s3.null-write |
| `screens[3].hints[0]` | Two steps: guard against `nullptr`, then write through `p`. | correct | checks l7.s3.fb-test-5, l7.s3.null-write |
| `screens[3].hints[1]` | `*p += 1;` changes the `int` that `p` points at. `p += 1` would move the pointer instead. | correct | checks l7.s3.fb-test-5, l7.s3.null-write |
| `screens[3].hints[2]` | `if (p == nullptr) return;` then `*p += 1;`. | correct | checks l7.s3.fb-test-5, l7.s3.null-write |
| `screens[3].feedback.correct` | Guard, then write through the pointer. | correct | checks l7.s3.fb-test-5, l7.s3.null-write |
| `screens[3].feedback.byKey.test-5` | The `nullptr` test failed: the code wrote through a null pointer. Return before `*p` when `p == nullptr`. | correct | checks l7.s3.fb-test-5, l7.s3.null-write |
| `screens[3].explain.text` | `*p += 1` changes the `int` at the address `p` holds, so the caller's `fills` becomes 8. The guard matters: a… | correct | checks l7.s3.fb-test-5, l7.s3.null-write |
| `screens[4].prose` | A range can be passed as two pointers: `begin` at the first element, and `end` one *past* the last. `end` is … | correct | checks l7.s4.fb-test-2, l7.s4.fb-test-5 |
| `screens[4].canvas` | canvas (array): {"cells": ["101.50", "99.25", "102.75", "100.00", ""]} | correct | checks l7.s4.fb-test-2, l7.s4.fb-test-5 |
| `screens[4].widget.solution` | code: Write `max_via_pointer(begin, end)`: the largest value in the range. An empty range (`begin == end`) re… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l7.s4.fb-test-2, l7.s4.fb-test-5 |
| `screens[4].hints[0]` | Start the best value at `*begin`, not at 0: prices can be negative returns. | correct | checks l7.s4.fb-test-2, l7.s4.fb-test-5 |
| `screens[4].hints[1]` | A loop `for (const double* p = begin; p != end; ++p)` visits each element once. | correct | checks l7.s4.fb-test-2, l7.s4.fb-test-5 |
| `screens[4].hints[2]` | Return 0 if `begin == end`. Otherwise set `best = *begin`, then for each `p` after it, keep `*p` if it is lar… | correct | checks l7.s4.fb-test-2, l7.s4.fb-test-5 |
| `screens[4].feedback.correct` | `p != end` stops exactly at the last element. | correct | checks l7.s4.fb-test-2, l7.s4.fb-test-5 |
| `screens[4].feedback.byKey.test-2` | All three values are negative, so a best that starts at 0 never changes. Start from `*begin`. | imprecise | correct for a best that starts at 0 (check l7.s4.fb-test-2), but `p <= end` also lands here with a stray number (check l7.s4.fb-test-5); finding 13 |
| `screens[4].feedback.byKey.test-5` | The range is `xs[1]` to `xs[2]`. Read from `begin` and stop before `end`. | imprecise | check l7.s4.fb-test-5: `p <= end` passes test 5 (xs[3] is 2) and fails test 2 on a stray read; finding 13 |
| `screens[4].explain.text` | `++p` moves one `double` on, and `p != end` stops before the address one past the last. Starting `best` at `*… | correct | checks l7.s4.fb-test-2, l7.s4.fb-test-5 |
| `screens[5].prose` | `bid` lives inside the inner braces. In this browser the program printed `101.25`. ```cpp double* p = nullptr… | correct | check l7.s5.dangling |
| `screens[5].canvas` | canvas (graph): {"height": 150, "nodeRadius": 20, "nodes": [{"id": "p", "label": "p", "x": 0.15, "y": 0.5, "s… | correct | check l7.s5.dangling |
| `screens[5].widget.options[0]` | KEY: Is the program correct? -> No: `bid` ended at `}`, so `*p` reads a dead object, which is undefined behav… | correct | check l7.s5.dangling |
| `screens[5].widget.options[1]` | not: Yes: it printed the right price / why: That is the trap. The read is undefined: it may print the old val… | correct | check l7.s5.dangling |
| `screens[5].widget.options[2]` | not: Yes: `p` keeps `bid` alive / why: A pointer only holds an address. It does not keep the object alive; `b… | correct | check l7.s5.dangling |
| `screens[5].widget.options[3]` | not: No: it does not compile / why: It compiles cleanly. The compiler cannot always see that `p` outlives `bi… | correct | check l7.s5.dangling |
| `screens[5].hints[0]` | When does `bid` stop existing? | correct | check l7.s5.dangling |
| `screens[5].hints[1]` | `bid` is declared inside `{ }`. Its life ends at the `}`. | correct | check l7.s5.dangling |
| `screens[5].hints[2]` | After the `}`, `p` holds the address of a dead `double`. Reading it is undefined, whatever it prints. | correct | check l7.s5.dangling |
| `screens[5].feedback.correct` | A right answer from undefined behaviour is luck. | correct | check l7.s5.dangling |
| `screens[5].feedback.byKey.fine` | That is the trap. The read is undefined; the browser build just left 101.25 in that memory. A desk build with… | correct | check l7.s5.dangling |
| `screens[5].feedback.byKey.alive` | A pointer does not keep its target alive. `bid` ended at its closing brace. | correct | check l7.s5.dangling |
| `screens[5].explain.text` | `bid` ends at the inner `}`, and `p` is left **dangling**. Undefined behaviour means the compiler may do anyt… | correct | check l7.s5.dangling |
| `screens[6].prose` | The same code saved as `scope.cpp` and built on Linux with g++ and AddressSanitizer, which watches every memo… | correct | check l7.s6.asan-scope |
| `screens[6].canvas` | canvas (console): {"lines": ["$ g++ -g -fsanitize=address scope.cpp -o scope", "$ ./scope", "ERROR: AddressSa… | correct | check l7.s6.asan-scope |
| `screens[6].widget.answer` | KEY: Tap the line that names the variable whose dead memory was read. -> ["l8"] | correct | check l7.s6.asan-scope |
| `screens[6].hints[0]` | One line quotes a variable name in single quotes. | correct | check l7.s6.asan-scope |
| `screens[6].hints[1]` | The frame lists its objects; one of them is where the read landed. | correct | check l7.s6.asan-scope |
| `screens[6].hints[2]` | `[32, 40) 'bid' (line 5)` is the 8 bytes of `bid`, declared on line 5, and the arrow says the read was inside… | correct | check l7.s6.asan-scope |
| `screens[6].feedback.correct` | `bid`, declared on line 5. | correct | check l7.s6.asan-scope |
| `screens[6].feedback.byKey.l5` | That line says *where in the code* the read happened, line 8. The variable is named further down. | correct | check l7.s6.asan-scope |
| `screens[6].feedback.byKey.l4` | `READ of size 8` says a `double` was read. Which variable's memory was it? | correct | check l7.s6.asan-scope |
| `screens[6].feedback.byKey.l3` | That names the kind of error. The variable is named further down. | correct | check l7.s6.asan-scope |
| `screens[6].explain.text` | `'bid' (line 5)` names the variable, and `scope.cpp:8` names the read. `READ of size 8` is one `double`. Buil… | correct | check l7.s6.asan-scope |
| `screens[7].prose` | What you used, in one place: ```cpp int* p = &x; // p holds x's address *p = 5; // write x through p p = null… | correct | check l7.s1.arith (&a == &b prints 0); ISO C++17 (N4659) [intro.object]/8 (distinct objects, distinct addresses) |
| `screens[7].widget.options[0]` | KEY: `double a = 5.0, b = 5.0;` What does `std::cout << (&a == &b);` print? -> `0` | correct | check l7.s1.arith (&a == &b prints 0); ISO C++17 (N4659) [intro.object]/8 (distinct objects, distinct addresses) |
| `screens[7].widget.options[1]` | not: `1` / why: You compared the values. `&a == &b` compares addresses, and two variables never share one. | correct | check l7.s1.arith (&a == &b prints 0); ISO C++17 (N4659) [intro.object]/8 (distinct objects, distinct addresses) |
| `screens[7].feedback.correct` | Two variables, two addresses. | correct | check l7.s1.arith (&a == &b prints 0); ISO C++17 (N4659) [intro.object]/8 (distinct objects, distinct addresses) |
| `screens[7].explain.text` | `&a` and `&b` are two different addresses, so they compare unequal and `std::cout` prints 0 for `false`. To c… | correct | check l7.s1.arith (&a == &b prints 0); ISO C++17 (N4659) [intro.object]/8 (distinct objects, distinct addresses) |
| `screens[8].prose` | `px` starts at 0x1000, with 8-byte `double`s, and `p = &px[1]`. Each line below gives one step and its reason. | correct | check l7.q3.hex, l7.s1.arith; ISO C++17 (N4659) [expr.add]/4 |
| `screens[8].widget.answer` | KEY order: `p` holds 0x1008: `px[1]` is one `double` past 0x1000 > `p + 2` holds 0x1008 + 2 × 8 = 0x1018: ari… | correct | check l7.q3.hex, l7.s1.arith; ISO C++17 (N4659) [expr.add]/4 |
| `screens[8].hints[0]` | Start with what `p` holds. | correct | check l7.q3.hex, l7.s1.arith; ISO C++17 (N4659) [expr.add]/4 |
| `screens[8].hints[1]` | Add before you dereference. | correct | check l7.q3.hex, l7.s1.arith; ISO C++17 (N4659) [expr.add]/4 |
| `screens[8].hints[2]` | Address of `p`, then the address `p + 2`, then which element sits there, then read it. | correct | check l7.q3.hex, l7.s1.arith; ISO C++17 (N4659) [expr.add]/4 |
| `screens[8].feedback.correct` | Address, step, element, read. | correct | check l7.q3.hex, l7.s1.arith; ISO C++17 (N4659) [expr.add]/4 |
| `screens[8].explain.text` | `p` starts at 0x1008. Moving 2 elements adds 16 bytes, giving 0x1018, which is `px[3]`'s address. Only then d… | correct | check l7.q3.hex, l7.s1.arith; ISO C++17 (N4659) [expr.add]/4 |
| `screens[9].prose` | An exchange SDK written in C calls you with a pointer to the first of `n` book levels. `p->size` means `(*p).… | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `screens[9].widget.options[0]` | KEY: Which loop sums every level's size? -> `for (const Level* p = levels; p != levels + n; ++p) total += p->… | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `screens[9].widget.options[1]` | not: `for (const Level* p = levels; p <= levels + n; ++p) total += p->size;` / why: `<=` also reads `levels +… | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `screens[9].widget.options[2]` | not: `for (int i = 0; i < n; ++i) total += levels->size;` / why: `levels` never moves, so this adds the first… | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `screens[9].widget.options[3]` | not: `for (const Level* p = levels; p != levels + n; p += sizeof(Level)) total += p->size;` / why: `++p` alre… | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `screens[9].hints[0]` | Which pointer moves, by how much, and where must it stop? | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `screens[9].hints[1]` | `levels + n` is one past the last level, like `end`. | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `screens[9].hints[2]` | Start at `levels`, step with `++p`, stop when `p == levels + n`. Read `p->size` each time. | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `screens[9].feedback.correct` | One past the end, never read. | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `screens[9].feedback.byKey.bytes` | Pointer arithmetic already scales by the size of `Level`. Adding `sizeof(Level)` jumps 16 levels at a time. | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `screens[9].explain.text` | `++p` moves one `Level` (16 bytes), and `p != levels + n` stops before the address one past the last. Off-by-… | correct | check l7.s1.arith (sizeof(Level) is 16); ISO C++17 (N4659) [expr.add]/4 (one past the end may be formed, not read) |
| `quiz[0].prose` | ```cpp int* p = nullptr; std::cout << *p << "\n"; ``` | correct | checks l7.q0.null-read, l7.q0.segv |
| `quiz[0].widget.options[0]` | KEY: What happens when this runs? -> Undefined behaviour: a desk build usually stops with `Segmentation fault` | correct | checks l7.q0.null-read, l7.q0.segv |
| `quiz[0].widget.options[1]` | not: It prints 0, the value of a null pointer / why: `*p` reads the `int` at address 0, not the pointer's val… | correct | checks l7.q0.null-read, l7.q0.segv |
| `quiz[0].widget.options[2]` | not: It does not compile / why: It compiles. The compiler does not track which pointers are null. | correct | checks l7.q0.null-read, l7.q0.segv |
| `quiz[0].feedback.correct` | Never dereference `nullptr`. | correct | checks l7.q0.null-read, l7.q0.segv |
| `quiz[0].explain.text` | On Linux, g++'s build dies with `Segmentation fault` (AddressSanitizer: "SEGV on unknown address 0x0000000000… | correct | checks l7.q0.null-read, l7.q0.segv |
| `quiz[1].prose` | ```cpp int x = 1; int* p = &x; int** pp = &p; **pp = 7; std::cout << x << "\n"; ``` | correct | check l7.q1.pp |
| `quiz[1].widget.options[0]` | KEY: What does it print? -> `7` | correct | check l7.q1.pp |
| `quiz[1].widget.options[1]` | not: `1` / why: `**pp` follows two arrows: `pp` to `p`, then `p` to `x`. Writing 7 there changes `x`. | correct | check l7.q1.pp |
| `quiz[1].widget.options[2]` | not: It does not compile / why: `int** pp = &p;` is a pointer to a pointer. It compiles. | correct | check l7.q1.pp |
| `quiz[1].feedback.correct` | Two hops, from `pp` to `p` to `x`. | correct | check l7.q1.pp |
| `quiz[1].explain.text` | `pp` holds `p`'s address, so `*pp` is `p`, and `**pp` is what `p` points at: `x`. Writing 7 through it change… | correct | check l7.q1.pp |
| `quiz[2].prose` | ```cpp double* best_bid() { double x = 101.25; return &x; } ``` | correct | check l7.q2.stack-address |
| `quiz[2].widget.options[0]` | KEY: What does the compiler do with this function? -> It compiles with a warning; the returned pointer dangles | correct | check l7.q2.stack-address |
| `quiz[2].widget.options[1]` | not: It refuses to compile / why: clang only warns: "address of stack memory associated with local variable '… | correct | check l7.q2.stack-address |
| `quiz[2].widget.options[2]` | not: It compiles silently, and the pointer is safe / why: `x` ends when the function returns, so the caller g… | correct | check l7.q2.stack-address |
| `quiz[2].feedback.correct` | A warning, not an error: read your warnings. | correct | check l7.q2.stack-address |
| `quiz[2].explain.text` | `x` lives in `best_bid`'s frame and ends at its `}`. clang warns "address of stack memory associated with loc… | correct | check l7.q2.stack-address |
| `quiz[3].widget.options[0]` | KEY: An `int` is 4 bytes. `int* p` holds 0x2000. What address does `p + 3` hold? -> 0x200C | correct | check l7.q3.hex |
| `quiz[3].widget.options[1]` | not: 0x2003 / why: You added 3 bytes. `p + 3` moves 3 whole `int`s: 3 × 4 = 12 bytes, which is 0xC. | correct | check l7.q3.hex |
| `quiz[3].widget.options[2]` | not: 0x2018 / why: You used 8 bytes per element, the size of a `double`. An `int` here is 4. | correct | check l7.q3.hex |
| `quiz[3].feedback.correct` | 3 × 4 = 12 bytes, 0xC in hex. | correct | check l7.q3.hex |
| `quiz[3].explain.text` | Pointer arithmetic scales by the type: `p + 3` moves 3 × 4 = 12 bytes. 12 is C in hex, so the address is 0x20… | correct | check l7.q3.hex |
| `summary.ideas[0]` | `&x` is `x`'s address; a pointer `T* p` holds one, and `*p` reaches the object there. `p + k` moves `k` whole… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | `nullptr` points at nothing. Reading through it, or through a pointer to an object that has ended, is undefin… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | This browser build is forgiving: null reads and dangling reads often print stale numbers. A desk build usuall… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \text{address}(p + k) = \text{address}(p) + k \times \texttt{sizeof(T)} / A range is `[begin, end)`: `end` po… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | A program that prints the right number can still read a dead object. Undefined behaviour is not a crash you c… | correct | restates the lesson: see the rows of the screens it summarises |

## l8-stack-and-heap.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | Two programs store two million prices, 16 MB. The locals of every running function share one fixed region of … | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].canvas` | canvas (table): {"columns": ["Program", "Declares", "Bytes"], "rows": [["A", "`double prices[2000000]`", "16,… | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].widget.options[0]` | KEY: Which program crashes? -> A only | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].widget.options[1]` | not: Both: 16 MB does not fit in 8 MB / why: B's vector keeps its two million `double`s somewhere else; only … | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].widget.options[2]` | not: B only / why: A's array is a local, all 16 MB of it, so A is the one that does not fit. | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].widget.options[3]` | not: Neither / why: A asks for 16 MB of locals in an 8 MB region, so it runs off the end. | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].hints[0]` | Where does each program put the two million `double`s? | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].hints[1]` | A's array is itself a local. B's local is a `std::vector`, which holds a pointer to its elements. | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].hints[2]` | A needs 16 MB of locals and has 8 MB: it crashes. B's elements live elsewhere, so B runs. | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].feedback.correct` | Only the array is a 16 MB local. | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].feedback.byKey.both` | B's elements are not locals. The vector object is small; it points at its elements elsewhere. | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[0].explain.text` | A's array is a local, so all 16 MB must fit in the 8 MB for locals. It overflows: this browser reports "memor… | correct | checks l8.s0.A, l8.s0.B, l8.s0.desk |
| `screens[1].prose` | Each call gets a **frame** holding its locals and parameters. Step through the program. ```cpp double mid(dou… | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].canvas` | canvas (array): {"cells": ["main: v"], "mode": "stack", "capacity": 3, "showIndex": false, "topLabel": "top"} | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].widget.states` | KEY path: `main` calls `value(300, 99.5, 100.5)` > `value` calls `mid(99.5, 100.5)` > `mid` returns 100 > `va… | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].widget.states.s0.ops[0]` | not: `main` prints `v` / why: `v` comes from `value`, so `main` must call `value` first. | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].widget.states.s1.ops[0]` | not: `value` returns / why: `value` needs `m`, so it must call `mid` first. | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].widget.states.s2.ops[0]` | not: `value` returns / why: Only the frame on top can finish, and `mid` is on top. | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].widget.states.s3.ops[0]` | not: `mid` returns again / why: `mid`'s frame, with its `bid` and `ask`, was removed when it returned. | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].widget.states.s4.ops[1]` | not: `value` returns again / why: `value` has finished; its frame and its `m` are gone. | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].hints[0]` | A call adds a frame on top; a return removes the top frame. | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].hints[1]` | Only the frame on top can finish. | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].hints[2]` | `main` calls `value`, `value` calls `mid`. Then `mid` returns, `value` returns, and `main` prints and ends. | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].feedback.correct` | Last in, first out. | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[1].explain.text` | Frames pile up as calls start and come off the top as they return. When `mid` returned, its `bid` and `ask` w… | correct | derivation by hand trace: mid(99.5, 100.5) = 100; 300 * 100 = 30000; ISO C++17 (N4659) [basic.stc.auto] |
| `screens[2].prose` | The pile of frames is the **stack**. `new` puts an object on the **heap** instead, where it stays until you `… | correct | check l8.s2.heap |
| `screens[2].canvas` | canvas (graph): {"height": 240, "nodeRadius": 20, "nodes": [{"id": "p", "label": "p", "x": 0.2, "y": 0.2, "sh… | correct | check l8.s2.heap |
| `screens[2].widget.options[0]` | KEY: Is reading `*q` in `main` safe? -> Yes: the `double` is on the heap and lives until `delete q` | correct | check l8.s2.heap |
| `screens[2].widget.options[1]` | not: No: it died when `make_price` returned / why: That is true of locals. Only `p` was a local; the `double`… | correct | check l8.s2.heap |
| `screens[2].widget.options[2]` | not: No: `q` is a copy of `p`, so it points somewhere else / why: Copying a pointer copies the address. `q` h… | correct | check l8.s2.heap |
| `screens[2].hints[0]` | Which objects live in `make_price`'s frame, and which does `new` create? | correct | check l8.s2.heap |
| `screens[2].hints[1]` | `p` is in the frame; the `double` is on the heap. | correct | check l8.s2.heap |
| `screens[2].hints[2]` | When `make_price` returns, `p` dies. The heap `double` stays, and `q` holds its address until `delete q`. | correct | check l8.s2.heap |
| `screens[2].feedback.correct` | Heap objects live until `delete`. | correct | check l8.s2.heap |
| `screens[2].feedback.byKey.dies` | Only `p` lived in the frame. The `double` came from `new`, so it is on the heap. | correct | check l8.s2.heap |
| `screens[2].explain.text` | `p` lived in `make_price`'s frame and died at its `}`, but it had already handed its address to `q`. The `dou… | correct | check l8.s2.heap |
| `screens[3].prose` | A local lives on the stack, even when it is a pointer or a vector. What `new` makes, and what a vector holds,… | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.stc.dynamic]; check l8.s0.B (12 bytes) and l8.s0.desk (24 bytes) |
| `screens[3].canvas` | canvas (console): {"lines": ["std::vector<double> load(int n) {", " std::vector<double> px(n, 100.0);", " ret… | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.stc.dynamic]; check l8.s0.B (12 bytes) and l8.s0.desk (24 bytes) |
| `screens[3].widget.rows` | KEY table: [["`n`", "stack"], ["`buf`, the pointer", "stack"], ["`buf[0]`", "heap"], ["`prices`, the vector o… | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.stc.dynamic]; check l8.s0.B (12 bytes) and l8.s0.desk (24 bytes) |
| `screens[3].hints[0]` | Every variable declared inside `main` is a local. What do the pointer and the vector point at? | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.stc.dynamic]; check l8.s0.B (12 bytes) and l8.s0.desk (24 bytes) |
| `screens[3].hints[1]` | `buf` holds an address; `new double[n]` made what it points at. | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.stc.dynamic]; check l8.s0.B (12 bytes) and l8.s0.desk (24 bytes) |
| `screens[3].hints[2]` | `n`, `buf` and `prices` are locals: stack. `buf[0]` came from `new[]`, and `prices[0]` is inside the vector's… | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.stc.dynamic]; check l8.s0.B (12 bytes) and l8.s0.desk (24 bytes) |
| `screens[3].feedback.correct` | The handles are on the stack; the data is on the heap. | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.stc.dynamic]; check l8.s0.B (12 bytes) and l8.s0.desk (24 bytes) |
| `screens[3].explain.text` | `n`, the pointer `buf` and the vector object `prices` are locals in `main`'s frame. The 1,000 `double`s from … | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.stc.dynamic]; check l8.s0.B (12 bytes) and l8.s0.desk (24 bytes) |
| `screens[4].prose` | A **leak** is a `new` with no `delete`: the memory stays taken until the program ends. LeakSanitizer, part of… | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[4].canvas` | canvas (console): {"lines": ["$ g++ -g -fsanitize=address leak.cpp -o leak && ./leak", "==21322==ERROR: LeakS… | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[4].widget.answer` | KEY: A backtest calls `sum_prices(1000)` once a day for 2,500 trading days. How many MB leak? Take 1 MB as 1,… | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[4].widget.wrong[0]` | slip one = 0.008: That is one call. The backtest calls it 2,500 times. | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[4].widget.wrong[1]` | slip bytes = 20000000: That is the count in bytes. Divide by 1,000,000. | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[4].widget.wrong[2]` | slip noeight = 2.5: You counted one byte per price. Each `double` is 8 bytes. | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[4].hints[0]` | How many bytes does one call leak? | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[4].hints[1]` | Line 3 of the report gives one call's leak. | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[4].hints[2]` | Each call leaks 1,000 × 8 = 8,000 bytes. Times 2,500 calls is 20,000,000 bytes, or 20 MB. | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[4].feedback.correct` | 8,000 bytes a day, 20 MB in all. | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[4].explain.text` | Each call leaks one `new double[1000]`, 8,000 bytes, and line 5 of the report names `sum_prices` at `leak.cpp… | correct | checks l8.s4.lsan, l8.s4.mb |
| `screens[5].prose` | A colleague frees an array of prices. In this browser the program runs, prints nothing odd, and exits with st… | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].canvas` | canvas (console): {"lines": ["$ ./prices", "$ echo $?", "0"], "title": "Browser build"} | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].widget.options[0]` | KEY: What is wrong? -> `new[]` must be paired with `delete[]`; plain `delete` is undefined behaviour | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].widget.options[1]` | not: Nothing: the program ran and exited with 0 / why: This browser build is forgiving. Pairing `new[]` with … | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].widget.options[2]` | not: It frees only the first 8 bytes and leaks the rest / why: It is not a tidy partial free. It is undefined… | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].widget.options[3]` | not: It should be `free(px)` / why: `free` pairs with `malloc`, not with `new[]`. Mixing them is undefined to… | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].hints[0]` | How was `px` allocated? | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].hints[1]` | `new double[1000]` has brackets. | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].hints[2]` | Every `new` pairs with `delete`, and every `new[]` with `delete[]`. Mixing them is undefined. | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].feedback.correct` | `new[]` goes with `delete[]`. | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].feedback.byKey.nothing` | This browser build is forgiving. A desk build with `-fsanitize=address` reports "alloc-dealloc-mismatch" here. | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].explain.text` | `new[]` must be freed with `delete[]`. clang warns at compile time, and a desk build with AddressSanitizer st… | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[5].explain.canvas.lines` | explain canvas: ["main.cpp:3:1: warning: 'delete' applied to a pointer", " that was allocated with 'new[]';",… | correct | checks l8.s5.mismatch-runs, l8.s5.asan-mismatch |
| `screens[6].prose` | Finish the program. It reads `n`, then `n` prices into a heap buffer, prints their sum to 2 decimals, and fre… | correct | check l8.s6.fb-test-1 |
| `screens[6].canvas` | canvas (console): {"lines": ["$ echo \"3 101.5 99.25 100\" / ./sum", "300.75", "$ echo \"0\" / ./sum", "0.00"… | correct | check l8.s6.fb-test-1 |
| `screens[6].widget.solution` | code: Complete the program. (5 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; check l8.s6.fb-test-1 |
| `screens[6].hints[0]` | Two loops, or one: read each `px[i]`, then add them up. | correct | check l8.s6.fb-test-1 |
| `screens[6].hints[1]` | `std::cout << std::fixed << std::setprecision(2)` prints two decimals. | correct | check l8.s6.fb-test-1 |
| `screens[6].hints[2]` | Read with `for (int i = 0; i < n; ++i) std::cin >> px[i];`, sum into `total`, print it, and finish with `dele… | correct | check l8.s6.fb-test-1 |
| `screens[6].feedback.correct` | Read, sum, print, `delete[]`. | correct | check l8.s6.fb-test-1 |
| `screens[6].feedback.byKey.test-1` | If the output is right but the test failed with status 1, the leak checker fired. `new[]` needs `delete[]`, n… | correct | check l8.s6.fb-test-1 |
| `screens[6].explain.text` | The buffer from `new double[n]` lives on the heap until `delete[] px`. With `n` = 0 the loops never run and t… | correct | check l8.s6.fb-test-1 |
| `screens[7].prose` | Exchange feeds often have a C interface: you hand over a buffer and the feed fills it. `fill_ticks(double* ou… | unverified | "Exchange feeds often have a C interface": an unsourced remark about industry practice; the rest of the line is correct ([vector.cons]) |
| `screens[7].canvas` | canvas (console): {"lines": ["void fill_ticks(double* out, int n);", "", "read_ticks(5) -> {100, 100.5, 101, … | correct | widget run: solution passes with the leak checker, starter fails; ISO C++17 (N4659) [vector.cons] (iterator-range constructor copies) |
| `screens[7].widget.solution` | code: Write `read_ticks(n)`: fill a `new[]` buffer, return its prices as a vector, and leave no leak. (5 hidd… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; widget run: solution passes with the leak checker, starter fails; ISO C++17 (N4659) [vector.cons] (iterator-range constructor copies) |
| `screens[7].hints[0]` | Allocate, fill, copy, free, return: in that order. | correct | widget run: solution passes with the leak checker, starter fails; ISO C++17 (N4659) [vector.cons] (iterator-range constructor copies) |
| `screens[7].hints[1]` | Free the buffer after copying it into the vector, never before. | correct | widget run: solution passes with the leak checker, starter fails; ISO C++17 (N4659) [vector.cons] (iterator-range constructor copies) |
| `screens[7].hints[2]` | `double* buf = new double[n]; fill_ticks(buf, n); std::vector<double> out(buf, buf + n); delete[] buf; return… | correct | widget run: solution passes with the leak checker, starter fails; ISO C++17 (N4659) [vector.cons] (iterator-range constructor copies) |
| `screens[7].feedback.correct` | The vector owns a copy; the buffer is freed. | correct | widget run: solution passes with the leak checker, starter fails; ISO C++17 (N4659) [vector.cons] (iterator-range constructor copies) |
| `screens[7].explain.text` | The vector copies the `n` prices into its own heap buffer, so the `new[]` buffer can be freed before returnin… | correct | widget run: solution passes with the leak checker, starter fails; ISO C++17 (N4659) [vector.cons] (iterator-range constructor copies) |
| `screens[8].prose` | The lifetimes you saw: ```cpp void f(int n) { double x = 1.0; // stack: dies at } double* p = new double(2.0)… | correct | check l8.s8.deep-recursion |
| `screens[8].widget.options[0]` | KEY: A recursion 10,000,000 calls deep stops with "call stack exhausted". What ran out? -> The stack: every c… | correct | check l8.s8.deep-recursion |
| `screens[8].widget.options[1]` | not: The heap / why: Frames are not on the heap. The heap is for `new` and for containers' elements. | correct | check l8.s8.deep-recursion |
| `screens[8].widget.options[2]` | not: Time: it ran too long / why: Each frame takes stack space, and 10 million waiting frames do not fit, wha… | correct | check l8.s8.deep-recursion |
| `screens[8].feedback.correct` | Deep recursion overflows the stack. | correct | check l8.s8.deep-recursion |
| `screens[8].explain.text` | Each call that has not returned keeps a frame on the stack. Ten million of them need far more than a few MB, … | correct | check l8.s8.deep-recursion |
| `screens[9].prose` | Back to `make_price` and `main`, where `main` does `double* q = make_price();`, reads `*q`, then calls `delet… | correct | ISO C++17 (N4659) [basic.stc.dynamic], [expr.delete]; check l8.s2.heap |
| `screens[9].widget.answer` | KEY order: `main`'s frame is pushed: the program starts > `make_price`'s frame is pushed on top: `main` calle… | correct | ISO C++17 (N4659) [basic.stc.dynamic], [expr.delete]; check l8.s2.heap |
| `screens[9].hints[0]` | Frames come and go with calls; heap objects come and go with `new` and `delete`. | correct | ISO C++17 (N4659) [basic.stc.dynamic], [expr.delete]; check l8.s2.heap |
| `screens[9].hints[1]` | The heap object is created inside `make_price`, and outlives it. | correct | ISO C++17 (N4659) [basic.stc.dynamic], [expr.delete]; check l8.s2.heap |
| `screens[9].hints[2]` | Push `main`, push `make_price`, `new`, pop `make_price`, then `delete` in `main`. | correct | ISO C++17 (N4659) [basic.stc.dynamic], [expr.delete]; check l8.s2.heap |
| `screens[9].feedback.correct` | The heap object outlives the frame that made it. | correct | ISO C++17 (N4659) [basic.stc.dynamic], [expr.delete]; check l8.s2.heap |
| `screens[9].explain.text` | The `double` is created while `make_price`'s frame is on top, survives that frame's pop, and ends only at `de… | correct | ISO C++17 (N4659) [basic.stc.dynamic], [expr.delete]; check l8.s2.heap |
| `screens[10].prose` | A binomial pricer needs `steps + 1` doubles of scratch space per price. A volatility calibration prices 50,00… | correct | ISO C++17 (N4659) [dcl.array] (bound is a constant expression); derivation: 50,000 calls each allocate once |
| `screens[10].widget.options[0]` | KEY: How should the pricer get its scratch space? -> Hold a `std::vector<double>` member, sized once to `step… | correct | ISO C++17 (N4659) [dcl.array] (bound is a constant expression); derivation: 50,000 calls each allocate once |
| `screens[10].widget.options[1]` | not: `new double[steps + 1]` and `delete[]` inside every call / why: That works, but it pays for 50,000 trips… | correct | ISO C++17 (N4659) [dcl.array] (bound is a constant expression); derivation: 50,000 calls each allocate once |
| `screens[10].widget.options[2]` | not: A local array `double v[steps + 1]` / why: In standard C++ an array's size must be known at compile time… | correct | ISO C++17 (N4659) [dcl.array] (bound is a constant expression); derivation: 50,000 calls each allocate once |
| `screens[10].widget.options[3]` | not: `new` once at start-up and never `delete` / why: It runs, but nothing owns the memory or frees it, and l… | correct | ISO C++17 (N4659) [dcl.array] (bound is a constant expression); derivation: 50,000 calls each allocate once |
| `screens[10].hints[0]` | The size is the same for every price. Why allocate it 50,000 times? | correct | ISO C++17 (N4659) [dcl.array] (bound is a constant expression); derivation: 50,000 calls each allocate once |
| `screens[10].hints[1]` | A member lives as long as the pricer object. | correct | ISO C++17 (N4659) [dcl.array] (bound is a constant expression); derivation: 50,000 calls each allocate once |
| `screens[10].hints[2]` | Size a vector once, then reuse its elements: one allocation, freed automatically when the pricer goes. | correct | ISO C++17 (N4659) [dcl.array] (bound is a constant expression); derivation: 50,000 calls each allocate once |
| `screens[10].feedback.correct` | Allocate once, reuse, free automatically. | correct | ISO C++17 (N4659) [dcl.array] (bound is a constant expression); derivation: 50,000 calls each allocate once |
| `screens[10].explain.text` | A vector member is allocated once, reused for all 50,000 prices, and freed when the pricer is destroyed. Allo… | correct | ISO C++17 (N4659) [dcl.array] (bound is a constant expression); derivation: 50,000 calls each allocate once |
| `quiz[0].prose` | ```cpp double price = 101.25; double* p = &price; delete p; ``` | correct | checks l8.q0.delete-local, l8.q0.gxx |
| `quiz[0].widget.options[0]` | KEY: What is wrong here? -> `price` is on the stack; `delete` is only for addresses `new` returned | correct | checks l8.q0.delete-local, l8.q0.gxx |
| `quiz[0].widget.options[1]` | not: Nothing: it frees `price` early / why: Stack objects are freed by their frame, at `}`. `delete` on one i… | correct | checks l8.q0.delete-local, l8.q0.gxx |
| `quiz[0].widget.options[2]` | not: It leaks `price` / why: Nothing leaks: `price` goes with its frame. The bug is deleting memory that `new… | correct | checks l8.q0.delete-local, l8.q0.gxx |
| `quiz[0].feedback.correct` | Only `delete` what `new` made. | correct | checks l8.q0.delete-local, l8.q0.gxx |
| `quiz[0].explain.text` | `price` lives in the frame and is freed at `}`. g++ warns "called on unallocated object 'price'", and the pro… | correct | checks l8.q0.delete-local, l8.q0.gxx |
| `quiz[1].widget.options[0]` | KEY: `int n = 0; double* p = new double[n];` What is true? -> It is valid: `p` is not null, must not be read … | correct | check l8.q1.new-zero |
| `quiz[1].widget.options[1]` | not: It returns `nullptr` / why: `new double[0]` returns a real, non-null pointer to zero elements. | correct | check l8.q1.new-zero |
| `quiz[1].widget.options[2]` | not: It is undefined behaviour / why: Allocating zero elements is allowed. Reading `p[0]` would be undefined;… | correct | check l8.q1.new-zero |
| `quiz[1].feedback.correct` | Zero elements, one block to free. | correct | check l8.q1.new-zero |
| `quiz[1].explain.text` | A zero-length `new[]` is legal and returns a unique non-null pointer. There is nothing to read, but the block… | correct | check l8.q1.new-zero |
| `quiz[2].widget.options[0]` | KEY: A strategy object is created at start-up and used until the program ends. Where can it live? -> A local … | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.start.main] |
| `quiz[2].widget.options[1]` | not: It must be on the heap, made with `new` / why: Nothing forces the heap. `main`'s frame exists from start… | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.start.main] |
| `quiz[2].widget.options[2]` | not: It cannot be a local: locals die too soon / why: Locals die at their function's `}`, and `main`'s `}` is… | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.start.main] |
| `quiz[2].feedback.correct` | `main`'s locals live as long as the program. | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.start.main] |
| `quiz[2].explain.text` | A local in `main` lives until `main` returns, which is the end of the run. Other code can reach it through re… | correct | ISO C++17 (N4659) [basic.stc.auto], [basic.start.main] |
| `quiz[3].widget.options[0]` | KEY: Inside a function, `std::vector<double> v(1000000);` Does it overflow the stack? -> No: the elements are… | correct | check l8.s0.B; 1,000,000 * 8 = 8 MB |
| `quiz[3].widget.options[1]` | not: Yes: 8 MB of locals is too much / why: The 8 MB of elements are on the heap. The local is the vector obj… | correct | check l8.s0.B; 1,000,000 * 8 = 8 MB |
| `quiz[3].feedback.correct` | A vector's data is on the heap. | correct | check l8.s0.B; 1,000,000 * 8 = 8 MB |
| `quiz[3].explain.text` | `v` itself holds a few pointers (12 bytes here, 24 on a desk). Its million `double`s sit on the heap, so the … | correct | check l8.s0.B; 1,000,000 * 8 = 8 MB |
| `summary.ideas[0]` | Each call's locals live in its frame on the stack and die at its `}`. The stack is a few MB, so big arrays an… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | `new` puts an object on the heap until you `delete` it: `new` with `delete`, `new[]` with `delete[]`, exactly… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | A vector object is a small local; its elements are on the heap. The browser build forgives mismatched or doub… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \texttt{new} \leftrightarrow \texttt{delete}, \qquad \texttt{new[]} \leftrightarrow \texttt{delete[]} / Never… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | Plain `delete` on memory from `new[]` is undefined behaviour, even when the program seems to run fine. | correct | restates the lesson: see the rows of the screens it summarises |

## l9-owning-memory.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A **constructor** runs when an object is created; a **destructor**, `~Position`, runs when it ends. Python fr… | correct | check l9.s0.order |
| `screens[0].canvas` | canvas (array): {"cells": ["main", "trade: p (VOD)"], "mode": "stack", "capacity": 3, "showIndex": false, "to… | correct | check l9.s0.order |
| `screens[0].widget.options[0]` | KEY: What does it print? -> `open VOD`, `trading`, `close VOD`, `done` | correct | check l9.s0.order |
| `screens[0].widget.options[1]` | not: `open VOD`, `trading`, `done` / why: You expected cleanup to happen later or not at all, as with a garba… | correct | check l9.s0.order |
| `screens[0].widget.options[2]` | not: `open VOD`, `trading`, `done`, `close VOD` / why: `p` is a local of `trade`, not of `main`. It ends when… | correct | check l9.s0.order |
| `screens[0].widget.options[3]` | not: `open VOD`, `close VOD`, `trading`, `done` / why: `p` lives until the end of its scope, so `trading` pri… | correct | check l9.s0.order |
| `screens[0].hints[0]` | When does `p`'s frame disappear? | correct | check l9.s0.order |
| `screens[0].hints[1]` | `p` is a local of `trade`. | correct | check l9.s0.order |
| `screens[0].hints[2]` | `trade` prints `trading`, then reaches `}`: `p`'s destructor prints `close VOD`. Only then does `main` print … | correct | check l9.s0.order |
| `screens[0].feedback.correct` | The destructor runs at the closing brace, every time. | correct | check l9.s0.order |
| `screens[0].feedback.byKey.never` | You expected cleanup later, as with a garbage collector. C++ runs the destructor at `trade`'s `}`. | correct | check l9.s0.order |
| `screens[0].explain.text` | `p` lives in `trade`'s frame. At `trade`'s `}` its destructor runs and prints `close VOD`, then `main` prints… | correct | check l9.s0.order |
| `screens[1].prose` | This volume-weighted average price allocates scratch space with `new[]`. A function can leave by any `return`. | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[1].canvas` | canvas (console): {"lines": ["double vwap(const std::vector<double>& px, const std::vector<double>& qty) {", … | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[1].widget.answer` | KEY: Tap every line that returns without freeing `notional`. -> ["l3", "l9"] | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[1].widget.wrong[0]` | slip set all = ["l3", "l9", "l11"]: Line 11 runs after the `delete[]` on line 10, so it does not leak. | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[1].hints[0]` | Find every `return`. Which ones run before line 10? | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[1].hints[1]` | Line 10 is the only `delete[]`. | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[1].hints[2]` | Lines 3 and 9 return before line 10 runs. Line 11 comes after the `delete[]`. | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[1].feedback.correct` | Two early exits skip the `delete[]`. | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[1].feedback.byKey.l11` | Line 11 runs after `delete[] notional;`, so it is safe. | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[1].feedback.byKey.l2` | Line 2 allocates. The leaks are the returns that skip line 10. | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[1].explain.text` | Lines 3 and 9 leave before line 10, so their `new[]` block is never freed. Every new exit, or a `throw`, is a… | correct | read off the listing: returns on lines 3 and 9 precede the delete[] on line 10 |
| `screens[2].prose` | Give the memory an owner whose destructor frees it. That pattern is **RAII**: a constructor acquires the reso… | correct | check l9.s2.throw-runs-destructor |
| `screens[2].canvas` | canvas (console): {"lines": ["double vwap(const std::vector<double>& px, const std::vector<double>& qty) {", … | correct | check l9.s2.throw-runs-destructor |
| `screens[2].widget.options[0]` | KEY: Now which `return` lines free the scratch space? -> All three: `notional`'s destructor runs at every exit | correct | check l9.s2.throw-runs-destructor |
| `screens[2].widget.options[1]` | not: Only line 10, the normal exit / why: The vector is a local. Whatever path leaves the function, its destr… | correct | check l9.s2.throw-runs-destructor |
| `screens[2].widget.options[2]` | not: None, until you call `notional.clear()` / why: `clear` empties a vector you keep using. Its destructor f… | correct | check l9.s2.throw-runs-destructor |
| `screens[2].hints[0]` | When does a local's destructor run? | correct | check l9.s2.throw-runs-destructor |
| `screens[2].hints[1]` | Every `return` ends the function's frame. | correct | check l9.s2.throw-runs-destructor |
| `screens[2].hints[2]` | Each `return` ends `vwap`'s frame, and the vector's destructor frees its heap buffer every time. | correct | check l9.s2.throw-runs-destructor |
| `screens[2].feedback.correct` | Every exit runs the destructor. | correct | check l9.s2.throw-runs-destructor |
| `screens[2].feedback.byKey.last` | The destructor runs on every path out of the function, not just the last one. | correct | check l9.s2.throw-runs-destructor |
| `screens[2].explain.text` | `notional` owns its heap buffer, and its destructor runs at every exit, early returns and `throw`s included. … | imprecise | check l9.s2.throw-runs-destructor; ISO C++17 (N4659) [except.handle]/9: with no handler, whether the stack is unwound is implementation-defined; in this app a throw ends the run and no destructor runs; finding 4 |
| `screens[3].prose` | `std::unique_ptr<T>` owns one heap object and deletes it in its destructor. `std::make_unique<T>()` creates t… | correct | checks l9.s3.fb-test-3, l9.s3.delete-unique |
| `screens[3].canvas` | canvas (console): {"lines": ["struct Book {", " static inline int live = 0; // Books that exist", " Book(); /… | correct | checks l9.s3.fb-test-3, l9.s3.delete-unique |
| `screens[3].widget.solution` | code: Convert `net_exposure` to `std::make_unique` so that no path leaks the `Book`. (6 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l9.s3.fb-test-3, l9.s3.delete-unique |
| `screens[3].hints[0]` | Replace the raw pointer with an owner, then delete the `delete`. | correct | checks l9.s3.fb-test-3, l9.s3.delete-unique |
| `screens[3].hints[1]` | `auto book = std::make_unique<Book>();` and keep using `book->`. | correct | checks l9.s3.fb-test-3, l9.s3.delete-unique |
| `screens[3].hints[2]` | With `make_unique`, both `return` lines free the `Book`. Remove `delete book;` too: `delete` needs a raw poin… | correct | checks l9.s3.fb-test-3, l9.s3.delete-unique |
| `screens[3].feedback.correct` | No `delete` left, and no leak on any path. | correct | checks l9.s3.fb-test-3, l9.s3.delete-unique |
| `screens[3].feedback.byKey.test-3` | A `Book` is still alive after the capped call: the early `return limit;` skipped the `delete`. Let a `unique_… | correct | checks l9.s3.fb-test-3, l9.s3.delete-unique |
| `screens[3].explain.text` | `book` now owns the `Book`, and its destructor deletes it on both returns. The capped path, which leaked befo… | correct | checks l9.s3.fb-test-3, l9.s3.delete-unique |
| `screens[4].prose` | A `unique_ptr` is the *only* owner, so copying one is a compile error. `std::move(a)` hands ownership over in… | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].canvas` | canvas (console): {"lines": ["main.cpp:6:16: error: call to implicitly-deleted", " copy constructor of 'std::… | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].widget.options[0]` | KEY: Which call compiles and leaves exactly one owner? -> `book_order(std::move(a));` | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].widget.options[1]` | not: `book_order(a.get());` / why: `get()` returns a raw `Order*`, and the parameter wants a `unique_ptr`, so… | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].widget.options[2]` | not: `std::unique_ptr<Order> b = a; book_order(b);` / why: That is the same copy, and the same error. | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].widget.options[3]` | not: `book_order(*a);` / why: `*a` is the `Order` itself, not an owner of it, so the types do not match. | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].hints[0]` | Copying is banned. What else can happen to ownership? | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].hints[1]` | The error says copying is deleted; moving is not. | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].hints[2]` | `std::move(a)` moves ownership into the parameter. Afterwards `a` is null. | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].feedback.correct` | Ownership moves; it is never copied. | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].feedback.byKey.get` | `get()` gives a raw pointer, not an owner. Two owners would delete the order twice. | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[4].explain.text` | `std::move(a)` transfers the order to `o`, and `a` becomes null: test it with `if (a)`. When `book_order` end… | correct | checks l9.s4.copy-error, l9.s4.move, l9.s4.get, l9.s4.deref |
| `screens[5].prose` | Returning a `unique_ptr` hands ownership to the caller: no copy, no leak. An empty `unique_ptr` (`nullptr`) s… | correct | check l9.s5.fb-test-4 |
| `screens[5].canvas` | canvas (console): {"lines": ["struct Position {", " std::string sym;", " int qty;", " Position(std::string s,… | correct | check l9.s5.fb-test-4 |
| `screens[5].widget.solution` | code: Write `open_position(sym, qty)`: a new `Position` owned by a `unique_ptr`, or `nullptr` when `qty` is 0… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; check l9.s5.fb-test-4 |
| `screens[5].hints[0]` | Two cases: `qty == 0`, and everything else. | correct | check l9.s5.fb-test-4 |
| `screens[5].hints[1]` | `return std::make_unique<Position>(sym, qty);` creates the position and its owner. | correct | check l9.s5.fb-test-4 |
| `screens[5].hints[2]` | `if (qty == 0) return nullptr;` then `return std::make_unique<Position>(sym, qty);`. | correct | check l9.s5.fb-test-4 |
| `screens[5].feedback.correct` | The caller now owns the position. | correct | check l9.s5.fb-test-4 |
| `screens[5].feedback.byKey.test-4` | A quantity of 0 should return an empty pointer: `return nullptr;`. | correct | check l9.s5.fb-test-4 |
| `screens[5].explain.text` | `make_unique` builds the `Position` on the heap and returns its sole owner, which moves out to the caller. A … | correct | check l9.s5.fb-test-4 |
| `screens[6].prose` | `std::shared_ptr` lets several owners share one object. It keeps a **count** of owners and deletes the object… | correct | check l9.s6.use-count |
| `screens[6].canvas` | canvas (graph): {"height": 200, "nodeRadius": 20, "nodes": [{"id": "a", "label": "a", "x": 0.15, "y": 0.5, "s… | correct | check l9.s6.use-count |
| `screens[6].widget.answer` | KEY: What does `a.use_count()` return at `// here`? -> 3 (3: `a`, `b` and `c` all own the order.) | correct | check l9.s6.use-count |
| `screens[6].widget.wrong[0]` | slip one = 1: That is the count before the braces. `b` and `c` are copies, and each adds an owner. | correct | check l9.s6.use-count |
| `screens[6].widget.wrong[1]` | slip two = 2: `c` copies `b`, which is also an owner of the same order. Count all three. | correct | check l9.s6.use-count |
| `screens[6].hints[0]` | Each copy of a `shared_ptr` is one more owner. | correct | check l9.s6.use-count |
| `screens[6].hints[1]` | `b` copies `a`; `c` copies `b`. | correct | check l9.s6.use-count |
| `screens[6].hints[2]` | `a`, `b` and `c` share one order, so the count is 3. At the `}`, `b` and `c` die and it drops back to 1. | correct | check l9.s6.use-count |
| `screens[6].feedback.correct` | Three owners, one order. | correct | check l9.s6.use-count |
| `screens[6].explain.text` | `a`, `b` and `c` own the same order, so `use_count()` is 3. At the `}` the count falls to 1, and the order is… | correct | check l9.s6.use-count |
| `screens[7].prose` | Two nodes that own each other, as in a book linked to its strategy and back. ```cpp struct Node { std::shared… | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].canvas` | canvas (graph): {"height": 240, "nodeRadius": 20, "nodes": [{"id": "a", "label": "a", "x": 0.12, "y": 0.2, "s… | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].widget.options[0]` | KEY: What does it print? -> `end of main` only | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].widget.options[1]` | not: `freed`, `freed`, `end of main` / why: You expected smart pointers to free everything. When `a` and `b` … | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].widget.options[2]` | not: `freed`, `end of main` / why: Neither node can go first: each keeps the other's count at 1. | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].widget.options[3]` | not: It crashes at the closing brace / why: Nothing is deleted at all, so nothing crashes. The nodes simply s… | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].hints[0]` | At the inner `}`, `a` and `b` die. What is each node's count then? | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].hints[1]` | Each node is still owned by the other's `other` member. | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].hints[2]` | Both counts drop from 2 to 1, never to 0. No destructor runs: the nodes leak. | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].feedback.correct` | A cycle keeps every count above 0. | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].feedback.byKey.both` | You expected smart pointers to free everything. Each node still owns the other, so neither count reaches 0. | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[7].explain.text` | When `a` and `b` die, each count drops to 1: the nodes own each other. No destructor runs, and LeakSanitizer … | correct | checks l9.s7.cycle, l9.s7.lsan |
| `screens[8].prose` | Build classes from members that own themselves, and write no cleanup at all. This is the **rule of zero**. ``… | correct | ISO C++17 (N4659) [class.dtor]/9 (members are destroyed after the destructor body); C++ Core Guidelines C.20 (rule of zero) |
| `screens[8].widget.options[0]` | KEY: What should `Desk`'s destructor do? -> Nothing: write no destructor at all | correct | ISO C++17 (N4659) [class.dtor]/9 (members are destroyed after the destructor body); C++ Core Guidelines C.20 (rule of zero) |
| `screens[8].widget.options[1]` | not: `delete pricer.get();` / why: The `unique_ptr` deletes the `Pricer` itself. A second `delete` would free… | correct | ISO C++17 (N4659) [class.dtor]/9 (members are destroyed after the destructor body); C++ Core Guidelines C.20 (rule of zero) |
| `screens[8].widget.options[2]` | not: Call `orders.clear()` / why: The vector's own destructor frees its elements. Clearing it first adds noth… | correct | ISO C++17 (N4659) [class.dtor]/9 (members are destroyed after the destructor body); C++ Core Guidelines C.20 (rule of zero) |
| `screens[8].feedback.correct` | Members clean up after themselves. | correct | ISO C++17 (N4659) [class.dtor]/9 (members are destroyed after the destructor body); C++ Core Guidelines C.20 (rule of zero) |
| `screens[8].explain.text` | Every member is RAII, so destroying a `Desk` destroys them, and they free their memory. No hand-written destr… | correct | ISO C++17 (N4659) [class.dtor]/9 (members are destroyed after the destructor body); C++ Core Guidelines C.20 (rule of zero) |
| `screens[9].prose` | `Position` prints `open` in its constructor and `close` in its destructor. ```cpp void hold(std::unique_ptr<P… | correct | checks l9.s9.param-lifetime, l9.s9.five-lines |
| `screens[9].widget.answer` | KEY order: `open VOD`: `make_unique` runs the constructor > `opened`: `main` owns the position > `hold 100`: … | correct | checks l9.s9.param-lifetime, l9.s9.five-lines |
| `screens[9].hints[0]` | Who owns the position after `std::move(p)`? | correct | checks l9.s9.param-lifetime, l9.s9.five-lines |
| `screens[9].hints[1]` | The owner that dies first runs the destructor. | correct | checks l9.s9.param-lifetime, l9.s9.five-lines |
| `screens[9].hints[2]` | Created, owned by `main`, moved into `hold`, destroyed at `hold`'s `}`, and `main`'s `p` is left null. | imprecise | check l9.s9.param-lifetime holds on this build only; ISO C++17 (N4659) [expr.call]/4 (implementation-defined; a desk g++ build destroys the parameter in the caller); finding 5 |
| `screens[9].feedback.correct` | Ownership moved, so the cleanup moved with it. | correct | checks l9.s9.param-lifetime, l9.s9.five-lines |
| `screens[9].explain.text` | After `std::move(p)`, `hold`'s parameter is the only owner, so the position closes at `hold`'s `}`, before `m… | imprecise | check l9.s9.param-lifetime holds on this build only; ISO C++17 (N4659) [expr.call]/4 (implementation-defined; a desk g++ build destroys the parameter in the caller); finding 5 |
| `screens[10].prose` | An order book holds live orders. Each order belongs to exactly one book. Strategies keep raw `Order*` pointer… | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `screens[10].widget.options[0]` | KEY: Which member should the book use? -> `std::vector<std::unique_ptr<Order>> orders;` | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `screens[10].widget.options[1]` | not: `std::vector<Order> orders;` / why: When the vector grows, it moves its elements to a new buffer, and ev… | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `screens[10].widget.options[2]` | not: `std::vector<std::shared_ptr<Order>> orders;` / why: Shared ownership blurs who cancels an order, and ev… | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `screens[10].widget.options[3]` | not: `std::vector<Order*> orders;` filled with `new` / why: Nothing owns these orders: every cancel path must… | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `screens[10].hints[0]` | Two needs: one owner per order, and a fixed address. | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `screens[10].hints[1]` | A `unique_ptr` keeps its object at one heap address, wherever the pointer itself moves. | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `screens[10].hints[2]` | `std::vector<std::unique_ptr<Order>>`: the book is the single owner, and each order stays put when the vector… | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `screens[10].feedback.correct` | One owner, fixed addresses, automatic cleanup. | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `screens[10].feedback.byKey.value` | A growing vector moves its elements, so raw pointers to them dangle. | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `screens[10].explain.text` | Each order lives at a fixed heap address owned by one `unique_ptr`, so growing the vector moves only the poin… | correct | ISO C++17 (N4659) [vector.capacity] (reallocation invalidates pointers to elements); C++ Core Guidelines R.20, R.21 |
| `quiz[0].prose` | ```cpp auto a = std::make_unique<double>(101.5); auto b = std::move(a); std::cout << (a == nullptr) << " " <<… | correct | check l9.q0.moved |
| `quiz[0].widget.options[0]` | KEY: What does it print? -> `1 101.5` | correct | check l9.q0.moved |
| `quiz[0].widget.options[1]` | not: `0 101.5` / why: `std::move(a)` hands the double over to `b` and leaves `a` empty, so `a == nullptr` is … | correct | check l9.q0.moved |
| `quiz[0].widget.options[2]` | not: It does not compile / why: Moving a `unique_ptr` is allowed; only copying is not. | correct | check l9.q0.moved |
| `quiz[0].feedback.correct` | A moved-from `unique_ptr` is null. | correct | check l9.q0.moved |
| `quiz[0].explain.text` | The move transfers ownership, so `b` owns 101.5 and `a` is null. Reading `*a` now would be a null dereference… | correct | check l9.q0.moved |
| `quiz[1].widget.options[0]` | KEY: `auto px = std::make_unique<double[]>(3);` How is the memory freed? -> Automatically with `delete[]` whe… | correct | check l9.q1.array |
| `quiz[1].widget.options[1]` | not: You must call `delete[] px.get();` / why: The `unique_ptr<double[]>` does that itself; a manual `delete[… | correct | check l9.q1.array |
| `quiz[1].widget.options[2]` | not: Automatically, but with plain `delete`, so it is a bug / why: The `[]` in the type makes the `unique_ptr… | correct | check l9.q1.array |
| `quiz[1].feedback.correct` | The array form uses `delete[]` for you. | correct | check l9.q1.array |
| `quiz[1].explain.text` | `std::unique_ptr<double[]>` owns an array, supports `px[i]` and frees with `delete[]`. A run set `px[2] = 101… | correct | check l9.q1.array |
| `quiz[2].prose` | ```cpp double quote_once(double spot) { Pricer* p = new Pricer; return p->price(spot); } ``` | correct | ISO C++17 (N4659) [basic.stc.dynamic]: a raw pointer going out of scope frees nothing; check l9.s3.fb-test-3 |
| `quiz[2].widget.options[0]` | KEY: What is wrong with this function? -> The `Pricer` is never deleted: a raw `new` with no owner leaks | correct | ISO C++17 (N4659) [basic.stc.dynamic]: a raw pointer going out of scope frees nothing; check l9.s3.fb-test-3 |
| `quiz[2].widget.options[1]` | not: `p` dangles after the return / why: `p` is never used after the return. The problem is the heap object i… | correct | ISO C++17 (N4659) [basic.stc.dynamic]: a raw pointer going out of scope frees nothing; check l9.s3.fb-test-3 |
| `quiz[2].widget.options[2]` | not: Nothing: the memory is freed when `p` goes out of scope / why: A raw pointer going out of scope frees no… | correct | ISO C++17 (N4659) [basic.stc.dynamic]: a raw pointer going out of scope frees nothing; check l9.s3.fb-test-3 |
| `quiz[2].feedback.correct` | Raw pointers do not own. | correct | ISO C++17 (N4659) [basic.stc.dynamic]: a raw pointer going out of scope frees nothing; check l9.s3.fb-test-3 |
| `quiz[2].explain.text` | `p` dies at the `}`, but a raw pointer's death does nothing to its target. Every call leaks one `Pricer`. `au… | correct | ISO C++17 (N4659) [basic.stc.dynamic]: a raw pointer going out of scope frees nothing; check l9.s3.fb-test-3 |
| `quiz[3].prose` | ```cpp std::vector<std::unique_ptr<Order>> book; auto o = std::make_unique<Order>(); book.push_back(o); ``` | correct | check l9.q3.push-back |
| `quiz[3].widget.options[0]` | KEY: Why does `book.push_back(o);` fail to compile? -> It would copy the `unique_ptr`; write `book.push_back(… | correct | check l9.q3.push-back |
| `quiz[3].widget.options[1]` | not: A vector cannot hold `unique_ptr`s / why: Vectors of `unique_ptr` are common. They only refuse copies. | correct | check l9.q3.push-back |
| `quiz[3].widget.options[2]` | not: `o` might be null / why: The compiler does not track nulls. The error is "call to implicitly-deleted cop… | correct | check l9.q3.push-back |
| `quiz[3].feedback.correct` | Move it in. | correct | check l9.q3.push-back |
| `quiz[3].explain.text` | `push_back(o)` copies its argument, and a `unique_ptr` has no copy. `std::move(o)` moves the order into the v… | correct | check l9.q3.push-back |
| `summary.ideas[0]` | RAII: an object acquires a resource in its constructor and releases it in its destructor. The destructor runs… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | `std::unique_ptr<T>` is the single owner of one heap object. Create it with `std::make_unique`; it cannot be … | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | `std::shared_ptr` counts owners and frees at zero, but cycles never reach zero and the counting costs time. T… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \texttt{new T} \quad\Rightarrow\quad \texttt{std::make\_unique<T>()}, \qquad \texttt{T* = new T[n]} \quad\Rig… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | Smart pointers do not make leaks impossible: two `shared_ptr`s that own each other are never freed. | correct | restates the lesson: see the rows of the screens it summarises |

## l10-invariants.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A quote's bid must stay below its ask. In Python, any code may set `q.bid` to anything. Here is a C++ `struct… | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].canvas` | canvas (table): {"columns": ["member", "value"], "rows": [["`q.bid`", "100.2"], ["`q.ask`", "100.4"]], "align… | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].widget.options[0]` | KEY: What does the last line print? -> `-0.2` | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].widget.options[1]` | not: A compile error, because the bid is now above the ask / why: You expected the compiler to know the rule.… | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].widget.options[2]` | not: `0.2` / why: You used the old bid. The line before set `q.bid` to 100.6, so the ask minus the bid is neg… | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].widget.options[3]` | not: The program stops when it runs / why: Nothing checks the values at run time either. A struct stores what… | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].hints[0]` | Which value does `q.bid` hold when the last line runs? | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].hints[1]` | The assignment changed this cell. | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].hints[2]` | The ask is 100.4 and the bid is now 100.6: 100.4 − 100.6. | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].feedback.correct` | The quote is now crossed, and nothing objected. | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].feedback.byKey.compile` | You expected the compiler to know the rule. It checks types only, and 100.6 is a valid `double`. | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[0].explain.text` | Every member of a `struct` is open to any code, as in Python. The typo made a quote whose bid is above its as… | correct | checks l10.s0.crossed, l10.s0.struct |
| `screens[1].prose` | Suppose a type could hide some members from outside code. Here are the members of a better `Quote`. `set_bid(… | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].canvas` | canvas (boxes): {"itemKind": "card", "containers": [{"id": "members", "label": "Members of Quote", "kind": "b… | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].widget.answer` | KEY: {"inside": ["bid", "ask"], "outside": ["mid", "spread", "setbid"]} | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].hints[0]` | Which members, if anyone could write them, would let outside code skip the check? | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].hints[1]` | These two hold the numbers the rule is about. | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].hints[2]` | Hide `bid_` and `ask_`. Leave the three functions open: two only read, and `set_bid` checks. | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].feedback.correct` | Data hidden, checked functions open. | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].feedback.byKey.bid` | If any code can write `bid_`, it can set 100.6 and skip every check. Keep it where only `Quote`'s functions r… | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].feedback.byKey.ask` | If any code can write `ask_`, it can drop it below the bid. Keep it where only `Quote`'s functions reach it. | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].feedback.byKey.mid` | `mid()` only reads. Hiding it protects nothing and stops everyone from using the quote. | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].feedback.byKey.spread` | `spread()` only reads. Hiding it protects nothing and stops everyone from using the quote. | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].feedback.byKey.setbid` | `set_bid` checks before it stores, so outside code may call it. Hidden, nobody could ever move the bid. | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[1].explain.text` | You hid the data and left open the functions that read or check. C++ calls the hidden part **private** and th… | correct | derivation: only members that are written need hiding; ISO C++17 (N4659) [class.access] |
| `screens[2].prose` | Here is that split in C++. A **class** marks its sections `public:` and `private:`. A `struct` is the same th… | correct | check l10.s2.private |
| `screens[2].canvas` | canvas (pair): {"left": {"kind": "console", "params": {"title": "main.cpp", "lines": ["class Quote {", "publi… | correct | check l10.s2.private |
| `screens[2].widget.options[0]` | KEY: What did the compiler refuse? -> Code outside the class writing a private member | correct | check l10.s2.private |
| `screens[2].widget.options[1]` | not: Storing a bid above the ask / why: You expected a check on the value. The compiler refused the name `bid… | correct | check l10.s2.private |
| `screens[2].widget.options[2]` | not: Putting `public:` before `private:` / why: The sections can come in any order. The error line names a pr… | correct | check l10.s2.private |
| `screens[2].widget.options[3]` | not: Using `class` instead of `struct` / why: Both are allowed. The error is about who may name `bid_`. | correct | check l10.s2.private |
| `screens[2].hints[0]` | Read the first `error:` line in the terminal. | correct | check l10.s2.private |
| `screens[2].hints[1]` | It names the member and the class. | correct | check l10.s2.private |
| `screens[2].hints[2]` | `'bid_' is a private member of 'Quote'`: line 12 is outside the class, so it may not name `bid_`. | correct | check l10.s2.private |
| `screens[2].feedback.correct` | The rule is about names: outside code may not name `bid_`. | correct | check l10.s2.private |
| `screens[2].feedback.byKey.value` | You expected a check on the value. The compiler refused the name `bid_` before looking at any number. | correct | check l10.s2.private |
| `screens[2].explain.text` | Line 12 is in `main`, outside `Quote`, so it may not name a private member. Python has no such check: `q._bid… | correct | check l10.s2.private |
| `screens[3].prose` | Now write the class. The **initialiser list**, `: bid_(bid), ask_(ask)`, builds each member before the body r… | correct | checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[3].canvas` | canvas (console): {"lines": ["Quote q(100.2, 100.4);", "q.mid() // 100.3", "q.spread() // 0.2", "Quote(100.0,… | correct | checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[3].widget.solution` | code: Write the constructor's check, `double mid() const` and `double spread() const`. A failed check may `th… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[3].hints[0]` | Put the check in the constructor's body, after the list has built the members. | correct | checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[3].hints[1]` | A locked quote, bid equal to ask, must stop the program too. | correct | checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[3].hints[2]` | `if (bid_ >= ask_) throw std::invalid_argument("bid must be below ask");` then `double mid() const { return (… | correct | checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[3].feedback.correct` | Every `Quote` that exists now has its bid below its ask. | correct | checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[3].feedback.byKey.compile` | The compiler stopped. If the message says a function is not marked const, add `const` after its brackets. If … | correct | checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[3].feedback.byKey.test-4` | Test 4 builds a quote with the bid above the ask, and your program carried on. Check in the constructor body. | correct | checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[3].feedback.byKey.test-5` | Test 5 builds a quote with the bid equal to the ask. Refuse it too: use `>=` in the check, not `>`. | correct | checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[3].explain.text` | The list builds `bid_` and `ask_`; the body refuses a crossed or locked quote before anyone can use it. `mid`… | correct | checks l10.s3.fb-test-4, l10.s3.fb-test-5, l10.s3.abort |
| `screens[4].prose` | A `Position` holds a quantity of shares and their **average price**. You hold 100 shares bought at £10.00, th… | correct | check l10.s4.avg |
| `screens[4].canvas` | canvas (table): {"columns": ["fill", "shares", "price"], "rows": [["buy", "100", "£10.00"], ["buy", "300", "£… | correct | check l10.s4.avg |
| `screens[4].widget.answer` | KEY: What is the average price of the 400 shares, in pounds? -> 11.5 (£11.50: $(100 \times 10 + 300 \times 12… | correct | check l10.s4.avg |
| `screens[4].widget.wrong[0]` | slip simple = 11.0: You averaged the two prices. Three times as many shares were bought at £12.00, so they pu… | correct | check l10.s4.avg |
| `screens[4].widget.wrong[1]` | slip last = 12.0: That is the price of the last buy. The first 100 shares still cost £10.00. | correct | check l10.s4.avg |
| `screens[4].hints[0]` | What did the 400 shares cost in total? | correct | check l10.s4.avg |
| `screens[4].hints[1]` | 300 of the 400 shares cost £12.00 each. | correct | check l10.s4.avg |
| `screens[4].hints[2]` | Total cost $100 \times 10 + 300 \times 12 = 4600$, over 400 shares. | correct | check l10.s4.avg |
| `screens[4].feedback.correct` | £4,600 over 400 shares is £11.50. | correct | check l10.s4.avg |
| `screens[4].explain.text` | You weighted each price by its shares: $4600 / 400 = 11.5$. The quantity and the average change together on e… | correct | check l10.s4.avg |
| `screens[5].prose` | Now let the class keep the two numbers consistent. A buy moves the average; a sale does not. This desk forbid… | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].canvas` | canvas (table): {"columns": ["step", "qty after", "average after"], "rows": [["buy 100 at £10.00", "100", "£1… | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].widget.solution` | code: Write `buy(int qty, double px)` and `sell(int qty)` to match the table. Refuse a buy of 0 or fewer shar… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].hints[0]` | Update the average before you add to `qty_`: the formula needs the old quantity. | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].hints[1]` | The last row sells 1 share of none. | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].hints[2]` | `avg_ = (qty_ * avg_ + qty * px) / (qty_ + qty); qty_ += qty;` In `sell`, check, subtract, and reset `avg_` w… | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].feedback.correct` | Quantity and average now move together, and never go short. | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].feedback.byKey.test-2` | Test 2 expects £11.50. Weight each price by its shares, and use `qty_` before you add the new shares. | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].feedback.byKey.test-4` | Test 4 sells 150 shares and expects the average to stay £11.50. A sale changes only the quantity. | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].feedback.byKey.test-6` | Test 6 sells everything. Set the average back to 0 when the quantity reaches 0. | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].feedback.byKey.test-8` | Test 8 sells 101 of 100 shares. Refuse before you change `qty_`. | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].feedback.byKey.test-9` | Test 9 buys 0 shares. Without a check the average becomes $0/0$, which is NaN. | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[5].explain.text` | `buy` updates the average from the old quantity, then the quantity. `sell` refuses a short before changing an… | correct | checks l10.s5.fb-test-2, l10.s5.fb-test-4, l10.s5.fb-test-6, l10.s5.fb-test-8, l10.s5.fb-test-9, l10.s5.nan; average-cost method: a sale leaves the average unchanged (derivation: q*avg removed in proportion) |
| `screens[6].prose` | A risk limit should never change once it is set, so its member is `const`. This constructor sets it in the bo… | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].canvas` | canvas (pair): {"left": {"kind": "console", "params": {"title": "main.cpp", "lines": ["class Limit {", "publi… | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].widget.options[0]` | KEY: Which constructor compiles? -> `Limit(double m) : max_(m) {}` | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].widget.options[1]` | not: `Limit(double m) { max_ = m; }` / why: That is the code that failed. By the time the body runs, `max_` a… | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].widget.options[2]` | not: `Limit(double m) { this->max_ = m; }` / why: `this->max_` is the same member. It is still an assignment … | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].widget.options[3]` | not: `Limit(double m) { const double max_ = m; }` / why: That makes a new local variable that hides the membe… | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].hints[0]` | When does the body of a constructor run: before or after the members exist? | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].hints[1]` | The first error says the member must be explicitly initialised. | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].hints[2]` | Members are built in the initialiser list, before the body. A `const` member can only get its value there. | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].feedback.correct` | The list builds `max_` with its value, once. | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].feedback.byKey.body` | That is the code that failed. By the time the body runs, `max_` already exists, and a `const` cannot be assig… | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[6].explain.text` | The list builds each member with its value; the body runs after that. Assigning in the body builds the member… | correct | checks l10.s6.const-member, l10.s6.list, l10.s6.this, l10.s6.local |
| `screens[7].prose` | This `Quote` checks its constructor and keeps its data private. A colleague adds a setter. | correct | check l10.s7.setter |
| `screens[7].canvas` | canvas (console): {"lines": ["class Quote {", "public:", " Quote(double bid, double ask) : bid_(bid), ask_(as… | correct | check l10.s7.setter |
| `screens[7].widget.options[0]` | KEY: What does the program print? -> `-0.2` | correct | check l10.s7.setter |
| `screens[7].widget.options[1]` | not: Nothing: it stops, because the constructor checks the bid / why: You expected the constructor's check to… | correct | check l10.s7.setter |
| `screens[7].widget.options[2]` | not: A compile error, because `bid_` is private / why: `set_bid` is a member function, so it may write `bid_`… | correct | check l10.s7.setter |
| `screens[7].widget.options[3]` | not: `0.2` / why: `set_bid` did store 100.6. The spread is 100.4 − 100.6. | correct | check l10.s7.setter |
| `screens[7].hints[0]` | When does the constructor's check run? | correct | check l10.s7.setter |
| `screens[7].hints[1]` | This line changes `bid_`. Does it check anything? | correct | check l10.s7.setter |
| `screens[7].hints[2]` | The check ran once, on line 14. Line 15 calls `set_bid`, which stores 100.6 straight away. | correct | check l10.s7.setter |
| `screens[7].feedback.correct` | A private member is only as safe as the functions that write it. | correct | check l10.s7.setter |
| `screens[7].feedback.byKey.ctor` | You expected the constructor's check to guard every change. It runs once, when `q` is built; `set_bid` stores… | correct | check l10.s7.setter |
| `screens[7].explain.text` | The constructor checks once. Every function that changes the data must check again, or it is a way round the … | correct | check l10.s7.setter |
| `screens[8].prose` | Bid below ask, and never short: each is an **invariant**. It is a fact about the members that holds whenever … | correct | ISO C++17 (N4659) [class.mfct.non-static]/5, [dcl.type.cv]: a const member function cannot modify members; check l10.s7.setter |
| `screens[8].widget.options[0]` | KEY: Which member function of `Quote` can safely skip the check? -> `double spread() const` | correct | ISO C++17 (N4659) [class.mfct.non-static]/5, [dcl.type.cv]: a const member function cannot modify members; check l10.s7.setter |
| `screens[8].widget.options[1]` | not: `void set_ask(double a)` / why: It changes `ask_`, so it could drop the ask below the bid. It must check. | correct | ISO C++17 (N4659) [class.mfct.non-static]/5, [dcl.type.cv]: a const member function cannot modify members; check l10.s7.setter |
| `screens[8].widget.options[2]` | not: `void widen(double d)`, which subtracts `d` from the bid and adds it to the ask / why: With a negative `… | correct | ISO C++17 (N4659) [class.mfct.non-static]/5, [dcl.type.cv]: a const member function cannot modify members; check l10.s7.setter |
| `screens[8].widget.options[3]` | not: The constructor `Quote(double b, double a)` / why: The constructor is the first place the rule can break… | correct | ISO C++17 (N4659) [class.mfct.non-static]/5, [dcl.type.cv]: a const member function cannot modify members; check l10.s7.setter |
| `screens[8].hints[0]` | Which function cannot change `bid_` or `ask_` at all? | correct | ISO C++17 (N4659) [class.mfct.non-static]/5, [dcl.type.cv]: a const member function cannot modify members; check l10.s7.setter |
| `screens[8].hints[1]` | `const` after the brackets means the function cannot change the members, so the invariant still holds when it… | correct | ISO C++17 (N4659) [class.mfct.non-static]/5, [dcl.type.cv]: a const member function cannot modify members; check l10.s7.setter |
| `screens[8].feedback.correct` | A `const` function cannot change the members, so it cannot break the rule. | correct | ISO C++17 (N4659) [class.mfct.non-static]/5, [dcl.type.cv]: a const member function cannot modify members; check l10.s7.setter |
| `screens[8].explain.text` | `spread() const` only reads, so the invariant holds after it as before. Every other function on the list chan… | correct | ISO C++17 (N4659) [class.mfct.non-static]/5, [dcl.type.cv]: a const member function cannot modify members; check l10.s7.setter |
| `screens[9].prose` | An order moves through states. It is `new` while it has shares left, even when partly filled, and `filled` wh… | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].canvas` | canvas (graph): {"nodes": [{"id": "new", "label": "new", "x": 0.25, "y": 0.5, "shape": "pill"}, {"id": "fille… | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].widget.solution` | code: Write the constructor's check (quantity above 0), `fill(int q)` and `cancel()`. Refuse a fill or cancel… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].hints[0]` | Each function that changes the order checks its state first. | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].hints[1]` | Only `new` has arrows leaving it. | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].hints[2]` | In `fill`: refuse unless `state_ == State::New`, refuse `q <= 0` or `filled_ + q > qty_`, add, then set `Stat… | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].feedback.correct` | The order's states only move along the arrows. | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].feedback.byKey.test-4` | Test 4 fills 40 then 60 of 100 and expects `filled`. Change the state when nothing remains. | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].feedback.byKey.test-7` | Test 7 fills a cancelled order. Check the state before you add to `filled_`. | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].feedback.byKey.test-8` | Test 8 fills 70 then 40 of 100. Refuse a fill larger than what remains. | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].feedback.byKey.test-9` | Test 9 cancels a filled order. `cancel` must check the state too. | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `screens[9].explain.text` | Each changing function checks the state first, so the only moves are the arrows from `new`. The fill check al… | correct | checks l10.s9.fb-test-4, l10.s9.fb-test-7, l10.s9.fb-test-8, l10.s9.fb-test-9 |
| `quiz[0].prose` | ```cpp class Quote { public: Quote(double b, double a) : bid_(b), ask_(a) { if (bid_ >= ask_) throw std::inva… | correct | check l10.q0.ref-getter |
| `quiz[0].widget.options[0]` | KEY: What happens? -> It prints `-0.2` | correct | check l10.q0.ref-getter |
| `quiz[0].widget.options[1]` | not: A compile error: you cannot assign to a function call / why: `bid()` returns a `double&`, another name f… | correct | check l10.q0.ref-getter |
| `quiz[0].widget.options[2]` | not: It stops, because the constructor checks the bid / why: The constructor checked once, when `q` was built… | correct | check l10.q0.ref-getter |
| `quiz[0].widget.options[3]` | not: It prints `0.2`, because `bid()` hands out a copy / why: A copy would need the return type `double`. Wit… | correct | check l10.q0.ref-getter |
| `quiz[0].feedback.correct` | A non-const reference is an open door to private data. | correct | check l10.q0.ref-getter |
| `quiz[0].explain.text` | `double& bid()` returns a reference to the private member, so `q.bid() = 100.6` writes it directly. Return `d… | correct | check l10.q0.ref-getter |
| `quiz[1].prose` | The same class in Python, with the usual underscore for private data: ```python class Quote: def __init__(sel… | correct | check l10.s0.crossed (Python prints -0.19999999999998863); Python tutorial 9.6 (underscore is a convention) |
| `quiz[1].widget.options[0]` | KEY: What happens? -> It prints `-0.19999999999998863` | correct | check l10.s0.crossed (Python prints -0.19999999999998863); Python tutorial 9.6 (underscore is a convention) |
| `quiz[1].widget.options[1]` | not: `AttributeError`, because `_bid` is private / why: The underscore is a convention for readers. Python le… | correct | check l10.s0.crossed (Python prints -0.19999999999998863); Python tutorial 9.6 (underscore is a convention) |
| `quiz[1].widget.options[2]` | not: `ValueError: crossed` / why: `__init__` checked once, when `q` was built. The assignment afterwards runs… | correct | check l10.s0.crossed (Python prints -0.19999999999998863); Python tutorial 9.6 (underscore is a convention) |
| `quiz[1].widget.options[3]` | not: It prints `-0.2` / why: Python prints a float's full shortest repr, so the binary error shows: `-0.19999… | correct | check l10.s0.crossed (Python prints -0.19999999999998863); Python tutorial 9.6 (underscore is a convention) |
| `quiz[1].feedback.correct` | Python trusts the caller; C++ `private` does not. | correct | check l10.s0.crossed (Python prints -0.19999999999998863); Python tutorial 9.6 (underscore is a convention) |
| `quiz[1].explain.text` | In Python `_bid` only signals "leave this alone"; the assignment runs. C++ `private` is checked by the compil… | correct | check l10.s0.crossed (Python prints -0.19999999999998863); Python tutorial 9.6 (underscore is a convention) |
| `quiz[2].prose` | ```cpp class Quote { public: Quote(double b, double a) : bid_(b), ask_(a) {} double spread() { return ask_ - … | correct | check l10.q2.not-const |
| `quiz[2].widget.options[0]` | KEY: What is the right fix? -> Write `double spread() const` | correct | check l10.q2.not-const |
| `quiz[2].widget.options[1]` | not: Take `Quote& q` in `width` instead / why: That compiles, but now `width` could change the quote, and it … | correct | check l10.q2.not-const |
| `quiz[2].widget.options[2]` | not: Make `bid_` and `ask_` public / why: The error is about a promise not to change the object, not about ac… | correct | check l10.q2.not-const |
| `quiz[2].widget.options[3]` | not: Take `Quote q` by value in `width` / why: That compiles by copying the quote on every call. The real gap… | correct | check l10.q2.not-const |
| `quiz[2].feedback.correct` | A reader should say it only reads. | correct | check l10.q2.not-const |
| `quiz[2].explain.text` | A `const Quote&` may call only `const` functions, since only they promise not to change it. `spread` only rea… | correct | check l10.q2.not-const |
| `quiz[3].prose` | A position holds 200 shares at £5.00. You buy 50 at £6.00, then sell 100. | correct | check l10.s4.avg |
| `quiz[3].widget.answer` | KEY: What is the average price after the sale, in pounds? -> 5.2 (£5.20: $(200 \times 5 + 50 \times 6) / 250$… | correct | check l10.s4.avg |
| `quiz[3].widget.wrong[0]` | slip simple = 5.5: You averaged £5.00 and £6.00. Four times as many shares cost £5.00. | correct | check l10.s4.avg |
| `quiz[3].widget.wrong[1]` | slip sold = 6.0: That is the last buy's price. The average covers all 250 shares bought. | correct | check l10.s4.avg |
| `quiz[3].feedback.correct` | £1,300 over 250 shares is £5.20, and selling leaves it there. | correct | check l10.s4.avg |
| `quiz[3].explain.text` | The buys give $(1000 + 300) / 250 = 5.2$. Selling 100 shares leaves 150 at the same average cost, £5.20. | correct | check l10.s4.avg |
| `summary.ideas[0]` | A `class` keeps its data `private`, so only its own member functions can change it. Python's `_name` is only … | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | An invariant is checked in the constructor and again in every function that changes the data. Functions that … | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | Members are built in the initialiser list, before the constructor's body runs. A `const` member can only get … | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \bar p_{\text{new}} = \dfrac{q\,\bar p + q_b\,p_b}{q + q_b} / A buy of $q_b$ shares at $p_b$ moves the averag… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | A setter that stores without checking lets outside code break the invariant the constructor checked. So does … | correct | restates the lesson: see the rows of the screens it summarises |

## l11-creation-destruction.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A **destructor**, written `~Logger()`, runs when an object is destroyed. This `Logger` prints when it is made… | correct | check l11.s0.lifo |
| `screens[0].canvas` | canvas (console): {"lines": ["int main() {", " Logger a(\"a\");", " Logger b(\"b\");", " std::cout << \"work\… | correct | check l11.s0.lifo |
| `screens[0].widget.answer` | KEY order: `open a` > `open b` > `work` > `close b` > `close a` | correct | check l11.s0.lifo |
| `screens[0].hints[0]` | Both objects live until the closing brace of `main`. | correct | check l11.s0.lifo |
| `screens[0].hints[1]` | At this brace both are destroyed, one after the other. | correct | check l11.s0.lifo |
| `screens[0].hints[2]` | They go in reverse order of construction: `b` was built last, so it closes first. | correct | check l11.s0.lifo |
| `screens[0].feedback.correct` | Built a, b; destroyed b, a. | correct | check l11.s0.lifo |
| `screens[0].feedback.byKey.ca` | You closed `a` first. Objects are destroyed in reverse order: `b` was built last, so it closes first. `b` mig… | correct | check l11.s0.lifo |
| `screens[0].feedback.byKey.w` | `work` prints while both objects are alive, before the closing brace. | correct | check l11.s0.lifo |
| `screens[0].feedback.byKey.cb` | Nothing closes until `main` reaches its closing brace, after `work`. | correct | check l11.s0.lifo |
| `screens[0].explain.text` | Objects are destroyed in reverse order of construction, like plates off a stack. `b` may depend on `a`, so `a… | correct | check l11.s0.lifo |
| `screens[1].prose` | Braces make a **scope**: a block where names live. Here `b` is declared inside an inner pair of braces. Same … | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].canvas` | canvas (console): {"lines": ["int main() {", " Logger a(\"a\");", " {", " Logger b(\"b\");", " std::cout << \… | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].widget.answer` | KEY: Tap the line where `b`'s destructor runs. -> ["l6"] | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].hints[0]` | Which braces enclose the line that declares `b`? | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].hints[1]` | `b` is declared here. | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].hints[2]` | `b` lives until the closing brace of the block it was declared in. | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].feedback.correct` | `b` dies at the end of its scope, line 6. | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].feedback.byKey.l5` | That is the last line that uses `b`. C++ does not track uses: `b` lives until its scope's closing brace. | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].feedback.byKey.l8` | That brace ends `a` and `c`. `b` was declared in the inner block, which ends earlier. | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].feedback.byKey.l4` | That line builds `b`. Its destructor runs when its scope ends. | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].feedback.byKey.l7` | By line 7 the inner block has already ended, so `b` is gone. | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[1].explain.text` | An object on the stack lives until the closing brace of its scope. So `b` closes on line 6, before `c` is eve… | correct | ISO C++17 (N4659) [basic.stc.auto], [stmt.dcl]; check l11.s2.scopes |
| `screens[2].prose` | Same program. `c` is built and never used. | correct | check l11.s2.scopes |
| `screens[2].canvas` | canvas (console): {"lines": ["int main() {", " Logger a(\"a\");", " {", " Logger b(\"b\");", " std::cout << \… | correct | check l11.s2.scopes |
| `screens[2].widget.answer` | KEY order: `open a` > `open b` > `work` > `close b` > `open c` > `close c` > `close a` | correct | check l11.s2.scopes |
| `screens[2].hints[0]` | Walk the lines from top to bottom, printing as each object starts and ends. | correct | check l11.s2.scopes |
| `screens[2].hints[1]` | Line 6 ends the inner scope. | correct | check l11.s2.scopes |
| `screens[2].hints[2]` | a, b, work, close b at line 6, then c, and at line 8 close c before close a. | correct | check l11.s2.scopes |
| `screens[2].feedback.correct` | Each brace ends what it owns, newest first. | correct | check l11.s2.scopes |
| `screens[2].feedback.byKey.oc` | `c` is built on line 7, after the inner scope has closed `b`. | correct | check l11.s2.scopes |
| `screens[2].feedback.byKey.ca` | At the last brace both `a` and `c` are alive. `c` was built later, so it closes first. | correct | check l11.s2.scopes |
| `screens[2].feedback.byKey.cb` | `b` closes at line 6, before `c` exists. | correct | check l11.s2.scopes |
| `screens[2].feedback.byKey.cc` | `c` is never used, but it is still an object. Its destructor runs at the end of `main`, before `a`'s. | correct | check l11.s2.scopes |
| `screens[2].explain.text` | Line 6 closes `b`. At line 8 `c` and `a` are both alive, so they close newest first. `c` was never used, yet … | correct | check l11.s2.scopes |
| `screens[3].prose` | Now write `Logger` yourself and make a program produce that shape. It reads three names. The first lives for … | correct | widget run: solution passes, starter fails; check l11.s2.scopes |
| `screens[3].canvas` | canvas (console): {"lines": ["$ ./main", "feed book risk", "open feed", "open book", "work", "close book", "o… | correct | widget run: solution passes, starter fails; check l11.s2.scopes |
| `screens[3].widget.solution` | code: Write the constructor and destructor of `Logger`, then `main`. (4 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; widget run: solution passes, starter fails; check l11.s2.scopes |
| `screens[3].hints[0]` | The constructor prints `open` and the name; `~Logger()` prints `close` and the name. | correct | widget run: solution passes, starter fails; check l11.s2.scopes |
| `screens[3].hints[1]` | This line comes from the destructor of the first logger. | correct | widget run: solution passes, starter fails; check l11.s2.scopes |
| `screens[3].hints[2]` | In `main`: `Logger first(x);` then `{ Logger second(y); std::cout << "work\n"; }` then `Logger third(z);`. | correct | widget run: solution passes, starter fails; check l11.s2.scopes |
| `screens[3].feedback.correct` | The braces alone decide when each `close` prints. | correct | widget run: solution passes, starter fails; check l11.s2.scopes |
| `screens[3].feedback.byKey.compile` | The compiler stopped. Check that the destructor is spelt `~Logger()`, with no return type and no arguments. | correct | widget run: solution passes, starter fails; check l11.s2.scopes |
| `screens[3].feedback.byKey.test-1` | Compare the order of your `close` lines with the expected output. An inner pair of braces must end before `th… | correct | widget run: solution passes, starter fails; check l11.s2.scopes |
| `screens[3].explain.text` | You never call a destructor yourself. The inner braces end `second`, and the end of `main` ends `third`, then… | correct | widget run: solution passes, starter fails; check l11.s2.scopes |
| `screens[4].prose` | Members are built in the order they are **declared** in the class, whatever order the initialiser list names … | correct | check l11.s4.reorder |
| `screens[4].canvas` | canvas (pair): {"left": {"kind": "console", "params": {"title": "main.cpp", "lines": ["#include <vector>", ""… | correct | check l11.s4.reorder |
| `screens[4].widget.options[0]` | KEY: `Window w(20)` runs. What size does `data_` get? -> Unpredictable: `n_` is read before it is set | correct | check l11.s4.reorder |
| `screens[4].widget.options[1]` | not: 20 / why: You read the list left to right. `data_` is declared first, so it is built first, from an `n_`… | correct | check l11.s4.reorder |
| `screens[4].widget.options[2]` | not: 0, because `n_` starts at zero / why: An `int` member is not zeroed. Reading it before it is set is unde… | correct | check l11.s4.reorder |
| `screens[4].widget.options[3]` | not: A compile error / why: These are warnings: the program builds. That is why they are worth reading. | correct | check l11.s4.reorder |
| `screens[4].hints[0]` | Which member is declared first, on lines 7 and 8? | correct | check l11.s4.reorder |
| `screens[4].hints[1]` | The second warning names the exact problem. | correct | check l11.s4.reorder |
| `screens[4].hints[2]` | `data_` is built first, using `n_`, which is built second. | correct | check l11.s4.reorder |
| `screens[4].feedback.correct` | `data_` is built first, from an `n_` that holds garbage. | correct | check l11.s4.reorder |
| `screens[4].feedback.byKey.twenty` | You read the list left to right. `data_` is declared first, so it is built first, from an `n_` not yet set. | correct | check l11.s4.reorder |
| `screens[4].explain.text` | Declaration order decides, so `data_(n_, 0.0)` reads `n_` before `n_(n)` runs. Build `data_` from the paramet… | correct | check l11.s4.reorder |
| `screens[5].prose` | Same `Logger`. Now one is made from another. ```cpp int main() { Logger a("a"); Logger b = a; } ``` | correct | check l11.s5.copy |
| `screens[5].canvas` | canvas (graph): {"nodes": [{"id": "a", "label": "a: \"a\"", "x": 0.2, "y": 0.5, "shape": "rect"}, {"id": "b",… | correct | check l11.s5.copy |
| `screens[5].widget.answer` | KEY: How many lines of output start with `close`? -> 2 (2: `open a`, `close a`, `close a`.) | correct | check l11.s5.copy |
| `screens[5].widget.wrong[0]` | slip one = 1: You counted one object because only one constructor printed. `b` was built by a constructor tha… | correct | check l11.s5.copy |
| `screens[5].widget.wrong[1]` | slip three = 3: Only two objects exist. The copy made `b`; it did not make a third. | correct | check l11.s5.copy |
| `screens[5].hints[0]` | How many `Logger` objects exist at the end of `main`? | correct | check l11.s5.copy |
| `screens[5].hints[1]` | `b` is a second object holding a copy of `a`'s name. | correct | check l11.s5.copy |
| `screens[5].hints[2]` | Two objects, two destructors. The copy itself printed nothing. | correct | check l11.s5.copy |
| `screens[5].feedback.correct` | Two objects, so two destructors: `close a` twice. | correct | check l11.s5.copy |
| `screens[5].explain.text` | `Logger b = a;` builds `b` with the **copy constructor**, `Logger(const Logger&)`. The compiler wrote one for… | correct | check l11.s5.copy |
| `screens[6].prose` | A class has four ways to fill an object from another. The **copy constructor** builds a new object. **Copy as… | correct | check l11.s6.which |
| `screens[6].canvas` | canvas (table): {"columns": ["line", "what runs"], "rows": [["`Buffer a(3, 1.5);`", "?"], ["`Buffer b = a;`",… | correct | check l11.s6.which |
| `screens[6].widget.answer` | KEY: Select all that apply: tap every line that runs the copy constructor. -> ["r1", "r2"] | correct | check l11.s6.which |
| `screens[6].hints[0]` | Does the line declare a new object, or change one that exists? | correct | check l11.s6.which |
| `screens[6].hints[1]` | On this line `b` already exists. | correct | check l11.s6.which |
| `screens[6].hints[2]` | Lines that declare a new `Buffer` from `a` build it: `Buffer b = a;` and `Buffer c(a);`. | correct | check l11.s6.which |
| `screens[6].feedback.correct` | A declaration builds; a plain `=` overwrites. | correct | check l11.s6.which |
| `screens[6].feedback.byKey.r3` | `b` already exists on this line, so `=` overwrites it: that is copy assignment, not construction. | correct | check l11.s6.which |
| `screens[6].feedback.byKey.r4` | `std::move(a)` lets the new object take `a`'s contents: the move constructor runs. | correct | check l11.s6.which |
| `screens[6].feedback.byKey.r5` | `c` exists and takes `b`'s contents: move assignment. | correct | check l11.s6.which |
| `screens[6].feedback.byKey.r0` | That builds a `Buffer` from two numbers: an ordinary constructor. | correct | check l11.s6.which |
| `screens[6].feedback.byKey.r1` | `Buffer b = a;` declares `b`, so it builds a new object. The `=` in a declaration is not assignment, unlike P… | correct | check l11.s6.which |
| `screens[6].explain.text` | A declaration always builds, even when it is written with `=`. Assignment needs an object that already exists… | correct | check l11.s6.which |
| `screens[7].prose` | A `std::vector` member already copies its doubles on a copy and hands over its heap block on a move. So the c… | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].canvas` | canvas (table): {"columns": ["line", "what runs"], "rows": [["`Buffer b = a;`", "copy: b gets its own doubles… | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].widget.solution` | code: Write `Buffer(int n, double x)` (n copies of x), `int size() const`, `double get(int i) const`, `void s… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].hints[0]` | Build `data_` in the initialiser list: `data_(n, x)`. | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].hints[1]` | After a move, the source is left empty. | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].hints[2]` | `Buffer(const Buffer&) = default;`, `Buffer(Buffer&&) = default;`, and `Buffer& operator=(const Buffer&) = de… | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].feedback.correct` | The vector did the work; you only asked for it. | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].feedback.byKey.test-2` | Test 2 changes `b` and reads `a`. A copy must not share doubles with its source. | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].feedback.byKey.test-5` | Test 5 reads `a.size()` after a move and expects 0. A moved vector leaves its source empty. | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].feedback.byKey.test-9` | Test 9 assigns one buffer to another. A declared move constructor deletes the copy assignment, so default it … | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].feedback.byKey.test-10` | Test 10 asks whether one `Buffer` can be move-assigned to another, and a deleted move assignment says no. Wri… | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].feedback.byKey.test-12` | Test 12 moves `a` into an existing buffer and expects `a` empty. Without a move assignment, `a` was copied. | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[7].explain.text` | A copy duplicates the doubles; a move passes the heap block over, so a million doubles cost one pointer swap.… | correct | checks l11.s7.fb-test-5, l11.s7.fb-test-9, l11.s7.fb-test-10, l11.s7.fb-test-12, l11.s7.moved-from |
| `screens[8].prose` | This class owns a heap block through a raw pointer, and frees it in its destructor. Then it is copied. ```cpp… | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].canvas` | canvas (graph): {"nodes": [{"id": "a", "label": "a", "x": 0.15, "y": 0.25, "shape": "pill"}, {"id": "b", "lab… | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].widget.options[0]` | KEY: What happens when `main` ends? -> Both destructors `delete[]` the same block: undefined behaviour, which… | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].widget.options[1]` | not: `b` has its own 100 doubles, so each destructor frees its own / why: You expected the copy to copy the d… | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].widget.options[2]` | not: A compile error: `Prices` has no copy constructor / why: The compiler writes one for you. It copies each… | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].widget.options[3]` | not: The block leaks, because nobody frees it / why: Each destructor frees it, so it is freed twice, not neve… | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].hints[0]` | What is the member that the default copy copies? | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].hints[1]` | Draw the arrow for `b` after the copy. | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].hints[2]` | `data_` is an address. `b` gets the same address, so two destructors free one block. | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].feedback.correct` | Copying a raw pointer copies an address, not the doubles. | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].feedback.byKey.deep` | You expected the copy to copy the doubles. The default copy constructor copies the member, a pointer, so both… | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[8].explain.text` | `b.data_` holds the same address as `a.data_`, so the block is freed twice. The fix is to own it with a membe… | correct | ISO C++17 (N4659) [class.copy.ctor]/14 (memberwise copy), [expr.delete]/2 (deleting twice is undefined) |
| `screens[9].prose` | Five **special members** decide how an object is copied, moved and destroyed. You choose between two patterns… | correct | C++ Core Guidelines C.20, C.21; ISO C++17 (N4659) [class.copy.ctor]/10; checks r3.i6.* |
| `screens[9].widget.options[0]` | KEY: A `Pricer` holds `std::string name_` and `std::unique_ptr<Lattice> grid_`. What do you write for copying… | correct | C++ Core Guidelines C.20, C.21; ISO C++17 (N4659) [class.copy.ctor]/10; checks r3.i6.* |
| `screens[9].widget.options[1]` | not: All five special members, by hand / why: That is for a class that owns a raw resource itself. Here every… | correct | C++ Core Guidelines C.20, C.21; ISO C++17 (N4659) [class.copy.ctor]/10; checks r3.i6.* |
| `screens[9].widget.options[2]` | not: A destructor that calls `delete grid_.get()` / why: `unique_ptr` already deletes the lattice. Deleting i… | correct | C++ Core Guidelines C.20, C.21; ISO C++17 (N4659) [class.copy.ctor]/10; checks r3.i6.* |
| `screens[9].widget.options[3]` | not: A copy constructor that copies the pointer / why: Two pricers would then share one lattice, and both wou… | correct | C++ Core Guidelines C.20, C.21; ISO C++17 (N4659) [class.copy.ctor]/10; checks r3.i6.* |
| `screens[9].hints[0]` | Does any member need help to be copied, moved or destroyed? | correct | C++ Core Guidelines C.20, C.21; ISO C++17 (N4659) [class.copy.ctor]/10; checks r3.i6.* |
| `screens[9].hints[1]` | `std::string` and `std::unique_ptr` each handle their own copying, moving and destruction. | correct | C++ Core Guidelines C.20, C.21; ISO C++17 (N4659) [class.copy.ctor]/10; checks r3.i6.* |
| `screens[9].feedback.correct` | Rule of zero: the members already do the right thing. | correct | C++ Core Guidelines C.20, C.21; ISO C++17 (N4659) [class.copy.ctor]/10; checks r3.i6.* |
| `screens[9].explain.text` | Self-managing members make the compiler's versions right: moves move, and the copy is deleted because `unique… | correct | C++ Core Guidelines C.20, C.21; ISO C++17 (N4659) [class.copy.ctor]/10; checks r3.i6.* |
| `screens[10].prose` | A market-data connection must disconnect exactly once, in its destructor. A copy would disconnect twice, so c… | correct | checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `screens[10].canvas` | canvas (graph): {"nodes": [{"id": "a", "label": "a", "x": 0.15, "y": 0.5, "shape": "pill"}, {"id": "b", "labe… | correct | checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `screens[10].widget.solution` | code: Write the destructor, delete copying, and write the move constructor so that each venue is disconnected… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `screens[10].hints[0]` | The destructor calls `disconnect(venue_)` only while `open_` is true. | correct | checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `screens[10].hints[1]` | After the move, `a` must be closed. | correct | checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `screens[10].hints[2]` | `Connection(Connection&& other) noexcept : venue_(std::move(other.venue_)), open_(other.open_) { other.open_ … | correct | checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `screens[10].feedback.correct` | One open connection, one disconnect, wherever it moves. | correct | checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `screens[10].feedback.byKey.test-2` | Test 2 moves `a` into `b`; both destructors run. Leave `other.open_` false in the move constructor. | correct | checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `screens[10].feedback.byKey.test-8` | Test 8 asks whether `Connection` can be copied. Write `Connection(const Connection&) = delete;`. | correct | checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `screens[10].feedback.byKey.test-1` | Test 1 builds one connection and expects one disconnect. Call `disconnect(venue_)` in `~Connection()` while i… | correct | checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `screens[10].explain.text` | The move constructor takes the venue and closes the source, so only one destructor disconnects. Deleting the … | correct | checks l11.s10.fb-test-2, l11.s10.fb-test-8, l11.s10.no-delete, l11.s10.fb-test-1 |
| `quiz[0].prose` | Same `Logger`, with `open` and `close` messages. ```cpp int main() { Logger("tmp"); std::cout << "next\n"; } … | correct | check l11.q0.temporary |
| `quiz[0].widget.options[0]` | KEY: What does it print? -> `open tmp`, `close tmp`, `next` | correct | check l11.q0.temporary |
| `quiz[0].widget.options[1]` | not: `open tmp`, `next`, `close tmp` / why: A temporary has no name, so it does not live to the end of the sc… | correct | check l11.q0.temporary |
| `quiz[0].widget.options[2]` | not: `next` only / why: The temporary is really built, so both its constructor and its destructor run. | correct | check l11.q0.temporary |
| `quiz[0].widget.options[3]` | not: `open tmp`, `next` / why: Every object that is built is destroyed. The temporary's destructor runs at th… | correct | check l11.q0.temporary |
| `quiz[0].feedback.correct` | A temporary dies at the end of its full expression. | correct | check l11.q0.temporary |
| `quiz[0].explain.text` | `Logger("tmp");` builds an unnamed object and destroys it at the semicolon. So `close tmp` prints before `nex… | correct | check l11.q0.temporary |
| `quiz[1].prose` | `Buffer` is the class you wrote, with default copy and move constructors. ```cpp const Buffer a(3, 1.5); Buff… | correct | check l11.q1.const-move |
| `quiz[1].widget.options[0]` | KEY: What does it print? -> `3` | correct | check l11.q1.const-move |
| `quiz[1].widget.options[1]` | not: `0` / why: `std::move` only casts. On a `const` object it gives `const Buffer&&`, which the move constru… | correct | check l11.q1.const-move |
| `quiz[1].widget.options[2]` | not: A compile error: you cannot move from a `const` object / why: It compiles. The copy constructor accepts … | correct | check l11.q1.const-move |
| `quiz[1].feedback.correct` | A `const` object cannot be moved from, so it is copied. | correct | check l11.q1.const-move |
| `quiz[1].explain.text` | A move empties its source, and `a` is `const`, so the copy constructor runs instead. `a` keeps its 3 doubles.… | correct | check l11.q1.const-move |
| `quiz[2].prose` | A pricer's lattice holds 500 doubles. `Lattice` has a copy constructor and a move constructor. ```cpp Lattice… | correct | check l11.q2.factory |
| `quiz[2].widget.options[0]` | KEY: How many times are the 500 doubles copied? -> 0 | correct | check l11.q2.factory |
| `quiz[2].widget.options[1]` | not: 1 / why: You expected `return grid;` to copy. A returned local is moved, or built straight into `g`. | correct | check l11.q2.factory |
| `quiz[2].widget.options[2]` | not: 2 / why: Neither the return nor `Lattice g = ...` copies. C++17 builds `g` straight from the returned va… | correct | check l11.q2.factory |
| `quiz[2].feedback.correct` | `return grid;` does not copy a movable local: it is built in place or moved. | correct | check l11.q2.factory |
| `quiz[2].explain.text` | The compiler usually builds `grid` directly in `g`'s place; if not, it moves it. Either way no double is copi… | correct | check l11.q2.factory |
| `quiz[3].prose` | ```cpp class Desk { Logger risk_; Logger feed_; public: Desk() : feed_("feed"), risk_("risk") {} }; int main(… | correct | check l11.q3.member-order |
| `quiz[3].widget.options[0]` | KEY: Which line prints first? -> `open risk` | correct | check l11.q3.member-order |
| `quiz[3].widget.options[1]` | not: `open feed` / why: You followed the initialiser list. Members are built in declaration order, and `risk_… | correct | check l11.q3.member-order |
| `quiz[3].widget.options[2]` | not: `close feed` / why: Nothing closes until `d` is destroyed at the end of `main`. | correct | check l11.q3.member-order |
| `quiz[3].feedback.correct` | Declaration order, not list order. | correct | check l11.q3.member-order |
| `quiz[3].explain.text` | `risk_` is declared first, so it is built first, whatever the list says. At the end the order reverses: `clos… | correct | check l11.q3.member-order |
| `summary.ideas[0]` | A destructor runs when its object's scope ends, in reverse order of construction. A temporary dies at the end… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | `T b = a;` builds `b` with the copy constructor; `b = a;` on an existing `b` is copy assignment. `std::move(a… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | Rule of zero: hold members that manage themselves (`std::vector`, `std::string`, `std::unique_ptr`) and write… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \text{built } a, b, c \quad\Rightarrow\quad \text{destroyed } c, b, a / Within one scope, newest first; an in… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | A class holding a raw pointer gets a default copy that copies the address, so two destructors free one block.… | correct | restates the lesson: see the rows of the screens it summarises |

## l12-operators.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | In Python, `a + b` on your own class calls `a.__add__(b)`. Here are two amounts in C++, held as whole pence, … | correct | check l12.s0.no-plus |
| `screens[0].canvas` | canvas (pair): {"left": {"kind": "console", "params": {"title": "main.cpp", "lines": ["class Money {", "publi… | correct | check l12.s0.no-plus |
| `screens[0].widget.options[0]` | KEY: What must you write so that `fee + tax` compiles? -> A function named `operator+` that takes two `Money`… | correct | check l12.s0.no-plus |
| `screens[0].widget.options[1]` | not: A member function named `__add__` / why: That is Python's name. C++ looks for a function spelt `operator… | correct | check l12.s0.no-plus |
| `screens[0].widget.options[2]` | not: Nothing: `+` should add the members / why: C++ does not guess what adding a class means. Only built-in t… | correct | check l12.s0.no-plus |
| `screens[0].widget.options[3]` | not: Make `pence_` public / why: Access is not the problem. The error says `+` has no meaning for two `Money`… | correct | check l12.s0.no-plus |
| `screens[0].hints[0]` | Read the error: which operands does `+` not understand? | correct | check l12.s0.no-plus |
| `screens[0].hints[1]` | The two operand types are named here. | correct | check l12.s0.no-plus |
| `screens[0].hints[2]` | You define `+` for a type by writing a function called `operator+`. | correct | check l12.s0.no-plus |
| `screens[0].feedback.correct` | C++ spells `__add__` as `operator+`. | correct | check l12.s0.no-plus |
| `screens[0].feedback.byKey.auto` | C++ does not guess what adding a class means. Only built-in types have `+` ready-made. | correct | check l12.s0.no-plus |
| `screens[0].explain.text` | `fee + tax` is a call to `operator+(fee, tax)`, and none exists yet. Writing one is **operator overloading**.… | correct | check l12.s0.no-plus |
| `screens[1].prose` | `str()` should show pence as pounds: 1234 becomes `£12.34`. A first try joins `pence_ / 100`, a dot and `penc… | correct | check l12.s1.first-try |
| `screens[1].canvas` | canvas (table): {"columns": ["pence", "first try prints", "wanted"], "rows": [["1234", "?", "£12.34"], ["1205… | correct | check l12.s1.first-try |
| `screens[1].widget.answer` | KEY: Select all that apply: tap every row where the first try prints the wrong text. -> ["r1", "r2", "r3", "r… | correct | check l12.s1.first-try |
| `screens[1].hints[0]` | `std::to_string(5)` is `"5"`, with no leading zero. | correct | check l12.s1.first-try |
| `screens[1].hints[1]` | Try this row: 1205 / 100 is 12, and 1205 % 100 is 5. | correct | check l12.s1.first-try |
| `screens[1].hints[2]` | Any remainder below 10 loses its zero. For −150, both `/` and `%` are negative: `£-1.-50`. | correct | check l12.s1.first-try |
| `screens[1].feedback.correct` | Small remainders lose their zero, and negatives go wrong twice. | correct | check l12.s1.first-try |
| `screens[1].feedback.byKey.r0` | 1234 gives 12 and 34, so `£12.34`: that one is right. | correct | check l12.s1.first-try |
| `screens[1].feedback.byKey.r4` | 99 gives 0 and 99, so `£0.99`: that one is right. | correct | check l12.s1.first-try |
| `screens[1].feedback.byKey.r1` | 1205 % 100 is 5, and `std::to_string(5)` is `"5"`: the first try prints `£12.5`. | correct | check l12.s1.first-try |
| `screens[1].feedback.byKey.r2` | 1200 % 100 is 0, printed as `"0"`: the first try prints `£12.0`. | correct | check l12.s1.first-try |
| `screens[1].feedback.byKey.r3` | 7 / 100 is 0 and 7 % 100 is 7: the first try prints `£0.7`. | correct | check l12.s1.first-try |
| `screens[1].feedback.byKey.r5` | −150 / 100 is −1 and −150 % 100 is −50 (both round towards zero): the first try prints `£-1.-50`. | correct | check l12.s1.first-try |
| `screens[1].explain.text` | A remainder below 10 needs a leading zero. For a negative amount, format the absolute value and put the minus… | correct | check l12.s1.first-try |
| `screens[2].prose` | Now write the operators. An arithmetic operator takes its operands by value and **returns a new value**, like… | correct | checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[2].canvas` | canvas (table): {"columns": ["pence", "first try prints", "wanted"], "rows": [["1234", "£12.34", "£12.34"], [… | correct | checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[2].widget.solution` | code: Write `str()` to match the wanted column (its minus is a plain `-`), then `Money operator+(Money a, Mon… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[2].hints[0]` | Work with the absolute value, then put `-` in front when `pence_` is negative. | correct | checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[2].hints[1]` | Rows 2 to 4 need a leading zero on the pence. | correct | checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[2].hints[2]` | `std::string cents = std::to_string(p % 100); if (cents.size() < 2) cents = "0" + cents;` and `return Money(a… | correct | checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[2].feedback.correct` | Whole pence in, exact text out. | correct | checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[2].feedback.byKey.compile` | The compiler stopped. If it says `invalid operands`, an operator is missing or its parameters do not match th… | correct | checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[2].feedback.byKey.test-2` | Test 2 expects `£12.05`. Pad a remainder below 10 with a `0`. | correct | checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[2].feedback.byKey.test-8` | Test 8 expects `-£1.50`. Format the absolute value and put the minus sign before the `£`. | correct | checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[2].explain.text` | Both operators build and return a new `Money`, so `a + b` leaves `a` and `b` alone. `str()` formats the absol… | correct | checks l12.s2.fb-test-2, l12.s2.fb-test-8, l12.s2.pound-bytes |
| `screens[3].prose` | An operator can also be a **member** function: then the object is always its left operand. This `Money` defin… | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].canvas` | canvas (pair): {"left": {"kind": "console", "params": {"title": "main.cpp", "lines": ["class Money {", "publi… | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].widget.options[0]` | KEY: Which declaration makes `3 * fee` compile? -> A free function `Money operator*(int k, Money m)` | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].widget.options[1]` | not: Another member, `Money operator*(int k) const` / why: A member operator always has the object on the lef… | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].widget.options[2]` | not: A free function `Money operator*(Money m, int k)` / why: That is `fee * 3` again. The parameters follow … | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].widget.options[3]` | not: None: C++ cannot put a class on the right of `*` / why: A free function can take its operands in either … | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].hints[0]` | For a member, which operand is the object? | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].hints[1]` | In line 12 the left operand is an `int`. | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].hints[2]` | Only a free function can have an `int` as its first parameter. | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].feedback.correct` | A free function puts the `int` first. | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].feedback.byKey.member` | A member operator always has the object on the left, so it only ever gives `fee * 3`. | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[3].explain.text` | `fee * 3` calls `fee.operator*(3)`, but `3 * fee` needs a function whose first parameter is an `int`. Only a … | correct | checks l12.s3.member-side, l12.s3.free |
| `screens[4].prose` | Python prints an object through `__repr__`. C++ prints through `operator<<`, which takes the stream by refere… | correct | check l12.s4.chain |
| `screens[4].canvas` | canvas (console): {"lines": ["$ ./main", "£12.50 + £3.99"], "title": "Terminal"} | correct | check l12.s4.chain |
| `screens[4].widget.options[0]` | KEY: Why does `operator<<` return `os`? -> So the next `<<` in the chain has a stream to write to | correct | check l12.s4.chain |
| `screens[4].widget.options[1]` | not: To hand back a copy of the stream / why: It returns a reference. Streams cannot be copied, which is also… | correct | check l12.s4.chain |
| `screens[4].widget.options[2]` | not: To report whether the write worked / why: The stream records errors itself. The returned `os` feeds the … | correct | check l12.s4.chain |
| `screens[4].widget.options[3]` | not: Because Python's `__repr__` returns a string / why: `operator<<` writes to the stream rather than return… | correct | check l12.s4.chain |
| `screens[4].hints[0]` | `a << b << c` is read as `(a << b) << c`. | correct | check l12.s4.chain |
| `screens[4].hints[1]` | The left operand of the second `<<` is whatever the first one returned. | correct | check l12.s4.chain |
| `screens[4].hints[2]` | The first call must return the stream itself, so the second call writes to the same stream. | correct | check l12.s4.chain |
| `screens[4].feedback.correct` | Each `<<` hands the stream to the next. | correct | check l12.s4.chain |
| `screens[4].explain.text` | `std::cout << a << b` is `operator<<(operator<<(std::cout, a), b)`. Returning `os` by reference keeps one str… | correct | check l12.s4.chain |
| `screens[5].prose` | A colleague's `+` saves a copy by working on the left operand directly. | correct | check l12.s5.plus-writes |
| `screens[5].canvas` | canvas (console): {"lines": ["struct Money { long long pence; };", "", "Money& operator+(Money& a, Money b) {… | correct | check l12.s5.plus-writes |
| `screens[5].widget.options[0]` | KEY: What does it print? -> `1250 1250` | correct | check l12.s5.plus-writes |
| `screens[5].widget.options[1]` | not: `1000 1250` / why: You expected `+` to leave `cash` alone, as built-in `+` does. This one takes `a` by n… | correct | check l12.s5.plus-writes |
| `screens[5].widget.options[2]` | not: A compile error: `+` must return a value / why: It returns `Money&`, which compiles. The bug is that it … | correct | check l12.s5.plus-writes |
| `screens[5].widget.options[3]` | not: `1250 1000` / why: `total` is a copy of the changed `cash`, so it also holds 1250. | correct | check l12.s5.plus-writes |
| `screens[5].hints[0]` | Look at the type of the first parameter. | correct | check l12.s5.plus-writes |
| `screens[5].hints[1]` | This line writes into `a`, which is `cash` itself. | correct | check l12.s5.plus-writes |
| `screens[5].hints[2]` | `cash + fee` adds 250 into `cash`, then `total` copies it: both are 1250. | correct | check l12.s5.plus-writes |
| `screens[5].feedback.correct` | This `+` changed `cash`: a `+=` in disguise. | correct | check l12.s5.plus-writes |
| `screens[5].feedback.byKey.pure` | You expected `+` to leave `cash` alone, as built-in `+` does. This one takes `a` by non-const reference and a… | correct | check l12.s5.plus-writes |
| `screens[5].explain.text` | `Money& a` is `cash` itself, so the sum is written into it. A reader of `cash + fee` never expects `cash` to … | correct | check l12.s5.plus-writes |
| `screens[6].prose` | A first `Price` type stores pounds in a `double`. Its `operator==` compares them directly. | correct | check l12.s6.double-eq |
| `screens[6].canvas` | canvas (console): {"lines": ["struct Price { double px; };", "", "bool operator==(Price a, Price b) {", " ret… | correct | check l12.s6.double-eq |
| `screens[6].widget.options[0]` | KEY: What does it print? -> `0` | correct | check l12.s6.double-eq |
| `screens[6].widget.options[1]` | not: `1` / why: You expected 0.1 + 0.2 to equal 0.3. In binary it is 0.30000000000000004, so `==` says no. | correct | check l12.s6.double-eq |
| `screens[6].widget.options[2]` | not: A compile error: `==` needs `const` references / why: Taking `Price` by value is fine for a small type. … | correct | check l12.s6.double-eq |
| `screens[6].hints[0]` | Is 0.1 + 0.2 exactly 0.3 as a `double`? | correct | check l12.s6.double-eq |
| `screens[6].hints[1]` | This line compares two doubles bit for bit. | correct | check l12.s6.double-eq |
| `screens[6].hints[2]` | 0.1 + 0.2 is 0.30000000000000004, so the comparison is false and prints 0. | correct | check l12.s6.double-eq |
| `screens[6].feedback.correct` | `==` on doubles is exact, and binary fractions are not. | correct | check l12.s6.double-eq |
| `screens[6].feedback.byKey.one` | You expected 0.1 + 0.2 to equal 0.3. In binary it is 0.30000000000000004, so `==` says no. | correct | check l12.s6.double-eq |
| `screens[6].explain.text` | The fill and the limit print as equal but differ in the last bit. Python's `__eq__` on floats has the same pr… | correct | check l12.s6.double-eq |
| `screens[7].prose` | `std::sort` orders a vector using `<`. So a `Price` in whole pence needs `operator<`. Its `==` must agree: tw… | correct | checks l12.s7.fb-test-5, l12.s7.fb-test-7 |
| `screens[7].canvas` | canvas (array): {"cells": ["101.25", "101.00", "101.50"]} | correct | checks l12.s7.fb-test-5, l12.s7.fb-test-7 |
| `screens[7].widget.solution` | code: Write `bool operator<(const Price& a, const Price& b)` and `bool operator==(const Price& a, const Price… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l12.s7.fb-test-5, l12.s7.fb-test-7 |
| `screens[7].hints[0]` | Compare the `pence` members. | correct | checks l12.s7.fb-test-5, l12.s7.fb-test-7 |
| `screens[7].hints[1]` | The smallest goes first after sorting. | correct | checks l12.s7.fb-test-5, l12.s7.fb-test-7 |
| `screens[7].hints[2]` | `return a.pence < b.pence;` and `return a.pence == b.pence;`. | correct | checks l12.s7.fb-test-5, l12.s7.fb-test-7 |
| `screens[7].feedback.correct` | `std::sort` now orders your type. | correct | checks l12.s7.fb-test-5, l12.s7.fb-test-7 |
| `screens[7].feedback.byKey.test-5` | Test 5 asks whether a price is less than itself, and expects false. Use `<`, not `<=`: `std::sort` needs a st… | correct | checks l12.s7.fb-test-5, l12.s7.fb-test-7 |
| `screens[7].feedback.byKey.test-7` | Test 7 compares the same pence at two venues and expects true. Compare pence only, as `<` does. | correct | checks l12.s7.fb-test-5, l12.s7.fb-test-7 |
| `screens[7].explain.text` | `std::sort` calls your `operator<` for every comparison it makes. It must be strict: `a < a` is false. And `=… | correct | checks l12.s7.fb-test-5, l12.s7.fb-test-7 |
| `screens[8].prose` | Each Python special method has a C++ operator. `__add__` is `operator+`, `__eq__` is `operator==`, `__lt__` i… | correct | ISO C++17 (N4659) [over.oper]; checks l12.s5.plus-writes, l12.s4.chain |
| `screens[8].widget.options[0]` | KEY: Which declaration is right for subtracting one `Money` from another? -> `Money operator-(Money a, Money … | correct | ISO C++17 (N4659) [over.oper]; checks l12.s5.plus-writes, l12.s4.chain |
| `screens[8].widget.options[1]` | not: `Money& operator-(Money& a, Money b)` / why: That writes into the left operand, the trap you met. `-` sh… | correct | ISO C++17 (N4659) [over.oper]; checks l12.s5.plus-writes, l12.s4.chain |
| `screens[8].widget.options[2]` | not: `void operator-(Money a, Money b)` / why: Then `a - b` would have no value to store or print. | correct | ISO C++17 (N4659) [over.oper]; checks l12.s5.plus-writes, l12.s4.chain |
| `screens[8].widget.options[3]` | not: `Money operator-(Money a)` / why: One parameter makes unary minus, `-a`, not subtraction. | correct | ISO C++17 (N4659) [over.oper]; checks l12.s5.plus-writes, l12.s4.chain |
| `screens[8].hints[0]` | Which shape does `+` have? | correct | ISO C++17 (N4659) [over.oper]; checks l12.s5.plus-writes, l12.s4.chain |
| `screens[8].hints[1]` | Subtraction is binary and pure, like `+`: two values in, a new value out. | correct | ISO C++17 (N4659) [over.oper]; checks l12.s5.plus-writes, l12.s4.chain |
| `screens[8].feedback.correct` | Two values in, one new value out. | correct | ISO C++17 (N4659) [over.oper]; checks l12.s5.plus-writes, l12.s4.chain |
| `screens[8].explain.text` | `-` has the same shape as `+`: two `Money` values in, a new one out. Arithmetic returns by value, comparisons… | correct | ISO C++17 (N4659) [over.oper]; checks l12.s5.plus-writes, l12.s4.chain |
| `screens[9].prose` | An exchange fills resting sell orders by **price-time priority**: the lowest ask first, and at the same price… | correct | checks l12.s9.fb-test-4, l12.s9.fb-test-1; price-time priority: Harris, Trading and Exchanges, ch. 6; ISO C++17 (N4659) [tuple.rel] (lexicographic) |
| `screens[9].canvas` | canvas (table): {"columns": ["order", "price", "arrived"], "rows": [["A", "£101.00", "3rd"], ["B", "£100.50",… | correct | checks l12.s9.fb-test-4, l12.s9.fb-test-1; price-time priority: Harris, Trading and Exchanges, ch. 6; ISO C++17 (N4659) [tuple.rel] (lexicographic) |
| `screens[9].widget.solution` | code: Write `bool operator<(const Order& a, const Order& b)`: true when `a` trades before `b` on the ask side… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l12.s9.fb-test-4, l12.s9.fb-test-1; price-time priority: Harris, Trading and Exchanges, ch. 6; ISO C++17 (N4659) [tuple.rel] (lexicographic) |
| `screens[9].hints[0]` | Compare prices first; look at times only when the prices are equal. | correct | checks l12.s9.fb-test-4, l12.s9.fb-test-1; price-time priority: Harris, Trading and Exchanges, ch. 6; ISO C++17 (N4659) [tuple.rel] (lexicographic) |
| `screens[9].hints[1]` | A and C share a price; C arrived first. | correct | checks l12.s9.fb-test-4, l12.s9.fb-test-1; price-time priority: Harris, Trading and Exchanges, ch. 6; ISO C++17 (N4659) [tuple.rel] (lexicographic) |
| `screens[9].hints[2]` | `return std::tie(a.price, a.time) < std::tie(b.price, b.time);` | correct | checks l12.s9.fb-test-4, l12.s9.fb-test-1; price-time priority: Harris, Trading and Exchanges, ch. 6; ISO C++17 (N4659) [tuple.rel] (lexicographic) |
| `screens[9].feedback.correct` | B, then C, then A: price first, time second. | correct | checks l12.s9.fb-test-4, l12.s9.fb-test-1; price-time priority: Harris, Trading and Exchanges, ch. 6; ISO C++17 (N4659) [tuple.rel] (lexicographic) |
| `screens[9].feedback.byKey.test-1` | Test 1 expects B, C, A. B has the lowest price; C and A tie on price, and C arrived first. | correct | checks l12.s9.fb-test-4, l12.s9.fb-test-1; price-time priority: Harris, Trading and Exchanges, ch. 6; ISO C++17 (N4659) [tuple.rel] (lexicographic) |
| `screens[9].feedback.byKey.test-4` | Test 4 puts a cheaper but later order first. Compare prices before times. | imprecise | check l12.s9.fb-test-4: comparing time first gives C, A, B on test 1 (key test-1); finding 14 |
| `screens[9].explain.text` | `std::tie` compares price first and falls through to time only on a tie. For bids you would flip the price te… | correct | checks l12.s9.fb-test-4, l12.s9.fb-test-1; price-time priority: Harris, Trading and Exchanges, ch. 6; ISO C++17 (N4659) [tuple.rel] (lexicographic) |
| `quiz[0].prose` | ```cpp struct Px { long long pence; std::string venue; }; bool operator<(const Px& a, const Px& b) { return a… | correct | check l12.q0.lt-eq |
| `quiz[0].widget.options[0]` | KEY: What does it print, and what does that mean? -> `000`: `<` treats them as the same, `==` does not | correct | check l12.q0.lt-eq |
| `quiz[0].widget.options[1]` | not: `001` / why: `==` also compares the venue, and LSE is not CBOE, so it is false. | correct | check l12.q0.lt-eq |
| `quiz[0].widget.options[2]` | not: `100` / why: Both have 100 pence, so neither is less than the other. | correct | check l12.q0.lt-eq |
| `quiz[0].widget.options[3]` | not: `000`, which is consistent / why: If neither is less than the other, a sort treats them as equal. `==` s… | correct | check l12.q0.lt-eq |
| `quiz[0].feedback.correct` | Neither is less, yet they are not equal: the two operators disagree. | correct | check l12.q0.lt-eq |
| `quiz[0].explain.text` | A sort treats `a` and `b` as equivalent, but `==` calls them different. So a search after a sort can miss. De… | correct | check l12.q0.lt-eq |
| `quiz[1].prose` | ```cpp struct Pnl { long long pence; }; struct Quantity { int shares; }; Pnl operator+(Pnl a, Pnl b) { return… | correct | check l12.q1.units |
| `quiz[1].widget.options[0]` | KEY: What happens? -> A compile error: no `operator+` takes a `Pnl` and a `Quantity` | correct | check l12.q1.units |
| `quiz[1].widget.options[1]` | not: `oops.pence` is 12800 / why: You expected C++ to add the numbers inside. It looks for an `operator+` tha… | correct | check l12.q1.units |
| `quiz[1].widget.options[2]` | not: The `Quantity` converts to `Pnl` first / why: There is no conversion from `Quantity` to `Pnl`, so the on… | correct | check l12.q1.units |
| `quiz[1].feedback.correct` | Separate types turn a unit mistake into a compile error. | correct | check l12.q1.units |
| `quiz[1].explain.text` | The only `operator+` takes two `Pnl` values, and a `Quantity` is not one. With plain `long long` and `int`, t… | correct | check l12.q1.units |
| `quiz[2].prose` | ```cpp std::ostream& operator<<(std::ostream os, const Money& m) { os << m.str(); return os; } std::cout << M… | correct | check l12.q2.stream-by-value |
| `quiz[2].widget.options[0]` | KEY: What happens? -> A compile error: the stream's copy constructor is deleted | correct | check l12.q2.stream-by-value |
| `quiz[2].widget.options[1]` | not: It prints `£12.50` / why: Taking `os` by value would copy `std::cout`. Streams cannot be copied: the cop… | correct | check l12.q2.stream-by-value |
| `quiz[2].widget.options[2]` | not: It prints nothing, because it writes to a copy / why: It never gets that far. Copying a stream does not … | correct | check l12.q2.stream-by-value |
| `quiz[2].feedback.correct` | Streams are passed by reference because they cannot be copied. | correct | check l12.q2.stream-by-value |
| `quiz[2].explain.text` | A by-value parameter is built with the copy constructor, and `std::ostream` deletes it. Write `std::ostream& … | correct | check l12.q2.stream-by-value |
| `quiz[3].prose` | With your `Money` class: ```cpp Money fee(-375); std::cout << (fee * 2).str() << '\n'; ``` | correct | check l12.q3.neg |
| `quiz[3].widget.options[0]` | KEY: What does it print? -> `-£7.50` | correct | check l12.q3.neg |
| `quiz[3].widget.options[1]` | not: `£-7.50` / why: `str()` puts the sign before the `£`, after formatting the absolute value. | correct | check l12.q3.neg |
| `quiz[3].widget.options[2]` | not: `-£7.5` / why: The pence are padded to two digits: 50 stays `50`, and 5 would become `05`. | correct | check l12.q3.neg |
| `quiz[3].widget.options[3]` | not: `£7.50` / why: `operator*` keeps the sign: −375 × 2 is −750. | correct | check l12.q3.neg |
| `quiz[3].feedback.correct` | −750 pence is −£7.50. | correct | check l12.q3.neg |
| `quiz[3].explain.text` | `operator*` gives −750 pence. `str()` formats 750 as `£7.50` and puts the minus sign in front. | correct | check l12.q3.neg |
| `summary.ideas[0]` | `a + b` on your type calls `operator+(a, b)`: C++'s spelling of Python's `__add__`. Arithmetic operators take… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | A member operator always has the object on the left. Write symmetric operators as free functions, so `3 * fee… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | `<` must be strict and agree with `==`; test equality on whole pence, never on doubles. `operator<<` takes an… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | a + b \quad\equiv\quad \texttt{operator+}(a, b) / And `std::cout << a << b` is `operator<<(operator<<(std::co… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | A `+` that takes its left operand by non-const reference changes it: `cash + fee` would change `cash`. Return… | correct | restates the lesson: see the rows of the screens it summarises |

## l13-templates.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | You need the largest value of a vector of `int` volumes and of a vector of `double` prices. C++ checks types,… | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].canvas` | canvas (console): {"lines": ["int max_of(const std::vector<int>& xs) {", " int best = xs[0];", " for (int x :… | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].widget.answer` | KEY: Select all that apply: tap every line of the `double` version that differs from the `int` version. -> ["… | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].hints[0]` | Compare line 6 with line 1, line 7 with line 2, and so on. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].hints[1]` | These two lines are the same in both. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].hints[2]` | Every line that names the element type differs: the signature, `best` and the loop variable. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].feedback.correct` | Only the type changes: lines 6, 7 and 8. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].feedback.byKey.l9` | `return best;` is the same in both versions. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].feedback.byKey.l10` | The closing brace is the same in both versions. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].feedback.byKey.l1` | That is in the `int` version. Compare the second function with the first. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].feedback.byKey.l2` | That is in the `int` version. Compare the second function with the first. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].feedback.byKey.l3` | That is in the `int` version. Compare the second function with the first. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].feedback.byKey.l4` | That is in the `int` version. Compare the second function with the first. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].feedback.byKey.l5` | That is in the `int` version. Compare the second function with the first. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].feedback.byKey.l8` | Line 8 declares `double x` in the loop, so the type appears there too. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].feedback.byKey.l7` | Line 7 declares `double best`, so it differs from line 2. | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[0].explain.text` | The two bodies are the same idea with a different type in three places. A string version would repeat them ag… | correct | read off the listing: lines 6, 7 and 8 name the element type |
| `screens[1].prose` | A **template** writes the function once, with the type as a parameter `T`. Each call fixes `T` from its argum… | correct | check l13.s1.max-of |
| `screens[1].canvas` | canvas (graph): {"nodes": [{"id": "tpl", "label": "max_of<T>", "x": 0.5, "y": 0.12, "shape": "rect"}, {"id": … | correct | check l13.s1.max-of |
| `screens[1].widget.answer` | KEY: Select all that apply: tap every function the compiler writes for this program. -> ["i", "d", "s"] | correct | check l13.s1.max-of |
| `screens[1].hints[0]` | Which types appear inside `std::vector<...>` in the calls? | correct | check l13.s1.max-of |
| `screens[1].hints[1]` | Two calls use `std::vector<int>`. | correct | check l13.s1.max-of |
| `screens[1].hints[2]` | Three types are used: `int`, `double` and `std::string`. One function is written for each. | correct | check l13.s1.max-of |
| `screens[1].feedback.correct` | Three types used, three functions written. | correct | check l13.s1.max-of |
| `screens[1].feedback.byKey.c` | No call uses `std::vector<char>`, so no `char` version is written. | correct | check l13.s1.max-of |
| `screens[1].feedback.byKey.l` | No call uses `std::vector<long>`, so no `long` version is written. | correct | check l13.s1.max-of |
| `screens[1].feedback.byKey.i` | `max_of<int>` is used, twice. It is written once and called twice. | correct | check l13.s1.max-of |
| `screens[1].feedback.byKey.s` | The last call uses `std::vector<std::string>`, so a string version is written. | correct | check l13.s1.max-of |
| `screens[1].feedback.byKey.d` | The second call uses `std::vector<double>`, so a `double` version is written. | correct | check l13.s1.max-of |
| `screens[1].explain.text` | At compile time the compiler writes one real function per type used: an **instantiation**. Two `int` calls sh… | correct | check l13.s1.max-of |
| `screens[2].prose` | Now write one. Start the total at `T{}`, the type's empty value: 0 for numbers, `""` for a string. Then `+=` … | correct | checks l13.s2.fb-test-2, l13.s2.fb-test-7 |
| `screens[2].canvas` | canvas (console): {"lines": ["sum_of(std::vector<int>{1, 2, 3}) // 6", "sum_of(std::vector<double>{0.5, 0.25}… | correct | checks l13.s2.fb-test-2, l13.s2.fb-test-7 |
| `screens[2].widget.solution` | code: Write `template <typename T> T sum_of(const std::vector<T>& xs)`. (7 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l13.s2.fb-test-2, l13.s2.fb-test-7 |
| `screens[2].hints[0]` | Write `template <typename T>` on the line before the function. | correct | checks l13.s2.fb-test-2, l13.s2.fb-test-7 |
| `screens[2].hints[1]` | An empty vector must give the type's empty value. | correct | checks l13.s2.fb-test-2, l13.s2.fb-test-7 |
| `screens[2].hints[2]` | `T total{}; for (const T& x : xs) total += x; return total;` | correct | checks l13.s2.fb-test-2, l13.s2.fb-test-7 |
| `screens[2].feedback.correct` | One source, four types. | correct | checks l13.s2.fb-test-2, l13.s2.fb-test-7 |
| `screens[2].feedback.byKey.compile` | The compiler stopped. Check that `template <typename T>` comes right before the function, and that it returns… | correct | checks l13.s2.fb-test-2, l13.s2.fb-test-7 |
| `screens[2].feedback.byKey.test-2` | Test 2 adds doubles and expects 0.75. If you got 0, the total was an `int`: declare it as `T`. | wrong | check l13.s2.fb-test-2: an int total does not compile (the std::string test instantiates `int += std::string`), so it can never give 0; finding 2 |
| `screens[2].feedback.byKey.test-7` | Test 7 joins strings. Start from `T{}`, not `0`: a `std::string` cannot start from a number. | correct | checks l13.s2.fb-test-2, l13.s2.fb-test-7 |
| `screens[2].explain.text` | `T{}` is 0 for numbers and an empty string for `std::string`, so one start value works for every type. `+=` m… | correct | checks l13.s2.fb-test-2, l13.s2.fb-test-7 |
| `screens[3].prose` | Here `T` is **deduced** from both arguments, and each argument has to agree. | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].canvas` | canvas (pair): {"left": {"kind": "console", "params": {"title": "main.cpp", "lines": ["template <typename T>"… | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].widget.options[0]` | KEY: Which call compiles and compares 3 with 2.5 without losing the half? -> `bigger<double>(3, 2.5)` | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].widget.options[1]` | not: `bigger(3, 2.5)` / why: That is the failing call: from 3, `T` is `int`, and from 2.5 it is `double`. One… | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].widget.options[2]` | not: `bigger<int>(3, 2.5)` / why: That compiles, but `T` is `int`, so 2.5 becomes 2 before the comparison. | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].widget.options[3]` | not: `bigger<int, double>(3, 2.5)` / why: `bigger` has one type parameter, so it takes one type in the angle … | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].hints[0]` | What type does `3` give `T`? What type does `2.5` give? | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].hints[1]` | The note says the two deductions conflict. | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].hints[2]` | Name `T` yourself in angle brackets; then both arguments convert to it. | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].feedback.correct` | Naming `T` stops the deduction, and 3 converts to 3.0. | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].feedback.byKey.same` | That is the failing call: from 3, `T` is `int`, and from 2.5 it is `double`. One `T` cannot be both. | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[3].explain.text` | Each argument proposes a `T`, and they must agree. Writing `bigger<double>` fixes `T`, so the `int` 3 convert… | correct | checks l13.s3.conflict, l13.s3.double, l13.s3.int, l13.s3.two |
| `screens[4].prose` | `std::sort` is a template, compiled again for every type you sort. Sorting `Quote`s, which have no `<`, fails… | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].canvas` | canvas (console): {"lines": ["$ clang++ -std=c++17 main.cpp", "In file included from main.cpp:1:", "In file i… | imprecise | checks l13.s4.sort-error (fails), l13.s4.sort-error-debug and l13.s4.two-lines (hold): lines 7 to 12 of the transcript appear only with the libc++ debug checks on; finding 6 |
| `screens[4].widget.answer` | KEY: Tap the two lines that matter: what is missing, and which line of your code asked for it. -> ["l5", "l20… | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].hints[0]` | Look for the first `error:` and for the first line that names `main.cpp`. | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].hints[1]` | This is the first error. | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].hints[2]` | Line 5 says `<` has no meaning for two `Quote`s. Line 20 points at `main.cpp:11`, your call to `std::sort`. | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].feedback.correct` | The first error says what is missing; the `main.cpp` note says where you asked. | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].feedback.byKey.l7` | That is a library file's path, an `instantiation` note. The cause is in the first `error:` line. | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].feedback.byKey.l11` | That is a library file's path, an `instantiation` note. Find the line that names `main.cpp`. | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].feedback.byKey.l14` | That is a library file's path, an `instantiation` note. Find the line that names `main.cpp`. | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].feedback.byKey.l2` | That line only says which header the error is in. Find the first `error:`. | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].feedback.byKey.l23` | Later errors repeat the same cause. Read the first one. | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[4].explain.text` | Line 5: `<` is missing for `Quote`. Line 20: your line 11 asked for it. Between them runs the template chain … | correct | checks l13.s4.sort-error, l13.s4.sort-error-debug, l13.s4.two-lines |
| `screens[5].prose` | A class can be a template too: `Series<T>` holds a vector of `T`. Here it holds tickers, where a mean makes n… | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[5].canvas` | canvas (console): {"lines": ["template <typename T>", "class Series {", "public:", " void push(T x) { xs_.pus… | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[5].widget.options[0]` | KEY: Does this program build? -> Yes: nothing calls `mean`, so it is never compiled for `std::string` | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[5].widget.options[1]` | not: No: a `std::string` cannot be divided / why: You expected every member to be checked for `std::string`. … | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[5].widget.options[2]` | not: No: `Series` only accepts number types / why: Nothing in the template says so. `T` can be any type until… | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[5].hints[0]` | Which member functions does `main` call? | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[5].hints[1]` | `mean` is defined here but never called. | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[5].hints[2]` | Only `push` is called, and pushing a string is fine. | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[5].feedback.correct` | It builds: `mean` is never instantiated for `std::string`. | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[5].feedback.byKey.no` | You expected every member to be checked for `std::string`. A class template's member function is compiled onl… | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[5].explain.text` | A template's body is checked for a type only when that code is used. Add `names.mean();` and clang reports `i… | correct | checks l13.s5.lazy, l13.s5.mean-string |
| `screens[6].prose` | The same `Series`, now holding traded volumes as `int`s. ```cpp int main() { Series<int> volumes; volumes.pus… | correct | check l13.s6.int-mean |
| `screens[6].canvas` | canvas (console): {"lines": ["template <typename T>", "class Series {", "public:", " void push(T x) { xs_.pus… | correct | check l13.s6.int-mean |
| `screens[6].widget.options[0]` | KEY: What does it print? -> `2000` | correct | check l13.s6.int-mean |
| `screens[6].widget.options[1]` | not: `2000.5` / why: You expected a fractional mean. With `T = int` the total and `mean`'s result are `int`s,… | correct | check l13.s6.int-mean |
| `screens[6].widget.options[2]` | not: `2001` / why: Integer division does not round: 4001 / 2 is 2000, the fraction thrown away. | correct | check l13.s6.int-mean |
| `screens[6].widget.options[3]` | not: A compile error: `int` cannot be divided by a size / why: `int` divides by an unsigned size and compiles… | correct | check l13.s6.int-mean |
| `screens[6].hints[0]` | What is `T` here, and what does `mean` return? | correct | check l13.s6.int-mean |
| `screens[6].hints[1]` | This line divides a total of type `T`. | correct | check l13.s6.int-mean |
| `screens[6].hints[2]` | 4001 / 2 in whole numbers is 2000. | correct | check l13.s6.int-mean |
| `screens[6].feedback.correct` | `T mean()` with `T = int` is an integer division. | correct | check l13.s6.int-mean |
| `screens[6].feedback.byKey.exact` | You expected a fractional mean. With `T = int` the total and `mean`'s result are `int`s, so the division drop… | correct | check l13.s6.int-mean |
| `screens[6].explain.text` | Returning `T` made the mean an `int`. A negative total would also become a huge unsigned number before the di… | correct | check l13.s6.int-mean |
| `screens[7].prose` | A template parameter can be a number instead of a type. `FixedPoint<Places>` stores a value as a whole number… | correct | checks l13.s7.units, l13.s7.slip-two |
| `screens[7].canvas` | canvas (table): {"columns": ["type", "value", "units stored"], "rows": [["`FixedPoint<2>`", "12.34", "1234"],… | correct | checks l13.s7.units, l13.s7.slip-two |
| `screens[7].widget.answer` | KEY: How many units does `FixedPoint<4>` store for the rate 1.2345? -> 12345 (12345: $1.2345 \times 10^4$.) | correct | checks l13.s7.units, l13.s7.slip-two |
| `screens[7].widget.wrong[0]` | slip two = 123: You used two places, as for pence. `FixedPoint<4>` keeps four. | wrong | check l13.s7.slip-two: two places give 1.2345 x 100 = 123.45, not 123; finding 3 |
| `screens[7].widget.wrong[1]` | slip raw = 1.2345: That is the value itself. The class stores a whole number of $10^{-4}$ units. | correct | checks l13.s7.units, l13.s7.slip-two |
| `screens[7].hints[0]` | How many units of $10^{-4}$ make 1.2345? | correct | checks l13.s7.units, l13.s7.slip-two |
| `screens[7].hints[1]` | The first row multiplies 12.34 by $10^2$. | correct | checks l13.s7.units, l13.s7.slip-two |
| `screens[7].hints[2]` | Multiply by $10^4 = 10000$. | correct | checks l13.s7.units, l13.s7.slip-two |
| `screens[7].feedback.correct` | $1.2345 \times 10^4 = 12345$. | correct | checks l13.s7.units, l13.s7.slip-two |
| `screens[7].explain.text` | `Places` is fixed at compile time, so `FixedPoint<2>` and `FixedPoint<4>` are different types. Adding pence t… | correct | checks l13.s7.units, l13.s7.slip-two |
| `screens[8].prose` | A template is a recipe the compiler fills in, once per set of parameters it is used with: ```cpp template <ty… | correct | ISO C++17 (N4659) [temp.spec], [temp.inst] |
| `screens[8].widget.options[0]` | KEY: What are `std::vector<double>` and `std::vector<int>`? -> Two classes the compiler wrote from one templa… | correct | ISO C++17 (N4659) [temp.spec], [temp.inst] |
| `screens[8].widget.options[1]` | not: One class that can hold any type, like a Python list / why: A Python list holds any object at run time. … | correct | ISO C++17 (N4659) [temp.spec], [temp.inst] |
| `screens[8].widget.options[2]` | not: Two classes the library authors wrote by hand / why: The library ships one template; your program's uses… | correct | ISO C++17 (N4659) [temp.spec], [temp.inst] |
| `screens[8].widget.options[3]` | not: One class that checks the element type at run time / why: There is no run-time check: the element type i… | correct | ISO C++17 (N4659) [temp.spec], [temp.inst] |
| `screens[8].hints[0]` | Recall the graph of `max_of<T>` and its instantiations. | correct | ISO C++17 (N4659) [temp.spec], [temp.inst] |
| `screens[8].hints[1]` | `vector` is a class template, instantiated once per element type you use. | correct | ISO C++17 (N4659) [temp.spec], [temp.inst] |
| `screens[8].feedback.correct` | The standard library is almost entirely templates. | correct | ISO C++17 (N4659) [temp.spec], [temp.inst] |
| `screens[8].explain.text` | `std::vector`, `std::map`, `std::sort` and `std::unique_ptr` are all templates. That is how one library serve… | correct | ISO C++17 (N4659) [temp.spec], [temp.inst] |
| `screens[9].prose` | A signal uses the mean of the last $n$ prices. A volume filter uses the mean of the last $n$ volumes. One cla… | correct | checks l13.s9.fb-test-2, l13.s9.fb-test-7, l13.s9.fb-test-8, l13.s9.deque |
| `screens[9].canvas` | canvas (array): {"cells": [100, 101, 102, 106]} | correct | checks l13.s9.fb-test-2, l13.s9.fb-test-7, l13.s9.fb-test-8, l13.s9.deque |
| `screens[9].widget.solution` | code: Write the constructor's check (`n` above 0) and `push`, which keeps only the last `n` values. Then writ… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks l13.s9.fb-test-2, l13.s9.fb-test-7, l13.s9.fb-test-8, l13.s9.deque |
| `screens[9].hints[0]` | In `push`, add the value, then drop the oldest if there are more than `n_`. | correct | checks l13.s9.fb-test-2, l13.s9.fb-test-7, l13.s9.fb-test-8, l13.s9.deque |
| `screens[9].hints[1]` | After the fourth push, the 100 is gone. | correct | checks l13.s9.fb-test-2, l13.s9.fb-test-7, l13.s9.fb-test-8, l13.s9.deque |
| `screens[9].hints[2]` | `xs_.push_back(x); if (static_cast<int>(xs_.size()) > n_) xs_.erase(xs_.begin());` and in `mean`, refuse `xs_… | correct | checks l13.s9.fb-test-2, l13.s9.fb-test-7, l13.s9.fb-test-8, l13.s9.deque |
| `screens[9].feedback.correct` | One template, any numeric series. | correct | checks l13.s9.fb-test-2, l13.s9.fb-test-7, l13.s9.fb-test-8, l13.s9.deque |
| `screens[9].feedback.byKey.test-2` | Test 2 pushes 4 values into a window of 3 and expects 103. Drop the oldest value. | correct | checks l13.s9.fb-test-2, l13.s9.fb-test-7, l13.s9.fb-test-8, l13.s9.deque |
| `screens[9].feedback.byKey.test-7` | Test 7 asks for the mean of an empty window. Refuse it before dividing by zero. | correct | checks l13.s9.fb-test-2, l13.s9.fb-test-7, l13.s9.fb-test-8, l13.s9.deque |
| `screens[9].feedback.byKey.test-8` | Test 8 builds a window of size 0. Refuse it in the constructor. | correct | checks l13.s9.fb-test-2, l13.s9.fb-test-7, l13.s9.fb-test-8, l13.s9.deque |
| `screens[9].explain.text` | `Window<double>` serves prices and volumes alike. `Window<FixedPoint<2>>` would work once it has `+=`, `/` an… | imprecise | check l13.s9.deque: no level 4 file names std::deque, std::queue or pop_front; std::vector::erase at the front is linear ([vector.modifiers]); finding 7 |
| `quiz[0].prose` | With the `max_of` template from this lesson: ```cpp max_of(std::vector<std::string>{"BARC", "AZN", "VOD", "LL… | correct | check l13.s1.max-of (returns VOD); ISO C++17 (N4659) [string.view.ops]/char_traits lexicographic compare; ASCII: capitals 65 to 90 precede lower case 97 to 122 |
| `quiz[0].widget.options[0]` | KEY: What does it return? -> `"VOD"` | correct | check l13.s1.max-of (returns VOD); ISO C++17 (N4659) [string.view.ops]/char_traits lexicographic compare; ASCII: capitals 65 to 90 precede lower case 97 to 122 |
| `quiz[0].widget.options[1]` | not: `"LLOY"` / why: `<` on strings compares character by character from the left, not by length. V comes aft… | correct | check l13.s1.max-of (returns VOD); ISO C++17 (N4659) [string.view.ops]/char_traits lexicographic compare; ASCII: capitals 65 to 90 precede lower case 97 to 122 |
| `quiz[0].widget.options[2]` | not: `"BARC"` / why: That is only the starting `best`. Any later string that compares greater replaces it. | correct | check l13.s1.max-of (returns VOD); ISO C++17 (N4659) [string.view.ops]/char_traits lexicographic compare; ASCII: capitals 65 to 90 precede lower case 97 to 122 |
| `quiz[0].widget.options[3]` | not: A compile error: strings have no maximum / why: `std::string` has `<`, which compares character by chara… | correct | check l13.s1.max-of (returns VOD); ISO C++17 (N4659) [string.view.ops]/char_traits lexicographic compare; ASCII: capitals 65 to 90 precede lower case 97 to 122 |
| `quiz[0].feedback.correct` | V is the latest first letter, so VOD is the maximum. | correct | check l13.s1.max-of (returns VOD); ISO C++17 (N4659) [string.view.ops]/char_traits lexicographic compare; ASCII: capitals 65 to 90 precede lower case 97 to 122 |
| `quiz[0].explain.text` | For `std::string`, `best < x` compares character codes from the left. For all-capital tickers that is alphabe… | correct | check l13.s1.max-of (returns VOD); ISO C++17 (N4659) [string.view.ops]/char_traits lexicographic compare; ASCII: capitals 65 to 90 precede lower case 97 to 122 |
| `quiz[1].prose` | ```cpp sum_of(std::vector<int>{1, 2}); sum_of(std::vector<double>{0.5}); sum_of(std::vector<int>{7}); sum_of(… | correct | ISO C++17 (N4659) [temp.inst]: one specialisation per distinct argument list (int, double, long long) |
| `quiz[1].widget.answer` | KEY: How many functions does the compiler write from `sum_of`? -> 3 (3: one each for `int`, `double` and `lon… | correct | ISO C++17 (N4659) [temp.inst]: one specialisation per distinct argument list (int, double, long long) |
| `quiz[1].widget.wrong[0]` | slip calls = 4: You counted calls. The two `int` calls share one instantiation. | correct | ISO C++17 (N4659) [temp.inst]: one specialisation per distinct argument list (int, double, long long) |
| `quiz[1].widget.wrong[1]` | slip one = 1: A template is not one function: each type used gets its own. | correct | ISO C++17 (N4659) [temp.inst]: one specialisation per distinct argument list (int, double, long long) |
| `quiz[1].feedback.correct` | One function per type: `int`, `double`, `long long`. | correct | ISO C++17 (N4659) [temp.inst]: one specialisation per distinct argument list (int, double, long long) |
| `quiz[1].explain.text` | The two `int` calls share `sum_of<int>`. With `double` and `long long`, that makes three instantiations. | correct | ISO C++17 (N4659) [temp.inst]: one specialisation per distinct argument list (int, double, long long) |
| `quiz[2].prose` | You declare `template <typename T> T sum_of(const std::vector<T>&);` in `stats.h` and define it in `stats.cpp… | correct | check l13.q2.template-in-cpp |
| `quiz[2].widget.options[0]` | KEY: What happens at the link step? -> An undefined reference to `sum_of<double>`: no file ever wrote it | correct | check l13.q2.template-in-cpp |
| `quiz[2].widget.options[1]` | not: It links and runs / why: `stats.cpp` never sees a `double` call, so it writes no `sum_of<double>`. `main… | correct | check l13.q2.template-in-cpp |
| `quiz[2].widget.options[2]` | not: `main.cpp` fails to compile / why: The declaration is enough to compile the call. The missing function s… | correct | check l13.q2.template-in-cpp |
| `quiz[2].feedback.correct` | A template's body must be visible where it is used, so it goes in the header. | correct | check l13.q2.template-in-cpp |
| `quiz[2].explain.text` | An instantiation is written where the body and the type meet. Here they never meet, so the linker finds no `s… | correct | check l13.q2.template-in-cpp |
| `quiz[3].prose` | With your `sum_of`: ```cpp auto a = sum_of(std::vector<double>{}); auto b = sum_of(std::vector<std::string>{}… | correct | check l13.q3.empty-sum |
| `quiz[3].widget.options[0]` | KEY: What are `a` and `b`? -> `a` is `0.0` and `b` is `""` | correct | check l13.q3.empty-sum |
| `quiz[3].widget.options[1]` | not: Both calls stop: the vectors are empty / why: The loop runs zero times and the function returns its star… | correct | check l13.q3.empty-sum |
| `quiz[3].widget.options[2]` | not: `a` is `0.0` and `b` is `"0"` / why: `T{}` for a string is the empty string, not the text 0. | correct | check l13.q3.empty-sum |
| `quiz[3].feedback.correct` | An empty sum is the type's empty value. | correct | check l13.q3.empty-sum |
| `quiz[3].explain.text` | With no elements the loop never runs, so the result is `T{}`: 0.0 for `double` and `""` for `std::string`. `a… | correct | check l13.q3.empty-sum |
| `summary.ideas[0]` | A template takes a type (or a number) as a parameter. The compiler writes one instantiation per set of parame… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[1]` | `T` is deduced from the arguments, and every argument must agree; name it yourself (`bigger<double>`) when th… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.ideas[2]` | In a template error, read the first `error:` line and the line naming your own file. The rest is the path bet… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.formula` | \texttt{max\_of<T>} \quad\to\quad \texttt{max\_of<int>},\ \texttt{max\_of<double>},\ \ldots / One function pe… | correct | restates the lesson: see the rows of the screens it summarises |
| `summary.trap` | Returning `T` from a mean makes `Series<int>` divide in whole numbers: 4001 / 2 gives 2000. Return `double`. | correct | restates the lesson: see the rows of the screens it summarises |

## review-1.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `items[0].prose` | ```text $ g++ -std=c++17 -Wall pnl.cpp -o pnl pnl.cpp:7:12: warning: unused variable 'fees' [-Wunused-variabl… | correct | check l1.s7.wall-unused |
| `items[0].widget.options[0]` | KEY: What is true now? -> `./pnl` exists and runs; `fees` is worth a look | correct | check l1.s7.wall-unused |
| `items[0].widget.options[1]` | not: There is no executable until the warning is fixed / why: You read `warning` as `error`. Only errors stop… | correct | check l1.s7.wall-unused |
| `items[0].widget.options[2]` | not: `./pnl` runs the version from before this build / why: With no errors, the linker wrote a fresh `pnl`. | correct | check l1.s7.wall-unused |
| `items[0].widget.options[3]` | not: You must run g++ again without `-Wall` / why: `-Wall` only adds warnings. It never stops a build. | correct | check l1.s7.wall-unused |
| `items[0].feedback.correct` | A warning is advice; the build finished. | correct | check l1.s7.wall-unused |
| `items[0].explain.text` | Only an `error:` stops the build, so `pnl` was written. The warning says `fees` is declared and never used, w… | correct | check l1.s7.wall-unused |
| `items[1].prose` | ```cpp int qty = 3; int lots = 4; double share = qty / lots; ``` | correct | check r1.prints |
| `items[1].widget.answer` | KEY: What does `share` hold? -> 0 (0) | correct | check r1.prints |
| `items[1].widget.wrong[0]` | slip true = 0.75: The `double` on the left does not reach the right side. `qty / lots` divides two `int`s and… | correct | check r1.prints |
| `items[1].feedback.correct` | `3 / 4` is 0 in `int`. | correct | check r1.prints |
| `items[1].explain.text` | Both operands are `int`, so the division drops the fraction and gives 0, stored as 0.0. Write `static_cast<do… | correct | check r1.prints |
| `items[2].prose` | ```cpp int turns = 0; for (int i = 3; i < 10; i += 2) { ++turns; } ``` | correct | check r1.prints |
| `items[2].widget.answer` | KEY: What is `turns` at the end? -> 4 (4) | correct | check r1.prints |
| `items[2].widget.wrong[0]` | slip seven = 7: You counted 3 to 9 one at a time. The step is `i += 2`. | correct | check r1.prints |
| `items[2].widget.wrong[1]` | slip five = 5: 11 fails the test `i < 10`, so there is no fifth turn. | correct | check r1.prints |
| `items[2].feedback.correct` | `i` takes 3, 5, 7 and 9. | correct | check r1.prints |
| `items[2].explain.text` | Start at 3, add 2 each turn, stop when `i < 10` fails: 3, 5, 7, 9. Four turns. | correct | check r1.prints |
| `items[3].widget.options[0]` | KEY: Which messages come from the linker rather than the compiler? Select all that apply. -> `undefined refer… | correct | checks l4.s7.multiple-definition, l4.q2.undefined-reference (ld), l1.s6.clang-semicolon, l4.s0.not-declared (compiler) |
| `items[3].widget.options[1]` | KEY: Which messages come from the linker rather than the compiler? Select all that apply. -> `multiple defini… | correct | checks l4.s7.multiple-definition, l4.q2.undefined-reference (ld), l1.s6.clang-semicolon, l4.s0.not-declared (compiler) |
| `items[3].widget.options[2]` | not: `expected ';' at end of declaration` / why: A missing `;` is found while reading one file: that is the c… | correct | checks l4.s7.multiple-definition, l4.q2.undefined-reference (ld), l1.s6.clang-semicolon, l4.s0.not-declared (compiler) |
| `items[3].widget.options[3]` | not: `'annualise' was not declared in this scope` / why: An unknown name in one file is a compiler error. The… | correct | checks l4.s7.multiple-definition, l4.q2.undefined-reference (ld), l1.s6.clang-semicolon, l4.s0.not-declared (compiler) |
| `items[3].feedback.correct` | The linker reports missing or doubled bodies across files. | correct | checks l4.s7.multiple-definition, l4.q2.undefined-reference (ld), l1.s6.clang-semicolon, l4.s0.not-declared (compiler) |
| `items[3].explain.text` | The compiler reads one `.cpp` at a time, so it reports syntax and unknown names. The linker joins the object … | correct | checks l4.s7.multiple-definition, l4.q2.undefined-reference (ld), l1.s6.clang-semicolon, l4.s0.not-declared (compiler) |
| `items[4].prose` | Two block trades of 1,500,000,000 shares each. ```cpp int volume = 1500000000; volume = volume + 1500000000; … | correct | checks r1.i4.wrap, r1.i4.arith |
| `items[4].widget.answer` | KEY: What does `volume` hold, in practice? -> -1294967296 (−1294967296) | correct | checks r1.i4.wrap, r1.i4.arith |
| `items[4].widget.wrong[0]` | slip true = 3000000000: That is the true total, but an `int` cannot hold it. It wraps by 2³², 4,294,967,296. | correct | checks r1.i4.wrap, r1.i4.arith |
| `items[4].widget.wrong[1]` | slip max = 2147483647: An `int` does not stop at its limit. It wraps round to negative values. | correct | checks r1.i4.wrap, r1.i4.arith |
| `items[4].widget.wrong[2]` | slip sign = 1294967296: 3,000,000,000 − 4,294,967,296 is below zero: the counter wraps past the largest int i… | correct | checks r1.i4.wrap, r1.i4.arith |
| `items[4].feedback.correct` | 3,000,000,000 − 2³² = −1,294,967,296. | correct | checks r1.i4.wrap, r1.i4.arith |
| `items[4].explain.text` | The true sum, 3,000,000,000, is 2³² too big for the wrapped result: 3,000,000,000 − 4,294,967,296 = −1,294,96… | correct | checks r1.i4.wrap, r1.i4.arith |
| `items[5].prose` | A risk check counts the days whose P&L lost more than the limit: a P&L below `-limit`. A loss of exactly the … | correct | checks r1.i5.fb-test-3, r1.i5.fb-test-1 |
| `items[5].widget.solution` | code: Write `count_breaches(pnl, limit)`. (5 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks r1.i5.fb-test-3, r1.i5.fb-test-1 |
| `items[5].feedback.correct` | Strictly below `-limit`, counted in one pass. | correct | checks r1.i5.fb-test-3, r1.i5.fb-test-1 |
| `items[5].feedback.byKey.test-3` | A loss of exactly 50 against a limit of 50 is not a breach. Use `<`, not `<=`. | correct | checks r1.i5.fb-test-3, r1.i5.fb-test-1 |
| `items[5].feedback.byKey.test-1` | Losses of 120.5 and 200 breach a limit of 100. Compare each P&L with `-limit`, not `limit`. | correct | checks r1.i5.fb-test-3, r1.i5.fb-test-1 |
| `items[5].explain.text` | A range-based `for` visits each day's P&L, and `x < -limit` counts only losses beyond the limit. An empty vec… | correct | checks r1.i5.fb-test-3, r1.i5.fb-test-1 |
| `items[6].prose` | `returns.h` declares `double annualise(double daily_vol, int days = 252);`. | correct | check r1.i6.default |
| `items[6].widget.options[0]` | KEY: Which call does not compile? -> `annualise()` | correct | check r1.i6.default |
| `items[6].widget.options[1]` | not: `annualise(0.01)` / why: `days` has a default, so one argument is enough. | correct | check r1.i6.default |
| `items[6].widget.options[2]` | not: `annualise(1)` / why: The `int` 1 converts to the `double` 1.0, so this compiles. | correct | check r1.i6.default |
| `items[6].widget.options[3]` | not: `annualise(0.01, 12)` / why: Both arguments given; 12 replaces the default. | correct | check r1.i6.default |
| `items[6].feedback.correct` | `daily_vol` has no default. | correct | check r1.i6.default |
| `items[6].explain.text` | Only `days` has a default. `daily_vol` must always be passed, so `annualise()` is a compile error. | correct | check r1.i6.default |
| `items[7].prose` | ```cpp std::cout << -9 / 4 << '\n'; ``` | correct | check r1.prints; Python: -9 // 4 == -3 (check r1.i4.arith) |
| `items[7].widget.answer` | KEY: What does it print? -> -2 (−2) | correct | check r1.prints; Python: -9 // 4 == -3 (check r1.i4.arith) |
| `items[7].widget.wrong[0]` | slip floor = -3: You floored, as Python's `//` does. C++ truncates towards zero, so −2.25 becomes −2. | correct | check r1.prints; Python: -9 // 4 == -3 (check r1.i4.arith) |
| `items[7].widget.wrong[1]` | slip exact = -2.25: Both operands are `int`, so the result is a whole number. | correct | check r1.prints; Python: -9 // 4 == -3 (check r1.i4.arith) |
| `items[7].widget.wrong[2]` | slip sign = 2: −9 / 4 is −2.25, and truncating towards zero gives −2. A positive 2 drops the minus sign of th… | correct | check r1.prints; Python: -9 // 4 == -3 (check r1.i4.arith) |
| `items[7].feedback.correct` | −2.25 truncated towards zero is −2. | correct | check r1.prints; Python: -9 // 4 == -3 (check r1.i4.arith) |
| `items[7].explain.text` | `-9 / 4` is −2.25 exactly, and C++ integer division drops the fraction towards zero: −2. Python's `-9 // 4` f… | correct | check r1.prints; Python: -9 // 4 == -3 (check r1.i4.arith) |

## review-2.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `items[0].prose` | ```cpp void swap_px(double a, double b) { double t = a; a = b; b = t; } double bid = 99.5, ask = 100.5; swap_… | correct | check r2.i0.swap |
| `items[0].widget.options[0]` | KEY: What does it print? -> `99.5 100.5` | correct | check r2.i0.swap |
| `items[0].widget.options[1]` | not: `100.5 99.5` / why: The parameters have no `&`, so `swap_px` swaps its own copies and the caller's `bid`… | correct | check r2.i0.swap |
| `items[0].widget.options[2]` | not: It does not compile / why: Passing `double`s by value is legal. It just does nothing useful here. | correct | check r2.i0.swap |
| `items[0].feedback.correct` | The swap happened to the copies. | correct | check r2.i0.swap |
| `items[0].explain.text` | `a` and `b` are copies of `bid` and `ask`, swapped and then destroyed at the `}`. The caller's variables keep… | correct | check r2.i0.swap |
| `items[1].widget.options[0]` | KEY: Inside `void report(const std::vector<double>& v)`, select all that apply: which lines compile? -> `std:… | correct | checks r2.i1.reads, r2.i1.push |
| `items[1].widget.options[1]` | KEY: Inside `void report(const std::vector<double>& v)`, select all that apply: which lines compile? -> `doub… | correct | checks r2.i1.reads, r2.i1.push |
| `items[1].widget.options[2]` | KEY: Inside `void report(const std::vector<double>& v)`, select all that apply: which lines compile? -> `std:… | correct | checks r2.i1.reads, r2.i1.push |
| `items[1].widget.options[3]` | not: `v.push_back(1.0);` / why: `push_back` changes the vector, and `v` is a `const` reference, so it is reje… | correct | checks r2.i1.reads, r2.i1.push |
| `items[1].feedback.correct` | Read `v`, or change your own copy. | correct | checks r2.i1.reads, r2.i1.push |
| `items[1].explain.text` | Reading through `v` is allowed, and so is copying it into a vector of your own and changing that. Only `v.pus… | correct | checks r2.i1.reads, r2.i1.push |
| `items[2].widget.answer` | KEY: `struct Level { double px; long long size; };` takes 16 bytes. `const Level* p` holds 0x4000. How many b… | correct | check l7.s1.arith (sizeof(Level) 16), l7.q3.hex (0x4050) |
| `items[2].widget.wrong[0]` | slip five = 5: You counted elements. Each step moves a whole 16-byte `Level`. | correct | check l7.s1.arith (sizeof(Level) 16), l7.q3.hex (0x4050) |
| `items[2].widget.wrong[1]` | slip eight = 40: You used 8 bytes per step. A `Level` holds a `double` and a `long long`: 16 bytes. | correct | check l7.s1.arith (sizeof(Level) 16), l7.q3.hex (0x4050) |
| `items[2].feedback.correct` | 5 × 16 = 80 bytes. | correct | check l7.s1.arith (sizeof(Level) 16), l7.q3.hex (0x4050) |
| `items[2].explain.text` | Pointer arithmetic moves whole objects: `p + 5` is 5 × 16 = 80 bytes on, address 0x4050. That is why `++p` wa… | correct | check l7.s1.arith (sizeof(Level) 16), l7.q3.hex (0x4050) |
| `items[3].widget.options[0]` | KEY: Select all that apply: which snippets are undefined behaviour? -> `double* f() { double x = 1.0; return … | correct | checks r2.i3.dead-local, r2.i3.at, r2.i3.asan-double-free |
| `items[3].widget.options[1]` | KEY: Select all that apply: which snippets are undefined behaviour? -> `double* p = new double(1.0); delete p… | correct | checks r2.i3.dead-local, r2.i3.at, r2.i3.asan-double-free |
| `items[3].widget.options[2]` | not: `double* q = new double[0]; delete[] q;` / why: Allocating zero elements is legal, and freeing the block… | correct | checks r2.i3.dead-local, r2.i3.at, r2.i3.asan-double-free |
| `items[3].widget.options[3]` | not: `std::vector<double> v(3); v.at(5);` / why: `at` checks the index and throws `std::out_of_range`. That i… | correct | checks r2.i3.dead-local, r2.i3.at, r2.i3.asan-double-free |
| `items[3].feedback.correct` | A dead local and a double delete. | correct | checks r2.i3.dead-local, r2.i3.at, r2.i3.asan-double-free |
| `items[3].explain.text` | Reading a dead local and deleting twice are undefined: this browser build ran both silently. A desk build wit… | correct | checks r2.i3.dead-local, r2.i3.at, r2.i3.asan-double-free |
| `items[4].prose` | ```cpp int depth(int n) { if (n == 0) return 0; return 1 + depth(n - 1); } ``` | correct | check r2.i4.frames |
| `items[4].widget.answer` | KEY: How many frames are on the stack at the deepest point of `main` calling `depth(4)`, counting `main`? -> … | correct | check r2.i4.frames |
| `items[4].widget.wrong[0]` | slip five = 5: You left out `main`, whose frame is at the bottom the whole time. | correct | check r2.i4.frames |
| `items[4].widget.wrong[1]` | slip four = 4: `depth(0)` is a call too, with its own frame. | correct | check r2.i4.frames |
| `items[4].feedback.correct` | `main` and five calls of `depth`. | correct | check r2.i4.frames |
| `items[4].explain.text` | While `depth(0)` runs, `depth(4)`, `depth(3)`, `depth(2)` and `depth(1)` are waiting, and `main` is under the… | correct | check r2.i4.frames |
| `items[5].prose` | `Position` prints `open` and `close` from its constructor and destructor. ```cpp { std::vector<std::unique_pt… | correct | check r2.i5.scope |
| `items[5].widget.options[0]` | KEY: What does it print? -> `open AZN`, `close AZN`, `end` | correct | check r2.i5.scope |
| `items[5].widget.options[1]` | not: `open AZN`, `end`, `close AZN` / why: `book` owns the position and dies at the inner `}`, so the destruc… | correct | check r2.i5.scope |
| `items[5].widget.options[2]` | not: `open AZN`, `end` / why: `book` is a vector of `unique_ptr`s; when it dies, each owner deletes its posit… | correct | check r2.i5.scope |
| `items[5].feedback.correct` | The owner died at the inner brace. | correct | check r2.i5.scope |
| `items[5].explain.text` | `book` lives inside the braces. At the `}` the vector is destroyed, its `unique_ptr` deletes the position, an… | correct | check r2.i5.scope |
| `items[6].prose` | A small balance book earns interest once per period. | correct | check r2.i6.accrue |
| `items[6].widget.solution` | code: Write `accrue(balances, rates)`: change each balance in place; never change or copy the rates. (4 hidde… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; check r2.i6.accrue |
| `items[6].feedback.correct` | Changed in place, read in place. | correct | check r2.i6.accrue |
| `items[6].explain.text` | `balances` must reach the caller, so it is `std::vector<double>&`. `rates` is only read, and the tests pass i… | correct | check r2.i6.accrue |
| `items[7].widget.options[0]` | KEY: Which `Book` method should be marked `const`? -> `double best_bid()` | correct | checks l6.s3.widen, l6.s3.ok |
| `items[7].widget.options[1]` | not: `void add(const Order& o)` / why: `add` changes the book, so it cannot promise not to. The `const` on it… | correct | checks l6.s3.widen, l6.s3.ok |
| `items[7].widget.options[2]` | not: `void cancel(int id)` / why: Cancelling removes an order, which changes the book. | correct | checks l6.s3.widen, l6.s3.ok |
| `items[7].feedback.correct` | Readers are `const`; writers are not. | correct | checks l6.s3.widen, l6.s3.ok |
| `items[7].explain.text` | `best_bid()` only reads, so mark it `double best_bid() const;`. Then code holding a `const Book&`, such as a … | correct | checks l6.s3.widen, l6.s3.ok |

## review-3.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `items[0].prose` | `Quote` keeps `bid_ < ask_` as an invariant. Four drafts of `set_ask`: | correct | derivation: the correct draft tests a <= bid_ before storing; the three others traced by hand |
| `items[0].widget.options[0]` | KEY: Which draft keeps the invariant? -> `void set_ask(double a) { if (a <= bid_) throw std::invalid_argument… | correct | derivation: the correct draft tests a <= bid_ before storing; the three others traced by hand |
| `items[0].widget.options[1]` | not: `void set_ask(double a) { ask_ = a; if (ask_ <= bid_) std::cout << "crossed"; }` / why: It stores first … | correct | derivation: the correct draft tests a <= bid_ before storing; the three others traced by hand |
| `items[0].widget.options[2]` | not: `void set_ask(double a) { ask_ = a; }` / why: It skips the check, so any ask goes in, even one below the… | correct | derivation: the correct draft tests a <= bid_ before storing; the three others traced by hand |
| `items[0].widget.options[3]` | not: `void set_ask(double a) { if (a >= bid_) throw std::invalid_argument(""); ask_ = a; }` / why: The test i… | correct | derivation: the correct draft tests a <= bid_ before storing; the three others traced by hand |
| `items[0].feedback.correct` | Check first, then store. | correct | derivation: the correct draft tests a <= bid_ before storing; the three others traced by hand |
| `items[0].explain.text` | A changing function checks before it stores, so a refused call leaves the object as it was. An ask equal to t… | correct | derivation: the correct draft tests a <= bid_ before storing; the three others traced by hand |
| `items[1].prose` | `Logger` prints `open` and `close` with its name. ```cpp class Desk { public: Desk() : feed_("feed"), risk_("… | correct | check r3.i1.desk-order |
| `items[1].widget.answer` | KEY order: `open feed` > `open risk` > `desk open` > `desk close` > `close risk` > `close feed` | correct | check r3.i1.desk-order |
| `items[1].feedback.correct` | Members first, then the body; on the way out, the reverse. | correct | check r3.i1.desk-order |
| `items[1].feedback.byKey.do` | The constructor's body runs only after every member has been built. | correct | check r3.i1.desk-order |
| `items[1].feedback.byKey.cf` | Members are destroyed in reverse declaration order: `risk_` before `feed_`. | correct | check r3.i1.desk-order |
| `items[1].feedback.byKey.dc` | The destructor's body runs first; the members it may use are destroyed after it. | correct | check r3.i1.desk-order |
| `items[1].explain.text` | The members are built in declaration order before the body prints `desk open`. Destruction mirrors it: the bo… | correct | check r3.i1.desk-order |
| `items[2].prose` | You want `std::cout << q` to print a `Quote`, and to chain with more `<<`. | correct | checks l12.s4.chain, l12.q2.stream-by-value; ISO C++17 (N4659) [over.binary]/1 (a member operator has the object on the left) |
| `items[2].widget.options[0]` | KEY: Which declaration do you write? -> `std::ostream& operator<<(std::ostream& os, const Quote& q)` | correct | checks l12.s4.chain, l12.q2.stream-by-value; ISO C++17 (N4659) [over.binary]/1 (a member operator has the object on the left) |
| `items[2].widget.options[1]` | not: `std::ostream operator<<(std::ostream os, const Quote& q)` / why: Streams cannot be copied, so neither t… | correct | checks l12.s4.chain, l12.q2.stream-by-value; ISO C++17 (N4659) [over.binary]/1 (a member operator has the object on the left) |
| `items[2].widget.options[2]` | not: `std::ostream& Quote::operator<<(std::ostream& os) const` / why: As a member, the `Quote` would be the l… | correct | checks l12.s4.chain, l12.q2.stream-by-value; ISO C++17 (N4659) [over.binary]/1 (a member operator has the object on the left) |
| `items[2].widget.options[3]` | not: `void operator<<(std::ostream& os, const Quote& q)` / why: It prints once, but returns nothing for the n… | correct | checks l12.s4.chain, l12.q2.stream-by-value; ISO C++17 (N4659) [over.binary]/1 (a member operator has the object on the left) |
| `items[2].feedback.correct` | Stream by reference in, the same stream out. | correct | checks l12.s4.chain, l12.q2.stream-by-value; ISO C++17 (N4659) [over.binary]/1 (a member operator has the object on the left) |
| `items[2].explain.text` | A free function puts the stream on the left. Taking and returning `std::ostream&` passes the one stream along… | correct | checks l12.s4.chain, l12.q2.stream-by-value; ISO C++17 (N4659) [over.binary]/1 (a member operator has the object on the left) |
| `items[3].prose` | ```cpp max_of(std::vector<int>{3, 1}); max_of(std::vector<std::string>{"AZN"}); max_of(std::vector<int>{8}); … | correct | ISO C++17 (N4659) [temp.inst]: int, std::string, double |
| `items[3].widget.answer` | KEY: How many functions does the compiler write from the `max_of` template? -> 3 (3: `int`, `std::string` and… | correct | ISO C++17 (N4659) [temp.inst]: int, std::string, double |
| `items[3].widget.wrong[0]` | slip calls = 5: You counted calls. Calls with the same type share one function. | correct | ISO C++17 (N4659) [temp.inst]: int, std::string, double |
| `items[3].widget.wrong[1]` | slip one = 1: Each type used gets its own function. | correct | ISO C++17 (N4659) [temp.inst]: int, std::string, double |
| `items[3].feedback.correct` | Three element types, three instantiations. | correct | ISO C++17 (N4659) [temp.inst]: int, std::string, double |
| `items[3].explain.text` | `int` and `std::string` are each used twice, `double` once: three instantiations, written at compile time. | correct | ISO C++17 (N4659) [temp.inst]: int, std::string, double |
| `items[4].prose` | A desk's risk limit caps the absolute exposure, long or short. A negative limit makes no sense, so it can nev… | correct | widget run: solution passes, starter fails |
| `items[4].widget.solution` | code: Finish `RiskLimit`: refuse a negative limit in the constructor and in `set`, and write `allows`, true w… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; widget run: solution passes, starter fails |
| `items[4].feedback.correct` | The limit can never go negative, through either door. | correct | widget run: solution passes, starter fails |
| `items[4].explain.text` | The constructor and `set` both refuse a negative value, so no `RiskLimit` ever holds one. `allows` checks bot… | correct | widget run: solution passes, starter fails |
| `items[5].prose` | Money now carries its currency. Adding pounds to dollars is a bug, so `+` refuses it. Two amounts are equal o… | correct | widget run: solution passes, starter does not compile |
| `items[5].widget.solution` | code: Write `Money operator+(const Money& a, const Money& b)` and `bool operator==(const Money& a, const Mone… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; widget run: solution passes, starter does not compile |
| `items[5].feedback.correct` | Mixed currencies are refused, never silently added. | correct | widget run: solution passes, starter does not compile |
| `items[5].explain.text` | `+` checks the currencies first, so £1 plus one dollar stops the program instead of giving 200 pence of nothi… | correct | widget run: solution passes, starter does not compile |
| `items[6].prose` | ```cpp class Pricer { std::string name_; std::unique_ptr<Lattice> grid_; public: explicit Pricer(std::string … | correct | checks r3.i6.move, r3.i6.copy, r3.i6.assign, r3.i6.const-move |
| `items[6].widget.options[0]` | KEY: Which line compiles? -> `Pricer b = std::move(a);` | correct | checks r3.i6.move, r3.i6.copy, r3.i6.assign, r3.i6.const-move |
| `items[6].widget.options[1]` | not: `Pricer b = a;` / why: The copy constructor is deleted, because `unique_ptr` cannot be copied. | correct | checks r3.i6.move, r3.i6.copy, r3.i6.assign, r3.i6.const-move |
| `items[6].widget.options[2]` | not: `Pricer b("tree"); b = a;` / why: Copy assignment is deleted for the same reason: one lattice cannot hav… | correct | checks r3.i6.move, r3.i6.copy, r3.i6.assign, r3.i6.const-move |
| `items[6].widget.options[3]` | not: `const Pricer c("tree"); Pricer b = std::move(c);` / why: A `const` object cannot be moved from, so this… | correct | checks r3.i6.move, r3.i6.copy, r3.i6.assign, r3.i6.const-move |
| `items[6].feedback.correct` | A `unique_ptr` member makes the class move-only. | correct | checks r3.i6.move, r3.i6.copy, r3.i6.assign, r3.i6.const-move |
| `items[6].explain.text` | With the rule of zero, `Pricer` gets what its members allow: moves, but no copies. Moving from a `const` obje… | correct | checks r3.i6.move, r3.i6.copy, r3.i6.assign, r3.i6.const-move |
| `items[7].prose` | A screen ranks values: the `n` largest, largest first. Write it once for any type with `<`. | correct | widget run: solution passes, starter does not compile; VOD, LLOY by check l13.s1.max-of ordering |
| `items[7].widget.solution` | code: Write `template <typename T> std::vector<T> top_n(std::vector<T> xs, int n)`. If `n` is larger than the… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; widget run: solution passes, starter does not compile; VOD, LLOY by check l13.s1.max-of ordering |
| `items[7].feedback.correct` | One template ranks numbers and tickers alike. | correct | widget run: solution passes, starter does not compile; VOD, LLOY by check l13.s1.max-of ordering |
| `items[7].explain.text` | `xs` is taken by value, so sorting it leaves the caller's vector alone. `std::sort` then `std::reverse` puts … | correct | widget run: solution passes, starter does not compile; VOD, LLOY by check l13.s1.max-of ordering |
| `items[8].prose` | On the bid side, the highest price trades first, and at the same price the earliest order. `Order` has `long … | correct | checks r3.i8.right, r3.i8.both, r3.i8.ask |
| `items[8].widget.options[0]` | KEY: Which body of `operator<(const Order& a, const Order& b)` puts bids in trading order? -> `return std::ti… | correct | checks r3.i8.right, r3.i8.both, r3.i8.ask |
| `items[8].widget.options[1]` | not: `return std::tie(b.price, b.time) < std::tie(a.price, a.time);` / why: That flips time as well, so at on… | correct | checks r3.i8.right, r3.i8.both, r3.i8.ask |
| `items[8].widget.options[2]` | not: `return std::tie(a.price, a.time) < std::tie(b.price, b.time);` / why: That is the ask side: lowest pric… | correct | checks r3.i8.right, r3.i8.both, r3.i8.ask |
| `items[8].widget.options[3]` | not: `return a.price > b.price;` / why: It ignores time, so orders at one price come out in any order. | correct | checks r3.i8.right, r3.i8.both, r3.i8.ask |
| `items[8].feedback.correct` | Price descending, then time ascending. | correct | checks r3.i8.right, r3.i8.both, r3.i8.ask |
| `items[8].explain.text` | Putting `b.price` on the left flips the price order, highest first, while `a.time` on the left keeps earlier … | correct | checks r3.i8.right, r3.i8.both, r3.i8.ask |

## homework-1.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `items[0].prose` | A backtest has `main.cpp` and `returns.cpp`, and both include `returns.h`. You build it with `g++ -std=c++17 … | correct | GCC manual 3.2; check l4.s7.multiple-definition |
| `items[0].widget.answer` | KEY order: The compiler reads `returns.h` into `main.cpp` and writes `main.o` > The compiler reads `returns.h… | correct | GCC manual 3.2; check l4.s7.multiple-definition |
| `items[0].feedback.correct` | Two separate compiles, one link, then run. | correct | GCC manual 3.2; check l4.s7.multiple-definition |
| `items[0].explain.text` | Each `.cpp` is compiled alone, in either order, each seeing `returns.h`. The linker then joins both object fi… | correct | GCC manual 3.2; check l4.s7.multiple-definition |
| `items[1].prose` | A file of closes arrives on `std::cin`: a header line, then one `date,close` line per day. The file may use W… | correct | checks h1.i1.fb-test-2, h1.i1.fb-test-6, h1.i1.falls |
| `items[1].widget.solution` | code: Print the maximum drawdown as `Max drawdown: 20.00%`, with two decimals. With no closes, print `Max dra… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks h1.i1.fb-test-2, h1.i1.fb-test-6, h1.i1.falls |
| `items[1].feedback.correct` | Parse, track the running peak, print once at the end. | correct | checks h1.i1.fb-test-2, h1.i1.fb-test-6, h1.i1.falls |
| `items[1].feedback.byKey.test-2` | With only a header, the loop never runs and the answer is 0.00%. If the program stopped, something read a clo… | correct | checks h1.i1.fb-test-2, h1.i1.fb-test-6, h1.i1.falls |
| `items[1].feedback.byKey.test-6` | Test 6 uses `\r\n` line ends and ends with a blank line. A line with no comma must be skipped, not passed to … | correct | checks h1.i1.fb-test-2, h1.i1.fb-test-6, h1.i1.falls |
| `items[1].feedback.byKey.test-4` | Test 4 has two falls: 262.50 to 199.50 (24%) and 275.00 to 247.50 (10%). Keep the worst, measured from the pe… | correct | checks h1.i1.fb-test-2, h1.i1.fb-test-6, h1.i1.falls |
| `items[1].feedback.byKey.error` | The program stopped. `std::stod` throws on text that is not a number, which is fatal here. Skip lines without… | imprecise | same as l3 screens[3]: the key `error` is never given for a program that stops; check h1.i1.fb-test-6 shows the route taken; finding 8 |
| `items[1].explain.text` | Read the header once, then loop on `std::getline`, skipping any line without a comma. Each close updates the … | correct | checks h1.i1.fb-test-2, h1.i1.fb-test-6, h1.i1.falls |
| `items[2].prose` | A mean-reversion rule compares the price with its moving average. Below the average by more than `band`: buy.… | correct | checks h1.i2.fb-test-4, h1.i2.fb-test-5 |
| `items[2].widget.solution` | code: Write `band_signal(price, average, band)` returning `"buy"`, `"sell"` or `"hold"`. (7 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; checks h1.i2.fb-test-4, h1.i2.fb-test-5 |
| `items[2].feedback.correct` | Strict tests on both sides, hold in between. | correct | checks h1.i2.fb-test-4, h1.i2.fb-test-5 |
| `items[2].feedback.byKey.test-4` | 98 is exactly `average - band`. The rule says the edge holds, so use `<`, not `<=`. | correct | checks h1.i2.fb-test-4, h1.i2.fb-test-5 |
| `items[2].feedback.byKey.test-5` | 102 is exactly `average + band`, so it holds. Use `>`, not `>=`. | correct | checks h1.i2.fb-test-4, h1.i2.fb-test-5 |
| `items[2].feedback.byKey.test-1` | 95 is more than 2 below 100, so buy. Compare `price < average - band`. | correct | checks h1.i2.fb-test-4, h1.i2.fb-test-5 |
| `items[2].explain.text` | An `if`, an `else if` and a final `return "hold"` cover the three cases. Strict `<` and `>` leave both edges … | correct | checks h1.i2.fb-test-4, h1.i2.fb-test-5 |
| `items[3].prose` | Each fill's size fits in an `int`, but a day's total may not. | correct | check h1.i3.fb-test-3 |
| `items[3].widget.solution` | code: Write `total_volume(fills)`: the sum of the fill sizes, as a `long long`. (5 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; check h1.i3.fb-test-3 |
| `items[3].feedback.correct` | Each `int` fill is added into a `long long` total. | correct | check h1.i3.fb-test-3 |
| `items[3].feedback.byKey.test-3` | Two fills of 2,000,000,000 should total 4,000,000,000. A negative or wrong total means the sum lived in an `i… | correct | check h1.i3.fb-test-3 |
| `items[3].explain.text` | `total` is a `long long`, so `total += f` converts each `int` fill up before adding. Nothing wraps until abou… | correct | check h1.i3.fb-test-3 |
| `items[4].prose` | ```cpp for (int i = 0; i < prices.size(); ++i) { ... } ``` `g++ -Wall` prints `warning: comparison of integer… | correct | check h1.i4.sign-compare |
| `items[4].widget.options[0]` | KEY: What is the best response? -> Make `i` a `std::size_t`, or compare with `static_cast<int>(prices.size())` | correct | check h1.i4.sign-compare |
| `items[4].widget.options[1]` | not: Change `<` to `<=` / why: That reads one past the end and keeps the warning. | correct | check h1.i4.sign-compare |
| `items[4].widget.options[2]` | not: Build without `-Wall` / why: That hides the warning and keeps the mixed comparison. A negative `int` com… | correct | check h1.i4.sign-compare |
| `items[4].widget.options[3]` | not: Make `i` a `double` / why: An index is a whole number. A `double` index is converted silently, and `i < … | correct | check h1.i4.sign-compare |
| `items[4].feedback.correct` | Compare like with like. | correct | check h1.i4.sign-compare |
| `items[4].explain.text` | `size()` returns an unsigned type, and comparing it with a signed `int` converts the `int`. Here it is harmle… | correct | check h1.i4.sign-compare |
| `items[5].prose` | ```cpp double price = 0.29; int pence = price * 100; ``` | correct | check h1.i5.pence |
| `items[5].widget.answer` | KEY: What does `pence` hold? -> 28 (28) | correct | check h1.i5.pence |
| `items[5].widget.wrong[0]` | slip round = 29: You expected rounding. The product is a hair below 29, and converting a `double` to an `int`… | correct | check h1.i5.pence |
| `items[5].feedback.correct` | 0.29 × 100 is stored as 28.999999999999996, then truncated. | correct | check h1.i5.pence |
| `items[5].explain.text` | 0.29 is stored slightly low, so the product is 28.999999999999996 and the conversion truncates to 28. `std::l… | correct | check h1.i5.pence |
| `items[6].prompt` | A colleague ports a Python backtest to C++. Two results look wrong. ```cpp int total_qty = 0; for (int q : fi… | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].model (paragraph 1)` | **The volume.** `total_qty` is an `int`, which holds at most 2,147,483,647. Two fills of 1,500,000,000 make 3… | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].model (paragraph 2)` | **The average.** `total_qty / n_fills` divides two `int`s, so C++ does integer division and drops the fractio… | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].model (paragraph 3)` | **Why Python hid both.** Python integers grow without limit, so a sum never overflows, and `/` always gives a… | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].model (paragraph 4)` | **Fixes.** | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].model (paragraph 5)` | ```cpp long long total_qty = 0; // 64-bit: up to about 9.2e18 for (int q : fills) total_qty += q; double avg … | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].model (paragraph 6)` | Writing `(double)(total_qty / n_fills)` or `total_qty / n_fills * 1.0` would not help: the division has alrea… | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].model (paragraph 7)` | **Catching them sooner.** A unit test on a known large day fails at once on the `int` version. Two fills of 1… | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].rubric[0]` | Explains that `int` stops at 2,147,483,647 and that 3,000,000,000 wraps to −1,294,967,296 (or says it wraps b… | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].rubric[1]` | Explains that `int / int` is integer division, done before the result reaches the `double` | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].rubric[2]` | Says why Python hid both: unbounded integers and `/` always giving a float | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].rubric[3]` | Gives a correct fix for the total in code: a `long long` accumulator | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].rubric[4]` | Fixes the average in code by converting to `double` before dividing; notes that converting afterwards does no… | correct | checks h1.i6.model, h1.i6.avg |
| `items[6].rubric[5]` | Names a way to catch each sooner: a unit test with large or odd values, a sanitiser build for the overflow, o… | correct | checks h1.i6.model, h1.i6.avg |
| `items[7].prose` | ```text $ g++ -std=c++17 main.cpp pricer.cpp -o backtest /usr/bin/ld: /tmp/ccg6pEss.o: in function `simple_re… | correct | check l4.s7.multiple-definition (also that inline fixes it) |
| `items[7].widget.options[0]` | KEY: Which change fixes the build? -> Keep only the declaration in `returns.h` and move the body into `return… | correct | check l4.s7.multiple-definition (also that inline fixes it) |
| `items[7].widget.options[1]` | not: Add include guards as well as `#pragma once` / why: Guards and `#pragma once` do the same job: one copy … | correct | check l4.s7.multiple-definition (also that inline fixes it) |
| `items[7].widget.options[2]` | not: Include `returns.h` in `main.cpp` only / why: Then `pricer.cpp` calls `simple_return` without a declarat… | correct | check l4.s7.multiple-definition (also that inline fixes it) |
| `items[7].widget.options[3]` | not: Put `pricer.cpp` before `main.cpp` in the command / why: The order of files does not matter. Both object… | correct | check l4.s7.multiple-definition (also that inline fixes it) |
| `items[7].feedback.correct` | Declarations in headers, one body in one `.cpp`. | correct | check l4.s7.multiple-definition (also that inline fixes it) |
| `items[7].explain.text` | Every `.cpp` that includes a header with a body compiles its own copy, and the linker refuses two. A declarat… | correct | check l4.s7.multiple-definition (also that inline fixes it) |
| `items[8].prose` | A feed gives each trade's price in ticks and its size in shares, in time order. The tick rule guesses which s… | correct | check h1.i8.tick-rule; tick test: Lee and Ready (1991), Journal of Finance 46(2), section I |
| `items[8].widget.solution` | code: Write `long long signed_volume(const std::vector<int>& prices, const std::vector<int>& sizes)`. (10 hid… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; check h1.i8.tick-rule; tick test: Lee and Ready (1991), Journal of Finance 46(2), section I |
| `items[8].feedback.correct` | Correct. The sign carries through flat trades, and the total lives in a `long long`. | correct | check h1.i8.tick-rule; tick test: Lee and Ready (1991), Journal of Finance 46(2), section I |
| `items[8].explain.text` | The first trade has sign 0, so start at the second and compare each price with the one before. A flat trade c… | correct | check h1.i8.tick-rule; tick test: Lee and Ready (1991), Journal of Finance 46(2), section I |

## homework-2.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `items[0].prose` | A position book in £ holds one `Position` per symbol (hidden above your code): ```cpp struct Position { std::… | correct | check h2.i0.fb-test-1 |
| `items[0].widget.solution` | code: Write `apply_fills(book, fills)`. (9 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; check h2.i0.fb-test-1 |
| `items[0].feedback.correct` | Every fill lands on the caller's book. | correct | check h2.i0.fb-test-1 |
| `items[0].feedback.byKey.test-1` | The quantity did not change. If you loop with `for (Position p : book)`, each `p` is a copy: use `Position& p… | correct | check h2.i0.fb-test-1 |
| `items[0].explain.text` | `book` is a plain reference, as the caller's positions change; `fills` is only read, so `const&` also accepts… | correct | check h2.i0.fb-test-1 |
| `items[1].prose` | A day's executions arrive on `std::cin`: a count `n`, then `n` lines of `qty price`. A quantity of 0 or less … | correct | check h2.i1.fb-test-4 |
| `items[1].widget.solution` | code: Complete the program. (6 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; check h2.i1.fb-test-4 |
| `items[1].feedback.correct` | Read once, pass by `const&`, print to four decimals. | correct | check h2.i1.fb-test-4 |
| `items[1].feedback.byKey.test-4` | 2,500,000,000 shares does not fit in an `int`. Keep quantities as `long long`, as `Order` does. | correct | check h2.i1.fb-test-4 |
| `items[1].explain.text` | The orders are read once into a vector, and every function after that takes `const std::vector<Order>&`, so n… | correct | check h2.i1.fb-test-4 |
| `items[2].prose` | ```cpp double payoff(double s, double k) { return s > k ? s - k : 0; } double price_option(double s, double k… | correct | check h2.i2.payoff |
| `items[2].widget.answer` | KEY order: Push `main`: the program starts > Push `price_option(100, 95)`: `main` calls it > Push `payoff(110… | correct | check h2.i2.payoff |
| `items[2].feedback.correct` | At most three frames, pushed and popped in strict order. | correct | check h2.i2.payoff |
| `items[2].explain.text` | Each `payoff` call returns before the next starts, so the stack is at most three deep: `main`, `price_option`… | correct | check h2.i2.payoff |
| `items[3].widget.options[0]` | KEY: Select all that apply: which `OrderBook` methods should be marked `const`? -> `double best_bid()` | correct | checks l6.s3.widen, l6.s3.ok |
| `items[3].widget.options[1]` | KEY: Select all that apply: which `OrderBook` methods should be marked `const`? -> `std::size_t depth()` | correct | checks l6.s3.widen, l6.s3.ok |
| `items[3].widget.options[2]` | not: `void add(const Order& o)` / why: `add` changes the book. The `const` on its parameter protects `o`, not… | correct | checks l6.s3.widen, l6.s3.ok |
| `items[3].widget.options[3]` | not: `bool cancel(long long id)` / why: Cancelling removes an order, so it changes the book. | correct | checks l6.s3.widen, l6.s3.ok |
| `items[3].feedback.correct` | Mark every reader `const`. | correct | checks l6.s3.widen, l6.s3.ok |
| `items[3].explain.text` | `best_bid` and `depth` only read, so mark them `const`. A pricer holding a `const OrderBook&` can then call t… | correct | checks l6.s3.widen, l6.s3.ok |
| `items[4].prose` | A pricer allocates `new double[steps + 1]` per call and forgets the `delete[]`. A calibration calls it 10,000… | correct | check h2.numbers |
| `items[4].widget.answer` | KEY: How many MB does a day's calibration leak? Take 1 MB as 1,000,000 bytes. -> 40.08 (40.08 MB: 10,000 call… | correct | check h2.numbers |
| `items[4].widget.wrong[0]` | slip n = 40: You used 500 doubles per call. The lattice has `steps + 1` = 501. | correct | check h2.numbers |
| `items[4].widget.wrong[1]` | slip one = 0.004008: That is one call. Multiply by 10,000 calls. | correct | check h2.numbers |
| `items[4].widget.wrong[2]` | slip bytes = 40080000: That is the count in bytes. Divide by 1,000,000. | correct | check h2.numbers |
| `items[4].feedback.correct` | 501 doubles, 8 bytes each, 10,000 times. | correct | check h2.numbers |
| `items[4].explain.text` | Each call leaks `new double[501]`, 4,008 bytes. 10,000 calls leak 40,080,000 bytes, about 40 MB a day. A `std… | correct | check h2.numbers |
| `items[5].prose` | Each snippet ran in this browser build without stopping. | wrong | check h2.i5.at: `v.at(5)` ends the run with an uncaught std::out_of_range (exit status 134); finding 1 |
| `items[5].widget.options[0]` | KEY: Select all that apply: which are undefined behaviour? -> `int* p = nullptr; int x = *p;` | correct | checks h2.i5.null, h2.i5.mismatch, h2.i5.twice, h2.i5.at, h2.i5.zero |
| `items[5].widget.options[1]` | KEY: Select all that apply: which are undefined behaviour? -> `double* q = new double[4]; delete q;` | correct | checks h2.i5.null, h2.i5.mismatch, h2.i5.twice, h2.i5.at, h2.i5.zero |
| `items[5].widget.options[2]` | KEY: Select all that apply: which are undefined behaviour? -> `double* r = new double(1.0); delete r; delete … | correct | checks h2.i5.null, h2.i5.mismatch, h2.i5.twice, h2.i5.at, h2.i5.zero |
| `items[5].widget.options[3]` | not: `std::vector<double> v(3); double y = v.at(5);` / why: `at` checks the index and throws `std::out_of_ran… | correct | checks h2.i5.null, h2.i5.mismatch, h2.i5.twice, h2.i5.at, h2.i5.zero |
| `items[5].widget.options[4]` | not: `double* s = new double[0]; delete[] s;` / why: A zero-length `new[]` is legal and `delete[]` is its mat… | correct | checks h2.i5.null, h2.i5.mismatch, h2.i5.twice, h2.i5.at, h2.i5.zero |
| `items[5].feedback.correct` | Null read, mismatched delete, double delete. | correct | checks h2.i5.null, h2.i5.mismatch, h2.i5.twice, h2.i5.at, h2.i5.zero |
| `items[5].explain.text` | Here all three undefined lines ran quietly: the null read gave a stray number, and both bad deletes were sile… | correct | checks h2.i5.null, h2.i5.mismatch, h2.i5.twice, h2.i5.at, h2.i5.zero |
| `items[6].prose` | ```cpp std::vector<double> px{100.0, 101.0, 102.0}; const double& first = px[0]; px.push_back(103.0); std::co… | correct | checks h2.i6.realloc, h2.i6.asan |
| `items[6].widget.options[0]` | KEY: What does `first` print? -> Anything: `push_back` may move the elements, leaving `first` dangling | correct | checks h2.i6.realloc, h2.i6.asan |
| `items[6].widget.options[1]` | not: `100` / why: That assumes the elements stay put. A full vector moves them to a bigger buffer, so `first`… | correct | checks h2.i6.realloc, h2.i6.asan |
| `items[6].widget.options[2]` | not: `103` / why: `first` was bound to the old `px[0]`, not to the last element. And after the move it refers… | correct | checks h2.i6.realloc, h2.i6.asan |
| `items[6].widget.options[3]` | not: It does not compile / why: It compiles. The compiler cannot know the vector will grow at run time. | correct | checks h2.i6.realloc, h2.i6.asan |
| `items[6].feedback.correct` | A reference into a vector dies when the vector grows. | correct | checks h2.i6.realloc, h2.i6.asan |
| `items[6].explain.text` | The vector was full, so `push_back` moved its elements to a new buffer and freed the old one. `first` still r… | unverified | check h2.i6.realloc: the same snippet printed 2.93542e-306 here, not the quoted 2.8974e-306 (the sentence says "a test run printed", so it claims no guarantee); check h2.i6.asan holds |
| `items[7].prompt` | A colleague's utilities for a trade blotter, in £: ```cpp struct Trade { std::string sym; int qty; double px;… | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].model (paragraph 1)` | **(a)** Cost: `trades` is taken by value, so every call copies the whole blotter, every `std::string` include… | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].model (paragraph 2)` | **(b)** `best` is a local, so it dies at the closing brace, and `&best` is a dangling pointer. clang warns "a… | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].model (paragraph 3)` | **(c)** `t` is a copy of the caller's trade. The fee is added to the copy, which dies at the `}`, so the call… | imprecise | "which dies at the }": the copy of a Trade (it holds a std::string) dies at the end of the calling full-expression on this build and on a desk build; checks l5.s0.param-lifetime(-desk); finding 5 |
| `items[7].model (paragraph 4)` | **(d)** It returns a raw owning pointer: every caller must remember `delete`, on every path, exactly once. On… | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].model (paragraph 5)` | **(e)** | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].model (paragraph 6)` | ```cpp double total_notional(const std::vector<Trade>& trades) { double sum = 0; for (const Trade& t : trades… | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].model (paragraph 7)` | std::optional<Trade> best_trade(const std::vector<Trade>& trades) { if (trades.empty()) return std::nullopt; … | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].model (paragraph 8)` | void add_fee(Trade& t, double fee) { t.px += fee; } | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].model (paragraph 9)` | std::unique_ptr<Pricer> make_pricer() { return std::make_unique<Pricer>(); } ``` | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].rubric[0]` | (a) Says the by-value parameter copies the whole blotter on each call and should be `const std::vector<Trade>… | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].rubric[1]` | (a) Says the off-by-one is undefined behaviour: libc++'s check stops it here, while a desk build may silently… | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].rubric[2]` | (b) Says `&best` dangles once its local dies at the `}`; proposes returning by value (`std::optional<Trade>` … | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].rubric[3]` | (b) Notes the parameter should be `const&`, the loop variable `const Trade&`, and that an empty blotter makes… | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].rubric[4]` | (c) Explains that `add_fee` changes a copy and needs `Trade&` | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].rubric[5]` | (d) Says the raw `new` makes every caller responsible for exactly one `delete`, and replaces it with `std::un… | correct | checks h2.i7.off-by-one, h2.i7.model-e |
| `items[7].rubric[6]` | (e) Gives four corrected functions that compile and match the fixes above | correct | checks h2.i7.off-by-one, h2.i7.model-e |

## homework-3.json

| JSON path | claim (short) | verdict | basis |
|---|---|---|---|
| `items[0].prose` | `Logger` prints `open` and `close` with its name. ```cpp int main() { Logger a("a"); { Logger b("b"); Logger(… | correct | checks l11.q0.temporary, l11.s2.scopes; ISO C++17 (N4659) [class.temporary]/4 |
| `items[0].widget.answer` | KEY order: `open a` > `open b` > `open tmp` > `close tmp` > `work` > `close b` > `end` > `close a` | correct | checks l11.q0.temporary, l11.s2.scopes; ISO C++17 (N4659) [class.temporary]/4 |
| `items[0].feedback.correct` | The temporary dies at its semicolon; the named objects at their braces. | correct | checks l11.q0.temporary, l11.s2.scopes; ISO C++17 (N4659) [class.temporary]/4 |
| `items[0].feedback.byKey.w` | The temporary has already closed by then: it dies at the `;` on its own line. | correct | checks l11.q0.temporary, l11.s2.scopes; ISO C++17 (N4659) [class.temporary]/4 |
| `items[0].feedback.byKey.cb` | `b` lives until the inner closing brace, after `work`. | correct | checks l11.q0.temporary, l11.s2.scopes; ISO C++17 (N4659) [class.temporary]/4 |
| `items[0].feedback.byKey.e` | `end` prints after the inner block has closed `b`. | correct | checks l11.q0.temporary, l11.s2.scopes; ISO C++17 (N4659) [class.temporary]/4 |
| `items[0].feedback.byKey.ca` | `a` lives until the end of `main`, after `end`. | correct | checks l11.q0.temporary, l11.s2.scopes; ISO C++17 (N4659) [class.temporary]/4 |
| `items[0].explain.text` | `Logger("tmp");` is born and dies on one line. `b` ends at the inner brace, before `end`, and `a` at the end … | correct | checks l11.q0.temporary, l11.s2.scopes; ISO C++17 (N4659) [class.temporary]/4 |
| `items[1].prose` | A position: buy 200 at £50.00, buy 100 at £53.00, sell 150, buy 50 at £56.00. | correct | check h3.numbers |
| `items[1].widget.answer` | KEY: What is the average price at the end, in pounds? -> 52.25 (£52.25: £51.00 on 300, then 150 left at £51.0… | correct | check h3.numbers |
| `items[1].widget.wrong[0]` | slip nosell = 51.7143: You kept all 300 shares in the last step. After selling 150, only 150 remain at £51.00. | correct | check h3.numbers |
| `items[1].widget.wrong[1]` | slip simple = 53.0: You averaged the three prices. Weight each by its shares. | correct | check h3.numbers |
| `items[1].feedback.correct` | £10,450 over 200 shares is £52.25. | correct | check h3.numbers |
| `items[1].explain.text` | The first two buys give $(10000 + 5300)/300 = 51$. Selling 150 leaves 150 at £51.00. The last buy gives $(765… | correct | check h3.numbers |
| `items[2].prose` | Extend your `Position`: `sell(qty, px)` now returns the P&L of that sale, $q \times (p - \bar p)$, and adds i… | correct | widget run: solution passes, starter fails; check h3.numbers |
| `items[2].widget.solution` | code: Write `buy` and `sell` with every check: no short sales, and no quantity or price of 0 or less. A flat … | correct | widget run (solution passes every hidden test, starter fails) under the app grader; widget run: solution passes, starter fails; check h3.numbers |
| `items[2].feedback.correct` | Quantity, average and realised P&L stay consistent. | correct | widget run: solution passes, starter fails; check h3.numbers |
| `items[2].explain.text` | A sale earns $q(p - \bar p)$ against the average cost and leaves the average alone. Selling 150 at £55.00 aga… | correct | widget run: solution passes, starter fails; check h3.numbers |
| `items[3].prose` | `Fixed<Places>` holds a value as a whole number of $10^{-\text{Places}}$ units. `Fixed<2>` is pence and `Fixe… | correct | widget run: solution passes, starter does not compile |
| `items[3].widget.solution` | code: Write `str()` and `operator+` for two values of the same `Fixed<Places>`. In `str()`, 1234 units of `Fi… | correct | widget run (solution passes every hidden test, starter fails) under the app grader; widget run: solution passes, starter does not compile |
| `items[3].feedback.correct` | Exact decimals, with the places fixed at compile time. | correct | widget run: solution passes, starter does not compile |
| `items[3].explain.text` | `str()` splits the absolute units by $10^{\text{Places}}$ and pads the fraction to `Places` digits. Because `… | correct | widget run: solution passes, starter does not compile |
| `items[4].prose` | ```cpp class Prices { public: explicit Prices(int n) : data_(new double[n]) {} ~Prices() { delete[] data_; } … | correct | check h3.i4.vector |
| `items[4].widget.options[0]` | KEY: Which change makes copying a `Prices` safe? -> Replace `double*` with `std::vector<double>`, built with … | correct | check h3.i4.vector |
| `items[4].widget.options[1]` | not: Add `Prices(const Prices&) = default;` / why: The default copy still copies the address, so the block is… | correct | check h3.i4.vector |
| `items[4].widget.options[2]` | not: Remove the destructor / why: Then nothing is freed twice, but nothing is freed at all: every `Prices` le… | correct | check h3.i4.vector |
| `items[4].widget.options[3]` | not: Make the member `double* const data_` / why: A const pointer still copies the same address. Two destruct… | correct | check h3.i4.vector |
| `items[4].feedback.correct` | Rule of zero: let a member own the memory. | correct | check h3.i4.vector |
| `items[4].explain.text` | A `std::vector<double>` copies its elements, frees them once, and moves cheaply. With it the class needs no s… | correct | check h3.i4.vector |
| `items[5].prose` | An order book holds bid and ask **levels**, each a price in pence and a total size. Bids are kept highest fir… | correct | widget run: solution passes, starter fails |
| `items[5].widget.solution` | code: Write `operator<` for `Level`, by price. Then write the `Book` functions `add`, `best_bid`, `best_ask` … | correct | widget run (solution passes every hidden test, starter fails) under the app grader; widget run: solution passes, starter fails |
| `items[5].feedback.correct` | The book stays sorted and never crosses. | correct | widget run: solution passes, starter fails |
| `items[5].explain.text` | `add` checks size and the crossing rule before touching either side, then merges into a level or inserts and … | correct | widget run: solution passes, starter fails |
| `items[6].prompt` | A desk asks you to design the C++ `Position` class its risk system will use. One object tracks one instrument… | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].model (paragraph 1)` | **(a) Invariants, and where they are checked.** | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].model (paragraph 2)` | 1. The ticker is not empty. *Checked in the constructor; nothing changes it afterwards.* 2. $/q/ \le$ the pos… | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].model (paragraph 3)` | **(b) Declaration.** | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].model (paragraph 4)` | ```cpp class Position { public: Position(std::string ticker, long long limit); void buy(long long qty, long l… | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].model (paragraph 5)` | The data is private, so only `buy` and `sell` can change it. Readers are `const`, and `ticker()` returns a `c… | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].model (paragraph 6)` | **(c) Special members.** None: the rule of zero. Every member (`std::string`, integers, a `double`) copies, m… | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].model (paragraph 7)` | **(d) Operators.** `operator<<(std::ostream&, const Position&)` for logs, returning the stream. `operator==` … | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].model (paragraph 8)` | **(e) Money and errors.** Prices and P&L are whole pence in `long long`, so sums are exact. Only the average,… | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].rubric[0]` | States at least three invariants and where each is checked. Examples: non-empty ticker, limit on /qty/, flat … | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].rubric[1]` | Data private; changes only through checked functions; readers `const`; no non-const reference to a member ret… | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].rubric[2]` | Initialiser list used in the constructor, with the check after the members are built | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].rubric[3]` | Rule of zero justified from the member types; says a raw resource would need the rule of five or `= delete` | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].rubric[4]` | Operators: `operator<<` returning `std::ostream&`; refuses `+` on positions (or on mixed units) with a reason | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[6].rubric[5]` | Money in integer pence (or ticks) with no `==` on doubles, and a refused call leaves the object unchanged | correct | C++ Core Guidelines C.2, C.20, C.21, C.160 to C.167; ISO C++17 (N4659) [class.base.init]/13 (declaration order) |
| `items[7].prose` | A risk screen tracks the lowest and highest value seen in a session. The value may be a price, a tick count o… | correct | widget run: solution passes (three compile probes included), starter does not compile; 2e9 - (-2e9) = 4e9 > 2,147,483,647 |
| `items[7].widget.solution` | code: Write `SessionRange<T>` and its operators to the specification above. (15 hidden tests) | correct | widget run (solution passes every hidden test, starter fails) under the app grader; widget run: solution passes (three compile probes included), starter does not compile; 2e9 - (-2e9) = 4e9 > 2,147,483,647 |
| `items[7].feedback.correct` | Correct. The ends stay in order, the operators agree, and `+=` hands back the range itself. | correct | widget run: solution passes (three compile probes included), starter does not compile; 2e9 - (-2e9) = 4e9 > 2,147,483,647 |
| `items[7].explain.text` | Every way to change a range goes through `add` or the checked constructor, so the low never passes the high. … | correct | widget run: solution passes (three compile probes included), starter does not compile; 2e9 - (-2e9) = 4e9 > 2,147,483,647 |
