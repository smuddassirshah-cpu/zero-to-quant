import random, collections, json, re, ast, posixpath, math
from harness import *
random.seed(21)
REP = {}; NUM = {}

# ---------- 2.1 find_anagrams, longest_palindrome ----------
FA_REF = '''
def find_anagrams(s, p):
    need = {}
    for ch in p:
        need[ch] = need.get(ch, 0) + 1
    have = {}
    out = []
    for i, ch in enumerate(s):
        have[ch] = have.get(ch, 0) + 1
        if i >= len(p):
            old = s[i - len(p)]
            have[old] -= 1
            if have[old] == 0:
                del have[old]
        if have == need:
            out.append(i - len(p) + 1)
    return out
'''
FA_START = '''
def find_anagrams(s, p):
    return [i for i in range(len(s)) if s[i:i + len(p)] == p]
'''
def fa_brute(s, p):
    return [i for i in range(len(s) - len(p) + 1) if sorted(s[i:i+len(p)]) == sorted(p)]
ns = {}; exec(FA_REF, ns); faref = ns['find_anagrams']
for _ in range(3000):
    s = ''.join(random.choice('abc') for _ in range(random.randint(0, 12))); p = ''.join(random.choice('abc') for _ in range(random.randint(1, 4)))
    assert faref(s, p) == fa_brute(s, p), (s, p)
fas = [('dcabbacbed','abc'),('babcab','bab'),('aaaa','aa'),('abc','abcd'),('','a'),('baa','aa'),('xyzzyx','zy')]
FA_TESTS = [dict(call=f'find_anagrams({s!r}, {p!r})', expect=fa_brute(s,p)) for s,p in fas]
FA_TESTS.append(dict(setup="s = 'ab' * 50000", call="len(find_anagrams(s, 'ba' * 500))", expect=fa_brute('ab'*3000, 'ba'*500).__len__() + 0 if False else None))
big_s = 'ab'*50000; # count of anagram starts of 'ab'*500 in s: windows of length 1000 -> 100000-1000+1
FA_TESTS[-1]['expect'] = 100000 - 1000 + 1
assert len(faref(big_s, 'ba'*500)) == 99001
check_py('find_anagrams', FA_REF, FA_START, FA_TESTS)
REP['fa'] = md_tests(FA_TESTS)

LP_REF = '''
def longest_palindrome(s):
    best = (0, 0)
    for c in range(2 * len(s) - 1):
        lo, hi = c // 2, c // 2 + c % 2
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
            lo -= 1
            hi += 1
        if hi - lo - 1 > best[1] - best[0]:
            best = (lo + 1, hi)
    return s[best[0]:best[1]]
'''
LP_START = '''
def longest_palindrome(s):
    return s[:1]
'''
def lp_brute(s):
    best = ''
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            t = s[i:j]
            if t == t[::-1] and len(t) > len(best): best = t
    return best
ns = {}; exec(LP_REF, ns); lpref = ns['longest_palindrome']
for _ in range(3000):
    s = ''.join(random.choice('abc') for _ in range(random.randint(0, 12)))
    assert lpref(s) == lp_brute(s), s
lps = ['cabbad','cbbd','a','','abacdfgdcaba','stressedesserts','abcd','aaaa','racecarxyz']
LP_TESTS = [dict(call=f'longest_palindrome({s!r})', expect=lp_brute(s)) for s in lps]
LP_TESTS.append(dict(setup="s = 'a' * 3000", call='len(longest_palindrome(s))', expect=3000))
check_py('longest_palindrome', LP_REF, LP_START, LP_TESTS)
REP['lp'] = md_tests(LP_TESTS)
# centres
NUM['centres_7'] = (2*7-1, 13)
NUM['palins_count_aaa'] = sum(1 for i in range(3) for j in range(i+1,4) if 'aaa'[i:j]=='aaa'[i:j][::-1])  # 6
def pal_count_centres(s):
    n=0
    for c in range(2*len(s)-1):
        lo,hi=c//2,c//2+c%2
        while lo>=0 and hi<len(s) and s[lo]==s[hi]: n+=1; lo-=1; hi+=1
    return n
assert pal_count_centres('aaa') == NUM['palins_count_aaa'] == 6
NUM['palins_count_abba'] = (pal_count_centres('abba'), sum(1 for i in range(4) for j in range(i+1,5) if 'abba'[i:j]=='abba'[i:j][::-1]))
assert NUM['palins_count_abba'][0]==NUM['palins_count_abba'][1]
# palindromic permutation: odd counts <= 1
def pp(s): return sum(v%2 for v in collections.Counter(s).values()) <= 1
def pp_brute(s):
    from itertools import permutations
    return any(''.join(p)==''.join(p)[::-1] for p in set(permutations(s)))
for w in ['carerac','aabb','abc','aab','civic','ivicc','aabbcd','']:
    assert pp(w)==pp_brute(w), w
NUM['pp'] = {w: pp(w) for w in ['carerac','aabbc','abcabc','abcd','aabbccd']}
# sliding window cost: find_anagrams with n=100000, p=1000: naive sort per window
NUM['naive_window_work'] = (100000-1000+1)*1000
NUM['window_work_fast'] = 100000
# group anagram key counts
NUM['fa_ex'] = fa_brute('dcabbacbed','abc')

# ---------- 2.2 calculate / decode_string ----------
CALC_REF = '''
def calculate(s):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, 'u': 3}
    nums, ops = [], []
    def apply():
        op = ops.pop()
        if op == 'u':
            nums.append(-nums.pop())
            return
        b, a = nums.pop(), nums.pop()
        if op == '+': nums.append(a + b)
        elif op == '-': nums.append(a - b)
        elif op == '*': nums.append(a * b)
        else: nums.append(abs(a) // abs(b) * (1 if (a < 0) == (b < 0) else -1))
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
            ops.append(c); i += 1; expect_operand = True
        elif c == ')':
            while ops[-1] != '(':
                apply()
            ops.pop(); i += 1; expect_operand = False
        else:
            if c == '-' and expect_operand:
                c = 'u'
            if c != 'u':
                while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[c]:
                    apply()
            ops.append(c); i += 1; expect_operand = True
    while ops:
        apply()
    return nums[0]
'''
CALC_START = '''
def calculate(s):
    return int(eval(s.replace('/', '//')))
'''
def calc_brute(s):
    def ev(n):
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.UnaryOp): return -ev(n.operand)
        a, b = ev(n.left), ev(n.right)
        if isinstance(n.op, ast.Add): return a + b
        if isinstance(n.op, ast.Sub): return a - b
        if isinstance(n.op, ast.Mult): return a * b
        q = abs(a) // abs(b); return q if (a < 0) == (b < 0) else -q
    return ev(ast.parse(s.strip(), mode='eval').body)
ns = {}; exec(CALC_REF, ns); cref = ns['calculate']
def rand_expr(d=0):
    r = random.random()
    if d > 2 or r < 0.3:
        return str(random.randint(0, 12))
    if r < 0.45: return '-' + rand_expr(d + 1) if False else '(-' + str(random.randint(1,9)) + ')'
    if r < 0.6: return '(' + rand_expr(d + 1) + ')'
    op = random.choice('+-*/')
    return rand_expr(d + 1) + random.choice(['', ' ']) + op + random.choice(['', ' ']) + rand_expr(d + 1)
n_ok = 0
for _ in range(4000):
    e = rand_expr()
    try:
        exp = calc_brute(e)
    except ZeroDivisionError:
        continue
    assert cref(e) == exp, (e, cref(e), exp); n_ok += 1
print('calc random cases', n_ok)
cs = ['4+3*2',' 7/2 ','(2+(6+3+1)-4)+(5+9)','-(2+3)*4','14-3/2','-7/2','(-7)/2','2*(5+5*2)/3+(6/2+8)','1-(-2)','2*-3','10-2-3','100/10/5','42','-(-(5))','8/3*3']
CALC_TESTS = [dict(call=f'calculate({e!r})', expect=calc_brute(e)) for e in cs]
check_py('calculate', CALC_REF, CALC_START, CALC_TESTS)
REP['calc'] = md_tests(CALC_TESTS)
# postfix traces for the lesson: infix 3+2*2 -> postfix
def to_postfix(s):
    prec={'+':1,'-':1,'*':2,'/':2}; out=[]; st=[]
    for t in re.findall(r'\d+|[-+*/()]', s):
        if t.isdigit(): out.append(t)
        elif t=='(': st.append(t)
        elif t==')':
            while st[-1]!='(': out.append(st.pop())
            st.pop()
        else:
            while st and st[-1]!='(' and prec[st[-1]]>=prec[t]: out.append(st.pop())
            st.append(t)
    while st: out.append(st.pop())
    return out
def eval_postfix(tokens):
    st=[]
    for t in tokens:
        if t.isdigit(): st.append(int(t))
        else:
            b,a=st.pop(),st.pop()
            st.append({'+':a+b,'-':a-b,'*':a*b,'/':abs(a)//abs(b)*(1 if (a<0)==(b<0) else -1)}[t])
    return st[0]
for e in ['3+2*2','2*(5+5*2)/3+(6/2+8)','10-2-3','8/3*3']:
    assert eval_postfix(to_postfix(e)) == calc_brute(e) == cref(e)
NUM['postfix'] = {e: ' '.join(to_postfix(e)) for e in ['3+2*2','10-2-3','(1+2)*3']}
NUM['postfix_vals'] = {e: calc_brute(e) for e in ['3+2*2','10-2-3','(1+2)*3']}
assert cref('(1+2)*3') == 9
# max stack depth for nested parentheses ((((1)))) 
NUM['calc_ops_depth'] = None
# stack size: peak size of ops stack for 2*(5+5*2)/3+(6/2+8)
def peak_ops(s):
    prec={'+':1,'-':1,'*':2,'/':2}; st=[]; peak=0
    for t in re.findall(r'\d+|[-+*/()]', s):
        if t.isdigit(): continue
        if t=='(': st.append(t)
        elif t==')':
            while st[-1]!='(': st.pop()
            st.pop()
        else:
            while st and st[-1]!='(' and prec[st[-1]]>=prec[t]: st.pop()
            st.append(t)
        peak=max(peak,len(st))
    return peak
NUM['peak_ops'] = peak_ops('2*(5+5*2)/3+(6/2+8)')

DS_REF = '''
def decode_string(s):
    stack = []
    count, cur = 0, []
    for ch in s:
        if ch.isdigit():
            count = count * 10 + int(ch)
        elif ch == '[':
            stack.append((cur, count))
            cur, count = [], 0
        elif ch == ']':
            prev, k = stack.pop()
            prev.append(''.join(cur) * k)
            cur = prev
        else:
            cur.append(ch)
    return ''.join(cur)
'''
DS_START = '''
def decode_string(s):
    return s
'''
def ds_brute(s):
    pat = re.compile(r'(\d+)\[([a-z]*)\]')
    while pat.search(s):
        s = pat.sub(lambda m: m.group(2) * int(m.group(1)), s)
    return s
ns = {}; exec(DS_REF, ns); dref = ns['decode_string']
def rand_enc(d=0):
    parts = []
    for _ in range(random.randint(1, 3)):
        if d < 2 and random.random() < 0.5:
            parts.append(str(random.randint(1, 3)) + '[' + rand_enc(d + 1) + ']')
        else:
            parts.append(''.join(random.choice('abc') for _ in range(random.randint(1, 2))))
    return ''.join(parts)
for _ in range(3000):
    e = rand_enc(); assert dref(e) == ds_brute(e), e
dss = ['3[a]2[bc]','2[b3[a]]','3[xy]2[z]w','abc','10[a]','','2[2[2[a]]]','a2[b]c','1[]','12[xy]']
DS_TESTS = [dict(call=f'decode_string({e!r})', expect=ds_brute(e)) for e in dss]
check_py('decode_string', DS_REF, DS_START, DS_TESTS)
REP['ds'] = md_tests(DS_TESTS)
NUM['decode_lens'] = {e: len(ds_brute(e)) for e in ['2[b3[a]]','3[xy]2[z]w','2[2[2[a]]]','12[xy]']}
NUM['decode_big'] = len(ds_brute('9[' * 1 + '9[' + '9[' + 'a' + ']]]'))  # 729
assert NUM['decode_big'] == 9**3

# HW2: simplify_path, longest_valid_parentheses
SP_REF = '''
def simplify_path(path):
    stack = []
    for part in path.split('/'):
        if part == '..':
            if stack:
                stack.pop()
        elif part and part != '.':
            stack.append(part)
    return '/' + '/'.join(stack)
'''
SP_START = '''
def simplify_path(path):
    return path
'''
def sp_brute(p): return posixpath.normpath('/' + p.lstrip('/'))
ns = {}; exec(SP_REF, ns); spref = ns['simplify_path']
parts = ['a','b','..','.','','c','...']
for _ in range(3000):
    p = '/' + '/'.join(random.choice(parts) for _ in range(random.randint(0, 7))) + random.choice(['','/'])
    p = re.sub(r'^/+', '/', p)
    assert spref(p) == sp_brute(p), p
sps = ['/home/','/home//foo/','/usr//lib/./../bin/','/../','/.../a/..','/a/b/c','/']
SP_TESTS = [dict(call=f'simplify_path({p!r})', expect=sp_brute(p)) for p in sps]
check_py('simplify_path', SP_REF, SP_START, SP_TESTS)
REP['sp'] = md_tests(SP_TESTS)

LV_REF = '''
def longest_valid_parentheses(s):
    stack = [-1]
    best = 0
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best
'''
LV_START = '''
def longest_valid_parentheses(s):
    return s.count('()') * 2
'''
def lv_brute(s):
    def valid(t):
        d = 0
        for c in t:
            d += 1 if c == '(' else -1
            if d < 0: return False
        return d == 0
    return max([j - i for i in range(len(s)) for j in range(i + 2, len(s) + 1, 2) if valid(s[i:j])] + [0])
ns = {}; exec(LV_REF, ns); lvref = ns['longest_valid_parentheses']
for _ in range(3000):
    s = ''.join(random.choice('()') for _ in range(random.randint(0, 14)))
    assert lvref(s) == lv_brute(s), s
lvs = ['(()',')(()())(','','()(())','(()(((()','()(()',')(','((()))','())((())']
LV_TESTS = [dict(call=f'longest_valid_parentheses({s!r})', expect=lv_brute(s)) for s in lvs]
LV_TESTS.append(dict(setup="s = '(' * 50000 + ')' * 50000", call='longest_valid_parentheses(s)', expect=100000))
assert lvref('('*50000+')'*50000) == 100000
check_py('longest_valid_parentheses', LV_REF, LV_START, LV_TESTS)
REP['lv'] = md_tests(LV_TESTS)

# ---------- 2.3 l8 run_strategy ----------
RS_REF = '''
def run_strategy(prices):
    pnl = trades = 0
    long_, entry, bought = False, 0, 0
    for i, p in enumerate(prices):
        if not long_:
            if i >= 1 and p < prices[i - 1]:
                long_, entry, bought = True, p, i
        else:
            if 100 * p >= 105 * entry or 100 * p <= 97 * entry or i - bought == 3:
                pnl += p - entry
                trades += 1
                long_ = False
    if long_:
        pnl += prices[-1] - entry
        trades += 1
    return [pnl, trades]
'''
RS_START = '''
def run_strategy(prices):
    return [prices[-1] - prices[0], 1]
'''
def rs_brute(prices):
    # second method: find each trade by scanning forward from the buy day, then jump
    n = len(prices); i = 1; pnl = trades = 0
    while i < n:
        if prices[i] < prices[i - 1]:
            e = prices[i]; j = i + 1; sold = None
            while j < n:
                p = prices[j]
                if 100 * p >= 105 * e or 100 * p <= 97 * e or j - i == 3:
                    sold = j; break
                j += 1
            if sold is None: sold = n - 1
            pnl += prices[sold] - e; trades += 1
            i = sold + 1 if sold > i else i + 1    # no buy on the sell day; last-day forced sale at buy day ends too
            if sold == i - 1 and sold == n - 1: break
        else:
            i += 1
    return [pnl, trades]
ns = {}; exec(RS_REF, ns); rsref = ns['run_strategy']
for _ in range(5000):
    pr = [random.randint(90, 112) for _ in range(random.randint(1, 14))]
    assert rsref(pr) == rs_brute(pr), (pr, rsref(pr), rs_brute(pr))
rss = [[100,98,99,100,104,110],[100,100,100],[100,99,98,97,96,95,94,93],[100,99,105,104,103,102],[100,95,100,106,90,89,95,99],[50],[100,101,99,100,101],[100,96,92,93,99,98,97,96]]
RS_TESTS = [dict(call=f'run_strategy({p})', expect=rs_brute(p)) for p in rss]
check_py('run_strategy', RS_REF, RS_START, RS_TESTS)
REP['rs'] = md_tests(RS_TESTS)
# worked trace of the lesson example
ex = [100,98,99,100,104,110]
print('strategy example', rsref(ex), rs_brute(ex))
NUM['rs_ex'] = rsref(ex)

# ---------- 2.4 grids ----------
SO_REF = '''
def spiral_order(m):
    if not m:
        return []
    top, bottom, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(m[top][c])
        for r in range(top + 1, bottom + 1):
            out.append(m[r][right])
        if top < bottom:
            for c in range(right - 1, left - 1, -1):
                out.append(m[bottom][c])
        if left < right:
            for r in range(bottom - 1, top, -1):
                out.append(m[r][left])
        top += 1; bottom -= 1; left += 1; right -= 1
    return out
'''
SO_START = '''
def spiral_order(m):
    return [x for row in m for x in row]
'''
def so_brute(m):
    if not m: return []
    R, C = len(m), len(m[0]); seen = set(); r = c = 0; dr, dc = 0, 1; out = []
    for _ in range(R * C):
        out.append(m[r][c]); seen.add((r, c))
        nr, nc = r + dr, c + dc
        if not (0 <= nr < R and 0 <= nc < C) or (nr, nc) in seen:
            dr, dc = dc, -dr
            nr, nc = r + dr, c + dc
        r, c = nr, nc
    return out
ns = {}; exec(SO_REF, ns); soref = ns['spiral_order']
for _ in range(1500):
    R, C = random.randint(0, 6), random.randint(1, 6)
    m = [[random.randint(0, 99) for _ in range(C)] for _ in range(R)]
    assert soref(m) == so_brute(m), m
sos = [[[1,2,3],[4,5,6],[7,8,9]],[[1,2,3,4],[5,6,7,8],[9,10,11,12]],[[1]],[[1,2,3]],[[1],[2],[3]],[],[[1,2],[3,4],[5,6],[7,8]]]
SO_TESTS = [dict(call=f'spiral_order({m})', expect=so_brute(m)) for m in sos]
SO_TESTS.append(dict(setup='m = [[r * 300 + c for c in range(300)] for r in range(300)]', call='spiral_order(m)[-1]', expect=so_brute([[r*300+c for c in range(300)] for r in range(300)])[-1]))
check_py('spiral_order', SO_REF, SO_START, SO_TESTS)
REP['so'] = md_tests(SO_TESTS)
NUM['so_3x4_last'] = so_brute(sos[1])[-1]
NUM['so_big_last'] = SO_TESTS[-1]['expect']

ROT_REF = '''
def rotate(m):
    n = len(m)
    for r in range(n):
        for c in range(r + 1, n):
            m[r][c], m[c][r] = m[c][r], m[r][c]
    for row in m:
        row.reverse()
'''
ROT_START = '''
def rotate(m):
    pass
'''
def rot_brute(m):
    n = len(m); return [[m[n - 1 - c][r] for c in range(n)] for r in range(n)]
ns = {}; exec(ROT_REF, ns); rotref = ns['rotate']
for _ in range(500):
    n = random.randint(0, 6); m = [[random.randint(0, 99) for _ in range(n)] for _ in range(n)]
    exp = rot_brute(m); mm = [r[:] for r in m]; rotref(mm); assert mm == exp
rots = [[[1,2,3],[4,5,6],[7,8,9]],[[1,2],[3,4]],[[1]],[[3,8,1,6],[9,2,7,4],[5,11,10,12],[14,0,13,15]],[]]
ROT_TESTS = [dict(setup=f'm = {m}; rotate(m)', call='m', expect=rot_brute(m)) for m in rots]
ROT_TESTS.append(dict(setup='m = [[r * 200 + c for c in range(200)] for r in range(200)]; rotate(m)', call='m[0][:3]', expect=rot_brute([[r*200+c for c in range(200)] for r in range(200)])[0][:3]))
check_py('rotate', ROT_REF, ROT_START, ROT_TESTS)
REP['rot'] = md_tests(ROT_TESTS)
# index mapping: (r, c) in n x n goes to (c, n-1-r)
NUM['rot_map'] = [(r, c, (c, 4 - r)) for r, c in [(0, 1), (1, 3), (4, 0)]]
m5 = [[r*5+c for c in range(5)] for r in range(5)]; rm5 = rot_brute(m5)
for r, c, (nr, nc) in NUM['rot_map']: assert rm5[nr][nc] == m5[r][c]

CR_REF = '''
def capture_regions(board):
    rows, cols = len(board), len(board[0]) if board else 0
    safe = set()
    stack = [(r, c) for r in range(rows) for c in range(cols)
             if (r in (0, rows - 1) or c in (0, cols - 1)) and board[r][c] == 'O']
    while stack:
        r, c = stack.pop()
        if (r, c) in safe:
            continue
        safe.add((r, c))
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'O' and (nr, nc) not in safe:
                stack.append((nr, nc))
    return [''.join('O' if ch == 'O' and (r, c) in safe else ('X' if ch == 'O' else ch) for c, ch in enumerate(row))
            for r, row in enumerate(board)]
'''
CR_START = '''
def capture_regions(board):
    return list(board)
'''
def cr_brute(board):
    rows = len(board); cols = len(board[0]) if board else 0
    g = [list(r) for r in board]
    safe = [[board[r][c] == 'O' and (r in (0, rows-1) or c in (0, cols-1)) for c in range(cols)] for r in range(rows)]
    changed = True
    while changed:
        changed = False
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O' and not safe[r][c]:
                    if any(0 <= r+dr < rows and 0 <= c+dc < cols and safe[r+dr][c+dc] for dr, dc in ((1,0),(-1,0),(0,1),(0,-1))):
                        safe[r][c] = True; changed = True
    return [''.join('O' if board[r][c] == 'O' and safe[r][c] else ('X' if board[r][c] == 'O' else board[r][c]) for c in range(cols)) for r in range(rows)]
ns = {}; exec(CR_REF, ns); crref = ns['capture_regions']
for _ in range(2000):
    R, C = random.randint(1, 6), random.randint(1, 6)
    b = [''.join(random.choice('XO') for _ in range(C)) for _ in range(R)]
    assert crref(b) == cr_brute(b), b
crs = [['XXXX','XOOX','XXOX','XOXX'],['X'],['O'],['XXX','XOX','XXX'],['OOO','OXO','OOO'],['XOXO','OXOX','XOXO'],['XXXXX','XOOOX','XOXOX','XOOOX','XXXXX']]
CR_TESTS = [dict(call=f'capture_regions({b})', expect=cr_brute(b)) for b in crs]
CR_TESTS.append(dict(setup="b = ['X' * 400] + ['X' + 'O' * 398 + 'X'] * 398 + ['X' * 400]", call='sum(r.count("O") for r in capture_regions(b))', expect=0))
b = ['X'*400]+['X'+'O'*398+'X']*398+['X'*400]; assert sum(r.count('O') for r in crref(b)) == 0 == sum(r.count('O') for r in cr_brute(b[:60]+[b[-1]]))*0
check_py('capture_regions', CR_REF, CR_START, CR_TESTS)
REP['cr'] = md_tests(CR_TESTS)
NUM['cr_ex_Os'] = sum(r.count('O') for r in cr_brute(crs[0]))
print('cr ex', cr_brute(crs[0]))

LF_REF = '''
def life_step(board):
    rows, cols = len(board), len(board[0])
    def live_neighbours(r, c):
        n = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if (dr or dc) and 0 <= r + dr < rows and 0 <= c + dc < cols:
                    n += board[r + dr][c + dc]
        return n
    return [[1 if (live_neighbours(r, c) == 3 or (board[r][c] and live_neighbours(r, c) == 2)) else 0
             for c in range(cols)] for r in range(rows)]
'''
LF_START = '''
def life_step(board):
    return [row[:] for row in board]
'''
def lf_brute(board):
    live = {(r, c) for r, row in enumerate(board) for c, v in enumerate(row) if v}
    cnt = collections.Counter((r+dr, c+dc) for r, c in live for dr in (-1,0,1) for dc in (-1,0,1) if dr or dc)
    R, C = len(board), len(board[0])
    return [[1 if (cnt[(r,c)] == 3 or ((r,c) in live and cnt[(r,c)] == 2)) else 0 for c in range(C)] for r in range(R)]
ns = {}; exec(LF_REF, ns); lfref = ns['life_step']
for _ in range(1500):
    R, C = random.randint(1, 6), random.randint(1, 6)
    b = [[random.randint(0, 1) for _ in range(C)] for _ in range(R)]
    assert lfref(b) == lf_brute(b)
lfs = [[[0,1,0],[0,1,0],[0,1,0]],[[1,1],[1,1]],[[0,0,0],[0,0,0]],[[1,0],[0,0]],[[1,1,0],[0,1,0],[0,1,1],[0,0,0]],[[1,1,1]]]
LF_TESTS = [dict(call=f'life_step({b})', expect=lf_brute(b)) for b in lfs]
LF_TESTS.append(dict(setup='b = [[(r * 7 + c * 3) % 5 % 2 for c in range(100)] for r in range(100)]', call='sum(map(sum, life_step(b)))', expect=sum(map(sum, lf_brute([[(r*7+c*3)%5%2 for c in range(100)] for r in range(100)])))))
check_py('life_step', LF_REF, LF_START, LF_TESTS)
REP['lf'] = md_tests(LF_TESTS)
NUM['lf_glider'] = lf_brute(lfs[4])

# ---------- 2.5 matching engine ----------
BOOK_REF = '''
from collections import deque

def _simulate(events):
    books = {0: {}, 1: {}}            # side -> price -> deque of [id, qty]
    where = {}                        # id -> (side, price)
    trades = []

    def match(taker, side, qty, limit):
        opp = books[1 - side]
        while qty > 0 and opp:
            best = min(opp) if side == 0 else max(opp)
            if limit is not None and ((side == 0 and best > limit) or (side == 1 and best < limit)):
                break
            queue = opp[best]
            while qty > 0 and queue:
                maker = queue[0]
                fill = min(qty, maker[1])
                trades.append([taker, maker[0], best, fill])
                qty -= fill
                maker[1] -= fill
                if maker[1] == 0:
                    queue.popleft()
                    del where[maker[0]]
            if not queue:
                del opp[best]
        return qty

    for ev in events:
        kind = ev[0]
        if kind == 0:
            _, oid, side, price, qty = ev
            rest = match(oid, side, qty, price)
            if rest > 0:
                books[side].setdefault(price, deque()).append([oid, rest])
                where[oid] = (side, price)
        elif kind == 1:
            _, oid, side, qty = ev
            match(oid, side, qty, None)
        elif kind == 2:
            oid = ev[1]
            if oid in where:
                side, price = where.pop(oid)
                queue = books[side][price]
                for k, o in enumerate(queue):
                    if o[0] == oid:
                        del queue[k]
                        break
                if not queue:
                    del books[side][price]
        else:
            _, oid, new_qty = ev
            if oid in where:
                side, price = where[oid]
                queue = books[side][price]
                for k, o in enumerate(queue):
                    if o[0] == oid:
                        if new_qty < o[1]:
                            o[1] = new_qty
                        elif new_qty > o[1]:
                            del queue[k]
                            queue.append([oid, new_qty])
                        break
    return trades, books

def run_book(events):
    return _simulate(events)[0]

def levels(events, side):
    book = _simulate(events)[1][side]
    prices = sorted(book, reverse=(side == 0))
    return [[p, sum(o[1] for o in book[p])] for p in prices]
'''
BOOK_START = '''
def run_book(events):
    return []

def levels(events, side):
    return []
'''
def book_brute(events):
    rest = []      # dicts: id, side, price, qty, seq
    seq = 0; trades = []
    def take(taker, side, qty, limit):
        while qty > 0:
            cands = [o for o in rest if o['side'] == 1 - side and (limit is None or (o['price'] <= limit if side == 0 else o['price'] >= limit))]
            if not cands: break
            best = min(cands, key=lambda o: (o['price'] if side == 0 else -o['price'], o['seq']))
            f = min(qty, best['qty']); trades.append([taker, best['id'], best['price'], f]); qty -= f; best['qty'] -= f
            if best['qty'] == 0: rest.remove(best)
        return qty
    for ev in events:
        if ev[0] == 0:
            _, i, s, p, q = ev; q = take(i, s, q, p)
            if q > 0: seq += 1; rest.append(dict(id=i, side=s, price=p, qty=q, seq=seq))
        elif ev[0] == 1:
            take(ev[1], ev[2], ev[3], None)
        elif ev[0] == 2:
            rest[:] = [o for o in rest if o['id'] != ev[1]]
        else:
            for o in rest:
                if o['id'] == ev[1]:
                    if ev[2] < o['qty']: o['qty'] = ev[2]
                    elif ev[2] > o['qty']: seq += 1; o['qty'] = ev[2]; o['seq'] = seq
    def lv(side):
        d = collections.defaultdict(int)
        for o in rest:
            if o['side'] == side: d[o['price']] += o['qty']
        return [[p, d[p]] for p in sorted(d, reverse=(side == 0))]
    return trades, lv(0), lv(1)
ns = {}; exec(BOOK_REF, ns); runb, levs = ns['run_book'], ns['levels']
def rand_events(n):
    ev, ids = [], 0
    for _ in range(n):
        r = random.random(); 
        if r < 0.55:
            ids += 1; ev.append([0, ids, random.randint(0, 1), random.randint(98, 103), random.randint(1, 9)])
        elif r < 0.7:
            ids += 1; ev.append([1, ids, random.randint(0, 1), random.randint(1, 12)])
        elif r < 0.85 and ids:
            ev.append([2, random.randint(1, ids)])
        elif ids:
            ev.append([3, random.randint(1, ids), random.randint(1, 9)])
    return ev
for _ in range(4000):
    e = rand_events(random.randint(1, 16)); bt, b0, b1 = book_brute(e)
    assert runb(e) == bt and levs(e, 0) == b0 and levs(e, 1) == b1, e
print('book random ok')
bk = [
 [[0,1,0,100,5],[0,2,1,101,5],[0,3,1,100,3]],
 [[0,1,1,101,4],[0,2,1,102,6],[0,3,0,102,7]],
 [[0,1,1,100,3],[0,2,1,100,4],[0,3,0,100,5]],
 [[0,1,0,99,10],[1,2,1,4],[1,3,1,20]],
 [[0,1,0,100,5],[2,1],[0,2,1,100,5]],
 [[0,1,1,101,5],[0,2,1,101,5],[3,1,3],[0,3,0,101,6]],
 [[0,1,1,101,5],[0,2,1,101,5],[3,1,8],[0,3,0,101,6]],
 [[0,1,0,100,2],[0,2,0,99,3],[0,3,1,99,4],[0,4,1,100,1]],
]
BOOK_TESTS = []
for e in bk:
    bt, b0, b1 = book_brute(e)
    BOOK_TESTS.append(dict(call=f'run_book({e})', expect=bt))
BOOK_TESTS.append(dict(call=f'levels({bk[0]}, 1)', expect=book_brute(bk[0])[2]))
BOOK_TESTS.append(dict(call=f'levels({bk[7]}, 0)', expect=book_brute(bk[7])[1]))
BOOK_TESTS.append(dict(call=f'levels({bk[7]}, 1)', expect=book_brute(bk[7])[2]))
BOOK_TESTS.append(dict(call=f'levels({bk[3]}, 0)', expect=book_brute(bk[3])[1]))
check_py('run_book+levels', BOOK_REF, BOOK_START, BOOK_TESTS)
REP['book'] = md_tests(BOOK_TESTS)
for e in bk: print(e, '->', book_brute(e))
BOOK_CPP_REF = '''#include <vector>
#include <map>
#include <deque>
#include <unordered_map>
#include <algorithm>
struct Resting { int id; int qty; };
struct Engine {
    std::map<int, std::deque<Resting>> bids, asks;
    std::unordered_map<int, std::pair<int, int>> where;
    std::vector<std::vector<int>> trades;
    int match(int taker, int side, int qty, bool has_limit, int limit) {
        while (qty > 0) {
            if (side == 0 ? asks.empty() : bids.empty()) break;
            int best = side == 0 ? asks.begin()->first : bids.rbegin()->first;
            if (has_limit && ((side == 0 && best > limit) || (side == 1 && best < limit))) break;
            auto& queue = side == 0 ? asks[best] : bids[best];
            while (qty > 0 && !queue.empty()) {
                Resting& m = queue.front();
                int fill = std::min(qty, m.qty);
                trades.push_back({taker, m.id, best, fill});
                qty -= fill; m.qty -= fill;
                if (m.qty == 0) { where.erase(m.id); queue.pop_front(); }
            }
            if (queue.empty()) { if (side == 0) asks.erase(best); else bids.erase(best); }
        }
        return qty;
    }
    std::map<int, std::deque<Resting>>& book(int side) { return side == 0 ? bids : asks; }
    void apply(const std::vector<int>& ev) {
        if (ev[0] == 0) {
            int rest = match(ev[1], ev[2], ev[4], true, ev[3]);
            if (rest > 0) { book(ev[2])[ev[3]].push_back({ev[1], rest}); where[ev[1]] = {ev[2], ev[3]}; }
        } else if (ev[0] == 1) {
            match(ev[1], ev[2], ev[3], false, 0);
        } else if (ev[0] == 2) {
            auto it = where.find(ev[1]);
            if (it == where.end()) return;
            auto& q = book(it->second.first)[it->second.second];
            q.erase(std::find_if(q.begin(), q.end(), [&](const Resting& r) { return r.id == ev[1]; }));
            if (q.empty()) book(it->second.first).erase(it->second.second);
            where.erase(it);
        } else {
            auto it = where.find(ev[1]);
            if (it == where.end()) return;
            auto& q = book(it->second.first)[it->second.second];
            auto pos = std::find_if(q.begin(), q.end(), [&](const Resting& r) { return r.id == ev[1]; });
            if (ev[2] < pos->qty) pos->qty = ev[2];
            else if (ev[2] > pos->qty) { q.erase(pos); q.push_back({ev[1], ev[2]}); }
        }
    }
};
std::vector<std::vector<int>> run_book(std::vector<std::vector<int>> events) {
    Engine e;
    for (const auto& ev : events) e.apply(ev);
    return e.trades;
}
std::vector<std::vector<int>> levels(std::vector<std::vector<int>> events, int side) {
    Engine e;
    for (const auto& ev : events) e.apply(ev);
    std::vector<std::vector<int>> out;
    auto add = [&](int price, const std::deque<Resting>& q) { int t = 0; for (const auto& r : q) t += r.qty; out.push_back({price, t}); };
    if (side == 0) for (auto it = e.bids.rbegin(); it != e.bids.rend(); ++it) add(it->first, it->second);
    else for (const auto& kv : e.asks) add(kv.first, kv.second);
    return out;
}
'''
BOOK_CPP_START = '''#include <vector>
std::vector<std::vector<int>> run_book(std::vector<std::vector<int>> events) {
    return {};
}
std::vector<std::vector<int>> levels(std::vector<std::vector<int>> events, int side) {
    return {};
}
'''
calls = []
V = 'std::vector<std::vector<int>>'
for t in BOOK_TESTS:
    fn, rest_ = t['call'].split('(', 1)
    if fn == 'run_book':
        calls.append((f"run_book({V}{cpp_lit(eval(rest_[:-1]))})", t['expect']))
    else:
        evs, side = eval('(' + rest_)
        calls.append((f"levels({V}{cpp_lit(evs)}, {side})", t['expect']))
check_cpp('run_book_cpp', BOOK_CPP_REF, BOOK_CPP_START, calls)
# also cross-check the C++ reference on random events vs brute
import subprocess, tempfile
rnd = [rand_events(random.randint(1, 16)) for _ in range(300)]
prog = BOOK_CPP_REF + '\n#include <iostream>\n' + TOSTR + '\nint main(){\n'
for i, e in enumerate(rnd):
    prog += f'  std::cout << "R{i}:"; zq_put(std::cout, run_book({V}{cpp_lit(e)})); std::cout << "|"; zq_put(std::cout, levels({V}{cpp_lit(e)}, 0)); std::cout << "|"; zq_put(std::cout, levels({V}{cpp_lit(e)}, 1)); std::cout << "\\n";\n'
prog += '}\n'
d = tempfile.mkdtemp(dir='build'); open(d + '/m.cpp', 'w').write(prog)
subprocess.run(['g++', '-std=c++20', '-O1', '-fno-exceptions', '-o', d + '/a', d + '/m.cpp'], check=True)
out = subprocess.run([d + '/a'], capture_output=True, text=True).stdout.splitlines()
for i, line in enumerate(out):
    a, b, c = line.split(':', 1)[1].split('|')
    bt, b0, b1 = book_brute(rnd[i])
    assert json.loads(a) == bt and json.loads(b) == b0 and json.loads(c) == b1, rnd[i]
print('cpp book matches brute on 300 random streams')

# numbers for review
NUM['book3_trades'] = book_brute(bk[2])[0]
NUM['book_market_unfilled'] = book_brute(bk[3])
NUM['book_amend_down'] = book_brute(bk[5])[0]
NUM['book_amend_up'] = book_brute(bk[6])[0]
NUM['sim_cost'] = 'one pass'
json.dump(NUM, open('l2_numbers.json', 'w'), default=str)
json.dump(REP, open('l2_tests.json', 'w'))
for k, v in NUM.items(): print(k, v)
