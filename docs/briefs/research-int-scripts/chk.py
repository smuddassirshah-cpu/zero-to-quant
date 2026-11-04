"""Shared helper: every brief number is computed by method A (hand formula, pure Python)
and method B (a library or a simulation); two() asserts they agree and prints the value."""
import math
FAILS = []
def two(label, a, b, tol=1e-9, rel=False):
    ok = abs(a - b) <= (tol * max(1, abs(a)) if rel else tol)
    print(f"{'OK  ' if ok else 'FAIL'} {label}: A={a!r:<24} B={b!r}")
    if not ok:
        FAILS.append(label)
def done():
    print("ALL AGREE" if not FAILS else f"FAILURES: {FAILS}")
    raise SystemExit(1 if FAILS else 0)
def Phi(z): return 0.5 * math.erfc(-z / math.sqrt(2))
