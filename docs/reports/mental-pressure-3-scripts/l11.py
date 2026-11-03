from common import *
from decimal import Decimal as D


def mins(t):
    h, m = map(int, t.split(':'))
    return 60 * h + m


def clock(x):
    x %= 24 * 60
    return f"{x // 60:02d}:{x % 60:02d}"


# ---------- numbers, twice ----------
assert 300 * (D('4.40') - D('4.25')) == 45 and 300 * D('4.40') - 300 * D('4.25') == 45 and 300 * D('4.40') == 1320
assert mins('14:47') == 887 and 887 + 158 == 1045 and clock(1045) == '17:25' and 47 + 38 == 85 and 2 * 60 + 38 == 158
assert clock(887 + 120) == '16:47' and clock(887 + 180) == '17:47'
assert D('1.12') * D('0.88') == D('0.9856') and 1 - D('0.12') ** 2 == D('0.9856')
assert D(1250) * D('0.04') * 9 / 12 == D('37.5') and D(1250) * D('0.04') == 50 and D(1250) * D('0.04') * 9 == 450 and D(1250) * D('0.04') * 3 / 12 == D('12.5')
assert D('2.99') + D('4.49') + D('7.99') == D('15.47') and 3 + D('4.5') + 8 - D('0.03') == D('15.47') and D('15.47') * 4 == D('61.88')
assert 300 * D('4.25') == 1275 and round(45 / 1275, 6) == 0.035294 and round(0.15 / 4.40, 6) == 0.034091
assert D(2400) * D('0.35') == 840 and 2400 - 840 == 1560 and 2400 * D('3.20') == 7680 and 840 * D('3.20') == 2688
assert D(2400) * D('0.05') * 6 / 12 == 60 and D(2400) * D('0.05') * 6 == 720 and D(2400) * D('0.05') == 120
assert 1500 * (D('12.60') - D('12.52')) == 120 and 2000 * D('0.08') == 160 and 1500 * (D('12.60') - D('12.48')) == 180
assert 1200 * D('0.85') == 1020 and 1200 * 85 == 102000
assert mins('11:15') - mins('09:50') == 85 and 1115 - 950 == 165
assert D(3600) * D('0.35') == 1260 and 3600 - 1260 == 2340 and D(3600) * D('0.15') == 540
assert D(84) / D('1.2') == 70 and D(84) * D('0.8') == D('67.2')
DRILL = [("Buy 200 at £3.15, sell at £3.40: profit (£)", D(200) * D('0.25'), "£"),
         ("A share rises 10%, then falls 10%: net change (%)", D('1.1') * D('0.9') - 1, "%"),
         ("An order of 1,800 shares is 40% filled: shares filled", D(1800) * D('0.4'), ""),
         ("Leave 09:38; the journey takes 1 h 47 min: arrive at", clock(mins('09:38') + 107), "t"),
         ("£800 at 3% simple interest for 6 months: interest (£)", D(800) * D('0.03') / 2, "£"),
         ("Items at £1.99, £5.49 and £3.99: total (£)", D('1.99') + D('5.49') + D('3.99'), "£"),
         ("2,500 shares at 64p each: cost (£)", D(2500) * D('0.64'), "£"),
         ("Bought 400 at £7.45, sold at £7.20: P&L (£)", 400 * (D('7.20') - D('7.45')), "£"),
         ("A 90-minute call starts at 16:45: it ends at", clock(mins('16:45') + 90), "t"),
         ("£50 rises 20%, then 20% again: new price (£)", D(50) * D('1.2') * D('1.2'), "£")]
assert [str(v) for _, v, _ in DRILL] == ['50.00', '-0.01', '720.0', '11:25', '12.00', '11.47', '1600.00', '-100.00', '18:15', '72.00']
assert 2 + D('5.5') + 4 - D('0.03') == D('11.47') and 47 + 38 == 85

screens = []

# 1 hook
screens.append({
    "type": "problem", "difficulty": 1,
    "prose": "A trading test asks: you buy 300 shares at £4.25 and sell them at £4.40. Before computing, write one line: 300 times the gain on each share.",
    "canvas": table_canvas(["Trade", "Shares", "Price"], [["Buy", "300", "£4.25"], ["Sell", "300", "£4.40"]], align=["left", "right", "right"]),
    "question": "What is the profit, in pounds?",
    "widget": num(45, 0.001, unit="£", label="Profit", accept="£45: $300 \\times 0.15$.", wrong=[("sale-value", 1320, 0.01), ("per-share", 0.15, 0.001), ("point", 4.5, 0.001)]),
    "hints": hints("Find the gain on one share first.", "$4.40 - 4.25 = 0.15$, so 15p a share.", "$300 \\times 0.15 = 45$.", ["r1"]),
    "feedback": {"correct": "15p a share on 300 shares: £45.", "generic": "Not quite right. Multiply the shares by the gain on each.",
                 "byKey": {"sale-value": "£1,320 is what the sale brings in. The profit is the sale less the £1,275 cost.",
                           "per-share": "15p is the gain on one share. There are 300 shares.", "point": "The point slipped: $300 \\times 0.15 = 45$, not 4.5."}},
    "explain": {"text": "One line, $300 \\times (4.40 - 4.25)$, avoids two big products. The gain is 15p, and $300 \\times 0.15 = 45$. Multiplying 300 by each price would mean £1,320 less £1,275, slower and riskier."},
})

# 2 explore: the train
screens.append({
    "type": "explore", "difficulty": 1,
    "prose": "A train leaves at 14:47 and takes 2 h 38 min. Drag the point to the arrival time. The bar is the journey, and the caption converts the minutes for you.",
    "canvas": {"kind": "number-line",
               "params": {"min": 880, "max": 1080, "step": 20, "snap": 1, "labels": [{"x": 900, "text": "15:00"}, {"x": 960, "text": "16:00"}, {"x": 1020, "text": "17:00"}, {"x": 1080, "text": "18:00"}]},
               "state": {"points": [{"id": "dep", "x": 887, "label": "14:47"}, {"id": "arr", "x": 900, "label": "Arrives"}], "intervals": [{"id": "trip", "from": 887, "to": 900, "colour": 2, "row": 1}]},
               "derive": {"trip.to": "max(arr.x, 887)",
                          "caption": "Arrives {{floor(arr.x / 60)}}:{{(arr.x % 60 < 10 ? \"0\" : \"\") + fixed(arr.x % 60, 0)}}, after {{floor(max(arr.x - 887, 0) / 60)}} h {{max(arr.x - 887, 0) % 60}} min"}},
    "question": "Drag the point to when the train arrives.",
    "widget": {"kind": "drag-point", "points": [{"id": "arr", "target": 1045, "tol": 0.5}],
               "wrong": [{"id": "hours-only", "region": {"x": [1006.5, 1007.5]}}, {"id": "rounded", "region": {"x": [1066.5, 1067.5]}}]},
    "hints": hints("Add the 2 hours first.", "14:47 plus 2 hours is 16:47. Then add 38 minutes.", "$47 + 38 = 85$ minutes, which is 1 h 25: 17:25.", ["arr"]),
    "feedback": {"correct": "16:47 plus 38 minutes is 17:25.", "generic": "Not quite right. Drag until the caption reads 2 h 38 min.",
                 "byKey": {"hours-only": "16:47 adds the 2 hours but not the 38 minutes.", "rounded": "17:47 adds 3 hours. The journey is 22 minutes short of that.",
                           "arr": "Drag until the caption says 2 h 38 min, then read the arrival."}},
    "explain": {"text": "Two hours take 14:47 to 16:47, and 38 more minutes make $47 + 38 = 85$. Eighty-five minutes is 1 h 25, so the train arrives at 17:25. Turning 85 minutes into hours is the unit change these questions hide.",
                "canvas": {"points": {"arr": {"x": 1045}}}},
})

# 3 name: one line
w = {"kind": "table", "columns": ["Step", "Value"], "rows": [
    ["Factor for +12%", cell(1.12, 0.00005)], ["Factor for −12%", cell(0.88, 0.00005)], ["One line: their product", cell(0.9856, 0.00005)], ["Net change (%)", cell(-0.0144, 0.00005, unit="%")]]}
screens.append({
    "type": "problem", "difficulty": 2,
    "prose": "You turned words into **one line** of arithmetic before computing. Try it on \"a share rises 12%, then falls 12%\". Each change is a growth factor, and the line is their product.",
    "canvas": table_canvas(["Words", "One line"], [["rises 12%", "× 1.12"], ["then falls 12%", "× 0.88"]], align=["left", "left"]),
    "question": "Fill in the factors, the line's product and the net change.",
    "widget": w,
    "hints": hints("+12% multiplies by 1.12.", "$1.12 \\times 0.88 = (1 + 0.12)(1 - 0.12)$.", "$1 - 0.12^2 = 0.9856$, so −1.44%.", ["r1"]),
    "feedback": {"correct": "$1.12 \\times 0.88 = 0.9856$: a net fall of 1.44%.", "generic": "Not quite right. Write each factor, then multiply.",
                 "byKey": {"r0c1": "+12% multiplies by 1.12.", "r1c1": "−12% multiplies by 0.88.", "r2c1": "$(1 + 0.12)(1 - 0.12) = 1 - 0.0144 = 0.9856$.",
                           "r3c1": "A factor of 0.9856 is a fall of 1.44%, not 0%. The fall acts on the higher price."}},
    "explain": {"text": "The line $1.12 \\times 0.88$ is a difference of two squares: $1 - 0.12^2 = 0.9856$. So the share ends 1.44% down. Writing the line first stops you adding +12 and −12 to get 0."},
})

# 4 ladder: interest, with a number that does not matter
screens.append({
    "type": "ladder", "difficulty": 2,
    "prose": "On 3 March a client deposits £1,250 at 4% a year, simple interest. Some numbers in the words are not in the line. Write the line before computing.",
    "canvas": table_canvas(["In the words", "In the line?"], [["3 March", "?"], ["£1,250", "?"], ["4% a year", "?"], ["9 months", "?"]], align=["left", "left"]),
    "question": "What interest is due after 9 months, in pounds?",
    "widget": num(37.5, 0.001, unit="£", label="Interest", accept="£37.50: $1250 \\times 0.04 \\times \\tfrac{9}{12}$.",
                  wrong=[("year", 50, 0.001), ("months-as-years", 450, 0.01), ("used-date", 12.5, 0.001)]),
    "hints": hints("A year's interest is 4% of £1,250.", "A year's interest is £50. Nine months is $\\tfrac34$ of a year.", "$50 \\times \\tfrac34 = 37.50$.", ["r3"]),
    "feedback": {"correct": "£50 a year, and nine months is three quarters: £37.50.", "generic": "Not quite right. Find a year's interest, then take $\\tfrac{9}{12}$ of it.",
                 "byKey": {"year": "£50 is a full year. The deposit earns for 9 months, so $\\tfrac34$ of £50.",
                           "months-as-years": "You multiplied by 9 as if it were 9 years. Nine months is $\\tfrac{9}{12}$ of a year.",
                           "used-date": "You used the 3 from 3 March as 3 months. The date is not in the line; the term is 9 months."}},
    "explain": {"text": "The line is $1250 \\times 0.04 \\times \\tfrac{9}{12}$, and the date is not in it. A year's interest is £50, and three quarters of that is £37.50. Spotting the number that does not matter is half these questions.",
                "canvas": {"values": {"r0c1": "no", "r1c1": "yes", "r2c1": "yes", "r3c1": "yes"}}},
})

# 5 ladder: shopping
screens.append({
    "type": "ladder", "difficulty": 2,
    "prose": "A desk of 4 traders orders lunch: one item at £2.99, one at £4.49 and one at £7.99. Round each up to a round price, add, then take off the pennies you added.",
    "canvas": table_canvas(["Price", "Rounded up", "Added"], [["£2.99", "£3", "1p"], ["£4.49", "£4.50", "1p"], ["£7.99", "£8", "1p"]], align=["right", "right", "right"]),
    "question": "What is the total, in pounds?",
    "widget": num(15.47, 0.001, unit="£", label="Total", accept="£15.47: £15.50 less 3p.", wrong=[("no-pence", 15.5, 0.001), ("times-desk", 61.88, 0.001), ("one-penny", 15.49, 0.001)]),
    "hints": hints("Round to £3, £4.50 and £8.", "$3 + 4.50 + 8 = 15.50$.", "Each rounding added 1p: $15.50 - 0.03 = 15.47$.", ["c2"]),
    "feedback": {"correct": "£15.50 less 3p: £15.47.", "generic": "Not quite right. Add the rounded prices, then take off the 3p.",
                 "byKey": {"no-pence": "£15.50 is the rounded sum. Each item was rounded up by 1p, so take off 3p.",
                           "times-desk": "You multiplied by the 4 traders. The order is three items, one of each.",
                           "one-penny": "You took off 1p. Each of the three roundings added 1p, so take off 3p."}},
    "explain": {"text": "£3, £4.50 and £8 make £15.50. Three roundings of 1p each mean the true total is 3p less: £15.47. The 4 traders were a number in the words, not in the line.",
                "canvas": {"highlight": {"cols": [2]}}},
})

# 6 follow-up
screens.append({
    "type": "ladder", "difficulty": 3, "title": "The follow-up",
    "prose": "Back to the trade: bought 300 at £4.25, sold at £4.40, a profit of £45. The interviewer follows up: what is that as a return on the money you put in?",
    "canvas": table_canvas(["Trade", "Shares", "Price"], [["Buy", "300", "£4.25"], ["Sell", "300", "£4.40"]], align=["left", "right", "right"]),
    "question": "What is the return on the cost, in percent?",
    "widget": num(0.035294, 0.0005, unit="%", label="Return", accept="3.53%: 15p on £4.25.", wrong=[("sale-price", 0.034091, 0.0003), ("pence", 0.0015, 0.0003)]),
    "hints": hints("The money put in is the cost, £1,275.", "Per share: 15p on £4.25.", "$0.15 \\div 4.25 = 0.0353$, so 3.53%.", ["r0"]),
    "feedback": {"correct": "15p on £4.25, or £45 on £1,275: 3.53%.", "generic": "Not quite right. Divide the gain by the price you paid.",
                 "byKey": {"sale-price": "You divided by £4.40, the sale price. A return is measured on what you paid: £4.25.",
                           "pence": "You typed 0.15, the gain in pounds, as the percentage. Divide it by £4.25."}},
    "explain": {"text": "The line is $\\tfrac{0.15}{4.25}$: the share count cancels. $\\tfrac{0.15}{4.25}$ is a little over $\\tfrac{0.15}{4.5} = 3.33\\%$, and it is 3.53%. One line again: the gain over what you paid."},
})

# 7 trap
screens.append({
    "type": "trap", "difficulty": 2,
    "prose": "An order to buy 2,400 shares at £3.20 is 35% filled.",
    "canvas": table_canvas(["Order", "Detail"], [["Size", "2,400 shares"], ["Limit price", "£3.20"], ["Status", "35% filled"]], align=["left", "left"]),
    "question": "How many shares have been bought so far?",
    "widget": num(840, 0, label="Shares bought", accept="840: 35% of 2,400.", wrong=[("left", 1560, 0), ("price", 7680, 0), ("value", 2688, 0)]),
    "hints": hints("\"Filled\" is the part already done.", "10% of 2,400 is 240.", "35% is $3.5 \\times 240 = 840$.", ["r2"]),
    "feedback": {"correct": "35% of 2,400: 840 shares bought.", "generic": "Not quite right. Take 35% of the 2,400 shares.",
                 "byKey": {"left": "1,560 is the 65% still to fill. You read \"35% filled\" as 35% left.",
                           "price": "£7,680 is the full order's value. The question asks for shares, and the price is not in the line.",
                           "value": "You found 840 shares and then multiplied by £3.20. The question asks for shares, not pounds."}},
    "explain": {"text": "\"35% filled\" means 35% done: $0.35 \\times 2400 = 840$. The price is in the words but not in this line. Reading filled as left gives 1,560, the most common slip."},
})

# 8 generalise
screens.append({
    "type": "generalise", "difficulty": 2,
    "prose": "Every answer came from one line, written before any arithmetic: shares times gain, a product of factors, part of a whole. Interest has its own line, with the months turned into years: $$\\text{interest} = P \\times \\frac{r}{100} \\times \\frac{m}{12}$$",
    "question": "£2,400 at 5% a year simple interest for 6 months: what interest is due, in pounds?",
    "widget": num(60, 0.001, unit="£", label="Interest", accept="£60: half of £120.", wrong=[("year", 120, 0.001), ("months-as-years", 720, 0.01)]),
    "feedback": {"correct": "£120 a year, half of it for 6 months: £60.", "generic": "Not quite right. Find a year's interest, then take $\\tfrac{6}{12}$ of it.",
                 "byKey": {"year": "£120 is a full year. Six months is half of that.", "months-as-years": "You multiplied by 6 as if it were years. Divide the months by 12."}},
    "explain": {"text": "$2400 \\times 0.05 = 120$ a year, and $\\tfrac{6}{12}$ of that is £60. The months-to-years step is the unit change. Leave it out and the answer is twelve times too big."},
})

# 9 derive
screens.append({
    "type": "derive", "difficulty": 3,
    "prose": "Write the interest line as one formula. $P$ is the deposit in pounds, $r$ the yearly rate in percent and $m$ the months. Fold the 100 and the 12 into one number.",
    "question": "Simple interest equals what?",
    "widget": {"kind": "expression", "answer": "\\frac{Prm}{1200}", "accept": ["P*r*m/1200", "Prm/1200", "(P*r*m)/1200", "P r m/1200"], "keyboard": "algebra",
               "wrong": [{"id": "years", "tex": "\\frac{Prm}{100}"}, {"id": "no-percent", "tex": "\\frac{Prm}{12}"}]},
    "hints": hints("Start from $P \\times \\tfrac{r}{100} \\times \\tfrac{m}{12}$.", "Multiply the tops and the bottoms.", "$\\dfrac{Prm}{100 \\times 12} = \\dfrac{Prm}{1200}$."),
    "feedback": {"correct": "$\\dfrac{Prm}{1200}$: the rate turned into a fraction and the months into years.", "generic": "Not quite right. Divide by 100 for the percent and by 12 for the months.",
                 "byKey": {"years": "That treats $m$ as years. Divide the months by 12 as well.", "no-percent": "That leaves $r$ as a whole number. Divide by 100 for the percent."}},
    "explain": {"text": "$P \\times \\tfrac{r}{100} \\times \\tfrac{m}{12} = \\tfrac{Prm}{1200}$. Check: $\\tfrac{1250 \\times 4 \\times 9}{1200} = 37.5$. Folding the constants once saves a step every time."},
})

# 10 code
code = {"kind": "code", "language": "python",
        "starter": "def minutes_between(t1, t2):\n    # t1 and t2 are 'HH:MM' on a 24-hour clock\n    ...\n\n\ndef simple_interest(principal, rate, months):\n    # rate is a yearly percentage\n    ...\n",
        "solution": "def minutes_between(t1, t2):\n    h1, m1 = map(int, t1.split(':'))\n    h2, m2 = map(int, t2.split(':'))\n    return (h2 * 60 + m2 - h1 * 60 - m1) % (24 * 60)\n\n\ndef simple_interest(principal, rate, months):\n    return principal * rate / 100 * months / 12\n",
        "examples": [{"call": "minutes_between('14:47', '17:25')", "expect": "158", "compare": "equal"}, {"call": "simple_interest(1250, 4, 9)", "expect": "37.5", "compare": "isclose"}],
        "tests": [{"call": "minutes_between('14:47', '17:25')", "expect": "158", "compare": "equal"},
                  {"call": "minutes_between('09:50', '11:15')", "expect": "85", "compare": "equal"},
                  {"call": "minutes_between('09:38', '11:25')", "expect": "107", "compare": "equal"},
                  {"call": "minutes_between('10:00', '10:00')", "expect": "0", "compare": "equal"},
                  {"call": "minutes_between('22:35', '02:25')", "expect": "230", "compare": "equal"},
                  {"call": "minutes_between('23:59', '00:01')", "expect": "2", "compare": "equal"},
                  {"call": "simple_interest(1250, 4, 9)", "expect": "37.5", "compare": "isclose"},
                  {"call": "simple_interest(2400, 5, 6)", "expect": "60.0", "compare": "isclose"},
                  {"call": "simple_interest(800, 3, 6)", "expect": "12.0", "compare": "isclose"},
                  {"call": "simple_interest(10000, 3.5, 12)", "expect": "350.0", "compare": "isclose"},
                  {"call": "simple_interest(5000, 4.5, 1)", "expect": "18.75", "compare": "isclose"},
                  {"call": "simple_interest(1000, 0, 12)", "expect": "0.0", "compare": "isclose", "tol": {"abs": 1e-09}}],
        "how": "Check runs 12 hidden tests: six time gaps (exact minutes, two of them past midnight) and six interest sums (math.isclose)."}
screens.append({
    "type": "problem", "difficulty": 3, "title": "Check your methods in code",
    "prose": "Two checks for your fast methods. `minutes_between(t1, t2)` returns the minutes from one `'HH:MM'` time to the next; if `t2` is earlier, it is the next day. `simple_interest(principal, rate, months)` returns the interest in pounds.",
    "canvas": table_canvas(["Check", "Answer"], [["14:47 to 17:25", "158 minutes"], ["£1,250 at 4% for 9 months", "£37.50"]], align=["left", "right"]),
    "question": "Complete both functions.",
    "widget": code,
    "hints": hints("Turn each time into minutes after midnight.", "`h * 60 + m`, then subtract. `% (24 * 60)` handles the next day.", "Interest is `principal * rate / 100 * months / 12`.", ["r0"]),
    "feedback": {"correct": "Both checks agree with your fast methods.", "generic": "Not quite right. Work in minutes after midnight, and turn months into years."},
    "explain": {"text": "Minutes after midnight make every time a plain number. The remainder by 1,440 turns 22:35 to 02:25 into 230 minutes rather than a negative gap. The interest is the lesson's one line, $\\tfrac{Prm}{1200}$."},
})

# 11 drill
rows, notes = [], []
for q, v, u in DRILL:
    if u == "t":
        rows.append([q, cell(v, accept=[v.replace(':', '.'), v.replace(':', '')], placeholder="HH:MM")])
    elif u == "%":
        rows.append([q, cell(float(v), 0.0005, unit="%")])
    else:
        rows.append([q, cell(float(v), 0.001)])
notes = ["$200 \\times 0.25 = 50$.", "$1.1 \\times 0.9 = 0.99$: −1%.", "$0.4 \\times 1800 = 720$.", "09:38 plus 1 h is 10:38; $38 + 47 = 85$ minutes, 1 h 25: 11:25.",
         "£24 a year; half of it is £12.", "£2 + £5.50 + £4 = £11.50, less 3p: £11.47.", "$2500 \\times 0.64 = 1600$: £1,600, not 160,000p.",
         "$400 \\times (7.20 - 7.45) = -100$: a loss of £100.", "16:45 plus 1 h 30 min is 18:15.", "$1.2 \\times 1.2 = 1.44$, and $50 \\times 1.44 = 72$."]
screens.append({
    "type": "problem", "difficulty": 3, "title": "Drill: ten word problems", "tags": ["drill-word-problems"],
    "prose": "Ten word problems. Target pace: 10 seconds each, 100 seconds in all. The app does not time you, so use your own watch. Write the one line in your head first. Times as HH:MM; a loss with a minus sign.",
    "question": "Fill in all ten.",
    "widget": {"kind": "table", "columns": ["Problem", "Answer"], "rows": rows},
    "hints": hints("Say the one line before any number.", "Row 4: 38 + 47 minutes is 85, which is 1 h 25.", "50, −1, 720, 11:25, 12, 11.47, 1,600, −100, 18:15, 72."),
    "feedback": {"correct": "All ten right. Note your time against the 100-second target.", "generic": "Not quite right. Redo the amber rows from the one line.",
                 "byKey": {f"r{i}c1": t for i, t in enumerate(notes)}},
    "explain": {"text": "Each row was one line: shares times gain, a product of factors, a percentage of a whole, minutes carried into hours. Rows 4, 7 and 9 needed a unit change. Those are the ones to time again."},
})

# 12 transfer
screens.append({
    "type": "transfer", "difficulty": 3,
    "prose": "A trading assessment's scenario: you quote 2,000 shares at £12.48 bid and £12.52 ask. A client buys 1,500 from you at the ask. Then the mid price moves to £12.60.",
    "canvas": table_canvas(["Event", "Detail"], [["Your quote", "2,000 at £12.48 / £12.52"], ["Client buys", "1,500 at £12.52"], ["New mid", "£12.60"]], align=["left", "left"]),
    "question": "What is your P&L on the 1,500 shares, marked at the new mid, in pounds?",
    "widget": num(-120, 0.001, unit="£", label="P&L", accept="−£120: short 1,500 at £12.52, now £12.60.",
                  wrong=[("quote-size", -160, 0.001), ("sign", 120, 0.001), ("bid", -180, 0.001)]),
    "hints": hints("The client bought, so you sold: you are short 1,500.", "You sold at £12.52, and they are now worth £12.60: 8p against you.", "$-1500 \\times 0.08 = -120$.", ["r1"]),
    "feedback": {"correct": "Short 1,500, 8p against you: −£120.", "generic": "Not quite right. You sold 1,500 at £12.52; mark them at £12.60.",
                 "byKey": {"quote-size": "You used the 2,000 quoted. Only 1,500 traded.", "sign": "You sold, and the price rose, so it is a loss: −£120.",
                           "bid": "You sold at the ask, £12.52, not the bid. The move against you is 8p, not 12p."}},
    "explain": {"text": "The line is $1500 \\times (12.52 - 12.60) = -120$. The 2,000 and the £12.48 are in the story but not in the line. Scenario questions test exactly that reading, at speed."},
})

quiz = []
quiz.append({"id": "q-pence-pounds", "difficulty": 2, "prose": "1,200 shares at 85p each.", "question": "What do they cost, in pounds?",
             "widget": num(1020, 0.001, unit="£", label="Cost", accept="£1,020: 102,000p.", wrong=[("pence", 102000, 0.01), ("point", 102, 0.001)]),
             "feedback": {"correct": "$1200 \\times 0.85 = 1020$: £1,020.", "generic": "Not quite right. Turn 85p into £0.85 first.",
                          "byKey": {"pence": "102,000 is the cost in pence. Divide by 100 for pounds.", "point": "The point slipped. $1200 \\times 0.85 = 1020$."}},
             "explain": {"text": "85p is £0.85, and $1200 \\times 0.85 = 1020$. The unit change from pence to pounds is a factor of 100."}})
quiz.append({"id": "q-meeting-length", "difficulty": 2, "prose": "A meeting runs from 09:50 to 11:15.", "question": "How many minutes does it last?",
             "widget": num(85, 0, unit="minutes", label="Length", accept="85 minutes: 10 to 10:00, then 75.", wrong=[("decimal", 165, 0)]),
             "feedback": {"correct": "10 minutes to 10:00, then 1 h 15: 85 minutes.", "generic": "Not quite right. Count up to the next hour, then on.",
                          "byKey": {"decimal": "You subtracted 950 from 1,115, as if an hour had 100 minutes."}},
             "explain": {"text": "From 09:50 to 10:00 is 10 minutes, then 1 h 15 to 11:15. That makes 85 minutes. Counting up past the hour avoids the 100-minute slip."}})
quiz.append({"id": "q-two-fills", "difficulty": 3, "prose": "An order for 3,600 shares is 15% filled by 10:00 and another 20% by noon.", "question": "How many shares are filled by noon?",
             "widget": num(1260, 0, label="Shares filled", accept="1,260: 35% of 3,600.", wrong=[("left", 2340, 0), ("first-only", 540, 0)]),
             "feedback": {"correct": "15% and 20% make 35%: 1,260 shares.", "generic": "Not quite right. Add the two fills, then take that share of 3,600.",
                          "byKey": {"left": "2,340 is the 65% still open. Filled is the part done.", "first-only": "540 is the 15% by 10:00. Add the noon fill too."}},
             "explain": {"text": "Both fills are shares of the same 3,600, so they add: 35%. And 35% of 3,600 is 1,260. The times are in the words, not the line."}})
quiz.append({"id": "q-vat-back", "difficulty": 3, "prose": "A bill of £84 includes VAT at 20%.", "question": "What was the price before VAT, in pounds?",
             "widget": num(70, 0.001, unit="£", label="Before VAT", accept="£70: $84 \\div 1.2$.", wrong=[("took-20", 67.2, 0.001)]),
             "feedback": {"correct": "$84 \\div 1.2 = 70$.", "generic": "Not quite right. The £84 is 120% of the price.",
                          "byKey": {"took-20": "You took 20% off £84. The VAT was 20% of the lower price, so divide by 1.2."}},
             "explain": {"text": "£84 is 1.2 times the price, so the line is $84 \\div 1.2 = 70$. Check: 20% of £70 is £14, and $70 + 14 = 84$."}})

lesson = {
    "id": "l11-word-problems", "course": "mental-pressure", "title": "Word problems at speed", "minutes": 14,
    "objectives": ["Turn short word problems into arithmetic quickly."], "skills": ["mp-formats"],
    "screens": screens,
    "summary": {"ideas": ["Write one line of arithmetic before computing: shares × gain, a product of factors, a share of a whole.",
                          "Some numbers in the words are not in the line: dates, sizes quoted, prices when shares are asked.",
                          "Watch the units: minutes carry into hours at 60, pence into pounds at 100, months into years at 12."],
                "formula": {"name": "Simple interest", "tex": "\\text{interest} = \\dfrac{Prm}{1200}", "note": "£1,250 at 4% for 9 months: £37.50."},
                "trap": "Reading \"35% filled\" as 35% left: 2,400 shares 35% filled is 840 bought, not 1,560."},
    "quiz": quiz,
}
check_voice(lesson, 'l11')
write('l11-word-problems.json', lesson)
