"""Tries the Fluency fixes of review-holes-1.6-2.1.md on copies of the sets (never the content files): patches a copy in
<out dir>, draws 200 of the patched family with fluency-sample.mjs --file, and checks the new entry or band.
   python3 docs/reviews/review-holes-1.6-2.1-scripts/try-fixes.py <out dir>      (from the repo root)"""
import json
import os
import subprocess
import sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bad = 0


def patched(set_path, fam, edit):
    d = json.load(open(set_path))
    f = next(x for x in d['families'] if x['id'] == fam)
    edit(f)
    p = os.path.join(out, os.path.basename(set_path).replace('.json', f'--{fam}.json'))
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2)
    r = subprocess.run(['node', 'app/tools/fluency-sample.mjs', '--file', p, '--family', fam, '--seed', '9101', '--n', '200', '--json'], capture_output=True, text=True)
    if r.returncode:
        print('DRAW FAILED', fam, r.stderr[-400:])
        return []
    return json.loads(r.stdout)['items']


def pct(expr, line):
    def edit(f):
        f['wrong'].append({'id': 'percent-sign', 'value': '{' + expr + '}', 'tol': f['widget']['tol'], 'line': line})
    return edit


def check_pct(items, fam):
    global bad
    n = 0
    for it in items:
        w = [x for x in it['wrong'] if x['id'] == 'percent-sign']
        if not w or abs(w[0]['value'] - it['answer'] / 100) > 1e-12:
            bad += 1
            continue
        tol = it['tol']['abs']
        clash = [x['id'] for x in it['wrong'] if x['id'] != 'percent-sign' and abs(x['value'] - w[0]['value']) <= 2 * tol]
        if clash or abs(w[0]['value'] - it['answer']) <= 2 * tol:
            bad += 1
            print('clash', fam, it['prompt'], clash)
        n += 1
    print(f'{fam}: percent-sign entry present and clear of the answer and the other entries in {n} of {len(items)} draws; distinct prompts {len({i["prompt"] for i in items})}')


SL16 = 'app/content/courses/stat-learning/fluency-l16-groups-nobody-labelled.json'
T15 = 'app/content/courses/testing/fluency-l15-sharpness-of-the-peak.json'
T17 = 'app/content/courses/testing/fluency-l17-ratio-of-likelihoods.json'
T18 = 'app/content/courses/testing/fluency-l18-counts-against-expectations.json'
SL18 = 'app/content/courses/stat-learning/fluency-l18-bending-the-line.json'

key_au = next(x for x in json.load(open(SL16))['families'] if x['id'] == 'assign-and-update')['let']['key']
check_pct(patched(SL16, 'assign-and-update', pct(f'({key_au})/100', 'Type the number alone, with no % sign after it.')), 'assign-and-update')
check_pct(patched(T15, 'volatility-se', pct('sig/sqrt(2*n)/100', 'Type the number alone. The answer is already in percentage points, so a % sign divides it by 100.')), 'volatility-se')


def band(prompt_old, prompt_new, tol, acc):
    def edit(f):
        assert prompt_old in f['prompt'], f['prompt']
        f['prompt'] = f['prompt'].replace(prompt_old, prompt_new)
        f['widget']['tol'] = {'abs': tol}
        f['widget']['accept'] = acc
        for w in f['wrong']:
            w['tol'] = {'abs': tol}
    return edit


for path, fam, old, new, tol, acc in (
        (T17, 'poisson-ratio-test', 'Give 3 decimal places.', 'Give 2 decimal places.', 0.05, '${key:dp2}$, within 0.05'),
        (T18, 'two-by-two', 'Give 3 decimal places.', 'Give 2 decimal places.', 0.05, '${key:dp2}$, within 0.05')):
    items = patched(path, fam, band(old, new, tol, acc))
    clash = 0
    for it in items:
        for w in it['wrong']:
            if abs(w['value'] - it['answer']) <= 2 * tol:
                clash += 1
    for a in range(len(items)):
        pass
    print(f'{fam}: band {tol}: {len(items)} draws, wrong entries inside twice the band of the answer: {clash}; smallest gap {min(abs(w["value"] - it["answer"]) for it in items for w in it["wrong"]):.4f}')
    bad += clash


def reword(f):
    assert 'has slope {b} on $x$, knots at' in f['prompt']
    f['prompt'] = f['prompt'].replace('has slope {b} on $x$, knots at', 'has slope {b} left of its first knot, knots at')


items = patched(SL18, 'slope-in-a-region', reword)
print('slope-in-a-region reworded, e.g.:', items[0]['prompt'] if items else None)
print('try-fixes:', 'all pass' if not bad else f'{bad} problems')
sys.exit(1 if bad else 0)
