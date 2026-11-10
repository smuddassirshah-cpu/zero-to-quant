// slip: clips on the size and writes +cap, so a large loss becomes a gain
#include <cmath>
#include <vector>

void clip_returns(std::vector<double>& rets, double cap, int& clipped) {
    clipped = 0;
    for (double& r : rets) {
        if (std::abs(r) > cap) { r = cap; ++clipped; }
    }
}
