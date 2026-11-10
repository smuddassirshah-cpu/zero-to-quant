// slip: the exercise value at step i uses the expiry powers, d to the n - j, not i - j
#include <algorithm>
#include <cmath>
#include <vector>

double bermudan_put(double s, double k, double u, double d, double growth, int n,
                    const std::vector<int>& dates) {
    double q = (growth - d) / (u - d);
    std::vector<bool> can(n + 1, false);
    for (int t : dates) can[t] = true;
    std::vector<double> v(n + 1);
    for (int j = 0; j <= n; ++j) v[j] = std::max(k - s * std::pow(u, j) * std::pow(d, n - j), 0.0);
    for (int i = n - 1; i >= 0; --i) {
        for (int j = 0; j <= i; ++j) {
            v[j] = (q * v[j + 1] + (1 - q) * v[j]) / growth;
            if (can[i]) v[j] = std::max(v[j], k - s * std::pow(u, j) * std::pow(d, n - j));
        }
    }
    return v[0];
}
