#!/usr/bin/env python3
"""Delta read AG: stat-models problems-3, p-hedge-ranks (re-authored on n = 14).

Recomputes every key, every wrong value and every printed number of the four
parts by a second method (own ranking, full listing of the 2^14 sign patterns,
erfc and a Simpson integral for the normal tail). Exits 0; prints a FINDING
line per failing check.
"""
import glob
import itertools
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
CONTENT = os.path.join(ROOT, 'app', 'content')
COURSE = os.path.join(CONTENT, 'courses', 'stat-models')
SET = os.path.join(COURSE, 'problems-3.json')

checks = 0
findings = 0


def check(name, ok, detail=''):
    global checks, findings
    checks += 1
    if not ok:
        findings += 1
        print(f'FINDING {findings}: {name} {detail}')


def close(a, b, eps=1e-9):
    return abs(a - b) <= eps


def in_band(x, centre, tol):
    return abs(x - centre) <= tol + 1e-12


problem = next(p for p in json.load(open(SET))['items'] if p['id'] == 'p-hedge-ranks')
parts = problem['parts']
check('four parts', len(parts) == 4)
check('skill sm-nonpar', problem['skills'] == ['sm-nonpar'])

# ---- data from the prose itself
prose = problem['prose']
after = prose.split('in bps, was', 1)[1].split('The desk ranks', 1)[0]
d = [float(x.replace('$', '')) for x in re.findall(r'\$?-?\d+\.\d+\$?', after)]
n = len(d)
check('14 values in the prose', n == 14, str(n))
check('prose says 14 months and 14 sizes', 'Over 14 months' in prose and 'the 14 sizes' in prose)
check('no zero difference', all(x != 0 for x in d))
pos = [x for x in d if x > 0]
neg = [x for x in d if x < 0]
check('two positive months, twelve negative', len(pos) == 2 and len(neg) == 12)
check('positives are 1.1 and 1.9', sorted(pos) == [1.1, 1.9])

# ---- ranks by counting (not rankdata): rank = #smaller + (#equal + 1) / 2
sizes = [abs(x) for x in d]


def rank_of(v, pool):
    less = sum(1 for s in pool if s < v - 1e-12)
    eq = sum(1 for s in pool if abs(s - v) < 1e-12)
    return less + (eq + 1) / 2


ranks = [rank_of(s, sizes) for s in sizes]
check('rank total 105', close(sum(ranks), 105))
w_plus = sum(r for r, x in zip(ranks, d) if x > 0)
w_minus = sum(r for r, x in zip(ranks, d) if x < 0)
check('W+ = 12.5', close(w_plus, 12.5), str(w_plus))
check('W- = 92.5', close(w_minus, 92.5), str(w_minus))
srt = sorted(sizes)
check('sorted head as the explain prints', srt[:8] == [0.3, 0.6, 0.8, 1.1, 1.1, 1.4, 1.7, 1.9] and srt[-1] == 4.4, str(srt))
ties = {s for s in sizes if sizes.count(s) > 1}
check('one tie only, the pair at 1.1', ties == {1.1} and sizes.count(1.1) == 2)
check('tie fills places 4 and 5', srt.index(1.1) + 1 == 4 and srt[4] == 1.1)
check('tie is one positive, one negative month', 1.1 in d and -1.1 in d)
check('1.9 ranks 8', close(rank_of(1.9, sizes), 8))
check('tie-low slip 4 + 8 = 12, tie-high 5 + 8 = 13', 4 + 8 == 12 and 5 + 8 == 13)

# ---- null distribution by listing all 2^14 sign patterns
N_PAT = 2 ** n
check('16,384 patterns', N_PAT == 16384)


def moments(rk):
    tot = 0.0
    tot2 = 0.0
    for signs in itertools.product((0, 1), repeat=len(rk)):
        w = sum(r for r, s in zip(rk, signs) if s)
        tot += w
        tot2 += w * w
    m = tot / 2 ** len(rk)
    return m, tot2 / 2 ** len(rk) - m * m


m0, v0 = moments(list(range(1, n + 1)))
check('untied mean 52.5 by listing', close(m0, 52.5, 1e-9))
check('untied variance 253.75 by listing', close(v0, 253.75, 1e-6), str(v0))
check('formula n(n+1)/4', close(n * (n + 1) / 4, 52.5))
check('formula n(n+1)(2n+1)/24', close(n * (n + 1) * (2 * n + 1) / 24, 253.75))
check('14 x 15 x 29 / 24', close(14 * 15 * 29 / 24, 253.75))
ssq = sum(r * r for r in range(1, n + 1))
check('sum of squared ranks 1015', ssq == 1015)
check('1015 / 4 = 253.75', close(ssq / 4, 253.75))
sd = math.sqrt(253.75)
check('SD 15.9295', round(sd, 4) == 15.9295, str(sd))
check('six-divisor sqrt(1015) = 31.8591', round(math.sqrt(1015), 4) == 31.8591)
check('six-divisor is n(n+1)(2n+1)/6', close(n * (n + 1) * (2 * n + 1) / 6, 1015))

# with the tie: variance and exact p
m1, v1 = moments(ranks)
check('tied mean still 52.5', close(m1, 52.5, 1e-9))
check('tied variance 253.625 (= 253.75 - 6/48)', close(v1, 253.625, 1e-6), str(v1))
count = 0
for signs in itertools.product((0, 1), repeat=n):
    w = sum(r for r, s in zip(ranks, signs) if s)
    if w <= 12.5 + 1e-9:
        count += 1
exact_p = count / N_PAT
check('exact one-sided p is 73 of 16,384', count == 73, str(count))
check('exact p under 1%', exact_p < 0.01)

# ---- z
z = (12.5 - 52.5) / 15.9295
z_full = (w_plus - m0) / sd
check('z printed working rounds to -2.511', round(z, 3) == -2.511, str(z))
check('z full precision rounds to -2.511', round(z_full, 3) == -2.511)
z_w_minus = (92.5 - 52.5) / 15.9295
z_var = (12.5 - 52.5) / 253.75
z_noc = 12.5 / 15.9295
check('w-minus slip 2.511', round(z_w_minus, 3) == 2.511)
check('variance slip -0.158', round(z_var, 3) == -0.158, str(z_var))
check('no-centre slip 0.785', round(z_noc, 3) == 0.785, str(z_noc))
check('gap of -40', close(12.5 - 52.5, -40))
z_tie = (12.5 - 52.5) / math.sqrt(v1)


# ---- normal tail, two ways
def phi_erfc(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))


def phi_simpson(x, steps=20000):
    h = x / steps
    s = 0.0
    for i in range(steps + 1):
        t = i * h
        f = math.exp(-t * t / 2)
        s += f if i in (0, steps) else (4 * f if i % 2 else 2 * f)
    return 0.5 + s * h / 3 / math.sqrt(2 * math.pi)


phi = phi_erfc(2.511)
check('Phi by erfc and by Simpson agree', close(phi, phi_simpson(2.511), 1e-10))
check('told Phi(2.511) = 0.99398', round(phi, 5) == 0.99398, str(phi))
p_told = 1 - 0.99398
check('1 - 0.99398 = 0.00602', close(p_told, 0.00602, 1e-12))
check('p rounds to 0.0060', f'{p_told:.4f}' == '0.0060')
check('two tails 0.01204 -> 0.0120', f'{2 * p_told:.4f}' == '0.0120')
check('upper 0.99398 -> 0.9940', f'{0.99398:.4f}' == '0.9940')
p_tie = phi_erfc(z_tie)
check('tie-corrected normal p within 0.0001 of the key ("ignoring the tie" is fair)', abs(p_tie - p_told) < 1e-4, str(p_tie))
check('normal p is the cautious side of the exact p', exact_p < p_told)

# ---- keys, bands, slips
W = [p['widget'] for p in parts]


def wrong(i, wid):
    return next(w for w in W[i]['wrong'] if w['id'] == wid)


expected = [
    (12.5, 0.01, {'tie-low': 12, 'tie-high': 13, 'w-minus': 92.5}),
    (sd, 0.0001, {'variance': 253.75, 'six-divisor': math.sqrt(1015)}),
    (z_full, 0.001, {'w-minus': -z_full, 'variance': z_var, 'no-centre': z_noc}),
    (phi_erfc(z_full), 0.0001, {'two-sided': 2 * p_told, 'upper': 0.99398}),
]
printed_working = [
    [12.5, 4.5 + 8],
    [15.9295, round(sd, 4), sd],
    [z, -2.511, z_full, z_tie],
    [p_told, 0.0060, phi_erfc(-2.511), phi_erfc(-2.51), phi_erfc(z_full), p_tie],
]
places = [1, 4, 3, 4]
for i, (key, tol, slips) in enumerate(expected):
    w = W[i]
    check(f'part {i + 1} numeric', w['kind'] == 'numeric')
    check(f'part {i + 1} key', abs(w['answer'] - key) < 2e-6, f"{w['answer']} vs {key}")
    check(f'part {i + 1} tolerance', close(w['tol']['abs'], tol))
    check(f'part {i + 1} slip ids', {x['id'] for x in w['wrong']} == set(slips))
    for v in printed_working[i]:
        check(f'part {i + 1} key band takes {v:.6f}', in_band(v, w['answer'], w['tol']['abs']))
    unit = 10 ** -places[i]
    frac = abs(w['answer']) / unit % 1
    check(f'part {i + 1} key off a rounding tie', abs(frac - 0.5) > 0.01, str(frac))
    for wid, val in slips.items():
        e = wrong(i, wid)
        check(f'part {i + 1} slip {wid} value', abs(e['value'] - val) <= e['tol']['abs'], f"{e['value']} vs {val}")
        check(f'part {i + 1} slip {wid} band takes its recomputed value', in_band(val, e['value'], e['tol']['abs']))
        check(f'part {i + 1} slip {wid} refused by the key', not in_band(e['value'], w['answer'], w['tol']['abs']))
        check(f'part {i + 1} slip {wid} band clear of the key band',
              abs(e['value'] - w['answer']) > e['tol']['abs'] + w['tol']['abs'])
        if i > 0:
            frac = abs(val) / unit % 1
            check(f'part {i + 1} slip {wid} off a rounding tie', abs(frac - 0.5) > 0.01, str(frac))
    vals = [x['value'] for x in w['wrong']]
    for a, b in itertools.combinations(w['wrong'], 2):
        check(f'part {i + 1} slips {a["id"]}, {b["id"]} apart', abs(a['value'] - b['value']) > a['tol']['abs'] + b['tol']['abs'])
    check(f'part {i + 1} no unit (not a percentage)', not w.get('unit'))

# a learner who keeps the tie-corrected SD in part 2 is refused there (the stem says to ignore the tie)
check('tie-corrected SD 15.9256 not in the part 2 band', not in_band(math.sqrt(v1), W[1]['answer'], W[1]['tol']['abs']))

# ---- printed numbers in the text
text = json.dumps(problem, ensure_ascii=False)
for s in ['4.5 + 8 = 12.5', 'ranks 4 and 5', 'W^- = 92.5', '14 \\\\times 15 \\\\times 29/24 = 253.75',
          '\\\\sqrt{253.75} \\\\approx 15.9295', '\\\\sqrt{1015}', '1015/4 = 253.75', '14 \\\\times 15/4 = 52.5',
          '(12.5 - 52.5)/15.9295 \\\\approx -2.511', 'gap of $-40$', '12.5/15.9295', '\\\\Phi(2.511) = 0.99398',
          '1 - 0.99398 \\\\approx 0.0060', '0.0120 counts both tails', '0.9940 is the area above',
          'which is 40 below', 'twelve months the new method won', 'For $n = 14$', 'Give 4 decimal places',
          'Give 3 decimal places', 'Give a decimal']:
    check(f'text has {s!r}', s in text)
check('no leftover of the 12-month version',
      not re.search(r'8\.5\b|69\.5|162\.5|12\.7475|2\.393|0\.0084|0\.99164|\b78\b|\b650\b|12 months|12 sizes', text))
check('part 4 names the source of the tail', 'You are told' in parts[3]['question'])
check('1% claim holds for normal and exact p', p_told < 0.01 and exact_p < 0.01)

# ---- claims
check('part 3 explain: 105 is the rank total, not a count of ranks (finding 1)',
      'half the 105 ranks' not in parts[2]['explain']['text'])

def leaves(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from leaves(v)
    elif isinstance(o, list):
        for v in o:
            yield from leaves(v)
    elif isinstance(o, str):
        yield o


# ---- reuse: key numbers nowhere else in the course or the exams that hold its items
others = [f for f in glob.glob(os.path.join(COURSE, '*.json'))]
others += [f for f in glob.glob(os.path.join(CONTENT, 'exams', '*.json')) if '"sm-' in open(f).read()]
check('exams holding the course items found (skills sm-*; the string stat-models is in no exam)', any(os.path.basename(os.path.dirname(f)) == 'exams' for f in others))
for f in others:
    raw = json.load(open(f))
    if os.path.samefile(f, SET):
        raw['items'] = [p for p in raw['items'] if p['id'] != 'p-hedge-ranks']
    body = json.dumps(raw, ensure_ascii=False)
    for num in ['92.5', '52.5', '253.75', '15.9295', '15.93', '31.8591', '1015', '2.511', '0.99398', '253.625']:
        check(f'{num} absent from {os.path.basename(f)}', not re.search(r'(?<![\d.])' + re.escape(num) + r'(?!\d)', body))
    # the data: no single text field of another file holds six or more of the 13 distinct sizes
    worst = max((len({f'{s:.1f}' for s in sizes} & set(re.findall(r'(?<![\d.])\d\.\d(?!\d)', leaf))) for leaf in leaves(raw)), default=0)
    check(f'data not held in one field of {os.path.basename(f)}', worst < 6, str(worst))
l10 = json.dumps(json.load(open(os.path.join(COURSE, 'l10-rank-tests.json'))), ensure_ascii=False)
check('l10 signed-rank screen has 12 days and W- = 8; set has 14 and 12.5', n != 12 and 'W^- = 8' in l10)
check('l10 ties are at ranks 3, 4 (quiz) and 5, 6 (screen 8 prose); set at 4, 5',
      'span ranks 3 and 4' in l10 and 'ranks 5 and 6' in l10 and 'ranks 4 and 5' not in l10)

print(f'{checks} checks, {findings} FINDING lines')
sys.exit(0)
