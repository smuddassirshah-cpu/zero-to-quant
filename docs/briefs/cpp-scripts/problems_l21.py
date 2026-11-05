# P-hand-vtable: l21-virtual-dispatch. A virtual call by hand: each object holds a pointer to a shared table of functions.
HEAD = '''#include <algorithm>

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

'''
STARTER = HEAD + '''// What `p->value(spot)` compiles to: find the object's table, call the function in it.
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
'''
SOLUTION = HEAD + '''// What `p->value(spot)` compiles to: find the object's table, call the function in it.
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
'''
def m(old, new):
    assert old in SOLUTION, old
    return SOLUTION.replace(old, new)
MUTANTS = {
    "value_of-passes-the-wrong-spot": m("return p->table->value(p, spot);", "return p->table->value(p, p->strike);"),
    "tables-swapped": m("Payoff{ &call_table, strike }", "Payoff{ &put_table, strike }"),
    "digital-priced-as-call": m("const PayoffTable digital_table = { digital_value };", "const PayoffTable digital_table = { call_value };"),
    "a-new-table-per-object": m("Payoff make_call(double strike) { return Payoff{ &call_table, strike }; }", "Payoff make_call(double strike) { return Payoff{ new PayoffTable{ call_value }, strike }; }"),
    "digital-uses-greater-or-equal": m("spot > self->strike", "spot >= self->strike"),
}
PRELUDE = ""
T = []
def t(call, expect, setup="", **kw):
    d = {"call": call, "expect": expect}
    if setup: d["setup"] = setup
    d.update(kw); T.append(d)
t("value_of(&c, 110.0)", 10.0, "Payoff c = make_call(100);")
t("value_of(&c, 90.0)", 0.0, "Payoff c = make_call(100);")
t("value_of(&p, 90.0)", 10.0, "Payoff p = make_put(100);")
t("value_of(&p, 110.0)", 0.0, "Payoff p = make_put(100);")
t("value_of(&d, 101.0)", 1.0, "Payoff d = make_digital(100);")
t("value_of(&d, 100.0)", 0.0, "Payoff d = make_digital(100);")
t("value_of(&c, 100.0)", 20.0, "Payoff c = make_call(80);")
t("a.table == b.table", True, "Payoff a = make_call(100); Payoff b = make_call(90);")
t("a.table != b.table", True, "Payoff a = make_call(100); Payoff b = make_put(100);")
t("total", 6.0, "Payoff c = make_call(100); Payoff p = make_put(100); Payoff d = make_digital(100); const Payoff* book[3] = {&c, &p, &d}; double total = 0.0; for (const Payoff* x : book) total += value_of(x, 105.0);")
t("value_of(&d, 99.0)", 0.0, "Payoff d = make_digital(100);")
P = dict(id="P-hand-vtable", starter=STARTER, solution=SOLUTION, prelude=PRELUDE, tests=T, alloc=True, leak=True, mutants=MUTANTS)
