# Engine brief: generated fluency sets (G), cumulative review (C), in-app hours (session Y)

Source: `docs/reviews/critical-review-fable-5-2.md` (4.1, change 2) and `docs/reviews/critical-review-fable-5-2/self-containment-gaps.md` (G, C). The design below is decided; raise a blocker rather than redesign. Record status lines in `docs/ENGINE-BACKLOG.md` and author-facing behaviour in `docs/AUTHORING.md` (new section 16 for G and C; section 14 for hours).

Two agents work at once in separate worktrees. Agent 1: inbox numbering and hours (items 705 upward, below 800). Agent 2: G (items 800 to 819) then C (820 to 829). Each commits in its own worktree branch and never pushes. Neither edits `app/content/` except the fixtures named here.

## Agent 1

1. Number every un-numbered bullet of `docs/BACKLOG-INBOX.md` into `docs/ENGINE-BACKLOG.md` from 705, in the existing manner (mark each inbox bullet "numbered n"). Do not implement them. Stop and report if the count would pass 799.
2. In-app hours shown apart from outside hours. `ZQ.hours` (the only place hours are added, AUTHORING 14) gains an in-app figure per lesson, course, topic, stage and role: authored lesson minutes plus the stated minutes of reviews, homework and exams where the files state them (a fixed allowance per set where they do not; state it in AUTHORING). Outside hours are the stored total minus in-app, floored at 0. Learn's header, stage cards and topic cards, the course page and `docs/readiness.md` (through `readiness-sums.mjs` and `curriculum-hours.mjs`) show both, in-app first: "Trader route: 630 lessons, about 150 h in the app, about 1,650 h of outside study". No surface shows the stored total alone. `readiness-sums.mjs` must still print OK; add the new fields to its check. A test `tools/test-hours-split.mjs`.

## Agent 2: G, generated fluency sets

Purpose: 20 fresh typed-answer items per procedural lesson, pass at 90%, repeatable for ever, authored by content agents as JSON only.

### Content shape (authors write this; no engine code per family)

`app/content/courses/<course>/fluency-<lesson-id>.json`, one set per lesson, found by file name (no `course.json` edit; the validator lists sets in `manifest.json`).

```json
{ "id": "fluency-l3-opening-brackets", "lesson": "l3-opening-brackets", "title": "Fluency: opening brackets",
  "n": 20, "pass": 0.9, "minutes": 10,
  "families": [
    { "id": "expand-single", "weight": 2, "skill": "expand a single bracket",
      "vars": { "a": { "int": [2, 9] }, "b": { "int": [-9, 9], "not": [0] }, "v": { "pick": ["x", "y", "t"] } },
      "let": { "p": "a*b" },
      "where": ["gcd(a, abs(b)) == 1"],
      "prompt": "Expand ${a}({v}{b:+})$.",
      "widget": { "kind": "expression", "answer": "{a}{v}{p:+}", "form": "expanded" },
      "wrong": [ { "id": "first-term-only", "tex": "{a}{v}{b:+}", "line": "You multiplied only the first term by {a}." } ],
      "solution": ["${a} \\times {v} = {a}{v}$ and ${a} \\times {b:()} = {p}$.", "So ${a}{v}{p:+}$."] } ] }
```

- `vars`: `int` (inclusive range), `pick` (list of numbers or strings), `not` (excluded values), `step`. Drawn from a seeded generator (reuse `ZQ.arith.rng`).
- `let`: derived values, in order, by a small safe evaluator written for this (no `eval`, no `Function`): `+ - * / ^ %`, comparison and `and`/`or` in `where`, and `gcd lcm abs min max floor ceil round(x, dp) sqrt comb fact sign`, plus exact rationals (`a/b` stays a reduced fraction until formatted). `where`: all must hold, else redraw (cap the redraws; the validator fails a family that rejects more than 80% of draws).
- Formats inside `{...}` in `prompt`, `widget`, `wrong`, `solution`: `{x}` plain; `{x:+}` signed term (`+3`, `-3`); `{x:c}` coefficient (1 gives nothing, -1 gives `-`); `{x:+c}` signed coefficient; `{x:()}` brackets when negative; `{x:frac}` reduced `\frac{}{}` or a whole number; `{x:dp2}` fixed decimals; and `{poly(v; c2, c1, c0)}` which writes a clean polynomial (no zero terms, no coefficient 1, signs joined). Any expression may sit before the colon (`{a*b:+}`). Document the list in AUTHORING; add a format only with a test.
- `widget`: `numeric` or `expression` only, every field the existing widgets take (`form`, `upToConstant`, `tolerance`, `integers`, `accept`), templated. Grading goes through the existing graders unchanged. No `choice`.
- Family mix: `weight`; a set draws `n` items, no two with the same prompt, families round robin by weight.

### Player

- A Fluency set opens from its lesson's row on the course page and from the lesson's end card ("Fluency: 20 fresh questions"). One item per screen, typed answer, immediate right or wrong; on wrong, the matched `wrong` line if any, then the `solution` steps. No hints, no second try on the same item. End card: score, pass or not at `pass`, "Go again" (new seed).
- State: per set, attempts, best score, last pass date, and per family the right and wrong counts (for C). Nothing keys on generated item text. A Fluency pass does not change the met rule and gates nothing (existing progress must not move); until first passed, a set whose lesson is done shows on Today under practice, after due reviews.
- Works at 440 px; keyboard as the widget's `keyboard` field.

### Validator, tools, tests

- `validate.mjs`: schema errors; `lesson` must exist in the same course; every family is sampled at 200 seeds in node and each sample must (a) fill every placeholder, (b) grade its own `answer` correct through the real grader path used by `test-expr-equations.mjs` where that needs Compute Engine, otherwise in a separate tool below, (c) grade each `wrong` as not correct, (d) stay under the redraw cap. A family must give at least 60 distinct prompts in 200 draws (warn under 60, error under 25). Voice rules apply to `prompt`, `line` and `solution` text.
- `tools/fluency-sample.mjs --set <course>/<set id> [--family id] [--seed s] [--n k] --json`: prints drawn items with resolved prompt, answer, wrongs and the variable values. Authors feed this to their Python recompute script, which must derive each answer independently from the variable values.
- `tools/test-fluency.mjs --local-cdn <pkgs>`: grades every family of every set at 50 seeds in the real browser grader (answer correct, each `wrong` incorrect, `form` enforced: for a `form` family the prompt's own expression typed back must fail). Also unit tests of the evaluator and each format.
- `playthrough.mjs`: `--fluency <course>/<set id>` plays one set right through (pass run and a fail run), desktop and `--mobile`; `--all` includes every set in the shard list after sets; overflow checks as for lessons.
- Fixture: one sample set marked `"sample": true` under `app/tools/fixtures/` (not in `app/content/`), with at least four families (numeric, expanded, factorised, upToConstant), used by the tests. Census (`census.mjs`) prints "Fluency sets N (families M)".

## Agent 2: C, cumulative review due on Today (after G)

- Once a week per learner (seven days after the last one was finished, first one seven days after the first met level), Today shows "Weekly mixed review" as due work, above optional practice. Not opt-in; it can be postponed but stays due.
- 20 items from every met level, built in `select.js`: first generated items from Fluency families of met levels' lessons (weighted towards families with more wrong answers and older last practice), then authored items the learner has never seen (unseen bank items and unseen versions on met material), then review items least recently seen. Spread across topics: no more than four items from one course. With no Fluency sets written yet it must still work from authored items.
- Result is recorded (date, score, per-level misses); a miss feeds the existing redo queue. No gate.
- `tools/test-cumulative.mjs`: selection rules on seeded states, with and without Fluency sets. Playthrough: the routes block advances the clock and checks the card appears, plays it and checks it clears.

## Finish (each agent)

`node tools/validate.mjs` 0 errors; `readiness-sums.mjs` OK; every `tools/test-*` green (six need `--local-cdn`); playthrough of the fixture set, three lessons and `--routes-only`, desktop and `--mobile`. The main session runs the four shards. Report to `docs/reports/engine-gen-<agent>.md` (deferred items listed plainly); hand back at most six lines.
