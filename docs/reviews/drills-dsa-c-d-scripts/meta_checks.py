"""Voice marks, spelling, index rows, skills, difficulty mix and the time-limit sentence for the 33 drills.
Usage: meta_checks.py <app/content>."""
import glob, json, os, re, sys
ROOT = sys.argv[1]
C = 'route-order shallowest-leaf shared-tail common-manager closest-level swapped-levels nearest-strikes short-codes print-queue window-every-venue total-booked double-booked peak-calls cover-opening shortest-cover'.split()
D = 'lift-buttons spare-cables climb-limit upstream-stations forced-order footpath-slabs stamp-gaps shift-pay feed-passes free-desk-square kiosk-change loop-depots ticker-batches split-prices server-loads'.split()
B3 = 'oncall-rota depth-block range-volumes'.split()
LINE = 'All the tests in a run share one 5-second limit in the browser.'
AMER = r'\b(color|behavior|favor|center|organiz|recogniz|minimiz|maximiz|optimiz|analyz|labeled|traveled|modeled|canceled|program\b|gray|license\b|catalog\b)'
idx = json.load(open(os.path.join(ROOT, 'drills', 'index.json')))
rows = {r['id']: r for r in (idx if isinstance(idx, list) else idx['drills'])}
declared = {}
for c in ('ds', 'algo-think', 'graphs-dp'):
    s = set()
    for f in glob.glob(os.path.join(ROOT, 'courses', c, 'l*.json')):
        s.update(json.load(open(f)).get('skills', []))
    declared[c] = s
for pack, ids in (('C', C), ('D', D), ('B rewrites', B3)):
    mix = {}
    for i in ids:
        d = json.load(open(os.path.join(ROOT, 'drills', 'dsa-' + i + '.json')))
        mix[d['difficulty']] = mix.get(d['difficulty'], 0) + 1
        prose = [d['brief'], d['hint'], d['name']] + d['notes'] + d['constraints'] + [e.get('note', '') for e in d['examples']]
        text = '\n'.join(prose)
        probs = []
        if '!' in re.sub(r'`[^`]*`|!=', '', text): probs.append('exclamation')
        if '—' in text or '–' in text: probs.append('dash')
        m = re.findall(AMER, text, re.I)
        if m: probs.append('spelling ' + ','.join(m))
        lim = [c for c in d['constraints'] if '5-second' in c]
        if not any(LINE in c for c in lim): probs.append('limit line: ' + ' / '.join(lim))
        r = rows.get(d['id'])
        if not r or r['name'] != d['name'] or r['course'] != d['course'] or r['difficulty'] != d['difficulty']: probs.append('index row')
        miss = [s for s in d['skills'] if s not in declared[d['course']]]
        if miss: probs.append('skills not declared ' + ','.join(miss))
        n = len(d['tests'])
        if not re.search(r'Submit runs %d hidden tests' % n, d['how']): probs.append('how count')
        if probs: print(d['id'], '|', '; '.join(probs))
    print(pack, 'difficulty mix', dict(sorted(mix.items())))
