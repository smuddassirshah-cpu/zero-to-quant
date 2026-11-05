# P-clone-basket: exam item e-code-clone-basket (topic-1.9 extension). The clone idiom: copying polymorphic objects without slicing.
HEAD = '''#include <memory>
#include <vector>

// Order is an interface. Market is written for you.
struct Order {
    virtual ~Order() = default;
    // pounds to buy at this market price
    virtual double cost(double market) const = 0;
    virtual std::unique_ptr<Order> clone() const = 0;
};

struct Market : Order {
    explicit Market(int q) : qty(q) {}
    double cost(double market) const override {
        return qty * market;
    }
    std::unique_ptr<Order> clone() const override {
        return std::make_unique<Market>(*this);
    }
    int qty;
};

'''
STARTER = HEAD + '''// TODO: Limit(q, px): buys q shares only if the market
// price is at most px, so cost is q * market then, and 0
// when the market is above px. clone() returns a Limit.
struct Limit : Order {
    Limit(int q, double px) : qty(q), limit(px) {}
    double cost(double) const override { return 0.0; }
    std::unique_ptr<Order> clone() const override {
        return nullptr;
    }
    int qty;
    double limit;
};

// TODO: Basket: holds orders of any kind. cost() is the
// sum of their costs. clone() returns a Basket holding a
// clone of each child (a deep copy).
struct Basket : Order {
    void add(std::unique_ptr<Order> o) { (void)o; }
    double cost(double) const override { return 0.0; }
    std::unique_ptr<Order> clone() const override {
        return nullptr;
    }
    std::vector<std::unique_ptr<Order>> kids;
};
'''
LIMIT = '''struct Limit : Order {
    Limit(int q, double px) : qty(q), limit(px) {}
    double cost(double market) const override {
        return market <= limit ? qty * market : 0.0;
    }
    std::unique_ptr<Order> clone() const override {
        return std::make_unique<Limit>(*this);
    }
    int qty;
    double limit;
};

'''
BASKET = '''struct Basket : Order {
    void add(std::unique_ptr<Order> o) {
        kids.push_back(std::move(o));
    }
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
'''
SOLUTION = HEAD + LIMIT + BASKET
def m(old, new):
    assert old in SOLUTION, old
    return SOLUTION.replace(old, new)
MUTANTS = {
    "limit-clone-forgets-limit": m("std::make_unique<Limit>(*this)", "std::make_unique<Limit>(qty, 1e9)"),
    "limit-fills-above-its-limit": m("market <= limit", "market <= limit + 1.0"),
    "basket-clone-is-shallow-sliced": m("for (const auto& k : kids) copy->add(k->clone());", "for (const auto& k : kids) copy->add(std::make_unique<Market>(1));"),
    "basket-clone-shares-nothing-but-is-empty": m("for (const auto& k : kids) copy->add(k->clone());", ""),
    "basket-clone-steals-the-originals-children": m("for (const auto& k : kids) copy->add(k->clone());", "copy->kids.swap(const_cast<Basket*>(this)->kids);"),
    "basket-cost-forgets-children": m("total += k->cost(market);", "total += 0.0;"),
}
PRELUDE = "#include <type_traits>\n"
T = []
def t(call, expect, setup="", **kw):
    d = {"call": call, "expect": expect}
    if setup: d["setup"] = setup
    d.update(kw); T.append(d)
t("l.cost(2.0)", 200.0, "Limit l(100, 2.5);")
t("l.cost(3.0)", 0.0, "Limit l(100, 2.5);")
t("l.cost(2.5)", 250.0, "Limit l(100, 2.5);")
t("q->cost(2.0)", 200.0, "Limit l(100, 2.5); std::unique_ptr<Order> q = l.clone();")
t("q->cost(3.0)", 0.0, "Limit l(100, 2.5); std::unique_ptr<Order> q = l.clone();")
t("b.cost(2.0)", 500.0, "Basket b; b.add(std::make_unique<Market>(100)); b.add(std::make_unique<Limit>(150, 2.5));")
t("b.cost(3.0)", 300.0, "Basket b; b.add(std::make_unique<Market>(100)); b.add(std::make_unique<Limit>(150, 2.5));")
t("c->cost(2.0)", 500.0, "Basket b; b.add(std::make_unique<Market>(100)); b.add(std::make_unique<Limit>(150, 2.5)); std::unique_ptr<Order> c = b.clone();")
t("c->cost(2.0)", 500.0, "Basket b; b.add(std::make_unique<Market>(100)); b.add(std::make_unique<Limit>(150, 2.5)); std::unique_ptr<Order> c = b.clone(); b.add(std::make_unique<Market>(1000));")
t("b.cost(2.0)", 500.0, "Basket b; b.add(std::make_unique<Market>(100)); b.add(std::make_unique<Limit>(150, 2.5)); std::unique_ptr<Order> c = b.clone();")
t("c->cost(3.0)", 300.0, "Basket inner; inner.add(std::make_unique<Limit>(10, 2.5)); inner.add(std::make_unique<Market>(100)); Basket outer; outer.add(inner.clone()); outer.add(std::make_unique<Market>(0)); std::unique_ptr<Order> c = outer.clone(); inner.add(std::make_unique<Market>(5));")
t("std::is_abstract_v<Basket>", False)
P = dict(id="P-clone-basket", starter=STARTER, solution=SOLUTION, prelude=PRELUDE, tests=T, leak=True, mutants=MUTANTS)
