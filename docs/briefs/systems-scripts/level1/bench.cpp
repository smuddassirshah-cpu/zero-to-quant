#include <algorithm>
#include <chrono>
#include <cstdio>
#include <vector>
#include <cstdint>
int main(int argc,char**argv){
  const int N=32768, REP=20000;
  std::vector<int> v(N); uint32_t x=12345; for(int i=0;i<N;i++){x=x*1103515245u+12345u; v[i]=(x>>16)&255;}
  auto run=[&](const char*name, const std::vector<int>&a){
    for(int variant=0;variant<2;variant++){
      long long sum=0; auto t0=std::chrono::steady_clock::now();
      for(int r=0;r<REP;r++){ if(variant==0){ for(int i=0;i<N;i++){ if(a[i]>=128) sum+=a[i]; } } else { for(int i=0;i<N;i++){ int m=-(a[i]>=128); sum+=a[i]&m; } } asm volatile(""::"r"(sum):"memory"); }
      double ms=std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-t0).count();
      std::printf("%s %s sum=%lld %.1f ms  %.3f ns/elem\n",name,variant?"mask":"branch",sum,ms,ms*1e6/((double)N*REP));
    }};
  run("unsorted",v); std::vector<int> s=v; std::sort(s.begin(),s.end()); run("sorted  ",s);
}
