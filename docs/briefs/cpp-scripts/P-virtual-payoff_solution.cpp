#include <algorithm>
#include <vector>

// Payoffs are valued through a base pointer. Make that work:
// Payoff is an interface: value() is virtual and has no body here (= 0), the destructor is virtual,
// and Call and Put override value(). Do not change book_value.
struct Payoff {
    explicit Payoff(double k) : strike(k) {}
    virtual ~Payoff() = default;
    virtual double value(double spot) const = 0;
    double strike;
};

struct Call : Payoff {
    using Payoff::Payoff;
    double value(double spot) const override { return std::max(spot - strike, 0.0); }
};

struct Put : Payoff {
    using Payoff::Payoff;
    double value(double spot) const override { return std::max(strike - spot, 0.0); }
};

// Total value of every payoff in the book at this spot.
double book_value(const std::vector<const Payoff*>& book, double spot) {
    double total = 0.0;
    for (const Payoff* p : book) total += p->value(spot);
    return total;
}
