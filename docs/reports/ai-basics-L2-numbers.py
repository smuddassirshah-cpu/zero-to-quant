"""Number check for ai-basics level 2 (l5 to l8, review-2, homework-2, problems-2).
Method A: every MSE in floats; method B: the same in exact fractions. The nudging runs are done twice: in exact
fractions here (the rule of l7, ties to the + step, strict "lower"), and by running each code widget's own solution
in CPython floats, which must agree after rounding. The best line on the 0.1 grid is confirmed by brute force.
Run: python3 docs/reports/ai-basics-L2-numbers.py   (exits 0 when every check passes)
"""
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("ai-basics", 2)
X = [1, 2, 3, 4, 5]; Y = [3, 4, 6, 7, 9]


def mse_f(w, b, xs=X, ys=Y):
    return sum((w * x + b - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def mse_q(w, b, xs=X, ys=Y):
    w, b = F(str(w)), F(str(b))
    return sum((w * x + b - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def M(w, b, xs=X, ys=Y):
    a, q = mse_f(float(w), float(b), xs, ys), mse_q(w, b, xs, ys)
    lv.claim(abs(a - float(q)) < 1e-9, f'MSE({w}, {b}) float {a:.6f} = fraction {float(q):.6f}')
    return q


def round_q(w, b, s, xs=X, ys=Y):
    cur = mse_q(w, b, xs, ys)
    up, dn = mse_q(w + s, b, xs, ys), mse_q(w - s, b, xs, ys)
    if min(up, dn) < cur:
        w, cur = (w + s, up) if up <= dn else (w - s, dn)
    up, dn = mse_q(w, b + s, xs, ys), mse_q(w, b - s, xs, ys)
    if min(up, dn) < cur:
        b, cur = (b + s, up) if up <= dn else (b - s, dn)
    return w, b


def fit_q(s, xs=X, ys=Y, w=F(0), b=F(0), pairs=False):
    r, hist = 0, [mse_q(w, b, xs, ys)]
    while True:
        nw, nb = round_q(w, b, s, xs, ys)
        if pairs:
            cur = mse_q(nw, nb, xs, ys)
            a, c = mse_q(nw + s, nb - s, xs, ys), mse_q(nw - s, nb + s, xs, ys)
            if min(a, c) < cur:
                nw, nb = (nw + s, nb - s) if a <= c else (nw - s, nb + s)
        r += 1
        if (nw, nb) == (w, b):
            return w, b, mse_q(w, b, xs, ys), r, hist
        w, b = nw, nb
        hist.append(mse_q(w, b, xs, ys))


def scr(f, title):
    doc = lv.files[[k for k in lv.files if k.startswith(f)][0]]
    for i, s in enumerate(doc['screens']):
        if s.get('title') == title:
            return f'screens[{i}]'
    raise KeyError(title)


def node(f, path):
    doc = lv.files[[k for k in lv.files if k.startswith(f)][0]]
    n = doc
    for part in path.replace(']', '').replace('[', '.').split('.'):
        n = n[int(part)] if part.isdigit() else n[part]
    return n


def item(f, iid):
    doc = lv.files[[k for k in lv.files if k.startswith(f)][0]]
    return f"items[{[i for i, s in enumerate(doc['items']) if s.get('id') == iid][0]}]"


def run_code(f, path, recompute=None):
    w = node(f, path)['widget']
    ok_all, starter_fails = True, False
    for src, want in ((w['solution'], True), (w['starter'], False)):
        ns = {}
        exec(src, ns)
        for t in w['tests']:
            try:
                got = eval(t['call'], ns)
                exp = eval(t['expect'])
                if isinstance(exp, list):
                    ok = len(got) == len(exp) and all(abs(g - e) <= 1e-9 * max(1, abs(e)) for g, e in zip(got, exp))
                else:
                    ok = abs(got - exp) <= 1e-9 * max(1, abs(exp))
            except Exception:
                ok = False
            ok_all &= ok or not want
            starter_fails |= (not ok) and not want
        if want and recompute:
            for t in w['tests']:
                exp = eval(t['expect'])
                alt = recompute(t['call'])
                if alt is not None:
                    same = all(abs(float(a) - e) < 1e-9 for a, e in zip(alt, exp)) if isinstance(exp, list) else abs(float(alt) - exp) < 1e-9
                    lv.claim(same, f"{f} {t['call'][:60]} expect {t['expect']} = exact recompute {alt}")
    lv.claim(ok_all, f'{f} {path}: solution passes every hidden test')
    lv.claim(starter_fails, f'{f} {path}: starter fails a hidden test')
    return w


# ---------------- the course numbers ----------------
lv.claim([2 * x + 1 - y for x, y in zip(X, Y)] == [0, 1, 1, 2, 2], 'errors of y = 2x + 1 are 0, 1, 1, 2, 2')
lv.claim(M(2, 1) == 2 and M(0, 0) == F('38.2') and M(1.5, 1.5) == F('0.1') and M(1.5, 1.3) == F('0.06') and M(0, 5.8) == F('4.56'), 'MSE 2, 38.2, 0.1, 0.06, 4.56')
flat = [F('5.8') - y for y in Y]
lv.claim(sum(flat) == 0 and sum(e * e for e in flat) == F('22.8'), 'flat line: errors add to 0, squares to 22.8')
lv.claim(sum(abs(e) for e in flat) == F('9.2'), 'flat line: sizes add to 9.2 (slip)')
lv.claim(F(sum(Y), 5) == F('5.8'), 'mean of y is 5.8')
grid = min((mse_q(F(i, 10), F(j, 10)), i, j) for i in range(0, 31) for j in range(-10, 31))
lv.claim(grid == (F('0.06'), 15, 13), f'best line on the 0.1 grid by brute force: {grid}')
n = 5; mx = F(sum(X), n); my = F(sum(Y), n)
wls = sum((x - mx) * (y - my) for x, y in zip(X, Y)) / sum((x - mx) ** 2 for x in X)
lv.claim((wls, my - wls * mx) == (F('1.5'), F('1.3')), 'least squares line is 1.5x + 1.3')
wq, bq, eq, rq, hist = fit_q(F(1, 10))
lv.claim((wq, bq, eq, rq) == (F('1.5'), F('1.3'), F('0.06'), 16), 'step 0.1: (1.5, 1.3), 0.06, 16 rounds')
lv.claim(fit_q(F(1, 2))[:4] == (F('1.5'), F('1.5'), F('0.1'), 4), 'step 0.5: (1.5, 1.5), 0.1, 4 rounds')
lv.claim(fit_q(F(1, 100))[:4] == (F('1.48'), F('1.36'), F('0.0608'), 155), 'step 0.01: (1.48, 1.36), 0.0608, 155 rounds')
lv.claim((M(0.1, 0), M(-0.1, 0), M(0.1, 0.1), M(0.1, -0.1)) == (F('34.23'), F('42.39'), F('33.14'), F('35.34')), 'first round 34.23, 42.39, 33.14, 35.34')
lv.claim((M(1.6, 1.3), M(1.4, 1.3), M(1.5, 1.4), M(1.5, 1.2)) == (F('0.17'), F('0.17'), F('0.07'), F('0.07')), 'around the best: 0.17 and 0.07')
lv.claim((M(1.49, 1.36), M(1.47, 1.36), M(1.48, 1.37), M(1.48, 1.35), M(1.49, 1.35), M(1.47, 1.37)) ==
         (F('0.0611'), F('0.0627'), F('0.0609'), F('0.0609'), F('0.0606'), F('0.0622')), 'step 0.01 stop: singles 0.0611 0.0627 0.0609 0.0609, pair 0.0606')
lv.claim(M(1.5, 1.3, X, [3, 4, 6, 7, 15]) == F('7.74'), 'outlier MSE 7.74')

# l5
lv.expect('l5', scr('l5', 'Fit by eye') + '.widget.answer', 2 * 5 + 1 - 9)
for i, e in enumerate([0, 1, 1, 2, 2]):
    lv.claim(node('l5', scr('l5', 'Five errors'))['widget']['rows'][i][3]['answer'] == e, f'l5 error cell {i} = {e}')
    lv.claim(node('l5', scr('l5', 'Square them'))['widget']['rows'][i][2]['answer'] == e * e, f'l5 square cell {i} = {e * e}')
lv.expect('l5', scr('l5', 'Add them up?') + '.widget.answer', 0)
lv.expect('l5', scr('l5', 'The flat line, squared') + '.widget.answer', 22.8)
lv.expect('l5', scr('l5', 'The flat line, squared') + '.feedback.correct', 22.8)
lv.claim(all(2 * x + 1 == y for x, y in [(1, 3), (2, 5), (4, 9)]), 'three points lie on y = 2x + 1')
lv.expect('l5', scr('l5', 'The rule') + '.widget.answer', (10 - 14) ** 2)
lv.claim(sum([1] * 5) == 5 and sum(e * e for e in [1] * 5) == 5 and sum([0, 0, 0, 0, 4]) == 4 and 4 * 4 == 16, 'forecasters: A 5 and 5, B 4 and 16')
lv.expect('l5', 'quiz[1].widget.answer', 1 + 4 + 0 + 9)
lv.claim(sum(e * e for e in [3, -3, 3, -3]) == 36 and sum(e * e for e in [1, 1, 1, 1]) == 4, 'l5 quiz: P 36, Q 4')

# l6
lv.claim(sum((F('1.5') * x + F('1.5') - y) ** 2 for x, y in zip(X, Y)) == F('0.5'), 'sum of squares of 1.5x + 1.5 is 0.5')
lv.expect('l6', scr('l6', 'Which line is better?') + '.widget.answer', 0.5)
chk = node('l6', scr('l6', 'Hunt for a low error'))['widget']
f_chk = lambda a, b: eval(chk['check'].replace('a', str(a)).replace('b', str(b)))
lv.claim(abs(f_chk(1.5, 1.3) - 0.06) < 1e-9 and abs(f_chk(2, 1) - 2) < 1e-9, 'sliders check formula is the MSE')
lv.claim(chk['value'] - chk['tol'] <= 0.06 and chk['value'] + chk['tol'] == 0.5 and f_chk(1.5, 1.5) <= 0.5, 'sliders band takes MSE 0 to 0.5')
lv.expect('l6', scr('l6', 'The mean of the squares') + '.widget.answer', M(2, 1))
lv.expect('l6', scr('l6', 'The mean of the squares') + '.widget.wrong[2].value', F(36, 5))
lv.expect('l6', scr('l6', 'No line at all') + '.widget.answer', M(0, 0))
lv.expect('l6', scr('l6', 'No line at all') + '.widget.wrong[1].value', F(191, 4))
lv.expect('l6', scr('l6', 'The best line') + '.widget.answer', M(1.5, 1.3))
lv.expect('l6', scr('l6', 'One wild point') + '.widget.answer', M(1.5, 1.3, X, [3, 4, 6, 7, 15]))
DA = [2, -1, 3, -2, 1]
lv.claim(F(sum(e * e for e in DA), 5) == F('3.8') and F(25, 5) == 5, 'desk forecasts: A 3.8, B 5')
lv.claim(abs(3.8 ** 0.5 - 1.95) < 0.005, 'root of 3.8 is about 1.95')
lv.expect('l6', scr('l6', 'Scoring forecasts in pounds') + '.widget.answer', 3.8)
lv.expect('l6', 'quiz[1].widget.answer', F(12, 8))
lv.expect('l6', 'quiz[0].widget.answer', F(4 + 1 + 4, 3))
w = run_code('l6', scr('l6', 'MSE in code'), recompute=lambda c: mse_q(*eval(c[3:])) if c.startswith('mse(') else None)
w = run_code('l6', scr('l6', 'Predict in code'))

# l7
lv.expect('l7', scr('l7', 'Try both') + '.widget.answer', M(0.1, 0))
lv.expect('l7', scr('l7', 'Nudge and keep') + '.widget.answer', 0.1)
bars = node('l7', scr('l7', 'Fifteen rounds of moving'))['canvas']['state']['values']
lv.claim([F(str(v)) for v in bars.values()] == hist and len(hist) == 16, 'bars are the 16 MSE values of the step 0.1 run')
first_below = next(i for i, h in enumerate(hist) if h < 1)
lv.expect('l7', scr('l7', 'Fifteen rounds of moving') + '.widget.answer', first_below)
lv.claim(hist[12] == F('1.24') and hist[13] == F('0.5'), 'round 12 leaves 1.24, round 13 leaves 0.50')
w = run_code('l7', scr('l7', 'One round in code'))
for t in w['tests']:
    args = eval(t['call'][len('list(nudge_once'):-1])
    qa = [F(str(a)) if isinstance(a, float) else a for a in args[:2]]
    exact = round_q(qa[0], qa[1], F(str(args[4])), args[2], args[3])
    lv.claim(all(abs(float(a) - e) < 1e-9 for a, e in zip(exact, eval(t['expect']))), f"nudge_once test {t['call'][:50]} = exact {exact}")
lv.expect('l7', 'quiz[0].widget.answer', 0.9)

# l8
w = run_code('l8', scr('l8', 'The fitting script'))
for t in w['tests']:
    xs, ys, s = eval(t['call'][len('list(fit_by_nudging'):-1])
    wq_, bq_, eq_, rq_, _ = fit_q(F(str(s)), xs, ys)
    lv.claim([float(wq_), float(bq_), round(float(eq_), 6), rq_] == eval(t['expect']), f"fit_by_nudging test {t['call'][:50]} = exact")
sw = node('l8', scr('l8', 'A script that reads its data'))['widget']
for t in sw['tests']:
    pts = [tuple(map(float, ln.split())) for ln in t['stdin'].strip().split('\n')]
    xs = [F(str(p[0])) for p in pts]; ys = [F(str(p[1])) for p in pts]
    wq_, bq_, eq_, _, _ = fit_q(F(1, 10), xs, ys)
    want = f"w = {round(float(wq_), 6)}, b = {round(float(bq_), 6)}, error = {round(float(eq_), 6)}\n"
    lv.claim(want == t['expect'], f"script output {t['expect'].strip()} = exact {want.strip()}")
lv.expect('l8', scr('l8', 'A coarser step') + '.widget.answer', fit_q(F(1, 2))[3])
lv.expect('l8', scr('l8', 'Already perfect') + '.widget.answer', fit_q(F(1, 10), [1, 2, 3], [0, 0, 0])[3])
PR = [F('20.10'), F('20.40'), F('20.20'), F('20.80'), F('21.00')]
d = [1, 2, 3, 4, 5]
# The share-price screen quotes the script's own output (fix pass, review-ai-basics): step 0.1 stops at
# w = 0.4, b = 19.3 after 194 rounds; step 0.01 at w = 0.24, b = 19.78 after 1,979 rounds. The least-squares line
# (0.22, 19.84) is NOT what the script prints and the screen must not say it is.
pw, pb, pe, pr = fit_q(F(1, 10), d, PR)[:4]
lv.claim((pw, pb, pr) == (F('0.4'), F('19.3'), 194) and round(float(pe), 6) == 0.088, 'price script, step 0.1: w 0.4, b 19.3, MSE 0.088, 194 rounds (exact)')
pw2, pb2, pe2, pr2 = fit_q(F(1, 100), d, PR)[:4]
lv.claim((pw2, pb2, pr2) == (F('0.24'), F('19.78'), 1979), 'price script, step 0.01: w 0.24, b 19.78, 1979 rounds (exact)')
mxp = F(3); myp = sum(PR) / 5
slope = sum((x - mxp) * (p - myp) for x, p in zip(d, PR)) / 10
lv.claim((slope, myp - slope * mxp) == (F('0.22'), F('19.84')), 'least-squares line 0.22x + 19.84 differs from the script output (not quoted as the script)')
lv.claim('0.22' not in node('l8', scr('l8', 'A line through prices') + '.prose'), 'price screen prose does not quote the least-squares line')
lv.expect('l8', scr('l8', 'A line through prices') + '.widget.answer', pw * 35 + pb)
lv.expect('l8', scr('l8', 'A line through prices') + '.widget.wrong[0].value', pw * 35)
lv.expect('l8', scr('l8', 'A line through prices') + '.widget.wrong[1].value', pw * 5 + pb)
# regression cases added in the fix pass (each wrong rule the review found must fail the hidden test it targets)
fz = fit_q(F(1), [0, 0], [1, 3])
lv.claim((fz[0], fz[1], fz[2], fz[3]) == (F(0), F(2), F(1), 3), 'fit_by_nudging([0,0],[1,3],1) = (0, 2, MSE 1, rounds 3) exact: w never moves, b takes two rounds, then one round changes nothing')
lv.claim(round_q(F(0), F(0), F(1), [0, 1, 2, 3], [2, 1, 0, -1]) == (F(0), F(0)), 'nudge_once tie case stays at (0, 0)')
lv.claim(round_q(F('1.4'), F('1.4'), F('0.1')) == (F('1.5'), F('1.3')), 'nudge_once(1.4, 1.4) -> (1.5, 1.3), b judged at the new w')
lv.claim(sum([1, -1, -3, -5]) / 4 == -2 and sum([-1, 1, 3, 5]) / 4 == 2, 'p-script raw errors have mean -2, the y values mean 2')
s15 = 0.0
for _ in range(15):
    s15 += 0.1
lv.claim(repr(s15) == '1.5000000000000002', 'fifteen 0.1s make 1.5000000000000002')

# ---------------- review-2 ----------------
lv.expect('review', item('review', 'r-error-one') + '.widget.answer', 3 * 2 - 1 - 4)
lv.claim(sum(e * e for e in [5, -5, 4, -4]) == 82, 'r-cancel squares 82')
lv.expect('review', item('review', 'r-squares') + '.widget.answer', 4 + 1 + 0 + 9)
lv.expect('review', item('review', 'r-mse-four') + '.widget.answer', F(14, 4))
lv.expect('review', item('review', 'r-mse-three') + '.widget.answer', round(14 / 3, 2))
lv.claim(round(4 / 3, 2) == 1.33, 'r-mse-three slip: total squared over 3 is 1.33')
lv.expect('review', item('review', 'r-outlier') + '.widget.answer', F(4 + 100, 5))
lv.expect('review', item('review', 'r-outlier') + '.widget.wrong[0].value', F(14, 5))

# ---------------- homework-2 ----------------
HX = [1, 2, 3, 4, 5]; HY = [2, 2, 4, 5, 6]
w = run_code('homework', item('homework', 'h-fit-fresh'))
for t in w['tests']:
    if t['call'].startswith('list(fit_by_nudging'):
        xs, ys, s = eval(t['call'][len('list(fit_by_nudging'):-1])
        r = fit_q(F(str(s)), xs, ys)
        lv.claim([float(r[0]), float(r[1]), round(float(r[2]), 6), r[3]] == eval(t['expect']), f"h-fit-fresh {t['call'][:45]} = exact")
    else:
        a = eval(t['call'][3:])
        lv.claim(abs(float(mse_q(*a)) - eval(t['expect'])) < 1e-9, f"h-fit-fresh {t['call']} = exact")
lv.claim(mse_q(F('1.1'), F('0.5'), HX, HY) == F('0.14') and fit_q(F(1, 10), HX, HY)[2] == F('0.16'), 'fresh table: nudging stops at 0.16, the line 1.1x + 0.5 scores 0.14')
w = run_code('homework', item('homework', 'h-pairs'))
for t in w['tests']:
    xs, ys, s = eval(t['call'][len('list(fit_with_pairs'):-1])
    r = fit_q(F(str(s)), xs, ys, pairs=True)
    lv.claim([float(r[0]), float(r[1]), round(float(r[2]), 6), r[3]] == eval(t['expect']), f"h-pairs {t['call'][:45]} = exact {r[:4]}")
H4X = [0, 1, 2, 3]; H4Y = [2, 3, 5, 6]
lv.expect('homework', item('homework', 'h-mse-fresh') + '.widget.answer', M(1.5, 2, H4X, H4Y))
lv.expect('homework', item('homework', 'h-round-fresh') + '.widget.answer', round_q(F(1), F(2), F(1, 2), H4X, H4Y)[1])
lv.claim(round_q(F(1), F(2), F(1, 2), H4X, H4Y) == (F('1.5'), 2), 'h-round-fresh ends at (1.5, 2)')
lv.claim((M(1, 2, H4X, H4Y), M(1.5, 2, H4X, H4Y), M(0.5, 2, H4X, H4Y), M(1.5, 2.5, H4X, H4Y), M(1.5, 1.5, H4X, H4Y)) ==
         (F('0.5'), F('0.125'), F('2.625'), F('0.625'), F('0.125')), 'h-round-fresh trial errors 0.5, 0.125, 2.625, 0.625, 0.125 (a tie)')

# ---------------- problems-2 ----------------
PX = [1, 2, 3, 4, 5]; PY = [1, 3, 4, 6, 6]
lv.expect('problems', 'items[0].parts[0].widget.answer', 4 + 1 - 6)
lv.expect('problems', 'items[0].parts[1].widget.answer', M(1, 1, PX, PY))
lv.expect('problems', 'items[0].parts[2].widget.answer', M(1.5, 0, PX, PY))
lv.claim((M(1.1, 1, PX, PY), M(0.9, 1, PX, PY), M(1.1, 1.1, PX, PY), M(1.1, 0.9, PX, PY)) == (F('0.39'), F('0.63'), F('0.46'), F('0.34')), 'shop round: 0.39, 0.63, 0.46, 0.34')
lv.claim(round_q(F(1), F(1), F(1, 10), PX, PY) == (F('1.1'), F('0.9')), 'shop round ends at (1.1, 0.9)')
lv.expect('problems', 'items[0].parts[3].widget.answer', 0.9)
lv.expect('problems', 'items[0].parts[4].widget.answer', M(1.1, 0.9, PX, PY))
QX = [1, 2, 3, 4, 5]; QY = [2, 6, 5, 9, 8]
lv.claim(sum(6 - y for y in QY) == 0, 'stuck: flat errors add to 0')
lv.expect('problems', 'items[1].parts[1].widget.answer', M(0, 6, QX, QY))
lv.expect('problems', 'items[1].parts[2].widget.answer', M(1.6, 1.2, QX, QY))
lv.claim((M(1.7, 1.2, QX, QY), M(1.5, 1.2, QX, QY), M(1.6, 1.3, QX, QY), M(1.6, 1.1, QX, QY)) == (F('1.67'), F('1.59'), F('1.53'), F('1.53')), 'stuck trials 1.67, 1.59, 1.53, 1.53')
lv.claim(round_q(F('1.6'), F('1.2'), F(1, 10), QX, QY) == (F('1.6'), F('1.2')), 'stuck: the round changes nothing')
lv.claim(M(1.5, 1.5, QX, QY) == F('1.5'), 'stuck: 1.5x + 1.5 scores 1.5 (least squares)')
RX = [0, 1, 2, 3]; RY = [-1, 1, 3, 5]
lv.expect('problems', 'items[2].parts[0].widget.answer', M(0, 0, RX, RY))
lv.claim((M(1, 0, RX, RY), M(-1, 0, RX, RY), M(1, 1, RX, RY), M(1, -1, RX, RY)) == (F('1.5'), F('23.5'), F('1.5'), F('3.5')), 'script problem trials 1.5, 23.5, 1.5 (tie), 3.5')
lv.claim(fit_q(F(1), RX, RY)[:4] == (2, -1, 0, 3), 'script problem: (2, -1), MSE 0, 3 rounds')
lv.expect('problems', 'items[2].parts[3].widget.answer', 3)

lv.check_wrongs()
lv.report()
