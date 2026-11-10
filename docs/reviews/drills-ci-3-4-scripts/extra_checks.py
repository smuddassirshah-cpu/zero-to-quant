"""Proposed new hidden tests (extra_tests.json): the value by the model solution and by
mine.py, the time the model takes, and what each wrong.py candidate for that drill returns.

usage: extra_checks.py <drills dir>   (run from the repo root)
Also checks that every `how` states the right number of hidden tests.
"""
import glob
import importlib.util
import json
import os
import re
import signal
import sys
import time

here = os.path.dirname(os.path.abspath(__file__))
LIMIT = 15.0


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(here, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class Slow(Exception):
    pass


def alarm(*_):
    raise Slow()


signal.signal(signal.SIGALRM, alarm)


def run(fn_name, fn, call):
    t0 = time.time()
    signal.setitimer(signal.ITIMER_REAL, LIMIT)
    try:
        got = repr(eval(call, {fn_name: fn}))
    except Slow:
        got = "SLOW (over %.0f s, native CPython)" % LIMIT
    except Exception as e:  # noqa
        got = "raised " + type(e).__name__
    signal.setitimer(signal.ITIMER_REAL, 0)
    return got, time.time() - t0


mine, wrong = load("mine"), load("wrong")
extra = json.load(open(os.path.join(here, "extra_tests.json")))
drills = {}
for f in glob.glob(sys.argv[1] + "/ci-*.json"):
    d = json.load(open(f))
    if {"pack-3", "pack-4"} & set(d.get("tags", [])):
        drills[d["id"]] = d
        m = re.search(r"runs (\d+) hidden tests", d["how"])
        if not m or int(m.group(1)) != len(d["tests"]):
            print("HOW COUNT WRONG", d["id"])
print(len(drills), "drills read; `how` counts checked")

for did, tests in extra.items():
    d = drills[did]
    fn = d["fn"]
    ns = {}
    exec(d["solution"], ns)
    for t in tests:
        print("\n%s  %s" % (did, t["call"][:150]))
        model, secs = run(fn, ns[fn], t["call"])
        own, _ = run(fn, getattr(mine, fn), t["call"])
        want = t["expect"]
        ok = model == own and (want == "?" or repr(eval(want)) == model)
        print("  model %s (%.2f s) | mine %s | proposed expect %s | %s" % (model[:70], secs, own[:70], want, "AGREE" if ok else "DISAGREE"))
        for name in sorted(vars(wrong)):
            if name.split("__")[0] == fn and "__" in name:
                got, secs = run(fn, getattr(wrong, name), t["call"])
                print("    %-34s %s (%.2f s)%s" % (name, got[:70], secs, "" if got != model else "  <- passes this test"))
