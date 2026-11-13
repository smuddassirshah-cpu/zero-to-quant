# Claim ledger: cpp levels 1 to 3, blind audit round 3

Stage 1 course, full depth: one row for each prose block, canvas, key, wrong option, slip, hint, feedback line, explain, summary line, model answer and rubric line of the lessons, review sets and homework sets that `course.json` maps to levels 1 to 3. Every row was read and judged by the auditor. The basis column gives the standard section, derivation or run that settles it; the rows of one screen, quiz item or set item share a basis, written in full on the first row of the unit, and a row judged other than `correct` carries its own. Check names refer to `docs/reports/cpp-L1-3-r3-concepts.py`. Standard sections are ISO C++17 (N4659) stable names.

Rows: 2532. correct 2515, imprecise 11, unverified 5, wrong 1.

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l1-source-to-program | screens[0].prose | In Python you run the source file itself: `python3 main.py`. Here is a C++ session in a terminal. T… | correct | the two `ls` listings on the canvas; a compiler writes an executable file (ISO C++ [lex.phases] 7 to 9) |
| l1-source-to-program | screens[0].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].widget.answer | key: ["l3"] | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].hints[0] | hint: Which command makes a new file appear in the folder? | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].hints[1] | hint: Compare the two `ls` listings, before and after. | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].hints[2] | hint: The file `main` appears after line 3, so line 3 made it. | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].feedback.correct | `g++` read the text and wrote a new file, `main`. | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].feedback.generic | Not quite right. Look for the command that changes what `ls` lists. | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].feedback.byKey.l6 | You tapped the command that runs the program. By then `main` already existed: the `ls` on line 4 sh… | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].feedback.byKey.l7 | That is the program's output. Something had to build the program before it could print. | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].feedback.byKey.l1 | `ls` only lists the folder. Compare its two listings to see what changed between them. | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].feedback.byKey.l4 | `ls` only lists the folder. The command before it is the one that made `main`. | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].explain.text | `g++` is a **compiler**. It read `main.cpp` and wrote `main`, a file of machine instructions. `./ma… | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[0].explain.canvas.caption | caption: Line 3 builds `main`; line 6 runs it. | correct | unit basis: first row of screens[0] |
| l1-source-to-program | screens[1].prose | Inside that one `g++` command are two steps, drawn here. The program uses `std::cout` to print, yet… | correct | [lex.phases] 7 to 9: translation to an object file, then linking against the library; the g++ driver runs both |
| l1-source-to-program | screens[1].widget.answer | key: ["ld"] | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[1].hints[0] | hint: Follow the arrow that leaves the library box. | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[1].hints[1] | hint: The library's arrow ends at one step. | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[1].feedback.correct | The linker joins `main.o` and the library into one file. | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[1].feedback.generic | Not quite right. Follow the arrow out of the library box. | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[1].feedback.byKey.cc | The compiler sees only your file. `#include <iostream>` tells it `std::cout` exists, but the printi… | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[1].feedback.byKey.lib | That box holds the printing code, but it does nothing by itself. Find the step its arrow points to. | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[1].feedback.byKey.exe | That is the finished program, after the join. | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[1].feedback.byKey.obj | `main.o` is your code alone, with a gap where `std::cout` goes. | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[1].explain.text | The **compiler** turns `main.cpp` into an **object file**, `main.o`: machine code with gaps for nam… | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[1].explain.canvas.caption | caption: compile, then link | correct | unit basis: first row of screens[1] |
| l1-source-to-program | screens[2].prose | So the **compiler** makes an **object file** and the **linker** makes the **executable**. Python re… | correct | derivation from s1: the executable is a separate file that nothing rebuilds; Python re-reads its source each run |
| l1-source-to-program | screens[2].widget.options[0] | key: `Hello, market` | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].widget.options[1].why | wrong option: `Hello, desk` :: You expected `./main` to read `main.cpp`, as `python3` reads `main.p… | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].widget.options[2].why | wrong option: An error saying the source has changed :: Nothing checks the source when `./main` run… | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].widget.options[3].why | wrong option: Nothing, because saving deletes `main` :: Saving changes only `main.cpp`. The executa… | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].hints[0] | hint: Which box does `./main` run? | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].hints[1] | hint: The edit changed this box only. | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].hints[2] | hint: `main` was built from the old text. Nothing has rebuilt it. | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].feedback.correct | The executable still holds the old text. | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].feedback.generic | Not quite right. Ask which file `./main` actually runs. | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].feedback.byKey.new | You expected `./main` to read `main.cpp`, as `python3` reads `main.py`. It runs the executable, whi… | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].explain.text | `./main` runs the executable, which was built from the old text. The edit reaches it only when you … | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[2].explain.canvas.caption | caption: Edit `main.cpp`, then rebuild `main`. | correct | unit basis: first row of screens[2] |
| l1-source-to-program | screens[3].prose | Every C++ program starts in `int main()`. `#include <iostream>` brings in `std::cout`, and `<<` sen… | correct | run under the app compiler and grader: solution passes, starter fails; both exact-compare slips fail test 2 only (checks l1.s3); [basic.start.main] |
| l1-source-to-program | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l1-source-to-program | screens[3].widget | code: 3 tests; solution passes, starter fails | correct | unit basis: first row of screens[3] |
| l1-source-to-program | screens[3].hints[0] | hint: Start the line with `std::cout <<`. | correct | unit basis: first row of screens[3] |
| l1-source-to-program | screens[3].hints[1] | hint: The text goes in double quotes; the line end is `'\n'`. | correct | unit basis: first row of screens[3] |
| l1-source-to-program | screens[3].hints[2] | hint: `std::cout << "Hello, market" << '\n';` inside `main`, before `return 0;`. | correct | unit basis: first row of screens[3] |
| l1-source-to-program | screens[3].feedback.correct | That is a complete C++ program. | correct | unit basis: first row of screens[3] |
| l1-source-to-program | screens[3].feedback.generic | Not quite right. Compare your output with the expected line under the editor. | correct | unit basis: first row of screens[3] |
| l1-source-to-program | screens[3].feedback.byKey.compile | The compiler stopped. Read the first `error:` line under the editor: it names the line and the colu… | correct | unit basis: first row of screens[3] |
| l1-source-to-program | screens[3].feedback.byKey.test-2 | The words match but not every character. Test 2 compares exactly: one `'\n'` at the end, no space b… | correct | unit basis: first row of screens[3] |
| l1-source-to-program | screens[3].explain.text | `std::cout` is the screen, and `<<` pushes each piece onto it in order. `return 0;` tells the shell… | correct | unit basis: first row of screens[3] |
| l1-source-to-program | screens[4].prose | `std::cin >> x` reads the next word typed into `x`, skipping spaces and line breaks. Unlike Python'… | correct | [istream.formatted]: >> skips whitespace and converts; run under the app compiler and grader: getline slip fails test 2, fixed-decimals slip fails test 1 (checks l1.s4) |
| l1-source-to-program | screens[4].canvas.state.caption | caption: You type lines 2 and 3; the program prints lines 4 and 5. | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[4].widget | code: 4 tests; solution passes, starter fails | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[4].hints[0] | hint: One `std::cin` line can read both: `std::cin >> ticker >> price;`. | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[4].hints[1] | hint: Test 2 types both on one line. `>>` skips the space for you. | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[4].hints[2] | hint: Then two `std::cout` lines, each ending with `'\n'`. | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[4].feedback.correct | `>>` read a word, then a number, and converted it. | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[4].feedback.generic | Not quite right. Compare the first failing test's output with the expected lines. | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[4].feedback.byKey.test-2 | Test 2 types `BARC 215.35` on one line. `std::cin >>` stops at the space, so read twice with `>>`, … | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[4].feedback.byKey.test-1 | Test 1 expects `Ticker: VOD`, then `Price: 72.5`. If your price shows as `72.50`, leave the number … | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[4].explain.text | `std::cin >> ticker >> price;` reads a word into the `std::string`, then converts the next word int… | correct | unit basis: first row of screens[4] |
| l1-source-to-program | screens[5].prose | You forget a semicolon and build. g++ prints an error in the shape `file:line:column: error: messag… | correct | run, g++ 13.3: `main.cpp:5:5: error: expected ',' or ';' before 'std'` under `In function 'int main()'` (check l1.s5) |
| l1-source-to-program | screens[5].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[5] |
| l1-source-to-program | screens[5].widget.answer | key: ["l5"] | correct | unit basis: first row of screens[5] |
| l1-source-to-program | screens[5].hints[0] | hint: Read the number straight after `main.cpp:` in the error line. | correct | unit basis: first row of screens[5] |
| l1-source-to-program | screens[5].hints[1] | hint: That error line is marked red. | correct | unit basis: first row of screens[5] |
| l1-source-to-program | screens[5].hints[2] | hint: `main.cpp:5:5` means line 5, column 5. | correct | unit basis: first row of screens[5] |
| l1-source-to-program | screens[5].feedback.correct | The error names line 5, column 5. | correct | unit basis: first row of screens[5] |
| l1-source-to-program | screens[5].feedback.generic | Not quite right. Read the first number after `main.cpp:`. | correct | unit basis: first row of screens[5] |
| l1-source-to-program | screens[5].feedback.byKey.l4 | That is where the slip is, and we come to it next. The error itself names line 5: read the number a… | correct | unit basis: first row of screens[5] |
| l1-source-to-program | screens[5].feedback.byKey.l6 | The error names line 5. Read the first number after `main.cpp:`. | correct | unit basis: first row of screens[5] |
| l1-source-to-program | screens[5].explain.text | `main.cpp:5:5` is the file, then line 5, then column 5. g++ also prints that line with a caret unde… | correct | unit basis: first row of screens[5] |
| l1-source-to-program | screens[6].prose | Same error. Line 5 looks perfectly fine, though: it is the same `std::cout` line that worked before. | correct | run, app clang 21: `main.cpp:4:25: error: expected ';' at end of declaration` (check l1.s6); g++ line as s5 |
| l1-source-to-program | screens[6].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[6] |
| l1-source-to-program | screens[6].widget.answer | key: ["l4"] | correct | unit basis: first row of screens[6] |
| l1-source-to-program | screens[6].hints[0] | hint: The message says what it expected: `','` or `';'`. | correct | unit basis: first row of screens[6] |
| l1-source-to-program | screens[6].hints[1] | hint: Look at how the line above line 5 ends. | correct | unit basis: first row of screens[6] |
| l1-source-to-program | screens[6].hints[2] | hint: `double price = 101.5` never ends, so the compiler read on into line 5. | correct | unit basis: first row of screens[6] |
| l1-source-to-program | screens[6].feedback.correct | Line 4 is missing its `;`. | correct | unit basis: first row of screens[6] |
| l1-source-to-program | screens[6].feedback.generic | Not quite right. Look at the end of the line above the one the error names. | correct | unit basis: first row of screens[6] |
| l1-source-to-program | screens[6].feedback.byKey.l5 | Line 5 is where g++ noticed, not where the slip is. The declaration on line 4 never ended, so the c… | correct | unit basis: first row of screens[6] |
| l1-source-to-program | screens[6].explain.text | g++ reports where it got confused, often the line after the slip. Clang, the compiler in this app, … | correct | unit basis: first row of screens[6] |
| l1-source-to-program | screens[7].prose | This time `main.cpp` has no `return 0;`, and you build with `-Wall`, which asks for extra warnings.… | correct | run, g++ -Wall: warning text and 4:9, the build runs (check l1.s7); [basic.start.main]/5: falling off main returns 0; [stmt.return]/2 for other functions |
| l1-source-to-program | screens[7].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[7].widget.options[0] | key: It built and ran: a warning is advice, and `main` returns 0 by itself | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[7].widget.options[1].why | wrong option: It did not build, because of the warning :: You read `warning` as `error`. Only an er… | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[7].widget.options[2].why | wrong option: It built, but `main` returns a random exit code :: `main` is the one function where r… | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[7].widget.options[3].why | wrong option: It built only because `-Wall` was given :: `-Wall` asks for more warnings. It never m… | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[7].hints[0] | hint: Is there an `error:` anywhere in the output? | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[7].hints[1] | hint: Line 6 tries to run the program. | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[7].feedback.correct | A warning flags something odd; it does not stop the build. | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[7].feedback.generic | Not quite right. Look for the word `error` and for what line 6 does. | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[7].feedback.byKey.nobuild | You read `warning` as `error`. Only an error stops the build, and line 6 shows `./main` running. | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[7].explain.text | g++ built `main` despite the warning, which only says `qty` is never used. `main` may end without `… | correct | unit basis: first row of screens[7] |
| l1-source-to-program | screens[8].prose | Most Python habits stop the build: a missing `;` or `print(...)`. Two do not: an indented second li… | correct | run: prints 0; g++ silent without -Wall and warns with it; app clang warns by default with -Wparentheses (checks l1.s8); [expr.ass]/1, [conv.bool] |
| l1-source-to-program | screens[8].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].widget.options[0] | key: `0` | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].widget.options[1].why | wrong option: `3` :: You read `=` as `==`. The test is false, so `flat` is skipped, but `=` still s… | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].widget.options[2].why | wrong option: `flat`, then `0` :: `signals = 0` has the value 0, and 0 counts as false. The body of… | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].widget.options[3].why | wrong option: Nothing: it does not compile :: In Python, `if signals = 0:` is a syntax error. C++ a… | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].hints[0] | hint: In C++, `=` always stores a value, even inside `if ( )`. | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].hints[1] | hint: After `signals = 0`, what does `signals` hold? That is what line 3 shows. | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].hints[2] | hint: The condition's value is 0, which is false, and `signals` is now 0. | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].feedback.correct | The `if` stored 0 and then tested it. | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].feedback.generic | Not quite right. Treat `=` as storing, wherever it appears. | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].feedback.byKey.three | You read `=` as `==`. The condition stored 0 in `signals`, so the last line prints 0. | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].feedback.byKey.noc | You expected the Python rule. C++ accepts an assignment as a condition, so this builds and runs. | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].explain.text | `signals = 0` stores 0 and has the value 0, which is false. The test was meant to be `signals == 0`… | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[8].explain.canvas.lines | canvas: $ g++ -std=c++17 main.cpp -o main / $ ./main / 0 | correct | unit basis: first row of screens[8] |
| l1-source-to-program | screens[9].prose | Put the life of a C++ program in order, from typing it to the shell hearing it finished. | correct | order follows s1 and [basic.start.main]; the shell reads the exit status |
| l1-source-to-program | screens[9].widget.answer | key: ["s1", "s2", "s3", "s4", "s5"] | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].widget.lines.s1 | step: You write and save `main.cpp` | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].widget.lines.s2 | step: The compiler turns it into `main.o`, with gaps for `std::cout` | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].widget.lines.s3 | step: The linker fills the gaps from the library and writes `main` | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].widget.lines.s4 | step: `./main` loads the executable and calls `main()` | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].widget.lines.s5 | step: `main` returns 0, and the shell reads that as success | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].hints[0] | hint: Nothing can run until the executable exists. | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].hints[1] | hint: The object file comes before the executable. | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].hints[2] | hint: Write, compile, link, run, return. | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].feedback.correct | Write, compile, link, run, return. | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].feedback.generic | Not quite right. Follow the arrows on the diagram. | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[9].explain.text | The diagram is the order: source, compiler, object file, linker, executable. Running comes last, an… | correct | unit basis: first row of screens[9] |
| l1-source-to-program | screens[10].prose | C++ suits pricers: a compiled loop, such as a binomial tree, runs many times faster than the same l… | correct | run, g++ 13.3: first error line as quoted and 232 lines in all (checks l1.s10); positional keys checked (check l1.s10 byKey); speed remark timed (check l1.s10 compiled loop) |
| l1-source-to-program | screens[10].canvas.state.caption | caption: Long lines scroll sideways. | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].widget.answer | key: ["l2"] | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].hints[0] | hint: Skip every line that says `note:`. | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].hints[1] | hint: Only one line says `error:`. | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].hints[2] | hint: Read it as: there is no `<<` that takes a stream on the left and a vector on the right. | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].feedback.correct | No `<<` exists for a stream and a whole vector. | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].feedback.generic | Not quite right. Look for the one line marked `error:` in your own file. | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].feedback.byKey.l6 | You picked a `note:`. Notes list every `<<` the compiler tried and rejected; the problem is stated … | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].feedback.byKey.l7 | You picked a `note:`. Notes list every `<<` the compiler tried and rejected; the problem is stated … | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].feedback.byKey.l8 | You picked a `note:`. The notes only list rejected candidates. Read the `error:` line instead. | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].feedback.byKey.l5 | That line says which header the notes come from. The problem itself is in the `error:` line. | correct | unit basis: first row of screens[10] |
| l1-source-to-program | screens[10].explain.text | In words: `std::cout` has no `<<` for a whole `std::vector<double>`, so loop and print each close. … | correct | unit basis: first row of screens[10] |
| l1-source-to-program | quiz[0].prose | ```text main.cpp:5:18: error: 'pirce' was not declared in this scope; did you mean 'price'? 5 \| st… | correct | run, g++ 13.3: `main.cpp:5:18: error: 'pirce' was not declared in this scope; did you mean 'price'?` (check l1.quiz0) |
| l1-source-to-program | quiz[0].widget.options[0] | key: Change `pirce` to `price` on line 5 | correct | unit basis: first row of quiz[0] |
| l1-source-to-program | quiz[0].widget.options[1].why | wrong option: Declare a new variable `pirce` above line 5 :: That silences the error but prints a d… | correct | unit basis: first row of quiz[0] |
| l1-source-to-program | quiz[0].widget.options[2].why | wrong option: Add `#include <pirce>` :: Headers bring in library names. `pirce` is a misspelling of… | correct | unit basis: first row of quiz[0] |
| l1-source-to-program | quiz[0].widget.options[3].why | wrong option: Add a semicolon to line 4 :: A missing semicolon gives `expected ';'`. This message s… | correct | unit basis: first row of quiz[0] |
| l1-source-to-program | quiz[0].feedback.correct | A typo in a name: the compiler even suggests the fix. | correct | unit basis: first row of quiz[0] |
| l1-source-to-program | quiz[0].feedback.generic | Not quite right. Read the end of the message: `did you mean`. | correct | unit basis: first row of quiz[0] |
| l1-source-to-program | quiz[0].explain.text | "Not declared in this scope" means the compiler has never met that name. Here it is a typo, and the… | correct | unit basis: first row of quiz[0] |
| l1-source-to-program | quiz[1].prose | You build with `g++ -std=c++17 prices.cpp -o pricer`. | correct | GCC manual, Overall Options: -o names the output file; `./` is the current folder |
| l1-source-to-program | quiz[1].widget.options[0] | key: `./pricer` | correct | unit basis: first row of quiz[1] |
| l1-source-to-program | quiz[1].widget.options[1].why | wrong option: `./prices.cpp` :: `prices.cpp` is the source text. The machine runs the executable th… | correct | unit basis: first row of quiz[1] |
| l1-source-to-program | quiz[1].widget.options[2].why | wrong option: `python3 pricer` :: `pricer` is machine code, not Python. Run it directly with `./`. | correct | unit basis: first row of quiz[1] |
| l1-source-to-program | quiz[1].widget.options[3].why | wrong option: `g++ pricer` :: `g++` builds programs; it does not run them. | correct | unit basis: first row of quiz[1] |
| l1-source-to-program | quiz[1].feedback.correct | `-o pricer` named the executable. | correct | unit basis: first row of quiz[1] |
| l1-source-to-program | quiz[1].feedback.generic | Not quite right. `-o` names the output file. | correct | unit basis: first row of quiz[1] |
| l1-source-to-program | quiz[1].explain.text | `-o pricer` tells g++ to call the executable `pricer`. `./` means "in this folder", so `./pricer` r… | correct | unit basis: first row of quiz[1] |
| l1-source-to-program | quiz[2].prose | The program starts with `#include <iostream>` and nothing else above `main`. | correct | [namespace.std], [stmt.expr]: a qualified name and a closing semicolon; print is not a C++ name |
| l1-source-to-program | quiz[2].widget.options[0] | key: `std::cout << "hi" << '\n';` | correct | unit basis: first row of quiz[2] |
| l1-source-to-program | quiz[2].widget.options[1].why | wrong option: `print("hi")` :: That is Python. C++ has no `print` function here; it uses `std::cout… | correct | unit basis: first row of quiz[2] |
| l1-source-to-program | quiz[2].widget.options[2].why | wrong option: `std::cout << "hi" << '\n'` :: A statement like this one must end with `;`. Without i… | correct | unit basis: first row of quiz[2] |
| l1-source-to-program | quiz[2].widget.options[3].why | wrong option: `cout << "hi" << '\n';` :: `cout` lives inside `std`. Without `std::` the compiler do… | correct | unit basis: first row of quiz[2] |
| l1-source-to-program | quiz[2].feedback.correct | `std::`, `<<` and a closing `;`. | correct | unit basis: first row of quiz[2] |
| l1-source-to-program | quiz[2].feedback.generic | Not quite right. Check for `std::` and a final `;`. | correct | unit basis: first row of quiz[2] |
| l1-source-to-program | quiz[2].explain.text | C++ needs the full name `std::cout`, and a statement like this one ends with `;`. `print` is a Pyth… | correct | unit basis: first row of quiz[2] |
| l1-source-to-program | quiz[3].prose | A build prints two warnings and no errors. | correct | GCC manual, Warning Options: a warning does not stop translation or linking; an error leaves no new executable |
| l1-source-to-program | quiz[3].widget.options[0] | key: Yes: warnings do not stop the build | correct | unit basis: first row of quiz[3] |
| l1-source-to-program | quiz[3].widget.options[1].why | wrong option: No: any warning stops the build :: You read warnings as errors. Only an `error:` line… | correct | unit basis: first row of quiz[3] |
| l1-source-to-program | quiz[3].widget.options[2].why | wrong option: Only an object file, with no executable :: Warnings stop neither step. Both compile a… | correct | unit basis: first row of quiz[3] |
| l1-source-to-program | quiz[3].widget.options[3].why | wrong option: No, the old executable is kept :: With no errors, the linker writes a new executable … | correct | unit basis: first row of quiz[3] |
| l1-source-to-program | quiz[3].feedback.correct | Only errors stop a build. | correct | unit basis: first row of quiz[3] |
| l1-source-to-program | quiz[3].feedback.generic | Not quite right. What does a warning stop? | correct | unit basis: first row of quiz[3] |
| l1-source-to-program | quiz[3].explain.text | A warning is advice about code that compiles; the build still finishes. An error means there is no … | correct | unit basis: first row of quiz[3] |
| l1-source-to-program | summary.ideas[0] | A C++ program is built before it runs: the compiler makes an object file and the linker makes the e… | correct | restates s1, s2, s5 to s8, each judged there |
| l1-source-to-program | summary.ideas[1] | `./main` runs the executable, so every edit needs a fresh build. | correct | unit basis: first row of summary |
| l1-source-to-program | summary.ideas[2] | Read `file:line:column: error:`, then check the named line and the one above it. Warnings do not st… | correct | unit basis: first row of summary |
| l1-source-to-program | summary.formula | Build and run: \texttt{main.cpp} \xrightarrow{\text{compile}} \texttt{main.o} \xrightarrow{\text{li… | correct | unit basis: first row of summary |
| l1-source-to-program | summary.trap | `if (x = 0)` compiles: it stores 0 and tests false. Comparison is `==`. | correct | unit basis: first row of summary |
| l1-source-to-program | screens[7].explain.text (last sentence) | Warnings "often point at a real bug" | unverified | a frequency remark with no source; not measured |
| l2-fixed-types | screens[0].prose | In Python, `7 / 2` is 3.5. Here is the same sum in C++. ```cpp int a = 7; int b = 2; std::cout << a… | correct | [expr.mul]/4: integer division discards the fraction; run under the app compiler and grader prints 3 (check l2 arithmetic table) |
| l2-fixed-types | screens[0].widget.answer | key: 3 (What does the C++ program print?) | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].widget.accept | accept: 3 | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].widget.wrong[0] | slip: 3.5 (py) | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].widget.wrong[1] | slip: 4 (round) | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].hints[0] | hint: `a` and `b` are both declared `int`. | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].hints[1] | hint: An `int` holds whole numbers only, and so does `int / int`. | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].hints[2] | hint: The exact answer 3.5 loses its fractional part. | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].feedback.correct | `int / int` gives an `int`: the .5 is dropped. | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].feedback.generic | Not quite right. Both sides are `int`, so the answer is a whole number. | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].feedback.byKey.py | You divided as Python's `/` does. In C++, two `int`s give an `int`, so the fraction is dropped. | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].feedback.byKey.round | You rounded 3.5 up. C++ does not round here; it drops the fraction. | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[0].explain.text | Each variable was declared `int`, so `a / b` is worked out in whole numbers. 3.5 loses its .5 and b… | correct | unit basis: first row of screens[0] |
| l2-fixed-types | screens[1].prose | An `int` is 4 bytes, 32 bits, shown here a byte per box. It starts as `int count = 2147483645;`. Sl… | correct | [expr.pre]/4: signed overflow is undefined; run under the app compiler and grader, app build: read at run time, +1 three times printed -2147483648 (check l2.s1); two's complement bit pattern by derivation |
| l2-fixed-types | screens[1].canvas.state.caption | caption: `count` = 2,147,483,645 | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[1].widget.answer | key: -2147483648 (What does `count` hold after you add 1 three times?) | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[1].widget.accept | accept: −2147483648 | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[1].widget.wrong[0] | slip: 2147483648 (nowrap) | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[1].widget.wrong[1] | slip: 2147483647 (stick) | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[1].hints[0] | hint: Slide to 3 and read the caption. | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[1].feedback.correct | It wrapped round to the most negative `int`. | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[1].feedback.generic | Not quite right. Slide to 3 and read the value under the boxes. | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[1].feedback.byKey.nowrap | That is the true sum, but an `int` cannot hold it. Slide to 3: the top bit flips and the value goes… | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[1].feedback.byKey.stick | That is the value after two additions, the largest an `int` holds. The third one does not stop ther… | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[1].explain.text | 2,147,483,647 is `0111...1`, the largest `int`. Adding 1 carries into the top bit, which marks a ne… | correct | unit basis: first row of screens[1] |
| l2-fixed-types | screens[2].prose | In C++ every variable has a **type** fixed when you declare it, as in `int qty = 500;`, and it neve… | correct | run under the app compiler and grader: sizeof int 4, long long 8, double 8, bool 1, char 1 in the app compiler (check l2 sizes); [basic.fundamental]; 3e9 > 2^31 - 1; IEEE 754 binary64 has 53 bits, about 15.95 digits |
| l2-fixed-types | screens[2].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[2].widget.answer | key: ["r1"] | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[2].hints[0] | hint: Compare 3 billion with the range of `int`. | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[2].hints[1] | hint: `int` stops near 2.1 billion. | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[2].hints[2] | hint: A whole-number count above that needs 8 bytes. | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[2].feedback.correct | `long long` counts to about 9.2 × 10¹⁸, exactly. | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[2].feedback.generic | Not quite right. Volumes are whole numbers above 2.1 billion. | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[2].feedback.byKey.r0 | 3 billion is above `int`'s limit of 2,147,483,647, so the counter would wrap negative, as on the la… | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[2].feedback.byKey.r2 | A `double` holds 3 billion, but a count is a whole number. An integer type adds exactly, every time. | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[2].feedback.byKey.r5 | A `std::string` holds text. You cannot add 1 to it as a counter. | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[2].explain.text | A volume is a whole number that can pass 2.1 billion, so it needs the 8-byte `long long`. A `double… | correct | unit basis: first row of screens[2] |
| l2-fixed-types | screens[3].prose | `auto` asks the compiler to give a variable the type of the value on the right. It is still fixed, … | correct | [dcl.spec.auto]: auto takes the initialiser's type; 7 / 2 is int 3; run under the app compiler and grader (check l2 arithmetic table, sizeof(r) 4) |
| l2-fixed-types | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].widget.options[0] | key: `int`, holding 3 | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].widget.options[1].why | wrong option: `double`, holding 3.5 :: You let `auto` pick the type of the true answer. It copies t… | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].widget.options[2].why | wrong option: `double`, holding 3.0 :: Nothing on the right is a `double`. `7` and `2` are both `in… | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].widget.options[3].why | wrong option: A type called `auto`, holding 3 :: `auto` is not a type of its own. The compiler repl… | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].hints[0] | hint: What is the type of `7 / 2` on its own? | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].hints[1] | hint: `7` and `2` are written without a decimal point. | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].hints[2] | hint: `int / int` is an `int`, so `r` is an `int` holding 3. | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].feedback.correct | `auto` copies the type of `7 / 2`: `int`. | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].feedback.generic | Not quite right. Work out the type of the right-hand side first. | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].feedback.byKey.d35 | You let `auto` pick the type of the true answer. It copies the type of the expression, `int / int`,… | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[3].explain.text | `7 / 2` is an `int` expression with value 3, so `auto r` becomes `int r`. Write `auto r = 7.0 / 2;`… | correct | unit basis: first row of screens[3] |
| l2-fixed-types | screens[4].prose | This function compiles and is wrong: `average(3, 4)` returns 3. The division happens between two `i… | correct | [expr.arith.conv]; run under the app compiler and grader: starter returns 3 on test 1; `(a + b) / 2.0` passes tests 1 to 4 and fails test 5 (checks l2.s4) |
| l2-fixed-types | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[4] |
| l2-fixed-types | screens[4].widget | code: 6 tests; solution passes, starter fails | correct | unit basis: first row of screens[4] |
| l2-fixed-types | screens[4].hints[0] | hint: Make one side of the division a `double` before dividing. | correct | unit basis: first row of screens[4] |
| l2-fixed-types | screens[4].hints[1] | hint: Test 5 adds 2,147,483,647 to itself. Where does that sum live? | correct | unit basis: first row of screens[4] |
| l2-fixed-types | screens[4].hints[2] | hint: `return (static_cast<double>(a) + b) / 2;` converts before the addition, so nothing overflows. | correct | unit basis: first row of screens[4] |
| l2-fixed-types | screens[4].feedback.correct | Converting first makes every step a `double` step. | correct | unit basis: first row of screens[4] |
| l2-fixed-types | screens[4].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[4] |
| l2-fixed-types | screens[4].feedback.byKey.test-1 | `average(3, 4)` came back as 3: `(a + b) / 2` divides two `int`s, and only then is 3 turned into 3.… | correct | unit basis: first row of screens[4] |
| l2-fixed-types | screens[4].feedback.byKey.test-5 | Test 5 adds 2,147,483,647 to itself. In `int` that sum wraps negative before any division. Convert … | correct | unit basis: first row of screens[4] |
| l2-fixed-types | screens[4].explain.text | Once `a` is a `double`, `a + b` and the division are done in `double`, so nothing is dropped and no… | correct | unit basis: first row of screens[4] |
| l2-fixed-types | screens[5].prose | Prices here are whole pence. This function passes small orders and fails a big one: 20,000 shares a… | correct | [conv.integral]: out-of-range conversion to int is implementation-defined in C++17 and wraps modulo 2^32 here; 2150000000 - 2^32 = -2144967296; run under the app compiler and grader (checks l2.s5) |
| l2-fixed-types | screens[5].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[5] |
| l2-fixed-types | screens[5].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[5] |
| l2-fixed-types | screens[5].hints[0] | hint: The multiplication is fine. Where does its result go? | correct | unit basis: first row of screens[5] |
| l2-fixed-types | screens[5].hints[1] | hint: `int value` holds at most 2,147,483,647. | correct | unit basis: first row of screens[5] |
| l2-fixed-types | screens[5].hints[2] | hint: Declare `long long value`, or return `qty * pence` directly. | correct | unit basis: first row of screens[5] |
| l2-fixed-types | screens[5].feedback.correct | A `long long` result needs a `long long` to hold it. | correct | unit basis: first row of screens[5] |
| l2-fixed-types | screens[5].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of screens[5] |
| l2-fixed-types | screens[5].feedback.byKey.test-2 | 2,150,000,000 does not fit in `int value`, so it was squeezed in and came out negative. Store it in… | correct | unit basis: first row of screens[5] |
| l2-fixed-types | screens[5].explain.text | `qty * pence` is worked out in `long long`, then stored in an `int` that cannot hold it. C++ narrow… | correct | unit basis: first row of screens[5] |
| l2-fixed-types | screens[6].prose | Python's `//` rounds down, so `-7 // 2` is −4. C++ integer division does something else. ```cpp std… | correct | [expr.mul]/4: truncation towards zero; run under the app compiler and grader prints -3 (check l2 arithmetic table); Python floor division: language reference 6.7 |
| l2-fixed-types | screens[6].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].widget.answer | key: -3 (What does the C++ line print?) | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].widget.accept | accept: −3 | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].widget.wrong[0] | slip: -4 (floor) | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].widget.wrong[1] | slip: -3.5 (exact) | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].widget.wrong[2] | slip: 3 (sign) | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].hints[0] | hint: C++ drops the fraction, whatever the sign. | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].hints[1] | hint: −3.5 without its fraction is which whole number? | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].hints[2] | hint: Dropping .5 from −3.5 moves towards zero: −3. | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].feedback.correct | C++ drops the fraction, towards zero. | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].feedback.generic | Not quite right. Drop the fractional part of −3.5. | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].feedback.byKey.floor | You rounded down, as Python's `//` does. C++ truncates towards zero, so −3.5 becomes −3. | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].feedback.byKey.exact | Both sides are `int`, so the answer is a whole number. | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].feedback.byKey.sign | A negative number divided by a positive one is negative. C++ truncates −3.5 towards zero to −3, so … | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].explain.text | C++ integer division truncates towards zero: 3.5 becomes 3 and −3.5 becomes −3. Python's `//` floor… | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[6].explain.canvas.values | canvas: {"r1c2": "−3"} | correct | unit basis: first row of screens[6] |
| l2-fixed-types | screens[7].prose | A fill price arrives as a `double` in pounds, and the ledger wants whole pence. ```cpp double price… | correct | run under the app compiler and grader: 19.99 is stored as 19.989999999999998, the product is 1998.9999999999998, int gives 1998, lround gives 1999 (check l2.s7); [conv.fpint] |
| l2-fixed-types | screens[7].widget.options[0] | key: 1998 | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[7].widget.options[1].why | wrong option: 1999 :: You did the sum on paper. `19.99 * 100` is stored as 1998.9999999999998, and … | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[7].widget.options[2].why | wrong option: 19 :: The multiplication happens first, in `double`. Only its result is cut down to a… | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[7].widget.options[3].why | wrong option: It does not compile :: C++ converts a `double` to an `int` silently. Only some warnin… | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[7].hints[0] | hint: 19.99 has no exact binary form, like 0.1 in Python. | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[7].hints[1] | hint: Is `19.99 * 100` stored a little above or a little below 1999? | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[7].hints[2] | hint: It is 1998.9999999999998, and the conversion to `int` drops everything after the point. | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[7].feedback.correct | Truncation turns 1998.9999999999998 into 1998. | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[7].feedback.generic | Not quite right. The `double` result is a hair below 1999. | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[7].feedback.byKey.1999 | You expected rounding. Assigning a `double` to an `int` drops the fraction, and `19.99 * 100` is 19… | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[7].explain.text | `19.99` is stored slightly low, so `price * 100` is 1998.9999999999998. Assigning it to an `int` tr… | correct | unit basis: first row of screens[7] |
| l2-fixed-types | screens[8].prose | Every result you met follows one rule: an operation works in its operands' type, and one `double` m… | correct | [expr.arith.conv] usual arithmetic conversions; run under the app compiler and grader: 3 / 4 * 1.0 and static_cast<double>(3 / 4) are 0, 3.0 / 4 is 0.75 (check l2 arithmetic table) |
| l2-fixed-types | screens[8].widget.options[0] | key: `3.0 / 4` | correct | unit basis: first row of screens[8] |
| l2-fixed-types | screens[8].widget.options[1].why | wrong option: `3 / 4` :: Both are `int`, so the answer is 0. | correct | unit basis: first row of screens[8] |
| l2-fixed-types | screens[8].widget.options[2].why | wrong option: `3 / 4 * 1.0` :: The division runs first, in `int`, and gives 0. Multiplying by 1.0 a… | correct | unit basis: first row of screens[8] |
| l2-fixed-types | screens[8].widget.options[3].why | wrong option: `static_cast<double>(3 / 4)` :: That converts after dividing. `3 / 4` is already 0, s… | correct | unit basis: first row of screens[8] |
| l2-fixed-types | screens[8].hints[0] | hint: Find where the first `double` appears, and whether the division has already happened. | correct | unit basis: first row of screens[8] |
| l2-fixed-types | screens[8].feedback.correct | The `double` is there before the division. | correct | unit basis: first row of screens[8] |
| l2-fixed-types | screens[8].feedback.generic | Not quite right. The conversion must come before the division. | correct | unit basis: first row of screens[8] |
| l2-fixed-types | screens[8].explain.text | `3.0` is a `double`, so `3.0 / 4` divides in `double` and gives 0.75. Every other option divides tw… | correct | unit basis: first row of screens[8] |
| l2-fixed-types | screens[9].prose | Exchanges quote prices in whole ticks, so a program can store each price as an integer number of ti… | correct | run under the app compiler and grader: solution passes; dividing by int 100 fails test 3 with 0; an int total fails test 2 with a positive value (checks l2.s9); tick sizes: MiFID II RTS 11 tick-size tables |
| l2-fixed-types | screens[9].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[9] |
| l2-fixed-types | screens[9].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[9] |
| l2-fixed-types | screens[9].hints[0] | hint: Work out the pence first: the change per share times the shares. | correct | unit basis: first row of screens[9] |
| l2-fixed-types | screens[9].hints[1] | hint: Row 2 is −3,000,000,000 pence. Which type holds that? | correct | unit basis: first row of screens[9] |
| l2-fixed-types | screens[9].hints[2] | hint: `long long pence = (sell_pence - buy_pence) * qty;` then `return pence / 100.0;`. | correct | unit basis: first row of screens[9] |
| l2-fixed-types | screens[9].feedback.correct | Exact pence, then one conversion to pounds. | correct | unit basis: first row of screens[9] |
| l2-fixed-types | screens[9].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of screens[9] |
| l2-fixed-types | screens[9].feedback.byKey.test-3 | A 1p profit came back wrong. If you got 0, you divided by `100`, an `int`: write `100.0`. | correct | unit basis: first row of screens[9] |
| l2-fixed-types | screens[9].feedback.byKey.test-2 | Test 2 is −3,000,000,000 pence. If it came back positive or small, an `int` held it on the way. Kee… | correct | unit basis: first row of screens[9] |
| l2-fixed-types | screens[9].explain.text | The pence sum is exact in `long long`, even at three billion. Dividing by `100.0` makes the last st… | correct | unit basis: first row of screens[9] |
| l2-fixed-types | quiz[0].prose | ```cpp bool up = 101.5 > 100.0; std::cout << up << '\n'; ``` | correct | [ostream.inserters.arithmetic]: bool prints as 1 or 0 without boolalpha; run under the app compiler and grader (check l2 arithmetic table) |
| l2-fixed-types | quiz[0].widget.options[0] | key: `1` | correct | unit basis: first row of quiz[0] |
| l2-fixed-types | quiz[0].widget.options[1].why | wrong option: `true` :: `std::cout` prints a `bool` as 1 or 0 unless you ask for words with `std::b… | correct | unit basis: first row of quiz[0] |
| l2-fixed-types | quiz[0].widget.options[2].why | wrong option: `True` :: That is Python's spelling. C++ prints the number 1. | correct | unit basis: first row of quiz[0] |
| l2-fixed-types | quiz[0].widget.options[3].why | wrong option: `101.5` :: `up` holds the result of the comparison, not a price. | correct | unit basis: first row of quiz[0] |
| l2-fixed-types | quiz[0].feedback.correct | A `bool` prints as 1 or 0. | correct | unit basis: first row of quiz[0] |
| l2-fixed-types | quiz[0].feedback.generic | Not quite right. How does `std::cout` show a `bool`? | correct | unit basis: first row of quiz[0] |
| l2-fixed-types | quiz[0].explain.text | The comparison is true, so `up` is `true`, and `std::cout` prints `true` as 1. Write `std::cout << … | correct | unit basis: first row of quiz[0] |
| l2-fixed-types | quiz[1].widget.answer | key: 8 (How many bytes does `sizeof(long long)` report?) | correct | run under the app compiler and grader: sizeof(long long) is 8 (check l2 sizes); [basic.fundamental]: at least 64 bits |
| l2-fixed-types | quiz[1].widget.accept | accept: 8 | correct | unit basis: first row of quiz[1] |
| l2-fixed-types | quiz[1].widget.wrong[0] | slip: 4 (four) | correct | unit basis: first row of quiz[1] |
| l2-fixed-types | quiz[1].widget.wrong[1] | slip: 64 (bits) | correct | unit basis: first row of quiz[1] |
| l2-fixed-types | quiz[1].feedback.correct | 8 bytes, 64 bits. | correct | unit basis: first row of quiz[1] |
| l2-fixed-types | quiz[1].feedback.generic | Not quite right. `sizeof` counts bytes. | correct | unit basis: first row of quiz[1] |
| l2-fixed-types | quiz[1].feedback.byKey.four | 4 bytes is an `int`. `long long` is twice the size. | correct | unit basis: first row of quiz[1] |
| l2-fixed-types | quiz[1].feedback.byKey.bits | 64 is the number of bits. `sizeof` counts bytes. | correct | unit basis: first row of quiz[1] |
| l2-fixed-types | quiz[1].explain.text | A `long long` is 8 bytes, or 64 bits, so it reaches about 9.2 × 10¹⁸. An `int` is 4 bytes. | correct | unit basis: first row of quiz[1] |
| l2-fixed-types | quiz[2].prose | ```cpp int ticks = 2147483647; ticks = ticks + 1; ``` | correct | as s1: undefined, wraps in practice (check l2.s1; the question says "in practice") |
| l2-fixed-types | quiz[2].widget.options[0] | key: −2,147,483,648 | correct | unit basis: first row of quiz[2] |
| l2-fixed-types | quiz[2].widget.options[1].why | wrong option: 2,147,483,648 :: That number does not fit in an `int`. The result wraps round instead. | correct | unit basis: first row of quiz[2] |
| l2-fixed-types | quiz[2].widget.options[2].why | wrong option: 2,147,483,647 :: C++ does not stop at the limit; adding 1 carries into the sign bit. | correct | unit basis: first row of quiz[2] |
| l2-fixed-types | quiz[2].widget.options[3].why | wrong option: The program stops with an error :: Nothing checks for overflow at run time. It happen… | correct | unit basis: first row of quiz[2] |
| l2-fixed-types | quiz[2].feedback.correct | It wraps to the most negative `int`. | correct | unit basis: first row of quiz[2] |
| l2-fixed-types | quiz[2].feedback.generic | Not quite right. Think of the bits on the slider screen. | correct | unit basis: first row of quiz[2] |
| l2-fixed-types | quiz[2].explain.text | The carry lands in the sign bit, so the value wraps to −2,147,483,648. Formally this is undefined b… | correct | unit basis: first row of quiz[2] |
| l2-fixed-types | quiz[3].prose | ```cpp double share = 1 / 4; ``` | correct | [expr.mul]/4 then [conv.fpint]; run under the app compiler and grader prints 0 (check l2 arithmetic table) |
| l2-fixed-types | quiz[3].widget.options[0] | key: 0 | correct | unit basis: first row of quiz[3] |
| l2-fixed-types | quiz[3].widget.options[1].why | wrong option: 0.25 :: The type on the left does not reach the right. `1 / 4` is worked out in `int`… | correct | unit basis: first row of quiz[3] |
| l2-fixed-types | quiz[3].widget.options[2].why | wrong option: It does not compile :: Storing an `int` in a `double` is allowed and silent. | correct | unit basis: first row of quiz[3] |
| l2-fixed-types | quiz[3].widget.options[3].why | wrong option: 1 :: `int` division drops the fraction of 0.25; it does not round up. | correct | unit basis: first row of quiz[3] |
| l2-fixed-types | quiz[3].feedback.correct | `1 / 4` is 0 before `share` ever sees it. | correct | unit basis: first row of quiz[3] |
| l2-fixed-types | quiz[3].feedback.generic | Not quite right. Which type is `1 / 4`? | correct | unit basis: first row of quiz[3] |
| l2-fixed-types | quiz[3].explain.text | `1 / 4` divides two `int`s and gives 0, which is then stored as 0.0. Write `1.0 / 4` to get 0.25. | correct | unit basis: first row of quiz[3] |
| l2-fixed-types | summary.ideas[0] | Every variable has a fixed type, which sets its size (`sizeof`) and range. `auto` takes the type of… | correct | restates s0 to s7; auto never deduces a reference: [dcl.type.auto.deduct] |
| l2-fixed-types | summary.ideas[1] | An operation works in its operands' type: `int / int` drops the fraction, towards zero, and one `do… | correct | unit basis: first row of summary |
| l2-fixed-types | summary.ideas[2] | `int` stops at 2,147,483,647. Going past it is undefined behaviour, and in practice the value usual… | correct | unit basis: first row of summary |
| l2-fixed-types | summary.formula | Integer division: 7 / 2 = 3, \quad -7 / 2 = -3, \quad 7.0 / 2 = 3.5 :: Convert with `static_cast<do… | correct | unit basis: first row of summary |
| l2-fixed-types | summary.trap | `int pence = 19.99 * 100;` is 1998: the `double` is a hair low and the conversion truncates. | correct | unit basis: first row of summary |
| l3-branches-and-loops | screens[0].prose | Five closes and a C++ loop over them. Read it as you would Python. ```cpp int ups = 0; for (int i =… | correct | trace of the loop: 104 > 100 and 106 > 101; [stmt.for]; the wrong set is every close above 100 |
| l3-branches-and-loops | screens[0].widget.answer | key: ["c1", "c3"] | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].widget.wrong[0] | slip: ["c1", "c2", "c3", "c4"] (first) | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].hints[0] | hint: `i` runs 1, 2, 3, 4. Each turn compares `prices[i]` with the close before it. | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].hints[1] | hint: Index 2 holds 101. What came the day before? | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].hints[2] | hint: 104 beats 100 and 106 beats 101. The others fell. | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].feedback.correct | Day 1 and day 3 beat the close before them. | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].feedback.generic | Not quite right. Compare each close with its left-hand neighbour only. | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].feedback.byKey.first | You compared every close with the first one, 100. The loop compares `prices[i]` with `prices[i - 1]… | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].feedback.byKey.c0 | The loop starts at `i = 1`, so index 0 is never counted itself; it is only the day before index 1. | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].feedback.byKey.c2 | 101 is below 104, the close before it, so that day fell. | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].feedback.byKey.c4 | 103 is below 106, the close before it, so that day fell. | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[0].explain.text | The loop runs `i` from 1 while `i < 5`, adding 1 each turn with `++i`. Days 1 and 3 beat their neig… | correct | unit basis: first row of screens[0] |
| l3-branches-and-loops | screens[1].prose | A backtest tracks the **drawdown**: the close's fall below its peak so far, as a fraction of that p… | correct | definition of drawdown from a running peak (Magdon-Ismail and Atiya 2004): (110 - 88) / 110 = 0.2; slips (100 - 88) / 100 = 0.12 and (110 - 99) / 110 = 0.1 |
| l3-branches-and-loops | screens[1].widget.answer | key: 0.2 (What is the largest drawdown you see, in %?) | correct | unit basis: first row of screens[1] |
| l3-branches-and-loops | screens[1].widget.accept | accept: 20% | correct | unit basis: first row of screens[1] |
| l3-branches-and-loops | screens[1].widget.wrong[0] | slip: 0.12 (start) | correct | unit basis: first row of screens[1] |
| l3-branches-and-loops | screens[1].widget.wrong[1] | slip: 0.1 (first) | correct | unit basis: first row of screens[1] |
| l3-branches-and-loops | screens[1].hints[0] | hint: Stop on each day and read the caption. Which day is lowest against its peak? | correct | unit basis: first row of screens[1] |
| l3-branches-and-loops | screens[1].feedback.correct | From the 110 peak down to 88 is a fall of 20%. | correct | unit basis: first row of screens[1] |
| l3-branches-and-loops | screens[1].feedback.generic | Not quite right. Slide to day 4 and read the caption. | correct | unit basis: first row of screens[1] |
| l3-branches-and-loops | screens[1].feedback.byKey.start | You measured from the first close, 100. Drawdown is measured from the highest close so far, 110. | correct | unit basis: first row of screens[1] |
| l3-branches-and-loops | screens[1].feedback.byKey.first | That is the fall to day 2. Day 4 falls further below the same peak. | correct | unit basis: first row of screens[1] |
| l3-branches-and-loops | screens[1].explain.text | The peak only ever moves up: 100, then 110, where it stays. Day 4 closes at 88, which is $(110 - 88… | correct | unit basis: first row of screens[1] |
| l3-branches-and-loops | screens[2].prose | A C++ `for` has three parts: a start `int i = 1`, a test `i < prices.size()` and a step `++i`. The … | correct | [stmt.for]: the condition is tested before each iteration; i takes 1 to 5, five turns |
| l3-branches-and-loops | screens[2].widget.answer | key: 5 (How many times does the body run?) | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].widget.accept | accept: 5 | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].widget.wrong[0] | slip: 6 (six) | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].widget.wrong[1] | slip: 4 (four) | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].hints[0] | hint: List the values of `i` that pass the test. | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].hints[1] | hint: `i` starts at index 1, not 0. | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].hints[2] | hint: `i` is 1, 2, 3, 4, 5; at 6 the test fails. | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].feedback.correct | `i` takes 1 to 5: five turns. | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].feedback.generic | Not quite right. Write out each `i` until `i < 6` fails. | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].feedback.byKey.six | You counted every close. The loop starts at 1, so index 0 is skipped. | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].feedback.byKey.four | The test is `i < 6`, so 5 still passes. The loop stops only when `i` reaches 6. | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[2].explain.text | The test runs before each turn: 1 to 5 pass and 6 fails, so five turns. Starting at 1 gives every c… | correct | unit basis: first row of screens[2] |
| l3-branches-and-loops | screens[3].prose | `const std::vector<double>&` hands the function the caller's closes to read, without copying them; … | correct | run under the app compiler and grader: solution passes; `size() - 1` fails test 2, `>=` fails test 6, `<=` fails test 1 with "vector[] index out of bounds" (checks l3.s3); 2^32 - 1 is about 4.29e9, 2^64 - 1 about 1.8e19; [vector.capacity] size_type |
| l3-branches-and-loops | screens[3].widget | code: 6 tests; solution passes, starter fails | correct | unit basis: first row of screens[3] |
| l3-branches-and-loops | screens[3].hints[0] | hint: Start the loop at index 1, as on the last screen. | correct | unit basis: first row of screens[3] |
| l3-branches-and-loops | screens[3].hints[1] | hint: Test 2 is empty. Does your loop run at all when `prices.size()` is 0? | correct | unit basis: first row of screens[3] |
| l3-branches-and-loops | screens[3].hints[2] | hint: `for (std::size_t i = 1; i < prices.size(); ++i)` with `if (prices[i] > prices[i - 1]) ++ups;… | correct | unit basis: first row of screens[3] |
| l3-branches-and-loops | screens[3].feedback.correct | Start at 1, stop before `size()`. | correct | unit basis: first row of screens[3] |
| l3-branches-and-loops | screens[3].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of screens[3] |
| l3-branches-and-loops | screens[3].feedback.byKey.test-2 | The empty vector broke it. With `i < prices.size() - 1`, 0 − 1 wraps, since `size()` is unsigned: a… | correct | unit basis: first row of screens[3] |
| l3-branches-and-loops | screens[3].feedback.byKey.test-6 | Three equal closes are not up days. Use `>`, not `>=`. | correct | unit basis: first row of screens[3] |
| l3-branches-and-loops | screens[3].feedback.byKey.test-1 | Test 1 has five closes and two up days. If the program stopped with index out of bounds, your loop … | correct | unit basis: first row of screens[3] |
| l3-branches-and-loops | screens[3].explain.text | Starting at 1 means every `prices[i - 1]` exists, and on an empty or one-close vector the loop neve… | correct | unit basis: first row of screens[3] |
| l3-branches-and-loops | screens[4].prose | Now the drawdown you slid through. `for (double p : prices)` visits each close in turn, like Python… | correct | run under the app compiler and grader: solution passes; first-close slip returns 0.12 and the sign slip 0 on test 1 (checks l3.s4); (120 - 60) / 120 = 0.5 and (100 - 90) / 100 = 0.1 |
| l3-branches-and-loops | screens[4].widget | code: 7 tests; solution passes, starter fails | correct | unit basis: first row of screens[4] |
| l3-branches-and-loops | screens[4].hints[0] | hint: Two variables carry across the loop: the peak so far and the worst fall so far. | correct | unit basis: first row of screens[4] |
| l3-branches-and-loops | screens[4].hints[1] | hint: Update the peak before you measure today's fall. | correct | unit basis: first row of screens[4] |
| l3-branches-and-loops | screens[4].hints[2] | hint: Inside the loop: raise `peak` if `p` is higher, then `double fall = (peak - p) / peak;` and k… | correct | unit basis: first row of screens[4] |
| l3-branches-and-loops | screens[4].feedback.correct | A running peak and a running worst: one pass. | correct | unit basis: first row of screens[4] |
| l3-branches-and-loops | screens[4].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of screens[4] |
| l3-branches-and-loops | screens[4].feedback.byKey.test-6 | In `100, 80, 120, 60` the worst fall is from the new peak 120 down to 60: 0.5. | correct | unit basis: first row of screens[4] |
| l3-branches-and-loops | screens[4].feedback.byKey.test-1 | Test 1 should give 0.2: from 110 to 88. If you got 0.12, you measured from the first close, not the… | correct | unit basis: first row of screens[4] |
| l3-branches-and-loops | screens[4].feedback.byKey.test-4 | A fall from 100 to 90 is 0.1, a positive fraction. | correct | unit basis: first row of screens[4] |
| l3-branches-and-loops | screens[4].explain.text | The peak only rises, so one variable holds it. Each close's fall is measured against it, and the wo… | correct | unit basis: first row of screens[4] |
| l3-branches-and-loops | screens[5].prose | A program reads how many numbers follow, then the numbers. Loop `n` times with `std::cin >>` inside… | correct | run under the app compiler and grader: solution passes; starting the total at n prints 9.75 on test 1 (check l3.s5); six significant digits: [ostream.inserters.arithmetic] with precision 6 |
| l3-branches-and-loops | screens[5].canvas.state.caption | caption: Input `3 1.5 2.25 3` prints `6.75`. | correct | unit basis: first row of screens[5] |
| l3-branches-and-loops | screens[5].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[5] |
| l3-branches-and-loops | screens[5].hints[0] | hint: You know how many numbers to read, so a counting `for` fits. | correct | unit basis: first row of screens[5] |
| l3-branches-and-loops | screens[5].hints[1] | hint: Read one number per turn into a fresh `double x`. | correct | unit basis: first row of screens[5] |
| l3-branches-and-loops | screens[5].hints[2] | hint: `for (int i = 0; i < n; ++i) { double x; std::cin >> x; total += x; }` | correct | unit basis: first row of screens[5] |
| l3-branches-and-loops | screens[5].feedback.correct | `n` turns, one read per turn. | correct | unit basis: first row of screens[5] |
| l3-branches-and-loops | screens[5].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of screens[5] |
| l3-branches-and-loops | screens[5].feedback.byKey.test-1 | The sum of 1.5, 2.25 and 3 is 6.75. If you got 9.75, you added `n` itself: it was already read befo… | correct | unit basis: first row of screens[5] |
| l3-branches-and-loops | screens[5].feedback.byKey.test-2 | With `n` = 0 the loop must not run, and the sum is 0. | correct | unit basis: first row of screens[5] |
| l3-branches-and-loops | screens[5].explain.text | `for (int i = 0; i < n; ++i)` runs exactly `n` times, and zero times when `n` is 0. `std::cin >>` d… | correct | unit basis: first row of screens[5] |
| l3-branches-and-loops | screens[6].prose | In Python, `range(len(prices))` stops for you. In C++ you write the test yourself. ```cpp double la… | correct | [vector.access]: [] with n >= size() is undefined, at() throws out_of_range; run under the app compiler and grader: the app's hardened libc++ stops at prices[3] (check l3.s6) |
| l3-branches-and-loops | screens[6].widget.options[0] | key: It reads `prices[3]`, past the end: this app stops it, a normal build may read garbage | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[6].widget.options[1].why | wrong option: `last` ends as 99.8 :: You read `<=` as `<`. The loop also runs with `i = 3`, and the… | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[6].widget.options[2].why | wrong option: It throws `std::out_of_range` :: Only `prices.at(i)` checks the index and throws. `pr… | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[6].widget.options[3].why | wrong option: It does not compile :: The compiler does not know how many closes there will be. This… | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[6].hints[0] | hint: List the values of `i` for which `i <= 3` is true. | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[6].hints[1] | hint: The valid indices are 0, 1 and 2. | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[6].hints[2] | hint: `i` reaches 3, and `prices[3]` is one past the last close. | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[6].feedback.correct | `<=` runs one turn too many. | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[6].feedback.generic | Not quite right. Write out every `i` the loop takes. | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[6].feedback.byKey.last | You read `<=` as `<`. With `<=`, `i` also takes 3, and `prices[3]` is past the end. | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[6].explain.text | Indices run from 0 to `size() - 1`, so the test must be `i < prices.size()`. This app's library che… | imprecise | [vector.access]: the read is undefined; "reads whatever memory is there" states one outcome as fact (the option says "may"). Finding 5 |
| l3-branches-and-loops | screens[6].explain.canvas.caption | caption: `prices[3]` is past the end. | correct | unit basis: first row of screens[6] |
| l3-branches-and-loops | screens[7].prose | The loops you wrote, in one place. ```cpp for (std::size_t i = 1; i < xs.size(); ++i) // by index f… | correct | [basic.scope.block], [stmt.for]: the loop variable's scope ends with the loop; run, g++: `'i' was not declared in this scope` (check l3.s7) |
| l3-branches-and-loops | screens[7].widget.options[0] | key: It does not compile: `i` exists only inside the loop | correct | unit basis: first row of screens[7] |
| l3-branches-and-loops | screens[7].widget.options[1].why | wrong option: It prints 5 :: That is Python, where the loop variable outlives the loop. In C++ `i` … | imprecise | Python leaves i at 4 after `for i in range(5)`; 5 is what a C++ i declared before the loop holds (NOTE check). Finding 3 |
| l3-branches-and-loops | screens[7].widget.options[2].why | wrong option: It prints 4 :: 4 is the last value the body saw, but `i` no longer exists after the l… | correct | unit basis: first row of screens[7] |
| l3-branches-and-loops | screens[7].widget.options[3].why | wrong option: It prints 0 :: `i` is not reset; it is gone. The compiler reports an undeclared name. | correct | unit basis: first row of screens[7] |
| l3-branches-and-loops | screens[7].hints[0] | hint: Where was `i` declared? | correct | unit basis: first row of screens[7] |
| l3-branches-and-loops | screens[7].feedback.correct | `i` belongs to the loop. | correct | unit basis: first row of screens[7] |
| l3-branches-and-loops | screens[7].feedback.generic | Not quite right. In C++ a name lives inside the braces where it was declared. | correct | unit basis: first row of screens[7] |
| l3-branches-and-loops | screens[7].explain.text | `int i` is declared inside the `for`, so it ends with the loop and `i` is undeclared on the next li… | correct | unit basis: first row of screens[7] |
| l3-branches-and-loops | screens[8].prose | Each of a day's fills arrives as a letter: `L` for the LSE, `C` for Cboe, `T` for Turquoise. Any ot… | correct | [stmt.switch]: control falls through without break; run under the app compiler and grader: starter gives [2,3,0,0] on test 1, no default fails test 3 (checks l3.s8); run: silent with -Wall, flagged by -Wimplicit-fallthrough (checks l3.s8 fall-through) |
| l3-branches-and-loops | screens[8].canvas.state.caption | caption: `LXCLLTA` gives LSE 3, Cboe 1, Turquoise 1, other 2. | correct | unit basis: first row of screens[8] |
| l3-branches-and-loops | screens[8].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[8] |
| l3-branches-and-loops | screens[8].hints[0] | hint: Run the starter on `L` in your head. Which counts go up? | correct | unit basis: first row of screens[8] |
| l3-branches-and-loops | screens[8].hints[1] | hint: Every `case` needs a `break` at its end. | correct | unit basis: first row of screens[8] |
| l3-branches-and-loops | screens[8].hints[2] | hint: Add `break;` after `++counts[0]`, a `case 'T':`, and `default: ++counts[3]; break;`. | correct | unit basis: first row of screens[8] |
| l3-branches-and-loops | screens[8].feedback.correct | Each case ends with `break`, and `default` takes the rest. | correct | unit basis: first row of screens[8] |
| l3-branches-and-loops | screens[8].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of screens[8] |
| l3-branches-and-loops | screens[8].feedback.byKey.test-1 | `LLCT` should give 2, 1, 1, 0. If Cboe came out as 3, each `L` fell through into the `C` case: add … | correct | unit basis: first row of screens[8] |
| l3-branches-and-loops | screens[8].feedback.byKey.test-3 | `X` and `A` belong in the fourth count. A `default:` case catches every letter no other case names. | correct | unit basis: first row of screens[8] |
| l3-branches-and-loops | screens[8].explain.text | Without `break`, the `L` case ran on into the `C` case, so every LSE fill also counted as Cboe. `de… | correct | unit basis: first row of screens[8] |
| l3-branches-and-loops | quiz[0].prose | ```cpp if (0.1 + 0.2 == 0.3) { std::cout << "equal\n"; } else { std::cout << "different\n"; } ``` | correct | IEEE 754: 0.1 + 0.2 = 0.30000000000000004; run under the app compiler and grader prints different (check l3 quiz0) |
| l3-branches-and-loops | quiz[0].widget.options[0] | key: `different` | correct | unit basis: first row of quiz[0] |
| l3-branches-and-loops | quiz[0].widget.options[1].why | wrong option: `equal` :: You did the sum on paper. A `double` stores 0.1 and 0.2 slightly off, so t… | correct | unit basis: first row of quiz[0] |
| l3-branches-and-loops | quiz[0].widget.options[2].why | wrong option: Nothing: `==` cannot compare doubles :: `==` compiles for doubles. It compares them e… | correct | unit basis: first row of quiz[0] |
| l3-branches-and-loops | quiz[0].feedback.correct | The sum is a hair above 0.3. | correct | unit basis: first row of quiz[0] |
| l3-branches-and-loops | quiz[0].feedback.generic | Not quite right. Are 0.1 and 0.2 stored exactly? | correct | unit basis: first row of quiz[0] |
| l3-branches-and-loops | quiz[0].explain.text | C++ doubles behave like Python floats: `0.1 + 0.2` is 0.30000000000000004. Compare with a tolerance… | correct | unit basis: first row of quiz[0] |
| l3-branches-and-loops | quiz[1].prose | ```cpp int turns = 0; for (int i = 0; i <= 5; ++i) { ++turns; } ``` | correct | i takes 0 to 5, six turns |
| l3-branches-and-loops | quiz[1].widget.answer | key: 6 (What is `turns` at the end?) | correct | unit basis: first row of quiz[1] |
| l3-branches-and-loops | quiz[1].widget.accept | accept: 6 | correct | unit basis: first row of quiz[1] |
| l3-branches-and-loops | quiz[1].widget.wrong[0] | slip: 5 (five) | correct | unit basis: first row of quiz[1] |
| l3-branches-and-loops | quiz[1].feedback.correct | 0 to 5 inclusive is six turns. | correct | unit basis: first row of quiz[1] |
| l3-branches-and-loops | quiz[1].feedback.generic | Not quite right. List the values of `i`. | correct | unit basis: first row of quiz[1] |
| l3-branches-and-loops | quiz[1].feedback.byKey.five | With `<=`, 5 also passes the test. `i` takes 0, 1, 2, 3, 4 and 5. | correct | unit basis: first row of quiz[1] |
| l3-branches-and-loops | quiz[1].explain.text | `i` runs 0, 1, 2, 3, 4, 5: six values, because `<=` lets 5 through. | correct | unit basis: first row of quiz[1] |
| l3-branches-and-loops | quiz[2].prose | ```cpp std::vector<double> prices; // empty for (std::size_t i = 0; i < prices.size() - 1; ++i) { s… | correct | [basic.fundamental]: unsigned arithmetic is modulo 2^n; run under the app compiler and grader: size() - 1 printed 4294967295 and the loop stopped on the first read (check l3.quiz2) |
| l3-branches-and-loops | quiz[2].widget.options[0] | key: `prices.size() - 1` wraps to a huge number, so the loop reads past the end | correct | unit basis: first row of quiz[2] |
| l3-branches-and-loops | quiz[2].widget.options[1].why | wrong option: The loop never runs, because 0 − 1 is −1 :: `size()` returns an unsigned `std::size_t… | correct | unit basis: first row of quiz[2] |
| l3-branches-and-loops | quiz[2].widget.options[2].why | wrong option: The loop runs once, with `i = 0` :: The test `0 < 0 - 1` is the question. In unsigned… | correct | unit basis: first row of quiz[2] |
| l3-branches-and-loops | quiz[2].widget.options[3].why | wrong option: It does not compile :: It compiles cleanly. The compiler cannot know the vector will … | correct | unit basis: first row of quiz[2] |
| l3-branches-and-loops | quiz[2].feedback.correct | Unsigned 0 − 1 is not −1. | correct | unit basis: first row of quiz[2] |
| l3-branches-and-loops | quiz[2].feedback.generic | Not quite right. What type does `size()` return? | correct | unit basis: first row of quiz[2] |
| l3-branches-and-loops | quiz[2].explain.text | `size()` is a `std::size_t`, which has no negatives, so 0 − 1 wraps to its maximum. The loop then i… | correct | unit basis: first row of quiz[2] |
| l3-branches-and-loops | quiz[3].prose | A stop-loss sells once a close falls below 95. ```cpp int day = 0; for (double p : {101.0, 97.5, 94… | correct | trace: 101.0 and 97.5 pass, 94.0 breaks before ++day; run under the app compiler and grader prints 2 (check l3 quiz3) |
| l3-branches-and-loops | quiz[3].widget.answer | key: 2 (What is `day` at the end?) | correct | unit basis: first row of quiz[3] |
| l3-branches-and-loops | quiz[3].widget.accept | accept: 2 | correct | unit basis: first row of quiz[3] |
| l3-branches-and-loops | quiz[3].widget.wrong[0] | slip: 3 (count) | correct | unit basis: first row of quiz[3] |
| l3-branches-and-loops | quiz[3].widget.wrong[1] | slip: 4 (idx) | correct | unit basis: first row of quiz[3] |
| l3-branches-and-loops | quiz[3].feedback.correct | 94.0 triggers the stop on the third close, before `++day`. | correct | unit basis: first row of quiz[3] |
| l3-branches-and-loops | quiz[3].feedback.generic | Not quite right. `break` leaves the loop at once. | correct | unit basis: first row of quiz[3] |
| l3-branches-and-loops | quiz[3].feedback.byKey.count | You counted the trigger day too. `break` runs before `++day` on that turn. | correct | unit basis: first row of quiz[3] |
| l3-branches-and-loops | quiz[3].feedback.byKey.idx | `break` leaves the loop; the later closes are never visited. | correct | unit basis: first row of quiz[3] |
| l3-branches-and-loops | quiz[3].explain.text | 101.0 and 97.5 pass and add 1 each. 94.0 is below 95, so `break` leaves the loop before `++day`. `d… | correct | unit basis: first row of quiz[3] |
| l3-branches-and-loops | summary.ideas[0] | `for (std::size_t i = 1; i < xs.size(); ++i)` names a start, a test checked before each turn, and a… | correct | restates s2, s6, s7, s8; the drawdown formula is s1's definition |
| l3-branches-and-loops | summary.ideas[1] | Braces mark the body, and a variable declared in a loop ends with it. | correct | unit basis: first row of summary |
| l3-branches-and-loops | summary.ideas[2] | A `switch` picks a `case` by value and falls through to the next case unless it hits `break`. | correct | unit basis: first row of summary |
| l3-branches-and-loops | summary.formula | Maximum drawdown: \text{MDD} = \max_t \dfrac{\max_{s \le t} p_s - p_t}{\max_{s \le t} p_s} :: One p… | correct | unit basis: first row of summary |
| l3-branches-and-loops | summary.trap | `i <= prices.size()` runs one turn too many and reads past the end; the test is `i < prices.size()`. | correct | unit basis: first row of summary |
| l4-functions-and-headers | screens[0].prose | In Python a function can sit below the code that calls it. It only has to exist when the call runs.… | correct | [basic.scope.pdecl]: a name is usable only after its declaration; run, g++: 5:18 `'annualise' was not declared in this scope` (check l4.s0) |
| l4-functions-and-headers | screens[0].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].widget.options[0] | key: The compiler reads from the top and has not met `annualise` by line 5 | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].widget.options[1].why | wrong option: `annualise` is misspelt on line 5 :: Lines 5 and 8 spell it the same way. The name is… | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].widget.options[2].why | wrong option: `main` must be the last function in the file :: `main` can sit anywhere. What matters… | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].widget.options[3].why | wrong option: The linker cannot find the body of `annualise` :: This is a compiler error, `main.cpp… | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].hints[0] | hint: The compiler reads the file once, from top to bottom. | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].hints[1] | hint: At line 5, which lines has it read? | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].hints[2] | hint: It has seen lines 1 to 4, and `annualise` first appears on line 8. | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].feedback.correct | At line 5 the compiler has never heard of `annualise`. | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].feedback.generic | Not quite right. Think about what the compiler has read by line 5. | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].feedback.byKey.spell | Lines 5 and 8 spell it the same way. The problem is order: line 5 comes first. | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[0].explain.text | The compiler reads top to bottom, and every name must be known before it is used. At line 5, `annua… | correct | unit basis: first row of screens[0] |
| l4-functions-and-headers | screens[1].prose | This version builds and prints 0.158745, with the function still at the bottom. One line was added. | correct | [basic.def]: a declaration without a body; run under the app compiler and grader prints 0.158745 (check l4.s1/s4) |
| l4-functions-and-headers | screens[1].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[1] |
| l4-functions-and-headers | screens[1].widget.answer | key: ["l4"] | correct | unit basis: first row of screens[1] |
| l4-functions-and-headers | screens[1].hints[0] | hint: Compare with the last screen. Which line is new? | correct | unit basis: first row of screens[1] |
| l4-functions-and-headers | screens[1].hints[1] | hint: It sits above `main` and ends with `;`, not a body. | correct | unit basis: first row of screens[1] |
| l4-functions-and-headers | screens[1].feedback.correct | Line 4 announces the function before `main` uses it. | correct | unit basis: first row of screens[1] |
| l4-functions-and-headers | screens[1].feedback.generic | Not quite right. Find the line that was not there before. | correct | unit basis: first row of screens[1] |
| l4-functions-and-headers | screens[1].feedback.byKey.l10 | That line starts the body, but the compiler reaches it only after line 7. Something above `main` mu… | correct | unit basis: first row of screens[1] |
| l4-functions-and-headers | screens[1].feedback.byKey.l1 | `<cmath>` brings in `std::sqrt`, which the body uses. It says nothing about `annualise`. | correct | unit basis: first row of screens[1] |
| l4-functions-and-headers | screens[1].explain.text | Line 4 is a **declaration**: the name, the return type and the parameter types, ending in `;`. Line… | correct | unit basis: first row of screens[1] |
| l4-functions-and-headers | screens[2].prose | A **declaration** gives a function's name and types and ends with `;`. A **definition** adds the bo… | correct | [basic.def]/2: a function declaration with a body is a definition, and every definition is a declaration |
| l4-functions-and-headers | screens[2].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[2].widget.answer | key: ["l1", "l2"] | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[2].widget.wrong[0] | slip: ["l1", "l2", "l3"] (def) | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[2].hints[0] | hint: Look for braces. | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[2].hints[1] | hint: Line 3 has a body in `{ }`. | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[2].hints[2] | hint: Lines 1 and 2 end in `;` with no body; line 4 is a variable. | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[2].feedback.correct | Lines 1 and 2: types and a semicolon, no body. | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[2].feedback.generic | Not quite right. A declaration only has no braces. | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[2].feedback.byKey.def | Line 3 has a body in braces, so it is a definition. It declares `half` too, but it is not only a de… | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[2].feedback.byKey.l4 | `double rate = 0.04;` is a variable with a value, not a function. | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[2].explain.text | Lines 1 and 2 promise functions without bodies. Line 3 is a definition, and line 4 a variable. Para… | correct | unit basis: first row of screens[2] |
| l4-functions-and-headers | screens[3].prose | Real projects split the work. `returns.h`, a **header**, holds declarations; `returns.cpp` holds th… | correct | [lex.phases]: each translation unit is compiled alone and the linker resolves the call; #include is textual: [cpp.include] |
| l4-functions-and-headers | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[3].widget.answer | key: ["l11"] | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[3].hints[0] | hint: Which file holds bodies? | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[3].hints[1] | hint: Look under `// returns.cpp`. | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[3].hints[2] | hint: Line 11 is the only `annualise` with braces. | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[3].feedback.correct | The body lives in `returns.cpp`, line 11. | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[3].feedback.generic | Not quite right. Find the `annualise` that has a body. | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[3].feedback.byKey.l5 | Line 5 only declares `annualise`; it has no body. It tells `main.cpp` the call is legal, and the li… | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[3].feedback.byKey.l16 | That is the call itself. Its body is elsewhere. | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[3].feedback.byKey.l15 | `#include "returns.h"` pastes in the declarations, not the bodies. | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[3].explain.text | `#include "returns.h"` pastes the header's text into `main.cpp`, so the compiler sees the declarati… | correct | unit basis: first row of screens[3] |
| l4-functions-and-headers | screens[4].prose | Line 5 says `int days = 252`: a **default argument**. A call that leaves `days` out gets 252, which… | correct | [dcl.fct.default]; 0.01 * sqrt(252) = 0.158745 and 0.01 * sqrt(365) = 0.1910497 (check l4.s1/s4); slips 0.1587 and 0.01 * 365 = 3.65 |
| l4-functions-and-headers | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[4].widget.answer | key: 0.191 (What does `annualise(0.01, 365)` return, to 4 decimal places?) | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[4].widget.accept | accept: 0.1910 (0.01 × √365 = 0.19105) | imprecise | 0.01 x sqrt(365) = 0.1910497; the 0.19105 shown reads as 0.1911 at 4 dp (NOTE check). Finding 4 |
| l4-functions-and-headers | screens[4].widget.wrong[0] | slip: 0.1587 (default) | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[4].widget.wrong[1] | slip: 3.65 (sum) | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[4].hints[0] | hint: The second argument replaces the default. | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[4].hints[1] | hint: Line 11 computes `daily_vol * std::sqrt(days)`. | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[4].hints[2] | hint: $0.01 \times \sqrt{365} = 0.01 \times 19.105$. | imprecise | sqrt(365) = 19.10497, not 19.105; 0.01 x 19.105 = 0.19105 reads as 0.1911 at 4 dp, which the key rejects (NOTE check). Finding 4 |
| l4-functions-and-headers | screens[4].feedback.correct | 365 replaces 252: $0.01\sqrt{365} \approx 0.1910$. | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[4].feedback.generic | Not quite right. Use `days = 365` in line 11. | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[4].feedback.byKey.default | That is the default, 252. Passing 365 replaces it. | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[4].feedback.byKey.sum | You multiplied by 365. Annualising multiplies by the square root of the days. | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[4].explain.text | A default fills in only when the call leaves that argument out. Here `days` is 365, so the result i… | correct | unit basis: first row of screens[4] |
| l4-functions-and-headers | screens[5].prose | The header line is hidden above your code, as `#include "returns.h"` would paste it. Write the defi… | correct | run under the app compiler and grader: solution passes; by-value, non-const-reference and other-return-type definitions give `ambiguous`, `undefined symbol` and `previous declaration`; do-while fails test 2, dividing by today test 1, size() - 1 test 3 (checks l4.s5) |
| l4-functions-and-headers | screens[5].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].hints[0] | hint: Loop from index 1, as in `count_up_days`. | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].hints[1] | hint: The signature must match the declaration on line 4 exactly. | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].hints[2] | hint: `out.push_back((prices[i] - prices[i - 1]) / prices[i - 1]);` for `i` from 1 while `i < price… | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].feedback.correct | n closes give n − 1 returns. | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].feedback.byKey.test-2 | One close has no day before it, so the list must be empty. If the program stopped, your loop read `… | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].feedback.byKey.test-1 | From 110 to 99 is (99 − 110) / 110 = −0.1. Divide by yesterday's close, not today's. If the program… | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].feedback.byKey.compile | If the message says `ambiguous`, `undefined symbol` or `previous declaration`, make your first line… | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].feedback.byKey.test-3 | The empty vector broke it. `prices.size() - 1` wraps when the size is 0: start at 1 and test `i < p… | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[5].explain.text | Starting at index 1 gives each return a yesterday, so one close or none gives an empty list. Your d… | correct | unit basis: first row of screens[5] |
| l4-functions-and-headers | screens[6].prose | The hidden header declares `double annualise(double daily_vol, int days = 252);`. A default argumen… | correct | [dcl.fct.default]/4: a default may not be given twice; run under the app compiler and grader: `redefinition of default argument` (check l4.s6); 0.01 * sqrt(252) = 0.1587 |
| l4-functions-and-headers | screens[6].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[6] |
| l4-functions-and-headers | screens[6].widget | code: 6 tests; solution passes, starter fails | correct | unit basis: first row of screens[6] |
| l4-functions-and-headers | screens[6].hints[0] | hint: `std::sqrt` from `<cmath>` takes a square root. | correct | unit basis: first row of screens[6] |
| l4-functions-and-headers | screens[6].hints[1] | hint: The default is already in the header on line 5. | correct | unit basis: first row of screens[6] |
| l4-functions-and-headers | screens[6].hints[2] | hint: `return daily_vol * std::sqrt(days);` and no `= 252` in your line. | correct | unit basis: first row of screens[6] |
| l4-functions-and-headers | screens[6].feedback.correct | The header holds the default; the definition holds the body. | correct | unit basis: first row of screens[6] |
| l4-functions-and-headers | screens[6].feedback.generic | Not quite right. Read the first failing test or the compiler message. | correct | unit basis: first row of screens[6] |
| l4-functions-and-headers | screens[6].feedback.byKey.compile | If the message says `redefinition of default argument`, delete `= 252` from your definition: the de… | correct | unit basis: first row of screens[6] |
| l4-functions-and-headers | screens[6].feedback.byKey.test-1 | `annualise(0.01)` should be 0.01 × √252 ≈ 0.1587. Multiply by the square root of `days`. | correct | unit basis: first row of screens[6] |
| l4-functions-and-headers | screens[6].explain.text | Callers see only the header, so the default must be there for `annualise(0.01)` to compile in their… | correct | unit basis: first row of screens[6] |
| l4-functions-and-headers | screens[7].prose | To save a file, someone puts a body in `returns.h`. Both `main.cpp` and `pricer.cpp` include it. ``… | correct | [basic.def.odr]: one definition of a non-inline function per program; run, g++ and ld: `multiple definition`, `first defined here`, `collect2`; inline fixes it (checks l4.s7) |
| l4-functions-and-headers | screens[7].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].widget.options[0] | key: Each `.cpp` file gets its own copy of the body, so the linker finds two | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].widget.options[1].why | wrong option: g++ ignores `#pragma once` :: g++ honours it. It stops one `.cpp` file including the … | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].widget.options[2].why | wrong option: The compiler should have caught it, so it is a compiler bug :: Each file was compiled… | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].widget.options[3].why | wrong option: `simple_return` clashes with a standard library name :: The message names `main.cpp` … | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].hints[0] | hint: `#pragma once` works within one `.cpp` file. | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].hints[1] | hint: Line 3 names two object files, one from each `.cpp`. | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].hints[2] | hint: Each `.cpp` pasted the header, body and all, so each object file defines `simple_return`. | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].feedback.correct | One body per program: in a `.cpp`, not a header. | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].feedback.generic | Not quite right. Who sees both object files? | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].feedback.byKey.ignored | You expected `#pragma once` to cover the whole program. It covers one `.cpp` at a time, and each of… | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[7].explain.text | `#include` pastes the header into each `.cpp`, so `main.o` and `pricer.o` both contain the body. `#… | correct | unit basis: first row of screens[7] |
| l4-functions-and-headers | screens[8].prose | The pattern you used: ```cpp // returns.h: declarations, defaults, #pragma once double annualise(do… | correct | [dcl.fct.default]/4: a default is visible only where its declaration is; run under the app compiler and grader: the one-argument call does not compile (check l4.s8) |
| l4-functions-and-headers | screens[8].widget.options[0] | key: It no longer compiles: `main.cpp` sees no default | correct | unit basis: first row of screens[8] |
| l4-functions-and-headers | screens[8].widget.options[1].why | wrong option: It still returns 0.158745 :: `main.cpp` is compiled from the header alone. It never s… | correct | unit basis: first row of screens[8] |
| l4-functions-and-headers | screens[8].widget.options[2].why | wrong option: It compiles, and `days` is 0 :: C++ never invents a value for a missing argument. Wit… | correct | unit basis: first row of screens[8] |
| l4-functions-and-headers | screens[8].widget.options[3].why | wrong option: It compiles, but the linker fails :: The problem appears earlier: the compiler reject… | correct | unit basis: first row of screens[8] |
| l4-functions-and-headers | screens[8].hints[0] | hint: When `main.cpp` is compiled, which files does the compiler read? | correct | unit basis: first row of screens[8] |
| l4-functions-and-headers | screens[8].feedback.correct | Callers see the header, so defaults go there. | correct | unit basis: first row of screens[8] |
| l4-functions-and-headers | screens[8].feedback.generic | Not quite right. Each `.cpp` is compiled on its own. | correct | unit basis: first row of screens[8] |
| l4-functions-and-headers | screens[8].explain.text | `main.cpp` is compiled with only the header's text, so it sees a function that needs two arguments.… | correct | unit basis: first row of screens[8] |
| l4-functions-and-headers | screens[9].prose | A vendor sells a fast volatility library. You receive `fastvol.h` and `libfastvol.a`, a file of com… | correct | a static library is an archive of object files joined at link time; a shared object is loaded by the dynamic loader at start-up (ld and ld.so manuals) |
| l4-functions-and-headers | screens[9].widget.options[0] | key: The header lets your code compile; the `.a` is joined in by the linker | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | screens[9].widget.options[1].why | wrong option: You compile `libfastvol.a` with g++ first :: It is already compiled object code. Ther… | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | screens[9].widget.options[2].why | wrong option: The header is enough; the `.a` is optional :: The header holds only declarations. Wit… | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | screens[9].widget.options[3].why | wrong option: You `#include` both files :: `#include` pastes text. The `.a` is machine code, so it … | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | screens[9].hints[0] | hint: Which file holds declarations, and which holds compiled bodies? | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | screens[9].hints[1] | hint: Follow each file's arrow. | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | screens[9].hints[2] | hint: Headers feed the compiler; compiled bodies feed the linker. | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | screens[9].feedback.correct | Declarations to the compiler, compiled code to the linker. | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | screens[9].feedback.generic | Not quite right. Follow each arrow on the diagram. | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | screens[9].feedback.byKey.hdr | The header only promises the functions exist. Without the `.a`, the linker cannot find their bodies… | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | screens[9].explain.text | A library ships declarations in a header and bodies already compiled. A `.a` is joined in at link t… | correct | unit basis: first row of screens[9] |
| l4-functions-and-headers | quiz[0].prose | Two functions share a name: an **overload**. The compiler picks one by the argument types. ```cpp d… | correct | [over.match]: the overload is chosen by argument types; run under the app compiler and grader prints 10001 100.015 (check l4.quiz0) |
| l4-functions-and-headers | quiz[0].widget.options[0] | key: `10001 100.015` | correct | unit basis: first row of quiz[0] |
| l4-functions-and-headers | quiz[0].widget.options[1].why | wrong option: `10001.5 100.015` :: `10001LL` and `10002LL` are `long long`, so the `long long` vers… | correct | unit basis: first row of quiz[0] |
| l4-functions-and-headers | quiz[0].widget.options[2].why | wrong option: Nothing: two functions cannot share a name :: That is true in Python, where the secon… | correct | unit basis: first row of quiz[0] |
| l4-functions-and-headers | quiz[0].widget.options[3].why | wrong option: `10001 100` :: The `double` version runs for `100.01` and `100.02`, so the result kee… | correct | unit basis: first row of quiz[0] |
| l4-functions-and-headers | quiz[0].feedback.correct | Ticks in `long long`, prices in `double`. | correct | unit basis: first row of quiz[0] |
| l4-functions-and-headers | quiz[0].feedback.generic | Not quite right. Match each call's argument types to a version. | correct | unit basis: first row of quiz[0] |
| l4-functions-and-headers | quiz[0].explain.text | `mid(10001LL, 10002LL)` matches the `long long` version: 20003 / 2 is 10001 in integer division. `m… | correct | unit basis: first row of quiz[0] |
| l4-functions-and-headers | quiz[1].prose | ```cpp double risk_free_rate() { return 0.04; } ``` | correct | [conv.func] then [conv.bool]: a function name converts to true; run under the app compiler and grader prints 1; (void) and (0) do not compile (checks l4.quiz1) |
| l4-functions-and-headers | quiz[1].widget.options[0] | key: `std::cout << risk_free_rate() << '\n';` | correct | unit basis: first row of quiz[1] |
| l4-functions-and-headers | quiz[1].widget.options[1].why | wrong option: `std::cout << risk_free_rate << '\n';` :: Without `()` you name the function without … | correct | unit basis: first row of quiz[1] |
| l4-functions-and-headers | quiz[1].widget.options[2].why | wrong option: `std::cout << risk_free_rate(void) << '\n';` :: `void` can appear in a declaration's … | correct | unit basis: first row of quiz[1] |
| l4-functions-and-headers | quiz[1].widget.options[3].why | wrong option: `std::cout << risk_free_rate(0) << '\n';` :: The function takes no arguments, so pass… | correct | unit basis: first row of quiz[1] |
| l4-functions-and-headers | quiz[1].feedback.correct | Empty brackets call a function with no parameters. | correct | unit basis: first row of quiz[1] |
| l4-functions-and-headers | quiz[1].feedback.generic | Not quite right. A call always has brackets. | correct | unit basis: first row of quiz[1] |
| l4-functions-and-headers | quiz[1].explain.text | A function with no parameters is still called with `()`. Without them you refer to the function its… | correct | unit basis: first row of quiz[1] |
| l4-functions-and-headers | quiz[2].prose | ```text $ g++ -std=c++17 main.cpp -o backtest /usr/bin/ld: /tmp/ccR5tWb1.o: in function `main': mai… | correct | run, g++ and ld: undefined reference to `annualise(double, int)' (check l4.quiz2) |
| l4-functions-and-headers | quiz[2].widget.options[0] | key: `returns.cpp` is missing from the command, so no body was linked | correct | unit basis: first row of quiz[2] |
| l4-functions-and-headers | quiz[2].widget.options[1].why | wrong option: `main.cpp` forgot `#include "returns.h"` :: Then the compiler would have stopped with… | correct | unit basis: first row of quiz[2] |
| l4-functions-and-headers | quiz[2].widget.options[2].why | wrong option: `annualise` is misspelt in `main.cpp` :: A misspelt call would fail to compile. The l… | correct | unit basis: first row of quiz[2] |
| l4-functions-and-headers | quiz[2].widget.options[3].why | wrong option: The default argument is missing :: The message names `annualise(double, int)`, so the… | correct | unit basis: first row of quiz[2] |
| l4-functions-and-headers | quiz[2].feedback.correct | Declared, called, never defined in the build. | correct | unit basis: first row of quiz[2] |
| l4-functions-and-headers | quiz[2].feedback.generic | Not quite right. Which program printed the message? | correct | unit basis: first row of quiz[2] |
| l4-functions-and-headers | quiz[2].explain.text | `ld` is the linker. `main.o` calls `annualise`, but no object file in this build defines it. Add `r… | correct | unit basis: first row of quiz[2] |
| l4-functions-and-headers | quiz[3].prose | `simple_returns` from this lesson is called with one close: `simple_returns({101.5})`. | correct | n closes give n - 1 returns; the loop from index 1 never runs on one close |
| l4-functions-and-headers | quiz[3].widget.answer | key: 0 (How many returns does it give back?) | correct | unit basis: first row of quiz[3] |
| l4-functions-and-headers | quiz[3].widget.accept | accept: 0 | correct | unit basis: first row of quiz[3] |
| l4-functions-and-headers | quiz[3].widget.wrong[0] | slip: 1 (one) | correct | unit basis: first row of quiz[3] |
| l4-functions-and-headers | quiz[3].feedback.correct | No day before it, so no return. | correct | unit basis: first row of quiz[3] |
| l4-functions-and-headers | quiz[3].feedback.generic | Not quite right. A return needs two closes. | correct | unit basis: first row of quiz[3] |
| l4-functions-and-headers | quiz[3].feedback.byKey.one | A return compares two closes. With one close there is no yesterday, so the list is empty. | correct | unit basis: first row of quiz[3] |
| l4-functions-and-headers | quiz[3].explain.text | n closes give n − 1 returns, so one close gives none. The loop from index 1 never runs. | correct | unit basis: first row of quiz[3] |
| l4-functions-and-headers | summary.ideas[0] | A name must be declared before it is used. A declaration gives the types and ends in `;`; a definit… | correct | restates s0, s2, s3, s7, each judged there |
| l4-functions-and-headers | summary.ideas[1] | A header holds declarations and defaults; each `.cpp` compiles alone, and the linker joins the obje… | correct | unit basis: first row of summary |
| l4-functions-and-headers | summary.ideas[2] | One definition per program for an ordinary function: a body in a header included by two `.cpp` file… | correct | unit basis: first row of summary |
| l4-functions-and-headers | summary.formula | Separate compilation: \texttt{main.cpp} \to \texttt{main.o},\quad \texttt{returns.cpp} \to \texttt{… | correct | unit basis: first row of summary |
| l4-functions-and-headers | summary.trap | `#pragma once` stops one file including a header twice; it does not stop two `.cpp` files each gett… | correct | unit basis: first row of summary |
| review-1 | items[0].prose | ```text $ g++ -std=c++17 -Wall pnl.cpp -o pnl pnl.cpp:7:12: warning: unused variable 'fees' [-Wunus… | correct | as l1 s7: a warning does not stop the build |
| review-1 | items[0].widget.options[0] | key: `./pnl` exists and runs; `fees` is worth a look | correct | unit basis: first row of items[0] |
| review-1 | items[0].widget.options[1].why | wrong option: There is no executable until the warning is fixed :: You read `warning` as `error`. O… | correct | unit basis: first row of items[0] |
| review-1 | items[0].widget.options[2].why | wrong option: `./pnl` runs the version from before this build :: With no errors, the linker wrote a… | correct | unit basis: first row of items[0] |
| review-1 | items[0].widget.options[3].why | wrong option: You must run g++ again without `-Wall` :: `-Wall` only adds warnings. It never stops … | correct | unit basis: first row of items[0] |
| review-1 | items[0].feedback.correct | A warning is advice; the build finished. | correct | unit basis: first row of items[0] |
| review-1 | items[0].feedback.generic | Not quite right. Does a warning stop a build? | correct | unit basis: first row of items[0] |
| review-1 | items[0].explain.text | Only an `error:` stops the build, so `pnl` was written. The warning says `fees` is declared and nev… | correct | unit basis: first row of items[0] |
| review-1 | items[1].prose | ```cpp int qty = 3; int lots = 4; double share = qty / lots; ``` | correct | [expr.mul]/4: 3 / 4 is 0 (check l2 arithmetic table) |
| review-1 | items[1].widget.answer | key: 0 (What does `share` hold?) | correct | unit basis: first row of items[1] |
| review-1 | items[1].widget.accept | accept: 0 | correct | unit basis: first row of items[1] |
| review-1 | items[1].widget.wrong[0] | slip: 0.75 (true) | correct | unit basis: first row of items[1] |
| review-1 | items[1].feedback.correct | `3 / 4` is 0 in `int`. | correct | unit basis: first row of items[1] |
| review-1 | items[1].feedback.generic | Not quite right. Which type is `qty / lots`? | correct | unit basis: first row of items[1] |
| review-1 | items[1].feedback.byKey.true | The `double` on the left does not reach the right side. `qty / lots` divides two `int`s and gives 0. | correct | unit basis: first row of items[1] |
| review-1 | items[1].explain.text | Both operands are `int`, so the division drops the fraction and gives 0, stored as 0.0. Write `stat… | correct | unit basis: first row of items[1] |
| review-1 | items[2].prose | ```cpp int turns = 0; for (int i = 3; i < 10; i += 2) { ++turns; } ``` | correct | i takes 3, 5, 7, 9 |
| review-1 | items[2].widget.answer | key: 4 (What is `turns` at the end?) | correct | unit basis: first row of items[2] |
| review-1 | items[2].widget.accept | accept: 4 | correct | unit basis: first row of items[2] |
| review-1 | items[2].widget.wrong[0] | slip: 7 (seven) | correct | unit basis: first row of items[2] |
| review-1 | items[2].widget.wrong[1] | slip: 5 (five) | correct | unit basis: first row of items[2] |
| review-1 | items[2].feedback.correct | `i` takes 3, 5, 7 and 9. | correct | unit basis: first row of items[2] |
| review-1 | items[2].feedback.generic | Not quite right. Write out each value of `i`. | correct | unit basis: first row of items[2] |
| review-1 | items[2].feedback.byKey.seven | You counted 3 to 9 one at a time. The step is `i += 2`. | correct | unit basis: first row of items[2] |
| review-1 | items[2].feedback.byKey.five | 11 fails the test `i < 10`, so there is no fifth turn. | correct | unit basis: first row of items[2] |
| review-1 | items[2].explain.text | Start at 3, add 2 each turn, stop when `i < 10` fails: 3, 5, 7, 9. Four turns. | correct | unit basis: first row of items[2] |
| review-1 | items[3].widget.options[0] | key: `undefined reference to 'annualise(double, int)'` | correct | linker against compiler messages, as l4 s7 and quiz2 (checks l4.s7, l4.quiz2, l1.s6, l4.s0) |
| review-1 | items[3].widget.options[1] | key: `multiple definition of 'simple_return(double, double)'` | correct | unit basis: first row of items[3] |
| review-1 | items[3].widget.options[2].why | wrong option: `expected ';' at end of declaration` :: A missing `;` is found while reading one file… | correct | unit basis: first row of items[3] |
| review-1 | items[3].widget.options[3].why | wrong option: `'annualise' was not declared in this scope` :: An unknown name in one file is a comp… | correct | unit basis: first row of items[3] |
| review-1 | items[3].feedback.correct | The linker reports missing or doubled bodies across files. | correct | unit basis: first row of items[3] |
| review-1 | items[3].feedback.generic | Not quite right. Which problems need more than one file to see? | correct | unit basis: first row of items[3] |
| review-1 | items[3].explain.text | The compiler reads one `.cpp` at a time, so it reports syntax and unknown names. The linker joins t… | correct | unit basis: first row of items[3] |
| review-1 | items[4].prose | Two block trades of 1,500,000,000 shares each. ```cpp int volume = 1500000000; volume = volume + 15… | correct | 3,000,000,000 - 2^32 = -1,294,967,296; run under the app compiler and grader: the app build printed it (check homework-1.6 / review-1.4); undefined, and the question says "in practice" |
| review-1 | items[4].widget.answer | key: -1294967296 (What does `volume` hold, in practice?) | correct | unit basis: first row of items[4] |
| review-1 | items[4].widget.accept | accept: −1294967296 | correct | unit basis: first row of items[4] |
| review-1 | items[4].widget.wrong[0] | slip: 3000000000 (true) | correct | unit basis: first row of items[4] |
| review-1 | items[4].widget.wrong[1] | slip: 2147483647 (max) | correct | unit basis: first row of items[4] |
| review-1 | items[4].widget.wrong[2] | slip: 1294967296 (sign) | correct | unit basis: first row of items[4] |
| review-1 | items[4].feedback.correct | 3,000,000,000 − 2³² = −1,294,967,296. | correct | unit basis: first row of items[4] |
| review-1 | items[4].feedback.generic | Not quite right. An `int` wraps after 2,147,483,647. | correct | unit basis: first row of items[4] |
| review-1 | items[4].feedback.byKey.true | That is the true total, but an `int` cannot hold it. It wraps by 2³², 4,294,967,296. | correct | unit basis: first row of items[4] |
| review-1 | items[4].feedback.byKey.max | An `int` does not stop at its limit. It wraps round to negative values. | correct | unit basis: first row of items[4] |
| review-1 | items[4].feedback.byKey.sign | 3,000,000,000 − 4,294,967,296 is below zero: the counter wraps past the largest int into negative n… | correct | unit basis: first row of items[4] |
| review-1 | items[4].explain.text | The true sum, 3,000,000,000, is 2³² too big for the wrapped result: 3,000,000,000 − 4,294,967,296 =… | correct | unit basis: first row of items[4] |
| review-1 | items[5].prose | A risk check counts the days whose P&L lost more than the limit: a P&L below `-limit`. A loss of ex… | correct | run under the app compiler and grader: solution passes; `<=` fails test 3, comparing with limit fails test 1 (checks review-1.5) |
| review-1 | items[5].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of items[5] |
| review-1 | items[5].feedback.correct | Strictly below `-limit`, counted in one pass. | correct | unit basis: first row of items[5] |
| review-1 | items[5].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of items[5] |
| review-1 | items[5].feedback.byKey.test-3 | A loss of exactly 50 against a limit of 50 is not a breach. Use `<`, not `<=`. | correct | unit basis: first row of items[5] |
| review-1 | items[5].feedback.byKey.test-1 | Losses of 120.5 and 200 breach a limit of 100. Compare each P&L with `-limit`, not `limit`. | correct | unit basis: first row of items[5] |
| review-1 | items[5].explain.text | A range-based `for` visits each day's P&L, and `x < -limit` counts only losses beyond the limit. An… | correct | unit basis: first row of items[5] |
| review-1 | items[6].prose | `returns.h` declares `double annualise(double daily_vol, int days = 252);`. | correct | [dcl.fct.default]: only days has a default; int converts to double |
| review-1 | items[6].widget.options[0] | key: `annualise()` | correct | unit basis: first row of items[6] |
| review-1 | items[6].widget.options[1].why | wrong option: `annualise(0.01)` :: `days` has a default, so one argument is enough. | correct | unit basis: first row of items[6] |
| review-1 | items[6].widget.options[2].why | wrong option: `annualise(1)` :: The `int` 1 converts to the `double` 1.0, so this compiles. | correct | unit basis: first row of items[6] |
| review-1 | items[6].widget.options[3].why | wrong option: `annualise(0.01, 12)` :: Both arguments given; 12 replaces the default. | correct | unit basis: first row of items[6] |
| review-1 | items[6].feedback.correct | `daily_vol` has no default. | correct | unit basis: first row of items[6] |
| review-1 | items[6].feedback.generic | Not quite right. Which parameter has no default? | correct | unit basis: first row of items[6] |
| review-1 | items[6].explain.text | Only `days` has a default. `daily_vol` must always be passed, so `annualise()` is a compile error. | correct | unit basis: first row of items[6] |
| review-1 | items[7].prose | ```cpp std::cout << -9 / 4 << '\n'; ``` | correct | [expr.mul]/4: -9 / 4 = -2 (check l2 arithmetic table) |
| review-1 | items[7].widget.answer | key: -2 (What does it print?) | correct | unit basis: first row of items[7] |
| review-1 | items[7].widget.accept | accept: −2 | correct | unit basis: first row of items[7] |
| review-1 | items[7].widget.wrong[0] | slip: -3 (floor) | correct | unit basis: first row of items[7] |
| review-1 | items[7].widget.wrong[1] | slip: -2.25 (exact) | correct | unit basis: first row of items[7] |
| review-1 | items[7].widget.wrong[2] | slip: 2 (sign) | correct | unit basis: first row of items[7] |
| review-1 | items[7].feedback.correct | −2.25 truncated towards zero is −2. | correct | unit basis: first row of items[7] |
| review-1 | items[7].feedback.generic | Not quite right. C++ drops the fraction towards zero. | correct | unit basis: first row of items[7] |
| review-1 | items[7].feedback.byKey.floor | You floored, as Python's `//` does. C++ truncates towards zero, so −2.25 becomes −2. | correct | unit basis: first row of items[7] |
| review-1 | items[7].feedback.byKey.exact | Both operands are `int`, so the result is a whole number. | correct | unit basis: first row of items[7] |
| review-1 | items[7].feedback.byKey.sign | −9 / 4 is −2.25, and truncating towards zero gives −2. A positive 2 drops the minus sign of the quo… | correct | unit basis: first row of items[7] |
| review-1 | items[7].explain.text | `-9 / 4` is −2.25 exactly, and C++ integer division drops the fraction towards zero: −2. Python's `… | correct | unit basis: first row of items[7] |
| review-1 | items[0].explain.text (second sentence) | An unused variable "often means a forgotten step in a P&L" | unverified | a frequency remark with no source |
| homework-1 | items[0].prose | A backtest has `main.cpp` and `returns.cpp`, and both include `returns.h`. You build it with `g++ -… | correct | as l4 s3: two compiles in either order, one link, then run |
| homework-1 | items[0].widget.answer | key: ["s1", "s2", "s3", "s4", "s5"] | correct | unit basis: first row of items[0] |
| homework-1 | items[0].widget.lines.s1 | step: The compiler reads `returns.h` into `main.cpp` and writes `main.o` | correct | unit basis: first row of items[0] |
| homework-1 | items[0].widget.lines.s2 | step: The compiler reads `returns.h` into `returns.cpp` and writes `returns.o` | correct | unit basis: first row of items[0] |
| homework-1 | items[0].widget.lines.s3 | step: The linker joins `main.o`, `returns.o` and the standard library | correct | unit basis: first row of items[0] |
| homework-1 | items[0].widget.lines.s4 | step: The linker writes the executable `backtest` | correct | unit basis: first row of items[0] |
| homework-1 | items[0].widget.lines.s5 | step: `./backtest` runs `main` | correct | unit basis: first row of items[0] |
| homework-1 | items[0].feedback.correct | Two separate compiles, one link, then run. | correct | unit basis: first row of items[0] |
| homework-1 | items[0].feedback.generic | Not quite right. Every object file must exist before the link. | correct | unit basis: first row of items[0] |
| homework-1 | items[0].explain.text | Each `.cpp` is compiled alone, in either order, each seeing `returns.h`. The linker then joins both… | correct | unit basis: first row of items[0] |
| homework-1 | items[1].prose | A file of closes arrives on `std::cin`: a header line, then one `date,close` line per day. The file… | correct | run under the app compiler and grader: solution passes; skipping only empty lines fails test 6, measuring from the whole file's top fails test 4 (checks homework-1.1); 63 / 262.5 = 0.24 and 27.5 / 275 = 0.10 |
| homework-1 | items[1].widget | code: 7 tests; solution passes, starter fails | correct | unit basis: first row of items[1] |
| homework-1 | items[1].feedback.correct | Parse, track the running peak, print once at the end. | correct | unit basis: first row of items[1] |
| homework-1 | items[1].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of items[1] |
| homework-1 | items[1].feedback.byKey.test-2 | With only a header, the loop never runs and the answer is 0.00%. If the program stopped, something … | correct | unit basis: first row of items[1] |
| homework-1 | items[1].feedback.byKey.test-6 | Test 6 uses `\r\n` line ends and ends with a blank line. A line with no comma must be skipped, not … | correct | unit basis: first row of items[1] |
| homework-1 | items[1].feedback.byKey.test-4 | Test 4 has two falls: 262.50 to 199.50 (24%) and 275.00 to 247.50 (10%). Keep the worst, measured f… | correct | unit basis: first row of items[1] |
| homework-1 | items[1].explain.text | Read the header once, then loop on `std::getline`, skipping any line without a comma. Each close up… | correct | unit basis: first row of items[1] |
| homework-1 | items[2].prose | A mean-reversion rule compares the price with its moving average. Below the average by more than `b… | correct | run under the app compiler and grader: solution passes; `<=` fails test 4, `>=` fails test 5 (checks homework-1.2) |
| homework-1 | items[2].widget | code: 7 tests; solution passes, starter fails | correct | unit basis: first row of items[2] |
| homework-1 | items[2].feedback.correct | Strict tests on both sides, hold in between. | correct | unit basis: first row of items[2] |
| homework-1 | items[2].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of items[2] |
| homework-1 | items[2].feedback.byKey.test-4 | 98 is exactly `average - band`. The rule says the edge holds, so use `<`, not `<=`. | correct | unit basis: first row of items[2] |
| homework-1 | items[2].feedback.byKey.test-5 | 102 is exactly `average + band`, so it holds. Use `>`, not `>=`. | correct | unit basis: first row of items[2] |
| homework-1 | items[2].feedback.byKey.test-1 | 95 is more than 2 below 100, so buy. Compare `price < average - band`. | correct | unit basis: first row of items[2] |
| homework-1 | items[2].explain.text | An `if`, an `else if` and a final `return "hold"` cover the three cases. Strict `<` and `>` leave b… | correct | unit basis: first row of items[2] |
| homework-1 | items[3].prose | Each fill's size fits in an `int`, but a day's total may not. | correct | run under the app compiler and grader: solution passes; an int total fails test 3 (check homework-1.3) |
| homework-1 | items[3].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of items[3] |
| homework-1 | items[3].feedback.correct | Each `int` fill is added into a `long long` total. | correct | unit basis: first row of items[3] |
| homework-1 | items[3].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of items[3] |
| homework-1 | items[3].feedback.byKey.test-3 | Two fills of 2,000,000,000 should total 4,000,000,000. A negative or wrong total means the sum live… | correct | unit basis: first row of items[3] |
| homework-1 | items[3].explain.text | `total` is a `long long`, so `total += f` converts each `int` fill up before adding. Nothing wraps … | correct | unit basis: first row of items[3] |
| homework-1 | items[4].prose | ```cpp for (int i = 0; i < prices.size(); ++i) { ... } ``` `g++ -Wall` prints `warning: comparison … | correct | run, g++ -Wall: the quoted sign-compare text (check homework-1.4); [expr.arith.conv]: the int converts to unsigned |
| homework-1 | items[4].widget.options[0] | key: Make `i` a `std::size_t`, or compare with `static_cast<int>(prices.size())` | correct | unit basis: first row of items[4] |
| homework-1 | items[4].widget.options[1].why | wrong option: Change `<` to `<=` :: That reads one past the end and keeps the warning. | correct | unit basis: first row of items[4] |
| homework-1 | items[4].widget.options[2].why | wrong option: Build without `-Wall` :: That hides the warning and keeps the mixed comparison. A neg… | correct | unit basis: first row of items[4] |
| homework-1 | items[4].widget.options[3].why | wrong option: Make `i` a `double` :: An index is a whole number. A `double` index is converted sile… | correct | unit basis: first row of items[4] |
| homework-1 | items[4].feedback.correct | Compare like with like. | correct | unit basis: first row of items[4] |
| homework-1 | items[4].feedback.generic | Not quite right. The warning is about mixing signed and unsigned types. | correct | unit basis: first row of items[4] |
| homework-1 | items[4].explain.text | `size()` returns an unsigned type, and comparing it with a signed `int` converts the `int`. Here it… | correct | unit basis: first row of items[4] |
| homework-1 | items[5].prose | ```cpp double price = 0.29; int pence = price * 100; ``` | correct | run under the app compiler and grader: 0.29 is stored as 0.28999999999999998, the product is 28.999999999999996, int gives 28, lround 29 (check l2.s7 and homework-1 items[5]) |
| homework-1 | items[5].widget.answer | key: 28 (What does `pence` hold?) | correct | unit basis: first row of items[5] |
| homework-1 | items[5].widget.accept | accept: 28 | correct | unit basis: first row of items[5] |
| homework-1 | items[5].widget.wrong[0] | slip: 29 (round) | correct | unit basis: first row of items[5] |
| homework-1 | items[5].feedback.correct | 0.29 × 100 is stored as 28.999999999999996, then truncated. | correct | unit basis: first row of items[5] |
| homework-1 | items[5].feedback.generic | Not quite right. Is `0.29 * 100` stored exactly? | correct | unit basis: first row of items[5] |
| homework-1 | items[5].feedback.byKey.round | You expected rounding. The product is a hair below 29, and converting a `double` to an `int` drops … | correct | unit basis: first row of items[5] |
| homework-1 | items[5].explain.text | 0.29 is stored slightly low, so the product is 28.999999999999996 and the conversion truncates to 2… | correct | unit basis: first row of items[5] |
| homework-1 | items[6].prompt | prompt: A colleague ports a Python backtest to C++. Two results look wrong. ```cpp int total_qty = … | correct | run under the app compiler and grader: -1294967296 and 2500000 (checks homework-1.6); g++ and clang++ silent under -Wall -Wextra -Wconversion; UBSan reports the overflow; clang-tidy bugprone-integer-division flags the division (checks homework-1.6) |
| homework-1 | items[6].model | model answer: **The volume.** `total_qty` is an `int`, which holds at most 2,147,483,647. Two fills… | correct | unit basis: first row of items[6] |
| homework-1 | items[6].rubric[0] | rubric: Explains that `int` stops at 2,147,483,647 and that 3,000,000,000 wraps to −1,294,967,296 (… | correct | unit basis: first row of items[6] |
| homework-1 | items[6].rubric[1] | rubric: Explains that `int / int` is integer division, done before the result reaches the `double` | correct | unit basis: first row of items[6] |
| homework-1 | items[6].rubric[2] | rubric: Says why Python hid both: unbounded integers and `/` always giving a float | correct | unit basis: first row of items[6] |
| homework-1 | items[6].rubric[3] | rubric: Gives a correct fix for the total in code: a `long long` accumulator | correct | unit basis: first row of items[6] |
| homework-1 | items[6].rubric[4] | rubric: Fixes the average in code by converting to `double` before dividing; notes that converting … | correct | unit basis: first row of items[6] |
| homework-1 | items[6].rubric[5] | rubric: Names a way to catch each sooner: a unit test with large or odd values, a sanitiser build f… | correct | unit basis: first row of items[6] |
| homework-1 | items[7].prose | ```text $ g++ -std=c++17 main.cpp pricer.cpp -o backtest /usr/bin/ld: /tmp/ccg6pEss.o: in function … | correct | as l4 s7 (checks l4.s7): one body in one .cpp, or inline |
| homework-1 | items[7].widget.options[0] | key: Keep only the declaration in `returns.h` and move the body into `returns.cpp`, added to the bu… | correct | unit basis: first row of items[7] |
| homework-1 | items[7].widget.options[1].why | wrong option: Add include guards as well as `#pragma once` :: Guards and `#pragma once` do the same… | correct | unit basis: first row of items[7] |
| homework-1 | items[7].widget.options[2].why | wrong option: Include `returns.h` in `main.cpp` only :: Then `pricer.cpp` calls `simple_return` wit… | correct | unit basis: first row of items[7] |
| homework-1 | items[7].widget.options[3].why | wrong option: Put `pricer.cpp` before `main.cpp` in the command :: The order of files does not matt… | correct | unit basis: first row of items[7] |
| homework-1 | items[7].feedback.correct | Declarations in headers, one body in one `.cpp`. | correct | unit basis: first row of items[7] |
| homework-1 | items[7].feedback.generic | Not quite right. How many bodies does the program end up with? | correct | unit basis: first row of items[7] |
| homework-1 | items[7].explain.text | Every `.cpp` that includes a header with a body compiles its own copy, and the linker refuses two. … | correct | unit basis: first row of items[7] |
| homework-1 | items[8].prose | A feed gives each trade's price in ticks and its size in shares, in time order. The tick rule guess… | correct | tick test of Lee and Ready (1991), with the zero-tick carry; run under the app compiler and grader: solution passes all ten tests; cpp-1-perf-numbers.py exit 0 |
| homework-1 | items[8].widget | code: 10 tests; solution passes, starter fails | correct | unit basis: first row of items[8] |
| homework-1 | items[8].feedback.correct | Correct. The sign carries through flat trades, and the total lives in a `long long`. | correct | unit basis: first row of items[8] |
| homework-1 | items[8].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of items[8] |
| homework-1 | items[8].explain.text | The first trade has sign 0, so start at the second and compare each price with the one before. A fl… | correct | unit basis: first row of items[8] |
| l5-value-or-reference | screens[0].prose | In Python, a function that appends to the list you pass changes your list, as the session above sho… | correct | [dcl.init]: a by-value parameter is copy-initialised from the argument; run under the app compiler and grader prints 2 (check l5 s0); Python passes object references (language reference 4.7) |
| l5-value-or-reference | screens[0].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].widget.options[0] | key: `2` | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].widget.options[1].why | wrong option: `3` :: You read it as Python, where the call shares the list. In C++ `costs` is a new… | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].widget.options[2].why | wrong option: `0` :: `costs` starts as a full copy of `mine`, and nothing ever empties `mine`. | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].widget.options[3].why | wrong option: It does not compile :: It compiles. A parameter of type `std::vector<double>` simply … | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].hints[0] | hint: Is `costs` the caller's vector, or a vector of its own? | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].hints[1] | hint: Look at the parameter type. It has no `&` or anything else after the type. | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].hints[2] | hint: `costs` is built as a copy of `mine`. `push_back` grows the copy, which is destroyed when the… | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].feedback.correct | The copy grew; `mine` did not. | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].feedback.generic | Not quite right. Ask whether `costs` is `mine` itself or a copy of it. | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].feedback.byKey.three | You read it as Python, where the call shares the list. In C++ `costs` is a new vector, copied from … | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].explain.text | `costs` is a separate vector, copied from `mine` when the call starts. `push_back` grows that copy,… | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[0].explain.canvas.lines | canvas: main: mine = {250.00, 120.00} / add_fee: costs = {250.00, 120.00, 1.50} (a copy) / after th… | correct | unit basis: first row of screens[0] |
| l5-value-or-reference | screens[1].prose | In C++ a variable *is* its object: a box in memory. Adding `&` to the type makes a second name for … | correct | [dcl.ref]: a reference is another name for an existing object; copy made before the push holds two prices |
| l5-value-or-reference | screens[1].canvas.state.caption | caption: The two vector objects after the last line | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[1].widget.answer | key: {"big": ["mine", "alias"], "small": ["copy"]} | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[1].hints[0] | hint: Which line builds a second vector? The other names share the first one. | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[1].hints[1] | hint: `copy` has no `&`, so it is a new box. | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[1].hints[2] | hint: `mine` and `alias` name the box that `push_back` grew. `copy` names its own box, still `{250,… | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[1].feedback.correct | `mine` and `alias` name one box; `copy` is its own. | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[1].feedback.generic | Not quite right. Only a declaration without `&` builds a new box. | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[1].feedback.byKey.mine | `mine` is the box the vector was built in, and the `push_back` through `alias` grew it. | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[1].feedback.byKey.alias | `alias` was declared with `&`, so it names the box `mine` already names. No new vector is made. | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[1].feedback.byKey.copy | `copy` has no `&`, so it is a new box, filled with `mine`'s two prices before the push. | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[1].explain.text | `alias` is a second name for `mine`'s box, so pushing through `alias` grew that box. `copy` is its … | correct | unit basis: first row of screens[1] |
| l5-value-or-reference | screens[2].prose | A name declared with `&` is a **reference**: another name for an object that already exists. A refe… | correct | [dcl.ref]; 1000 - 2.5 = 997.5; run under the app compiler and grader prints 997.5 (check l5 s2); default floating output drops trailing zeros |
| l5-value-or-reference | screens[2].canvas.state.caption | caption: During the call: `balance` and `cash` name one `double` | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].widget.options[0] | key: `997.5` | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].widget.options[1].why | wrong option: `1000` :: That is what happens without the `&`. Here `balance` is another name for `c… | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].widget.options[2].why | wrong option: `2.5` :: `balance -= fee` subtracts the fee from the balance. It does not replace the… | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].widget.options[3].why | wrong option: `997.50` :: The value is right, but `std::cout` prints a `double` without trailing ze… | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].hints[0] | hint: Is `balance` a copy of `cash`, or another name for it? | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].hints[1] | hint: Both `cash` and `balance` point at the same box. | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].hints[2] | hint: `balance -= fee` changes the one `double` that both names share: 1000 minus 2.5 is 997.5. | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].feedback.correct | `balance` is `cash` under another name. | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].feedback.generic | Not quite right. Follow the arrows: which box does `balance -= fee` change? | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].feedback.byKey.unchanged | That is what happens without the `&`. Here `balance` is another name for `cash`, so `cash` changes. | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[2].explain.text | `balance` is a reference, so it names the same `double` as `cash`. Subtracting 2.50 through `balanc… | correct | unit basis: first row of screens[2] |
| l5-value-or-reference | screens[3].prose | `prices` holds 1,000,000 prices, and `mean` only reads them. We want `v` to be a second name for `p… | correct | [dcl.ref], [dcl.type.cv]: a const reference shares without copying and forbids writes through it |
| l5-value-or-reference | screens[3].canvas.state.caption | caption: Which parameter type joins `v` to this box, read only? | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].widget.options[0] | key: `double mean(const std::vector<double>& v)` | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].widget.options[1].why | wrong option: `double mean(std::vector<double> v)` :: That builds a second box and copies all 1,000… | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].widget.options[2].why | wrong option: `double mean(std::vector<double>& v)` :: That shares the box, but it lets `mean` chan… | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].widget.options[3].why | wrong option: `double mean(const std::vector<double> v)` :: `const` stops changes, but without `&` … | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].hints[0] | hint: Two things are needed: no copy, and no changes. | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].hints[1] | hint: `&` gives the sharing. What gives the read only part? | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].hints[2] | hint: `const std::vector<double>&` is a reference, so nothing is copied, and `const` makes `v` read… | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].feedback.correct | Shared and read only. | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].feedback.generic | Not quite right. Find the type that has both `&` and `const`. | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].feedback.byKey.value | That copies all 1,000,000 prices into `v` on every call. | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].feedback.byKey.cvalue | Without `&` this is still a copy, even if it is a read-only one. | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].explain.text | `const std::vector<double>& v` makes `v` a second name for `prices`, so nothing is copied. `const` … | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[3].explain.canvas.caption | caption: `v` names the same box; the dashed arrow is read only | correct | unit basis: first row of screens[3] |
| l5-value-or-reference | screens[4].prose | A `double` takes 8 bytes. Passing a vector by value copies every element into a new buffer. The tab… | correct | 1,000,000 x 8 bytes = 8 MB; run under the app compiler and grader: by-value times 0.13, 1.8, 23 and 990 microseconds, const& about 4 ns, within a factor of 10 of the table (check l5.s4 copy timings); 1,000 x 1 ms = 1 s |
| l5-value-or-reference | screens[4].canvas.state.caption | caption: A `const&` call took a few nanoseconds at every size: nothing is copied. | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].widget.answer | key: 8 (How many megabytes does one by-value call copy for 1,000,000 prices? Take 1 MB as 1,000,000… | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].widget.accept | accept: 8 MB: 1,000,000 prices times 8 bytes is 8,000,000 bytes. | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].widget.wrong[0] | slip: 8000000 (bytes) | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].widget.wrong[1] | slip: 1 (one) | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].widget.wrong[2] | slip: 64 (bits) | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].hints[0] | hint: Each price is 8 bytes. How many bytes is a million of them? | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].hints[1] | hint: Follow the column: each row multiplies the number of prices by 8. | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].hints[2] | hint: 1,000,000 times 8 bytes is 8,000,000 bytes, which is 8 MB. | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].feedback.correct | 8 MB on every call. | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].feedback.generic | Not quite right. Multiply the number of prices by 8 bytes, then convert to MB. | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].feedback.byKey.bytes | That is the count in bytes. Divide by 1,000,000 to get megabytes. | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].feedback.byKey.one | That counts one byte per price. A `double` takes 8. | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].feedback.byKey.bits | You multiplied by 64, the bits in a `double`. Count bytes: 8 each. | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].explain.text | Each of the 1,000,000 prices takes 8 bytes, so a by-value call copies 8,000,000 bytes, which is 8 M… | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[4].explain.canvas.values | canvas: {"r3c1": "8,000,000"} | correct | unit basis: first row of screens[4] |
| l5-value-or-reference | screens[5].prose | A book holds share quantities and their prices in £, one entry per stock. Its value is the sum of q… | correct | run under the app compiler and grader: solution passes, starter fails; the postlude static_assert fixes the signature; 485 + 180 + 1248 = 1913 |
| l5-value-or-reference | screens[5].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[5] |
| l5-value-or-reference | screens[5].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[5] |
| l5-value-or-reference | screens[5].hints[0] | hint: Start with the signature: two `const std::vector<double>&` parameters, returning `double`. | correct | unit basis: first row of screens[5] |
| l5-value-or-reference | screens[5].hints[1] | hint: Loop over the indices with `std::size_t i` from 0 to `qty.size()`. | correct | unit basis: first row of screens[5] |
| l5-value-or-reference | screens[5].hints[2] | hint: Set `double total = 0;`, add `qty[i] * px[i]` for each `i`, then `return total;`. An empty bo… | correct | unit basis: first row of screens[5] |
| l5-value-or-reference | screens[5].feedback.correct | Both vectors are read in place; nothing is copied. | correct | unit basis: first row of screens[5] |
| l5-value-or-reference | screens[5].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of screens[5] |
| l5-value-or-reference | screens[5].explain.text | `const std::vector<double>&` hands the function the caller's vectors without copying them. The loop… | correct | unit basis: first row of screens[5] |
| l5-value-or-reference | screens[6].prose | A colleague wants weights that add up to 1. Their function works on its own copy without anyone not… | correct | as s0: the division happens in the copy; run under the app compiler and grader prints 2 (check l5 s6); 2/10, 3/10, 5/10 |
| l5-value-or-reference | screens[6].canvas.state.caption | caption: Two boxes: the parameter has no `&` | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].widget.options[0] | key: `2` | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].widget.options[1].why | wrong option: `0.2` :: You assumed the call changes the caller's vector. Without `&`, `normalise` d… | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].widget.options[2].why | wrong option: It does not compile :: It compiles cleanly. Taking a vector by value is legal; it jus… | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].widget.options[3].why | wrong option: `1` :: `w[0]` is the first weight, 2, and nothing changed it in the caller. | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].hints[0] | hint: Which box does `x /= sum` divide? | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].hints[1] | hint: `normalise`'s `w` is a separate box. | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].hints[2] | hint: The parameter has no `&`, so the division happens in the copy. The caller's `w[0]` is still 2. | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].feedback.correct | The copy was normalised; the caller's weights were not. | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].feedback.generic | Not quite right. Check whether `normalise`'s `w` is the caller's vector or a copy. | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].feedback.byKey.fifth | You assumed the call changes the caller's vector. Without `&`, `normalise` divides its own copy, wh… | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[6].explain.text | `normalise` divided its own copy, `{0.2, 0.3, 0.5}`, and that copy died when the call was over. The… | correct | unit basis: first row of screens[6] |
| l5-value-or-reference | screens[7].prose | Fix `normalise` so it changes the caller's weights. Weights may be negative (a short position). If … | correct | run under the app compiler and grader: solution passes, the by-value starter fails test 1 (check l5.s7); IEEE 754: x / 0 is infinity and 0 / 0 is NaN |
| l5-value-or-reference | screens[7].widget | code: 6 tests; solution passes, starter fails | correct | unit basis: first row of screens[7] |
| l5-value-or-reference | screens[7].hints[0] | hint: Two fixes: the parameter type, and the case where the sum is 0. | correct | unit basis: first row of screens[7] |
| l5-value-or-reference | screens[7].hints[1] | hint: Add `&` after the type so `w` names the caller's vector. | correct | unit basis: first row of screens[7] |
| l5-value-or-reference | screens[7].hints[2] | hint: Write `std::vector<double>& w`. After summing, `if (sum == 0) return;` before dividing. | correct | unit basis: first row of screens[7] |
| l5-value-or-reference | screens[7].feedback.correct | The caller's weights now add up to 1. | correct | unit basis: first row of screens[7] |
| l5-value-or-reference | screens[7].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of screens[7] |
| l5-value-or-reference | screens[7].explain.text | With `std::vector<double>& w`, every `x /= sum` divides the caller's own weights. The early `return… | correct | unit basis: first row of screens[7] |
| l5-value-or-reference | screens[8].prose | Each parameter type says what the function will do with your object. ```cpp void f(std::vector<doub… | correct | [class.copy.elision]: a returned local is built in place where the compiler can, and otherwise moved; run: 0 copies and 0 moves, or 1 move with elision off (checks l5.s8); a plain T& rejects temporaries and const objects: [dcl.init.ref] |
| l5-value-or-reference | screens[8].widget.options[0] | key: `const std::vector<double>& prices` | correct | unit basis: first row of screens[8] |
| l5-value-or-reference | screens[8].widget.options[1].why | wrong option: `std::vector<double> prices` :: That copies 8 MB on every call, only to read it. | correct | unit basis: first row of screens[8] |
| l5-value-or-reference | screens[8].widget.options[2].why | wrong option: `std::vector<double>& prices` :: That compiles, but it claims the function may change… | correct | unit basis: first row of screens[8] |
| l5-value-or-reference | screens[8].feedback.correct | Read only, and no copy. | correct | unit basis: first row of screens[8] |
| l5-value-or-reference | screens[8].feedback.generic | Not quite right. The function only reads, and the vector is large. | correct | unit basis: first row of screens[8] |
| l5-value-or-reference | screens[8].explain.text | A function that only reads a large object takes it by `const&`. Small values such as `double` and `… | correct | unit basis: first row of screens[8] |
| l5-value-or-reference | screens[9].prose | Two reference parameters let one function change two of the caller's variables. Here `a` and `b` ar… | correct | trace of the three assignments through the references |
| l5-value-or-reference | screens[9].widget.options[0] | key: `a = b;` | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[9].widget.options[1].why | wrong option: `b = a;` :: That copies `a` into `b`, so the old `b` is lost and both end up as the o… | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[9].widget.options[2].why | wrong option: `t = b;` :: `t` holds the old `a`. Overwriting it loses that value, and `a` never cha… | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[9].widget.options[3].why | wrong option: `a = t;` :: `t` is a copy of `a`, so this writes `a` back into itself and changes not… | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[9].hints[0] | hint: After the first line, `t` keeps the old `a`. What should `a` become? | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[9].hints[1] | hint: Each line has one job: save `a`, then overwrite `a`, then fill `b`. | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[9].hints[2] | hint: `a` should take `b`'s value, which is safe because `t` saved the old `a`. Then `b = t` finish… | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[9].feedback.correct | Save, overwrite, fill. | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[9].feedback.generic | Not quite right. After saving `a` in `t`, which variable can be overwritten safely? | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[9].feedback.byKey.ba | That copies `a` into `b` before `b` is saved, so the old `b` is lost. | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[9].explain.text | Line 1 saves the old `a` in `t`. Line 2 overwrites `a` with `b`, which is safe because `t` holds th… | correct | unit basis: first row of screens[9] |
| l5-value-or-reference | screens[10].prose | A risk engine revalues a desk 1,000 times a second. The order book has 50,000 price levels and is o… | correct | [dcl.ref], [dcl.type.cv] applied to the two arguments: read-only large object, caller-visible change |
| l5-value-or-reference | screens[10].widget.options[0] | key: `void revalue(const OrderBook& book, std::vector<Position>& pos)` | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].widget.options[1].why | wrong option: `void revalue(OrderBook book, std::vector<Position> pos)` :: That copies the whole bo… | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].widget.options[2].why | wrong option: `void revalue(OrderBook& book, const std::vector<Position>& pos)` :: The `const` is o… | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].widget.options[3].why | wrong option: `void revalue(const OrderBook book, std::vector<Position>& pos)` :: The positions are… | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].hints[0] | hint: Ask two questions per argument: is it large, and does the function change it? | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].hints[1] | hint: The book is large and read only. The positions are changed and must reach the caller. | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].hints[2] | hint: Book: `const OrderBook&`. Positions: `std::vector<Position>&`. | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].feedback.correct | Read the book in place; change the positions in place. | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].feedback.generic | Not quite right. One argument is read only; the other must be changed for the caller. | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].feedback.byKey.copies | Both arguments are copied, so the P&L updates are lost. | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].feedback.byKey.swapped | The `const` belongs on the book, which is only read. | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | screens[10].explain.text | The book is large and only read, so `const OrderBook&` shares it at no cost. The positions must cha… | correct | unit basis: first row of screens[10] |
| l5-value-or-reference | quiz[0].prose | ```cpp int x = 5; int& r = x; int& r2 = r; r2 = 9; std::cout << x << "\n"; ``` | correct | [dcl.ref]/5: there are no references to references; run under the app compiler and grader prints 9 (check l5 quiz0) |
| l5-value-or-reference | quiz[0].widget.options[0] | key: `9` | correct | unit basis: first row of quiz[0] |
| l5-value-or-reference | quiz[0].widget.options[1].why | wrong option: `5` :: You read `r2` as a copy of `r`. A reference made from a reference names the sa… | correct | unit basis: first row of quiz[0] |
| l5-value-or-reference | quiz[0].widget.options[2].why | wrong option: It does not compile :: `int& r2 = r;` is fine: `r` is just another name for `x`, so `… | correct | unit basis: first row of quiz[0] |
| l5-value-or-reference | quiz[0].feedback.correct | Three names, one `int`. | correct | unit basis: first row of quiz[0] |
| l5-value-or-reference | quiz[0].feedback.generic | Not quite right. What does `r` name? | correct | unit basis: first row of quiz[0] |
| l5-value-or-reference | quiz[0].explain.text | `r` names `x`, so `int& r2 = r;` makes `r2` name `x` too. There is no reference to a reference: `r2… | correct | unit basis: first row of quiz[0] |
| l5-value-or-reference | quiz[1].prose | ```cpp void apply_fee(double& balance, double fee) { balance -= fee; } int main() { apply_fee(100.0… | correct | [dcl.init.ref]: a non-const lvalue reference cannot bind a temporary; run under the app compiler and grader: "expects an lvalue for 1st argument" (check l5.quiz1) |
| l5-value-or-reference | quiz[1].widget.options[0] | key: It does not compile: a plain `double&` cannot bind to the temporary `100.0` | correct | unit basis: first row of quiz[1] |
| l5-value-or-reference | quiz[1].widget.options[1].why | wrong option: It prints nothing and runs :: A non-const reference must name a real variable. `100.0… | correct | unit basis: first row of quiz[1] |
| l5-value-or-reference | quiz[1].widget.options[2].why | wrong option: It compiles and changes a hidden copy :: C++ will not make a hidden copy for a plain … | correct | unit basis: first row of quiz[1] |
| l5-value-or-reference | quiz[1].feedback.correct | A plain reference needs a variable to change. | correct | unit basis: first row of quiz[1] |
| l5-value-or-reference | quiz[1].feedback.generic | Not quite right. What would `balance -= fee` change here? | correct | unit basis: first row of quiz[1] |
| l5-value-or-reference | quiz[1].explain.text | `apply_fee` promises to change its first argument, so the argument must be a variable. clang says "… | correct | unit basis: first row of quiz[1] |
| l5-value-or-reference | quiz[2].prose | ```cpp std::vector<double> make_prices(int n) { std::vector<double> v(n, 100.0); return v; } std::v… | correct | [class.copy.elision]; run: 0 copies (checks l5.s8) |
| l5-value-or-reference | quiz[2].widget.options[0] | key: None: the vector is built in `px` itself, or moved there | correct | unit basis: first row of quiz[2] |
| l5-value-or-reference | quiz[2].widget.options[1].why | wrong option: Once, from `v` into `px` :: That was the worry before copy elision. The compiler buil… | correct | unit basis: first row of quiz[2] |
| l5-value-or-reference | quiz[2].widget.options[2].why | wrong option: Twice, into a temporary and then into `px` :: The compiler removes both copies. A ret… | correct | unit basis: first row of quiz[2] |
| l5-value-or-reference | quiz[2].feedback.correct | Return by value freely. | correct | unit basis: first row of quiz[2] |
| l5-value-or-reference | quiz[2].feedback.generic | Not quite right. What does copy elision do with a returned local? | correct | unit basis: first row of quiz[2] |
| l5-value-or-reference | quiz[2].explain.text | The compiler usually builds `v` in the caller's `px` from the start; when it does not, it moves `v`… | correct | unit basis: first row of quiz[2] |
| l5-value-or-reference | quiz[3].widget.options[0] | key: `std::vector<double>& costs` | correct | Python shares the caller's list; T& does the same in C++ |
| l5-value-or-reference | quiz[3].widget.options[1].why | wrong option: `std::vector<double> costs` :: That is C++'s default, a copy. Python's call shares th… | correct | unit basis: first row of quiz[3] |
| l5-value-or-reference | quiz[3].widget.options[2].why | wrong option: `const std::vector<double>& costs` :: It shares, but `const` forbids `push_back`, so … | correct | unit basis: first row of quiz[3] |
| l5-value-or-reference | quiz[3].feedback.correct | A plain reference shares and allows changes, as Python does. | correct | unit basis: first row of quiz[3] |
| l5-value-or-reference | quiz[3].feedback.generic | Not quite right. Python shares the list and lets the function change it. | correct | unit basis: first row of quiz[3] |
| l5-value-or-reference | quiz[3].explain.text | A Python call shares the caller's list and may change it. In C++ that needs `&` without `const`. Wi… | correct | unit basis: first row of quiz[3] |
| l5-value-or-reference | summary.ideas[0] | A C++ variable is its object. Passing by value gives the function its own copy; `T&` passes a secon… | correct | restates s0, s2, s3, s8 |
| l5-value-or-reference | summary.ideas[1] | `const T&` shares without copying and promises not to change; it also accepts temporaries such as `… | correct | unit basis: first row of summary |
| l5-value-or-reference | summary.ideas[2] | Return results by value: the compiler builds them in the caller's variable, so a returned vector is… | correct | unit basis: first row of summary |
| l5-value-or-reference | summary.formula | Choosing a parameter: \texttt{T} \to \text{copy}, \qquad \texttt{const T\&} \to \text{read}, \qquad… | correct | unit basis: first row of summary |
| l5-value-or-reference | summary.trap | Forgetting `&` compiles cleanly: the function changes its own copy and the caller sees nothing. | correct | unit basis: first row of summary |
| l6-const | screens[0].prose | A tick is the smallest price step an exchange allows. In Python a name can always be pointed at a n… | correct | [dcl.type.cv]: a const object cannot be assigned; run under the app compiler and grader: both quoted lines with 3:10 and 2:18 (check l6.s0) |
| l6-const | screens[0].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].widget.options[0] | key: The compiler rejects line 3 | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].widget.options[1].why | wrong option: It builds, and `tick` ends as 0.05 :: That is the Python habit of rebinding a name. `… | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].widget.options[2].why | wrong option: It builds, and line 3 is ignored, so `tick` stays 0.01 :: C++ never ignores a line si… | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].widget.options[3].why | wrong option: It builds, then stops with an error when line 3 runs :: `const` is checked by the com… | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].hints[0] | hint: When is `const` checked: while compiling, or while running? | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].hints[1] | hint: Line 3 assigns to `tick`, which line 2 declared `const`. | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].hints[2] | hint: The compiler checks every assignment against the type. `const double` cannot be assigned, so … | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].feedback.correct | The build stops at line 3. | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].feedback.generic | Not quite right. `const` is a promise the compiler checks before anything runs. | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].feedback.byKey.five | That is the Python habit of rebinding a name. `const` forbids any assignment after the declaration. | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].explain.text | The compiler checks every assignment against the variable's type. `tick` is a `const double`, so li… | correct | unit basis: first row of screens[0] |
| l6-const | screens[0].explain.canvas.lines | canvas: main.cpp:3:10: error: cannot assign to variable 'tick' / with const-qualified type 'const d… | correct | unit basis: first row of screens[0] |
| l6-const | screens[1].prose | `const double& px` makes `px` a read-only name for the caller's price. The other parameter, `fee`, … | correct | run under the app compiler and grader: only line 4 is rejected, with the quoted text, 1 error (check l6.s1) |
| l6-const | screens[1].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].widget.answer | key: ["l4"] | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].widget.wrong[0] | slip: ["l4", "l5"] (fee-too) | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].widget.wrong[1] | slip: ["l3", "l4"] (copy) | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].hints[0] | hint: Which lines assign to something? Of those, which name is `const`? | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].hints[1] | hint: Only `px` carries `const`. `out` is a new local copy. | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].hints[2] | hint: Line 4 writes through `px`, which is read only. Lines 3 and 5 change `out` and `fee`, which a… | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].feedback.correct | Only line 4 writes through the `const` name. | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].feedback.generic | Not quite right. Find the lines that write to `px` itself. | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].feedback.byKey.fee-too | `fee` has no `const`: it is the function's own copy, so `fee = 0` is allowed. Only line 4 writes th… | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].feedback.byKey.copy | `out` is a new `double` copied from `px`. Changing the copy is fine; only line 4 writes through `px… | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].feedback.byKey.l2 | Line 2 reads `px` to copy it. Reading is what `const` allows. | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].feedback.byKey.l5 | `fee` has no `const`, so line 5 is allowed. | correct | unit basis: first row of screens[1] |
| l6-const | screens[1].explain.text | Line 4 is the only write through `px`. Clang says "cannot assign to variable 'px' with const-qualif… | correct | unit basis: first row of screens[1] |
| l6-const | screens[2].prose | A `const` reference parameter is a **const reference**: the function may read the caller's object b… | correct | [dcl.init.ref]; run under the app compiler and grader: mean(prices) compiles, the braced list gives "expects an lvalue", the const vector "would lose const qualifier" (checks l6.s2) |
| l6-const | screens[2].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].widget.options[0] | key: Only `mean(prices)` | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].widget.options[1].why | wrong option: All three :: A plain reference may change its object. So the compiler refuses a tempo… | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].widget.options[2].why | wrong option: `mean(prices)` and `mean(fixed)` :: `fixed` is `const`. Binding a plain reference to … | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].widget.options[3].why | wrong option: `mean(prices)` and `mean({101.5, 99.0})` :: `{101.5, 99.0}` is a temporary. A plain r… | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].hints[0] | hint: A plain reference says the function might change the argument. Which arguments must not be ch… | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].hints[1] | hint: `fixed` is `const`, and `{101.5, 99.0}` is a temporary with no name. | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].hints[2] | hint: Only `prices` is a non-const variable. Adding `const` to the parameter makes all three calls … | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].feedback.correct | Only a non-const variable binds to a plain reference. | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].feedback.generic | Not quite right. Ask which arguments the function would be allowed to change. | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].feedback.byKey.all | A plain reference may change its object, so it refuses the temporary and the `const` vector. | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].explain.text | A plain reference may change its argument, so it accepts only a non-const variable. With `const std… | correct | unit basis: first row of screens[2] |
| l6-const | screens[2].explain.canvas.lines | canvas: double mean(const std::vector<double>& v); / / std::vector<double> prices{101.5, 99.0}; / c… | correct | unit basis: first row of screens[2] |
| l6-const | screens[3].prose | `const` after a method's parameter list promises the method does not change the object. A `const` o… | correct | [class.mfct.non.static]: a const object calls only const member functions; run under the app compiler and grader: mid and bid compile, widen gives "function is not marked const", the assignment is rejected (checks l6.s3) |
| l6-const | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].widget.options[0] | key: `double m = q.mid();` | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].widget.options[1] | key: `double b = q.bid;` | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].widget.options[2].why | wrong option: `q.widen(0.01);` :: `widen` is not marked `const`, so a `const Quote` cannot call it.… | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].widget.options[3].why | wrong option: `q.ask = 100.05;` :: `q` is `const`, so every member is read only, and assigning to `… | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].hints[0] | hint: Reading is always allowed. Which lines would change `q`? | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].hints[1] | hint: Line 3 has `const` after `()`; line 4 does not. | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].hints[2] | hint: `mid()` is a `const` method and reading `q.bid` is fine. `widen` and the assignment would cha… | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].feedback.correct | A `const` object reads and calls `const` methods only. | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].feedback.generic | Not quite right. Keep the lines that only read `q`. | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].feedback.byKey.widen | `widen` is not marked `const`, so a `const Quote` cannot call it, even before it runs. | correct | unit basis: first row of screens[3] |
| l6-const | screens[3].explain.text | `q.mid()` compiles because `mid` is marked `const`, and reading `q.bid` is always fine. `q.widen(0.… | correct | unit basis: first row of screens[3] |
| l6-const | screens[4].prose | The data in `Quote` is private: read it through the `const` getters `bid()` and `ask()`. The starte… | correct | run under the app compiler and grader: solution passes, starter does not compile; the static_assert postlude fixes the signature |
| l6-const | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[4] |
| l6-const | screens[4].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[4] |
| l6-const | screens[4].hints[0] | hint: Two fixes: the parameter type, and how the prices are read. | correct | unit basis: first row of screens[4] |
| l6-const | screens[4].hints[1] | hint: `bid_` and `ask_` are private. The getters are `bid()` and `ask()`, with brackets. | correct | unit basis: first row of screens[4] |
| l6-const | screens[4].hints[2] | hint: Write `double spread(const Quote& q) { return q.ask() - q.bid(); }`. The getters are `const`,… | correct | unit basis: first row of screens[4] |
| l6-const | screens[4].feedback.correct | Read only, and it accepts any `Quote`. | correct | unit basis: first row of screens[4] |
| l6-const | screens[4].feedback.generic | Not yet. The results under the editor say what failed. | correct | unit basis: first row of screens[4] |
| l6-const | screens[4].feedback.byKey.compile | Read the compiler's first error. Private members are reached through `q.ask()` and `q.bid()`, and t… | correct | unit basis: first row of screens[4] |
| l6-const | screens[4].explain.text | `const Quote&` accepts a variable, a `const` quote and a temporary, without copying. Inside, only `… | correct | unit basis: first row of screens[4] |
| l6-const | screens[5].prose | `constexpr` asks for more than `const`: the value must be known while compiling. The compiler can t… | correct | [dcl.constexpr]/10: a constexpr variable needs a constant initialiser; run under the app compiler and grader: line 5 rejected with the quoted text, the other five lines compile (checks l6.s5) |
| l6-const | screens[5].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[5] |
| l6-const | screens[5].widget.answer | key: ["l5"] | correct | unit basis: first row of screens[5] |
| l6-const | screens[5].hints[0] | hint: Which values could the compiler work out without running anything? | correct | unit basis: first row of screens[5] |
| l6-const | screens[5].hints[1] | hint: `read_tick()` runs only when the program starts. | correct | unit basis: first row of screens[5] |
| l6-const | screens[5].hints[2] | hint: Line 5 asks for a compile-time value from a run-time call. Line 6 is fine: `const` only forbi… | correct | unit basis: first row of screens[5] |
| l6-const | screens[5].feedback.correct | A `constexpr` value cannot come from a run-time call. | correct | unit basis: first row of screens[5] |
| l6-const | screens[5].feedback.generic | Not quite right. Find the `constexpr` whose value needs the program to run. | correct | unit basis: first row of screens[5] |
| l6-const | screens[5].feedback.byKey.l6 | Line 6 uses `const`, which only forbids later changes. Its value may come from a run-time call. | correct | unit basis: first row of screens[5] |
| l6-const | screens[5].feedback.byKey.l3 | `tick * lot_size` uses two `constexpr` values, so the compiler can multiply them itself. | correct | unit basis: first row of screens[5] |
| l6-const | screens[5].explain.text | Line 5 is rejected: "constexpr variable 'live_tick' must be initialized by a constant expression". … | correct | unit basis: first row of screens[5] |
| l6-const | screens[6].prose | `view` is a read-only name for `px`. (`const int x` and `int const x` mean the same; the place of `… | correct | const restricts the access path, not the object: [dcl.type.cv]/3; run under the app compiler and grader prints 99 (check l6.s6) |
| l6-const | screens[6].canvas.state.caption | caption: Two names, one vector; the dashed name is read only | correct | unit basis: first row of screens[6] |
| l6-const | screens[6].widget.options[0] | key: `99` | correct | unit basis: first row of screens[6] |
| l6-const | screens[6].widget.options[1].why | wrong option: `100` :: You treated `const` as freezing the vector. It only stops changes made throu… | correct | unit basis: first row of screens[6] |
| l6-const | screens[6].widget.options[2].why | wrong option: It does not compile :: `px` is not `const`, so `px[0] = 99.0` is allowed. Only writes… | correct | unit basis: first row of screens[6] |
| l6-const | screens[6].hints[0] | hint: How many vectors are there? | correct | unit basis: first row of screens[6] |
| l6-const | screens[6].hints[1] | hint: `view` and `px` name the same box. | correct | unit basis: first row of screens[6] |
| l6-const | screens[6].hints[2] | hint: `px[0] = 99.0` changes the one vector. `view[0]` reads that vector, so it prints 99. | correct | unit basis: first row of screens[6] |
| l6-const | screens[6].feedback.correct | `const` limited `view`, not the vector. | correct | unit basis: first row of screens[6] |
| l6-const | screens[6].feedback.generic | Not quite right. Count the vectors, then ask which name did the writing. | correct | unit basis: first row of screens[6] |
| l6-const | screens[6].feedback.byKey.hundred | You treated `const` as freezing the vector. It only stops changes made through `view`; `px` changed… | correct | unit basis: first row of screens[6] |
| l6-const | screens[6].explain.text | There is one vector with two names. `const` restricts the name `view`, so `view[0] = 1` would not c… | correct | unit basis: first row of screens[6] |
| l6-const | screens[7].prose | This function does not compile: it writes through a `const` reference. Keep the promise to the call… | correct | run under the app compiler and grader: starter gives the canvas message at 5:15; solution passes (check l6.s7); return of a local: [class.copy.elision] |
| l6-const | screens[7].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[7] |
| l6-const | screens[7].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[7] |
| l6-const | screens[7].hints[0] | hint: You may not change `px`. What may you change? | correct | unit basis: first row of screens[7] |
| l6-const | screens[7].hints[1] | hint: A local `std::vector<double> out = px;` is your own copy. | correct | unit basis: first row of screens[7] |
| l6-const | screens[7].hints[2] | hint: Copy into `out`, add `fee` to each `out[i]`, and `return out;`. Returning it is free: copy el… | correct | unit basis: first row of screens[7] |
| l6-const | screens[7].feedback.correct | One deliberate copy, and the caller's prices are untouched. | correct | unit basis: first row of screens[7] |
| l6-const | screens[7].feedback.generic | Not yet. The results under the editor say what failed. | correct | unit basis: first row of screens[7] |
| l6-const | screens[7].feedback.byKey.compile | The parameter must stay `const std::vector<double>&`. Change a local copy instead of `px`. | correct | unit basis: first row of screens[7] |
| l6-const | screens[7].explain.text | `std::vector<double> out = px;` is the one copy this function needs, and it is yours to change. The… | correct | unit basis: first row of screens[7] |
| l6-const | screens[8].prose | Every `const` you used is a promise the compiler checks. ```cpp const double tick = 0.01; // never … | correct | restates s0, s3, s5 |
| l6-const | screens[8].widget.options[0] | key: Only those marked `const` | correct | unit basis: first row of screens[8] |
| l6-const | screens[8].widget.options[1].why | wrong option: All of them :: A method without `const` may change the object, so the compiler stops … | correct | unit basis: first row of screens[8] |
| l6-const | screens[8].widget.options[2].why | wrong option: None of them: it can only read members :: Methods marked `const` are allowed, and get… | correct | unit basis: first row of screens[8] |
| l6-const | screens[8].feedback.correct | Only methods that promise not to change it. | correct | unit basis: first row of screens[8] |
| l6-const | screens[8].feedback.generic | Not quite right. Think back to `widen` and `mid`. | correct | unit basis: first row of screens[8] |
| l6-const | screens[8].explain.text | A `const` object can read its members and call `const` methods. Mark every method that does not cha… | correct | unit basis: first row of screens[8] |
| l6-const | screens[9].prose | The next lesson builds pointers: `double* p` holds the address of a `double`, and `*p` is the `doub… | correct | [dcl.ptr]: the cv-qualifier after * applies to the pointer; reading right to left gives const pointer to const double |
| l6-const | screens[9].widget.answer | key: ["p", "c2", "star", "cd"] | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].widget.lines.p | step: `p` is: start at the name | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].widget.lines.c2 | step: a `const`: the `const` next to `p` fixes `p` itself | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].widget.lines.star | step: pointer to: the `*` to its left | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].widget.lines.cd | step: a `const double`: the type it points at is read only | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].hints[0] | hint: Start at the name and move left one piece at a time. | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].hints[1] | hint: Directly left of `p` is `const`; left of that is `*`. | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].hints[2] | hint: `p` is a `const` pointer to a `const double`: neither `p` nor `*p` can change. | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].feedback.correct | A `const` pointer to a `const double`. | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].feedback.generic | Not quite right. Begin at `p` and walk left. | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].feedback.byKey.cd | The type pointed at is the last thing you reach, at the far left. | correct | unit basis: first row of screens[9] |
| l6-const | screens[9].explain.text | From the name: `p` is `const`, then `*` makes it a pointer, then `const double` is what it points a… | correct | unit basis: first row of screens[9] |
| l6-const | screens[10].prose | Use the right-to-left reading. A `const` next to the name fixes the pointer; a `const` next to `dou… | correct | [dcl.ptr]/2 examples; run under the app compiler and grader: all four cells compile or fail as keyed, with the quoted 'double *const' text (checks l6.s10) |
| l6-const | screens[10].widget.answer | key: [[], ["No", "Yes"], ["Yes", "No"], ["No", "No"]] | correct | unit basis: first row of screens[10] |
| l6-const | screens[10].hints[0] | hint: Read each declaration from `p` leftwards. | correct | unit basis: first row of screens[10] |
| l6-const | screens[10].hints[1] | hint: `const double* p`: `p` is a pointer to a `const double`. The pointer itself is not `const`. | correct | unit basis: first row of screens[10] |
| l6-const | screens[10].hints[2] | hint: Row 2: No, Yes. Row 3: `p` is a `const` pointer to `double`: Yes, No. Row 4: No, No. | correct | unit basis: first row of screens[10] |
| l6-const | screens[10].feedback.correct | `const` binds to what sits on its left, or to its right when nothing is on its left. | correct | unit basis: first row of screens[10] |
| l6-const | screens[10].feedback.generic | Not quite right. Read each line right to left from `p`. | correct | unit basis: first row of screens[10] |
| l6-const | screens[10].explain.text | `const double* p` is a pointer to read-only values: `*p = 3` fails, `p = &y` is fine. `double* cons… | correct | unit basis: first row of screens[10] |
| l6-const | screens[11].prose | A feed handler calls every strategy for each tick, 2 million times a second. ```cpp struct Tick { s… | correct | [dcl.ref], [dcl.type.cv]: no copy and no write through the reference; lifetime is not extended by a parameter |
| l6-const | screens[11].widget.options[0] | key: No copy per call, and no strategy can change the tick the next one sees | correct | unit basis: first row of screens[11] |
| l6-const | screens[11].widget.options[1].why | wrong option: `const` makes the compiler run strategies in parallel :: `const` says nothing about t… | correct | unit basis: first row of screens[11] |
| l6-const | screens[11].widget.options[2].why | wrong option: `const&` keeps the tick alive after the callback returns :: The feed owns the tick an… | correct | unit basis: first row of screens[11] |
| l6-const | screens[11].widget.options[3].why | wrong option: A plain `Tick&` would copy the tick :: A plain reference copies nothing either. It wo… | correct | unit basis: first row of screens[11] |
| l6-const | screens[11].hints[0] | hint: Two costs matter here: copying, and one strategy breaking another. | correct | unit basis: first row of screens[11] |
| l6-const | screens[11].hints[1] | hint: Each tick goes to many strategies in turn. | correct | unit basis: first row of screens[11] |
| l6-const | screens[11].hints[2] | hint: `&` avoids copying the string and three numbers. `const` stops one strategy editing the tick … | correct | unit basis: first row of screens[11] |
| l6-const | screens[11].feedback.correct | Shared, read only, and cheap. | correct | unit basis: first row of screens[11] |
| l6-const | screens[11].feedback.generic | Not quite right. Think about copies, and about the strategies that read the same tick later. | correct | unit basis: first row of screens[11] |
| l6-const | screens[11].feedback.byKey.plainref | A plain reference avoids the copy too, but any strategy could change the tick for the others. | correct | unit basis: first row of screens[11] |
| l6-const | screens[11].explain.text | `&` means the handler passes its own tick without copying the symbol string. `const` means no strat… | correct | unit basis: first row of screens[11] |
| l6-const | quiz[0].widget.options[0] | key: Both `const int lots = 5;` and `int const lots = 5;` | correct | [dcl.type.cv]: const int and int const are the same type |
| l6-const | quiz[0].widget.options[1].why | wrong option: Only `const int lots = 5;` :: `const` may sit either side of `int`; both lines declar… | correct | unit basis: first row of quiz[0] |
| l6-const | quiz[0].widget.options[2].why | wrong option: Only `int const lots = 5;` :: `const int` and `int const` are the same type, so both … | correct | unit basis: first row of quiz[0] |
| l6-const | quiz[0].feedback.correct | Same type, two spellings. | correct | unit basis: first row of quiz[0] |
| l6-const | quiz[0].feedback.generic | Not quite right. Does the side of `int` that `const` sits on change the type? | correct | unit basis: first row of quiz[0] |
| l6-const | quiz[0].explain.text | For a plain type, `const int` and `int const` mean the same. The position matters only around a `*`… | correct | unit basis: first row of quiz[0] |
| l6-const | quiz[1].widget.options[0] | key: `const Limits limits = load_limits("desk.ini");` | correct | [dcl.constexpr]: a file read at run time is not a constant expression; const fixes it after initialisation |
| l6-const | quiz[1].widget.options[1].why | wrong option: `constexpr Limits limits = load_limits("desk.ini");` :: `constexpr` needs the value w… | correct | unit basis: first row of quiz[1] |
| l6-const | quiz[1].widget.options[2].why | wrong option: `Limits limits = load_limits("desk.ini");` :: That works, but nothing stops a later l… | correct | unit basis: first row of quiz[1] |
| l6-const | quiz[1].feedback.correct | Set once at start-up, then read only. | correct | unit basis: first row of quiz[1] |
| l6-const | quiz[1].feedback.generic | Not quite right. When is the value known, and should it ever change? | correct | unit basis: first row of quiz[1] |
| l6-const | quiz[1].explain.text | The limits are known only when the program runs, so `constexpr` is impossible. `const` fixes them a… | correct | unit basis: first row of quiz[1] |
| l6-const | quiz[2].prose | ```cpp struct Position { int qty; }; void report(const Position& p) { p.qty = 0; } ``` | correct | run under the app compiler and grader: "cannot assign to variable 'p' with const-qualified type 'const Position &'" (check l6.quiz2) |
| l6-const | quiz[2].widget.options[0] | key: It does not compile: `p` is a `const` reference | correct | unit basis: first row of quiz[2] |
| l6-const | quiz[2].widget.options[1].why | wrong option: It compiles and sets the caller's quantity to 0 :: That would need a plain `Position&… | correct | unit basis: first row of quiz[2] |
| l6-const | quiz[2].widget.options[2].why | wrong option: It compiles and changes a local copy :: `const Position&` is not a copy. The compiler… | correct | unit basis: first row of quiz[2] |
| l6-const | quiz[2].feedback.correct | The promise is checked at compile time. | correct | unit basis: first row of quiz[2] |
| l6-const | quiz[2].feedback.generic | Not quite right. What does `const` on the parameter forbid? | correct | unit basis: first row of quiz[2] |
| l6-const | quiz[2].explain.text | clang says "cannot assign to variable 'p' with const-qualified type 'const Position &'". A reportin… | correct | unit basis: first row of quiz[2] |
| l6-const | quiz[3].widget.options[0] | key: Yes: a `const` reference can bind to a temporary | correct | [dcl.init.ref]/5, [class.temporary]/6: a const reference binds a temporary, which lasts to the end of the full expression; run under the app compiler and grader prints 3 (check l6.quiz3) |
| l6-const | quiz[3].widget.options[1].why | wrong option: No: a reference needs a named variable :: That is the rule for a plain `T&`. A `const… | correct | unit basis: first row of quiz[3] |
| l6-const | quiz[3].feedback.correct | `const&` accepts temporaries. | correct | unit basis: first row of quiz[3] |
| l6-const | quiz[3].feedback.generic | Not quite right. Compare a plain `&` with a `const&`. | correct | unit basis: first row of quiz[3] |
| l6-const | quiz[3].explain.text | A `const` reference may bind to a temporary, which then lives until the call ends. That is why `con… | correct | unit basis: first row of quiz[3] |
| l6-const | summary.ideas[0] | `const` is a promise the compiler checks. A `const` variable is never reassigned, and a `const&` pa… | correct | restates s0, s2, s3, s5, s6, s9 |
| l6-const | summary.ideas[1] | A `const` reference accepts variables, `const` objects and temporaries; a `const` object can call o… | correct | unit basis: first row of summary |
| l6-const | summary.ideas[2] | `const` restricts one name, not the object: another name may still change it. `constexpr` also dema… | correct | unit basis: first row of summary |
| l6-const | summary.formula | Reading a declaration: \texttt{const double* const p} \quad\to\quad p \text{ is a const pointer to … | correct | unit basis: first row of summary |
| l6-const | summary.trap | A `const&` view is not a frozen copy: if the object changes through another name, the view sees the… | correct | unit basis: first row of summary |
| l6-const | screens[4].explain.text (last sentence) | A crossed quote is something "a feed handler would flag" | unverified | an industry remark with no source |
| l7-addresses | screens[0].prose | Every object sits at an **address**, a numbered place in memory. `&qty` gives `qty`'s address, and … | correct | [expr.unary.op]: & gives the address, * the object; run under the app compiler and grader prints 500 (check l7 s0) |
| l7-addresses | screens[0].canvas.state.caption | caption: `p`'s box holds `qty`'s address | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].widget.options[0] | key: `500` | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].widget.options[1].why | wrong option: `300` :: You read `*p = 500` as changing `p`. The `*` means the `int` that `p` points… | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].widget.options[2].why | wrong option: `0x1000` :: Printing `qty` prints its value. Its address would be `&qty`. | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].widget.options[3].why | wrong option: It does not compile :: `*p = 500` is the normal way to write through a pointer, so it… | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].hints[0] | hint: What does the `*` in `*p = 500` refer to: the pointer, or what it points at? | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].hints[1] | hint: Follow the dashed arrow from `p`'s box. | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].hints[2] | hint: `*p` is the `int` at the address `p` holds, which is `qty`. Writing 500 there changes `qty`. | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].feedback.correct | `*p` is `qty`. | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].feedback.generic | Not quite right. Follow the arrow: which box does `*p` reach? | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].feedback.byKey.three | You read `*p = 500` as changing `p`. The `*` reaches the `int` that `p` points at, which is `qty`. | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[0].explain.text | `p` holds `qty`'s address, so `*p` reaches `qty` itself. Writing 500 through `*p` changes `qty`. `p… | correct | unit basis: first row of screens[0] |
| l7-addresses | screens[1].prose | A pointer can hold the address of a vector element. Adding a whole number moves it along the elemen… | correct | [expr.add]/4: p + 2 points two elements on, px[3] |
| l7-addresses | screens[1].canvas.state.caption | caption: `p` points at `px[1]` | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[1].widget.answer | key: ["c3"] | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[1].hints[0] | hint: Where does `p` start? | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[1].hints[1] | hint: `p` starts at index 1. | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[1].hints[2] | hint: `p + 2` is two elements on from index 1, which is index 3. `*` reads the price there. | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[1].feedback.correct | Two elements on from `px[1]` is `px[3]`. | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[1].feedback.generic | Not quite right. Start from where `p` points, not from the front. | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[1].feedback.byKey.c2 | That is `*(p + 1)`. Move two elements from `px[1]`. | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[1].feedback.byKey.c1 | That is `*p` itself. `p + 2` moves two elements on. | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[1].feedback.byKey.c0 | `p` starts at `px[1]`, not `px[0]`. Count two on from there. | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[1].explain.text | `p` points at `px[1]`, so `p + 2` points at `px[3]`, and `*(p + 2)` reads 102.00. Pointer arithmeti… | correct | unit basis: first row of screens[1] |
| l7-addresses | screens[2].prose | `&x` is the **address of** `x`. `double* p` is a **pointer**: a variable holding an address. `*p` *… | correct | [expr.add]: the step is sizeof(double) = 8 bytes; 0x1008 + 16 = 0x1018; slips 2, 8 and 24 = 0x1018 - 0x1000 |
| l7-addresses | screens[2].canvas.state.caption | caption: `p` holds 0x1008, the address of `px[1]` | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].widget.answer | key: 16 (How many bytes past `p`'s address is the address `p + 2` holds?) | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].widget.accept | accept: 16 bytes: 2 elements of 8 bytes each, so 0x1008 + 16 = 0x1018. | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].widget.wrong[0] | slip: 2 (two) | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].widget.wrong[1] | slip: 8 (eight) | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].widget.wrong[2] | slip: 24 (twentyfour) | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].hints[0] | hint: `p + 2` moves two elements. How big is one element? | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].hints[1] | hint: `px[1]` and `px[3]` are two steps apart on the line. | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].hints[2] | hint: Each `double` is 8 bytes, so two elements are 16 bytes: 0x1008 + 16 = 0x1018. | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].feedback.correct | `p + 2` moves 2 × 8 bytes. | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].feedback.generic | Not quite right. Multiply the elements moved by the size of one `double`. | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].feedback.byKey.two | You counted elements. The address moves by 2 elements times 8 bytes. | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].feedback.byKey.eight | That is one element, `p + 1`. | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].feedback.byKey.twentyfour | That is the distance from `px[0]`. Measure from `p`, which starts at `px[1]`. | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[2].explain.text | `p + 2` moves two whole `double`s, and each is 8 bytes, so the address grows by 16: from 0x1008 to … | correct | unit basis: first row of screens[2] |
| l7-addresses | screens[3].prose | `nullptr` is the pointer that points at nothing. Reading or writing through it is **undefined behav… | correct | [expr.unary.op], [basic.compound]: indirection through null is undefined; run under the app compiler and grader: solution passes, no guard fails test 5 (check l7.s3) |
| l7-addresses | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l7-addresses | screens[3].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[3] |
| l7-addresses | screens[3].hints[0] | hint: Two steps: guard against `nullptr`, then write through `p`. | correct | unit basis: first row of screens[3] |
| l7-addresses | screens[3].hints[1] | hint: `*p += 1;` changes the `int` that `p` points at. `p += 1` would move the pointer instead. | correct | unit basis: first row of screens[3] |
| l7-addresses | screens[3].hints[2] | hint: `if (p == nullptr) return;` then `*p += 1;`. | correct | unit basis: first row of screens[3] |
| l7-addresses | screens[3].feedback.correct | Guard, then write through the pointer. | correct | unit basis: first row of screens[3] |
| l7-addresses | screens[3].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of screens[3] |
| l7-addresses | screens[3].feedback.byKey.test-5 | The `nullptr` test failed: the code wrote through a null pointer. Return before `*p` when `p == nul… | correct | unit basis: first row of screens[3] |
| l7-addresses | screens[3].explain.text | `*p += 1` changes the `int` at the address `p` holds, so the caller's `fills` becomes 8. The guard … | imprecise | RUN: bump(nullptr), the call on the canvas and in test 5, stopped (trap, or exit status 3 in the grader); only a pointer the compiler cannot see is null wrote quietly (NOTE checks). Finding 2 |
| l7-addresses | screens[4].prose | A range can be passed as two pointers: `begin` at the first element, and `end` one *past* the last.… | correct | half-open range [begin, end): [iterator.requirements]; run under the app compiler and grader: solution passes; best from 0 gives 0 on test 2, reading *end gave another number (checks l7.s4) |
| l7-addresses | screens[4].canvas.state.caption | caption: `end` points one past the last price | correct | unit basis: first row of screens[4] |
| l7-addresses | screens[4].widget | code: 6 tests; solution passes, starter fails | correct | unit basis: first row of screens[4] |
| l7-addresses | screens[4].hints[0] | hint: Start the best value at `*begin`, not at 0: prices can be negative returns. | correct | unit basis: first row of screens[4] |
| l7-addresses | screens[4].hints[1] | hint: A loop `for (const double* p = begin; p != end; ++p)` visits each element once. | correct | unit basis: first row of screens[4] |
| l7-addresses | screens[4].hints[2] | hint: Return 0 if `begin == end`. Otherwise set `best = *begin`, then for each `p` after it, keep `… | correct | unit basis: first row of screens[4] |
| l7-addresses | screens[4].feedback.correct | `p != end` stops exactly at the last element. | correct | unit basis: first row of screens[4] |
| l7-addresses | screens[4].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of screens[4] |
| l7-addresses | screens[4].feedback.byKey.test-2 | All three values are negative. If you got 0, your best started at 0: start from `*begin`. If you go… | correct | unit basis: first row of screens[4] |
| l7-addresses | screens[4].feedback.byKey.test-5 | Test 5 passes the range `xs + 1` to `xs + 3`: the values 1 and 4, so the answer is 4. | correct | unit basis: first row of screens[4] |
| l7-addresses | screens[4].explain.text | `++p` moves one `double` on, and `p != end` stops before the address one past the last. Starting `b… | correct | unit basis: first row of screens[4] |
| l7-addresses | screens[5].prose | `bid` lives inside the inner braces. In this browser the program printed `101.25`. ```cpp double* p… | correct | [basic.life]: use after the block ends is undefined; run under the app compiler and grader: the app build printed 101.25 (check l7.s5) |
| l7-addresses | screens[5].canvas.state.caption | caption: Inside the braces: `p` points at `bid` | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].widget.options[0] | key: No: `bid` ended at `}`, so `*p` reads a dead object, which is undefined behaviour | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].widget.options[1].why | wrong option: Yes: it printed the right price :: That is the trap. The read is undefined: it may pr… | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].widget.options[2].why | wrong option: Yes: `p` keeps `bid` alive :: A pointer only holds an address. It does not keep the o… | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].widget.options[3].why | wrong option: No: it does not compile :: It compiles cleanly. The compiler cannot always see that `… | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].hints[0] | hint: When does `bid` stop existing? | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].hints[1] | hint: `bid` is declared inside `{ }`. Its life ends at the `}`. | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].hints[2] | hint: After the `}`, `p` holds the address of a dead `double`. Reading it is undefined, whatever it… | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].feedback.correct | A right answer from undefined behaviour is luck. | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].feedback.generic | Not quite right. Check whether `bid` still exists when `*p` runs. | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].feedback.byKey.fine | That is the trap. The read is undefined; the browser build just left 101.25 in that memory. A desk … | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].feedback.byKey.alive | A pointer does not keep its target alive. `bid` ended at its closing brace. | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].explain.text | `bid` ends at the inner `}`, and `p` is left **dangling**. Undefined behaviour means the compiler m… | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[5].explain.canvas.caption | caption: After the braces: `p` dangles | correct | unit basis: first row of screens[5] |
| l7-addresses | screens[6].prose | The same code saved as `scope.cpp` and built on Linux with g++ and AddressSanitizer, which watches … | correct | run, g++ 13.3 with -fsanitize=address: stack-use-after-scope, READ of size 8, 'bid' (line 5), scope.cpp:8 (check l7.s6) |
| l7-addresses | screens[6].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[6].widget.answer | key: ["l8"] | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[6].hints[0] | hint: One line quotes a variable name in single quotes. | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[6].hints[1] | hint: The frame lists its objects; one of them is where the read landed. | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[6].hints[2] | hint: `[32, 40) 'bid' (line 5)` is the 8 bytes of `bid`, declared on line 5, and the arrow says the… | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[6].feedback.correct | `bid`, declared on line 5. | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[6].feedback.generic | Not quite right. Find the line naming a variable in quotes. | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[6].feedback.byKey.l5 | That line says *where in the code* the read happened, line 8. The variable is named further down. | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[6].feedback.byKey.l4 | `READ of size 8` says a `double` was read. Which variable's memory was it? | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[6].feedback.byKey.l3 | That names the kind of error. The variable is named further down. | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[6].explain.text | `'bid' (line 5)` names the variable, and `scope.cpp:8` names the read. `READ of size 8` is one `dou… | correct | unit basis: first row of screens[6] |
| l7-addresses | screens[7].prose | What you used, in one place: ```cpp int* p = &x; // p holds x's address *p = 5; // write x through … | correct | [expr.eq]: pointers to different objects compare unequal; run under the app compiler and grader prints 0 (check l7 s7) |
| l7-addresses | screens[7].widget.options[0] | key: `0` | correct | unit basis: first row of screens[7] |
| l7-addresses | screens[7].widget.options[1].why | wrong option: `1` :: You compared the values. `&a == &b` compares addresses, and two variables neve… | correct | unit basis: first row of screens[7] |
| l7-addresses | screens[7].feedback.correct | Two variables, two addresses. | correct | unit basis: first row of screens[7] |
| l7-addresses | screens[7].feedback.generic | Not quite right. What does `==` compare when both sides are addresses? | correct | unit basis: first row of screens[7] |
| l7-addresses | screens[7].explain.text | `&a` and `&b` are two different addresses, so they compare unequal and `std::cout` prints 0 for `fa… | correct | unit basis: first row of screens[7] |
| l7-addresses | screens[8].prose | `px` starts at 0x1000, with 8-byte `double`s, and `p = &px[1]`. Each line below gives one step and … | correct | 0x1000 + 8 = 0x1008; + 16 = 0x1018 = 0x1000 + 3 x 8 |
| l7-addresses | screens[8].widget.answer | key: ["s1", "s2", "s3", "s4"] | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[8].widget.lines.s1 | step: `p` holds 0x1008: `px[1]` is one `double` past 0x1000 | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[8].widget.lines.s2 | step: `p + 2` holds 0x1008 + 2 × 8 = 0x1018: arithmetic counts whole `double`s | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[8].widget.lines.s3 | step: 0x1018 = 0x1000 + 3 × 8, so it is the address of `px[3]` | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[8].widget.lines.s4 | step: `*(p + 2)` reads the `double` at 0x1018: `px[3]`, which is 102.00 | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[8].hints[0] | hint: Start with what `p` holds. | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[8].hints[1] | hint: Add before you dereference. | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[8].hints[2] | hint: Address of `p`, then the address `p + 2`, then which element sits there, then read it. | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[8].feedback.correct | Address, step, element, read. | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[8].feedback.generic | Not quite right. You need an address before you can move it, and you move it before you read. | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[8].explain.text | `p` starts at 0x1008. Moving 2 elements adds 16 bytes, giving 0x1018, which is `px[3]`'s address. O… | correct | unit basis: first row of screens[8] |
| l7-addresses | screens[9].prose | An exchange SDK written in C calls you with a pointer to the first of `n` book levels. `p->size` me… | correct | [expr.add], [expr.ref]: p->size is (*p).size; sizeof(Level) is 16 on both targets; reading one past the end is undefined |
| l7-addresses | screens[9].widget.options[0] | key: `for (const Level* p = levels; p != levels + n; ++p) total += p->size;` | correct | unit basis: first row of screens[9] |
| l7-addresses | screens[9].widget.options[1].why | wrong option: `for (const Level* p = levels; p <= levels + n; ++p) total += p->size;` :: `<=` also … | correct | unit basis: first row of screens[9] |
| l7-addresses | screens[9].widget.options[2].why | wrong option: `for (int i = 0; i < n; ++i) total += levels->size;` :: `levels` never moves, so this… | correct | unit basis: first row of screens[9] |
| l7-addresses | screens[9].widget.options[3].why | wrong option: `for (const Level* p = levels; p != levels + n; p += sizeof(Level)) total += p->size;… | correct | unit basis: first row of screens[9] |
| l7-addresses | screens[9].hints[0] | hint: Which pointer moves, by how much, and where must it stop? | correct | unit basis: first row of screens[9] |
| l7-addresses | screens[9].hints[1] | hint: `levels + n` is one past the last level, like `end`. | correct | unit basis: first row of screens[9] |
| l7-addresses | screens[9].hints[2] | hint: Start at `levels`, step with `++p`, stop when `p == levels + n`. Read `p->size` each time. | correct | unit basis: first row of screens[9] |
| l7-addresses | screens[9].feedback.correct | One past the end, never read. | correct | unit basis: first row of screens[9] |
| l7-addresses | screens[9].feedback.generic | Not quite right. Check where each loop starts, how it steps, and where it stops. | correct | unit basis: first row of screens[9] |
| l7-addresses | screens[9].feedback.byKey.bytes | Pointer arithmetic already scales by the size of `Level`. Adding `sizeof(Level)` jumps 16 levels at… | correct | unit basis: first row of screens[9] |
| l7-addresses | screens[9].explain.text | `++p` moves one `Level` (16 bytes), and `p != levels + n` stops before the address one past the las… | correct | unit basis: first row of screens[9] |
| l7-addresses | quiz[0].prose | ```cpp int* p = nullptr; std::cout << *p << "\n"; ``` | correct | undefined; run: g++ build exits on SIGSEGV, ASan says "SEGV on unknown address 0x000000000000", the app build printed 0 (checks l7.quiz0) |
| l7-addresses | quiz[0].widget.options[0] | key: Undefined behaviour: a desk build usually stops with `Segmentation fault` | correct | unit basis: first row of quiz[0] |
| l7-addresses | quiz[0].widget.options[1].why | wrong option: It prints 0, the value of a null pointer :: `*p` reads the `int` at address 0, not th… | correct | unit basis: first row of quiz[0] |
| l7-addresses | quiz[0].widget.options[2].why | wrong option: It does not compile :: It compiles. The compiler does not track which pointers are nu… | correct | unit basis: first row of quiz[0] |
| l7-addresses | quiz[0].feedback.correct | Never dereference `nullptr`. | correct | unit basis: first row of quiz[0] |
| l7-addresses | quiz[0].feedback.generic | Not quite right. What does `*p` read when `p` points at nothing? | correct | unit basis: first row of quiz[0] |
| l7-addresses | quiz[0].explain.text | On Linux, g++'s build dies with `Segmentation fault` (AddressSanitizer: "SEGV on unknown address 0x… | correct | unit basis: first row of quiz[0] |
| l7-addresses | quiz[1].prose | ```cpp int x = 1; int* p = &x; int** pp = &p; **pp = 7; std::cout << x << "\n"; ``` | correct | two indirections reach x; run under the app compiler and grader prints 7 (check l7 quiz1) |
| l7-addresses | quiz[1].widget.options[0] | key: `7` | correct | unit basis: first row of quiz[1] |
| l7-addresses | quiz[1].widget.options[1].why | wrong option: `1` :: `**pp` follows two arrows: `pp` to `p`, then `p` to `x`. Writing 7 there chang… | correct | unit basis: first row of quiz[1] |
| l7-addresses | quiz[1].widget.options[2].why | wrong option: It does not compile :: `int** pp = &p;` is a pointer to a pointer. It compiles. | correct | unit basis: first row of quiz[1] |
| l7-addresses | quiz[1].feedback.correct | Two hops, from `pp` to `p` to `x`. | correct | unit basis: first row of quiz[1] |
| l7-addresses | quiz[1].feedback.generic | Not quite right. Follow `pp`, then follow what you find. | correct | unit basis: first row of quiz[1] |
| l7-addresses | quiz[1].explain.text | `pp` holds `p`'s address, so `*pp` is `p`, and `**pp` is what `p` points at: `x`. Writing 7 through… | correct | unit basis: first row of quiz[1] |
| l7-addresses | quiz[2].prose | ```cpp double* best_bid() { double x = 101.25; return &x; } ``` | correct | run under the app compiler and grader: builds with "address of stack memory associated with local variable 'x' returned" (check l7.quiz2) |
| l7-addresses | quiz[2].widget.options[0] | key: It compiles with a warning; the returned pointer dangles | correct | unit basis: first row of quiz[2] |
| l7-addresses | quiz[2].widget.options[1].why | wrong option: It refuses to compile :: clang only warns: "address of stack memory associated with l… | correct | unit basis: first row of quiz[2] |
| l7-addresses | quiz[2].widget.options[2].why | wrong option: It compiles silently, and the pointer is safe :: `x` ends when the function returns, … | correct | unit basis: first row of quiz[2] |
| l7-addresses | quiz[2].feedback.correct | A warning, not an error: read your warnings. | correct | unit basis: first row of quiz[2] |
| l7-addresses | quiz[2].feedback.generic | Not quite right. When does `x` stop existing? | correct | unit basis: first row of quiz[2] |
| l7-addresses | quiz[2].explain.text | `x` lives in `best_bid`'s frame and ends at its `}`. clang warns "address of stack memory associate… | correct | unit basis: first row of quiz[2] |
| l7-addresses | quiz[3].widget.options[0] | key: 0x200C | correct | 0x2000 + 3 x 4 = 0x200C |
| l7-addresses | quiz[3].widget.options[1].why | wrong option: 0x2003 :: You added 3 bytes. `p + 3` moves 3 whole `int`s: 3 × 4 = 12 bytes, which is… | correct | unit basis: first row of quiz[3] |
| l7-addresses | quiz[3].widget.options[2].why | wrong option: 0x2018 :: You used 8 bytes per element, the size of a `double`. An `int` here is 4. | correct | unit basis: first row of quiz[3] |
| l7-addresses | quiz[3].feedback.correct | 3 × 4 = 12 bytes, 0xC in hex. | correct | unit basis: first row of quiz[3] |
| l7-addresses | quiz[3].feedback.generic | Not quite right. Multiply 3 by the size of an `int`. | correct | unit basis: first row of quiz[3] |
| l7-addresses | quiz[3].explain.text | Pointer arithmetic scales by the type: `p + 3` moves 3 × 4 = 12 bytes. 12 is C in hex, so the addre… | correct | unit basis: first row of quiz[3] |
| l7-addresses | summary.ideas[0] | `&x` is `x`'s address; a pointer `T* p` holds one, and `*p` reaches the object there. `p + k` moves… | correct | restates s0 to s6 |
| l7-addresses | summary.ideas[1] | `nullptr` points at nothing. Reading through it, or through a pointer to an object that has ended, … | correct | unit basis: first row of summary |
| l7-addresses | summary.ideas[2] | This browser build is forgiving: null reads and dangling reads often print stale numbers. A desk bu… | correct | unit basis: first row of summary |
| l7-addresses | summary.formula | Pointer arithmetic: \text{address}(p + k) = \text{address}(p) + k \times \texttt{sizeof(T)} :: A ra… | correct | unit basis: first row of summary |
| l7-addresses | summary.trap | A program that prints the right number can still read a dead object. Undefined behaviour is not a c… | correct | unit basis: first row of summary |
| l8-stack-and-heap | screens[0].prose | Two programs store two million prices, 16 MB. The locals of every running function share one fixed … | correct | run under the app compiler and grader: A stops with "memory access out of bounds", B prints 101 and its vector object is 12 bytes; g++ A dies on SIGSEGV (checks l8.s0); 8 MB: the app's -z stack-size=8388608 and Linux `ulimit -s` 8192 |
| l8-stack-and-heap | screens[0].canvas.state.caption | caption: Locals get 8 MB in total, here and on a typical Linux desk | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].widget.options[0] | key: A only | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].widget.options[1].why | wrong option: Both: 16 MB does not fit in 8 MB :: B's vector keeps its two million `double`s somewh… | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].widget.options[2].why | wrong option: B only :: A's array is a local, all 16 MB of it, so A is the one that does not fit. | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].widget.options[3].why | wrong option: Neither :: A asks for 16 MB of locals in an 8 MB region, so it runs off the end. | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].hints[0] | hint: Where does each program put the two million `double`s? | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].hints[1] | hint: A's array is itself a local. B's local is a `std::vector`, which holds a pointer to its eleme… | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].hints[2] | hint: A needs 16 MB of locals and has 8 MB: it crashes. B's elements live elsewhere, so B runs. | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].feedback.correct | Only the array is a 16 MB local. | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].feedback.generic | Not quite right. Ask which program makes the 16 MB a local variable. | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].feedback.byKey.both | B's elements are not locals. The vector object is small; it points at its elements elsewhere. | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[0].explain.text | A's array is a local, so all 16 MB must fit in the 8 MB for locals. It overflows: this browser repo… | correct | unit basis: first row of screens[0] |
| l8-stack-and-heap | screens[1].prose | Each call gets a **frame** holding its locals and parameters. Step through the program. ```cpp doub… | correct | call stack model (Stroustrup, TC++PL4 6.4.2); mid returns 100, value 30000; run under the app compiler and grader (check l8.s1/s2) |
| l8-stack-and-heap | screens[1].canvas.state.caption | caption: 1 frame | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].widget.answer | key: "s5" | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].widget.states.s0.ops[0].why | wrong step: `main` prints `v` :: `v` comes from `value`, so `main` must call `value` first. | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].widget.states.s1.ops[0].why | wrong step: `value` returns :: `value` needs `m`, so it must call `mid` first. | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].widget.states.s2.ops[0].why | wrong step: `value` returns :: Only the frame on top can finish, and `mid` is on top. | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].widget.states.s3.ops[0].why | wrong step: `mid` returns again :: `mid`'s frame, with its `bid` and `ask`, was removed when it ret… | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].widget.states.s4.ops[1].why | wrong step: `value` returns again :: `value` has finished; its frame and its `m` are gone. | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].hints[0] | hint: A call adds a frame on top; a return removes the top frame. | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].hints[1] | hint: Only the frame on top can finish. | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].hints[2] | hint: `main` calls `value`, `value` calls `mid`. Then `mid` returns, `value` returns, and `main` pr… | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].feedback.correct | Last in, first out. | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].feedback.generic | Not quite right. Only the frame on top can return. | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].explain.text | Frames pile up as calls start and come off the top as they return. When `mid` returned, its `bid` a… | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[1].explain.canvas.caption | caption: No frames left | correct | unit basis: first row of screens[1] |
| l8-stack-and-heap | screens[2].prose | The pile of frames is the **stack**. `new` puts an object on the **heap** instead, where it stays u… | correct | [basic.stc.dynamic]: an object from new lasts until delete; run under the app compiler and grader prints 101.5 (check l8.s1/s2) |
| l8-stack-and-heap | screens[2].canvas.state.caption | caption: `p` in `make_price`'s frame, `q` in `main`'s; the `double` on the heap | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].widget.options[0] | key: Yes: the `double` is on the heap and lives until `delete q` | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].widget.options[1].why | wrong option: No: it died when `make_price` returned :: That is true of locals. Only `p` was a loca… | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].widget.options[2].why | wrong option: No: `q` is a copy of `p`, so it points somewhere else :: Copying a pointer copies the… | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].hints[0] | hint: Which objects live in `make_price`'s frame, and which does `new` create? | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].hints[1] | hint: `p` is in the frame; the `double` is on the heap. | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].hints[2] | hint: When `make_price` returns, `p` dies. The heap `double` stays, and `q` holds its address until… | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].feedback.correct | Heap objects live until `delete`. | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].feedback.generic | Not quite right. Separate the pointer `p` from the `double` it points at. | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].feedback.byKey.dies | Only `p` lived in the frame. The `double` came from `new`, so it is on the heap. | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].explain.text | `p` lived in `make_price`'s frame and died at its `}`, but it had already handed its address to `q`… | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[2].explain.canvas.caption | caption: After the call: `p` is gone, the heap `double` is not | correct | unit basis: first row of screens[2] |
| l8-stack-and-heap | screens[3].prose | A local lives on the stack, even when it is a pointer or a vector. What `new` makes, and what a vec… | correct | automatic against dynamic storage: [basic.stc]; vector elements are allocated by its allocator: [vector.overview]; 12 and 24 bytes measured (checks l8.s0) |
| l8-stack-and-heap | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l8-stack-and-heap | screens[3].widget.answer | key: [["stack"], ["stack"], ["heap"], ["stack"], ["heap"]] | correct | unit basis: first row of screens[3] |
| l8-stack-and-heap | screens[3].hints[0] | hint: Every variable declared inside `main` is a local. What do the pointer and the vector point at? | correct | unit basis: first row of screens[3] |
| l8-stack-and-heap | screens[3].hints[1] | hint: `buf` holds an address; `new double[n]` made what it points at. | correct | unit basis: first row of screens[3] |
| l8-stack-and-heap | screens[3].hints[2] | hint: `n`, `buf` and `prices` are locals: stack. `buf[0]` came from `new[]`, and `prices[0]` is ins… | correct | unit basis: first row of screens[3] |
| l8-stack-and-heap | screens[3].feedback.correct | The handles are on the stack; the data is on the heap. | correct | unit basis: first row of screens[3] |
| l8-stack-and-heap | screens[3].feedback.generic | Not quite right. Separate each local from what it points at. | correct | unit basis: first row of screens[3] |
| l8-stack-and-heap | screens[3].explain.text | `n`, the pointer `buf` and the vector object `prices` are locals in `main`'s frame. The 1,000 `doub… | correct | unit basis: first row of screens[3] |
| l8-stack-and-heap | screens[4].prose | A **leak** is a `new` with no `delete`: the memory stays taken until the program ends. LeakSanitize… | correct | run, g++ with -fsanitize=address: the report lines as shown, 8000 bytes in 1 object, sum_prices at leak.cpp:2 (check l8.s4); 2,500 x 8,000 = 20,000,000 bytes; slips 0.008, 20,000,000 and 2.5 |
| l8-stack-and-heap | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].widget.answer | key: 20 (A backtest calls `sum_prices(1000)` once a day for 2,500 trading days. How many MB leak? T… | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].widget.accept | accept: 20 MB: 2,500 calls × 8,000 bytes = 20,000,000 bytes. | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].widget.wrong[0] | slip: 0.008 (one) | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].widget.wrong[1] | slip: 20000000 (bytes) | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].widget.wrong[2] | slip: 2.5 (noeight) | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].hints[0] | hint: How many bytes does one call leak? | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].hints[1] | hint: Line 3 of the report gives one call's leak. | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].hints[2] | hint: Each call leaks 1,000 × 8 = 8,000 bytes. Times 2,500 calls is 20,000,000 bytes, or 20 MB. | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].feedback.correct | 8,000 bytes a day, 20 MB in all. | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].feedback.generic | Not quite right. Multiply one call's leak by the number of calls. | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].feedback.byKey.one | That is one call. The backtest calls it 2,500 times. | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].feedback.byKey.bytes | That is the count in bytes. Divide by 1,000,000. | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].feedback.byKey.noeight | You counted one byte per price. Each `double` is 8 bytes. | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[4].explain.text | Each call leaks one `new double[1000]`, 8,000 bytes, and line 5 of the report names `sum_prices` at… | correct | unit basis: first row of screens[4] |
| l8-stack-and-heap | screens[5].prose | A colleague frees an array of prices. In this browser the program runs, prints nothing odd, and exi… | correct | [expr.delete]/2: delete on a new[] pointer is undefined; run under the app compiler and grader: runs, exit 0, with the quoted clang warning; ASan: alloc-dealloc-mismatch (checks l8.s5) |
| l8-stack-and-heap | screens[5].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].widget.options[0] | key: `new[]` must be paired with `delete[]`; plain `delete` is undefined behaviour | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].widget.options[1].why | wrong option: Nothing: the program ran and exited with 0 :: This browser build is forgiving. Pairin… | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].widget.options[2].why | wrong option: It frees only the first 8 bytes and leaks the rest :: It is not a tidy partial free. … | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].widget.options[3].why | wrong option: It should be `free(px)` :: `free` pairs with `malloc`, not with `new[]`. Mixing them … | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].hints[0] | hint: How was `px` allocated? | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].hints[1] | hint: `new double[1000]` has brackets. | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].hints[2] | hint: Every `new` pairs with `delete`, and every `new[]` with `delete[]`. Mixing them is undefined. | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].feedback.correct | `new[]` goes with `delete[]`. | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].feedback.generic | Not quite right. Match the form of `delete` to the form of `new`. | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].feedback.byKey.nothing | This browser build is forgiving. A desk build with `-fsanitize=address` reports "alloc-dealloc-mism… | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].explain.text | `new[]` must be freed with `delete[]`. clang warns at compile time, and a desk build with AddressSa… | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[5].explain.canvas.lines | canvas: main.cpp:3:1: warning: 'delete' applied to a pointer / that was allocated with 'new[]'; / d… | correct | unit basis: first row of screens[5] |
| l8-stack-and-heap | screens[6].prose | Finish the program. It reads `n`, then `n` prices into a heap buffer, prints their sum to 2 decimal… | correct | run under the app compiler and grader: solution passes; `delete px` gives the right output and fails test 1 with the leak checker's status 1 (check l8.s6); [expr.new]/8: a zero-length array is allowed |
| l8-stack-and-heap | screens[6].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[6] |
| l8-stack-and-heap | screens[6].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[6] |
| l8-stack-and-heap | screens[6].hints[0] | hint: Two loops, or one: read each `px[i]`, then add them up. | correct | unit basis: first row of screens[6] |
| l8-stack-and-heap | screens[6].hints[1] | hint: `std::cout << std::fixed << std::setprecision(2)` prints two decimals. | correct | unit basis: first row of screens[6] |
| l8-stack-and-heap | screens[6].hints[2] | hint: Read with `for (int i = 0; i < n; ++i) std::cin >> px[i];`, sum into `total`, print it, and f… | correct | unit basis: first row of screens[6] |
| l8-stack-and-heap | screens[6].feedback.correct | Read, sum, print, `delete[]`. | correct | unit basis: first row of screens[6] |
| l8-stack-and-heap | screens[6].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of screens[6] |
| l8-stack-and-heap | screens[6].feedback.byKey.test-1 | If the output is right but the test failed with status 1, the leak checker fired. `new[]` needs `de… | correct | unit basis: first row of screens[6] |
| l8-stack-and-heap | screens[6].explain.text | The buffer from `new double[n]` lives on the heap until `delete[] px`. With `n` = 0 the loops never… | correct | unit basis: first row of screens[6] |
| l8-stack-and-heap | screens[7].prose | Say a market-data feed has a C interface: you hand over a buffer and the feed fills it. `fill_ticks… | correct | run under the app compiler and grader: solution passes, starter fails; [vector.cons] iterator-range constructor copies |
| l8-stack-and-heap | screens[7].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[7] |
| l8-stack-and-heap | screens[7].widget | code: 5 tests; solution passes, starter fails | correct | unit basis: first row of screens[7] |
| l8-stack-and-heap | screens[7].hints[0] | hint: Allocate, fill, copy, free, return: in that order. | correct | unit basis: first row of screens[7] |
| l8-stack-and-heap | screens[7].hints[1] | hint: Free the buffer after copying it into the vector, never before. | correct | unit basis: first row of screens[7] |
| l8-stack-and-heap | screens[7].hints[2] | hint: `double* buf = new double[n]; fill_ticks(buf, n); std::vector<double> out(buf, buf + n); dele… | correct | unit basis: first row of screens[7] |
| l8-stack-and-heap | screens[7].feedback.correct | The vector owns a copy; the buffer is freed. | correct | unit basis: first row of screens[7] |
| l8-stack-and-heap | screens[7].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of screens[7] |
| l8-stack-and-heap | screens[7].explain.text | The vector copies the `n` prices into its own heap buffer, so the `new[]` buffer can be freed befor… | correct | unit basis: first row of screens[7] |
| l8-stack-and-heap | screens[8].prose | The lifetimes you saw: ```cpp void f(int n) { double x = 1.0; // stack: dies at } double* p = new d… | correct | run under the app compiler and grader: a 10,000,000-deep recursion stops with "call stack exhausted" (check l8.s8) |
| l8-stack-and-heap | screens[8].widget.options[0] | key: The stack: every call still waiting holds a frame | correct | unit basis: first row of screens[8] |
| l8-stack-and-heap | screens[8].widget.options[1].why | wrong option: The heap :: Frames are not on the heap. The heap is for `new` and for containers' ele… | correct | unit basis: first row of screens[8] |
| l8-stack-and-heap | screens[8].widget.options[2].why | wrong option: Time: it ran too long :: Each frame takes stack space, and 10 million waiting frames … | correct | unit basis: first row of screens[8] |
| l8-stack-and-heap | screens[8].feedback.correct | Deep recursion overflows the stack. | correct | unit basis: first row of screens[8] |
| l8-stack-and-heap | screens[8].feedback.generic | Not quite right. Where does each waiting call keep its frame? | correct | unit basis: first row of screens[8] |
| l8-stack-and-heap | screens[8].explain.text | Each call that has not returned keeps a frame on the stack. Ten million of them need far more than … | correct | unit basis: first row of screens[8] |
| l8-stack-and-heap | screens[9].prose | Back to `make_price` and `main`, where `main` does `double* q = make_price();`, reads `*q`, then ca… | correct | order follows s1 and s2 |
| l8-stack-and-heap | screens[9].widget.answer | key: ["e1", "e2", "e3", "e4", "e5"] | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].widget.lines.e1 | step: `main`'s frame is pushed: the program starts | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].widget.lines.e2 | step: `make_price`'s frame is pushed on top: `main` called it | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].widget.lines.e3 | step: `new` puts 101.5 on the heap; `p` in the top frame holds its address | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].widget.lines.e4 | step: `make_price`'s frame and `p` are popped; the heap `double` stays | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].widget.lines.e5 | step: `delete q` frees the heap `double`: `q` now dangles | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].hints[0] | hint: Frames come and go with calls; heap objects come and go with `new` and `delete`. | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].hints[1] | hint: The heap object is created inside `make_price`, and outlives it. | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].hints[2] | hint: Push `main`, push `make_price`, `new`, pop `make_price`, then `delete` in `main`. | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].feedback.correct | The heap object outlives the frame that made it. | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].feedback.generic | Not quite right. A frame must exist before code inside it runs `new`. | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[9].explain.text | The `double` is created while `make_price`'s frame is on top, survives that frame's pop, and ends o… | correct | unit basis: first row of screens[9] |
| l8-stack-and-heap | screens[10].prose | A binomial pricer needs `steps + 1` doubles of scratch space per price. A volatility calibration pr… | correct | one allocation reused against 50,000 allocations (derivation); an array bound must be a constant expression: [dcl.array] |
| l8-stack-and-heap | screens[10].widget.options[0] | key: Hold a `std::vector<double>` member, sized once to `steps + 1` and reused for every price | correct | unit basis: first row of screens[10] |
| l8-stack-and-heap | screens[10].widget.options[1].why | wrong option: `new double[steps + 1]` and `delete[]` inside every call :: That works, but it pays f… | correct | unit basis: first row of screens[10] |
| l8-stack-and-heap | screens[10].widget.options[2].why | wrong option: A local array `double v[steps + 1]` :: In standard C++ an array's size must be known … | correct | unit basis: first row of screens[10] |
| l8-stack-and-heap | screens[10].widget.options[3].why | wrong option: `new` once at start-up and never `delete` :: It runs, but nothing owns the memory or … | correct | unit basis: first row of screens[10] |
| l8-stack-and-heap | screens[10].hints[0] | hint: The size is the same for every price. Why allocate it 50,000 times? | correct | unit basis: first row of screens[10] |
| l8-stack-and-heap | screens[10].hints[1] | hint: A member lives as long as the pricer object. | correct | unit basis: first row of screens[10] |
| l8-stack-and-heap | screens[10].hints[2] | hint: Size a vector once, then reuse its elements: one allocation, freed automatically when the pri… | correct | unit basis: first row of screens[10] |
| l8-stack-and-heap | screens[10].feedback.correct | Allocate once, reuse, free automatically. | correct | unit basis: first row of screens[10] |
| l8-stack-and-heap | screens[10].feedback.generic | Not quite right. Count the allocations each design makes, and ask who frees them. | correct | unit basis: first row of screens[10] |
| l8-stack-and-heap | screens[10].explain.text | A vector member is allocated once, reused for all 50,000 prices, and freed when the pricer is destr… | correct | unit basis: first row of screens[10] |
| l8-stack-and-heap | quiz[0].prose | ```cpp double price = 101.25; double* p = &price; delete p; ``` | correct | [expr.delete]/2: undefined; run: g++ warns "called on unallocated object 'price'" and the run aborts with "free(): invalid pointer"; the app build ran it silently (checks l8.quiz0) |
| l8-stack-and-heap | quiz[0].widget.options[0] | key: `price` is on the stack; `delete` is only for addresses `new` returned | correct | unit basis: first row of quiz[0] |
| l8-stack-and-heap | quiz[0].widget.options[1].why | wrong option: Nothing: it frees `price` early :: Stack objects are freed by their frame, at `}`. `d… | correct | unit basis: first row of quiz[0] |
| l8-stack-and-heap | quiz[0].widget.options[2].why | wrong option: It leaks `price` :: Nothing leaks: `price` goes with its frame. The bug is deleting m… | correct | unit basis: first row of quiz[0] |
| l8-stack-and-heap | quiz[0].feedback.correct | Only `delete` what `new` made. | correct | unit basis: first row of quiz[0] |
| l8-stack-and-heap | quiz[0].feedback.generic | Not quite right. Who created `price`, and who frees it? | correct | unit basis: first row of quiz[0] |
| l8-stack-and-heap | quiz[0].explain.text | `price` lives in the frame and is freed at `}`. g++ warns "called on unallocated object 'price'", a… | correct | unit basis: first row of quiz[0] |
| l8-stack-and-heap | quiz[1].widget.options[0] | key: It is valid: `p` is not null, must not be read through, and still needs `delete[] p` | correct | [expr.new]/8, [basic.stc.dynamic.allocation]/2: non-null, not to be dereferenced, must be freed; run under the app compiler and grader (check l8.quiz1) |
| l8-stack-and-heap | quiz[1].widget.options[1].why | wrong option: It returns `nullptr` :: `new double[0]` returns a real, non-null pointer to zero elem… | correct | unit basis: first row of quiz[1] |
| l8-stack-and-heap | quiz[1].widget.options[2].why | wrong option: It is undefined behaviour :: Allocating zero elements is allowed. Reading `p[0]` woul… | correct | unit basis: first row of quiz[1] |
| l8-stack-and-heap | quiz[1].feedback.correct | Zero elements, one block to free. | correct | unit basis: first row of quiz[1] |
| l8-stack-and-heap | quiz[1].feedback.generic | Not quite right. Is a zero-length array allowed? | correct | unit basis: first row of quiz[1] |
| l8-stack-and-heap | quiz[1].explain.text | A zero-length `new[]` is legal and returns a unique non-null pointer. There is nothing to read, but… | correct | unit basis: first row of quiz[1] |
| l8-stack-and-heap | quiz[2].widget.options[0] | key: A local in `main`: `main`'s frame lasts the whole run | correct | main's frame lasts for the whole run: [basic.start.main] |
| l8-stack-and-heap | quiz[2].widget.options[1].why | wrong option: It must be on the heap, made with `new` :: Nothing forces the heap. `main`'s frame ex… | correct | unit basis: first row of quiz[2] |
| l8-stack-and-heap | quiz[2].widget.options[2].why | wrong option: It cannot be a local: locals die too soon :: Locals die at their function's `}`, and … | correct | unit basis: first row of quiz[2] |
| l8-stack-and-heap | quiz[2].feedback.correct | `main`'s locals live as long as the program. | correct | unit basis: first row of quiz[2] |
| l8-stack-and-heap | quiz[2].feedback.generic | Not quite right. When does `main`'s frame end? | correct | unit basis: first row of quiz[2] |
| l8-stack-and-heap | quiz[2].explain.text | A local in `main` lives until `main` returns, which is the end of the run. Other code can reach it … | correct | unit basis: first row of quiz[2] |
| l8-stack-and-heap | quiz[3].widget.options[0] | key: No: the elements are on the heap; only the small vector object is a local | correct | as s3; 12 bytes measured here, 24 on x86-64 |
| l8-stack-and-heap | quiz[3].widget.options[1].why | wrong option: Yes: 8 MB of locals is too much :: The 8 MB of elements are on the heap. The local is… | correct | unit basis: first row of quiz[3] |
| l8-stack-and-heap | quiz[3].feedback.correct | A vector's data is on the heap. | correct | unit basis: first row of quiz[3] |
| l8-stack-and-heap | quiz[3].feedback.generic | Not quite right. Which part of a vector is a local? | correct | unit basis: first row of quiz[3] |
| l8-stack-and-heap | quiz[3].explain.text | `v` itself holds a few pointers (12 bytes here, 24 on a desk). Its million `double`s sit on the hea… | correct | unit basis: first row of quiz[3] |
| l8-stack-and-heap | summary.ideas[0] | Each call's locals live in its frame on the stack and die at its `}`. The stack is a few MB, so big… | correct | restates s1 to s5; run under the app compiler and grader: mismatched and double deletes ran silently in the app build (checks l8.s5, l8 summary) |
| l8-stack-and-heap | summary.ideas[1] | `new` puts an object on the heap until you `delete` it: `new` with `delete`, `new[]` with `delete[]… | correct | unit basis: first row of summary |
| l8-stack-and-heap | summary.ideas[2] | A vector object is a small local; its elements are on the heap. The browser build forgives mismatch… | correct | unit basis: first row of summary |
| l8-stack-and-heap | summary.formula | Pairing allocations: \texttt{new} \leftrightarrow \texttt{delete}, \qquad \texttt{new[]} \leftright… | correct | unit basis: first row of summary |
| l8-stack-and-heap | summary.trap | Plain `delete` on memory from `new[]` is undefined behaviour, even when the program seems to run fi… | correct | unit basis: first row of summary |
| l9-owning-memory | screens[0].prose | A **constructor** runs when an object is created; a **destructor**, `~Position`, runs when it ends.… | correct | [class.dtor], [stmt.dcl]: destroyed at the end of the block; run under the app compiler and grader prints open, trading, close, done (check l9.s0) |
| l9-owning-memory | screens[0].canvas.state.caption | caption: While `trade` runs, `p` lives in its frame | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].widget.options[0] | key: `open VOD`, `trading`, `close VOD`, `done` | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].widget.options[1].why | wrong option: `open VOD`, `trading`, `done` :: You expected cleanup to happen later or not at all, … | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].widget.options[2].why | wrong option: `open VOD`, `trading`, `done`, `close VOD` :: `p` is a local of `trade`, not of `main… | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].widget.options[3].why | wrong option: `open VOD`, `close VOD`, `trading`, `done` :: `p` lives until the end of its scope, s… | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].hints[0] | hint: When does `p`'s frame disappear? | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].hints[1] | hint: `p` is a local of `trade`. | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].hints[2] | hint: `trade` prints `trading`, then reaches `}`: `p`'s destructor prints `close VOD`. Only then do… | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].feedback.correct | The destructor runs at the closing brace, every time. | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].feedback.generic | Not quite right. Find the exact line where `p` stops existing. | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].feedback.byKey.never | You expected cleanup later, as with a garbage collector. C++ runs the destructor at `trade`'s `}`. | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].explain.text | `p` lives in `trade`'s frame. At `trade`'s `}` its destructor runs and prints `close VOD`, then `ma… | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[0].explain.canvas.caption | caption: `p`'s destructor ran at `trade`'s `}` | correct | unit basis: first row of screens[0] |
| l9-owning-memory | screens[1].prose | This volume-weighted average price allocates scratch space with `new[]`. A function can leave by an… | correct | trace: the returns on lines 3 and 9 come before the delete[] on line 10 |
| l9-owning-memory | screens[1].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].widget.answer | key: ["l3", "l9"] | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].widget.wrong[0] | slip: ["l3", "l9", "l11"] (all) | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].hints[0] | hint: Find every `return`. Which ones run before line 10? | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].hints[1] | hint: Line 10 is the only `delete[]`. | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].hints[2] | hint: Lines 3 and 9 return before line 10 runs. Line 11 comes after the `delete[]`. | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].feedback.correct | Two early exits skip the `delete[]`. | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].feedback.generic | Not quite right. Check each `return` against line 10. | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].feedback.byKey.all | Line 11 runs after the `delete[]` on line 10, so it does not leak. | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].feedback.byKey.l11 | Line 11 runs after `delete[] notional;`, so it is safe. | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].feedback.byKey.l2 | Line 2 allocates. The leaks are the returns that skip line 10. | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[1].explain.text | Lines 3 and 9 leave before line 10, so their `new[]` block is never freed. Every new exit, or a `th… | correct | unit basis: first row of screens[1] |
| l9-owning-memory | screens[2].prose | Give the memory an owner whose destructor frees it. That pattern is **RAII**: a constructor acquire… | correct | RAII (Stroustrup, TC++PL4 13.3); automatic objects are destroyed on every exit from the block: [stmt.jump]/2, and during unwinding only when the exception is caught: [except.terminate] |
| l9-owning-memory | screens[2].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[2].widget.options[0] | key: All three: `notional`'s destructor runs at every exit | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[2].widget.options[1].why | wrong option: Only line 10, the normal exit :: The vector is a local. Whatever path leaves the func… | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[2].widget.options[2].why | wrong option: None, until you call `notional.clear()` :: `clear` empties a vector you keep using. I… | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[2].hints[0] | hint: When does a local's destructor run? | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[2].hints[1] | hint: Every `return` ends the function's frame. | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[2].hints[2] | hint: Each `return` ends `vwap`'s frame, and the vector's destructor frees its heap buffer every ti… | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[2].feedback.correct | Every exit runs the destructor. | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[2].feedback.generic | Not quite right. When does a local vector's destructor run? | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[2].feedback.byKey.last | The destructor runs on every path out of the function, not just the last one. | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[2].explain.text | `notional` owns its heap buffer, and its destructor runs at every exit: each `return`, and a `throw… | correct | unit basis: first row of screens[2] |
| l9-owning-memory | screens[3].prose | `std::unique_ptr<T>` owns one heap object and deletes it in its destructor. `std::make_unique<T>()`… | correct | [unique.ptr]; run under the app compiler and grader: solution passes, starter fails test 3 only (check l9.s3); delete on a unique_ptr does not compile (check l9.s3 hint) |
| l9-owning-memory | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l9-owning-memory | screens[3].widget | code: 6 tests; solution passes, starter fails | correct | unit basis: first row of screens[3] |
| l9-owning-memory | screens[3].hints[0] | hint: Replace the raw pointer with an owner, then delete the `delete`. | correct | unit basis: first row of screens[3] |
| l9-owning-memory | screens[3].hints[1] | hint: `auto book = std::make_unique<Book>();` and keep using `book->`. | correct | unit basis: first row of screens[3] |
| l9-owning-memory | screens[3].hints[2] | hint: With `make_unique`, both `return` lines free the `Book`. Remove `delete book;` too: `delete` … | correct | unit basis: first row of screens[3] |
| l9-owning-memory | screens[3].feedback.correct | No `delete` left, and no leak on any path. | correct | unit basis: first row of screens[3] |
| l9-owning-memory | screens[3].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of screens[3] |
| l9-owning-memory | screens[3].feedback.byKey.test-3 | A `Book` is still alive after the capped call: the early `return limit;` skipped the `delete`. Let … | correct | unit basis: first row of screens[3] |
| l9-owning-memory | screens[3].explain.text | `book` now owns the `Book`, and its destructor deletes it on both returns. The capped path, which l… | correct | unit basis: first row of screens[3] |
| l9-owning-memory | screens[4].prose | A `unique_ptr` is the *only* owner, so copying one is a compile error. `std::move(a)` hands ownersh… | correct | [unique.ptr.single.ctor]: move only; run under the app compiler and grader: the two quoted clang lines at 6:16; move compiles, get(), a copy and *a do not (checks l9.s4) |
| l9-owning-memory | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].widget.options[0] | key: `book_order(std::move(a));` | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].widget.options[1].why | wrong option: `book_order(a.get());` :: `get()` returns a raw `Order*`, and the parameter wants a `… | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].widget.options[2].why | wrong option: `std::unique_ptr<Order> b = a; book_order(b);` :: That is the same copy, and the same… | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].widget.options[3].why | wrong option: `book_order(*a);` :: `*a` is the `Order` itself, not an owner of it, so the types do … | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].hints[0] | hint: Copying is banned. What else can happen to ownership? | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].hints[1] | hint: The error says copying is deleted; moving is not. | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].hints[2] | hint: `std::move(a)` moves ownership into the parameter. Afterwards `a` is null. | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].feedback.correct | Ownership moves; it is never copied. | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].feedback.generic | Not quite right. Find the call that transfers ownership. | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].feedback.byKey.get | `get()` gives a raw pointer, not an owner. Two owners would delete the order twice. | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[4].explain.text | `std::move(a)` transfers the order to `o`, and `a` becomes null: test it with `if (a)`. When `book_… | correct | unit basis: first row of screens[4] |
| l9-owning-memory | screens[5].prose | Returning a `unique_ptr` hands ownership to the caller: no copy, no leak. An empty `unique_ptr` (`n… | correct | run under the app compiler and grader: solution passes; always calling make_unique fails test 4 (check l9.s5) |
| l9-owning-memory | screens[5].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[5] |
| l9-owning-memory | screens[5].widget | code: 6 tests; solution passes, starter fails | correct | unit basis: first row of screens[5] |
| l9-owning-memory | screens[5].hints[0] | hint: Two cases: `qty == 0`, and everything else. | correct | unit basis: first row of screens[5] |
| l9-owning-memory | screens[5].hints[1] | hint: `return std::make_unique<Position>(sym, qty);` creates the position and its owner. | correct | unit basis: first row of screens[5] |
| l9-owning-memory | screens[5].hints[2] | hint: `if (qty == 0) return nullptr;` then `return std::make_unique<Position>(sym, qty);`. | correct | unit basis: first row of screens[5] |
| l9-owning-memory | screens[5].feedback.correct | The caller now owns the position. | correct | unit basis: first row of screens[5] |
| l9-owning-memory | screens[5].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of screens[5] |
| l9-owning-memory | screens[5].feedback.byKey.test-4 | A quantity of 0 should return an empty pointer: `return nullptr;`. | correct | unit basis: first row of screens[5] |
| l9-owning-memory | screens[5].explain.text | `make_unique` builds the `Position` on the heap and returns its sole owner, which moves out to the … | correct | unit basis: first row of screens[5] |
| l9-owning-memory | screens[6].prose | `std::shared_ptr` lets several owners share one object. It keeps a **count** of owners and deletes … | correct | [util.smartptr.shared]: use_count counts owners; run under the app compiler and grader printed 1 3 1 (check l9.s6); libc++ and libstdc++ update the count atomically |
| l9-owning-memory | screens[6].canvas.state.caption | caption: Before the braces: one owner | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].widget.answer | key: 3 (What does `a.use_count()` return at `// here`?) | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].widget.accept | accept: 3: `a`, `b` and `c` all own the order. | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].widget.wrong[0] | slip: 1 (one) | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].widget.wrong[1] | slip: 2 (two) | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].hints[0] | hint: Each copy of a `shared_ptr` is one more owner. | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].hints[1] | hint: `b` copies `a`; `c` copies `b`. | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].hints[2] | hint: `a`, `b` and `c` share one order, so the count is 3. At the `}`, `b` and `c` die and it drops… | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].feedback.correct | Three owners, one order. | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].feedback.generic | Not quite right. Count every `shared_ptr` that points at the order. | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].feedback.byKey.one | That is the count before the braces. `b` and `c` are copies, and each adds an owner. | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].feedback.byKey.two | `c` copies `b`, which is also an owner of the same order. Count all three. | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].explain.text | `a`, `b` and `c` own the same order, so `use_count()` is 3. At the `}` the count falls to 1, and th… | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[6].explain.canvas.caption | caption: At `// here`: three owners | correct | unit basis: first row of screens[6] |
| l9-owning-memory | screens[7].prose | Two nodes that own each other, as in a book linked to its strategy and back. ```cpp struct Node { s… | correct | run under the app compiler and grader prints end of main only; LeakSanitizer: 64 byte(s) leaked in 2 allocation(s) (checks l9.s7); weak_ptr: [util.smartptr.weak] |
| l9-owning-memory | screens[7].canvas.state.caption | caption: Inside the braces: each node has two owners | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].widget.options[0] | key: `end of main` only | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].widget.options[1].why | wrong option: `freed`, `freed`, `end of main` :: You expected smart pointers to free everything. Wh… | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].widget.options[2].why | wrong option: `freed`, `end of main` :: Neither node can go first: each keeps the other's count at … | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].widget.options[3].why | wrong option: It crashes at the closing brace :: Nothing is deleted at all, so nothing crashes. The… | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].hints[0] | hint: At the inner `}`, `a` and `b` die. What is each node's count then? | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].hints[1] | hint: Each node is still owned by the other's `other` member. | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].hints[2] | hint: Both counts drop from 2 to 1, never to 0. No destructor runs: the nodes leak. | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].feedback.correct | A cycle keeps every count above 0. | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].feedback.generic | Not quite right. Count each node's owners after `a` and `b` die. | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].feedback.byKey.both | You expected smart pointers to free everything. Each node still owns the other, so neither count re… | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].explain.text | When `a` and `b` die, each count drops to 1: the nodes own each other. No destructor runs, and Leak… | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[7].explain.canvas.caption | caption: After the braces: no names left, both counts stuck at 1 | correct | unit basis: first row of screens[7] |
| l9-owning-memory | screens[8].prose | Build classes from members that own themselves, and write no cleanup at all. This is the **rule of … | correct | rule of zero (C++ Core Guidelines C.20); each member's destructor runs: [class.dtor] |
| l9-owning-memory | screens[8].widget.options[0] | key: Nothing: write no destructor at all | correct | unit basis: first row of screens[8] |
| l9-owning-memory | screens[8].widget.options[1].why | wrong option: `delete pricer.get();` :: The `unique_ptr` deletes the `Pricer` itself. A second `del… | correct | unit basis: first row of screens[8] |
| l9-owning-memory | screens[8].widget.options[2].why | wrong option: Call `orders.clear()` :: The vector's own destructor frees its elements. Clearing it … | correct | unit basis: first row of screens[8] |
| l9-owning-memory | screens[8].feedback.correct | Members clean up after themselves. | correct | unit basis: first row of screens[8] |
| l9-owning-memory | screens[8].feedback.generic | Not quite right. Which member does not already free its own memory? | correct | unit basis: first row of screens[8] |
| l9-owning-memory | screens[8].explain.text | Every member is RAII, so destroying a `Desk` destroys them, and they free their memory. No hand-wri… | correct | unit basis: first row of screens[8] |
| l9-owning-memory | screens[9].prose | `Position` prints `open` in its constructor and `close` in its destructor. ```cpp void hold(std::un… | correct | run under the app compiler and grader: the five lines in the stated order (check l9.s9) |
| l9-owning-memory | screens[9].widget.answer | key: ["o1", "o2", "o3", "o4", "o5"] | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].widget.lines.o1 | step: `open VOD`: `make_unique` runs the constructor | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].widget.lines.o2 | step: `opened`: `main` owns the position | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].widget.lines.o3 | step: `hold 100`: `std::move` passed ownership into `hold`'s parameter | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].widget.lines.o4 | step: `close VOD`: `hold`'s parameter was the only owner, and it dies when the call is over, so the… | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].widget.lines.o5 | step: `1 after hold`: `main`'s `p` was moved from, so it is null | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].hints[0] | hint: Who owns the position after `std::move(p)`? | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].hints[1] | hint: The owner that dies first runs the destructor. | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].hints[2] | hint: Created, owned by `main`, moved into `hold`, destroyed when the call to `hold` is over, and `… | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].feedback.correct | Ownership moved, so the cleanup moved with it. | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].feedback.generic | Not quite right. Track which variable owns the position at each line. | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[9].explain.text | After `std::move(p)`, `hold`'s parameter is the only owner, so the position closes when the call is… | correct | unit basis: first row of screens[9] |
| l9-owning-memory | screens[10].prose | An order book holds live orders. Each order belongs to exactly one book. Strategies keep raw `Order… | correct | [vector.capacity]: reallocation invalidates pointers to elements; a unique_ptr's pointee does not move |
| l9-owning-memory | screens[10].widget.options[0] | key: `std::vector<std::unique_ptr<Order>> orders;` | correct | unit basis: first row of screens[10] |
| l9-owning-memory | screens[10].widget.options[1].why | wrong option: `std::vector<Order> orders;` :: When the vector grows, it moves its elements to a new… | correct | unit basis: first row of screens[10] |
| l9-owning-memory | screens[10].widget.options[2].why | wrong option: `std::vector<std::shared_ptr<Order>> orders;` :: Shared ownership blurs who cancels a… | correct | unit basis: first row of screens[10] |
| l9-owning-memory | screens[10].widget.options[3].why | wrong option: `std::vector<Order*> orders;` filled with `new` :: Nothing owns these orders: every c… | correct | unit basis: first row of screens[10] |
| l9-owning-memory | screens[10].hints[0] | hint: Two needs: one owner per order, and a fixed address. | correct | unit basis: first row of screens[10] |
| l9-owning-memory | screens[10].hints[1] | hint: A `unique_ptr` keeps its object at one heap address, wherever the pointer itself moves. | correct | unit basis: first row of screens[10] |
| l9-owning-memory | screens[10].hints[2] | hint: `std::vector<std::unique_ptr<Order>>`: the book is the single owner, and each order stays put… | correct | unit basis: first row of screens[10] |
| l9-owning-memory | screens[10].feedback.correct | One owner, fixed addresses, automatic cleanup. | correct | unit basis: first row of screens[10] |
| l9-owning-memory | screens[10].feedback.generic | Not quite right. Check ownership and what happens when the vector grows. | correct | unit basis: first row of screens[10] |
| l9-owning-memory | screens[10].feedback.byKey.value | A growing vector moves its elements, so raw pointers to them dangle. | correct | unit basis: first row of screens[10] |
| l9-owning-memory | screens[10].explain.text | Each order lives at a fixed heap address owned by one `unique_ptr`, so growing the vector moves onl… | correct | unit basis: first row of screens[10] |
| l9-owning-memory | quiz[0].prose | ```cpp auto a = std::make_unique<double>(101.5); auto b = std::move(a); std::cout << (a == nullptr)… | correct | [unique.ptr.single.ctor]: the source is null after a move; run under the app compiler and grader prints 1 101.5 (check l9.quiz0) |
| l9-owning-memory | quiz[0].widget.options[0] | key: `1 101.5` | correct | unit basis: first row of quiz[0] |
| l9-owning-memory | quiz[0].widget.options[1].why | wrong option: `0 101.5` :: `std::move(a)` hands the double over to `b` and leaves `a` empty, so `a … | correct | unit basis: first row of quiz[0] |
| l9-owning-memory | quiz[0].widget.options[2].why | wrong option: It does not compile :: Moving a `unique_ptr` is allowed; only copying is not. | correct | unit basis: first row of quiz[0] |
| l9-owning-memory | quiz[0].feedback.correct | A moved-from `unique_ptr` is null. | correct | unit basis: first row of quiz[0] |
| l9-owning-memory | quiz[0].feedback.generic | Not quite right. What is left in `a` after the move? | correct | unit basis: first row of quiz[0] |
| l9-owning-memory | quiz[0].explain.text | The move transfers ownership, so `b` owns 101.5 and `a` is null. Reading `*a` now would be a null d… | correct | unit basis: first row of quiz[0] |
| l9-owning-memory | quiz[1].widget.options[0] | key: Automatically with `delete[]` when `px` goes out of scope | correct | [unique.ptr.runtime]: the array form uses delete[]; make_unique value-initialises; run under the app compiler and grader prints 0 101.5 (check l9.quiz0) |
| l9-owning-memory | quiz[1].widget.options[1].why | wrong option: You must call `delete[] px.get();` :: The `unique_ptr<double[]>` does that itself; a … | correct | unit basis: first row of quiz[1] |
| l9-owning-memory | quiz[1].widget.options[2].why | wrong option: Automatically, but with plain `delete`, so it is a bug :: The `[]` in the type makes … | correct | unit basis: first row of quiz[1] |
| l9-owning-memory | quiz[1].feedback.correct | The array form uses `delete[]` for you. | correct | unit basis: first row of quiz[1] |
| l9-owning-memory | quiz[1].feedback.generic | Not quite right. What does the `[]` in the type change? | correct | unit basis: first row of quiz[1] |
| l9-owning-memory | quiz[1].explain.text | `std::unique_ptr<double[]>` owns an array, supports `px[i]` and frees with `delete[]`. A run set `p… | correct | unit basis: first row of quiz[1] |
| l9-owning-memory | quiz[2].prose | ```cpp double quote_once(double spot) { Pricer* p = new Pricer; return p->price(spot); } ``` | correct | a raw pointer has no destructor action: [basic.fundamental]; one Pricer leaks per call |
| l9-owning-memory | quiz[2].widget.options[0] | key: The `Pricer` is never deleted: a raw `new` with no owner leaks | correct | unit basis: first row of quiz[2] |
| l9-owning-memory | quiz[2].widget.options[1].why | wrong option: `p` dangles after the return :: `p` is never used after the return. The problem is th… | correct | unit basis: first row of quiz[2] |
| l9-owning-memory | quiz[2].widget.options[2].why | wrong option: Nothing: the memory is freed when `p` goes out of scope :: A raw pointer going out of… | correct | unit basis: first row of quiz[2] |
| l9-owning-memory | quiz[2].feedback.correct | Raw pointers do not own. | correct | unit basis: first row of quiz[2] |
| l9-owning-memory | quiz[2].feedback.generic | Not quite right. What happens to the `Pricer` when `p` disappears? | correct | unit basis: first row of quiz[2] |
| l9-owning-memory | quiz[2].explain.text | `p` dies at the `}`, but a raw pointer's death does nothing to its target. Every call leaks one `Pr… | correct | unit basis: first row of quiz[2] |
| l9-owning-memory | quiz[3].prose | ```cpp std::vector<std::unique_ptr<Order>> book; auto o = std::make_unique<Order>(); book.push_back… | correct | run under the app compiler and grader: "call to implicitly-deleted copy constructor" (check l9.quiz3) |
| l9-owning-memory | quiz[3].widget.options[0] | key: It would copy the `unique_ptr`; write `book.push_back(std::move(o));` | correct | unit basis: first row of quiz[3] |
| l9-owning-memory | quiz[3].widget.options[1].why | wrong option: A vector cannot hold `unique_ptr`s :: Vectors of `unique_ptr` are common. They only r… | correct | unit basis: first row of quiz[3] |
| l9-owning-memory | quiz[3].widget.options[2].why | wrong option: `o` might be null :: The compiler does not track nulls. The error is "call to implici… | correct | unit basis: first row of quiz[3] |
| l9-owning-memory | quiz[3].feedback.correct | Move it in. | correct | unit basis: first row of quiz[3] |
| l9-owning-memory | quiz[3].feedback.generic | Not quite right. What does `push_back(o)` do with `o`? | correct | unit basis: first row of quiz[3] |
| l9-owning-memory | quiz[3].explain.text | `push_back(o)` copies its argument, and a `unique_ptr` has no copy. `std::move(o)` moves the order … | correct | unit basis: first row of quiz[3] |
| l9-owning-memory | summary.ideas[0] | RAII: an object acquires a resource in its constructor and releases it in its destructor. The destr… | correct | restates s2 to s8 |
| l9-owning-memory | summary.ideas[1] | `std::unique_ptr<T>` is the single owner of one heap object. Create it with `std::make_unique`; it … | correct | unit basis: first row of summary |
| l9-owning-memory | summary.ideas[2] | `std::shared_ptr` counts owners and frees at zero, but cycles never reach zero and the counting cos… | correct | unit basis: first row of summary |
| l9-owning-memory | summary.formula | Ownership: \texttt{new T} \quad\Rightarrow\quad \texttt{std::make\_unique<T>()}, \qquad \texttt{T* … | correct | unit basis: first row of summary |
| l9-owning-memory | summary.trap | Smart pointers do not make leaks impossible: two `shared_ptr`s that own each other are never freed. | correct | unit basis: first row of summary |
| l9-owning-memory | quiz[1].explain.text (last sentence) | For prices a std::vector<double> is "still the usual choice" | unverified | a usage remark with no source |
| l9-owning-memory | quiz[3].widget.options[1].why (first sentence) | Vectors of unique_ptr "are common" | unverified | a usage remark with no source; that they compile was run (check l9.quiz3 context, review-2.5) |
| review-2 | items[0].prose | ```cpp void swap_px(double a, double b) { double t = a; a = b; b = t; } double bid = 99.5, ask = 10… | correct | by-value parameters are copies; run under the app compiler and grader prints 99.5 100.5 (check review-2.0) |
| review-2 | items[0].widget.options[0] | key: `99.5 100.5` | correct | unit basis: first row of items[0] |
| review-2 | items[0].widget.options[1].why | wrong option: `100.5 99.5` :: The parameters have no `&`, so `swap_px` swaps its own copies and the… | correct | unit basis: first row of items[0] |
| review-2 | items[0].widget.options[2].why | wrong option: It does not compile :: Passing `double`s by value is legal. It just does nothing usef… | correct | unit basis: first row of items[0] |
| review-2 | items[0].feedback.correct | The swap happened to the copies. | correct | unit basis: first row of items[0] |
| review-2 | items[0].feedback.generic | Not quite right. Are `a` and `b` the caller's variables, or copies? | correct | unit basis: first row of items[0] |
| review-2 | items[0].explain.text | `a` and `b` are copies of `bid` and `ask`, swapped and then destroyed at the `}`. The caller's vari… | correct | unit basis: first row of items[0] |
| review-2 | items[1].widget.options[0] | key: `std::size_t n = v.size();` | correct | [dcl.type.cv]: reading and copying compile, push_back through a const reference does not |
| review-2 | items[1].widget.options[1] | key: `double first = v[0];` | correct | unit basis: first row of items[1] |
| review-2 | items[1].widget.options[2] | key: `std::vector<double> c = v; c.push_back(1.0);` | correct | unit basis: first row of items[1] |
| review-2 | items[1].widget.options[3].why | wrong option: `v.push_back(1.0);` :: `push_back` changes the vector, and `v` is a `const` reference… | correct | unit basis: first row of items[1] |
| review-2 | items[1].feedback.correct | Read `v`, or change your own copy. | correct | unit basis: first row of items[1] |
| review-2 | items[1].feedback.generic | Not quite right. Which lines change `v` itself? | correct | unit basis: first row of items[1] |
| review-2 | items[1].explain.text | Reading through `v` is allowed, and so is copying it into a vector of your own and changing that. O… | correct | unit basis: first row of items[1] |
| review-2 | items[2].widget.answer | key: 80 (`struct Level { double px; long long size; };` takes 16 bytes. `const Level* p` holds 0x40… | correct | 5 x 16 = 80 bytes, 0x4050; slips 5 and 40 |
| review-2 | items[2].widget.accept | accept: 80 bytes: 5 levels of 16 bytes, so 0x4050. | correct | unit basis: first row of items[2] |
| review-2 | items[2].widget.wrong[0] | slip: 5 (five) | correct | unit basis: first row of items[2] |
| review-2 | items[2].widget.wrong[1] | slip: 40 (eight) | correct | unit basis: first row of items[2] |
| review-2 | items[2].feedback.correct | 5 × 16 = 80 bytes. | correct | unit basis: first row of items[2] |
| review-2 | items[2].feedback.generic | Not quite right. Multiply the steps by the size of one `Level`. | correct | unit basis: first row of items[2] |
| review-2 | items[2].feedback.byKey.five | You counted elements. Each step moves a whole 16-byte `Level`. | correct | unit basis: first row of items[2] |
| review-2 | items[2].feedback.byKey.eight | You used 8 bytes per step. A `Level` holds a `double` and a `long long`: 16 bytes. | correct | unit basis: first row of items[2] |
| review-2 | items[2].explain.text | Pointer arithmetic moves whole objects: `p + 5` is 5 × 16 = 80 bytes on, address 0x4050. That is wh… | correct | unit basis: first row of items[2] |
| review-2 | items[3].widget.options[0] | key: `double* f() { double x = 1.0; return &x; }` then reading `*f()` | correct | [basic.life], [expr.delete]: undefined; [vector.access]: at() throws; run under the app compiler and grader: both ran silently in the app build, at(5) stopped; ASan reports attempting double-free (checks review-2.3) |
| review-2 | items[3].widget.options[1] | key: `double* p = new double(1.0); delete p; delete p;` | correct | unit basis: first row of items[3] |
| review-2 | items[3].widget.options[2].why | wrong option: `double* q = new double[0]; delete[] q;` :: Allocating zero elements is legal, and fr… | correct | unit basis: first row of items[3] |
| review-2 | items[3].widget.options[3].why | wrong option: `std::vector<double> v(3); v.at(5);` :: `at` checks the index and throws `std::out_of… | correct | unit basis: first row of items[3] |
| review-2 | items[3].feedback.correct | A dead local and a double delete. | correct | unit basis: first row of items[3] |
| review-2 | items[3].feedback.generic | Not quite right. Separate checked errors from unchecked ones. | correct | unit basis: first row of items[3] |
| review-2 | items[3].explain.text | Reading a dead local and deleting twice are undefined: this browser build ran both silently. A desk… | correct | unit basis: first row of items[3] |
| review-2 | items[4].prose | ```cpp int depth(int n) { if (n == 0) return 0; return 1 + depth(n - 1); } ``` | correct | main plus depth(4) to depth(0): 6 frames |
| review-2 | items[4].widget.answer | key: 6 (How many frames are on the stack at the deepest point of `main` calling `depth(4)`, countin… | correct | unit basis: first row of items[4] |
| review-2 | items[4].widget.accept | accept: 6: `main` plus `depth(4)` down to `depth(0)`. | correct | unit basis: first row of items[4] |
| review-2 | items[4].widget.wrong[0] | slip: 5 (five) | correct | unit basis: first row of items[4] |
| review-2 | items[4].widget.wrong[1] | slip: 4 (four) | correct | unit basis: first row of items[4] |
| review-2 | items[4].feedback.correct | `main` and five calls of `depth`. | correct | unit basis: first row of items[4] |
| review-2 | items[4].feedback.generic | Not quite right. List every call that is still waiting when `depth(0)` runs. | correct | unit basis: first row of items[4] |
| review-2 | items[4].feedback.byKey.five | You left out `main`, whose frame is at the bottom the whole time. | correct | unit basis: first row of items[4] |
| review-2 | items[4].feedback.byKey.four | `depth(0)` is a call too, with its own frame. | correct | unit basis: first row of items[4] |
| review-2 | items[4].explain.text | While `depth(0)` runs, `depth(4)`, `depth(3)`, `depth(2)` and `depth(1)` are waiting, and `main` is… | correct | unit basis: first row of items[4] |
| review-2 | items[5].prose | `Position` prints `open` and `close` from its constructor and destructor. ```cpp { std::vector<std:… | correct | run under the app compiler and grader prints open AZN, close AZN, end (check review-2.5) |
| review-2 | items[5].widget.options[0] | key: `open AZN`, `close AZN`, `end` | correct | unit basis: first row of items[5] |
| review-2 | items[5].widget.options[1].why | wrong option: `open AZN`, `end`, `close AZN` :: `book` owns the position and dies at the inner `}`,… | correct | unit basis: first row of items[5] |
| review-2 | items[5].widget.options[2].why | wrong option: `open AZN`, `end` :: `book` is a vector of `unique_ptr`s; when it dies, each owner de… | correct | unit basis: first row of items[5] |
| review-2 | items[5].feedback.correct | The owner died at the inner brace. | correct | unit basis: first row of items[5] |
| review-2 | items[5].feedback.generic | Not quite right. When does `book` go out of scope? | correct | unit basis: first row of items[5] |
| review-2 | items[5].explain.text | `book` lives inside the braces. At the `}` the vector is destroyed, its `unique_ptr` deletes the po… | correct | unit basis: first row of items[5] |
| review-2 | items[6].prose | A small balance book earns interest once per period. | correct | run under the app compiler and grader: solution passes, starter does not compile; 1000 x 1.01 = 1010, 2500 x 1.002 = 2505, 100 x 1.1 x 1.1 = 121 |
| review-2 | items[6].widget | code: 4 tests; solution passes, starter fails | correct | unit basis: first row of items[6] |
| review-2 | items[6].feedback.correct | Changed in place, read in place. | correct | unit basis: first row of items[6] |
| review-2 | items[6].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of items[6] |
| review-2 | items[6].explain.text | `balances` must reach the caller, so it is `std::vector<double>&`. `rates` is only read, and the te… | correct | unit basis: first row of items[6] |
| review-2 | items[7].widget.options[0] | key: `double best_bid()` | correct | [class.mfct.non.static]: a reader is const |
| review-2 | items[7].widget.options[1].why | wrong option: `void add(const Order& o)` :: `add` changes the book, so it cannot promise not to. Th… | correct | unit basis: first row of items[7] |
| review-2 | items[7].widget.options[2].why | wrong option: `void cancel(int id)` :: Cancelling removes an order, which changes the book. | correct | unit basis: first row of items[7] |
| review-2 | items[7].feedback.correct | Readers are `const`; writers are not. | correct | unit basis: first row of items[7] |
| review-2 | items[7].feedback.generic | Not quite right. Which method only reads the book? | correct | unit basis: first row of items[7] |
| review-2 | items[7].explain.text | `best_bid()` only reads, so mark it `double best_bid() const;`. Then code holding a `const Book&`, … | correct | unit basis: first row of items[7] |
| homework-2 | items[0].prose | A position book in £ holds one `Position` per symbol (hidden above your code): ```cpp struct Positi… | correct | run under the app compiler and grader: solution passes; a by-value loop variable fails test 1 (check homework-2.0); 200 x 1.85 - 50 x 1.90 = 275 |
| homework-2 | items[0].widget | code: 9 tests; solution passes, starter fails | correct | unit basis: first row of items[0] |
| homework-2 | items[0].feedback.correct | Every fill lands on the caller's book. | correct | unit basis: first row of items[0] |
| homework-2 | items[0].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of items[0] |
| homework-2 | items[0].feedback.byKey.test-1 | The quantity did not change. If you loop with `for (Position p : book)`, each `p` is a copy: use `P… | correct | unit basis: first row of items[0] |
| homework-2 | items[0].explain.text | `book` is a plain reference, as the caller's positions change; `fills` is only read, so `const&` al… | correct | unit basis: first row of items[0] |
| homework-2 | items[1].prose | A day's executions arrive on `std::cin`: a count `n`, then `n` lines of `qty price`. A quantity of … | correct | run under the app compiler and grader: solution passes; an int total or an int read fails test 4 (checks homework-2.1); 121,485 / 1,200 = 101.2375 |
| homework-2 | items[1].widget | code: 6 tests; solution passes, starter fails | correct | unit basis: first row of items[1] |
| homework-2 | items[1].feedback.correct | Read once, pass by `const&`, print to four decimals. | correct | unit basis: first row of items[1] |
| homework-2 | items[1].feedback.generic | Not yet. The results under the editor say which test failed. | correct | unit basis: first row of items[1] |
| homework-2 | items[1].feedback.byKey.test-4 | 2,500,000,000 shares does not fit in an `int`. Keep quantities as `long long`, as `Order` does. | correct | unit basis: first row of items[1] |
| homework-2 | items[1].explain.text | The orders are read once into a vector, and every function after that takes `const std::vector<Orde… | correct | unit basis: first row of items[1] |
| homework-2 | items[2].prose | ```cpp double payoff(double s, double k) { return s > k ? s - k : 0; } double price_option(double s… | correct | run under the app compiler and grader prints 7.5 (check homework-2.2); the order of the two calls in one + is unspecified: [intro.execution]/17 |
| homework-2 | items[2].widget.answer | key: ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8"] | correct | unit basis: first row of items[2] |
| homework-2 | items[2].widget.lines.e1 | step: Push `main`: the program starts | correct | unit basis: first row of items[2] |
| homework-2 | items[2].widget.lines.e2 | step: Push `price_option(100, 95)`: `main` calls it | correct | unit basis: first row of items[2] |
| homework-2 | items[2].widget.lines.e3 | step: Push `payoff(110, 95)`: the up state, 100 × 1.1 | correct | unit basis: first row of items[2] |
| homework-2 | items[2].widget.lines.e4 | step: Pop `payoff`, returning 15 | correct | unit basis: first row of items[2] |
| homework-2 | items[2].widget.lines.e5 | step: Push `payoff(90, 95)`: the down state, 100 × 0.9 | correct | unit basis: first row of items[2] |
| homework-2 | items[2].widget.lines.e6 | step: Pop `payoff`, returning 0: 90 is below the strike | correct | unit basis: first row of items[2] |
| homework-2 | items[2].widget.lines.e7 | step: Pop `price_option`, returning 0.5 × 15 + 0.5 × 0 = 7.5 | correct | unit basis: first row of items[2] |
| homework-2 | items[2].widget.lines.e8 | step: `main` prints 7.5, then its frame is popped | correct | unit basis: first row of items[2] |
| homework-2 | items[2].feedback.correct | At most three frames, pushed and popped in strict order. | correct | unit basis: first row of items[2] |
| homework-2 | items[2].feedback.generic | Not quite right. A frame must be popped before the next call from the same caller starts. | correct | unit basis: first row of items[2] |
| homework-2 | items[2].explain.text | Each `payoff` call returns before the next starts, so the stack is at most three deep: `main`, `pri… | correct | unit basis: first row of items[2] |
| homework-2 | items[3].widget.options[0] | key: `double best_bid()` | correct | as l6 s3: readers are const |
| homework-2 | items[3].widget.options[1] | key: `std::size_t depth()` | correct | unit basis: first row of items[3] |
| homework-2 | items[3].widget.options[2].why | wrong option: `void add(const Order& o)` :: `add` changes the book. The `const` on its parameter pr… | correct | unit basis: first row of items[3] |
| homework-2 | items[3].widget.options[3].why | wrong option: `bool cancel(long long id)` :: Cancelling removes an order, so it changes the book. | correct | unit basis: first row of items[3] |
| homework-2 | items[3].feedback.correct | Mark every reader `const`. | correct | unit basis: first row of items[3] |
| homework-2 | items[3].feedback.generic | Not quite right. Which methods only read the book? | correct | unit basis: first row of items[3] |
| homework-2 | items[3].explain.text | `best_bid` and `depth` only read, so mark them `const`. A pricer holding a `const OrderBook&` can t… | correct | unit basis: first row of items[3] |
| homework-2 | items[4].prose | A pricer allocates `new double[steps + 1]` per call and forgets the `delete[]`. A calibration calls… | correct | 10,000 x 501 x 8 = 40,080,000 bytes; slips 40, 0.004008 and 40,080,000 |
| homework-2 | items[4].widget.answer | key: 40.08 (How many MB does a day's calibration leak? Take 1 MB as 1,000,000 bytes.) | correct | unit basis: first row of items[4] |
| homework-2 | items[4].widget.accept | accept: 40.08 MB: 10,000 calls × 501 × 8 bytes = 40,080,000 bytes. | correct | unit basis: first row of items[4] |
| homework-2 | items[4].widget.wrong[0] | slip: 40 (n) | correct | unit basis: first row of items[4] |
| homework-2 | items[4].widget.wrong[1] | slip: 0.004008 (one) | correct | unit basis: first row of items[4] |
| homework-2 | items[4].widget.wrong[2] | slip: 40080000 (bytes) | correct | unit basis: first row of items[4] |
| homework-2 | items[4].feedback.correct | 501 doubles, 8 bytes each, 10,000 times. | correct | unit basis: first row of items[4] |
| homework-2 | items[4].feedback.generic | Not quite right. Count the doubles per call first: `steps + 1`. | correct | unit basis: first row of items[4] |
| homework-2 | items[4].feedback.byKey.n | You used 500 doubles per call. The lattice has `steps + 1` = 501. | correct | unit basis: first row of items[4] |
| homework-2 | items[4].feedback.byKey.one | That is one call. Multiply by 10,000 calls. | correct | unit basis: first row of items[4] |
| homework-2 | items[4].feedback.byKey.bytes | That is the count in bytes. Divide by 1,000,000. | correct | unit basis: first row of items[4] |
| homework-2 | items[4].explain.text | Each call leaks `new double[501]`, 4,008 bytes. 10,000 calls leak 40,080,000 bytes, about 40 MB a d… | correct | unit basis: first row of items[4] |
| homework-2 | items[5].prose | In this browser build four of these snippets ran to the end, and one stopped with an error message. | correct | run under the app compiler and grader: the null read gave 0, both bad deletes ran to the end, at(5) stopped; ASan: SEGV, alloc-dealloc-mismatch, double-free (checks homework-2.5, l7.quiz0, l8.s5, review-2.3) |
| homework-2 | items[5].widget.options[0] | key: `int* p = nullptr; int x = *p;` | correct | unit basis: first row of items[5] |
| homework-2 | items[5].widget.options[1] | key: `double* q = new double[4]; delete q;` | correct | unit basis: first row of items[5] |
| homework-2 | items[5].widget.options[2] | key: `double* r = new double(1.0); delete r; delete r;` | correct | unit basis: first row of items[5] |
| homework-2 | items[5].widget.options[3].why | wrong option: `std::vector<double> v(3); double y = v.at(5);` :: `at` checks the index and throws `… | correct | unit basis: first row of items[5] |
| homework-2 | items[5].widget.options[4].why | wrong option: `double* s = new double[0]; delete[] s;` :: A zero-length `new[]` is legal and `delet… | correct | unit basis: first row of items[5] |
| homework-2 | items[5].feedback.correct | Null read, mismatched delete, double delete. | correct | unit basis: first row of items[5] |
| homework-2 | items[5].feedback.generic | Not quite right. Separate checked errors from unchecked ones. | correct | unit basis: first row of items[5] |
| homework-2 | items[5].explain.text | Here all three undefined lines ran quietly: the null read gave 0, and both bad deletes were silent.… | correct | unit basis: first row of items[5] |
| homework-2 | items[6].prose | ```cpp std::vector<double> px{100.0, 101.0, 102.0}; const double& first = px[0]; px.push_back(103.0… | correct | [vector.modifiers]: reallocation invalidates references; run under the app compiler and grader printed 2.93542e-306; ASan: heap-use-after-free (checks homework-2.6) |
| homework-2 | items[6].widget.options[0] | key: Anything: `push_back` may move the elements, leaving `first` dangling | correct | unit basis: first row of items[6] |
| homework-2 | items[6].widget.options[1].why | wrong option: `100` :: That assumes the elements stay put. A full vector moves them to a bigger buf… | correct | unit basis: first row of items[6] |
| homework-2 | items[6].widget.options[2].why | wrong option: `103` :: `first` was bound to the old `px[0]`, not to the last element. And after the… | correct | unit basis: first row of items[6] |
| homework-2 | items[6].widget.options[3].why | wrong option: It does not compile :: It compiles. The compiler cannot know the vector will grow at … | correct | unit basis: first row of items[6] |
| homework-2 | items[6].feedback.correct | A reference into a vector dies when the vector grows. | correct | unit basis: first row of items[6] |
| homework-2 | items[6].feedback.generic | Not quite right. Where are the three prices after `push_back` on a full vector? | correct | unit basis: first row of items[6] |
| homework-2 | items[6].explain.text | The vector was full, so `push_back` moved its elements to a new buffer and freed the old one. `firs… | correct | unit basis: first row of items[6] |
| homework-2 | items[7].prompt | prompt: A colleague's utilities for a trade blotter, in £: ```cpp struct Trade { std::string sym; i… | correct | run under the app compiler and grader: the hardening message "vector[] index out of bounds", the clang warning for &best, and model answer (e) compiles and runs (checks homework-2.7) |
| homework-2 | items[7].model | model answer: **(a)** Cost: `trades` is taken by value, so every call copies the whole blotter, eve… | imprecise | part (a): "silently reads whatever follows the buffer" states one outcome of undefined behaviour as fact; the rubric says "may". Finding 6. The rest of the model was run (checks homework-2.7) |
| homework-2 | items[7].rubric[0] | rubric: (a) Says the by-value parameter copies the whole blotter on each call and should be `const … | correct | unit basis: first row of items[7] |
| homework-2 | items[7].rubric[1] | rubric: (a) Says the off-by-one is undefined behaviour: libc++'s check stops it here, while a desk … | correct | unit basis: first row of items[7] |
| homework-2 | items[7].rubric[2] | rubric: (b) Says `&best` dangles once its local dies at the `}`; proposes returning by value (`std:… | correct | unit basis: first row of items[7] |
| homework-2 | items[7].rubric[3] | rubric: (b) Notes the parameter should be `const&`, the loop variable `const Trade&`, and that an e… | correct | unit basis: first row of items[7] |
| homework-2 | items[7].rubric[4] | rubric: (c) Explains that `add_fee` changes a copy and needs `Trade&` | correct | unit basis: first row of items[7] |
| homework-2 | items[7].rubric[5] | rubric: (d) Says the raw `new` makes every caller responsible for exactly one `delete`, and replace… | correct | unit basis: first row of items[7] |
| homework-2 | items[7].rubric[6] | rubric: (e) Gives four corrected functions that compile and match the fixes above | correct | unit basis: first row of items[7] |
| l10-invariants | screens[0].prose | A quote's bid must stay below its ask. In Python, any code may set `q.bid` to anything. Here is a C… | correct | struct members are public by default: [class.access]; 100.4 - 100.6 prints -0.2; run under the app compiler and grader (check l10.s0) |
| l10-invariants | screens[0].canvas.state.caption | caption: `q` after its first line | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].widget.options[0] | key: `-0.2` | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].widget.options[1].why | wrong option: A compile error, because the bid is now above the ask :: You expected the compiler to… | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].widget.options[2].why | wrong option: `0.2` :: You used the old bid. The line before set `q.bid` to 100.6, so the ask minus… | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].widget.options[3].why | wrong option: The program stops when it runs :: Nothing checks the values at run time either. A str… | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].hints[0] | hint: Which value does `q.bid` hold when the last line runs? | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].hints[1] | hint: The assignment changed this cell. | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].hints[2] | hint: The ask is 100.4 and the bid is now 100.6: 100.4 − 100.6. | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].feedback.correct | The quote is now crossed, and nothing objected. | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].feedback.generic | Not quite right. Follow `q.bid` through each line. | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].feedback.byKey.compile | You expected the compiler to know the rule. It checks types only, and 100.6 is a valid `double`. | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].explain.text | Every member of a `struct` is open to any code, as in Python. The typo made a quote whose bid is ab… | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].explain.canvas.caption | caption: The bid is above the ask: a crossed quote. | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[0].explain.canvas.values | canvas: {"r0c1": "100.6"} | correct | unit basis: first row of screens[0] |
| l10-invariants | screens[1].prose | Suppose a type could hide some members from outside code. Here are the members of a better `Quote`.… | correct | access control keeps the data behind checked functions (Stroustrup, TC++PL4 16.2.3) |
| l10-invariants | screens[1].widget.answer | key: {"inside": ["bid", "ask"], "outside": ["mid", "spread", "setbid"]} | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].hints[0] | hint: Which members, if anyone could write them, would let outside code skip the check? | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].hints[1] | hint: These two hold the numbers the rule is about. | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].hints[2] | hint: Hide `bid_` and `ask_`. Leave the three functions open: two only read, and `set_bid` checks. | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].feedback.correct | Data hidden, checked functions open. | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].feedback.generic | Not quite right. Ask of each member: could outside code break the rule through it? | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].feedback.byKey.bid | If any code can write `bid_`, it can set 100.6 and skip every check. Keep it where only `Quote`'s f… | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].feedback.byKey.ask | If any code can write `ask_`, it can drop it below the bid. Keep it where only `Quote`'s functions … | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].feedback.byKey.mid | `mid()` only reads. Hiding it protects nothing and stops everyone from using the quote. | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].feedback.byKey.spread | `spread()` only reads. Hiding it protects nothing and stops everyone from using the quote. | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].feedback.byKey.setbid | `set_bid` checks before it stores, so outside code may call it. Hidden, nobody could ever move the … | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[1].explain.text | You hid the data and left open the functions that read or check. C++ calls the hidden part **privat… | correct | unit basis: first row of screens[1] |
| l10-invariants | screens[2].prose | Here is that split in C++. A **class** marks its sections `public:` and `private:`. A `struct` is t… | correct | [class.access]; run under the app compiler and grader: 12:7 "'bid_' is a private member of 'Quote'", 6:12 note, 1 error (check l10.s2) |
| l10-invariants | screens[2].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].widget.options[0] | key: Code outside the class writing a private member | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].widget.options[1].why | wrong option: Storing a bid above the ask :: You expected a check on the value. The compiler refuse… | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].widget.options[2].why | wrong option: Putting `public:` before `private:` :: The sections can come in any order. The error … | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].widget.options[3].why | wrong option: Using `class` instead of `struct` :: Both are allowed. The error is about who may nam… | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].hints[0] | hint: Read the first `error:` line in the terminal. | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].hints[1] | hint: It names the member and the class. | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].hints[2] | hint: `'bid_' is a private member of 'Quote'`: line 12 is outside the class, so it may not name `bi… | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].feedback.correct | The rule is about names: outside code may not name `bid_`. | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].feedback.generic | Not quite right. Read the `error:` line word by word. | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].feedback.byKey.value | You expected a check on the value. The compiler refused the name `bid_` before looking at any numbe… | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[2].explain.text | Line 12 is in `main`, outside `Quote`, so it may not name a private member. Python has no such chec… | correct | unit basis: first row of screens[2] |
| l10-invariants | screens[3].prose | Now write the class. The **initialiser list**, `: bid_(bid), ask_(ask)`, builds each member before … | correct | [class.base.init]: members are initialised before the body; run under the app compiler and grader: solution passes, abort also passes, no check fails test 4, `>` fails test 5, a non-const spread and a missing mid give the named compile messages (checks l10.s3) |
| l10-invariants | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[3].widget | code: 6 tests; solution passes, starter fails | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[3].hints[0] | hint: Put the check in the constructor's body, after the list has built the members. | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[3].hints[1] | hint: A locked quote, bid equal to ask, must stop the program too. | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[3].hints[2] | hint: `if (bid_ >= ask_) throw std::invalid_argument("bid must be below ask");` then `double mid() … | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[3].feedback.correct | Every `Quote` that exists now has its bid below its ask. | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[3].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[3].feedback.byKey.compile | The compiler stopped. If the message says a function is not marked const, add `const` after its bra… | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[3].feedback.byKey.test-4 | Test 4 builds a quote with the bid above the ask, and your program carried on. Check in the constru… | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[3].feedback.byKey.test-5 | Test 5 builds a quote with the bid equal to the ask. Refuse it too: use `>=` in the check, not `>`. | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[3].explain.text | The list builds `bid_` and `ask_`; the body refuses a crossed or locked quote before anyone can use… | correct | unit basis: first row of screens[3] |
| l10-invariants | screens[4].prose | A `Position` holds a quantity of shares and their **average price**. You hold 100 shares bought at … | correct | (100 x 10 + 300 x 12) / 400 = 11.5; slips (10 + 12) / 2 = 11 and 12 |
| l10-invariants | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].widget.answer | key: 11.5 (What is the average price of the 400 shares, in pounds?) | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].widget.accept | accept: £11.50: $(100 \times 10 + 300 \times 12) / 400 = 4600 / 400$. | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].widget.wrong[0] | slip: 11.0 (simple) | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].widget.wrong[1] | slip: 12.0 (last) | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].hints[0] | hint: What did the 400 shares cost in total? | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].hints[1] | hint: 300 of the 400 shares cost £12.00 each. | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].hints[2] | hint: Total cost $100 \times 10 + 300 \times 12 = 4600$, over 400 shares. | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].feedback.correct | £4,600 over 400 shares is £11.50. | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].feedback.generic | Not quite right. Divide the total cost by the total shares. | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].feedback.byKey.simple | You averaged the two prices. Three times as many shares were bought at £12.00, so they pull the ave… | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].feedback.byKey.last | That is the price of the last buy. The first 100 shares still cost £10.00. | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].explain.text | You weighted each price by its shares: $4600 / 400 = 11.5$. The quantity and the average change tog… | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[4].explain.canvas.caption | caption: $100 \times 10 + 300 \times 12 = 4600$, over 400 shares | correct | unit basis: first row of screens[4] |
| l10-invariants | screens[5].prose | Now let the class keep the two numbers consistent. A buy moves the average; a sale does not. This d… | correct | run under the app compiler and grader: solution passes; each of the six named slips fails first at its test (checks l10.s5); 0.0 / 0 is NaN (check l10.s5 unchecked buy) |
| l10-invariants | screens[5].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].widget | code: 10 tests; solution passes, starter fails | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].hints[0] | hint: Update the average before you add to `qty_`: the formula needs the old quantity. | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].hints[1] | hint: The last row sells 1 share of none. | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].hints[2] | hint: `avg_ = (qty_ * avg_ + qty * px) / (qty_ + qty); qty_ += qty;` In `sell`, check, subtract, an… | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].feedback.correct | Quantity and average now move together, and never go short. | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].feedback.byKey.test-2 | Test 2 expects £11.50. Weight each price by its shares, and use `qty_` before you add the new share… | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].feedback.byKey.test-4 | Test 4 sells 150 shares and expects the average to stay £11.50. A sale changes only the quantity. | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].feedback.byKey.test-6 | Test 6 sells everything. Set the average back to 0 when the quantity reaches 0. | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].feedback.byKey.test-8 | Test 8 sells 101 of 100 shares. Refuse before you change `qty_`. | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].feedback.byKey.test-9 | Test 9 buys 0 shares. Without a check the average becomes $0/0$, which is NaN. | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[5].explain.text | `buy` updates the average from the old quantity, then the quantity. `sell` refuses a short before c… | correct | unit basis: first row of screens[5] |
| l10-invariants | screens[6].prose | A risk limit should never change once it is set, so its member is `const`. This constructor sets it… | correct | [class.base.init]/9, [dcl.type.cv]; run under the app compiler and grader: both errors, the note and "2 errors generated"; the list form compiles; this-> and a local const do not (checks l10.s6) |
| l10-invariants | screens[6].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[6].widget.options[0] | key: `Limit(double m) : max_(m) {}` | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[6].widget.options[1].why | wrong option: `Limit(double m) { max_ = m; }` :: That is the code that failed. By the time the body… | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[6].widget.options[2].why | wrong option: `Limit(double m) { this->max_ = m; }` :: `this->max_` is the same member. It is still… | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[6].widget.options[3].why | wrong option: `Limit(double m) { const double max_ = m; }` :: That makes a new local variable that … | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[6].hints[0] | hint: When does the body of a constructor run: before or after the members exist? | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[6].hints[1] | hint: The first error says the member must be explicitly initialised. | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[6].hints[2] | hint: Members are built in the initialiser list, before the body. A `const` member can only get its… | imprecise | [class.mem]: a default member initialiser also gives a const member its value (check l10 summary). Finding 7 |
| l10-invariants | screens[6].feedback.correct | The list builds `max_` with its value, once. | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[6].feedback.generic | Not quite right. A `const` member gets its value when it is built, in the list. | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[6].feedback.byKey.body | That is the code that failed. By the time the body runs, `max_` already exists, and a `const` canno… | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[6].explain.text | The list builds each member with its value; the body runs after that. Assigning in the body builds … | correct | unit basis: first row of screens[6] |
| l10-invariants | screens[7].prose | This `Quote` checks its constructor and keeps its data private. A colleague adds a setter. | correct | trace: set_bid stores 100.6 unchecked; run under the app compiler and grader prints -0.2 (check l10.s0, s7) |
| l10-invariants | screens[7].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].widget.options[0] | key: `-0.2` | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].widget.options[1].why | wrong option: Nothing: it stops, because the constructor checks the bid :: You expected the constru… | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].widget.options[2].why | wrong option: A compile error, because `bid_` is private :: `set_bid` is a member function, so it m… | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].widget.options[3].why | wrong option: `0.2` :: `set_bid` did store 100.6. The spread is 100.4 − 100.6. | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].hints[0] | hint: When does the constructor's check run? | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].hints[1] | hint: This line changes `bid_`. Does it check anything? | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].hints[2] | hint: The check ran once, on line 14. Line 15 calls `set_bid`, which stores 100.6 straight away. | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].feedback.correct | A private member is only as safe as the functions that write it. | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].feedback.generic | Not quite right. Trace line 15 into `set_bid`. | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].feedback.byKey.ctor | You expected the constructor's check to guard every change. It runs once, when `q` is built; `set_b… | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[7].explain.text | The constructor checks once. Every function that changes the data must check again, or it is a way … | correct | unit basis: first row of screens[7] |
| l10-invariants | screens[8].prose | Bid below ask, and never short: each is an **invariant**. It is a fact about the members that holds… | correct | class invariant (Stroustrup, TC++PL4 2.4.3.2, 17.2.1); a const member function cannot modify members: [class.this] |
| l10-invariants | screens[8].widget.options[0] | key: `double spread() const` | correct | unit basis: first row of screens[8] |
| l10-invariants | screens[8].widget.options[1].why | wrong option: `void set_ask(double a)` :: It changes `ask_`, so it could drop the ask below the bid… | correct | unit basis: first row of screens[8] |
| l10-invariants | screens[8].widget.options[2].why | wrong option: `void widen(double d)`, which subtracts `d` from the bid and adds it to the ask :: Wi… | correct | unit basis: first row of screens[8] |
| l10-invariants | screens[8].widget.options[3].why | wrong option: The constructor `Quote(double b, double a)` :: The constructor is the first place the… | correct | unit basis: first row of screens[8] |
| l10-invariants | screens[8].hints[0] | hint: Which function cannot change `bid_` or `ask_` at all? | correct | unit basis: first row of screens[8] |
| l10-invariants | screens[8].hints[1] | hint: `const` after the brackets means the function cannot change the members, so the invariant sti… | correct | unit basis: first row of screens[8] |
| l10-invariants | screens[8].feedback.correct | A `const` function cannot change the members, so it cannot break the rule. | correct | unit basis: first row of screens[8] |
| l10-invariants | screens[8].feedback.generic | Not quite right. Look for the one function that cannot write to the members. | correct | unit basis: first row of screens[8] |
| l10-invariants | screens[8].explain.text | `spread() const` only reads, so the invariant holds after it as before. Every other function on the… | correct | unit basis: first row of screens[8] |
| l10-invariants | screens[9].prose | An order moves through states. It is `new` while it has shares left, even when partly filled, and `… | correct | run under the app compiler and grader: solution passes; the four named slips fail first at tests 4, 7, 8 and 9 (checks l10.s9); enum class: [dcl.enum] |
| l10-invariants | screens[9].widget | code: 11 tests; solution passes, starter fails | correct | unit basis: first row of screens[9] |
| l10-invariants | screens[9].hints[0] | hint: Each function that changes the order checks its state first. | correct | unit basis: first row of screens[9] |
| l10-invariants | screens[9].hints[1] | hint: Only `new` has arrows leaving it. | correct | unit basis: first row of screens[9] |
| l10-invariants | screens[9].hints[2] | hint: In `fill`: refuse unless `state_ == State::New`, refuse `q <= 0` or `filled_ + q > qty_`, add… | correct | unit basis: first row of screens[9] |
| l10-invariants | screens[9].feedback.correct | The order's states only move along the arrows. | correct | unit basis: first row of screens[9] |
| l10-invariants | screens[9].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[9] |
| l10-invariants | screens[9].feedback.byKey.test-4 | Test 4 fills 40 then 60 of 100 and expects `filled`. Change the state when nothing remains. | correct | unit basis: first row of screens[9] |
| l10-invariants | screens[9].feedback.byKey.test-7 | Test 7 fills a cancelled order. Check the state before you add to `filled_`. | correct | unit basis: first row of screens[9] |
| l10-invariants | screens[9].feedback.byKey.test-8 | Test 8 fills 70 then 40 of 100. Refuse a fill larger than what remains. | correct | unit basis: first row of screens[9] |
| l10-invariants | screens[9].feedback.byKey.test-9 | Test 9 cancels a filled order. `cancel` must check the state too. | correct | unit basis: first row of screens[9] |
| l10-invariants | screens[9].explain.text | Each changing function checks the state first, so the only moves are the arrows from `new`. The fil… | correct | unit basis: first row of screens[9] |
| l10-invariants | quiz[0].prose | ```cpp class Quote { public: Quote(double b, double a) : bid_(b), ask_(a) { if (bid_ >= ask_) throw… | correct | a returned non-const reference exposes the member; run under the app compiler and grader prints -0.2; returning double or const double& stops the assignment (checks l10.quiz0) |
| l10-invariants | quiz[0].widget.options[0] | key: It prints `-0.2` | correct | unit basis: first row of quiz[0] |
| l10-invariants | quiz[0].widget.options[1].why | wrong option: A compile error: you cannot assign to a function call :: `bid()` returns a `double&`,… | correct | unit basis: first row of quiz[0] |
| l10-invariants | quiz[0].widget.options[2].why | wrong option: It stops, because the constructor checks the bid :: The constructor checked once, whe… | correct | unit basis: first row of quiz[0] |
| l10-invariants | quiz[0].widget.options[3].why | wrong option: It prints `0.2`, because `bid()` hands out a copy :: A copy would need the return typ… | correct | unit basis: first row of quiz[0] |
| l10-invariants | quiz[0].feedback.correct | A non-const reference is an open door to private data. | correct | unit basis: first row of quiz[0] |
| l10-invariants | quiz[0].feedback.generic | Not quite right. Look at the return type of `bid()`. | correct | unit basis: first row of quiz[0] |
| l10-invariants | quiz[0].explain.text | `double& bid()` returns a reference to the private member, so `q.bid() = 100.6` writes it directly.… | correct | unit basis: first row of quiz[0] |
| l10-invariants | quiz[1].prose | The same class in Python, with the usual underscore for private data: ```python class Quote: def __… | correct | run, CPython 3.12: prints -0.19999999999998863 (check l10.quiz1); the underscore is a convention (PEP 8) |
| l10-invariants | quiz[1].widget.options[0] | key: It prints `-0.19999999999998863` | correct | unit basis: first row of quiz[1] |
| l10-invariants | quiz[1].widget.options[1].why | wrong option: `AttributeError`, because `_bid` is private :: The underscore is a convention for rea… | correct | unit basis: first row of quiz[1] |
| l10-invariants | quiz[1].widget.options[2].why | wrong option: `ValueError: crossed` :: `__init__` checked once, when `q` was built. The assignment … | correct | unit basis: first row of quiz[1] |
| l10-invariants | quiz[1].widget.options[3].why | wrong option: It prints `-0.2` :: Python prints a float's full shortest repr, so the binary error s… | correct | unit basis: first row of quiz[1] |
| l10-invariants | quiz[1].feedback.correct | Python trusts the caller; C++ `private` does not. | correct | unit basis: first row of quiz[1] |
| l10-invariants | quiz[1].feedback.generic | Not quite right. Python has no access check at all. | correct | unit basis: first row of quiz[1] |
| l10-invariants | quiz[1].explain.text | In Python `_bid` only signals "leave this alone"; the assignment runs. C++ `private` is checked by … | correct | unit basis: first row of quiz[1] |
| l10-invariants | quiz[2].prose | ```cpp class Quote { public: Quote(double b, double a) : bid_(b), ask_(a) {} double spread() { retu… | correct | run under the app compiler and grader: the quoted clang text (check l10.quiz2) |
| l10-invariants | quiz[2].widget.options[0] | key: Write `double spread() const` | correct | unit basis: first row of quiz[2] |
| l10-invariants | quiz[2].widget.options[1].why | wrong option: Take `Quote& q` in `width` instead :: That compiles, but now `width` could change the… | correct | unit basis: first row of quiz[2] |
| l10-invariants | quiz[2].widget.options[2].why | wrong option: Make `bid_` and `ask_` public :: The error is about a promise not to change the objec… | correct | unit basis: first row of quiz[2] |
| l10-invariants | quiz[2].widget.options[3].why | wrong option: Take `Quote q` by value in `width` :: That compiles by copying the quote on every cal… | correct | unit basis: first row of quiz[2] |
| l10-invariants | quiz[2].feedback.correct | A reader should say it only reads. | correct | unit basis: first row of quiz[2] |
| l10-invariants | quiz[2].feedback.generic | Not quite right. The message says the function is not marked const. | correct | unit basis: first row of quiz[2] |
| l10-invariants | quiz[2].explain.text | A `const Quote&` may call only `const` functions, since only they promise not to change it. `spread… | correct | unit basis: first row of quiz[2] |
| l10-invariants | quiz[3].prose | A position holds 200 shares at £5.00. You buy 50 at £6.00, then sell 100. | correct | (200 x 5 + 50 x 6) / 250 = 5.2; slips 5.5 and 6.0 |
| l10-invariants | quiz[3].widget.answer | key: 5.2 (What is the average price after the sale, in pounds?) | correct | unit basis: first row of quiz[3] |
| l10-invariants | quiz[3].widget.accept | accept: £5.20: $(200 \times 5 + 50 \times 6) / 250$; the sale leaves it unchanged. | correct | unit basis: first row of quiz[3] |
| l10-invariants | quiz[3].widget.wrong[0] | slip: 5.5 (simple) | correct | unit basis: first row of quiz[3] |
| l10-invariants | quiz[3].widget.wrong[1] | slip: 6.0 (sold) | correct | unit basis: first row of quiz[3] |
| l10-invariants | quiz[3].feedback.correct | £1,300 over 250 shares is £5.20, and selling leaves it there. | correct | unit basis: first row of quiz[3] |
| l10-invariants | quiz[3].feedback.generic | Not quite right. Weight the two buys by their shares; the sale changes only the quantity. | correct | unit basis: first row of quiz[3] |
| l10-invariants | quiz[3].feedback.byKey.simple | You averaged £5.00 and £6.00. Four times as many shares cost £5.00. | correct | unit basis: first row of quiz[3] |
| l10-invariants | quiz[3].feedback.byKey.sold | That is the last buy's price. The average covers all 250 shares bought. | correct | unit basis: first row of quiz[3] |
| l10-invariants | quiz[3].explain.text | The buys give $(1000 + 300) / 250 = 5.2$. Selling 100 shares leaves 150 at the same average cost, £… | correct | unit basis: first row of quiz[3] |
| l10-invariants | summary.ideas[0] | A `class` keeps its data `private`, so only its own member functions can change it. Python's `_name… | correct | restates s2, s3, s6, s7; the average formula is s4's |
| l10-invariants | summary.ideas[1] | An invariant is checked in the constructor and again in every function that changes the data. Funct… | correct | unit basis: first row of summary |
| l10-invariants | summary.ideas[2] | Members are built in the initialiser list, before the constructor's body runs. A `const` member can… | imprecise | [class.mem]: a default member initialiser also gives a const member its value (check l10 summary). Finding 7 |
| l10-invariants | summary.formula | Weighted average price: \bar p_{\text{new}} = \dfrac{q\,\bar p + q_b\,p_b}{q + q_b} :: A buy of $q_… | correct | unit basis: first row of summary |
| l10-invariants | summary.trap | A setter that stores without checking lets outside code break the invariant the constructor checked… | correct | unit basis: first row of summary |
| l11-creation-destruction | screens[0].prose | A **destructor**, written `~Logger()`, runs when an object is destroyed. This `Logger` prints when … | correct | [stmt.dcl]/2, [class.dtor]: automatic objects are destroyed in reverse order of construction; run under the app compiler and grader (check l11.s0) |
| l11-creation-destruction | screens[0].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].widget.answer | key: ["oa", "ob", "w", "cb", "ca"] | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].widget.lines.oa | step: `open a` | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].widget.lines.ob | step: `open b` | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].widget.lines.w | step: `work` | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].widget.lines.cb | step: `close b` | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].widget.lines.ca | step: `close a` | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].hints[0] | hint: Both objects live until the closing brace of `main`. | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].hints[1] | hint: At this brace both are destroyed, one after the other. | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].hints[2] | hint: They go in reverse order of construction: `b` was built last, so it closes first. | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].feedback.correct | Built a, b; destroyed b, a. | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].feedback.generic | Not quite right. Ask which object was built last. | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].feedback.byKey.ca | You closed `a` first. Objects are destroyed in reverse order: `b` was built last, so it closes firs… | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].feedback.byKey.w | `work` prints while both objects are alive, before the closing brace. | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].feedback.byKey.cb | Nothing closes until `main` reaches its closing brace, after `work`. | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[0].explain.text | Objects are destroyed in reverse order of construction, like plates off a stack. `b` may depend on … | correct | unit basis: first row of screens[0] |
| l11-creation-destruction | screens[1].prose | Braces make a **scope**: a block where names live. Here `b` is declared inside an inner pair of bra… | correct | [basic.stc.auto]: the object lasts until its block ends, line 6 |
| l11-creation-destruction | screens[1].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[1].widget.answer | key: ["l6"] | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[1].hints[0] | hint: Which braces enclose the line that declares `b`? | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[1].hints[1] | hint: `b` is declared here. | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[1].hints[2] | hint: `b` lives until the closing brace of the block it was declared in. | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[1].feedback.correct | `b` dies at the end of its scope, line 6. | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[1].feedback.generic | Not quite right. Find the closing brace of the block that declares `b`. | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[1].feedback.byKey.l5 | That is the last line that uses `b`. C++ does not track uses: `b` lives until its scope's closing b… | imprecise | line 5 prints "work" and does not use b; it is the last line inside the block. Finding 8 |
| l11-creation-destruction | screens[1].feedback.byKey.l8 | That brace ends `a` and `c`. `b` was declared in the inner block, which ends earlier. | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[1].feedback.byKey.l4 | That line builds `b`. Its destructor runs when its scope ends. | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[1].feedback.byKey.l7 | By line 7 the inner block has already ended, so `b` is gone. | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[1].explain.text | An object on the stack lives until the closing brace of its scope. So `b` closes on line 6, before … | correct | unit basis: first row of screens[1] |
| l11-creation-destruction | screens[2].prose | Same program. `c` is built and never used. | correct | run under the app compiler and grader: open a, open b, work, close b, open c, close c, close a (check l11.s2) |
| l11-creation-destruction | screens[2].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].widget.answer | key: ["oa", "ob", "w", "cb", "oc", "cc", "ca"] | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].widget.lines.oa | step: `open a` | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].widget.lines.ob | step: `open b` | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].widget.lines.w | step: `work` | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].widget.lines.cb | step: `close b` | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].widget.lines.oc | step: `open c` | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].widget.lines.cc | step: `close c` | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].widget.lines.ca | step: `close a` | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].hints[0] | hint: Walk the lines from top to bottom, printing as each object starts and ends. | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].hints[1] | hint: Line 6 ends the inner scope. | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].hints[2] | hint: a, b, work, close b at line 6, then c, and at line 8 close c before close a. | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].feedback.correct | Each brace ends what it owns, newest first. | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].feedback.generic | Not quite right. Walk the lines in order and note every brace that ends a scope. | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].feedback.byKey.oc | `c` is built on line 7, after the inner scope has closed `b`. | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].feedback.byKey.ca | At the last brace both `a` and `c` are alive. `c` was built later, so it closes first. | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].feedback.byKey.cb | `b` closes at line 6, before `c` exists. | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].feedback.byKey.cc | `c` is never used, but it is still an object. Its destructor runs at the end of `main`, before `a`'… | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[2].explain.text | Line 6 closes `b`. At line 8 `c` and `a` are both alive, so they close newest first. `c` was never … | correct | unit basis: first row of screens[2] |
| l11-creation-destruction | screens[3].prose | Now write `Logger` yourself and make a program produce that shape. It reads three names. The first … | correct | run under the app compiler and grader: solution passes, starter fails; without the inner braces test 1 fails (check l11.s3) |
| l11-creation-destruction | screens[3].canvas.state.caption | caption: You type line 2; the program prints the rest. | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[3].widget | code: 4 tests; solution passes, starter fails | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[3].hints[0] | hint: The constructor prints `open` and the name; `~Logger()` prints `close` and the name. | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[3].hints[1] | hint: This line comes from the destructor of the first logger. | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[3].hints[2] | hint: In `main`: `Logger first(x);` then `{ Logger second(y); std::cout << "work\n"; }` then `Logge… | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[3].feedback.correct | The braces alone decide when each `close` prints. | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[3].feedback.generic | Not quite right. Compare your output with the expected lines under the editor. | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[3].feedback.byKey.compile | The compiler stopped. Check that the destructor is spelt `~Logger()`, with no return type and no ar… | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[3].feedback.byKey.test-1 | Compare the order of your `close` lines with the expected output. An inner pair of braces must end … | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[3].explain.text | You never call a destructor yourself. The inner braces end `second`, and the end of `main` ends `th… | correct | unit basis: first row of screens[3] |
| l11-creation-destruction | screens[4].prose | Members are built in the order they are **declared** in the class, whatever order the initialiser l… | correct | [class.base.init]/13: members are initialised in declaration order; reading n_ first is undefined: [dcl.init]/12; run under the app compiler and grader with -Wall: both warnings with positions, "2 warnings generated" (check l11.s4) |
| l11-creation-destruction | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].widget.options[0] | key: Unpredictable: `n_` is read before it is set | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].widget.options[1].why | wrong option: 20 :: You read the list left to right. `data_` is declared first, so it is built firs… | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].widget.options[2].why | wrong option: 0, because `n_` starts at zero :: An `int` member is not zeroed. Reading it before it… | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].widget.options[3].why | wrong option: A compile error :: These are warnings: the program builds. That is why they are worth… | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].hints[0] | hint: Which member is declared first, on lines 7 and 8? | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].hints[1] | hint: The second warning names the exact problem. | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].hints[2] | hint: `data_` is built first, using `n_`, which is built second. | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].feedback.correct | `data_` is built first, from an `n_` that holds garbage. | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].feedback.generic | Not quite right. Members are built in declaration order. | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].feedback.byKey.twenty | You read the list left to right. `data_` is declared first, so it is built first, from an `n_` not … | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[4].explain.text | Declaration order decides, so `data_(n_, 0.0)` reads `n_` before `n_(n)` runs. Build `data_` from t… | correct | unit basis: first row of screens[4] |
| l11-creation-destruction | screens[5].prose | Same `Logger`. Now one is made from another. ```cpp int main() { Logger a("a"); Logger b = a; } ``` | correct | [class.copy.ctor]: the implicit copy constructor copies each member; run under the app compiler and grader prints open a, close a, close a (check l11.s5) |
| l11-creation-destruction | screens[5].widget.answer | key: 2 (How many lines of output start with `close`?) | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].widget.accept | accept: 2: `open a`, `close a`, `close a`. | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].widget.wrong[0] | slip: 1 (one) | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].widget.wrong[1] | slip: 3 (three) | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].hints[0] | hint: How many `Logger` objects exist at the end of `main`? | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].hints[1] | hint: `b` is a second object holding a copy of `a`'s name. | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].hints[2] | hint: Two objects, two destructors. The copy itself printed nothing. | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].feedback.correct | Two objects, so two destructors: `close a` twice. | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].feedback.generic | Not quite right. Count the objects alive at the closing brace. | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].feedback.byKey.one | You counted one object because only one constructor printed. `b` was built by a constructor that pr… | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].feedback.byKey.three | Only two objects exist. The copy made `b`; it did not make a third. | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].explain.text | `Logger b = a;` builds `b` with the **copy constructor**, `Logger(const Logger&)`. The compiler wro… | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[5].explain.canvas.caption | caption: Two objects, two destructors | correct | unit basis: first row of screens[5] |
| l11-creation-destruction | screens[6].prose | A class has four ways to fill an object from another. The **copy constructor** builds a new object.… | correct | [dcl.init]: a declaration with = is initialisation; run under the app compiler and grader: constructor, copy constructor twice, copy assignment, move constructor, move assignment (check l11.s6) |
| l11-creation-destruction | screens[6].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].widget.answer | key: ["r1", "r2"] | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].hints[0] | hint: Does the line declare a new object, or change one that exists? | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].hints[1] | hint: On this line `b` already exists. | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].hints[2] | hint: Lines that declare a new `Buffer` from `a` build it: `Buffer b = a;` and `Buffer c(a);`. | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].feedback.correct | A declaration builds; a plain `=` overwrites. | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].feedback.generic | Not quite right. Ask whether each line makes a new object. | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].feedback.byKey.r3 | `b` already exists on this line, so `=` overwrites it: that is copy assignment, not construction. | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].feedback.byKey.r4 | `std::move(a)` lets the new object take `a`'s contents: the move constructor runs. | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].feedback.byKey.r5 | `c` exists and takes `b`'s contents: move assignment. | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].feedback.byKey.r0 | That builds a `Buffer` from two numbers: an ordinary constructor. | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].feedback.byKey.r1 | `Buffer b = a;` declares `b`, so it builds a new object. The `=` in a declaration is not assignment… | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].explain.text | A declaration always builds, even when it is written with `=`. Assignment needs an object that alre… | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[6].explain.canvas.values | canvas: {"r0c1": "constructor", "r1c1": "copy constructor", "r2c1": "copy constructor", "r3c1": "co… | correct | unit basis: first row of screens[6] |
| l11-creation-destruction | screens[7].prose | A `std::vector` member already copies its doubles on a copy and hands over its heap block on a move… | correct | [class.copy.ctor]/8, [class.copy.assign]/4: declared moves delete the implicit copies; run under the app compiler and grader: solution and the rule-of-zero form pass; the four named slips fail first at tests 5, 9, 10 and 12 (checks l11.s7); [container.requirements], [lib.types.movedfrom] |
| l11-creation-destruction | screens[7].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].widget | code: 12 tests; solution passes, starter fails | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].hints[0] | hint: Build `data_` in the initialiser list: `data_(n, x)`. | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].hints[1] | hint: After a move, the source is left empty. | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].hints[2] | hint: `Buffer(const Buffer&) = default;`, `Buffer(Buffer&&) = default;`, and `Buffer& operator=(con… | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].feedback.correct | The vector did the work; you only asked for it. | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].feedback.byKey.test-2 | Test 2 changes `b` and reads `a`. A copy must not share doubles with its source. | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].feedback.byKey.test-5 | Test 5 reads `a.size()` after a move and expects 0. A moved vector leaves its source empty. | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].feedback.byKey.test-9 | Test 9 assigns one buffer to another. A declared move constructor deletes the copy assignment, so d… | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].feedback.byKey.test-10 | Test 10 asks whether one `Buffer` can be move-assigned to another, and a deleted move assignment sa… | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].feedback.byKey.test-12 | Test 12 moves `a` into an existing buffer and expects `a` empty. Without a move assignment, `a` was… | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[7].explain.text | A copy duplicates the doubles; a move passes the heap block over, so a million doubles cost one poi… | correct | unit basis: first row of screens[7] |
| l11-creation-destruction | screens[8].prose | This class owns a heap block through a raw pointer, and frees it in its destructor. Then it is copi… | correct | the implicit copy copies the pointer; deleting twice is undefined: [expr.delete]; run, g++: aborts with a double free (check l11.s8) |
| l11-creation-destruction | screens[8].widget.options[0] | key: Both destructors `delete[]` the same block: undefined behaviour, which usually crashes a desk … | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].widget.options[1].why | wrong option: `b` has its own 100 doubles, so each destructor frees its own :: You expected the cop… | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].widget.options[2].why | wrong option: A compile error: `Prices` has no copy constructor :: The compiler writes one for you.… | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].widget.options[3].why | wrong option: The block leaks, because nobody frees it :: Each destructor frees it, so it is freed … | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].hints[0] | hint: What is the member that the default copy copies? | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].hints[1] | hint: Draw the arrow for `b` after the copy. | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].hints[2] | hint: `data_` is an address. `b` gets the same address, so two destructors free one block. | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].feedback.correct | Copying a raw pointer copies an address, not the doubles. | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].feedback.generic | Not quite right. Ask what the default copy does with `data_`. | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].feedback.byKey.deep | You expected the copy to copy the doubles. The default copy constructor copies the member, a pointe… | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].explain.text | `b.data_` holds the same address as `a.data_`, so the block is freed twice. The fix is to own it wi… | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[8].explain.canvas.caption | caption: Two owners: `delete[]` runs twice | correct | unit basis: first row of screens[8] |
| l11-creation-destruction | screens[9].prose | Five **special members** decide how an object is copied, moved and destroyed. You choose between tw… | correct | rule of zero and rule of five (C++ Core Guidelines C.20, C.21); run under the app compiler and grader: a unique_ptr member makes the class move-only (checks review-3.6) |
| l11-creation-destruction | screens[9].widget.options[0] | key: Nothing. Copies are refused because `unique_ptr` cannot be copied, and moves work. | correct | unit basis: first row of screens[9] |
| l11-creation-destruction | screens[9].widget.options[1].why | wrong option: All five special members, by hand :: That is for a class that owns a raw resource its… | correct | unit basis: first row of screens[9] |
| l11-creation-destruction | screens[9].widget.options[2].why | wrong option: A destructor that calls `delete grid_.get()` :: `unique_ptr` already deletes the latt… | correct | unit basis: first row of screens[9] |
| l11-creation-destruction | screens[9].widget.options[3].why | wrong option: A copy constructor that copies the pointer :: Two pricers would then share one lattic… | correct | unit basis: first row of screens[9] |
| l11-creation-destruction | screens[9].hints[0] | hint: Does any member need help to be copied, moved or destroyed? | correct | unit basis: first row of screens[9] |
| l11-creation-destruction | screens[9].hints[1] | hint: `std::string` and `std::unique_ptr` each handle their own copying, moving and destruction. | correct | unit basis: first row of screens[9] |
| l11-creation-destruction | screens[9].feedback.correct | Rule of zero: the members already do the right thing. | correct | unit basis: first row of screens[9] |
| l11-creation-destruction | screens[9].feedback.generic | Not quite right. Check what each member does on its own. | correct | unit basis: first row of screens[9] |
| l11-creation-destruction | screens[9].explain.text | Self-managing members make the compiler's versions right: moves move, and the copy is deleted becau… | correct | unit basis: first row of screens[9] |
| l11-creation-destruction | screens[10].prose | A market-data connection must disconnect exactly once, in its destructor. A copy would disconnect t… | correct | run under the app compiler and grader: solution passes; the three named slips fail first at tests 2, 8 and 1; a declared move constructor alone already deletes the copy (checks l11.s10) |
| l11-creation-destruction | screens[10].canvas.state.caption | caption: After the move, only `b` is open. | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | screens[10].widget | code: 9 tests; solution passes, starter fails | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | screens[10].hints[0] | hint: The destructor calls `disconnect(venue_)` only while `open_` is true. | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | screens[10].hints[1] | hint: After the move, `a` must be closed. | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | screens[10].hints[2] | hint: `Connection(Connection&& other) noexcept : venue_(std::move(other.venue_)), open_(other.open_… | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | screens[10].feedback.correct | One open connection, one disconnect, wherever it moves. | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | screens[10].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | screens[10].feedback.byKey.test-2 | Test 2 moves `a` into `b`; both destructors run. Leave `other.open_` false in the move constructor. | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | screens[10].feedback.byKey.test-8 | Test 8 asks whether `Connection` can be copied. Write `Connection(const Connection&) = delete;`. | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | screens[10].feedback.byKey.test-1 | Test 1 builds one connection and expects one disconnect. Call `disconnect(venue_)` in `~Connection(… | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | screens[10].explain.text | The move constructor takes the venue and closes the source, so only one destructor disconnects. Del… | correct | unit basis: first row of screens[10] |
| l11-creation-destruction | quiz[0].prose | Same `Logger`, with `open` and `close` messages. ```cpp int main() { Logger("tmp"); std::cout << "n… | correct | [class.temporary]/4: a temporary is destroyed at the end of the full expression; run under the app compiler and grader (check l11.quiz0) |
| l11-creation-destruction | quiz[0].widget.options[0] | key: `open tmp`, `close tmp`, `next` | correct | unit basis: first row of quiz[0] |
| l11-creation-destruction | quiz[0].widget.options[1].why | wrong option: `open tmp`, `next`, `close tmp` :: A temporary has no name, so it does not live to th… | correct | unit basis: first row of quiz[0] |
| l11-creation-destruction | quiz[0].widget.options[2].why | wrong option: `next` only :: The temporary is really built, so both its constructor and its destruc… | correct | unit basis: first row of quiz[0] |
| l11-creation-destruction | quiz[0].widget.options[3].why | wrong option: `open tmp`, `next` :: Every object that is built is destroyed. The temporary's destru… | correct | unit basis: first row of quiz[0] |
| l11-creation-destruction | quiz[0].feedback.correct | A temporary dies at the end of its full expression. | correct | unit basis: first row of quiz[0] |
| l11-creation-destruction | quiz[0].feedback.generic | Not quite right. A temporary has no scope of its own. | correct | unit basis: first row of quiz[0] |
| l11-creation-destruction | quiz[0].explain.text | `Logger("tmp");` builds an unnamed object and destroys it at the semicolon. So `close tmp` prints b… | correct | unit basis: first row of quiz[0] |
| l11-creation-destruction | quiz[1].prose | `Buffer` is the class you wrote, with default copy and move constructors. ```cpp const Buffer a(3, … | correct | [over.match]: const Buffer&& does not bind Buffer&&, so the copy constructor is chosen; run under the app compiler and grader prints 3 (check l11.quiz1) |
| l11-creation-destruction | quiz[1].widget.options[0] | key: `3` | correct | unit basis: first row of quiz[1] |
| l11-creation-destruction | quiz[1].widget.options[1].why | wrong option: `0` :: `std::move` only casts. On a `const` object it gives `const Buffer&&`, which t… | correct | unit basis: first row of quiz[1] |
| l11-creation-destruction | quiz[1].widget.options[2].why | wrong option: A compile error: you cannot move from a `const` object :: It compiles. The copy const… | correct | unit basis: first row of quiz[1] |
| l11-creation-destruction | quiz[1].feedback.correct | A `const` object cannot be moved from, so it is copied. | correct | unit basis: first row of quiz[1] |
| l11-creation-destruction | quiz[1].feedback.generic | Not quite right. A move must change its source. | correct | unit basis: first row of quiz[1] |
| l11-creation-destruction | quiz[1].explain.text | A move empties its source, and `a` is `const`, so the copy constructor runs instead. `a` keeps its … | correct | unit basis: first row of quiz[1] |
| l11-creation-destruction | quiz[2].prose | A pricer's lattice holds 500 doubles. `Lattice` has a copy constructor and a move constructor. ```c… | correct | [class.copy.elision]; run under the app compiler and grader: 0 copies (check l11.quiz2) |
| l11-creation-destruction | quiz[2].widget.options[0] | key: 0 | correct | unit basis: first row of quiz[2] |
| l11-creation-destruction | quiz[2].widget.options[1].why | wrong option: 1 :: You expected `return grid;` to copy. A returned local is moved, or built straigh… | correct | unit basis: first row of quiz[2] |
| l11-creation-destruction | quiz[2].widget.options[2].why | wrong option: 2 :: Neither the return nor `Lattice g = ...` copies. C++17 builds `g` straight from … | correct | unit basis: first row of quiz[2] |
| l11-creation-destruction | quiz[2].feedback.correct | `return grid;` does not copy a movable local: it is built in place or moved. | correct | unit basis: first row of quiz[2] |
| l11-creation-destruction | quiz[2].feedback.generic | Not quite right. A returned local is moved or built in place. | correct | unit basis: first row of quiz[2] |
| l11-creation-destruction | quiz[2].explain.text | The compiler usually builds `grid` directly in `g`'s place; if not, it moves it. Either way no doub… | correct | unit basis: first row of quiz[2] |
| l11-creation-destruction | quiz[3].prose | ```cpp class Desk { Logger risk_; Logger feed_; public: Desk() : feed_("feed"), risk_("risk") {} };… | correct | [class.base.init]/13; run under the app compiler and grader prints open risk first, then close feed, close risk (check l11.quiz3) |
| l11-creation-destruction | quiz[3].widget.options[0] | key: `open risk` | correct | unit basis: first row of quiz[3] |
| l11-creation-destruction | quiz[3].widget.options[1].why | wrong option: `open feed` :: You followed the initialiser list. Members are built in declaration or… | correct | unit basis: first row of quiz[3] |
| l11-creation-destruction | quiz[3].widget.options[2].why | wrong option: `close feed` :: Nothing closes until `d` is destroyed at the end of `main`. | correct | unit basis: first row of quiz[3] |
| l11-creation-destruction | quiz[3].feedback.correct | Declaration order, not list order. | correct | unit basis: first row of quiz[3] |
| l11-creation-destruction | quiz[3].feedback.generic | Not quite right. Look at the order of the member declarations. | correct | unit basis: first row of quiz[3] |
| l11-creation-destruction | quiz[3].explain.text | `risk_` is declared first, so it is built first, whatever the list says. At the end the order rever… | correct | unit basis: first row of quiz[3] |
| l11-creation-destruction | summary.ideas[0] | A destructor runs when its object's scope ends, in reverse order of construction. A temporary dies … | correct | restates s0, s4, s6, s8, s9 |
| l11-creation-destruction | summary.ideas[1] | `T b = a;` builds `b` with the copy constructor; `b = a;` on an existing `b` is copy assignment. `s… | correct | unit basis: first row of summary |
| l11-creation-destruction | summary.ideas[2] | Rule of zero: hold members that manage themselves (`std::vector`, `std::string`, `std::unique_ptr`)… | correct | unit basis: first row of summary |
| l11-creation-destruction | summary.formula | Order of destruction: \text{built } a, b, c \quad\Rightarrow\quad \text{destroyed } c, b, a :: With… | correct | unit basis: first row of summary |
| l11-creation-destruction | summary.trap | A class holding a raw pointer gets a default copy that copies the address, so two destructors free … | correct | unit basis: first row of summary |
| l12-operators | screens[0].prose | In Python, `a + b` on your own class calls `a.__add__(b)`. Here are two amounts in C++, held as who… | correct | [over.oper]: an operator on a class type needs an operator function; run under the app compiler and grader: 10:23 "invalid operands to binary expression ('Money' and 'Money')", 1 error (check l12.s0) |
| l12-operators | screens[0].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].widget.options[0] | key: A function named `operator+` that takes two `Money` values | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].widget.options[1].why | wrong option: A member function named `__add__` :: That is Python's name. C++ looks for a function … | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].widget.options[2].why | wrong option: Nothing: `+` should add the members :: C++ does not guess what adding a class means. … | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].widget.options[3].why | wrong option: Make `pence_` public :: Access is not the problem. The error says `+` has no meaning … | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].hints[0] | hint: Read the error: which operands does `+` not understand? | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].hints[1] | hint: The two operand types are named here. | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].hints[2] | hint: You define `+` for a type by writing a function called `operator+`. | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].feedback.correct | C++ spells `__add__` as `operator+`. | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].feedback.generic | Not quite right. The error says `+` is not defined for two `Money` values. | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].feedback.byKey.auto | C++ does not guess what adding a class means. Only built-in types have `+` ready-made. | correct | unit basis: first row of screens[0] |
| l12-operators | screens[0].explain.text | `fee + tax` is a call to `operator+(fee, tax)`, and none exists yet. Writing one is **operator over… | correct | unit basis: first row of screens[0] |
| l12-operators | screens[1].prose | `str()` should show pence as pounds: 1234 becomes `£12.34`. A first try joins `pence_ / 100`, a dot… | correct | run under the app compiler and grader: the first try prints the six texts keyed (check l12.s1); [expr.mul]/4: / and % truncate towards zero |
| l12-operators | screens[1].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].widget.answer | key: ["r1", "r2", "r3", "r5"] | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].hints[0] | hint: `std::to_string(5)` is `"5"`, with no leading zero. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].hints[1] | hint: Try this row: 1205 / 100 is 12, and 1205 % 100 is 5. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].hints[2] | hint: Any remainder below 10 loses its zero. For −150, both `/` and `%` are negative: `£-1.-50`. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].feedback.correct | Small remainders lose their zero, and negatives go wrong twice. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].feedback.generic | Not quite right. Work out `pence_ / 100` and `pence_ % 100` for each row. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].feedback.byKey.r0 | 1234 gives 12 and 34, so `£12.34`: that one is right. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].feedback.byKey.r4 | 99 gives 0 and 99, so `£0.99`: that one is right. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].feedback.byKey.r1 | 1205 % 100 is 5, and `std::to_string(5)` is `"5"`: the first try prints `£12.5`. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].feedback.byKey.r2 | 1200 % 100 is 0, printed as `"0"`: the first try prints `£12.0`. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].feedback.byKey.r3 | 7 / 100 is 0 and 7 % 100 is 7: the first try prints `£0.7`. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].feedback.byKey.r5 | −150 / 100 is −1 and −150 % 100 is −50 (both round towards zero): the first try prints `£-1.-50`. | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].explain.text | A remainder below 10 needs a leading zero. For a negative amount, format the absolute value and put… | correct | unit basis: first row of screens[1] |
| l12-operators | screens[1].explain.canvas.values | canvas: {"r0c1": "£12.34", "r1c1": "£12.5", "r2c1": "£12.0", "r3c1": "£0.7", "r4c1": "£0.99", "r5c1… | correct | unit basis: first row of screens[1] |
| l12-operators | screens[2].prose | Now write the operators. An arithmetic operator takes its operands by value and **returns a new val… | correct | run under the app compiler and grader: solution passes; no padding fails test 2, no sign handling test 8, a missing operator* gives "invalid operands" (checks l12.s2); the pound sign is C2 A3 in UTF-8 |
| l12-operators | screens[2].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[2] |
| l12-operators | screens[2].widget | code: 11 tests; solution passes, starter fails | correct | unit basis: first row of screens[2] |
| l12-operators | screens[2].hints[0] | hint: Work with the absolute value, then put `-` in front when `pence_` is negative. | correct | unit basis: first row of screens[2] |
| l12-operators | screens[2].hints[1] | hint: Rows 2 to 4 need a leading zero on the pence. | correct | unit basis: first row of screens[2] |
| l12-operators | screens[2].hints[2] | hint: `std::string cents = std::to_string(p % 100); if (cents.size() < 2) cents = "0" + cents;` and… | correct | unit basis: first row of screens[2] |
| l12-operators | screens[2].feedback.correct | Whole pence in, exact text out. | correct | unit basis: first row of screens[2] |
| l12-operators | screens[2].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[2] |
| l12-operators | screens[2].feedback.byKey.compile | The compiler stopped. If it says `invalid operands`, an operator is missing or its parameters do no… | correct | unit basis: first row of screens[2] |
| l12-operators | screens[2].feedback.byKey.test-2 | Test 2 expects `£12.05`. Pad a remainder below 10 with a `0`. | correct | unit basis: first row of screens[2] |
| l12-operators | screens[2].feedback.byKey.test-8 | Test 8 expects `-£1.50`. Format the absolute value and put the minus sign before the `£`. | correct | unit basis: first row of screens[2] |
| l12-operators | screens[2].explain.text | Both operators build and return a new `Money`, so `a + b` leaves `a` and `b` alone. `str()` formats… | correct | unit basis: first row of screens[2] |
| l12-operators | screens[3].prose | An operator can also be a **member** function: then the object is always its left operand. This `Mo… | correct | [over.match.oper]: a member operator takes the object as its left operand; run under the app compiler and grader: 12:17 "('int' and 'Money')", 1 error; the free operator*(int, Money) compiles, (Money, int) does not help (checks l12.s3) |
| l12-operators | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].widget.options[0] | key: A free function `Money operator*(int k, Money m)` | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].widget.options[1].why | wrong option: Another member, `Money operator*(int k) const` :: A member operator always has the ob… | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].widget.options[2].why | wrong option: A free function `Money operator*(Money m, int k)` :: That is `fee * 3` again. The par… | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].widget.options[3].why | wrong option: None: C++ cannot put a class on the right of `*` :: A free function can take its oper… | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].hints[0] | hint: For a member, which operand is the object? | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].hints[1] | hint: In line 12 the left operand is an `int`. | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].hints[2] | hint: Only a free function can have an `int` as its first parameter. | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].feedback.correct | A free function puts the `int` first. | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].feedback.generic | Not quite right. Match the parameters to the operands, left to right. | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].feedback.byKey.member | A member operator always has the object on the left, so it only ever gives `fee * 3`. | correct | unit basis: first row of screens[3] |
| l12-operators | screens[3].explain.text | `fee * 3` calls `fee.operator*(3)`, but `3 * fee` needs a function whose first parameter is an `int… | correct | unit basis: first row of screens[3] |
| l12-operators | screens[4].prose | Python prints an object through `__repr__`. C++ prints through `operator<<`, which takes the stream… | imprecise | print() calls str(), which uses __str__ and falls back to __repr__ (Python data model 3.3.1). Finding 9 |
| l12-operators | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | << groups left to right: [expr.shift]; streams are not copyable: [ostream.cons]; run under the app compiler and grader prints the chained line; a by-value stream gives a deleted-constructor error (checks l12.s4) |
| l12-operators | screens[4].widget.options[0] | key: So the next `<<` in the chain has a stream to write to | correct | unit basis: first row of screens[4] |
| l12-operators | screens[4].widget.options[1].why | wrong option: To hand back a copy of the stream :: It returns a reference. Streams cannot be copied… | correct | unit basis: first row of screens[4] |
| l12-operators | screens[4].widget.options[2].why | wrong option: To report whether the write worked :: The stream records errors itself. The returned … | correct | unit basis: first row of screens[4] |
| l12-operators | screens[4].widget.options[3].why | wrong option: Because Python's `__repr__` returns a string :: `operator<<` writes to the stream rat… | correct | unit basis: first row of screens[4] |
| l12-operators | screens[4].hints[0] | hint: `a << b << c` is read as `(a << b) << c`. | correct | unit basis: first row of screens[4] |
| l12-operators | screens[4].hints[1] | hint: The left operand of the second `<<` is whatever the first one returned. | correct | unit basis: first row of screens[4] |
| l12-operators | screens[4].hints[2] | hint: The first call must return the stream itself, so the second call writes to the same stream. | correct | unit basis: first row of screens[4] |
| l12-operators | screens[4].feedback.correct | Each `<<` hands the stream to the next. | correct | unit basis: first row of screens[4] |
| l12-operators | screens[4].feedback.generic | Not quite right. Read `std::cout << x << y` as two calls, one inside the other. | correct | unit basis: first row of screens[4] |
| l12-operators | screens[4].explain.text | `std::cout << a << b` is `operator<<(operator<<(std::cout, a), b)`. Returning `os` by reference kee… | correct | unit basis: first row of screens[4] |
| l12-operators | screens[5].prose | A colleague's `+` saves a copy by working on the left operand directly. | correct | the first parameter is a reference to cash; run under the app compiler and grader prints 1250 1250 (check l12.s5) |
| l12-operators | screens[5].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].widget.options[0] | key: `1250 1250` | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].widget.options[1].why | wrong option: `1000 1250` :: You expected `+` to leave `cash` alone, as built-in `+` does. This one… | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].widget.options[2].why | wrong option: A compile error: `+` must return a value :: It returns `Money&`, which compiles. The … | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].widget.options[3].why | wrong option: `1250 1000` :: `total` is a copy of the changed `cash`, so it also holds 1250. | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].hints[0] | hint: Look at the type of the first parameter. | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].hints[1] | hint: This line writes into `a`, which is `cash` itself. | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].hints[2] | hint: `cash + fee` adds 250 into `cash`, then `total` copies it: both are 1250. | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].feedback.correct | This `+` changed `cash`: a `+=` in disguise. | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].feedback.generic | Not quite right. Follow `a` back to `cash`. | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].feedback.byKey.pure | You expected `+` to leave `cash` alone, as built-in `+` does. This one takes `a` by non-const refer… | correct | unit basis: first row of screens[5] |
| l12-operators | screens[5].explain.text | `Money& a` is `cash` itself, so the sum is written into it. A reader of `cash + fee` never expects … | correct | unit basis: first row of screens[5] |
| l12-operators | screens[6].prose | A first `Price` type stores pounds in a `double`. Its `operator==` compares them directly. | correct | IEEE 754: 0.1 + 0.2 is not 0.3; run under the app compiler and grader prints 0 (check l12.s5, s6) |
| l12-operators | screens[6].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[6] |
| l12-operators | screens[6].widget.options[0] | key: `0` | correct | unit basis: first row of screens[6] |
| l12-operators | screens[6].widget.options[1].why | wrong option: `1` :: You expected 0.1 + 0.2 to equal 0.3. In binary it is 0.30000000000000004, so `… | correct | unit basis: first row of screens[6] |
| l12-operators | screens[6].widget.options[2].why | wrong option: A compile error: `==` needs `const` references :: Taking `Price` by value is fine for… | correct | unit basis: first row of screens[6] |
| l12-operators | screens[6].hints[0] | hint: Is 0.1 + 0.2 exactly 0.3 as a `double`? | correct | unit basis: first row of screens[6] |
| l12-operators | screens[6].hints[1] | hint: This line compares two doubles bit for bit. | correct | unit basis: first row of screens[6] |
| l12-operators | screens[6].hints[2] | hint: 0.1 + 0.2 is 0.30000000000000004, so the comparison is false and prints 0. | correct | unit basis: first row of screens[6] |
| l12-operators | screens[6].feedback.correct | `==` on doubles is exact, and binary fractions are not. | correct | unit basis: first row of screens[6] |
| l12-operators | screens[6].feedback.generic | Not quite right. Work out 0.1 + 0.2 in binary floating point. | correct | unit basis: first row of screens[6] |
| l12-operators | screens[6].feedback.byKey.one | You expected 0.1 + 0.2 to equal 0.3. In binary it is 0.30000000000000004, so `==` says no. | correct | unit basis: first row of screens[6] |
| l12-operators | screens[6].explain.text | The fill and the limit print as equal but differ in the last bit. Python's `__eq__` on floats has t… | correct | unit basis: first row of screens[6] |
| l12-operators | screens[7].prose | `std::sort` orders a vector using `<`. So a `Price` in whole pence needs `operator<`. Its `==` must… | correct | [alg.sorting]: the comparison must be a strict weak ordering; run under the app compiler and grader: solution passes; `<=` fails test 5 first, venue in == fails test 7 (checks l12.s7) |
| l12-operators | screens[7].canvas.state.caption | caption: Ask prices in pounds, before sorting | correct | unit basis: first row of screens[7] |
| l12-operators | screens[7].widget | code: 8 tests; solution passes, starter fails | correct | unit basis: first row of screens[7] |
| l12-operators | screens[7].hints[0] | hint: Compare the `pence` members. | correct | unit basis: first row of screens[7] |
| l12-operators | screens[7].hints[1] | hint: The smallest goes first after sorting. | correct | unit basis: first row of screens[7] |
| l12-operators | screens[7].hints[2] | hint: `return a.pence < b.pence;` and `return a.pence == b.pence;`. | correct | unit basis: first row of screens[7] |
| l12-operators | screens[7].feedback.correct | `std::sort` now orders your type. | correct | unit basis: first row of screens[7] |
| l12-operators | screens[7].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[7] |
| l12-operators | screens[7].feedback.byKey.test-5 | Test 5 asks whether a price is less than itself, and expects false. Use `<`, not `<=`: `std::sort` … | correct | unit basis: first row of screens[7] |
| l12-operators | screens[7].feedback.byKey.test-7 | Test 7 compares the same pence at two venues and expects true. Compare pence only, as `<` does. | correct | unit basis: first row of screens[7] |
| l12-operators | screens[7].explain.text | `std::sort` calls your `operator<` for every comparison it makes. It must be strict: `a < a` is fal… | correct | unit basis: first row of screens[7] |
| l12-operators | screens[7].explain.canvas.caption | caption: After `std::sort` | correct | unit basis: first row of screens[7] |
| l12-operators | screens[8].prose | Each Python special method has a C++ operator. `__add__` is `operator+`, `__eq__` is `operator==`, … | imprecise | as screens[4]: __str__ is the closer match for operator<<. Finding 9 |
| l12-operators | screens[8].widget.options[0] | key: `Money operator-(Money a, Money b)` | correct | operator shapes as in s2 to s7 (C++ Core Guidelines C.160, C.161) |
| l12-operators | screens[8].widget.options[1].why | wrong option: `Money& operator-(Money& a, Money b)` :: That writes into the left operand, the trap … | correct | unit basis: first row of screens[8] |
| l12-operators | screens[8].widget.options[2].why | wrong option: `void operator-(Money a, Money b)` :: Then `a - b` would have no value to store or pr… | correct | unit basis: first row of screens[8] |
| l12-operators | screens[8].widget.options[3].why | wrong option: `Money operator-(Money a)` :: One parameter makes unary minus, `-a`, not subtraction. | correct | unit basis: first row of screens[8] |
| l12-operators | screens[8].hints[0] | hint: Which shape does `+` have? | correct | unit basis: first row of screens[8] |
| l12-operators | screens[8].hints[1] | hint: Subtraction is binary and pure, like `+`: two values in, a new value out. | correct | unit basis: first row of screens[8] |
| l12-operators | screens[8].feedback.correct | Two values in, one new value out. | correct | unit basis: first row of screens[8] |
| l12-operators | screens[8].feedback.generic | Not quite right. Copy the shape of `operator+`. | correct | unit basis: first row of screens[8] |
| l12-operators | screens[8].explain.text | `-` has the same shape as `+`: two `Money` values in, a new one out. Arithmetic returns by value, c… | correct | unit basis: first row of screens[8] |
| l12-operators | screens[9].prose | An exchange fills resting sell orders by **price-time priority**: the lowest ask first, and at the … | correct | [tuple.rel]: tuples compare lexicographically; price-time priority: Harris, Trading and Exchanges (2003) ch. 6, the rule on LSE and Cboe order books; run under the app compiler and grader: solution passes; time-only gives C, A, B and price-only B, A, C on test 1 (checks l12.s9) |
| l12-operators | screens[9].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[9] |
| l12-operators | screens[9].widget | code: 7 tests; solution passes, starter fails | correct | unit basis: first row of screens[9] |
| l12-operators | screens[9].hints[0] | hint: Compare prices first; look at times only when the prices are equal. | correct | unit basis: first row of screens[9] |
| l12-operators | screens[9].hints[1] | hint: A and C share a price; C arrived first. | correct | unit basis: first row of screens[9] |
| l12-operators | screens[9].hints[2] | hint: `return std::tie(a.price, a.time) < std::tie(b.price, b.time);` | correct | unit basis: first row of screens[9] |
| l12-operators | screens[9].feedback.correct | B, then C, then A: price first, time second. | correct | unit basis: first row of screens[9] |
| l12-operators | screens[9].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[9] |
| l12-operators | screens[9].feedback.byKey.test-1 | Test 1 expects B, C, A: B is cheapest, and C arrived before A at the same price. If you got C, A, B… | correct | unit basis: first row of screens[9] |
| l12-operators | screens[9].explain.text | `std::tie` compares price first and falls through to time only on a tie. For bids you would flip th… | correct | unit basis: first row of screens[9] |
| l12-operators | screens[9].explain.canvas.caption | caption: Trading order: B, C, A | correct | unit basis: first row of screens[9] |
| l12-operators | quiz[0].prose | ```cpp struct Px { long long pence; std::string venue; }; bool operator<(const Px& a, const Px& b) … | correct | run under the app compiler and grader prints 000 (check l12.quiz0); equivalence under < against ==: [alg.sorting]/7 |
| l12-operators | quiz[0].widget.options[0] | key: `000`: `<` treats them as the same, `==` does not | correct | unit basis: first row of quiz[0] |
| l12-operators | quiz[0].widget.options[1].why | wrong option: `001` :: `==` also compares the venue, and LSE is not CBOE, so it is false. | correct | unit basis: first row of quiz[0] |
| l12-operators | quiz[0].widget.options[2].why | wrong option: `100` :: Both have 100 pence, so neither is less than the other. | correct | unit basis: first row of quiz[0] |
| l12-operators | quiz[0].widget.options[3].why | wrong option: `000`, which is consistent :: If neither is less than the other, a sort treats them a… | correct | unit basis: first row of quiz[0] |
| l12-operators | quiz[0].feedback.correct | Neither is less, yet they are not equal: the two operators disagree. | correct | unit basis: first row of quiz[0] |
| l12-operators | quiz[0].feedback.generic | Not quite right. Work out each comparison, then ask whether they agree. | correct | unit basis: first row of quiz[0] |
| l12-operators | quiz[0].explain.text | A sort treats `a` and `b` as equivalent, but `==` calls them different. So a search after a sort ca… | correct | unit basis: first row of quiz[0] |
| l12-operators | quiz[1].prose | ```cpp struct Pnl { long long pence; }; struct Quantity { int shares; }; Pnl operator+(Pnl a, Pnl b… | correct | [over.match.oper]: no viable operator+; run under the app compiler and grader does not compile (check l12.quiz1) |
| l12-operators | quiz[1].widget.options[0] | key: A compile error: no `operator+` takes a `Pnl` and a `Quantity` | correct | unit basis: first row of quiz[1] |
| l12-operators | quiz[1].widget.options[1].why | wrong option: `oops.pence` is 12800 :: You expected C++ to add the numbers inside. It looks for an … | correct | unit basis: first row of quiz[1] |
| l12-operators | quiz[1].widget.options[2].why | wrong option: The `Quantity` converts to `Pnl` first :: There is no conversion from `Quantity` to `… | correct | unit basis: first row of quiz[1] |
| l12-operators | quiz[1].feedback.correct | Separate types turn a unit mistake into a compile error. | correct | unit basis: first row of quiz[1] |
| l12-operators | quiz[1].feedback.generic | Not quite right. Which `operator+` exists? | correct | unit basis: first row of quiz[1] |
| l12-operators | quiz[1].explain.text | The only `operator+` takes two `Pnl` values, and a `Quantity` is not one. With plain `long long` an… | correct | unit basis: first row of quiz[1] |
| l12-operators | quiz[2].prose | ```cpp std::ostream& operator<<(std::ostream os, const Money& m) { os << m.str(); return os; } std:… | correct | [ostream.cons]: the copy constructor is deleted; run under the app compiler and grader (check l12.s4 / quiz2) |
| l12-operators | quiz[2].widget.options[0] | key: A compile error: the stream's copy constructor is deleted | correct | unit basis: first row of quiz[2] |
| l12-operators | quiz[2].widget.options[1].why | wrong option: It prints `£12.50` :: Taking `os` by value would copy `std::cout`. Streams cannot be … | correct | unit basis: first row of quiz[2] |
| l12-operators | quiz[2].widget.options[2].why | wrong option: It prints nothing, because it writes to a copy :: It never gets that far. Copying a s… | correct | unit basis: first row of quiz[2] |
| l12-operators | quiz[2].feedback.correct | Streams are passed by reference because they cannot be copied. | correct | unit basis: first row of quiz[2] |
| l12-operators | quiz[2].feedback.generic | Not quite right. What does passing `os` by value require? | correct | unit basis: first row of quiz[2] |
| l12-operators | quiz[2].explain.text | A by-value parameter is built with the copy constructor, and `std::ostream` deletes it. Write `std:… | correct | unit basis: first row of quiz[2] |
| l12-operators | quiz[3].prose | With your `Money` class: ```cpp Money fee(-375); std::cout << (fee * 2).str() << '\n'; ``` | correct | -375 x 2 = -750; run under the app compiler and grader prints -£7.50 (check l12.s4 chain) |
| l12-operators | quiz[3].widget.options[0] | key: `-£7.50` | correct | unit basis: first row of quiz[3] |
| l12-operators | quiz[3].widget.options[1].why | wrong option: `£-7.50` :: `str()` puts the sign before the `£`, after formatting the absolute value. | correct | unit basis: first row of quiz[3] |
| l12-operators | quiz[3].widget.options[2].why | wrong option: `-£7.5` :: The pence are padded to two digits: 50 stays `50`, and 5 would become `05`. | correct | unit basis: first row of quiz[3] |
| l12-operators | quiz[3].widget.options[3].why | wrong option: `£7.50` :: `operator*` keeps the sign: −375 × 2 is −750. | correct | unit basis: first row of quiz[3] |
| l12-operators | quiz[3].feedback.correct | −750 pence is −£7.50. | correct | unit basis: first row of quiz[3] |
| l12-operators | quiz[3].feedback.generic | Not quite right. Multiply the pence, then format. | correct | unit basis: first row of quiz[3] |
| l12-operators | quiz[3].explain.text | `operator*` gives −750 pence. `str()` formats 750 as `£7.50` and puts the minus sign in front. | correct | unit basis: first row of quiz[3] |
| l12-operators | summary.ideas[0] | `a + b` on your type calls `operator+(a, b)`: C++'s spelling of Python's `__add__`. Arithmetic oper… | correct | restates s0, s3, s5, s6, s7 |
| l12-operators | summary.ideas[1] | A member operator always has the object on the left. Write symmetric operators as free functions, s… | correct | unit basis: first row of summary |
| l12-operators | summary.ideas[2] | `<` must be strict and agree with `==`; test equality on whole pence, never on doubles. `operator<<… | correct | unit basis: first row of summary |
| l12-operators | summary.formula | Operators are function calls: a + b \quad\equiv\quad \texttt{operator+}(a, b) :: And `std::cout << … | correct | unit basis: first row of summary |
| l12-operators | summary.trap | A `+` that takes its left operand by non-const reference changes it: `cash + fee` would change `cas… | correct | unit basis: first row of summary |
| l13-templates | screens[0].prose | You need the largest value of a vector of `int` volumes and of a vector of `double` prices. C++ che… | correct | line-by-line comparison of the two functions: 6, 7 and 8 name the type |
| l13-templates | screens[0].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].widget.answer | key: ["l6", "l7", "l8"] | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].hints[0] | hint: Compare line 6 with line 1, line 7 with line 2, and so on. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].hints[1] | hint: These two lines are the same in both. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].hints[2] | hint: Every line that names the element type differs: the signature, `best` and the loop variable. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.correct | Only the type changes: lines 6, 7 and 8. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.generic | Not quite right. Compare each line of the second function with the matching line of the first. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.byKey.l9 | `return best;` is the same in both versions. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.byKey.l10 | The closing brace is the same in both versions. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.byKey.l1 | That is in the `int` version. Compare the second function with the first. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.byKey.l2 | That is in the `int` version. Compare the second function with the first. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.byKey.l3 | That is in the `int` version. Compare the second function with the first. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.byKey.l4 | That is in the `int` version. Compare the second function with the first. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.byKey.l5 | That is in the `int` version. Compare the second function with the first. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.byKey.l8 | Line 8 declares `double x` in the loop, so the type appears there too. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].feedback.byKey.l7 | Line 7 declares `double best`, so it differs from line 2. | correct | unit basis: first row of screens[0] |
| l13-templates | screens[0].explain.text | The two bodies are the same idea with a different type in three places. A string version would repe… | correct | unit basis: first row of screens[0] |
| l13-templates | screens[1].prose | A **template** writes the function once, with the type as a parameter `T`. Each call fixes `T` from… | correct | [temp.inst]: one implicit instantiation per set of template arguments used; run under the app compiler and grader: the four calls compile (check l13.s1) |
| l13-templates | screens[1].widget.answer | key: ["i", "d", "s"] | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].hints[0] | hint: Which types appear inside `std::vector<...>` in the calls? | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].hints[1] | hint: Two calls use `std::vector<int>`. | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].hints[2] | hint: Three types are used: `int`, `double` and `std::string`. One function is written for each. | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].feedback.correct | Three types used, three functions written. | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].feedback.generic | Not quite right. Write one function per type the calls use. | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].feedback.byKey.c | No call uses `std::vector<char>`, so no `char` version is written. | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].feedback.byKey.l | No call uses `std::vector<long>`, so no `long` version is written. | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].feedback.byKey.i | `max_of<int>` is used, twice. It is written once and called twice. | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].feedback.byKey.s | The last call uses `std::vector<std::string>`, so a string version is written. | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].feedback.byKey.d | The second call uses `std::vector<double>`, so a `double` version is written. | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].explain.text | At compile time the compiler writes one real function per type used: an **instantiation**. Two `int… | correct | unit basis: first row of screens[1] |
| l13-templates | screens[1].explain.canvas.caption | caption: Written at compile time: one function per type used | correct | unit basis: first row of screens[1] |
| l13-templates | screens[2].prose | Now write one. Start the total at `T{}`, the type's empty value: 0 for numbers, `""` for a string. … | correct | [dcl.init.list]: T{} value-initialises; run under the app compiler and grader: solution passes; `T total = 0` fails test 7; an int or double total gives "invalid operands" beside std::string (checks l13.s2) |
| l13-templates | screens[2].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[2] |
| l13-templates | screens[2].widget | code: 7 tests; solution passes, starter fails | correct | unit basis: first row of screens[2] |
| l13-templates | screens[2].hints[0] | hint: Write `template <typename T>` on the line before the function. | correct | unit basis: first row of screens[2] |
| l13-templates | screens[2].hints[1] | hint: An empty vector must give the type's empty value. | correct | unit basis: first row of screens[2] |
| l13-templates | screens[2].hints[2] | hint: `T total{}; for (const T& x : xs) total += x; return total;` | correct | unit basis: first row of screens[2] |
| l13-templates | screens[2].feedback.correct | One source, four types. | correct | unit basis: first row of screens[2] |
| l13-templates | screens[2].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[2] |
| l13-templates | screens[2].feedback.byKey.compile | The compiler stopped. Check that `template <typename T>` comes right before the function, and that … | correct | unit basis: first row of screens[2] |
| l13-templates | screens[2].feedback.byKey.test-7 | Test 7 joins strings. Start from `T{}`, not `0`: a `std::string` cannot start from a number. | correct | unit basis: first row of screens[2] |
| l13-templates | screens[2].explain.text | `T{}` is 0 for numbers and an empty string for `std::string`, so one start value works for every ty… | correct | unit basis: first row of screens[2] |
| l13-templates | screens[3].prose | Here `T` is **deduced** from both arguments, and each argument has to agree. | correct | [temp.deduct.call]: each argument deduces T and they must agree; run under the app compiler and grader: both quoted lines, 1 error; the four alternatives behave as keyed (checks l13.s3) |
| l13-templates | screens[3].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].widget.options[0] | key: `bigger<double>(3, 2.5)` | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].widget.options[1].why | wrong option: `bigger(3, 2.5)` :: That is the failing call: from 3, `T` is `int`, and from 2.5 it i… | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].widget.options[2].why | wrong option: `bigger<int>(3, 2.5)` :: That compiles, but `T` is `int`, so 2.5 becomes 2 before the… | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].widget.options[3].why | wrong option: `bigger<int, double>(3, 2.5)` :: `bigger` has one type parameter, so it takes one typ… | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].hints[0] | hint: What type does `3` give `T`? What type does `2.5` give? | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].hints[1] | hint: The note says the two deductions conflict. | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].hints[2] | hint: Name `T` yourself in angle brackets; then both arguments convert to it. | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].feedback.correct | Naming `T` stops the deduction, and 3 converts to 3.0. | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].feedback.generic | Not quite right. Find the call where `T` is fixed and is a type that keeps the .5. | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].feedback.byKey.same | That is the failing call: from 3, `T` is `int`, and from 2.5 it is `double`. One `T` cannot be both. | correct | unit basis: first row of screens[3] |
| l13-templates | screens[3].explain.text | Each argument proposes a `T`, and they must agree. Writing `bigger<double>` fixes `T`, so the `int`… | correct | unit basis: first row of screens[3] |
| l13-templates | screens[4].prose | `std::sort` is a template, compiled again for every type you sort. Sorting `Quote`s, which have no … | correct | run under the app compiler and grader with the library's debug mode and clang's default error limit: every quoted line, "20 errors generated" (check l13.s4 template error); positional keys checked (check l13.s4 byKey) |
| l13-templates | screens[4].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].widget.answer | key: ["l5", "l20"] | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].hints[0] | hint: Look for the first `error:` and for the first line that names `main.cpp`. | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].hints[1] | hint: This is the first error. | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].hints[2] | hint: Line 5 says `<` has no meaning for two `Quote`s. Line 20 points at `main.cpp:11`, your call t… | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].feedback.correct | The first error says what is missing; the `main.cpp` note says where you asked. | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].feedback.generic | Not quite right. Skip the library paths and look for `error:` and `main.cpp`. | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].feedback.byKey.l7 | That is a library file's path, an `instantiation` note. The cause is in the first `error:` line. | wrong | line 7 of the canvas is the caret line under the first error; the first instantiation note is line 8 (check l13.s4 byKey fails). Finding 1 |
| l13-templates | screens[4].feedback.byKey.l11 | That is a library file's path, an `instantiation` note. Find the line that names `main.cpp`. | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].feedback.byKey.l14 | That is a library file's path, an `instantiation` note. Find the line that names `main.cpp`. | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].feedback.byKey.l2 | That line only says which header the error is in. Find the first `error:`. | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].feedback.byKey.l23 | Later errors repeat the same cause. Read the first one. | correct | unit basis: first row of screens[4] |
| l13-templates | screens[4].explain.text | Line 5: `<` is missing for `Quote`. Line 20: your line 11 asked for it. Between them runs the templ… | correct | unit basis: first row of screens[4] |
| l13-templates | screens[5].prose | A class can be a template too: `Series<T>` holds a vector of `T`. Here it holds tickers, where a me… | correct | [temp.inst]/4: a member function of a class template is instantiated only when used; run under the app compiler and grader: builds; with names.mean() the quoted error at the division line (checks l13.s5) |
| l13-templates | screens[5].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[5] |
| l13-templates | screens[5].widget.options[0] | key: Yes: nothing calls `mean`, so it is never compiled for `std::string` | correct | unit basis: first row of screens[5] |
| l13-templates | screens[5].widget.options[1].why | wrong option: No: a `std::string` cannot be divided :: You expected every member to be checked for … | correct | unit basis: first row of screens[5] |
| l13-templates | screens[5].widget.options[2].why | wrong option: No: `Series` only accepts number types :: Nothing in the template says so. `T` can be… | correct | unit basis: first row of screens[5] |
| l13-templates | screens[5].hints[0] | hint: Which member functions does `main` call? | correct | unit basis: first row of screens[5] |
| l13-templates | screens[5].hints[1] | hint: `mean` is defined here but never called. | correct | unit basis: first row of screens[5] |
| l13-templates | screens[5].hints[2] | hint: Only `push` is called, and pushing a string is fine. | correct | unit basis: first row of screens[5] |
| l13-templates | screens[5].feedback.correct | It builds: `mean` is never instantiated for `std::string`. | correct | unit basis: first row of screens[5] |
| l13-templates | screens[5].feedback.generic | Not quite right. Ask which members `main` actually calls. | correct | unit basis: first row of screens[5] |
| l13-templates | screens[5].feedback.byKey.no | You expected every member to be checked for `std::string`. A class template's member function is co… | correct | unit basis: first row of screens[5] |
| l13-templates | screens[5].explain.text | A template's body is checked for a type only when that code is used. Add `names.mean();` and clang … | correct | unit basis: first row of screens[5] |
| l13-templates | screens[6].prose | The same `Series`, now holding traded volumes as `int`s. ```cpp int main() { Series<int> volumes; v… | correct | [expr.arith.conv]: int / size_t is unsigned; run under the app compiler and grader prints 2000, and a negative total gives 2147483645 (check l13.s6) |
| l13-templates | screens[6].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].widget.options[0] | key: `2000` | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].widget.options[1].why | wrong option: `2000.5` :: You expected a fractional mean. With `T = int` the total and `mean`'s res… | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].widget.options[2].why | wrong option: `2001` :: Integer division does not round: 4001 / 2 is 2000, the fraction thrown away. | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].widget.options[3].why | wrong option: A compile error: `int` cannot be divided by a size :: `int` divides by an unsigned si… | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].hints[0] | hint: What is `T` here, and what does `mean` return? | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].hints[1] | hint: This line divides a total of type `T`. | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].hints[2] | hint: 4001 / 2 in whole numbers is 2000. | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].feedback.correct | `T mean()` with `T = int` is an integer division. | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].feedback.generic | Not quite right. Work out the type of `total / xs_.size()`. | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].feedback.byKey.exact | You expected a fractional mean. With `T = int` the total and `mean`'s result are `int`s, so the div… | correct | unit basis: first row of screens[6] |
| l13-templates | screens[6].explain.text | Returning `T` made the mean an `int`. A negative total would also become a huge unsigned number bef… | correct | unit basis: first row of screens[6] |
| l13-templates | screens[7].prose | A template parameter can be a number instead of a type. `FixedPoint<Places>` stores a value as a wh… | correct | [temp.param]: a non-type parameter; 1.2345 x 10^4 = 12345; slips 123.45 and 1.2345 |
| l13-templates | screens[7].canvas | canvas: the listing, terminal output or table shown | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].widget.answer | key: 12345 (How many units does `FixedPoint<4>` store for the rate 1.2345?) | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].widget.accept | accept: 12345: $1.2345 \times 10^4$. | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].widget.wrong[0] | slip: 123.45 (two) | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].widget.wrong[1] | slip: 1.2345 (raw) | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].hints[0] | hint: How many units of $10^{-4}$ make 1.2345? | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].hints[1] | hint: The first row multiplies 12.34 by $10^2$. | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].hints[2] | hint: Multiply by $10^4 = 10000$. | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].feedback.correct | $1.2345 \times 10^4 = 12345$. | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].feedback.generic | Not quite right. Multiply the value by $10^{\text{Places}}$. | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].feedback.byKey.two | You used two places, as for pence. `FixedPoint<4>` keeps four. | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].feedback.byKey.raw | That is the value itself. The class stores a whole number of $10^{-4}$ units. | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].explain.text | `Places` is fixed at compile time, so `FixedPoint<2>` and `FixedPoint<4>` are different types. Addi… | correct | unit basis: first row of screens[7] |
| l13-templates | screens[7].explain.canvas.values | canvas: {"r1c2": "12345"} | correct | unit basis: first row of screens[7] |
| l13-templates | screens[8].prose | A template is a recipe the compiler fills in, once per set of parameters it is used with: ```cpp te… | correct | [temp]: vector, map, sort and unique_ptr are templates ([vector.syn], [map.overview], [alg.sort], [unique.ptr]) |
| l13-templates | screens[8].widget.options[0] | key: Two classes the compiler wrote from one template | correct | unit basis: first row of screens[8] |
| l13-templates | screens[8].widget.options[1].why | wrong option: One class that can hold any type, like a Python list :: A Python list holds any objec… | correct | unit basis: first row of screens[8] |
| l13-templates | screens[8].widget.options[2].why | wrong option: Two classes the library authors wrote by hand :: The library ships one template; your… | correct | unit basis: first row of screens[8] |
| l13-templates | screens[8].widget.options[3].why | wrong option: One class that checks the element type at run time :: There is no run-time check: the… | correct | unit basis: first row of screens[8] |
| l13-templates | screens[8].hints[0] | hint: Recall the graph of `max_of<T>` and its instantiations. | correct | unit basis: first row of screens[8] |
| l13-templates | screens[8].hints[1] | hint: `vector` is a class template, instantiated once per element type you use. | correct | unit basis: first row of screens[8] |
| l13-templates | screens[8].feedback.correct | The standard library is almost entirely templates. | correct | unit basis: first row of screens[8] |
| l13-templates | screens[8].feedback.generic | Not quite right. Think of `max_of<T>` and the functions written from it. | correct | unit basis: first row of screens[8] |
| l13-templates | screens[8].explain.text | `std::vector`, `std::map`, `std::sort` and `std::unique_ptr` are all templates. That is how one lib… | correct | unit basis: first row of screens[8] |
| l13-templates | screens[9].prose | A signal uses the mean of the last $n$ prices. A volume filter uses the mean of the last $n$ volume… | correct | run under the app compiler and grader: solution passes; the three named slips fail first at tests 2, 7 and 8 (checks l13.s9); (101 + 102 + 106) / 3 = 103; deque pop_front is constant: [deque.modifiers] |
| l13-templates | screens[9].canvas.state.caption | caption: Mean of the last 3: (101 + 102 + 106) / 3 = 103 | correct | unit basis: first row of screens[9] |
| l13-templates | screens[9].widget | code: 9 tests; solution passes, starter fails | correct | unit basis: first row of screens[9] |
| l13-templates | screens[9].hints[0] | hint: In `push`, add the value, then drop the oldest if there are more than `n_`. | correct | unit basis: first row of screens[9] |
| l13-templates | screens[9].hints[1] | hint: After the fourth push, the 100 is gone. | correct | unit basis: first row of screens[9] |
| l13-templates | screens[9].hints[2] | hint: `xs_.push_back(x); if (static_cast<int>(xs_.size()) > n_) xs_.erase(xs_.begin());` and in `me… | correct | unit basis: first row of screens[9] |
| l13-templates | screens[9].feedback.correct | One template, any numeric series. | correct | unit basis: first row of screens[9] |
| l13-templates | screens[9].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of screens[9] |
| l13-templates | screens[9].feedback.byKey.test-2 | Test 2 pushes 4 values into a window of 3 and expects 103. Drop the oldest value. | correct | unit basis: first row of screens[9] |
| l13-templates | screens[9].feedback.byKey.test-7 | Test 7 asks for the mean of an empty window. Refuse it before dividing by zero. | correct | unit basis: first row of screens[9] |
| l13-templates | screens[9].feedback.byKey.test-8 | Test 8 builds a window of size 0. Refuse it in the constructor. | correct | unit basis: first row of screens[9] |
| l13-templates | screens[9].explain.text | `Window<double>` serves prices and volumes alike. `Window<FixedPoint<2>>` would work once it has `+… | correct | unit basis: first row of screens[9] |
| l13-templates | quiz[0].prose | With the `max_of` template from this lesson: ```cpp max_of(std::vector<std::string>{"BARC", "AZN", … | correct | [string.cmp]: lexicographic comparison; run under the app compiler and grader returns VOD (check l13.s1) |
| l13-templates | quiz[0].widget.options[0] | key: `"VOD"` | correct | unit basis: first row of quiz[0] |
| l13-templates | quiz[0].widget.options[1].why | wrong option: `"LLOY"` :: `<` on strings compares character by character from the left, not by leng… | correct | unit basis: first row of quiz[0] |
| l13-templates | quiz[0].widget.options[2].why | wrong option: `"BARC"` :: That is only the starting `best`. Any later string that compares greater … | correct | unit basis: first row of quiz[0] |
| l13-templates | quiz[0].widget.options[3].why | wrong option: A compile error: strings have no maximum :: `std::string` has `<`, which compares cha… | correct | unit basis: first row of quiz[0] |
| l13-templates | quiz[0].feedback.correct | V is the latest first letter, so VOD is the maximum. | correct | unit basis: first row of quiz[0] |
| l13-templates | quiz[0].feedback.generic | Not quite right. `<` on strings compares character by character from the left. | correct | unit basis: first row of quiz[0] |
| l13-templates | quiz[0].explain.text | For `std::string`, `best < x` compares character codes from the left. For all-capital tickers that … | correct | unit basis: first row of quiz[0] |
| l13-templates | quiz[1].prose | ```cpp sum_of(std::vector<int>{1, 2}); sum_of(std::vector<double>{0.5}); sum_of(std::vector<int>{7}… | correct | [temp.inst]: int, double, long long |
| l13-templates | quiz[1].widget.answer | key: 3 (How many functions does the compiler write from `sum_of`?) | correct | unit basis: first row of quiz[1] |
| l13-templates | quiz[1].widget.accept | accept: 3: one each for `int`, `double` and `long long`. | correct | unit basis: first row of quiz[1] |
| l13-templates | quiz[1].widget.wrong[0] | slip: 4 (calls) | correct | unit basis: first row of quiz[1] |
| l13-templates | quiz[1].widget.wrong[1] | slip: 1 (one) | correct | unit basis: first row of quiz[1] |
| l13-templates | quiz[1].feedback.correct | One function per type: `int`, `double`, `long long`. | correct | unit basis: first row of quiz[1] |
| l13-templates | quiz[1].feedback.generic | Not quite right. Count the different element types, not the calls. | correct | unit basis: first row of quiz[1] |
| l13-templates | quiz[1].feedback.byKey.calls | You counted calls. The two `int` calls share one instantiation. | correct | unit basis: first row of quiz[1] |
| l13-templates | quiz[1].feedback.byKey.one | A template is not one function: each type used gets its own. | correct | unit basis: first row of quiz[1] |
| l13-templates | quiz[1].explain.text | The two `int` calls share `sum_of<int>`. With `double` and `long long`, that makes three instantiat… | correct | unit basis: first row of quiz[1] |
| l13-templates | quiz[2].prose | You declare `template <typename T> T sum_of(const std::vector<T>&);` in `stats.h` and define it in … | correct | [temp.pre]/10: a template must be defined where it is implicitly instantiated; run, g++ and ld: undefined reference to sum_of<double> (check l13.quiz2) |
| l13-templates | quiz[2].widget.options[0] | key: An undefined reference to `sum_of<double>`: no file ever wrote it | correct | unit basis: first row of quiz[2] |
| l13-templates | quiz[2].widget.options[1].why | wrong option: It links and runs :: `stats.cpp` never sees a `double` call, so it writes no `sum_of<… | correct | unit basis: first row of quiz[2] |
| l13-templates | quiz[2].widget.options[2].why | wrong option: `main.cpp` fails to compile :: The declaration is enough to compile the call. The mis… | correct | unit basis: first row of quiz[2] |
| l13-templates | quiz[2].feedback.correct | A template's body must be visible where it is used, so it goes in the header. | correct | unit basis: first row of quiz[2] |
| l13-templates | quiz[2].feedback.generic | Not quite right. Which file could write `sum_of<double>`? | correct | unit basis: first row of quiz[2] |
| l13-templates | quiz[2].explain.text | An instantiation is written where the body and the type meet. Here they never meet, so the linker f… | correct | unit basis: first row of quiz[2] |
| l13-templates | quiz[3].prose | With your `sum_of`: ```cpp auto a = sum_of(std::vector<double>{}); auto b = sum_of(std::vector<std:… | correct | T{} is 0.0 and the empty string; run under the app compiler and grader (check l13.quiz3) |
| l13-templates | quiz[3].widget.options[0] | key: `a` is `0.0` and `b` is `""` | correct | unit basis: first row of quiz[3] |
| l13-templates | quiz[3].widget.options[1].why | wrong option: Both calls stop: the vectors are empty :: The loop runs zero times and the function r… | correct | unit basis: first row of quiz[3] |
| l13-templates | quiz[3].widget.options[2].why | wrong option: `a` is `0.0` and `b` is `"0"` :: `T{}` for a string is the empty string, not the text… | correct | unit basis: first row of quiz[3] |
| l13-templates | quiz[3].feedback.correct | An empty sum is the type's empty value. | correct | unit basis: first row of quiz[3] |
| l13-templates | quiz[3].feedback.generic | Not quite right. What does `T{}` give for each type? | correct | unit basis: first row of quiz[3] |
| l13-templates | quiz[3].explain.text | With no elements the loop never runs, so the result is `T{}`: 0.0 for `double` and `""` for `std::s… | correct | unit basis: first row of quiz[3] |
| l13-templates | summary.ideas[0] | A template takes a type (or a number) as a parameter. The compiler writes one instantiation per set… | correct | restates s1, s3, s4, s5, s6 |
| l13-templates | summary.ideas[1] | `T` is deduced from the arguments, and every argument must agree; name it yourself (`bigger<double>… | correct | unit basis: first row of summary |
| l13-templates | summary.ideas[2] | In a template error, read the first `error:` line and the line naming your own file. The rest is th… | correct | unit basis: first row of summary |
| l13-templates | summary.formula | Instantiation: \texttt{max\_of<T>} \quad\to\quad \texttt{max\_of<int>},\ \texttt{max\_of<double>},\… | correct | unit basis: first row of summary |
| l13-templates | summary.trap | Returning `T` from a mean makes `Series<int>` divide in whole numbers: 4001 / 2 gives 2000. Return … | correct | unit basis: first row of summary |
| review-3 | items[0].prose | `Quote` keeps `bid_ < ask_` as an invariant. Four drafts of `set_ask`: | correct | as l10 s7 and s8: check before storing |
| review-3 | items[0].widget.options[0] | key: `void set_ask(double a) { if (a <= bid_) throw std::invalid_argument(""); ask_ = a; }` | correct | unit basis: first row of items[0] |
| review-3 | items[0].widget.options[1].why | wrong option: `void set_ask(double a) { ask_ = a; if (ask_ <= bid_) std::cout << "crossed"; }` :: I… | correct | unit basis: first row of items[0] |
| review-3 | items[0].widget.options[2].why | wrong option: `void set_ask(double a) { ask_ = a; }` :: It skips the check, so any ask goes in, eve… | correct | unit basis: first row of items[0] |
| review-3 | items[0].widget.options[3].why | wrong option: `void set_ask(double a) { if (a >= bid_) throw std::invalid_argument(""); ask_ = a; }… | correct | unit basis: first row of items[0] |
| review-3 | items[0].feedback.correct | Check first, then store. | correct | unit basis: first row of items[0] |
| review-3 | items[0].feedback.generic | Not quite right. The ask must stay above the bid, checked before it is stored. | correct | unit basis: first row of items[0] |
| review-3 | items[0].explain.text | A changing function checks before it stores, so a refused call leaves the object as it was. An ask … | correct | unit basis: first row of items[0] |
| review-3 | items[1].prose | `Logger` prints `open` and `close` with its name. ```cpp class Desk { public: Desk() : feed_("feed"… | correct | [class.base.init]/13, [class.dtor]/9; run under the app compiler and grader: the six lines in the keyed order (check review-3.1) |
| review-3 | items[1].widget.answer | key: ["of", "or", "do", "dc", "cr", "cf"] | correct | unit basis: first row of items[1] |
| review-3 | items[1].widget.lines.of | step: `open feed` | correct | unit basis: first row of items[1] |
| review-3 | items[1].widget.lines.or | step: `open risk` | correct | unit basis: first row of items[1] |
| review-3 | items[1].widget.lines.do | step: `desk open` | correct | unit basis: first row of items[1] |
| review-3 | items[1].widget.lines.dc | step: `desk close` | correct | unit basis: first row of items[1] |
| review-3 | items[1].widget.lines.cr | step: `close risk` | correct | unit basis: first row of items[1] |
| review-3 | items[1].widget.lines.cf | step: `close feed` | correct | unit basis: first row of items[1] |
| review-3 | items[1].feedback.correct | Members first, then the body; on the way out, the reverse. | correct | unit basis: first row of items[1] |
| review-3 | items[1].feedback.generic | Not quite right. Members are built before the constructor's body runs, and destroyed after the dest… | correct | unit basis: first row of items[1] |
| review-3 | items[1].feedback.byKey.do | The constructor's body runs only after every member has been built. | correct | unit basis: first row of items[1] |
| review-3 | items[1].feedback.byKey.cf | Members are destroyed in reverse declaration order: `risk_` before `feed_`. | correct | unit basis: first row of items[1] |
| review-3 | items[1].feedback.byKey.dc | The destructor's body runs first; the members it may use are destroyed after it. | correct | unit basis: first row of items[1] |
| review-3 | items[1].explain.text | The members are built in declaration order before the body prints `desk open`. Destruction mirrors … | correct | unit basis: first row of items[1] |
| review-3 | items[2].prose | You want `std::cout << q` to print a `Quote`, and to chain with more `<<`. | correct | as l12 s4: stream by reference in and out; a member would need q << std::cout |
| review-3 | items[2].widget.options[0] | key: `std::ostream& operator<<(std::ostream& os, const Quote& q)` | correct | unit basis: first row of items[2] |
| review-3 | items[2].widget.options[1].why | wrong option: `std::ostream operator<<(std::ostream os, const Quote& q)` :: Streams cannot be copie… | correct | unit basis: first row of items[2] |
| review-3 | items[2].widget.options[2].why | wrong option: `std::ostream& Quote::operator<<(std::ostream& os) const` :: As a member, the `Quote`… | correct | unit basis: first row of items[2] |
| review-3 | items[2].widget.options[3].why | wrong option: `void operator<<(std::ostream& os, const Quote& q)` :: It prints once, but returns no… | correct | unit basis: first row of items[2] |
| review-3 | items[2].feedback.correct | Stream by reference in, the same stream out. | correct | unit basis: first row of items[2] |
| review-3 | items[2].feedback.generic | Not quite right. The stream must be on the left, by reference, and returned. | correct | unit basis: first row of items[2] |
| review-3 | items[2].explain.text | A free function puts the stream on the left. Taking and returning `std::ostream&` passes the one st… | correct | unit basis: first row of items[2] |
| review-3 | items[3].prose | ```cpp max_of(std::vector<int>{3, 1}); max_of(std::vector<std::string>{"AZN"}); max_of(std::vector<… | correct | [temp.inst]: int, std::string, double |
| review-3 | items[3].widget.answer | key: 3 (How many functions does the compiler write from the `max_of` template?) | correct | unit basis: first row of items[3] |
| review-3 | items[3].widget.accept | accept: 3: `int`, `std::string` and `double`. | correct | unit basis: first row of items[3] |
| review-3 | items[3].widget.wrong[0] | slip: 5 (calls) | correct | unit basis: first row of items[3] |
| review-3 | items[3].widget.wrong[1] | slip: 1 (one) | correct | unit basis: first row of items[3] |
| review-3 | items[3].feedback.correct | Three element types, three instantiations. | correct | unit basis: first row of items[3] |
| review-3 | items[3].feedback.generic | Not quite right. Count types, not calls. | correct | unit basis: first row of items[3] |
| review-3 | items[3].feedback.byKey.calls | You counted calls. Calls with the same type share one function. | correct | unit basis: first row of items[3] |
| review-3 | items[3].feedback.byKey.one | Each type used gets its own function. | correct | unit basis: first row of items[3] |
| review-3 | items[3].explain.text | `int` and `std::string` are each used twice, `double` once: three instantiations, written at compil… | correct | unit basis: first row of items[3] |
| review-3 | items[4].prose | A desk's risk limit caps the absolute exposure, long or short. A negative limit makes no sense, so … | correct | run under the app compiler and grader: solution passes, starter fails |
| review-3 | items[4].widget | code: 9 tests; solution passes, starter fails | correct | unit basis: first row of items[4] |
| review-3 | items[4].feedback.correct | The limit can never go negative, through either door. | correct | unit basis: first row of items[4] |
| review-3 | items[4].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of items[4] |
| review-3 | items[4].explain.text | The constructor and `set` both refuse a negative value, so no `RiskLimit` ever holds one. `allows` … | correct | unit basis: first row of items[4] |
| review-3 | items[5].prose | Money now carries its currency. Adding pounds to dollars is a bug, so `+` refuses it. Two amounts a… | correct | run under the app compiler and grader: solution passes, starter does not compile |
| review-3 | items[5].widget | code: 7 tests; solution passes, starter fails | correct | unit basis: first row of items[5] |
| review-3 | items[5].feedback.correct | Mixed currencies are refused, never silently added. | correct | unit basis: first row of items[5] |
| review-3 | items[5].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of items[5] |
| review-3 | items[5].explain.text | `+` checks the currencies first, so £1 plus one dollar stops the program instead of giving 200 penc… | correct | unit basis: first row of items[5] |
| review-3 | items[6].prose | ```cpp class Pricer { std::string name_; std::unique_ptr<Lattice> grid_; public: explicit Pricer(st… | correct | run under the app compiler and grader: the move compiles; the copy, copy assignment and move from const do not (checks review-3.6) |
| review-3 | items[6].widget.options[0] | key: `Pricer b = std::move(a);` | correct | unit basis: first row of items[6] |
| review-3 | items[6].widget.options[1].why | wrong option: `Pricer b = a;` :: The copy constructor is deleted, because `unique_ptr` cannot be co… | correct | unit basis: first row of items[6] |
| review-3 | items[6].widget.options[2].why | wrong option: `Pricer b("tree"); b = a;` :: Copy assignment is deleted for the same reason: one lat… | correct | unit basis: first row of items[6] |
| review-3 | items[6].widget.options[3].why | wrong option: `const Pricer c("tree"); Pricer b = std::move(c);` :: A `const` object cannot be move… | correct | unit basis: first row of items[6] |
| review-3 | items[6].feedback.correct | A `unique_ptr` member makes the class move-only. | correct | unit basis: first row of items[6] |
| review-3 | items[6].feedback.generic | Not quite right. Which special members does `unique_ptr` allow? | correct | unit basis: first row of items[6] |
| review-3 | items[6].explain.text | With the rule of zero, `Pricer` gets what its members allow: moves, but no copies. Moving from a `c… | correct | unit basis: first row of items[6] |
| review-3 | items[7].prose | A screen ranks values: the `n` largest, largest first. Write it once for any type with `<`. | correct | run under the app compiler and grader: solution passes, starter does not compile |
| review-3 | items[7].widget | code: 7 tests; solution passes, starter fails | correct | unit basis: first row of items[7] |
| review-3 | items[7].feedback.correct | One template ranks numbers and tickers alike. | correct | unit basis: first row of items[7] |
| review-3 | items[7].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of items[7] |
| review-3 | items[7].explain.text | `xs` is taken by value, so sorting it leaves the caller's vector alone. `std::sort` then `std::reve… | correct | unit basis: first row of items[7] |
| review-3 | items[8].prose | On the bid side, the highest price trades first, and at the same price the earliest order. `Order` … | correct | [tuple.rel]; run under the app compiler and grader: the keyed body gives C B A D, both flipped B C A D, the ask form D A C B (checks review-3.8) |
| review-3 | items[8].widget.options[0] | key: `return std::tie(b.price, a.time) < std::tie(a.price, b.time);` | correct | unit basis: first row of items[8] |
| review-3 | items[8].widget.options[1].why | wrong option: `return std::tie(b.price, b.time) < std::tie(a.price, a.time);` :: That flips time as… | correct | unit basis: first row of items[8] |
| review-3 | items[8].widget.options[2].why | wrong option: `return std::tie(a.price, a.time) < std::tie(b.price, b.time);` :: That is the ask si… | correct | unit basis: first row of items[8] |
| review-3 | items[8].widget.options[3].why | wrong option: `return a.price > b.price;` :: It ignores time, so orders at one price come out in an… | correct | unit basis: first row of items[8] |
| review-3 | items[8].feedback.correct | Price descending, then time ascending. | correct | unit basis: first row of items[8] |
| review-3 | items[8].feedback.generic | Not quite right. Flip the price comparison only. | correct | unit basis: first row of items[8] |
| review-3 | items[8].explain.text | Putting `b.price` on the left flips the price order, highest first, while `a.time` on the left keep… | correct | unit basis: first row of items[8] |
| homework-3 | items[0].prose | `Logger` prints `open` and `close` with its name. ```cpp int main() { Logger a("a"); { Logger b("b"… | correct | run under the app compiler and grader: the eight lines in the keyed order (check homework-3.0) |
| homework-3 | items[0].widget.answer | key: ["oa", "ob", "ot", "ct", "w", "cb", "e", "ca"] | correct | unit basis: first row of items[0] |
| homework-3 | items[0].widget.lines.oa | step: `open a` | correct | unit basis: first row of items[0] |
| homework-3 | items[0].widget.lines.ob | step: `open b` | correct | unit basis: first row of items[0] |
| homework-3 | items[0].widget.lines.ot | step: `open tmp` | correct | unit basis: first row of items[0] |
| homework-3 | items[0].widget.lines.ct | step: `close tmp` | correct | unit basis: first row of items[0] |
| homework-3 | items[0].widget.lines.w | step: `work` | correct | unit basis: first row of items[0] |
| homework-3 | items[0].widget.lines.cb | step: `close b` | correct | unit basis: first row of items[0] |
| homework-3 | items[0].widget.lines.e | step: `end` | correct | unit basis: first row of items[0] |
| homework-3 | items[0].widget.lines.ca | step: `close a` | correct | unit basis: first row of items[0] |
| homework-3 | items[0].feedback.correct | The temporary dies at its semicolon; the named objects at their braces. | correct | unit basis: first row of items[0] |
| homework-3 | items[0].feedback.generic | Not quite right. A temporary dies at the end of its full expression. | correct | unit basis: first row of items[0] |
| homework-3 | items[0].feedback.byKey.w | The temporary has already closed by then: it dies at the `;` on its own line. | correct | unit basis: first row of items[0] |
| homework-3 | items[0].feedback.byKey.cb | `b` lives until the inner closing brace, after `work`. | correct | unit basis: first row of items[0] |
| homework-3 | items[0].feedback.byKey.e | `end` prints after the inner block has closed `b`. | correct | unit basis: first row of items[0] |
| homework-3 | items[0].feedback.byKey.ca | `a` lives until the end of `main`, after `end`. | correct | unit basis: first row of items[0] |
| homework-3 | items[0].explain.text | `Logger("tmp");` is born and dies on one line. `b` ends at the inner brace, before `end`, and `a` a… | correct | unit basis: first row of items[0] |
| homework-3 | items[1].prose | A position: buy 200 at £50.00, buy 100 at £53.00, sell 150, buy 50 at £56.00. | correct | 15300 / 300 = 51; (150 x 51 + 50 x 56) / 200 = 52.25; slips 18100 / 350 = 51.7143 and 53 |
| homework-3 | items[1].widget.answer | key: 52.25 (What is the average price at the end, in pounds?) | correct | unit basis: first row of items[1] |
| homework-3 | items[1].widget.accept | accept: £52.25: £51.00 on 300, then 150 left at £51.00, then $(150 \times 51 + 50 \times 56) / 200$. | correct | unit basis: first row of items[1] |
| homework-3 | items[1].widget.wrong[0] | slip: 51.7143 (nosell) | correct | unit basis: first row of items[1] |
| homework-3 | items[1].widget.wrong[1] | slip: 53.0 (simple) | correct | unit basis: first row of items[1] |
| homework-3 | items[1].feedback.correct | £10,450 over 200 shares is £52.25. | correct | unit basis: first row of items[1] |
| homework-3 | items[1].feedback.generic | Not quite right. Weight each buy by its shares; a sale changes only the quantity. | correct | unit basis: first row of items[1] |
| homework-3 | items[1].feedback.byKey.nosell | You kept all 300 shares in the last step. After selling 150, only 150 remain at £51.00. | correct | unit basis: first row of items[1] |
| homework-3 | items[1].feedback.byKey.simple | You averaged the three prices. Weight each by its shares. | correct | unit basis: first row of items[1] |
| homework-3 | items[1].explain.text | The first two buys give $(10000 + 5300)/300 = 51$. Selling 150 leaves 150 at £51.00. The last buy g… | correct | unit basis: first row of items[1] |
| homework-3 | items[2].prose | Extend your `Position`: `sell(qty, px)` now returns the P&L of that sale, $q \times (p - \bar p)$, … | correct | run under the app compiler and grader: solution passes, starter fails; 150 x (55 - 51) = 600, 150 x (49 - 51) = -300 |
| homework-3 | items[2].widget | code: 11 tests; solution passes, starter fails | correct | unit basis: first row of items[2] |
| homework-3 | items[2].feedback.correct | Quantity, average and realised P&L stay consistent. | correct | unit basis: first row of items[2] |
| homework-3 | items[2].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of items[2] |
| homework-3 | items[2].explain.text | A sale earns $q(p - \bar p)$ against the average cost and leaves the average alone. Selling 150 at … | correct | unit basis: first row of items[2] |
| homework-3 | items[3].prose | `Fixed<Places>` holds a value as a whole number of $10^{-\text{Places}}$ units. `Fixed<2>` is pence… | correct | run under the app compiler and grader: solution passes, starter does not compile |
| homework-3 | items[3].widget | code: 8 tests; solution passes, starter fails | correct | unit basis: first row of items[3] |
| homework-3 | items[3].feedback.correct | Exact decimals, with the places fixed at compile time. | correct | unit basis: first row of items[3] |
| homework-3 | items[3].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of items[3] |
| homework-3 | items[3].explain.text | `str()` splits the absolute units by $10^{\text{Places}}$ and pads the fraction to `Places` digits.… | correct | unit basis: first row of items[3] |
| homework-3 | items[4].prose | ```cpp class Prices { public: explicit Prices(int n) : data_(new double[n]) {} ~Prices() { delete[]… | correct | as l11 s8 and s9: a vector member copies and frees itself |
| homework-3 | items[4].widget.options[0] | key: Replace `double*` with `std::vector<double>`, built with `data_(n)`, and delete the destructor | correct | unit basis: first row of items[4] |
| homework-3 | items[4].widget.options[1].why | wrong option: Add `Prices(const Prices&) = default;` :: The default copy still copies the address, … | correct | unit basis: first row of items[4] |
| homework-3 | items[4].widget.options[2].why | wrong option: Remove the destructor :: Then nothing is freed twice, but nothing is freed at all: ev… | correct | unit basis: first row of items[4] |
| homework-3 | items[4].widget.options[3].why | wrong option: Make the member `double* const data_` :: A const pointer still copies the same addres… | correct | unit basis: first row of items[4] |
| homework-3 | items[4].feedback.correct | Rule of zero: let a member own the memory. | correct | unit basis: first row of items[4] |
| homework-3 | items[4].feedback.generic | Not quite right. Who owns the block after a copy? | correct | unit basis: first row of items[4] |
| homework-3 | items[4].explain.text | A `std::vector<double>` copies its elements, frees them once, and moves cheaply. With it the class … | correct | unit basis: first row of items[4] |
| homework-3 | items[5].prose | An order book holds bid and ask **levels**, each a price in pence and a total size. Bids are kept h… | correct | run under the app compiler and grader: solution passes, starter fails |
| homework-3 | items[5].widget | code: 15 tests; solution passes, starter fails | correct | unit basis: first row of items[5] |
| homework-3 | items[5].feedback.correct | The book stays sorted and never crosses. | correct | unit basis: first row of items[5] |
| homework-3 | items[5].feedback.generic | Not quite right. Read the first failing test under the editor. | correct | unit basis: first row of items[5] |
| homework-3 | items[5].explain.text | `add` checks size and the crossing rule before touching either side, then merges into a level or in… | correct | unit basis: first row of items[5] |
| homework-3 | items[6].prompt | prompt: A desk asks you to design the C++ `Position` class its risk system will use. One object tra… | correct | design answer judged against l10 to l12: invariants, rule of zero, operator choices, integer pence |
| homework-3 | items[6].model | model answer: **(a) Invariants, and where they are checked.** 1. The ticker is not empty. *Checked … | correct | unit basis: first row of items[6] |
| homework-3 | items[6].rubric[0] | rubric: States at least three invariants and where each is checked. Examples: non-empty ticker, lim… | correct | unit basis: first row of items[6] |
| homework-3 | items[6].rubric[1] | rubric: Data private; changes only through checked functions; readers `const`; no non-const referen… | correct | unit basis: first row of items[6] |
| homework-3 | items[6].rubric[2] | rubric: Initialiser list used in the constructor, with the check after the members are built | correct | unit basis: first row of items[6] |
| homework-3 | items[6].rubric[3] | rubric: Rule of zero justified from the member types; says a raw resource would need the rule of fi… | correct | unit basis: first row of items[6] |
| homework-3 | items[6].rubric[4] | rubric: Operators: `operator<<` returning `std::ostream&`; refuses `+` on positions (or on mixed un… | correct | unit basis: first row of items[6] |
| homework-3 | items[6].rubric[5] | rubric: Money in integer pence (or ticks) with no `==` on doubles, and a refused call leaves the ob… | correct | unit basis: first row of items[6] |
| homework-3 | items[7].prose | A risk screen tracks the lowest and highest value seen in a session. The value may be a price, a ti… | correct | run under the app compiler and grader: solution passes, starter does not compile; cpp-3-perf-numbers.py exit 0; 2,000,000,000 - (-2,000,000,000) = 4,000,000,000 |
| homework-3 | items[7].widget | code: 15 tests; solution passes, starter fails | correct | unit basis: first row of items[7] |
| homework-3 | items[7].feedback.correct | Correct. The ends stay in order, the operators agree, and `+=` hands back the range itself. | correct | unit basis: first row of items[7] |
| homework-3 | items[7].feedback.generic | Not quite right. Read the first failing test. | correct | unit basis: first row of items[7] |
| homework-3 | items[7].explain.text | Every way to change a range goes through `add` or the checked constructor, so the low never passes … | correct | unit basis: first row of items[7] |
