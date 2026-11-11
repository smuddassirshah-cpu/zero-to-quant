"""Print the learner-facing text of drills as they stand, for a whole read.

drill_text.py [--code] [--width N] <drill id> ...
Prints every field; long values are cut at --width characters (default 700). Planted code only with --code.
"""
import json
import sys

args = sys.argv[1:]
code = '--code' in args
if code:
    args.remove('--code')
width = 700
if '--width' in args:
    i = args.index('--width')
    width = int(args[i + 1])
    del args[i:i + 2]


def cut(s):
    s = str(s)
    return s if len(s) <= width else s[:width] + f' ...[{len(s)} chars]'


for i in args:
    d = json.load(open(f'app/content/drills/{i}.json'))
    print('=' * 20, i)
    for k, v in d.items():
        if k in ('tests', 'examples'):
            print(f'{k}: {len(v)}')
            for n, t in enumerate(v):
                extra = {a: b for a, b in t.items() if a not in ('call', 'expect', 'compare', 'args', 'types')}
                call = t.get('call', '') + (' args=' + json.dumps(t['args']) if 'args' in t else '')
                print(f'  [{n}] {cut(call)} -> {cut(t.get("expect"))} ({t.get("compare")}) {extra if extra else ""}')
        elif k == 'planted':
            print(f'planted: {len(v)}')
            for n, p in enumerate(v):
                print(f'  [{n}] {p["slip"]}')
                if code:
                    print('      ' + p['code'].replace('\n', '\n      '))
        elif isinstance(v, list):
            print(f'{k}:')
            for x in v:
                print('  - ' + cut(x if isinstance(x, str) else json.dumps(x)))
        elif isinstance(v, str) and '\n' in v and k in ('starter', 'solution', 'prelude', 'postlude'):
            print(f'{k}:')
            print('    ' + cut(v).replace('\n', '\n    '))
        else:
            print(f'{k}: {cut(v if isinstance(v, str) else json.dumps(v))}')
