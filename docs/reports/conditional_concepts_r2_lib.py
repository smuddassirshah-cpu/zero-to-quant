"""Helpers for the round 2 concept audit of course `conditional` (levels 1 to 3).

Written from scratch by the round 2 auditor. Every check recomputes a value
independently (exact enumeration with Fractions, a closed form, or a seeded
Monte Carlo run) and compares it with what the content JSON states.

Usage in a script:
    from conditional_concepts_r2_lib import *
    A('l1-what-changes', 'screens[3]', F(1, 3), before=F(1, 6), half=F(1, 2))
    done()
"""
import json
import math
import os
import random
import re
import sys
from fractions import Fraction as F
from itertools import product, permutations, combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'conditional'))
_cache = {}
_fails = []
_count = [0]


def load(name):
    if name not in _cache:
        with open(os.path.join(ROOT, name + '.json'), encoding='utf-8') as fh:
            _cache[name] = json.load(fh)
    return _cache[name]


def get(name, path):
    """Navigate 'screens[3].widget.answer' or 'items[0].parts[1].widget'."""
    node = load(name)
    for part in re.findall(r'[^.\[\]]+|\[\d+\]', path):
        if part.startswith('['):
            node = node[int(part[1:-1])]
        else:
            node = node[part]
    return node


def ok(label, cond):
    _count[0] += 1
    if not cond:
        _fails.append(label)
        print('FAIL', label)


def close(a, b, tol):
    return abs(float(a) - float(b)) <= tol + 1e-12


def _tol(widget, default=None):
    t = widget.get('tol') if isinstance(widget, dict) else None
    if isinstance(t, dict) and 'abs' in t:
        return max(float(t['abs']), 1e-9)
    return default if default is not None else 1e-9


def A(name, base, expected, /, **wrongs):
    """Numeric widget: the key equals `expected` within the widget's own
    tolerance, the stated key is itself a faithful rounding (5e-5 relative to
    the tolerance), and each named wrong value equals its recomputed slip.
    No wrong value may fall inside the key's accepted band."""
    w = get(name, base + '.widget')
    tol = _tol(w, 1e-9)
    ok(f'{name} {base} answer {w["answer"]} vs {float(expected):.6g}', close(w['answer'], expected, tol))
    listed = {x['id']: x for x in w.get('wrong', [])}
    for wid, val in wrongs.items():
        if wid not in listed:
            ok(f'{name} {base} wrong[{wid}] missing', False)
            continue
        wt = _tol(listed[wid], 1e-9)
        ok(f'{name} {base} wrong[{wid}] {listed[wid]["value"]} vs {float(val):.6g}',
           close(listed[wid]['value'], val, max(wt, 6e-5)))
    for wid, x in listed.items():
        if wid not in wrongs:
            ok(f'{name} {base} wrong[{wid}] not recomputed', False)
        wt = _tol(x, 0.0) if 'tol' in x else 0.0
        ok(f'{name} {base} wrong[{wid}] overlaps the accepted band',
           abs(float(x['value']) - float(w['answer'])) > tol + wt - 1e-12)


def texnum(text):
    """First number in an option text: \\dfrac{a}{b}, \\tfrac{a}{b}, a/b or a decimal."""
    m = re.search(r'\\[dt]?frac\{(\d+)\}\{(\d+)\}', text)
    if m:
        return F(int(m.group(1)), int(m.group(2)))
    m = re.search(r'(?<![\w.])(\d+(?:\.\d+)?)', text.replace(',', ''))
    if m:
        return F(m.group(1))
    return None


def C(name, base, correct_id, value=None, /, **others):
    """Choice widget: exactly the option `correct_id` is marked correct.
    `value` (optional) is the recomputed value the correct option must show.
    `others` map wrong option ids to the recomputed slip values they show."""
    opts = get(name, base + '.widget.options')
    marked = [o['id'] for o in opts if o.get('correct')]
    ok(f'{name} {base} correct option {marked} vs {correct_id}', marked == [correct_id])
    byid = {o['id']: o for o in opts}
    if value is not None:
        got = texnum(byid[correct_id]['text'])
        ok(f'{name} {base} option {correct_id} shows {got} vs {float(value):.5g}',
           got is not None and close(got, value, 6e-3))
    for oid, val in others.items():
        got = texnum(byid[oid]['text']) if oid in byid else None
        ok(f'{name} {base} option {oid} shows {got} vs {float(val):.5g}',
           got is not None and close(got, val, 6e-3))


def M(name, base, correct_ids):
    """Multi-select widget: the set of options marked correct."""
    opts = get(name, base + '.widget.options')
    marked = sorted(o['id'] for o in opts if o.get('correct'))
    ok(f'{name} {base} multi {marked} vs {sorted(correct_ids)}', marked == sorted(correct_ids))


def TB(name, base, cells):
    """Table widget: cells maps (row, col) to the recomputed value."""
    rows = get(name, base + '.widget.rows')
    seen = set()
    for (r, c), val in cells.items():
        cell = rows[r][c]
        seen.add((r, c))
        ok(f'{name} {base} cell r{r}c{c} {cell.get("answer")} vs {float(val):.6g}',
           isinstance(cell, dict) and close(cell['answer'], val, _tol(cell, 1e-9)))
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            if isinstance(cell, dict) and cell.get('edit') and (r, c) not in seen:
                ok(f'{name} {base} cell r{r}c{c} not recomputed', False)


def TAP(name, base, expected):
    w = get(name, base + '.widget')
    ok(f'{name} {base} tap {sorted(w["answer"])} vs {sorted(expected)}', sorted(w['answer']) == sorted(expected))


def ORD(name, base, expected):
    w = get(name, base + '.widget')
    ok(f'{name} {base} order {w["answer"]}', list(w['answer']) == list(expected))


def S(name, path, fragment, cond=True):
    """A sentence claim: `fragment` must still be in the text at `path` (so the
    check tracks the content), and `cond` is the recomputed truth of the claim."""
    text = get(name, path)
    if isinstance(text, list):
        text = ' '.join(str(t) for t in text)
    present = fragment in str(text)
    ok(f'{name} {path} text no longer has "{fragment}"', present)
    ok(f'{name} {path} claim "{fragment}" is false on recomputation', bool(cond))


# ---------- generic tree canvases ----------

def _pnum(s):
    return F(str(s).replace(',', '').strip())


def _walk_canvases(node, path, out):
    if isinstance(node, dict):
        if node.get('kind') == 'tree' and isinstance(node.get('params'), dict):
            out.append((path, node))
        for k, v in node.items():
            _walk_canvases(v, path + '.' + k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk_canvases(v, f'{path}[{i}]', out)


def trees(name, stated_leaves=()):
    """Every tree canvas in the file: the branches out of each node add to 1
    (or to the parent count on a counts tree), and each stated leaf equals the
    product of the branches on its path. `stated_leaves` lists canvas paths
    whose prose says the leaves show something else (checked by hand)."""
    found = []
    _walk_canvases(load(name), '', found)
    for path, canvas in found:
        prm = canvas['params']
        if 'levels' in prm:
            counts = 'rootLabel' in prm
            root_total = None
            if counts:
                root_total = _pnum(re.search(r'[\d,]+', prm['rootLabel']).group(0))
            paths = {'': (root_total if counts else F(1))}
            for level in prm['levels']:
                new = {}
                for parent, pval in paths.items():
                    tot = F(0)
                    for br in level['branches']:
                        p = br['p']
                        if isinstance(p, dict):
                            if parent not in p:
                                continue
                            p = p[parent]
                        p = _pnum(p)
                        tot += p
                        key = (parent + '-' + br['id']) if parent else br['id']
                        new[key] = p if counts else pval * p
                    target = pval if counts else F(1)
                    ok(f'{name}{path} node "{parent}" branches add to {float(tot):.6g}, want {float(target):.6g}',
                       tot == target)
                paths = new
            for leaf, val in prm.get('leaves', {}).items():
                if counts or any(path.startswith('.' + sl) for sl in stated_leaves):
                    continue
                ok(f'{name}{path} leaf {leaf} {val} vs {float(paths.get(leaf, -1)):.6g}',
                   leaf in paths and close(_pnum(val), paths[leaf], 6e-5))
        elif 'nodes' in prm:
            nodes = prm['nodes']
            kids = nodes['children'] if isinstance(nodes, dict) else nodes

            def rec(children, where):
                tot = sum(_pnum(c['p']) for c in children)
                ok(f'{name}{path} node "{where}" branches add to {float(tot):.6g}', tot == 1)
                for c in children:
                    if c.get('children'):
                        rec(c['children'], where + '-' + c['id'])
            rec(kids, 'root')
    return len(found)


# ---------- probability helpers ----------

def binom_pmf(n, k, p):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def binom_tail(k, n, p):
    return sum(binom_pmf(n, j, p) for j in range(k, n + 1))


def bayes(prior, hit, false):
    """P(H | E) from P(H), P(E | H), P(E | not H)."""
    return prior * hit / (prior * hit + (1 - prior) * false)


def odds(p):
    return p / (1 - p)


def from_odds(o):
    return o / (1 + o)


def posterior(priors, liks):
    prods = [a * b for a, b in zip(priors, liks)]
    tot = sum(prods)
    return [x / tot for x in prods]


def cond(space, event, given):
    """P(event | given) on a list of equally likely outcomes."""
    kept = [o for o in space if given(o)]
    return F(sum(1 for o in kept if event(o)), len(kept))


def prob(space, event):
    return F(sum(1 for o in space if event(o)), len(space))


def wprob(dist, event, given=lambda o: True):
    """Weighted outcome space: dist is a list of (outcome, weight)."""
    den = sum(w for o, w in dist if given(o))
    num = sum(w for o, w in dist if given(o) and event(o))
    return num / den


def mc(trial, n, seed):
    """Share of n seeded trials for which trial(rng) is true."""
    rng = random.Random(seed)
    return sum(1 for _ in range(n) if trial(rng)) / n


def mc_cond(trial, n, seed):
    """trial(rng) returns (given, event). Returns the conditional frequency."""
    rng = random.Random(seed)
    g = e = 0
    for _ in range(n):
        a, b = trial(rng)
        if a:
            g += 1
            e += 1 if b else 0
    return e / g


def expect_of(test):
    """`expect` is a Python expression held as text (AUTHORING, code widgets)."""
    e = test['expect']
    return eval(e) if isinstance(e, str) else e


def run_code(name, base, namespace_fn):
    """Run a code widget for real: the solution passes every hidden test and
    example, and the starter fails at least one."""
    w = get(name, base + '.widget')

    def passes(src):
        ns = {}
        try:
            exec(src, ns)
        except Exception:
            return 0, len(w['tests'])
        good = 0
        for t in w['tests'] + w.get('examples', []):
            try:
                got = eval(t['call'], ns)
                if math.isclose(got, expect_of(t), rel_tol=1e-9, abs_tol=1e-12):
                    good += 1
            except Exception:
                pass
        return good, len(w['tests']) + len(w.get('examples', []))

    g, n = passes(w['solution'])
    ok(f'{name} {base} solution passes {g}/{n}', g == n)
    g2, n2 = passes(w['starter'])
    ok(f'{name} {base} starter passes {g2}/{n2} (must fail at least one)', g2 < n2)
    ns = {}
    exec(w['solution'], ns)
    fn = ns[namespace_fn]
    return fn, w


def done():
    print(f'{_count[0]} checks, {len(_fails)} failed')
    sys.exit(1 if _fails else 0)
