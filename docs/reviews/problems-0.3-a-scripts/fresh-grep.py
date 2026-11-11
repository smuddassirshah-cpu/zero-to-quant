"""Reader's own freshness pass: each problem's setting (nouns) and formulae (numbers), searched across its own course
(lessons, fluency, reviews, homework, the other problem sets), the later course counting-chance for the counting sets,
and the exams. Prints file, count and the first hit in context. Hits inside the problem's own file are skipped.

Usage (repo root): python3 docs/reviews/problems-0.3-a-scripts/fresh-grep.py [--wide]   (--wide also searches every other course)
"""
import glob
import json
import re
import sys

PAT = {
    'counting': {
        1: {
            'p-tulip-bed': [r'tulip', r'gardener', r'varieties', r'binom\{8\}\{4\}', r'P\(8, ?4\)', r'\b1680\b', r'\b6720\b'],
            'p-team-photo': [r'netball', r'photo', r'twins', r'captain', r'middle (place|seat)', r'\b192\b'],
            'p-five-a-side': [r'\bleague', r'home and away', r'at home', r'n\(n ?- ?1\)', r'binom\{9\}\{6\}', r'\b84\b', r'every (team|player) plays'],
            'p-ice-cream-van': [r'ice.cream', r'flavour', r'scoop', r'topping', r'binom\{11\}\{3\}', r'\b990\b', r'\b5775\b'],
        },
        2: {
            'p-signal-flags': [r'\bflags?\b', r'sailing', r'4 red', r'7!\}\{4!', r'\b105\b', r'tfrac\{5\}\{7\}'],
            'p-leisure-centre': [r'leisure', r'\bswim', r'\bgym\b', r'45 ?\+ ?38', r'do(es)? both', r'do(es)? neither', r'binom\{80\}\{2\}', r'binom\{17\}\{2\}'],
            'p-balloon-blocks': [r'BALLOON', r'letter blocks?', r'\b1260\b', r'\b660\b', r'tfrac\{11\}\{21\}', r'matching'],
            'p-quiz-team': [r'quiz team', r'youth club', r'girls', r'boys', r'binom\{11\}\{4\}', r'\b330\b', r'tfrac\{31\}\{33\}', r'at least one (woman|man|girl|boy)'],
        },
        3: {
            'p-orienteering': [r'orienteer', r'checkpoint', r'runner', r'\(9, ?12\)', r'9 \\\\ 12', r'-12 \\\\ 16', r'sqrt\{793\}', r'\(1, ?2\)'],
            'p-power-line': [r'pylon', r'power line', r'cable', r'engineer', r'\(6, ?4\)', r'6 \\\\ 4', r'15 \\\\ 10', r'2\.5\\?,?\\?overrightarrow'],
            'p-grain-merchant': [r'grain', r'wheat', r'barley', r'merchant', r'tonne', r'60 \\\\ 40', r'-145', r'2\.50 \\\\ -3\.50'],
            'p-sail-ring': [r'\bsail', r'centroid', r'median', r'tfrac\{2\}\{3\}\\?,?\\overrightarrow', r'midpoint of RS', r'mathbf\{r\}', r'frac\{1\}\{3\}\(?\\?mathbf'],
        },
    },
    'functions': {
        4: {
            'p-photo-mount': [r'print shop', r'\bmount', r'enlarge', r'1\.5x ?\+ ?4', r'x ?- ?4\}\{1\.5\}'],
            'p-fountain-jet': [r'fountain', r'\bjet\b', r'nozzle', r'0\.15x', r'h\(0\.8x\)', r'x\(12 ?- ?x\)'],
            'p-car-park': [r'car park', r'parking', r'receipt', r'2\.5t ?- ?2', r'2\.5\(t ?- ?2\)', r'C\(t ?- ?1\)'],
            'p-ticket-bonus': [r'bonus', r'theatre', r'ticket', r'5n ?- ?100', r'0\.2\(v ?- ?500\)', r'25n'],
        },
    },
}
ALSO = {'counting': ['counting-chance']}


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
for course, sets in PAT.items():
    files = sorted(glob.glob(f'app/content/courses/{course}/*.json')) + sorted(glob.glob('app/content/exams/*.json'))
    for extra in ALSO.get(course, []):
        files += sorted(glob.glob(f'app/content/courses/{extra}/*.json'))
    if wide:
        files += sorted(f for f in glob.glob('app/content/courses/*/*.json') if f not in files)
    blobs = {f: ' \n '.join(texts(json.load(open(f)))) for f in files}
    for n, items in sets.items():
        own = f'app/content/courses/{course}/problems-{n}.json'
        own_items = {i['id']: ' \n '.join(texts(i)) for i in json.load(open(own))['items']}
        for item, pats in items.items():
            print(f'== {course} {n} {item}')
            for p in pats:
                rx = re.compile(p)
                for f, b in blobs.items():
                    if f == own:
                        b = ' \n '.join(t for k, t in own_items.items() if k != item)
                    hits = list(rx.finditer(b))
                    if not hits:
                        continue
                    m = hits[0]
                    ctx = b[max(0, m.start() - 70):m.end() + 70].replace('\n', ' ')
                    print(f'   /{p}/ {f.replace("app/content/", "")} x{len(hits)}: ...{ctx}...')
