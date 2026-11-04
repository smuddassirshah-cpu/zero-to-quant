"""Freshness grep for exam topic-3.5: search every content file, brief and mock script for each candidate key.

Run: python3 fresh.py 'pattern' ['pattern' ...]    (regular expressions, case-insensitive)
Builds corpus.txt next to this script from app/content/**/*.json (all lessons, reviews, homework, drills, bank,
exams, data) and docs/briefs/*.md and mocks-scripts, skipping topic-3.5 itself.
"""
import json, glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CORPUS = os.path.join(HERE, 'corpus.txt')
ONLY = os.environ.get('ONLY', '')  # regex on file names, e.g. 'research-int|coding-int|systems|exams|bank|drills|mocks'

def walk(o, acc):
    if isinstance(o, str): acc.append(o)
    elif isinstance(o, (int, float)) and not isinstance(o, bool): acc.append(str(o))
    elif isinstance(o, list):
        for x in o: walk(x, acc)
    elif isinstance(o, dict):
        for v in o.values(): walk(v, acc)

def build():
    with open(CORPUS, 'w') as out:
        for f in sorted(glob.glob(ROOT + '/app/content/**/*.json', recursive=True)):
            if f.endswith('manifest.json') or 'topic-3.5' in f: continue
            try: d = json.load(open(f))
            except Exception: continue
            acc = []; walk(d, acc)
            out.write('@@ ' + f.replace(ROOT + '/', '') + '\n' + ' | '.join(acc) + '\n')
        for f in sorted(glob.glob(ROOT + '/docs/briefs/*.md')) + sorted(glob.glob(ROOT + '/docs/briefs/mocks-scripts/*.json')) + sorted(glob.glob(ROOT + '/docs/briefs/mocks-scripts/*.md')):
            out.write('@@ ' + f.replace(ROOT + '/', '') + '\n' + open(f).read() + '\n')

if __name__ == '__main__':
    if not os.path.exists(CORPUS) or '--rebuild' in sys.argv: build()
    pats = [a for a in sys.argv[1:] if a != '--rebuild']
    text = open(CORPUS).read().split('@@ ')
    for p in pats:
        rx = re.compile(p, re.I)
        hits = []
        for blk in text:
            name, _, body = blk.partition('\n')
            if ONLY and not re.search(ONLY, name): continue
            for m in rx.finditer(body):
                hits.append((name, body[max(0, m.start() - 50):m.end() + 50].replace('\n', ' ')))
        print('==', p, len(hits))
        for h in hits[:6]: print('   ', h[0], '::', h[1])
