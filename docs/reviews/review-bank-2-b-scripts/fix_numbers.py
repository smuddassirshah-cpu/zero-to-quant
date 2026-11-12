"""Numbers for the fixes proposed in docs/reviews/review-bank-2-b.md, each by two routes that share no code. Exit 0 when all agree.
Prints the values the review quotes."""
import io, math, contextlib
from fractions import Fraction as F


def N(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))


def agree(a, b, tol=1e-9, what=''):
    assert abs(a - b) <= tol, (what, a, b)
    return a


# 1. op-parity-price-the-put, new numbers: share 80, strike 84, three months, 6% continuous, call 4.10
kd = 84 * math.exp(-0.06 * 0.25)
kd2 = 84 / sum((0.015 ** k) / math.factorial(k) for k in range(30))  # the series for e^0.015
agree(kd, kd2, 1e-9, 'discounted strike')
put = 4.10 - 80 + kd
# second route: the put by Black-Scholes at the vol that gives the 4.10 call must match parity
def bs(S, K, r, T, v, call=True):
    d1 = (math.log(S / K) + (r + v * v / 2) * T) / (v * math.sqrt(T))
    d2 = d1 - v * math.sqrt(T)
    c = S * N(d1) - K * math.exp(-r * T) * N(d2)
    return c if call else c - S + K * math.exp(-r * T)
lo, hi = 0.01, 2.0
for _ in range(100):
    mid = (lo + hi) / 2
    if bs(80, 84, 0.06, 0.25, mid) < 4.10:
        lo = mid
    else:
        hi = mid
d1 = (math.log(80 / 84) + (0.06 + lo * lo / 2) * 0.25) / (lo * math.sqrt(0.25))
p_direct = 84 * math.exp(-0.015) * N(-(d1 - lo * 0.5)) - 80 * N(-d1)
agree(put, p_direct, 1e-6, 'put')
print(f'put-call parity: discounted strike {kd:.4f}, put {put:.4f} ({put:.2f}); undiscounted {4.10 - 80 + 84:.2f}; signs swapped {4.10 + 80 - kd:.2f}')

# 2. fi-forwards-currency-forward, new setting: a euro costs 0.8600 pounds; simple rates 4.5% in pounds, 2% in euros
fwd = F(86, 100) * F(1045, 1000) / F(102, 100)
# second route: two deposits that must match
euros = F(102, 100)                 # 1 euro grown
pounds = F(86, 100) * F(1045, 1000)  # its cost in pounds, grown
assert pounds / euros == fwd
print(f'currency forward: {float(fwd):.6f} (0.8811); rates swapped {0.86 * 1.02 / 1.045:.4f}; added gap {0.86 * 1.025:.4f}')

# 3. ms-costs-shortfall-with-unfilled, new numbers: 8,000 at 12.50; 5,000 filled at 12.54; close 12.70; commission 25
paper = 8000 * (F(1270, 100) - F(1250, 100))
real = 5000 * (F(1270, 100) - F(1254, 100)) - 25
parts = 5000 * F(4, 100) + 3000 * F(20, 100) + 25
assert paper - real == parts == 825
print(f'shortfall: {parts} (200 + 600 + 25); filled only {5000 * F(4, 100) + 25}; no commission {parts - 25}')

# 4. bull spread: buy the 40 call for 7, sell the 50 call for 3
pnl = lambda s: max(s - 40, 0) - max(s - 50, 0) - 7 + 3
be = [s / 100 for s in range(0, 10001) if pnl(s / 100) == 0]
assert be == [44.0] and 40 + (7 - 3) == 44
print('bull spread: break-even 44; one premium 47; both premiums 50')

# 5. short strangle: sell the 90 put for 3.20 and the 110 call for 2.80; share at 81
res = F(320, 100) + F(280, 100) - max(90 - 81, 0) - max(81 - 110, 0)
assert res == -3 == 6 - 9
print('short strangle: -3; no premium -9; premium only 6')

# 6. butterfly: 70, 80, 90 calls at 13.00, 6.50, 2.00
cost = F(13) - 2 * F(13, 2) + 2
best = max(max(s - 70, 0) - 2 * max(s - 80, 0) + max(s - 90, 0) for s in range(0, 201)) - cost
assert cost == 2 and best == 8 == (80 - 70) - 2
print('butterfly: cost 2, largest profit 8; ignored cost 10; gave cost 2')

# 7. calendar the other way round: buy the one-month call, sell the six-month call, at the money, zero rate (spot 100, vol 20%)
def greeks(T, S=100.0, v=0.2):
    d1 = v * math.sqrt(T) / 2
    ph = math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi)
    return ph / (S * v * math.sqrt(T)), S * ph * math.sqrt(T), -S * ph * v / (2 * math.sqrt(T))
def bump(T, S=100.0, v=0.2, h=0.01):
    p = lambda s, vv, t: s * (2 * N(vv * math.sqrt(t) / 2) - 1) if abs(s - 100) < 1e-12 else bs(s, 100, 0, t, vv)
    q = lambda s, vv, t: bs(s, 100, 0, t, vv)
    return (q(S + h, v, T) - 2 * q(S, v, T) + q(S - h, v, T)) / h / h, (q(S, v + 1e-5, T) - q(S, v - 1e-5, T)) / 2e-5, -(q(S, v, T + 1e-6) - q(S, v, T - 1e-6)) / 2e-6
g = [a - b for a, b in zip(greeks(1 / 12), greeks(0.5))]
gb = [a - b for a, b in zip(bump(1 / 12), bump(0.5))]
for a, b in zip(g, gb):
    agree(a, b, 2e-3, 'reverse calendar')
assert g[0] > 0 and g[1] < 0 and g[2] < 0
print(f'reverse calendar (long 1 month, short 6 months): gamma {g[0]:+.4f}, vega {g[1]:+.2f}, theta {g[2]:+.2f} a year')

# 8. weighted mid, new question: how many shares added to the offer bring the weighted mid back to 100.00
for add in range(0, 2000):
    wm = (F(9998, 100) * (100 + add) + F(10002, 100) * 900) / (1000 + add)
    if wm == 100:
        break
assert add == 800 and 900 - 100 == 800
print('weighted mid: add 800 shares to the offer (slips: 900, the size wanted, and 100, the size now)')

# 9. code blocks for the four reasoning items that copy a lesson
def out(src):
    b = io.StringIO()
    ns = {}
    with contextlib.redirect_stdout(b):
        exec(src, ns)
    return ns, b.getvalue().strip()
ns, _ = out('def tally(x, seen={}):\n    seen[x] = seen.get(x, 0) + 1\n    return len(seen)\n\ntotal = tally("a") + tally("b") + tally("a")\n')
assert ns['total'] == 5 == 1 + 2 + 2
print('default dict: total 5 (fresh dict each call 3; counted the key, not the length 4)')
_, o = out('class Desk:\n    limit = 5\n    names = []\n    def __init__(self, name):\n        self.names.append(name)\n        self.limit += 1\na, b = Desk("x"), Desk("y")\nprint(len(a.names) + a.limit)\n')
assert o == '8' and 2 + 6 == 8
print('class body: prints 8 (own list 7; shared limit 9)')
v = int(-3.5) + round(-3.5) + (-7 // 2)
assert v == -11 and (int(-3.5), round(-3.5), -7 // 2) == (-3, -4, -4)
print('three roundings: -11 (all towards zero -9; round to -3 gives -10)')
assert (7 // -2, 7 % -2) == (-4, -1)
assert (int(7 / -2), 7 - (-2) * int(7 / -2)) == (-3, 1)  # the C++ rule: quotient cut towards zero, remainder takes the sign of the dividend
print('7 over -2: C++ -3 and 1, Python -4 and -1')

# 10. one-step-short lines proposed in finding 7: the values
assert 100 * (math.exp(-0.05 ** 2 / 2) / math.sqrt(2 * math.pi)) * 0.5 > 19.9  # vega per unit of vol 19.92
print('step-short values: vega 20 per unit of vol (19.92 exact); VaR one standard deviation 36000; fair forward 202; price change 1.00; auction price 10.1; 600 pence; C - P over DF 2.14; top payoff 22.5; filled cost 360; left after C 350')
print('all agree')
