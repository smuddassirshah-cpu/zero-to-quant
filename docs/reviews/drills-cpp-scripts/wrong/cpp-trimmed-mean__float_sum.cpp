// slip: float for double in the sum
#include <algorithm>
#include <numeric>
#include <vector>

double latency_trimmed_mean(std::vector<int> ticks, int k) {
    int n = static_cast<int>(ticks.size());
    if (2 * k >= n) return 0.0;
    std::sort(ticks.begin(), ticks.end());
    float sum = std::accumulate(ticks.begin() + k, ticks.end() - k, 0.0f);
    return sum / (n - 2 * k);
}
