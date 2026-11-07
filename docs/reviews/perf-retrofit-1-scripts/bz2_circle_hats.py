"""brainteasers/homework-2 hw9-circle-hats: reader's own plan, shipped solution,
starter and six reader-planted plans against every example and hidden test."""
import itertools
from harness import item, run, check, finish

_, it = item('brainteasers', 'homework-2', 'hw9-circle-hats')
w = it['widget']
cases = w['examples'] + w['tests']
H = "def guess(i, n, left, right):\n"

# Reader's own plan: pairs (1, 2), (3, 4), ..., wrapping (n - 1, 0) when n is even.
mine = H + (
    "    if i % 2 == 1:\n"
    "        return right if i + 1 < n or n % 2 == 0 else 0   # bets match with i + 1\n"
    "    if i == 0 and n % 2 == 1:\n"
    "        return 0                                          # odd n: person 0 is alone\n"
    "    return 1 - left                                       # bets differ with i - 1\n")

for name, code in [('shipped solution', w['solution']), ('reader plan', mine)]:
    res = run(code, w, cases)
    check(all(r[0] for r in res), f'{name} passes all {len(cases)} cases, slowest {max(r[1] for r in res):.3f} s')

res = run(w['starter'], w, w['tests'])
check(not any(r[0] for r in res), 'starter fails every hidden test')

planted = {
    'chain: even matches i - 1, odd differs from i - 1': H + "    return left if i % 2 == 0 else 1 - left\n",
    'everyone says the parity of the two seen': H + "    return left ^ right\n",
    'odd differs from its right, not its partner': H + "    return right if i % 2 == 0 else 1 - right\n",
    'gives up on odd n': H + "    if n % 2:\n        return 0\n    return right if i % 2 == 0 else 1 - left\n",
    'roles by half of the circle': H + "    return right if i < n // 2 else 1 - left\n",
    'pairs hard-coded for six people': H + "    return right if i in (0, 2, 4) else 1 - left\n",
}
for name, code in planted.items():
    hid = run(code, w, w['tests'])
    ex = run(code, w, w['examples'])
    bad = [k + 1 for k, r in enumerate(hid) if not r[0]]
    check(bool(bad), f'planted "{name}" caught by hidden tests {bad} (example passes: {all(r[0] for r in ex)})')

# Independent recount of the guarantee: the best plan for n = 3 over every pair of
# per-person rules, by brute force on (left, right) -> guess tables.
best = 0
for plan in itertools.product(range(16), repeat=3):
    worst = min(sum(((plan[i] >> (2 * h[(i - 1) % 3] + h[(i + 1) % 3])) & 1) == h[i] for i in range(3))
                for h in itertools.product((0, 1), repeat=3))
    best = max(best, worst)
check(best == 1, f'n = 3: no plan guarantees more than 1 (best {best})')

# Each guess is right on exactly half the colourings (it cannot see its own hat), the explain's average.
for n in (4, 5):
    ns = {}
    exec(w['solution'], ns)
    tot = sum(ns['guess'](i, n, h[(i - 1) % n], h[(i + 1) % n]) == h[i]
              for h in itertools.product((0, 1), repeat=n) for i in range(n))
    check(tot == n * 2 ** (n - 1), f'n = {n}: total right over all colourings {tot} = n 2^(n-1)')
finish()
