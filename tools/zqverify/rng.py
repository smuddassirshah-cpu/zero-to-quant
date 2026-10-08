"""Twin of @zq/mathcore/rng: Philox4x32-10, hash32, SeedSource and Rng (docs/ARCHITECTURE.md 5.1).

Written from the plain-language specification ("Philox draws", ARCHITECTURE.md 5.1) and the sources it cites,
without reading the TypeScript (CLAUDE.md hard rule 4). Decision notes:
- Words are Python ints masked to 32 bits, with no NumPy, so no fixed-width type can wrap unseen.
- Philox4x32-10's constants and rounds are Random123's include/Random123/philox.h at commit 9545ff6
  [sourced: lines 241 and 244 (multipliers), 255 and 258 (Weyl increments), 295 to 305 (round), 307 to 312
  (key bump), 323 to 334 (ten rounds, the key bumped before every round after the first)]. The SC11 paper
  gives the same values [recalled].
- hash32 takes a number part only when it is a safe integer, |n| <= 2^53 - 1, and writes it as str(int(n)),
  which is JavaScript's String(n) there. Any other number (a fraction, |n| >= 2^53, NaN, an infinity) is the
  spec's RangeError, because above 2^53 ECMA-262's normative Number::toString does not always fix the last
  digit (only its non-normative Note 2 does) [sourced: tc39/ecma262 spec.html at 6db9135,
  sec-numeric-types-number-tostring].
- A str holds code points, and json.loads joins an escaped surrogate pair into one code point exactly as
  JSON.parse's UTF-16 does [measured: CPython 3.12.15 and Node 22.22.0], so a surrogate code point in a str
  decoded from JSON is one that JavaScript also sees unpaired. hash32 lets the strict UTF-8 codec reject it:
  UnicodeEncodeError, a ValueError subclass, is raised for exactly U+D800 to U+DFFF and nothing else, which is
  the spec's rule, at no cost beyond the encoding hash32 does anyway. An explicit check was rejected as a
  second scan.
- normal uses correctly rounded ln and cos: mpmath at 50 digits, then rounded to the nearest double through
  Fraction, whose float() rounds correctly [recalled]; the tests check each rounding on the golden inputs
  against a 100-digit reference. The TypeScript uses dmath, so normal goldens carry r for the spec's bound
  of 1e-14 max(1, r).
- Errors: each RangeError of the spec is ValueError here (UnicodeEncodeError for a lone surrogate); a value
  of a type the TypeScript signatures exclude (a bool, None, a list) is TypeError.

Goldens and the known-answer file live in packages/mathcore/test/. A golden line's `kind` is one of:
- hash32: `parts` (strings and numbers; -0.0 reads back as -0 in JSON.parse) and either the unsigned `hash`
  or `error`, which is always "RangeError": the TypeScript must throw a RangeError for those parts. Error
  lines hold number parts that are not safe integers and string parts with a lone surrogate, which the file
  writes as a \\uXXXX escape that JSON.parse reads back as one unpaired code unit. NaN and the infinities have
  no JSON form, so the TypeScript tests those RangeErrors directly;
- draw: `seed`, the stream `path` (rng(path[0]).fork(path[1])...), its `key`, index `j`, draw j's `words` [u, v]
  and `at`, the double's exact hexadecimal (float.hex);
- int: eight int(lo, hi) calls of size `n` on a fresh stream, each [lo, hi, value, position after];
- normal: twelve normal() calls on a fresh stream, each [value, r] in hexadecimal, r = sqrt(-2 ln(1 - u1));
  each value is compared within the spec's normal tolerance, 1e-14 max(1, r), using the r beside it;
- sequence: next, at, int and normal calls in turn on one fresh stream, each [name, arguments..., results...,
  position after], which pins the position rules. A normal op, ["normal", value, r, position after], follows
  the normal rule: its value is compared within 1e-14 max(1, r) using the r it carries. Every other entry of
  a sequence line, the positions included, is compared exactly.
From the repository root, rewrite the goldens with:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.rng
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterator, Sequence
from fractions import Fraction
from pathlib import Path

import mpmath

TEST_DIR = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test"
GOLDEN = TEST_DIR / "rng.golden.jsonl"
KAT = TEST_DIR / "philox4x32-10.kat.txt"

MASK = 0xFFFFFFFF
TWO32 = 1 << 32
TWO53 = 1 << 53
SAFE = TWO53 - 1  # Number.MAX_SAFE_INTEGER
M0, M1 = 0xD2511F53, 0xCD9E8D57  # PHILOX_M4x32_0 and _1
W0, W1 = 0x9E3779B9, 0xBB67AE85  # PHILOX_W32_0 (golden ratio) and _1 (sqrt(3) - 1)
ROUNDS = 10
FNV_OFFSET, FNV_PRIME = 2166136261, 16777619
SEPARATOR = "\x1f"
TAU = 6.283185307179586  # the double nearest 2 pi
DPS = 50

Words = tuple[int, int, int, int]
Part = str | int | float


def philox(counter: Words, key: tuple[int, int]) -> Words:
    """Philox4x32-10 on a counter of four 32-bit words and a key of two."""
    c0, c1, c2, c3 = counter
    k0, k1 = key
    for r in range(ROUNDS):
        if r:
            k0, k1 = (k0 + W0) & MASK, (k1 + W1) & MASK
        p0, p1 = M0 * c0, M1 * c2
        c0, c1, c2, c3 = (p1 >> 32) ^ c1 ^ k0, p1 & MASK, (p0 >> 32) ^ c3 ^ k1, p0 & MASK
    return c0, c1, c2, c3


def _integer(x: object, lo: int, hi: int, what: str) -> int:
    """x as an int when it is a number equal to an integer in [lo, hi]; ValueError (RangeError) otherwise."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise TypeError(f"{what} must be a number, not {type(x).__name__}")
    if isinstance(x, float):
        if not x.is_integer():
            raise ValueError(f"{what} {x!r} is not an integer")
        x = int(x)
    if not lo <= x <= hi:
        raise ValueError(f"{what} {x} is outside [{lo}, {hi}]")
    return x


def js_string(n: int | float) -> str:
    """String(n) for a number part, which must be a safe integer (|n| <= 2^53 - 1), else ValueError."""
    if isinstance(n, bool) or not isinstance(n, (int, float)):
        raise TypeError(f"a hash32 part must be a str or a number, not {type(n).__name__}")
    if not (isinstance(n, int) or n.is_integer()) or abs(n) > SAFE:  # NaN fails both tests
        raise ValueError(f"the number part {n!r} is not a safe integer")
    return str(int(n))  # -0.0 is written 0


def fnv1a32(data: bytes) -> int:
    h = FNV_OFFSET
    for byte in data:
        h = ((h ^ byte) * FNV_PRIME) & MASK
    return h


def hash32(*parts: Part) -> int:
    """32-bit FNV-1a over the UTF-8 bytes of the parts joined by U+001F. A str holds code points, so a surrogate
    in it is never half of a pair: it has no UTF-8 form and raises UnicodeEncodeError, a ValueError."""
    return fnv1a32(SEPARATOR.join(p if isinstance(p, str) else js_string(p) for p in parts).encode("utf-8"))


def _name(name: object) -> str:
    if not isinstance(name, str):
        raise TypeError(f"a stream name must be a str, not {type(name).__name__}")
    return name


def correctly_rounded(v: mpmath.mpf) -> float:
    man, exp = v.man_exp  # |v| = man 2^exp; mpmath drops the sign here
    q = Fraction(man) * Fraction(2) ** exp
    return float(-q if v < 0 else q)


def ln(x: float) -> float:
    with mpmath.workdps(DPS):
        return correctly_rounded(mpmath.log(mpmath.mpf(x)))


def cos(x: float) -> float:
    with mpmath.workdps(DPS):
        return correctly_rounded(mpmath.cos(mpmath.mpf(x)))


def box_muller(u1: float, u2: float) -> tuple[float, float]:
    """(sqrt(-2 ln(1 - u1)) cos(tau u2), r): one double operation per step, in the spec's order."""
    r = math.sqrt(-2.0 * ln(1.0 - u1))
    return r * cos(TAU * u2), r


class Rng:
    """A stream with key (seed, stream) and a position; at(j) is a pure function of the key and j."""

    __slots__ = ("key", "position")

    def __init__(self, seed: int, stream: int) -> None:
        self.key = (seed, stream)
        self.position = 0

    def words(self, j: object) -> tuple[int, int]:
        """Draw j's words (u, v): the halves of the block at counter (b mod 2^32, b div 2^32, 0, 0)."""
        b, h = divmod(_integer(j, 0, TWO53 - 1, "index"), 2)
        w = philox((b & MASK, b >> 32, 0, 0), self.key)
        return w[2 * h], w[2 * h + 1]

    def at(self, j: object) -> float:
        u, v = self.words(j)
        return ((u >> 5) * (1 << 26) + (v >> 6)) / TWO53  # an integer below 2^53 over 2^53: exact

    def next(self) -> float:
        x = self.at(self.position)
        self.position += 1
        return x

    def int(self, lo: object, hi: object) -> int:
        a, b = _integer(lo, -SAFE, SAFE, "lo"), _integer(hi, -SAFE, SAFE, "hi")
        n = b - a + 1
        if not 1 <= n <= TWO32:
            raise ValueError(f"int({a}, {b}) needs lo <= hi and at most 2^32 values")
        limit = TWO32 - TWO32 % n  # a multiple of n, so u mod n is uniform on u < limit
        while True:
            u = self.words(self.position)[0]
            self.position += 1
            if u < limit:
                return a + u % n

    def normal(self) -> float:
        u1 = self.next()
        return box_muller(u1, self.next())[0]

    def fork(self, name: str) -> Rng:
        return Rng(self.key[0], hash32(self.key[1], _name(name)))


class SeedSource:
    __slots__ = ("seed",)

    def __init__(self, seed: object) -> None:
        self.seed = _integer(seed, 0, MASK, "seed")

    def rng(self, name: str) -> Rng:
        return Rng(self.seed, hash32(_name(name)))


def stream(seed: int, path: Sequence[str]) -> Rng:
    """SeedSource(seed).rng(path[0]).fork(path[1]).fork(path[2])..."""
    rng = SeedSource(seed).rng(path[0])
    for name in path[1:]:
        rng = rng.fork(name)
    return rng


# The golden grid (spec: "Golden draws"). Indices cover both halves of a block, the carry into the counter's
# second word (2^32 - 1 to 2^33 + 1) and the last index.
SEEDS = (0, 1, 20261008, MASK)
PATHS = (("",), ("lsn.cond.shrinking-sample-space",), ("café π ✓ 🎲",), ("grid", "row:3"), ("grid", "row:3", ""))
INDICES = (0, 1, 2, 7, TWO32 - 1, TWO32, TWO32 + 1, 2 * TWO32, 2 * TWO32 + 1, TWO53 - 2, TWO53 - 1)
INT_SIZES = (1, 2, 3, 6, 7, 10, (1 << 31) + 1, TWO32)
HASH_CASES: tuple[tuple[Part, ...], ...] = (
    (),
    ("",),
    ("", ""),
    ("", "", ""),
    ("a",),
    ("a", "b"),
    ("a\x1fb",),
    ("foobar",),
    ("café",),
    ("π", "ß"),
    ("中文", "", "日本"),
    ("🎲", "\x00"),
    ("\ud7ff\ue000", "\uffff\U00010000\U0010ffff"),  # the code points either side of the surrogates, and the ends
    (0,),
    (-0.0,),
    (1,),
    (-1,),
    ("7",),
    (7,),
    (7.0,),
    (2**31,),
    (MASK,),
    (TWO32,),
    (SAFE,),
    (-SAFE,),
    ("lsn.cond.shrinking-sample-space", "s3"),
    ("gen.dice-sum", 4),
    ("att.0001", 2, 0),
    (MASK, "row:3"),
)
# Parts that make hash32 a RangeError. Never put a high surrogate directly before a low one in one string here:
# the file would escape them as a pair, which both JSON readers join into one valid code point.
HASH_ERRORS: tuple[tuple[Part, ...], ...] = (
    (TWO53,),
    (-TWO53,),
    (TWO53 + 2,),
    (2**54 + 4,),
    (2**54 + 8,),
    (2**57,),
    (2**59,),
    (2**64,),
    (123456789012345680,),
    (1e21,),
    (-1e21,),
    (2.0**70,),
    (1e300,),
    (0.5,),
    (-1.5,),
    (2**52 - 0.5,),  # the largest double that is a fraction, which a magnitude test alone accepts
    (5e-324,),
    ("gen.dice-sum", 4.5),
    ("\ud800",),
    ("\udfff",),
    ("a\ud83c",),  # a high surrogate at the end
    ("\udfb2a",),  # a low surrogate at the start
    ("\udfb2\ud83c",),  # low before high is no pair
    ("\ud83c\U0001f3b2",),  # a high surrogate before a valid pair
    ("\U0001f3b2\udfb2",),  # a valid pair before a low surrogate
    ("ok", "\ud800"),
    ("\ud83c", "\udfb2"),  # a pair split across parts: U+001F stands between its halves
)


SEQUENCE = (
    ("next",), ("next",), ("at", 0), ("at", 5), ("next",), ("int", 1, 6),
    ("normal",), ("at", 2), ("next",), ("int", 0, MASK), ("next",), ("normal",),
)


def _normal_hex(rng: Rng) -> list[str]:
    """One normal() call's value and its r, as exact hexadecimal."""
    u1 = rng.next()
    return [x.hex() for x in box_muller(u1, rng.next())]


def _int_calls(rng: Rng, n: int) -> list[list[int]]:
    """Eight calls of size n at the edges of the safe range: [lo, hi, value, position after]."""
    return [[lo, lo + n - 1, rng.int(lo, lo + n - 1), rng.position] for lo in (0, -7, SAFE - n + 1, -SAFE) * 2]


def _sequence(rng: Rng) -> list[list[object]]:
    """Calls of every kind in turn, each with its result and the position after it, to pin the position rules."""
    ops: list[list[object]] = []
    for name, *args in SEQUENCE:
        if name == "next":
            out: list[object] = [rng.next().hex()]
        elif name == "at":
            out = [rng.at(args[0]).hex()]
        elif name == "int":
            out = [rng.int(*args)]
        else:
            out = list(_normal_hex(rng))
        ops.append([name, *args, *out, rng.position])
    return ops


def _range_error(parts: Sequence[Part]) -> str:
    """The golden `error` for parts that the spec makes a RangeError; a hash here is a bug, so it raises."""
    try:
        h = hash32(*parts)
    except ValueError:
        return "RangeError"
    raise AssertionError(f"hash32{tuple(parts)!r} is {h}, where the spec throws RangeError")


def goldens() -> Iterator[dict[str, object]]:
    for parts in HASH_CASES:
        yield {"kind": "hash32", "parts": list(parts), "hash": hash32(*parts)}
    for parts in HASH_ERRORS:
        yield {"kind": "hash32", "parts": list(parts), "error": _range_error(parts)}
    for seed in SEEDS:
        for path in PATHS:
            rng = stream(seed, path)
            for j in INDICES:
                case = {"kind": "draw", "seed": seed, "path": list(path), "key": list(rng.key), "j": j}
                yield case | {"words": list(rng.words(j)), "at": rng.at(j).hex()}
    for seed in SEEDS[1:3]:
        for path in PATHS[1:4:2]:
            head = {"seed": seed, "path": list(path)}
            for n in INT_SIZES:
                yield {"kind": "int", **head, "n": n, "calls": _int_calls(stream(seed, path), n)}
            rng = stream(seed, path)
            yield {"kind": "normal", **head, "values": [_normal_hex(rng) for _ in range(12)]}
            yield {"kind": "sequence", **head, "ops": _sequence(stream(seed, path))}


SURROGATE = re.compile("[\ud800-\udfff]")


def _json_line(case: dict[str, object]) -> str:
    """The case as one JSON line, text as UTF-8 except surrogates, which UTF-8 cannot hold: those are \\uXXXX."""
    return SURROGATE.sub(lambda m: f"\\u{ord(m[0]):04x}", json.dumps(case, ensure_ascii=False)) + "\n"


def render() -> str:
    """JSON Lines, one case per line, so a changed case is a one-line diff."""
    return "".join(map(_json_line, goldens()))


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
