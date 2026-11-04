"""Build app/content/exams/topic-3.2.json from build_ito, build_mp and build_pdes.
Run: python3 build.py  (from any folder). File order: difficulty 2, 3, 4, 5, courses interleaved.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_ito import ITEMS as I
from build_mp import ITEMS as M
from build_pdes import ITEMS as P

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'app', 'content', 'exams', 'topic-3.2.json')

ALL = {}
for k, v in I.items(): ALL['I%d' % k] = v
for k, v in M.items(): ALL['M%d' % k] = v
for k, v in P.items(): ALL['P%d' % k] = v
assert len(ALL) == 30, len(ALL)

ORDER = ['I1', 'M1', 'P1', 'I3', 'M3', 'M10',                                     # difficulty 2
         'I2', 'M2', 'P2', 'I4', 'M5', 'P4', 'I5', 'M6', 'P5', 'I6', 'M7', 'P6', 'I10', 'M9', 'P7',  # 3
         'I7', 'M4', 'P3', 'I8', 'M11', 'I9',                                       # 4
         'I11', 'M8', 'P8']                                                         # 5
assert sorted(ORDER) == sorted(ALL)
items = [ALL[k] for k in ORDER]
diffs = [i['difficulty'] for i in items]
assert diffs == sorted(diffs)
assert [diffs.count(d) for d in (2, 3, 4, 5)] == [6, 15, 6, 3], [diffs.count(d) for d in (2, 3, 4, 5)]

SKILLS = {
    "it-bm": "Brownian motion", "it-calculus": "Itô calculus", "it-martingale": "Martingales and measures",
    "it-pricing": "Continuous-time pricing",
    "mt-sigma": "Sigma-algebras and measures", "mt-integral": "The Lebesgue integral", "mt-condexp": "Conditional expectation",
    "mt-martingale": "Martingales and stopping times", "mt-change": "Change of measure",
    "pe-heat": "The heat equation", "pe-fourier": "Fourier series and separation", "pe-bs": "Black-Scholes as a heat equation",
    "pe-fk": "Feynman-Kac", "pe-fd": "Finite-difference solution",
}
counts = {}
for it in items:
    for s in it['skills']:
        assert s in SKILLS, s
        counts[s] = counts.get(s, 0) + 1
PLAN = dict(zip("it-bm it-calculus it-martingale it-pricing mt-sigma mt-integral mt-condexp mt-martingale mt-change pe-heat pe-fourier pe-bs pe-fk pe-fd".split(),
                [4, 5, 3, 3, 2, 2, 3, 3, 3, 3, 3, 1, 1, 1]))
assert counts == PLAN, (counts, PLAN)
pace = sum(i['pace'] for i in items)
print('pace', pace, pace / 60)
assert pace == 4875, pace

exam = {"id": "topic-3.2", "topic": "3.2", "name": "Stochastic calculus", "minutes": 90, "pass": 0.7, "skills": SKILLS, "items": items}
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(exam, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('wrote', OUT, len(items))
