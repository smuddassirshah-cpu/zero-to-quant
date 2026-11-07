"""terminal L3 (Setting up to code): every graded key, wrong[] value and stated number, recomputed (second read).
Versions compare as integer tuples; PATH searches walk the folder list; byte counts are len() of the UTF-8 text with
its newline; script outputs come from exec() in CPython (the code items themselves are run separately against every
hidden test, solution and starter, in the review's Tool results)."""
import os, sys, io, contextlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("terminal", 3)
V = lambda s: tuple(int(x) for x in s.replace("Python ", "").split("."))

# --- l9: versions ---
lv.claim(V("3.12.4") >= V("3.10"), "l9 screens[2]: 3.12.4 is at least 3.10")
lv.claim(V("3.12.4") > V("3.9.6") and float("3.9") > float("3.12"), "l9 screens[5]: newer as versions, older-looking as decimals")
lv.stated("l9", "screens[5].hints[2].text", "three releases after 3.9", 12 - 9 == 3)
order = ["Python 3.8.10", "Python 3.9.6", "Python 3.10.14", "Python 3.12.4"]
lv.claim(sorted(order, key=V) == order, "l9 screens[6]: order oldest first")
fleet = ["Python 3.12.4", "Python 3.9.6", "Python 3.10.14", "Python 3.8.10", "Python 3.11.9"]
ok_rows = [f"r{i}c1" for i, v in enumerate(fleet) if V(v) >= (3, 10)]
lv.claim(lv.files["l9-installing-python"]["screens"][10]["widget"]["answer"] == ok_rows, "l9 screens[10]: machines with 3.10 or newer")
lv.expect("l9", "quiz[0].widget.options[0].text", max(["3.10.2", "3.9.18", "3.12.0", "3.11.9"], key=V))
lv.expect("l9", "quiz[1].widget.answer", V("3.11.4")[1])
lv.expect("l9", "quiz[1].widget.wrong[0].value", V("3.11.4")[2])
lv.expect("l9", "quiz[1].widget.wrong[1].value", V("3.11.4")[0])
r3 = {"A": "3.9.20", "B": "3.10.15", "C": "3.11.0", "D": "3.8.19"}
lv.claim([k for k, v in r3.items() if V(v) >= (3, 11)] == ["C"], "review-3 items[0]: only C has 3.11 or newer")
hw = ["Python 3.9.18", "Python 3.10.4", "Python 3.11.0", "Python 3.12.7", "Python 3.13.0"]
lv.claim(sorted(hw, key=V) == hw, "homework-3 items[0]: order oldest first")

# --- l10: bytes, typing ---
b = lambda line: len((line + "\n").encode())
lv.expect("l10", "screens[0].canvas", b('print("hello")'), fmt="{} bytes")
lv.expect("l10", "screens[1].prose", len('print("hello")'))
lv.expect("l10", "quiz[1].widget.answer", b("print(2 + 2)"))
lv.expect("l10", "quiz[1].widget.wrong[0].value", len("print(2 + 2)"))
lv.expect("l10", "quiz[1].widget.wrong[1].value", b("print(2+2)"))           # both spaces skipped, newline kept
lv.stated("l10", "quiz[1].feedback.byKey.no-spaces", "or the newline", len("print(2 + 2)") == 11)
lv.expect("l10", "screens[7].widget.answer", 300 / 20 - 300 / 40)
lv.expect("l10", "screens[7].widget.wrong[0].value", 300 / 20)
lv.expect("l10", "screens[7].widget.wrong[1].value", 40 - 20)
lv.expect("review", "items[1].widget.answer", b('print("hi")'))
lv.expect("review", "items[1].widget.wrong[0].value", len('print("hi")'))
lv.expect("review", "items[1].widget.wrong[1].value", b('print(hi)'))
lv.expect("review", "items[8].widget.answer", 600 / 30 - 600 / 50)
lv.expect("review", "items[8].widget.wrong[0].value", 600 / 30)
lv.expect("review", "items[8].widget.wrong[0].value", 50 - 30)
lv.expect("review", "items[8].widget.wrong[1].value", 600 / 50)

# --- l11: PATH search ---
def search(path, holds, name):
    opened = []
    for d in path:
        opened.append(d)
        if name in holds.get(d, ()):
            return d + "/" + name, opened
    return None, opened
H = {"/usr/local/bin": {"python3"}, "/usr/bin": {"python3"}, "/bin": {"ls"}}
P = ["/usr/local/bin", "/usr/bin", "/bin"]
lv.claim(search(P, H, "ls")[1] == P, "l11 screens[0]: ls opens all three folders")
lv.expect("l11", "screens[2].widget.options[0].text", search(P, H, "python3")[0])
lv.claim(search(["/usr/bin", "/bin"], H, "python3")[0] == "/usr/bin/python3", "l11 screens[8]: the job's PATH finds /usr/bin/python3")
lv.claim(search(P, H, "code")[0] is None, "l11 screens[3]: code is not found")
hb = "/Users/ana/bin" if "/Users/ana/bin" in lv.text("l11", "screens[6]") else "/home/ana/bin"   # review finding: /home becomes /Users
lv.expect("l11", "screens[6].widget.options[0].text", search([hb, "/usr/bin"], {hb: {"report"}, "/usr/bin": {"report"}}, "report")[0])
lv.expect("l11", "quiz[0].widget.options[0].text", search(P, {"/usr/bin": {"jq"}, "/bin": {"jq"}}, "jq")[0])
five = [f"/d{i}" for i in range(1, 6)]
lv.expect("homework", "items[1].widget.answer", len(search(five, {"/d4": {"pytest"}}, "pytest")[1]))
lv.expect("homework", "items[1].widget.wrong[0].value", len(five))
lv.claim(search(["/opt/homebrew/bin", "/usr/bin", "/bin"], {"/opt/homebrew/bin": {"git"}, "/usr/bin": {"git"}}, "git")[0].startswith("/opt/homebrew"), "review-3 items[2]: homebrew git wins")
new = ["/usr/local/bin", "/opt/homebrew/bin", "/usr/bin"]
lv.claim(search(new, {d: {"python3"} for d in new}, "python3")[0] == "/usr/local/bin/python3", "homework-3 items[2]: moving /usr/local/bin first makes it win")

# --- l12: scripts ---
def out(code):
    s = io.StringIO()
    with contextlib.redirect_stdout(s):
        exec(code, {})
    return s.getvalue()
lv.claim(out('print("Ready")\nprint(2 + 3)\n') == "Ready\n5\n", "l12 screens[0]: Ready then 5")
lv.expect("l12", "screens[3].widget.examples[0].expect", out("price = 100.00\nprice = price * 0.98\nprint(price)\n").strip())
lv.claim(out("price = 100.00\nprice = price * 1.04\nprint(price)\n") == "104.0\n", "l12 screens[3]: the starter prints 104.0")
lv.expect("l12", "screens[5].widget.examples[0].expect", out("friday = 262.50\nmonday = 250.00\nprint(friday - monday)\n").strip())
lv.expect("l12", "screens[9].explain.text", 262.50 - 250.00)
lv.expect("l12", "screens[9].explain.text", (262.50 - 250.00) / 250.00)
lv.expect("l12", "screens[9].widget.examples[0].expect", "Return: " + str((262.50 - 250.00) / 250.00))
lv.expect("l12", "quiz[0].widget.answer", float(out("x = 3\nx = x + 2\nprint(x * 10)\n")))
lv.expect("l12", "quiz[0].widget.wrong[0].value", 3 * 10)
lv.expect("l12", "quiz[0].widget.wrong[1].value", 3 * 10 + 2)
lv.expect("l12", "quiz[3].explain.text", "five characters" if len("2 + 3") == 5 else "?")
lv.expect("review", "items[3].widget.answer", float(out("price = 50.00\nprice = price * 2\nprint(price - 25)\n")))
lv.expect("review", "items[3].widget.wrong[0].value", 50 - 25)
lv.expect("review", "items[3].widget.wrong[1].value", 50 * 2)
dr = lambda o, n: (n - o) / o
lv.expect("homework", "items[5].widget.examples[0].expect", f"Day 1: {dr(100.00, 104.00) * 100:.2f}%")
lv.expect("homework", "items[5].widget.examples[0].expect", f"Day 2: {dr(104.00, 101.92) * 100:.2f}%")
for i, (o, n, want) in enumerate([(80.00, 76.00, -0.05), (250.00, 262.50, 0.05), (12.40, 12.71, 0.025), (104.00, 104.00, 0.0)]):
    lv.claim(abs(dr(o, n) - want) < 1e-12, f"homework-3 items[5] hidden test daily_return({o}, {n}) = {want}")
lv.expect("homework", "items[7].widget.answer", 6 * 7 * 10 / 60)
lv.expect("homework", "items[7].widget.wrong[0].value", 6 * 7 * 10)
lv.expect("homework", "items[7].widget.wrong[1].value", 6 * 5 * 10 / 60)

lv.check_wrongs()
lv.report()
