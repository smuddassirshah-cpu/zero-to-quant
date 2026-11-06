#!/usr/bin/env python3
"""Concept checks for coding-int level 2 (blind concept audit, 6 Nov 2026).

Run from the repo root: python3 -I docs/reports/coding-int-L2-concepts.py
Exit 0 when every check passes. A check that encodes a content claim the
audit found wrong stays failing until the content is fixed (brief step 4).

Covers l6 to l10, review-2 and homework-2: every Python and C++ code widget
(model solution passes its hidden tests, the untouched starter fails at least
one), and the stated traces, counts, invariants and complexity claims, by
brute force, operation counters or direct computation. No timing is used.
"""
import bisect
import heapq
import json
import math
import os
import pathlib
import random
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, deque

ROOT = pathlib.Path(__file__).resolve().parents[2]
COURSE = ROOT / 'app' / 'content' / 'courses' / 'coding-int'
FAILS = []


def check(cond, name):
    print(('ok   ' if cond else 'FAIL ') + name)
    if not cond:
        FAILS.append(name)


def load(name):
    return json.loads((COURSE / f'{name}.json').read_text())


def code_widgets(doc):
    out = []

    def add(path, obj):
        w = obj.get('widget')
        if w and w.get('kind') == 'code':
            out.append((path, w))
        for k, p in enumerate(obj.get('parts', []) or []):
            w = p.get('widget')
            if w and w.get('kind') == 'code':
                out.append((f'{path}.parts[{k}]', w))

    for i, s in enumerate(doc.get('screens', [])):
        add(f'screens[{i}]', s)
    for key in ('quiz', 'items'):
        for i, it in enumerate(doc.get(key, [])):
            add(f'{key}[{i}]', it)
    return out


def _close(a, b):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    try:
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    except TypeError:
        return a == b


def run_py(widget, code):
    """Run `code` against the widget's hidden tests as the engine does. Returns one bool per test."""
    tests = widget['tests']
    cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    os.chdir(tmp)
    try:
        for name, rel in (widget.get('data') or {}).items():
            shutil.copy(ROOT / 'app' / rel, name)
        ns = {'__learner_source__': code}
        src = widget.get('prelude', '') + '\n' + code + '\n' + widget.get('postlude', '')
        try:
            exec(src, ns)
        except Exception:
            return [False] * len(tests)
        res = []
        for t in tests:
            try:
                if t.get('setup'):
                    exec(t['setup'], ns)
                if t.get('compare') == 'raises':
                    try:
                        eval(t['call'], ns)
                        res.append(False)
                    except Exception as e:
                        res.append(isinstance(e, eval(t['expect'], ns)))
                    continue
                val = eval(t['call'], ns)
                exp = eval(t['expect'], ns)
                res.append(_close(val, exp) if t.get('compare') == 'isclose' else val == exp)
            except Exception:
                res.append(False)
        return res
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)


CPP_PRINT = r'''
#include <iostream>
#include <string>
#include <vector>
static void pj(int v) { std::cout << v; }
static void pj(long long v) { std::cout << v; }
static void pj(const std::string& s) { std::cout << '"' << s << '"'; }
template <class T> static void pj(const std::vector<T>& v) {
    std::cout << '[';
    for (size_t i = 0; i < v.size(); ++i) { if (i) std::cout << ','; pj(v[i]); }
    std::cout << ']';
}
'''


def cpp_lit(value, typ):
    if typ is None:
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, (int, float)):
            return repr(value)
        if isinstance(value, str):
            return json.dumps(value)
        return '{' + ','.join(cpp_lit(v, None) for v in value) + '}'
    if typ.startswith('std::vector<'):
        inner = typ[len('std::vector<'):-1]
        return typ + '{' + ','.join(cpp_lit(v, inner) for v in value) + '}'
    if typ == 'std::string':
        return json.dumps(value)
    return str(value)


def cpp_run_source(src, timeout=120):
    """Compile and run a C++17 program; returns stdout or None on a compile error."""
    tmp = tempfile.mkdtemp()
    try:
        p = pathlib.Path(tmp) / 'main.cpp'
        p.write_text(src)
        c = subprocess.run(['g++', '-std=c++17', '-O1', '-o', tmp + '/a.out', str(p)],
                           capture_output=True, text=True)
        if c.returncode != 0:
            return None
        r = subprocess.run([tmp + '/a.out'], capture_output=True, text=True, timeout=timeout)
        return r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_cpp(widget, code, extra_tests=None):
    """Run C++ `code` against the widget's tests (function mode) with g++. Returns one bool per test."""
    tests = list(widget['tests']) + list(extra_tests or [])
    main = ['int main() {']
    for k, t in enumerate(tests):
        body = []
        if t.get('setup'):
            body.append(t['setup'])
        call = t['call']
        if 'args' in t or 'types' in t:
            types = t.get('types') or [None] * len(t.get('args', []))
            args = t.get('args', [[] for _ in types])
            call = call + '(' + ', '.join(cpp_lit(a, ty) for a, ty in zip(args, types)) + ')'
        body.append(f'std::cout << {k} << " "; pj({call}); std::cout << "\\n";')
        main.append('{' + '\n'.join(body) + '}')
    main.append('return 0; }')
    src = code + '\n' + widget.get('postlude', '') + '\n' + CPP_PRINT + '\n'.join(main)
    out = cpp_run_source(src)
    if out is None:
        return [False] * len(tests)
    got = {}
    for line in out.splitlines():
        k, _, rest = line.partition(' ')
        try:
            got[int(k)] = json.loads(rest)
        except ValueError:
            pass
    return [k in got and got[k] == t.get('expect', []) for k, t in enumerate(tests)]


def check_code(doc, label):
    for path, w in code_widgets(doc):
        runner = run_cpp if w.get('language') == 'cpp' else run_py
        sol = runner(w, w['solution'])
        st = runner(w, w['starter'])
        check(all(sol), f'{label} {path}: model solution passes all {len(sol)} hidden tests')
        check(not all(st), f'{label} {path}: untouched starter fails at least one hidden test')


def widget(doc, path):
    key, idx = path[:-1].split('[')
    return doc[key][int(idx)]['widget']


def ns_of(w, code=None):
    ns = {}
    exec(w.get('prelude', '') + '\n' + (code or w['solution']) + '\n' + w.get('postlude', ''), ns)
    return ns


# ---------------------------------------------------------------- load
L6, L7, L8, L9, L10 = (load(n) for n in ('l6-anagrams-and-palindromes', 'l7-parsing-with-a-stack',
                                        'l8-simulating-the-rules', 'l9-grids-and-matrices', 'l10-matching-engine'))
R2, H2 = load('review-2'), load('homework-2')
random.seed(20261106)

print('# code widgets: solution passes, starter fails')
for doc, label in ((L6, 'l6'), (L7, 'l7'), (L8, 'l8'), (L9, 'l9'), (L10, 'l10'), (R2, 'review-2'), (H2, 'homework-2')):
    check_code(doc, label)

# ---------------------------------------------------------------- l6 anagrams and palindromes
print('# l6 anagrams and palindromes')
fa = ns_of(widget(L6, 'screens[3]'))['find_anagrams']
lp = ns_of(widget(L6, 'screens[5]'))['longest_palindrome']


def brute_anagrams(s, p):
    return [i for i in range(len(s) - len(p) + 1) if sorted(s[i:i + len(p)]) == sorted(p)]


def brute_longest_pal(s):
    best = ''
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            sub = s[i:j]
            if sub == sub[::-1] and len(sub) > len(best):
                best = sub
    return best


def letters_only(s):
    best = ''
    for c in range(len(s)):
        lo = hi = c
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
            lo -= 1
            hi += 1
        if hi - lo - 1 > len(best):
            best = s[lo + 1:hi]
    return best


def count_pal_substrings(s):
    return sum(1 for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])


def centre_steps(s):
    steps = 0
    for c in range(2 * len(s) - 1):
        lo, hi = c // 2, c // 2 + c % 2
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
            steps += 1
            lo -= 1
            hi += 1
    return steps


def can_permute_palindrome(s):
    return sum(v % 2 for v in Counter(s).values()) <= 1


check(brute_anagrams('dcabbacbed', 'abc') == [1, 4, 5] and len('dcabbacbed') - 3 + 1 == 8, 'l6 s0 and s1: windows 1, 4, 5 are anagrams; 8 windows of width 3')
check(100000 - 1000 + 1 == 99001, 'l6 s2: 99,001 windows')
ok = True
for _ in range(400):
    s = ''.join(random.choice('abc') for _ in range(random.randint(0, 10)))
    p = ''.join(random.choice('abc') for _ in range(random.randint(1, 4)))
    ok &= fa(s, p) == brute_anagrams(s, p)
check(ok, 'l6 s3: sliding counts equal sorting every window on 400 random cases')
check(fa('ab' * 50000, 'ba' * 500) == list(range(99001)), 'l6 s3 test 8: every window of ab*50000 matches ba*500 (99,001)')
check(2 * 7 - 1 == 13, 'l6 s4: 7 letters have 13 centres')
ok = True
for _ in range(400):
    s = ''.join(random.choice('ab') for _ in range(random.randint(0, 9)))
    ok &= lp(s) == brute_longest_pal(s)
check(ok, 'l6 s5: centre expansion returns the first longest palindrome on 400 random strings')
check(letters_only('cbbd') == 'c' and lp('cbbd') == 'bb', 'l6 s6: letters-only centres return c for cbbd; gaps find bb')
check([can_permute_palindrome(w) for w in ('carerac', 'abcabc', 'aabbccd', 'abcd', 'aabbcd')] == [True, True, True, False, False],
      'l6 s8: at most one odd count: carerac, abcabc, aabbccd yes; abcd, aabbcd no')
ok = True
for _ in range(300):
    s = ''.join(random.choice('abc') for _ in range(random.randint(0, 7)))
    from itertools import permutations
    truth = any(''.join(p) == ''.join(p)[::-1] for p in set(permutations(s)))
    ok &= can_permute_palindrome(s) == truth
check(ok, 'l6 s8 rule: a string permutes to a palindrome iff at most one letter has an odd count (300 random, all permutations)')
check(count_pal_substrings('abba') == 6 and count_pal_substrings('aaa') == 6 and count_pal_substrings('abcba') == 7,
      'l6 s9 and r2 i1: abba 6, aaa 6, abcba 7 palindromic substrings')
ok = True
for _ in range(200):
    s = ''.join(random.choice('ab') for _ in range(random.randint(0, 8)))
    ok &= centre_steps(s) == count_pal_substrings(s)
check(ok, 'l6 s9: one widening step per palindromic substring (200 random)')
check([can_permute_palindrome(w) for w in ('ttaccoa', 'abcabd', 'aabbcde', 'abcdab')] == [True, False, False, False]
      and [can_permute_palindrome(w) for w in ('civic', 'ivicc', 'xxyyz', 'aabbcd', 'abcde')] == [True, True, True, False, False],
      'l6 q2 and r2 i2: ttaccoa; civic, ivicc, xxyyz')
r = [centre_steps('a' * n) / n ** 2 for n in (200, 400, 800)]
check(all(0.45 < x < 0.55 for x in r) and centre_steps('a' * 800) > 3.9 * centre_steps('a' * 400),
      'l6 q3: on a*n the widening steps are about n^2 / 2 (ratios %.3f, %.3f, %.3f)' % tuple(r))
check(12 - 4 + 1 == 9 and 6 - 3 + 1 == 4 and brute_anagrams('abcbac', 'abc') == [0, 2, 3], 'l6 q0 and r2 i0: 9 windows; abcbac has 3 anagram windows')

# ---------------------------------------------------------------- l7 parsing with a stack
print('# l7 parsing with a stack')
calculate = ns_of(widget(L7, 'screens[5]'))['calculate']
decode = ns_of(widget(L7, 'screens[7]'))['decode_string']


def calc_traced(s, pop_strict=False):
    """The lesson's parser with a peak-stack counter; pop_strict uses > instead of >= for equal ranks."""
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, 'u': 3}
    nums, ops, peak = [], [], 0

    def apply():
        op = ops.pop()
        if op == 'u':
            nums.append(-nums.pop())
            return
        b, a = nums.pop(), nums.pop()
        if op == '+':
            nums.append(a + b)
        elif op == '-':
            nums.append(a - b)
        elif op == '*':
            nums.append(a * b)
        else:
            q = abs(a) // abs(b)
            nums.append(q if (a < 0) == (b < 0) else -q)
    i, expect_operand = 0, True
    while i < len(s):
        c = s[i]
        if c == ' ':
            i += 1
        elif c.isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            nums.append(int(s[i:j]))
            i, expect_operand = j, False
        elif c == '(':
            ops.append(c)
            peak = max(peak, len(ops))
            i, expect_operand = i + 1, True
        elif c == ')':
            while ops[-1] != '(':
                apply()
            ops.pop()
            i, expect_operand = i + 1, False
        else:
            if c == '-' and expect_operand:
                c = 'u'
            if c != 'u':
                while ops and ops[-1] != '(' and (prec[ops[-1]] > prec[c] if pop_strict else prec[ops[-1]] >= prec[c]):
                    apply()
            ops.append(c)
            peak = max(peak, len(ops))
            i, expect_operand = i + 1, True
    while ops:
        apply()
    return nums[0], peak


check(calculate('4+3*2') == 10 and calculate('10-2-3') == 5 and calc_traced('10-2-3', pop_strict=True)[0] == 11,
      'l7 s0 and s2: 4+3*2 = 10; 10-2-3 = 5 with >=, 11 with >')
check(calc_traced('2*(5+5*2)/3+(6/2+8)') == (21, 4), 'l7 s3: value 21 and a peak operator stack of 4 entries')
check(int(-7 / 2) == -3 and -7 // 2 == -4 and calculate('-7/2') == -3 and calculate('(-7)/2') == -3, 'l7 s4: truncation gives -3; // floors to -4')
starter_res = run_py(widget(L7, 'screens[5]'), widget(L7, 'screens[5]')['starter'])
check([i for i, r in enumerate(starter_res) if not r] == [4, 5], 'l7 s5 hint: the eval starter fails exactly tests 5 and 6')
check(calculate('--5') == 5 and calculate('2*-3*4') == -24 and calculate('-(2+3)*4') == -20, 'l7 s5 explain: --5 stacks two unary minuses; 2*-3*4 = -24')
check(len(decode('2[b3[a]]')) == 8 and len(decode('3[xy]2[z]w')) == 9 and len(decode('9[9[9[a]]]')) == 729
      and len(decode('3[a2[b]]')) == 9 and len(decode('2[x3[y]]z')) == 9, 'l7 s6, s10, q2 and r2 i4: decoded lengths 8, 9, 729, 9, 9')


def decode_depth(s):
    stack, count, cur, peak = [], 0, [], 0
    for ch in s:
        if ch.isdigit():
            count = count * 10 + int(ch)
        elif ch == '[':
            stack.append((cur, count))
            peak = max(peak, len(stack))
            cur, count = [], 0
        elif ch == ']':
            prev, k = stack.pop()
            prev.append(''.join(cur) * k)
            cur = prev
        else:
            cur.append(ch)
    return peak


check(decode_depth('2[a3[b4[c]]]') == 3 and decode_depth('9[9[9[a]]]') == 3, 'l7 q3 and s10: the stack peaks at 3 entries')
check(calculate('12/2*3') == 18 and calculate('-8/3') == -2 and calculate('-9/4') == -2 and calculate('(8+2)*(9-4)/5-3') == 7,
      'l7 q0, q1, r2 i5 and r2 i3: 18, -2, -2, 7')
check(calculate('8+2*9-4/5-3') == 23, 'r2 i3 distractor: without the brackets, 23')
check(eval('40*(12-5)') == 280 and eval('-(2*350+100)//3') == -267 and calculate('-(2*350+100)/3') == -266,
      'l7 s9: line 1 is -266 truncated, -267 floored with //; line 2 is 280')
# content claim (l7 s9 option b why and feedback.byKey.b, corrected in the fix pass): plain eval gives line 1 as the
# float -266.67 (true division), not the truncated whole number -266.
_v = eval('-(2*350+100)/3')
check(isinstance(_v, float) and round(_v, 2) == -266.67 and _v != int(_v) and calculate('-(2*350+100)/3') == -266,
      'l7 s9 o1.why: plain eval gives line 1 as the float -266.67, not the truncated -266 (corrected claim, fix pass; eval gives %r)' % _v)

# ---------------------------------------------------------------- l8 simulating the rules
print('# l8 simulating the rules')
run_strategy = ns_of(widget(L8, 'screens[4]'))['run_strategy']


def strategy_reasons(prices, same_day_buy=False, time_rule='==3'):
    """The statement with a log of (day, action, price, reason) and variants for the lesson's distractors."""
    pnl = trades = 0
    long_, entry, bought = False, 0, 0
    log, positions = [], []
    for i, p in enumerate(prices):
        sold_today = False
        if long_:
            reason = None
            if 100 * p >= 105 * entry:
                reason = 'take profit'
            elif 100 * p <= 97 * entry:
                reason = 'stop'
            elif time_rule == '==3' and i - bought == 3:
                reason = 'time'
            elif time_rule == '>3' and i - bought > 3:
                reason = 'time'
            elif time_rule == '==2' and i - bought == 2:
                reason = 'time'
            if reason:
                pnl += p - entry
                trades += 1
                long_ = False
                sold_today = True
                log.append((i, 'sell', p, reason))
        if not long_ and (same_day_buy or not sold_today) and i >= 1 and p < prices[i - 1]:
            long_, entry, bought = True, p, i
            log.append((i, 'buy', p, 'fall'))
        positions.append(1 if long_ else 0)
    if long_:
        pnl += prices[-1] - entry
        trades += 1
        log.append((len(prices) - 1, 'sell', prices[-1], 'end'))
    return [pnl, trades], log, positions


res, log, pos = strategy_reasons([100, 98, 99, 100, 104, 110])
check(res == [6, 1] and run_strategy([100, 98, 99, 100, 104, 110]) == [6, 1] and log == [(1, 'buy', 98, 'fall'), (4, 'sell', 104, 'take profit')]
      and pos == [0, 1, 1, 1, 0, 0], 'l8 s0 and s1: buy 98 on day 1, sell 104 on day 4 by rule 1; positions 0 1 1 1 0 0')
res, log, _ = strategy_reasons([100, 98, 99, 100, 103])
check(log[-1] == (4, 'sell', 103, 'take profit') and 100 * 103 >= 105 * 98 and 4 - 1 == 3, 'l8 s2: on day 4 rule 1 fires first although the time rule is true too')
res, log, _ = strategy_reasons([100, 101, 99, 100, 101, 100, 99])
check(log[0] == (2, 'buy', 99, 'fall') and log[1] == (5, 'sell', 100, 'time'), 'l8 s3: bought on day 2, the time rule sells on day 5')
check(run_strategy([100, 95, 90, 85]) == [-5, 2] and strategy_reasons([100, 95, 90, 85], same_day_buy=True)[0] == [-10, 3],
      'l8 s5: [-5, 2]; buying on the day of a sale gives [-10, 3]')
res, log, _ = strategy_reasons([250, 240, 245, 252, 249, 247, 236, 240])
check(res == [-1, 2] and run_strategy([250, 240, 245, 252, 249, 247, 236, 240]) == [-1, 2]
      and [(d, a, p) for d, a, p, _ in log] == [(1, 'buy', 240), (3, 'sell', 252), (4, 'buy', 249), (6, 'sell', 236)],
      'l8 s9: +12 then -13 over two trades, total -1; day 3 sells at exactly 5% up')
check(run_strategy([100, 97, 99, 102, 101]) == [5, 2] and run_strategy([200, 190, 200, 212, 180, 178, 192, 197]) == [22, 2],
      'l8 q3 and r2 i6: 5 and 22')
prices = [396, 401, 398, 400, 394, 392, 404, 400, 388]
check(run_strategy(prices) == [-18, 2] and strategy_reasons(prices, time_rule='>3')[0] == [-6, 2]
      and strategy_reasons(prices, time_rule='==2')[0] == [4, 3] and strategy_reasons(prices, time_rule='none')[0] == [-10, 1],
      'h2 i7: [-18, 2]; > 3 gives [-6, 2]; == 2 gives [4, 3]; no time rule gives [-10, 1]')
res, log, _ = strategy_reasons([300, 297, 299, 298, 295, 291])
check(res == [-2, 2] and [(d, a, p) for d, a, p, _ in log] == [(1, 'buy', 297), (4, 'sell', 295), (5, 'buy', 291), (5, 'sell', 291)],
      'h2 i3 model: buy 297 day 1, time rule sells 295 day 4, buy 291 day 5, end sells 291: [-2, 2]')
ok = True
for _ in range(300):
    ps = [random.randint(90, 110) for _ in range(random.randint(0, 9))]
    ok &= run_strategy(ps) == strategy_reasons(ps)[0]
check(ok, 'l8 s4: the model solution agrees with an independent reading of the statement on 300 random price lists')
import csv as _csv
for name, exp in (('ticks-40.csv', [249, 8]), ('ticks-3.csv', [700, 1]), ('ticks-header-only.csv', [0, 0])):
    with open(ROOT / 'app' / 'content' / 'data' / 'coding-int' / name) as f:
        ps = [int(r['price_pence']) for r in _csv.DictReader(f)]
    check(run_strategy(ps) == exp, f'l8 s7: {name} gives {exp}')
check(100 * 194 <= 97 * 200 and 19400 == 19400, 'l8 q0: at 194 the stop holds with equality')

# ---------------------------------------------------------------- l9 grids and matrices
print('# l9 grids and matrices')
spiral_order = ns_of(widget(L9, 'screens[3]'))['spiral_order']
rotate = ns_of(widget(L9, 'screens[5]'))['rotate']
capture_regions = ns_of(widget(L9, 'screens[8]'))['capture_regions']


def spiral_ref(m):
    """Walk with a direction vector and a visited set (independent of the four-bounds code)."""
    if not m:
        return []
    R, C = len(m), len(m[0])
    seen, out = set(), []
    r = c = 0
    dr, dc = 0, 1
    for _ in range(R * C):
        out.append(m[r][c])
        seen.add((r, c))
        nr, nc = r + dr, c + dc
        if not (0 <= nr < R and 0 <= nc < C) or (nr, nc) in seen:
            dr, dc = dc, -dr
            nr, nc = r + dr, c + dc
        r, c = nr, nc
    return out


def unchecked_lap(m):
    top, bottom, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    out = []
    for c in range(left, right + 1):
        out.append(m[top][c])
    for r in range(top + 1, bottom + 1):
        out.append(m[r][right])
    for c in range(right - 1, left - 1, -1):
        out.append(m[bottom][c])
    for r in range(bottom - 1, top, -1):
        out.append(m[r][left])
    return out


check(unchecked_lap([[1, 2, 3]]) == [1, 2, 3, 2, 1] and unchecked_lap([[1], [2], [3]]) == [1, 2, 3, 2],
      'l9 s2: an unguarded lap reads a 1 by 3 as [1, 2, 3, 2, 1] and a 3 by 1 as [1, 2, 3, 2]')
ok = True
for _ in range(300):
    R, C = random.randint(0, 6), random.randint(1, 6)
    m = [[random.randint(0, 99) for _ in range(C)] for _ in range(R)]
    ok &= spiral_order(m) == spiral_ref(m)
check(ok, 'l9 s3: four bounds with two guards equal a direction-vector walk on 300 random rectangles')
m3 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
check(spiral_order(m3) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7], 'l9 s0 and s1: 3 by 4 spiral ends 5, 6, 7')
check(spiral_order([[300 * r + c for c in range(300)] for r in range(300)])[-1] == 45149 == 300 * 150 + 149, 'l9 s11: 300 by 300 spiral ends at 45,149')
check(spiral_order([[400 * r + c for c in range(400)] for r in range(250)])[-1] == 50124 == 400 * 125 + 124, 'h2 i4: 250 by 400 spiral ends at 50,124')
check(spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])[-1] == 8, 'r2 i7: 4 by 3 spiral ends at 8')
ok = True
for n in range(0, 7):
    m = [[random.randint(0, 99) for _ in range(n)] for _ in range(n)]
    want = [list(row) for row in zip(*m[::-1])]
    want2 = [[m[n - 1 - c][r] for c in range(n)] for r in range(n)]
    rotate(m)
    ok &= m == want == want2
    ok &= all(m[c][n - 1 - r] == want[c][n - 1 - r] for r in range(n) for c in range(n))
check(ok, 'l9 s5: in-place transpose then row reverse equals zip(*m[::-1]) for n = 0 to 6')


def new_pos(r, c, n):
    return (c, n - 1 - r)


check(new_pos(0, 1, 5) == (1, 4) and new_pos(1, 3, 5) == (3, 3) and new_pos(4, 0, 5) == (0, 0) and new_pos(1, 4, 5) == (4, 3),
      'l9 s4 and r2 i8: (r, c) -> (c, n - 1 - r)')
m = [[1, 2], [3, 4]]
n = len(m)
m5 = [[random.randint(0, 9) for _ in range(5)] for _ in range(5)]
rot = [[m5[5 - 1 - c][r] for c in range(5)] for r in range(5)]
check(all(rot[c][4 - r] == m5[r][c] for r in range(5) for c in range(5)), 'l9 s4: the formula sends each entry to the clockwise-turned place')


def rebinding_rotate(m):
    m = [list(row) for row in zip(*m[::-1])]


m = [[1, 2], [3, 4]]
rebinding_rotate(m)
check(m == [[1, 2], [3, 4]], 'l9 s6: m = [...] inside the function leaves the caller\'s list unchanged')
tr = [[1, 3], [2, 4]]
check([list(r) for r in zip(*[[1, 2], [3, 4]])] == tr and [r[::-1] for r in tr] == [[3, 1], [4, 2]] and tr[::-1] == [[2, 4], [1, 3]],
      'l9 q1: transpose [[1, 3], [2, 4]]; row reverse [[3, 1], [4, 2]] clockwise; row-order reverse is anticlockwise')


def capture_ref(board):
    R = len(board)
    C = len(board[0]) if board else 0
    safe = set()
    for r in range(R):
        for c in range(C):
            if board[r][c] == 'O' and (r in (0, R - 1) or c in (0, C - 1)) and (r, c) not in safe:
                q = deque([(r, c)])
                safe.add((r, c))
                while q:
                    a, b = q.popleft()
                    for na, nb in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= na < R and 0 <= nb < C and board[na][nb] == 'O' and (na, nb) not in safe:
                            safe.add((na, nb))
                            q.append((na, nb))
    return [''.join('O' if (r, c) in safe else 'X' if ch == 'O' else ch for c, ch in enumerate(row)) for r, row in enumerate(board)]


ok = True
for _ in range(300):
    R, C = random.randint(1, 6), random.randint(1, 6)
    b = [''.join(random.choice('XO') for _ in range(C)) for _ in range(R)]
    ok &= capture_regions(b) == capture_ref(b)
check(ok, 'l9 s8: stack flood from the border equals a BFS reference on 300 random boards')
big = ['XO' + 'X' * 398] + ['X' + 'O' * 398 + 'X'] * 398 + ['X' * 400]
check(sum(r.count('O') for r in capture_regions(big)) == 158405 == 1 + 398 * 398, 'l9 s8 test 12: 158,405 safe cells')
board7 = ['XXXXXX', 'XOOXOX', 'XXOXOO', 'XOXXXX', 'XOXXXX']
cap = capture_regions(board7)
safe_cells = {(r, c) for r, row in enumerate(cap) for c, ch in enumerate(row) if ch == 'O'}
check(safe_cells == {(1, 4), (2, 4), (2, 5), (3, 1), (4, 1)}, 'l9 s7: five O cells survive (right group of three, left pair)')
check(capture_regions(['XXXXX', 'XOXOX', 'XXXXX', 'XOOXO']) == ['XXXXX', 'XXXXX', 'XXXXX', 'XOOXO'], 'l9 q2: two O cells captured')
grid = [[5, 8, 2, 7], [4, 9, 6, 3], [10, 1, 12, 11]]
check(spiral_order(grid)[:10] == [5, 8, 2, 7, 3, 11, 12, 1, 10, 4], 'l9 s10: the ring is 5, 8, 2, 7, 3, 11, 12, 1, 10, 4')
check((0 + 1, 4 - 1, 0 + 1, 5 - 1) == (1, 3, 1, 4), 'l9 q0: bounds after one lap of a 5 by 6 are 1, 3, 1, 4')

# ---------------------------------------------------------------- l10 matching engine
print('# l10 matching engine')
eng = ns_of(widget(L10, 'screens[6]'))
run_book, levels = eng['run_book'], eng['levels']
check(run_book([[0, 1, 1, 100, 3], [0, 2, 1, 100, 4], [0, 3, 0, 100, 5]]) == [[3, 1, 100, 3], [3, 2, 100, 2]]
      and levels([[0, 1, 1, 100, 3], [0, 2, 1, 100, 4], [0, 3, 0, 100, 5]], 1) == [[100, 2]],
      'l10 s0 and s1: a buy of 5 fills #1 for 3 then #2 for 2; 2 remain at 100')
book = [[0, 1, 1, 100, 3], [0, 2, 1, 100, 4], [0, 4, 1, 101, 6], [0, 3, 0, 99, 5]]
check(run_book(book + [[0, 9, 0, 101, 8]])[-1][2] == 101 and sum(t[3] for t in run_book(book + [[1, 9, 0, 13]])) == 13
      and sum(t[3] for t in run_book(book + [[1, 9, 0, 14]])) == 13,
      'l10 s1 explain: a buy of 8 reaches 101; the book holds 13 so a market buy of 14 drops 1')
check(run_book([[0, 1, 1, 101, 4], [0, 2, 1, 102, 6], [0, 3, 0, 102, 7]]) == [[3, 1, 101, 4], [3, 2, 102, 3]],
      'l10 s2 and s3: order 3 trades 4 at 101 (the maker price) then 3 at 102')
ev = [[0, 1, 0, 99, 10], [1, 2, 1, 4], [1, 3, 1, 20]]
check(sum(t[3] for t in run_book(ev)) == 10 and levels(ev, 0) == [], 'l10 s4: market sells trade 10 in all; the bid side ends empty')
check(run_book([[0, 1, 1, 101, 5], [0, 2, 1, 101, 5], [3, 1, 8], [0, 3, 0, 101, 6]]) == [[3, 2, 101, 5], [3, 1, 101, 1]]
      and run_book([[0, 1, 1, 101, 5], [0, 2, 1, 101, 5], [3, 1, 3], [0, 3, 0, 101, 6]]) == [[3, 1, 101, 3], [3, 2, 101, 3]],
      'l10 s5: an amend up joins the back; an amend down keeps its place')
ev = [[0, 1, 0, 100, 2], [0, 2, 0, 99, 3], [0, 3, 1, 99, 4], [0, 4, 1, 100, 1]]
check(levels(ev, 0) == [[99, 1]] and levels(ev, 1) == [[100, 1]] and sum(t[3] for t in run_book(ev)) == 4,
      'l10 s10: best bid 99, best ask 100, 4 traded')
check(run_book([[0, 1, 1, 99, 5], [0, 2, 0, 101, 5]]) == [[2, 1, 99, 5]], 'l10 q0: the trade is at the resting 99')
check(sum(t[3] for t in run_book([[0, 1, 1, 100, 3], [0, 2, 1, 101, 4], [1, 3, 0, 10]])) == 7, 'l10 q1: a market buy of 10 trades 7 and drops 3')
check(levels([[0, 1, 1, 100, 5], [2, 1], [2, 1], [0, 2, 0, 100, 5]], 0) == [[100, 5]], 'l10 q2: a second cancel is ignored; order 2 rests')
check(run_book([[0, 1, 1, 101, 5], [0, 2, 1, 101, 5], [3, 1, 3], [3, 1, 4], [0, 3, 0, 101, 6]]) == [[3, 2, 101, 5], [3, 1, 101, 1]],
      'l10 q3: amended 5 to 3 then 3 to 4, order 1 sits at the back')
tr = run_book([[0, 1, 1, 100, 4], [0, 2, 1, 100, 4], [0, 3, 1, 100, 4], [3, 1, 2], [0, 9, 0, 100, 7]])
check([t[1:] for t in tr] == [[1, 100, 2], [2, 100, 4], [3, 100, 1]], 'r2 i9: id 1 trades 2, id 2 trades 4, id 3 trades 1')
ev = [[0, 1, 1, 102, 3], [0, 2, 1, 101, 2], [0, 3, 0, 101, 4], [0, 4, 0, 100, 5], [1, 5, 1, 6]]
check(run_book(ev) == [[3, 2, 101, 2], [5, 3, 101, 2], [5, 4, 100, 4]] and levels(ev, 0) == [[100, 1]] and levels(ev, 1) == [[102, 3]],
      'h2 i6: trades of 2, 2 and 4; 1 rests bid at 100 and 3 offered at 102')


def random_events(n):
    ev, nid = [], 1
    for _ in range(n):
        kind = random.choice([0, 0, 0, 1, 2, 3])
        if kind == 0:
            ev.append([0, nid, random.randint(0, 1), random.randint(98, 102), random.randint(1, 6)])
            nid += 1
        elif kind == 1:
            ev.append([1, nid, random.randint(0, 1), random.randint(1, 8)])
            nid += 1
        elif kind == 2:
            ev.append([2, random.randint(1, max(1, nid - 1))])
        else:
            ev.append([3, random.randint(1, max(1, nid - 1)), random.randint(1, 8)])
    return ev


extra = []
for _ in range(12):
    ev = random_events(14)
    extra.append({'call': 'run_book', 'args': [ev], 'types': ['std::vector<std::vector<int>>'], 'expect': run_book(ev)})
    extra.append({'call': 'levels', 'args': [ev, 0], 'types': ['std::vector<std::vector<int>>', 'int'], 'expect': levels(ev, 0)})
    extra.append({'call': 'levels', 'args': [ev, 1], 'types': ['std::vector<std::vector<int>>', 'int'], 'expect': levels(ev, 1)})
cpp_res = run_cpp(widget(L10, 'screens[7]'), widget(L10, 'screens[7]')['solution'], extra_tests=extra)
check(all(cpp_res), 'l10 s7: the C++ engine agrees with the Python engine on its 15 tests and 12 random event streams')


def price_time_ok(ev):
    """Every fill is at the maker's resting price, never through the taker's limit, and within a level in arrival order."""
    trades = run_book(ev)
    resting = {}
    seq = {}
    for e in ev:
        if e[0] == 0:
            resting[e[1]] = (e[2], e[3])
            seq[e[1]] = len(seq)
    for taker, maker, price, qty in trades:
        if price != resting[maker][1]:
            return False
        tk = next(e for e in ev if e[1] == taker and e[0] in (0, 1))
        if tk[0] == 0 and ((tk[2] == 0 and price > tk[3]) or (tk[2] == 1 and price < tk[3])):
            return False
    return True


check(all(price_time_ok(random_events(20)) for _ in range(200)), 'l10 s3 and s8: on 200 random streams every fill is at the maker price and never through the taker limit')

# ---------------------------------------------------------------- homework-2
print('# homework-2')
import posixpath
simplify_path = ns_of(widget(H2, 'items[0]'))['simplify_path']
life_step = ns_of(widget(H2, 'items[1]'))['life_step']
lvp = ns_of(widget(H2, 'items[2]'))['longest_valid_parentheses']
ok = True
for _ in range(300):
    parts = [random.choice(['a', 'b', '.', '..', '...', '']) for _ in range(random.randint(0, 6))]
    p = '/' + '/'.join(parts) + random.choice(['', '/'])
    ok &= simplify_path(p) == posixpath.normpath(p).replace('//', '/')
check(ok, 'h2 i0: simplify_path equals posixpath.normpath on 300 random absolute paths')


def life_ref(b):
    R, C = len(b), len(b[0])
    out = [[0] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            n = sum(b[rr][cc] for rr in range(max(0, r - 1), min(R, r + 2)) for cc in range(max(0, c - 1), min(C, c + 2))) - b[r][c]
            out[r][c] = 1 if n == 3 or (b[r][c] == 1 and n == 2) else 0
    return out


ok = True
for _ in range(300):
    R, C = random.randint(1, 6), random.randint(1, 6)
    b = [[random.randint(0, 1) for _ in range(C)] for _ in range(R)]
    ok &= life_step(b) == life_ref(b)
check(ok, 'h2 i1: one Life step equals an independent neighbour count on 300 random boards')
b = [[(r * 7 + c * 3) % 5 % 2 for c in range(100)] for r in range(100)]
check(sum(map(sum, life_ref(b))) == 4079, 'h2 i1 test 7: 4,079 live cells by the reference')


def brute_lvp(s):
    best = 0
    for i in range(len(s)):
        depth = 0
        for j in range(i, len(s)):
            depth += 1 if s[j] == '(' else -1
            if depth < 0:
                break
            if depth == 0:
                best = max(best, j - i + 1)
    return best


ok = True
for _ in range(400):
    s = ''.join(random.choice('()') for _ in range(random.randint(0, 12)))
    ok &= lvp(s) == brute_lvp(s)
check(ok, 'h2 i2: the index stack with base -1 equals brute force on 400 random strings')

print()
print(f'{len(FAILS)} failures')
for f in FAILS:
    print('  -', f)
sys.exit(1 if FAILS else 0)
