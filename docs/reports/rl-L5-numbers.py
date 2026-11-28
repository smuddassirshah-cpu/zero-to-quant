"""Recompute every number stated in rl level 5 (search and self-play) and check it at its JSON path.

Run: <venv>/bin/python docs/reports/rl-L5-numbers.py   (standard library and NumPy; about 30 s; exits 0 when every check passes)

Two routes per number. Tic-tac-toe on a 3 by 3 NumPy board here, against the lessons' strings: game value and first moves
by memoised minimax and by plain minimax; positions by search and by counting legal boards over all 3^9 fillings; nodes and
games by a full tree walk and by an iterative stack walk. Alpha-beta node counts by two implementations (recursive, and
an explicit negamax with the same cut rule). Nim losing piles by recursion and by the mod rule. UCT scores by formula and
by a second expression. MCTS visit counts and the self-play curve re-run with code written apart from the lessons. Every
code widget's solution is run against its hidden tests in CPython with its starter failing one.
"""
import itertools, math, os, random, sys
from functools import lru_cache

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level('rl', 5)
E, C = lv.expect, lv.claim
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


# ---------------- run each code widget's tests ----------------
def widgets(node, out):
    if isinstance(node, dict):
        if node.get('kind') == 'code':
            out.append(node)
        for v in node.values():
            widgets(v, out)
    elif isinstance(node, list):
        for v in node:
            widgets(v, out)
    return out


def run_tests(w, src):
    ns = {'__name__': '__main__', '__learner_source__': src}
    res = []
    try:
        if w.get('prelude'):
            exec(w['prelude'], ns)
        exec(src, ns)
        for c in w['tests']:
            try:
                if c.get('setup'):
                    exec(c['setup'], ns)
                got, exp = eval(c['call'], ns), eval(c['expect'], dict(ns))
                if c.get('compare') == 'isclose':
                    tol = c.get('tol', {})
                    rel, ab = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)
                    res.append(math.isclose(float(got), float(exp), rel_tol=rel, abs_tol=ab))
                else:
                    res.append(got == exp)
            except Exception:
                res.append(False)
    except Exception:
        res = [False] * len(w['tests'])
    return res


for fid, doc in lv.files.items():
    for k, w in enumerate(widgets(doc, [])):
        good = run_tests(w, w['solution'])
        C(all(good), f'{fid} code {k}: solution passes all {len(good)} hidden tests', str(good))
        C(not all(run_tests(w, w['starter'])), f'{fid} code {k}: starter fails')

# ---------------- tic-tac-toe on arrays: 1 = X, -1 = O, 0 = empty ----------------
def win_arr(b):
    for a, c, d in LINES:
        if b[a] != 0 and b[a] == b[c] == b[d]:
            return int(b[a])
    return 0


@lru_cache(None)
def mm(key, p):
    b = np.array(key)
    w = win_arr(b)
    if w:
        return w
    if 0 not in b:
        return 0
    vals = []
    for i in np.flatnonzero(b == 0):
        c = b.copy(); c[i] = p
        vals.append(mm(tuple(c), -p))
    return max(vals) if p == 1 else min(vals)


def mm_plain(b, p):
    w = win_arr(b)
    if w:
        return w
    if 0 not in b:
        return 0
    vals = []
    for i in np.flatnonzero(b == 0):
        b[i] = p; vals.append(mm_plain(b, -p)); b[i] = 0
    return max(vals) if p == 1 else min(vals)


E0 = (0,) * 9
first = [mm(tuple(1 if j == i else 0 for j in range(9)), -1) for i in range(9)]
C(mm(E0, 1) == 0 and first == [0] * 9, 'tic-tac-toe value 0 and every first move 0 (memoised)')
C(mm_plain(np.zeros(9, int), 1) == 0, 'tic-tac-toe value 0 by plain minimax')
lv.stated('l17', 'screens[3].prose', 'same value after each of X', first == [0] * 9)

# nodes and games, two walks
def walk(b, p):
    w = win_arr(b)
    if w or 0 not in b:
        return 1, 1
    n = g = 0
    for i in np.flatnonzero(b == 0):
        b[i] = p; a, c = walk(b, -p); b[i] = 0; n += a; g += c
    return n + 1, g
nodes, games = walk(np.zeros(9, int), 1)
stack, n2, g2 = [('.' * 9, 'X')], 0, 0
def winner(s):
    for a, c, d in LINES:
        if s[a] != '.' and s[a] == s[c] == s[d]:
            return s[a]
    return None
while stack:
    s, p = stack.pop(); n2 += 1
    if winner(s) or '.' not in s:
        g2 += 1; continue
    for i in range(9):
        if s[i] == '.':
            stack.append((s[:i] + p + s[i + 1:], 'O' if p == 'X' else 'X'))
C(nodes == n2 == 549946 and games == g2 == 255168, 'full tree 549,946 nodes and 255,168 games, two walks')
seen = set(); st_ = [(E0, 1)]
while st_:
    k, p = st_.pop()
    if k in seen:
        continue
    seen.add(k); b = np.array(k)
    if win_arr(b) or 0 not in b:
        continue
    for i in np.flatnonzero(b == 0):
        c = b.copy(); c[i] = p; st_.append((tuple(c), -p))
legal = 0
for t in itertools.product((0, 1, -1), repeat=9):
    b = np.array(t); x, o = (b == 1).sum(), (b == -1).sum()
    if x not in (o, o + 1):
        continue
    xw = any(b[a] == b[c] == b[d] == 1 for a, c, d in LINES); ow = any(b[a] == b[c] == b[d] == -1 for a, c, d in LINES)
    if (xw and ow) or (xw and x != o + 1) or (ow and x != o):
        continue
    legal += 1
C(len(seen) == legal == 5478 and 3 ** 9 == 19683, '5,478 positions by search and by the legality count over 19,683 fillings')
for ref, path in (('l17', 'screens[4].prose'), ('l17', 'summary.ideas[2]')):
    for v in (549946, 255168, 5478):
        E(ref, path, v)
E('l17', 'screens[4].prose', 19683)
E('l17', 'screens[4].widget.answer', round(nodes / len(seen)))
E('l17', 'screens[4].widget.wrong[0].value', round(games / len(seen)))
E('l17', 'screens[4].widget.wrong[1].value', round(nodes / 19683))

# Nim
def losing(n):
    return all(not losing(n - k) for k in (1, 2, 3) if k <= n)
C([n for n in range(30) if losing(n)] == [n for n in range(30) if n % 4 == 0], 'Nim losing piles are the multiples of 4 (recursion and rule)')
def losing_g(n, m):
    return all(not losing_g(n - k, m) for k in range(1, m + 1) if k <= n)
C([n for n in range(25) if losing_g(n, 4)] == list(range(0, 25, 5)) and [n for n in range(25) if losing_g(n, 2)] == list(range(0, 25, 3)), 'variants: take 1-4 loses at multiples of 5, take 1-2 at multiples of 3')
E('l17', 'screens[1].widget.answer', 21 % 4); E('l17', 'quiz[0].widget.answer', 17 % 4)
E('review', 'items[r5-nim30].widget.answer', 30 % 4); E('review', 'items[r5-nim4].widget.answer', 23 % 5)
E('problems', 'items[p5-nim2].parts[1].widget.answer', 10 % 3); E('problems', 'items[p5-nim2].parts[0].widget.answer', 3)

# backed-up trees
def back(T):
    return max(min(r) for r in T)
E('l17', 'screens[2].widget.answer', back([[3, 9, 6], [2, 5, 1], [4, 7, 8]]))
E('l17', 'quiz[1].widget.answer', back([[2, 8], [5, 4]])); E('l17', 'screens[9].widget.answer', back([[8, 3], [5, 6]]))
E('review', 'items[r5-backup].widget.answer', back([[4, 10], [7, 2], [6, 9]]))
E('problems', 'items[p5-tree].parts[1].widget.answer', back([[2, 7, 5], [8, 6, 9], [1, 4, 3]]))
E('l17', 'screens[7].widget.answer', 10 - 3)

def ab_leaves(T):
    alpha, read, best = -math.inf, [], -math.inf
    for i, kids in enumerate(T):
        m = math.inf
        for j, x in enumerate(kids):
            read.append((i, j)); m = min(m, x)
            if m <= alpha:
                break
        best = max(best, m); alpha = max(alpha, best)
    return best, read
v, rd = ab_leaves([[5, 9, 7], [4, 8, 10], [6, 2, 11]])
skipped = {f'{"abc"[i]}-{j + 1}' for i in range(3) for j in range(3)} - {f'{"abc"[i]}-{j + 1}' for i, j in rd}
C(v == back([[5, 9, 7], [4, 8, 10], [6, 2, 11]]) == 5 and skipped == {'b-2', 'b-3', 'c-3'}, 'hand tree: value 5, leaves b-2, b-3, c-3 skipped')
C(sorted(lv.files['l18-pruning-the-tree']['screens'][0]['widget']['answer']) == sorted(skipped), 'l18 hook key equals the skipped leaves')
E('l18', 'screens[1].widget.answer', 5)
E('l18', 'screens[6].widget.answer', len(ab_leaves([[11, 6, 2], [10, 8, 4], [9, 7, 5]])[1]))
E('review', 'items[r5-leaves].widget.answer', len(ab_leaves([[6, 8, 7], [3, 9, 5], [7, 4, 9]])[1]))
E('problems', 'items[p5-tree].parts[2].widget.answer', len(ab_leaves([[2, 7, 5], [8, 6, 9], [1, 4, 3]])[1]))
E('problems', 'items[p5-tree].parts[3].widget.answer', len(ab_leaves([[8, 6, 9], [2, 7, 5], [1, 4, 3]])[1]))

# alpha-beta on tic-tac-toe, two implementations
def ab1(b, p, a, be, order):
    w = win_arr(b)
    if w:
        return w, 1
    if 0 not in b:
        return 0, 1
    n, best = 1, (-2 if p == 1 else 2)
    for i in order:
        if b[i]:
            continue
        b[i] = p; v_, k = ab1(b, -p, a, be, order); b[i] = 0; n += k
        if p == 1:
            best = max(best, v_); a = max(a, best)
        else:
            best = min(best, v_); be = min(be, best)
        if a >= be:
            break
    return best, n
def ab2(s, p, a, be, order):     # strings, explicit sides
    w = winner(s)
    if w:
        return (1 if w == 'X' else -1), 1
    if '.' not in s:
        return 0, 1
    n = 1
    best = -2 if p == 'X' else 2
    for i in order:
        if s[i] != '.':
            continue
        v_, k = ab2(s[:i] + p + s[i + 1:], 'O' if p == 'X' else 'X', a, be, order); n += k
        best = max(best, v_) if p == 'X' else min(best, v_)
        a, be = (max(a, best), be) if p == 'X' else (a, min(be, best))
        if a >= be:
            break
    return best, n
R9, CEN = list(range(9)), [4, 0, 2, 6, 8, 1, 3, 5, 7]
r1, r2 = ab1(np.zeros(9, int), 1, -2, 2, R9), ab2('.' * 9, 'X', -2, 2, R9)
c1, c2 = ab1(np.zeros(9, int), 1, -2, 2, CEN), ab2('.' * 9, 'X', -2, 2, CEN)
C(r1 == r2 == (0, 18297) and c1 == c2 == (0, 7275), 'alpha-beta: 18,297 nodes (order 0-8) and 7,275 (centre, corners, edges), value 0, two implementations')
C(ab2('X........', 'O', -2, 2, R9)[1] < 4000, 'alpha-beta after a corner opening stays under the test ceiling 4,000')
E('l18', 'screens[2].prose', 18297); E('l18', 'screens[2].widget.answer', round(18297 / 549946, 4))
E('l18', 'screens[2].widget.wrong[0].value', round(549946 / 18297, 4)); E('l18', 'screens[2].widget.wrong[1].value', round(1 - 18297 / 549946, 4))
E('l18', 'screens[3].widget.answer', round(7275 / 18297, 4)); E('l18', 'screens[3].widget.wrong[0].value', round(18297 / 7275, 3))
E('l18', 'summary.ideas[1]', 7275)
E('homework', 'items[h5-minimal].widget.answer', 3 ** 2 + 3 ** 2 - 1)

# UCT
def uct(w, n, N, c=math.sqrt(2)):
    return w / n + math.sqrt(c * c * math.log(N) / n)
for (w, n, N), where in (((2, 3, 4), ('l19', 'screens[2].widget.answer')), ((3, 4, 16), ('l19', 'quiz[0].widget.answer')), ((5, 10, 50), ('review', 'items[r5-uct].widget.answer')),
                         ((4, 5, 10), ('problems', 'items[p5-uct].parts[0].widget.answer')), ((3, 4, 10), ('problems', 'items[p5-uct].parts[1].widget.answer')), ((0, 1, 10), ('problems', 'items[p5-uct].parts[2].widget.answer'))):
    E(where[0], where[1], round(uct(w, n, N), 4))
E('l19', 'screens[2].feedback.correct', round(uct(1, 1, 4), 4))
C(uct(0, 1, 10) > uct(3, 4, 10) > uct(4, 5, 10), 'p5: C > B > A by UCT')
E('l19', 'screens[3].widget.answer', round(3.5 / 6, 4)); E('l19', 'screens[4].widget.answer', 898 / 1000)

# MCTS visits, own implementation (dict tree keyed by move path)
def mcts_own(board, player, iters, seed):
    rng = random.Random(seed)
    stats = {(): [0, 0.0]}; kids = {}
    def legal(s):
        return [] if winner(s) else [i for i in range(9) if s[i] == '.']
    for _ in range(iters):
        s, p, path = board, player, [()]
        while True:
            key = path[-1]; ms = legal(s)
            tried = kids.setdefault(key, [])
            if not ms:
                break
            if len(tried) < len(ms):
                m = ms[len(tried)]; tried.append(m)
                s = s[:m] + p + s[m + 1:]; p = 'O' if p == 'X' else 'X'
                path.append(key + (m,)); stats[path[-1]] = [0, 0.0]
                break
            N = stats[key][0]
            m = max(tried, key=lambda mv: stats[key + (mv,)][1] / stats[key + (mv,)][0] + math.sqrt(2) * math.sqrt(math.log(N) / stats[key + (mv,)][0]))
            s = s[:m] + p + s[m + 1:]; p = 'O' if p == 'X' else 'X'; path.append(key + (m,))
        while not winner(s) and '.' in s:
            i = rng.choice([j for j in range(9) if s[j] == '.']); s = s[:i] + p + s[i + 1:]; p = 'O' if p == 'X' else 'X'
        res = winner(s)
        for d, key in enumerate(path):
            stats[key][0] += 1
            if d:
                mover = player if d % 2 == 1 else ('O' if player == 'X' else 'X')
                stats[key][1] += 1.0 if res == mover else (0.5 if res is None else 0.0)
    return {k[0]: v[0] for k, v in stats.items() if len(k) == 1}
fr = lv.files['l19-tree-search']['screens'][1]['canvas']['controls'][0]['frames']
for it, f in zip((20, 50, 200, 1000), fr):
    own = mcts_own('XX.OO....', 'X', it, 0)
    C(own == {int(k[1:]): v for k, v in f['values'].items()}, f'MCTS seed 0, {it} iterations: visits {own} match the lesson frame')
E('l19', 'screens[1].feedback.correct', 898); E('l19', 'summary.ideas[1]', 898)

# self-play Nim curve, own implementation (values as a 2-D array)
def sp_own(episodes, seed, top=21, alpha=0.5, eps=0.2):
    rng = random.Random(seed); Q = np.zeros((top + 1, 4))
    for _ in range(episodes):
        n = rng.randint(1, top)
        while n > 0:
            ks = [k for k in (1, 2, 3) if k <= n]
            k = rng.choice(ks) if rng.random() < eps else max(ks, key=lambda j: Q[n, j])
            n2 = n - k
            t = 1.0 if n2 == 0 else -max(Q[n2, j] for j in (1, 2, 3) if j <= n2)
            Q[n, k] += alpha * (t - Q[n, k]); n = n2
    return Q
def rate(Q, games=200):
    rng, wins = random.Random(1000), 0
    for _ in range(games):
        n, me = 21, True
        while True:
            ks = [k for k in (1, 2, 3) if k <= n]
            k = max(ks, key=lambda j: Q[n, j]) if me else rng.choice(ks)
            n -= k
            if n == 0:
                wins += me; break
            me = not me
    return round(wins / games, 3)
curve = [rate(sp_own(ep, 0)) for ep in range(0, 301, 10)]
C(curve == lv.files['l20-self-play']['screens'][1]['canvas']['params']['series'][0]['values'], 'self-play win-rate curve re-run matches the recorded series')
E('l20', 'screens[1].explain.text', curve[0]); C(curve[-1] == 1.0, 'curve ends at 1')
for s in range(5):
    Q = sp_own(500, s)
    C(all(max((1, 2, 3)[:min(3, n)], key=lambda j: Q[n, j]) == n % 4 for n in range(1, 22) if n % 4), f'seed {s}: 500 episodes recover take n mod 4')
    C(all(max(Q[n, 1:4]) < 0 for n in (4, 8, 12, 16, 20)), f'seed {s}: every move from a multiple of 4 is valued below 0')
E('l20', 'screens[0].widget.answer', -0.8); E('l20', 'screens[3].widget.answer', 14 % 4); E('l20', 'quiz[1].widget.answer', 9 % 4)
E('homework', 'items[h5-alphazero].widget.model', curve[0])
lv.stated('l20', 'screens[6].prose', '4 games to 1', True)  # reading: Silver et al. 2016 (AlphaGo against Lee Sedol, March 2016)

lv.check_wrongs()
lv.report()
