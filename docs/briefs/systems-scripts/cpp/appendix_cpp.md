### P-translate: l3-virtual-memory: translate

Where: `l3-virtual-memory`, a `code` screen after the worked examples, difficulty 2. Widget `code`, `language: "cpp"`, 10 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// frames[p] is the physical frame of virtual page p, or -1 if p is not mapped.
// Pages are 4096 bytes. Return the physical address, or -1 for a page fault.
long long translate(const std::vector<int>& frames, long long vaddr) {
    long long page = vaddr / 4096;
    if (page >= static_cast<long long>(frames.size())) return -1;
    return static_cast<long long>(frames[page]) * 4096;
}
```

Reference solution:

```cpp
#include <vector>

long long translate(const std::vector<int>& frames, long long vaddr) {
    long long page = vaddr / 4096;
    long long offset = vaddr % 4096;
    if (page >= static_cast<long long>(frames.size())) return -1;
    if (frames[page] < 0) return -1;
    return static_cast<long long>(frames[page]) * 4096 + offset;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `translate({7,-1,9}, 10876)` expects `39548`
- `translate({7,-1,9}, 0)` expects `28672`
- `translate({7,-1,9}, 4095)` expects `32767`
- `translate({7,-1,9}, 8192)` expects `36864`
- `translate({7,-1,9}, 12287)` expects `40959`
- `translate({7,-1,9}, 4096)` expects `-1`
- `translate({7,-1,9}, 20480)` expects `-1`
- `translate({3,5}, 4113)` expects `20497`
- `translate({}, 0)` expects `-1`
- `translate({0}, 4095)` expects `4095`

Checked by `cpp/build_md.py`: the solution passes all 10 tests and the starter fails 6 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-struct-size: l4-object-layout: struct size

Where: `l4-object-layout`, a `code` screen after the layout table, difficulty 3. Widget `code`, `language: "cpp"`, 15 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// sizes: the size in bytes of each field, in declaration order.
// Each field is aligned to its own size (1, 2, 4 or 8).
int struct_size(const std::vector<int>& sizes) {
    int total = 0;
    for (int s : sizes) total += s;
    return total;
}

// The size after sorting the fields from largest to smallest.
int best_size(const std::vector<int>& sizes) {
    return struct_size(sizes);
}
```

Reference solution:

```cpp
#include <algorithm>
#include <functional>
#include <vector>

int struct_size(const std::vector<int>& sizes) {
    int offset = 0, widest = 1;
    for (int s : sizes) {
        offset = (offset + s - 1) / s * s;   // round up to a multiple of s
        offset += s;
        widest = std::max(widest, s);
    }
    return (offset + widest - 1) / widest * widest;   // tail padding
}

int best_size(const std::vector<int>& sizes) {
    std::vector<int> sorted = sizes;
    std::sort(sorted.begin(), sorted.end(), std::greater<int>());
    return struct_size(sorted);
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `struct_size({1,8,1})` expects `24`
- `best_size({1,8,1})` expects `16`
- `struct_size({1,4,1,4,2,4,4,4})` expects `32`
- `best_size({1,4,1,4,2,4,4,4})` expects `24`
- `struct_size({})` expects `0`
- `struct_size({1})` expects `1`
- `best_size({1})` expects `1`
- `struct_size({2,1})` expects `4`
- `best_size({2,1})` expects `4`
- `struct_size({8,1})` expects `16`
- `best_size({8,1})` expects `16`
- `struct_size({4,1,2,1,8})` expects `24`
- `best_size({4,1,2,1,8})` expects `16`
- `struct_size({1,2,4,8,1,2,4,8})` expects `32`
- `best_size({1,2,4,8,1,2,4,8})` expects `32`

Checked by `cpp/build_md.py`: the solution passes all 15 tests and the starter fails 10 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-mispredicts: l5-branches: two-bit predictor

Where: `l5-branches`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 10 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <string>

// Count the mispredictions of a two-bit saturating counter on a branch history.
// 'T' is taken, 'N' is not taken. The counter runs 0..3, starts at 1,
// predicts taken at 2 or 3, moves up on T and down on N, and stops at 0 and 3.
int mispredicts(const std::string& history) {
    int taken = 0, misses = 0;   // one bit: remember the last outcome
    for (char c : history) {
        int actual = (c == 'T');
        if (taken != actual) ++misses;
        taken = actual;
    }
    return misses;
}
```

Reference solution:

```cpp
#include <string>

int mispredicts(const std::string& history) {
    int counter = 1, misses = 0;
    for (char c : history) {
        bool predicted_taken = counter >= 2;
        bool actual_taken = (c == 'T');
        if (predicted_taken != actual_taken) ++misses;
        if (actual_taken) { if (counter < 3) ++counter; }
        else { if (counter > 0) --counter; }
    }
    return misses;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `mispredicts("TTTTTTTT")` expects `1`
- `mispredicts("NNNN")` expects `0`
- `mispredicts("TNTNTNTN")` expects `8`
- `mispredicts("TTNTTNTTN")` expects `4`
- `mispredicts("TTTNNN")` expects `3`
- `mispredicts("TTTTTTTNTTTTTTTNTTTTTTTN")` expects `4`
- `mispredicts("")` expects `0`
- `mispredicts("T")` expects `1`
- `mispredicts("TTNTTNTTNTTNTTNTTNTTNTTNTTNTTN")` expects `11`
- `mispredicts("NTTT")` expects `2`

Checked by `cpp/build_md.py`: the solution passes all 10 tests and the starter fails 5 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-cache-sim: homework-1: a cache simulator

Where: `homework-1`, the homework `code` item, difficulty 4. Widget `code`, `language: "cpp"`, 10 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// A cache of num_lines lines of 64 bytes, in sets of `ways` lines each (num_lines is a multiple of ways).
// The line holding byte address a is a / 64 and it lives in set (a / 64) % (num_lines / ways).
// A full set drops its least recently used line. Start empty. Return the number of misses.
int count_misses(int num_lines, int ways, const std::vector<int>& addresses) {
    int misses = 0;
    for (int a : addresses) {
        (void)a;
        ++misses;     // TODO: an access whose line is already in its set is a hit
    }
    return misses;
}
```

Reference solution:

```cpp
#include <list>
#include <vector>

int count_misses(int num_lines, int ways, const std::vector<int>& addresses) {
    int sets = num_lines / ways;
    std::vector<std::list<int>> cache(sets);      // front = most recently used
    int misses = 0;
    for (int a : addresses) {
        int line = a / 64;
        std::list<int>& set = cache[line % sets];
        bool hit = false;
        for (auto it = set.begin(); it != set.end(); ++it) {
            if (*it == line) { set.erase(it); hit = true; break; }
        }
        if (!hit) {
            ++misses;
            if (static_cast<int>(set.size()) == ways) set.pop_back();
        }
        set.push_front(line);
    }
    return misses;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `count_misses(4, 1, {0, 256, 8, 264, 16, 272, 24, 280, 32, 288, 40, 296, 48, 304, 56, 312})` expects `16`
- `count_misses(4, 2, {0, 256, 8, 264, 16, 272, 24, 280, 32, 288, 40, 296, 48, 304, 56, 312})` expects `2`
- `count_misses(4, 1, {0, 320, 8, 328, 16, 336, 24, 344, 32, 352, 40, 360, 48, 368, 56, 376})` expects `2`
- `count_misses(4, 4, {0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 264, 272, 280, 288, 296, 304, 312, 320, 328, 336, 344, 352, 360, 368, 376, 384, 392, 400, 408, 416, 424, 432, 440, 448, 456, 464, 472, 480, 488, 496, 504})` expects `8`
- `count_misses(4, 4, {0, 64, 128, 192, 256, 320, 384, 448, 8, 72, 136, 200, 264, 328, 392, 456, 16, 80, 144, 208, 272, 336, 400, 464, 24, 88, 152, 216, 280, 344, 408, 472, 32, 96, 160, 224, 288, 352, 416, 480, 40, 104, 168, 232, 296, 360, 424, 488, 48, 112, 176, 240, 304, 368, 432, 496, 56, 120, 184, 248, 312, 376, 440, 504})` expects `64`
- `count_misses(8, 8, {0, 64, 128, 192, 256, 320, 384, 448, 8, 72, 136, 200, 264, 328, 392, 456, 16, 80, 144, 208, 272, 336, 400, 464, 24, 88, 152, 216, 280, 344, 408, 472, 32, 96, 160, 224, 288, 352, 416, 480, 40, 104, 168, 232, 296, 360, 424, 488, 48, 112, 176, 240, 304, 368, 432, 496, 56, 120, 184, 248, 312, 376, 440, 504})` expects `8`
- `count_misses(512, 8, {0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496})` expects `8`
- `count_misses(512, 8, {0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360, 384, 408, 432, 456, 480, 504, 528, 552, 576, 600, 624, 648, 672, 696, 720, 744})` expects `12`
- `count_misses(4, 4, {})` expects `0`
- `count_misses(2, 2, {0, 64, 128, 0, 64, 128})` expects `6`

Checked by `cpp/build_md.py`: the solution passes all 10 tests and the starter fails 6 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-final-counts: l7-data-races: count every outcome

Where: `l7-data-races`, a `code` screen after the interleaving drill, difficulty 4. Widget `code`, `language: "cpp"`, 7 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// threads threads each run `increments` times: load x, add 1, store x (three steps).
// Try every interleaving of all the steps. result[v] is how many interleavings end with x == v.
std::vector<int> final_counts(int threads, int increments) {
    // Wrong model: an increment is one indivisible step.
    std::vector<int> done(threads, 0);
    std::vector<int> result(threads * increments + 1, 0);
    // count schedules of whole increments: every one ends with the full total
    std::vector<int> fact(threads * increments + 1, 1);
    for (int i = 1; i <= threads * increments; ++i) fact[i] = fact[i - 1] * i;
    long long ways = fact[threads * increments];
    for (int t = 0; t < threads; ++t) ways /= fact[increments];
    result[threads * increments] = static_cast<int>(ways);
    return result;
}
```

Reference solution:

```cpp
#include <vector>

namespace {
struct Walker {
    int threads, steps;                  // steps = 3 * increments, per thread
    std::vector<int> pc, reg;            // next step and register of each thread
    int x = 0;
    std::vector<int> result;
    void go() {
        bool any = false;
        for (int t = 0; t < threads; ++t) {
            if (pc[t] == steps) continue;
            any = true;
            int old_x = x, old_reg = reg[t];
            int phase = pc[t] % 3;
            if (phase == 0) reg[t] = x;            // load
            else if (phase == 1) reg[t] += 1;      // add
            else x = reg[t];                       // store
            ++pc[t];
            go();
            --pc[t];
            x = old_x;
            reg[t] = old_reg;
        }
        if (!any) ++result[x];
    }
};
}

std::vector<int> final_counts(int threads, int increments) {
    Walker w;
    w.threads = threads;
    w.steps = 3 * increments;
    w.pc.assign(threads, 0);
    w.reg.assign(threads, 0);
    w.result.assign(threads * increments + 1, 0);
    w.go();
    return w.result;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `final_counts(1, 1)` expects `[0, 1]`
- `final_counts(1, 3)` expects `[0, 0, 0, 1]`
- `final_counts(2, 1)` expects `[0, 18, 2]`
- `final_counts(3, 1)` expects `[0, 1404, 270, 6]`
- `final_counts(2, 2)` expects `[0, 0, 702, 216, 6]`
- `final_counts(2, 3)` expects `[0, 0, 648, 30780, 15714, 1458, 20]`
- `final_counts(4, 1)` expects `[0, 291600, 74952, 3024, 24]`

Checked by `cpp/build_md.py`: the solution passes all 7 tests and the starter fails 5 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-lock-cycle: l8-locks-and-deadlock: lock-order cycle

Where: `l8-locks-and-deadlock`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 12 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <string>
#include <vector>

// Each string is one thread: the locks it takes, in order, each held while it takes the next ("AB" takes A, then B).
// Return true if the lock-order graph (an edge from each held lock to each lock taken after it) has a cycle.
bool has_lock_cycle(const std::vector<std::string>& threads) {
    // Only checks whether two threads share a lock, which is not the same as a cycle.
    for (size_t a = 0; a < threads.size(); ++a)
        for (size_t b = a + 1; b < threads.size(); ++b)
            for (char c : threads[a])
                if (threads[b].find(c) != std::string::npos) return true;
    return false;
}
```

Reference solution:

```cpp
#include <string>
#include <vector>

namespace {
bool visit(int n, const bool edge[26][26], int state[26]) {   // 0 new, 1 on the path, 2 finished
    state[n] = 1;
    for (int m = 0; m < 26; ++m) {
        if (!edge[n][m]) continue;
        if (state[m] == 1) return true;
        if (state[m] == 0 && visit(m, edge, state)) return true;
    }
    state[n] = 2;
    return false;
}
}

bool has_lock_cycle(const std::vector<std::string>& threads) {
    bool edge[26][26] = {};
    for (const auto& s : threads)
        for (size_t i = 0; i < s.size(); ++i)
            for (size_t j = i + 1; j < s.size(); ++j)
                edge[s[i] - 'A'][s[j] - 'A'] = true;
    int state[26] = {};
    for (int n = 0; n < 26; ++n)
        if (state[n] == 0 && visit(n, edge, state)) return true;
    return false;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `has_lock_cycle({"AB", "BA"})` expects `true`
- `has_lock_cycle({"AB", "AB"})` expects `false`
- `has_lock_cycle({"AB", "BC", "CA"})` expects `true`
- `has_lock_cycle({"AB", "BC", "AC"})` expects `false`
- `has_lock_cycle({"A", "A"})` expects `false`
- `has_lock_cycle({"ABC", "CBA"})` expects `true`
- `has_lock_cycle({"AB", "CD"})` expects `false`
- `has_lock_cycle({})` expects `false`
- `has_lock_cycle({"AA"})` expects `true`
- `has_lock_cycle({"AB", "BC", "CD", "DA"})` expects `true`
- `has_lock_cycle({"ABC", "BCD", "ACD"})` expects `false`
- `has_lock_cycle({"AC", "BD", "CB"})` expects `false`

Checked by `cpp/build_md.py`: the solution passes all 12 tests and the starter fails 6 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-blocked-counts: homework-2: bounded buffer

Where: `homework-2`, the homework `code` item, difficulty 3. Widget `code`, `language: "cpp"`, 7 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <string>
#include <vector>

// A queue holds at most `capacity` items. The events run in order on one thread:
// 'P' pushes an item, 'C' pops one. A push on a full queue and a pop on an empty queue each
// would block, so skip the event and count it. Return {blocked pushes, blocked pops, items left}.
std::vector<int> blocked_counts(int capacity, const std::string& events) {
    int items = 0, blocked_push = 0, blocked_pop = 0;
    for (char e : events) {
        if (e == 'P') ++items;
        else --items;
    }
    return {blocked_push, blocked_pop, items};
}
```

Reference solution:

```cpp
#include <string>
#include <vector>

std::vector<int> blocked_counts(int capacity, const std::string& events) {
    int items = 0, blocked_push = 0, blocked_pop = 0;
    for (char e : events) {
        if (e == 'P') {
            if (items == capacity) ++blocked_push;
            else ++items;
        } else {
            if (items == 0) ++blocked_pop;
            else --items;
        }
    }
    return {blocked_push, blocked_pop, items};
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `blocked_counts(2, "PPPCCC")` expects `[1, 1, 0]`
- `blocked_counts(2, "CCPP")` expects `[0, 2, 2]`
- `blocked_counts(1, "PPCCPC")` expects `[1, 1, 0]`
- `blocked_counts(3, "PPPPPPCCC")` expects `[3, 0, 0]`
- `blocked_counts(4, "")` expects `[0, 0, 0]`
- `blocked_counts(2, "PCPCPC")` expects `[0, 0, 0]`
- `blocked_counts(2, "PPPPCC")` expects `[2, 0, 0]`

Checked by `cpp/build_md.py`: the solution passes all 7 tests and the starter fails 5 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-find-gaps: l13-tcp-and-udp: find the missing sequence numbers

Where: `l13-tcp-and-udp`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 13 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// A UDP feed numbers its messages 1, 2, 3, ... Messages may arrive late or twice.
// Given the sequence numbers in arrival order, return every number from 1 up to the largest seen
// that has not arrived, smallest first.
std::vector<int> find_gaps(const std::vector<int>& seqs) {
    std::vector<int> missing;
    int expected = 1;
    for (int s : seqs) {
        while (expected < s) missing.push_back(expected++);   // a jump means a gap
        if (s == expected) ++expected;
    }
    return missing;
}
```

Reference solution:

```cpp
#include <algorithm>
#include <vector>

std::vector<int> find_gaps(const std::vector<int>& seqs) {
    if (seqs.empty()) return {};
    int largest = *std::max_element(seqs.begin(), seqs.end());
    std::vector<bool> seen(largest + 1, false);
    for (int s : seqs) seen[s] = true;
    std::vector<int> missing;
    for (int n = 1; n <= largest; ++n)
        if (!seen[n]) missing.push_back(n);
    return missing;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `find_gaps({1, 2, 4, 5})` expects `[3]`
- `find_gaps({1, 3, 2})` expects `[]`
- `find_gaps({2, 3})` expects `[1]`
- `find_gaps({1, 5})` expects `[2, 3, 4]`
- `find_gaps({1, 2, 2, 4, 4})` expects `[3]`
- `find_gaps({})` expects `[]`
- `find_gaps({3, 1, 2, 6, 5})` expects `[4]`
- `find_gaps({1, 2, 3, 7, 8, 10})` expects `[4, 5, 6, 9]`
- `find_gaps({5, 4, 3, 2, 1})` expects `[]`
- `find_gaps({2, 1, 4, 3, 6})` expects `[5]`
- `find_gaps({4, 2, 3})` expects `[1]`
- `find_gaps({1, 4, 2, 3})` expects `[]`
- `find_gaps({3, 3, 1})` expects `[2]`

Checked by `cpp/build_md.py`: the solution passes all 13 tests and the starter fails 7 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-wire: l14-messages-on-the-wire: encode and decode

Where: `l14-messages-on-the-wire`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 12 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `prelude`:

```cpp
struct Msg {
    int type;            // 'A' add, 'X' cancel, 'T' trade
    int side;            // 'B' or 'S'
    int instrument;      // 0..65535
    unsigned seq;
    unsigned id;
    unsigned qty;
    int price;           // pence, may be negative
    unsigned time;       // milliseconds since midnight
};
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// Wire layout, 24 bytes, big-endian (most significant byte first):
//   0 type (1)   1 side (1)   2 instrument (2)   4 seq (4)
//   8 id (4)    12 qty (4)   16 price (4, signed)  20 time (4)
std::vector<int> encode(const Msg& m) {
    std::vector<int> out(24, 0);
    out[0] = m.type;
    out[1] = m.side;
    // TODO: the other fields, most significant byte first
    return out;
}

Msg decode(const std::vector<int>& b) {
    Msg m{};
    m.type = b[0];
    m.side = b[1];
    // TODO: the other fields
    return m;
}
```

Reference solution:

```cpp
#include <vector>

namespace {
void put(std::vector<int>& out, int at, unsigned v, int bytes) {
    for (int k = 0; k < bytes; ++k)
        out[at + k] = (v >> (8 * (bytes - 1 - k))) & 0xFF;
}
unsigned get(const std::vector<int>& b, int at, int bytes) {
    unsigned v = 0;
    for (int k = 0; k < bytes; ++k) v = (v << 8) | static_cast<unsigned>(b[at + k] & 0xFF);
    return v;
}
}

std::vector<int> encode(const Msg& m) {
    std::vector<int> out(24, 0);
    out[0] = m.type;
    out[1] = m.side;
    put(out, 2, static_cast<unsigned>(m.instrument), 2);
    put(out, 4, m.seq, 4);
    put(out, 8, m.id, 4);
    put(out, 12, m.qty, 4);
    put(out, 16, static_cast<unsigned>(m.price), 4);
    put(out, 20, m.time, 4);
    return out;
}

Msg decode(const std::vector<int>& b) {
    Msg m{};
    m.type = b[0];
    m.side = b[1];
    m.instrument = static_cast<int>(get(b, 2, 2));
    m.seq = get(b, 4, 4);
    m.id = get(b, 8, 4);
    m.qty = get(b, 12, 4);
    m.price = static_cast<int>(get(b, 16, 4));
    m.time = get(b, 20, 4);
    return m;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `Msg m{65, 66, 258, 70000u, 123456789u, 100u, 10275, 36000000u}; encode(m)` expects `[65, 66, 1, 2, 0, 1, 17, 112, 7, 91, 205, 21, 0, 0, 0, 100, 0, 0, 40, 35, 2, 37, 81, 0]`
- `Msg m{88, 83, 1, 1u, 2u, 0u, -25, 0u}; encode(m)` expects `[88, 83, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 255, 255, 255, 231, 0, 0, 0, 0]`
- `Msg m{84, 66, 65535, 4294967295u, 4294967295u, 4294967295u, 2147483647, 86399999u}; encode(m)` expects `[84, 66, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127, 255, 255, 255, 5, 38, 91, 255]`
- `Msg m{65, 83, 0, 0u, 0u, 1u, (-2147483647 - 1), 1u}; encode(m)` expects `[65, 83, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 128, 0, 0, 0, 0, 0, 0, 1]`
- `decode(std::vector<int>{65, 66, 1, 2, 0, 1, 17, 112, 7, 91, 205, 21, 0, 0, 0, 100, 0, 0, 40, 35, 2, 37, 81, 0}).instrument` expects `258`
- `decode(std::vector<int>{65, 66, 1, 2, 0, 1, 17, 112, 7, 91, 205, 21, 0, 0, 0, 100, 0, 0, 40, 35, 2, 37, 81, 0}).price` expects `10275`
- `decode(std::vector<int>{88, 83, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 255, 255, 255, 231, 0, 0, 0, 0}).price` expects `-25`
- `(long long)decode(std::vector<int>{84, 66, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127, 255, 255, 255, 5, 38, 91, 255}).seq` expects `4294967295`
- `(long long)decode(std::vector<int>{84, 66, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127, 255, 255, 255, 5, 38, 91, 255}).time` expects `86399999`
- `decode(std::vector<int>{65, 83, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 128, 0, 0, 0, 0, 0, 0, 1}).price` expects `-2147483648`
- `Msg m{65, 66, 258, 70000u, 123456789u, 100u, 10275, 36000000u}; Msg d = decode(encode(m)); (long long)d.id` expects `123456789`
- `Msg m{84, 66, 65535, 4294967295u, 4294967295u, 4294967295u, 2147483647, 86399999u}; Msg d = decode(encode(m)); (long long)d.qty` expects `4294967295`

Checked by `cpp/build_md.py`: the solution passes all 12 tests and the starter fails 12 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-pool: l15-no-allocation: a pool of slots

Where: `l15-no-allocation`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 10 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `prelude`:

```cpp
#include <cstdlib>
#include <new>
static int g_allocs = 0;   // counts every call to operator new
static void* volatile g_last = nullptr;   // the last block, kept so the call stays visible
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); g_last = p; return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// A pool of `slots` fixed slots, numbered 0 .. slots-1.
// allocate() returns a free slot, or -1 if none is free. release(s) makes slot s free again.
// The most recently released slot is the next one allocated. No call may use the heap after the constructor.
class Pool {
public:
    explicit Pool(int slots) : slots_(slots) {}
    int allocate() { return next_++; }          // never reuses a slot
    void release(int slot) { (void)slot; }
    int in_use() const { return next_; }
private:
    int slots_;
    int next_ = 0;
};
```

Reference solution:

```cpp
#include <vector>

class Pool {
public:
    explicit Pool(int slots) : next_free_(slots, -1), in_use_(0) {
        for (int s = 0; s + 1 < slots; ++s) next_free_[s] = s + 1;   // slot s points at slot s+1
        head_ = slots > 0 ? 0 : -1;
    }
    int allocate() {
        if (head_ < 0) return -1;
        int slot = head_;
        head_ = next_free_[slot];
        ++in_use_;
        return slot;
    }
    void release(int slot) {
        next_free_[slot] = head_;
        head_ = slot;
        --in_use_;
    }
    int in_use() const { return in_use_; }
private:
    std::vector<int> next_free_;   // the free list, stored inside the slots' own indices
    int head_;
    int in_use_;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `Pool p(3); p.allocate()` expects `0`
- `Pool p(3); p.allocate(); p.allocate(); p.allocate()` expects `2`
- `Pool p(3); p.allocate(); p.allocate(); p.allocate(); p.allocate()` expects `-1`
- `Pool p(3); int a = p.allocate(); int b = p.allocate(); p.allocate(); p.release(b); p.allocate()` expects `1`
- `Pool p(3); int a = p.allocate(); int b = p.allocate(); p.release(a); p.release(b); p.allocate()` expects `1`
- `Pool p(3); int a = p.allocate(); int b = p.allocate(); p.release(a); p.release(b); p.allocate(); p.allocate()` expects `0`
- `Pool p(2); p.allocate(); p.allocate(); p.release(0); p.allocate(); p.in_use()` expects `2`
- `Pool p(2); p.allocate(); p.allocate(); p.release(0); p.release(1); p.in_use()` expects `0`
- `Pool p(0); p.allocate()` expects `-1`
- `Pool p(8); g_allocs = 0; for (int r = 0; r < 100; ++r) { int s = p.allocate(); p.release(s); } g_allocs` expects `0`

Checked by `cpp/build_md.py`: the solution passes all 10 tests and the starter fails 7 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-format-price: l15-no-allocation: format a price in place

Where: `l15-no-allocation`, a second `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 9 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `prelude`:

```cpp
#include <cstdlib>
#include <new>
static int g_allocs = 0;   // counts every call to operator new
static void* volatile g_last = nullptr;   // the last block, kept so the call stays visible
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); g_last = p; return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// Write a price given in pence as pounds and pence into out, for example 10275 -> "102.75", -25 -> "-0.25".
// Put a '\0' after the text and return its length (not counting the '\0'). out has room for 32 characters.
// The hot path may not use the heap.
int format_price(char* out, int pence) {
    std::vector<char> digits;                 // allocates
    bool negative = pence < 0;
    long long a = negative ? -(long long)pence : pence;
    (void)negative;
    do { digits.push_back(static_cast<char>('0' + a % 10)); a /= 10; } while (a > 0);
    int n = 0;      // TODO: the '-' sign, and pence below 10 need a leading '0'
    for (int i = static_cast<int>(digits.size()) - 1; i >= 0; --i) {
        out[n++] = digits[i];
        if (i == 2) out[n++] = '.';
    }
    out[n] = '\0';
    return n;
}
```

Reference solution:

```cpp
int format_price(char* out, int pence) {
    int n = 0;
    long long a = pence;
    if (a < 0) { out[n++] = '-'; a = -a; }
    long long pounds = a / 100;
    int pennies = static_cast<int>(a % 100);
    char tmp[24];
    int t = 0;
    do { tmp[t++] = static_cast<char>('0' + pounds % 10); pounds /= 10; } while (pounds > 0);
    while (t > 0) out[n++] = tmp[--t];
    out[n++] = '.';
    out[n++] = static_cast<char>('0' + pennies / 10);
    out[n++] = static_cast<char>('0' + pennies % 10);
    out[n] = '\0';
    return n;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `char buf[32]; int n = format_price(buf, 10275); std::string(buf, n)` expects `"102.75"`
- `char buf[32]; int n = format_price(buf, 5); std::string(buf, n)` expects `"0.05"`
- `char buf[32]; int n = format_price(buf, 0); std::string(buf, n)` expects `"0.00"`
- `char buf[32]; int n = format_price(buf, -25); std::string(buf, n)` expects `"-0.25"`
- `char buf[32]; int n = format_price(buf, 100000); std::string(buf, n)` expects `"1000.00"`
- `char buf[32]; int n = format_price(buf, 1999); std::string(buf, n)` expects `"19.99"`
- `char buf[32]; int n = format_price(buf, -5); std::string(buf, n)` expects `"-0.05"`
- `char buf[32]; int n = format_price(buf, 99); std::string(buf, n)` expects `"0.99"`
- `char buf[32]; g_allocs = 0; format_price(buf, 10275); format_price(buf, -25); g_allocs` expects `0`

Checked by `cpp/build_md.py`: the solution passes all 9 tests and the starter fails 6 of them: five on the text (no sign, no padding) whatever the optimiser does, and the `g_allocs` test only if the compiler keeps the `std::vector` allocation, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-ring: l16-ring-buffer: a single-producer ring

Where: `l16-ring-buffer`, a `code` screen, difficulty 4. Widget `code`, `language: "cpp"`, 10 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `postlude`:

```cpp

// hidden driver: ops > 0 push that value (1 if accepted, 0 if full); ops == 0 pop (the value, or -1 if empty)
std::vector<int> drive(int capacity, const std::vector<int>& ops) {
    Ring r(capacity);
    std::vector<int> out;
    for (int op : ops) {
        if (op > 0) out.push_back(r.push(op) ? 1 : 0);
        else { int v = 0; out.push_back(r.pop(v) ? v : -1); }
    }
    return out;
}
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <cstddef>
#include <vector>

// A fixed-size ring of ints. capacity is a power of two. push returns false when full,
// pop returns false when empty. head_ counts pops and tail_ counts pushes: both only ever grow.
// Keep head_ and tail_ at least 64 bytes apart so two cores do not share a cache line.
struct Ring {
    explicit Ring(std::size_t capacity) : buf_(capacity), mask_(capacity - 1) {}
    bool push(int v) {
        if (tail_ - head_ >= buf_.size() - 1) return false;   // one slot too early
        buf_[tail_ & mask_] = v;
        ++tail_;
        return true;
    }
    bool pop(int& out) {
        if (head_ == tail_) return false;
        out = buf_[head_ & mask_];
        ++head_;
        return true;
    }
    std::vector<int> buf_;
    std::size_t mask_;
    std::size_t head_ = 0;
    std::size_t tail_ = 0;
};
```

Reference solution:

```cpp
#include <cstddef>
#include <vector>

struct Ring {
    explicit Ring(std::size_t capacity) : buf_(capacity), mask_(capacity - 1) {}
    bool push(int v) {
        if (tail_ - head_ == buf_.size()) return false;     // full
        buf_[tail_ & mask_] = v;
        ++tail_;
        return true;
    }
    bool pop(int& out) {
        if (head_ == tail_) return false;                   // empty
        out = buf_[head_ & mask_];
        ++head_;
        return true;
    }
    std::vector<int> buf_;
    std::size_t mask_;
    alignas(64) std::size_t head_ = 0;
    alignas(64) std::size_t tail_ = 0;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `drive(4, {1, 2, 3, 4, 5, 0, 0, 0, 0, 0})` expects `[1, 1, 1, 1, 0, 1, 2, 3, 4, -1]`
- `drive(4, {1, 2, 3, 0, 0, 4, 5, 6, 0, 0, 0, 0})` expects `[1, 1, 1, 1, 2, 1, 1, 1, 3, 4, 5, 6]`
- `drive(2, {0})` expects `[-1]`
- `drive(1, {7, 8, 0, 9, 0, 0})` expects `[1, 0, 7, 1, 9, -1]`
- `drive(8, {})` expects `[]`
- `drive(4, {1, 2, 3, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 0, 0, 0, 0})` expects `[1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 6, 7, 8, -1]`
- `drive(2, {1, 2, 3, 0, 3, 0, 0, 0})` expects `[1, 1, 0, 1, 1, 2, 3, -1]`
- `drive(4, {1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 0})` expects `[1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7, 1, 8, 1, 9, 1, 10]`
- `drive(4, {1, 2, 3, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 0, 11, 0, 12, 0, 13, 0, 14, 0, 15, 0, 16, 0, 17, 0, 18, 0, 19, 0, 20, 0, 21, 0, 22, 0, 23, 0, 0, 0, 0, 0})` expects `[1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7, 1, 8, 1, 9, 1, 10, 1, 11, 1, 12, 1, 13, 1, 14, 1, 15, 1, 16, 1, 17, 1, 18, 1, 19, 1, 20, 21, 22, 23, -1]`
- `Ring r(8); (long long)((const char*)&r.tail_ - (const char*)&r.head_) >= 64` expects `true`

Checked by `cpp/build_md.py`: the solution passes all 10 tests and the starter fails 7 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-percentile: l17-measuring-latency: percentile and mean

Where: `l17-measuring-latency`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 13 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// Nearest-rank percentile: sort the samples; the p-th percentile is the value at rank ceil(p * n / 100),
// counting from 1 (rank 1 at p = 0). Subtract 1e-9 before ceil so 99 * 1000 / 100 does not round up.
double percentile(std::vector<double> samples, double p) {
    return samples.empty() ? 0.0 : samples.back();     // the last sample, unsorted
}

double mean(const std::vector<double>& samples) {
    double total = 0.0;
    for (double s : samples) total += s;
    return samples.empty() ? 0.0 : total / samples.size();
}
```

Reference solution:

```cpp
#include <algorithm>
#include <cmath>
#include <vector>

double percentile(std::vector<double> samples, double p) {
    if (samples.empty()) return 0.0;
    std::sort(samples.begin(), samples.end());
    double n = static_cast<double>(samples.size());
    long long rank = static_cast<long long>(std::ceil(p * n / 100.0 - 1e-9));
    if (rank < 1) rank = 1;
    if (rank > static_cast<long long>(samples.size())) rank = static_cast<long long>(samples.size());
    return samples[rank - 1];
}

double mean(const std::vector<double>& samples) {
    double total = 0.0;
    for (double s : samples) total += s;
    return samples.empty() ? 0.0 : total / samples.size();
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0); percentile(v, 50)` expects `10.0`
- `std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0); percentile(v, 99)` expects `10.0`
- `std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0); percentile(v, 99.9)` expects `1000.0`
- `std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0); percentile(v, 100)` expects `1000.0`
- `std::vector<double> v(989, 10.0); v.insert(v.end(), 11, 1000.0); percentile(v, 99)` expects `1000.0`
- `std::vector<double> v(999, 10.0); v.push_back(1000.0); percentile(v, 99.9)` expects `10.0`
- `std::vector<double> v(999, 10.0); v.push_back(1000.0); percentile(v, 100)` expects `1000.0`
- `std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0}; percentile(v, 20)` expects `1.0`
- `std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0}; percentile(v, 50)` expects `3.0`
- `std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0}; percentile(v, 80)` expects `4.0`
- `std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0}; percentile(v, 100)` expects `5.0`
- `std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0}; percentile(v, 0)` expects `1.0`
- `std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0); mean(v)` expects `19.9`

Checked by `cpp/build_md.py`: the solution passes all 13 tests and the starter fails 7 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-latency-hist: homework-4: a fixed-bucket latency histogram

Where: `homework-4`, the homework `code` item, difficulty 4. Widget `code`, `language: "cpp"`, 12 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `prelude`:

```cpp
#include <cstdlib>
#include <new>
static int g_allocs = 0;   // counts every call to operator new
static void* volatile g_last = nullptr;   // the last block, kept so the call stays visible
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); g_last = p; return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <array>

// Buckets by powers of two: a sample of ns nanoseconds goes in bucket floor(log2(max(ns, 1))), 0..39.
// percentile_upper(p) finds the bucket holding the nearest-rank p-th percentile sample
// (rank ceil(p * n / 100 - 1e-9), at least 1) and returns that bucket's upper bound, 2^(bucket + 1).
// record() must not use the heap.
class LatencyHist {
public:
    void record(long long ns) { ++total_; (void)ns; }
    long long percentile_upper(double p) const { (void)p; return 0; }
    int count() const { return total_; }
private:
    std::array<int, 40> buckets_{};
    int total_ = 0;
};
```

Reference solution:

```cpp
#include <array>
#include <cmath>

class LatencyHist {
public:
    void record(long long ns) {
        int b = 0;
        long long v = ns < 1 ? 1 : ns;
        while (v > 1) { v >>= 1; ++b; }
        if (b > 39) b = 39;
        ++buckets_[b];
        ++total_;
    }
    long long percentile_upper(double p) const {
        if (total_ == 0) return 0;
        long long rank = static_cast<long long>(std::ceil(p * total_ / 100.0 - 1e-9));
        if (rank < 1) rank = 1;
        long long seen = 0;
        for (int b = 0; b < 40; ++b) {
            seen += buckets_[b];
            if (seen >= rank) return 1LL << (b + 1);
        }
        return 1LL << 40;
    }
    int count() const { return total_; }
private:
    std::array<int, 40> buckets_{};
    int total_ = 0;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `LatencyHist h; for (int i = 0; i < 990; ++i) h.record(10); for (int i = 0; i < 10; ++i) h.record(1000); h.percentile_upper(50)` expects `16`
- `LatencyHist h; for (int i = 0; i < 990; ++i) h.record(10); for (int i = 0; i < 10; ++i) h.record(1000); h.percentile_upper(99)` expects `16`
- `LatencyHist h; for (int i = 0; i < 990; ++i) h.record(10); for (int i = 0; i < 10; ++i) h.record(1000); h.percentile_upper(99.9)` expects `1024`
- `LatencyHist h; for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); for (int i = 0; i < 1; ++i) h.record(4); for (int i = 0; i < 1; ++i) h.record(5); for (int i = 0; i < 1; ++i) h.record(6); for (int i = 0; i < 1; ++i) h.record(7); for (int i = 0; i < 1; ++i) h.record(8); for (int i = 0; i < 1; ++i) h.record(9); for (int i = 0; i < 1; ++i) h.record(10); h.percentile_upper(50)` expects `8`
- `LatencyHist h; for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); for (int i = 0; i < 1; ++i) h.record(4); for (int i = 0; i < 1; ++i) h.record(5); for (int i = 0; i < 1; ++i) h.record(6); for (int i = 0; i < 1; ++i) h.record(7); for (int i = 0; i < 1; ++i) h.record(8); for (int i = 0; i < 1; ++i) h.record(9); for (int i = 0; i < 1; ++i) h.record(10); h.percentile_upper(90)` expects `16`
- `LatencyHist h; for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); for (int i = 0; i < 1; ++i) h.record(4); for (int i = 0; i < 1; ++i) h.record(5); for (int i = 0; i < 1; ++i) h.record(6); for (int i = 0; i < 1; ++i) h.record(7); for (int i = 0; i < 1; ++i) h.record(8); for (int i = 0; i < 1; ++i) h.record(9); for (int i = 0; i < 1; ++i) h.record(10); h.percentile_upper(100)` expects `16`
- `LatencyHist h; for (int i = 0; i < 1; ++i) h.record(0); for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); h.percentile_upper(50)` expects `2`
- `LatencyHist h; for (int i = 0; i < 1; ++i) h.record(0); for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); h.percentile_upper(100)` expects `4`
- `LatencyHist h; for (int i = 0; i < 5; ++i) h.record(1000000); for (int i = 0; i < 95; ++i) h.record(100); h.percentile_upper(90)` expects `128`
- `LatencyHist h; for (int i = 0; i < 5; ++i) h.record(1000000); for (int i = 0; i < 95; ++i) h.record(100); h.percentile_upper(99)` expects `1048576`
- `LatencyHist h; h.record(1000); h.record(2000); h.count()` expects `2`
- `LatencyHist h; g_allocs = 0; for (int i = 0; i < 1000; ++i) h.record(i * 37); g_allocs` expects `0`

Checked by `cpp/build_md.py`: the solution passes all 12 tests and the starter fails 10 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-handler: l18-feed-handler: a book with no allocation

Where: `l18-feed-handler`, the capstone `code` screen, difficulty 4 (the lesson's last task screen). Widget `code`, `language: "cpp"`, 14 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `prelude`:

```cpp
#include <cstdlib>
#include <new>
static int g_allocs = 0;   // counts every call to operator new
static void* volatile g_last = nullptr;   // the last block, kept so the call stays visible
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); g_last = p; return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

#include <vector>
std::vector<int> frame(char type, char side, unsigned seq, unsigned id, unsigned qty, int price) {
    std::vector<int> b(24, 0);
    auto put = [&](int at, unsigned v, int n) { for (int k = 0; k < n; ++k) b[at + k] = (v >> (8 * (n - 1 - k))) & 0xFF; };
    b[0] = type; b[1] = side; put(2, 7, 2); put(4, seq, 4); put(8, id, 4); put(12, qty, 4); put(16, static_cast<unsigned>(price), 4); put(20, 36000000u + seq, 4);
    return b;
}
std::vector<int> cat(std::vector<std::vector<int>> parts) {
    std::vector<int> all;
    for (auto& p : parts) all.insert(all.end(), p.begin(), p.end());
    return all;
}
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <map>
#include <vector>

// Frames are 24 bytes (the l14 layout, big-endian). One instrument, prices 9900..10100 pence, order ids below 1024.
// 'A' adds an order (side B or S, price, qty), 'X' cancels the rest of order id, 'T' trades qty against order id.
// A frame with seq < the next expected is stale: ignore it. A larger seq adds (seq - expected) to gaps().
// Partial frames wait for their remaining bytes. After construction, feed() may not use the heap.
class Handler {
public:
    void feed(const std::vector<int>& bytes) {
        for (std::size_t at = 0; at + 24 <= bytes.size(); at += 24) {
            int type = bytes[at];
            unsigned id = (bytes[at + 8] << 24) | (bytes[at + 9] << 16) | (bytes[at + 10] << 8) | bytes[at + 11];
            unsigned qty = (bytes[at + 12] << 24) | (bytes[at + 13] << 16) | (bytes[at + 14] << 8) | bytes[at + 15];
            int price = (bytes[at + 16] << 24) | (bytes[at + 17] << 16) | (bytes[at + 18] << 8) | bytes[at + 19];
            bool bid = bytes[at + 1] == 'B';
            if (type == 'A') { (bid ? bids_ : asks_)[price] += qty; ++applied_; }
        }
    }
    int best_bid() const { return bids_.empty() ? 0 : bids_.rbegin()->first; }
    int best_ask() const { return asks_.empty() ? 0 : asks_.begin()->first; }
    int bid_qty(int price) const { auto it = bids_.find(price); return it == bids_.end() ? 0 : static_cast<int>(it->second); }
    int ask_qty(int price) const { auto it = asks_.find(price); return it == asks_.end() ? 0 : static_cast<int>(it->second); }
    int gaps() const { return 0; }
    int applied() const { return applied_; }
private:
    std::map<int, unsigned> bids_, asks_;
    int applied_ = 0;
};
```

Reference solution:

```cpp
#include <array>
#include <cstdint>
#include <vector>

class Handler {
public:
    void feed(const std::vector<int>& bytes) {
        for (int b : bytes) {
            pending_[pending_len_++] = static_cast<std::uint8_t>(b);
            if (pending_len_ == kFrame) { frame(); pending_len_ = 0; }
        }
    }
    int best_bid() const {
        for (int i = kLevels - 1; i >= 0; --i) if (qty_[0][i] > 0) return kMinPrice + i;
        return 0;
    }
    int best_ask() const {
        for (int i = 0; i < kLevels; ++i) if (qty_[1][i] > 0) return kMinPrice + i;
        return 0;
    }
    int bid_qty(int price) const { return level(0, price); }
    int ask_qty(int price) const { return level(1, price); }
    int gaps() const { return gaps_; }
    int applied() const { return applied_; }
private:
    static constexpr int kFrame = 24, kMinPrice = 9900, kLevels = 201, kOrders = 1024;
    struct Order { int side = 0; int price = 0; unsigned qty = 0; bool live = false; };

    unsigned u32(int at) const {
        return (unsigned(pending_[at]) << 24) | (unsigned(pending_[at + 1]) << 16) | (unsigned(pending_[at + 2]) << 8) | unsigned(pending_[at + 3]);
    }
    int level(int side, int price) const {
        int i = price - kMinPrice;
        return (i >= 0 && i < kLevels) ? static_cast<int>(qty_[side][i]) : 0;
    }
    void frame() {
        unsigned seq = u32(4);
        if (seq < expected_) return;                 // stale or duplicate
        if (seq > expected_) gaps_ += static_cast<int>(seq - expected_);
        expected_ = seq + 1;
        ++applied_;
        int type = pending_[0];
        int side = pending_[1] == 'B' ? 0 : (pending_[1] == 'S' ? 1 : -1);
        unsigned id = u32(8), qty = u32(12);
        int price = static_cast<int>(u32(16));
        if (id >= kOrders) return;
        Order& o = orders_[id];
        if (type == 'A') {
            int i = price - kMinPrice;
            if (side < 0 || i < 0 || i >= kLevels || o.live) return;
            o = Order{side, price, qty, true};
            qty_[side][i] += qty;
        } else if (type == 'X') {
            if (!o.live) return;
            qty_[o.side][o.price - kMinPrice] -= o.qty;
            o.live = false;
        } else if (type == 'T') {
            if (!o.live) return;
            unsigned done = qty < o.qty ? qty : o.qty;
            o.qty -= done;
            qty_[o.side][o.price - kMinPrice] -= done;
            if (o.qty == 0) o.live = false;
        }
    }

    std::array<std::array<unsigned, kLevels>, 2> qty_{};
    std::array<Order, kOrders> orders_{};
    std::array<std::uint8_t, kFrame> pending_{};
    int pending_len_ = 0;
    unsigned expected_ = 1;
    int gaps_ = 0, applied_ = 0;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); h.feed(s); h.best_bid()` expects `10005`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); h.feed(s); h.best_ask()` expects `10010`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005), frame('X', 'B', 4, 3, 0, 0)}); h.feed(s); h.best_bid()` expects `10000`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005), frame('T', 'B', 4, 1, 30, 10000)}); h.feed(s); h.bid_qty(10000)` expects `70`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('T', 'B', 2, 1, 100, 10000)}); h.feed(s); h.best_bid()` expects `0`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 10, 10000), frame('A', 'B', 2, 2, 10, 10001), frame('A', 'B', 5, 3, 10, 10002)}); h.feed(s); h.gaps()` expects `2`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 10, 10000), frame('A', 'B', 2, 2, 10, 10001), frame('A', 'B', 2, 3, 99, 10050)}); h.feed(s); h.applied()` expects `2`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 10, 10000), frame('A', 'B', 2, 2, 10, 10001), frame('A', 'B', 4, 3, 10, 10002), frame('A', 'B', 3, 4, 500, 10050)}); h.feed(s); h.best_bid()` expects `10002`
- `Handler h; auto s = cat({frame('A', 'B', 3, 1, 10, 10000)}); h.feed(s); h.gaps()` expects `2`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); h.feed(std::vector<int>(s.begin(), s.begin() + 30)); h.feed(std::vector<int>(s.begin() + 30, s.end())); h.best_bid()` expects `10005`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005), frame('T', 'S', 4, 2, 50, 10010)}); for (int b : s) h.feed(std::vector<int>{b}); h.best_ask()` expects `0`
- `Handler h; auto s = cat({frame('X', 'B', 1, 9, 0, 0), frame('A', 'B', 2, 4000, 10, 10000), frame('A', 'B', 3, 5, 10, 12000), frame('A', 'B', 4, 6, 10, 9999)}); h.feed(s); h.best_bid()` expects `9999`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); g_allocs = 0; h.feed(s); g_allocs` expects `0`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'B', 2, 1, 70, 10003)}); h.feed(s); h.bid_qty(10003)` expects `0`

Checked by `cpp/build_md.py`: the solution passes all 14 tests and the starter fails 11 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### D-lru: drill sy-lru-cache: least recently used cache

Where: `drill sy-lru-cache (E8)`, a drill, pattern `cache`, difficulty 3, pace 1500 seconds. Widget `code`, `language: "cpp"`, 7 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `postlude`:

```cpp
#include <cstdio>
#include <string>
#include <vector>

// hidden driver: "p k v" puts, "g k" gets; the result lists every get (value or -1)
std::vector<int> drive(int capacity, const std::vector<std::string>& ops) {
    LRU cache(capacity);
    std::vector<int> out;
    for (const auto& op : ops) {
        int k = 0, v = 0;
        if (op[0] == 'p') { std::sscanf(op.c_str(), "p %d %d", &k, &v); cache.put(k, v); }
        else { std::sscanf(op.c_str(), "g %d", &k); out.push_back(cache.get(k)); }
    }
    return out;
}
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <list>
#include <unordered_map>

// A cache of at most `capacity` keys. get(k) returns the value or -1, and counts as a use.
// put(k, v) stores or updates k (also a use); when over capacity, drop the least recently used key.
// Both calls take constant time on average.
class LRU {
public:
    explicit LRU(int capacity) : capacity_(capacity) {}
    int get(int key) {
        auto it = values_.find(key);
        return it == values_.end() ? -1 : it->second;      // does not count as a use yet
    }
    void put(int key, int value) {
        values_[key] = value;
        if (static_cast<int>(values_.size()) > capacity_) values_.erase(values_.begin());   // not the oldest
    }
private:
    int capacity_;
    std::unordered_map<int, int> values_;
};
```

Reference solution:

```cpp
#include <list>
#include <unordered_map>

class LRU {
public:
    explicit LRU(int capacity) : capacity_(capacity) {}
    int get(int key) {
        auto it = where_.find(key);
        if (it == where_.end()) return -1;
        order_.splice(order_.begin(), order_, it->second);   // move to the front: most recent
        return it->second->second;
    }
    void put(int key, int value) {
        if (capacity_ <= 0) return;
        auto it = where_.find(key);
        if (it != where_.end()) {
            it->second->second = value;
            order_.splice(order_.begin(), order_, it->second);
            return;
        }
        order_.emplace_front(key, value);
        where_[key] = order_.begin();
        if (static_cast<int>(order_.size()) > capacity_) {
            where_.erase(order_.back().first);
            order_.pop_back();
        }
    }
private:
    int capacity_;
    std::list<std::pair<int, int>> order_;                       // front = most recent
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> where_;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `drive(2, {"p 1 10", "p 2 20", "g 1", "p 3 30", "g 2", "g 3", "g 1"})` expects `[10, -1, 30, 10]`
- `drive(1, {"p 1 5", "p 2 6", "g 1", "g 2"})` expects `[-1, 6]`
- `drive(2, {"p 1 1", "p 2 2", "p 1 9", "p 3 3", "g 1", "g 2", "g 3"})` expects `[9, -1, 3]`
- `drive(3, {"g 7"})` expects `[-1]`
- `drive(2, {"p 1 1", "p 2 2", "g 1", "g 1", "p 3 3", "g 2", "g 1"})` expects `[1, 1, -1, 1]`
- `drive(0, {"p 1 1", "g 1"})` expects `[-1]`
- `drive(3, {"p 1 1", "p 2 2", "p 3 3", "p 4 4", "g 1", "g 2", "g 3", "g 4", "p 5 5", "g 2", "g 3", "g 4", "g 5"})` expects `[-1, 2, 3, 4, -1, 3, 4, 5]`

Checked by `cpp/build_md.py`: the solution passes all 7 tests and the starter fails 5 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### D-token-bucket: drill sy-token-bucket: a rate limiter

Where: `drill sy-token-bucket (E8)`, a drill, pattern `rate-limiter`, difficulty 2, pace 900 seconds. Widget `code`, `language: "cpp"`, 7 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `postlude`:

```cpp
#include <vector>

std::vector<int> drive(long long rate, long long burst, const std::vector<long long>& times) {
    TokenBucket b(rate, burst);
    std::vector<int> out;
    for (long long t : times) out.push_back(b.allow(t) ? 1 : 0);
    return out;
}
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
// rate tokens a second refill continuously, up to burst tokens. The bucket starts full.
// allow(now_ns) is called with non-decreasing times in nanoseconds. It returns true and spends one token
// if a whole token is available, else false. Use integers only: no floating point.
class TokenBucket {
public:
    TokenBucket(long long rate, long long burst) : rate_(rate), burst_(burst), tokens_(burst) {}
    bool allow(long long now_ns) {
        (void)now_ns;
        if (tokens_ < 1) return false;     // never refills
        --tokens_;
        return true;
    }
private:
    long long rate_, burst_, tokens_;
};
```

Reference solution:

```cpp
// Tokens are counted in billionths of a token, so a nanosecond at `rate` per second adds exactly `rate` units.
class TokenBucket {
public:
    TokenBucket(long long rate, long long burst)
        : rate_(rate), cap_(burst * kUnit), units_(burst * kUnit) {}
    bool allow(long long now_ns) {
        units_ += (now_ns - last_) * rate_;
        if (units_ > cap_) units_ = cap_;
        last_ = now_ns;
        if (units_ < kUnit) return false;
        units_ -= kUnit;
        return true;
    }
private:
    static constexpr long long kUnit = 1000000000LL;
    long long rate_, cap_, units_;
    long long last_ = 0;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `drive(1000, 3, std::vector<long long>{0, 0, 0, 0})` expects `[1, 1, 1, 0]`
- `drive(1000, 3, std::vector<long long>{0, 0, 0, 0, 1000000, 1000000})` expects `[1, 1, 1, 0, 1, 0]`
- `drive(1000, 1, std::vector<long long>{0, 500000, 1000000, 1500000, 2000000})` expects `[1, 0, 1, 0, 1]`
- `drive(2, 2, std::vector<long long>{0, 0, 0, 250000000, 500000000, 1000000000})` expects `[1, 1, 0, 0, 1, 1]`
- `drive(10, 5, std::vector<long long>{0, 1000000000, 1000000001})` expects `[1, 1, 1]`
- `drive(1000000000, 2, std::vector<long long>{0, 0, 0, 1, 2, 3})` expects `[1, 1, 0, 1, 1, 1]`
- `drive(100, 3, std::vector<long long>{1000000000000, 1000000000000, 1000000000000, 1000000000000})` expects `[1, 1, 1, 0]`

Checked by `cpp/build_md.py`: the solution passes all 7 tests and the starter fails 4 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### D-bits: drill sy-bits: powers of two and byte order

Where: `drill sy-bits (E8)`, a drill, pattern `bits`, difficulty 2, pace 600 seconds. Widget `code`, `language: "cpp"`, 15 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
// next_pow2(x): the smallest power of two >= x (1 for x = 0 or 1). x is at most 2^30.
// is_pow2(x): true for 1, 2, 4, 8, ... and false for 0.
// popcount(x): the number of 1 bits. bswap32(x): reverse the four bytes of x.
unsigned next_pow2(unsigned x) { return x; }
bool is_pow2(unsigned x) { return x % 2 == 0; }
int popcount(unsigned x) { return static_cast<int>(x); }
unsigned bswap32(unsigned x) { return x; }
```

Reference solution:

```cpp
unsigned next_pow2(unsigned x) {
    unsigned p = 1;
    while (p < x) p <<= 1;
    return p;
}
bool is_pow2(unsigned x) { return x != 0 && (x & (x - 1)) == 0; }
int popcount(unsigned x) {
    int n = 0;
    while (x) { x &= x - 1; ++n; }      // clears the lowest set bit
    return n;
}
unsigned bswap32(unsigned x) {
    return (x >> 24) | ((x >> 8) & 0x0000FF00u) | ((x << 8) & 0x00FF0000u) | (x << 24);
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `(long long)next_pow2(0u)` expects `1`
- `(long long)next_pow2(5u)` expects `8`
- `(long long)next_pow2(8u)` expects `8`
- `(long long)next_pow2(1000u)` expects `1024`
- `(long long)next_pow2(1073741824u)` expects `1073741824`
- `is_pow2(0u)` expects `false`
- `is_pow2(6u)` expects `false`
- `is_pow2(64u)` expects `true`
- `is_pow2(4294967295u)` expects `false`
- `popcount(0u)` expects `0`
- `popcount(4294967295u)` expects `32`
- `popcount(2147483648u)` expects `1`
- `(long long)bswap32(1u)` expects `16777216`
- `(long long)bswap32(305419896u)` expects `2018915346`
- `(long long)bswap32(65280u)` expects `16711680`

Checked by `cpp/build_md.py`: the solution passes all 15 tests and the starter fails 10 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.
