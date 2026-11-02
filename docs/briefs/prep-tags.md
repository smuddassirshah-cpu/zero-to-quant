# Prep tags and "Prepare for" paths (user request, 2 Nov 2026)

The user asked for lessons to carry a tag saying which assessments they prepare for: a generic "General interview prep" tag, tags for the online assessment (OA), interview and superday stages, and firm tags that name the firm. Firm names are allowed here (user decision, 2 Nov), in addition to recruiting l4 and mock exam descriptions.

Two parts, in order: an engine pass (ENGINE-BACKLOG 455) builds the schema, validator checks, chips and the page with a two-path sample; then one content agent writes the full mapping.

## Data: `app/content/prep.json` (one file, not fields on lessons)

One central file, because firm facts go stale every cycle (one place to re-date), lesson ids never change, content agents keep their one-folder rule, and paths can point at levels not yet written.

```json
{
  "asOf": "2026-11-02",
  "paths": [
    {
      "id": "general",
      "name": "General interview prep",
      "kind": "general",
      "description": "One or two plain sentences.",
      "mocks": [],
      "steps": [
        { "ref": "mental", "priority": "must", "why": "One line, under 20 words." },
        { "ref": "puzzles/level-1", "priority": "must", "why": "..." },
        { "ref": "conditional/l3-...", "priority": "should", "why": "..." }
      ]
    },
    {
      "id": "oa-trader", "name": "OA prep: trader", "kind": "stage", "stage": "oa", "track": "trader",
      "mocks": ["mock-oa-arith", "mock-oa-trader", "mock-oa-sig"], "steps": []
    },
    {
      "id": "firm-optiver", "name": "Optiver", "kind": "firm", "track": "trader",
      "asOf": "2026-10", "source": "recruiting/l4-firm-by-firm", "reported": true,
      "mocks": ["mock-oa-arith"], "steps": []
    }
  ]
}
```

- `kind`: `general`, `stage` (with `stage`: `oa`, `interview` or `superday`, and `track`: `trader`, `research`, `strats` or `developer`) or `firm`.
- `ref`: a course id, `<course>/level-<n>`, or `<course>/<lesson-id>`. Steps are in study order; the page shows them in that order.
- `priority`: `must` or `should`.
- `mocks`: mock exam ids; ids not yet written are allowed and shown as "not yet written".
- Firm paths need `asOf`, `source` and `reported: true`; a step may carry `track` when one firm runs several roles.

## Engine (ENGINE-BACKLOG 455; engine agent; no content edits except creating `app/content/prep.json` with two sample paths)

- Loader in `js/content.js` (`ZQ.content.prep()`), with an inverse index lesson id to paths (a course or level ref expands to its lessons).
- Validator: every ref, mock id and track resolves (refs may name lessons listed in `course.json` but not yet written); `why` under 20 words, British spelling, no em-dashes; firm paths have `asOf`, `source`, `reported`; warning when a firm path's `asOf` is over 12 months old (as E19 proposes). Unknown fields are errors.
- Chips: at most one chip on a lesson card (`learn.js` card) and a course map node (`course.js`): "Interview prep" when the lesson is on any path. Its detail (lesson start screen or node detail) lists the stages and firms, for example "OA, superday. Optiver, SIG, Jane Street (reported, October 2026)". No chip clutter at 390 px.
- A "Prepare for" page (reached from Learn and from Review next to "Mock assessments"): pick general, a stage and track, or a firm; see ordered steps with done, in progress or not yet written, must or should, the `why` line, and links to its mocks. Firm paths show "Reported formats, as of <month year>" under the title. Path names join the Today search index.
- "Quant path only" keeps working; paths never unlock or gate anything.
- Document the schema in `docs/AUTHORING.md` (new section) and the item in `docs/ENGINE-BACKLOG.md`; playthrough covers the page under `--routes-only` and at `--mobile`; report to `docs/reports/engine-prep-tags.md`.

## Mapping (content agent, after the engine pass; edits only `app/content/prep.json`)

Read `recruiting/l4-firm-by-firm.json`, `docs/briefs/interview-gaps.md` and the mock table in `docs/briefs/interview-plan.md`. Prefer level refs; use lesson refs where one lesson in a level matters. Trader and researcher paths first and fullest (user decision); strats and developer paths may be short. The user's superdays are not with a named firm (2 Nov): write `general` and the stage paths first and in full, each ordered from foundations (Stage 0 and 1 courses) up to superday topics, so one path reads as a study route; firm paths come last and may be short. Seeds, to refine:

- general: mental, mental-pressure L1 to L2, counting-chance, conditional L1 to L2, random-vars L1 to L2, puzzles L1 to L2, recruiting.
- oa-trader: mental, mental-pressure, number-sense L3, ratio L1, series L1, puzzles L1 to L2, conditional L1 to L2, counting-chance L2.
- oa-research: py-found, ds, algo-think, graphs-dp, coding-int, numpy-pandas, sql, random-vars, limits-thm, estimation, regression, testing.
- oa-strats: py-found, ds, limits, integrals, vectors, eigen, random-vars, conditional.
- oa-developer: ds, algo-think, graphs-dp, coding-int, cpp, systems L1.
- interview-trader: puzzles, brainteasers, conditional, random-vars, markov L3 and L5, limits-thm L1 to L3, mm-games L1 to L2, game-theory L1, options L1 to L2, micro L1.
- interview-research: puzzles L1 to L3, conditional, random-vars, limits-thm, estimation, regression, testing, least-squares, eigen, stat-learning, validation, ensembles, research-int L1 to L2, coding-int.
- interview-strats: options, trees, ito, markov L5, random-vars, cpp L5, multivar L3, taylor.
- interview-developer: coding-int, ds, graphs-dp, cpp L5, systems.
- superday-trader: mm-games, game-theory, puzzles L4 to L5, mental-pressure L3 to L4, micro L3, recruiting L3.
- superday-research: research-int L3 to L4, coding-int L4, stat-learning, validation, alpha (a project to talk about), recruiting L3.
- superday-strats: trees L4, ito L4, options L3, cpp L5, puzzles L5.
- superday-developer: systems, coding-int L3 to L4, cpp L4 to L5.
- Firms, one path each, from l4's ten rows: Optiver, Jane Street, SIG, IMC, Citadel Securities, Two Sigma, Citadel, JP Morgan, Goldman Sachs, Morgan Stanley. Steps follow each firm's reported OA, interview and superday content; mocks from the plan's "Models" column.

Acceptance (from `app/`): `node tools/validate.mjs 2>&1 | tail -5` 0 errors; `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>` and `--mobile` pass; chips and the page checked in screenshots at 390 px.
