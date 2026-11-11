"""How deep does a natural recursive solution go on each example and hidden test?
ring bonuses: the remembered recursion need(i) = 1 + max(need(lower neighbour)) is as deep as the
longest strictly falling walk from a trader, which is the largest token count.
stop cascade: a buy that fires the next stop from inside itself is two frames per stop of a cascade.
usage: depth.py <drills dir>"""
import heapq
import json
import os
import sys

d = sys.argv[1]


def bonus_depth(scores):
    n = len(scores)
    tok = [1] * n
    for i in sorted(range(n), key=scores.__getitem__):
        for j in ((i - 1) % n, (i + 1) % n):
            if scores[j] < scores[i] and tok[j] + 1 > tok[i]:
                tok[i] = tok[j] + 1
    return max(tok)


def cascade_depth(text):
    """the same order of work as the recursion, with a loop and a counter of stops fired per event"""
    tokens = text.split()
    n = int(tokens[0])
    asks, stops = [], []
    last = None
    deepest = 0

    def buy(qty):
        nonlocal last
        while qty > 0 and asks:
            best = asks[0]
            take = min(qty, best[2])
            qty -= take
            best[2] -= take
            last = best[0]
            if best[2] == 0:
                heapq.heappop(asks)
    pos = 1
    for seq in range(n):
        kind = tokens[pos]
        chain = 0
        if kind == 'B':
            buy(int(tokens[pos + 1]))
            chain = 1
            pos += 2
        else:
            price, qty = int(tokens[pos + 1]), int(tokens[pos + 2])
            if kind == 'S':
                heapq.heappush(asks, [price, seq, qty])
            else:
                heapq.heappush(stops, (price, seq, qty))
            pos += 3
        while stops and last is not None and stops[0][0] <= last:
            buy(heapq.heappop(stops)[2])
            chain += 1
        deepest = max(deepest, 2 * chain)
    return deepest


for did, fn, f in (('ci-ring-bonuses', 'ring_bonuses', bonus_depth), ('ci-stop-cascade', 'solve_stop_cascade', cascade_depth)):
    j = json.load(open(os.path.join(d, did + '.json')))
    out = []
    for kind in ('examples', 'tests'):
        for i, t in enumerate(j[kind]):
            got = []
            try:
                eval(t['call'], {fn: lambda *a: got.append(f(*a)) or ('' if fn[0] == 's' else 0)})
            except Exception:
                pass
            out.append('%s%d:%d' % (kind[0], i, got[0]))
    print(did, 'frames by test:', ' '.join(out))
