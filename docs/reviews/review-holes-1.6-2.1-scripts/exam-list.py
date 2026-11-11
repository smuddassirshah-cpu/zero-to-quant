"""List the items of an exam file: id, difficulty, skills, widget kinds, title.
python3 exam-list.py <exam json> [...]   (also reads a file saved from an older commit)"""
import json
import sys

for path in sys.argv[1:]:
    d = json.load(open(path))
    print(path, {k: v for k, v in d.items() if not isinstance(v, (list, dict))})
    print(json.dumps(d.get('skills'), ensure_ascii=False))
    for it in d['items']:
        w = it.get('widget', {}).get('kind') or 'parts:' + ','.join(p['widget']['kind'] for p in it.get('parts', []))
        print(' ', it['id'], it['difficulty'], it['skills'], w, '|', it.get('title'))
