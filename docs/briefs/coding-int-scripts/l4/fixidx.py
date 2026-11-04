import json
p = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app/content/drills/index.json'
idx = json.load(open(p))
idx = [r for r in idx if r['id'] != 'ci-' + 'digit' + '-sum-pairs']
with open(p, 'w') as f:
    json.dump(idx, f, indent=2, ensure_ascii=False)
    f.write('\n')
print(len(idx))
