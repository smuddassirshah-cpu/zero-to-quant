"""llm-apps level 3 (Tools and agents): a scripted stand-in for a language model, three small tools and planted tasks.

There is no language model here. `respond` looks up the task id in the first user message ("[T07] ...") and the turn
number, and replies from a fixed script, so every run is the same. Real models differ: they are not scripted, they vary
with sampling, and they can be steered by a tool's description; the scripts plant those behaviours so they can be measured.

Messages: [{"role": "user", "content": text}, {"role": "assistant", "content": reply}, {"role": "tool", "name": n, "content": result}, ...]
respond(messages, tools) -> {"type": "tool_call", "name": str, "arguments": "<JSON text>"} or {"type": "answer", "text": str}
    `tools` is the list of tool specs {"name", "description", "input_schema"} the model is shown. A tool result is a dict:
    {"result": value} on success or {"error": message}. Scripts that self-correct read the last error message: they fix
    a call only when the message names what was wrong (the field and the expected type, the word JSON, the real tool name,
    or the missing field); "invalid input" fixes nothing, so the script repeats its call.
TASKS: list of {"id", "question", "answer", "required", "kind", ...}: 20 planted tasks (see the table in the level report).
get_close(ticker, date) -> float; search_notes(query, k=3) -> [note ids]; pct_change(a, b) -> rounded percentage change.
SCHEMAS: the JSON schema of each tool's arguments. TOOLS: {name: {"fn": f, "schema": s, "description": d}}.
PRICES: {ticker: {date: close}} for 4 invented tickers over 20 business days of March 2024 (29 March, a holiday, has none).
"""
import json
import random

import llm_apps_ops_l1 as _l1

__version__ = "1.0"

TICKERS = ["CORR", "DUNM", "ELRY", "HALL"]
DAYS = ["2024-03-01", "2024-03-04", "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-08", "2024-03-11", "2024-03-12",
        "2024-03-13", "2024-03-14", "2024-03-15", "2024-03-18", "2024-03-19", "2024-03-20", "2024-03-21", "2024-03-22",
        "2024-03-25", "2024-03-26", "2024-03-27", "2024-03-28"]


def _prices():
    g = random.Random(7)
    out = {}
    for t, p0 in zip(TICKERS, (100.0, 54.0, 212.0, 31.0)):
        p, row = p0, {}
        for d in DAYS:
            p = round(p * (1 + g.gauss(0, 0.015)), 2)
            row[d] = p
        out[t] = row
    return out


PRICES = _prices()
_NOTES = None
_MODEL = None


def get_close(ticker, date):
    if ticker not in PRICES:
        raise ValueError(f"unknown ticker {ticker!r}")
    if date not in PRICES[ticker]:
        raise ValueError(f"no close for {ticker} on {date}")
    return PRICES[ticker][date]


def search_notes(query, k=3):
    global _NOTES, _MODEL
    if _MODEL is None:
        _NOTES = _l1.load_notes()['notes']
        _MODEL = _l1.fit_tfidf([n['text'] for n in _NOTES])
    s = _MODEL['X'] @ _l1.embed(query, _MODEL)
    order = sorted(range(len(s)), key=lambda i: (-s[i], i))
    return [int(i) for i in order[:k] if s[i] > 0]


def pct_change(a, b):
    return round((b - a) / a * 100, 2)


SCHEMAS = {
    "get_close": {"type": "object", "properties": {"ticker": {"type": "string", "enum": TICKERS}, "date": {"type": "string"}},
                  "required": ["ticker", "date"], "additionalProperties": False},
    "search_notes": {"type": "object", "properties": {"query": {"type": "string"}, "k": {"type": "integer", "minimum": 1, "maximum": 10}},
                     "required": ["query"], "additionalProperties": False},
    "pct_change": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                   "required": ["a", "b"], "additionalProperties": False},
}
DESCRIPTIONS = {
    "get_close": "Closing price of one share on one trading day. ticker: one of CORR, DUNM, ELRY, HALL. date: 'YYYY-MM-DD'.",
    "search_notes": "Search the desk's research notes by text; returns the ids of the best-matching notes, best first.",
    "pct_change": "Percentage change from a to b, rounded to 2 places: (b - a) / a * 100.",
}
TOOLS = {n: {"fn": f, "schema": SCHEMAS[n], "description": DESCRIPTIONS[n]} for n, f in
         (("get_close", get_close), ("search_notes", search_notes), ("pct_change", pct_change))}


def _call(name, **args):
    return {"type": "tool_call", "name": name, "arguments": json.dumps(args)}


def _answer(text):
    return {"type": "answer", "text": text}


def _pc(t, d1, d2):
    return pct_change(PRICES[t][d1], PRICES[t][d2])


# kind: what the script does. Every script ends with the known answer if it gets the facts it needs.
_SPEC = [
    ("T01", "direct", "What was CORR's close on 2024-03-08?", ("CORR", "2024-03-08")),
    ("T02", "direct", "What was HALL's close on 2024-03-21?", ("HALL", "2024-03-21")),
    ("T03", "move", "By what percentage did DUNM move from 2024-03-01 to 2024-03-15?", ("DUNM", "2024-03-01", "2024-03-15")),
    ("T04", "move", "By what percentage did ELRY move from 2024-03-04 to 2024-03-28?", ("ELRY", "2024-03-04", "2024-03-28")),
    ("T05", "search", "Which note is the best match for 'corran refinancing debt'?", ("corran refinancing debt",)),
    ("T06", "bad_json", "What was DUNM's close on 2024-03-12?", ("DUNM", "2024-03-12")),
    ("T07", "unknown_tool", "What was ELRY's close on 2024-03-07?", ("ELRY", "2024-03-07")),
    ("T08", "wrong_type", "What was CORR's close on 2024-03-19?", ("CORR", "2024-03-19")),
    ("T09", "missing_arg", "What was HALL's close on 2024-03-05?", ("HALL", "2024-03-05")),
    ("T10", "loop", "Which note is the best match for 'halloran margins profit'?", ("halloran margins profit",)),
    ("T11", "no_tool", "What was DUNM's close on 2024-03-26?", ("DUNM", "2024-03-26")),
    ("T12", "holiday", "What was CORR's close on 2024-03-29, or the last close before it?", ("CORR", "2024-03-28")),
    ("T13", "two_paths", "By what percentage did HALL move from 2024-03-11 to 2024-03-22?", ("HALL", "2024-03-11", "2024-03-22")),
    ("T14", "memory", "What was ELRY's close on 2024-03-14?", ("ELRY", "2024-03-14")),
    ("T15", "wrong_type", "What was DUNM's close on 2024-03-20?", ("DUNM", "2024-03-20")),
    ("T16", "direct", "What was ELRY's close on 2024-03-25?", ("ELRY", "2024-03-25")),
    ("T17", "move", "By what percentage did CORR move from 2024-03-13 to 2024-03-27?", ("CORR", "2024-03-13", "2024-03-27")),
    ("T18", "bad_json", "What was HALL's close on 2024-03-18?", ("HALL", "2024-03-18")),
    ("T19", "search", "Which note is the best match for 'ellery barrels oil'?", ("ellery barrels oil",)),
    ("T20", "loop", "Which note is the best match for 'garside rates yields'?", ("garside rates yields",)),
]


def _task(tid, kind, q, a):
    if kind in ("move", "two_paths"):
        t, d1, d2 = a
        ans, req = f"{_pc(t, d1, d2):.2f}%", ["get_close", "pct_change"] if kind == "move" else ["get_close"]
        return {"id": tid, "kind": kind, "question": q, "answer": ans, "required": req, "ticker": t, "dates": [d1, d2]}
    if kind in ("search", "loop"):
        return {"id": tid, "kind": kind, "question": q, "answer": str(search_notes(a[0], 1)[0]), "required": ["search_notes"], "query": a[0]}
    t, d = a
    return {"id": tid, "kind": kind, "question": q, "answer": f"{PRICES[t][d]:.2f}", "required": ["get_close"], "ticker": t, "dates": [d]}


TASKS = [_task(*s) for s in _SPEC]
# D01: the model picks a tool by its description; with no description naming a closing price it takes the first tool.
DEMO_TASKS = [dict(_task("D01", "pick", "What was CORR's close on 2024-03-08?", ("CORR", "2024-03-08")))]
_BY_ID = {t["id"]: t for t in TASKS + DEMO_TASKS}


def task_message(task):
    return {"role": "user", "content": f"[{task['id']}] {task['question']}"}


def _task_of(messages):
    c = messages[0]["content"]
    return _BY_ID[c[1:c.index("]")]]


def _last_error(messages):
    for m in reversed(messages):
        if m.get("role") == "tool":
            c = m.get("content") or {}
            return str(c.get("error", "")) if isinstance(c, dict) and "error" in c else ""
    return ""


def _results(messages):
    return [m["content"]["result"] for m in messages if m.get("role") == "tool" and isinstance(m.get("content"), dict) and "result" in m["content"]]


def respond(messages, tools):
    task = _task_of(messages)
    kind = task["kind"]
    turn = sum(1 for m in messages if m.get("role") == "assistant")
    err = _last_error(messages) if turn else ""
    got = _results(messages)
    names = [t["name"] for t in tools]
    if kind == "pick":                            # chooses by description, as a real model leans on it
        if got:
            r = got[-1]
            return _answer(f"{r:.2f}" if isinstance(r, float) else f"note {r[0]}" if r else "nothing found")
        hit = [t for t in tools if "closing price" in str(t.get("description", "")).lower()]
        if hit:
            return _call(hit[0]["name"], ticker=task["ticker"], date=task["dates"][0])
        return _call(tools[0]["name"], query=task["question"])
    if kind == "memory":                          # answers from memory, right by luck
        return _answer(task["answer"])
    if kind == "no_tool":                         # a confident wrong answer, no tool used
        return _answer(f"{PRICES[task['ticker']][task['dates'][0]] + 1.37:.2f}")
    if kind in ("search", "loop"):
        if kind == "loop":                        # never satisfied: the same search for ever
            return _call("search_notes", query=task["query"], k=3)
        if got:
            return _answer(str(got[-1][0]))
        return _call("search_notes", query=task["query"], k=3)
    if kind in ("move", "two_paths"):
        t, (d1, d2) = task["ticker"], task["dates"]
        if len(got) == 0:
            return _call("get_close", ticker=t, date=d1)
        if len(got) == 1:
            return _call("get_close", ticker=t, date=d2)
        if kind == "two_paths":                   # works the change out itself, no pct_change
            return _answer(f"{pct_change(got[0], got[1]):.2f}%")
        if len(got) == 2:
            return _call("pct_change", a=got[0], b=got[1])
        return _answer(f"{got[2]:.2f}%")
    t, d = task["ticker"], task["dates"][0]
    if got:
        return _answer(f"{got[-1]:.2f}")
    good = _call("get_close", ticker=t, date=d)
    if kind == "direct":
        return good
    if kind == "holiday":
        if "no close" in err:                     # an actionable tool error: step back a day
            return good
        return _call("get_close", ticker=t, date="2024-03-29")
    if turn == 0 or not _fixed_by(kind, err, names):
        return _bad(kind, t, d)
    return good


def _bad(kind, t, d):
    if kind == "bad_json":
        return {"type": "tool_call", "name": "get_close", "arguments": '{"ticker": "%s", "date": "%s"' % (t, d)}
    if kind == "unknown_tool":
        return {"type": "tool_call", "name": "get_price", "arguments": json.dumps({"ticker": t, "date": d})}
    if kind == "wrong_type":
        return {"type": "tool_call", "name": "get_close", "arguments": json.dumps({"ticker": t, "date": int(d.replace("-", ""))})}
    if kind == "missing_arg":
        return {"type": "tool_call", "name": "get_close", "arguments": json.dumps({"ticker": t})}
    raise ValueError(kind)


def _fixed_by(kind, err, names):
    e = err.lower()
    if kind == "bad_json":
        return "json" in e
    if kind == "unknown_tool":
        return "get_close" in e
    if kind == "wrong_type":
        return "date" in e and "string" in e
    if kind == "missing_arg":
        return "date" in e and ("missing" in e or "required" in e)
    return False
