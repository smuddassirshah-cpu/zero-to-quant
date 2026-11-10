// slip: float for double in the running low and high
#include <vector>

bool range_of(const std::vector<double>& xs, double* lo, double* hi) {
    if (xs.empty()) return false;
    float mn = xs[0], mx = xs[0];
    for (double x : xs) {
        if (x < mn) mn = x;
        if (x > mx) mx = x;
    }
    if (lo) *lo = mn;
    if (hi) *hi = mx;
    return true;
}
