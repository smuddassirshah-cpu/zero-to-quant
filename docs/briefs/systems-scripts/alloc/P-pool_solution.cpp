#include "alloc_check.hpp"

#include <cstdio>
#include <cmath>
#include <string>
#include <vector>
#include <cstdint>
#include <cstddef>
#include <algorithm>
#include <array>
#include <map>
#include <initializer_list>
#include <type_traits>
template<class A,class B> bool eqv(const A&a,const B&b){ if constexpr(std::is_floating_point<A>::value||std::is_floating_point<B>::value){ double x=(double)a,y=(double)b; return std::fabs(x-y)<=1e-9*std::max(std::fabs(x),std::fabs(y))+1e-12;} else return a==b; }

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

int main(){ int fail=0;
  { Pool p(3);  auto __r = (p.allocate()); auto __e = (0); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 0\n"); } }
  { Pool p(3); p.allocate(); p.allocate();  auto __r = (p.allocate()); auto __e = (2); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 1\n"); } }
  { Pool p(3); p.allocate(); p.allocate(); p.allocate();  auto __r = (p.allocate()); auto __e = (-1); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 2\n"); } }
  { Pool p(3); int a = p.allocate(); int b = p.allocate(); p.allocate(); p.release(b);  auto __r = (p.allocate()); auto __e = (1); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 3\n"); } }
  { Pool p(3); int a = p.allocate(); int b = p.allocate(); p.release(a); p.release(b);  auto __r = (p.allocate()); auto __e = (1); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 4\n"); } }
  { Pool p(3); int a = p.allocate(); int b = p.allocate(); p.release(a); p.release(b); p.allocate();  auto __r = (p.allocate()); auto __e = (0); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 5\n"); } }
  { Pool p(2); p.allocate(); p.allocate(); p.release(0); p.allocate();  auto __r = (p.in_use()); auto __e = (2); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 6\n"); } }
  { Pool p(2); p.allocate(); p.allocate(); p.release(0); p.release(1);  auto __r = (p.in_use()); auto __e = (0); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 7\n"); } }
  { Pool p(0);  auto __r = (p.allocate()); auto __e = (-1); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 8\n"); } }
  { Pool p(8); reset_alloc_count(); for (int r = 0; r < 100; ++r) { int s = p.allocate(); p.release(s); }  auto __r = (alloc_count()); auto __e = (0); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 9\n"); } }
  std::printf("%d of %d failed\n", fail, 10); return fail?1:0; }
