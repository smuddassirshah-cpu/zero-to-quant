#include <vector>
#include <unordered_map>
#include <cstdio>
long long count_subarrays_divisible_by_k(std::vector<int> nums, int k) {
    std::unordered_map<int, long long> seen;
    seen[0] = 1;
    long long total = 0, count = 0;
    for (int x : nums) {
        total = ((total + x) % k + k) % k;
        count += seen[(int)total];
        ++seen[(int)total];
    }
    return count;
}
int main(){
  printf("%lld\n", count_subarrays_divisible_by_k({6,-1,8,3,-4,7},5));
  printf("%lld\n", count_subarrays_divisible_by_k({-2,-4,-6},5));
  printf("%lld\n", count_subarrays_divisible_by_k({-1,3,0},3));
  printf("%lld\n", count_subarrays_divisible_by_k(std::vector<int>(400000,3),1));
  std::vector<int> v; for (int i=0;i<200000;++i){v.push_back(1);v.push_back(-1);}
  printf("%lld\n", count_subarrays_divisible_by_k(v,2));
}
