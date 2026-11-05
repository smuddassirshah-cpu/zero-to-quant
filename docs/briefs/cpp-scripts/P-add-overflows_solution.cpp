#include <climits>

// Return true if a + b does not fit in an int. The check itself must never overflow.
bool add_overflows(int a, int b) {
    if (b > 0) return a > INT_MAX - b;
    return a < INT_MIN - b;
}
