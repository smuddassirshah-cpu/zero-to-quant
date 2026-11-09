"""Recompute every figure of options homework-3 item h-derive-box (performance task, L3).

Route 1: symbolic (sympy) where it is installed: the box payoff on each region, the two trades' cash flows,
and the difference of the two parity lines. Without sympy the script falls back to exact fractions on a
grid of strikes and prices (route 2 below runs either way).
Route 2: exact fractions. The payoff is evaluated leg by leg at every share price on a fine grid for many
strike pairs; the dealer's figures are computed from the printed quotes, and again from parity gaps.
The optional American part is checked by brute force over exercise times and share prices.
Also: the item's shape, the rubric (every passing tick set, none skipping a named part), and every figure the
model prints, matched to the recomputed value.
Run: python3 -I docs/reports/options-3-perf-numbers.py (sympy optional; the venv has it).
"""
import json, os, itertools
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'options', 'homework-3.json')
doc = json.load(open(HW, encoding='utf-8'))
item = next(i for i in doc['items'] if i['id'] == 'h-derive-box')
fails = 0


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails += 1


# ---- shape ----
check(item['performance'] == 'derivation' and item['kind'] == 'longform', 'derivation built on a longform')
for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts'):
    check(k not in item, f'no {k}')
rub = item['rubric']
check(3 <= len(rub) <= 5 and sum(r['points'] for r in rub) == 10, f'{len(rub)} rows summing to 10')
req = [i for i, r in enumerate(rub) if r.get('required')]
check(req == [0, 1, 2, 3], 'rows 1 to 4 required, row 5 (the optional part) not')
check('\n5. Optional:' in item['prompt'] and rub[4]['text'].startswith('Optional part'), 'part 5 is marked optional in prompt and rubric')
check(len(doc['items']) <= 12 and sum(1 for i in doc['items'] if i.get('performance')) == 1, 'homework within 12 items, one performance item')

# every passing tick set: 7 points or more and every required row ticked; named parts are rows 1 to 4
named = {0, 1, 2, 3}
passing = []
for n in range(len(rub) + 1):
    for s in itertools.combinations(range(len(rub)), n):
        pts = sum(rub[i]['points'] for i in s)
        if pts >= 7 and all(i in s for i in req):
            passing.append(s)
print('passing tick sets (1-based):', [[i + 1 for i in s] for s in passing])
check(all(named <= set(s) for s in passing), 'no passing set skips a named part (payoff, both trades, parity, dealer)')
check(len(passing) == 2, 'two passing sets: rows 1-4 and rows 1-5')

# ---- route 1: symbolic ----
try:
    import sympy as sp
    S, K1, K2, r, T, L, B, S0 = sp.symbols('S K1 K2 r T L B S0', positive=True)
    C1, C2, P1, P2 = sp.symbols('C1 C2 P1 P2')
    # regions: payoff with each max resolved by hand, and the claim each equals K2 - K1
    region = {
        'S <= K1': (0 - 0 + (K2 - S) - (K1 - S)),
        'K1 < S < K2': ((S - K1) - 0 + (K2 - S) - 0),
        'S >= K2': ((S - K1) - (S - K2) + 0 - 0),
    }
    for name, expr in region.items():
        check(sp.simplify(expr - (K2 - K1)) == 0, f'symbolic payoff {name} is K2 - K1')
    Lv = (K2 - K1) / (1 + r) ** T
    check(sp.simplify(Lv * (1 + r) ** T - (K2 - K1)) == 0, 'loan of L grows to K2 - K1')
    # cheap: buy box (-B), borrow L (+L); expiry: +(K2-K1) - L(1+r)^T
    check(sp.simplify((K2 - K1) - Lv * (1 + r) ** T) == 0, 'cheap trade nets 0 at expiry')
    check(sp.simplify((-(K2 - K1)) + Lv * (1 + r) ** T) == 0, 'dear trade nets 0 at expiry')
    par1 = sp.Eq(C1 + K1 / (1 + r) ** T, P1 + S0)
    par2 = sp.Eq(C2 + K2 / (1 + r) ** T, P2 + S0)
    lhs = (par1.lhs - par2.lhs) - (par1.rhs - par2.rhs)  # = 0 under parity
    box = C1 - C2 + P2 - P1
    check(sp.simplify(lhs - (box - Lv)) == 0, 'first parity line less the second: box - (K2-K1)/(1+r)^T, S0 gone')
    check(S0 not in sp.simplify(lhs).free_symbols, 'S0 cancels in the difference')
    D = sp.symbols('D', positive=True)
    lhs_div = ((C1 + K1 / (1 + r) ** T) - (C2 + K2 / (1 + r) ** T)) - ((P1 + S0 - D) - (P2 + S0 - D))
    check(D not in sp.simplify(lhs_div).free_symbols, 'a dividend present value cancels the same way')
except ImportError:
    print('sympy not installed: symbolic route skipped, fraction route below covers it')


# ---- route 2: exact fractions ----
def call(s, k):
    return max(s - k, 0)


def put(s, k):
    return max(k - s, 0)


def box_pay(s, k1, k2):
    return call(s, k1) - call(s, k2) + put(s, k2) - put(s, k1)


ok = True
for k1 in [F(x, 2) for x in range(1, 60, 7)]:
    for k2 in [k1 + F(x, 4) for x in range(1, 40, 9)]:
        for s in [F(x, 8) for x in range(0, 8 * 80)]:
            if box_pay(s, k1, k2) != k2 - k1:
                ok = False
check(ok, 'box pays K2 - K1 at every grid price for many strike pairs (fractions)')

# the dealer's box
S_0, r_, T_ = F(100), F(4, 100), 1
c90, c110, p90, p110 = F('16.20'), F('5.60'), F('2.80'), F('10.90')
Lfair = F(20) / (1 + r_) ** T_
Bq = c90 - c110 + p110 - p90
check(Bq == F('18.70'), f'box cost 16.20 - 5.60 + 10.90 - 2.80 = 18.70 ({float(Bq)})')
check(round(float(Lfair), 4) == 19.2308, f'fair 20/1.04 = {float(Lfair):.6f}')
gap = Lfair - Bq
check(round(float(gap), 4) == 0.5308, f'cheap by {float(gap):.6f}')
cash_today = -c90 - p110 + c110 + p90 + Lfair
check(cash_today == gap, f'cash today -16.20 - 10.90 + 5.60 + 2.80 + 19.2308 = {float(cash_today):.4f}')
check(all(box_pay(F(s, 4), 90, 110) - Lfair * (1 + r_) ** T_ == 0 for s in range(0, 4 * 300)), 'at expiry box pays 20 and repays the 20 loan at every price')
# second route for the dealer's figures: parity gaps (call side less put side)
g90 = (c90 + F(90) / (1 + r_)) - (p90 + S_0)
g110 = (c110 + F(110) / (1 + r_)) - (p110 + S_0)
check(round(float(g90), 2) == -0.06 and round(float(g110), 2) == 0.47, f'parity gaps {float(g90):.4f} at 90, {float(g110):.4f} at 110')
check(g110 - g90 == gap, 'box cheapness equals the difference of the parity gaps')
check(round(float(g110), 2) - round(float(g90), 2) == round(float(gap), 2), 'rounded gaps 0.47 + 0.06 = 0.53, matching')
# each quote alone within its bounds (so only parity and the box flag the sheet)
pv = lambda k: F(k) / (1 + r_)
check(max(S_0 - pv(90), 0) <= c90 <= S_0 and max(S_0 - pv(110), 0) <= c110 <= S_0, 'calls inside their bounds')
check(max(pv(90) - S_0, 0) <= p90 <= pv(90) and max(pv(110) - S_0, 0) <= p110 <= pv(110), 'puts inside their bounds')
check(c90 >= c110 and p110 >= p90 and c90 - c110 <= pv(110) - pv(90) and p110 - p90 <= pv(110) - pv(90), 'strike order and spread bounds hold')

# ---- optional part: American early exercise against the long box ----
ok = True
for tq in range(0, 12):
    t = F(tq, 12)
    owe_f = 20 / (1.04 ** (1 - float(t)))  # loan balance at t, annual compounding
    if not owe_f <= 20 + 1e-12:
        ok = False
    for sq in range(0, 400):
        s = F(sq, 2)
        # assigned on the short 90 put: pay 90, get share; exercise long 110 put: get 110
        cash = -90 + 110
        if cash != 20:
            ok = False
        # left: long 90 call, short 110 call; value at expiry for any later price is in [0, 20]
        for s_T in (F(0), F(90), F(100), F(110), F(200)):
            rest = call(s_T, 90) - call(s_T, 110)
            if not 0 <= rest <= 20:
                ok = False
        # if the short 110 call is exercised later at any price, exercising the 90 call nets +20
        if (-s + 110) + (s - 90) != 20:
            ok = False
check(ok, 'early exercise: +20 on the assigned pair, loan balance at most 20, the rest never negative')

# ---- every figure the model prints ----
model = item['model']
for txt in ['20/1.04 = 19.2308', '£19.23', '16.20 - 5.60 + 10.90 - 2.80 = 18.70', '19.2308 - 18.70 = 0.5308',
            '-16.20 - 10.90 + 5.60 + 2.80 + 19.2308 = 0.5308', '£0.53', '£0.06', '£0.47', '£20.00',
            'L(1+r)^T = K_2 - K_1', '(K_2 - S_T) - (K_1 - S_T) = K_2 - K_1', '(S_T - K_1) + (K_2 - S_T) = K_2 - K_1',
            '(S_T - K_1) - (S_T - K_2) = K_2 - K_1', '20/1.04^{1 - t} \\le 20']:
    check(txt in model, f'model prints {txt!r}')
for txt in ['£16.20', '£5.60', '£2.80', '£10.90', '£100.00', '4%']:
    check(txt in item['prompt'], f'prompt prints {txt}')
for txt in ['£19.23', '£18.70', '£0.53', '£0.00']:
    check(txt in rub[3]['text'], f'rubric row 4 prints {txt}')

print('failures:', fails)
raise SystemExit(1 if fails else 0)
