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

int main(){ int fail=0;
  { LatencyHist h; for (int i = 0; i < 990; ++i) h.record(10); for (int i = 0; i < 10; ++i) h.record(1000);  auto __r = (h.percentile_upper(50)); auto __e = (16); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 0\n"); } }
  { LatencyHist h; for (int i = 0; i < 990; ++i) h.record(10); for (int i = 0; i < 10; ++i) h.record(1000);  auto __r = (h.percentile_upper(99)); auto __e = (16); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 1\n"); } }
  { LatencyHist h; for (int i = 0; i < 990; ++i) h.record(10); for (int i = 0; i < 10; ++i) h.record(1000);  auto __r = (h.percentile_upper(99.9)); auto __e = (1024); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 2\n"); } }
  { LatencyHist h; for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); for (int i = 0; i < 1; ++i) h.record(4); for (int i = 0; i < 1; ++i) h.record(5); for (int i = 0; i < 1; ++i) h.record(6); for (int i = 0; i < 1; ++i) h.record(7); for (int i = 0; i < 1; ++i) h.record(8); for (int i = 0; i < 1; ++i) h.record(9); for (int i = 0; i < 1; ++i) h.record(10);  auto __r = (h.percentile_upper(50)); auto __e = (8); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 3\n"); } }
  { LatencyHist h; for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); for (int i = 0; i < 1; ++i) h.record(4); for (int i = 0; i < 1; ++i) h.record(5); for (int i = 0; i < 1; ++i) h.record(6); for (int i = 0; i < 1; ++i) h.record(7); for (int i = 0; i < 1; ++i) h.record(8); for (int i = 0; i < 1; ++i) h.record(9); for (int i = 0; i < 1; ++i) h.record(10);  auto __r = (h.percentile_upper(90)); auto __e = (16); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 4\n"); } }
  { LatencyHist h; for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); for (int i = 0; i < 1; ++i) h.record(4); for (int i = 0; i < 1; ++i) h.record(5); for (int i = 0; i < 1; ++i) h.record(6); for (int i = 0; i < 1; ++i) h.record(7); for (int i = 0; i < 1; ++i) h.record(8); for (int i = 0; i < 1; ++i) h.record(9); for (int i = 0; i < 1; ++i) h.record(10);  auto __r = (h.percentile_upper(100)); auto __e = (16); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 5\n"); } }
  { LatencyHist h; for (int i = 0; i < 1; ++i) h.record(0); for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3);  auto __r = (h.percentile_upper(50)); auto __e = (2); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 6\n"); } }
  { LatencyHist h; for (int i = 0; i < 1; ++i) h.record(0); for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3);  auto __r = (h.percentile_upper(100)); auto __e = (4); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 7\n"); } }
  { LatencyHist h; for (int i = 0; i < 5; ++i) h.record(1000000); for (int i = 0; i < 95; ++i) h.record(100);  auto __r = (h.percentile_upper(90)); auto __e = (128); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 8\n"); } }
  { LatencyHist h; for (int i = 0; i < 5; ++i) h.record(1000000); for (int i = 0; i < 95; ++i) h.record(100);  auto __r = (h.percentile_upper(99)); auto __e = (1048576); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 9\n"); } }
  { LatencyHist h; h.record(1000); h.record(2000);  auto __r = (h.count()); auto __e = (2); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 10\n"); } }
  { LatencyHist h; reset_alloc_count(); for (int i = 0; i < 1000; ++i) h.record(i * 37);  auto __r = (alloc_count()); auto __e = (0); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 11\n"); } }
  std::printf("%d of %d failed\n", fail, 12); return fail?1:0; }
