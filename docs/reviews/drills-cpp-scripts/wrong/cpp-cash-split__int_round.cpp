// slip: the rounded pence pass through an int (or a 32-bit long, as std::lround gives in the app)
#include <cmath>
#include <cstdlib>
#include <vector>

class Cash {
public:
    static Cash from_pence(long long p) { Cash c; c.p_ = p; return c; }
    static Cash from_pounds(double pounds) { int p = static_cast<int>(std::round(pounds * 100)); return from_pence(p); }
    long long pence() const { return p_; }
    Cash operator+(Cash o) const { return from_pence(p_ + o.p_); }
    std::vector<Cash> split(int n) const {
        std::vector<Cash> parts;
        long long q = p_ / n, r = p_ % n;
        for (int i = 0; i < n; ++i) {
            long long extra = i < std::llabs(r) ? (r > 0 ? 1 : -1) : 0;
            parts.push_back(from_pence(q + extra));
        }
        return parts;
    }
private:
    long long p_ = 0;
};
