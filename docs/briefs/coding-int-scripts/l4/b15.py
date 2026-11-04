from lib2 import *
import refs4 as R

T1 = ['oa-triage']
T2 = ['partial-credit']
T3 = ['timed-plan']

BIG_SETUP = ("import random; random.seed(1); "
             "ps = [(lambda fm, fp: [fp, fm, random.randint(1, fp), random.randint(2, fm)])"
             "(random.randint(5, 40), random.randint(10, 100)) for _ in range(60)]")

PROB_LINES = [
    "P1: 40 points in 20 minutes. The small groups alone: 12 points in 6.",
    "P2: 60 points in 35 minutes. The small groups alone: 25 points in 12.",
    "P3: 90 points in 50 minutes. The small groups alone: 30 points in 18.",
]


def asm_console(extra=None, title="Assessment of 65 minutes. Reading takes 3, so the budget is 62."):
    return console(title, PROB_LINES + (extra or []))


def lesson():
    S = []
    # 1 hook
    S.append(screen(
        'problem', 1, 'Which problem pays best per minute', T1 + ['timed-plan'],
        "Reported assessments set two problems in 60 minutes, or three in 90, and score by hidden test groups. "
        "You ranked problems in `contests` l14-which-first. New here: partial credit and a minute budget.",
        "Which problem earns the most points per minute if you solve it in full?",
        choice([
            ('a', 'P1', None),
            ('b', 'P2', "You picked the middle problem. Its $60 / 35 \\approx 1.71$ is the lowest rate of the three."),
            ('c', 'P3', "You picked the biggest score. Its rate is $90 / 50 = 1.8$, and P1 earns 2.0."),
            ('d', 'They tie', "You assumed the rates match. They are 2.0, 1.71 and 1.8."),
        ]),
        hints("Divide each full score by its full minutes.",
              "P1 is 40 points in 20 minutes.", "P1: 40 / 20 = 2.0. P2: 60 / 35 = 1.71. P3: 90 / 50 = 1.8.", ["l1"]),
        fb("P1 pays 2.0 points a minute, ahead of P3 at 1.8 and P2 at 1.71.",
           "Not quite right. Points divided by minutes gives the rate.",
           {'b': "$60 / 35$ is about 1.71, the lowest rate.", 'c': "P3 has the most points, but $90 / 50 = 1.8$ is below 2.0.",
            'd': "The three rates are 2.0, 1.71 and 1.8."}),
        explain("Divide each score by its minutes: 2.0, 1.71 and 1.8. The largest score, P3, is not the best price per minute.",
                {"shade": {"best": ["l1"]}}),
        canvas=asm_console(), pace=120))
    # 2 ladder numeric greedy
    S.append(screen(
        'ladder', 2, 'Take them by rate', T1 + ['timed-plan'],
        "Take whole problems in order of points per minute: P1, then P3, then P2. Skip any that no longer fits in the 62 minutes. Nothing partial yet.",
        "How many points does that earn?",
        numeric(100, 'Points', '100: P1 (20 minutes) and P2 (35 minutes), 55 minutes in all',
                [('over', 130), ('all', 190), ('one', 40)]),
        hints("After P1, how many minutes remain?",
              "62 - 20 = 42 minutes remain. P3 needs 50.", "P3 does not fit, so skip it. P2 needs 35 and fits: 40 + 60 = 100.", ["l1", "l3"]),
        fb("P1 and P2 fit in 55 minutes and earn $40 + 60 = 100$.",
           "Not quite right. Check the minutes left before each pick.",
           {'over': "You took P1 and P3, which needs 70 minutes. The budget is 62.", 'all': "You took all three. They need 105 minutes.",
            'one': "You stopped at P1. After 20 minutes, 42 remain and P2 needs only 35."}),
        explain("P1 leaves 42 minutes, so P3 at 50 minutes is skipped. P2 fits, and the plan earns $40 + 60 = 100$ in 55 minutes.",
                {"shade": {"taken": ["l1", "l2"]}}),
        canvas=asm_console()))
    # 3 ladder table: best plan
    S.append(screen(
        'ladder', 3, 'Mix full and partial', T2,
        "Now each problem may be full, partial or skipped. Fill the plan that earns the most inside 62 minutes. Enter 0 for a problem you skip.",
        "Which minutes and points do you plan for P2, for P3 and in total?",
        table_w(["Problem", "Minutes", "Points"], [
            ["P1 (skipped)", "0", "0"],
            ["P2", ed(12), ed(25)],
            ["P3", ed(50), ed(90)],
            ["Total", ed(62), ed(115)],
        ]),
        hints("Which problem is worth the most? Give it full marks first.",
              "P3 in full takes 50 minutes and leaves 12.", "12 minutes buys the partial of P2: 25 points. The total is 62 minutes and 115 points.", ["l3"]),
        fb("P3 in full and P2 in part use exactly 62 minutes and earn $90 + 25 = 115$.",
           "Not quite right. After P3 in full, spend the last 12 minutes.",
           {'r1c1': "P2's partial takes 12 minutes. Its full marks take 35.", 'r1c2': "P2's partial is worth 25 points.",
            'r2c1': "P3 in full takes 50 minutes.", 'r2c2': "P3 in full is worth 90 points.",
            'r3c1': "Add 12 and 50.", 'r3c2': "Add 25 and 90."}),
        explain("P3 in full takes 50 minutes and leaves 12. That is exactly the partial of P2, worth 25. The plan earns 115, more than the 100 of full marks alone.",
                {"shade": {"plan": ["l2", "l3"]}}),
        canvas=asm_console()))
    # 4 code
    ex = [([[30, 15, 10, 5], [50, 30, 20, 10], [80, 45, 25, 15]], 55), ([[40, 20, 30, 5]], 10)]
    ex = [{'call': f"best_plan({a!r}, {b})", 'expect': R.best_plan(a, b)} for a, b in ex]
    tests = [{'call': f"best_plan({p!r}, {b})", 'expect': e} for p, b, e in R.BP_TESTS]
    tests.append({'setup': BIG_SETUP, 'call': 'best_plan(ps, 600)', 'expect': 2724})
    S.append(screen(
        'problem', 3, 'The best plan, in code', T2 + ['best-plan'],
        "Listing every choice is $3^n$ plans, which fails on a long paper. Build a table over minutes instead, one problem at a time.",
        "Write `best_plan(problems, budget)`.",
        code('python', R.BEST_PLAN_STARTER, R.BEST_PLAN_SOL, ex, tests,
             "Check runs 10 hidden tests. They cover small papers, a zero budget, an empty paper and 60 problems with a budget of 600."),
        hints("What is best[m] before any problem is read?",
              "Zero points for every m. A problem can only improve it.",
              "For each problem, copy best. At each m, try full and partial from best[m - minutes]. Return best[budget].", ["l2", "l4"]),
        fb("One table over minutes, updated once per problem.",
           "Not quite right. Check the first failing test.",
           tkeys(10, {1: "Test 1: P3 in full and P2 in part fit in 55 minutes: 100 points.", 4: "Test 4: with no minutes nothing can be earned.",
                      5: "Test 5: at 14 minutes only a partial fits.", 6: "Test 6: an empty paper earns 0.",
                      7: "Test 7: the partial costs as much as the full, so take the full.",
                      8: "Test 8: the partial costs 5 minutes and fits in 10.",
                      10: "Test 10 has 60 problems. Trying every choice would take $3^{60}$ steps."})),
        explain("For each problem we copy the table, then try full and partial from the row of earlier minutes. Each problem costs one pass over the minutes, so the work is problems times budget. Choosing from the old copy stops one problem being used twice.",
                None),
        canvas=console('best_plan(problems, budget)', [
            "Each problem is [full_points, full_minutes, partial_points, partial_minutes].",
            "Choose full, partial or skip for every problem.",
            "Return the most points earned in at most budget minutes.",
            "best[m] is the most points that m minutes can earn."]),
        pace=900))
    # 5 trap
    S.append(screen(
        'trap', 3, 'Full or nothing', T2,
        "A friend says: partial credit is not worth the minutes. Solve what you can in full and skip the rest. Their plan earns 100 here.",
        "Is 100 the most the three problems can earn in 62 minutes?",
        choice([
            ('a', 'No: P3 in full and P2 in part earn 115', None),
            ('b', 'Yes: P1 and P2 use 55 minutes and nothing else fits', "You ruled out partial credit. P3 in full plus P2's partial fits in exactly 62 minutes."),
            ('c', 'No: P1 and P3 in full earn 130', "You added P1's 20 minutes to P3's 50. That is 70, over the budget of 62."),
            ('d', 'Yes: the partials earn too little to matter', "You judged the partials by their score alone. Their score per minute is 2.0 and 2.08."),
        ]),
        hints("Is there any plan that uses all 62 minutes?",
              "Try P3 in full: 50 minutes, 90 points.", "That leaves 12 minutes, exactly the partial of P2: 25 points. The plan earns 115.", ["l2", "l3"]),
        fb("115 beats 100: the partial of P2 fills the gap left by P3.",
           "Not quite right. Try giving P3 full marks first.",
           {'b': "You ruled out partial credit. 12 spare minutes buy 25 points from P2's partial.",
            'c': "P1 and P3 in full need 70 minutes. The budget is 62.",
            'd': "The partials pay 2.0 and 2.08 points a minute, as good as any full."}),
        explain("Full marks only gives 100. P3 in full and P2's partial use all 62 minutes and earn 115. A plan with no partials cannot reach it.",
                {"shade": {"plan": ["l2", "l3"]}}),
        canvas=asm_console(), pace=120))
    # 6 ladder: test groups
    S.append(screen(
        'ladder', 2, 'Test groups', ['partial-credit', 'complexity-read'],
        "A statement lists three groups: $n \\le 1{,}000$, $n \\le 100{,}000$ and $n \\le 1{,}000{,}000$. "
        "Count about $10^8$ steps a second, as in `contests` l2. Mark each group a solution passes.",
        "Fill in Yes or No for each solution and group.",
        table_w(["Solution", "Group 1", "Group 2", "Group 3"], [
            ["O(n^2)", ed('Yes', ['y']), ed('No', ['n']), ed('No', ['n'])],
            ["O(n log n)", ed('Yes', ['y']), ed('Yes', ['y']), ed('Yes', ['y'])],
            ["O(n)", ed('Yes', ['y']), ed('Yes', ['y']), ed('Yes', ['y'])],
        ]),
        hints("Count steps at the top of each group.",
              "A quadratic solution takes $n^2$ steps: $10^6$, then $10^{10}$, then $10^{12}$.",
              "Only $10^6$ is under $10^8$. An $n \\log n$ solution takes about $2 \\times 10^7$ steps at the top group.", ["l1", "l2", "l3"]),
        fb("The quadratic solution earns the first group only. The other two earn all three.",
           "Not quite right. Compare the step count with $10^8$.",
           {'r0c1': "$1{,}000^2 = 10^6$ steps is far under $10^8$.", 'r0c2': "$100{,}000^2 = 10^{10}$ steps is far over $10^8$.",
            'r0c3': "$10^{12}$ steps is far over $10^8$.", 'r1c3': "$10^6 \\times 20 = 2 \\times 10^7$ steps is under $10^8$.",
            'r2c3': "$10^6$ steps is far under $10^8$."}),
        explain("Squaring $10^3$ gives $10^6$ steps, which is fine. Squaring $10^5$ gives $10^{10}$, which is not. The quadratic solution scores the small group and stops there.",
                None),
        canvas=console('Hidden test groups', ["Group 1: n up to 1,000.", "Group 2: n up to 100,000.", "Group 3: n up to 1,000,000."]), pace=120))
    # 7 ladder order: first five minutes
    S.append(screen(
        'ladder', 2, 'The first five minutes', T1,
        "You have the numbers. Now the habit: what you do before you write any code.",
        "Put the first five minutes in order.",
        order([
            ('a1', 'Read every statement to the end', None),
            ('a2', 'Note each limit and the points of each group', None),
            ('a3', 'Estimate the full and partial minutes of each problem', None),
            ('a4', 'Rank by points per minute and settle the partials', None),
            ('a5', 'Set a time box for each problem', None),
            ('a6', 'Start the surest problem', None),
        ], ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']),
        hints("What must you know before you can rank anything?",
              "You need every statement read, with limits and points noted.",
              "Read, note, estimate, rank, box, then start. Code comes last.", ["l1", "l2", "l3"]),
        fb("Read and note first, then estimate, rank and box, and start last.",
           "Not quite right. Ranking needs the estimates, and estimates need the reading.",
           {'a6': "Starting is the last step. Until you have ranked the problems you do not know which is surest.",
            'a4': "Ranking needs the estimates of step 3 first."}),
        explain("You cannot rank problems you have not read, and you cannot rank them without minute estimates. Boxes come after the ranking, and code after the boxes.",
                None),
        canvas=asm_console(), pace=90))
    # 8 generalise + order
    S.append(screen(
        'generalise', 2, 'Plan, then spend', T3,
        "The plan is a table over minutes. Each problem offers a full price and a partial price, and `best[m]` keeps the most points.\n\n"
        "```python\nnew = best[:]\nfor m in range(budget + 1):\n    if m >= full_min:\n        new[m] = max(new[m], best[m - full_min] + full_pts)\n"
        "    if m >= part_min:\n        new[m] = max(new[m], best[m - part_min] + part_pts)\nbest = new\n```",
        "Put the update for one problem in order.",
        order([
            ('s1', 'Copy `best` into `new`, which also covers skipping', None),
            ('s2', 'For each minute count `m`, try the full price from `best[m - full_min]`', None),
            ('s3', 'Try the partial price from `best[m - part_min]` as well', None),
            ('s4', 'Keep the larger of the options in `new[m]`', None),
            ('s5', 'Replace `best` by `new` before the next problem', None),
        ], ['s1', 's2', 's3', 's4', 's5'], same=[['s2', 's3']]),
        hints("What does skipping a problem do to the table?",
              "It leaves every entry as it was, so start from a copy.",
              "Copy first, try both prices, keep the larger, then swap the table in."),
        fb("Copy, try full and partial, keep the larger, then swap.",
           "Not quite right. Skipping is the copy, so it comes first.",
           {'s5': "You swapped too early. The table must be finished before `best` is replaced."}),
        explain("The copy is the skip option. Each price looks back in the old table, so a problem is used at most once. After the pass, the new table replaces the old.",
                None),
        canvas=asm_console(), pace=120))
    # 9 transfer numeric 102
    S.append(screen(
        'transfer', 3, 'A shorter budget', T3,
        "The same three problems, but the assessment is cut and the budget falls from 62 to 60 minutes. The full-marks greedy by rate still earns 100.",
        "What is the most the best plan can earn now?",
        numeric(102, 'Points', '102: P1 and P3 in part, P2 in full (6, 35 and 18 minutes)', [('same', 115), ('greedy', 100), ('low', 90)]),
        hints("Try giving up the biggest problem.",
              "P3 in full takes 50 minutes, leaving 10.", "Instead take P2 in full (35) with partials of P1 (6) and P3 (18): 59 minutes.", ["l1", "l2", "l3"]),
        fb("$12 + 60 + 30 = 102$ in 59 minutes. Nothing else fits for more.",
           "Not quite right. Try mixing full and partial across all three.",
           {'same': "You kept the plan from 62 minutes. P3 in full and P2 in part now needs exactly 62 minutes.", 'greedy': "That is the greedy plan. A mix of partials earns 2 more.",
            'low': "You stopped at P3 in full and a tiny partial. Two partials and P2 in full beat it."}),
        explain("P3 in full plus P2's partial needs 62 minutes, so it no longer fits. The best plan is P2 in full with the partials of P1 and P3. The program and a list of all 27 choices both give 102.",
                {"shade": {"plan": ["l1", "l2", "l3"]}}),
        canvas=asm_console(), pace=180))
    # 10 transfer choice + mock
    S.append(screen(
        'transfer', 3, 'Two problems, 55 minutes', T3,
        "A bank's assessment sets two problems in 60 minutes and reading takes 5. Problem A: 50 points in 40 minutes, or 20 in 12. "
        "Problem B: 60 points in 45 minutes, or 25 in 15. Reading leaves 55 minutes.",
        "Which plan earns the most?",
        choice([
            ('a', 'A in full and B in part: 55 minutes, 75 points', None),
            ('b', 'B in full and A in part: 57 minutes, 80 points', "You added 45 and 12 to get 57. That is over the 55 minutes left."),
            ('c', 'Both in full: 85 minutes, 110 points', "You ignored the budget. Both in full need 85 minutes."),
            ('d', 'Both in part: 27 minutes, 45 points', "You left 28 minutes unused. A full A fits in them."),
        ]),
        hints("List the plans that fit in 55 minutes.",
              "A in full takes 40 and leaves 15.", "15 minutes is exactly B's partial. B in full plus A in part needs 57, which is too many.", ["l1", "l2"]),
        fb("A in full and B in part fill the 55 minutes and earn 75. Nothing else fits for more.",
           "Not quite right. Add the minutes of each plan to the 55 left.",
           {'b': "$45 + 12 = 57$ minutes, which is over 55.", 'c': "$40 + 45 = 85$ minutes, far over 55.", 'd': "$12 + 15 = 27$ minutes leaves 28 minutes idle."}),
        explain("A in full with B in part fills the 55 minutes and earns 75, the most that fits. To rehearse, sit the mock at `#exam/mock-oa-code`: two Python problems in 60 minutes. It scores a problem only when every hidden test passes.",
                None),
        canvas=console('Assessment of 60 minutes. Reading takes 5.', [
            "A: 50 points in 40 minutes. The small groups alone: 20 points in 12.",
            "B: 60 points in 45 minutes. The small groups alone: 25 points in 15."]), pace=150))

    quiz = [
        item('q-rate', 2, None, T1, "Problem X earns 36 points in 24 minutes. Problem Y earns 28 points in 14 minutes. Which has the higher rate?",
             choice([('a', 'Y, at 2.0 points a minute', None),
                     ('b', 'X, because it earns more points', "You compared the scores. Divide by the minutes: X gives 1.5 and Y gives 2.0."),
                     ('c', 'They are equal', "The rates are 1.5 and 2.0."),
                     ('d', 'X, because it takes longer', "A longer problem is not a better one. The rate is points over minutes.")]),
             fb("Y earns $28 / 14 = 2.0$ points a minute, X earns $36 / 24 = 1.5$.", "Not quite right. Divide each score by its minutes.",
                {'b': "You compared the scores, not the rates.", 'c': "$36 / 24 = 1.5$ and $28 / 14 = 2.0$.", 'd': "Taking longer lowers the rate."}),
             explain("A rate is points divided by minutes. X gives 1.5 and Y gives 2.0, so Y pays better per minute."), quiz=True),
        item('q-budget', 2, None, T3, "An assessment lasts 80 minutes. You read for 5 and keep 5 for a final check. How many minutes can you spend on solving?",
             numeric(70, 'Minutes', '70: 80 minus 5 minus 5', [('read', 75), ('full', 80)], None),
             fb("$80 - 5 - 5 = 70$ minutes.", "Not quite right. Take both the reading and the check from 80.",
                {'read': "You took off only the reading. The final check also needs 5 minutes.", 'full': "You used the whole length. Reading and checking come out of it."}),
             explain("The budget is the length minus the reading and the final check. That leaves 70 minutes to spend across the problems."), quiz=True),
        item('q-group', 2, None, ['partial-credit', 'complexity-read'], "A statement has two groups: $n \\le 2{,}000$ and $n \\le 300{,}000$. Your solution takes about $n^2$ steps. Which groups can it pass?",
             choice([('a', 'Only the first: $2{,}000^2 = 4 \\times 10^6$ steps', None),
                     ('b', 'Both: it is correct, so it passes every group', "You checked correctness but not speed. $300{,}000^2$ is $9 \\times 10^{10}$ steps."),
                     ('c', 'Neither: a quadratic solution is always too slow', "You ruled out every quadratic solution. $4 \\times 10^6$ steps is quick."),
                     ('d', 'Only the second: larger groups are easier', "Larger groups are harder. They have more steps.")]),
             fb("The first group needs $4 \\times 10^6$ steps, the second $9 \\times 10^{10}$.", "Not quite right. Square the largest $n$ in each group.",
                {'b': "A correct but slow solution fails the large group by time.", 'c': "$4 \\times 10^6$ steps runs in a blink.", 'd': "More input means more steps, not fewer."}),
             explain("A slow solution still scores the small group. At $10^8$ steps a second, $4 \\times 10^6$ is fast and $9 \\times 10^{10}$ is not."), quiz=True),
        item('q-partial', 3, None, T2, "A problem pays 30 points for 25 minutes in full, or 12 points for 5 minutes in part. You have 8 minutes left. What do you take?",
             choice([('a', 'The partial: 12 points in 5 minutes', None),
                     ('b', 'The full marks: 30 points is worth more', "You compared points and ignored the minutes. Full marks needs 25, and you have 8."),
                     ('c', 'Neither: a partial is not worth submitting', "You ruled out partial credit. It earns 12 points now."),
                     ('d', 'Start the full marks and hope to finish', "You hoped to finish in 8 minutes what needs 25. Take the sure points.")]),
             fb("Only the partial fits in 8 minutes, and it earns 12.", "Not quite right. Compare each price with the 8 minutes left.",
                {'b': "Full marks needs 25 minutes. You have 8.", 'c': "Twelve sure points beat none.", 'd': "A guess at 25 minutes of work in 8 earns nothing."}),
             explain("Full marks needs 25 minutes and only 8 remain. The partial costs 5 and earns 12, so it is the only plan that scores."), quiz=True),
    ]
    # q-order duplicates S7 sense only; keep four quiz items
    return {
        "id": "l15-reading-an-assessment", "course": "coding-int", "title": "Reading an online assessment", "minutes": 13,
        "objectives": ["Triage an assessment's problems and plan the minutes before writing code."],
        "skills": ["ci-timed"], "screens": S,
        "summary": summary(
            ["Read every problem first. Note the limits and the points, and estimate full and partial minutes for each.",
             "Choose full, partial or skip for each problem so the points are most for the minutes you have.",
             "A slow solution still earns the small test groups. Count steps at each group's top $n$."],
            "Rate of a problem", "\\text{rate} = \\dfrac{\\text{points}}{\\text{minutes}}",
            "Rank by rate, then check that a partial does not fill a gap better.",
            "Allowing no partial credit, which leaves minutes unspent."),
        "quiz": quiz,
    }
