"""llm-apps level 1 (Retrieval): an invented corpus of short research notes, and a reference TF-IDF search.

Every note and company here is invented by the course; none comes from a real firm or report.

make_notes(seed=4) -> {"notes": [...], "queries": [...]}
    180 notes. 144 are about one of 8 invented companies and one of 6 topics (3 notes for each pair):
    the company's name (once or twice), three words from the topic's pool of six near-synonyms,
    filler words, and in half of them one aside word from another topic. 36 are market notes with
    no company. Each note is {"id", "company", "topic", "text"} (company "" for a market note).
    20 labelled queries: {"text": "<company> <word> <word>", "relevant": [the 3 note ids of that pair]}.
load_notes(path="llm-apps-notes.json") -> the same dict, read from the shipped file.
make_reports(notes, seed=11, per=6) -> list of {"ids": [note ids], "text": notes joined by ". "}
    Long documents for chunking: the notes shuffled and cut into reports of `per` notes.
tokenise(text) -> lower-case runs of letters a to z.
fit_tfidf(docs, stop_words=()) -> {"vocab": sorted words, "index": {word: column}, "idf": array, "X": rows of length 1}
    scikit-learn's TfidfVectorizer defaults: raw counts, idf = ln((1 + n) / (1 + df)) + 1, each row scaled to length 1.
embed(text, model, stop_words=()) -> the query's TF-IDF vector of length 1 (all zeros if no word is known).
rank(text, model, stop_words=()) -> every row index, highest cosine first, ties to the lower index.
NumPy and the standard library only; nothing is kept between calls.
"""
import json
import random
import re

import numpy as np

__version__ = "1.0"

COMPANIES = ["ashcombe", "brackley", "corran", "dunmore", "ellery", "fairholt", "garside", "halloran"]
TOPICS = {
    "rates": ["rates", "yields", "gilts", "coupons", "curve", "inflation"],
    "oil": ["oil", "crude", "barrels", "refining", "pipeline", "fuel"],
    "funding": ["funding", "liquidity", "refinancing", "lenders", "covenant", "debt"],
    "earnings": ["earnings", "profit", "margins", "guidance", "revenue", "sales"],
    "legal": ["lawsuit", "regulator", "fine", "probe", "settlement", "court"],
    "deals": ["merger", "takeover", "bid", "acquisition", "shareholders", "offer"],
}
FILL = ["the", "and", "a", "of", "on", "as", "with", "for", "this", "quarter", "analysts", "note", "says",
        "we", "expect", "could", "after", "week", "team", "view", "market", "update", "outlook", "desk"]
STOP_WORDS = ("a", "about", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "in", "is", "it",
              "its", "of", "on", "or", "that", "the", "this", "to", "was", "we", "what", "with")
_TEMPLATES = [
    "{c} {w0} {f0} {w1} {f1} {c} {w2} {f2} {f3}",
    "{f0} {c} {w0} {f1} {w1} {f2} {c} {w2}",
    "{c} {f0} {f1} {w0} {w1} {f2} {f3} {w2}",
]


def make_notes(seed=4):
    g = random.Random(seed)
    notes = []
    for c in COMPANIES:
        for t, pool in TOPICS.items():
            for _ in range(3):
                ws = g.sample(pool, 3)
                fs = g.sample(FILL, 4)
                if g.random() < 0.5:
                    other = g.choice([u for u in TOPICS if u != t])
                    fs[3] = g.choice(TOPICS[other])
                tpl = g.choice(_TEMPLATES)
                text = tpl.format(c=c, w0=ws[0], w1=ws[1], w2=ws[2], f0=fs[0], f1=fs[1], f2=fs[2], f3=fs[3])
                notes.append({"company": c, "topic": t, "text": text})
    for _ in range(36):
        t1, t2 = g.sample(list(TOPICS), 2)
        fs = g.sample(FILL, 4)
        text = f"{fs[0]} {g.choice(TOPICS[t1])} {fs[1]} {g.choice(TOPICS[t1])} {fs[2]} {g.choice(TOPICS[t2])} {fs[3]}"
        notes.append({"company": "", "topic": t1, "text": text})
    g.shuffle(notes)
    notes = [{"id": i, "company": n["company"], "topic": n["topic"], "text": n["text"]} for i, n in enumerate(notes)]
    combos = [(c, t) for c in COMPANIES for t in TOPICS]
    g.shuffle(combos)
    queries = []
    for c, t in combos[:20]:
        ws = g.sample(TOPICS[t], 2)
        rel = [n["id"] for n in notes if n["company"] == c and n["topic"] == t]
        queries.append({"text": f"{c} {ws[0]} {ws[1]}", "relevant": rel})
    return {"notes": notes, "queries": queries}


def load_notes(path="llm-apps-notes.json"):
    with open(path, encoding="utf8") as f:
        return json.load(f)


def make_reports(notes, seed=11, per=6):
    g = random.Random(seed)
    order = [n["id"] for n in notes]
    g.shuffle(order)
    text = {n["id"]: n["text"] for n in notes}
    return [{"ids": order[i:i + per], "text": ". ".join(text[j] for j in order[i:i + per]) + "."}
            for i in range(0, len(order), per)]


def tokenise(text):
    return re.findall(r"[a-z]+", text.lower())


def fit_tfidf(docs, stop_words=()):
    stop = set(stop_words)
    toks = [[w for w in tokenise(d) if w not in stop] for d in docs]
    vocab = sorted({w for t in toks for w in t})
    index = {w: i for i, w in enumerate(vocab)}
    df = np.zeros(len(vocab))
    for t in toks:
        for w in set(t):
            df[index[w]] += 1
    idf = np.log((1 + len(docs)) / (1 + df)) + 1
    X = np.zeros((len(docs), len(vocab)))
    for i, t in enumerate(toks):
        for w in t:
            X[i, index[w]] += 1
    X = X * idf
    n = np.linalg.norm(X, axis=1, keepdims=True)
    X = np.where(n > 0, X / np.where(n > 0, n, 1.0), 0.0)
    return {"vocab": vocab, "index": index, "idf": idf, "X": X}


def embed(text, model, stop_words=()):
    stop = set(stop_words)
    v = np.zeros(len(model["vocab"]))
    for w in tokenise(text):
        if w in model["index"] and w not in stop:
            v[model["index"][w]] += 1
    v = v * model["idf"]
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def rank(text, model, stop_words=()):
    s = model["X"] @ embed(text, model, stop_words)
    return [int(j) for j in np.argsort(-s, kind="stable")]
