from lib2 import *
import refs4 as R

SK = ['ci-timed']
SKD = ['ci-timed', 'ci-design']

H3_SMALL = [([3, -1, -2, 5], 3), ([9, -9], 2), ([], 0), ([8], 0), ([0, 0], 2), ([4, 5, 6], 0), ([-2, 1, 1, -4, 4], 5), ([7, -7, 3], 2), ([2, 4, -6, 1, -1, 5], 5)]
CPP_LZS_STARTER = """#include <vector>
#include <algorithm>
int longest_zero_sum_subarray(std::vector<int> nums) {
    // correct but slow: it tries every start and every end
    int best = 0;
    for (size_t i = 0; i < nums.size(); ++i) {
        long long total = 0;
        for (size_t j = i; j < nums.size(); ++j) {
            total += nums[j];
            if (total == 0) best = std::max(best, (int)(j - i + 1));
        }
    }
    return best;
}
"""
CPP_LZS_SOL = """#include <vector>
#include <unordered_map>
#include <algorithm>
int longest_zero_sum_subarray(std::vector<int> nums) {
    std::unordered_map<long long, int> first;
    first[0] = -1;
    long long total = 0;
    int best = 0;
    for (int i = 0; i < (int)nums.size(); ++i) {
        total += nums[i];
        auto it = first.find(total);
        if (it != first.end()) best = std::max(best, i - it->second);
        else first[total] = i;
    }
    return best;
}
"""

# extra reset rows for the leaderboard (checked against the brute force)
LB_EXTRA = [
    ([[0, 1, 10], [2, 1], [0, 1, 4], [1, 1]], [4]),
    ([[2, 9], [0, 1, 6], [1, 1], [1, 3]], [6, 6]),
]
for ops, e in LB_EXTRA:
    assert R.board_brute(ops) == e == R.run_board(ops), ops


def lb_p1_tests():
    return [{'call': f"run_board({ops!r})", 'expect': e} for ops, e in R.LB_P1]


def lb_p3_tests():
    rows = [R.LB_P3[0], R.LB_P3[3]] + LB_EXTRA
    return [{'call': f"run_board({ops!r})", 'expect': e} for ops, e in rows]


def build():
    items = []
    # 1 parts: leaderboard
    p1 = code('python', R.LB_P1_STARTER, R.LB_P1_SOL,
              [{'call': 'run_board([[0, 1, 5], [0, 1, 7], [1, 1]])', 'expect': [12]}, {'call': 'run_board([[1, 2]])', 'expect': [0]}],
              lb_p1_tests(), "Check runs 4 hidden tests: a score that changes, an empty board, and a `top` larger than the board.", postlude=R.LB_DRIVER)
    p3 = code('python', R.LB_P3_STARTER, R.LB_P3_SOL,
              [{'call': 'run_board([[0, 1, 10], [0, 2, 20], [2, 2], [1, 2]])', 'expect': [10]}, {'call': 'run_board([[1, 2]])', 'expect': [0]}],
              lb_p3_tests(), "Check runs this part's tests and part 1's tests again. A reset player leaves the board.", postlude=R.LB_DRIVER)
    items.append({
        "id": "h4-leaderboard", "difficulty": 4, "skills": SKD, "tags": ['live-round', 'follow-up-layering'],
        "prose": "An interviewer sets a leaderboard and then follows up. `add_score(player, delta)` adds to a player's score. `top(k)` returns the sum of the `k` highest scores. The driver `run_board` is hidden, with rows `[0, player, delta]`, `[1, k]` and `[2, player]`.",
        "parts": [
            {"question": "Write `Leaderboard` with `add_score` and `top`.", "difficulty": 3, "widget": p1,
             "feedback": {"correct": "A dict of scores, sorted when `top` is asked.", "generic": "Not quite right. Check the first failing test.",
                          "byKey": tkeys(4, {1: "Test 1: player 2 gains 51, so the top two are 73 and 107.", 2: "Test 2: player 1 adds 5 and 7, so the score is 12.",
                                             3: "Test 3: an empty board sums to 0.", 4: "Test 4: with 3 players, `top(5)` sums all three."})},
             "explain": {"text": "Keep one score per player in a dict. `top(k)` sorts the scores from the largest and sums the first `k`. A `k` larger than the board just sums everyone."}},
            {"question": "The interviewer says there are 100,000 players and 2,000 `top(10)` calls. What do you change?", "difficulty": 4,
             "widget": choice([
                 ('a', 'Keep a structure of the 10 best scores, updated on each score change', None),
                 ('b', 'Sort once at the start and never update', "You sorted once. Scores change, so the order goes stale."),
                 ('c', 'Use a list of pairs instead of a dict', "You changed the container. Sorting a list every time costs the same."),
                 ('d', 'Recompute `top` only on the first call', "You cached the first answer. Later calls would return old totals."),
             ]),
             "feedback": {"correct": "Maintain the top 10, so a query touches 10 entries.", "generic": "Not quite right. Ask what each query costs now.",
                          "byKey": {'b': "A sort done once is out of date after the next score change.", 'c': "A list sorted on every call costs as much as a dict sorted on every call.",
                                    'd': "A cached total goes wrong as soon as a score changes."}},
             "explain": {"text": "Sorting 100,000 scores for each of 2,000 queries visits 200,000,000 scores. A maintained top 10 touches 10 entries a query. Update it on each score change instead."}},
            {"question": "Now add `reset(player)`, which sets a player's score to zero and removes the player from the board.", "difficulty": 5, "widget": p3,
             "feedback": {"correct": "Pop the player from the dict.", "generic": "Not quite right. Check the first failing test.",
                          "byKey": tkeys(8, {1: "Test 1 is from part 1: `top` must still sum the highest scores.", 5: "Test 5: after players 1 and 2 are reset, `top(2)` reads the players that remain.",
                                             6: "Test 6: a reset player leaves the board, so the later `top` calls sum fewer players.", 7: "Test 7: a reset player who scores again starts from zero.", 8: "Test 8: resetting a player who is not there changes nothing."})},
             "explain": {"text": "`reset` removes the player's entry, so the next `top` cannot see the old score. A later `add_score` then starts from zero. Resetting a player who is not there changes nothing."}},
        ]})
    # 2 parts: calendar follow-ups
    items.append({
        "id": "h4-calendar-follow-ups", "difficulty": 4, "skills": SKD, "tags": ['calendar-booking', 'follow-up-layering'],
        "prose": "A calendar takes 1,200 bookings, one at a time. Each `book` scans the whole list of earlier bookings, and an accepted booking is added to the list.",
        "parts": [
            {"question": "In all, how many booking comparisons does the scan make?", "difficulty": 3,
             "widget": numeric(719400, 'Comparisons', '719,400: 0 + 1 + ... + 1,199', [('square', 1440000), ('once', 1200)]),
             "feedback": {"correct": "$0 + 1 + \\dots + 1{,}199 = 719{,}400$.", "generic": "Not quite right. The first booking scans none and the last scans 1,199.",
                          "byKey": {'square': "You multiplied 1,200 by 1,200. The list starts empty and grows.", 'once': "You counted one scan. Each booking scans all earlier ones."}},
             "explain": {"text": "Booking number $i$ compares with the $i$ bookings before it. The total is $0 + 1 + \\dots + 1{,}199 = 1{,}200 \\times 1{,}199 / 2 = 719{,}400$."}},
            {"question": "Thousands of bookings arrive every second. What do you do for `k = 1`?", "difficulty": 4,
             "widget": choice([
                 ('a', 'Keep the starts and ends sorted and check the neighbours with `bisect`', None),
                 ('b', 'Scan faster by writing the loop in a lower-level language', "You kept the scan. It is still linear in the bookings so far."),
                 ('c', 'Cache only the last booking', "You cached one booking. An earlier booking can still overlap a new one."),
                 ('d', 'Sort the whole list on every `book`', "You sorted every time. That costs more than the scan."),
             ]),
             "feedback": {"correct": "A sorted list with `bisect` checks two neighbours.", "generic": "Not quite right. Ask which bookings can overlap a new one.",
                          "byKey": {'b': "A faster scan is still a scan.", 'c': "Only the neighbours in sorted order matter, not the latest booking.", 'd': "Sorting is more work than scanning."}},
             "explain": {"text": "Accepted bookings never overlap, so sorted order is time order. A new booking can only clash with its left and right neighbours. `bisect` finds them in $O(\\log n)$."}},
            {"question": "A binary search over 1,000,000 bookings needs how many comparisons at most, rounded up to a whole number?", "difficulty": 4,
             "widget": numeric(20, 'Comparisons', '20: the ceiling of log base 2 of 1,000,000', [('half', 500000), ('nineteen', 19)]),
             "feedback": {"correct": "$2^{19} = 524{,}288$ is below $10^6$ and $2^{20} = 1{,}048{,}576$ is above, so 20.", "generic": "Not quite right. Each comparison halves the range.",
                          "byKey": {'half': "You halved once. Each comparison halves the range again.", 'nineteen': "$2^{19}$ is 524,288, which is below a million. You need 20."}},
             "explain": {"text": "Each comparison halves the range, so $n$ bookings need $\\lceil \\log_2 n \\rceil$ comparisons. Here $2^{19} = 524{,}288 < 10^6 < 2^{20} = 1{,}048{,}576$, so the answer is 20."}},
        ]})
    # 3 C++ code
    tests = [cpp_case("longest_zero_sum_subarray", [xs], ["std::vector<int>"], e) for xs, e in H3_SMALL]
    tests.append({"call": "[&]{ std::vector<int> v; for (int i = 0; i < 150000; ++i) { v.push_back(2); v.push_back(-2); } return longest_zero_sum_subarray(v); }()", "expect": 300000, "compare": "equal"})
    tests.append({"call": "[&]{ std::vector<int> v; for (int i = 0; i < 120000; ++i) { v.push_back(3); v.push_back(1); v.push_back(-4); } v.push_back(6); return longest_zero_sum_subarray(v); }()", "expect": 360000, "compare": "equal"})
    cw = {"kind": "code", "language": "cpp", "starter": CPP_LZS_STARTER, "solution": CPP_LZS_SOL,
          "examples": [cpp_case("longest_zero_sum_subarray", [[9, -9]], ["std::vector<int>"], 2), cpp_case("longest_zero_sum_subarray", [[4, 5, 6]], ["std::vector<int>"], 0)],
          "tests": tests, "how": "Check runs 11 hidden tests: nine small ones and two of about 300,000 numbers. The starter is correct but slow."}
    items.append({
        "id": "h4-zero-sum-cpp", "difficulty": 4, "skills": SK, "tags": ['hash-first-seen'], "pace": 1200,
        "prose": "Return the length of the longest contiguous stretch of `nums` that sums to 0, or 0 if there is none. Values may be negative or zero. "
                 "This code is correct but slow. It passes the small groups. Make the large group pass, in C++, as in l17.",
        "question": "Write a fast `longest_zero_sum_subarray` in C++.", "widget": cw,
        "feedback": {"correct": "A map from each prefix sum to its first index.", "generic": "Not quite right. Check the first failing test.",
                     "byKey": tkeys(11, {3: "Test 3: an empty list has no stretch.", 5: "Test 5: two zeros are a stretch of 2.", 7: "Test 7: the stretch of 5 starts at the second number.",
                                         10: "Test 10: 300,000 numbers, and the whole list sums to zero.", 11: "Test 11: the last number spoils the whole list but not the rest."})},
        "explain": {"text": "Store the first index of each prefix sum, starting with 0 at index -1. A repeat marks a stretch that sums to zero, and the first sighting makes it longest. Use `long long` for the running total."}})
    # 4 longform
    lf = {"kind": "longform",
          "prompt": "Say this aloud, timing yourself to six minutes, then write the main points. The problem is `count_subarrays_divisible_by_k`. Restate it and give an example. Name the brute force and its cost. "
                    "Give the prefix-remainder idea, write the plan as comments and state the complexity. Use `[7, -2, 9, 4, -5, 6]` with `k = 5`.",
          "model": "**Restate.** Count the non-empty contiguous subarrays whose sum is divisible by `k`.\n\n"
                   "**Example.** For `[7, -2, 9, 4, -5, 6]` and `k = 5` the answer is 3. The prefix sums are 0, 7, 5, 14, 18, 13 and 19. Their remainders are 0, 2, 0, 4, 3, 3 and 4. Three pairs of prefixes share a remainder.\n\n"
                   "**Brute force.** Try every start and every end: $n(n + 1)/2$ subarrays. At $n = 300{,}000$ that is 45,000,150,000 steps, far too slow for a 5-second limit.\n\n"
                   "**Idea.** Two prefix sums with the same remainder differ by a multiple of `k`. So the stretch between them is divisible. Count, in a dict, the earlier prefixes with each remainder, starting with `{0: 1}`. Add that count at each step. In C++ fix a negative remainder with `((total + x) % k + k) % k`.\n\n"
                   "**Plan, as comments.** `# seen[r] = earlier prefixes with remainder r`, `# for each x: update remainder, add seen[r], then count it`, `# O(n) time, O(k) memory`.\n\n"
                   "**Complexity.** Linear time, and memory proportional to the number of distinct remainders, at most `k`.",
          "rubric": [
              {"points": 2, "text": "Restates the problem and gives an example with its answer, 3"},
              {"points": 2, "text": "Names the brute force and its cost, 45,000,150,000 steps at 300,000"},
              {"points": 2, "text": "Gives the prefix-remainder idea: equal remainders bound a divisible subarray"},
              {"points": 2, "text": "States the plan before the code, including the dict started at {0: 1}"},
              {"points": 2, "text": "States linear time and memory by remainders, and the C++ negative remainder"}]}
    assert R.csdk([7, -2, 9, 4, -5, 6], 5) == R.csdk_slow([7, -2, 9, 4, -5, 6], 5) == 3
    assert 300000 * 300001 // 2 == 45000150000
    items.append(item('h4-aloud', 5, SK, ['narration'], "Say aloud how you would open a live round on `count_subarrays_divisible_by_k`.", lf,
                      fb("Compare your answer with the model and tick the rubric.", "Mark your answer against the rubric.", None),
                      explain("A good opening restates the problem and gives an example. It names the slow way with its cost, and states the idea before any code.")))
    # 5 numeric
    assert 80000 * 1500 == 120000000 and 80000 // 5 == 16000
    items.append(item('h4-leaderboard-cost', 4, SKD, ['complexity-read'], "A leaderboard has 80,000 players and answers 1,500 `top(5)` queries. Sorting every score for each query visits how many scores in all?",
                      numeric(120000000, 'Scores', '120,000,000: 80,000 times 1,500', [('top', 7500), ('once', 80000)]),
                      fb("$80{,}000 \\times 1{,}500 = 120{,}000{,}000$ scores.", "Not quite right. Each query sorts all 80,000 scores.",
                         {'top': "You counted the entries a maintained top 5 would touch. Sorting touches every score.", 'once': "You counted one query. There are 1,500 of them."}),
                      explain("Each query sorts all 80,000 scores, so 1,500 queries visit $80{,}000 \\times 1{,}500 = 120{,}000{,}000$. A maintained top 5 touches 5 entries a query, 7,500 in all. That is 16,000 times fewer.")))
    # 6 order
    items.append(item('h4-first-minutes', 4, SK, ['oa-triage'], "Put the first five minutes of an assessment in order. Leave out the steps that do not belong.",
                      order([
                          ('o1', 'Read every statement to the end', None),
                          ('o2', 'Note the limits and the points of each group', None),
                          ('o3', 'Estimate the full and partial minutes of each problem', None),
                          ('o4', 'Choose full, partial or skip by points per minute and the budget', None),
                          ('o5', 'Start the surest problem', None),
                          ('d1', 'Start with the hardest problem, because it pays most', "You started with the hardest. Its rate may be the lowest, and a long problem can use the whole budget."),
                          ('d2', 'Write code for the first problem before reading the others', "You coded before reading. A later problem may pay better per minute."),
                      ], ['o1', 'o2', 'o3', 'o4', 'o5'], distractors=['d1', 'd2']),
                      fb("Read, note, estimate, choose, then start.", "Not quite right. Choosing needs the estimates.",
                         {'d1': "The hardest problem is not always the best use of the minutes.", 'd2': "You must read every statement before you choose.", 'left-out': "Five steps belong. The two starts that skip the plan do not."}),
                      explain("Reading and noting give the limits and points. Estimates give the minutes, and the choice follows from points per minute. Only then do you start.")))
    # 7 fresh plan
    Q = [[28, 16, 9, 5], [54, 32, 21, 11], [80, 46, 26, 14]]
    assert R.best_plan(Q, 58) == R.best_plan_brute(Q, 58) == 101 and R.greedy_ppm(Q, 58) == 82
    items.append(item('h4-plan', 4, SK, ['timed-plan'], "Problems are `(28, 16, 9, 5)`, `(54, 32, 21, 11)` and `(80, 46, 26, 14)`: full points, full minutes, partial points, partial minutes. The budget is 58 minutes. What is the most a plan can earn?",
                      numeric(101, 'Points', '101: the third in full and the second in part', [('greedy', 82), ('over', 110)]),
                      fb("$80 + 21 = 101$ in 57 minutes.", "Not quite right. Try the largest problem in full first.",
                         {'greedy': "That is the plan with full marks only, by rate. A partial of the second earns 19 more.", 'over': "You added the first partial too. The three need 62 minutes, over 58."}),
                      explain("The third in full takes 46 minutes and leaves 12, enough for the partial of the second at 11. That is 57 minutes and $80 + 21 = 101$ points. Full marks only, by rate, earns 82.")))
    # 8 choice
    assert R.lzs([5, 3, -1, -2, 4, 7]) == R.lzs_slow([5, 3, -1, -2, 4, 7]) == 3
    items.append(item('h4-next-test', 4, SK, ['edge-case-list'], "For `longest_zero_sum_subarray`, your tests so far are `[]`, `[7]`, `[0]` and `[2, -2]`. Which test is most worth adding?",
                      choice([('a', '`[5, 3, -1, -2, 4, 7]`', None),
                              ('b', '`[2, -2, 2, -2, 2, -2]`', "You chose the alternating case again. `[2, -2]` already tests a stretch at the start."),
                              ('c', '`[0, 0, 0, 0, 0, 0]`', "You chose zeros again. `[0]` already tests a single zero."),
                              ('d', '`[1, 2, 3, 4, 5, 6]`', "You chose the no-stretch case again. `[7]` already tests it.")]),
                      fb("The middle stretch is neither a prefix nor the whole list, and the answer is 3.", "Not quite right. Choose a case your tests do not cover.",
                         {'b': "A stretch at the start is already tested by `[2, -2]`.", 'c': "A zero is already tested by `[0]`.", 'd': "A list with no stretch is already tested by `[7]`."}),
                      explain("Your tests cover empty, one number, a zero and a stretch at the start. A stretch in the middle, `3, -1, -2`, is the shape they miss. A solution that only checks prefixes would fail it.")))
    return {"id": "homework-4", "course": "coding-int", "level": 4, "dueDays": 7, "items": items}
