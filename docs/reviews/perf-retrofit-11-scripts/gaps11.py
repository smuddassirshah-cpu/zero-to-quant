"""Slips the shipped tests do not catch (each names a finding), and the proposed test changes that catch them.
Run with the venv Python: python -I gaps11.py. Exits 0 when every gap and every proposed fix behaves as stated."""
import sys, pathlib, copy
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from harness11 import item, summary, patched

bad = 0
def check(name, ok):
    global bad
    print(("ok   " if ok else "FAIL ") + name)
    bad += 0 if ok else 1

# NP2-1: the ticker column is never read
w = item("numpy-pandas", "homework-2.json", "h-fills-report")["widget"]
slip = patched(w["solution"], ('{"ticker": ticker, "side": side,', '{"side": side,'))
f, _ = summary(w, slip, "NP2-1 slip: no ticker column (shipped tests)")
check("NP2-1 fixed in the item: a frame without ticker fails test 3", f == [3])
w2 = copy.deepcopy(w)
w2["tests"][2]["call"] = '(r["fills"].index.tolist(), r["fills"]["ticker"].tolist())'
w2["tests"][2]["expect"] = '([4, 1, 6, 2, 7, 3, 5], ["BARC", "VOD", "BARC", "SHEL", "VOD", "BARC", "SHEL"])'
f, _ = summary(w2, slip, "NP2-1 slip with the proposed test 3")
check("NP2-1 fix: test 3 catches it", f == [3])
f, _ = summary(w2, w["solution"], "NP2-1 shipped with the proposed test 3", "all")
check("NP2-1 fix: shipped passes", f == [])

# PL3-1: no arrow on the annotation
w = item("plotting", "homework-3.json", "h-price-file-report")["widget"]
slip = patched(w["solution"], (',\n                     arrowprops=dict(arrowstyle="->"))', ')'))
f, _ = summary(w, slip, "PL3-1 slip: label with no arrow (shipped tests)")
check("PL3-1 fixed in the item: a label with no arrow fails test 5", f == [5])
w2 = copy.deepcopy(w)
w2["tests"][4]["call"] = '_arrow(axes[2]) + [next(t for t in axes[2].texts if t.get_text().startswith("Max drawdown")).arrow_patch is not None]'
w2["tests"][4]["expect"] = '["Max drawdown -10.5%", "2026-03-17", -0.104911, True]'
f, _ = summary(w2, slip, "PL3-1 slip with the proposed test 5")
check("PL3-1 fix: test 5 catches it", f == [5])
f, _ = summary(w2, w["solution"], "PL3-1 shipped with the proposed test 5", "all")
check("PL3-1 fix: shipped passes", f == [])
print("failures:", bad)
sys.exit(1 if bad else 0)
