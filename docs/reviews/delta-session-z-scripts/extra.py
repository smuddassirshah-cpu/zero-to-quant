import json, time, random
d = json.load(open('app/content/drills/ci-reference-split.json'))
def split_by_reference(sizes, ref):
    lo = 0
    for i in range(len(sizes)):
        if sizes[i] < ref:
            sizes.insert(lo, sizes.pop(i)); lo += 1
    hi = lo
    for i in range(lo, len(sizes)):
        if sizes[i] == ref:
            sizes.insert(hi, sizes.pop(i)); hi += 1
    return (lo, hi)
tot = 0
for k, t in enumerate(d['tests']):
    t0 = time.time(); got = eval(t['call'], {'split_by_reference': split_by_reference}); dt = time.time() - t0; tot += dt
    print('pop/insert t%d %.2fs %s' % (k, dt, got == eval(t['expect'])))
print('total %.2fs' % tot)
# sizes.sort() one-liner passes?
def s2(sizes, ref):
    sizes.sort(); return (sum(x < ref for x in sizes), sum(x <= ref for x in sizes))
print('sort passes all', all(eval(t['call'], {'split_by_reference': s2}) == eval(t['expect']) for t in d['examples'] + d['tests']))
# two-pass (lomuto twice) passes?
def s3(sizes, ref):
    lo = 0
    for i in range(len(sizes)):
        if sizes[i] < ref: sizes[lo], sizes[i] = sizes[i], sizes[lo]; lo += 1
    hi = lo
    for i in range(lo, len(sizes)):
        if sizes[i] == ref: sizes[hi], sizes[i] = sizes[i], sizes[hi]; hi += 1
    return (lo, hi)
print('two-pass passes all', all(eval(t['call'], {'split_by_reference': s3}) == eval(t['expect']) for t in d['examples'] + d['tests']))
# wrong: returns list not tuple
def s4(sizes, ref):
    a, b = s3(sizes, ref); return [a, b]
print('list-return passes', sum(eval(t['call'], {'split_by_reference': s4}) == eval(t['expect']) for t in d['examples'] + d['tests']), 'of', len(d['examples'] + d['tests']))
# wrong: hi returned as count of equal (not boundary)
def s5(sizes, ref):
    a, b = s3(sizes, ref); return (a, b - a)
print('count-return passes', sum(eval(t['call'], {'split_by_reference': s5}) == eval(t['expect']) for t in d['examples'] + d['tests']), 'of', len(d['examples'] + d['tests']))
# wrong: partition unstable variant that mishandles when ref absent? (two-way then hi=lo)
def s6(sizes, ref):
    lo = 0
    for i in range(len(sizes)):
        if sizes[i] < ref: sizes[lo], sizes[i] = sizes[i], sizes[lo]; lo += 1
    return (lo, lo + sizes.count(ref))
print('no-equal-move passes', sum(eval(t['call'], {'split_by_reference': s6}) == eval(t['expect']) for t in d['examples'] + d['tests']), 'of', len(d['examples'] + d['tests']))
# widest banner: does two-pointer with strict > find the widest best pair?
def tp(p):
    i, j = 0, len(p) - 1; best = (0, 0)
    while i < j:
        a = min(p[i], p[j]) * (j - i)
        if a > best[0]: best = (a, j - i)
        if p[i] < p[j]: i += 1
        else: j -= 1
    return best
def br(p):
    best = (0, 0)
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            a = min(p[i], p[j]) * (j - i)
            if a > best[0] or (a == best[0] and a > 0 and j - i > best[1]): best = (a, j - i)
    return best
random.seed(7); bad = 0
for _ in range(20000):
    p = [random.randint(0, 6) for _ in range(random.randint(2, 9))]
    if tp(p) != br(p): bad += 1
print('widest tie-rule mismatches', bad)
# 2^99999 mod 10010 and its sum
v = pow(2, 99999, 10010); print('2s', v, v * 100000)
print('quiet', sorted((c, 'quietoceanaudio'.count(c)) for c in 'aeiou'))
