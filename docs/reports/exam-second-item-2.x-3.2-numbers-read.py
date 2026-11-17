"""Second read of the new exam items of exam second item 2.x-3.2 (topics 3.2, 2.1, 2.3, 2.6).
Every key, wrong value and printed number is recomputed by a method other than the author's
(exact fractions, substitution into the PDE, RK4, a survival-function integral, brute force).
Exit 0 always; a failing check prints a line starting FINDING. The last block recomputes the
numbers after the fix pass."""
import json, math, os, re, sys
from fractions import Fraction as Fr
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CON = os.path.join(ROOT, 'app', 'content')
findings = 0


def load(*p):
    return json.load(open(os.path.join(CON, *p)))


def item(exam, iid):
    return next(it for it in load('exams', exam + '.json')['items'] if it['id'] == iid)


def check(ok, label):
    global findings
    if ok:
        print('ok      ' + label)
    else:
        findings += 1
        print('FINDING ' + label)


def band(w, exact, label, dp=None):
    """Key within tol of the exact value; every wrong value outside the key band and bands disjoint;
    the exact value is not on a rounding tie at dp places."""
    tol = w['tol']['abs']
    check(abs(w['answer'] - exact) <= tol * 0.5 + 1e-12, f'{label}: key {w["answer"]} against {exact:.6f}')
    for x in w.get('wrong', []):
        check(abs(x['value'] - w['answer']) > tol + x['tol']['abs'], f'{label}: wrong {x["id"]} {x["value"]} outside the key band')
    ws = w.get('wrong', [])
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            check(abs(ws[i]['value'] - ws[j]['value']) > ws[i]['tol']['abs'] + ws[j]['tol']['abs'], f'{label}: wrong bands {ws[i]["id"]} and {ws[j]["id"]} apart')
    if dp is not None:
        check(not_tie(exact, dp), f'{label}: {exact:.7f} is not on a rounding tie at {dp} dp')
        check(abs(round(exact, dp) - w['answer']) <= tol, f'{label}: the value printed to {dp} dp is accepted')


def not_tie(v, dp):
    f = abs(v) * 10 ** dp
    return abs(f - math.floor(f) - 0.5) > 1e-3


def wrong(w, wid, exact, label, dp=None):
    x = next(x for x in w['wrong'] if x['id'] == wid)
    check(abs(x['value'] - exact) <= x['tol']['abs'] * 0.5 + 1e-12, f'{label}: wrong {wid} {x["value"]} against {exact:.6f}')
    if dp is not None:
        check(not_tie(exact, dp), f'{label}: slip {wid} {exact:.7f} not on a tie at {dp} dp')


def text_of(o):
    if isinstance(o, dict):
        return ' '.join(text_of(v) for v in o.values())
    if isinstance(o, list):
        return ' '.join(text_of(v) for v in o)
    return o if isinstance(o, str) else ''


Phi = lambda z: 0.5 * math.erfc(-z / math.sqrt(2))


def emax(N, h=1e-3, L=12.0):
    """E[max of N standard normals] = int_0^inf (1 - Phi^N) dz - int_-inf^0 Phi^N dz (trapezium rule)."""
    n = int(L / h)
    up = sum((1 - Phi(k * h) ** N) * (0.5 if k in (0, n) else 1) for k in range(n + 1)) * h
    dn = sum((Phi(-k * h) ** N) * (0.5 if k in (0, n) else 1) for k in range(n + 1)) * h
    return up - dn


# ---------- skills: every listed pair has two auto items, no skill fell to one, removals ----------
def auto(it):
    L = lambda w: bool(w) and w.get('kind') == 'longform'
    return not (it.get('kind') == 'longform' or L(it.get('widget')) or any(L(p.get('widget')) for p in it.get('parts', [])))


PAIRS = {'topic-3.2': ['pe-bs', 'pe-fk', 'pe-fd'], 'topic-2.1': ['en-interpret'], 'topic-2.3': ['bt-report'], 'topic-2.6': ['sm-hier']}
REMOVED = {'topic-3.2': {'e-drift-t2w2': ['it-calculus'], 'e-gbm-below': ['it-bm']}, 'topic-2.1': {'e-odds-update': ['sl-classify']},
           'topic-2.3': {'e-impact-double': ['bt-execution']}, 'topic-2.6': {}}
NEW = {'topic-3.2': ['e-heat-grid-steps', 'e-fk-reverting'], 'topic-2.1': ['e-pd-two-trees'], 'topic-2.3': ['e-honest-bar'], 'topic-2.6': ['e-two-fund-shrink']}
SHAPE = {'topic-3.2': (30, 90), 'topic-2.1': (30, 90), 'topic-2.3': (30, 90), 'topic-2.6': (26, 80)}
for ex in PAIRS:
    d = load('exams', ex + '.json')
    cnt = Counter(s for it in d['items'] if auto(it) for s in it.get('skills', []))
    ids = {it['id'] for it in d['items']}
    check((len(d['items']), d['minutes']) == SHAPE[ex], f'{ex}: {len(d["items"])} items, {d["minutes"]} minutes')
    check(all(i in ids for i in NEW[ex]) and not any(i in ids for i in REMOVED[ex]), f'{ex}: new items present, removed items gone')
    for s in PAIRS[ex]:
        check(cnt[s] >= 2, f'{ex}: listed skill {s} has {cnt[s]} auto items')
    for rid, sk in REMOVED[ex].items():
        for s in sk:
            check(cnt[s] >= 2, f'{ex}: removed {rid}, its skill {s} keeps {cnt[s]} auto items')
    low = [s for s, n in cnt.items() if n < 2]
    check(not low, f'{ex}: no skill on one auto item (lowest {min(cnt.values())}) {low}')
    # essential skills of every level of the topic: the skills on its review's items
    for cdir in sorted(os.listdir(os.path.join(CON, 'courses'))):
        cj = os.path.join(CON, 'courses', cdir, 'course.json')
        if not os.path.exists(cj) or str(json.load(open(cj)).get('topic')) != str(d['topic']):
            continue
        for lv in json.load(open(cj))['levels']:
            rv = os.path.join(CON, 'courses', cdir, str(lv.get('review')) + '.json')
            if not os.path.exists(rv):
                continue
            ess = {s for it in json.load(open(rv)).get('items', []) for s in it.get('skills', [])}
            one = sorted(s for s in ess if cnt[s] == 1)
            check(not one, f'{ex}: {cdir}/L{lv["n"]} essential skills on one auto item: {one}')
check(5 * round(Fr(75 * 26, 25) / 5) == 80, 'topic-2.6 minutes: 75 x 26/25 = 78, to the nearest 5 is 80')

# ---------- topic-3.2 e-heat-grid-steps (two parts after the fix pass) ----------
it = item('topic-3.2', 'e-heat-grid-steps'); w1, w = it['parts'][0]['widget'], it['parts'][1]['widget']
check('widget' not in it and len(it['parts']) == 2, 'heat-grid: two parts, no top-level widget')
sig, T, dx = Fr(35, 100), Fr(6, 10), Fr(4, 100)
tau = sig * sig * T / 2
check(tau == Fr(3675, 100000), f'heat time {float(tau)} = 0.03675')
check(dx * dx / 2 == Fr(8, 10000) and dx * dx == Fr(16, 10000) and sig * sig == Fr(1225, 10000), 'printed 0.0008, 0.0016, 0.1225')
check('0.03675' in it['parts'][1]['question'], 'heat-grid: part 2 prints the heat time')
band(w1, float(tau), 'heat-grid part 1', 5)
for wid, v in (('no-half', sig * sig * T), ('sigma-unsquared', sig * T / 2), ('calendar', T)):
    wrong(w1, wid, float(v), 'heat-grid part 1')
steps = math.ceil(tau / (dx * dx / 2))          # exact ceiling of a fraction
check(steps == 46 == w['answer'] and w['tol']['abs'] == 0, f'fewest steps {steps}')
check(round(float(tau / (dx * dx / 2)), 2) == 45.94, 'ratio prints 45.94')
check(round(float(tau / 46 / dx ** 2), 4) == 0.4993 and round(float(tau / 45 / dx ** 2), 4) == 0.5104, 'lambda 0.4993 at 46 steps, 0.5104 at 45')
check(tau / 46 / dx ** 2 <= Fr(1, 2) < tau / 45 / dx ** 2, '46 is stable and 45 is not, exactly')
check(sig * sig * T == Fr(735, 10000) and sig * T / 2 == Fr(105, 1000), 'printed 0.0735 and 0.105')
for wid, v in (('lambda-one', math.ceil(tau / (dx * dx))), ('round-down', math.floor(tau / (dx * dx / 2)))):
    wrong(w, wid, v, 'heat-grid part 2')
band(w, 46, 'heat-grid part 2')
# two-skill strictness: each listed slip alone now costs a part; the double slip scores nothing
double = math.ceil(sig * sig * T / (dx * dx))
check(double == w['answer'] and abs(float(sig * sig * T) - w1['answer']) > w1['tol']['abs'] and abs(math.ceil(tau / (dx * dx)) - w['answer']) > 0,
      f'heat-grid: the double slip would give {double} in one number, but as two parts the tau slip fails part 1 and the lambda slip fails part 2')
check(any('no-half' == x['id'] for x in w1['wrong']) and any('lambda-one' == x['id'] for x in w['wrong']), 'heat-grid: one slip per skill, each in its own part')

# ---------- topic-3.2 e-fk-reverting ----------
it = item('topic-3.2', 'e-fk-reverting'); w = it['widget']
kap, th, x0, Tm, r, half = 0.3, 3.0, 1.0, 2.0, 0.04, 0.08
V = lambda t, x: math.exp(-r * (Tm - t)) * (th + (x - th) * math.exp(-kap * (Tm - t)))      # candidate solution
# substitution into V_t + 0.3(3 - x)V_x + 0.08 V_xx - 0.04 V = 0 by central differences, and the end condition
res = 0.0
for (t, x) in ((0.0, 1.0), (0.7, 2.2), (1.5, -0.4), (1.9, 4.0)):
    e = 1e-4
    Vt = (V(t + e, x) - V(t - e, x)) / (2 * e); Vx = (V(t, x + e) - V(t, x - e)) / (2 * e)
    Vxx = (V(t, x + e) - 2 * V(t, x) + V(t, x - e)) / e ** 2
    res = max(res, abs(Vt + kap * (th - x) * Vx + half * Vxx - r * V(t, x)))
check(res < 1e-6 and abs(V(Tm, 1.7) - 1.7) < 1e-12, f'fk: the closed form solves the printed PDE (residual {res:.1e}) and V(T, x) = x')
# the mean by RK4 on m' = 0.3(3 - m)
m, n = x0, 2000; h = Tm / n; f = lambda y: kap * (th - y)
for _ in range(n):
    k1 = f(m); k2 = f(m + h * k1 / 2); k3 = f(m + h * k2 / 2); k4 = f(m + h * k3); m += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
disc = math.exp(-r * Tm)
check(abs(m * disc - V(0, 1)) < 1e-10 and round(m, 4) == 1.9024 and round(V(0, 1), 4) == 1.7561, f'fk: mean {m:.6f}, value {V(0, 1):.6f}')
check(abs(math.sqrt(2 * half) - 0.4) < 1e-12 and abs(kap * (th - x0) - 0.6) < 1e-12 and abs(r * Tm - 0.08) < 1e-12, 'fk: sigma 0.4, starting drift 0.6, exponent 0.08')
band(w, V(0, 1), 'fk', 4)
for wid, v in (('no-discount', m), ('straight-line-drift', disc * (x0 + 0.6 * Tm)), ('no-drift', disc * x0), ('level-reached', disc * th)):
    wrong(w, wid, v, 'fk', 4)

# ---------- topic-2.1 e-pd-two-trees ----------
it = item('topic-2.1', 'e-pd-two-trees'); w = it['widget']
lines = it['canvas']['params']['lines']
rows = [tuple(float(v) for v in l.split()[1:]) for l in lines if re.match(r'^\d', l)]
check(rows == [(0.2, 0.4), (1.1, 1.6), (-0.6, 0.3), (0.9, 1.3)], f'pd: rows read from the console {rows}')
leaf = [float(l.split('->')[1]) for l in lines if '->' in l]
check(leaf == [3.0, 2.0, -1.0, 4.0, 1.0, 0.0] and 'volume_z > 0.5' in lines[0] and 'gap_z > 1' in lines[1] and 'gap_z > 1' in lines[3] and 'volume_z > 0.5' in lines[4], 'pd: trees read from the console')


def tree1(v, z):
    if v > 0.5: return leaf[0]
    return leaf[1] if z > 1 else leaf[2]


def tree2(v, z):
    if z > 1: return leaf[3]
    return leaf[4] if v > 0.5 else leaf[5]


table = {v: [Fr(tree1(v, z) + tree2(v, z)) / 2 for _, z in rows] for v in (0, 1)}
check([float(x) for x in table[1]] == [2, 3.5, 2, 3.5] and [float(x) for x in table[0]] == [-0.5, 3, -0.5, 3], 'pd: forecasts 2, 3.5, 2, 3.5 and -0.5, 3, -0.5, 3')
pd1, pd0 = sum(table[1]) / 4, sum(table[0]) / 4
check(pd1 == Fr(11, 4) and pd0 == Fr(5, 4) and pd1 - pd0 == Fr(3, 2), 'pd: 2.75, 1.25, rise 1.5')
asis = [Fr(tree1(v, z) + tree2(v, z)) / 2 for v, z in rows]
hi = [a for a, (v, _) in zip(asis, rows) if v > 0.5]; lo = [a for a, (v, _) in zip(asis, rows) if v <= 0.5]
band(w, 1.5, 'pd', 1)
wrong(w, 'conditional-means', float(sum(hi) / len(hi) - sum(lo) / len(lo)), 'pd')
wrong(w, 'one-tree', sum(tree1(1, z) - tree1(0, z) for _, z in rows) / 4, 'pd')
wrong(w, 'summed', float(2 * (pd1 - pd0)), 'pd')
check(all(tree2(v, z) == 4.0 for v, z in rows if z > 1) and [i + 1 for i, (_, z) in enumerate(rows) if z > 1] == [2, 4], 'pd: rows 2 and 4 have high gap_z and get 4.0 from tree 2')
check(w.get('unit') == 'bp', 'pd: unit bp')
kmeans = item('topic-2.1', 'e-kmeans-spreads')
check(not ('bid-ask' in kmeans['prose'] and 'bid-ask' in it['prose']), 'pd: the story (bond bid-ask spreads in bp) is also the story of e-kmeans-spreads on the same paper')

# ---------- topic-2.3 e-honest-bar (five contracts by 12 settings, sd 0.39) ----------
it = item('topic-2.3', 'e-honest-bar'); w = it['parts'][0]['widget']
e12, e60 = emax(12), emax(60)
check(round(e12, 3) == 1.629 and round(e60, 3) == 2.319, f'bar: E[max] of 12 is {e12:.5f}, of 60 is {e60:.5f}')
check('1.629' in it['prose'] and '2.319' in it['prose'] and 'By integration' in it['prose'] and '0.39' in it['prose'], 'bar: both tail values printed, with their source, and sd 0.39')
check(5 * 12 == 60, 'bar: 5 contracts x 12 settings = 60')
bar = 0.39 * e60
band(w, bar, 'bar', 2)
check(round(bar, 2) == 0.90 and round(0.39 * 2.319, 2) == 0.90 and abs(0.39 * 2.319 - w['answer']) <= w['tol']['abs'], 'bar: 0.39 x 2.319 = 0.90, the printed route is accepted')
wrong(w, 'one-contract', 0.39 * e12, 'bar', 2); wrong(w, 'no-scale', e60, 'bar')
check(round(0.39 * e12, 2) == 0.64 and round(0.39 * 1.629, 2) == 0.64, 'bar: one-contract bar 0.64')
check(0.39 * e12 < 0.84 < bar, 'bar: 0.84 is below the honest bar and above the one-contract bar')
check([o['id'] for o in it['parts'][1]['widget']['options'] if o.get('correct')] == ['a'], 'bar: choice key a')
txt = text_of(it)
check('0.90' in txt and '0.64' in txt and '0.88' not in txt and '0.74' not in txt, 'bar: printed bars 0.90 and 0.64 only')
l15 = load('courses', 'backtest', 'l15-how-many-settings.json')['screens'][6]['prose']
check('dropped settings' not in txt and 'dropped setting' not in txt and 'futures' not in l15, 'bar: no dropped-settings story, a search across contracts')

# ---------- topic-2.6 e-two-fund-shrink (forecasters, mu 2, tau 2.5, in bp) ----------
it = item('topic-2.6', 'e-two-fund-shrink'); pa, pb = it['parts'][0]['widget'], it['parts'][1]['widget']


def post(mu, tau, a, s):
    """Posterior mean and shrink factor by exact precision weighting."""
    mu, tau, a, s = Fr(mu), Fr(tau), Fr(a), Fr(s)
    return (mu / tau ** 2 + a / s ** 2) / (1 / tau ** 2 + 1 / s ** 2), s ** 2 / (s ** 2 + tau ** 2)


A, BA = post(2, '2.5', 11, '7.5'); B, BB = post(2, '2.5', 6, 1)
check(BA == Fr(9, 10) and A == Fr(29, 10), f'shrink A: B_A {float(BA)}, error {float(A)} bp')
check(round(float(BB), 4) == 0.1379 and round(float(1 - BB), 4) == 0.8621 and round(float(B), 2) == 5.45 and abs(float(B) - 5.4483) < 5e-5, f'shrink B: B_B {float(BB):.6f}, error {float(B):.6f} bp')
check(Fr('7.5') ** 2 == Fr('56.25') and Fr('2.5') ** 2 == Fr('6.25') and Fr('56.25') + Fr('6.25') == Fr('62.5') and 1 + Fr('6.25') == Fr('7.25'), 'shrink: printed 56.25, 6.25, 62.5, 7.25')
check(abs(2 + 0.8621 * 4 - 5.45) < 0.005, 'shrink: 2 + 0.8621 x 4 = 5.45')
band(pa, float(A), 'shrink A', 1); band(pb, float(B), 'shrink B', 2)
check(pa.get('unit') == 'bp' and pb.get('unit') == 'bp', 'shrink: unit bp')
for wdg, a, s, Bf, tag in ((pa, 11, Fr('7.5'), BA, 'A'), (pb, 6, Fr(1), BB, 'B')):
    wrong(wdg, 'raw', a, 'shrink ' + tag)
    wrong(wdg, 'inverted', float(2 + Bf * (a - 2)), 'shrink ' + tag, 2)
    wrong(wdg, 'se-not-squared', float(2 + (1 - s / (s + Fr('2.5'))) * (a - 2)), 'shrink ' + tag, 2)
check(B > A and Fr(4, 5) < 1 - BB < Fr(9, 10), 'shrink: B ends above A; B keeps over four fifths of its gap')
r4 = next(i for i in load('courses', 'stat-models', 'review-4.json')['items'] if i['id'] == 'r4-shrink')
check('9%' not in text_of({k: v for k, v in it.items() if k != 'id'}) and 'fund' not in text_of({k: v for k, v in it.items() if k != 'id'}).lower(), 'shrink: no fund story, no 9% alpha (r4-shrink)')

print('findings:', findings)
sys.exit(0)
