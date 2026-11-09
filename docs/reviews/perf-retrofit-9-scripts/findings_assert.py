"""One check per finding of review-perf-retrofit-9. Exits 1 while any finding is open, by design: each FAIL line
names a finding and stays failing until its fix lands. Basis lines print the evidence. Run from this folder with the
venv Python."""
import json, pathlib, re, sys
from decimal import Decimal, ROUND_HALF_UP
ROOT = pathlib.Path(__file__).resolve().parents[3] / "app" / "content" / "courses"
def item(c, n, iid):
    return next(x for x in json.loads((ROOT / c / f"homework-{n}.json").read_text())["items"] if x["id"] == iid)
openf = 0
def finding(fid, fixed, basis):
    global openf
    print(("closed " if fixed else "FAIL   ") + fid + "  basis: " + basis)
    openf += 0 if fixed else 1

for fid, n, iid in (("LT1-1", 1, "h-prove-capped-wait"), ("LT2-1", 2, "h-prove-cycles-exponential"), ("LT3-1", 3, "h-prove-desk-guarantee")):
    it = item("limits-thm", n, iid)
    opt = [i + 1 for i, r in enumerate(it["rubric"]) if not r.get("required")]
    finding(fid, bool(re.search(r"optional", it["prompt"], re.I)) or not opt,
            f"rubric rows {opt} not required; the prompt asks for that part without marking it optional (DECISIONS Session X)")

it = item("limits-thm", 2, "h-prove-cycles-exponential")
finding("LT2-2", bool(re.search(r"true time plus|plus \$D\$|reported time is|minus the true", it["prompt"])),
        "'off from the true time by D seconds' leaves the sign of D open; the model reads D as reported minus true ('reports run 30 ms late')")

it = item("limits-thm", 3, "h-prove-desk-guarantee")
m = it["model"]
finding("LT3-2", ("Bin" in m or "binomial" in m and "W_" in m) and "no continuity correction" not in m,
        "exact P(S<=0) = P(W_A + 2W_B <= n), W_A ~ Bin(n,0.55), W_B ~ Bin(n,0.3) independent: 0.0528 at n=131, 0.05005 at 135, 0.0494 at 136, "
        "below 0.05 for every n from 136 to 1,000; normal 0.0499 at 131; with a continuity correction the normal asks 138 (lt_numbers.py)")

it = item("pytest", 3, "h3-fee-test-first")
def half_case(call):
    mm = re.fullmatch(r"broker_fee\(([\d_.]+)\)", call)
    if not mm:
        return False
    x = float(mm.group(1))
    f = Decimal(repr(x)) / 1000
    hu = float(f.quantize(Decimal("0.01"), ROUND_HALF_UP))
    return f == f.quantize(Decimal("0.001")) and str(f).endswith("5") and round(x * 0.001, 2) != hu
finding("PT3-1", any(half_case(t["call"]) for t in it["widget"]["tests"]),
        "no hidden test calls broker_fee on a half-penny fee that float round() gets wrong; "
        f"round(5005 * 0.001, 2) = {round(5005 * 0.001, 2)} against 5.01 (pt_three.py: the float-round planted file passes all 15)")
finding("PT3-2", bool(re.search(r"whole pence|whole number of pence", it["prose"])),
        "the shipped solution rounds the notional to the penny first: broker_fee(12344.996) gives 12.35, the rule gives 12.34")
finding("PT3-3", "cannot see" in it["widget"]["how"] or "by reading" in it["widget"]["how"],
        "weak() runs only against the stub, so a file with one real test and two 'is not None' tests passes all 15 (pt_three.py)")

it = item("pytest", 1, "h-average-cost-tests")
finding("PT1-1", "cannot see" in it["widget"]["how"] or "by reading" in it["widget"]["how"],
        "one test copied three times, and an oracle that copies the formula, both pass all 12; arrange, act, assert order is unseen")
finding("PT1-2", bool(re.search(r"empty|leaves open", it["feedback"]["byKey"]["test-3"])),
        "a test that empty fills raise ZeroDivisionError fails only on right_running (returns 0.0), and test-3 then blames rounding")

it = item("pytest", 2, "h2-curve-properties")
finding("PT2-1", "cannot see" in it["widget"]["how"] or "by reading" in it["widget"]["how"],
        "three tests over one table of five hand-worked curves, with no rule, pass all 14 (pt_three.py)")
print("open findings:", openf)
sys.exit(1 if openf else 0)
