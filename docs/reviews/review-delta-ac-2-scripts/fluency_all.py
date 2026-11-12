#!/usr/bin/env python3
"""Delta read AC-2, holes fix pass: the two Fluency families whose `where`, `let` and `wrong` changed, over EVERY draw
(not a sample): testing/fluency-l18 `two-by-two` (61^4 tables) and testing/fluency-l17 `poisson-ratio-test` (3,120 draws).
The formulas are read from the family files (the `let` strings are evaluated here, so a change to them is seen), the
grading rule is numGrade's: key band first (abs + 1e-9), then the first wrong[] band in file order.
For every draw the `where` keeps:
  - the key by a second route (Pearson's sum over four cells; the likelihood ratio from the log-likelihoods) agrees with `key`
  - right working as the prompt allows it is accepted: answer to 2 places; expected counts rounded to 2 places (two-by-two);
    the logarithm rounded to 4 places (poisson); the solution's printed figures
  - each wrong[] value, typed to 2 places, is refused and lands on its own id
Usage (repo root, venv python): fluency_all.py     exit 1 on a FAIL row; FINDING rows are recorded in the review."""
import json, math, sys
import numpy as np

fails = 0
findings = 0


def row(ok, msg, finding=False):
    global fails, findings
    if ok:
        print('ok      ' + msg)
    elif finding:
        findings += 1
        print('FINDING ' + msg)
    else:
        fails += 1
        print('FAIL    ' + msg)


def fam(path, fid):
    return next(f for f in json.load(open('app/content/courses/testing/' + path))['families'] if f['id'] == fid)


def ev(expr, env):
    return eval(expr.replace('^', '**'), {'__builtins__': {}}, dict(env, ln=np.log, abs=np.abs, sqrt=np.sqrt))


def r2(x):
    return np.round(x + 1e-12, 2)  # half up at 2 places, as a learner rounds; ties are measure zero here


def grade(typed, key, wrongs, ktol):
    """numGrade on arrays: returns -1 where accepted, else index of the first wrong band hit, else -2 (generic)."""
    out = np.full(typed.shape, -2)
    for i in range(len(wrongs) - 1, -1, -1):
        v, t = wrongs[i]
        out = np.where(np.abs(typed - v) <= t + 1e-9, i, out)
    return np.where(np.abs(typed - key) <= ktol + 1e-9, -1, out)


# ---------------------------------------------------------------- two-by-two
f = fam('fluency-l18-counts-against-expectations.json', 'two-by-two')
lo, hi = f['vars']['a']['int']
assert all(f['vars'][k]['int'] == [lo, hi] for k in 'abcd')
ktol = f['widget']['tol']['abs']
ids = [w['id'] for w in f['wrong']]
tot_kept = tot_all = 0
bad = {k: 0 for k in ['route', 'ans2', 'e2', 'e3', 'printed'] + ['refuse:' + i for i in ids] + ['own:' + i for i in ids]}
worst = {'e2': (0, None), 'printed': (0, None)}
ex = {}
B, Cc, Dd = np.meshgrid(np.arange(lo, hi + 1.0), np.arange(lo, hi + 1.0), np.arange(lo, hi + 1.0), indexing='ij')
B, Cc, Dd = B.ravel(), Cc.ravel(), Dd.ravel()
for a in range(lo, hi + 1):
    env = dict(a=np.full(B.shape, float(a)), b=B, c=Cc, d=Dd)
    for k, e in f['let'].items():
        env[k] = ev(e, env)
    keep = np.ones(B.shape, bool)
    for w in f['where']:
        keep &= ev(w, env)
    tot_all += keep.size
    env = {k: v[keep] for k, v in env.items()}
    A, b, c, d, key = env['a'], env['b'], env['c'], env['d'], env['key']
    n = A + b + c + d
    tot_kept += key.size
    O = [A, b, c, d]
    E = [(A + b) * (A + c) / n, (A + b) * (b + d) / n, (c + d) * (A + c) / n, (c + d) * (b + d) / n]
    pearson = sum((o - e) ** 2 / e for o, e in zip(O, E))
    bad['route'] += int((np.abs(pearson - key) > 1e-9).sum())
    wr = [(env[w['value'].strip('{}')], w['tol']['abs']) for w in f['wrong']]
    # second routes for the two new slips
    obs = sum((o - e) ** 2 / o for o, e in zip(O, E))
    g = 2 * sum(o * np.log(o / e) for o, e in zip(O, E))
    bad['route'] += int((np.abs(obs - env['obs']) > 1e-9).sum()) + int((np.abs(g - env['g']) > 1e-9).sum())
    bad['ans2'] += int((grade(r2(key), key, wr, ktol) != -1).sum())
    for dp, name in ((2, 'e2'), (3, 'e3')):
        Er = [np.round(e + 1e-12, dp) for e in E]
        x = sum((o - e) ** 2 / e for o, e in zip(O, Er))
        miss = grade(r2(x), key, wr, ktol) != -1
        bad[name] += int(miss.sum())
        if name == 'e2':
            dev = np.abs(r2(x) - key)
            i = int(dev.argmax())
            if dev[i] > worst['e2'][0]:
                worst['e2'] = (float(dev[i]), (a, int(b[i]), int(c[i]), int(d[i]), float(key[i]), float(r2(x)[i])))
    # the solution's printed figures: one gap to 3 places, squared, over each expected count to 2 places
    gap = np.round(env['gap'] + 1e-12, 3)
    x = sum(gap ** 2 / np.round(e + 1e-12, 2) for e in E)
    miss = grade(r2(x), key, wr, ktol) != -1
    bad['printed'] += int(miss.sum())
    dev = np.abs(r2(x) - key)
    if dev.size and dev.max() > worst['printed'][0]:
        i = int(dev.argmax())
        worst['printed'] = (float(dev[i]), (a, int(b[i]), int(c[i]), int(d[i]), float(key[i]), float(r2(x)[i])))
    for j, (v, t) in enumerate(wr):
        got = grade(r2(v), key, wr, ktol)
        acc = got == -1
        bad['refuse:' + ids[j]] += int(acc.sum())
        other = (got != j) & ~acc
        bad['own:' + ids[j]] += int(other.sum())
        if other.any() and ('own:' + ids[j]) not in ex:
            i = int(np.flatnonzero(other)[0])
            ex['own:' + ids[j]] = (a, int(b[i]), int(c[i]), int(d[i]), round(float(key[i]), 4), round(float(v[i]), 4), ids[int(got[i])] if got[i] >= 0 else 'generic')
        if acc.any() and ('refuse:' + ids[j]) not in ex:
            i = int(np.flatnonzero(acc)[0])
            ex['refuse:' + ids[j]] = (a, int(b[i]), int(c[i]), int(d[i]), round(float(key[i]), 4), round(float(v[i]), 4))

print(f'two-by-two: {tot_all:,} tables, {tot_kept:,} kept by `where` ({100 * tot_kept / tot_all:.1f}%)')
row(tot_kept / tot_all >= 0.2, f'two-by-two: the validator\'s limit (at least 20% of draws kept): {100 * tot_kept / tot_all:.1f}%')
row(bad['route'] == 0, f'two-by-two: key, `obs` and `g` agree with a cell-by-cell second route in every kept table ({bad["route"]} off)')
row(bad['ans2'] == 0, f'two-by-two: the key to 2 places is accepted in every kept table ({bad["ans2"]} refused)')
row(bad['e2'] == 0, f'two-by-two: expected counts kept to 2 places (the prompt\'s floor), answer to 2 places: refused in {bad["e2"]:,} kept tables; worst miss {worst["e2"][0]:.3f} at (a, b, c, d, key, typed) = {worst["e2"][1]}', finding=True)
row(bad['e3'] == 0, f'two-by-two: expected counts kept to 3 places: refused in {bad["e3"]:,} kept tables')
row(bad['printed'] == 0, f'two-by-two: the solution\'s own printed figures (gap to 3 places, counts to 2): refused in {bad["printed"]:,} kept tables; worst miss {worst["printed"][0]:.3f} at {worst["printed"][1]}', finding=True)
for i in ids:
    row(bad['refuse:' + i] == 0, f'two-by-two: slip {i} to 2 places is refused in every kept table ({bad["refuse:" + i]:,} accepted; first {ex.get("refuse:" + i)})', finding=True)
    row(bad['own:' + i] == 0, f'two-by-two: slip {i} to 2 places gets its own line in every kept table ({bad["own:" + i]:,} get another; first (a, b, c, d, key, slip, line given) = {ex.get("own:" + i)})', finding=True)

# ---------------------------------------------------------------- poisson-ratio-test
f = fam('fluency-l17-ratio-of-likelihoods.json', 'poisson-ratio-test')
ktol = f['widget']['tol']['abs']
ids = [w['id'] for w in f['wrong']]
v = f['vars']
ns = range(v['n']['int'][0], v['n']['int'][1] + 1, v['n']['step'])
dvs = [x for x in range(v['dv']['int'][0], v['dv']['int'][1] + 1) if x not in v['dv']['not']]
kept = alln = 0
cnt = {k: 0 for k in ['route', 'ans2', 'ln4', 'ln5'] + ['refuse:' + i for i in ids] + ['own:' + i for i in ids]}
first = {}
worst_ln4 = (0, None)
for n in ns:
    for lam0 in v['lam0']['pick']:
        for dv in dvs:
            alln += 1
            if n * lam0 + dv <= 0:
                continue
            env = dict(n=float(n), lam0=float(lam0), dv=float(dv))
            for k, e in f['let'].items():
                env[k] = float(ev(e, env))
            if not all(bool(ev(w, env)) for w in f['where']):
                continue
            kept += 1
            key, s = env['key'], n * lam0 + dv
            lhat = s / n
            # second route: twice the gap between the two Poisson log-likelihoods (the factorial terms cancel)
            ll = lambda lam: s * math.log(lam) - n * lam
            cnt['route'] += abs(2 * (ll(lhat) - ll(lam0)) - key) > 1e-9
            cnt['route'] += abs(dv * dv / (n * lam0) - env['score']) > 1e-12
            wr = [(np.array(env[w['value'].strip('{}')]), w['tol']['abs']) for w in f['wrong']]
            g1 = lambda x: int(grade(np.array(round(x + 1e-12, 2)), key, wr, ktol))
            cnt['ans2'] += g1(key) != -1
            for dp, name in ((4, 'ln4'), (5, 'ln5')):
                x = 2 * (s * round(math.log(s / (n * lam0)), dp) - dv)
                cnt[name] += g1(x) != -1
                if name == 'ln4' and abs(round(x, 2) - key) > worst_ln4[0]:
                    worst_ln4 = (abs(round(x, 2) - key), (n, lam0, dv, round(key, 4), round(x, 2)))
            for j, (val, t) in enumerate(wr):
                got = g1(float(val))
                if got == -1:
                    cnt['refuse:' + ids[j]] += 1
                    first.setdefault('refuse:' + ids[j], (n, lam0, dv, round(key, 4), round(float(val), 4)))
                elif got != j:
                    cnt['own:' + ids[j]] += 1
                    first.setdefault('own:' + ids[j], (n, lam0, dv, round(key, 4), round(float(val), 4), ids[got] if got >= 0 else 'generic'))
print(f'poisson-ratio-test: {alln:,} draws, {kept:,} kept by `where` ({100 * kept / alln:.1f}%)')
row(kept / alln >= 0.2, f'poisson: at least 20% of draws kept: {100 * kept / alln:.1f}%')
row(cnt['route'] == 0, f'poisson: key and `score` agree with a second route in every kept draw ({cnt["route"]} off)')
row(cnt['ans2'] == 0, f'poisson: the key to 2 places is accepted in every kept draw ({cnt["ans2"]} refused)')
row(cnt['ln4'] == 0, f'poisson: logarithm kept to 4 places (the prompt\'s floor): refused in {cnt["ln4"]} kept draws; worst miss {worst_ln4[0]:.3f} at (n, lam0, dv, key, typed) = {worst_ln4[1]}', finding=True)
row(cnt['ln5'] == 0, f'poisson: logarithm kept to 5 places: refused in {cnt["ln5"]} kept draws')
for i in ids:
    row(cnt['refuse:' + i] == 0, f'poisson: slip {i} to 2 places is refused in every kept draw ({cnt["refuse:" + i]} accepted; first {first.get("refuse:" + i)})', finding=True)
    row(cnt['own:' + i] == 0, f'poisson: slip {i} to 2 places gets its own line in every kept draw ({cnt["own:" + i]} get another; first (n, lam0, dv, key, slip, line given) = {first.get("own:" + i)})', finding=True)

print(f'fluency_all: {fails} failures, {findings} FINDING rows')
sys.exit(1 if fails else 0)
