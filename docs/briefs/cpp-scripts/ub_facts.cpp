// l22: the sanitiser output and optimiser facts the lesson shows in `console` screens (the app has no sanitiser and runs no UB).
// Sanitiser lines:  g++ -std=c++17 -O0 -g -fsanitize=undefined -fno-sanitize-recover=all ub_facts.cpp -o ub && ./ub N      (N = 1 to 6)
// Optimiser facts:  clang++ -std=c++17 -O1 -S -masm=intel -fno-asynchronous-unwind-tables -o - -DASM ub_facts.cpp | grep -v '^\s*\.'
#include <climits>
#include <cstdio>
#include <cstdlib>
#include <vector>

#ifdef ASM
bool grows(int x) { return x + 1 > x; }                         // true for every x, unless x == INT_MAX
bool wraps(int x) { return x + 1 < x; }                         // the "overflow check" a learner writes
int first(int* p) { int v = *p; if (p == nullptr) return -1; return v; }   // the null test comes after the read
int sign(int x) { if (x > 0) return 1; }                        // no return when x <= 0
#else
int main(int argc, char** argv) {
    int which = argc > 1 ? std::atoi(argv[1]) : 0;
    volatile int big = INT_MAX, one = 1, zero = 0, thirty_two = 32;
    int a[3] = {1, 2, 3};
    volatile int idx = 3;
    int* np = nullptr;
    switch (which) {
        case 1: { int s = big + one; std::printf("%d\n", s); break; }            // signed overflow
        case 2: { int s = 1 << thirty_two; std::printf("%d\n", s); break; }      // shift by the width
        case 3: { std::printf("%d\n", a[idx]); break; }                          // one past the end of an array
        case 4: { int q = 10 / zero; std::printf("%d\n", q); break; }            // integer division by zero
        case 5: { volatile int* vp = np; std::printf("%d\n", *vp); break; }      // null read
        case 6: { volatile unsigned um = UINT_MAX; unsigned u = um + 1u; std::printf("%u\n", u); break; } // unsigned wraps to 0: defined, no report
    }
}
#endif
