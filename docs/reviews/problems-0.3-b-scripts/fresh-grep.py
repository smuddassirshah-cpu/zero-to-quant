"""Reader's own freshness pass: each problem's setting (nouns) and formulae (numbers), searched across the exp-log course
(lessons, Fluency, reviews, homework), the other Stage 0 courses and the exams. The three files under read are skipped.
Prints pattern, number of files hit and each hit in context (up to four per pattern).

Usage (repo root): python3 docs/reviews/problems-0.3-b-scripts/fresh-grep.py [--wide]   (--wide searches every course)
"""
import glob
import re
import sys

PAT = {
    'yeast': r'yeast|culture', 'cells hourly': r'cells?\b.{0,60}(every|each) hour|(doubles|triples) every hour',
    '3000 x 2^n': r'3,?000 \\times 2\^', '2^{1/2} halfway': r'2\^\{1/2\}|2\^\{0\.5\}',
    'laptop': r'laptop', 'loses 25%': r'loses 25%|falls? 25%', '0.75^': r'0\.75\^', '1,200': r'£1,200\b',
    'coin': r'\bcoin', '640': r'£640\b|\b640\b', '1.5625': r'1\.5625', '1.25^': r'1\.25\^', '18 months': r'18 months',
    '(3, 64)': r'\(3, ?64\)', '4^x': r'y = 4\^x|4\^\{?x', '(1/4)^x': r'0\.25\^x|tfrac\{1\}\{4\}\\right\)\^x', '2,048': r'2,?048',
    'fault search': r'faulty|binary search|rules out half', '65,536': r'65,?\{?,?\}?536', '327': r'327,?\{?,?\}?680',
    '2^40': r'2\^\{40\}', 'log 2 0.30103': r'0\.30103', 'doubled 40': r'doubled 40|40 doublings', '10^15': r'10\^\{15\}',
    'drawdown': r'drawdown|recover', 'falls 20% twice': r'falls 20%', '32,000': r'32,?\{?,?\}?000', '56.25': r'56\.25',
    '1.08^n': r'1\.08\^', '1.25^2': r'1\.25\^2', 'app users': r'\bapp\b|users', '1.3^n': r'1\.3\^', '50,000': r'50,?\{?,?\}?000 users',
    'first move': r'first move',
    'Mia': r'\bMia\b', '2,400': r'£2,400\b|2400e', '5.5%': r'5\.5%|0\.055', '19,200': r'19,?\{?,?\}?200', 'halfway in time': r'halfway (there )?in time',
    'weekly target': r'Monday.{0,80}Friday', '£40.00 close': r'closes at £40', '0.043': r'0\.043\b', '41.76': r'41\.76',
    '£45.00': r'£45\.00', 'three equal': r'three equal',
    '£15 to £135': r'£15\b.{0,80}£135|£135', 'ln 9': r'\\ln 9', 'log chart line 2026': r'2026', '12 cm': r'\bcm\b',
    'geometric mid': r'sqrt\{15|halfway up',
    'Leo': r'\bLeo\b', '4.8% monthly': r'4\.8%|0\.048', '1.004': r'1\.004', '£6,000': r'£6,000', 'compounded monthly': r'compounded monthly',
    'straight line rate': r'straight.{0,120}continuous (yearly )?(growth )?rate',
}
wide = '--wide' in sys.argv
files = sorted(glob.glob('app/content/courses/exp-log/*.json')) + sorted(glob.glob('app/content/exams/*.json'))
for c in ('counting', 'series', 'trig', 'equations', 'functions', 'quadratics', 'number-sense', 'ratio'):
    files += sorted(glob.glob(f'app/content/courses/{c}/*.json'))
if wide:
    files = sorted(set(glob.glob('app/content/courses/*/*.json') + glob.glob('app/content/exams/*.json')))
files = [f for f in files if not re.search(r'exp-log/problems-[123]\.json$', f)]
text = {f: open(f).read() for f in files}
for name, pat in PAT.items():
    hits = []
    for f, t in text.items():
        for m in re.finditer(pat, t):
            hits.append((f.replace('app/content/', ''), t[max(0, m.start() - 70):m.end() + 70].replace('\n', ' ')))
    nf = len({h[0] for h in hits})
    print(f'## {name}: {len(hits)} hit(s) in {nf} file(s)')
    seen = set()
    for f, ctx in hits:
        if f in seen or len(seen) >= 4:
            continue
        seen.add(f)
        print(f'   {f}: ...{ctx}...')
