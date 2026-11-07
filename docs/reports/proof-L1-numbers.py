"""Second-read number and claim checks for proof level 1 (l1 to l5, review-1, homework-1).
Run from the repo root: python3 docs/reports/proof-L1-numbers.py  (exits 0 when every check passes).
Every graded key and wrong value is recomputed, and every "for all" or "there exists" claim on a grid,
table or range is brute-forced from the JSON itself. Checks tied to wording use lv.stated: they fail while
a false sentence is in the text and pass once it is reworded (review-proof-1-3.md says which).
"""
import itertools, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('proof', 1)


def num(s):
    return float(s.replace('−', '-').replace('£', '').replace('+', '').replace('%', '').replace(',', ''))


def imp(p, q):
    return (not p) or q


ROWS = [(True, True), (True, False), (False, True), (False, False)]
TF = lambda b: 'T' if b else 'F'

# ---------- l1 ----------
lv.expect('l1', 'screens[2].widget.answer', 91 // 7)
lv.claim(7 * 13 == 91 and 91 % 7 == 0, '91 = 7 x 13 (division and product)')
lv.claim([round(91 / d, 2) for d in (2, 3, 5)] == [45.5, 30.33, 18.2], 'l1 divisor table 45.5, 30.33, 18.2')
lv.claim(7 * 12 == 84 and 7 * 14 == 98, 'l1 wrong 12 and 14 lines: 84 and 98')
lv.claim(2 ** 10 == 1024 and 2 * 512 == 1024 and 1024 > 1000, '2^10 = 1024 > 1000, two ways')
lv.claim(3 * 19 == 57 and sum(map(int, '57')) == 12 and 27 == 3 * 9, '57 = 3 x 19, digit sum 12; 27 = 3 x 9')
lv.claim([x for x in range(0, 7) if x + 2 == 5] == [3], 'truth set of x + 2 = 5 on 0..6 is {3}')
lv.claim(0.1 + 0.2 != 0.3 and repr(0.1 + 0.2) == '0.30000000000000004', 'CPython 0.1 + 0.2 prints 0.30000000000000004 and != 0.3')
lv.claim(abs(9.8 / 61 - 0.1607) < 1e-3 and 9.8 / 61 > 0.10 and 4.1 / 52 < 0.10, 'l1 transfer: Rates 16% over 10%, Equities 7.9% under')
lv.claim(32400 < 50000 and 1240 > 1000, 'l1: £32,400 under £50,000; £1,240 over £1,000')
# Definition of prime (Hardy and Wright 1.2: p > 1 and no divisors but 1 and p). l14 says "1 is not prime".
lv.stated('l1', 'screens[2].prose', 'A prime has no whole-number divisors except 1 and itself', False)

# ---------- l2 ----------
d2 = lv.files[[k for k in lv.files if k.startswith('l2')][0]]
days = d2['screens'][0]['canvas']['params']['rows']
P = {r[0]: num(r[1]) > 100 for r in days}
Q = {r[0]: num(r[2]) > 1 for r in days}
order = [r[0] for r in days]
tap = lambda f: [f'r{i}' for i, dname in enumerate(order) if f(dname)]
lv.claim(d2['screens'][0]['widget']['answer'] == tap(lambda x: P[x] and Q[x]), 'l2 and-alert days Mon, Thu')
lv.claim(d2['screens'][1]['widget']['answer'] == tap(lambda x: P[x] or Q[x]), 'l2 or-alert days Mon to Thu')
lv.claim(d2['screens'][2]['widget']['answer'] == tap(lambda x: not P[x]), 'l2 not-alert days Tue, Fri')
lv.claim(d2['screens'][1]['widget']['wrong'][0]['set'] == tap(lambda x: P[x] != Q[x]), 'l2 exclusive-or slip = Tue, Wed')
lv.claim([[TF(P[x]), TF(Q[x])] for x in order] == [r[1:] for r in d2['screens'][3]['canvas']['params']['rows']], 'l2 P, Q columns match the price table')
for si, fs in ((3, (lambda p, q: p and q, lambda p, q: p or q)), (6, (lambda p, q: not (p and q), lambda p, q: (not p) or (not q)))):
    rows = d2['screens'][si]['widget']['rows']
    got = [[c['answer'] for c in r[2:]] for r in rows]
    lv.claim(got == [[TF(f(p, q)) for f in fs] for p, q in ROWS], f'l2 screens[{si}] truth table keys')
lv.claim(all((not (p or q)) == ((not p) and (not q)) for p, q in ROWS) and not all((not (p or q)) == ((not p) or (not q)) for p, q in ROWS), 'second De Morgan law holds; or-form fails')
lv.claim(not (True or False) is False and ((not True) or (not False)) is True, 'l2 why: on T, F row not(P or Q) F but (not P) or (not Q) T')
lv.claim(((not False) or True) is True and (not (False or True)) is False, 'l2 why: on F, T row (not P) or Q is T, not(P or Q) is F')
agree = sum((not (p and q)) == ((not p) and (not q)) for p, q in ROWS)
lv.expect('l2', 'quiz[0].widget.answer', agree)
lv.expect('l2', 'quiz[1].widget.answer', len(list(itertools.product([0, 1], repeat=3))))
lv.claim(2 ** 3 == 8 and 2 * 3 == 6 and 3 ** 2 == 9 and 4 + 1 == 5, 'l2 quiz rows 8; wrongs 6, 9, 5')
trades = d2['screens'][10]['widget']['rows']
lv.claim([r[3]['answer'] for r in trades] == [TF(num(r[1].replace('m', '')) > 1 or r[2] == 'unrated') for r in trades], 'l2 risk flags A, B, C T and D F')
# code screen: run solution and starter on all tests
w = d2['screens'][8]['widget']
for label, src in (('solution', w['solution']), ('starter', w['starter'])):
    res = []
    for t in w['tests']:
        g = {}
        exec(src, g)
        exec(t['setup'], g)
        res.append(eval(t['call'], g) == eval(t['expect']))
    lv.claim(all(res) if label == 'solution' else not all(res), f'l2 same_truth_table {label}: {sum(res)} of {len(res)} tests pass')
lv.claim([(lambda p, q: p or q)(p, q) == True for p, q in ROWS] == [True, True, True, False], 'l2 test-5 (p or q vs True) differs only on the F, F row')

# ---------- l3 ----------
d3 = lv.files[[k for k in lv.files if k.startswith('l3')][0]]
lv.claim([r[2]['answer'] for r in d3['screens'][1]['widget']['rows']] == [TF(imp(p, q)) for p, q in ROWS], 'l3 P => Q column T, F, T, T')
lv.claim([[c['answer'] for c in r[3:]] for r in d3['screens'][5]['widget']['rows']] == [[TF(imp(q, p)), TF(imp(not q, not p))] for p, q in ROWS], 'l3 converse and contrapositive columns')
lv.claim(all(imp(p, q) == imp(not q, not p) for p, q in ROWS) and all(imp(q, p) == imp(not p, not q) for p, q in ROWS), 'contrapositive agrees; inverse agrees with converse')
U = range(1, 13)
lv.claim([n for n in U if n % 4 == 0] == [4, 8, 12] and [n for n in U if n % 2 == 0 and n % 4] == [2, 6, 10], 'l3 venn 1..12: multiples of 4; even non-multiples 2, 6, 10')
lv.expect('l3', 'quiz[1].widget.answer', min(n for n in range(1, 100) if n % 2 == 0 and n % 4))
lv.claim(0 + 0 + 3 + 14 == 17, 'l3 quiet Monday counts add to 17')
# four-card task: brute force every hidden side; a card must be turned iff some hidden value breaks the rule
sizes, sigs = [12000, 3000], [2, 1]
must = [any(s > 10000 and g < 2 for g in (1, 2)) for s in sizes] + [any(s > 10000 and g < 2 for s in (12000, 3000)) for g in sigs]
lv.claim(must == [True, False, False, True], 'l3 four tickets: turn £12,000 and 1 signature only')
bal, stat = [18000, 40000], ['Blocked', 'Allowed']
must = [any(b < 25000 and s == 'Allowed' for s in stat) for b in bal] + [any(b < 25000 and s == 'Allowed' for b in bal) for s in stat]
lv.claim(must == [True, False, False, True], 'l3 transfer: turn £18,000 and Allowed only')
lv.claim([imp(p, q) and imp(q, p) for p, q in ROWS] == [True, False, False, True], 'l3 iff true on T, T and F, F')

# ---------- l4 ----------
d4 = lv.files[[k for k in lv.files if k.startswith('l4')][0]]
cells = [[num(c) for c in r] for r in d4['screens'][0]['canvas']['params']['cells']]
wit = [f'r{i + 1}c{j + 1}' for i, r in enumerate(cells) for j, v in enumerate(r) if v > 100]
lv.claim(d4['screens'][0]['widget']['answer'] == wit and all(sum(v > 100 for v in r) == 1 for r in cells), 'l4 one witness per trader above 100')
lv.claim(d4['screens'][0]['widget']['wrong'][0]['set'] == sorted([f'r{i + 1}c{j + 1}' for i, r in enumerate(cells) for j, v in enumerate(r) if v > 0], key=lambda s: (int(s[1]), int(s[3]))) and sum(v > 0 for r in cells for v in r) == 13, 'l4 all-profits slip: 13 positive cells')
lv.claim(all(any(v > 100 for v in r) for r in cells), 'claim A (forall t exists d) true')
lv.claim(not any(all(cells[i][j] > 100 for i in range(4)) for j in range(5)), 'claim B (exists d forall t) false')
lv.claim(max(sum(cells[i][j] > 100 for i in range(4)) for j in range(5)) == 2, 'l4 hint: each column has at most two values above 100')
lv.claim(sorted(d4['screens'][1]['widget']['among']) == sorted(f'r{i + 1}c4' for i in range(4) if cells[i][3] <= 100), 'l4 Thursday breakers T1 and T4')
low = d4['screens'][6]['explain']['canvas']['shade']['low']
lv.claim(all(cells[int(c[1]) - 1][int(c[3]) - 1] <= 100 for c in low) and sorted(int(c[3]) for c in low) == [1, 2, 3, 4, 5], 'l4 trap shading: one value <= 100 in each column')
marks = d4['screens'][9]['canvas']['state']['mark']
H = [[marks[f'r{h}c{s}']['text'] == '✓' for s in range(1, 5)] for h in range(1, 4)]
lv.claim(all(any(H[h][s] for h in range(3)) for s in range(4)) and not any(all(r) for r in H) and not H[0][1], 'l4 hedges: forall s exists h true; exists h forall s false; H1 fails rates down')
R = range(-2000, 2001)
lv.claim(all(n * n >= n for n in R), 'forall n in Z, n^2 >= n (brute force -2000..2000)')
lv.claim(not any(2 * n == 7 for n in R), 'no integer with 2n = 7')
lv.claim(all(any(m == 2 * n for m in (2 * n,)) for n in R) and not any(all(m == 2 * n for n in range(-5, 6)) for m in range(-20, 21)), 'forall n exists m = 2n true; exists m forall n false')
lv.claim(all(any(y > x for y in range(x - 2, x + 3)) for x in range(-500, 501)) and not any(all(y > x for x in range(-500, 501)) for y in range(-500, 501)), 'forall x exists y > x true; exists y forall x false (finite window)')
lv.claim(not any(x * x == 2 for x in range(-100, 101)) and abs(2 ** 0.5 - 1.414) < 1e-3, 'no integer squares to 2; sqrt 2 ~ 1.414')
lv.claim(3 ** 2 == 9 and 9 ** 2 == 81 and 4.5 ** 2 == 20.25, 'l4 witness quiz: 9, 81, 20.25')
lv.claim(all(x * x >= 0 for x in [i / 7 for i in range(-700, 701)]) and 0 * 0 == 0, 'x^2 >= 0 on a grid of reals; x = 0 breaks x^2 > 0')
lv.claim(all(False for _ in []) is True and any(True for _ in []) is False, 'empty domain: forall true, exists false')

# ---------- l5 ----------
d5 = lv.files[[k for k in lv.files if k.startswith('l5')][0]]
pl = [num(r[1]) for r in d5['screens'][0]['canvas']['params']['rows']]
lv.claim(sorted(d5['screens'][0]['widget']['among']) == [f'r{i}' for i, v in enumerate(pl) if not v > 0], 'l5 unprofitable trades T3 (£0) and T5 (-£80)')
lv.claim(min(pl) == -80 and -min(pl) < 500 and not any(-v > 500 for v in pl), 'l5 worst loss £80: no trade lost more than £500')
lv.claim(not any(v < 0 for i, v in enumerate(pl) if i != 4) and pl[2] == 0, 'l5 why: with T5 profitable, only T3 (£0) breaks the claim and nothing lost')
c5 = [[num(c) for c in r] for r in d5['screens'][3]['canvas']['params']['cells']]
lv.claim(c5 == cells and not any(all(v <= 100 for v in r) for r in c5), 'l5 negation of claim A false: every row has a value above 100')
lv.claim([x for x in range(0, 11) if not x < 5] == [x for x in range(0, 11) if x >= 5], 'not (x < 5) is x >= 5 on 0..10')
lv.claim(all((not (x <= 2 and y > 0)) == (x > 2 or y <= 0) for x in range(-5, 6) for y in range(-5, 6)), 'not(x <= 2 and y > 0) = x > 2 or y <= 0 (brute force)')
rows5 = [(r[1] == 'yes', r[2] == 'yes') for r in d5['screens'][5]['canvas']['params']['rows']]
lv.claim([not imp(p, q) for p, q in rows5] == [False, True, False, False] and imp(*rows5[3]) and imp(rows5[3][0], not rows5[3][1]), 'l5 trap: only Tuesday breaches; Thursday keeps both rules')
m5 = d5['screens'][9]['canvas']['state']['mark']
lv.claim([k for k, v in m5.items() if v['text'] == '×'] == ['r2c3'], 'l5 audit: one breach, Rates on Wednesday')

# ---------- review-1 ----------
r1 = lv.files['review-1']
lv.claim([c['answer'] for c in r1['items'][1]['widget']['rows'][0][2:]] == [TF(False and True), TF(False or True), TF(not False)], 'review-1 F, T row: and F, or T, not P T')
types, times = ['Market', 'Limit'], [1515, 1620]
must = [any(t == 'Market' and s >= 1600 for s in times) for t in types] + [any(t == 'Market' and s >= 1600 for t in types) for s in times]
lv.claim(must == [True, False, False, True] and r1['items'][2]['widget']['answer'] == ['mkt', 't420'], 'review-1 cards: turn Market and 4:20pm only')
wk = [[num(c) for c in r] for r in r1['items'][4]['canvas']['params']['cells']]
lv.claim(any(all(wk[s][w] > 0 for s in range(3)) for w in range(4)), 'review-1: a week where every stock rose (W3)')
lv.claim(all(any(v > 0 for v in r) for r in wk), 'review-1: every stock rose in some week')
lv.claim(not all(any(wk[s][w] > 0 for s in range(3)) for w in range(4)), 'review-1: in every week some stock rose is false (W2)')
lv.claim(not any(all(v > 0 for v in r) for r in wk), 'review-1: some stock rose every week is false')
lv.expect('review', 'items[5].widget.answer', 12 // 3)
lv.claim(12 * 3 == 36 and 12 - 3 == 9, 'review-1 wrongs 36 and 9')

# ---------- homework-1 ----------
h1 = lv.files['homework-1']
lv.claim([[c['answer'] for c in r[2:]] for r in h1['items'][0]['widget']['rows']] == [[TF(imp(q, p)), TF(imp(p, imp(q, p)))] for p, q in ROWS], 'homework-1 P => (Q => P) table, a tautology')
g = [[num(c) for c in r] for r in h1['items'][2]['canvas']['params']['cells']]
desks = {'A': (0, 1), 'B': (2, 3)}
witness = {k: [d for d in range(4) if all(g[t][d] > 0 for t in ts)] for k, ts in desks.items()}
lv.claim(witness == {'A': [2], 'B': [1]}, 'homework-1 desk A only Wednesday, desk B only Tuesday')
lv.claim(all(witness.values()), 'forall k exists d forall t: true')
lv.claim(not any(all(g[t][d] > 0 for t in range(4)) for d in range(4)), 'exists d forall k forall t: false')
lv.claim(all(any(g[t][d] > 0 for t in ts) for ts in desks.values() for d in range(4)), 'forall k forall d exists t: true')
lv.claim(not all(any(all(g[t][d] > 0 for d in range(4)) for t in ts) for ts in desks.values()), 'forall k exists t forall d: false')
lv.claim(imp(True, True) and [TF(imp(not q, not p)) for p, q in ROWS] == ['T', 'F', 'T', 'T'], 'homework-1 order: contrapositive reads T, F, T, T')
lv.claim(25 > 40 / 2 and 32.4 > 30, 'homework-1 model: £25m is more than half of £40m; VIX 32.4 > 30')

# Positional references to shuffled options (review-proof-1-3.md findings): pass once reworded.
lv.stated('l1', 'quiz[0].explain.text', 'Only the first sentence', False)
lv.stated('review', 'items[0].explain.text', 'Only the first line', False)
lv.stated('homework', 'items[3].feedback.correct', 'The first and third are true', False)


# ---------- fix pass: the new wording must be present (a revert fails these) ----------
def has(ref, path, phrase, present=True):
    t = lv.text(ref, path)
    lv.claim((phrase in t) == present, f'{ref} {path} {"has" if present else "lacks"} {phrase!r}')

has('l1', 'screens[2].prose', 'A prime is a whole number above 1 whose only whole-number divisors are 1 and itself')
lv.claim(91 > 1 and 91 % 7 == 0 and 91 // 7 == 13, 'fix pass: 91 is above 1 and has the divisor 7, so it is not prime')
has('l1', 'quiz[0].explain.text', 'the sentence about the median trade')
has('l1', 'screens[4].explain.text', "yesterday's loss was large")
has('l1', 'quiz[3].explain.text', '`0.30000000000000004`')
has('review', 'items[0].explain.text', 'giving the spread as 12 basis points')
has('review', 'items[6].prose', 'the fund beat its benchmark and stayed within its risk limit')
has('homework', 'items[3].feedback.correct', r'$\forall k\ \exists d\ \forall t$ and $\forall k\ \forall d\ \exists t$ are true')
has('l3', 'screens[9].widget.options[3].why', 'which this level comes back to')
has('l5', 'quiz[0].widget.options[2].why', 'turned “did not rise” into “fell”')
has('l5', 'screens[9].widget.options[1].why', 'You kept “every day”. The negation needs only some day.')
has('homework', 'items[5].explain.text', r'for some $\varepsilon$, however late we start, a later term lies at least $\varepsilon$ from $L$')
has('l3', 'quiz[2].widget.options[0].text', 'T, T and F, F')
lv.claim(all(imp(P, Q) == ((not P) or Q) for P, Q in ROWS) and [not (P and Q) for P, Q in ROWS] == [False, True, True, True], 'review-1 De Morgan item: not (P and Q) is true on three rows, as "not P or not Q"')
lv.claim(all((not (P and Q)) == ((not P) or (not Q)) and (not (P and Q)) != ((not P) and (not Q)) for P, Q in [(True, False), (False, True)]), 'review-1 distractor "and" differs from "or" on the middle rows')

lv.check_wrongs()
lv.report()
