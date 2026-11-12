"""Second read, extra task: a random sample of 12 `ci-` drills whose `nearMiss` plant was an existing plant
(outcome "existing" in docs/reports/near-miss-1.md and near-miss-2.md). Seeded, so the sample can be redrawn.
Prints, per drill: statement, constraints, model solution and the marked plant, for the reader's verdict.
Run from the repo root:  python3 docs/reviews/review-problems-eigen-4-scripts/nearmiss-sample.py [--list | <drill id>]"""
import json
import random
import re
import sys

existing = {}
for line in open('docs/reports/near-miss-1.md'):
    m = re.match(r'- (ci-[\w-]+): existing \(plant (\d+)\)', line)
    if m:
        existing[m.group(1)] = int(m.group(2))
for line in open('docs/reports/near-miss-2.md'):
    if line.startswith('ci-') and ';' in line:
        for m in re.finditer(r'(ci-[\w-]+) (\d+)', line):
            existing[m.group(1)] = int(m.group(2))
pool = sorted(existing)
random.seed(20261112)
sample = sorted(random.sample(pool, 12))
print(f'pool: {len(pool)} drills marked "existing"; sample (seed 20261112): {sample}')
bad = 0
for d in sample:
    doc = json.load(open(f'app/content/drills/{d}.json'))
    blob = json.dumps(doc)
    marked = [i for i, p in enumerate(doc.get('planted') or doc.get('widget', {}).get('planted') or []) if p.get('nearMiss')]
    if not marked and '"nearMiss": true' not in blob:
        bad += 1
    print(f'   {d}: report says plant {existing[d]}, file marks plant(s) {marked}')
if '--list' in sys.argv:
    sys.exit(1 if bad else 0)
for d in (sys.argv[1:] or []):
    doc = json.load(open(f'app/content/drills/{d}.json'))
    print('\n' + '=' * 20, d, 'keys', list(doc))
    print(json.dumps({k: v for k, v in doc.items() if k not in ('tests', 'hidden', 'planted')}, indent=1, ensure_ascii=False)[:6000])
    for i, p in enumerate(doc.get('planted') or []):
        if p.get('nearMiss'):
            print(f'--- marked plant {i}:\n' + json.dumps(p, indent=1, ensure_ascii=False)[:3000])
sys.exit(1 if bad else 0)
