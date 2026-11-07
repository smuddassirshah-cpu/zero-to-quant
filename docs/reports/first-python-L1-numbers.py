"""first-python level 1 (Values): every graded key, wrong[] value and stated number, computed twice.
Second read, session V (docs/reviews/review-first-python-1-3.md). Method 1 runs the Python the screen shows;
method 2 is hand arithmetic. Claims are tied to their wording with lv.stated, so they pass once a fix rewords them.
Checks that fail on the content as read are review findings (listed in the review's Tool results).
"""
import sys, os, io, contextlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("first-python", 1)


def run(src):
    """Method 1: what the program prints, as Python prints it."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(src, {'input': lambda p='': TYPED.pop(0)})
    return buf.getvalue()


TYPED = []


def two(a, b, label):
    lv.claim(a == b or (isinstance(a, float) and abs(a - b) < 1e-9), f'two methods agree: {label} ({a!r} vs {b!r})')
    return a


# ---------- l1-calculator ----------
L = "l1-calculator"
two(run("print(2 + 3 * 4)"), f"{2 + 12}\n", "2 + 3 * 4")
lv.expect(L, "screens[0].widget.options[0].text", 14)
lv.expect(L, "screens[0].widget.options[1].text", (2 + 3) * 4)
lv.expect(L, "screens[1].widget.options[0].text", "3.0")
two(run("print(6 / 2)"), "3.0\n", "6 / 2")
lv.expect(L, "screens[1].widget.options[2].text", 7 / 2)
lv.expect(L, "screens[1].explain.text", 3.5)
two(run("print(7 / 2)\nprint(7 // 2)"), "3.5\n3\n", "7 / 2 then 7 // 2")
two(run("print(19 // 5)"), f"{(19 - 19 % 5) // 5}\n", "19 // 5")
lv.expect(L, "screens[4].widget.options[0].text", 3)
lv.expect(L, "screens[4].widget.options[2].text", 19 / 5)
lv.expect(L, "screens[4].widget.options[1].text", round(19 / 5))
two(run("print(2 * 3 ** 2)"), f"{2 * 9}\n", "2 * 3 ** 2")
lv.expect(L, "screens[5].widget.options[0].text", 18)
lv.expect(L, "screens[5].widget.options[1].text", (2 * 3) ** 2)
lv.expect(L, "screens[5].widget.options[2].text", 2 * 3 * 2)
lv.expect(L, "screens[5].widget.options[3].text", 2 ** 6)
two(run("print(10 + 14 / 2)"), "17.0\n", "10 + 14 / 2")
lv.expect(L, "screens[6].widget.options[1].text", "17.0")
lv.expect(L, "screens[6].widget.options[0].text", "12.0")
two(run("print((10 + 14) / 2)"), f"{24 / 2}\n", "(10 + 14) / 2")
two(run("print(8 - 6 / 2)"), "5.0\n", "8 - 6 / 2")
lv.expect(L, "screens[8].feedback.correct", 5.0)
two(10 - 4 - 3, (10 - 4) - 3, "10 - 4 - 3 left to right")
lv.expect(L, "screens[8].explain.text", 3)
two(run("print((262.5 - 250) / 250)"), "0.05\n", "return 12.50 / 250")
two(run("print(262.5 - 250 / 250)"), f"{262.5 - 1.0}\n", "the unbracketed slip")
lv.expect(L, "screens[9].feedback.byKey.test-1", 261.5)
lv.expect(L, "screens[9].explain.text", 12.50)
two(run("print(3 + 4 * 2)"), "11\n", "quiz 3 + 4 * 2")
lv.expect(L, "quiz[0].widget.options[1].text", (3 + 4) * 2)
two(run("print(type(8 / 4))"), "<class 'float'>\n", "type(8 / 4)")
two(20 // 6, int(20 / 6), "20 // 6 (positive, so chop and floor agree)")
lv.expect(L, "quiz[2].widget.answer", 3)
lv.expect(L, "quiz[2].feedback.correct", 20 - 3 * 6)
lv.claim(abs(20 / 6 - 3.3333) <= 0.01, "quiz[2] wrong 'decimal' 3.3333 is 20 / 6 within its tol")
# claims
power_left_to_right = (2 ** 3 ** 2) == ((2 ** 3) ** 2)
two(2 ** 3 ** 2, 512, "2 ** 3 ** 2 groups right to left")
two(power_left_to_right, False, "powers do not tie left to right")
lv.expect(L, "screens[8].prose", "Ties go left to right, except powers: `2 ** 3 ** 2` is `2 ** 9`.")
lv.expect(L, "summary.formula.note", "Ties go left to right, except powers.")
chop_is_floor = (-7 // 2) == int(-7 / 2)
two(chop_is_floor, False, "-7 // 2 is -4 but int(-7 / 2) is -3")
lv.expect(L, "screens[1].explain.text", "So `//` divides and then rounds down to a whole number.")
lv.expect(L, "screens[4].widget.options[2].why", "The double slash rounds down to a whole number.")
lv.expect(L, "quiz[2].feedback.byKey.decimal", "The double slash rounds down to a whole number.")
lv.stated(L, "screens[4].widget.options[2].why", "drops the part after the decimal point", chop_is_floor)
lv.stated(L, "quiz[2].feedback.byKey.decimal", "keeps only the whole part", chop_is_floor)

# ---------- l2-naming-a-value ----------
L = "l2-naming-a-value"
two(run("price = 12\nprint(price * 3)"), "36\n", "price * 3")
lv.expect(L, "screens[0].widget.options[0].text", 36)
two(run("price = 12.5\nqty = 4\nprint(price * qty)"), "50.0\n", "12.5 * 4")
lv.expect(L, "screens[3].explain.text", "50.0")
two(run("cash = 1000\ncash = cash - 3 * 120\nprint(cash)"), f"{1000 - 360}\n", "cash after 3 shares")
lv.expect(L, "screens[7].feedback.correct", 360)
lv.expect(L, "screens[7].feedback.correct", 640)
old_value, new_value = 182.40 * 25, 185.10 * 25
two(run("print(182.40 * 25)"), "4560.0\n", "old position value prints 4560.0")
two(run("print(185.10 * 25)"), "4627.5\n", "new position value prints 4627.5")
lv.expect(L, "screens[9].feedback.byKey.test-1", "4560.0")
lv.expect(L, "screens[9].explain.text", 4560)
lv.expect(L, "screens[9].explain.text", 4627.50)
two(round(new_value - old_value, 2), round(2.70 * 25, 2), "gain on the move")
lv.expect(L, "screens[9].explain.text", 67.50)
two(run("a = 4\nb = a\na = a + 1\nprint(b)"), "4\n", "quiz b stays 4")
two(run("price = 10\nvalue = price * 3\nprice = 11\nprint(value)"), "30\n", "quiz stale value")
lv.expect(L, "quiz[1].widget.options[1].text", 11 * 3)
two(run("x = 2\nx = x * 3\nx = x + 1\nprint(x)"), f"{2 * 3 + 1}\n", "quiz x")
lv.expect(L, "quiz[2].widget.answer", 7)
lv.expect(L, "quiz[2].widget.wrong[1].value", (2 + 1) * 3)

# ---------- l3-text ----------
L = "l3-text"
two(run('print("12" + "5")'), "125\n", '"12" + "5"')
pair = "GBPUSD"
two(pair[0:3], pair[:3], "pair[0:3]")
two(len(pair[0:3]), 3 - 0, "slice length 3")
two(pair[3:6], pair[3:], "pair[3:6]")
two(pair[3], "GBPUSD"[-3], "pair[3]")
two(len("abcdefgh"[2:7]), 7 - 2, "s[2:7] length when s is long enough")
lv.expect(L, "screens[8].widget.options[0].text", 5)
two(run('mon = 37.25\ntue = -8.5\nprint(f"{mon:+.2f}")\nprint(f"{tue:+.2f}")'), "+37.25\n-8.50\n", "signed formats")
two(run('cost = 7\nprint(f"Cost: £{cost:.2f}")'), "Cost: £7.00\n", "quiz cost 7.00")
two(run('print(type("3" * 2))'), "<class 'str'>\n", 'type("3" * 2)')
two("VOD.L"[0:3], "VOD", "quiz ticker slice")
# claims
lv.stated(L, "screens[2].prose", "runs to the end, index 6", len(pair) - 1 == 6)
types_differ_never_equal = not (1 == 1.0) and not (True == 1)
lv.stated(L, "screens[5].hints[1].text", "Different types are not equal", types_differ_never_equal)
lv.stated(L, "screens[5].widget.options[2].why", "When the types differ it answers False", types_differ_never_equal)


def fails(expr):
    try:
        eval(expr)
        return False
    except TypeError:
        return True


only_plus_fails = not fails('"3" - 2') and not fails('"3" * 2.0') and fails('"3" + 2')
lv.stated(L, "quiz[2].explain.text", "Only `+` between a str and a number fails", only_plus_fails)
lv.stated(L, "summary.ideas[1]", "$b - a$ characters", True)  # true while 0 <= a <= b <= len(s); the generalise question needs that (finding)

# ---------- l4-asking-and-printing ----------
L = "l4-asking-and-printing"
TYPED[:] = ["3"]
two(run('qty = input("Shares: ")\nprint(qty * 2)'), "33\n", "input then * 2")
two(run('print(int("250") * 2)'), "500\n", "int then * 2")
lv.expect(L, "screens[2].feedback.byKey.test-1", 250250)
two(run('print(float("12.75") * 4)'), f"{12.75 * 4}\n", "12.75 * 4")
lv.expect(L, "screens[4].feedback.correct", 51)
two(run('print(12.5 * int("8"))'), "100.0\n", "12.5 * 8")
lv.expect(L, "screens[7].question", 100.0)
old, new = 184.20, 189.35
r1 = (new - old) / old
r2 = 5.15 / 184.20
two(round(r1, 5), round(r2, 5), "return 189.35 on 184.20")
lv.expect(L, "screens[9].explain.text", 0.02796, fmt="{:.5f}")
two(run('old = float("184.20")\nnew = float("189.35")\nret = (new - old) / old\nprint(f"Return: {ret * 100:.2f}%")'), "Return: 2.80%\n", "formatted return")
lv.expect(L, "screens[9].explain.text", 5.15)
two(float("4.5%"[0:-1]) / 100, 4.5 / 100, "rate 0.045")
two(round(2000 * float("4.5") / 100, 2), round(2000 * 0.045, 2), "interest 90")
lv.expect(L, "screens[10].question", "£90.00")
two(run('print(int("40") * float("2.5"))'), "100.0\n", "quiz 40 * 2.5")
lv.expect(L, "quiz[1].widget.answer", 100)
lv.expect(L, "quiz[1].widget.wrong[1].value", 40 * 2)

# ---------- review-1 ----------
R = "review"
two(run("print(2 + 6 / 2)"), "5.0\n", "review 2 + 6 / 2")
lv.expect(R, "items[0].widget.options[1].text", (2 + 6) / 2)
two(run("cash = 500\ncost = 120\ncash = cash - cost\ncost = 200\nprint(cash)"), "380\n", "review cash")
lv.expect(R, "items[1].widget.options[1].text", 500 - 200)
two("BARC.L"[0:4], "BARC", "review ticker slice")
two(run('shares = int("12")\nprice = float("3.5")\nprint(f"Cost: £{shares * price:.2f}")'), "Cost: £42.00\n", "review cost")
two(run("print(18 // 5 + 3 ** 2)"), f"{3 + 9}\n", "review 18 // 5 + 3 ** 2")
lv.expect(R, "items[4].widget.wrong[0].value", 4 + 9)
lv.expect(R, "items[4].widget.wrong[1].value", 3 + 3 * 2)
two(run('pnl = -12.5\nprint(f"P&L: {pnl:+.2f}")'), "P&L: -12.50\n", "review signed")
two(float("41.20") * int("150"), 41.2 * 150, "review position value")
lv.expect(R, "items[6].question", "£6180.00")
lv.expect(R, "items[7].widget.options[1].why", "99.51.5")
two(str(99.5) + "1.5", "99.51.5", "str join of price and fee")

# ---------- homework-1 ----------
H = "homework"
two(run("print(-7 // 2)"), "-4\n", "homework -7 // 2")
lv.expect(H, "items[0].widget.options[1].text", int(-7 / 2))
lv.expect(H, "items[0].widget.options[2].text", -7 / 2)
two(run("a = 4\nb = a\nb = b * 3\na = a + b\nprint(a)"), "16\n", "homework trace")
lv.expect(H, "items[1].widget.wrong[0].value", 12 + 12)
lv.expect(H, "items[1].widget.wrong[1].value", 4 + 4)
two(run("print(2 + 18 / 3 ** 2)"), "4.0\n", "homework precedence")
lv.claim(abs((2 + 18) / 9 - 2.2222) <= 0.001, "homework wrong 'bracketed' 2.2222 is (2 + 18) / 9")
lv.expect(H, "items[2].widget.wrong[1].value", (18 / 3) ** 2 + 2)
r = (98.7 - 102.4) / 102.4
two(f"{r * 100:+.2f}", f"{-3.70 / 102.40 * 100:+.2f}", "weekly return")
lv.expect(H, "items[4].question", "-3.61%")
lv.expect(H, "items[4].explain.text", 0.03613, fmt="{:.5f}")
lv.expect(H, "items[4].explain.text", 3.70)
trade = 63.50 * 40
fee = trade * float("0.25") / 100
two(round(fee, 2), round(2540 * 0.0025, 2), "fee")
two(f"{trade + fee:.2f}", "2546.35", "total")
lv.expect(H, "items[5].question", "£6.35")
lv.expect(H, "items[5].question", "£2546.35")
lv.expect(H, "items[5].feedback.byKey.test-1", "£635.00")
lv.expect(H, "items[5].explain.text", "£2,546.35")
two(round(trade * 0.25, 2), 635.0, "fee with 0.25 as the rate")
two(run('price = 63.50\nqty = 40\nfee_text = "0.25%"\nrate = float(fee_text[0:-1]) / 100\ntrade = price * qty\nfee = trade * rate\nprint(f"Fee: £{fee:.2f}")\nprint(f"Total: £{trade + fee:.2f}")'), "Fee: £6.35\nTotal: £2546.35\n", "homework-1 items[5] solution prints")
two(round(63.50 * 40 * 0.0025, 6), 6.35, "homework-1 items[5] test 2 fee")
two(run('date = "2026-10-16"\nprint(date[5:7])'), "10\n", "review-1 items[2] date[5:7]")
two(("2026-10-16"[5:8], "2026-10-16"[4:6]), ("10-", "-1"), "review-1 items[2] wrong options")
lv.expect("review", "items[2].widget.options[0].text", "10")
lv.expect("review", "items[2].widget.options[1].text", "10-")
lv.expect("review", "items[2].widget.options[2].text", "-1")
two(7 - 5, 2, "review-1 items[2] length")
lv.expect("review", "items[2].explain.text", 2)
pnl = (98.20 - 104.50) * 300
two(round(pnl, 2), -6.30 * 300, "round trip P&L")
lv.expect(H, "items[6].question", "-1890.00")
two(f"{(98.2 - 104.5) / 104.5 * 100:+.2f}", "-6.03", "round trip return")
lv.expect(H, "items[6].explain.text", -0.0603)
TYPED[:] = ["50"]
two(run('price = input("Price: ")\nqty = 10\nvalue = price * qty\nprice = 52\navg = 50 + 52 / 2\nprint(value)\nprint(avg)'), "50" * 10 + "\n76.0\n", "longform as written")
TYPED[:] = ["50"]
fixed = run('price = float(input("Price: "))\nqty = 10\nvalue = price * qty\nprice = 52\nvalue = price * qty\navg = (50 + 52) / 2\nprint(value)\nprint(avg)')
lv.expect(H, "items[7].model", "It prints 520 and then 51.0.")
lv.claim(fixed == "520\n51.0\n", f"the fixed longform script prints 520 then 51.0 ({fixed!r})")

lv.check_wrongs()
lv.report()
