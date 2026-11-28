# gpt level 1 (Tokenisation): second-reader findings

Scope: `app/content/courses/gpt/` l1-text-as-bytes, l2-merging-pairs, l3-encode-and-decode, l4-cleaning-the-corpus, review-1, homework-1, problems-1, at e3bbbb98. Context read: `docs/briefs/gpt.md` Level 1, `docs/reports/gpt-L1.md`, `docs/AUTHORING.md` (section 9 `mutants` rule), `docs/briefs/ai-strand-curriculum.md` 2.9, `info` level 2 (l5 to l8, review-2, problems-2).
Method, no browser: ran `docs/reports/gpt-L1-numbers.py` with the venv (251 of 251, exit 0), then again with `GPT_FULL_TEXT` set to the 1,115,394-character Tiny Shakespeare (md5 6fb458f1232090904fb40fe944165e91, found in the session scratchpad: 253 of 253); wrote an independent recompute (`scratchpad/rgpt1/recompute.py`: BPE on byte strings with explicit first-position ties, its own encoder, line dedup on slice and full text with a strict per-occurrence speaker-tag test, shingles, every bits-per-byte figure) and an add-one bigram on the slice (2.45538 validation, 2.42367 training); `grade-all.mjs --file <each> --code --local-cdn <pkgs>` on all seven files (0 failures; 12 Python widgets); 67 reviewer wrong solutions injected as `mutants` into scratchpad copies and graded the same way (appendix); every numeric `answer`, `tol` and `wrong[]` listed and checked against the rounding asked; distractor values re-derived from their `why`; `voice-scan.py 35 --summary` (0 over 35 words, 0 explanations over three sentences); grep for em-dashes, exclamation marks and American spellings (none in prose).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching issue or a test gap that lets a taught bug pass; note = style, script or minor wording.

Counts: 2 errors, 8 warnings, 14 notes.

Numbers: every figure on screen was recomputed and agrees: UTF-8 lengths and bytes, the toy merges and row lengths (23, 19, 15, 12, 10; after merge 3 the pair ` bid` + `d` is still at 2), Shakespeare token counts at 0 to 200 merges, first eight merges, held-out 13,809 tokens (1.8104) and 5,000-character 1.4434, `strawberry` and `there whether` ids, the order log (63 bytes to 35 tokens; merges ` B`, `00`, `00\n`, `NE`, `NEW`, ` BU`, ` BUY`, ` 1`), every bits-per-byte conversion, slice and full-text dedup counts, the five-bar charts, 6,913 speaker-tag repeats (same count under a strict per-occurrence test), 65 distinct characters, all Jaccard values (83/93, 58/68, the distributor table 0.91, 0.83, 0.801, 0.22, 0.19, 0.18), the bond and Lefèvre problems. Tolerances: every key typed at the asked rounding lands inside its band (27.3% against 0.2726 ± 0.0005, 98.0% against 0.9797 ± 0.0005, 2.7603 from the carried 2.1429 inside 2.7604 ± 0.0002); no `wrong[]` band reaches its answer. Conversions match `info` L2: one bit is $\ln 2$ nats, bits are nats over $\ln 2$, and per-letter against per-word losses do not compare (info l7), which is the per-token against per-byte point here.

Script verdict: it recomputes rather than restates. Each kind of figure is computed two independent ways (two trainers with different tie mechanics, two encoders, set against sorted-merge Jaccard), and 30 `expect` calls tie keys to the JSON. Gaps are in the notes below: without `GPT_FULL_TEXT` the author's own full-text figures (6,913, 143, the bars 193, 163, 162, 158, 1,115,394, 65 characters) are not checked at all in CI, and about a dozen on-screen keys are computed in `claim` calls with no `expect` tying them to the file. I closed both by hand: all agree.

## Lessons

- app/content/courses/gpt/l1-text-as-bytes.json | screens[7] feedback.byKey.lloyds | error | "You checked the name with the most characters." `Lloyds plc` has 10, the same as `naïve café`; `Société Générale` has 16. The line states a false reason. | "Lloyds plc fills the field exactly: plain letters are one byte each, so 10 characters are 10 bytes."
- app/content/courses/gpt/l4-cleaning-the-corpus.json | screens[3] explain | error | "Only 143 repeated lines are speech, such as `Farewell.`": 26 of the 143 are the heading `3 KING HENRY VI` (a play title repeated before scenes), which is structure, not speech. The rest are short speech (`My lord?` 6, `him.` 5, `No.` 5 ...). | "Most of the other 143 are short speech such as `My lord?`; 26 are the heading `3 KING HENRY VI`."
- app/content/courses/gpt/l3-encode-and-decode.json | screens[6] question, canvas row, explain | warning | The worked example breaks the lesson's own rule ("both on the same text", screens[7], summary). 2.0121 bytes per token is the tokeniser's figure on its 20,000-character training text, while the bigram's 2.4554 is its loss on the held-out 25,000 characters, where this tokeniser gives 1.8104 (screens[4]). The comparison "per byte it beats the bigram" is drawn across two texts. The conclusion survives (4.20 / (1.8104 ln 2) = 3.3470 < 3.5424) but the method is the one the trap warns against. | Score the token model on the held-out text: "4.20 nats per token on the held-out 25,000 characters, where its tokeniser gives 1.8104 bytes per token" (key 3.3470; wrongs 2.3199 no-ln2, 6.0593 per-token, 10.970 times). The brief's worked example with 2.0121 can stay in the generalise prose as a plain conversion, without a comparison.
- app/content/courses/gpt/l1-text-as-bytes.json | screens[5] widget tests | warning | Test 11 bans only the text `.encode`. `return len(bytes(s, 'utf-8'))` and `len(bytearray(s, 'utf-8'))` pass all 11 tests, so the task "work from `ord` and the table; do not call `.encode`" is not enforced (appendix, l1 s5 items 1 and 2). | Test 11: `all(w not in __learner_source__ for w in ('encode', 'bytes(', 'bytearray'))`, with the byKey line naming all three.
- app/content/courses/gpt/l2-merging-pairs.json | screens[5] prose; l1, l2, l3 as a whole | warning | The level never says how production byte-level BPE differs from ours. GPT-2 first splits text with a regex into words, numbers, punctuation and spaces, so no token crosses those boundaries and a space joins the start of the next word (` the`), never the end of the last. Here the first Shakespeare merges are `e `, `t `, `s ` and the log merges `00\n` and `NEW BUY`, and screens[5] calls them "word endings". Special tokens (`<|endoftext|>` between documents) are also absent. The topic's sources (Karpathy's tokeniser lecture, CS336) make both central. | One generalise sentence in l2 screens[5] or l3 screens[7]: "Production tokenisers such as GPT-2's first split text with a regex into words, numbers and punctuation, so a merge never crosses a word, and the space goes at the front: ` the`. They also add special tokens such as `<|endoftext|>` that no text can produce." Optionally a quiz item on why `e ` never appears in GPT-2's vocabulary.
- app/content/courses/gpt/l4-cleaning-the-corpus.json | screens[11] canvas row B and C, hints[0]; screens[7] prose | warning | Screen 7 states the filter rule as "Jaccard similarity above 0.8"; screen 11 shows B and C as `0.80` and expects it flagged, with the hint switching to "0.8 or more". A learner applying screen 7's rule to the 0.80 on screen leaves r2 untapped and gets only the generic line. | Show `0.801`, or replace the note so B and C score clearly above 0.8; and say "0.8 or more" in screen 7 (problems-1 items[2] parts[2] mixes "at least" and "above" too).
- app/content/courses/gpt/l4-cleaning-the-corpus.json | screens[8] prose | warning | "Comparing every pair of a billion documents is too slow. Real pipelines use MinHash, which estimates $J$ from short signatures" implies MinHash removes the all-pairs comparison. MinHash only makes each comparison cheap; avoiding all pairs needs locality-sensitive hashing on the signatures (banding). | "Real pipelines use MinHash, which estimates $J$ from short signatures, and bucket those signatures so only likely pairs are compared."

## Review, homework and problems

- app/content/courses/gpt/homework-1.json | items[0] widget tests | warning | The prose requires `decode` with `errors='replace'`, but no test decodes a cut-off character: a `decode` with plain `.decode('utf-8')` passes all 11 tests (appendix, hw items[0] item 1). l3's test 8 checks this; the performance task does not. | Add a test: `t = BPETokenizer(); t.train('bid bids', 2)`, call `t.decode([226, 130])`, expect `'�'`; mention a cut-off character in `how`.
- app/content/courses/gpt/homework-1.json | items[0] widget tests | warning | Counting without overlaps (skipping a position after a pair of equal ids) passes all 11 tests: `aaaaaaaa` is an even run, so both counting rules pick the same merges, and the Shakespeare case checks only the count, a round trip, the ratio and `there whether` (appendix, hw items[0] item 2). l2's `train_bpe` catches it with `£££` (test 5); the homework, whose prose states "Count overlapping pairs", does not. | Add a test on an odd run: `t.train('aaaaaa', 5)` (counts 5 then (256,256) twice overlapping, once without), expect `[[97, 97], [256, 256]]`, or reuse `£££`.
- app/content/courses/gpt/problems-1.json | items[0] parts[1] wrong `no-space` (6) | warning | No slip gives 6. The why ("Merge 259 needs a space before `bond`; the first word has none, so it stays `bond`") describes a learner who also gives the first `bond` a space, which leaves the count at 7. | Drop the entry, or key a real slip: 9 for stopping after merge 258 ("You stopped before merges 259 and 260"), or 11 for stopping after merge 257.

## Notes

- app/content/courses/gpt/l3-encode-and-decode.json | screens[5] prose | note | "`th` is the most frequent pair in it": in `the there`, `th` and `he` both occur twice. | "`th` and `he` are its most frequent pairs, twice each."
- app/content/courses/gpt/l1-text-as-bytes.json | quiz[2] feedback.correct | note | "Twice the bytes": spaces, digits and punctuation stay one byte in Greek text, so the Greek report is under twice the bytes. | "More bytes, and fewer learned groups, mean more tokens for the same meaning."
- app/content/courses/gpt/l1-text-as-bytes.json | screens[1] explain | note | "2 for most accented letters, 3 for most other scripts" sits oddly with quiz[2], where Greek letters take 2: Greek, Cyrillic, Hebrew and Arabic are all 2 bytes. | "1 for plain English, 2 for accented Latin, Greek, Cyrillic, Hebrew and Arabic, 3 for Chinese, Japanese and most other scripts, 4 for emoji."
- app/content/courses/gpt/l1-text-as-bytes.json | screens[3] explain | note | "The second byte happens to equal 163, because 163 is below 192" leaves out the other half of the reason (163 is at least 128, so its bits already read `10xxxxxx`). | "...because 163 lies between 128 and 191, so its bits already have the form `10xxxxxx`."
- app/content/courses/gpt/l2-merging-pairs.json | screens[5] prose | note | "The first merges join a letter and the space after it": 5 of the 8 shown (`th`, `ou` and `, ` are not). | "Most of the first merges join a letter and the space after it." (see the regex warning above).
- app/content/courses/gpt/l2-merging-pairs.json | quiz[0] prose | note | The listed byte-pair counts of `see sea seen` omit `a` then space (1), so the list reads as complete but is not. | Add "`a` then space 1".
- app/content/courses/gpt/l2-merging-pairs.json | screens[8] test 7 | note | The key-order test `[3, 1, 2, 3, 1, 2, 9]` gives first-seen order equal to count order, so a `pair_counts` that returns keys sorted by count (`dict(Counter(...).most_common())`) also passes. Harmless for the tie rule (a stable sort keeps first-seen order among ties), but the test does not check what its byKey line says. | Use `[5, 6, 1, 2, 1, 2]`: first-seen `[5, 6], [6, 1], [1, 2], [2, 1]`, count order puts `[1, 2]` first.
- app/content/courses/gpt/l3-encode-and-decode.json | quiz[3] option `cannot` why | note | "Both figures are on the same text" is not in the prose, which says only "validation loss". | Prose: "On the same validation text, the loss rises ...".
- app/content/courses/gpt/problems-1.json | items[2] parts[3] wrong `over-train` (0.0037) | note | 36 / 9,850 (the deduplicated corpus); a learner who divides by the 12,400 named in the prose gets 0.29% and the generic line. | Add `over-raw` 0.0029 with "You divided by the training corpus. The share asked is of the 400 test transcripts."
- app/content/courses/gpt/homework-1.json | items[1] widget tests | note | Shingles kept as lists (repeats counted) and lower-cased texts both pass all 8 tests: no test text repeats a 5-character run or differs only in case (appendix, hw items[1] items 5 and 6). | Add a case with a repeated run, e.g. `['abcdeabcde', 'abcdeabcdf']` (sets give 5/6 = 0.8333, the list version 1.0), at threshold 0.9, and a pair that differs only in case.
- docs/reports/gpt-L1-numbers.py | full-text block | note | Without `GPT_FULL_TEXT` (the CI case) the author's own full-text figures are unchecked: 6,913 and 143 enter only as literals in `FULL`, and the bars 193, 163, 162, 158, the 1,115,394 characters and the "65 distinct characters" of l4 screens[4] are not in the default path (65 is not in the script at all). I recomputed all with the full text: they agree. | Record a digest of the full text and the derived counts in the script and say so in the report; add `len(set(full)) == 65`.
- docs/reports/gpt-L1-numbers.py | claims without `expect` | note | About a dozen keys are computed in `claim` calls against literals with no `expect` tying them to the JSON: problems items[0] parts[2] (2.1429), items[1] parts[0] to [3] (15, 11, 12, 15), items[2] parts[0], [1], [3] (2550, 0.88, 0.09); review items[2], [4], [8] (4, 3, 0.5); l2 screens[6] bars; l4 screens[11] table; homework items[0] explain (1.44). The bigram's 2.4554 is used, not recomputed (I get 2.45538). All agree with the file. | Add `lv.expect` for each; recompute the bigram in the script (a 15-line counter).
- docs/reports/gpt-L1.md | file name | note | The brief and CLAUDE.md name the report `docs/reports/gpt-1.md`; it was written as `gpt-L1.md`. | Rename, or record the convention in the report.
- app/content/courses/gpt/l4-cleaning-the-corpus.json, problems-1.json | thresholds | note | "above" and "at least" are used for the same filter rule across l4 screens[7], screens[11] hints and problems items[2] parts[2]. | One wording, "at least", everywhere (the homework uses it).

## Appendix: reviewer wrong solutions

Each source was injected as a `mutants` entry (`test: 1`) into a scratchpad copy of its file and graded with `node tools/grade-all.mjs --file <copy> --code --local-cdn <pkgs>`; the result is the first hidden test it fails, or SURVIVES. 67 sources: 52 fail a test, 9 survive because they are correct alternatives (marked), 6 survive as real bugs (l1 screens[5] items 1 and 2; homework items[0] items 1 and 2; homework items[1] items 5 and 6), all raised above.

### l1-text-as-bytes.json screens[5] `utf8_length`

1. bytes() instead of .encode: **SURVIVES**

```python
def utf8_length(s):
    return len(bytes(s, 'utf-8'))
```

2. bytearray instead of .encode: **SURVIVES**

```python
def utf8_length(s):
    return len(bytearray(s, 'utf-8'))
```

3. 3-byte row ends one early (< 0xFFFF): **test 9**

```python
def utf8_length(s):
    total = 0
    for ch in s:
        cp = ord(ch)
        if cp < 0x80:
            total += 1
        elif cp < 0x800:
            total += 2
        elif cp < 0xFFFF:
            total += 3
        else:
            total += 4
    return total
```

4. one extra byte for any non-ASCII: **test 3**

```python
def utf8_length(s):
    return len(s) + sum(1 for ch in s if ord(ch) >= 0x80)
```

5. rows by 8 bits (256, 65536): **test 2**

```python
def utf8_length(s):
    total = 0
    for ch in s:
        cp = ord(ch)
        total += 1 if cp < 0x100 else 2 if cp < 0x10000 else 4
    return total
```

### l1-text-as-bytes.json screens[6] `char_spans`

1. position moves by 1 per character: **test 1**

```python
def char_spans(s):
    spans, pos = [], 0
    for ch in s:
        n = len(ch.encode('utf-8'))
        spans.append((pos, pos + n))
        pos += 1
    return spans
```

2. spans start at 1: **test 1**

```python
def char_spans(s):
    spans, pos = [], 1
    for ch in s:
        n = len(ch.encode('utf-8'))
        spans.append((pos, pos + n))
        pos += n
    return spans
```

3. start bytes found by scanning, last span dropped: **test 1**

```python
def char_spans(s):
    b = s.encode('utf-8')
    starts = [i for i, x in enumerate(b) if x & 0xC0 != 0x80]
    return list(zip(starts, starts[1:]))
```

4. continuation test inverted to 0x40 mask: **SURVIVES (a correct alternative; my label was wrong)**

```python
def char_spans(s):
    b = s.encode('utf-8')
    starts = [i for i, x in enumerate(b) if x & 0x40 or x < 0x80]
    return list(zip(starts, starts[1:] + [len(b)]))
```

### l1-text-as-bytes.json screens[10] `safe_truncate`

1. decode without error handling: **test 1**

```python
def safe_truncate(s, n_bytes):
    return s.encode('utf-8')[:n_bytes].decode('utf-8')
```

2. errors=ignore (correct alternative): **SURVIVES (correct; the explain names it)**

```python
def safe_truncate(s, n_bytes):
    return s.encode('utf-8')[:n_bytes].decode('utf-8', errors='ignore')
```

3. drops one byte on a decode error, once: **test 7**

```python
def safe_truncate(s, n_bytes):
    b = s.encode('utf-8')[:n_bytes]
    try:
        return b.decode('utf-8')
    except UnicodeDecodeError:
        return b[:-1].decode('utf-8')
```

4. skips a character that does not fit and carries on: **test 1**

```python
def safe_truncate(s, n_bytes):
    out, used = [], 0
    for ch in s:
        k = len(ch.encode('utf-8'))
        if used + k > n_bytes:
            continue
        out.append(ch)
        used += k
    return ''.join(out)
```

5. counts only 1 or 2 bytes per character: **test 7**

```python
def safe_truncate(s, n_bytes):
    out, used = [], 0
    for ch in s:
        k = 1 if ord(ch) < 0x80 else 2
        if used + k > n_bytes:
            break
        out.append(ch)
        used += k
    return ''.join(out)
```

### l2-merging-pairs.json screens[8] `pair_counts`

1. str.count, which does not count overlaps: **test 2**

```python
def pair_counts(ids):
    s = ''.join(map(chr, ids))
    counts = {}
    for a, b in zip(ids, ids[1:]):
        counts[(a, b)] = s.count(chr(a) + chr(b))
    return counts
```

2. pairs only at even positions: **test 1**

```python
def pair_counts(ids):
    counts = {}
    for pair in zip(ids[::2], ids[1::2]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts
```

3. misses the last pair: **test 1**

```python
def pair_counts(ids):
    counts = {}
    for i in range(len(ids) - 2):
        p = (ids[i], ids[i + 1])
        counts[p] = counts.get(p, 0) + 1
    return counts
```

4. Counter (correct alternative): **SURVIVES (correct)**

```python
from collections import Counter


def pair_counts(ids):
    return Counter(zip(ids, ids[1:]))
```

5. keys ordered by count, most common first: **SURVIVES (equivalent: a stable sort by count keeps first-seen order among ties, so the tie rule still holds)**

```python
from collections import Counter


def pair_counts(ids):
    return dict(Counter(zip(ids, ids[1:])).most_common())
```

### l2-merging-pairs.json screens[9] `merge`

1. moves on by 1 after a match: **test 1**

```python
def merge(ids, pair, new_id):
    out, i = [], 0
    while i < len(ids):
        if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            out.append(new_id)
        else:
            out.append(ids[i])
        i += 1
    return out
```

2. replaces every overlapping position, dropping the second id: **test 2**

```python
def merge(ids, pair, new_id):
    out, skip = [], False
    for i in range(len(ids)):
        if i + 1 < len(ids) and (ids[i], ids[i + 1]) == pair:
            out.append(new_id)
            skip = True
        elif skip:
            skip = False
        else:
            out.append(ids[i])
    return out
```

3. repeated find-first-and-splice (quadratic): **SURVIVES (correct; quadratic but inside the limit on 60,000 ids)**

```python
def merge(ids, pair, new_id):
    ids = list(ids)
    i = 0
    while i + 1 < len(ids):
        if ids[i] == pair[0] and ids[i + 1] == pair[1]:
            ids = ids[:i] + [new_id] + ids[i + 2:]
        i += 1
    return ids
```

4. list.index loop that restarts from 0 each time: **test 10 (time limit)**

```python
def merge(ids, pair, new_id):
    ids = list(ids)
    while True:
        for i in range(len(ids) - 1):
            if ids[i] == pair[0] and ids[i + 1] == pair[1]:
                ids[i:i + 2] = [new_id]
                break
        else:
            return ids
```

### l2-merging-pairs.json screens[10] `train_bpe` (prelude defines `pair_counts` and `merge`)

1. tie goes to the last pair seen: **test 1**

```python
def train_bpe(text, n_merges):
    ids = list(text.encode('utf-8'))
    merges = []
    for k in range(n_merges):
        counts = pair_counts(ids)
        if not counts:
            break
        best = max(counts.values())
        pair = [p for p in counts if counts[p] == best][-1]
        if counts[pair] < 2:
            break
        ids = merge(ids, pair, 256 + k)
        merges.append(pair)
    return merges
```

2. counts without overlaps (skips a position after a counted pair of equal ids): **test 5**

```python
def train_bpe(text, n_merges):
    ids = list(text.encode('utf-8'))
    merges = []
    for k in range(n_merges):
        counts, i = {}, 0
        while i + 1 < len(ids):
            p = (ids[i], ids[i + 1])
            counts[p] = counts.get(p, 0) + 1
            i += 2 if ids[i] == ids[i + 1] else 1
        if not counts:
            break
        pair = max(counts, key=counts.get)
        if counts[pair] < 2:
            break
        ids = merge(ids, pair, 256 + k)
        merges.append(pair)
    return merges
```

3. new ids start at 257: **test 1**

```python
def train_bpe(text, n_merges):
    ids = list(text.encode('utf-8'))
    merges = []
    for k in range(n_merges):
        counts = pair_counts(ids)
        if not counts:
            break
        pair = max(counts, key=counts.get)
        if counts[pair] < 2:
            break
        ids = merge(ids, pair, 257 + k)
        merges.append(pair)
    return merges
```

4. stops when the top count is 2 or less: **test 1**

```python
def train_bpe(text, n_merges):
    ids = list(text.encode('utf-8'))
    merges = []
    for k in range(n_merges):
        counts = pair_counts(ids)
        if not counts:
            break
        pair = max(counts, key=counts.get)
        if counts[pair] <= 2:
            break
        ids = merge(ids, pair, 256 + k)
        merges.append(pair)
    return merges
```

5. no empty-counts guard: **test 6**

```python
def train_bpe(text, n_merges):
    ids = list(text.encode('utf-8'))
    merges = []
    for k in range(n_merges):
        counts = pair_counts(ids)
        pair = max(counts, key=counts.get)
        if counts[pair] < 2:
            break
        ids = merge(ids, pair, 256 + k)
        merges.append(pair)
    return merges
```

6. trains on characters, not bytes: **test 5**

```python
def train_bpe(text, n_merges):
    ids = [ord(c) for c in text]
    merges = []
    for k in range(n_merges):
        counts = pair_counts(ids)
        if not counts:
            break
        pair = max(counts, key=counts.get)
        if counts[pair] < 2:
            break
        ids = merge(ids, pair, 256 + k)
        merges.append(pair)
    return merges
```

7. ties by smallest pair (sorted keys): **test 3**

```python
def train_bpe(text, n_merges):
    ids = list(text.encode('utf-8'))
    merges = []
    for k in range(n_merges):
        counts = pair_counts(ids)
        if not counts:
            break
        pair = max(sorted(counts), key=counts.get)
        if counts[pair] < 2:
            break
        ids = merge(ids, pair, 256 + k)
        merges.append(pair)
    return merges
```

### l3-encode-and-decode.json screens[8] `encode` / `decode` (prelude defines `merge`)

1. decode with errors=ignore: **test 8**

```python
def encode(text, merges):
    ids = list(text.encode('utf-8'))
    for k, pair in enumerate(merges):
        ids = merge(ids, pair, 256 + k)
    return ids


def decode(ids, merges):
    vocab = {i: bytes([i]) for i in range(256)}
    for k, (a, b) in enumerate(merges):
        vocab[256 + k] = vocab[a] + vocab[b]
    return b''.join(vocab[i] for i in ids).decode('utf-8', errors='ignore')
```

2. decodes each token on its own: **test 7**

```python
def encode(text, merges):
    ids = list(text.encode('utf-8'))
    for k, pair in enumerate(merges):
        ids = merge(ids, pair, 256 + k)
    return ids


def decode(ids, merges):
    vocab = {i: bytes([i]) for i in range(256)}
    for k, (a, b) in enumerate(merges):
        vocab[256 + k] = vocab[a] + vocab[b]
    return ''.join(vocab[i].decode('utf-8', errors='replace') for i in ids)
```

3. vocab ids off by one (257 + k): **test 2**

```python
def encode(text, merges):
    ids = list(text.encode('utf-8'))
    for k, pair in enumerate(merges):
        ids = merge(ids, pair, 256 + k)
    return ids


def decode(ids, merges):
    vocab = {i: bytes([i]) for i in range(256)}
    for k, (a, b) in enumerate(merges):
        vocab[257 + k] = vocab[a] + vocab.get(b, b'')
    return b''.join(vocab.get(i, b'') for i in ids).decode('utf-8', errors='replace')
```

4. decodes latin-1, not UTF-8: **test 7**

```python
def encode(text, merges):
    ids = list(text.encode('utf-8'))
    for k, pair in enumerate(merges):
        ids = merge(ids, pair, 256 + k)
    return ids


def decode(ids, merges):
    vocab = {i: bytes([i]) for i in range(256)}
    for k, (a, b) in enumerate(merges):
        vocab[256 + k] = vocab[a] + vocab[b]
    return b''.join(vocab[i] for i in ids).decode('latin-1')
```

5. encode by lowest rank first (correct alternative): **SURVIVES (correct)**

```python
def encode(text, merges):
    ids = list(text.encode('utf-8'))
    rank = {p: k for k, p in enumerate(merges)}
    while True:
        ks = [rank[p] for p in zip(ids, ids[1:]) if p in rank]
        if not ks:
            return ids
        k = min(ks)
        ids = merge(ids, merges[k], 256 + k)


def decode(ids, merges):
    vocab = {i: bytes([i]) for i in range(256)}
    for k, (a, b) in enumerate(merges):
        vocab[256 + k] = vocab[a] + vocab[b]
    return b''.join(vocab[i] for i in ids).decode('utf-8', errors='replace')
```

6. encode replays merges in reverse order: **test 1**

```python
def encode(text, merges):
    ids = list(text.encode('utf-8'))
    for k in reversed(range(len(merges))):
        ids = merge(ids, merges[k], 256 + k)
    return ids


def decode(ids, merges):
    vocab = {i: bytes([i]) for i in range(256)}
    for k, (a, b) in enumerate(merges):
        vocab[256 + k] = vocab[a] + vocab[b]
    return b''.join(vocab[i] for i in ids).decode('utf-8', errors='replace')
```

7. encode from characters (ord), not bytes: **test 4**

```python
def encode(text, merges):
    ids = [ord(c) for c in text]
    for k, pair in enumerate(merges):
        ids = merge(ids, pair, 256 + k)
    return ids


def decode(ids, merges):
    vocab = {i: bytes([i]) for i in range(256)}
    for k, (a, b) in enumerate(merges):
        vocab[256 + k] = vocab[a] + vocab[b]
    return b''.join(vocab[i] for i in ids).decode('utf-8', errors='replace')
```

### l3-encode-and-decode.json screens[9] `bits_per_byte`

1. ln 2 rounded to 0.693: **test 1**

```python
def bits_per_byte(loss_nats_per_token, bytes_per_token):
    return loss_nats_per_token / (bytes_per_token * 0.693)
```

2. multiplies by ln 2: **test 1**

```python
import math


def bits_per_byte(loss_nats_per_token, bytes_per_token):
    return loss_nats_per_token / bytes_per_token * math.log(2)
```

3. divides by log2(e) wrongly (log base 10): **test 1**

```python
import math


def bits_per_byte(loss_nats_per_token, bytes_per_token):
    return loss_nats_per_token / (bytes_per_token * math.log10(2))
```

4. forgets the bytes per token: **test 2**

```python
import math


def bits_per_byte(loss_nats_per_token, bytes_per_token):
    return loss_nats_per_token / math.log(2)
```

5. times log2(e) (correct alternative): **SURVIVES (correct)**

```python
import math


def bits_per_byte(loss_nats_per_token, bytes_per_token):
    return loss_nats_per_token / bytes_per_token * math.log2(math.e)
```

### l4-cleaning-the-corpus.json screens[9] `dedup_lines`

1. strips each line: **test 6**

```python
def dedup_lines(text):
    seen, kept, removed = set(), [], 0
    for line in text.split('\n'):
        line = line.strip()
        if line == '':
            continue
        if line in seen:
            removed += 1
        else:
            seen.add(line)
            kept.append(line)
    return kept, removed
```

2. kept lines in sorted order: **test 1**

```python
def dedup_lines(text):
    lines = [l for l in text.split('\n') if l != '']
    kept = sorted(set(lines))
    return kept, len(lines) - len(kept)
```

3. removed counts blank lines too: **test 1**

```python
def dedup_lines(text):
    seen, kept = set(), []
    lines = text.split('\n')
    for line in lines:
        if line != '' and line not in seen:
            seen.add(line)
            kept.append(line)
    return kept, len(lines) - len(kept)
```

4. splitlines (correct alternative): **SURVIVES (correct)**

```python
def dedup_lines(text):
    seen, kept, removed = set(), [], 0
    for line in text.splitlines():
        if not line:
            continue
        if line in seen:
            removed += 1
        else:
            seen.add(line)
            kept.append(line)
    return kept, removed
```

5. keeps the last copy, not the first: **test 1**

```python
def dedup_lines(text):
    lines = [l for l in text.split('\n') if l != '']
    last = {l: i for i, l in enumerate(lines)}
    kept = [l for i, l in enumerate(lines) if last[l] == i]
    return kept, len(lines) - len(kept)
```

6. drops only adjacent repeats: **test 1**

```python
def dedup_lines(text):
    kept, removed, prev = [], 0, None
    for line in text.split('\n'):
        if line == '':
            continue
        if line == prev:
            removed += 1
        else:
            kept.append(line)
        prev = line
    return kept, removed
```

### l4-cleaning-the-corpus.json screens[10] `shingles` / `jaccard`

1. one start too many, keeps a short tail: **test 1**

```python
def shingles(text, n):
    return {text[i:i + n] for i in range(len(text) - n + 2)}


def jaccard(a, b):
    return len(a & b) / len(a | b)
```

2. short text gives itself as one shingle: **test 3**

```python
def shingles(text, n):
    return {text[i:i + n] for i in range(max(1, len(text) - n + 1))}


def jaccard(a, b):
    return len(a & b) / len(a | b)
```

3. jaccard over the smaller set: **test 6**

```python
def shingles(text, n):
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def jaccard(a, b):
    return len(a & b) / min(len(a), len(b))
```

4. integer division: **test 6**

```python
def shingles(text, n):
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def jaccard(a, b):
    return len(a & b) // len(a | b)
```

5. word shingles instead of characters: **test 1**

```python
def shingles(text, n):
    w = text.split()
    return {' '.join(w[i:i + n]) for i in range(len(w) - n + 1)}


def jaccard(a, b):
    return len(a & b) / len(a | b)
```

6. non-overlapping shingles (step n): **test 1**

```python
def shingles(text, n):
    return {text[i:i + n] for i in range(0, len(text) - n + 1, n)}


def jaccard(a, b):
    return len(a & b) / len(a | b)
```

### homework-1.json items[0] `BPETokenizer` (performance task)

1. decode without errors=replace: **SURVIVES**

```python
class BPETokenizer:
    def __init__(self):
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}

    @staticmethod
    def _merge(ids, pair, new_id):
        out, i = [], 0
        while i < len(ids):
            if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
                out.append(new_id)
                i += 2
            else:
                out.append(ids[i])
                i += 1
        return out

    def train(self, text, n_merges):
        ids = list(text.encode('utf-8'))
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}
        for k in range(n_merges):
            counts = {}
            for pair in zip(ids, ids[1:]):
                counts[pair] = counts.get(pair, 0) + 1
            if not counts:
                break
            pair = max(counts, key=counts.get)
            if counts[pair] < 2:
                break
            new_id = 256 + k
            ids = self._merge(ids, pair, new_id)
            self.merges.append(pair)
            self.vocab[new_id] = self.vocab[pair[0]] + self.vocab[pair[1]]

    def encode(self, text):
        ids = list(text.encode('utf-8'))
        for k, pair in enumerate(self.merges):
            ids = self._merge(ids, pair, 256 + k)
        return ids

    def decode(self, ids):
        return b''.join(self.vocab[i] for i in ids).decode('utf-8')
```

2. counts without overlaps: **SURVIVES**

```python
class BPETokenizer:
    def __init__(self):
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}

    @staticmethod
    def _merge(ids, pair, new_id):
        out, i = [], 0
        while i < len(ids):
            if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
                out.append(new_id)
                i += 2
            else:
                out.append(ids[i])
                i += 1
        return out

    def train(self, text, n_merges):
        ids = list(text.encode('utf-8'))
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}
        for k in range(n_merges):
            counts, i = {}, 0
            while i + 1 < len(ids):
                p = (ids[i], ids[i + 1])
                counts[p] = counts.get(p, 0) + 1
                i += 2 if ids[i] == ids[i + 1] else 1
            if not counts:
                break
            pair = max(counts, key=counts.get)
            if counts[pair] < 2:
                break
            new_id = 256 + k
            ids = self._merge(ids, pair, new_id)
            self.merges.append(pair)
            self.vocab[new_id] = self.vocab[pair[0]] + self.vocab[pair[1]]

    def encode(self, text):
        ids = list(text.encode('utf-8'))
        for k, pair in enumerate(self.merges):
            ids = self._merge(ids, pair, 256 + k)
        return ids

    def decode(self, ids):
        return b''.join(self.vocab[i] for i in ids).decode('utf-8', errors='replace')
```

3. tie goes to the last pair seen: **test 1**

```python
class BPETokenizer:
    def __init__(self):
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}

    @staticmethod
    def _merge(ids, pair, new_id):
        out, i = [], 0
        while i < len(ids):
            if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
                out.append(new_id)
                i += 2
            else:
                out.append(ids[i])
                i += 1
        return out

    def train(self, text, n_merges):
        ids = list(text.encode('utf-8'))
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}
        for k in range(n_merges):
            counts = {}
            for pair in zip(ids, ids[1:]):
                counts[pair] = counts.get(pair, 0) + 1
            if not counts:
                break
            pair = max(reversed(list(counts)), key=counts.get)
            if counts[pair] < 2:
                break
            new_id = 256 + k
            ids = self._merge(ids, pair, new_id)
            self.merges.append(pair)
            self.vocab[new_id] = self.vocab[pair[0]] + self.vocab[pair[1]]

    def encode(self, text):
        ids = list(text.encode('utf-8'))
        for k, pair in enumerate(self.merges):
            ids = self._merge(ids, pair, 256 + k)
        return ids

    def decode(self, ids):
        return b''.join(self.vocab[i] for i in ids).decode('utf-8', errors='replace')
```

4. decodes each token on its own: **test 7**

```python
class BPETokenizer:
    def __init__(self):
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}

    @staticmethod
    def _merge(ids, pair, new_id):
        out, i = [], 0
        while i < len(ids):
            if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
                out.append(new_id)
                i += 2
            else:
                out.append(ids[i])
                i += 1
        return out

    def train(self, text, n_merges):
        ids = list(text.encode('utf-8'))
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}
        for k in range(n_merges):
            counts = {}
            for pair in zip(ids, ids[1:]):
                counts[pair] = counts.get(pair, 0) + 1
            if not counts:
                break
            pair = max(counts, key=counts.get)
            if counts[pair] < 2:
                break
            new_id = 256 + k
            ids = self._merge(ids, pair, new_id)
            self.merges.append(pair)
            self.vocab[new_id] = self.vocab[pair[0]] + self.vocab[pair[1]]

    def encode(self, text):
        ids = list(text.encode('utf-8'))
        for k, pair in enumerate(self.merges):
            ids = self._merge(ids, pair, 256 + k)
        return ids

    def decode(self, ids):
        return ''.join(self.vocab[i].decode('utf-8', errors='replace') for i in ids)
```

5. encode ids off by one (257 + k): **test 2**

```python
class BPETokenizer:
    def __init__(self):
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}

    @staticmethod
    def _merge(ids, pair, new_id):
        out, i = [], 0
        while i < len(ids):
            if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
                out.append(new_id)
                i += 2
            else:
                out.append(ids[i])
                i += 1
        return out

    def train(self, text, n_merges):
        ids = list(text.encode('utf-8'))
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}
        for k in range(n_merges):
            counts = {}
            for pair in zip(ids, ids[1:]):
                counts[pair] = counts.get(pair, 0) + 1
            if not counts:
                break
            pair = max(counts, key=counts.get)
            if counts[pair] < 2:
                break
            new_id = 256 + k
            ids = self._merge(ids, pair, new_id)
            self.merges.append(pair)
            self.vocab[new_id] = self.vocab[pair[0]] + self.vocab[pair[1]]

    def encode(self, text):
        ids = list(text.encode('utf-8'))
        for k, pair in enumerate(self.merges):
            ids = self._merge(ids, pair, 257 + k)
        return ids

    def decode(self, ids):
        return b''.join(self.vocab[i] for i in ids).decode('utf-8', errors='replace')
```

6. encode skips the last merge: **test 5**

```python
class BPETokenizer:
    def __init__(self):
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}

    @staticmethod
    def _merge(ids, pair, new_id):
        out, i = [], 0
        while i < len(ids):
            if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
                out.append(new_id)
                i += 2
            else:
                out.append(ids[i])
                i += 1
        return out

    def train(self, text, n_merges):
        ids = list(text.encode('utf-8'))
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}
        for k in range(n_merges):
            counts = {}
            for pair in zip(ids, ids[1:]):
                counts[pair] = counts.get(pair, 0) + 1
            if not counts:
                break
            pair = max(counts, key=counts.get)
            if counts[pair] < 2:
                break
            new_id = 256 + k
            ids = self._merge(ids, pair, new_id)
            self.merges.append(pair)
            self.vocab[new_id] = self.vocab[pair[0]] + self.vocab[pair[1]]

    def encode(self, text):
        ids = list(text.encode('utf-8'))
        for k, pair in enumerate(self.merges[:-1]):
            ids = self._merge(ids, pair, 256 + k)
        return ids

    def decode(self, ids):
        return b''.join(self.vocab[i] for i in ids).decode('utf-8', errors='replace')
```

7. second train keeps the old vocab (harmless): **SURVIVES (harmless: every merged id is rewritten)**

```python
class BPETokenizer:
    def __init__(self):
        self.merges = []
        self.vocab = {i: bytes([i]) for i in range(256)}

    @staticmethod
    def _merge(ids, pair, new_id):
        out, i = [], 0
        while i < len(ids):
            if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
                out.append(new_id)
                i += 2
            else:
                out.append(ids[i])
                i += 1
        return out

    def train(self, text, n_merges):
        ids = list(text.encode('utf-8'))
        self.merges = []
        for k in range(n_merges):
            counts = {}
            for pair in zip(ids, ids[1:]):
                counts[pair] = counts.get(pair, 0) + 1
            if not counts:
                break
            pair = max(counts, key=counts.get)
            if counts[pair] < 2:
                break
            new_id = 256 + k
            ids = self._merge(ids, pair, new_id)
            self.merges.append(pair)
            self.vocab[new_id] = self.vocab[pair[0]] + self.vocab[pair[1]]

    def encode(self, text):
        ids = list(text.encode('utf-8'))
        for k, pair in enumerate(self.merges):
            ids = self._merge(ids, pair, 256 + k)
        return ids

    def decode(self, ids):
        return b''.join(self.vocab[i] for i in ids).decode('utf-8', errors='replace')
```

### homework-1.json items[1] `near_duplicates`

1. misses the last shingle: **test 7**

```python
def near_duplicates(docs, threshold):
    sets = [{d[i:i + 5] for i in range(len(d) - 5)} for d in docs]
    pairs = []
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            a, b = sets[i], sets[j]
            if a and b and len(a & b) / len(a | b) >= threshold:
                pairs.append([i, j])
    return pairs
```

2. jaccard over the smaller set: **test 2**

```python
def near_duplicates(docs, threshold):
    sets = [{d[i:i + 5] for i in range(len(d) - 4)} for d in docs]
    pairs = []
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            a, b = sets[i], sets[j]
            if a and b and len(a & b) / min(len(a), len(b)) >= threshold:
                pairs.append([i, j])
    return pairs
```

3. compares every ordered pair: **test 1**

```python
def near_duplicates(docs, threshold):
    sets = [{d[i:i + 5] for i in range(len(d) - 4)} for d in docs]
    pairs = []
    for i in range(len(docs)):
        for j in range(len(docs)):
            a, b = sets[i], sets[j]
            if i != j and a and b and len(a & b) / len(a | b) >= threshold:
                pairs.append([i, j])
    return pairs
```

4. 4-character shingles: **test 2**

```python
def near_duplicates(docs, threshold):
    sets = [{d[i:i + 4] for i in range(len(d) - 3)} for d in docs]
    pairs = []
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            a, b = sets[i], sets[j]
            if a and b and len(a & b) / len(a | b) >= threshold:
                pairs.append([i, j])
    return pairs
```

5. lists, so repeats count (multiset): **SURVIVES**

```python
def near_duplicates(docs, threshold):
    out = []
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            a = [docs[i][k:k + 5] for k in range(len(docs[i]) - 4)]
            b = [docs[j][k:k + 5] for k in range(len(docs[j]) - 4)]
            if a and b:
                shared = sum(1 for x in a if x in b)
                if shared / (len(a) + len(b) - shared) >= threshold:
                    out.append([i, j])
    return out
```

6. words lower-cased first: **SURVIVES**

```python
def near_duplicates(docs, threshold):
    sets = [{d.lower()[i:i + 5] for i in range(len(d) - 4)} for d in docs]
    pairs = []
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            a, b = sets[i], sets[j]
            if a and b and len(a & b) / len(a | b) >= threshold:
                pairs.append([i, j])
    return pairs
```

## Fix pass

Recomputed before writing: 4.20 / (1.8104 ln 2) = 3.34695 (3.3470 from the shown 1.8104, 3.3469 from the exact 25000 / 13809, so the key's tolerance is 0.0002); no-ln2 4.20 / 1.8104 = 2.3199; per token 4.20 / ln 2 = 6.0593; times 4.20 x 1.8104 / ln 2 = 10.970; bigram add-one 2.45538 validation and 2.42367 training (script now recomputes both); 26 of the 143 non-tag repeats are `3 KING HENRY VI`, 6 are `My lord?` (script, full text). Number script: 275 of 275 default, 279 of 279 with `GPT_FULL_TEXT`.

1. l1 screens[7] byKey.lloyds (error): fixed. Lloyds plc and naïve café both have 10 characters, Société Générale has 16 (19 bytes); the line now says Lloyds plc fills the field exactly.
2. l4 screens[3] explain (error): fixed. "Most of the other 143 are short speech such as `My lord?`; 26 are the heading `3 KING HENRY VI`."
3. l3 screens[6] and screens[9] (warning): fixed. The token model is scored on the held-out text at 1.8104 bytes per token: key 3.3470 (was 3.0114, graded answer changed), wrongs 2.3199, 6.0593, 10.970; canvas rows of screens[6] and [9], hints, feedback, explain and the hidden test `bits_per_byte(4.2, 1.8104)` (3.346950493) updated. Numbers script updated.
4. l1 screens[5] test 11 (warning): fixed. It bans `encode`, `bytes(` and `bytearray`; prose, `how` and byKey say so. Two mutants added (`bytes(s, 'utf-8')`, `bytearray(s, 'utf-8')`, both failing test 11).
5. GPT-2 regex and special tokens (warning): fixed in l2 screens[5] explain (no new screen); prose now says "Most of the first merges".
6. l4 0.8 versus 0.80 (warning): fixed. The table shows 0.801 (checked: 0.801 to three places), and "at least 0.8" is used in l4 screens[7] (prose, hint), screens[11] and problems items[2] parts[2].
7. l4 screens[8] MinHash (warning): fixed with the suggested wording (signatures bucketed so only likely pairs are compared).
8. homework items[0] decode without `errors='replace'` (warning): fixed. Test 12 decodes `[226, 130]` after `train('bid bids', 2)`; the prose-matching mutant fails test 12.
9. homework items[0] pair counting without overlaps (warning): fixed. Test 13 trains on `aaaaaa` (merges `[[97, 97], [256, 256]]`); mutant fails test 13.
10. problems items[0] parts[1] `no-space` 6 (warning): fixed. Replaced by `stop-258` = 9 (row length after merge 258, recomputed 15, 13, 11, 9, 8, 7).
11. l3 screens[5] "th is the most frequent pair" (note): fixed, "`th` and `he` are its most frequent pairs, twice each."
12. l1 quiz[2] feedback "Twice the bytes" (note): fixed.
13. l1 screens[1] explain, byte widths by script (note): fixed with the suggested sentence.
14. l1 screens[3] explain, 163 (note): fixed, "between 128 and 191, so its bits already have the form `10xxxxxx`".
15. l2 screens[5] "first merges" (note): fixed, "Most of".
16. l2 quiz[0] missing pair (note): fixed, `a` then space 1 added (counts sum to 11 pairs).
17. l2 screens[8] test 7 key order (note): fixed with `[5, 6, 1, 2, 1, 2]`, first-seen `[[5, 6], [6, 1], [1, 2], [2, 1]]`; the sorted-pairs mutant still fails test 7.
18. l3 quiz[3] "same text" (note): fixed, prose says "On the same validation text".
19. problems items[2] parts[3] `over-raw` (note): fixed. Added 0.0029 (36 / 12,400, tolerance 0.0001 so it does not meet the 0.0037 band); `over-train` line now names the deduplicated corpus.
20. homework items[1] repeats and case (note): fixed. Tests 9 (`['abcdeabcde', 'abcdeabcdf']` at 0.9, expect `[]`) and 10 (case-only pair at 0.5, expect `[]`); prose states that shingles form a set and case matters; both appendix mutants added and fail tests 9 and 10.
21. gpt-L1-numbers.py full-text block (note): fixed. Records the md5 and checks 65 distinct characters in the full-text path, and the 143 split; the default path carries the digest constant. Not checkable without the text in CI: the counts themselves, as before.
22. gpt-L1-numbers.py claims without `expect` (note): fixed in part. Added expects for problems items[0] parts[2], items[2] parts[0], [1], [3], the new keys, the l4 table, homework 1.44, and the bigram recompute. Left as claims only: review items[2], [4], [8] and the l2 screens[6] bars (all agree with the files; the review's own hand check stands).
23. docs/reports/gpt-L1.md file name (note): declined. The report name is outside the level 1 content files this pass may touch, and the number script and reviews already cite `gpt-L1`; rename it with the brief's convention in a state-file pass.
24. "above" and "at least" (note): fixed, see item 6.
