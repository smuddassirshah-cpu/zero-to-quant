import json, re

COURSE = 'coding-int'


def hints(nudge, point, step, hl=None):
    p = {"rung": "point", "text": point}
    if hl:
        p["highlight"] = hl
    return [{"rung": "nudge", "text": nudge}, p, {"rung": "step", "text": step}]


def fb(correct, generic, by=None):
    d = {"correct": correct, "generic": generic}
    if by:
        d["byKey"] = by
    return d


def choice(opts, layout="stack"):
    """opts: list of (id, text, why); why None marks the key."""
    out = []
    for oid, text, why in opts:
        o = {"id": oid, "text": text}
        if why is None:
            o["correct"] = True
        else:
            o["why"] = why
        out.append(o)
    assert sum(1 for o in out if o.get("correct")) == 1
    return {"kind": "choice", "layout": layout, "options": out, "shuffle": True}


def multi(opts, layout="stack"):
    out = []
    for oid, text, why in opts:
        o = {"id": oid, "text": text}
        if why is None:
            o["correct"] = True
        else:
            o["why"] = why
        out.append(o)
    return {"kind": "multi", "layout": layout, "options": out, "shuffle": True}


def numeric(answer, label, accept, wrong=(), unit=None):
    w = {"kind": "numeric", "answer": answer, "tol": {"abs": 0}, "label": label, "accept": accept}
    if unit:
        w["unit"] = unit
    if wrong:
        w["wrong"] = [{"id": i, "value": v} for i, v in wrong]
    return w


def order(lines, answer, distractors=None, same=None):
    """lines: list of (id, text, why-or-None)."""
    ls = []
    for lid, text, why in lines:
        o = {"id": lid, "text": text}
        if why:
            o["why"] = why
        ls.append(o)
    w = {"kind": "order", "lines": ls, "answer": answer}
    if distractors:
        w["distractors"] = distractors
    if same:
        w["same"] = same
    return w


def tests_json(tests, lang='python'):
    out = []
    for t in tests:
        d = {}
        if t.get('setup'):
            d['setup'] = t['setup']
        if lang == 'python':
            d['call'] = t['call']
            d['expect'] = t['expect'] if isinstance(t['expect'], str) and t.get('compare') == 'raises' else repr(t['expect'])
            d['compare'] = t.get('compare', 'equal')
        else:
            d.update(t)
        out.append(d)
    return out


def code(lang, starter, solution, examples, tests, how, prelude=None, postlude=None, budget=None, label=None):
    w = {"kind": "code", "language": lang, "starter": starter, "solution": solution}
    if lang == 'python':
        w["examples"] = tests_json(examples)
        w["tests"] = tests_json(tests)
    else:
        w["examples"] = examples
        w["tests"] = tests
    w["how"] = how
    if prelude:
        w["prelude"] = prelude
    if postlude:
        w["postlude"] = postlude
    if budget:
        w["budget"] = budget
    return w


def console(title, lines, compact=True):
    return {"kind": "console", "params": {"title": title, "lines": lines, "compact": compact, "wrap": True}, "state": {}}


def screen(typ, diff, title, tags, prose, question, widget, hnts, fbk, explain, canvas=None, pace=None, **kw):
    s = {"type": typ, "difficulty": diff, "title": title, "tags": tags}
    if pace:
        s["pace"] = pace
    s["prose"] = prose
    if canvas:
        s["canvas"] = canvas
    s["question"] = question
    s["widget"] = widget
    s["hints"] = hnts
    s["feedback"] = fbk
    s["explain"] = explain
    s.update(kw)
    return s


def item(iid, diff, skills, tags, question, widget, fbk, explain, prose=None, canvas=None, pace=None, quiz=False):
    d = {"id": iid, "difficulty": diff}
    if not quiz:
        d["skills"] = skills
    d["tags"] = tags
    if pace:
        d["pace"] = pace
    if prose:
        d["prose"] = prose
    if canvas:
        d["canvas"] = canvas
    d["question"] = question
    d["widget"] = widget
    d["feedback"] = fbk
    d["explain"] = explain
    return d


def write(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')


def linked(cells, caption=None, pointers=None, highlight=None):
    c = {"kind": "array", "params": {"cells": cells, "mode": "linked"}, "state": {}}
    if caption:
        c["state"]["caption"] = caption
    if pointers:
        c["state"]["pointers"] = pointers
    if highlight:
        c["state"]["highlight"] = highlight
    return c


def check_voice(obj):
    """Walk every string: no exclamation mark, no em dash, sentences under 20 words."""
    bad = []

    def walk(x, path=''):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in ('starter', 'solution', 'prelude', 'postlude', 'call', 'setup', 'expect', 'lines', 'args', 'types'):
                    continue
                walk(v, path + '/' + str(k))
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, path + '/' + str(i))
        elif isinstance(x, str):
            t = re.sub(r'```.*?```', '', x, flags=re.S)
            if '!' in t.replace('!=', ''):
                bad.append((path, 'exclamation', t[:60]))
            if '—' in x or '–' in x:
                bad.append((path, 'dash', t[:60]))
            t2 = re.sub(r'`[^`]*`', 'X', t)
            for s in re.split(r'(?<=[.?])\s+', t2):
                if len(s.split()) > 20:
                    bad.append((path, 'long sentence', s[:80]))
    walk(obj)
    return bad
