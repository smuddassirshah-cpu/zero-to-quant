"""Stale text in the re-authored items: every string of an item (prose, questions, options, every feedback
line, explanations, accept lines) searched for numbers and words of the version before the fix pass.

Run from the repo root: python docs/reviews/delta-problems-aa-2-scripts/stale.py
Each hit prints; the reader judges it (a hit can be a true use of the same number).
"""
import json
import re

ITEMS = [
    ('multivar', 4, 'p-drone-landing', [r'/8\b', r'(?<!3)8\\pi', r'\b2 m\b', r'2\\sqrt2', r'\\sigma = 2', r'5\.0133', r'4\.29', r'root8']),
    ('multivar', 4, 'p-corner-sprinkler', [r'\\sqrt\{9', r'3 - x', r'9 - x\^2(?! )', r'straight', r'no-root(?!.*a\^2)']),
    ('functions', 2, 'p-path-and-pipe', [r'0\.5x', r'-2x', r'2x \+', r'\+ 7\b', r'\+ 2\b', r'\b3\.6\b', r'\(2, 3\)', r'gradient 0\.5', r'gradient \$?-2']),
    ('functions', 3, 'p-sledge-cyclist', [r'4 seconds', r'\b8 m', r'= 8\b', r'\b16\b', r'8 \\div', r'\b32\b']),
    ('functions', 3, 'p-track-cubic', [r'x - 3', r'3x\^2', r'h\(2\) = 2\b', r'h\(1\)', r'= 4\b(?! \\times)', r'x = 1\b', r'x = 3\b', r'\b0, 3\b', r'1 < x', r'\\le 4']),
    ('functions', 3, 'p-bakery-trays', [r'[Pp]art 5', r'part 4 (found|gave)']),
    ('counting', 1, 'p-ice-cream-van', [r'\b11\b', r'\b165\b', r'\b990\b', r'\b1155\b', r'\b5775\b', r'\b1331\b', r'\b33\b', r'\b495\b', r'\b171\b', r'\border(s)? (can|are)', r'different orders']),
    ('counting', 1, 'p-team-photo', [r'photo', r'camera', r'picture']),
    ('quadratics', 1, 'p-cinema-block', [r'11x \+ 24', r'\b24\b', r'x \+ 8', r'x \+ 2\)', r'x \+ 9\)(?!.*13)', r'\b18\b(?! and)', r'\b228\b', r'\b234\b', r'\b208\b', r'\b308\b', r'2k = 11', r'four', r'three']),
    ('quadratics', 1, 'p-allotment-plots', [r'x \+ 4', r'9x \+ 20', r'2x \+ 7', r'15x', r'\b28\b', r'x = 6', r'sum-twelve', r'sum-21', r'\b12\b', r'\b21\b']),
    ('quadratics', 2, 'p-bus-chase', [r'6t \+ 7', r'\\sqrt\{2\}', r'\\sqrt\{8\}', r'1\.59', r'1\.586', r'4\.41', r'7 m']),
    ('quadratics', 2, 'p-cliff-stone', [r'stone', r'cliff', r'throw', r'beach', r'ground']),
    ('equations', 4, 'p-remote-cars', [r'81 m(?! from| \(|,|\.| and)']),
]


def strings(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, path + '/' + str(i))


hits = 0
for course, n, item, pats in ITEMS:
    d = json.load(open(f'app/content/courses/{course}/problems-{n}.json'))
    it = next(i for i in d['items'] if i['id'] == item)
    for path, s in strings(it):
        if path in ('/id',) or path.endswith('/id'):
            continue
        for pat in pats:
            m = re.search(pat, s)
            if m:
                hits += 1
                print(f'{course} {n} {item} {path}: /{pat}/ :: ...{s[max(0, m.start() - 50):m.end() + 60]}...')
print(f'stale.py: {hits} hits to judge')
