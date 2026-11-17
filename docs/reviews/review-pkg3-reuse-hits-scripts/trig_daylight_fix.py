"""Fault 1 of review-pkg3-reuse-hits: new numbers for trig/problems-3.json p-daylight-model.

The item's 16.4 and 7.6 hours are the homework's 820 and 380 GWh divided by 50, so
a = 4.4 and d = 12 are h3-demand-model's 220 and 600 on another scale. New: 17.6 and 6.4.

  python trig_daylight_fix.py <path to problems-3.json>            # dry run: prints the table and every changed string
  python trig_daylight_fix.py <path to problems-3.json> --apply    # writes the file (same indent, ensure_ascii off)

Every number is computed twice (closed form, then bisection or a scan) before a string is touched.
"""
import json, math, re, sys
from fractions import Fraction as F

HI, LO, LEVEL, PEAK = F(176, 10), F(64, 10), 10, 6

# ---- compute, route 1: closed form
a = (HI - LO) / 2
d = (HI + LO) / 2
rng = HI - LO
c = PEAK - 3
s = F(LEVEL - d) / a                      # the sine at the level
u = math.asin(float(-s))                  # positive angle
second = math.pi + u
r1, r2 = 3 - 6 * u / math.pi, 3 + 6 * second / math.pi
above = r2 - r1
ns1, ns2 = 6 * (math.pi + u) / math.pi, 6 * (2 * math.pi - u) / math.pi      # slip: shift left out
ab1, ab2 = 3 + 6 * u / math.pi, 3 + 6 * (math.pi - u) / math.pi              # slip: sine taken positive

# ---- route 2: bisection and a 12,000-step scan on the model itself
L = lambda t: float(a) * math.sin(math.pi / 6 * (t - c)) + float(d)
def bisect(f, lo, hi):
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(lo) * f(mid) > 0 else (lo, mid)
    return (lo + hi) / 2
b1, b2 = bisect(lambda t: L(t) - LEVEL, 0, 3), bisect(lambda t: L(t) - LEVEL, 9, 12)
scan = sum(1 for i in range(12000) if L((i + 0.5) / 1000) > LEVEL) / 1000
grid = [L(i / 1000) for i in range(12001)]
checks = [
    (a == F(28, 5) and d == 12 and rng == F(56, 5), 'a = 5.6, d = 12, range 11.2'),
    (abs(max(grid) - float(HI)) < 1e-9 and abs(min(grid) - float(LO)) < 1e-9, 'model peaks at 17.6 and dips to 6.4'),
    (abs(L(6) - 17.6) < 1e-12 and abs(L(12) - 6.4) < 1e-12, 'peak in month 6, trough in month 12'),
    (s == F(-5, 14), 'sine at 10 hours is -5/14'),
    (abs(r1 - b1) < 1e-9 and abs(r2 - b2) < 1e-9, 'roots agree with bisection'),
    (abs(above - scan) < 2e-3, 'months above agree with the scan'),
    (abs(u - 0.3652) < 5e-5 and abs(math.pi + 0.3652 - 3.5068) < 5e-5, 'printed u = -0.3652 and pi + 0.3652 = 3.5068'),
    (round(6 * -0.3652 / math.pi, 2) == -0.70 and round(6 * 3.5068 / math.pi, 2) == 6.70, 'printed t - 3 = -0.70 and 6.70'),
    (abs(r1 - 2.30) < 0.01 and abs(r2 - 9.70) < 0.01, 'key 2.3, 9.7 inside its band of 0.01'),
    (abs(above - 7.4) < 0.05 and abs((12 - above) - 4.6) < 0.05 and abs(8 - 7.4) > 0.1, 'part 5: 7.4 in band, slips 4.6 and 8 outside it'),
    (abs(ns1 - 6.7) < 0.01 and abs(ns2 - 11.3) < 0.01 and abs(ab1 - 3.7) < 0.01 and abs(ab2 - 8.3) < 0.01, 'part 4 slips 6.7, 11.3 and 3.7, 8.3'),
    (abs(L(3.7) - 14) < 0.02 and abs(L(8.3) - 14) < 0.02, 'the "above" slip gives 14 hours'),
    (float(HI / LO) != 820 / 380 and float(a) * 50 != 220, 'no longer the homework on another scale'),
]
bad = [m for okay, m in checks if not okay]
for okay, m in checks:
    print('ok  ' if okay else 'FAIL', m)
print(f'a={float(a)} d={float(d)} range={float(rng)} sine={s} u={u:.5f} second={second:.5f} roots={r1:.4f},{r2:.4f} above={above:.4f} below={12 - above:.4f}')
print(f'slips: no-shift {ns1:.4f},{ns2:.4f}  above {ab1:.4f},{ab2:.4f}  whole-months 8  outside {12 - above:.4f}')
if bad:
    sys.exit('computation checks failed')

# ---- the replacement table: old printed number -> new, applied in one pass to every string of the item
TEXT = {
    '16.4': '17.6', '7.6': '6.4', '8.8': '11.2', '4.4': '5.6',
    '0.4719': '0.3652', '3.6135': '3.5068', '0.90': '0.70', '6.90': '6.70',
    '2.10': '2.30', '9.90': '9.70', '7.8': '7.4', '4.2': '4.6',
    '6.9, 11.1': '6.7, 11.3', '3.9, 8.1': '3.7, 8.3',
}
FRAC = {'\\tfrac{5}{11}': '\\tfrac{5}{14}'}
NUM = {4.4: 5.6, 8.8: 11.2, 16.4: 17.6, 2.1: 2.3, 9.9: 9.7, 7.8: 7.4, 4.2: 4.6}
pat = re.compile(r'(?<![\d.])(' + '|'.join(re.escape(k) for k in sorted(TEXT, key=len, reverse=True)) + r')(?!\d)')

changed = []
def walk(node, path):
    if isinstance(node, dict):
        return {k: walk(v, f'{path}.{k}') for k, v in node.items()}
    if isinstance(node, list):
        return [walk(v, f'{path}[{i}]') for i, v in enumerate(node)]
    if isinstance(node, str):
        new = pat.sub(lambda m: TEXT[m.group(1)], node)
        for k, v in FRAC.items():
            new = new.replace(k, v)
        if new != node:
            changed.append((path, node, new))
        return new
    if isinstance(node, float) and node in NUM and not path.endswith('.abs'):
        changed.append((path, node, NUM[node]))
        return NUM[node]
    return node

if len(sys.argv) > 1:
    path = sys.argv[1]
    raw = open(path, encoding='utf-8').read()
    doc = json.loads(raw)
    i = next(k for k, it in enumerate(doc['items']) if it['id'] == 'p-daylight-model')
    doc['items'][i] = walk(doc['items'][i], f'items[{i}]')
    for p, old, new in changed:
        print(f'\n{p}\n  - {old}\n  + {new}')
    print(f'\n{len(changed)} fields change')
    left = [o for o in ('16.4', '7.6', '8.8', '4.4', '5}{11', '0.4719', '3.6135', '2.10', '9.90', '7.8', '4.2') if re.search(r'(?<![\d.])' + re.escape(o) + r'(?!\d)', json.dumps(doc['items'][i], ensure_ascii=False))]
    print('old numbers left in the item:', left or 'none')
    if '--apply' in sys.argv:
        indent = len(re.search(r'\n( +)"', raw).group(1))
        open(path, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, indent=indent) + ('\n' if raw.endswith('\n') else ''))
        print('written', path)
