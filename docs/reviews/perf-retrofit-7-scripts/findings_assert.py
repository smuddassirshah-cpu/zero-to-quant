"""One check per finding of review-perf-retrofit-7.md. Each FAIL line names a finding
and stays failing until its fix lands; exit 1 while any is open (by design).
Run from this folder with the venv Python."""
import sys, os, subprocess, tempfile
import mpmath as mp
from cpp_harness import item

FAILS = []


def check(cond, fid, msg):
    print(("ok   " if cond else "FAIL ") + f"{fid}: {msg}")
    if not cond:
        FAILS.append(fid)


c1 = item("cpp-pricing", "homework-1.json", "h-perf-corridor")
c2 = item("cpp-pricing", "homework-2.json", "h-perf-yield-tree")
a1 = item("analysis", "homework-1.json", "h-prove-binary-dense")
a3 = item("analysis", "homework-3.json", "h-prove-integral-test")

check("for every corridor." not in c1["prose"], "CP1-1", "prose no longer promises 9 figures for every corridor (narrow ones lose digits)")
check("sit next to 1 and the difference cancels" not in c1["explain"]["text"], "CP1-2", "explain no longer says both values sit next to 1 whenever a > 0")
check("vector" in c2["widget"]["how"], "CP2-1", "how says the tests cannot see the one vector")
check("starting at" in c2["prose"], "CP2-2", "prose says the tree starts at S")
check("These are the numbers a float can hold exactly" not in a1["prompt"], "AN1-1", "prompt no longer says every binary fraction is a float")
check("below" in a1["rubric"][2]["text"], "AN1-2", "rubric row 3 asks for an integer below 2^k a as well")
check("F'" in a3["prompt"] or "fundamental" in a3["prompt"], "AN3-1", "prompt lists the FTC (and existence, a constant) among the facts the model uses")
check("Archimedean" in a3["model"], "AN3-2", "model names the Archimedean property for 1/n -> 0")

# The CP1-1 fix's threshold holds: corridors 0.01% wide keep 9 figures with the shipped solution.
mp.mp.dps = 40
cases = [(100, 140, 140.014, 0.02, 0.1, 0.25), (100, 60, 60.006, 0.02, 0.1, 0.25), (100, 100, 100.01, 0.02, 0.1, 0.25), (250, 400, 400.04, 0.035, 0.28, 0.75)]


def ref(s, lo, hi, r, sig, t):
    s, lo, hi, r, sig, t = map(mp.mpf, (s, lo, hi, r, sig, t))
    dr, v = (r - sig**2 / 2) * t, sig * mp.sqrt(t)
    return mp.exp(-r * t) * mp.quad(mp.npdf, [(mp.log(lo / s) - dr) / v, (mp.log(hi / s) - dr) / v])


main = "#include <cstdio>\nint main(){double c[][6]={" + ",".join("{%r,%r,%r,%r,%r,%r}" % x for x in cases) + "};for(auto&x:c)std::printf(\"%.17g\\n\",corridor_price(x[0],x[1],x[2],x[3],x[4],x[5]));}\n"
with tempfile.TemporaryDirectory() as tmp:
    p = os.path.join(tmp, "w")
    open(p + ".cpp", "w").write(c1["widget"]["solution"] + main)
    subprocess.run(["g++", "-std=c++17", "-O1", "-fno-exceptions", p + ".cpp", "-o", p], check=True)
    got = [float(x) for x in subprocess.run([p], capture_output=True, text=True).stdout.split()]
worst = max(float(abs(g - ref(*c)) / ref(*c)) for g, c in zip(got, cases))
check(worst < 1e-10, "CP1-1 basis", f"corridors 0.01% wide keep 9 figures (worst rel error {worst:.1e})")

print(f"\nopen findings: {len(set(FAILS))}")
sys.exit(1 if FAILS else 0)
