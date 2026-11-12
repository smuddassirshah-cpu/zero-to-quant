"""The judge and the timed runner shared by code_run.py and proposed_code.py (see code_run.py for the rules)."""
import signal, sys, time
from fractions import Fraction
sys.setrecursionlimit(3000)
SLOW, STOP = 1.0, 4.0


class Stopped(BaseException):
    pass


def _alarm(*_):
    raise Stopped()


signal.signal(signal.SIGALRM, _alarm)


def same(x, y):
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p, q) for p, q in zip(x, y))
    try:
        if x != x and y != y:
            return True
    except Exception:
        pass
    return bool(x == y)


def judge(a, e, c):
    if c == 'fraction':
        return isinstance(a, Fraction) and a == e
    assert c == 'equal', c
    return same(a, e)


def run(src, cases):
    ns = {}
    try:
        exec(src, ns)
    except Exception as x:
        return [(False, 0, 'load error ' + repr(x))] * len(cases)
    out = []
    for c in cases:
        env = dict(ns)
        t = time.perf_counter()
        signal.setitimer(signal.ITIMER_REAL, STOP)
        try:
            if c.get('setup'):
                exec(c['setup'], env)
            a = eval(c['call'], env)
            dt = time.perf_counter() - t
            signal.setitimer(signal.ITIMER_REAL, 0)
            out.append((judge(a, eval(c['expect'], env), c.get('compare', 'equal')), dt, repr(a)[:70]))
        except Stopped:
            out.append((False, STOP, 'stopped'))
        except RecursionError:
            out.append((False, 0, 'RecursionError'))
        except Exception as x:
            out.append((False, 0, 'raised ' + type(x).__name__))
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
    return out


