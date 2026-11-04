#include <vector>
#include <unordered_map>
#include <cstdio>
long long bad(std::vector<int> nums, int k) {
    std::unordered_map<int, long long> seen;
    seen[0] = 1;
    long long total = 0, count = 0;
    for (int x : nums) {
        total = (total + x) % k;
        count += seen[(int)total];
        ++seen[(int)total];
    }
    return count;
}
int main() {
    printf("%lld %lld %lld\n", bad({-1, 3, 0}, 3), bad({-3, 3}, 3), bad({-2, -4, -6}, 5));
}
