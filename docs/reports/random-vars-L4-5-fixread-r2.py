"""Fix-pass read, random-vars L4-5 round 2 (commit 1b198892). Recomputes every number the
changed sentences state or rely on, by exact enumeration (one seeded simulation for the median).
Exits 0 on correct content."""
import json, os, sys, re, random
from fractions import Fraction as F
from math import comb, sqrt, log, exp
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'random-vars')
L = lambda f: json.load(open(os.path.join(B, f + '.json')))
bad = []
def ok(name, cond):
    if not cond: bad.append(name)

def wait(pattern):
    """Expected wait for a fair-coin pattern from each proper prefix (value iteration on the prefix chain)."""
    pre = [pattern[:i] for i in range(len(pattern))]
    def step(s, c):
        t = s + c
        while t and not pattern.startswith(t): t = t[1:]
        return t
    E = {s: 0.0 for s in pre}
    for _ in range(4000):
        E = {s: 1 + 0.5 * sum(0 if step(s, c) == pattern else E[step(s, c)] for c in 'HT') for s in pre}
    return E

# 1 homework-4 items[5]: HT waits 4, HH waits 6, E_H = 2
h4 = L('homework-4')['items'][5]
e = wait('HT'); ok('hw4 HT=4', abs(e[''] - 4) < 1e-9 and abs(e['H'] - 2) < 1e-9)
ok('hw4 HH=6', abs(wait('HH')[''] - 6) < 1e-9)
ok('hw4 text', 'waits 4 tosses against 6 for two heads' in h4['explain']['text'] and h4['widget']['answer'] == 4)

# 2 homework-5 items[4]: multinomial correlation
h5 = L('homework-5')['items']
n, pu, pd = 50, 0.4, 0.35
rho = -n * pu * pd / sqrt(n * pu * (1 - pu) * n * pd * (1 - pd))
ok('hw5 rho', abs(rho - h5[4]['widget']['answer']) < 0.002 and 'independently' in h5[4]['prose'])
ok('hw5 probs sum', abs(0.4 + 0.35 + 0.25 - 1) < 1e-12)

# 3 homework-5 items[7]: median close to exp(120 E ln(1+R)), below the mean
m = h5[7]['model']
ok('hw5 fund numbers', abs(1.012 ** 120 - 4.18) < 0.01 and abs(exp(120 * 0.00955) - 3.1) < 0.06
   and abs(log(1.012) - 0.01193) < 5e-6 and 'is close to' in m)
rng = random.Random(7); ws = []
for _ in range(20000):  # two-point R = 1.2% +/- 7%: mean 1.2%, sd 7%
    k = sum(rng.random() < 0.5 for _ in range(120)); ws.append(k * log(1.082) + (120 - k) * log(0.942))
ws.sort(); med = exp(ws[10000]); typ = exp(60 * (log(1.082) + log(0.942)))
ok('hw5 median close to exp(E log), below mean', abs(med / typ - 1) < 0.05 and med < 4.18)

# 4 l15 screens[8]: conditional means -0.9 and 0.7, midpoint 0.8
s = L('l15-given-information')['screens'][8]
rows = s['canvas']['params']['rows']; ys = [-2, -1, 0, 1, 2]
dn = sum(y * float(r[1]) for y, r in zip(ys, rows)); up = sum(y * float(r[2]) for y, r in zip(ys, rows))
ok('l15 means', abs(dn + 0.9) < 1e-9 and abs(up - 0.7) < 1e-9 and abs((0.9 + 0.7) / 2 - 0.8) < 1e-12)
ok('l15 no beta', 'beta' not in s['explain']['text'])

# 5 l16 screens[5]: slip 3 = wait for one head (2) + 1; key 6; leaves
s = L('l16-averaging-averages')['screens'][5]
ok('l16', abs(wait('H')[''] + 1 - 3) < 1e-9 and s['widget']['answer'] == 6
   and any(w['id'] == 'three' and w['value'] == 3 for w in s['widget']['wrong'])
   and s['canvas']['params']['leaves'] == {'t': '1 + E', 'h-h': '2', 'h-t': '2 + E'})
ok('l16 E=6', F(3, 2) / (1 - F(3, 4)) == 6)

# 6-8 l18
l18 = L('l18-random-sums'); s = l18['screens'][2]
ok('l18 sd slip', any(w['id'] == 'sd' and w['value'] == 25 * 30 for w in s['widget']['wrong']) and 'independent' in s['prose'])
q = l18['quiz'][2]
ok('l18 quiz', q['question'] == 'When can they fail?' and 'enough' in q['feedback']['correct'])
# X1, X2 fair +/-1, so E[X] = 0, Var(X) = 1. Enumerate the four outcomes.
def moments(count):
    out = [(sum(x[:count(x)]), count(x)) for x in [(a, b) for a in (1, -1) for b in (1, -1)]]
    ES = F(sum(o[0] for o in out), 4); ES2 = F(sum(o[0] ** 2 for o in out), 4)
    EN = F(sum(o[1] for o in out), 4); VN = F(sum(o[1] ** 2 for o in out), 4) - EN ** 2
    return ES, ES2 - ES ** 2, EN, VN
ES, VS, EN, VN = moments(lambda x: 1 if x[1] == 1 else 2)   # N looks ahead at fill 2: dependent
ok('l18 dependence can break the mean', ES != EN * 0)
ES, VS, EN, VN = moments(lambda x: 1 if x[0] == 1 else 2)   # N depends on fill 1 (a stopping rule)
ok('l18 independence not necessary', ES == EN * 0 and VS == EN * 1 + VN * 0)

# 9 l20 screens[9]: tree and key
s = L('l20-many-categories')['screens'][9]
br = {b['id']: float(b['p']) for b in s['canvas']['params']['levels'][0]['branches']}
ok('l20 tree', br == {'u': 0.6, 'f': 0.0, 'd': 0.4} and abs(sum(br.values()) - 1) < 1e-12)
p = comb(10, 6) * 0.6 ** 6 * 0.4 ** 4
ok('l20 key', abs(p - s['widget']['answer']) < 0.0005 and comb(10, 6) == 210 and abs(0.6 ** 6 * 0.4 ** 4 - 0.0012) < 0.0005)
ok('l20 prose', 'up 0.6, flat 0, down 0.4' in s['prose'])

# 10 problems-4 items[1] part 4
px = {0: F(5, 10), 1: F(3, 10), 2: F(2, 10)}; py = {0: F(7, 10), 1: F(3, 10)}
ps2 = sum(px[x] * py[y] for x in px for y in py if x + y == 2)
ok('p4', ps2 == F(23, 100) and px[1] * py[1] / ps2 > py[1])

# 11 problems-5 items[3] part 5
tot = F(0); EW = F(0); pn = {2: F(1, 4), 4: F(1, 2), 6: F(1, 4)}
for N, w in pn.items():
    for k in range(N + 1):
        W = F(3, 2) ** k * F(3, 5) ** (N - k); pr = w * comb(N, k) / 2 ** N
        EW += pr * W
        if W < 1: tot += pr
        ok('p5 iff N=%d k=%d' % (N, k), (W < 1) == (2 * k <= N))
    ok('p5 one more up N=%d' % N, F(3, 2) ** (N // 2 + 1) * F(3, 5) ** (N // 2 - 1) > 1)
ok('p5 total', tot == F(89, 128) and abs(float(EW) - 1.2184) < 5e-5)

# 12 review-5 items[8]
r = L('review-5')['items'][8]
p_ = F(1, 4)
ok('r5', 1 / p_ == 4 and (1 - p_) / p_ ** 2 == 12 and 4 * 5 + 12 * 9 == r['widget']['answer']
   and 'independent of the other fees and of $N$' in r['prose'])

# voice on the changed strings
changed = [h4['explain']['text'], h5[4]['prose'], L('l15-given-information')['screens'][8]['explain']['text'],
           L('l16-averaging-averages')['screens'][5]['feedback']['byKey']['three'], l18['screens'][2]['feedback']['byKey']['sd'],
           q['question'], q['feedback']['correct'], L('problems-4')['items'][1]['parts'][3]['widget']['options'][3]['why'],
           L('problems-5')['items'][3]['parts'][4]['explain']['text'], r['prose']]
for t in changed:
    ok('voice chars: ' + t[:30], '!' not in t and '—' not in t and not re.search(r'\bl\d\d\b|[Ll]esson \d', t))
    plain = re.sub(r'\$[^$]*\$', 'X', t)
    sents = [x for x in re.split(r'(?<=[.?])\s+(?=[A-Z0-9X])', plain) if x.strip()]
    ok('voice length: ' + t[:30], all(len(x.split()) <= 35 for x in sents) and len(sents) <= 3)

if bad:
    print('FAIL:', *bad, sep='\n  '); sys.exit(1)
print('fix-read r2: all checks pass')
