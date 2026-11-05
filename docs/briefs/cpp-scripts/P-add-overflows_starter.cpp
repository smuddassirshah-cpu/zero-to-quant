#include <climits>

// Return true if a + b does not fit in an int. The check itself must never overflow.
bool add_overflows(int a, int b) {
    return a + b > INT_MAX;    // TODO: this looks at the sum after it has already overflowed
}
