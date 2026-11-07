"""first-python level 3 (Functions and files): every graded key, wrong[] value and stated number, computed twice.
Second read, session V (docs/reviews/review-first-python-1-3.md). Method 1 runs the code the screen shows;
method 2 is a closed form or hand arithmetic. Claims are tied to their wording with lv.stated.
Checks that fail on the content as read are review findings (listed in the review's Tool results).
"""
import sys, os, io, math, contextlib, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("first-python", 3)
os.chdir(tempfile.mkdtemp())


def run(src):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(src, {})
    return buf.getvalue()


def two(a, b, label):
    ok = a == b or (isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) < 1e-9)
    lv.claim(ok, f'two methods agree: {label} ({a!r} vs {b!r})')
    return a


def err(src):
    try:
        exec(src, {})
    except Exception as x:
        return f'{type(x).__name__}: {x}'
    return None


# ---------- l9-packaging-steps ----------
L = "l9-packaging-steps"
two(run("def double(x):\n    return 2 * x\n\nprint(double(4) + 1)"), f"{2 * 4 + 1}\n", "double(4) + 1")
lv.expect(L, "screens[0].widget.options[1].text", 2 * (4 + 1))
two(run("def fee(px):\n    cost = px * 0.01\n    return cost\n\nprint(fee(250.00))"), "2.5\n", "fee(250.00)")
two(250.00 / 100, 2.5, "1% of 250")
for p, want in [(100.00, 101.5), (19.99, 21.49), (250.00, 251.5), (0.00, 1.5)]:
    two(round(p + 1.50, 2), want, f"with_fee({p})")
two(12.50 * 10 + 1.50, 126.5, "total_cost test 1")
lv.expect(L, "screens[4].feedback.byKey.test-1", (12.50 + 1.50) * 10)
lv.expect(L, "screens[4].feedback.byKey.test-1", 12.50 * 10)
two(round(3.20 * 250 + 1.50, 2), 801.5, "total_cost test 2")
two(run("def change(old, new):\n    return new - old\n\nprint(change(105.00, 100.00))"), "-5.0\n", "change(105, 100)")
lv.expect(L, "screens[5].widget.options[1].text", 105.0 - 100.0)
# the 'swapped' distractor: treating the first argument as new gives new - old = 105.0 - 100.0, not the option's -105.0
swapped = 105.0 - 100.0
lv.stated(L, "screens[5].widget.options[2].why", "You treated the first argument as `new`", swapped == -105.0)
two(100.00 - 1.50, 98.5, "net(100.00)")
lv.expect(L, "screens[6].explain.text", 98.5)
lv.expect(L, "screens[6].explain.text", "NameError: name 'left' is not defined")
lv.claim(err("print(left)") == "NameError: name 'left' is not defined", "NameError text for left")
lv.claim(err("g = None\ng * 10") == "TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'", "TypeError text for None * 10")
lv.expect(L, "screens[7].explain.text", "TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'")
two(103.00 - 100.00, 3.0, "daily_gain")
two((21.00 - 20.00) * 10, 10.0, "daily_gain test 3")
r = (245.00 - 250.00) / 250.00
two(r, -5 / 250, "daily return -0.02")
lv.expect(L, "screens[10].feedback.byKey.test-1", round((245 - 250) / 245, 4))
lv.expect(L, "screens[10].feedback.byKey.test-1", 245.00 - 250.00 / 250.00)
lv.expect(L, "screens[10].feedback.byKey.test-1", r * 100)
two((13.75 - 12.50) / 12.50, 0.1, "daily_return test 4")
two(run("def with_fee(price):\n    return price + 1.50\nprint(with_fee(10.00))"), "11.5\n", "quiz with_fee after the move")
lv.claim(err("print(with_fee(10.00))\ndef with_fee(price):\n    return price + 1.50") == "NameError: name 'with_fee' is not defined", "quiz NameError text")
two(run("def tax(amount):\n    print(amount * 0.2)\n\nt = tax(50.00)\nprint(t)"), "10.0\nNone\n", "quiz tax")
two(run("def grow(balance):\n    balance = balance + 50.00\n    return balance\n\nsavings = 500.00\ngrow(savings)\nprint(savings)"), "500.0\n", "quiz grow")
two(run("def cost(price, shares, fee):\n    return price * shares + fee\n\nprint(cost(2.40, 50, 1.50))"), "121.5\n", "quiz cost")
lv.expect(L, "quiz[3].widget.wrong[0].value", (2.40 + 1.50) * 50)
lv.expect(L, "quiz[3].widget.wrong[1].value", 2.40 * 50)

# ---------- l10-reading-errors ----------
L = "l10-reading-errors"
pr = [101.20, 102.50, 99.80, 100.40]
two(pr[2], 99.80, "prices[2]")
two(pr[1:3], [102.5, 99.8], "prices[1:3]")
lv.claim(err("prices = [101.20, 102.50, 99.80, 100.40]\nprint(prices[4])") == "IndexError: list index out of range", "IndexError text")
two(run("def average(xs):\n    return sum(xs) / len(xs)\nprint(average([101.20, 102.50]))"), "101.85\n", "average after the move")
lv.expect(L, "screens[3].explain.text", 101.85)
lv.claim(err("closes = [101.20, 102.50]\ncloses = closes.append(99.80)\ncount = len(closes)") == "TypeError: object of type 'NoneType' has no len()", "None has no len text")
lv.claim(err("def daily_return(p0, p1):\n    return (p1 - p0) / p0\nprint(daily_return(0.00, 101.20))") == "ZeroDivisionError: float division by zero", "float division by zero text")
two(round(float("101.20") + 1.50, 2), 102.7, "with_fee from text")
two(float(" 12.50\n") + 1.50, 14.0, "float ignores spaces and newline")
lv.claim(err('float("Close")') == "ValueError: could not convert string to float: 'Close'", "ValueError Close text")


def mdd(ps):
    pk, w = ps[0], 0.0
    for p in ps[1:]:
        pk = max(pk, p)
        w = max(w, (pk - p) / pk)
    return w


two(mdd([100.0, 110.0, 99.0, 105.0, 88.0, 95.0]), (110 - 88) / 110, "drawdown 22 / 110")
lv.expect(L, "screens[8].prose", 0.2)
two(mdd([50.00, 40.00, 60.00, 30.00]), (60 - 30) / 60, "drawdown test 5")
two(mdd([50.00, 40.00, 60.00]), (50 - 40) / 50, "the one-step-early loop never sees 30")
two(run("closes = [101.20, 102.50, 99.80, 100.40]\nprint(closes[1:])"), "[102.5, 99.8, 100.4]\n", "quiz slice")
two(len([101.20, 102.50, 99.80, 100.40]) - 1, 3, "quiz last index")
lv.claim(err("xs = [1, 2, 3, 4, 5]\nprint(sum(xs[5:]) / len(xs[5:]))") == "ZeroDivisionError: division by zero", "int division by zero text")

# ---------- l11-numbers-from-a-file ----------
L = "l11-numbers-from-a-file"
lv.claim(err('total = 0\ntotal = total + "101.20\\n"') == "TypeError: unsupported operand type(s) for +: 'int' and 'str'", "int + str text")
two(round(101.20 + 102.50 + 99.80, 2), 303.5, "the sum the slip expects")
two(float("Tue,102.50\n".split(",")[1]), 102.5, "close_from_row")
open("c.txt", "w").write("101.20\n102.50\n99.80\n")
two([float(l) for l in open("c.txt")], [101.2, 102.5, 99.8], "read_closes")
lv.claim(err('float("Close\\n")') == "ValueError: could not convert string to float: 'Close\\n'", "ValueError Close newline text")
open("p.csv", "w").write("Day,Close\nMon,101.20\nTue,102.50\nWed,99.80\nThu,100.40\nFri,101.10\n")
two([float(l.split(",")[1]) for l in open("p.csv").readlines()[1:]], [101.2, 102.5, 99.8, 100.4, 101.1], "read_csv_closes")
two(f"£{float(open('p.csv').readlines()[-1].split(',')[1]):.2f}", "£101.10", "last close")
lv.claim(err('float("\\n")') == "ValueError: could not convert string to float: '\\n'", "ValueError newline text")
two(len(["h"] + ["d"] * 20) - 1, 20, "quiz rows")
lv.expect(L, "quiz[2].widget.wrong[0].value", 21)
lv.expect(L, "quiz[2].widget.wrong[1].value", 19)
two("  101.20\n".strip() + "0", "101.200", "quiz strip")

# ---------- l12-savings-script ----------
L = "l12-savings-script"


def project(b, r_, n):
    for _ in range(n):
        b = b * (1 + r_)
    return b


two(round(project(2000.00, 0.04, 3), 2), round(2000 * 1.04 ** 3, 2), "2000 at 4% for 3 years")
lv.expect(L, "screens[0].widget.options[0].text", 2249.73)
lv.expect(L, "screens[0].widget.options[1].text", 2000 + 3 * 80)
lv.expect(L, "screens[0].widget.options[2].text", 2000 * 1.04)
lv.expect(L, "screens[0].widget.options[3].text", round(2000 * 1.04 ** 4, 2))
lv.expect(L, "screens[0].hints[1].text", round(2000 * 1.04 ** 2, 2))
lv.expect(L, "screens[0].hints[1].text", round(2000 * 1.04 ** 3, 3))
two(round(project(1000, 0.05, 10) - 1000, 2), round(1000 * (1.05 ** 10 - 1), 2), "ten-year gain at 5%")
lv.expect(L, "screens[1].widget.options[2].why", round(1000 * (1.05 ** 10 - 1), 2))
lv.expect(L, "screens[1].widget.options[2].why", round(1000 * (1.10 ** 10 - 1), 2))
lv.claim(1000 * (1.10 ** 10 - 1) > 2 * 1000 * (1.05 ** 10 - 1), "doubling the rate more than doubles the gain")
lv.expect(L, "screens[1].explain.text", round(1000 * 1.05 ** 9 * 0.05, 2))
lv.claim(1000 * 1.10 ** 10 < 2700, "the 10% bars fit under yMax 2700")
lv.expect(L, "screens[2].feedback.byKey.test-1", round(2000 * 1.04 ** 4, 2))


def saving(b, r_, n, d):
    for _ in range(n):
        b = b * (1 + r_) + d
    return b


two(saving(1000.00, 0.05, 2, 100.00), 1000 * 1.05 ** 2 + 100 * 1.05 + 100, "project_saving test 1")
two(round(saving(0.00, 0.04, 3, 500.00), 2), round(500 * (1.04 ** 2 + 1.04 + 1), 2), "project_saving test 2")
lv.expect(L, "screens[3].feedback.byKey.test-1", round(((1000 + 100) * 1.05 + 100) * 1.05, 2))
lv.expect(L, "screens[3].feedback.byKey.test-1", 1000 * 1.05 ** 2 + 200)
two(f"{1628.894626777442:.2f}", f"{round(1000 * 1.05 ** 10, 2):.2f}", "Year 10 balance")
two(round(project(1000.00, 0.10, 2), 6), 1210.0, "project(1000, 0.10, 2)")
lv.expect(L, "screens[9].widget.options[1].text", 1000 * (1 + 2 * 0.1))
lv.expect(L, "screens[9].widget.options[2].text", round(1000 * 0.1 ** 2, 6))
lv.expect(L, "screens[9].widget.options[3].text", round(1000 * 1.1 ** 3, 6))
cl = [101.2, 102.5, 99.8, 100.4, 101.1]
rets = [(b - a) / a for a, b in zip(cl, cl[1:])]
two([f"{x:.2%}" for x in rets], ["1.28%", "-2.63%", "0.60%", "0.70%"], "returns as percentages")
two(len(rets), len(cl) - 1, "five closes give four returns")
two(round(project(500.00, 0.10, 2), 2), round(500 * 1.1 ** 2, 2), "quiz 605")
lv.expect(L, "quiz[2].widget.wrong[0].value", 500 + 2 * 50)
lv.expect(L, "quiz[2].widget.wrong[1].value", 500 * 1.1)
two(f"{round(project(1000.00, 0.05, 10), 2)}", "1628.89", "quiz silent script print")
two(len(range(1, 5)), 4, "quiz range(1, 5)")

# ---------- review-3 ----------
R = "review"
two(round(5000.00 * 0.002, 6), 10.0, "fee 5000")
two(round(project(1500.00, 0.02, 3), 2), round(1500 * 1.02 ** 3, 2), "review compound")
lv.expect(R, "items[3].widget.wrong[0].value", 1500 + 3 * 30)
lv.expect(R, "items[3].widget.wrong[1].value", round(1500 * 1.02 ** 2, 2))
two(round(sum([101.20, 102.50, 99.80]) / 3, 2), 101.17, "average test 1")
lv.expect(R, "items[4].feedback.byKey.test-1", (101.20 + 102.50 + 99.80) / 2)
two(round(101.20 + 102.50, 2), 203.7, "scope sum")
two(round(sum(cl) / 5, 6), 101.0, "average close")
lv.expect(R, "items[6].feedback.byKey.test-1", round(sum(cl) / 6, 2))

# ---------- homework-3 ----------
H = "homework"
pnl = lambda b, s, n: (s - b) * n - 3.00
for args, want in [((100.00, 103.00, 50), 147.0), ((250.00, 245.00, 10), -53.0), ((10.00, 10.00, 100), -3.0), ((12.40, 12.90, 1000), 497.0)]:
    two(round(pnl(*args), 6), want, f"pnl{args}")
lv.expect(H, "items[0].feedback.byKey.test-1", 150 - 1.50)
lv.expect(H, "items[0].feedback.byKey.test-1", (3.00 - 3.00) * 50)
lv.expect(H, "items[0].feedback.byKey.test-1", (100 - 103) * 50 - 3)


def mdd2(ps):
    pk, w = ps[0], 0.0
    for p in ps:
        pk = max(pk, p)
        w = max(w, (pk - p) / pk)
    return w


for ps, want in [([100.00, 120.00, 90.00, 130.00], 0.25), ([100.00, 110.00, 99.00, 105.00, 88.00, 95.00], 0.2),
                 ([100.00, 80.00, 120.00, 60.00, 130.00], 0.5), ([100.00, 95.00, 90.00, 85.00], 0.15)]:
    two(round(mdd2(ps), 9), want, f"max_drawdown{ps}")
two(round((130 - 90) / 130, 2), 0.31, "high-low slip on test 1")
two((100 - 90) / 100, 0.1, "peak stuck at the first price")
one_day = max((a - b) / a for a, b in zip([100.0, 110.0, 99.0, 105.0, 88.0, 95.0], [110.0, 99.0, 105.0, 88.0, 95.0]))
two(round(one_day, 3), round(17 / 105, 3), "one-day falls on test 2")
lv.expect(H, "items[1].feedback.byKey.test-2", round(one_day, 3))
lv.claim("99.80\n" > "102.50\n", "as text '99.80' beats '102.50'")
two(f"{0.012845849802371512:.2%}", "1.28%", "log_result format")
two(round(project(1000.00, 0.05, 3), 3), 1157.625, "grow would give 1157.625")
two(round(saving(0, 0.05, 3, 200.00), 2), round(200 * (1.05 ** 2 + 1.05 + 1), 2), "deposits at year end")
lv.expect(H, "items[6].widget.wrong[1].value", round(200 * (1.05 ** 3 + 1.05 ** 2 + 1.05), 2))
lv.expect(H, "items[6].feedback.correct", 410.00)

lv.check_wrongs()
lv.report()
