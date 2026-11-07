"""terminal L1 (Files and folders): every graded key, wrong[] value and stated number, recomputed (second read).
Each number is computed in code, not copied. Path claims are resolved with posixpath; sort claims with sorted(),
which is byte order, as Python and C-locale `ls` use (GNU `ls` in en_GB.UTF-8 differs: see review-terminal-1-3).
Checks that fail because the content is wrong are tied to their wording with stated(): they pass once a fix rewords them."""
import os, sys, posixpath
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("terminal", 1)
wpm = lambda chars, minutes: chars / 5 / minutes

# --- keyboard: finger owning each column of the 10-key grid (1-based columns) ---
ROWS = ["QWERTYUIOP", "ASDFGHJKL;", "ZXCVBNM,./"]
FINGER = {1: "L-little", 2: "L-ring", 3: "L-middle", 4: "L-index", 5: "L-index",
          6: "R-index", 7: "R-index", 8: "R-middle", 9: "R-ring", 10: "R-little"}
cell = lambda r, c: f"r{r}c{c}"
keys_of = lambda finger: sorted(cell(r, c) for r in (1, 2, 3) for c in FINGER if FINGER[c] == finger)
where = {ch: cell(r + 1, c + 1) for r, row in enumerate(ROWS) for c, ch in enumerate(row)}
lv.claim(sorted(lv.files["l1-home-row"]["screens"][2]["widget"]["answer"]) == keys_of("L-middle"), "l1 screens[2] answer = left middle finger keys E D C")
lv.claim(sorted(lv.files["l1-home-row"]["screens"][3]["widget"]["answer"]) == keys_of("L-index"), "l1 screens[3] answer = left index keys R T F G V B")
lv.claim(sorted(lv.files["review-1"]["items"][0]["widget"]["answer"]) == keys_of("R-index"), "review-1 items[0] answer = right index keys Y U H J N M")
ret_index = sorted({where[ch.upper()] for ch in "return" if FINGER[int(where[ch.upper()][3:])].endswith("index")})
lv.claim(sorted(lv.files["homework-1"]["items"][1]["widget"]["answer"]) == ret_index, "homework-1 items[1] answer = index-finger keys of 'return' (R T U N)")
lv.claim(FINGER[int(where["B"][3:])] == "L-index" and FINGER[int(where["T"][3:])] == "L-index", "l1 screens[5], quiz[2]: B and T are left index")
f_pos, j_pos = ROWS[1].index("F") + 1, len(ROWS[1]) - ROWS[1].index("J")
lv.stated("l1", "screens[0].hints[2].text", "the fourth key from each end", f_pos == 4 and j_pos == 4)
fingers_on_letters = len(set(FINGER.values()))   # 8: thumbs only rest on the space bar
keys = sum(len(r) for r in ROWS)
lv.claim("eight fingers cover thirty keys" in lv.text("l1", "screens[3].explain.text") and fingers_on_letters == 8 and keys == 30,
         "l1 screens[3] explain (fixed): eight fingers cover thirty keys, as the screen now says")
lv.claim("ten fingers" not in lv.text("l1", "screens[3].explain.text"), "l1 screens[3] explain: the false 'ten fingers' is gone")

# --- words per minute ---
lv.expect("l1", "screens[6].widget.answer", wpm(200, 1))
lv.expect("l1", "screens[6].widget.wrong[0].value", 200 / 1)
lv.expect("l1", "screens[6].widget.wrong[1].value", 200 * 5)
lv.expect("l1", "screens[7].widget.options[0].text", wpm(450, 3))
lv.expect("l1", "screens[7].widget.options[1].text", 450 / 3)
lv.expect("l1", "screens[7].widget.options[2].text", 450 / 5)
lv.expect("l1", "screens[7].hints[1].text", 450 / 5)
words = 1800 / 5
lv.expect("l1", "screens[8].canvas", words)
lv.expect("l1", "screens[8].explain.canvas.values", words / 15)
lv.expect("l1", "screens[8].explain.canvas.values", words / 45)
lv.expect("l1", "screens[8].widget.answer", words / 15 - words / 45)
lv.expect("l1", "screens[8].explain.text", words / 15)
lv.expect("l1", "screens[8].explain.text", words / 45)
lv.expect("l1", "screens[8].explain.text", words / 15 - words / 45)   # the saving, 16, now stated (validator O2)
lv.expect("l1", "screens[8].widget.wrong[2].value", 45 - 15)
lv.expect("l1", "quiz[1].widget.answer", wpm(275, 1))
lv.expect("l1", "quiz[1].widget.wrong[1].value", 275 * 5)
lv.expect("l1", "quiz[3].widget.answer", wpm(600, 4))
lv.expect("l1", "quiz[3].widget.wrong[0].value", 600 / 4)
lv.expect("l1", "quiz[3].widget.wrong[1].value", 600 / 5)
lv.expect("review", "items[1].widget.answer", wpm(520, 2))
lv.expect("review", "items[1].widget.wrong[0].value", 520 / 2)
lv.expect("review", "items[1].widget.wrong[1].value", 520 / 5)
hw_words = 4500 / 5
lv.expect("homework", "items[0].feedback.correct", hw_words)
lv.expect("homework", "items[0].widget.answer", hw_words / 25 - hw_words / 50)
lv.expect("homework", "items[0].widget.wrong[0].value", hw_words / 25)
lv.expect("homework", "items[0].widget.wrong[1].value", 50 - 25)
lv.expect("homework", "items[0].widget.wrong[2].value", 4500 / 25 - 4500 / 50)   # forgot the 5

# --- folder trees and paths (l2, l3) ---
paths = ["ana/Downloads/prices.csv", "ana/project/data/prices.csv", "ana/project/data/trades.csv"]
lv.expect("l2", "quiz[3].widget.options[0].text", len(set(paths)))
folders_with_csv = len({posixpath.dirname(p) for p in paths})
folders_named = len({c for p in paths for c in p.split("/")[:-1]})
lv.claim(folders_with_csv == 2 and folders_named == 4, "l2 quiz[3]: two folders hold a CSV, four folders appear in the paths")
lv.expect("l2", "quiz[3].widget.options[2].text", folders_named)
lv.claim(lv.files["l2-folder-tree"]["quiz"][3]["widget"]["options"][2]["id"] == "four", "l2 quiz[3]: the slip option is the folder count, 4")
lv.expect("l2", "quiz[3].widget.options[2].why", folders_named and "Downloads")
lv.expect("l2", "quiz[3].explain.text", len(set(paths)))
lv.claim("You counted folders that hold a CSV" not in lv.text("l2", "quiz[3]"), "l2 quiz[3]: the false 'folders that hold a CSV' wording is gone")
lv.expect("l2", "screens[8].explain.text", "project/data/spx-daily.csv")
cwd = "/home/ana/project"
R = lambda cur, rel: posixpath.normpath(posixpath.join(cur, rel))
lv.claim(R(cwd, "data/prices.csv") == "/home/ana/project/data/prices.csv", "l3 screens[3]: data/prices.csv from project")
lv.claim(R(cwd + "/src", "../data/prices.csv") == "/home/ana/project/data/prices.csv", "l3 screens[4]: ../data/prices.csv from src")
lv.claim(R(cwd + "/src", "../../project/data/prices.csv") == "/home/ana/project/data/prices.csv", "review-1 items[4]: ../../project/data/prices.csv from src")
lv.expect("review", "items[4].prose", "../../project/data/prices.csv")
lv.expect("review", "items[4].explain.text", R(cwd + "/src", "../../project/data/prices.csv"))
lv.claim(lv.files["review-1"]["items"][4]["widget"]["answer"] == ["r-h-a-j-d-p"], "review-1 items[4]: answer is the project data file")
lv.claim(posixpath.dirname(paths[0]) == "ana/Downloads" and lv.files["review-1"]["items"][2]["widget"]["answer"] == ["a-dl"], "review-1 items[2]: parent of the prices.csv outside project is Downloads (a-dl)")
lv.expect("review", "items[2].explain.text", "ana/Downloads/prices.csv")
lv.expect("l3", "screens[6].explain.text", R(cwd + "/src", "data/prices.csv"))
lv.expect("l3", "screens[7].widget.options[0].text", R("/home/ana", "project/src/backtest.py"))
lv.expect("l3", "screens[8].explain.text", R(cwd, "data/spx-daily.csv"))
lv.claim(abs(10 * 252 - 2500) / 2520 < 0.01, "l3 screens[8]: ten years of daily closes is about 2,500 rows (10 x 252 = 2520)")
lv.expect("l3", "quiz[1].widget.options[0].text", R(cwd, "src/backtest.py"))
lv.claim(R(cwd + "/notes", "../data/prices.csv") == "/home/ana/project/data/prices.csv", "l3 quiz[2]: ../data/prices.csv from notes")
lv.claim(R(cwd + "/notes", "../../data/prices.csv") == "/home/ana/data/prices.csv", "l3 quiz[2] why: two up lands in /home/ana")
lv.expect("l3", "quiz[3].widget.options[0].text", R("/home/ana", ".."))
lv.claim(R(cwd + "/notes", "../../../../data/prices.csv") == "/data/prices.csv", "review-1 items[5]: four .. from notes reach /data")
lv.claim(R(cwd + "/notes", "../../../data/prices.csv") != "/data/prices.csv", "review-1 items[5]: three .. do not")
lv.claim(R(cwd + "/data", "../src/backtest.py") == "/home/ana/project/src/backtest.py", "homework-1 items[2]: ../src/backtest.py from data")
lv.expect("homework", "items[3].widget.options[0].text", R("/home/ana", "data/prices.csv"))
hw = lv.files["homework-1"]["items"][6]["widget"]
lv.claim([t["expect"] for t in hw["tests"]] == [repr("data/spx-daily.csv"), repr(posixpath.relpath("/home/ana/project/data/spx-daily.csv", cwd + "/src")),
                                               repr(cwd + "/data/spx-daily.csv"), repr(posixpath.relpath(cwd + "/results", cwd + "/src"))],
         "homework-1 items[6]: the four expected path strings")

# --- extensions, hidden files, sorting (l4) ---
sizes = {"prices.csv": 48e3, "backtest.py": 3e3, "chart.png": 120e3, "notes.txt": 2e3, "results.xlsx": 35e3,
         "photo.jpg": 2.1e6, "README.md": 1e3, "report.pdf": 310e3}
rank = sorted(sizes, key=sizes.get, reverse=True)
lv.claim(rank[0] == "photo.jpg" and rank[1] == "report.pdf" and rank[2] == "chart.png", "l4 screens[0]: sizes rank photo.jpg, report.pdf, chart.png")
lv.claim(lv.text("l4", "screens[0].hints[1].text") == "One picture is the largest file here.", "l4 screens[0] hints[1] (fixed): a picture is the largest file")
ext = lambda n: "." + n.rsplit(".", 1)[1]
lv.expect("l4", "screens[5].widget.options[0].text", ext("spx.2024.daily.csv"))
lv.expect("l4", "quiz[0].widget.options[0].text", ext("trades.2024-06.csv"))
runs = ["run-1.csv", "run-10.csv", "run-2.csv", "run-3.csv"]
order = [l["id"] for l in lv.files["l4-extensions"]["screens"][8]["widget"]["lines"]]
lv.claim(sorted(runs) == [f"run-{o[1:]}.csv" for o in lv.files["l4-extensions"]["screens"][8]["widget"]["answer"]], "l4 screens[8]: byte order run-1, run-10, run-2, run-3")
dmy = ["prices-28-02-2025.csv", "prices-30-11-2024.csv", "prices-31-01-2025.csv", "prices-31-12-2024.csv"]
lv.claim([r[0] for r in lv.files["l4-extensions"]["screens"][10]["canvas"]["params"]["rows"]] == sorted(dmy), "l4 screens[10]: table rows are the DMY names in name order")
iso = sorted("prices-" + "-".join(reversed(n[7:17].split("-"))) + ".csv" for n in dmy)
vals = lv.files["l4-extensions"]["screens"][10]["explain"]["canvas"]["values"]
lv.claim([vals[f"r{i}c0"] for i in range(4)] == iso, "l4 screens[10] explain: ISO names sort in date order")
lv.claim(sorted(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])[:4] == ["apr", "aug", "dec", "feb"], "l4 screens[10] words why: apr, aug, dec, feb")
lv.claim("2025-10-31" < "2025-2-28", "l4 screens[10] nopad why: month 10 sorts before month 2")
lv.claim("2025-3-31" > "2025-10-31", "l4 quiz[2] nopad why: month 3 sorts after month 10")
lv.claim(sorted(["prices-2024-02-29.csv", "prices-2024-11-30.csv", "prices-2024-12-31.csv", "prices-2025-01-31.csv"]) ==
         [l["text"].strip("`") for l in lv.files["review-1"]["items"][7]["widget"]["lines"]], "review-1 items[7]: listed order is name order")
pad = {"a": "run-02.csv", "b": "run-1.csv", "c": "run-12.csv", "d": "run-2.csv"}
lv.claim([pad[k] for k in lv.files["homework-1"]["items"][4]["widget"]["answer"]] == sorted(pad.values()), "homework-1 items[4]: sorted() order")

lv.check_wrongs()
lv.report()
