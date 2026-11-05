# Confirms the allocation counts quoted for the std::vector<Buffer> growth test of P-move-buffer:
# 2 with the solution, 4 with a move that is not noexcept, 5 with copy members only (the starter).
import sys, os, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness
import problems_l19 as m
P = dict(m.P)
test = [t for t in P["tests"] if "v.push_back(Buffer(100, 3.0))" in t.get("setup", "")][0]
P["tests"] = [dict(test, expect=0)]            # expect 0 so the printed program says nothing useful; we read the value instead
for name, code in (("solution", P["solution"]), ("no-noexcept", P["mutants"]["no-noexcept"]), ("starter (copy only)", P["starter"])):
    src = harness.PRE + harness.ALLOC + P["prelude"] + code + "\nint main(){ " + test["setup"] + " std::printf(\"%d\\n\", alloc_count()); }\n"
    d = tempfile.mkdtemp(dir=harness.BUILD)
    fn = d + "/g.cpp"; open(fn, "w").write(src)
    subprocess.run(["g++", "-std=c++17", "-O1", "-fno-exceptions", "-fno-builtin", fn, "-o", d + "/g"], check=True)
    print(f"{name:22s} allocations for the third push_back: " + subprocess.run([d + "/g"], capture_output=True, text=True).stdout.strip())
