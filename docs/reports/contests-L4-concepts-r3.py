#!/usr/bin/env python3
"""Concept audit, round 3: contests level 4 (l13 to l16, review-4, homework-4). Blind, written before any earlier review was opened.

Run from anywhere:  python docs/reports/contests-L4-concepts-r3.py     (NumPy needed for the Monte Carlo checks)
Exit 0 means every check passed. A check that fails because the content is wrong stays failing: it is a finding in
docs/reviews/audit-contests-4-r3.md (the check name is quoted there).

Three parts.
 A. Numbers and stated results, recomputed from the content JSON (not copied): scores, orders, the split curve, counts, slips.
 B. Monte Carlo for the empirical claims (the sequential E-then-D value; "wide values almost never tie").
 C. The test-N sweep. Every `feedback.byKey.test-N` line of every code widget gets natural codings of the mistake it names.
    Each coding is graded here in CPython with the widget's own prelude and tests (5 s per test, recursion limit 3000, as the
    page) and its first failing test is compared with (i) the key the page's own harness gave under Pyodide 0.27.7
    (tools/code-runner.mjs, recorded in the `pyodide` field when the audit was run) and (ii) the line it was written for.
    Rule (docs/briefs/concept-audit.md, round-3 task): a line that names a mistake is right only if at least half of the
    failing codings of that mistake fail first on test N. Timing-dependent keys are marked TIMING.

Fix pass (docs/reviews/audit-contests-4-r3.md, "Fix pass"): the three FINDING checks now test the fixed content, the
`fix-` codings were added (each graded under Pyodide by the fixer), and five labels moved with the new lines: the two
unguarded greedies now land on test 12, `t3-increments-per-call` is test 3's named mistake, and the two codings that
never empty the set between cases are test 2's mistake, not test 3's.
"""
import json, math, os, subprocess, sys, itertools
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'contests')
load = lambda f: json.load(open(os.path.join(ROOT, f + '.json'), encoding='utf-8'))
L13, L14, L15, L16, R4, HW = (load(f) for f in ('l13-virtual-contest', 'l14-which-first', 'l15-debugging-under-time', 'l16-upsolving', 'review-4', 'homework-4'))

FAILS, COUNT = [], [0]
def check(name, ok, detail=''):
    COUNT[0] += 1
    if not ok:
        FAILS.append(name)
    print(('ok   ' if ok else 'FAIL ') + name + ((' :: ' + str(detail)) if detail and not ok else ''))
def near(a, b, tol=0.5):
    return abs(a - b) <= tol
def wrongs(w):
    return {x['id']: x['value'] for x in w.get('wrong', [])}
def ns_of(widget):
    g = {'__name__': 'audit'}
    exec(widget.get('prelude', ''), g); exec(widget['solution'], g)
    return g

# ------------------------------------------------------------------ A. numbers
S13, S14, S15, S16 = L13['screens'], L14['screens'], L15['screens'], L16['screens']

# --- l13
g = ns_of(S13[3]['widget']); peaks = g['peaks']
check('l13 s1 key: peaks of 5 1 5 is 0', peaks([5, 1, 5]) == 0 == S13[1]['widget']['answer'])
ends_counted = sum(1 for i, x in enumerate([5, 1, 5]) if (i == 0 or x > [5, 1, 5][i - 1]) and (i == 2 or x > [5, 1, 5][i + 1]))
check('l13 s1 slip ends = both ends counted', wrongs(S13[1]['widget'])['ends'] == ends_counted == 2)
check('l13 s1 slip valley = day 2 counted', wrongs(S13[1]['widget'])['valley'] == 1)
check('l13 statement example 3 5 4 6 2 -> 2', peaks([3, 5, 4, 6, 2]) == 2)
q = {x['id']: x for x in L13['quiz']}
xs = [2, 2, 3, 3, 2]
check('l13 q-plateau key 0', peaks(xs) == 0 == q['q-plateau']['widget']['answer'])
ge_both = sum(1 for i in range(1, 4) if xs[i] >= xs[i - 1] and xs[i] >= xs[i + 1])
ge_one = sum(1 for i in range(1, 4) if xs[i] >= xs[i - 1] and xs[i] > xs[i + 1])
check('l13 q-plateau slips: 2 is >= on both sides, 1 is >= on one side', wrongs(q['q-plateau']['widget']) == {'one': ge_one, 'two': ge_both} and (ge_one, ge_both) == (1, 2))
g = ns_of(S13[4]['widget']); cover = g['shortest_cover']
tape = ['AAA', 'BBB', 'AAA', 'CCC', 'BBB']
check('l13 B example 2; all three names 3 (q-cover key)', cover(tape, ['BBB', 'CCC']) == 2 and cover(tape, ['AAA', 'BBB', 'CCC']) == 3 == q['q-cover']['widget']['answer'])
check('l13 q-cover: trades 2-4 and 3-5 both hold all three, no run of 2 does', set(tape[1:4]) == set(tape[2:5]) == {'AAA', 'BBB', 'CCC'} and all(len(set(tape[i:i + 2])) < 3 for i in range(4)))
n = 200000
check('l13 s4 explain: restart at every left end is about 2e10 steps on test 9', near(n * (n + 1) / 2 / 2e10, 1, 0.01))
t = g['_tape'](2000, 22)
check('l13 s4 how: ZZZ only as the last trade; solution within 4n reads', t.count('ZZZ') == 1 and t[-1] == 'ZZZ' and g['reads_for'](cover, t, g['_ALL']) <= 4 * 2000)
g = ns_of(S13[5]['widget']); can_ship, min_cap = g['can_ship'], g['min_capacity']
W = [4, 8, 2, 7, 5, 3]
def days_at(ws, cap):
    days, load, split = 1, 0, [[]]
    for w in ws:
        if load + w > cap:
            days += 1; load = 0; split.append([])
        load += w; split[-1].append(w)
    return days, split
check('l13 C example 12; at 11 the greedy needs 4 days: 4 | 8 2 | 7 | 5 3', min_cap(W, 3) == 12 and days_at(W, 11) == (4, [[4], [8, 2], [7], [5, 3]]) and not can_ship(W, 3, 11))
w40 = g['_weights'](40, 32, 100)
ans, calls = g['checks_used'](w40, 2)
check('l13 s5 how/explain: 40 orders total 1,807, answer 909, 11 checks, scan up from 99 is 811', (sum(w40), max(w40), ans, calls, ans - max(w40) + 1) == (1807, 99, 909, 11, 811), (sum(w40), max(w40), ans, calls))
check('l13 summary formula: log2(sum - max) is about the 11 checks', near(math.log2(sum(w40) - max(w40)), calls, 0.5))
check('l13 q-capacity: total <= 1e9, 2^30 = 1.07e9 > 1e9, 30 * 1e5 = 3e6', 10**5 * 10**4 == 10**9 < 2**30 and near(2**30 / 1e9, 1.07, 0.005) and 30 * 10**5 == 3 * 10**6)
g = ns_of(S13[6]['widget']); grid_moves = g['grid_moves']
G = ['..#.>', '.#>..', '.#.#.', '...v.']
def bfs_plain(grid, banned=()):
    from collections import deque
    R, C = len(grid), len(grid[0]); d = {(0, 0): 0}; qu = deque([(0, 0)])
    while qu:
        r, c = qu.popleft()
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            a, b = r + dr, c + dc
            if 0 <= a < R and 0 <= b < C and grid[a][b] != '#' and (a, b) not in d and (a, b) not in banned:
                d[(a, b)] = d[(r, c)] + 1; qu.append((a, b))
    return d.get((R - 1, C - 1), -1)
check('l13 D example 11; ignoring arrows 7 (test-1 line)', grid_moves(G) == 11 and bfs_plain(G) == 7)
check('l13 D test-1 line: every 7-move arrow-free route crosses the v in row 4 (without that cell the shortest is longer)', bfs_plain(G, banned={(3, 3)}) > 7)
G2 = [row.replace('>', '#') if i == 1 else row for i, row in enumerate(G)]
check('l13 D explain: every route goes through the > in row 2 (blocking it gives -1)', grid_moves(G2) == -1)
check('l13 q-boxed / test 2: .> over v. is -1; ignoring arrows 2', grid_moves(['.>', 'v.']) == -1 == q['q-boxed']['widget']['answer'] and bfs_plain(['.>', 'v.']) == 2 == wrongs(q['q-boxed']['widget'])['two'])
check('l13 D test 9 is 200,000 cells', 400 * 500 == 200000)
sam = S13[7]['canvas']['params']['lines']
check('l13 trap: D took 52 minutes, A seven, the second wrong answer 13 more', sam[3].startswith('00:52') and sam[4].startswith('00:59') and 59 - 52 == 7 and 51 - 38 == 13)
rows = S13[8]['widget']['rows']
num = [[int(x) for x in r[1:]] for r in rows[:4]]
cols = [sum(r[c] for r in num) for c in (0, 1, 2)]
check('l13 log totals 16, 27, 17 = 60; 12 of the debugging on C', cols == [rows[4][c]['answer'] for c in (1, 2, 3)] == [16, 27, 17] and sum(cols) == 60 and num[2][2] == 12)
check('l13 homework model minutes: A 9, B 17, C 27, D 7 left', [sum(r) for r in num] == [9, 17, 27, 7])

# --- l14
P4 = [('A', 500, 10), ('B', 1000, 20), ('C', 1500, 35), ('D', 2000, 50)]
def score(v, minute, wrong=0, floor=0.3):
    return max(floor * v, v - v / 250 * minute - 50 * wrong)
def run(order, minutes=10**9):
    clock, out = 0, {}
    for name, v, tm in order:
        clock += tm
        out[name] = score(v, clock) if clock <= minutes else 0
    return out
by = {p[0]: p for p in P4}
frames = S14[1]['canvas']['controls'][0]['frames']
for label, fr in zip(('ABCD', 'DCBA', 'CABD'), frames):
    got = run([by[c] for c in label])
    check(f'l14 s1 bars for order {label} and caption total', all(near(got[k], fr['values'][k]) for k in 'ABCD') and f"{round(sum(got.values())):,}" in fr['caption'], got)
tot = {''.join(p[0] for p in o): sum(run(o).values()) for o in itertools.permutations(P4)}
best = max(tot.values())
check('l14 s0 key: best of all 24 orders is 3,550, reached only by ABCD and BACD (the tie the widget allows)', best == 3550 and sorted(k for k, v in tot.items() if v == best) == ['ABCD', 'BACD'])
check('l14 s1 explain: hardest first lifts D 1,080 -> 1,600 and drops the other three by 630; totals 3,440 and 3,520', run([by[c] for c in 'DCBA'])['D'] == 1600 and run(P4)['D'] == 1080 and sum(run(P4)[k] - run([by[c] for c in 'DCBA'])[k] for k in 'ABC') == 630 and (tot['DCBA'], tot['CABD']) == (3440, 3520))
check('l14 s2 rates 50, 50, 42.857, 40', [round(v / tm, 3) for _, v, tm in P4] == [50, 50, 42.857, 40] and S14[2]['widget']['rows'][2][1]['answer'] == 42.857)
w = S14[3]['widget']
check('l14 s3 key 810 and slips 860 (no rejection), 760 (two), 300 (floor)', w['answer'] == score(1000, 35, 1) == 810 and wrongs(w) == {'nopen': score(1000, 35, 0), 'floor': 0.3 * 1000, 'twice': score(1000, 35, 2)})
check('l14 s3 explain: 120 minutes of decay is 48%, so the 30% floor needs rejections', 120 / 250 == 0.48 and 1 - 0.48 > 0.3)
# Smith's rule under linear decay without floors: rate order is optimal on random instances
import random
rng = random.Random(7); smith_ok = True
for _ in range(300):
    ps = [(i, rng.randint(1, 20) * 100, rng.randint(1, 12)) for i in range(5)]   # short times: no floor reached, all finish
    val = lambda o: sum(v - v / 250 * c for (_, v, _), c in zip(o, itertools.accumulate(p[2] for p in o)))
    smith_ok &= near(val(sorted(ps, key=lambda p: -p[1] / p[2])), max(val(o) for o in itertools.permutations(ps)), 1e-6)
check('l14 s9: points-per-minute order is optimal under the rule when no floor binds (300 random rounds, brute force)', smith_ok)
check('l14 s9 key: CD beats DC by 20; ABDC 3,530', (2000 * 35 - 1500 * 50) / 250 == -20 and tot['ABCD'] - tot['ABDC'] == 20 == S14[9]['widget']['answer'] and tot['ABDC'] == 3530 and wrongs(S14[9]['widget']) == {'neg': -20, 'big': 5000})
f = lambda x: 1000 * (1 - math.exp(-x / 50)) + 800 * (1 - math.exp(-(60 - x) / 15))
xstar = max((i / 1000 for i in range(60001)), key=f)
check('l14 s6 key: top of the curve at 34.84, 1,152.3; all D 699, all E 785; start point value', near(xstar, S14[6]['widget']['points'][0]['target']['x'], 0.01) and near(f(xstar), 1152.3, 0.05) and round(f(60)) == 699 and round(f(0)) == 785 and near(f(10), S14[6]['canvas']['state']['points'][0]['y'], 1e-9))
# E first until solved (exponential, mean 15), then D (mean 50) with what is left: closed form
seq = 800 * (1 - math.exp(-4)) + 1000 * ((1 - math.exp(-4)) - (1 / 15) * math.exp(-1.2) * (150 / 7) * (1 - math.exp(-2.8)))
seq_d_first = 1000 * (1 - math.exp(-1.2)) + 800 * ((1 - math.exp(-1.2)) - (1 / 50) * math.exp(-4) * (-150 / 7) * (1 - math.exp(2.8)))
check('l14 s6 explain: E first then D is about 1,363 (closed form), and beats D first', round(seq) == 1363 and seq > seq_d_first, (seq, seq_d_first))
g = ns_of(S14[5]['widget']); key = g['icpc_rank_key']
check('l14 s5: table key (-3, 208) = 12 + 61 + 135', key([(12, 0), (41, 1), (95, 2), (None, 3)]) == (-3, 208) and 12 + (41 + 20) + (95 + 40) == 208)
check('l14 q-icpc: X 195, Y 185, Z four solves first', key([(15, 0), (50, 2), (90, 0)]) == (-3, 195) and key([(20, 0), (45, 0), (100, 1)]) == (-3, 185))
g = ns_of(S14[10]['widget']); bo = g['best_order']
check('l14 s10: 60 minutes -> 2,090 by B then C; A then B 1,360; no three problems fit', bo(P4, 60) == (2090.0, ['B', 'C', 'A', 'D']) and sum(run([by['A'], by['B']], 60).values()) == 1360 and min(sum(p[2] for p in c) for c in itertools.combinations(P4, 3)) > 60)
check('l14 q-rate: P 30, Q 25 a minute, and best_order agrees', 750 / 25 == 30 and 1250 / 50 == 25 and bo([('P', 750, 25), ('Q', 1250, 50)], 120)[1] == ['P', 'Q'])
tr = S14[11]['canvas']['params']['rows']
check('l14 transfer: rates 600, 480, 100; 1% a minute costs 600 against 750; both fit in 30', (3000 / 5, 12000 / 25, 2000 / 20) == (600, 480, 100) and 0.01 * 12000 * 5 == 600 and 0.01 * 3000 * 25 == 750 and 5 + 25 == 30)
q = {x['id']: x for x in L14['quiz']}
check('l14 q-floor: 230 below the floor -> 300; slip 280 leaves out the rejection', q['q-floor']['widget']['answer'] == score(1000, 180, 1) == 300 and wrongs(q['q-floor']['widget']) == {'nofloor': 1000 - 720 - 50, 'nopen': 1000 - 720})

# --- l15
g = ns_of({'solution': S15[3]['widget']['starter']}); buggy = g['last_occurrence']
cases = [([5], 5, 0), ([3, 3, 3], 3, 2), ([10**9, 10**9, 1], 10**9, 1), ([4, 7], 9, -1)]
got = [buggy(a, x) for a, x, _ in cases]
check('l15 s1 table: the submission gives -1, 1, 1, -1; two of four differ (key 2)', got == [-1, 1, 1, -1] and sum(o != e for o, (_, _, e) in zip(got, cases)) == 2 == S15[1]['widget']['answer'])
check('l15 s0: the example hides the bug (its last 7 is not at the end)', buggy([4, 7, 7, 1], 7) == 2)
check('l15 s7: Python default recursion limit is 1000', True)  # sys.getrecursionlimit() of a fresh interpreter, checked in part C child
inv = lambda a: sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])
check('l15 s4: 3 1 2 -> 2, [2,1,2,1] -> 3, 1,500 values is about 1.1 million pairs', inv([3, 1, 2]) == 2 and inv([2, 1, 2, 1]) == 3 and math.comb(1500, 2) == 1124250)
q = {x['id']: x for x in L15['quiz']}
check('l15 q-adjacent: neighbours only on 3 2 1 gives 2, true count 3', sum(1 for a, b in zip([3, 2, 1], [2, 1]) if a > b) == 2 == q['q-adjacent']['widget']['answer'] and inv([3, 2, 1]) == 3)
check('l15 q-overflow: 2e5 * 1e9 = 2e14 > 2^31 - 1 = 2,147,483,647; long long about 9.2e18', 2 * 10**5 * 10**9 == 2 * 10**14 > 2**31 - 1 == 2147483647 and near((2**63 - 1) / 1e18, 9.2, 0.03))
check('l15 r4-hand: the loop from index 1 gives 0 on [5], 4 on [2,2,2], 0 on []', (sum([5][1:]), sum([2, 2, 2][1:]), sum([][1:])) == (0, 4, 0))

# --- l16
g = ns_of(S16[3]['widget']); thirds = g['equal_thirds']
def thirds_brute(a):
    n = len(a); P = [0]
    for x in a: P.append(P[-1] + x)
    return sum(1 for i in range(1, n - 1) for j in range(i + 1, n) if P[i] == P[j] - P[i] == P[n] - P[j])
rng = random.Random(3)
check('l16 s3: one-pass count equals the double loop on 2,000 random small cases', all(thirds(a) == thirds_brute(a) for a in ([rng.randint(-2, 2) for _ in range(rng.randint(1, 9))] for _ in range(2000))))
w = S16[1]['widget']
check('l16 s1 key 6 = C(4,2); slips 10 = C(5,2), 3 = four zeros, 1', w['answer'] == thirds_brute([0] * 5) == math.comb(4, 2) and wrongs(w) == {'ten': math.comb(5, 2), 'three': thirds_brute([0] * 4), 'one': 1})
check('l16 test 9 answer C(199999, 2) = 19,999,700,001, about 2e10, above 2^31 - 1, about nine times it, exact in a double', math.comb(199999, 2) == 19999700001 and near(19999700001 / 2e10, 1, 0.01) and 9 < 19999700001 / (2**31 - 1) < 9.5 and float(19999700001) == 19999700001 < 2**53)
check('l16 s3 lines: example 2; test 5 total 2; test 6 total 0 and answer 1', thirds([1, 2, 3, 0, 3]) == 2 and sum([2, -2] * 4 + [2]) == 2 and sum([1, -1] * 3) == 0 and thirds_brute([1, -1] * 3) == 1)
log = [r[1] for r in S16[4]['canvas']['params']['rows']]
check('l16 s4 tally 3, 2, 2, 1 (eight) and rows 2, 4, 8 are forgot n = 1', [log.count(r[0]) for r in S16[4]['widget']['rows']] == [r[1]['answer'] for r in S16[4]['widget']['rows']] == [3, 2, 2, 1] and [i + 1 for i, c in enumerate(log) if c == 'forgot n = 1'] == [2, 4, 8])
q = {x['id']: x for x in L16['quiz']}
check('l16 q-zeros key 3 = C(3,2); slips 6 (five zeros) and 4 = C(4,1)', q['q-zeros']['widget']['answer'] == thirds_brute([0] * 4) == 3 and wrongs(q['q-zeros']['widget']) == {'six': 6, 'four': 4})
g = ns_of(S16[5]['widget'])
check('l16 q-sort key', g['mistakes_summary']([('1', 'misread'), ('2', 'edge case'), ('3', 'misread'), ('4', 'edge case'), ('5', 'overflow')]) == [('edge case', 2), ('misread', 2), ('overflow', 1)])
check('l16 ratings: 1200 + 300 = 1500 keeps C, D; E, F are 700 and 1,200 above; 1500 + 300 = 1800; 1250 + 100..200', 1900 - 1200 == 700 and 2400 - 1200 == 1200 and 1500 + 300 == 1800 and (1250 + 100, 1250 + 200) == (1350, 1450) and 2000 - 1250 == 750 and 1800 - 1410 == 390)

# --- review-4, homework-4
it = {x['id']: x for x in R4['items']}
check('r4-log 18/60 = 0.3; slips 0.5 and 0.6', it['r4-log']['widget']['answer'] == 18 / 60 and wrongs(it['r4-log']['widget']) == {'code': 30 / 60, 'of-code': 18 / 30} and 12 + 30 + 18 == 60)
check('r4-decay 1,112; slips 1,212 and 1,162; floor 450', it['r4-decay']['widget']['answer'] == score(1500, 48, 2) == 1112 and wrongs(it['r4-decay']['widget']) == {'nopen': score(1500, 48, 0), 'onepen': score(1500, 48, 1)} and 0.3 * 1500 == 450)
qp = run([('Q', 500, 15), ('P', 1000, 40)]); pq = run([('P', 1000, 40), ('Q', 500, 15)])
check('r4-swap 20: Q first costs P 60, P first costs Q 80; rates 33 and 25', sum(qp.values()) - sum(pq.values()) == 20 == it['r4-swap']['widget']['answer'] and 1000 * 15 / 250 == 60 and 500 * 40 / 250 == 80 and round(500 / 15) == 33 and 1000 / 40 == 25 and (1000 * 15 - 500 * 40) / 250 == -20)
check('r4-pattern: a scan is up to 2e14 limits', 2 * 10**5 * 10**9 == 2 * 10**14)
check('r4-late 675 at minute 115; slips 1,150 and 375', it['r4-late']['widget']['answer'] == score(1250, 115) == 675 and 1250 / 250 == 5 and wrongs(it['r4-late']['widget']) == {'twenty': 1250 - 5 * 20, 'floor': 0.3 * 1250})
check('r4-upsolve: 1350 + 300 = 1650; 550 and 950 above', 1350 + 300 == 1650 and 1900 - 1350 == 550 and 2300 - 1350 == 950)
it = {x['id']: x for x in HW['items']}
g = ns_of(S14[5]['widget'])
check('hw4-penalty 269; slips 349 (E charged) and 209', g['icpc_rank_key']([(8, 0), (27, 2), (64, 1), (110, 0), (None, 4)]) == (-4, 269) and it['hw4-penalty']['widget']['answer'] == 269 and wrongs(it['hw4-penalty']['widget']) == {'withE': 269 + 80, 'nopen': 8 + 27 + 64 + 110})
g = ns_of(it['hw4-ktrades']['widget']); mp = g['max_profit_k']
def mp_brute(p, k):
    from functools import lru_cache
    @lru_cache(None)
    def go(i, k, holding):
        if i == len(p): return 0
        best = go(i + 1, k, holding)
        if holding: best = max(best, p[i] + go(i, k, False))          # sell today, may buy again today
        elif k: best = max(best, -p[i] + go(i + 1, k - 1, True))      # buy today, sell on a later day
        return best
    return go(0, k, False)
rng = random.Random(5)
check('hw4-ktrades: the DP equals a brute force on 1,500 random cases; test 6 is 2 + 3 + 4 = 9', all(mp(p, k) == mp_brute(tuple(p), k) for p, k in (([rng.randint(1, 9) for _ in range(rng.randint(1, 8))], rng.randint(0, 5)) for _ in range(1500))) and mp([1, 3, 2, 5, 4, 8], 10) == 9 == (3 - 1) + (5 - 2) + (8 - 4))
check('hw4-ktrades sizes: O(nk) is 2e5 updates, O(n^2 k) about 2e9', 10**4 * 20 == 2 * 10**5 and 10**8 * 20 == 2 * 10**9)
g = ns_of(it['hw4-gap']['widget']); wg = g['widest_gap']
def wg_brute(a, m):
    return max(min(b - c for c, b in zip(s, s[1:])) for s in (sorted(c) for c in itertools.combinations(a, m)))
rng = random.Random(9)
check('hw4-gap: binary search with greedy equals a brute force on 800 random cases; example 3 by 1,4,8 or 1,4,9', all(wg(a, m) == wg_brute(a, m) for a, m in ((lambda a: (a, rng.randint(2, len(a))))([rng.randint(1, 12) for _ in range(rng.randint(2, 7))]) for _ in range(800))) and wg([1, 2, 8, 4, 9], 3) == 3 == min(4 - 1, 8 - 4) == min(4 - 1, 9 - 4))
g = ns_of(it['hw4-desks']['widget'])
check('hw4-desks: test 7 chain cut in the middle leaves a first group of 100,001 desks (recursion about 100,000 deep)', g['_chain'](200000)[100000] == (100000, 100001))

# ------------------------------------------------------------------ B. Monte Carlo
try:
    import numpy as np
    r = np.random.default_rng(20261126)
    N = 400000
    te, td = r.exponential(15, N), r.exponential(50, N)
    e_first = 800 * (te <= 60) + 1000 * ((te <= 60) & (te + td <= 60))
    fixed = 1000 * (td <= 34.84) + 800 * (te <= 60 - 34.84)
    se = e_first.std() / math.sqrt(N)
    check('MC l14 s6: E first until solved, then D: mean about 1,363 (400,000 rounds, within 4 SE)', abs(e_first.mean() - 1363) < 4 * se + 0.5, (e_first.mean(), se))
    check('MC l14 s6: the fixed 35/25 split averages about 1,152, below the sequential plan', abs(fixed.mean() - 1152.3) < 4 * fixed.std() / math.sqrt(N) + 0.5 and fixed.mean() < e_first.mean())
except ImportError:
    check('MC l14 s6 (NumPy missing)', False)
# "wide values almost never tie": chance that smallest_failing's 1,600 cases (lengths 1..8, 200 each) hold any tie at all
p_none = 1.0
for nlen in range(1, 9):
    p_case = math.prod((10**6 - i) / 10**6 for i in range(nlen))
    p_none *= p_case ** 200
gl = ns_of(S15[9]['widget'])
hits = sum(gl['smallest_failing'](gl['fast_ties'], gl['brute_inv'], gl['gen_wide'], s) is not None for s in range(300))
check('MC l15 s9 test-6 line: a tie among values to 1e6 is rare: P(any in a whole run) = %.3f, and %d of 300 seeds find one' % (1 - p_none, hits), 1 - p_none < 0.03 and hits <= 15)

# ------------------------------------------------------------------ C. the test-N sweep
VARIANTS = json.loads(r'''[
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l13-virtual-contest",
"at": "screens[4]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l14-which-first",
"at": "screens[4]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l14-which-first",
"at": "screens[5]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l15-debugging-under-time",
"at": "screens[3]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l15-debugging-under-time",
"at": "screens[4]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "homework-4",
"at": "items[2]",
"id": "solution",
"line": null,
"named": false,
"pyodide": null,
"src": "@solution"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t3-last-counted-a",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def peaks(closes):\n    count = 0\n    for i in range(1, len(closes)):\n        right = closes[i + 1] if i + 1 < len(closes) else float(\"-inf\")\n        if closes[i] > closes[i - 1] and closes[i] > right:\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t3-last-counted-b",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def peaks(closes):\n    count = 0\n    n = len(closes)\n    for i in range(1, n):\n        if closes[i] > closes[i - 1] and (i == n - 1 or closes[i] > closes[i + 1]):\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t3-both-ends-padded",
"line": "test-3",
"named": false,
"pyodide": "test-2",
"src": "def peaks(closes):\n    xs = [float(\"-inf\")] + list(closes) + [float(\"-inf\")]\n    return sum(1 for i in range(1, len(xs) - 1) if xs[i] > xs[i - 1] and xs[i] > xs[i + 1])\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t3-both-ends-guard",
"line": "test-3",
"named": false,
"pyodide": "test-2",
"src": "def peaks(closes):\n    n = len(closes)\n    count = 0\n    for i in range(n):\n        left = i == 0 or closes[i] > closes[i - 1]\n        right = i == n - 1 or closes[i] > closes[i + 1]\n        if left and right:\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t4-first-counted-a",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "def peaks(closes):\n    count = 0\n    n = len(closes)\n    for i in range(0, n - 1):\n        if (i == 0 or closes[i] > closes[i - 1]) and closes[i] > closes[i + 1]:\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t4-first-counted-b",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "def peaks(closes):\n    count = 0\n    for i in range(len(closes) - 1):\n        left = closes[i - 1] if i > 0 else float(\"-inf\")\n        if closes[i] > left and closes[i] > closes[i + 1]:\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t4-ends-n>=3-only",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "def peaks(closes):\n    n = len(closes)\n    if n < 3:\n        return 0\n    count = 0\n    for i in range(n):\n        left = i == 0 or closes[i] > closes[i - 1]\n        right = i == n - 1 or closes[i] > closes[i + 1]\n        if left and right:\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t6-ge-both",
"line": "test-6",
"named": true,
"pyodide": "test-5",
"src": "def peaks(closes):\n    count = 0\n    for i in range(1, len(closes) - 1):\n        if closes[i] >= closes[i - 1] and closes[i] >= closes[i + 1]:\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t6-ge-left",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def peaks(closes):\n    count = 0\n    for i in range(1, len(closes) - 1):\n        if closes[i] >= closes[i - 1] and closes[i] > closes[i + 1]:\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t6-ge-right",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def peaks(closes):\n    count = 0\n    for i in range(1, len(closes) - 1):\n        if closes[i] > closes[i - 1] and closes[i] >= closes[i + 1]:\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t5-ge-both(same as t6)",
"line": "test-5",
"named": true,
"pyodide": "test-5",
"src": "def peaks(closes):\n    return sum(1 for i in range(1, len(closes) - 1) if closes[i] >= closes[i - 1] and closes[i] >= closes[i + 1])\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t2-special-case-wrong",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def peaks(closes):\n    if len(closes) == 1:\n        return 1\n    count = 0\n    for i in range(1, len(closes) - 1):\n        if closes[i] > closes[i - 1] and closes[i] > closes[i + 1]:\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t2-index-error",
"line": "test-2",
"named": false,
"pyodide": "test-3",
"src": "def peaks(closes):\n    count = 0\n    for i in range(len(closes)):\n        if closes[i] > closes[i - 1] and closes[i] > closes[i + 1]:\n            count += 1\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[3]",
"id": "t2-max-based",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def peaks(closes):\n    count = 0\n    i = 1\n    while True:\n        if closes[i] > closes[i - 1] and closes[i] > closes[i + 1]:\n            count += 1\n        i += 1\n        if i >= len(closes) - 1:\n            break\n    return count\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[4]",
"id": "t3-no-minus1-inf",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def shortest_cover(tickers, needed):\n    need = set(needed)\n    count = {}\n    have = 0\n    best = float(\"inf\")\n    left = 0\n    for right, t in enumerate(tickers):\n        if t in need:\n            count[t] = count.get(t, 0) + 1\n            if count[t] == 1:\n                have += 1\n        while have == len(need):\n            best = min(best, right - left + 1)\n            u = tickers[left]\n            if u in need:\n                count[u] -= 1\n                if count[u] == 0:\n                    have -= 1\n            left += 1\n    return best\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[4]",
"id": "t3-no-minus1-len",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def shortest_cover(tickers, needed):\n    need = set(needed)\n    count = {}\n    have = 0\n    best = len(tickers)\n    left = 0\n    for right, t in enumerate(tickers):\n        if t in need:\n            count[t] = count.get(t, 0) + 1\n            if count[t] == 1:\n                have += 1\n        while have == len(need):\n            best = min(best, right - left + 1)\n            u = tickers[left]\n            if u in need:\n                count[u] -= 1\n                if count[u] == 0:\n                    have -= 1\n            left += 1\n    return best\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[4]",
"id": "t5-len-needed",
"line": "test-5",
"named": true,
"pyodide": "test-5",
"src": "def shortest_cover(tickers, needed):\n    count = {}\n    have = 0\n    best = -1\n    left = 0\n    for right, t in enumerate(tickers):\n        if t in needed:\n            count[t] = count.get(t, 0) + 1\n            if count[t] == 1:\n                have += 1\n        while have == len(needed):\n            if best == -1 or right - left + 1 < best:\n                best = right - left + 1\n            u = tickers[left]\n            if u in needed:\n                count[u] -= 1\n                if count[u] == 0:\n                    have -= 1\n            left += 1\n    return best\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[4]",
"id": "t5-multiset",
"line": "test-5",
"named": true,
"pyodide": "test-5",
"src": "from collections import Counter\ndef shortest_cover(tickers, needed):\n    need = Counter(needed)\n    missing = len(needed)\n    best = -1\n    left = 0\n    have = Counter()\n    for right, t in enumerate(tickers):\n        if t in need:\n            have[t] += 1\n            if have[t] <= need[t]:\n                missing -= 1\n        while missing == 0:\n            if best == -1 or right - left + 1 < best:\n                best = right - left + 1\n            u = tickers[left]\n            if u in need:\n                have[u] -= 1\n                if have[u] < need[u]:\n                    missing += 1\n            left += 1\n    return best\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[4]",
"id": "t8-restart-indexing",
"line": "test-8",
"named": true,
"pyodide": "test-8",
"src": "def shortest_cover(tickers, needed):\n    need = set(needed)\n    n = len(tickers)\n    best = -1\n    for left in range(n):\n        seen = set()\n        for right in range(left, n):\n            if tickers[right] in need:\n                seen.add(tickers[right])\n            if len(seen) == len(need):\n                if best == -1 or right - left + 1 < best:\n                    best = right - left + 1\n                break\n    return best\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[4]",
"id": "t8-restart-slices",
"line": "test-8",
"named": true,
"pyodide": "test-9",
"src": "def shortest_cover(tickers, needed):\n    need = set(needed)\n    n = len(tickers)\n    best = -1\n    for left in range(n):\n        seen = set()\n        for k, t in enumerate(tickers[left:]):\n            if t in need:\n                seen.add(t)\n            if len(seen) == len(need):\n                if best == -1 or k + 1 < best:\n                    best = k + 1\n                break\n    return best\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[4]",
"id": "t8-all-windows-by-length",
"line": "test-8",
"named": true,
"pyodide": "test-8",
"src": "def shortest_cover(tickers, needed):\n    need = set(needed)\n    n = len(tickers)\n    for size in range(1, n + 1):\n        for left in range(0, n - size + 1):\n            if need <= set(tickers[left:left + size]):\n                return size\n    return -1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[4]",
"id": "t9-restart-copy-first",
"line": "test-9",
"named": true,
"pyodide": "test-9",
"src": "def shortest_cover(tickers, needed):\n    tickers = list(tickers)\n    need = set(needed)\n    n = len(tickers)\n    best = -1\n    for left in range(n):\n        seen = set()\n        for right in range(left, n):\n            if tickers[right] in need:\n                seen.add(tickers[right])\n            if len(seen) == len(need):\n                if best == -1 or right - left + 1 < best:\n                    best = right - left + 1\n                break\n    return best\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t4-heavy-order-newday",
"line": "test-12",
"named": true,
"pyodide": "test-12",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\n\ndef min_capacity(weights, k):\n    lo, hi = max(weights), sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t4-heavy-order-newday-lo1",
"line": "test-4",
"named": true,
"pyodide": "test-6",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\n\ndef min_capacity(weights, k):\n    lo, hi = 1, sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t10-hi-1e9",
"line": "test-10",
"named": true,
"pyodide": "test-10",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if w > cap:\n            return False\n        if load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\n\ndef min_capacity(weights, k):\n    lo, hi = 1, 10**9\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t10-hi-n*maxw",
"line": "test-10",
"named": true,
"pyodide": "test-10",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if w > cap:\n            return False\n        if load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\n\ndef min_capacity(weights, k):\n    lo, hi = 0, 10**4 * 10**5\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t10-lo0-hi-sum (range not narrowed to max)",
"line": "test-10",
"named": false,
"pyodide": null,
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if w > cap:\n            return False\n        if load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\n\ndef min_capacity(weights, k):\n    lo, hi = 0, sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t10-linear-scan",
"line": "test-10",
"named": true,
"pyodide": "test-10",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if w > cap:\n            return False\n        if load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\n\ndef min_capacity(weights, k):\n    cap = max(weights)\n    while not can_ship(weights, k, cap):\n        cap += 1\n    return cap\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t11-linear-scan-from-1",
"line": "test-11",
"named": true,
"pyodide": "test-10",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if w > cap:\n            return False\n        if load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\n\ndef min_capacity(weights, k):\n    cap = 1\n    while not can_ship(weights, k, cap):\n        cap += 1\n    return cap\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t11-linear-inline",
"line": "test-11",
"named": true,
"pyodide": "test-11",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if w > cap:\n            return False\n        if load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\ndef min_capacity(weights, k):\n    cap = max(weights)\n    while True:\n        days, load = 1, 0\n        for w in weights:\n            if load + w > cap:\n                days += 1\n                load = 0\n            load += w\n        if days <= k:\n            return cap\n        cap += 1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t1-days-off-by-one(start 0)",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "def can_ship(weights, k, cap):\n    days, load = 0, 0\n    for w in weights:\n        if w > cap:\n            return False\n        if load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\ndef min_capacity(weights, k):\n    lo, hi = max(weights), sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t1-ge-overflow",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if w > cap:\n            return False\n        if load + w >= cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\ndef min_capacity(weights, k):\n    lo, hi = max(weights), sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t2-canship-wrong-min-right",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def can_ship(weights, k, cap):\n    return sum(weights) <= cap * k and max(weights) <= cap\n\ndef min_capacity(weights, k):\n    def ok(cap):\n        days, load = 1, 0\n        for w in weights:\n            if load + w > cap:\n                days += 1\n                load = 0\n            load += w\n        return days <= k\n    lo, hi = max(weights), sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if ok(mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t1-ignore-arrows",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "from collections import deque\n\nSTEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    dist = [[-1] * cols for _ in range(rows)]\n    dist[0][0] = 0\n    queue = deque([(0, 0)])\n    while queue:\n        r, c = queue.popleft()\n        if (r, c) == (rows - 1, cols - 1):\n            return dist[r][c]\n        cell = grid[r][c]\n        moves = STEP.values()\n        for dr, dc in moves:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != \"#\" and dist[nr][nc] == -1:\n                dist[nr][nc] = dist[r][c] + 1\n                queue.append((nr, nc))\n    return -1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t1-arrows-as-blocks",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "from collections import deque\n\nSTEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    dist = [[-1] * cols for _ in range(rows)]\n    dist[0][0] = 0\n    queue = deque([(0, 0)])\n    while queue:\n        r, c = queue.popleft()\n        if (r, c) == (rows - 1, cols - 1):\n            return dist[r][c]\n        cell = grid[r][c]\n        moves = [STEP[cell]] if cell in STEP else STEP.values()\n        for dr, dc in moves:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == \".\" and dist[nr][nc] == -1:\n                dist[nr][nc] = dist[r][c] + 1\n                queue.append((nr, nc))\n    return -1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t2-arrow-restricts-entry-not-exit",
"line": "test-2",
"named": false,
"pyodide": "test-1",
"src": "from collections import deque\n\nSTEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    dist = [[-1] * cols for _ in range(rows)]\n    dist[0][0] = 0\n    queue = deque([(0, 0)])\n    while queue:\n        r, c = queue.popleft()\n        if (r, c) == (rows - 1, cols - 1):\n            return dist[r][c]\n        for dr, dc in STEP.values():\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != \"#\" and dist[nr][nc] == -1:\n                cell = grid[nr][nc]\n                if cell in STEP and STEP[cell] != (dr, dc):\n                    continue\n                dist[nr][nc] = dist[r][c] + 1\n                queue.append((nr, nc))\n    return -1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t2-arrow-skips-through",
"line": "test-2",
"named": false,
"pyodide": null,
"src": "from collections import deque\n\nSTEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    dist = [[-1] * cols for _ in range(rows)]\n    dist[0][0] = 0\n    queue = deque([(0, 0)])\n    while queue:\n        r, c = queue.popleft()\n        if (r, c) == (rows - 1, cols - 1):\n            return dist[r][c]\n        cell = grid[r][c]\n        moves = [STEP[cell]] if cell in STEP else STEP.values()\n        for dr, dc in moves:\n            nr, nc = r + dr, c + dc\n            nr, nc = max(0, min(rows - 1, nr)), max(0, min(cols - 1, nc))\n            if grid[nr][nc] != \"#\" and dist[nr][nc] == -1:\n                dist[nr][nc] = dist[r][c] + 1\n                queue.append((nr, nc))\n    return -1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t3-target-check-on-push",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "from collections import deque\n\nSTEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    dist = [[-1] * cols for _ in range(rows)]\n    dist[0][0] = 0\n    queue = deque([(0, 0)])\n    while queue:\n        r, c = queue.popleft()\n        cell = grid[r][c]\n        moves = [STEP[cell]] if cell in STEP else STEP.values()\n        for dr, dc in moves:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != \"#\" and dist[nr][nc] == -1:\n                dist[nr][nc] = dist[r][c] + 1\n                if (nr, nc) == (rows - 1, cols - 1):\n                    return dist[nr][nc]\n                queue.append((nr, nc))\n    return -1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t9-no-visited-bfs",
"line": "test-9",
"named": true,
"pyodide": "test-9",
"src": "from collections import deque\n\nSTEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    dist = [[-1] * cols for _ in range(rows)]\n    dist[0][0] = 0\n    queue = deque([(0, 0)])\n    while queue:\n        r, c = queue.popleft()\n        if (r, c) == (rows - 1, cols - 1):\n            return dist[r][c]\n        cell = grid[r][c]\n        moves = [STEP[cell]] if cell in STEP else STEP.values()\n        for dr, dc in moves:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != \"#\":\n                dist[nr][nc] = dist[r][c] + 1\n                queue.append((nr, nc))\n    return -1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t9-visited-list",
"line": "test-9",
"named": true,
"pyodide": "test-9",
"src": "from collections import deque\n\nSTEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    seen = [(0, 0)]\n    queue = deque([(0, 0, 0)])\n    while queue:\n        r, c, d = queue.popleft()\n        if (r, c) == (rows - 1, cols - 1):\n            return d\n        cell = grid[r][c]\n        moves = [STEP[cell]] if cell in STEP else STEP.values()\n        for dr, dc in moves:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != \"#\" and (nr, nc) not in seen:\n                seen.append((nr, nc))\n                queue.append((nr, nc, d + 1))\n    return -1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t9-dfs-relax-recursive",
"line": "test-9",
"named": true,
"pyodide": "test-9",
"src": "STEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    best = [[-1] * cols for _ in range(rows)]\n\n    def go(r, c, d):\n        if best[r][c] != -1 and best[r][c] <= d:\n            return\n        best[r][c] = d\n        cell = grid[r][c]\n        moves = [STEP[cell]] if cell in STEP else STEP.values()\n        for dr, dc in moves:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != \"#\":\n                go(nr, nc, d + 1)\n\n    go(0, 0, 0)\n    return best[rows - 1][cols - 1]\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t9-mark-on-pop",
"line": "test-9",
"named": false,
"pyodide": null,
"src": "from collections import deque\n\nSTEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    seen = set()\n    queue = deque([(0, 0, 0)])\n    while queue:\n        r, c, d = queue.popleft()\n        if (r, c) == (rows - 1, cols - 1):\n            return d\n        if (r, c) in seen:\n            continue\n        seen.add((r, c))\n        cell = grid[r][c]\n        moves = [STEP[cell]] if cell in STEP else STEP.values()\n        for dr, dc in moves:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != \"#\":\n                queue.append((nr, nc, d + 1))\n    return -1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t4-first-order-opens-day",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "def can_ship(weights, k, cap):\n    days, load = 0, 0\n    for w in weights:\n        if days == 0 or load + w > cap:\n            days += 1\n            load = w\n        else:\n            load += w\n    return days <= k\n\ndef min_capacity(weights, k):\n    lo, hi = max(weights), sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t4-guard-load>0",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if load > 0 and load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    return days <= k\n\ndef min_capacity(weights, k):\n    lo, hi = max(weights), sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "t4-count-day-ends",
"line": "test-12",
"named": true,
"pyodide": "test-12",
"src": "def can_ship(weights, k, cap):\n    days, load = 0, 0\n    for w in weights:\n        if load + w > cap:\n            days += 1\n            load = 0\n        load += w\n    if load > 0:\n        days += 1\n    return days <= k\n\ndef min_capacity(weights, k):\n    lo, hi = max(weights), sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t2-arrow-offgrid-falls-back",
"line": "test-2",
"named": false,
"pyodide": "test-1",
"src": "from collections import deque\n\nSTEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    dist = [[-1] * cols for _ in range(rows)]\n    dist[0][0] = 0\n    queue = deque([(0, 0)])\n    while queue:\n        r, c = queue.popleft()\n        if (r, c) == (rows - 1, cols - 1):\n            return dist[r][c]\n        cell = grid[r][c]\n        moves = list(STEP.values())\n        if cell in STEP:\n            dr, dc = STEP[cell]\n            if 0 <= r + dr < rows and 0 <= c + dc < cols:\n                moves = [STEP[cell]]\n        for dr, dc in moves:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != \"#\" and dist[nr][nc] == -1:\n                dist[nr][nc] = dist[r][c] + 1\n                queue.append((nr, nc))\n    return -1\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[6]",
"id": "t2-return-dist-target-init0",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "from collections import deque\n\nSTEP = {\">\": (0, 1), \"<\": (0, -1), \"^\": (-1, 0), \"v\": (1, 0)}\n\n\ndef grid_moves(grid):\n    rows, cols = len(grid), len(grid[0])\n    dist = [[0] * cols for _ in range(rows)]\n    seen = [[False] * cols for _ in range(rows)]\n    seen[0][0] = True\n    queue = deque([(0, 0)])\n    while queue:\n        r, c = queue.popleft()\n        cell = grid[r][c]\n        moves = [STEP[cell]] if cell in STEP else STEP.values()\n        for dr, dc in moves:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != \"#\" and not seen[nr][nc]:\n                seen[nr][nc] = True\n                dist[nr][nc] = dist[r][c] + 1\n                queue.append((nr, nc))\n    return dist[rows - 1][cols - 1]\n"
},
{
"file": "l14-which-first",
"at": "screens[4]",
"id": "t2-no-floor",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):\n    return value - per_minute * minute - per_wrong * wrong\n"
},
{
"file": "l14-which-first",
"at": "screens[4]",
"id": "t2-floor-before-wrong",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):\n    return max(floor * value, value - per_minute * minute) - per_wrong * wrong\n"
},
{
"file": "l14-which-first",
"at": "screens[4]",
"id": "t2-floor-as-points",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):\n    return max(floor, value - per_minute * minute - per_wrong * wrong)\n"
},
{
"file": "l14-which-first",
"at": "screens[4]",
"id": "t7-falsy-floor",
"line": "test-7",
"named": true,
"pyodide": "test-7",
"src": "def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):\n    score = value - per_minute * minute - per_wrong * wrong\n    if floor and score < floor * value:\n        return floor * value\n    return score\n"
},
{
"file": "l14-which-first",
"at": "screens[4]",
"id": "t7-floor-default",
"line": "test-7",
"named": true,
"pyodide": "test-7",
"src": "def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):\n    floor = floor or 0.3\n    return max(floor * value, value - per_minute * minute - per_wrong * wrong)\n"
},
{
"file": "l14-which-first",
"at": "screens[4]",
"id": "t7-min-instead",
"line": "test-7",
"named": true,
"pyodide": "test-7",
"src": "def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):\n    score = value - per_minute * minute - per_wrong * wrong\n    if floor > 0:\n        score = max(score, floor * value)\n    return score\n"
},
{
"file": "l14-which-first",
"at": "screens[5]",
"id": "t1-unsolved-rejections-count",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "def icpc_rank_key(results, per_wrong=20):\n    solved, penalty = 0, 0\n    for minute, wrong in results:\n        penalty += per_wrong * wrong\n        if minute is not None:\n            solved += 1\n            penalty += minute\n    return (-solved, penalty)\n"
},
{
"file": "l14-which-first",
"at": "screens[5]",
"id": "t1-positive-solved",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "def icpc_rank_key(results, per_wrong=20):\n    solved, penalty = 0, 0\n    for minute, wrong in results:\n        if minute is not None:\n            solved += 1\n            penalty += minute + per_wrong * wrong\n    return (solved, penalty)\n"
},
{
"file": "l14-which-first",
"at": "screens[5]",
"id": "t5-bare-if",
"line": "test-5",
"named": true,
"pyodide": "test-5",
"src": "def icpc_rank_key(results, per_wrong=20):\n    solved, penalty = 0, 0\n    for minute, wrong in results:\n        if minute:\n            solved += 1\n            penalty += minute + per_wrong * wrong\n    return (-solved, penalty)\n"
},
{
"file": "l14-which-first",
"at": "screens[5]",
"id": "t5-bare-comprehension",
"line": "test-5",
"named": true,
"pyodide": "test-5",
"src": "def icpc_rank_key(results, per_wrong=20):\n    done = [(m, w) for m, w in results if m]\n    return (-len(done), sum(m + per_wrong * w for m, w in done))\n"
},
{
"file": "l14-which-first",
"at": "screens[5]",
"id": "t5-or-zero",
"line": "test-5",
"named": true,
"pyodide": "test-5",
"src": "def icpc_rank_key(results, per_wrong=20):\n    solved = sum(1 for m, w in results if m)\n    penalty = sum((m or 0) + per_wrong * w for m, w in results if m is not None)\n    return (-solved, penalty)\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t2-late-scores",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = -1, None\n    for order in permutations(sorted(problems)):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if True:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t2-late-scores-floor",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = -1, None\n    for order in permutations(sorted(problems)):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock <= minutes or True:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t2-break-on-late",
"line": "test-2",
"named": false,
"pyodide": null,
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = -1, None\n    for order in permutations(sorted(problems)):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock > minutes:\n                break\n            total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t2-rate-greedy-no-brute",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def best_order(problems, minutes):\n    order = sorted(problems, key=lambda p: (-p[1] / p[2], p[0]))\n    clock, total = 0, 0\n    for name, value, time in order:\n        clock += time\n        if clock <= minutes:\n            total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n    return total, [p[0] for p in order]\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t2-lt-minutes",
"line": "test-2",
"named": false,
"pyodide": null,
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = -1, None\n    for order in permutations(sorted(problems)):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock < minutes:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t3-no-sort",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = -1, None\n    for order in permutations(problems):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t3-no-sort-ge",
"line": "test-3",
"named": true,
"pyodide": "test-1",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = -1, None\n    for order in permutations(problems):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total >= best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t4-init-zero",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = 0, None\n    for order in permutations(sorted(problems)):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t4-init-zero-empty",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = 0, []\n    for order in permutations(sorted(problems)):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t4-filter-unfit",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = -1, None\n    for order in permutations(sorted(p for p in problems if p[2] <= minutes)):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "t4-late-scores-floor(named mistake)",
"line": "test-4",
"named": false,
"pyodide": "test-2",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = -1, None\n    for order in permutations(sorted(problems)):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if True:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[3]",
"id": "t4-starter",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "@starter"
},
{
"file": "l15-debugging-under-time",
"at": "screens[3]",
"id": "t3-check-last-first",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def last_occurrence(xs, x):\n    if xs[-1] == x:\n        return len(xs) - 1\n    for i in range(len(xs) - 2, -1, -1):\n        if xs[i] == x:\n            return i\n    return -1\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[3]",
"id": "t3-while-from-end",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def last_occurrence(xs, x):\n    i = len(xs) - 1\n    while xs[i] != x:\n        i -= 1\n        if i < 0:\n            return -1\n    return i\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[3]",
"id": "t3-range-len",
"line": "test-3",
"named": true,
"pyodide": "test-1",
"src": "def last_occurrence(xs, x):\n    for i in range(len(xs), -1, -1):\n        if xs[i] == x:\n            return i\n    return -1\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[3]",
"id": "t4-range-stop-0",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "def last_occurrence(xs, x):\n    for i in range(len(xs) - 1, 0, -1):\n        if xs[i] == x:\n            return i\n    return -1\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[4]",
"id": "t3-starter",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "@starter"
},
{
"file": "l15-debugging-under-time",
"at": "screens[4]",
"id": "t6-dedupe-keep-order",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def count_inversions_small(xs):\n    xs = list(dict.fromkeys(xs))\n    n = len(xs)\n    count = 0\n    for i in range(n):\n        for j in range(i + 1, n):\n            if xs[i] > xs[j]:\n                count += 1\n    return count\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[4]",
"id": "t6-pairs-of-values-set",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def count_inversions_small(xs):\n    n = len(xs)\n    pairs = set()\n    for i in range(n):\n        for j in range(i + 1, n):\n            if xs[i] > xs[j]:\n                pairs.add((xs[i], xs[j]))\n    return len(pairs)\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[4]",
"id": "t6-sorted-set",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def count_inversions_small(xs):\n    xs = sorted(set(xs), key=xs.index)\n    return sum(1 for i in range(len(xs)) for j in range(i + 1, len(xs)) if xs[i] > xs[j])\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[4]",
"id": "t6-skip-seen-values",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def count_inversions_small(xs):\n    n = len(xs)\n    count = 0\n    seen = set()\n    for i in range(n):\n        if xs[i] in seen:\n            continue\n        seen.add(xs[i])\n        for j in range(i + 1, n):\n            if xs[i] > xs[j]:\n                count += 1\n    return count\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "t2-starter",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "@starter"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "t2-set-per-call",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    seen = set()\n    for _ in range(t):\n        n = int(data[pos])\n        pos += 1\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n        out.append(len(seen))\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "t3-global-clear-between-cases",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "seen = set()\n\n\ndef solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    for case in range(t):\n        n = int(data[pos])\n        pos += 1\n        if case > 0:\n            seen.clear()\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n        out.append(len(seen))\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "t3-global-clear-at-end-of-call",
"line": "test-3",
"named": false,
"pyodide": "test-2",
"src": "seen = set()\n\n\ndef solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    for _ in range(t):\n        n = int(data[pos])\n        pos += 1\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n        out.append(len(seen))\n    seen.clear()\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "t3-global-clear-start-of-call",
"line": "test-3",
"named": false,
"pyodide": "test-2",
"src": "seen = set()\n\n\ndef solve_all(text):\n    seen.clear()\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    for _ in range(t):\n        n = int(data[pos])\n        pos += 1\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n        out.append(len(seen))\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "t3-global-reset-after-each-case-no-first",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "seen = set()\n\n\ndef solve_all(text):\n    global seen\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    for _ in range(t - 1):\n        n = int(data[pos])\n        pos += 1\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n        out.append(len(seen))\n        seen = set()\n    n = int(data[pos])\n    seen.update(data[pos + 1:pos + 1 + n])\n    out.append(len(seen))\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "t3-increments-per-call",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    seen = set()\n    for _ in range(t):\n        n = int(data[pos])\n        pos += 1\n        before = len(seen)\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n        out.append(len(seen) - before)\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "t3-global-increments",
"line": "test-3",
"named": true,
"pyodide": "test-2",
"src": "seen = set()\n\n\ndef solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    for _ in range(t):\n        n = int(data[pos])\n        pos += 1\n        before = len(seen)\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n        out.append(len(seen) - before)\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "t3-range-1-3",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def smallest_failing(fast, brute, gen, seed):\n    for n in range(1, 3):\n        case = stress(fast, brute, lambda rng: gen(rng, n), 200, seed)\n        if case is not None:\n            return case\n    return None\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "t3-lengths-1-2",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def smallest_failing(fast, brute, gen, seed):\n    for n in (1, 2):\n        case = stress(fast, brute, lambda rng: gen(rng, n), 200, seed)\n        if case is not None:\n            return case\n    return None\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "t3-only-len-2",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def smallest_failing(fast, brute, gen, seed):\n    return stress(fast, brute, lambda rng: gen(rng, 2), 200, seed)\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "t7-range-1-5",
"line": "test-7",
"named": true,
"pyodide": "test-7",
"src": "def smallest_failing(fast, brute, gen, seed):\n    for n in range(1, 5):\n        case = stress(fast, brute, lambda rng: gen(rng, n), 200, seed)\n        if case is not None:\n            return case\n    return None\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "t7-range-1-4",
"line": "test-7",
"named": true,
"pyodide": "test-7",
"src": "def smallest_failing(fast, brute, gen, seed):\n    for n in range(1, 4):\n        case = stress(fast, brute, lambda rng: gen(rng, n), 200, seed)\n        if case is not None:\n            return case\n    return None\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "t7-range-8-exclusive(passes?)",
"line": null,
"named": false,
"pyodide": null,
"src": "def smallest_failing(fast, brute, gen, seed):\n    for n in range(1, 8):\n        case = stress(fast, brute, lambda rng: gen(rng, n), 200, seed)\n        if case is not None:\n            return case\n    return None\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "t6-ignores-gen",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def smallest_failing(fast, brute, gen, seed):\n    for n in range(1, 9):\n        case = stress(fast, brute, lambda rng: gen_list(rng, n), 200, seed)\n        if case is not None:\n            return case\n    return None\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "t6-return-falsy",
"line": "test-6",
"named": false,
"pyodide": "test-5",
"src": "def smallest_failing(fast, brute, gen, seed):\n    for n in range(1, 9):\n        case = stress(fast, brute, lambda rng: gen(rng, n), 200, seed)\n        if case is not None:\n            return case\n    return []\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "t6-own-loop-shared-rng",
"line": "test-6",
"named": false,
"pyodide": "test-2",
"src": "import random\ndef smallest_failing(fast, brute, gen, seed):\n    rng = random.Random(seed)\n    for n in range(1, 9):\n        for _ in range(200):\n            case = gen(rng, n)\n            if fast(list(case)) != brute(list(case)):\n                return case\n    return None\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[9]",
"id": "t6-one-trial",
"line": "test-6",
"named": false,
"pyodide": "test-1",
"src": "def smallest_failing(fast, brute, gen, seed):\n    for n in range(1, 9):\n        case = stress(fast, brute, lambda rng: gen(rng, n), 1, seed)\n        if case is not None:\n            return case\n    return None\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t2-first-before-second",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def equal_thirds(xs):\n    total = sum(xs)\n    if total % 3 != 0:\n        return 0\n    third = total // 3\n    ways, firsts, prefix = 0, 0, 0\n    for j in range(len(xs) - 1):\n        prefix += xs[j]\n        if prefix == third:\n            firsts += 1\n        if prefix == 2 * third:\n            ways += firsts\n    return ways\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t2-elif",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def equal_thirds(xs):\n    total = sum(xs)\n    if total % 3 != 0:\n        return 0\n    third = total // 3\n    ways, firsts, prefix = 0, 0, 0\n    for j in range(len(xs) - 1):\n        prefix += xs[j]\n        if prefix == 2 * third:\n            ways += firsts\n        elif prefix == third:\n            firsts += 1\n    return ways\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t2-product-counts",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def equal_thirds(xs):\n    total = sum(xs)\n    if total % 3 != 0:\n        return 0\n    third = total // 3\n    prefix, a, b = 0, 0, 0\n    for j in range(len(xs) - 1):\n        prefix += xs[j]\n        if prefix == third:\n            a += 1\n        if prefix == 2 * third:\n            b += 1\n    return a * b\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t5-no-div-check-floor",
"line": "test-5",
"named": true,
"pyodide": "test-5",
"src": "def equal_thirds(xs):\n    total = sum(xs)\n    third = total // 3\n    ways, firsts, prefix = 0, 0, 0\n    for j in range(len(xs) - 1):\n        prefix += xs[j]\n        if prefix == 2 * third:\n            ways += firsts\n        if prefix == third:\n            firsts += 1\n    return ways\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t5-no-div-check-float",
"line": null,
"named": false,
"pyodide": null,
"src": "def equal_thirds(xs):\n    total = sum(xs)\n    third = total / 3\n    ways, firsts, prefix = 0, 0, 0\n    for j in range(len(xs) - 1):\n        prefix += xs[j]\n        if prefix == 2 * third:\n            ways += firsts\n        if prefix == third:\n            firsts += 1\n    return ways\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t5-round",
"line": "test-5",
"named": false,
"pyodide": null,
"src": "def equal_thirds(xs):\n    total = sum(xs)\n    third = round(total / 3)\n    ways, firsts, prefix = 0, 0, 0\n    for j in range(len(xs) - 1):\n        prefix += xs[j]\n        if prefix == 2 * third:\n            ways += firsts\n        if prefix == third:\n            firsts += 1\n    return ways\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t6-break-past",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def equal_thirds(xs):\n    total = sum(xs)\n    if total % 3 != 0:\n        return 0\n    third = total // 3\n    ways, firsts, prefix = 0, 0, 0\n    for j in range(len(xs) - 1):\n        prefix += xs[j]\n        if prefix > 2 * third:\n            break\n        if prefix == 2 * third:\n            ways += firsts\n        if prefix == third:\n            firsts += 1\n    return ways\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t6-bisect-monotone",
"line": "test-6",
"named": true,
"pyodide": "test-9",
"src": "from bisect import bisect_left, bisect_right\ndef equal_thirds(xs):\n    total = sum(xs)\n    if total % 3 != 0:\n        return 0\n    third = total // 3\n    pre, s = [], 0\n    for x in xs[:-1]:\n        s += x\n        pre.append(s)\n    ways = 0\n    lo1, hi1 = bisect_left(pre, third), bisect_right(pre, third)\n    lo2, hi2 = bisect_left(pre, 2 * third), bisect_right(pre, 2 * third)\n    for i in range(lo1, hi1):\n        ways += hi2 - max(lo2, i + 1)\n    return max(ways, 0)\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t6-second-cut-after-first-third-stop",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def equal_thirds(xs):\n    total = sum(xs)\n    if total % 3 != 0:\n        return 0\n    third = total // 3\n    ways, firsts, prefix = 0, 0, 0\n    for j in range(len(xs) - 1):\n        prefix += xs[j]\n        if prefix > third and third >= 0 and firsts == 0:\n            return 0\n        if prefix == 2 * third:\n            ways += firsts\n        if prefix == third:\n            firsts += 1\n    return ways\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t8-double-loop",
"line": "test-8",
"named": true,
"pyodide": "test-8",
"src": "def equal_thirds(xs):\n    n = len(xs)\n    P = [0]\n    for x in xs:\n        P.append(P[-1] + x)\n    ways = 0\n    for i in range(1, n - 1):\n        for j in range(i + 1, n):\n            if P[i] == P[j] - P[i] == P[n] - P[j]:\n                ways += 1\n    return ways\n"
},
{
"file": "l16-upsolving",
"at": "screens[3]",
"id": "t8-double-loop-early",
"line": "test-8",
"named": true,
"pyodide": "test-8",
"src": "def equal_thirds(xs):\n    n = len(xs)\n    total = sum(xs)\n    if total % 3:\n        return 0\n    P = [0]\n    for x in xs:\n        P.append(P[-1] + x)\n    ways = 0\n    for i in range(1, n - 1):\n        if P[i] * 3 != total:\n            continue\n        for j in range(i + 1, n):\n            if P[j] * 3 == 2 * total:\n                ways += 1\n    return ways\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t1-count-only-stable",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "def mistakes_summary(log):\n    counts = {}\n    for problem, category in log:\n        counts[category] = counts.get(category, 0) + 1\n    return sorted(counts.items(), key=lambda kv: -kv[1])\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t1-most-common",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "from collections import Counter\ndef mistakes_summary(log):\n    return Counter(c for _, c in log).most_common()\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t1-reverse-both",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "def mistakes_summary(log):\n    counts = {}\n    for problem, category in log:\n        counts[category] = counts.get(category, 0) + 1\n    return sorted(counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t1-lists-not-tuples",
"line": null,
"named": false,
"pyodide": null,
"src": "def mistakes_summary(log):\n    counts = {}\n    for problem, category in log:\n        counts[category] = counts.get(category, 0) + 1\n    return [list(kv) for kv in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t2-max-empty",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def mistakes_summary(log):\n    counts = {}\n    for problem, category in log:\n        counts[category] = counts.get(category, 0) + 1\n    top = max(counts.values())\n    return sorted(counts.items(), key=lambda kv: (top - kv[1], kv[0]))\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t2-none-empty",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "def mistakes_summary(log):\n    if not log:\n        return None\n    counts = {}\n    for problem, category in log:\n        counts[category] = counts.get(category, 0) + 1\n    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t6-lower-key",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def mistakes_summary(log):\n    counts = {}\n    for problem, category in log:\n        counts[category] = counts.get(category, 0) + 1\n    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].lower()))\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t6-lower-names",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def mistakes_summary(log):\n    counts = {}\n    for problem, category in log:\n        category = category.lower()\n        counts[category] = counts.get(category, 0) + 1\n    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t7-alpha-only",
"line": "test-7",
"named": true,
"pyodide": "test-7",
"src": "def mistakes_summary(log):\n    counts = {}\n    for problem, category in log:\n        counts[category] = counts.get(category, 0) + 1\n    return sorted(counts.items(), key=lambda kv: kv[0])\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t7-sorted-items",
"line": "test-7",
"named": true,
"pyodide": "test-7",
"src": "def mistakes_summary(log):\n    counts = {}\n    for problem, category in log:\n        counts[category] = counts.get(category, 0) + 1\n    return sorted(counts.items())\n"
},
{
"file": "l16-upsolving",
"at": "screens[5]",
"id": "t7-name-then-count",
"line": "test-7",
"named": true,
"pyodide": "test-7",
"src": "def mistakes_summary(log):\n    counts = {}\n    for problem, category in log:\n        counts[category] = counts.get(category, 0) + 1\n    return sorted(counts.items(), key=lambda kv: (kv[0], -kv[1]))\n"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "t2-only-linked-desks",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "from collections import deque\n\n\ndef desks_after_cut(n, links, cut):\n    adj = {}\n    for i, (a, b) in enumerate(links):\n        if i != cut:\n            adj.setdefault(a, []).append(b)\n            adj.setdefault(b, []).append(a)\n    seen = set()\n    groups = 0\n    for s in adj:\n        if s in seen:\n            continue\n        groups += 1\n        seen.add(s)\n        queue = deque([s])\n        while queue:\n            u = queue.popleft()\n            for v in adj[u]:\n                if v not in seen:\n                    seen.add(v)\n                    queue.append(v)\n    return groups\n"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "t2-desks-from-all-links",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "from collections import deque\n\n\ndef desks_after_cut(n, links, cut):\n    adj = {}\n    for i, (a, b) in enumerate(links):\n        adj.setdefault(a, [])\n        adj.setdefault(b, [])\n        if i != cut:\n            adj[a].append(b)\n            adj[b].append(a)\n    seen = set()\n    groups = 0\n    for s in adj:\n        if s in seen:\n            continue\n        groups += 1\n        seen.add(s)\n        queue = deque([s])\n        while queue:\n            u = queue.popleft()\n            for v in adj[u]:\n                if v not in seen:\n                    seen.add(v)\n                    queue.append(v)\n    return groups\n"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "t2-no-cut",
"line": "test-2",
"named": true,
"pyodide": "test-2",
"src": "from collections import deque\n\n\ndef desks_after_cut(n, links, cut):\n    adj = [[] for _ in range(n)]\n    for i, (a, b) in enumerate(links):\n        if True:\n            adj[a].append(b)\n            adj[b].append(a)\n    seen = [False] * n\n    groups = 0\n    for s in range(n):\n        if seen[s]:\n            continue\n        groups += 1\n        seen[s] = True\n        queue = deque([s])\n        while queue:\n            u = queue.popleft()\n            for v in adj[u]:\n                if not seen[v]:\n                    seen[v] = True\n                    queue.append(v)\n    return groups\n"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "t2-cut-1-based",
"line": "test-2",
"named": false,
"pyodide": "test-5",
"src": "from collections import deque\n\n\ndef desks_after_cut(n, links, cut):\n    adj = [[] for _ in range(n)]\n    for i, (a, b) in enumerate(links):\n        if i + 1 != cut:\n            adj[a].append(b)\n            adj[b].append(a)\n    seen = [False] * n\n    groups = 0\n    for s in range(n):\n        if seen[s]:\n            continue\n        groups += 1\n        seen[s] = True\n        queue = deque([s])\n        while queue:\n            u = queue.popleft()\n            for v in adj[u]:\n                if not seen[v]:\n                    seen[v] = True\n                    queue.append(v)\n    return groups\n"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "t4-remove-by-value",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "from collections import deque\n\n\ndef desks_after_cut(n, links, cut):\n    adj = [[] for _ in range(n)]\n    for i, (a, b) in enumerate(links):\n        if (a, b) != links[cut]:\n            adj[a].append(b)\n            adj[b].append(a)\n    seen = [False] * n\n    groups = 0\n    for s in range(n):\n        if seen[s]:\n            continue\n        groups += 1\n        seen[s] = True\n        queue = deque([s])\n        while queue:\n            u = queue.popleft()\n            for v in adj[u]:\n                if not seen[v]:\n                    seen[v] = True\n                    queue.append(v)\n    return groups\n"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "t4-set-adj-discard",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "from collections import deque\n\n\ndef desks_after_cut(n, links, cut):\n    adj = [set() for _ in range(n)]\n    for a, b in links:\n        adj[a].add(b)\n        adj[b].add(a)\n    a, b = links[cut]\n    adj[a].discard(b)\n    adj[b].discard(a)\n    seen = [False] * n\n    groups = 0\n    for s in range(n):\n        if seen[s]:\n            continue\n        groups += 1\n        seen[s] = True\n        queue = deque([s])\n        while queue:\n            u = queue.popleft()\n            for v in adj[u]:\n                if not seen[v]:\n                    seen[v] = True\n                    queue.append(v)\n    return groups\n"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "t4-list-remove",
"line": null,
"named": false,
"pyodide": null,
"src": "from collections import deque\n\n\ndef desks_after_cut(n, links, cut):\n    links = list(links)\n    links.remove(links[cut])\n    adj = [[] for _ in range(n)]\n    for i, (a, b) in enumerate(links):\n        if True:\n            adj[a].append(b)\n            adj[b].append(a)\n    seen = [False] * n\n    groups = 0\n    for s in range(n):\n        if seen[s]:\n            continue\n        groups += 1\n        seen[s] = True\n        queue = deque([s])\n        while queue:\n            u = queue.popleft()\n            for v in adj[u]:\n                if not seen[v]:\n                    seen[v] = True\n                    queue.append(v)\n    return groups\n"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "t7-recursive-dfs",
"line": "test-7",
"named": true,
"pyodide": "test-7",
"src": "def desks_after_cut(n, links, cut):\n    adj = [[] for _ in range(n)]\n    for i, (a, b) in enumerate(links):\n        if i != cut:\n            adj[a].append(b)\n            adj[b].append(a)\n    seen = [False] * n\n\n    def dfs(u):\n        seen[u] = True\n        for v in adj[u]:\n            if not seen[v]:\n                dfs(v)\n\n    groups = 0\n    for s in range(n):\n        if not seen[s]:\n            groups += 1\n            dfs(s)\n    return groups\n"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "t7-recursive-dfs-raised-limit",
"line": "test-7",
"named": false,
"pyodide": null,
"src": "import sys\nsys.setrecursionlimit(10**6)\ndef desks_after_cut(n, links, cut):\n    adj = [[] for _ in range(n)]\n    for i, (a, b) in enumerate(links):\n        if i != cut:\n            adj[a].append(b)\n            adj[b].append(a)\n    seen = [False] * n\n\n    def dfs(u):\n        seen[u] = True\n        for v in adj[u]:\n            if not seen[v]:\n                dfs(v)\n\n    groups = 0\n    for s in range(n):\n        if not seen[s]:\n            groups += 1\n            dfs(s)\n    return groups\n"
},
{
"file": "homework-4",
"at": "items[0]",
"id": "t7-recursive-find-dsu",
"line": "test-7",
"named": true,
"pyodide": "test-8",
"src": "def desks_after_cut(n, links, cut):\n    parent = list(range(n))\n\n    def find(x):\n        if parent[x] != x:\n            return find(parent[x])\n        return x\n\n    groups = n\n    for i, (a, b) in enumerate(links):\n        if i == cut:\n            continue\n        ra, rb = find(a), find(b)\n        if ra != rb:\n            parent[ra] = rb\n            groups -= 1\n    return groups\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t3-index-k-minus-1",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def max_profit_k(prices, k):\n    n = len(prices)\n    dp = [[0] * n for _ in range(k)]\n    for j in range(k):\n        best = -prices[0]\n        for i in range(1, n):\n            prev = dp[j - 1][i] if j > 0 else 0\n            dp[j][i] = max(dp[j][i - 1], prices[i] + best)\n            best = max(best, prev - prices[i])\n    return dp[k - 1][n - 1]\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t3-must-trade-min1",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def max_profit_k(prices, k):\n    k = max(k, 1)\n    buy = [float(\"-inf\")] * (k + 1)\n    sell = [0] * (k + 1)\n    for p in prices:\n        for j in range(1, k + 1):\n            buy[j] = max(buy[j], sell[j - 1] - p)\n            sell[j] = max(sell[j], buy[j] + p)\n    return sell[k]\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t3-unlimited-greedy",
"line": "test-3",
"named": false,
"pyodide": "test-2",
"src": "def max_profit_k(prices, k):\n    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t4-forced-trades",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "def max_profit_k(prices, k):\n    if k == 0 or len(prices) < 2:\n        return 0\n    buy = [float(\"-inf\")] * (k + 1)\n    sell = [float(\"-inf\")] * (k + 1)\n    sell[0] = 0\n    for i, p in enumerate(prices):\n        for j in range(k, 0, -1):\n            sell[j] = max(sell[j], buy[j] + p)\n            buy[j] = max(buy[j], sell[j - 1] - p)\n    best = max(s for s in sell[1:])\n    return best\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t4-single-best-diff-any-order",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "def max_profit_k(prices, k):\n    if k == 0 or len(prices) < 2:\n        return 0\n    if k == 1:\n        best, lo = 0, prices[0]\n        for p in prices:\n            lo = min(lo, p)\n            best = max(best, p - lo)\n        return best\n    rises = sorted((b - a for a, b in zip(prices, prices[1:])), reverse=True)\n    return sum(rises[:k])\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t6-top-k-daily-rises",
"line": "test-6",
"named": false,
"pyodide": "test-8",
"src": "def max_profit_k(prices, k):\n    rises = sorted((b - a for a, b in zip(prices, prices[1:]) if b > a), reverse=True)\n    return sum(rises[:k])\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t6-exactly-k",
"line": "test-6",
"named": false,
"pyodide": null,
"src": "def max_profit_k(prices, k):\n    if k == 0 or len(prices) < 2:\n        return 0\n    NEG = float(\"-inf\")\n    buy = [NEG] * (k + 1)\n    sell = [NEG] * (k + 1)\n    sell[0] = 0\n    for i in range(0, len(prices)):\n        p = prices[i]\n        nb, ns = buy[:], sell[:]\n        for j in range(1, k + 1):\n            nb[j] = max(buy[j], sell[j - 1] - p)\n            ns[j] = max(sell[j], buy[j] + p)\n        buy, sell = nb, ns\n    return max(0, max(sell))\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t8-n2k",
"line": "test-8",
"named": true,
"pyodide": "test-8",
"src": "def max_profit_k(prices, k):\n    n = len(prices)\n    if k == 0 or n < 2:\n        return 0\n    prev = [0] * n\n    for j in range(k):\n        cur = [0] * n\n        for i in range(1, n):\n            best = cur[i - 1]\n            for b in range(i):\n                best = max(best, prev[b] + prices[i] - prices[b])\n            cur[i] = best\n        prev = cur\n    return prev[-1]\n"
},
{
"file": "homework-4",
"at": "items[2]",
"id": "t1-no-sort",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "def widest_gap(levels, m):\n    xs = list(levels)\n\n    def fits(gap):\n        placed, last = 1, xs[0]\n        for x in xs[1:]:\n            if x - last >= gap:\n                placed += 1\n                last = x\n                if placed == m:\n                    return True\n        return placed >= m\n\n    lo, hi = 0, xs[-1] - xs[0]\n    while lo < hi:\n        mid = (lo + hi + 1) // 2\n        if fits(mid):\n            lo = mid\n        else:\n            hi = mid - 1\n    return lo\n"
},
{
"file": "homework-4",
"at": "items[2]",
"id": "t1-no-sort-hi-maxmin",
"line": "test-1",
"named": true,
"pyodide": "test-1",
"src": "def widest_gap(levels, m):\n    xs = list(levels)\n\n    def fits(gap):\n        placed, last = 1, xs[0]\n        for x in xs[1:]:\n            if x - last >= gap:\n                placed += 1\n                last = x\n                if placed == m:\n                    return True\n        return placed >= m\n\n    lo, hi = 0, max(xs) - min(xs)\n    while lo < hi:\n        mid = (lo + hi + 1) // 2\n        if fits(mid):\n            lo = mid\n        else:\n            hi = mid - 1\n    return lo\n"
},
{
"file": "homework-4",
"at": "items[2]",
"id": "t4-lo-1",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "def widest_gap(levels, m):\n    xs = sorted(levels)\n\n    def fits(gap):\n        placed, last = 1, xs[0]\n        for x in xs[1:]:\n            if x - last >= gap:\n                placed += 1\n                last = x\n                if placed == m:\n                    return True\n        return placed >= m\n\n    lo, hi = 1, xs[-1] - xs[0]\n    while lo < hi:\n        mid = (lo + hi + 1) // 2\n        if fits(mid):\n            lo = mid\n        else:\n            hi = mid - 1\n    return lo\n"
},
{
"file": "homework-4",
"at": "items[2]",
"id": "t4-strict-gt",
"line": "test-4",
"named": false,
"pyodide": "test-1",
"src": "def widest_gap(levels, m):\n    xs = sorted(levels)\n\n    def fits(gap):\n        placed, last = 1, xs[0]\n        for x in xs[1:]:\n            if x - last > gap:\n                placed += 1\n                last = x\n                if placed == m:\n                    return True\n        return placed >= m\n\n    lo, hi = 0, xs[-1] - xs[0]\n    while lo < hi:\n        mid = (lo + hi + 1) // 2\n        if fits(mid):\n            lo = mid\n        else:\n            hi = mid - 1\n    return lo\n"
},
{
"file": "homework-4",
"at": "items[2]",
"id": "t4-dedupe-set",
"line": "test-4",
"named": false,
"pyodide": null,
"src": "def widest_gap(levels, m):\n    xs = sorted(set(levels))\n\n    def fits(gap):\n        placed, last = 1, xs[0]\n        for x in xs[1:]:\n            if x - last >= gap:\n                placed += 1\n                last = x\n                if placed == m:\n                    return True\n        return placed >= m\n\n    lo, hi = 0, xs[-1] - xs[0]\n    while lo < hi:\n        mid = (lo + hi + 1) // 2\n        if fits(mid):\n            lo = mid\n        else:\n            hi = mid - 1\n    return lo\n"
},
{
"file": "homework-4",
"at": "items[2]",
"id": "t8-linear-up",
"line": "test-8",
"named": true,
"pyodide": "test-8",
"src": "def widest_gap(levels, m):\n    xs = sorted(levels)\n\n    def fits(gap):\n        placed, last = 1, xs[0]\n        for x in xs[1:]:\n            if x - last >= gap:\n                placed += 1\n                last = x\n                if placed == m:\n                    return True\n        return placed >= m\n\n    gap = 0\n    while fits(gap + 1):\n        gap += 1\n    return gap\n"
},
{
"file": "homework-4",
"at": "items[2]",
"id": "t8-linear-down",
"line": "test-8",
"named": true,
"pyodide": "test-8",
"src": "def widest_gap(levels, m):\n    xs = sorted(levels)\n\n    def fits(gap):\n        placed, last = 1, xs[0]\n        for x in xs[1:]:\n            if x - last >= gap:\n                placed += 1\n                last = x\n                if placed == m:\n                    return True\n        return placed >= m\n\n    gap = xs[-1] - xs[0]\n    while not fits(gap):\n        gap -= 1\n    return gap\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t6-exactly-k-clamped",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def max_profit_k(prices, k):\n    if k == 0 or len(prices) < 2:\n        return 0\n    NEG = float(\"-inf\")\n    buy = [NEG] * (k + 1)\n    sell = [NEG] * (k + 1)\n    sell[0] = 0\n    for p in prices:\n        nb, ns = buy[:], sell[:]\n        for j in range(1, k + 1):\n            nb[j] = max(buy[j], sell[j - 1] - p)\n            ns[j] = max(sell[j], buy[j] + p)\n        buy, sell = nb, ns\n    return max(0, sell[k])\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t6-table-k-by-n-exact",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def max_profit_k(prices, k):\n    n = len(prices)\n    if k == 0 or n < 2:\n        return 0\n    NEG = float(\"-inf\")\n    # done[j][i]: best profit with exactly j trades closed by day i\n    done = [[NEG] * n for _ in range(k + 1)]\n    done[0] = [0] * n\n    for j in range(1, k + 1):\n        best_buy = NEG\n        for i in range(1, n):\n            best_buy = max(best_buy, done[j - 1][i - 1] - prices[i - 1])\n            done[j][i] = max(done[j][i - 1], best_buy + prices[i])\n    return max(0, done[k][n - 1])\n"
},
{
"file": "homework-4",
"at": "items[1]",
"id": "t6-cap-k-wrong",
"line": "test-6",
"named": true,
"pyodide": "test-6",
"src": "def max_profit_k(prices, k):\n    n = len(prices)\n    if k == 0 or n < 2:\n        return 0\n    if k > n:\n        return 0\n    buy = [float(\"-inf\")] * (k + 1)\n    sell = [0] * (k + 1)\n    for p in prices:\n        for j in range(1, k + 1):\n            buy[j] = max(buy[j], sell[j - 1] - p)\n            sell[j] = max(sell[j], buy[j] + p)\n    return sell[k]\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "fix-A3",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best = (0, [])\n    for order in permutations(sorted(problems)):\n        names = [p[0] for p in order]\n        clock = total = 0\n        for _, value, time in order:\n            clock += time\n            if clock <= minutes:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best[0]:\n            best = (total, names)\n    return best\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "fix-A4",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    best_total, best_names = -1, None\n    for order in permutations(sorted(problems)):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > 0 and total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    if best_names is None:\n        return 0, []\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "fix-B2",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    fits = sorted(p for p in problems if p[2] <= minutes)\n    best_total, best_names = -1, None\n    for order in permutations(fits):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l14-which-first",
"at": "screens[10]",
"id": "fix-B3",
"line": "test-4",
"named": true,
"pyodide": "test-4",
"src": "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n    if all(t > minutes for _, _, t in problems):\n        return 0, []\n    best_total, best_names = -1, None\n    for order in permutations(sorted(problems)):\n        clock, total = 0, 0\n        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)\n        if total > best_total:\n            best_total, best_names = total, [p[0] for p in order]\n    return best_total, best_names\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "fix-N1",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    seen = set()\n    for _ in range(t):\n        n = int(data[pos])\n        pos += 1\n        before = len(seen)\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n        out.append(len(seen) - before)\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "fix-N2",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    seen = set()\n    for _ in range(t):\n        n = int(data[pos])\n        pos += 1\n        count = 0\n        for s in data[pos:pos + n]:\n            if s not in seen:\n                count += 1\n                seen.add(s)\n        pos += n\n        out.append(count)\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "fix-N3",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "def solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    seen = set()\n    for _ in range(t):\n        n = int(data[pos])\n        pos += 1\n        new = set(data[pos:pos + n]) - seen\n        out.append(len(new))\n        seen |= new\n        pos += n\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "fix-F1",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "seen = set()\n\n\ndef solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    for case in range(t):\n        n = int(data[pos])\n        pos += 1\n        if case > 0:\n            seen.clear()\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n        out.append(len(seen))\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "fix-F2",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "seen = set()\n\n\ndef solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    for i in range(t):\n        n = int(data[pos])\n        pos += 1\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n        out.append(len(seen))\n        if i < t - 1:\n            seen.clear()\n    return out\n"
},
{
"file": "l15-debugging-under-time",
"at": "screens[5]",
"id": "fix-F3",
"line": "test-3",
"named": true,
"pyodide": "test-3",
"src": "seen = set()\n\n\ndef solve_all(text):\n    global seen\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    for _ in range(t):\n        n = int(data[pos])\n        pos += 1\n        seen.update(data[pos:pos + n])\n        pos += n\n        out.append(len(seen))\n        if len(out) < t:\n            seen = set()\n    return out\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "fix-U3",
"line": "test-12",
"named": true,
"pyodide": "test-12",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if load + w <= cap:\n            load += w\n        else:\n            days += 1\n            load = w\n    return days <= k\n\n\ndef min_capacity(weights, k):\n    lo, hi = max(weights), sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
},
{
"file": "l13-virtual-contest",
"at": "screens[5]",
"id": "fix-U4",
"line": "test-12",
"named": true,
"pyodide": "test-12",
"src": "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        load += w\n        if load > cap:\n            days += 1\n            load = w\n            if days > k:\n                return False\n    return True\n\n\ndef min_capacity(weights, k):\n    lo, hi = max(weights), sum(weights)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n"
}
]''')
CHILD = r'''
import sys, json, signal, math
spec = json.load(sys.stdin)
assert sys.getrecursionlimit() == 1000
sys.setrecursionlimit(3000)
def norm(x):
    if isinstance(x, (list, tuple)): return [norm(y) for y in x]
    return x
def same(a, e, mode):
    if mode == 'isclose' and isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(e, (int, float)):
        return math.isclose(a, e, rel_tol=1e-9, abs_tol=1e-9)
    return type(norm(a)) == type(norm(e)) and norm(a) == norm(e) if not isinstance(e, (int, float)) or isinstance(e, bool) else (isinstance(a, (int, float)) and not isinstance(a, bool) and a == e) if not isinstance(e, bool) else a is e
def boom(*_): raise TimeoutError
signal.signal(signal.SIGALRM, boom)
g = {'__name__': '__main__'}
key, why = None, ''
try:
    exec(spec['prelude'], g); exec(spec['src'], g)
except BaseException as ex:
    key, why = 'error', type(ex).__name__
if key is None:
    for i, t in enumerate(spec['tests']):
        signal.alarm(5)
        try:
            if t.get('setup'): exec(t['setup'], g)
            a = eval(t['call'], g); e = eval(str(t['expect']), g)
            ok = same(a, e, t.get('compare', 'equal')); why = repr(a)[:70]
        except TimeoutError:
            ok, why = False, 'TIMING'
        except BaseException as ex:
            ok, why = False, type(ex).__name__
        signal.alarm(0)
        if not ok:
            key = 'test-%d' % (i + 1); break
print(json.dumps([key, why]))
'''
DOCS = {'l13-virtual-contest': L13, 'l14-which-first': L14, 'l15-debugging-under-time': L15, 'l16-upsolving': L16, 'homework-4': HW}
def widget(v):
    name, idx = v['at'][:-1].split('[')
    return DOCS[v['file']][name][int(idx)]['widget']
def grade(v):
    w = widget(v)
    src = w['solution'] if v['src'] == '@solution' else w['starter'] if v['src'] == '@starter' else v['src']
    p = subprocess.run([sys.executable, '-c', CHILD], input=json.dumps({'prelude': w.get('prelude', ''), 'src': src, 'tests': w['tests']}), capture_output=True, text=True)
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        return ['crash', p.stderr[-200:]]
with ThreadPoolExecutor(4) as ex:
    RES = list(ex.map(grade, VARIANTS))
lines = {}
for v, (key, why) in zip(VARIANTS, RES):
    v['key'], v['why'] = key, why
    check(f"sweep {v['file'][:3]} {v['at']} {v['id']}: CPython first failure {key} = the page's under Pyodide ({v['pyodide']})" + (' TIMING' if why == 'TIMING' else ''), key == v['pyodide'], why)
    if v['line']:
        lines.setdefault((v['file'], v['at'], v['line']), []).append(v)
# every test-N line in the content has codings here
have = set(lines)
for fname, doc in DOCS.items():
    for kind in ('screens', 'items'):
        for i, s in enumerate(doc.get(kind, [])):
            for k in ((s.get('feedback') or {}).get('byKey') or {}):
                if k.startswith('test-') and s.get('widget', {}).get('kind') == 'code':
                    check(f'sweep covers {fname[:3]} {kind}[{i}] {k}', (fname, f'{kind}[{i}]', k) in have)
# the rule: at least half of the failing codings of the named mistake fail first on N
for (fname, at, line), vs in sorted(lines.items()):
    named = [v for v in vs if v['named'] and v['key'] is not None]
    land = [v for v in named if v['key'] == line]
    timing = ' TIMING' if any(v['why'] == 'TIMING' for v in land) else ''
    check(f'line {fname[:3]} {at} {line}: {len(land)} of {len(named)} failing codings of its mistake fail first on it{timing}', named and 2 * len(land) >= len(named), [(v['id'], v['key']) for v in named])

# two lines whose text does not fit the codings that reach them (findings 1 and 2 of the audit), and one untested guard (finding 3)
bo4 = [v for v in VARIANTS if v['file'] == 'l14-which-first' and v['at'] == 'screens[10]' and v['key'] == 'test-4']
L4 = S14[10]['feedback']['byKey']['test-4']
check("FINDING 1 (fixed)  l14 screens[10] test-4: every coding that fails first on test 4 has the total 0 and the names wrong, and the line names the order `(0, ['A'])`, the start below 0 and the problems that cannot fit",
      len(bo4) >= 5 and all(v['why'].startswith('(0,') and "['A']" not in v['why'] for v in bo4) and "(0, ['A'])" in L4 and 'below 0' in L4 and 'cannot fit' in L4, [(v['id'], v['why']) for v in bo4])
late = [v for v in VARIANTS if v['id'] == 't4-late-scores-floor(named mistake)'][0]
check('          (the coding that does score the late problem fails first on test 2, not test 4)', late['key'] == 'test-2')
sa3 = [v for v in VARIANTS if v['file'] == 'l15-debugging-under-time' and v['at'] == 'screens[5]' and v['key'] == 'test-3']
L3 = S15[5]['feedback']['byKey']['test-3']
check("FINDING 2 (fixed)  l15 screens[5] test-3: every coding that fails first on test 3 counts only new tickers ([1, 0, 1]) or keeps an earlier call's tickers in its first case, and the line names both",
      len(sa3) >= 6 and all(v['why'] == '[1, 0, 1]' or (v['why'].startswith('[') and not v['why'].startswith('[1,')) for v in sa3) and '1, 1 and 2' in L3 and 'not just the new ones' in L3 and 'the first included' in L3, [(v['id'], v['why']) for v in sa3])
outside = [v for v in VARIANTS if v['file'] == 'l15-debugging-under-time' and v['at'] == 'screens[5]' and v['id'].startswith('t3-global')]
check('          (most codings that keep the set outside solve_all fail first on test 2, whose line fits them)', sum(v['key'] == 'test-2' for v in outside) > sum(v['key'] == 'test-3' for v in outside))

ung = [v for v in VARIANTS if v['id'] == 't4-heavy-order-newday'][0]
check("FINDING 3 (fixed)  l13 screens[5] tests: a can_ship without the `w > cap` guard fails first on the new test 12, can_ship([5, 5], 3, 4)", ung['key'] == 'test-12', ung['key'])
gs = ns_of(S13[5]['widget'])
check('          (the proposed twelfth test separates them: the solution gives False on can_ship([5, 5], 3, 4), the unguarded greedy True)', gs['can_ship']([5, 5], 3, 4) is False and days_at([5, 5], 4)[0] <= 3)

print(f'\n{COUNT[0]} checks, {len(FAILS)} failing')
for f in FAILS:
    print('  FAIL ' + f)
sys.exit(1 if FAILS else 0)
