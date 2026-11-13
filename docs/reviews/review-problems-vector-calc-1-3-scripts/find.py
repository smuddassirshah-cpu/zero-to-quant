"""find.py <file> <needle>...: print top-level items/screens (learner text, trimmed) containing every needle."""
import json, sys
d = json.load(open(sys.argv[1]))
needles = sys.argv[2:]
def texts(o, out):
    if isinstance(o, str):
        out.append(o)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ('canvas', 'tests', 'hidden', 'solution', 'starter') and not isinstance(v, str):
                continue
            texts(v, out)
    elif isinstance(o, list):
        for v in o:
            texts(v, out)
for key in ('screens', 'items', 'quiz', 'families'):
    for i, it in enumerate(d.get(key, [])):
        out = []
        texts(it, out)
        s = ' | '.join(out)
        if all(n in s for n in needles):
            print('--- %s[%d] %s' % (key, i, it.get('id', it.get('title', ''))))
            print(s[:int(1400)])
