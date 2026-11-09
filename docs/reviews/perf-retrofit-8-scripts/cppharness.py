"""Reader harness for C++ code items, written for this batch (not the authors').

It mirrors the shapes app/js/engine/widgets/cpp-grade.js grades: a value case
(setup, call or call with args and types, expect, equal or isclose with
relative 1e-9 and absolute 1e-12), a raises case (any abnormal end passes), a
compile check (the probe goes in a function after the learner's code) and a
script-mode stdout case (stdin in, whitespace-normalised text out).
Each source is compiled natively with g++ and clang++ at -std=c++20 -O1
-fno-exceptions, with -D_GLIBCXX_ASSERTIONS as the stand-in for the app's
libc++ hardening (no libc++ on this machine). A source that uses `throw` is
compiled without -fno-exceptions, since the app lets a throw end the run.
"""
import json, math, os, pathlib, re, subprocess, tempfile, time

ROOT = pathlib.Path(__file__).resolve().parents[3]
COURSES = ROOT / "app" / "content" / "courses"
COMPILERS = ["g++", "clang++"]
BASE = ["-std=c++20", "-O1", "-D_GLIBCXX_ASSERTIONS"]


def item(course, fname, iid):
    for it in json.loads((COURSES / course / fname).read_text())["items"]:
        if it["id"] == iid:
            return it
    raise KeyError(iid)


def lit(v, ty=None):
    """A JSON value as a C++ literal, typed as cpp-grade.js types it."""
    if ty and ty.startswith("std::vector<"):
        inner = ty[len("std::vector<"):-1]
        return ty + "{" + ", ".join(lit(x, inner) for x in v) + "}"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v) + ("LL" if abs(v) > 2147483647 else "")
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, list):
        return "{" + ", ".join(lit(x) for x in v) + "}"
    raise TypeError(v)


PRINT = r'''
#include <cstdio>
#include <string>
#include <vector>
#include <type_traits>
namespace zqr {
inline void put(bool b) { std::printf(b ? "true" : "false"); }
template <class T> typename std::enable_if<std::is_integral<T>::value && !std::is_same<T, bool>::value>::type put(T x) { std::printf("%lld", (long long)x); }
template <class T> typename std::enable_if<std::is_floating_point<T>::value>::type put(T x) { std::printf("%.17g", (double)x); }
inline void put(const std::string& s) { std::putchar('"'); for (char c : s) { if (c == '"' || c == '\\') std::putchar('\\'); std::putchar(c); } std::putchar('"'); }
template <class T> void put(const std::vector<T>& v) { std::putchar('['); for (std::size_t i = 0; i < v.size(); ++i) { if (i) std::putchar(','); put(v[i]); } std::putchar(']'); }
}
'''


def _call_expr(c):
    if "args" in c:
        tys = c.get("types") or [None] * len(c["args"])
        return c["call"] + "(" + ", ".join(lit(a, t) for a, t in zip(c["args"], tys)) + ")"
    return c["call"]


def unit(w, src, case):
    """Source for one case (compile checks and stdout cases)."""
    pre = w.get("prelude", "")
    post = w.get("postlude", "")
    if case.get("compiles") is not None:
        body = "\n[[maybe_unused]] static void zq_compile_probe() {\n%s\n%s\n}\n" % (case.get("setup", ""), case["compiles"])
        return pre + "\n" + src + "\n" + post + body + "\nint main() { return 0; }\n"
    return pre + "\n" + src + "\n" + post


def is_script(c):
    return c.get("compiles") is None and (c.get("compare") == "stdout" or "stdin" in c)


def value_unit(w, src, cases):
    """One program for every function-mode case; argv[1] picks the case, each in its own process."""
    pre = w.get("prelude", "")
    post = w.get("postlude", "")
    fns = []
    for k, c in enumerate(cases):
        if c.get("compare") == "raises":
            body = "auto zq_v = %s; (void)zq_v; std::printf(\"no error\\n\");" % _call_expr(c)
        else:
            body = "zqr::put(%s); std::printf(\"\\n\");" % _call_expr(c)
        fns.append("static void zq_case_%d() {\n%s\n%s\n}\n" % (k, c.get("setup", ""), body))
    disp = "".join("if (k == %d) zq_case_%d();\n" % (k, k) for k in range(len(cases)))
    main = "#include <cstdlib>\nint main(int argc, char** argv) { int k = std::atoi(argv[1]);\n%sreturn 0; }\n" % disp
    return pre + PRINT + "#define main zq_learner_main\n" + src + "\n#undef main\n" + post + "\n" + "".join(fns) + main


def _same(a, e, mode, tol=None):
    if isinstance(e, list):
        return isinstance(a, list) and len(a) == len(e) and all(_same(x, y, mode, tol) for x, y in zip(a, e))
    if isinstance(e, bool) or isinstance(a, bool):
        return a == e
    if isinstance(e, (int, float)):
        if not isinstance(a, (int, float)):
            return False
        if mode == "isclose":
            r, ab = (tol or [1e-9, 1e-12])
            return a == e or (math.isfinite(a) and math.isfinite(e) and abs(a - e) <= max(r * max(abs(a), abs(e)), ab))
        return a == e
    return a == e


def _norm(t):
    ls = [l.rstrip() for l in t.replace("\r\n", "\n").split("\n")]
    while ls and not ls[0]:
        ls.pop(0)
    while ls and not ls[-1]:
        ls.pop()
    return "\n".join(ls)


_cache = {}


def _build(cc, code, flags):
    key = (cc, code)
    if key not in _cache:
        d = tempfile.mkdtemp(prefix="zqr")
        f = os.path.join(d, "main.cpp")
        open(f, "w").write(code)
        exe = os.path.join(d, "a.out")
        r = subprocess.run([cc, *flags, f, "-o", exe], capture_output=True, text=True)
        _cache[key] = (exe, "") if r.returncode == 0 else (None, r.stderr)
    return _cache[key]


def _flags(src):
    return BASE + ([] if "throw" in src else ["-fno-exceptions"])


def _judge(case, r, dt):
    if case.get("compare") == "raises":
        return r.returncode != 0, "exit %d" % r.returncode, dt
    if r.returncode != 0:
        return False, "crash, exit %d" % r.returncode, dt
    if case.get("compare") == "stdout":
        return _norm(r.stdout) == _norm(case["expect"]), r.stdout.strip()[:80], dt
    try:
        a = json.loads(r.stdout.strip())
    except Exception:
        return False, "unreadable " + r.stdout[:60], dt
    tol = None
    if isinstance(case.get("tol"), dict):
        tol = [float(case["tol"].get("rel", 0) or 0), float(case["tol"].get("abs", 0) or 0)]
    return _same(a, case["expect"], case.get("compare", "equal"), tol), str(a)[:80], dt


def results(w, src, cases, cc, timeout=20):
    """[(ok, what, seconds)] per case."""
    flags = _flags(src)
    out = [None] * len(cases)
    vidx = [k for k, c in enumerate(cases) if c.get("compiles") is None and not is_script(c)]
    if vidx:
        exe, err = _build(cc, value_unit(w, src, [cases[k] for k in vidx]), flags)
        for j, k in enumerate(vidx):
            if exe is None:
                m = re.search(r"error: .*", err)
                out[k] = (False, "compile error: " + (m.group(0)[:100] if m else ""), 0.0)
                continue
            t0 = time.time()
            try:
                r = subprocess.run([exe, str(j)], capture_output=True, text=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                out[k] = (False, "timeout", timeout)
                continue
            out[k] = _judge(cases[k], r, time.time() - t0)
    for k, c in enumerate(cases):
        if c.get("compiles") is not None:
            d = tempfile.mkdtemp(prefix="zqr")
            f = os.path.join(d, "probe.cpp")
            open(f, "w").write(unit(w, src, c))
            r = subprocess.run([cc, *flags, "-fsyntax-only", f], capture_output=True, text=True)
            did = r.returncode == 0
            want = c["expect"] not in (False, "false")
            out[k] = (did == want, "compiles" if did else "does not compile", 0.0)
        elif is_script(c):
            exe, err = _build(cc, unit(w, src, c), flags)
            if exe is None:
                m = re.search(r"error: .*", err)
                out[k] = (False, "compile error: " + (m.group(0)[:100] if m else ""), 0.0)
                continue
            t0 = time.time()
            try:
                r = subprocess.run([exe], input=c.get("stdin", ""), capture_output=True, text=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                out[k] = (False, "timeout", timeout)
                continue
            out[k] = _judge(c, r, time.time() - t0)
    return out


def fails(w, src, which="tests", cc="g++"):
    res = results(w, src, w[which], cc)
    return [k + 1 for k, x in enumerate(res) if not x[0]], max((x[2] for x in res), default=0.0)


class Checker:
    def __init__(self):
        self.bad = 0

    def check(self, cond, msg):
        print(("ok   " if cond else "FAIL ") + msg)
        if not cond:
            self.bad += 1


def standard(w, solution_label_pairs, bugs, ck):
    """Shipped solution and reader solutions pass every example and test on both
    compilers; the starter fails at least one test; each reader bug fails one."""
    for label, src in solution_label_pairs:
        for cc in COMPILERS:
            fe, _ = fails(w, src, "examples", cc)
            ft, slow = fails(w, src, "tests", cc)
            ck.check(not fe and not ft, "%s on %s: passes every example and test (slowest run %.3f s)%s" % (label, cc, slow, "" if not ft else " FAILS %s" % ft))
    for cc in COMPILERS:
        ft, _ = fails(w, w["starter"], "tests", cc)
        ck.check(len(ft) >= 1, "starter on %s fails tests %s" % (cc, ft))
    for label, src in bugs:
        res = {}
        for cc in COMPILERS:
            res[cc], _ = fails(w, src, "tests", cc)
        ck.check(all(res.values()), "reader bug %-48s caught: g++ %s, clang++ %s" % ('"%s"' % label, res["g++"], res["clang++"]))
