"""Delta read, freshness of the re-authored items: searches the content for the story words, numbers and formulae of each
re-authored item and prints every other place that holds them (file and a snippet). The reader judges the hits.

python3 docs/reviews/review-delta-holes-scripts/fresh.py      (from the repo root)"""
import glob
import json
import re

C = 'app/content/'


def strings(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, f'{path}.{k}' if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            idv = v.get('id') if isinstance(v, dict) else None
            yield from strings(v, f'{path}[{idv or i}]')
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        yield path, str(o)


def files(globs):
    out = []
    for g in globs:
        out += sorted(glob.glob(C + g, recursive=True))
    return out


ZERO1 = ['courses/number-sense/*.json', 'courses/fractions*/*.json', 'exams/topic-0.1.json', 'exams/stage-0*.json', 'exams/mock*.json']
ZERO2 = ['courses/quadratics/*.json', 'courses/equations/*.json', 'courses/functions/*.json', 'exams/topic-0.2.json', 'exams/stage-0*.json']
ST16 = ['courses/testing/*.json', 'courses/estimation/*.json', 'courses/regression/*.json', 'exams/topic-1.6.json', 'exams/stage-1*.json']
SL21 = ['courses/stat-learning/*.json', 'courses/ensembles/*.json', 'exams/topic-2.1.json', 'exams/stage-2*.json']
# [label, the item's own file, its item id, scope, patterns]
SEARCH = [
    ['p-hall-tiles (kitchen floor 360 by 600, HCF 120)', 'courses/number-sense/problems-4.json', 'p-hall-tiles', ZERO1,
     [r'kitchen', r'\btiles?\b', r'\b360\b.{0,60}\b600\b|\b600\b.{0,60}\b360\b', r'\b1,?800\b', r'21\.6\b']],
    ['p-lawn-pond (courtyard 14 by 11, basin 5 m across, tins of 15)', 'courses/number-sense/problems-4.json', 'p-lawn-pond', ZERO1,
     [r'courtyard', r'\bbasin\b', r'[Ss]ealant', r'\btins?\b', r'19\.6[34]', r'134\.37', r'6\.25\\pi', r'\b14 m by 11\b']],
    ['e-diameter-ends (circle centre (1, 6), radius 13)', 'exams/topic-0.2.json', 'e-diameter-ends', ZERO2,
     [r'\b169\b', r'5\^2 ?\+ ?12\^2', r'\(1, ?6\)', r'\(-4, ?-6\)', r'\(6, ?18\)', r'diameter']],
    ['p-windy-ride part 4 (9v over 16(v - 2))', 'courses/quadratics/problems-4.json', 'p-windy-ride', ZERO2, [r'9v', r'16\(v ?- ?2\)']],
    ['s-pareto-losses (recovery rates, theta x^(theta - 1) on (0, 1))', 'exams/topic-1.6.json', 's-pareto-losses', ST16,
     [r'[Rr]ecover', r'x\^\{\\theta ?- ?1\}', r'defaulted loans', r'\\sum ?\\ln x_i ?= ?-32', r'0\.078125|0\.0781\b']],
    ['p-disk-failures part 5 (efficiency at least 0.99, n = 200)', 'courses/testing/problems-4.json', 'p-disk-failures', ST16,
     [r'at least 0\.99', r'efficiency.{0,60}0\.99', r'\\tfrac\{198\}\{200\}', r'n ?- ?2\}\{n\}']],
    ['p-spam-filter part 4 (refit w = (0.9, -1.2), b = 0.3)', 'courses/stat-learning/problems-4.json', 'p-spam-filter', SL21,
     [r'0\.9, ?-1\.2', r'smaller \$C\$', r'0\.667']],
    ['p-one-unit parts 4 and 5 (eta 0.002, w1 0.596, knot 1.678)', 'courses/stat-learning/problems-4.json', 'p-one-unit', SL21,
     [r'0\.596', r'1\.678', r'eta ?= ?0\.002', r'8\.536']],
    ['e-odds-update (coefficient 0.45 on leverage, 10% at leverage 2)', 'exams/topic-2.1.json', 'e-odds-update', SL21,
     [r'leverage', r'e\^\{0\.9\}', r'0\.45\b.{0,80}log-odds|log-odds.{0,80}0\.45\b', r'21\.5']],
]

for label, own, iid, scope, pats in SEARCH:
    print('=' * 100)
    print(label)
    for pat in pats:
        hits = []
        for f in files(scope):
            doc = json.load(open(f))
            for path, s in strings(doc):
                if f == C + own and f'[{iid}]' in path:
                    continue
                m = re.search(pat, s)
                if m:
                    hits.append((f.replace(C, ''), path, s[max(0, m.start() - 60):m.end() + 60].replace('\n', ' ')))
        seen = {}
        for f, path, snip in hits:
            seen.setdefault(f, []).append((path, snip))
        print(f'  /{pat}/: {len(hits)} hit(s) in {len(seen)} file(s)')
        for f, lst in list(seen.items())[:8]:
            path, snip = lst[0]
            print(f'      {f} ({len(lst)}) {path[:60]}: ...{snip[:170]}...')
