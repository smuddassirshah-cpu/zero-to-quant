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

int main(){ int fail=0;
  { char buf[32]; int n = format_price(buf, 10275);  auto __r = (std::string(buf, n)); auto __e = ("102.75"); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 0\n"); } }
  { char buf[32]; int n = format_price(buf, 5);  auto __r = (std::string(buf, n)); auto __e = ("0.05"); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 1\n"); } }
  { char buf[32]; int n = format_price(buf, 0);  auto __r = (std::string(buf, n)); auto __e = ("0.00"); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 2\n"); } }
  { char buf[32]; int n = format_price(buf, -25);  auto __r = (std::string(buf, n)); auto __e = ("-0.25"); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 3\n"); } }
  { char buf[32]; int n = format_price(buf, 100000);  auto __r = (std::string(buf, n)); auto __e = ("1000.00"); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 4\n"); } }
  { char buf[32]; int n = format_price(buf, 1999);  auto __r = (std::string(buf, n)); auto __e = ("19.99"); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 5\n"); } }
  { char buf[32]; int n = format_price(buf, -5);  auto __r = (std::string(buf, n)); auto __e = ("-0.05"); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 6\n"); } }
  { char buf[32]; int n = format_price(buf, 99);  auto __r = (std::string(buf, n)); auto __e = ("0.99"); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 7\n"); } }
  { char buf[32]; reset_alloc_count(); format_price(buf, 10275); format_price(buf, -25);  auto __r = (alloc_count()); auto __e = (0); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 8\n"); } }
  std::printf("%d of %d failed\n", fail, 9); return fail?1:0; }
