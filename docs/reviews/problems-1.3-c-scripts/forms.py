"""Shape checks on the five sets: parts and kinds, explanation length, a stated answer form on every numeric part,
wrong[] bands wide against their own value, and whether each later part restates a value (a "Using ..." or a quoted number).

Usage (repo root): python docs/reviews/problems-1.3-c-scripts/forms.py
"""
import json
import re

FORM = re.compile(r'Give |whole number|as a decimal|exact|nearest|decimal place|in terms of', re.I)
for c, n in [('limits', 4), ('limits', 5), ('integrals', 4), ('multivar', 4), ('multivar', 5)]:
    d = json.load(open(f'app/content/courses/{c}/problems-{n}.json'))
    kinds = {}
    for it in d['items']:
        for i, p in enumerate(it['parts'], 1):
            w = p['widget']
            k = w['kind']
            kinds[k] = kinds.get(k, 0) + 1
            e = p['explain']
            e = e['text'] if isinstance(e, dict) else e
            t = re.sub(r'\$[^$]*\$', 'M', e)
            sents = [x for x in re.split(r'(?<=[.?:])\s+(?=[A-Z])', t) if x.strip()]
            if len([x for x in re.split(r'(?<=[.?])\s+', t) if x.strip()]) > 3:
                print('  LONG EXPLAIN', c, n, it['id'], i, len(sents))
            if k == 'numeric' and not FORM.search(p['question']):
                print(f"  NO FORM   {c} {n} {it['id']} part {i}: answer {w['answer']} tol {w.get('tol')} | {p['question'][-110:]}")
            if k == 'numeric':
                for x in w.get('wrong', []):
                    tt = (x.get('tol') or {}).get('abs', 0)
                    if tt and abs(x['value']) > 0 and tt > 0.2 * abs(x['value']):
                        print(f"  WIDE WRONG {c} {n} {it['id']} part {i}: {x['id']} = {x['value']} ±{tt}")
            if i > 1 and not re.search(r'Using|from part|Part \d|part \d|parts \d', p['question']):
                print(f"  NO RESTATE {c} {n} {it['id']} part {i}: {p['question'][:120]}")
            if 'accept' in w and isinstance(w['accept'], str) and 'Any form' in w['accept']:
                print(f"  ANY FORM  {c} {n} {it['id']} part {i}: {w['accept']}")
    print(c, n, len(d['items']), 'items', sum(kinds.values()), 'parts', kinds, [(it['id'], it['difficulty'], len(it['parts'])) for it in d['items']])
