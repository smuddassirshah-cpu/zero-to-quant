#!/usr/bin/env python3
"""Concept checks for systems level 4 (l15 to l18, review-4, homework-4), audit round 2.

Run from the repo root: python3 -I docs/reports/systems-L4-concepts-r2.py
Exit 0 when the content is correct. Each assert names its ledger row
(docs/reports/audit-systems-4-r2-ledger.md). A check that fails because the
content is wrong is marked EXPECTED_FAIL with the corrected assert in a comment.

Needs g++ (the C++ items are compiled with -std=c++17 and -std=c++20 and run with
an overloaded operator new that counts allocations) and a ThreadSanitizer-capable
g++ for the SPSC ring checks (skipped with a note when -fsanitize=thread is not
available). No wall-clock asserts anywhere: the timing claims are checked as the
arithmetic of the model each screen states.
"""
import csv
import json
import math
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTENT = ROOT / "app" / "content" / "courses" / "systems"
DATA = ROOT / "app" / "content" / "data" / "systems"
WORK = pathlib.Path(tempfile.mkdtemp(prefix="sysL4r2-"))
NOTES = []


def load(name):
    return json.loads((CONTENT / f"{name}.json").read_text())


L15, L16, L17, L18 = load("l15-no-allocation"), load("l16-ring-buffer"), load("l17-measuring-latency"), load("l18-feed-handler")
R4, H4 = load("review-4"), load("homework-4")


def screen(lesson, title):
    for i, s in enumerate(lesson["screens"]):
        if s.get("title") == title:
            return i, s
    raise KeyError(title)


def item(doc, iid):
    for it in doc["items"]:
        if it["id"] == iid:
            return it
    raise KeyError(iid)


def quiz(lesson, qid):
    for q in lesson["quiz"]:
        if q["id"] == qid:
            return q
    raise KeyError(qid)


# ---------------------------------------------------------------- C++ harness

HARNESS = r"""
#include <cstdlib>
#include <cstddef>
#include <new>
static volatile long g_allocs = 0;
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void* operator new[](std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void* operator new(std::size_t n, const std::nothrow_t&) noexcept { ++g_allocs; return std::malloc(n ? n : 1); }
void* operator new[](std::size_t n, const std::nothrow_t&) noexcept { ++g_allocs; return std::malloc(n ? n : 1); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
int alloc_count() { return static_cast<int>(g_allocs); }
void reset_alloc_count() { g_allocs = 0; }
"""

TEST_HEAD = r"""
#include <string>
#include <vector>
#include <cstdio>
#include <cmath>
static int g_fail = 0;
static void report(const char* name, bool ok) { std::printf("%s %s\n", ok ? "PASS" : "FAIL", name); if (!ok) ++g_fail; }
template <class A, class B> static bool same(const A& a, const B& b) { return a == b; }
static bool same(const std::string& a, const std::string& b) { return a == b; }
static bool close(double a, double b) { return std::fabs(a - b) <= std::fmax(1e-9 * std::fmax(std::fabs(a), std::fabs(b)), 1e-12); }
"""


def cxx_lit(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return f"{v}LL" if abs(v) > 2147483647 else str(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, str):
        return "std::string(" + json.dumps(v) + ")"
    if isinstance(v, list):
        return "std::vector<int>{" + ", ".join(cxx_lit(x) for x in v) + "}"
    raise TypeError(v)


def cxx_main(tests):
    body = []
    for k, t in enumerate(tests, 1):
        setup = t.get("setup", "")
        cmp = "close(__r, %s)" % cxx_lit(t["expect"]) if t.get("compare") == "isclose" else "same(__r, %s)" % cxx_lit(t["expect"])
        body.append("  { %s auto __r = (%s); report(\"t%d\", %s); }" % (setup, t["call"], k, cmp))
    return "int main() {\n" + "\n".join(body) + "\n  std::printf(\"FAILS %d\\n\", g_fail); return g_fail ? 1 : 0;\n}\n"


def run_cpp(name, code, tests, std="c++17", extra=""):
    """Compile harness + code + tests with g++ and return the list of failing test names."""
    src = WORK / f"{name}-{std}.cpp"
    src.write_text(HARNESS + TEST_HEAD + "\n" + extra + "\n" + code + "\n" + cxx_main(tests))
    exe = WORK / f"{name}-{std}"
    cp = subprocess.run(["g++", f"-std={std}", "-O1", "-fno-builtin", "-w", str(src), "-o", str(exe)], capture_output=True, text=True)
    if cp.returncode != 0:
        return ["COMPILE: " + cp.stderr.strip().splitlines()[0]]
    out = subprocess.run([str(exe)], capture_output=True, text=True, timeout=60)
    return [ln.split()[1] for ln in out.stdout.splitlines() if ln.startswith("FAIL ")]


def code_widget(container):
    w = container["widget"]
    return w["starter"], w["solution"], w.get("prelude", "") + "\n", w.get("postlude", ""), w["tests"]


def check_code_item(label, container, alloc_test_index=None):
    starter, solution, prelude, postlude, tests = code_widget(container)
    for std in ("c++17", "c++20"):
        fails = run_cpp(label + "-sol", prelude + solution + postlude, tests, std)
        assert fails == [], f"{label}: model solution fails {fails} under {std}"
    fails = run_cpp(label + "-start", prelude + starter + postlude, tests, "c++17")
    assert fails, f"{label}: the starter passes every hidden test"
    if alloc_test_index is not None:
        assert f"t{alloc_test_index}" in fails, f"{label}: the starter passes the alloc_count() test, so it does not allocate as the lesson says"
    return fails


# ------------------------------------------------------------ l15: allocation

def l15_checks():
    # l15/screens[0]: which lines of on_message allocate (ledger rows l15-s0-*).
    code = r"""
#include <vector>
#include <string>
#include <map>
#include <array>
struct Msg { int price; int qty; };
struct Event { Msg m; explicit Event(const Msg& x) : m(x) {} };
int line_vector_decl() { reset_alloc_count(); std::vector<int> levels; return alloc_count(); }
int line_vector_push() { std::vector<int> levels; reset_alloc_count(); levels.push_back(7); return alloc_count(); }
int line_new_event() { Msg m{1, 2}; reset_alloc_count(); auto* ev = new Event(m); int n = alloc_count(); delete ev; return n; }
int line_string100() { reset_alloc_count(); std::string s(100, 'x'); return alloc_count(); }
int line_string64() { reset_alloc_count(); std::string s(64, 'y'); return alloc_count(); }
int line_string15() { reset_alloc_count(); std::string s(15, 'x'); return alloc_count(); }
int line_map_decl() { reset_alloc_count(); std::map<int, int> book; return alloc_count(); }
int line_map_index() { std::map<int, int> book; reset_alloc_count(); book[10000] = 1; return alloc_count(); }
int line_arith() { Msg m{1, 2}; reset_alloc_count(); volatile int x = m.qty * 2; (void)x; return alloc_count(); }
int whole_on_message() { Msg m{10000, 5}; reset_alloc_count();
    std::vector<int> levels; levels.push_back(m.price); auto* ev = new Event(m); std::string s(100, 'x');
    std::map<int, int> book; book[m.price] = 1; int n = alloc_count(); delete ev; return n; }
int std_array_decl() { reset_alloc_count(); std::array<int, 8> a{}; volatile int k = a[3]; (void)k; return alloc_count(); }
int plain_array_decl() { reset_alloc_count(); int b[8] = {0}; volatile int k = b[3]; (void)k; return alloc_count(); }
int emplace_double() { std::vector<double> v; reset_alloc_count(); v.emplace_back(2.5); return alloc_count(); }
int new_double3() { reset_alloc_count(); auto* q = new double[3]; int n = alloc_count(); delete[] q; return n; }
int reserve_then_messages() { std::vector<int> v; v.reserve(1000); reset_alloc_count();
    for (int msg = 0; msg < 50; ++msg) { for (int i = 0; i < 500; ++i) v.push_back(i); v.clear(); } return alloc_count(); }
int unordered_map_insert_allocates() { std::map<int, int> m; (void)m; return 0; }
"""
    tests = [
        {"call": "line_vector_decl()", "expect": 0},       # t1  l15-s0-l2
        {"call": "line_vector_push()", "expect": 1},       # t2  l15-s0-l3
        {"call": "line_new_event()", "expect": 1},         # t3  l15-s0-l4
        {"call": "line_string100()", "expect": 1},         # t4  l15-s0-l5
        {"call": "line_map_index()", "expect": 1},         # t5  l15-s0-l6
        {"call": "line_arith()", "expect": 0},             # t6  l15-s0-l7
        {"call": "whole_on_message()", "expect": 4},       # t7  l15-s0-explain (four a message)
        {"call": "std_array_decl()", "expect": 0},         # t8  l15-trap-array
        {"call": "plain_array_decl()", "expect": 0},       # t9  l15-trap-plain
        {"call": "emplace_double()", "expect": 1},         # t10 r4-allocating-lines emplace
        {"call": "new_double3()", "expect": 1},            # t11 r4-allocating-lines new
        {"call": "line_string64()", "expect": 1},          # t12 r4-allocating-lines string(64)
        {"call": "reserve_then_messages()", "expect": 0},  # t13 q15-reserve
        {"call": "line_map_decl()", "expect": 0},          # t14 l15-s0-l6 (the declaration itself)
        {"call": "line_string15()", "expect": 0},          # t15 SSO exists: a 15-char string stays inside the object (libstdc++)
    ]
    for std in ("c++17", "c++20"):
        fails = run_cpp("l15-alloc", code, tests, std)
        assert fails == [], f"l15 allocation table (ledger rows l15-s0-*, l15-trap-*, q15-reserve, r4-allocating-lines): g++ {std} disagrees on {fails}"

    # Screen arithmetic (model stated on screen).
    assert 50 * 200_000 / 1e6 == 10, "l15-s1: 50 ns x 200,000 a second is 10 ms a second"
    assert 1 / 200_000 * 1e6 == 5, "l15-s1: 200,000 a second is one every 5 us"
    assert (4 * 50, 4 * 50 * 200_000 / 1e6, 4 * 50 * 200_000 / 1e6 / 1000 * 100) == (200, 40, 4), "l15-s2: 200 ns, 40 ms, 4%"
    assert (3 * 200_000 * 50 / 1e6, 3 * 200_000 * 2 / 1e6) == (30, 1.2) and 30 / 1.2 == 25, "l15-s4: 30 ms, 1.2 ms, 25 times"
    assert 5 * 50 * 150_000 / 1e6 == 37.5, "q15-cost: 37.5 ms"
    assert 3 * 50 * 120_000 / 1e6 == 18, "r4-alloc-bill: 18 ms"
    assert (1000 * 1.5, 1500 * 24, 1500 * 32, (1 - 24 / 32) * 100) == (1500, 36000, 48000, 25), "l15-transfer: 1,500 slots, 36,000 and 48,000 bytes, 25%"
    assert 36000 > 32768 and 48000 > 32768 and round(36000 / 1024) == 35 and round(48000 / 1024) == 47, "l15-transfer explain: neither fits 32 KiB L1; 35 KiB and 47 KiB"
    assert 800 * 1.5 * 20 == 24000, "q15-size: 24,000 bytes"

    # Pool free list: a LIFO stack of slot numbers (ledger rows l15-s3, l15-s7, l15-drill, q15-pool, r4-pool-order).
    def pool(n, ops):
        free = list(range(n))  # head is free[0]
        out = []
        for op in ops:
            if op == "a":
                out.append(free.pop(0) if free else -1)
            else:
                free.insert(0, op)
        return out, free

    assert pool(4, ["a", "a", 0])[1] == [0, 2, 3], "l15-s3: after two allocations and release 0 the free list reads 0, 2, 3 (cells 2, used, 3, end)"
    assert pool(4, ["a", "a", 0, "a"])[0][-1] == 0, "l15-s3: the next allocate returns slot 0"
    assert pool(3, ["a", "a", "a", "a"])[0][-1] == -1, "l15-s7 and l15-drill row 3: a full pool returns -1"
    assert pool(3, ["a", "a", "a", 1, "a"])[0][-1] == 1, "l15-drill row 1"
    assert pool(3, ["a", "a", "a", 0, 2, "a"])[0][-1] == 2, "l15-drill row 2"
    assert pool(4, ["a"] * 4 + [3, 1, 2, "a", "a"])[0][-2:] == [2, 1], "l15-drill row 4: heads come out 2, 1"
    assert pool(5, ["a"] * 5 + [3, 0, "a"])[0][-1] == 0, "q15-pool: slot 0"
    assert pool(4, ["a"] * 4 + [2, 3, 1, "a"])[0][-1] == 1 and pool(4, ["a"] * 4 + [2, 3, 1])[1] == [1, 3, 2], "r4-pool-order: list 1, 3, 2, next allocate 1"
    # The Pool code item's hidden tests follow the same model.
    w = L15["screens"][9]["widget"]
    assert L15["screens"][9]["title"] == "Write the pool"
    expect = {1: 0, 2: 2, 3: -1, 4: 1, 5: 1, 6: 0, 9: -1}
    sims = {1: pool(3, ["a"]), 2: pool(3, ["a"] * 3), 3: pool(3, ["a"] * 4), 4: pool(3, ["a", "a", "a", 1, "a"]),
            5: pool(3, ["a", "a", 0, 1, "a"]), 6: pool(3, ["a", "a", 0, 1, "a", "a"]), 9: pool(0, ["a"])}
    for k, v in expect.items():
        assert w["tests"][k - 1]["expect"] == v == sims[k][0][-1], f"l15 Write the pool test {k}: expected {v} by the free-list model"

    # Code items: format_price (screen 5) and Pool (screen 9): solution passes, starter fails the count test.
    s5 = L15["screens"][5]
    assert s5["title"] == "Count the heap"
    fails = check_code_item("l15-format-price", s5, alloc_test_index=10)
    s9 = L15["screens"][9]
    fails = check_code_item("l15-pool", s9, alloc_test_index=None)
    assert "t3" in fails and "t4" in fails, "l15 Pool starter must fail the full-pool and reuse tests"
    # The starter's allocate never reuses a slot and never reports full: it passes the alloc test (it allocates nothing) but
    # fails the contract. The lesson's `how` says the count test is the last of ten; the starter's failure is on reuse, not on the heap.
    assert "t10" not in fails, "l15 Pool: the starter does not allocate, so the count test alone would pass it (ledger l15-s9-how)"


# ---------------------------------------------------------- l16: ring buffer

def l16_checks():
    M32 = 1 << 32
    # Counter arithmetic (ledger rows l16-s1-*, l16-s2-*, l16-generalise, l16-drill, q16-*, r4-ring-counters).
    assert (5 % 4, 20 - 13, 20 % 8, 20 & 7, 13 & 7) == (1, 7, 4, 4, 5), "l16-s1: slot 1, 7 items, slot 4, head slot 5"
    assert 4294967293 & 3 == 1 and 4294967295 % 3 == 0 and 0 % 3 == 0 and M32 % 3 == 1, "l16-s2 rows 1 to 3 and the 2^32 mod 3 = 1 hint"
    assert abs(M32 / 1e7 - 429.5) < 0.05, "l16-s2 row 4: 429.5 s to wrap at 10 million a second"
    table = [(4294967294, 4294967292), (4294967295, 4294967293), (0, 4294967294), (1, 4294967295)]
    assert [((t - h) % M32, t & 3) for t, h in table] == [(2, 2), (2, 3), (2, 0), (2, 1)], "l16-s2 console: size stays 2 and slots run 2, 3, 0, 1 across the wrap"
    assert [t % 3 for t in (4294967294, 4294967295, 0, 1)] == [2, 0, 0, 1], "l16-s2 explain: a ring of 3 puts 4,294,967,295 and 0 in one slot"
    for n in (3, 4, 5, 6, 7, 8):
        ok = all(((t + k) % M32 - t) % M32 == k for t in (M32 - 3, M32 - 1) for k in range(8))
        assert ok, f"l16-generalise: unsigned tail - head is exact modulo 2^32 for any N (N={n})"
    assert all(((M32 - 1 + k) % M32) % n == ((M32 - 1 + k) % n) for n in (4, 8) for k in range(1, 9)) and not all(((M32 - 1 + k) % M32) % 3 == ((M32 - 1 + k) % 3) for k in range(1, 9)), \
        "l16-generalise: counter mod N keeps order across the wrap only when N divides 2^32 (4 and 8 do, 3 does not)"
    assert (11 - 7, 7 & 3, 11 & 3) == (4, 3, 3), "l16-full-ring: counters differ by 4, both slots 3"
    assert (45 & 15, 103 - 100) == (13, 3), "l16-drill rows 3 and 4"
    assert (50 - 37, 50 & 15) == (13, 2), "q16-slot"
    assert (85 - 70, 85 & 31, 85 % 32) == (15, 21, 21), "r4-ring-counters"
    assert all((c & 5) != c % 6 for c in (2, 3, 6, 7)), "q16-pow2 explain: for N = 6 the mask 101 keeps the wrong bits"
    # Sizing (model on screen).
    assert (200_000 * 0.001, 256 * 24, 1_000_000 * 0.005) == (200, 6144, 5000) and 2 ** 8 >= 200 > 2 ** 7 and 2 ** 13 >= 5000 > 2 ** 12, "l16-transfer: 200, 256, 6,144, 8,192"
    assert 8192 * 24 == 196608 == 192 * 1024, "l16-transfer explain: 192 KiB"
    assert 400_000 * 0.005 == 2000 and 2 ** 11 >= 2000 > 2 ** 10, "q16-stall: 2,048"
    assert (1e7 * 60 / 1e6, 1e7 * 1 / 1e6) == (600, 10) and 600 / 1000 == 0.6, "l16-s4: 600 ms (60% of a core) against 10 ms"

    # The explore ring of four and the review ring of two: a growing-counter ring model (ledger l16-s0, l16-drill rows 1 and 2, r4-ring-order).
    def ring(n, ops):
        buf, head, tail, out = [None] * n, 0, 0, []
        for op in ops:
            if op == "pop":
                if head == tail:
                    out.append(-1)
                else:
                    out.append(buf[head % n]); head += 1
            else:
                if tail - head == n:
                    out.append(0)
                else:
                    buf[tail % n] = op; tail += 1; out.append(1)
        return out

    assert ring(4, [1, 2, 3, 4, 5] + ["pop"] * 5) == [1, 1, 1, 1, 0, 1, 2, 3, 4, -1], "l16-s0: push 5 refused, pops 1 2 3 4 then empty"
    assert ring(1, [7, 8, "pop"]) == [1, 0, 7], "l16-drill rows 1 and 2"
    assert ring(2, [10, 20, 30, "pop", 40, "pop", "pop", "pop"]) == [1, 1, 0, 10, 1, 20, 40, -1], "r4-ring-order: third pop returns 40"

    # Code item: the Ring (screen 9).
    s9 = L16["screens"][9]
    assert s9["title"] == "Write the ring"
    for k, t in enumerate(s9["widget"]["tests"][:9], 1):
        ops = [int(x) for x in t["call"][t["call"].index("{") + 1:t["call"].index("}")].split(",") if x.strip()]
        cap = int(t["call"][t["call"].index("(") + 1:t["call"].index(",")])
        assert ring(cap, [o if o > 0 else "pop" for o in ops]) == t["expect"], f"l16 Write the ring test {k}: expected output by the counter model"
    fails = check_code_item("l16-ring", s9)
    assert "t1" in fails and "t10" in fails, "l16 Ring starter must fail the full-ring test (holds N-1) and the 64-byte separation test"

    # SPSC ring under ThreadSanitizer: the orders of the push screen and the pop item are race free; a relaxed tail store is a data race
    # (ledger rows l16-s5-*, l16-trap-*, h4-pop-order-*).
    probe = r"""
#include <atomic>
#include <thread>
#include <cstdio>
#include <cstddef>
#ifndef ORDER_TAIL
#define ORDER_TAIL std::memory_order_release
#endif
#ifndef ORDER_HEAD
#define ORDER_HEAD std::memory_order_release
#endif
#ifndef LOAD_TAIL
#define LOAD_TAIL std::memory_order_acquire
#endif
constexpr std::size_t N = 8;
int buf_[N];
std::atomic<std::size_t> head_{0}, tail_{0};
bool push(int v) { std::size_t t = tail_.load(std::memory_order_relaxed); if (t - head_.load(std::memory_order_acquire) == N) return false; buf_[t & (N - 1)] = v; tail_.store(t + 1, ORDER_TAIL); return true; }
bool pop(int& out) { std::size_t h = head_.load(std::memory_order_relaxed); if (h == tail_.load(LOAD_TAIL)) return false; out = buf_[h & (N - 1)]; head_.store(h + 1, ORDER_HEAD); return true; }
int main() { const int M = 200000; std::thread p([&] { for (int i = 0; i < M;) if (push(i)) ++i; });
  long long bad = 0; int v; for (int i = 0; i < M;) { if (pop(v)) { if (v != i) ++bad; ++i; } } p.join(); std::printf("bad=%lld\n", bad); return bad ? 1 : 0; }
"""
    src = WORK / "spsc.cpp"
    src.write_text(probe)
    exe = WORK / "spsc-ok"
    cp = subprocess.run(["g++", "-std=c++17", "-O1", "-pthread", "-fsanitize=thread", str(src), "-o", str(exe)], capture_output=True, text=True)
    if cp.returncode != 0:
        NOTES.append("ThreadSanitizer not available: SPSC race checks skipped (rows l16-s5-d1, h4-pop-order-d1, h4-pop-order-d3 rest on Williams ch. 5 only)")
        return
    out = subprocess.run([str(exe)], capture_output=True, text=True, timeout=120)
    assert out.returncode == 0 and "ThreadSanitizer" not in out.stderr + out.stdout, "l16-s5 and h4-pop-order: the release/acquire SPSC ring must deliver every item in order with no TSan report"
    for defs, row in ((["-DORDER_TAIL=std::memory_order_relaxed"], "l16-s5-d1"), (["-DORDER_HEAD=std::memory_order_relaxed"], "h4-pop-order-d1"), (["-DLOAD_TAIL=std::memory_order_relaxed"], "h4-pop-order-d3")):
        exe2 = WORK / ("spsc-" + row)
        cp = subprocess.run(["g++", "-std=c++17", "-O1", "-pthread", "-fsanitize=thread"] + defs + [str(src), "-o", str(exe2)], capture_output=True, text=True)
        assert cp.returncode == 0
        out = subprocess.run([str(exe2)], capture_output=True, text=True, timeout=120)
        assert "WARNING: ThreadSanitizer: data race" in out.stderr + out.stdout, f"{row}: TSan must report the slot access as a data race when the pairing memory order is relaxed"


# -------------------------------------------------------- l17: latency

def nearest_rank(values, p):
    """Nearest-rank percentile with exact arithmetic: rank = ceil(p n / 100), at least 1."""
    s = sorted(values)
    r = max(1, math.ceil(Fraction(str(p)) * len(s) / 100))
    return s[r - 1]


def l17_checks():
    v = [10] * 990 + [1000] * 10
    assert sum(v) / len(v) == 19.9 and 19.9 not in v, "l17-s0: mean 19.9 us, no request took it"
    assert nearest_rank([10] * 990 + [1000] * 10, 99) == 10 and nearest_rank([10] * 989 + [1000] * 11, 99) == 1000, "l17-s1: p99 flips to 1,000 at 11 slow"
    assert round(sum([10] * 989 + [1000] * 11) / 1000, 1) == 20.9, "l17-s1 explain: mean 20.89, stated to one place as 20.9, at 11 slow"
    assert [nearest_rank(v, p) for p in (50, 99, 99.9)] == [10, 10, 1000] and nearest_rank([10] * 999 + [1000], 99.9) == 10, "l17-s2: 10, 10, 1,000 and 10"
    assert (math.ceil(Fraction(50) * 1000 / 100), math.ceil(Fraction(99) * 1000 / 100), math.ceil(Fraction("99.9") * 1000 / 100)) == (500, 990, 999), "l17-s2 hint: positions 500, 990, 999"
    assert nearest_rank(range(1, 41), 95) == 38 and math.ceil(Fraction(95) * 40 / 100) == 38, "l17-generalise: p95 of 40 is rank 38"
    assert [nearest_rank([5, 1, 4, 2, 3], p) for p in (20, 50, 80, 100)] == [1, 3, 4, 5], "l17-drill"
    assert nearest_rank([3, 9, 4, 7, 5, 8, 6, 2, 10, 1], 75) == 8, "q17-rank"
    assert (95 * 20 + 5 * 400) / 100 == 39, "q17-mean"
    assert nearest_rank([10] * 970 + [1000] * 30, 99) == 1000 and (10 + 1000) / 2 == 505 and nearest_rank([10] * 1970 + [1000] * 30, 99) == 1000, "l17-transfer: 1,000, 505, 1,000"
    assert math.ceil(Fraction(99) * 2000 / 100) == 1980, "l17-transfer: position 1,980"
    assert nearest_rank([7, 3, 9, 1, 5, 8, 2, 6], 60) == 6 and math.ceil(Fraction(60) * 8 / 100) == 5, "r4-p60"
    assert (940 * 15 + 60 * 400) / 1000 == 38.1 and nearest_rank([15] * 940 + [400] * 60, 99) == 400, "r4-mean-p99"
    assert (20 + 800) / 2 == 410 and nearest_rank([20] * 1960 + [800] * 40, 99) == 800 and nearest_rank([20] * 1985 + [800] * 15, 99) == 20 and nearest_rank([20] * 985 + [800] * 15, 99) == 800, "h4-two-hosts parts 1 to 3"
    assert 40_000 / 250 == 160, "h4-stall-count"
    # Floating-point rank boundary (ledger rows l17-s6-*, l17-s8-prose).
    assert 99.9 / 100 * 1000 == 999.0000000000001 and math.ceil(99.9 / 100 * 1000) == 1000, "l17-s6: 99.9 / 100 * 1000 is 999.0000000000001 and ceil gives 1,000"
    assert 0.999 * 1000 == 999.0, "l17-s6: 0.999 * 1000 is 999 exactly"
    assert 64.4 * 250 / 100 == 161.00000000000003 and math.ceil(64.4 * 250 / 100 - 1e-9) == 161, "l17-s8: 64.4 x 250 / 100 is 161.00000000000003; the guard gives 161"
    try:
        import numpy as np
        got = float(np.percentile(np.array([10.0] * 999 + [1000.0]), 99.9, method="inverted_cdf"))
        assert got == 1000.0, f"l17-s6 explain: NumPy inverted_cdf reads position 1,000 (got {got}); the lesson names NumPy 2.0.2, this run has {np.__version__}"
        NOTES.append(f"NumPy {np.__version__}: inverted_cdf p99.9 of 999 tens and one 1,000 gives {got}, as the lesson says of 2.0.2")
    except ImportError:
        NOTES.append("numpy missing: l17-s6 NumPy claim not simulated")
    # Timing model stated on the screen (ledger rows l17-s9-*): one read's worth inside the bracket.
    assert abs(20 / (10 + 20) * 100 - 66.7) < 0.05 and 20 / 1000 == 0.02, "l17-s9: 66.7% and 0.02 ns a call"
    assert abs(2 * 20 / (10 + 2 * 20) * 100 - 80) < 0.05, "l17-s9 slip two-reads: 80% is two whole reads"

    # latencies.csv: the console figures of screen 3 and the hidden tests of screen 4, recomputed from the file (ledger rows l17-s3-console, l17-s4-tests).
    rows = list(csv.DictReader((DATA / "latencies.csv").open()))
    assert len(rows) == 2000, "l17-s4: 2,000 rows"
    sent = [int(r["done_us"]) - int(r["sent_us"]) for r in rows]
    true = [int(r["done_us"]) - int(r["intended_us"]) for r in rows]
    late = sum(1 for r in rows if int(r["sent_us"]) > int(r["intended_us"]))
    assert late == 875, f"l17-s3 console: 875 of 2,000 sent late (got {late})"
    assert [nearest_rank(sent, p) for p in (50, 99, 99.9)] == [40, 50, 248], "l17-s3 console: done - sent p50 40, p99 50, p99.9 248"
    assert [nearest_rank(true, p) for p in (50, 99, 99.9)] == [49, 48821, 49911], "l17-s3 console: done - intended p50 49, p99 48,821, p99.9 49,911"
    assert abs(sum(true) / len(true) - 10584.622) < 0.001, "l17-s4 test 7: mean of the true latency 10584.622"
    assert max(true) >= 50000 - 100 and sum(1 for r in rows if int(r["done_us"]) - int(r["sent_us"]) > 1000) == 1, "l17-s3: one reply of about 50 ms; the rest under 1 ms by the client's clock"
    assert all(int(r["intended_us"]) == 100 * i for i, r in enumerate(rows)), "l17-s3 prose: requests due every 100 us"

    # The Python code item (screen 4): the model solution passes its own tests, the starter fails them.
    w = L17["screens"][4]["widget"]
    assert L17["screens"][4]["title"] == "Measure it both ways"

    def run_py(code):
        d = WORK / "py17"
        d.mkdir(exist_ok=True)
        shutil.copy(DATA / "latencies.csv", d / "latencies.csv")
        cwd = os.getcwd()
        os.chdir(d)
        fails = []
        try:
            for k, t in enumerate(w["tests"], 1):
                ns = {}
                exec(code, ns)
                if t.get("setup"):
                    exec(t["setup"], ns)
                got = eval(t["call"], ns)
                if t.get("compare") == "isclose":
                    ok = abs(float(got) - float(t["expect"])) <= t["tol"]["abs"]
                else:
                    ok = str(got) == str(t["expect"])
                if not ok:
                    fails.append(k)
        finally:
            os.chdir(cwd)
        return fails

    assert run_py(w["solution"]) == [], "l17-s4: the model solution passes its eleven hidden tests"
    assert run_py(w["starter"]), "l17-s4: the starter fails"
    # Hidden tests on the synthetic files, by the exact rank rule.
    for n, p, exp in ((77, 99, 86), (77, 99.9, 86), (1000, 99.9, 1008), (78, 50, 48)):
        vals = [i * 37 % n + 10 for i in range(n)]
        assert nearest_rank(vals, p) == exp, f"l17-s4 synthetic test n={n} p={p}: expected {exp}"
    # The C++ percentile (screen 8).
    s8 = L17["screens"][8]
    assert s8["title"] == "Write the percentile"
    for k, t in enumerate(s8["widget"]["tests"], 1):
        pass  # expectations are recomputed below from the setups' sample sets
    sets = {"990/10": [10.0] * 990 + [1000.0] * 10, "989/11": [10.0] * 989 + [1000.0] * 11, "999/1": [10.0] * 999 + [1000.0], "five": [5.0, 1.0, 4.0, 2.0, 3.0], "seven": [5.0, 1.0, 4.0, 2.0, 3.0, 7.0, 6.0], "250": [float(i) for i in range(1, 251)]}
    exp = [("990/10", 50, 10), ("990/10", 99, 10), ("990/10", 99.9, 1000), ("990/10", 100, 1000), ("989/11", 99, 1000), ("999/1", 99.9, 10), ("999/1", 100, 1000), ("five", 20, 1), ("five", 50, 3), ("five", 80, 4), ("five", 100, 5), ("five", 0, 1), ("seven", 30, 3), ("250", 64.4, 161)]
    for k, (name, p, e) in enumerate(exp, 1):
        assert nearest_rank(sets[name], p) == e == s8["widget"]["tests"][k - 1]["expect"], f"l17-s8 test {k}: nearest rank gives {e}"
    check_code_item("l17-percentile", s8)


# ------------------------------------------------------ l18: feed handler

def l18_checks():
    stages = [1000, 200, 300, 500, 500]
    assert sum(stages) == 2500 and 1000 / 2500 == 0.4 and 3000 - 2500 == 500 and 2500 + 4 * 50 == 2700 and 2500 + 5000 == 7500, "l18-s1 and l18-s2 budget figures"
    assert 10_000 / 3000 > 3, "l18-s1 explain: 10 us on the kernel path is over three times the 3 us target"
    assert (10100 - 9900 + 1, 201 * 2 * 4, 1024 * 16, 1608 + 16384 + 40) == (201, 1608, 16384, 18032) and 18032 < 32768, "l18-s3 book sizes, fits 32 KiB"
    assert (sum([800, 150, 250, 400, 400]), 2000 + 150, 150_000 * 24 / 1e6, 900 // 24, 900 % 24) == (2000, 2150, 3.6, 37, 12), "l18-drill"
    assert (18032 * 50, round(901600 / 1024, 1), math.ceil(901600 / 32768)) == (901600, 880.5, 28) and abs(901600 / 32768 - 27.5) < 0.02, "l18-transfer"
    assert sum([600, 100, 200, 300, 300]) == 1500 and 2000 - 1500 == 500, "q18-budget"
    assert 14 - 10 == 4 and 2048 * 16 == 32768, "q18-gap and q18-orders"
    assert (2400 * 1.25, 3000 * 20, 150_000 * 0.002, 512 * 24) == (3000, 60000, 300, 12288) and 2 ** 9 >= 300 > 2 ** 8, "h4-sizing parts 1 to 4"
    assert (60000 - 32768, 12288 + 60000, 72288 - 32768, 2400 * 20) == (27232, 72288, 39520, 48000) and 48000 > 32768 and abs(60000 / 1024 - 58.6) < 0.05, "h4-sizing part 5 why lines"
    assert (1200 + 250 + 350 + 600 + 600, 4000 - 3000, 401 * 2 * 4 + 1024 * 16) == (3000, 1000, 19592) and 19592 < 32768, "h4-handler-aloud model: 3,000 ns, 1,000 slack, about 20 KB in L1"
    assert 401 == 400 + 1, "h4-handler-aloud model: a GBP 4 range in pennies is 401 levels"

    # Sequence policy of the lesson (apply at or above expected, count the skipped numbers, drop below): ledger rows l18-s4-*, q18-gap, q18-stale.
    def arbitrate(frames):
        expected, applied, gaps = 1, [], 0
        for i, seq in enumerate(frames):
            if seq < expected:
                continue
            gaps += seq - expected
            expected = seq + 1
            applied.append(i)
        return applied, gaps

    assert arbitrate([1, 1, 2, 2, 4, 3, 4, 5, 5]) == ([0, 2, 4, 7], 1), "l18-s4: 1A, 2A, 4A, 5A applied, gap 1"
    # Partial frames (ledger rows l18-s6, r4-two-reads).
    def reads(sizes, frame=24):
        held, out = 0, []
        for s in sizes:
            held += s
            out.append((held // frame, held % frame))
            held %= frame
        return out

    assert reads([50, 40, 80]) == [(2, 2), (1, 18), (4, 2)], "l18-s6: 2 and 2 left, 1 and 18 left, 4 and 2 left"
    assert sum(f for f, _ in reads([31, 41])) == 3 and reads([31, 41])[-1][1] == 0, "r4-two-reads: 3 frames, nothing left"

    # Code item: the Handler (screen 8). Expectations recomputed by a Python model of the contract, then the C++ solution and starter.
    s8 = L18["screens"][8]
    assert s8["title"] == "Build the handler"

    def frame(type_, side, seq, id_, qty, price):
        return (type_, side, seq, id_, qty, price)

    class Model:
        def __init__(self):
            self.qty = [[0] * 201, [0] * 201]
            self.orders = {}
            self.expected, self.gaps, self.applied = 1, 0, 0

        def feed(self, frames):
            for t, side, seq, id_, q, price in frames:
                if seq < self.expected:
                    continue
                if seq > self.expected:
                    self.gaps += seq - self.expected
                self.expected = seq + 1
                self.applied += 1
                if id_ >= 1024:
                    continue
                sd = 0 if side == "B" else 1
                o = self.orders.get(id_)
                if t == "A":
                    i = price - 9900
                    if not (0 <= i < 201) or (o and o["live"]):
                        continue
                    self.orders[id_] = {"side": sd, "price": price, "qty": q, "live": True}
                    self.qty[sd][i] += q
                elif t == "X" and o and o["live"]:
                    self.qty[o["side"]][o["price"] - 9900] -= o["qty"]
                    o["live"] = False
                elif t == "T" and o and o["live"]:
                    done = min(q, o["qty"])
                    o["qty"] -= done
                    self.qty[o["side"]][o["price"] - 9900] -= done
                    if o["qty"] == 0:
                        o["live"] = False

        def best_bid(self):
            return next((9900 + i for i in range(200, -1, -1) if self.qty[0][i] > 0), 0)

        def best_ask(self):
            return next((9900 + i for i in range(201) if self.qty[1][i] > 0), 0)

        def bid_qty(self, p):
            return self.qty[0][p - 9900]

    A, B, S = "A", "B", "S"
    cases = [
        ([frame(A, B, 1, 1, 100, 10000), frame(A, S, 2, 2, 50, 10010), frame(A, B, 3, 3, 40, 10005)], "best_bid", 10005),
        ([frame(A, B, 1, 1, 100, 10000), frame(A, S, 2, 2, 50, 10010), frame(A, B, 3, 3, 40, 10005)], "best_ask", 10010),
        ([frame(A, B, 1, 1, 100, 10000), frame(A, S, 2, 2, 50, 10010), frame(A, B, 3, 3, 40, 10005), frame("X", B, 4, 3, 0, 0)], "best_bid", 10000),
        ([frame(A, B, 1, 1, 100, 10000), frame(A, S, 2, 2, 50, 10010), frame(A, B, 3, 3, 40, 10005), frame("T", B, 4, 1, 30, 10000)], ("bid_qty", 10000), 70),
        ([frame(A, B, 1, 1, 100, 10000), frame("T", B, 2, 1, 150, 10000)], "best_bid", 0),
        ([frame(A, B, 1, 1, 10, 10000), frame(A, B, 2, 2, 10, 10001), frame(A, B, 5, 3, 10, 10002), frame(A, B, 6, 4, 10, 10003)], "gaps", 2),
        ([frame(A, B, 1, 1, 10, 10000), frame(A, B, 2, 2, 10, 10001), frame(A, B, 2, 3, 99, 10050)], "applied", 2),
        ([frame(A, B, 1, 1, 10, 10000), frame(A, B, 2, 2, 10, 10001), frame(A, B, 4, 3, 10, 10002), frame(A, B, 3, 4, 500, 10050)], "best_bid", 10002),
        ([frame(A, B, 3, 1, 10, 10000)], "gaps", 2),
        ([frame("X", B, 1, 9, 0, 0), frame(A, B, 2, 4000, 10, 10000), frame(A, B, 3, 5, 10, 12000), frame(A, B, 4, 6, 10, 9999)], "best_bid", 9999),
        ([frame(A, B, 1, 1, 100, 10000), frame(A, B, 2, 1, 70, 10003)], ("bid_qty", 10003), 0),
        ([frame(A, B, 1, 1, 100, 10000), frame(A, B, 2, 2, 40, 10000), frame("X", B, 3, 1, 0, 0), frame("X", B, 4, 1, 0, 0)], ("bid_qty", 10000), 40),
    ]
    for frames, what, exp in cases:
        m = Model()
        m.feed(frames)
        got = m.bid_qty(what[1]) if isinstance(what, tuple) else getattr(m, what) if what in ("gaps", "applied") else getattr(m, what)()
        assert got == exp, f"l18-s8 model check {what}: expected {exp}, model gives {got}"
    assert [t["expect"] for t in s8["widget"]["tests"]] == [10005, 10010, 10000, 70, 0, 2, 2, 10002, 2, 10005, 0, 9999, 0, 0, 40], "l18-s8 hidden-test expectations as the contract gives them"
    fails = check_code_item("l18-handler", s8, alloc_test_index=13)
    assert {"t3", "t4", "t6", "t7", "t13"} <= set(fails), "l18 Handler starter must fail cancels, trades, gaps, duplicates and the count"


# -------------------------------------------------------- homework-4 code

def h4_checks():
    it = item(H4, "h4-latency-hist")

    def bucket(ns):
        return min(39, max(1, ns).bit_length() - 1)

    def upper(samples, p):
        counts = [0] * 40
        for s in samples:
            counts[bucket(s)] += 1
        rank = max(1, math.ceil(Fraction(str(p)) * len(samples) / 100))
        seen = 0
        for b in range(40):
            seen += counts[b]
            if seen >= rank:
                return 1 << (b + 1)
        return 1 << 40

    assert bucket(10) == 3 and upper([10], 100) == 16, "h4-latency-hist explain: 10 ns is bucket 3 (8 to 15), upper bound 16"
    assert all(bucket(n) == math.floor(math.log2(n)) for n in range(1, 5000)), "h4-latency-hist prose: bucket is floor(log2 ns)"
    ladder = list(range(1, 11))
    exp = [([6] * 920 + [3000] * 80, 50, 8), ([6] * 920 + [3000] * 80, 92, 8), ([6] * 920 + [3000] * 80, 93, 4096), (ladder, 50, 8), (ladder, 90, 16), (ladder, 100, 16), (ladder, 31, 8),
           ([10] * 161 + [1000] * 89, 64.4, 16), ([35184372088832], 100, 1 << 40), ([0, 1, 2, 3], 50, 2), ([0, 1, 2, 3], 100, 4), ([1000000] * 5 + [100] * 95, 90, 128), ([1000000] * 5 + [100] * 95, 99, 1048576)]
    for k, (samples, p, e) in enumerate(exp, 1):
        assert upper(samples, p) == e == it["widget"]["tests"][k - 1]["expect"], f"h4-latency-hist test {k}: the bucket model gives {e}"
    assert 1 << 40 == 1099511627776 and 35184372088832 == 1 << 45, "h4-latency-hist test 9: 2^45 clamps to bucket 39, upper 2^40"
    fails = check_code_item("h4-hist", it, alloc_test_index=None)
    assert "t15" not in fails, "h4-latency-hist: the starter allocates nothing either; it fails on the percentiles (ledger h4-hist-how)"


def main():
    for f in (l15_checks, l16_checks, l17_checks, l18_checks, h4_checks):
        f()
        print("ok", f.__name__)
    for n in NOTES:
        print("note:", n)
    shutil.rmtree(WORK, ignore_errors=True)
    print("systems L4 concepts r2: all checks passed")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAILED:", e)
        shutil.rmtree(WORK, ignore_errors=True)
        sys.exit(1)
