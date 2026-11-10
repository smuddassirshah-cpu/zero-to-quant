// slip: the comparator uses <=, which is not a strict ordering (undefined behaviour in std::sort)
#include <algorithm>
#include <numeric>
#include <vector>

std::vector<double> mean_ranks(const std::vector<int>& scores) {
    int n = static_cast<int>(scores.size());
    std::vector<int> idx(n);
    std::iota(idx.begin(), idx.end(), 0);
    std::sort(idx.begin(), idx.end(), [&](int a, int b) { return scores[a] <= scores[b]; });
    std::vector<double> out(n);
    int i = 0;
    while (i < n) {
        int j = i;
        while (j + 1 < n && scores[idx[j + 1]] == scores[idx[i]]) ++j;
        double r = (i + 1 + j + 1) / 2.0;
        for (int m = i; m <= j; ++m) out[idx[m]] = r;
        i = j + 1;
    }
    return out;
}
