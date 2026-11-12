"""coding-1: my solutions (written from the statements before the models were read) and candidate-wrong solutions."""
CANDS = {}

CANDS['ds-arrays-sign-changes'] = {'mine': '''
def sign_changes(pnl):
    last = 0
    n = 0
    for x in pnl:
        if x == 0:
            continue
        if last and (x > 0) != (last > 0):
            n += 1
        last = x
    return n
''', 'wrong': [
    ('zero-as-a-loss', 'a flat day is read as a loss (sign is x > 0): [1, 0, 2] gives 2, [0, 5] gives 1', '''
def sign_changes(pnl):
    n = 0
    for a, b in zip(pnl, pnl[1:]):
        if (a > 0) != (b > 0):
            n += 1
    return n
'''),
    ('zero-as-a-gain', 'a flat day is read as a gain (sign is x >= 0)', '''
def sign_changes(pnl):
    return sum(1 for a, b in zip(pnl, pnl[1:]) if (a >= 0) != (b >= 0))
'''),
    ('neighbours-only', 'the product of neighbours, so a flat day breaks the chain', '''
def sign_changes(pnl):
    return sum(1 for a, b in zip(pnl, pnl[1:]) if a * b < 0)
'''),
    ('first-element', 'reads pnl[0] with no guard for the empty list', '''
def sign_changes(pnl):
    xs = [x for x in pnl if x]
    last = xs[0]
    n = 0
    for x in xs[1:]:
        if x * last < 0:
            n += 1
        last = x
    return n
'''),
    ('remove-zeros-in-place', 'the slower order and a changed input: list.remove(0) in a loop is quadratic', '''
def sign_changes(pnl):
    while 0 in pnl:
        pnl.remove(0)
    return sum(1 for a, b in zip(pnl, pnl[1:]) if a * b < 0)
'''),
    ('skip-one-zero', 'looks back two places, so one flat day is skipped but two in a row are not', '''
def sign_changes(pnl):
    n = 0
    for i in range(1, len(pnl)):
        if pnl[i] == 0:
            continue
        j = i - 1
        if pnl[j] == 0 and j > 0:
            j -= 1
        if pnl[i] * pnl[j] < 0:
            n += 1
    return n
'''),
    ('counts-runs', 'off by one: counts the runs of one sign, not the flips between them', '''
def sign_changes(pnl):
    xs = [x > 0 for x in pnl if x]
    return sum(1 for i, s in enumerate(xs) if i == 0 or s != xs[i - 1])
'''),
]}

CANDS['ds-hashing-price-mode'] = {'mine': '''
def price_mode(prices):
    if not prices:
        return None
    count = {}
    for p in prices:
        count[p] = count.get(p, 0) + 1
    return max(count, key=lambda p: (count[p], p))
''', 'wrong': [
    ('set-count', 'max(set(xs), key=xs.count): a tie goes to whichever price the set yields first', '''
def price_mode(prices):
    if not prices:
        return None
    return max(set(prices), key=prices.count)
'''),
    ('most-common', 'Counter.most_common: a tie goes to the price seen first', '''
from collections import Counter
def price_mode(prices):
    if not prices:
        return None
    return Counter(prices).most_common(1)[0][0]
'''),
    ('tie-to-lowest', 'a tie goes to the lowest price', '''
def price_mode(prices):
    if not prices:
        return None
    c = {}
    for p in prices:
        c[p] = c.get(p, 0) + 1
    return max(c, key=lambda p: (c[p], -p))
'''),
    ('no-empty-case', 'no guard for the empty list', '''
def price_mode(prices):
    c = {}
    for p in prices:
        c[p] = c.get(p, 0) + 1
    return max(c, key=lambda p: (c[p], p))
'''),
    ('strict-greater-scan', 'one pass over sorted prices keeping the first best run, so a tie goes to the lowest', '''
def price_mode(prices):
    best = None
    bestn = 0
    xs = sorted(prices)
    i = 0
    while i < len(xs):
        j = i
        while j < len(xs) and xs[j] == xs[i]:
            j += 1
        if j - i > bestn:
            best, bestn = xs[i], j - i
        i = j
    return best
'''),
    ('tie-by-size', 'a tie goes to the price that is largest in size, so -5 beats -3', '''
def price_mode(prices):
    if not prices:
        return None
    c = {}
    for p in prices:
        c[p] = c.get(p, 0) + 1
    return max(c, key=lambda p: (c[p], abs(p)))
'''),
    ('alt:quadratic-count', 'right answers by the slower order: xs.count for every distinct price, highest first', '''
def price_mode(prices):
    if not prices:
        return None
    return max(sorted(set(prices), reverse=True), key=prices.count)
'''),
]}

CANDS['edge-case-list-to-pence'] = {'mine': '''
def to_pence(text):
    s = text.strip()
    neg = s.startswith('-')
    if neg:
        s = s[1:]
    s = s.replace('£', '').replace(',', '').strip()
    whole, _, frac = s.partition('.')
    frac = (frac + '00')[:2]
    v = int(whole or '0') * 100 + int(frac)
    return -v if neg else v
''', 'wrong': [
    ('float-truncate', 'int(float(s) * 100): 0.29 gives 28', '''
def to_pence(text):
    s = text.strip().replace('£', '').replace(',', '')
    return int(float(s) * 100)
'''),
    ('alt:float-round', 'round(float(s) * 100): right for every price below about 10 to the 13 pounds, wrong above', '''
def to_pence(text):
    s = text.strip().replace('£', '').replace(',', '')
    return round(float(s) * 100)
'''),
    ('sign-on-pounds-only', 'the sign stays on the pounds, so -£2.05 is -200 + 5', '''
def to_pence(text):
    s = text.strip().replace('£', '').replace(',', '')
    whole, _, frac = s.partition('.')
    frac = (frac + '00')[:2]
    return int(whole) * 100 + int(frac)
'''),
    ('no-padding', 'one decimal place is read as pence, so 3.5 gives 305', '''
def to_pence(text):
    s = text.strip()
    neg = s.startswith('-')
    s = s.lstrip('-').replace('£', '').replace(',', '')
    whole, _, frac = s.partition('.')
    v = int(whole) * 100 + int(frac or 0)
    return -v if neg else v
'''),
    ('first-comma-only', 'drops one comma only', '''
def to_pence(text):
    s = text.strip()
    neg = s.startswith('-')
    s = s.lstrip('-').replace('£', '').replace(',', '', 1)
    whole, _, frac = s.partition('.')
    v = int(whole) * 100 + int((frac + '00')[:2])
    return -v if neg else v
'''),
    ('no-strip', 'does not strip the spaces before looking for the sign and the £', '''
def to_pence(text):
    s = text
    neg = s[0] == '-'
    if neg:
        s = s[1:]
    if s[0] == '£':
        s = s[1:]
    s = s.replace(',', '')
    whole, _, frac = s.partition('.')
    v = int(whole) * 100 + int((frac + '00')[:2])
    return -v if neg else v
'''),
    ('returns-float', 'returns a float of pence (the statement asks for an int)', '''
def to_pence(text):
    s = text.strip().replace('£', '').replace(',', '')
    return float(round(float(s) * 100))
'''),
]}

CANDS['integer-division-lot-round'] = {'mine': '''
def lot_round(qty, lot):
    lots = abs(qty) // lot
    return lots * lot if qty >= 0 else -(lots * lot)
''', 'wrong': [
    ('floor', 'qty // lot * lot rounds a negative quantity away from zero', '''
def lot_round(qty, lot):
    return qty // lot * lot
'''),
    ('float-divide', 'int(qty / lot) * lot goes through a float', '''
def lot_round(qty, lot):
    return int(qty / lot) * lot
'''),
    ('python-mod', 'qty - qty % lot: the Python remainder is never negative', '''
def lot_round(qty, lot):
    return qty - qty % lot
'''),
    ('fmod', 'qty - fmod(qty, lot) returns a float', '''
import math
def lot_round(qty, lot):
    return qty - math.fmod(qty, lot)
'''),
    ('fmod-small', 'fmod for the remainder, cast to int: exact for every qty a float holds, wrong above 2 to the 53', '''
import math
def lot_round(qty, lot):
    return qty - int(math.fmod(qty, lot))
'''),
    ('copysign', 'copysign makes a float of the rounded size', '''
import math
def lot_round(qty, lot):
    return int(math.copysign(abs(qty) // lot * lot, qty))
'''),
    ('lots-not-shares', 'returns the number of lots, not the quantity', '''
def lot_round(qty, lot):
    lots = abs(qty) // lot
    return lots if qty >= 0 else -lots
'''),
    ('round-nearest', 'rounds to the nearest lot', '''
def lot_round(qty, lot):
    lots = (abs(qty) + lot // 2) // lot
    return lots * lot if qty >= 0 else -(lots * lot)
'''),
]}

CANDS['pf-types-parse-fix'] = {'mine': '''
def parse_fix(msg):
    out = {}
    if not msg:
        return out
    for field in msg.split(';'):
        tag, _, value = field.partition('=')
        out[int(tag)] = value
    return out
''', 'wrong': [
    ('split-all', 'split("=") with two names: a value holding = raises', '''
def parse_fix(msg):
    out = {}
    if not msg:
        return out
    for field in msg.split(';'):
        tag, value = field.split('=')
        out[int(tag)] = value
    return out
'''),
    ('split-all-keep-second', 'split("=")[1]: a value holding = is cut at its own =', '''
def parse_fix(msg):
    out = {}
    if not msg:
        return out
    for field in msg.split(';'):
        parts = field.split('=')
        out[int(parts[0])] = parts[1]
    return out
'''),
    ('text-tags', 'tags left as text', '''
def parse_fix(msg):
    if not msg:
        return {}
    return dict(field.split('=', 1) for field in msg.split(';'))
'''),
    ('first-value-kept', 'a repeated tag keeps its first value', '''
def parse_fix(msg):
    out = {}
    if not msg:
        return out
    for field in msg.split(';'):
        tag, _, value = field.partition('=')
        out.setdefault(int(tag), value)
    return out
'''),
    ('no-empty-guard', 'no guard for the empty message', '''
def parse_fix(msg):
    out = {}
    for field in msg.split(';'):
        tag, _, value = field.partition('=')
        out[int(tag)] = value
    return out
'''),
    ('last-equals', 'splits at the last =', '''
def parse_fix(msg):
    out = {}
    if not msg:
        return out
    for field in msg.split(';'):
        tag, _, value = field.rpartition('=')
        out[int(tag)] = value
    return out
'''),
    ('numbers-as-int', 'a value that is all digits becomes an int', '''
def parse_fix(msg):
    out = {}
    if not msg:
        return out
    for field in msg.split(';'):
        tag, _, value = field.partition('=')
        out[int(tag)] = int(value) if value.isdigit() else value
    return out
'''),
    ('alt:skip-empty-fields', 'skips empty fields, so the empty message works with no special case (also right)', '''
def parse_fix(msg):
    out = {}
    for field in msg.split(';'):
        if field:
            tag, _, value = field.partition('=')
            out[int(tag)] = value
    return out
'''),
]}

CANDS['pf-functions-binom-tail'] = {'mine': '''
from fractions import Fraction
from math import comb

def binom_tail(n, k):
    if k <= 0:
        return Fraction(1)
    if k > n:
        return Fraction(0)
    return Fraction(sum(comb(n, j) for j in range(k, n + 1)), 2 ** n)
''', 'wrong': [
    ('strictly-more', 'more than k heads, not at least k', '''
from fractions import Fraction
from math import comb
def binom_tail(n, k):
    k = max(k, -1)
    return Fraction(sum(comb(n, j) for j in range(k + 1, n + 1)), 2 ** n)
'''),
    ('float', 'returns a float', '''
from math import comb
def binom_tail(n, k):
    return sum(comb(n, j) for j in range(max(k, 0), n + 1)) / 2 ** n
'''),
    ('fraction-of-float', 'Fraction(float): exact only while the numerator fits 53 bits', '''
from fractions import Fraction
from math import comb
def binom_tail(n, k):
    return Fraction(sum(comb(n, j) for j in range(max(k, 0), n + 1)) / 2 ** n)
'''),
    ('negative-k', 'a negative k reaches comb', '''
from fractions import Fraction
from math import comb
def binom_tail(n, k):
    return Fraction(sum(comb(n, j) for j in range(k, n + 1)), 2 ** n)
'''),
    ('at-most', 'at most k heads', '''
from fractions import Fraction
from math import comb
def binom_tail(n, k):
    return Fraction(sum(comb(n, j) for j in range(0, min(k, n) + 1)), 2 ** n)
'''),
    ('plain-recursion', 'right, by the slower order: Pascal recursion with no memory', '''
from fractions import Fraction
def binom_tail(n, k):
    if k <= 0:
        return Fraction(1)
    if k > n:
        return Fraction(0)
    return (binom_tail(n - 1, k - 1) + binom_tail(n - 1, k)) / 2
'''),
    ('exactly-k', 'exactly k heads', '''
from fractions import Fraction
from math import comb
def binom_tail(n, k):
    if k < 0 or k > n:
        return Fraction(0)
    return Fraction(comb(n, k), 2 ** n)
'''),
]}
