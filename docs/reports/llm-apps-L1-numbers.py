"""llm-apps level 1 (Retrieval): every stated number recomputed by a second route.

Route A is the content builder (NumPy, `llm_apps_ops_l1`). Route B here: pure-Python TF-IDF and cosines with Fractions and math.log,
scikit-learn's TfidfVectorizer(token_pattern='[a-z]+') for IDF and rows, LSA by an eigen-decomposition of X^T X instead of an SVD,
recall and MRR by hand loops; every code widget's hidden tests are rerun in CPython with its solution and with an independent twin,
and every mutant is checked to fail its named test first. Strict coverage. Run through tools/run-number-scripts.mjs (venv Python).
Run by hand with OMP_NUM_THREADS=1: BLAS threads make this script several times slower.
"""
import json, math, os, sys, random, re, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
sys.path.insert(0, DATA)
import numpy as np
from numbers_lib import Level, ZQ_LIB
import llm_apps_ops_l1 as ops
from sklearn.feature_extraction.text import TfidfVectorizer

lv = Level("llm-apps", 1, coverage="strict")
F = lv.files
STOP = ops.STOP_WORDS


def close(a, b, t=1e-9):
    return abs(a - b) <= t


# ------------------------------------------------------------------ route B: pure Python retrieval
def tok(s):
    out, cur = [], ''
    for ch in s.lower():
        if 'a' <= ch <= 'z':
            cur += ch
        elif cur:
            out.append(cur); cur = ''
    if cur:
        out.append(cur)
    return out


def b_idf(docs, stop=()):
    n = len(docs)
    df = {}
    for d in docs:
        for w in {w for w in tok(d) if w not in stop}:
            df[w] = df.get(w, 0) + 1
    return {w: math.log((1 + n) / (1 + c)) + 1 for w, c in df.items()}


def b_vec(text, idf, stop=()):
    v = {}
    for w in tok(text):
        if w in idf and w not in stop:
            v[w] = v.get(w, 0.0) + idf[w]
    L = math.sqrt(sum(x * x for x in v.values()))
    return {w: x / L for w, x in v.items()} if L else {}


def b_cos(u, v):
    return sum(x * v.get(w, 0.0) for w, x in u.items())


def b_rank(text, docs, stop=()):
    idf = b_idf(docs, stop)
    q = b_vec(text, idf, stop)
    s = [b_cos(q, b_vec(d, idf, stop)) for d in docs]
    return sorted(range(len(docs)), key=lambda i: (-s[i], i)), s


def b_chunk(text, size, overlap):
    w = text.split()
    out = []
    i = 0
    while i < len(w):
        out.append(' '.join(w[i:i + size]))
        if i + size >= len(w):
            break
        i += size - overlap
    return out


def b_lsa(X, k):
    """Second route for LSA: eigenvectors of X^T X give V, D = X V; the same sign rule (largest entry of each column of U = D / s positive)."""
    X = np.asarray(X, float)
    w, V = np.linalg.eigh(X.T @ X)
    order = np.argsort(-w)[:k]
    V = V[:, order]
    D = X @ V
    for j in range(k):
        col = D[:, j]
        if col[np.argmax(np.abs(col))] < 0:
            D[:, j] *= -1; V[:, j] *= -1
    return D, V


def b_cosv(a, b):
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
    return 0.0 if na == 0 or nb == 0 else sum(x * y for x, y in zip(a, b)) / (na * nb)


def b_recall(ranked, rel, k):
    rel = set(rel)
    return None if not rel else sum(1 for d in set(ranked[:k]) if d in rel) / len(rel)


# ------------------------------------------------------------------ the corpus file and the module
NOTES = json.load(open(os.path.join(DATA, 'llm-apps-notes.json')))
gen = ops.make_notes(4)
lv.claim(NOTES['notes'] == gen['notes'] and NOTES['queries'] == gen['queries'], 'llm-apps-notes.json equals make_notes(seed=4)')
NT = [n['text'] for n in NOTES['notes']]
QS = NOTES['queries']
lv.claim(len(NT) == 180 and sum(1 for n in NOTES['notes'] if n['company']) == 144 and len(QS) == 20 and all(len(q['relevant']) == 3 for q in QS),
         '180 notes (144 company notes, 36 market notes), 20 queries with 3 relevant notes each', covers=[180, 144, 36, 20])
lv.claim(len({(n['company'], n['topic']) for n in NOTES['notes'] if n['company']}) == 48, '8 companies by 6 topics')
lv.claim(os.path.getsize(os.path.join(DATA, 'llm-apps-notes.json')) < 262144, 'notes file under 256 KB')
M = ops.fit_tfidf(NT)
sk = TfidfVectorizer(token_pattern='[a-z]+')
Xs = sk.fit_transform(NT).toarray()
lv.claim(list(sk.get_feature_names_out()) == M['vocab'] and np.allclose(sk.idf_, M['idf'], atol=1e-12) and np.allclose(Xs, M['X'], atol=1e-12),
         'ops.fit_tfidf equals scikit-learn TfidfVectorizer on the 180 notes (vocabulary, IDF and rows)')
bi = b_idf(NT)
lv.claim(all(close(bi[w], M['idf'][j]) for j, w in enumerate(M['vocab'])), 'ops IDF equals the pure-Python IDF')

# ------------------------------------------------------------------ l1
D4 = ["rates rise as inflation stays high", "bank shares rise on higher rates", "oil falls as supply grows", "inflation falls and bonds rally"]
s4 = TfidfVectorizer(token_pattern='[a-z]+').fit(D4)
idf4 = dict(zip(s4.get_feature_names_out(), s4.idf_))
lv.claim(len(idf4) == 17, 'four notes, 17 distinct words', covers=[17])
i_inf, i_one = math.log(5 / 3) + 1, math.log(5 / 2) + 1
lv.claim(close(idf4['inflation'], i_inf) and close(idf4['and'], i_one) and close(idf4['oil'], i_one), 'IDF of inflation 1.5108 and of a one-note word 1.9163 (scikit-learn = formula)')
l1 = 'l1-words-as-weights'
for path in ('screens[2].widget.rows[0][1].answer', 'screens[2].widget.rows[1][1].answer', 'screens[2].widget.rows[3][1].answer'):
    lv.expect(l1, path, 2)
lv.expect(l1, 'screens[2].widget.rows[2][1].answer', 1)
lv.claim([sum(1 for d in D4 if w in tok(d)) for w in ('inflation', 'rates', 'and', 'as')] == [2, 2, 1, 2], 'df of inflation, rates, and, as = 2, 2, 1, 2')
lv.expect(l1, 'screens[3].widget.answer', round(i_inf, 4))
lv.expect(l1, 'screens[3].explain.text', round(i_one, 4))
lv.expect(l1, 'screens[3].widget.wrong[0].value', round(math.log(5 / 3), 4))
lv.expect(l1, 'screens[3].widget.wrong[1].value', round(math.log(2), 4))
lv.expect(l1, 'screens[3].widget.wrong[2].value', round(math.log(2) + 1, 4))
L1 = math.sqrt(sum(b_idf(D4)[w] ** 2 for w in tok(D4[0])))
lv.expect(l1, 'screens[4].widget.answer', round(L1, 4))
lv.expect(l1, 'screens[4].hints[2].text', round(4 * round(i_inf, 4) ** 2 + 2 * round(i_one, 4) ** 2, 4))
lv.expect(l1, 'screens[4].widget.wrong[0].value', round(4 * i_inf + 2 * i_one, 4))
lv.expect(l1, 'screens[4].widget.wrong[1].value', round(L1 ** 2, 4))
lv.expect(l1, 'screens[5].widget.answer', round(i_inf / L1, 4))
lv.claim(close(round(i_inf / L1, 4), round(s4.transform([D4[0]]).toarray()[0][list(s4.get_feature_names_out()).index('inflation')], 4)), "0.3722 is scikit-learn's weight for 'inflation' in note 1")
lv.expect(l1, 'screens[5].explain.text', round(i_one / L1, 4))
lv.expect(l1, 'screens[5].feedback.byKey.by-sum', round(4 * i_inf + 2 * i_one, 4))
lv.expect(l1, 'screens[5].widget.wrong[0].value', round(i_inf / (4 * i_inf + 2 * i_one), 4))
lv.expect(l1, 'screens[5].widget.wrong[1].value', round(i_inf / L1 ** 2, 4))
lv.expect(l1, 'screens[6].widget.answer', round(i_one, 4))
lv.expect(l1, 'screens[6].widget.wrong[1].value', round(math.log(5 / 2), 4))
lv.claim(close(math.log(2 / 2) + 1, 1.0), 'IDF fitted on the query alone: ln(2/2) + 1 = 1', covers=[1])
lv.claim(close(math.log(5 / 5) + 1, 1.0), 'a word in all four notes: ln(5/5) + 1 = 1')
ra, rc = math.log(201 / 5) + 1, math.log(201 / 197) + 1
lv.expect(l1, 'screens[10].widget.answer', round(ra / rc, 2))
lv.expect(l1, 'screens[10].explain.text', round(ra, 4))
lv.expect(l1, 'screens[10].explain.text', round(rc, 4))
lv.expect(l1, 'screens[10].widget.wrong[0].value', round(math.log(200 / 4) / math.log(200 / 196), 1))
lv.claim(196 / 4 == 49, "df ratio 196/4 = 49 (a slip)", covers=[49, 196, 200])
# quiz
lv.expect(l1, 'quiz[1].widget.answer', round(math.log(10 / 3) + 1, 4))
lv.expect(l1, 'quiz[1].widget.wrong[0].value', round(math.log(10 / 3), 4))
lv.expect(l1, 'quiz[1].widget.wrong[1].value', round(math.log(9 / 2) + 1, 4))
lv.expect(l1, 'quiz[3].widget.answer', round(2.5 / math.sqrt(2 * 2.5 ** 2), 4))
lv.claim(close(math.sqrt(12.5), 3.5355, 5e-5), 'sqrt(12.5) = 3.5355', covers=[3.5355, 12.5, 2.5])

# ------------------------------------------------------------------ l2
l2 = 'l2-the-closest-document'
order4, c4 = b_rank("inflation and rates", D4)
STOP3 = ('and', 'as', 'on')
order4s, c4s = b_rank("inflation and rates", D4, STOP3)
lv.claim(order4 == [3, 0, 1, 2] and order4s == [0, 3, 1, 2], 'note 4 first with stop words kept, note 1 first without')
for v in c4:
    lv.expect(l2, 'screens[1].canvas', round(v, 4))
for v in c4s:
    lv.expect(l2, 'screens[1].canvas.controls', round(v, 4))
idf = b_idf(D4)
q = b_vec("inflation and rates", idf)
n4 = b_vec(D4[3], idf)
lv.claim(close(round(q['and'], 4), 0.6677, 1e-12) and close(round(q['inflation'], 4), 0.5264, 1e-12) and close(round(n4['and'], 4), 0.4855, 1e-12) and close(round(n4['inflation'], 4), 0.3827, 1e-12),
         'query weights 0.6677 and 0.5264; note 4 weights 0.4855 and 0.3827', covers=[0.6677, 0.5264, 0.4855, 0.3827])
lv.expect(l2, 'screens[0].widget.answer', round(c4[3], 4))
lv.claim(round(0.6677 * 0.4855 + 0.5264 * 0.3827, 4) == round(c4[3], 4), 'printed products give 0.5256')
lv.expect(l2, 'screens[0].explain.text', round(0.6677 * 0.4855, 4))
lv.expect(l2, 'screens[0].explain.text', round(0.5264 * 0.3827, 4))
lv.expect(l2, 'screens[0].widget.wrong[0].value', round(n4['and'] + n4['inflation'], 4))
lv.expect(l2, 'screens[0].widget.wrong[1].value', round(q['inflation'] * n4['inflation'], 4))
lv.expect(l2, 'screens[0].feedback.correct', round(c4[0], 4))
qs3 = b_vec("inflation and rates", b_idf(D4, STOP3), STOP3)
n1s = b_vec(D4[0], b_idf(D4, STOP3), STOP3)
lv.claim(close(round(qs3['rates'], 5), 0.70711, 1e-12) and close(round(n1s['inflation'], 5), 0.40104, 1e-12), 'without stop words: query 0.70711 each, note 1 0.40104', covers=[0.70711, 0.40104])
lv.expect(l2, 'screens[2].widget.answer', round(c4s[0], 4))
lv.expect(l2, 'screens[2].explain.text', round(0.70711 * 0.40104, 4))
lv.claim(round(2 * 0.70711 * 0.40104, 4) == round(c4s[0], 4), 'printed 2 x 0.70711 x 0.40104 = 0.5672')
lv.expect(l2, 'screens[2].widget.wrong[0].value', round(n1s['inflation'] / math.sqrt(2), 4))
lv.expect(l2, 'screens[1].widget.options', round(c4s[3], 4))
lv.expect(l2, 'screens[1].widget.options', round(c4s[1], 4))
lv.claim(close(0.6 * 0.8 + 0.8 * 0 + 0 * 0.6, 0.48), 'cosine of (0.6, 0.8, 0) and (0.8, 0, 0.6) = 0.48', covers=[0.48, 0.6, 0.8, 1.4])
lv.expect(l2, 'screens[3].widget.answer', 0.48)
# a note pasted twice keeps its direction: check with the fitted IDF held fixed
v4 = {}
for w in tok(D4[3]):
    v4[w] = v4.get(w, 0.0) + idf[w]
v4d = {w: 2 * x for w, x in v4.items()}
lv.claim(close(b_cos(q, {w: x / math.sqrt(sum(y * y for y in v4d.values())) for w, x in v4d.items()}), c4[3]) and close(sum(q.get(w, 0) * x for w, x in v4d.items()), 2 * sum(q.get(w, 0) * x for w, x in v4.items())),
         'doubled note: same cosine 0.5256, dot product doubles')
lv.expect(l2, 'screens[4].widget.wrong[0].value', round(2 * c4[3], 4))
lv.expect(l2, 'screens[5].widget.answer', round(q['inflation'] * n4['inflation'], 4))
lv.expect(l2, 'screens[5].widget.wrong[0].value', round(q['and'] * n4['and'], 4))
lv.claim(q['and'] * n4['and'] > c4[3] / 2, "more than half of note 4's score comes from 'and'")
lv.claim(b_vec("gilt yields", idf) == {}, 'gilt yields: no known word, zero vector')
AP = ["apple harvest results hit by frost", "apple shares rise after record results", "orchard frost cuts the pear crop", "chip maker results beat forecasts"]
oa, ca = b_rank("apple results", AP, STOP)
lv.expect(l2, 'screens[10].prose', round(ca[0], 4))
lv.expect(l2, 'screens[10].prose', round(ca[1], 4))
for v in ca:
    lv.expect(l2, 'screens[10].canvas', round(v, 4))
lv.expect(l2, 'quiz[0].widget.answer', 0.96)
lv.claim(close(0.8 * 0.6 * 2, 0.96), '(0.8, 0.6).(0.6, 0.8) = 0.96', covers=[0.96, 0.48])
lv.expect(l2, 'quiz[1].widget.answer', 3.6)
lv.claim(close(2 * 1.8, 3.6), 'doubled dot product 3.6', covers=[1.8])
lv.expect(l2, 'quiz[2].explain.text', round(math.log(6 / 2) + 1, 4))

# ------------------------------------------------------------------ l3
l3 = 'l3-search-by-meaning'
M8 = ["gilt yields rise as rates climb", "rates and inflation push yields higher", "inflation lifts rates again", "yields fall as inflation cools",
      "lenders cut credit lines to the firm", "the firm seeks new funding from lenders", "funding gap widens as lenders pull credit", "higher rates squeeze funding for the firm"]
m8 = ops.fit_tfidf(M8, STOP)
lv.claim(b_rank("bond yields", M8, STOP)[1][2] == 0, 'TF-IDF cosine of bond yields and note 3 is 0')
D8, V8 = b_lsa(m8['X'], 2)
q8 = ops.embed("bond yields", m8, STOP) @ V8
lv.claim(np.allclose(D8 @ np.diag([1, 1]), np.asarray([[p['x'], p['y']] for p in F[l3]['screens'][1]['canvas']['params']['points'][:8]]), atol=6e-4)
         and np.allclose(q8, [F[l3]['screens'][1]['canvas']['params']['points'][8]['x'], F[l3]['screens'][1]['canvas']['params']['points'][8]['y']], atol=6e-4),
         'scatter points equal the LSA coordinates by the eigen route (3 places)')
lc = [b_cosv(q8, d) for d in D8]
lv.claim(sorted(range(8), key=lambda i: -lc[i])[:4] == [3, 0, 2, 1], 'by LSA cosine the four rates notes come first')
qx, qy = round(q8[0], 3), round(q8[1], 3)
n3x, n3y = round(D8[2][0], 3), round(D8[2][1], 3)
lv.claim((qx, qy, n3x, n3y) == (0.32, -0.287, 0.467, -0.353), 'printed Q and note 3 coordinates', covers=[0.32, 0.287, 0.467, 0.353])
cp_ = b_cosv([qx, qy], [n3x, n3y])
lv.expect(l3, 'screens[2].widget.answer', round(cp_, 4))
lv.claim(close(round(lc[2], 4), round(cp_, 4)), 'unrounded LSA cosine also 0.9965')
lv.expect(l3, 'screens[2].explain.text', round(qx * n3x + qy * n3y, 4))
lv.expect(l3, 'screens[2].explain.text', round(math.hypot(qx, qy), 4))
lv.expect(l3, 'screens[2].explain.text', round(math.hypot(n3x, n3y), 4))
lv.expect(l3, 'screens[2].widget.wrong[0].value', round(qx * n3x + qy * n3y, 4))
P16 = "sales held up but the going concern doubt from auditors hit the shares hard this week"
lv.claim(len(P16.split()) == 16, '16-word passage', covers=[16])
lv.expect(l3, 'screens[3].widget.answer', len(b_chunk(P16, 6, 2)))
lv.expect(l3, 'screens[3].widget.wrong[0].value', len(b_chunk(P16, 6, 0)))
lv.claim(b_chunk(P16, 6, 2)[1] == 'the going concern doubt from auditors' and all('going concern doubt' not in c for c in b_chunk(P16, 6, 0)) and all('going concern doubt' not in c for c in b_chunk(P16, 3, 0)), 'overlap 2 keeps the phrase whole; overlap 0 and size 3 split it')
cw, cf = 3 / math.sqrt(3 * 6), 3 / math.sqrt(3 * 18)
lv.claim(sum(c * c for c in [P16.split().count(w) for w in set(P16.split())]) == 18, "passage squared length 18 ('the' twice)", covers=[18, 14])
lv.expect(l3, 'screens[5].prose', round(cw, 4))
lv.expect(l3, 'screens[5].widget.answer', round(cf, 4))
lv.expect(l3, 'screens[5].widget.wrong[0].value', round(3 / math.sqrt(48), 4))
lv.claim(close(3 / math.sqrt(54), cf), '3/sqrt(54) = 0.4082', covers=[54])
lv.literal('50-page', why='the size of a broker report in the trap scenario, not a computed figure')
lv.literal('page 37', why='where the breach sits in the trap scenario, a given')
q0 = QS[0]
tfr = [i for i in b_rank(q0['text'], NT)[0][:3]]
X_ = ops.fit_tfidf(NT)['X']
DN, VN = b_lsa(X_, 8)
qN = ops.embed(q0['text'], ops.fit_tfidf(NT)) @ VN
sN = [b_cosv(qN, d) for d in DN]
lsr = sorted(range(180), key=lambda i: (-sN[i], i))[:3]
lv.claim(tfr == [49, 68, 85] and lsr == [49, 72, 54], 'corran refinancing debt: TF-IDF top 3 [49, 68, 85], LSA k = 8 top 3 [49, 72, 54]')
lv.expect(l3, 'screens[10].widget.answer', len(set(lsr) & set(q0['relevant'])))
lv.expect(l3, 'screens[10].widget.wrong[0].value', len(set(tfr) & set(q0['relevant'])))
for j in tfr + lsr:
    lv.expect(l3, 'screens[10]', j)
lv.claim('refinancing' not in NT[54] and 'debt' not in NT[54], "note 54 says neither 'refinancing' nor 'debt'")
lv.expect(l3, 'quiz[0].widget.answer', len(b_chunk(' '.join(map(str, range(20))), 8, 3)))
lv.claim([c.split()[0] for c in b_chunk(' '.join(map(str, range(20))), 8, 3)] == ['0', '5', '10', '15'], '20 words, size 8, overlap 3: starts 0, 5, 10, 15', covers=[17, 19])
lv.literal('3,000', why='the vocabulary size in the LSA quiz scenario, a given')
lv.expect(l3, 'quiz[2].widget.answer', 50)

# ------------------------------------------------------------------ l4
l4 = 'l4-did-we-find-it'
lv.expect(l4, 'screens[0].widget.answer', b_recall([4, 1, 2, 3], [1, 4], 1))
q1 = QS[1]
r1 = b_rank(q1['text'], NT)[0][:6]
pos = [i + 1 for i, j in enumerate(r1) if j in q1['relevant']]
lv.claim(pos == [1, 2, 5], 'halloran margins profit: relevant at ranks 1, 2, 5')
lv.expect(l4, 'screens[1].widget.answer', 5)
for j in r1:
    lv.expect(l4, 'screens[1].canvas', j)
lv.expect(l4, 'screens[2].widget.answer', round(2 / 3, 4))
lv.expect(l4, 'screens[2].widget.wrong[0].value', round(2 / 6, 4))
mrr3 = (1 + 1 / 3 + 1 / 2) / 3
lv.expect(l4, 'screens[3].widget.answer', round(mrr3, 4))
lv.expect(l4, 'screens[3].explain.text', round(1 + 1 / 3 + 1 / 2, 4))
lv.claim(close(round(1 / 3, 4), 0.3333), '1/3 = 0.3333', covers=[0.3333])
tfrec = [b_recall(b_rank(q['text'], NT)[0], q['relevant'], 3) for q in QS]
qv = [ops.embed(q['text'], ops.fit_tfidf(NT)) @ VN for q in QS]
lsrec = []
for q, v in zip(QS, qv):
    s = [b_cosv(v, d) for d in DN]
    lsrec.append(b_recall(sorted(range(180), key=lambda i: (-s[i], i)), q['relevant'], 3))
dd = [b - a for a, b in zip(tfrec, lsrec)]
mean_d = statistics.fmean(dd)
sd_d = statistics.stdev(dd)
se_d = sd_d / math.sqrt(20)
lv.claim(close(sum(dd), 4.0), 'differences add up to 4', covers=[4])
lv.expect(l4, 'screens[4].widget.answer', round(mean_d, 2))
lv.expect(l4, 'screens[4].feedback.correct', round(statistics.fmean(lsrec), 4))
lv.expect(l4, 'screens[4].feedback.correct', round(statistics.fmean(tfrec), 4))
lv.expect(l4, 'screens[4].widget.wrong[0].value', round(statistics.fmean(lsrec), 2))
lv.expect(l4, 'screens[5].prose', round(sd_d, 4))
lv.expect(l4, 'screens[5].widget.answer', round(se_d, 4))
lv.expect(l4, 'screens[5].widget.wrong[1].value', round(sd_d / 20, 4))
lv.expect(l4, 'screens[5].feedback.correct', round(mean_d / se_d, 1))
lv.expect(l4, 'screens[5].explain.text', round(math.sqrt(20), 4))
TAB = F[l4]['screens'][4]['canvas']['params']['rows']
fr = {0: '0', 1: '1/3', 2: '2/3', 3: '1'}
lv.claim(all(r[1] == fr[round(a * 3)] and r[2] == fr[round(b * 3)] for r, a, b in zip(TAB, tfrec, lsrec)), 'table of 20 per-query recalls matches route B', covers=[1 / 3, 2 / 3])
lv.claim(all(abs(round(lsr_k, 9) - 1.0) < 1e-9 for lsr_k in [statistics.fmean([b_recall(sorted(range(180), key=lambda i, v=v: (-b_cosv(v, DN13[i]), i)), q['relevant'], 3) for q, v in zip(QS, [ops.embed(q['text'], ops.fit_tfidf(NT)) @ VN13 for q in QS])])
        for DN13, VN13 in [b_lsa(X_, 13)]]), 'LSA at k = 13 gives recall at 3 of 1.0 on the 20 queries', covers=[13, 1.0])
# fresh queries for the trap's last sentence
used = {(n['company'], n['topic']) for q in QS for n in NOTES['notes'] if n['id'] in q['relevant']}
g = random.Random(21)
combos = [(c, t) for c in ops.COMPANIES for t in ops.TOPICS if (c, t) not in used]
g.shuffle(combos)
fresh = []
for c, t in combos[:20]:
    ws = g.sample(ops.TOPICS[t], 2)
    fresh.append((f'{c} {ws[0]} {ws[1]}', [n['id'] for n in NOTES['notes'] if n['company'] == c and n['topic'] == t]))
D13, V13 = b_lsa(X_, 13)
fr13 = statistics.fmean([b_recall(sorted(range(180), key=lambda i, v=ops.embed(t, ops.fit_tfidf(NT)) @ V13: (-b_cosv(v, D13[i]), i)), r, 3) for t, r in fresh])
lv.claim(close(fr13, 1.0), f'on 20 fresh queries k = 13 also gives recall at 3 of {fr13}')
lv.claim(close(statistics.fmean([1, 0.5, 0]), 0.5), 'mean recall over A, B, D = 0.5', covers=[0.5])
lv.expect(l4, 'screens[7].widget.wrong[0].value', 1.5 / 4)
lv.claim(close(2.5 / 4, 0.625) and close(1.5 / 4, 0.375), "counting query C as 1 gives 0.625 and as 0 gives 0.375, exactly the wrong values, with a band of 0.006 that holds the rounded 0.63 and 0.38 too")
lv.expect(l4, 'screens[7].widget.wrong[1].value', 2.5 / 4)
lv.expect(l4, 'screens[11].widget.answer', 38 / 50)
lv.expect(l4, 'screens[11].widget.wrong[1].value', round(38 / 250, 2))
lv.claim(50 * 5 == 250 and 50 - 38 == 12, '50 searches of 5 notes is 250 listed; 12 misses', covers=[250, 12, 38, 50])
lv.expect(l4, 'quiz[1].widget.answer', round((1 + 1 + 0.25 + 0) / 4, 4))
lv.expect(l4, 'quiz[1].widget.wrong[0].value', round(2.25 / 3, 4))
lv.expect(l4, 'quiz[2].widget.answer', round(0.3 / math.sqrt(25), 2))
lv.claim(close(2 / 4, 0.5) and close(2 / 5, 0.4), 'recall 2/4 and precision 2/5', covers=[0.4, 0.5])
lv.claim(0.6 > 0.4, 'B recall at 2 0.6 against A 0.4', covers=[0.6, 0.4, 0.9, 0.7])
lv.literal('0.04, 0.30', why='given mean and standard deviation in the l4 quiz scenario; the standard error built from them is checked')

# ------------------------------------------------------------------ review
lv.expect('review', 'items[0].widget.answer', round(math.log(3) + 1, 4))
lv.expect('review', 'items[0].widget.wrong[1].value', round(math.log(11 / 3) + 1, 4))
lv.expect('review', 'items[1].widget.answer', 0.6)
lv.expect('review', 'items[1].widget.wrong[0].value', round(3 / 7, 2))
lv.claim(close(3 / 5, 0.6) and close(4 / 5, 0.8), '3/5 and 4/5', covers=[0.6, 0.8])
lv.literal('1,000', why='the number of filings in a review scenario, a given')
lv.literal('1001/1001', why='the smooth IDF fraction for df = n = 1,000, shown as the working')
lv.expect('review', 'items[3].widget.answer', 0.64)
lv.expect('review', 'items[5].explain.text', round(6 / math.sqrt(45), 4))
lv.expect('review', 'items[6].widget.answer', len(b_chunk(' '.join(map(str, range(50))), 12, 4)))
lv.claim([c.split()[0] for c in b_chunk(' '.join(map(str, range(50))), 12, 4)] == ['0', '8', '16', '24', '32', '40'], '50 words, size 12, overlap 4: starts 0 to 40', covers=[40, 49, 48])
lv.expect('review', 'items[7].widget.answer', round(0.6 * 0.5 + 0.8 * 0.4, 2))
lv.expect('review', 'items[7].widget.wrong[0].value', round(0.6 * 0.1 - 0.8 * 0.3, 2))
lv.expect('review', 'items[8].widget.answer', round((1 / 2 + 1 / 3) / 2, 4))
lv.expect('review', 'items[8].widget.wrong[0].value', round((1 / 2 + 1 / 3 + 1 / 3) / 2, 4))
lv.expect('review', 'items[9].widget.answer', round(0.4 / math.sqrt(16), 2))
lv.claim(close(0.15 / 0.1, 1.5), 'gap of 0.15 is 1.5 standard errors', covers=[1.5, 0.15, 0.4])

# ------------------------------------------------------------------ homework
lv.expect('homework', 'items[4].widget.answer', (18 + 10 + 4) / 40)
lv.claim(18 + 10 + 4 == 32 and close(18 / 40, 0.45) and close(8 / 40, 0.2), 'log: 32 of 40 in the top 3; recall at 1 0.45', covers=[32, 0.45, 0.2])
lv.literal('4,000', why='the size of the broker-note index in the long-form scenario, a given')
lv.literal('30,000; 150; 300; 3,000; 0.81; 0.62', why='givens of the chunk-size scenario (report and paragraph lengths, two measured recalls stated as data)')
lv.literal('50 to 100', why='a suggested number of labelled queries in the model answer, a recommendation not a result')

# ------------------------------------------------------------------ problem set
P5 = ["freight rates jump as ports clog", "ports reopen and freight eases", "copper demand lifts miners", "miners cut output as copper slides", "freight costs squeeze copper importers"]
idf5 = b_idf(P5, STOP)
lv.expect('problems', 'items[0].parts[0].widget.answer', round(idf5['copper'], 4))
lv.claim(close(idf5['costs'], math.log(3) + 1), 'one-headline words: IDF 2.0986', covers=[round(math.log(3) + 1, 4)])
v5 = b_vec(P5[4], idf5, STOP)
L5 = math.sqrt(2 * idf5['copper'] ** 2 + 3 * idf5['costs'] ** 2)
lv.expect('problems', 'items[0].parts[1].widget.answer', round(v5['copper'], 4))
lv.expect('problems', 'items[0].parts[1].feedback.correct', round(L5, 4))
lv.claim(close(round(2 * 1.4055 ** 2 + 3 * 2.0986 ** 2, 4), 17.1632, 1e-9), 'printed squares sum 17.1632', covers=[17.1632])
qp = b_vec("copper freight", idf5, STOP)
o5, c5 = b_rank("copper freight", P5, STOP)
lv.expect('problems', 'items[0].parts[2].widget.answer', round(c5[4], 4))
lv.claim(round(2 * 0.7071 * 0.3393, 4) == round(c5[4], 4) and close(round(qp['copper'], 4), 0.7071), 'printed 2 x 0.7071 x 0.3393 = 0.4798', covers=[0.7071, 0.3393])
lv.expect('problems', 'items[0].parts[2].explain.text', round(0.7071 * 0.3393, 4))
for i in range(4):
    lv.expect('problems', 'items[0].parts[3].question', round(c5[i], 4))
lv.claim(o5[0] == 4 and o5[1] == 1, 'headline 5 first, headline 2 second (tie with 3 to the lower index)')
lv.expect('problems', 'items[0].parts[4].widget.answer', b_recall(o5, [4, 3], 2))
lv.expect('problems', 'items[1].parts[0].widget.answer', len(b_chunk(' '.join(f'w{i}' for i in range(30)), 10, 3)))
lv.claim([c.split()[0] for c in b_chunk(' '.join(f'w{i}' for i in range(30)), 10, 3)] == ['w0', 'w7', 'w14', 'w21'] and 'w9 w10 w11' in b_chunk(' '.join(f'w{i}' for i in range(30)), 10, 3)[1],
         'windows start at 0, 7, 14, 21; the second holds words 9 to 11', covers=[21, 29, 30])
lv.expect('problems', 'items[1].parts[2].widget.answer', round(3 / math.sqrt(30), 4))
lv.expect('problems', 'items[1].parts[3].widget.answer', round(3 / math.sqrt(90), 4))
lv.expect('problems', 'items[1].parts[2].widget.wrong[1].value', round(3 / math.sqrt(10), 4))
A = [1, 2, 1, 5]
lv.expect('problems', 'items[2].parts[0].widget.answer', round(sum(1 / r for r in A) / 4, 4))
lv.claim(close(sum(1 / r for r in A), 2.7) and close(statistics.fmean(A), 2.25), 'reciprocals sum 2.7; mean rank 2.25', covers=[2.7, 2.25])
dl = [1 / 3, 0, -1 / 3, 1 / 3, 0, 2 / 3]
lv.expect('problems', 'items[2].parts[1].widget.answer', round(statistics.fmean(dl), 4))
lv.expect('problems', 'items[2].parts[2].question', round(statistics.stdev(dl), 4))
sel = statistics.stdev(dl) / math.sqrt(6)
lv.expect('problems', 'items[2].parts[2].widget.answer', round(sel, 4))
lv.expect('problems', 'items[2].parts[2].explain.text', round(math.sqrt(6), 4))
lv.expect('problems', 'items[2].parts[3].feedback.correct', round(statistics.fmean(dl) / sel, 2))
lv.expect('problems', 'items[2].parts[1].widget.wrong[1].value', round(1 / 5, 4))

# ------------------------------------------------------------------ every code widget: solution, twin, starter and mutants in CPython
TWINS = {
    'idf': """
def tokenise(text):
    out, cur = [], ''
    for ch in text.lower():
        if 'a' <= ch <= 'z':
            cur += ch
        elif cur:
            out.append(cur); cur = ''
    return out + ([cur] if cur else [])
def idf(docs):
    from sklearn.feature_extraction.text import TfidfVectorizer
    v = TfidfVectorizer(token_pattern='[a-z]+').fit(docs)
    return dict(zip(v.get_feature_names_out(), (float(x) for x in v.idf_)))
""",
    'tfidf_matrix': """
def tfidf_matrix(docs):
    from sklearn.feature_extraction.text import TfidfVectorizer
    v = TfidfVectorizer(token_pattern='[a-z]+')
    X = v.fit_transform(docs).toarray()
    return list(v.get_feature_names_out()), X.tolist()
""",
    'rank': """
import math
def cosine(a, b):
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(x * x for x in b))
    return 0.0 if na == 0 or nb == 0 else sum(x * y for x, y in zip(a, b)) / (na * nb)
def rank(query, docs, stop_words=()):
    from sklearn.feature_extraction.text import TfidfVectorizer
    v = TfidfVectorizer(token_pattern='[a-z]+', stop_words=list(stop_words) or None)
    X = v.fit_transform(docs).toarray(); q = v.transform([query]).toarray()[0]
    if not q.any():
        return []
    s = [float(r @ q) for r in X]
    return sorted(range(len(docs)), key=lambda i: (-s[i], i))
""",
    'top_k': """
def top_k(query, docs, k):
    from sklearn.feature_extraction.text import TfidfVectorizer
    v = TfidfVectorizer(token_pattern='[a-z]+', stop_words=list(STOP))
    X = v.fit_transform(docs).toarray(); q = v.transform([query]).toarray()[0]
    s = [float(r @ q) for r in X]
    return [i for i in sorted(range(len(docs)), key=lambda i: (-s[i], i)) if s[i] > 0][:k]
""",
    'lsa_embed': """
import numpy as np
def lsa_embed(X, k):
    X = np.asarray(X, float)
    w, V = np.linalg.eigh(X.T @ X)
    V = V[:, np.argsort(-w)[:k]]
    D = X @ V
    for j in range(k):
        if D[np.argmax(np.abs(D[:, j])), j] < 0:
            D[:, j] *= -1; V[:, j] *= -1
    return D, V
""",
    'chunk': """
import math
def chunk(text, size, overlap):
    w = text.split()
    if not w:
        return []
    n = 1 if len(w) <= size else 1 + math.ceil((len(w) - size) / (size - overlap))
    return [' '.join(w[i * (size - overlap): i * (size - overlap) + size]) for i in range(n)]
def search(query_vec, doc_vecs, k):
    def c(a, b):
        na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(x * x for x in b))
        return 0.0 if na == 0 or nb == 0 else sum(x * y for x, y in zip(a, b)) / (na * nb)
    if not any(query_vec):
        return []
    s = [c(list(query_vec), list(r)) for r in doc_vecs]
    return sorted(range(len(s)), key=lambda i: (-s[i], i))[:k]
""",
    'recall_at_k': """
from fractions import Fraction
def recall_at_k(ranked, relevant, k):
    r = set(relevant)
    if len(r) == 0:
        return None
    return float(Fraction(len([d for d in set(ranked[:k]) if d in r]), len(r)))
def mrr(rankings, relevants):
    tot, n = Fraction(0), 0
    for L, R in zip(rankings, relevants):
        if not R:
            continue
        n += 1
        for i, d in enumerate(L):
            if d in R:
                tot += Fraction(1, i + 1); break
    return float(tot / n)
""",
    'compare': """
import statistics, math
def compare(r1, r2, queries, k):
    d = []
    for t, rel in queries:
        if not set(rel):
            continue
        a, b = r1(t), r2(t)
        d.append(len(set(a[:k]) & set(rel)) / len(set(rel)) - len(set(b[:k]) & set(rel)) / len(set(rel)))
    return statistics.fmean(d), statistics.stdev(d) / math.sqrt(len(d))
""",
    'build_index': """
import numpy as np, re
from llm_apps_ops_l1 import STOP_WORDS as STOP
def build_index(docs):
    chunks, owner = [], []
    for i, d in enumerate(docs):
        w = re.findall('[a-z]+', d.lower())
        s = 0
        while s < len(w):
            chunks.append(' '.join(x for x in w[s:s + 12] if x not in STOP)); owner.append(i)
            if s + 12 >= len(w):
                break
            s += 8
    from sklearn.feature_extraction.text import TfidfVectorizer
    v = TfidfVectorizer(token_pattern='[a-z]+')
    X = v.fit_transform(chunks).toarray()
    return v, X, owner
def query(index, text, k):
    v, X, owner = index
    q = v.transform([' '.join(x for x in re.findall('[a-z]+', text.lower()) if x not in STOP)]).toarray()[0]
    if not q.any():
        return []
    s = X @ q
    best = {}
    for sc, o in zip(s, owner):
        if sc > 1e-12 and sc > best.get(o, 0):
            best[o] = sc
    return sorted(best, key=lambda o: (-best[o], o))[:k]
""",
    'reciprocal_rank': """
import statistics, math
def reciprocal_rank(ranked, relevant):
    for i, d in enumerate(ranked, start=1):
        if d in set(relevant):
            return 1 / i
    return 0.0
def paired_gap(a, b):
    d = [x - y for x, y in zip(a, b) if x is not None and y is not None]
    return statistics.fmean(d), statistics.stdev(d) / math.sqrt(len(d))
""",
}


def norm(v):
    if hasattr(v, 'tolist'):
        v = v.tolist()
    if isinstance(v, tuple):
        v = list(v)
    return [norm(x) for x in v] if isinstance(v, list) else v


def same(a, b, cmp, tol):
    a, b = norm(a), norm(b)
    if isinstance(a, list) or isinstance(b, list):
        return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(same(x, y, cmp, tol) for x, y in zip(a, b))
    if cmp == 'isclose' and isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        rel = (tol or {}).get('rel', 1e-9 if not tol else 0) or 0
        ab = (tol or {}).get('abs', 1e-12 if not tol else 0) or 0
        return math.isclose(a, b, rel_tol=rel, abs_tol=ab)
    return a == b


def run(w, src):
    cwd = os.getcwd()
    os.chdir(DATA)
    res = []
    try:
        ns = {'__name__': '__zq__', '__learner_source__': src}
        exec(ZQ_LIB, ns)
        try:
            exec(w.get('prelude', ''), ns)
            exec(src, ns)
        except Exception:
            return [False] * len(w['tests'])
        for t in w['tests']:
            try:
                if t.get('setup'):
                    exec(t['setup'], ns)
                res.append(same(eval(t['call'], ns), eval(t['expect'], ns), t.get('compare', 'equal'), t.get('tol')))
            except Exception:
                res.append(False)
    finally:
        os.chdir(cwd)
    return res


def widgets(doc):
    for key in ('screens', 'items'):
        for i, s in enumerate(doc.get(key, [])):
            w = s.get('widget')
            if isinstance(w, dict) and w.get('kind') == 'code':
                yield f'{key}[{i}]', w, s.get('feedback', {}).get('byKey', {})


n_code = 0
for fid, doc in F.items():
    for path, w, bk in widgets(doc):
        n_code += 1
        r = run(w, w['solution'])
        lv.claim(all(r), f'{fid} {path}: the model solution passes all {len(r)} hidden tests in CPython')
        name = next(k for k in TWINS if f'def {k}(' in w['solution'])
        rt = run(w, TWINS[name])
        lv.claim(all(rt), f'{fid} {path}: an independent twin ({name}, scikit-learn or loops) passes them too' + ('' if all(rt) else f' (fails {[i + 1 for i, x in enumerate(rt) if not x]})'))
        lv.claim(not all(run(w, w['starter'])), f'{fid} {path}: the starter fails')
        ms = w.get('mutants', [])
        lv.claim(len(ms) >= 2, f'{fid} {path}: {len(ms)} mutants')
        for m in ms:
            rm = run(w, m['source'])
            first = next((i + 1 for i, x in enumerate(rm) if not x), None)
            lv.claim(first == m['test'] and f"test-{m['test']}" in bk, f"{fid} {path}: mutant '{m['symptom'][:40]}' first fails test {m['test']}, which has a byKey line")
        lv.claim(all(any(m['test'] == int(k.split('-')[1]) for m in ms) for k in bk if k.startswith('test-')), f'{fid} {path}: every byKey test line is reached by a mutant')
lv.claim(n_code == 10, f'{n_code} code widgets in the level')

# exact-list tests must not hang on a floating tie: the scores around each cut are well apart
nsH = {}
exec(F['homework-1']['items'][0]['widget']['solution'], nsH)
REPS = ops.make_reports(NOTES['notes'])
DOCS = [r['text'] for r in REPS]
ixH = nsH['build_index'](DOCS)
gq = random.Random(99)
cmb = [(c, t) for c in ops.COMPANIES for t in ops.TOPICS]
gq.shuffle(cmb)
WHERE = {i: ri for ri, r in enumerate(REPS) for i in r['ids']}
HQ = []
for c, t in cmb[:24]:
    a, b = gq.sample(ops.TOPICS[t], 2)
    HQ.append((f'what about {c} and {a} or {b}', sorted({WHERE[n['id']] for n in NOTES['notes'] if n['company'] == c and n['topic'] == t})))


def doc_scores(ix, text):
    q = {}
    for t in re.findall('[a-z]+', text.lower()):
        if t in ix['col'] and t not in nsH['STOP']:
            q[ix['col'][t]] = q.get(ix['col'][t], 0) + ix['idf'][ix['col'][t]]
    L = math.sqrt(sum(v * v for v in q.values()))
    best = {}
    for row, d in zip(ix['rows'], ix['owner']):
        s = sum(v * row.get(j, 0) for j, v in q.items()) / L
        best[d] = max(best.get(d, 0), s)
    return sorted(best.values(), reverse=True)


gaps = []
for qi, kk in ((0, 3), (1, 3), (2, 3), (5, 6)):
    sc = doc_scores(ixH, HQ[qi][0])
    gaps.append(min(sc[i] - sc[i + 1] for i in range(kk)))
lv.claim(min(gaps) > 1e-6, f'homework report queries: no near-tie at the cut (smallest gap {min(gaps):.2e})')
recH = statistics.fmean(len(set(nsH['query'](ixH, t, 3)) & set(r)) / len(r) for t, r in HQ)
lv.claim(recH >= 0.5 + 0.05, f'homework: model recall at 3 on 24 hidden questions {recH:.4f}, above the 0.5 bar with margin', covers=[0.5])
nsW = {}
exec(F['homework-1']['items'][0]['widget']['mutants'][0]['source'], nsW)
recW = statistics.fmean(len(set(nsW['query'](nsW['build_index'](DOCS), t, 3)) & set(r)) / len(r) for t, r in HQ)
lv.claim(recW < 0.5, f'homework: indexing whole reports gives {recW:.4f}, under the bar')
lv.claim(len(REPS) == 30 and len(HQ) == 24, '30 reports, 24 hidden questions', covers=[30, 24])
lv.claim(tuple(nsH['STOP']) == tuple(ops.STOP_WORDS), "the homework's STOP list equals the module's STOP_WORDS (the twin uses the module's)")
# fractions, words and small figures stated in working, each recomputed
lv.claim(close((1 + 4) / (1 + 2), 5 / 3) and close((1 + 4) / (1 + 3), 5 / 4) and close((1 + 200) / (1 + 4), 201 / 5) and close((1 + 9) / (1 + 2), 10 / 3),
         'fractions inside the logs: 5/3, 5/4 (a slip), 201/5, 10/3 (n = 9)', covers=[5 / 3, 5 / 4, 201 / 5, 10 / 3, 9])
lv.claim(close((1 + 5) / (1 + 1), 6 / 2) and close((1 + 11) / (1 + 3), 12 / 4), 'fractions 6/2 (five notes, df 1) and 12/4 (eleven notes, df 3)', covers=[6 / 2, 12 / 4])
lv.claim(all(close(v4d[w], 2 * v4[w]) for w in v4) and P16.split().count('the') == 2, "'twice' = 2: a note pasted twice doubles every count; 'the' appears twice in the passage", covers=[2])
lv.claim(len(P16.split()) - 1 == 15 and 20 - 1 == 19, 'the last word of the 16-word passage is word 15', covers=[15])
lv.claim(close((1 / 1) / (1 / 3), 3) and close(6 / 2, 3), "'three times': a first hit at rank 1 counts three times one at rank 3; the long note's dot product 6 is three times 2", covers=[3])
lv.claim(5 ** 2 == 25 and 3 ** 2 + 4 ** 2 == 25, 'sqrt(25) = 5 in the SE quiz; 3^2 + 4^2 = 25 in the review', covers=[25])
lv.claim(30 - 3 == 27, 'the whole paragraph has 27 words besides the three matches', covers=[27])
lv.literal('12, 8, 4', why='window size, step and overlap the homework task specifies; the tests run them')
lv.literal('$10^{-9}$, $10^{-12}$, $2 \\times 10^{-6}$, 6 places', why='tolerances named in how lines are settings of the hidden tests, which this script runs')
lv.check_wrongs()
lv.report()
