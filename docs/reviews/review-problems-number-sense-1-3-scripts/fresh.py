"""Reuse check (DECISIONS, session AB): key numbers and story nouns of the ten
problems searched across all of app/content, outside the three sets themselves.
Run from the repo root:
python3 docs/reviews/review-problems-number-sense-1-3-scripts/fresh.py
Prints hits to be read by hand; it does not judge."""
import glob
import json
import os
import re

OWN = {f'app/content/courses/number-sense/problems-{n}.json' for n in (1, 2, 3)}

TERMS = {
    'p-garden-beds': [r'garden', r'\bbeds?\b', r'potato', r'\bbeans?\b', r'roses?\b',
                      r'tfrac\{13\}\{20\}', r'tfrac\{7\}\{40\}'],
    'p-rye-loaves': [r'\brye\b', r'loaf|loaves', r'\bbaker', r'flour',
                     r'tfrac\{5\}\{6\} *(\\div|\\times) *\\tfrac\{1\}\{4\}', r'tfrac\{10\}\{3\}'],
    'p-two-printers': [r'printer', r'leaflet', r'tfrac\{17\}\{24\}', r'tfrac\{7\}\{9\}',
                       r'106\\tfrac', r'tfrac\{320\}\{3\}'],
    'p-squash-jugs': [r'squash', r'cordial', r'\bjugs?\b', r'tfrac\{31\}\{48\}', r'tfrac\{31\}\{72\}',
                      r'tfrac\{4\}\{9\}.{0,40}tfrac\{5\}\{12\}'],
    'p-moor-weather': [r'\bmoor\b', r'weather station', r'-3\.6\b', r'-6\.3\b', r'-7\.8\b'],
    'p-golf-card': [r'golf', r'birdie', r'bogey', r'\bpar\b', r'tfrac\{5\}\{18\}', r'0\.2777', r'0\.278\b'],
    'p-taxi-split': [r'\btaxi', r'2\.8333', r'17 *\\div *6', r'1\{,\}698', r'\b2\.85\b'],
    'p-cube-tub': [r'craft', r'wooden cube', r'1\{,\}500\b', r'1\{,\}331', r'1\{,\}728', r'\b169\b'],
    'p-stationery-bill': [r'stationery', r'boxes of paper', r'delivery', r'4\.85\b', r'19\.50?\b',
                          r'203\.8', r'190\.8', r'67\.93'],
    'p-comet-probe': [r'comet', r'\bprobe\b', r'1\.2 *\\times *10\^\{?9', r'4 *\\times *10\^\{?4',
                      r'8\{,\}760|8760', r'30\{,\}000 hours'],
}


def strings(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, path + '.' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, f'{path}[{i}]')


files = [f for f in glob.glob('app/content/**/*.json', recursive=True)
         if f not in OWN and os.path.basename(f) != 'manifest.json']
corpus = []
for f in sorted(files):
    try:
        corpus.append((f, list(strings(json.load(open(f))))))
    except Exception as e:  # noqa: BLE001
        print('unreadable', f, e)
print(len(corpus), 'files searched')

for item, terms in TERMS.items():
    print('\n###', item)
    for t in terms:
        rx = re.compile(t, re.I)
        hits = []
        for f, ss in corpus:
            for p, s in ss:
                m = rx.search(s)
                if m:
                    hits.append((f, p, s[max(0, m.start() - 50):m.end() + 50].replace('\n', ' ')))
        same = [h for h in hits if '/number-sense/' in h[0]]
        print(f'  {t!r}: {len(hits)} hit(s) in {len({h[0] for h in hits})} file(s), {len(same)} in number-sense')
        for f, p, ctx in (same + [h for h in hits if h not in same])[:3]:
            print('      ', f.replace('app/content/', ''), p[:40], '|', ctx)
