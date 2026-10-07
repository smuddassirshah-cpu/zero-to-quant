# The probe's review before publishing (spike S1)

This review ran before the first publish. Each finding is listed here in full, with the change it asked for. Then come the fix run's own record of what it changed, the findings it answered without a change, and what it handed to the stage session. The fix run reported its changes per area, not per finding, so a finding is matched to its fix by file and subject. `docs/DECISIONS.md` B18 relies on this file.

- **Findings:** 17 major, 34 minor and 15 nit, from four reviewers: completeness (19), cdn and harness (17), platform and dbsize (16), and mathml and caps (14).
- **Fix run:** 24 recorded changes, and 4 findings answered without a change.
- **Verification:** a third session re-verified the result. Its tests met 107 of 107 expectations.
- **After publishing:** three changes followed, checked by the archive's own review. They are listed in B18. That review's fixes are in commits 042d476 onwards.

## Findings

**1. major, `CONTRACT.md:108`** (completeness)

- Problem: Several results depend on what Claude does outside the page, and none of it is written down in s1/. Four steps go wrong without it. (1) The v2 publish uses file_path dist/v2/index.html, a different path from v1. Per the Artifact tool, a different path creates a NEW artifact unless url is passed, which would void every republish check. (2) v2 changes index.html (data-version), so the v2 publish cannot also be the omit-page test. If Claude tried to omit the page there, the host would keep the v1 fragment and platform.reload would report 'loaded v1', a false reading of item 14. (3) Claude must write meta/release as {release: 's1-v2', at} and ops/s1-republished as {to: 'v2', at}, both with at later than page load. These values live only in caps.js and harness.js. (4) The null-removals answer needs more than 'accepted'. Claude must also confirm the removals took effect, by listing the files to see 115 paths and no b-001, and needs a split plan if the 303-entry publish is refused.
- Fix asked: Add a short runbook to CONTRACT.md. - v1 publish: dist/v1/index.html with the files map, icon and the capability declaration. - Wait for 'S1 ready for republish'. - v2 publish: url set to the v1 URL, file_path dist/v2/index.html, files as the object map with 201 nulls (the array form cannot carry nulls, and its schema caps it at 255). Record the result as platform.null-removals. - If v2 is refused: publish 255 entries, then the rest, and only then send the signal. - After a successful v2 publish, list the files: expect 115. - Write meta/release, then ops/s1-republished. - After the owner's platform.reload: a third publish with url, no file_path and one new own data file (for example data/v3-only.json from the build). Record it as platform.publish-omit-page, then list the files to confirm index.html is unchanged.

**2. major, `probe/caps.js:243`** (mathml+caps)

- Problem: caps.user passes on a non-empty id alone, but PLAN stage 2 (d) asks for 'user (viewer id, profile)'. If the publish declares no `scopes: ['profile']`, or names are withheld, me().name and profiles()[id].name are '' and the check still passes. The friends board in ASSESSMENT 12.5 depends on profiles() names, so this pass would hide a failed profile property.
- Fix asked: Judge the two parts separately, either as a second check caps.user-profile or as a combined status. Pass only when the id is non-empty and both me().name and profiles([id])[id].name are non-empty. When the id is fine but names are '', report 'inconclusive' and name both possible causes: user.d.ts says a declared scope is a ceiling, and the organisation may withhold names.

**3. major, `probe/caps.js:396`** (mathml+caps)

- Problem: caps.db-rules cannot tell whether the declared rule set is in effect. Every case gives the same outcome under the platform's default rules. db.d.ts says the owner meets every level rule and only {self} privacy limits him, and data/users/{self} privacy is the default. So with the ARCHITECTURE 6.2.4 rule set (root write owner, board write owner, board/{self}, meta write owner), the four results (own ok, notMe invalid_argument, board ok, meta ok) are identical with or without the declaration. The check still reports 'All four as stated' as a pass, and the result goes into the 'the rule set' item of PLAN stage 2 (d).
- Fix asked: Add a canary that only a declared rule can produce. Declare `{ path: 's1canary/{self}', write: 'interact' }` with no prefix rule; db.d.ts says siblings then stay private, the owner included. Add two cases: `s1canary/<own id>` expects ok, `s1canary/zz-not-me` expects invalid_argument. Under the defaults the second write would succeed. Pass only when the canary rejects. Until then, report 'info' with a summary saying that, as the owner, the outcomes equal the defaults. Tell the publishing session that its capabilities declaration must include the canary rule.

**4. major, `probe/caps.js:396`** (completeness)

- Problem: The PLAN asks S1 to check the db rule set, but caps.db-rules cannot see any declared rule. It runs only as the owner, and 'rules never limit the owner; only {self} privacy does' (db.d.ts). So its board/<own id> and meta cases succeed under every possible rule set. Its only refusal case is data/users/zz-not-me, which is the platform's default {self} rule, not one the page declares. No file in s1/ records what capability declaration v1, v2 and dbsize are published with, including the db rules of PLAN 7.3. A pass therefore says nothing about the board/{self} rule or any other declared rule.
- Fix asked: Publish v1 and v2 with the PLAN 7.3 rule set written down: root read interact and write owner, data/users/{self}, board/{self} write interact, meta read view and write owner. Add a case board/zz-not-me that expects invalid_argument: {self} privacy binds the owner too, so this measures a declared rule as the owner. Record the declared rules in the run document. State in the summary that the non-owner levels (root and meta writes refused below owner) cannot be measured with one participant and stay with the emulator (PLAN 7.3).

**5. major, `probe/caps.js:507`** (mathml+caps)

- Problem: caps.meta-release can pass on the initial snapshot. findFresh counts a s1-v2 delivery as fresh when parseAt(docAt) > MODULE_START, but those two times come from different clocks: Claude's sandbox wrote `at`, and MODULE_START is the phone's Date.now(). If the writer's clock runs ahead of the phone by more than the gap between the write and page load, the stale document from the first delivery passes. The likeliest case is a reload or reopen shortly after Claude wrote meta/release.
- Fix asked: Use a test that needs no clock. A s1-v2 delivery is fresh only when an earlier delivery in this subscription had another release, or no document, or a different `at` from the first delivery that showed s1-v2. Keep the existing sawOther rule. As corroboration, compare docAt with the signal's `at`: Claude writes both, so that is a same-clock comparison. Record whether the fresh delivery was index 0, and never pass on index 0.

**6. major, `probe/caps.js:604`** (mathml+caps)

- Problem: Model output is written to the db run document. The consent check stores data.text and puts the reply in its summary. The tiers check stores tiers[t].text. The tools check stores up to 200 characters of the reply in data.text and the tool arguments Claude chose in data.inputs. The harness persists summary and data to ops/s1-run-<runId>. That breaks the security floor in CLAUDE.md and PLAN 8.4 ('Never logged: ... chat, tutor replies') and the reviewer brief's privacy item.
- Fix asked: Store only what was derived from the reply: saidReady, saidOk per tier, hasValue, chars, words, and input key counts. Keep the reply text on screen only, through textContent. Remove the reply from the consent summary.

**7. major, `probe/caps.js:746`** (mathml+caps)

- Problem: caps.sample-abort can pass without testing a mid-stream stop. The 2 s timer aborts before any text arrives whenever the consent dialog is up (if the owner taps this check before caps.sample-consent), the call waits its turn, or the first token is slow. sample.d.ts says such an abort 'is simply dropped' and rejects cancelled, so the check passes with deltasBeforeAbort 0. It has then shown neither that onText stops nor that Claude stops writing. The pass condition also ignores deltasAfterAbort, which the contract says must be 0.
- Fix asked: Pass only when reason === 'first delta', deltasBeforeAbort >= 1, deltasAfterAbort === 0 and code is cancelled. A timer abort before any delta gives 'inconclusive' ('stopped before any text; the mid-stream stop was not measured'). Remove the 2 s timer, or make it a long safety stop (for example 60 s) that also gives inconclusive.

**8. major, `probe/cdn.js:95`** (cdn+harness)

- Problem: readImportMap() reads document.querySelector('script[type="importmap"]'), which is the first import map in the document and not necessarily ours. If the host wrapper has any import map before the fragment, integrity-enforced returns inconclusive and blames 'a probe build defect'. cdnjs-candidates then marks every load as unproven. The bootstrap's mapPresent has the same blind spot.
- Fix asked: Give our map an id in build.mjs (<script type="importmap" id="s1-importmap">) and read that element in readImportMap. In the bootstrap, record document.querySelectorAll('script[type=importmap]').length, and pass it into the data of every check that depends on the map. When there is more than one map, the summary says so instead of naming a build defect.

**9. major, `probe/cdn.js:187`** (cdn+harness)

- Problem: cdn.bootstrap-map passes on any module with an h export, and cdn.static-import passes on any working Preact. Neither checks that 'preact' (or the other specifiers) resolved to the locked URL. If another import map comes first, Preact 10 runs behind 'preact', and both checks still report that the page's map was honoured with Preact 11.0.0.
- Fix asked: In bootstrap-map, fail when moduleResolvesPreact.supported is true and its url differs from lockUrl ('resolved, but not to the locked URL'). Where import.meta.resolve is missing, require a Resource Timing entry for lockUrl. In cdn-static.js, record import.meta.resolve() for preact, preact/hooks, @preact/signals and zod/mini. Make the pass require each to equal its lock.modules url.

**10. major, `probe/cdn.js:377`** (cdn+harness)

- Problem: cdn.integrity-enforced passes even when the wrong-hash URL fails for a reason other than integrity, as long as the control loads. The verdict never uses the Resource Timing evidence that it already stores in data.badUrlTiming.
- Fix asked: Pass only when the bytes are shown to have arrived and been refused. That means a Resource Timing entry for bad.url whose decodedBodySize equals the lock's bytes (1617), or whose responseStatus is 200 where the browser exposes it. If the entry shows 0 bytes or status 0, return inconclusive ('the wrong-hash URL failed before its bytes arrived'). Where timing is not exposed, add a second wrong-hash URL to the map (for example jsxRuntime.mjs?s1-bad2) and require both to be refused.

**11. major, `probe/cdn.js:377`** (completeness)

- Problem: cdn.integrity-enforced passes on any rejection of the one wrong-hash import while the control loads. In WebKit a failed integrity check and a network failure give the same message ('Importing a module script failed'). The module map caches the failure, so it cannot be retried. A single transient failure of that one request therefore reads as 'integrity is enforced', which is a false pass on the property ARCHITECTURE 14 item 18 depends on. The check already records the bad URL's Resource Timing (badUrlTiming) but never uses it in the verdict.
- Fix asked: Pass only when the evidence shows the bytes arrived and were refused. Either require a badUrlTiming entry with responseStatus 200 or decodedBodySize equal to the lock's byte count (jsDelivr sends Timing-Allow-Origin), and otherwise return inconclusive with the reason. Or add a second wrong-hash URL, for example the entry with ?s1-bad2 and its own wrong integrity entry, and require both refusals while the control loads.

**12. major, `probe/cdn.js:591`** (cdn+harness)

- Problem: cdn.umd-fallback says 'the script with a wrong hash was refused' whenever the signals-core script fires onerror. The same URL is never loaded with its correct hash as a control, so a 404, a CORS or a network failure reads as SRI enforcement. This breaks the file's own decision note: 'An integrity verdict always has a control load of the same bytes'.
- Fix asked: After the wrong-hash load, load the same URL again with its correct integrity from lock.umd. Require it to fire 'load' and to define window.preactSignalsCore. If this control fails, return inconclusive. Also record the Resource Timing entry for the bad URL, its decodedBodySize against the lock's 5696 bytes, in data.bad.

**13. major, `probe/cdn.js:591`** (completeness)

- Problem: The wrong-hash classic script has no control. The bad load uses the signals-core UMD URL, and no check ever loads that URL with its correct hash. A 404, a jsDelivr fault or a network blip on that one request ends in onerror, and the check reports 'the script with a wrong hash was refused'. That is a false pass. In the same check, ARCHITECTURE 6.2.7 item 6's fallback also loads @preact/signals as UMD, but signals-core.min.js and signals.min.js are never loaded with their real hashes. Nothing shows a signal driving a Preact 10.29.8 render, so the named fallback is only half measured.
- Fix asked: After the bad load, load the same signals-core URL with ?s1-control and its correct integrity (classic scripts have no module map, so the query avoids an HTTP cache hit being misread). Require that control to load before calling the refusal enforcement, and return inconclusive otherwise. Then load signals.min.js with its hash and render a component that reads a signal under Preact 10.29.8. Record both loads in data.

**14. major, `probe/harness.js:40`** (cdn+harness)

- Problem: REPUBLISH_TIMEOUT_MS is 60 s, but caps.meta-release waits up to 90 s after the signal (RELEASE_WAIT_MS in caps.js line 29). A delivery between 60 and 90 s, or no delivery at all (the check's fail verdict), is therefore recorded as status 'error', with the real verdict tucked into data.lateResult. On timeout, paintRepublish counts the check as done, so the page tells the owner 'S1 republish checks done' before the verdict exists. If the page is closed, the late verdict may never be saved.
- Fix asked: Let a check declare its own limit (for example check.timeoutMs, with caps.meta-release at 100 s), or set REPUBLISH_TIMEOUT_MS to at least 120 s. Keep the republish panel at 'running' until each republish check has a result that did not come from a timeout.

**15. major, `probe/mathml.js:593`** (completeness)

- Problem: ARCHITECTURE 14 item 20 names S1 to close whether `\htmlData` term anchors survive KaTeX's MathML output. No check in the probe, test.mjs or katex-html.mjs does this, so the [unverified] item stays open, against the 11.1 definition of done. The answer does not depend on the device and is already known: KaTeX 0.19.0 drops the attributes in MathML. So item 20's fallback applies: live-formula in the Artifact highlights a term from its term list.
- Fix asked: Add an expectation in tools/test.mjs, or an auto check mathml.htmldata, that renders `\htmlData{term=b}{b^2}` with trust: true and output 'mathml' and records whether any element has data-term. Record the measured 'no' in DECISIONS.md, and write item 20's term-list fallback into ARCHITECTURE before stage 23.

**16. major, `probe/platform.js:852`** (platform+dbsize)

- Problem: The version-scoping and version.json-after checks each take one reading as soon as ctx.republished resolves. They have no delayed re-read and no control showing that v2 is live. Two other causes give the same reading as host scoping: the republish not yet live (propagation delay), or the owner tapping the harness's manual 'The signal did not arrive: start the republish checks' button before Claude has republished. Either way the v1 page sees v1-only present and v2-only absent. versionScoping then reports 'its paths are scoped to the version it loaded' (info), and versionAfter reports a v1/v1 'fail'. The PLAN's definition of done sets the emulator's version-scoping switch from this reading, so a slow publish would set it wrong. versionScoping does not even record the signal, its source ('db' or 'manual') or the time since it arrived.
- Fix asked: Record the signal (at, source) and the ms since it arrived in both checks. When versionScoping reads v1-present and v2-absent, or versionAfter reads v1, fetch again at about +15 s and +40 s, inside the harness's 60 s republish timeout, and keep every reading. Report 'inconclusive' instead of a scoping or caching verdict when the signal source is 'manual' and the readings never change. Also add a structural control: carry the v1 page's base path shape across the reload in sessionStorage (segment count, and whether it equals the reloaded page's base path, never the path itself). Have resume record whether the v2 page's base path differs. A different path is direct evidence that versions are scoped by URL.

**17. major, `probe/platform.js:978`** (platform+dbsize)

- Problem: The back-gesture check cannot record its likeliest failure. If the swipe leaves the artifact screen and the frame is unloaded, the check stops waiting for an answer. On the next load, resume() reports 'inconclusive' and tells the owner to 'Run it again and say what you saw'. Running it again repeats the same swipe and unload, so the result never becomes 'fail'. If the app recreates the frame, sessionStorage is lost and nothing is recorded at all. The answer 'The probe closed or left the artifact' (BACK_CHOICES[1]) can only be given when the page survived, which is the case it was not designed for.
- Fix asked: When resume finds the back marker, also set a session flag such as s1.platform.back.reloaded. When the check runs and that flag is present, ask first: 'Last time the page reloaded during this check. What did the swipe do?', with a choice that maps 'It closed or left the probe' to fail. Record data.reloadedDuringCheck. Also offer that choice before the pushes, so the owner can record a known outcome without swiping again.

**18. minor, `dbsize/dbsize.js:133`** (platform+dbsize)

- Problem: fromSaved accepts any maxDocs from 1 to 9994, and any pauseMs, basePauseMs or cleanPauseMs from 0 to 64,000. The saved status is db data, and the file treats it as untrusted. Yet a status edited by hand or left by a test can lift the PLAN's fixed 60 MB ceiling (9,994 × 192 KiB is about 1.9 GB) or set the pace to 0 ms. Resume then writes back to back, despite the decision note's 'the pause never shrinks'.
- Fix asked: Outside test overrides, require maxDocs <= DEFAULT_MAX_DOCS and pauseMs >= basePauseMs >= DEFAULT_PAUSE_MS. Accept the test values only when the page itself loaded with TEST_PACE or TEST_MAX set. Otherwise put the field in `bad`.

**19. minor, `dbsize/dbsize.js:255`** (platform+dbsize)

- Problem: A run of resource_exhausted refusals is retried without limit at a 64 s pause. If the store keeps refusing, which is plausible when a budget rather than a cap is hit, the run never stops and never records an outcome. The status stays 'running' with exhaustedCount climbing, and the PLAN's 'records success or the cap it reached' is never met.
- Fix asked: Stop as a recorded outcome, for example state 'error' with code 'throttled' and the refused index, after N refusals in a row at MAX_PAUSE_MS (for example 5, about 5 minutes). Keep Resume able to try again.

**20. minor, `dbsize/dbsize.js:383`** (platform+dbsize)

- Problem: dbsize never checks snapshot.metadata.fromCache. (1) At load, a not-yet-definitive status read with exists: false makes the page show 'No earlier run is saved' and enables Start. start() then calls fresh() and saveStatus(), which overwrites a finished 'capped' or 'done' record. (2) At the end of clean-up, an empty listing served from cache sets state 'clean' and saves it, so the status document can claim clean while documents remain.
- Fix asked: Treat a fromCache snapshot as unknown. At load, retry the get, with a pause, until fromCache is false before enabling Start. At the end of clean-up, accept 'empty' only when metadata.fromCache is false and hasPendingWrites is false, otherwise list again. Record the metadata of the final listing in the status.

**21. minor, `probe/caps.js:29`** (mathml+caps)

- Problem: caps.meta-release waits up to 90 s from the moment the signal is seen (RELEASE_WAIT_MS, and its `what` text). The harness stops republish checks 60 s after they start (harness.js line 40, REPUBLISH_TIMEOUT_MS). The check can also start late, queued behind the platform republish checks. A delivery on the periodic fallback (the 15 to 60 s band in the check's own classification), or no delivery at all, then shows as harness 'error: did not finish within 60 s', not as the module's verdict.
- Fix asked: Align the two. Either set the deadline to min(signalSeenAt + 90 s, the check's start + 55 s) and say so in `what`, or have the harness owner give this check a limit above 90 s. Record the deadline used in data.

**22. minor, `probe/caps.js:246`** (completeness)

- Problem: PLAN (d) lists user 'viewer id, profile', but caps.user passes on the id alone. Empty names in me() and profiles() still give a pass, for example when the profile scope was not declared, so the profile half has no verdict.
- Fix asked: Pass only when the id is present and me().name or profiles()[id].name is non-empty. When the id is present but names are empty, return info that names the possible causes (scope not declared, organisation policy).

**23. minor, `probe/caps.js:558`** (mathml+caps)

- Problem: A dead-bridge 'unavailable' on the meta/release watch gives a 'fail'. db.d.ts says such a listener is terminated and 'a fresh onSnapshot is the only recovery', and the harness's own ops/s1-republished watch resubscribes on 'unavailable' (harness.js lines 614 to 618). A transient platform fault would therefore record that meta/release does not reach the page, and push the version.json polling fallback into ARCHITECTURE without cause. The subscription is also never unsubscribed on the fail and inconclusive paths.
- Fix asked: On code 'unavailable', resubscribe up to two times, 5 s apart, and keep the earlier deliveries. If the watch is still dead, report 'inconclusive' and record the code. Call watch.unsubscribe on every exit path.

**24. minor, `probe/caps.js:587`** (completeness)

- Problem: caps.sample-consent passes whenever the first quick-tier call resolves, so it never shows that a consent dialog appeared. If sample was already granted, the pass is measuring something else.
- Fix asked: Read permissions.state('sample') just before and just after the call and record both. Report the consent path as seen only for 'prompt' then 'granted', and as not exercised for 'granted' before the call (info). Optionally ask the owner whether a dialog appeared.

**25. minor, `probe/caps.js:597`** (mathml+caps)

- Problem: caps.sample-consent cannot show that its own call was the one that asked. If the owner taps another sample check first, consent is already granted for the view and this check passes 'with consent' without the dialog being exercised. The page declares permissions, and permissions.state() never prompts, so consent can be measured directly.
- Fix asked: Read permissions.state('sample') before and after the call, and keep a module-level count of sample calls already made. Pass when the state before was 'prompt' and after is 'granted' with a resolve. Report 'inconclusive' when it was already 'granted' or another call came first. Record both states in data.

**26. minor, `probe/caps.js:688`** (mathml+caps)

- Problem: caps.sample-streaming records the onText guarantees it measures (deliveriesAfterResolve, textEqualsDeltasSoFar, lastTextEqualsResult) but passes on count >= 2 alone. A runtime that called onText after the resolve, or broke text === previous + delta, would still pass, although the app's tutor renderer relies on both.
- Fix asked: Pass only when count >= 2, deliveriesAfterResolve === 0, textEqualsDeltasSoFar and lastTextEqualsResult all hold. Report a broken guarantee as 'fail' with the field named.

**27. minor, `probe/cdn.js:537`** (cdn+harness)

- Problem: The UMD check's 'what' claims to measure 'whether the named fallback works', but it never loads @preact/signals' UMD (or signals-core) with a correct hash and never renders a signal. The named fallback in PLAN.md 4.3 and ARCHITECTURE.md 6.2.7 item 6 is Preact 10.29.8 plus '@preact/signals' UMD build'. signals-core is used only as the wrong-hash target.
- Fix asked: After preact and hooks, load signals-core and signals UMD with their correct hashes. Render P.h(Probe) with a signal from window.preactSignals passed as a text child, change its value, and wait for the text to update. The correct-hash signals-core load also gives the control the wrong-hash test lacks (finding above).

**28. minor, `probe/harness.js:40`** (completeness)

- Problem: The harness gives republish checks 60 s (REPUBLISH_TIMEOUT_MS), but caps.meta-release waits up to 90 s from the signal (RELEASE_WAIT_MS). It also queues behind version-json-after and version-scoping. A meta/release delivery 60 to 90 s after its start, which is its own 'periodic fallback' range, is recorded as status 'error' (timeout), with the real result only under data.lateResult.
- Fix asked: Raise REPUBLISH_TIMEOUT_MS to at least 120 s, or let a check declare its own timeout. Alternatively cap RELEASE_WAIT_MS below the harness limit, minus the time the queue may take.

**29. minor, `probe/harness.js:210`** (cdn+harness)

- Problem: connectDb uses useCapability, which resolves null after its own 10 s timer and then ignores a namespace that arrives later ('after the 10 s limit, ignored'). On a slow phone connection, db can be dropped for the whole run. use('db') is memoised, though, so the caps checks that call ctx.claude('db') later get the namespace. The screen then shows 'db is not available' while caps.db-roundtrip passes, and no results reach db.
- Fix asked: In connectDb, keep the claude.use('db') promise after the 10 s mark. If it later resolves to a namespace, set state.db, change dbState to connected, call persist() and the ops/s1-latest write, and start watchRepublish. Log that db arrived late.

**30. minor, `probe/harness.js:488`** (cdn+harness)

- Problem: Write-failure handling has three defects. state.writes.lastError is never cleared, so after one transient failure the header shows 'failing' and 'Last save failed ... Results stay on this screen' for the rest of the visit, even when later saves succeed. Second, a path's retry count (retries) is only reset by a success, so a path that has failed three times is never retried again. Third, nothing flushes or re-queues on pagehide. Together these mean that if the last persist fails, db keeps an older run document and nothing tries again.
- Fix asked: Clear lastError on the next successful write of the same path, base the 'failing' state on whether the latest attempt failed, and reset retries[path] whenever a new body is queued for it. On a final failure, schedule one more persist, for example after 10 s or on visibilitychange to hidden, so the last results get another chance.

**31. minor, `probe/harness.js:601`** (cdn+harness)

- Problem: Whenever 'at' parses, the republish signal counts as fresh only if Claude's clock time is later than the phone's page-start time. If the phone clock is ahead by more than the time between loading the page and the republish, a signal written while the page is open is ignored as 'an older signal', and the owner has to use the manual button. When 'at' does not parse, sawOther also counts fromCache snapshots, which db.d.ts calls not server-definitive; caps.js requires fromCache === false for the same reasoning.
- Fix asked: Also count as fresh a v2 document whose 'at' differs from the recorded stale value, or one that follows a fromCache === false snapshot of a different body. Set sawOther only for fromCache === false snapshots.

**32. minor, `probe/harness.js:891`** (completeness)

- Problem: After the republish checks finish, the panel tells the owner only to say 'S1 republish checks done'. It does not route him to platform.reload, which must run last and after the signal, or say that the omit-page publish follows it. An early tap is skipped, and a late order risks the reload happening after the third publish.
- Fix asked: Add one line: 'Then run "location.reload() after the republish" (Platform checks); it reloads the page. Wait for Claude before anything else.'

**33. minor, `probe/harness.js:932`** (completeness)

- Problem: PLAN 8.1's fallback for a handoff link that cannot leave the frame is a copyable link, and its fallback for a refused clipboard write is selected text. Copy results exercises both paths, but the outcome (writeText, execCommand or blocked) goes only to the harness log, not to a check result. platform.external-link's fallback therefore rests on an unrecorded measurement.
- Fix asked: Record the copy outcome as an extra result, platform.clipboard, with the method that worked, any error name and whether the fallback selected the text. Alternatively add a manual check that copies a fixed link and asks the owner to paste it into the note field.

**34. minor, `probe/harness.js:1025`** (completeness)

- Problem: The Done when requires 'device, app version and date'. The run document records the UA, viewport, typed app version and startedAt, but not the device model: an iOS UA gives only 'iPhone' and the OS version.
- Fix asked: Add a second field, 'iPhone model (Settings, General, About)', stored next to appVersion in the run document. Alternatively, have the stage report ask the owner and say so.

**35. minor, `probe/idb-worker.js:155`** (platform+dbsize)

- Problem: The worker never reports whether it runs as a module. The file deliberately has no import or export, so a browser that ignored `{type: 'module'}` and ran it as a classic worker would still pass. The summary would then say 'A module worker wrote 100 records' without that having been measured.
- Fix asked: Post `module: this === undefined` in the ready message. idbVerdict should fail, or the summary should say 'classic', when type is 'module' and ready.module is not true.

**36. minor, `probe/mathml.js:34`** (completeness)

- Problem: PLAN (b) compares the slot digits in the swapped <mn> 'against the surrounding maths font AND against the sentinel's own <mtext>'. texslots-verdict asks only about the surrounding font. The <mtext> comparison line is drawn but the owner is never asked about it, and the recorded fontOf() values are computed font-family strings, not the fonts actually rendered.
- Fix asked: Add a second question: 'Do the digits in the first line (<mn>) look different from the digits in the comparison line (<mtext>)?' Record the answer next to the existing one.

**37. minor, `probe/mathml.js:220`** (mathml+caps)

- Problem: The clippedLeft evidence cannot detect left clipping in a display formula. It compares the <math> element's box with its scroll box. For display="block", the <math> box is the container's width, and any overflow belongs to its contents. WebKit centres block math [recalled], so overflow there could fall to the left, out of scroll reach, while clippedLeft stays []. Claude reads this field from the run document as evidence that nothing was clipped.
- Fix asked: Measure the content: take the minimum getBoundingClientRect().left over the math element's descendants (or the first child of <semantics>) and compare it with the scroll box's left. Report the count in the specimen summary next to the sideways-scroll count.

**38. minor, `probe/mathml.js:301`** (mathml+caps)

- Problem: The probe tests a binding that goes beyond the documented one. ARCHITECTURE 5.11 and PLAN conflict 10 say only to swap each sentinel <mtext> for an <mn>. They say nothing of KaTeX's TeX <annotation>, which repeats the sentinels, so a straight implementation of 5.11 leaves sentinel text in every MathML tree, including the web's hidden copy. The probe rewrites the annotation and requires that for a pass, which is a deviation that has to be reported, not settled silently.
- Fix asked: No code change in the probe. List it in the stage report and in DECISIONS.md as an addition to the TexSlots binding of 5.11 (rewrite or drop the annotation on both outputs). The owner should then amend ARCHITECTURE 5.11 and PLAN conflict 10.

**39. minor, `probe/mathml.js:340`** (mathml+caps)

- Problem: The TexSlots self-test only compares the binding with slotValues(5), the same function that produced the value. The comment at line 339 says 'k = 5 must show 5 and 0.9527', but no fixed value is checked. The slider wiring is not exercised either: update() is called directly, and no input event is sent, while the pass summary says 'the binding writes the live values'.
- Fix asked: Expect the literal { k: '5', p: '0.9527' }. Set slider.value = '5', dispatch new Event('input'), read the <mn> text, then restore the slider and dispatch again, so the slider path is measured.

**40. minor, `probe/mathml.js:528`** (completeness)

- Problem: The Done when asks for 'the MathML verdict recorded with screenshots'. The page cannot take screenshots and does not ask the owner for any. compare/mathml-chromium.png is Chromium in the sandbox, not the iPhone.
- Fix asked: Make the verdict prompt tell the owner to take screenshots of the sheet and the slots on the phone, light and dark, and send them to Claude. Add 'Screenshots sent' to the choices, or a ctx.note, so the record shows whether they exist.

**41. minor, `probe/platform.js:297`** (platform+dbsize)

- Problem: When encodedBodySize equals decodedBodySize and no Content-Encoding header is visible, the compression check returns 'fail'. On a CORS response (a frame with an opaque origin fetching its files), Content-Encoding is not a safelisted header and reads as null even when the body was compressed. In that case the missing header is not evidence. The check records neither the response type nor `redirected`, and does not use transferSize as a cross-check.
- Fix asked: Record r.type and r.redirected in data. Count a missing header as 'not compressed' only when r.type === 'basic'. Otherwise return inconclusive. Also treat transferSize > 0 && transferSize < dec * 0.8 as a contradiction that gives inconclusive.

**42. minor, `probe/platform.js:329`** (platform+dbsize)

- Problem: The Web Locks check tests contention only inside one agent: an inner ifAvailable request in the same document, and steal against its own lock. Decision 26 depends on the lock manager being shared across tabs and agents. A frame where locks are scoped per document would still pass.
- Fix asked: Add one cross-agent step. A dedicated worker takes `zq-s1-x-<suffix>` and holds it, then the page checks that its ifAvailable request gets null and that steal takes the lock (the worker sees AbortError). If that step fails, count it as a fail.

**43. minor, `probe/platform.js:510`** (platform+dbsize)

- Problem: The hash-route check adds two history entries with `location.hash = target`. It then rewrites only the current entry with history.replaceState, so the frame's back stack keeps #/learn/crs.numwork. Any later back step or back gesture, including the owner leaving the probe, lands the page on that wrong hash first and fires hashchange. The back-gesture check adds to this: it restores with history.go(-n), which leaves #s1-back-1 to 3 as forward entries.
- Fix asked: Restore by walking back instead of rewriting: count the entries the check pushed (2, or 3 with the start replacement), call history.go(-pushed) and await the popstate before restoring with replaceState. Record historyLengthAfter, and compare it with historyLengthBefore, in data.

**44. minor, `probe/platform.js:646`** (platform+dbsize)

- Problem: The external-link check returns 'fail' ('Tapping the link did nothing') when the owner answers 'Nothing happened', even if no click reached the link. A tap on a link fires the page's click event before any host interception. So zero clicks means the tap did not land, and the result is a false fail on the handoff-link decision.
- Fix asked: Return 'inconclusive' with 'no click reached the link' when the answer is LINK_CHOICES[2] and data.clicks === 0. Fail only when clicks > 0.

**45. minor, `probe/platform.js:838`** (platform+dbsize)

- Problem: When versionAfter gets v1 from both fetches, it returns 'fail' with a summary saying the page 'reads its own version's files, not a browser cache'. That cause is asserted, not measured: a lagging publish (see the major finding) or an edge cache that ignores both the query and no-cache gives the same pair. The decision note (lines 19-20) is also wrong. Both URLs carry a fresh `?t=` query, so the browser cache can never hit either one. And `cache: 'no-store'` makes the browser send `Cache-Control: no-cache` upstream. So a v1/v2 split means an intermediary that honours no-cache, or a change between the two fetches, never the browser cache.
- Fix asked: Correct the decision note. Change the v1/v1 summary to say what was measured, for example 'version.json said v1 with default caching and with no-store, N ms after the signal'. Make the status 'inconclusive' unless the delayed re-reads also say v1. Let platform.version-scoping give the cause.

**46. minor, `probe/platform.js:838`** (completeness)

- Problem: When both the default-cache and the no-store fetch of version.json say v1, the summary says 'this open page reads its own version's files, not a browser cache'. A host-side cache that ignores the query string, which is item 12's exact question, gives the same pair of readings. Only platform.version-scoping's v2-only result can tell the two apart, and the check does not consult it.
- Fix asked: In version-json-after, also fetch data/v2-only.json with no-store. If v2-only is present while version.json says v1, report 'the host served a cached version.json despite the query string'. If it is absent, report version scoping.

**47. minor, `probe/platform.js:853`** (completeness)

- Problem: On the reloaded v2 page, version-scoping returns skipped. So no on-device reading confirms that the null removals took effect for a fresh load (b-001 and v1-only gone, b-300 and v2-only present). The tool's acceptance of the v2 publish is the only evidence for item 15's removal half.
- Fix asked: On a v2 page that loaded after the republish, fetch the same four files and report info: removed files absent, added files present. Keep the v1 branch as it is.

**48. minor, `probe/platform.js:904`** (platform+dbsize)

- Problem: The reload marker goes into the URL hash only when the sessionStorage write throws. If the write succeeds but the storage does not survive the reload, resume finds no marker and platform.reload is never recorded. Examples are a frame the host recreates, or ephemeral or partitioned storage that is reset.
- Fix asked: Always write both carriers: sessionStorage, plus the #s1-reload-<version> hash. Have resume prefer sessionStorage, fall back to the hash, clear both, and record which carriers survived.

**49. minor, `tools/build.mjs:32`** (completeness)

- Problem: PLAN (a) asks for Preact 11.0.0, @preact/signals and zod/mini from cdnjs where it hosts the identical file. The cdnjs candidates cover only preact, preact/hooks, katex and fflate, so @preact/signals, @preact/signals-core and zod/mini are never tried. The candidates are also imported by full URL rather than reached through a bare specifier in the map's imports. STATE open question 6 and ARCHITECTURE 14 item 21 close at stage 4, so this is partial evidence, not a block.
- Fix asked: Add the cdnjs paths cdnjs would use for @preact/signals 2.11.3, @preact/signals-core 1.14.4 and zod 4.6.5 (mini entry), with the npm hashes in the map. Say in the summary that the stage 4 lock tool remains the authority.

**50. minor, `tools/build.mjs:182`** (completeness)

- Problem: The Artifact tool requires the publishing session to read in full every file it did not write. Builder subagents wrote these files, and the build generated them. v1 and v2 are each about 555 KB, of which data/compress.json is 300,289 bytes and the import map 16.8 KB. Reading every file twice costs a large share of the publishing session's context for no measurement gain.
- Fix asked: Shrink compress.json to about 64 KB, which is still far above any compression threshold, and keep it byte-identical in v1 and v2. Plan the read: the bulk files are 8 to 9 bytes each, and v2 shares 12 files byte-for-byte with v1, by SHA-256 in manifest.json.

**51. minor, `tools/build.mjs:297`** (cdn+harness)

- Problem: The v2 republish described by manifest.republish has 304 entries: 101 added and 2 changed files plus 201 null removals. That is over the tool's 255 per publish if nulls count, and this is the very property platform.null-removals exists to measure. The manifest gives no fallback split. Its removed list is sorted, so data/v1-only.json, the file platform.version-scoping relies on, comes last. Trimming the list from the end to fit 255 would leave it published, and version-scoping would then read 'v1-only present' as version scoping. The path check (line 283) also flags 255 although the tool allows at most 255.
- Fix asked: Write the planned publish sizes into the manifest, and add a fallbackBatches field that splits the removals so data/v1-only.json and bulk/b-001.json are removed in the first batch. Change the path check to count > 255.

**52. nit, `dbsize/dbsize.js:10`** (platform+dbsize)

- Problem: The decision note says the base-36 pad means 'no layer can compress it much'. In fact gzip and brotli shrink a body to about 66%. If the store counted compressed bytes, the 60 MiB run would put only about 40 MiB in the store.
- Fix asked: Correct the note to 'compresses to about two thirds'. Or use a 64-character alphabet (6 bits a character, about 75%) to narrow the gap. Since the app's JSON compresses better, the logical-byte reading stays conservative. Say so in the note.

**53. nit, `dbsize/dbsize.js:66`** (platform+dbsize)

- Problem: withTimeout gives up after 90 s but does not cancel the call. Resume, enabled at once in the 'error' state, can then send a second set() to the same document while the first is still in flight. That goes against db.d.ts's one-write-at-a-time rule. The content is identical, so the risk is only slower writes.
- Fix asked: Keep the timed-out promise and have Resume await its settlement, with its own cap, before writing that index again.

**54. nit, `dbsize/dbsize.js:555`** (platform+dbsize)

- Problem: PLAN.md item (d) says the probe 'records success or the cap it reached, then deletes its documents'. Here clean-up waits for the owner to tap Clean up after 'done' or 'capped'. This is a small departure from PLAN.md that is not logged.
- Fix asked: Start cleanLoop automatically after the final status write, keeping the button for resuming. Or log the manual step as a deviation in the stage report.

**55. nit, `probe/caps.js:617`** (mathml+caps)

- Problem: caps.sample-limits is kind 'consent', but sample.d.ts says limits() is 'Cheap and local: no usage is spent, the viewer is not prompted'. It only runs on a tap, so its evidence is often missing when the tools check needs it.
- Fix asked: Make it kind 'auto'.

**56. nit, `probe/cdn-worker.js:97`** (completeness)

- Problem: The worker loads each library with a dynamic import(url). ARCHITECTURE 6.2.7 item 4 builds the data worker with static imports rewritten to full URLs. Both are module-graph fetches under the same CSP, so a difference is unlikely, but the shape measured is not the shape that ships.
- Fix asked: Optionally add a second module worker whose source statically imports the three full URLs. The URLs live in lock.json, so the build would have to generate it as our own file. Record whether both start.

**57. nit, `probe/cdn.js:187`** (completeness)

- Problem: cdn.bootstrap-map passes when a module exporting h arrives, without checking that 'preact' resolved to the locked jsDelivr URL. moduleResolvesPreact and lockUrl are both recorded but never compared.
- Fix asked: When import.meta.resolve is supported, require moduleResolvesPreact.url === lockUrl for a pass, and return inconclusive with both values otherwise.

**58. nit, `probe/cdn.js:421`** (cdn+harness)

- Problem: In cdnjs-candidates, proven = loaded.filter(r => r.inMap !== false) counts a candidate whose map entry could not be read (inMap null) as proven byte-identical.
- Fix asked: Count a candidate as proven only when inMap === true. Report null ones as 'map not readable'.

**59. nit, `probe/cdn.js:520`** (cdn+harness)

- Problem: The module-worker pass does not record that no integrity applies to the worker's CDN imports. A worker has no import map and import() takes no integrity, so classic zod's 95-file closure loads unverified. Decision 24 expects the host's CSP and the drift check to cover this, and the report should say so.
- Fix asked: Add data.integrityApplied: false, and say in the summary that the worker imports are not hash-checked, so the stage report states it from the evidence.

**60. nit, `probe/harness.js:326`** (cdn+harness)

- Problem: normalise() never clips a summary, and fitDoc only shrinks data. A very long summary or lateResult summary could keep the document over its limit after every cut. The resulting invalid_argument is in NO_RETRY, so every later save of the run document would fail too.
- Fix asked: Clip summaries in normalise() and late(), for example to 600 characters, and record that they were clipped.

**61. nit, `probe/harness.js:617`** (cdn+harness)

- Problem: The republish watch subscribes again only when the code is exactly 'unavailable'. db.d.ts says to treat unknown codes as unavailable, and queue_overflow is terminal for a listener.
- Fix asked: Also subscribe again for codes outside the known set, for example any code other than invalid_argument, resource_exhausted and revoked.

**62. nit, `probe/mathml.js:579`** (mathml+caps)

- Problem: mathml.texslots-verdict asks the owner to move the slider, but does not record whether he did before answering the font question. kAtAnswer = 3 is ambiguous, because 3 is also the starting value.
- Fix asked: Count input events on the slider and store sliderMoves and the distinct k values seen in data. Report 'inconclusive' when the font answer came with zero moves.

**63. nit, `probe/platform.js:234`** (platform+dbsize)

- Problem: idbVerdict fails 'IndexedDB in a worker' when indexedDB.databases() still lists the database right after deleteDatabase succeeds. That is a cleanup property, not the one being measured, and a brief listing lag would be a false fail.
- Fix asked: Record listedAfterDelete in data and mention it in the summary, but leave it out of the pass bar. Keep the delete.ok requirement, or move it to the summary as well.

**64. nit, `tools/build.mjs:141`** (cdn+harness)

- Problem: The build takes each module's closure from cdn-lock.json's files list and never derives it again. A closure file left out of the lock would load with no integrity check, and the build would not notice, so the note 'the import map can never ship a hash nobody checked' is stronger than what the code guarantees.
- Fix asked: Add the same scan to build.mjs. Parse each closure file's import and export specifiers, resolve them against the file URL or the map, and make it a problem if a reached URL has no integrity entry or a non-literal import() appears.

**65. nit, `tools/build.mjs:174`** (cdn+harness)

- Problem: If the host blocks the inline import map and bootstrap, the page shows 'The probe is loading.' forever and the owner has nothing to report.
- Fix asked: Change the boot line to say what it means if it stays, for example 'The probe is loading. If this line is still here after a minute, the page's scripts did not run: tell Claude.'

**66. nit, `tools/build.mjs:277`** (cdn+harness)

- Problem: The fragment checks (no html, head or body tags, no module script, title first) run on v1 and v2 only. dist/dbsize/index.html, which is published as its own Artifact, is copied without them.
- Fix asked: Run the same checks on dist/dbsize/index.html.

## What the fix run changed

1. cdn.js integrity-enforced (major): a pass now needs the refused URL's Resource Timing entry to show the bytes arrived (decodedBodySize equal to lock bytes, or status 200). Zero bytes while the control's sizes are exposed gives inconclusive. Where sizes are hidden, a second wrong-hash URL (?s1-bad2) must also be refused. build.mjs adds badIntegrity.bytes and badIntegrity.second.
2. cdn.js umd-fallback (two majors, one minor): after the wrong-hash loads (two URLs), signals-core is loaded with its correct hash at ?s1-control and must define preactSignalsCore, or the check is inconclusive. Then signals.min.js is loaded with its hash and a signal drives a Preact 10.29.8 render. Timing for the bad URL is recorded against the lock's 5696 bytes.
3. cdn.js and cdn-static.js resolution (major): bootstrap-map fails when import.meta.resolve('preact') is not the locked URL, and needs a Resource Timing entry when resolve is missing. cdn-static.js records import.meta.resolve for its four specifiers, and static-import requires each to match lock.modules.
4. readImportMap and the bootstrap (major): the map has id s1-importmap and is read by that id. The bootstrap records mapCount. Map-dependent checks record mapCount and say so when there is more than one map.
5. Republish timeouts (major in harness.js, minor duplicates in caps.js and from the completeness reviewer): a check may declare timeoutMs (at most 300 s). The republish default is 120 s, and caps.meta-release declares 120 s and records its deadline. The panel waits for results that did not come from a timeout.
6. harness.js connectDb (minor): a db namespace that arrives after 10 s is taken through the onLate callback of useCapability. It connects, persists, writes ops/s1-latest and starts the watch. The run document records db.lateMs.
7. harness.js writes (minor): lastError and the failing state clear when a later write of the same path succeeds. Retries reset whenever a new body is queued. Exhausted retries get a 10 s retry (at most 3), and failing paths are queued again on visibilitychange to hidden.
8. harness.js signal freshness (minor): the check needs no clock. Only definitive deliveries count. A v2 signal is fresh after a definitive delivery of another value (sawOther is kept across subscriptions), or when its 'at' differs from the stale one seen at load. Resubscribe on any code outside the terminal set (nit). Summaries are clipped to 600 characters in normalise() and late() (nit).
9. build.mjs (minor and nits): manifest.publishPlan gives planned sizes and v2FallbackBatches (255 + 50 entries), with data/v1-only.json and bulk/b-001.json removed first. The path check is now > 255. The closure walk uses vm.SourceTextModule specifiers plus a scan for dynamic import(). dbsize/index.html gets the fragment checks. Both pages get the new boot line. compress.json is about 64 KB. Adds dist/v3 for the omit-page publish, the capabilities declaration (with the s1canary/{self} canary) in lock.json and the manifest, and cdnjs candidates for @preact/signals, signals-core and zod/mini.
10. cdn.js nits: cdnjs counts a candidate as proven only when inMap === true; a null is recorded as 'map not readable', and the summary names the stage 4 lock tool as the authority. module-worker records integrityApplied: false and says so.
11. caps.js db-rules (major, two reviewers): adds the canaryOwn and canaryNotMe cases. Pass requires the canary refusal; otherwise inconclusive. Records the declared rules and canaryDeclared, and states that levels below owner stay with the emulator.
12. caps.js meta-release (major and minor): the check needs no clock and never passes on the first delivery. A dead bridge's 'unavailable' resubscribes twice, 5 s apart, and if the watch is still dead the result is inconclusive. The watch is unsubscribed on exit. writeGapMs and corroborated are a same-clock comparison.
13. caps.js sample-abort (major): the 2 s timer is removed, following sample.d.ts. A pass needs reason 'first delta', at least one delta before the abort, none after (it waits 500 ms for late calls) and code cancelled. A resolve with no delta gives inconclusive.
14. caps.js model output (major): no reply text is stored. Consent keeps saidReady and chars; tiers keep saidOk and chars; tools keep chars and the type and key count of each input. The text appears on screen only.
15. caps.js user (major and minor): a pass needs a non-empty id and non-empty names from both me() and profiles(). Empty names give inconclusive, naming the declared scopes and organisation policy.
16. caps.js streaming (minor): a pass also needs deliveriesAfterResolve 0, textEqualsDeltasSoFar and lastTextEqualsResult; a broken guarantee is a named fail. consent (minor, two reviewers): reads permissions.state('sample') before and after and counts earlier sample calls; a pass needs prompt then granted on the first call. limits (nit): kind auto.
17. mathml.js (minors and nit): clippedLeft is measured from the content's descendants, and the count is in the summary. The TexSlots self-test drives the slider (value 5 and an input event) and expects the literal 5 and 0.9527 in both copies. texslots-verdict counts slider moves (inconclusive at zero), adds the mn-against-mtext question and a screenshots prompt. specimen-verdict adds a screenshots prompt. New auto check mathml.htmldata (completeness major).
18. platform.js version checks (major and two minors): both record the signal (at, source, ms since). A v1 reading is read again 15 s and 40 s after the signal. A manual signal with unchanged readings gives inconclusive. version-json-after cross-checks data/v2-only.json, and its v1/v1 result is now inconclusive or 'cached', never an asserted cause. The decision note is corrected.
19. platform.js back-gesture (major): resume sets s1.platform.back.reloaded. The next run asks what the swipe did, and 'It closed or left the probe' is a fail. There is always a pre-swipe choice to record a known outcome. hash-routes (minor): walks back history.go(-pushed), waits for popstate, then restores; historyLengthAfter is recorded.
20. platform.js other minors: compression records type and redirected, gives inconclusive for a missing header on a non-basic response, and checks transferSize. external-link with 'Nothing happened' and 0 clicks gives inconclusive. reload always writes both carriers plus a base-path hash; resume prefers sessionStorage and records the carriers and basePath.same. web-locks adds a cross-agent step with the new probe/locks-worker.js.
21. platform.js additions for completeness minors: new auto check platform.version-files (pass or fail on a fresh v2 load) and new manual check platform.clipboard (paste-back match only). The harness records the outcome of Copy results in harness.copy. idb-worker.js reports module (top-level this undefined), idbVerdict requires it, and listedAfterDelete moved out of the pass bar into the summary (nit).
22. dbsize.js (minors and nits): loads retry until fromCache is false. Clean-up ends only on a definitive empty listing and records finalListing. fromSaved limits maxDocs and pacing to the defaults unless a test override is set. 5 refusals in a row at the pause cap give 'error' with code 'throttled'. Clean-up starts by itself after done or capped. Resume waits up to 30 s for a timed-out call. The decision note now says the pad compresses to about two thirds. page.html boot line.
23. harness.js and CONTRACT.md (completeness major and minor): the harness gets an iPhone model field (deviceModel in the run document). CONTRACT.md gets a 9-step publishing runbook (url on v2, the null map, fallback batches, signal order with a new 'at', file listings, v3 publish without the page) and documents timeoutMs and the new lock and ctx fields.
24. tools/test.mjs: the fake adds {self} prefixes, granted-after-consent, a db delay, write faults, seeds, cached gets, listener faults, withheld names and always-on exhaust. The main run seeds future-dated stale signals and switches 8 s after the signal. New variants phase (network-aborted wrong-hash URLs, 404 UMD, late db, failing writes, host map first, no Timing-Allow-Origin, no canary). New dbsize runs 3 to 5, plus publish-plan, limits, no-model-output and resubscription rows.

## Answered without a change

- Completeness major (caps.js 396), the part asking for a board/zz-not-me case that expects invalid_argument: under the declared rule set this case reads wrong. ARCHITECTURE 6.2.4 declares a 'board' prefix rule (read interact, write owner). db.d.ts says a rule at the prefix opens siblings' subtrees at its levels, and the owner meets 'owner'. So the owner's write to board/zz-not-me succeeds with or without the declaration. I used the mathml+caps reviewer's s1canary/{self} canary instead, which has no prefix rule. The rest of that finding (record the declared rules, state the non-owner limits) is implemented.
- mathml.js 301 (the annotation rewrite goes beyond ARCHITECTURE 5.11): no code change, as the finding itself asks. It is a deviation for the stage report, DECISIONS.md and the owner, noted in the mathml.js decision notes.
- Choices between conflicting fixes. caps.user requires both names and gives inconclusive (mathml+caps), not either name with info (completeness). caps.db-rules gives inconclusive, not info, when the canary is not refused, because CONTRACT.md defines info as a reading with no pass bar. caps.sample-abort has no 60 s safety stop, because sample.d.ts says not to build a page-side timeout.
- Premise of the platform.js 853 finding: on a v2 page, version-scoping does not return skipped. It never runs, because the signal stored there is stale and ctx.republished never resolves. I added the auto check platform.version-files for the fresh-load reading instead of a v2 branch inside a republish check.

## Handed to the stage session, and where each now stands

- `\htmlData` measured "no": recorded in `docs/DECISIONS.md` section 4. The fallback is written into `ARCHITECTURE.md` with the device results, before stage 23.
- The TexSlots annotation rewrite: B20.
- The declaration: `permissions` removed (B19), and the canary rule kept.
- These paths are not exercised by tools/test.mjs: the republish panel waiting on a late result; the inconclusive path of the version checks after a manual signal; a broken onText guarantee; the abort check resolving with no delta; dbsize waiting on a stale call (it needs a 90 s hang); a non-definitive empty listing during clean-up; a positive case of clippedLeft (Chromium never clips display maths on the left); a cdnjs candidate with inMap null. Seven of these paths can end only in inconclusive, fail, info or a wait. The eighth, content clipped on the left, still lets `mathml.specimen` pass: the count of clipped formulas is named in its summary, for the owner's verdict on the sheet.
- The fix run reported the `tools/build.mjs` 182 finding as cut off. The stored finding is complete (above). Both of its asks were carried out: `data/compress.json` was cut to about 64 KB, and the publishing session read v2 as the differences from v1, by SHA-256.
