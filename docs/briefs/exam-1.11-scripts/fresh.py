"""Freshness grep for topic-1.11: each item's distinctive parameters and keys against every course, exam, bank and
drill file (except topic-1.11.json itself). Prints the hits per token; the report records the reading of each.
Tokens are matched on the raw JSON text, so LaTeX is written with doubled backslashes.
Run: python3 docs/briefs/exam-1.11-scripts/fresh.py
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'e-divide-conjugate': ['4 + 7i', '{29+26i}', '-13 + 26i'],
    'e-arg-quadrant': ['-2\\\\sqrt3 - 2i', '(-2\\\\sqrt3, -2)'],
    'e-wire-mass': ['(1, 0)$ to $(4, 4)', '2 + 10t'],
    'e-rate-pull': ['0.25(0.045 - r)', '0.054197', '0.025e^{-0.25t}'],
    'e-char-roots': ["2y' - 15y", '\\\\sqrt{14}\\\\,t'],
    'e-laplace-shift': ['e^{-2t}\\\\sin 3t', '(s+2)^2+9'],
    'e-fifth-roots': ['w^5', '2e^{7\\\\pi i/5}'],
    'e-harmonic-partner': ['e^x\\\\cos y + 2xy', 'e^z - iz^2'],
    'e-log-square': ['-1 + \\\\sqrt3\\\\,i', '-2 - 2\\\\sqrt3'],
    'e-conjugate-circle': ['|z| = 2.5', '12.5\\\\pi'],
    'e-cauchy-plus-normal': ['e^{-1.12}', '0.3263', '\\\\varphi_{X+Y}(0.8)'],
    'e-potential-work': ['2xy + y^3', 'x^2y + xy^3 + y^2'],
    'e-circulation-flux': ['2x - 5y', '72\\\\pi', '27\\\\pi'],
    'e-tilted-patch': ['3u - v', '(-3, 1, 1)', '6.633'],
    'e-cube-outflow': ['xz^2', 'zy^2'],
    'e-integrating-factor': ['9e^{-t}', '3e^{-t} + 2e^{-4t}', '1.1403'],
    'e-resonant-guess': ['12e^{2t}', "2y' - 8y"],
    'e-damping-rate': ['16y', '(r + 2)(r + 8)'],
    'e-saddle-solution': ['1&4\\\\\\\\1&1', '(6, 1)', '19.14'],
    'e-spiral-turn': ['-1&-4\\\\\\\\2&-3', '-2 \\\\pm i\\\\sqrt7'],
    'e-euler-by-hand': ['y - t^2', '1.546875'],
    'e-upper-pole': ['x^2 + 6x + 13', '-3 + 2i', '-3 \\\\pm 2i'],
    'e-third-power-pole': ['(z - 1)^3'],
    'e-damped-call': ['e^{\\\\alpha k}C(k)'],
    'e-hemisphere-curl': ['z - y,\\\\ x + z', 'xy)'],
    'e-crowded-prey': ['4 - x - 2y', 'y(x - 2)', '-2&-4\\\\\\\\1&0'],
    'e-laplace-rebound': ["6y' + 5y", 's + 9}{(s + 1)(s + 5)', '2e^{-t} - e^{-5t}', '0.7290'],
    'e-semicircle-proof': ['\\\\deg q \\\\ge \\\\deg p + 2', 'pi M}{R}'],
    'e-vortex-square': ['(\\\\pm 2, \\\\pm 2)', '(y^2,\\\\ 3x)', '(4, 1)'],
    'e-stiff-steps': ['-80(y - \\\\cos t)', '0.0348', '80h'],
}
files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('topic-1.11.json', 'manifest.json')]
text = {f: open(f, encoding='utf8').read() for f in files}
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if t in s and pat.search(s)]
        print(f'{iid:24s} {t!r:34s} {len(hits):3d} ' + ', '.join(hits[:5]))
