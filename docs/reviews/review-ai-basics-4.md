# ai-basics level 4 (Language by counting): second-reader findings

Scope: `app/content/courses/ai-basics/` l13-what-comes-next, l14-chances-for-the-next-word, l15-writing-by-rolling-dice, l16-temperature-and-tokens, review-4, homework-4, problems-4 (at b8da7b0f).
Method: no browser. Ran `docs/reports/ai-basics-L4-numbers.py` with the venv Python (exit 0, 421 of 421; it reads the stated values from the JSON by path, recomputes them two ways and checks every `wrong[]` against its band, so it checks rather than restates; gaps under "Numbers script"). Ran `node tools/grade-all.mjs --file <f> --code --local-cdn <pkgs>` on all seven files (75 widgets, 7 Python code widgets, 0 failures). Ran 39 wrong solutions of my own against the hidden tests in CPython 3.12.3 (the same compensated `sum()` as Pyodide 0.27.7's Python 3.12), and confirmed the two survivors in Pyodide by adding them as mutants to scratch copies and rerunning `grade-all --code` (both `mutant-passes`). Recomputed every number independently with `collections.Counter`, `bisect` on running totals and `math.fsum` (course table, chances, running totals, the five u picks, the float total 0.9999999999999999 against `sum()` 1.0, both temperature rows, the four seed-7 runs, the greedy loop, fund text, share table, BoE rows, every review, homework and problem figure, token counts, and `names.txt`: 32,033 names, n row 18,327, n then end 6,763, 228,146 pairs). Every value agrees with the screen; every distractor matches its `why`; tolerances (0.0005 for 3 and 4 places, 5e-5 on p-boe) take the exact value and refuse every slip. Read every screen for teaching and voice; `voice-scan.py 35 --summary` 0 over 35 words, 0 explanations over three sentences; own scan for em-dashes, exclamation marks and American spelling found none in prose. Checked terms, tables and numbers against `ai-use` L1 (l1, l4, homework-1) and `docs/briefs/makemore.md` Level 1.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching issue or a test that a wrong solution passes; note = style or polish.

Counts: 1 error, 5 warnings, 10 notes.

## Findings

- app/content/courses/ai-basics/problems-4.json | p-boe parts[1] explain | error | "0.1 ÷ 1.6 = 0.0625: six times its chance at temperature 1". 0.0625 ÷ 0.01 = 6.25, so it is not six times. The number script checks the part's answer but not the prose ratio. | "...$0.1 \div 1.6 = 0.0625$: more than six times its chance at temperature 1."
- app/content/courses/ai-basics/l15-writing-by-rolling-dice.json | screens[8] Picking in code, tests | warning | The fall-back test (test 6, u = 0.9999999999999999 on the "the" row) is passed by a picker with no fall-back that builds each running total as `sum(chances[:i + 1])`: Python 3.12's `sum()` is compensated and returns 1.0, which is above u. The learner has met `sum()` in `first-python`. SURVIVES all 7 tests in Pyodide (appendix W13). The brief asked for chances "that sum to slightly less than 1". | Add test 8 `pick(['a', 'b', 'c'], [0.3, 0.3, 0.3999], 0.99995)` expecting `'c'` (solution 'c', the survivor `None`; checked), and add the survivor as a mutant naming test 8. Keep test 6 for the loop.
- app/content/courses/ai-basics/homework-4.json | h-bigram-writer tests | warning | No hidden test reaches the fall-back to the last word, though the prose demands it: a writer whose `chosen` starts as `None` passes all 9 tests in Pyodide (appendix W32). | Add `bigram_writer(TEXT, 'the', [0.9999999999999999], 1)` expecting `['the', 'dog']` (the loop's running total ends at 0.9999999999999999; the survivor gives `['the', None]`; checked), and add the survivor as a mutant naming it.
- app/content/courses/ai-basics/homework-4.json | h-at-or-above option 'either' why | warning | "Every boundary would then lean the same way, giving each word a little extra chance" is false: moving each boundary by one point leaves every word's chance unchanged (one value of u has chance 0; in floats a middle word gains one value at its top and loses one at its bottom). The distractor "one draw of exactly 0.5 never matters" is true as a statement about chances, so the item is ambiguous as asked ("should"). | Question: "Which word does the lessons' rule give for $u = 0.5$, and why?" Why for 'either': "Such a draw is rare, but a picker must follow one rule exactly, or its runs stop matching the tests and other seeded runs."
- app/content/courses/ai-basics/l16-temperature-and-tokens.json | screens[5] More creative?, explain; summary.ideas[1] | warning | "It never adds a word: a chance of 0 stays 0" is true of the counting table, but screen 11 then says a chatbot's setting "works just like this". A network gives almost every token a small chance above 0, so a high temperature does bring rare tokens forward; the learner may conclude it can only reorder words already seen. | Add one sentence to the explain: "A real model gives almost every token a tiny chance, so a high temperature lets rare tokens through; it still adds no knowledge."
- app/content/courses/ai-basics/l16-temperature-and-tokens.json | screens[11] Drafting a contract | warning | The transfer reuses the course row's chances ($\tfrac12, \tfrac16, \tfrac16, \tfrac16$) and the answer $\tfrac34$ from screen 2, and its first hint says so: it tests relabelling, not transfer. | Fresh chances: pay 0.6, deliver 0.2, inspect 0.2; squares 0.36, 0.04, 0.04 add to 0.44; pay 0.8182 at temperature $\tfrac12$ (checked in fractions, 9/25 ÷ 11/25 = 9/11, and floats). Slips: 0.6 (same), 0.36 (no rescale), 0.4641 (temperature 2: 0.7746 ÷ 1.6690).
- app/content/courses/ai-basics/l15-writing-by-rolling-dice.json | screens[11] A chatbot's next word, prose | note | "in just this way, with the table replaced by a big network" leaves out that the network reads all the tokens so far, not only the last word. The level says it only in homework h-long-nonsense (d); `ai-use` l1 screen 0 then builds on exactly this contrast, so one clause here makes the hand-over clean. | "...with the table replaced by a big network that reads the whole text so far, not just the last word."
- app/content/courses/ai-basics/l16-temperature-and-tokens.json | screens[0] Bold and safe, explain | note | "A is the safe writer: it nearly always takes the top word" overstates 0.75. | "A is the safe writer: it takes the top word three times in four."
- app/content/courses/ai-basics/l16-temperature-and-tokens.json | screens[10] Why pieces?, correct option and explain | note | "Pieces can spell any word" holds only if the list of pieces keeps every single character, which real tokenisers do. | Explain: "A fixed list of pieces, which keeps every single character as a last resort, can spell a word the model never saw..."
- app/content/courses/ai-basics/l16-temperature-and-tokens.json | screens[6] Temperature as a power, prose | note | The link between the temperature and the power (power = 1 ÷ temperature) is never said, so 2 and 0.5 look arbitrary; `makemore` L3 returns to temperature. Stage 0 can follow it ($1 \div \tfrac12 = 2$). | Add: "The power is 1 divided by the temperature: $1 \div \tfrac12 = 2$ and $1 \div 2 = \tfrac12$."
- app/content/courses/ai-basics/l16-temperature-and-tokens.json | screens[9] Three ways to split, prose | note | Spaces are left out of every split with no word on why; real tokenisers keep the space, usually joined to the next piece. | Add: "Real models keep the spaces too, usually stuck to the front of the next piece."
- app/content/courses/ai-basics/homework-4.json | h-long-nonsense model (d) | note | "A low temperature repeats the likeliest pairs, as in 'the cat sat on the cat sat on'": that loop is the greedy writer (temperature towards 0); at $\tfrac12$ the writer still samples. | "A temperature near 0 repeats the likeliest pairs, as in..."
- app/content/courses/ai-basics/l13-what-comes-next.json | screens[9] A trader's keyboard, prose against explain | note | The prose says a phone keyboard "suggests your next word from a giant table of this kind"; the explain then says modern keyboards use networks. | Prose: "Early phone keyboards suggested your next word from a giant table of this kind."
- app/content/courses/ai-basics/l14-chances-for-the-next-word.json, l16-temperature-and-tokens.json | screens[7] widget.how | note | `math.isclose` in prose without code formatting (reads as American "math"). | `` `math.isclose` ``
- docs/reports/ai-basics-L4-numbers.py | whole script | note | It checks answers, wrongs and the seed-7 console from the JSON, but not numbers stated in explain prose (the p-boe "six times" slipped through), and it restates some inputs as literals instead of reading the canvas: the l14 share table (68, 62, 61, 58), the l16 pieces count 5, the roots total 1.9319. | Read `screens[9].canvas.params.rows` in l14 and the l16 pieces cells; add a claim for the p-boe ratio 6.25 once the prose is fixed.
- app/content/courses/ai-use/l1-reading-the-internet.json, l4-confident-and-wrong.json (downstream, outside scope) | screens[0], screens[1] | note | They write words in straight quotes ("the") where ai-basics L4 uses curly quotes (“the”); terms, the row for "the" (3, 1, 1, 1 and $\tfrac12, \tfrac16, \tfrac16, \tfrac16$), "next-word table" and "token" otherwise match. | For the ai-use owner: curly quotes, if `AUTHORING.md` prefers them.

## Downstream check (ai-use L1, makemore L1)

- `ai-use` L1: l1 screen 0 reproduces the row for "the" exactly and names it a next-word table; "token" is defined as "a word or a piece of one, as in ai-basics", matching l16; l4's sentence chance $\tfrac16 \times \tfrac16 = \tfrac1{36}$ and "11 runs in 12" recompute (the three text sentences each have chance $\tfrac1{36}$ from "the"). l15's "ai-use level 1 shows how such a network is trained" is true (pretraining). No gap besides the context clause (note above).
- `makemore` L1 brief: n then end 6,763 (review-4 r-names-n, from `names.txt`), 32,033 names, the n row 18,327 and 228,146 pairs all agree; ".emma." with start and end marks and five pairs (homework h-emma) matches its l1 explore; its l2 trap (whole table total against the row total) is l14's trap at letter scale; "the next-word table there is this table with words for letters" holds. `row_chances` triples are not used downstream.

## Appendix: wrong solutions

39 sources, run against each widget's hidden tests (first failing test shown). Survivors marked SURVIVES; W13 and W32 were confirmed in Pyodide with `grade-all --code`. Four entries are correct solutions by another route (marked "should pass"), to confirm the tests do not refuse valid code: W5, W10, W26 and W34 all pass, and W26 and W34 confirm that a temperature applied to counts or to chances gives the same rescaled row, as h-bigram-writer's explain says.

### W1. l13-what-comes-next Counting pairs in code: does not count pairs across a sentence end (skips any pair that touches a full stop)

Result: fails hidden test 1.

```python
def count_pairs(words):
    pairs = []
    for i in range(len(words) - 1):
        if words[i] != '.' and words[i + 1] != '.':
            pairs.append((words[i], words[i + 1]))
    pairs = sorted(pairs)
    result = []
    for p in pairs:
        if len(result) > 0 and result[-1][0] == p[0] and result[-1][1] == p[1]:
            result[-1] = (p[0], p[1], result[-1][2] + 1)
        else:
            result.append((p[0], p[1], 1))
    return result
```

### W2. l13-what-comes-next Counting pairs in code: counts each pair with str.count on the joined text (misses overlapping repeats)

Result: fails hidden test 5.

```python
def count_pairs(words):
    joined = ' ' + ' '.join(words) + ' '
    pairs = []
    for i in range(len(words) - 1):
        pairs.append((words[i], words[i + 1]))
    result = []
    for p in sorted(pairs):
        if len(result) == 0 or result[-1][:2] != p:
            result.append((p[0], p[1], joined.count(' ' + p[0] + ' ' + p[1] + ' ')))
    return result
```

### W3. l13-what-comes-next Counting pairs in code: loops one word too far (range(len(words)))

Result: fails hidden test 1.

```python
def count_pairs(words):
    pairs = []
    for i in range(len(words)):
        pairs.append((words[i], words[(i + 1) % len(words)]))
    pairs = sorted(pairs)
    result = []
    for p in pairs:
        if len(result) > 0 and result[-1][0] == p[0] and result[-1][1] == p[1]:
            result[-1] = (p[0], p[1], result[-1][2] + 1)
        else:
            result.append((p[0], p[1], 1))
    return result
```

### W4. l13-what-comes-next Counting pairs in code: keeps first-seen order instead of sorting

Result: fails hidden test 1.

```python
def count_pairs(words):
    result = []
    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        found = False
        for k in range(len(result)):
            if result[k][0] == a and result[k][1] == b:
                result[k] = (a, b, result[k][2] + 1)
                found = True
        if not found:
            result.append((a, b, 1))
    return result
```

### W5. l13-what-comes-next Counting pairs in code: right idea by another route: set of pairs, then list.count (correct, should pass)

Result: passes every hidden test (expected: a correct solution).

```python
def count_pairs(words):
    pairs = []
    for i in range(len(words) - 1):
        pairs.append((words[i], words[i + 1]))
    result = []
    for p in sorted(set(pairs)):
        result.append((p[0], p[1], pairs.count(p)))
    return result
```

### W6. l14-chances-for-the-next-word Chances in code: divides by the largest count instead of the row total

Result: fails hidden test 1.

```python
def chances(counts):
    return [c / max(counts) for c in counts]
```

### W7. l14-chances-for-the-next-word Chances in code: total over all but the first count (off by one in the loop)

Result: fails hidden test 1.

```python
def chances(counts):
    total = 0
    for i in range(1, len(counts)):
        total = total + counts[i]
    return [c / total for c in counts]
```

### W8. l14-chances-for-the-next-word Chances in code: hard-codes the row total of 6 for the row for the

Result: fails hidden test 2.

```python
def chances(counts):
    return [c / 6 for c in counts]
```

### W9. l14-chances-for-the-next-word Chances in code: integer division

Result: fails hidden test 1.

```python
def chances(counts):
    total = 0
    for c in counts:
        total = total + c
    return [c // total for c in counts]
```

### W10. l14-chances-for-the-next-word Chances in code: right idea by another route: sum() (correct, should pass)

Result: passes every hidden test (expected: a correct solution).

```python
def chances(counts):
    return [c / sum(counts) for c in counts]
```

### W11. l15-writing-by-rolling-dice Picking in code: off-by-one in the cumulative walk: compares before adding the chance

Result: fails hidden test 1.

```python
def pick(words, chances, u):
    total = 0
    for i in range(len(words)):
        if u < total:
            return words[i]
        total = total + chances[i]
    return words[-1]
```

### W12. l15-writing-by-rolling-dice Picking in code: off-by-one the other way: returns the word after the one whose total is above u

Result: fails hidden test 1.

```python
def pick(words, chances, u):
    total = 0
    for i in range(len(words) - 1):
        total = total + chances[i]
        if u < total:
            return words[i + 1]
    return words[-1]
```

### W13. l15-writing-by-rolling-dice Picking in code: no fallback, running total by sum() of a slice (compensated in Python 3.12)

Result: SURVIVES (passes every hidden test).

```python
def pick(words, chances, u):
    for i in range(len(words)):
        if u < sum(chances[:i + 1]):
            return words[i]
```

### W14. l15-writing-by-rolling-dice Picking in code: falls back to the first word instead of the last

Result: fails hidden test 6.

```python
def pick(words, chances, u):
    total = 0
    for i in range(len(words)):
        total = total + chances[i]
        if u < total:
            return words[i]
    return words[0]
```

### W15. l15-writing-by-rolling-dice Picking in code: unseeded: ignores u and draws its own random number

Result: fails hidden test 1.

```python
import random
def pick(words, chances, u):
    u = random.random()
    total = 0
    for i in range(len(words)):
        total = total + chances[i]
        if u < total:
            return words[i]
    return words[-1]
```

### W16. l15-writing-by-rolling-dice Picking in code: returns the last word inside the loop on the first miss

Result: fails hidden test 2.

```python
def pick(words, chances, u):
    total = 0
    for i in range(len(words)):
        total = total + chances[i]
        if u < total:
            return words[i]
        else:
            return words[-1]
```

### W17. l15-writing-by-rolling-dice Writing in code: unseeded: draws its own random numbers instead of using us

Result: fails hidden test 1.

```python
def pick(words, chances, u):
    total = 0
    for i in range(len(words)):
        total = total + chances[i]
        if u < total:
            return words[i]
    return words[-1]

import random
def generate(table, start, us):
    out = [start]
    word = start
    for u in us:
        words, chances = row_for(table, word)
        word = pick(words, chances, random.random())
        out.append(word)
    return out
```

### W18. l15-writing-by-rolling-dice Writing in code: seeds its own Random(7) inside the function

Result: fails hidden test 1.

```python
def pick(words, chances, u):
    total = 0
    for i in range(len(words)):
        total = total + chances[i]
        if u < total:
            return words[i]
    return words[-1]

import random
def generate(table, start, us):
    rng = random.Random(7)
    out = [start]
    word = start
    for u in us:
        words, chances = row_for(table, word)
        word = pick(words, chances, rng.random())
        out.append(word)
    return out
```

### W19. l15-writing-by-rolling-dice Writing in code: appends the word before picking, so the list ends one word short

Result: fails hidden test 1.

```python
def pick(words, chances, u):
    total = 0
    for i in range(len(words)):
        total = total + chances[i]
        if u < total:
            return words[i]
    return words[-1]

def generate(table, start, us):
    out = []
    word = start
    for u in us:
        out.append(word)
        words, chances = row_for(table, word)
        word = pick(words, chances, u)
    return out
```

### W20. l15-writing-by-rolling-dice Writing in code: skips the first u (off by one over us)

Result: fails hidden test 1.

```python
def pick(words, chances, u):
    total = 0
    for i in range(len(words)):
        total = total + chances[i]
        if u < total:
            return words[i]
    return words[-1]

def generate(table, start, us):
    out = [start]
    word = start
    for u in us[1:]:
        words, chances = row_for(table, word)
        word = pick(words, chances, u)
        out.append(word)
    return out
```

### W21. l16-temperature-and-tokens Temperature in code: temperature as the power itself (power 2 read as temperature 2)

Result: fails hidden test 1.

```python
def with_temperature(chances, power):
    raised = [c ** (1 / power) for c in chances]
    total = sum(raised)
    return [round(r / total, 4) for r in raised]
```

### W22. l16-temperature-and-tokens Temperature in code: rescales first, then raises (no rescale after)

Result: fails hidden test 1.

```python
def with_temperature(chances, power):
    total = sum(chances)
    return [round((c / total) ** power, 4) for c in chances]
```

### W23. l16-temperature-and-tokens Temperature in code: rounds the raised values before rescaling

Result: fails hidden test 1.

```python
def with_temperature(chances, power):
    raised = [round(c ** power, 4) for c in chances]
    total = sum(raised)
    return [round(r / total, 4) for r in raised]
```

### W24. l16-temperature-and-tokens Temperature in code: never rounds

Result: fails hidden test 1.

```python
def with_temperature(chances, power):
    raised = [c ** power for c in chances]
    total = sum(raised)
    return [r / total for r in raised]
```

### W25. l16-temperature-and-tokens Temperature in code: precedence slip: c ** 1 / power

Result: fails hidden test 1.

```python
def with_temperature(chances, power):
    raised = [c ** 1 / power for c in chances]
    total = sum(raised)
    return [round(r / total, 4) for r in raised]
```

### W26. l16-temperature-and-tokens Temperature in code: applied to counts instead of chances (scaled the row by 6 first; equivalent, should pass)

Result: passes every hidden test (expected: a correct solution).

```python
def with_temperature(chances, power):
    counts = [c * 6 for c in chances]
    raised = [c ** power for c in counts]
    total = sum(raised)
    return [round(r / total, 4) for r in raised]
```

### W27. homework-4 h-row-chances: row total from words.count(word), which counts a final word that starts no pair

Result: fails hidden test 4.

```python
def row_chances(text, word):
    words = text.split()
    nexts = []
    counts = []
    for i in range(len(words) - 1):
        if words[i] == word:
            b = words[i + 1]
            if b in nexts:
                counts[nexts.index(b)] += 1
            else:
                nexts.append(b)
                counts.append(1)
    total = words.count(word)
    return [(nexts[k], counts[k], total) for k in range(len(nexts))]
```

### W28. homework-4 h-row-chances: reduces each fraction (3, 6) to (1, 2)

Result: fails hidden test 1.

```python
import math
def row_chances(text, word):
    words = text.split()
    nexts = []
    counts = []
    for i in range(len(words) - 1):
        if words[i] == word:
            b = words[i + 1]
            if b in nexts:
                counts[nexts.index(b)] += 1
            else:
                nexts.append(b)
                counts.append(1)
    total = sum(counts)
    return [(nexts[k], counts[k] // math.gcd(counts[k], total), total // math.gcd(counts[k], total)) for k in range(len(nexts))]
```

### W29. homework-4 h-row-chances: sorts the next words instead of first-seen order

Result: fails hidden test 1.

```python
def row_chances(text, word):
    words = text.split()
    nexts = []
    for i in range(len(words) - 1):
        if words[i] == word:
            nexts.append(words[i + 1])
    out = []
    for b in sorted(set(nexts)):
        out.append((b, nexts.count(b), len(nexts)))
    return out
```

### W30. homework-4 h-row-chances: does not count pairs across a sentence end (skips a next word of ".")

Result: fails hidden test 2.

```python
def row_chances(text, word):
    words = text.split()
    nexts = []
    counts = []
    for i in range(len(words) - 1):
        if words[i] == word and words[i + 1] != '.':
            b = words[i + 1]
            if b in nexts:
                counts[nexts.index(b)] += 1
            else:
                nexts.append(b)
                counts.append(1)
    total = sum(counts)
    return [(nexts[k], counts[k], total) for k in range(len(nexts))]
```

### W31. homework-4 h-row-chances: total = all pairs of the text

Result: fails hidden test 1.

```python
def row_chances(text, word):
    words = text.split()
    nexts = []
    counts = []
    for i in range(len(words) - 1):
        if words[i] == word:
            b = words[i + 1]
            if b in nexts:
                counts[nexts.index(b)] += 1
            else:
                nexts.append(b)
                counts.append(1)
    return [(nexts[k], counts[k], len(words) - 1) for k in range(len(nexts))]
```

### W32. homework-4 h-bigram-writer: no fallback to the last word (chosen starts as None)

Result: SURVIVES (passes every hidden test).

```python
def bigram_writer(text, start, us, power):
    words = text.split()
    heads = []
    nexts = []
    counts = []
    for i in range(len(words) - 1):
        a = words[i]
        b = words[i + 1]
        if a not in heads:
            heads.append(a)
            nexts.append([])
            counts.append([])
        k = heads.index(a)
        if b in nexts[k]:
            counts[k][nexts[k].index(b)] += 1
        else:
            nexts[k].append(b)
            counts[k].append(1)
    out = [start]
    word = start
    for u in us:
        if word not in heads:
            break
        k = heads.index(word)
        raised = [c ** power for c in counts[k]]
        total = sum(raised)
        chosen = None
        running = 0
        for j in range(len(raised)):
            running = running + raised[j] / total
            if u < running:
                chosen = nexts[k][j]
                break
        word = chosen
        out.append(word)
    return out
```

### W33. homework-4 h-bigram-writer: temperature on the chances, then no rescale (raise after dividing)

Result: fails hidden test 5.

```python
def bigram_writer(text, start, us, power):
    words = text.split()
    heads = []
    nexts = []
    counts = []
    for i in range(len(words) - 1):
        a = words[i]
        b = words[i + 1]
        if a not in heads:
            heads.append(a)
            nexts.append([])
            counts.append([])
        k = heads.index(a)
        if b in nexts[k]:
            counts[k][nexts[k].index(b)] += 1
        else:
            nexts[k].append(b)
            counts[k].append(1)
    out = [start]
    word = start
    for u in us:
        if word not in heads:
            break
        k = heads.index(word)
        total = sum(counts[k])
        raised = [(c / total) ** power for c in counts[k]]
        chosen = nexts[k][-1]
        running = 0
        for j in range(len(raised)):
            running = running + raised[j]
            if u < running:
                chosen = nexts[k][j]
                break
        word = chosen
        out.append(word)
    return out
```

### W34. homework-4 h-bigram-writer: temperature on the chances, rescaled (equivalent to counts, should pass)

Result: passes every hidden test (expected: a correct solution).

```python
def bigram_writer(text, start, us, power):
    words = text.split()
    heads = []
    nexts = []
    counts = []
    for i in range(len(words) - 1):
        a = words[i]
        b = words[i + 1]
        if a not in heads:
            heads.append(a)
            nexts.append([])
            counts.append([])
        k = heads.index(a)
        if b in nexts[k]:
            counts[k][nexts[k].index(b)] += 1
        else:
            nexts[k].append(b)
            counts[k].append(1)
    out = [start]
    word = start
    for u in us:
        if word not in heads:
            break
        k = heads.index(word)
        total = sum(counts[k])
        raised = [(c / total) ** power for c in counts[k]]
        t2 = sum(raised)
        chosen = nexts[k][-1]
        running = 0
        for j in range(len(raised)):
            running = running + raised[j] / t2
            if u < running:
                chosen = nexts[k][j]
                break
        word = chosen
        out.append(word)
    return out
```

### W35. homework-4 h-bigram-writer: power read as the temperature (1 / power)

Result: fails hidden test 2.

```python
def bigram_writer(text, start, us, power):
    words = text.split()
    heads = []
    nexts = []
    counts = []
    for i in range(len(words) - 1):
        a = words[i]
        b = words[i + 1]
        if a not in heads:
            heads.append(a)
            nexts.append([])
            counts.append([])
        k = heads.index(a)
        if b in nexts[k]:
            counts[k][nexts[k].index(b)] += 1
        else:
            nexts[k].append(b)
            counts[k].append(1)
    out = [start]
    word = start
    for u in us:
        if word not in heads:
            break
        k = heads.index(word)
        raised = [c ** (1 / power) for c in counts[k]]
        total = sum(raised)
        chosen = nexts[k][-1]
        running = 0
        for j in range(len(raised)):
            running = running + raised[j] / total
            if u < running:
                chosen = nexts[k][j]
                break
        word = chosen
        out.append(word)
    return out
```

### W36. homework-4 h-bigram-writer: off-by-one in the cumulative walk: compares before adding

Result: fails hidden test 1.

```python
def bigram_writer(text, start, us, power):
    words = text.split()
    heads = []
    nexts = []
    counts = []
    for i in range(len(words) - 1):
        a = words[i]
        b = words[i + 1]
        if a not in heads:
            heads.append(a)
            nexts.append([])
            counts.append([])
        k = heads.index(a)
        if b in nexts[k]:
            counts[k][nexts[k].index(b)] += 1
        else:
            nexts[k].append(b)
            counts[k].append(1)
    out = [start]
    word = start
    for u in us:
        if word not in heads:
            break
        k = heads.index(word)
        raised = [c ** power for c in counts[k]]
        total = sum(raised)
        chosen = nexts[k][-1]
        running = 0
        for j in range(len(raised)):
            if u < running:
                chosen = nexts[k][j]
                break
            running = running + raised[j] / total
        word = chosen
        out.append(word)
    return out
```

### W37. homework-4 h-bigram-writer: next words sorted instead of first-seen order

Result: fails hidden test 3.

```python
def bigram_writer(text, start, us, power):
    words = text.split()
    out = [start]
    word = start
    for u in us:
        nx = [words[i + 1] for i in range(len(words) - 1) if words[i] == word]
        if len(nx) == 0:
            break
        row = sorted(set(nx))
        raised = [nx.count(b) ** power for b in row]
        total = sum(raised)
        chosen = row[-1]
        running = 0
        for j in range(len(row)):
            running = running + raised[j] / total
            if u < running:
                chosen = row[j]
                break
        word = chosen
        out.append(word)
    return out
```

### W38. homework-4 h-bigram-writer: unseeded: draws its own random numbers

Result: fails hidden test 1.

```python
def bigram_writer(text, start, us, power):
    words = text.split()
    heads = []
    nexts = []
    counts = []
    for i in range(len(words) - 1):
        a = words[i]
        b = words[i + 1]
        if a not in heads:
            heads.append(a)
            nexts.append([])
            counts.append([])
        k = heads.index(a)
        if b in nexts[k]:
            counts[k][nexts[k].index(b)] += 1
        else:
            nexts[k].append(b)
            counts[k].append(1)
    import random
    out = [start]
    word = start
    for u in us:
        if word not in heads:
            break
        k = heads.index(word)
        raised = [c ** power for c in counts[k]]
        total = sum(raised)
        chosen = nexts[k][-1]
        running = 0
        r = random.random()
        for j in range(len(raised)):
            running = running + raised[j] / total
            if r < running:
                chosen = nexts[k][j]
                break
        word = chosen
        out.append(word)
    return out
```

### W39. homework-4 h-bigram-writer: does not count pairs across a sentence end (skips pairs that touch ".")

Result: fails hidden test 3.

```python
def bigram_writer(text, start, us, power):
    words = text.split()
    out = [start]
    word = start
    for u in us:
        nx = [words[i + 1] for i in range(len(words) - 1) if words[i] == word and words[i] != '.' and words[i + 1] != '.']
        if len(nx) == 0:
            break
        row = []
        for b in nx:
            if b not in row:
                row.append(b)
        raised = [nx.count(b) ** power for b in row]
        total = sum(raised)
        chosen = row[-1]
        running = 0
        for j in range(len(row)):
            running = running + raised[j] / total
            if u < running:
                chosen = row[j]
                break
        word = chosen
        out.append(word)
    return out
```

