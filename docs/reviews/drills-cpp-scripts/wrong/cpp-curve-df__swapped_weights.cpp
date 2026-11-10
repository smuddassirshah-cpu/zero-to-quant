// slip: the two weights are the wrong way round
#include <cmath>
#include <vector>

double curve_df(const std::vector<double>& times, const std::vector<double>& zeros, double t) {
    std::size_t n = times.size();
    double y;
    if (t <= times[0]) {
        y = zeros[0] * t;
    } else if (t >= times[n - 1]) {
        y = zeros[n - 1] * t;
    } else {
        std::size_t i = 1;
        while (times[i] < t) ++i;
        double y0 = zeros[i - 1] * times[i - 1], y1 = zeros[i] * times[i];
        double w = (t - times[i - 1]) / (times[i] - times[i - 1]);
        y = y1 + w * (y0 - y1);
    }
    return std::exp(-y);
}
