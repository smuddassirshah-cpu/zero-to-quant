# llm-apps (Language Models at Work) L1 to L3: second-reader findings

Scope: every file in `app/content/courses/llm-apps/` (12 lessons, 3 reviews, 3 homeworks, 3 problem sets, `course.json`), the modules `app/content/data/ai/llm_apps_ops_l1.py` to `_l3.py`, and `llm-apps-notes.json`.
Method: no browser. Modules read against their docstrings and tried on edge cases. The three number scripts run through `run-number-scripts.mjs --only llm-apps` and directly with `ZQ_NUMBERS_STRICT=1`. `llm-apps-notes.json` compared with `make_notes(seed=4)`. `grade-all.mjs --file <f> --code --strict-feedback --local-cdn <pkgs>` run on each of the 21 files on its own. `same-course-reuse.mjs --all` filtered for errors. 23 own solutions run against the hidden tests through `tools/code-runner.mjs`, the page's own harness (appendix). Every stated number recomputed independently: the seeded market, TF-IDF, LSA, chunking, recall, MRR, standard errors, haircuts, closes and agent counts. Distractors re-derived from their `why`. Prose read against Anthropic's "Building effective agents" and the quant lessons it cites. `voice-scan.py 35`, plus my own greps for em-dashes, exclamation marks and American spellings.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation or teaching issue, or a wrong solution that survives; note = style or small.

Counts: 4 errors, 12 warnings, 19 notes. Wrong solutions: 21 tried, 7 survive (W03, W04, W05, W08, W18, W19, W20). W17 is a correct-in-spirit solution that fails. W22 turned out to be equivalent to the solution.

Gates as run here (all green):
- Number scripts: the runner gives 3 of 3 passed in 3 s. Run directly in strict mode: L1 390/390 (0 uncovered, 11 literals), L2 348/348 (14 literals), L3 231/231 (8 literals). Every literal is a scenario given or a test setting. Each script imports the shipped module from `content/data/ai`, and L1 checks the shipped notes against `make_notes(4)`. I found no fiat values and no dead branches.
- `llm-apps-notes.json` equals `make_notes(seed=4)` in `notes` and `queries`; the file adds one `about` key.
- `grade-all --code --strict-feedback`: 0 failures on all 21 files. 3 to 10 s per file. No `mutant-thin-margin`, `feedback-unreachable` or `feedback-missing`.
- `same-course-reuse.mjs --all`: no error lines for llm-apps.
- Voice: 8,020 sentences scanned, 0 over 35 words, 0 explanations over three sentences, 0 doubled words. No em-dashes, exclamation marks or American spellings in prose. "license" in l7 is the verb, which is correct.

## Modules

- `llm_apps_ops_l1.py`: matches its contract. `fit_tfidf` reproduces scikit-learn's smooth IDF and unit rows, including empty documents (a zero row) and an empty corpus. `embed` gives a zero vector when no word is known. `rank` breaks ties to the lower index with `argsort(kind="stable")`. `make_reports` cuts 180 notes into 30 reports. All 20 queries have exactly 3 relevant notes, so this level's per-query recall equals the pooled recall here (see the l4 warning). Edge cases tried: k larger than the list, a query of unknown words, ties at 0.
- `llm_apps_ops_l2.py`: matches its contract, and I reproduced every seeded figure myself. Cut-off 2021-10-01 is `dates[1499]`. Sharpe 9.2165 before and 0.9960 after. Hit rates 52.8%, 65.6% and 74.6%. The four designs give 6.84, 4.90, 0.27 and 0.475. "Late" means after 16:30 (`m > 990`), which agrees with every `<=` join in the content.
- `llm_apps_ops_l3.py`: matches its contract. The loop scripts (T10, T20, H07) never answer, so a harness must stop them. `search_notes` returns at most k ids with a positive score, and k = 0 gives []. `pct_change(0, b)` raises, and `run_call` catches it. March 2024 has 20 business days and 29 March (Good Friday) has no close, both correct. Checked: CORR 97.87 (8 Mar), 95.98 (28 Mar), 100.39 (19 Mar); DUNM 54.25 to 56.46 (4.07%); HALL 30.10 to 27.43 (−8.87%); ELRY 200.84 (14 Mar); DUNM 55.01 (26 Mar), so T11's 56.38 is wrong by 1.37 as planted.
- app/content/data/ai/llm_apps_ops_l2.py | `make_market` | note | Memory is planted for `t < cutoff_day`, which includes the cut-off day. That doc's score adds `ret[1499]`, the move from the 1 October close to the 4 October close, which happens after the training text ends. The effect is one day in 1,500. | Plant memory for `t < cutoff_day - 1`, or say in the docstring that the cut-off day's next move is treated as known. Changing the module would change every seeded figure, so a docstring line is the cheaper fix.
- app/content/data/ai/llm_apps_ops_l1.py | `load_notes` docstring | note | It says load_notes gives "the same dict" as make_notes, but the shipped file has an extra `about` key. | "...the same notes and queries, plus an `about` line."
- docs/reports/llm-apps-L*-numbers.py | runtime | note | With default threads, L1 takes 9.0 s against 1.9 s single-threaded (BLAS oversubscription on 4 cores). Both runs pass, and the CI runner pins one thread. | None needed. If anyone runs the scripts by hand, tell them to set `OMP_NUM_THREADS=1`.

## Level 1 (Retrieval)

- app/content/courses/llm-apps/l2-the-closest-document.json | screens[8] feedback.byKey.test-7 | error | "Notes 1 and 2 tie for 'rates': the lower index, 0, must come first." They do not tie. For the query 'rates', note 1 scores 0.3722 and note 2 scores 0.3443. The tie is notes 3 and 4, both at 0. The test-7 mutant (reversed tie order) returns [0, 1, 3, 2], so the feedback points the learner at the wrong pair. | "Notes 3 and 4 both score 0 for 'rates': the lower index, 2, must come before 3."
- app/content/courses/llm-apps/l3-search-by-meaning.json | screens[4] option `size3` why | error | "Windows of 3 start at 0, 3, 6: 'the going concern' and 'doubt from auditors' split it again." Windows starting at 0, 3 and 6 are 'sales held up', 'but the going' and 'concern doubt from'. The quoted windows start at 4 and 7. The conclusion (the phrase is split) still holds. | "Windows of 3 start at 0, 3, 6: 'but the going' and 'concern doubt from' split it again."
- app/content/courses/llm-apps/l4-did-we-find-it.json | whole lesson | warning | The brief's Level 1 note asks this level to name `representations` L1's pooled `recall_at_k(E, pairs, k)` in one sentence. No file in the course mentions pooling. A learner coming from `representations` meets a function with the same name and a different meaning, and is never told. On these 20 queries both definitions agree, because every query has 3 relevant notes. | Add one sentence to screens[1] explain or screens[8] prose: "`representations` level 1 pooled the hits over all pairs; here recall is per query, then averaged. They agree only when every query has the same number of relevant notes."
- app/content/courses/llm-apps/l4-did-we-find-it.json | screens[4] to [6], screens[8] | warning | The letter $k$ means two things in one lesson. It is the number of LSA directions ("LSA at $k = 8$", "every $k$ from 4 to 16") and also the recall cut-off (recall@$k$, "Which $k$ matches what the model reads?"). screens[6] option `k-high` mixes them: "Recall at 16 directions". | Call the LSA size $d$ (or "8 directions") in l3's code and l4. Keep $k$ for the cut-off.
- app/content/courses/llm-apps/homework-1.json | items[0] h-retriever tests | warning | The question says "ties to the lower id", but no hidden test has a tie. W05 (ties to the higher id) passes all 11 tests. | Add a planted case with two documents whose best windows are identical, for example two copies of 'dunmore covenant', and expect `[0, 1]`.
- app/content/courses/llm-apps/homework-1.json | items[0] h-retriever tests | warning | "Stop once a window reaches the last word" is not pinned down. W08 keeps adding short tail windows, which changes both the window count and the IDF, and still passes every test, including the recall bar. | Add an exact-list test on a document whose tail window would win if extra tail windows existed. Or expose the window count (for example `len(build_index(['a b ... t'])['rows'])` on a 20-word text, expecting 2).
- app/content/courses/llm-apps/l2-the-closest-document.json | screens[10] explain | note | "the fruit one has fewer other words diluting them". Both headlines have six words. The fruit headline has fewer only after the stop list drops 'by', and the prose never says stop words were dropped. The 0.5309 is the score with stop words removed; with them kept it is 0.4704. | Prose: "...scores headlines, stop words left out, against **apple results**."
- app/content/courses/llm-apps/l2-the-closest-document.json | screens[5] explain | note | "'and', a word with no meaning" is too loose. | "...from 'and', a word that says nothing about the subject".
- app/content/courses/llm-apps/l2-the-closest-document.json | screens[8] vs `llm_apps_ops_l1.rank` | note | Two functions share the name `rank` with different contracts. The lesson's returns [] for a zero query; the module's returns every index. | Note it in the module docstring, or rename the module function `rank_all`.
- app/content/courses/llm-apps/l4-did-we-find-it.json | screens[7] wrong `as-zero` 0.38, `as-one` 0.63 | note | The true slips are 0.375 and 0.625, each exactly on the edge of its ±0.005 band. A learner who rounds 0.625 half-to-even, as Python's `round(0.625, 2)` does to 0.62, or truncates 0.375 to 0.37, gets only the generic line. | Values 0.375 and 0.625 with tol 0.006.
- app/content/courses/llm-apps/l2-the-closest-document.json, l3-search-by-meaning.json | screens[8] `rank`, screens[9] `search` | note | W03 and W04 (unstable `np.argsort`) survive. NumPy sorts arrays of 16 or fewer with a stable insertion sort, and no test has tied scores in a larger array. | Optional: a tie test over the 180 notes. For example, `rank('zzz rates', N)[-3:]` expects the three highest indices in ascending order among the zero scores.

## Level 2 (Language models in quant research)

The level is correct and useful to a quant researcher. It treats a training cut-off as `fin-ml` look-ahead, uses a clean window with a buffer, joins as-of on publication time, fits inside walk-forward folds, deducts costs and haircuts for selection. The seeded market plants each leak at a known size and the prose says so. Every figure reproduces. The findings below are about framing.

- app/content/courses/llm-apps/l8-an-honest-text-backtest.json | screens[0] prose, screens[1] feedback.correct and explain, screens[0] explain | warning | The lesson says $\sqrt{2\ln N}/\sqrt T$ is "what the best of $N$ noise strategies reaches", and that "the best of 55 noise strategies reaches a Sharpe of 2". The expected maximum of $N$ standard normals is 1.63 for $N = 12$ (not 2.23) and 2.29 for $N = 55$ (not 2.83). So over 2 years the noise best averages about 1.15 for 12 tries and 1.62 for 55, not 1.58 and 2. `validation` l12 itself calls the formula a rule of thumb that "runs higher" than the average. As written, this lesson presents an upper-end bound as the expected value. | "...the rule of thumb $\sqrt{2\ln N}/\sqrt T$, a generous allowance for the best of $N$ noise strategies (their best averages a little less)". In screens[1]: "...should allow for a Sharpe near 2 from noise alone."
- app/content/courses/llm-apps/l7-leaks-in-text.json | screens[4] explain, screens[5] explain, summary.ideas[1] | warning | The lesson reads a name effect as memory ("has memorised something about it"; "evidence that names, not words, move these scores"). For a quant this misses two points. (1) A name effect can be prior knowledge about the firm rather than look-ahead. Glasserman and Lin (2023), cited in the brief, found that masked headlines did better out of sample. The test that isolates look-ahead compares the name effect before and after the cut-off. (2) A null result does not clear a model, because dates, figures and product names ('zenvia') still identify the firm. | Add to screens[5] explain: "Compare the effect before and after the cut-off: memory shows as a larger effect before it." In screens[6] or the summary: "Masking names does not hide dates, numbers or product names, so a small effect is not a clean bill."
- app/content/courses/llm-apps/l6-text-as-a-feature.json | screens[1] byKey.r6, screens[9] test-7 | note | A document from 16:29 counts fully for a 16:30 close decision. Real close orders have earlier cut-offs (auction entry deadlines), and pipelines add a latency margin. The rule as taught is internally consistent. | One sentence in screens[8]: "In practice set $\tau_t$ a few minutes before the close, to cover latency and order deadlines."
- app/content/courses/llm-apps/l5-what-the-model-knows.json | screens[4] prose; l12-judging-an-agent.json screens[2] prose | note | Both cite `post-train` level 4, which has a course map but no lesson files yet. The edge is `gate: false` and l5 defines the test itself. | "(`post-train` level 4, when you reach it)".
- app/content/courses/llm-apps/homework-2.json | items[2] h-checklist | note | k3 (timestamps) and k4 (fitting in folds) are independent checks, and their order is forced only by the "feature before fit" story in the explanation. That is defensible, but say so. | Keep the order, and add to feedback.generic: "Build the feature before you check how it is fitted."

## Level 3 (Tools and agents)

The stand-in is mostly honest. l9 screens[0] says there is no model and that the script plants behaviours; the module docstring lists how real models differ. The harness code taught is right: validate, report errors as tool results, cap the loop, score the process. The findings are about places where the script shows a behaviour a real model would not, and about how the course uses Anthropic's terms.

- app/content/courses/llm-apps/l10-reading-a-tool-call.json | screens[7] prose vs question; screens[0] explain | error | The generalise prose says "What you built, in order: parse the JSON, look up the name, validate the arguments, run the tool". Its own question then marks "Look up the name, parse the JSON, validate, run" as the right order, and so do the solution, quiz q10-order, summary.ideas[0] and homework-3 i4. screens[0] explain also puts parsing first. The screen contradicts itself. | screens[7] prose: "...in order: look up the name, parse the JSON, validate the arguments, run the tool." screens[0] explain: "look the name up, parse the JSON, validate the arguments".
- app/content/courses/llm-apps/l11-the-agent-loop.json screens[9]; l12-judging-an-agent.json screens[8], screens[11], summary.ideas[2]; homework-3.json items[1] | error | "The fixed workflow succeeds on 20 of 20; the agent on 16" and "the workflow beat the agent on every count" compare unlike things. `run_workflow` and `fixed_chain` read the task record's `ticker`, `dates` and `query` fields. The agent has to work these out from the question text. For T12 the record's date is already 2024-03-28: the workflow never sees the holiday it is credited with handling, while the agent had to recover from the 29 March error. The agent's 4 failures are planted (loops, a no-tool answer, memory). So 20 against 16 measures the plant, not the design. The lesson's conclusion (prefer a workflow when the steps are known) is right, but this evidence does not support it. | State the asymmetry: "The workflow is handed the parsed task (ticker, dates, query); a real one needs a parsing step, often a model call." Either make the workflow parse T12's question and step back from 29 March itself, or drop "on every count" and present 20/16 as an illustration, not a measurement.
- app/content/courses/llm-apps/l9-tools-as-schemas.json | screens[0] prose and explain; quiz[2] (q9-desc) | warning | "Like a real model, it picks a tool by reading the tools' descriptions." With three tools all described as 'Gets data.', the script takes the first tool listed and calls `search_notes` for a closing price. A real model would also read the names (`get_close`) and the schemas (`ticker`, `date`) and would very likely pick `get_close`. quiz[2]'s correct answer says much the same ("Little more than their names and order"), and the 'schema' option's why says "Schemas show arguments, not purpose", which a {ticker, date} schema contradicts. The demo shows a failure a real model is unlikely to make. | Give the vague demo uninformative names as well (`tool_a`, `tool_b`, `tool_c`). Or use two tools whose names overlap (`get_close` and `get_price_history`, both 'Gets prices.'). Then say: "With nothing to tell them apart, a model guesses."
- app/content/courses/llm-apps/l11-the-agent-loop.json | screens[5] title, prose and byKey.fine; summary.trap; homework-3.json items[2] x2 | warning | The trap is framed as "results under the wrong role" (`user` instead of `tool`). In Anthropic's Messages API, tool results do travel in a `user`-role message, as `tool_result` blocks keyed by `tool_use_id`. Only OpenAI-style APIs use a `tool` role. What actually breaks is the missing pairing with the call, which the explain gets right. The course's own message format has no call id at all. | Title "Results not tied to their call". Prose: "...appends each result as plain text, not as a tool result tied to its call." Summary trap: "results not paired with the call they answer".
- app/content/courses/llm-apps/l11-the-agent-loop.json screens[4]; l12-judging-an-agent.json screens[8]; review-3.json r3-workflow | warning | Anthropic's article defines workflows as "LLMs and tools orchestrated through predefined code paths" and names five patterns (prompt chaining, routing, parallelisation, orchestrator-workers, evaluator-optimiser), with the augmented model as the building block. The brief lists all of these. The course never names the augmented model or any pattern, and its "workflow" makes no model call at all. A learner will take "workflow" to mean "plain code", which is the article's "no agentic system", a different rung. | In l11 screens[4]: "A **workflow** is fixed code that calls the model and tools in a set order (prompt chaining, routing and the like); here even the model call can go, since the steps need no judgement." One line in l12 screens[8] naming the augmented model and two of the patterns.
- app/content/courses/llm-apps/l12-judging-an-agent.json | screens[7] feedback.correct and explain; screens[9] `score_trajectory` | warning | The lesson says scoring "requires the facts (the closes)", but the code checks only that a tool with the required name returned some result. A run that fetches CORR's close on the wrong date and then answers the right value from memory counts as a success. W19 shows a related gap: counting any call by name, errored or not, passes all 7 tests, because test 5's trajectory has no assistant messages. | Either say "requires the tools" (not "the facts"), or check the arguments: the required close must have been fetched for the task's ticker and dates. Give test 5 a real trajectory, with an assistant call followed by its error.
- app/content/courses/llm-apps/l12-judging-an-agent.json | screens[9] tests | warning | W18 (an answer counts as right if it contains the true value) passes all 7 tests. A grader that accepts "97.87 or 98.10" rewards hedged and hallucinated answers, which is exactly the failure this lesson is about. | Add a test: `score_trajectory({'answer': '97.87 or 98.10', 'messages': [...]}, T['T01'])['correct']` expects False.
- app/content/courses/llm-apps/homework-3.json | items[0] h-agent hidden tests | warning | The prose asks the learner to "name the field and the expected type". The scripted model fixes a call only if the error contains the exact words `date` and `string` (or `JSON`, `get_close`, `missing`/`required`). W17 words its message "field 'date': expected str, got int", which names the field and the type, and fails test 4. A learner who names Python types fails the performance task for wording alone. | Prose: "...name the field and the expected JSON-schema type (string, integer, number, boolean)". Or widen `_fixed_by` to accept `str`.
- app/content/courses/llm-apps/l9-tools-as-schemas.json | screens[8] tests | note | W20 (accepts 2.5 where an integer is wanted) passes all 10 tests. A float for an integer field is a common model slip. | Add `validate({'query': 'debt', 'k': 2.5}, SN)` expecting ["field 'k' must be integer, got number"].
- app/content/courses/llm-apps/l9-tools-as-schemas.json | screens[7] prose; summary.formula.note | note | "This is the shape real model APIs use." `input_schema` is Anthropic's field name; OpenAI calls it `parameters`. | "This is the shape Anthropic's API uses; others rename `input_schema`."
- app/content/courses/llm-apps/l10-reading-a-tool-call.json | screens[3] canvas | note | The 'invalid input' bar shows 0 until the learner answers, which reads as the value. | Add a caption: "The second bar is waiting for your answer", as l2 screens[0] does.
- app/content/courses/llm-apps/l10-reading-a-tool-call.json | screens[9] widget.how | note | It says the test uses "the 20 planted tasks with clear errors, 7 of 7 fixed". Test 5 is a hand-made list of 7 fixed and 13 not-failed entries, not a run of the tasks. | "...and a list shaped like the 20 planted tasks' clear-error runs (7 of 7 fixed)."
- app/content/courses/llm-apps/l11-the-agent-loop.json | screens[1] explain | note | "The model plans nothing in advance here: each reply depends on the results so far, which makes it an agent." The scripted model is a fixed chain indexed by turn. | "A real model would choose each reply from the results so far; that choice is what makes this an agent rather than a fixed chain."
- app/content/courses/llm-apps/l12-judging-an-agent.json | screens[3] feedback.correct | note | "worse than a coin toss would suggest by eye" is confusing, since 0.5987 is better than a coin toss. | "$0.95^{10} = 0.5987$: four tasks in ten fail, though each step looks safe."
- app/content/courses/llm-apps/l12-judging-an-agent.json screens[4] feedback.correct; problems-3.json items[0] parts[3] option `no` | note | Both judge the 5-point gap against one rate's standard error (0.0725). Two independent rates on 40 tasks each have a difference standard error of $\sqrt 2 \times 0.0725 = 0.1025$. The conclusion holds, and holds more strongly. | "...the difference has standard error about 0.10, twice the gap."
- app/content/courses/llm-apps/l12-judging-an-agent.json | screens[11] explain | note | "an agent would finish only about 36% of weeks cleanly" rests on an assumed 0.95 a step, stated as if it followed from the scorecard. | "...if each of 20 steps succeeded with chance 0.95, an agent would finish..."

## Appendix: wrong solutions run against the hidden tests

Each source below is run in full by `tools/code-runner.mjs`, the page's harness and worker grader, under the local Pyodide, against the widget's hidden tests. Wrong solutions: 21 tried, 7 survive (W03, W04, W05, W08, W18, W19, W20). W17 is correct in spirit but fails. W22 is equivalent to the solution, so it is not counted: a decayed mean does not depend on the reference time, because the constant factor cancels.

### W01 pooled recall in compare

`l4-did-we-find-it.json` screens[10].widget. Result: FAILS test 1 (`compare(A, B, Q3, 2)[0]`: pooled 0.4, expected 0.5).

```python
import math


def compare(r1, r2, queries, k):
    diffs, ha, hb, tot = [], 0, 0, 0
    for text, relevant in queries:
        rel = set(relevant)
        if not rel:
            continue
        a = len(set(r1(text)[:k]) & rel)
        b = len(set(r2(text)[:k]) & rel)
        ha, hb, tot = ha + a, hb + b, tot + len(rel)
        diffs.append(a / len(rel) - b / len(rel))
    n = len(diffs)
    mean = (ha - hb) / tot          # pooled over all relevant notes
    m = sum(diffs) / n
    sd = math.sqrt(sum((d - m) ** 2 for d in diffs) / (n - 1))
    return mean, sd / math.sqrt(n)
```

### W02 h-retriever rows not scaled to length 1 (dot product)

`homework-1.json` items[0].widget. Result: FAILS test 2 (`query(IP, 'covenant', 1)` gives [0], expected [2]: the long window wins on size).

```python
import math
import re

STOP = ('a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'we', 'what', 'with')


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def build_index(docs):
    chunks, owner = [], []
    for i, d in enumerate(docs):
        w = words(d)
        start = 0
        while w:
            chunks.append([t for t in w[start:start + 12] if t not in STOP])
            owner.append(i)
            if start + 12 >= len(w):
                break
            start += 8
    vocab = sorted({t for c in chunks for t in c})
    col = {t: j for j, t in enumerate(vocab)}
    df = [0] * len(vocab)
    for c in chunks:
        for t in set(c):
            df[col[t]] += 1
    n = len(chunks)
    idf = [math.log((1 + n) / (1 + x)) + 1 for x in df]
    rows = []
    for c in chunks:
        r = {}
        for t in c:
            r[col[t]] = r.get(col[t], 0.0) + idf[col[t]]
        length = math.sqrt(sum(v * v for v in r.values()))
        rows.append(r)
    return {"col": col, "idf": idf, "rows": rows, "owner": owner}


def query(index, text, k):
    q = {}
    for t in words(text):
        if t in index["col"] and t not in STOP:
            j = index["col"][t]
            q[j] = q.get(j, 0.0) + index["idf"][j]
    length = math.sqrt(sum(v * v for v in q.values()))
    if length == 0:
        return []
    best = {}
    for row, doc in zip(index["rows"], index["owner"]):
        s = sum(v * row.get(j, 0.0) for j, v in q.items()) / length
        if s > 0 and s > best.get(doc, 0.0):
            best[doc] = s
    return sorted(best, key=lambda d: (-best[d], d))[:k]
```

### W03 rank ties by np.argsort default (not stable)

`l2-the-closest-document.json` screens[8].widget. Result: SURVIVES all 8 (no tie in an array longer than 16).

```python
import numpy as np
from llm_apps_ops_l1 import fit_tfidf, embed


def cosine(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(a @ b / (na * nb))


def rank(query, docs, stop_words=()):
    model = fit_tfidf(docs, stop_words)
    q = embed(query, model, stop_words)
    if not q.any():
        return []
    scores = np.array([cosine(q, row) for row in model['X']])
    return [int(i) for i in np.argsort(-scores)]
```

### W04 search ties by np.argsort default (not stable)

`l3-search-by-meaning.json` screens[9].widget. Result: SURVIVES all 9.

```python
import numpy as np


def chunk(text, size, overlap):
    words = text.split()
    if not words:
        return []
    out, start = [], 0
    while True:
        out.append(' '.join(words[start:start + size]))
        if start + size >= len(words):
            break
        start += size - overlap
    return out


def search(query_vec, doc_vecs, k):
    q = np.asarray(query_vec, dtype=float)
    D = np.asarray(doc_vecs, dtype=float)
    nq = np.linalg.norm(q)
    if nq == 0:
        return []
    nd = np.linalg.norm(D, axis=1)
    s = np.where(nd > 0, D @ q / (np.where(nd > 0, nd, 1.0) * nq), 0.0)
    return [int(i) for i in np.argsort(-s)][:k]
```

### W05 h-retriever ties to the higher id

`homework-1.json` items[0].widget. Result: SURVIVES all 11 (no tie in any test).

```python
import math
import re

STOP = ('a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'we', 'what', 'with')


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def build_index(docs):
    chunks, owner = [], []
    for i, d in enumerate(docs):
        w = words(d)
        start = 0
        while w:
            chunks.append([t for t in w[start:start + 12] if t not in STOP])
            owner.append(i)
            if start + 12 >= len(w):
                break
            start += 8
    vocab = sorted({t for c in chunks for t in c})
    col = {t: j for j, t in enumerate(vocab)}
    df = [0] * len(vocab)
    for c in chunks:
        for t in set(c):
            df[col[t]] += 1
    n = len(chunks)
    idf = [math.log((1 + n) / (1 + x)) + 1 for x in df]
    rows = []
    for c in chunks:
        r = {}
        for t in c:
            r[col[t]] = r.get(col[t], 0.0) + idf[col[t]]
        length = math.sqrt(sum(v * v for v in r.values()))
        rows.append({j: v / length for j, v in r.items()} if length > 0 else r)
    return {"col": col, "idf": idf, "rows": rows, "owner": owner}


def query(index, text, k):
    q = {}
    for t in words(text):
        if t in index["col"] and t not in STOP:
            j = index["col"][t]
            q[j] = q.get(j, 0.0) + index["idf"][j]
    length = math.sqrt(sum(v * v for v in q.values()))
    if length == 0:
        return []
    best = {}
    for row, doc in zip(index["rows"], index["owner"]):
        s = sum(v * row.get(j, 0.0) for j, v in q.items()) / length
        if s > 0 and s > best.get(doc, 0.0):
            best[doc] = s
    return sorted(best, key=lambda d: (-best[d], -d))[:k]
```

### W06 h-retriever IDF fitted on whole documents, not windows

`homework-1.json` items[0].widget. Result: FAILS test 9 (`query(IX, HQ[5][0], 30)[:6]` gives [2, 18, 1, 8, 29, 25]).

```python
import math
import re

STOP = ('a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'we', 'what', 'with')


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def build_index(docs):
    chunks, owner = [], []
    for i, d in enumerate(docs):
        w = words(d)
        start = 0
        while w:
            chunks.append([t for t in w[start:start + 12] if t not in STOP])
            owner.append(i)
            if start + 12 >= len(w):
                break
            start += 8
    vocab = sorted({t for c in chunks for t in c})
    col = {t: j for j, t in enumerate(vocab)}
    df = [0] * len(vocab)
    for i in range(len(docs)):
        seen = {t for c, o in zip(chunks, owner) if o == i for t in c}
        for t in seen:
            df[col[t]] += 1
    n = len(docs)
    idf = [math.log((1 + n) / (1 + x)) + 1 for x in df]
    rows = []
    for c in chunks:
        r = {}
        for t in c:
            r[col[t]] = r.get(col[t], 0.0) + idf[col[t]]
        length = math.sqrt(sum(v * v for v in r.values()))
        rows.append({j: v / length for j, v in r.items()} if length > 0 else r)
    return {"col": col, "idf": idf, "rows": rows, "owner": owner}


def query(index, text, k):
    q = {}
    for t in words(text):
        if t in index["col"] and t not in STOP:
            j = index["col"][t]
            q[j] = q.get(j, 0.0) + index["idf"][j]
    length = math.sqrt(sum(v * v for v in q.values()))
    if length == 0:
        return []
    best = {}
    for row, doc in zip(index["rows"], index["owner"]):
        s = sum(v * row.get(j, 0.0) for j, v in q.items()) / length
        if s > 0 and s > best.get(doc, 0.0):
            best[doc] = s
    return sorted(best, key=lambda d: (-best[d], d))[:k]
```

### W07 h-retriever drops STOP before cutting windows

`homework-1.json` items[0].widget. Result: FAILS test 6 (`query(IX, HQ[0][0], 3)`).

```python
import math
import re

STOP = ('a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'we', 'what', 'with')


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def build_index(docs):
    chunks, owner = [], []
    for i, d in enumerate(docs):
        w = [t for t in words(d) if t not in STOP]
        start = 0
        while w:
            chunks.append([t for t in w[start:start + 12] if t not in STOP])
            owner.append(i)
            if start + 12 >= len(w):
                break
            start += 8
    vocab = sorted({t for c in chunks for t in c})
    col = {t: j for j, t in enumerate(vocab)}
    df = [0] * len(vocab)
    for c in chunks:
        for t in set(c):
            df[col[t]] += 1
    n = len(chunks)
    idf = [math.log((1 + n) / (1 + x)) + 1 for x in df]
    rows = []
    for c in chunks:
        r = {}
        for t in c:
            r[col[t]] = r.get(col[t], 0.0) + idf[col[t]]
        length = math.sqrt(sum(v * v for v in r.values()))
        rows.append({j: v / length for j, v in r.items()} if length > 0 else r)
    return {"col": col, "idf": idf, "rows": rows, "owner": owner}


def query(index, text, k):
    q = {}
    for t in words(text):
        if t in index["col"] and t not in STOP:
            j = index["col"][t]
            q[j] = q.get(j, 0.0) + index["idf"][j]
    length = math.sqrt(sum(v * v for v in q.values()))
    if length == 0:
        return []
    best = {}
    for row, doc in zip(index["rows"], index["owner"]):
        s = sum(v * row.get(j, 0.0) for j, v in q.items()) / length
        if s > 0 and s > best.get(doc, 0.0):
            best[doc] = s
    return sorted(best, key=lambda d: (-best[d], d))[:k]
```

### W08 h-retriever keeps stepping past the end (extra tail windows)

`homework-1.json` items[0].widget. Result: SURVIVES all 11, the recall bar included.

```python
import math
import re

STOP = ('a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'we', 'what', 'with')


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def build_index(docs):
    chunks, owner = [], []
    for i, d in enumerate(docs):
        w = words(d)
        start = 0
        while w:
            chunks.append([t for t in w[start:start + 12] if t not in STOP])
            owner.append(i)
            start += 8
            if start >= len(w):
                break
    vocab = sorted({t for c in chunks for t in c})
    col = {t: j for j, t in enumerate(vocab)}
    df = [0] * len(vocab)
    for c in chunks:
        for t in set(c):
            df[col[t]] += 1
    n = len(chunks)
    idf = [math.log((1 + n) / (1 + x)) + 1 for x in df]
    rows = []
    for c in chunks:
        r = {}
        for t in c:
            r[col[t]] = r.get(col[t], 0.0) + idf[col[t]]
        length = math.sqrt(sum(v * v for v in r.values()))
        rows.append({j: v / length for j, v in r.items()} if length > 0 else r)
    return {"col": col, "idf": idf, "rows": rows, "owner": owner}


def query(index, text, k):
    q = {}
    for t in words(text):
        if t in index["col"] and t not in STOP:
            j = index["col"][t]
            q[j] = q.get(j, 0.0) + index["idf"][j]
    length = math.sqrt(sum(v * v for v in q.values()))
    if length == 0:
        return []
    best = {}
    for row, doc in zip(index["rows"], index["owner"]):
        s = sum(v * row.get(j, 0.0) for j, v in q.items()) / length
        if s > 0 and s > best.get(doc, 0.0):
            best[doc] = s
    return sorted(best, key=lambda d: (-best[d], d))[:k]
```

### W09 vocabulary and IDF refitted on train plus test docs

`l7-leaks-in-text.json` screens[9].widget. Result: FAILS test 4 (`transform(TE, fit_vocab_in_fold(TR))`: the row width grows).

```python
import math
import re


def fit_vocab_in_fold(train_docs):
    n = len(train_docs)
    df = {}
    for d in train_docs:
        for w in set(re.findall(r'[a-z]+', d.lower())):
            df[w] = df.get(w, 0) + 1
    vocab = sorted(df)
    return {'train': list(train_docs), 'vocab': vocab, 'idf': {w: math.log((1 + n) / (1 + df[w])) + 1 for w in vocab}}


def transform(test_docs, model):
    model = fit_vocab_in_fold(model['train'] + list(test_docs))
    col = {w: j for j, w in enumerate(model['vocab'])}
    rows = []
    for d in test_docs:
        r = [0.0] * len(col)
        for w in re.findall(r'[a-z]+', d.lower()):
            if w in col:
                r[col[w]] += model['idf'][w]
        n = math.sqrt(sum(x * x for x in r))
        rows.append([x / n for x in r] if n > 0 else r)
    return rows
```

### W10 as-of join on the calendar date (date join)

`l6-text-as-a-feature.json` screens[9].widget. Result: FAILS test 3 (gives [-0.3, 0.1], expected [0.8, 0.1]: d5 at 18:05 leaks into Tuesday).

```python
def known_by(docs, t):
    return [d for d in docs if d['published'] <= t]


def asof_feature(docs, days, decision_time):
    out = []
    for day in days:
        k = [d for d in docs if d['published'][:10] <= day]
        out.append(max(k, key=lambda d: d['published'])['score'] if k else None)
    return out
```

### W11 h-text-signal: strict < at the decision time (bisect_left)

`homework-2.json` items[0].widget. Result: FAILS test 6 (seed 0 market: a document at exactly 16:30 moves the Sharpe by more than 0.0005).

```python
import bisect
import datetime as dt
import math


def text_signal_report(panel, docs, cutoff, buffer_days, folds, n_trials, decision_time='16:30'):
    edge = (dt.date.fromisoformat(cutoff) + dt.timedelta(days=buffer_days)).isoformat()
    docs = sorted(docs, key=lambda d: d['published'])
    times = [d['published'] for d in docs]
    days = [(d, r) for d, r in zip(panel['dates'], panel['ret']) if d > edge]
    feat = []
    for d, r in days:
        i = bisect.bisect_left(times, d + ' ' + decision_time)
        feat.append(docs[i - 1]['score'] if i > 0 else None)
    n = len(days)
    b = [round(i * n / folds) for i in range(folds + 1)]
    pnl = []
    for k in range(1, folds):
        past = [f for f in feat[:b[k]] if f is not None]
        mu = sum(past) / len(past)
        for t in range(b[k], b[k + 1]):
            f = feat[t]
            pos = 0 if f is None else (1 if f > mu else -1 if f < mu else 0)
            pnl.append(pos * days[t][1])
    m = sum(pnl) / len(pnl)
    sd = math.sqrt(sum((x - m) ** 2 for x in pnl) / (len(pnl) - 1))
    sharpe = m / sd * math.sqrt(252)
    years = len(pnl) / 252
    return {'sharpe': sharpe, 'haircut': sharpe - math.sqrt(2 * math.log(n_trials)) / math.sqrt(years)}
```

### W12 h-text-signal: threshold from the previous fold only

`homework-2.json` items[0].widget. Result: FAILS test 6 (seed 0 market).

```python
import bisect
import datetime as dt
import math


def text_signal_report(panel, docs, cutoff, buffer_days, folds, n_trials, decision_time='16:30'):
    edge = (dt.date.fromisoformat(cutoff) + dt.timedelta(days=buffer_days)).isoformat()
    docs = sorted(docs, key=lambda d: d['published'])
    times = [d['published'] for d in docs]
    days = [(d, r) for d, r in zip(panel['dates'], panel['ret']) if d > edge]
    feat = []
    for d, r in days:
        i = bisect.bisect_right(times, d + ' ' + decision_time)
        feat.append(docs[i - 1]['score'] if i > 0 else None)
    n = len(days)
    b = [round(i * n / folds) for i in range(folds + 1)]
    pnl = []
    for k in range(1, folds):
        past = [f for f in feat[b[k - 1]:b[k]] if f is not None]
        mu = sum(past) / len(past)
        for t in range(b[k], b[k + 1]):
            f = feat[t]
            pos = 0 if f is None else (1 if f > mu else -1 if f < mu else 0)
            pnl.append(pos * days[t][1])
    m = sum(pnl) / len(pnl)
    sd = math.sqrt(sum((x - m) ** 2 for x in pnl) / (len(pnl) - 1))
    sharpe = m / sd * math.sqrt(252)
    years = len(pnl) / 252
    return {'sharpe': sharpe, 'haircut': sharpe - math.sqrt(2 * math.log(n_trials)) / math.sqrt(years)}
```

### W13 h-text-signal: buffer counted in trading days

`homework-2.json` items[0].widget. Result: FAILS test 7 (seed 3, 60-day buffer: Sharpe 2.26, expected 1.88).

```python
import bisect
import datetime as dt
import math


def text_signal_report(panel, docs, cutoff, buffer_days, folds, n_trials, decision_time='16:30'):
    edge = (dt.date.fromisoformat(cutoff) + dt.timedelta(days=buffer_days)).isoformat()
    docs = sorted(docs, key=lambda d: d['published'])
    times = [d['published'] for d in docs]
    i0 = sum(1 for d in panel['dates'] if d <= cutoff) + buffer_days
    days = list(zip(panel['dates'], panel['ret']))[i0:]
    feat = []
    for d, r in days:
        i = bisect.bisect_right(times, d + ' ' + decision_time)
        feat.append(docs[i - 1]['score'] if i > 0 else None)
    n = len(days)
    b = [round(i * n / folds) for i in range(folds + 1)]
    pnl = []
    for k in range(1, folds):
        past = [f for f in feat[:b[k]] if f is not None]
        mu = sum(past) / len(past)
        for t in range(b[k], b[k + 1]):
            f = feat[t]
            pos = 0 if f is None else (1 if f > mu else -1 if f < mu else 0)
            pnl.append(pos * days[t][1])
    m = sum(pnl) / len(pnl)
    sd = math.sqrt(sum((x - m) ** 2 for x in pnl) / (len(pnl) - 1))
    sharpe = m / sd * math.sqrt(252)
    years = len(pnl) / 252
    return {'sharpe': sharpe, 'haircut': sharpe - math.sqrt(2 * math.log(n_trials)) / math.sqrt(years)}
```

### W14 run_agent with no step cap

`l11-the-agent-loop.json` screens[8].widget. Result: FAILS test 3 (`run_agent(T['T10'], respond, TOOLS, 2)` gives 'repeated', expected 'max_steps').

```python
def run_agent(task, model, tools, max_steps):
    specs = [{'name': n, 'description': t['description'], 'input_schema': t['schema']} for n, t in tools.items()]
    messages = [task_message(task)]
    while True:
        reply = model(messages, specs)
        messages.append({'role': 'assistant', 'content': reply})
        if reply['type'] == 'answer':
            return {'status': 'answer', 'answer': reply['text'], 'messages': messages}
        p = parse_call(reply, tools)
        if p[0] == 'ok':
            r = run_call(p[1], p[2], tools)
            content = {'result': r[1]} if r[0] == 'ok' else {'error': r[1]}
        else:
            content = {'error': p[1]}
        messages.append({'role': 'tool', 'name': reply['name'], 'content': content})
        if repeated_call(messages, 3):
            return {'status': 'repeated', 'answer': None, 'messages': messages}
    return {'status': 'max_steps', 'answer': None, 'messages': messages}


def repeated_call(messages, window):
    calls = [(m['content']['name'], m['content']['arguments']) for m in messages
             if m['role'] == 'assistant' and m['content']['type'] == 'tool_call']
    return len(calls) >= window and len(set(calls[-window:])) == 1
```

### W15 Agent.run with no step cap

`homework-3.json` items[0].widget. Result: FAILS test 9 (cap of 2 on H07 gives 'repeated').

```python
TYPE_NAMES = {str: 'string', bool: 'boolean', int: 'integer', float: 'number', list: 'array', dict: 'object', type(None): 'null'}
def _validate(args, schema):
    if not isinstance(args, dict):
        return ['arguments must be an object']
    errors = []
    props = schema.get('properties', {})
    for name in schema.get('required', []):
        if name not in args:
            errors.append(f"missing required field '{name}'")
    for key, value in args.items():
        if key not in props:
            if schema.get('additionalProperties') is False:
                errors.append(f"unexpected field '{key}'")
            continue
        p = props[key]
        want = p.get('type')
        ok = {'string': isinstance(value, str),
              'integer': isinstance(value, int) and not isinstance(value, bool),
              'number': isinstance(value, (int, float)) and not isinstance(value, bool),
              'boolean': isinstance(value, bool)}.get(want, True)
        if not ok:
            errors.append(f"field '{key}' must be {want}, got {TYPE_NAMES[type(value)]}")
            continue
        if 'enum' in p and value not in p['enum']:
            errors.append(f"field '{key}' must be one of {', '.join(map(str, p['enum']))}")
        if 'minimum' in p and value < p['minimum']:
            errors.append(f"field '{key}' must be at least {p['minimum']}")
        if 'maximum' in p and value > p['maximum']:
            errors.append(f"field '{key}' must be at most {p['maximum']}")
    return errors
import json


class Agent:
    def __init__(self, tools, schemas, max_steps):
        self.tools, self.schemas, self.max_steps = tools, schemas, max_steps

    def _specs(self):
        return [{'name': n, 'description': s['description'], 'input_schema': s['input_schema']} for n, s in self.schemas.items()]

    def _call(self, reply):
        name = reply.get('name')
        if name not in self.tools:
            return {'error': f"unknown tool '{name}'; available: {', '.join(sorted(self.tools))}"}
        try:
            args = json.loads(reply.get('arguments', ''))
        except json.JSONDecodeError as e:
            return {'error': f'arguments are not valid JSON: {e.msg}'}
        errors = _validate(args, self.schemas[name]['input_schema'])
        if errors:
            return {'error': '; '.join(errors)}
        try:
            return {'result': self.tools[name](**args)}
        except Exception as e:
            return {'error': f'{name} failed: {e}'}

    def run(self, task, model):
        messages = [{'role': 'user', 'content': f"[{task['id']}] {task['question']}"}]
        status, answer, calls = 'max_steps', None, []
        while True:
            reply = model(messages, self._specs())
            messages.append({'role': 'assistant', 'content': reply})
            if reply['type'] == 'answer':
                status, answer = 'answer', reply['text']
                break
            messages.append({'role': 'tool', 'name': reply['name'], 'content': self._call(reply)})
            calls.append((reply['name'], reply['arguments']))
            if len(calls) >= 3 and len(set(calls[-3:])) == 1:
                status = 'repeated'
                break
        used = {m['name'] for m in messages if m['role'] == 'tool' and 'result' in m['content']}
        correct = answer is not None and answer.strip() == task['answer']
        required = all(r in used for r in task['required'])
        score = {'correct': correct, 'used_required': required,
                 'invalid_calls': sum(1 for m in messages if m['role'] == 'tool' and 'error' in m['content']),
                 'steps': sum(1 for m in messages if m['role'] == 'assistant'), 'success': correct and required}
        return {'status': status, 'answer': answer, 'messages': messages, 'score': score}
```

### W16 Agent runs tool calls without validating arguments

`homework-3.json` items[0].widget. Result: FAILS test 4 (H04, integer date: the tool's own error lacks 'string', so the script never fixes it).

```python
TYPE_NAMES = {str: 'string', bool: 'boolean', int: 'integer', float: 'number', list: 'array', dict: 'object', type(None): 'null'}
def _validate(args, schema):
    if not isinstance(args, dict):
        return ['arguments must be an object']
    errors = []
    props = schema.get('properties', {})
    for name in schema.get('required', []):
        if name not in args:
            errors.append(f"missing required field '{name}'")
    for key, value in args.items():
        if key not in props:
            if schema.get('additionalProperties') is False:
                errors.append(f"unexpected field '{key}'")
            continue
        p = props[key]
        want = p.get('type')
        ok = {'string': isinstance(value, str),
              'integer': isinstance(value, int) and not isinstance(value, bool),
              'number': isinstance(value, (int, float)) and not isinstance(value, bool),
              'boolean': isinstance(value, bool)}.get(want, True)
        if not ok:
            errors.append(f"field '{key}' must be {want}, got {TYPE_NAMES[type(value)]}")
            continue
        if 'enum' in p and value not in p['enum']:
            errors.append(f"field '{key}' must be one of {', '.join(map(str, p['enum']))}")
        if 'minimum' in p and value < p['minimum']:
            errors.append(f"field '{key}' must be at least {p['minimum']}")
        if 'maximum' in p and value > p['maximum']:
            errors.append(f"field '{key}' must be at most {p['maximum']}")
    return errors
import json


class Agent:
    def __init__(self, tools, schemas, max_steps):
        self.tools, self.schemas, self.max_steps = tools, schemas, max_steps

    def _specs(self):
        return [{'name': n, 'description': s['description'], 'input_schema': s['input_schema']} for n, s in self.schemas.items()]

    def _call(self, reply):
        name = reply.get('name')
        if name not in self.tools:
            return {'error': f"unknown tool '{name}'; available: {', '.join(sorted(self.tools))}"}
        try:
            args = json.loads(reply.get('arguments', ''))
        except json.JSONDecodeError as e:
            return {'error': f'arguments are not valid JSON: {e.msg}'}
        try:
            return {'result': self.tools[name](**args)}
        except Exception as e:
            return {'error': f'{name} failed: {e}'}

    def run(self, task, model):
        messages = [{'role': 'user', 'content': f"[{task['id']}] {task['question']}"}]
        status, answer, calls = 'max_steps', None, []
        for _ in range(self.max_steps):
            reply = model(messages, self._specs())
            messages.append({'role': 'assistant', 'content': reply})
            if reply['type'] == 'answer':
                status, answer = 'answer', reply['text']
                break
            messages.append({'role': 'tool', 'name': reply['name'], 'content': self._call(reply)})
            calls.append((reply['name'], reply['arguments']))
            if len(calls) >= 3 and len(set(calls[-3:])) == 1:
                status = 'repeated'
                break
        used = {m['name'] for m in messages if m['role'] == 'tool' and 'result' in m['content']}
        correct = answer is not None and answer.strip() == task['answer']
        required = all(r in used for r in task['required'])
        score = {'correct': correct, 'used_required': required,
                 'invalid_calls': sum(1 for m in messages if m['role'] == 'tool' and 'error' in m['content']),
                 'steps': sum(1 for m in messages if m['role'] == 'assistant'), 'success': correct and required}
        return {'status': status, 'answer': answer, 'messages': messages, 'score': score}
```

### W17 Agent error says "expected str" (Python type name)

`homework-3.json` items[0].widget. Result: FAILS test 4 (H04): a clear message in Python type names is not accepted by the scripted model.

```python
TYPE_NAMES = {str: 'string', bool: 'boolean', int: 'integer', float: 'number', list: 'array', dict: 'object', type(None): 'null'}
def _validate(args, schema):
    if not isinstance(args, dict):
        return ['arguments must be an object']
    errors = []
    props = schema.get('properties', {})
    for name in schema.get('required', []):
        if name not in args:
            errors.append(f"missing required field '{name}'")
    for key, value in args.items():
        if key not in props:
            if schema.get('additionalProperties') is False:
                errors.append(f"unexpected field '{key}'")
            continue
        p = props[key]
        want = p.get('type')
        ok = {'string': isinstance(value, str),
              'integer': isinstance(value, int) and not isinstance(value, bool),
              'number': isinstance(value, (int, float)) and not isinstance(value, bool),
              'boolean': isinstance(value, bool)}.get(want, True)
        if not ok:
            errors.append(f"field '{key}': expected {dict(string='str', integer='int', number='float', boolean='bool')[want]}, got {type(value).__name__}")
            continue
        if 'enum' in p and value not in p['enum']:
            errors.append(f"field '{key}' must be one of {', '.join(map(str, p['enum']))}")
        if 'minimum' in p and value < p['minimum']:
            errors.append(f"field '{key}' must be at least {p['minimum']}")
        if 'maximum' in p and value > p['maximum']:
            errors.append(f"field '{key}' must be at most {p['maximum']}")
    return errors
import json


class Agent:
    def __init__(self, tools, schemas, max_steps):
        self.tools, self.schemas, self.max_steps = tools, schemas, max_steps

    def _specs(self):
        return [{'name': n, 'description': s['description'], 'input_schema': s['input_schema']} for n, s in self.schemas.items()]

    def _call(self, reply):
        name = reply.get('name')
        if name not in self.tools:
            return {'error': f"unknown tool '{name}'; available: {', '.join(sorted(self.tools))}"}
        try:
            args = json.loads(reply.get('arguments', ''))
        except json.JSONDecodeError as e:
            return {'error': f'arguments are not valid JSON: {e.msg}'}
        errors = _validate(args, self.schemas[name]['input_schema'])
        if errors:
            return {'error': '; '.join(errors)}
        try:
            return {'result': self.tools[name](**args)}
        except Exception as e:
            return {'error': f'{name} failed: {e}'}

    def run(self, task, model):
        messages = [{'role': 'user', 'content': f"[{task['id']}] {task['question']}"}]
        status, answer, calls = 'max_steps', None, []
        for _ in range(self.max_steps):
            reply = model(messages, self._specs())
            messages.append({'role': 'assistant', 'content': reply})
            if reply['type'] == 'answer':
                status, answer = 'answer', reply['text']
                break
            messages.append({'role': 'tool', 'name': reply['name'], 'content': self._call(reply)})
            calls.append((reply['name'], reply['arguments']))
            if len(calls) >= 3 and len(set(calls[-3:])) == 1:
                status = 'repeated'
                break
        used = {m['name'] for m in messages if m['role'] == 'tool' and 'result' in m['content']}
        correct = answer is not None and answer.strip() == task['answer']
        required = all(r in used for r in task['required'])
        score = {'correct': correct, 'used_required': required,
                 'invalid_calls': sum(1 for m in messages if m['role'] == 'tool' and 'error' in m['content']),
                 'steps': sum(1 for m in messages if m['role'] == 'assistant'), 'success': correct and required}
        return {'status': status, 'answer': answer, 'messages': messages, 'score': score}
```

### W18 score_trajectory: right if the answer contains the true value

`l12-judging-an-agent.json` screens[9].widget. Result: SURVIVES all 7.

```python
import math


def score_trajectory(traj, task):
    used = {m['name'] for m in traj['messages'] if m['role'] == 'tool' and 'result' in m['content']}
    correct = traj['answer'] is not None and task['answer'] in traj['answer']
    required = all(r in used for r in task['required'])
    return {'correct': correct, 'used_required': required,
            'invalid_calls': sum(1 for m in traj['messages'] if m['role'] == 'tool' and 'error' in m['content']),
            'steps': sum(1 for m in traj['messages'] if m['role'] == 'assistant'),
            'success': correct and required}
```

### W19 score_trajectory: a required tool counts if it was called at all

`l12-judging-an-agent.json` screens[9].widget. Result: SURVIVES all 7 (test 5 has no assistant messages, so nothing is counted).

```python
import math


def score_trajectory(traj, task):
    used = {m['content']['name'] for m in traj['messages'] if m['role'] == 'assistant' and m['content'].get('type') == 'tool_call'}
    correct = traj['answer'] is not None and traj['answer'].strip() == task['answer']
    required = all(r in used for r in task['required'])
    return {'correct': correct, 'used_required': required,
            'invalid_calls': sum(1 for m in traj['messages'] if m['role'] == 'tool' and 'error' in m['content']),
            'steps': sum(1 for m in traj['messages'] if m['role'] == 'assistant'),
            'success': correct and required}
```

### W20 validate accepts 2.5 for an integer field

`l9-tools-as-schemas.json` screens[8].widget. Result: SURVIVES all 10.

```python
def validate(args, schema):
    if not isinstance(args, dict):
        return ['arguments must be an object']
    errors = []
    props = schema.get('properties', {})
    for name in schema.get('required', []):
        if name not in args:
            errors.append(f"missing required field '{name}'")
    for key, value in args.items():
        if key not in props:
            if schema.get('additionalProperties') is False:
                errors.append(f"unexpected field '{key}'")
            continue
        p = props[key]
        want = p.get('type')
        ok = {'string': isinstance(value, str),
              'integer': isinstance(value, (int, float)) and not isinstance(value, bool),
              'number': isinstance(value, (int, float)) and not isinstance(value, bool),
              'boolean': isinstance(value, bool)}.get(want, True)
        if not ok:
            errors.append(f"field '{key}' must be {want}, got {TYPE_NAMES[type(value)]}")
            continue
        if 'enum' in p and value not in p['enum']:
            errors.append(f"field '{key}' must be one of {', '.join(map(str, p['enum']))}")
        if 'minimum' in p and value < p['minimum']:
            errors.append(f"field '{key}' must be at least {p['minimum']}")
        if 'maximum' in p and value > p['maximum']:
            errors.append(f"field '{key}' must be at most {p['maximum']}")
    return errors
```

### W21 compare_agents with the n (population) standard deviation

`l12-judging-an-agent.json` screens[10].widget. Result: FAILS test 4 (`compare_agents` 2-task case: 0.3536, expected 0.5).

```python
import math


def success_rate(scores):
    n = len(scores)
    p = sum(1 for s in scores if s['success']) / n
    return p, math.sqrt(p * (1 - p) / n)


def compare_agents(a, b):
    d = [int(x['success']) - int(y['success']) for x, y in zip(a, b)]
    n = len(d)
    m = sum(d) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in d) / n)
    return m, sd / math.sqrt(n)
```

### W22 decayed_score ages measured to midnight, not the decision time

`l6-text-as-a-feature.json` screens[10].widget. Result: passes all 7: EQUIVALENT, not counted (the reference time cancels in a decayed mean).

```python
import datetime as dt


def decayed_score(docs, day, half_life, decision_time='16:30'):
    t = dt.datetime.fromisoformat(day + ' ' + decision_time)
    t0 = dt.datetime.fromisoformat(day + ' 00:00')
    num = den = 0.0
    for d in docs:
        p = dt.datetime.fromisoformat(d['published'])
        if p > t:
            continue
        w = 0.5 ** ((t0 - p).total_seconds() / 86400 / half_life)
        num += w * d['score']
        den += w
    return num / den if den > 0 else None
```

### W23 name_masking_test masks with str.replace in three letter cases

`homework-2.json` items[1].widget. Result: FAILS test 5 (`Corranby` is masked inside the longer word).

```python
import math
import re
import statistics


def name_masking_test(texts, names, score):
    def mask(t):
        for n in sorted(names, key=len, reverse=True):
            for v in (n, n.lower(), n.upper()):
                t = t.replace(v, 'NAME')
        return t
    d = [score(t) - score(mask(t)) for t in texts]
    m = statistics.fmean(d)
    se = statistics.stdev(d) / math.sqrt(len(d))
    return m, se, (m / se if se > 0 else 0.0)
```
