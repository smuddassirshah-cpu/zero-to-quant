"""Dump the parts named in docs/reports/engine-pass-9-hits.md for reading.

Usage (from the repo root): python docs/reviews/review-pass9-hits-scripts/dump.py [tag] [file-substring]
"""
import json, re, sys, os

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..')
hits = []
for line in open(os.path.join(ROOT, 'docs/reports/engine-pass-9-hits.md'), encoding='utf-8'):
    m = re.match(r'- \[([a-z-]+)\] (courses/\S+) \| (\S+) \| part (\d+) \| (.*)', line)
    if m:
        hits.append(m.groups())

args = [a for a in sys.argv[1:] if not a.startswith('--')]
tag = args[0] if args else None
sub = args[1] if len(args) > 1 else ''
seen = set()
for t, f, pid, part, msg in hits:
    if tag and t != tag:
        continue
    if sub not in f:
        continue
    key = (f, pid, part)
    d = json.load(open(os.path.join(ROOT, 'app/content', f), encoding='utf-8'))
    idx = [i for i, it in enumerate(d['items']) if it.get('id') == pid][0]
    it = d['items'][idx]
    p = it['parts'][int(part) - 1]
    m = re.search(r'wrong "([^"]+)"', msg)
    print('=' * 100)
    print(f'[{t}] {f} items[{idx}] {pid} parts[{int(part)-1}]', ('wrong=' + m.group(1)) if m else msg[:60])
    if key in seen:
        continue
    seen.add(key)
    stem = {k: v for k, v in it.items() if k != 'parts'}
    print('STEM:', json.dumps(stem, ensure_ascii=False)[:1400])
    if '--prev' in sys.argv:
        for q in it['parts'][:int(part) - 1]:
            print('  PREV Q:', q.get('question'), '| key', q.get('widget', {}).get('answer', q.get('widget', {}).get('value')))
    print('PART:', json.dumps(p, ensure_ascii=False, indent=1))
