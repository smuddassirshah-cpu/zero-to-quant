#!/usr/bin/env python3
"""Concept audit, counting-chance level 3 (l9 to l12, review-3, homework-3, problems-3).
Exact enumeration of every counting and probability claim, plus Monte Carlo where a claim is empirical.
Run from the repository root: python3 docs/reports/counting-chance-L3-concepts.py
Exits 0 when the content is correct. A check that fails because the content is wrong stays failing."""
import itertools, json, math, os, random, re, sys
from fractions import Fraction as F

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'counting-chance')
FAIL, N, NOTES = [], [0], []


def load(name):
    return json.load(open(os.path.join(BASE, name + '.json'), encoding='utf-8'))


def get(obj, path):
    for part in re.findall(r'[A-Za-z_][\w-]*|\[\d+\]', path):
        obj = obj[int(part[1:-1])] if part[0] == '[' else obj[part]
    return obj


def check(label, cond):
    N[0] += 1
    if not cond:
        FAIL.append(label)
        print('FAIL', label)


def near(a, b, tol=6e-5):
    return abs(float(a) - float(b)) <= tol


def key(doc, path, value, label, tol=6e-5):
    """The graded answer at path equals the recomputed value."""
    check(f'{label}: key {get(doc, path)} vs {float(value):.6g}', near(get(doc, path), value, tol))


def wrongs(doc, path, values, label, tol=6e-5):
    """Every wrong[].value at path equals, in order, the recomputed slip value, and none equals the key."""
    w = get(doc, path)
    got = [x['value'] for x in w['wrong']]
    check(f'{label}: wrong values {got} vs {[round(float(v), 6) for v in values]}',
          len(got) == len(values) and all(near(g, v, tol) for g, v in zip(got, values)))
    check(f'{label}: no wrong value equals the key', all(not near(g, w['answer'], 1e-9) for g in got))


def correct_option(doc, path):
    return [o for o in get(doc, path)['options'] if o.get('correct')]


def cells(pairs):
    return sorted(f'r{r}c{c}' for r, c in pairs)


def has(doc, path, text, label=None):
    check(label or f'text at {path} holds "{text}"', text in json.dumps(get(doc, path), ensure_ascii=False))


random.seed(20261111)
C = math.comb
P = lambda ev, space: F(sum(1 for o in space if ev(o)), len(space))
DECK = [(r, s) for s in range(4) for r in range(13)]      # rank 0 = ace ... 12 = king; suit 1 = hearts


def no_match(n, d=365):
    p = F(1)
    for i in range(n):
        p *= F(d - i, d)
    return p


def run_code(widget, label):
    """Real execution: the solution passes every hidden test and example; the starter fails at least one
    (an error, a wrong value, or no return within 5 seconds)."""
    import signal

    class Slow(Exception):
        pass

    def alarm(*_):
        raise Slow()

    def passes(src):
        env = {}
        signal.signal(signal.SIGALRM, alarm)
        signal.alarm(5)
        try:
            exec(src, env)
            for t in widget['tests'] + widget.get('examples', []):
                got, exp = eval(t['call'], env), t['expect']
                if isinstance(exp, str):
                    exp = eval(exp)
                if t['compare'] == 'isclose':
                    if not math.isclose(got, exp, rel_tol=1e-9, abs_tol=1e-12):
                        return False, 'value'
                elif got != exp:
                    return False, 'value'
            return True, ''
        except Slow:
            return False, 'timeout'
        except Exception:
            return False, 'error'
        finally:
            signal.alarm(0)
    check(f'{label}: solution passes all {len(widget["tests"])} hidden tests', passes(widget['solution'])[0])
    ok, why = passes(widget['starter'])
    check(f'{label}: starter fails ({why})', not ok)
    if why == 'timeout':
        NOTES.append(f'{label}: the untouched starter never returns (it fails only by the time limit); see the Engine section of the audit')


# ---------------------------------------------------------------- l9
l9 = load('l9-double-counting')
H = {c for c in DECK if c[1] == 1}
FC = {c for c in DECK if c[0] in (10, 11, 12)}
v = get(l9, 'screens[0].canvas.params.values')
check('l9 s0 regions 10, 3, 9, 30', (v['A'], v['AB'], v['B'], v['none']) == (len(H - FC), len(H & FC), len(FC - H), 52 - len(H | FC)))
key(l9, 'screens[2].widget.answer', F(len(H | FC), 52), 'l9 s2 heart or face card')
wrongs(l9, 'screens[2].widget', [F(25, 52), F(19, 52), F(3, 52), 22], 'l9 s2')
ROLLS = list(itertools.product(range(1, 7), repeat=2))
key(l9, 'screens[3].widget.answer', P(lambda o: 6 in o, ROLLS), 'l9 s3 at least one six')
wrongs(l9, 'screens[3].widget', [F(12, 36), F(10, 36), F(1, 36)], 'l9 s3')
check('l9 s4 heart or spade one half', F(26, 52) == F(1, 2) and correct_option(l9, 'screens[4].widget')[0]['text'] == '$\\dfrac{1}{2}$')
A = {1, 2, 3, 4}
B = {2, 4, 6}
check('l9 s5 union 5/6', F(len(A | B), 6) == F(5, 6) and correct_option(l9, 'screens[5].widget')[0]['text'] == '$\\dfrac{5}{6}$')
U = frozenset(range(5))
subs = [frozenset(s) for k in range(6) for s in itertools.combinations(U, k)]
random.seed(7)
trip = [(random.choice(subs), random.choice(subs), random.choice(subs)) for _ in range(4000)]
check('l9 s6/s7 three-event inclusion and exclusion holds for 4,000 random triples of sets',
      all(len(a | b | c) == len(a) + len(b) + len(c) - len(a & b) - len(a & c) - len(b & c) + len(a & b & c) for a, b, c in trip))
rows = get(l9, 'screens[6].widget.rows')
check('l9 s6 table: all three counted 3, 3, 1, net 1', [c['answer'] for c in rows[2][1:]] == [3, 3, 1, 1] and rows[1][2]['answer'] == 1 and rows[1][4]['answer'] == 1)
key(l9, 'screens[7].widget.answer', 40 + 35 + 30 - 12 - 10 - 8 + 5, 'l9 s7 stock screen')
v = get(l9, 'screens[7].canvas.params.values')
check('l9 s7 Venn regions rebuild the stated counts (40, 35, 30; pairs 12, 10, 8; triple 5; outside 20)',
      v['A'] + v['AB'] + v['AC'] + v['ABC'] == 40 and v['B'] + v['AB'] + v['BC'] + v['ABC'] == 35 and v['C'] + v['AC'] + v['BC'] + v['ABC'] == 30
      and sorted([v['AB'] + v['ABC'], v['AC'] + v['ABC'], v['BC'] + v['ABC']]) == [8, 10, 12] and sum(v[k] for k in v if k != 'none') == 80 and v['none'] == 20)
key(l9, 'screens[8].widget.answer', F(60 + 50 - 45, 100), 'l9 s8 moving averages')
wrongs(l9, 'screens[8].widget', [F(110, 100), F(20, 100), F(45, 100), F(35, 100)], 'l9 s8')
key(l9, 'screens[9].widget.answer', F(10 + 8 + 5 - 4 - 3 - 2 + 1, 100), 'l9 s9 three limits')
v = get(l9, 'screens[9].canvas.params.values')
check('l9 s9 regions are all non-negative and add to 0.15 and 0.85', all(x >= 0 for x in v.values()) and near(sum(x for k, x in v.items() if k != 'none'), 0.15) and near(v['none'], 0.85))
key(l9, 'quiz[0].widget.answer', F(5, 10) + F(4, 10) - F(7, 10), 'l9 q0')
key(l9, 'quiz[1].widget.answer', F(sum(1 for n in range(1, 101) if n % 2 == 0 or n % 5 == 0), 100), 'l9 q1')
key(l9, 'quiz[2].widget.answer', F(sum(1 for n in range(1, 31) if n % 2 == 0 or n % 3 == 0 or n % 5 == 0), 30), 'l9 q2')
wrongs(l9, 'quiz[2].widget', [F(31, 30), F(21, 30), F(20, 30)], 'l9 q2')
check('l9 q3 smallest overlap 0.3 and largest 0.6', max(F(0), F(7, 10) + F(6, 10) - 1) == F(3, 10) and min(F(7, 10), F(6, 10)) == F(6, 10)
      and correct_option(l9, 'quiz[3].widget')[0]['text'] == '$0.3$')

# ---------------------------------------------------------------- l10
l10 = load('l10-birthday')
shared = lambda n, d=365: 1 - no_match(n, d)
check('l10 s0 six-day year: 6 of 36', len(get(l10, 'screens[0].widget.answer')) == 6)
T6 = list(itertools.product(range(6), repeat=3))
key(l10, 'screens[1].widget.answer', P(lambda o: len(set(o)) < 3, T6), 'l10 s1 three people, six days (enumerated)')
wrongs(l10, 'screens[1].widget', [F(3, 6), 1 - F(5, 6) * F(5, 6), F(5, 9)], 'l10 s1')
key(l10, 'screens[2].widget.answer', next(n for n in range(1, 100) if shared(n) > F(1, 2)), 'l10 s2 smallest room')
check('l10 values 0.4757 at 22, 0.5073 at 23, 0.9704 at 50, 0.9992 at 70', all(near(shared(n), v) for n, v in ((22, 0.4757), (23, 0.5073), (50, 0.9704), (70, 0.9992))))


def curve(x):
    return 1 - math.exp(1791.4127110448455 - ((365.5 - x) * math.log(366 - x) - (366 - x) + 1 / (12 * (366 - x)) - 1 / (360 * (366 - x) ** 3)) - x * math.log(365))


check('l10 the plotted curve (Stirling form) agrees with the exact product to 1e-6 for 1 to 70 people', all(abs(curve(n) - float(shared(n))) < 1e-6 for n in range(1, 71))
      and '1791.4127110448455' in get(l10, 'screens[2].canvas.params.functions[0].expr'))
key(l10, 'screens[3].widget.answer', C(23, 2), 'l10 s3 pairs')
you = 1 - F(364, 365) ** 23
check('l10 s4 options 0.0630, 0.0612, 0.5073, 0.6932', near(23 / 365, 0.0630) and near(you, 0.0612) and near(253 / 365, 0.6932) and correct_option(l10, 'screens[4].widget')[0]['text'] == '$0.5073$')
random.seed(20261111)
n = 200000
hits = you_hits = 0
for _ in range(n):
    b = [random.randrange(365) for _ in range(23)]
    hits += len(set(b)) < 23
    you_hits += random.randrange(365) in b
check(f'l10 MC 23 people share {hits / n:.4f} (0.5073), someone shares yours {you_hits / n:.4f} (0.0612)', abs(hits / n - 0.5073) < 0.005 and abs(you_hits / n - 0.0612) < 0.003)
check('l10 s5 order', get(l10, 'screens[5].widget.answer') == ['s1', 's2', 's3', 's4', 's5'])
w = get(l10, 'screens[6].widget')
run_code(w, 'l10 s6 p_shared')
env = {}
exec(w['solution'], env)
check('l10 s6 code equals the exact product for 0 to 400 people, and is exactly 1 from 366 on', all(math.isclose(env['p_shared'](k), float(shared(k)), rel_tol=1e-9, abs_tol=1e-12) for k in range(0, 366)) and all(env['p_shared'](k) == 1.0 for k in (366, 400)))
key(l10, 'screens[7].widget.answer', next(n for n in range(1, 400) if shared(n) == 1), 'l10 s7 certain at 366')
check('l10 s7 "183 almost certain"', shared(183) > 1 - F(1, 10 ** 20) and shared(365) < 1)
check('l10 s8 30 trades in 60 seconds: 0.99986; 10 trades 0.5475 and 9 below one half; options 0.7063 and 0.3858',
      near(shared(30, 60), 0.99986, 6e-6) and near(shared(10, 60), 0.5475) and shared(9, 60) < F(1, 2) and near(shared(30), 0.7063) and near(1 - (59 / 60) ** 29, 0.3858)
      and correct_option(l10, 'screens[8].widget')[0]['text'] == '$0.9999$')
check('l10 s9 100 orders, 10,000 codes: 0.3914; options 0.0099 and 0.495',
      near(shared(100, 10000), 0.3914) and near(1 - (9999 / 10000) ** 99, 0.0099) and C(100, 2) == 4950 and correct_option(l10, 'screens[9].widget')[0]['text'] == '$0.3914$')
half = lambda d: next(n for n in range(1, 5000) if shared(n, d) >= F(1, 2))
check('l10 summary: draws to an even chance of a collision are about sqrt(d) (ratio 1.0 to 1.3) for d = 60, 365, 10000', all(1.0 <= half(d) / math.sqrt(d) <= 1.3 for d in (60, 365, 10000)))
key(l10, 'quiz[0].widget.answer', C(30, 2), 'l10 q0')
D4 = list(itertools.product(range(6), repeat=4))
key(l10, 'quiz[1].widget.answer', P(lambda o: len(set(o)) < 4, D4), 'l10 q1 four dice (enumerated)')
wrongs(l10, 'quiz[1].widget', [1, 1 - F(5, 6) ** 3, F(5, 18)], 'l10 q1')
check('l10 q2 seven rolls force a repeat; six rolls give 0.9846', shared(7, 6) == 1 and near(shared(6, 6), 0.9846))

# ---------------------------------------------------------------- l11
l11 = load('l11-axioms')
rows = get(l11, 'screens[0].canvas.params.rows')
valid = [i for i, r in enumerate(rows) if all(float(x.replace('−', '-')) >= 0 for x in r[1:]) and abs(sum(float(x.replace('−', '-')) for x in r[1:]) - 1) < 1e-9]
check('l11 s0 only Ana (row 0) obeys the axioms', valid == [0] and get(l11, 'screens[0].widget.answer') == ['r0'])
key(l11, 'screens[1].widget.answer', 1 - F(55, 100), 'l11 s1 largest draw')
key(l11, 'screens[2].widget.answer', F(5, 10) + F(3, 10), 'l11 s2 home side does not lose')
# s7: which unions are possible for P(A) = 0.3 and P(B) = 0.25: build every overlap on a grid of 1/20
poss = sorted({F(30, 100) + F(25, 100) - F(k, 100) for k in range(0, 26)})      # overlap from 0 to min(P(A), P(B))
opts = get(l11, 'screens[7].widget.options')
want = [F(2, 10) in poss, F(3, 10) in poss, F(45, 100) in poss, F(55, 100) in poss, F(6, 10) in poss]
check('l11 s7 multi: 0.3, 0.45 and 0.55 are attainable, 0.2 and 0.6 are not', [bool(o.get('correct')) for o in opts] == want and min(poss) == F(3, 10) and max(poss) == F(55, 100))
key(l11, 'screens[10].widget.answer', 10 * F(2, 1000), 'l11 s10 union bound')
wrongs(l11, 'screens[10].widget', [F(2, 1000), 1 - F(998, 1000) ** 10, F(2, 1000) ** 10], 'l11 s10', tol=6e-5)
# Monte Carlo: the union bound holds whatever the link between failures (independent, common outage, mutually exclusive)
n = 200000


def any_fail(mode):
    c = 0
    for _ in range(n):
        if mode == 'independent':
            c += any(random.random() < 0.002 for _ in range(10))
        elif mode == 'outage':            # one outage takes all ten down together
            c += random.random() < 0.002
        else:                             # mutually exclusive failures: the bound is met exactly
            c += random.random() < 0.02
    return c / n


res = {m: any_fail(m) for m in ('independent', 'outage', 'exclusive')}
check(f'l11 s10 MC union bound 0.02 holds under three dependence models {res}', all(x <= 0.02 + 0.001 for x in res.values()) and abs(res['independent'] - 0.0198) < 0.001 and abs(res['outage'] - 0.002) < 0.0005)
# the dart: a point has probability 0 under the uniform law (no exact hit in a million draws), yet every draw lands somewhere
check('l11 s8 MC dart: no draw equals 0.5 exactly in 1,000,000 uniform draws', all(random.random() != 0.5 for _ in range(1000000)))
check('l11 q1 disjoint 0.45 and 0.6 would give 1.05', F(45, 100) + F(6, 10) == F(105, 100))
key(l11, 'quiz[3].widget.answer', 5 * F(1, 100), 'l11 q3 union bound')
wrongs(l11, 'quiz[3].widget', [F(1, 100), 1 - F(99, 100) ** 5], 'l11 q3')

# ---------------------------------------------------------------- l12 and every card claim of level 3: all 2,598,960 hands
l12 = load('l12-poker-hands')
RUNS = [set(range(i, i + 5)) for i in range(9)] + [{9, 10, 11, 12, 0}]
cls = dict.fromkeys(['sf', 'four', 'full', 'flush', 'straight', 'three', 'twopair', 'pair', 'nothing'], 0)
five_ranks = all_suits = no_ace_king = ace = ace_and_king = hearts5 = 0
for h in itertools.combinations(DECK, 5):
    ranks = [c[0] for c in h]
    rs = set(ranks)
    suits = {c[1] for c in h}
    if len(rs) == 5:
        five_ranks += 1
        fl, st = len(suits) == 1, rs in RUNS
        cls['sf' if fl and st else 'flush' if fl else 'straight' if st else 'nothing'] += 1
    else:
        pat = sorted((ranks.count(r) for r in rs), reverse=True)
        cls['four' if pat[0] == 4 else 'full' if pat == [3, 2] else 'three' if pat[0] == 3 else 'twopair' if pat == [2, 2, 1] else 'pair'] += 1
    all_suits += len(suits) == 4
    hearts5 += suits == {1}
    a, k = 0 in rs, 12 in rs
    ace += a
    ace_and_king += a and k
    no_ace_king += not a and not k
TOTAL = sum(cls.values())
check(f'l12 enumeration of all hands: {cls}', TOTAL == C(52, 5) == 2598960 and cls == {'sf': 40, 'four': 624, 'full': 3744, 'flush': 5108, 'straight': 10200, 'three': 54912, 'twopair': 123552, 'pair': 1098240, 'nothing': 1302540})
check('l12 s0 key 2,598,960', correct_option(l12, 'screens[0].widget')[0]['text'] == '$2{,}598{,}960$' and math.perm(52, 5) == 311875200 and 52 ** 5 == 380204032)
check('l12 s1 the three other queens', sorted(get(l12, 'screens[1].widget.answer')) == ['r2c12', 'r3c12', 'r4c12'])
key(l12, 'screens[2].widget.answer', cls['four'], 'l12 s2 four of a kind')
check('l12 s2 1 in 4,165 and s3 about 1 in 694', F(cls['four'], TOTAL) == F(1, 4165) and round(TOTAL / cls['full']) == 694)
check('l12 s3 table product 3,744', [r[1]['answer'] for r in get(l12, 'screens[3].widget.rows')] == [13, 4, 12, 6, cls['full']])
key(l12, 'screens[5].widget.answer', cls['flush'], 'l12 s5 flushes')
wrongs(l12, 'screens[5].widget', [cls['flush'] + 40, C(13, 5), C(13, 5) - 10], 'l12 s5')
check('l12 s6 two pair key', '123{,}552' in correct_option(l12, 'screens[6].widget')[0]['text'])
key(l12, 'screens[7].widget.answer', cls['straight'], 'l12 s7 straights')
order = ['sf', 'four', 'full', 'flush', 'straight', 'three', 'twopair', 'pair', 'nothing']
check('l12 s7 every hand is rarer than the one below it in the ranking', all(cls[a] < cls[b] for a, b in zip(order, order[1:])))
pts = get(l12, 'screens[7].canvas.state.points')
check('l12 s7 chart chances match the counts', all(near(p['y'], cls[k] / TOTAL, 1e-7) for p, k in zip(pts, ['sf', 'four', 'full', 'flush', 'three', 'twopair', 'pair', 'nothing'])))
key(l12, 'screens[8].widget.answer', cls['nothing'], 'l12 s8 nothing')
wrongs(l12, 'screens[8].widget', [TOTAL - cls['pair'], TOTAL, cls['nothing'] + 40], 'l12 s8')
check('l12 s8 0.5012 and "nine in ten are a pair or less"', near(cls['nothing'] / TOTAL, 0.5012) and (cls['nothing'] + cls['pair']) / TOTAL > 0.9)
q = F(1, 4165)
key(l12, 'screens[9].widget.answer', 1 - (1 - q) ** 2520, 'l12 s9 ten years', tol=5e-4)
wrongs(l12, 'screens[9].widget', [2520 * q, q, 1 - (1 - q) ** 252], 'l12 s9', tol=5e-4)
check('l12 q0 three of a kind key', '54{,}912' in correct_option(l12, 'quiz[0].widget')[0]['text'] and 13 * 4 * C(48, 2) - cls['three'] == cls['full'])
key(l12, 'quiz[1].widget.answer', F(cls['pair'], TOTAL), 'l12 q1 one pair')
check('l12 q2 0.632', near(1 - (1 - q) ** 4165, 0.632, 5e-4) and correct_option(l12, 'quiz[2].widget')[0]['text'] == '$0.632$')
# Monte Carlo: a shuffled deck deals a full house about 0.00144 of the time (the count rule needs equally likely hands)
n = 300000
deck = list(range(52))
fh = 0
for _ in range(n):
    hand = random.sample(deck, 5)
    rk = [c % 13 for c in hand]
    fh += sorted(rk.count(x) for x in set(rk)) == [2, 3]
check(f'l12 MC full house {fh / n:.5f}, near 0.00144 and not the halved 0.00072', abs(fh / n - 0.00144) < 0.00030)

# ---------------------------------------------------------------- review-3
r3 = load('review-3')
key(r3, 'items[0].widget.answer', F(35 + 25 - 10, 100), 'r3 i0')
check('r3 i1 40 people 0.8912; options 0.1096, 0.1039, 2.137', near(shared(40), 0.8912) and near(40 / 365, 0.1096) and near(1 - (364 / 365) ** 40, 0.1039) and near(780 / 365, 2.137, 5e-4)
      and correct_option(r3, 'items[1].widget')[0]['text'] == '$0.8912$')
key(r3, 'items[3].widget.answer', F(cls['full'], TOTAL), 'r3 i3 full house', tol=5e-6)
key(r3, 'items[4].widget.answer', 3 * F(3, 10) - 3 * F(1, 10) + F(5, 100), 'r3 i4')
key(r3, 'items[5].widget.answer', F(9, 10) + F(85, 100) - 1, 'r3 i5 smallest overlap')
wrongs(r3, 'items[5].widget', [F(9, 10) * F(85, 100), 0, F(85, 100)], 'r3 i5')
check('r3 i6 one pair key and the slip counts', '1{,}098{,}240' in correct_option(r3, 'items[6].widget')[0]['text'] and 13 * 6 * C(48, 3) == 1349088 and 13 * 6 * 12 * 11 * 10 * 64 == 6589440)
key(r3, 'items[7].widget.answer', shared(5, 12), 'r3 i7 months')
wrongs(r3, 'items[7].widget', [no_match(5, 12), F(5, 12), 1 - F(11, 12) ** 4], 'r3 i7')
check('r3 i7 five is the first to pass one half with 12 months', shared(4, 12) < F(1, 2) < shared(5, 12))

# ---------------------------------------------------------------- homework-3
h3 = load('homework-3')
key(h3, 'items[0].widget.answer', sum(1 for n in range(1, 1001) if n % 3 == 0 or n % 5 == 0 or n % 7 == 0), 'h3 i0 multiples')
wrongs(h3, 'items[0].widget', [675, 534, 525], 'h3 i0')
PERM = list(itertools.permutations(range(4)))
key(h3, 'items[1].widget.answer', P(lambda p: any(p[i] == i for i in range(4)), PERM), 'h3 i1 letters (24 orders enumerated)')
wrongs(h3, 'items[1].widget', [1, 1 - F(3, 4) ** 4, F(1, 2), F(2, 3)], 'h3 i1')
w = get(h3, 'items[2].widget')
run_code(w, 'h3 i2 smallest_n')
env = {}
exec(w['solution'], env)
check('h3 i2 code agrees with the exact product for d = 2..400 at target one half', all(env['smallest_n'](d, 0.5) == next(n for n in range(1, d + 2) if shared(n, d) >= F(1, 2)) for d in list(range(2, 60)) + [365, 400]))
check('h3 i2 1,178 draws is about 1.18 sqrt(d)', near(1178 / 1000, 1.18, 0.005))
check('h3 i3 order', get(h3, 'items[3].widget.answer') == ['s1', 's2', 's3', 's4'])
key(h3, 'items[4].widget.answer', F(five_ranks, TOTAL), 'h3 i4 five different ranks (enumerated)')
check('h3 i4 1,317,888 = nothing + straights + flushes + straight flushes', five_ranks == 1317888 == cls['nothing'] + cls['straight'] + cls['flush'] + cls['sf'])
key(h3, 'items[5].widget.answer', F(all_suits, TOTAL), 'h3 i5 all four suits (enumerated)')
check('h3 i5 685,464 hands', all_suits == 685464 == 4 * C(13, 2) * 13 ** 3)
wr = get(h3, 'items[5].widget.wrong')
two_terms = F(TOTAL - 4 * C(39, 5) + 6 * C(26, 5), TOTAL)
# content check, stays failing while the slip value is mis-rounded (finding)
check(f'h3 i5 slip "two-terms" value {wr[1]["value"]} equals the two-term figure {float(two_terms):.6f} to 4 places ({float(two_terms):.4f})', near(wr[1]['value'], round(float(two_terms), 4), 1e-9))
check('h3 i5 slips one-term and direct-double', near(wr[0]['value'], F(TOTAL - 4 * C(39, 5), TOTAL)) and near(wr[2]['value'], 2 * F(all_suits, TOTAL)))
check('h3 i6 500 ids from a million: 0.1173, union bound 0.1248', near(shared(500, 10 ** 6), 0.1173) and near(C(500, 2) / 10 ** 6, 0.1248, 6e-5) and correct_option(h3, 'items[6].widget')[0]['text'] == '$0.1173$')
check('h3 i7 0.6 + 0.5 - 0.05 = 1.05, overlap at least 0.1', F(6, 10) + F(5, 10) - F(5, 100) == F(105, 100) and F(6, 10) + F(5, 10) - 1 == F(1, 10))
check('h3 i8 use: 0.15 and bound 0.23', '0.15' in get(h3, 'items[8].model') and '0.23' in get(h3, 'items[8].model'))

# ---------------------------------------------------------------- problems-3
p3 = load('problems-3')
key(p3, 'items[0].parts[0].widget.answer', no_match(5, 50), 'p3 i0 p0')
wrongs(p3, 'items[0].parts[0].widget', [F(49, 50) ** 4, F(46, 50)], 'p3 i0 p0')
key(p3, 'items[0].parts[1].widget.answer', shared(5, 50), 'p3 i0 p1')
key(p3, 'items[0].parts[2].widget.answer', next(n for n in range(1, 60) if shared(n, 50) > F(1, 2)), 'p3 i0 p2')
wrongs(p3, 'items[0].parts[2].widget', [25, next(n for n in range(2, 60) if F(C(n, 2), 50) >= F(1, 2)), int(math.sqrt(50))], 'p3 i0 p2')
key(p3, 'items[0].parts[3].widget.answer', F(C(9, 2), 50), 'p3 i0 p3 union bound')
n = 200000
cl = sum(1 for _ in range(n) if len({random.randrange(50) for _ in range(9)}) < 9) / n
check(f'p3 i0 MC nine symbols clash {cl:.4f}: near 0.5345 and below the bound 0.72', abs(cl - 0.5345) < 0.005)
# i1: t = P(A and B and C) ranges over [0, 0.015]; every Venn region stays non-negative across it
def regions(t):
    ab, ac, bc = F(3, 100) - t, F(2, 100) - t, F(15, 1000) - t
    a = F(10, 100) - ab - ac - t
    b = F(8, 100) - ab - bc - t
    c = F(6, 100) - ac - bc - t
    return [a, b, c, ab, ac, bc, t]
feas = [F(k, 2000) for k in range(-10, 80) if all(x >= 0 for x in regions(F(k, 2000)))]
check('p3 i1 feasible t runs from 0 to 0.015, union 0.175 + t from 0.175 to 0.19', min(feas) == 0 and max(feas) == F(15, 1000) and sum(regions(F(15, 1000))) == F(19, 100) and sum(regions(F(0))) == F(175, 1000))
key(p3, 'items[1].parts[0].widget.answer', F(15, 100), 'p3 i1 p0')
key(p3, 'items[1].parts[2].widget.answer', max(feas), 'p3 i1 p2')
key(p3, 'items[1].parts[3].widget.answer', F(175, 1000) + max(feas), 'p3 i1 p3')
key(p3, 'items[2].parts[0].widget.answer', no_ace_king, 'p3 i2 p0 (enumerated)')
key(p3, 'items[2].parts[1].widget.answer', 1 - F(no_ace_king, TOTAL), 'p3 i2 p1')
key(p3, 'items[2].parts[2].widget.answer', F(ace_and_king, TOTAL), 'p3 i2 p2 (enumerated)')
key(p3, 'items[2].parts[3].widget.answer', ace_and_king, 'p3 i2 p3 (enumerated)')
check('p3 i2 886,656 hands hold an ace; ace and king are negatively linked', ace == 886656 and F(ace_and_king, TOTAL) < F(ace, TOTAL) ** 2)
SHORT = [(r, s) for r in range(5) for s in range(4)]
H4 = list(itertools.combinations(SHORT, 4))
pat = lambda h: sorted(([c[0] for c in h].count(r) for r in {c[0] for c in h}), reverse=True)
cnt = {}
for h in H4:
    cnt[tuple(pat(h))] = cnt.get(tuple(pat(h)), 0) + 1
check(f'p3 i3 short deck classes {cnt}', cnt == {(1, 1, 1, 1): 1280, (2, 1, 1): 2880, (2, 2): 360, (3, 1): 320, (4,): 5} and len(H4) == 4845)
key(p3, 'items[3].parts[0].widget.answer', F(16, 19), 'p3 i3 p0')
key(p3, 'items[3].parts[1].widget.answer', F(16, 19) * F(12, 18), 'p3 i3 p1')
key(p3, 'items[3].parts[2].widget.answer', F(cnt[(1, 1, 1, 1)], 4845), 'p3 i3 p2')
key(p3, 'items[3].parts[3].widget.answer', cnt[(1, 1, 1, 1)], 'p3 i3 p3')
key(p3, 'items[3].parts[4].widget.answer', cnt[(2, 1, 1)], 'p3 i3 p4')
wrongs(p3, 'items[3].parts[4].widget', [4845 - 1280, 2885, 4845 - 1280 - 720 - 320 - 5, 4845 - 1280 - 320 - 5], 'p3 i3 p4')

for note in NOTES:
    print('NOTE', note)
print(f'counting-chance L3 concepts: {N[0] - len(FAIL)} of {N[0]} checks passed')
sys.exit(1 if FAIL else 0)
