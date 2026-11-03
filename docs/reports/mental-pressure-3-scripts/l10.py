from common import *


def dtable(seq):
    rows = [list(seq)]
    while len(rows[-1]) > 1 and len(set(rows[-1])) > 1:
        r = rows[-1]
        rows.append([b - a for a, b in zip(r, r[1:])])
    return rows


def nbd(seq):
    rows = dtable(seq)
    return None if len(rows[-1]) < 2 else sum(r[-1] for r in rows)


def fib_next(seq):
    return seq[-1] + seq[-2] if all(c == a + b for a, b, c in zip(seq, seq[1:], seq[2:])) else None


# ---------- numbers, twice ----------
assert nbd([3, 7, 11, 15]) == 19 == 15 + 4
assert nbd([1, 3, 6, 10, 15]) == 21 == 15 + 6 and dtable([1, 3, 6, 10, 15])[2] == [1, 1, 1]
assert nbd([2, 6, 12, 20, 30]) == 42 == 6 * 7 and dtable([2, 6, 12, 20, 30]) == [[2, 6, 12, 20, 30], [4, 6, 8, 10], [2, 2, 2]]
assert 10 * 11 == 110 and all(n * (n + 1) == v for n, v in zip(range(1, 6), [2, 6, 12, 20, 30])) and 9 * 10 == 90
assert [3 * 2 ** i for i in range(5)] == [3, 6, 12, 24, 48] and [5 * 3 ** i for i in range(5)] == [5, 15, 45, 135, 405]
t = [3]
for _ in range(5):
    t.append(2 * t[-1] - 1)
assert t == [3, 5, 9, 17, 33, 65]
assert [n * n for n in range(1, 6)] == [1, 4, 9, 16, 25] and [n ** 3 for n in range(1, 5)] == [1, 8, 27, 64]
assert fib_next([1, 1, 2, 3, 5, 8]) == 13 and [1, 10, 2, 20, 3, 30][::2] == [1, 2, 3]
assert nbd([1, 2, 4, 7, 11]) == 16 and dtable([1, 2, 4, 7, 11])[1] == [1, 2, 3, 4]
assert nbd([7, 7, 7, 7]) == 7
m = [150]
for _ in range(4):
    m.append(2 * m[-1] - 50)
assert m == [150, 250, 450, 850, 1650] and nbd([150, 250, 450, 850]) is None and 850 + 400 == 1250
# drill
DRILL = [([4, 9, 14, 19], 24), ([50, 44, 38, 32], 26), ([1, 3, 9, 27], 81), ([2, 5, 10, 17, 26], 37), ([1, 4, 9, 16, 25], 36),
         ([2, 3, 5, 8, 13], 21), ([64, 32, 16, 8], 4), ([1, 8, 27, 64], 125), ([2, 2, 4, 6, 10], 16), ([5, 6, 8, 12, 20], 36),
         ([2, 20, 4, 40, 6, 60], 8), ([2, 3, 5, 7, 11, 13], 17)]
assert nbd(DRILL[0][0]) == 24 and nbd(DRILL[1][0]) == 26 and 27 * 3 == 81 and nbd(DRILL[3][0]) == 37 and nbd(DRILL[4][0]) == 36
assert fib_next(DRILL[5][0]) == 21 and 8 // 2 == 4 and 5 ** 3 == 125 and fib_next(DRILL[8][0]) == 16 and 2 * 20 - 4 == 36
assert all(b == 2 * a - 4 for a, b in zip([5, 6, 8, 12, 20], [6, 8, 12, 20, 36])) and DRILL[10][0][::2] == [2, 4, 6]
assert [p for p in range(2, 18) if all(p % d for d in range(2, p))] == [2, 3, 5, 7, 11, 13, 17]
# quiz
assert nbd([41, 35, 29, 23]) == 17 and [n ** 3 + 1 for n in range(1, 6)] == [2, 9, 28, 65, 126] and 65 + 37 == 102
assert [2, 5, 4, 10, 8, 20][::2] == [2, 4, 8] and fib_next([3, 4, 7, 11, 18]) == 29 and 18 + 7 == 25


def sg(v):
    return "0" if v == 0 else f"{v:+d}".replace("-", "−")


def seq_rows(seq, nxt=None):
    """a vertical difference table: term, first difference, second difference"""
    d1 = [b - a for a, b in zip(seq, seq[1:])]
    d2 = [b - a for a, b in zip(d1, d1[1:])]
    rows = []
    for i, v in enumerate(seq):
        rows.append([str(v), sg(d1[i - 1]) if i >= 1 else "", sg(d2[i - 2]) if i >= 2 else ""])
    return rows


def frame_values(seq):
    rows = seq_rows(seq)
    return {f"r{i}c{j}": rows[i][j] for i in range(5) for j in range(3)}


SEQS = [[3, 7, 11, 15, 19], [1, 3, 6, 10, 15], [3, 6, 12, 24, 48], [2, 3, 5, 7, 11]]
frames = [{"values": frame_values(s), "caption": "Sequence " + "ABCD"[i] + ": " + ", ".join(map(str, s))} for i, s in enumerate(SEQS)]

screens = []

# 1 hook
screens.append({
    "type": "problem", "difficulty": 1,
    "prose": "One question in eight of the test asks for the next term of a sequence. Start with this one.",
    "canvas": table_canvas(["Term", "Gap from the last"], [["3", ""], ["7", "+4"], ["11", "+4"], ["15", "+4"], ["?", ""]], align=["right", "right"]),
    "question": "What comes next: 3, 7, 11, 15, ?",
    "widget": num(19, 0, label="Next term", accept="19: add 4 each time.", wrong=[("first-term", 18, 0), ("doubled", 30, 0)]),
    "hints": hints("Look at the gaps between terms.", "Every gap is +4.", "$15 + 4 = 19$.", ["r3"]),
    "feedback": {"correct": "Each gap is +4, so $15 + 4 = 19$.", "generic": "Not quite right. Find the gap between neighbouring terms.",
                 "byKey": {"first-term": "You added 3, the first term. The gap between terms is 4.", "doubled": "You doubled 15. The terms grow by 4, not by a factor."}},
    "explain": {"text": "The gaps are all +4, so the next term is 19. A sequence with one fixed gap is the fastest kind to spot. Always check the gaps first.",
                "canvas": {"values": {"r4c0": "19", "r4c1": "+4"}}},
})

# 2 explore
screens.append({
    "type": "explore", "difficulty": 1,
    "prose": "Step through four sequences with the control. The table shows each term, the gap from the last term, and the change in that gap.",
    "canvas": {"kind": "table", "params": {"columns": ["Term", "Gap", "Change in gap"], "rows": seq_rows(SEQS[0]), "align": ["right", "right", "right"]},
               "state": {"caption": frames[0]["caption"]},
               "controls": [{"frames": frames, "frameLabels": ["A", "B", "C", "D"], "label": "Sequence", "start": 0}]},
    "question": "In one sequence the gap grows by the same amount each time. What is its next term?",
    "widget": num(21, 0, label="Next term", accept="21: sequence B, whose gaps grow by 1.", wrong=[("same-gap", 20, 0), ("ratio", 96, 0)]),
    "hints": hints("Look for a column of equal changes that is not all zero.", "Sequence B: gaps 2, 3, 4, 5, each up by 1.", "The next gap is 6, so $15 + 6 = 21$.", ["c2"]),
    "feedback": {"correct": "B's gaps grow by 1: the next gap is 6, so 21.", "generic": "Not quite right. Find the sequence whose last column is a constant, not zero.",
                 "byKey": {"same-gap": "You added the last gap, 5, again. B's gaps grow by 1, so the next is 6: 21.",
                           "ratio": "96 continues C, which doubles. Its gaps double too, rather than growing by a fixed step."}},
    "explain": {"text": "In B the gaps 2, 3, 4, 5 each grow by 1. So the next gap is 6 and the next term is 21. A's gaps never change, C's double, and D's follow no step.",
                "canvas": {"values": frames[1]["values"], "caption": frames[1]["caption"]}},
})

# 3 name: the difference table
w = {"kind": "table", "columns": ["Term", "First difference", "Second difference"], "rows": [
    ["2", "", ""], ["6", cell(4, 0), ""], ["12", cell(6, 0), cell(2, 0)], ["20", cell(8, 0), cell(2, 0)], ["30", cell(10, 0), cell(2, 0)],
    [cell(42, 0, placeholder="next"), cell(12, 0), "+2"]]}
screens.append({
    "type": "problem", "difficulty": 2,
    "prose": "You were reading a **difference table**. The gaps are the **first differences**, and the changes in the gaps are the **second differences**. When a row is constant, extend it and add back up.",
    "canvas": table_canvas(["Term", "First difference", "Second difference"], seq_rows([1, 3, 6, 10, 15]), align=["right", "right", "right"]),
    "question": "Fill in the difference table for 2, 6, 12, 20, 30, then the next term.",
    "widget": w,
    "hints": hints("First differences: $6 - 2$, $12 - 6$, and so on.", "They are 4, 6, 8, 10, and each grows by 2.", "Next first difference $10 + 2 = 12$, so $30 + 12 = 42$.", ["c2"]),
    "feedback": {"correct": "Differences 4, 6, 8, 10 grow by 2: next 12, so 42.", "generic": "Not quite right. Subtract each term from the next, then do the same to the differences.",
                 "byKey": {"r1c1": "$6 - 2 = 4$.", "r2c1": "$12 - 6 = 6$.", "r3c1": "$20 - 12 = 8$.", "r4c1": "$30 - 20 = 10$.",
                           "r2c2": "$6 - 4 = 2$.", "r3c2": "$8 - 6 = 2$.", "r4c2": "$10 - 8 = 2$.",
                           "r5c1": "The second differences stay at 2, so the next first difference is $10 + 2 = 12$.",
                           "r5c0": "$30 + 12 = 42$. Adding the last gap, 10, again gives 40, which ignores the growth."}},
    "explain": {"text": "The second differences are all 2, so the next first difference is 12 and the next term 42. Read upwards: $2 + 10 + 30 = 42$. The table for B on the canvas works the same way.",
                "canvas": {"highlight": {"cols": [2]}}},
})

# 4 ladder: ratios
w = {"kind": "table", "columns": ["Sequence", "Next"], "rows": [
    ["3, 6, 12, 24, ?", cell(48, 0)], ["5, 15, 45, 135, ?", cell(405, 0)], ["3, 5, 9, 17, 33, ?", cell(65, 0)]]}
screens.append({
    "type": "ladder", "difficulty": 2,
    "prose": "When the differences never settle, try **ratios**: divide each term by the one before. Some sequences multiply and then adjust: 3, 5, 9, 17 doubles and takes 1 each time.",
    "canvas": table_canvas(["Term", "Gap", "Change in gap"], seq_rows([3, 6, 12, 24, 48]), align=["right", "right", "right"]),
    "question": "Fill in the next term of each.",
    "widget": w,
    "hints": hints("Divide the second term by the first.", "3, 6, 12, 24 doubles; 5, 15, 45 triples.", "48, 405 and $2 \\times 33 - 1 = 65$.", ["c1"]),
    "feedback": {"correct": "48 and 405 by ratio; 65 by doubling and taking 1.", "generic": "Not quite right. Divide each term by the last, then look for a small adjustment.",
                 "byKey": {"r0c1": "Each term doubles: $24 \\times 2 = 48$.", "r1c1": "Each term triples: $135 \\times 3 = 405$.",
                           "r2c1": "Double and take 1: $33 \\times 2 - 1 = 65$. Its gaps 2, 4, 8, 16 double too, giving the same 65."}},
    "explain": {"text": "A doubling sequence has gaps that double too, so its difference table never settles. Ratios catch it at once. For 3, 5, 9, 17, 33, both ways agree on 65."},
})

# 5 ladder: known lists and interleaving
w = {"kind": "table", "columns": ["Sequence", "Next"], "rows": [
    ["1, 4, 9, 16, ?", cell(25, 0)], ["1, 8, 27, ?", cell(64, 0)], ["2, 3, 5, 7, 11, ?", cell(13, 0)], ["1, 1, 2, 3, 5, 8, ?", cell(13, 0)], ["1, 10, 2, 20, 3, 30, ?", cell(4, 0)]]}
screens.append({
    "type": "ladder", "difficulty": 2,
    "prose": "Some sequences are lists to know on sight: squares, cubes, primes, and the Fibonacci rule, where each term adds the two before. Others weave two sequences together: read every other term.",
    "canvas": table_canvas(["List", "Starts"], [["Squares", "1, 4, 9, 16"], ["Cubes", "1, 8, 27, 64"], ["Primes", "2, 3, 5, 7, 11"], ["Fibonacci", "1, 1, 2, 3, 5"]], align=["left", "left"]),
    "question": "Fill in the next term of each.",
    "widget": w,
    "hints": hints("Name the list each one comes from.", "Squares, cubes, primes, Fibonacci, then two sequences woven together.", "25, 64, 13, 13 and 4.", ["r2"]),
    "feedback": {"correct": "25, 64, 13, 13 and 4.", "generic": "Not quite right. Match each to a known list, or split it into odd and even places.",
                 "byKey": {"r0c1": "Squares: $5^2 = 25$.", "r1c1": "Cubes: $4^3 = 64$.", "r2c1": "Primes: 13 follows 11, as 12 is $2 \\times 6$.",
                           "r3c1": "Each term adds the two before: $5 + 8 = 13$.", "r4c1": "Two sequences woven together: 1, 2, 3 and 10, 20, 30. The 7th term is in the first: 4."}},
    "explain": {"text": "These lists defeat differences and ratios, so recognise them on sight. For the woven one, odd places read 1, 2, 3 and even places 10, 20, 30. The next place is odd, so 4."},
})

# 6 follow-up
screens.append({
    "type": "ladder", "difficulty": 3, "title": "The follow-up",
    "prose": "The interviewer follows up on 2, 6, 12, 20, 30: what is the 10th term? Writing out ten terms is slow. Look at each term as a product of two neighbours.",
    "canvas": table_canvas(["Position", "Term", "As a product"], [["1", "2", "1 × 2"], ["2", "6", "2 × 3"], ["3", "12", "3 × 4"], ["10", "?", "?"]], align=["right", "right", "left"]),
    "question": "What is the 10th term of 2, 6, 12, 20, 30?",
    "widget": num(110, 0, label="10th term", accept="110: $10 \\times 11$.", wrong=[("ninth", 90, 0), ("square", 100, 0)]),
    "hints": hints("Term $n$ is $n$ times something.", "$2 = 1 \\times 2$, $6 = 2 \\times 3$, $12 = 3 \\times 4$.", "Term $n$ is $n(n + 1)$, so $10 \\times 11 = 110$.", ["r2"]),
    "feedback": {"correct": "Term $n$ is $n(n + 1)$: $10 \\times 11 = 110$.", "generic": "Not quite right. Write each term as position times the next number.",
                 "byKey": {"ninth": "90 is $9 \\times 10$, the 9th term. The 10th is $10 \\times 11$.", "square": "100 is $10^2$. Each term is $n(n + 1)$, which is $n^2 + n$: 110."}},
    "explain": {"text": "Constant second differences of 2 mean a rule with $n^2$ in it: here $n(n + 1) = n^2 + n$. So the 10th term is 110. Half the second difference is the number in front of $n^2$."},
})

# 7 trap
screens.append({
    "type": "trap", "difficulty": 2,
    "prose": "A candidate sees 1, 2, 4 and starts doubling. Check every term before you commit.",
    "canvas": table_canvas(["Position", "Term"], [["1", "1"], ["2", "2"], ["3", "4"], ["4", "7"], ["5", "11"], ["6", "?"]], align=["right", "right"]),
    "question": "What comes next: 1, 2, 4, 7, 11, ?",
    "widget": num(16, 0, label="Next term", accept="16: the gaps are 1, 2, 3, 4, 5.", wrong=[("doubled", 22, 0), ("first-three", 8, 0), ("same-gap", 15, 0)]),
    "hints": hints("Does doubling give the fourth term?", "$4 \\times 2 = 8$, but the fourth term is 7. Look at the gaps.", "Gaps 1, 2, 3, 4, so the next is 5: $11 + 5 = 16$.", ["r3"]),
    "feedback": {"correct": "The gaps run 1, 2, 3, 4, so the next is 5: 16.", "generic": "Not quite right. Test your rule on every term, then use the gaps.",
                 "byKey": {"doubled": "You doubled 11. Doubling breaks at the fourth term: $4 \\times 2$ is 8, not 7.",
                           "first-three": "You doubled from 1, 2, 4. The fourth term is 7, so doubling is not the rule.",
                           "same-gap": "You added 4, the last gap, again. The gaps grow by 1, so the next is 5."}},
    "explain": {"text": "Three terms fit many rules; the fourth decides. Some test sequences stay ambiguous: 1, 2, 4, 8, 16, 31 counts the regions of a circle cut by chords. Tests expect the simplest rule that fits every term shown.",
                "canvas": {"values": {"r5c1": "16"}}},
})

# 8 generalise (edge case: a constant sequence)
screens.append({
    "type": "generalise", "difficulty": 2,
    "prose": "Each time you extended the last constant row and added back up the table. With last entries $a_n$, $\\Delta_n$ and $\\Delta^2_n$: $$a_{n+1} = a_n + \\Delta_n + \\Delta^2_n + \\cdots$$ If no row settles, try ratios, then known lists, then woven sequences.",
    "question": "What comes after 7, 7, 7, 7?",
    "widget": num(7, 0, label="Next term", accept="7: every difference is 0.", wrong=[("plus-one", 8, 0), ("difference", 0, 0)]),
    "feedback": {"correct": "Every gap is 0, so the next term is still 7.", "generic": "Not quite right. Find the first differences.",
                 "byKey": {"plus-one": "You added 1. The gaps are all 0, so the term does not change.", "difference": "0 is the first difference. The next term is $7 + 0 = 7$."}},
    "explain": {"text": "The sequence itself is the constant row, so $a_{n+1} = 7 + 0$. A constant sequence is the edge case of the rule. It also has ratio 1, so both tests agree."},
})

# 9 derive: the order to try
screens.append({
    "type": "derive", "difficulty": 3,
    "prose": "Put the four tests in the order to try them, fastest and most common first. Leave out the habit that wastes time.",
    "question": "Put the lines in order.",
    "widget": {"kind": "order", "lines": [
        {"id": "s1", "text": "Differences: write the gaps, then their changes; a constant row gives the next term"},
        {"id": "s2", "text": "Ratios: divide each term by the last; look for ×2 or ×3, maybe with a fixed step"},
        {"id": "s3", "text": "Known lists: squares, cubes, primes, the Fibonacci rule"},
        {"id": "s4", "text": "Woven sequences: split odd and even places and solve each"},
        {"id": "d1", "text": "Guess a rule from the last two terms alone", "why": "Two terms fit any rule: 4, 8 could go on to 12 or 16. Use every term."}],
        "answer": ["s1", "s2", "s3", "s4"], "distractors": ["d1"]},
    "hints": hints("Which test covers the most sequences in the fewest seconds?", "Differences catch every polynomial rule; ratios catch growth.", "Differences, ratios, known lists, woven."),
    "feedback": {"correct": "Differences, ratios, known lists, then woven sequences.", "generic": "Not quite right. Start with the test that is quickest to write down.",
                 "byKey": {"d1": "Two terms fit any rule: 4, 8 could go on to 12 or 16. Use every term.", "left-out": "Every line except the two-term guess belongs.",
                           "s2": "Ratios come after differences: they catch what differences miss.", "s3": "Known lists come after the two tests that work by arithmetic.",
                           "s4": "Woven sequences are the last resort: split them only if nothing else fits."}},
    "explain": {"text": "Differences cover fixed gaps and growing gaps in a few seconds. Ratios catch doubling, which differences never settle. Lists and weaving are rarer, so they come last."},
})

# 10 code
code = {"kind": "code", "language": "python",
        "starter": "def difference_table(seq):\n    rows = []\n    # the sequence, then rows of differences until one is constant\n    ...\n    return rows\n\n\ndef next_by_differences(seq):\n    rows = difference_table(seq)\n    total = 0\n    # add each row's last entry, or return None if no row settled\n    ...\n    return total\n",
        "solution": "def difference_table(seq):\n    rows = [list(seq)]\n    while len(rows[-1]) > 1 and len(set(rows[-1])) > 1:\n        row = rows[-1]\n        rows.append([b - a for a, b in zip(row, row[1:])])\n    return rows\n\n\ndef next_by_differences(seq):\n    rows = difference_table(seq)\n    if len(rows[-1]) < 2:\n        return None\n    return sum(row[-1] for row in rows)\n",
        "examples": [{"call": "difference_table([2, 6, 12, 20, 30])", "expect": "[[2, 6, 12, 20, 30], [4, 6, 8, 10], [2, 2, 2]]", "compare": "equal"},
                     {"call": "next_by_differences([2, 6, 12, 20, 30])", "expect": "42", "compare": "equal"}],
        "tests": [{"call": "difference_table([3, 7, 11, 15])", "expect": "[[3, 7, 11, 15], [4, 4, 4]]", "compare": "equal"},
                  {"call": "difference_table([2, 6, 12, 20, 30])", "expect": "[[2, 6, 12, 20, 30], [4, 6, 8, 10], [2, 2, 2]]", "compare": "equal"},
                  {"call": "difference_table([3, 6, 12, 24])", "expect": "[[3, 6, 12, 24], [3, 6, 12], [3, 6], [3]]", "compare": "equal"},
                  {"call": "difference_table([7, 7, 7])", "expect": "[[7, 7, 7]]", "compare": "equal"},
                  {"call": "next_by_differences([3, 7, 11, 15])", "expect": "19", "compare": "equal"},
                  {"call": "next_by_differences([2, 6, 12, 20, 30])", "expect": "42", "compare": "equal"},
                  {"call": "next_by_differences([1, 4, 9, 16])", "expect": "25", "compare": "equal"},
                  {"call": "next_by_differences([1, 8, 27, 64, 125])", "expect": "216", "compare": "equal"},
                  {"call": "next_by_differences([50, 44, 38, 32])", "expect": "26", "compare": "equal"},
                  {"call": "next_by_differences([7, 7, 7, 7])", "expect": "7", "compare": "equal"},
                  {"call": "next_by_differences([3, 6, 12, 24, 48]) is None", "expect": "True", "compare": "equal"},
                  {"call": "next_by_differences([1, 1, 2, 3, 5, 8]) is None", "expect": "True", "compare": "equal"},
                  {"call": "next_by_differences([5, 9]) is None", "expect": "True", "compare": "equal"}],
        "how": "Check runs 13 hidden tests (exact): four tables, then six polynomial sequences and three it should not solve (doubling, Fibonacci, two terms), which return None."}
screens.append({
    "type": "problem", "difficulty": 3, "title": "The table in code",
    "prose": "`difference_table(seq)` returns the rows: the sequence, then its differences, stopping at a constant row or a row of one entry. `next_by_differences(seq)` adds up the last entries when a constant row of two or more exists, and returns `None` otherwise.",
    "canvas": table_canvas(["Term", "First difference", "Second difference"], seq_rows([2, 6, 12, 20, 30]), align=["right", "right", "right"]),
    "question": "Complete both functions.",
    "widget": code,
    "hints": hints("Keep subtracting neighbours while the last row has two or more different values.", "`[b - a for a, b in zip(row, row[1:])]` is one row of differences.",
                   "If the last row has one entry, no row settled: return `None`. Otherwise sum each row's last entry.", ["c1", "c2"]),
    "feedback": {"correct": "Both functions match the lesson's tables.", "generic": "Not quite right. Stop at a constant row, and refuse when only one entry is left."},
    "explain": {"text": "The doubling sequence never reaches a constant row: it shrinks to one entry, so the function says `None`. Two terms are refused the same way, which is right: two terms fit any rule. A constant sequence stops at once and returns itself."},
})

# 11 drill
rows = [[", ".join(map(str, s)) + ", ?", cell(a, 0)] for s, a in DRILL]
notes = ["+5 each time: 24.", "−6 each time: 26.", "×3 each time: 81.", "Gaps 3, 5, 7, 9: next 11, so 37.", "Squares: $6^2 = 36$.",
         "Each term adds the two before: $8 + 13 = 21$.", "Halving: 4.", "Cubes: $5^3 = 125$.", "Each term adds the two before: $6 + 10 = 16$.",
         "Gaps 1, 2, 4, 8 double: next 16, so 36.", "Woven: odd places 2, 4, 6, so 8.", "Primes: 17 follows 13."]
screens.append({
    "type": "problem", "difficulty": 3, "title": "Drill: twelve sequences", "tags": ["drill-sequences"],
    "prose": "Twelve sequences, all with one clear rule. Target pace: 8 seconds each, 96 seconds in all. The app does not time you, so use your own watch. Try differences, then ratios, then lists, then weaving.",
    "question": "Fill in the next term of each.",
    "widget": {"kind": "table", "columns": ["Sequence", "Next"], "rows": rows},
    "hints": hints("Write the first gaps in your head before anything else.", "Rows 3 and 7 multiply; rows 6 and 9 add the two before.", "24, 26, 81, 37, 36, 21, 4, 125, 16, 36, 8, 17."),
    "feedback": {"correct": "All twelve right. Note your time against the 96-second target.", "generic": "Not quite right. Redo the amber rows with the four tests in order.",
                 "byKey": {f"r{i}c1": t for i, t in enumerate(notes)}},
    "explain": {"text": "Five rows fell to differences, three to ratios and four to known lists or weaving. The slow ones show which test you reach for too late. Under 8 seconds each is test pace."},
})

# 12 transfer
screens.append({
    "type": "transfer", "difficulty": 3,
    "prose": "Tests set sequences because spotting a rule fast is daily work on a price path or an order book. A market maker's quoted size grows at each level away from the best price: 150, 250, 450, 850 shares.",
    "canvas": table_canvas(["Level", "Size"], [["1", "150"], ["2", "250"], ["3", "450"], ["4", "850"], ["5", "?"]], align=["right", "right"]),
    "question": "If the rule holds, what size is quoted at level 5?",
    "widget": num(1650, 0, label="Shares at level 5", accept="1,650: double and take 50.", wrong=[("same-gap", 1250, 0), ("doubled", 1700, 0)]),
    "hints": hints("The gaps are 100, 200, 400.", "The gaps double, so try a ratio with a fixed step.", "Double and take 50: $2 \\times 850 - 50 = 1650$.", ["r3"]),
    "feedback": {"correct": "Double and take 50: 1,650 shares.", "generic": "Not quite right. The gaps double; find the fixed step after doubling.",
                 "byKey": {"same-gap": "You added the last gap, 400, again. The gaps double, so the next gap is 800.", "doubled": "Doubling 850 misses the −50 that every step has: $2 \\times 150 = 300$, not 250."}},
    "explain": {"text": "The gaps 100, 200, 400 double, so the next is 800: $850 + 800 = 1650$. Equally, each size is double the last less 50. It is 3, 5, 9, 17, 33 again, at a larger scale.",
                "canvas": {"values": {"r4c1": "1,650"}}},
})

quiz = []
quiz.append({"id": "q-falling", "difficulty": 2, "prose": "A falling sequence.", "question": "What comes next: 41, 35, 29, 23, ?",
             "widget": num(17, 0, label="Next term", accept="17: take 6 each time.", wrong=[("sign", 29, 0)]),
             "feedback": {"correct": "−6 each time: 17.", "generic": "Not quite right. Find the gap, with its sign.",
                          "byKey": {"sign": "You added 6. The terms fall by 6, so $23 - 6 = 17$."}},
             "explain": {"text": "Each gap is −6, so the next term is $23 - 6 = 17$. Keep the sign of the gap."}})
quiz.append({"id": "q-cubes-plus-one", "difficulty": 3, "prose": "Look for a list you know, shifted.", "question": "What comes next: 2, 9, 28, 65, ?",
             "widget": num(126, 0, label="Next term", accept="126: $5^3 + 1$.", wrong=[("same-gap", 102, 0), ("cube", 125, 0)]),
             "feedback": {"correct": "Cubes plus 1: $5^3 + 1 = 126$.", "generic": "Not quite right. Compare each term with 1, 8, 27, 64.",
                          "byKey": {"same-gap": "You added the last gap, 37, again. The gaps grow, so use the cubes.", "cube": "125 is $5^3$. Every term here is one more than a cube."}},
             "explain": {"text": "2, 9, 28, 65 are $1 + 1$, $8 + 1$, $27 + 1$, $64 + 1$. So the next is $125 + 1 = 126$. A full difference table gives 126 too, three rows down."}})
quiz.append({"id": "q-woven", "difficulty": 3, "prose": "Two sequences woven together.", "question": "What comes next: 2, 5, 4, 10, 8, 20, ?",
             "widget": num(16, 0, label="Next term", accept="16: odd places double, 2, 4, 8.", wrong=[("even-row", 40, 0)]),
             "feedback": {"correct": "Odd places 2, 4, 8 double: 16.", "generic": "Not quite right. Split the odd and even places.",
                          "byKey": {"even-row": "40 continues the even places, 5, 10, 20. The 7th term is an odd place: 2, 4, 8, so 16."}},
             "explain": {"text": "Odd places read 2, 4, 8 and even places 5, 10, 20. The 7th place is odd, so the next term is 16."}})
quiz.append({"id": "q-fibonacci-like", "difficulty": 2, "prose": "Each term may depend on more than one before it.", "question": "What comes next: 3, 4, 7, 11, 18, ?",
             "widget": num(29, 0, label="Next term", accept="29: $11 + 18$.", wrong=[("same-gap", 25, 0), ("doubled", 36, 0)]),
             "feedback": {"correct": "Each term adds the two before: $11 + 18 = 29$.", "generic": "Not quite right. Add the last two terms.",
                          "byKey": {"same-gap": "You added 7, the last gap, again. Each term is the sum of the two before.", "doubled": "Doubling fails at once: $3 \\times 2$ is 6, not 4."}},
             "explain": {"text": "$3 + 4 = 7$, $4 + 7 = 11$ and $7 + 11 = 18$. So the next term is $11 + 18 = 29$, the Fibonacci rule from different starting terms."}})

lesson = {
    "id": "l10-next-in-sequence", "course": "mental-pressure", "title": "Next in the sequence", "minutes": 14,
    "objectives": ["Find a sequence’s rule under time pressure."], "skills": ["mp-formats"],
    "screens": screens,
    "summary": {"ideas": ["Try differences first: a constant row of first or second differences gives the next term by adding back up.",
                          "Then ratios (×2, ×3, perhaps with a fixed step), then known lists, then two sequences woven together.",
                          "Check the rule on every term shown; three terms fit many rules."],
                "formula": {"name": "Adding up the table", "tex": "a_{n+1} = a_n + \\Delta_n + \\Delta^2_n + \\cdots", "note": "2, 6, 12, 20, 30: $30 + 10 + 2 = 42$."},
                "trap": "Doubling 1, 2, 4 without checking the fourth term: 1, 2, 4, 7, 11 goes on to 16."},
    "quiz": quiz,
}
check_voice(lesson, 'l10')
write('l10-next-in-sequence.json', lesson)
