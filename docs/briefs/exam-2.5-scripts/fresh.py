"""Freshness grep for topic-2.5: each item's distinctive parameters and keys against every course, exam, bank and
drill file (except topic-2.5.json itself). Prints the hits per token; the report records the reading of each.
Tokens are matched on the raw JSON text, so LaTeX is written with doubled backslashes.
A second pass compares every numeric key of the exam, and every wrong value, with every keyed numeric answer in
the convex and numerics course folders (lessons, reviews, homework). A key that equals a course key is a clash
and the script exits 1; a wrong value that equals one is listed. Small round values (multiples of 0.25 up to 10 in
size) are structure and skipped.
Run: python3 docs/briefs/exam-2.5-scripts/fresh.py
"""
import glob
import json
import math
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'e-lp-corner': ['x + 2y \\\\le 8', '3x + 2y \\\\le 12'],
    'e-duality-sandwich': ['earning 8.4', 'cost is 9.6'],
    'e-step-limit': ['6.45&6.05', '0.4 and 12.5'],
    'e-double-gap': ['3{,}000{,}000', '2^{-31}', '4.656612873077393e-10'],
    'e-bisection-count': ['[1, 3]$ and halves', '2 \\\\times 10^6'],
    'e-mc-error': ['£12.30', '0.0615'],
    'e-convex-sets': ['xy \\\\ge 1,\\\\ x > 0', '\\\\max(|x|, |y|) \\\\le 1', '|x| \\\\ge 1'],
    'e-hessian-threshold': ['3xy + ky^2', '4k - 9'],
    'e-linprog-bounds': ['bounds=(None, None)', 'linprog(-c, A_ub=A, b_ub=b)'],
    'e-dual-function': ['(x + 1)^2 + \\\\lambda(2 - x)', '3\\\\lambda - \\\\tfrac{\\\\lambda^2}{4}'],
    'e-slsqp-sign': ['0.02 - w @ S @ w'],
    'e-rate-from-kappa': ['0.5 and 12', '{23}{25}', '165.7'],
    'e-newton-minimise': ['e^x - 3x', '\\\\tfrac3e', '1.1036'],
    'e-cancel-rewrite': ['\\\\sqrt{x^2 + 1} - x', '10^{16} + 1'],
    'e-log-condition': ['50.50', '\\\\ln 1.02'],
    'e-log1p-blame': ['3.0000446571375978', 'log(1 + 3e-12)'],
    'e-three-point-poly': ['(0, 1)$, $(1, 3)$ and $(4, 2)$', '{23}{6}'],
    'e-richardson-three': ['27B - A', '27B-A', '{26}'],
    'e-gauss-two-point': ['int_{-1}^{5} x^4', '625.2', '582'],
    'e-explicit-step': ['900.02', '0.001111', '2{,}499.98', 'S_{\\\\max} = 300'],
    'e-control-variate': ['17.85', '1.9833', '0.7225'],
    'e-projection-kkt': ['(x - 4)^2 + (y - 1)^2', 'x + 2y \\\\le 3', '(3.4, -0.2)', '1.682'],
    'e-long-only-kkt': ['0.01, 0.04 and 0.09', '0.01, 0.06 and 0.10', '(0, 0.5, 0.5)'],
    'e-local-global-proof': ['max(f(\\\\mathbf x), g(\\\\mathbf x))', 'min(x^2, (x - 2)^2)', 'worse of two'],
    'e-normal-equations': ['94{,}900', '9.0 \\\\times 10^9', '94906'],
    'e-natural-spline': ['(0, 0)$, $(1, 2)$, $(2, 1)$ and $(3, 3)$', '-x^3 + 3x', '1.375'],
    'e-log-sum-exp': ['log_sum_exp', '1.8 \\\\times 10^{308}'],
    'e-solver-certificate': ['x^2 + 3y^2', '(3.02, 0.98)', '11.9967', '12.0016'],
    'e-error-budget': ['7.9620', '7.9680', '56{,}250{,}000'],
    'e-stiff-implicit': ['-200e', 'h = 0.04', '-0.6', '28 steps'],
}
files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('topic-2.5.json', 'manifest.json')]
text = {f: open(f, encoding='utf8').read() for f in files}
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if t in s and pat.search(s)]
        print(f'{iid:24s} {t!r:34s} {len(hits):3d} ' + ', '.join(hits[:5]))


# ---- keys against keyed answers in the two courses
def _num(x):
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str) and re.fullmatch(r'-?\d+(\.\d+)?', x.strip()):
        return float(x)
    return None


def nums(node):
    """Yield (kind, value) for every numeric `answer` and every `wrong[].value` under node."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == 'answer' and _num(v) is not None:
                yield 'answer', _num(v)
            elif k == 'wrong' and isinstance(v, list):
                for w in v:
                    if isinstance(w, dict) and _num(w.get('value')) is not None:
                        yield 'wrong:' + str(w.get('id')), _num(w['value'])
            if isinstance(v, (dict, list)):
                yield from nums(v)
    elif isinstance(node, list):
        for v in node:
            yield from nums(v)


def trivial(v):
    return abs(v) <= 10 and abs(v * 4 - round(v * 4)) < 1e-9


course_keys = []
for course in ('convex', 'numerics'):
    for f in glob.glob(os.path.join(ROOT, 'courses', course, '*.json')):
        if os.path.basename(f) == 'course.json':
            continue
        with open(f, encoding='utf8') as fh:
            for kind, v in nums(json.load(fh)):
                if kind == 'answer':
                    course_keys.append((v, os.path.relpath(f, ROOT)))
with open(os.path.join(ROOT, 'exams', 'topic-2.5.json'), encoding='utf8') as fh:
    exam = json.load(fh)
clash = 0
for it in exam['items']:
    for kind, v in nums(it):
        if trivial(v):
            continue
        hits = sorted({f for cv, f in course_keys if math.isclose(cv, v, rel_tol=1e-6, abs_tol=1e-12)})
        if hits:
            is_key = kind == 'answer'
            clash += is_key
            print(f'{"KEY CLASH" if is_key else "wrong value matches a course key"}: {it["id"]} {kind} = {v!r} in {", ".join(hits[:4])}')
print(f'key clashes with convex and numerics answers: {clash}')
sys.exit(1 if clash else 0)
