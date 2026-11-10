// slip: writes only when both pointers are given
#include <vector>

bool range_of(const std::vector<double>& xs, double* lo, double* hi) {
    if (xs.empty()) return false;
    double mn = xs[0], mx = xs[0];
    for (double x : xs) {
        if (x < mn) mn = x;
        if (x > mx) mx = x;
    }
    if (lo && hi) { *lo = mn; *hi = mx; }
    return true;
}
