"""Items of topic-3.5, part C: the systems items (22 to 30)."""
from helpers import *

I = {}

# ---------------------------------------------------------------- 22 latency ladder
I[22] = item(
    "e-seek-round-trips", 2, ["sy-memory"], ["latency-ladder"], 60,
    title="A seek against a round trip",
    prose="A disk seek takes 10 ms. A round trip inside one data centre takes 500 µs.",
    question="How many data-centre round trips fit in the time of one disk seek?",
    widget=numeric(20, abs_=0, placeholder="a number", label="Round trips", unit="round trips",
                   wrong=[("inverted", 0.05, 0.001), ("tenth-of-ms", 200, 0), ("units-ignored", 2, 0)], accept="20"),
    feedback=fb("10 ms is 10,000 µs, and $10{,}000 / 500 = 20$.",
                "Write both times in the same unit, then divide the larger by the smaller.",
                {"inverted": "You divided the round trip by the seek. Divide the longer time by the shorter one.",
                 "tenth-of-ms": "You read 500 µs as 0.05 ms. It is 0.5 ms, so the quotient is 20.",
                 "units-ignored": "You divided 10 by 5 and dropped the units. Convert 10 ms to 10,000 µs first."}),
    explain="10 ms is 10,000 µs. Divide by 500 µs to get 20 round trips.")

# ---------------------------------------------------------------- 23 cache misses
I[23] = item(
    "e-stride-misses", 3, ["sy-memory"], ["cache-misses"], 120,
    title="Count the misses of a stride",
    prose="An array of `double` (8 bytes each) starts on a 64-byte line boundary. A loop reads `a[0]`, `a[3]`, `a[6]` and so on, 1,000 reads in all. The cache starts cold and is big enough to keep every line it loads.",
    question="How many of the reads miss the cache?",
    widget=numeric(375, abs_=0, placeholder="a whole number", label="Misses", unit="misses",
                   wrong=[("every-read", 1000, 0), ("unit-stride", 125, 0), ("one-in-three", 333, 0)], accept="375"),
    feedback=fb("The reads span lines 0 to 374, and every line in between is touched once: 375 misses.",
                "Find the line of the last read, then ask whether any line is skipped.",
                {"every-read": "You counted every read as a miss. Reads 24 bytes apart often land in the same 64-byte line.",
                 "unit-stride": "You counted for 1,000 neighbouring doubles, 8,000 bytes. These reads span about 24,000 bytes.",
                 "one-in-three": "You divided by 3. A line holds about 2.7 reads here, so count the lines covered instead."}),
    explain="Read $k$ is at byte $24k$, so the last is at byte 23,976, in line 374. The stride is below 64 bytes, so every line from 0 to 374 is touched. That makes 375 misses.")

# ---------------------------------------------------------------- 24 struct padding (tap-regions on a grid)
def _cells():
    return [[str(r * 8 + c) for c in range(8)] for r in range(3)]


def rc(k):
    return "r%dc%d" % (k // 8 + 1, k % 8 + 1)


PAD24 = [rc(k) for k in (1, 2, 3, 10, 11, 12, 13, 14, 15)]
I[24] = item(
    "e-tick-padding", 3, ["sy-memory"], ["struct-padding"], 150,
    title="Where is the padding",
    prose="`struct Tick { uint8_t side; uint32_t qty; uint16_t venue; uint64_t id; };` Each field starts at a multiple of its own size. The struct's size is a multiple of its largest field. The grid shows its 24 bytes by offset, 8 to a row.",
    canvas={"kind": "grid", "params": {"rows": 3, "cols": 8, "rowHeads": False, "colHeads": False, "cells": _cells()},
            "state": {"caption": "24 bytes, numbered by offset. Each row is 8 bytes."}},
    question="Tap every byte that is padding.",
    widget={"kind": "tap-regions", "answer": PAD24, "countWord": "tapped",
            "wrong": [{"id": "first-gap-only", "set": [rc(1), rc(2), rc(3)]},
                      {"id": "second-gap-only", "set": [rc(k) for k in (10, 11, 12, 13, 14, 15)]}]},
    feedback=fb("9 of the 24 bytes are padding: bytes 1 to 3, and bytes 10 to 15.",
                "Find where each field must start, and mark the bytes skipped before it.",
                {"first-gap-only": "You found the gap before `qty` only. `id` must start at 16, so bytes 10 to 15 are skipped too.",
                 "second-gap-only": "You found the gap before `id` only. `qty` must start at 4, so bytes 1 to 3 are skipped too.",
                 rc(0): "Byte 0 holds `side`.",
                 rc(4): "Bytes 4 to 7 hold `qty`.",
                 rc(8): "Bytes 8 and 9 hold `venue`.",
                 rc(16): "Bytes 16 to 23 hold `id`."}),
    explain="`qty` must start at a multiple of 4, so bytes 1 to 3 are skipped. `id` must start at a multiple of 8, so bytes 10 to 15 are skipped. That is 9 padding bytes in 24.",
    explain_canvas={"shade": {"pad": PAD24}})

# ---------------------------------------------------------------- 25 page fault
I[25] = item(
    "e-first-write-fault", 3, ["sy-memory", "sy-os"], ["page-fault"], 120,
    title="Why the first loop is slow",
    prose="A program calls `malloc` for a 192 MiB buffer. A loop then writes one byte into each 4 KiB page. That first loop is slow. A second identical loop over the same buffer is far faster.",
    question="What explains the slow first loop?",
    widget=choice([
        ("a", "Each first write to a page traps into the kernel, which maps a zeroed page.", True, None),
        ("b", "Each write misses every cache level and waits for the disk.", False,
         "New memory is not read from disk. The kernel creates a zeroed page, so there is nothing to fetch."),
        ("c", "A cold TLB makes every write cost as much as a page fault.", False,
         "A TLB miss is a hardware page-table walk of tens of cycles. A fault enters the kernel and costs far more."),
        ("d", "`malloc` zeroed the whole buffer when it was called, and the loop pays for it.", False,
         "For a large request `malloc` touches no pages. The kernel supplies each page on its first write."),
    ]),
    feedback=fb("The buffer is address space until first use. Each first write to a page faults once.",
                "Ask what the kernel has to do the first time a program touches a page."),
    explain="The 192 MiB is only address space until it is used. The first write to each of its 49,152 pages traps into the kernel, which maps a zeroed page. The second loop finds every page already mapped.")

# ---------------------------------------------------------------- 26 branch cost
I[26] = item(
    "e-wrong-guesses", 2, ["sy-memory", "sy-latency"], ["branch-cost"], 60,
    title="The cost of wrong guesses",
    prose="A loop tests 2,000,000 prices with `if (p < limit)`. The test is true for 30% of them, in no pattern. The predictor always guesses the likelier outcome. Each wrong guess costs 14 cycles.",
    question="How many cycles do the wrong guesses cost in all?",
    widget=numeric(8400000, abs_=0, placeholder="a whole number", label="Cycles", unit="cycles",
                   wrong=[("coin-flip", 14000000, 0), ("every-pass", 28000000, 0), ("likelier-side", 19600000, 0)], accept="8,400,000"),
    feedback=fb("The wrong guesses are 30% of 2,000,000, so 600,000 of them. At 14 cycles that is 8.4 million.",
                "Count the wrong guesses first, then multiply by the cost of one.",
                {"coin-flip": "You assumed half are wrong. The predictor picks the likelier side, so only 30% are.",
                 "every-pass": "You charged every pass 14 cycles. Only the wrong guesses pay.",
                 "likelier-side": "You counted the 70% that are false. The predictor guesses those, so the 30% are the misses."}),
    explain="The predictor always guesses the likelier outcome, so it is wrong on the 30% that go the other way. That is $2{,}000{,}000 \\times 0.3 = 600{,}000$ wrong guesses. At 14 cycles each, the cost is 8.4 million cycles.")

# ---------------------------------------------------------------- 27 race claims
I[27] = item(
    "e-two-statements", 3, ["sy-concurrency"], ["race-claims"], 150,
    title="Two threads, one integer",
    prose="Two threads start together on a shared `int n = 0;` with no lock. Thread A runs `n = n + 2;`. Thread B runs `n = n * 3;`. Each statement reads `n`, calculates, then writes `n`.",
    question="Select all that apply. Which claims hold?",
    widget=multi([
        ("a", "Some interleavings give a final value of 0.", True, None),
        ("b", "Making `n` a `std::atomic<int>` removes the data race but not the 0.", True, None),
        ("c", "With a mutex around each whole statement, the final value is 2 or 6.", True, None),
        ("d", "The only possible final values are 2 and 6.", False,
         "You counted the two whole-statement orders. A write can use a stale read, which gives 0."),
        ("e", "A final value of 8 is possible.", False,
         "8 needs A to read a 6. A reads before it writes, and 6 exists only after A has written."),
        ("f", "Declaring `n` as `volatile int` makes each statement indivisible.", False,
         "`volatile` stops the compiler caching `n`. It does not make the read and the write one step."),
    ]),
    feedback=fb("Claims a, b and c hold. The final value can be 0, 2 or 6, and never 8.",
                "Step the two threads through the reads and writes in different orders."),
    explain="A can read 0, B can finish and write 0, and then A writes 2. Another order gives 0 as the last write, so 0, 2 and 6 are all possible, and 8 is not. An atomic removes the undefined behaviour, but only a mutex per statement forces 2 or 6.")

# ---------------------------------------------------------------- 28 feed design
I[28] = item(
    "e-feed-design", 4, ["sy-os", "sy-latency"], ["transport-pick"], 180,
    title="One feed, thirty servers",
    prose="An exchange sends 2,000 price updates a second. Thirty strategy servers in one rack must each see every update. A server must never act on a gap it has not noticed.",
    question="Which design suits the feed?",
    widget=choice([
        ("a", "Multicast UDP with a sequence number on each message, and a TCP channel to ask for a replay", True, None),
        ("b", "One TCP connection from the exchange to each server, so the network guarantees every message", False,
         "The exchange sends thirty copies, and one lost packet holds back that server's stream until the retransmit."),
        ("c", "Multicast UDP with no sequence numbers, because the next update replaces a lost one", False,
         "A lost message may be a trade or a cancel. Without sequence numbers a server cannot tell it missed one."),
        ("d", "UDP unicast to each server, resent every 10 ms until it is acknowledged", False,
         "Acknowledged resends rebuild the delays of TCP, and the exchange still sends thirty copies."),
    ]),
    feedback=fb("Multicast sends one copy to all thirty. Sequence numbers expose a gap and a replay repairs it.",
                "Ask which design sends one copy and still lets a server notice a missing message."),
    explain="Multicast sends one copy that all thirty servers receive. A sequence number on each message shows a server where it missed one. A TCP channel then fetches the missing messages without delaying the live stream.")

# ---------------------------------------------------------------- 29 tail percentile
LAT = [212, 198, 205, 219, 201, 207, 3100, 214, 203, 209, 196, 211, 206, 202, 2650, 208, 200, 215, 204, 210, 197, 213, 199, 216, 205]
I[29] = item(
    "e-p96-latency", 5, ["sy-latency"], ["tail-percentile"], 300,
    title="The 96th percentile of 25 messages",
    prose="A handler timed 25 messages, in µs.\n\n```text\n" + "\n".join(" ".join(str(v) for v in LAT[i:i + 5]) for i in range(0, 25, 5)) + "\n```\n\nUse the nearest-rank rule: the $p$th percentile is the value at rank $\\lceil pn/100 \\rceil$ in the sorted list, counting from 1.",
    question="What is the 96th percentile, in µs?",
    widget=numeric(2650, abs_=0, unit="µs", placeholder="a whole number", label="96th percentile",
                   wrong=[("mean", 420, 0), ("maximum", 3100, 0), ("median", 207, 0), ("interpolated", 2668, 0.5)], accept="2650"),
    feedback=fb("Rank $\\lceil 0.96 \\times 25 \\rceil = 24$, and the 24th sorted value is 2650 µs.",
                "Sort the list, find the rank, then read that value.",
                {"mean": "You gave the mean, 420 µs. It is twice every typical message and far below both slow ones.",
                 "maximum": "You took the largest value. The rank is 24 of 25, so one value sits above it.",
                 "median": "You gave the median. The 96th percentile sits near the top of the sorted list.",
                 "interpolated": "You interpolated between two values. The nearest-rank rule returns a value from the list."}),
    explain="Sorted, the 24th of 25 values is 2650, because $\\lceil 0.96 \\times 25 \\rceil = 24$. The mean is 420 µs, a figure no typical message resembles. Two slow messages lift the mean from about 207 to 420, while the median stays at 207.")

# ---------------------------------------------------------------- 30 ring indices (C++)
SOL30 = '''#include <vector>

std::vector<int> newest_first(const std::vector<int>& xs, int capacity, int k) {
    std::vector<int> buf(capacity);
    unsigned count = 0;
    unsigned mask = capacity - 1;
    for (int x : xs) {
        buf[count & mask] = x;
        ++count;
    }
    int held = count < (unsigned)capacity ? (int)count : capacity;
    int take = k < held ? k : held;
    std::vector<int> out;
    for (int i = 0; i < take; ++i) {
        out.push_back(buf[(count - 1 - i) & mask]);
    }
    return out;
}
'''
START30 = '''#include <vector>

// capacity is a power of two. One counter only grows.
// Counter c uses slot c & (capacity - 1).
// A full ring overwrites its oldest value.
// Return the newest k values held, newest first.
std::vector<int> newest_first(const std::vector<int>& xs, int capacity, int k) {
    // Your code here
    return {};
}
'''
import random as _r
_rr = _r.Random(305)
BIG30 = [_rr.randint(1, 999) for _ in range(300)]


def _ref30(xs, cap, k):
    held = xs[-cap:] if xs else []
    return list(reversed(held))[:k]


def _case30(xs, cap, k):
    return {"call": "newest_first", "args": [xs, cap, k], "types": ["std::vector<int>", "int", "int"],
            "expect": _ref30(xs, cap, k), "compare": "equal"}


T30 = [_case30([4, 8, 15, 16, 23, 42], 4, 3),
       _case30([1, 2, 3], 8, 5),
       _case30(list(range(1, 21)), 8, 8),
       _case30([9, 7], 1, 1),
       _case30(BIG30, 32, 25),
       _case30([], 4, 3)]
I[30] = item(
    "e-newest-first", 5, ["sy-latency", "sy-concurrency"], ["ring-index"], 600,
    title="The newest values in a ring",
    prose="A price feed keeps its newest values in a ring of `capacity` slots, a power of two. One counter grows with every push and never wraps back. The value pushed with counter $c$ lives in slot `c & (capacity - 1)`, and a full ring overwrites its oldest value. The code runs on one thread.",
    question="Write `newest_first(xs, capacity, k)`. Push every value of `xs` in order, then return the newest `k` values still held, newest first. If fewer than `k` are held, return them all.",
    widget=code_cpp(START30, SOL30, [T30[0]], T30,
                    how="Check runs 6 hidden tests. They cover a ring that wraps, fewer values than `k` and a capacity of 1. They also run 300 pushes through 32 slots and an empty list. A wrong mask fails the wrapping tests."),
    feedback=fb("Write each value at `count & mask`, then read back from `count - 1` downwards with the same mask.",
                "Run it by hand with capacity 4 and six values, and write down which slot each value takes."),
    explain="With a power-of-two capacity, `c & (capacity - 1)` keeps the low bits of the counter, which is the counter modulo the capacity. Writing there overwrites the oldest value once the ring is full. Reading from `count - 1` downwards with the same mask returns the newest values first.")

ITEMS_C = I
