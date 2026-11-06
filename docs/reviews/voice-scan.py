"""List learner-visible sentences over MAX words in one course (or an exam file).
Usage: VOICE_BASE=/home/user/zero-to-quant/app/content/courses/<course>/ python3 docs/reviews/voice-scan.py [MAX=20] [--summary]
Canvas derive/let/formula strings are skipped (a derive caption is scanned). A $...$ formula, $$...$$ block `code` span or {{template}} value counts as one word; fenced code is dropped.
"""
import json, glob, re, sys, os
BASE = os.environ.get('VOICE_BASE', '/home/user/zero-to-quant/app/content/courses/graphs-dp/')
BASE = os.path.join(os.path.abspath(BASE), '')
if not glob.glob(BASE + '*.json'):
    sys.exit('voice-scan: no .json files in ' + BASE)
MAX = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20
# keys whose values are code, tests, ids or structure (never prose)
SKIP = {'id', 'kind', 'type', 'course', 'skills', 'answer', 'accept_ids', 'starter', 'solution',
        'prelude', 'postlude', 'setup', 'call', 'expect', 'compare', 'tex', 'language', 'highlight',
        'ids', 'from', 'to', 'layout', 'shape', 'set', 'only', 'dim', 'outline', 'shade', 'flash',
        'tone', 'orient', 'mode', 'itemKind', 'bind', 'start', 'target', 'unit', 'align', 'files', 'outcome'}
def strings(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in SKIP: continue
            yield from strings(v, f'{path}.{k}' if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, f'{path}.{i}')
def mask(t):
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)
    t = re.sub(r'`[^`]*`', 'CODE', t)
    t = re.sub(r'\{\{.*?\}\}', 'VALUE', t, flags=re.S)
    t = re.sub(r'\$\$.*?\$\$', ' MATH ', t, flags=re.S)
    t = re.sub(r'\$[^$]*\$', 'MATH', t)
    return t
def sentences(t):
    t = mask(t)
    out = []
    for line in t.split('\n'):
        line = line.strip()
        if not line: continue
        if line.startswith('|'):  # markdown table: each cell
            if re.fullmatch(r'[|:\- ]+', line): continue
            parts = [c.strip() for c in line.strip('|').split('|')]
        else:
            parts = [line]
        for p in parts:
            p = re.sub(r'^([-*]|\d+\.)\s+', '', p)
            # split after . ? ! ; but not inside decimals like 0.5 or e.g.
            # a bold or italic heading ending in a full stop, or a closing bracket or quote, also ends a sentence
            for s in re.split(r'(?:(?<=[.?!])|(?<=[.?!]\*\*)|(?<=[.?!]\*)|(?<=[.!]")|(?<=[.?!]\)))\s+(?=\S)', p):
                if s.strip(): out.append(s.strip())
    return out
def words(s):
    return len([w for w in s.split() if re.search(r'[A-Za-z0-9£]', w)])
def is_formula_path(path):
    """canvas derive rules (let, targets), curve and function formulas are expressions, not prose; a derive caption is prose (ENGINE-BACKLOG 580)"""
    if re.search(r'(^|\.)derive\.', path):
        return not re.search(r'derive\.caption$', path)
    return bool(re.search(r'\.(expr|formula|formulas|polar|inner)$', path)) and '.canvas.' in path
def is_code_path(path):
    if is_formula_path(path): return True
    return '.canvas.params.lines.' in path or path.endswith('.code') or '.tests.' in path and not re.search(r'\.(why|hint|feedback)$', path)
rows = []; total = 0
for f in sorted(glob.glob(BASE + '*.json')):
    name = os.path.basename(f)
    if name == 'course.json': continue
    for path, t in strings(json.load(open(f))):
        if is_code_path(path): continue
        for s in sentences(t):
            total += 1
            n = words(s)
            if n > MAX: rows.append((name, path, n, s))
# explanation fields: at most three sentences
over3 = []
for f in sorted(glob.glob(BASE + '*.json')):
    name = os.path.basename(f)
    if name == 'course.json': continue
    for path, t in strings(json.load(open(f))):
        if re.search(r'(explain\.text|\.why|\.byKey\.[^.]+)$', path):
            n = len(sentences(t))
            if n > 3: over3.append((name, path, n))
if '--summary' not in sys.argv:
    for name, path, n, s in rows:
        print(f'{name} | {path} | {n} | {s}')
for name, path, n in over3: print(f'# explanation over three sentences: {name} | {path} | {n}')
print(f'# explanations over three sentences: {len(over3)}')
print(f'# sentences scanned: {total}; over {MAX} words: {len(rows)}')
