"""Seeded four-option mock generator for mental-pressure level 3 (l9 block, l12 mock, homework drill).

mock_generator(seed, mix) returns a list of (text, options, answer) tuples. The same function, cut down, is the
homework's difficulty-5 solution; exam authors can reuse it for the fixed versions of mock-oa-arith.
Internally every value is a Fraction, so no float ever decides an answer.
"""
import random
from fractions import Fraction as F
from math import gcd

MIX = {"addsub": 15, "mul": 15, "div": 10, "dec": 12, "frac": 10, "pct": 10, "seq": 8}
BLOCK = {"addsub": 4, "mul": 4, "div": 2, "dec": 3, "frac": 3, "pct": 2, "seq": 2}


def terminating(x, places=4):
    x = F(x)
    return (x * 10 ** places).denominator == 1


def near(d, ans):
    """a near miss: positive, different, within a factor of ten of the answer"""
    return d > 0 and d != ans and ans / 10 <= d <= ans * 10


def slips(rng, ans, step):
    """slipped digits: the answer moved by one unit in one of its places"""
    out = [ans + s * step * k for k in (1, 10, 100) for s in (1, -1)]
    rng.shuffle(out)
    return out


def num_text(x):
    x = F(x)
    if x.denominator == 1:
        return f"{x.numerator:,}"
    s = f"{float(x):.6f}".rstrip('0').rstrip('.')
    assert F(s) == x, (s, x)
    return s


def frac_text(x):
    x = F(x)
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def make(rng, kind):
    if kind == "addsub":
        a, b, op = rng.randint(100, 999), rng.randint(12, 999), rng.choice("+-")
        if op == "-" and a < b:
            a, b = b, a
        if a == b:
            b -= 1
        ans = F(a + b) if op == "+" else F(a - b)
        cands = [F(a - b) if op == "+" else F(a + b), ans + rng.choice((10, -10))] + slips(rng, ans, 1)
        text = f"{num_text(a)} {'+' if op == '+' else '−'} {num_text(b)}"
    elif kind == "mul":
        if rng.random() < 2 / 3:
            a, b = rng.randint(12, 99), rng.randint(12, 99)
        else:
            a, b = rng.randint(3, 9), rng.randint(101, 999)
        ans = F(a * b)
        cands = [ans + rng.choice((a, -a)), ans + rng.choice((10, -10))] + slips(rng, ans, 1)
        text = f"{num_text(a)} × {num_text(b)}"
    elif kind == "div":
        b, q = rng.randint(3, 19), rng.randint(12, 99)
        a, ans = b * q, F(q)
        cands = [ans + rng.choice((1, -1)), ans * 10, ans + rng.choice((10, -10))] + slips(rng, ans, 1)
        text = f"{num_text(a)} ÷ {b}"
    elif kind == "dec":
        if rng.random() < 0.5:
            x = F(rng.randint(2, 99), 10)
            y = F(rng.randint(2, 9), 10) if rng.random() < 0.5 else F(rng.randint(2, 9))
            if x.denominator == 1 and y.denominator == 1:
                y = y / 10
            ans = x * y
            rev = x / y
            text = f"{num_text(x)} × {num_text(y)}"
        else:
            y = rng.choice([F(2, 10), F(4, 10), F(5, 10), F(25, 100), F(3, 10), F(6, 10), F(8, 10), F(12, 10), F(25, 10)])
            ans = F(rng.randint(3, 40))
            x = y * ans
            rev = x * y
            text = f"{num_text(x)} ÷ {num_text(y)}"
        step = F(1) if ans.denominator == 1 else F(1, 10 ** len(num_text(ans).split('.')[1]))
        cands = [ans * 10, ans / 10] + ([rev] if terminating(rev) else []) + slips(rng, ans, step)
    elif kind == "frac":
        dens = [2, 3, 4, 5, 6, 8, 10, 12]
        while True:
            q, s = rng.choice(dens), rng.choice(dens)
            p, r = rng.randint(1, q - 1), rng.randint(1, s - 1)
            if gcd(p, q) == 1 and gcd(r, s) == 1 and F(p, q) != F(r, s):
                break
        op = rng.choice("+-")
        if op == "-" and F(p, q) < F(r, s):
            p, q, r, s = r, s, p, q
        ans = F(p, q) + F(r, s) if op == "+" else F(p, q) - F(r, s)
        cands = [F(p, q) - F(r, s) if op == "+" else F(p, q) + F(r, s)]
        if op == "+":
            cands.append(F(p + r, q + s))
        elif q != s and p - r > 0 and q - s > 0:
            cands.append(F(p - r, q - s))
        cands += [F(ans.numerator + 1, ans.denominator), F(ans.numerator - 1, ans.denominator), F(ans.numerator, ans.denominator + 1),
                  F(ans.numerator, max(ans.denominator - 1, 1)), ans * 2, ans / 2, F(ans.numerator + 2, ans.denominator)]
        text = f"{p}/{q} {'+' if op == '+' else '−'} {r}/{s}"
    elif kind == "pct":
        p = rng.choice([F(5), F(10), F(15), F(20), F(25), F(30), F(35), F(40), F(45), F(60), F(75), F(25, 2)])
        n = 8 * rng.randint(5, 125) if p.denominator == 2 else 20 * rng.randint(2, 100)
        ans = p * n / 100
        cands = [(100 - p) * n / 100, ans * 10, ans / 10, (p + 5) * n / 100, (p - 5) * n / 100] + slips(rng, ans, 1)
        text = f"{num_text(p)}% of {num_text(n)}"
    elif kind == "seq":
        style = rng.choice(["arith", "quad", "geom", "affine"])
        if style == "arith":
            a, d = rng.randint(2, 40), rng.choice([-1, 1]) * rng.randint(3, 15)
            if d < 0:
                a += 60
            t = [a + d * i for i in range(5)]
        elif style == "quad":
            a, d, s = rng.randint(1, 12), rng.randint(1, 6), rng.randint(1, 4)
            t, diff = [a], d
            for _ in range(4):
                t.append(t[-1] + diff)
                diff += s
        elif style == "geom":
            a, r = rng.randint(2, 7), rng.choice([2, 3])
            t = [a * r ** i for i in range(5)]
        else:
            a, c = rng.randint(2, 9), rng.choice([-1, 1]) * rng.randint(1, 5)
            if a + c <= 1:
                c = abs(c)
            t = [a]
            for _ in range(4):
                t.append(2 * t[-1] + c)
        shown, ans = t[:4] if style in ("arith", "geom") else t[:5], None
        nxt = t[4] if style in ("arith", "geom") else None
        if style in ("arith", "geom"):
            ans = F(t[4])
        else:
            diff_last = t[4] - t[3]
            if style == "quad":
                ans = F(t[4] + diff_last + s)
            else:
                ans = F(2 * t[4] + c)
        last_d = shown[-1] - shown[-2]
        cands = [F(shown[-1] + last_d), ans + rng.choice((1, -1)), ans + last_d, ans - rng.choice((2, 3))] + slips(rng, ans, 1)
        text = ", ".join(num_text(v) for v in shown) + ", ?"
    else:
        raise ValueError(kind)
    cands += [ans * 2, ans / 2, ans + 1, ans + 2, ans * 3]
    out = []
    for c in cands:
        c = F(c)
        if near(c, ans) and c not in out and (kind == "frac" or terminating(c)):
            out.append(c)
        if len(out) == 3:
            break
    assert len(out) == 3, (kind, text, ans, cands)
    return text, ans, out


def generate(seed, mix=None):
    """internal form: (kind, text, options as Fractions, answer Fraction, letter)"""
    mix = MIX if mix is None else mix
    rng = random.Random(seed)
    kinds = [k for k in mix for _ in range(mix[k])]
    rng.shuffle(kinds)
    items, seen = [], set()
    for k in kinds:
        while True:
            text, ans, dis = make(rng, k)
            if text not in seen:
                break
        seen.add(text)
        opts = [ans] + dis
        rng.shuffle(opts)
        items.append((k, text, opts, ans, "ABCD"[opts.index(ans)]))
    return items


def plain(x):
    x = F(x)
    return int(x) if x.denominator == 1 else float(x)


def mock_generator(seed, mix=None):
    out = []
    for k, text, opts, ans, _ in generate(seed, mix):
        conv = (lambda v: v) if k == "frac" else plain
        out.append((text, [conv(o) for o in opts], conv(ans)))
    return out


def show(kind, x):
    return frac_text(x) if kind == "frac" else num_text(x)


def row_text(kind, text, opts):
    return f"{text}: " + "  ".join(f"**{L}** {show(kind, o)}" for L, o in zip("ABCD", opts))


if __name__ == "__main__":
    for i, (k, t, o, a, L) in enumerate(generate(80), 1):
        print(f"{i:2d} {k:6s} {t:24s} " + "  ".join(f"{l} {show(k, v)}" for l, v in zip("ABCD", o)) + f"   -> {L} ({show(k, a)})")
