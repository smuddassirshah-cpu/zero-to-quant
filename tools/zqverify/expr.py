"""Twin of @zq/mathcore/expr: the expression language of calc-linalg 2.3, parsed and evaluated independently.

The specification, in plain words (docs/blueprint/work/widgets-calc-linalg.md 2.3, with the details stage 3
fixed): numbers are decimal or scientific ("2", "0.5", ".5", "1.5e-3"; not "1.") in ASCII digits, with at most
20 significant digits (from the first non-zero digit to the last), and one that rounds to infinity is an error;
names are an ASCII letter followed by letters, digits and "_"; the operators are + - * / ^ and unary minus,
with ^ above unary minus above * and / above + and -, ^ grouping to the right and the rest to the left, so
-x^2 is -(x^2) and 2^-1 is 0.5; multiplication is always written. The functions are sin cos tan asin acos atan
atan2 sinh cosh tanh exp ln log10 sqrt cbrt abs sign floor ceil min max (two or more arguments) Phi phi erf,
if(a < b, then, else) with exactly one of < <= > >= == (a comparison appears nowhere else) and
sum(k, lo, hi, term); pi and e are constants; every function name, if, sum, pi and e is reserved. Sources are
at most 1,000 characters with brackets nested at most 32 deep.

Values are IEEE-754 doubles. Undefined points are NaN: a / 0, 0 ^ b for b < 0, ln and log10 of x <= 0, any
NaN operand of an operator or function, an if whose comparison has a NaN side (only the chosen branch is
evaluated), a sum whose bounds are not integers of magnitude at most 2^53 - 1, and any evaluation whose sums
cost more than 1,000,000 in all. A sum costs its number of terms times the number of nodes in its term, where
each number, constant, variable, unary minus, operator, function call, if and sum is one node, a comparison
belongs to its if and the index to its sum. (+-1) ^ (+-inf) is 1. A sum adds its terms from lo up to hi,
starting from 0, and is 0 when hi < lo. min and max rank -0 below +0. Every free variable needs a number.

Each operation's value is its correctly rounded result: + - * / and sqrt in IEEE arithmetic, abs sign floor
ceil min max exactly, the other functions and ^ from mpmath at 50 digits rounded to the nearest double, with
C99 Annex F's special values (F.9, F.10) where an argument is infinite or a zero's sign matters, since mpmath
has no signed zero. No NumPy and no libm transcendental runs, so the goldens are the same on every CPU (stage
3's review measured NumPy's SIMD paths changing three of them). The TypeScript, with Math's functions or
dmath's, agrees to a tolerance where a table function or ^ runs, and to the bit elsewhere.

Parsing: precedence and grouping come from CPython's parser. The source is tokenised here and re-spelt as
Python (each name gains a trailing underscore, so `lambda` or `if` is an ordinary name; ^ becomes **; each
number becomes the repr of its nearest double), parsed by `ast` and walked against a whitelist. Nothing
reaches eval, exec or compile (CLAUDE.md, security floor). Where Python's grammar is wider (a trailing comma
in a call, a call on a bracketed callee, brackets round if's comparison or sum's index) the twin refuses it.

Independence: the session that wrote the TypeScript wrote this twin, after it, so it falls short of hard rule
4's "written without reading the TypeScript". It stays as a cross-check until a twin written blind from the
plain-language specification replaces it (stage 3's adversarial review of 8 October 2026).

From the repository root, rewrite the goldens with:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.expr
"""

from __future__ import annotations

import ast
import json
import math
import operator
import random
import re
import sys
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path

import mpmath

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "expr.golden.jsonl"
MAX_LENGTH, MAX_DEPTH, MAX_WORK, MAX_DIGITS = 1000, 32, 1_000_000, 20
DPS = 50
# A tree nests up to MAX_LENGTH deep (999 unary minuses) and check and value_of take a frame a level, so ten
# times that leaves room for the caller's frames [our choice].
FRAMES = 10 * MAX_LENGTH
INF, NAN = math.inf, math.nan
TOKEN = re.compile(
    r"(?P<num>(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)|(?P<name>[A-Za-z][A-Za-z0-9_]*)"
    r"|(?P<op><=|>=|==|[-+*/^(),<>])|(?P<space>[ \t\n\r]+)",
    re.ASCII,
)


def nearest(v: mpmath.mpf) -> float:
    """v rounded to the nearest double, ties to even: CPython's int true division rounds correctly."""
    if not v:
        return 0.0
    if mpmath.mag(v) > 1100:
        return math.copysign(INF, v)
    if mpmath.mag(v) < -1100:
        return math.copysign(0.0, v)
    man, exp = v.man_exp  # mpmath keeps the sign apart
    man = -man if v < 0 else man
    try:
        return float(man << exp) if exp >= 0 else man / (1 << -exp)
    except OverflowError:
        return math.copysign(INF, v)


def _cbrt(v: mpmath.mpf) -> mpmath.mpf:
    return mpmath.sign(v) * mpmath.cbrt(abs(v))


TABLE: dict[str, Callable[[mpmath.mpf], object]] = {
    "sin": mpmath.sin, "cos": mpmath.cos, "tan": mpmath.tan, "asin": mpmath.asin, "acos": mpmath.acos,
    "atan": mpmath.atan, "sinh": mpmath.sinh, "cosh": mpmath.cosh, "tanh": mpmath.tanh, "exp": mpmath.exp,
    "ln": mpmath.log, "log10": mpmath.log10, "cbrt": _cbrt, "erf": mpmath.erf, "Phi": mpmath.ncdf,
    "phi": mpmath.npdf,
}  # fmt: skip
with mpmath.workdps(DPS):
    PI, HALF_PI, QUARTER_PI, THREE_QUARTERS_PI = (nearest(mpmath.pi * k) for k in (1, 0.5, 0.25, 0.75))
# Annex F's values at +inf and -inf; ln and log10 refuse x <= 0 before they are asked.
AT_INFINITY = {
    "sin": (NAN, NAN), "cos": (NAN, NAN), "tan": (NAN, NAN), "asin": (NAN, NAN), "acos": (NAN, NAN),
    "atan": (HALF_PI, -HALF_PI), "sinh": (INF, -INF), "cosh": (INF, INF), "tanh": (1.0, -1.0),
    "exp": (INF, 0.0), "ln": (INF, NAN), "log10": (INF, NAN), "cbrt": (INF, -INF),
}  # fmt: skip
# Beyond these bounds, infinities included, the correctly rounded value is the limit: erf rounds to +-1 from
# |x| = 5.93, Phi to 1 from 8.3 and to 0 below -38.4, phi to 0 beyond 38.5 [measured, mpmath at 50 digits].
# They also keep mpmath's ncdf from overflowing, which it does near -1e300 [measured].
SATURATED = {"erf": (6.0, 1.0, -1.0), "Phi": (40.0, 1.0, 0.0), "phi": (40.0, 0.0, 0.0)}
ODD = {"sin", "tan", "asin", "atan", "sinh", "tanh", "cbrt", "erf"}  # f(-0) is -0


def table(name: str, x: float) -> float:
    if name in SATURATED and abs(x) > SATURATED[name][0]:
        return SATURATED[name][1 if x > 0 else 2]
    if math.isinf(x):
        return AT_INFINITY[name][x < 0]
    if x == 0 and name in ODD:
        return x
    with mpmath.workdps(DPS):
        v = TABLE[name](mpmath.mpf(x))
    return nearest(v) if isinstance(v, mpmath.mpf) else NAN  # mpmath answers outside the reals with mpc


def rounded(f: Callable[[float], int]) -> Callable[[float], float]:
    """floor or ceil, keeping the sign of a zero result (ceil(-0.5) is -0) as IEEE-754 does."""
    return lambda x: x if not math.isfinite(x) or x == 0 else math.copysign(float(f(x)), x)


EXACT: dict[str, Callable[[float], float]] = {
    "abs": abs,
    "sign": lambda x: x if x == 0 else math.copysign(1.0, x),
    "floor": rounded(math.floor),
    "ceil": rounded(math.ceil),
    "sqrt": lambda x: NAN if x < 0 else math.sqrt(x),
}
ARITY = {**{name: (1, 1) for name in TABLE | EXACT}, "atan2": (2, 2), "min": (2, math.inf), "max": (2, math.inf)}
CONSTANTS = {"pi": math.pi, "e": math.e}
RESERVED = set(ARITY) | {"if", "sum"} | set(CONSTANTS)
NEEDS_ARGUMENTS = RESERVED - set(CONSTANTS)
RELATIONS = {ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge, ast.Eq: operator.eq}


def atan2(y: float, x: float) -> float:
    """Annex F.9.1.4 where an argument is infinite or y is a zero; mpmath elsewhere."""
    if math.isinf(y):
        return math.copysign(QUARTER_PI if x == INF else THREE_QUARTERS_PI if x == -INF else HALF_PI, y)
    if math.isinf(x) or y == 0:
        return math.copysign(0.0 if math.copysign(1.0, x) > 0 else PI, y)
    with mpmath.workdps(DPS):
        return nearest(mpmath.atan2(y, x))


def power(x: float, y: float) -> float:
    """x ^ y: the language's rules, then Annex F.9.4.4's special values, then mpmath."""
    if math.isnan(x) or math.isnan(y) or (x == 0 and y < 0):
        return NAN
    if y == 0 or (abs(x) == 1 and math.isinf(y)):
        return 1.0
    odd = y.is_integer() and y % 2 == 1
    if x == 0:
        return x if odd else 0.0
    if math.isinf(y):
        return (INF if y > 0 else 0.0) if abs(x) > 1 else (0.0 if y > 0 else INF)
    if math.isinf(x):
        r = INF if y > 0 else 0.0
        return -r if x < 0 and odd else r
    if x < 0 and not y.is_integer():
        return NAN
    with mpmath.workdps(DPS):
        return nearest(mpmath.power(mpmath.mpf(x), mpmath.mpf(y)))


class ExprError(ValueError):
    """The source is not in the grammar."""


class ScopeError(LookupError):
    """The scope has no number for a free variable."""


@contextmanager
def deep() -> Iterator[None]:
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, FRAMES))
    try:
        yield
    finally:
        sys.setrecursionlimit(old)


def respell(source: str) -> str:
    """The source as Python text, or ExprError for a character, number, length or depth outside the grammar."""
    if len(source) > MAX_LENGTH:
        raise ExprError("length")
    out: list[str] = []
    depth = pos = 0
    prev = ""
    while pos < len(source):
        m = TOKEN.match(source, pos)
        if m is None:
            raise ExprError(f"character at {pos}")
        pos, kind, text = m.end(), m.lastgroup, m.group()
        if kind == "num":
            if len(re.sub(r"[eE].*", "", text).replace(".", "").strip("0")) > MAX_DIGITS or math.isinf(float(text)):
                raise ExprError("number")
            out.append(repr(float(text)))
        elif kind == "name":
            out.append(text + "_")
        elif kind == "op":
            depth += (text == "(") - (text == ")")
            if depth > MAX_DEPTH:
                raise ExprError("depth")
            # Python accepts a trailing comma in a call and a call on a bracketed callee; the grammar has neither.
            if (prev, text) in ((",", ")"), (")", "(")):
                raise ExprError(f"{prev}{text} at {m.start()}")
            out.append("**" if text == "^" else text)
        if kind != "space":
            prev = text
    return " ".join(out)


Sizes = dict[int, int]  # id of each sum's Call node: the node count of its term


def check(node: ast.expr, bound: frozenset[str], free: dict[str, None], sizes: Sizes) -> int:
    """Rejects any node outside the grammar, wherever it is; records the free variables in order and each
    sum's term size; returns the node count."""
    match node:
        case ast.Constant(value=float()):
            return 1
        case ast.Name(id=ident):
            name = ident[:-1]
            if name in NEEDS_ARGUMENTS:
                raise ExprError(f"{name} needs its arguments")
            if name not in CONSTANTS and name not in bound:
                free.setdefault(name)
            return 1
        case ast.UnaryOp(op=ast.USub(), operand=x):
            return 1 + check(x, bound, free, sizes)
        case ast.BinOp(op=ast.Add() | ast.Sub() | ast.Mult() | ast.Div() | ast.Pow(), left=a, right=b):
            return 1 + check(a, bound, free, sizes) + check(b, bound, free, sizes)
        case ast.Call(func=ast.Name(id=ident) as func, args=args, keywords=[]) if not any(
            isinstance(a, ast.Starred) for a in args
        ):
            name = ident[:-1]
            # ast drops brackets: a first argument that starts after "name ( " was bracketed, which if's
            # comparison and sum's index may not be.
            bare = bool(args) and args[0].col_offset == (func.end_col_offset or 0) + 3
            if name == "if":
                if len(args) != 3 or not bare or not is_relation(args[0]):
                    raise ExprError("if needs (a < b, then, else)")
                cond = args[0]
                assert isinstance(cond, ast.Compare)
                parts = [cond.left, cond.comparators[0], args[1], args[2]]
            elif name == "sum":
                if len(args) != 4 or not bare or not isinstance(args[0], ast.Name) or args[0].id[:-1] in RESERVED:
                    raise ExprError("sum needs (index, lo, hi, term)")
                bounds = check(args[1], bound, free, sizes) + check(args[2], bound, free, sizes)
                sizes[id(node)] = check(args[3], bound | {args[0].id[:-1]}, free, sizes)
                return 1 + bounds + sizes[id(node)]
            elif name in ARITY and ARITY[name][0] <= len(args) <= ARITY[name][1]:
                parts = args
            else:
                raise ExprError(f"{name} is not a function of {len(args)} arguments")
            count = 1
            for part in parts:
                count += check(part, bound, free, sizes)
            return count
        case _:
            raise ExprError(f"{type(node).__name__} is outside the grammar")


def is_relation(node: ast.expr) -> bool:
    return isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in RELATIONS


def parse(source: str) -> tuple[ast.expr, list[str], Sizes]:
    """The checked tree, its free variables in order of first appearance, and its sums' term sizes."""
    try:
        tree = ast.parse(respell(source), mode="eval")
    except SyntaxError as err:
        raise ExprError(f"syntax: {err.msg}") from err
    free: dict[str, None] = {}
    sizes: Sizes = {}
    with deep():
        check(tree.body, frozenset(), free, sizes)
    return tree.body, list(free), sizes


def evaluate(source: str, scope: Mapping[str, float]) -> float:
    body, free, sizes = parse(source)
    env: dict[str, float] = {}
    for name in free:
        value = scope.get(name)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ScopeError(name)
        env[name] = float(value)
    with deep():
        return value_of(body, env, sizes, [MAX_WORK])


def value_of(node: ast.expr, env: dict[str, float], sizes: Sizes, budget: list[int]) -> float:
    match node:
        case ast.Constant(value=float() as v):
            return v
        case ast.Name(id=ident):
            return CONSTANTS.get(ident[:-1], env.get(ident[:-1], NAN))
        case ast.UnaryOp(operand=x):
            return -value_of(x, env, sizes, budget)
        case ast.BinOp(op=op, left=a, right=b):
            x, y = value_of(a, env, sizes, budget), value_of(b, env, sizes, budget)
            if isinstance(op, ast.Add):
                return x + y
            if isinstance(op, ast.Sub):
                return x - y
            if isinstance(op, ast.Mult):
                return x * y
            if isinstance(op, ast.Div):
                return NAN if y == 0 else x / y
            return power(x, y)
        case ast.Call(func=ast.Name(id=ident), args=args):
            name = ident[:-1]
            if name == "if":
                cond = args[0]
                assert isinstance(cond, ast.Compare)
                x, y = value_of(cond.left, env, sizes, budget), value_of(cond.comparators[0], env, sizes, budget)
                if math.isnan(x) or math.isnan(y):
                    return NAN
                return value_of(args[1] if RELATIONS[type(cond.ops[0])](x, y) else args[2], env, sizes, budget)
            if name == "sum":
                return total(node, env, sizes, budget)
            xs = [value_of(a, env, sizes, budget) for a in args]
            if any(math.isnan(x) for x in xs):
                return NAN
            if name in ("min", "max"):
                return (min if name == "min" else max)(xs, key=lambda x: (x, math.copysign(1.0, x)))
            if name == "atan2":
                return atan2(xs[0], xs[1])
            if name in ("ln", "log10") and not xs[0] > 0:
                return NAN
            return EXACT[name](xs[0]) if name in EXACT else table(name, xs[0])
    raise AssertionError("check() admits no other node")


def total(node: ast.Call, env: dict[str, float], sizes: Sizes, budget: list[int]) -> float:
    index, lo_node, hi_node, term = node.args
    assert isinstance(index, ast.Name)
    lo, hi = value_of(lo_node, env, sizes, budget), value_of(hi_node, env, sizes, budget)
    if not all(v.is_integer() and abs(v) <= 2**53 - 1 for v in (lo, hi)):
        return NAN
    count = max(0, int(hi) - int(lo) + 1)
    cost = count * sizes[id(node)]
    if cost > budget[0]:
        return NAN
    budget[0] -= cost
    inner, acc = dict(env), 0.0
    for i in range(count):
        inner[index.id[:-1]] = lo + i
        acc += value_of(term, inner, sizes, budget)
    return acc


def wide(hi: int) -> str:
    """A sum whose term has 500 nodes but runs four of them a term: 2,000 terms cost exactly MAX_WORK."""
    return f"sum(k, 1, {hi}, if(k < 0, {'-' * 495}k, 1))"


INF_TEXT = "1e308*10"
# Hand-picked cases: grouping, every function, every NaN rule, the limits and the errors. Each scope is the
# variables the case reads; the generated cases below read x, y, z and k.
HAND: list[tuple[str, dict[str, float]]] = [
    ("1 + 2*3", {}), ("(1 + 2)*3", {}), ("2^3^2", {}), ("-2^2", {}), ("2^-1", {}), ("-2^-2^-1", {}),
    ("(-2)^2", {}), ("x - y - z", {"x": 1.0, "y": 2.0, "z": 3.0}), ("x/y/z", {"x": 1.0, "y": 2.0, "z": 3.0}),
    ("x/y*z", {"x": 1.0, "y": 3.0, "z": 3.0}), ("--x", {"x": 2.0}), ("x*-y", {"x": 2.0, "y": 3.0}),
    ("x - -y", {"x": 2.0, "y": 3.0}), ("0.1 + 0.2", {}), (".5 + 007 + 1.5e-3*2E3", {}), ("1e+21^2", {}),
    ("pi", {}), ("e", {}), ("1/0", {}), ("-1/0", {}), ("0/0", {}), ("0^-1", {}), ("0^0", {}), ("ln(0)", {}),
    ("ln(-1)", {}), ("log10(1000)", {}), ("sqrt(-1)", {}), ("asin(2)", {}), ("(-8)^(1/3)", {}), ("1^(0/0)", {}),
    ("(0/0)^0", {}), ("1e308*10", {}), ("-1e308*10", {}), ("1e308*10 - 1e308*10", {}), ("exp(1000)", {}),
    ("sin(1)", {}), ("cos(1)", {}), ("tan(1)", {}), ("asin(0.5)", {}), ("acos(0.5)", {}), ("atan(2)", {}),
    ("atan2(1, -1)", {}), ("atan2(0, 0)", {}), ("sinh(1)", {}), ("cosh(1)", {}), ("tanh(0.5)", {}),
    ("exp(1)", {}), ("ln(2)", {}), ("sqrt(2)", {}), ("sqrt(-0)", {}), ("cbrt(-27)", {}), ("abs(-3)", {}),
    ("sign(-2)", {}), ("sign(0)", {}), ("sign(-0)", {}), ("floor(-2.5)", {}), ("ceil(-0.5)", {}),
    ("Phi(1.5)", {}), ("Phi(-2)", {}), ("phi(0.5)", {}), ("erf(0.75)", {}), ("min(3, x, -1)", {"x": 2.0}),
    ("max(-0, 0)", {}), ("min(0, -0)", {}), ("max(1, 0/0, 2)", {}), ("if(x < 0, -x, x)", {"x": -3.0}),
    ("if(x == 0, 1, sin(x)/x)", {"x": 0.0}), ("if(x <= y, 1, 2)", {"x": 2.0, "y": 2.0}),
    ("if(x >= 1, 1, 2) + if(x > 1, 10, 20)", {"x": 1.0}), ("if(0/0 < 1, 1, 2)", {}), ("sum(k, 1, 10, k^2)", {}),
    ("sum(k, 1, n, 1/k)", {"n": 100.0}), ("sum(k, 3, 2, k)", {}), ("sum(k, 0.5, 2, k)", {}),
    ("sum(k, -2, 2, k*k)", {}), ("sum(x, 1, 3, x) + x", {"x": 10.0}), ("sum(k, 1, k, k)", {"k": 4.0}),
    ("sum(k, 9007199254740990, 9007199254740991, 1)", {}), ("sum(k, 9007199254740992, 9007199254740992, 1)", {}),
    ("lambda*2", {"lambda": 3.0}), ("W_t + x_1", {"W_t": 1.0, "x_1": 2.0}),
    ("constructor + prototype", {"constructor": 1.0, "prototype": 2.0}), ("(" * 32 + "1" + ")" * 32, {}),
    (" 1 +\t2\n", {}), ("if((x) < 0, 1, 2)", {"x": -1.0}),
    # ^ at the language's own special values, and Annex F's where NumPy's power departs from it
    (f"1^({INF_TEXT})", {}), (f"1^(-{INF_TEXT})", {}), (f"(-1)^({INF_TEXT})", {}), (f"(-1)^(-{INF_TEXT})", {}),
    (f"min(-1, (1)^(({INF_TEXT})))", {}), (f"(-{INF_TEXT})^0.5", {}), ("(-0)^0.5", {}), ("(-0)^3", {}),
    # the work budget: a term's nodes count whether or not they run
    (wide(2000), {}), (wide(2001), {}), ("sum(i, 1, 400, sum(j, 1, 2496, 1))", {}),
    ("sum(i, 1, 400, sum(j, 1, 2497, 1))", {}), ("sum(k, 1, 1000001, 1)", {}),
    # the deepest trees the limits allow
    ("-" * 999 + "1", {}), ("2^" * 499 + "1", {}), ("1" + "-1" * 499, {}), ("1" + "+1" * 499, {}),
    ("(" * 32 + "-" * 935 + "1" + ")" * 32, {}),
    # significant digits: at most 20, from the first non-zero digit to the last
    ("12345678901234567890", {}), ("100000000000000000000000000", {}), ("1.000000000000000000000000000", {}),
    ("0.00012345678901234567890e3", {}),
    # errors
    ("", {}), ("2x", {"x": 1.0}), ("x y", {"x": 1.0, "y": 1.0}), ("1.", {}), ("1.e5", {}), ("2**3", {}),
    ("+1", {}), ("sin", {}), ("sin(1, 2)", {}), ("min(1)", {}), ("atan2(1)", {}), ("foo(1)", {}),
    ("x(1)", {"x": 1.0}), ("pi(1)", {}), ("x < 1", {"x": 1.0}), ("(1 < 2) + 1", {}), ("if(x, 1, 2)", {"x": 1.0}),
    ("if(1 < 2 < 3, 1, 2)", {}), ("if(1 < 2, 1)", {}), ("sum(pi, 1, 2, 3)", {}), ("sum(1, 1, 2, 3)", {}),
    ("1e999", {}), ("x[0]", {"x": 1.0}), ("x.y", {"x": 1.0}), ("__proto__", {}), ("_x", {}), ("1_000", {}),
    ("0x10", {}), ("if(x < 0, 1, sin)", {"x": -1.0}), ("1 = 1", {}), ("1 != 2", {}), ("(1, 2)", {}),
    ("(" * 33 + "1" + ")" * 33, {}), ("(1", {}), ("1)", {}), ("x", {}), ("x + y", {"x": 1.0}),
    ("constructor(1)", {}), ("toString", {}), ("1" + " + 1" * 250, {}), ("π", {}), ("x²", {"x": 1.0}),
    ("sin(1,)", {}), ("min(1, 2,)", {}), ("(sin)(1)", {}), ("sin(1)(2)", {}), ("if((1 < 2), 1, 2)", {}),
    ("sum((k), 1, 2, k)", {}), ("sin()", {}), ("()", {}), ("123456789012345678901", {}),
    ("1.00000000000000011102230246251565404236316680908203125", {}), ("١ + 1", {}), ("１ + 1", {}),
    ("1٣", {}), ("\U0001d7cf*2", {}), ("x٣", {"x": 1.0}),
]  # fmt: skip
RELS = ["<", "<=", ">", ">=", "=="]
# Edge arguments for every function of one or two arguments and for ^: the zeros, +-1, +-inf, NaN and two
# ordinary values, so that the special values, not only the rounding, are compared.
EDGES = ["0", "-0", "1", "-1", "0.5", "-0.5", "2", "-2", INF_TEXT, f"-{INF_TEXT}", "0/0"]
# Token soup: random strings over the grammar's pieces, nearly all outside it, so that the two parsers are
# checked to accept and refuse the same texts.
SOUP = ["x", "y", "k", "1", "2.5", "pi", "e", "e5", ".", "sin", "min", "atan2", "if", "sum", "(", ")", ",", "+", "-",
        "*", "/", "^", "<", "<=", "=="]  # fmt: skip


def operand(rng: random.Random, depth: int) -> str:
    """A random operand built from the exact operations only, so its value is identical to the bit."""
    roll = rng.random()
    if depth <= 0 or roll < 0.35:
        atom = rng.choice(["x", "y", "z", "k", "pi", "e", str(rng.randint(1, 12)), "2.5", ".75", "1.5e3", "2E-2"])
    elif roll < 0.55:
        atom = f"({expression(rng, depth - 1)})"
    elif roll < 0.7:
        atom = f"{rng.choice(['abs', 'sign', 'floor', 'ceil', 'sqrt'])}({expression(rng, depth - 1)})"
    elif roll < 0.8:
        args = ", ".join(expression(rng, depth - 1) for _ in range(rng.randint(2, 3)))
        atom = f"{rng.choice(['min', 'max'])}({args})"
    elif roll < 0.9:
        a, b, t, f = (expression(rng, depth - 1) for _ in range(4))
        atom = f"if({a} {rng.choice(RELS)} {b}, {t}, {f})"
    else:
        atom = f"sum(k, {rng.randint(1, 3)}, {rng.randint(0, 6)}, {expression(rng, depth - 1)})"
    return "-" * rng.choice([0, 0, 0, 1, 2]) + atom


def expression(rng: random.Random, depth: int) -> str:
    parts = [operand(rng, depth)]
    for _ in range(rng.randint(0, 2)):
        parts += [rng.choice("+-*/"), operand(rng, depth)]
    return " ".join(parts)


def encode(value: float) -> float | str:
    return value if math.isfinite(value) else str(value)


def case(source: str, scope: dict[str, float]) -> dict[str, object]:
    out: dict[str, object] = {"src": source, "scope": scope}
    try:
        out["free"] = parse(source)[1]
        out["value"] = encode(evaluate(source, scope))
    except ExprError:
        return out | {"error": "parse"}
    except ScopeError:
        return out | {"error": "scope"}
    names = set(re.findall(r"[A-Za-z][A-Za-z0-9_]*|\^", source))
    return out | {"exact": not names & (set(TABLE) | {"atan2", "^"})}


def goldens() -> list[dict[str, object]]:
    rng = random.Random("zqverify.expr")
    cases = [case(source, scope) for source, scope in HAND]
    cases += [case(f"{name}({a})", {}) for name in [*TABLE, "sqrt"] for a in EDGES]
    cases += [case(f"atan2({a}, {b})", {}) for a in EDGES for b in EDGES]
    cases += [case(f"({a})^({b})", {}) for a in EDGES for b in EDGES]
    for _ in range(300):
        scope = {name: rng.choice([-0.0, 1.0, -2.0, 0.5, 3.0, round(rng.uniform(-10, 10), 3)]) for name in "xyzk"}
        cases.append(case(expression(rng, 3), scope))
    for _ in range(1000):
        soup = "".join(rng.choice(SOUP) + rng.choice(["", " "]) for _ in range(rng.randint(1, 14)))
        cases.append(case(soup, {"x": 1.5, "y": -2.0, "k": 3.0}))
    return cases


def render() -> str:
    return "".join(json.dumps(c) + "\n" for c in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
