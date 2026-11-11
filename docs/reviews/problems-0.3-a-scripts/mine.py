"""Second reader's own answers for counting problems 1 to 3 and functions problems 4.

Every counting answer is found by full enumeration (itertools) and again by formula with exact fractions.
Every `wrong` value is rebuilt from the slip its feedback names. Vector and function parts: sympy, then numbers.

Usage (repo root): <venv>/bin/python docs/reviews/problems-0.3-a-scripts/mine.py
Exit 0 when every check passes.
"""
import itertools as it
import json
import math
import sys
from fractions import Fraction as F
from math import comb, factorial as fact, perm

ROOT = 'app/content/courses/'
checks = fails = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', label)


def load(course, n):
    d = json.load(open(f'{ROOT}{course}/problems-{n}.json'))
    return {i['id']: i for i in d['items']}


def tolv(w):
    t = w.get('tol') or {}
    return t.get('abs', 0) if isinstance(t, dict) else 0


def part(items, pid, k, mine, wrongs=None, accept=(), reject=()):
    """mine: my value. wrongs: {id: value rebuilt from the slip}. accept/reject: typed values the band must take/refuse."""
    w = items[pid]['parts'][k - 1]['widget']
    lab = f'{pid}[{k}]'
    a, t = w['answer'], tolv(w)
    ok(abs(float(mine) - a) <= t + 1e-12, f'{lab} mine {float(mine)} vs key {a} tol {t}')
    for v in accept:
        ok(abs(float(v) - a) <= t + 1e-12, f'{lab} should accept {v}')
    for v in reject:
        ok(abs(float(v) - a) > t + 1e-12, f'{lab} should reject {v}')
    have = {x['id']: x for x in w.get('wrong', [])}
    for x in have.values():
        ok(abs(x['value'] - a) > t + tolv(x) - 1e-12, f'{lab} wrong {x["id"]} band overlaps the answer band')
    for wid, v in (wrongs or {}).items():
        if wid not in have:
            ok(False, f'{lab} no wrong id {wid}')
            continue
        x = have[wid]
        ok(abs(float(v) - x['value']) <= max(tolv(x), 5e-5) + 1e-12, f'{lab} wrong {wid}: slip gives {float(v)}, file {x["value"]}')
    missing = set(have) - set(wrongs or {})
    ok(not missing, f'{lab} wrong ids not rebuilt: {sorted(missing)}')


# ---------------------------------------------------------------- counting 1
c1 = load('counting', 1)

# tulip bed: choose 4 of 8, order them, 4 edging colours
groups = list(it.combinations(range(8), 4))
rows = list(it.permutations(range(8), 4))
ok(len(groups) == comb(8, 4) == 70 and len(rows) == perm(8, 4) == 1680, 'tulip enumerations')
part(c1, 'p-tulip-bed', 1, len(groups), {'ordered': 8 * 7 * 6 * 5, 'divide-four': 1680 // 4, 'times': 8 * 4})
part(c1, 'p-tulip-bed', 2, len(list(it.permutations(range(4)))), {'four': 4, 'repeats': 4 ** 4})
part(c1, 'p-tulip-bed', 3, len(rows), {'added': 70 + 24, 'carried': 1680 * 24})
part(c1, 'p-tulip-bed', 4, len(list(it.product(rows, range(4)))), {'added': 1680 + 4, 'no-order': 70 * 4, 'carried': 40320 * 4})

# team photo: 7 in a row, captain (0) in the middle, twins (1, 2) side by side
allp = list(it.permutations(range(7)))
mid = [p for p in allp if p[3] == 0]
both = [p for p in mid if abs(p.index(1) - p.index(2)) == 1]
pairs = [(i, i + 1) for i in range(6) if 3 not in (i, i + 1)]
ok(len(pairs) == 4, 'team photo: 4 free side-by-side pairs')
glued = [p for p in mid if abs(p.index(1) - p.index(2)) == 1 or {p.index(1), p.index(2)} == {2, 4}]
ok(len(glued) == 240 == fact(5) * 2, 'team photo: the glued block count is the 192 plus the 48 across the captain')
part(c1, 'p-team-photo', 1, len(allp), {'square': 49, 'sum': sum(range(1, 8)), 'seven': 7})
part(c1, 'p-team-photo', 2, len(mid), {'not-middle': 5040 - 720, 'six': 6})
part(c1, 'p-team-photo', 4, len(both), {'block': fact(5) * 2, 'no-swap': 4 * 24, 'pairs-six': 6 * 2 * 24})
ok(len(both) == 4 * 2 * fact(4) == 192, 'team photo formula')

# five-a-side
teams = range(8)
part(c1, 'p-five-a-side', 1, len(list(it.combinations(teams, 2))), {'ordered': 56, 'square': 64, 'times-two': 16})
part(c1, 'p-five-a-side', 2, len(list(it.permutations(teams, 2))), {'half': 14, 'carried': 112})
sol = [n for n in range(1, 100) if n * (n - 1) == 72]
ok(sol == [9], 'five-a-side: n(n-1) = 72 has one positive whole solution')
part(c1, 'p-five-a-side', 3, sol[0], {'halved': 36, 'one-factor': 8})
part(c1, 'p-five-a-side', 4, len(list(it.combinations(range(9), 6))), {'ordered': perm(9, 6), 'no-divide': 9 * 8 * 7, 'times': 54})

# ice-cream van
cups = list(it.combinations(range(11), 3))
cones = list(it.permutations(range(11), 3))
part(c1, 'p-ice-cream-van', 1, len(cups), {'ordered': 990, 'repeats': 11 ** 3, 'times': 33})
part(c1, 'p-ice-cream-van', 2, len(cones), {'times-three': 165 * 3, 'added': 165 + 6, 'carried': 990 * 6})
part(c1, 'p-ice-cream-van', 3, len(cups) + len(cones), {'multiplied': 165 * 990, 'carried': 990 + 5940})
part(c1, 'p-ice-cream-van', 4, (len(cups) + len(cones)) * 5, {'no-none': 1155 * 4, 'added': 1155 + 5, 'carried': 163350 * 5})

# ---------------------------------------------------------------- counting 2
c2 = load('counting', 2)


def touching(s, ch):
    return ch + ch in ''.join(s)


sig = set(it.permutations('RRRRBBY'))
tog = {s for s in sig if touching(s, 'B')}
ok(len(sig) == fact(7) // (fact(4) * 2) == 105 and len(tog) == fact(6) // fact(4) == 30, 'flags formulae')
part(c2, 'p-signal-flags', 1, len(sig), {'no-divide': 5040, 'reds-only': 5040 // 24, 'blues-only': 5040 // 2})
part(c2, 'p-signal-flags', 2, len(tog), {'flipped': 60, 'no-divide': 720, 'blue-divide': 720 // 48})
part(c2, 'p-signal-flags', 3, len(sig - tog), {'carried': 105 - 60, 'added': 135})
part(c2, 'p-signal-flags', 4, F(len(sig - tog), len(sig)), {'together': F(30, 105), 'carried': F(45, 105), 'bottom': F(75, 5040)},
     accept=[0.714, F(5, 7), F(75, 105), 0.7143], reject=[0.71, 0.7, 0.72])
ok(F(comb(7, 2) - 6, comb(7, 2)) == F(5, 7), 'flags: the check by places in the explanation')

S, G, B, N = 45, 38, 20, 80
members = ['s'] * (S - B) + ['g'] * (G - B) + ['b'] * B
members += ['n'] * (N - len(members))
atleast = sum(m != 'n' for m in members)
neither = members.count('n')
part(c2, 'p-leisure-centre', 1, atleast, {'no-overlap': 83, 'twice': 83 - 40})
part(c2, 'p-leisure-centre', 2, neither, {'carried': 80 - 43, 'only-one': (S - B) + (G - B)})
part(c2, 'p-leisure-centre', 3, F(neither, N), {'at-least': F(63, 80), 'carried': F(37, 80), 'bottom': F(17, 63)},
     accept=[0.213, 0.2125, 0.212, F(17, 80)], reject=[0.21, 0.22, 0.2])
pr = list(it.combinations(range(N), 2))
bothn = sum(1 for a, b in pr if members[a] == 'n' and members[b] == 'n')
ok(len(pr) == 3160 and bothn == 136, 'leisure pairs')
part(c2, 'p-leisure-centre', 4, F(bothn, len(pr)), {'replaced': F(17, 80) ** 2, 'ordered-top': F(17 * 16, 3160), 'pairs-over-members': F(136, 80)},
     accept=[0.043, F(17, 80) * F(16, 79), F(136, 3160), F(17, 395)], reject=[0.045, 0.04, 0.044])

bal = set(it.permutations('BALLOON'))
oo = {s for s in bal if touching(s, 'O')}
ll = {s for s in bal if touching(s, 'L')}
ok(len(bal) == 1260 and len(oo) == 360 == len(ll) and len(oo & ll) == 120 == fact(5), 'balloon formulae')
part(c2, 'p-balloon-blocks', 1, len(bal), {'no-divide': 5040, 'one-pair': 2520})
part(c2, 'p-balloon-blocks', 2, len(oo), {'flipped': 720, 'both-divided': 180})
part(c2, 'p-balloon-blocks', 3, len(bal - oo), {'carried': 1260 - 720, 'carried-half': 1260 - 180})
part(c2, 'p-balloon-blocks', 4, len(bal - oo - ll), {'all-ls': 900 - 360, 'both-only': 900 - 120})
part(c2, 'p-balloon-blocks', 5, F(len(bal - oo - ll), len(bal)), {'carried': F(540, 1260), 'os-only': F(900, 1260), 'bottom': F(660, 5040)},
     accept=[0.524, F(11, 21), F(660, 1260), 0.5238], reject=[0.52, 0.53, 0.5])

kids = ['g'] * 6 + ['b'] * 5
tm = list(it.combinations(range(11), 4))
nog = [t for t in tm if all(kids[i] == 'b' for i in t)]
nob = [t for t in tm if all(kids[i] == 'g' for i in t)]
mixed = [t for t in tm if len({kids[i] for i in t}) == 2]
part(c2, 'p-quiz-team', 1, len(tm), {'ordered': perm(11, 4), 'times': 44})
part(c2, 'p-quiz-team', 2, len(nog), {'no-boys': len(nob), 'ordered': perm(5, 4)})
part(c2, 'p-quiz-team', 3, len(tm) - len(nog), {'no-boys': 330 - 15, 'exactly-one': sum(1 for t in tm if sum(kids[i] == 'g' for i in t) == 1)})
part(c2, 'p-quiz-team', 4, len(mixed), {'no-girls-again': 325 - 5, 'both-off': 325 - 15 - 5})
part(c2, 'p-quiz-team', 5, F(len(mixed), len(tm)), {'girl-only': F(325, 330), 'bottom': F(310, 325), 'carried': F(305, 330)},
     accept=[0.939, F(31, 33), F(310, 330), 0.9394], reject=[0.94, 0.93, 0.9])

# SETS-3-AND-4 (appended below as each set is read)

if __name__ == '__main__':
    print(f'{checks} checks, {fails} failures')
    sys.exit(1 if fails else 0)
