# allocCheck re-check (4 Nov)

`alloc_check.hpp` is a native stand-in for the planned `allocCheck: true` harness flag (inbox label C-alloc-check). The `.cpp` files are P-pool, P-format-price, P-latency-hist and P-handler as now written in `docs/briefs/systems.md`, checked with g++ 13.3 and clang++ 18.1 at `-std=c++20 -O1 -fno-exceptions`: every reference passes, every starter fails.

The brief is the source of truth for these four problems. `../cpp/problems_l4.py`, `problems_l4b.py` and `appendix_cpp.md` still use the old `prelude` with `g_allocs`; do not regenerate the brief's appendix from them.
