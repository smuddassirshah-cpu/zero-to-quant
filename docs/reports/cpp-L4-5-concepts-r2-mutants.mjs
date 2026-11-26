// Natural wrong codings (and valid alternatives) for every C++ code widget of cpp levels 4 and 5 (audit cpp-4-5-r2).
// want: 'test-N' or 'compile' = the feedback line the coding must reach first; null = a valid program that must pass; 'reject' = must fail
// some test; 'FINDING' = a wrong program that passes today (it must fail: the check stays red until the content is fixed);
// 'DOCUMENTED' = passes, and the widget's own text says no test covers it.
// Natural wrong (and a few valid alternative) codings for every code widget; `want` is the test-N line they should reach.
const rep = (a, b) => (sol) => { if (!sol.includes(a)) throw new Error('pattern missing: ' + a); return sol.replace(a, b); };
const body = (head, b) => () => head + b;
export const jobs = [];
export const fixes = [];
const X = {};
const J = (name, file, where, src, want, note) => jobs.push({ name, file, where, src, want, note });

/* ---------- l14 ---------- */
const MA = '#include <vector>\n\nstd::vector<double> moving_average(const std::vector<double>& xs, int n) {\n    std::vector<double> out;\n';
J('l14s3-A size-n wraps (unsigned loop bound)', 'l14-vector', 's3', body(MA, '    for (std::size_t i = 0; i <= xs.size() - n; ++i) { double s = 0; for (int j = 0; j < n; ++j) s += xs[i + j]; out.push_back(s / n); }\n    return out;\n}\n'), 'test-4');
J('l14s3-B size-n+1 windows, size_t count', 'l14-vector', 's3', body(MA, '    std::size_t w = xs.size() - n + 1;\n    for (std::size_t i = 0; i < w; ++i) { double s = 0; for (int j = 0; j < n; ++j) s += xs[i + j]; out.push_back(s / n); }\n    return out;\n}\n'), 'test-4');
J('l14s3-C int window count (no wrap), no n<1 guard', 'l14-vector', 's3', body(MA, '    int w = static_cast<int>(xs.size()) - n + 1;\n    for (int i = 0; i < w; ++i) { double s = 0; for (int j = 0; j < n; ++j) s += xs[i + j]; out.push_back(s / n); }\n    return out;\n}\n'), 'test-7');
J('l14s3-D guard n>size only, i+n<=size loop', 'l14-vector', 's3', body(MA, '    if (n > static_cast<int>(xs.size())) return out;\n    for (std::size_t i = 0; i + n <= xs.size(); ++i) { double s = 0; for (int j = 0; j < n; ++j) s += xs[i + j]; out.push_back(s / n); }\n    return out;\n}\n'), 'test-7');
const RF = '#include <vector>\n\nstd::vector<double> returns_from(const std::vector<double>& px) {\n    std::vector<double> out;\n';
J('l14s4-A reserve without early return', 'l14-vector', 's4', body(RF, '    out.reserve(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out.push_back(px[i] / px[i - 1] - 1);\n    return out;\n}\n'), 'test-3');
J('l14s4-B no reserve', 'l14-vector', 's4', body(RF, '    for (std::size_t i = 1; i < px.size(); ++i) out.push_back(px[i] / px[i - 1] - 1);\n    return out;\n}\n'), 'test-5');
J('l14s4-C divide by later close', 'l14-vector', 's4', body(RF, '    if (px.size() < 2) return out;\n    out.reserve(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out.push_back((px[i] - px[i - 1]) / px[i]);\n    return out;\n}\n'), 'test-1');
J('l14s4-D reserve(px.size()) (one too many)', 'l14-vector', 's4', body(RF, '    out.reserve(px.size());\n    for (std::size_t i = 1; i < px.size(); ++i) out.push_back(px[i] / px[i - 1] - 1);\n    return out;\n}\n'), 'test-5');
J('l14s4-E sized constructor (valid)', 'l14-vector', 's4', () => '#include <vector>\n\nstd::vector<double> returns_from(const std::vector<double>& px) {\n    if (px.size() < 2) return {};\n    std::vector<double> out(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out[i - 1] = px[i] / px[i - 1] - 1;\n    return out;\n}\n', null);
const T3 = '#include <algorithm>\n#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<double> prices;\n    double p;\n    while (std::cin >> p) {\n        prices.push_back(p);\n    }\n    std::sort(prices.begin(), prices.end());\n';
J('l14s6-A always three', 'l14-vector', 's6', body(T3, '    for (std::size_t k = 0; k < 3; ++k) std::cout << prices[prices.size() - 1 - k] << \'\\n\';\n    return 0;\n}\n'), 'test-2');
J('l14s6-B from the front', 'l14-vector', 's6', body(T3, '    for (std::size_t k = 0; k < 3 && k < prices.size(); ++k) std::cout << prices[k] << \'\\n\';\n    return 0;\n}\n'), 'test-1');
J('l14s6-C first unguarded, rest guarded', 'l14-vector', 's6', body(T3, '    std::size_t n = prices.size();\n    std::cout << prices[n - 1] << \'\\n\';\n    if (n > 1) std::cout << prices[n - 2] << \'\\n\';\n    if (n > 2) std::cout << prices[n - 3] << \'\\n\';\n    return 0;\n}\n'), 'test-3');
J('l14s6-D int k countdown from size-1 to size-3', 'l14-vector', 's6', body(T3, '    for (int k = static_cast<int>(prices.size()) - 1; k >= static_cast<int>(prices.size()) - 3; --k) std::cout << prices[k] << \'\\n\';\n    return 0;\n}\n'), 'test-2');
J('l14s7-A at on to only', 'l14-vector', 's7', () => '#include <vector>\n\ndouble price_change(const std::vector<double>& px, int from, int to) {\n    return px.at(to) - px[from];\n}\n', 'test-4');
J('l14s7-B at on from only', 'l14-vector', 's7', () => '#include <vector>\n\ndouble price_change(const std::vector<double>& px, int from, int to) {\n    return px[to] - px.at(from);\n}\n', 'test-3');
J('l14s7-C hand check, upper bound only', 'l14-vector', 's7', () => '#include <stdexcept>\n#include <vector>\n\ndouble price_change(const std::vector<double>& px, int from, int to) {\n    if (to >= static_cast<int>(px.size()) || from >= static_cast<int>(px.size())) throw std::out_of_range("day");\n    return px[to] - px[from];\n}\n', 'test-4');
const PL = '#include <vector>\n\nstd::vector<std::vector<double>> price_lattice(double s0, double u, double d, int steps) {\n    std::vector<std::vector<double>> tree;\n';
J('l14s10-A rows 1..steps only (no root when steps=0)', 'l14-vector', 's10', body(PL, '    for (int i = 1; i <= steps; ++i) { if (tree.empty()) tree.push_back({s0}); std::vector<double> row; const std::vector<double>& prev = tree.back(); row.push_back(prev[0] * u); for (int j = 0; j < i; ++j) row.push_back(prev[j] * d); tree.push_back(row); }\n    return tree;\n}\n'), 'test-2');
J('l14s10-B ups and downs swapped', 'l14-vector', 's10', body('#include <cmath>\n' + PL, '    for (int i = 0; i <= steps; ++i) { std::vector<double> row; for (int j = 0; j <= i; ++j) row.push_back(s0 * std::pow(u, j) * std::pow(d, i - j)); tree.push_back(row); }\n    return tree;\n}\n'), 'test-1');
J('l14s10-C pow form (valid)', 'l14-vector', 's10', body('#include <cmath>\n' + PL, '    for (int i = 0; i <= steps; ++i) { std::vector<double> row; for (int j = 0; j <= i; ++j) row.push_back(s0 * std::pow(u, i - j) * std::pow(d, j)); tree.push_back(row); }\n    return tree;\n}\n'), null);

/* ---------- l15 ---------- */
J('l15s4-A = not +=', 'l15-maps', 's4', rep('pos[syms[i]] += qty[i];', 'pos[syms[i]] = qty[i];'), 'test-1');
J('l15s4-B erase flat symbols', 'l15-maps', 's4', rep('pos[syms[i]] += qty[i];', 'pos[syms[i]] += qty[i]; if (pos[syms[i]] == 0) pos.erase(syms[i]);'), 'test-3');
J('l15s5-A px[sym]', 'l15-maps', 's5', (s) => s.replace(/auto it = px.find\(sym\);[\s\S]*?\n        \}\n/, 'total += qty * px[sym];\n'), 'compile');
J('l15s5-B px.at(sym)', 'l15-maps', 's5', (s) => s.replace(/auto it = px.find\(sym\);[\s\S]*?\n        \}\n/, 'total += qty * px.at(sym);\n'), 'test-2');
J('l15s5-C count then at (valid)', 'l15-maps', 's5', (s) => s.replace(/auto it = px.find\(sym\);[\s\S]*?\n        \}\n/, 'if (px.count(sym)) total += qty * px.at(sym);\n'), null);
J('l15s7-A unordered_map', 'l15-maps', 's7', (s) => s.replace('#include <map>', '#include <map>\n#include <unordered_map>').replace(/std::map</g, 'std::unordered_map<'), 'test-1');
J('l15s7-B arrival order (vector of names)', 'l15-maps', 's7', () => '#include <iostream>\n#include <map>\n#include <string>\n#include <vector>\n\nint main() {\n    std::map<std::string, int> fills, shares;\n    std::vector<std::string> order;\n    std::string venue;\n    int qty;\n    while (std::cin >> venue >> qty) {\n        if (!fills.count(venue)) order.push_back(venue);\n        ++fills[venue];\n        shares[venue] += qty;\n    }\n    for (const auto& v : order) std::cout << v << \' \' << fills[v] << \' \' << shares[v] << \'\\n\';\n    return 0;\n}\n', 'test-1');

/* ---------- l16 ---------- */
const VW = '#include <numeric>\n#include <vector>\n\ndouble vwap(const std::vector<double>& px, const std::vector<double>& qty) {\n';
J('l16s3-A both totals int 0', 'l16-algorithms', 's3', body(VW, '    auto shares = std::accumulate(qty.begin(), qty.end(), 0);\n    if (shares == 0) return 0;\n    auto value = std::inner_product(px.begin(), px.end(), qty.begin(), 0);\n    return value / shares;\n}\n'), 'test-1');
J('l16s3-B value int 0, shares 0.0', 'l16-algorithms', 's3', body(VW, '    double shares = std::accumulate(qty.begin(), qty.end(), 0.0);\n    if (shares == 0) return 0;\n    double value = std::inner_product(px.begin(), px.end(), qty.begin(), 0);\n    return value / shares;\n}\n'), 'test-6');
J('l16s3-C shares int 0, value 0.0', 'l16-algorithms', 's3', body(VW, '    double shares = std::accumulate(qty.begin(), qty.end(), 0);\n    if (shares == 0) return 0;\n    double value = std::inner_product(px.begin(), px.end(), qty.begin(), 0.0);\n    return value / shares;\n}\n'), 'test-7');
J('l16s3-D unweighted mean', 'l16-algorithms', 's3', body(VW, '    if (px.empty()) return 0;\n    double shares = std::accumulate(qty.begin(), qty.end(), 0.0);\n    if (shares == 0) return 0;\n    return std::accumulate(px.begin(), px.end(), 0.0) / px.size();\n}\n'), 'test-1');
J('l16s3-E no zero check', 'l16-algorithms', 's3', body(VW, '    return std::inner_product(px.begin(), px.end(), qty.begin(), 0.0) / std::accumulate(qty.begin(), qty.end(), 0.0);\n}\n'), 'test-3');
J('l16s3-F checks empty only', 'l16-algorithms', 's3', body(VW, '    if (qty.empty()) return 0;\n    return std::inner_product(px.begin(), px.end(), qty.begin(), 0.0) / std::accumulate(qty.begin(), qty.end(), 0.0);\n}\n'), 'test-4');
const SB = (cmp) => () => '#include <algorithm>\n#include <vector>\n\nstd::vector<Order> sort_book(std::vector<Order> b) {\n    std::sort(b.begin(), b.end(), [](const Order& x, const Order& y) {\n' + cmp + '\n    });\n    return b;\n}\n';
J('l16s4-A price only >', 'l16-algorithms', 's4', SB('        return x.price > y.price;'), 'test-2');
J('l16s4-B price only >=', 'l16-algorithms', 's4', SB('        return x.price >= y.price;'), 'test-2');
J('l16s4-C two keys, time <=', 'l16-algorithms', 's4', SB('        if (x.price != y.price) return x.price > y.price;\n        return x.time <= y.time;'), 'test-6');
J('l16s4-D two keys, price >= then time', 'l16-algorithms', 's4', SB('        if (x.price >= y.price) return true;\n        return x.time < y.time;'), 'test-1');
J('l16s4-E ascending price', 'l16-algorithms', 's4', SB('        if (x.price != y.price) return x.price < y.price;\n        return x.time < y.time;'), 'test-1');
J('l16s4-F price desc, time desc', 'l16-algorithms', 's4', SB('        if (x.price != y.price) return x.price > y.price;\n        return x.time > y.time;'), 'test-2');
J('l16s4-G stable_sort by price only', 'l16-algorithms', 's4', () => '#include <algorithm>\n#include <vector>\n\nstd::vector<Order> sort_book(std::vector<Order> b) {\n    std::stable_sort(b.begin(), b.end(), [](const Order& x, const Order& y) { return x.price > y.price; });\n    return b;\n}\n', 'test-2');
const CU = '#include <algorithm>\n#include <numeric>\n#include <vector>\n\nint count_up_days(const std::vector<double>& px) {\n';
J('l16s5-A counts slot 0', 'l16-algorithms', 's5', body(CU, '    std::vector<double> d(px.size());\n    std::adjacent_difference(px.begin(), px.end(), d.begin());\n    return std::count_if(d.begin(), d.end(), [](double x) { return x > 0; });\n}\n'), 'test-1');
J('l16s5-B skips slot 0, no early return', 'l16-algorithms', 's5', body(CU, '    std::vector<double> d(px.size());\n    std::adjacent_difference(px.begin(), px.end(), d.begin());\n    return std::count_if(d.begin() + 1, d.end(), [](double x) { return x > 0; });\n}\n'), 'test-2');
J('l16s5-C >= 0', 'l16-algorithms', 's5', body(CU, '    if (px.size() < 2) return 0;\n    std::vector<double> d(px.size());\n    std::adjacent_difference(px.begin(), px.end(), d.begin());\n    return std::count_if(d.begin() + 1, d.end(), [](double x) { return x >= 0; });\n}\n'), 'test-5');
J('l16s5-D counts slot 0 minus one', 'l16-algorithms', 's5', body(CU, '    std::vector<double> d(px.size());\n    std::adjacent_difference(px.begin(), px.end(), d.begin());\n    return std::count_if(d.begin(), d.end(), [](double x) { return x > 0; }) - 1;\n}\n'), 'test-2');
const WD = '#include <algorithm>\n#include <numeric>\n#include <vector>\n\ndouble worst_drawdown(const std::vector<double>& daily) {\n    std::vector<double> cum(daily.size());\n    std::partial_sum(daily.begin(), daily.end(), cum.begin());\n';
J('l16s9-A peak from first total (guarded)', 'l16-algorithms', 's9', body(WD, '    if (cum.empty()) return 0;\n    double peak = cum[0];\n    double worst = 0;\n    std::for_each(cum.begin(), cum.end(), [&peak, &worst](double c) { peak = std::max(peak, c); worst = std::max(worst, peak - c); });\n    return worst;\n}\n'), 'test-3');
J('l16s9-B mutable copies', 'l16-algorithms', 's9', body(WD, '    double peak = 0;\n    double worst = 0;\n    std::for_each(cum.begin(), cum.end(), [peak, worst](double c) mutable { peak = std::max(peak, c); worst = std::max(worst, peak - c); });\n    return worst;\n}\n'), 'test-1');
J('l16s9-C value captures, not mutable', 'l16-algorithms', 's9', body(WD, '    double peak = 0;\n    double worst = 0;\n    std::for_each(cum.begin(), cum.end(), [peak, worst](double c) { peak = std::max(peak, c); worst = std::max(worst, peak - c); });\n    return worst;\n}\n'), 'compile');
J('l16s9-D peak from first total (unguarded)', 'l16-algorithms', 's9', body(WD, '    double peak = cum[0];\n    double worst = 0;\n    std::for_each(cum.begin(), cum.end(), [&peak, &worst](double c) { peak = std::max(peak, c); worst = std::max(worst, peak - c); });\n    return worst;\n}\n'), 'test-2');

/* ---------- l17 ---------- */
J('l17s4-A forward discounted', 'l17-cmake', 's4', rep('return spot / discount_factor(r, t);', 'return spot * discount_factor(r, t);'), 'test-2');
J('l17s4-B pv with one time', 'l17-cmake', 's4', rep('pv += cash[i] * discount_factor(r, times[i]);', 'pv += cash[i] * discount_factor(r, times.back());'), 'test-4');
J('l17s4-C pv not discounted', 'l17-cmake', 's4', rep('pv += cash[i] * discount_factor(r, times[i]);', 'pv += cash[i];'), 'test-4');
J('l17s4-D float parameter (overload, no definition)', 'l17-cmake', 's4', rep('double forward_price(double spot, double r, double t) {', 'double forward_price(double spot, double r, float t) {'), 'compile');
J('l17s5-A two params, basis fixed 365', 'l17-cmake', 's5', () => '// src/daycount.cpp\n\ndouble year_fraction(int days, int basis) {\n    return days / 365.0;\n}\n\ndouble accrued(double coupon, int days, int basis) {\n    return coupon * year_fraction(days, basis);\n}\n', 'test-1');
J('l17s5-B int division', 'l17-cmake', 's5', () => '// src/daycount.cpp\n\ndouble year_fraction(int days, int basis) {\n    return days / basis;\n}\n\ndouble accrued(double coupon, int days, int basis) {\n    return coupon * year_fraction(days, basis);\n}\n', 'test-1');
J('l17s5-C basis fixed 360', 'l17-cmake', 's5', () => '// src/daycount.cpp\n\ndouble year_fraction(int days, int basis) {\n    return days / 360.0;\n}\n\ndouble accrued(double coupon, int days, int basis) {\n    return coupon * year_fraction(days, basis);\n}\n', 'test-2');
J('l17s5-D double basis parameter', 'l17-cmake', 's5', () => '// src/daycount.cpp\n\ndouble year_fraction(int days, double basis) {\n    return days / basis;\n}\n\ndouble accrued(double coupon, int days, int basis) {\n    return coupon * year_fraction(days, basis);\n}\n', 'compile');

/* ---------- l18 ---------- */
const T18 = (a, b) => () => '// tests\n\nTEST(at_the_money_matches_known_value) {\n' + a + '\n}\n\nTEST(expiry_pays_intrinsic) {\n' + b + '\n}\n';
J('l18s3-A == on the pin', 'l18-unit-tests', 's3', T18('    CHECK(bs_call(100, 100, 0.05, 0.2, 1.0) == 10.4506);', '    CHECK_CLOSE(bs_call(90, 100, 0.05, 0.2, 0.0), 0.0, 1e-12);\n    CHECK_CLOSE(bs_call(110, 100, 0.05, 0.2, 0.0), 10.0, 1e-12);'), 'test-1');
J('l18s3-B tol 1e-5', 'l18-unit-tests', 's3', T18('    CHECK_CLOSE(bs_call(100, 100, 0.05, 0.2, 1.0), 10.4506, 1e-5);', '    CHECK_CLOSE(bs_call(90, 100, 0.05, 0.2, 0.0), 0.0, 1e-12);\n    CHECK_CLOSE(bs_call(110, 100, 0.05, 0.2, 0.0), 10.0, 1e-12);'), 'test-1');
J('l18s3-C expiry only at 110', 'l18-unit-tests', 's3', T18('    CHECK_CLOSE(bs_call(100, 100, 0.05, 0.2, 1.0), 10.4506, 1e-4);', '    CHECK_CLOSE(bs_call(110, 100, 0.05, 0.2, 0.0), 10.0, 1e-12);'), 'test-3');
J('l18s3-D no ATM pin', 'l18-unit-tests', 's3', T18('', '    CHECK_CLOSE(bs_call(90, 100, 0.05, 0.2, 0.0), 0.0, 1e-12);\n    CHECK_CLOSE(bs_call(110, 100, 0.05, 0.2, 0.0), 10.0, 1e-12);'), 'test-2');
J('l18s3-E ATM pin, empty expiry test', 'l18-unit-tests', 's3', T18('    CHECK_CLOSE(bs_call(100, 100, 0.05, 0.2, 1.0), 10.4506, 1e-4);', ''), 'test-3');
J('l18s3-F ATM pin at r=0 (hand value 7.9656), both expiry', 'l18-unit-tests', 's3', T18('    CHECK_CLOSE(bs_call(100, 100, 0.0, 0.2, 1.0), 7.9656, 1e-4);', '    CHECK_CLOSE(bs_call(90, 100, 0.05, 0.2, 0.0), 0.0, 1e-12);\n    CHECK_CLOSE(bs_call(110, 100, 0.05, 0.2, 0.0), 10.0, 1e-12);'), 'test-4');
const T184 = (b) => (sol, st) => st.replace(/    \/\/ arrange, act, assert:\n    \/\/ pin the value you work out by hand\n/, b + '\n');
J('l18s4-A == 0.1', 'l18-unit-tests', 's4', T184('    CHECK(simple_returns({100.0, 110.0})[0] == 0.1);'), 'test-2');
J('l18s4-B pins shipped value', 'l18-unit-tests', 's4', T184('    CHECK_CLOSE(simple_returns({100.0, 110.0})[0], 0.0909, 1e-4);'), 'test-1');
J('l18s4-C size check only', 'l18-unit-tests', 's4', T184('    CHECK(simple_returns({100.0, 110.0}).size() == 1);'), 'test-1');
J('l18s4-D loose tolerance 0.02', 'l18-unit-tests', 's4', T184('    CHECK_CLOSE(simple_returns({100.0, 110.0})[0], 0.1, 0.02);'), 'test-1');
const SR = '#include <vector>\n// src/returns.cpp\n\nstd::vector<double> simple_returns(const std::vector<double>& px) {\n';
J('l18s5-A guard only', 'l18-unit-tests', 's5', body(SR, '    if (px.size() < 2) return {};\n    std::vector<double> out(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out[i - 1] = (px[i] - px[i - 1]) / px[i];\n    return out;\n}\n'), 'test-1');
J('l18s5-B divisor only', 'l18-unit-tests', 's5', body(SR, '    std::vector<double> out(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out[i - 1] = (px[i] - px[i - 1]) / px[i - 1];\n    return out;\n}\n'), 'test-1');
J('l18s5-C minimal fix: divisor px[i-1], difference form (valid)', 'l18-unit-tests', 's5', body(SR, '    if (px.size() < 2) return {};\n    std::vector<double> out(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out[i - 1] = (px[i] - px[i - 1]) / px[i - 1];\n    return out;\n}\n'), null);
J('l18s5-D hardcoded for scale 1', 'l18-unit-tests', 's5', body(SR, '    std::vector<double> out;\n    for (std::size_t i = 1; i < px.size(); ++i) out.push_back((px[i] - px[i - 1]) / 100.0);\n    return out;\n}\n'), 'test-2');
const T189 = (a, b) => () => '// tests\n\nTEST(matches_python_pricer_at_100_steps) {\n' + a + '\n}\n\nTEST(converges_to_black_scholes) {\n' + b + '\n}\n';
J('l18s9-A pin only, convergence empty', 'l18-unit-tests', 's9', T189('    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 100), 10.430612, 1e-6);', ''), 'test-4');
J('l18s9-B convergence only', 'l18-unit-tests', 's9', T189('', '    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 2000), 10.450584, 0.002);'), 'test-3');
J('l18s9-C pin tol 1e-7', 'l18-unit-tests', 's9', T189('    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 100), 10.430612, 1e-7);', '    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 2000), 10.450584, 0.002);'), 'test-1');
J('l18s9-D pin with ==', 'l18-unit-tests', 's9', T189('    CHECK(binomial_call(100, 100, 0.05, 0.2, 1.0, 100) == 10.430612);', '    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 2000), 10.450584, 0.002);'), 'test-1');
J('l18s9-E pin tol 0.05', 'l18-unit-tests', 's9', T189('    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 100), 10.430612, 0.05);', '    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 2000), 10.450584, 0.002);'), 'test-3');

/* ---------- l19 Buffer ---------- */
const BUFM = (ctor, asg) => (sol) => { const a = sol.indexOf('    Buffer(Buffer&& other) noexcept'), b = sol.indexOf('    int size() const'); if (a < 0 || b < 0) throw new Error('Buffer anchors'); return sol.slice(0, a) + ctor + '\n' + asg + '\n\n' + sol.slice(b); };
const BC = '    Buffer(Buffer&& other) noexcept : size_(other.size_), data_(other.data_) { other.size_ = 0; other.data_ = nullptr; }';
const BA = '    Buffer& operator=(Buffer&& other) noexcept { if (this != &other) { delete[] data_; size_ = other.size_; data_ = other.data_; other.size_ = 0; other.data_ = nullptr; } return *this; }';
J('l19s5-A ctor does not empty source', 'l19-moving-not-copying', 's5', BUFM('    Buffer(Buffer&& other) noexcept : size_(other.size_), data_(other.data_) {}', BA), 'reject');
J('l19s5-B ctor nulls data only', 'l19-moving-not-copying', 's5', BUFM('    Buffer(Buffer&& other) noexcept : size_(other.size_), data_(other.data_) { other.data_ = nullptr; }', BA), 'reject');
J('l19s5-C assign leaks own block', 'l19-moving-not-copying', 's5', BUFM(BC, '    Buffer& operator=(Buffer&& other) noexcept { if (this != &other) { size_ = other.size_; data_ = other.data_; other.size_ = 0; other.data_ = nullptr; } return *this; }'), 'reject');
J('l19s5-D assign without self guard', 'l19-moving-not-copying', 's5', BUFM(BC, '    Buffer& operator=(Buffer&& other) noexcept { delete[] data_; size_ = other.size_; data_ = other.data_; other.size_ = 0; other.data_ = nullptr; return *this; }'), 'reject');
J('l19s5-E no noexcept', 'l19-moving-not-copying', 's5', BUFM(BC.replace(' noexcept', ''), BA.replace(' noexcept', '')), 'reject');
J('l19s5-F swap-based assign (leaves source holding old block)', 'l19-moving-not-copying', 's5', BUFM(BC, '    Buffer& operator=(Buffer&& other) noexcept { std::swap(size_, other.size_); std::swap(data_, other.data_); return *this; }'), 'reject');
J('l19s5-G moves that copy', 'l19-moving-not-copying', 's5', BUFM('    Buffer(Buffer&& other) noexcept : size_(other.size_), data_(new double[other.size_]) { for (int i = 0; i < size_; ++i) data_[i] = other.data_[i]; delete[] other.data_; other.data_ = nullptr; other.size_ = 0; }', BA), 'reject');
J('l19s5-H move ctor only (no move assign)', 'l19-moving-not-copying', 's5', BUFM(BC, ''), 'reject');
J('l19s5-I assign by release-then-take (valid, no guard needed)', 'l19-moving-not-copying', 's5', BUFM(BC, '    Buffer& operator=(Buffer&& other) noexcept { if (this == &other) return *this; double* d = other.data_; int n = other.size_; other.data_ = nullptr; other.size_ = 0; delete[] data_; data_ = d; size_ = n; return *this; }'), null);

/* ---------- l20 Samples ---------- */
const SAM = (ctor, asg) => (sol) => { const a = sol.indexOf('    Samples(const Samples& other) :'), b = sol.indexOf('    int size() const'); if (a < 0 || b < 0) throw new Error('Samples anchors'); return sol.slice(0, a) + ctor + '\n' + asg + '\n\n' + sol.slice(b); };
const SC = '    Samples(const Samples& other) : size_(other.size_), data_(new double[other.size_]) { for (int i = 0; i < size_; ++i) data_[i] = other.data_[i]; }';
J('l20s5-A assign delete-first, no guard', 'l20-rule-of-five', 's5', SAM(SC, '    Samples& operator=(const Samples& other) { delete[] data_; size_ = other.size_; data_ = new double[size_]; for (int i = 0; i < size_; ++i) data_[i] = other.data_[i]; return *this; }'), 'reject');
J('l20s5-B assign leaks old block', 'l20-rule-of-five', 's5', SAM(SC, '    Samples& operator=(const Samples& other) { if (this != &other) { size_ = other.size_; data_ = new double[size_]; for (int i = 0; i < size_; ++i) data_[i] = other.data_[i]; } return *this; }'), 'reject');
J('l20s5-C assign still shallow', 'l20-rule-of-five', 's5', SAM(SC, '    Samples& operator=(const Samples& other) { size_ = other.size_; data_ = other.data_; return *this; }'), 'reject');
J('l20s5-D guard + delete-first (valid here)', 'l20-rule-of-five', 's5', SAM(SC, '    Samples& operator=(const Samples& other) { if (this != &other) { delete[] data_; size_ = other.size_; data_ = new double[size_]; for (int i = 0; i < size_; ++i) data_[i] = other.data_[i]; } return *this; }'), null);
J('l20s5-E allocate-first, no guard (valid)', 'l20-rule-of-five', 's5', SAM(SC, '    Samples& operator=(const Samples& other) { double* fresh = new double[other.size_]; for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i]; delete[] data_; data_ = fresh; size_ = other.size_; return *this; }'), null);
J('l20s5-F copy-and-swap (valid)', 'l20-rule-of-five', 's5', SAM(SC, '    Samples& operator=(const Samples& other) { Samples t(other); std::swap(size_, t.size_); std::swap(data_, t.data_); return *this; }'), null);
J('l20s5-G assign reuses block without resize', 'l20-rule-of-five', 's5', SAM(SC, '    Samples& operator=(const Samples& other) { for (int i = 0; i < other.size_ && i < size_; ++i) data_[i] = other.data_[i]; return *this; }'), 'reject');
J('l20s5-H ctor copies size but loops on other.size_ after shallow', 'l20-rule-of-five', 's5', SAM('    Samples(const Samples& other) : size_(other.size_), data_(new double[other.size_]) {}', '    Samples& operator=(const Samples& other) { if (this != &other) { double* fresh = new double[other.size_]; for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i]; delete[] data_; data_ = fresh; size_ = other.size_; } return *this; }'), 'reject');

/* ---------- l21 ---------- */
J('l21s5-A digital >=', 'l21-virtual-dispatch', 's5', rep('spot > self->strike ? 1.0 : 0.0', 'spot >= self->strike ? 1.0 : 0.0'), 'reject');
J('l21s5-B value_of ignores table', 'l21-virtual-dispatch', 's5', rep('return p->table->value(p, spot);', 'return std::max(spot - p->strike, 0.0);'), 'reject');
J('l21s5-C every maker uses call table', 'l21-virtual-dispatch', 's5', (s) => s.replace('Payoff{ &put_table, strike }', 'Payoff{ &call_table, strike }').replace('Payoff{ &digital_table, strike }', 'Payoff{ &call_table, strike }'), 'reject');
J('l21s5-D a fresh table per object', 'l21-virtual-dispatch', 's5', rep('Payoff make_call(double strike) { return Payoff{ &call_table, strike }; }', 'Payoff make_call(double strike) { return Payoff{ new PayoffTable{ call_value }, strike }; }'), 'reject');
J('l21s5-E put and call bodies swapped', 'l21-virtual-dispatch', 's5', (s) => s.replace('return std::max(spot - self->strike, 0.0); }', 'return std::max(self->strike - spot, 0.0); }'), 'reject');

/* ---------- l22 ---------- */
const AO = (b) => () => '#include <climits>\n\nconstexpr bool add_overflows(int a, int b) {\n' + b + '\n}\n';
J('l22s4-A sum then compare with a', 'l22-undefined-behaviour', 's4', AO('    int s = a + b;\n    return (b > 0 && s < a) || (b < 0 && s > a);'), 'reject');
J('l22s4-B sum then sign test', 'l22-undefined-behaviour', 's4', AO('    int s = a + b;\n    return (a > 0 && b > 0 && s < 0) || (a < 0 && b < 0 && s >= 0);'), 'reject');
J('l22s4-C long long (valid)', 'l22-undefined-behaviour', 's4', AO('    long long s = static_cast<long long>(a) + b;\n    return s > INT_MAX || s < INT_MIN;'), null);
J('l22s4-D positive side only', 'l22-undefined-behaviour', 's4', AO('    return b > 0 && a > INT_MAX - b;'), 'reject');
J('l22s4-E not constexpr, correct logic', 'l22-undefined-behaviour', 's4', () => '#include <climits>\n\nbool add_overflows(int a, int b) {\n    if (b > 0) return a > INT_MAX - b;\n    return a < INT_MIN - b;\n}\n', 'reject');
J('l22s4-F unsigned wrap then sign bits (valid, defined)', 'l22-undefined-behaviour', 's4', AO('    unsigned s = static_cast<unsigned>(a) + static_cast<unsigned>(b);\n    return ((~(static_cast<unsigned>(a) ^ static_cast<unsigned>(b))) & (static_cast<unsigned>(a) ^ s)) >> 31;'), null);
J('l22s4-G a > INT_MAX - b for every b', 'l22-undefined-behaviour', 's4', AO('    return a > INT_MAX - b;'), 'reject');
J('l22s4-H sum volatile-free, non-constexpr path: int s; s < a only', 'l22-undefined-behaviour', 's4', AO('    return b > 0 ? a + b < a : a + b > a;'), 'reject');
J('l22s4-I builtin (valid)', 'l22-undefined-behaviour', 's4', AO('    int s = 0;\n    return __builtin_add_overflow(a, b, &s);'), null);

/* ---------- l23 ---------- */
const UP = (members) => (sol) => { const a = sol.indexOf('    ~UniquePtr()'), b = sol.indexOf('    T* get() const'); const c = sol.indexOf('    T* release() {'), d = sol.indexOf('private:'); if (a < 0 || b < 0 || c < 0 || d < 0) throw new Error('UniquePtr anchors'); return sol.slice(0, a) + members.top + '\n\n' + sol.slice(b, c) + (members.rr || sol.slice(c, d)) + sol.slice(d); };
const UTOP = (asg, extra = {}) => '    ~UniquePtr() { delete ptr_; }\n    UniquePtr(const UniquePtr&) = delete;\n    UniquePtr& operator=(const UniquePtr&) = delete;\n    ' + (extra.ctor || 'UniquePtr(UniquePtr&& other) noexcept : ptr_(other.ptr_) { other.ptr_ = nullptr; }') + '\n    ' + asg;
J('l23s2-A assign delete-first with guard', 'l23-own-smart-pointer', 's2', UP({ top: UTOP('UniquePtr& operator=(UniquePtr&& other) noexcept { if (this != &other) { delete ptr_; ptr_ = other.ptr_; other.ptr_ = nullptr; } return *this; }') }), 'reject');
J('l23s2-B assign without guard, take-first', 'l23-own-smart-pointer', 's2', UP({ top: UTOP('UniquePtr& operator=(UniquePtr&& other) noexcept { T* p = other.ptr_; other.ptr_ = nullptr; delete ptr_; ptr_ = p; return *this; }') }), null);
J('l23s2-C reset(other.release()) (valid, the std form)', 'l23-own-smart-pointer', 's2', UP({ top: UTOP('UniquePtr& operator=(UniquePtr&& other) noexcept { reset(other.release()); return *this; }') }), null);
J('l23s2-D no noexcept', 'l23-own-smart-pointer', 's2', UP({ top: UTOP('UniquePtr& operator=(UniquePtr&& other) { if (this != &other) { T* p = other.ptr_; other.ptr_ = nullptr; delete ptr_; ptr_ = p; } return *this; }', { ctor: 'UniquePtr(UniquePtr&& other) : ptr_(other.ptr_) { other.ptr_ = nullptr; }' }) }), 'reject');
J('l23s2-E release deletes', 'l23-own-smart-pointer', 's2', UP({ top: UTOP('UniquePtr& operator=(UniquePtr&& other) noexcept { if (this != &other) { T* p = other.ptr_; other.ptr_ = nullptr; delete ptr_; ptr_ = p; } return *this; }'), rr: '    T* release() { delete ptr_; ptr_ = nullptr; return nullptr; }\n    void reset(T* p = nullptr) { T* old = ptr_; ptr_ = p; delete old; }\n\n' }), 'reject');
J('l23s2-F reset leaks old', 'l23-own-smart-pointer', 's2', UP({ top: UTOP('UniquePtr& operator=(UniquePtr&& other) noexcept { if (this != &other) { T* p = other.ptr_; other.ptr_ = nullptr; delete ptr_; ptr_ = p; } return *this; }'), rr: '    T* release() { T* p = ptr_; ptr_ = nullptr; return p; }\n    void reset(T* p = nullptr) { ptr_ = p; }\n\n' }), 'reject');
J('l23s2-G move ctor leaves source set', 'l23-own-smart-pointer', 's2', UP({ top: UTOP('UniquePtr& operator=(UniquePtr&& other) noexcept { if (this != &other) { T* p = other.ptr_; other.ptr_ = nullptr; delete ptr_; ptr_ = p; } return *this; }', { ctor: 'UniquePtr(UniquePtr&& other) noexcept : ptr_(other.ptr_) {}' }) }), 'reject');
J('l23s2-H swap-based assign', 'l23-own-smart-pointer', 's2', UP({ top: UTOP('UniquePtr& operator=(UniquePtr&& other) noexcept { std::swap(ptr_, other.ptr_); return *this; }') }), 'reject');
J('l23s2-I copy not deleted (moves written, copies shallow)', 'l23-own-smart-pointer', 's2', UP({ top: '    ~UniquePtr() { delete ptr_; }\n    UniquePtr(const UniquePtr& o) : ptr_(o.ptr_) {}\n    UniquePtr& operator=(const UniquePtr& o) { ptr_ = o.ptr_; return *this; }\n    UniquePtr(UniquePtr&& other) noexcept : ptr_(other.ptr_) { other.ptr_ = nullptr; }\n    UniquePtr& operator=(UniquePtr&& other) noexcept { if (this != &other) { T* p = other.ptr_; other.ptr_ = nullptr; delete ptr_; ptr_ = p; } return *this; }' }), 'reject');
J('l23s2-J reset deletes then assigns (valid order for this spec)', 'l23-own-smart-pointer', 's2', UP({ top: UTOP('UniquePtr& operator=(UniquePtr&& other) noexcept { if (this != &other) { T* p = other.ptr_; other.ptr_ = nullptr; delete ptr_; ptr_ = p; } return *this; }'), rr: '    T* release() { T* p = ptr_; ptr_ = nullptr; return p; }\n    void reset(T* p = nullptr) { delete ptr_; ptr_ = p; }\n\n' }), null);

const SP = (m) => (sol) => { const a = sol.indexOf('    SharedPtr(const SharedPtr& other) :'), b = sol.indexOf('    long use_count() const'); const c = sol.indexOf('private:'); if (a < 0 || b < 0 || c < 0) throw new Error('SharedPtr anchors'); return sol.slice(0, a) + m.members + '\n\n' + sol.slice(b, c) + 'private:\n' + (m.drop || '    void drop() { if (count_ && --*count_ == 0) { delete ptr_; delete count_; } ptr_ = nullptr; count_ = nullptr; }') + '\n    T* ptr_ = nullptr;\n    long* count_ = nullptr;\n};\n'; };
const S_CC = '    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) { if (count_) ++*count_; }';
const S_CA = '    SharedPtr& operator=(const SharedPtr& other) { if (count_ != other.count_) { T* p = other.ptr_; long* c = other.count_; if (c) ++*c; drop(); ptr_ = p; count_ = c; } return *this; }';
const S_MC = '    SharedPtr(SharedPtr&& other) noexcept : ptr_(other.ptr_), count_(other.count_) { other.ptr_ = nullptr; other.count_ = nullptr; }';
const S_MA = '    SharedPtr& operator=(SharedPtr&& other) noexcept { if (this != &other) { T* p = other.ptr_; long* c = other.count_; other.ptr_ = nullptr; other.count_ = nullptr; drop(); ptr_ = p; count_ = c; } return *this; }';
const S_D = '    ~SharedPtr() { drop(); }';
const all = (...x) => x.join('\n');
J('l23s5-A destructor and drop without the null test', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, S_CA, S_MC, S_MA, S_D), drop: '    void drop() { if (--*count_ == 0) { delete ptr_; delete count_; } ptr_ = nullptr; count_ = nullptr; }' }), 'reject');
J('l23s5-A2 plain destructor without null test, members as taught', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, S_CA, S_MC, S_MA, '    ~SharedPtr() { if (--*count_ == 0) { delete ptr_; delete count_; } }') }), 'reject');
J('l23s5-B copy assign drop-first, this guard', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, '    SharedPtr& operator=(const SharedPtr& other) { if (this != &other) { drop(); ptr_ = other.ptr_; count_ = other.count_; if (count_) ++*count_; } return *this; }', S_MC, S_MA, S_D) }), 'reject');
J('l23s5-C copy assign drop-first, no guard', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, '    SharedPtr& operator=(const SharedPtr& other) { drop(); ptr_ = other.ptr_; count_ = other.count_; if (count_) ++*count_; return *this; }', S_MC, S_MA, S_D) }), 'reject');
J('l23s5-D counter never freed', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, S_CA, S_MC, S_MA, S_D), drop: '    void drop() { if (count_ && --*count_ == 0) { delete ptr_; } ptr_ = nullptr; count_ = nullptr; }' }), 'reject');
J('l23s5-E copy-and-swap copy assign (valid)', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, '    SharedPtr& operator=(const SharedPtr& other) { SharedPtr t(other); std::swap(ptr_, t.ptr_); std::swap(count_, t.count_); return *this; }', S_MC, S_MA, S_D) }), null);
J('l23s5-F move assign as swap', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, S_CA, S_MC, '    SharedPtr& operator=(SharedPtr&& other) noexcept { std::swap(ptr_, other.ptr_); std::swap(count_, other.count_); return *this; }', S_D) }), 'reject');
J('l23s5-G move assign drop-first with guard', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, S_CA, S_MC, '    SharedPtr& operator=(SharedPtr&& other) noexcept { if (this != &other) { drop(); ptr_ = other.ptr_; count_ = other.count_; other.ptr_ = nullptr; other.count_ = nullptr; } return *this; }', S_D) }), 'reject');
J('l23s5-H move adds to the count', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, S_CA, '    SharedPtr(SharedPtr&& other) noexcept : ptr_(other.ptr_), count_(other.count_) { if (count_) ++*count_; }', S_MA, S_D) }), 'reject');
J('l23s5-I no moves declared (copies only)', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, S_CA, S_D) }), 'reject');
J('l23s5-J copy assign this-guard, add-first (valid)', 'l23-own-smart-pointer', 's5', SP({ members: all(S_CC, '    SharedPtr& operator=(const SharedPtr& other) { if (this != &other) { T* p = other.ptr_; long* c = other.count_; if (c) ++*c; drop(); ptr_ = p; count_ = c; } return *this; }', S_MC, S_MA, S_D) }), null);
J('l23s5-K copy ctor without null test (copying an empty one writes through null)', 'l23-own-smart-pointer', 's5', SP({ members: all('    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) { ++*count_; }', S_CA, S_MC, S_MA, S_D) }), 'test-9');
J('l23s5-L count per pointer (a long member copied, not shared)', 'l23-own-smart-pointer', 's5', SP({ members: all('    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_ ? new long(*other.count_ + 1) : nullptr) {}', S_CA, S_MC, S_MA, S_D) }), 'reject');

/* ---------- homework-4 ---------- */
J('h4vwap-A unordered_map', 'homework-4', 'h4-vwap-book', (s) => s.replace('#include <map>', '#include <map>\n#include <unordered_map>').replace('std::map<std::string, std::vector<Trade>> book;', 'std::unordered_map<std::string, std::vector<Trade>> book;'), 'test-6');
J('h4vwap-B unweighted', 'homework-4', 'h4-vwap-book', (s) => s.replace('value += t.price * t.qty;', 'value += t.price;').replace('shares += t.qty;', 'shares += 1;'), 'test-1');
J('h4vwap-C no fixed/setprecision', 'homework-4', 'h4-vwap-book', rep('    std::cout << std::fixed << std::setprecision(4);\n', ''), 'test-1');
J('h4vwap-D min/max without sort, input order (valid output)', 'homework-4', 'h4-vwap-book', (s) => s.replace(/        std::sort\(trades.begin\(\), trades.end\(\), [^\n]*\n/, '        double lo = trades[0].price, hi = trades[0].price; for (const Trade& t : trades) { lo = std::min(lo, t.price); hi = std::max(hi, t.price); }\n').replace('trades.front().price', 'lo').replace('trades.back().price', 'hi'), null);
J('h4vwap-E int value total', 'homework-4', 'h4-vwap-book', rep('double value = 0;', 'int value = 0;'), 'test-3');
J('h4vwap-F sorted descending (low/high swapped)', 'homework-4', 'h4-vwap-book', rep('return a.price < b.price;', 'return a.price > b.price;'), 'test-1');
const DD = (a, b, c) => () => '// tests\n\nTEST(worst_fall_from_running_peak) {\n' + a + '\n}\n\nTEST(rising_prices_have_no_drawdown) {\n' + b + '\n}\n\nTEST(empty_and_single_price_are_zero) {\n' + c + '\n}\n';
const D1 = '    CHECK_CLOSE(max_drawdown({100.0, 120.0, 90.0, 130.0, 104.0}), 0.25, 1e-12);';
J('h4dd-A rising test left empty', 'homework-4', 'h4-test-drawdown', DD(D1, '', '    CHECK_CLOSE(max_drawdown({}), 0.0, 1e-12);\n    CHECK_CLOSE(max_drawdown({100.0}), 0.0, 1e-12);'), 'test-6');
J('h4dd-B no empty call', 'homework-4', 'h4-test-drawdown', DD(D1, '    CHECK_CLOSE(max_drawdown({100.0, 101.0}), 0.0, 1e-12);', '    CHECK_CLOSE(max_drawdown({100.0}), 0.0, 1e-12);'), 'test-4');
J('h4dd-C series falls from the first price', 'homework-4', 'h4-test-drawdown', DD('    CHECK_CLOSE(max_drawdown({100.0, 80.0}), 0.2, 1e-12);', '    CHECK_CLOSE(max_drawdown({100.0, 101.0}), 0.0, 1e-12);', '    CHECK_CLOSE(max_drawdown({}), 0.0, 1e-12);'), 'test-2');
J('h4dd-D pins pounds 30', 'homework-4', 'h4-test-drawdown', DD('    CHECK_CLOSE(max_drawdown({100.0, 120.0, 90.0, 130.0, 104.0}), 30.0, 1e-12);', '    CHECK_CLOSE(max_drawdown({100.0, 101.0}), 0.0, 1e-12);', '    CHECK_CLOSE(max_drawdown({}), 0.0, 1e-12);'), 'test-1');
J('h4dd-E worst fall is last', 'homework-4', 'h4-test-drawdown', DD('    CHECK_CLOSE(max_drawdown({100.0, 120.0, 90.0}), 0.25, 1e-12);', '    CHECK_CLOSE(max_drawdown({100.0, 101.0}), 0.0, 1e-12);', '    CHECK_CLOSE(max_drawdown({}), 0.0, 1e-12);'), 'test-5');
J('h4dd-F peak 100 so pounds equal fraction x100? series 100,75', 'homework-4', 'h4-test-drawdown', DD('    CHECK_CLOSE(max_drawdown({100.0, 120.0, 90.0, 130.0, 104.0}), 0.25, 1e-12);', '    CHECK_CLOSE(max_drawdown({100.0, 101.0}), 0.0, 1e-12);', ''), 'test-4');
J('h4dd-G four tests', 'homework-4', 'h4-test-drawdown', (s) => s + '\nTEST(extra) { CHECK(true); }\n', 'test-1');
const MED = (b) => () => '// tests\n' + b;
J('h4med-A solution without the empty case', 'homework-4', 'h4-test-median', (s) => s.replace(/TEST\(no_volumes_give_zero\) \{[\s\S]*?\n\}\n/, ''), 'test-6');
J('h4med-B solution without the large case', 'homework-4', 'h4-test-median', (s) => s.replace(/TEST\(large_volumes_do_not_overflow\) \{[\s\S]*?\n\}\n/, ''), 'test-4');
J('h4med-C sorted inputs only', 'homework-4', 'h4-test-median', MED('TEST(a) { CHECK_CLOSE(median_volume({100, 200, 300}), 200.0, 1e-9); }\nTEST(b) { CHECK_CLOSE(median_volume({100, 301, 400, 700}), 350.5, 1e-9); }\nTEST(c) { CHECK_CLOSE(median_volume({1999999999, 2000000000}), 1999999999.5, 1e-6); }\nTEST(d) { CHECK_CLOSE(median_volume({}), 0.0, 1e-12); }\n'), 'test-2');

/* ---------- homework-5 ---------- */
J('h5sg-A move does not switch off the source', 'homework-5', 'h5-scope-guard', rep('        other.active_ = false;\n', ''), 'reject');
J('h5sg-B move not noexcept', 'homework-5', 'h5-scope-guard', rep('ScopeGuard(ScopeGuard&& other) noexcept', 'ScopeGuard(ScopeGuard&& other)'), 'reject');
J('h5sg-C move always active', 'homework-5', 'h5-scope-guard', rep('active_(other.active_) {', 'active_(true) {'), 'reject');
J('h5sg-D dismiss clears the function instead (calls empty function?)', 'homework-5', 'h5-scope-guard', (s) => s.replace('void dismiss() { active_ = false; }', 'void dismiss() { f_ = nullptr; }').replace('if (active_) f_();', 'if (active_ && f_) f_();'), null);
J('h5sg-E relies on moved-from std::function being empty, no flag change', 'homework-5', 'h5-scope-guard', (s) => s.replace('        other.active_ = false;\n', '').replace('if (active_) f_();', 'if (active_ && f_) f_();'), 'reject');
J('h5sg-F move assignment left declared (defaulted)', 'homework-5', 'h5-scope-guard', rep('ScopeGuard& operator=(ScopeGuard&&) = delete;', 'ScopeGuard& operator=(ScopeGuard&&) = default;'), 'reject');
const VEC = (emplace) => (sol) => { const a = sol.indexOf('    template <typename U>\n    void emplace(U&& x) {'), b = sol.indexOf('    std::size_t size_ = 0;\n    std::size_t cap_ = 0;\n    T* data_ = nullptr;\n};', a); if (a < 0 || b < 0) throw new Error('Vec anchors'); return sol.slice(0, a) + emplace + '\n' + sol.slice(b); };
J('h5vec-A relocate first, then build the argument', 'homework-5', 'h5-vec', VEC('    template <typename U>\n    void emplace(U&& x) {\n        if (size_ == cap_) {\n            std::size_t new_cap = cap_ ? cap_ * 2 : 1;\n            T* fresh = allocate(new_cap);\n            for (std::size_t i = 0; i < size_; ++i) { new (fresh + i) T(std::move_if_noexcept(data_[i])); data_[i].~T(); }\n            ::operator delete(data_);\n            data_ = fresh;\n            cap_ = new_cap;\n        }\n        new (data_ + size_) T(std::forward<U>(x));\n        ++size_;\n    }'), 'reject');
J('h5vec-B plain std::move on growth', 'homework-5', 'h5-vec', rep('T(std::move_if_noexcept(data_[i]))', 'T(std::move(data_[i]))'), 'reject');
J('h5vec-C copies on growth', 'homework-5', 'h5-vec', rep('T(std::move_if_noexcept(data_[i]))', 'T(data_[i])'), 'reject');
J('h5vec-D old elements not destroyed on growth', 'homework-5', 'h5-vec', rep('                data_[i].~T();\n', ''), 'reject');
J('h5vec-E grows by one', 'homework-5', 'h5-vec', rep('cap_ ? cap_ * 2 : 1', 'cap_ + 1'), 'reject');
J('h5vec-F rvalue push copies', 'homework-5', 'h5-vec', rep('void push_back(T&& x) { emplace(std::move(x)); }', 'void push_back(T&& x) { emplace(x); }'), 'reject');
J('h5vec-G copy assign without guard, destroy first', 'homework-5', 'h5-vec', (s) => s.replace(/    Vec& operator=\(const Vec& other\) \{[\s\S]*?\n    \}\n/, '    Vec& operator=(const Vec& other) {\n        destroy();\n        data_ = allocate(other.size_);\n        cap_ = other.size_;\n        for (std::size_t i = 0; i < other.size_; ++i) new (data_ + i) T(other.data_[i]);\n        size_ = other.size_;\n        return *this;\n    }\n'), 'reject');
J('h5vec-H destructor frees without destroying elements', 'homework-5', 'h5-vec', rep('    ~Vec() { destroy(); }', '    ~Vec() { ::operator delete(data_); }'), 'reject');
const HS = (f) => (sol) => f(sol);
J('h5ptr-A CountedPtr destructor without null test', 'homework-5', 'h5-sole-and-counted', rep('        if (count_ && --*count_ == 0) {', '        if (--*count_ == 0) {'), 'test-15');
J('h5ptr-B SolePtr move assign delete-first with guard', 'homework-5', 'h5-sole-and-counted', (s) => s.replace(/    SolePtr& operator=\(SolePtr&& other\) noexcept \{[\s\S]*?\n    \}\n/, '    SolePtr& operator=(SolePtr&& other) noexcept {\n        if (this != &other) { delete ptr_; ptr_ = other.ptr_; other.ptr_ = nullptr; }\n        return *this;\n    }\n'), 'reject');
J('h5ptr-C CountedPtr copy assign drop-first with guard', 'homework-5', 'h5-sole-and-counted', (s) => s.replace(/    CountedPtr& operator=\(const CountedPtr& other\) \{[\s\S]*?\n    \}\n/, '    CountedPtr& operator=(const CountedPtr& other) {\n        if (this != &other) {\n            if (count_ && --*count_ == 0) { delete ptr_; delete count_; }\n            ptr_ = other.ptr_; count_ = other.count_;\n            if (count_) ++*count_;\n        }\n        return *this;\n    }\n'), 'reject');
J('h5ptr-D CountedPtr from SolePtr via get() (two owners)', 'homework-5', 'h5-sole-and-counted', rep('CountedPtr(SolePtr<T>&& s) : CountedPtr(s.release()) {}', 'CountedPtr(SolePtr<T>&& s) : CountedPtr(s.get()) {}'), 'reject');
J('h5ptr-E count started for a null pointer', 'homework-5', 'h5-sole-and-counted', rep('count_(p ? new long(1) : nullptr)', 'count_(new long(1))'), 'reject');
J('h5ptr-F copy ctor without null test', 'homework-5', 'h5-sole-and-counted', rep('        if (count_) ++*count_;\n    }\n    CountedPtr(CountedPtr&& other)', '        ++*count_;\n    }\n    CountedPtr(CountedPtr&& other)'), 'test-15');
J('h5ptr-G SolePtr copyable by default (no copy members declared, moves declared)', 'homework-5', 'h5-sole-and-counted', (s) => s.replace('    SolePtr(const SolePtr&) = delete;\n    SolePtr& operator=(const SolePtr&) = delete;\n', ''), null);

Object.assign(X, { SP, all, S_CC, S_CA, S_MC, S_MA, S_D, rep, T189, DD, D1, VW, body });

/* ---------- proposed fixes: each new hidden test (or planted bug) keeps the solution green and rejects the wrong program ----------
   Fix pass: these tests and planted bugs are now in the content, so the jobs below run on it as it stands (their `extra` patches are gone).
   The content's l23 and h5 tests split the counts into separate digits; the old tS9 and tH15 objects are kept for the record only. */
const add = (tests) => (spec) => { spec.tests.push(...tests); return spec; };
/* C++ widgets take at most 15 hidden tests and these two have 15, so the new check replaces a neighbouring test and keeps what it asked */
const swap = (i, t) => (spec) => { if (spec.tests.length !== 15) throw new Error('expected 15 tests'); spec.tests[i] = t; return spec; };
const tS9 = { setup: 'SharedPtr<Tracked> p; SharedPtr<Tracked> q = p;', call: '(p.use_count() + q.use_count()) * 10 + (p.get() == nullptr ? 1 : 0)', expect: 1, compare: 'equal' };
fixes.push({ name: 'X l23s5 solution, test 9 also copies the empty pointer', file: 'l23-own-smart-pointer', where: 's5', src: 'solution', want: null });
fixes.push({ name: 'X l23s5-K copy ctor without null test, test 9 also copies the empty pointer', file: 'l23-own-smart-pointer', where: 's5', src: X.SP({ members: X.all('    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) { ++*count_; }', X.S_CA, X.S_MC, X.S_MA, X.S_D) }), want: 'test-9' });
const tH15 = { setup: 'SolePtr<Quote> u; CountedPtr<Quote> s(std::move(u)); CountedPtr<Quote> e; long n = 0; { CountedPtr<Quote> c(e); n = c.use_count(); }', call: '(s.use_count() + n) * 10 + (s.get() == nullptr ? 1 : 0)', expect: 1, compare: 'equal' };
fixes.push({ name: 'X h5 solution, test 15 also copies and destroys an empty pointer', file: 'homework-5', where: 'h5-sole-and-counted', src: 'solution', want: null });
fixes.push({ name: 'X h5ptr-A dtor without null test, test 15 also copies and destroys an empty pointer', file: 'homework-5', where: 'h5-sole-and-counted', src: X.rep('        if (count_ && --*count_ == 0) {', '        if (--*count_ == 0) {'), want: 'test-15' });
fixes.push({ name: 'X h5ptr-F copy without null test, test 15 also copies and destroys an empty pointer', file: 'homework-5', where: 'h5-sole-and-counted', src: X.rep('        if (count_) ++*count_;\n    }\n    CountedPtr(CountedPtr&& other)', '        ++*count_;\n    }\n    CountedPtr(CountedPtr&& other)'), want: 'test-15' });
fixes.push({ name: 'X h5ptr-E count started for a null pointer, new test 15 still catches it', file: 'homework-5', where: 'h5-sole-and-counted', src: X.rep('count_(p ? new long(1) : nullptr)', 'count_(new long(1))'), want: 'test-15' });
const tV = [{ call: 'vwap', args: [[10.0, 20.0], [0.5, 1.5]], types: ['std::vector<double>', 'std::vector<double>'], expect: 17.5, compare: 'isclose' }];
fixes.push({ name: 'X l16s3 solution + fractional shares', file: 'l16-algorithms', where: 's3', src: 'solution', want: null });
fixes.push({ name: 'X l16s3-C shares int + fractional shares', file: 'l16-algorithms', where: 's3', src: X.body(X.VW, '    double shares = std::accumulate(qty.begin(), qty.end(), 0);\n    if (shares == 0) return 0;\n    double value = std::inner_product(px.begin(), px.end(), qty.begin(), 0.0);\n    return value / shares;\n}\n'), want: 'test-7' });
const p18 = (spec) => { const a = 'int n = v == 2 ? steps - 1 : steps;'; if (!spec.prelude.includes(a)) throw new Error('l18 prelude'); spec.prelude = spec.prelude.replace(a, 'int n = v == 2 ? steps - 1 : v == 3 ? std::min(steps, 100) : steps;'); spec.tests.push({ compare: 'stdout', stdin: '3\n', expect: 'planted bug 3: caught\n' }); return spec; };
fixes.push({ name: 'X l18s9 solution + bug 3', file: 'l18-unit-tests', where: 's9', src: 'solution', want: null });
fixes.push({ name: 'X l18s9-A pin only + bug 3', file: 'l18-unit-tests', where: 's9', src: X.T189('    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 100), 10.430612, 1e-6);', ''), want: 'test-4' });
const pdd = (spec) => { const a = '    return worst;\n}'; if (!spec.prelude.includes(a)) throw new Error('h4 prelude'); spec.prelude = spec.prelude.replace(a, '    if (v == 5 && worst == 0 && px.size() > 1) return (px.back() - px.front()) / px.front();\n    return worst;\n}'); spec.tests.push({ compare: 'stdout', stdin: '5\n', expect: 'planted bug 5: caught\n' }); return spec; };
fixes.push({ name: 'X h4dd solution + bug 5', file: 'homework-4', where: 'h4-test-drawdown', src: 'solution', want: null });
fixes.push({ name: 'X h4dd-A rising empty + bug 5', file: 'homework-4', where: 'h4-test-drawdown', src: X.DD(X.D1, '', '    CHECK_CLOSE(max_drawdown({}), 0.0, 1e-12);\n    CHECK_CLOSE(max_drawdown({100.0}), 0.0, 1e-12);'), want: 'test-6' });

/* ---------- fix pass (audit cpp-4-5-r2): natural codings of each test-N line it wrote, run on the content as it stands ---------- */
J('FP l16s3 test-1: int / int, both totals int 0', 'l16-algorithms', 's3', body(VW, '    int shares = std::accumulate(qty.begin(), qty.end(), 0);\n    if (shares == 0) return 0;\n    int value = std::inner_product(px.begin(), px.end(), qty.begin(), 0);\n    return value / shares;\n}\n'), 'test-1');
J('FP l16s3 test-1: one expression, both int 0', 'l16-algorithms', 's3', body(VW, '    if (std::accumulate(qty.begin(), qty.end(), 0) == 0) return 0;\n    return std::inner_product(px.begin(), px.end(), qty.begin(), 0) / std::accumulate(qty.begin(), qty.end(), 0);\n}\n'), 'test-1');
J('FP l16s3 test-7: auto shares from int 0', 'l16-algorithms', 's3', body(VW, '    auto shares = std::accumulate(qty.begin(), qty.end(), 0);\n    if (shares == 0) return 0;\n    double value = std::inner_product(px.begin(), px.end(), qty.begin(), 0.0);\n    return value / shares;\n}\n'), 'test-7');
J('FP l16s3 test-7: int shares', 'l16-algorithms', 's3', body(VW, '    int shares = std::accumulate(qty.begin(), qty.end(), 0);\n    if (shares == 0) return 0;\n    return std::inner_product(px.begin(), px.end(), qty.begin(), 0.0) / shares;\n}\n'), 'test-7');
J('FP l16s3 test-7: long shares from 0L', 'l16-algorithms', 's3', body(VW, '    long shares = std::accumulate(qty.begin(), qty.end(), 0L);\n    if (shares == 0) return 0;\n    double value = std::inner_product(px.begin(), px.end(), qty.begin(), 0.0);\n    return value / shares;\n}\n'), 'test-7');
const PIN = '    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 100), 10.430612, 1e-6);';
J('FP l18s9 test-4: convergence tolerance 0.05', 'l18-unit-tests', 's9', T189(PIN, '    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 2000), 10.450584, 0.05);'), 'test-4');
J('FP l18s9 test-4: convergence tolerance 0.02', 'l18-unit-tests', 's9', T189(PIN, '    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 2000), 10.450584, 0.02);'), 'test-4');
J('FP l18s9 test-4: convergence only a lower bound', 'l18-unit-tests', 's9', T189(PIN, '    CHECK(binomial_call(100, 100, 0.05, 0.2, 1.0, 2000) > 10.4);'), 'test-4');
J('FP l18s9 test-4: convergence run at 100 steps', 'l18-unit-tests', 's9', T189(PIN, '    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 100), 10.450584, 0.05);'), 'test-4');
const EDGE = '    CHECK_CLOSE(max_drawdown({}), 0.0, 1e-12);\n    CHECK_CLOSE(max_drawdown({100.0}), 0.0, 1e-12);';
J('FP h4dd test-6: flat prices in the rising test', 'homework-4', 'h4-test-drawdown', DD(D1, '    CHECK_CLOSE(max_drawdown({100.0, 100.0, 100.0}), 0.0, 1e-12);', EDGE), 'test-6');
J('FP h4dd test-6: rising test checks only >= 0', 'homework-4', 'h4-test-drawdown', DD(D1, '    CHECK(max_drawdown({100.0, 101.0, 103.5}) >= 0.0);', EDGE), 'test-6');
J('FP h4dd test-6: rising test checks only < 0.25', 'homework-4', 'h4-test-drawdown', DD(D1, '    CHECK(max_drawdown({100.0, 101.0, 103.5}) < 0.25);', EDGE), 'test-6');
J('FP l23s5 test-9: copy ctor adds to *count_ unguarded', 'l23-own-smart-pointer', 's5', SP({ members: all('    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) { *count_ += 1; }', S_CA, S_MC, S_MA, S_D) }), 'test-9');
J('FP h5ptr-H CountedPtr copy and destructor both unguarded', 'homework-5', 'h5-sole-and-counted', (s) => rep('        if (count_ && --*count_ == 0) {', '        if (--*count_ == 0) {')(rep('        if (count_) ++*count_;\n    }\n    CountedPtr(CountedPtr&& other)', '        ++*count_;\n    }\n    CountedPtr(CountedPtr&& other)')(s)), 'test-15');
