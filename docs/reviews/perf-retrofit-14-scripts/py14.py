"""Second read, batch 14 Python code items: first-python h-split-bill and h-contract-cost, terminal h-perf-fx-paths
and h-perf-trade-script, py-found h4-sweep-offers. For each: the shipped solution passes every test, the starter
fails, reader solutions written independently pass, reader plants fail, and every expect is recomputed by a second
route (Fraction arithmetic or a bash run). Proposed fixes are checked where they change a graded value.
Run with the venv Python: python -I py14.py. Exit 0 when every claim holds."""
import copy, os, shutil, subprocess, sys, tempfile
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness14 as H

fails = []


def check(c, m):
    print('ok  ' if c else 'FAIL', m)
    if not c:
        fails.append(m)


def suite(name, w, readers, plants, nstart=None):
    f, _ = H.grade(w, w['solution'])
    check(f == [], f'{name}: shipped solution passes all {len(w["tests"])}')
    f, _ = H.grade(w, w['starter'])
    check(len(f) >= 1, f'{name}: starter fails tests {f}')
    for k, src in readers.items():
        f, r = H.grade(w, src)
        check(f == [], f'{name}: reader {k} passes all' + ('' if not f else f' (fails {f}: {[r[i-1] for i in f][:2]})'))
    for k, src in plants.items():
        f, r = H.grade(w, src)
        check(len(f) >= 1, f'{name}: plant {k} fails tests {f}')

# ---------------- first-python homework-2 h-split-bill ----------------
w = H.item('first-python', 'homework-2.json', 'h-split-bill')['widget']
R = {
 'R1 while loop, people > 5': 'def split_bill(prices, people):\n    share = None\n    i = 0\n    bill = 0.0\n    while i < len(prices):\n        bill += float(prices[i])\n        i += 1\n    if people > 5:\n        bill = bill + bill * 12.5 / 100\n    share = bill / people\n    return share\n',
 'R2 charge per dish': 'def split_bill(prices, people):\n    share = None\n    total = 0\n    for p in prices:\n        x = float(p)\n        if not people < 6:\n            x = x * 1.125\n        total = total + x\n    share = total / people\n    return share\n',
}
P = {
 'P1 int() on prices': R['R2 charge per dish'].replace('x = float(p)', 'x = int(p)'),
 'P2 charge at more than 6': R['R1 while loop, people > 5'].replace('people > 5', 'people > 6'),
 'P3 charge counted by dishes': R['R1 while loop, people > 5'].replace('people > 5', 'len(prices) >= 6'),
 'P4 charge 12.5 not 0.125': R['R1 while loop, people > 5'].replace('bill * 12.5 / 100', 'bill * 12.5'),
 'P5 share rounded to pence': R['R1 while loop, people > 5'].replace('share = bill / people', 'share = round(bill / people, 2)'),
 'P6 loop skips the last price': R['R1 while loop, people > 5'].replace('while i < len(prices)', 'while i < len(prices) - 1'),
}
suite('fp2', w, R, P)
# expects by Fractions
bills = [(['10', '20', '30'], 3), (['12.50', '8.00', '3.20'], 2), (['16.00'] * 6, 6), (['24.00', '31.50', '18.25', '9.75', '42.00'], 8),
         (['19.99', '22.50', '14.00', '8.75', '30.00'], 5), (['7.99'], 1),
         (['11.50', '13.25', '9.99', '14.00', '12.75', '10.50', '15.20', '8.95', '13.00', '12.40', '11.10', '16.36'], 12),
         (['4.50', '6.25', '3.80', '5.00', '7.45', '2.99', '6.01'], 4)]
for k, (ps, n) in enumerate(bills):
    tot = sum(F(p) for p in ps) * (F(9, 8) if n >= 6 else 1) / n
    check(abs(float(tot) - float(eval(w['tests'][k]['expect']))) < 1e-12, f'fp2 test {k+1}: Fraction route {tot} = {w["tests"][k]["expect"]}')

# ---------------- first-python homework-3 h-contract-cost ----------------
w = H.item('first-python', 'homework-3.json', 'h-contract-cost')['widget']
R = {
 'R1 while loop and a month count': 'form_fee = "14.99"\nform_rise = "3"\n\ndef contract_cost(fee, rise, years):\n    f = float(fee)\n    r = float(rise) / 100\n    paid = 0.0\n    y = 0\n    while y < years:\n        m = 0\n        while m < 12:\n            paid = paid + f\n            m = m + 1\n        f = f + f * r\n        y = y + 1\n    return paid\n\ntotal = contract_cost(form_fee, form_rise, 2)\nprint("Total: £" + format(total, ".2f"))\n',
 'R2 power of the rise': 'form_fee = "14.99"\nform_rise = "3"\n\ndef contract_cost(fee, rise, years):\n    total = 0\n    for y in range(years):\n        total += 12 * float(fee) * (1 + float(rise) / 100) ** y\n    return total\n\nprint(f"Total: £{contract_cost(form_fee, form_rise, 2):.2f}")\n',
}
P = {
 'P1 rise applied in year 1': R['R2 power of the rise'].replace('** y', '** (y + 1)'),
 'P2 int() on the rise': R['R2 power of the rise'].replace('float(rise)', 'int(rise)'),
 'P3 prints the total, returns nothing': R['R2 power of the rise'].replace('    return total\n\nprint(f"Total: £{contract_cost(form_fee, form_rise, 2):.2f}")\n', '    print(f"Total: £{total:.2f}")\n\ncontract_cost(form_fee, form_rise, 2)\n'),
 'P4 one payment a year': R['R2 power of the rise'].replace('12 * float(fee)', 'float(fee)'),
 'P5 prints with no £ and 1 dp': R['R2 power of the rise'].replace('Total: £{contract_cost(form_fee, form_rise, 2):.2f}', 'Total: {contract_cost(form_fee, form_rise, 2):.1f}'),
 'P6 three years in the print': R['R2 power of the rise'].replace('form_rise, 2)', 'form_rise, 3)'),
}
suite('fp3', w, R, P)


def cc(fee, rise, years):
    f, r, t = F(fee), F(rise) / 100, F(0)
    for _ in range(years):
        t += 12 * f
        f *= 1 + r
    return t
calls = [('10', '5', 1), ('20.00', '10', 2), ('15.50', '3.5', 3), ('12.00', '0', 4), ('8.99', '2.5', 5), ('25.00', '4', 0)]
for k, a in enumerate(calls):
    check(cc(*a) == F(str(eval(w['tests'][k]['expect']))), f'fp3 test {k+1}: exact {cc(*a)} = {w["tests"][k]["expect"]}')
check(f'{float(cc("14.99", "3", 2)):.2f}' == '365.16' and cc('14.99', '3', 2) == F('365.1564'), 'fp3 test 7: 2 years at £14.99, 3%: exactly 365.1564, printed 365.16')
check(cc('10.00', '5', 2) == 246, 'fp3 example: 246')

# ---------------- terminal homework-1 h-perf-fx-paths ----------------
w = H.item('terminal', 'homework-1.json', 'h-perf-fx-paths')['widget']
base = w['solution']
R = {'R1 ./ prefixes': base.replace('"../../.config/fx.ini"', '"./../.././.config/fx.ini"').replace('"/home/priya/fx/clean/eurusd.csv"', '"/home/priya/fx/./clean/eurusd.csv"')}
P = {
 'P1 lower-case raw': base.replace('/fx/Raw/gbpusd', '/fx/raw/gbpusd'),
 'P2 .config without the dot': base.replace('"/home/priya/.config/fx.ini"', '"/home/priya/config/fx.ini"'),
 'P3 one .. from scripts': base.replace('"../../.config/fx.ini"', '"../.config/fx.ini"'),
 'P4 tidy relative left as written': base.replace('"/home/priya/fx/scripts/tidy.py"', '"../scripts/tidy.py"'),
 'P5 holidays under home': base.replace('"/team/holidays.csv"', '"/home/team/holidays.csv"'),
 'P6 Windows backslashes': base.replace('"/home/priya/fx/clean/eurusd.csv"', '"\\\\home\\\\priya\\\\fx\\\\clean\\\\eurusd.csv"'),
}
suite('tm1', w, R, P)
# a correct absolute path with .. in it is refused: the message's claim
ns = {}
exec(w['prelude'], ns)
msg = ns['_lands']('/', '/home/priya/fx/../.config/fx.ini', 'top')
check(msg == 'uses .., but a path from the top only goes down', 'tm1: _lands refuses /home/priya/fx/../.config/fx.ini with "a path from the top only goes down"')
# bash agrees that path is absolute and reaches the file (second route on a scratch tree)
tmp = tempfile.mkdtemp()
for p in ['home/priya/.config/fx.ini', 'home/priya/fx/Raw/gbpusd.csv', 'home/priya/fx/clean/eurusd.csv', 'home/priya/fx/scripts/tidy.py', 'team/holidays.csv']:
    os.makedirs(os.path.join(tmp, os.path.dirname(p)), exist_ok=True)
    open(os.path.join(tmp, p), 'w').write('x')
out = subprocess.run(['bash', '-c', f'cd {tmp}/home/priya/fx/scripts && cat ../../.config/fx.ini && cat {tmp}/home/priya/fx/../.config/fx.ini && (cat {tmp}/home/priya/fx/raw/gbpusd.csv 2>/dev/null || echo NO) && cd {tmp}/home/priya/fx/clean && cat ../scripts/tidy.py'], capture_output=True, text=True).stdout
shutil.rmtree(tmp)
check(out == 'xxNO\nx', 'tm1 bash: ../../.config/fx.ini from scripts works, /…/fx/../.config/fx.ini works, raw (lower case) fails on Linux, ../scripts/tidy.py from clean works')

# ---------------- terminal homework-3 h-perf-trade-script ----------------
w = H.item('terminal', 'homework-3.json', 'h-perf-trade-script')['widget']
R = {
 'R1 one line, £ and 2 dp': '# cd /home/sam/desk && python3 trade.py\nshares = 40\ncost = shares * 12.25 + 10\nproceeds = shares * 13 - 10\nprofit = proceeds - cost\nret = profit / cost\nprint(f"Cost: £{cost:.2f}")\nprint(f"Proceeds: £{proceeds:.2f}")\nprint(f"Profit: £{profit:.2f}")\nprint(f"Return: {ret}")\n',
 'R2 $ prompts, cd desk/': '# $ cd desk/\n# $ python3 trade.py\ncost = 40 * 12.25 + 10.0\nproceeds = 40 * 13.0 - 10.0\nprofit = proceeds - cost\nret = profit / cost\nprint("Cost:", cost)\nprint("Proceeds:", proceeds)\nprint("Profit:", profit)\nprint("Return:", round(ret, 4))\n',
}
P = {
 'P1 fee once only': R['R2 $ prompts, cd desk/'].replace('proceeds = 40 * 13.0 - 10.0', 'proceeds = 40 * 13.0'),
 'P2 return on proceeds': R['R2 $ prompts, cd desk/'].replace('ret = profit / cost', 'ret = profit / proceeds'),
 'P3 runs from home': R['R2 $ prompts, cd desk/'].replace('# $ cd desk/\n# $ python3 trade.py', '# python3 desk/trade.py'),
 'P4 python not python3': R['R2 $ prompts, cd desk/'].replace('python3 trade.py', 'python trade.py'),
 'P5 labels out of order': R['R2 $ prompts, cd desk/'].replace('print("Cost:", cost)\nprint("Proceeds:", proceeds)', 'print("Proceeds:", proceeds)\nprint("Cost:", cost)'),
 'P6 cd into a folder that is not there': R['R2 $ prompts, cd desk/'].replace('cd desk/', 'cd sam/desk'),
}
suite('tm3', w, R, P)
# forms a learner may write that the follower does not read
for label, src, want in [
    ('cd "$HOME/desk"', R['R2 $ prompts, cd desk/'].replace('# $ cd desk/', '# $ cd "$HOME/desk"'), 'FAIL'),
    ('cd ~/desk', R['R2 $ prompts, cd desk/'].replace('# $ cd desk/', '# $ cd ~/desk'), 'pass'),
    ('Return printed as a percentage', R['R2 $ prompts, cd desk/'].replace('print("Return:", round(ret, 4))', 'print(f"Return: {ret:.2%}")'), 'FAIL'),
]:
    f, _ = H.grade(w, src)
    check((f == []) == (want == 'pass'), f'tm3: {label}: {"passes" if not f else "fails tests " + str(f)}')
check(F(40) * F('12.25') + 10 == 500 and F(40) * 13 - 10 == 510 and F(10, 500) == F(1, 50), 'tm3: 500, 510, 10, 0.02 by Fractions')

# ---------------- py-found homework-4 h4-sweep-offers ----------------
w = H.item('py-found', 'homework-4.json', 'h4-sweep-offers')['widget']
R = {
 'R1 stable sort by index, Fraction-free running sums': 'def sweep_offers(qty, offers):\n    if not qty > 0:\n        raise ValueError("qty")\n    book = list(offers)\n    order = sorted(range(len(book)), key=lambda i: (book[i][0], i))\n    need = qty\n    for i in order:\n        if need == 0:\n            return\n        price, size = book[i]\n        got = size if size < need else need\n        need -= got\n        yield (price, got)\n\n\ndef average_price(qty, offers):\n    n = 0\n    spent = 0\n    for p, s in sweep_offers(qty, offers):\n        n += s\n        spent += p * s\n    return spent / n if n else None\n',
 'R2 eager check, inner generator': 'def sweep_offers(qty, offers):\n    if qty <= 0:\n        raise ValueError(qty)\n    def walk():\n        left = qty\n        for price, size in sorted(offers, key=lambda o: o[0]):\n            if left <= 0:\n                break\n            take = min(left, size)\n            left -= take\n            yield price, take\n    return walk()\n\n\ndef average_price(qty, offers):\n    fills = list(sweep_offers(qty, offers))\n    bought = sum(s for _, s in fills)\n    if bought == 0:\n        return None\n    return sum(p * s for p, s in fills) / bought\n',
}
LISTY = 'def sweep_offers(qty, offers):\n    if qty <= 0:\n        raise ValueError(qty)\n    out = []\n    left = qty\n    for price, size in sorted(offers, key=lambda o: o[0]):\n        if left == 0:\n            break\n        take = min(left, size)\n        out.append((price, take))\n        left -= take\n    return out\n\n\ndef average_price(qty, offers):\n    fills = sweep_offers(qty, offers)\n    bought = sum(s for _, s in fills)\n    if bought == 0:\n        return None\n    return sum(p * s for p, s in fills) / bought\n'
P = {
 'P1 returns a list': LISTY,
 'P2 sorts the caller\'s book': R['R2 eager check, inner generator'].replace('sorted(offers, key=lambda o: o[0])', '(offers.sort(key=lambda o: o[0]) or offers)'),
 'P3 sorted on the whole pair (size breaks ties)': R['R2 eager check, inner generator'].replace('sorted(offers, key=lambda o: o[0])', 'sorted(offers)'),
 'P4 average over qty': R['R2 eager check, inner generator'].replace('/ bought\n', '/ qty\n'),
 'P5 assert instead of raise': R['R2 eager check, inner generator'].replace('    if qty <= 0:\n        raise ValueError(qty)\n', '    assert qty > 0\n'),
 'P6 zero fill yielded at the end': R['R1 stable sort by index, Fraction-free running sums'].replace('        if need == 0:\n            return\n', ''),
}
suite('pf4', w, R, P)
# the gap: a function that is not a generator but returns iter(list) passes every test
ITER = LISTY.split('\n\n\ndef average_price')[0].replace('    return out', '    return iter(out)') + '\n\n\ndef average_price' + R['R1 stable sort by index, Fraction-free running sums'].split('\n\n\ndef average_price')[1]
f, _ = H.grade(w, ITER)
check(f == [], 'pf4 gap: return iter(list) (not a generator) passes all 15 shipped tests')
w2 = copy.deepcopy(w)
w2['tests'][6] = {'setup': w['tests'][6]['setup'], 'call': '(next(sweep_offers(100, book)), type(sweep_offers(100, book)).__name__)', 'expect': "((4.50, 100), 'generator')", 'compare': 'equal'}
f, _ = H.grade(w2, ITER)
check(f == [7], f'pf4 proposed test 7 fails iter(list) at test 7 only: {f}')
f, _ = H.grade(w2, LISTY)
check(7 in f, f'pf4 proposed test 7 still fails a returned list: {f}')
for name, src in [('shipped', w['solution'])] + list(R.items()):
    f, _ = H.grade(w2, src)
    check(f == [], f'pf4 proposed test 7: {name} passes all 15')
# expects by Fractions
book = [(F('4.52'), 300), (F('4.50'), 200), (F('4.55'), 500), (F('4.50'), 100)]


def sweep(q, b):
    out, left = [], q
    for p, s in sorted(b, key=lambda o: o[0]):
        if left == 0:
            break
        t = min(s, left)
        out.append((p, t)); left -= t
    return out


def avg(q, b):
    fl = sweep(q, b)
    n = sum(s for _, s in fl)
    return sum(p * s for p, s in fl) / n if n else None
check(sweep(450, book) == [(F('4.5'), 200), (F('4.5'), 100), (F('4.52'), 150)], 'pf4 test 1 fills')
check(avg(450, book) == F(2028, 450) and abs(float(F(2028, 450)) - 4.506666666666667) < 1e-15, 'pf4 tests 1/10: £2,028 over 450 = 4.50666...')
check(avg(2000, book) == F(4981, 1100) and abs(float(F(4981, 1100)) - 4.528181818181818) < 1e-15, 'pf4 test 13: £4,981 over 1,100')
check(avg(250, book) == F('4.5') and avg(50, book) == F('4.5') and avg(300, book) == F('4.5'), 'pf4 tests 11, 12, 15: 4.5')

print('\nFAILURES: %d' % len(fails))
sys.exit(1 if fails else 0)
