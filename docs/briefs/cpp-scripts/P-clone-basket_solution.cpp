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

struct Limit : Order {
    Limit(int q, double px) : qty(q), limit(px) {}
    double cost(double market) const override { return market <= limit ? qty * market : 0.0; }
    std::unique_ptr<Order> clone() const override { return std::make_unique<Limit>(*this); }
    int qty;
    double limit;
};

struct Basket : Order {
    void add(std::unique_ptr<Order> o) { kids.push_back(std::move(o)); }
    double cost(double market) const override {
        double total = 0.0;
        for (const auto& k : kids) total += k->cost(market);
        return total;
    }
    std::unique_ptr<Order> clone() const override {
        auto copy = std::make_unique<Basket>();
        for (const auto& k : kids) copy->add(k->clone());
        return copy;
    }
    std::vector<std::unique_ptr<Order>> kids;
};
