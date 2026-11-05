# Exam topic-1.9 extension (cpp level 5)

File: `app/content/exams/topic-1.9.json`. 25 items to 30, minutes 60 to 75, pass 0.7. The existing 25 items and ids are untouched. `content/manifest.json` did not change (the validator wrote the same file).

## Items added

| id | kind | difficulty | skill | tag | pace | after |
| --- | --- | --- | --- | --- | --- | --- |
| e-const-move | choice | 2 | cp-memory | move-semantics | 60 | e-link-stage |
| e-vector-growth | numeric | 3 | cp-stl | noexcept-move | 90 | e-code-credit-line |
| e-ub-which | multi | 3 | cp-basics | defined-vs-undefined | 90 | e-vector-growth |
| e-virtual-dtor | choice | 4 | cp-classes | virtual-destructor | 90 | e-code-rank-fills |
| e-code-clone-basket | code (C++) | 4 | cp-classes | clone-idiom | 600 | e-virtual-dtor |

Ramp is 6, 14, 7, 3 of 30 (20%, 47%, 23%, 10%). 7 `code` items and one `longform`. Starter, solution and 11 tests were generated from `docs/briefs/cpp-scripts/P-clone-basket_*` by script (no retyping); `leakCheck: true`; `examples` are the first two tests; bool test uses `equal`, costs `isclose`.

## Numbers, computed twice
- e-vector-growth: capacity 1, 2, 4; grows at pushes 2 and 3, relocating 1 and 2 elements by copy: 3 copies, 4 moves. Native g++ run printed `copies 3 moves 4`.
- e-const-move: native run gives `a.fills.size()` 3. e-virtual-dtor: native `gone` is 1. e-ub-which: `s[s.size()]` is 0 and the wrapped `unsigned char` is 0.

## Results
- Validator: 0 errors (610 warnings elsewhere, none for topic-1.9).
- Playthrough `--exam topic-1.9 --local-cdn`: 30 of 30, passed, at desktop (40 s), `--mobile` (40 s) and `--tablet` (37 s).
- Voice scan on a scratch copy: 0 explanations over three sentences, 0 sentences over 20 words. Two long sentences in the clone item were split.
- App toolchain (`app_toolchain/run.mjs P-clone-basket`, YoWASP clang 21, c++17): solution 0 of 11 fail; starter 9 of 11 fail; mutants limit-clone-forgets-limit 2, limit-fills-above-its-limit 4, basket-clone-is-shallow-sliced 3, basket-clone-shares-nothing-but-is-empty 3, basket-cost-forgets-children 5 fail (all caught).

## Notes for the second reader
- `e-virtual-dtor` overlaps one option of `r5-virtual-dtor` (review 5, `shared`) in claim; the exam item asks for the consequence with a counter, as the brief specifies.
- `e-ub-which` lines appear in no l19 to l23 lesson, review or homework (grep checked).
- Voice: no firm named, no em-dashes, no exclamation marks.
