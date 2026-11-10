"""Second-reader harness for the cpp drill pack (native g++ or clang++).

Usage, from the repo root:
  python harness.py model            model solution, starter and planted on every example and hidden test
  python harness.py san              model solutions under -fsanitize=address,undefined
  python harness.py wrong            every candidate in wrong/<drill-id>__<name>.cpp
  python harness.py extra            proposed tests in extra_tests.json: model must pass, named candidates fail
  python harness.py show <id>        compact dump of one drill for reading
  python harness.py expects          every case as JSON lines (id, kind, index, call, expect) for mine.py
Env: CXX (default g++), ZQ_TMP (build folder).
A case is run in its own process, as the app does. Comparison copies the drill page:
isclose with rel 1e-9 and abs 1e-12 unless the case gives tol; equal is exact.
"""
import json, glob, os, subprocess, sys, hashlib, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
TMP = os.environ.get('ZQ_TMP', '/tmp/zq-cpp-review')
CXX = os.environ.get('CXX', 'g++')
os.makedirs(TMP, exist_ok=True)

PRINT = r'''
// the app compiles against a precompiled header of the standard library, so a learner's missing
// #include does not fail there (app_probe.py confirmed it with cpp-temp-limit); mirror that here
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <iterator>
#include <map>
#include <memory>
#include <numeric>
#include <string>
#include <utility>
#include <vector>
namespace zq_out {
inline void o(bool b) { std::printf(b ? "true" : "false"); }
inline void o(int v) { std::printf("%d", v); }
inline void o(long v) { std::printf("%ld", v); }
inline void o(unsigned v) { std::printf("%u", v); }
inline void o(unsigned long v) { std::printf("%lu", v); }
inline void o(long long v) { std::printf("%lld", v); }
inline void o(unsigned long long v) { std::printf("%llu", v); }
inline void o(double v) {
    if (v != v) std::printf("NaN"); else if (v > 1e308) std::printf("Infinity");
    else if (v < -1e308) std::printf("-Infinity"); else std::printf("%.17g", v); }
inline void o(float v) { o((double)v); }
inline void o(const std::string& s) {
    std::printf("\""); for (char c : s) { if (c == '"' || c == '\\') std::printf("\\%c", c);
    else if (c == '\n') std::printf("\\n"); else std::printf("%c", c); } std::printf("\""); }
inline void o(const char* s) { o(std::string(s)); }
template <class T> void o(const std::vector<T>& v) {
    std::printf("["); for (std::size_t i = 0; i < v.size(); ++i) { if (i) std::printf(","); o(v[i]); } std::printf("]"); }
}
'''


def drills():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'app/content/drills/cpp-*.json'))):
        d = json.load(open(f))
        if d.get('pack') == 'cpp':
            out.append(d)
    return out


def lit(v, t):
    if t.startswith('std::vector<'):
        inner = t[len('std::vector<'):-1]
        return t + '{' + ', '.join(lit(x, inner) for x in v) + '}'
    if t == 'double':
        return '(double)(' + repr(float(v)) + ')'
    if t == 'long long':
        return str(int(v)) + 'LL'
    if t == 'int':
        return str(int(v))
    if t == 'bool':
        return 'true' if v else 'false'
    if t == 'std::string':
        return 'std::string(' + json.dumps(v) + ')'
    raise ValueError(t)


def call_expr(case):
    if 'args' in case:
        return case['call'] + '(' + ', '.join(lit(a, t) for a, t in zip(case['args'], case['types'])) + ')'
    return case['call']


def build(d, code, cases, flags=()):
    """One binary; argv[1] picks the case. Returns (exe or None, compiler stderr)."""
    src = PRINT + d.get('prelude', '') + '\n' + code + '\n' + d.get('postlude', '') + '\nint main(int argc, char** argv) {\n  int k = std::atoi(argv[1]);\n  switch (k) {\n'
    for i, c in enumerate(cases):
        if 'compiles' in c:
            continue
        src += '  case %d: { zq_out::o(%s); break; }\n' % (i, call_expr(c))
    src += '  }\n  return 0;\n}\n'
    h = hashlib.sha1((src + CXX + ' '.join(flags)).encode()).hexdigest()[:16]
    cpp, exe = os.path.join(TMP, h + '.cpp'), os.path.join(TMP, h + '.exe')
    if not os.path.exists(exe):
        open(cpp, 'w').write(src)
        r = subprocess.run([CXX, '-std=c++17', '-O1', '-w', *flags, cpp, '-o', exe], capture_output=True, text=True)
        if r.returncode:
            return None, r.stderr
    return exe, ''


def compiles(d, code, case):
    src = d.get('prelude', '') + '\n' + code + '\n' + d.get('postlude', '') + '\nvoid zq_probe() {\n' + case.get('setup', '') + '\n' + case['compiles'] + '\n}\nint main() { return 0; }\n'
    cpp = os.path.join(TMP, 'probe.cpp')
    open(cpp, 'w').write(src)
    r = subprocess.run([CXX, '-std=c++17', '-fsyntax-only', '-w', cpp], capture_output=True, text=True)
    return r.returncode == 0


def close(a, b, tol):
    rel = (tol or {}).get('rel', 1e-9)
    ab = (tol or {}).get('abs', 1e-12)
    if isinstance(b, list):
        return isinstance(a, list) and len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, (bool, str)) or isinstance(b, (bool, str)):
        return a == b
    if a is None or b is None:
        return a is b
    if isinstance(a, list):
        return False
    if math.isnan(a) or math.isnan(b):
        return math.isnan(a) and math.isnan(b)
    return abs(a - b) <= max(rel * max(abs(a), abs(b)), ab)


def run(d, code, cases=None, flags=(), timeout=5):
    """A list of (ok, got) per case; got is the value, or a string starting '!' for a failure to run."""
    cases = cases if cases is not None else d['examples'] + d['tests']
    exe, err = build(d, code, cases, flags)
    res = []
    for i, c in enumerate(cases):
        if 'compiles' in c:
            got = compiles(d, code, c)
            res.append((got == c['expect'], got))
            continue
        if exe is None:
            el = [x for x in err.split('\n') if 'error' in x]
            res.append((False, '!compile: ' + (el[0] if el else err)[:200]))
            continue
        try:
            r = subprocess.run([exe, str(i)], capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            res.append((False, '!timeout'))
            continue
        if r.returncode:
            res.append((False, '!exit %d %s' % (r.returncode, r.stderr.strip()[:300])))
            continue
        try:
            got = json.loads(r.stdout)
        except Exception:
            res.append((False, '!output ' + r.stdout[:80]))
            continue
        if c['compare'] == 'isclose':
            ok = close(got, c['expect'], c.get('tol'))
        else:
            ok = got == c['expect'] and isinstance(got, bool) == isinstance(c['expect'], bool)
        res.append((ok, got))
    return res


def fails(res):
    return [i for i, (ok, _) in enumerate(res) if not ok]


def main():
    mode = sys.argv[1]
    ds = drills()
    by = {d['id']: d for d in ds}
    bad = 0
    if mode == 'model':
        npl = 0
        for d in ds:
            r = run(d, d['solution'])
            f = fails(r)
            s = fails(run(d, d['starter'], d['tests']))
            line = '%-22s model %s  starter fails %d of %d' % (d['id'], 'PASS' if not f else 'FAIL %s %s' % (f, [r[i][1] for i in f][:3]), len(s), len(d['tests']))
            if f or not s:
                bad += 1
            for k, p in enumerate(d.get('planted', [])):
                pf = fails(run(d, p['code'], d['tests']))
                npl += 1
                line += '  p%d:%d' % (k, len(pf))
                if not pf:
                    bad += 1
                    line += '(PASSES)'
            print(line)
        print('drills %d, planted %d, problems %d, compiler %s' % (len(ds), npl, bad, CXX))
    elif mode == 'san':
        for d in ds:
            r = run(d, d['solution'], flags=('-fsanitize=address,undefined', '-fno-sanitize-recover=all', '-g'), timeout=60)
            f = fails(r)
            if f:
                bad += 1
            print('%-22s %s' % (d['id'], 'clean' if not f else 'FAIL %s %s' % (f, [r[i][1] for i in f][:2])))
        print('problems', bad)
    elif mode == 'wrong':
        n = caught = 0
        only = sys.argv[2] if len(sys.argv) > 2 else ''
        for f in sorted(glob.glob(os.path.join(HERE, 'wrong', only + '*.cpp'))):
            did, name = os.path.basename(f)[:-4].split('__')
            d = by[did]
            r = run(d, open(f).read(), d['tests'])
            ff = fails(r)
            n += 1
            caught += bool(ff)
            tag = 'RIGHT' if name.startswith('right') else 'wrong'
            print('%-20s %-26s %s %s' % (did, name, tag, 'passes ALL %d' % len(r) if not ff else 'fails %d of %d, first tests[%d] -> %s' % (len(ff), len(r), ff[0], str(r[ff[0]][1])[:90])))
        print('candidates %d, caught %d, pass all %d' % (n, caught, n - caught))
    elif mode == 'extra':
        ex = json.load(open(os.path.join(HERE, 'extra_tests.json')))
        for did, items in ex.items():
            for it in items:
                d = by[did]
                if it.get('postlude'):
                    d = dict(d, postlude=d.get('postlude', '') + '\n' + it['postlude'])
                case = it['test']
                r = run(d, d['solution'], [case])
                ok = r[0][0]
                line = '%-20s model %s (%s)' % (did, 'ok' if ok else 'FAIL', str(r[0][1])[:60])
                if not ok:
                    bad += 1
                for nm in it.get('fails', []):
                    code = open(os.path.join(HERE, 'wrong', did + '__' + nm + '.cpp')).read()
                    rr = run(d, code, [case])
                    line += ' | %s -> %s%s' % (nm, str(rr[0][1])[:50], '' if not rr[0][0] else ' STILL PASSES')
                    if rr[0][0]:
                        bad += 1
                for nm in it.get('passes', []):
                    code = open(os.path.join(HERE, 'wrong', did + '__' + nm + '.cpp')).read()
                    rr = run(d, code, [case])
                    line += ' | %s passes: %s' % (nm, rr[0][0])
                    if not rr[0][0]:
                        bad += 1
                print(line)
        print('problems', bad)
    elif mode == 'expects':
        for d in ds:
            for k in ('examples', 'tests'):
                for i, c in enumerate(d[k]):
                    if 'compiles' in c:
                        continue
                    print(json.dumps({'id': d['id'], 'kind': k, 'i': i, 'call': c['call'], 'args': c.get('args'), 'expect': c['expect'], 'compare': c['compare'], 'tol': c.get('tol')}))
    elif mode == 'show':
        d = by[sys.argv[2]]
        for k in ('id', 'name', 'course', 'skills', 'tags', 'difficulty', 'pace', 'brief', 'constraints', 'hint', 'how', 'notes'):
            print(k.upper() + ':', d[k] if isinstance(d[k], (str, int)) else json.dumps(d[k], ensure_ascii=False))
        for k in ('prelude', 'starter', 'postlude', 'solution'):
            if k in d:
                print('--- ' + k + '\n' + d[k])
        for k in ('examples', 'tests'):
            for i, c in enumerate(d[k]):
                print('%s[%d] %s => %s %s %s %s' % (k, i, json.dumps(c.get('args')) if 'args' in c else c.get('call', c.get('compiles')), json.dumps(c['expect']), c.get('compare', ''), c.get('tol', ''), c.get('note', '')))
        for p in d['planted']:
            print('--- planted: ' + p['slip'] + '\n' + p['code'])
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
