#include <algorithm>

// A virtual call by hand. Every Payoff holds a pointer to a table of functions,
// as the compiler arranges for a class with virtual functions.
struct Payoff;
struct PayoffTable {
    double (*value)(const Payoff* self, double spot);
};
struct Payoff {
    const PayoffTable* table;    // the "vptr": which table this object uses
    double strike;
};

// What `p->value(spot)` compiles to: find the object's table, call the function in it.
double value_of(const Payoff* p, double spot) {
    return 0.0;    // TODO
}

// TODO: the three functions: call max(spot - strike, 0), put max(strike - spot, 0),
// digital 1 if spot > strike else 0.
double call_value(const Payoff* self, double spot) { return 0.0; }
double put_value(const Payoff* self, double spot) { return 0.0; }
double digital_value(const Payoff* self, double spot) { return 0.0; }

// TODO: one table per kind, shared by every object of that kind.
const PayoffTable call_table = { nullptr };
const PayoffTable put_table = { nullptr };
const PayoffTable digital_table = { nullptr };

// TODO: each maker builds a Payoff that points at the right table.
Payoff make_call(double strike) { return Payoff{ nullptr, strike }; }
Payoff make_put(double strike) { return Payoff{ nullptr, strike }; }
Payoff make_digital(double strike) { return Payoff{ nullptr, strike }; }
