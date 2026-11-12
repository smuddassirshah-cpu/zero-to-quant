"""Shared helpers for the delta read of the problems fix passes (estimation, regression, testing, vectors)."""
import json, glob, re, sys

_docs = {}
checks = fails = 0
findings = []


def item(course, iid):
    for f in sorted(glob.glob(f'app/content/courses/{course}/problems-*.json')):
        d = _docs.get(f) or _docs.setdefault(f, json.load(open(f)))
        for it in d['items']:
            if it['id'] == iid:
                return it
    raise KeyError(iid)


def part(course, iid, k):
    return item(course, iid)['parts'][k - 1]


def W(course, iid, k):
    return part(course, iid, k)['widget']


def wrong(course, iid, k, wid):
    for x in W(course, iid, k).get('wrong', []):
        if x['id'] == wid:
            return x
    raise KeyError(f'{iid} {k} {wid}')


def ok(cond, msg, finding=None):
    """A check. With finding set, a failure is printed as FINDING (recorded in the review) and does not fail the run."""
    global checks, fails
    checks += 1
    if cond:
        return True
    if finding:
        findings.append(msg)
        print(f'FINDING {msg}   [{finding}]')
    else:
        fails += 1
        print(f'FAIL    {msg}')
    return False


def near(a, b, tol=1e-9):
    return abs(a - b) <= tol


def key(course, iid, k, value, slack=None, finding=None):
    """The stored answer equals my value to within the part's own band (or slack)."""
    w = W(course, iid, k)
    t = slack if slack is not None else max(w.get('tol', {}).get('abs', 0), 1e-12)
    return ok(abs(w['answer'] - value) <= t + 1e-12, f'{course} {iid} part {k}: key {w["answer"]} against my {value:.8g} (band {t})', finding)


def slip(course, iid, k, wid, value, finding=None):
    """A wrong entry's stored value sits within its own band of my value for the slip, and its band is clear of the key's."""
    w = W(course, iid, k)
    x = wrong(course, iid, k, wid)
    t = x.get('tol', {}).get('abs', 0)
    a = ok(abs(x['value'] - value) <= t + 1e-12, f'{course} {iid} part {k}: wrong {wid} {x["value"]} +- {t} against my {value:.8g}', finding)
    kt = w.get('tol', {}).get('abs', 0)
    b = ok(abs(x['value'] - w['answer']) > t + kt, f'{course} {iid} part {k}: wrong {wid} band clear of the key band', finding)
    return a and b


def bands_clear(course, iid, k):
    """No two wrong bands of the part overlap."""
    ws = W(course, iid, k).get('wrong', [])
    for i, a in enumerate(ws):
        for b in ws[i + 1:]:
            ok(abs(a['value'] - b['value']) > a.get('tol', {}).get('abs', 0) + b.get('tol', {}).get('abs', 0),
               f'{course} {iid} part {k}: wrong bands {a["id"]} and {b["id"]} do not meet')


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ('id', 'kind', 'keyboard', 'layout', 'skills', 'placeholder', 'unit'):
                yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def text(o):
    return '\n'.join(strings(o))


def says(o, s, msg=None, finding=None):
    return ok(s in text(o), msg or f'text holds "{s}"', finding)


NUM = re.compile(r'(?<![A-Za-z_\\])-?\d+(?:\.\d+)?')


def numbers(o):
    """Every number written in an object's strings (thousands separators of TeX and prose joined up)."""
    out = set()
    for s in strings(o):
        s = s.replace('{,}', '').replace('\\\\', ' ').replace('\\,', ' ')
        s = re.sub(r'(?<=\d),(?=\d{3}\b)', '', s)
        s = re.sub(r'\$-(?=\d)', '$ -', s)
        for m in NUM.finditer(s):
            out.add(m.group().lstrip('-'))
    return out


def stale(o, known, where):
    """Every number written in a re-authored item or part is one I derived (known: values, matched as printed)."""
    k = {str(x) for x in known}
    unknown = sorted(numbers(o) - k, key=lambda x: float(x))
    ok(not unknown, f'{where}: every printed number is one of mine; not derived: {unknown}')


def done(name):
    print(f'{name}: {checks} checks, {fails} failures, {len(findings)} FINDING rows (recorded in the review)')
    sys.exit(1 if fails else 0)
