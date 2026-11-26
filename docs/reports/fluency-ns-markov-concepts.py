#!/usr/bin/env python3
"""Blind concept audit of six Fluency sets (audit fluency-ns-markov).

number-sense: fluency-l3-adding-pieces, l5-how-many-halves, l8-below-zero, l9-negative-times-negative, l12-which-first
markov:       fluency-l2-transition-matrix

Part A enumerates the WHOLE range of every family, from the vars read out of the JSON but with the key, every slip and
every `when` re-derived here in exact fractions (never from the file's `let`). Per draw it checks: the draw is well
posed, the key is what the named operation gives, every offered slip is the value its feedback line names, no slip
(with its band) reaches the key, no two offered slips of one draw are the same value (a learner would then be told
the wrong mistake), and the rules the feedback states hold.
Part B draws 300 items per family with tools/fluency-sample.mjs and compares the printed key and slips with Part A's
derivation from the printed vars.

Exit 0 when every check passes. A check that fails because the content is wrong stays failing (see the audit).
Run from the repo root or anywhere: python3 docs/reports/fluency-ns-markov-concepts.py [--no-node]
"""
import itertools, json, math, os, re, subprocess, sys
from fractions import Fraction as F

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
APP = os.path.join(ROOT, 'app')
NS = os.path.join(APP, 'content', 'courses', 'number-sense')
MK = os.path.join(APP, 'content', 'courses', 'markov')
fails, passes, notes = [], [0], []


def check(ok, label, detail=''):
    if ok:
        passes[0] += 1
    else:
        fails.append(f'{label}: {detail}')


def load(folder, name):
    d = json.load(open(os.path.join(folder, name + '.json')))
    return {f['id']: f for f in d['families']}


def space(fam):
    """Every combination of the family's vars (before `where`), as dicts. Decimals become exact fractions."""
    axes = []
    for key, v in fam['vars'].items():
        if 'int' in v:
            lo, hi = v['int']
            vals = [x for x in range(lo, hi + 1, v.get('step', 1)) if x not in v.get('not', [])]
            axes.append([{key: x} for x in vals])
        elif 'as' in v:
            axes.append([dict(zip(v['as'], [F(str(x)) if isinstance(x, float) else x for x in t])) for t in v['pick']])
        else:
            axes.append([{key: (F(str(x)) if isinstance(x, (int, float)) else x)} for x in v['pick'] if x not in v.get('not', [])])
    for combo in itertools.product(*axes):
        d = {}
        for part in combo:
            d.update(part)
        yield d


def lowest(pairs, label):
    for n, d in pairs:
        check(math.gcd(n, d) == 1 and 0 < n < d, label + ' tuple is a proper fraction in lowest terms', f'{n}/{d}')


# ---------------------------------------------------------------------------------------------------------------
# Derivations: for each family, model(vars) -> None when the draw is rejected, else
#   { key, slips: {id: (value, band)}, rules: [(label, bool)] }   (slips holds only those offered on the draw)
# ---------------------------------------------------------------------------------------------------------------
def m_add_unlike(v):
    a, b, c, d = v['a'], v['b'], v['c'], v['d']
    L = b * d // math.gcd(b, d)
    if b == d or L > 36:
        return None
    key = F(a, b) + F(c, d)
    u, w = a * L // b, c * L // d
    return dict(key=key, slips={'tops-and-bottoms': (F(a + c, b + d), 0), 'tops-not-renamed': (F(a + c, L), 0)},
                rules=[('renamed tops', F(u, L) == F(a, b) and F(w, L) == F(c, d)),
                       ('sum over the common size', F(u + w, L) == key),
                       ('key is not a whole number (prompt says fraction)', key.denominator != 1),
                       ('mediant lies strictly below the sum', F(a + c, b + d) < key)])


def m_sub_unlike(v):
    a, b, c, d = v['a'], v['b'], v['c'], v['d']
    L = b * d // math.gcd(b, d)
    if b == d or L > 36 or not a * d > b * c:
        return None
    key = F(a, b) - F(c, d)
    slips = {}
    if a > c and b > d and F(a - c, b - d) != key:
        slips['tops-and-bottoms'] = (F(a - c, b - d), 0)
    if F(a - c, L) != key:
        slips['tops-not-renamed'] = (F(a - c, L), 0)
    u, w = a * L // b, c * L // d
    return dict(key=key, slips=slips, rules=[('difference over the common size', F(u - w, L) == key), ('key positive', key > 0),
                                             ('key is not a whole number', key.denominator != 1)])


def m_whole_by_fraction(v):
    n, a, b = v['n'], v['a'], v['b']
    key = F(n) / F(a, b)
    slips = {'multiplied': (F(n) * F(a, b), 0)}
    if a > 1:
        slips['bottom-only'] = (F(n * b), 0)
    # the key is the number of portions of a/b that fit into n: key * (a/b) == n
    return dict(key=key, slips=slips, rules=[('key portions make n', key * F(a, b) == n), ('pieces / a', F(n * b, a) == key)])


def m_fraction_by_fraction(v):
    a, b, c, d = v['a'], v['b'], v['c'], v['d']
    if a * d == b * c or F(a * d, b * c) > 12:
        return None
    key = F(a, b) / F(c, d)
    return dict(key=key, slips={'multiplied': (F(a, b) * F(c, d), 0), 'flipped-first': (F(b, a) * F(c, d), 0)},
                rules=[('key times divisor is the dividend', key * F(c, d) == F(a, b)),
                       ('multiply by the upside-down', F(a, b) * F(d, c) == key and F(a * d, b * c) == key)])


def m_add_signed(v):
    a, m, s, dr = v['a'], v['m'], v['s'], v['dir']
    if not (a < 0 or s < 0):
        return None
    b = s * m
    key = a + b
    slips = {'wrong-way': (a - b, 0)}
    if abs(a) + m != a - b and abs(a) + m != key:
        slips['dropped-signs'] = (abs(a) + abs(b), 0)
    return dict(key=key, slips=slips, rules=[('adding a negative moves left, a positive right', dr == ('left' if b < 0 else 'right')),
                                             ('direction and distance give the key', key == a + (m if dr == 'right' else -m))])


def m_subtract_signed(v):
    a, m, s, dr = v['a'], v['m'], v['s'], v['dir']
    b = s * m
    if not (a < 0 or s < 0 or a < m) or a == b:
        return None
    key = a - b
    return dict(key=key, slips={'added': (a + b, 0), 'reversed': (b - a, 0)},
                rules=[('subtracting a negative moves right, a positive left', dr == ('right' if b < 0 else 'left')),
                       ('direction and distance give the key', key == a + (m if dr == 'right' else -m)),
                       ('opp is the other direction', {dr, v['opp']} == {'left', 'right'})])


def m_multiply_two(v):
    a, b = v['a'], v['b']
    if not (a < 0 or b < 0):
        return None
    key = a * b
    slips = {'sign-flipped': (-key, 0)}
    if a < 0 and b < 0 and a + b != -key:
        slips['added'] = (a + b, 0)
    negs = (a < 0) + (b < 0)
    return dict(key=key, slips=slips, rules=[('two negatives positive, one negative negative', (key > 0) == (negs == 2)),
                                             ('size is the product of sizes', abs(key) == abs(a) * abs(b))])


def m_divide_two(v):
    q, b = v['q'], v['b']
    a = q * b
    if not (a < 0 or b < 0):
        return None
    key = F(a, b)
    return dict(key=key, slips={'sign-flipped': (-key, 0), 'upside-down': (F(b, a), F(5, 1000))},
                rules=[('key is whole', key.denominator == 1 and key == q),
                       ('division follows the sign rule of multiplication', (key > 0) == ((a < 0) == (b < 0))),
                       ('a decimal to 2 places of b/a lands in the slip band', abs(F(round(F(b, a) * 100), 100) - F(b, a)) <= F(5, 1000))])


def m_multiply_three(v):
    a, b, c = v['a'], v['b'], v['c']
    if not (a < 0 or b < 0 or c < 0):
        return None
    key = a * b * c
    negs = (a < 0) + (b < 0) + (c < 0)
    return dict(key=key, slips={'sign-flipped': (-key, 0), 'first-pair-only': (a * b, 0)},
                rules=[('odd count of negatives gives a negative', (key < 0) == (negs % 2 == 1))])


def m_times_before_plus(v):
    a, b, c, s = v['a'], v['b'], v['c'], v['s']
    check(v['o'] == ('+' if s == 1 else '-'), 'l12 times-before-plus: sign matches symbol', str(v))
    key = a + b * c if s == 1 else a - b * c
    ltr = ((a + b) if s == 1 else (a - b)) * c
    slips = {'left-to-right': (ltr, 0)}
    if key < 0 and abs(key) != ltr:
        slips['lost-sign'] = (abs(key), 0)
    return dict(key=key, slips=slips, rules=[('a negative key only arises from a subtraction', key >= 0 or s == -1)])


def m_powers_next(v):
    a, b, c, s = v['a'], v['b'], v['c'], v['s']
    check(v['o'] == ('+' if s == 1 else '-'), 'l12 powers-next: sign matches symbol', str(v))
    key = a + s * (b * (c ** 2))
    slips = {'multiplied-then-squared': (a + s * ((b * c) ** 2), 0)}
    if c != 2:
        slips['doubled'] = (a + s * (b * (c * 2)), 0)
    return dict(key=key, slips=slips, rules=[])


def m_brackets_first(v):
    a, b, d, g = v['a'], v['b'], v['d'], v['g']
    c = d + g
    key = a + b * ((c - d) ** 2)
    return dict(key=key, slips={'added-first': ((a + b) * (c - d) ** 2, 0), 'multiplied-then-squared': (a + (b * (c - d)) ** 2, 0)},
                rules=[('bracket is positive', c - d >= 2)])


def m_left_to_right(v):
    b, m, c, k = v['b'], v['m'], v['c'], v['k']
    a = b * m
    check((v['o1'], v['o2']) == (('-', '+') if k == 1 else ('\\div', '\\times')), 'l12 left-to-right: symbols match k', str(v))
    if k == 1:
        key = (a - b) + c
        slips = {'right-pair-first': (F(a - (b + c)), F(1, 100)), 'minus-lost': (a + b + c, 0)}
    else:
        key = F(a, b) * c
        slips = {'right-pair-first': (F(a, b * c), F(1, 100))}
    rp = slips['right-pair-first'][0]
    return dict(key=key, slips=slips, rules=[('key is whole', F(key).denominator == 1),
                                             ('a decimal to 2 places of the right-pair slip lands in its band', abs(F(round(rp * 100), 100) - rp) <= F(1, 100))])


def P2(P):
    n = len(P)
    return [[sum(P[i][k] * P[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def m_two_state(v):
    a, b, i, j = v['a'], v['b'], v['i'], v['j']
    if a == b:
        return None
    P = [[a, 1 - a], [b, 1 - b]]
    names = ['bull', 'bear']
    key = P2(P)[i][j]
    slips = {}
    if P[i][j] ** 2 != key:
        slips['squared-entry'] = (P[i][j] ** 2, 0)
    if P[i][j] != key:
        slips['one-step'] = (P[i][j], 0)
    return dict(key=key, slips=slips, rules=[('rows sum to 1', all(sum(r) == 1 for r in P)), ('entries strictly between 0 and 1', all(0 < x < 1 for r in P for x in r)),
                                             ('state words match indices', v['fi'] == names[i] and v['tj'] == names[j]),
                                             ('key has at most 2 decimal places', (key * 100).denominator == 1),
                                             ('row of P^2 sums to 1', sum(P2(P)[i]) == 1)])


def m_three_state(v):
    P = [[v['a1'], v['a2'], v['a3']], [v['b1'], v['b2'], v['b3']], [v['c1'], v['c2'], v['c3']]]
    j = v['j'] - 1
    key = P2(P)[0][j]
    slips = {}
    if P[0][j] ** 2 != key:
        slips['squared-entry'] = (P[0][j] ** 2, 0)
    if P[0][j] != key:
        slips['one-step'] = (P[0][j], 0)
    return dict(key=key, slips=slips, rules=[('rows sum to 1', all(sum(r) == 1 for r in P)), ('entries strictly between 0 and 1', all(0 < x < 1 for r in P for x in r)),
                                             ('state word matches column', v['tj'] == ['Sunny', 'Cloudy', 'Rain'][j]),
                                             ('key has at most 2 decimal places', (key * 100).denominator == 1)])


def m_distribution(v):
    u, a, b, j = v['u'], v['a'], v['b'], v['j']
    if a == b:
        return None
    P = [[a, 1 - a], [b, 1 - b]]
    pi0 = [u, 1 - u]
    pi1 = [sum(pi0[k] * P[k][c] for k in range(2)) for c in range(2)]   # row vector times matrix
    key = pi1[j]
    slips = {}
    if P[0][j] != key:
        slips['bull-row-only'] = (P[0][j], 0)
    if P[0][j] + P[1][j] != key:
        slips['unweighted-column'] = (P[0][j] + P[1][j], 0)
    return dict(key=key, slips=slips, rules=[('rows sum to 1', all(sum(r) == 1 for r in P)), ('pi_1 sums to 1', sum(pi1) == 1),
                                             ('state word matches column', v['tj'] == ['bull', 'bear'][j]),
                                             ('key has at most 3 decimal places', (key * 1000).denominator == 1)])


SETS = [
    (NS, 'number-sense', 'fluency-l3-adding-pieces', {'add-unlike': m_add_unlike, 'subtract-unlike': m_sub_unlike}),
    (NS, 'number-sense', 'fluency-l5-how-many-halves', {'whole-by-fraction': m_whole_by_fraction, 'fraction-by-fraction': m_fraction_by_fraction}),
    (NS, 'number-sense', 'fluency-l8-below-zero', {'add-signed': m_add_signed, 'subtract-signed': m_subtract_signed}),
    (NS, 'number-sense', 'fluency-l9-negative-times-negative', {'multiply-two': m_multiply_two, 'divide-two': m_divide_two, 'multiply-three': m_multiply_three}),
    (NS, 'number-sense', 'fluency-l12-which-first', {'times-before-plus': m_times_before_plus, 'powers-next': m_powers_next, 'brackets-first': m_brackets_first, 'left-to-right': m_left_to_right}),
    (MK, 'markov', 'fluency-l2-transition-matrix', {'two-state-two-step': m_two_state, 'three-state-two-step': m_three_state, 'distribution-forward': m_distribution}),
]

# ------------------------------------------------- Part A: whole range -------------------------------------------------
print('Part A: whole-range enumeration')
for folder, course, sid, models in SETS:
    fams = load(folder, sid)
    check(set(fams) == set(models), f'{sid}: families audited', f'{sorted(fams)} vs {sorted(models)}')
    for fid, model in models.items():
        fam = fams[fid]
        tag = f'{sid}#{fid}'
        for key, vv in fam['vars'].items():
            if 'as' in vv and all(isinstance(x, int) for t in vv['pick'] for x in t) and len(vv['as']) == 2 and sid in ('fluency-l3-adding-pieces', 'fluency-l5-how-many-halves'):
                lowest(vv['pick'], f'{tag} {key}')
        total = kept = 0
        offered = {}
        clash = {}
        keyhit = {}
        rulebad = {}
        declared = [w['id'] for w in fam.get('wrong', [])]
        for v in space(fam):
            total += 1
            r = model(v)
            if r is None:
                continue
            kept += 1
            for label, ok in r['rules']:
                if not ok:
                    rulebad.setdefault(label, []).append(v)
            ids = list(r['slips'])
            for sidn in ids:
                offered[sidn] = offered.get(sidn, 0) + 1
                val, band = r['slips'][sidn]
                if abs(F(val) - F(r['key'])) <= band:
                    keyhit.setdefault(sidn, []).append(v)
            for x, y in itertools.combinations(ids, 2):
                (vx, bx), (vy, by) = r['slips'][x], r['slips'][y]
                if abs(F(vx) - F(vy)) <= max(bx, by):
                    clash.setdefault((x, y), []).append(v)
        check(kept > 0 and (total - kept) / total <= 0.8, f'{tag}: where keeps enough draws', f'{kept} of {total}')
        check(set(offered) == set(declared), f'{tag}: every declared slip is offered somewhere', f'{sorted(offered)} vs {declared}')
        for label, bad in rulebad.items():
            check(False, f'{tag}: rule "{label}"', f'{len(bad)} draws, first {bad[0]}')
        if not rulebad:
            check(True, tag)
        for sidn, bad in keyhit.items():
            check(False, f'{tag}: slip {sidn} reaches the key', f'{len(bad)} draws, first {bad[0]}')
        for pair, bad in clash.items():
            check(False, f'{tag}: slips {pair[0]} and {pair[1]} are the same value', f'{len(bad)} of {kept} draws, first {bad[0]}')
        print(f'  {tag}: {kept} of {total} combinations kept; slips offered {offered}')

# Identities behind "never equal" claims the content relies on (stated in the audit).
# two-state chain with a != b: P^2[i][j] != P[i][j] for every i, j (so the one-step slip is always a slip)
for a, b in itertools.product([F(k, 10) for k in range(1, 10)], repeat=2):
    P = [[a, 1 - a], [b, 1 - b]]
    for i in range(2):
        for j in range(2):
            check((P2(P)[i][j] == P[i][j]) == (a == b), 'two-state: P^2 = P entrywise exactly when the rows are equal', f'{a} {b} {i} {j}')

# ---------------------------------------- Part A2: draws where a named wrong method scores ----------------------------------------
# A slip switched off by `when ... != key` on a draw means the mistake its line names GIVES THE KEY there: the draw rewards the wrong method.
print('Part A2: draws where a named wrong method gives the key (should be excluded by `where`)')
def wrong_method_hits():
    out = {}
    fam = load(NS, 'fluency-l3-adding-pieces')['subtract-unlike']
    for v in space(fam):
        r = m_sub_unlike(v)
        if r is None:
            continue
        a, b, c, d = v['a'], v['b'], v['c'], v['d']
        L = b * d // math.gcd(b, d)
        if F(a - c, L) == r['key']:
            out.setdefault('fluency-l3-adding-pieces#subtract-unlike tops-not-renamed', []).append(v)
        if a > c and b > d and F(a - c, b - d) == r['key']:
            out.setdefault('fluency-l3-adding-pieces#subtract-unlike tops-and-bottoms', []).append(v)
    fams = load(MK, 'fluency-l2-transition-matrix')
    for v in space(fams['two-state-two-step']):
        r = m_two_state(v)
        if r is None:
            continue
        P = [[v['a'], 1 - v['a']], [v['b'], 1 - v['b']]]
        if P[v['i']][v['j']] ** 2 == r['key']:
            out.setdefault('fluency-l2-transition-matrix#two-state-two-step squared-entry', []).append(v)
        if P[v['i']][v['j']] == r['key']:
            out.setdefault('fluency-l2-transition-matrix#two-state-two-step one-step', []).append(v)
    for v in space(fams['three-state-two-step']):
        r = m_three_state(v)
        p = [v['a1'], v['a2'], v['a3']][v['j'] - 1]
        if p ** 2 == r['key']:
            out.setdefault('fluency-l2-transition-matrix#three-state-two-step squared-entry', []).append(v)
        if p == r['key']:
            out.setdefault('fluency-l2-transition-matrix#three-state-two-step one-step', []).append(v)
    for v in space(fams['distribution-forward']):
        r = m_distribution(v)
        if r is None:
            continue
        pj = [v['a'], 1 - v['a']][v['j']]
        if pj == r['key']:
            out.setdefault('fluency-l2-transition-matrix#distribution-forward bull-row-only', []).append(v)
    return out
for label, hits in wrong_method_hits().items():
    show = {k: (str(x) if isinstance(x, F) else x) for k, x in hits[0].items()}
    check(False, f'{label}: the named wrong method gives the key', f'{len(hits)} draws, first {show}')

# ---------------------------------------- Part A3: a key above 1 and the mixed number the lesson teaches ----------------------------------------
# form "fraction" grades a mixed number wrong (key `form`; AUTHORING section 3, checked with grade-all on a scratch widget), Fluency gives no
# second try, and lessons l3 and l5 teach and accept 1 1/2. A family whose key can be a fraction above 1 must say which form it wants.
print('Part A3: prompts of families whose key can be a fraction above 1 say "not a mixed number"')
for sid, fid, model in [('fluency-l3-adding-pieces', 'add-unlike', m_add_unlike), ('fluency-l3-adding-pieces', 'subtract-unlike', m_sub_unlike),
                        ('fluency-l5-how-many-halves', 'whole-by-fraction', m_whole_by_fraction), ('fluency-l5-how-many-halves', 'fraction-by-fraction', m_fraction_by_fraction)]:
    fam = load(NS, sid)[fid]
    rs = [r for r in (model(v) for v in space(fam)) if r is not None]
    top_heavy = sum(1 for r in rs if r['key'] > 1 and F(r['key']).denominator > 1)
    says = bool(re.search(r'mixed number|one fraction|single fraction|top-heavy', fam['prompt']))
    print(f'  {sid}#{fid}: {top_heavy} of {len(rs)} draws have a top-heavy key; prompt names the form: {says}')
    check(top_heavy == 0 or says, f'{sid}#{fid}: prompt does not rule out a mixed number', f'{top_heavy} of {len(rs)} draws have a key above 1 that is not whole')

# Info only: l8 subtract-signed "reversed" (b - a). On draws with a < 0 the same value is "dropped the signs" (|a| - |b| or |a| + |b|).
fam = load(NS, 'fluency-l8-below-zero')['subtract-signed']
tot = same = 0
for v in space(fam):
    r = m_subtract_signed(v)
    if r is None:
        continue
    tot += 1
    b = v['s'] * v['m']
    same += r['slips']['reversed'][0] in (abs(v['a']) - abs(b), abs(v['a']) + abs(b))
print(f'Info: l8 subtract-signed "reversed" equals a dropped-signs sum or difference of sizes on {same} of {tot} draws')

# ------------------------------------------------- Part B: sampler draws -------------------------------------------------
def texval(t):
    t = str(t).strip()
    m = re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(-?\d+)\}', t)
    if m:
        return F(int(m.group(2)), int(m.group(3))) * (-1 if m.group(1) else 1)
    return F(t)


def vnum(x):
    if isinstance(x, str) and re.fullmatch(r'-?\d+/\d+', x):
        return F(x)
    if isinstance(x, float):
        return F(str(x))
    return x


if '--no-node' not in sys.argv:
    print('Part B: 300 sampler draws per family against the derivation')
    N = 300
    for folder, course, sid, models in SETS:
        for fid, model in models.items():
            tag = f'{sid}#{fid}'
            out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', f'{course}/{sid}', '--family', fid, '--n', str(N), '--json'],
                                 cwd=APP, capture_output=True, text=True)
            if out.returncode != 0:
                check(False, f'{tag}: sampler ran', out.stderr[-300:])
                continue
            items = json.loads(out.stdout)['items']
            check(len(items) == N, f'{tag}: {N} draws', str(len(items)))
            bad = 0
            first = ''
            prompts = set()
            for it in items:
                v = {k: vnum(x) for k, x in it['vars'].items()}
                r = model(v)
                prompts.add(it['prompt'])
                ok = r is not None
                if ok:
                    ans = texval(it['answer'])
                    ok = ans == F(r['key'])
                    if it['kind'] == 'expression':     # printed key must itself be in lowest terms, positive denominator
                        m = re.fullmatch(r'-?\\frac\{(\d+)\}\{(\d+)\}', it['answer'])
                        ok = ok and (it['answer'].lstrip('-').isdigit() or (m is not None and math.gcd(int(m.group(1)), int(m.group(2))) == 1 and int(m.group(2)) > 1))
                    got = {w['id']: (w.get('tex', w.get('value'))) for w in it['wrong']}
                    ok = ok and set(got) == set(r['slips'])
                    if ok:
                        for wid, raw in got.items():
                            val = texval(raw) if it['kind'] == 'expression' else F(str(raw))
                            want, band = r['slips'][wid]
                            if abs(val - F(want)) > F(1, 10 ** 9):
                                ok = False
                if not ok:
                    bad += 1
                    first = first or json.dumps({'vars': it['vars'], 'answer': it['answer'], 'wrong': it['wrong']})[:400]
            check(bad == 0, f'{tag}: sampler key and slips equal the derivation', f'{bad} of {N}; first {first}')
            print(f'  {tag}: {N} draws, {len(prompts)} distinct prompts, {bad} mismatches')

print(f'\n{passes[0]} checks passed, {len(fails)} failed')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
