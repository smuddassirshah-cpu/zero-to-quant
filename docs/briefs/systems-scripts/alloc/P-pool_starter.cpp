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
