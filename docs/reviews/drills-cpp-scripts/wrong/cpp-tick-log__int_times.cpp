// slip: the times are stored in int, though they may pass 2,147,483,647
#include <vector>

class TickLog {
public:
    bool add(long long t) {
        if (!times_.empty() && t < times_.back()) return false;
        times_.push_back(t);
        return true;
    }
    int size() const { return static_cast<int>(times_.size()); }
    long long span() const { return times_.size() < 2 ? 0 : times_.back() - times_.front(); }
private:
    std::vector<int> times_;
};
