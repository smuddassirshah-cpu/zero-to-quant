"""Fix-pass read, contests level 4 round 3 (commit 51c05b3e). Run from the repo root:
  python docs/reports/contests-L4-fixread-r3.py <pkgs> [scratch dir]
1. Expected values of l13 test 12, l14 test 4 and l15 test 3 by brute force, independent of the model solutions.
2. Natural codings of the mistake each changed test-N line names, graded by the page's harness under Pyodide
   (app/tools/code-runner.mjs); each must first fail the test named here. Exits 0 when all agree."""
import itertools, json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(ROOT, "app", "content", "courses", "contests")
bad = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (" " + str(detail) if detail else ""))
    if not cond:
        bad.append(name)


# ---- 1. expected values by brute force ----
def ships(weights, k, cap):
    """True if some split into at most k non-empty contiguous days keeps every day's sum within cap."""
    n = len(weights)
    for d in range(1, min(k, n) + 1):
        for cuts in itertools.combinations(range(1, n), d - 1):
            b = (0,) + cuts + (n,)
            if all(sum(weights[b[i]:b[i + 1]]) <= cap for i in range(d)):
                return True
    return False


check("l13 test 12: [5, 5] in 3 days at 4 cannot ship", ships([5, 5], 3, 4) is False)
check("l13 test 4: [5] in 1 day at 4 cannot ship", ships([5], 1, 4) is False)
check("l13 tests 2, 3: 11 fails and 12 ships in 3 days",
      (ships([4, 8, 2, 7, 5, 3], 3, 11), ships([4, 8, 2, 7, 5, 3], 3, 12)) == (False, True))
# the day count a guard-free greedy reaches on test 12
days, load = 1, 0
for w in [5, 5]:
    if load + w > 4:
        days, load = days + 1, 0
    load += w
check("l13 test-12 line: counting days gives 3", days == 3, days)


def decayed(value, minute):
    return max(0.3 * value, value - value / 250 * minute)


def brute_best(problems, minutes):
    best = None
    for order in itertools.permutations(problems):
        clock, total = 0, 0
        for _, v, t in order:
            clock += t
            if clock <= minutes:
                total += decayed(v, clock)
        names = [p[0] for p in order]
        if best is None or total > best[0] or (total == best[0] and names < best[1]):
            best = (total, names)
    return best


R = [("A", 500, 10), ("B", 1000, 20), ("C", 1500, 35), ("D", 2000, 50)]
check("l14 test 4: one problem of 10 minutes in a 5-minute round is (0, ['A'])", brute_best([("A", 500, 10)], 5) == (0, ["A"]))
check("l14 test 2: (2090, B C A D)", brute_best(R, 60) == (2090.0, ["B", "C", "A", "D"]))
check("l14: a solved problem always scores above 0 (floor 0.3 of value)", decayed(500, 10 ** 6) == 150.0)


def distinct(text):
    d = text.split()
    pos, out = 1, []
    for _ in range(int(d[0])):
        n = int(d[pos])
        out.append(len(set(d[pos + 1:pos + 1 + n])))
        pos += 1 + n
    return out


check("l15 test 3: cases AAA, AAA, BBB AAA give [1, 1, 2]", distinct("3\n1\nAAA\n1\nAAA\n2\nBBB AAA\n") == [1, 1, 2])

# ---- 2. natural codings, first failing test under the page's harness ----
MIN_CAP = """

def min_capacity(weights, k):
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(weights, k, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
"""
BO = "from itertools import permutations\n\n\ndef best_order(problems, minutes):\n"
SCORE = "decayed_score(value, clock, 0, value / 250, 50, 0.3)"
L13, L14, L15 = ("l13-virtual-contest.json", 5), ("l14-which-first.json", 10), ("l15-debugging-under-time.json", 5)
CODINGS = [
    # (widget, label, expected first failing test or 0 for a pass, source)
    (L13, "A no guard, else branch starts the day with w", 12,
     "def can_ship(weights, k, cap):\n    days, cur = 1, 0\n    for w in weights:\n        if cur + w <= cap:\n            cur += w\n"
     "        else:\n            days += 1\n            cur = w\n    return days <= k\n" + MIN_CAP),
    (L13, "B no guard, add then test overflow", 12,
     "def can_ship(weights, k, cap):\n    days = 1\n    load = 0\n    for w in weights:\n        load += w\n        if load > cap:\n"
     "            days += 1\n            load = w\n    return days <= k\n" + MIN_CAP),
    (L13, "C no guard, early exit once days pass k", 12,
     "def can_ship(weights, k, cap):\n    days, load = 1, 0\n    for w in weights:\n        if load + w > cap:\n            days += 1\n"
     "            load = 0\n            if days > k:\n                return False\n        load += w\n    return True\n" + MIN_CAP),
    (L13, "D contrast: no guard and days counted from 0 (fails test 4, not 12)", 4,
     "def can_ship(weights, k, cap):\n    days, load = 0, cap\n    for w in weights:\n        if load + w > cap:\n            days += 1\n"
     "            load = w\n        else:\n            load += w\n    return days <= k\n" + MIN_CAP),
    (L14, "A best starts at 0, names None, strict >", 4,
     BO + "    best, names = 0, None\n    for order in permutations(sorted(problems)):\n        clock = total = 0\n"
     "        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n"
     "                total += " + SCORE + "\n        if total > best:\n            best, names = total, [p[0] for p in order]\n    return best, names\n"),
    (L14, "B best starts at 0, names [], strict >", 4,
     BO + "    best = 0\n    names = []\n    for order in permutations(sorted(problems)):\n        clock = 0\n        total = 0\n"
     "        for name, value, time in order:\n            clock += time\n            if clock > minutes:\n                continue\n"
     "            total += " + SCORE + "\n        if total > best:\n            best = total\n            names = [name for name, _, _ in order]\n"
     "    return best, names\n"),
    (L14, "C filters out problems longer than the round", 4,
     BO + "    fits = sorted(p for p in problems if p[2] <= minutes)\n    best, names = -1, None\n    for order in permutations(fits):\n"
     "        clock = total = 0\n        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n"
     "                total += " + SCORE + "\n        if total > best:\n            best, names = total, [p[0] for p in order]\n    return best, names\n"),
    (L14, "D contrast: names only the problems solved (fails test 2, not 4)", 2,
     BO + "    best, names = -1, None\n    for order in permutations(sorted(problems)):\n        clock = total = 0\n        done = []\n"
     "        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n"
     "                total += " + SCORE + "\n                done.append(name)\n        if total > best:\n            best, names = total, done\n"
     "    return best, names\n"),
    (L14, "E following the line: best starts at -1, float total (passes)", 0,
     BO + "    best, names = -1, None\n    for order in permutations(sorted(problems)):\n        clock, total = 0, 0.0\n"
     "        for name, value, time in order:\n            clock += time\n            if clock <= minutes:\n"
     "                total += " + SCORE + "\n        if total > best:\n            best, names = total, [p[0] for p in order]\n    return best, names\n"),
    (L15, "A one set per call, counts tickers not seen before", 3,
     "def solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    seen = set()\n    for _ in range(t):\n"
     "        n = int(data[pos])\n        pos += 1\n        count = 0\n        for s in data[pos:pos + n]:\n            if s not in seen:\n"
     "                seen.add(s)\n                count += 1\n        pos += n\n        out.append(count)\n    return out\n"),
    (L15, "B global set emptied between cases only, so the last case leaks into the next call", 3,
     "seen = set()\n\n\ndef solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    for i in range(t):\n"
     "        n = int(data[pos])\n        pos += 1\n        for s in data[pos:pos + n]:\n            seen.add(s)\n        pos += n\n"
     "        out.append(len(seen))\n        if i < t - 1:\n            seen.clear()\n    return out\n"),
    (L15, "C global set, cleared at the top of every case but the first", 3,
     "seen = set()\n\n\ndef solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    for case in range(t):\n"
     "        n = int(data[pos])\n        pos += 1\n        if case:\n            seen.clear()\n        seen.update(data[pos:pos + n])\n"
     "        pos += n\n        out.append(len(seen))\n    return out\n"),
    (L15, "D contrast: one set per call, never emptied (fails test 2, not 3)", 2,
     "def solve_all(text):\n    data = text.split()\n    t = int(data[0])\n    pos = 1\n    out = []\n    seen = set()\n    for _ in range(t):\n"
     "        n = int(data[pos])\n        pos += 1\n        seen.update(data[pos:pos + n])\n        pos += n\n        out.append(len(seen))\n"
     "    return out\n"),
]

DRIVER = r"""
import fs from 'node:fs';
const [, , runnerPath, root, pkgs, jobsPath] = process.argv;
const { makeRunner } = await import(runnerPath);
const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));
const runner = makeRunner({ pkgs, root, jobs: 2 });
const out = [];
for (const j of jobs) {
  const spec = JSON.parse(fs.readFileSync(j.path, 'utf8')).screens[j.screen].widget;
  const src = j.source === '@solution' ? spec.solution : j.source === '@starter' ? spec.starter : j.source;
  const r = await runner.grade(spec, src, 'tests');
  const first = r.rows.findIndex((x) => !x.ok);
  out.push({ ok: r.ok, key: r.key, first: first + 1, actual: first >= 0 ? r.rows[first].actual : null, error: r.error || (first >= 0 ? r.rows[first].error : null) });
}
await runner.close();
console.log('ZQOUT' + JSON.stringify(out));
process.exit(0);
"""

if len(sys.argv) < 2:
    print("no <pkgs> given: Pyodide part skipped")
    sys.exit(1 if bad else 0)
pkgs = sys.argv[1]
scratch = sys.argv[2] if len(sys.argv) > 2 else tempfile.mkdtemp()
jobs = []
for f, s in (L13, L14, L15):
    jobs.append({"path": os.path.join(C, f), "screen": s, "label": f.split("-")[0] + " solution passes", "source": "@solution", "want": 0})
    jobs.append({"path": os.path.join(C, f), "screen": s, "label": f.split("-")[0] + " starter fails", "source": "@starter", "want": -1})
for (f, s), label, want, src in CODINGS:
    jobs.append({"path": os.path.join(C, f), "screen": s, "label": f.split("-")[0] + " " + label, "source": src, "want": want})
jp, dp = os.path.join(scratch, "jobs.json"), os.path.join(scratch, "driver.mjs")
json.dump(jobs, open(jp, "w"))
open(dp, "w").write(DRIVER)
p = subprocess.run(["node", dp, os.path.join(ROOT, "app", "tools", "code-runner.mjs"), os.path.join(ROOT, "app"), pkgs, jp],
                   capture_output=True, text=True)
line = [l for l in p.stdout.splitlines() if l.startswith("ZQOUT")]
if not line:
    print(p.stdout[-800:], p.stderr[-800:])
    sys.exit(2)
for j, r in zip(jobs, json.loads(line[0][5:])):
    got = 0 if r["ok"] else r["first"]
    cond = (got != 0) if j["want"] == -1 else got == j["want"]
    check(j["label"], cond, "| first fail: %s, key: %s, actual: %s %s" % (got or "none", r["key"], r["actual"], (r["error"] or "")[:80]))
print("failures:", len(bad))
sys.exit(1 if bad else 0)
