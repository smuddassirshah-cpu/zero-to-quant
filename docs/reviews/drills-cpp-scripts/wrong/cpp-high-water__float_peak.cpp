// slip: float for double in the running mark
#include <vector>

std::vector<double> high_water(const std::vector<double>& pnl) {
    std::vector<double> out;
    out.reserve(pnl.size());
    float peak = 0;
    for (std::size_t i = 0; i < pnl.size(); ++i) {
        if (i == 0 || pnl[i] > peak) peak = pnl[i];
        out.push_back(peak);
    }
    return out;
}
