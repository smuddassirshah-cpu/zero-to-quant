# Spike S1 results

Measured on 7 October 2026 on the owner's iPhone 17 Pro Max, iOS 27.2 (from Settings; the page's user agent reports `iPhone OS 18_7`), Claude app 1.261002.20 (37091698851). The raw run documents are beside this file; `docs/DECISIONS.md` section 4 holds the verdicts.

## Runs

| Run | Page | Started (UTC) | Role |
|---|---|---|---|
| `muyo6opa-zw5x5f` | v1 | 22:19:12 | v1, first cold load; left after four checks |
| `muyo87q6-54fhvx` | v1 | 22:20:24 | v1, every automatic check |
| `muyocrk9-mt4r0y` | v1 | 22:23:56 | v1, every automatic check and the 13 tapped checks; open during the republish |
| `muyonw26-eo20ft` | v2 | 22:32:35 | v2, the open page reloaded by the host after the first publish batch |
| `muyoo2d3-s9cuc0` | v2 | 22:32:43 | v2, reloaded again after the second batch; received the signal |
| `muyotd7h-2qr2y6` | v2 | 22:36:51 | v2, after `platform.reload`; ran the back-gesture check |

## Every check, by the run that settles it

| Check | Kind | Status | Run | Summary |
|---|---|---|---|---|
| `caps.db-roundtrip` | auto | pass | `muyotd7h` | The body of 15 fields came back equal from a server read (set 205 ms, get 289 ms, delete 218 ms); the document was deleted. |
| `caps.db-rules` | auto | pass | `muyotd7h` | All six as stated, and the canary shows the declared rule set is in effect: own written and read back; notMe set() rejected with invalid_argument; board written and read back; meta written and read back; canaryOwn written and read back; canaryNotMe set() rejected with invalid_argument. Levels below owner need a second participant and stay with the emulator. |
| `caps.meta-release` | republish | pass | `muyoo2d3` | meta/release said s1-v2 on this open page (it followed a server delivery of another value while the page was open), 1.6 s before the ops/s1-republished time (db signal); it looked realtime. |
| `caps.permissions` | auto | info | `muyotd7h` | permissions.state() resolved in 2 ms: db granted, sample granted. |
| `caps.sample-abort` | tap | pass | `muyocrk9` | Aborted at the first delta (615 ms); the call rejected cancelled 1 ms later and onText did not fire again. |
| `caps.sample-consent` | tap | pass | `muyocrk9` | sample() resolved in 3097 ms, including the consent dialog: the state went from prompt to granted, and the reply said the word asked for. |
| `caps.sample-limits` | auto | info | `muyotd7h` | sample.limits(): 262144 prompt bytes, images not offered, tools offered (at most 16). |
| `caps.sample-streaming` | tap | pass | `muyocrk9` | onText fired 7 times before the call resolved, the first after 924 ms, each text the previous plus its delta and the last equal to the result; the whole answer took 3141 ms. |
| `caps.sample-tiers` | tap | pass | `muyocrk9` | All three tiers answered as asked: quick 631 ms, default 2043 ms, complex 1027 ms. |
| `caps.sample-tools` | tap | pass | `muyocrk9` | execute ran 1 time and the reply carries 4217 (1580 ms). |
| `caps.user` | auto | pass | `muyotd7h` | The user namespace answered with an id and a profile: owner yes, can edit yes, can('data.write') true, an id of 24 characters, a name in me() yes, in profiles() yes. |
| `cdn.bootstrap-map` | auto | pass | `muyotd7h` | The bootstrap's import('preact') resolved through the map to the locked URL in 2 ms and the module exports h. |
| `cdn.cdnjs-candidates` | auto | info | `muyotd7h` | cdnjs serves 1 of 14 candidates byte-identical to npm: katex (KaTeX/0.19.0/katex.mjs). Not served or refused: preact (preact/11.0.0/preact.mjs), preact (preact/11.0.0/dist/preact.mjs), preact/hooks (preact/11.0.0/hooks.mjs), preact/hooks (preact/11.0.0/hooks/dist/hooks.mjs), @preact/signals (preact-signals/2.11.3/signals.mjs), @preact/signals (preact-signals/2.11.3/dist/signals.mjs), @preact/signals-core (preact-signals-core/1.14.4/signals-core.mjs), @preact/signals-core (preact-signals-core/1.14.4/dist/signals-core.mjs), zod/mini (zod/4.6.5/mini/index.js), zod/mini (zod/4.6.5/mini/index.mjs),... [188 more characters] |
| `cdn.integrity-enforced` | auto | pass | `muyotd7h` | Both wrong-hash URLs were refused (TypeError: Cannot load script due to integrity mismatch) and the same file with no integrity entry loaded in 0 ms. Resource Timing does not expose sizes for the CDN here, so the verdict rests on the two refusals beside the control. |
| `cdn.load-cost` | auto | info | `muyotd7h` | 96 CDN requests so far: zod@4.6.5 92, preact@11.0.0 2, @preact/signals@2.11.3 1, @preact/signals-core@1.14.4 1 (the zod/mini closure is 92 files); 995 ms of request time over a 383 ms span; the browser reported zero for every size field, so sizes were not measured. |
| `cdn.module-worker` | auto | pass | `muyotd7h` | A module worker started in 6 ms, imported zod (19 ms), ts-fsrs (1 ms), fflate (3 ms) by full URL and ran each. ts-fsrs due offsets: 1 min, 6 min, 10 min, 8 d. These imports are not hash-checked: a worker has no import map and import() takes no integrity. |
| `cdn.static-import` | auto | pass | `muyotd7h` | The static bare imports resolved through the map to the locked URLs and loaded in 43 ms; Preact rendered, the component and the bound text both updated on the signal change (component after 1 ms, both after 1 ms), and zod/mini accepted the valid object and rejected the invalid one. |
| `cdn.umd-fallback` | auto | pass | `muyotd7h` | Preact 10.29.8, its hooks, signals-core and @preact/signals loaded as classic scripts with integrity, rendered with useState and updated on a signal change in 10 ms; the signals-core script with a wrong hash was refused at two URLs (Resource Timing does not expose sizes here), while the same file with its correct hash loaded in 0 ms. |
| `mathml.htmldata` | auto | fail | `muyotd7h` | KaTeX 0.19.0's MathML output drops \htmlData: no element carries data-term, while the HTML output does. The fallback of ARCHITECTURE.md 14 item 20 applies: live-formula in the Artifact highlights a term from its term list. |
| `mathml.katex` | auto | pass | `muyotd7h` | KaTeX 0.19.0 loaded through the import map in 4 ms and rendered MathML in 1 ms. |
| `mathml.native-layout` | auto | pass | `muyotd7h` | The browser lays MathML out: the numerator sits 30.7 px above the denominator and the superscript 8.4 px above its base. |
| `mathml.specimen` | auto | pass | `muyotd7h` | All 40 formulas rendered as MathML without a KaTeX error in 9 ms; 5 scroll sideways, 0 start left of their scroll box. |
| `mathml.specimen-verdict` | tap | pass | `muyocrk9` | The owner judged every formula readable and correctly set. Screenshots: sent. |
| `mathml.texslots` | auto | pass | `muyotd7h` | Both sentinels became <mn> elements and no sentinel text is left, after the TeX annotation, which repeated them, was rewritten; moving the slider to 5 showed 5 and 0.9527 in both copies. |
| `mathml.texslots-verdict` | tap | pass | `muyocrk9` | The live digits match the maths font over 2 values of k, and VoiceOver reads the current values. The <mn> digits look the same as the <mtext> copy; screenshots sent. |
| `platform.back-gesture` | tap | fail | `muyotd7h` | The back gesture did nothing in the frame: no popstate event and the hash stayed #s1-back-3. |
| `platform.clipboard` | tap | pass | `muyocrk9` | The link was copied (clipboard.writeText) and pasted back unchanged. |
| `platform.compression` | auto | pass | `muyotd7h` | Compressed in transit: 6.4 KB on the wire for 62.7 KB of JSON (10%), Content-Encoding gzip. |
| `platform.external-link` | tap | pass | `muyocrk9` | It opened in a browser. The handoff link of ASSESSMENT.md 14.3 can be an anchor. |
| `platform.file-input` | tap | pass | `muyocrk9` | The file input worked: FileReader read the first 64 bytes of a 62511-byte file in 1 ms. |
| `platform.google-fonts` | auto | pass | `muyotd7h` | Archivo loaded in 2 ms; Source Code Pro loaded in 2 ms. |
| `platform.hash-routes` | auto | pass | `muyotd7h` | #/learn/crs.numwork round-tripped and hashchange fired in 2 ms; #s1-plain round-tripped. The original hash was restored. The check walked back 2 entries. |
| `platform.idb-worker` | auto | pass | `muyotd7h` | A module worker (top-level this undefined) wrote 100 records in one transaction in 10 ms, read all of them back unchanged in 1 ms and deleted the database (19 ms in all). |
| `platform.inline-style` | auto | pass | `muyotd7h` | The style attribute parsed through innerHTML applied (computed rgb(1, 2, 3)); element.style applied too. |
| `platform.null-removals` | auto | info | `muyotd7h` | Claude records this from the publishing tool |
| `platform.publish-omit-page` | auto | info | `muyotd7h` | Claude records this from the publishing tool |
| `platform.reload` | resume | info | `muyotd7h` | After the republish, location.reload() loaded v2 (the page was v2 before; version.json now says v2). The page loaded from the same base path as before. |
| `platform.storage-estimate` | auto | info | `muyotd7h` | Usage 0.1 MB of a 983 MB quota; persisted: false. |
| `platform.version-files` | auto | pass | `muyotd7h` | On a fresh v2 load the removed files are gone and the added ones served (v1-only absent, b-001 absent, v2-only present, b-300 present): the null removals took effect. |
| `platform.version-json-after` | republish | skipped | `muyoo2d3` | This page is v2. The check runs on the v1 page that stayed open during the republish. |
| `platform.version-json-before` | auto | info | `muyotd7h` | version.json says v2, matching this page (HTTP 200, 234 ms). |
| `platform.version-scoping` | republish | skipped | `muyoo2d3` | This page is v2. The check runs on the v1 page that stayed open during the republish. |
| `platform.web-locks` | auto | pass | `muyotd7h` | navigator.locks granted the lock, refused a second ifAvailable request inside it, and steal: true took a held lock (15 ms); against a dedicated worker's lock the page's ifAvailable got null and steal: true took it (the worker saw AbortError). |
| `platform.window-open` | tap | info | `muyocrk9` | window.open returned null; you saw: Nothing happened. |

`platform.version-json-after` and `platform.version-scoping` were skipped by design: they run only on a v1 page that stays open across the republish, and the host reloaded that page to v2 within 4 s of each publish (the runs above). What they set out to measure is answered by the reload itself.

## Measured with the publishing tool

| Step | Answer |
|---|---|
| v1 publish, 7 October 19:51 UTC | Accepted: version `1791402675-43ad`, 216 files, the declaration stored as sent (`db` with six rules, `user` with `profile`, `sample`) |
| v2 as one publish: 303 `files` entries (102 added or changed, 201 `null` removals) | **Refused, nothing published**: "`files` lists 303 entries (removals included), over the limit of 255 one publish may send. Nothing was published: send at most 255 now and add the rest with another publish to the same url." The message adds that files left out of a later publish are kept and a version holds up to 511 files. So `null` removals count against the 255. |
| v2 in two publishes (254 entries, then 49 removals) | Both accepted: versions `1791412351-44e4` (22:32:31) and `1791412362-9e54` (22:32:42); the declaration carried forward; the listing shows the 116 paths of the v2 build, without `data/v1-only.json` or `bulk/b-001.json` |
| v3, one file and no page | **Refused by the tool before sending**: "`files` and `root` only name supporting files, and nothing was published: also pass `file_path`" (the page's `.html` file). Every publish carries the page. |
| Open pages after a publish | The page open on the iPhone was reloaded by the host to the new version 4 s after the first batch and 1 s after the second (runs `muyonw26` and `muyoo2d3`, whose `previousRunId` is the page they replaced) |
| Response headers of published files | `cache-control: private, max-age=31536000, immutable, no-transform`, `content-encoding: gzip`, served through Cloudflare (`platform.compression`, `platform.reload`) |

## The `db` size probe

`dbsize-status-s1-size.json`, run 22:39 to 23:07 UTC: all 320 documents of 196,608 bytes written (62,914,560 bytes, 60 MiB) with no `quota_exceeded` and no `resource_exhausted`; one `unavailable` at document 182, retried once and accepted. Writes took 414 ms on average and 997 ms at most. Clean-up deleted indices 1 to 325 and a server-definitive listing came back empty. The screen wake lock was refused: "'screen-wake-lock' is not allowed by Feature-Policy".
