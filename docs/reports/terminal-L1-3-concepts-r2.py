#!/usr/bin/env python3
"""Concept audit, round 2: terminal levels 1 to 3 (audit terminal-1-3-r2).

Runs every command claim of the course in bash (and zsh where the course speaks of zsh or a Mac)
inside a temporary folder, and every Python claim in this interpreter. Reads keys from the content
files, so a changed key is checked against the run, not against a copy typed here.

Exit 0 when every check holds. A check that fails because the content is wrong stays failing.
Usage (repo root):  python docs/reports/terminal-L1-3-concepts-r2.py
Needs bash; zsh checks are skipped (and said so) when zsh is absent. No network, no macOS:
BSD-only wording (the Mac's mkdir, rm and wc messages) is cited in the ledger, not run.
"""
import contextlib, io, json, math, os, posixpath, pty, re, select, shutil, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CDIR = os.path.join(ROOT, "app", "content", "courses", "terminal")
ZSH = shutil.which("zsh")
RES = []


def J(name):
    with open(os.path.join(CDIR, name + ".json"), encoding="utf8") as f:
        return json.load(f)


def check(name, ok, got=""):
    RES.append((name, bool(ok)))
    if not ok:
        print("FAIL", name, "::", str(got)[:300])


def sh(cmd, cwd, shell="bash", env=None):
    e = dict(os.environ, LC_ALL="C")
    e.update(env or {})
    argv = ["bash", "-c", cmd] if shell == "bash" else [ZSH, "-fc", cmd]
    p = subprocess.run(argv, cwd=cwd, env=e, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return p.returncode, p.stdout, p.stderr


def write(path, text=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8") as f:
        f.write(text)


def names(d):
    return sorted(os.listdir(d))


def correct_ids(w):
    return sorted(o["id"] for o in w["options"] if o.get("correct"))


def opt(w, oid):
    return next(o["text"] for o in w["options"] if o["id"] == oid)


PRICES = ("date,ticker,close\n2024-03-01,AAPL,179.66\n2024-03-01,MSFT,415.50\n2024-03-04,AAPL,175.10\n"
          "2024-03-04,MSFT,414.92\n2024-03-05,AAPL,170.12\n2024-03-05,MSFT,402.65\n")


# ---------------------------------------------------------------- level 1
def level1():
    l1 = J("l1-home-row")
    check("l1 s6 200 chars in 1 min = 40 WPM", l1["screens"][6]["widget"]["answer"] == 200 / 5 / 1)
    check("l1 s8 saving 16 min", l1["screens"][8]["widget"]["answer"] == 1800 / 5 / 15 - 1800 / 5 / 45)
    for q, v in (("q-wpm", 275 / 5), ("q-four-min", 600 / 5 / 4)):
        w = next(x for x in l1["quiz"] if x["id"] == q)["widget"]
        check("l1 quiz " + q, w["answer"] == v, w["answer"])
    h1 = J("homework-1")
    check("hw1 notes time 18", h1["items"][0]["widget"]["answer"] == 4500 / 5 / 25 - 4500 / 5 / 50)
    w = h1["items"][0]["widget"]
    slips = {x["id"]: x["value"] for x in w["wrong"]}
    check("hw1 slips 36, 25, 90", slips == {"slow": 4500 / 5 / 25, "diff": 50 - 25, "chars": 4500 / 25 - 4500 / 50}, slips)
    r1 = J("review-1")
    check("review-1 52 WPM", r1["items"][1]["widget"]["answer"] == 520 / 5 / 2)

    # paths: resolve with posixpath, as the kernel does for a tree with no symlinks
    res = lambda here, rel: posixpath.normpath(posixpath.join(here, rel))
    l3 = J("l3-paths")
    check("l3 s6 data/prices.csv from src", res("/home/ana/project/src", "data/prices.csv") == "/home/ana/project/src/data/prices.csv")
    check("l3 s7 key", opt(l3["screens"][7]["widget"], "ok").strip("`") == res("/home/ana", "project/src/backtest.py"))
    check("l3 quiz from notes", res("/home/ana/project/notes", "../data/prices.csv") == "/home/ana/project/data/prices.csv"
          and res("/home/ana/project/notes", "../../data/prices.csv") == "/home/ana/data/prices.csv")
    check("l3 quiz .. of /home/ana is /home", res("/home/ana", "..") == "/home")
    check("review-1 ../../project/data from src", res("/home/ana/project/src", "../../project/data/prices.csv") == "/home/ana/project/data/prices.csv")
    check("review-1 four .. from notes reach /data", res("/home/ana/project/notes", "../../../../data/prices.csv") == "/data/prices.csv"
          and res("/home/ana/project/notes", "../data/prices.csv") != "/data/prices.csv")
    check("hw1 run from home", res("/home/ana", "data/prices.csv") == "/home/ana/data/prices.csv")
    check("POSIX: absolute iff leading /", all(posixpath.isabs(p) for p in ("/", "/data/prices.csv", "/home/ana/project"))
          and not any(posixpath.isabs(p) for p in ("data/prices.csv", "../data/prices.csv", "home/ana", "~/data")))

    # extensions and sorting
    check("l4 extension after the last dot", os.path.splitext("spx.2024.daily.csv")[1] == ".csv"
          and os.path.splitext("trades.2024-06.csv")[1] == ".csv" and os.path.splitext(".prices.csv")[1] == ".csv"
          and os.path.splitext(".env")[1] == "")
    l4 = J("l4-extensions")
    w = l4["screens"][8]["widget"]
    txt = {x["id"]: x["text"].strip("`") for x in w["lines"]}
    check("l4 s8 sorted() order of run files", [txt[i] for i in w["answer"]] == sorted(txt.values()), sorted(txt.values()))
    rows = [r[0] for r in l4["screens"][10]["canvas"]["params"]["rows"]]
    check("l4 s10 table is in name order", rows == sorted(rows))
    iso = ["prices-2024-11-30.csv", "prices-2024-12-31.csv", "prices-2025-01-31.csv", "prices-2025-02-28.csv"]
    check("l4 s10 ISO names sort by date", sorted(iso) == iso)
    check("l4 unpadded month 10 sorts before month 2 and month 3", sorted(["p-2025-2-28", "p-2025-10-31"])[0] == "p-2025-10-31"
          and sorted(["p-2025-3-31", "p-2025-10-31"])[0] == "p-2025-10-31")
    check("l4 month names sort apr, aug, dec, feb", sorted("jan feb mar apr may jun jul aug sep oct nov dec".split())[:4] == ["apr", "aug", "dec", "feb"])
    for item in (r1["items"][7], h1["items"][4]):
        w = item["widget"]
        txt = {x["id"]: x["text"].strip("`") for x in w["lines"]}
        check("sorted() order " + item["id"], [txt[i] for i in w["answer"]] == sorted(txt.values()), sorted(txt.values()))
    with tempfile.TemporaryDirectory() as t:
        t = os.path.realpath(t)
        write(os.path.join(t, "prices.csv"), "x\n")
        try:
            open(os.path.join(t, "Prices.csv")).close()
            cs = False
        except FileNotFoundError:
            cs = True
        check("l4 s9 Linux: Prices.csv is not prices.csv", cs or sys.platform != "linux")
        for n in (".env", ".gitignore", "README.md"):
            write(os.path.join(t, "p", n))
        rc, out, _ = sh("ls; echo --; ls -a", os.path.join(t, "p"))
        a, b = out.split("--\n")
        check("l4 leading dot hides from ls; ls -a shows it", a.split() == ["README.md"] and ".env" in b.split() and ".gitignore" in b.split(), out)

    # homework-1 code widgets: solution passes, starter fails, natural slips fail where the item says
    w = h1["items"][6]["widget"]
    check("hw1 code-paths solution passes", fn_tests(w, w["solution"]) == [])
    check("hw1 code-paths starter fails", fn_tests(w, w["starter"]) != [])
    w = h1["items"][8]["widget"]
    check("hw1 perf solution passes", fn_tests(w, w["solution"]) == [])
    check("hw1 perf starter fails all six", len(fn_tests(w, w["starter"])) == 6)
    bad = w["solution"].replace("/home/priya/fx/Raw/gbpusd.csv", "/home/priya/fx/raw/gbpusd.csv")
    check("hw1 perf lower-case raw fails test 4 only", fn_tests(w, bad) == [4], fn_tests(w, bad))
    bad = w["solution"].replace("../../.config/fx.ini", "../.config/fx.ini")
    check("hw1 perf one .. fails test 6 only", fn_tests(w, bad) == [6], fn_tests(w, bad))


def fn_tests(w, src):
    """Function-mode tests of a code widget in CPython: the 1-based numbers of the failing tests."""
    ns = {}
    try:
        exec(w.get("prelude", ""), ns)
        exec(src, ns)
    except Exception:
        return list(range(1, len(w["tests"]) + 1))
    bad = []
    for i, c in enumerate(w["tests"], 1):
        try:
            got, exp = eval(c["call"], ns), eval(c["expect"], ns)
            ok = math.isclose(got, exp, rel_tol=1e-9, abs_tol=1e-9) if c.get("compare") == "isclose" else got == exp
        except Exception:
            ok = False
        if not ok:
            bad.append(i)
    return bad


def script_tests(w, src):
    """Script-mode tests in CPython (fresh run per case, `printed`, postlude after the run)."""
    bad = []
    for i, c in enumerate(w["tests"], 1):
        ns, buf, ok = {"__name__": "__main__", "__learner_source__": src}, io.StringIO(), True
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(src, "solution.py", "exec"), ns)
        except BaseException:
            ok = False
        out = buf.getvalue()
        norm = lambda s: "\n".join(x.rstrip() for x in s.strip("\n").split("\n"))
        if ok:
            ns["printed"] = out.splitlines()
            try:
                if c.get("compare") == "stdout":
                    ok = bool(re.search(c["match"], out)) if c.get("match") else norm(out) == norm(c["expect"])
                else:
                    exec(w.get("postlude", ""), ns)
                    got, exp = eval(c["call"], ns), eval(c["expect"], ns)
                    ok = (isinstance(got, (int, float)) and math.isclose(got, exp, rel_tol=1e-9, abs_tol=1e-9)) if c.get("compare") == "isclose" else got == exp
            except Exception:
                ok = False
        if not ok:
            bad.append(i)
    return bad


# ---------------------------------------------------------------- level 2
def level2():
    l5, l6, l7, l8 = J("l5-where-am-i"), J("l6-making-things"), J("l7-looking-inside"), J("l8-options-and-help")
    rv, hw = J("review-2"), J("homework-2")
    with tempfile.TemporaryDirectory() as t:
        t = os.path.realpath(t)
        home = os.path.join(t, "Users", "ana")
        for d in ("Downloads", "data", "projects/backtest"):
            os.makedirs(os.path.join(home, d))
        write(os.path.join(home, "notes.txt"), "n\n")
        write(os.path.join(home, "data", "prices.csv"), PRICES)
        E = {"HOME": home}
        rc, out, _ = sh("ls", home)
        check("l5 s2 ls in ana (byte order, as on a Mac)", out.split() == ["Downloads", "data", "notes.txt", "projects"], out)
        rc, out, _ = sh("ls data", home)
        check("l5 s2 ls data prints prices.csv", out.strip() == opt(l5["screens"][2]["widget"], "right").strip("`"))
        rc, out, err = sh("cd projects; echo \"[$?]\"; pwd", home)
        check("l5 s3 cd is silent on success", out == "[0]\n" + home + "/projects\n" and err == "", out + err)
        rc, out, _ = sh("cd ../data && pwd", home + "/projects")
        check("l5 s4 cd ../data", out.strip() == home + "/data")
        rc, out, _ = sh("cd ~/projects/backtest && pwd", home + "/data", env=E)
        check("l5 s5 cd ~/projects/backtest; pwd prints the full path", out.strip() == home + "/projects/backtest")
        rc, out, _ = sh("echo ~/data; echo '~/data'", home, env=E)
        check("l5 the shell swaps an unquoted leading ~", out.split() == [home + "/data", "~/data"], out)
        check("l5 s5 Python does not expand ~; expanduser does",
              subprocess.run([sys.executable, "-c", "import os;print(os.path.exists('~/data'),os.path.exists(os.path.expanduser('~/data')))"],
                             env=dict(os.environ, HOME=home), capture_output=True, text=True).stdout.split() == ["False", "True"])
        for shell in ("bash", "zsh"):
            if shell == "zsh" and not ZSH:
                continue
            rc, out, err = sh("cd data/prices.csv; echo \"[$?]\"; pwd", home, shell)
            check("l5 s6 %s: cd to a file fails, you stay" % shell, out == "[1]\n" + home + "\n" and "ot a directory" in err, out + err)
            if shell == "zsh":
                check("l5 s6 zsh wording 'cd: not a directory: data/prices.csv'", "not a directory: data/prices.csv" in err, err)
        rc, out, err = sh("cd /; cd ..; echo \"[$?]\"; pwd", home)
        check("l5 quiz cd .. at / stays quietly", out == "[0]\n/\n" and err == "", out + err)
        rc, out, _ = sh("cd ../.. && pwd", home + "/projects/backtest")
        check("l5 quiz cd ../..", out.strip() == home)
        rc, out, _ = sh("cd ../../data && pwd; cd ~/data && pwd", home + "/projects/backtest", env=E)
        check("l5 s8 ../../data and ~/data from backtest", out.split() == [home + "/data"] * 2)
        rc1, out1, _ = sh("ls ~/Downloads", home + "/projects/backtest", env=E)
        rc2, _, _ = sh("ls Downloads", home + "/projects/backtest")
        rc3, _, _ = sh("ls ../Downloads", home + "/projects/backtest")
        rc4, _, _ = sh("ls ../../Downloads", home + "/projects/backtest")
        check("l5 s9 only ~/Downloads and ../../Downloads list it", (rc1, rc4) == (0, 0) and rc2 != 0 and rc3 != 0)
        os.makedirs(os.path.join(home, "projects", "backtest", "results"))
        rc, out, _ = sh("cd ../../../Downloads && pwd", home + "/projects/backtest/results")
        check("hw2 ../../../Downloads from results", out.strip() == home + "/Downloads" and len(hw["items"][0]["widget"]["order"]) == 4)

    # l6: files
    with tempfile.TemporaryDirectory() as t:
        t = os.path.realpath(t)
        dl, data = os.path.join(t, "Downloads"), os.path.join(t, "data")
        os.makedirs(dl), os.makedirs(data)
        write(dl + "/prices.csv", "p\n"), write(dl + "/trades.csv", "t\n")
        sh("mv Downloads/prices.csv data/; cp Downloads/trades.csv data/", t)
        check("l6 s0 mv leaves nothing, cp leaves the original", names(dl) == ["trades.csv"] and names(data) == ["prices.csv", "trades.csv"])
        shutil.rmtree(dl), shutil.rmtree(data), os.makedirs(dl), os.makedirs(data)
        rows = [r[0] for r in l6["screens"][1]["canvas"]["params"]["rows"]]
        for n in rows + [".hidden.csv"]:
            write(os.path.join(dl, n))
        key = sorted(rows[int(re.match(r"r(\d+)c0", a).group(1))] for a in l6["screens"][1]["widget"]["answer"])
        rc, out, _ = sh("ls *.csv", dl)
        check("l6 s1 ls *.csv lists the keyed names, no .bak, no hidden", sorted(out.split()) == key, out)
        if ZSH:
            rc, out, _ = sh("echo *.csv", dl, "zsh")
            check("l6 s1 zsh agrees", sorted(out.split()) == key, out)
        sh("mv *.csv ../data/", dl)
        check("l6 s2 mv *.csv moves exactly those", names(data) == key and names(dl) == sorted(set(rows) - set(key) | {".hidden.csv"}), names(dl))
        rc, out, err = sh("mv prices.csv prices_old.csv; ls", data)
        check("l6 s3 mv renames", out.split() == ["prices_2024.csv", "prices_old.csv", "trades.csv"] and err == "", out + err)
        write(data + "/a", "A\n"), write(data + "/b", "B\n")
        rc, out, err = sh("mv a b </dev/null; cat b", data)
        check("l6 s3 mv replaces an existing file without asking", out == "A\n" and err == "", out + err)
        rc, out, err = sh("mkdir data; echo \"[$?]\"", t)
        check("l6 s4 mkdir on an existing folder refuses", "[1]" in out and "File exists" in err and "prices_old.csv" in names(data), err)
        rc, out, err = sh("rm data; echo \"[$?]\"", t)
        check("l6 s5 plain rm refuses a folder", "[1]" in out and "s a directory" in err and os.path.isdir(data), err)
        rc, out, err = sh("mv data", t)
        check("l6 quiz mv with one name is an error", rc != 0 and os.path.isdir(data))
        rc, out, err = sh("cp Downloads/notes.txt nodir/", t)
        check("l6 s8 cp into a missing folder stops with an error", rc != 0 and not os.path.exists(t + "/nodir"), err)
        os.makedirs(t + "/p/q"), write(t + "/p/q/report.csv")
        sh("mv report.csv ..", t + "/p/q")
        check("l6 quiz mv report.csv .. moves it up", os.path.exists(t + "/p/report.csv") and not os.path.exists(t + "/p/q/report.csv"))
        write(t + "/c/prices.csv", "x\n")
        rc, out, _ = sh("cp prices.csv backup.csv; ls", t + "/c")
        check("l6 quiz cp makes a second file", out.split() == ["backup.csv", "prices.csv"])
        for n in ("prices.csv", "trades.csv", "notes.txt"):
            write(os.path.join(t, "r", n))
        sh("rm *.csv", t + "/r")
        check("l6 quiz rm *.csv leaves one file", len(names(t + "/r")) == next(x for x in l6["quiz"] if x["id"] == "q-rm-star")["widget"]["answer"])
        h = os.path.join(t, "ana")
        write(h + "/data/prices.csv"), write(h + "/data/trades.csv"), write(h + "/projects/data/old.csv")
        sh("rm -r data", h)
        check("l6 s6 rm -r data from home removes ~/data, not projects/data", not os.path.exists(h + "/data") and os.path.exists(h + "/projects/data/old.csv"))

    # l7, l8, review-2, homework-2: reading and options
    with tempfile.TemporaryDirectory() as t:
        t = os.path.realpath(t)
        write(t + "/prices.csv", PRICES)
        rowsof = lambda ans: [PRICES.splitlines()[int(re.match(r"r(\d+)c0", a).group(1))] for a in sorted(ans)]
        rc, out, _ = sh("grep AAPL prices.csv", t)
        check("l7 s0 grep AAPL", out.splitlines() == rowsof(l7["screens"][0]["widget"]["answer"]), out)
        rc, out, _ = sh("grep 03-04 prices.csv", t)
        check("l7 s1 grep 03-04", out.splitlines() == rowsof(l7["screens"][1]["widget"]["answer"]), out)
        write(t + "/spx.csv", "date,close\n" + "2014-01-02,1831.98\n" * 2516)
        rc, out, _ = sh("head spx.csv | wc -l; wc -l spx.csv; cat spx.csv | wc -l", t)
        v = out.split()
        check("l7 s2 head prints 10 lines", int(v[0]) == l7["screens"][2]["widget"]["answer"], out)
        check("l7 s8 2517 lines, 2516 days, about ten years at 252", int(v[1]) == 2517 and l7["screens"][8]["widget"]["answer"] == 2516 and abs(2516 / 252 - 10) < 0.05)
        rc, out, _ = sh("wc -l prices.csv", t)
        check("l7 s3 GNU wc -l prints '7 prices.csv'", out == "%d prices.csv\n" % l7["screens"][3]["widget"]["answer"], out)
        rc, out, err = sh("grep AAPL prices.csv > aapl.csv; cat aapl.csv", t)
        check("l7 s4 > writes grep's lines to the file", out.splitlines() == rowsof(l7["screens"][4]["widget"]["answer"]))
        rc, out, err = sh("grep AAPL prices.csv > x.csv", t)
        check("l7 s4 nothing appears on screen", out == "" and err == "")
        rc, out, _ = sh("grep AAPL prices.csv | wc -l", t)
        check("l7 s5 pipeline prints 3", int(out) == l7["screens"][5]["widget"]["answer"])
        rc, out, _ = sh("grep AAPL prices.csv > picks.csv; grep MSFT prices.csv > picks.csv; wc -l < picks.csv; grep -c MSFT picks.csv", t)
        check("l7 s6 second > wipes the first: 3 MSFT lines", out.split() == [str(l7["screens"][6]["widget"]["answer"]), "3"], out)
        w = l7["screens"][7]["widget"]
        rc, out, _ = sh(opt(w, "right").strip("`") + "; cat count.txt", t)
        check("l7 s7 key saves the count 3", out.strip() == "3", out)
        os.remove(t + "/count.txt")
        rc, out, _ = sh(opt(w, "two-gt").strip("`") + "; wc -c < wc; cat count.txt", t)
        check("l7 s7 '> wc -l >' makes an empty file wc and hands -l to grep", out.split() == ["0", "prices.csv"], out)
        os.remove(t + "/wc")
        rc, out, err = sh(opt(w, "pipe-file").strip("`"), t)
        check("l7 s7 piping into a file name: command not found", rc == 127 and "command not found" in err, err)
        rc, out, _ = sh(opt(w, "reversed").strip("`").replace("wc -l |", "wc -l </dev/null |") + "; cat count.txt", t)
        check("l7 s7 reversed saves the AAPL lines, not a count", out.count("AAPL") == 3, out)
        rc, out, err = sh("grep aapl prices.csv; echo \"[$?]\"", t)
        check("l7 quiz grep is case-sensitive, no error message", out == "[1]\n" and err == "", out + err)
        rc, out, _ = sh("grep 2024-03-05 prices.csv | grep MSFT", t)
        check("l7 quiz two greps", out.strip() == opt(next(x for x in l7["quiz"] if x["id"] == "q-two-greps")["widget"], "right").strip("`"))
        rc, out, _ = sh("head prices.csv | wc -l", t)
        check("l7 quiz head of a 7-line file prints 7", int(out) == 7)
        rc, out, _ = sh("head -n 3 prices.csv; echo --; head -1 prices.csv; echo --; head -n 1 prices.csv", t)
        a, b, c = out.split("--\n")
        check("l8 s3 head -n 3", a.splitlines() == rowsof(l8["screens"][3]["widget"]["answer"]))
        check("l8 s9 head -1 is head -n 1", b == c == "date,ticker,close\n")
        rc, out, _ = sh("grep -i aapl prices.csv | wc -l", t)
        check("l8 quiz grep -i", int(out) == 3)
        ex = t + "/ex"
        stamps = {"notes.txt": "2024-03-05 09:12", "trades_0301.csv": "2024-03-01 18:02", "trades_0304.csv": "2024-03-04 18:05", "trades_0305.csv": "2024-03-05 18:01"}
        for n, s in stamps.items():
            write(ex + "/" + n)
            m = time.mktime(time.strptime(s, "%Y-%m-%d %H:%M"))
            os.utime(ex + "/" + n, (m, m))
        rows = [r[0] for r in l8["screens"][1]["canvas"]["params"]["rows"]]
        rc, out, _ = sh("ls -t", ex)
        check("l8 s1 ls -t newest first", out.split()[0] == rows[int(l8["screens"][1]["widget"]["answer"][0][1])]
              and out.split() == ["trades_0305.csv", "notes.txt", "trades_0304.csv", "trades_0301.csv"], out)
        outs = [sh(c, ex)[1] for c in ("ls -l -t", "ls -lt", "ls -tl", "ls -t -l")]
        check("l8 s4 -lt, -tl, -t -l equal -l -t", len(set(outs)) == 1 and outs[0].count("\n") == 5)
        rc1, _, e1 = sh("ls lt", ex)
        rc2, _, e2 = sh("ls -l-t", ex)
        check("l8 s4 'ls lt' looks for a file; 'ls -l-t' is an unknown option", rc1 != 0 and "lt" in e1 and rc2 != 0 and "option" in e2, e1 + e2)
        rc, out, _ = sh("ls -t | head -1; ls -t -r | head -1", ex)
        check("l8 s9 ls -t | head -1 prints the newest; -r the oldest", out.split() == ["trades_0305.csv", "trades_0301.csv"], out)
        rc, out, _ = sh("ls -t > head -1; cat head", ex)
        check("l8 s9 '>' would write the list into a file named head", "trades_0305.csv" in out and os.path.exists(ex + "/head"))
        write(t + "/closes.txt", "9.85\n100.40\n102.30\n99.10\n")
        g = lambda c: sh(c, t)[1].split()
        check("l8 s5 sort -n -r largest first", g("sort -n -r closes.txt") == ["102.30", "100.40", "99.10", "9.85"])
        check("l8 s5 sort -r as text: 99.10 beats 102.30", g("sort -r closes.txt")[0] == "99.10")
        check("l8 s5 sort -n smallest first", g("sort -n closes.txt")[0] == "9.85")
        check("l8 s5 plain sort: 9.85 after 102.30", g("sort closes.txt").index("9.85") > g("sort closes.txt").index("102.30"))
        write(t + "/dates.txt", "2024-03-01\n2024-03-05\n2024-03-04\n")
        check("l8 quiz sort -r dates | head -1", g("sort -r dates.txt | head -1") == ["2024-03-05"])
        os.makedirs(t + "/ad/data"), write(t + "/ad/.env"), write(t + "/ad/notes.txt")
        rc, out, _ = sh("ls -a | wc -l", t + "/ad")
        check("l8 quiz ls -a prints 5 names", int(out) == next(x for x in l8["quiz"] if x["id"] == "q-ls-a")["widget"]["answer"])
        rc, out, err = sh("grep --everything x prices.csv", t)
        check("l8 quiz a guessed option is an error", rc == 2)
        p = subprocess.run(["bash", "-c", "grep man"], cwd=t, input="a manual\nother\n", capture_output=True, text=True)
        check("l8 quiz 'grep man' reads its input for the text man", p.stdout == "a manual\n")
        rc, out, _ = sh("rm -r old_runs </dev/null; echo \"[$?]\"", (os.makedirs(t + "/o/old_runs/x"), t + "/o")[1])
        check("l8 s6 rm -r deletes the folder and asks nothing", out == "[0]\n" and names(t + "/o") == [])
        # review-2
        bx = t + "/bx"
        for n in ("positions_mar.csv", "trades_jan.csv", "trades_summary.txt", "trades_feb.csv", "trades_mar.csv"):
            write(bx + "/" + n)
        os.makedirs(t + "/dst")
        sh("cp trades_*.csv ../dst/", bx)
        check("review-2 cp trades_*.csv copies 3", len(names(t + "/dst")) == rv["items"][1]["widget"]["answer"])
        write(t + "/fills.csv", "time,ticker,side,qty\n09:30,AAPL,buy,100\n09:31,MSFT,sell,50\n09:45,AAPL,sell,100\n10:02,NVDA,buy,20\n10:15,AAPL,buy,40\n")
        check("review-2 grep buy | wc -l", int(g("grep buy fills.csv | wc -l")[0]) == rv["items"][2]["widget"]["answer"])
        shutil.copy(t + "/prices.csv", t + "/self.csv")
        sh("grep AAPL self.csv > self.csv", t)
        check("review-2 redirect onto the input empties the file", os.path.getsize(t + "/self.csv") == 0)
        check("review-2 >> appends: 6 lines", int(g("grep AAPL prices.csv > all.csv; grep MSFT prices.csv >> all.csv; wc -l < all.csv")[0]) == rv["items"][7]["widget"]["answer"])
        ex2 = t + "/ex2"
        for n, s in {"export_a.csv": "2024-06-03 18:04", "export_b.csv": "2024-06-05 17:58", "export_c.csv": "2024-06-04 18:10"}.items():
            write(ex2 + "/" + n)
            m = time.mktime(time.strptime(s, "%Y-%m-%d %H:%M"))
            os.utime(ex2 + "/" + n, (m, m))
        rc, out, _ = sh("ls -t | head -1", ex2)
        check("review-2 newest export", out.strip() == opt(rv["items"][6]["widget"], "right").strip("`"))
        # homework-2
        shutil.copy(t + "/prices.csv", t + "/s.csv")
        check("hw2 sort onto itself leaves 0 lines", int(g("sort s.csv > s.csv; wc -l < s.csv")[0]) == hw["items"][2]["widget"]["answer"])
        st = t + "/st"
        for n in ("prices.csv", "trades.csv", "notes.txt"):
            write(st + "/" + n)
        os.makedirs(st + "/charts")
        rc, out, err = sh("rm * .csv", st)
        check("hw2 bash 'rm * .csv': files gone, charts stays, .csv reported", names(st) == ["charts"] and "charts" in err and ".csv" in err and rc != 0, err)
        if ZSH:
            rc, out, _ = sh("[[ -o rmstarsilent ]] && echo silent || echo asks", t, "zsh")
            check("hw2 zsh default asks before rm * (RM_STAR_SILENT unset)", out.strip() == "asks")
        write(t + "/short.csv", "date,ticker,close\n2024-03-01,AAPL,179.66\n")
        check("hw2 wc -w short.csv is 2", int(g("wc -w < short.csv")[0]) == hw["items"][5]["widget"]["answer"])
        p = subprocess.run(["bash", "-c", "printf 'a\\nb' | wc -l"], capture_output=True, text=True)
        check("hw2 wc -l counts newline characters", int(p.stdout) == 1)
        w = hw["items"][4]["widget"]
        check("hw2 wc_l solution passes, starter fails", fn_tests(w, w["solution"]) == [] and fn_tests(w, w["starter"]) != [])
        for nm, body in (("splitlines", "len(text.splitlines())"), ("plus one", 'text.count("\\n") + 1'), ("split", 'len(text.split("\\n"))')):
            check("hw2 wc_l wrong program fails: " + nm, fn_tests(w, "def wc_l(text):\n    return " + body + "\n") != [])
        write(t + "/all_prices.csv", "date,ticker,close\n2024-03-01,NVDA,1\n2024-03-01,AAPL,2\n2024-03-04,NVDA,3\n")
        lines = {x["id"]: x["text"].strip("`") for x in hw["items"][1]["widget"]["lines"]}
        rc, out, _ = sh("; ".join(lines[i] for i in hw["items"][1]["widget"]["answer"]) + "; cat nvda.csv", t)
        check("hw2 keep-header order gives header + NVDA rows, one more line than NVDA days", out.split()[0] == "3" and out.splitlines()[1] == "date,ticker,close", out)
    tab_checks()


def pty_session(argv, cwd, steps):
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(cwd)
        os.execvpe(argv[0], argv, dict(os.environ, TERM="dumb", PS1="P> ", HOME=cwd))
    def read(t):
        buf, end = b"", time.time() + t
        while time.time() < end:
            if select.select([fd], [], [], 0.1)[0]:
                try:
                    buf += os.read(fd, 4096)
                except OSError:
                    break
        return re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", buf.decode("utf8", "replace")).replace("\r", "")
    read(1.5)
    out = []
    for s in steps:
        os.write(fd, s.encode())
        out.append(read(0.8))
    with contextlib.suppress(OSError):
        os.write(fd, b"\x03\x04")
        os.close(fd)
    with contextlib.suppress(OSError):
        os.waitpid(pid, 0)
    return out


def tab_checks():
    shells = {"bash": ["bash", "--norc", "--noprofile", "-i"]}
    if ZSH:
        shells["zsh"] = [ZSH, "-f", "-i"]
    with tempfile.TemporaryDirectory() as t:
        t = os.path.realpath(t)
        for n in ("ana/Downloads", "ana/data", "ana/projects/backtest", "two", "nopre"):
            os.makedirs(os.path.join(t, n))
        write(t + "/ana/notes.txt"), write(t + "/two/data.csv"), write(t + "/two/data_old.csv"), write(t + "/nopre/da1.csv"), write(t + "/nopre/dab.csv")
        for name, argv in shells.items():
            o = pty_session(argv, t + "/ana", ["cd pro", "\t"])
            check("l5 s7 %s: 'cd pro' + Tab gives 'cd projects/'" % name, (o[0] + o[1]).endswith("cd projects/"), o)
            o = pty_session(argv, t + "/two", ["head da", "\t", "\t", "\t"])
            line = (o[0] + o[1]).replace("\x07", "")
            check("review-2 %s: one Tab fills the shared part 'head data' and lists nothing" % name, line.endswith("head data") and "data_old.csv" not in o[1], o)
            later = o[2] if name == "zsh" else o[3]
            check("review-2 %s: the list comes on the %s Tab after that" % (name, "next" if name == "zsh" else "second"),
                  "data_old.csv" in later and (name == "zsh" or "data_old.csv" not in o[2]), o)
            o = pty_session(argv, t + "/nopre", ["head da", "\t", "\t"])
            first = "dab.csv" in o[1]
            check("l5 s7 %s: nothing to fill, list %s" % (name, "at once" if name == "zsh" else "on the second press"),
                  first if name == "zsh" else (not first and "dab.csv" in o[2]), o)


# ---------------------------------------------------------------- level 3
def vt(s):
    return tuple(int(x) for x in re.search(r"(\d+(?:\.\d+)+)", s).group(1).split("."))


def run_py(src, cwd, name="s.py", args=()):
    write(os.path.join(cwd, name), src)
    p = subprocess.run([sys.executable, name, *args], cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def level3():
    l9, l10, l11, l12 = J("l9-installing-python"), J("l10-code-editor"), J("l11-command-not-found"), J("l12-first-script")
    rv, hw = J("review-3"), J("homework-3")
    # versions compare part by part as whole numbers
    for src, w in (("l9 s6", l9["screens"][6]["widget"]), ("hw3 sort", hw["items"][0]["widget"])):
        txt = {x["id"]: x["text"] for x in w["lines"]}
        check(src + " version order", [txt[i] for i in w["answer"]] == sorted(txt.values(), key=vt))
    rows = l9["screens"][10]["canvas"]["params"]["rows"]
    key = sorted(int(a[1]) for a in l9["screens"][10]["widget"]["answer"])
    check("l9 s10 machines with 3.10 or newer", key == [i for i, r in enumerate(rows) if vt(r[1]) >= (3, 10)])
    check("l9 version facts", vt("3.12.4") > vt("3.9.6") and float("3.9") > float("3.12") and vt("3.11.9")[2] - vt("3.11.2")[2] == 7
          and max(["3.10.2", "3.9.18", "3.12.0", "3.11.9"], key=vt) == "3.12.0")
    rr = rv["items"][0]["canvas"]["params"]["rows"]
    check("review-3 only C has 3.11 or newer", [r[0] for r in rr if vt(r[1]) >= (3, 11)] == ["C"] and correct_ids(rv["items"][0]["widget"]) == ["c"])
    # plain text and bytes
    check("l10 bytes: hello 15, total.py 13, hi.py 12", len('print("hello")\n'.encode()) == 15
          and len("print(2 + 2)\n".encode()) == next(x for x in l10["quiz"] if x["id"] == "q-bytes")["widget"]["answer"]
          and len('print("hi")\n'.encode()) == rv["items"][1]["widget"]["answer"])
    check("l10 s7 typing 7.5 min; review-3 8 min; hw3 7 hours", l10["screens"][7]["widget"]["answer"] == 300 / 20 - 300 / 40
          and rv["items"][8]["widget"]["answer"] == 600 / 30 - 600 / 50 and hw["items"][7]["widget"]["answer"] == 6 * 7 * 10 / 60)
    with tempfile.TemporaryDirectory() as t:
        t = os.path.realpath(t)
        rc, out, err = run_py('print("hello")\n', t, "hello.txt")
        check("l10 s4 python runs a .txt file", out == "hello\n" and rc == 0)
        rc, out, err = run_py("print(“hello”)\n", t, "curly.py")
        check("l10 s3 curly quote: SyntaxError invalid character (U+201C)", "SyntaxError: invalid character '“' (U+201C)" in err, err)
        p = subprocess.run([sys.executable, "backtest.py"], cwd=t, capture_output=True, text=True)
        check("l10 s6 can't open file '<cwd>/backtest.py': [Errno 2]", "can't open file '%s/backtest.py': [Errno 2] No such file or directory" % t in p.stderr, p.stderr)
        p = subprocess.run([sys.executable, "install", "requests"], cwd=t, capture_output=True, text=True)
        check("l9 quiz 'python3 install requests' looks for a file called install", "can't open file" in p.stderr and "install'" in p.stderr)
        os.makedirs(t + "/project/src"), write(t + "/project/data/prices.csv", "x\n")
        src = "print(open('data/prices.csv').read().strip())\n"
        write(t + "/project/src/backtest.py", src)
        a = subprocess.run([sys.executable, "src/backtest.py"], cwd=t + "/project", capture_output=True, text=True)
        b = subprocess.run([sys.executable, "backtest.py"], cwd=t + "/project/src", capture_output=True, text=True)
        check("hw3/hw1/l3 a script's relative path is read from the current folder, not the script's", a.stdout == "x\n" and "FileNotFoundError: [Errno 2] No such file or directory: 'data/prices.csv'" in b.stderr, b.stderr)
        # l12
        rc, out, _ = run_py('print("Ready")\nprint(2 + 3)\n', t)
        check("l12 s0 prints Ready then 5", out == "Ready\n5\n")
        rc, out, _ = run_py('print("2 + 3")\n', t)
        check("l12 quiz quoted sum prints as text", out == "2 + 3\n")
        rc, out, _ = run_py("x = 3\nx = x + 2\nprint(x * 10)\n", t)
        check("l12 quiz reassign prints 50", float(out) == next(x for x in l12["quiz"] if x["id"] == "q-reassign")["widget"]["answer"])
        rc, out, _ = run_py("price = 50.00\nprice = price * 2\nprint(price - 25)\n", t)
        check("review-3 predict prints 75.0", out == "75.0\n" and rv["items"][3]["widget"]["answer"] == 75)
        rc, out, err = run_py(l12["screens"][5]["widget"]["starter"], t, "week.py")
        want = [r[0] for r in l12["screens"][4]["canvas"]["params"]["rows"]]
        el = [x.strip() for x in err.splitlines()]
        check("l12 s4 traceback: File line 3, code line, NameError with suggestion", el[0] == want[0] and el[1].endswith('week.py", line 3, in <module>')
              and el[2] == want[2] and el[-1] == want[4], err)
        rc, out, err = run_py("old = 0.00\nnew = 104.00\nret = (new - old) / old\nprint(ret)\n", t, "ret.py")
        check("l12 s6 ZeroDivisionError on line 3 (wording 'float division by zero' up to 3.13)", "line 3" in err and "ZeroDivisionError" in err
              and ("float division by zero" in err or sys.version_info >= (3, 14)), err)
        rc, out, err = run_py('start = "250.00"\nclose = 262.50\n\ngain = (close - start) / start\n', t, "gain.py")
        check("review-3 TypeError float minus str on line 4", "line 4" in err and "TypeError: unsupported operand type(s) for -: 'float' and 'str'" in err, err)
        rc, out, err = run_py("average = 1.0\nclose = 2.0\n" + "\n" * 6 + "gap = close - avrage\n", t, "signal.py")
        check("hw3 NameError avrage, suggests average, line 9", "line 9" in err and "NameError: name 'avrage' is not defined. Did you mean: 'average'?" in err, err)
        sol = hw["items"][5]["widget"]["solution"].replace("p1 = 104.00", "p1 = 0.00")
        rc, out, err = run_py(sol, t, "returns.py")
        check("hw3 model (d): stops on line 8 inside daily_return, called from line 12; p1 on line 3", "line 12, in <module>" in err and "line 8, in daily_return" in err
              and "ZeroDivisionError" in err and sol.splitlines()[2] == "p1 = 0.00" and out == "", err)
    # code widgets, script mode
    for tag, w in (("l12 s2", l12["screens"][2]["widget"]), ("l12 s3", l12["screens"][3]["widget"]), ("l12 s5", l12["screens"][5]["widget"]),
                   ("l12 s9", l12["screens"][9]["widget"]), ("hw3 returns", hw["items"][5]["widget"]), ("hw3 trade", hw["items"][8]["widget"])):
        check(tag + " solution passes its tests", script_tests(w, w["solution"]) == [], script_tests(w, w["solution"]))
        check(tag + " starter fails", script_tests(w, w["starter"]) != [])
    w = l12["screens"][5]["widget"]
    for m in w.get("mutants", []):
        check("l12 s5 mutant first fails test %d: %s" % (m["test"], m.get("symptom", "")[:30]), (script_tests(w, m["source"]) or [0])[0] == m["test"])
    check("l12 s5 fixing either spelling works", script_tests(w, w["starter"].replace("friday - monday", "Friday - monday")) == [])
    # a wrong program must not pass: a 2% fall is not 'minus 2' (finding 1 while this fails)
    w = l12["screens"][3]["widget"]
    minus2 = w["starter"].replace("* 1.04", "- 2")
    check("l12 s3 hidden tests reject 'price - 2' for a 2% fall", minus2 != w["starter"] and script_tests(w, minus2) != [], "price - 2 passes every test")
    check("l12 s3 tests reject printing the answer without computing it", script_tests(w, w["starter"].replace("print(price)", "print(%s)" % w["tests"][1]["expect"])) != [])
    w = l12["screens"][9]["widget"]
    body = "monday = 250.00\nfriday = 262.50\n"
    check("l12 s9 hard-coded prints fail", script_tests(w, body + 'print("Change: 12.5")\nprint("Return: 0.05")\n') != [])
    check("l12 s9 dividing by Friday fails", script_tests(w, w["solution"].replace("change / monday", "change / friday")) != [])
    check("l12 s9 figures: 12.5 and 0.05 print exactly", repr(262.50 - 250.00) == "12.5" and repr(12.5 / 250.00) == "0.05")
    w = hw["items"][5]["widget"]
    S = w["solution"]
    for nm, rep in (("over new", "(new - old) / new"), ("sign", "(old - new) / old"), ("no brackets", "new - old / old"), ("globals", "(p1 - p0) / p0")):
        check("hw3 returns wrong program fails: " + nm, script_tests(w, S.replace("(new - old) / old", rep)) != [])
    check("hw3 returns: new / old - 1 is the same return and passes", script_tests(w, S.replace("(new - old) / old", "new / old - 1")) == [])
    check("hw3 returns figures", "%.2f" % ((104 - 100) / 100 * 100) == "4.00" and "%.2f" % ((101.92 - 104.00) / 104.00 * 100) == "-2.00")
    w = hw["items"][8]["widget"]
    S = w["solution"]
    check("hw3 trade figures 500, 510, 10, 0.02", (40 * 12.25 + 10, 40 * 13.00 - 10) == (500.0, 510.0) and math.isclose(10 / 500, 0.02))
    for nm, a, b in (("one fee", "shares * sell - fee", "shares * sell"), ("no fees", "+ fee", ""), ("return on proceeds", "profit / cost", "profit / proceeds"),
                     ("no cd", "# cd ~/desk\n", ""), ("python not python3", "# python3 trade.py", "# python trade.py"), ("wrong folder", "cd ~/desk", "cd ~/Desk")):
        check("hw3 trade wrong program fails: " + nm, script_tests(w, S.replace(a, b)) != [])
    for nm, head in (("cd desk", "# cd desk\n# python3 trade.py"), ("&&", "# cd desk && python3 trade.py"), ("absolute cd", "# cd /home/sam/desk\n# python3 trade.py")):
        check("hw3 trade accepts: " + nm, script_tests(w, S.replace("# cd ~/desk\n# python3 trade.py", head)) == [])
    # the report must be true: this comment line does run python3 (finding 3 while this fails)
    one = S.replace("# cd ~/desk\n# python3 trade.py", "# In a new terminal type cd desk then python3 trade.py")
    check("hw3 trade: 'cd desk then python3 trade.py' on one comment line is followed, not reported as 'no comment line runs python3'", script_tests(w, one) == [], script_tests(w, one))

    # PATH: the search, in bash and zsh
    with tempfile.TemporaryDirectory() as t:
        t = os.path.realpath(t)
        for d, word in (("b1", "one"), ("b2", "two")):
            write("%s/%s/prog" % (t, d), "#!/bin/sh\necho %s\n" % word)
            os.chmod("%s/%s/prog" % (t, d), 0o755)
        os.makedirs(t + "/b3")
        P = {"PATH": "%s/b1:%s/b2:/usr/bin:/bin" % (t, t)}
        for shell in ("bash",) + (("zsh",) if ZSH else ()):
            rc, out, _ = sh("prog; %s/b2/prog; cd %s/b2 && prog" % (t, t), t, shell, P)
            check("l11 %s: first PATH folder wins; a / skips the search; the current folder is not searched" % shell, out.split() == ["one", "two", "one"], out)
            rc, out, err = sh("nosuchprog; echo \"[$?]\"", t, shell, P)
            check("l11 %s: command not found" % shell, out == "[127]\n" and "command not found" in err, err)
            rc, out, _ = sh("type cd; type echo", t, shell, P)
            check("l11 %s: cd and echo are built in" % shell, out.count("builtin") == 2, out)
            rc, out, _ = sh("echo $PATH", t, shell, P)
            check("l11 %s: echo $PATH prints the colon-separated list" % shell, out.strip() == P["PATH"])
            rc, out, err = sh("cd %s/b2 && prog" % t, t, shell, {"PATH": "%s/b3:/usr/bin:/bin" % t})
            check("l11 %s: on disk but not on the PATH is 'not found'" % shell, rc == 127, out + err)
            rc, out, err = sh("hello.py", (write(t + "/hello.py", "print(1)\n"), t)[1], shell, P)
            check("l12 quiz %s: a bare 'hello.py' is searched for on the PATH" % shell, rc == 127 and "not found" in err, err)
        if shutil.which("which"):
            rc, out, _ = sh("which prog; echo --; which -a prog", t, "bash", P)
            a, b = out.split("--\n")
            check("l11 s2 which prints the first match; which -a every match in order", a.strip() == t + "/b1/prog" and b.split() == [t + "/b1/prog", t + "/b2/prog"], out)
        # a window reads its PATH settings once, when it opens
        write(t + "/rc", "export PATH=%s/b3:/usr/bin:/bin\n" % t)
        old = subprocess.Popen(["bash", "--noprofile", "--rcfile", t + "/rc", "-i"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, cwd=t)
        old.stdin.write("echo ready\n"), old.stdin.flush(), old.stdout.readline()
        write(t + "/rc", "export PATH=%s/b1:%s/b3:/usr/bin:/bin\n" % (t, t))
        new = subprocess.run(["bash", "--noprofile", "--rcfile", t + "/rc", "-i", "-c", "prog"], capture_output=True, text=True, cwd=t, stdin=subprocess.DEVNULL)
        o, _ = old.communicate("prog 2>&1\n", timeout=20)
        check("l11 s5 the window opened before the change still fails; a new window works", "not found" in o and new.stdout.strip() == "one", o + new.stdout + new.stderr)
        rc, out, _ = sh("python3 --version 2>&1; echo --; /usr/bin/env PATH=/usr/bin:/bin sh -c 'echo $PATH'", t)
        check("l9 python3 --version prints 'Python X.Y.Z'", re.match(r"Python \d+\.\d+\.\d+\n", out) is not None, out)
    w = hw["items"][1]["widget"]
    check("hw3 folders opened: 4", w["answer"] == 4)


level1()
level2()
level3()
bad = [n for n, ok in RES if not ok]
print("terminal L1-3 concepts r2: %d checks, %d failed%s" % (len(RES), len(bad), "" if ZSH else " (zsh absent: zsh checks skipped)"))
sys.exit(1 if bad else 0)
