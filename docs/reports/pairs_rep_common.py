"""Shared second computation for the pairs-rep number scripts (pairs-rep-L<n>-numbers.py).

Everything here is written independently of the lesson builders: SSDs by pairwise differences,
pair ranking by sorting Python tuples, and trading as a day-by-day state machine. The panel is
the course's seeded generator, copied verbatim from docs/briefs/pairs-rep.md (it defines the data).
`check_code(lv)` runs every code widget of a level in CPython: the solution must pass every hidden
test and the starter must fail at least one.
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402


def pairs_panel(seed=2006, n_ind=10, per_ind=10, n_pairs=20, days=3024, half_life=8.0, ou_sd=0.008,
                rw_sd=0.015, break_day=1512, break_frac=0.8, half_spread=0.005):
    rng = np.random.default_rng(seed)
    N = n_ind * per_ind
    ind = np.repeat(np.arange(n_ind), per_ind)
    mkt = np.cumsum(0.0003 + 0.010 * rng.standard_normal(days))
    indf = np.cumsum(0.008 * rng.standard_normal((days, n_ind)), axis=0)
    phi = 0.5 ** (1.0 / half_life)
    u = np.cumsum(rw_sd * rng.standard_normal((days, N)), axis=0)
    common = np.cumsum(rw_sd * rng.standard_normal((days, n_pairs)), axis=0)
    eps = ou_sd * rng.standard_normal((days, 2 * n_pairs))
    a = np.zeros((days, 2 * n_pairs))
    for t in range(1, days):
        a[t] = phi * a[t - 1] + eps[t]
    broken = rng.random(n_pairs) < break_frac
    drift = np.cumsum(rw_sd * rng.standard_normal((days, 2 * n_pairs)), axis=0)
    for k in range(n_pairs):
        for j in (2 * k, 2 * k + 1):
            x = common[:, k] + a[:, j]
            if broken[k]:
                x = x + np.where(np.arange(days) >= break_day, drift[:, j] - drift[break_day, j], 0.0)
            u[:, j] = x
    pair_ind = np.repeat(np.arange(n_ind), 2)[:n_pairs]
    ind[:2 * n_pairs] = np.repeat(pair_ind, 2)
    logp = np.log(50.0) + mkt[:, None] + indf[:, ind] + u
    mid = np.exp(logp)
    bounce = np.where(rng.random((days, N)) < 0.5, 1 + half_spread, 1 - half_spread)
    close = mid * bounce
    return close, mid, ind, broken, mkt


CLOSE, MID, IND, BROKEN, MKT = pairs_panel()


def ssd_all(Pn):
    """SSD matrix by pairwise differences, one row at a time."""
    N = Pn.shape[1]
    D = np.zeros((N, N))
    for i in range(N):
        D[i] = ((Pn[:, [i]] - Pn) ** 2).sum(axis=0)
    return D


def ranked(Pn):
    D = ssd_all(Pn)
    N = D.shape[0]
    items = [(D[i, j], i, j) for i in range(N) for j in range(i + 1, N)]
    items.sort(key=lambda x: x[0])          # Python's sort is stable
    return items, D


def closest(Pn, k, one_partner=False, lo=0):
    items, _ = ranked(Pn)
    out, used = [], set()
    for _, i, j in items:
        if one_partner and (i in used or j in used):
            continue
        out.append((i, j)); used |= {i, j}
        if len(out) == k + lo:
            break
    return out[lo:]


def trade(form, tr, i, j, wait=0, m=2.0, log=None):
    """Day-by-day state machine: flat -> open -> flat. Returns (payoff, opened, round trips)."""
    sd = float(np.std(form[:, i] - form[:, j]))
    s = tr[:, i] - tr[:, j]
    n = len(s)
    state, side, entry, t, pay, trips = 'flat', 0, None, 0, 0.0, 0
    while t < n:
        if state == 'flat':
            if sd > 0 and abs(s[t]) > m * sd and t + wait < n - 1:
                side = 1 if s[t] > 0 else -1
                entry = t + wait
                state = 'open'
            t += 1
            continue
        crossed = s[t] * side <= 0
        if crossed or t == n - 1:
            ex = min(t + wait, n - 1) if crossed else n - 1
            r_i = tr[ex, i] / tr[entry, i] - 1
            r_j = tr[ex, j] / tr[entry, j] - 1
            pay += side * (r_j - r_i)
            trips += 1
            if log is not None:
                log.append((entry, ex, side, side * (r_j - r_i)))
            state = 'flat'
            t = ex + 1
            continue
        t += 1
    return pay, trips > 0, trips


def cycle(px, start, k, wait=0, lo=0, m=2.0, one_partner=False):
    P = px[start:start + 378] / px[start]
    form, tr = P[:252], P[252:]
    prs = closest(form, k, one_partner, lo)
    res = [trade(form, tr, i, j, wait, m) for i, j in prs]
    tot = sum(r[0] for r in res); n = sum(1 for r in res if r[1])
    return tot / k, (tot / n if n else 0.0), n, prs, res


def run(px, k, wait=0, step=21, lo=0):
    return [(st,) + cycle(px, st, k, wait, lo)[:3] for st in range(0, px.shape[0] - 377, step)]


# ---------------------------------------------------------------- code widgets
def _close(a, b, rel=1e-9, ab=1e-12):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_close(a[k], b[k], rel, ab) for k in a)
    if hasattr(a, 'tolist'):
        a = a.tolist()
    if hasattr(b, 'tolist'):
        b = b.tolist()
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y, rel, ab) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=rel, abs_tol=ab)
    return a == b


def _run_tests(w, src):
    ns = {'__learner_source__': src}
    exec(w.get('prelude', ''), ns)
    exec(src, ns)
    fails = 0
    for t in w['tests']:
        try:
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            exp = eval(t['expect'], ns)
            if t.get('compare', 'equal') == 'isclose':
                tol = t.get('tol', {})
                ok = _close(got, exp, tol.get('rel', 0 if 'abs' in tol else 1e-9), tol.get('abs', 0 if 'rel' in tol else 1e-12))
            else:
                ok = got == exp if not hasattr(got, 'tolist') else got.tolist() == exp
            fails += not ok
        except Exception:
            fails += 1
    return fails


def _widgets(node, path=''):
    if isinstance(node, dict):
        if node.get('kind') == 'code' and 'tests' in node:
            yield path, node
        for k, v in node.items():
            yield from _widgets(v, f'{path}.{k}')
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _widgets(v, f'{path}[{i}]')


def check_code(lv):
    for fid, doc in lv.files.items():
        for path, w in _widgets(doc):
            try:
                sol = _run_tests(w, w['solution'])
            except Exception as e:
                sol = f'error {e}'
            try:
                st = _run_tests(w, w['starter'])
            except Exception:
                st = len(w['tests'])
            lv._rec(sol == 0, f'{fid}{path} solution passes {len(w["tests"])} tests', '' if sol == 0 else f'{sol} failing')
            lv._rec(st > 0, f'{fid}{path} starter fails', '' if st > 0 else 'starter passes every test')
