import sys, importlib
sys.path.insert(0, '.')
from lib2 import write, check_voice

OUT = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app/content/courses/coding-int/'
mods = {
    'l15-reading-an-assessment.json': ('b15', 'lesson'),
    'l16-edge-cases-first.json': ('b16', 'lesson'),
    'l17-two-in-sixty.json': ('b17', 'lesson'),
    'l18-talking-while-coding.json': ('b18', 'lesson'),
    'l19-a-live-round.json': ('b19', 'lesson'),
    'review-4.json': ('b_rev', 'build'),
    'homework-4.json': ('b_hw', 'build'),
}
only = sys.argv[1:]
for name, (m, fn) in mods.items():
    if only and not any(name.startswith(o) for o in only):
        continue
    try:
        mod = importlib.import_module(m)
    except ModuleNotFoundError:
        print('skip', name)
        continue
    obj = getattr(mod, fn)()
    for b in check_voice(obj):
        print('VOICE', name, b)
    write(OUT + name, obj)
    print('wrote', name)
