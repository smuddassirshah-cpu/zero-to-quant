# Engine pass G and C (agent 2): generated fluency sets and the weekly mixed review

Brief: `docs/briefs/engine-gen.md`. Backlog items 800 to 829 (status lines in `docs/ENGINE-BACKLOG.md`, last block). Author side: `docs/AUTHORING.md` section 16. Branch `worktree-agent-ae6c892c44384d187`, two commits: G (`Engine G: generated fluency sets`), C (`Engine C: weekly mixed review`).

## What works

**G, generated fluency sets (800 to 819).**
- Content shape `content/courses/<course>/fluency-<lesson>.json`, found by file name, listed in `manifest.json` under `fluency` (the manifest is unchanged while no set exists).
- `js/engine/gen.js` (new, loaded by the page and by node): safe evaluator (no `eval`, no `Function`), exact rationals in BigInt, every operator and function of the brief, every format of the brief plus `+frac` and `+dpN`, `poly(v; ...)`, seeded drawing on `ZQ.arith.rng`, redraw cap 60, families round robin by weight, no repeated prompt.
- Player: route `#fluency/<course>/<set>[/<seed>]` (`js/screens/fluency.js`) on the shared set page (`ZQ.setPage`, exported from `review.js`): start card, one item a screen, one try, wrong line then solution steps, result with pass or not at `pass`, Go again (new seed); 440 px checked.
- State `ZQ.state.fluency` (attempts, best, last score, last pass date, per family right and wrong; a part-way leave keeps only the family counts). A pass moves nothing else (the playthrough compares XP, mastery, skills, lessons, reviews, homework, exams, redo queue, prerequisites and streak before and after).
- Today: "Practice" rows in the Due card, after the due work, for a set whose lesson is done and that is not yet passed (newest lesson first, two rows and a count). Course page: a Fluency row on the lesson's card. Lesson end card: "Fluency: 20 fresh questions" line.
- Validator (`tools/fluency-rules.mjs`, called from `validate.mjs`): schema, file name, lesson on the course map, static checks of every template, then each family at 200 seeds (placeholders, typed answer graded, each wrong not graded correct, redraw rate at most 80%, 60 distinct prompts warn and 25 error), voice rules and a 35-word gate on the text as drawn. The fixture is validated on every run.
- Tools: `fluency-sample.mjs`, `test-fluency.mjs` (261 unit cases; 50 seeds of every family in the real widgets, `form` enforced), `test-validate-fluency.mjs` (30 scratch cases), playthrough `--fluency` (also in `--all`, in shard order after the sets, with the fixtures), census line, fixture `app/tools/fixtures/fluency/fluency-l3-opening-brackets.json` (five families: numeric, expanded, factorised, upToConstant, fractions).

**C, weekly mixed review (820 to 829).**
- State `ZQ.state.cumulative`: due seven days after the last review, the first seven days after the first met level; postponing keeps it due.
- `ZQ.select.cumulative.build` (pure) and `ZQ.select.weeklyReview` / `weeklyFinish`: 20 items, generated Fluency items first (weighted by wrong counts and age), then unseen authored items, then least recently seen review items; at most four per course; no long-form or code; misses of authored items join the redo queue; family counts and seen uids kept; a history row (date, score, per-level misses). Nothing gates.
- Route `#weekly` (`js/screens/weekly.js`), "Not today" on the start card, a "Weekly mixed review" row in Today's Due card above the practice rows.
- `tools/test-cumulative.mjs` (25 cases: selection with and without Fluency families, schedule, recording, on the real content) and the playthrough routes block (`cumulativeChecks`: state clock eight days on, card appears above the practice rows, postponed, played, recorded, cleared, due again after seven days).

## Commands an author runs (from `app/`)

```
node tools/validate.mjs 2>&1 | tail -5
node tools/fluency-sample.mjs --set <course>/<set id> [--family <id>] [--seed s] [--n k] --json
node tools/test-fluency.mjs --local-cdn <pkgs> --set <course>/<set id>
node tools/playthrough.mjs --fluency <course>/<set id> --local-cdn <pkgs> [--mobile]
```

## Decisions where the brief was silent (all reversible)

- **Braces in templates.** `{{` and `}}` are literal braces, so LaTeX is `\\frac{{{p}}}{{{q}}}` and `x^{{{k}}}`. Documented first thing under "Templates".
- **Numeric widgets in a family.** `answer`, `tol` values and the `wrong[].value` are templates that give a number (`"{p/q + r/s}"`); `tolerance` is accepted as another name for `tol`; a wrong numeric entry uses `value`, an expression entry `tex`.
- **Formats.** Added `+frac` and `+dpN` (each tested). No other format.
- **Expression grading in the validator.** The Compute Engine is not available to `validate.mjs` without a local copy, so the validator grades `numeric` families fully and checks expression families by text (answer and wrongs filled, wrongs not equal to the key); `test-fluency.mjs` grades every expression family in the real browser at 50 seeds. The validator's own 200-seed sampling is therefore a text check for expression families (stated in AUTHORING).
- **Cap of four per course** relaxes in steps (4, 6, 8, ...) only when too few courses are met to fill 20; otherwise a learner with two met courses would get eight questions.
- **Weekly "met levels"** are `ZQ.prereq.levelMet` levels with something written; the review's tier 3 reads the twelve levels a weekly review has covered least recently (bounded loading).
- **A Fluency attempt** logs its time as review hours and touches nothing else; it does not count toward the streak or skill scores (the brief: it gates nothing and existing progress must not move).
- **`runSet` hook** gained `answerWrong()` (numeric and expression only) for the playthrough; `ZQ.setPage` gained `back`, `backLabel`, `overview`, `againRoute`, `verdict` and `later`; the defaults leave every existing page unchanged.

## Deferred, plainly

1. **Unseen "versions" on met material (brief, C step 2).** Tier 2 draws bank items and the fixed items of topic exams not yet sat, on met courses. Fixed mock-version files (`mock-*-2`, `-3`) and stage exams are not drawn from. Cause: no per-item "seen" record exists for them beyond exam attempts; worth an item once content has Fluency sets and the bank grows.
2. **No real fluency set exists.** Content agents write them; until then the weekly review is tiers 2 and 3 only (tested both ways).
3. **Course row on mobile.** The playthrough checks the Fluency row on the desktop card; at 440 px the same `fillInfo` renders into the sheet, and the pages around it are checked for overflow, but the sheet itself is not probed.
4. **Expression `integers` and `functions` fields** are passed through to the widget but the validator does not sample-check a family that uses them beyond the text checks (they are exercised by `test-fluency.mjs` only if a set uses them; the fixture does not).
5. **Today shows at most two practice rows**; further sets are counted in a caption and listed on their course pages.
6. **Merge notes for the other worktree:** this branch touches `app/js/content.js` (two inserts: the `fluencyMeta` lines and a block before `window.ZQ.content = api`), `app/js/state.js`, `app/js/screens/today.js` (two blocks in the Due card), `app/js/screens/course.js` (`fluencyRow` and one click handler), `app/js/screens/review.js`, `app/index.html` (three script tags), `app/README.md`, and appends at the end of `docs/AUTHORING.md` and `docs/ENGINE-BACKLOG.md`. It does not touch `hours.js`, section 14, `readiness-sums.mjs` or `curriculum-hours.mjs`.

## Verification

`node tools/validate.mjs` 0 errors; `readiness-sums.mjs` OK; every `tools/test-*` green (the seven that take `--local-cdn` run with it; `test-validate-fluency` takes about 4 minutes); playthrough of the fixture, three lessons (equations/l3-opening-brackets, trig/l4-exact-values, conditional/l3-shrinking) and `--routes-only`, each at desktop and `--mobile`. The four shards are the main session's.
