// l22: what the optimiser does with four undefined-behaviour snippets (no headers, so it builds for wasm32 without a sysroot).
// x86-64:  clang++ -std=c++17 -O1 -S -masm=intel -fno-asynchronous-unwind-tables -o - ub_asm.cpp | grep -v '^\s*\.'
// wasm32:  clang++ --target=wasm32-unknown-wasi -std=c++17 -O1 -S -o - ub_asm.cpp | grep -v '^\s*\.'
bool grows(int x) { return x + 1 > x; }                                      // true for every x the rules allow
bool wraps(int x) { return x + 1 < x; }                                      // the "overflow check" a learner writes
int first(int* p) { int v = *p; if (p == nullptr) return -1; return v; }     // the null test comes after the read
int sign(int x) { if (x > 0) return 1; }                                     // no return when x <= 0
