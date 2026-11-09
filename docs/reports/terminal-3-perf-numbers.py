"""terminal level 3 performance task h-perf-trade-script: every number and command checked twice.

Route A runs the item's solution, starter, planted bugs and correct variants the way the Python code
widget does in script mode (a fresh namespace per test: the script, then the postlude; printed holds
the output lines; a call is evaluated there; a stdout match is re.search with re.M).
Route B works the trade in exact fractions, and runs the solution for real with bash in a scratch
home folder: a new shell in HOME, the commands from the script's own comments, then python3.
Run from the repo root: python3 docs/reports/terminal-3-perf-numbers.py
"""
import ast, contextlib, io, json, math, os, re, shutil, subprocess, sys, tempfile
from fractions import Fraction as Fr

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "app", "tools"))
from numbers_lib import Level

lv = Level("terminal", 3)
hw = json.load(open(os.path.join(ROOT, "app/content/courses/terminal/homework-3.json")))
idx = next(i for i, it in enumerate(hw["items"]) if it["id"] == "h-perf-trade-script")
item = hw["items"][idx]
w = item["widget"]
H = f"items[{idx}]"

# ---- shape ----------------------------------------------------------------
lv.claim(item["performance"] == "code" and w["kind"] == "code" and w["language"] == "python", "code performance item in Python")
lv.claim(len(w["tests"]) >= 3 and len(w["tests"]) > len(w.get("examples", [])), f"{len(w['tests'])} tests, {len(w.get('examples', []))} examples")
lv.claim(any(t.get("compare") == "stdout" for t in w["tests"]), "a stdout case puts the widget in script mode")
lv.claim(sum(1 for it in hw["items"] if it.get("performance")) == 1, "one performance item in homework-3")
lv.claim(6 <= len(hw["items"]) <= 12, f"homework-3 has {len(hw['items'])} items (6 to 12)")
lv.claim("parts" not in item and "hints" not in item, "no parts, no hints")
lv.expect("homework", f"{H}.widget.how", len(w["tests"]))           # "Check runs 10 hidden tests"

# ---- route B1: the trade in exact fractions ---------------------------------
shares, buy, sell, fee = 40, Fr("12.25"), Fr("13.00"), Fr("10.00")
cost = shares * buy + fee
proceeds = shares * sell - fee
profit = proceeds - cost
ret = profit / cost
lv.claim((cost, proceeds, profit, ret) == (500, 510, 10, Fr(1, 50)), f"fractions: {cost}, {proceeds}, {profit}, {ret}")
# a second route: total fees once, then the gross gain
gross = shares * (sell - buy)
lv.claim(gross - 2 * fee == profit and gross == 30, "gross gain 30 less two fees of 10 is the profit 10")
for t, v in zip(w["tests"][1:9], [cost, proceeds, profit, ret] * 2):
    lv.claim(Fr(t["expect"]) == v, f"test {t['call']} expects {t['expect']}")
for v in (40, 12.25, 13.00, 10.00):
    lv.expect("homework", f"{H}.prose", v)
lv.expect("homework", f"{H}.explain.text", 500)
lv.expect("homework", f"{H}.explain.text", 510)
lv.expect("homework", f"{H}.explain.text", 10)
lv.expect("homework", f"{H}.explain.text", 0.02)
lv.expect("homework", f"{H}.explain.text", 12.25)
lv.expect("homework", f"{H}.explain.text", "13.00")

# ---- route A: the widget's script-mode harness ------------------------------
def run_case(src, t):
    ns = {"__name__": "__main__", "__learner_source__": src}
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            exec(compile(src, "solution.py", "exec"), ns)
            exec(compile(w["postlude"], "<postlude>", "exec"), ns)
    except Exception:
        return False
    txt = out.getvalue()
    ns["printed"] = txt.splitlines()
    if t.get("compare") == "stdout":
        return bool(re.search(t["match"], txt, re.M))
    try:
        got = eval(t["call"], ns)
    except Exception:
        return False
    if t["compare"] == "isclose":
        return isinstance(got, (int, float)) and not isinstance(got, bool) and math.isclose(got, float(t["expect"]), rel_tol=1e-9, abs_tol=1e-12)
    return got == ast.literal_eval(t["expect"])

def run(src):
    return [run_case(src, t) for t in w["tests"]]

sol = run(w["solution"])
lv.claim(all(sol), f"solution passes {sum(sol)} of {len(sol)}")
st = run(w["starter"])
lv.claim(not any(st), f"starter fails {len(st) - sum(st)} of {len(st)}")

S = w["solution"]
def sub(*pairs):
    s = S
    for a, b in pairs:
        assert a in s, a
        s = s.replace(a, b)
    return s

BUGS = {
    "fees ignored": sub(("shares * buy + fee", "shares * buy"), ("shares * sell - fee", "shares * sell")),
    "fee only on the buy": sub(("shares * sell - fee", "shares * sell")),
    "fee only on the sell": sub(("shares * buy + fee", "shares * buy")),
    "fee taken off the cost": sub(("shares * buy + fee", "shares * buy - fee")),
    "fee added to the proceeds": sub(("shares * sell - fee", "shares * sell + fee")),
    "return on proceeds": sub(("ret = profit / cost", "ret = profit / proceeds")),
    "return on the shares alone": sub(("ret = profit / cost", "ret = profit / (shares * buy)")),
    "return as a percentage": sub(("ret = profit / cost", "ret = profit / cost * 100")),
    "profit the wrong way round": sub(("profit = proceeds - cost", "profit = cost - proceeds")),
    "capital Cost, then cost": sub(("cost = shares", "Cost = shares")),
    "lines out of order": sub(('print("Profit:", profit)\nprint("Return:", ret)', 'print("Return:", ret)\nprint("Profit:", profit)')),
    "Return line unlabelled": sub(('print("Return:", ret)', "print(ret)")),
    "price per share printed as cost": sub(('print("Cost:", cost)', 'print("Cost:", buy)')),
    "no run comments": sub(("# cd ~/desk\n# python3 trade.py\n", "")),
    "python3 from home, no cd": sub(("# cd ~/desk\n", "")),
    "path from home, not from its folder": sub(("# cd ~/desk\n# python3 trade.py", "# python3 desk/trade.py")),
    "python, not python3": sub(("# python3 trade.py", "# python trade.py")),
    "python3 before cd": sub(("# cd ~/desk\n# python3 trade.py", "# python3 trade.py\n# cd ~/desk")),
    "cd from the top, /desk": sub(("# cd ~/desk", "# cd /desk")),
    "cd into the file": sub(("# cd ~/desk", "# cd ~/desk/trade.py")),
    "commands not commented": sub(("# cd ~/desk\n# python3 trade.py", "cd ~/desk\npython3 trade.py")),
}
caught = 0
for name, src in BUGS.items():
    r = run(src)
    caught += not all(r)
    lv.claim(not all(r), f"planted bug fails {len(r) - sum(r)} test(s): {name}")
lv.claim(caught == len(BUGS) >= 3, f"{caught} planted bugs caught")

GOOD = {
    "one line with &&": sub(("# cd ~/desk\n# python3 trade.py", "# Run: cd ~/desk && python3 trade.py")),
    "prompt signs and a full path": sub(("# cd ~/desk\n# python3 trade.py", "# $ cd /home/sam/desk\n# $ python3 ./trade.py")),
    "relative cd": sub(("# cd ~/desk", "# cd desk")),
    "a failed cd first, then the right one": sub(("# cd ~/desk", "# cd into the folder first:\n# cd desk")),
    "two decimals in an f-string": sub(('print("Cost:", cost)', 'print(f"Cost: {cost:.2f}")'), ('print("Return:", ret)', 'print(f"Return: {ret:.2f}")')),
    "whole-number fee and price": sub(("fee = 10.00", "fee = 10"), ("sell = 13.00", "sell = 13")),
    "pound sign before the money": sub(('print("Cost:", cost)', 'print("Cost: £" + str(cost))')),
    "no named shares or fee": "# cd ~/desk\n# python3 trade.py\ncost = 40 * 12.25 + 10\nproceeds = 40 * 13 - 10\nprofit = proceeds - cost\nret = profit / cost\nprint('Cost:', cost)\nprint('Proceeds:', proceeds)\nprint('Profit:', profit)\nprint('Return:', ret)\n",
}
for name, src in GOOD.items():
    r = run(src)
    lv.claim(all(r), f"correct variant passes {sum(r)} of {len(r)}: {name}")

# ---- route B2: run it for real with bash and python3 -------------------------
def comment_cmds(src):
    """The shell commands written in the script's comment lines, as a shell would read them."""
    lines = []
    for l in src.splitlines():
        s = l.strip()
        if s.startswith("#"):
            body = s.lstrip("#").strip()
            body = re.sub(r"^\$\s*", "", body)
            body = re.sub(r"^Run:\s*", "", body)
            if re.match(r"(cd|python3?)\b", body):
                lines.append(body)
    return lines

R = tempfile.mkdtemp(prefix="terminal-3-perf-")
try:
    home = os.path.join(R, "home", "sam")
    os.makedirs(os.path.join(home, "desk"))
    def shell(src, cmds):
        open(os.path.join(home, "desk", "trade.py"), "w").write(src)
        # an absolute /home/sam/... in a command is mapped into the scratch home
        cmds = [c.replace("/home/sam", home) for c in cmds]
        script = "cd \"$HOME\"\n" + "\n".join(cmds) + "\necho \"cwd=$PWD\"\n"
        return subprocess.run(["bash", "-c", script], capture_output=True, text=True, env={"HOME": home, "PATH": os.environ["PATH"]})
    r = shell(S, comment_cmds(S))
    lines = r.stdout.splitlines()
    lv.claim(r.returncode == 0 and lines[:4] == ["Cost: 500.0", "Proceeds: 510.0", "Profit: 10.0", "Return: 0.02"], f"bash: the solution's own comments run it and print {lines[:4]}")
    lv.claim(lines[-1] == f"cwd={home}/desk", "bash: it ran from its own folder")
    for t in w["tests"][5:9]:
        label = t["call"].split("'")[1]
        val = next(float(l.split(":", 1)[1]) for l in lines if l.startswith(label + ":"))
        lv.claim(math.isclose(val, float(t["expect"])), f"bash: printed {label} {val} matches the test")
    for name in ("one line with &&", "prompt signs and a full path", "relative cd"):
        g = GOOD[name]
        rr = shell(g, comment_cmds(g))
        lv.claim(rr.returncode == 0 and rr.stdout.splitlines()[-1] == f"cwd={home}/desk" and "Cost: 500.0" in rr.stdout, f"bash: variant '{name}' runs from the folder")
    # the planted run mistakes, in a real shell
    rr = shell(S, ["python3 trade.py"])
    lv.claim("Errno 2" in rr.stderr and "Cost" not in rr.stdout, "bash: python3 trade.py from /home/sam finds no file")
    rr = shell(S, ["python3 desk/trade.py"])
    lv.claim("Cost: 500.0" in rr.stdout and rr.stdout.splitlines()[-1] == f"cwd={home}", "bash: python3 desk/trade.py runs, but from /home/sam, not its own folder")
    rr = shell(S, ["python3 trade.py", "cd ~/desk"])
    lv.claim("Cost" not in rr.stdout, "bash: python3 before cd finds no file")
    rr = shell(S, ["cd /desk"])
    lv.claim(rr.returncode == 0 and rr.stdout.splitlines()[-1] == f"cwd={home}" and "No such file" in rr.stderr, "bash: cd /desk fails and the shell stays in /home/sam")
    rr = shell(S, ["cd ~/desk/trade.py"])
    lv.claim("Not a directory" in rr.stderr and rr.stdout.splitlines()[-1] == f"cwd={home}", "bash: cd into the file fails and the shell stays put")
    rr = shell(S, ["cd into", "cd desk", "python3 trade.py"])
    lv.claim(rr.stdout.splitlines()[-1] == f"cwd={home}/desk" and "Cost: 500.0" in rr.stdout, "bash: a failed cd leaves the shell where it was, as the postlude assumes")
    rr = shell(S, ["cd"])
    lv.claim(rr.stdout.splitlines()[-1] == f"cwd={home}", "bash: cd alone goes home, as the postlude assumes")
    # the explain's commands
    rr = shell(S, ["cd desk", "python3 trade.py"])
    lv.claim("Return: 0.02" in rr.stdout, "bash: the explain's cd desk then python3 trade.py works")
finally:
    shutil.rmtree(R)

lv.check_wrongs()
lv.report()
