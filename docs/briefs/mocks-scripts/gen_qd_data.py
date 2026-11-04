"""mock-oa-quant-data: the three data files, made with a pure-Python generator (no numpy, so the bytes never depend
on a library version).  Run: python3 -I gen_qd_data.py   (writes ./data/qd-*.csv and prints size and SHA-256).

The mock author copies the three files to app/content/data/qd/ (each is far below the 256 KB cap) and may copy this
script to app/tools/gen-qd-data.py.  Deterministic: a 32-bit linear congruential generator, fixed seeds.
"""
import datetime, hashlib, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


class Rng:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF

    def u(self):
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return (self.s + 0.5) / 4294967296.0

    def n(self):  # about N(0, 1): twelve uniforms minus six
        return sum(self.u() for _ in range(12)) - 6.0

    def shuffle(self, xs):
        for i in range(len(xs) - 1, 0, -1):
            j = int(self.u() * (i + 1))
            xs[i], xs[j] = xs[j], xs[i]


def weekdays(start, count):
    d, out = start, []
    while len(out) < count:
        if d.weekday() < 5:
            out.append(d.isoformat())
        d += datetime.timedelta(days=1)
    return out


def make_prices():
    r = Rng(2601)
    days = weekdays(datetime.date(2025, 1, 2), 260)
    spec = [("KAPPA", 50.0, 0.011), ("LAMBDA", 120.0, 0.016), ("MU", 8.5, 0.022)]
    rows = []
    for tick, p0, sd in spec:
        p = p0
        for d in days:
            p *= math.exp(0.0003 + sd * r.n())
            rows.append([d, tick, f"{p:.2f}"])
    # planted problems: 7 blank closes, 3 exact repeats, then shuffled rows
    blanks = [37, 140, 301, 398, 455, 560, 702]
    for i in blanks:
        rows[i][2] = ""
    dups = [rows[90][:], rows[333][:], rows[610][:]]
    rows += dups
    r.shuffle(rows)
    return "date,ticker,close\n" + "".join(",".join(x) + "\n" for x in rows)


def make_pair():
    r = Rng(2602)
    days = weekdays(datetime.date(2024, 1, 2), 520)
    rows = []
    N = len(days)
    for t, d in enumerate(days):
        idx = 0.0004 + 0.010 * r.n()
        beta = 0.8 + 0.6 * t / (N - 1)
        ast = 0.0001 + beta * idx + 0.006 * r.n()
        rows.append([d, ast, idx])
    # three data-entry errors: a return typed as a whole percent in the asset column
    rows[100][1], rows[250][1], rows[400][1] = 0.31, -0.28, 0.35
    return "date,asset,mkt\n" + "".join(f"{d},{a:.6f},{i:.6f}\n" for d, a, i in rows)


def make_signal():
    r = Rng(2603)
    days = weekdays(datetime.date(2022, 1, 3), 800)
    x1 = [r.n() for _ in days]
    x2 = [r.n() for _ in days]
    ret = []
    for t in range(len(days)):
        if t == 0:
            ret.append(0.0002 + 0.010 * r.n())
        else:
            ret.append(0.0002 + 0.0020 * x1[t - 1] - 0.0015 * x2[t - 1] + 0.010 * r.n())
    return "date,x1,x2,ret\n" + "".join(f"{d},{a:.6f},{b:.6f},{c:.6f}\n" for d, a, b, c in zip(days, x1, x2, ret))


FILES = {"qd-prices.csv": make_prices, "qd-pair.csv": make_pair, "qd-signal.csv": make_signal}

if __name__ == "__main__":
    os.makedirs(DATA, exist_ok=True)
    for name, fn in FILES.items():
        text = fn()
        path = os.path.join(DATA, name)
        with open(path, "w", newline="") as f:
            f.write(text)
        b = text.encode()
        assert len(b) < 262144
        print(f"{name}: {len(b)} bytes, {text.count(chr(10)) - 1} rows, sha256 {hashlib.sha256(b).hexdigest()[:16]}")
