"""game-theory homework-1 hw1-street-carts: shipped solution, starter, a reader solution (Fractions, distance
maps, argmax by sorting) and reader-planted slips, on every example and test. Venv Python, from this folder."""
import sys
from harness import item, run, summary

it = item("game-theory", "homework-1.json", "hw1-street-carts")
w = it["widget"]
bad = 0
READER = r'''
from fractions import Fraction
from collections import Counter

def street_table(homes, ana_spots, ben_spots, a, b):
    cnt = Counter(homes)
    out = []
    for x in ana_spots:
        row = []
        for y in ben_spots:
            sa = sb = Fraction(0)
            for h, k in cnt.items():
                da, db = abs(h - x), abs(h - y)
                share = Fraction(1) if da < db else Fraction(0) if da > db else Fraction(1, 2)
                sa += k * share; sb += k * (1 - share)
            row.append((float(a * sa), float(b * sb)))
        out.append(row)
    return out

def best_replies(table):
    rows, cols = len(table), len(table[0])
    ana = []
    for j in range(cols):
        col = [table[i][j][0] for i in range(rows)]
        ana.append(sorted(i for i, v in enumerate(col) if v == max(col)))
    ben = []
    for i in range(rows):
        row = [c[1] for c in table[i]]
        ben.append(sorted(j for j, v in enumerate(row) if v == max(row)))
    return ana, ben
'''
sol = w["solution"]
def slip(old, new, src=None):
    src = src or sol
    assert old in src, old
    return src.replace(old, new)
SLIPS = {
    "shared spot gives the whole street to Ana": slip("                else:  # equally far, or the carts share a spot\n                    ana += 0.5\n                    ben += 0.5",
        "                elif x == y:\n                    ana += 1\n                else:\n                    ana += 0.5\n                    ben += 0.5"),
    "equidistant home buys nothing": slip("                    ana += 0.5\n                    ben += 0.5", "                    pass"),
    "repeated homes counted once": slip("            for h in homes:", "            for h in set(homes):"),
    "Ana's reply read along a row": slip("top = max(table[i][j][0] for i in range(m))\n        ana.append([i for i in range(m) if table[i][j][0] == top])",
        "top = max(table[j][i][0] for i in range(len(table[j])))\n        ana.append([i for i in range(len(table[j])) if table[j][i][0] == top])"),
    "max starting from 0 (negatives)": slip("top = max(table[i][j][0] for i in range(m))", "top = max([0] + [table[i][j][0] for i in range(m)])"),
    "only the first best reply kept": slip("ana.append([i for i in range(m) if table[i][j][0] == top])", "ana.append([[i for i in range(m) if table[i][j][0] == top][0]])"),
    "both prices a": slip("row.append((a * ana, b * ben))", "row.append((a * ana, a * ben))"),
}
print("hw1-street-carts")
f, _ = summary(w, sol, "shipped solution"); bad += bool(f)
bad += any(x[0] != "pass" for x in run(w, sol, "examples"))
f, _ = summary(w, READER, "reader solution (Fractions, Counter)"); bad += bool(f)
f, _ = summary(w, w["starter"], "starter"); bad += len(f) != len(w["tests"])
for name, src in SLIPS.items():
    f, _ = summary(w, src, "slip: " + name)
    if not f:
        print("     ^ passes every test"); bad += 1
print("bad:", bad)
sys.exit(1 if bad else 0)
