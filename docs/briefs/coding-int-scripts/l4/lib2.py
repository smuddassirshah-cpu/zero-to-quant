from lib import *


def table_w(columns, rows):
    return {"kind": "table", "columns": columns, "rows": rows}


def ed(answer, accept=None):
    c = {"edit": True, "answer": answer}
    if isinstance(answer, (int, float)):
        c["tol"] = {"abs": 0}
    if accept:
        c["accept"] = accept
    return c


def cpp_case(call, args, types, expect, compare="equal", **kw):
    d = {"call": call, "args": args}
    if types:
        d["types"] = types
    d["expect"] = expect
    d["compare"] = compare
    d.update(kw)
    return d


def pcases(lst, fn):
    """list of (args tuple, expect) -> test dicts calling fn(*args)"""
    out = []
    for args, exp in lst:
        out.append({"call": f"{fn}({', '.join(repr(a) for a in args)})", "expect": exp})
    return out


def explain(text, canvas=None):
    d = {"text": text}
    if canvas:
        d["canvas"] = canvas
    return d


def tkeys(n, notes):
    return {f"test-{i}": notes.get(i, f"Test {i} did not match. Trace it by hand.") for i in range(1, n + 1)}


def cons(title, lines):
    return console(title, lines)


def summary(ideas, name, tex, note, trap):
    assert len(ideas) == 3
    return {"ideas": ideas, "formula": {"name": name, "tex": tex, "note": note}, "trap": trap}
