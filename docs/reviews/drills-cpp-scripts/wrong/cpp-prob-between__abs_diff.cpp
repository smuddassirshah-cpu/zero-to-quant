// slip: takes the size of the difference instead of returning 0 for an empty band
#include <cmath>

double prob_between(double mu, double sigma, double a, double b) {
    auto cdf = [&](double x) { return 0.5 * std::erfc(-(x - mu) / (sigma * std::sqrt(2.0))); };
    return std::abs(cdf(b) - cdf(a));
}
