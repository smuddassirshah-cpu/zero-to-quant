#!/usr/bin/env python3
"""Second reader's recomputation of measure-prob problems-4 (review-problems-measure-prob-4.md).

Imports nothing from the author's script. Route 1 is exact (fractions, polynomial
antiderivatives typed by hand, closed forms). Route 2 is another method: a midpoint
rule for the integrals, a walk over every tree path or every one of the 1,024 trade
sequences with exact path weights, and the pricing of the contract under Q against
the share measure. No solver and no random draw is used, so the result does not
depend on the SciPy build. Exits 0; each failing check prints a FINDING line.
"""
import json
import math
import os
import re
from fractions import Fraction as F
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
SET = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'measure-prob', 'problems-4.json')
d = json.load(open(SET, encoding='utf-8'))
items = {it['id']: it for it in d['items']}

n_checks = 0
n_find = 0


def check(ok, label):
    global n_checks, n_find
    n_checks += 1
    if not ok:
        n_find += 1
        print('FINDING', label)


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def part(pid, k):
    return items[pid]['parts'][k]


def key_takes(pid, k, value):
    w = part(pid, k)['widget']
    return abs(float(value) - float(w['answer'])) <= w['tol']['abs'] * (1 + 1e-9)


def wrong_of(pid, k, wid):
    for x in part(pid, k)['widget']['wrong']:
        if x['id'] == wid:
            return x
    return None


def num_part(pid, k, value, places, wrongs, also=()):
    """Key takes my value at the asked places and unrounded; each wrong is my slip value, is refused by the key,
    and no two bands overlap."""
    w = part(pid, k)['widget']
    tag = f'{pid} part {k + 1}'
    v = float(value)
    check(key_takes(pid, k, v), f'{tag}: key {w["answer"]} does not take my value {v:.8g}')
    check(key_takes(pid, k, round(v, places)), f'{tag}: key does not take my value at {places} places, {round(v, places)}')
    for a in also:
        check(key_takes(pid, k, a), f'{tag}: key does not take the value {a} that the rounded inputs give')
    ids = [x['id'] for x in w.get('wrong', [])]
    check(sorted(ids) == sorted(wrongs), f'{tag}: wrong ids {ids} are not the slips I rebuilt {sorted(wrongs)}')
    bands = [(float(w['answer']), w['tol']['abs'], 'key')]
    for wid, sv in wrongs.items():
        x = wrong_of(pid, k, wid)
        if x is None:
            continue
        sv = float(sv)
        tol = x['tol']['abs']
        check(abs(sv - x['value']) <= tol, f'{tag}: wrong "{wid}" is {x["value"]}, my slip gives {sv:.8g}')
        check(abs(round(sv, places) - x['value']) <= tol * (1 + 1e-9),
              f'{tag}: wrong "{wid}" band does not take the slip at {places} places, {round(sv, places)}')
        check(not key_takes(pid, k, sv), f'{tag}: the key band takes the slip "{wid}"')
        check(tol <= abs(x['value']) or x['value'] == 0, f'{tag}: wrong "{wid}" band is wider than its value')
        bands.append((x['value'], tol, wid))
    for i in range(len(bands)):
        for j in range(i + 1, len(bands)):
            a, b = bands[i], bands[j]
            check(abs(a[0] - b[0]) > a[1] + b[1], f'{tag}: bands "{a[2]}" and "{b[2]}" overlap')


def text_of(pid, k):
    p = part(pid, k)
    out = [p['question'], p['feedback']['correct'], p['feedback'].get('generic', ''), p['explain']['text']]
    out += list(p['feedback'].get('byKey', {}).values())
    for o in p['widget'].get('options', []):
        out += [o.get('text', ''), o.get('why', '')]
    return ' '.join(out)


def printed(pid, k, *figures):
    t = text_of(pid, k)
    for f_ in figures:
        check(str(f_) in t, f'{pid} part {k + 1}: expected the figure {f_} in the text')


def midpoint(f, a, b, n=200000):
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))


def choice_key(pid, k, want):
    opts = part(pid, k)['widget']['options']
    right = [o['id'] for o in opts if o.get('correct')]
    check(right == [want], f'{pid} part {k + 1}: correct option is {right}, I find {want}')


# ---------------------------------------------------------------- shape of the set
check(len(d['items']) == 4, 'set: 4 problems')
parts_all = [p for it in d['items'] for p in it['parts']]
check(len(parts_all) == 18, 'set: 18 parts')
typed = sum(1 for p in parts_all if p['widget']['kind'] in ('numeric', 'expression'))
check(typed * 3 >= 2 * len(parts_all), 'set: typed parts are under two thirds')
check(max(it['difficulty'] for it in d['items']) == 5, 'set: no difficulty 5')
course = json.load(open(os.path.join(os.path.dirname(SET), 'course.json'), encoding='utf-8'))
level4 = [lv for lv in course['levels'] if lv['n'] == 4][0]['lessons']
lesson_skills = set()
for les in level4:
    lesson_skills |= set(json.load(open(os.path.join(os.path.dirname(SET), les + '.json'), encoding='utf-8')).get('skills', []))
for it in d['items']:
    check(set(it['skills']) <= lesson_skills, f'{it["id"]}: skills {it["skills"]} not all carried by a level 4 lesson')
    check(3 <= len(it['parts']) <= 5, f'{it["id"]}: part count')
for p in parts_all:
    if p['widget']['kind'] == 'numeric':
        check(re.search(r'places|fraction|whole number', p['question']) is not None, f'numeric part states no form: {p["question"][:50]}')

# ---------------------------------------------------------------- p-recovery-reweight
# P density 2x, Q density 4x^3 on [0, 1]. Antiderivatives typed by hand.
P = 'p-recovery-reweight'
check(close(midpoint(lambda x: 2 * x, 0, 1), 1, 1e-9) and close(midpoint(lambda x: 4 * x ** 3, 0, 1), 1, 1e-9), P + ': both densities integrate to 1')
w0 = part(P, 0)['widget']
check(w0['answer'] == '2x^2', P + ' part 1: key is 2x^2')
pts = (F(1, 7), F(1, 3), F(9, 10), F(1))
for x in pts:
    check((4 * x ** 3) / (2 * x) == 2 * x ** 2, P + ' part 1: weight is 2x^2')
for name, form in (('reversed', lambda x: 1 / (2 * x ** 2)), ('q-only', lambda x: 4 * x ** 3), ('product', lambda x: 8 * x ** 4)):
    check(any(form(x) != 2 * x ** 2 for x in pts), f'{P} part 1: wrong form "{name}" equals the key')
check({x['id']: x['tex'] for x in w0['wrong']} == {'reversed': '\\frac{1}{2x^2}', 'q-only': '4x^3', 'product': '8x^4'}, P + ' part 1: wrong forms')
# part 2: Q(X > 0.8) = 1 - 0.8^4 exactly; route 2 integrates Z times the P density
q_tail = 1 - F(4, 5) ** 4
check(q_tail == F(369, 625), P + ' part 2: 369/625')
check(close(midpoint(lambda x: 2 * x * x * 2 * x, 0.8, 1), q_tail, 1e-9), P + ' part 2: midpoint rule')
num_part(P, 1, q_tail, 4, {
    'no-weight': 1 - F(4, 5) ** 2,                      # P chance
    'frozen': 2 * F(4, 5) ** 2 * (1 - F(4, 5) ** 2),    # weight held at its value at 0.8
    'complement': F(4, 5) ** 4,
})
printed(P, 1, '0.4096', '0.5904', '0.36')
# part 3: Var_P(Z) = E_P[Z^2] - 1, E_P[Z^2] = int 4x^4 2x = 8/6
ez = F(4, 4)                                              # int 2x^2 2x dx = 4/4
ez2 = F(8, 6)
check(close(midpoint(lambda x: 2 * x * x * 2 * x, 0, 1), ez, 1e-9), P + ' part 3: E_P[Z] = 1')
check(close(midpoint(lambda x: (2 * x * x) ** 2 * 2 * x, 0, 1), ez2, 1e-9), P + ' part 3: E_P[Z^2] = 4/3')
num_part(P, 2, ez2 - ez ** 2, 4, {
    'second-moment': ez2,
    'under-q': F(16, 8) - 1,                              # int 4x^4 4x^3 = 16/8, less 1
})
printed(P, 2, '\\tfrac43', '\\tfrac86', '\\tfrac13')
# part 4: E_Q[(dP/dQ)^2] = int (1/(4x^4)) 4x^3 dx = int dx/x, which diverges; P << Q holds
for eps in (1e-2, 1e-4, 1e-6):
    val = midpoint(lambda u: 1.0, math.log(eps), 0.0, 1000)       # x = e^u turns dx/x into du
    check(close(val, -math.log(eps), 1e-9), P + ' part 4: int_eps^1 dx/x = -ln eps')
for x in (F(1, 9), F(1, 3), F(7, 8)):
    check((1 / (2 * x ** 2)) ** 2 * 4 * x ** 3 == 1 / x, P + ' part 4: integrand is 1/x')
    check(1 / (2 * x ** 2) * 4 * x ** 3 == 2 * x, P + ' part 4: the mean of dP/dQ integrates the P density, 1')
choice_key(P, 3, 'infinite')
check('Part 3' in part(P, 3)['question'] and '\\tfrac13' in part(P, 3)['question'], P + ' part 4: restates part 3')

# ---------------------------------------------------------------- p-share-numeraire
P = 'p-share-numeraire'
S0, u, dn, R = F(48), F(5, 4), F(17, 20), F(51, 50)
q = (R - dn) / (u - dn)
check(q == F(17, 40), P + ': q = 0.425')
check('0.425' in items[P]['prose'], P + ': prose states q')
paths = list(product('ud', repeat=3))


def S_end(path, s0=S0, up=u, down=dn):
    s = s0
    for m in path:
        s *= up if m == 'u' else down
    return s


def prob(path, pu):
    r = F(1)
    for m in path:
        r *= pu if m == 'u' else 1 - pu
    return r


Z3 = {p_: S_end(p_) / (S0 * R ** 3) for p_ in paths}
check(S_end(('u', 'd', 'd')) == F(4335, 100), P + ' part 1: S_3 = 43.35')
num_part(P, 0, Z3[('u', 'd', 'd')], 4, {
    'no-discount': S_end(('u', 'd', 'd')) / S0,
    'one-discount': S_end(('u', 'd', 'd')) / (S0 * R),
}, also=(43.35 / 50.938,))
printed(P, 0, '43.35', '1.061208', '0.7225', '50.938', '0.8510')
check(round(float(S0 * R ** 3), 3) == 50.938 and round(float(R ** 3), 6) == 1.061208, P + ' part 1: printed cash figures')
# part 2: Z_3 > 0 on all eight, E_Q[Z_3] = 1, Z_3 < 2
check(len(paths) == 8 and all(z > 0 for z in Z3.values()), P + ' part 2: Z_3 > 0 on all eight paths')
check(sum(prob(p_, q) * Z3[p_] for p_ in paths) == 1, P + ' part 2: E_Q[Z_3] = 1')
check(max(Z3.values()) < 2, P + ' part 2: Z_3 < 2 on every path')
for p_real in (F(1, 2), F(3, 5)):
    check(sum(prob(p_, p_real) * Z3[p_] for p_ in paths) != 1, P + ' part 2: the mean is not 1 under another up chance')
choice_key(P, 1, 'mart')
# part 3: q^S from the measure itself (sum of Q^S over paths that start up), against q u / R
QS = {p_: prob(p_, q) * Z3[p_] for p_ in paths}
qS = sum(v for p_, v in QS.items() if p_[0] == 'u')
check(qS == q * u / R == F(25, 48), P + ' part 3: q^S = 25/48')
check(all(QS[p_] == prob(p_, qS) for p_ in paths), P + ' part 3: Q^S is the tree with up chance 25/48 at every step')
num_part(P, 2, qS, 4, {
    'no-cash': q * u,
    'down-factor': q * dn / R,
    'down-chance': (1 - q) * dn / R,
})
check(q * u + (1 - q) * dn > 1, P + ' part 3: without the cash factor the two chances add to more than 1')
check((1 - q) * dn / R == F(23, 48), P + ' part 3: down chance 23/48')
printed(P, 2, '\\tfrac{25}{48}', '\\tfrac{23}{48}', '0.575', '0.5208')
# part 4 and 5: price under Q against 48 Q^S(S_3 > 50)
price_q = sum(prob(p_, q) * S_end(p_) for p_ in paths if S_end(p_) > 50) / R ** 3
chance_s = sum(QS[p_] for p_ in paths if S_end(p_) > 50)
check(price_q == S0 * chance_s, P + ' part 4: the Q price equals 48 Q^S(S_3 > 50)')
check(sorted(set(S_end(p_) for p_ in paths)) == [F(29478, 1000), F(4335, 100), F(6375, 100), F(9375, 100)], P + ' part 5: end prices')
check(chance_s == 3 * qS ** 2 * (1 - qS) + qS ** 3, P + ' part 5: two or three ups')
check(round(float(chance_s), 6) == 0.531232, P + ' part 5: chance 0.531232')
e_qs_s = sum(QS[p_] * S_end(p_) for p_ in paths if S_end(p_) > 50) / R ** 3      # option "twice"
check(e_qs_s != price_q and chance_s / R ** 3 != price_q and S0 * sum(prob(p_, q) for p_ in paths if S_end(p_) > 50) != price_q,
      P + ' part 4: a distractor line equals the price')
choice_key(P, 3, 'qs')
num_part(P, 4, price_q, 2, {
    'q-chance': S0 * (3 * q ** 2 * (1 - q) + q ** 3),
    'top-only': S0 * qS ** 3,
    'discount': price_q / R ** 3,
}, also=(48 * 0.531232, 48 * (3 * 0.5208 ** 2 * 0.4792 + 0.5208 ** 3)))
printed(P, 4, '0.531232', '25.50', '63.75', '93.75', '43.35')

# ---------------------------------------------------------------- p-ten-trades
P = 'p-ten-trades'
pw, qw = F(1, 2), F(4, 5)
seqs = list(product((1, 0), repeat=10))
check(len(seqs) == 1024, P + ': 1,024 sequences')


def pr(seq, a):
    r = F(1)
    for s in seq:
        r *= a if s else 1 - a
    return r


A = [s for s in seqs if sum(s) >= 8]
PA = sum(pr(s, pw) for s in A)
check(PA == F(7, 128) and '\\tfrac{7}{128}' in items[P]['prose'], P + ': P(A) = 7/128')
L = {s: pr(s, pw) / pr(s, qw) for s in A}                    # dP/dQ on A
w8 = (pw / qw) ** 8 * ((1 - pw) / (1 - qw)) ** 2
check(all(L[s] == w8 for s in A if sum(s) == 8), P + ' part 1: weight of 8 wins')
num_part(P, 0, w8, 4, {
    'reversed': 1 / w8,
    'wins-only': (pw / qw) ** 8,
})
printed(P, 0, '0.625^8', '6.25', '0.1455', '2.5')
# part 2: E_Q[Y^2] summed under Q, against E_P[1_A dP/dQ] summed under P
m2_q = sum(pr(s, qw) * L[s] ** 2 for s in A)
m2_p = sum(pr(s, pw) * L[s] for s in A)
check(m2_q == m2_p, P + ' part 2: E_Q[Y^2] = E_P[1_A dP/dQ]')
check(sum(pr(s, qw) * L[s] for s in A) == PA, P + ' part 2: the estimator is unbiased')
wk = {k: float((pw / qw) ** k * ((1 - pw) / (1 - qw)) ** (10 - k)) for k in (8, 9, 10)}
check([round(wk[k], 5) for k in (8, 9, 10)] == [0.14552, 0.03638, 0.00909], P + ' part 2: printed weights')
eight_only = 45 * w8 / 1024
num_part(P, 1, m2_p, 5, {
    'no-weight': PA,
    'eight-only': eight_only,
}, also=((45 * 0.1455 + 10 * wk[9] + wk[10]) / 1024, (45 * 0.14552 + 10 * 0.03638 + 0.00909) / 1024))
printed(P, 1, '0.14552', '0.03638', '0.00909', '0.00676')
# the slip P(A) = 0.0546875 is an exact tie at the 5 places asked: its band should take both roundings
x = wrong_of(P, 1, 'no-weight')
for r5 in (0.05468, 0.05469):
    check(abs(r5 - x['value']) <= x['tol']['abs'] * (1 + 1e-9),
          f'{P} part 2: wrong "no-weight" is P(A) = 0.0546875, a tie at 5 places; its band {x["value"]} +-{x["tol"]["abs"]} refuses the rounding {r5}')
# part 3: relative error per draw
m2_used = 0.00676
rel = math.sqrt(m2_used - float(PA) ** 2) / float(PA)
rel_exact = math.sqrt(float(m2_p) - float(PA) ** 2) / float(PA)
check(round(rel, 2) == round(rel_exact, 2) == 1.12, P + ' part 3: rounded and exact inputs agree at 2 places')
num_part(P, 2, rel, 2, {
    'no-mean': math.sqrt(m2_used) / float(PA),
    'no-root': (m2_used - float(PA) ** 2) / float(PA) ** 2,
}, also=(rel_exact,))
check(round(float(PA) ** 2, 7) == 0.0029907 and round(m2_used - float(PA) ** 2, 7) == 0.0037693, P + ' part 3: printed figures')
check(round(math.sqrt(0.0037693), 5) == 0.06139 and round(m2_used - float(PA) ** 2, 6) == 0.003769, P + ' part 3: printed root')
printed(P, 2, '0.003769', '0.0546875', '0.0029907', '0.0037693', '0.06139', '0.00299', '1.12')
# part 4: draws
plain_sq = (1 - PA) / PA
check(plain_sq == F(121, 7), P + ' part 4: plain square 121/7')
ratio = float(plain_sq) / 1.12 ** 2
ratio_exact = float(plain_sq) / rel_exact ** 2
check(round(ratio) == round(ratio_exact) == 14, P + ' part 4: 14 with rounded and exact inputs')
# plain sampler's variance checked on the indicator itself
var_plain = PA * (1 - PA)
check(var_plain / PA ** 2 == plain_sq, P + ' part 4: plain relative error squared')
w3 = part(P, 3)['widget']
check(w3['answer'] == 14 and abs(ratio - 14) <= w3['tol']['abs'], P + ' part 4: key 14 takes 13.78')
ids = {x['id']: x for x in w3['wrong']}
check(set(ids) == {'not-squared', 'plain-only'}, P + ' part 4: wrong ids')
check(ids['not-squared']['value'] == round(math.sqrt(float(plain_sq)) / 1.12) == 4, P + ' part 4: slip not-squared')
check(ids['plain-only']['value'] == round(float(plain_sq)) == 17, P + ' part 4: slip plain-only')
for x in w3['wrong']:
    check(abs(x['value'] - 14) > w3['tol']['abs'] + x['tol']['abs'], P + ' part 4: slip band clear of the key')
check(round(math.sqrt(float(plain_sq)), 2) == 4.16 and round(float(plain_sq), 2) == 17.29 and round(1.12 ** 2, 4) == 1.2544, P + ' part 4: printed figures')
printed(P, 3, '17.29', '1.2544', '4.16', '\\tfrac{121}{7}')

# ---------------------------------------------------------------- p-premium-weight
P = 'p-premium-weight'
s0, su, sd, R, p = F(40), F(48), F(34), F(101, 100), F(3, 5)
q = (s0 * R - sd) / (su - sd)
check(q == F(16, 35) and q * su + (1 - q) * sd == s0 * R, P + ' part 1: q = 16/35 and the martingale equation')
num_part(P, 0, q, 4, {
    'no-cash': (s0 - sd) / (su - sd),
    'down': 1 - q,
})
printed(P, 0, '\\tfrac{16}{35}', '6.4', '40.4', '0.4571')
zu, zd = q / p, (1 - q) / (1 - p)
check(zu == F(16, 21) and zd == F(19, 14) and p * zu + (1 - p) * zd == 1, P + ' part 2: weights 16/21 and 19/14 with mean 1')
q_nocash = (s0 - sd) / (su - sd)
num_part(P, 1, zd, 4, {
    'up': zu,
    'inverse': 1 / zd,
    'no-cash': (1 - q_nocash) / (1 - p),
})
check(q_nocash == F(3, 7), P + ' part 2: the no-cash q is 3/7')
printed(P, 1, '\\tfrac{19}{14}', '\\tfrac{16}{21}', '\\tfrac37', '\\tfrac{19}{35}', '1.3571')
# part 3: covariance by the definition, then by E_Q[S_1] - E_P[S_1]
ezs = p * zu * su + (1 - p) * zd * sd
es = p * su + (1 - p) * sd
cov1 = p * (zu - 1) * (su - es) + (1 - p) * (zd - 1) * (sd - es)
check(ezs == F(404, 10) and es == F(424, 10) and cov1 == ezs - es == -2, P + ' part 3: covariance -2')
num_part(P, 2, cov1, 2, {
    'sign': -cov1,
    'no-mean': ezs,
}, also=(0.6 * 0.7619 * 48 + 0.4 * 1.3571 * 34 - 42.4,))
printed(P, 2, '40.4', '42.4', '-2.00')
# part 4: the identity for an arbitrary traded price; E_Q[Z_1] is E_P[Z_1^2]
for xu, xd in ((F(7), F(3)), (F(120), F(95)), (F(1), F(0))):
    x0 = (q * xu + (1 - q) * xd) / R                         # its arbitrage-free price
    lhs = p * zu * xu + (1 - p) * zd * xd
    check(lhs == R * x0, P + ' part 4: E_P[Z_1 X_1] = 1.01 X_0')
    check(lhs - (p * xu + (1 - p) * xd) == p * (zu - 1) * xu + (1 - p) * (zd - 1) * xd, P + ' part 4: covariance identity')
eqz = q * zu + (1 - q) * zd
check(eqz == p * zu ** 2 + (1 - p) * zd ** 2 and round(float(eqz), 3) == 1.085, P + ' part 4: E_Q[Z_1] = E_P[Z_1^2] = 1.085')
check(es - s0 * R == -cov1, P + ' part 4: the premium 2 is minus the covariance')
choice_key(P, 3, 'any')
printed(P, 3, '1.085', '42.4', '40.4')
# part 5: two steps, the share moving by the factors 48/40 and 34/40 at each step
fu, fd = su / s0, sd / s0
two = list(product('ud', repeat=2))
S2 = {t: S_end(t, s0, fu, fd) for t in two}
Z2 = {t: (zu if t[0] == 'u' else zd) * (zu if t[1] == 'u' else zd) for t in two}
ez2s2 = sum(prob(t, p) * Z2[t] * S2[t] for t in two)
es2 = sum(prob(t, p) * S2[t] for t in two)
ez2 = sum(prob(t, p) * Z2[t] for t in two)
cov2 = sum(prob(t, p) * (Z2[t] - 1) * (S2[t] - es2) for t in two)
check(ez2 == 1 and ez2s2 == s0 * R ** 2 == F(40804, 1000) and es2 == F(44944, 1000), P + ' part 5: the two means')
check(cov2 == ez2s2 - es2 == F(-414, 100), P + ' part 5: covariance -4.14')
check(min(Z2, key=Z2.get) == ('u', 'u') and es / s0 == F(106, 100), P + ' part 5: smallest weight on up, up; growth 1.06')
num_part(P, 4, cov2, 2, {
    'doubled': 2 * cov1,
    'sign': -cov2,
    'cash-once': s0 * R - es2,
})
printed(P, 4, '40.804', '44.944', '1.06', '-4.14')
# The value -4.14 needs the second step to repeat the factors 1.2 and 0.85. The prose gives one step in pounds only.
# An additive second step (48 to 56 or 42, 34 to 42 or 28) is a different tree with a different answer.
p5_text = items[P]['prose'] + ' ' + part(P, 4)['question']
check(re.search(r'factor|1\.2\b|0\.85|same proportion|multipl', p5_text) is not None,
      P + ' part 5: neither the prose nor the question says how the share moves at the second step (factors 1.2 and 0.85); the key -4.14 needs it')
q_up_add = (48 * R - 42) / (56 - 42)
check(q_up_add != q, P + ' part 5: on an additive second step the weights would not repeat')

# ---------------------------------------------------------------- restatements (chain)
check('part 4' in part('p-share-numeraire', 4)['question'].lower() or 'part 3' not in part('p-share-numeraire', 4)['question'].lower(),
      'p-share-numeraire part 5: the question credits the price line to part 3; part 4 found it')
for pid in items:
    for k in range(1, len(items[pid]['parts'])):
        qn = part(pid, k)['question']
        check(re.search(r'[Pp]art \d|Using|the stem|Its price is|Z = 2X\^2', qn) is not None, f'{pid} part {k + 1}: no restatement of an earlier value')

print(f'{n_checks} checks, {n_find} FINDING line(s)')
raise SystemExit(0)
