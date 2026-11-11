"""Print the source of fluency families, one compact line a field: family.py <set file> [family id ...]"""
import json
import sys

d = json.load(open(sys.argv[1]))
print({k: v for k, v in d.items() if k != 'families'})
for f in d['families']:
    if sys.argv[2:] and f['id'] not in sys.argv[2:]:
        continue
    print('==', f['id'])
    for k, v in f.items():
        if k == 'wrong':
            for w in v:
                print('   wrong', json.dumps(w, ensure_ascii=False))
        elif k != 'id':
            print('  ', k, json.dumps(v, ensure_ascii=False))
