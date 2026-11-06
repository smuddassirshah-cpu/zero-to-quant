# Concept audit (user priority, 6 Nov 2026: learning only what is correct comes first)

Every level, review set, homework set and exam gets a concept audit by a Fable reader (model `fable`) who has not seen that level's earlier reviews. Courses already read in earlier sessions are audited now by a parallel session on branch `claude/fable-audit` (user, 6 Nov; prompt `docs/briefs/fable-audit-session-prompt.md`). Courses still in Phase 2 are audited after all content is finished. It checks meaning, not arithmetic: definitions, methods, conventions and claims. The number scripts already cover arithmetic.

## Auditor brief (binding)

Scope: one course, up to three levels (or one exam). Output `docs/reviews/audit-<course>-<levels>.md`, claim ledger `docs/reports/audit-<course>-<levels>-ledger.md`, and simulation script `docs/reports/<course>-L<n>-concepts.py` where any claim is empirical.

1. Blind first. Do not open `docs/reviews/review-<course>*.md` or the author reports until your ledger and findings are written. Then read them and fill the overlap table (step 7).
2. Ledger: one row for every definition, theorem or result, method step, convention, "always / never / every / only" claim, interpretation of a statistic or test, causal claim, code-behaviour claim, and the reasoning in each `explain`, `why`, hint and feedback line. Columns: file, JSON path, claim (short), verdict, basis.
3. Verdicts: `correct`, `wrong` (false as stated), `imprecise` (true only under an unstated hypothesis or convention a learner would carry away wrongly), `misleading` (true but teaches a wrong habit or intuition), `unverified` (you could not establish it; never leave this as a pass).
4. Basis for every row: a named standard source with chapter or section (for example Hamilton, *Time Series Analysis*; Tsay, *Analysis of Financial Time Series*; MacKinnon (2010) critical values; Hull, *Options, Futures and Other Derivatives*; Casella and Berger; Shreve; Rudin; Axler), a short derivation, or a simulation. Every empirical or statistical claim ("longer samples fit better", "this test rejects about 5%", "the estimate is biased towards zero") gets a Monte Carlo check in the concepts script, with enough replications to separate the claim from its negation. The script exits 0 on correct content; a check that fails because the content is wrong stays failing and becomes a finding.
5. Also check: hypotheses a learner would drop (a result stated without the condition that makes it true); conventions stated or implied (simple or log returns, 252 or 365 days, population or sample variance, one- or two-sided tests, sign conventions) and whether they match the standard practitioner and interview usage, said once where they first matter; graded keys that are right only under one convention the item does not state; `wrong[]` options or slip values that are in fact correct under a valid alternative method; explanations that reach the right number by wrong reasoning; finite-sample versus asymptotic statements; code that passes its tests but teaches a wrong method (for example look-ahead, in-sample tuning, a biased estimator presented as the standard one).
6. Findings in the review pattern (`N. file | JSON path | severity | problem | evidence and basis | exact fix`), severities `wrong`, `imprecise`, `misleading`. Each fix is exact paste-ready text with its basis. Where a correct fix needs more than a sentence (a method taught wrongly across screens), say so and propose the screens to rewrite.
7. Overlap table, after reading the earlier review: count of conceptual findings found by you only, by the earlier review only, and by both. This measures the miss rate of a single read.
8. Run the validator, the course's number scripts and the playthrough tails as the reader brief does; state results.

Hand back at most six lines: audit path, ledger rows and verdict counts, findings by severity, overlap counts, scripts and exit codes, inbox bullets.

## Fix pass for an audit (Opus, not Sonnet)

Concept fixes are applied by an Opus fixer, because applying a conceptual correction needs the same judgement as finding it. For every finding the fixer writes, in `## Fix pass`, the status and its own one-line basis (source or derivation, independent of the auditor's). If it cannot establish the fix independently it marks the finding `disputed: unverified` and does not apply it; the orchestrator sends disputed findings to a third Opus reader. The concepts and number scripts exit 0 afterwards; voice gate 35; validator 0 errors; playthrough of changed files desktop and mobile.

## Convergence rule

A course is closed only when an audit finds at most one new `wrong` per three levels that no earlier read found. Otherwise, after its fix pass merges, the course gets another blind audit by a fresh reader. The overlap counts per course are recorded in `docs/reports/concept-audit-log.md` (course, levels, audit round, wrong / imprecise / misleading, overlap counts, closed yes or no).

## Order (starts once all content is finished)

1. Interview courses and Stages 2 and 3.
2. Stage 1, then Stage 0.
3. Performance tasks, drill packs and bank items, with the courses they draw on.
4. Topic, stage and mock exams, after their courses close.

## Limits (stated plainly)

Two independent model reads and a convergence rule reduce errors and measure what is left; they do not prove zero. Author, reader and auditor are the same model family, so shared misconceptions can survive. A human expert read of the interview-critical courses (human-owned, like the pilot) is the strongest check available and is recommended before relying on them for interviews.
