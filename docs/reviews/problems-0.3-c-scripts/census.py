"""Second read, problems 0.3 c: parts by kind and wrong entries, per set. Run from the repo root with python3."""
import json

tot = {}
for c in ('series', 'trig'):
    for n in (1, 2, 3):
        d = json.load(open(f'app/content/courses/{c}/problems-{n}.json'))
        k = {'items': len(d['items']), 'parts': 0, 'numeric': 0, 'set': 0, 'expression': 0, 'choice': 0, 'wrong': 0}
        for it in d['items']:
            for p in it['parts']:
                w = p['widget']
                k['parts'] += 1
                k['set' if 'answers' in w else w['kind']] += 1
                k['wrong'] += len(w.get('wrong', []))
        print(c, n, k)
        for a, b in k.items():
            tot[(c, a)] = tot.get((c, a), 0) + b
print({f'{c} {a}': b for (c, a), b in tot.items()})
