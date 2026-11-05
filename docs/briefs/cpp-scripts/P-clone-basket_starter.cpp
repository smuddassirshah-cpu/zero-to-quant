#include <memory>
#include <vector>

// Order is an interface. clone() returns a copy of the same dynamic type, so an
// Order can be copied through a base pointer without slicing. Market is written for you.
struct Order {
    virtual ~Order() = default;
    virtual double cost(double market) const = 0;      // pounds to buy at this market price
    virtual std::unique_ptr<Order> clone() const = 0;
};

struct Market : Order {
    explicit Market(int q) : qty(q) {}
    double cost(double market) const override { return qty * market; }
    std::unique_ptr<Order> clone() const override { return std::make_unique<Market>(*this); }
    int qty;
};

// TODO: Limit(q, px): buys q shares only if the market price is at most px,
// so cost is q * market then, and 0 when the market is above px. clone() returns a Limit.
struct Limit : Order {
    Limit(int q, double px) : qty(q), limit(px) {}
    double cost(double) const override { return 0.0; }
    std::unique_ptr<Order> clone() const override { return nullptr; }
    int qty;
    double limit;
};

// TODO: Basket: holds orders of any kind. cost() is the sum of their costs.
// clone() returns a Basket holding a clone of each child (a deep copy).
struct Basket : Order {
    void add(std::unique_ptr<Order> o) { (void)o; }
    double cost(double) const override { return 0.0; }
    std::unique_ptr<Order> clone() const override { return nullptr; }
    std::vector<std::unique_ptr<Order>> kids;
};
