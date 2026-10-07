# The probe's review before publishing (spike S1)

This review ran before the first publish. The findings are kept here so that `docs/DECISIONS.md` B18's "all fixed or answered" can be checked from the repository.

- **Findings:** 17 major, 34 minor and 15 nit, from three reviewers: cdn and platform, mathml and caps, and completeness.
- **Fix run:** 24 fixes, and 4 findings answered without a change (listed below).
- **Verification:** a third session re-verified the result. Its tests met 107 of 107 expectations.
- **Archive review:** a separate review of this archive produced commit 042d476.

<details><summary>All findings (severity, place, problem)</summary>

| Severity | Where | Problem |
|---|---|---|
| major | `probe/cdn.js:377` | cdn.integrity-enforced passes even when the wrong-hash URL fails for a reason other than integrity, as long as the control loads. The verdict never uses the Resource T... |
| major | `probe/cdn.js:591` | cdn.umd-fallback says 'the script with a wrong hash was refused' whenever the signals-core script fires onerror. The same URL is never loaded with its correct hash as ... |
| major | `probe/cdn.js:187` | cdn.bootstrap-map passes on any module with an h export, and cdn.static-import passes on any working Preact. Neither checks that 'preact' (or the other specifiers) res... |
| major | `probe/cdn.js:95` | readImportMap() reads document.querySelector('script[type="importmap"]'), which is the first import map in the document and not necessarily ours. If the host wrapper h... |
| major | `probe/harness.js:40` | REPUBLISH_TIMEOUT_MS is 60 s, but caps.meta-release waits up to 90 s after the signal (RELEASE_WAIT_MS in caps.js line 29). A delivery between 60 and 90 s, or no deliv... |
| minor | `probe/cdn.js:537` | The UMD check's 'what' claims to measure 'whether the named fallback works', but it never loads @preact/signals' UMD (or signals-core) with a correct hash and never re... |
| minor | `probe/harness.js:210` | connectDb uses useCapability, which resolves null after its own 10 s timer and then ignores a namespace that arrives later ('after the 10 s limit, ignored'). On a slow... |
| minor | `probe/harness.js:488` | Write-failure handling has three defects. state.writes.lastError is never cleared, so after one transient failure the header shows 'failing' and 'Last save failed ... ... |
| minor | `probe/harness.js:601` | Whenever 'at' parses, the republish signal counts as fresh only if Claude's clock time is later than the phone's page-start time. If the phone clock is ahead by more t... |
| minor | `tools/build.mjs:297` | The v2 republish described by manifest.republish has 304 entries: 101 added and 2 changed files plus 201 null removals. That is over the tool's 255 per publish if null... |
| nit | `tools/build.mjs:141` | The build takes each module's closure from cdn-lock.json's files list and never derives it again. A closure file left out of the lock would load with no integrity chec... |
| nit | `probe/harness.js:326` | normalise() never clips a summary, and fitDoc only shrinks data. A very long summary or lateResult summary could keep the document over its limit after every cut. The ... |
| nit | `probe/cdn.js:421` | In cdnjs-candidates, proven = loaded.filter(r => r.inMap !== false) counts a candidate whose map entry could not be read (inMap null) as proven byte-identical. |
| nit | `probe/harness.js:617` | The republish watch subscribes again only when the code is exactly 'unavailable'. db.d.ts says to treat unknown codes as unavailable, and queue_overflow is terminal fo... |
| nit | `tools/build.mjs:277` | The fragment checks (no html, head or body tags, no module script, title first) run on v1 and v2 only. dist/dbsize/index.html, which is published as its own Artifact, ... |
| nit | `tools/build.mjs:174` | If the host blocks the inline import map and bootstrap, the page shows 'The probe is loading.' forever and the owner has nothing to report. |
| nit | `probe/cdn.js:520` | The module-worker pass does not record that no integrity applies to the worker's CDN imports. A worker has no import map and import() takes no integrity, so classic zo... |
| major | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/caps.js:396` | caps.db-rules cannot tell whether the declared rule set is in effect. Every case gives the same outcome under the platform's default rules. db.d.ts says the owner meet... |
| major | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/caps.js:507` | caps.meta-release can pass on the initial snapshot. findFresh counts a s1-v2 delivery as fresh when parseAt(docAt) > MODULE_START, but those two times come from differ... |
| major | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/caps.js:746` | caps.sample-abort can pass without testing a mid-stream stop. The 2 s timer aborts before any text arrives whenever the consent dialog is up (if the owner taps this ch... |
| major | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/caps.js:604` | Model output is written to the db run document. The consent check stores data.text and puts the reply in its summary. The tiers check stores tiers[t].text. The tools c... |
| major | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/caps.js:243` | caps.user passes on a non-empty id alone, but PLAN stage 2 (d) asks for 'user (viewer id, profile)'. If the publish declares no `scopes: ['profile']`, or names are wit... |
| minor | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/mathml.js:220` | The clippedLeft evidence cannot detect left clipping in a display formula. It compares the <math> element's box with its scroll box. For display="block", the <math> bo... |
| minor | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/caps.js:29` | caps.meta-release waits up to 90 s from the moment the signal is seen (RELEASE_WAIT_MS, and its `what` text). The harness stops republish checks 60 s after they start ... |
| minor | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/caps.js:558` | A dead-bridge 'unavailable' on the meta/release watch gives a 'fail'. db.d.ts says such a listener is terminated and 'a fresh onSnapshot is the only recovery', and the... |
| minor | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/caps.js:688` | caps.sample-streaming records the onText guarantees it measures (deliveriesAfterResolve, textEqualsDeltasSoFar, lastTextEqualsResult) but passes on count >= 2 alone. A... |
| minor | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/caps.js:597` | caps.sample-consent cannot show that its own call was the one that asked. If the owner taps another sample check first, consent is already granted for the view and thi... |
| minor | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/mathml.js:340` | The TexSlots self-test only compares the binding with slotValues(5), the same function that produced the value. The comment at line 339 says 'k = 5 must show 5 and 0.9... |
| minor | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/mathml.js:301` | The probe tests a binding that goes beyond the documented one. ARCHITECTURE 5.11 and PLAN conflict 10 say only to swap each sentinel <mtext> for an <mn>. They say noth... |
| nit | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/mathml.js:579` | mathml.texslots-verdict asks the owner to move the slider, but does not record whether he did before answering the font question. kAtAnswer = 3 is ambiguous, because 3... |
| nit | `/tmp/claude-0/-home-user/3305760c-454b-5c39-abc8-c860c921c4c9/scratchpad/s1/probe/caps.js:617` | caps.sample-limits is kind 'consent', but sample.d.ts says limits() is 'Cheap and local: no usage is spent, the viewer is not prompted'. It only runs on a tap, so its ... |
| major | `probe/platform.js:852` | The version-scoping and version.json-after checks each take one reading as soon as ctx.republished resolves. They have no delayed re-read and no control showing that v... |
| major | `probe/platform.js:978` | The back-gesture check cannot record its likeliest failure. If the swipe leaves the artifact screen and the frame is unloaded, the check stops waiting for an answer. O... |
| minor | `probe/platform.js:510` | The hash-route check adds two history entries with `location.hash = target`. It then rewrites only the current entry with history.replaceState, so the frame's back sta... |
| minor | `probe/platform.js:838` | When versionAfter gets v1 from both fetches, it returns 'fail' with a summary saying the page 'reads its own version's files, not a browser cache'. That cause is asser... |
| minor | `probe/idb-worker.js:155` | The worker never reports whether it runs as a module. The file deliberately has no import or export, so a browser that ignored `{type: 'module'}` and ran it as a class... |
| minor | `dbsize/dbsize.js:383` | dbsize never checks snapshot.metadata.fromCache. (1) At load, a not-yet-definitive status read with exists: false makes the page show 'No earlier run is saved' and ena... |
| minor | `dbsize/dbsize.js:133` | fromSaved accepts any maxDocs from 1 to 9994, and any pauseMs, basePauseMs or cleanPauseMs from 0 to 64,000. The saved status is db data, and the file treats it as unt... |
| minor | `dbsize/dbsize.js:255` | A run of resource_exhausted refusals is retried without limit at a 64 s pause. If the store keeps refusing, which is plausible when a budget rather than a cap is hit, ... |
| minor | `probe/platform.js:297` | When encodedBodySize equals decodedBodySize and no Content-Encoding header is visible, the compression check returns 'fail'. On a CORS response (a frame with an opaque... |
| minor | `probe/platform.js:646` | The external-link check returns 'fail' ('Tapping the link did nothing') when the owner answers 'Nothing happened', even if no click reached the link. A tap on a link f... |
| minor | `probe/platform.js:904` | The reload marker goes into the URL hash only when the sessionStorage write throws. If the write succeeds but the storage does not survive the reload, resume finds no ... |
| minor | `probe/platform.js:329` | The Web Locks check tests contention only inside one agent: an inner ifAvailable request in the same document, and steal against its own lock. Decision 26 depends on t... |
| nit | `dbsize/dbsize.js:10` | The decision note says the base-36 pad means 'no layer can compress it much'. In fact gzip and brotli shrink a body to about 66%. If the store counted compressed bytes... |
| nit | `dbsize/dbsize.js:555` | PLAN.md item (d) says the probe 'records success or the cap it reached, then deletes its documents'. Here clean-up waits for the owner to tap Clean up after 'done' or ... |
| nit | `dbsize/dbsize.js:66` | withTimeout gives up after 90 s but does not cancel the call. Resume, enabled at once in the 'error' state, can then send a second set() to the same document while the... |
| nit | `probe/platform.js:234` | idbVerdict fails 'IndexedDB in a worker' when indexedDB.databases() still lists the database right after deleteDatabase succeeds. That is a cleanup property, not the o... |
| major | `probe/caps.js:396` | The PLAN asks S1 to check the db rule set, but caps.db-rules cannot see any declared rule. It runs only as the owner, and 'rules never limit the owner; only {self} pri... |
| major | `probe/cdn.js:591` | The wrong-hash classic script has no control. The bad load uses the signals-core UMD URL, and no check ever loads that URL with its correct hash. A 404, a jsDelivr fau... |
| major | `probe/mathml.js:593` | ARCHITECTURE 14 item 20 names S1 to close whether `\htmlData` term anchors survive KaTeX's MathML output. No check in the probe, test.mjs or katex-html.mjs does this, ... |
| major | `CONTRACT.md:108` | Several results depend on what Claude does outside the page, and none of it is written down in s1/. Four steps go wrong without it. (1) The v2 publish uses file_path d... |
| major | `probe/cdn.js:377` | cdn.integrity-enforced passes on any rejection of the one wrong-hash import while the control loads. In WebKit a failed integrity check and a network failure give the ... |
| minor | `probe/harness.js:40` | The harness gives republish checks 60 s (REPUBLISH_TIMEOUT_MS), but caps.meta-release waits up to 90 s from the signal (RELEASE_WAIT_MS). It also queues behind version... |
| minor | `tools/build.mjs:32` | PLAN (a) asks for Preact 11.0.0, @preact/signals and zod/mini from cdnjs where it hosts the identical file. The cdnjs candidates cover only preact, preact/hooks, katex... |
| minor | `probe/mathml.js:34` | PLAN (b) compares the slot digits in the swapped <mn> 'against the surrounding maths font AND against the sentinel's own <mtext>'. texslots-verdict asks only about the... |
| minor | `probe/mathml.js:528` | The Done when asks for 'the MathML verdict recorded with screenshots'. The page cannot take screenshots and does not ask the owner for any. compare/mathml-chromium.png... |
| minor | `probe/harness.js:1025` | The Done when requires 'device, app version and date'. The run document records the UA, viewport, typed app version and startedAt, but not the device model: an iOS UA ... |
| minor | `probe/caps.js:587` | caps.sample-consent passes whenever the first quick-tier call resolves, so it never shows that a consent dialog appeared. If sample was already granted, the pass is me... |
| minor | `probe/caps.js:246` | PLAN (d) lists user 'viewer id, profile', but caps.user passes on the id alone. Empty names in me() and profiles() still give a pass, for example when the profile scop... |
| minor | `probe/platform.js:838` | When both the default-cache and the no-store fetch of version.json say v1, the summary says 'this open page reads its own version's files, not a browser cache'. A host... |
| minor | `probe/platform.js:853` | On the reloaded v2 page, version-scoping returns skipped. So no on-device reading confirms that the null removals took effect for a fresh load (b-001 and v1-only gone,... |
| minor | `probe/harness.js:932` | PLAN 8.1's fallback for a handoff link that cannot leave the frame is a copyable link, and its fallback for a refused clipboard write is selected text. Copy results ex... |
| minor | `tools/build.mjs:182` | The Artifact tool requires the publishing session to read in full every file it did not write. Builder subagents wrote these files, and the build generated them. v1 an... |
| minor | `probe/harness.js:891` | After the republish checks finish, the panel tells the owner only to say 'S1 republish checks done'. It does not route him to platform.reload, which must run last and ... |
| nit | `probe/cdn.js:187` | cdn.bootstrap-map passes when a module exporting h arrives, without checking that 'preact' resolved to the locked jsDelivr URL. moduleResolvesPreact and lockUrl are bo... |
| nit | `probe/cdn-worker.js:97` | The worker loads each library with a dynamic import(url). ARCHITECTURE 6.2.7 item 4 builds the data worker with static imports rewritten to full URLs. Both are module-... |

</details>

**Answered without a change:**

- Completeness major (caps.js 396), the part asking for a board/zz-not-me case that expects invalid_argument: under the declared rule set this case reads wrong. ARCHITECTURE 6.2.4 declares a 'board' prefix rule (read interact, write owner). db.d.ts says a rule at the prefix opens siblings' subtrees at its levels, and the owner meets 'owner'. So the owner's write to board/zz-not-me succeeds with o...
- mathml.js 301 (the annotation rewrite goes beyond ARCHITECTURE 5.11): no code change, as the finding itself asks. It is a deviation for the stage report, DECISIONS.md and the owner, noted in the mathml.js decision notes.
- Choices between conflicting fixes. caps.user requires both names and gives inconclusive (mathml+caps), not either name with info (completeness). caps.db-rules gives inconclusive, not info, when the canary is not refused, because CONTRACT.md defines info as a reading with no pass bar. caps.sample-abort has no 60 s safety stop, because sample.d.ts says not to build a page-side timeout.
- Premise of the platform.js 853 finding: on a v2 page, version-scoping does not return skipped. It never runs, because the signal stored there is stale and ctx.republished never resolves. I added the auto check platform.version-files for the fresh-load reading instead of a v2 branch inside a republish check.

**Handed to the stage session, and where each now stands:**

- `\htmlData` measured "no": recorded in `docs/DECISIONS.md` section 4. The fallback is written into `ARCHITECTURE.md` with the device results, before stage 23.
- The TexSlots annotation rewrite: B20.
- The declaration: `permissions` removed (B19); the canary rule kept.
- Paths `tools/test.mjs` does not exercise: listed in the fix run, and none of them is a pass path.
- One finding (`build.mjs` 182) was cut off in the review's output. Its visible part was applied; whatever else it asked for is unknown.
