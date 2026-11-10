// slip: std::remove_if without the erase, so the vector keeps its length
#include <algorithm>
#include <vector>

int drop_small(std::vector<int>& sizes, int min_size) {
    auto it = std::remove_if(sizes.begin(), sizes.end(), [&](int s) { return s < min_size; });
    return static_cast<int>(sizes.end() - it);
}
