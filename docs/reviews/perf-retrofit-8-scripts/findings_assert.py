"""One check per finding in review-perf-retrofit-8.md. Exits 1 while any finding is open (by design);
each FAIL line names its finding and turns to ok when the fix lands. It also checks that every
replacement text proposed in the review passes the voice gate (35 words, three-sentence explains),
with voice-scan.py's own sentence splitter. Python 3, from this folder."""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
C = ROOT / "app" / "content" / "courses"
R = ROOT / "docs" / "reports"
fails = 0

# voice-scan.py's mask, sentences and words, loaded from the file itself
src = (ROOT / "docs" / "reviews" / "voice-scan.py").read_text()
ns = {"re": re}
for name in ("mask", "sentences", "words"):
    m = re.search(r"^def %s\(.*?(?=^def |\Z)" % name, src, flags=re.S | re.M)
    exec(m.group(0), ns)
sentences, words = ns["sentences"], ns["words"]


def item(course, f, iid):
    return next(i for i in json.loads((C / course / f).read_text())["items"] if i["id"] == iid)


def check(fid, ok, what):
    global fails
    print(("ok   " if ok else "FAIL ") + f"{fid}: {what}")
    fails += not ok


sr = item("cpp", "homework-3.json", "h-session-range")["widget"]
check("CPP3-1", any(t.get("compiles", "").startswith("auto [a, b] = r;") and t.get("expect") is False for t in sr["tests"]),
      "a compile check refuses a range whose two ends are public (structured binding)")
check("CPP3-1", "No test can see whether the ends are private" not in sr["how"], "the how no longer says no test can see privacy")
t11 = sr["tests"][10]
check("CPP3-2", "SessionRange<int>(1, 4) == SessionRange<int>(2, 5)" in t11["call"], "test 11 compares two ranges of equal width")

med = item("cpp", "homework-4.json", "h4-test-median")["widget"]
check("CPP4-1", "a check fails, or the run stops" not in med["how"], "the how says which tests expect a failed check and which a stopped run")
check("CPP4-2", "(s[n / 2 - 1] + s[n / 2]) / 2" not in med["prelude"], "slips 2 and 3 wrap the sum without signed overflow")

for rep, old in [("cpp-1-perf.md", "l3 screen 3 "), ("cpp-3-perf.md", "l10 screen 3 "), ("cpp-3-perf.md", "l12 screens 2 and 7"), ("cpp-3-perf.md", "l13 screen 9 "), ("cpp-4-perf.md", "l18 screens 3, 4 and 9")]:
    check("REP-2", old not in (R / rep).read_text(), f"{rep}: no 0-based screen number '{old.strip()}'")

lz = item("markov", "homework-5.json", "h-build-lazy-martingales")["widget"] if "widget" in item("markov", "homework-5.json", "h-build-lazy-martingales") else item("markov", "homework-5.json", "h-build-lazy-martingales")
rows = [r["text"] for r in lz["rubric"]]
check("MK5-1", "finite mean" in rows[2] or "mean is finite" in rows[2], "rubric row 3 asks for a reason the power has a finite mean")
check("MK5-2", "$E[T]$" in rows[3], "rubric row 4 accepts condition (2) as well as condition (3)")
check("MK5-2", "Condition (2) would serve too" in lz["model"], "the model shows condition (2) holds too")

l19 = json.loads((C / "markov" / "l19-optional-stopping.json").read_text())
l20 = json.loads((C / "markov" / "l20-when-stopping-fails.json").read_text())
hw5 = json.loads((C / "markov" / "homework-5.json").read_text())
check("L19-1", "stays bounded, and $T$ is finite with chance 1." in l19["screens"][2]["prose"], "l19 screen 3 states condition (3) with T finite")
check("L19-1", "stays bounded with $T$ finite." in l19["summary"]["ideas"][0], "l19 summary states condition (3) with T finite")
check("L19-1", "$T$ is finite with chance 1" in l19["screens"][3]["widget"]["lines"][1]["text"], "l19 screen 4 line 2 says T is finite")
check("L19-1", "the stopped walk bounded with $T$ finite." in l20["screens"][3]["prose"], "l20 screen 4 recalls condition (3) with T finite")
tp = next(i for i in hw5["items"] if i["id"] == "h-long-take-profit")
check("L19-1", "bounded stopped process with $T$ finite" in tp["model"], "h-long-take-profit model states condition (3) with T finite")
for k in (2, 5, 9):
    n = len(sentences(l19["screens"][k]["explain"]["text"]))
    check("VOICE-1", n <= 3, f"l19 screens.{k}.explain has {n} sentences")

# the replacement texts proposed in the review pass the voice gate
PROPOSED = {
    "CPP3-1 how": "The first Check downloads the C++ compiler (about 26 MB) and compiles in 10 to 15 s. Later Checks take 1 to 3 s. Check runs 15 hidden tests with `int`, `long long` and `double` ranges. Doubles are accepted within a relative 1e-9. One builds a low above the high and passes only if the program stops. Three only compile a line: one on a `const` range, and two that must be refused. One of those unpacks a range as `auto [a, b] = r;`, which compiles only when its two ends are its only data and public. It cannot catch every layout, so check privacy yourself too.",
    "CPP4-1 how": "The first Check downloads the C++ compiler (about 26 MB) and compiles in 10 to 15 s. Later Checks take 1 to 3 s. Test 1 runs your tests against the real median_volume and expects every one to pass. Tests 2 to 5 each swap in a version with one slip, and expect one of your checks to fail. Test 6 swaps in a version that crashes on some input, and expects the run to stop.",
    "MK5-1 row 3": "Tick only if all are given: $E[\\theta^{S_{n+1}} \\mid \\text{history}] = \\theta^{S_n}(p\\theta + r + q/\\theta)$ with its reasons; a reason $\\theta^{S_n}$ has a finite mean; the equation solved as $(\\theta - 1)(p\\theta - q) = 0$, so $\\theta = 1$ or $\\theta = q/p$; and why no other $\\theta$ works, since $\\theta^{S_n} > 0$.",
    "MK5-2 row 4": "Tick only if all are given: a condition of optional stopping named and shown to hold, with reasons. Either the stopped process stays between $\\theta^5$ and 1 and $T$ is finite with chance 1, or $E[T]$ is finite and the stopped steps are bounded. Then $P\\theta^5 + (1 - P) = \\theta^2$ with $\\theta = \\tfrac23$, and $P = \\tfrac{135}{211} \\approx 0.640$.",
    "MK5-2 model": "Condition (2) would serve too: summing the block bound gives $E[T] \\le 5/0.00243$, which is finite, and each step of the stopped $\\theta^{S_n}$ is at most $1 - \\theta$.",
    "L19-1 l19 prose": "A **stopping time** $T$ is a rule that decides at each step $n$ from the first $n$ steps only. The **optional stopping theorem**: for a martingale $M$, $E[M_T] = E[M_0]$ in three cases. (1) $T$ is bounded. (2) $E[T]$ is finite and the steps of $M$ are bounded. (3) The stopped process stays bounded, and $T$ is finite with chance 1.",
    "L19-1 summary": "A stopping time decides from the past alone. A stopped martingale keeps its mean if $T$ is bounded, or has finite mean with bounded steps, or stays bounded with $T$ finite.",
    "L19-1 l19 s4 line": "$T$, the first hit of 0 or $N$, is a stopping time, the stopped walk stays in $[0, N]$, and $T$ is finite with chance 1. So the theorem applies.",
    "L19-1 hw5 model": "The stopped P&L lies in $[-9, 1]$ and $T$ is finite with chance 1, so condition (3) holds and $E[X_T] = 0$.",
}
EXPLAINS = {
    "VOICE-1 s2": "Whether you have hit £0 or £10 is known from the bets so far, so it is a stopping time. The other rules need results that have not happened. Here condition (3) holds: the stopped bankroll stays between £0 and £10, and the game ends with chance 1.",
    "VOICE-1 s5": "$P = \\dfrac{1 - 1.5^5}{1 - 1.5^{10}} = \\tfrac{32}{275} \\approx 0.1164$. On the chart the average of $S_T$ drifts down to about £1.17, while the average of $r^{S_T}$ stays near its start, $r^5 \\approx 7.59$. Choose the martingale before you stop.",
    "VOICE-1 s9": "The plain walk loses 0.02 a bet, so its stopped mean falls: these games averaged £11.75, and 23 of 200 reached £100. The right martingale is $(q/p)^{S_n}$ with $r = \\tfrac{51}{49}$, giving $P \\approx 0.1192$. Optional stopping needs a martingale first.",
}
bad_text = 0
for k, t in {**PROPOSED, **EXPLAINS}.items():
    longest = max(words(s) for s in sentences(t))
    n = len(sentences(t))
    ok = longest <= 35 and "!" not in t and "—" not in t and "–" not in t and (k not in EXPLAINS or n <= 3)
    print(("ok   " if ok else "FAIL ") + f"proposed text {k}: longest sentence {longest} words, {n} sentences")
    bad_text += not ok
print("open findings:", fails, " proposed texts failing voice:", bad_text)
sys.exit(1 if fails or bad_text else 0)
