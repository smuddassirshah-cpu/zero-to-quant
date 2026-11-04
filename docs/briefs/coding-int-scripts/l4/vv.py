import subprocess, re, sys
APP = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app'
out = subprocess.run(['node', 'tools/validate.mjs'], cwd=APP, capture_output=True, text=True).stdout
keys = ['coding-int/l15', 'coding-int/l16', 'coding-int/l17', 'coding-int/l18', 'coding-int/l19', 'coding-int/review-4', 'coding-int/homework-4',
        'drills/ci-', 'drills/index', 'drills/sessions']
for line in out.splitlines():
    if line.startswith('error') or any(k in line for k in keys):
        print(line[:400])
print(out.strip().splitlines()[-1])
