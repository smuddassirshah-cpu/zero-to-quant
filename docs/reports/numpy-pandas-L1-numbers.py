"""Recompute every number and printed output stated in numpy-pandas level 1 (Arrays): l1 to l4, review-1, homework-1.
Second read (session V). Run: python3 docs/reports/numpy-pandas-L1-numbers.py   (needs numpy; exits 0 when every check passes)
Each "What does it print" snippet is executed and its output compared with the keyed option (whitespace-normalised;
a 2-D array printed on two lines is compared on one line, as the options show it). Numbers are computed twice where a
second route exists (by hand arithmetic and by NumPy). `lv.claim_text` ties a claim to its wording: it fails while a
false sentence is in the text and passes once it is reworded. Checks that fail on the current content are findings in
docs/reviews/review-numpy-pandas-1-3.md. Behaviour is checked against the NumPy that runs this script; the reader ran it
under NumPy 2.0.2 (Pyodide 0.27.7's) and NumPy 2.5.3, with the same results.
"""
import sys, os, io, math, contextlib, warnings
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("numpy-pandas", 1)
E = lv.expect
C = lv.claim


def run(code):
    """Exec a snippet with numpy imported; return (printed text, exception class name or None)."""
    out = io.StringIO()
    g = {'np': np}
    try:
        with contextlib.redirect_stdout(out), warnings.catch_warnings():
            warnings.simplefilter('error')
            exec(code, g)
        return out.getvalue(), None
    except Exception as e:
        return out.getvalue(), type(e).__name__ + ': ' + str(e)


def norm(s):
    return ' '.join(s.replace('`', '').split())


def prints(fid, path, code, label=None):
    """The snippet prints exactly the text at path (backticks stripped, whitespace collapsed)."""
    txt, err = run(code)
    want = norm(lv.text(fid, path))
    C(err is None and norm(txt) == want, label or f'{fid} {path} prints {want!r}', f'printed {txt!r} err {err}')


def raises(fid, path, code, exc, fragment=''):
    txt, err = run(code)
    C(err is not None and err.startswith(exc) and fragment in err, f'{fid} {path}: snippet raises {exc} {fragment!r}', f'got {err!r}')


def two(label, a, b, tol=1e-9):
    C(abs(a - b) <= tol * max(1, abs(a)), f'two routes agree: {label} ({a!r})', f'{a!r} vs {b!r}')


# ---------------------------------------------------------------- l1-not-lists
p = np.array([100.00, 102.50, 98.00, 101.20])
E('l1', 'screens[0].explain.text', round(100 * 1.02, 2))
E('l1', 'screens[0].explain.text', round(98 * 1.02, 2))                       # 99.96
two('98 x 1.02', 98 * 1.02, 99.96)
E('l1', 'screens[0].widget.options[2].why', 101.02)                           # 100 + 1.02
sh, pr = np.array([10, 4, 25]), np.array([12.50, 40.00, 3.20])
v = sh * pr
two('value[1]', float(v[1]), 4 * 40.0)
E('l1', 'screens[1].widget.answer', 160)
E('l1', 'screens[1].widget.wrong[0].value', float(v.sum()))                   # 365
two('total', float(v.sum()), 125 + 160 + 80)
E('l1', 'screens[1].widget.wrong[1].value', float(v[0]))
E('l1', 'screens[1].widget.wrong[2].value', float(v[2]))
E('l1', 'screens[1].explain.canvas.caption', 125.00)
raises('l1', 'screens[2]', 'a = np.array([1.0, 2.0, 3.0]); b = np.array([10.0, 20.0]); print(a + b)', 'ValueError', 'shapes (3,) (2,)')
txt, _ = run('prices = [100.00, 102.50, 98.00]\ndoubled = prices * 2\nprint(len(doubled))')
C(txt.strip() == '6', 'l1 screens[3]: len(prices * 2) is 6')
raises('l1', 'screens[3].widget.options[2].why', 'x = [100.0, 102.5] * 1.02', 'TypeError')
_, err = run("x = [1.0, 2.0] * 'a'")
lv.claim_text('l1', 'screens[3].widget.options[2].why', 'Only a float such as', False,
              'l1 screens[3] why: "Only a float" raises TypeError (a str, a list or None does too: any non-integer)')
lv.claim_text('l1', 'screens[3].feedback.byKey.error', 'Only a float such as', False,
              'l1 screens[3] byKey.error: "Only a float" raises TypeError (any non-integer does)')
prints('l1', 'screens[4].widget.options[1].text', 'qty = np.array([100, 250, 40])\nqty[0] = 99.75\nprint(qty[0])')  # no warning either (warnings are errors in run)
q = np.array([100.00, 102.00, 100.98, 103.00])
r = q[1:] / q[:-1] - 1
two('r[1]', float(r[1]), -0.01)
E('l1', 'screens[6].widget.answer', -0.01)
E('l1', 'screens[6].widget.wrong[0].value', round(100.98 / 102.00, 4))       # 0.99
E('l1', 'screens[6].widget.wrong[1].value', round(float(r[0]), 4))           # 0.02
E('l1', 'screens[6].widget.wrong[2].value', round(102.00 / 100.98 - 1, 4))   # 0.0101
E('l1', 'screens[6].widget.wrong[3].value', -1)
E('l1', 'screens[6].explain.canvas.values.r2c3', 0.0200)
two('r[2]', round(float(r[2]), 4), 0.02)
E('l1', 'screens[6].hints[2].text', 0.99)
two('diff route = slice route', float((np.diff(q) / q[:-1])[1]), float(r[1]))
raises('l1', 'screens[7].widget.options[2].why', 'p = np.array([1.0, 2.0, 3.0, 4.0]); np.diff(p) / p', 'ValueError')
reb = np.array([250.0, 255.0, 245.0]) / 250.0 * 100
C(np.allclose(reb, [100, 102, 98]), 'l1 screens[8] prose: 250, 255, 245 rebase to 100, 102, 98')
E('l1', 'screens[8].prose', 102)
E('l1', 'screens[9].feedback.byKey.test-1', -0.01)
prints('l1', 'quiz[0].widget.options[0].text', 'a = np.array([1, 2, 3]); b = np.array([4, 5, 6]); print(a * b)')
two('dot', float(np.dot([1, 2, 3], [4, 5, 6])), 32)
E('l1', 'quiz[0].widget.options[1].text', 32)
prints('l1', 'quiz[1].widget.options[1].text', 'print([1, 2] + [3, 4])')
E('l1', 'quiz[2].widget.answer', 250 - 1)
C(len(np.diff(np.arange(250.0)) / np.arange(250.0)[:-1]) == 249, 'l1 quiz[2]: 250 prices give 249 returns')
prints('l1', 'quiz[3].widget.options[0].text', 'print(np.array([10, 20, 30]) / 4)')
E('l1', 'quiz[3].widget.options[3].text', 60 / 4)
prints('l1', 'quiz[3].widget.options[1].text', 'print(np.array([10, 20, 30]) // 4)', 'l1 quiz[3] floor option is what // prints')

# ---------------------------------------------------------------- l2-shapes-and-axes
pnl = np.array([[120, -40, 15], [-60, 80, 25], [30, 10, -45], [90, -20, 5]])
E('l2', 'screens[0].widget.answer', int(pnl[3, 1]))
E('l2', 'screens[0].widget.wrong[0].value', int(pnl[2, 0]))                   # counted from 1
C(pnl.shape == (4, 3) and pnl.size == 12, 'l2 screens[1]: shape (4, 3), size 12')
prints('l2', 'screens[3].widget.options[0].text', 'print(pnl.sum(axis=0))'.replace('pnl', repr(pnl.tolist()).join(['np.array(', ')'])))
E('l2', 'screens[2].hints[2].text', 120 - 60 + 30 + 90)
prints('l2', 'screens[3].widget.options[1].text', f'print(np.array({pnl.tolist()}).sum(axis=1))')
E('l2', 'screens[3].widget.options[2].text', int(pnl.sum()))
two('210', int(pnl.sum()), 95 + 45 - 5 + 75)
prints('l2', 'screens[3].widget.options[3].text', f'print(np.array({pnl.tolist()}).sum(axis=1)[:3])', 'l2 screens[3] first-three option format')
M = np.arange(6).reshape(2, 3)
C(M[1, 0] == 3 and M[0, 2] == 2 and M[0, 0] == 0, 'l2 screens[4]: 3 lands at row 1, column 0')
C(np.arange(6).reshape(2, 3, order='F')[1, 1] == 3, 'l2 screens[4] byKey M-1-1: filling down columns puts 3 at row 1, column 1')
raises('l2', 'screens[4].explain.text', 'np.arange(6).reshape(4, 2)', 'ValueError')
rr = np.array([1.0, -0.5, 2.0, 0.5, -1.0])
two('mean 0.4', float(rr.mean()), 0.4)
ss = float(((rr - rr.mean()) ** 2).sum())
two('squared deviations 5.7', ss, 0.36 + 0.81 + 2.56 + 0.01 + 1.96)
E('l2', 'screens[5].canvas.state.caption', 5.7)
prints('l2', 'screens[5].widget.options[0].text', 'r = np.array([1.0, -0.5, 2.0, 0.5, -1.0]); print(round(float(np.std(r)), 3))')
E('l2', 'screens[5].widget.options[1].text', round(float(np.std(rr, ddof=1)), 3))
two('sample sd', float(np.std(rr, ddof=1)), math.sqrt(5.7 / 4))
E('l2', 'screens[5].widget.options[2].text', round(float(np.var(rr)), 3), fmt='{:.3f}')
E('l2', 'screens[5].widget.options[3].text', 0.4, fmt='{:.3f}')
E('l2', 'screens[5].explain.text', round(math.sqrt(5.7 / 4), 3))
prints('l2', 'screens[6].widget.options[0].text', 'r = np.array([0.10, -0.10]); print(np.cumprod(1 + r))')
prints('l2', 'screens[6].widget.options[2].text', 'r = np.array([0.10, -0.10]); print(np.cumsum(r))', 'l2 screens[6] cumsum option is what np.cumsum(r) prints')
two('0.11 lost', 1.10 * 0.10, 0.11)
E('l2', 'screens[6].widget.options[1].why', 0.11)
E('l2', 'screens[7].widget.options[2].why', 252 * 5)
raises('l2', 'screens[7].widget.options[3].why', 'np.ones((252, 5)).mean(axis=2)', 'AxisError')
# desk_pnl test-1 feedback: a learner who sums with axis=0 and keeps the cumsum returns 180, 210, 210, not 180, 30, 0
wrong_axis = np.cumsum(pnl.sum(axis=0)).tolist()
C(np.cumsum(pnl.sum(axis=1)).tolist() == [95, 140, 135, 210], 'l2 screens[8]: desk P&L 95, 140, 135, 210')
lv.claim_text('l2', 'screens[8].feedback.byKey.test-1', 'If you got 180, 30, 0', wrong_axis == [180, 30, 0],
              f'l2 screens[8] byKey.test-1: an axis=0 learner gets {wrong_axis}, not 180, 30, 0')
t1 = np.array([[0.01, 0.02], [-0.01, 0.00], [0.02, -0.02], [0.00, 0.01]])
ratio = float(np.std(t1, axis=0)[0] / np.std(t1, axis=0, ddof=1)[0])
two('ddof ratio n=4', ratio, math.sqrt(3 / 4))
C(round(ratio, 2) == 0.87, 'l2 screens[9] byKey.test-1: about 0.87 times too small without ddof (n = 4)')
C(round(252 / math.sqrt(252), 1) == 15.9, 'l2 screens[9] byKey.test-1: 252 is 15.9 times sqrt(252)')
E('l2', 'screens[9].explain.text', round(math.sqrt(252), 2))
prints('l2', 'quiz[0].widget.options[0].text', 'x = np.zeros((3, 5)); print(x.sum(axis=0).shape)')
raises('l2', 'quiz[1]', 'np.arange(6).reshape(4, 2)', 'ValueError')
x8 = np.array([2, 4, 4, 4, 5, 5, 7, 9])
two('mean 5', float(x8.mean()), 5)
two('sq dev 32', float(((x8 - 5) ** 2).sum()), 32)
E('l2', 'quiz[2].widget.answer', round(float(np.std(x8, ddof=1)), 3))
two('sqrt(32/7)', float(np.std(x8, ddof=1)), math.sqrt(32 / 7))
E('l2', 'quiz[2].widget.wrong[0].value', float(np.std(x8)))
E('l2', 'quiz[2].widget.wrong[1].value', round(32 / 7, 3))
prints('l2', 'quiz[3].widget.options[0].text', 'print(np.cumsum(np.array([5, -2, 3])))')
prints('l2', 'quiz[3].widget.options[3].text', 'print(np.cumprod(np.array([5, -2, 3])))', 'l2 quiz[3] cumprod option is what np.cumprod prints')
prints('l2', 'quiz[3].widget.options[2].text', 'print(np.array([5, -2, 3]))', 'l2 quiz[3] same option format')
# "The last element of np.cumsum always equals np.sum": true for integers, false for floats (sum is pairwise, cumsum sequential)
f = np.random.default_rng(0).random(1000)
lv.claim_text('l2', 'quiz[3].explain.text', 'always equals `np.sum`', float(np.cumsum(f)[-1]) == float(np.sum(f)),
              f'l2 quiz[3] explain "always equals np.sum": floats differ, {np.cumsum(f)[-1]!r} vs {np.sum(f)!r}')

# ---------------------------------------------------------------- l3-masks
ret = np.array([0.8, -1.2, 0.0, 2.1, -0.4, 0.3, -2.5])
C(np.flatnonzero(ret < 0).tolist() == [1, 4, 6], 'l3 screens[0]: losing days at 1, 4, 6')
prints('l3', 'screens[1].widget.options[0].text', f'returns = np.array({ret.tolist()}); print(returns < 0)')
prints('l3', 'screens[1].widget.options[1].text', f'returns = np.array({ret.tolist()}); print(returns[returns < 0])', 'l3 screens[1] values option format')
E('l3', 'screens[2].widget.answer', round(float(ret[ret < 0].mean()), 2))
two('loss mean', float(ret[ret < 0].mean()), -4.1 / 3)
E('l3', 'screens[2].widget.accept', round(-4.1 / 3, 4))
E('l3', 'screens[2].widget.wrong[0].value', round(-4.1 / 7, 2))
E('l3', 'screens[2].widget.wrong[1].value', round(float(ret[ret < 0].sum()), 2))
E('l3', 'screens[2].widget.wrong[2].value', round(float(ret.mean()), 2))
E('l3', 'screens[3].widget.answer', round(float((ret < 0).mean()), 4))
two('3/7', float((ret < 0).mean()), 3 / 7)
E('l3', 'screens[3].widget.wrong[0].value', int((ret < 0).sum()))
E('l3', 'screens[3].widget.wrong[1].value', round(-4.1 / 3, 4))
E('l3', 'screens[3].widget.wrong[2].value', round(float((ret >= 0).mean()), 4))
E('l3', 'screens[3].widget.wrong[3].value', 3 / 6)
raises('l3', 'screens[4]', f'returns = np.array({ret.tolist()}); mid = returns[returns < 0 and returns > -2]', 'ValueError', 'ambiguous')
C(ret[(ret < 0) & (ret > -2)].tolist() == [-1.2, -0.4], 'l3 screens[5]: mid keeps -1.2 and -0.4')
C(((ret < 0) | (ret > -2)).all(), 'l3 screens[5] byKey.either: every day is below 0 or above -2')
raises('l3', 'screens[5].explain.text', f'returns = np.array({ret.tolist()}); returns[returns < 0 & returns > -2]', 'TypeError')
E('l3', 'screens[6].widget.answer', int((np.where(ret > 0, 1, -1) == -1).sum()))
C(int((ret > 1).sum()) == 1, 'l3 screens[7]: one day above 1')
C(len(ret > 1) == 7, 'l3 screens[7] why: len of the mask is 7')
hr = np.array([120.50, -40.00, 0.00, 75.25])
two('hit rate', float((hr > 0).sum() / ((hr > 0).sum() + (hr < 0).sum())), 2 / 3)
E('l3', 'screens[9].feedback.byKey.test-1', float((hr > 0).sum() / len(hr)))   # 0.5
xq = 'x = np.array([3, -1, 4, -1, 5]); '
prints('l3', 'quiz[0].widget.options[0].text', xq + 'print(x[x > 3])')
prints('l3', 'quiz[0].widget.options[1].text', xq + 'print(x > 3)', 'l3 quiz[0] mask option format')
E('l3', 'quiz[1].widget.answer', 2)
txt, _ = run(xq + 'print((x < 0).sum())')
C(txt.strip() == '2', 'l3 quiz[1] prints 2')
E('l3', 'quiz[1].widget.wrong[0].value', -2)
prints('l3', 'quiz[2].widget.options[0].text', xq + 'print(np.where(x > 0, x, 0))')
prints('l3', 'quiz[2].widget.options[2].text', xq + 'print(np.where(x > 0, 0, x))', 'l3 quiz[2] swap option format')
txt, _ = run(xq + 'print(x[(x >= 0) & (x <= 4)])')
C(txt.strip() == '[3 4]', 'l3 quiz[3] explain: keeps 3 and 4')
raises('l3', 'quiz[3].widget.options[1].why', xq + 'x[x >= 0 & x <= 4]', 'ValueError')
raises('l3', 'quiz[3].widget.options[3].why', xq + 'x[0 <= x <= 4]', 'ValueError')

# ---------------------------------------------------------------- l4-broadcasting
R = np.array([[2.5, 2.5, 1.0], [2.0, -0.5, -1.5], [0.5, 2.0, 2.0], [1.0, 0.0, 0.5]])
m = R.mean(axis=0)
C(m.tolist() == [1.5, 1.0, 0.5], 'l4 screens[0] prose: m = [1.5, 1.0, 0.5]')
D = R - m
C(D.tolist() == [[1.0, 1.5, 0.5], [0.5, -1.5, -2.0], [-1.0, 1.0, 1.5], [-0.5, -1.0, 0.0]], 'l4 screens[1] canvas: R - m as drawn')
C(np.allclose(D.sum(axis=0), 0), 'l4 screens[1]: every column of R - m adds to 0')
E('l4', 'screens[2].widget.answer', float(D[1, 2]))
E('l4', 'screens[2].widget.wrong[0].value', float(R[1, 2] - m[1]))
E('l4', 'screens[2].widget.wrong[1].value', float(-D[1, 2]))
E('l4', 'screens[2].widget.wrong[2].value', float(R[1, 2]))
for shape, ok in [((3,), True), ((1, 3), True), ((4, 1), True), ((4,), False), ((3, 1), False), ((3, 4), False)]:
    try:
        R + np.ones(shape)
        res = True
    except ValueError:
        res = False
    C(res == ok, f'l4 screens[3]: shape {shape} {"adds" if ok else "fails"}')
c = R.mean(axis=1)
C(c.tolist() == [2.0, 0.0, 1.5, 0.5], 'l4 screens[4] canvas: day means 2.0, 0.0, 1.5, 0.5')
raises('l4', 'screens[4]', f'R = np.array({R.tolist()}); print(R - R.mean(axis=1))', 'ValueError')
X = R - R.mean(axis=1, keepdims=True)
E('l4', 'screens[5].widget.answer', float(X[0, 2]))
E('l4', 'screens[5].widget.wrong[0].value', float(R[0, 2] - m[2]))
E('l4', 'screens[5].widget.wrong[1].value', float(R[0, 2] - c[2]))
E('l4', 'screens[5].widget.wrong[2].value', float(R[0, 2]))
txt, _ = run('rng1 = np.random.default_rng(7)\nrng2 = np.random.default_rng(7)\nprint(rng1.normal() == rng2.normal())')
C(txt.strip() == 'True', 'l4 screens[6] prints True')
ser = {s['id']: s['values'] for s in lv.files['l4-broadcasting']['screens'][6]['canvas']['params']['series']}
for seed in (7, 8):
    path = np.concatenate([[100.0], 100 * np.cumprod(1 + np.random.default_rng(seed).normal(0, 0.01, 60))])
    C(np.allclose(np.round(path, 2), ser[f's{seed}'], atol=0.006), f'l4 screens[6] canvas: seed {seed} path is 100 then 100 * cumprod(1 + normal(0, 0.01, 60))',
      f'first {np.round(path[:4], 2)} vs {ser[f"s{seed}"][:4]}')
C((np.ones((5, 1)) + np.ones((1, 4))).shape == (5, 4), 'l4 screens[7]: (5, 4)')
# standardise test-1 feedback: "about 13% too big" without ddof=1; the test-1 data have n = 4, so ddof=0 values are sqrt(4/3) times
big = float(np.sqrt(4 / 3) - 1)
two('ddof=0 inflation, n = 4', float(((R - m) / R.std(axis=0))[0, 0] / ((R - m) / R.std(axis=0, ddof=1))[0, 0]) - 1, big)
lv.claim_text('l4', 'screens[8].feedback.byKey.test-1', 'about 13% too big', abs(big - 0.13) < 0.005,
              f'l4 screens[8] byKey.test-1: test-1 has n = 4, so ddof=0 values are {100 * big:.1f}% too big, not 13%')
C(np.allclose((np.array([[1.0], [3.0]]) - 2) / math.sqrt(2), [[-0.707107], [0.707107]], atol=1e-6), 'l4 screens[8] example: +-0.707107')
w42 = 100 * np.cumprod(1 + np.random.default_rng(42).normal(0.0, 0.01, 5))
E('l4', 'screens[9].feedback.byKey.test-1', round(float(w42[0]), 4))
prints('l4', 'quiz[0].widget.options[0].text', 'print((np.ones((3, 1)) * np.ones(4)).shape)')
prints('l4', 'quiz[1].widget.options[0].text', 'print(np.array([[1, 2], [3, 4]]) + np.array([10, 20]))')
raises('l4', 'quiz[2].widget.options[0]', 'A = np.ones((2, 3)); A + np.ones(2)', 'ValueError')
for s in [(3,), (2, 1), (1, 3)]:
    C((np.ones((2, 3)) + np.ones(s)).shape == (2, 3), f'l4 quiz[2]: A + ones{s} works')
rng = np.random.default_rng(1)
a, b = rng.integers(0, 10, 3), rng.integers(0, 10, 3)
C(a.tolist() == [4, 5, 7] and b.tolist() == [9, 0, 1], f'l4 quiz[3] explain: a = [4 5 7], b = [9 0 1]', f'got {a} {b}')
C(not (a == b).all(), 'l4 quiz[3] prints False')

# ---------------------------------------------------------------- review-1
prints('review', 'items[0].widget.options[0].text', 'prices = np.array([20.00, 25.00, 40.00]); print(prices / prices[0])')
prints('review', 'items[0].widget.options[1].text', 'prices = np.array([20.00, 25.00, 40.00]); print(prices[0] / prices)', 'review-1 items[0] flip option format')
p3 = np.array([50.00, 55.00, 44.00])
r3 = np.diff(p3) / p3[:-1]
E('review', 'items[1].widget.answer', round(float(r3[1]), 4))
two('-11/55', float(r3[1]), -11 / 55)
E('review', 'items[1].widget.wrong[0].value', -11 / 44)
E('review', 'items[1].widget.wrong[1].value', float(np.diff(p3)[1]))
E('review', 'items[1].widget.wrong[2].value', round(float(r3[0]), 4))
E('review', 'items[2].widget.answer', np.ones((252, 5)).std(axis=1, ddof=1).size)
E('review', 'items[2].widget.wrong[1].value', 252 * 5)
E('review', 'items[3].widget.answer', round(float(np.std([1.0, 3.0], ddof=1)), 4))
two('sqrt 2', float(np.std([1.0, 3.0], ddof=1)), math.sqrt(2))
E('review', 'items[3].widget.wrong[0].value', float(np.std([1.0, 3.0])))
E('review', 'items[3].widget.wrong[1].value', float(np.var([1.0, 3.0], ddof=1)))
xr = 'x = np.array([0.5, -0.3, 0.0, 1.2]); '
prints('review', 'items[4].widget.options[0].text', xr + 'print(x[x >= 0])')
prints('review', 'items[4].widget.options[2].text', xr + 'print(x >= 0)', 'review-1 items[4] mask option format')
E('review', 'items[5].widget.answer', round(float(np.where(np.array([0.5, -0.3, 0.0, 1.2]) < 0, 0.0, [0.5, -0.3, 0.0, 1.2]).sum()), 4))
E('review', 'items[5].widget.wrong[0].value', round(0.5 - 0.3 + 0.0 + 1.2, 4))
C((np.ones((6, 1)) - np.ones(4)).shape == (6, 4), 'review-1 items[6]: (6, 4)')
raises('review', 'items[7].widget.options[1].why', 'X = np.ones((100, 3)); X - X.mean(axis=1)', 'ValueError')
tot = float(np.cumprod(1 + np.array([0.10, -0.05, 0.02]))[-1] - 1)
E('review', 'items[8].widget.answer', round(tot, 4))
two('1.1 x 0.95 x 1.02 - 1', tot, 1.10 * 0.95 * 1.02 - 1)
E('review', 'items[8].widget.wrong[0].value', round(0.10 - 0.05 + 0.02, 4))
E('review', 'items[8].widget.wrong[1].value', round(tot + 1, 4))
cnt = (R > 0).sum(axis=0)
C(cnt.tolist() == [4, 2, 3], 'review-1 items[9] explain: [4 2 3]')
E('review', 'items[9].widget.answer', int(cnt[1]))
E('review', 'items[9].widget.wrong[0].value', int((R[:, 1] >= 0).sum()))
E('review', 'items[9].widget.wrong[1].value', int((R[1] > 0).sum()))
E('review', 'items[9].widget.wrong[2].value', int((R > 0).sum()))

# ---------------------------------------------------------------- homework-1
hp = np.array([250.00, 252.50, 247.45, 249.92, 254.92])
hr_ = hp[1:] / hp[:-1] - 1
vol = float(np.std(hr_, ddof=1) * np.sqrt(252))
E('homework', 'items[0].feedback.correct', round(100 * vol, 2))
E('homework', 'items[0].feedback.byKey.test-1', round(vol, 4), fmt='{:.4f}')
E('homework', 'items[0].feedback.byKey.test-1', round(float(np.std(hr_) * np.sqrt(252)), 3))   # 0.238
C(float(np.std(hr_, ddof=1) * 252) > 4, 'homework-1 items[0] byKey: using 252 gives above 4')
C(abs(max(1 - np.array([100, 120, 90, 110, 80, 130.0]) / np.maximum.accumulate([100, 120, 90, 110, 80, 130.0])) - 1 / 3) < 1e-12, 'homework-1 items[1]: drawdown 1/3')
C(np.maximum.accumulate([100, 120, 90]).tolist() == [100, 120, 120], 'homework-1 items[1] prose: running peak 100, 120, 120')
fp = 100 * np.prod(1 + np.random.default_rng(42).normal(0.0, 0.01, (3, 5)), axis=1)
C(np.allclose(np.round(fp, 4), [98.9776, 97.6547, 103.3589]), 'homework-1 items[2] example')
C(np.prod(np.ones((3, 5)), axis=0).size == 5, 'homework-1 items[2] byKey: axis=0 gives 5 numbers')
H = 'R = np.array([[1.0, 2.0], [3.0, 5.0]]); '
prints('homework', 'items[3].widget.options[0].text', H + 'print(R - R.mean(axis=1))')
prints('homework', 'items[3].widget.options[1].text', H + 'print(R - R.mean(axis=1, keepdims=True))', 'homework-1 items[3] meant option')
prints('homework', 'items[3].widget.options[3].text', H + 'print(R - R.mean(axis=0))', 'homework-1 items[3] cols option')
E('homework', 'items[3].widget.options[1].why', 4.0)
raises('homework', 'items[4]', 'prices = np.array([100, 101, 99]); prices *= 1.01', 'UFuncTypeError')
C(issubclass(np._core._exceptions._UFuncOutputCastingError, np._core._exceptions._UFuncNoLoopError.__mro__[1]) if hasattr(np, '_core') else True,
  'homework-1 items[4]: the cast error is a UFuncTypeError')
prints('homework', 'items[4].widget.options[1].text', 'prices = np.array([100, 101, 99]); prices = prices * 1.01; print("`prices` becomes", prices)', 'homework-1 items[4] new option format')
rb = np.array([0.012, -0.025, 0.004, 0.031, -0.008, -0.022, 0.001, 0.019])
E('homework', 'items[5].widget.answer', float((np.abs(rb) > 0.02).mean()))
two('3/8', float((np.abs(rb) > 0.02).mean()), 3 / 8)
E('homework', 'items[5].widget.wrong[0].value', float((rb > 0.02).mean()))
E('homework', 'items[5].widget.wrong[1].value', int((np.abs(rb) > 0.02).sum()))
E('homework', 'items[5].widget.wrong[2].value', float((rb < -0.02).mean()))
w, rw = np.array([0.5, 0.3, 0.2]), np.array([0.02, -0.01, 0.05])
two('weighted', float((w * rw).sum()), 0.010 - 0.003 + 0.010)
E('homework', 'items[6].widget.answer', round(float((w * rw).sum()), 4))
E('homework', 'items[6].widget.wrong[0].value', round(float(rw.mean()), 4))
E('homework', 'items[6].widget.wrong[1].value', round(float(rw.sum()), 4))
# longform h-debug-vol
raises('homework', 'items[7].model', 'prices = [250.00, 252.50, 247.45, 249.92, 254.92]; prices[1:] / prices[:-1]', 'TypeError', "unsupported operand type(s) for /: 'list' and 'list'")
for v_ in [0.01, -0.02, 0.009982, 0.020006]:
    C(np.isclose(np.round(hr_, 6), v_).any(), f'homework-1 items[7] model: return {v_}')
E('homework', 'items[7].model', round(float(hr_.mean()), 6))
E('homework', 'items[7].model', round(float(((hr_ - hr_.mean()) ** 2).sum()), 8))
E('homework', 'items[7].model', round(float(np.var(hr_, ddof=1)), 8), fmt='{:.8f}')
E('homework', 'items[7].model', round(float(np.std(hr_, ddof=1)), 6))
E('homework', 'items[7].model', round(vol, 4), fmt='{:.4f}')
E('homework', 'items[7].model', round(float(np.std(hr_)), 6), fmt='{:.6f}')
E('homework', 'items[7].model', round(float(np.std(hr_) * 252), 2))
E('homework', 'items[7].model', round(math.sqrt(4 / 3), 3))
E('homework', 'items[7].model', round(math.sqrt(252), 2))

lv.check_wrongs()
lv.report()
