from lib2 import *
import refs4 as R

E1 = ['edge-case-list']
E2 = ['test-first']
E3 = ['mutation-tests']

M1_LINES = [
    "best = run = 0",
    "for i, x in enumerate(xs):",
    "    if i and x == xs[i - 1]:",
    "        run += 1",
    "    else:",
    "        best = max(best, run)",
    "        run = 1",
    "return best",
]

BUG_LINES = [
    "m1 forgets the last run.",
    "m2 returns 1 for an empty list.",
    "m3 returns 0 for a single number.",
    "m4 counts runs that never fall, so 1, 2 counts as a run.",
    "m5 restarts a run at 0 after a break.",
    "m6 compares every number only with the first one.",
]

CPP_PRELUDE = """#include <vector>
#include <algorithm>
int longest_streak(const std::vector<int>& xs);
"""

CPP_POSTLUDE = """int longest_streak(const std::vector<int>& xs) {
    int best = 0, run = 0;
#ifdef BUG1
    for (size_t i = 0; i < xs.size(); ++i) {
        if (i && xs[i] == xs[i - 1]) ++run;
        else { best = std::max(best, run); run = 1; }
    }
    return best;
#elif defined(BUG2)
    best = 1;
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#elif defined(BUG3)
    if (xs.size() == 1) return 0;
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#elif defined(BUG4)
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] >= xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#elif defined(BUG5)
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : (i == 0 ? 1 : 0);
        best = std::max(best, run);
    }
    return best;
#else
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#endif
}
"""

CPP_STARTER = """#include <vector>
#include <algorithm>
TEST(empty) { CHECK(longest_streak({}) == 0); }
"""

CPP_SOL = """#include <vector>
#include <algorithm>
TEST(empty) { CHECK(longest_streak({}) == 0); }
TEST(single) { CHECK(longest_streak({7}) == 1); }
TEST(rising) { CHECK(longest_streak({1, 2}) == 1); }
TEST(run_after_break) { CHECK(longest_streak({3, 1, 1}) == 2); }
TEST(whole_list) { CHECK(longest_streak({2, 2, 2}) == 3); }
TEST(two_runs) { CHECK(longest_streak({1, 1, 2, 2, 2}) == 3); }
"""


def rule_console():
    return console("longest_streak(xs)", [
        "A run is a stretch of equal neighbours.",
        "longest_streak returns the length of the longest run.",
        "An empty list has no run, so its answer is 0."])


def lesson():
    S = []
    # 1 hook multi
    S.append(screen(
        'problem', 1, 'Which inputs catch the bug', E1 + ['mutation-tests'],
        "`longest_streak(xs)` is the length of the longest run of equal neighbours: `[1, 1, 2, 2, 2]` gives 3. "
        "This version, m1, has a planted bug. You tested for empty, one and many in `pytest` l5 and stress-tested in `contests` l4. New here: a bug marks your tests.",
        "Select all that apply: which inputs expose m1?",
        multi([
            ('a', '`[]`', "You chose the empty list. m1 returns 0 there, and 0 is right."),
            ('b', '`[1, 2]`', "You chose a list with no repeat. m1 returns 1 there, and 1 is right."),
            ('c', '`[2, 2, 2]`', None),
            ('d', '`[3, 1, 1]`', None),
            ('e', '`[2, 1]`', "You chose a list with no repeat. m1 returns 1 there, and 1 is right."),
        ]),
        hints("Where does m1 record the length of a run?",
              "It records at a break, in the `else` branch.", "A run that reaches the end of the list never meets a break. So the answer must be a run at the end.", ["l5", "l6", "l7"]),
        fb("The last run is the longest in `[2, 2, 2]` and `[3, 1, 1]`, so m1 misses it.",
           "Not quite right. Find the inputs whose longest run is the last one.",
           {'a': "Both m1 and the correct version return 0 for `[]`.", 'b': "m1 and the correct version both return 1.", 'e': "m1 and the correct version both return 1."}),
        explain("m1 records `best` only when a run breaks. In `[2, 2, 2]` and `[3, 1, 1]` the longest run ends the list, so it is never recorded. The other three inputs give the right answer.",
                {"shade": {"bug": ["l5", "l6", "l7"]}}),
        canvas=console('Version m1 of longest_streak', M1_LINES), pace=120))
    # 2 ladder table: expected outputs
    S.append(screen(
        'ladder', 1, 'What should come out', E1,
        "A test needs the expected answer, worked out by hand before you run anything. Write the answer for each input.",
        "Fill in `longest_streak` for each input.",
        table_w(["Input", "Expected"], [
            ["`[]`", ed(0)], ["`[7]`", ed(1)], ["`[1, 2]`", ed(1)],
            ["`[3, 1, 1]`", ed(2)], ["`[2, 2, 2]`", ed(3)], ["`[1, 1, 2, 2, 2]`", ed(3)]]),
        hints("What is the longest run in each list?",
              "A single number is a run of length 1. An empty list has no run.", "Two different neighbours give runs of 1. In `[1, 1, 2, 2, 2]` the run of 2s has length 3.", ["l1", "l2", "l3"]),
        fb("0, 1, 1, 2, 3 and 3.", "Not quite right. Count each run of equal neighbours.",
           {'r0c1': "An empty list has no run, so the answer is 0.", 'r1c1': "One number is a run of length 1.", 'r2c1': "1 and 2 differ, so each run has length 1.",
            'r3c1': "The two 1s at the end are a run of 2.", 'r4c1': "All three numbers are equal: one run of 3.", 'r5c1': "The 2s are the longest run, with length 3."}),
        explain("An empty list gives 0 and a single number gives 1. Runs only grow while neighbours are equal. The last list has runs of 2 and 3, so its answer is 3.",
                None),
        canvas=rule_console(), pace=120))
    # 3 code A
    ex = [{'call': "caught('m1')", 'expect': True}, {'call': 'well_formed()', 'expect': True}]
    tests = [{'call': f"caught('m{i}')", 'expect': True} for i in range(1, 7)] + [{'call': 'well_formed()', 'expect': True}]
    S.append(screen(
        'problem', 3, 'Write the tests', E1 + ['mutation-tests'],
        "Six wrong versions are hidden. Return at most 8 inputs that tell every one of them apart from the correct function. "
        "The empty list is `[]`.",
        "Write `edge_cases()`.",
        code('python', R.EDGE_STARTER, R.EDGE_SOL, ex, tests,
             "Check runs 7 hidden tests. Six ask whether one wrong version gives a different answer on one of your inputs. The seventh needs at most 8 lists of whole numbers.",
             prelude=R.PRELUDE_16),
        hints("Which bugs does the empty list catch? And a single number?",
              "`[]` catches m2 and `[7]` catches m1 and m3.", "Add `[1, 2]` for m4 and `[3, 1, 1]` for m5 and m6. `[1, 1, 2, 2, 2]` catches four at once.", ["l1", "l2", "l3", "l4", "l5", "l6"]),
        fb("Six inputs catch all six wrong versions.", "Not quite right. Check which test failed.",
           tkeys(7, {1: "Test 1: m1 forgets the last run. Add a list that ends on its longest run.", 2: "Test 2: m2 gives 1 for an empty list. Add `[]`.",
                     3: "Test 3: m3 gives 0 for one number. Add a one-element list.", 4: "Test 4: m4 counts runs that never fall. Add a list with a rise, such as `[1, 2]`.",
                     5: "Test 5: m5 restarts at 0 after a break. Add a run that follows a break.", 6: "Test 6: m6 compares only with the first value. Add a run that does not start the list.",
                     7: "Test 7: return a list of at most 8 lists of whole numbers."})),
        explain("Each input exposes the wrong versions whose answers differ from the correct one. `[]` and `[7]` take the two length cases, and `[1, 2]` takes the rise. `[3, 1, 1]` and `[1, 1, 2, 2, 2]` take the runs after a break.",
                None),
        canvas=console('The six wrong versions', BUG_LINES), pace=480))
    # 4 ladder numeric
    S.append(screen(
        'ladder', 2, 'How many does one input catch', E3,
        "Your tests are marked by the bugs they expose. Run `[3, 1, 1]` through each wrong version in turn.",
        "How many of the six wrong versions give a wrong answer on `[3, 1, 1]`?",
        numeric(3, 'Bugs', '3: m1, m5 and m6', [('one', 1), ('two', 2), ('all', 6)]),
        hints("The correct answer is 2. Which versions return something else?",
              "m1 returns 1, because the last run is never recorded.", "m5 and m6 return 1 as well. m2, m3 and m4 return 2.", ["l1", "l3", "l5", "l6"]),
        fb("m1, m5 and m6 are wrong on `[3, 1, 1]`.", "Not quite right. The correct answer is 2: which versions differ?",
           {'one': "You counted m1 only. m5 and m6 also fail on a run after a break.", 'two': "m1, m5 and m6 all fail. Check each against the answer 2.",
            'all': "m2, m3 and m4 are right on this list. They fail on other inputs."}),
        explain("The correct answer is 2. m1 never records the last run and gives 1. m5 and m6 also give 1 here, so three versions fail.",
                {"shade": {"fails": ["l1", "l5", "l6"]}}),
        canvas=console('The six wrong versions', BUG_LINES), pace=120))
    # 5 trap
    S.append(screen(
        'trap', 2, 'A thousand random lists', E3,
        "You skip the checklist and write a loop. It makes 1,000 random lists of length 5 to 50 and runs each through every wrong version.",
        "Which wrong version can those lists never catch?",
        choice([
            ('a', 'm2, which returns 1 for an empty list', None),
            ('b', 'm4, which counts runs that never fall', "You thought m4 would hide. A random list has many rises, and each one makes m4 count too much."),
            ('c', 'm5, which restarts a run at 0 after a break', "You chose a bug that shows on any run after a break. Random lists of 5 or more hold such runs."),
            ('d', 'm6, which compares only with the first value', "You chose a bug that shows when the longest run does not start the list. Random lists show that often."),
        ]),
        hints("What is the shortest list your loop makes?",
              "Five numbers. It never makes an empty list.", "m2 differs from the correct version only on `[]`, so only a list of length 0 catches it.", ["l2"]),
        fb("Every random list has at least 5 numbers, so the empty list never appears.",
           "Not quite right. Which bug needs a list the loop never makes?",
           {'b': "A list of 5 or more numbers with one rise already exposes m4.", 'c': "Any random list with a run after a break can expose m5.",
            'd': "Any random list whose longest run is not first can expose m6."}),
        explain("The loop makes lists of length 5 to 50, so it never makes the empty list. m2 differs from the correct version only there. Random tests do not replace the empty, single and repeated cases."),
        canvas=console('The six wrong versions', BUG_LINES), pace=120))
    # 6 C++ twin with testkit
    cases = [{"call": "run_tests()", "expect": 0, "compare": "equal"}]
    for n in range(1, 6):
        cases.append({"call": "run_tests() > 0", "expect": True, "compare": "equal", "defines": {f"BUG{n}": 1}})
    cw = {"kind": "code", "language": "cpp", "starter": CPP_STARTER, "solution": CPP_SOL, "testkit": True,
          "examples": [{"call": "run_tests()", "expect": 0, "compare": "equal"}], "tests": cases,
          "how": "Check runs 6 cases. Your tests must all pass the correct function, and each of five planted bugs must make a test fail.",
          "prelude": CPP_PRELUDE, "postlude": CPP_POSTLUDE}
    S.append(screen(
        'problem', 3, 'The same game in C++', E3,
        "Write `TEST` blocks with `CHECK`, as in `cpp` l18. A hidden `longest_streak` and five planted bugs, `BUG1` to `BUG5`, are the same as m1 to m5. "
        "The starter catches only `BUG2`.",
        "Write tests that fail on every bug and pass on the correct version.",
        cw,
        hints("Your starter catches only the empty list. What else do the bugs need?",
              "Add a single number, a rise, a run after a break and a run that fills the list.", "Use `{7}`, `{1, 2}`, `{3, 1, 1}`, `{2, 2, 2}` and `{1, 1, 2, 2, 2}`, each with the expected value worked out by hand.", ["l1", "l2", "l3", "l4"]),
        fb("Six tests pass the correct version and fail every bug.", "Not quite right. Check which case failed.",
           {"test-1": "Test 1: a test of yours fails on the correct function. Check the expected values.", "test-2": "Test 2: BUG1 passed your tests. Add a list that ends on its longest run.",
            "test-3": "Test 3: BUG2 passed your tests. Check the empty-list test.", "test-4": "Test 4: BUG3 passed your tests. Add a one-element list.",
            "test-5": "Test 5: BUG4 passed your tests. Add a list with a rise, such as `{1, 2}`.", "test-6": "Test 6: BUG5 passed your tests. Add a run that follows a break."}),
        explain("`run_tests()` counts the failing tests. The first case wants 0 on the correct version, so your expected values must be right. Each later case switches on one bug and wants at least one failure."),
        canvas=console('testkit in C++', [
            "TEST(name) { CHECK(condition); } registers a test.",
            "run_tests() returns how many tests failed.",
            "The hidden function has five bugs, switched on one at a time."]), pace=480))
    # 7 ladder table families
    S.append(screen(
        'ladder', 2, 'Edge cases by family', E1,
        "Edge inputs come in families: strings, then intervals, then numbers. For each call, work out the answer.",
        "Fill in the expected value of each call.",
        table_w(["Call", "Expected"], [
            ['`longest_run("")`', ed(0)], ['`longest_run("zzz")`', ed(3)],
            ["`blocks([[1, 2], [2, 3]])`", ed(1)], ["`blocks([[1, 9], [3, 4]])`", ed(1)],
            ["`digits(0)`", ed(1)], ["`digits(-45)`", ed(2)]]),
        hints("Each call is the edge of its family: empty, touching, nested, zero, negative.",
              "Closed intervals that share an end join into one block.", "`[3, 4]` lies inside `[1, 9]`, so one block. Zero has one digit, and the sign is not a digit.", ["l1", "l2", "l3"]),
        fb("0, 3, 1, 1, 1 and 2.", "Not quite right. Think about what the edge input does.",
           {'r0c1': "An empty string has no letters and no run, so 0.", 'r1c1': "Three equal letters are one run of 3.",
            'r2c1': "Closed intervals that touch at 2 join, so one block.", 'r3c1': "`[3, 4]` lies inside `[1, 9]`, so one block.",
            'r4c1': "Zero is written with one digit.", 'r5c1': "`-45` has two digits. The sign is not a digit."}),
        explain("Each row is the edge of one family. The empty string, touching and nested intervals, and zero and negatives are where solutions slip. Write them before the code, with answers worked out by hand.",
                None),
        canvas=console('Three small functions', [
            "longest_run(s): the longest run of one letter in a string.",
            "blocks(spans): how many blocks the closed intervals merge into.",
            "digits(n): how many digits the whole number n has, ignoring its sign."]), pace=150))
    # 8 generalise order
    S.append(screen(
        'generalise', 2, 'Tests before code', E2,
        "Before the code, write the edge inputs down as a checklist of comments.\n\n"
        "```python\n# arrays:    [], [x], [x, x], all equal, sorted, reversed, negatives\n# strings:   \"\", \"a\", repeated letters\n"
        "# intervals: touching, nested, identical\n# numbers:   0, negative, largest\n```",
        "Put the test-first steps in order. Leave out the step that does not belong.",
        order([
            ('t1', 'List the empty, single, repeated and boundary inputs', None),
            ('t2', 'Write each expected output by hand', None),
            ('t3', 'Write a stub that returns a wrong value', None),
            ('t4', 'Run the tests and watch them fail', None),
            ('t5', 'Write the real solution', None),
            ('t6', 'Run the tests again', None),
            ('d1', 'Write the solution, then pick tests it passes', "Then the solution picks the tests, so they cannot catch its own mistakes."),
        ], ['t1', 't2', 't3', 't4', 't5', 't6'], distractors=['d1'], same=[['t2', 't3']]),
        hints("Why watch the tests fail?",
              "A test that cannot fail proves nothing.", "List the inputs and expected outputs, then run them on a stub to see them fail. Write the real code and see them pass."),
        fb("List, expect, stub, fail, solve, pass.", "Not quite right. The tests come before the solution.",
           {'d1': "You let the solution choose the tests. Tests written after the code tend to pass it.", 'left-out': "Six steps belong. Only picking tests after the solution is wrong.",
            't5': "The real solution comes after the tests have failed on the stub."}),
        explain("The inputs and their expected outputs fix what right means. A stub shows the tests can fail, and only then do we write the solution. A second run shows that it passes.",
                None),
        canvas=rule_console(), pace=120))
    # 9 transfer multi merge_intervals
    S.append(screen(
        'transfer', 3, 'Tests for merge_intervals', E1,
        "You will write `merge_intervals(spans)`, as in l1. The spans are closed. Time is short and you may write only a few tests first.",
        "Select all that apply: which three inputs are worth writing first?",
        multi([
            ('a', '`[]`', None),
            ('b', '`[[2, 5], [5, 9]]`, a touching pair', None),
            ('c', '`[[1, 10], [3, 4]]`, a nested pair', None),
            ('d', '`[[1, 3], [6, 9], [12, 15]]`, three apart', "You chose the ordinary case. Almost any solution passes it, so it catches no slip."),
            ('e', '`[[0, 2], [5, 6]]`, two apart', "You chose another ordinary case. A gap between spans is not where solutions fail."),
        ]),
        hints("Where do interval solutions slip?",
              "At the ends: empty, touching and nested.", "Choose the empty list, the touching pair and the nested pair. The spread-out inputs pass almost any code.", ["l1"]),
        fb("The empty list, the touching pair and the nested pair.", "Not quite right. Choose the three edges, not the ordinary inputs.",
           {'d': "Spans that are far apart pass any merge, right or wrong.", 'e': "Two spans with a gap pass any merge, right or wrong."}),
        explain("Merges go wrong on the empty list, a touching pair and a nested pair. Those are a missed join, a missed end and a shorter end taken. Spans far apart pass almost any code."),
        canvas=console('merge_intervals(spans)', ["Closed spans [a, b] that overlap or touch join into one.", "The result is sorted by start."]), pace=120))
    # 10 transfer numeric 3
    S.append(screen(
        'transfer', 3, 'The shortest test list', E3,
        "Ten candidate inputs: `[]`, `[7]`, `[1, 2]`, `[3, 1, 1]`, `[2, 2, 2]`, `[1, 1, 2, 2, 2]`, `[1, 1]`, `[2, 1]`, `[1, 2, 2]` and `[6, 6, 6, 1]`. "
        "Choose the fewest that expose all six wrong versions.",
        "How many inputs do you need at least?",
        numeric(3, 'Inputs', '3: `[]`, `[7]` and `[1, 1, 2, 2, 2]`', [('two', 2), ('four', 4), ('six', 6)]),
        hints("Only `[]` catches m2. Which input catches m3?",
              "`[]` catches m2 and `[7]` catches m1 and m3.", "`[1, 1, 2, 2, 2]` catches m1, m4, m5 and m6. Together the three expose all six.", ["l2", "l3", "l6"]),
        fb("Three inputs expose all six.", "Not quite right. Count which versions each input catches.",
           {'two': "Two inputs cannot cover m2, m3 and m4 to m6 together.", 'four': "Three already do it, so four is not the fewest.", 'six': "One input per bug is not the fewest, because one input can catch several."}),
        explain("Only `[]` catches m2 and only `[7]` or a one-element list catches m3. `[1, 1, 2, 2, 2]` catches m1, m4, m5 and m6 at once. Trying every subset of the ten finds nothing smaller than three."),
        canvas=console('Which input catches which', [
            "[]: m2.", "[7]: m1, m3.", "[1, 2]: m4.", "[3, 1, 1]: m1, m5, m6.", "[2, 2, 2]: m1.", "[1, 1, 2, 2, 2]: m1, m4, m5, m6."]), pace=150))
    # 11 transfer choice
    S.append(screen(
        'transfer', 2, 'What to say first', E2,
        "In a live round you are given `longest_streak`. The interviewer watches how you start, so say your plan aloud before you type.",
        "Which opening line is best?",
        choice([
            ('a', 'I will start with empty, single, repeated and boundary inputs.', None),
            ('b', 'I will code it first and add tests after it passes.', "You let the solution choose the tests. Tests written afterwards tend to pass it."),
            ('c', 'I will run a thousand random lists and trust them.', "You skipped the cases random lists never make, such as the empty list."),
            ('d', 'I will test only the example in the statement.', "You chose one input. A single example misses most of the bugs."),
        ]),
        hints("What do you want the interviewer to hear?",
              "That you have a method for the inputs that break code.", "Name the families aloud: empty, single, repeated, boundary.", ["l1"]),
        fb("Naming the edge families shows a method before any code.", "Not quite right. Choose the line that names a method.",
           {'b': "Tests written after the code are chosen to fit it.", 'c': "Random lists never include the empty list.", 'd': "One example exposes very few of the bugs."}),
        explain("Saying the families aloud shows the plan and starts the tests before the code. It also gives you the checklist as you work."),
        canvas=rule_console(), pace=90))

    quiz = [
        item('q-expose', 2, None, E3, "A wrong version returns the length of the first run only. Which input exposes it?",
             choice([('a', '`[1, 4, 4]`', None),
                     ('b', '`[4, 4, 1]`', "You chose a list whose first run is also the longest. The wrong version gives 2, which is right."),
                     ('c', '`[5, 5, 5]`', "You chose a list with one run. The first run is the longest, so the wrong version is right."),
                     ('d', '`[7]`', "You chose a single number. Its first run is its only run.")]),
             fb("On `[1, 4, 4]` the wrong version gives 1 and the right answer is 2.", "Not quite right. The first run must be shorter than a later one.",
                {'b': "The first run is longest here, so both versions give 2.", 'c': "One run only: both versions give 3.", 'd': "One run only: both versions give 1."}),
             explain("To expose a first-run-only version, make a later run longer than the first. `[1, 4, 4]` has a first run of 1 and a later run of 2."), quiz=True),
        item('q-expected', 2, None, E1, "What is `longest_streak([8, 8, 3, 8, 8, 8])`?",
             numeric(3, 'Length', '3: the last three 8s', [('first', 2), ('count', 5)]),
             fb("The last three 8s are the longest run: 3.", "Not quite right. Equal neighbours only: the 3 breaks the 8s.",
                {'first': "You stopped at the first run of 2. A longer run follows the 3.", 'count': "You counted all five 8s. The 3 splits them into runs of 2 and 3."}),
             explain("The 3 splits the 8s into a run of 2 and a run of 3. The longest is 3."), quiz=True),
        item('q-random', 3, None, E3, "Why can random tests miss a bug?",
             choice([('a', 'They seldom make cases such as the empty list', None),
                     ('b', 'They repeat the same list again and again', "You thought random lists repeat. They differ each time, but they share a typical shape."),
                     ('c', 'They are too slow to run on large inputs', "Speed is not the problem. A million lists run quickly and still miss the empty list."),
                     ('d', 'They only find bugs in the last run of a list', "You tied random tests to one bug. Their weakness is the special case.")]),
             fb("Random lists have a typical shape, so special cases are rare or absent.", "Not quite right. Think about what a random list looks like.",
                {'b': "Random lists differ, but none of them is special.", 'c': "Running time is not the issue.", 'd': "No bug is tied to the last run only."}),
             explain("Random lists are typical lists. The empty list, one number and a list that is all equal are special, and a generator seldom makes them."), quiz=True),
        item('q-family', 2, None, E1, "You write tests for a function that reverses a string. Which input family do you add first?",
             choice([('a', 'The empty string and one letter', None),
                     ('b', 'The longest string you can build', "You chose size first. Short inputs expose more slips than long ones."),
                     ('c', 'A string with every letter of the alphabet', "You chose a rich string. Rich strings pass a lot of broken code."),
                     ('d', 'A string copied from the statement', "You chose the example. The example is the case the setter knew would work.")]),
             fb("The empty string and one letter come first.", "Not quite right. Start with the smallest inputs.",
                {'b': "Large inputs test speed, not the edge.", 'c': "A rich string rarely exposes a slip.", 'd': "The example in the statement passes most attempts."}),
             explain("Empty and one-letter inputs are where loops and indexes slip. They go first, before the larger cases."), quiz=True),
    ]
    return {
        "id": "l16-edge-cases-first", "course": "coding-int", "title": "Edge cases first", "minutes": 13,
        "objectives": ["List edge cases and write tests before the solution."],
        "skills": ["ci-timed"], "screens": S,
        "summary": summary(
            ["Before the code, list the empty, single, repeated and boundary inputs and write each expected output by hand.",
             "Run the tests on a wrong version first. A test that cannot fail proves nothing.",
             "Planted bugs mark a test list. A good list exposes every bug with few inputs."],
            "Checklist", "\\text{empty},\\ \\text{single},\\ \\text{repeated},\\ \\text{boundary}",
            "Write these before the solution, and say them aloud.",
            "Relying on random tests, which rarely make the empty list."),
        "quiz": quiz,
    }
