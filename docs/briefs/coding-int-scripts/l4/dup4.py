"""Freshness: list literals and big numbers in my files against every other content file, and review/homework against lessons."""
import glob, json, os, re, sys
APP = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app/content/'
C = APP + 'courses/coding-int/'
mine_lessons = [C + f for f in ['l15-reading-an-assessment.json', 'l16-edge-cases-first.json', 'l17-two-in-sixty.json', 'l18-talking-while-coding.json', 'l19-a-live-round.json']]
mine_sets = [C + 'review-4.json', C + 'homework-4.json']
mine_drills = [APP + 'drills/' + n + '.json' for n in ['ci-balanced-run', 'ci-pair-gaps', 'ci-interval-intersections', 'ci-cpp-longest-sum-k', 'ci-cpp-first-missing', 'ci-cpp-insert-interval', 'ci-split-points', 'ci-same-total-pairs', 'ci-cpp-range-sums', 'ci-cpp-sum-pairs']]
mine = set(mine_lessons + mine_sets + mine_drills)


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def text(path):
    return ' '.join(strings(json.load(open(path))))


LIST = re.compile(r'\[(?:\s*-?\d+\s*,){3,}\s*-?\d+\s*\]')
BIG = re.compile(r'(?<![\d.])\d{1,3}(?:,\d{3})+(?![\d])|(?<![\d.])\d{5,}(?![\d])')


def tokens(t):
    out = set()
    for m in LIST.findall(t):
        out.add(re.sub(r'\s+', '', m))
    for m in BIG.findall(t):
        m = m.replace(',', '')
        if re.fullmatch(r'\d{1,2}0*', m):
            continue
        out.add(m)
    return out


others = {}
for p in glob.glob(APP + '**/*.json', recursive=True):
    if p in mine or p.endswith('manifest.json') or '/data/' in p:
        continue
    try:
        others[p] = re.sub(r'\s+', '', text(p)) if False else text(p)
    except Exception:
        pass
other_norm = {p: (re.sub(r'\s+', '', t), t.replace(',', '')) for p, t in others.items()}

hits = 0
for path in sorted(mine):
    t = text(path)
    for tok in sorted(tokens(t)):
        for p, (nospace, nocomma) in other_norm.items():
            if tok.startswith('['):
                if tok in nospace:
                    print('HIT', os.path.basename(path), tok, 'in', p.replace(APP, ''))
                    hits += 1
            else:
                if re.search(r'(?<![\d.])' + re.escape(tok) + r'(?![\d])', nocomma):
                    print('NUM', os.path.basename(path), tok, 'in', p.replace(APP, ''))
                    hits += 1
print('external hits', hits)
# own course: review and homework against lessons
lt = {p: text(p) for p in mine_lessons}
for path in mine_sets:
    t = text(path)
    for tok in sorted(tokens(t)):
        for p, lx in lt.items():
            if tok.startswith('['):
                if tok in re.sub(r'\s+', '', lx):
                    print('OWN HIT', os.path.basename(path), tok, 'in', os.path.basename(p))
            elif re.search(r'(?<![\d.])' + re.escape(tok) + r'(?![\d])', lx.replace(',', '')):
                print('OWN NUM', os.path.basename(path), tok, 'in', os.path.basename(p))
