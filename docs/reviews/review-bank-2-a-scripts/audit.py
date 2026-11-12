"""Structural audit of statistics-1..4 and behavioural-5..8 against docs/briefs/bank-2.md sections 2 to 5.
Prints every difference; the reader decides which are findings. Run from anywhere: python3 audit.py"""
import json, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
BANK = os.path.join(ROOT, 'app', 'content', 'bank')
brief = open(os.path.join(ROOT, 'docs', 'briefs', 'bank-2.md')).read().split('\n')
plan = {}; cur = None
for line in brief:
    m = re.match(r'##### Session (\d): (\w+) ', line)
    if m: cur = (int(m.group(1)), m.group(2)); continue
    if line.startswith('#'): cur = None if not line.startswith('#####') else cur
    if cur and cur[1] in ('statistics', 'behavioural') and line.startswith('| `'):
        c = [x.strip() for x in line.strip('|').split('|')]
        plan[c[0].strip('`')] = dict(file='%s-%d' % (cur[1], cur[0] + (4 if cur[1] == 'behavioural' else 0)), family=c[1].strip('`'), d=int(c[2]), kind=c[3], pace=int(c[4]), roles=c[5], draws=c[6].strip('`'), text=c[7], show=c[8])
ROLE = {'T': 'trader', 'R': 'research', 'S': 'strats', 'D': 'developer'}
allids = collections.Counter()
for f in sorted(os.listdir(BANK)):
    for it in json.load(open(os.path.join(BANK, f)))['items']: allids[it['id']] += 1
skills_ok = set(); lessons = set()
CD = os.path.join(ROOT, 'app', 'content', 'courses')
for c in os.listdir(CD):
    p = os.path.join(CD, c, 'course.json')
    if not os.path.exists(p): continue
    t = open(p).read()
    for s in re.findall(r'"id":\s*"([a-z0-9-]+)"', t): skills_ok.add(s)
    for l in os.listdir(os.path.join(CD, c)):
        if l.endswith('.json'): lessons.add(c + '/' + l[:-5])
n = 0; fam = collections.Counter(); dcount = collections.Counter(); seen = set()
for name in ['statistics-%d' % i for i in (1, 2, 3, 4)] + ['behavioural-%d' % i for i in (5, 6, 7, 8)]:
    d = json.load(open(os.path.join(BANK, name + '.json')))
    if d['id'] != name: print('file id', name, d['id'])
    print(name, len(d['items']), 'items | name:', d['name'], '| description words:', len(d.get('description', '').split()))
    for it in d['items']:
        n += 1; i = it['id']; seen.add(i); p = plan.get(i); w = it['widget']
        fam[(name.split('-')[0], it['tags'][0])] += 1; dcount[(name, it['difficulty'])] += 1
        def diff(what, got, want):
            if got != want: print('  DIFF %s %s: content %r, brief %r' % (i, what, got, want))
        if allids[i] != 1: print('  id not unique in bank:', i)
        if not p: print('  not in brief:', i); continue
        diff('file', name, p['file']); diff('family', it['tags'], [p['family']]); diff('difficulty', it['difficulty'], p['d'])
        diff('kind', w['kind'], p['kind']); diff('pace', it.get('pace'), p['pace'])
        diff('role', sorted(it['role']), sorted(ROLE[x] for x in p['roles'].split(',')))
        diff('requires', it.get('requires'), [p['draws']] if p['d'] >= 4 else None)
        if p['draws'] not in lessons: print('  draws-on lesson missing:', i, p['draws'])
        if it['style'] != name.split('-')[0]: print('  style', i, it['style'])
        if it['source'] != 'Original': print('  source', i, it['source'])
        if w['kind'] == 'choice':
            opts = w['options']; key = [o for o in opts if o.get('correct')]
            others = [len(o['text']) for o in opts if not o.get('correct')]
            if len(opts) != 4 or len(key) != 1: print('  choice shape', i)
            if w.get('shuffle') is False: print('  shuffle off', i)
            if any(not o.get('why') for o in opts if not o.get('correct')): print('  distractor without why', i)
            print('  choice %s: key %d, others %s, key minus longest other %+d' % (i, len(key[0]['text']), others, len(key[0]['text']) - max(others)))
        if w['kind'] == 'numeric':
            if len(w.get('wrong', [])) < 2: print('  fewer than two wrong', i)
            if not w.get('label') or not w.get('accept'): print('  no label or accept', i)
            side = {(x['value'] > w['answer']) for x in w['wrong']}
            if len(side) == 1: print('  note: all wrong values on one side of the key:', i)
        if w['kind'] == 'longform':
            pts = [r['points'] for r in w['rubric']]
            if pts != [2, 2, 2, 2, 1, 1]: print('  rubric points', i, pts)
            words = len(w['model'].split())
            if not 120 <= words <= 180: print('  model words', i, words)
            if not it['question'].startswith('Answer aloud, then type it: '): print('  question line', i, it['question'])
            if it.get('prose'): print('  prose on longform', i)
            for unit, sec in (('two minutes', 120), ('ninety seconds', 90), ('three minutes', 180), ('one minute', 60), ('sixty seconds', 60)):
                if unit in (w['prompt'] + ' ' + ' '.join(r['text'] for r in w['rubric'])).lower() and it['pace'] != sec: print('  pace %d but text says %s: %s' % (it['pace'], unit, i))
        ex = it['explain']['text']
        if len(re.findall(r'[.?](?:\s|$)', re.sub(r'\$[^$]*\$', 'X', ex))) > 3: print('  explanation over three sentences?', i)
        blob = json.dumps(it, ensure_ascii=False)
        for badw, rx in (('em-dash', '—'), ('exclamation', r'!(?!=)'), ('percent', r'\bpercent\b'), ('dollar sign money', r'\\\$\d'), ('US spelling', r'\b(color|center|analyze|behavior|modeling|modeled|favor|labor|program\b(?! ))')):
            if re.search(rx, blob): print('  voice:', badw, i)
for i in plan:
    if i not in seen: print('planned but absent:', i)
print(n, 'items')
print('families:', dict(sorted(fam.items())))
print('difficulty:', dict(sorted(dcount.items())))
