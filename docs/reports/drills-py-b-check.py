"""Check for drill pack py, agent B: the 12 numpy-pandas drills.

For every drill it:
- runs the model solution on every example and hidden test and compares with `expect`, using the
  drill page's own rule (`__zq_eq` in app/js/screens/drill.js: plain lists, isclose at rel 1e-9, None for NaN);
- runs an independent method written here in plain Python loops (no pandas reduction, shift,
  rolling, resample, groupby or merge) and compares it with every `expect` too;
- checks the starter fails at least one hidden test;
- runs every planted solution on the hidden tests and asserts it fails at least one;
- checks the mix (4 / 5 / 3 at difficulty 1 / 2 / 3), pace 300 to 1,200, 2 or 3 examples with a
  note, 10 to 14 hidden tests, two or more planted, the test count in `how`, and the index row.
Exit 0 on success.
Run from the repo root: <scratchpad>/venv/bin/python docs/reports/drills-py-b-check.py
"""
import csv, datetime as dt, json, math, os, shutil, statistics, sys, tempfile, warnings

import numpy as np
import pandas as pd

warnings.simplefilter('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DRILLS = os.path.join(APP, 'content', 'drills')
IDS = ['py-big-move-days', 'py-best-desk-each-day', 'py-carry-forward-limit', 'py-volume-surge',
       'py-fx-to-pounds', 'py-fill-summary', 'py-weekly-range', 'py-gap-aware-returns',
       'py-combined-desk-pnl', 'py-prior-zscore', 'py-excess-vs-benchmark', 'py-month-hit-rate']
MIX = {1: 4, 2: 5, 3: 3}


def isnan(x):
    return isinstance(x, float) and x != x

# ---------------------------------------------------------------- independent methods

def big_move_days(returns, volumes, move, min_volume):
    out = []
    for i in range(len(returns)):
        r = returns[i]
        if (r >= move or -r >= move) and volumes[i] >= min_volume:
            out.append(i)
    return out


def best_desk(pnl, desks):
    out = []
    for row in pnl:
        best = 0
        for j in range(1, len(row)):
            if row[j] > row[best]:      # strictly greater: the first desk keeps a tie
                best = j
        out.append(desks[best])
    return out


def carry_forward(close, limit):
    vals = [float(v) for v in close.tolist()]
    out, last, run = [], None, 0
    for v in vals:
        if isnan(v):
            run += 1
            out.append(last if (last is not None and run <= limit) else float('nan'))
        else:
            last, run = v, 0
            out.append(v)
    return pd.Series(out, index=close.index, dtype=float)


def volume_surges(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    out = []
    for i in range(1, len(rows)):
        if int(rows[i]['volume']) >= 2 * int(rows[i - 1]['volume']):
            out.append(dt.datetime.strptime(rows[i]['date'], '%Y-%m-%d').strftime('%Y-%m-%d'))
    return out


def to_pounds(prices, rates):
    return np.array([[float(p) * rates[i] for p in row] for i, row in enumerate(prices)])


def fill_summary(fills):
    acc = {}
    for t, s, q, p in fills[['ticker', 'side', 'qty', 'price']].itertuples(index=False):
        a = acc.setdefault(t, [0, 0.0, 0, 0])
        a[0] += q if s == 'B' else -q
        a[1] += q * p
        a[2] += q
        a[3] += 1
    keys = sorted(acc)
    return pd.DataFrame({'net': [acc[k][0] for k in keys], 'vwap': [acc[k][1] / acc[k][2] for k in keys],
                         'fills': [acc[k][3] for k in keys]}, index=keys)


def weekly_range(close):
    weeks = {}
    for d, v in zip(close.index, close.tolist()):
        fri = (d + pd.Timedelta(days=(4 - d.weekday()) % 7)).normalize()
        weeks.setdefault(fri, []).append(v)
    keys = sorted(weeks)
    vals = [(max(weeks[k]) - min(weeks[k])) / weeks[k][0] for k in keys]
    return pd.Series(vals, index=pd.DatetimeIndex(keys), dtype=float)


def gap_returns(close):
    vals = [float(v) for v in close.tolist()]
    out = []
    for i, v in enumerate(vals):
        if i == 0 or isnan(v) or isnan(vals[i - 1]):
            out.append(float('nan'))
        else:
            out.append(v / vals[i - 1] - 1)
    return pd.Series(out, index=close.index, dtype=float)


def combined_pnl(a, b):
    tot = {}
    for s in (a, b):
        for d, v in zip(s.index, s.tolist()):
            tot[d] = tot.get(d, 0.0) + v
    keys = sorted(tot)
    return pd.Series([tot[k] for k in keys], index=pd.DatetimeIndex(keys), dtype=float)


def prior_zscore(close, n):
    vals = close.tolist()
    out = []
    for i, v in enumerate(vals):
        if i < n:
            out.append(float('nan'))
            continue
        w = vals[i - n:i]
        s = statistics.stdev(w)
        out.append(float('nan') if s == 0 else (v - statistics.fmean(w)) / s)
    return pd.Series(out, index=close.index, dtype=float)


def mean_excess_bps(prices, bench):
    brows = sorted(zip(bench['date'], bench['close']))
    bret = {brows[i][0]: brows[i][1] / brows[i - 1][1] - 1 for i in range(1, len(brows))}
    by = {}
    for d, t, c in prices[['date', 'ticker', 'close']].itertuples(index=False):
        by.setdefault(t, []).append((d, c))
    out = {}
    for t in sorted(by):
        rows = sorted(by[t])
        ex = [rows[i][1] / rows[i - 1][1] - 1 - bret[rows[i][0]] for i in range(1, len(rows))]
        if ex:
            out[t] = sum(ex) / len(ex) * 10000
    return pd.Series(list(out.values()), index=list(out.keys()), dtype=float)


def month_hit_rate(close):
    last = {}
    for d, v in zip(close.index, close.tolist()):
        last[(d.year, d.month)] = v          # dates are sorted, so the last write is the month's last close
    months = sorted(last)
    ups, cnt = {}, {}
    for i in range(1, len(months)):
        m = months[i][1]
        r = last[months[i]] / last[months[i - 1]] - 1
        cnt[m] = cnt.get(m, 0) + 1
        ups[m] = ups.get(m, 0) + (1 if r > 0 else 0)
    keys = sorted(cnt)
    return pd.Series([ups[m] / cnt[m] for m in keys], index=keys, dtype=float)


INDEP = {'big_move_days': big_move_days, 'best_desk': best_desk, 'carry_forward': carry_forward,
         'volume_surges': volume_surges, 'to_pounds': to_pounds, 'fill_summary': fill_summary,
         'weekly_range': weekly_range, 'gap_returns': gap_returns, 'combined_pnl': combined_pnl,
         'prior_zscore': prior_zscore, 'mean_excess_bps': mean_excess_bps, 'month_hit_rate': month_hit_rate}

# ---------------------------------------------------------------- the drill page's comparison
# A copy of __zq_eq in app/js/screens/drill.js: isclose walks lists and tuples and compares numbers with
# math.isclose(rel 1e-9, abs 1e-12); None must meet None; anything else (text, dicts, NaN) fails in isclose.
# equal is plain ==. So the drills hand the tests plain lists, with None for a missing value.

def drill_eq(a, e, mode):
    if mode == 'isclose':
        if e is None:
            return a is None
        if isinstance(e, (list, tuple)):
            return isinstance(a, (list, tuple)) and len(a) == len(e) and all(drill_eq(x, y, mode) for x, y in zip(a, e))
        if isinstance(a, bool) or not isinstance(a, (int, float)):
            return False
        return math.isclose(a, e, rel_tol=1e-9, abs_tol=1e-12)
    return a == e


def judge(actual, case, ns):
    exp = eval(case['expect'], ns)
    return bool(drill_eq(actual, exp, case.get('compare', 'isclose')))


# ---------------------------------------------------------------- runner

def run_cases(drill, code, cases, fn_override=None):
    """Returns a list of (ok, detail) per case, each case in a fresh namespace and directory."""
    res = []
    for case in cases:
        tmp = tempfile.mkdtemp()
        for name, src in (drill.get('data') or {}).items():
            shutil.copy(os.path.join(APP, src), os.path.join(tmp, name))
        cwd = os.getcwd()
        os.chdir(tmp)
        try:
            ns = {}
            if code is not None:
                exec(code, ns)                      # the drill page runs the learner's code first,
            exec(drill.get('prelude', ''), ns)      # then the prelude, then the tests
            if fn_override is not None:
                ns[drill['fn']] = fn_override
            actual = eval(case['call'], ns)
            ok = judge(actual, case, ns)
            res.append((ok, repr(actual)[:160]))
        except Exception as e:
            res.append((False, f'raised {type(e).__name__}: {e}'[:160]))
        finally:
            os.chdir(cwd)
            shutil.rmtree(tmp, ignore_errors=True)
    return res


def brief_numbers():
    """The numbers stated in briefs and notes that no example `expect` carries, worked a second way by hand."""
    bad = []
    def near(name, got, want, tol=5e-4):
        if abs(got - want) > tol:
            bad.append(f'{name}: {got} against the stated {want}')
    near('volume surge: 2 x 98,100', 2 * 98100, 196200, 0)
    near('fill summary: VOD value', 1200 * 72.40 + 800 * 72.10 + 1500 * 72.90, 253910, 1e-6)
    near('fill summary: VOD vwap', 253910 / 3500, 72.546)
    near('fill summary: VOD net', 1200 + 800 - 1500, 500, 0)
    near('weekly range: week 1', (52.0 - 49.6) / 50.0, 0.048, 1e-12)
    near('weekly range: week 2', (53.5 - 51.0) / 52.4, 2.5 / 52.4, 1e-12)
    near('gap returns: 82 / 80 - 1', 82 / 80 - 1, 0.025, 1e-12)
    near('gap returns: 83.16 / 84 - 1', 83.16 / 84 - 1, -0.01, 1e-12)
    near('fx: 102 x 0.78', 102 * 0.78, 79.56, 1e-9)
    m = (21 + 22 + 24) / 3
    sd = math.sqrt(((21 - m) ** 2 + (22 - m) ** 2 + (24 - m) ** 2) / 2)
    near('z-score: deviation is sqrt(7/3)', sd, math.sqrt(7 / 3), 1e-12)
    near('z-score: day 4', (20 - m) / sd, -1.528)
    near('z-score: day 3', (24 - 21) / 1.0, 3.0, 0)
    nwg = [412 / 400 - 1, 420 / 412 - 1]
    idx = [8240.59 / 8159 - 1, 0.0]
    near('excess: NWG day 1 return 3%', nwg[0], 0.03, 1e-12)
    near('excess: NWG day 2 return about 1.942%', nwg[1] * 100, 1.942)
    near('excess: index day 1 return 1%', idx[0], 0.01, 1e-9)
    near('excess: NWG mean about 197.1 bp', ((nwg[0] - idx[0]) + (nwg[1] - idx[1])) / 2 * 10000, 197.1, 0.05)
    near('excess: LLOY returns 1% and 2%', (54.54 / 54 - 1) + (55.6308 / 54.54 - 1), 0.03, 1e-9)
    near('fill summary: 40 shares in example', 40, 40, 0)
    for b in bad:
        print('brief number:', b)
    return len(bad)


def main():
    errors = brief_numbers()
    index = {r['id']: r for r in json.load(open(os.path.join(DRILLS, 'index.json')))}
    mix = {}
    planted_total = 0
    for did in IDS:
        d = json.load(open(os.path.join(DRILLS, did + '.json')))
        cases = d['examples'] + d['tests']
        def bad(msg):
            nonlocal errors
            errors += 1
            print(f'{did}: {msg}')
        for i, (ok, det) in enumerate(run_cases(d, d['solution'], cases)):
            if not ok:
                bad(f'model fails case {i}: {cases[i]["call"][:80]} -> {det}')
        for i, (ok, det) in enumerate(run_cases(d, None, cases, INDEP[d['fn']])):
            if not ok:
                bad(f'independent method disagrees on case {i}: {cases[i]["call"][:80]} -> {det}')
        if all(ok for ok, _ in run_cases(d, d['starter'], d['tests'])):
            bad('starter passes every hidden test')
        for k, p in enumerate(d.get('planted', [])):
            planted_total += 1
            r = run_cases(d, p['code'], d['tests'])
            if all(ok for ok, _ in r):
                bad(f'planted {k} passes every hidden test: {p["slip"]}')
        # shape of the drill
        mix[d['difficulty']] = mix.get(d['difficulty'], 0) + 1
        if not (300 <= d['pace'] <= 1200):
            bad('pace out of range')
        if not (2 <= len(d['examples']) <= 3) or not all(e.get('note') for e in d['examples']):
            bad('needs 2 or 3 examples, each with a note')
        if not (10 <= len(d['tests']) <= 14):
            bad('needs 10 to 14 hidden tests')
        if len(d.get('planted', [])) < 2:
            bad('needs two or more planted solutions')
        if f'Submit runs {len(d["tests"])} hidden tests' not in d['how']:
            bad('`how` test count is wrong')
        if d.get('pack') != 'py' or d.get('course') != 'numpy-pandas' or not did.startswith('py-'):
            bad('pack, course or id prefix')
        if len(d.get('notes', [])) != 3:
            bad('notes must be three lines')
        row = index.get(did)
        if not row or row['name'] != d['name'] or row['course'] != d['course'] or row['difficulty'] != d['difficulty']:
            bad('index.json row missing or disagrees with the file')
        print(f'{did}: {len(cases)} cases, {len(d.get("planted", []))} planted checked')
    if mix != MIX:
        errors += 1
        print('difficulty mix', mix, 'expected', MIX)
    print(f'{len(IDS)} drills, {planted_total} planted, {errors} errors')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
