"""Helpers for building mental-pressure level 2 content as JSON."""
import json, re, os

OUT = '/home/user/zero-to-quant/app/content/courses/mental-pressure'


def tol(abs_=None, rel=None):
    if rel is not None:
        return {"rel": rel}
    return {"abs": abs_ if abs_ is not None else 0}


def num(answer, abs_=None, rel=None, unit=None, label=None, accept=None, wrong=None, placeholder=None):
    w = {"kind": "numeric", "answer": answer, "tol": tol(abs_, rel)}
    if unit:
        w["unit"] = unit
    if label:
        w["label"] = label
    if placeholder:
        w["placeholder"] = placeholder
    if accept:
        w["accept"] = accept
    if wrong:
        w["wrong"] = [{"id": i, "value": v, "tol": tol(*t) if isinstance(t, tuple) else {"abs": t}} for i, v, t in wrong]
    return w


def cell(answer, abs_=None, rel=None, unit=None, accept=None, placeholder=None):
    c = {"edit": True, "answer": answer}
    if isinstance(answer, str):
        if accept:
            c["accept"] = accept
    else:
        c["tol"] = tol(abs_, rel)
    if unit:
        c["unit"] = unit
    if placeholder:
        c["placeholder"] = placeholder
    return c


def hints(nudge, point, step, highlight=None):
    p = {"rung": "point", "text": point}
    if highlight:
        p["highlight"] = highlight
    return [{"rung": "nudge", "text": nudge}, p, {"rung": "step", "text": step}]


def opt(id_, text, why=None, correct=False):
    o = {"id": id_, "text": text}
    if correct:
        o["correct"] = True
    else:
        o["why"] = why
    return o


def choice(options, layout="stack", shuffle=True):
    w = {"kind": "choice", "layout": layout, "options": options}
    if shuffle:
        w["shuffle"] = True
    return w


def bykey_from_choice(w):
    return {o["id"]: o["why"] for o in w["options"] if not o.get("correct")}


def table_canvas(columns, rows, align=None, state=None, maxHeight=None):
    c = {"kind": "table", "params": {"columns": columns, "rows": rows}, "state": state or {}}
    if align:
        c["params"]["align"] = align
    if maxHeight:
        c["maxHeight"] = maxHeight
    return c


CODE_KEYS = {'starter', 'solution', 'call', 'expect', 'setup', 'prelude', 'postlude', 'tex', 'expr', 'id', 'kind', 'align', 'answer', 'accept', 'bind', 'order'}


def curly(o, key=None):
    if isinstance(o, dict):
        return {k: curly(v, k) for k, v in o.items()}
    if isinstance(o, list):
        return [curly(v, key) for v in o]
    if isinstance(o, str) and key not in CODE_KEYS:
        parts = re.split(r'(`[^`]*`|```.*?```)', o, flags=re.S)
        return ''.join(p if p.startswith('`') else re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", '\u2019', p) for p in parts)
    return o


def write(name, obj):
    obj = curly(obj)
    path = os.path.join(OUT, name)
    with open(path, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print('wrote', path)


# ---------- voice checks ----------
AMERICAN = ['color', 'center', 'favorite', 'analyze', 'optimize', 'behavior', 'modeling', 'labeled', ' math ']
PROSE_KEYS = {'prose', 'question', 'text', 'why', 'correct', 'generic', 'caption', 'prompt', 'model', 'accept', 'how', 'note', 'trap', 'label'}


def strings(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, path + '.' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, path + f'[{i}]')
    elif isinstance(o, str):
        yield path, o


def strip_math(s):
    s = re.sub(r'\$\$.*?\$\$', ' M ', s, flags=re.S)
    s = re.sub(r'\$.*?\$', ' M ', s)
    s = re.sub(r'```.*?```', ' C ', s, flags=re.S)
    s = re.sub(r'`[^`]*`', ' C ', s)
    return s


def check_voice(obj, name):
    problems = []
    for path, s in strings(obj):
        key = path.split('.')[-1].split('[')[0]
        if key in CODE_KEYS:
            continue
        if '!' in strip_math(s).replace('!=', ''):
            problems.append((path, 'exclamation', s[:80]))
        if '—' in s or '–' in s:
            problems.append((path, 'dash', s[:80]))
        for a in AMERICAN:
            if a in s.lower():
                problems.append((path, 'american ' + a, s[:80]))
        if key in ('model',):
            continue
        t = strip_math(s)
        # sentences
        for sent in re.split(r'(?<=[.?:;])\s+', t):
            words = [w for w in re.split(r'\s+', sent) if w]
            if len(words) > 20 and key not in ('how',):
                problems.append((path, f'long sentence {len(words)}', sent[:100]))
        if key == 'prose':
            words = [w for w in re.split(r'\s+', t) if w]
            if len(words) > 60:
                problems.append((path, f'prose {len(words)} words', ''))
        if key == 'text' and '.explain.' in path + '.':
            n = len([x for x in re.split(r'(?<=[.?])\s+', t.strip()) if x])
            if n > 3:
                problems.append((path, f'explain {n} sentences', s[:80]))
    for p in problems:
        print(name, *p)
    return problems
