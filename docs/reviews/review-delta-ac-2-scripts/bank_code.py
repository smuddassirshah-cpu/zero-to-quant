#!/usr/bin/env python3
"""Delta read AC-2, bank part 2: the six code tasks whose hidden tests the fix pass swapped (commit 6392a67).
For each task, on the tests BEFORE the pass (git show 6392a67^) and as they stand now:
  model passes all, starter fails, my own solution (MINE below, written from the statement) passes all,
  every candidate-wrong solution of the first reader (review-bank-2-b-scripts/cands_<n>.py), of the delta reader
  (review-delta-bank-2-scripts/cands.py) and my extras (EXTRA below) is run. A candidate that passes every test now is
  printed PASSES NOW; one that failed before and passes now is printed REGRESSION. "alt:" names are right solutions.
The expect of each changed test is recomputed by MINE and by a brute route (BRUTE).
Judge: the rule of __zq_judge in widgets/code.js (code_run_lib.py of the delta reader). A case is stopped at 4 s of CPython.
Usage (repo root, venv python): bank_code.py [id ...]     exit 1 on any failure of a right solution, PASSES NOW or REGRESSION
(known: `index-method`, stopped in the page for time, is in KNOWN_PASS; my three extras that pass are in FINDING; neither sets the
exit code). The two slow tasks are best run one id a command (each under 90 s)."""
import importlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REV = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(REV, 'review-delta-bank-2-scripts'))
sys.path.insert(0, os.path.join(REV, 'review-bank-2-b-scripts'))
from code_run_lib import run
from cands import C

FIX = '6392a67'
TASKS = {  # id: (file number, changed test number, 1-based)
    'ds-pointers-merge-ticks': (2, 9), 'edge-case-list-to-pence': (1, 5), 'pf-idioms-count-above-mean': (4, 5),
    'edge-case-list-second-largest': (2, 4), 'at-search-count-in-range': (3, 10), 'pf-collections-top-symbols': (2, 10),
}
KNOWN_PASS = {('at-search-count-in-range', 'index-method')}
# My own extras that pass every test now: recorded in the review (findings 2 and 3, and a note), printed as FINDING.
FINDING = {('ds-pointers-merge-ticks', 'x-sort-into-b'), ('edge-case-list-second-largest', 'x-falsy-second'), ('edge-case-list-to-pence', 'x-lstrip-only')}
# The first reader wrote these two before the items were restated under new function names (fix pass of bank 2 b), so
# as written they raise NameError on every test and "caught" means nothing. Wrapped here so they are run for what they compute.
ADAPT = {
    'edge-case-list-second-largest': '\ndef runner_up_gap(xs):\n    s = second_largest(xs)\n    return None if s is None or not xs else max(xs) - s\n',
    'pf-collections-top-symbols': '\ndef busiest_symbols(trades, k):\n    return top_symbols(trades, k)\n',
}

MINE = {
 'ds-pointers-merge-ticks': '''
def merge_ticks(a, b):
    pa, pb = dict(a), dict(b)
    out = []
    for t in sorted(set(pa) | set(pb)):
        if t in pa and t in pb:
            out.append((t, (pa[t] + pb[t]) / 2))
        else:
            out.append((t, pa[t] if t in pa else pb[t]))
    return out
''',
 'edge-case-list-to-pence': '''
import re
def to_pence(text):
    m = re.fullmatch(r"\\s*(-?)\\s*£?\\s*([0-9,]*)(?:\\.([0-9]{0,2}))?\\s*", text)
    neg, whole, frac = m.group(1), m.group(2).replace(",", ""), m.group(3) or ""
    v = int(whole or 0) * 100 + int(frac.ljust(2, "0") or 0)
    return -v if neg else v
''',
 'pf-idioms-count-above-mean': '''
from fractions import Fraction
def above_mean(xs):
    if len(xs) == 0:
        return 0
    m = Fraction(sum(xs), len(xs))
    return len([x for x in xs if x > m])
''',
 'edge-case-list-second-largest': '''
def runner_up_gap(xs):
    top = second = None
    for x in xs:
        if top is None or x > top:
            top, second = x, top
        elif x != top and (second is None or x > second):
            second = x
    return None if second is None else top - second
''',
 'at-search-count-in-range': '''
def count_in_range(xs, lo, hi):
    def first(pred):
        a, b = 0, len(xs)
        while a < b:
            m = (a + b) // 2
            if pred(xs[m]):
                b = m
            else:
                a = m + 1
        return a
    return max(0, first(lambda v: v > hi) - first(lambda v: v >= lo))
''',
 'pf-collections-top-symbols': '''
from collections import defaultdict
def busiest_symbols(trades, k):
    size, first = defaultdict(int), {}
    for i, (s, q) in enumerate(trades):
        size[s] += -q if q < 0 else q
        first.setdefault(s, i)
    return sorted(size, key=lambda s: (-size[s], first[s]))[:k]
''',
}

# Brute, by hand or by closed form, for the expect of each changed test (a second route to MINE).
BRUTE = {
 'ds-pointers-merge-ticks': lambda: ([(1, (4.0 + 2.0) / 2), (2, 1.0), (3, 5.0)], [(1, 4.0), (2, 1.0)], [(1, 2.0), (3, 5.0)]),
 'edge-case-list-to-pence': lambda: -(2 * 100 + 5),
 'pf-idioms-count-above-mean': lambda: sum(5 * x > 0 + 6 + 10 + 10 + 10 for x in [0, 6, 10, 10, 10]),
 'edge-case-list-second-largest': lambda: (-1) - (-2),
 # xs = 0, 2, ..., 1,999,998; values >= k for even k number 10^6 - k/2; k/2 runs 0..2999
 'at-search-count-in-range': lambda: 3000 * 10**6 - sum(range(3000)),
 'pf-collections-top-symbols': lambda: _top(),
}


def _top():
    # symbol j (0..19999) trades at i = j + 20000 m, m = 0..4; its size is the sum of |(i % 7) - 3|
    tot = [sum(abs(((j + 20000 * m) % 7) - 3) for m in range(5)) for j in range(20000)]
    best = sorted(range(20000), key=lambda j: (-tot[j], j))[:3]
    return ['S%05d' % j for j in best]


# My extra candidates: each is wrong, or (alt:) right; aimed at what the swapped test might have dropped.
EXTRA = {
 'ds-pointers-merge-ticks': [
  ('x-extend-a-tail', 'puts the rest of b on the end of a', 'def merge_ticks(a, b):\n    d = dict(b)\n    out = [(t, (p + d.pop(t)) / 2) if t in d else (t, p) for t, p in a]\n    a.extend(sorted(d.items()))\n    return sorted(out + sorted(d.items()))\n'),
  ('x-sort-into-b', 'b.extend(a) when the times are all different', 'def merge_ticks(a, b):\n    ta = {t for t, _ in a}\n    if not any(t in ta for t, _ in b):\n        b.extend(a); b.sort(); return list(b)\n    d = dict(a)\n    for t, p in b: d[t] = (d[t] + p) / 2 if t in d else p\n    return sorted(d.items())\n'),
  ('x-int-mean', 'whole-number mean', 'def merge_ticks(a, b):\n    d = dict(a)\n    for t, p in b: d[t] = (d[t] + p) // 2 if t in d else p\n    return sorted(d.items())\n'),
 ],
 'edge-case-list-to-pence': [
  ('x-lstrip-only', 'strips the left side only', 'def to_pence(text):\n    s = text.lstrip()\n    sign = 1\n    if s.startswith("-"): sign, s = -1, s[1:]\n    s = s.replace("£", "").replace(",", "")\n    a, _, b = s.partition(".")\n    return sign * (int(a or "0") * 100 + int((b + "00")[:2]))\n'),
  ('x-no-sign', 'drops the minus sign', 'def to_pence(text):\n    s = text.strip().lstrip("-").replace("£", "").replace(",", "")\n    a, _, b = s.partition(".")\n    return int(a or "0") * 100 + int((b + "00")[:2])\n'),
  ('x-sign-on-pounds', 'sign applied to the pounds only', 'def to_pence(text):\n    s = text.strip().replace("£", "").replace(",", "")\n    a, _, b = s.partition(".")\n    return int(a or "0") * 100 + int((b + "00")[:2])\n'),
 ],
 'pf-idioms-count-above-mean': [
  ('x-median', 'above the median', 'def above_mean(xs):\n    if not xs: return 0\n    s = sorted(xs); m = s[len(s) // 2]\n    return sum(x > m for x in xs)\n'),
  ('x-mean-of-distinct', 'mean of the different values', 'def above_mean(xs):\n    if not xs: return 0\n    d = set(xs); m = sum(d) / len(d)\n    return sum(x > m for x in xs)\n'),
  ('x-round-mean', 'mean rounded to a whole number', 'def above_mean(xs):\n    if not xs: return 0\n    m = round(sum(xs) / len(xs))\n    return sum(x > m for x in xs)\n'),
  ('x-ceil-mean', 'at or above the mean rounded up', 'def above_mean(xs):\n    if not xs: return 0\n    m = -(-sum(xs) // len(xs))\n    return sum(x >= m for x in xs)\n'),
  ('x-count-distinct', 'counts different values above the mean', 'def above_mean(xs):\n    if not xs: return 0\n    m = sum(xs) / len(xs)\n    return len({x for x in xs if x > m})\n'),
 ],
 'edge-case-list-second-largest': [
  ('x-zero-floor', 'second value started at 0', 'def runner_up_gap(xs):\n    if len(set(xs)) < 2: return None\n    m = max(xs); s = 0\n    for x in xs:\n        if x != m and x > s: s = x\n    return m - s\n'),
  ('x-abs-gap-of-ends', 'abs of first less last of the sorted set', 'def runner_up_gap(xs):\n    d = sorted(set(xs))\n    return abs(d[0] - d[1]) if len(d) > 1 else None\n'),
  ('x-falsy-second', '`if not second` for the missing second value', 'def runner_up_gap(xs):\n    d = sorted(set(xs), reverse=True)\n    second = d[1] if len(d) > 1 else None\n    return d[0] - second if second else None\n'),
 ],
 'at-search-count-in-range': [
  ('x-count-method', 'sum of a generator over the whole list', 'def count_in_range(xs, lo, hi):\n    return sum(1 for x in xs if lo <= x <= hi)\n'),
  ('x-bisect-then-walk-right', 'bisect for the left edge, then walks to hi', 'from bisect import bisect_left\ndef count_in_range(xs, lo, hi):\n    i = bisect_left(xs, lo); n = 0\n    while i < len(xs) and xs[i] <= hi:\n        n += 1; i += 1\n    return n\n'),
  ('x-clamp-hi', 'treats hi beyond the last value as nothing found', 'from bisect import bisect_left, bisect_right\ndef count_in_range(xs, lo, hi):\n    if hi < lo or not xs or hi > xs[-1]: return 0\n    return bisect_right(xs, hi) - bisect_left(xs, lo)\n'),
 ],
 'pf-collections-top-symbols': [
  ('x-ties-by-name', 'ties by symbol name', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + abs(q)\n    return sorted(t, key=lambda s: (-t[s], s))[:k]\n'),
  ('x-ties-by-last', 'ties by last trade', 'def busiest_symbols(trades, k):\n    t, last = {}, {}\n    for i, (s, q) in enumerate(trades):\n        t[s] = t.get(s, 0) + abs(q); last[s] = i\n    return sorted(t, key=lambda s: (-t[s], last[s]))[:k]\n'),
  ('x-nlargest-set', 'heapq.nlargest over a set of names', 'import heapq\ndef busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + abs(q)\n    return heapq.nlargest(k, set(t), key=lambda s: t[s])\n'),
  ('alt:x-nlargest-dict', 'heapq.nlargest over the dict, which is stable in first-seen order', 'import heapq\ndef busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + abs(q)\n    return heapq.nlargest(k, t, key=lambda s: t[s])\n'),
 ],
}


def load(n, rev=None):
    path = f'app/content/bank/coding-{n}.json'
    txt = subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True, text=True, check=True).stdout if rev else open(path).read()
    return {it['id']: it for it in json.loads(txt)['items'] if it['widget']['kind'] == 'code'}


def main():
    ids = sys.argv[1:] or list(TASKS)
    bad = False
    tried = passing = 0
    for iid in ids:
        n, k = TASKS[iid]
        now, old = load(n)[iid]['widget'], load(n, FIX + '^')[iid]['widget']
        tests, otests = now['tests'], old['tests']
        changed = [i + 1 for i, (a, b) in enumerate(zip(tests, otests)) if a != b] + list(range(len(otests) + 1, len(tests) + 1))
        print(f'\n## coding-{n} {iid}: {len(tests)} tests now, {len(otests)} before; changed {changed}')
        if changed != [k]:
            print('  CHANGED TESTS NOT AS THE FIX PASS LISTS'); bad = True
        print(f'  before {json.dumps(otests[k - 1], ensure_ascii=False)[:230]}')
        print(f'  now    {json.dumps(tests[k - 1], ensure_ascii=False)[:230]}')
        case = tests[k - 1]
        env = {}
        exec(case.get('setup', ''), env)
        exp, br = eval(case['expect'], env), BRUTE[iid]()
        print(f'  expect of test {k} by the brute route: {"agrees" if exp == br else "DISAGREES " + repr(br)[:80]}')
        bad |= exp != br
        for nm, src in (('model', now['solution']), ('mine', MINE[iid])):
            r = run(src, now['examples'] + tests)
            ok = all(x[0] for x in r)
            print(f'  {nm:6} {"passes all" if ok else "FAILS"} {sum(x[0] for x in r)} of {len(r)}, slowest {max(x[1] for x in r):.3f} s')
            bad |= not ok
        st = run(now['starter'], tests)
        print(f'  starter fails {sum(not x[0] for x in st)} of {len(st)}')
        bad |= all(x[0] for x in st)
        first = importlib.import_module(f'cands_{n}').CANDS[iid]['wrong']
        pools = (('first', first), ('delta', C[iid]), ('ac2', [c for c in EXTRA[iid] if c[2]]))
        for pool, cands in pools:
            for nm, why, src in cands:
                if pool == 'first' and iid in ADAPT:
                    src = src + ADAPT[iid]
                rn = run(src, tests)
                if all('NameError' in x[2] for x in rn):
                    print(f'  {pool:5} VACUOUS (NameError on every test) {nm}')
                    bad = True
                    continue
                fn = [i + 1 for i, x in enumerate(rn) if not x[0]]
                wrongans = [i + 1 for i, x in enumerate(rn) if not x[0] and 'stopped' not in x[2]]
                if nm.startswith('alt:'):
                    tag = 'alt ok' if not fn else ('alt STOPPED' if not wrongans else 'ALT WRONG ANSWER')
                    if wrongans and pool != 'first':
                        bad = True
                    print(f'  {pool:5} {tag:16} {nm[4:]} {fn or ""} {[rn[i - 1][2] for i in wrongans][:2] if wrongans else ""}')
                    continue
                tried += 1
                if fn and not wrongans or (iid, nm) in KNOWN_PASS:  # slow ones are not run a second time on the old tests
                    print(f'  {pool:5} {"caught" if fn else "PASSES NOW (known, stopped in the page)"} {nm}: {fn}{" for time only" if fn else ""} (slowest {max(x[1] for x in rn):.2f} s)')
                    passing += not fn
                    continue
                ro = run(src, otests)
                fo = [i + 1 for i, x in enumerate(ro) if not x[0]]
                if not fn:
                    passing += 1
                    reg = 'REGRESSION (failed before: %s)' % fo if fo else 'PASSES NOW (and before)'
                    if (iid, nm) in FINDING:
                        reg = 'FINDING ' + reg
                    elif (iid, nm) not in KNOWN_PASS:
                        bad = True
                    print(f'  {pool:5} {reg} {nm}: {why[:90]} (slowest {max(x[1] for x in rn):.2f} s)')
                else:
                    note = '' if wrongans else ' for time only'
                    newly = ' (passed before)' if not fo else ''
                    print(f'  {pool:5} caught {nm}: {fn}{note}{newly}')
    print(f'\ncandidates tried {tried}, passing every test now {passing}; exit {1 if bad else 0}')
    sys.exit(1 if bad else 0)


main()
