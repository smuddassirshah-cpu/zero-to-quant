# Mimics the app's C++ function-mode runner for the cpp level 5 problems.
# For each problem it builds a starter program and a solution program (hidden prelude, learner code, postlude, one block per test),
# compiles both with g++ and clang++ at -std=c++17 and -std=c++20, -O1 -fno-exceptions, runs them, and expects:
#   solution: every test passes; starter: at least one test fails (and it compiles); every mutant (a plausible learner slip) fails a test.
# allocCheck is emulated by a header that counts every global operator new / new[] and tracks live blocks; a problem with
# leak=True also fails any test block that ends with more live blocks than it began with (the app's leakCheck, per test).
# A test with "compiles" is checked by compiling the snippet alone (-fsyntax-only), as the app's compile checks do.
import json, subprocess, os, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
os.makedirs(BUILD, exist_ok=True)


def lit(v):
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, int): return f"{v}LL" if abs(v) > 2**31 - 1 else str(v)
    if isinstance(v, float): return repr(v)
    if isinstance(v, str): return json.dumps(v)
    raise TypeError(v)


def ctype(v):
    if isinstance(v, bool): return "bool"
    if isinstance(v, int): return "long long"
    if isinstance(v, float): return "double"
    if isinstance(v, str): return "std::string"
    raise TypeError(v)


PRE = '''#include <cstdio>
#include <cmath>
#include <string>
#include <vector>
#include <cstdint>
#include <cstddef>
#include <algorithm>
#include <initializer_list>
#include <type_traits>
'''
ALLOC = '''#include <cstdlib>
#include <new>
namespace zq_alloc { inline volatile int n = 0; inline volatile int live = 0; }
inline void reset_alloc_count() { zq_alloc::n = 0; }
inline int alloc_count() { return zq_alloc::n; }
inline void* zq_get(std::size_t n) { zq_alloc::n = zq_alloc::n + 1; zq_alloc::live = zq_alloc::live + 1; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
inline void zq_put(void* p) noexcept { if (p) { zq_alloc::live = zq_alloc::live - 1; std::free(p); } }
void* operator new(std::size_t n) { return zq_get(n); }
void* operator new[](std::size_t n) { return zq_get(n); }
void* operator new(std::size_t n, const std::nothrow_t&) noexcept { return zq_get(n); }
void* operator new[](std::size_t n, const std::nothrow_t&) noexcept { return zq_get(n); }
void operator delete(void* p) noexcept { zq_put(p); }
void operator delete[](void* p) noexcept { zq_put(p); }
void operator delete(void* p, std::size_t) noexcept { zq_put(p); }
void operator delete[](void* p, std::size_t) noexcept { zq_put(p); }
'''
CMP = '''
template<class A,class B> bool eqv(const A&a,const B&b){ if constexpr(std::is_floating_point<A>::value||std::is_floating_point<B>::value){ double x=(double)a,y=(double)b; return std::fabs(x-y)<=1e-9*std::max(std::fabs(x),std::fabs(y))+1e-12;} else return a==b; }
'''


def esc(s):
    return s.replace("\\", "").replace('"', "'").replace("\n", " ")[:80]


def build(prob, code):
    alloc = prob.get("alloc", False)
    s = PRE + (ALLOC if alloc else "") + prob.get("prelude", "") + "\n" + code + "\n" + prob.get("postlude", "") + CMP
    s += "\nint main(int argc, char** argv){ int which = argc > 1 ? std::atoi(argv[1]) : -1;\n"
    for i, t in enumerate(prob["tests"]):
        if "compiles" in t:
            continue
        ty = ctype(t["expect"])
        leak = prob.get("leak", False)
        s += f"  if (which == {i}) {{\n"
        if leak:
            s += "    int live0 = zq_alloc::live;\n"
        s += f'    bool zq_ok = false;\n    {{ {t.get("setup", "")} auto zq_r = ({t["call"]}); {ty} zq_e = {lit(t["expect"])}; zq_ok = eqv(zq_r, zq_e); }}\n'
        if leak:
            s += "    if (zq_alloc::live != live0) zq_ok = false;\n"
        s += '    std::printf(zq_ok ? "PASS\\n" : "FAIL\\n"); return zq_ok ? 0 : 1;\n  }\n'
    s += "  return 2; }\n"
    return s


def compile_check(prob, code, t, cxx, std):
    s = PRE + prob.get("prelude", "") + "\n" + code + "\n" + prob.get("postlude", "") + "\nvoid zq_snippet() {\n" + t.get("setup", "") + "\n" + t["compiles"] + "\n}\n"
    d = tempfile.mkdtemp(dir=BUILD)
    fn = f"{d}/c.cpp"
    open(fn, "w").write(s)
    r = subprocess.run([cxx, f"-std={std}", "-fsyntax-only", "-fno-exceptions", fn], capture_output=True, text=True)
    return (r.returncode == 0) == t["expect"]


def one(prob, code, name, cxx, std, extra=()):
    """returns (failed, total, lines): failed -1 means a compile error, -2 a crash"""
    src = build(prob, code)
    d = tempfile.mkdtemp(dir=BUILD)
    fn = f"{d}/{prob['id']}_{name}.cpp"
    open(fn, "w").write(src)
    exe = fn[:-4] + "." + cxx.replace("+", "p")
    flags = [f"-std={std}", "-O1", "-fno-exceptions", "-Wall", "-Wno-unused", "-Wno-pessimizing-move", "-Wno-self-move", *extra]
    if prob.get("alloc"):
        flags.append("-fno-builtin")
    r = subprocess.run([cxx, *flags, fn, "-o", exe], capture_output=True, text=True)
    if r.returncode != 0:
        return -1, 0, r.stderr[:1800].splitlines()
    lines = []
    failed = 0
    total = 0
    for i, t in enumerate(prob["tests"]):
        total += 1
        if "compiles" in t:
            if not compile_check(prob, code, t, cxx, std):
                failed += 1
                lines.append("FAIL compile check: " + esc(t["compiles"]))
            continue
        try:
            p = subprocess.run([exe, str(i)], capture_output=True, text=True, timeout=20)
            ok = p.returncode == 0 and p.stdout.strip() == "PASS"
            how = "" if ok else ("crash" if p.returncode not in (0, 1) else "wrong")
        except subprocess.TimeoutExpired:
            ok, how = False, "timeout"
        if not ok:
            failed += 1
            lines.append(f"FAIL test {i} ({how}): {esc(t['call'])}")
    return failed, total, lines


def run(prob, compilers=("g++", "clang++"), stds=("c++17", "c++20")):
    allok = True
    for std in stds:
        for cxx in compilers:
            for which, code in (("solution", prob["solution"]), ("starter", prob["starter"])):
                f, n, lines = one(prob, code, which, cxx, std)
                good = (f == 0) if which == "solution" else (f not in (0, -1))
                allok &= good
                tag = {-1: "COMPILE ERROR"}.get(f)
                print(f"[{prob['id']}] {which:8s} {cxx:8s} {std}: " + (tag if tag else f"{f} of {n} failed") + f"   {'OK' if good else 'UNEXPECTED'}")
                if not good or (which == "starter" and cxx == "g++" and std == "c++17"):
                    print("    ", [l for l in lines if l.startswith("FAIL") or "error" in l][:5])
            for name, code in prob.get("mutants", {}).items():
                f, n, lines = one(prob, code, "mut_" + name, cxx, std)
                good = f != 0
                allok &= good
                tag = {-1: "COMPILE ERROR"}.get(f)
                print(f"[{prob['id']}] mutant {name:24s} {cxx:8s} {std}: " + (tag if tag else f"{f} of {n} failed") + f"   {('caught' if f != -1 else 'caught by a compile error') if good else 'NOT CAUGHT'}")
            for name, code in prob.get("alts", {}).items():
                f, n, lines = one(prob, code, "alt_" + name, cxx, std)
                good = f == 0
                allok &= good
                print(f"[{prob['id']}] alt solution {name:20s} {cxx:8s} {std}: {f} of {n} failed   {'OK' if good else 'UNEXPECTED'}")
            if prob.get("ubsan", True) and cxx == "g++":
                f, n, lines = one(prob, prob["solution"], "solution_ubsan", cxx, std, ("-fsanitize=undefined", "-fno-sanitize-recover=all"))
                good = f == 0
                allok &= good
                print(f"[{prob['id']}] solution under -fsanitize=undefined {cxx:8s} {std}: {f} of {n} failed   {'OK' if good else 'UNEXPECTED'}")
                if not good: print("    ", lines[:5])
    return allok
