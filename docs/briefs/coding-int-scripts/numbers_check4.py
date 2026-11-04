import itertools, functools, collections
def best(pr, b):
    r = 0
    for ch in itertools.product(range(3), repeat=len(pr)):
        pts = m = 0
        for (fp, fm, pp, pm), c in zip(pr, ch):
            if c == 1: pts += fp; m += fm
            elif c == 2: pts += pp; m += pm
        if m <= b: r = max(r, pts)
    return r
def memo(pr, b):
    @functools.lru_cache(None)
    def go(i, left):
        if i == len(pr): return 0
        fp, fm, pp, pm = pr[i]; r = go(i+1, left)
        if left >= fm: r = max(r, fp + go(i+1, left-fm))
        if left >= pm: r = max(r, pp + go(i+1, left-pm))
        return r
    return go(0, b)
def greedy(pr, b):
    order = sorted(pr, key=lambda p: -p[0]/p[1]); t = pts = 0
    for fp, fm, pp, pm in order:
        if t + fm <= b: t += fm; pts += fp
    return pts
P = ((40,20,12,6),(60,35,25,12),(90,50,30,18))
for b in (60, 62, 65, 70):
    print(b, best(P, b), memo(P, b), greedy(P, b))
print([(p[0]/p[1]) for p in P])
# second_largest distinct
def sl(xs):
    s = sorted(set(xs), reverse=True)
    return s[1] if len(s) > 1 else None
def sl2(xs):
    top = second = None
    for x in xs:
        if top is None or x > top: top, second = x, top
        elif x < top and (second is None or x > second): second = x
    return second
for xs in ([], [5], [5,5], [3,1,2], [2,2,1], [4,4,3,3,1]):
    assert sl(xs) == sl2(xs); print(xs, sl(xs))
# calendar lesson numbers: k=1
def cal(k, ops):
    bk, out = [], []
    def fits(s, e):
        return all(sum(1 for a, b in bk if a <= t < b) + 1 <= k for t in range(s, e))
    for op in ops:
        if op[0] == 0:
            if fits(op[1], op[2]): bk.append((op[1], op[2])); out.append(True)
            else: out.append(False)
        elif op[0] == 1:
            if (op[1], op[2]) in bk: bk.remove((op[1], op[2])); out.append(True)
            else: out.append(False)
        else:
            t = op[2]
            while not fits(t, t + op[1]): t += 1
            out.append(t)
    return out
print('cal lesson A', cal(1, [[0,1,4],[0,3,6],[0,4,8],[0,0,1]]))
print('cal lesson B', cal(2, [[0,1,4],[0,3,6],[0,2,5],[0,4,8]]))
print('cal lesson C', cal(1, [[0,9,12],[0,12,15],[2,2,9],[2,3,9],[1,9,12],[2,3,9]]))
# lesson l18 product except self
def pe(nums):
    return [eval('*'.join(str(v) for j, v in enumerate(nums) if j != i) or '1') for i in range(len(nums))]
print(pe([2,3,4,5]), pe([1,2,3,4]), pe([3,0,2]))
# 60-minute plan numbers
print(60-5-25-25, 60-5-2*25-5)
