"""Print a drill for reading. Usage (repo root): python3 show.py <id> [field ...] [--full]"""
import json
import sys

args = [a for a in sys.argv[1:] if not a.startswith('--')]
full = '--full' in sys.argv
d = json.load(open(f'app/content/drills/{args[0]}.json'))
fields = args[1:] or ['difficulty', 'pace', 'fn', 'returns', 'brief', 'constraints', 'hint', 'examples', 'tests',
                      'how', 'notes', 'solution', 'planted']
for k in fields:
    v = d.get(k)
    print(f'--- {k}')
    if isinstance(v, list):
        for i, x in enumerate(v):
            if isinstance(x, dict) and 'code' in x:
                print(f'[{i}] slip: {x.get("slip")}')
                if full:
                    print(x['code'])
            else:
                s = json.dumps(x, ensure_ascii=False) if not isinstance(x, str) else x
                print(f'[{i}] {s if full else s[:600]}')
    else:
        print(v)
