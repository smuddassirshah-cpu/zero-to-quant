// not wrong in its answers: the n squared count, which the stated n of 100,000 rules out
#include <vector>

std::vector<double> mean_ranks(const std::vector<int>& scores) {
    std::vector<double> out;
    for (int x : scores) {
        int less = 0, same = 0;
        for (int y : scores) { if (y < x) ++less; if (y == x) ++same; }
        out.push_back(less + (same + 1) / 2.0);
    }
    return out;
}
