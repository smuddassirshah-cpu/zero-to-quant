#include <vector>
#include <unordered_map>
#include <algorithm>
#include <cstdio>
int longest_zero_sum_subarray(std::vector<int> nums) {
    std::unordered_map<long long, int> first;
    first[0] = -1;
    long long total = 0;
    int best = 0;
    for (int i = 0; i < (int)nums.size(); ++i) {
        total += nums[i];
        auto it = first.find(total);
        if (it != first.end()) best = std::max(best, i - it->second);
        else first[total] = i;
    }
    return best;
}
int main(){
  printf("%d %d %d\n", longest_zero_sum_subarray({5,-2,-3,8,1}), longest_zero_sum_subarray({}), longest_zero_sum_subarray({3,1,-4,2,2,-4,9}));
  std::vector<int> v; for (int i=0;i<200000;++i){v.push_back(1);v.push_back(-1);}
  printf("%d\n", longest_zero_sum_subarray(v));
  std::vector<int> w; for (int i=0;i<133333;++i){w.push_back(1);w.push_back(2);w.push_back(-3);} w.push_back(5);
  printf("%d\n", longest_zero_sum_subarray(w));
}
