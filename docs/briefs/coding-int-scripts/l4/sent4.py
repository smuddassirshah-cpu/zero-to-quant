import json, re, glob
B = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app/content/courses/coding-int/'
files = ['l15-reading-an-assessment', 'l16-edge-cases-first', 'l17-two-in-sixty', 'l18-talking-while-coding', 'l19-a-live-round', 'review-4', 'homework-4']


def nsent(t):
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)
    t = re.sub(r'\$[^$]*\$', 'M', t)
    t = re.sub(r'`[^`]*`', 'C', t)
    return len([s for s in re.split(r'(?<=[.?])\s+', t.strip()) if s])


def walk(o, path, f):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('explain',) and isinstance(v, dict) and 'text' in v:
                if nsent(v['text']) > 3:
                    print('EXPLAIN >3', f, path, nsent(v['text']), v['text'][:70])
            if k == 'byKey':
                for kk, vv in v.items():
                    if nsent(vv) > 3:
                        print('BYKEY >3', f, path, kk)
            if k == 'why' and isinstance(v, str) and nsent(v) > 3:
                print('WHY >3', f, path)
            walk(v, path + '/' + k, f)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + '/' + str(i), f)


for f in files:
    d = json.load(open(B + f + '.json'))
    walk(d, '', f)
    for i, s in enumerate(d.get('screens', [])):
        words = len(re.sub(r'```.*?```', '', s['prose'], flags=re.S).split())
        if words > 60:
            print('PROSE >60', f, i + 1, words)
    # choices: key visibly longer than distractors
    def chk(w, where):
        if w and w.get('kind') == 'choice':
            lens = {o['id']: len(o['text']) for o in w['options']}
            key = [o['id'] for o in w['options'] if o.get('correct')][0]
            others = [v for k, v in lens.items() if k != key]
            if lens[key] > 1.5 * max(others):
                print('KEY LONGER', f, where, lens)
    for i, s in enumerate(d.get('screens', [])):
        chk(s.get('widget'), f'screen {i + 1}')
    for i, q in enumerate(d.get('quiz', [])):
        chk(q.get('widget'), f'quiz {i + 1}')
    for i, q in enumerate(d.get('items', [])):
        chk(q.get('widget'), f'item {i + 1}')
print('done')
