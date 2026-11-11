"""Helper for the conditional concept-audit scripts (conditional-L1/L2/L3-concepts.py).

Each script recomputes a claim from first principles (exact enumeration with fractions, or a
seeded Monte Carlo run) and compares it with what the content JSON says. Nothing here edits content.
A check that fails because the content is wrong stays failing: the script then exits 1.
"""
import json
import os
import re
import sys
from fractions import Fraction as F

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'conditional')
_cache = {}
fails = []
count = [0]


def load(name):
    if name not in _cache:
        with open(os.path.join(COURSE, name + '.json'), encoding='utf-8') as fh:
            _cache[name] = json.load(fh)
    return _cache[name]


def get(name, path):
    node = load(name)
    for key, idx in re.findall(r'([A-Za-z_][\w-]*)|\[(\d+)\]', path):
        node = node[key] if key else node[int(idx)]
    return node


def ok(cond, label, note=''):
    count[0] += 1
    if not cond:
        fails.append(label + (' :: ' + note if note else ''))
        print('FAIL ' + label + (' :: ' + note if note else ''))


def _val(text):
    """First fraction or decimal in an option's text, as a float."""
    m = re.search(r'\\[dt]?frac\{([^{}]+)\}\{([^{}]+)\}', text)
    if m:
        return float(m.group(1)) / float(m.group(2))
    m = re.search(r'-?\d+(?:\.\d+)?', text.replace('{,}', ''))
    return float(m.group(0)) if m else None


def key(name, path):
    """The graded key of the widget at screen/item/part `path`."""
    w = get(name, path)['widget']
    k = w['kind']
    if k == 'numeric':
        return float(w['answer'])
    if k == 'choice':
        right = [o for o in w['options'] if o.get('correct')]
        assert len(right) == 1, (name, path)
        return _val(right[0]['text'])
    if k == 'expression':
        return _val(w['answer'])
    raise ValueError(k)


def eq(name, path, value, atol=6e-4):
    """The key at path equals the recomputed value."""
    got = key(name, path)
    ok(got is not None and abs(got - float(value)) <= atol, f'{name} {path} key',
       f'content {got!r}, recomputed {float(value):.6g}')


def cid(name, path, want):
    """The correct option id(s), tap answer or order answer at path."""
    w = get(name, path)['widget']
    if w['kind'] in ('choice', 'multi'):
        got = sorted(o['id'] for o in w['options'] if o.get('correct'))
    else:
        got = sorted(w['answer']) if w['kind'] != 'order' else list(w['answer'])
    want = sorted(want) if w['kind'] != 'order' else list(want)
    ok(got == want, f'{name} {path} correct set', f'content {got}, recomputed {want}')


def tab(name, path, values, atol=6e-4):
    """Editable table cells, row by row, equal the recomputed values."""
    w = get(name, path)['widget']
    got = [float(c['answer']) for r in w['rows'] for c in r if isinstance(c, dict) and c.get('edit')]
    good = len(got) == len(values) and all(abs(a - float(b)) <= atol for a, b in zip(got, values))
    ok(good, f'{name} {path} table', f'content {got}, recomputed {[round(float(v), 6) for v in values]}')


def says(name, path, phrase):
    """True while the phrase is still in the text at path (for claims tied to wording)."""
    def strings(x):
        if isinstance(x, str):
            return [x]
        if isinstance(x, dict):
            return [s for v in x.values() for s in strings(v)]
        if isinstance(x, list):
            return [s for v in x for s in strings(v)]
        return []
    return phrase in '\n'.join(strings(get(name, path)))


def pr(space, a):
    """P(a) on a list of equally likely outcomes."""
    return F(sum(1 for s in space if a(s)), len(space))


def cond(space, a, b):
    """P(a | b) on a list of equally likely outcomes."""
    left = [s for s in space if b(s)]
    return F(sum(1 for s in left if a(s)), len(left))


def wpr(dist, a):
    """P(a) on a dict outcome -> probability."""
    return sum(p for s, p in dist.items() if a(s))


def wcond(dist, a, b):
    return wpr(dist, lambda s: a(s) and b(s)) / wpr(dist, b)


def report(tag):
    print(f'{tag}: {count[0]} checks, {len(fails)} failed')
    sys.exit(1 if fails else 0)
