"""Pack 8 extras. Usage (repo root): python3 extra_8.py
Plain brute forces for the eight drills whose tests or examples changed in the fix
pass, on every example and hidden test small enough, then against the model on random
small inputs."""
import itertools
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brute_lib import run_brutes  # noqa: E402


def b_checks(jobs):
    if not jobs:
        return 0
    minutes = sorted({m for s, e, k in jobs for m in range(s, e + 1)})
    for size in range(0, len(minutes) + 1):
        for pick in itertools.combinations(minutes, size):
            if all(sum(1 for m in pick if s <= m <= e) >= k for s, e, k in jobs):
                return size


def b_first_fit(bookings, start, length):
    busy = set()
    for s, e in bookings:
        busy.update(range(s, e))
    slot = start
    while any(m in busy for m in range(slot, slot + length)):
        slot += 1
    busy.update(range(slot, slot + length))
    # touching bookings join, so the joined list is the maximal runs of busy minutes,
    # except that two runs can only be apart if a free minute lies between them
    merged = []
    for m in sorted(busy):
        if merged and merged[-1][1] == m:
            merged[-1][1] = m + 1
        else:
            merged.append([m, m + 1])
    return [slot, merged]


def b_kbits(queries):
    return [sum(1 for x in range(lo, hi + 1) if bin(x).count('1') == k) for lo, hi, k in queries]


def b_run_days(tasks, rest):
    ready = {}
    day = 0
    out = []
    for m in tasks:
        day += 1
        while day < ready.get(m, 0):
            day += 1
        out.append(day)
        ready[m] = day + rest.get(m, 0) + 1
    return out


def b_hops(stones, lo, hi):
    n = len(stones)
    dist = [None] * n
    dist[0] = 0
    for j in range(1, n):
        if stones[j] == '.':
            c = [dist[i] for i in range(max(0, j - hi), j - lo + 1) if i >= 0 and dist[i] is not None]
            if c:
                dist[j] = min(c) + 1
    return -1 if dist[-1] is None else dist[-1]


def b_cascade(text):
    rng = random.Random(len(text))
    lines = [ln.split() for ln in text.split('\n') if ln.strip()]
    n = int(lines[0][0])
    book, stops = [], []
    last, total = None, 0
    out = []

    def buy(q):
        nonlocal last, total
        while q and book:
            i = min(range(len(book)), key=lambda t: (book[t][0], t))
            take = min(q, book[i][1])
            book[i][1] -= take
            q -= take
            total += take
            last = book[i][0]
            if book[i][1] == 0:
                book.pop(i)

    for ev in lines[1:1 + n]:
        if ev[0] == 'S':
            book.append([int(ev[1]), int(ev[2])])
        elif ev[0] == 'B':
            buy(int(ev[1]))
        else:
            stops.append((int(ev[1]), int(ev[2])))
        while True:
            ready = [i for i, s in enumerate(stops) if last is not None and s[0] <= last]
            if not ready:
                break
            p, q = stops.pop(rng.choice(ready))      # any ready stop, as the brief allows
            buy(q)
        out.append('- 0' if last is None else '%d %d' % (last, total))
    return '\n'.join(out)


def b_switches(switches, target):
    want = int(target, 2)
    for size in range(len(switches) + 1):
        for idx in itertools.combinations(range(len(switches)), size):
            x = 0
            for i in idx:
                x ^= int(switches[i], 2)
            if x == want:
                return list(idx)
    return None


def b_rooms(meetings, clean):
    free_at = []
    out = [None] * len(meetings)
    for i in sorted(range(len(meetings)), key=lambda i: (meetings[i][0], i)):
        s, e = meetings[i]
        for r, f in enumerate(free_at):
            if f <= s:
                break
        else:
            r = len(free_at)
            free_at.append(0)
        free_at[r] = e + clean
        out[i] = r
    return out


def _gen_jobs(r):
    jobs = []
    for _ in range(r.randint(0, 4)):
        s = r.randint(0, 7)
        e = r.randint(s, min(s + 5, 9))
        jobs.append([s, e, r.randint(1, min(5, e - s + 1))])
    return (jobs,)


def _gen_fit(r):
    t, out = 0, []
    for _ in range(r.randint(0, 5)):
        s = t + r.randint(0, 3)
        e = s + r.randint(1, 3)
        out.append([s, e])
        t = e
    return out, r.randint(0, t + 2), r.randint(1, 4)


def _gen_cascade(r):
    ev = []
    for _ in range(r.randint(1, 9)):
        k = r.choice('SSBBT')
        if k == 'S':
            ev.append('S %d %d' % (r.randint(1, 6), r.randint(1, 3)))
        elif k == 'B':
            ev.append('B %d' % r.randint(1, 4))
        else:
            ev.append('T %d %d' % (r.randint(1, 6), r.randint(1, 3)))
    return ('%d\n%s\n' % (len(ev), '\n'.join(ev)),)


def _gen_hops(r):
    n = r.randint(1, 12)
    s = '.' + ''.join(r.choice('..~') for _ in range(max(0, n - 2))) + ('.' if n > 1 else '')
    lo = r.randint(1, len(s))
    return s, lo, r.randint(lo, len(s))


def _gen_sw(r):
    w = r.randint(1, 4)
    return ([''.join(r.choice('01') for _ in range(w)) for _ in range(r.randint(0, 5))],
            ''.join(r.choice('01') for _ in range(w)))


BRUTES = {
    'ci-double-checks': (b_checks, lambda a: len({m for s, e, k in a[0] for m in range(s, min(e, s + 40) + 1)}) <= 16
                         and all(e - s < 40 for s, e, k in a[0]), _gen_jobs, 600),
    'ci-first-fit-slot': (b_first_fit, lambda a: len(a[0]) <= 10 and a[1] + a[2] <= 200
                          and all(e <= 200 for s, e in a[0]), _gen_fit),
    'ci-k-bit-count': (b_kbits, lambda a: all(hi - lo <= 5000 for lo, hi, k in a[0]) and len(a[0]) <= 5,
                       lambda r: ([(lambda lo: [lo, lo + r.randint(0, 60), r.randint(0, 7)])(r.randint(0, 200))
                                   for _ in range(r.randint(1, 3))],)),
    'ci-rest-days': (b_run_days, lambda a: len(a[0]) <= 20 and all(v <= 50 for v in a[1].values()),
                     lambda r: ([r.choice(['a', 'b', 'c']) for _ in range(r.randint(0, 8))],
                                {m: r.randint(0, 4) for m in r.sample(['a', 'b', 'c', 'd'], r.randint(0, 4))})),
    'ci-stone-hops': (b_hops, lambda a: len(a[0]) <= 2000, _gen_hops),
    'ci-stop-cascade': (b_cascade, lambda a: len(a[0]) <= 400, _gen_cascade),
    'ci-switch-panel': (b_switches, lambda a: True, _gen_sw),
    'ci-room-numbers': (b_rooms, lambda a: len(a[0]) <= 2000,
                        lambda r: ([(lambda s: [s, s + r.randint(1, 6)])(r.randint(0, 12))
                                    for _ in range(r.randint(0, 7))], r.randint(0, 3))),
}

sys.exit(1 if run_brutes(BRUTES, 808) else 0)
