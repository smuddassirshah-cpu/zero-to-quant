import random, csv, io, subprocess, os
from harness import *
random.seed(77)
src = open('l2.py').read()
a = src.index("RS_REF = '''"); b = src.index("RS_START")
ns0 = {}; exec(src[a:b], ns0); RS_SRC = ns0['RS_REF']; ns = {}; exec(RS_SRC, ns); rs_a = ns['run_strategy']
def rs_b(prices):
    n = len(prices); i = 1; pnl = trades = 0
    while i < n:
        if prices[i] < prices[i-1]:
            e = prices[i]; sold = n - 1
            for j in range(i+1, n):
                p = prices[j]
                if 100*p >= 105*e or 100*p <= 97*e or j - i == 3: sold = j; break
            pnl += prices[sold] - e; trades += 1
            if sold == n - 1: break
            i = sold + 1
        else: i += 1
    return [pnl, trades]
def walk(n, start=10000):
    p = start; out = []
    for _ in range(n):
        p = max(100, int(p * (1 + random.uniform(-0.04, 0.045)))); out.append(p)
    return out
files = {'ticks-40.csv': walk(40), 'ticks-3.csv': [10000, 9900, 10600], 'ticks-header-only.csv': []}
for name, pr in files.items():
    rows = 'day,price_pence\n' + ''.join(f'{i},{p}\n' for i, p in enumerate(pr))
    open('data/' + name, 'w').write(rows)
    # parse two ways
    p1 = [int(r['price_pence']) for r in csv.DictReader(io.StringIO(rows))]
    p2 = [int(l.split(',')[1]) for l in rows.strip().splitlines()[1:]]
    assert p1 == p2 == pr
    A, B = rs_a(pr), rs_b(pr); assert A == B, (name, A, B)
    print(name, len(pr), A)
LOAD_REF = '''
import csv

def load_prices(path):
    with open(path) as f:
        return [int(row['price_pence']) for row in csv.DictReader(f)]

def strategy_from_file(path):
    return run_strategy(load_prices(path))
'''
LOAD_START = '''
def load_prices(path):
    return []

def strategy_from_file(path):
    return run_strategy(load_prices(path))
'''
RS_REF = RS_SRC
TESTS = []
for name, pr in files.items():
    TESTS.append(dict(call=f"strategy_from_file('{name}')", expect=rs_b(pr)))
# run_py needs files in cwd: run inside data dir
os.chdir('data')
check_py('strategy_from_file', RS_REF + LOAD_REF, RS_REF + LOAD_START, TESTS)
print(md_tests(TESTS))
print(open('ticks-40.csv').read().splitlines()[:6])
