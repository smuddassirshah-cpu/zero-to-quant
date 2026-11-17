"""Print learner-facing text of a content file. usage: taught.py file [maxchars] [top-key[:index]]"""
import json, sys
f = sys.argv[1]
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 400
sel = sys.argv[3] if len(sys.argv) > 3 else None
d = json.load(open(f))
SKIP = {'id', 'kind', 'type', 'keyboard', 'layout', 'skills', 'canvas', 'widget_id', 'art', 'course'}

def strings(o, out, key=None):
    if isinstance(o, str):
        if key not in SKIP and (' ' in o or '$' in o or key in ('answer', 'tex')):
            out.append(o)
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        if key in ('answer', 'value'):
            out.append('<%s=%s>' % (key, o))
    elif isinstance(o, list):
        for x in o:
            strings(x, out, key)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ('correct',) and isinstance(v, bool):
                out.append('<CORRECT>')
            strings(v, out, k)

for top in ('screens', 'quiz', 'items'):
    if top not in d:
        continue
    for i, s in enumerate(d[top]):
        if sel:
            t, _, ix = sel.partition(':')
            if t != top or (ix and int(ix) != i):
                continue
        out = []
        strings(s, out)
        txt = ' | '.join(out)
        print('%s[%d] %s: %s' % (top, i, s.get('id', s.get('type', '')), txt[:mx]))
