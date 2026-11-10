"""Writes extra_tests.json: each test the review proposes, its `expect` computed by mine.py's model.

Run with the scratchpad venv Python. `harness.py extra` then runs the C++ model (must pass) and the
named candidates in wrong/ (must fail). An item may carry `postlude`, C++ added after the drill's own.
"""
import bisect, json, os
import mine as m

HERE = os.path.dirname(os.path.abspath(__file__))
X = {}


def add(drill, test, fails, postlude=None, passes=None, replaces=None):
    it = {'test': test, 'fails': fails}
    if replaces is not None:
        it['replaces'] = replaces      # index in the drill's tests that this one takes the place of
    if postlude:
        it['postlude'] = postlude
    if passes:
        it['passes'] = passes
    X.setdefault(drill, []).append(it)


def case(call, args, types, expect, compare):
    return {'call': call, 'args': args, 'types': types, 'expect': expect, 'compare': compare}


add('cpp-cash-split', case('pounds_to_pence', [30000000.01], ['double'], m.pounds_to_pence(30000000.01), 'equal'), ['int_round'], replaces=1)
add('cpp-compound-df', case('df_compounded', [0.05, 0.3, 1], ['double', 'double', 'int'], m.df_compounded(0.05, 0.3, 1), 'isclose'), ['whole_periods'])
add('cpp-compound-df', case('df_compounded', [0.06, 0.75, 2], ['double', 'double', 'int'], m.df_compounded(0.06, 0.75, 2), 'isclose'), ['whole_periods'])
add('cpp-fee-pence', case('fee_pence', [999999999999, 9999], ['long long', 'int'], m.fee_pence(999999999999, 9999), 'equal'), ['double_ceil'])
add('cpp-fill-csv', case('fills_value', ['3,-10\n2,5\n'], ['std::string'], m.fills_value('3,-10\n2,5\n'), 'equal'), ['minus_price'])
add('cpp-fill-csv', case('fills_value', ['1\r2,5\n3,4\n'], ['std::string'], m.fills_value('1\r2,5\n3,4\n'), 'equal'), ['cr_anywhere'])
add('cpp-high-water', case('high_water', [[0.1, 0.3, 0.2]], ['std::vector<double>'], m.high_water([0.1, 0.3, 0.2]), 'isclose'), ['float_peak'])
add('cpp-range-out', case('probe', [[0.1, 0.7, 0.3], True, True], ['std::vector<double>', 'bool', 'bool'], m.probe([0.1, 0.7, 0.3], True, True), 'isclose'), ['float_range'])
add('cpp-scaled-payoff', {'call': 'Forward(99.9)(100.0)', 'expect': m.Forward(99.9)(100.0), 'compare': 'isclose'}, ['float_strike'])
add('cpp-session-time', {'call': 'SessionTime(1500) < SessionTime(100)', 'expect': m.SessionTime(1500) < m.SessionTime(100), 'compare': 'equal'}, ['raw_less'], replaces=12)
add('cpp-session-time', {'call': 'SessionTime(-10) < SessionTime(5)', 'expect': m.SessionTime(-10) < m.SessionTime(5), 'compare': 'equal'}, ['raw_less'])
add('cpp-tick-log', case('run_log', [[3000000000, 1]], ['std::vector<long long>'], m.run_log([3000000000, 1]), 'equal'), ['int_times'])
add('cpp-trimmed-mean', case('latency_trimmed_mean', [[100000001, 100000002, 100000004], 0], ['std::vector<int>', 'int'], m.latency_trimmed_mean([100000001, 100000002, 100000004], 0), 'isclose'), ['float_sum'])
add('cpp-movers', case('movers', [['H', 'H'], [100, 129], 29], ['std::vector<std::string>', 'std::vector<double>', 'double'], m.movers(['H', 'H'], [100, 129], 29), 'equal'), ['divide_threshold'])

# sixty symbols, three sizes of move, twenty tied at each: the tie-break must be written, not inherited
syms = ['S%02d' % i for i in range(60)]
px = [100] * 60 + [110 + 10 * (i * 7 % 3) for i in range(60)]
add('cpp-movers', case('movers', [syms + syms, px, 5], ['std::vector<std::string>', 'std::vector<double>', 'double'], m.movers(syms + syms, px, 5), 'equal'), ['no_tie_break'])

# 100,000 scores with many ties: a comparator that is not strict, or an n squared count, does not get through
s = [(i * 7919) % 1000 for i in range(100000)]
ss = sorted(s)
rank = lambda x: (bisect.bisect_left(ss, x) + bisect.bisect_right(ss, x) + 1) / 2
assert m.mean_ranks(s[:200]) == [(lambda t: (bisect.bisect_left(t, x) + bisect.bisect_right(t, x) + 1) / 2)(sorted(s[:200])) for x in s[:200]]
add('cpp-mean-ranks', {'call': '[]{ std::vector<int> s(100000); for (int i = 0; i < 100000; ++i) s[i] = (i * 7919) % 1000; std::vector<double> r = mean_ranks(s); return std::vector<double>{r[0], r[1], r[99999]}; }()',
                       'expect': [rank(s[0]), rank(s[1]), rank(s[99999])], 'compare': 'isclose'}, ['leq_comparator', 'quadratic'])
add('cpp-mean-ranks', {'call': '[]{ std::vector<double> r = mean_ranks(std::vector<int>(3000, 7)); return std::vector<double>{r[0], r[2999]}; }()',
                       'expect': [1500.5, 1500.5], 'compare': 'isclose'}, ['leq_comparator'])

# a type with < and nothing else, as the constraint promises
add('cpp-crossings', {'call': 'count_crossings(std::vector<Px>{{98}, {101}, {100}, {99}, {102}}, Px{100})', 'expect': m.count_crossings([98, 101, 100, 99, 102], 100), 'compare': 'equal'},
    ['right_but_other_ops'], postlude='struct Px { int p; };\nbool operator<(Px a, Px b) { return a.p < b.p; }\n')

json.dump(X, open(os.path.join(HERE, 'extra_tests.json'), 'w'), indent=1)
print(sum(len(v) for v in X.values()), 'tests for', len(X), 'drills')
