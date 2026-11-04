"""Small constructors for the exam items, so build_a/b/c read as content."""


def fb(correct, generic, by_key=None):
    d = {"correct": correct, "generic": generic}
    if by_key:
        d["byKey"] = by_key
    return d


def item(id, difficulty, skills, tags, pace, title, prose, question, widget, feedback, explain,
         canvas=None, explain_canvas=None):
    it = {"id": id, "difficulty": difficulty, "skills": skills, "tags": tags, "pace": pace,
          "title": title, "prose": prose}
    if canvas:
        it["canvas"] = canvas
    it["question"] = question
    it["widget"] = widget
    it["feedback"] = feedback
    ex = {"text": explain}
    if explain_canvas:
        ex["canvas"] = explain_canvas
    it["explain"] = ex
    return it


def parts_item(id, difficulty, skills, tags, pace, title, prose, question, parts, explain):
    out_parts = []
    for p in parts:
        part = {"question": p["question"], "widget": p["widget"], "feedback": p["feedback"]}
        out_parts.append(part)
    return {"id": id, "difficulty": difficulty, "skills": skills, "tags": tags, "pace": pace,
            "title": title, "prose": prose, "question": question, "parts": out_parts,
            "explain": {"text": explain}}


def numeric(answer, abs_=None, rel=None, unit=None, placeholder="a number", label="Answer", wrong=None, accept=None):
    tol = {"abs": abs_} if abs_ is not None else {"rel": rel}
    w = {"kind": "numeric", "answer": answer, "tol": tol, "placeholder": placeholder, "label": label}
    if unit:
        w["unit"] = unit
    if accept:
        w["accept"] = accept
    if wrong:
        w["wrong"] = [{"id": i, "value": v, "tol": {"abs": t}} for i, v, t in wrong]
    return w


def _opts(opts):
    out = []
    for oid, text, correct, why in opts:
        o = {"id": oid, "text": text}
        if correct:
            o["correct"] = True
        else:
            o["why"] = why
        out.append(o)
    return out


def choice(opts, layout="stack"):
    return {"kind": "choice", "layout": layout, "shuffle": True, "options": _opts(opts)}


def multi(opts, layout="stack"):
    return {"kind": "multi", "layout": layout, "shuffle": True, "options": _opts(opts)}


def order(lines, answer, distractors=None):
    ls = []
    for lid, text, why in lines:
        l = {"id": lid, "text": text}
        if why:
            l["why"] = why
        ls.append(l)
    w = {"kind": "order", "lines": ls, "answer": answer}
    if distractors:
        w["distractors"] = distractors
    return w


def _case(c, default_compare):
    call, expect = c[0], c[1]
    d = {"call": call, "expect": expect, "compare": default_compare}
    if len(c) > 2 and c[2]:
        d.update(c[2])
    return d


def code_py(starter, solution, prelude, examples, tests, how, compare="equal"):
    return {"kind": "code", "language": "python", "starter": starter, "solution": solution,
            "prelude": prelude,
            "examples": [_case(c, compare) for c in examples],
            "tests": [_case(c, compare) for c in tests],
            "how": how}


def code_cpp(starter, solution, examples, tests, how):
    return {"kind": "code", "language": "cpp", "starter": starter, "solution": solution,
            "examples": examples, "tests": tests, "how": how}
