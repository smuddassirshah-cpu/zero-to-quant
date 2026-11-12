"""Fix pass, proof problems-1 to -3: the re-set problems, checked from the files by brute force.
Independent of docs/reports/problems-proof-numbers.py. For each re-set or changed problem it rebuilds the key and each
`wrong` value from the slip its line names, and checks every claim the new text states (true by search over a range;
a false claim has its smallest counterexample verified). `mine.py` is the pre-fix reader's script: its checks on
p-rule-and-domain, p-two-odd-squares and p-even-test-contra describe the old text and are superseded by this file.
Usage (repo root): <venv>/bin/python docs/reviews/review-problems-proof-1-3-scripts/fix-pass.py"""
import itertools
import json
import sys

C = 'app/content/courses/proof/'
SETS = {n: {i['id']: i for i in json.load(open(f'{C}problems-{n}.json'))['items']} for n in (1, 2, 3)}
checks = fails = 0


def ok(c, m):
    global checks, fails
    checks += 1
    if not c:
        fails += 1
        print('FAIL', m)


def key(n, iid, k):
    w = SETS[n][iid]['parts'][k - 1]['widget']
    return w['answer'], {x['id']: x['value'] for x in w.get('wrong', []) if 'value' in x}


def num(n, iid, k, answer, slips):
    a, w = key(n, iid, k)
    ok(a == answer, f'{iid} part {k}: key {a} vs {answer}')
    ok(w == slips, f'{iid} part {k}: wrong {w} vs {slips}')
    ok(answer not in w.values() and len(set(w.values())) == len(w), f'{iid} part {k}: slips distinct from the key')


# ---- problems-1: parcels (40 parcels, 12 heavy, 15 labelled, 9 both)
parcels = [(True, True)] * 9 + [(True, False)] * 3 + [(False, True)] * 6 + [(False, False)] * 22
imp = lambda a, b: (not a) or b
num(1, 'p-leverage-calls', 1, sum(p and not q for p, q in parcels), {'swapped': 6, 'both': 9})
num(1, 'p-leverage-calls', 2, sum(imp(p, q) for p, q in parcels), {'true-true': 9, 'breakers': 3})
num(1, 'p-leverage-calls', 3, sum(not imp(q, p) for p, q in parcels), {'rule': 3, 'true-count': 34})
ok(len(parcels) == 40 and sum(p for p, _ in parcels) == 12 and sum(q for _, q in parcels) == 15, 'parcel counts 40, 12, 15')

# ---- problems-1: greenhouse
rows = list(itertools.product([True, False], repeat=3))
P, Q, R = 24 < 30, 21 > 25, 40 < 50
num(1, 'p-spread-signal', 1, int(P) + int(Q) + int(R), {'all': 3, 'one': 1})
ok(not ((P or Q) and not R), 'no watering on Monday')
num(1, 'p-spread-signal', 3, sum((p or q) and not r for p, q, r in rows), {'or-only': 6, 'not-r-only': 4, 'and': 1})
num(1, 'p-spread-signal', 4, sum(imp(p or q, not r) for p, q, r in rows), {'as-and': 3, 'only-false-if': 2})
androws = {r for r in rows if (r[0] or r[1]) and not r[2]}
failrows = {r for r in rows if not imp(r[0] or r[1], not r[2])}
ok(len(androws) == len(failrows) == 3 and not androws & failrows, 'finding 1: the and rows and the failing rows share no row')

# ---- problems-1: dancers (grid in the file)
cells = SETS[1]['p-fund-thresholds']['canvas']['params']['cells']
g = [[int(x) for x in r] for r in cells]
ok(all('%' not in x for r in cells for x in r), 'no % sign in the grid')
A = lambda t: all(any(v > t for v in r) for r in g)
B = lambda t: any(all(r[y] > t for r in g) for y in range(4))
num(1, 'p-fund-thresholds', 2, sum(all(r[y] > 5 for r in g) for y in range(4)), {'some-fund': 4})
num(1, 'p-fund-thresholds', 3, max(t for t in range(-3, 12) if B(t)), {'at-least': 3, 'swapped': 6})
num(1, 'p-fund-thresholds', 4, max(t for t in range(-3, 12) if A(t)), {'at-least': 7, 'kept-b': 2, 'best-fund': 8})

# ---- problems-2: f_c(x) = c x - 4
fc = lambda c, x: c * x - 4
box = range(-25, 26)
inj = {c: len({fc(c, x) for x in box}) == len(box) for c in range(-15, 16)}
ok([c for c, v in inj.items() if not v] == [0], 'f_c is one-to-one exactly for c != 0 (box search)')
num(2, 'p-rule-and-domain', 1, [c for c, v in inj.items() if not v][0], {'constant': -4, 'unit': 1})
sol = [x for x in range(-50, 51) if fc(-2, x) == -10]
num(2, 'p-rule-and-domain', 3, sol[0], {'sign': 7, 'applied-f': fc(-2, -10), 'dropped-minus': -3})
ok(fc(-2, 7) == -18 and fc(-2, -3) == 2, 'checks stated in the slip lines')
img = {fc(4, n) for n in range(-100, 101)}
num(2, 'p-rule-and-domain', 4, sum(y not in img for y in range(1, 31)), {'hits': 7, 'onto': 0})
ok(all(fc(c, (y + 4) / c) == y for c in (-7, -2, 3, 4, 9) for y in range(-20, 21)), 'onto for c != 0: x = (y + 4)/c')

# ---- problems-2: ferries (same maths as the old traders and desks)
berth = {f: (f + 1) // 2 for f in range(1, 9)}
im = lambda X: {berth[f] for f in X}
Aa, Bb = {1, 2, 3, 5}, {2, 4, 6, 7}
num(2, 'p-shift-images', 1, len(im(Aa)), {'traders': 4})
num(2, 'p-shift-images', 2, len(im(Aa) & im(Bb)), {'image-of-meet': 1, 'union': 4})
num(2, 'p-shift-images', 3, len(im(Aa & Bb)), {'same': 3, 'empty': 0})

# ---- problems-3: remainder 1 on division by 5
T = range(-60, 61)
ok(all((u * v) % 5 == 1 for u in T for v in T if u % 5 == 1 and v % 5 == 1), 'claim true on -60..60')
num(3, 'p-two-odd-squares', 3, (11 * 16 - 1) // 5, {'lost-middle': 5 * 2 * 3, 'whole-product': 176})
first = [n for n in range(1, 40) if (4 * n) % 5 == 1 and not (4 % 5 == 1 and n % 5 == 1)][0]
num(3, 'p-two-odd-squares', 4, first, {'if-fails': 1})
ok([(4 * n) % 5 for n in (1, 2, 3, 4)] == [4, 3, 2, 1], 'the converse: 4 x 4 = 16 is the first product leaving 1')
ok(all((a * b) % 5 == 1 for a in (6, 11) for b in (6, 11)) and 6 * 6 == 36, 'the cases option: 36 and 66 leave 1')

# ---- problems-3: the sum
S = lambda n: sum(3 * i - 2 for i in range(1, n + 1))
num(3, 'p-step-three-sum', 2, S(10), {'guess-a': 37, 'last-term': 28})
w = SETS[3]['p-step-three-sum']['parts'][2]['widget']
k = 7
ok(w['answer'] == '3k^2+5k+2' and k * (3 * k - 1) + 2 * (3 * k + 1) == 3 * k * k + 5 * k + 2 == (k + 1) * (3 * k + 2), 'numerator multiplied out, tested at k = 7')
ok(w.get('form') == 'expanded' and w['accept'] == ['3k^2+5k+2'], 'part 3 takes the expanded form only')
ok({x['id']: x['tex'] for x in w['wrong']} == {'no-double': '3k^2+2k+1', 'copied': '3k^2-k', 'bracket': '3k+2'}, 'part 3 slips')
ok(all(k * (3 * k - 1) + (3 * k + 1) == 3 * k * k + 2 * k + 1 and k * (3 * k - 1) == 3 * k * k - k for k in range(-9, 10)), 'slip values')

# ---- problems-3: n^2 + 2
Tn = range(-90, 91)
ok(all(t % 3 != 0 for t in Tn if (t * t + 2) % 3 == 0), 'claim: n^2 + 2 a multiple of 3 gives n not a multiple of 3, true on -90..90')
ok(all((t * t + 2) % 3 == 0 for t in Tn if t % 3 != 0), 'the converse is true here, as the option says')
ok(all(((3 * t) ** 2 + 2) == 3 * (3 * t * t) + 2 and ((3 * t) ** 2 + 2) % 3 == 2 for t in Tn), 'n = 3k: bracket 3k^2, remainder 2')
num(3, 'p-even-test-contra', 4, 3 * (-2) ** 2, {'sign': -12, 'n-squared': 36, 'whole': 38})
ok((-6) ** 2 + 2 == 38 == 3 * 12 + 2, 'n = -6: 38 = 3 x 12 + 2')

print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
