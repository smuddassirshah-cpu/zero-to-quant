"""research-int/homework-4 h4-quote-at: reader's own sweep solution, shipped
solution, starter and seven reader-planted bugs against every case, with times."""
import random
from harness import item, run, check, finish

_, it = item('research-int', 'homework-4', 'h4-quote-at')
w = it['widget']
cases = w['examples'] + w['tests']

# Reader's own route: clean into sorted lists, then answer the asked seconds in
# sorted order with one moving pointer, and put the answers back in asked order.
mine = '''
def quote_at(quotes, times, max_gap):
    acc = {}
    for s, p in quotes:
        if p is not None:
            a = acc.setdefault(s, [0.0, 0])
            a[0] += p
            a[1] += 1
    xs = sorted(acc)
    ys = [acc[x][0] / acc[x][1] for x in xs]
    out = [None] * len(times)
    if not xs:
        return out
    j = 0
    for k in sorted(range(len(times)), key=times.__getitem__):
        t = times[k]
        while j < len(xs) and xs[j] < t:
            j += 1
        if j < len(xs) and xs[j] == t:
            out[k] = ys[j]
        elif j == 0:
            out[k] = ys[0] if xs[0] - t <= max_gap else None
        elif j == len(xs):
            out[k] = ys[-1] if t - xs[-1] <= max_gap else None
        elif xs[j] - xs[j - 1] <= max_gap:
            w = (t - xs[j - 1]) / (xs[j] - xs[j - 1])
            out[k] = (1 - w) * ys[j - 1] + w * ys[j]
    return out
'''
for name, code in [('shipped solution', w['solution']), ('reader sweep', mine)]:
    res = run(code, w, cases)
    check(all(r[0] for r in res), f'{name} passes all {len(cases)} cases, test 9 in {res[-1][1]:.3f} s')

res = run(w['starter'], w, w['tests'])
check(not any(r[0] for r in res), 'starter fails every hidden test')

# Random cross-check of the two routes on small cases with repeats, cancels and gaps.
ns1, ns2 = {}, {}
exec(w['solution'], ns1)
exec(mine, ns2)
rng = random.Random(7)
agree = True
for _ in range(3000):
    q = [(rng.randrange(0, 40), None if rng.random() < 0.2 else float(rng.randrange(90, 110)))
         for _ in range(rng.randrange(0, 8))]
    ts = [rng.randrange(-15, 55) for _ in range(6)]
    g = rng.randrange(1, 15)
    a, b = ns1['quote_at'](q, ts, g), ns2['quote_at'](q, ts, g)
    if any((x is None) != (y is None) or (x is not None and abs(x - y) > 1e-9) for x, y in zip(a, b)):
        agree = False
        break
check(agree, 'shipped solution and reader sweep agree on 3,000 random small cases')

S = w['solution']
def mut(old, new):
    assert S.count(old) == 1, old
    return S.replace(old, new)

planted = {
    'a cancel still counts in the mean': mut(
        "        if p is None:\n            continue\n        sums[t] = sums.get(t, 0.0) + p\n",
        "        sums[t] = sums.get(t, 0.0) + (p or 0.0)\n        if p is None:\n            continue\n"),
    'gap read as distance to the nearest quote': mut(
        "elif xs[i] - xs[i - 1] > max_gap:",
        "elif min(xs[i] - t, t - xs[i - 1]) > max_gap:"),
    'ends extrapolated, not held': mut(
        "            out.append(ys[0] if xs[0] - t <= max_gap else None)",
        "            out.append((ys[0] + (ys[1] - ys[0]) * (t - xs[0]) / (xs[1] - xs[0]) if len(xs) > 1 else ys[0]) if xs[0] - t <= max_gap else None)"),
    'gap rule checked before an exact hit': mut(
        "        if i < len(xs) and xs[i] == t:",
        "        if 0 < i < len(xs) and xs[i] - xs[i - 1] > max_gap:\n            out.append(None)\n        elif i < len(xs) and xs[i] == t:"),
    'repeated asked seconds answered once': mut(
        "    return out\n", "    return list(dict(zip(times, out)).values())\n"),
    'end hold strict at max_gap': mut(
        "ys[-1] if t - xs[-1] <= max_gap", "ys[-1] if t - xs[-1] < max_gap"),
    'repeats: mean of the first and the last only': mut(
        "        sums[t] = sums.get(t, 0.0) + p\n        counts[t] = counts.get(t, 0) + 1\n",
        "        if t in sums:\n            sums[t] = (first[t] + p)\n            counts[t] = 2\n        else:\n            first[t] = p\n            sums[t], counts[t] = p, 1\n").replace(
        "    sums, counts = {}, {}", "    sums, counts, first = {}, {}, {}"),
}
for name, code in planted.items():
    hid = run(code, w, w['tests'])
    bad = [k + 1 for k, r in enumerate(hid) if not r[0]]
    check(bool(bad), f'planted "{name}" caught by hidden tests {bad}')
finish()
