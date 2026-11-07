"""terminal L2 (The terminal): every graded key, wrong[] value and stated number, recomputed (second read).
Paths resolve with posixpath, wildcards with fnmatch (the shell's * does not match a leading dot; no name here has one),
grep as substring search, wc -l as a newline count, ls -t and sort as Python sorts. Each was also run in bash 5.2.21
with GNU coreutils 9.4 (see review-terminal-1-3); this script needs no shell."""
import os, sys, posixpath, fnmatch
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("terminal", 2)
R = lambda cur, rel: posixpath.normpath(posixpath.join(cur, rel.replace("~", "/Users/ana", 1) if rel.startswith("~") else rel))
HOME = "/Users/ana"
TREE = {HOME, HOME + "/Downloads", HOME + "/data", HOME + "/projects", HOME + "/projects/backtest"}

# --- l5: where am I ---
lv.claim(R(HOME + "/projects", "../data") == HOME + "/data", "l5 screens[4]: cd ../data from projects lands in data")
lv.expect("l5", "screens[5].widget.options[0].text", R(HOME + "/data", "~/projects/backtest"))
lv.claim(R(HOME + "/projects/backtest", "../../data") == HOME + "/data", "l5 screens[8]: ../../data from backtest")
lv.claim([t for t in lv.files["l5-where-am-i"]["screens"][8]["widget"]["order"]].count("u1") == 1 and len(lv.files["l5-where-am-i"]["screens"][8]["widget"]["order"]) == 3, "l5 screens[8]: two ../ then data")
lv.claim(R(HOME + "/projects/backtest", "../Downloads") not in TREE, "l5 screens[9] one-up why: ../Downloads from backtest does not exist")
lv.claim(R(HOME + "/projects/backtest", "../../Downloads") == HOME + "/Downloads", "l5 screens[9] explain: ../../Downloads works from backtest")
lv.expect("l5", "quiz[0].widget.options[0].text", R("/", ".."))
lv.expect("l5", "quiz[2].widget.options[0].text", R(HOME + "/projects/backtest", "../.."))
lv.claim(R(HOME + "/data", "../projects") == HOME + "/projects", "review-2 items[0]: ../projects from data")
lv.expect("review", "items[0].widget.options[0].text", R(HOME + "/data", "../projects"))
res = HOME + "/projects/backtest/results"
lv.claim(R(res, "../../../Downloads") == HOME + "/Downloads", "homework-2 items[0]: three ../ from results reach Downloads")

# --- l6: wildcards ---
dl = ["prices.csv", "trades.csv", "prices_2024.csv", "notes.txt", "chart.png", "trades.csv.bak"]
hit = [n for n in dl if fnmatch.fnmatchcase(n, "*.csv")]
lv.claim(len(hit) == 3 and "trades.csv.bak" not in hit, "l6 screens[1], [2]: *.csv matches three names, not trades.csv.bak")
left = [n for n in ["prices.csv", "trades.csv", "notes.txt"] if not fnmatch.fnmatchcase(n, "*.csv")]
lv.expect("l6", "quiz[0].widget.answer", len(left))
lv.expect("l6", "quiz[0].widget.wrong[2].value", 3 - 1)
ex = ["positions_mar.csv", "trades_feb.csv", "trades_jan.csv", "trades_mar.csv", "trades_summary.txt"]
lv.expect("review", "items[1].widget.answer", len(fnmatch.filter(ex, "trades_*.csv")))
lv.expect("review", "items[1].widget.wrong[0].value", len(fnmatch.filter(ex, "trades_*")) )
lv.expect("review", "items[1].widget.wrong[1].value", len(ex))
files = ["prices.csv", "trades.csv", "notes.txt"]     # charts is a folder: rm refuses it
lv.claim(len(fnmatch.filter(files, "*")) == 3, "homework-2 items[3]: a lone * matches all three files")

# --- l7: grep, head, wc, pipes ---
P = ["date,ticker,close", "2024-03-01,AAPL,179.66", "2024-03-01,MSFT,415.50", "2024-03-04,AAPL,175.10",
     "2024-03-04,MSFT,414.92", "2024-03-05,AAPL,170.12", "2024-03-05,MSFT,402.65"]
grep = lambda pat, lines: [l for l in lines if pat in l]
lv.claim(lv.files["l7-looking-inside"]["screens"][0]["widget"]["answer"] == [f"r{i}c0" for i, l in enumerate(P) if "AAPL" in l], "l7 screens[0]: grep AAPL rows")
lv.claim(lv.files["l7-looking-inside"]["screens"][1]["widget"]["answer"] == [f"r{i}c0" for i, l in enumerate(P) if "03-04" in l], "l7 screens[1]: grep 03-04 rows")
lv.expect("l7", "screens[2].widget.answer", min(10, 2517))
lv.expect("l7", "screens[2].widget.wrong[1].value", 10 - 1)
lv.expect("l7", "screens[3].widget.answer", len(P))
lv.expect("l7", "screens[3].widget.wrong[0].value", len(P) - 1)
lv.expect("l7", "screens[3].widget.wrong[1].value", len({l[:10] for l in P[1:]}))
lv.expect("l7", "screens[3].explain.text", len(P) - 1)
lv.expect("l7", "screens[5].widget.answer", len(grep("AAPL", P)))
lv.expect("l7", "screens[5].widget.wrong[1].value", len(grep("AAPL", P)) + 1)
lv.expect("l7", "screens[6].widget.answer", len(grep("MSFT", P)))
lv.expect("l7", "screens[6].widget.wrong[0].value", len(grep("AAPL", P)) + len(grep("MSFT", P)))
lv.expect("l7", "screens[8].widget.answer", 2517 - 1)
lv.claim(abs(2516 / 252 - 10) < 0.1, "l7 screens[8] explain: 2516 days at about 252 a year is close to ten years")
lv.expect("l7", "quiz[1].widget.answer", min(10, len(P)))
# Observed in bash 5.2.21 / dash: `grep AAPL prices.csv > wc -l > count.txt` leaves wc empty (0 bytes) and count.txt
# holding "prices.csv" (the last redirection wins and -l goes to grep). `wc -l | grep AAPL prices.csv > count.txt`
# saves the three AAPL lines while wc waits for keyboard input.
WC_FILE_BYTES, COUNT_TXT = 0, "prices.csv\n"
lv.stated("l7", "screens[7].widget.options[1].why", "The first `>` sends grep's output to a file named wc", WC_FILE_BYTES > 0)
lv.stated("l7", "screens[7].widget.options[3].why", "wc would have nothing to count", False)
lv.expect("l7", "quiz[3].widget.options[0].text", grep("MSFT", grep("2024-03-05", P))[0])
fills = ["time,ticker,side,qty", "09:30,AAPL,buy,100", "09:31,MSFT,sell,50", "09:45,AAPL,sell,100", "10:02,NVDA,buy,20", "10:15,AAPL,buy,40"]
lv.expect("review", "items[2].widget.answer", len(grep("buy", fills)))
lv.expect("review", "items[2].widget.wrong[0].value", len(fills))
lv.expect("review", "items[2].widget.wrong[1].value", len(grep("buy", grep("AAPL", fills))))
lv.expect("review", "items[7].widget.answer", 3 + 3)
lv.expect("homework", "items[2].widget.answer", 0)
short = ["date,ticker,close", "2024-03-01,AAPL,179.66"]
lv.expect("homework", "items[5].widget.answer", sum(len(l.split()) for l in short))
lv.expect("homework", "items[5].widget.wrong[0].value", sum(len(l.split(",")) for l in short))

# --- l8: options ---
lv.claim(4.5 < 48210 / 9120 < 5.5, "l8 screens[0] explain: prices.csv is about five times trades.csv (5.29)")
times = {"notes.txt": (5, 9, 12), "trades_0301.csv": (1, 18, 2), "trades_0304.csv": (4, 18, 5), "trades_0305.csv": (5, 18, 1)}
newest = sorted(times, key=times.get, reverse=True)
lv.expect("l8", "screens[1].explain.text", "trades_0305.csv, then notes.txt")
lv.claim(newest == ["trades_0305.csv", "notes.txt", "trades_0304.csv", "trades_0301.csv"], "l8 screens[1]: ls -t order")
lv.expect("l8", "screens[9].feedback.correct", newest[0])
closes = ["9.85", "100.40", "102.30", "99.10"]
lv.expect("l8", "screens[5].explain.text", ", ".join(sorted(closes, key=float, reverse=True)))
lv.claim(sorted(closes, reverse=True)[0] == "99.10", "l8 screens[5] text-r why: text sort -r puts 99.10 first")
lv.claim(sorted(closes).index("9.85") > sorted(closes).index("102.30"), "l8 screens[5] plain why: 9.85 after 102.30 as text")
lv.expect("l8", "quiz[2].widget.options[0].text", sorted(["2024-03-01", "2024-03-05", "2024-03-04"], reverse=True)[0])
lv.expect("l8", "quiz[3].widget.answer", len([".", "..", ".env", "data", "notes.txt"]))
lv.expect("l8", "quiz[3].widget.wrong[1].value", 3)
ex_t = {"export_a.csv": (3, 18, 4), "export_b.csv": (5, 17, 58), "export_c.csv": (4, 18, 10)}
lv.expect("review", "items[6].widget.options[0].text", max(ex_t, key=ex_t.get))

lv.check_wrongs()
lv.report()
