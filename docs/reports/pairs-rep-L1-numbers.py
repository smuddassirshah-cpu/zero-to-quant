"""pairs-rep level 1: recompute every stated number and check it at its JSON path. Exit 0 when all pass."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pairs_rep_common import *  # noqa: F401,F403
from scipy.stats import spearmanr

lv = Level("pairs-rep", 1)
C = CLOSE
P0 = C[:378] / C[0]; F0, T0 = P0[:252], P0[252:]
items0, D0 = ranked(F0)
top20 = [(i, j) for _, i, j in items0[:20]]

# ---- l1
log = []; trade(F0, T0, 2, 3, 0, log=log)
od, cd = 252 + log[0][0], 252 + log[0][1]
gap = P0[od, 2] - P0[od, 3]
sd23 = float(np.std(F0[:, 2] - F0[:, 3])); sdT = float(np.std(T0[:, 2] - T0[:, 3]))
lv.expect("l1", "screens[0].prose", od)
lv.expect("l1", "screens[0].explain.text", round(abs(gap), 3))
lv.expect("l1", "screens[0].explain.text", cd)
lv.expect("l1", "screens[1].widget.answer", sum(1 for m in range(6) if 21 * m + 252 <= 360 <= 21 * m + 377))
lv.expect("l1", "screens[5].prose", round(sd23, 4)); lv.expect("l1", "screens[5].prose", round(2 * sd23, 4)); lv.expect("l1", "screens[5].prose", round(sdT, 4))
lv.expect("l1", "screens[7].widget.answer", 1134 + 252)
lv.expect("l1", "screens[8].widget.answer", 6 * 20)
lv.expect("l1", "quiz[0].widget.options[2].why", round(sdT, 4)); lv.expect("l1", "quiz[0].widget.options[2].why", round(sd23, 4))
lv.expect("l1", "quiz[1].widget.answer", len(range(max(0, 2 - 5), 3)))

# ---- l2
for n in (63, 126, 189, 252):
    lv.expect("l2", "screens[1].canvas.controls", round(float(((F0[:n, 2] - F0[:n, 3]) ** 2).sum()), 4))
    lv.expect("l2", "screens[1].canvas.controls", round(float(((F0[:n, 2] - F0[:n, 50]) ** 2).sum()), 2))
lv.expect("l2", "screens[1].widget.answer", round(D0[2, 3], 4))
ta = np.array([1, 1.02, 1.05, 1.03, 1.06, 1.08]); tb = np.array([1, 1.01, 1.03, 1.05, 1.04, 1.07])
lv.expect("l2", "screens[2].widget.rows[6][4].answer", round(float(((ta - tb) ** 2).sum()), 4))
lv.expect("l2", "screens[2].widget.rows[6][4].wrong[0].value", round(float((ta - tb).sum()), 2))
lv.expect("l2", "screens[2].widget.rows[6][4].wrong[1].value", round(float(np.abs(ta - tb).sum()), 2))
sp = ta - tb
lv.expect("l2", "screens[3].widget.answer", round(float(np.sqrt(((sp - sp.mean()) ** 2).mean())), 4))
lv.expect("l2", "screens[3].widget.wrong[0].value", round(float(np.sqrt(((sp - sp.mean()) ** 2).sum() / 5)), 4))
lv.expect("l2", "screens[3].widget.wrong[1].value", round(float(np.sqrt((sp ** 2).mean())), 4))
lv.expect("l2", "screens[3].explain.text", round(2 * float(np.sqrt(((sp - sp.mean()) ** 2).mean())), 4))
A = np.round(F0[:, 2], 4); A2 = np.round(A * A, 4)
lv.expect("l2", "screens[8].explain.text", round(float(((A - A2) ** 2).sum()), 2))
lv.expect("l2", "screens[5].widget.tests[4].expect", round(D0[2, 3], 4))
lv.expect("l2", "quiz[0].widget.answer", round(0.1 ** 2 + 0.1 ** 2, 4))

# ---- l3
L = np.log10([x[0] for x in items0])
lv.expect("l3", "screens[0].widget.answer", 100 * 99 // 2)
lv.expect("l3", "screens[1].widget.answer", int((L < 0).sum()))
lv.expect("l3", "screens[1].explain.text", round(float(np.median([x[0] for x in items0])), 2))
lv.expect("l3", "screens[1].explain.text", round(items0[19][0], 4)); lv.expect("l3", "screens[1].explain.text", round(items0[20][0], 4))
sh = [0, 1, 2, 3, 40]
for a, b in ((2, 3), (0, 1), (2, 40)):
    lv.expect("l3", "screens[2].canvas.params.rows", round(D0[a, b], 3))
lv.expect("l3", "screens[3].widget.tests[1].expect", str([list(p) for p in top20]))
P1512 = C[1512:1764] / C[1512]
t10 = closest(P1512, 10)
flat = [s for p in t10 for s in p]
dups = sorted(set(s for s in flat if flat.count(s) > 1))
lv.expect("l3", "screens[6].widget.answer", len(dups))
for s_ in dups:
    lv.expect("l3", "screens[6].widget.accept", s_)
t20_1512 = closest(P1512, 20); f20 = [s for p in t20_1512 for s in p]
lv.expect("l3", "screens[6].explain.text", len(set(s for s in f20 if f20.count(s) > 1)))
prof = {}
for _, i, j in items0[:20]:
    prof[(i, j)] = trade(F0, T0, i, j)[0]
rho20 = spearmanr([x[0] for x in items0[:20]], [prof[(i, j)] for _, i, j in items0[:20]]).correlation
lv.expect("l3", "screens[7].explain.text", round(float(rho20), 2))
lv.expect("l3", "screens[7].explain.text", round(max(prof.values()) * 100))
lv.expect("l3", "screens[7].widget.options[0].text", round(float(rho20), 2))
_, i5, j5 = items0[4]
lv._rec(prof[(i5, j5)] == 0.0 and not trade(F0, T0, i5, j5)[1], "l3 fifth closest pair never opens", "")
P2016 = C[2016:2268] / C[2016]
t2016 = closest(P2016, 20)
lv.expect("l3", "screens[8].widget.answer", sum(1 for i, j in t2016 if i % 2 == 0 and j == i + 1 and i < 40))
lv.expect("l3", "screens[9].widget.answer", 500 * 499 // 2)
same8 = sum(1 for i, j in t20_1512[:8] if IND[i] == IND[j])
lv.expect("l3", "screens[10].widget.answer", round(same8 / 8, 3))
lv.expect("l3", "screens[10].explain.text", round(sum(1 for i, j in t20_1512 if IND[i] == IND[j]) / 20, 2))
lv.expect("l3", "screens[5].widget.tests[7].expect", sum(1 for i, j in t20_1512 if IND[i] == IND[j]) / 20)
lv.expect("l3", "quiz[0].widget.answer", 50 * 49 // 2)

# ---- l4
c, e, n, prs, res = cycle(C, 0, 20)
tot = sum(r[0] for r in res)
lv.expect("l4", "screens[0].prose", round(tot, 2))
lv.expect("l4", "screens[0].widget.answer", round(tot / 20, 4)); lv.expect("l4", "screens[0].widget.wrong[0].value", round(tot / n, 4))
lv.expect("l4", "screens[1].explain.text", round(tot / n, 4)); lv.expect("l4", "screens[1].explain.text", round(tot / 20, 4))
lv._rec(n == 19, "l4 first cycle: 19 of 20 opened", "")
runs = {(k, w): run(C, k, w) for k in (5, 20) for w in (0, 1)}
mean = lambda r, col: float(np.mean([x[col] for x in r]))
c6 = [round(mean(runs[(20, 0)], 1) * 100, 2), round(mean(runs[(20, 0)], 2) * 100, 2), round(mean(runs[(20, 1)], 1) * 100, 2), round(mean(runs[(20, 1)], 2) * 100, 2)]
for r, v in enumerate(c6):
    lv.expect("l4", f"screens[2].widget.rows[{r}][1]", v)
    lv.expect("l4", f"screens[2].widget.rows[{r}][2].answer", round(v / 100 / 6, 5))
band = {w: run(C, 20, w, lo=100) for w in (0, 1)}
cells = [(0, [runs[(5, 0)], runs[(5, 0)], runs[(5, 1)], runs[(5, 1)]], 5), (1, [runs[(20, 0)], runs[(20, 0)], runs[(20, 1)], runs[(20, 1)]], 20), (2, [band[0], band[0], band[1], band[1]], 20)]
for row, rs, k in cells:
    for col, r in enumerate(rs):
        lv.expect("l4", f"screens[3].canvas.params.rows[{row}][{col + 1}]", round(mean(r, 1 + col % 2) / 6 * 100, 2))
    lv.expect("l4", f"screens[3].canvas.params.rows[{row}][5]", round(mean(rs[0], 3) / k * 100))
lv.expect("l4", "screens[4].widget.answer", round(1.0075 ** 12 - 1, 4))
lv.expect("l4", "screens[4].prose", round(mean(runs[(20, 1)], 1) / 6 * 100, 2))
lv.expect("l4", "screens[5].prose", round(mean(runs[(20, 1)], 2) / 6 * 100, 2)); lv.expect("l4", "screens[5].prose", round((1.0084 ** 12 - 1) * 100, 1))
lv.expect("l4", "screens[8].widget.answer", round(0.13 / 3, 4)); lv.expect("l4", "screens[8].explain.text", round(0.13 / 5, 3))
lv.expect("l4", "quiz[0].widget.wrong[0].value", round(1.09 ** 12 - 1, 4))
lv._rec(all(x[3] > 0 for k in (5, 20) for w in (0, 1) for x in runs[(k, w)]), "l4 no cycle with zero opened pairs (top 5 and 20)", "")

# ---- l5
lv.expect("l5", "screens[0].canvas.params.lines", round(sdT, 4)); lv.expect("l5", "screens[0].canvas.params.lines", round(prof[(2, 3)], 4))
lv.expect("l5", "screens[0].canvas.params.lines", round(c * 100, 2)); lv.expect("l5", "screens[0].canvas.params.lines", round(e * 100, 2))
lv._rec(sorted(k for k in range(20) if not BROKEN[k]) == [4, 7, 16], "l5 unbroken pairs are 4, 7 and 16", "")
lv.expect("l5", "screens[3].widget.answer", round(0.5 ** (1 / 8), 4))

def placebo(form, tr, k, seed):
    rng = np.random.default_rng(seed); out = []
    for _ in range(k):
        i, j = rng.choice(form.shape[1], 2, replace=False)
        out.append(trade(form, tr, int(i), int(j))[0])
    return float(np.mean(out))
Pm = MID[:378] / MID[0]
lv.expect("l5", "screens[6].widget.tests[0].expect", round(placebo(F0, T0, 20, 0), 6))
lv.expect("l5", "screens[6].widget.tests[2].expect", round(placebo(Pm[:252], Pm[252:], 20, 0), 6))
p200c = float(np.mean([placebo(F0, T0, 20, s) for s in range(200)]))
p200m = float(np.mean([placebo(Pm[:252], Pm[252:], 20, s) for s in range(200)]))
lv.expect("l5", "screens[6].explain.text", round(p200c, 4)); lv.expect("l5", "screens[6].explain.text", round(p200m, 4))
mid20 = mean(run(MID, 20, 0), 1) / 6
cm0, cm1 = mean(runs[(20, 0)], 1) / 6, mean(runs[(20, 1)], 1) / 6
lv.expect("l5", "screens[7].prose", round(cm0 * 100, 2)); lv.expect("l5", "screens[7].prose", round(mid20 * 100, 2)); lv.expect("l5", "screens[7].prose", round(cm1 * 100, 2))
lv.expect("l5", "screens[7].widget.options[0].text", round((cm0 - mid20) * 100, 2))
lv.expect("l5", "screens[7].explain.text", round((p200c - p200m) * 100, 2))
lv.expect("l5", "screens[9].widget.answer", round(20 / 19, 4))

# ---- review and homework
lv.expect("review", "items[0].widget.answer", 2016 + 252)
lv.expect("review", "items[2].widget.answer", round(0.03 ** 2 + 0.04 ** 2, 4))
sp4 = np.array([0, 0.03, -0.03, 0])
lv.expect("review", "items[3].widget.answer", round(float(np.std(sp4)), 4)); lv.expect("review", "items[3].widget.wrong[0].value", round(float(np.std(sp4, ddof=1)), 4))
lv.expect("review", "items[6].widget.answer", round(1.2 / 15, 4))
lv.expect("review", "items[7].widget.answer", round(1.01 ** 12 - 1, 4))
lv.expect("review", "items[8].widget.answer", round(0.5 ** 0.25, 4))
s23 = F0[:, 2] - F0[:, 3]
lv.expect("homework", "items[1].widget.tests[1].expect", round(float((s23 ** 2).sum()), 6))
lv.expect("homework", "items[1].widget.tests[1].expect", round(float(np.abs(s23).max() / np.std(s23)), 6))
c5, e5, n5, _, _ = cycle(C, 0, 5)
lv.expect("homework", "items[4].prose", round(c5 * 100, 2)); lv.expect("homework", "items[4].prose", round(e5 * 100, 2))
lv.expect("homework", "items[4].widget.answer", n5)
lv.expect("homework", "items[5].widget.answer", round(1.0084 ** 12 - 1, 4))
lv.expect("homework", "items[0].widget.tests[6].expect", str([list(p) for p in closest(P2016, 10, True)]))
lv.expect("homework", "items[0].widget.tests[5].expect", str([list(p) for p in closest(P2016, 10, False)]))

check_code(lv)
lv.report()
