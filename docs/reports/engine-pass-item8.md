# Engine pass, item 8: independent capstone (backlog 564 to 569)

Built: `content/capstones.json` schema (optional file), validator rules in `tools/capstone-rules.mjs` with 17 scratch cases, `ZQ.content.readiness.status` and `verdict` (ready only with every required level met plus a complete external record), a read-only You "Capstone" card (learner's role first, 390 px safe), and the oa-drill rule in `perfPassed`. AUTHORING.md section 15 documents it.

Decisions:
- "Required levels" means every level of the courses the role marks `required` in `readiness.json`. Most roles have unwritten levels, so none can show ready today.
- Today showed no role verdict. The "N% ready, from your mastery map" lines (Today exam card, Review card and ring) are per-exam estimates, but the word "ready" invites a role reading, so they now say "Mastery map estimate: N%."
- One verified mapped oa drill is enough for the task. Drill level comes from an optional `level` field, else the course's lowest gated code level (coding-int L1). No content field is required today.

Tests: test-capstone 9 of 9, test-validate-capstone 17 of 17; test-met-rule 17, perf 33, versions 5, why 12 unchanged. Validator 0 errors; readiness-sums OK.

Playthrough `--routes-only` (desktop and `--mobile`): the new capstone check passes. The existing gating check fails in both modes on trader brainteasers L2 (`graphs-dp/L3` is still a hard edge in content; the DECISIONS lever turns it into a diagnostic, a content change). Not caused by this pass.

Main session: write the five empty records, regenerate `manifest.json`.
