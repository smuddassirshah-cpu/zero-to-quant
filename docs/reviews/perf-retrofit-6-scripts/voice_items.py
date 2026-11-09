"""Voice scan of the five items' strings: no '!', no em-dash or en-dash,
no listed American spellings, longest prose sentence (maths and code cut out).
Exit 0 when clean. Run from this folder: python3 voice_items.py
"""
import json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
ITEMS = [('contests/homework-3.json', 'hw3-due-order'), ('alpha/homework-4.json', 'h-neutral-book'),
         ('opt-dash/homework-4.json', 'h4-weekend-explain'), ('ensembles/homework-2.json', 'hw-floor-derive'),
         ('fin-ml/homework-2.json', 'h-return-rank')]
SKIP = {'starter', 'solution', 'setup', 'call', 'compiles', 'expect', 'id', 'kind', 'language', 'compare', 'performance', 'skills', 'tags', 'prelude'}
AMERICAN = r'\b(color\w*|behavior\w*|favor\w*|center\w*|analyz\w*|optimiz\w*|modeling|labeled|neighbor\w*|gray|normaliz\w*|recogniz\w*)\b'
bad = 0
def strings(o, key=''):
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in SKIP:
                yield from strings(v, k)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, key)
    elif isinstance(o, str):
        yield o
for f, i in ITEMS:
    it = next(x for x in json.load(open(os.path.join(ROOT, 'app/content/courses', f)))['items'] if x['id'] == i)
    longest, worst = 0, ''
    for s in strings(it):
        if '!' in re.sub(r'\$[^$]*\$|`[^`]*`|```.*?```', '', s, flags=re.S) or '—' in s or '–' in s:
            print('PUNCT', i, s[:80]); bad += 1
        for m in re.finditer(AMERICAN, s, flags=re.I):
            print('SPELL', i, m.group(0)); bad += 1
        prose = re.sub(r'```.*?```', ' ', s, flags=re.S)
        prose = re.sub(r'\$\$.*?\$\$', ' X. ', prose, flags=re.S)
        prose = re.sub(r'\$[^$]*\$', 'X', prose)
        prose = re.sub(r'`[^`]*`', 'X', prose)
        for sent in re.split(r'(?<=[.?:;])\s+|\n+', prose):
            w = len(sent.split())
            if w > longest:
                longest, worst = w, sent
    print('%-22s longest sentence %2d words: %s' % (i, longest, worst[:90]))
    if longest > 35:
        bad += 1
for f, i in ITEMS:
    it = next(x for x in json.load(open(os.path.join(ROOT, 'app/content/courses', f)))['items'] if x['id'] == i)
    t = re.sub(r'\$[^$]*\$', 'X', it['explain']['text'])
    n = len([x for x in re.split(r'(?<=[.?])\s+', t.strip()) if x])
    print('%-22s explain sentences %d' % (i, n)); bad += n > 3
print('problems:', bad)
sys.exit(1 if bad else 0)
