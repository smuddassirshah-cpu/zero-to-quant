// slip: discounts one whole period at a time, so a part period is dropped
#include <cmath>

double df_compounded(double r, double t, int m) {
    if (m == 0) return std::exp(-r * t);
    int periods = static_cast<int>(m * t);
    double df = 1.0;
    for (int i = 0; i < periods; ++i) df /= 1.0 + r / m;
    return df;
}
