# Assembles docs/briefs/cpp.md from the hand-written parts and the problem modules (so no starter, solution or test is retyped).
# Usage: python3 run_all.py > build/all_out.txt 2>&1 ; python3 number_checks.py > build/numbers_out.txt ; python3 build_brief.py
import os, re, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

META = {
    "P-move-buffer": dict(where="`l19-moving-not-copying`, screen 6 (ladder), a `code` screen, difficulty 3", flags="allocCheck: true, leakCheck: true",
        how="Submit runs 15 hidden tests. `alloc_count()` counts calls to `operator new` and `new[]` since the last reset. A move that copies shows as 1 instead of 0. A block never freed fails its test. A moved-from buffer must report size 0 and `data()` null.",
        note="Extends the l11 `Buffer(int n, double x)` (say \"the l11 `Buffer`\" in the prose): l11 asked for `= default` moves, here the learner writes them. The commonest slip, a move that zeroes the size but leaves the pointer set (so two buffers `delete[]` one block), is caught by the two `data() == nullptr` tests, not by the allocator: the app's allocator frees twice silently, and `leakCheck` does not see a double free. The starter comment says the move assignment must be safe for `a = std::move(a)`. A test of `std::vector<Buffer>` growth reads the allocation count: 2 with a `noexcept` move (the new block and the temporary), 4 when the move is not `noexcept` (the two old elements are copied) and 5 when there is no move at all (checked by `check_growth_allocs.py`)."),
    "P-copy-samples": dict(where="`l20-rule-of-five`, screen 6 (ladder), a `code` screen, difficulty 3", flags="allocCheck: true, leakCheck: true",
        how="Submit runs 13 hidden tests. `alloc_count()` counts calls to `operator new` and `new[]`: a copy must allocate once. A block never freed fails its test.",
        note="WAITING ON AN ENGINE ITEM. A delete-first assignment (`delete[] data_; data_ = new double[n]; copy from other`) misbehaves only for `a = a`, by reading the block it has just freed. No test can make that read deterministic: the app's allocator leaves the old contents in place, so the copy usually succeeds and the slip passes 13 of 13 in the app (it was caught natively only because glibc overwrote the block). The `a = a` test therefore stays as a well-defined check that a correct solution keeps its data, and the slip is listed as not caught. It needs the harness to poison freed blocks or to expose the order of `new` and `delete`: the [Must] under \"Raised later (cpp L5 brief, 5 Nov)\" in `docs/BACKLOG-INBOX.md`. Do not describe `a = a` to the learner as exposing delete-first."),
    "P-hand-vtable": dict(where="`l21-virtual-dispatch`, screen 6 (ladder), a `code` screen, difficulty 3", flags="leakCheck: true",
        how="Submit runs 11 hidden tests. Each call goes through the object's own table; two objects of one kind must share one table.", note="Function mode; the tests build the objects in `setup`."),
    "P-add-overflows": dict(where="`l22-undefined-behaviour`, screen 5 (ladder), a `code` screen, difficulty 3", flags="none",
        how="Submit runs 13 hidden tests. Each answer is `true` when `a + b` does not fit in an `int`. Every test uses values the correct check handles without overflowing.",
        note="Do not set `compare: \"raises\"`. Tests only use `INT_MAX`, `INT_MIN` and nearby values; a widening solution (`long long` sum) passes too, which is checked. The starter fails whatever the compiler does with its undefined line. A learner's post-check solution (`int s = a + b; return (b > 0 && s < a) || (b < 0 && s > a);`) is another matter: it fails 7 of 13 in the app (clang 21 `-O1` folds the check) and passes 13 of 13 under g++ 13 `-O1`. Whether an undefined solution is caught depends on the optimiser, so the hidden tests double as an optimiser test: say so in the author's notes and in l22 S5's explain, and promise no failing row for every undefined solution."),
    "P-unique-ptr": dict(where="`l23-own-smart-pointer`, screen 3 (ladder), a `code` screen, difficulty 3", flags="leakCheck: true",
        how="Submit runs 15 hidden tests. A hidden `Tracked` type counts live objects, so an object deleted twice or never shows in the count. Two compile checks fail if copying is allowed.",
        note="Two of the 15 are `compiles` cases (they pass when the snippet does not compile). A file with an unrelated compile error shows that error and no rows, so the `how` must not say the checks \"confirm\" anything on such a file. The starter comment says the move assignment must be safe for `a = std::move(a)`; the self-move test reads the pointer value (non-null), never freed memory."),
    "P-shared-ptr": dict(where="`l23-own-smart-pointer`, screen 6 (ladder), a `code` screen, difficulty 3", flags="leakCheck: true",
        how="Submit runs 15 hidden tests. A hidden `Tracked` type counts live objects; `leakCheck` also fails a test whose counter block is never freed.",
        note="The counter is a heap `long` shared by all owners (`new long(1)` is already in the starter's constructor)."),
    "P-scope-guard": dict(where="`homework-5`, item 1, a `code` item, difficulty 4", flags="leakCheck: true",
        how="Submit runs 12 hidden tests. The callbacks write to a hidden counter and a hidden string. Two compile checks fail if copying or assignment is allowed.",
        note="`postlude` holds `make_guard()`, which returns a guard by value. Two of the 12 are `compiles` cases. This is interview recall of the l11 `Connection` (destructor, copying deleted, an inert moved-from object) with a `std::function` callback; the prompt says so, and the new part is the `std::vector<ScopeGuard>` growth test."),
    "P-vec": dict(where="`homework-5`, item 2, a `code` item, difficulty 5", flags="allocCheck: true, leakCheck: true",
        how="Submit runs 15 hidden tests. `alloc_count()` counts calls to `operator new` and `new[]`: 1,000 pushes must allocate 11 times. A hidden `Counted` type counts copies, moves and live objects. It also counts any copy or move made from a destroyed object (`Counted::bad`).",
        note="`Counted` has no default constructor and no assignment, which forces raw storage and placement new. It keeps a table of the addresses of its live objects (no heap use) and never reads a source that is not in the table, so `v.push_back(v[0])` is tested by `Counted::bad` and the copied value, with no read of freed memory: a growth that destroys the old elements before copying the argument gives `bad` 1 and fails. The starter comment tells the learner that copy assignment must be safe for `a = a` and that a template `U&&` helper can serve both `push_back` overloads."),
    "P-clone-basket": dict(where="exam item `e-code-clone-basket` (see the exam section), a `code` item, difficulty 4", flags="leakCheck: true",
        how="Submit runs 12 hidden tests. Costs are compared with `isclose`.", note="Function mode. `leakCheck` is on so that a raw `new` that is never deleted is caught (every owner in a normal solution is a `unique_ptr`). Tests that clone and then change the original check that the copy is deep."),
}
ORDER = [("problems_l19", "P-move-buffer"), ("problems_l20", "P-copy-samples"), ("problems_l21", "P-hand-vtable"), ("problems_l22", "P-add-overflows"),
         ("problems_l23", "P-unique-ptr"), ("problems_l23", "P-shared-ptr"), ("problems_hw", "P-scope-guard"), ("problems_hw", "P-vec"), ("problems_exam", "P-clone-basket")]

def results():
    txt = open(os.path.join(HERE, "build", "all_out.txt")).read().splitlines()
    return [l for l in txt if l.startswith("[P-")]

def app_lines():
    """lines of results_app.txt, annotated: solution passes, starter fails, mutants caught, known gaps named as such"""
    fn = os.path.join(HERE, "results_app.txt")
    if not os.path.exists(fn): return []
    out = []
    for l in open(fn).read().splitlines():
        m = re.match(r"(\[P-[^\]]+\]) (c\+\+\d+) (\S+): (\d+) of (\d+) failed", l)
        if not m: continue
        pid, std, who, f, n = m.group(1), m.group(2), m.group(3), int(m.group(4)), int(m.group(5))
        kind = who.split(":")[0]
        if kind == "solution": tag = "OK" if f == 0 else "UNEXPECTED"
        elif kind == "starter": tag = "OK" if f > 0 else "UNEXPECTED"
        elif kind == "alt": tag = "OK" if f == 0 else "UNEXPECTED"
        elif kind == "unc": tag = "not caught (known gap)" if f == 0 else "caught (not relied on)"
        else: tag = "caught" if f > 0 else "NOT CAUGHT"
        out.append(f"{pid} {std} {who}: {f} of {n} failed  {tag}")
    return out

def get_problem(mod, pid):
    m = importlib.import_module(mod)
    for P in (m.PROBLEMS if hasattr(m, "PROBLEMS") else [m.P]):
        if P["id"] == pid: return P
    raise KeyError(pid)

def fmt_test(t):
    exp = t["expect"]
    e = "true" if exp is True else "false" if exp is False else (f'"{exp}"' if isinstance(exp, str) else repr(exp))
    if "compiles" in t:
        s = f"- compiles: `{t['compiles']}`" + (f" (with `{t['setup']}`)" if t.get("setup") else "") + f" expects `{e}` (it must not compile)"
        return s
    cmp_ = "isclose" if isinstance(exp, float) else "equal"
    s = "- `" + (t["setup"] + " " if t.get("setup") else "") + t["call"] + "` expects `" + e + "` (`" + cmp_ + "`)"
    return s

def section(pid, mod, lines):
    P = get_problem(mod, pid); M = META[pid]
    mine = [l for l in lines if l.startswith(f"[{pid}]")]
    out = [f"### {pid}", ""]
    out.append(f"Where: {M['where']}. Widget `code`, `language: \"cpp\"`, {len([t for t in P['tests']])} hidden tests (function mode, `compare: \"equal\"` for integers, booleans and strings, `isclose` for doubles). Flags: {M['flags']}. `examples` are the first two tests.")
    out.append("")
    out.append(f"`how`: \"{M['how']}\"")
    out.append("")
    if P.get("prelude"):
        out += ["Hidden `prelude`:", "", "```cpp", P["prelude"].rstrip(), "```", ""]
    if P.get("postlude"):
        out += ["Hidden `postlude`:", "", "```cpp", P["postlude"].rstrip(), "```", ""]
    out += ["Starter (the learner sees this; it compiles and fails the tests):", "", "```cpp", P["starter"].rstrip(), "```", ""]
    out += ["Reference solution:", "", "```cpp", P["solution"].rstrip(), "```", ""]
    out += ["Hidden tests (`setup` then `call`, with its `expect`):", ""] + [fmt_test(t) for t in P["tests"]] + [""]
    out.append(f"Note: {M['note']}")
    out.append("")
    # pass lines
    sol = [l for l in mine if " solution " in l and "sanitize" not in l and "alt" not in l and "mutant" not in l and "starter" not in l]
    sta = [l for l in mine if " starter " in l]
    mut = [l for l in mine if " mutant " in l]
    alt = [l for l in mine if "alt solution" in l]
    ub = [l for l in mine if "sanitize" in l]
    out.append("Checked by `docs/briefs/cpp-scripts/run_all.py` (each test as its own process, as the app runs them; `-O1 -fno-exceptions`):")
    out.append("")
    out.append("```text")
    for l in sol + sta: out.append(re.sub(r"\s+", " ", l.replace("   OK", "  OK")))
    for l in alt + ub: out.append(re.sub(r"\s+", " ", l.replace("   OK", "  OK")))
    out.append("```")
    out.append("")
    names = sorted(set(re.match(r"\[[^\]]+\] mutant (\S+)", l).group(1) for l in mut))
    caught = sum(1 for l in mut if "caught" in l and "NOT" not in l)
    out.append(f"Plausible learner slips (mutants of the solution), each failing at least one test in every native compiler and standard (caught {caught} of {len(mut)} runs): " + ", ".join(f"`{n}`" for n in names) + ".")
    out.append("")
    unc = sorted(set(re.match(r"\[[^\]]+\] known-uncaught (\S+)", l).group(1) for l in mine if "known-uncaught" in l))
    if unc:
        out.append("Known gap, not counted as caught: " + ", ".join(f"`{n}`" for n in unc) + " (see the note above; it waits on the [Must] in `docs/BACKLOG-INBOX.md`).")
        out.append("")
    app = [l for l in app_lines() if l.startswith(f"[{pid}]")]
    if app:
        out.append("Checked in the app's own toolchain (`cpp-scripts/app_toolchain/`: YoWASP clang 21, libc++ in debug hardening, the app's own `unit()` from `cpp-grade.js`, its `leakCheck` and `allocCheck` wrappers, one process per test, `-std=c++17` and `-std=c++20` at `-O1`), `results_app.txt`:")
        out.append("")
        out.append("```text")
        out += app
        out.append("```")
        out.append("")
    return out

def main():
    lines = results()
    bad = [l for l in lines if "UNEXPECTED" in l or "NOT CAUGHT" in l or "COMPILE ERROR" in l and "caught" not in l]
    bad += [l for l in app_lines() if "UNEXPECTED" in l or "NOT CAUGHT" in l]
    if bad:
        print("PROBLEMS IN RESULTS:"); [print(" ", b) for b in bad]; sys.exit(1)
    p1 = open(os.path.join(HERE, "part1-level5.md")).read().rstrip() + "\n"
    p2 = open(os.path.join(HERE, "part2-exam.md")).read().rstrip() + "\n"
    out = ["Levels 1 to 4 of `cpp` predate briefs; this file starts at level 5.", "", p1, p2]
    out += ["## Code problems", "",
            "Nine problems with hidden tests: six in lessons (l19 to l23, two in l23), two in `homework-5` and one in the exam extension. Each is in `docs/briefs/cpp-scripts/` as `<id>_starter.cpp`, `<id>_solution.cpp` and `<id>_tests.json`, produced from `problems_*.py` by `run_all.py`. `harness.py` mimics the app's function mode: a hidden prelude, the learner's code, a hidden postlude, then one block per test (the `setup`, then the `call` as a value), each run as its own process; it adds a counter header for `allocCheck` and a live-block count per test for `leakCheck`; a `compiles` case is a `-fsanitize`-free `-fsyntax-only` compile of the snippet in a function after the code. Every starter compiles and fails; every solution passes all tests with g++ 13.3 and clang++ 18.1 at `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`, and is clean under `-fsanitize=undefined` with g++ (the clang sanitiser runtime is not installed here). Native runs are not enough: the app's allocator frees a block twice without complaint and leaves freed memory readable, where glibc aborts, so a slip that only the native allocator catches is not caught. Every problem is therefore also run in the app's own toolchain (`app_toolchain/`, results in `results_app.txt`) and a slip counts as caught only if the app run fails a test. No test reads freed memory or relies on the allocator noticing a mistake. Expected values come from a hand derivation or the independent model in `number_checks.py`; the harness reports a test as failed when it fails, crashes or times out.", "",
            "Every starter fails at least 6 of its tests in every run listed below, so the first Check shows a real list of red rows.", ""]
    for mod, pid in ORDER:
        out += section(pid, mod, lines)
    out += ["## Number checks", "",
            "Every figure in the lessons, review, homework and exam is computed twice. Source 1 is `cpp-scripts/number_checks.py`, a Python model that shares no code with the C++ (output below); source 2 is the native run or the hidden test named beside it.", "",
            "```text"] + open(os.path.join(HERE, "build", "numbers_out.txt")).read().rstrip().splitlines() + ["```", "",
            "Second sources, run natively with g++ 13.3 and clang++ 18.1 (libstdc++; see the runtime-facts note about libc++):", "",
            "- Copy and move counts in l19 and the exam: `cpp-scripts/facts_l19.cpp` prints copies and moves for sixteen snippets (identical under both compilers: `Tracked b = a;` 1 copy; `Tracked b = std::move(a);` 1 move; `std::move(a);` alone 0 and 0; `make()` 0 and 0; `return std::move(t)` 1 move; a `const` source 1 copy; `take(a)` 1 copy; `take(std::move(a))` 1 move; `take(Tracked(1))` 0 and 0; four pushes with a `noexcept` move 0 copies and 7 moves; two pushes with a throwing move 1 copy and 2 moves). `facts_misc.cpp` checks 3 copies and 4 moves for four pushes with a throwing move.",
            "- The special-members table in l20: `cpp-scripts/special_members.cpp` prints it (same under both compilers); the l20 and homework keys are read from it.",
            "- Layout facts in l21: `cpp-scripts/wasm_sizes.cpp` compiles with `clang++ --target=wasm32-unknown-wasi -fsyntax-only` (pointer 4; one virtual and an `int` 8; two virtuals still 8; derived with two `int`s 12; `Quote` 24); the same file fails five static assertions on a 64-bit target, as the lesson says (16, 16 and so on).",
            "- Undefined-behaviour facts in l22: `ub_asm.cpp` (wasm32 `-O1` output, and x86-64) and `ub_facts.cpp` (the sanitiser lines; the unsigned wrap prints 0).",
            "- Smart-pointer facts in l23: `facts_misc.cpp` counts allocations (`shared_ptr<int>(new int)` 2, `make_shared<int>` 1) and sizes (`unique_ptr` one pointer, `shared_ptr` two); the `Vec` counts (11 allocations, capacity 1,024, 15 moves) are tested by P-vec and modelled in `number_checks.py`.",
            "- Fix-pass facts: `cpp-scripts/facts_fixpass.cpp` prints `1 0` (a defaulted move is `noexcept`, a hand-written one without the keyword is not: l20 S4 and review 4), `order move 0 copy 0` (l20 S8: `is_move_constructible` is false because the deleted copy constructor is chosen), `gone 1` (`e-virtual-dtor`: `shared_ptr<Base>` from `make_shared<Derived>` runs `~Derived`), `c=0` and `b=0` (the two defined lines of `e-ub-which`). The homework 8 growth copy, 1,000 x 1,000 x 8 = 8,000,000 bytes, is in `number_checks.py`.",
            "- Exam: 3 copies for four pushes with a throwing move (model and native); the three `e-ub-which` keys by rule.", ""]
    path = os.path.normpath(os.path.join(HERE, "..", "cpp.md"))
    open(path, "w").write("\n".join(out))
    print("wrote", path, len("\n".join(out).splitlines()), "lines")

main()
