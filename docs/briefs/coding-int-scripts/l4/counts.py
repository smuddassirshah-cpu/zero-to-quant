import json, glob, os
C = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app/content/courses/coding-int/'
for f in ['l15-reading-an-assessment', 'l16-edge-cases-first', 'l17-two-in-sixty', 'l18-talking-while-coding', 'l19-a-live-round']:
    d = json.load(open(C + f + '.json'))
    codes = [(i + 1, s['widget']['language'], len(s['widget']['tests']), s.get('pace')) for i, s in enumerate(d['screens']) if s.get('widget', {}).get('kind') == 'code']
    print(f, len(d['screens']), 'screens', len(d['quiz']), 'quiz', [s['type'] for s in d['screens']], codes)
r = json.load(open(C + 'review-4.json'))
print('review', len(r['items']), [i['difficulty'] for i in r['items']], r['timed'])
h = json.load(open(C + 'homework-4.json'))
print('homework', len(h['items']), [i['difficulty'] for i in h['items']])
for it in h['items']:
    print(it['id'], it.get('tags'), [p['widget']['kind'] for p in it['parts']] if 'parts' in it else it['widget']['kind'])
