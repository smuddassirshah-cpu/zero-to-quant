from common import *
from decimal import Decimal as D
import inspect
import mockgen
from l10 import nbd, fib_next
from l11 import mins, clock

# ================= review-3 =================
assert F(600, 50) == 12 and 12 * 30 == 360 and 360 / 60 == 6
assert sorted([6, 12, 5, 20, 7, 4, 9])[:6] == [4, 5, 6, 7, 9, 12] and 4 + 5 + 6 + 7 + 9 + 12 == 43 and 43 + 20 > 45 and 4 + 5 + 6 + 7 + 9 == 31
assert nbd([3, 6, 11, 18, 27]) == 38 == 6 * 6 + 2 and 27 + 9 == 36
t = [4]
for _ in range(5):
    t.append(2 * t[-1] - 1)
assert t == [4, 7, 13, 25, 49, 97] and 49 + 24 == 73
assert [3, 100, 6, 90, 12, 80][::2] == [3, 6, 12] and 12 * 2 == 24
assert D(4800) * D('0.35') == 1680 and D(4800) * D('0.65') == 3120 and D(4800) * D('2.15') == 10320
assert clock(mins('22:35') + 230) == '02:25' and 35 + 50 == 85 and clock(mins('22:35') + 180) == '01:35'
assert D(3600) * D('0.05') * 4 / 12 == 60 and D(3600) * D('0.05') == 180 and D(3600) * D('0.05') * 4 == 720
assert 71 - 13 == 58 and 58 - 13 == 45

R = []
R.append({"id": "r-checkpoint-fifty", "difficulty": 2, "skills": ["mp-formats", "mp-speed"], "tags": ["checkpoints"],
          "prose": "A test has 50 questions in 10 minutes.", "question": "When is question 30 due, in minutes?",
          "widget": num(6, 0.001, unit="minutes", label="Due at", accept="6 minutes: 12 s a question.", wrong=[("count-rate", 3, 0.001), ("seconds", 360, 0.01)]),
          "feedback": {"correct": "12 s a question: Q30 at 360 s, 6 minutes.", "generic": "Not quite right. Find the pace, then multiply by 30.",
                       "byKey": {"count-rate": "You divided 30 by 10. The pace is 5 questions a minute, so Q30 is at 6 minutes.", "seconds": "360 is in seconds. In minutes it is 6."}},
          "explain": {"text": "600 s over 50 questions is 12 s each. Question 30 is due at $30 \\times 12 = 360$ s, which is 6 minutes. Equally, 5 a minute reaches 30 at minute 6."}})
R.append({"id": "r-squares-plus-two", "difficulty": 2, "skills": ["mp-formats"], "tags": ["sequence-differences"],
          "prose": "About 8 seconds.", "question": "What comes next: 3, 6, 11, 18, 27, ?",
          "widget": num(38, 0, label="Next term", accept="38: gaps 3, 5, 7, 9, then 11.", wrong=[("same-gap", 36, 0)]),
          "feedback": {"correct": "Gaps 3, 5, 7, 9 grow by 2: next 11, so 38.", "generic": "Not quite right. Write the gaps, then their changes.",
                       "byKey": {"same-gap": "You added 9, the last gap, again. The gaps grow by 2, so the next is 11."}},
          "explain": {"text": "The gaps 3, 5, 7, 9 grow by 2, so the next gap is 11 and the term is 38. These are the squares plus 2: $6^2 + 2 = 38$."}})
R.append({"id": "r-left-to-fill", "difficulty": 3, "skills": ["mp-formats"], "tags": ["word-filled"],
          "prose": "An order to buy 4,800 shares at £2.15 is 65% filled.", "question": "How many shares are still to fill?",
          "widget": num(1680, 0, label="Shares left", accept="1,680: the 35% not yet filled.", wrong=[("filled", 3120, 0), ("price", 10320, 0)]),
          "feedback": {"correct": "35% of 4,800 is still open: 1,680 shares.", "generic": "Not quite right. 65% is done, so 35% is left.",
                       "byKey": {"filled": "3,120 is the 65% already filled. The question asks what is left.", "price": "£10,320 is the order's value. The price is not in this line."}},
          "explain": {"text": "65% filled leaves 35% open. 10% of 4,800 is 480, so 35% is $3.5 \\times 480 = 1680$. The £2.15 is in the words but not the line."}})
R.append({"id": "r-net-seventy-one", "difficulty": 2, "skills": ["mp-formats", "mp-speed"], "tags": ["net-score"],
          "prose": "A forward-only sitting scored +1 right and −1 wrong. You answered 71 questions, 13 of them wrong.", "question": "What is your net score?",
          "widget": num(45, 0, label="Net score", accept="45: 58 right less 13 wrong.", wrong=[("right-count", 58, 0), ("answered", 71, 0)]),
          "feedback": {"correct": "58 right less 13 wrong: 45.", "generic": "Not quite right. Find the right count, then take off the wrong ones.",
                       "byKey": {"right-count": "58 is the number right. Each wrong answer takes off a mark: $58 - 13 = 45$.", "answered": "71 counts every answer as right."}},
          "explain": {"text": "71 answered with 13 wrong leaves 58 right. Net is $58 - 13 = 45$, or $2 \\times 58 - 71 = 45$. That is below the reported 50 to 60."}})
R.append({"id": "r-skip-forty-five", "difficulty": 3, "skills": ["mp-formats", "mp-speed"], "tags": ["skip-budget"],
          "prose": "A test that allows skipping. 45 s are left, and the last questions would take you 6, 12, 5, 20, 7, 4 and 9 s.", "question": "What is the most you can answer?",
          "widget": num(6, 0, label="Questions", accept="6: 4 + 5 + 6 + 7 + 9 + 12 = 43 s.", wrong=[("drop-12", 5, 0), ("all", 7, 0)]),
          "feedback": {"correct": "Skip the 20 s one: the other six take 43 s.", "generic": "Not quite right. Keep the cheapest until the next would pass 45 s.",
                       "byKey": {"drop-12": "You skipped the 12 s one too. With it the six take 43 s, inside 45.", "all": "All seven take 63 s, over the 45 s left."}},
          "explain": {"text": "Sorted: 4, 5, 6, 7, 9, 12, 20. The first six take 43 s, and the 20 s one would make 63. So six, with 2 s to spare."}})
R.append({"id": "r-double-less-one", "difficulty": 3, "skills": ["mp-formats"], "tags": ["sequence-ratio"],
          "prose": "About 8 seconds.", "question": "What comes next: 4, 7, 13, 25, 49, ?",
          "widget": num(97, 0, label="Next term", accept="97: double and take 1.", wrong=[("same-gap", 73, 0), ("doubled", 98, 0)]),
          "feedback": {"correct": "Double and take 1: $2 \\times 49 - 1 = 97$.", "generic": "Not quite right. The gaps double; look for a fixed step after doubling.",
                       "byKey": {"same-gap": "You added the last gap, 24, again. The gaps double, so the next is 48.", "doubled": "Doubling misses the −1 in every step: $2 \\times 4 = 8$, not 7."}},
          "explain": {"text": "Each term is double the last, less 1. The gaps 3, 6, 12, 24 double too, so the next gap is 48. Both give $49 + 48 = 97$."}})
R.append({"id": "r-interest-four-months", "difficulty": 3, "skills": ["mp-formats"], "tags": ["word-interest"],
          "prose": "£3,600 is deposited at 5% a year, simple interest.", "question": "What interest is due after 4 months, in pounds?",
          "widget": num(60, 0.001, unit="£", label="Interest", accept="£60: a third of £180.", wrong=[("year", 180, 0.001), ("months-as-years", 720, 0.01)]),
          "feedback": {"correct": "£180 a year; 4 months is a third: £60.", "generic": "Not quite right. Find a year's interest, then take $\\tfrac{4}{12}$ of it.",
                       "byKey": {"year": "£180 is a full year. Four months is a third of that.", "months-as-years": "You multiplied by 4 as if it were years. Divide the months by 12."}},
          "explain": {"text": "A year's interest is $3600 \\times 0.05 = 180$. Four months is $\\tfrac{4}{12} = \\tfrac13$ of a year, so £60. In one line: $\\tfrac{3600 \\times 5 \\times 4}{1200} = 60$."}})
w = choice([opt("q31", "Q31: wrong, after 9 s", correct=True),
            opt("q12", "Q12: wrong, after 4 s", "Wrong in 6 s or less is a slip: you knew the way and erred. Care fixes it."),
            opt("q47", "Q47: right, after 15 s", "Right but over 12 s is a time loss, not a method gap.")])
R.append({"id": "r-which-gap", "difficulty": 3, "skills": ["mp-formats"], "tags": ["error-sort"],
          "prose": "A review lists three questions from your mock.", "question": "Which one is a method gap?", "widget": w,
          "feedback": {"correct": "Wrong after more than 6 s: a method gap.", "generic": "Not quite right. A method gap is wrong and slow.", "byKey": bykey_from_choice(w)},
          "explain": {"text": "Q31 took 9 s and was still wrong, so the method was missing. Q12 was a fast slip and Q47 a slow right answer. Only the method gap needs a drill of its own."}})
R.append({"id": "r-woven-halves", "difficulty": 3, "skills": ["mp-formats"], "tags": ["sequence-woven"],
          "prose": "About 8 seconds.", "question": "What comes next: 3, 100, 6, 90, 12, 80, ?",
          "widget": num(24, 0, label="Next term", accept="24: odd places double.", wrong=[("even-row", 70, 0)]),
          "feedback": {"correct": "Odd places 3, 6, 12 double: 24.", "generic": "Not quite right. Split the odd and even places.",
                       "byKey": {"even-row": "70 continues the even places, 100, 90, 80. The 7th place is odd: 3, 6, 12, so 24."}},
          "explain": {"text": "Odd places read 3, 6, 12 and even places 100, 90, 80. The 7th term is in the odd places, so it is 24."}})
w = choice([opt("ok", "02:25", correct=True),
            opt("carry", "01:25", "You turned 85 minutes into 25 and dropped the hour. 01:35 plus 50 minutes passes 02:00."),
            opt("wrap", "26:25", "The clock passes midnight: 26:25 is 02:25 on the next day."),
            opt("raw", "01:85", "85 minutes is 1 h 25. Carry the hour: 02:25.")], layout="grid")
R.append({"id": "r-past-midnight", "difficulty": 4, "skills": ["mp-formats"], "tags": ["word-time"],
          "prose": "A flight leaves at 22:35 and takes 3 h 50 min.", "question": "When does it land?", "widget": w,
          "feedback": {"correct": "22:35 plus 3 hours is 01:35; plus 50 minutes is 02:25.", "generic": "Not quite right. Add the hours, then the minutes, and carry past 60 and past midnight.", "byKey": bykey_from_choice(w)},
          "explain": {"text": "Three hours take 22:35 to 01:35, past midnight. Then $35 + 50 = 85$ minutes, which is 1 h 25. So the flight lands at 02:25."}})

review = {"id": "review-3", "course": "mental-pressure", "level": 3, "timed": {"seconds": 300, "lockAtZero": False}, "items": R}
check_voice(review, 'review-3')
write('review-3.json', review)

# ================= homework-3 =================
H = []
# 1 drill: twenty four-option questions, seed 31
B31 = generate(31, BLOCK)
tbl, bk = four_option_table(B31)
H.append({"id": "h-drill-eighty-block", "difficulty": 3, "skills": ["mp-speed", "mp-formats"], "tags": ["drill-eighty-block"], "title": "Twenty in two minutes",
          "prose": "A fresh block of 20 in the 80-in-8 mix, four options each. Target: 2 minutes, 6 s a question. Time yourself with your own watch; the page has no clock. Count your amber rows on the first Check.",
          "question": "Type the letter of each answer.", "widget": tbl,
          "feedback": {"correct": "All twenty right. Compare your time and amber count with your block from the lesson.", "generic": "Not quite right. Note the amber rows by kind, then redo them.", "byKey": bk},
          "explain": {"text": "Each row needed one move from the course. Compare your time with the lesson block. If one kind was amber twice, it is your drill this week."}})

# 2 drill: ten sequences and ten word problems
SEQ = [([7, 12, 17, 22], 27), ([81, 27, 9, 3], 1), ([1, 4, 10, 19, 31], 46), ([2, 6, 18, 54], 162), ([1, 3, 4, 7, 11], 18),
       ([0, 3, 8, 15, 24], 35), ([6, 11, 21, 41], 81), ([1, 20, 3, 40, 5, 60], 7), ([125, 64, 27, 8], 1), ([100, 93, 86, 79], 72)]
assert nbd(SEQ[0][0]) == 27 and 3 // 3 == 1 and nbd(SEQ[2][0]) == 46 and 54 * 3 == 162 and fib_next(SEQ[4][0]) == 18 and nbd(SEQ[5][0]) == 35
assert all(b == 2 * a - 1 for a, b in zip([6, 11, 21, 41], [11, 21, 41, 81])) and SEQ[7][0][::2] == [1, 3, 5] and [5 ** 3, 4 ** 3, 3 ** 3, 2 ** 3, 1] == [125, 64, 27, 8, 1] and nbd(SEQ[9][0]) == 72
WORD = [("Buy 500 at £2.36, sell at £2.50: profit (£)", 500 * (D('2.50') - D('2.36')), "£"),
        ("An order of 6,000 shares is 15% filled: shares filled", D(6000) * D('0.15'), ""),
        ("Leave 13:52; the journey takes 3 h 24 min: arrive at", clock(mins('13:52') + 204), "t"),
        ("£2,000 at 6% simple interest for 3 months: interest (£)", D(2000) * D('0.06') * 3 / 12, "£"),
        ("Items at £0.99, £2.49 and £6.99: total (£)", D('0.99') + D('2.49') + D('6.99'), "£"),
        ("4,000 shares at 35p each: cost (£)", D(4000) * D('0.35'), "£"),
        ("A share falls 20%, then rises 20%: net change (%)", D('0.8') * D('1.2') - 1, "%"),
        ("Bought 250 at £9.20, sold at £9.80: P&L (£)", 250 * (D('9.80') - D('9.20')), "£"),
        ("From 08:45 to 10:20: minutes", D(mins('10:20') - mins('08:45')), ""),
        ("£1,200 including 20% VAT: price before VAT (£)", D(1200) / D('1.2'), "£")]
assert [v if isinstance(v, str) else float(v) for _, v, _ in WORD] == [70, 900, '17:16', 30, 10.47, 1400, -0.04, 150, 95, 1000]
assert 1 + D('2.5') + 7 - D('0.03') == D('10.47') and 52 + 24 == 76 and 15 + 80 == 95 and 3 * 60 + 24 == 204
rows, notes = [], []
for s, a in SEQ:
    rows.append([", ".join(map(str, s)) + ", ?", cell(a, 0)])
for q, v, u in WORD:
    if u == "t":
        rows.append([q, cell(v, accept=[v.replace(':', '.'), v.replace(':', '')], placeholder="HH:MM")])
    elif u == "%":
        rows.append([q, cell(float(v), 0.0005, unit="%")])
    else:
        rows.append([q, cell(float(v), 0.001)])
notes = ["+5 each time: 27.", "Divide by 3 each time: 1.", "Gaps 3, 6, 9, 12: next 15, so 46.", "×3 each time: 162.", "Each term adds the two before: $7 + 11 = 18$.",
         "Gaps 3, 5, 7, 9: next 11, so 35. These are the squares less 1.", "Double and take 1: 81.", "Woven: odd places 1, 3, 5, so 7.", "Cubes falling: $1^3 = 1$.", "−7 each time: 72.",
         "$500 \\times 0.14 = 70$.", "10% is 600 and 5% is 300: 900.", "13:52 plus 3 h is 16:52; $52 + 24 = 76$ minutes, 1 h 16: 17:16.", "£120 a year; a quarter is £30.",
         "£1 + £2.50 + £7 = £10.50, less 3p: £10.47.", "$4000 \\times 0.35 = 1400$: £1,400.", "$0.8 \\times 1.2 = 0.96$: −4%.", "$250 \\times 0.60 = 150$.",
         "15 minutes to 09:00, then 80 more: 95.", "$1200 \\div 1.2 = 1000$, not £960."]
H.append({"id": "h-drill-sequences-words", "difficulty": 4, "skills": ["mp-formats"], "tags": ["drill-sequences", "drill-word-problems"], "title": "Ten sequences, ten word problems",
          "prose": "Ten sequences at 8 seconds each, then ten word problems at 10 seconds each: 3 minutes in all. Time yourself with your own watch. Times as HH:MM; a loss or a fall with a minus sign.",
          "question": "Fill in all twenty.", "widget": {"kind": "table", "columns": ["Question", "Answer"], "rows": rows},
          "feedback": {"correct": "All twenty right. Compare your time with the 3-minute target.", "generic": "Not quite right. Redo the amber rows: differences first, or the one line first.",
                       "byKey": {f"r{i}c1": t for i, t in enumerate(notes)}},
          "explain": {"text": "The sequences fell to differences, ratios, lists or weaving, in that order of speed. The word problems were one line each, with unit changes in rows 13, 16 and 19. Time the slower half again tomorrow."}})

# 3 code, difficulty 5: the mock generator
src = "".join(inspect.getsource(f) + "\n\n" for f in (mockgen.terminating, mockgen.near, mockgen.slips, mockgen.num_text, mockgen.make, mockgen.generate, mockgen.plain, mockgen.mock_generator))
solution = ("import random\nfrom fractions import Fraction as F\nfrom math import gcd\n\n"
            "MIX = {\"addsub\": 15, \"mul\": 15, \"div\": 10, \"dec\": 12, \"frac\": 10, \"pct\": 10, \"seq\": 8}\n\n\n" + src).rstrip() + "\n"
solution = solution.replace('    mix = MIX if mix is None else mix\n', '    mix = MIX if mix is None else mix\n')
prelude = open('/tmp/claude-0/-home-user-zero-to-quant/f2cb57c1-0333-5a7c-8b45-5ff551a039e9/scratchpad/mental-pressure-3/prelude_hw.py').read()
starter = ("import random\nfrom fractions import Fraction\n\n"
           "MIX = {\"addsub\": 15, \"mul\": 15, \"div\": 10, \"dec\": 12, \"frac\": 10, \"pct\": 10, \"seq\": 8}\n\n\n"
           "def mock_generator(seed, mix=None):\n    mix = MIX if mix is None else mix\n    rng = random.Random(seed)\n    items = []\n"
           "    for kind, count in mix.items():\n        for _ in range(count):\n            ...  # one (text, options, answer) of this kind\n    return items\n")
tests = [{"call": "len(mock_generator(80))", "expect": "80", "compare": "equal"},
         {"call": "_counts(mock_generator(80)) == _MIX", "expect": "True", "compare": "equal"},
         {"call": "_counts(mock_generator(7, {'seq': 3, 'pct': 2, 'frac': 4})) == {'seq': 3, 'pct': 2, 'frac': 4}", "expect": "True", "compare": "equal"},
         {"call": "_shape_ok(mock_generator(80))", "expect": "True", "compare": "equal"},
         {"call": "_answers_ok(mock_generator(80))", "expect": "True", "compare": "equal"},
         {"call": "_answers_ok(mock_generator(2026))", "expect": "True", "compare": "equal"},
         {"call": "_answers_ok(mock_generator(11, {'div': 12, 'dec': 12}))", "expect": "True", "compare": "equal"},
         {"call": "_answer_once(mock_generator(80))", "expect": "True", "compare": "equal"},
         {"call": "_answer_once(mock_generator(404))", "expect": "True", "compare": "equal"},
         {"call": "_near_ok(mock_generator(80))", "expect": "True", "compare": "equal"},
         {"call": "_whole_div(mock_generator(80))", "expect": "True", "compare": "equal"},
         {"call": "_same(mock_generator(5), mock_generator(5))", "expect": "True", "compare": "equal"},
         {"call": "_differ(mock_generator(5), mock_generator(6))", "expect": "True", "compare": "equal"},
         {"call": "_counts(mock_generator(3, {'addsub': 1})) == {'addsub': 1}", "expect": "True", "compare": "equal"}]
H.append({"id": "h-mock-generator", "difficulty": 5, "skills": ["mp-formats", "mp-speed"], "tags": ["code-mock-generator"], "title": "Generate your own mock",
          "prose": ("`mock_generator(seed, mix)` returns a list of `(text, options, answer)` tuples, `mix[kind]` of each kind, from `random.Random(seed)`. "
                    "Options are four different positive numbers, the answer among them once, each wrong one within a factor of ten of it. Text formats:\n\n"
                    "| Kind | Text |\n|---|---|\n| `addsub` | `291 + 883`, `508 − 96` |\n| `mul`, `div` | `41 × 63`, `342 ÷ 6` (a whole answer) |\n"
                    "| `dec` | `8.3 × 8`, `34.8 ÷ 1.2` |\n| `frac` | `2/3 − 1/2` (answers as `Fraction`) |\n| `pct` | `15% of 1,260` |\n| `seq` | `66, 57, 48, 39, ?` |\n\n"
                    "Sequences need fixed gaps, fixed second gaps, or each term $r$ times the last plus $c$."),
          "question": "Write `mock_generator(seed, mix)`.",
          "widget": {"kind": "code", "language": "python", "prelude": prelude, "starter": starter, "solution": solution,
                     "examples": [{"call": "len(mock_generator(80))", "expect": "80", "compare": "equal"}, {"call": "_counts(mock_generator(80)) == _MIX", "expect": "True", "compare": "equal"}],
                     "tests": tests,
                     "how": "Check runs 14 hidden tests. A hidden reader parses each text and recomputes the answer with fractions, counts the kinds against the mix, checks four distinct options with the answer once and every option within ten times the answer, whole division answers, and that one seed gives one paper and another seed another."},
          "feedback": {"correct": "Your generator makes papers whose answers recompute, whose kinds match the mix, and whose wrong options are near misses.",
                       "generic": "Not quite right. Read which hidden test failed: the kind counts, a recomputed answer, the options, or the seed."},
          "explain": {"text": "Every random choice comes from one `random.Random(seed)`, so a seed fixes a paper and exam authors can rebuild it. Working in `Fraction` keeps 0.1 + 0.2 from ever deciding an answer. Near misses come from the slips this level named: a carry, a moved point, the reverse operation."}})

# 4 code, difficulty 4: next term with ratios
nt_solution = ("from fractions import Fraction\n\n\n"
               "def next_term(seq):\n    t = [Fraction(x) for x in seq]\n    rows = [t]\n"
               "    while len(rows[-1]) > 1 and len(set(rows[-1])) > 1:\n        r = rows[-1]\n        rows.append([b - a for a, b in zip(r, r[1:])])\n"
               "    if len(rows[-1]) >= 2:\n        return tidy(sum(r[-1] for r in rows))\n"
               "    if len(t) >= 3 and 0 not in t[:-1]:\n        ratios = {b / a for a, b in zip(t, t[1:])}\n        if len(ratios) == 1:\n            return tidy(t[-1] * ratios.pop())\n"
               "    if len(t) >= 4 and t[1] != t[0]:\n        k = (t[2] - t[1]) / (t[1] - t[0])\n        c = t[1] - k * t[0]\n"
               "        if all(b == k * a + c for a, b in zip(t, t[1:])):\n            return tidy(k * t[-1] + c)\n    return None\n\n\n"
               "def tidy(x):\n    return int(x) if x.denominator == 1 else x\n")
from fractions import Fraction
ns = {}
exec(nt_solution, ns)
nt = ns["next_term"]
assert nt([3, 7, 11, 15]) == 19 and nt([2, 6, 12, 20, 30]) == 42 and nt([3, 6, 12, 24]) == 48 and nt([5, 15, 45, 135]) == 405 and nt([64, 32, 16, 8]) == 4
assert nt([4, 6, 9]) == 13.5 and nt([9, 6, 4]) == Fraction(8, 3) and nt([3, 5, 9, 17, 33]) == 65 and nt([150, 250, 450, 850]) == 1650 and nt([7, 7, 7]) == 7
assert nt([1, 1, 2, 3, 5, 8]) is None and nt([2, 3, 5, 7, 11]) is None and nt([1, 2]) is None and nt([0, 0, 0]) == 0
assert 4 * F(2, 3) == F(8, 3) and 9 * F(3, 2) == F(27, 2) and 2 * 33 - 1 == 65
H.append({"id": "h-next-term", "difficulty": 4, "skills": ["mp-formats"], "tags": ["code-next-term"], "title": "Differences, then ratios",
          "prose": "Extend `next_by_differences` from the lesson. `next_term(seq)` tries differences first; then a constant ratio; then a ratio with a fixed step, each term $k$ times the last plus $c$. It returns `None` if none fits. Work in `fractions.Fraction`, so 9, 6, 4 gives exactly $\\tfrac83$.",
          "question": "Write `next_term(seq)`.",
          "widget": {"kind": "code", "language": "python", "starter": "from fractions import Fraction\n\n\ndef next_term(seq):\n    t = [Fraction(x) for x in seq]\n    answer = Fraction(0)\n    # differences, then a ratio, then a ratio with a fixed step\n    ...\n    return answer\n",
                     "solution": nt_solution,
                     "examples": [{"call": "next_term([3, 5, 9, 17, 33])", "expect": "65", "compare": "equal"}],
                     "tests": [{"call": "next_term([3, 7, 11, 15])", "expect": "19", "compare": "equal"},
                               {"call": "next_term([2, 6, 12, 20, 30])", "expect": "42", "compare": "equal"},
                               {"call": "next_term([7, 7, 7])", "expect": "7", "compare": "equal"},
                               {"call": "next_term([3, 6, 12, 24])", "expect": "48", "compare": "equal"},
                               {"call": "next_term([5, 15, 45, 135])", "expect": "405", "compare": "equal"},
                               {"call": "next_term([64, 32, 16, 8])", "expect": "4", "compare": "equal"},
                               {"call": "next_term([4, 6, 9])", "expect": "13.5", "compare": "equal"},
                               {"setup": "from fractions import Fraction", "call": "next_term([9, 6, 4]) == Fraction(8, 3)", "expect": "True", "compare": "equal"},
                               {"call": "next_term([3, 5, 9, 17, 33])", "expect": "65", "compare": "equal"},
                               {"call": "next_term([150, 250, 450, 850])", "expect": "1650", "compare": "equal"},
                               {"call": "next_term([1, 1, 2, 3, 5, 8]) is None", "expect": "True", "compare": "equal"},
                               {"call": "next_term([2, 3, 5, 7, 11]) is None", "expect": "True", "compare": "equal"},
                               {"call": "next_term([1, 2]) is None", "expect": "True", "compare": "equal"}],
                     "how": "Check runs 13 hidden tests, compared exactly: three by differences, four ratios (one of them $\\tfrac83$ as a Fraction), two ratios with a step, and three that fit nothing and return None."},
          "feedback": {"correct": "Differences, then ratios, then a ratio with a step, all exact.", "generic": "Not quite right. Keep the lesson's order, and use Fraction so no float rounds a ratio."},
          "explain": {"text": "Differences settle for fixed gaps and growing gaps; a doubling sequence never settles, so ratios come next. 3, 5, 9, 17, 33 needs the step: $k = 2$, $c = -1$. Fibonacci fits none of the three, which is why the lesson keeps known lists as a separate test."}})

# 5 order: the review routine
H.append({"id": "h-review-routine", "difficulty": 4, "skills": ["mp-formats"], "tags": ["review-routine"], "title": "The review, in order",
          "prose": "You have just sat a mock of 80 in 8. Put the review routine in order. Two lines are habits that waste the review: leave them out.",
          "question": "Put the lines in order.",
          "widget": {"kind": "order", "lines": [
              {"id": "o1", "text": "Score it net, +1 right and −1 wrong, so you know where you stand against the pass line"},
              {"id": "o2", "text": "Mark each block's time against 2, 4, 6 and 8 minutes, to see where the time went"},
              {"id": "o3", "text": "List every wrong answer and every right answer over 12 s, with its seconds"},
              {"id": "o4", "text": "Sort each into a slip, a method gap or a time loss, by its mark and seconds"},
              {"id": "o5", "text": "Count the method gaps and time losses by kind, because slips need care rather than a drill"},
              {"id": "o6", "text": "Pick one drill for the kind with the most, and book the next mock for a week later"},
              {"id": "d1", "text": "Redo only the wrong answers until each one is right", "why": "That skips the slow right answers, which cost questions too, and it rehearses these answers rather than the method."},
              {"id": "d2", "text": "Drill every kind a little each day", "why": "Spread over seven kinds, no weak kind improves. One drill, chosen by the count, does."}],
              "answer": ["o1", "o2", "o3", "o4", "o5", "o6"], "same": [["o1", "o2"]], "distractors": ["d1", "d2"]},
          "feedback": {"correct": "Score, time, list, sort, count, then one drill and a date for the next mock.", "generic": "Not quite right. Measure first, then sort, then choose.",
                       "byKey": {"d1": "That skips the slow right answers, which cost questions too, and it rehearses these answers rather than the method.",
                                 "d2": "Spread over seven kinds, no weak kind improves. One drill, chosen by the count, does.",
                                 "left-out": "Every line except the two habits belongs.",
                                 "o3": "List the errors once the score and the times are down.", "o4": "Sort only after the list is made.",
                                 "o5": "Count by kind after sorting.", "o6": "Choosing the drill comes last, from the count."}},
          "explain": {"text": "The score and the block times say how far off you are and where. The list and the sort say why. The count chooses one drill, and the next mock checks whether it worked."}})

# 6 numeric: guessing the last five
assert 5 * (F(1, 3) - F(2, 3)) == F(-5, 3) and round(-5 / 3, 3) == -1.667 and 5 * F(-1, 2) == F(-5, 2)
H.append({"id": "h-last-five-guesses", "difficulty": 4, "skills": ["mp-formats"], "tags": ["guess-value"],
          "prose": "A forward-only test, four options, +1 right and −1 wrong; a question you never reach scores 0. With 30 s left, five questions remain. You can remove one wrong option from each, then guess.",
          "question": "What is the expected net score from guessing all five?",
          "widget": num(-1.6667, 0.005, placeholder="fraction or decimal", label="Expected net", accept="$-\\tfrac53$, about −1.67.", wrong=[("blind", -2.5, 0.005), ("two-removed", 0, 0.005), ("one-guess", -0.3333, 0.005)]),
          "feedback": {"correct": "$5 \\times (\\tfrac13 - \\tfrac23) = -\\tfrac53$.", "generic": "Not quite right. Find one guess's value among three, then times five.",
                       "byKey": {"blind": "−2.5 is five blind guesses among four. You removed one option, so each is among three.",
                                 "two-removed": "0 needs two options removed from each. With one removed, each guess costs a third.",
                                 "one-guess": "That is one guess. There are five."}},
          "explain": {"text": "Each guess among three is worth $\\tfrac13 - \\tfrac23 = -\\tfrac13$, so five are worth $-\\tfrac53$. Leaving them unreached scores 0, so here guessing costs marks. Remove a second option, and each guess becomes free."}})

# 7 numeric: behind pace in another format
assert F(600, 60) == 10 and 240 // 10 == 24 and 24 - 20 == 4 and 240 // 6 - 20 == 20
H.append({"id": "h-behind-sixty", "difficulty": 3, "skills": ["mp-formats", "mp-speed"], "tags": ["checkpoints"],
          "prose": "A test has 60 questions in 10 minutes. At 4 minutes you finish question 20.",
          "question": "How many questions behind pace are you?",
          "widget": num(4, 0, label="Questions behind", accept="4: pace at 4 minutes is Q24.", wrong=[("used-six", 20, 0), ("sign", -4, 0)]),
          "feedback": {"correct": "10 s a question puts pace at Q24: 4 behind.", "generic": "Not quite right. Find this test's pace first.",
                       "byKey": {"used-six": "You used 6 s, the 80-in-8 pace. Here it is $600 \\div 60 = 10$ s.", "sign": "That says ahead. Pace is Q24 and you are at Q20."}},
          "explain": {"text": "600 s over 60 questions is 10 s each, so 240 s is Q24. You are at Q20, four behind, which is 40 s. Every test needs its own checkpoints."}})

# 8 longform
model = (
    "**The plan for the week before an 80-in-8 test.**\n\n"
    "**1. Warm-up every day.** Five rounds of the daily warm-up from Today, about 10 minutes. I note every score. This week my best is 41; the Stage 3 mark is 50. I aim for a best of 45 by Friday and a daily average that rises. A round at 50 is 2.4 s an answer, well inside the test's 6 s.\n\n"
    "**2. Drills from my last review.** My mock review found five fraction method gaps and three slow sequences. So each day:\n\n"
    "- 20 fraction sums at 6 s each, 2 minutes, one denominator first;\n"
    "- 12 sequences at 8 s each, 96 s, differences first.\n\n"
    "Slips get care, not a drill: I check the decimal point and the last digit.\n\n"
    "**3. One mock mid-week.** On Wednesday I sit a full mock of 80 against my own watch, then run the review: net score, block times, sort into slips, method gaps and time losses, count by kind. Thursday's drill follows from that count.\n\n"
    "**4. Checkpoints.** I write Q20 2:00, Q40 4:00, Q60 6:00 at the top of my paper before the test starts. Ten a minute.\n\n"
    "**5. Skip rules.** If the test allows skipping, I skip any question that looks like 12 s or more, two questions' worth, and return at the end. If it is forward only with +1 and −1, I cannot skip. I remove options fast: a blind guess is worth −0.5, after one removal −1/3, after two 0. So I guess only after removing two, or when unreached questions would score nothing anyway.\n\n"
    "**6. The first minute.** I start at a steady 6 s and let any hard early question go. Spending 30 s on question 3 costs four questions at the end. I take one breath between blocks of 20.\n\n"
    "**7. A bad start.** If I am 15 s behind at 2:00, that is 2.5 questions. I do not rush the easy kinds, which raises slips. I guess faster on the slow kinds, fractions and long sequences, and keep the rest at pace. A slow block costs a few questions; panic costs more.\n\n"
    "**8. The day before.** One warm-up round only, a tested link, a quiet room, pen and paper if allowed, and sleep.")
assert F(15, 6) == F(5, 2) and 6 + 6 + 30 + 73 * 6 == 480 and F(120, 50) == F(12, 5) and 20 * 6 == 120 and 12 * 8 == 96
H.append({"id": "h-long-week-plan", "difficulty": 5, "skills": ["mp-formats", "mp-speed"], "tags": ["test-week-plan"], "kind": "longform", "title": "The week before the test",
          "prompt": "Write your plan for the week before an 80-questions-in-8-minutes test. Include: (a) daily warm-up rounds and the scores you will track; (b) the drills you will do, chosen from an error review, with their target times; (c) when you will sit a mock and how you will review it; (d) your checkpoints; (e) your skip and guess rules for a test that allows skipping and for one that does not; (f) the first-minute rule; (g) what you will do after a bad start.",
          "model": model,
          "rubric": [{"points": 2, "text": "Plans daily warm-up rounds with a logged score and a target, such as the Stage 3 mark of 50."},
                     {"points": 2, "text": "Chooses drills from an error review, naming the kind, the count of questions and a target pace."},
                     {"points": 1, "text": "Sits a mock during the week and reviews it: net score, block times, slips, method gaps and time losses."},
                     {"points": 1, "text": "States the checkpoints: Q20 at 2:00, Q40 at 4:00, Q60 at 6:00."},
                     {"points": 2, "text": "Gives skip rules for both formats: skip and return where allowed; remove options and guess where not, with the guess values."},
                     {"points": 1, "text": "Applies the first-minute rule and a breath between blocks."},
                     {"points": 1, "text": "Says how to recover from a bad start, with a number: guess faster on slow kinds rather than rushing easy ones."}]})

hw = {"id": "homework-3", "course": "mental-pressure", "level": 3, "dueDays": 7, "items": H}
check_voice(hw, 'homework-3')
write('homework-3.json', hw)
