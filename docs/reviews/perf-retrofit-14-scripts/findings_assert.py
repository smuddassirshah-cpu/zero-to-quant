"""One line per finding of review-perf-retrofit-14: FAIL while the finding is open, ok once its fix is in.
Written in the fix pass. Text checks only; cpp14.py part E and py14.py grade the changed code natively.
Run with any Python 3."""
import json, pathlib, sys
C = pathlib.Path(__file__).resolve().parents[3] / "app" / "content" / "courses"


def load(course, name):
    return json.loads((C / course / name).read_text())


def item(course, name, iid):
    return next(x for x in load(course, name)["items"] if x["id"] == iid)


L = load("cpp", "l23-own-smart-pointer.json")["screens"]
r5 = item("cpp", "review-5.json", "r5-unique-move-assign")
h5 = item("cpp", "homework-5.json", "h5-shared-move-assign")
sc = item("cpp", "homework-5.json", "h5-sole-and-counted")
pf = item("py-found", "homework-4.json", "h4-sweep-offers")
gt = item("git", "homework-3.json", "h-ignore-options-repo")
tm = item("terminal", "homework-1.json", "h-perf-fx-paths")
fp = item("first-python", "homework-2.json", "h-split-bill")
lines = lambda w: {l["id"]: l["text"] for l in w["lines"]}
u = L[2]["widget"]["solution"]
u = u[u.index("UniquePtr& operator=(UniquePtr&& other)"):]   # the move assignment onwards
s5 = L[5]["widget"]["solution"]
checks = [
    ("CP5-1 screens[2] move takes the source before delete", u.index("T* p = other.ptr_;") < u.index("other.ptr_ = nullptr;") < u.index("delete ptr_;") < u.index("ptr_ = p;")),
    ("CP5-1 screens[2] list test and Link postlude", "h = std::move(h->next)" in L[2]["widget"]["tests"][-1]["setup"] and "struct Link" in L[2]["widget"]["postlude"]),
    ("CP5-1 screens[2] hint and explain own the source first", "owns `p` first" in L[2]["hints"][2]["text"] and "nulls the source, then deletes the old object" in L[2]["explain"]["text"]),
    ("CP5-1 screens[4] reads other into locals", "into locals" in lines(L[4]["widget"])["s1"] and "head = head->next" in L[4]["explain"]["text"]),
    ("CP5-1 screens[5] copy and move read other before drop()", s5.count("T* p = other.ptr_;") == 2 and s5.index("long* c = other.count_;") < s5.index("drop();\n            ptr_ = p;")),
    ("CP5-1 screens[5] two list tests", [t["expect"] for t in L[5]["widget"]["tests"][-2:]] == [211, 211]),
    ("CP5-1 screens[7] takes a's share, then drops b's", L[7]["explain"]["text"].startswith("The move assignment takes `a`'s pointers") and L[7]["widget"]["answer"] == 1),
    ("CP5-2 r5 key: take, null, free, keep", [lines(r5["widget"])[x] for x in r5["widget"]["answer"]] == ["`if (this != &other) {`", "`T* p = other.ptr_;`", "`other.ptr_ = nullptr;`", "`delete ptr_;`", "`ptr_ = p;`", "`return *this;`"]),
    ("CP5-2 r5 unsafe order keyed s4, names the slip", "too early" in r5["feedback"]["byKey"].get("s4", "") and r5["widget"]["after"]["s4"] == ["s3"]),
    ("CP5-2 h5 key: take, empty, drop, keep", h5["widget"]["answer"] == ["s1", "s2", "s3", "s4", "s5"] and "into locals" in lines(h5["widget"])["s2"] and lines(h5["widget"])["s4"].startswith("drop own count")),
    ("CP5-2 h5 old d2 gone; new d2 adds one", lines(h5["widget"])["d2"] == "add one to the count you took" and "too early" in h5["feedback"]["byKey"].get("s4", "")),
    ("CP5-3 SolePtr move releases the source first", sc["widget"]["solution"].index("T* taken = other.release();") < sc["widget"]["solution"].index("T* old = ptr_;")),
    ("CP5-3 test 3 adds the self-move, expect 111", sc["widget"]["tests"][2]["setup"].endswith("SolePtr<Quote>& r = b; b = std::move(r);") and sc["widget"]["tests"][2]["expect"] == 111),
    ("CP5-3 prose names a = std::move(a)", "(for a `SolePtr`, `a = std::move(a)`)" in sc["prose"]),
    ("PF4-1 test 7 checks the generator type", pf["widget"]["tests"][6]["expect"] == "((4.50, 100), 'generator')" and "type(sweep_offers" in pf["widget"]["tests"][6]["call"]),
    ("PF4-1 byKey test-7 names iter of a list", "or `iter` of one" in pf["feedback"]["byKey"]["test-7"]),
    ("GT3-1 the ! rule names the ignored-folder exception", "It does nothing when a folder above them is itself ignored." in gt["prose"]),
    ("TM1-1 explain says Linux reads raw as another name", "Linux reads `raw` as another name" in tm["explain"]["text"]),
    ("TM1-2 refusal no longer says a path from the top only goes down", "only goes down" not in tm["widget"]["prelude"] and "name each folder on the way down" in tm["widget"]["prelude"]),
    ("FP2-1 byKey test-1 reads 'If the row shows'", "If the row shows TypeError" in fp["feedback"]["byKey"]["test-1"] and "; if None" in fp["feedback"]["byKey"]["test-1"]),
]
bad = 0
for name, ok in checks:
    print(("ok   " if ok else "FAIL ") + name)
    bad += not ok
print("open findings: %d" % bad)
sys.exit(1 if bad else 0)
