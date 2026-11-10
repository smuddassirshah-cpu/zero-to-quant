// slip: the tier starts are stored in int
#include <utility>
#include <vector>

class FeeSchedule {
public:
    FeeSchedule(std::vector<long long> from, std::vector<int> bps) : bps_(std::move(bps)) {
        for (long long f : from) from_.push_back(static_cast<int>(f));
    }
    int bps_for(long long notional) const {
        std::size_t i = from_.size() - 1;
        while (i > 0 && from_[i] > notional) --i;
        return bps_[i];
    }
    int tiers() const { return static_cast<int>(from_.size()); }
private:
    std::vector<int> from_;
    std::vector<int> bps_;
};
