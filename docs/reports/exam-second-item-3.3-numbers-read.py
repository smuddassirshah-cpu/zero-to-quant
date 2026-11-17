"""Second read of the nine new topic-3.3 exam items (exam second item, session AG).

Every key, wrong value and printed number is recomputed by a route that does not use the
explanation's closed form: enumeration, an exact piecewise integral, a knowledge model or a
seeded simulation. Structure (36 items, 90 minutes, removals, two auto items a skill) and the
reuse of lesson number sets are checked too. The fixes proposed in
docs/reviews/review-exam-second-item-3.3.md are recomputed at the end.

Run from anywhere: python3 docs/reports/exam-second-item-3.3-numbers-read.py
Exit 0 always; a FINDING line is printed for each failing check.
"""
import datetime
import itertools
import json
import os
import random
import subprocess
from collections import Counter, defaultdict
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
CONTENT = os.path.join(ROOT, 'app', 'content')
EXAM_REL = 'app/content/exams/topic-3.3.json'
AUTHOR_COMMIT = '1eea0d98'
exam = json.load(open(os.path.join(ROOT, EXAM_REL), encoding='utf-8'))
ITEMS = {i['id']: i for i in exam['items']}
NEW = ['e-divide-4512', 'e-thousand-days', 'e-bags-any-fake', 'e-divides-forty', 'e-bluff-or-check',
       'e-consecutive-numbers', 'e-second-price-win', 'e-alerts-close', 'e-tree-plans']
REMOVED = {'e-even-faces': ['pz-expectation'], 'e-edge-lift': ['mg-quote'], 'e-ten-cards': ['mg-update']}
PAIRS = ['bz-invariant', 'bz-quick', 'bz-search', 'bz-strategy', 'gm-auction', 'gm-mixed', 'gm-normal',
         'gm-poker', 'gm-sequential', 'mp-speed', 'pz-conditioning', 'pz-geometry']
COURSES = ['brainteasers', 'game-theory', 'mental-pressure', 'mm-games', 'puzzles']
checks = 0
findings = 0


def check(ok, label):
    global checks, findings
    checks += 1
    if not ok:
        findings += 1
        print('FINDING', label)


def near(a, b, t=1e-9):
    return abs(float(a) - float(b)) <= t


def load(rel):
    return json.load(open(os.path.join(CONTENT, rel), encoding='utf-8'))


def is_auto(it):
    w = it.get('widget') or {}
    return it.get('kind') != 'longform' and w.get('kind') not in (None, 'longform')


def auto_counts(items):
    c = Counter()
    for it in items:
        if is_auto(it):
            for s in it.get('skills', []):
                c[s] += 1
    return c


def wrongs(iid):
    return {w['id']: w['value'] for w in ITEMS[iid]['widget'].get('wrong', [])}


def key(iid):
    return ITEMS[iid]['widget']['answer']


def chosen(iid):
    return [o['id'] for o in ITEMS[iid]['widget']['options'] if o.get('correct')]


# ---------------------------------------------------------------- structure
check(len(exam['items']) == 36, 'exam holds 36 items')
check(20 <= len(exam['items']) <= 36, 'item count inside the validator cap 20 to 36')
check(exam['minutes'] == 90 and 5 * round(75 * 36 / 30 / 5) == 90, 'minutes 75 x 36 / 30 = 90')
check(all(i in ITEMS for i in NEW), 'all nine new ids present')
check(all(i not in ITEMS for i in REMOVED), 'three removed ids absent')
now = auto_counts(exam['items'])
check(all(now[s] >= 2 for s in exam['skills']), 'every exam skill has two auto items: %s' % {s: now[s] for s in exam['skills'] if now[s] < 2})
check(all(now[s] >= 2 for s in PAIRS), 'every listed pair now has two auto items')

# essential skills of each level (skills on its review items) and the pairs before the edit
essential = defaultdict(set)
for c in COURSES:
    for lv in load('courses/%s/course.json' % c)['levels']:
        for it in load('courses/%s/%s.json' % (c, lv['review']))['items']:
            for s in it.get('skills', []):
                essential[s].add('%s L%s' % (c, lv['n']))
try:
    old_txt = subprocess.run(['git', '-C', ROOT, 'show', AUTHOR_COMMIT + '~1:' + EXAM_REL], capture_output=True, text=True, check=True).stdout
    old = json.loads(old_txt)
    before = auto_counts(old['items'])
    old_ids = {i['id']: i for i in old['items']}
    pairs = sorted(s for s in essential if s in old['skills'] and before[s] <= 1)
    check(pairs == sorted(PAIRS), 'pairs before the edit are the twelve listed: %s' % pairs)
    check(len(old['items']) == 30 and old['minutes'] == 75, 'the exam held 30 items and 75 minutes before')
    check(set(ITEMS) - set(old_ids) == set(NEW), 'new ids are exactly the nine listed')
    check(set(old_ids) - set(ITEMS) == set(REMOVED), 'removed ids are exactly the three listed')
    for rid, sk in REMOVED.items():
        check(old_ids[rid]['skills'] == sk, '%s carried %s' % (rid, sk))
        check(all(now[s] >= 2 for s in sk), '%s: each skill keeps two auto items after removal' % rid)
        check(all(before[s] - 1 >= 2 for s in sk), '%s: each skill had two other auto items before any new one' % rid)
    kept = [i for i in old['items'] if i['id'] in ITEMS]
    check(all(json.dumps(i, sort_keys=True) == json.dumps(ITEMS[i['id']], sort_keys=True) for i in kept), 'the 27 kept items are unchanged')
except Exception as e:  # no git history available: the checks above on the current file still hold
    print('note: history checks skipped (%s)' % type(e).__name__)
for iid, sk in [('e-divide-4512', ['mp-speed']), ('e-thousand-days', ['bz-quick']), ('e-bags-any-fake', ['bz-search']),
                ('e-divides-forty', ['bz-invariant']), ('e-bluff-or-check', ['gm-poker', 'gm-mixed']),
                ('e-consecutive-numbers', ['bz-strategy']), ('e-second-price-win', ['gm-auction']),
                ('e-alerts-close', ['pz-conditioning', 'pz-geometry']), ('e-tree-plans', ['gm-sequential', 'gm-normal'])]:
    check(ITEMS[iid]['skills'] == sk, '%s skills %s' % (iid, sk))
ramp = Counter(i['difficulty'] for i in exam['items'])
check(dict(ramp) == {2: 7, 3: 18, 4: 7, 5: 4}, 'ramp 7, 18, 7, 4: %s' % dict(ramp))

# bands: no wrong value inside the key's band, no two wrong bands touching, no key on a rounding tie
for iid in NEW:
    w = ITEMS[iid]['widget']
    if w['kind'] != 'numeric':
        continue
    tol = w['tol']['abs']
    vals = [(x['id'], x['value'], x['tol']['abs']) for x in w.get('wrong', [])]
    check(all(abs(v - w['answer']) > tol + t for _, v, t in vals), '%s: a wrong value sits in the key band' % iid)
    check(all(abs(a[1] - b[1]) > a[2] + b[2] for a, b in itertools.combinations(vals, 2)), '%s: two wrong bands touch' % iid)

# ---------------------------------------------------------------- e-divide-4512 (repeated subtraction)
q, r = 0, 4512
while r >= 48:
    r -= 48
    q += 1
check((q, r) == (94, 0) and key('e-divide-4512') == 94, 'divide: 4512 / 48 = 94 exactly')
w = wrongs('e-divide-4512')
check(w == {'place': 940, 'point': 9.4, 'short': 93}, 'divide: wrong values 940, 9.4, 93')
check(sum([48] * 940) == 45120 > 45000, 'divide: 48 x 940 is over 45,000')
check(round(48 * 9.4) == 451, 'divide: 48 x 9.4 is about 451')
check(sum([48] * 93) == 4464 and 4512 - 4464 == 48, 'divide: 48 x 93 = 4464, 48 over')
check(sum([48] * 90) == 4320 and 4512 - 4320 == 192 == 48 * 4, 'divide: 4320, 192 = 48 x 4')
check(50 * 94 == 4700 and 2 * 94 == 188 and 4700 - 188 == 4512, 'divide: the check line')

# ---------------------------------------------------------------- e-thousand-days (a real calendar)
monday = datetime.date(2026, 11, 16)
check(monday.strftime('%A') == 'Monday', 'days: the anchor date is a Monday')
day = lambda n: (monday + datetime.timedelta(days=n)).strftime('%A').lower()
check(chosen('e-thousand-days') == [day(1000)] == ['sunday'], 'days: 1000 days after a Monday is a Sunday')
check(day(999) == 'saturday', 'days: counting today as day 1 gives Saturday')
check(day(-6) == 'tuesday', 'days: six days back gives Tuesday')
check(day(994) == 'monday' and 994 == 7 * 142 and 1000 - 994 == 6, 'days: 994 = 7 x 142, remainder 6')
check(day(1) == 'tuesday', 'days: day 1 is Tuesday')

# ---------------------------------------------------------------- e-bags-any-fake (search over every way to take coins)
def tells_apart(counts):
    sums = set()
    for mask in itertools.product((0, 1), repeat=len(counts)):
        s = sum(c for c, m in zip(counts, mask) if m)
        if s in sums:
            return False
        sums.add(s)
    return True


best = None
for total in range(5, 33):
    hits = [c for c in itertools.combinations_with_replacement(range(0, total + 1), 5) if sum(c) == total and tells_apart(c)] if total <= 31 else []
    if hits:
        best = (total, hits)
        break
check(best is not None and best[0] == 31 == key('e-bags-any-fake'), 'bags: the fewest coins is 31 (search over every 5-way split of 5 to 31 coins)')
check(best is not None and best[1] == [(1, 2, 4, 8, 16)], 'bags: the only 31-coin plan is 1, 2, 4, 8, 16')
w = wrongs('e-bags-any-fake')
check(w == {'k-from-k': 15, 'patterns': 32, 'one-each': 5}, 'bags: wrong values 15, 32, 5')
check(not tells_apart((1, 2, 3, 4, 5)) and 1 + 4 == 2 + 3 == 5, 'bags: 1 to 5 coins confuses bags 1 and 4 with 2 and 3 at 5 g over')
check(2 ** 5 == 32 and 31 * 10 == 310, 'bags: 32 patterns, 310 g for 31 genuine coins')
check(len({sum(m) for m in itertools.product((0, 1), repeat=5)}) == 6, 'bags: one coin each gives only the number of fake bags')

# ---------------------------------------------------------------- e-divides-forty (largest set with no divisor pair, by matching)
def largest_free(lo, hi):
    """Largest subset of lo..hi with no pair a | b: Dilworth, size = n - maximum matching of the divisibility order."""
    nums = list(range(lo, hi + 1))
    adj = {a: [b for b in nums if b > a and b % a == 0] for a in nums}
    match = {}

    def aug(a, seen):
        for b in adj[a]:
            if b in seen:
                continue
            seen.add(b)
            if b not in match or aug(match[b], seen):
                match[b] = a
                return True
        return False

    m = sum(1 for a in nums if aug(a, set()))
    return len(nums) - m


free = largest_free(11, 40)
check(free == 20 and key('e-divides-forty') == free + 1 == 21, 'divisors: 20 numbers from 11 to 40 can avoid a pair, so 21 force one (retargeted to the fixed item)')
check(all(b % a for a, b in itertools.combinations(range(21, 41), 2)), 'divisors: 21 to 40 holds no divisor pair')
odd = lambda n: n if n % 2 else odd(n // 2)
check(len({odd(n) for n in range(11, 41)}) == 20, 'divisors: 20 odd parts')
check(wrongs('e-divides-forty') == {'boxes': 20, 'half': 16, 'all': 31}, 'divisors: wrong values 20, 16 and 31')
check('fewest' in ITEMS['e-divides-forty']['question'],
      'divisors: the question asks for the fewest, so 22 to 30 do not count as the answer (review 3, applied)')
# the course's pigeonhole items on "pick from 1 to 2n" all key n + 1 (l3: 1 to 12 gives 7; review-1: 1 to 100 gives 51)
m_lo, m_hi = [int(x) for x in __import__('re').search(r'from (\d+) to (\d+)', ITEMS['e-divides-forty']['prose']).groups()]
check(key('e-divides-forty') != (m_hi - m_lo + 1) // 2 + 1 or (m_lo, m_hi) == (11, 40), 'divisors: the range 11 to 40 keeps the key 21 but is not the half-plus-one pattern of l3-pigeonhole and review-1 r6-consecutive (review 4, applied)')

# ---------------------------------------------------------------- e-bluff-or-check (bisection and a seeded simulation)
POT, BET, SHOW = 90, 60, F(1, 5)
ev_bet = lambda c: POT * (1 - c) - BET * c
lo, hi = F(0), F(1)
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if ev_bet(mid) > POT * SHOW else (lo, mid)
check(near(lo, 0.48, 1e-9) and key('e-bluff-or-check') == 0.48, 'bluff: bet and check earn the same at c = 0.48')
check(ev_bet(F(12, 25)) == POT * SHOW == 18 and F(72, 150) == F(12, 25), 'bluff: both earn 18; 72/150 = 0.48')
rng = random.Random(33)
n = 400000
bet_avg = sum((-BET if rng.random() < 0.48 else POT) for _ in range(n)) / n
chk_avg = sum((POT if rng.random() < 0.2 else 0) for _ in range(n)) / n
check(abs(bet_avg - chk_avg) < 0.8, 'bluff: simulated averages agree at c = 0.48 (%.2f, %.2f)' % (bet_avg, chk_avg))
w = wrongs('e-bluff-or-check')
check(near(w['formula'], F(POT, POT + BET)) and ev_bet(F(POT, POT + BET)) == 0, 'bluff: 0.6 = P/(P+B) makes a worthless bluff break even')
check(near(w['no-loss'], 1 - SHOW), 'bluff: 0.8 from 90(1 - c) = 18')
check(near(w['folds'], 1 - F(12, 25)), 'bluff: 0.52 is the fold share')
share = F(BET, POT + 2 * BET)
check(near(w['bluff-share'], 0.29) and F(57, 200) < share < F(59, 200) and share * 100 % 1 != F(1, 2), 'bluff: 60/210 = 0.2857 rounds to 0.29, no tie')
check(0.48 < 0.6, 'bluff: Ben calls less than P/(P+B)')

# ---------------------------------------------------------------- e-consecutive-numbers (knowledge model)
TOP = 40
worlds = {(a, b) for a in range(1, TOP + 1) for b in range(1, TOP + 1) if abs(a - b) == 1}


def first_knower(true_world, worlds):
    live = set(worlds)
    for stmt in range(1, 30):
        who = 0 if stmt % 2 else 1  # Ana speaks on odd statements
        knows = {w for w in live if sum(1 for v in live if v[who] == w[who]) == 1}
        if true_world in knows:
            return ('ana' if who == 0 else 'ben', stmt)
        live -= knows  # 'I don't know' removes every world where the speaker would have known
    return None


check(first_knower((3, 4), worlds) == ('ana', 3) and chosen('e-consecutive-numbers') == ['ana-3'], 'consecutive: Ana knows first, on statement 3')
check(first_knower((1, 2), worlds) == ('ana', 1) and first_knower((3, 2), worlds) == ('ben', 2), 'consecutive: Ana with 1 knows at once; Ben with 2 knows on statement 2')
check(first_knower((3, 4), {w for w in worlds if max(w) <= 12}) == ('ana', 3), 'consecutive: the answer does not depend on the model cap')

# ---------------------------------------------------------------- e-second-price-win (exact grid and simulation)
def price_given_win(n_bidders, value, grid=1200):
    """E[highest rival | all rivals below value], rivals uniform on 0..100: exact for a fine grid of cells, by order statistics of cell counts."""
    k = n_bidders - 1
    cells = int(grid * value / 100)
    tot = F(0)
    for j in range(cells):  # the maximum falls in cell j with chance ((j+1)^k - j^k) / cells^k; its mean there lies inside the cell
        tot += F((j + 1) ** k - j ** k, cells ** k) * F(2 * j + 1, 2) * F(100, grid)
    return tot


g = price_given_win(4, 60)
rng = random.Random(8)
tot = 0.0
N = 600000
for _ in range(N):
    m = max(rng.uniform(0, 100), rng.uniform(0, 100), rng.uniform(0, 100))
    tot += m if m < 60 else 0.0
check(abs(float(g) - 45) < 0.05 and F(6, 10) ** 3 * 45 == F(243, 25) and abs(tot / N - 9.72) < 0.08 and key('e-second-price-win') == 9.72,
      'auction: expected payment is 9.72 (retargeted to the fixed item; price given a win %.3f, simulation %.3f)' % (g, tot / N))
w = wrongs('e-second-price-win')
check(w == {'given-win': 45, 'own-bid': 12.96, 'seller-share': 15}, 'auction: wrong values 45, 12.96 and 15')
check(near(w['own-bid'], float(F(27, 125) * 60)) and w['seller-share'] == 60 / 4, 'auction: 12.96 = 0.216 x 60 and 15 = 60 / 4')
# reuse: game-theory l8-sealed-bids screens[6] asked "Three bidders, first price, value 90" and keyed 60; the fixed item no longer shares it
l8 = load('courses/game-theory/l8-sealed-bids.json')['screens'][6]
same = ('Three bidders, first price, value £90' in l8['question'] and 'three bidders' in ITEMS['e-second-price-win']['prose']
        and '£90' in ITEMS['e-second-price-win']['prose'] and key('e-second-price-win') == 60)
check(not same, 'auction: REUSE of l8-sealed-bids screens[6] (three bidders, value 90, key 60, options 45 and 90) (review 1)')

# ---------------------------------------------------------------- e-alerts-close (exact piecewise integral and simulation)
def close_areas(gap_min):
    """P(|X - Y| < gap) and P(that and both below 30), X, Y uniform on 0..60 minutes: trapezium rule on whole minutes, exact because
    the section length is linear between whole minutes when gap is a whole number of minutes."""
    def section(x, top):  # length of y in [0, top] with |x - y| < gap
        return max(F(0), min(F(top), x + gap_min) - max(F(0), x - gap_min))
    def area(xtop, ytop):
        return sum((section(F(x), ytop) + section(F(x + 1), ytop)) / 2 for x in range(xtop)) / 3600
    return area(60, 60), area(30, 30)


p_close, p_both = close_areas(18)
check(p_close == F(51, 100) and p_both == F(21, 100), 'alerts: areas 51/100 and 21/100 (retargeted to 18 minutes)')
check(p_both / p_close == F(7, 17) and key('e-alerts-close') == 0.4118, 'alerts: conditional chance 7/17 = 0.4118')
rng = random.Random(21)
hit = tot = 0
for _ in range(600000):
    x, y = rng.uniform(0, 60), rng.uniform(0, 60)
    if abs(x - y) < 18:
        tot += 1
        hit += x < 30 and y < 30
check(abs(hit / tot - 0.4118) < 0.004, 'alerts: simulation %.4f' % (hit / tot))
w = wrongs('e-alerts-close')
check(w['unconditional'] == 0.25, 'alerts: 1/4 unconditional')
check(near(w['joint'], round(float(p_both), 4)), 'alerts: joint 0.21')
check(near(w['no-corners'], F(1, 4) / p_close, 0.00005) and F(25, 51) == F(1, 4) / p_close, 'alerts: 0.4902 keeps the corners')
check(near(w['condition'], round(float(p_close), 4)), 'alerts: condition 0.51')
check(F(1, 4) - p_both == F(1, 25) == 2 * F(1, 2) * F(1, 5) ** 2 and 1 - F(7, 10) ** 2 == F(51, 100), 'alerts: corner triangles 1/25 in all')
check(p_both / p_close > F(1, 4), 'alerts: closeness makes an early pair likelier')
# reuse: puzzles l24-mixed-set screens[8] drill row "each waits 20 minutes" keys 0.5556, the item's condition and its 'condition' value
l24 = json.dumps(load('courses/puzzles/l24-mixed-set.json')['screens'][8], ensure_ascii=False)
same = 'each waits 20 minutes' in l24 and '0.5556' in l24 and 'within 20 minutes' in ITEMS['e-alerts-close']['prose']
check(not same, 'alerts: (applied: the item now says 18 minutes) number set shared with puzzles l24-mixed-set screens[8] (an hour, 20 minutes, 0.5556) (review 2)')

# ---------------------------------------------------------------- e-tree-plans (every cell of the 2 x 9 table)
leaves = {}
for mv in ITEMS['e-tree-plans']['canvas']['params']['nodes']['children']:
    for ans in mv['children']:
        a, b = [int(x) for x in ans['value'].strip('()').split(',')]
        leaves[(mv['label'], ans['label'])] = (a, b)
check(leaves == {('Left', 'X'): (1, 4), ('Left', 'Y'): (0, 3), ('Left', 'Z'): (4, 0), ('Right', 'X'): (5, 1), ('Right', 'Y'): (0, 0), ('Right', 'Z'): (2, 2)},
      'tree: payoffs as printed')
plans = list(itertools.product('XYZ', repeat=2))
out = lambda mv, plan: leaves[(mv, plan[0] if mv == 'Left' else plan[1])]
nash = [(mv, ''.join(p)) for mv in ('Left', 'Right') for p in plans
        if all(out(m2, p)[0] <= out(mv, p)[0] for m2 in ('Left', 'Right')) and all(out(mv, p2)[1] <= out(mv, p)[1] for p2 in plans)]
check(sorted(nash) == [('Left', 'XY'), ('Right', 'XZ'), ('Right', 'YZ')] and key('e-tree-plans') == 3, 'tree: three Nash cells, Left XY, Right XZ, Right YZ')
best = {mv: max('XYZ', key=lambda a: leaves[(mv, a)][1]) for mv in ('Left', 'Right')}
spe = max(('Left', 'Right'), key=lambda mv: leaves[(mv, best[mv])][0])
check(best == {'Left': 'X', 'Right': 'Z'} and spe == 'Right' and leaves[('Right', 'Z')] == (2, 2) and leaves[('Left', 'X')][0] == 1, 'tree: backward induction gives Right then Z; Left would pay Ana 1')
w = wrongs('e-tree-plans')
check(w['tree-only'] == 1 and w['right-only'] == sum(1 for c in nash if c[0] == 'Right') == 2 and w['plans'] == len(plans) == 9, 'tree: wrong values 1, 2, 9')
simul = [(mv, a) for mv in ('Left', 'Right') for a in 'XYZ'
         if all(leaves[(m2, a)][0] <= leaves[(mv, a)][0] for m2 in ('Left', 'Right')) and all(leaves[(mv, a2)][1] <= leaves[(mv, a)][1] for a2 in 'XYZ')]
check(w['actions'] == len(simul) == 0, 'tree: the 2 x 3 table of single answers has no pure equilibrium')
check(leaves[('Right', 'Y')][0] == 0 < 1, 'tree: Y after Right holds Ana to 0')

# ---------------------------------------------------------------- fixes proposed in the review, recomputed
# review 1: four bidders, value 60, expected payment counting a loss as 0
p_win = F(60, 100) ** 3
pay = p_win * 45
g4 = price_given_win(4, 60)
rng = random.Random(14)
tot = 0.0
N = 400000
for _ in range(N):
    m = max(rng.uniform(0, 100), rng.uniform(0, 100), rng.uniform(0, 100))
    tot += m if m < 60 else 0.0
check(abs(float(g4) - 45) < 0.05 and pay == F(243, 25) and abs(tot / N - 9.72) < 0.08, 'fix 1: payment 0.216 x 45 = 9.72 (simulation %.3f)' % (tot / N))
check(p_win == F(27, 125) and near(p_win * 60, 12.96) and F(3, 5) * 100 / 4 == 15, 'fix 1: wrong values 45, 12.96 and 15')
for name in ('l8-sealed-bids', 'l9-winners-curse', 'review-2', 'homework-2'):
    t = json.dumps(load('courses/game-theory/%s.json' % name), ensure_ascii=False)
    check('9.72' not in t and not __import__('re').search(r'[Ff]our bidders[^"\]]{0,60}£60', t), 'fix 1: four bidders at 60 is not in %s' % name)
# review 2: a gap of 18 minutes (12 and 24 minutes give 9/25 and 0.64, both printed in puzzles l16-meeting)
pc, pb = close_areas(18)
check(pc == F(51, 100) and pb == F(21, 100) and pb / pc == F(7, 17), 'fix 2: 18 minutes gives 0.51, 0.21 and 7/17')
check(round(float(F(7, 17)), 4) == 0.4118 and 1 - F(7, 10) ** 2 == F(51, 100), 'fix 2: key 0.4118, condition 1 - (7/10)^2')
check(F(1, 4) / pc == F(25, 51) and round(float(F(25, 51)), 4) == 0.4902 and F(1, 4) - pb == F(1, 25) == 2 * F(1, 2) * F(1, 5) ** 2, 'fix 2: no-corners 0.4902, triangles of leg 1/5')
check(all(abs(a - b) > 0.001 for a, b in itertools.combinations([0.4118, 0.25, 0.21, 0.4902, 0.51], 2)), 'fix 2: bands clear at 0.0005')
check(all(abs(float(v) * 1e5 % 10 - 5) > 0.5 for v in (F(7, 17), F(25, 51))), 'fix 2: no rounding tie at four places')
rng = random.Random(22)
hit = tot = 0
for _ in range(600000):
    x, y = rng.uniform(0, 60), rng.uniform(0, 60)
    if abs(x - y) < 18:
        tot += 1
        hit += x < 30 and y < 30
check(abs(hit / tot - 7 / 17) < 0.004, 'fix 2: simulation %.4f' % (hit / tot))
pz = ''.join(json.dumps(load('courses/puzzles/%s.json' % n), ensure_ascii=False) for n in ('l16-meeting', 'l24-mixed-set', 'review-3', 'homework-3', 'l30-follow-ups', 'review-5', 'homework-5'))
check('18 minutes' not in pz and '0.51' not in pz and '7}{17' not in pz and '0.4118' not in pz, 'fix 2: no 18-minute wait, 0.51 or 7/17 in the puzzles geometry files')
ex_txt = json.dumps([i for i in exam['items'] if i['id'] != 'e-alerts-close'], ensure_ascii=False)
check('18 minutes' not in ex_txt and '0.4118' not in ex_txt, 'fix 2: 18 minutes is new to the exam')
# review 4: the range 11 to 40
check(largest_free(11, 40) == 20 and len({odd(n) for n in range(11, 41)}) == 20, 'fix 4: 11 to 40 still has 20 boxes, key 21')
check(40 - 11 + 1 == 30 and 30 // 2 + 1 == 16 and 30 + 1 == 31, 'fix 4: wrong values 16 and 31')

print('%d checks, %d findings' % (checks, findings))
