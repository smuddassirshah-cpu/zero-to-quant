"""Print one screen or item of a content file without its canvas: screen.py <N chars> <file> <key:index> [...]
   key is s (screens), q (quiz) or i (items); index is 1-based."""
import json
import sys

N = int(sys.argv[1])
d = json.load(open(sys.argv[2]))
for ref in sys.argv[3:]:
    k, i = ref.split(':')
    s = d[{'s': 'screens', 'q': 'quiz', 'i': 'items'}[k]][int(i) - 1]
    s = {a: b for a, b in s.items() if a != 'canvas'}
    print(ref, json.dumps(s, ensure_ascii=False)[:N])
    print()
