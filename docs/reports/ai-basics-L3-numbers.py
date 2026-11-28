"""Number check for ai-basics level 3 (l9 to l12, review-3, homework-3, problems-3).
Method A: each weighted sum in exact fractions, input by input. Method B: the same sum as the bias plus the sum of the
weights of the inputs that are 1 (a subset sum, no multiplication), computed separately. Every firing set, truth table
and count is built from both. The XOR impossibility is checked by brute force over the 0.5 grid from -5 to 5 (method A)
and by the inequality argument's conclusion on a random sample of 20,000 real neurons (method B). Code widgets run their
own solutions in CPython; each starter must fail a test.
Run: python3 docs/reports/ai-basics-L3-numbers.py   (exits 0 when every check passes)
"""
import itertools
import os
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, ZQ_LIB

lv = Level("ai-basics", 3)
C4 = [(0, 0), (0, 1), (1, 0), (1, 1)]
P8 = list(itertools.product((0, 1), repeat=3))


def s_a(w, x, b):
    return sum(F(str(a)) * c for a, c in zip(w, x)) + F(str(b))


def s_b(w, x, b):
    if all(c in (0, 1) for c in x):   # inputs that are 0 or 1: the bias plus the weights of the inputs that are 1
        return F(str(b)) + sum((F(str(a)) for a, c in zip(w, x) if c == 1), F(0))
    total = F(str(b))                  # other inputs: the products added in reverse order
    for a, c in reversed(list(zip(w, x))):
        total += F(str(a)) * F(str(c))
    return total


def S(w, x, b):
    a, c = s_a(w, x, b), s_b(w, x, b)
    lv.claim(a == c, f'sum {w} {x} {b}: {a} = {c}')
    return a


def fire(w, x, b):
    return 1 if S(w, x, b) > 0 else 0


def table(w, b, pats=C4):
    return [fire(w, x, b) for x in pats]


def scr(f, title):
    doc = lv.files[[k for k in lv.files if k.startswith(f)][0]]
    return f"screens[{[i for i, s in enumerate(doc['screens']) if s.get('title') == title][0]}]"


def item(f, iid):
    doc = lv.files[[k for k in lv.files if k.startswith(f)][0]]
    return f"items[{[i for i, s in enumerate(doc['items']) if s.get('id') == iid][0]}]"


def node(f, path):
    n = lv.files[[k for k in lv.files if k.startswith(f)][0]]
    for part in path.replace(']', '').replace('[', '.').split('.'):
        n = n[int(part)] if part.isdigit() else n[part]
    return n


def run_code(f, path):
    w = node(f, path)['widget']
    ok_all, starter_fails = True, False
    for src, want in ((w['solution'], True), (w['starter'], False)):
        ns = {}
        if w.get('prelude'):
            exec(w['prelude'], ns)
        exec(src, ns)
        ns['__learner_source__'] = src
        exec(ZQ_LIB, ns)
        for t in w['tests']:
            try:
                if t.get('setup'):
                    exec(t['setup'], ns)
                got = eval(t['call'], ns); exp = eval(t['expect'])
                ok = abs(got - exp) <= 1e-9 * max(1, abs(exp)) if t.get('compare') == 'isclose' else got == exp
            except Exception:
                ok = False
            ok_all &= ok or not want
            starter_fails |= (not ok) and not want
    lv.claim(ok_all, f'{f} {path}: solution passes every hidden test')
    lv.claim(starter_fails, f'{f} {path}: starter fails a hidden test')
    return w


# ---------------- the umbrella neuron ----------------
UW, UB = [2, 3, -1], -2.5
US = [S(UW, p, UB) for p in P8]
lv.claim([float(v) for v in US] == [-2.5, -3.5, 0.5, -0.5, -0.5, -1.5, 2.5, 1.5], f'umbrella sums {US}')
lv.claim([p for p in P8 if fire(UW, p, UB)] == [(0, 1, 0), (1, 1, 0), (1, 1, 1)], 'umbrella fires on (0,1,0), (1,1,0), (1,1,1)')
lv.claim(sum(fire(UW, p, -0.4) for p in P8) == 6 and [p for p in P8 if not fire(UW, p, -0.4)] == [(0, 0, 0), (0, 0, 1)], 'bias -0.4: 6 fire, all but (0,0,0) and (0,0,1)')
lv.claim(S(UW, (1, 0, 0), -2) == 0 and S(UW, (0, 1, 1), -2) == 0 and fire(UW, (1, 0, 0), -2) == 0, 'bias -2: (1,0,0) and (0,1,1) sum to exactly 0 and do not fire')
lv.claim(min(S(UW, p, 0) for p in P8) == -1 and all(fire(UW, p, 2) for p in P8) and not all(fire(UW, p, 1) for p in P8), 'smallest whole bias that always fires is 2 (1 leaves the bag alone at 0)')
lv.claim(max(S(UW, p, UB) for p in P8) == F('2.5') and [p for p in P8 if S(UW, p, UB) == F('2.5')] == [(1, 1, 0)], 'largest sum 2.5 at cloudy and rain')
for p, path in (((0, 1, 0), scr('l9', 'The weighted sum')), ((1, 1, 0), scr('l9', 'Cloudy and rain')), ((0, 0, 1), scr('l9', 'Cloudy alone, bag alone'))):
    lv.expect('l9', path + '.widget.answer', S(UW, p, UB))
lv.expect('l9', scr('l9', 'Cloudy alone, bag alone') + '.feedback.correct', S(UW, (1, 0, 0), UB))
rows = node('l9', scr('l9', 'The other four'))['widget']['rows']
for r, p in zip(rows, P8):
    cell = r[3]
    v = cell['answer'] if isinstance(cell, dict) else float(cell.replace('−', '-'))
    lv.claim(F(str(v)) == S(UW, p, UB), f'l9 table row {p} = {v}')
lv.claim(S([2, -1], (1, 1), UB) == F('-1.5') and S([2, -1], (1, 1), 0) == 1 and S([2, 3, -1], (1, 1, 1), UB) == F('1.5') and S([2, 1], (1, 1), UB) == F('0.5'), 'trap slips: -1.5 right; 1 no bias; 1.5 rain added; 0.5 bag sign')
lv.expect('l9', scr('l9', 'Any weighted sum') + '.widget.answer', S([1.5, -2], (1, 1), 0.5))
lv.claim(S([4, -15], (F('4.5'), 1), 20) == 23, 'credit score 23')
lv.expect('l9', scr('l9', 'A credit score') + '.widget.answer', 23)
lv.expect('l9', 'quiz[0].widget.answer', S([4, -3], (1, 1), -0.5))
lv.expect('l9', 'quiz[1].widget.answer', S([4, -3], (0, 1), -0.5))

# l10
bars = node('l10', scr('l10', 'Take it or not?'))['canvas']['state']['values']
lv.claim([F(str(v)) for v in bars.values()] == US, 'l10 bars are the eight umbrella sums')
lv.expect('l10', scr('l10', 'The threshold rule') + '.widget.answer', 3)
der = node('l10', scr('l10', 'Move the bias'))['canvas']['derive']
for p, key in zip(P8, [f'values.p{"".join(map(str, p))}' for p in P8]):
    base = F(str(float(der[key].split('+')[0])))
    lv.claim(base + F('-2.5') == US[P8.index(p)], f'l10 slider formula for {p}')
lv.expect('l10', scr('l10', 'Move the bias') + '.widget.answer', 6)
bars2 = node('l10', scr('l10', 'Exactly zero'))['canvas']['state']['values']
lv.claim([F(str(v)) for v in bars2.values()] == [S(UW, p, -2) for p in P8], 'l10 bias -2 bars')
lv.expect('l10', scr('l10', 'Always yes') + '.widget.answer', 2)
lv.claim(S([F('0.6'), F('-0.4')], (F('0.5'), F('0.4')), F('-0.1')) == F('0.04'), 'fund score 0.04')
lv.expect('l10', scr('l10', 'A trading rule as a neuron') + '.widget.answer', 0.04)
lv.claim(S([F('0.6'), F('-0.4')], (F('0.5'), F('0.4')), 0) == F('0.14') and S([F('0.6'), F('0.4')], (F('0.5'), F('0.4')), F('-0.1')) == F('0.36'), 'fund slips 0.14 and 0.36')
lv.claim(table([1, 2], -1.5) == [0, 1, 0, 1], 'l10 quiz: weights 1, 2, bias -1.5 fire on 2')
run_code('l10', scr('l10', 'The sum in code'))
run_code('l10', scr('l10', 'Firing in code'))

# l11
lv.claim(table([2, 2], -3) == [0, 0, 0, 1] and table([2, 2], -1) == [0, 1, 1, 1] and table([-2, -2], 3) == [1, 1, 1, 0], 'AND, OR, NAND tables')
lv.claim(table([5, 5], -7) == [0, 0, 0, 1] and [S([5, 5], x, -7) for x in C4] == [-7, -2, -2, 3], '5, 5, -7 is AND with sums -7, -2, -2, 3')
lv.claim([S([2, 2], x, -2) for x in C4] == [-2, 0, 0, 2] and table([2, 2], -2) == [0, 0, 0, 1], '2, 2, -2: sums -2, 0, 0, 2, AND under ">"')
lv.claim([1 if S([2, 2], x, -2) >= 0 else 0 for x in C4] == [0, 1, 1, 1], '2, 2, -2 under ">= 0" is OR')
lv.claim([fire([-2], [x], 1) for x in (0, 1)] == [1, 0], 'NOT: weight -2, bias 1')
lv.claim(sum(fire([1, 1, 1], p, -1.5) for p in P8) == 4, 'at least two of three fires on 4 patterns')
for path, (w, b) in ((scr('l11', 'AND'), ([2, 2], -3)), (scr('l11', 'NAND'), ([-2, -2], 3))):
    rows = node('l11', path)['widget']['rows']
    lv.claim([r[3]['answer'] for r in rows] == table(w, b), f'l11 table {w} {b}')
    lv.claim([F(r[2].replace('−', '-')) for r in rows] == [S(w, x, b) for x in C4], f'l11 sums shown {w} {b}')
chk = node('l11', scr('l11', 'Both or nothing'))['widget']['check']


def and_indicator(a, d, c):
    return (1 if c > 0 else 0) + (1 if d + c > 0 else 0) + (1 if a + c > 0 else 0) + (0 if a + d + c > 0 else 1)
lv.claim(chk == "(c>0?1:0)+(d+c>0?1:0)+(a+c>0?1:0)+(a+d+c>0?0:1)", 'l11 sliders check is the AND indicator')
grid = [F(k, 2) for k in range(-8, 9)]
cnt_ok = sum(1 for a in grid for d in grid if d > 0 for c in [F(k, 2) for k in range(-10, 11)] if and_indicator(a, d, c) == 0)
cnt_tab = sum(1 for a in grid for d in grid if d > 0 for c in [F(k, 2) for k in range(-10, 11)] if table([a, d], c) == [0, 0, 0, 1])
lv.claim(cnt_ok == cnt_tab and cnt_ok > 0 and and_indicator(2, 2, -3) == 0, f'the indicator is 0 exactly for AND neurons ({cnt_ok} on the slider grid)')
lv.claim(table([3, 3], -4) == [0, 0, 0, 1], 'l11 quiz: 3, 3, -4 is AND')
lv.claim(table([1, 1], -0.5) == [0, 1, 1, 1], 'l11 quiz: 1, 1, -0.5 is OR')
run_code('l11', scr('l11', 'Truth tables in code'))

# l12
g = [F(k, 2) for k in range(-10, 11)]
found = [(a, b, c) for a in g for b in g for c in g if [1 if a * x + b * y + c > 0 else 0 for x, y in C4] == [0, 1, 1, 0]]
lv.claim(len(g) == 21 and len(g) ** 3 == 9261 and not found, 'no XOR neuron among the 9261 on the 0.5 grid')
lv.expect('l12', scr('l12', 'Checking by search') + '.widget.answer', 9261)
rnd = random.Random(12)
viol = 0
for _ in range(20000):
    a, b, c = (rnd.uniform(-50, 50) for _ in range(3))
    if c <= 0 and a + c > 0 and b + c > 0 and not a + b + c > 0:
        viol += 1
lv.claim(viol == 0, 'the proof: b <= 0, w1 + b > 0, w2 + b > 0 always give w1 + w2 + b > 0 (20,000 random neurons)')
OR_, NAND_ = ([2, 2], -1), ([-2, -2], 3)
xor = [fire([2, 2], [fire(OR_[0], x, OR_[1]), fire(NAND_[0], x, NAND_[1])], -3) for x in C4]
lv.claim(xor == [0, 1, 1, 0], 'AND(OR, NAND) is XOR')
rows = node('l12', scr('l12', 'Two layers'))['widget']['rows']
lv.claim([[r[2]['answer'], r[3]['answer'], r[4]['answer']] for r in rows] == [[fire(OR_[0], x, OR_[1]), fire(NAND_[0], x, NAND_[1]), v] for x, v in zip(C4, xor)], 'l12 table OR, NAND, XOR')
lv.expect('l12', scr('l12', 'Counting the numbers') + '.widget.answer', 2 * 2 + 2 + 2 + 1)
lv.expect('l12', 'quiz[1].widget.answer', 3 * 2 + 3 + 3 + 1)
lv.claim(table([2, 0], -1) == [0, 0, 1, 1] and table([-2, -2], 1) == [1, 0, 0, 0], 'copy x1 and NOR neurons exist (homework distractors)')
run_code('l12', scr('l12', 'XOR in code'))
xt = node('l12', scr('l12', 'XOR in code'))['widget']['tests']
lv.claim([int(t['expect']) for t in xt[:4]] == [x ^ y for x, y in C4], 'xor_net expected outputs are XOR')

# ---------------- review-3 ----------------
lv.expect('review', item('review', 'r-sum-a') + '.widget.answer', S([1.5, -0.5], (1, 1), -1))
lv.expect('review', item('review', 'r-sum-three') + '.widget.answer', S([4, -2, 1], (1, 1, 0), -2.5))
lv.claim(S([4, -2, 1], (1, 1, 1), -2.5) == F('0.5'), 'r-sum-three slip "all" gives 0.5')
lv.expect('review', item('review', 'r-count-fire') + '.widget.answer', sum(table([1, 2], -1.5)))
lv.claim(table([3, 3], -4) == [0, 0, 0, 1] and table([3, 3], -2) == [0, 1, 1, 1] and table([3, 3], 1) == [1, 1, 1, 1] and table([3, 3], -7) == [0, 0, 0, 0], 'r-and-bias options')
lv.claim(fire([-3], [1], 2) == 0 and S([-3], [1], 2) == -1, 'r-not: sum -1, output 0')
lv.expect('review', item('review', 'r-nand-sum') + '.widget.answer', S([-2, -2], (1, 1), 3))
lv.expect('review', item('review', 'r-count-numbers') + '.widget.answer', 3 * 2 + 2 + 2 + 1)
lv.claim(sum(table([2, 3], -4)) == 1 and sum(table([2, 3], -2.5)) == 2, 'r-bias-raise: 1 then 2')
lv.expect('review', item('review', 'r-bias-raise') + '.widget.answer', 2)

# ---------------- homework-3 ----------------
w = run_code('homework', item('homework', 'h-exactly-two'))
for t in w['tests'][:8]:
    a, b, c = eval(t['call'][len('exactly_two'):])
    lv.claim(int(t['expect']) == int(a + b + c == 2), f"exactly_two{(a, b, c)} = {t['expect']}")
def ex2(x):
    return fire([2, -2], [fire([1, 1, 1], x, -1.5), fire([1, 1, 1], x, -2.5)], -1)
lv.claim([ex2(p) for p in P8] == [int(sum(p) == 2) for p in P8], 'the model weights compute exactly two of three')
run_code('homework', item('homework', 'h-my-neuron'))
lv.claim(table([2, -2], -1) == [0, 0, 1, 0], 'h-my-neuron model: 2, -2, -1')
lv.expect('homework', item('homework', 'h-sum-neg') + '.widget.answer', S([0.5, -1.5, 2], (1, 0, 1), -2))
biases = [b for b in range(-10, 11) if table([3, 3], b) == [0, 0, 0, 1]]
lv.claim(biases == [-5, -4, -3], f'h-and-biases: {biases}')
lv.expect('homework', item('homework', 'h-and-biases') + '.widget.answer', len(biases))

# ---------------- problems-3 ----------------
LW, LB = [1.5, 2.5, -1], -2
LS = [S(LW, p, LB) for p in P8]
lv.claim([float(v) for v in LS] == [-2, -3, 0.5, -0.5, -0.5, -1.5, 2, 1], f'alert sums {LS}')
lv.expect('problems', 'items[0].parts[0].widget.answer', S(LW, (1, 1, 0), LB))
lv.claim(fire(LW, (1, 0, 1), LB) == 0 and S(LW, (1, 0, 1), LB) == F('-1.5'), 'alert (1,0,1): -1.5, no flag')
lv.expect('problems', 'items[0].parts[2].widget.answer', sum(1 for v in LS if v > 0))
lv.expect('problems', 'items[0].parts[2].explain.text', 0.5)
lv.expect('problems', 'items[0].parts[3].widget.answer', S([1.5, 2.5, -2], (1, 1, 1), LB))
lv.claim(fire([1.5, 2.5, -2], (1, 1, 1), LB) == 0 and fire(LW, (1, 1, 1), LB) == 1, 'alert: weight change drops the flag at (1,1,1)')
lv.claim(sum(table([2, 2], -3)) == 1 and S([2, 2], (0, 1), -1) == 1 and sum(table([2, 2], -1)) == 3, 'AND to OR: 1, 1, 3')
lv.expect('problems', 'items[1].parts[2].widget.answer', 1)
lv.expect('problems', 'items[1].parts[3].widget.answer', 3)
lv.expect('problems', 'items[2].parts[0].widget.answer', S([3, 3], (1, 0), -2))
lv.expect('problems', 'items[2].parts[1].widget.answer', S([-3, -3], (1, 1), 4))
def net(x, ob):
    return fire([3, 3], [fire([3, 3], x, -2), fire([-3, -3], x, 4)], ob)
lv.claim([net(x, -5) for x in C4] == [0, 1, 1, 0], 'scaled network is XOR')
lv.claim([net(x, -2) for x in C4] == [1, 1, 1, 1], 'with output bias -2 it says 1 for all 4 inputs')
lv.expect('problems', 'items[2].parts[2].widget.answer', net((1, 1), -5))
lv.expect('problems', 'items[2].parts[3].widget.answer', 3 * 3)
lv.expect('problems', 'items[2].parts[4].widget.answer', sum(net(x, -2) for x in C4))

lv.check_wrongs()
lv.report()
