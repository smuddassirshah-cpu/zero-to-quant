"""Fresh data for research-int homework-4 (answer-check fix pass, 4 Nov 2026).
Run: python3 gen_hw4_data.py <out_dir>  -> rates-gaps.csv, lakes-level.csv, fills-messy.csv
Every file comes from numpy default_rng(seed) and the standard library, so the output is the same on any 2.x NumPy.
Each file stays far below the 256 KB limit for a code widget's data."""
import csv
import os
import sys

import numpy as np

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'


def rates_gaps(seed=2041):
    """200 quotes of a rate, minutes since 08:00 (0 to 479), unsorted, 14 written NA.
    rate = 0.85 + a random walk with step sd 0.0004, rounded to 4 places. No repeated minutes."""
    rng = np.random.default_rng(seed)
    n = 200
    minute = np.sort(rng.choice(np.arange(0, 480), n, replace=False))
    rate = np.round(0.85 + np.cumsum(rng.normal(0, 0.0004, n)), 4)
    rows = [[int(m), f'{r:.4f}'] for m, r in zip(minute, rate)]
    for k in rng.choice(n, 14, replace=False):
        rows[k][1] = 'NA'
    order = rng.permutation(n)
    return ['minute', 'rate'], [rows[i] for i in order]


def lakes_level(seed=2042):
    """9 lakes by 40 years (1 to 40), level = base + slope * year + N(0, 0.12) metres, 3 places,
    and one lake, Tarn, with only 4 years."""
    rng = np.random.default_rng(seed)
    lakes = ['Ard', 'Bala', 'Cree', 'Dee', 'Esk', 'Fyne', 'Gill', 'Hawes', 'Isla']
    slopes = [-0.012, -0.004, 0.0, 0.003, 0.006, 0.009, 0.015, 0.002, -0.008]
    base = np.round(rng.uniform(20, 60, len(lakes)), 1)
    rows = []
    for k, name in enumerate(lakes):
        for yr in range(1, 41):
            rows.append([name, yr, f'{base[k] + slopes[k] * yr + rng.normal(0, 0.12):.3f}'])
    for yr, lv in [(1, 31.2), (2, 31.1), (3, 30.9), (4, 30.8)]:
        rows.append(['Tarn', yr, f'{lv:.3f}'])
    return ['lake', 'year', 'level_m'], rows


def fills_messy(seed=2043):
    """380 fills of one day, then 12 later rows that correct an id and 10 that cancel one.
    Messy text: side in mixed case with spaces, qty like '2k', price like '£12.34'."""
    rng = np.random.default_rng(seed)
    n = 380
    secs = np.sort(rng.integers(34200, 57600, n))
    side = rng.choice(['buy', 'sell'], n)
    qty = rng.integers(1, 40, n) * 50
    price = np.round(12.0 + np.cumsum(rng.normal(0, 0.01, n)), 2)

    def text_side(s):
        return rng.choice([s, s.upper(), s.capitalize(), ' ' + s + ' '])

    def text_qty(q):
        return f'{q // 1000}k' if q % 1000 == 0 and rng.random() < 0.7 else str(q)

    def text_price(p):
        return f'£{p:.2f}' if rng.random() < 0.4 else f'{p:.2f}'

    def clock(s):
        return f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'

    rows = [[i + 1, clock(int(secs[i])), text_side(side[i]), text_qty(int(qty[i])), text_price(price[i]), 'FILLED'] for i in range(n)]
    ids = rng.choice(n, 22, replace=False)
    corr, canc = ids[:12], ids[12:]
    late = []
    for i in corr:
        q2 = int(qty[i]) + 50 * int(rng.integers(1, 5))
        p2 = round(float(price[i]) + float(rng.choice([-0.02, -0.01, 0.01, 0.02])), 2)
        late.append([i + 1, clock(int(secs[i]) + 1), text_side(side[i]), text_qty(q2), text_price(p2), 'FILLED'])
    for i in canc:
        late.append([i + 1, clock(int(secs[i]) + 2), text_side(side[i]), text_qty(int(qty[i])), text_price(price[i]), 'CANCELLED'])
    order = rng.permutation(len(late))
    rows += [late[j] for j in order]
    return ['fill_id', 'time', 'side', 'qty', 'price', 'status'], rows


for name, fn in (('rates-gaps.csv', rates_gaps), ('lakes-level.csv', lakes_level), ('fills-messy.csv', fills_messy)):
    head, rows = fn()
    with open(os.path.join(OUT, name), 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(head)
        w.writerows(rows)
    print(name, len(rows), 'rows')
