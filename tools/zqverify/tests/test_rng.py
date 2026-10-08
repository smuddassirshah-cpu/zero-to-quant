"""The rng twin against Random123's known answers, FNV's published vectors, the spec's rules and fresh goldens."""

from __future__ import annotations

import math

import pytest
from hypothesis import given, strategies as st

from zqverify import rng as R

U32 = st.integers(0, R.MASK)
INDEX = st.integers(0, R.TWO53 - 1)
NAME = st.text(max_size=12)


def kat_lines() -> list[list[str]]:
    lines = R.KAT.read_text(encoding="utf-8").splitlines()
    return [line.split() for line in lines if line.strip() and not line.startswith("#")]


def test_the_committed_goldens_are_fresh() -> None:
    assert R.GOLDEN.read_text(encoding="utf-8") == R.render()


def test_the_known_answer_file_holds_random123s_philox4x32_10_lines() -> None:
    lines = kat_lines()
    assert len(lines) == 55 and all(len(f) == 12 and f[:2] == ["philox4x32", "10"] for f in lines)
    assert lines[0][2:8] == ["00000000"] * 6


@pytest.mark.parametrize("fields", kat_lines(), ids=lambda f: "-".join(f[2:8]))
def test_philox_meets_random123s_known_answers(fields: list[str]) -> None:
    c0, c1, c2, c3, k0, k1, *expected = (int(f, 16) for f in fields[2:])
    assert R.philox((c0, c1, c2, c3), (k0, k1)) == tuple(expected)


def _inverse_round(out: R.Words, key: tuple[int, int]) -> R.Words:
    """Undo one round: the multipliers are odd, so lo = M c mod 2^32 gives c back through M's inverse."""
    o0, lo1, o2, lo0 = out
    c0, c2 = lo0 * pow(R.M0, -1, 1 << 32) & R.MASK, lo1 * pow(R.M1, -1, 1 << 32) & R.MASK
    return c0, o0 ^ (R.M1 * c2 >> 32) ^ key[0], c2, o2 ^ (R.M0 * c0 >> 32) ^ key[1]


@given(st.tuples(U32, U32, U32, U32), st.tuples(U32, U32))
def test_ten_inverted_rounds_with_the_bumped_keys_recover_the_counter(counter: R.Words, key: tuple[int, int]) -> None:
    keys = [((key[0] + r * R.W0) & R.MASK, (key[1] + r * R.W1) & R.MASK) for r in range(R.ROUNDS)]
    out = R.philox(counter, key)
    for k in reversed(keys):
        out = _inverse_round(out, k)
    assert out == counter


# FNV-1a 32 from Landon Curt Noll's reference code, github.com/lcn2/fnv at commit 6f5d7fa (14 January 2026), fetched
# 8 October 2026 [sourced]: test_fnv.c lines 121 to 144 (TEST(x) hashes x, TEST0(x) hashes x and its NUL) and
# lines 736 to 759 (fnv1a_32_vector); the offset basis is fnv.h line 136 and the prime hash_32a.c line 83.
FNV_STRINGS = ("", "a", "b", "c", "d", "e", "f", "fo", "foo", "foob", "fooba", "foobar")
FNV_1A_32 = (
    0x811C9DC5, 0xE40C292C, 0xE70C2DE5, 0xE60C2C52, 0xE10C2473, 0xE00C22E0,
    0xE30C2799, 0x6222E842, 0xA9F37ED7, 0x3F5076EF, 0x39AAA18A, 0xBF9CF968,
    0x050C5D1F, 0x2B24D044, 0x9D2C3F7F, 0x7729C516, 0xB91D6109, 0x931AE6A0,
    0x052255DB, 0xBEF39FE6, 0x6150AC75, 0x9AAB3A3D, 0x519C4C3E, 0x0C1C9EB8,
)


def test_hash32_meets_fnvs_published_vectors() -> None:
    assert (R.FNV_OFFSET, R.FNV_PRIME) == (0x811C9DC5, 0x01000193)
    strings = FNV_STRINGS + tuple(s + "\x00" for s in FNV_STRINGS)
    assert tuple(R.hash32(s) for s in strings) == FNV_1A_32


def test_hash32_joins_parts_with_unit_separator() -> None:
    assert R.hash32() == R.hash32("") == R.FNV_OFFSET
    assert R.hash32("a", "b") == R.fnv1a32(b"a\x1fb") == R.hash32("a\x1fb")
    assert R.hash32("", "") == R.fnv1a32(b"\x1f") and R.hash32("", "") != R.hash32("")
    assert R.hash32("café", 3) == R.fnv1a32("café\x1f3".encode())


@pytest.mark.parametrize(
    ("n", "text"),
    [  # String(n) in Node 22.22.0 [measured, 8 October 2026]
        (0, "0"),
        (-0.0, "0"),
        (7.0, "7"),
        (-1, "-1"),
        (2**53, "9007199254740992"),
        (2**53 + 2, "9007199254740994"),
        (2**64, "18446744073709552000"),
        (123456789012345680, "123456789012345680"),
        (999999999999999900000.0, "999999999999999900000"),
        (1e21, "1e+21"),
        (-1e21, "-1e+21"),
        (2.0**70, "1.1805916207174113e+21"),
        (1e300, "1e+300"),
        (1.5e300, "1.5e+300"),
        (2.0**1023, "8.98846567431158e+307"),
    ],
)
def test_number_parts_are_written_as_javascripts_string(n: int | float, text: str) -> None:
    assert R.js_string(n) == text
    assert R.hash32(n) == R.hash32(text)


@pytest.mark.parametrize("part", [0.5, -1e-300, math.inf, -math.inf, math.nan, 2**64 + 1, 10**400, "\ud800"])
def test_hash32_rejects_parts_with_no_integral_double_or_no_utf8(part: object) -> None:
    with pytest.raises(ValueError):
        R.hash32("x", part)  # type: ignore[arg-type]


@pytest.mark.parametrize("part", [True, None, b"a", [1]])
def test_hash32_rejects_parts_of_other_types(part: object) -> None:
    with pytest.raises(TypeError):
        R.hash32(part)  # type: ignore[arg-type]


@given(st.integers(-(R.TWO53 - 1), R.TWO53 - 1), st.lists(NAME, max_size=3))
def test_an_integer_part_hashes_as_its_decimal(n: int, rest: list[str]) -> None:
    h = R.hash32(n, *rest)
    assert 0 <= h <= R.MASK and h == R.hash32(str(n), *rest) == R.hash32(float(n), *rest)


@given(st.floats(allow_nan=False, allow_infinity=False).filter(float.is_integer))
def test_the_written_number_reads_back_as_the_same_double(x: float) -> None:
    text = R.js_string(x)
    assert float(text) == x and ("e" in text) == (abs(x) >= 1e21)


@pytest.mark.parametrize("seed", [-1, R.TWO32, 0.5, math.nan, math.inf])
def test_a_seed_outside_the_32_bit_integers_is_a_range_error(seed: object) -> None:
    with pytest.raises(ValueError):
        R.SeedSource(seed)


@pytest.mark.parametrize("bad", [True, "1", None, [0]])
def test_seeds_indices_and_bounds_of_other_types_are_type_errors(bad: object) -> None:
    with pytest.raises(TypeError):
        R.SeedSource(bad)
    with pytest.raises(TypeError):
        R.SeedSource(1).rng("s").at(bad)
    with pytest.raises(TypeError):
        R.SeedSource(1).rng("s").int(0, bad)


@pytest.mark.parametrize("bad", [1, None, b"s"])
def test_stream_names_of_other_types_are_type_errors(bad: object) -> None:
    with pytest.raises(TypeError):
        R.SeedSource(1).rng(bad)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        R.SeedSource(1).rng("s").fork(bad)  # type: ignore[arg-type]


@given(U32, NAME, NAME)
def test_keys_come_from_the_seed_and_the_stream_names(seed: int, name: str, child: str) -> None:
    source = R.SeedSource(float(seed))
    parent = source.rng(name)
    parent.next()
    forked = parent.fork(child)
    assert source.seed == seed and parent.key == (seed, R.hash32(name))
    assert forked.key == (seed, R.hash32(parent.key[1], child)) and forked.position == 0 and parent.position == 1


@given(U32, NAME, st.integers(0, R.TWO53 // 2 - 1))
def test_draws_2b_and_2b_plus_1_share_block_b(seed: int, name: str, b: int) -> None:
    rng = R.SeedSource(seed).rng(name)
    block = R.philox((b % R.TWO32, b // R.TWO32, 0, 0), rng.key)
    assert rng.words(2 * b) + rng.words(2 * b + 1) == block


@given(U32, NAME, INDEX)
def test_at_is_53_bits_of_the_two_words(seed: int, name: str, j: int) -> None:
    rng = R.SeedSource(seed).rng(name)
    u, v = rng.words(j)
    x = rng.at(j)
    m = x * R.TWO53
    assert 0 <= x < 1 and m.is_integer() and int(m) == (u >> 5) << 26 | v >> 6
    assert rng.at(float(j)) == x and rng.position == 0


class Scripted(R.Rng):
    """An Rng whose draw j has the words (script[j], v): pins the arithmetic at chosen words."""

    def __init__(self, script: list[int], v: int = 0) -> None:
        super().__init__(0, 0)
        self.script, self.v = script, v

    def words(self, j: object) -> tuple[int, int]:
        return self.script[j], self.v  # type: ignore[index]


def test_at_reaches_one_minus_2_to_the_minus_53_and_zero() -> None:
    assert Scripted([R.MASK], R.MASK).at(0) == 1 - 2.0**-53
    assert Scripted([31], 63).at(0) == 0.0


@pytest.mark.parametrize("j", [-1, R.TWO53, 0.5, math.nan, math.inf, -math.inf])
def test_an_index_outside_0_to_2_to_the_53_is_a_range_error(j: object) -> None:
    with pytest.raises(ValueError):
        R.SeedSource(3).rng("s").at(j)


def test_next_reads_the_position_and_at_never_moves_it() -> None:
    rng = R.SeedSource(7).rng("pos")
    expected = [rng.at(j) for j in range(6)]
    assert rng.position == 0
    assert [rng.next() for _ in range(3)] == expected[:3] and rng.position == 3
    rng.at(100)
    assert rng.next() == expected[3]
    rng.normal()
    assert rng.position == 6


def test_normal_is_box_muller_on_the_next_two_draws_in_the_specs_order() -> None:
    rng = R.SeedSource(11).rng("n")
    u1, u2 = rng.at(0), rng.at(1)
    r = math.sqrt(-2 * R.ln(1 - u1))
    assert rng.normal() == r * R.cos(R.TAU * u2) and R.box_muller(u1, u2) == (r * R.cos(R.TAU * u2), r)
    assert rng.position == 2


INT_SIZES = [1, 2, 3, 6, 7, 10, 1000, (1 << 31) + 1, R.TWO32 - 1, R.TWO32]


@pytest.mark.parametrize("n", INT_SIZES)
def test_int_rejects_exactly_the_words_at_or_above_l(n: int) -> None:
    """L counted as whole buckets, n (2^32 div n), the same number as the spec's 2^32 - (2^32 mod n)."""
    limit = n * (R.TWO32 // n)
    script = [limit, R.MASK, limit - 1] if limit < R.TWO32 else [R.MASK]
    rng = Scripted(script, v=R.MASK)
    assert rng.int(-5, n - 6) == (limit - 1) % n - 5 and rng.position == len(script)


@pytest.mark.parametrize("n", INT_SIZES[1:])
def test_int_over_a_block_returns_the_accepted_words_mod_n(n: int) -> None:
    """Over a block of draws, the words u with u div n < 2^32 div n, taken mod n, are int(0, n - 1)'s values in
    order. The calls stop at draw 4000; the words run to 4200 so the last call's accepted word is among them."""
    rng = R.SeedSource(2026).rng(f"int/{n}")
    accepted = [u % n for u, _ in map(rng.words, range(4200)) if u // n < R.TWO32 // n]
    got = []
    while rng.position < 4000:
        got.append(rng.int(0, n - 1))
    assert got == accepted[: len(got)]


@pytest.mark.parametrize(
    ("lo", "hi"), [(1, 0), (0, R.TWO32), (R.TWO53, R.TWO53), (-R.TWO53, 0), (0.5, 2), (0, math.inf)]
)
def test_int_range_errors(lo: object, hi: object) -> None:
    rng = R.SeedSource(1).rng("e")
    with pytest.raises(ValueError):
        rng.int(lo, hi)
    assert rng.position == 0


@given(U32, st.integers(-(R.TWO53 - 1), R.TWO53 - 1), st.integers(1, R.TWO32))
def test_int_stays_in_range_and_consumes_a_draw(seed: int, lo: int, n: int) -> None:
    hi = min(lo + n - 1, R.SAFE)
    rng = R.SeedSource(seed).rng("prop")
    assert lo <= rng.int(lo, hi) <= hi and rng.position >= 1


def test_ln_and_cos_are_correctly_rounded() -> None:
    assert R.ln(1.0) == 0.0 and R.cos(0.0) == 1.0
    assert R.ln(0.5) == -0.6931471805599453 and R.cos(R.TAU / 4) == 6.123233995736766e-17
    for x in (2.0**-53, 1e-300, 0.1, 0.75, 1 - 2.0**-53):
        assert abs(R.ln(x) - math.log(x)) <= math.ulp(math.log(x))
    for x in (0.1, 1.0, 3.0, R.TAU - 2.0**-50, 6.0):
        assert abs(R.cos(x) - math.cos(x)) <= math.ulp(math.cos(x))


def test_box_muller_at_u1_zero_follows_ieee_signed_zeros() -> None:
    value, r = R.box_muller(0.0, 0.25)
    assert r == 0 and math.copysign(1, r) == -1  # -2 x ln(1) is -0, and sqrt(-0) is -0
    assert value == 0


def test_a_fixed_stream_of_draws_has_plausible_moments() -> None:
    rng = R.SeedSource(20261008).rng("moments")
    xs = [rng.next() for _ in range(20000)]
    zs = [rng.normal() for _ in range(2000)]
    mean = sum(zs) / len(zs)
    assert abs(sum(xs) / len(xs) - 0.5) < 0.01 and abs(mean) < 0.1
    assert abs(sum((z - mean) ** 2 for z in zs) / (len(zs) - 1) - 1) < 0.1
