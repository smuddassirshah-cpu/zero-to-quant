"""Second computation of every stated number in pack `cpp` (docs/briefs/drills-1.1-1.9.md, pack cpp).

Run from the repo root with the scratchpad venv Python:
    <scratchpad>/venv/bin/python docs/reports/drills-cpp-check.py
For each drill it holds an independent Python model of the C++ function (written apart from the
builder that produced the `expect` values, by another method where one exists) and compares it with
every example and hidden test. Calls that are C++ lambdas are matched by their text to a value
worked out here by hand or by the model. It also checks the brief's worked answer appears in the
brief, the `how` count, examples repeated in the tests, the index rows and the pack mix.
The C++ solution, the starter and the planted solutions are run in the real runtime by
`playthrough.mjs --drill` and `planted-check.mjs --require`; this script does not compile C++.
Exit 0 when everything agrees.
"""
import json, math, os, sys, re, itertools
from fractions import Fraction
from statistics import NormalDist

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DR = os.path.join(ROOT, 'app', 'content', 'drills')
errors = []
MODELS = {}      # id -> function(test) -> expected value
BRIEF = {}       # id -> text that must appear in the brief (the worked answer)


def model(drill_id, brief_answer):
    def deco(f):
        MODELS[drill_id] = f
        BRIEF[drill_id] = brief_answer
        return f
    return deco


def close(a, b, rel=1e-9, ab=1e-12):
    if isinstance(a, list):
        return isinstance(b, list) and len(a) == len(b) and all(close(x, y, rel, ab) for x, y in zip(a, b))
    return abs(a - b) <= max(rel * max(abs(a), abs(b)), ab)


# ------------------------------------------------------------------ cpp-fee-pence
@model('cpp-fee-pence', 'the answer is 62')
def _(t):
    n, b = t['args']
    return math.ceil(Fraction(n * b, 10000))


# ------------------------------------------------------------------ cpp-longest-rise
@model('cpp-longest-rise', 'The answer is 3')
def _(t):
    xs = t['args'][0]
    ups = [b > a for a, b in zip(xs, xs[1:])]
    return max([len(list(g)) for k, g in itertools.groupby(ups) if k] or [0])


# ------------------------------------------------------------------ cpp-fill-csv
def _whole(s, minus):
    if minus and s.startswith('-'):
        s = s[1:]
    return len(s) > 0 and all('0' <= c <= '9' for c in s)


@model('cpp-fill-csv', 'The answer is 151,400')
def _(t):
    text = t['args'][0]
    total = 0
    for raw in text.split('\n'):
        line = raw[:-1] if raw[-1:] == '\r' else raw
        if line.count(',') != 1:
            continue
        q, p = line.split(',')
        if _whole(q, True) and _whole(p, False):
            total += int(q) * int(p)
    return total


# ------------------------------------------------------------------ cpp-temp-limit
def _nest(start, caps):
    rec, stack, lim = [], [], start
    for c in caps:                       # open each block inside the last
        stack.append(lim)
        lim = min(lim, c)
        rec.append(lim)
    while stack:                         # close the innermost; record unless it was the outermost
        lim = stack.pop()
        if stack:
            rec.append(lim)
    rec.append(lim)
    return rec


@model('cpp-temp-limit', '{200, 200, 50, 200, 200, 500}')
def _(t):
    if 'compiles' in t:
        return False                     # a copy of TempLimit must not compile
    if t['call'] == 'nest':
        return _nest(*t['args'])
    if t['call'] == 'siblings':
        start, caps = t['args']
        out = []
        for c in caps:
            out += [c if c < start else start, start]
        return out
    if 'make_unique<TempLimit>(lim, 1)' in t['call']:
        return [1, 7]                    # 7 lowered to 1, then reset() restores 7
    if 'TempLimit x(a, 10)' in t['call']:
        return [10, 20, 50, 60]          # two limits, each restored on leaving the block
    raise KeyError(t['call'])


# ------------------------------------------------------------------ cpp-take-all
@model('cpp-take-all', '`Fill::copies` is still 0')
def _(t):
    if t['call'] == 'run_take':
        m, n = t['args']
        dst = [('a%d' % i, i + 1) for i in range(m)]
        src = [('b%d' % i, i + 1) for i in range(n)]
        dst.extend(src)
        src = []
        return ['0', str(len(dst)), str(len(src))] + ['%s:%d' % f for f in dst]
    if 'make_fills("b", 400)' in t['call']:
        return [0, 405, 0, 400]          # no copies, 5 + 400 fills, src empty, the last fill is b399 with qty 400
    if 's.emplace_back("c0", 9)' in t['call']:
        return 'b0 b1 c0 0'
    raise KeyError(t['call'])


# ================================================================== driver
def main():
    files = sorted(f for f in os.listdir(DR) if f.startswith('cpp-') and f.endswith('.json'))
    index = {r['id']: r for r in json.load(open(os.path.join(DR, 'index.json')))}
    mix = {}
    checked = 0
    for f in files:
        d = json.load(open(os.path.join(DR, f)))
        i = d['id']
        if i not in MODELS:
            errors.append(f'{i}: no model in this script')
            continue
        if d.get('pack') != 'cpp' or d.get('language') != 'cpp':
            errors.append(f'{i}: pack or language')
        if d['course'] not in ('cpp', 'cpp-pricing'):
            errors.append(f'{i}: course {d["course"]}')
        row = index.get(i)
        if not row or row['name'] != d['name'] or row['course'] != d['course'] or row['difficulty'] != d['difficulty']:
            errors.append(f'{i}: index row disagrees with the file')
        if not 300 <= d['pace'] <= 1200:
            errors.append(f'{i}: pace {d["pace"]}')
        mix.setdefault(d['course'], {}).setdefault(d['difficulty'], 0)
        mix[d['course']][d['difficulty']] += 1
        if not d['how'].startswith(f'Submit runs {len(d["tests"])} hidden tests.'):
            errors.append(f'{i}: how count')
        if BRIEF[i] not in d['brief']:
            errors.append(f'{i}: worked answer {BRIEF[i]!r} not in the brief')
        if len(d.get('planted', [])) < 2:
            errors.append(f'{i}: fewer than two planted')
        calls = [json.dumps({k: v for k, v in t.items() if k != 'note'}, sort_keys=True) for t in d['tests']]
        for ex in d['examples']:
            key = json.dumps({k: v for k, v in ex.items() if k != 'note'}, sort_keys=True)
            if key not in calls:
                errors.append(f'{i}: example {ex.get("call")} is not also a hidden test')
        for kind in ('examples', 'tests'):
            for n, t in enumerate(d[kind]):
                want = MODELS[i](t)
                got = t['expect']
                ok = close(want, got) if t.get('compare') == 'isclose' else want == got
                if not ok:
                    errors.append(f'{i} {kind}[{n}]: file {got!r}, model {want!r}')
                checked += 1
    print('mix', json.dumps(mix, sort_keys=True))
    print(f'{len(files)} drills, {checked} cases compared')
    for e in errors:
        print('ERROR', e)
    print(f'errors: {len(errors)}')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
