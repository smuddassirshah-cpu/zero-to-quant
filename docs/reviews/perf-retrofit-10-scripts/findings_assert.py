"""One check per finding of review-perf-retrofit-10. Each FAIL line names a finding that is still open; the script
exits 1 until every fix has landed (then 0). Run from this folder with any Python 3, -I."""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[3] / "app" / "content" / "courses"


def item(course, n, iid):
    return next(x for x in json.loads((ROOT / course / f"homework-{n}.json").read_text())["items"] if x["id"] == iid)


def optional_ok(it):
    """Every row without required: true has its part marked optional in the prompt (the [perf-optional-row] rule)."""
    text = " ".join(it.get(k, "") for k in ("prose", "question", "prompt")) + " " + it.get("widget", {}).get("prompt", "")
    loose = [r for r in it["rubric"] if r.get("required") is not True]
    return not loose or re.search(r"optional", text, re.I) is not None


open_ = 0


def check(fid, ok, what):
    global open_
    print(("closed " if ok else "FAIL   ") + fid + ": " + what)
    open_ += 0 if ok else 1


i1 = item("integrals", 1, "h-derive-falling-area")
i2 = item("integrals", 2, "h-derive-window")
i3 = item("integrals", 3, "h-derive-parts-tail")
l1 = item("linear-maps", 1, "h-prove-extend-basis")
l2 = item("linear-maps", 2, "h-prove-commutator-rank")
o3 = item("options", 3, "h-derive-box")
t1 = item("trees", 1, "h-derive-one-step")

check("IN1-1", optional_ok(i1), "integrals L1 row 1 optional with no part marked optional")
check("IN2-1", optional_ok(i2), "integrals L2 row 1 optional with no part marked optional")
check("IN3-1", optional_ok(i3), "integrals L3 row 2 grades a point the prompt never asks")
check("IN1-2", "A split into pieces set up the same way counts." not in i1["rubric"][0]["text"], "integrals L1 row 1 credits a split route rows 2 and 5 cannot accept")
check("IN3-2", "leaves a harder integral" not in i3["model"] and "any correct route" in i3["rubric"][2]["text"], "integrals L3 other split called harder; row 3 names two routes only")
check("IN2-2", "reaches $e^{-3x^2/2} = \\tfrac12$" not in i2["rubric"][3]["text"] or "any route" in i2["rubric"][3]["text"], "integrals L2 row 4 worded by one route")
check("IN2-3", "Nothing else about $f$ is needed" not in i2["model"] or "for $A$ to exist" in i2["model"], "integrals L2 continuity also makes A exist")
check("IN2-4", "No formula exists" not in i2["prompt"], "integrals L2 'no formula' should be 'no elementary formula'")
check("LM1-1", "found from $a_1 = -2a_2 - 4a_3$" not in l1["rubric"][1]["text"] or "for example" in l1["rubric"][1]["text"], "linear-maps L1 row 2 worded by one route")
check("LM2-1", "T(\\mathbf{E}_{21}) + (a + b - d)" in l2["rubric"][2]["text"], "linear-maps L2 row 3 accepts only the kernel-terms route to spanning")
check("OP3-1", "£0.55" in o3["rubric"][3]["text"], "options L3 rows 2 and 4 accept only the cash-today trade")
check("OP3-2", "sold short" in o3["model"].split("**3. Check by parity.**")[1].split("**4.")[0], "options L3 parity's short-sale assumption unstated")
check("TR1-1", "short" in t1["prompt"].split("(a)")[0], "trees L1 prompt states no borrowing or short-sale assumption")
check("TR1-2", "pays something in both states" not in t1["model"], "trees L1 'lends because it pays in both states' is not the reason")
print(f"{open_} open")
sys.exit(1 if open_ else 0)
