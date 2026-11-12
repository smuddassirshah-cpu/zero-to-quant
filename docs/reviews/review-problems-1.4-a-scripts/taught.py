"""Skim what a lesson teaches: one line a screen (type, title, start of prose, start of question).

Usage (repo root): python docs/reviews/review-problems-1.4-a-scripts/taught.py <course> <lesson-prefix>... [--len n] [--grep regex]
With --grep, prints only the screens whose text matches, with 200 characters around each hit."""
import glob
import json
import re
import sys

args = sys.argv[1:]
n = 170
pat = None
if '--len' in args:
    i = args.index('--len'); n = int(args[i + 1]); del args[i:i + 2]
if '--grep' in args:
    i = args.index('--grep'); pat = re.compile(args[i + 1], re.I); del args[i:i + 2]
course, prefixes = args[0], args[1:]
for f in sorted(glob.glob(f'app/content/courses/{course}/*.json')):
    name = f.split('/')[-1][:-5]
    if not any(name == p or name.startswith(p + '-') for p in prefixes):
        continue
    d = json.load(open(f))
    screens = d.get('screens') or d.get('items') or []
    print(f'#### {name}: {d.get("title", "")} ({len(screens)} screens)')
    for k, s in enumerate(screens):
        if pat:
            t = json.dumps(s, ensure_ascii=False)
            for m in list(pat.finditer(t))[:4]:
                print(f'  [{k}] {s.get("title", s.get("id", ""))} | ...{t[max(0, m.start() - 200):m.end() + 200]}...')
            continue
        prose = s.get('prose') or s.get('text') or ''
        if isinstance(prose, list):
            prose = ' '.join(map(str, prose))
        q = s.get('question') or ''
        parts = s.get('parts') or []
        pq = ' || '.join((p.get('question') or '')[:n // 2] for p in parts)
        print(f'  [{k}] {s.get("type", "")} {s.get("title", s.get("id", ""))!r} | {prose[:n]} | Q: {q[:n]}{" || " + pq if pq else ""}')
