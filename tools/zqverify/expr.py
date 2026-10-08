"""Twin of @zq/mathcore/expr: the expression language of calc-linalg 2.3, parsed and evaluated independently.

The specification, in plain words (docs/blueprint/work/widgets-calc-linalg.md 2.3, with the details stage 3
fixed): numbers are decimal or scientific ("2", "0.5", ".5", "1.5e-3"; not "1."), and one that rounds to
infinity is an error; names are an ASCII letter followed by letters, digits and "_"; the operators are
+ - * / ^ and unary minus, with ^ above unary minus above * and / above + and -, ^ grouping to the right and
the rest to the left, so -x^2 is -(x^2) and 2^-1 is 0.5; multiplication is always written. The functions are
sin cos tan asin acos atan atan2 sinh cosh tanh exp ln log10 sqrt cbrt abs sign floor ceil min max (two or
more arguments) Phi phi erf, if(a < b, then, else) with exactly one of < <= > >= == (a comparison appears
nowhere else) and sum(k, lo, hi, term); pi and e are constants; every function name, if, sum, pi and e is
reserved. Sources are at most 1,000 characters with brackets nested at most 32 deep.

Values are IEEE-754 doubles. Undefined points are NaN: a / 0, 0 ^ b for b < 0, ln and log10 of x <= 0, any
NaN operand of an operator or function, an if whose comparison has a NaN side (only the chosen branch is
evaluated), a sum whose bounds are not integers of magnitude at most 2^53 - 1, and any evaluation that would
take more than 100,000 sum terms in all. A sum adds its terms from lo up to hi, starting from 0, and is 0 when
hi < lo. min and max rank -0 below +0. Every free variable needs a number in the scope.

Independence: precedence and grouping come from CPython's parser. The source is tokenised here and re-spelt as
Python (each name gains a trailing underscore, so `lambda` or `if` is an ordinary name; ^ becomes **; each
number becomes the repr of its nearest double), parsed by `ast` and walked against a whitelist. Nothing
reaches eval, exec or compile (CLAUDE.md, security floor). Where Python's grammar is wider (a trailing comma
in a call, a call on a bracketed callee, brackets round if's comparison or sum's index) the twin refuses it.
The transcendental functions are NumPy's and SciPy's, so values that use them agree with the TypeScript to a
tolerance, not to the bit.

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
from collections.abc import Callable, Mapping
from pathlib import Path

import numpy as np
from scipy import special

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "expr.golden.jsonl"
MAX_LENGTH, MAX_DEPTH, MAX_TERMS = 1000, 32, 100_000
TOKEN = re.compile(
    r"(?P<num>(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?)|(?P<name>[A-Za-z][A-Za-z0-9_]*)"
    r"|(?P<op><=|>=|==|[-+*/^(),<>])|(?P<space>[ \t\n\r]+)"
)
TABLE: dict[str, Callable[[float], float]] = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan, "asin": np.arcsin, "acos": np.arccos, "atan": np.arctan,
    "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh, "exp": np.exp, "ln": np.log, "log10": np.log10,
    "sqrt": np.sqrt, "cbrt": np.cbrt, "erf": special.erf, "Phi": special.ndtr,
    "phi": lambda x: np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi),
}  # fmt: skip
EXACT: dict[str, Callable[[float], float]] = {
    "abs": abs,
    "sign": lambda x: x if x == 0 else math.copysign(1.0, x),
    "floor": np.floor,
    "ceil": np.ceil,
}
ARITY = {**{name: (1, 1) for name in TABLE | EXACT}, "atan2": (2, 2), "min": (2, math.inf), "max": (2, math.inf)}
CONSTANTS = {"pi": math.pi, "e": math.e}
RESERVED = set(ARITY) | {"if", "sum"} | set(CONSTANTS)
NEEDS_ARGUMENTS = RESERVED - set(CONSTANTS)
RELATIONS = {ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge, ast.Eq: operator.eq}


class ExprError(ValueError):
    """The source is not in the grammar."""


class ScopeError(LookupError):
    """The scope has no number for a free variable."""


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
            if math.isinf(float(text)):
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


def check(node: ast.expr, bound: frozenset[str], free: dict[str, None]) -> None:
    """Rejects any node outside the grammar, wherever it is, and records the free variables in order."""
    match node:
        case ast.Constant(value=float()):
            pass
        case ast.Name(id=ident):
            name = ident[:-1]
            if name in NEEDS_ARGUMENTS:
                raise ExprError(f"{name} needs its arguments")
            if name not in CONSTANTS and name not in bound:
                free.setdefault(name)
        case ast.UnaryOp(op=ast.USub(), operand=x):
            check(x, bound, free)
        case ast.BinOp(op=ast.Add() | ast.Sub() | ast.Mult() | ast.Div() | ast.Pow(), left=a, right=b):
            check(a, bound, free)
            check(b, bound, free)
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
                for part in (cond.left, cond.comparators[0], args[1], args[2]):
                    check(part, bound, free)
            elif name == "sum":
                if len(args) != 4 or not bare or not isinstance(args[0], ast.Name) or args[0].id[:-1] in RESERVED:
                    raise ExprError("sum needs (index, lo, hi, term)")
                check(args[1], bound, free)
                check(args[2], bound, free)
                check(args[3], bound | {args[0].id[:-1]}, free)
            elif name in ARITY and ARITY[name][0] <= len(args) <= ARITY[name][1]:
                for a in args:
                    check(a, bound, free)
            else:
                raise ExprError(f"{name} is not a function of {len(args)} arguments")
        case _:
            raise ExprError(f"{type(node).__name__} is outside the grammar")


def is_relation(node: ast.expr) -> bool:
    return isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in RELATIONS


def parse(source: str) -> tuple[ast.expr, list[str]]:
    """The checked tree and its free variables in order of first appearance."""
    try:
        tree = ast.parse(respell(source), mode="eval")
    except SyntaxError as err:
        raise ExprError(f"syntax: {err.msg}") from err
    free: dict[str, None] = {}
    check(tree.body, frozenset(), free)
    return tree.body, list(free)


def evaluate(source: str, scope: Mapping[str, float]) -> float:
    body, free = parse(source)
    env: dict[str, float] = {}
    for name in free:
        value = scope.get(name)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ScopeError(name)
        env[name] = float(value)
    with np.errstate(all="ignore"):
        return value_of(body, env, [MAX_TERMS])


def value_of(node: ast.expr, env: dict[str, float], budget: list[int]) -> float:
    def of(n: ast.expr) -> float:
        return value_of(n, env, budget)

    match node:
        case ast.Constant(value=float() as v):
            return v
        case ast.Name(id=ident):
            return CONSTANTS.get(ident[:-1], env.get(ident[:-1], math.nan))
        case ast.UnaryOp(operand=x):
            return -of(x)
        case ast.BinOp(op=op, left=a, right=b):
            x, y = of(a), of(b)
            if isinstance(op, ast.Add):
                return x + y
            if isinstance(op, ast.Sub):
                return x - y
            if isinstance(op, ast.Mult):
                return x * y
            if isinstance(op, ast.Div):
                return math.nan if y == 0 else x / y
            return math.nan if math.isnan(x) or math.isnan(y) or (x == 0 and y < 0) else float(np.power(x, y))
        case ast.Call(func=ast.Name(id=ident), args=args):
            name = ident[:-1]
            if name == "if":
                cond = args[0]
                assert isinstance(cond, ast.Compare)
                x, y = of(cond.left), of(cond.comparators[0])
                if math.isnan(x) or math.isnan(y):
                    return math.nan
                return of(args[1] if RELATIONS[type(cond.ops[0])](x, y) else args[2])
            if name == "sum":
                return total(args, env, budget)
            xs = [of(a) for a in args]
            if any(math.isnan(x) for x in xs):
                return math.nan
            if name in ("min", "max"):
                return (min if name == "min" else max)(xs, key=lambda x: (x, math.copysign(1.0, x)))
            if name == "atan2":
                return float(np.arctan2(xs[0], xs[1]))
            if name in ("ln", "log10") and not xs[0] > 0:
                return math.nan
            return float((TABLE | EXACT)[name](xs[0]))
    raise AssertionError("check() admits no other node")


def total(args: list[ast.expr], env: dict[str, float], budget: list[int]) -> float:
    index = args[0]
    assert isinstance(index, ast.Name)
    lo, hi = value_of(args[1], env, budget), value_of(args[2], env, budget)
    if not all(v.is_integer() and abs(v) <= 2**53 - 1 for v in (lo, hi)):
        return math.nan
    count = max(0, int(hi) - int(lo) + 1)
    if count > budget[0]:
        return math.nan
    budget[0] -= count
    inner, acc = dict(env), 0.0
    for i in range(count):
        inner[index.id[:-1]] = lo + i
        acc += value_of(args[3], inner, budget)
    return acc


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
    ("exp(1)", {}), ("ln(2)", {}), ("sqrt(2)", {}), ("cbrt(-27)", {}), ("abs(-3)", {}), ("sign(-2)", {}),
    ("sign(0)", {}), ("sign(-0)", {}), ("floor(-2.5)", {}), ("ceil(-0.5)", {}), ("Phi(1.5)", {}),
    ("Phi(-2)", {}), ("phi(0.5)", {}), ("erf(0.75)", {}), ("min(3, x, -1)", {"x": 2.0}), ("max(-0, 0)", {}),
    ("min(0, -0)", {}), ("max(1, 0/0, 2)", {}), ("if(x < 0, -x, x)", {"x": -3.0}),
    ("if(x == 0, 1, sin(x)/x)", {"x": 0.0}), ("if(x <= y, 1, 2)", {"x": 2.0, "y": 2.0}),
    ("if(x >= 1, 1, 2) + if(x > 1, 10, 20)", {"x": 1.0}), ("if(0/0 < 1, 1, 2)", {}), ("sum(k, 1, 10, k^2)", {}),
    ("sum(k, 1, n, 1/k)", {"n": 100.0}), ("sum(k, 3, 2, k)", {}), ("sum(k, 0.5, 2, k)", {}),
    ("sum(k, -2, 2, k*k)", {}), ("sum(x, 1, 3, x) + x", {"x": 10.0}), ("sum(k, 1, k, k)", {"k": 4.0}),
    ("sum(i, 1, 400, sum(j, 1, 249, 1))", {}), ("sum(i, 1, 400, sum(j, 1, 250, 1))", {}),
    ("sum(k, 1, 100001, 1)", {}), ("sum(k, 9007199254740990, 9007199254740991, 1)", {}),
    ("sum(k, 9007199254740992, 9007199254740992, 1)", {}), ("lambda*2", {"lambda": 3.0}),
    ("W_t + x_1", {"W_t": 1.0, "x_1": 2.0}), ("constructor + prototype", {"constructor": 1.0, "prototype": 2.0}),
    ("(" * 32 + "1" + ")" * 32, {}), (" 1 +\t2\n", {}), ("if((x) < 0, 1, 2)", {"x": -1.0}),
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
    ("sum((k), 1, 2, k)", {}), ("sin()", {}), ("()", {}),
]  # fmt: skip
RELS = ["<", "<=", ">", ">=", "=="]
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
        atom = f"{rng.choice(['abs', 'sign', 'floor', 'ceil'])}({expression(rng, depth - 1)})"
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
