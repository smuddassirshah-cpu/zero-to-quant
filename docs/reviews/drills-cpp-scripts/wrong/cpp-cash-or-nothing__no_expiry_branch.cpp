// slip: no branch for t = 0, so d2 divides by zero
#include <cmath>

double cash_call(double s, double k, double r, double sigma, double t, double payout) {
    double d2 = (std::log(s / k) + (r - 0.5 * sigma * sigma) * t) / (sigma * std::sqrt(t));
    return payout * std::exp(-r * t) * 0.5 * std::erfc(-d2 / std::sqrt(2.0));
}
