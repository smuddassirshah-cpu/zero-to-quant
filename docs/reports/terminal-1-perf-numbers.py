"""terminal level 1 performance task h-perf-fx-paths: every path and number checked twice.

Route A runs the item's own prelude, solution, starter and planted bugs the way the Python code
widget does in function mode (prelude, then the code, in one namespace; each test call evaluated
there and compared with its expect literal).
Route B builds the folder tree from the canvas in a real scratch directory and checks every path
with bash (cd, test -f, realpath), so each answer is confirmed on a real, case-sensitive file system.
The tree's top folder / is mapped to a scratch folder R: an absolute path /a/b is checked as R/a/b.
Run from the repo root: python3 docs/reports/terminal-1-perf-numbers.py
"""
import ast, json, os, posixpath, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "app", "tools"))
from numbers_lib import Level

lv = Level("terminal", 1)
hw = json.load(open(os.path.join(ROOT, "app/content/courses/terminal/homework-1.json")))
idx = next(i for i, it in enumerate(hw["items"]) if it["id"] == "h-perf-fx-paths")
item = hw["items"][idx]
w = item["widget"]
H = f"items[{idx}]"

# ---- shape ----------------------------------------------------------------
lv.claim(item["performance"] == "code" and w["kind"] == "code" and w["language"] == "python", "code performance item in Python")
lv.claim(len(w["tests"]) >= 3 and len(w["tests"]) > len(w.get("examples", [])), f"{len(w['tests'])} tests, {len(w.get('examples', []))} examples")
lv.claim(sum(1 for it in hw["items"] if it.get("performance")) == 1, "one performance item in homework-1")
lv.claim(6 <= len(hw["items"]) <= 12, f"homework-1 has {len(hw['items'])} items (6 to 12)")
lv.claim("parts" not in item and "hints" not in item, "no parts, no hints")
lv.expect("homework", f"{H}.widget.how", len(w["tests"]))           # "Check runs 6 hidden tests"
lv.claim(w["how"].count("one per function") == 1, "how says one test per function")
fns = [l.split("def ")[1].split("(")[0] for l in w["starter"].splitlines() if l.startswith("def ")]
lv.claim(len(fns) == len(w["tests"]) == 6, f"{len(fns)} functions, one test each")
lv.stated("homework", f"{H}.question", "six paths", len(fns) == 6)
lv.stated("homework", f"{H}.title", "Six paths", len(fns) == 6)

# ---- route A: the widget's function-mode harness ------------------------------
def run(src):
    ns = {}
    exec(compile(w["prelude"], "<prelude>", "exec"), ns)
    exec(compile(src, "solution.py", "exec"), ns)
    res = []
    for t in w["tests"]:
        try:
            res.append(eval(t["call"], ns) == ast.literal_eval(t["expect"]))
        except Exception:
            res.append(False)
    return res

sol = run(w["solution"])
lv.claim(all(sol), f"solution passes {sum(sol)} of {len(sol)}")
st = run(w["starter"])
lv.claim(not any(st), f"starter fails {len(st) - sum(st)} of {len(st)}")

def swap(fn, value):
    """The solution with one function's returned text replaced."""
    out, skip = [], False
    for line in w["solution"].splitlines():
        if line.startswith(f"def {fn}("):
            out += [line, f"    return {value!r}"]
            skip = True
            continue
        if skip and line.startswith("    return"):
            skip = False
            continue
        out.append(line)
    return "\n".join(out) + "\n"

BUGS = {
    "no leading slash": ("clean_eurusd", "home/priya/fx/clean/eurusd.csv"),
    "raw file, not the clean one": ("clean_eurusd", "/home/priya/fx/Raw/eurusd.csv"),
    "trailing slash": ("clean_eurusd", "/home/priya/fx/clean/eurusd.csv/"),
    "Windows backslashes": ("clean_eurusd", "\\home\\priya\\fx\\clean\\eurusd.csv"),
    "team folder put inside home": ("bank_holidays", "/home/team/holidays.csv"),
    "team folder put inside priya": ("bank_holidays", "/home/priya/team/holidays.csv"),
    "hidden dot dropped": ("settings_file", "/home/priya/config/fx.ini"),
    "hidden folder left out": ("settings_file", "/home/priya/fx.ini"),
    "starts at priya, not the top": ("settings_file", "/priya/.config/fx.ini"),
    "note copied, lower-case raw": ("note_fixed", "/home/priya/fx/raw/gbpusd.csv"),
    "note with home left out": ("note_fixed", "/priya/fx/Raw/gbpusd.csv"),
    ".. ignored": ("tidy_named", "/home/priya/fx/clean/scripts/tidy.py"),
    ".. read as two steps": ("tidy_named", "/home/priya/scripts/tidy.py"),
    "relative path handed back": ("tidy_named", "../scripts/tidy.py"),
    "unresolved .. in the absolute path": ("tidy_named", "/home/priya/fx/clean/../scripts/tidy.py"),
    "one step up, not two": ("settings_from_scripts", "../.config/fx.ini"),
    "no step up": ("settings_from_scripts", ".config/fx.ini"),
    "absolute where relative asked": ("settings_from_scripts", "/home/priya/.config/fx.ini"),
    "two steps, dot dropped": ("settings_from_scripts", "../../config/fx.ini"),
    "home shorthand": ("settings_from_scripts", "~/.config/fx.ini"),
}
for name, (fn, val) in BUGS.items():
    r = run(swap(fn, val))
    lv.claim(not all(r), f"planted bug fails {len(r) - sum(r)} test(s): {name}")
# a correct alternative route is accepted: up three and back down through fx's parent
alt = run(swap("settings_from_scripts", "../../../priya/.config/fx.ini"))
lv.claim(all(alt), "a longer correct relative path also passes")

# ---- route B: the tree on a real file system, checked with bash ---------------
def leaves(nodes, prefix):
    out, dirs = [], []
    for n in nodes:
        p = posixpath.join(prefix, n["label"]) if prefix else n["label"]
        if n.get("children"):
            dirs.append(p)
            a, b = leaves(n["children"], p)
            out += a; dirs += b
        else:
            out.append(p)
    return out, dirs

files, dirs = leaves(item["canvas"]["params"]["nodes"], "")
files = sorted(files)
ns = {}
exec(w["prelude"], ns)
lv.claim(sorted(ns["_FILES"]) == files, "the prelude's file list equals the canvas tree's files")
lv.claim(len(files) == 6, f"the tree holds {len(files)} files")

R = tempfile.mkdtemp(prefix="terminal-1-perf-")
try:
    for d in dirs:
        os.makedirs(R + d, exist_ok=True)
    for f in files:
        open(R + f, "w").write("x\n")

    def sh(cmd):
        return subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)

    sns = {}
    exec(w["solution"], sns)
    for t in w["tests"]:
        args = t["call"][len("_lands("):-1]
        here = ast.literal_eval(args.split(",")[0])
        fn = args.split(",")[1].strip()[:-2]
        kind = ast.literal_eval(args.split(",")[2].strip())
        target = ast.literal_eval(t["expect"])
        path = sns[fn]()
        mapped = (R + path) if kind == "top" else path
        r = sh(f'cd "{R}{here}" && test -f "{mapped}" && realpath "{mapped}"')
        lv.claim(r.returncode == 0 and r.stdout.strip() == R + target, f"bash: {fn} from {here} reaches {target}")
        lv.claim(posixpath.normpath(posixpath.join(here, path)) == target, f"posixpath: {fn} resolves to {target}")
        lv.claim(path.startswith("/") == (kind == "top"), f"{fn}: {'absolute' if kind == 'top' else 'relative'}")
    # every planted bug path names no file on the real tree (or is the wrong kind of path)
    for name, (fn, val) in BUGS.items():
        here = "/home/priya/fx/scripts" if fn == "settings_from_scripts" else "/"
        kind = "rel" if fn == "settings_from_scripts" else "top"
        if "\\" in val or val.startswith("~"):
            ok_shape = True          # not a Linux path to this file at all
        else:
            mapped = (R + val) if val.startswith("/") else val
            r = sh(f'cd "{R}{here}" && realpath -e "{mapped}"')
            right = {"clean_eurusd": "/home/priya/fx/clean/eurusd.csv", "bank_holidays": "/team/holidays.csv",
                     "settings_file": "/home/priya/.config/fx.ini", "note_fixed": "/home/priya/fx/Raw/gbpusd.csv",
                     "tidy_named": "/home/priya/fx/scripts/tidy.py", "settings_from_scripts": "/home/priya/.config/fx.ini"}[fn]
            reaches = r.returncode == 0 and r.stdout.strip() == R + right and not val.endswith("/")
            wrong_kind = val.startswith("/") != (kind == "top") or (kind == "top" and ".." in val.split("/"))
            ok_shape = (not reaches) or wrong_kind
        lv.claim(ok_shape, f"bash: planted '{name}' does not reach the file as asked")
    # the prose facts the starter and explain state
    r = sh(f'test -f "{R}/home/priya/fx/raw/gbpusd.csv"')
    lv.claim(r.returncode != 0, "bash: Tom's lower-case path fails on a case-sensitive file system")
    r = sh(f'cd "{R}/home/priya/fx/clean/.." && pwd')
    lv.claim(r.stdout.strip() == R + "/home/priya/fx", "bash: from clean, .. leads to fx")
    r = sh(f'cd "{R}/home/priya/fx/scripts/../.." && pwd')
    lv.claim(r.stdout.strip() == R + "/home/priya", "bash: from scripts, two steps up reach priya")
    r = sh(f'ls "{R}/home/priya"')
    lv.claim(r.stdout.split() == ["fx"], "bash: plain ls hides .config, so the tree shows it on purpose")
    r = sh(f'ls -a "{R}/home/priya"')
    lv.claim(".config" in r.stdout.split(), "bash: ls -a shows .config")
finally:
    shutil.rmtree(R)

for s in ["`/`", "`.config`", "`Raw`", "`../scripts/tidy.py`", "`/home/priya/fx/scripts/tidy.py`", "`../../.config/fx.ini`", "`fx`", "`priya`"]:
    lv.stated("homework", f"{H}.explain.text", s, True)
lv.stated("homework", f"{H}.prose", "hidden ones included", ".config" in [posixpath.basename(d) for d in dirs])

lv.check_wrongs()
lv.report()
