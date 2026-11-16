# Engine backlog inbox

Content agents append their engine and canvas limitations here, under `Raised later (<course> level <n>):`, as bullets. An integration pass numbers them into `ENGINE-BACKLOG.md` and clears this file.

Cleared by engine pass AE part 1 (items up to 1051 in `ENGINE-BACKLOG.md`); the previous text is in commit 3e95964.

Raised later (problems validation):
- A `wrong[]` entry above 1 on a `unit: "%"` numeric draws the over-100 warning meant for the key (validator item 515). A slip such as typing the ratio 1.2 as "120%" for a 20% rise cannot be routed without `"over100": true`, which also silences the check on the key. Suggest: apply the over-100 warning to `answer` only, or give a `wrong` entry its own flag. (problems-2 dropped the slip.)
- `fresh-check.mjs`'s shared-formula advisory compares the displayed text, so an equivalent rewrite escapes it: problems-3 first stated the sign-agreement rule as $\tfrac12 + \arcsin(\rho)/\pi$ (homework-3's form, flagged) and now states $1 - \arccos(\rho)/\pi$ (not flagged). Suggest: normalise a few standard identities, or compare formulas by value at seeded points as the expression grader does.
Raised later (problems ensembles):
- `tools/fresh-check.mjs --file` on a problem set lists as advisory a shared displayed formula even when it is the course's own standard formula ($p = 1/(1 + e^{-F})$, $\sqrt{b(1 - b)/n}$, the Newton leaf step). To reach 0 advisories an author must say the formula in words in the stem. Suggest an allowlist of each course's taught formulas (or skipping formulas that occur in a lesson's `tex` screen), so the advisory keeps its signal for copied setups.
