"""Recompute every number in alpha homework-4 item h-neutral-book (performance task, code).

Run from the repo root with a Python that has pandas 2.2 (the scratchpad venv):
    <venv>/bin/python docs/reports/alpha-4-perf-numbers.py      exits 0 when every check passes.
Route A is the item's own `solution` (median, clip, per-side division, shift).
Route B is an independent loop in this file: a hand-sorted median, side sums and a P&L
added up share by share in plain Python. Every test expectation must equal both routes.
The starter must fail every test, and each planted bug must fail a hidden test that is
not a timing test (there is none), with the byKey line named beside it where one exists.
"""
import json, math, os, sys
try:
    import pandas as pd  # noqa: F401
except ImportError:
    sys.exit('needs pandas: run with the venv named in docs/reports/alpha-4-perf.md')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/alpha/homework-4.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-neutral-book')
w = item['widget']
fails = []

def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

REF = '''import math
import pandas as pd
def split_book(signal, gross):
    out = []
    for row in signal.values.tolist():
        have = sorted(x for x in row if not math.isnan(x))
        k = len(have)
        med = have[k // 2] if k % 2 else (have[k // 2 - 1] + have[k // 2]) / 2
        dist = [0.0 if math.isnan(x) else x - med for x in row]
        L = sum(x for x in dist if x > 0)
        S = sum(-x for x in dist if x < 0)
        if L == 0 or S == 0:
            out.append([0.0] * len(row))
            continue
        out.append([gross / 2 * (x / L if x > 0 else x / S if x < 0 else 0.0) for x in dist])
    return pd.DataFrame(out, index=signal.index, columns=signal.columns)
def split_pnl(signal, ret, gross):
    P = split_book(signal, gross).values.tolist()
    Rv = ret.values.tolist()
    pnl = []
    for t in range(1, len(Rv)):
        pnl.append(sum(P[t - 1][j] * (0.0 if math.isnan(r) else r) for j, r in enumerate(Rv[t])))
    return pd.Series(pnl, index=signal.index[1:])
'''

SOL = w['solution']
def variant(*pairs):
    s = SOL
    for old, new in pairs:
        assert old in s, old
        s = s.replace(old, new)
    return s

W_LINE = 'w = up.div(longs.where(both), axis=0) + down.div(shorts.where(both), axis=0)'
BUGS = {
    'one scale for the whole book': (variant((W_LINE, 'w = 2 * d.div((longs + shorts).where(both), axis=0)')), 'test-1'),
    'each side scaled to the whole gross': (variant(('(w * gross / 2)', '(w * gross)')), 'test-1'),
    'mean, not median': (variant(('signal.median(axis=1)', 'signal.mean(axis=1)')), 'test-2'),
    'rank weights as in the lesson': (variant(('d = signal.sub(signal.median(axis=1), axis=0)',
        'r = signal.rank(axis=1); d = r.sub(r.median(axis=1), axis=0)')), 'test-2'),
    'ties split by order': (variant(('d = signal.sub(signal.median(axis=1), axis=0)',
        'r = signal.rank(axis=1, method="first"); d = r.sub(r.median(axis=1), axis=0)')), 'test-2'),
    'median down each column': (variant(('signal.sub(signal.median(axis=1), axis=0)', 'signal - signal.median()')), 'test-2'),
    'missing signal counted as 0': (variant(('d = signal.sub(', 'signal = signal.fillna(0.0)\n    d = signal.sub(')), 'test-3'),
    'one-sided book when a side is empty': (variant((W_LINE, 'w = up.div(longs.where(longs > 0), axis=0).fillna(0.0) + down.div(shorts.where(shorts > 0), axis=0).fillna(0.0)')), 'test-4'),
    'empty side left as NaN or inf': (variant((W_LINE, 'w = up.div(longs, axis=0) + down.div(shorts, axis=0)'),
        ('(w * gross / 2).fillna(0.0)', '(w * gross / 2).where(signal.notna(), 0.0)')), 'test-4'),
    'no-signal shares left NaN': (variant(('(w * gross / 2).fillna(0.0)', '(w * gross / 2).mask(~both, 0.0)')), 'test-3'),
    'same-day signal (no shift)': (variant(('.shift(1)          #', '                   #')), 'test-7'),
    'shift the wrong way': (variant(('.shift(1)', '.shift(-1)')), 'test-7'),
    'returns moved back, P&L dated at the close it was set': (variant(('held = split_book(signal, gross).shift(1)', 'held = split_book(signal, gross)'),
        ('(held * ret.fillna(0.0)).sum(axis=1).iloc[1:]', '(held * ret.shift(-1).fillna(0.0)).sum(axis=1).iloc[:-1]')), 'test-8'),
    'P&L kept on the first date': (variant(('.sum(axis=1).iloc[1:]', '.sum(axis=1)')), 'test-8'),
    'NaN return spoils the day (NumPy product)': (variant(('return (held * ret.fillna(0.0)).sum(axis=1).iloc[1:]',
        'return pd.Series((held.values * ret.values).sum(axis=1), index=ret.index).iloc[1:]')), 'test-9'),
}

def flat(v):
    if hasattr(v, 'tolist'):
        v = v.tolist()
    if isinstance(v, (list, tuple)):
        out = []
        for a in v:
            out.extend(flat(a))
        return out
    return [v]

def same(got, t, ns):
    exp = eval(t['expect'], ns)
    if t['compare'] == 'equal':
        return got == exp
    g, e = flat(got), flat(exp)
    tol = t['tol']['abs']
    return len(g) == len(e) and all(isinstance(a, (int, float)) and not math.isnan(a)
                                    and abs(a - b) <= tol + 1e-9 for a, b in zip(g, e))

def run_tests(code, cases=None):
    res = []
    for t in (cases or w['tests']):
        ns = {}
        try:
            exec(w['prelude'], ns)
            exec(code, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            res.append(bool(same(eval(t['call'], ns), t, ns)))
        except Exception as e:
            res.append(type(e).__name__)
    return res

for name, code in (('A solution', SOL), ('B plain loop', REF)):
    r = run_tests(code)
    check(f'{name} passes all {len(r)} tests', all(x is True for x in r), str(r))
    check(f'{name} passes the example', run_tests(code, w['examples']) == [True])

r = run_tests(w['starter'])
check('starter fails every test', all(x is not True for x in r), str(r))

for name, (code, key) in BUGS.items():
    r = run_tests(code)
    bad = [i + 1 for i, x in enumerate(r) if x is not True]
    check(f'bug "{name}" caught', bool(bad), f'fails tests {bad}')
    check(f'bug "{name}" first fails {key}', bool(bad) and bad[0] == int(key[5:]))
    check(f'byKey {key} present', key in item['feedback']['byKey'])

# figures stated in the item and the explain text, each by both routes
nsA, nsB = {}, {}
exec(w['prelude'], nsA); exec(SOL, nsA)
exec(w['prelude'], nsB); exec(REF, nsB)
S, R = nsA['five_days']()
check('five_days(): six shares, 4 to 8 March 2024', S.shape == (5, 6) and str(S.index[0].date()) == '2024-03-04'
      and str(S.index[-1].date()) == '2024-03-08' and list(S.columns) == list('ABCDEF'))
row = S.iloc[0].tolist()
med = sorted(row)[2] / 2 + sorted(row)[3] / 2
above = sum(x - med for x in row if x > med); below = sum(med - x for x in row if x < med)
check('4 March: distances above the median add to 1.1', abs(above - 1.1) < 1e-12, f'{above}')
check('4 March: distances below the median add to 1.3', abs(below - 1.3) < 1e-12, f'{below}')
d = S.iloc[0] - S.iloc[0].median()
net = float(d.sum() / d.abs().sum() * 1_000_000)
net_b = (above - below) / (above + below) * 1_000_000
check('one scale for the whole book: £83,333 net short', round(net) == round(net_b) == -83333, f'{net:.2f} {net_b:.2f}')
PA = nsA['split_book'](S, 1_000_000); PB = nsB['split_book'](S, 1_000_000)
for P in (PA, PB):
    check('4 March sides £500,000 and -£500,000', abs(P.iloc[0].clip(lower=0).sum() - 5e5) < 1e-6 and abs(P.iloc[0].clip(upper=0).sum() + 5e5) < 1e-6)
mar6 = S.loc['2024-03-06']
check('6 March: five shares tie at the median, only C below', (mar6 == mar6.median()).sum() == 5 and list(mar6[mar6 < mar6.median()].index) == ['C'])
check('5 March: B has no signal', list(S.loc['2024-03-05'][S.loc['2024-03-05'].isna()].index) == ['B'])
check('8 March: F did not trade', list(R.loc['2024-03-08'][R.loc['2024-03-08'].isna()].index) == ['F'])
pA = nsA['split_pnl'](S, R, 1e6); pB = nsB['split_pnl'](S, R, 1e6)
check('8 March P&L agrees by both routes (4,051.72)', abs(pA.iloc[-1] - pB.iloc[-1]) < 1e-9 and round(pA.iloc[-1], 2) == 4051.72, f'{pA.iloc[-1]:.4f}')
S7, R7 = nsA['panel'](7)
check('panel(7): 30 shares over 40 days', S7.shape == (40, 30) and R7.shape == (40, 30))
check('panel(7) has missing signals, ties and missing returns',
      S7.isna().sum().sum() > 0 and R7.isna().sum().sum() > 0 and any(r.dropna().duplicated().any() for _, r in S7.drop(S7.index[[12, 25]]).iterrows()))
n_t, n_e = len(w['tests']), len(w['examples'])
check('tests 12, examples 1, tests > examples', (n_t, n_e) == (12, 1) and n_t > n_e)
check('how states the test count', f'runs {n_t} hidden tests' in w['how'])
check('homework items within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('one performance item in the homework', sum(1 for i in doc['items'] if i.get('performance')) == 1)

print(f'\n{len(fails)} failures')
sys.exit(1 if fails else 0)
