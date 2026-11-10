"""ci-live-median: the model (two heaps, lazy cancels) against one sorted list
(insort and del), on inputs of the shape of the two large hidden tests, at three sizes.

Runs as it stands in CPython, and in Pyodide through pyodide_time.mjs.
The model is pasted from the drill file (Pyodide sees no repo).
"""
import bisect
import heapq
import time


def model(text):
    tokens = text.split()
    q = int(tokens[0]) if tokens else 0
    low, high = [], []
    gone_low, gone_high = {}, {}
    n_low = n_high = 0

    def tidy(heap, gone, sign):
        while heap and gone.get(sign * heap[0]):
            gone[sign * heapq.heappop(heap)] -= 1

    records = []
    for i in range(q):
        op, x = tokens[1 + 2 * i], int(tokens[2 + 2 * i])
        tidy(low, gone_low, -1)
        if op == '+':
            if n_low and x <= -low[0]:
                heapq.heappush(low, -x)
                n_low += 1
            else:
                heapq.heappush(high, x)
                n_high += 1
        elif n_low and x <= -low[0]:
            gone_low[x] = gone_low.get(x, 0) + 1
            n_low -= 1
        else:
            gone_high[x] = gone_high.get(x, 0) + 1
            n_high -= 1
        if n_low > n_high + 1:
            tidy(low, gone_low, -1)
            heapq.heappush(high, -heapq.heappop(low))
            n_low -= 1
            n_high += 1
        elif n_low < n_high:
            tidy(high, gone_high, 1)
            heapq.heappush(low, -heapq.heappop(high))
            n_low += 1
            n_high -= 1
        tidy(low, gone_low, -1)
        records.append(str(-low[0]) if n_low else '-')
    return ' '.join(records)


def insort(text):
    tokens = text.split()
    q = int(tokens[0]) if tokens else 0
    live, out = [], []
    for i in range(q):
        x = int(tokens[2 + 2 * i])
        if tokens[1 + 2 * i] == '+':
            bisect.insort(live, x)
        else:
            del live[bisect.bisect_left(live, x)]
        out.append(str(live[(len(live) + 1) // 2 - 1]) if live else '-')
    return ' '.join(out)


def t10(q):  # hidden test 10: three quarters arrive, then a quarter are cancelled
    a = q * 3 // 4
    return '%d\n' % q + '\n'.join(
        '+ %d' % (i * 7919 % 1000003) if i < a else '- %d' % ((i - a) * 3 * 7919 % 1000003)
        for i in range(q)) + '\n'


def t11(q):  # hidden test 11: two arrive, one is cancelled, sizes below 1,000
    return '%d\n' % q + '\n'.join(
        '- %d' % ((i - 2) * 37 % 1000) if i % 3 == 2 else '+ %d' % (i * 37 % 1000)
        for i in range(q)) + '\n'


for name, make in (('test 10 shape', t10), ('test 11 shape', t11)):
    for q in (200000, 400000, 600000):
        text = make(q)
        t = time.time()
        a = model(text)
        tm = time.time() - t
        t = time.time()
        b = insort(text)
        ti = time.time() - t
        print('%s q=%d: model %.2f s, sorted list %.2f s, same answer %s' % (name, q, tm, ti, a == b))
