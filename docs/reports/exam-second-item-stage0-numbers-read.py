"""Second read of the exam second items, stage0 (topic-0.3, topic-0.2, topic-0.4).

Run: python3 docs/reports/exam-second-item-stage0-numbers-read.py   (always exits 0; a FINDING line per failing check)

Every key, `wrong` value and printed number of the eight new items is recomputed by a route the author's script
does not use: enumeration, bisection, a grid scan for roots, polynomial multiplication, a keyboard map. The script
also recounts the auto items per skill, the (exam, skill) pairs, the three removals, and recomputes the numbers of
the exact fixes proposed in docs/reviews/review-exam-second-item-stage0.md (lines marked `fix`).
"""
import collections, glob, itertools, json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, '..', '..', 'app', 'content')
n, findings = [0], []


def check(ok, label):
    n[0] += 1
    print(('ok      ' if ok else 'FINDING ') + label)
    if not ok:
        findings.append(label)


def near(a, b, eps=1e-9):
    return abs(a - b) <= eps


def load(path):
    return json.load(open(os.path.join(CONTENT, path), encoding='utf8'))


def is_auto(it):
    lf = lambda w: bool(w) and w.get('kind') == 'longform'
    return not (it.get('kind') == 'longform' or lf(it.get('widget')) or any(lf(p.get('widget')) for p in it.get('parts', [])))


def numeric(where, it, key, wrongs):
    """Key and every wrong value against my figures; bands apart; a byKey line per wrong id."""
    w = it['widget']
    a, t = w['answer'], w['tol']['abs']
    check(abs(a - key) <= max(t, 1e-9), f'{where} key {a} = {key:.6g}')
    got = {x['id']: x for x in w.get('wrong', [])}
    check(set(got) == set(wrongs), f'{where} wrong ids {sorted(got)}')
    for k, v in wrongs.items():
        if k not in got:
            continue
        x = got[k]
        check(abs(x['value'] - v) <= x['tol']['abs'] + 1e-9, f'{where} wrong {k} {x["value"]} = {v:.6g}')
        check(abs(x['value'] - a) > t + x['tol']['abs'], f'{where} wrong {k} outside the key band')
        check(k in it['feedback'].get('byKey', {}), f'{where} wrong {k} has a byKey line')
    for x, y in itertools.combinations(got.values(), 2):
        check(abs(x['value'] - y['value']) > x['tol']['abs'] + y['tol']['abs'], f'{where} wrongs {x["id"]}, {y["id"]} apart')


def bisect(f, lo, hi):
    for _ in range(200):
        mid = (lo + hi) / 2
        if (f(lo) < 0) == (f(mid) < 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def roots_deg(f, step=0.25):
    """Roots of f on [0, 360) in degrees: exact grid zeros and sign changes, refined by bisection."""
    out, k = [], 0
    while k * step < 360:
        x0, x1 = k * step, (k + 1) * step
        if abs(f(x0)) < 1e-12:
            out.append(x0)
        elif abs(f(x1)) > 1e-12 and (f(x0) < 0) != (f(x1) < 0):
            out.append(bisect(f, x0, x1))
        k += 1
    return sorted(round(x, 6) for x in out)


def rad(x):
    return math.radians(x)


# ---------------------------------------------------------------- structure
SPEC = {
    'topic-0.3': dict(items=30, minutes=70, old=(26, 60),
                      new=['e-desk-meetings', 'e-double-angle-roots', 'e-parallelogram-midpoint', 'e-rebate-third', 'e-coefficients-in-step'],
                      removed={'e-sigma-odd': ['seq-sums']},
                      pairs=['ct-comb', 'seq-arith', 'seq-binomial', 'seq-converge', 'tr-equations', 'tr-identities', 'vc-arrows', 'vc-geometry']),
    'topic-0.2': dict(items=30, minutes=75, old=(30, 75), new=['e-read-the-change', 'e-two-rates'],
                      removed={'e-two-roots': ['quad-solve', 'quad-factor'], 'e-formula': ['quad-solve']},
                      pairs=['fn-transform', 'quad-model']),
    'topic-0.4': dict(items=21, minutes=65, old=(20, 60), new=['e-left-hand-commands'], removed={}, pairs=['tm-typing']),
}
EX, IT = {}, {}
for e, sp in SPEC.items():
    doc = load(f'exams/{e}.json')
    EX[e] = doc
    ids = [i['id'] for i in doc['items']]
    IT.update({i['id']: i for i in doc['items']})
    check(len(ids) == sp['items'] and len(set(ids)) == len(ids), f'{e} holds {sp["items"]} items, ids unique')
    check(20 <= len(ids) <= 30, f'{e} within the validator range 20 to 30')
    scaled = sp['old'][1] * sp['items'] / sp['old'][0]
    want = sp['old'][1] if sp['items'] == sp['old'][0] else 5 * math.floor(scaled / 5 + 0.5)
    check(doc['minutes'] == sp['minutes'] == want, f'{e} minutes {doc["minutes"]} = {sp["old"][1]} x {sp["items"]}/{sp["old"][0]} = {scaled:.1f} to the nearest 5')
    cnt = collections.Counter(s for i in doc['items'] if is_auto(i) for s in i['skills'])
    # essentials of each level of the topic: the skills tagged on its review
    ess = collections.defaultdict(set)
    for cj in glob.glob(os.path.join(CONTENT, 'courses', '*', 'course.json')):
        co = json.load(open(cj, encoding='utf8'))
        if str(co.get('topic')) != doc['topic']:
            continue
        for lv in co.get('levels', []):
            rp = os.path.join(os.path.dirname(cj), str(lv.get('review')) + '.json')
            if lv.get('review') and os.path.exists(rp):
                for r in json.load(open(rp, encoding='utf8')).get('items', []):
                    for s in r.get('skills', []):
                        ess[s].add(f'{co["id"]}/L{lv["n"]}')
    check(set(sp['pairs']) <= set(ess), f'{e} every listed pair is an essential skill of a level ({len(ess)} essential skills)')
    for s in sp['pairs']:
        check(cnt[s] >= 2, f'{e} pair {s} now on {cnt[s]} auto items')
    low = sorted(s for s in set(doc['skills']) | set(ess) if cnt[s] < 2)
    check(not low, f'{e} no skill under two auto items (lowest: {sorted(cnt.items(), key=lambda kv: kv[1])[:3]}) {low}')
    for i in sp['new']:
        check(i in ids and is_auto(IT[i]), f'{e} new item {i} present and auto')
        check(all(s in doc['skills'] for s in IT[i]['skills']), f'{e} {i} skills are exam skills')
    for rid, sk in sp['removed'].items():
        check(rid not in ids, f'{e} removed {rid} is gone')
        for s in sk:
            check(cnt[s] >= 2, f'{e} removed {rid}: {s} keeps {cnt[s]} auto items')

# ---------------------------------------------------------------- topic-0.3 e-desk-meetings (ct-comb)
it = IT['e-desk-meetings']
pts = range(10)
tri = {frozenset(c) for c in itertools.permutations(pts, 3)}
numeric('desk-meetings', it, len(tri), {'ordered': len(list(itertools.permutations(pts, 3))),
                                        'third': len(list(itertools.permutations(pts, 3))) // 3, 'pairs': len(list(itertools.combinations(pts, 2)))})
check('Ten points' in it['prose'] and '120' in it['explain']['text'] and '720' in it['explain']['text'], 'desk-meetings prints ten points, 120 and 720')
p5 = load('courses/counting/problems-1.json')['items'][2]
check('triangle' not in p5['prose'] and 'triangle' not in json.dumps(load('courses/counting/l4-choosing-without-order.json')),
      'desk-meetings REUSE: fixed, the triangle count of 10 points shares no story with p-five-a-side (8 teams, 28) or the counting lessons')
check(len(tri) == 120 and len(list(itertools.permutations(pts, 3))) == 720 and 720 // 3 == 240 and len(list(itertools.combinations(pts, 2))) == 45,
      'fix desk-meetings: 10 points on a circle give 120 triangles; slips 720 ordered, 240 divided by 3, 45 pairs')

# ---------------------------------------------------------------- topic-0.3 e-rebate-third (seq-converge, seq-geom)
it = IT['e-rebate-third']
r = bisect(lambda q: 18 / (1 - q) - 30, 0.0, 0.99)
terms = [18 * r ** k for k in range(400)]
check(near(sum(terms), 30, 1e-6), f'rebate-third ratio {r:.6f} sums to 30 over 400 months')
numeric('rebate-third', it, terms[2], {'ratio-flip': 18 * (18 / 30) ** 2, 'second': terms[1], 'tail': sum(terms[2:])})
check(near(sum(terms[2:]), 30 - 18 - 7.2, 1e-6), 'rebate-third tail = 30 less 18 less 7.20 = 4.80')
check(near(r, 0.4, 1e-9) and near(1 - r, 0.6, 1e-9), 'rebate-third prints r = 0.4 and 1 - r = 0.6')

# ---------------------------------------------------------------- topic-0.3 e-double-angle-roots (tr-identities, tr-equations)
it = IT['e-double-angle-roots']
f = lambda x: math.sin(rad(2 * x)) - math.sqrt(3) * math.cos(rad(x))
roots = roots_deg(f)
check(sorted(it['widget']['answers']) == [round(x) for x in roots] and all(near(x, round(x), 1e-5) for x in roots),
      f'double-angle-roots answers {it["widget"]["answers"]} = grid roots {roots}')
check(it['widget'].get('unordered') is True, 'double-angle-roots set is unordered')
for wv in it['widget']['wrong']:
    vals = [float(v) for v in wv['value'].split(',')]
    check(sorted(vals) != sorted(it['widget']['answers']) and any(abs(f(v)) > 1e-6 for v in vals) and wv['id'] in it['feedback']['byKey'],
          f'double-angle-roots wrong {wv["id"]} {vals} is not the solution set and has a line')
check(sorted([90, 270] + [60, 360 - 60]) == [60, 90, 270, 300] and sorted([90, 270, 30, 330]) == [30, 90, 270, 330], 'double-angle-roots slips are the two printed sets')
check(len([x for x in roots if abs(math.cos(rad(x))) > 1e-9]) == 2 and 'count' in it['feedback']['byKey'], 'double-angle-roots dividing by cos x leaves 2 roots (count line)')
# strict two-skill test: sqrt(3) cos x against sin 2x has no equal-angle pairing, so the identity is needed.
check(not any(abs(math.sin(rad(2 * x)) - math.sin(rad(x))) < 1e-9 for x in (90, 120, 270)),
      'double-angle-roots TWO-SKILL: fixed, the roots 60, 90, 120, 270 do not come from equal sines, so the double-angle identity is needed')
check([round(x) for x in roots] == [60, 90, 120, 270] and all(abs(f(v)) > 1e-3 for v in (300, 30, 330)),
      'fix double-angle-roots: sin 2x = sqrt(3) cos x has roots 60, 90, 120, 270; 300, 30 and 330 are not roots')

# ---------------------------------------------------------------- topic-0.3 e-parallelogram-midpoint (vc-arrows, vc-geometry)
it = IT['e-parallelogram-midpoint']


def par(a, c):
    A, C = complex(*a), complex(*c)
    B = A + C                      # AB equals OC
    M = (B + C) / 2
    Bm = A - C
    return dict(key=abs(M - A), bminus=abs((Bm + C) / 2 - A), om=abs(M), sq=abs(M - A) ** 2, B=B, M=M, AM=M - A)


p = par((-4, 2), (3, 5))
numeric('parallelogram-midpoint', it, p['key'], {'b-minus': p['bminus'], 'om': p['om'], 'no-root': p['sq']})
check(p['B'] == complex(-1, 7) and p['M'] == complex(1, 6) and p['AM'] == complex(5, 4) and near(p['sq'], 41), 'parallelogram-midpoint prints B (-1, 7), M (1, 6), AM (5, 4), 41')
check(near(math.dist((-4, 2), (1, 6)), 6.403124, 1e-6) and abs(6.40 - p['key']) <= 0.005, 'parallelogram-midpoint band takes the printed 6.40')
l10 = json.dumps(load('courses/counting/l10-adding-arrows.json')['screens'][5:7])
check('(-4, 2)' not in l10 and 'pmatrix}-4' not in l10.replace(' ', '') and '[-4, 6]' in l10,
      'parallelogram-midpoint REUSE: fixed, (-4, 2) and (3, 5) are not the pair of counting/l10-adding-arrows')
check(round(p['key'], 6) == 6.403124 and round(p['bminus'], 2) == 2.24 and round(p['om'], 2) == 6.08 and near(p['om'] ** 2, 37) and near(p['bminus'] ** 2, 5),
      f'fix parallelogram-midpoint: (-4, 2), (3, 5) give length {p["key"]:.6f}; slips 2.24, 6.08, 41')

# ---------------------------------------------------------------- topic-0.3 e-coefficients-in-step (seq-arith, seq-binomial)
it = IT['e-coefficients-in-step']


def row(m):
    c = [1]
    for _ in range(m):
        c = [x + y for x, y in zip([0] + c, c + [0])]      # multiply by (1 + x)
    return c + [0, 0, 0]


step = [m for m in range(1, 200) if row(m)[2] - row(m)[1] == row(m)[3] - row(m)[2]]
numeric('coefficients-in-step', it, [m for m in step if m > 2][0], {'small-root': [m for m in step if m <= 2][0]})
check(step == [2, 7], f'coefficients-in-step: n with coefficients in step, 1 to 199: {step}')
check(row(7)[1:4] == [7, 21, 35] and 21 - 7 == 14 == 35 - 21 and row(2)[3] == 0, 'coefficients-in-step prints 7, 21, 35, step 14; (1 + x)^2 has no x^3 term')
check(all(m * m - 9 * m + 14 == 0 for m in step) and (7 - 2) * (7 - 7) == 0, 'coefficients-in-step n^2 - 9n + 14 = (n - 2)(n - 7)')

# ---------------------------------------------------------------- topic-0.2 e-read-the-change (fn-transform)
it = IT['e-read-the-change']
fn = {x['id']: x for x in it['canvas']['params']['functions']}
ev = lambda expr, x: eval(expr.replace('^', '**'), {'x': x})
f0 = lambda x: ev(fn['f']['expr'], x)
g0 = lambda x: ev(fn['g']['expr'], x)
rules = {'a': lambda x: 2 * f0(x - 2), 'b': lambda x: 2 * f0(x + 2), 'c': lambda x: f0(x - 2) - 1, 'd': lambda x: f0(2 * (x - 2))}
grid = [k / 8 for k in range(-24, 41)]
match = [k for k, h in rules.items() if all(near(h(x), g0(x)) for x in grid)]
correct = [o['id'] for o in it['widget']['options'] if o.get('correct')]
check(match == correct == ['a'], f'read-the-change only rule {match} draws the dashed curve; marked {correct}')
check(all(near(f0(x), x * x - 1) for x in grid), 'read-the-change solid curve is x^2 - 1')
lo = min(grid, key=g0)
check((lo, g0(lo)) == (2, -2) and near(g0(1), 0) and near(g0(3), 0), 'read-the-change dashed curve: lowest point (2, -2), crosses at 1 and 3')
lc = min(grid, key=rules['c'])
check((lc, rules['c'](lc)) == (2, -2) and near(rules['c'](2 + math.sqrt(2)), 0) and near(rules['c'](2 - math.sqrt(2)), 0), 'read-the-change option c: same lowest point, roots 2 +- sqrt 2')
check(min(rules['d'](x) for x in grid) == -1 and min(grid, key=rules['b']) == -2, 'read-the-change option d lowest height -1; option b sits at x = -2')
py = it['canvas']['params']['y']
for k in ('f', 'g'):
    d0, d1 = fn[k]['domain']
    h = f0 if k == 'f' else g0
    check(py[0] <= min(h(d0 + (d1 - d0) * j / 200) for j in range(201)) and max(h(d0), h(d1)) <= py[1], f'read-the-change curve {k} stays inside the y window')

# ---------------------------------------------------------------- topic-0.2 e-two-rates (quad-model, quad-solve)
it = IT['e-two-rates']
grow = lambda r: 25000 * (1 + r) * (1 + 2 * r) - 31320
r1, r2 = bisect(grow, 0, 1), bisect(grow, -3, -1)
numeric('two-rates', it, r1, {'simple': (31320 / 25000 - 1) / 3, 'one-rate': bisect(lambda r: 25000 * (1 + r) ** 2 - 31320, 0, 1), 'other-root': r2})
check(it['widget'].get('unit') == '%' and it['widget'].get('over100') is True, 'two-rates carries unit % and over100')
check(near(25000 * 1.08 * 1.16, 31320, 1e-6) and near(3 * 3 + 4 * 2 * 0.2528, 11.0224) and near(3.32 ** 2, 11.0224), 'two-rates prints 8% then 16%, discriminant 11.0224, root 3.32')
check(near(r2, -1.58, 1e-9) and near(2 * r1 * r1 + 3 * r1 - 0.2528, 0), 'two-rates other root -1.58; 2r^2 + 3r - 0.2528 = 0 at r = 0.08')
hw = load('courses/quadratics/homework-2.json')['items'][3]
check('5,618' not in it['prose'] and '1.06' not in it['explain']['text'] and '25,000' in it['prose'],
      'two-rates REUSE: fixed, 25,000 to 31,320 at 8% is not the 6% of quadratics/homework-2 hw2-return')
grow8 = lambda r: 25000 * (1 + r) * (1 + 2 * r) - 31320
check(near(bisect(grow8, 0, 1), 0.08) and near(bisect(grow8, -3, -1), -1.58) and near(9 + 8 * 0.2528, 11.0224) and near(3.32 ** 2, 11.0224)
      and round((31320 / 25000 - 1) / 3, 4) == 0.0843 and round(math.sqrt(31320 / 25000) - 1, 4) == 0.1193 and near(25000 * 1.08 * 1.16, 31320, 1e-6),
      'fix two-rates: 25,000 to 31,320 gives 8% (then 16%); 2r^2 + 3r - 0.2528 = 0, discriminant 11.0224, root 3.32; slips 8.43%, 11.93%, -158%')

# ---------------------------------------------------------------- topic-0.4 e-left-hand-commands (tm-typing)
it = IT['e-left-hand-commands']
ROWS = ['qwertyuiop', 'asdfghjkl;', 'zxcvbnm,./']
left = {ch for row_ in ROWS for ch in row_[:5]}          # five columns, Q A Z across to T G B
opts = {o['id']: bool(o.get('correct')) for o in it['widget']['options']}
mine = {w: set(w) <= left for w in opts}
check(mine == opts, f'left-hand-commands marked {sorted(k for k, v in opts.items() if v)} = keyboard map {sorted(k for k, v in mine.items() if v)}')
check(sum(opts.values()) == 3 and len(opts) == 6, 'left-hand-commands three of six')
check([sorted(set(w) - left) for w in ('grep', 'head', 'cut')] == [['p'], ['h'], ['u']], 'left-hand-commands right-hand keys: P, H, U, one each')
col = lambda ch: next(r.index(ch) for r in ROWS if ch in r)
check(col('h') == col('y') == col('n') == 5 and col('u') == col('j') == 6 and col('p') == col(';') == 9 and col('t') == col('g') == col('b') == 4,
      'left-hand-commands columns: Y H N, U above J, P above the semicolon, T G B')

print(f'{n[0] - len(findings)} of {n[0]} checks passed, {len(findings)} FINDING')
