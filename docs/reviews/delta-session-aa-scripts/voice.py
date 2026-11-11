"""Delta read, session AA: em-dashes and exclamation marks in the prose of the files the three fix passes changed.

Run from the repo root. Code spans (`...`) and code fields are left out. voice-scan.py 35 covers sentence length.
"""
import glob
import json
import re
import sys

bad = []


def prose(s):
    return re.sub(r'`[^`]*`', '', s)


for f in sorted(glob.glob('app/content/drills/cpp-*.json') + glob.glob('app/content/drills/py-*.json')):
    d = json.load(open(f))
    texts = [d.get(k, '') for k in ('brief', 'hint', 'how', 'where')] + d.get('notes', []) + d.get('constraints', [])
    texts += [p['slip'] for p in d.get('planted', [])] + [t.get('note', '') for t in d.get('examples', [])]
    for s in texts:
        if '!' in prose(s) or '—' in s:
            bad.append((f, s[:60]))


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ('tex', 'answer', 'id'):
                yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


for f in ['limits-thm/problems-4', 'markov/problems-4', 'markov/problems-5', 'random-vars/problems-2',
          'random-vars/problems-4', 'random-vars/problems-5']:
    for s in strings(json.load(open(f'app/content/courses/{f}.json'))):
        t = re.sub(r'\$[^$]*\$', '', s)
        if '!' in t or '—' in s:
            bad.append((f, s[:60]))
print('em-dash or exclamation mark in prose:', len(bad), bad[:5])
sys.exit(1 if bad else 0)
