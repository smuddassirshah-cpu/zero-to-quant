"""pairs-rep level 2: recompute every stated number and check it at its JSON path. Exit 0 when all pass."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pairs_rep_common import *  # noqa: F401,F403
from numbers_lib import Level  # noqa: E402  (explicit, for the validator rule 579)

lv = Level("pairs-rep", 2)
C = CLOSE
P0 = C[:378] / C[0]; F0, T0 = P0[:252], P0[252:]
sd = float(np.std(F0[:, 2] - F0[:, 3])); sp = T0[:, 2] - T0[:, 3]

# ---- l6
first = next(t for t in range(126) if abs(sp[t]) > 2 * sd)
lv.expect("l6", "screens[0].widget.answer", first); lv.expect("l6", "screens[0].prose", round(sd, 4)); lv.expect("l6", "screens[0].prose", round(2 * sd, 4))
lv.expect("l6", "screens[0].explain.text", round(sp[first], 4))
lv.expect("l6", "screens[0].widget.wrong[0].value", next(t for t in range(126) if abs(sp[t]) > 1.5 * sd))
cnt = {}
pay = {}
for m in (1.5, 2.0, 2.5, 3.0):
    lg = []; p, _, n = trade(F0, T0, 2, 3, 0, m, log=lg); cnt[m] = n; pay[m] = p
    lv.expect("l6", "screens[1].canvas.controls", round(m * sd, 4))
lv.expect("l6", "screens[1].widget.answer", cnt[3.0]); lv.expect("l6", "screens[1].explain.text", cnt[1.5]); lv.expect("l6", "screens[1].explain.text", cnt[2.5])
for r, m in enumerate((1.5, 2.0, 3.0)):
    lv.expect("l6", f"screens[4].widget.rows[{r}][1].answer", cnt[m]); lv.expect("l6", f"screens[4].widget.rows[{r}][2]", round(pay[m], 4))
pa, pb = T0[first, 2], T0[first, 3]
lv.expect("l6", "screens[2].prose", round(pa, 4)); lv.expect("l6", "screens[2].prose", round(pb, 4))
lv.expect("l6", "screens[3].widget.answer", round(1 / pa, 4)); lv.expect("l6", "screens[3].explain.text", round(1 / pb, 4))
lg = []; trade(F0, T0, 2, 3, 0, log=lg)
lv.expect("l6", "screens[5].widget.answer", round(-lg[0][3], 4)); lv.expect("l6", "screens[5].prose", round(lg[0][3], 4))
lv.expect("l6", "screens[7].widget.tests[6].expect", round(2 * sd, 6))
lv.expect("l6", "screens[9].widget.answer", round(1_000_000 / 58.40))

# ---- l7
tot = sum(x[3] for x in lg)
lv.expect("l7", "screens[0].widget.answer", lg[0][1]); lv.expect("l7", "screens[0].explain.text", round(lg[0][3], 4))
lv.expect("l7", "screens[1].widget.answer", len(lg)); lv.expect("l7", "screens[1].explain.text", round(tot, 4))
e0, x0 = lg[0][0], lg[0][1]
lv.expect("l7", "screens[2].prose", round(T0[e0, 2], 4)); lv.expect("l7", "screens[2].prose", round(T0[x0, 3], 4))
lv.expect("l7", "screens[2].widget.answer", round(lg[0][3], 4))
lv.expect("l7", "screens[2].explain.text", round(T0[x0, 2] / T0[e0, 2] - 1, 4)); lv.expect("l7", "screens[2].explain.text", round(T0[x0, 3] / T0[e0, 3] - 1, 4))
for r, x in enumerate(lg):
    lv.expect("l7", f"screens[3].widget.rows[{r}][3].answer", x[1]); lv.expect("l7", f"screens[3].widget.rows[{r}][4]", round(x[3], 4))
lv.expect("l7", "screens[3].widget.rows[4][4].answer", round(tot, 4))
lv._rec([x[1] - x[0] for x in lg] == [15, 8, 11, 9], "l7 holding days 15, 8, 11, 9", "")
P21 = C[21:399] / C[21]
lg21 = []; trade(P21[:252], P21[252:], 48, 62, 0, log=lg21)
lv._rec((48, 62) in closest(P21[:252], 20), "l7 pair (48, 62) is in the top 20 of the cycle from day 21", "")
lv.expect("l7", "screens[4].prose", lg21[-1][0]); lv.expect("l7", "screens[4].explain.text", round(lg21[-1][3], 4))
nf = nt = 0
for st in range(0, 2647, 21):
    P = C[st:st + 378] / C[st]
    for i, j in closest(P[:252], 20):
        L = []; trade(P[:252], P[252:], i, j, 0, log=L)
        nt += len(L)
        s_ = P[252:, i] - P[252:, j]; sdv = np.std(P[:252, i] - P[:252, j])
        for (en, ex, side, _) in L:
            nf += not any(s_[u] * side <= 0 for u in range(en + 1, ex + 1))
lv.expect("l7", "screens[4].explain.text", round(100 * nf / nt))

def trade_stop(form, tr, i, j, stop=4.0):
    sdv = float(np.std(form[:, i] - form[:, j])); s_ = tr[:, i] - tr[:, j]; n = len(s_); t = 0; pay = 0.0
    while t < n:
        if abs(s_[t]) > 2 * sdv and t < n - 1:
            side = 1 if s_[t] > 0 else -1; en = t; ex = n - 1; hit = False
            for u in range(t + 1, n):
                if s_[u] * side <= 0:
                    ex = u; break
                if abs(s_[u]) > stop * sdv:
                    ex = u; hit = True; break
            pay += side * ((tr[ex, j] / tr[en, j] - 1) - (tr[ex, i] / tr[en, i] - 1))
            if hit:
                break
            t = ex + 1; continue
        t += 1
    return pay
def stop_cycle(st):
    P = C[st:st + 378] / C[st]
    return sum(trade_stop(P[:252], P[252:], i, j) for i, j in closest(P[:252], 20)) / 20
s21 = float(np.mean([stop_cycle(st) for st in range(0, 2647, 21)]))
f21 = float(np.mean([x[1] for x in run(C, 20, 0)]))
lv.expect("l7", "screens[5].widget.options[0].text", round(s21 * 100, 2)); lv.expect("l7", "screens[5].widget.options[0].text", round(f21 * 100, 2))
lv.expect("l7", "screens[5].explain.text", round(stop_cycle(0) * 100, 2)); lv.expect("l7", "screens[5].explain.text", round(cycle(C, 0, 20)[0] * 100, 2))

def trade_band(form, tr, i, j):
    sdv = float(np.std(form[:, i] - form[:, j])); s_ = tr[:, i] - tr[:, j]; n = len(s_); t = 0; pay = 0.0; k = 0
    while t < n:
        if abs(s_[t]) > 2 * sdv and t < n - 1:
            side = 1 if s_[t] > 0 else -1; en = t
            ex = next((u for u in range(t + 1, n) if abs(s_[u]) <= 2 * sdv), n - 1)
            pay += side * ((tr[ex, j] / tr[en, j] - 1) - (tr[ex, i] / tr[en, i] - 1)); k += 1; t = ex + 1; continue
        t += 1
    return pay, k
bp, bk = trade_band(F0, T0, 2, 3)
lv.expect("l7", "screens[6].prose", round(bp, 4)); lv.expect("l7", "screens[6].explain.text", bk)
lv.expect("l7", "screens[6].explain.text", round(sum(trade_band(F0, T0, i, j)[0] for i, j in closest(F0, 20)) / 20 * 100, 2))
lgw = []; trade(F0, T0, 2, 3, 1, log=lgw)
lv.expect("l7", "screens[8].explain.text", round(sum(x[3] for x in lgw), 4))
lv.expect("l7", "screens[8].widget.tests[11].expect", str([x[1] - x[0] for x in lgw]))

# ---- l8
c5, e5, n5, _, r5 = cycle(C, 0, 5); c20, e20, n20, _, r20 = cycle(C, 0, 20)
t5 = sum(r[0] for r in r5); t20 = sum(r[0] for r in r20)
lv.expect("l8", "screens[0].prose", round(t5, 4)); lv.expect("l8", "screens[0].widget.answer", round(t5 / 5, 4)); lv.expect("l8", "screens[0].explain.text", round(t5 / 4 * 100, 2))
runs = {(k, w): run(C, k, w) for k in (5, 20) for w in (0, 1)}
mean = lambda r, col: float(np.mean([x[col] for x in r]))
lv.expect("l8", "screens[1].widget.answer", round(mean(runs[(20, 0)], 1), 4)); lv.expect("l8", "screens[1].explain.text", round(mean(runs[(5, 0)], 1) * 100, 2))
lv.expect("l8", "screens[2].widget.rows[1][2].answer", round(t20 / 19, 4)); lv.expect("l8", "screens[2].widget.rows[0][2].answer", round(t5 / 4, 4))

def nw(x, L=5):
    x = np.asarray(x); n = len(x); e = x - x.mean(); s2 = sum(e[t] * e[t] for t in range(n)) / n
    for l in range(1, L + 1):
        s2 += 2 * (1 - l / (L + 1)) * sum(e[t] * e[t - l] for t in range(l, n)) / n
    return x.mean() / np.sqrt(s2 / n), x.mean() / (x.std(ddof=1) / np.sqrt(n))
m0 = [x[1] / 6 for x in runs[(20, 0)]]; m1 = [x[1] / 6 for x in runs[(20, 1)]]
nw0, nv0 = nw(m0); nw1, nv1 = nw(m1)
lv.expect("l8", "screens[4].question", round(nw0, 2)); lv.expect("l8", "screens[4].question", round(nv0, 2))
lv.expect("l8", "screens[4].explain.text", round(nw1, 2)); lv.expect("l8", "screens[4].explain.text", round(nv1, 2))
c21, e21, n21, _, _ = cycle(C, 21, 20)
lv._rec(n21 == 20 and abs(c21 - e21) < 1e-15, "l8 every pair opens in the cycle from day 21", "")
lv.expect("l8", "screens[6].explain.text", round(c21 * 100, 2))
lv.expect("l8", "screens[6].explain.text", sum(1 for x in runs[(20, 0)] if x[3] == 20))
r126 = {(k, w): run(C, k, w, 126) for k in (5, 20) for w in (0, 1)}
lv._rec(len(r126[(20, 0)]) == 22, "l8 step 126 gives 22 cycles", "")
lv.expect("l8", "screens[8].widget.tests[3].expect", round(mean(r126[(20, 0)], 1), 6))
lv.expect("l8", "screens[8].explain.text", round(mean(r126[(20, 0)], 1) * 100, 2))
lv.expect("l8", "screens[9].widget.answer", 20 * 1_000_000 * round(mean(runs[(20, 1)], 1), 4))

# ---- l9
mid0 = mean(run(MID, 20, 0), 1) / 6; midw = mean(run(MID, 20, 1), 1) / 6
cm0, cm1 = mean(runs[(20, 0)], 1) / 6, mean(runs[(20, 1)], 1) / 6
lv.expect("l9", "screens[2].widget.answer", round(cm0 - mid0, 4))
Pm = MID[:378] / MID[0]
jc = float(np.mean(np.abs(np.diff(np.round(sp, 4))))); jm = float(np.mean(np.abs(np.diff(np.round(Pm[252:, 2] - Pm[252:, 3], 4)))))
lv.expect("l9", "screens[1].explain.text", round(jc, 4)); lv.expect("l9", "screens[1].explain.text", round(jm, 4))
trips = 0
for st in range(0, 2647, 21):
    P = C[st:st + 378] / C[st]
    trips += sum(trade(P[:252], P[252:], i, j, 1)[2] for i, j in closest(P[:252], 20))
tpp = trips / 127 / 20
g6 = mean(runs[(20, 1)], 1)
lv.expect("l9", "screens[4].prose", round(tpp, 2)); lv.expect("l9", "screens[4].widget.answer", round(4 * 0.001 * tpp, 5))
lv.expect("l9", "screens[5].widget.answer", round(g6 / (4 * tpp), 5)); lv.expect("l9", "screens[5].prose", round(tpp, 4))
lv.expect("l9", "screens[6].widget.options[0].text", round(g6 / (4 * tpp) * 100, 2))
lv.expect("l9", "screens[7].widget.answer", round(mid0 - midw, 4))
lv.expect("l9", "screens[8].widget.tests[5].expect", round(mean(r126[(20, 0)], 1) / 6, 6))
lv.expect("l9", "screens[8].widget.tests[5].expect", round(mean(run(MID, 20, 0, 126), 1) / 6, 6))
for path, v in (("screens[2].canvas.params.rows[0][1]", cm0), ("screens[2].canvas.params.rows[1][1]", mid0), ("screens[2].canvas.params.rows[2][1]", cm1), ("screens[2].canvas.params.rows[3][1]", midw)):
    lv.expect("l9", path, round(v * 100, 2))

# ---- l10
ann = lambda m: (1 + m) ** 12 - 1
cells = [cm0, cm1, mean(runs[(5, 0)], 1) / 6, mean(runs[(5, 1)], 1) / 6]
lv.expect("l10", "screens[1].widget.answer", sum(1 for c in cells if ann(c) > 0.11))
for r, c in enumerate(cells):
    lv.expect("l10", f"screens[1].canvas.params.rows[{r}][3]", round(ann(c) * 100, 1))
lv.expect("l10", "screens[4].widget.answer", round(mean(r126[(20, 0)], 1) / 6 - cm0, 4))
lv.expect("l10", "screens[8].widget.answer", round(ann(cells[3]), 4))
lv.expect("l10", "screens[0].canvas.params.rows[1][1]", round(g6 / (4 * tpp) * 100, 2))
lv.expect("l10", "screens[7].widget.tests[1].expect", round(mean(r126[(5, 1)], 1) / 6, 6))

# ---- review and homework
lv.expect("review", "items[2].widget.answer", round((1.05 / 1.10 - 1) - (1.08 / 1.20 - 1), 4))
lv.expect("review", "items[4].widget.answer", round(0.90 / 20 / 6, 4))
lv.expect("review", "items[6].widget.answer", round(0.036 / 6, 4))
lv.expect("review", "items[7].widget.answer", round(cm0 - mid0, 4))
lv.expect("review", "items[5].prose", round(nv0, 2)); lv.expect("review", "items[5].prose", round(nw0, 2))
lv.expect("review", "items[3].explain.text", round(sum(trade_band(F0, T0, i, j)[0] for i, j in closest(F0, 20)) / 20 * 100, 2))
for k, w in ((5, 0), (5, 1), (20, 0), (20, 1)):
    lv.expect("homework", "items[0].widget.tests[1].expect", round(mean(runs[(k, w)], 1) / 6, 6))
lv.expect("homework", "items[1].widget.tests[1].expect", round(lgw[1][3], 6))
net = (g6 - 4 * 0.002 * tpp) / 6
lv.expect("homework", "items[4].widget.answer", round(net, 5))
lv.expect("homework", "items[5].widget.answer", round(1_000_000 / 23.10))
lv.expect("homework", "items[3].widget.model", round((mid0 - midw) * 100, 2))

# ---- fix pass additions
lv.expect("l7", "screens[2].widget.accept", round(T0[x0, 2] / T0[e0, 2] - 1, 5)); lv.expect("l7", "screens[2].widget.accept", round(T0[x0, 3] / T0[e0, 3] - 1, 5))
lv.expect("l7", "screens[4].prose", round(lg21[0][3], 4))
_cl = mean(run(C, 20, 0), 1) / 6; _mi = mean(run(MID, 20, 0), 1) / 6
lv.expect("l9", "screens[2].widget.accept", round(_cl * 100, 3)); lv.expect("l9", "screens[2].widget.accept", round(_mi * 100, 3))
_rows = [(st, cycle(C, st, 5)[0], cycle(C, st, 5)[3]) for st in range(1260, 2647, 21)]
_un = set((2 * k, 2 * k + 1) for k in range(20) if not BROKEN[k])
lv.expect("l10", "screens[6].explain.text", round(float(np.mean([len(_un & set(r[2])) for r in _rows])), 1))
lv.expect("l10", "screens[6].explain.text", round(float(np.mean([r[1] for r in _rows])) / 6 * 100, 2))
lv.expect("l10", "screens[6].explain.text", round(float(np.mean([cycle(C, st, 20)[0] for st in range(1260, 2647, 21)])) / 6 * 100, 2))

check_code(lv)
lv.report()
