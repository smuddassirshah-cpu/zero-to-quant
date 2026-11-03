"""Shared pieces for mental-pressure level 3: four-option tables and the working for each generated question."""
import sys, re, math
sys.path.insert(0, '/tmp/claude-0/-home-user-zero-to-quant/f2cb57c1-0333-5a7c-8b45-5ff551a039e9/scratchpad/mental-pressure-3')
from fractions import Fraction as F
from h import *
from mockgen import generate, show, num_text, frac_text, MIX, BLOCK


def n(x):
    return num_text(x)


def parse_num(s):
    return F(s.replace(',', ''))


def working(kind, text, ans):
    """one line of mental working, checked against the answer"""
    if kind == "addsub":
        a, op, b = re.match(r"([\d,]+) ([+−]) ([\d,]+)", text).groups()
        a, b = int(a.replace(',', '')), int(b.replace(',', ''))
        if op == "+":
            h = b // 100 * 100
            if h:
                mid = a + h
                assert mid + (b - h) == ans
                return f"Left to right: {n(a)} + {n(h)} = {n(mid)}, then + {b - h} = {n(ans)}."
            t = b // 10 * 10
            assert a + t + b % 10 == ans
            return f"{n(a)} + {t} = {n(a + t)}, then + {b % 10} = {n(ans)}."
        up = -(-b // 10) * 10
        if up == b:
            assert a - b == ans
            return f"{n(a)} − {n(b)} = {n(ans)}."
        assert a - up + (up - b) == ans
        return f"Round up: {n(a)} − {n(up)} = {n(a - up)}, then add back {up - b}: {n(ans)}."
    if kind == "mul":
        a, b = [int(x.replace(',', '')) for x in text.split(' × ')]
        if a >= 10:
            t, u = b // 10 * 10, b % 10
            assert a * t + a * u == ans
            return f"{a} × {b} = {a} × {t} + {a} × {u} = {n(a * t)} + {n(a * u)} = {n(ans)}." if u else f"{a} × {b} = {n(ans)}."
        h, t, u = b // 100 * 100, b // 10 % 10 * 10, b % 10
        parts = [a * h, a * t, a * u]
        assert sum(parts) == ans
        return f"{a} × {n(b)} = " + " + ".join(n(p) for p in parts if p) + f" = {n(ans)}."
    if kind == "div":
        a, b = [int(x.replace(',', '')) for x in text.split(' ÷ ')]
        assert b * ans == a
        return f"Missing multiplication: {b} × {n(ans)} = {n(a)}, so {n(ans)}."
    if kind == "dec":
        if ' × ' in text:
            x, y = [parse_num(v) for v in text.split(' × ')]
            dx = len(n(x).split('.')[1]) if '.' in n(x) else 0
            dy = len(n(y).split('.')[1]) if '.' in n(y) else 0
            ix, iy = int(x * 10 ** dx), int(y * 10 ** dy)
            assert F(ix * iy, 10 ** (dx + dy)) == ans
            pl = dx + dy
            return f"{ix} × {iy} = {n(ix * iy)}; {pl} decimal place{'s' if pl > 1 else ''} in all: {n(ans)}."
        x, y = [parse_num(v) for v in text.split(' ÷ ')]
        dy = len(n(y).split('.')[1]) if '.' in n(y) else 0
        sx, sy = x * 10 ** dy, y * 10 ** dy
        assert sx / sy == ans
        return f"Move both points {dy} place{'s' if dy > 1 else ''}: {n(sx)} ÷ {n(sy)} = {n(ans)}."
    if kind == "frac":
        p, q, op, r, s = re.match(r"(\d+)/(\d+) ([+−]) (\d+)/(\d+)", text).groups()
        p, q, r, s = map(int, (p, q, r, s))
        L = q * s // math.gcd(q, s)
        a1, a2 = p * L // q, r * L // s
        top = a1 + a2 if op == "+" else a1 - a2
        assert F(top, L) == ans
        tail = "" if F(top, L).denominator == L else f" = {frac_text(ans)}"
        return f"Over {L}: {a1}/{L} {op} {a2}/{L} = {top}/{L}{tail}."
    if kind == "pct":
        p, m = re.match(r"([\d.]+)% of ([\d,]+)", text).groups()
        p, m = F(p), parse_num(m)
        ten = m / 10
        assert p * m / 100 == ans
        ways = {F(5): f"10% is {n(ten)}, so 5% is half: {n(ans)}.",
                F(10): f"10%: move the point one place: {n(ans)}.",
                F(15): f"10% is {n(ten)} and 5% is {n(ten / 2)}: {n(ans)}.",
                F(20): f"10% is {n(ten)}, doubled: {n(ans)}.",
                F(25): f"A quarter of {n(m)}: {n(ans)}.",
                F(30): f"10% is {n(ten)}, times 3: {n(ans)}.",
                F(35): f"30% is {n(3 * ten)} and 5% is {n(ten / 2)}: {n(ans)}.",
                F(40): f"10% is {n(ten)}, times 4: {n(ans)}.",
                F(45): f"Half is {n(m / 2)}, less 5% ({n(ten / 2)}): {n(ans)}.",
                F(60): f"10% is {n(ten)}, times 6: {n(ans)}.",
                F(75): f"Three quarters of {n(m)}: {n(ans)}.",
                F(25, 2): f"12.5% is an eighth: {n(m)} ÷ 8 = {n(ans)}."}
        return ways[p]
    if kind == "seq":
        t = [int(v.replace(',', '')) for v in text[:-3].split(', ')]
        d = [b - a for a, b in zip(t, t[1:])]
        if len(set(d)) == 1:
            assert t[-1] + d[0] == ans
            return f"The difference is {('+' if d[0] > 0 else '−') + str(abs(d[0]))} each time: {n(t[-1])} {'+' if d[0] > 0 else '−'} {abs(d[0])} = {n(ans)}."
        d2 = [b - a for a, b in zip(d, d[1:])]
        if len(set(d2)) == 1:
            nd = d[-1] + d2[0]
            assert t[-1] + nd == ans
            return f"Differences " + ", ".join(map(str, d)) + f" grow by {d2[0]}: next {nd}, so {n(ans)}."
        if all(b == t[1] // t[0] * a for a, b in zip(t, t[1:])):
            r = t[1] // t[0]
            assert t[-1] * r == ans
            return f"Times {r} each time: {n(t[-1])} × {r} = {n(ans)}."
        c = t[1] - 2 * t[0]
        assert all(b == 2 * a + c for a, b in zip(t, t[1:])) and 2 * t[-1] + c == ans
        return f"Double and {'add' if c > 0 else 'take'} {abs(c)}: 2 × {n(t[-1])} {'+' if c > 0 else '−'} {abs(c)} = {n(ans)}."
    raise ValueError(kind)


def kind_is_seq(k):
    return k == "seq"


def four_option_table(items, start=1, letter_col="Letter"):
    """table widget rows (Q, question and options, letter cell) and byKey lines for each letter cell"""
    rows, bk = [], {}
    for i, (k, text, opts, ans, L) in enumerate(items):
        opt_txt = " · ".join(f"**{x}**\u00a0{show(k, o)}" for x, o in zip("ABCD", opts))
        qt = text if kind_is_seq(k) else text.replace(" ", "\u00a0")
        rows.append([f"Q{start + i}: {qt}", opt_txt, cell(L, placeholder="A to D")])
        bk[f"r{i}c2"] = f"Q{start + i}: {working(k, text, ans)} That is {L}."
    return {"kind": "table", "columns": ["Question", "Options", letter_col], "rows": rows}, bk


def block_line(items, start=1):
    Ls = [x[4] for x in items]
    parts = []
    for j in range(0, len(Ls), 5):
        parts.append(f"Q{start + j} to Q{start + j + len(Ls[j:j + 5]) - 1}: " + ", ".join(Ls[j:j + 5]))
    return ". ".join(parts)


def numline_block(b):
    """an 8-minute line with this block's two minutes marked"""
    ints = [{"id": f"i{b}", "from": 2 * (b - 1), "to": 2 * b, "label": f"Block {b}", "colour": 2, "row": 1}]
    pts = [{"id": f"k{b}", "x": 2 * b, "label": f"Q{20 * b}"}]
    return {"kind": "number-line", "params": {"min": 0, "max": 8, "step": 1, "labels": 1},
            "state": {"intervals": ints, "points": pts, "caption": f"Minutes. Block {b} runs from {2 * (b - 1)}:00 to {2 * b}:00."}}
