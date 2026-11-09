"""Reader harness for C++ code items: one program per code variant, each case
selected by argv, built with g++ and clang++ at -O1 -fno-exceptions in C++17
(the engine's standard) and C++20. Values print with %.17g and are compared
as the engine does (isclose: relative 1e-9 and absolute 1e-12 unless the
case's tol says otherwise; equal: exact)."""
import json, math, os, shutil, subprocess, tempfile, time, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
COURSES = ROOT / "app" / "content" / "courses"

SHOW = r'''
#include <cstdio>
#include <type_traits>
#include <vector>
static void __show(double v) { std::printf("%.17g", v); }
static void __show(bool v) { std::printf("%s", v ? "true" : "false"); }
static void __show(int v) { std::printf("%d", v); }
static void __show(long long v) { std::printf("%lld", v); }
template <class T> static void __show(const std::vector<T>& v) {
    std::printf("["); for (size_t i = 0; i < v.size(); ++i) { if (i) std::printf(","); __show(v[i]); } std::printf("]");
}
'''


def item(course, fname, iid):
    for it in json.loads((COURSES / course / fname).read_text())["items"]:
        if it["id"] == iid:
            return it
    raise KeyError(iid)


def compilers():
    return [c for c in ("g++", "clang++") if shutil.which(c)]


def _close(a, e, tol):
    if isinstance(e, list):
        return isinstance(a, list) and len(a) == len(e) and all(_close(x, y, tol) for x, y in zip(a, e))
    rel, ab = 1e-9, 1e-12
    if tol:
        rel = tol.get("rel", 0) or 0
        ab = tol.get("abs", 0) or 0
    return math.isclose(float(a), float(e), rel_tol=rel, abs_tol=ab)


def build(widget, code, cxx, std, tmp, tag):
    cases = widget["examples"] + widget["tests"]
    body = []
    for k, c in enumerate(cases):
        body.append("  if (__k == %d) { %s\n auto __r = (%s); __show(__r); std::printf(\"\\n\"); return 0; }" % (k, c.get("setup", ""), c["call"]))
    src = (widget.get("prelude", "") + "\n" + code + "\n" + SHOW +
           "\n#include <cstdlib>\nint main(int argc, char** argv) { int __k = std::atoi(argv[1]);\n" + "\n".join(body) + "\n return 2; }\n")
    path = os.path.join(tmp, tag)
    open(path + ".cpp", "w").write(src)
    r = subprocess.run([cxx, "-std=" + std, "-O1", "-fno-exceptions", "-w", path + ".cpp", "-o", path], capture_output=True, text=True)
    return path if r.returncode == 0 else None, r.stderr


def run(widget, code, cxx, std="c++17", which="tests"):
    """Returns a list of (status, got, seconds, rel_err) per case of `which`."""
    cases = widget["examples"] + widget["tests"]
    idx = list(range(len(widget["examples"]))) if which == "examples" else list(range(len(widget["examples"]), len(cases)))
    with tempfile.TemporaryDirectory() as tmp:
        exe, err = build(widget, code, cxx, std, tmp, "v")
        out = []
        for k in idx:
            c = cases[k]
            if exe is None:
                out.append(("compile-error", err.splitlines()[0] if err else "", 0, None))
                continue
            t0 = time.time()
            try:
                r = subprocess.run([exe, str(k)], capture_output=True, text=True, timeout=20)
                got = r.stdout.strip()
            except subprocess.TimeoutExpired:
                out.append(("timeout", "", 20, None)); continue
            dt = time.time() - t0
            if r.returncode != 0 or not got:
                out.append(("crash", r.stderr[:80], dt, None)); continue
            a = json.loads(got.replace("nan", "NaN").replace("inf", "Infinity"))
            e = c["expect"]
            if c.get("compare") == "equal":
                ok = a == e
            else:
                ok = _close(a, e, c.get("tol"))
            relerr = None
            if not isinstance(e, list) and isinstance(a, (int, float)) and e != 0:
                relerr = abs(a - e) / abs(e)
            out.append(("pass" if ok else "FAIL", got, dt, relerr))
        return out


def fails(widget, code, cxx, std="c++17"):
    r = run(widget, code, cxx, std)
    return [i + 1 for i, x in enumerate(r) if x[0] != "pass"], r
