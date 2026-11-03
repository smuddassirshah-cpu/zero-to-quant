from common import *
from candidate import candidate_log, sort_type

PAPER = generate(80)
LOG = candidate_log()
KINDS = ["addsub", "mul", "div", "dec", "frac", "pct", "seq"]
LABEL = {"addsub": "+ −", "mul": "×", "div": "÷", "dec": "Dec", "frac": "Frac", "pct": "%", "seq": "Seq"}
NAME = {"addsub": "+ or −", "mul": "×", "div": "÷", "dec": "decimal", "frac": "fraction", "pct": "%", "seq": "sequence"}

# ---------- numbers, twice ----------
from collections import Counter
assert Counter(k for k, *_ in PAPER) == Counter(MIX) and len(PAPER) == 80
for k, text, opts, ans, L in PAPER:
    assert len(set(opts)) == 4 and opts["ABCD".index(L)] == ans and working(k, text, ans)
R = sum(r["mark"] == "right" for r in LOG); W = sum(r["mark"] == "wrong" for r in LOG); B = sum(r["mark"] == "blank" for r in LOG)
assert (R, W, B) == (57, 11, 12) and R - W == 46 and R + W + B == 80
blocks = [LOG[20 * b: 20 * b + 20] for b in range(4)]
bstats = [(sum(r["mark"] == "right" for r in x), sum(r["mark"] == "wrong" for r in x), sum(r["mark"] == "blank" for r in x), sum(r["secs"] or 0 for r in x)) for x in blocks]
assert [s[:3] for s in bstats] == [(16, 4, 0), (14, 6, 0), (19, 1, 0), (8, 0, 12)] and [s[0] - s[1] for s in bstats] == [12, 8, 18, 8] and 12 + 8 + 18 + 8 == 46
assert [s[3] for s in bstats] == [F(120), F(1651, 10), F(139), F(523, 10)] and sum(s[3] for s in bstats) == F(4764, 10)
b3 = [F(x).limit_denominator(10) for x in ("5.8 6.7 4.7 5.7 6.7 7.0 5.7 6.7 11.8 4.9 5.8 3.8 5.4 4.0 18.6 4.3 5.4 4.5 4.5 17.0".split())]
assert b3 == [r["secs"] for r in blocks[2]] and sum(b3) == 139 and 139 - 120 == 19 and F(186, 10) - 6 == F(126, 10) and F(158, 10) + F(186, 10) - 12 == F(224, 10)
# per-kind means of the reached questions
st = {k: [0, F(0), 0] for k in KINDS}
for r in LOG:
    if r["mark"] != "blank":
        st[r["kind"]][0] += 1; st[r["kind"]][1] += r["secs"]; st[r["kind"]][2] += r["mark"] == "wrong"
frac_secs = [F(x).limit_denominator(10) for x in "8.3 9.7 7.5 6.2 9.3 7.0 7.9 6.8 8.9".split()]
seq_secs = [F(x).limit_denominator(10) for x in "6.9 16.9 21.8 5.8 8.4 8.7 8.9".split()]
assert st["frac"][:2] == [9, sum(frac_secs)] and sum(frac_secs) == F(716, 10) and st["seq"][:2] == [7, sum(seq_secs)] and sum(seq_secs) == F(774, 10)
means = {k: round(float(st[k][1] / st[k][0]), 1) for k in KINDS}
wrongs = {k: st[k][2] for k in KINDS}
assert means == {"addsub": 6.1, "mul": 6.4, "div": 7.6, "dec": 5.9, "frac": 8.0, "pct": 5.5, "seq": 11.1} and wrongs == {"addsub": 1, "mul": 2, "div": 1, "dec": 1, "frac": 5, "pct": 0, "seq": 1}
# the sort, blocks 1 and 2
SORT = [r for r in LOG[:40] if sort_type(r)]
assert [(r["q"], sort_type(r)) for r in SORT] == [(8, "S"), (13, "M"), (14, "M"), (19, "M"), (21, "S"), (24, "M"), (26, "M"), (27, "M"), (30, "T"), (31, "T"), (34, "M"), (38, "M"), (40, "T")]
mt = Counter(r["kind"] for r in SORT if sort_type(r) in "MT")
assert mt == Counter({"frac": 5, "seq": 3, "mul": 2, "div": 1})
assert [r["q"] for r in blocks[2] if sort_type(r)] == [55, 60] and [r["q"] for r in blocks[2] if r["mark"] == "wrong"] == [60]
# quiz and generalise
assert F(126, 10) + 11 == F(236, 10) and F(236, 10) - 19 == F(46, 10) and F(126, 10) / 6 > 2
assert 66 - 9 - 9 == 48 and 74 - 14 - 14 == 46 and 660 / 80 == 8.25 and int(480 / 8.25) == 58
assert 115 + 130 + 150 - 360 == 35 and 150 - 120 == 30 and 115 + 130 + 150 + 100 - 480 == 15

screens = []
intros = [
    "The mock: 80 questions, four options each, in four blocks of 20 at 2 minutes a block. The app does not time this lesson, so start your own watch. On your first Check, count the amber rows: those are your wrong answers.",
    "Block 2: Q21 to Q40, due by 4:00. Take one breath first. Note your time and your amber count when you finish.",
    "Block 3: Q41 to Q60, due by 6:00. If you are behind, cut options and guess on slow kinds rather than rushing easy ones.",
    "Block 4: Q61 to Q80, due by 8:00. Note your final time. The screens after this one show how to review a marked set."]
for b in range(4):
    items = PAPER[20 * b: 20 * b + 20]
    tbl, bk = four_option_table(items, start=20 * b + 1)
    kinds = Counter(k for k, *_ in items)
    screens.append({
        "type": "problem" if b == 0 else "ladder", "difficulty": 2 if b < 2 else 3, "title": f"Block {b + 1} of 4", "tags": ["mock-eighty"],
        "prose": intros[b],
        "canvas": numline_block(b + 1),
        "question": f"Type the letter for Q{20 * b + 1} to Q{20 * b + 20}.",
        "widget": tbl,
        "hints": hints("Estimate first; then the last digit often picks between close options.", "Fractions: put both over one denominator before you look at the options.", block_line(items, 20 * b + 1) + ".", [f"i{b + 1}"]),
        "feedback": {"correct": f"All twenty right. Note your time for block {b + 1} against 2 minutes.", "generic": "Not quite right. Note how many rows are amber, then redo them.", "byKey": bk},
        "explain": {"text": f"This block held " + ", ".join(f"{v} {NAME[k]}" for k, v in sorted(kinds.items(), key=lambda kv: KINDS.index(kv[0]))) + " questions. Each took one move from the earlier lessons. Write your time and amber count on paper before you go on."},
    })

# 5 explore: the sample candidate, by kind
bars_params = {"categories": [{"id": k, "label": LABEL[k]} for k in KINDS], "yMax": 12, "showValues": True, "decimals": 1, "yLabel": "By kind"}
frames = [{"values": means, "caption": "Mean seconds a question, for the questions reached"},
          {"values": {k: float(v) for k, v in wrongs.items()}, "caption": "Wrong answers"}]
w = choice([opt("frac", "Fractions", correct=True),
            opt("seq", "Sequences", "Sequences were the slowest, 11.1 s each, but only one was wrong. Switch to the wrong answers."),
            opt("mul", "Multiplication", "Two multiplications were wrong, out of 14 reached. Fractions lost five."),
            opt("dec", "Decimals", "Only one decimal was wrong. Five decimals were never reached, which is a time problem, not a decimal one.")], layout="grid")
screens.append({
    "type": "explore", "difficulty": 2,
    "prose": "The app cannot pass your own marked set to the next screen. So we review a sample candidate who sat this paper (seed 81). Switch the chart between seconds and wrong answers.",
    "canvas": {"kind": "bars", "params": bars_params, "state": {"values": means, "caption": frames[0]["caption"]},
               "controls": [{"frames": frames, "frameLabels": ["Seconds", "Wrong"], "label": "Show", "start": 0}]},
    "question": "Which kind of question cost the candidate the most marks?",
    "widget": w,
    "hints": hints("Switch the chart to wrong answers.", "One bar stands well above the rest.", "Fractions: 5 wrong of the 9 reached.", ["frac"]),
    "feedback": {"correct": "Fractions: 5 wrong of the 9 reached.", "generic": "Not quite right. Look at the wrong answers, not the seconds.", "byKey": bykey_from_choice(w)},
    "explain": {"text": "Fractions lost five marks; no other kind lost more than two. Sequences were slowest, at 11.1 s each, but mostly right. Seconds and marks point at different weaknesses, so a review reads both.",
                "canvas": {"values": frames[1]["values"], "caption": frames[1]["caption"]}},
})

# 6 name: net score
rows = [[f"Block {b + 1}", f"{s[0]} right, {s[1]} wrong, {s[2]} blank", cell(s[0] - s[1], 0)] for b, s in enumerate(bstats)]
rows.append(["Total", f"{R} right, {W} wrong, {B} blank", cell(R - W, 0)])
screens.append({
    "type": "problem", "difficulty": 2,
    "prose": "The reported format scores +1 right, −1 wrong and 0 for a blank. The total is the **net score**. Net scoring is not built into the app, so we score the candidate by hand. The candidate ran out of time after Q68.",
    "canvas": table_canvas(["Mark", "Score"], [["Right", "+1"], ["Wrong", "−1"], ["Blank", "0"]], align=["left", "right"]),
    "question": "Fill in the net score for each block and for the paper.",
    "widget": {"kind": "table", "columns": ["Block", "Marks", "Net"], "rows": rows},
    "hints": hints("Net is right minus wrong; blanks add nothing.", "Block 1: $16 - 4 = 12$.", "12, 8, 18, 8, and 46 in all.", ["r1"]),
    "feedback": {"correct": "12, 8, 18 and 8: a net score of 46.", "generic": "Not quite right. Take the wrong count from the right count; blanks score 0.",
                 "byKey": {"r0c2": "$16 - 4 = 12$.", "r1c2": "$14 - 6 = 8$.", "r2c2": "$19 - 1 = 18$.", "r3c2": "$8 - 0 = 8$: the 12 blanks score nothing.",
                           "r4c2": "$57 - 11 = 46$. Check: $12 + 8 + 18 + 8 = 46$."}},
    "explain": {"text": "57 right less 11 wrong is 46 net, below the reported 50 to 60. Block 2 lost the most to errors and block 4 the most to time. Both point the review somewhere different.",
                "canvas": {"highlight": {"rows": [1]}}},
})

# 7 ladder: sort the errors
sort_rows = []
for r in SORT:
    t = sort_type(r)
    acc = {"S": ["slip"], "M": ["method", "method gap", "gap"], "T": ["time", "time loss"]}[t]
    sort_rows.append([f"Q{r['q']}: " + (r['text'] if r['kind'] == "seq" else r['text'].replace(" ", "\u00a0")), f"{float(r['secs']):.1f} s, {r['mark']}", cell(t, accept=acc, placeholder="S, M or T")])
why = {"S": "wrong in 6 s or less: a slip", "M": "wrong after more than 6 s: a method gap", "T": "right, but over 12 s: a time loss"}
screens.append({
    "type": "ladder", "difficulty": 3,
    "prose": "Sort every error into one of three kinds, using the seconds. A **slip** (S) is wrong in 6 s or less. A **method gap** (M) is wrong after longer. A **time loss** (T) is right, but over 12 s. Here are blocks 1 and 2.",
    "canvas": table_canvas(["Type", "Rule"], [["S, slip", "wrong, 6 s or less"], ["M, method gap", "wrong, over 6 s"], ["T, time loss", "right, over 12 s"]], align=["left", "left"]),
    "question": "Type S, M or T for each row.",
    "widget": {"kind": "table", "columns": ["Question", "Seconds, mark", "Type"], "rows": sort_rows},
    "hints": hints("Read the mark first, then the seconds.", "Q8 was wrong in 5.3 s: a slip. Q30 was right in 16.9 s: a time loss.",
                   "S, M, M, M, S, M, M, M, T, T, M, M, T.", ["r0", "r1"]),
    "feedback": {"correct": "Two slips, eight method gaps and three time losses.", "generic": "Not quite right. Wrong rows split at 6 s; right rows count only over 12 s.",
                 "byKey": {f"r{i}c2": f"Q{r['q']}, {float(r['secs']):.1f} s and {r['mark']}: {why[sort_type(r)]}." for i, r in enumerate(SORT)}},
    "explain": {"text": "Five of the eight method gaps are fractions. The time losses are two sequences and one product, each over 15 s. Slips call for care; method gaps and time losses call for a drill."},
})

# 8 follow-up: pick one drill
w = choice([opt("frac", "Fractions: one denominator, then the options", correct=True),
            opt("seq", "Sequences: they took the most seconds each", "Sequences hold three rows, two of them right answers. Fractions hold five, all lost marks."),
            opt("slips", "Slips: check every decimal point twice", "The two slips cost two marks. Care fixes slips; a drill is for a method gap."),
            opt("resit", "The same mock again tomorrow", "The same 80 questions tomorrow test your memory of them. Drill the weak kind; sit a mock weekly.")])
screens.append({
    "type": "ladder", "difficulty": 3, "title": "The follow-up",
    "prose": "The interviewer follows up: \"So what will you practise next week?\" Count the method gaps and time losses by kind. One drill, chosen from the review, beats five chosen by mood.",
    "canvas": table_canvas(["Kind", "M and T rows"], [["Fractions", "5"], ["Sequences", "3"], ["Multiplication", "2"], ["Division", "1"]], align=["left", "right"]),
    "question": "Which one drill should the candidate pick for next week?",
    "widget": w,
    "hints": hints("Slips do not need a drill.", "Look for the kind with the most M and T rows.", "Fractions, with five method gaps.", ["r0"]),
    "feedback": {"correct": "Fractions: five method gaps, every one a lost mark.", "generic": "Not quite right. Pick the kind with the most method gaps and time losses.", "byKey": bykey_from_choice(w)},
    "explain": {"text": "Fractions hold five of the eleven M and T rows, and each was a lost mark. A daily set of twenty fraction sums targets them. Sequences come second, for speed rather than accuracy."},
})

# 9 trap: only the wrong answers
b3rows = [[f"Q{r['q']}", f"{float(r['secs']):.1f} s", r["mark"]] for r in blocks[2]]
screens.append({
    "type": "trap", "difficulty": 3,
    "prose": "Block 3 looks the candidate's best: 19 right and 1 wrong. Yet it took 139 s, 19 s over its two minutes. A review must find where those seconds went.",
    "canvas": {"kind": "table", "params": {"columns": ["Question", "Seconds", "Mark"], "rows": b3rows, "align": ["left", "right", "left"], "tap": "rows"}, "state": {}},
    "question": "Tap every row in block 3 that the review must look at.",
    "widget": {"kind": "tap-regions", "answer": ["r14", "r19"], "countWord": "selected", "wrong": [{"id": "only-wrong", "set": ["r19"]}]},
    "hints": hints("Use the three types: slips, method gaps and time losses.", "Q60 is wrong after 17.0 s. Is any right answer over 12 s?", "Q55, right in 18.6 s, and Q60.", ["r14", "r19"]),
    "feedback": {"correct": "Q55, a time loss, and Q60, a method gap.", "generic": "Not quite right. Look for wrong answers and right answers over 12 s.",
                 "byKey": {"only-wrong": "You tapped only the wrong answer. Q55 was right but took 18.6 s, 12.6 s beyond pace. Slow right answers cost questions too.",
                           "r14": "Q55 was right, but 18.6 s is a time loss: tap it.", "r19": "Q60 was wrong after 17.0 s: a method gap.",
                           "r8": "Q49 took 11.8 s, slow but under the 12 s line. The routine starts at 12 s."}},
    "explain": {"text": "Q55 and Q60 took 23.6 s beyond pace between them, more than the whole 19 s overrun. Reviewing only the wrong answer would miss Q55. Slow right answers like Q55 are part of why block 4 ran out at Q68.",
                "canvas": {"highlight": {"rows": [14, 19]}}},
})

# 10 generalise
screens.append({
    "type": "generalise", "difficulty": 2,
    "prose": "The routine you just ran: score, sort, pick one drill. With $R$ right and $W$ wrong, $$\\text{net} = R - W,$$ and blanks score 0. Then sort the wrong answers and the slow right ones into slips, method gaps and time losses.",
    "question": "A sitting has 66 answered, 9 of them wrong. What is the net score?",
    "widget": num(48, 0, label="Net score", accept="48: 57 right less 9 wrong.", wrong=[("right-count", 57, 0), ("answered", 66, 0)]),
    "feedback": {"correct": "57 right less 9 wrong: 48.", "generic": "Not quite right. Find the right count first.",
                 "byKey": {"right-count": "57 is the number right. Each wrong answer also takes a mark: $57 - 9 = 48$.", "answered": "66 counts every answer as +1. The 9 wrong ones score −1."}},
    "explain": {"text": "66 answered with 9 wrong leaves 57 right. Net is $57 - 9 = 48$. Each wrong answer costs two marks against getting it right."},
})

# 11 derive
screens.append({
    "type": "derive", "difficulty": 3,
    "prose": "At the end of a sitting you know two counts quickly: $a$ answered and $r$ right. The wrong count is $a - r$. Write the net score in $a$ and $r$ alone.",
    "question": "Net score equals what?",
    "widget": {"kind": "expression", "answer": "2r - a", "accept": ["2r-a", "-a+2r", "2*r-a", "r-(a-r)"], "keyboard": "algebra",
               "wrong": [{"id": "flipped", "tex": "a - 2r"}, {"id": "no-penalty", "tex": "r"}, {"id": "wrong-count", "tex": "a - r"}]},
    "hints": hints("Net is right minus wrong.", "Wrong is $a - r$, so net is $r - (a - r)$.", "$r - a + r = 2r - a$."),
    "feedback": {"correct": "$r - (a - r) = 2r - a$.", "generic": "Not quite right. Replace the wrong count by $a - r$ in right minus wrong.",
                 "byKey": {"flipped": "That is the net with its sign flipped. Right answers add.", "no-penalty": "That ignores the −1 for each wrong answer.",
                           "wrong-count": "$a - r$ is the number wrong, not the net."}},
    "explain": {"text": "Net is $r - w$ and $w = a - r$, so net is $2r - a$. For the candidate: $2 \\times 57 - 68 = 46$. Each extra right answer moves the net by two."},
})

# 12 transfer
w = choice([opt("ok", "Five warm-up rounds a day towards 50, a daily fractions drill, and a mock in a week", correct=True),
            opt("daily", "The same mock every day until the net passes 55", "The same 80 questions every day teach the answers, not the speed. Sit a mock once a week."),
            opt("seq", "A daily sequences drill, since sequences took the most seconds", "Sequences were slow but mostly right. Fractions lost five marks: drill those."),
            opt("warmup", "The warm-up only: the mock was a one-off", "The warm-up drills four operations. Only a mock times the full mix, so repeat it weekly.")])
screens.append({
    "type": "transfer", "difficulty": 3,
    "prose": "The candidate scored 46 net, below the reported 50 to 60, with 12 blanks. Their best warm-up round this week was 41. The Today screen's daily warm-up marks the Stage 3 target at 50.",
    "canvas": table_canvas(["Measure", "This week", "Target"], [["Mock, net", "46", "50 to 60"], ["Warm-up, best round", "41", "50"], ["Fraction method gaps", "5", "0"]], align=["left", "right", "right"]),
    "question": "Which plan for next week follows from the review?",
    "widget": w,
    "hints": hints("Speed and fractions were the two weaknesses.", "The warm-up builds speed; the drill fixes fractions.", "Warm-up rounds, a fractions drill, and a mock again in a week.", ["r1"]),
    "feedback": {"correct": "Speed from the warm-up, fractions from the drill, progress from a weekly mock.", "generic": "Not quite right. Match one fix to each weakness the review found.", "byKey": bykey_from_choice(w)},
    "explain": {"text": "Open the daily warm-up from Today and note each score against the dashed Stage 3 mark of 50. Drill fractions daily, then sit a mock a week later and run the same review. Each review chooses the next week's drill."},
})

quiz = []
w = choice([opt("speed", "Speed: the same accuracy at 6 s a question", correct=True),
            opt("harder", "Harder papers: 80 of 80 means this one is too easy", "At 8.25 s a question, 8 minutes reaches only Q58. The paper is not the limit; the pace is."),
            opt("none", "Nothing: a perfect score passes", "At this pace the 8-minute clock stops at Q58, leaving 22 blank.")])
quiz.append({"id": "q-perfect-slow", "difficulty": 3, "prose": "On an untimed practice paper you score 80 out of 80, taking 11 minutes.",
             "question": "What is your next target?", "widget": w,
             "feedback": {"correct": "Speed: 11 minutes is 8.25 s a question, and the test allows 6.", "generic": "Not quite right. Work out the pace, then compare with 6 s.", "byKey": bykey_from_choice(w)},
             "explain": {"text": "660 s over 80 questions is 8.25 s each. In 480 s that pace reaches only 58 questions. A perfect slow score means the next target is time, not accuracy."}})
quiz.append({"id": "q-net-74", "difficulty": 2, "prose": "A sitting: 74 questions answered, 14 of them wrong, 6 blank.", "question": "What is the net score?",
             "widget": num(46, 0, label="Net score", accept="46: 60 right less 14 wrong.", wrong=[("right-count", 60, 0), ("answered", 74, 0)]),
             "feedback": {"correct": "60 right less 14 wrong: 46.", "generic": "Not quite right. Find the right count, then take off the wrong ones.",
                          "byKey": {"right-count": "60 is the number right. Take off 14 for the wrong answers.", "answered": "74 counts every answer as right."}},
             "explain": {"text": "74 answered with 14 wrong leaves 60 right. Net is $60 - 14 = 46$; the 6 blanks score nothing."}})
w = choice([opt("slip", "A slip", correct=True),
            opt("gap", "A method gap", "A method gap is wrong after more than 6 s. At 3.5 s you knew the way and slipped."),
            opt("time", "A time loss", "A time loss is a right answer over 12 s. This one was wrong and fast.")])
quiz.append({"id": "q-classify", "difficulty": 2, "prose": "In your review, $7.4 \\times 0.9$ was answered wrong in 3.5 s.", "question": "Which type of error is it?", "widget": w,
             "feedback": {"correct": "Wrong in 6 s or less: a slip.", "generic": "Not quite right. Use the mark and the seconds.", "byKey": bykey_from_choice(w)},
             "explain": {"text": "Wrong and fast means you knew the method and made a small error. Slips call for care, such as checking the decimal point, not a drill."}})
quiz.append({"id": "q-checkpoint-behind", "difficulty": 3, "prose": "Your four block times are 1:55, 2:10, 2:30 and 1:40.",
             "question": "How many seconds behind were you at the 6-minute checkpoint?",
             "widget": num(35, 0, unit="seconds", label="Behind", accept="35 s: 395 s against 360 s.", wrong=[("block-only", 30, 0), ("final", 15, 0)]),
             "feedback": {"correct": "$115 + 130 + 150 = 395$ s, against 360: 35 s behind.", "generic": "Not quite right. Add the first three blocks, then compare with 360 s.",
                          "byKey": {"block-only": "30 s is block 3's own overrun. Block 2 was already 10 s late and block 1 5 s early.", "final": "15 s is the overrun at the end. The question asks about 6 minutes."}},
             "explain": {"text": "The first three blocks took 395 s, so you reached Q60 35 s late. A fast block 4 brought the end back to 15 s over. Checkpoints show where time was lost, not only how much."}})

lesson = {
    "id": "l12-mock-test", "course": "mental-pressure", "title": "A full mock test", "minutes": 15,
    "objectives": ["Sit a full timed test and review every error."], "skills": ["mp-formats", "mp-speed"],
    "screens": screens,
    "summary": {"ideas": ["Sit the 80 in four blocks of 20, checking 2, 4 and 6 minutes, with a breath between blocks.",
                          "Score it net, +1 right and −1 wrong, then sort errors into slips, method gaps and time losses.",
                          "Pick one drill from the method gaps and time losses, and sit a mock again a week later."],
                "formula": {"name": "Net score", "tex": "\\text{net} = R - W = 2R - A", "note": "57 right of 68 answered: $114 - 68 = 46$."},
                "trap": "Reviewing only the wrong answers: Q55 was right but took 18.6 s, two questions' worth of time."},
    "quiz": quiz,
}
check_voice(lesson, 'l12')
write('l12-mock-test.json', lesson)
