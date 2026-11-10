// slip: only a fall ends a run; a flat day neither adds to it nor ends it
#include <vector>

int longest_rise(const std::vector<double>& closes) {
    int best = 0, run = 0;
    for (std::size_t i = 1; i < closes.size(); ++i) {
        if (closes[i] > closes[i - 1]) ++run;
        else if (closes[i] < closes[i - 1]) run = 0;
        if (run > best) best = run;
    }
    return best;
}
