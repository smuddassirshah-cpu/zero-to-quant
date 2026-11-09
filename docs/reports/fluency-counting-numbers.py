"""Recompute every Fluency family of the counting course from the drawn variables alone (docs/briefs/fluency.md check 1).

Run from anywhere with a Python that has sympy:
    <scratchpad>/venv/bin/python docs/reports/fluency-counting-numbers.py [--n 200]
For each family it reads `node tools/fluency-sample.mjs --set counting/<set> --family <id> --n N --json`, derives the
key again from `vars` only (never from the printed answer), by brute-force enumeration with itertools where the count
is small enough and by sympy's `ff`/`binomial` otherwise, checks it equals the engine's answer, and checks each
`wrong` equals the slip recomputed from the vars and differs from the key. It also scans the drawn text for `1x`,
`+-`, `--`, `x^{1}` and `+0`. Exit 0 when all agree.
"""
import itertools
import json
import os
import re
import subprocess
import sys

import sympy as sp

APP = os.environ.get('FLUENCY_APP') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 200
fails = []
checked = 0
BAD = [r'(?<![\d.])1[a-z]', r'\+-', r'--', r'\^\{1\}', r'\+0(?![.\d])', r'(?<![\d.])0[a-z]', r'\+\s*-']
ENUM_LIMIT = 20000


def rat(v):
    return sp.nsimplify(v, rational=True) if isinstance(v, float) else sp.Integer(v) if isinstance(v, int) else sp.Rational(str(v))


def sample(set_id, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', 'counting/' + set_id, '--family', fam,
                          '--n', str(N), '--json'], cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def scan(label, texts):
    for t in texts:
        plain = re.sub(r'\\[a-zA-Z]+', ' ', str(t))
        for pat in BAD:
            if re.search(pat, plain):
                fails.append('%s: pattern %s in %r' % (label, pat, t))


def ordered(n, r):
    """ordered picks of r from n, counted by enumeration when small, else as a falling factorial."""
    n, r = int(n), int(r)
    if sp.ff(n, r) <= ENUM_LIMIT:
        return sp.Integer(sum(1 for _ in itertools.permutations(range(n), r)))
    return sp.ff(n, r)


def unordered(n, r):
    n, r = int(n), int(r)
    if sp.binomial(n, r) <= ENUM_LIMIT:
        return sp.Integer(sum(1 for _ in itertools.combinations(range(n), r)))
    return sp.binomial(n, r)


def check(set_id, fam, derive):
    global checked
    for it in sample(set_id, fam):
        V = {kk: (rat(v) if isinstance(v, (int, float)) else v) for kk, v in it['vars'].items()}
        key, wrongs = derive(V)
        label = '%s/%s seed %s' % (set_id, fam, it['seed'])
        scan(label, [it['prompt'], it['answer']] + it['solution'] + [w['line'] for w in it['wrong']])
        got = sp.Rational(str(it['answer']))
        tol = (it.get('tol') or {}).get('abs', 0)
        checked += 1
        if got != key:
            fails.append('%s: key %s, engine %s' % (label, key, it['answer']))
        if set(w['id'] for w in it['wrong']) != set(wrongs):
            fails.append('%s: wrong ids %s' % (label, [w['id'] for w in it['wrong']]))
        vals = []
        for w in it['wrong']:
            want = wrongs.get(w['id'])
            wv = sp.Rational(str(w['value']))
            vals.append(wv)
            checked += 1
            if want is None or abs(float(wv - want)) > 1e-6 or abs(float(wv - key)) <= tol:
                fails.append('%s: wrong %s, expected %s, engine %s' % (label, w['id'], want, w['value']))
        if len(set(vals)) != len(vals):
            fails.append('%s: two wrongs coincide %s' % (label, vals))


# ---- fluency-l3-choosing-in-order ----
def l3_p(V):
    n, r = V['n'], V['r']
    return ordered(n, r), {'repeats-allowed': n ** r, 'one-factor-short': ordered(n, r - 1)}


def l3_awards(V):
    n, r = V['n'], V['r']
    return ordered(n, r), {'repeats-allowed': n ** r, 'times-places': n * r}


def l3_quotient(V):
    n, g = V['n'], V['g']
    key = sp.factorial(n) / sp.factorial(n - g)
    assert key == sp.prod(range(int(n - g + 1), int(n + 1)))
    return key, {'subtracted': sp.factorial(g), 'divided-the-numbers': sp.Rational(n, n - g)}


# ---- fluency-l4-choosing-without-order ----
def l4_pairs(V):
    n = V['n']
    return unordered(n, 2), {'order-counted': ordered(n, 2), 'n-plus-one': n * (n + 1) / 2}


def l4_binomial(V):
    n, s, f = V['n'], V['s'], V['f']
    r = s if f == 0 else n - s
    key = unordered(n, r)
    assert key == unordered(n, s)
    return key, {'not-divided': ordered(n, s), 'divided-by-s': ordered(n, s) / s}


def l4_committee(V):
    n, r = V['n'], V['r']
    return unordered(n, r), {'order-counted': ordered(n, r), 'divided-by-r': ordered(n, r) / r}


def l4_updown(V):
    n, k = int(V['n']), int(V['k'])
    pats = list(itertools.product('UD', repeat=n))
    key = sp.Integer(sum(1 for p in pats if p.count('U') == k))
    return key, {'all-patterns': sp.Integer(len(pats)), 'order-counted': ordered(n, k)}


FAMILIES = [
    ('fluency-l3-choosing-in-order', 'evaluate-p', l3_p),
    ('fluency-l3-choosing-in-order', 'awards', l3_awards),
    ('fluency-l3-choosing-in-order', 'factorial-quotient', l3_quotient),
    ('fluency-l4-choosing-without-order', 'pairs', l4_pairs),
    ('fluency-l4-choosing-without-order', 'evaluate-binomial', l4_binomial),
    ('fluency-l4-choosing-without-order', 'committee', l4_committee),
    ('fluency-l4-choosing-without-order', 'up-down-patterns', l4_updown),
]

if __name__ == '__main__':
    for set_id, fam, fn in FAMILIES:
        check(set_id, fam, fn)
    print('%d checks over %d families, %d failures' % (checked, len(FAMILIES), len(fails)))
    for f in fails[:30]:
        print('FAIL', f)
    sys.exit(1 if fails else 0)
