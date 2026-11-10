# Engine session Z

Items 852 to 858 of `docs/ENGINE-BACKLOG.md`; all seven addressed.

1. **Mobile overflow (852).** The course page's topic chip now wraps (`css/screens/course.css`). `--fluency --mobile` is green for `complex`, `odes`, `vector-calc` and `vectors`.
2. **Flake (853), not reproduced.** 60 same-seed plays (30 per set, alternating a failing and a clean first attempt) never differed. Ruled out: generation (no clock or `Math.random`, seeded from the route), widget kinds (numeric and expression only, so no option shuffle), KaTeX (synchronous script, no `<code>` fallback after load), item render (synchronous). Probably a load-dependent read of `innerText`; no code change, no retry added.
3. **merge-wave (854).** A `manifest.json` conflict takes ours; the validator step regenerates it. The test now adds a drill file per branch so the manifests collide: the old script fails that case, the new one passes.
4. **numbers_lib (855).** `Level` loads `problems-<n>.json` (ref `"problems"`); `check_wrongs` prints a count, lines with `--verbose`.
5. **Problem sets (856).** Done note: "Every problem was right first time."; result rows read "Problem n. <first sentence, about 60 characters>". Note: "Well done." is also in `js/screens/fluency.js` (left alone).
6. **Shots (858).** `--problems --shots` shoots every part at 440 px.
7. **Validator (857).** `[answer-form]` warning plus two test cases.

Docs: `docs/AUTHORING.md` section 5, `docs/LEVEL-BRIEF.md`, playthrough header.

## Validator pass (859, 860)
- 860: `[answer-form]` accepts "decimal", "places", "dp", "sf", "fraction", "nearest", "per cent", "%", "exact value", "in pounds" and similar. Warnings 137 to 1. Remaining: `counting-chance/problems-1.json` items[1].parts[4] (answer 4.75, "what is the fair price of one play, the average payout per play?"), a genuine lack. I read it plus ten sampled formerly-warned parts: each carries "Give a decimal [to N places]" or "the exact decimal".
- 859: index rows must match drill files on name, course, difficulty; unlisted non-sample file is an error. Real content fires nothing (no offenders).
- Tests: problems 42/42, drill-index 8/8, session, planted-check green; validator 0 errors.

- Closing fault 1 (test-merge-wave): the toy index rows carried name "Test <id>", difficulty 1, and the zz-a and zz-b drill files had no row, so rule 859 (row equals file; unlisted non-sample file) rightly fired. Fixed the fixtures in `app/tools/test-merge-wave.sh` (rows copied from the drill file, plus a row per zz drill); the rule and merge-wave.sh are unchanged.
- Closing fault 2 (`--fluency-all` "moved progress"): an artefact of the check, not an engine fault. The Review hub's `assignDue` creates a level's homework the first time it opens after the level's lessons are all done; the check's `go('review')` after the attempt opened it (same-hash navigations do not re-render, so it fired only on the first visit), and which set tripped it depended on the profile (quadratics l4, then the fixture). `playthrough.mjs` now leaves and re-enters Review before taking the baseline, and the failure message names the changed fields. Full run: 85 ok, All passed.
