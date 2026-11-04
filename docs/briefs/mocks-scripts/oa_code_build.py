"""mock-oa-code: writes the eight drill files of pack `oa`, their index rows and the mock exam.

Run: python3 -I oa_code_build.py   (standard library only; reads oa_code.py for references and tests).
Run oa_code.py first: it asserts every expected value two ways and writes oa_code_tests.json.
This script re-asserts that every written solution passes every written test and every starter fails one.
"""
import inspect, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oa_code
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CONTENT = os.path.join(ROOT, "app", "content")
T = json.load(open(os.path.join(HERE, "oa_code_tests.json")))

HEADERS = {"oa-merge-cost": "import heapq\n\n\n", "oa-rising-run": "import bisect\n\n\n",
           "oa-decodings": "MOD = 1_000_000_007\n\n\n"}
SKILLS = {"oa-product-windows": ["ci-patterns", "ci-timed"], "oa-rain-water": ["ci-patterns", "ci-timed"],
          "oa-min-jumps": ["ci-patterns", "ci-timed"], "oa-merge-cost": ["ci-timed"],
          "oa-remove-digits": ["ci-strings", "ci-timed"], "oa-rising-run": ["ci-timed"],
          "oa-decodings": ["ci-strings", "ci-timed"], "oa-critical-path": ["ci-timed"]}
REF = {p["id"]: p["ref"] for p in oa_code.P}
SIG = {p["id"]: p["sig"] for p in oa_code.P}

# per drill: returns, the example in words (in the brief), constraints, hint, two example notes, notes
X = {
 "oa-product-windows": dict(
  returns="a whole number",
  words="For `nums = [5]` and `k = 6` the only block is `[5]`, its product 5 is below 6, so the answer is 1.",
  cons=["$0 \\le n \\le 200{,}000$ entries, each a positive whole number.", "$O(n)$ time is the target. Checking every block is too slow.",
        "All tests share a 5-second time limit."],
  hint="Slide a window and keep its product. When the product reaches `k`, shrink from the left. Each right end adds one block per window start.",
  enotes=["Five singles, four pairs and the triple 2, 5, 1 (product 10) are all below 20. That is 10.",
          "The single block `[5]` has product 5, which is below 6."],
  notes=["The window always holds the longest block ending at `right` whose product is below `k`.",
         "Every shorter block ending at `right` also qualifies, so `right - left + 1` blocks are added.",
         "Each entry enters and leaves the window once, so the work is $O(n)$."]),
 "oa-rain-water": dict(
  returns="a whole number",
  words="For `heights = [3, 1, 3]` the middle column holds 2 units between two walls of 3, so the answer is 2.",
  cons=["$0 \\le n \\le 200{,}000$ bars, each at least 0 high.", "$O(n)$ time is the target. Scanning for walls at every bar is too slow.",
        "All tests share a 5-second time limit."],
  hint="Water over a bar rises to the lower of its two walls. Walk inward from both ends and move the side with the lower wall.",
  enotes=["The bars 0, 2 and 0 sit under a level of 3. They hold 3, 1 and 3 units, so 7.",
          "The middle bar is 1 high between two bars of 3, so it holds 2."],
  notes=["The lower end bar limits the water at its side, whatever lies between the ends.",
         "So the side with the lower bar can be settled using only the tallest bar it has met.",
         "Each bar is visited once, so the work is $O(n)$."]),
 "oa-min-jumps": dict(
  returns="a whole number",
  words="For `nums = [1, 1, 1, 1]` each jump moves one place, so reaching position 3 takes 3 jumps.",
  cons=["$0 \\le n \\le 200{,}000$ entries, each at least 0.", "$O(n)$ time is the target. Trying every earlier position is too slow.",
        "All tests share a 5-second time limit."],
  hint="Keep the furthest place reachable so far. When you reach the end of the current jump, you must take another, to that furthest place.",
  enotes=["Jump from 0 to position 3, which holds a 3, then jump 3 places to the end: 2 jumps.",
          "Each entry is 1, so every jump moves one place and the end needs 3 jumps."],
  notes=["`end` marks the last position the current number of jumps can reach.",
         "`far` marks the furthest position one more jump could reach from anywhere inside that range.",
         "Reaching `end` forces a jump to `far`. If `far` has not moved, the end is out of reach."]),
 "oa-merge-cost": dict(
  returns="a whole number",
  words="For `sticks = [4, 4]` there is one join, costing 4 + 4, so the answer is 8.",
  cons=["$0 \\le n \\le 200{,}000$ sticks, each of positive whole length.", "$O(n \\log n)$ time is the target. Scanning for the two shortest sticks each time is too slow.",
        "All tests share a 5-second time limit."],
  hint="A join is counted again in every later join that holds its stick. So always join the two shortest sticks first, using a heap.",
  enotes=["Join 2 and 3 for 5, then 5 and 5 for 10, then 10 and 8 for 18. The total is 5 + 10 + 18 = 33.",
          "There is one join, 4 + 4 = 8."],
  notes=["A stick that is joined early is counted again in every later join that holds it.",
         "So the shortest sticks should sit deepest, joined first, and the heap finds them in $O(\\log n)$.",
         "There are $n - 1$ joins, so the work is $O(n \\log n)$."]),
 "oa-remove-digits": dict(
  returns="a string",
  words="For `digits = \"5291\"` and `k = 2`, removing 5 and 9 leaves \"21\", the smallest two-digit result.",
  cons=["$0 \\le k \\le n \\le 200{,}000$ characters.", "$O(n)$ time is the target. Removing one digit at a time with a scan is too slow.",
        "All tests share a 5-second time limit."],
  hint="A digit that is bigger than the one after it should go. Keep a stack of kept digits and pop while the top is bigger than the new digit.",
  enotes=["Removing 5 and 9 leaves 21, and no other choice of two digits gives a smaller number.",
          "Removing the first 1 leaves 00200, which is the number 200 once the leading zeros go."],
  notes=["A larger digit sitting before a smaller one makes the number bigger, so it is popped first.",
         "If removals are left over, the digits are already rising, so the last ones go.",
         "Strip the leading zeros last, and return \"0\" if nothing is left."]),
 "oa-rising-run": dict(
  returns="a whole number",
  words="For `nums = [5, 5, 5]` a rising run must be strictly increasing, so the longest has length 1.",
  cons=["$0 \\le n \\le 200{,}000$ entries.", "$O(n \\log n)$ time is the target. The quadratic table is too slow.",
        "All tests share a 5-second time limit."],
  hint="Keep, for each length, the smallest last value of any rising run of that length. These stay in order, so each new entry finds its place by binary search.",
  enotes=["The run 4, 8, 9 has length 3, and no rising run of 4 exists.",
          "The run 2, 5, 7, 8 has length 4, and no longer run exists."],
  notes=["`tails[i]` is the smallest last value of any rising run of length `i + 1`.",
         "A new entry replaces the first tail that is not below it. If every tail is below it, the list grows.",
         "Only the length is kept, not the run itself, and each entry costs one $O(\\log n)$ search."]),
 "oa-decodings": dict(
  returns="a whole number",
  words="For `s = \"226\"` the messages are BZ, VF and BBF, so the answer is 3.",
  cons=["$0 \\le n \\le 200{,}000$ digits.", "$O(n)$ time is the target. Listing every message is too slow, and so is recursion without a table.",
        "All tests share a 5-second time limit."],
  hint="Let `ways[i]` count the messages for the first `i` digits. A digit adds `ways[i - 1]` if it is not 0, and a valid pair adds `ways[i - 2]`.",
  enotes=["The three messages are 2|26 (BZ), 22|6 (VF) and 2|2|6 (BBF).",
          "The last 0 cannot stand alone, and 00 is not a letter. So no message fits."],
  notes=["A message for the first `i` digits ends in one digit or a pair. Digits give 1 to 9, pairs 10 to 26.",
         "So `ways[i]` is a sum of two earlier counts, and two variables are enough.",
         "Reduce modulo 1,000,000,007 at each step so the numbers stay small."]),
 "oa-critical-path": dict(
  returns="a whole number",
  words="For three tasks that must run in a loop, no order works, so the answer is -1.",
  cons=["$0 \\le n \\le 100{,}000$ tasks and up to $200{,}000$ pairs.", "$O(n + m)$ time is the target, with $m$ pairs. A recursive search runs out of stack.",
        "All tests share a 5-second time limit."],
  hint="Process tasks in an order where every task comes after the ones it waits for. A task starts when its last prerequisite finishes.",
  enotes=["Task 0 takes 3. Then task 2 takes 4 and task 3 takes 1, so the longest chain is 3 + 4 + 1 = 8.",
          "The three tasks wait on each other in a loop, so none can start."],
  notes=["`start[v]` is the latest finish time among the tasks that must come before `v`.",
         "A task joins the queue when its last prerequisite is done, so a loop never joins it.",
         "If fewer than `n` tasks were processed, there is a loop. Otherwise the answer is the latest finish."]),
}


def build_drill(did, t):
    ref = REF[did]
    src = HEADERS.get(did, "") + inspect.getsource(ref)
    x = X[did]
    brief = f"{t['statement']}\n\nWrite `{SIG[did]}`.\n\nExample. {x['words']}"
    exs = []
    for e, note in zip(t["examples"], x["enotes"]):
        exs.append({"call": e["call"], "expect": e["expect"], "note": note, "compare": "equal"})
    tests = [{"call": r["call"], "expect": r["expect"], "compare": "equal"} for r in t["tests"]]
    n = len(tests)
    d = {"id": did, "name": t["name"], "course": "coding-int", "pack": "oa", "pattern": t["pattern"], "tags": t["tags"],
         "skills": SKILLS[did], "difficulty": t["difficulty"], "pace": t["pace"], "fn": t["fn"], "returns": x["returns"],
         "brief": brief, "constraints": x["cons"], "hint": x["hint"], "starter": t["starter"],
         "examples": exs, "tests": tests,
         "how": f"Submit runs {n} hidden tests. Each answer must equal the expected value.",
         "solution": src, "notes": x["notes"]}
    return d


def verify(d):
    for label, code in (("solution", d["solution"]), ("starter", d["starter"])):
        ns = {}
        exec(code, ns)
        fails = 0
        for r in d["tests"]:
            t0 = time.time()
            try:
                ok = eval(r["call"], ns) == eval(r["expect"])
            except Exception:
                ok = False
            if label == "solution":
                assert ok, (d["id"], r["call"])
                assert time.time() - t0 < 1.0, (d["id"], r["call"])
            fails += (not ok)
        if label == "starter":
            assert fails >= 1, d["id"]
            print(f"  {d['id']}: starter fails {fails} of {len(d['tests'])}")
        else:
            print(f"  {d['id']}: solution passes {len(d['tests'])} of {len(d['tests'])}")
    for e in d["examples"]:
        assert any(e["call"] == r["call"] and e["expect"] == r["expect"] for r in d["tests"])


def dump(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    idx_path = os.path.join(CONTENT, "drills", "index.json")
    idx = json.load(open(idx_path))
    have = {r["id"] for r in idx}
    for did, t in T.items():
        d = build_drill(did, t)
        verify(d)
        dump(d, os.path.join(CONTENT, "drills", did + ".json"))
        if did not in have:
            idx.append({"id": did, "name": t["name"], "course": "coding-int", "difficulty": t["difficulty"]})
    dump(idx, idx_path)

    exam = {
        "id": "mock-oa-code", "name": "Coding assessment", "style": "developer",
        "models": "Reported, as of Nov 2026: online coding tests at JP Morgan, Two Sigma and Goldman Sachs. Two Python algorithm problems in 60 minutes, for quant, software and strats roles.",
        "description": ("This is the reported format of an online coding assessment, as candidates described it by Nov 2026. "
                        "You have two algorithm problems in 60 minutes and write both in Python. The first is medium and the second is harder. "
                        "Hidden tests include large inputs, so a slow answer fails them. A problem scores only when all its hidden tests pass. "
                        "The results panel lists each test, so use it to see how far you got. "
                        "The two problems are drawn afresh from a pool each time you sit. The pool is also in the drill library. "
                        "Use no search engine and no notes. Read both statements and plan your minutes first."),
        "skills": {"ci-patterns": "Further patterns", "ci-strings": "Strings and simulation", "ci-timed": "Solving under time"},
        "parts": [
            {"kind": "paper", "id": "code", "name": "Two problems in sixty minutes", "minutes": 60,
             "scoring": {"right": 1, "wrong": 0, "blank": 0}, "pass": 0.5, "items": [],
             "draw": [{"from": "drills/oa", "difficulty": 3, "n": 1}, {"from": "drills/oa", "difficulty": 4, "n": 1}]},
            {"kind": "check", "id": "plan-first", "name": "I read both statements and planned my minutes before I wrote code",
             "detail": "Tick this only if you spent the first five minutes reading and noting the constraints."},
            {"kind": "check", "id": "no-lookup", "name": "I used no search engine and no notes",
             "detail": "Tick this only if you sat the whole paper without either."},
        ]}
    assert len(exam["models"]) < 200, len(exam["models"])
    dump(exam, os.path.join(CONTENT, "exams", "mock-oa-code.json"))
    print("BUILT: 8 drills, mock-oa-code")


if __name__ == "__main__":
    main()
