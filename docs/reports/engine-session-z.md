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
