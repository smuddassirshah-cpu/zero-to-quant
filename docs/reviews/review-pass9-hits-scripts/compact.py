"""Compact view of the parts named in docs/reports/engine-pass-9-hits.md.

Usage (from the repo root): python docs/reviews/review-pass9-hits-scripts/compact.py <tag> [file-substring]
Prints, per hit part: the stem, the earlier questions with keys, the question, the key and band,
every wrong value with its band and feedback line, and the correct feedback.
"""
import json, re, sys, os

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..')
hits = []
for line in open(os.path.join(ROOT, 'docs/reports/engine-pass-9-hits.md'), encoding='utf-8'):
    m = re.match(r'- \[([a-z-]+)\] (courses/\S+) \| (\S+) \| part (\d+) \| (.*)', line)
    if m:
        hits.append(m.groups())

tag = sys.argv[1]
sub = sys.argv[2] if len(sys.argv) > 2 else ''
seen = set()
for t, f, pid, part, msg in hits:
    if t != tag or sub not in f:
        continue
    key = (f, pid, part)
    m = re.search(r'wrong "([^"]+)"', msg)
    flagged = m.group(1) if m else ('KEY' if 'the key' in msg else '')
    if key in seen:
        print('   also flagged:', flagged)
        continue
    seen.add(key)
    d = json.load(open(os.path.join(ROOT, 'app/content', f), encoding='utf-8'))
    idx = [i for i, it in enumerate(d['items']) if it.get('id') == pid][0]
    it = d['items'][idx]
    pi = int(part) - 1
    p = it['parts'][pi]
    w = p.get('widget', {})
    print('=' * 80)
    print(f'{f[8:]} items[{idx}] {pid} parts[{pi}] flagged={flagged}')
    print('STEM:', it.get('prose', '')[:900])
    for k in it:
        if k not in ('prose', 'parts', 'id', 'difficulty', 'skills'):
            print('  stem.' + k + ':', json.dumps(it[k], ensure_ascii=False)[:500])
    for q in it['parts'][:pi]:
        qw = q.get('widget', {})
        print('  prev:', q.get('question'), '| key', qw.get('answer'), qw.get('tol'))
    print('Q:', p.get('question'))
    wk = {k: v for k, v in w.items() if k != 'wrong'}
    print('W:', json.dumps(wk, ensure_ascii=False))
    fb = p.get('feedback', {})
    for x in w.get('wrong', []) or []:
        print('  wrong', x.get('id'), x.get('value'), x.get('tol'), '|', fb.get('byKey', {}).get(x.get('id'), ''))
    print('correct:', fb.get('correct'))
    print('generic:', fb.get('generic'))
    if tag != 'key-in-question':
        print('explain:', p.get('explain', {}).get('text'))
