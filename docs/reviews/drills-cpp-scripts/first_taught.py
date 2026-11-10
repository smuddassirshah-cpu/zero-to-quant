"""Where each tool a drill leans on first appears in the taught course.

For every token below, the lessons of `cpp` then `cpp-pricing` (course order, with the level
reviews and homework after their level) whose JSON text contains it. The drill's named lesson
comes from docs/reports/drills-cpp.md. A token first seen after the named lesson is printed
with LATE; one seen nowhere with NEVER.

  python first_taught.py            the table
  python first_taught.py grep TOKEN every file holding TOKEN, with a 100-character context
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')

NAMED = {
    'cpp-clip-returns': 'cpp/l5', 'cpp-fee-pence': 'cpp/l2', 'cpp-high-water': 'cpp/l14', 'cpp-longest-rise': 'cpp/l3',
    'cpp-tick-log': 'cpp/l10', 'cpp-tick-round': 'cpp/l4', 'cpp-crossings': 'cpp/l13', 'cpp-drop-small': 'cpp/l14',
    'cpp-fee-tier': 'cpp/l6', 'cpp-range-out': 'cpp/l7', 'cpp-session-time': 'cpp/l12', 'cpp-temp-limit': 'cpp/l11',
    'cpp-trimmed-mean': 'cpp/l16', 'cpp-fill-csv': 'cpp/l3', 'cpp-mean-ranks': 'cpp/l16', 'cpp-movers': 'cpp/l15',
    'cpp-take-all': 'cpp/l19', 'cpp-compound-df': 'cpp-pricing/l2', 'cpp-prob-between': 'cpp-pricing/l4',
    'cpp-cash-or-nothing': 'cpp-pricing/l7', 'cpp-curve-df': 'cpp-pricing/l2', 'cpp-scaled-payoff': 'cpp-pricing/l5',
    'cpp-bermudan-put': 'cpp-pricing/l6', 'cpp-cash-split': 'cpp-pricing/l1', 'cpp-running-stats': 'cpp-pricing/l8',
}

# drill -> tokens its brief, hint, starter or model solution use
USES = {
    'cpp-clip-returns': ['double& ', 'int& '],
    'cpp-fee-pence': ['long long'],
    'cpp-high-water': ['reserve(', '.back()', 'push_back'],
    'cpp-longest-rise': ['std::vector', '.size()'],
    'cpp-tick-log': ['class ', 'std::vector', 'push_back', '.back()', '.front()', '.empty()', ' const {'],
    'cpp-tick-round': ['std::round', '<cmath>', ' = 0.'],
    'cpp-crossings': ['template <typename'],
    'cpp-drop-small': ['.erase(', '.begin()'],
    'cpp-fee-tier': ['class ', ') const', 'private:', 'std::move'],
    'cpp-range-out': ['nullptr', 'double* '],
    'cpp-session-time': ['explicit ', 'operator+', 'operator<', 'operator-', '% '],
    'cpp-temp-limit': ['= delete', 'int& ', '~'],
    'cpp-trimmed-mean': ['std::sort', 'std::accumulate', '0LL'],
    'cpp-fill-csv': ['std::string', "- '0'", 'const std::string&', '\\\\r', 'long long& ', 'pop_back', 'stoi'],
    'cpp-mean-ranks': ['std::iota', '[&]', 'std::sort'],
    'cpp-movers': ['std::map', '.find(', 'emplace', 'std::sort', '[](', 'std::pair', 'std::abs', 'auto& ['],
    'cpp-take-all': ['&& ', 'std::move', '.clear()'],
    'cpp-compound-df': ['std::pow', 'std::exp'],
    'cpp-prob-between': ['erfc'],
    'cpp-cash-or-nothing': ['erfc', 'std::log', 'd_2'],
    'cpp-curve-df': ['std::exp', 'std::vector', 'interpolat'],
    'cpp-scaled-payoff': ['unique_ptr', 'override', 'make_unique', 'std::move'],
    'cpp-bermudan-put': ['vector<bool>', 'std::pow', 'std::max'],
    'cpp-cash-split': ['llround', 'llabs', 'static ', 'std::round', '% '],
    'cpp-running-stats': ['Welford', 'merge', 'variance', 'n - 1'],
}


def files():
    out = []
    for c in ('cpp', 'cpp-pricing'):
        d = json.load(open(os.path.join(C, c, 'course.json')))
        for k, lv in enumerate(d['levels'], 1):
            for l in lv['lessons']:
                out.append((c + '/' + l.split('-')[0], os.path.join(C, c, l + '.json')))
            for extra in ('review-%d' % k, 'homework-%d' % k):
                p = os.path.join(C, c, extra + '.json')
                if os.path.exists(p):
                    out.append((c + '/' + extra, p))
    return out


def main():
    fs = files()
    order = [n for n, _ in fs]
    text = {n: open(p).read().replace('\\n', '\n').replace('\\"', '"') for n, p in fs}
    if len(sys.argv) > 2 and sys.argv[1] == 'grep':
        tok = sys.argv[2]
        for n in order:
            for m in re.finditer(re.escape(tok), text[n]):
                print('%-24s %s' % (n, text[n][max(0, m.start() - 60):m.end() + 60].replace('\n', ' | ')))
        return
    for d, toks in USES.items():
        named = NAMED[d]
        # the last file a learner at the named lesson has seen: the lesson itself
        cut = order.index(named)
        # a cpp-pricing drill may use all of cpp
        for t in toks:
            seen = [n for n in order if t in text[n]]
            if not seen:
                print('%-20s %-22s NEVER' % (d, t))
            elif order.index(seen[0]) > cut:
                print('%-20s %-22s LATE: named %s, first %s' % (d, t, named, seen[0]))
            else:
                print('%-20s %-22s ok (%s)' % (d, t, seen[0]))


if __name__ == '__main__':
    main()
