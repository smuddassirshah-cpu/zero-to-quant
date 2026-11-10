// slip: a value at the level forgets the side, so below, level, above is not counted
#include <vector>

template <typename T>
int count_crossings(const std::vector<T>& xs, T level) {
    int side = 0, n = 0;
    for (const T& x : xs) {
        int s = x < level ? -1 : (level < x ? 1 : 0);
        if (side != 0 && s != 0 && s != side) ++n;
        side = s;
    }
    return n;
}
