# Review rounds of the stage 2 plan edits (#16)

This digest records every review round of smuddassirshah-cpu/zero-to-quant#16, which carried the S1 results into `docs/PLAN.md` and the appendices, and of the fresh gate review that followed its merge. The raw outputs were workflow results kept outside the repository, so this file is the record (the gate review's non-blocking item 11). "Decision" names the main session's decisions for that round; B, D and W numbers are `docs/DECISIONS.md` entries. Round 1's finding ids are the reviewer's lens and position: E (evidence), C (consistency), P (protocol).

| Round | Reviewed by | Findings | Major or blocking | Minor or non-blocking | Nit |
|---|---|---|---|---|---|
| 1 | 3 reviewers of the docs diff | 61 | 8 | 28 | 25 |
| 2 | round 1's 2 verifiers | 34 | 1 | 11 | 22 |
| 3 | round 2's 2 verifiers | 23 | 0 | 6 | 17 |
| 3, verification | round 3's 2 verifiers | 22 | 0 | 7 | 15 |
| Gate | 3 Fable reviewers and a judge | 18 | 6 | 12 | 0 |
| Gate 2 | 3 Fable reviewers and a judge | 15 | 3 | 12 | 0 |
| Gate 3 | 3 Fable reviewers and a judge | 12 | 0 | 12 | 0 |

**Commits.** 395e5a5: PLAN and the appendices, rounds 1 and 2. c616038: B22 to B32, W2 narrowed, STATE open questions 1 to 6 closed and 31 to 37 added. 7978398: B33, B34 and round 2's DECISIONS and STATE residuals. 95157e4: round 3's decisions in PLAN and the appendices. ad076f8: round 3's verification, settled by the main session. 2543174: the stage record. #16 was squash-merged into `stage/2` as b89f21e. 3fda12b: the gate revision's records (STATE, DECISIONS, spikes).

**Superseded later.** B28's "met by inference" (round 1) became "not met" at the gate. B27's emit rewrite (round 1; placed at stage 23 in round 2) became a render-time KaTeX macro at the gate. B29's contract 0.2.73 (round 2) became 0.2.74 at the gate. B34's dependency of stage 63 on 25 (round 3) was dropped at the gate for 11.1's rule. The handoff fragment check moved from stage 83 (round 1) to stage 82 (round 2, B30). ad076f8's `reserved.ts` lint exemption gave way to `@zq/contracts` at the gate.

## Round 1

Five drafting sessions (cdn, mathml, versioning, platform, caps) proposed the edits, and 115 were applied to six files. Three review sessions then read the uncommitted `docs/` diff on `stage2/s1-results` against the S1 run documents, the probe source, the npm mirror and the 0.2.73 type definitions: evidence (2 major, 10 minor, 8 nit), consistency (2 major, 11 minor, 8 nit) and protocol (4 major, 7 minor, 9 nit). Four fixer sessions, one each for ARCHITECTURE, PLAN, ASSESSMENT and the other appendices, applied the fixes under decisions M1 to M6 and the round's other decisions. Two verifiers then found 58 and 59 of the 61 fixed, 3 and 2 partly fixed and none unfixed.

The decisions: M1 scopes the reload to the page open in the foreground on the owner's iPhone. M2 says version scoping was not measured, so the item is met by inference (B28). M3 says `location.reload()` was measured only from the newest version. M4 proposes B27's sentinel `\textcolor` term targets, with the term list as the floor. M5 logs each new design (B22 to B26) and changes no AD figure. M6 rewrites ASSESSMENT 15.3's tag. The other decisions settle the iOS tag, `window.claude.hot`, the handoff fragment, `invalid_argument`, `zod/mini` (PLAN 12 row 15), 34 MB against 30 MB and the `sample` consent copy.

| Finding | Severity | Disposition |
|---|---|---|
| E1: ARCH 14 item 14 and the Reload button rest on `location.reload()`, measured only v2 to v2 | major | Fixed, M3: measured scope stated; from an older page [unverified], checked by stage 83's Self-test |
| E2, P2: "the host reloads every open page" generalises one foreground page | major | Fixed, M1: scoped everywhere; other views [sourced: `artifact.d.ts` 0.2.73]; backgrounded app, second device and desktop and web viewers [unverified]; risk 14 [unverified] |
| C1, P1: the version-scoping item is met by a sourced inference; deleting the emulator's stale-page setting breaks scenario 17 | major | Fixed, M1 and M2: unmeasured, "met by inference" (B28); fault injection "the host does not reload this page"; reload within 5 s by default. B28 reversed at the gate |
| C2: the `\htmlData` fallback leaves out composites that select terms inside a formula | major | Fixed, M4, in place of the reviewer's two candidates: B27 proposed for `live-formula` and seven composites, term list the floor. Mechanics revised at the gate |
| P3: new designs and later stages' definitions of done changed without DECISIONS or STATE entries | major | Fixed, M5: B22 to B28 written by the main session (c616038) and cited in the docs |
| P4: ASSESSMENT 15.3 keeps a stage 2 [unverified] tag that S1 closed | major | Fixed, M6 |
| E3, P6: `FileReader` read 64 bytes, not the 62,511-byte file | minor | Fixed in all four places |
| E4: decision 32 cites five `version.json` reads that cannot tell scoping from newest-version serving | minor | Fixed, M2 |
| E5: the 2.8 s cold load is credited to `zod/mini` alone | minor | Fixed: all the static imports; zod 9,393 of 9,646 ms of request time |
| E6: an identical republish and the staging re-send are tagged measured | minor | Fixed: [inferred] |
| E7: "the probe ran on 0.2.73" has no evidence | minor | Fixed: written against 0.2.73's types; the runtime version was not recorded |
| E8: iOS 27.2 tagged as an S1 measurement | minor | Fixed: [sourced: the owner, from Settings]; the user agent's `iPhone OS 18_7` [measured] |
| E9, C5: `invalid_argument` also covers malformed and over-limit writes | minor | Fixed: the access probe is a minimal, well-formed write; PLAN 8.1 and ASSESSMENT 13.8 rows split |
| E10: the cdnjs verdict rests on two guessed paths per package | minor | Fixed: 13 of 14 URLs failed to import, not on integrity; `lock.ts` checks every locked file |
| E11: ASSESSMENT 13.6's 30 MB against PLAN's 34 MB, settled silently | minor | Partly: 13.6 states the $2445/2148$ scaling and STATE logs it (c616038); a DECISIONS entry only at the gate (B37) |
| E12, C13, P9: W2 still calls import-map integrity unverified | minor | Main session: W2 narrowed to worker imports (c616038) |
| C3: closures claim more than S1 measured (reload, every open page, `version.json` caching) | minor | Fixed, M1 to M3; 14 item 12 "closed for loads; after a publish, unmeasured" |
| C4: the handoff link's 8 KB fragment was never tried | minor | Fixed: [unverified], checked at stage 83; moved to stage 82 in round 2 (B30) |
| C6: the `zod/mini` and classic zod closures breach 9.2's rows unannotated | minor | Fixed: both rows annotated, pending PLAN 12 row 15 |
| C7, P11: the `zod/mini` choice has no owner-decision row or recommendation | minor | Fixed: PLAN 12 row 15, default (a), recommendation (b); STATE open question 31 |
| C8, P7: the `sessionStorage` mirror is missing from the contracts and PLAN 7.5 | minor | Partly: `DraftStore.mirror`, the 5.9 row, PLAN 7.5, ASSESSMENT 3.4 and 13.4 (B22); no stage built the homework and paper mirror until round 2 |
| C9: the back-gesture fallback is not in stage 74a's definition of done | minor | Fixed: B23 in 74a; `zq/no-forbidden-apis` refuses `history.back` and `history.go` |
| C10, P10: risk 2 reads as if S1 had not run | minor | Fixed: closed by S1, with what failed and what was not measured |
| C11: a reloaded paper may wait 60 s for its own lease | minor | Fixed: B26, the holder is the device and tab identity |
| C12: the kept `sample` grant undercuts "reload to be asked again" | minor | Fixed: [unverified]; copy conditional on `permissions.state('sample')`; decline check at stage 63 |
| P5: [measured] on the `TexSlots` binding hides B20's annotation rewrite | minor | Fixed: the tag names B20 |
| P8: `window.claude.hot` cites a brief that is not in the repository | minor | Fixed: [sourced: the page-design guidance], quoted in DECISIONS section 4 |
| E13 to E20: 983 MiB; zero sizes for CDN files only; "a non-empty name"; "every own file S1 fetched"; `meta/release` timing a cross-clock hint; the reload delay from two samples; the 440 by 820 frame; the 6.3.3 citation | 8 nit | Fixed |
| C14 to C20: 254 entries plus the page; PLAN 6.4's file picker; cdnjs "load error", not "timed out"; `dist/signals.mjs`; a tag form; E0 names both failures; zod's share inferred | 7 nit | Fixed |
| P12 to P19: 0.2.73 untagged; tag forms; iOS tag and "the gate below"; "spike S1" in the sink entry; a comma splice; the synthetic id; `downloads` [inferred]; section 14's columns | 8 nit | Fixed; tag forms partly (PLAN's stayed undated until round 2) |
| C21, P20: STATE open questions 1 to 6; DECISIONS section 4's figures | 2 nit | Main session (c616038) |

The fixers also raised, outside the findings: KaTeX's `strict: 'error'` refuses `\htmlData` (B33, round 3); 9.2's KaTeX row against `katex.mjs` and the Preact figure (round 2 decision 4); stage 12's device check cannot run before stage 25 (round 2 decision 7); "Use here" against `steal: true` (B31); the 0.2.69 contract lines (B29). Left as written: a paper's pause budget for host reloads, the authoring syntax of term anchors (stage 6 or 12), AI-TUTOR decision 22's "in this view" (stage 63) and 2.13's `images` (P1).

## Round 2

The input was round 1's verification: evidence-and-findings (3 minor, 14 nit) and consistency-and-protocol (1 major, 8 minor, 8 nit). Four fixer sessions applied round 2's decisions 1 to 13. The main session fixed DECISIONS and STATE in c616038, and the docs of rounds 1 and 2 went in as 395e5a5. Two verifiers then found 33 of 34 fixed and 1 partly (STATE open question 31 lacked the CI rule), and 32 fixed and 2 partly (no stage that builds retention tested the second injection; CONTENT-FORMAT 6.9 still refused term anchors).

| Finding | Severity | Disposition |
|---|---|---|
| ARCH 1853: the emulator models only version-scoped serving, so the lazy-chunk row and the retained version cannot be tested | major | Fixed, decision 1: second injection "this page's own-file fetches reach the newest version" (B25); its tests placed at stage 83 in round 3 |
| DECISIONS 169: fflate's cdnjs paths "not reached" (both verifiers) | 2 minor | Main session (c616038) |
| DECISIONS 174: the term-list fallback "applies" (minor here, a nit from the other verifier) | minor | Main session (c616038): B27 proposed, term list the floor |
| ASSESSMENT 1523, ARCH 1617: no stage builds the homework and paper mirror or the lease key | 2 minor | Fixed, decision 2: stage 69's definition of done; ASSESSMENT 16 and 19 |
| ARCH 1852: the emulator targets "the contract the live Artifact is pinned to" [sourced] | minor | Fixed, decision 8: 0.2.73 (B29); 0.2.74 at the gate |
| ARCH 1619: the plan's page field cannot describe garbage-collection and maintenance publishes | minor | Fixed, decision 9: roles `previous`, `new` and `maintenance` |
| PLAN 962: no stage builds B27's rewrite or its colour check | minor | Fixed, decision 3: check at stage 7, rewrite at 23, binding at 12; default the term list. The rewrite was removed at the gate |
| ARCH 2127: B27's sentinels survive in KaTeX's TeX annotation | minor | Fixed, decision 3: restored or dropped under B20's rule. At the gate the macro keeps the authored TeX |
| PLAN 1107: decision 15 is silent on the entry budget | minor | Fixed, decision 4: `budgets.ts` reports the CDN part without failing until row 15 is decided; KaTeX row annotated. The rule after the decision is left to the owner |
| ARCH 2090: E2, E4 and E7 lag PLAN stages 4, 10a and 74a | minor | Fixed |
| Scope, timing and units: the full unmeasured list; "about 4 s and 1 to 2 s"; KiB; 894 px on the reloaded loads; two two-batch generalisations; the FileSaver row; $2445/2148$ in LaTeX; PLAN 707's wording | 9 nit | Fixed, decision 12 |
| PLAN's size tags undated (both verifiers) | 2 nit | Fixed, decision 12; restated in round 3 |
| "Stage 12's iPhone gate" against PLAN 11.1 (both verifiers) | 2 nit | Fixed, decision 7: taken in stage 25's preview Artifact |
| PLAN 1051: stage 83 has no web build to receive the fragment | nit | Fixed, decision 6: stage 82's handoff check (B30) |
| PLAN 1107: stage 25 does not carry option (b)'s measurement | nit | Fixed, decision 5 |
| CONTENT-FORMAT 1267: `trust: false` against conflict 10 | nit | Fixed, decision 11 (B32); it exposed the strict problem settled in round 3 |
| DECISIONS and STATE residuals: real-time delivery (both verifiers, one adding B27's composite list), the `hot` quote, STATE open question 5, the 34 MB deviation | 5 nit | Main session (c616038); the 34 MB entry at the gate (B37) |

The fixers left five items for round 3: the two sources for "0.2.74 exists" (decision 9), the "gzip -9" tag (decision 8), ARCH 5.4's untagged sentence (decision 14), the KaTeX strict contradiction (decision 1) and row 15's missing KaTeX recommendation (decision 7). Decision 17's "content first under the live page" was kept as correct, and PLAN 13's "60 MB" as history.

## Round 3

The input was round 2's verification: evidence-and-findings (2 minor, 8 nit) and consistency-and-protocol (4 minor, 9 nit). The main session logged B33 and B34 and fixed DECISIONS and STATE in 7978398. Three fixer sessions (PLAN; ARCHITECTURE; CONTENT-FORMAT, WIDGETS, ASSESSMENT and AI-TUTOR) applied round 3's decisions 1 to 15 in 57 recorded changes (95157e4). Two verifiers re-ran the KaTeX 0.19.0 claims in Node against `spikes/s1/npm` and reproduced every size with zlib level 9 through Python. All 15 decisions were in every place they name.

| Finding | Severity | Disposition |
|---|---|---|
| CONTENT-FORMAT 1267: `strict: 'error'` refuses `\htmlData` before `trust`, so every term anchor throws (both verifiers) | 2 minor | Fixed, decision 1 (B33): a strict function that ignores only `htmlExtension`; `errorColor` `#0a0100` reserved and checked; stage 7 fixtures |
| ARCH 1893: the data worker's breach has no CI rule, and the three breaches are handled unevenly (both verifiers) | 2 minor | Fixed, decision 6: one rule for the entry, data worker and KaTeX (B36 at the gate) |
| ARCH 1843: the retained version is tested at stage 4, which has no retention | minor | Fixed, decision 10: both injections on one page, at stage 83, scenario 17 and E10 |
| PLAN 1030: stage 63's iPhone check is unlogged, and 63 does not depend on 25 | minor | Fixed, decision 13 (B34): 63 depends on 25. Reverted at the gate |
| CONTENT-FORMAT 1267: a colour written without `#` escapes a text match | nit | Fixed, decision 2: the check reads KaTeX's output, without regard to case |
| ARCH 1853: the lazy-chunk tests need both injections on one page | nit | Fixed, decision 10 |
| PLAN 770: a maintenance release's last publish carries `new` (both verifiers) | 2 nit | Fixed, decision 11 |
| ARCH 2127: "if that check fails" has no antecedent | nit | Fixed, decision 5 |
| ARCH 2116 and 105: item 9 untagged; decision 32 tagged [sourced] where B28 says [inferred] | 2 nit | Fixed, decision 14 |
| PLAN 327 and 1107: size tags dated 7 October and not reproducible with `gzip -9` | 2 nit | Fixed, decision 8: "zlib level 9, 8 October 2026" |
| ARCH 1852, DECISIONS 466: two sources for "0.2.74 exists" | 2 nit | Fixed, decision 9; B29 cites both (7978398) |
| PLAN 1107: row 15 recommends nothing for KaTeX | nit | Fixed, decision 7: `katex.min.js`, 75,906 bytes |
| PLAN 975: stage 25's preview has the binding off, so nothing to tap | nit | Fixed, decision 4: a build switch, on in stage 25's preview build |
| PLAN 681: the lazy-chunk row omits the unmeasured condition | nit | Fixed, decision 12; its wording corrected in ad076f8 |
| STATE 241 and 192, DECISIONS 414: open question 31's CI rule; lagging deviation columns; untagged lines | 3 nit | Main session (7978398) |

### Round 3's verification, settled in ad076f8

Two verifiers (decisions and evidence; consistency, citations and writing) raised 7 minor and 15 nit findings. The main session settled them in ad076f8 without another fixer round.

| Finding | Severity | Disposition |
|---|---|---|
| PLAN 681: a page left behind fails only once a further release removes the retained version | minor | Fixed |
| STATE 98: the stage 63 row lacks 25 (both verifiers) | 2 minor | Fixed, then reverted with B34 at the gate; STATE's row itself was reverted only at the second gate revision |
| DECISIONS 434: B25 pairs the tests with the second injection alone (minor here, a nit from the other verifier) | minor | Fixed |
| ARCH 1363: reserved colour literals in `src/` against `zq/no-colour-literals` | minor | Fixed by an exemption for `src/engine/render/reserved.ts`; at the gate the colours moved to `@zq/contracts` and the exemption went |
| ARCH 1360: `TexService.html` cannot ask for the untrusted configuration | minor | Fixed: a `source` argument, `authored` or `untrusted` |
| STATE 248: B20's timing differs between STATE and DECISIONS | minor | Fixed: B20 before stage 12; B27 as open question 38, with stage 25's result |
| CONTENT-FORMAT 1509: the 8.1 row says off until adopted, against stage 25's preview (both verifiers) | 2 nit | Fixed; the row deleted at the gate |
| PLAN 952: stage 4 appears to own the lazy-chunk injection test (both verifiers) | 2 nit | Fixed: both tests at stage 83 |
| ARCH 2131, PLAN 554, CONTENT-FORMAT 1267: "on the authored source" against reading the output; "in either case" | 3 nit | Fixed |
| ARCH 2027: the build switch is missing from both flag lists | nit | Fixed: `artifact.termBinding` |
| PLAN 327: Node's bundled zlib gives other figures | nit | Fixed: tags name Python's zlib 1.3, and 9.2 gained a Node note; its "within 0.1%" was wrong (gate blocking item 5) |
| STATE 249, PLAN 327: open question 36 untagged; counts tagged differently in PLAN and ARCH | 2 nit | Fixed |
| PLAN 639, PLAN 85, AI-TUTOR 1813: the threat row implies model output under the strict function; two pronouns lost their antecedents; T4 overstates hard rule 2 | 3 nit | Fixed |

## Gate review

After #16 merged with no review on the pull request, a fresh-context review on the Fable model judged the stage (D9). Three reviewers took one lens each: definition of done and evidence (2 blocking, 5 non-blocking); protocol and security (1 blocking, 7 non-blocking); and quality of the plan edits, read as the engineer of stages 4, 7, 12, 23, 25, 63, 69, 74a, 82 and 83 (3 blocking, 5 non-blocking). They re-derived the verdicts from the run documents, re-ran the KaTeX claims and the byte figures, and found CI green, 497 tests passing and no viewer data in the committed runs. The judge's verdict was "revise". It kept all 6 blocking findings, merged the 17 non-blocking ones into 12, listed 11 owner decisions and rejected 2 sub-claims. Items marked "fixed in the gate revision" are covered by the gate revision's decisions 1 to 9, which edit PLAN and the appendices on `stage2/gate-fixes`. The main session's records are in 3fda12b.

| Item | Severity | Disposition |
|---|---|---|
| Two S1 checks failed, a gating rule 10 stop for the owner, yet STATE hands the gate to the reviewer's verdict | blocking | Main session (STATE, DECISIONS D9): the stop is named; the owner clears it by accepting B23 and the term-list default |
| The version-scoping item is not met, and PLAN's own Done-when column was edited to say "met by inference" | blocking | Fixed in the gate revision (decision 2: the parenthetical reverted, "not met" wherever "met by inference" stood); main session: B28 and STATE, with a waiver recommended or a polling probe |
| D9 carries the base-branch departure as if the owner had decided it | blocking | Main session (DECISIONS/STATE): B35 and its Decisions row |
| B27's emit rewrite breaks ARCH 4.5's layering and makes content hashes differ per target | blocking | Fixed in the gate revision (decision 1): a render-time `\htmlData` macro under `artifact.termBinding`, reserved colours in `@zq/contracts`, the emit rewrite and the lint exemption deleted; the annotation keeps the authored TeX, so B20 covers only slot sentinels |
| ARCH 9.2 claims Node's gzip is within 0.1% of Python's | blocking | Fixed in the gate revision (decision 3): within 0.6% on the small files and 0.05% on the three breaching files; `budgets.ts`'s Node figures are the gate |
| `spikes/README.md` says the S1 results are pending | blocking | Main session (spikes): its S1 section gives the outcome |
| A seventh page load, `muyq3ed6`, is missing from the record | non-blocking | Main session (spikes): run document committed, `README.md` and `s1-latest.json` updated |
| DECISIONS understates the `db` latency | non-blocking | Main session (DECISIONS): reads and deletes 170 to 300 ms, writes 200 to 570 ms |
| Five display formulas overflow the 377 px line box | non-blocking | Fixed in the gate revision (decision 4: ARCH 5.11, a wide formula scrolls in its own container, never clipped or scaled); main session: DECISIONS section 4 |
| The force push without asking has no Decisions row | non-blocking | Main session (DECISIONS/STATE): B38; both backup branches on the owner's deletion list |
| The budget relaxation has no B entry and no owning stage | non-blocking | Fixed in the gate revision (decision 5: stage 4's deliverable and test); main session: B36 |
| The 34 MB reconciliation has no DECISIONS entry | non-blocking | Main session (DECISIONS): B37 |
| D9's two rules of the build's own making are untagged | non-blocking | Main session (DECISIONS): tagged [our choice], for the owner to confirm |
| B34 makes stage 63 wait on stage 25 | non-blocking | Fixed in the gate revision (decision 6): 63 depends on 60 to 62; 11.1 states the rule once; B34 revised |
| 0.2.73 and 0.2.74 differ only in `user.d.ts`'s `"people.add"` | non-blocking | Fixed in the gate revision (decision 7): emulator on 0.2.74; B29 revised; S1's facts stay tagged 0.2.73 |
| Step 4 re-sends the previous page without reading it | non-blocking | Fixed in the gate revision (decision 8): a `path` read, its SHA-256 checked against the previous ledger, a mismatch is the drift stop |
| The review rounds exist only as a sentence | non-blocking | Main session (spikes): this file |
| STATE's "Last updated" is stale | non-blocking | Main session (STATE) |
| Reviewer 3: the compiler must import `src/app/config.ts` to read the switch | sub-claim | Refuted by the judge: a flag can reach the compiler without an import; the finding stood on its other two legs |
| Reviewer 1: a poll from page load would take 10 or more readings | sub-claim | Refuted by the judge: the window was at most 4 s at 125 to 234 ms a fetch, so a handful; the finding stood |

The judge's 11 owner decisions: the rule 10 stop, B28's waiver or measurement, B35, D9's two clauses, B27 and B20, B21, B22 with B24 and B26, row 15, B31 and B32, the deletions with B38, and open questions 15 and 37. The stage 2 record in STATE carries the first ten under "For the owner"; the last two stay among STATE's open questions.

## Second gate review (fresh Fable, after #17)

Three Fable reviewers and a judge read `stage/2` at 54cfb68 on 8 October 2026; the first attempt stopped at a session limit and was run again. Verdict "revise": 3 blocking, 12 non-blocking, no refuted blocking finding. Everything below was fixed in the second gate revision (smuddassirshah-cpu/zero-to-quant#19, from `stage2/gate-fixes-2`), except the `stage/3` item, which is smuddassirshah-cpu/zero-to-quant#20, merged into `stage/3` at 11:50 UTC.

| Finding | Severity | Disposition |
|---|---|---|
| STATE's stage 63 row still depends on 25; this digest called it fixed | blocking | STATE row reverted to 60, 61, 62; the row above corrected |
| STATE's Next action says stage 3 runs from `stage/1`; `stage/3` was cut from `stage/2` before an approving verdict | blocking | Next action states the fact; B39 and the early start in the record's Deviations and "For the owner"; B39's condition on `stage/3` corrected by #20 (merged 11:50 UTC) |
| PLAN 10 says `@zq/contracts` is "types only" while 6.5 puts a runtime module there | blocking | PLAN 10's tree line names the KaTeX module; B27's Deviation and the record name the tree change, for the owner |
| DECISIONS gives the S1 window as ending 23:07 | non-blocking | 22:19 to 23:13 UTC, the size probe 22:39 to 23:07 |
| B25 names contract 0.2.73 | non-blocking | 0.2.74 (B29, revised) |
| STATE's B27 row names stage 23; PLAN 11.1's iPhone list lacks 9a and 12 | non-blocking | Stages 7, 12 and 25; 9a and 12 added |
| The record says open question 6 closed, omits B20, cites CI on #16 only | non-blocking | Corrected |
| The results README overstates muyocrk9's tapped checks and leaves the dark screenshot's run open | non-blocking | 11 of 13 tapped; `muyo87q6` from its 36 ms check |
| #17 merged without a review of its own diff | non-blocking | B41; every pull request since gets one |
| The stage's effort was not re-measured | non-blocking | Re-measured to the start of stage 3 and through both gate reviews (STATE) |
| `zq check` cannot import the authored KaTeX configuration; no stage builds `TexService` before stage 12 needs `TexSlots` | non-blocking | B42: `katexOptions` in `@zq/contracts`' KaTeX module; stage 12 builds `TexService`, `Tex` and `TexSlots`; stage 23 builds `Prose` on them |
| B27's $k$ is unspecified | non-blocking | $k$ is the term's index in `terms(src)`, distinct term ids in order of first appearance; more than 256 is a `zq check` error; "until stage 23's Artifact output exists" became "until stage 23's content bundles exist" |
| Row 15 sets no gate for after the decision | non-blocking | Row 15 states the gate each option implies; B36's report mode ends at the decision |
| Step 4's `path` read of the live page is assumed byte-identical | non-blocking | The previous page comes from the previous tag's rebuild, checked against the ledger; the read is a cross-check, [unverified], settled at stage 83 |
| `artifact.termBinding` would be on in every later preview | non-blocking | `zq preview --artifact --term-binding`, for stage 12's check only |

## Third gate review (fresh Fable, after #19)

Three Fable reviewers and a judge read `stage2/gate-fixes-2` at 9e11ab0 before its merge, so the review was also #19's own second-session review (recorded on #19). Verdict **"approved, continue"** as the quality pass: no blocking finding, 12 non-blocking. Stage 2 remains a gating-rule-10 stop for the owner. All 12 were fixed in the third gate revision, the pull request from `stage2/gate-fixes-3`.

| Finding | Disposition |
|---|---|
| No stage builds `@zq/contracts`' KaTeX module | Stage 3 builds it once the owner accepts its place (B42); stage 3's row, E1, E4 and E5 updated |
| "The same object" is wrong: KaTeX writes `\gdef` definitions into the `macros` it is given | A fresh options object with copied `macros` per call; `\gdef`, `\xdef` and `\global` are `zq check` errors |
| `terms(src)` misses anchors a shared macro expands to | A shared macro that expands to `\htmlData` is a `zq check` error, recorded in B42 |
| The effort line does not add up | 18.8 agent-hours, 3.1 AD |
| B35 says stage 3 was cut from `stage/1` | B35 says it was to be, and points to B39 |
| The stage 2 record is a revision behind | Second revision and #20 recorded; CI on #16, #17 and #19; B41 and B42; B20 in order |
| "With SRI" overstates the probe's hash checks | SRI on the import map and the UMD scripts; worker imports and cdnjs candidates unchecked (W2) |
| The `--term-binding` sentence breaks ARCH 6.5's bullet | Reordered; the flag is the build-time define `__TERM_BINDING__`, named in 11.4 |
| B41 cites #18, which shows no review | Corrected; reviews are now posted on their pull requests (#19, #20) |
| Who implements `DraftStore.mirror` | Stage 4 in the Artifact adapter and the fake, with a conformance test; stage 10a wires `commit` and owns the reload test |
| This digest's table and #20 attribution | Rows for gates 2 and 3; #20 named |
| STATE's Gate legend | The owner's reply or, under D9, the fresh reviewer's verdict; a rule 10 stop records the owner's reply |
