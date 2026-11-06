#!/usr/bin/env python3
"""Concept checks for systems L2 (l6 to l10, review-2, homework-2): exhaustive enumeration of every
interleaving, lock schedule and litmus test the lessons count; compiled checks of the spin-loop
claims (clang -O1 deletes it, g++ -O1 reads once); g++ runs of every C++ code item (solution passes
all hidden tests, starter fails at least one). Run from the repo root:
python3 -I docs/reports/systems-L2-concepts.py
Each assert names the ledger row (file: JSON path) in docs/reports/audit-systems-1-3-ledger.md."""
import json, os, random, shutil, subprocess, sys, tempfile
from collections import Counter
from math import comb, factorial

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'systems')
PASSED = []

def load(name):
    with open(os.path.join(COURSE, name + '.json')) as f:
        return json.load(f)

def check(name, cond, msg):
    assert cond, f'{name}: {msg}'
    PASSED.append(name)

# ---------------------------------------------------------------- C++ runner (same as L1 script)
CXX = shutil.which('g++') or shutil.which('clang++')

def cpp_lit(v, typ=None):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return f'{v}LL' if abs(v) > 2**31 - 1 else str(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, str):
        return 'std::string("' + v.replace('\\', '\\\\').replace('"', '\\"') + '")'
    if isinstance(v, list):
        if typ is None:
            if v and all(isinstance(x, str) for x in v):
                typ = 'std::vector<std::string>'
            else:
                typ = 'std::vector<int>'
        return typ + '{' + ', '.join(cpp_lit(x) for x in v) + '}'
    raise TypeError(repr(v))

def canon(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, list):
        return '[' + ','.join(canon(x) for x in v) + ']'
    return str(v)

HARNESS_SHOW = '''
template <class T> void show(const T& v) { std::cout << v; }
void show(bool v) { std::cout << (v ? "true" : "false"); }
void show(const std::string& s) { std::cout << s; }
template <class T> void show(const std::vector<T>& v) {
    std::cout << '['; for (size_t i = 0; i < v.size(); ++i) { if (i) std::cout << ','; show(v[i]); } std::cout << ']'; }
'''

def run_cpp(widget, code):
    body = []
    for t in widget['tests']:
        if 'args' in t:
            types = t.get('types') or [None] * len(t['args'])
            call = t['call'] + '(' + ', '.join(cpp_lit(a, ty) for a, ty in zip(t['args'], types)) + ')'
        else:
            call = t['call']
        body.append('    { ' + t.get('setup', '') + ' show(' + call + '); std::cout << "\\n"; }')
    src = ('#include <iostream>\n#include <string>\n#include <vector>\n' + widget.get('prelude', '') + '\n' + code
           + '\n' + HARNESS_SHOW + 'int main() {\n' + '\n'.join(body) + '\n    return 0;\n}\n')
    d = tempfile.mkdtemp()
    path = os.path.join(d, 'main.cpp')
    with open(path, 'w') as f:
        f.write(src)
    exe = os.path.join(d, 'a.out')
    r = subprocess.run([CXX, '-std=c++17', '-O1', '-w', '-o', exe, path], capture_output=True, text=True)
    if r.returncode != 0:
        return False, r.stderr
    return True, subprocess.run([exe], capture_output=True, text=True, timeout=300).stdout.splitlines()

def code_item(name, widget):
    expected = [canon(t.get('expect', [])) for t in widget['tests']]
    ok, lines = run_cpp(widget, widget['solution'])
    check(name + ':solution_compiles', ok, f'solution does not compile: {str(lines)[:600]}')
    bad = [(i, e, l) for i, (e, l) in enumerate(zip(expected, lines)) if e != l]
    check(name + ':solution_passes', len(lines) == len(expected) and not bad, f'solution fails {bad[:3]}')
    ok2, lines2 = run_cpp(widget, widget['starter'])
    fails = (not ok2) or len(lines2) != len(expected) or any(e != l for e, l in zip(expected, lines2))
    check(name + ':starter_fails', fails, 'the starter passes every hidden test')

# ---------------------------------------------------------------- interleaving enumerator
def enumerate_schedules(lanes, init):
    """lanes: list of step lists. Steps: ('load', reg, var), ('add', reg, by), ('store', var, reg),
    ('fetch', var, by), ('lock', L), ('unlock', L), ('setreg', reg, value), ('if', reg, cmp, value)
    (a lane whose 'if' fails skips the rest of its steps). A lane whose next step is a lock held by another
    lane is blocked. Returns Counter of outcomes keyed by (sorted vars tuple, sorted regs tuple, deadlocked)."""
    results = Counter()
    n = len(lanes)
    def rec(pc, vars_, regs, held):
        enabled = []
        for t in range(n):
            if pc[t] >= len(lanes[t]):
                continue
            step = lanes[t][pc[t]]
            if step[0] == 'lock' and held.get(step[1]) not in (None, t):
                continue
            if step[0] == 'lock' and held.get(step[1]) == t:
                continue   # self-lock: blocked forever (std::mutex)
            enabled.append(t)
        if not enabled:
            dead = any(pc[t] < len(lanes[t]) for t in range(n))
            results[(tuple(sorted(vars_.items())), tuple(sorted(regs.items())), dead)] += 1
            return
        for t in enabled:
            step = lanes[t][pc[t]]
            v2, r2, h2, p2 = dict(vars_), dict(regs), dict(held), list(pc)
            op = step[0]
            if op == 'load':
                r2[(t, step[1])] = v2[step[2]]
            elif op == 'add':
                r2[(t, step[1])] = r2.get((t, step[1]), 0) + step[2]
            elif op == 'store':
                v2[step[1]] = r2[(t, step[2])]
            elif op == 'fetch':
                v2[step[1]] += step[2]
            elif op == 'setvar':
                v2[step[1]] = step[2]
            elif op == 'lock':
                h2[step[1]] = t
            elif op == 'unlock':
                h2[step[1]] = None
            elif op == 'act':      # ('act', reg, var, amount, paid): one step: if reg >= amount, var = reg - amount, paid += amount
                if r2[(t, step[1])] >= step[3]:
                    v2[step[2]] = r2[(t, step[1])] - step[3]
                    v2[step[4]] += step[3]
            elif op == 'if':
                val = r2[(t, step[1])]
                ok = (val >= step[3]) if step[2] == '>=' else (val == step[3])
                if not ok:
                    p2[t] = len(lanes[t])
                    rec(p2, v2, r2, h2)
                    continue
            p2[t] += 1
            rec(p2, v2, r2, h2)
    rec([0] * n, dict(init), {}, {})
    return results

def finals(results, var):
    c = Counter()
    for (vars_, regs, dead), k in results.items():
        c[dict(vars_)[var]] += k
    return c

def inc_lane(var, by=1, times=1):
    return [('load', 'r', var), ('add', 'r', by), ('store', var, 'r')] * times

# ---------------------------------------------------------------- l6, l7: races
def races():
    r = finals(enumerate_schedules([inc_lane('t', 10), inc_lane('t', 26)], {'t': 0}), 't')
    check('L2:interleave_total', r == Counter({36: 2, 10: 9, 26: 9}) and sum(r.values()) == 20, f'l6 screens[1]: {r}')
    r = finals(enumerate_schedules([inc_lane('x'), inc_lane('x')], {'x': 0}), 'x')
    check('L2:lost_update', r == Counter({1: 18, 2: 2}), f'l7 screens[0..2], quiz[0], quiz[3]: {r}')
    r = finals(enumerate_schedules([inc_lane('x')] * 3, {'x': 0}), 'x')
    check('L2:three_lanes', r == Counter({1: 1404, 2: 270, 3: 6}) and sum(r.values()) == 1680, f'l7 screens[3]: {r}')
    # check-then-act: each lane loads the balance, and if >= 80 stores balance - 80 and pays 80
    lane = [('load', 'r', 'bal'), ('act', 'r', 'bal', 80, 'paid')]   # check in one step, act in one step
    res = enumerate_schedules([lane, lane], {'bal': 100, 'paid': 0})
    paid = Counter()
    for (vars_, regs, dead), k in res.items():
        paid[(dict(vars_)['paid'], dict(vars_)['bal'])] += k
    check('L2:check_then_act', paid == Counter({(160, 20): 4, (80, 20): 2}), f'l7 screens[4]: {paid}')
    two_step = [[('load', 'r', 'f'), ('setvar', 'f', 1)]] * 2       # atomic check, atomic store
    res = enumerate_schedules(two_step, {'f': 0})
    ent = Counter()
    for (vars_, regs, dead), k in res.items():
        rd = dict(regs); ent[sum(1 for t in range(2) if rd[(t, 'r')] == 0)] += k
    check('L2:atomic_check_then_act', ent[2] == 4 and ent[1] == 2, f'l9 screens[6]: both enter in {ent[2]} of 6')
    # x = x + 1 on an atomic: an atomic load then an atomic store (the add is in a register), 6 schedules
    def ls_enum():
        out = Counter()
        def rec(pc, x, regs):
            if all(p == 2 for p in pc):
                out[x] += 1; return
            for t in range(2):
                if pc[t] == 2: continue
                if pc[t] == 0:
                    r2 = dict(regs); r2[t] = x; p2 = list(pc); p2[t] = 1; rec(p2, x, r2)
                else:
                    p2 = list(pc); p2[t] = 2; rec(p2, regs[t] + 1, regs)
        rec([0, 0], 0, {}); return out
    r = ls_enum()
    check('L2:atomic_load_store', r == Counter({1: 4, 2: 2}), f'l9 screens[7]: {r}')
    r = finals(enumerate_schedules([inc_lane('x', 1, 2), inc_lane('x', 1, 2)], {'x': 0}), 'x')
    check('L2:two_increments', r == Counter({2: 702, 3: 216, 4: 6}) and sum(r.values()) == 924
          and comb(12, 6) == 924 and factorial(6) // 8 == 90, f'l7 screens[8]: {r}')
    r = finals(enumerate_schedules([inc_lane('p', 100), inc_lane('p', -300)], {'p': 500}), 'p')
    check('L2:position', r == Counter({200: 9, 300: 2, 600: 9}), f'l7 screens[10]: {r}')
    check('L2:count70', comb(8, 4) == 70, 'l7 quiz[1]')
    # quiz[1] of l9: two threads of n plain increments can end as low as 2 (n = 3 enumerated) and as high as 2n
    r = finals(enumerate_schedules([inc_lane('x', 1, 3), inc_lane('x', 1, 3)], {'x': 0}), 'x')
    check('L2:min_two', min(r) == 2 and max(r) == 6 and sum(r.values()) == comb(18, 9), f'l9 quiz[1]: {sorted(r)}')

def review_hw_races():
    a = [('load', 'r', 'x'), ('add', 'r', 1), ('store', 'x', 'r')]
    b = [('fetch', 'x', 1), ('fetch', 'x', 1)]
    r = finals(enumerate_schedules([a, b], {'x': 0}), 'x')
    check('L2:review_mixed', r == Counter({3: 3, 2: 4, 1: 3}) and comb(5, 2) == 10, f'review-2 items[2]: {r}')
    r = finals(enumerate_schedules([inc_lane('x', 1), inc_lane('x', 2), inc_lane('x', 4)], {'x': 0}), 'x')
    check('L2:three_adds', set(r) == set(range(1, 8)) and r[7] == 6, f'review-2 items[3]: {r}')
    fill = inc_lane('p', 100, 2)
    sale = inc_lane('p', -300)
    r = finals(enumerate_schedules([fill, sale], {'p': 800}), 'p')
    check('L2:position_fills', sum(r.values()) == 84 and set(r) == {500, 600, 700, 1000} and r[700] == 3,
          f'homework-2 items[0]: {r}')
    r = finals(enumerate_schedules([[('fetch', 'p', 100), ('fetch', 'p', 100)], [('fetch', 'p', -300)]], {'p': 800}), 'p')
    check('L2:position_atomic', r == Counter({700: 3}), f'homework-2 items[0] part 3: {r}')

# ---------------------------------------------------------------- l8: locks and deadlock
def lock_lane(order, work=None):
    steps = [('lock', L) for L in order]
    steps += [('unlock', L) for L in reversed(order)]
    return steps

def count_locks(lanes):
    res = enumerate_schedules(lanes, {'x': 0, 'bal': 100})
    total = sum(res.values())
    dead = sum(k for (v, r, d), k in res.items() if d)
    return total, dead

def locks():
    inc = [('lock', 'm')] + inc_lane('x') + [('unlock', 'm')]
    res = enumerate_schedules([inc, inc], {'x': 0})
    check('L2:mutex_increment', finals(res, 'x') == Counter({2: 2}), f'l8 screens[0]: {finals(res, "x")}')
    check('L2:two_locks', count_locks([lock_lane('AB'), lock_lane('BA')]) == (6, 2), f'l8 screens[2]: {count_locks([lock_lane("AB"), lock_lane("BA")])}')
    check('L2:ring_three', count_locks([lock_lane('AB'), lock_lane('BC'), lock_lane('CA')]) == (168, 6),
          f'l8 screens[3]: {count_locks([lock_lane("AB"), lock_lane("BC"), lock_lane("CA")])}')
    self_lock = [('lock', 'm'), ('lock', 'm'), ('fetch', 'x', 1), ('unlock', 'm')]
    res = enumerate_schedules([self_lock], {'x': 0})
    check('L2:self_deadlock', all(d for (v, r, d) in res), 'l8 screens[7]: a std::mutex locked twice hangs')
    t2 = [('load', 'r', 'x')] + lock_lane('BA')
    check('L2:review_two_locks', count_locks([lock_lane('AB'), t2]) == (14, 3), f'review-2 items[5]: {count_locks([lock_lane("AB"), t2])}')
    tr1 = [('lock', 'A'), ('load', 'r', 'bal'), ('lock', 'B'), ('unlock', 'B'), ('unlock', 'A')]
    tr2 = [('lock', 'B'), ('load', 'r', 'bal'), ('lock', 'A'), ('unlock', 'A'), ('unlock', 'B')]
    check('L2:transfer_locks', count_locks([tr1, tr2]) == (12, 6), f'homework-2 items[2] part 1: {count_locks([tr1, tr2])}')
    check('L2:transfer_fixed', count_locks([tr1, tr1])[1] == 0, 'homework-2 items[2] part 2: {AB, AB} never deadlocks')
    check('L2:transfer_money', (100 - 10 + 5, 100 + 10 - 5) == (95, 105), 'l8 screens[11]')
    check('L2:lock_costs', abs(4e6 * 25e-9 - 0.1) < 1e-9 and abs(4e6 * 5e-6 - 20) < 1e-9 and abs(1e6 * 25e-9 - 0.025) < 1e-12
          and abs(2e-6 * 200_000 - 0.4) < 1e-12, 'l8 screens[5], quiz[1], quiz[3]')

def has_cycle(threads):
    edges = set()
    for s in threads:
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                edges.add((s[i], s[j]))
    nodes = {n for e in edges for n in e}
    state = {}
    def visit(n):
        state[n] = 1
        for a, b in edges:
            if a != n: continue
            if state.get(b) == 1: return True
            if state.get(b) is None and visit(b): return True
        state[n] = 2
        return False
    return any(state.get(n) is None and visit(n) for n in sorted(nodes))

def lock_cycles():
    drill = [has_cycle(t) for t in (['AB', 'BA'], ['AB', 'BC', 'AC'], ['AB', 'BC', 'CD', 'DA'], ['ABC', 'BCD', 'ACD'])]
    check('L2:lock_cycles', drill == [True, False, True, False] and not has_cycle(['AC', 'BD', 'CB'])
          and has_cycle(['ABC', 'CD', 'DA']) and not has_cycle(['ABC', 'CD', 'AD']) and has_cycle(['AA']) and not has_cycle(['AB', 'AB']),
          f'l8 screens[9], quiz[0]; review-2 items[4]: {drill}')

# ---------------------------------------------------------------- l9: litmus tests under interleaving
def litmus(lanes, init):
    res = enumerate_schedules(lanes, init)
    out = Counter()
    for (vars_, regs, dead), k in res.items():
        rd = dict(regs)
        out[(rd[(0, 'r')], rd[(1, 'r')])] += k
    return out

def litmus_tests():
    sb = litmus([[('setvar', 'x', 1), ('load', 'r', 'y')], [('setvar', 'y', 1), ('load', 'r', 'x')]], {'x': 0, 'y': 0})
    check('L2:litmus_sb', sb == Counter({(0, 1): 1, (1, 0): 1, (1, 1): 4}) and abs(4 / 6 - 0.667) < 0.001,
          f'l9 screens[1], [9]; homework-2 items[5]: {sb}')
    sb2 = litmus([[('setvar', 'x', 2), ('load', 'r', 'y')], [('setvar', 'y', 3), ('load', 'r', 'x')]], {'x': 0, 'y': 0})
    check('L2:litmus_sb_variant', sb2 == Counter({(0, 2): 1, (3, 0): 1, (3, 2): 4}), f'homework-2 items[5] part 0: {sb2}')
    # message passing: lane 1 has r1 (ready) and r2 (data)
    res = enumerate_schedules([[('setvar', 'data', 42), ('setvar', 'ready', 1)], [('load', 'r1', 'ready'), ('load', 'r2', 'data')]], {'data': 0, 'ready': 0})
    pairs = Counter()
    for (vars_, regs, dead), k in res.items():
        rd = dict(regs); pairs[(rd[(1, 'r1')], rd[(1, 'r2')])] += k
    check('L2:litmus_mp', pairs == Counter({(0, 0): 1, (0, 42): 4, (1, 42): 1}), f'l9 screens[3]: {pairs}')
    res = enumerate_schedules([[('setvar', 'ready', 1), ('setvar', 'data', 42)], [('load', 'r1', 'ready'), ('load', 'r2', 'data')]], {'data': 0, 'ready': 0})
    pairs = Counter()
    for (vars_, regs, dead), k in res.items():
        rd = dict(regs); pairs[(rd[(1, 'r1')], rd[(1, 'r2')])] += k
    check('L2:litmus_mp_flag_first', pairs[(1, 0)] == 1 and sum(pairs.values()) == 6, f'l9 screens[4]: {pairs}')
    lb = litmus([[('load', 'r', 'x'), ('setvar', 'y', 1)], [('load', 'r', 'y'), ('setvar', 'x', 1)]], {'x': 0, 'y': 0})
    check('L2:litmus_lb', (1, 1) not in lb and {(0, 0), (0, 1), (1, 0)} <= set(lb), f'review-2 items[6]: {lb}')
    check('L2:atomic_costs', abs(4e6 * 5e-9 - 0.02) < 1e-12 and abs(4e6 * 60e-9 - 0.24) < 1e-12 and abs(2e6 * 60e-9 - 0.12) < 1e-12
          and abs(8 * 5e5 * 60e-9 / (5e5 * 1e-9) - 480) < 1e-9 and abs(1e6 * 60e-9 / (2.5e5 * 1e-9) - 240) < 1e-9
          and 1e7 * 59e-9 * 1e3 == 590, 'l9 screens[5], quiz[0]; l6 screens[8]; homework-2 items[6]; review-2 items[8]')

# ---------------------------------------------------------------- l7 screens[6]: the spin loop under clang and gcc
def spin_loop():
    src = 'bool done = false;\nvoid spin() { while (!done) { } }\nvoid finish() { done = true; }\n'
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'spin.cpp')
    with open(p, 'w') as f:
        f.write(src)
    def body(cc):
        asm = subprocess.run([cc, '-std=c++17', '-O1', '-S', '-o', '-', p], capture_output=True, text=True).stdout
        lines = asm.splitlines()
        start = next(i for i, l in enumerate(lines) if l.startswith('_Z4spinv:'))
        out = []
        for l in lines[start + 1:]:
            if l.startswith('.Lfunc_end') or l.startswith('.LFE') or '.cfi_endproc' in l:
                break
            s = l.strip()
            if s and not s.startswith('.') and not s.startswith('#'):
                out.append(s.split()[0])
        return out
    if shutil.which('clang++'):
        ins = body('clang++')
        check('L2:spin_loop_clang', ins == ['retq'] or ins == ['ret'], f'l7 screens[6]: clang -O1 spin() is {ins}, not a bare ret')
    if shutil.which('g++'):
        ins = body('g++')
        loads = [i for i in ins if i.startswith('mov')]
        jumps = [i for i in ins if i.startswith('j')]
        check('L2:spin_loop_gcc', len(loads) == 1 and jumps, f'l7 screens[6]: g++ -O1 spin() is {ins}, not read-once-then-spin')

# ---------------------------------------------------------------- l10: producer and consumer
def producer_consumer():
    # lanes: consumer c1 check (empty?), c2 wait-if-empty; producer p1 push, p2 notify
    orders = []
    def rec(seq, cpc, ppc):
        if cpc == 2 and ppc == 2:
            orders.append(seq); return
        if cpc < 2: rec(seq + ['c%d' % (cpc + 1)], cpc + 1, ppc)
        if ppc < 2: rec(seq + ['p%d' % (ppc + 1)], cpc, ppc + 1)
    rec([], 0, 0)
    asleep = 0
    for o in orders:
        items, waiting, saw_empty, sleeping = 0, False, False, False
        for s in o:
            if s == 'p1': items += 1
            elif s == 'p2': waiting = False
            elif s == 'c1': saw_empty = items == 0
            elif s == 'c2':
                if saw_empty: waiting = True
        asleep += waiting
    check('L2:lost_wakeup', len(orders) == 6 and asleep == 1, f'l10 screens[0..1]; homework-2 items[3]: {asleep} of {len(orders)} asleep')
    def tallies(cap, events):
        items = bp = bc = 0
        for e in events:
            if e == 'P':
                if items == cap: bp += 1
                else: items += 1
            else:
                if items == 0: bc += 1
                else: items -= 1
        return bp, bc, items
    check('L2:bounded_queue', tallies(2, 'PCCPPP') == (1, 1, 2) and tallies(3, 'PPPCCCC') == (0, 1, 0) and tallies(2, 'PPPPCC')[0] == 2
          and tallies(1, 'PPCCPC')[1:] == (1, 0) and tallies(3, 'PPPPC')[0] == 1, 'l10 screens[4], [8], quiz[3]')
    rng = random.Random(3)
    waits = [1.0 - rng.random() for _ in range(200_000)]      # arrival uniform in a 1 ms sleep: wait until the next check
    mean = sum(waits) / len(waits)
    check('L2:poll_delay', abs(mean - 0.5) < 0.005 and max(waits) <= 1.0, f'l10 screens[5], quiz[1]: mean wait {mean:.3f} ms')
    check('L2:spin_costs', 5 / 0.1 == 50 and 1 / 8 == 0.125 and 200_000 * 5e-6 == 1.0, 'l10 screens[8], [9]')

def code_items():
    code_item('L2:code_final_counts', load('l7-data-races')['screens'][9]['widget'])
    code_item('L2:code_lock_cycle', load('l8-locks-and-deadlock')['screens'][10]['widget'])
    code_item('L2:code_blocked_counts', load('homework-2')['items'][1]['widget'])

if __name__ == '__main__':
    assert CXX, 'no C++ compiler found'
    races()
    review_hw_races()
    locks()
    lock_cycles()
    litmus_tests()
    spin_loop()
    producer_consumer()
    code_items()
    print(f'systems L2 concepts: {len(PASSED)} checks passed')
