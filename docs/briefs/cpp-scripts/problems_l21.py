# P-virtual-payoff: l21-virtual-dispatch. Starter: value() is not virtual, so a Payoff* always returns 0.
HEAD = '''#include <algorithm>
#include <vector>

// Payoffs are valued through a base pointer. Make that work:
// Payoff is an interface: value() is virtual and has no body here (= 0), the destructor is virtual,
// and Call and Put override value(). Do not change book_value.
'''
BOOK = '''
// Total value of every payoff in the book at this spot.
double book_value(const std::vector<const Payoff*>& book, double spot) {
    double total = 0.0;
    for (const Payoff* p : book) total += p->value(spot);
    return total;
}
'''
STARTER = HEAD + '''struct Payoff {
    explicit Payoff(double k) : strike(k) {}
    double value(double spot) const { return 0.0; }
    double strike;
};

struct Call : Payoff {
    using Payoff::Payoff;
    double value(double spot) const { return std::max(spot - strike, 0.0); }
};

struct Put : Payoff {
    using Payoff::Payoff;
    double value(double spot) const { return std::max(strike - spot, 0.0); }
};
''' + BOOK
SOLUTION = HEAD + '''struct Payoff {
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
''' + BOOK

def mut(old, new):
    assert old in SOLUTION, old
    return SOLUTION.replace(old, new)

MUTANTS = {
    "virtual-but-not-pure": mut("virtual double value(double spot) const = 0;", "virtual double value(double spot) const { return 0.0; }"),
    "no-virtual-destructor": mut("    virtual ~Payoff() = default;\n", ""),
    "forgot-const-in-base": mut("virtual double value(double spot) const = 0;", "virtual double value(double spot) { return 0.0; }"),
    "forgot-const-in-derived": mut("struct Put : Payoff {\n    using Payoff::Payoff;\n    double value(double spot) const override", "struct Put : Payoff {\n    using Payoff::Payoff;\n    double value(double spot) override"),
}
# "forgot-const-in-base" does not compile: `override` in Call and Put names a function the base lacks, and clang says so.
# A compile error is a caught slip in the app (the learner sees the message), and it is the reason to write `override`.

PRELUDE = "#include <type_traits>\n"

T = []
def t(call, expect, setup="", **kw):
    d = {"call": call, "expect": expect}
    if setup: d["setup"] = setup
    d.update(kw); T.append(d)

t("book_value(book, 110.0)", 10.0, "Call c(100); Put p(100); std::vector<const Payoff*> book{&c, &p};")
t("book_value(book, 90.0)", 10.0, "Call c(100); Put p(100); std::vector<const Payoff*> book{&c, &p};")
t("book_value(book, 110.0)", 15.0, "Call c1(100); Call c2(105); std::vector<const Payoff*> book{&c1, &c2};")
t("book_value(book, 80.0)", 20.0, "Put p(100); std::vector<const Payoff*> book{&p};")
t("book_value(book, 100.0)", 0.0, "Put p(100); Call c(100); std::vector<const Payoff*> book{&p, &c};")
t("r.value(130.0)", 30.0, "Call c(100); const Payoff& r = c;")
t("std::has_virtual_destructor_v<Payoff>", True)
t("std::is_abstract_v<Payoff>", True)
t("std::is_abstract_v<Call>", False)
t("std::is_polymorphic_v<Put>", True)
T.append({"compiles": "Payoff p(100);", "expect": False})

P = dict(id="P-virtual-payoff", starter=STARTER, solution=SOLUTION, prelude=PRELUDE, tests=T, mutants=MUTANTS)
