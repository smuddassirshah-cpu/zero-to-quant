"""Twin of @zq/mathcore/expr: the expression language's text, grammar, values and work budget.

Written from the plain-language specification alone (docs/ARCHITECTURE.md 5.15, with the grammar's working paper
docs/blueprint/work/widgets-calc-linalg.md 2.3 as background), without reading the TypeScript or the twin this
file replaces (CLAUDE.md hard rule 4). Decision notes:
- A hand-written scanner and recursive-descent parser; nothing here calls eval, exec, compile or ast. Runs of unary
  minus and chains of `+ -`, `* /` and `^` are loops, so recursion follows bracket depth (at most 32) and a legal
  source of 999 minuses or 499 carets parses and evaluates within CPython's default recursion limit.
- Values are Python floats, IEEE-754 doubles. `+ - *` and `/` by a non-zero are CPython's float operations, which
  are IEEE's correctly rounded ones [recalled]. Every other value that is not exact by construction is mpmath at 50
  digits (169 bits) rounded once to the nearest double, ties to even, by the integer arithmetic of `round_ratio`,
  which also gives subnormals and overflow: no NumPy, SciPy or platform libm. `abs sign floor ceil min max` are
  exact by construction, and the special values of the spec and C99 Annex F are written out, not left to mpmath,
  which has no signed zero.
- A literal's value is its exact rational rounded by `round_ratio`, not CPython's float(); the tests check the two
  agree, so the literal rule has two implementations.
- `^`: an integer power whose exact value has at most 4,096 bits is computed exactly. Otherwise mpmath, and a
  result within 2^-100 ulp of a half-ulp boundary is tested for an exact tie: for y = a/2^k the base's odd part
  must be a 2^k-th power, so `(w^4)^1.25` for an odd w near 2^10.7 is exactly halfway between two doubles, which
  169 bits of exp(y ln x) cannot settle alone. A near tie that is not exact keeps the side mpmath's value lies
  on; that value lands exactly on the half only if a^y lies within about 2^-115 ulp of it. Elsewhere a near tie
  closer than mpmath's error is assumed not to occur: a transcendental value at a double is never an exact tie,
  and the hardest elementary-function cases in double precision need about 120 bits [recalled: Lefevre and
  Muller's searches]; for `^` off its exact ties and for erf and Phi no such table exists, so there it is
  [inferred].
- Functions far into a tail return their limit without mpmath (`exp` beyond 1000, `tanh` beyond 40, `erf` beyond
  10, `Phi` and `phi` beyond 40, `sinh` and `cosh` beyond 1000): each limit is the correctly rounded value there,
  and the cut keeps mpmath away from exponents of a thousand digits.
- A sum that cannot pay ends the evaluation with NaN at once. The spec makes that sum NaN, and NaN reaches the top
  through every operator, function, `if` and sum, so what is left cannot change the value.
- The counter of `sum(k, lo, hi, term)` is the integer lo + i as a double, so it is +0 when lo is -0: the
  counter's values are integers, which have no signed zero (spec 4, decided by the main session).

The golden file, packages/mathcore/test/expr.golden.jsonl, holds one JSON object per line: `src` and `scope`, then
either `error` ("parse" for a refused source, "scope" for a free variable without a number) or `free` (the free
variables in order of first appearance), `value` (a number, or "nan", "inf", "-inf") and `exact` (no `^` and no
function of INEXACT, so the TypeScript must match to the bit; otherwise it may differ by a relative 1e-12 on finite
non-zero values). Hand-picked lines cover every rule of the spec; seeded random lines (`random.Random` seeded with
the module name) add exact trees, inexact calls kept clear of the tolerance's edges, and one-character mutations of
valid sources. Every erf call a line makes receives an argument of magnitude at most 2 and every Phi call one of at
most 2.8, or an infinity, a zero or NaN, because the parity test's stand-in table is accurate only there (spec 6); the
twin's own erf and Phi are correctly rounded everywhere. From the repository root, rewrite the file with:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.expr
"""

from __future__ import annotations

import json
import math
import operator
import random
from collections.abc import Callable, Mapping
from functools import cache
from pathlib import Path

import mpmath

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "expr.golden.jsonl"

MAX_LENGTH = 1000
MAX_DIGITS = 20
MAX_DEPTH = 32
BUDGET = 1_000_000
MAX_SAFE = 2**53 - 1
EXACT_POWER_BITS = 4096

MP = mpmath.MPContext()
MP.dps = 50

INF = math.inf
NAN = math.nan

WHITE = frozenset(" \t\n\r")
DIGITS = frozenset("0123456789")
LETTERS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
NAME_CHARS = LETTERS | DIGITS | {"_"}
SINGLES = frozenset("+-*/^(),")
RELATIONS: dict[str, Callable[[float, float], bool]] = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
}
ONE_ARG = (
    "sin cos tan asin acos atan sinh cosh tanh exp ln log10 sqrt cbrt abs sign floor ceil Phi phi erf".split()
)
FUNCTIONS = frozenset(ONE_ARG) | {"atan2", "min", "max"}
CALLS = FUNCTIONS | {"if", "sum"}
INEXACT = frozenset("sin cos tan asin acos atan sinh cosh tanh exp ln log10 cbrt Phi phi erf atan2".split())


class ParseError(ValueError):
    """The source is not in the language (spec sections 1 and 2)."""


class ScopeError(ValueError):
    """A free variable has no number in the scope (spec section 3)."""


class _Spent(Exception):
    """A sum could not pay from what is left of the budget; the evaluation's value is NaN."""


# Rounding.


def round_ratio(negative: bool, num: int, den: int = 1, exp2: int = 0) -> float:
    """The double nearest (-1)^negative * num / den * 2^exp2, for num >= 0 and den > 0, ties to even: an infinity
    from 2^1024 - 2^970 up and a signed zero up to half the smallest subnormal."""
    if num == 0:
        return -0.0 if negative else 0.0
    e = num.bit_length() - den.bit_length()
    if (num << -e if e < 0 else num) < (den << e if e > 0 else den):
        e -= 1
    e += exp2  # 2^e <= magnitude < 2^(e + 1)
    if e >= 1024:
        magnitude = INF
    elif e < -1075:
        magnitude = 0.0
    else:
        unit = max(e - 52, -1074)  # the exponent of one ulp at this magnitude
        shift = exp2 - unit
        n, d = (num << shift, den) if shift >= 0 else (num, den << -shift)
        q, r = divmod(n, d)
        if 2 * r > d or (2 * r == d and q & 1):
            q += 1
        magnitude = INF if q.bit_length() + unit > 1024 else math.ldexp(q, unit)
    return -magnitude if negative else magnitude


def nearest(v: mpmath.mpf) -> float:
    """The double nearest a finite mpmath value, ties to even. Every caller passes an argument at which its
    function is finite, so mpmath's inf and nan (the values with a negative bit count) mean a bug here."""
    sign, man, exp, bc = v._mpf_
    if bc < 0:
        raise ValueError(f"mpmath returned {v} where a finite value was due")
    return round_ratio(bool(sign), int(man), 1, int(exp))


def _odd_part(a: float) -> tuple[int, int]:
    """(X, F) with |a| = X * 2^F and X odd, for finite non-zero a."""
    n, d = abs(a).as_integer_ratio()
    zeros = (n & -n).bit_length() - 1
    return n >> zeros, zeros - (d.bit_length() - 1)


PI = nearest(MP.pi)
HALF_PI = nearest(MP.pi / 2)
QUARTER_PI = nearest(MP.pi / 4)
THREE_QUARTERS_PI = nearest(3 * MP.pi / 4)
CONSTANTS = {"pi": PI, "e": nearest(MP.e)}


# Functions. Each takes and returns doubles; a NaN argument gives NaN.


def _mp(f: Callable[[mpmath.mpf], mpmath.mpf], x: float) -> float:
    return nearest(f(MP.mpf(x)))


def _negative(x: float) -> bool:
    return math.copysign(1.0, x) < 0


def _sin(x: float) -> float:
    return NAN if not math.isfinite(x) else x if x == 0 else _mp(MP.sin, x)


def _cos(x: float) -> float:
    return NAN if not math.isfinite(x) else 1.0 if x == 0 else _mp(MP.cos, x)


def _tan(x: float) -> float:
    return NAN if not math.isfinite(x) else x if x == 0 else _mp(MP.tan, x)


def _asin(x: float) -> float:
    return NAN if not abs(x) <= 1 else x if x == 0 else _mp(MP.asin, x)


def _acos(x: float) -> float:
    return NAN if not abs(x) <= 1 else _mp(MP.acos, x)


def _atan(x: float) -> float:
    if math.isinf(x):
        return math.copysign(HALF_PI, x)
    return x if x == 0 or x != x else _mp(MP.atan, x)


def _sinh(x: float) -> float:
    if x == 0 or not math.isfinite(x):
        return x
    return math.copysign(INF, x) if abs(x) > 1000 else _mp(MP.sinh, x)


def _cosh(x: float) -> float:
    return NAN if x != x else INF if abs(x) > 1000 else 1.0 if x == 0 else _mp(MP.cosh, x)


def _tanh(x: float) -> float:
    return x if x == 0 or x != x else math.copysign(1.0, x) if abs(x) > 40 else _mp(MP.tanh, x)


def _exp(x: float) -> float:
    if x != x:
        return NAN
    return INF if x > 1000 else 0.0 if x < -1000 else 1.0 if x == 0 else _mp(MP.exp, x)


def _ln(x: float) -> float:
    return NAN if not x > 0 else x if math.isinf(x) else _mp(MP.log, x)


def _log10(x: float) -> float:
    return NAN if not x > 0 else x if math.isinf(x) else _mp(MP.log10, x)


def _sqrt(x: float) -> float:
    return NAN if not x >= 0 else x if x == 0 or math.isinf(x) else _mp(MP.sqrt, x)


def _cbrt(x: float) -> float:
    return x if x == 0 or not math.isfinite(x) else math.copysign(_mp(MP.cbrt, abs(x)), x)


def _sign(x: float) -> float:
    return x if x == 0 or x != x else math.copysign(1.0, x)


def _floor(x: float) -> float:
    if x == 0 or not math.isfinite(x):
        return x
    n, d = x.as_integer_ratio()
    return float(n // d)


def _ceil(x: float) -> float:
    if x == 0 or not math.isfinite(x):
        return x
    n, d = x.as_integer_ratio()
    c = -(-n // d)
    return float(c) if c else -0.0


def _Phi(x: float) -> float:
    if x != x:
        return NAN
    if abs(x) > 40:
        return 1.0 if x > 0 else 0.0
    return nearest(MP.erfc(-MP.mpf(x) / MP.sqrt(2)) / 2)


def _phi(x: float) -> float:
    if x != x:
        return NAN
    if abs(x) > 40:
        return 0.0
    v = MP.mpf(x)
    return nearest(MP.exp(-v * v / 2) / MP.sqrt(2 * MP.pi))


def _erf(x: float) -> float:
    return x if x == 0 or x != x else math.copysign(1.0, x) if abs(x) > 10 else _mp(MP.erf, x)


def _atan2(y: float, x: float) -> float:
    """C99 F.9.1.4 at every zero and infinity, mpmath elsewhere."""
    if y != y or x != x:
        return NAN
    if y == 0:
        return math.copysign(PI if _negative(x) else 0.0, y)
    if x == 0:
        return math.copysign(HALF_PI, y)
    if math.isinf(y):
        return math.copysign(THREE_QUARTERS_PI if x == -INF else QUARTER_PI if x == INF else HALF_PI, y)
    if math.isinf(x):
        return math.copysign(PI if x < 0 else 0.0, y)
    return nearest(MP.atan2(MP.mpf(y), MP.mpf(x)))


def _rank(v: float) -> tuple[float, float]:
    return v, math.copysign(1.0, v)  # -0 ranks below +0


def _min(*values: float) -> float:
    return NAN if any(v != v for v in values) else min(values, key=_rank)


def _max(*values: float) -> float:
    return NAN if any(v != v for v in values) else max(values, key=_rank)


def _divide(a: float, b: float) -> float:
    return NAN if b == 0 or a != a or b != b else a / b


def _odd_integer(y: float) -> bool:
    return y.is_integer() and abs(y) <= MAX_SAFE and int(y) & 1 == 1


def power(x: float, y: float) -> float:
    """`x ^ y`: C99 F.9.4.4 with the spec's overrides (NaN in gives NaN, 0 to a negative power is NaN)."""
    if x != x or y != y:
        return NAN
    if y == 0 or x == 1 or (x == -1 and math.isinf(y)):
        return 1.0
    if x == 0:
        return NAN if y < 0 else x if _odd_integer(y) else 0.0
    if math.isinf(y):
        return INF if (abs(x) > 1) == (y > 0) else 0.0
    if math.isinf(x):
        odd = x < 0 and _odd_integer(y)
        return (-INF if odd else INF) if y > 0 else (-0.0 if odd else 0.0)
    if x < 0 and not y.is_integer():
        return NAN
    return _magnitude_power(abs(x), y, x < 0 and _odd_integer(y))


def _magnitude_power(a: float, y: float, negative: bool) -> float:
    """(-1)^negative * a^y for finite a > 0 and finite y != 0, correctly rounded."""
    odd, f = _odd_part(a)
    if y.is_integer():
        k = int(y)
        if odd == 1:
            return round_ratio(negative, 1, 1, f * k)
        if abs(k) * odd.bit_length() <= EXACT_POWER_BITS:
            p = odd ** abs(k)
            return round_ratio(negative, p, 1, f * k) if k > 0 else round_ratio(negative, 1, p, f * k)
    t = MP.mpf(y) * MP.log(MP.mpf(a), 2)  # log2 of the result, far from the cuts below whenever they apply
    if t > 1100 or t < -1200:
        return round_ratio(negative, 1, 1, 2000 if t > 0 else -2000)
    r = MP.power(MP.mpf(a), MP.mpf(y))
    _, man, exp, bc = r._mpf_
    man, exp = int(man), int(exp)
    unit = max(exp + bc - 1 - 52, -1074)
    below = unit - exp  # bits of man below one ulp
    if below >= 1:
        q, rest = man >> below, man & ((1 << below) - 1)
        half = 1 << (below - 1)
        if abs(rest - half) << 100 <= 1 << below and not y.is_integer():
            if _is_exact_power(odd, f, y, 2 * q + 1, unit - 1):
                return round_ratio(negative, q + (q & 1), 1, unit)
    return round_ratio(negative, man, 1, exp)


def _is_exact_power(odd: int, f: int, y: float, m: int, g: int) -> bool:
    """Whether (odd * 2^f)^y is exactly m * 2^g, for odd m and odd > 0 and finite non-integer y = num / 2^k.
    With num odd, odd^num = m^(2^k) forces odd = w^(2^k) and m = w^num; a negative num forces odd = m = 1."""
    num, den = y.as_integer_ratio()
    if num < 0:
        return odd == 1 and m == 1 and g * den == f * num
    if odd == 1:
        return m == 1 and f * num == g * den
    k = den.bit_length() - 1
    if k > 5 or num > 34:  # w >= 3 odd: w^(2^k) < 2^53 needs k <= 5, and w^num = m < 2^54 needs num <= 34
        return False
    w = odd
    for _ in range(k):
        root = math.isqrt(w)
        if root * root != w:
            return False
        w = root
    return w**num == m and f * num == g * den


FUNCTION_TABLE: dict[str, Callable[..., float]] = {
    "sin": _sin,
    "cos": _cos,
    "tan": _tan,
    "asin": _asin,
    "acos": _acos,
    "atan": _atan,
    "sinh": _sinh,
    "cosh": _cosh,
    "tanh": _tanh,
    "exp": _exp,
    "ln": _ln,
    "log10": _log10,
    "sqrt": _sqrt,
    "cbrt": _cbrt,
    "abs": abs,
    "sign": _sign,
    "floor": _floor,
    "ceil": _ceil,
    "Phi": _Phi,
    "phi": _phi,
    "erf": _erf,
    "atan2": _atan2,
    "min": _min,
    "max": _max,
}


# Text.


def literal(text: str) -> float:
    """The nearest double of a number token's text; ParseError past 20 significant digits or to an infinity."""
    mantissa, _, exponent = text.replace("E", "e").partition("e")
    whole, _, fraction = mantissa.partition(".")
    digits = whole + fraction
    significant = digits.strip("0")
    if len(significant) > MAX_DIGITS:
        raise ParseError(f"more than {MAX_DIGITS} significant digits")
    if not significant:
        return 0.0
    scale = int(exponent or "0") - len(fraction) + len(digits) - len(digits.rstrip("0"))
    s, size = int(significant), len(significant)
    if size - 1 + scale >= 309:  # at least 1e309
        raise ParseError("a number whose nearest double is infinite")
    if size + scale <= -325:  # below 1e-325, under half the smallest subnormal
        return 0.0
    value = round_ratio(False, s * 10**scale) if scale >= 0 else round_ratio(False, s, 10**-scale)
    if value == INF:
        raise ParseError("a number whose nearest double is infinite")
    return value


def _number_end(src: str, i: int) -> int:
    n = len(src)
    while i < n and src[i] in DIGITS:
        i += 1
    if i < n and src[i] == ".":
        j = i + 1
        while j < n and src[j] in DIGITS:
            j += 1
        if j == i + 1:
            raise ParseError("a decimal point with no digit after it")
        i = j
    if i < n and src[i] in "eE":
        j = i + 1 + (i + 1 < n and src[i + 1] in "+-")
        if j < n and src[j] in DIGITS:
            while j < n and src[j] in DIGITS:
                j += 1
            i = j
    return i


Token = tuple[str, str, float]  # (kind, text, value): kind is num, name, op, rel or end


def tokens(src: str) -> list[Token]:
    """The source's tokens, ending with an end token; ParseError for anything section 1 refuses."""
    if not isinstance(src, str):
        raise TypeError("a source is a str")
    if len(src) > MAX_LENGTH:
        raise ParseError(f"longer than {MAX_LENGTH} characters")
    out: list[Token] = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c in WHITE:
            i += 1
        elif c in DIGITS or (c == "." and i + 1 < n and src[i + 1] in DIGITS):
            j = _number_end(src, i)
            out.append(("num", src[i:j], literal(src[i:j])))
            i = j
        elif c in LETTERS:
            j = i + 1
            while j < n and src[j] in NAME_CHARS:
                j += 1
            out.append(("name", src[i:j], 0.0))
            i = j
        elif c in "<>=":
            two = src[i : i + 2]
            if two in RELATIONS:
                out.append(("rel", two, 0.0))
                i += 2
            elif c in RELATIONS:
                out.append(("rel", c, 0.0))
                i += 1
            else:
                raise ParseError("'=' alone")
        elif c in SINGLES:
            out.append(("op", c, 0.0))
            i += 1
        else:
            raise ParseError(f"the character {c!r}")
    out.append(("end", "", 0.0))
    return out


# Nodes. `size` is the node count of section 5; `ev` evaluates against a _Run.


class _Run:
    __slots__ = ("env", "left")

    def __init__(self, env: dict[str, float]) -> None:
        self.env = env
        self.left = BUDGET


class Num:
    __slots__ = ("value",)
    size = 1

    def __init__(self, value: float) -> None:
        self.value = value

    def ev(self, run: _Run) -> float:
        return self.value


class Var:
    __slots__ = ("name",)
    size = 1

    def __init__(self, name: str) -> None:
        self.name = name

    def ev(self, run: _Run) -> float:
        return run.env[self.name]


class Neg:
    __slots__ = ("count", "arg", "size")

    def __init__(self, count: int, arg: Node) -> None:
        self.count, self.arg, self.size = count, arg, count + arg.size

    def ev(self, run: _Run) -> float:
        v = self.arg.ev(run)
        return -v if self.count & 1 else v


class Chain:
    """A left-associative run of `+ -` or of `* /`."""

    __slots__ = ("first", "rest", "size")

    def __init__(self, first: Node, rest: list[tuple[str, Node]]) -> None:
        self.first, self.rest = first, rest
        self.size = first.size + sum(1 + node.size for _, node in rest)

    def ev(self, run: _Run) -> float:
        acc = self.first.ev(run)
        for op, node in self.rest:
            b = node.ev(run)
            if op == "+":
                acc += b
            elif op == "-":
                acc -= b
            elif op == "*":
                acc *= b
            else:
                acc = _divide(acc, b)
        return acc


class Power:
    """links [(m0, p0), ..., (mn, pn)] stand for -^m0 (p0 ^ -^m1 (p1 ^ ... -^mn pn)), the right fold of
    `unary = "-" unary | power` and `power = primary [ "^" unary ]`."""

    __slots__ = ("links", "size")

    def __init__(self, links: list[tuple[int, Node]]) -> None:
        self.links = links
        self.size = sum(m + p.size for m, p in links) + len(links) - 1

    def ev(self, run: _Run) -> float:
        values = [(m, p.ev(run)) for m, p in self.links]
        m, acc = values.pop()
        if m & 1:
            acc = -acc
        for m, base in reversed(values):
            acc = power(base, acc)
            if m & 1:
                acc = -acc
        return acc


class Call:
    __slots__ = ("fn", "args", "size")

    def __init__(self, fn: Callable[..., float], args: list[Node]) -> None:
        self.fn, self.args = fn, args
        self.size = 1 + sum(a.size for a in args)

    def ev(self, run: _Run) -> float:
        return self.fn(*[a.ev(run) for a in self.args])


class If:
    __slots__ = ("lhs", "rel", "rhs", "then", "other", "size")

    def __init__(self, lhs: Node, rel: str, rhs: Node, then: Node, other: Node) -> None:
        self.lhs, self.rel, self.rhs, self.then, self.other = lhs, RELATIONS[rel], rhs, then, other
        self.size = 1 + lhs.size + rhs.size + then.size + other.size

    def ev(self, run: _Run) -> float:
        a, b = self.lhs.ev(run), self.rhs.ev(run)
        if a != a or b != b:
            return NAN
        return (self.then if self.rel(a, b) else self.other).ev(run)


class Sum:
    __slots__ = ("index", "lo", "hi", "term", "size")

    def __init__(self, index: str, lo: Node, hi: Node, term: Node) -> None:
        self.index, self.lo, self.hi, self.term = index, lo, hi, term
        self.size = 1 + lo.size + hi.size + term.size

    def ev(self, run: _Run) -> float:
        lo, hi = self.lo.ev(run), self.hi.ev(run)
        if not (_safe_integer(lo) and _safe_integer(hi)):
            return NAN
        first, count = int(lo), max(0, int(hi) - int(lo) + 1)
        cost = count * self.term.size
        if cost > run.left:
            raise _Spent
        run.left -= cost
        env, index, term = run.env, self.index, self.term
        outer = env.get(index)
        total = 0.0
        try:
            for i in range(count):
                env[index] = float(first + i)
                total += term.ev(run)
                if total != total:
                    break
        finally:
            if outer is None:
                env.pop(index, None)
            else:
                env[index] = outer
        return total


Node = Num | Var | Neg | Chain | Power | Call | If | Sum


def _safe_integer(v: float) -> bool:
    return v.is_integer() and abs(v) <= MAX_SAFE


# Grammar.


class _Parser:
    def __init__(self, toks: list[Token], table: Mapping[str, Callable[..., float]]) -> None:
        self.toks, self.at, self.depth, self.table = toks, 0, 0, table
        self.free: dict[str, None] = {}
        self.bound: list[str] = []

    def peek(self, text: str) -> bool:
        kind, t, _ = self.toks[self.at]
        return kind in ("op", "rel") and t == text

    def take(self) -> Token:
        tok = self.toks[self.at]
        self.at += 1
        return tok

    def expect(self, text: str) -> None:
        if not self.peek(text):
            raise ParseError(f"expected {text!r}, found {self.toks[self.at][1] or 'the end'!r}")
        self.at += 1

    def open(self) -> None:
        self.expect("(")
        self.depth += 1
        if self.depth > MAX_DEPTH:
            raise ParseError(f"brackets nest deeper than {MAX_DEPTH}")

    def close(self) -> None:
        self.expect(")")
        self.depth -= 1

    def source(self) -> Node:
        node = self.expr()
        if self.toks[self.at][0] != "end":
            raise ParseError(f"unexpected {self.toks[self.at][1]!r}")
        return node

    def expr(self) -> Node:
        return self.chain(self.term, "+", "-")

    def term(self) -> Node:
        return self.chain(self.unary, "*", "/")

    def chain(self, operand: Callable[[], Node], a: str, b: str) -> Node:
        first = operand()
        rest: list[tuple[str, Node]] = []
        while self.peek(a) or self.peek(b):
            rest.append((self.take()[1], operand()))
        return Chain(first, rest) if rest else first

    def unary(self) -> Node:
        links: list[tuple[int, Node]] = []
        while True:
            m = 0
            while self.peek("-"):
                self.at += 1
                m += 1
            links.append((m, self.primary()))
            if not self.peek("^"):
                break
            self.at += 1
        if len(links) > 1:
            return Power(links)
        m, p = links[0]
        return Neg(m, p) if m else p

    def primary(self) -> Node:
        kind, text, value = self.toks[self.at]
        if kind == "num":
            self.at += 1
            return Num(value)
        if self.peek("("):
            self.open()
            node = self.expr()
            self.close()
            return node
        if kind != "name":
            raise ParseError(f"unexpected {text or 'end'!r}")
        self.at += 1
        called = self.peek("(")
        if text in CALLS:
            if not called:
                raise ParseError(f"{text} without its call")
            return self.call(text)
        if called:
            raise ParseError(f"a call on {text}, which is not a function")
        if text in CONSTANTS:
            return Num(CONSTANTS[text])
        if text not in self.bound:
            self.free.setdefault(text)
        return Var(text)

    def call(self, name: str) -> Node:
        self.open()
        node: Node
        if name == "if":
            lhs = self.expr()
            kind, rel, _ = self.take()
            if kind != "rel":
                raise ParseError("if needs a comparison as its first argument")
            rhs = self.expr()
            self.expect(",")
            then = self.expr()
            self.expect(",")
            node = If(lhs, rel, rhs, then, self.expr())
        elif name == "sum":
            kind, index, _ = self.take()
            if kind != "name" or index in CALLS or index in CONSTANTS:
                raise ParseError("a sum's index is a bare name that is not reserved")
            self.expect(",")
            lo = self.expr()
            self.expect(",")
            hi = self.expr()
            self.expect(",")
            self.bound.append(index)
            term = self.expr()
            self.bound.pop()
            node = Sum(index, lo, hi, term)
        else:
            args = [self.expr()]
            while self.peek(","):
                self.at += 1
                args.append(self.expr())
            wanted = 2 if name == "atan2" else 1 if name in ONE_ARG else 0
            if (wanted and len(args) != wanted) or (not wanted and len(args) < 2):
                raise ParseError(f"{name} takes {wanted or 'two or more'} arguments, not {len(args)}")
            node = Call(self.table[name], args)
        self.close()
        return node


class Expr:
    """A compiled source: its tree, free variables in order of first appearance, and whether it is exact. `table`
    maps each function name to its implementation; the golden generator passes one that records arguments."""

    __slots__ = ("root", "free", "exact")

    def __init__(self, src: str, table: Mapping[str, Callable[..., float]] = FUNCTION_TABLE) -> None:
        toks = tokens(src)
        parser = _Parser(toks, table)
        self.root = parser.source()
        self.free = list(parser.free)
        self.exact = not any(t == "^" or (k == "name" and t in INEXACT) for k, t, _ in toks)

    def evaluate(self, scope: Mapping[str, object]) -> float:
        env: dict[str, float] = {}
        for name in self.free:
            v = scope.get(name)
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise ScopeError(f"{name} needs a number")
            env[name] = v if isinstance(v, float) else round_ratio(v < 0, abs(v))
        try:
            return self.root.ev(_Run(env))
        except _Spent:
            return NAN


def parse(src: str) -> Expr:
    return Expr(src)


def value(src: str, scope: Mapping[str, object] | None = None) -> float:
    return Expr(src).evaluate(scope or {})


# Goldens.


def encode(v: float) -> float | str:
    return "nan" if v != v else ("inf" if v > 0 else "-inf") if math.isinf(v) else v


def case(src: str, scope: Mapping[str, object]) -> dict[str, object]:
    line: dict[str, object] = {"src": src, "scope": dict(scope)}
    try:
        expr = Expr(src)
    except ParseError:
        return line | {"error": "parse"}
    try:
        v = expr.evaluate(scope)
    except ScopeError:
        return line | {"error": "scope"}
    return line | {"free": expr.free, "value": encode(v), "exact": expr.exact}


BIG = "(1e308*10)"  # +inf, since no literal is infinite
NEG_BIG = "(-(1e308*10))"
NOT_A_NUMBER = "(0/0)"
TERM_500 = "if(k < 0, " + "-" * 495 + "k, 1)"  # the spec's 500-node term
TERM_499 = "if(k < 0, " + "-" * 494 + "k, 1)"
TERM_250 = "if(k<0," + "-" * 245 + "k,1)"
TIE_BASES = (1553**4, 1555**4, 1781**4)  # w^4 with w^5 odd in [2^53, 2^54), so x^1.25 is exactly a half-ulp


def _nested(open_: str, close: str, count: int, inner: str = "1") -> str:
    return open_ * count + inner + close * count


TEXT = [
    *(
        (s, {})
        for s in (
            "2", "007", "0.5", ".5", "1.5e-3", "2E+3", "2e3", "2E3", "1e0", "1e-0", "0e5", "0.0", "00.000",
            "12.75e+1", ".5e1", "0.000", "1.", "1.e5", "1.5.", "5.+1", "1..5", ".", ".e5", "1e", "1e+", "1e-",
            "1E", "1e5.5", ".5.5", "1 .", "0x10", "1_000", "1,000", "1e5e", "e", "12345678901234567890",
            "123456789012345678901", "100000000000000000000000000", "0.00012345678901234567890e3",
            "1234567890.1234567890", "12345678901234567890.1", "1.0000000000000000001", "1.00000000000000000001",
            "10000000000000000000001", "0.000000000000000000000000001", "000000000000000000000000000000000001",
            "99999999999999999999", "999999999999999999999", "9.9999999999999999999e5", "4.9999999999999999999",
            "0.00000000000000000000000000000000000000000000000000", "1.0000000000000000000000000000000",
            "9007199254740993", "9007199254740995", "9007199254740992.5", "0.1000000000000000055511151231257827",
            "0.30000000000000004", "1e999", "1e309", "1e308", "1.7976931348623157e308", "1.7976931348623158e308",
            "1.7976931348623159e308", "17976931348623157e292", "2e-324", "3e-324", "1e-400", "4.9406564584124654e-324",
            "2.4703282292062327e-324", "2.4703282292062328e-324", "2.2250738585072014e-308",
            "2.2250738585072011e-308", "1e-0000000000000000000000000000400", "1e0000000000000000000000000000000300",
            "1e-99999999999999999999", "1e99999999999999999999", "0e99999999999999999999",
            "0.00000000000000000000000000001e330", "100000000000000000000e288", "100000000000000000000e289",
            " 1 ", "\t1\n", "1\r\n+\r\n2", "\n\n\n", "", " ", "1\f", "1\v", "1\u00a0", "\u20001", "1\u3000+1",
            "1\u2028", "1 +\t\t2", "_x", "__proto__", "\u03c0", "x\u00b2", "x\u0661", "\u0661", "x\uff11", "\uff11",
            "\uff58", "caf\u00e9", "\U0001d465", "\ud800", "x\u200b", "Infinity", "nan", "2**3", "[1]", "1 . 2",
            "2 % 3", "2 & 3", "#1", "'1'", '"1"', "1;", "{1}", "1!", "~1", "?", "@x", "$x", "1 =< 2", "\\x",
            "2 \u00d7 3", "2 \u2212 3", "1\u20442", "1" + " " * 999, " " * 1000 + "1", "1" + "+1" * 499 + " ",
            "1" + "+1" * 499 + "  ", "1" + " " * 998 + "+",
        )
    ),
    ("e5", {"e5": 2}), ("E5", {"E5": 3}), ("E", {"E": 4}), ("x", {"x": 1.5}), ("x_1", {"x_1": 2}),
    ("W_t", {"W_t": -1}), ("lambda", {"lambda": 3}), ("pi2", {"pi2": 4}), ("Z9", {"Z9": 5}), ("a__b", {"a__b": 6}),
    ("x1_", {"x1_": 7}), ("x__", {"x__": 8}), ("NaN", {"NaN": 1}), ("inf", {"inf": 2}), ("x = 1", {"x": 1}),
    ("x != 1", {"x": 1}), ("x'", {"x": 1}),
]

GRAMMAR = [
    *(
        (s, {})
        for s in (
            "2^-1", "2^3^2", "-2^-2^-1", "1 - 2 - 3", "8/4*2", "2*3+4*5", "2+3*4", "(2+3)*4", "2^2*3", "2*3^2",
            "-2^2", "(-2)^2", "2^-2^2", "--1", "1--1", "1-+1", "+1", "1++1", "1+-1", "2*-3", "2^--2", "1/2/4",
            "1-2+3", "2/3*3", "-(1)", "-(-(-1))", "2^3*2^2", "(2^3)^2", "2^(3^2)", "-1^2", "2^-0.5", "2^2^-1",
            "2 3", "(1)(2)", "2(3)", "(1)2", "pi e", "2pi", "2 pi", "1 -", "* 1", "1 *", "()", "(", ")", "(1", "1)",
            "((1)", "(1))", ",", "1,2", "(1, 2)", "1^", "^1", "1^^2", "1//2", "1*/2", "sin()", "sin(1, 2)",
            "min(1)", "sin(1,)", "(sin)(1)", "sin(1)(2)", "sin", "sin + 1", "sin (1)", "sin\t(1)", "sin\n(0)",
            "min(1,2)", "min(3,1,2)", "max(1,2,3,4,5)", "atan2(1)", "atan2(1,2,3)", "atan2(1, 1)", "min(,1)",
            "min(1,,2)", "max()", "max(1)", "sqrt(4)", "sqrt 4", "abs(-3)", "abs(1, 2)", "if(1<2,3)",
            "if(1<2,3,4,5)", "if(1<2,3,4)", "sum(k,1,3)", "sum(k,1,3,k,1)", "sum(k,1,3,k)", "sin(1", "sin 1)",
            "sin(1))", "min(1, 2", "pi(1)", "foo(1)", "constructor(1)", "e(1)", "pi + e", "sum",
            "sum + 1", "if", "if + 1", "Phi", "PHI(0)", "Sin(0)", "log(10)", "ln(e)", "log10 (100)", "pi*2", "e^2",
            "e*pi", "min", "atan2", "sin^2(1)", "sin(1)^2", "sum(k, 1, 2, k)(1)", "if(1<2,1,2)(3)", "pi(1+1)",
            "if((1 < 2), 1, 2)", "if(1 < 2 < 3, 1, 2)", "(1 < 2) + 1", "if(1 <= 1, 1, 2)", "if(1 == 1, 1, 2)",
            "if(1 >= 2, 1, 2)", "if(1 > 2, 1, 2)", "if(2 > 1, 1, 2)", "if(1 < 1, 1, 2)", "if(1 = 1, 1, 2)",
            "if(1 != 1, 1, 2)", "if(1 < 2, 1 < 2, 3)", "if(1<2, if(2<3, 4, 5), 6)", "if(-0 == 0, 1, 2)",
            "if(-0 < 0, 1, 2)", "if(0 <= -0, 1, 2)", "if(0/0 < 1, 1, 2)", "if(1 < 0/0, 1, 2)",
            "if(0/0 == 0/0, 1, 2)", "if(1 < 2, 1, 0/0)", "if(1 > 2, 1/0, 3)", "if(if(1<2,1,2) < 2, 3, 4)",
            "if(1 < 2, 3, 4) + if(1 > 2, 3, 4)", "if (1 < 2, 3, 4)", "if(1 <2,3,4)", "if(1 < = 2, 3, 4)",
            "if(1 =  = 1, 3, 4)", "if(1 << 2, 3, 4)", "if(1 => 2, 3, 4)", "if(1 >== 2, 3, 4)", "if(1e999 < 2, 1, 2)",
            "if(1 < 2)", "if()", "if(1 < 2, , 3)", f"if({BIG} > 1e308, 1, 2)", f"if({NEG_BIG} < -1e308, 1, 2)",
            "if(1 < 2, 3, 4", "if(1 < 2; 3, 4)", "sum(k, 1, 3, k)", "sum((k), 1, 3, k)", "sum(pi, 1, 3, 1)",
            "sum(sin, 1, 3, 1)", "sum(e, 1, 2, 1)", "sum(if, 1, 2, 1)", "sum(sum, 1, 2, 1)", "sum(2, 1, 3, 1)",
            "sum(k+1, 1, 3, k)", "sum(-k, 1, 3, k)", "sum(k, 3, 1, k)", "sum(k, 1, 1, -0)", "sum(k, 1, 2, -0)",
            "sum(k, 1.5, 3, k)", "sum(k, 1, 2.5, k)", "sum(k, 1, 0/0, k)", "sum(k, 0/0, 1, k)", f"sum(k, 1, {BIG}, k)",
            f"sum(k, {NEG_BIG}, 1, k)", "sum(k, 9007199254740991, 9007199254740991, k)",
            "sum(k, 9007199254740992, 9007199254740992, k)", "sum(k, -9007199254740991, -9007199254740991, k)",
            "sum(k, -9007199254740992, -9007199254740992, k)", "sum(k, 9007199254740990, 9007199254740991, k)",
            "sum(k, 1, 9007199254740991, 1)", "sum(k, -0, 0, atan2(k, -1))", "sum(k, -0, 1, atan2(k, -1))",
            "sum(k, -0, 1, k)", "sum(k, 1, 4, 1/k)", "sum(k, 1, 10, 0.1)", "sum(k, 1, 3, sum(k, 1, k, k))",
            "sum(k, 1, 2, sum(j, 1, k, k*j))", "sum(constructor, 1, 3, constructor)", "sum(k, 1, sum(j, 1, 3, j), k)",
            "sum(k, sum(j, 1, 2, j), 3, k)", "sum(k, 1, 3, k^2)", "sum(k, 1, 3, k)*2", "sum (k, 1, 3, k)",
            "sum(k, 1, 3, k", "sum(k 1, 3, k)", "sum(k, 1, 3, )", "sum(k1, 1, 3, k1)", "sum(k, -2, 2, k)",
            "sum(k, 1, 3, if(k == 2, 0/0, k))", "sum(k, 1, 3, if(k == 4, 0/0, k))", "sum(k, 2, 1, 0/0)",
            "sum(k, -3, -1, k)", "sum(k, 1, 5, k*k*k)", "sum(k, 1, 3, -k)", "sum(k, 0, 0, sign(k))",
            "sum(k, -0, -0, sign(k))", "sum(k, 1, 2)", "sum()", "sum(k)", "sum(k, 1)",
        )
    ),
    ("-x^2", {"x": 3}), ("-x", {"x": 0}), ("- -x", {"x": 0}), ("x*-y^2", {"x": 2, "y": 3}), ("2x", {"x": 1}),
    ("x y", {"x": 1, "y": 2}), ("x(1)", {"x": 1}), ("SIN", {"SIN": 2}), ("Pi", {"Pi": 3}), ("PI", {}),
    ("constructor", {}), ("constructor", {"constructor": 2}), ("toString", {}), ("prototype", {"prototype": 3}),
    ("constructor + prototype + toString", {"constructor": 1, "prototype": 2, "toString": 3}),
    ("valueOf", {"valueOf": 5}), ("hasOwnProperty", {}), ("hasOwnProperty", {"hasOwnProperty": 1}),
    ("if((x) < 0, 1, 2)", {"x": -1}), ("x < 1", {"x": 0}), ("if(x, 1, 2)", {"x": 1}), ("if(1 < 2, x, y)", {"x": 1}),
    ("if(x + 1 < y * 2, x, y)", {"x": 1, "y": 2}), ("if(x < 2, 3, 4)", {"x": 2}), ("if(x <= 2, 3, 4)", {"x": 2}),
    ("if(x == y, 3, 4)", {"x": 0.0, "y": -0.0}), ("if(x > y, 3, 4)", {"x": 0.0, "y": -0.0}),
    ("sum(x, 1, 3, x) + x", {"x": 10}), ("sum(k, 1, k, k)", {"k": 4}), ("sum(b, a, 3, b) + b", {"a": 1, "b": 10}),
    ("sum(k, 1, 3, k) + k", {"k": 1}), ("sum(k, 1, 3, k)", {"k": True}), ("sum(k, 1, x, k)", {"x": 4}),
    ("sum(k, x, 3, k)", {}), ("sum(k, 1, 3, x)", {}), ("sum(k, 1, 3, x)", {"x": 2}), ("sum(K, 1, 3, k)", {"k": 2}),
    ("sum(k, lo, hi, k*x)", {"lo": 1, "hi": 4, "x": 0.5}), ("sum(x, x, x + 2, x)", {"x": 5}),
    ("sum(i, 1, n, sum(j, 1, i, i*j))", {"n": 4}), ("sum(n, 1, n, n)", {"n": 3}),
]

LIMITS = [
    (_nested("(", ")", 32), {}), (_nested("(", ")", 33), {}), (_nested("abs(", ")", 32), {}),
    (_nested("abs(", ")", 33), {}), (_nested("(abs(", "))", 16), {}), (_nested("(abs(", "))", 16, "(1)"), {}),
    ("if(" + _nested("(", ")", 31) + " < 2, 3, 4)", {}), ("if(" + _nested("(", ")", 32) + " < 2, 3, 4)", {}),
    ("sum(k, 1, 2, " + _nested("(", ")", 31, "k") + ")", {}), ("sum(k, 1, 2, " + _nested("(", ")", 32, "k") + ")", {}),
    ("min(" + _nested("(", ")", 31) + ", 2)", {}), ("min(2, " + _nested("(", ")", 32) + ")", {}),
    (_nested("(", ")", 32) + "+" + _nested("(", ")", 32), {}), (_nested("sum(k, 1, 1, ", ")", 32, "k"), {}),
    (_nested("sum(k, 1, 1, ", ")", 33, "k"), {}), (_nested("if(1 < 2, ", ", 0)", 32), {}),
    (_nested("if(1 < 2, ", ", 0)", 33), {}), ("-" * 999 + "1", {}), ("-" * 998 + "1", {}), ("-" * 1000 + "1", {}),
    ("-" * 999 + "x", {"x": 2}), ("2^" + "-" * 997 + "1", {}), ("1" + "^1" * 499, {}), ("2" + "^1" * 499, {}),
    ("1" + "+1" * 499, {}), ("1" + "-1" * 499, {}), ("2" + "*1" * 499, {}), ("1" + "/1" * 499, {}),
    ("-" * 497 + "(" + "-" * 499 + "1)", {}), ("1" + "+1" * 500, {}), ("x" + "+x" * 499, {"x": 0.1}),
    ("sum(k, 1, 2000, " + TERM_500 + ")", {}), ("sum(k, 1, 2001, " + TERM_500 + ")", {}),
    ("sum(i, 1, 400, sum(j, 1, 2496, 1))", {}), ("sum(i, 1, 400, sum(j, 1, 2497, 1))", {}),
    ("sum(k, 1, 1000000, 1)", {}), ("sum(k, 1, 1000001, 1)", {}),
    ("sum(k,1,2000," + TERM_250 + ")+sum(k,1,2000," + TERM_250 + ")", {}),
    ("sum(k,1,2000," + TERM_250 + ")+sum(k,1,2001," + TERM_250 + ")", {}),
    ("sum(k, 1, sum(j, 1, 2000, 1), " + TERM_499 + ")", {}), ("sum(k, 1, sum(j, 1, 2001, 1), " + TERM_499 + ")", {}),
    ("if(1 < 2, 1, sum(k, 1, 1e7, k))", {}), ("if(1 > 2, 1, sum(k, 1, 1e7, k))", {}),
    ("sum(k, 1, 0, sum(j, 1, 1e9, j))", {}), ("sum(k, 1, 1e9, k) * 0", {}), ("0 * sum(k, 1, 1e9, k)", {}),
    ("min(1, sum(k, 1, 1e9, k))", {}), ("if(sum(k, 1, 1e9, k) < 0, 1, 2)", {}), ("sum(k, 1, 1e9, k)^0", {}),
]

VARIABLES = [
    ("x + y + x", {"x": 1, "y": 2}), ("y + x", {"x": 1, "y": 2}), ("x*0", {}), ("x", {"x": True}),
    ("x", {"x": False}), ("x", {"x": "1"}), ("x", {"x": None}), ("pi*x", {"x": 2}), ("x", {"x": -0.0}),
    ("x", {"x": 5e-324}), ("x", {"x": 1.7976931348623157e308}), ("x", {"y": 1}), ("x + y", {"x": 1}),
    ("x + y", {"y": 1}), ("x", {"x": 1, "y": True}), ("e*E", {"E": 2}), ("x_1 - x_2", {"x_1": 3, "x_2": 1}),
    ("if(1 < 2, 1, z)", {}), ("a*b*c*a*b*c", {"c": 2, "b": 3, "a": 4}), ("x", {"x": 3}), ("x/y", {"x": 1, "y": 3}),
    ("1/x", {"x": -0.0}), ("x - x", {"x": -0.0}), ("x + x", {"x": -0.0}), ("-x", {"x": -0.0}),
]

EXACT_VALUES = [
    "1/0", "1/-0", "0/0", "-1/0", f"{BIG}/0", f"1/{BIG}", f"-1/{BIG}", BIG, "-1e308*10", f"{BIG} - {BIG}",
    f"0*{BIG}", "1e308+1e308", "5e-324/2", "1.5*5e-324", "2.5*5e-324", "0.1+0.2", "1-1", "-0+0", "-0-0", "-0+-0",
    "0*-1", "-0*-0", "1/3", "2/3", "1e308*1.5", f"{BIG}*0", f"{BIG}/{BIG}", "9007199254740992 + 1",
    "9007199254740992 + 2", "0.1*3", "1 - 0.9", "4.35*100", "1e16 + 1 - 1e16", "1e-320*1e-10", "-1e-320*1e-10",
    "1e-320/1e10", "5e-324 - 5e-324", "sqrt(-0)", "sqrt(-1)", "sqrt(2)", f"sqrt({BIG})", f"sqrt({NEG_BIG})", "sqrt(0)",
    "sqrt(5e-324)", "sqrt(0/0)", "sqrt(1e308)", "sqrt(2)*sqrt(2)", "sqrt(16)", "sqrt(0.01)",
    "sqrt(1.7976931348623157e308)",
    "sqrt(-5e-324)", "sqrt(2.0000000000000004)", "sqrt(1e-300)", "sqrt(3)", "abs(-0)", "abs(0)", f"abs({NEG_BIG})",
    "abs(-2.5)", "abs(0/0)", "sign(-0)", "sign(0)", "sign(-3)", "sign(5e-324)", "sign(-5e-324)", f"sign({BIG})",
    f"sign({NEG_BIG})", "sign(0/0)", "floor(-0.5)", "ceil(-0.5)", "floor(-0)", "ceil(-0)", "floor(0.5)", "ceil(0.5)",
    "floor(4503599627370495.5)", "ceil(4503599627370495.5)", "floor(-4503599627370495.5)", "ceil(-4503599627370495.5)",
    "floor(1e300)", f"floor({BIG})", f"ceil({NEG_BIG})", "floor(5e-324)", "floor(-5e-324)", "ceil(-5e-324)",
    "ceil(5e-324)", "floor(-0.9999999999999999)", "ceil(0.9999999999999999)", "floor(2.9999999999999996)",
    "ceil(-1)", "floor(-1)", "ceil(-1.5)", "floor(0/0)", "ceil(0/0)", "floor(-2.5)", "ceil(2.5)", "min(0, -0)",
    "max(-0, 0)", "min(-0, 0)", "max(0, -0)", "min(1, 0/0)", "max(0/0, 1)", "min(1, 2, 0/0, 3)", f"min({BIG}, 1)",
    f"max({NEG_BIG}, -1e308)", "min(3, 1, 2)", "max(1, 3, 2)", "min(-0, -0)", "max(-0, -0)", "min(0, 0, -0, 0)",
    "max(-0, -0, 0, -0)", "min(0/0, 0/0)", f"max({BIG}, {NEG_BIG})", "min(5e-324, -0)", "0/0*0", "-(0/0)",
    "0/0 - 0/0", f"0/0 + {BIG}", "pi", "-pi", "pi/2", "2*pi", "e*e", "pi - 3", "e - 2.718281828459045",
    "if(pi > 3.14159, 1, 2)", "1/x", "sum(k, 1, 4, k/3)", "sum(k, 1, 20, 1/k)", "sum(k, 1, 30, k*0.1)",
]

POWER_VALUES = [
    "1^(0/0)", "(0/0)^0", "(0/0)^1", "0^-1", "(-0)^-1", f"0^{NEG_BIG}", f"(-0)^{NEG_BIG}", "0^-0.5", "0^0",
    "(-0)^0", "0^-0", f"{BIG}^0", f"{NEG_BIG}^0", f"1^{BIG}", f"(-1)^{BIG}", f"1^{NEG_BIG}",
    f"(-1)^{NEG_BIG}", "(-1)^0.5", "1^0.5", "1^-3", "(-1)^3", "(-1)^2", "(-1)^1e300", "(-1)^9007199254740991",
    "(-1)^9007199254740993", "(-1)^-3", f"{NEG_BIG}^0.5", "(-0)^0.5", "(-0)^3", "(-0)^2", f"(-0)^{BIG}", f"0^{BIG}",
    "0^3", "0^0.5", "(-0)^1", "(-0)^9007199254740991", "(-0)^1e300", f"2^{BIG}", f"0.5^{BIG}", f"2^{NEG_BIG}",
    f"0.5^{NEG_BIG}", f"(-2)^{BIG}", f"(-0.5)^{BIG}", f"(-2)^{NEG_BIG}", f"(-0.5)^{NEG_BIG}", "(-2)^0.5",
    f"{NEG_BIG}^3", f"{NEG_BIG}^-3", f"{NEG_BIG}^-2", f"{NEG_BIG}^2", f"{BIG}^-1", f"{BIG}^0.5", f"{NEG_BIG}^-0.5",
    f"{BIG}^{BIG}", f"{BIG}^{NEG_BIG}", f"{NEG_BIG}^{BIG}", f"{NEG_BIG}^{NEG_BIG}", "(-8)^(1/3)", "2^0.5", "2^1024",
    "2^1023", "2^-1074", "2^-1075", "2^-1074.5", "(-2)^-1075", "(-2)^-1074", "(-2)^-1073", "(2^-860)^1.25",
    "(2^860)^-1.25", "(2^-859)^1.25", "(2^-430)^2.5", "10^308", "10^309", "10^-323", "10^-324", "3^40", "3^34",
    "(-3)^33",
    "1.0000000000000002^4503599627370496", "0.9999999999999999^4503599627370496", "1.5^1e300", "0.5^1e300",
    "(-1.5)^1e300", "(-1.5)^9007199254740991", "2^0.1", "4^0.5", "8^(1/3)", "10^-1", "10^22", "10^23", "7^-2",
    "(-7)^-3", "2^-1022", "2^-1023", "0.1^2", "1.1^1000", "(1+2^-52)^(2^52)", "e^1", "e^-1", "pi^2",
]

FUNCTION_VALUES = [
    "sin(-0)", "tan(-0)", "asin(-0)", "atan(-0)", "sinh(-0)", "tanh(-0)", "cbrt(-0)", "erf(-0)", "sin(0)",
    "tan(0)", "asin(0)", "atan(0)", "sinh(0)", "tanh(0)", "cbrt(0)", "erf(0)", "cos(-0)", "cosh(-0)", "exp(-0)",
    "cos(0)", "cosh(0)", "exp(0)", f"sin({BIG})", f"cos({NEG_BIG})", f"tan({BIG})", f"sin({NEG_BIG})", f"atan({BIG})",
    f"atan({NEG_BIG})", f"tanh({BIG})", f"tanh({NEG_BIG})", f"exp({NEG_BIG})", f"exp({BIG})", "exp(709)",
    "exp(710)", "exp(-745)", "exp(-746)", "exp(-708)", f"erf({BIG})", f"erf({NEG_BIG})", f"Phi({NEG_BIG})",
    f"Phi({BIG})", f"phi({BIG})", f"phi({NEG_BIG})", "Phi(0)", "Phi(-0)", "phi(0)", "phi(-0)", "Phi(-2.8)",
    "Phi(2.8)", "Phi(-2.5)", "Phi(2.75)", "Phi(-2)", "Phi(0.5)", "Phi(1e-300)", "Phi(5e-324)", "Phi(1)",
    "Phi(-1)", "Phi(1.96)", "phi(30)", "phi(37)", "phi(-1)", "phi(1)", "phi(45)", "erf(0.1)", "erf(-2)",
    "erf(1e-300)", "erf(5e-324)", "erf(2)", "erf(-1.5)", "erf(1.9999999999999998)", "erf(1)", "erf(-1e-8)",
    "ln(0)", "ln(-0)", "ln(-1)", "ln(1)",
    f"ln({BIG})", f"ln({NEG_BIG})", "ln(5e-324)", "ln(2)", "ln(1e308)", "ln(0/0)", "log10(0)", "log10(-0)",
    "log10(-1)", "log10(1)", "log10(1000)", "log10(1e-300)", f"log10({BIG})", "log10(5e-324)", "log10(2)",
    "log10(1e22)", "asin(1.0000000000000002)", "acos(-1.0000000000000002)", "asin(1)", "acos(-1)", "acos(1)",
    "acos(0)", "asin(-1)", f"asin({BIG})", f"acos({NEG_BIG})", "asin(0.5)", "acos(0.5)", "acos(-0)",
    "acos(0.9999999999999999)", "cbrt(-27)", "cbrt(27)", f"cbrt({NEG_BIG})", f"cbrt({BIG})", "cbrt(5e-324)",
    "cbrt(-8)", "cbrt(0.001)", "cbrt(2)", "atan(1e308)", "atan(1)", "atan(-1)", "atan(5e-324)", "atan2(0, -0)",
    "atan2(-0, -0)", "atan2(0, 0)", "atan2(-0, 0)", "atan2(-0, -1)", "atan2(0, -1)", "atan2(0, 1)", "atan2(-0, 1)",
    "atan2(1, 0)", "atan2(-1, -0)", "atan2(1, -0)", "atan2(-1, 0)", f"atan2(1, {NEG_BIG})", f"atan2(-1, {NEG_BIG})",
    f"atan2(1, {BIG})", f"atan2(-1, {BIG})", f"atan2({BIG}, 1)", f"atan2({NEG_BIG}, 1)", f"atan2({BIG}, {NEG_BIG})",
    f"atan2({NEG_BIG}, {BIG})", f"atan2({BIG}, {BIG})", f"atan2({NEG_BIG}, {NEG_BIG})", f"atan2({BIG}, 0)",
    f"atan2({NEG_BIG}, -0)", f"atan2(0, {NEG_BIG})", f"atan2(-0, {BIG})", "atan2(0/0, 1)", "atan2(1, 0/0)",
    "atan2(1, 2)", "atan2(-1, -1)", "atan2(5e-324, 1e308)", "atan2(-5e-324, 1e308)",
    "atan2(1e308, 5e-324)", "atan2(5e-324, -1e308)", "atan2(-5e-324, -1e308)", "sinh(710)", "sinh(711)",
    "cosh(710)", "cosh(711)", "sinh(-711)", "cosh(-711)", f"sinh({BIG})", f"cosh({NEG_BIG})", f"sinh({NEG_BIG})",
    f"cosh({BIG})", "tanh(20)", "tanh(-20)", "tanh(1e-300)", "sinh(1e-300)", "sinh(1)", "cosh(1)", "tanh(1)",
    "tanh(0.5)", "sin(1)", "cos(1)", "tan(1)", "exp(1)", "exp(-1)", "sin(1e22)", "sin(1e300)", "cos(1e300)",
    "tan(1e300)", "sin(pi)", "cos(pi/2)", "tan(pi/2)", "sin(pi/6)", "cos(pi)", "tan(pi/4)", "sin(5e-324)",
    "tan(5e-324)", "asin(5e-324)", "sinh(5e-324)", "tanh(5e-324)", "cos(5e-324)", "sin(1e-8)", "cos(1e-8)",
    "exp(1e-300)", "ln(1.0000000000000002)", "log10(10)", "log10(0.1)", "exp(ln(2))", "sin(0/0)",
    "cos(0/0)", "tan(0/0)", "asin(0/0)", "acos(0/0)", "atan(0/0)", "sinh(0/0)", "cosh(0/0)", "tanh(0/0)",
    "exp(0/0)", "cbrt(0/0)", "Phi(0/0)", "phi(0/0)", "erf(0/0)", "log10(0/0)",
]


def _fixed() -> list[tuple[str, dict[str, object]]]:
    values = EXACT_VALUES + POWER_VALUES + FUNCTION_VALUES
    ties = [(s, {"x": float(b)}) for b in TIE_BASES for s in ("x^1.25", "x^-1.25", "-x^1.25")]
    return TEXT + GRAMMAR + LIMITS + VARIABLES + [(s, {}) for s in values] + ties


TABLE_RANGE = {"erf": 2.0, "Phi": 2.8}  # spec 6: the parity test's stand-in table is accurate only there


def within_table(src: str, scope: Mapping[str, object]) -> bool:
    """Whether every erf and Phi call the evaluation of src makes receives an argument the parity test's table
    meets: magnitude at most TABLE_RANGE, or a special value (an infinity, a zero or NaN), which any table meets
    exactly (spec 6). A call in a branch not taken receives nothing."""
    seen: list[tuple[str, float]] = []

    def recorder(name: str) -> Callable[..., float]:
        def call(x: float) -> float:
            seen.append((name, x))
            return FUNCTION_TABLE[name](x)

        return call

    table = FUNCTION_TABLE | {name: recorder(name) for name in TABLE_RANGE}
    try:
        Expr(src, table).evaluate(scope)
    except (ParseError, ScopeError):
        return True
    return all(abs(x) <= TABLE_RANGE[name] or math.isinf(x) or x != x for name, x in seen)


# Random lines. Every source the generators build is valid by construction (an expression, an operator and an
# expression make an expression); the twin decides what it means.

NAMES = ("x", "y", "z", "t", "a", "b", "n", "x_1", "W_t", "lambda", "E", "pi2", "e5", "sigma", "mu")
_EXACT_ONE = ("abs", "sign", "floor", "ceil", "sqrt")
_DOMAIN = {
    "sin": (-50.0, 50.0), "cos": (-50.0, 50.0), "tan": (-50.0, 50.0), "asin": (-1.0, 1.0), "acos": (-1.0, 1.0),
    "atan": (-1e3, 1e3), "sinh": (-700.0, 700.0), "cosh": (-700.0, 700.0), "tanh": (-25.0, 25.0),
    "exp": (-700.0, 700.0), "ln": (1e-6, 1e6), "log10": (1e-6, 1e6), "cbrt": (-1e6, 1e6), "Phi": (-2.8, 2.8),
    "phi": (-30.0, 30.0), "erf": (-2.0, 2.0),
}
_BOUNDED = ("sin", "cos", "tanh", "atan", "erf", "Phi", "phi")  # outputs within [-pi/2, pi/2]
_OUTER = ("exp", "atan", "tanh", "erf", "sinh", "cosh", "Phi", "phi", "sin")  # condition number at most 2.5 there
_POSITIVE = ("exp", "cosh", "Phi", "phi")
_ARG_SHAPES = ("{x}", "{x}", "{x}", "({x} + {y})/2", "{x}/2", "-{x}", "abs({x})", "{x}*0.5", "({x} - {y})/4")


def _space(rng: random.Random) -> str:
    return rng.choice(("", " ", " ", " ", "  ", "\t", "\n", "\r\n"))


def _int_text(v: int) -> str:
    return str(v) if v >= 0 else f"-{-v}"


def _num_text(v: float) -> str:
    return repr(v) if not math.copysign(1.0, v) < 0 else f"-{repr(-v)}"


def _literal_text(rng: random.Random) -> str:
    style = rng.randrange(8)
    if style == 0:
        return str(rng.randint(0, 12))
    if style == 1:
        return f"{rng.randint(0, 999)}.{rng.randint(0, 999):03d}"
    if style == 2:
        return f".{rng.randint(1, 99):02d}"
    if style == 3:
        return f"{rng.randint(1, 9)}{rng.choice('eE')}{rng.choice(('', '+', '-'))}{rng.randint(0, 9)}"
    if style == 4:
        return "0" * rng.randint(1, 3) + str(rng.randint(1, 99))
    if style == 5:
        return repr(rng.uniform(0, 100))
    if style == 6:
        digit = rng.randint(1, 9)
        return f"{digit}e-{rng.randint(100, 330)}" if rng.randrange(2) else f"{digit}e{rng.randint(100, 300)}"
    return str(rng.choice((1, 2, 3, 4, 10, 100, 1000)))


def _scope_value(rng: random.Random) -> float:
    roll = rng.randrange(10)
    if roll == 0:
        return rng.choice((0.0, -0.0))
    if roll < 3:
        return float(rng.randint(-10, 10))
    if roll < 5:
        return round(rng.uniform(-10, 10), rng.randint(1, 4))
    if roll < 7:
        return rng.uniform(-100, 100)
    if roll == 7:
        return rng.randint(-64, 64) / 8
    if roll == 8:
        return math.ldexp(rng.uniform(-1, 1), rng.randint(-1074, 1023))
    return rng.choice((0.5, 1.0, 2.0, 3.0, 0.1, 1e300, -1e-300, 5e-324))


def _atom(rng: random.Random, names: tuple[str, ...], bound: tuple[str, ...]) -> str:
    roll = rng.random()
    if bound and roll < 0.4:
        return rng.choice(bound)
    if roll < 0.6:
        return rng.choice(names)
    if roll < 0.66:
        return rng.choice(("pi", "e"))
    return _literal_text(rng)


def _exact_source(rng: random.Random, depth: int, names: tuple[str, ...], bound: tuple[str, ...] = ()) -> str:
    roll = rng.random()
    if depth <= 0 or roll < 0.2:
        return _atom(rng, names, bound)

    def sub() -> str:
        return _exact_source(rng, depth - 1, names, bound)

    if roll < 0.45:
        return f"{sub()}{_space(rng)}{rng.choice('+-*/')}{_space(rng)}{sub()}"
    if roll < 0.52:
        return "-" + _space(rng) + sub()
    if roll < 0.64:
        return f"{rng.choice(_EXACT_ONE)}({sub()})"
    if roll < 0.72:
        return f"{rng.choice(('min', 'max'))}({', '.join(sub() for _ in range(rng.randint(2, 4)))})"
    if roll < 0.82:
        return f"if({sub()} {rng.choice(tuple(RELATIONS))} {sub()}, {sub()}, {sub()})"
    if roll < 0.9 and len(bound) < 2:
        index = rng.choice(("k", "i", "j", "x"))
        lo = rng.randint(-3, 3)
        term = _exact_source(rng, depth - 1, names, (*bound, index))
        return f"sum({index}, {_int_text(lo)}, {_int_text(lo + rng.randint(-1, 6))}, {term})"
    return f"({sub()})"


def _exact_case(rng: random.Random) -> tuple[str, dict[str, object]]:
    names = tuple(rng.sample(NAMES, rng.randint(1, 3)))
    src = _exact_source(rng, rng.randint(2, 4), names)
    scope: dict[str, object] = {name: _scope_value(rng) for name in names}
    if rng.random() < 0.03:
        del scope[names[0]]
    return src, scope


def _uniform(rng: random.Random, f: str) -> float:
    lo, hi = _DOMAIN[f]
    return power(10.0, rng.uniform(-6, 6)) if f in ("ln", "log10") else rng.uniform(lo, hi)


def _inexact_call(rng: random.Random, f: str, x: str, y: str, scope: dict[str, object]) -> str:
    """f applied to an exact argument in f's domain (once in 25 outside it), with x and y set in scope."""
    shape = rng.choice(_ARG_SHAPES)
    arg = shape.format(x=x, y=y)
    for _ in range(50):
        scope[x], scope[y] = _uniform(rng, f), _uniform(rng, f)
        v = value(arg, scope)
        lo, hi = _DOMAIN[f]
        if lo <= v <= hi or rng.random() < 0.04:
            break
    return f"{f}({arg})"


def _inexact_case(rng: random.Random) -> tuple[str, dict[str, object]] | None:
    """A random inexact line, or None when its value would sit at an edge of the parity tolerance."""
    x, y, u, w = rng.sample(NAMES, 4)
    scope: dict[str, object] = {}
    f = rng.choice(tuple(_DOMAIN))
    inner = _inexact_call(rng, f, x, y, scope)
    c = _literal_text(rng)
    style = rng.randrange(16)
    if style < 3:
        src = inner
    elif style == 3:
        src = f"{inner} * {c}"
    elif style == 4:
        src = f"{inner} / {c}"
    elif style == 5:
        src = f"-{inner}"
    elif style == 6:
        src = f"{inner} * {_inexact_call(rng, rng.choice(tuple(_DOMAIN)), u, w, scope)}"
    elif style == 7:
        src = f"{rng.choice(('min', 'max'))}({inner}, {c})"
    elif style == 8:
        g, b = rng.choice(_OUTER), rng.choice(_BOUNDED)
        inner = _inexact_call(rng, b, x, y, scope)
        src = f"{g}({inner})"
    elif style == 9:
        scope[x], scope[y] = rng.uniform(0.01, 20), rng.uniform(-8, 8)
        src = rng.choice((f"{x}^{y}", f"{x}^{c}", f"2^{y}", f"{x}^-{c}", f"(-{x})^{rng.randint(-9, 9)}", f"{x}^0.5"))
    elif style == 10:
        scope[x], scope[y] = _scope_value(rng), _scope_value(rng)
        src = rng.choice((f"atan2({x}, {y})", f"atan2({y}, {x})", f"atan2({x}, {c})", f"atan2({c}, -{y})"))
    elif style == 11:
        scope[x] = rng.uniform(0.05, 2)
        g = rng.choice(_POSITIVE)
        term = rng.choice((f"{g}(k*{x})", f"{g}(-k*{x})", f"{g}(k/{x})", f"sin(k*{x})^2", f"sqrt(k)*exp(-k*{x})"))
        if g == "Phi":
            term = rng.choice((f"Phi({x}/k)", f"Phi(-{x}/k)", f"Phi(k*{x}/30 - 1.4)"))
        if g in ("exp", "cosh") and "-" not in term:
            term = f"1/{term}"
        src = f"sum(k, 1, {rng.randint(1, 30)}, {term})"
    elif style == 12:
        v = value(inner, scope)
        if v != v or math.isinf(v):
            return None
        bound_ = v + rng.choice((-1, 1)) * max(1e-3, abs(v) * rng.uniform(0.01, 0.5))  # clear of v by 1e-3 or 1%
        src = f"if({inner} {rng.choice(('<', '<=', '>', '>='))} {_num_text(bound_)}, {c}, {x})"
    elif style == 13:
        v = value(inner, scope) * 10
        if not math.isfinite(v) or abs(v) > 1e12 or not 1e-6 < v - _floor(v) < 1 - 1e-6:
            return None
        src = f"floor({inner} * 10)"
    elif style == 14:
        v = value(inner, scope)
        if not math.isfinite(v) or v == 0:
            return None
        src = f"{inner} + {c}" if v > 0 else f"{inner} - {c}"
    else:
        src = f"abs({inner})" if rng.randrange(2) else f"sqrt(abs({inner}))"
    v = value(src, scope)
    if v == v and v != 0 and not 1e-290 < abs(v) < 1e290:
        return None
    return (src, scope) if _steady(rng, src, scope, v) and within_table(src, scope) else None


def _close(v: float, w: float) -> bool:
    """Whether the parity test would accept w for v: the same NaN, infinity or signed zero, or a relative 1e-12."""
    if v != v or w != w:
        return v != v and w != w
    if v == 0 or w == 0 or math.isinf(v) or math.isinf(w):
        return v == w and math.copysign(1.0, v) == math.copysign(1.0, w)
    return abs(v - w) <= 1e-12 * abs(v)


def _steady(rng: random.Random, src: str, scope: dict[str, object], v: float) -> bool:
    """Whether nudging every number in the scope by a relative 1e-14, a hundred times a double's rounding error,
    keeps the value where the parity test accepts it. A line that fails sits near a branch of `if` or `floor`,
    a cancellation, an underflow or a domain edge, where an error of an ulp in the TypeScript's table could move
    it past the tolerance; such a line is not drawn."""
    for _ in range(3):
        nudged = {k: x * (1 + rng.choice((-1e-14, 1e-14))) if isinstance(x, float) else x for k, x in scope.items()}
        if not _close(v, value(src, nudged)):
            return False
    return True


def _mutant(rng: random.Random, src: str) -> str:
    i = rng.randrange(len(src) + 1)
    kind = rng.randrange(4)
    if kind == 0 and i < len(src):
        return src[:i] + src[i + 1 :]
    if kind == 1 and i < len(src):
        return src[:i] + src[i] + src[i:]
    if kind == 2 and i + 1 < len(src):
        return src[:i] + src[i + 1] + src[i] + src[i + 2 :]
    return src[:i] + rng.choice("()+-*/^,.<=>e1x _!#[]\u03c0\u00b2\t") + src[i:]


@cache
def goldens() -> tuple[dict[str, object], ...]:
    rng = random.Random("zqverify.expr")
    pairs = _fixed()
    pairs += [_exact_case(rng) for _ in range(800)]
    inexact: list[tuple[str, dict[str, object]]] = []
    while len(inexact) < 900:
        picked = _inexact_case(rng)
        if picked is not None:
            inexact.append(picked)
    pairs += inexact
    mutants: list[tuple[str, dict[str, object]]] = []
    while len(mutants) < 300:
        src, scope = _exact_case(rng)
        bent = _mutant(rng, src)
        try:
            exact = Expr(bent).exact
        except ParseError:
            exact = True
        if exact:
            mutants.append((bent, scope))
    pairs += mutants
    outside = [src for src, scope in pairs if not within_table(src, scope)]
    if outside:
        raise ValueError(f"erf or Phi outside the parity table's range in {outside}")
    return tuple(case(src, scope) for src, scope in pairs)


def render() -> str:
    """JSON Lines: one case per line, so a changed case is a one-line diff."""
    return "".join(json.dumps(line) + "\n" for line in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
