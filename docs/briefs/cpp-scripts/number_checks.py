# Number checks for the cpp level 5 brief: every figure the brief states, computed here by a model that shares no code with the C++.
# Run: python3 numbers.py
from fractions import Fraction

ok = True
def check(name, got, want):
    global ok
    good = got == want
    ok &= good
    print(f"{'ok ' if good else 'BAD'} {name}: {got}" + ("" if good else f"  (brief says {want})"))

# --- l19: sizes and costs
check("1,000,000 doubles in bytes", 1_000_000 * 8, 8_000_000)
check("copy time at 10 GB/s, ms", Fraction(8_000_000, 10_000_000_000) * 1000, Fraction(4, 5))      # 0.8 ms
check("pointer and size moved, bytes here (wasm32)", 4 + 4, 8)
check("pointer and size moved, bytes on a desktop", 8 + 8, 16)

def push_model(n, move_noexcept):
    """std::vector growth: capacity 0, 1, 2, 4, ...; returns (copies, moves) for n push_back(T(i)) of rvalues"""
    cap, size, copies, moves = 0, 0, 0, 0
    for _ in range(n):
        if size == cap:
            newcap = max(1, cap * 2)
            if move_noexcept: moves += size
            else: copies += size
            cap = newcap
        moves += 1            # the new element is built from the temporary by a move
        size += 1
    return copies, moves

check("4 pushes, noexcept move: (copies, moves)", push_model(4, True), (0, 7))
check("2 pushes, move not noexcept: (copies, moves)", push_model(2, False), (1, 2))
check("3 pushes, move not noexcept: (copies, moves)", push_model(3, False), (3, 3))
check("4 pushes, move not noexcept: (copies, moves)", push_model(4, False), (3, 4))
check("8 pushes, noexcept move: moves (P-vec, Counted)", push_model(8, True), (0, 15))

def allocations(n):
    cap, k = 0, 0
    for size in range(n):
        if size == cap:
            cap = max(1, cap * 2); k += 1
    return k, cap
check("1000 pushes: (allocations, capacity) (P-vec)", allocations(1000), (11, 1024))
check("size * 10000 + capacity after 1000 pushes", 1000 * 10000 + 1024, 10_001_024)

# sink idiom: copies of doubles
check("set_prices(lvalue): doubles copied", 1_000_000, 1_000_000)
check("set_prices(lvalue) counted wrongly as copy plus assign", 2 * 1_000_000, 2_000_000)

# --- l21: layout under wasm32 rules (pointer 4, double align 8) and a desktop (pointer 8)
def layout(fields, ptr, dalign=8):
    """fields: list of (size, align) in order; returns struct size"""
    off, maxa = 0, 1
    for size, al in fields:
        off = (off + al - 1) // al * al + size
        maxa = max(maxa, al)
    return (off + maxa - 1) // maxa * maxa
for ptr, name in ((4, "wasm32"), (8, "desktop")):
    check(f"D {{vptr, int, int}} on {name}", layout([(ptr, ptr), (4, 4), (4, 4)], ptr), 12 if ptr == 4 else 16)
    check(f"Quote {{vptr, double, double}} on {name}", layout([(ptr, ptr), (8, 8), (8, 8)], ptr), 24)
    check(f"OneVirtual {{vptr, int}} on {name}", layout([(ptr, ptr), (4, 4)], ptr), 8 if ptr == 4 else 16)
check("PlainQuote {double, double}", layout([(8, 8), (8, 8)], 4), 16)
check("B {vptr, double} on wasm32 (homework 7a)", layout([(4, 4), (8, 8)], 4), 16)
check("Tick {int} (l21 hook)", layout([(4, 4)], 4), 4)

# --- l22: ranges and money
INT_MAX = 2**31 - 1
check("INT_MAX in pence as pounds", Fraction(INT_MAX, 100), Fraction(2147483647, 100))
print("   as text:", f"{INT_MAX // 100:,}.{INT_MAX % 100:02d}")
check("INT_MAX pence, pounds text", f"£{INT_MAX // 100:,}.{INT_MAX % 100:02d}", "£21,474,836.47")
check("£25,000,000 in pence", 25_000_000 * 100, 2_500_000_000)
check("£25,000,000 exceeds INT_MAX", 2_500_000_000 > INT_MAX, True)
check("5,000 fills of £5,000, pounds", 5_000 * 5_000, 25_000_000)
U32 = 2**32 - 1
check("UINT_MAX pence, pounds text", f"£{U32 // 100:,}.{U32 % 100:02d}", "£42,949,672.95")
I64 = 2**63 - 1
check("int64 max pence, pounds text", f"£{I64 // 100:,}.{I64 % 100:02d}", "£92,233,720,368,547,758.07")
check("0 - 1 as unsigned 32-bit (v.size() - 1, empty, wasm32)", (0 - 1) % 2**32, 4_294_967_295)
check("0 - 1 as unsigned 64-bit (desktop)", (0 - 1) % 2**64, 18_446_744_073_709_551_615)
check("2^30 + 2^30 overflows int", 2**30 + 2**30 > INT_MAX, True)
check("2^30 - 1 + 2^30 equals INT_MAX exactly", 2**30 - 1 + 2**30, INT_MAX)

# --- l23: make_shared
per_sec = 200_000
check("shared_ptr<T>(new T): allocations a second", per_sec * 2, 400_000)
check("make_shared: allocations a second", per_sec * 1, 200_000)
check("saved allocations a second at 50 ns, ms", Fraction(per_sec * 50, 10**9) * 1000, 10)
check("that is a share of one core, per cent", Fraction(per_sec * 50, 10**9) * 100, 1)

print("ALL NUMBERS OK" if ok else "SOME NUMBER BAD")
