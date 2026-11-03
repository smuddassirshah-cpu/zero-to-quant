from common import *
import itertools

# ---------- numbers, twice ----------
assert 8 * 60 == 480 and F(480, 80) == 6 and 480 // 80 == 6
assert F(120, 50) == F(24, 10)                      # Zetamac 50 is 2.4 s an answer
assert [6 * k for k in (20, 40, 60)] == [120, 240, 360] and [10 * m for m in (2, 4, 6)] == [20, 40, 60]
COSTS = [22, 25, 4, 14, 3, 5, 14, 8, 4, 6]           # random.Random(95), see knapsack search in the report
assert sum(COSTS) == 105
keep = sorted(COSTS)[:8]
assert sum(keep) == 58 and sum(sorted(COSTS)[:9]) == 80
best = [S for S in itertools.combinations(range(10), 8) if sum(COSTS[i] for i in S) <= 60]
assert best == [(2, 3, 4, 5, 6, 7, 8, 9)]            # the only way to answer 8: skip Q71 and Q72
assert not [S for S in itertools.combinations(range(10), 9) if sum(COSTS[i] for i in S) <= 60]
assert 60 - (58 - 28) == 30 and 3 + 4 + 4 + 5 + 6 + 8 == 30   # skipping the 14 s pair too uses 30 s of 60
assert F(1, 4) - F(3, 4) == F(-1, 2) and F(1, 3) - F(2, 3) == F(-1, 3) and F(1, 2) - F(1, 2) == 0
assert 6 + 6 + 30 == 42 and (480 - 42) / 6 == 73 and 3 + 73 == 76 and 30 - 6 == 24 and 24 / 6 == 4
assert F(540, 60) == 9 and [9 * k for k in (15, 30, 45)] == [135, 270, 405]
assert 5 * 10 - 44 == 6
assert sorted([4, 5, 6, 18, 7, 25])[:5] == [4, 5, 6, 7, 18] and 4 + 5 + 6 + 7 + 18 == 40 and 40 + 25 > 60

BLOCK9 = generate(9, BLOCK)
blk, blk_bk = four_option_table(BLOCK9)

fmt_rows = [["Questions", "80, four options each"], ["Time", "8 minutes"], ["Mix", "+, −, ×, ÷, decimals, fractions, %, sequences"]]

screens = []

# 1 hook
screens.append({
    "type": "problem", "difficulty": 1,
    "prose": "Some firms set an arithmetic test of 80 questions in 8 minutes. The mix runs from $291 + 883$ to $\\tfrac23 - \\tfrac12$ and the next term of a sequence. Before any question, work out the pace.",
    "canvas": table_canvas(["The test", "As reported"], fmt_rows, align=["left", "left"]),
    "question": "How many seconds does each question get?",
    "widget": num(6, 0, unit="seconds", label="Seconds a question", accept="6 seconds: 480 s over 80 questions.",
                  wrong=[("per-minute", 10, 0), ("flipped", 0.1, 0.001)]),
    "hints": hints("Turn 8 minutes into seconds first.", "8 minutes is 480 seconds.", "$480 \\div 80 = 6$.", ["r1"]),
    "feedback": {"correct": "480 s over 80 questions: 6 s each.", "generic": "Not quite right. Share 480 seconds over 80 questions.",
                 "byKey": {"per-minute": "10 is the number of questions a minute, $80 \\div 8$. Each one gets 60 s over 10: 6 s.",
                           "flipped": "You divided 8 by 80, which gives minutes: 0.1 of a minute is 6 s."}},
    "explain": {"text": "8 minutes is 480 seconds, and $480 \\div 80 = 6$. Zetamac at 50 is 2.4 s an answer, so this pace is slower. The questions are harder, though, and four options sit beside each one.",
                "canvas": {"highlight": {"rows": [1]}}},
})

# 2 explore
screens.append({
    "type": "explore", "difficulty": 1,
    "prose": "The line is the 8 minutes of the test. Drag the point along it. The caption says how many questions you should have answered by then, at 6 seconds each.",
    "canvas": {"kind": "number-line", "params": {"min": 0, "max": 8, "step": 1, "snap": 0.5},
               "state": {"points": [{"id": "t", "x": 1, "label": "You", "drag": True}]},
               "derive": {"caption": "At {{fixed(t.x, 1)}} minutes, on pace, you have answered {{round(t.x * 10)}} questions."}},
    "question": "Drag to 4 minutes. How many questions should be done by then?",
    "widget": num(40, 0, label="Questions done", accept="40: ten a minute.", wrong=[("times-six", 24, 0), ("minutes", 4, 0)]),
    "hints": hints("Move the point to 4 and read the caption.", "Ten questions fit in each minute.", "$4 \\times 10 = 40$.", ["t"]),
    "feedback": {"correct": "Ten a minute: 40 at 4 minutes, halfway in time and in count.", "generic": "Not quite right. Read the caption with the point at 4 minutes.",
                 "byKey": {"times-six": "You multiplied 4 by 6. Four minutes is 240 s, and $240 \\div 6 = 40$.",
                           "minutes": "4 is the time. The count at 4 minutes is ten a minute: 40."}},
    "explain": {"text": "At 6 s a question, ten fit in a minute. So 4 minutes is 40 questions, exactly half the paper. If you are below that count at 4 minutes, you are behind pace.",
                "canvas": {"points": {"t": {"x": 4}}}},
})

# 3 name: checkpoints
screens.append({
    "type": "problem", "difficulty": 2,
    "prose": "A **checkpoint** is the question you should have reached by a given minute. Write three before you start, and one glance at the clock tells you whether you are on pace.",
    "canvas": {"kind": "number-line", "params": {"min": 0, "max": 8, "step": 1, "snap": 0.5},
               "state": {"points": [{"id": "q20", "x": 0.5, "label": "Q20"}, {"id": "q40", "x": 1, "label": "Q40"}, {"id": "q60", "x": 1.5, "label": "Q60"}],
                         "caption": "Minutes into the test"}},
    "question": "Drag Q20, Q40 and Q60 to the minute when each should be done.",
    "widget": {"kind": "drag-point", "points": [{"id": "q20", "target": 2, "tol": 0.1}, {"id": "q40", "target": 4, "tol": 0.1}, {"id": "q60", "target": 6, "tol": 0.1}]},
    "hints": hints("Twenty questions at 6 s each take how long?", "20 questions take 120 s, which is 2 minutes.", "Q20 at 2, Q40 at 4, Q60 at 6.", ["q20"]),
    "feedback": {"correct": "Q20 at 2, Q40 at 4, Q60 at 6: twenty questions every two minutes.", "generic": "Not quite right. Each block of 20 questions takes 2 minutes.",
                 "byKey": {"q20": "Q20 at 6 s each is 120 s: 2 minutes.", "q40": "Q40 is 240 s: 4 minutes.", "q60": "Q60 is 360 s: 6 minutes."}},
    "explain": {"text": "Every 20 questions is two minutes, so the checkpoints are 2, 4 and 6. Ten seconds behind at a checkpoint is under two questions. Steady up rather than race.",
                "canvas": {"points": {"q20": {"x": 2}, "q40": {"x": 4}, "q60": {"x": 6}}}},
})

# 4 ladder: skip and return
skip_rows = [[f"Q{71 + i}", f"{c} s"] for i, c in enumerate(COSTS)]
screens.append({
    "type": "ladder", "difficulty": 2,
    "prose": "Some tests let you skip and come back. A question that takes 20 s costs three others at 6 s. You have 60 s left and ten questions, with the seconds each would take you.",
    "canvas": {"kind": "table", "params": {"columns": ["Question", "Seconds it takes you"], "rows": skip_rows, "align": ["left", "right"], "tap": "rows"}, "state": {}},
    "question": "Tap the questions to skip, so that you answer as many as possible in 60 s.",
    "widget": {"kind": "tap-regions", "answer": ["r0", "r1"], "countWord": "skipped",
               "wrong": [{"id": "slow-all", "set": ["r0", "r1", "r3", "r6"]}]},
    "hints": hints("Which questions cost the most?", "Q71 and Q72 take 22 s and 25 s.", "Skip those two: the other eight take 58 s.", ["r0", "r1"]),
    "feedback": {"correct": "Skip Q71 and Q72: the other eight take 58 s and all fit.", "generic": "Not quite right. Keep the cheapest questions until the 60 s runs out.",
                 "byKey": {"slow-all": "You skipped the two 14 s questions too. The eight cheapest take 58 s, inside 60, so keep them.",
                           "r0": "Q71 takes 22 s, nearly four quick ones. Skip it.", "r1": "Q72 takes 25 s, the slowest. Skip it first.",
                           "r3": "Q74 takes 14 s, but it still fits: the eight cheapest total 58 s.", "r6": "Q77 takes 14 s, but it still fits: the eight cheapest total 58 s.",
                           "r2": "Q73 takes 4 s. Skipping a quick one wastes the easiest mark.", "r4": "Q75 takes 3 s, the cheapest. Keep it.",
                           "r5": "Q76 takes 5 s. Keep the quick ones.", "r7": "Q78 takes 8 s, which fits easily.", "r8": "Q79 takes 4 s. Keep it.", "r9": "Q80 takes 6 s, exactly on pace. Keep it."}},
    "explain": {"text": "Sorted, the costs run 3, 4, 4, 5, 6, 8, 14, 14, 22, 25. The first eight sum to 58 s; adding 22 would pass 60. Cheapest first always fits the most when every question scores the same.",
                "canvas": {"highlight": {"rows": [0, 1]}}},
})

# 5 ladder: a block of 20, four options
screens.append({
    "type": "ladder", "difficulty": 3, "title": "A block of twenty", "tags": ["drill-eighty-block"],
    "prose": "Twenty questions in the test's mix, four options each. Target: 2 minutes, 6 s a question. Nothing in this lesson is timed by the app, so start your own watch. When the block ends, take one breath, then note your time on paper.",
    "canvas": table_canvas(["Pace", "Target"], [["One question", "6 s"], ["This block", "2 minutes"], ["Then", "one breath"]], align=["left", "left"]),
    "question": "Type the letter of each answer.",
    "widget": blk,
    "hints": hints("Estimate first, then let the last digit choose between close options.", "$41 \\times 24$ must end in 4, which rules out two options.", block_line(BLOCK9) + ".", ["r0"]),
    "feedback": {"correct": "All twenty right. Compare your time with the 2-minute target.", "generic": "Not quite right. Redo the amber rows, and note which kind each one was.", "byKey": blk_bk},
    "explain": {"text": "Each row took one move: left to right, a split product, a missing multiplication, a moved point, a common denominator, 10% first, or a difference. The last digit alone settles many options. The kind that took longest is your next drill."},
})

# 6 follow-up: the reported format
screens.append({
    "type": "ladder", "difficulty": 3, "title": "The follow-up",
    "prose": "Candidates report this test as four options, +1 right and −1 wrong, forward only, with no skipping. The reported pass line is about 50 to 60 net. Rules vary by test and change each cycle. With no skip, a slow question becomes a fast guess.",
    "canvas": table_canvas(["Mark", "Score"], [["Right", "+1"], ["Wrong", "−1"]], align=["left", "right"]),
    "question": "Fill in the average mark of a guess after removing 0, 1 or 2 options.",
    "widget": {"kind": "table", "columns": ["Guess", "Average mark"], "rows": [
        ["Among all 4", cell(-0.5, 0.005, placeholder="mark")], ["Among 3 left", cell(-0.333333, 0.005, placeholder="mark")], ["Among 2 left", cell(0, 0.005, placeholder="mark")]]},
    "hints": hints("A guess among 4 is right 1 time in 4.", "Among 4: $\\tfrac14 \\times 1 + \\tfrac34 \\times (-1)$.", "$-0.5$, $-\\tfrac13$ and $0$.", ["r1"]),
    "feedback": {"correct": "$-0.5$, $-\\tfrac13$, then $0$: each option removed makes the guess cheaper.", "generic": "Not quite right. Weigh +1 and −1 by the chance of each.",
                 "byKey": {"r0c1": "Right 1 time in 4, wrong 3 times: $\\tfrac14 - \\tfrac34 = -0.5$.", "r1c1": "Right 1 time in 3: $\\tfrac13 - \\tfrac23 = -\\tfrac13$.",
                           "r2c1": "Right half the time: $\\tfrac12 - \\tfrac12 = 0$."}},
    "explain": {"text": "A blind guess costs half a mark on average, and removing two options makes it free. So cut options fast, pick one and move on. Level 4 works out when a guess beats a blank."},
})

# 7 trap
trap_rows = [["Q1 and Q2", "6 s each"], ["Q3", "30 s"], ["Q4 onwards", "6 s each"]]
screens.append({
    "type": "trap", "difficulty": 2,
    "prose": "Sam answers Q1 and Q2 in 6 s each, then spends 30 s on Q3 and gets it right. Sam plans to make the time up later.",
    "canvas": table_canvas(["Questions", "Time"], trap_rows, align=["left", "right"]),
    "question": "Sam then keeps exactly 6 s a question. How many questions does Sam reach in 480 s?",
    "widget": num(76, 0, label="Questions reached", accept="76: 438 s left after Q3 fits 73 more.", wrong=[("catch-up", 80, 0), ("five-off", 75, 0)]),
    "hints": hints("Add up the time used by the end of Q3.", "$6 + 6 + 30 = 42$ s, which leaves 438 s.", "$438 \\div 6 = 73$ more, so $3 + 73 = 76$.", ["r1"]),
    "feedback": {"correct": "Q3 cost 24 s over its share: four questions, so Sam reaches Q76.", "generic": "Not quite right. Count the seconds left after Q3, at 6 s each.",
                 "byKey": {"catch-up": "You assumed the 30 s comes back later. At a steady 6 s it never does: the last four questions go unreached.",
                           "five-off": "You took off five questions for 30 s. Q3 itself was answered, so only 24 s were extra: four questions."}},
    "explain": {"text": "Q3 used 24 s more than its share, so four questions at the end are never seen. Rushing the last 30 to catch up only raises the errors. That is the first-minute rule: settle the pace early and let a hard question go."},
})

# 8 generalise
screens.append({
    "type": "generalise", "difficulty": 2,
    "prose": "You shared the time out evenly. For $N$ questions in $T$ seconds, question $k$ is due at $$t_k = \\frac{T}{N}\\,k.$$ The first minute sets that pace. A question that costs far more than $\\tfrac{T}{N}$ is skipped, or cut down and guessed.",
    "question": "For 80 questions in 480 s, when is question 60 due, in seconds?",
    "widget": num(360, 0, unit="seconds", label="Due at", accept="360 s: six minutes.", wrong=[("minutes", 6, 0), ("ten", 600, 0)]),
    "feedback": {"correct": "$t_{60} = 6 \\times 60 = 360$ s, the 6-minute checkpoint.", "generic": "Not quite right. Multiply the pace, 6 s, by 60.",
                 "byKey": {"minutes": "6 is the time in minutes. In seconds it is 360.", "ten": "600 uses 10 s a question. The pace is $480 \\div 80 = 6$ s."}},
    "explain": {"text": "The pace is $\\tfrac{480}{80} = 6$ s, so $t_{60} = 360$ s. That is 6 minutes, the third checkpoint. The same rule works for any test once you know $N$ and $T$."},
})

# 9 derive
screens.append({
    "type": "derive", "difficulty": 3,
    "prose": "Derive the checkpoints for 80 questions in 8 minutes. Put the lines in order, and leave out the one that confuses minutes with seconds.",
    "question": "Put the lines in order.",
    "widget": {"kind": "order", "lines": [
        {"id": "s1", "text": "8 minutes is 480 s, since a minute is 60 s"},
        {"id": "s2", "text": "Each question gets $480 \\div 80 = 6$ s, as every question scores the same"},
        {"id": "s3", "text": "After $k$ questions on pace, $6k$ seconds have passed"},
        {"id": "s4", "text": "So Q20 is due at 120 s, Q40 at 240 s and Q60 at 360 s"},
        {"id": "s5", "text": "That is ten a minute: write 20, 40 and 60 against minutes 2, 4 and 6"},
        {"id": "d1", "text": "Each question gets $8 \\div 80 = 0.1$, so 10 s each", "why": "$8 \\div 80 = 0.1$ is in minutes: 0.1 of a minute is 6 s, not 10 s."}],
        "answer": ["s1", "s2", "s3", "s4", "s5"], "distractors": ["d1"]},
    "hints": hints("Start by putting the time in seconds.", "Then share it out, then multiply by $k$.", "Seconds, share, multiply, the three times, then minutes."),
    "feedback": {"correct": "Seconds, the share, the rule, the three times, then the minutes to write down.", "generic": "Not quite right. Start with the time in seconds.",
                 "byKey": {"d1": "$8 \\div 80 = 0.1$ is in minutes: 0.1 of a minute is 6 s, not 10 s.", "left-out": "Every line except the 10-second one belongs.",
                           "s2": "Share the time out once it is in seconds.", "s3": "The rule for question $k$ comes after the pace.",
                           "s4": "Apply the rule to 20, 40 and 60 after stating it.", "s5": "The minutes to write down come last."}},
    "explain": {"text": "Seconds first, then the share, then $t_k = 6k$. Q20, Q40 and Q60 fall at 120, 240 and 360 s. In minutes that is 2, 4 and 6."},
})

# 10 code
code = {"kind": "code", "language": "python",
        "starter": "def best_skips(costs, budget):\n    # the most questions you can answer within budget seconds\n    ...\n\n\ndef checkpoint_times(n=80, seconds=480, every=20):\n    # when questions every, 2 * every, ... (and the last) are due\n    ...\n",
        "solution": "def best_skips(costs, budget):\n    count, used = 0, 0\n    for c in sorted(costs):\n        if used + c > budget:\n            break\n        used += c\n        count += 1\n    return count\n\n\ndef checkpoint_times(n=80, seconds=480, every=20):\n    marks = list(range(every, n + 1, every))\n    if not marks or marks[-1] != n:\n        marks.append(n)\n    return [seconds * k / n for k in marks]\n",
        "examples": [{"call": "best_skips([5, 4, 20, 6, 5], 20)", "expect": "4", "compare": "equal"}, {"call": "checkpoint_times()", "expect": "[120.0, 240.0, 360.0, 480.0]", "compare": "isclose"}],
        "tests": [{"call": "best_skips([22, 25, 4, 14, 3, 5, 14, 8, 4, 6], 60)", "expect": "8", "compare": "equal"},
                  {"call": "best_skips([5, 4, 20, 6, 5], 20)", "expect": "4", "compare": "equal"},
                  {"call": "best_skips([4, 5, 6, 18, 7, 25], 60)", "expect": "5", "compare": "equal"},
                  {"call": "best_skips([], 60)", "expect": "0", "compare": "equal"},
                  {"call": "best_skips([30], 20)", "expect": "0", "compare": "equal"},
                  {"call": "best_skips([6] * 80, 480)", "expect": "80", "compare": "equal"},
                  {"call": "best_skips([7, 3, 3, 3], 9)", "expect": "3", "compare": "equal"},
                  {"call": "checkpoint_times()", "expect": "[120.0, 240.0, 360.0, 480.0]", "compare": "isclose"},
                  {"call": "checkpoint_times(50, 120, 10)", "expect": "[24.0, 48.0, 72.0, 96.0, 120.0]", "compare": "isclose"},
                  {"call": "checkpoint_times(60, 540, 25)", "expect": "[225.0, 450.0, 540.0]", "compare": "isclose"},
                  {"call": "checkpoint_times(60, 540, 15)", "expect": "[135.0, 270.0, 405.0, 540.0]", "compare": "isclose"},
                  {"call": "checkpoint_times(80, 480, 80)", "expect": "[480.0]", "compare": "isclose"}],
        "how": "Check runs 12 hidden tests: seven skip budgets (exact counts) and five checkpoint lists (math.isclose on each time)."}
screens.append({
    "type": "problem", "difficulty": 3, "title": "Skips and checkpoints in code",
    "prose": "`best_skips(costs, budget)` returns the most questions you can answer in `budget` seconds, given the seconds each costs. `checkpoint_times(n, seconds, every)` returns when questions `every`, `2 * every`, ... are due, with the last question added if the steps miss it.",
    "canvas": table_canvas(["Question", "Seconds it takes you"], skip_rows[:4], align=["left", "right"]),
    "question": "Complete both functions.",
    "widget": code,
    "hints": hints("Sort the costs and keep adding until the next one would pass the budget.", "Question $k$ is due at `seconds * k / n`.", "Use `range(every, n + 1, every)`, then append `n` if it is missing.", ["r0", "r1"]),
    "feedback": {"correct": "Both functions match the lesson: cheapest first, and $t_k = \\tfrac{T}{N}k$.", "generic": "Not quite right. Sort before counting, and multiply the pace by each checkpoint."},
    "explain": {"text": "Sorting first makes the greedy count exact: no other choice fits more questions. `checkpoint_times(60, 540, 25)` adds question 60 because 25 and 50 miss the end. That last time is always the whole test."},
})

# 11 transfer
screens.append({
    "type": "transfer", "difficulty": 3,
    "prose": "Your real online test: 60 questions in 9 minutes, pen and paper allowed. Plan the room first: quiet, a charged laptop, a tested link, a phone out of reach. Then write the checkpoints at the top of your paper.",
    "canvas": table_canvas(["Before the test", "Done"], [["Quiet room, tested link", "✓"], ["Pen and paper, if allowed", "✓"], ["Checkpoints on the paper", "?"]], align=["left", "center"]),
    "question": "Fill in the pace and the three checkpoints, in seconds.",
    "widget": {"kind": "table", "columns": ["Plan", "Seconds"], "rows": [
        ["Pace, one question", cell(9, 0)], ["Q15 due at", cell(135, 0)], ["Q30 due at", cell(270, 0)], ["Q45 due at", cell(405, 0)]]},
    "hints": hints("9 minutes is 540 s.", "$540 \\div 60 = 9$ s a question.", "9, 135, 270 and 405.", ["r2"]),
    "feedback": {"correct": "9 s a question: Q15 at 135 s, Q30 at 270 s, Q45 at 405 s.", "generic": "Not quite right. Find the pace, then multiply by 15, 30 and 45.",
                 "byKey": {"r0c1": "540 s over 60 questions is 9 s.", "r1c1": "$15 \\times 9 = 135$ s, which is 2 min 15 s.",
                           "r2c1": "$30 \\times 9 = 270$ s, which is 4 min 30 s.", "r3c1": "$45 \\times 9 = 405$ s, which is 6 min 45 s."}},
    "explain": {"text": "The pace is $540 \\div 60 = 9$ s, so the checkpoints are 2:15, 4:30 and 6:45. Write them in minutes and seconds, as the test clock shows them. Read the test's own rules on skipping and marking before you start."},
})

quiz = []
w = choice([opt("skips", "Go back to the three skipped questions", correct=True),
            opt("recheck", "Recheck the easy answers from the first block", "You spent the spare time on answers that are most likely right already. A skip is a sure blank until you try it."),
            opt("wait", "Stop: the score is already set", "Unused time scores nothing. Spend it on the skips.")])
quiz.append({"id": "q-finish-early", "difficulty": 2, "prose": "A test that allows skipping. You reach the last question with 40 s left and three questions skipped.",
             "question": "What do you do with the 40 s?", "widget": w,
             "feedback": {"correct": "Return to the skips: each is a blank until you try it.", "generic": "Not quite right. Ask where a mark can still be gained.", "byKey": bykey_from_choice(w)},
             "explain": {"text": "Finishing early is the time skip and return was saving. The skipped questions are the only blanks left. Rechecking easy ones rarely changes a mark."}})
quiz.append({"id": "q-behind-pace", "difficulty": 2, "prose": "80 questions in 8 minutes. At the 5-minute mark you are reading question 44.",
             "question": "How many questions behind pace are you?",
             "widget": num(6, 0, label="Questions behind", accept="6: pace at 5 minutes is Q50.", wrong=[("sign", -6, 0), ("seconds", 36, 0)]),
             "feedback": {"correct": "Pace at 5 minutes is Q50, so you are 6 behind.", "generic": "Not quite right. Find the on-pace question at 5 minutes first.",
                          "byKey": {"sign": "That says ahead. Pace is Q50 and you are at Q44: 6 behind.", "seconds": "36 is the gap in seconds. In questions it is $36 \\div 6 = 6$."}},
             "explain": {"text": "Ten a minute puts pace at Q50 at 5 minutes. You are at Q44, six behind, which is 36 s. Close it by guessing faster, not by rushing every question."}})
quiz.append({"id": "q-blind-guess", "difficulty": 2, "prose": "Four options, +1 for right and −1 for wrong.",
             "question": "What is a blind guess worth on average?",
             "widget": num(-0.5, 0.001, label="Average mark", accept="−0.5: $\\tfrac14 - \\tfrac34$.", wrong=[("chance", 0.25, 0.001), ("cancel", 0, 0.001)]),
             "feedback": {"correct": "$\\tfrac14 - \\tfrac34 = -0.5$.", "generic": "Not quite right. Weigh +1 by the chance of right and −1 by the chance of wrong.",
                          "byKey": {"chance": "0.25 is the chance of being right. The 3 in 4 wrong answers each cost a mark.", "cancel": "+1 and −1 cancel only when right and wrong are equally likely, after removing two options."}},
             "explain": {"text": "Right 1 time in 4 earns $\\tfrac14$; wrong 3 times in 4 costs $\\tfrac34$. On average a blind guess loses half a mark."}})
quiz.append({"id": "q-skip-budget", "difficulty": 3, "prose": "A test that allows skipping. 60 s are left, and the questions would take you 4, 5, 6, 18, 7 and 25 s.",
             "question": "What is the most you can answer?",
             "widget": num(5, 0, label="Questions", accept="5: 4 + 5 + 6 + 7 + 18 = 40 s.", wrong=[("drop-18", 4, 0), ("all", 6, 0)]),
             "feedback": {"correct": "Skip the 25 s one: the other five take 40 s.", "generic": "Not quite right. Keep the cheapest until the next would pass 60 s.",
                          "byKey": {"drop-18": "You skipped the 18 s one too. With it the five take 40 s, still inside 60.", "all": "All six take 65 s, over the 60 s left."}},
             "explain": {"text": "Sorted: 4, 5, 6, 7, 18, 25. The first five take 40 s and the 25 s one would make 65. So five, with 20 s to spare."}})

lesson = {
    "id": "l9-eighty-in-eight", "course": "mental-pressure", "title": "Eighty questions in eight minutes", "minutes": 15,
    "objectives": ["Practise the 80-in-8 format and pace yourself through it."], "skills": ["mp-formats", "mp-speed"],
    "screens": screens,
    "summary": {"ideas": ["80 in 8 is 6 s a question: ten a minute, with Q20, Q40 and Q60 due at 2, 4 and 6 minutes.",
                          "Where skipping is allowed, skip any question far over 6 s and come back; cheapest first fits the most.",
                          "Where it is not, cut options and guess: a blind guess is worth −0.5, and 0 after removing two."],
                "formula": {"name": "Checkpoints", "tex": "t_k = \\dfrac{T}{N}\\,k", "note": "80 questions in 480 s: $t_{40} = 240$ s."},
                "trap": "Spending 30 s on question 3 costs four questions at the end, and the rush raises errors."},
    "quiz": quiz,
}
check_voice(lesson, 'l9')
write('l9-eighty-in-eight.json', lesson)
