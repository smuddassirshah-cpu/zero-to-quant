"""List every code task (any dict holding a `starter` or `solution` string) in the lessons,
reviews and homework of a course: file, function names defined, and the start of its prompt.
Run from the repo root: python docs/reviews/drills-py-scripts/lesson_tasks.py <course> [file-prefix ...]"""
import json, re, sys, glob, os

course = sys.argv[1]
prefixes = sys.argv[2:]


def walk(o, path, out):
    if isinstance(o, dict):
        code = ' '.join(str(o.get(k, '')) for k in ('starter', 'solution', 'code') if isinstance(o.get(k), str))
        if code and ('def ' in code or 'class ' in code or o.get('type') == 'code'):
            names = sorted(set(re.findall(r'(?:def|class)\s+([A-Za-z_]\w*)', code)))
            prompt = str(o.get('prompt') or o.get('brief') or o.get('task') or o.get('q') or o.get('text') or '')
            out.append((path, names, prompt[:230].replace('\n', ' ')))
        for k, v in o.items():
            walk(v, path, out)
    elif isinstance(o, list):
        for v in o:
            walk(v, path, out)


for f in sorted(glob.glob(f'app/content/courses/{course}/*.json')):
    base = os.path.basename(f)[:-5]
    if prefixes and not any(base.startswith(p) for p in prefixes):
        continue
    out = []
    walk(json.load(open(f)), base, out)
    for path, names, prompt in out:
        print(f'{path}: {names} | {prompt}')
