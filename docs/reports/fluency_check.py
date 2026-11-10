"""Shared checker for the Fluency number scripts of topics 1.5 and 1.6 (docs/briefs/fluency.md check 1, second wave).

A course script imports `Checker`, registers one derive function per family and calls `run()`:

    ck = Checker('markov')
    ck.add('fluency-l2-transition-matrix', 'two-state-two-step', derive)
    ck.run()

For each family it reads `node tools/fluency-sample.mjs --set <course>/<set> --family <id> --n N --json` (N = 200, or
`--n`), turns the drawn `vars` into exact sympy Rationals (decimals stay exact: 0.1 is 1/10) and calls derive(V), which
must return (key, wrongs): key is a number (or a tuple for a set answer), wrongs a dict {wrong id: value} holding
exactly the slips the family should offer on that draw (a tuple for a set answer). Derive functions never read `lets`
or the printed answer. The checker then asserts:
  - the engine's answer (or answers, in any order) equals the key, to 1e-9 relative;
  - the engine offers exactly the expected wrong ids, each equal to the derived slip;
  - each wrong lies outside the widget tolerance plus its own tolerance of the key, and no two wrongs coincide;
  - the drawn prompt, answer, accept line, solution and wrong lines hold none of `+-`, `--`, `+ -`, `^{1}`, a stray
    `+0`, a `1x` or `0x` coefficient, and every `\\frac{n}{d}` of whole numbers is in lowest terms.
Exit 0 when every check passes.
"""
import json
import math
import os
import re
import subprocess
import sys

import sympy as sp

APP = os.environ.get('FLUENCY_APP') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 200
BAD = [r'(?<![\d.])1[a-z]', r'\+-', r'--', r'\^\{1\}', r'\+0(?![.\d])', r'(?<![\d.])0[a-z]', r'\+\s*-', r'-\s*-']
FRAC = re.compile(r'\\frac\{(-?\d+)\}\{(\d+)\}')


def rat(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, int):
        return sp.Integer(v)
    if isinstance(v, float):
        return sp.Rational(repr(v))
    return v


def num(x):
    return float(sp.N(x, 30)) if not isinstance(x, (int, float)) else float(x)


def close(a, b, rel=1e-9):
    a, b = num(a), num(b)
    return abs(a - b) <= rel * max(1.0, abs(a), abs(b))


def phi(z):
    """Standard normal CDF from the error function (independent of the prompt's table value)."""
    return 0.5 * (1 + math.erf(float(z) / math.sqrt(2)))


class Checker:
    def __init__(self, course):
        self.course = course
        self.fams = []
        self.fails = []
        self.checked = 0

    def add(self, set_id, fam, derive):
        self.fams.append((set_id, fam, derive))

    def sample(self, set_id, fam):
        out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', self.course + '/' + set_id, '--family', fam,
                              '--n', str(N), '--json'], cwd=APP, capture_output=True, text=True, check=True).stdout
        return json.loads(out)['items']

    def fail(self, msg):
        self.fails.append(msg)

    def scan(self, label, texts):
        for t in texts:
            if not isinstance(t, str):
                continue
            plain = re.sub(r'\\[a-zA-Z]+', ' ', t)
            for pat in BAD:
                if re.search(pat, plain):
                    self.fail('%s: pattern %s in %r' % (label, pat, t))
            for n_, d_ in FRAC.findall(t):
                if math.gcd(abs(int(n_)), int(d_)) != 1 or int(d_) == 1:
                    self.fail('%s: unreduced \\frac{%s}{%s} in %r' % (label, n_, d_, t))

    def check_item(self, set_id, fam, it, derive):
        label = '%s/%s seed %s' % (set_id, fam, it['seed'])
        V = {k: rat(v) for k, v in it['vars'].items()}
        key, wrongs = derive(V)
        tol = it.get('tol') or {'abs': 0}
        wtexts = [w['line'] for w in it['wrong']]
        self.scan(label, [it['prompt'], it.get('accept')] + it['solution'] + wtexts)
        self.checked += 1
        if isinstance(key, tuple):
            got = sorted(float(x) for x in it['answers'])
            want = sorted(num(x) for x in key)
            if len(got) != len(want) or not all(close(g, w) for g, w in zip(got, want)):
                self.fail('%s: key %s, engine %s' % (label, want, got))
        else:
            if not close(it['answer'], key):
                self.fail('%s: key %s (%s), engine %s' % (label, key, num(key), it['answer']))
        ids = [w['id'] for w in it['wrong']]
        if sorted(ids) != sorted(wrongs):
            self.fail('%s: wrong ids %s, expected %s' % (label, ids, sorted(wrongs)))
        seen = []
        for w in it['wrong']:
            if w['id'] not in wrongs:
                continue
            self.checked += 1
            want = wrongs[w['id']]
            wt = (w.get('tol') or {}).get('abs', 0)
            reach = tol.get('abs', 0) + wt + 1e-9
            if isinstance(want, tuple):
                vals = sorted(float(x) for x in str(w['value']).split(','))
                wv = sorted(num(x) for x in want)
                if not all(close(a, b) for a, b in zip(vals, wv)):
                    self.fail('%s: wrong %s, expected %s, engine %s' % (label, w['id'], wv, vals))
                kv = sorted(num(x) for x in key)
                if all(abs(a - b) <= reach for a, b in zip(vals, kv)):
                    self.fail('%s: wrong %s grades as the key' % (label, w['id']))
                seen.append(tuple(vals))
            else:
                wv = float(w['value'])
                if not close(wv, want):
                    self.fail('%s: wrong %s, expected %s, engine %s' % (label, w['id'], num(want), wv))
                if abs(wv - num(key)) <= reach:
                    self.fail('%s: wrong %s within tolerance of the key' % (label, w['id']))
                seen.append(round(wv, 12))
        if len(set(seen)) != len(seen):
            self.fail('%s: two wrongs coincide %s' % (label, seen))

    def run(self):
        for set_id, fam, derive in self.fams:
            for it in self.sample(set_id, fam):
                self.check_item(set_id, fam, it, derive)
        print('%s: %d checks over %d families, %d failures' % (self.course, self.checked, len(self.fams), len(self.fails)))
        for f in self.fails[:30]:
            print('FAIL', f)
        sys.exit(1 if self.fails else 0)
