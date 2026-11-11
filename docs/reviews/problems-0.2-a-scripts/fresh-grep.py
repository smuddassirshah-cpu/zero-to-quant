"""Reader's own freshness pass: each problem's setting (nouns) and formulae (numbers), searched across its own course
(lessons, fluency, reviews, homework, the other problem sets) and the exams. Prints file, count and the first hit in context.

Usage (repo root): python3 docs/reviews/problems-0.2-a-scripts/fresh-grep.py [--wide]   (--wide also searches every other course)
"""
import glob
import json
import re
import sys

PAT = {
    'equations': {
        'p-family-tickets': [r'theatre', r'child ticket', r'adult ticket', r'5a ?- ?15', r'5\(a ?- ?3\)'],
        'p-food-van': [r'burger', r'food van', r'pitch', r'4\.2n', r'6\.50'],
        'p-number-trick': [r'number trick', r'[Tt]hink of a number', r'2n ?\+ ?26', r'5\(n ?\+ ?4\)'],
        'p-market-pitch': [r'corner', r's\(s ?\+ ?2\)', r'7s\^2'],
        'p-climbing-wall': [r'climb', r'45 ?\+ ?8c', r'whole pence', r'£213'],
        'p-cottage-share': [r'cottage', r'split the cost', r'x ?\+ ?30', r'extra bed', r'each share'],
        'p-power-tariffs': [r'[Tt]ariff', r'unit of electricity', r'daily charge', r'45 ?\+ ?24u'],
        'p-interest-split': [r'bond fund', r'12,000', r'6\.5%', r'0\.065', r'savings account'],
        'p-bakery-stock': [r'loaves', r'[Bb]akery', r'240 ?- ?18h'],
        'p-fridge-temperature': [r'Fahrenheit', r'1\.8C', r'fridge', r'freezer', r'F ?- ?32'],
        'p-van-value': [r'P ?- ?kt', r'loses £', r'value lost', r'24000 ?- ?2400', r'leasing'],
        'p-fund-weight': [r'a ?\+ ?b\}', r'appears twice', r'1 ?- ?w', r'blocks of'],
    },
    'functions': {
        'p-exchange-kiosk': [r'kiosk', r'euro', r'€', r'1\.15'],
        'p-van-fuel': [r'litres', r'fuel', r'0\.15d', r'tank'],
        'p-stone-throw': [r'stone', r'cliff', r'45 ?- ?5\(t', r'\(t ?- ?2\)\^2'],
        'p-sapling-log': [r'sapling', r'gardener', r'5w ?\+ ?12', r'struck out'],
        'p-candle-burn': [r'candle', r'burn', r'26 ?- ?2\.5t'],
        'p-path-and-pipe': [r'pipe', r'drain', r'park plan', r'0\.5x ?\+ ?2', r'-2x ?\+ ?7'],
        'p-two-gyms': [r'[Gg]ym', r'joining fee', r'24x ?\+ ?20', r'18x ?\+ ?50'],
        'p-two-savers': [r'savings jar', r'\bjar\b', r'15x ?\+ ?40', r'15x ?\+ ?20', r'catch up'],
        'p-bakery-trays': [r'[Bb]akery', r'trays', r'-5x\^2 ?\+ ?60x', r'break even'],
        'p-sledge-cyclist': [r'sledge', r'cyclist', r'0\.5t\^2', r'3t\b'],
        'p-two-cultures': [r'culture', r'cells', r'200 \\times 2\^', r'1000 ?\+ ?300t', r'doubles each'],
        'p-track-cubic': [r'x\^3 ?- ?6x\^2 ?\+ ?9x', r'train track', r'x\(x ?- ?3\)\^2', r'toy train'],
    },
}


def texts(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)


wide = '--wide' in sys.argv
for course, items in PAT.items():
    files = sorted(glob.glob(f'app/content/courses/{course}/*.json')) + sorted(glob.glob('app/content/exams/*.json'))
    if wide:
        files += sorted(f for f in glob.glob('app/content/courses/*/*.json') if f'/{course}/' not in f)
    blobs = {f: ' \n '.join(texts(json.load(open(f)))) for f in files}
    for item, pats in items.items():
        print(f'== {course} {item}')
        for p in pats:
            rx = re.compile(p)
            for f, b in blobs.items():
                hits = list(rx.finditer(b))
                if not hits:
                    continue
                own = [h for h in hits if item in f]
                m = hits[0]
                ctx = b[max(0, m.start() - 70):m.end() + 70].replace('\n', ' ')
                tag = f.replace('app/content/', '')
                print(f'   /{p}/ {tag} x{len(hits)}: ...{ctx}...')
