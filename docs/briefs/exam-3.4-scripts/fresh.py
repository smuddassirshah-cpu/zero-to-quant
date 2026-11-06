"""Freshness grep for topic-3.4: each item's distinctive parameters and keys against every course, exam, bank and
drill file (except topic-3.4.json itself). Prints the hits per token; the report records the reading of each.
Tokens are matched on the raw JSON text, so LaTeX is written with doubled backslashes (raw strings below).
It also prints any token missing from topic-3.4.json itself, so a stale token cannot pass silently.
Run: python3 docs/briefs/exam-3.4-scripts/fresh.py
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'e-order-fifteen': [r'\\mathbb{Z}_{36}', r'\\langle 15 \\rangle'],
    'e-cycles-bottom-row': ['3, 5, 1, 2, 6, 4', r'(2\\,5\\,6\\,4)'],
    'e-zero-divisors-z14': [r'\\mathbb{Z}_{14}', 'modulo 14'],
    'e-jump-metric': ['|x - y| + 1', 'd(x, x) = 0$, and'],
    'e-preimage-quadratic': ['x^2 - 4x', 'V = (-3, 5)', r'(-1, 1) \\cup (3, 5)'],
    'e-four-point-topology': [r'\\{1, 2, 3, 4\\}', r'\\{1, 2, 3\\}, X'],
    'e-inverse-mod-60': ['17^{-1}', 'bmod 60', '901'],
    'e-units-mod-17': [r'\\mathbb{Z}_{17}', 'varphi(16)'],
    'e-even-or-odd': [r'(1\\,2)(3\\,4\\,5\\,6)', r'(1\\,4)(2\\,5\\,3)'],
    'e-product-table': [r'(1\\,3\\,5)(2\\,4)', r'(1\\,5)(2\\,3\\,4)', r'(2\\,5\\,3)'],
    'e-hom-z18-z12': [r'\\mathbb{Z}_{18} \\to \\mathbb{Z}_{12}', r'2x \\bmod 12'],
    'e-normal-in-s4': [r'\\langle (1\\,2\\,3\\,4) \\rangle', r'(1\\,3)(2\\,4), (1\\,4)(2\\,3)'],
    'e-euler-mod-14': ['5^{100}', 'varphi(14)', 'bmod 14'],
    'e-remainder-z7': ['x^5 + 3x^2 + 2', '1074'],
    'e-irreducible-z3': ['x^2 + x + 2', 'x^3 + 2x^2 + 1', 'x^4 + x^3 + x + 2', 'x^3 + x + 2'],
    'e-half-disc': [r'y \\ge 0\\}', r'[-1, 1] \\times \\{0\\}'],
    'e-two-function-metrics': ['g(x) = x^3', '0.3849', '8}{105}'],
    'e-homeomorphic-pairs': [r'$(0, 1)$ and $(0, \\infty)$', '(3, 7)', r'(0, 1) \\cup (2, 3)'],
    'e-connected-subsets': [r'(-1, 0] \\cup (0, 3)', 'x^2 > 4', '[0, 5]'],
    'e-compact-subsets': [r'(t, \\sin t)', '(x, 2x)', r'(\\tfrac1n, 0)'],
    'e-log-metric': [r'ln x - \\ln y', r'|\\ln x'],
    'e-which-fields': [r'\\mathbb{Z}_{103}', r'\\mathbb{Z}_{87}', 'sqrt3 :'],
    'e-max-on-circle': ['x + 2y', '2.2361', '2,236'],
    'e-cyclic-subgroups-proof': ['g^r = g^k', 'least positive integer with $g^m'],
    'e-equaliser-closed': [r'f(x) = g(x)\\}', r'f^{-1}(U) \\cap g^{-1}(V)'],
    'e-image-sizes': ['|G| = 28', '|H| = 21', r'\\mathbb{Z}_{28}'],
    'e-order-three-s6': ['order 3', r'(1\\,2\\,3)(4\\,5\\,6)'],
    'e-squares-mod-11': [r'\\mathbb{Z}_{11}^{\\times}', 'x^5 = 1', '243'],
    'e-plane-contraction': [r'tfrac13 \\sin y', r'tfrac14 \\cos x', '1.9678', '0.0967', '0.1561'],
    'e-power-contraction-proof': ['e^{-x}$ on', 'T^k', 'e^{-e^{-x}}', '0.5671'],
}
files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('topic-3.4.json', 'manifest.json')]
text = {f: open(f, encoding='utf8').read() for f in files}
with open(os.path.join(ROOT, 'exams', 'topic-3.4.json'), encoding='utf8') as fh:
    own = fh.read()
print('tokens missing from topic-3.4.json:', [t for toks in TOKENS.values() for t in toks if t not in own])
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if t in s and pat.search(s)]
        print(f'{iid:26s} {t!r:42s} {len(hits):3d} ' + ', '.join(hits[:5]))
