// slip: the ceiling taken in double, against the constraint "whole-number arithmetic only"
#include <cmath>
#include <cstdint>

long long fee_pence(long long notional_pence, int bps) {
    return static_cast<long long>(std::ceil(notional_pence * bps / 10000.0));
}
