"""Recompute every number in conditional homework-4 item h-host-rules-code (performance task, code).

Run from the repo root with any Python 3 (standard library only):
    python3 docs/reports/conditional-4-perf-numbers.py      exits 0 when every check passes.
Route A: exact enumeration in Fractions, written here without the solution's code. For each car place the host's
rule is a law over the doors he might open; the event seen is (he opens `opened`, it shows a goat).
Route B: a seeded simulation of 400,000 games per test case, keeping the games that match what was seen.
Then the solution passes every test, the starter fails every test, and each planted wrong solution fails one,
all under a copy of the engine's isclose rule (code.js __zq_cmp: rel 1e-9, abs 1e-12, lists element by element).
"""
import contextlib, io, json, math, os, random, sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/conditional/homework-4.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-host-rules-code')
w = item['widget']
tests = w['tests']
fails = []
def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

# ---- route A: the host's rule as a law over doors, in Fractions ----
def host_law(n, pick, car, host):
    """dict door -> chance the host opens it, given the car place."""
    if host == 'knows':
        ok = [d for d in range(n) if d not in (pick, car)]
        return {d: F(1, len(ok)) for d in ok}
    if host == 'random':
        ok = [d for d in range(n) if d != pick]
        return {d: F(1, len(ok)) for d in ok}
    if host == 'lowest':
        return {min(d for d in range(n) if d not in (pick, car)): F(1)}
    raise ValueError(host)

def lik_A(n, pick, car, opened, host):
    # seen: he opens `opened` AND a goat is there, so the car is not behind it
    return host_law(n, pick, car, host).get(opened, F(0)) * (car != opened)

def post_A(prior, pick, opened, host):
    prior = [F(p).limit_denominator(1000) for p in prior]
    n = len(prior)
    joint = {(c, d): prior[c] * q for c in range(n) for d, q in host_law(n, pick, c, host).items()}
    seen = {k: v for k, v in joint.items() if k[1] == opened and k[0] != opened}
    tot = sum(seen.values())
    check(f'  law sums to 1 for prior {prior}, {host}', sum(joint.values()) == sum(prior) == 1)
    if tot == 0:
        return None
    return [sum(v for (c, d), v in seen.items() if c == k) / tot for k in range(n)]

# the exact answer of every test, by route A
EXACT = [
    post_A([F(1, 3)] * 3, 0, 2, 'knows'),
    [lik_A(5, 2, c, 4, 'knows') for c in range(5)],
    [lik_A(5, 2, c, 4, 'random') for c in range(5)],
    [lik_A(4, 1, c, d, 'lowest') for d in (0, 2) for c in range(4)],
    post_A([F(1, 2), F(3, 10), F(1, 5)], 0, 2, 'knows'),
    post_A([F(1, 2), F(3, 10), F(1, 5)], 0, 2, 'random'),
    post_A([F(1, 10), F(1, 5), F(3, 10), F(3, 20), F(1, 4)], 2, 4, 'knows'),
    post_A([F(1, 10), F(1, 5), F(3, 10), F(3, 20), F(1, 4)], 2, 4, 'random'),
    [post_A([F(2, 5), F(1, 10), F(1, 5), F(3, 10)], 3, d, 'lowest') for d in (0, 1)],
    [post_A([0, 0, 1], 0, 2, 'knows'), post_A([0, F(1, 2), F(1, 2)], 0, 1, 'knows')],
    post_A([F(1, 10)] * 10, 0, 9, 'knows'),
]
def frac_tree(v):
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        return [frac_tree(x) for x in v]
    return F(v).limit_denominator(10000)
for i, (t, ex) in enumerate(zip(tests, EXACT)):
    got = frac_tree(eval(t['expect'], {}))
    check(f'test {i + 1}: expect equals the exact enumeration', got == ex, f'{t["expect"]}')

# route B: closed forms by hand for the stated cases
check('classic: 1/3 stay, 2/3 switch', EXACT[0] == [F(1, 3), F(2, 3), 0])
check('uneven knows: 0.25 : 0.3, so 5/11 and 6/11', EXACT[4][:2] == [F(25, 100) / F(55, 100), F(30, 100) / F(55, 100)])
check('uneven random: prior renormalised without door 2, 5/8 and 3/8', EXACT[5][:2] == [F(1, 2) / F(4, 5), F(3, 10) / F(4, 5)])
check('five doors knows: 1/30, 1/15, 3/40, 1/20 normalised = 4, 8, 9, 6 over 27',
      EXACT[6] == [x / (F(1, 30) + F(1, 15) + F(3, 40) + F(1, 20)) for x in (F(1, 30), F(1, 15), F(3, 40), F(1, 20))] + [0]
      and F(1, 30) + F(1, 15) + F(3, 40) + F(1, 20) == F(27, 120))
check('ten doors: your door keeps 1/10, others 9/80 each, sum 1', EXACT[10][0] == F(1, 10) and EXACT[10][1:9] == [F(9, 80)] * 8 and sum(EXACT[10]) == 1)
check('random host on three doors equals dropping the opened door', EXACT[5] == [F(5, 8), F(3, 8), 0])

# ---- route C: seeded simulation of the games ----
def play(prior, pick, host, rng):
    n = len(prior)
    car = rng.choices(range(n), weights=prior)[0]
    law = host_law(n, pick, car, host)
    doors = list(law)
    d = rng.choices(doors, weights=[float(law[x]) for x in doors])[0]
    return car, d
def simulate(prior, pick, opened, host, games, seed):
    rng = random.Random(seed)
    counts, kept = [0] * len(prior), 0
    for _ in range(games):
        car, d = play([float(p) for p in prior], pick, host, rng)
        if d == opened and car != opened:
            counts[car] += 1; kept += 1
    return [c / kept for c in counts] if kept else None, kept
SIM = [((F(1, 3),) * 3, 0, 2, 'knows', EXACT[0]),
       ((F(1, 2), F(3, 10), F(1, 5)), 0, 2, 'knows', EXACT[4]),
       ((F(1, 2), F(3, 10), F(1, 5)), 0, 2, 'random', EXACT[5]),
       ((F(1, 10), F(1, 5), F(3, 10), F(3, 20), F(1, 4)), 2, 4, 'knows', EXACT[6]),
       ((F(1, 10), F(1, 5), F(3, 10), F(3, 20), F(1, 4)), 2, 4, 'random', EXACT[7]),
       ((F(2, 5), F(1, 10), F(1, 5), F(3, 10)), 3, 0, 'lowest', EXACT[8][0]),
       ((F(2, 5), F(1, 10), F(1, 5), F(3, 10)), 3, 1, 'lowest', EXACT[8][1]),
       ((F(1, 10),) * 10, 0, 9, 'knows', EXACT[10])]
for k, (pr, pick, op, host, ex) in enumerate(SIM):
    est, kept = simulate(pr, pick, op, host, 400_000, 100 + k)
    worst = max(abs(a - float(b)) / max(math.sqrt(float(b) * (1 - float(b)) / kept), 1e-12) if 0 < b < 1 else abs(a - float(b)) * 1e9
                for a, b in zip(est, ex))
    check(f'simulation {host}, {len(pr)} doors, pick {pick}, opened {op}: within 4.5 se of exact', worst < 4.5, f'{kept} games kept, worst {worst:.2f} se')
est, kept = simulate([0, 0, 1], 0, 2, 'knows', 50_000, 7)
check('simulation: with the car surely behind the opened door, no game matches', est is None and kept == 0)

# ---- run code against the tests with the engine's compare rule ----
def _close(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y
def run(src, cases=tests):
    res = []
    for c in cases:
        g = {}
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(src, g)
            a = eval(c['call'], g); e = eval(c['expect'], g)
            res.append(bool(_close(a, e)))
        except Exception:
            res.append(False)
    return res
check('11 tests, 1 example, the example is test 1', len(tests) == 11 and len(w['examples']) == 1 and w['examples'][0] == tests[0])
check('every case compares isclose', all(c['compare'] == 'isclose' for c in tests + w['examples']))
check('how says 11 hidden tests and 1e-9', '11 hidden tests' in w['how'] and '1e-9' in w['how'])
r = run(w['solution']); check('solution passes all 11', all(r), str(r))
r = run(w['starter']); check('starter fails all 11', not any(r), str(r))

SOL = w['solution']
def variant(*pairs):
    s = SOL
    for old, new in pairs:
        assert old in s, old
        s = s.replace(old, new)
    return s
BUGS = {
    'host ignored: drop the opened door, renormalise the prior': variant(
        ("    paths = [prior[c] * host_likelihood(n, pick, c, opened, host)\n             for c in range(n)]",
         "    paths = [0 if c == opened else prior[c] for c in range(n)]")),
    'random host may show the car: no goat condition': variant(
        ("    if opened == pick or opened == car:\n        return 0.0      # not your door; a car is no goat\n",
         "    if opened == pick:\n        return 0.0\n"),
        ("    if host == 'knows':\n", "    if host == 'knows':\n        if opened == car:\n            return 0.0\n"),
        ("    if host == 'lowest':\n", "    if host == 'lowest':\n        if opened == car:\n            return 0.0\n")),
    'knowing host always has n - 2 doors': variant(("        return 1 / len(allowed)", "        return 1 / (n - 2)")),
    'knowing host always has n - 1 doors': variant(("        return 1 / len(allowed)", "        return 1 / (n - 1)")),
    'no normalising': variant(("    return [p / total for p in paths]", "    return paths")),
    'zeros instead of None when nothing seen can happen': variant(("    if total == 0:\n        return None\n", "    if total == 0:\n        return [0.0] * n\n")),
    'lowest read as highest': variant(("        first = min(d for d in range(n) if d != pick and d != car)",
                                       "        first = max(d for d in range(n) if d != pick and d != car)")),
    'lowest host may open the car door': variant(("        first = min(d for d in range(n) if d != pick and d != car)",
                                                  "        first = min(d for d in range(n) if d != pick)")),
    'even prior assumed': variant(("    paths = [prior[c] * host_likelihood", "    paths = [1 / n * host_likelihood")),
    'random host over every door, yours included': variant(("        return 1 / (n - 1)  # any door but yours", "        return 1 / n")),
}
SWAP = variant(("    paths = [prior[c] * host_likelihood(n, pick, c, opened, host)",
                "    paths = [prior[c] * host_likelihood(n, c, pick, opened, host)"))
check('pick and car swapped is equivalent (every rule treats them alike), so it passes', all(run(SWAP)))
for name, src in BUGS.items():
    r = run(src)
    failed = [i + 1 for i, x in enumerate(r) if not x]
    check(f'planted bug fails a test: {name}', bool(failed), f'fails tests {failed}')

# byKey and how texts name the right numbers
fb = item['feedback']['byKey']
check('byKey keys are test ids that exist', all(k.startswith('test-') and 1 <= int(k[5:]) <= len(tests) for k in fb))
check('test-11 line: your door keeps 1/10', '\\tfrac{1}{10}' in fb['test-11'] and EXACT[10][0] == F(1, 10))
check('test-3 line: chance 1/4 for door 4', '\\tfrac14' in fb['test-3'] and all(lik_A(5, 2, c, 4, 'random') == F(1, 4) for c in range(4)))
check('test-1 line: two goat doors, 1/2 each', '\\tfrac12' in fb['test-1'] and lik_A(3, 0, 0, 2, 'knows') == F(1, 2))
check('test-2 line: four doors with the car behind yours, three otherwise', lik_A(5, 2, 2, 4, 'knows') == F(1, 4) and lik_A(5, 2, 0, 4, 'knows') == F(1, 3))
check('test-4 line: car behind 0, pick 1, he opens 2', host_law(4, 1, 0, 'lowest') == {2: 1})
check('test-9 line: pick 3, opened 1 means car behind 0', EXACT[8][1] == [1, 0, 0, 0])

items = doc['items']
check('homework has 6 to 12 items', 6 <= len(items) <= 12, str(len(items)))
check('one performance item in the homework', sum(1 for i in items if i.get('performance')) == 1)
check('the item is last, code, difficulty 5', items[-1]['id'] == 'h-host-rules-code' and item['performance'] == 'code' and item['difficulty'] == 5)
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
