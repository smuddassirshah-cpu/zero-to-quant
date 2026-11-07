# Review size audit (PLAN section 5, session X, 7 Nov)

Question (review-first-python-1-3 item E): AUTHORING section 11 says a level that others require should carry 12 or more review items, so a test-out retake (6 items, items not yet shown drawn first) gives a fully new second paper. How many gating levels fall short?

Method: `course.json` of all 79 courses and every exam file read by a script (`docs/reports/review-size-audit.py`, run from the repo root; output below). A level counts as required when a gating entry (`gate` not false) in another level's `requires`, a `lessonRequires` list or an exam's `requires` names it as `course/L<n>`. Counted apart: levels named only by a lesson reference (`course/<lesson-id>`) or only by the implicit previous-level edge.

## Result

| set | levels | reviews under 12 items | items missing to reach 12 |
|---|---|---|---|
| required by a gating level or exam reference | 206 | 206 (all) | 620 |
| required only implicitly or by a lesson reference | 48 | 48 (all) | 150 |

Size histogram of the 206: 51 reviews hold 8 items, 106 hold 9, 49 hold 10. No level review in the app holds more than 10, because `docs/LEVEL-BRIEF.md` "What to write" asks for 6 to 10 review items. The two rules contradict each other, and every author followed LEVEL-BRIEF.

## Assessment

This is not a first-python fault. It is app-wide and structural. Authoring 620 items (about 70 reviews' worth) with second reads is a multi-session content wave, and the items would exist only to feed the test-out retake. Cheaper routes, for the user to choose:

1. Engine: draw 5 items for a test-out instead of 6 (pass at 4 of 5 at 0.8), so a 10-item review already gives two fully new papers; 8 and 9-item reviews still repeat 1 or 2 items. One-line change in `prereq.js` plus the test-out test.
2. Engine: keep 6 items and accept a partial repeat on the retake; the seen-set already puts unseen items first, so a 9-item review repeats 3 of 6 on paper two. Change section 11 to say "10 or more" and raise LEVEL-BRIEF to "8 to 10".
3. Content: author to 12 for the 206 levels (620 items), interview courses and Stages 2 and 3 first, as a Phase after the performance-task retrofit.

Recommendation: route 1 now (it needs no content), and route 3 only for the levels whose test-out matters most (the interview courses, 26 levels, about 70 items). No authoring was started in session X; this report precedes it as PLAN section 5 asks.

## Per-level list

Columns: level, review items, gating dependants, lesson-reference dependants, implicit dependants.

    algo-think/L1            8   1   0   1
    algo-think/L2            9   2   0   1
    algo-think/L3            9   2   0   0
    alpha/L2                 9   1   0   0
    alpha/L3                 9   1   0   0
    analysis/L1              9   1   0   0
    analysis/L2              9   1   0   0
    analysis/L3              9   1   0   0
    analysis/L4              8   1   0   0
    analysis/L5              9   1   0   0
    arma/L2                  9   2   0   1
    arma/L3                  8   1   0   0
    backtest/L1              9   1   0   0
    backtest/L2              9   2   0   0
    backtest/L4              9   1   0   0
    brainteasers/L1          9   4   0   0
    brainteasers/L2         10   1   0   0
    brainteasers/L3         10   1   0   0
    coding-int/L1           10   1   0   0
    coding-int/L2           10   2   0   0
    coding-int/L3           10   1   0   0
    coding-int/L4           10   2   0   0
    coint/L3                 8   1   0   0
    complex/L1              10   2   0   0
    complex/L2               9   1   0   0
    conditional/L1          10   1   0   1
    conditional/L2           9   3   0   1
    conditional/L3           9   1   0   1
    conditional/L4           8   1   0   1
    contests/L2             10   1   0   1
    contests/L3              8   1   0   0
    convex/L2               10   1   0   0
    convex/L3               10   1   0   0
    counting-chance/L2       8   3   0   1
    counting-chance/L3       8   2   0   0
    counting/L1              9   1   0   1
    counting/L2              9   1   1   0
    counting/L3              9   2   0   0
    cpp-pricing/L1           8   2   0   0
    cpp-pricing/L2           8   2   0   0
    cpp/L1                   8   1   0   1
    cpp/L2                   8   1   0   1
    cpp/L3                   9   1   0   1
    cpp/L4                   9   2   0   1
    cpp/L5                  10   1   0   0
    ds/L2                    9   1   0   1
    ds/L3                    8   2   0   0
    ds/L4                    9   1   0   0
    eigen/L1                 9   2   0   0
    eigen/L2                 8   4   0   1
    eigen/L3                10   2   0   0
    eigen/L4                10   1   0   0
    elimination/L2          10   2   0   1
    elimination/L3          10   1   0   0
    ensembles/L3             8   1   0   0
    equations/L1             9   4   0   1
    equations/L2            10   3   0   1
    equations/L3             8   5   2   1
    equations/L4             9   2   0   0
    estimation/L1            9   3   0   0
    estimation/L2           10   1   1   0
    estimation/L3            9   1   0   0
    exp-log/L2               8   2   0   1
    exp-log/L3               9   4   0   0
    fin-ml/L2                8   1   0   1
    fin-ml/L3                9   2   0   0
    first-python/L1          8   1   0   0
    first-python/L2          8   1   0   0
    first-python/L3          8   1   0   0
    functions/L1             9   2   0   0
    functions/L2             9   3   0   1
    functions/L3             8   3   0   0
    functions/L4             9   3   0   0
    game-theory/L1           9   1   0   0
    game-theory/L2           9   1   0   0
    game-theory/L3          10   1   0   0
    garch/L1                10   1   0   0
    git/L3                   9   1   0   0
    graphs-dp/L1             8   1   0   0
    graphs-dp/L2             8   2   0   1
    graphs-dp/L4             8   2   0   0
    integrals/L1             9   1   0   0
    integrals/L2             9   4   0   0
    integrals/L3             9   3   0   0
    integrals/L4             9   1   0   0
    ito/L1                   9   1   0   0
    ito/L2                  10   1   0   1
    ito/L3                  10   3   0   0
    ito/L4                   9   1   0   0
    least-squares/L1         8   1   0   1

Levels required only implicitly or by a lesson reference (48) are listed in the script output and are the next level of their own course in every case but the lesson references into equations L3, counting L2 and estimation L2.
