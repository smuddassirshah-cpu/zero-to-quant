"""Freshness by key formula and noun: where else in app/content does each problem's setup appear?

fresh-check.mjs compares word runs; this looks for the function or story itself. Run from the repo root.
Prints, per key, the files other than the six sets under review that hold it (the course's lessons, fluency sets, reviews,
homework, and every exam). With --show <course> <regex> it prints the matching strings and their JSON paths.
"""
import glob
import json
import re
import sys

KEYS = {
    'taylor': [r'x\^\{1/3\}|\\sqrt\[3\]', r'27\.81|\b27\b', r'x\^3 \+ x - 3', r'x\^3 [+-] \d*x [+-] \d', r'3[,{}]*700', r'40[,{}]*000 lots|loss limit', r'£3 coupon|3% coupon|4-year',
               r'x\^\{3/2\}', r'4\.4\b', r'\(1 - x\)\^\{-2\}|\(1 - x\)\^2', r'£8 coupon|8% coupon', r'3\.3502|15\.06', r'\\ln 2\.1|\\ln 2\b', r'x = -\\tfrac12|x = -0\.5',
               r'2\^n\}\{n\^2\}', r'n\^2\}', r'\+8\\%|-5\\%|0\.0768', r'e\^\{0\.4\}|T_3', r'1\.8\b|\\ln 2\.8|\\ln 1\.4', r'DV01', r'loan'],
    'multivar': [r'9x\^2 \+ y\^2|x\^2 \+ 9y\^2', r'ellipse', r'x\^3 ?y - 2xy\^2|x\^3 ?y', r'2000P|dollars per pound|exchange rate|US stock', r'x\^2 ?y\b', r'\(3, 2\)|\(12, 9\)',
                 r'\\sqrt\{x\^2 \+ y\^2\}', r'uncorrelated|two books|desk', r'\(3, 4\)|\(0\.6, 0\.8\)', r'4\(a - 1\)\^2|\(b \+ 2\)\^2', r'1 - 8s|1 - 2s',
                 r'2x\^3 - 6xy \+ 3y\^2|x\^3 - 3xy', r'14x \+ 6y|14x', r'momentum|carry', r'0\.09w|volatility 30|30\\%', r'correlation 0\.25|\\rho = 0\.25', r'1\.02|102'],
}
UNDER = {f'app/content/courses/{c}/problems-{n}.json' for c in KEYS for n in (1, 2, 3)}
files = [f for f in glob.glob('app/content/**/*.json', recursive=True) if f not in UNDER and not f.endswith('manifest.json')]


def strings(o, path=''):
    if isinstance(o, dict):
        for kk, v in o.items():
            yield from strings(v, path + '.' + kk)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, f'{path}[{i}]')
    elif isinstance(o, str):
        yield path, o


if '--show' in sys.argv:
    course, pat = sys.argv[sys.argv.index('--show') + 1:][:2]
    for f in sorted(files):
        if f'/courses/{course}/' in f or '/exams/' in f:
            for path, s in strings(json.load(open(f))):
                if re.search(pat, s):
                    print(f'{f.replace("app/content/", "")} {path[:50]}: {s[:300]}')
    sys.exit(0)
texts = {}
for f in files:
    try:
        texts[f] = json.dumps(json.load(open(f)), ensure_ascii=False).replace('\\\\', '\\')
    except Exception:
        pass
for course, keys in KEYS.items():
    print(f'== {course}')
    for kx in keys:
        hits = {}
        for f, tx in texts.items():
            c = len(re.findall(kx, tx))
            if c and (f'/courses/{course}/' in f or '/exams/' in f):
                hits[f.replace('app/content/', '').replace('courses/', '').replace('.json', '')] = c
        print(f'  {kx}: ' + (', '.join(f'{a}:{b_}' for a, b_ in sorted(hits.items())[:12]) or 'none'))
