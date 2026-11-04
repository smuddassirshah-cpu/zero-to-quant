import json
m = json.load(open('/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app/content/manifest.json'))
dr = m['drills']
idx = json.load(open('/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app/content/drills/index.json'))
rows = {r['id']: r for r in idx}
print(type(dr), len(dr))
items = dr.items() if isinstance(dr, dict) else [(d['id'], d) for d in dr]
for pat in ('prefix-sums', 'hashing', 'intervals'):
    for lang in ('python', 'cpp'):
        pool = []
        for did, d in items:
            if did not in rows or d.get('sample'):
                continue
            if d.get('pattern') != pat or (d.get('language') or 'python') != lang:
                continue
            diff = rows[did]['difficulty']
            if 3 <= diff <= 4:
                pool.append(did)
        print(pat, lang, pool)
