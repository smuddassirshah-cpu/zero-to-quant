"""Freshness of the re-authored items: search every content file (courses, exams, Fluency sets) for the new
numbers, formulae and story words. Formulae are matched with spaces removed. The item's own set is left out.

Run from the repo root: python docs/reviews/delta-problems-aa-2-scripts/fresh.py [--all]
Default: hits in the item's own course, its topic's sibling courses and the exams. --all: every course.
"""
import glob
import json
import re
import sys

ALL = '--all' in sys.argv
TOPIC = {
    'multivar': ['limits', 'integrals', 'taylor', 'multivar', 'vector-calc'],
    'functions': ['equations', 'functions', 'quadratics', 'arithmetic', 'algebra', 'ratio'],
    'quadratics': ['equations', 'functions', 'quadratics'],
    'counting': ['counting', 'exp-log', 'series', 'trig', 'counting-chance'],
}
# (own course, own file, label, needles); a needle starting with "w:" is a whole word, case-insensitive
NEEDLES = [
    ('multivar', 'multivar/problems-4.json', 'p-drone-landing', ['/32}', '32\\pi', '\\sqrt{32', 'w:drone', '10.0265', '8.58', '0.3935', '\\sigma=4', '4\\sqrt{2\\pi}', '32\\ln10']),
    ('multivar', 'multivar/problems-4.json', 'p-corner-sprinkler 1', ['9-r^2', '9-r^{2}', '9r-r^3', '9-(x^2+y^2)', '9-x^2-y^2', 'w:sprinkler']),
    ('functions', 'functions/problems-2.json', 'p-path-and-pipe', ['4x+9', '0.25x+26', '\\frac{x}{4}+26', '(-2,1)', '(5,29)', '(12,23)', '(4,25)', '4.25x', 'w:drain']),
    ('functions', 'functions/problems-3.json', 'p-sledge-cyclist 1-2', ['0.5t^2', '\\tfrac{1}{2}t^2', '\\frac{1}{2}t^2', '12.5\\div5', 'w:sledge', '(5,12.5)']),
    ('functions', 'functions/problems-3.json', 'p-track-cubic', ['x^3-12x^2+36x', 'x(x-6)^2', '(x-6)^2', '(2,32)', 'h(2)=32', '3(x-2)(x-6)']),
    ('counting', 'counting/problems-1.json', 'p-ice-cream-van', ['w:14 flavours', '\\binom{14}{3}', '14\\times13\\times12', 'P(14,3)', '14^3', 'w:364', 'w:2184', 'w:2548', 'w:12740', 'w:netball', 'w:flavours', 'w:scoops']),
    ('quadratics', 'quadratics/problems-1.json', 'p-cinema-block', ['x^2+15x+44', 'x^2+15x+36', '(x+3)(x+12)', '(x+4)(x+11)', '(x+12)', '(x+11)', 'w:286', 'w:294', 'w:cinema']),
    ('quadratics', 'quadratics/problems-1.json', 'p-allotment-plots', ['x^2+11x+30', '(x+5)(x+6)', '2x^2+19x+45', '(2x+9)', '3(x+5)^2', '(x+5)^2', 'w:allotment']),
    ('quadratics', 'quadratics/problems-2.json', 'p-bus-chase 3', ['t^2-6t+6', 'x^2-6x+6', '(t-3)^2-3', '(x-3)^2-3', '3\\pm\\sqrt{3}', '3-\\sqrt{3}', '\\sqrt{12}', '1.268', '4.732']),
    ('quadratics', 'quadratics/problems-2.json', 'p-cliff-stone story', ['w:flare', 'w:deck', 'w:ship', '15+10t-5t^2', '-5(t-1)^2+20']),
]


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


files = sorted(glob.glob('app/content/**/*.json', recursive=True))
files = [f for f in files if not f.endswith('manifest.json')]
cache = {}
for f in files:
    try:
        cache[f] = list(strings(json.load(open(f))))
    except Exception as e:  # not JSON content
        print('skip', f, e)

total = 0
for course, own, label, needles in NEEDLES:
    scope = TOPIC[course]
    print(f'\n== {label} ({own})')
    for nd in needles:
        hits = []
        for f, strs in cache.items():
            if f.endswith(own):
                continue
            rel = f.split('app/content/')[1]
            top = rel.split('/')
            in_scope = top[0] != 'courses' or top[1] in scope
            if not (ALL or in_scope):
                continue
            for s in strs:
                if nd.startswith('w:'):
                    m = re.search(r'(?<![\w.])' + re.escape(nd[2:]) + r'(?![\w])', s, re.I)
                    found = bool(m)
                    pos = m.start() if m else 0
                else:
                    z = s.replace(' ', '')
                    pos = z.find(nd)
                    found = pos >= 0
                    s = z
                if found:
                    hits.append((rel, s[max(0, pos - 60):pos + 70].replace('\n', ' ')))
        total += len(hits)
        if hits:
            print(f'  "{nd}": {len(hits)} hit(s)')
            for rel, snip in hits[:6]:
                print(f'      {rel}: ...{snip}...')
            if len(hits) > 6:
                print(f'      and {len(hits) - 6} more: ' + ', '.join(sorted({h[0] for h in hits[6:]}))[:300])
print(f'\nfresh.py: {total} hits over {len(cache)} files; each is judged in the review')
