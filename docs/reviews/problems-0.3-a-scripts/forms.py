"""Shape checks on the six sets: parts and kinds, difficulty, skills against the level's lesson skills, explanation length,
a stated answer form on every numeric part, wrong[] bands wide against their own value, whether each later part restates a
value, choice parts (share, key length, options named by place), and reading load (words in prose and questions).

Usage (repo root): python3 docs/reviews/problems-0.2-a-scripts/forms.py
"""
import json
import re

FORM = re.compile(r'Give |whole number|as a decimal|exact|nearest|decimal place|in terms of|How many', re.I)
PLACE = re.compile(r'\b(first|second|third|fourth|last|top|bottom) (option|choice|answer)|option [A-D1-4]\b|\babove\b|\bbelow\b', re.I)
tot = {}
for c in ('equations', 'functions'):
    cj = json.load(open(f'app/content/courses/{c}/course.json'))
    for n in (1, 2, 3):
        d = json.load(open(f'app/content/courses/{c}/problems-{n}.json'))
        lessons = next(lv for lv in cj['levels'] if lv['n'] == n)['lessons']
        lskills = set()
        for l in lessons:
            lj = json.load(open(f'app/content/courses/{c}/{l}.json'))
            lskills |= set(lj.get('skills', []))
            for s in lj.get('screens', []) + lj.get('quiz', []):
                lskills |= set(s.get('skills', []))
        kinds = {}
        words = []
        for it in d['items']:
            if not set(it['skills']) <= lskills:
                print(f'  SKILL     {c} {n} {it["id"]}: {set(it["skills"]) - lskills} not a skill of the level ({sorted(lskills)})')
            words.append(len(re.sub(r'\$[^$]*\$', 'M', it['prose']).split()))
            for i, p in enumerate(it['parts'], 1):
                w = p['widget']
                k = w['kind']
                kinds[k] = kinds.get(k, 0) + 1
                e = p['explain']
                e = e['text'] if isinstance(e, dict) else e
                t = re.sub(r'\$[^$]*\$', 'M', e)
                if len([x for x in re.split(r'(?<=[.?])\s+', t) if x.strip()]) > 3:
                    print(f'  LONG EXPLAIN {c} {n} {it["id"]} part {i}')
                q = p['question']
                if k == 'numeric' and not FORM.search(q):
                    print(f"  NO FORM   {c} {n} {it['id']} part {i}: answer {w.get('answer', w.get('answers'))} tol {w.get('tol')} | {q[-110:]}")
                if k == 'numeric':
                    for x in w.get('wrong', []):
                        tt = (x.get('tol') or {}).get('abs', 0)
                        if tt and isinstance(x['value'], (int, float)) and abs(x['value']) > 0 and tt > 0.2 * abs(x['value']):
                            print(f"  WIDE WRONG {c} {n} {it['id']} part {i}: {x['id']} = {x['value']} ±{tt}")
                if i > 1 and not re.search(r'Using|from part|Part \d|part \d|[Pp]arts \d|\$', q):
                    print(f"  NO RESTATE {c} {n} {it['id']} part {i}: {q[:140]}")
                if i > 1 and not re.search(r'Using|from part|Part \d|part \d|[Pp]arts \d', q):
                    print(f"  no lead-in {c} {n} {it['id']} part {i}: {q[:140]}")
                if k == 'choice':
                    opts = w['options']
                    lens = [len(o['text']) for o in opts]
                    right = next(o for o in opts if o.get('correct'))
                    if len(right['text']) == max(lens) and sorted(lens)[-1] > 1.25 * sorted(lens)[-2]:
                        print(f"  KEY LENGTH {c} {n} {it['id']} part {i}: key {len(right['text'])} chars, others {lens}")
                    blob = ' '.join([o.get('why', '') + ' ' + o['text'] for o in opts] + [json.dumps(p['feedback']), e])
                    if PLACE.search(blob):
                        print(f"  BY PLACE? {c} {n} {it['id']} part {i}: {PLACE.search(blob).group(0)}")
                words.append(len(re.sub(r'\$[^$]*\$', 'M', q).split()))
        parts = sum(kinds.values())
        typed = parts - kinds.get('choice', 0)
        print(c, n, len(d['items']), 'items', parts, 'parts', kinds, f'typed {typed}/{parts}',
              [(it['id'], it['difficulty'], len(it['parts'])) for it in d['items']], f'longest text {max(words)} words')
        for k, v in kinds.items():
            tot[(c, k)] = tot.get((c, k), 0) + v
print(tot)
