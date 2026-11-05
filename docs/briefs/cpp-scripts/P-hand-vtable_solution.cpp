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
    return p->table->value(p, spot);
}

double call_value(const Payoff* self, double spot) { return std::max(spot - self->strike, 0.0); }
double put_value(const Payoff* self, double spot) { return std::max(self->strike - spot, 0.0); }
double digital_value(const Payoff* self, double spot) { return spot > self->strike ? 1.0 : 0.0; }

const PayoffTable call_table = { call_value };
const PayoffTable put_table = { put_value };
const PayoffTable digital_table = { digital_value };

Payoff make_call(double strike) { return Payoff{ &call_table, strike }; }
Payoff make_put(double strike) { return Payoff{ &put_table, strike }; }
Payoff make_digital(double strike) { return Payoff{ &digital_table, strike }; }
