"""Run every code widget's solution and starter against its hidden tests in CPython."""
import json, math, glob, sys

DIR = '/home/user/zero-to-quant/app/content/courses/mental-pressure/'
FILES = ['l9-eighty-in-eight.json', 'l10-next-in-sequence.json', 'l11-word-problems.json', 'l12-mock-test.json', 'review-3.json', 'homework-3.json']


def close(a, b, tol):
    rel = tol.get('rel', 1e-9 if 'abs' not in tol else 0)
    ab = tol.get('abs', 0 if 'rel' in tol else 1e-12)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    try:
        return math.isclose(a, b, rel_tol=rel, abs_tol=ab)
    except TypeError:
        return False


def run(code, w, t):
    ns = {'__learner_source__': code}
    if w.get('prelude'):
        exec(w['prelude'], ns)
    exec(code, ns)
    if w.get('postlude'):
        exec(w['postlude'], ns)
    if t.get('setup'):
        exec(t['setup'], ns)
    got = eval(t['call'], ns)
    exp = eval(t['expect'], ns)
    if t.get('compare') == 'isclose':
        return close(got, exp, t.get('tol', {}))
    return got == exp


def widgets(o):
    if isinstance(o, dict):
        if o.get('kind') == 'code':
            yield o
        for v in o.values():
            yield from widgets(v)
    elif isinstance(o, list):
        for v in o:
            yield from widgets(v)


bad = 0
for f in FILES:
    d = json.load(open(DIR + f))
    for w in widgets(d):
        sol = [run(w['solution'], w, t) for t in w['tests']]
        st = []
        for t in w['tests']:
            try:
                st.append(run(w['starter'], w, t))
            except Exception:
                st.append(False)
        ex = []
        for t in w.get('examples', []):
            ex.append(run(w['solution'], w, t))
        print(f, w['starter'].split('(')[0][4:], 'solution', sum(sol), '/', len(sol), 'examples ok' if all(ex) else 'EXAMPLES FAIL',
              'starter passes', [w['tests'][i]['call'] for i, s in enumerate(st) if s])
        if not all(sol) or not all(ex) or all(st):
            bad += 1
            for i, s in enumerate(sol):
                if not s:
                    print('   FAIL', w['tests'][i])
print('problems:', bad)
