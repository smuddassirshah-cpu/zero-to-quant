# llm-apps level 1: Retrieval (report)

Branch `ai-w7-llm-apps`, from `56dd6746`. Brief: `docs/briefs/llm-apps.md` Level 1, including the note on per-query recall (`representations` L1's `recall_at_k(E, pairs, k)` is pooled; this level's `recall_at_k(ranked, relevant, k)` is per query, and l4 screen 2 and the code screens use it per query and average over queries).

## Files

| File | Screens / items | Code widgets (tests, mutants) |
|---|---|---|
| `l1-words-as-weights.json` | 11 screens, quiz 4 | `tokenise` + `idf` (8, 4); `tfidf_matrix` (7, 3) |
| `l2-the-closest-document.json` | 11 screens, quiz 4 | `cosine` + `rank` (8, 5); `top_k` (6, 3) |
| `l3-search-by-meaning.json` | 11 screens, quiz 4 | `lsa_embed` (6, 3); `chunk` + `search` (9, 4) |
| `l4-did-we-find-it.json` | 12 screens, quiz 4 | `recall_at_k` + `mrr` (7, 5); `compare` (6, 3) |
| `review-1.json` | 10 items, pass 0.8 | none |
| `homework-1.json` | 6 items: performance code task `h-retriever` (11, 5), code `h-mrr-gap` (6, 3), order with two distractors, longform (10-point rubric), numeric, choice | 2 |
| `problems-1.json` | 3 chained problems, 13 parts (difficulty 5, 4, 3) | none |
| `app/content/data/ai/llm_apps_ops_l1.py` | shared module v1.0 (signatures below) | |
| `app/content/data/ai/llm-apps-notes.json` | 180 invented notes, 20 labelled queries, 23,090 bytes | |

Performance task: `docs/reports/llm-apps-1-perf.md`.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors (no `[source-ban]`, no `[ai-mutants]` for these files).
2. `VOICE_BASE=app/content/courses/llm-apps python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 lesson ids in code spans.
3. `docs/reports/llm-apps-L1-numbers.py` through `node tools/run-number-scripts.mjs --python <venv> --only llm-apps-L1`: passed (strict, 390 of 390 checks, 0 uncovered, 11 literals each with a reason).
4. Playthrough with `--local-cdn <pkgs>`, desktop and `--mobile`: l1 to l4 all ok (quiz 4/4 each), `review-1` 10 of 10, `homework-1` 6 of 6 with the performance starter failing and the longform marked by the button, `problems-1` 3 problems, 13 parts. All passed.
Also: `grade-all.mjs --code --strict-feedback` on all seven files, 0 failures (10 Python widgets: solution passes, starter fails, every mutant fails its named test, every `byKey` test line reached); `same-course-reuse.mjs --all` lists nothing for `llm-apps`; `perf-reports.mjs` reports no gap.

## Numbers and their sources

Every figure is recomputed in the number script by a route other than the builder's NumPy: pure-Python TF-IDF and cosines; scikit-learn `TfidfVectorizer(token_pattern='[a-z]+')` for IDF and rows; LSA from an eigen-decomposition of $X^\top X$ (not an SVD) with the same sign rule; recall, MRR and standard errors by loops and `statistics`.

- Planner's worked example, confirmed: IDF 1.5108 ('inflation', 'rates'), 1.9163 ('and', 'oil'); query cosines 0.3919, 0.1812, 0, 0.5256; without 'and', 'as', 'on' 0.5672, 0.2706, 0, 0.3096; cosine of $(0.6, 0.8, 0)$ and $(0.8, 0, 0.6)$ 0.48. Note 1's length 4.0589, its 'inflation' weight 0.3722 (scikit-learn's figure). Note 4's 'and' term 0.3242 (from printed weights; 0.3241 unrounded, inside the slip band), 'inflation' term 0.2015.
- Filings transfer: $\ln(201/5)+1 = 4.6939$, $\ln(201/197)+1 = 1.0201$, ratio 4.60.
- l3: two-topic corpus of eight notes, LSA $k = 2$: Q $(0.320, -0.287)$, note 3 $(0.467, -0.353)$, cosine 0.9965 against a TF-IDF cosine of 0; 16-word passage gives 4 chunks at size 6, overlap 2; plain-count cosines 0.7071 (chunk) and 0.4082 (passage). Corran funding query on the 180 notes: TF-IDF top 3 holds 1 of 3, LSA $k = 8$ holds 3 of 3.
- l4: 'halloran margins profit' relevant at ranks 1, 2, 5; precision at 3 0.6667; MRR of ranks 1, 3, 2 is 0.6111; recall at 3 over the 20 queries 0.6333 (TF-IDF) and 0.8333 (LSA $k = 8$), mean difference 0.20, sd 0.2513, standard error 0.0562 (3.6 standard errors). LSA $k = 13$ gives 1.0 on these queries and also on 20 fresh ones (said so in the trap's explanation: only fresh queries can show it).
- Homework: model recall at 3 on the 24 hidden questions 0.5556, whole reports 0.4514, bar 0.5; smallest score gap at an exact-list cut is checked above $10^{-6}$.
- Problem set: IDF 1.4055, weight 0.3393 (length 4.1428), cosine 0.4798, recall at 2 of 0.5; 4 windows, cosines 0.5477 and 0.3162; MRR 0.675, mean 0.1667, sd 0.3496, standard error 0.1427.

## Data and seeds (provenance)

- `llm-apps-notes.json`: **invented** research notes, written by `llm_apps_ops_l1.make_notes(seed=4)` (Python `random.Random`); 8 invented company names (ashcombe, brackley, corran, dunmore, ellery, fairholt, garside, halloran), 6 topics of six near-synonyms each, 3 notes per company and topic, 36 market notes, 20 labelled queries. No real firm, report or person. Proposed credit row for `app/content/data/ai/README.md` (the main session owns it): "`llm-apps-notes.json` | 180 invented research notes and 20 labelled queries for llm-apps L1 | 23 KB | Written by this course | 'Notes invented for this course.'"
- Reports for the homework: `make_reports(notes, seed=11)`, 30 reports of 6 notes. Hidden questions: `random.Random(99)`, 24 company-topic pairs. Fresh queries in the number script: `random.Random(21)`.
- The four- and eight-note corpora, the filings, apple headlines, the five commodity headlines and the 30-word prospectus are written for the lessons (invented).
- Every hidden test is far under a third of its limit: TF-IDF on 180 notes and an SVD of a 180 by 68 matrix are milliseconds; the homework builds 30 reports' windows in pure Python (desktop playthrough 13.5 s for the whole homework page, Python load included). No scikit-learn import in the browser: tests compare with scikit-learn's values computed ahead of time, and the prose says so.

## Shared module `llm_apps_ops_l1.py` (v1.0; frozen once merged)

A hyphen cannot be imported in Python, so the file is `llm_apps_ops_l1.py` (the `nt_ops_*` and `seq_ops_*` pattern), not `llm-apps_ops_l1.py`.

- `make_notes(seed=4) -> {"notes": [{"id", "company", "topic", "text"}], "queries": [{"text", "relevant"}]}`
- `load_notes(path="llm-apps-notes.json") -> same dict`
- `make_reports(notes, seed=11, per=6) -> [{"ids", "text"}]`
- `tokenise(text) -> list[str]` (lower-case runs of a to z)
- `fit_tfidf(docs, stop_words=()) -> {"vocab", "index", "idf", "X"}` (scikit-learn defaults; rows of length 1)
- `embed(text, model, stop_words=()) -> np.ndarray` (length 1, zeros if no known word)
- Constants `COMPANIES`, `TOPICS`, `STOP_WORDS`, `FILL`.

## course.json

No change proposed.

## Backlog

Three bullets under "Raised later (llm-apps level 1)" in `docs/BACKLOG-INBOX.md`.
