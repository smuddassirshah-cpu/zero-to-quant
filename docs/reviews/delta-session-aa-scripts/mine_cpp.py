"""Delta read, session AA: my own C++ solutions to the 17 `cpp` drills whose tests or starter the fix pass changed.

Each is written from the brief as it now stands (and from the cut starter where there is one), by a method other
than the model's. cpp_run.py compiles and runs them.
"""

SOLUTIONS = {}

SOLUTIONS['cpp-cash-split'] = r'''
// floor and a half test on the size, not llround; split by a running ceiling of what is left
#include <cmath>
#include <vector>
class Cash {
    long long p_ = 0;
public:
    static Cash from_pence(long long p) { Cash c; c.p_ = p; return c; }
    static Cash from_pounds(double pounds) {
        double x = pounds * 100.0;
        double m = std::fabs(x);
        long long whole = static_cast<long long>(std::floor(m));
        if (m - static_cast<double>(whole) >= 0.5) ++whole;
        return from_pence(x < 0 ? -whole : whole);
    }
    long long pence() const { return p_; }
    Cash operator+(Cash other) const { return from_pence(p_ + other.p_); }
    std::vector<Cash> split(int n) const {
        long long size = p_ < 0 ? -p_ : p_, sign = p_ < 0 ? -1 : 1;
        std::vector<Cash> out;
        for (int left = n; left > 0; --left) {
            long long part = (size + left - 1) / left;   // ceiling: the larger parts come first
            out.push_back(from_pence(sign * part));
            size -= part;
        }
        return out;
    }
};
'''

SOLUTIONS['cpp-session-time'] = r'''
// floor division for the wrap; operator< by a difference
class SessionTime {
    int m_;
    static int wrap(long long x) {
        long long q = x / 1440;
        if (x % 1440 != 0 && x < 0) --q;
        return static_cast<int>(x - q * 1440);
    }
public:
    explicit SessionTime(int minutes) : m_(wrap(minutes)) {}
    int minutes() const { return m_; }
};
SessionTime operator+(SessionTime t, int m) {
    long long x = (static_cast<long long>(t.minutes()) + m) % 1440;
    return SessionTime(static_cast<int>(x));
}
int operator-(SessionTime b, SessionTime a) { int d = b.minutes() - a.minutes(); return d < 0 ? d + 1440 : d; }
bool operator<(SessionTime a, SessionTime b) { return b.minutes() - a.minutes() > 0; }
'''

SOLUTIONS['cpp-fill-csv'] = r'''
// one pass over the characters of each line, no substrings
#include <string>
long long fills_value(const std::string& text) {
    long long total = 0;
    std::size_t i = 0, n = text.size();
    while (i <= n) {
        std::size_t e = i;
        while (e < n && text[e] != '\n') ++e;
        std::size_t stop = e;
        if (stop > i && text[stop - 1] == '\r') --stop;   // one \r at the end of the line
        bool good = stop > i;
        int field = 0, digits = 0;
        bool neg = false;
        long long v[2] = {0, 0};
        for (std::size_t k = i; k < stop && good; ++k) {
            char c = text[k];
            if (c >= '0' && c <= '9') { v[field] = v[field] * 10 + (c - '0'); ++digits; }
            else if (c == '-' && field == 0 && k == i) neg = true;
            else if (c == ',' && field == 0 && digits > 0) { field = 1; digits = 0; }
            else good = false;
        }
        if (good && field == 1 && digits > 0) total += (neg ? -v[0] : v[0]) * v[1];
        if (e >= n) break;
        i = e + 1;
    }
    return total;
}
'''

SOLUTIONS['cpp-compound-df'] = r'''
// exp and log1p, not pow
#include <cmath>
double df_compounded(double r, double t, int m) {
    if (m == 0) return std::exp(-r * t);
    return std::exp(-static_cast<double>(m) * t * std::log1p(r / m));
}
'''

SOLUTIONS['cpp-tick-log'] = r'''
// first, last and a count; no vector
class TickLog {
    long long first_ = 0, last_ = 0;
    int n_ = 0;
public:
    bool add(long long t) {
        if (n_ > 0 && t < last_) return false;
        if (n_ == 0) first_ = t;
        last_ = t;
        ++n_;
        return true;
    }
    int size() const { return n_; }
    long long span() const { return n_ < 2 ? 0 : last_ - first_; }
};
'''

SOLUTIONS['cpp-mean-ranks'] = r'''
// sort a copy of the scores, then two binary searches for each score
#include <algorithm>
#include <vector>
std::vector<double> mean_ranks(const std::vector<int>& scores) {
    std::vector<int> s(scores);
    std::sort(s.begin(), s.end());
    std::vector<double> out;
    out.reserve(scores.size());
    for (int x : scores) {
        long long below = std::lower_bound(s.begin(), s.end(), x) - s.begin();
        long long upto = std::upper_bound(s.begin(), s.end(), x) - s.begin();
        out.push_back((below + 1 + upto) / 2.0);
    }
    return out;
}
'''

SOLUTIONS['cpp-movers'] = r'''
// no map: a stable sort of trade positions by symbol, then a stable sort by move on the alphabetical list
#include <algorithm>
#include <cmath>
#include <string>
#include <vector>
std::vector<std::string> movers(const std::vector<std::string>& syms, const std::vector<double>& px, double pct) {
    std::vector<std::size_t> idx(syms.size());
    for (std::size_t i = 0; i < idx.size(); ++i) idx[i] = i;
    std::stable_sort(idx.begin(), idx.end(), [&](std::size_t a, std::size_t b) { return syms[a] < syms[b]; });
    struct M { double move; std::string sym; };
    std::vector<M> keep;
    std::size_t i = 0;
    while (i < idx.size()) {
        std::size_t j = i;
        while (j + 1 < idx.size() && syms[idx[j + 1]] == syms[idx[i]]) ++j;
        double first = px[idx[i]], last = px[idx[j]];
        double ch = std::fabs(last - first);
        if (!(ch * 100 < pct * first)) keep.push_back({ch / first, syms[idx[i]]});
        i = j + 1;
    }
    std::stable_sort(keep.begin(), keep.end(), [](const M& a, const M& b) { return b.move < a.move; });
    std::vector<std::string> out;
    for (const M& m : keep) out.push_back(m.sym);
    return out;
}
'''

SOLUTIONS['cpp-fee-pence'] = r'''
// quotient and remainder of the notional, no + 9999 on the product
long long fee_pence(long long notional_pence, int bps) {
    long long whole = notional_pence / 10000, rest = notional_pence % 10000;
    long long fee = whole * bps;
    long long part = rest * bps;              // below 10^8
    fee += part / 10000;
    if (part % 10000 != 0) ++fee;
    return fee;
}
'''

SOLUTIONS['cpp-high-water'] = r'''
// std::partial_sum with max
#include <algorithm>
#include <numeric>
#include <vector>
std::vector<double> high_water(const std::vector<double>& pnl) {
    std::vector<double> out(pnl.size());
    std::partial_sum(pnl.begin(), pnl.end(), out.begin(), [](double a, double b) { return std::max(a, b); });
    return out;
}
'''

SOLUTIONS['cpp-range-out'] = r'''
// std::minmax_element
#include <algorithm>
#include <vector>
bool range_of(const std::vector<double>& xs, double* lo, double* hi) {
    if (xs.empty()) return false;
    auto mm = std::minmax_element(xs.begin(), xs.end());
    if (lo != nullptr) *lo = *mm.first;
    if (hi != nullptr) *hi = *mm.second;
    return true;
}
'''

SOLUTIONS['cpp-trimmed-mean'] = r'''
// nth_element twice instead of a full sort; the sum in long long
#include <algorithm>
#include <vector>
double latency_trimmed_mean(std::vector<int> ticks, int k) {
    long long n = static_cast<long long>(ticks.size());
    if (2LL * k >= n) return 0.0;
    std::nth_element(ticks.begin(), ticks.begin() + k, ticks.end());
    std::nth_element(ticks.begin() + k, ticks.end() - k - 1, ticks.end());
    long long sum = 0;
    for (long long i = k; i < n - k; ++i) sum += ticks[i];
    return static_cast<double>(sum) / static_cast<double>(n - 2LL * k);
}
'''

SOLUTIONS['cpp-scaled-payoff'] = r'''
// from the brief and the comment-only starter
#include <memory>
#include <utility>
class Forward : public Payoff {
    double strike_;
public:
    explicit Forward(double k) : strike_(k) {}
    double operator()(double spot) const override { return spot - strike_; }
};
class Scaled : public Payoff {
    std::unique_ptr<Payoff> leg_;
    double q_;
public:
    Scaled(double qty, std::unique_ptr<Payoff> inner) : leg_(std::move(inner)), q_(qty) {}
    double operator()(double spot) const override { const Payoff& p = *leg_; return p(spot) * q_; }
};
'''

SOLUTIONS['cpp-crossings'] = r'''
// only operator< on T; two flags, not a side number
#include <vector>
template <typename T>
int count_crossings(const std::vector<T>& xs, T level) {
    int count = 0;
    bool known = false, above = false;
    for (std::size_t i = 0; i < xs.size(); ++i) {
        bool lo = xs[i] < level, hi = level < xs[i];
        if (!lo && !hi) continue;
        if (known && above != hi) ++count;
        known = true;
        above = hi;
    }
    return count;
}
'''

SOLUTIONS['cpp-fee-tier'] = r'''
// upper_bound on the tier starts
#include <algorithm>
#include <vector>
class FeeSchedule {
    std::vector<long long> from_;
    std::vector<int> bps_;
public:
    FeeSchedule(std::vector<long long> from, std::vector<int> bps) : from_(from), bps_(bps) {}
    int bps_for(long long notional) const {
        auto it = std::upper_bound(from_.begin(), from_.end(), notional);
        return bps_[static_cast<std::size_t>(it - from_.begin()) - 1];
    }
    int tiers() const { return static_cast<int>(bps_.size()); }
};
'''

SOLUTIONS['cpp-take-all'] = r'''
// move iterators and one insert
#include <iterator>
void take_all(std::vector<Fill>& dst, std::vector<Fill>&& src) {
    dst.reserve(dst.size() + src.size());
    dst.insert(dst.end(), std::make_move_iterator(src.begin()), std::make_move_iterator(src.end()));
    src.clear();
}
'''

SOLUTIONS['cpp-clip-returns'] = r'''
// from the brief and the comment-only starter
#include <algorithm>
#include <vector>
void clip_returns(std::vector<double>& rets, double cap, int& clipped) {
    int n = 0;
    for (std::size_t i = 0; i < rets.size(); ++i) {
        double c = std::min(std::max(rets[i], -cap), cap);
        if (c != rets[i]) { rets[i] = c; ++n; }
    }
    clipped = n;
}
'''

SOLUTIONS['cpp-drop-small'] = r'''
// erase-remove; the count is the change of size
#include <algorithm>
#include <vector>
int drop_small(std::vector<int>& sizes, int min_size) {
    std::size_t before = sizes.size();
    sizes.erase(std::remove_if(sizes.begin(), sizes.end(), [min_size](int s) { return s < min_size; }), sizes.end());
    return static_cast<int>(before - sizes.size());
}
'''

# Candidates that keep to the brief or break one rule, to see what the changed tests now do with them.
PROBES = {
    # cpp-crossings: right by its results, but uses > and == on T (the constraint forbids it): must not compile now
    ('cpp-crossings', 'right results, uses > and ==', False): r'''
#include <vector>
template <typename T>
int count_crossings(const std::vector<T>& xs, T level) {
    int side = 0, n = 0;
    for (const T& x : xs) {
        if (x == level) continue;
        int s = x > level ? 1 : -1;
        if (side != 0 && s != side) ++n;
        side = s;
    }
    return n;
}
''',
    # cpp-mean-ranks: correct but quadratic; the 100,000-score test is meant to stop it on time
    ('cpp-mean-ranks', 'correct, n squared', None): r'''
#include <vector>
std::vector<double> mean_ranks(const std::vector<int>& scores) {
    std::vector<double> out;
    for (int x : scores) {
        long long below = 0, same = 0;
        for (int y : scores) { below += y < x; same += y == x; }
        out.push_back(below + (same + 1) / 2.0);
    }
    return out;
}
''',
    # cpp-fill-csv: drops a \r\r pair at the line end (the brief says one)
    ('cpp-fill-csv', 'drops every \\r at the line end', None): r'''
#include <string>
static bool num(const std::string& s, bool minus, long long& out) {
    std::size_t i = 0; bool neg = false;
    if (minus && !s.empty() && s[0] == '-') { neg = true; i = 1; }
    if (i == s.size()) return false;
    long long v = 0;
    for (; i < s.size(); ++i) { if (s[i] < '0' || s[i] > '9') return false; v = v * 10 + (s[i] - '0'); }
    out = neg ? -v : v; return true;
}
long long fills_value(const std::string& text) {
    long long total = 0; std::string line;
    for (std::size_t i = 0; i <= text.size(); ++i) {
        if (i == text.size() || text[i] == '\n') {
            while (!line.empty() && line.back() == '\r') line.pop_back();
            std::size_t c = line.find(',');
            long long q = 0, p = 0;
            if (c != std::string::npos && line.find(',', c + 1) == std::string::npos
                && num(line.substr(0, c), true, q) && num(line.substr(c + 1), false, p)) total += q * p;
            line.clear();
        } else line += text[i];
    }
    return total;
}
''',
    # cpp-cash-split: lround, whose long is 32 bits in the app's wasm32 and 64 bits natively
    ('cpp-cash-split', 'std::lround (32-bit long in the app)', None): r'''
#include <cmath>
#include <cstdlib>
#include <vector>
class Cash {
public:
    static Cash from_pence(long long p) { Cash c; c.p_ = p; return c; }
    static Cash from_pounds(double pounds) { return from_pence(std::lround(pounds * 100)); }
    long long pence() const { return p_; }
    Cash operator+(Cash o) const { return from_pence(p_ + o.p_); }
    std::vector<Cash> split(int n) const {
        std::vector<Cash> parts;
        long long q = p_ / n, r = p_ % n;
        for (int i = 0; i < n; ++i) parts.push_back(from_pence(q + (i < std::llabs(r) ? (r > 0 ? 1 : -1) : 0)));
        return parts;
    }
private:
    long long p_ = 0;
};
''',
}
