"""Recompute every number in py-found homework-3 item h-cash-account (performance task, code).

Run from anywhere with any Python 3 (standard library only):
    python3 -I docs/reports/py-found-3-perf-numbers.py      exits 0 when every check passes.
Route A is the item's own `solution` (whole pence in an int, a list of pence moves).
Route B is written differently in this file: it keeps the balance in exact Fractions of a pound
rounded to the penny on entry, and the history as pounds. Route C checks the stated figures by
integer pence arithmetic. Each test runs as the engine runs it: the prelude, the learner code,
the case's setup, then its call, judged by a copy of code.js __zq_cmp (== here, or raises).
The starter must fail, and each planted beginner slip must fail at least one hidden test.
"""
import contextlib, io, json, math, os, sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/py-found/homework-3.json')
doc = json.load(open(HW, encoding='utf-8'))
item = next(i for i in doc['items'] if i['id'] == 'h-cash-account')
w = item['widget']
fails = []


def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)


def run_tests(code, cases=None):
    res = []
    for t in (cases or w['tests']):
        ns = {'__learner_source__': code}
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(w['prelude'], ns)
                exec(code, ns)
                if t.get('setup'):
                    exec(t['setup'], ns)
                if t.get('compare') == 'raises':
                    try:
                        eval(t['call'], ns)
                        res.append(False)
                    except Exception as e:
                        res.append(t['expect'] in [k.__name__ for k in type(e).__mro__])
                    continue
                got = eval(t['call'], ns)
            res.append(bool(got == eval(t['expect'], ns)))
        except Exception as e:
            res.append(type(e).__name__)
    return res


SOL = w['solution']
REF = '''from fractions import Fraction


class Account:
    def __init__(self, opening=0.0):
        self.cash = Fraction(round(Fraction(str(opening)) * 100), 100)
        self.log = []

    def _amount(self, amount):
        if not amount > 0:
            raise ValueError("not above zero")
        return Fraction(round(Fraction(str(amount)) * 100), 100)

    def deposit(self, amount):
        x = self._amount(amount)
        self.cash += x
        self.log.append(float(x))

    def withdraw(self, amount):
        x = self._amount(amount)
        if x > self.cash:
            raise ValueError("more than the balance")
        self.cash -= x
        self.log.append(float(-x))

    def balance(self):
        return float(self.cash)

    def history(self):
        return list(self.log)
'''


def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)


FLOATS = '''class Account:
    def __init__(self, opening=0.0):
        self.money = opening
        self.moves = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("not above zero")
        self.money = self.money + amount
        self.moves.append(amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("not above zero")
        if amount > self.money:
            raise ValueError("too much")
        self.money = self.money - amount
        self.moves.append(-amount)

    def balance(self):
        return self.money

    def history(self):
        return self.moves
'''
FLOATS_ROUNDED = FLOATS.replace('self.money = self.money + amount', 'self.money = round(self.money + amount, 2)').replace(
    'self.money = self.money - amount', 'self.money = round(self.money - amount, 2)')

BUGS = {
    'pounds as floats': FLOATS,
    'int() truncates pence': variant('p = round(amount * 100)\n        self.pence = self.pence + p', 'p = int(amount * 100)\n        self.pence = self.pence + p').replace(
        'p = round(amount * 100)\n        if p > self.pence', 'p = int(amount * 100)\n        if p > self.pence'),
    '>= refuses the whole balance': variant('if p > self.pence:', 'if p >= self.pence:'),
    'no overdraft check': variant('        if p > self.pence:\n            raise ValueError(f"only £{self.pence / 100:.2f} to withdraw from")\n', ''),
    'changes the balance before checking': variant('        if p > self.pence:\n            raise ValueError(f"only £{self.pence / 100:.2f} to withdraw from")\n        self.pence = self.pence - p\n        self.moves.append(-p)\n',
                                                   '        self.pence = self.pence - p\n        self.moves.append(-p)\n        if self.pence < 0:\n            raise ValueError("overdrawn")\n'),
    'deposit check < 0 lets 0 through': variant('        if amount <= 0:\n            raise ValueError(f"a deposit', '        if amount < 0:\n            raise ValueError(f"a deposit'),
    'no deposit check': variant('        if amount <= 0:\n            raise ValueError(f"a deposit must be above zero: {amount}")\n', ''),
    'no check on a negative withdrawal': variant('        if amount <= 0:\n            raise ValueError(f"a withdrawal must be above zero: {amount}")\n', ''),
    'returns False instead of raising': variant('raise ValueError(f"only £{self.pence / 100:.2f} to withdraw from")', 'return False').replace(
        'raise ValueError(f"a deposit must be above zero: {amount}")', 'return False').replace('raise ValueError(f"a withdrawal must be above zero: {amount}")', 'return False'),
    'raises Exception, not ValueError': SOL.replace('raise ValueError(', 'raise Exception('),
    'history list in the class body': variant('class Account:\n    def __init__(self, opening=0.0):\n        self.pence = round(opening * 100)\n        self.moves = []\n',
                                              'class Account:\n    moves = []\n\n    def __init__(self, opening=0.0):\n        self.pence = round(opening * 100)\n'),
    'history in pence': variant('return [p / 100 for p in self.moves]', 'return self.moves'),
    'opening counted as a move': variant('        self.moves = []\n', '        self.moves = [self.pence]\n'),
    'balance in pence': variant('return self.pence / 100', 'return self.pence'),
    'balance printed, not returned': variant('return self.pence / 100', 'print(self.pence / 100)'),
    'opening ignored': variant('self.pence = round(opening * 100)', 'self.pence = 0'),
}

n = len(w['tests'])
for name, code in (('A solution', SOL), ('B Fractions', REF)):
    r = run_tests(code)
    check(f'{name} passes all {n} tests', all(x is True for x in r), str(r))
r = run_tests(FLOATS_ROUNDED)
check('pounds rounded to 2 places at every move also passes (exact by another route)', all(x is True for x in r), str(r))
check('solution passes the example', all(x is True for x in run_tests(SOL, w['examples'])))
check('example equals test 1', w['examples'][0] == w['tests'][0])
r = run_tests(w['starter'])
check('starter fails every test', all(x is not True for x in r), str(r))

for name, code in BUGS.items():
    r = run_tests(code)
    bad = [i + 1 for i, x in enumerate(r) if x is not True]
    check(f'slip "{name}" caught', bool(bad), f'fails tests {bad}')

for key, name in (('test-2', 'pounds as floats'), ('test-3', 'int() truncates pence'), ('test-4', '>= refuses the whole balance'),
                  ('test-6', 'changes the balance before checking'), ('test-7', 'deposit check < 0 lets 0 through'),
                  ('test-9', 'no check on a negative withdrawal'), ('test-10', 'history list in the class body')):
    check(f'byKey {key} present', key in item['feedback']['byKey'])
    check(f'slip "{name}" fails {key}', run_tests(BUGS[name])[int(key[5:]) - 1] is not True)

# Route C: integer pence for every stated figure.
check('example: 1000 + 250 - 400 = 850 pence = 8.5', 1000 + 250 - 400 == 850 and 850 / 100 == 8.5)
check('test 2: three deposits of 70p are 210p = 2.1', 3 * 70 == 210 and 210 / 100 == 2.1)
check('test 2: as floats they fall short of 2.1', 0.7 + 0.7 + 0.7 != 2.1 and 0.7 + 0.7 + 0.7 < 2.1)
check('test 3: 0.29 * 100 is under 29, int gives 28, round gives 29',
      0.29 * 100 < 29 and int(0.29 * 100) == 28 and round(0.29 * 100) == 29 and 29 / 100 == 0.29)
check('test 4: 1999 - 1999 = 0, move -19.99', round(19.99 * 100) == 1999 and -1999 / 100 == -19.99)
check('test 5: 10.01 is 1001p, over 1000p', round(10.01 * 100) == 1001 > 1000)
check('test 6: £25.00 is more than £10.00', 2500 > 1000)
check('fractions agree: 3 x 0.70 is exactly 2.10', 3 * F('0.70') == F('2.10'))
check('feedback test 9: a withdrawal of -5 would add money', 500 - (-500) == 1000)

n_t, n_e = len(w['tests']), len(w['examples'])
check('tests 10, examples 1, tests > examples', (n_t, n_e) == (10, 1) and n_t > n_e)
check('how states the test count', f'runs {n_t} hidden tests' in w['how'])
check('how names the raises tests 5 and 7', [i + 1 for i, t in enumerate(w['tests']) if t.get('compare') == 'raises'] == [5, 7])
check('how names the refused tests 6, 8 and 9', [i + 1 for i, t in enumerate(w['tests']) if 'refused(' in t.get('setup', '')] == [6, 8, 9])
check('homework items within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('one performance item in the homework', sum(1 for i in doc['items'] if i.get('performance')) == 1)

print(f'\n{len(fails)} failures')
sys.exit(1 if fails else 0)
