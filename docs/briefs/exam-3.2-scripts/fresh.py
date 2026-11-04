"""Freshness greps for topic-3.2: every item's keys, parameters and wrong values, with number boundaries,
over app/content (courses, exams, bank, drills, data), excluding topic-3.2.json itself. Prints each hit with context.
Run: python3 fresh.py   (a hit in a question, answer or explanation is a clash; one inside a long decimal series is not)
"""
import glob, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
FILES = [f for f in glob.glob(ROOT + '/app/content/**/*.json', recursive=True)
         if not f.endswith('exams/topic-3.2.json') and not f.endswith('manifest.json')]
TEXT = {f: open(f, encoding='utf-8').read() for f in FILES}
num = lambda s: r'(?<![0-9.])' + re.escape(s) + r'(?![0-9])'

# item id -> list of patterns (regex)
PATS = {
    'e-var-two-times': [r'2W_3 - W_7', r'2W_3-W_7', r'W_7'],
    'e-qv-drift': [r'3W_t\s*-\s*2t', r'3W_t-2t'],
    'e-gbm-below': [r'S_0 = 80', r'S_0=80', num('0.3500'), num('0.2751'), num('0.2928'), r'S_2 < 70'],
    'e-drift-tw2': [r'tW_t\^2', r't W_t\^2', r'tx\^2'],
    'e-pick-martingales': [r'4\.5t', r'W_t\^4 - 6tW_t\^2', r'tW_t - \\\\int', r'3tW_t'],
    'e-theta-from-pde': [num('10.8791'), num('0.70216'), num('0.019056'), num('5.73'), num('0.0191'), r'K = 65'],
    'e-moment-and-isometry': [r'W_2W_5\^3', r'W_2 W_5\^3', r'e\^\{2\.5\}', num('11.1825'), num('12.1825'), r'2\.5\} e\^\{W_t - t/2\}'],
    'e-daily-touch': [num('0.5826'), num('0.6956'), num('0.69557'), num('0.06917'), r'126 days', r'1/252'],
    'e-exit-drift': [num('0.4132'), num('0.41317'), num('2.5350'), num('2.535'), r'-0\.3t', r'0\.9W_t', num('0.7407')],
    'e-sixth-repair': [r'W_t\^6', r'15tw\^4', r'-15t\^3', r't\^3'],
    'e-cubed-claim': [num('23.5574'), num('25.0141'), num('5.5814'), num('-0.375'), r'S_T\^3', r'S_0 = 2'],
    'e-atoms-three-sets': [r'\\\\\{3, 4, 5, 6\\\\\}', r'\\\\\{6, 7\\\\\}', r'\\\\Omega = \\\\\{1, 2, \\\\ldots, 9'],
    'e-tail-integral': [r'\(2/t\)\^3', r'8t\^\{-3\}', r'P\(X > t\) = \(2'],
    'e-die-reweight': [r'0\.35, 0\.25, 0\.15', num('8.6'), r'2\.1, 1\.5, 0\.9', num('15.17')],
    'e-sigma-families': [r'\\\\\{a,b\\\\\}, \\\\\{c,d\\\\\}, \\\\\{a,c\\\\\}', r'\\\\\{a\\\\\}, \\\\\{b,c,d\\\\\}'],
    'e-var-of-condexp': [num('2.0833'), r'25\}\{12\}', r'\\\\tfrac\{25\}\{12', r'\\\\\{5\\\\\}, \\\\\{6\\\\\}'],
    'e-adapted-predictable': [r'xi_\{n\+1\}', r'S_n > 0', r'\\\\max\(S_0'],
    'e-ruin-by-martingale': [num('0.1896'), r'1\.5\^\{S_n\}', r'1\.5\^3', r'1\.5\^\{-2\}'],
    'e-is-weight': [num('0.0076'), r'4\.875', r'N\(2\.5, 1\)', r'x = 3\.2'],
    'e-swap-limits': [r'1/n\^2', r'\\\\min\(n, 1/U\)', r'nU\^n'],
    'e-tree-price': [num('0.475'), num('8.770'), num('8.7696'), r'62\.4', num('33.75'), num('3.75'), r'u = 1\.25', r'd = 0\.85', r'S_0 = 60'],
    'e-variance-split': [r'Var\}\(X\) = E\[\\\\mathrm\{Var\}\(X \\\\mid', r'X - \\\\mu = \(X - Y\)', r'orthogonal, not independent'],
    'e-kernel-peak': [num('0.2660'), num('0.26596'), r'D = 0\.45', num('0.45')],
    'e-slab-heat': [num('0.8787'), r'D = 0\.4,', r'\[-1\.2, 1\.2\]'],
    'e-coefficient-k': [r'x\(\\\\pi - x\)', r'x\(pi - x\)', r'4\(1 - \(-1\)\^k\)'],
    'e-jump-gibbs': [num('7.537'), num('7.5369'), r'8\.949', r'0\.08949'],
    'e-rod-centre': [num('2.938'), num('2.9382'), r'4\\\\sin\(\\\\pi x/3\)', r'0\.3\\\\,u_\{xx\}'],
    'e-heat-change': [num('1.92'), num('2.1316'), num('0.46'), num('-0.46')],
    'e-fk-square': [num('9.7265'), num('11.88'), num('2.88'), r'0\.5\\\\,dt \+ 1\.2'],
    'e-explicit-code': [r'explicit_heat', r'def explicit', r'dt_max'],
}
total = 0
for item, pats in PATS.items():
    for p in pats:
        rx = re.compile(p)
        hits = []
        for f, t in TEXT.items():
            for m in rx.finditer(t):
                a = max(0, m.start() - 55); b = min(len(t), m.end() + 55)
                hits.append((os.path.relpath(f, ROOT + '/app/content'), t[a:b].replace('\n', ' ')))
        if hits:
            total += len(hits)
            print('== %s  %s  (%d hits)' % (item, p, len(hits)))
            for f, c in hits[:6]:
                print('   ', f, '|', c)
print('total hits', total)
