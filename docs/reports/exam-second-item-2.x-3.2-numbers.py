"""Recompute every key, wrong value and printed number of the new exam items (exam second item, 2.x-3.2).
Each figure is worked two ways where a second way exists. Exit 0 when every check holds."""
import json, math, os, sys
from scipy import stats, integrate

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EX = os.path.join(ROOT, 'app', 'content', 'exams')
fails = 0

def item(exam, iid):
    d = json.load(open(os.path.join(EX, exam + '.json')))
    return next(it for it in d['items'] if it['id'] == iid)

def check(ok, label):
    global fails
    print(('ok   ' if ok else 'FAIL ') + label)
    if not ok: fails += 1

def close(a, b, t=1e-9): return abs(a - b) <= t

def key_and_wrongs(w, key, wrongs, label):
    check(close(w['answer'], key, w['tol']['abs'] + 1e-12), f'{label} key {w["answer"]} ~ {key}')
    got = {x['id']: x for x in w['wrong']}
    check(set(got) == set(wrongs), f'{label} wrong ids {sorted(got)}')
    for k, v in wrongs.items():
        x = got[k]
        check(close(x['value'], v, x['tol']['abs'] + 1e-12), f'{label} wrong {k} {x["value"]} ~ {v}')
        check(abs(x['value'] - w['answer']) > w['tol']['abs'] + x['tol']['abs'], f'{label} wrong {k} outside the key band')

# topic-3.2 e-heat-grid-steps: heat time tau = sigma^2 T / 2, explicit cap dtau <= dx^2 / 2
s, T, dx = 0.35, 0.6, 0.04
tau = 0.5 * s ** 2 * T
tau2 = s * s * T / 2                          # second way
cap = dx ** 2 / 2
steps = math.ceil(tau / cap - 1e-12)
steps2 = next(n for n in range(1, 1000) if (tau2 / n) / dx ** 2 <= 0.5)   # search for the first stable count
check(close(tau, 0.03675) and close(tau2, 0.03675), 'heat tau 0.03675')
check(close(cap, 0.0008), 'cap 0.0008')
check(round(tau / cap, 2) == 45.94, 'ratio 45.94')
check(steps == steps2 == 46, 'steps 46')
check(round(tau / 46 / dx ** 2, 4) == 0.4993, 'lambda at 46 is 0.4993')
check(round(tau / 45 / dx ** 2, 4) == 0.5104, 'lambda at 45 is 0.5104')
check(close(s * s * T, 0.0735) and close(0.5 * s * T, 0.105) and close(s * s, 0.1225) and close(dx * dx, 0.0016), 'printed 0.0735, 0.105, 0.1225, 0.0016')
it = item('topic-3.2', 'e-heat-grid-steps')
check('widget' not in it and len(it['parts']) == 2, 'heat-grid: two parts')
key_and_wrongs(it['parts'][0]['widget'], tau, {'no-half': s * s * T, 'sigma-unsquared': s * T / 2, 'calendar': T}, 'heat-grid part 1')
key_and_wrongs(it['parts'][1]['widget'], steps, {
    'lambda-one': math.ceil(tau / dx ** 2),
    'round-down': math.floor(tau / cap)}, 'heat-grid part 2')
check(it['parts'][0]['widget']['answer'] == 0.03675 and '0.03675' in it['parts'][1]['question'], 'heat-grid: part 2 prints the part 1 key')

# topic-3.2 e-fk-reverting: dX = 0.3(3 - X) dt + 0.4 dW, V = e^{-0.04 * 2} E[X_2], payoff x
k, th, x0, t, r = 0.3, 3.0, 1.0, 2.0, 0.04
m = th + (x0 - th) * math.exp(-k * t)
# second way: integrate the mean ODE m' = k (th - m) by small steps
mm, h = x0, 1e-5
for _ in range(int(t / h)): mm += k * (th - mm) * h
check(abs(m - mm) < 1e-4, f'mean {m:.6f} by formula and by steps {mm:.6f}')
check(close(math.sqrt(2 * 0.08), 0.4), 'sigma 0.4 from 0.08 V_xx')
V = math.exp(-r * t) * m
check(round(m, 4) == 1.9024 and round(V, 4) == 1.7561, f'mean 1.9024, V 1.7561 ({V:.6f})')
check(close(k * (th - x0), 0.6), 'starting drift 0.6 a year')
it = item('topic-3.2', 'e-fk-reverting')
key_and_wrongs(it['widget'], V, {
    'no-discount': m,
    'straight-line-drift': math.exp(-r * t) * (x0 + k * (th - x0) * t),
    'no-drift': math.exp(-r * t) * x0,
    'level-reached': math.exp(-r * t) * th}, 'fk-reverting')

# topic-2.1 e-pd-two-trees: partial dependence of a two-tree average
t1 = lambda v, z: 3.0 if v > 0.5 else (2.0 if z > 1 else -1.0)
t2 = lambda v, z: 4.0 if z > 1 else (1.0 if v > 0.5 else 0.0)
rows = [(0.2, 0.4), (1.1, 1.6), (-0.6, 0.3), (0.9, 1.3)]
f = lambda v, z: (t1(v, z) + t2(v, z)) / 2
pd = lambda val, g=f: sum(g(val, z) for _, z in rows) / len(rows)
hi = [f(v, z) for v, z in rows if v > 0.5]; lo = [f(v, z) for v, z in rows if v <= 0.5]
check([f(1.0, z) for _, z in rows] == [2, 3.5, 2, 3.5] and pd(1.0) == 2.75, 'forecasts at 1: 2, 3.5, 2, 3.5, mean 2.75')
check([f(0.0, z) for _, z in rows] == [-0.5, 3, -0.5, 3] and pd(0.0) == 1.25, 'forecasts at 0: -0.5, 3, -0.5, 3, mean 1.25')
# second way: the trees split only at volume_z 0.5, so any value above (0.7) and below (0.3) gives the same rise
check(pd(0.7) - pd(0.3) == pd(1.0) - pd(0.0) == 1.5, 'rise 1.5')
check(all(t2(v, z) == 4.0 for v, z in rows if z > 1), 'tree 2 gives 4.0 to the high vol_z rows')
it = item('topic-2.1', 'e-pd-two-trees')
key_and_wrongs(it['widget'], 1.5, {
    'conditional-means': sum(hi) / len(hi) - sum(lo) / len(lo),
    'one-tree': pd(1.0, t1) - pd(0.0, t1),
    'summed': 2 * (pd(1.0) - pd(0.0))}, 'pd-trees')
check(close(sum(hi) / len(hi) - sum(lo) / len(lo), 4.0), 'conditional gap 4.0')

# topic-2.3 e-honest-bar: five contracts x 12 settings = 60 runs, sd 0.39; expected best by integration
def emax(N):
    return integrate.quad(lambda z: z * N * stats.norm.pdf(z) * stats.norm.cdf(z) ** (N - 1), -12, 12, limit=200)[0]
import numpy as np
rng = np.random.default_rng(7)
for N, printed in ((12, 1.629), (60, 2.319)):
    e = emax(N); sim = rng.standard_normal((200000, N)).max(axis=1).mean()
    check(round(e, 3) == printed and abs(sim - e) < 0.01, f'E[max of {N}] {e:.4f} (simulated {sim:.4f}) prints {printed}')
sd = 0.39
bar = sd * emax(60)
check(round(bar, 2) == 0.90 and round(sd * 2.319, 2) == 0.90, f'bar 0.90 ({bar:.5f})')
check(round(sd * emax(12), 2) == 0.64 and round(sd * 1.629, 2) == 0.64, 'one-contract bar 0.64')
check(sd * emax(12) < 0.84 < bar, 'best 0.84 below the honest bar, above the one-contract bar')
check(5 * 12 == 60, 'count 60')
it = item('topic-2.3', 'e-honest-bar')
key_and_wrongs(it['parts'][0]['widget'], bar, {'one-contract': sd * emax(12), 'no-scale': emax(60)}, 'honest-bar')
opts = it['parts'][1]['widget']['options']
check([o['id'] for o in opts if o.get('correct')] == ['a'], 'choice key a')

# topic-2.6 e-two-fund-shrink: normal-normal shrinkage, B = s^2 / (s^2 + tau^2), forecasters in bp
mu, tau_ = 2.0, 2.5
def shrink(a, se):
    B = se ** 2 / (se ** 2 + tau_ ** 2)
    post = (mu / tau_ ** 2 + a / se ** 2) / (1 / tau_ ** 2 + 1 / se ** 2)     # second way: precision-weighted mean
    assert abs(post - (mu + (1 - B) * (a - mu))) < 1e-12
    return B, post
BA, A = shrink(11, 7.5); BB, Bv = shrink(6, 1.0)
check(close(BA, 0.9) and close(A, 2.9), 'forecaster A: B 0.9, 2.9 bp')
check(round(BB, 4) == 0.1379 and round(1 - BB, 4) == 0.8621 and round(Bv, 2) == 5.45, f'forecaster B: B 0.1379, keeps 0.8621, 5.45 bp ({Bv:.5f})')
check(close(7.5 ** 2, 56.25) and close(2.5 ** 2, 6.25) and close(56.25 + 6.25, 62.5) and close(1 + 6.25, 7.25), 'printed 56.25, 6.25, 62.5, 7.25')
check(Bv > A and 0.8 < 1 - BB < 0.9, 'B ends higher; keeps over four fifths')
it = item('topic-2.6', 'e-two-fund-shrink')
pa, pb = it['parts'][0]['widget'], it['parts'][1]['widget']
check(pa['unit'] == 'bp' and pb['unit'] == 'bp', 'unit bp on both parts')
key_and_wrongs(pa, A, {'raw': 11, 'inverted': mu + BA * (11 - mu), 'se-not-squared': mu + (1 - 7.5 / (7.5 + 2.5)) * 9}, 'forecaster-A')
key_and_wrongs(pb, Bv, {'raw': 6, 'inverted': mu + BB * 4, 'se-not-squared': mu + (1 - 1 / (1 + 2.5)) * 4}, 'forecaster-B')
check(pb['tol']['abs'] == 0.01 and close(2 + 0.86 * 4, pb['answer'], pb['tol']['abs']), 'forecaster-B: band one unit, a working with B_B = 0.14 (5.44) is accepted')
hp = item('topic-3.2', 'e-heat-grid-steps')['parts']
check('today' in hp[0]['question'] and 'at expiry' not in hp[0]['question'] and 'at expiry back to' in hp[1]['question'] and 'today' in hp[1]['question'], 'heat-grid: wording says today (tau = 0 at expiry)')
check(close(0.39 * 1.629, 0.64, 0.005) and close(0.39 * 2.319, 0.90, 0.005), 'honest-bar: 0.39 x 1.629 = 0.64 and 0.39 x 2.319 = 0.90 for the reviewer reply')

# topic-2.1 e-pd-two-trees: the feature is gap_z, the story a share borrow fee
txt = json.dumps(item('topic-2.1', 'e-pd-two-trees'))
check('vol_z' not in txt and 'gap_z' in txt and 'borrow fee' in txt, 'pd: gap_z and borrow fee wording')

# exam minutes: topic-2.6 grows from 25 to 26 items, 75 * 26 / 25 = 78, rounded to 5
d = json.load(open(os.path.join(EX, 'topic-2.6.json')))
check(len(d['items']) == 26 and d['minutes'] == 5 * round(75 * 26 / 25 / 5) == 80, 'topic-2.6 26 items, 80 minutes')
for e in ('topic-3.2', 'topic-2.1', 'topic-2.3'):
    d = json.load(open(os.path.join(EX, e + '.json')))
    check(len(d['items']) == 30 and d['minutes'] == 90, f'{e} 30 items, 90 minutes unchanged')

print('failures:', fails)
sys.exit(1 if fails else 0)
