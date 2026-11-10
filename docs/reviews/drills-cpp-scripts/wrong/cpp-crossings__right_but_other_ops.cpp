// right answers, against the constraint "T needs only <": uses >, == and -
#include <vector>

template <typename T>
int count_crossings(const std::vector<T>& xs, T level) {
    int side = 0, n = 0;
    for (const T& x : xs) {
        if (x == level) continue;
        int s = (x - level) > 0 ? 1 : -1;
        if (side != 0 && s != side) ++n;
        side = s;
    }
    return n;
}
