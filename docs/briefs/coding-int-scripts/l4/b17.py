from lib2 import *
import refs4 as R

P1 = ['timed-plan']
P2 = ['prefix-sum-count']
P3 = ['hash-first-seen']

CPP_CSDK_STARTER = """#include <vector>
long long count_subarrays_divisible_by_k(std::vector<int> nums, int k) {
    // correct but slow: it checks every subarray
    long long count = 0;
    for (size_t i = 0; i < nums.size(); ++i) {
        long long total = 0;
        for (size_t j = i; j < nums.size(); ++j) {
            total += nums[j];
            if (total % k == 0) ++count;
        }
    }
    return count;
}
"""
CPP_CSDK_SOL = """#include <vector>
#include <unordered_map>
long long count_subarrays_divisible_by_k(std::vector<int> nums, int k) {
    std::unordered_map<int, long long> seen;
    seen[0] = 1;
    long long total = 0, count = 0;
    for (int x : nums) {
        total = ((total + x) % k + k) % k;
        count += seen[(int)total];
        ++seen[(int)total];
    }
    return count;
}
"""

TYP = ["std::vector<int>", "int"]


def csdk_py_tests():
    t = [{'call': f"count_subarrays_divisible_by_k({xs!r}, {k})", 'expect': e} for xs, k, e in R.CSDK_SMALL]
    t.append({'setup': 'xs = [3] * 400000', 'call': 'count_subarrays_divisible_by_k(xs, 3)', 'expect': 80000200000})
    t.append({'setup': 'ys = [1, -1] * 200000', 'call': 'count_subarrays_divisible_by_k(ys, 2)', 'expect': 40000000000})
    return t


def csdk_cpp_tests():
    t = [cpp_case("count_subarrays_divisible_by_k", [xs, k], TYP, e) for xs, k, e in R.CSDK_SMALL]
    t.append({"call": "count_subarrays_divisible_by_k(std::vector<int>(400000, 3), 3)", "expect": 80000200000, "compare": "equal"})
    t.append({"call": "[&]{ std::vector<int> v; for (int i = 0; i < 200000; ++i) { v.push_back(1); v.push_back(-1); } return count_subarrays_divisible_by_k(v, 2); }()",
              "expect": 40000000000, "compare": "equal"})
    return t


def lzs_tests():
    t = [{'call': f"longest_zero_sum_subarray({xs!r})", 'expect': e} for xs, e in R.LZS_SMALL]
    t.append({'setup': 'xs = [1, -1] * 200000', 'call': 'longest_zero_sum_subarray(xs)', 'expect': 400000})
    t.append({'setup': 'ys = [1, 2, -3] * 133333 + [5]', 'call': 'longest_zero_sum_subarray(ys)', 'expect': 399999})
    return t


def statement(lines):
    return console('Statement', lines)


def lesson():
    S = []
    # 1 hook
    S.append(screen(
        'problem', 1, 'The plan for sixty minutes', P1,
        "You sat a timed set in `contests` l13-virtual-contest. This lesson budgets one hour for two problems: 5 minutes to read, 25 for each, 5 to test.",
        "The first problem takes 28 minutes. How many minutes are left for the second, after the reading and the tests?",
        numeric(22, 'Minutes', '22: 60 minus 5, 28 and 5', [('plan', 25), ('notest', 27), ('only', 32)]),
        hints("Take every block from the 60 minutes.",
              "The reading, the first problem and the tests use 5, 28 and 5.", "60 - 5 - 28 - 5 = 22 minutes for the second problem.", ["r0", "r1", "r3"]),
        fb("$60 - 5 - 28 - 5 = 22$ minutes.", "Not quite right. Subtract the reading, the first problem and the tests.",
           {'plan': "You used the plan's 25 minutes. The first problem ran 3 over, so the second loses them.", 'notest': "You took off the reading or the tests but not both. Each is 5 minutes.",
            'only': "You took off only the first problem. The reading and the tests also cost time."}),
        explain("The hour is $5 + 25 + 25 + 5$. A first problem that takes 28 minutes eats 3 minutes of the second. Only 22 remain.",
                {"highlight": {"rows": [2]}}),
        canvas={"kind": "table", "params": {"columns": ["Block", "Minutes"], "rows": [["Read both problems", "5"], ["First problem", "25"], ["Second problem", "25"], ["Tests and edge cases", "5"], ["Total", "60"]]}, "state": {}},
        pace=90))
    # 2 code A python
    ex = [{'call': 'count_subarrays_divisible_by_k([10, 20], 10)', 'expect': 3}, {'call': 'count_subarrays_divisible_by_k([-3, 3], 3)', 'expect': 3}]
    S.append(screen(
        'problem', 3, 'Count by remainder', P2,
        "This code is correct but slow. It passes the small groups. Make the large group pass. "
        "`ds` l7 counted subarrays with a given sum. New here: two prefix sums with the same remainder bound a subarray whose sum is divisible by `k`.",
        "Write a fast `count_subarrays_divisible_by_k(nums, k)`.",
        code('python', R.CSDK_STARTER, R.CSDK_SOL, ex, csdk_py_tests(),
             "Check runs 11 hidden tests: nine small ones and two of 400,000 numbers. A case that runs past 5 seconds stops the rest."),
        hints("Two prefix sums with the same remainder: what lies between them?",
              "A subarray whose sum leaves remainder 0.", "Keep a dict counting each remainder seen, starting with `{0: 1}`. Add the count of the current remainder before you increase it.", ["l1", "l2"]),
        fb("Count how many earlier prefixes share each remainder.", "Not quite right. Check the first failing test.",
           tkeys(11, {1: "Test 1: two subarrays have a sum divisible by 5.", 3: "Test 3: an empty list has no subarray.", 4: "Test 4: every one of the 6 subarrays of zeros counts.",
                      5: "Test 5: Python's `%` is never negative, so negative sums need no fix.", 9: "Test 9: the prefix remainders are 0, 2, 2 and 2.",
                      10: "Test 10: 400,000 numbers. A double loop makes 80 billion steps.", 11: "Test 11: the remainders alternate between 0 and 1."})),
        explain("A prefix sum is the total so far. Two prefixes with the same remainder differ by a multiple of `k`, so each pair bounds one good subarray. Counting pairs with a dict takes one pass.",
                None),
        canvas=statement(["count_subarrays_divisible_by_k(nums, k)", "k is at least 1. Return the number of non-empty subarrays whose sum is divisible by k.",
                          "Values may be negative or zero.", "The starter checks every subarray: correct, but slow."]), pace=1500))
    # 3 ladder numeric 9
    S.append(screen(
        'ladder', 2, 'What partial credit looks like', P1,
        "Run the quadratic starter. It is correct, so tests 1 to 9 pass. Test 10 has 400,000 numbers and runs past 5 seconds, which stops the run.",
        "How many of the 11 tests does the slow code pass?",
        numeric(9, 'Tests', '9: the small cases', [('ten', 10), ('all', 11), ('none', 0)]),
        hints("Which tests have a small input?",
              "Tests 1 to 9. Tests 10 and 11 are large.", "A case that runs too long stops the later cases, so test 11 never runs either.", ["l1", "l2", "l3"]),
        fb("Nine: the small groups pass and the large one stops the run.", "Not quite right. Count the tests the slow code finishes in time.",
           {'ten': "Test 10 has 80 billion steps, so it runs past the limit and fails.", 'all': "Test 11 never runs: test 10 already stopped the run.", 'none': "The small cases are fast, so the slow code passes them."}),
        explain("The double loop is correct on small inputs, so tests 1 to 9 pass. Test 10 runs out of time and stops the run. Partial credit is the score for those nine."),
        canvas=console('The hidden tests', ["Tests 1 to 9: at most 6 numbers each.", "Test 10: 400,000 numbers, 80 billion steps for the double loop.", "Test 11: 400,000 numbers, never reached by a slow solution."]), pace=90))
    # 4 C++ code A
    cw = {"kind": "code", "language": "cpp", "starter": CPP_CSDK_STARTER, "solution": CPP_CSDK_SOL,
          "examples": [cpp_case("count_subarrays_divisible_by_k", [[10, 20], 10], TYP, 3), cpp_case("count_subarrays_divisible_by_k", [[-3, 3], 3], TYP, 3)],
          "tests": csdk_cpp_tests(),
          "how": "Check runs the same 11 tests. The result is a `long long`, as the largest count is 80,000,200,000."}
    S.append(screen(
        'ladder', 3, 'The same count in C++', P2,
        "This code is correct but slow, and the same 11 tests apply. New in C++: `%` of a negative number is negative, so normalise the remainder.",
        "Write the fast version in C++.",
        cw,
        hints("What does `-1 % 3` give in C++?",
              "-1, not 2. The remainder keeps the sign of the sum.", "Use `((total + x) % k + k) % k` so every remainder is 0 to k - 1. Keep `total` and the count in `long long`.", ["l3", "l4"]),
        fb("Normalise the remainder, then count with a map.", "Not quite right. Check which test failed.",
           tkeys(11, {1: "Test 1: two subarrays have a sum divisible by 5.", 5: "Test 5: check a negative sum against `k`.",
                      9: "Test 9: without the fix this returns 1, not 3.", 10: "Test 10: 80 billion steps for a double loop.", 11: "Test 11 needs `long long` for the count."})),
        explain("A negative sum has a negative remainder in C++, so equal remainders could look different. Adding `k` and taking `%` again puts every remainder in 0 to `k - 1`. The count needs `long long` because it reaches 80,000,200,000."),
        canvas=console('C++ remainders', ["-1 % 3 is -1 in C++.", "((-1 % 3) + 3) % 3 is 2.", "Python's % gives 2 directly."]), pace=1500))
    # 5 trap
    S.append(screen(
        'trap', 2, 'Polishing the first problem', P1,
        "You read for 5 minutes. The brute force of problem 1 passes the small groups, and one large test still fails. You keep polishing it until minute 45.",
        "That leaves 15 minutes for problem 2 and its tests. What should you have done at minute 30?",
        choice([
            ('a', 'Submit the partial and move on to problem 2', None),
            ('b', 'Keep polishing: the full marks are worth more', "You let the minutes already spent decide. Problem 2 has none yet, and its partial is free."),
            ('c', 'Drop problem 2 and use the hour on problem 1', "You gave up a whole problem's points for a few more on the first."),
            ('d', 'Start problem 2 but keep problem 1 open', "You split your attention. Switching back and forth loses the thread of both."),
        ]),
        hints("What does problem 2 cost if you never start it?",
              "All of its points.", "At the box you stop, bank the partial and start problem 2. You can come back with spare minutes.", ["r1"]),
        fb("Bank the partial at the box and move on.", "Not quite right. Think about what the unread problem is worth.",
           {'b': "Time already spent is gone whether you keep polishing or not. Spend the next minutes where they earn most.",
            'c': "A whole problem's points are lost to chase a few.", 'd': "Two problems open at once give neither your full attention."}),
        explain("The 30 minutes are spent either way. A second problem started now can earn a partial or a full score. Polishing the first earns only the points of one test.",
                None),
        canvas={"kind": "table", "params": {"columns": ["Block", "Minutes"], "rows": [["Read both problems", "5"], ["Problem 1 polished", "40"], ["Left for problem 2 and tests", "15"]]}, "state": {}},
        pace=90))
    # 6 code B
    ex = [{'call': 'longest_zero_sum_subarray([2, -2])', 'expect': 2}, {'call': 'longest_zero_sum_subarray([1, 2, 3])', 'expect': 0}]
    S.append(screen(
        'problem', 3, 'The longest zero-sum stretch', P3,
        "This code is correct but slow, like the last one. Keep a dict from each prefix sum to the first index where you saw it. When a prefix sum repeats, the stretch between the two sightings sums to zero.",
        "Write a fast `longest_zero_sum_subarray(nums)`.",
        code('python', R.LZS_STARTER, R.LZS_SOL, ex, lzs_tests(),
             "Check runs 11 hidden tests: nine small ones and two of about 400,000 numbers."),
        hints("What does a repeated prefix sum tell you?",
              "The numbers between the two sightings add to zero.", "Start with `{0: -1}`. If the total is in the dict, the stretch is `i - first[total]`. Otherwise store `i`.", ["l1", "l2"]),
        fb("Store the first index of each prefix sum.", "Not quite right. Check the first failing test.",
           tkeys(11, {3: "Test 3: an empty list has no stretch.", 4: "Test 4: a single 7 does not sum to zero.", 5: "Test 5: a single 0 is a stretch of length 1.",
                      6: "Test 6: no stretch sums to zero, so the answer is 0.", 8: "Test 8: the whole list sums to 0, so the answer is 4.",
                      10: "Test 10: 400,000 numbers, and the whole list sums to zero.", 11: "Test 11: the last number spoils the whole list but not the rest."})),
        explain("Equal prefix sums mark a stretch that adds to zero. Keeping the first index of each sum makes the stretch as long as possible. One pass with a dict finds the longest.",
                None),
        canvas=statement(["longest_zero_sum_subarray(nums)", "Return the length of the longest contiguous subarray whose sum is 0, or 0 if there is none.", "Values may be negative or zero.",
                          "The starter tries every start and end: correct, but slow."]), pace=1200))
    # 7 ladder choice first sighting
    S.append(screen(
        'ladder', 2, 'First or latest', P3,
        "Take `[4, -4, 3, -3]`. Its prefix sums, with the empty start, are 0, 4, 0, 3 and 0. The sum 0 is seen at index -1, at index 1 and at index 3.",
        "When a prefix sum repeats, which index does the dict keep?",
        choice([
            ('a', 'The first sighting', None),
            ('b', 'The latest sighting', "You overwrote the first sighting. The stretch from 1 to 3 has length 2, shorter than the whole list."),
            ('c', 'The middle sighting', "You kept a sighting in the middle. Both ends of the stretch then fall short of the longest."),
            ('d', 'Both of them', "You kept every sighting. One index is enough, and the earliest gives the longest stretch."),
        ]),
        hints("Which start gives the longest stretch?",
              "The earliest sighting.", "From index -1 to 3 is length 4. From the latest, 1 to 3, is only 2.", ["l1"]),
        fb("The first sighting gives the longest stretch: here all 4.", "Not quite right. The earliest start is the longest.",
           {'b': "You overwrote the first sighting, so the length was only 2.", 'c': "A middle start loses length at the front.", 'd': "Keeping every sighting wastes memory. The earliest is enough."}),
        explain("The stretch runs from the first sighting to the current index. The earliest start makes it longest, so the dict never overwrites. Here the whole list, length 4, sums to zero."),
        canvas=console('Prefix sums of [4, -4, 3, -3]', ["index -1: 0", "index 0: 4", "index 1: 0", "index 2: 3", "index 3: 0"]), pace=90))
    # 8 E8 session
    S.append(screen(
        'transfer', 3, 'Sit a session', P1,
        "Open `#drill/session` and start a session: two drills, 60 minutes, pattern `prefix-sums` or `hashing`, difficulty 3 to 4. "
        "A C++ learner sets the language to C++. The clock keeps running if you leave.",
        "Which split of the 60 minutes will you set before you start?",
        choice([
            ('a', 'Read 5, first problem 25, second problem 25, tests 5', None),
            ('b', 'Read 0, first problem 30, second problem 30, tests 0', "You dropped the reading and the tests. A misread statement can then cost a whole problem."),
            ('c', 'Read 10, first problem 20, second problem 20, tests 10', "You spent 20 minutes on reading and tests. Each problem lost 5 minutes from its box."),
            ('d', 'Read 5, first problem 45, second problem 5, tests 5', "You gave the first problem every spare minute. The second then has no time to earn a partial."),
        ]),
        hints("The plan of this lesson has four blocks.",
              "5 to read, 25 for each problem and 5 to test.", "Check that the blocks add to 60: 5 + 25 + 25 + 5.", ["r0", "r1", "r2", "r3"]),
        fb("5, 25, 25 and 5 add to 60 and keep a box for each problem.", "Not quite right. Add the blocks and compare them with the plan.",
           {'b': "Zero reading and zero tests leaves no margin for a misread or a missed edge.", 'c': "Ten minutes of reading is too long and each problem gets only 20.", 'd': "A box of 5 minutes cannot earn anything on the second problem."}),
        explain("The four blocks add to 60 and give each problem the same box. After the session the result shows your own split and the tests each drill passed. Compare it with 5, 25, 25 and 5."),
        canvas={"kind": "table", "params": {"columns": ["Block", "Minutes"], "rows": [["Read both problems", "5"], ["First problem", "25"], ["Second problem", "25"], ["Tests and edge cases", "5"]]}, "state": {}},
        pace=120))
    # 9 generalise + order
    S.append(screen(
        'generalise', 2, 'The minute plan', P1,
        "Two medium problems fit in an hour when each has a box.\n\n"
        "```python\n# 00:00 read both, note limits, rank     (5)\n# 00:05 problem 1: brute force, then fast  (25 box)\n"
        "# 00:30 problem 2: brute force, then fast  (25 box)\n# 00:55 tests and edge cases on both        (5)\n```",
        "Put the plan in order.",
        order([
            ('m1', 'Read both statements and note the limits', None),
            ('m2', 'Solve problem 1 inside its 25-minute box', None),
            ('m3', 'Move on at the box and solve problem 2 the same way', None),
            ('m4', 'Spend the last five minutes on tests and edge cases', None),
        ], ['m1', 'm2', 'm3', 'm4']),
        hints("What comes before any code?",
              "Reading, so you know both limits.", "Read, problem 1, problem 2, then tests."),
        fb("Read, problem 1, problem 2, then tests.", "Not quite right. Reading comes first and testing last.",
           {'m4': "Tests come last, after both problems have a solution.", 'm1': "Reading comes first."}),
        explain("Reading first lets you rank the problems. Each box ends with a move, not a polish. The last five minutes catch the edge cases of both."),
        canvas={"kind": "table", "params": {"columns": ["Block", "Minutes"], "rows": [["Read", "5"], ["Problem 1", "25"], ["Problem 2", "25"], ["Tests", "5"]]}, "state": {}},
        pace=90))
    # 10 transfer choice
    S.append(screen(
        'transfer', 3, 'Which first', P1,
        "Reading leaves 50 minutes. Problem A: 50 points in 20 minutes, a prefix-sum count you know. Problem B: 60 points in 40 minutes, but a brute force earns 15 points in 10 minutes.",
        "Which plan do you start?",
        choice([
            ('a', 'A in full, then B by brute force: 30 minutes, 65 points', None),
            ('b', 'B in full first: 60 points, and A gets 10 minutes', "You started the long problem. It uses 40 minutes, and A then earns nothing in 10."),
            ('c', 'Both in full: 60 minutes, 110 points', "You ignored the budget. Both in full need 60 minutes and you have 50."),
            ('d', 'A only, then rest: 50 points', "You left 30 minutes unused. B's brute force adds 15 points in 10 of them."),
        ]),
        hints("Which problem is the surest points?",
              "A: 50 points in 20 minutes.", "Bank A first. B in full needs 40 more, so only its partial fits: 15 points.", ["l1", "l2"]),
        fb("A in full and B's partial earn 65 inside 50 minutes.", "Not quite right. Add the minutes of each plan to the 50 you have.",
           {'b': "$40 + 10 = 50$ minutes, but A earns nothing in 10 minutes.", 'c': "$20 + 40 = 60$ minutes, over the 50.", 'd': "30 minutes remain after A. A partial is still worth 15 points."}),
        explain("Sure points go first, then a partial on the hard one. The mock at `#exam/mock-oa-code` draws two Python problems for 60 minutes. It scores a problem only when every hidden test passes, so a brute-force partial earns nothing there."),
        canvas=console('Reading leaves 50 minutes', ["A: 50 points in 20 minutes.", "B: 60 points in 40 minutes. The brute force: 15 points in 10 minutes."]), pace=150))

    quiz = [
        item('q-left', 2, None, P1, "A 90-minute paper: 6 minutes reading, 8 minutes testing, and the first problem took 37. How many minutes are left for the second?",
             numeric(39, 'Minutes', '39: 90 minus 6, 8 and 37', [('notest', 47), ('first', 53)]),
             fb("$90 - 6 - 8 - 37 = 39$.", "Not quite right. Take the reading, the testing and the first problem.",
                {'notest': "You left out the 8 testing minutes.", 'first': "You took off only the first problem. Reading and testing cost 14 more."}),
             explain("Reading, testing and the first problem use 6, 8 and 37 minutes. Of 90, that leaves 39."), quiz=True),
        item('q-points', 2, None, ['partial-credit'], "Three groups are worth 30, 30 and 40 points, with n up to 500, 5,000 and 200,000. Your code takes about $n^2$ steps. How many points does it earn?",
             numeric(60, 'Points', '60: the first two groups', [('one', 30), ('all', 100)]),
             fb("$5{,}000^2 = 2.5 \\times 10^7$ is quick, so 30 + 30 = 60.", "Not quite right. Square the top $n$ of each group.",
                {'one': "You stopped after the first group. $5{,}000^2$ is only $2.5 \\times 10^7$ steps.", 'all': "$200{,}000^2$ is $4 \\times 10^{10}$ steps, far too many."}),
             explain("The first two groups need at most $2.5 \\times 10^7$ steps. The third needs $4 \\times 10^{10}$. The quadratic code earns the first two groups, 60 points."), quiz=True),
        item('q-box', 2, None, P1, "Your 25-minute box on a problem ends and one large test still fails. What do you do?",
             choice([('a', 'Submit what passes and start the next problem', None),
                     ('b', 'Keep going until it passes', "You let one test hold up the rest of the paper."),
                     ('c', 'Delete the code and begin again', "You threw away the points that already pass."),
                     ('d', 'Skip the testing block to gain time', "Testing is the block that protects the points you have.")]),
             fb("Bank what passes and move on at the box.", "Not quite right. The box is a limit, not a target.",
                {'b': "More minutes here cost minutes elsewhere.", 'c': "Your partial is worth keeping.", 'd': "Skipping the tests risks the points you hold."}),
             explain("A box ends with a move. The partial you hold is worth points, and the next problem has none yet."), quiz=True),
        item('q-first', 3, None, P3, "For `[5, -3, 3]` the prefix sums are 0, 5, 2 and 5. With a first-seen dict, what length does the repeat of 5 give?",
             numeric(2, 'Length', '2: the stretch -3, 3', [('three', 3), ('one', 1)]),
             fb("The first 5 is at index 0 and the repeat at index 2, so the length is 2.", "Not quite right. Subtract the first sighting's index from the current one.",
                {'three': "You counted the whole list. The 5 itself is outside the stretch.", 'one': "You counted one number. The stretch holds -3 and 3."}),
             explain("The sum 5 is first seen at index 0 and again at index 2. The two numbers after the first sighting, -3 and 3, sum to zero. The length is $2 - 0 = 2$."), quiz=True),
    ]
    return {
        "id": "l17-two-in-sixty", "course": "coding-int", "title": "Two problems in sixty minutes", "minutes": 14,
        "objectives": ["Solve two medium problems inside 60 minutes, with a plan for partial credit."],
        "skills": ["ci-timed"], "screens": S,
        "summary": summary(
            ["Split the hour: 5 minutes to read, 25 for each problem and 5 to test. Move on at the box.",
             "A brute force that passes the small groups is partial credit. Bank it, then look for the fast idea.",
             "Prefix sums with a dict count subarrays by remainder and find the longest zero-sum stretch from the first sighting."],
            "Same remainder", "\\text{pairs} = \\sum_r \\binom{c_r}{2}",
            "Here $c_r$ is the number of prefix sums with remainder $r$, and the empty prefix counts.",
            "Polishing the first problem because of the minutes already spent."),
        "quiz": quiz,
    }
