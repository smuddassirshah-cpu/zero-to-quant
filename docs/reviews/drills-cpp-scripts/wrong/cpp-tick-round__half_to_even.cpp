// slip: std::nearbyint sends a half-way price to the even tick, not away from zero
#include <cmath>

double round_to_tick(double price, double tick = 0.25) {
    return std::nearbyint(price / tick) * tick;
}
