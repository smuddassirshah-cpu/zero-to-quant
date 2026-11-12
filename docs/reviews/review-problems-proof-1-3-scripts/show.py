"""Second read, proof problems-1 to -3: print a problem set compactly for reading.
Usage (repo root): python3 docs/reviews/review-problems-proof-1-3-scripts/show.py <n>"""
import json
import sys

d = json.load(open(f'app/content/courses/proof/problems-{sys.argv[1]}.json'))
print({k: v for k, v in d.items() if k != 'items'})
for i, it in enumerate(d['items']):
    rest = [k for k in it if k not in ('id', 'difficulty', 'skills', 'prose', 'parts')]
    print(f"\n=== [{i}] {it['id']} diff {it.get('difficulty')} skills {it.get('skills')} keys {rest}")
    print('PROSE:', it.get('prose'))
    for j, p in enumerate(it['parts']):
        w = p.get('widget', {})
        rest = [k for k in p if k not in ('question', 'widget', 'feedback', 'explain')]
        print(f"\n--- part {j + 1} [{w.get('kind')}] extra keys {rest}")
        print('Q:', p.get('question'))
        print('W:', json.dumps({k: v for k, v in w.items() if k != 'wrong'}, ensure_ascii=False))
        for x in w.get('wrong', []):
            print('   wrong:', json.dumps(x, ensure_ascii=False))
        print('FB:', json.dumps(p.get('feedback'), ensure_ascii=False, indent=1))
        print('EX:', p.get('explain'))
