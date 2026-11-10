// slip: divides the trimmed sum by the full count
#include <algorithm>
#include <numeric>
#include <vector>

double latency_trimmed_mean(std::vector<int> ticks, int k) {
    int n = static_cast<int>(ticks.size());
    if (2 * k >= n) return 0.0;
    std::sort(ticks.begin(), ticks.end());
    long long sum = std::accumulate(ticks.begin() + k, ticks.end() - k, 0LL);
    return static_cast<double>(sum) / n;
}
