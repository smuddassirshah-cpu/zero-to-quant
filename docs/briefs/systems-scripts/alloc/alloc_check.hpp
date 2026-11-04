// Native stand-in for the harness flag allocCheck: true (C-alloc-check).
// Rule: every call to a global operator new / new[] (any overload) anywhere in the program increments one counter,
// including the test harness's own allocations. reset_alloc_count() sets it to 0. alloc_count() returns it.
// The tests therefore call reset_alloc_count() after their setup and read alloc_count() last.
#pragma once
#include <cstdlib>
#include <cstddef>
#include <new>
namespace zq { inline volatile int g_alloc_n = 0; inline void* volatile g_alloc_last = nullptr; }
inline void reset_alloc_count() { zq::g_alloc_n = 0; }
inline int alloc_count() { return zq::g_alloc_n; }
inline void* zq_alloc(std::size_t n) { zq::g_alloc_n = zq::g_alloc_n + 1; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); zq::g_alloc_last = p; return p; }
void* operator new(std::size_t n) { return zq_alloc(n); }
void* operator new[](std::size_t n) { return zq_alloc(n); }
void* operator new(std::size_t n, const std::nothrow_t&) noexcept { return zq_alloc(n); }
void* operator new[](std::size_t n, const std::nothrow_t&) noexcept { return zq_alloc(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
