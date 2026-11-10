"""Run a module of candidate functions against the hidden tests of ci packs 1 and 2.

usage: harness.py <module.py> <drills dir> [--limit seconds]
A module defines functions under the drill's `fn` name. A name with a suffix
`__tag` (two underscores) is a second candidate for the same drill.
Prints one line per candidate: PASS, or the first failing test, or SLOW.
"""
import glob
import importlib.util
import json
import signal
import sys
import time

mod_path, drills = sys.argv[1], sys.argv[2]
limit = float(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 5.0
spec = importlib.util.spec_from_file_location("cand", mod_path)
cand = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cand)


class Slow(Exception):
    pass


def alarm(*_):
    raise Slow()


signal.signal(signal.SIGALRM, alarm)
by_fn = {}
for f in sorted(glob.glob(drills + "/ci-*.json")):
    d = json.load(open(f))
    if "pack-1" in d["tags"] or "pack-2" in d["tags"]:
        by_fn[d["fn"]] = d

passed = failed = 0
for name in sorted(vars(cand)):
    base = name.split("__")[0]
    if base not in by_fn or not callable(getattr(cand, name)):
        continue
    d = by_fn[base]
    ns = {base: getattr(cand, name)}
    verdict = "PASS"
    t0 = time.time()
    signal.setitimer(signal.ITIMER_REAL, limit)
    try:
        for i, t in enumerate(d["examples"] + d["tests"]):
            where = ("example %d" % i) if i < len(d["examples"]) else ("test %d" % (i - len(d["examples"])))
            try:
                got = eval(t["call"], dict(ns))
            except Slow:
                raise
            except Exception as e:  # noqa
                verdict = "FAIL %s: raised %s" % (where, type(e).__name__)
                break
            want = eval(t["expect"])
            if got != want or type(got) is not type(want):
                verdict = "FAIL %s: got %s want %s" % (where, repr(got)[:60], repr(want)[:60])
                break
    except Slow:
        verdict = "SLOW (over %.0f s in total, native CPython)" % limit
    signal.setitimer(signal.ITIMER_REAL, 0)
    if verdict == "PASS":
        passed += 1
    else:
        failed += 1
    print("%-24s %-34s %-5.2fs %s" % (d["id"], name, time.time() - t0, verdict))
print("candidates: %d pass, %d not" % (passed, failed))
