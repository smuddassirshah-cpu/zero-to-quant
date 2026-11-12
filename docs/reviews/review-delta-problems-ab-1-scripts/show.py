#!/usr/bin/env python3
"""Print items of a problem set compactly, to read them whole.
   show.py <course> <item-id>[:part,part] ...      (from the repo root)"""
import json, glob, sys
course = sys.argv[1]
for spec in sys.argv[2:]:
    iid, _, ps = spec.partition(':')
    parts = [int(x) for x in ps.split(',')] if ps else []
    for f in sorted(glob.glob(f'app/content/courses/{course}/problems-*.json')):
        for it in json.load(open(f))['items']:
            if it['id'] != iid:
                continue
            print('==', f.split('/')[-1], it['id'], 'difficulty', it.get('difficulty'), 'skills', it.get('skills'), 'lessons', it.get('lessons'))
            for a in it:
                if a not in ('id', 'difficulty', 'skills', 'lessons', 'parts'):
                    print(f'{a.upper()}:', it[a] if isinstance(it[a], str) else json.dumps(it[a], ensure_ascii=False))
            for k, p in enumerate(it['parts'], 1):
                if parts and k not in parts:
                    continue
                w = p['widget']
                print(f'-- part {k} [{w.get("kind")}]')
                print('   widget:', json.dumps({a: b for a, b in w.items() if a not in ('wrong', 'options')}, ensure_ascii=False))
                for o in w.get('options', []):
                    print('   opt:', json.dumps(o, ensure_ascii=False))
                for x in w.get('wrong', []):
                    print('   wrong:', json.dumps(x, ensure_ascii=False))
                for a in p:
                    if a == 'widget':
                        continue
                    b = p[a]
                    if isinstance(b, dict):
                        for c, d in b.items():
                            if isinstance(d, dict):
                                for e, h in d.items():
                                    print(f'   {a}.{c}.{e}:', h)
                            else:
                                print(f'   {a}.{c}:', d)
                    else:
                        print(f'   {a}:', b if isinstance(b, str) else json.dumps(b, ensure_ascii=False))
