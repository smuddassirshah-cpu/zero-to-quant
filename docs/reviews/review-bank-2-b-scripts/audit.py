"""Structural audit of the eight files: counts against sections 2 and 3 of the brief, fields, requires, key lengths, pace, voice.
Prints findings; exit 0 always (it is a reading aid)."""
import json, os, re, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
FIN = {'fi-interest': '1/1/1/1', 'fi-bonds': '1/1/2/1', 'fi-equity': '1/0/0/1', 'fi-forwards': '1/2/2/1', 'op-payoff': '0/0/1/0', 'op-strategies': '1/2/1/1',
       'op-parity': '1/1/1/1', 'op-greeks': '1/0/1/1', 'ms-book': '1/1/1/1', 'ms-orders': '1/0/0/1', 'ms-costs': '1/1/1/1', 'ms-mm': '0/1/0/0',
       'tp-riskneutral': '1/0/1/0', 'tp-multistep': '1/1/1/1', 'tp-bs': '0/0/2/1', 'gv-risk': '1/1/0/0', 'greek-signs': '1/0/0/0', 'option-estimate': '1/0/0/1',
       'gamma-pnl': '0/1/0/1', 'digital-option': '0/1/0/1', 'exotic-ranking': '0/1/0/0'}
COD = {'pf-types': '3/0/0/0', 'pf-functions': '2/1/0/0', 'pf-collections': '0/2/0/0', 'pf-idioms': '0/2/2/1', 'pf-classes': '0/0/0/1', 'at-complexity': '1/0/0/0',
       'at-recursion': '0/1/1/0', 'at-search': '0/0/2/1', 'at-sort': '0/0/1/0', 'at-greedy': '0/0/1/0', 'ds-arrays': '1/1/0/1', 'ds-hashing': '1/1/0/0',
       'ds-pointers': '0/1/0/1', 'ds-stacks': '0/0/1/0', 'ds-trees': '0/0/0/1', 'gd-dp': '0/1/1/1', 'gd-traversal': '0/0/0/1', 'np-broadcast': '0/0/1/0',
       'edge-case-list': '1/1/0/1', 'integer-division': '2/0/0/0', 'complexity-read': '1/0/0/0', 'simulation-rules': '0/0/1/1', 'bit-lowest': '0/0/0/1',
       'copy-vs-move': '0/1/0/0', 'virtual-dispatch': '0/0/1/0', 'defined-vs-undefined': '0/0/0/1'}
skills = {}
lessons = set()
for c in os.listdir(os.path.join(ROOT, 'courses')):
    p = os.path.join(ROOT, 'courses', c, 'course.json')
    if os.path.exists(p):
        cj = json.load(open(p))
        for s in (cj.get('skills') or {}):
            skills[s] = c
        for lv in cj.get('levels', []):
            for l in lv.get('lessons', []):
                lessons.add(f"{c}/{l if isinstance(l, str) else l.get('id')}")
allids = collections.Counter()
for f in os.listdir(os.path.join(ROOT, 'bank')):
    for it in json.load(open(os.path.join(ROOT, 'bank', f)))['items']:
        allids[it['id']] += 1
print('duplicate ids across the bank:', [k for k, v in allids.items() if v > 1])

for fam, table, per in (('finance', FIN, 15), ('coding', COD, 12)):
    got = collections.defaultdict(lambda: [0, 0, 0, 0])
    kinds = collections.Counter()
    diffs = collections.Counter()
    longest = 0
    nchoice = 0
    for n in (1, 2, 3, 4):
        d = json.load(open(os.path.join(ROOT, 'bank', f'{fam}-{n}.json')))
        if d['id'] != f'{fam}-{n}' or len(d['items']) != per:
            print('FILE', fam, n, d['id'], len(d['items']))
        for it in d['items']:
            iid = it['id']
            w = it['widget']
            t = it['tags']
            got[t[0]][n - 1] += 1
            kinds[(n, w['kind'])] += 1
            diffs[(n, it['difficulty'])] += 1
            if len(t) != 1:
                print(iid, 'tags', t)
            if not iid.startswith(t[0] + '-'):
                print(iid, 'id does not start with its family', t[0])
            if it['style'] != fam or it['source'] != 'Original':
                print(iid, 'style/source', it['style'], it['source'])
            for s in it.get('skills', []):
                if s not in skills:
                    print(iid, 'unknown skill', s)
            if t[0] in skills and t[0] not in it.get('skills', []):
                print(iid, 'family is a skill id but is not in skills', it.get('skills'))
            req = it.get('requires')
            if it['difficulty'] >= 4 and not req:
                print(iid, 'difficulty', it['difficulty'], 'without requires')
            if it['difficulty'] < 4 and req:
                print(iid, 'difficulty', it['difficulty'], 'with requires', req)
            for r in req or []:
                if r not in lessons:
                    print(iid, 'requires unknown lesson', r)
            if w['kind'] == 'choice':
                nchoice += 1
                o = w['options']
                key = [x for x in o if x.get('correct')]
                others = [len(x['text']) for x in o if not x.get('correct')]
                if len(o) != 4 or len(key) != 1 or w.get('shuffle') is False:
                    print(iid, 'choice shape', len(o), len(key), w.get('shuffle'))
                kl = len(key[0]['text'])
                if kl > max(others):
                    longest += 1
                    print(f'  key longest: {iid} by {kl - max(others)} ({kl} against {sorted(others)})')
                if kl < min(others):
                    print(f'  key shortest: {iid} by {min(others) - kl}')
                for x in o:
                    if not x.get('correct') and not x.get('why', '').startswith('You '):
                        print(iid, 'why does not open with You:', x.get('why', '')[:60])
            if w['kind'] == 'numeric':
                wr = w.get('wrong', [])
                if len(wr) < 2:
                    print(iid, 'fewer than two wrong entries')
                side = {x['value'] > w['answer'] for x in wr}
                if len(side) == 1:
                    print(f'  one-sided wrongs: {iid} (all {"above" if True in side else "below"} the key {w["answer"]})')
                for x in wr:
                    line = it['feedback'].get('byKey', {}).get(x['id'], '')
                    if not line.startswith('You '):
                        print(iid, 'byKey does not open with You:', x['id'], line[:50])
                if not w.get('label') or not w.get('accept'):
                    print(iid, 'no label or accept')
            if w['kind'] == 'code':
                if not (240 <= it['pace'] <= 480):
                    print(iid, 'code pace', it['pace'])
                if not (6 <= len(w['tests']) <= 10) or len(w['examples']) != 2:
                    print(iid, 'tests', len(w['tests']), 'examples', len(w['examples']))
                m = re.search(r'runs (\d+) hidden', w.get('how', ''))
                if not m or int(m.group(1)) != len(w['tests']):
                    print(iid, 'how line count', w.get('how'), 'against', len(w['tests']))
                if w['starter'].strip().split('\n')[-1].strip() != '...':
                    print(iid, 'starter', repr(w['starter']))
            blob = json.dumps(it, ensure_ascii=False)
            for pat, nm in ((r'!(?!=)', 'exclamation'), ('—', 'em-dash'), (r'\bpercent\b', 'percent'), (r'\$\d+(?:\.\d+)? (?:dollars|a share|per)', 'dollar sign'),
                            (r'\b(color|center|analyze|favor|behavior|modeling|canceled)\b', 'American spelling')):
                txt = re.sub(r'"(starter|solution|call|expect)": "(?:[^"\\]|\\.)*"', '', blob)
                txt = re.sub(r'```.*?```', '', txt, flags=re.S)
                txt = re.sub(r'`[^`]*`', '', txt)
                if re.search(pat, txt):
                    print(iid, 'voice:', nm, re.search(pat, txt).group(0))
            sents = len(re.findall(r'[.?](?:\s|$)', re.sub(r'\$[^$]*\$', 'X', re.sub(r'`[^`]*`', 'X', it['explain']['text']))))
            if sents > 3:
                print(iid, 'explain sentences', sents)
    for k in sorted(set(table) | set(got)):
        g = '/'.join(map(str, got.get(k, [0, 0, 0, 0])))
        if table.get(k) != g:
            print('FAMILY', k, 'brief', table.get(k), 'files', g)
    print(fam, 'kinds', dict(sorted(kinds.items())))
    print(fam, 'difficulty', dict(sorted(diffs.items())))
    print(fam, f'choice items {nchoice}, key strictly longest in {longest}')
