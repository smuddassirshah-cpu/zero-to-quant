// Spike S1 local test: builds dist/, serves it through tools/serve.mjs, runs the probe in Chromium with a fake
// window.claude and the CDN answered from npm/, drives every manual, consent and republish check, runs the db
// size probe, takes the comparison screenshots and checks each result against what this browser and this
// emulation should give. Never published; the owner's iPhone gives the real results.
//
// Usage: node tools/test.mjs        (ZQ_CHROMIUM=/path/to/chrome picks the browser)
//
// Decision notes:
// - playwright-core is imported by path from the repository's node_modules and drives an installed
//   Chromium; nothing is installed or downloaded.
// - One router answers every request the browser makes: 127.0.0.1 passes, cdn.jsdelivr.net is answered from
//   npm/ (so SRI and import-map integrity are checked against the real npm bytes), cdnjs answers 404 (it is
//   not reachable from this sandbox), fonts.googleapis.com answers an empty stylesheet and fonts.gstatic.com
//   404, and any other host is aborted and counted against the page that asked. The browser also runs with
//   --no-proxy-server, so nothing the router misses can leave through the sandbox proxy.
// - The fake window.claude follows the .d.ts contracts the probe calls: db with the path grammar and parity,
//   the {self} privacy of the declared rules (data/users and, as the probe declares it, the s1canary canary),
//   body limits, asynchronous snapshots and injected faults; user, permissions (sample turns granted after the
//   first resolved call) and sample as the test brief fixes them. It also watches the probe: reads of any
//   member but use, overlapping writes to one document, and the spacing of the harness's writes.
// - The main run seeds a stale republish signal and a stale meta/release whose `at` is an hour in the future
//   (a writer's clock ahead of the phone), so a clock comparison would start the republish checks at once;
//   the switch to v2 happens 8 s after the signal, so version.json is read again after a delay.
// - The variants phase runs the automatic checks under faults a reviewer reproduced: the wrong-hash URLs
//   aborted at the network, the signals-core UMD answering 404, db arriving after the 10 s limit, failing
//   run-document writes, a host import map ahead of the page's, Resource Timing sizes hidden, and the canary
//   rule not declared. Each must give inconclusive or fail, never a pass.
// - The main probe's fake store is kept in sessionStorage across the reload, as the real store survives one;
//   the db size probe's store is in memory, and a new browser context gives a fresh one.
// - Every check id has an expectation below; an id this file does not know fails the run, so a new check
//   needs an expectation before the test passes again. Expected statuses are for this Chromium and this
//   emulation, not for the iPhone.

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createServer } from './serve.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIST = path.join(ROOT, 'dist');
const NPM = path.join(ROOT, 'npm');
const COMPARE = path.join(ROOT, 'compare');
const PLAYWRIGHT = path.join(ROOT, '..', '..', 'node_modules', 'playwright-core', 'index.mjs');
const VIEWER = 'u-test-owner';
const VIEWPORT = { width: 390, height: 844 };
const AUTO_WAIT_MS = 120_000;
const DOC_BYTES = 196_608;
const DOC_SLACK = 64;
const STATUS_BYTES = 6144;
const AUTO_KINDS = new Set(['auto', 'tool']);
const TYPES = { '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8', '.cjs': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8' };
const SHOTS = {
  light: path.join(COMPARE, 'probe-390-light.png'),
  dark: path.join(COMPARE, 'probe-390-dark.png'),
  katex: path.join(COMPARE, 'katex-html.png'),
  mathml: path.join(COMPARE, 'mathml-chromium.png'),
};

const started = Date.now();
const rows = [];
const notes = [];
const say = line => console.log(`[${((Date.now() - started) / 1000).toFixed(1)}s] ${line}`);
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const clip = (s, n) => { const t = String(s ?? ''); return t.length > n ? `${t.slice(0, n - 3)}...` : t; };
const domId = s => s.replace(/[^A-Za-z0-9_-]/g, '-');
const errText = e => (e instanceof Error ? `${e.name}: ${e.message.split('\n')[0]}` : String(e));

// The republish panel's copyable line and the line just above it.
const quoteAndPrompt = page => page.evaluate(() => {
  const q = document.querySelector('.rp-text .quote');
  return { quote: q?.textContent ?? null, prompt: q?.previousElementSibling?.textContent ?? null };
});

function expectRow(group, id, ok, { kind = '', status = '', want = '', summary = '' } = {}) {
  rows.push({ group, id, kind, status, want, ok: !!ok, summary: String(summary).replace(/\s+/g, ' ') });
  if (!ok) say(`UNEXPECTED ${group} / ${id}: ${status ? `${status}, wanted ${want}. ` : ''}${clip(summary, 400)}`);
}

// ---- expectations: statuses this Chromium and this emulation should give, and a test of the raw evidence
// (true when it holds; a string says what is wrong)

const EXPECT = {
  'cdn.bootstrap-map': { want: ['pass'], data: d => (d.lockUrl && d.moduleResolvesPreact?.url === d.lockUrl && d.mapCount === 1) || `preact went to ${d.moduleResolvesPreact?.url}` },
  'cdn.static-import': { want: ['pass'], data: d => Object.values(d.resolution ?? {}).length === 4 && Object.values(d.resolution).every(r => r.resolvedUrl === r.lockUrl) || 'a specifier did not resolve to its locked URL' },
  'cdn.load-cost': { want: ['info'], data: d => d.requests > 0 || 'no CDN request was counted' },
  'cdn.integrity-enforced': { want: ['pass'], data: d => (d.bytesArrivedAndRefused === true && d.sizesExposed === true && d.second?.state === 'rejected') || 'the refusal was not shown to follow the bytes' },
  'cdn.cdnjs-candidates': { want: ['info'], data: d => (d.tried > 0 && d.results.every(r => r.outcome !== 'loaded')) || 'a cdnjs candidate loaded, but cdnjs answers 404 here' },
  'cdn.module-worker': {
    want: ['pass'],
    data: d => {
      const libs = Object.values(d.libs ?? {});
      if (libs.length !== 3) return `${libs.length} libraries reported, not 3`;
      const compared = libs.filter(l => 'matchesNode' in l);
      if (d.integrityApplied !== false) return 'integrityApplied is not recorded as false';
      return (compared.length === 2 && compared.every(l => l.matchesNode === true)) || 'a worker output differs from the value computed in Node';
    },
  },
  'cdn.umd-fallback': { want: ['pass'], data: d => (d.control?.definesGlobal && d.signalRender?.updated && d.bytesArrivedAndRefused && d.bad2?.outcome === 'error') || 'the control, the signal render or the refusal evidence is missing' },
  'mathml.katex': { want: ['pass'] },
  'mathml.native-layout': { want: ['pass'] },
  'mathml.specimen': { want: ['pass'], data: d => (d.mathElements === 40 && d.errorElements === 0) || `${d.mathElements} math elements, ${d.errorElements} errors` },
  'mathml.specimen-verdict': { want: ['pass'], data: d => d.screenshots === 'Screenshots sent' || `screenshots: ${d.screenshots}` },
  'mathml.texslots': { want: ['pass'], data: d => (d.selfTest?.shown?.p?.join() === '0.9527' && d.selfTest.comparisonShown?.p?.join() === '0.9527' && d.selfTest.restored) || 'the slider self-test did not show 0.9527' },
  'mathml.texslots-verdict': { want: ['pass'], data: d => (d.sliderMoves >= 1 && d.mtextComparison && d.screenshots === 'Screenshots sent') || `slider moves ${d.sliderMoves}` },
  'mathml.htmldata': { want: ['fail'], data: d => (d.html?.withDataTerm >= 1 && d.mathml?.withDataTerm === 0) || 'the MathML or HTML reading is not what Node measured' },
  'platform.compression': { want: ['inconclusive', 'fail'] }, // the local server does not compress
  'platform.web-locks': { want: ['pass'], data: d => (d.crossAgent?.ifAvailableGotNull === true && d.crossAgent.stolen === true && d.crossAgent.workerEnded === 'AbortError') || 'the cross-agent step did not run' },
  'platform.idb-worker': { want: ['pass'], data: d => d.module?.ready?.module === true || 'the worker did not report running as a module' },
  'platform.storage-estimate': { want: ['info'] },
  'platform.inline-style': { want: ['pass'] },
  'platform.hash-routes': { want: ['pass'], data: d => (d.walkedBack?.popstate === true && d.restored === true) || 'the check did not walk back over its entries' },
  'platform.google-fonts': { want: ['fail', 'inconclusive'] }, // the emulated stylesheet is empty: no face can load
  'platform.version-json-before': { want: ['info'], data: d => d.version === 'v1' || `version.json said ${d.version}` },
  'platform.version-files': { want: ['info'], data: d => (d.present?.v1Only && d.present.bulkV1 && !d.present.v2Only && !d.present.bulkV2) || 'the v1 load did not show only v1\'s files' },
  'platform.clipboard': { want: ['pass'], data: d => (d.pastedMatches === true && !('pasted' in d)) || 'the pasted link did not match' },
  'platform.external-link': { want: ['pass'], data: d => d.clicks >= 1 || 'no click reached the link' },
  'platform.window-open': { want: ['info'], data: d => d.clicked === true || 'the button click did not reach the check' },
  'platform.file-input': { want: ['pass'], data: d => d.bytesRead === 64 || `read ${d.bytesRead} bytes` },
  'platform.back-gesture': { want: ['pass'] },
  'platform.version-json-after': { want: ['pass'], data: d => (d.defaultCache?.version === 'v2' && d.readings?.length >= 2 && d.readings[0].defaultCache === 'v1') || `readings ${JSON.stringify(d.readings)}` },
  'platform.version-scoping': {
    want: ['info'],
    data: d => {
      const f = d.files ?? {};
      const ok = f['v1-only']?.status === 404 && !f['v1-only'].present && f['v2-only']?.status === 200 && f['v2-only'].present
        && f['bulk-v1']?.status === 404 && f['bulk-v2']?.status === 200;
      return ok || `v1-only HTTP ${f['v1-only']?.status}, v2-only HTTP ${f['v2-only']?.status}, bulk ${f['bulk-v1']?.status}/${f['bulk-v2']?.status}`;
    },
  },
  'platform.reload': { want: ['info'], data: d => (d.loaded === 'v2' && d.from === 'v1' && d.versionJson?.version === 'v2') || `loaded ${d.loaded} from ${d.from}` },
  'platform.publish-omit-page': { want: ['info'] },
  'platform.null-removals': { want: ['info'] },
  'caps.user': { want: ['pass'], data: d => (d.id?.length === VIEWER.length && d.me?.nameNonEmpty === true && d.profiles?.nameNonEmpty === true) || 'the user readings are not what the fake gave' },
  'caps.permissions': { want: ['info'], data: d => d.named?.db === 'granted' || `db state ${d.named?.db}` },
  'caps.db-roundtrip': { want: ['pass'] },
  'caps.db-rules': {
    want: ['pass'],
    data: d => (['notMe', 'canaryNotMe'].every(k => d.outcomes?.[k]?.set?.error?.code === 'invalid_argument') && ['own', 'board', 'meta', 'canaryOwn'].every(k => d.outcomes[k]?.readBack === true) && d.canaryDeclared === true) || 'the six cases did not meet the fake as written',
  },
  'caps.meta-release': { want: ['pass'], data: d => (!!d.fresh && d.fresh.index > 0 && d.fresh.wasFirstDelivery === false && d.corroborated === true && d.watch?.resubscribes?.length === 1) || 'no fresh delivery after the first, no same-clock corroboration, or no resubscription' },
  'caps.sample-consent': { want: ['pass'], data: d => (d.saidReady === true && d.stateBefore === 'prompt' && d.stateAfter === 'granted' && !('text' in d)) || 'the consent path was not shown' },
  'caps.sample-limits': { want: ['info'] },
  'caps.sample-streaming': {
    want: ['pass'],
    data: d => (d.deliveriesBeforeResolve === 3 && d.deliveriesAfterResolve === 0 && d.textEqualsDeltasSoFar && d.lastTextEqualsResult) || 'the deliveries do not match the three the fake made',
  },
  'caps.sample-tiers': { want: ['pass'] },
  'caps.sample-abort': { want: ['pass'], data: d => (d.deltasBeforeAbort === 1 && d.deltasAfterAbort === 0) || `deltas ${d.deltasBeforeAbort} before, ${d.deltasAfterAbort} after the abort` },
  'caps.sample-tools': { want: ['pass'], data: d => (d.executeCalls === 1 && !('text' in d)) || `execute ran ${d.executeCalls} times` },
};

function judge(group, id, r, kind, override) {
  const e = override ?? EXPECT[id];
  if (!e) return expectRow(group, id, false, { kind, status: r?.status ?? 'none', want: 'listed in test.mjs', summary: `This check has no expectation in tools/test.mjs. ${r?.summary ?? ''}` });
  const want = e.want.join('|');
  if (!r) return expectRow(group, id, false, { kind, status: 'none', want, summary: 'No result was recorded.' });
  let ok = e.want.includes(r.status);
  let why = '';
  if (ok && e.data) {
    if (r.data?.truncated === true) {
      ok = false;
      why = 'The data was cut to a preview, so its evidence could not be tested.';
    } else {
      let v;
      try {
        v = e.data(r.data ?? {});
      } catch (err) {
        v = `the evidence test threw ${errText(err)}`;
      }
      if (v !== true) {
        ok = false;
        why = `Evidence: ${typeof v === 'string' ? v : 'the test failed'}.`;
      }
    }
  }
  return expectRow(group, id, ok, { kind, status: r.status, want, summary: why ? `${why} ${r.summary}` : r.summary });
}

// ---- the fake window.claude, injected before any page script (serialised: no outer references)

function fakeClaude(opts) {
  if (location.hostname !== '127.0.0.1') return;
  const VIEWER_ID = opts.viewerId;
  const LATENCY = opts.latencyMs;
  const STEP = opts.sampleStepMs;
  const SEGMENT = /^[A-Za-z0-9_\-.~:@+]+$/;
  const DOC_MAX = 256 * 1024;
  const SUB_MAX = 64;
  const enc = new TextEncoder();
  const bytes = s => enc.encode(s).length;
  const later = (fn, ms = LATENCY) => setTimeout(fn, ms);
  const wait = (ms = LATENCY) => new Promise(resolve => setTimeout(resolve, ms));
  const fail = (code, message, extra) => Object.assign({ code, message }, extra);
  const log = { use: [], memberReads: [], writes: [], overlaps: [], rejections: [], sample: [], subscriptions: 0, persistError: null, writeFaults: 0, cacheGets: 0, subFaults: [] };
  const subFaults = (opts.subscribeFaults ?? []).map(f => ({ ...f, used: false }));
  const faults = { quota: null, exhaust: null, creates: {} };
  const writeFaults = opts.writeFaults ? { ...opts.writeFaults, left: opts.writeFaults.count } : null;
  let cacheGets = opts.cacheFirstGets ?? 0;

  // The store: path -> JSON text. The main probe keeps it in sessionStorage across a reload.
  const store = new Map();
  if (opts.persistKey) {
    try {
      const raw = sessionStorage.getItem(opts.persistKey);
      if (raw) for (const [p, j] of JSON.parse(raw)) store.set(p, j);
    } catch (e) {
      log.persistError = String(e);
    }
  }
  const persist = () => {
    if (!opts.persistKey) return;
    try {
      sessionStorage.setItem(opts.persistKey, JSON.stringify([...store]));
    } catch (e) {
      log.persistError = String(e);
    }
  };
  // Documents a writer left before this page first loaded (seeded only into an empty store).
  if (opts.seed && store.size === 0) {
    for (const [p, d] of opts.seed) store.set(p, JSON.stringify(d));
    persist();
  }

  const parse = (p, kind) => {
    if (typeof p !== 'string' || !p) throw new TypeError(`${kind}(): the path must be a non-empty string`);
    if (bytes(p) > 1000) throw new TypeError(`${kind}(): the path is over 1000 bytes`);
    const segs = p.split('/');
    if (segs.length > 16) throw new TypeError(`${kind}(): the path has more than 16 segments`);
    for (const s of segs) {
      if (!SEGMENT.test(s) || s === '.' || s === '..' || bytes(s) > 200) throw new TypeError(`${kind}(): the segment ${JSON.stringify(s)} breaks the path grammar`);
    }
    if ((segs.length % 2 === 0) !== (kind === 'doc')) throw new TypeError(`${kind}(): ${p} has ${segs.length} segments, so it is not a ${kind === 'doc' ? 'document' : 'collection'} path`);
    return segs;
  };
  // The {self} rules: under each prefix, another viewer's subtree is hidden and unwritable, the owner included.
  const SELF_PREFIXES = (opts.selfPrefixes ?? ['data/users']).map(x => x.split('/'));
  const hidden = segs => SELF_PREFIXES.some(pre => segs.length > pre.length && pre.every((x, i) => segs[i] === x) && segs[pre.length] !== VIEWER_ID);
  const depth = v => (v && typeof v === 'object' ? 1 + Object.values(v).reduce((m, x) => Math.max(m, depth(x)), 0) : 0);
  const freeze = o => {
    if (o && typeof o === 'object') {
      Object.freeze(o);
      for (const v of Object.values(o)) freeze(v);
    }
    return o;
  };
  const META = Object.freeze({ fromCache: false, hasPendingWrites: false });
  const CACHED = Object.freeze({ fromCache: true, hasPendingWrites: false });
  const snap = (p, json, metadata = META) => Object.freeze({
    id: p.slice(p.lastIndexOf('/') + 1),
    exists: json != null,
    data: () => (json == null ? undefined : freeze(JSON.parse(json))),
    metadata,
  });
  const visible = (p, segs) => (hidden(segs) ? null : store.get(p) ?? null);
  const parentOf = p => p.slice(0, p.lastIndexOf('/'));

  // A body is serialised at call time, as the platform reads its arguments once.
  const body = data => {
    if (!data || typeof data !== 'object' || Array.isArray(data)) return { error: fail('invalid_argument', 'The body must be a JSON object.') };
    let json;
    try {
      json = JSON.stringify(data);
    } catch (e) {
      return { error: fail('transform_error', `The body could not be prepared: ${e.message}`) };
    }
    if (bytes(json) > DOC_MAX) return { error: fail('invalid_argument', `The document is ${bytes(json)} bytes, over 256 KiB.`) };
    if (depth(data) > 32) return { error: fail('invalid_argument', 'The document is more than 32 levels deep.') };
    return { json };
  };

  const docSubs = new Map();
  const querySubs = new Set();
  const notify = p => {
    for (const l of docSubs.get(p) ?? []) later(l.deliver);
    const c = parentOf(p);
    for (const q of querySubs) if (q.cpath === c) later(q.deliver);
  };

  const childPaths = cpath => {
    const n = cpath.split('/').length + 1;
    return [...store.keys()].filter(p => p.startsWith(`${cpath}/`) && p.split('/').length === n);
  };
  function createFault(p) {
    if (store.has(p)) return null;
    const c = parentOf(p);
    faults.creates[c] = (faults.creates[c] ?? 0) + 1;
    const ex = faults.exhaust;
    if (ex && ex.collection === c && ex.remaining > 0 && (ex.always ? faults.creates[c] >= ex.atCreate : faults.creates[c] === ex.atCreate)) {
      if (!ex.always) ex.remaining -= 1;
      return fail('resource_exhausted', 'Too many writes at once (an injected test fault).');
    }
    const q = faults.quota;
    if (q && q.collection === c && childPaths(c).length >= q.max) return fail(q.code, q.message);
    return null;
  }

  const inflight = new Map();
  function write(p, segs, op, prepared, apply) {
    const rec = { path: p, op, t: Math.round(performance.now()), wall: Date.now() };
    log.writes.push(rec);
    if (inflight.get(p)) log.overlaps.push({ path: p, op, t: rec.t });
    inflight.set(p, (inflight.get(p) ?? 0) + 1);
    return (async () => {
      try {
        await wait();
        if (writeFaults && writeFaults.left > 0 && op === 'set' && p.startsWith(writeFaults.prefix)) {
          writeFaults.left -= 1;
          log.writeFaults += 1;
          throw fail(writeFaults.code, 'An injected write fault.');
        }
        if (prepared?.error) throw prepared.error;
        if (hidden(segs)) throw fail('invalid_argument', `This viewer cannot write ${p}.`);
        rec.bytes = apply();
        notify(p);
        persist();
      } catch (e) {
        rec.rejected = e?.code ?? String(e);
        log.rejections.push({ path: p, op, code: rec.rejected });
        throw e;
      } finally {
        inflight.set(p, inflight.get(p) - 1);
      }
    })();
  }

  const merge = (base, patch) => {
    for (const [k, v] of Object.entries(patch)) {
      base[k] = v && typeof v === 'object' && !Array.isArray(v) && base[k] && typeof base[k] === 'object' && !Array.isArray(base[k]) ? merge(base[k], v) : v;
    }
    return base;
  };

  function subscribe(map, key, deliver, error) {
    if (log.subscriptions >= SUB_MAX) {
      later(() => error?.(fail('resource_exhausted', 'More than 64 subscriptions in this view.')));
      return () => {};
    }
    log.subscriptions += 1;
    const l = { closed: false, deliver: () => { if (!l.closed) deliver(); } };
    if (map instanceof Map) {
      if (!map.has(key)) map.set(key, new Set());
      map.get(key).add(l);
    } else {
      l.cpath = key;
      map.add(l);
    }
    later(l.deliver);
    return () => {
      if (l.closed) return;
      l.closed = true;
      log.subscriptions -= 1;
      if (map instanceof Map) map.get(key)?.delete(l);
      else map.delete(l);
    };
  }
  const safely = (fn, arg) => {
    try {
      fn(arg);
    } catch (e) {
      console.error('a snapshot listener threw', e);
    }
  };

  function docRef(p) {
    const segs = parse(p, 'doc');
    return Object.freeze({
      id: segs[segs.length - 1],
      path: p,
      get: () => wait().then(() => {
        if (cacheGets > 0) {
          cacheGets -= 1;
          log.cacheGets += 1;
          return snap(p, null, CACHED);
        }
        return snap(p, visible(p, segs));
      }),
      set(data) {
        const b = body(data);
        return write(p, segs, 'set', b, () => {
          const f = createFault(p);
          if (f) throw f;
          store.set(p, b.json);
          return bytes(b.json);
        });
      },
      update(data) {
        const b = body(data);
        return write(p, segs, 'update', b, () => {
          if (!store.has(p)) throw fail('invalid_argument', `update() needs ${p} to exist.`);
          const json = JSON.stringify(merge(JSON.parse(store.get(p)), JSON.parse(b.json)));
          if (bytes(json) > DOC_MAX) throw fail('invalid_argument', 'The merged document is over 256 KiB.');
          store.set(p, json);
          return bytes(json);
        });
      },
      delete: () => write(p, segs, 'delete', null, () => { store.delete(p); return 0; }),
      acquire: o => wait().then(() => ({ acquired: true, version: 1, expiresAt: new Date(Date.now() + (o?.ttlMs || 30000)).toISOString(), holder: o?.holder })),
      onSnapshot: (next, error) => {
        const unsub = subscribe(docSubs, p, () => safely(next, snap(p, visible(p, segs))), error);
        // An injected fault ends the first subscription to this path after its first delivery.
        const f = subFaults.find(x => x.path === p && !x.used);
        if (f) {
          f.used = true;
          setTimeout(() => {
            unsub();
            log.subFaults.push(`${p} ${f.code}`);
            error?.(fail(f.code, 'An injected listener fault.'));
          }, f.afterMs ?? 60);
        }
        return unsub;
      },
      collection: sub => collRef(`${p}/${sub}`),
    });
  }

  const OPS = {
    '==': (a, b) => a === b, '!=': (a, b) => a !== b, '<': (a, b) => a < b, '<=': (a, b) => a <= b, '>': (a, b) => a > b, '>=': (a, b) => a >= b,
    in: (a, b) => Array.isArray(b) && b.includes(a), 'not-in': (a, b) => Array.isArray(b) && !b.includes(a), 'array-contains': (a, b) => Array.isArray(a) && a.includes(b),
  };
  function query(cpath, spec) {
    const run = () => {
      if (spec.limit !== null && !(Number.isInteger(spec.limit) && spec.limit >= 1 && spec.limit <= 1000)) throw fail('invalid_argument', 'limit() takes 1 to 1000.');
      if (spec.filters.length > 10 || spec.filters.some(f => !OPS[f.op])) throw fail('invalid_argument', 'A filter is not supported.');
      let docs = childPaths(cpath).filter(p => !hidden(p.split('/'))).map(p => ({ p, j: store.get(p), v: JSON.parse(store.get(p)) }));
      docs = docs.filter(d => spec.filters.every(f => OPS[f.op](d.v[f.field], f.value)));
      const idOf = d => d.p.slice(d.p.lastIndexOf('/') + 1);
      docs.sort((a, b) => {
        if (spec.order) {
          const [x, y] = [a.v[spec.order.field], b.v[spec.order.field]];
          if (x !== y) return (x === undefined ? 1 : y === undefined ? -1 : x < y ? -1 : 1) * (spec.order.dir === 'desc' && x !== undefined && y !== undefined ? -1 : 1);
        }
        return idOf(a) < idOf(b) ? -1 : idOf(a) > idOf(b) ? 1 : 0;
      });
      if (spec.limit !== null) docs = docs.slice(0, spec.limit);
      const snaps = docs.map(d => snap(d.p, d.j));
      return Object.freeze({ docs: snaps, size: snaps.length, empty: snaps.length === 0, docChanges: () => snaps.map((doc, i) => ({ type: 'added', doc, oldIndex: -1, newIndex: i })), metadata: META });
    };
    const next = patch => query(cpath, { ...spec, ...patch });
    return Object.freeze({
      where: (field, op, value) => next({ filters: [...spec.filters, { field, op, value }] }),
      orderBy: (field, dir = 'asc') => next({ order: { field, dir } }),
      limit: n => next({ limit: n }),
      get: () => wait().then(run),
      onSnapshot: (nextFn, error) => subscribe(querySubs, cpath, () => {
        let s;
        try {
          s = run();
        } catch (e) {
          error?.(e);
          return;
        }
        safely(nextFn, s);
      }, error),
    });
  }
  function collRef(cpath) {
    parse(cpath, 'collection');
    const q = query(cpath, { filters: [], order: null, limit: null });
    const mint = () => `id${Date.now().toString(36)}${Math.random().toString(36).slice(2, 8)}`;
    return Object.freeze({
      ...q,
      path: cpath,
      doc: id => docRef(`${cpath}/${id ?? mint()}`),
      add: async data => {
        const ref = docRef(`${cpath}/${mint()}`);
        await ref.set(data);
        return ref;
      },
    });
  }
  const db = Object.freeze({ doc: p => docRef(p), collection: p => collRef(p) });

  const NAME = 'Test Owner';
  const AVATAR = 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22/%3E';
  const SHOWN_NAME = opts.withholdNames ? '' : NAME; // '' when the scope is missing or the organisation withholds names
  const profile = id => ({ id, name: id === VIEWER_ID ? SHOWN_NAME : '', avatarUrl: AVATAR, color: '#3366cc', email: null, isMe: id === VIEWER_ID, guest: false });
  const user = Object.freeze({
    isOwner: async () => true,
    canEdit: async () => true,
    can: async name => ['data.write', 'files.write', 'assets.write'].includes(name),
    id: async () => VIEWER_ID,
    me: async () => ({ id: VIEWER_ID, name: SHOWN_NAME, avatarUrl: AVATAR, color: '#3366cc', email: null, isOwner: true, canEdit: true }),
    profiles: async ids => Object.fromEntries([...new Set([].concat(ids))].map(id => [id, profile(String(id))])),
    name: async () => NAME,
    avatarUrl: async () => AVATAR,
    search: async () => [],
    email: async () => null,
  });

  const STATES = { db: 'granted', user: 'granted', permissions: 'granted', sample: 'prompt' };
  const permissions = Object.freeze({
    state: async name => (name === undefined ? { ...STATES } : STATES[name] ?? 'unavailable'),
    request: async names => Object.fromEntries((names ?? Object.keys(STATES)).map(n => [n, STATES[n] === 'prompt' ? 'granted' : STATES[n] ?? 'unavailable'])),
    manage: async () => undefined,
  });

  // Three onText deliveries, then the resolve; an abort rejects cancelled at once; tools run the first tool.
  const thirds = s => {
    const a = Math.ceil(s.length / 3);
    const b = Math.ceil((2 * s.length) / 3);
    return [s.slice(0, a), s.slice(a, b), s.slice(b)].filter(Boolean);
  };
  const replyFor = prompt => (/single word: ready/i.test(prompt) ? 'ready'
    : /single word: ok/i.test(prompt) ? 'ok.'
      : 'Rain smells because dry ground holds oils from plants and compounds made by soil bacteria. When drops hit the ground they trap air, which bursts and carries the scent up.');
  function sample(input, options) {
    return new Promise((resolve, reject) => {
      const o = options ?? {};
      const prompt = typeof input === 'string' ? input : JSON.stringify(input);
      const rec = { tier: o.modelTier ?? 'default', cache: o.cache === undefined ? 'omitted' : JSON.stringify(o.cache), tools: Array.isArray(o.tools) ? o.tools.length : 0, onText: typeof o.onText === 'function', signal: !!o.signal, deliveries: 0, outcome: null };
      log.sample.push(rec);
      let text = '';
      let settled = false;
      const done = (ok, v) => {
        if (settled) return;
        settled = true;
        rec.outcome = ok ? 'resolved' : v.code;
        o.signal?.removeEventListener?.('abort', onAbort);
        if (ok) resolve(v);
        else reject(v);
      };
      const onAbort = () => done(false, fail('cancelled', 'The call was cancelled.', { text }));
      const invalid = rec.tools && o.cache !== undefined && o.cache !== false ? 'cache with tools'
        : o.modelTier !== undefined && !['quick', 'default', 'complex'].includes(o.modelTier) ? 'modelTier'
          : o.signal !== undefined && !(o.signal instanceof AbortSignal) ? 'signal' : null;
      if (invalid) return later(() => done(false, fail('invalid_request', `The option ${invalid} is not valid.`)), 0);
      if (o.signal?.aborted) return later(onAbort, 0);
      o.signal?.addEventListener('abort', onAbort, { once: true });
      (async () => {
        await wait(STEP);
        let reply = replyFor(prompt);
        if (rec.tools) {
          const ctl = new AbortController();
          o.signal?.addEventListener('abort', () => ctl.abort(), { once: true });
          let out;
          try {
            out = await o.tools[0].execute({}, { signal: ctl.signal });
          } catch (e) {
            out = `Error: ${e?.message ?? e}`;
          }
          if (settled) return;
          const value = out && typeof out === 'object' && 'value' in out ? out.value : out;
          reply = `The value is ${typeof value === 'string' ? value : JSON.stringify(value)}.`;
        }
        for (const delta of thirds(reply)) {
          await wait(STEP);
          if (settled) return;
          text += delta;
          rec.deliveries += 1;
          if (rec.onText) {
            try {
              o.onText({ text, delta });
            } catch (e) {
              console.error('onText threw', e);
            }
          }
        }
        await wait(STEP);
        STATES.sample = 'granted'; // the consent the first call asked for now governs later calls
        done(true, { text, truncated: false, modelTierApplied: rec.tier });
      })().catch(e => done(false, fail('unavailable', String(e))));
    });
  }
  sample.limits = () => Promise.resolve({ maxPromptBytes: 262144, images: false });
  sample.json = (input, options) => sample(input, options).then(r => JSON.parse(r.text));
  Object.freeze(sample);

  const served = { db, user, permissions, sample };
  const memo = {};
  function use(name) {
    log.use.push(String(name));
    if (!Object.hasOwn(served, name)) return Promise.resolve(null);
    memo[name] ??= new Promise(resolve => later(() => resolve(served[name]), name === 'db' && opts.dbDelayMs ? opts.dbDelayMs : LATENCY));
    return memo[name];
  }
  const claude = new Proxy(Object.freeze({ use }), {
    get(target, key, receiver) {
      if (key !== 'use') log.memberReads.push(String(key));
      return Reflect.get(target, key, receiver);
    },
  });
  Object.defineProperty(window, 'claude', { value: claude, enumerable: true });

  // The test's hook: reads and writes from Node act as another writer (Claude's ArtifactData).
  Object.defineProperty(window, '__fakeClaude', {
    value: Object.freeze({
      log,
      faults,
      configure(c) {
        faults.quota = c.quota ?? null;
        faults.exhaust = c.exhaust ? { remaining: 1, ...c.exhaust } : null;
        faults.creates = {};
        return true;
      },
      get: p => (store.has(p) ? JSON.parse(store.get(p)) : null),
      bytes: p => (store.has(p) ? bytes(store.get(p)) : null),
      set(p, data) {
        store.set(p, JSON.stringify(data));
        notify(p);
        persist();
        return true;
      },
      delete(p) {
        const had = store.delete(p);
        if (had) {
          notify(p);
          persist();
        }
        return had;
      },
      paths: prefix => [...store.keys()].filter(p => !prefix || p.startsWith(prefix)).sort(),
    }),
  });
}

// ---- browser plumbing

function chromiumPath() {
  if (process.env.ZQ_CHROMIUM) return process.env.ZQ_CHROMIUM;
  const base = '/opt/pw-browsers';
  if (!fs.existsSync(base)) return null;
  for (const d of fs.readdirSync(base).filter(x => x.startsWith('chromium-')).sort()) {
    const exe = path.join(base, d, 'chrome-linux', 'chrome');
    if (fs.existsSync(exe)) return exe;
  }
  return null;
}

const traffic = { npm: new Map(), npmByRequester: {}, npmMissing: [], cdnjs: [], fonts: [], outside: [] };
const labels = new WeakMap();
const pageProblems = [];
const consoleErrors = [];
const popups = [];

// The page that made a request. A popup's first navigation has no frame yet, so it is named 'new page'.
function requester(req) {
  try {
    return labels.get(req.frame().page()) ?? 'unlabelled page';
  } catch (e) {
    return req.isNavigationRequest() ? 'new page' : `no frame (${clip(errText(e), 40)})`;
  }
}

function serveNpm(route, u, req, { tao = true } = {}) {
  const from = requester(req);
  const notFound = why => {
    traffic.npmMissing.push(`${u.pathname} (${why})`);
    return route.fulfill({ status: 404, contentType: 'text/plain', headers: { 'access-control-allow-origin': '*' }, body: 'Not found\n' });
  };
  const m = /^\/npm\/((?:@[^/@]+\/)?[^/@]+)@([^/]+)\/(.+)$/.exec(u.pathname);
  if (!m) return notFound('not a package path');
  const base = path.join(NPM, `${m[1].replace(/^@/, '').replace('/', '-')}-${m[2]}`, 'package');
  let rel;
  try {
    rel = decodeURIComponent(m[3]);
  } catch (e) {
    return notFound(errText(e));
  }
  const file = path.resolve(base, rel);
  if (!file.startsWith(base + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) return notFound('no such npm file');
  const key = `${m[1]}@${m[2]}`;
  traffic.npm.set(key, (traffic.npm.get(key) ?? 0) + 1);
  traffic.npmByRequester[from] = (traffic.npmByRequester[from] ?? 0) + 1;
  return route.fulfill({
    status: 200,
    headers: {
      'content-type': TYPES[path.extname(file)] ?? 'application/octet-stream',
      'access-control-allow-origin': '*',
      ...(tao ? { 'timing-allow-origin': '*' } : {}), // jsDelivr sends it [recalled]
      'x-content-type-options': 'nosniff',
    },
    body: fs.readFileSync(file),
  });
}

function routeRequest(route) {
  const req = route.request();
  let u;
  try {
    u = new URL(req.url());
  } catch (e) {
    traffic.outside.push({ from: requester(req), url: clip(req.url(), 120), why: errText(e) });
    return route.abort('addressunreachable');
  }
  if ((u.protocol === 'http:' && u.hostname === '127.0.0.1') || u.protocol === 'file:') return route.continue();
  if (u.protocol === 'https:' && u.hostname === 'cdn.jsdelivr.net') return serveNpm(route, u, req);
  if (u.hostname === 'cdnjs.cloudflare.com') {
    traffic.cdnjs.push(u.pathname);
    return route.fulfill({ status: 404, contentType: 'text/plain', headers: { 'access-control-allow-origin': '*' }, body: 'Not found\n' });
  }
  if (u.hostname === 'fonts.googleapis.com') {
    traffic.fonts.push(`googleapis ${u.pathname}`);
    return route.fulfill({ status: 200, contentType: 'text/css; charset=utf-8', headers: { 'access-control-allow-origin': '*' }, body: '' });
  }
  if (u.hostname === 'fonts.gstatic.com') {
    traffic.fonts.push(`gstatic ${u.pathname}`);
    return route.fulfill({ status: 404, contentType: 'text/plain', headers: { 'access-control-allow-origin': '*' }, body: 'Not found\n' });
  }
  traffic.outside.push({ from: requester(req), url: `${u.protocol}//${u.host}${u.pathname}` });
  return route.abort('blockedbyclient');
}

function watch(page, label) {
  labels.set(page, label);
  page.on('pageerror', e => pageProblems.push({ label, text: clip(errText(e), 300) }));
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push({ label, text: clip(m.text(), 240) }); });
}

async function newContext(browser, { persist = false, init = null, initArg, fake: fakeOpts = {} } = {}) {
  const context = await browser.newContext({ viewport: VIEWPORT, deviceScaleFactor: 2, colorScheme: 'light', locale: 'en-GB', serviceWorkers: 'block' });
  await context.route(() => true, routeRequest);
  await context.addInitScript(fakeClaude, { viewerId: VIEWER, latencyMs: 8, sampleStepMs: 40, persistKey: persist ? '__s1fake.db' : null, selfPrefixes: ['data/users', 's1canary'], ...fakeOpts });
  if (init) await context.addInitScript(init, initArg);
  context.on('page', p => {
    p.opener().then(o => {
      if (!o) return;
      watch(p, 'popup');
      popups.push(p);
    }, e => notes.push(`could not read a new page's opener: ${errText(e)}`));
  });
  return context;
}

// ---- the main probe

const hdoc = page => page.evaluate(() => window.__s1harness.document());
const fake = (page, method, ...args) => page.evaluate(([m, a]) => window.__fakeClaude[m](...a), [method, args]);
const card = (page, id) => page.locator(`#check-${domId(id)}`);
const answer = (c, n = 0) => c.locator('.prompt .prompt-choices button').nth(n).click();

async function readCards(page) {
  return page.$$eval('article.card[id^="check-"]', cards => cards.map(c => ({
    id: c.querySelector('code.check-id')?.textContent ?? '',
    kind: c.querySelector('.chip')?.dataset.kind ?? '',
    status: c.dataset.status,
    summary: c.querySelector('.card-summary')?.textContent ?? '',
  })));
}

// Waits until the db's run document carries the harness's latest result for every id.
async function settledRunDoc(page, runPath, ids, ms = 15_000) {
  const end = Date.now() + ms;
  for (;;) {
    const [stored, live] = await page.evaluate(p => [window.__fakeClaude.get(p), window.__s1harness.document()], runPath);
    const same = !!stored && ids.every(id => live.results[id] && stored.results?.[id]?.at === live.results[id].at && stored.results[id].status === live.results[id].status);
    if (same || Date.now() > end) return { stored, live, same };
    await sleep(500);
  }
}

async function tapCheck(page, id, act, timeout = 40_000) {
  const before = (await hdoc(page)).results[id]?.at ?? null;
  const c = card(page, id);
  await c.locator('.actions .btn').click();
  if (act) await act(c);
  await page.waitForFunction(([cid, b]) => { const r = window.__s1harness.document().results[cid]; return !!r && r.at !== b; }, [id, before], { timeout, polling: 200 });
  return (await hdoc(page)).results[id];
}

async function closePopups() {
  for (const p of popups.splice(0)) {
    await p.close().catch(e => notes.push(`a popup did not close: ${errText(e)}`));
  }
}

async function probePhase(browser, server) {
  const G1 = 'probe v1';
  // An earlier run's signals, written by a machine whose clock is an hour ahead of the phone's.
  const future = new Date(Date.now() + 3_600_000).toISOString();
  const seed = [['ops/s1-republished', { to: 'v2', at: future }], ['meta/release', { release: 's1-v2', at: future }]];
  // Both watches lose their first subscription: the harness's to an unknown code, the release watch to a dead bridge.
  const subscribeFaults = [{ path: 'ops/s1-republished', code: 'queue_overflow' }, { path: 'meta/release', code: 'unavailable' }];
  const context = await newContext(browser, { persist: true, fake: { seed, subscribeFaults } });
  const page = await context.newPage();
  watch(page, 'probe');
  try {
    await page.goto(server.url);
    await page.waitForFunction(() => !!window.__s1harness, null, { timeout: 30_000 });
    const runId = await page.evaluate(() => window.__s1harness.runId);
    const runPath = `ops/s1-run-${runId}`;
    say(`probe v1 loaded, run ${runId}; waiting for the automatic checks`);
    const finished = await page.evaluate(ms => Promise.race([window.__s1harness.autoDone, new Promise(r => setTimeout(() => r(false), ms))]), AUTO_WAIT_MS);
    expectRow(G1, 'auto checks finish in 120 s', finished === true, { summary: finished === true ? 'autoDone resolved' : 'autoDone did not resolve within 120 s' });
    const readyQuote = await quoteAndPrompt(page);
    expectRow(G1, 'ready quote sits under its prompt', readyQuote.quote === 'S1 ready for republish' && /tell Claude:$/.test(readyQuote.prompt), { summary: JSON.stringify(readyQuote) });

    const cards = await readCards(page);
    const kindOf = Object.fromEntries(cards.map(c => [c.id, c.kind]));
    const autoIds = cards.filter(c => AUTO_KINDS.has(c.kind)).map(c => c.id);
    const first = await settledRunDoc(page, runPath, autoIds);
    expectRow(G1, 'run doc holds every auto result', first.same, { summary: first.same ? `${autoIds.length} auto and tool results in ${runPath}` : 'the stored run document lags the harness after 15 s' });
    const extras = Object.keys(first.live.results).filter(id => !kindOf[id]);
    expectRow(G1, 'no module or definition errors', extras.length === 0, { summary: extras.length ? extras.map(id => `${id}: ${first.live.results[id].summary}`).join('; ') : `modules: ${Object.entries(first.live.modules).map(([m, v]) => `${m} ${v.ok ? v.checks.length : 'failed'}`).join(', ')}` });
    for (const id of autoIds) judge(G1, id, first.stored?.results?.[id], kindOf[id]);
    const unknown = cards.filter(c => !EXPECT[c.id]).map(c => c.id);
    if (unknown.length) expectRow(G1, 'every check has an expectation', false, { summary: unknown.join(', ') });

    await card(page, 'mathml.specimen').screenshot({ path: SHOTS.mathml });
    say(`wrote ${path.relative(ROOT, SHOTS.mathml)}`);

    // A stale signal from a clock ahead of the phone must not start the republish checks.
    const early = await page.evaluate(() => window.__s1harness.document().republish);
    expectRow(G1, 'stale signal ignored at load', early.phase !== 'arrived' && !!early.stale, { summary: `phase ${early.phase}, stale ${JSON.stringify(early.stale?.at ?? null)}` });
    const resub = await page.waitForFunction(() => window.__s1harness.document().republish.subscriptions >= 2, null, { timeout: 15_000, polling: 250 }).then(() => true, () => false);
    const subs = await page.evaluate(() => window.__s1harness.document().republish.subscriptions);
    expectRow(G1, 'signal watch subscribed again', resub, { summary: `${subs} subscriptions to ops/s1-republished after a queue_overflow` });
    const limits = await page.evaluate(() => window.__s1harness.limits());
    const repLimits = cards.filter(c => c.kind === 'republish').map(c => [c.id, limits[c.id]]);
    expectRow(G1, 'republish limits cover their waits', limits['caps.meta-release'] >= 100_000 && repLimits.every(([, ms]) => ms >= 100_000), { summary: repLimits.map(([id, ms]) => `${id} ${ms / 1000} s`).join(', ') });

    // The Claude app version and iPhone model fields reach the run document.
    await page.fill('#s1-app-version', '1.0.0 (local test)');
    await page.fill('#s1-device-model', 'Chromium (local test)');
    await page.locator('.appver .btn').click();

    // Manual checks: Run, do what the prompt asks, then the first choice.
    say('driving the manual checks');
    const tapped = {};
    tapped['mathml.specimen-verdict'] = await tapCheck(page, 'mathml.specimen-verdict', async c => {
      await answer(c);
      await answer(c);
    });
    const noMove = await tapCheck(page, 'mathml.texslots-verdict', async c => {
      for (let i = 0; i < 4; i++) await answer(c);
    });
    judge(G1, 'mathml.texslots-verdict', noMove, 'manual', { want: ['inconclusive'], data: d => d.sliderMoves === 0 || `${d.sliderMoves} moves` });
    rows.at(-1).id = 'mathml.texslots-verdict (slider not moved)';
    tapped['mathml.texslots-verdict'] = await tapCheck(page, 'mathml.texslots-verdict', async c => {
      await c.locator('.prompt').waitFor();
      const slider = c.locator('input[type=range]');
      await slider.focus();
      await page.keyboard.press('ArrowRight');
      await page.keyboard.press('ArrowRight');
      for (let i = 0; i < 4; i++) await answer(c);
    });
    const untapped = await tapCheck(page, 'platform.external-link', c => answer(c));
    judge(G1, 'platform.external-link', untapped, 'manual', {
      want: ['inconclusive'],
      data: d => d.clicks === 0 || `${d.clicks} clicks`,
    });
    rows.at(-1).id = 'platform.external-link (link not tapped)';
    const nothing = await tapCheck(page, 'platform.external-link', c => answer(c, 2));
    judge(G1, 'platform.external-link', nothing, 'manual', { want: ['inconclusive'], data: d => (d.clicks === 0 && d.answer === 'Nothing happened') || `${d.clicks} clicks` });
    rows.at(-1).id = 'platform.external-link (nothing, no click)';
    tapped['platform.external-link'] = await tapCheck(page, 'platform.external-link', async c => {
      await c.locator('.mount a').click();
      await sleep(300);
      await answer(c);
    });
    tapped['platform.window-open'] = await tapCheck(page, 'platform.window-open', async c => {
      await c.locator('.mount button').click();
      await answer(c);
    });
    await closePopups();
    tapped['platform.file-input'] = await tapCheck(page, 'platform.file-input', c => c.locator('.mount input[type=file]').setInputFiles({ name: 'probe.txt', mimeType: 'text/plain', buffer: Buffer.alloc(100, 0x61) }));
    tapped['platform.back-gesture'] = await tapCheck(page, 'platform.back-gesture', async c => {
      await answer(c); // Start the swipe test
      await c.locator('.prompt').waitFor();
      await page.evaluate(() => new Promise(resolve => { window.addEventListener('popstate', () => resolve(), { once: true }); history.back(); }));
      await answer(c);
    });
    tapped['platform.clipboard'] = await tapCheck(page, 'platform.clipboard', async c => {
      await c.locator('.mount button').click();
      await c.locator('.prompt textarea').fill('https://claude.ai/s1-clipboard-probe');
      await c.locator('.prompt .prompt-choices button').click();
    });
    const before = await tapCheck(page, 'platform.reload', null);
    judge(G1, 'platform.reload', before, 'manual', { want: ['skipped'] });
    rows.at(-1).id = 'platform.reload (before republish)';

    say('driving the consent checks');
    for (const id of ['caps.sample-consent', 'caps.sample-streaming', 'caps.sample-tiers', 'caps.sample-abort', 'caps.sample-tools']) {
      tapped[id] = await tapCheck(page, id, null);
    }

    // The republish: Claude's two db writes, then the emulator serves v2 8 s later (a publish still going live).
    say('emulating the republish');
    await fake(page, 'set', 'meta/release', { release: 's1-v2', at: new Date().toISOString() });
    await sleep(300);
    await fake(page, 'set', 'ops/s1-republished', { to: 'v2', at: new Date().toISOString() });
    await sleep(8000);
    const sw = await fetch(`${server.url}__switch?dir=${encodeURIComponent(path.join(DIST, 'v2'))}`, { method: 'POST' });
    expectRow(G1, 'emulator switched to dist/v2', sw.ok, { summary: `POST /__switch answered ${sw.status}` });
    const repIds = cards.filter(c => c.kind === 'republish').map(c => c.id);
    await page.waitForFunction(ids => { const r = window.__s1harness.document().results; return ids.every(id => r[id]?.trigger === 'republish'); }, repIds, { timeout: 100_000, polling: 300 });
    const panel = await page.textContent('.republish');
    expectRow(G1, 'republish panel says done', panel.includes('S1 republish checks done'), { summary: clip(panel, 200) });
    const doneQuote = await quoteAndPrompt(page);
    expectRow(G1, 'done quote sits under its prompt', doneQuote.quote === 'S1 republish checks done' && /Tell Claude:$/.test(doneQuote.prompt), { summary: JSON.stringify(doneQuote) });

    // Every v1 result, read back from the db and from the screen.
    const all = cards.map(c => c.id);
    const done = await settledRunDoc(page, runPath, all);
    const stored = done.stored;
    for (const id of [...Object.keys(tapped), ...repIds]) judge(G1, id, stored?.results?.[id], kindOf[id]);
    const screen = await readCards(page);
    const disagree = screen.filter(c => stored?.results?.[c.id]?.status !== c.status);
    expectRow(G1, 'screen and db agree', done.same && disagree.length === 0, { summary: disagree.length ? disagree.map(c => `${c.id} screen ${c.status}, db ${stored.results[c.id].status}`).join('; ') : `${screen.length} cards, every status as stored` });
    expectRow(G1, 'run doc has the contract fields', ['version', 'ua', 'viewport', 'startedAt', 'appVersion', 'deviceModel', 'results'].every(k => k in (stored ?? {})) && stored.version === 'v1' && stored.appVersion === '1.0.0 (local test)' && stored.deviceModel === 'Chromium (local test)', { summary: `version ${stored?.version}, appVersion ${JSON.stringify(stored?.appVersion)}, deviceModel ${JSON.stringify(stored?.deviceModel)}` });
    const storedText = JSON.stringify(stored ?? {});
    const leaked = ['Rain smells', 'The value is', 'soil bacteria'].filter(t => storedText.includes(t));
    expectRow(G1, 'no model output in db', leaked.length === 0, { summary: leaked.length ? `found: ${leaked.join(', ')}` : 'no reply text in the run document' });
    const runBytes = await fake(page, 'bytes', runPath);
    expectRow(G1, 'run doc under 200 KB', runBytes < 200_000, { summary: `${runBytes} bytes${stored?.truncation ? `; cut: ${stored.truncation.join('; ')}` : ''}` });
    const latest = await fake(page, 'get', 'ops/s1-latest');
    expectRow(G1, 'ops/s1-latest names the run', latest?.runId === runId && latest?.version === 'v1', { summary: JSON.stringify(latest) });

    // What the fake saw.
    const flog = await page.evaluate(() => window.__fakeClaude.log);
    expectRow(G1, 'only window.claude.use is read', flog.memberReads.length === 0, { summary: flog.memberReads.length ? `read: ${[...new Set(flog.memberReads)].join(', ')}` : `use() called for ${[...new Set(flog.use)].join(', ')}` });
    expectRow(G1, 'no overlapping writes to a doc', flog.overlaps.length === 0, { summary: flog.overlaps.length ? flog.overlaps.slice(0, 5).map(o => `${o.op} ${o.path} at ${o.t} ms`).join('; ') : `${flog.writes.length} writes, none overlapping` });
    const hw = flog.writes.filter(w => w.path.startsWith('ops/s1-run-') || w.path === 'ops/s1-latest');
    const gaps = hw.slice(1).map((w, i) => w.t - hw[i].t);
    const minGap = gaps.length ? Math.min(...gaps) : null;
    expectRow(G1, 'harness writes at most 1 a second', gaps.every(g => g >= 1000), { summary: `${hw.length} harness writes, smallest gap ${minGap} ms` });
    const leftovers = (await fake(page, 'paths', '')).filter(p => !p.startsWith('ops/s1-run-') && !['ops/s1-latest', 'ops/s1-republished', 'meta/release'].includes(p));
    expectRow(G1, 'checks deleted what they wrote', leftovers.length === 0, { summary: leftovers.length ? leftovers.join(', ') : 'only the run, latest, republish and release documents remain' });
    const rejected = flog.rejections.map(r => `${r.op} ${r.path.replace(VIEWER, '<own id>')} ${r.code}`);
    notes.push(`fake db rejections on v1: ${rejected.join('; ') || 'none'}`);
    notes.push(`sample calls on v1: ${flog.sample.map(s => `${s.tier}/${s.outcome}/${s.deliveries}`).join(', ')}`);
    expectRow(G1, 'sample calls as the checks state', flog.sample.every(s => s.outcome) && flog.sample.filter(s => s.tools).every(s => s.cache === 'omitted') && flog.sample.filter(s => !s.tools).every(s => s.cache === 'false'), { summary: `${flog.sample.length} calls; cache ${[...new Set(flog.sample.map(s => s.cache))].join(', ')}` });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expectRow(G1, 'no horizontal scroll at 390 px', overflow <= 0, { summary: `scrollWidth minus clientWidth is ${overflow} px` });

    // A full-page capture paints the sticky summary bar at the scroll position, leaving a blank band at the top.
    const flat = '.summary { position: static !important; }';
    await page.screenshot({ path: SHOTS.light, fullPage: true, style: flat });
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.screenshot({ path: SHOTS.dark, fullPage: true, style: flat });
    await page.emulateMedia({ colorScheme: 'light' });
    say(`wrote ${path.relative(ROOT, SHOTS.light)} and ${path.relative(ROOT, SHOTS.dark)}`);

    // location.reload() after the republish: a new run document on the v2 page.
    const G2 = 'probe after reload';
    say('running platform.reload');
    const rc = card(page, 'platform.reload');
    await rc.locator('.actions .btn').click();
    const loaded = page.waitForEvent('load', { timeout: 30_000 });
    await answer(rc);
    await loaded;
    await page.waitForFunction(old => !!window.__s1harness && window.__s1harness.runId !== old, runId, { timeout: 30_000 });
    const after = await page.evaluate(() => ({ runId: window.__s1harness.runId, version: window.__s1harness.version }));
    const newPath = `ops/s1-run-${after.runId}`;
    await page.waitForFunction(([p, id]) => {
      const d = window.__fakeClaude.get(p);
      return !!d?.results?.['platform.reload'] && window.__fakeClaude.get('ops/s1-latest')?.runId === id;
    }, [newPath, after.runId], { timeout: 30_000, polling: 300 });
    const doc2 = await fake(page, 'get', newPath);
    const r2 = doc2.results['platform.reload'];
    judge(G2, 'platform.reload', r2, 'manual');
    expectRow(G2, 'new run doc after the reload', after.version === 'v2' && doc2.version === 'v2' && doc2.previousRunId === runId && r2?.trigger === 'resume', { summary: `page ${after.version}, doc ${doc2.version}, previousRunId ${doc2.previousRunId === runId ? 'is the v1 run' : doc2.previousRunId}, trigger ${r2?.trigger}` });
    const oldKept = await fake(page, 'get', runPath);
    expectRow(G2, 'the v1 run doc is kept', !!oldKept?.results, { summary: oldKept ? `${Object.keys(oldKept.results).length} results in ${runPath}` : 'missing' });
    const repState = await page.evaluate(() => window.__s1harness.document().republish);
    expectRow(G2, 'old signal not taken as new', repState.phase !== 'arrived', { summary: `republish phase ${repState.phase}${repState.stale ? ', the stored signal was recognised as older' : ''}` });
    expectRow(G2, 'reload carried both markers', r2?.data?.carriers?.session === true && r2.data.carriers.hash === true && r2.data.basePath?.same === true, { summary: JSON.stringify({ carriers: r2?.data?.carriers, basePath: r2?.data?.basePath }) });
    const v2done = await page.evaluate(ms => Promise.race([window.__s1harness.autoDone, new Promise(r => setTimeout(() => r(false), ms))]), AUTO_WAIT_MS);
    expectRow(G2, 'v2 auto checks finish', v2done === true, { summary: String(v2done) });
    const v2doc = await settledRunDoc(page, newPath, ['platform.version-files']);
    judge(G2, 'platform.version-files', v2doc.stored?.results?.['platform.version-files'], 'auto', {
      want: ['pass'],
      data: d => (!d.present?.v1Only && !d.present.bulkV1 && d.present.v2Only && d.present.bulkV2) || JSON.stringify(d.present),
    });
    rows.at(-1).id = 'platform.version-files (v2 load)';

    // The back gesture when the page reloads during the check: resume says so, and the next run asks.
    say('back gesture with a reload in the middle');
    const bc = card(page, 'platform.back-gesture');
    await bc.locator('.actions .btn').click();
    await answer(bc); // Start the swipe test
    await bc.locator('.prompt').waitFor();
    const oldRun = after.runId;
    await page.reload();
    await page.waitForFunction(old => !!window.__s1harness && window.__s1harness.runId !== old, oldRun, { timeout: 30_000 });
    await page.waitForFunction(() => !!window.__s1harness.document().results['platform.back-gesture'], null, { timeout: 30_000, polling: 200 });
    const resumed = (await hdoc(page)).results['platform.back-gesture'];
    judge(G2, 'platform.back-gesture', resumed, 'manual', { want: ['inconclusive'], data: d => d.reloadedFlagSet === true || 'the reload flag was not set' });
    rows.at(-1).id = 'platform.back-gesture (reloaded mid-check)';
    const known = await tapCheck(page, 'platform.back-gesture', c => answer(c, 0));
    judge(G2, 'platform.back-gesture', known, 'manual', { want: ['fail'], data: d => (d.reloadedDuringCheck === true && d.firstAnswer === 'It closed or left the probe') || JSON.stringify(d) });
    rows.at(-1).id = 'platform.back-gesture (answer after reload)';
  } finally {
    await closePopups();
    await context.close();
  }
}

// ---- the db size probe

async function dbsizePhase(browser) {
  const G = 'dbsize';
  const server = await createServer({ root: path.join(DIST, 'dbsize') });
  const pace = o => { globalThis.__S1_TEST_PACE_MS = o.pace; globalThis.__S1_TEST_MAX_DOCS = o.max; if (o.maxPause) globalThis.__S1_TEST_MAX_PAUSE_MS = o.maxPause; };
  const stateOf = page => page.evaluate(() => document.getElementById('app')?.dataset.state ?? null);
  const waitState = (page, states, ms = 60_000) => page.waitForFunction(s => s.includes(document.getElementById('app')?.dataset.state), states, { timeout: ms, polling: 100 });
  const probeBytes = async page => (await page.evaluate(() => window.__fakeClaude.log.writes.filter(w => w.path.startsWith('probe/') && w.op === 'set' && !w.rejected).map(w => w.bytes)));
  const sizesOk = list => list.length > 0 && list.every(b => Math.abs(b - DOC_BYTES) <= DOC_SLACK);
  const open = async (opts = {}) => {
    const context = await newContext(browser, { init: opts.noPace ? null : pace, initArg: { pace: 5, max: 12, ...opts.pace }, fake: opts.fake ?? {} });
    const page = await context.newPage();
    watch(page, 'dbsize');
    await page.goto(server.url);
    return { context, page };
  };
  const startable = page => page.waitForFunction(() => { const b = document.getElementById('start'); return !!b && !b.disabled; }, null, { timeout: 30_000 });
  try {
    // Run 1: resource_exhausted once at the third create, quota_exceeded after 8 documents; clean-up starts by itself.
    let { context, page } = await open();
    await startable(page);
    await fake(page, 'configure', { quota: { collection: 'probe', max: 8, code: 'quota_exceeded', message: 'size cap' }, exhaust: { collection: 'probe', atCreate: 3 } });
    await page.click('#start');
    await waitState(page, ['clean', 'error']);
    let st = await fake(page, 'get', 'status/s1-size');
    const sizes = await probeBytes(page);
    let left = await fake(page, 'paths', 'probe/');
    expectRow(G, 'run 1 capped at 8, then cleaned', st?.outcome === 'capped' && st.state === 'clean' && st.docsWritten === 8 && st.refusedIndex === 9 && st.capMessage === 'size cap' && left.length === 0, { status: st?.state, want: 'clean', summary: `outcome ${st?.outcome}, ${st?.docsWritten} written, refused at ${st?.refusedIndex}, cap message ${JSON.stringify(st?.capMessage)}, ${left.length} documents left` });
    const exhausted = (st?.events ?? []).filter(e => e.code === 'resource_exhausted');
    expectRow(G, 'pause doubles once', st?.basePauseMs === 5 && st?.pauseMs === 10 && st?.exhaustedCount === 1 && exhausted.length === 1 && exhausted[0].pauseMs === 10, { summary: `base ${st?.basePauseMs} ms, now ${st?.pauseMs} ms, ${st?.exhaustedCount} refusals, events ${JSON.stringify(exhausted)}` });
    expectRow(G, 'bodies are 196,608 bytes', sizesOk(sizes) && sizes.length === 8, { summary: `${sizes.length} bodies: ${[...new Set(sizes)].join(', ')} bytes` });
    const statusBytes = await fake(page, 'bytes', 'status/s1-size');
    expectRow(G, 'status doc is 6,144 bytes', statusBytes === STATUS_BYTES, { summary: `${statusBytes} bytes` });
    const pill = await page.textContent('#state');
    const capShown = await page.textContent('#f-cap');
    const said = await page.textContent('#instructions');
    expectRow(G, 'screen shows the cap after clean-up', pill === 'clean' && capShown === 'size cap' && said.includes('quota_exceeded'), { summary: `pill ${JSON.stringify(pill)}, cap ${JSON.stringify(capShown)}, ${clip(said, 120)}` });
    expectRow(G, 'clean only on a definitive empty listing', st?.remainingAfterClean === 0 && st.finalListing?.fromCache === false && st.finalListing.hasPendingWrites === false, { summary: JSON.stringify(st?.finalListing) });
    await context.close();

    // Run 2: a fresh store, no faults, 12 documents.
    ({ context, page } = await open());
    await startable(page);
    await page.click('#start');
    await waitState(page, ['clean', 'error']);
    st = await fake(page, 'get', 'status/s1-size');
    const sizes2 = await probeBytes(page);
    left = await fake(page, 'paths', 'probe/');
    expectRow(G, 'run 2 done at 12, then cleaned', st?.outcome === 'done' && st.state === 'clean' && st.docsWritten === 12 && left.length === 0 && sizesOk(sizes2) && sizes2.length === 12, { status: st?.state, want: 'clean', summary: `outcome ${st?.outcome}, ${st?.docsWritten} written, ${left.length} left, bodies ${[...new Set(sizes2)].join(', ')} bytes, pause ${st?.pauseMs} ms` });
    const dlog = await page.evaluate(() => window.__fakeClaude.log);
    expectRow(G, 'dbsize reads only use', dlog.memberReads.length === 0 && dlog.overlaps.length === 0, { summary: `${dlog.memberReads.length} member reads, ${dlog.overlaps.length} overlapping writes` });
    await context.close();

    // Run 3: the store refuses every create from the second on: the run stops as throttled, not forever.
    ({ context, page } = await open({ pace: { maxPause: 40 } }));
    await startable(page);
    await fake(page, 'configure', { exhaust: { collection: 'probe', atCreate: 2, always: true } });
    await page.click('#start');
    await waitState(page, ['error', 'clean', 'done', 'capped'], 30_000);
    st = await fake(page, 'get', 'status/s1-size');
    expectRow(G, 'run 3 stops as throttled', st?.state === 'error' && st.lastError?.code === 'throttled' && st.lastError.i === 2 && st.docsWritten === 1, { status: st?.state, want: 'error', summary: `${st?.lastError?.code} at ${st?.lastError?.i}, ${st?.exhaustedCount} refusals, pause ${st?.pauseMs} ms` });
    const canResume = await page.evaluate(() => !document.getElementById('resume').disabled);
    expectRow(G, 'resume offered after throttling', canResume, { summary: `Resume ${canResume ? 'enabled' : 'disabled'}` });
    await fake(page, 'configure', {});
    await page.click('#clean');
    await waitState(page, ['clean', 'error']);
    left = await fake(page, 'paths', 'probe/');
    expectRow(G, 'run 3 cleans up', (await stateOf(page)) === 'clean' && left.length === 0, { summary: `${left.length} left` });
    await context.close();

    // Run 4: a saved status and two cached reads at load: the page reads again and never offers Start.
    const saved = {
      state: 'clean', phase: 'clean', outcome: 'capped', docsWritten: 8, bytesWritten: 8 * DOC_BYTES, maxDocs: 12, docBytes: DOC_BYTES,
      basePauseMs: 5, pauseMs: 10, cleanPauseMs: 300, refusedIndex: 9, capMessage: 'size cap', deletedCount: 13, cleanTarget: 13, events: [],
    };
    ({ context, page } = await open({ fake: { seed: [['status/s1-size', saved]], cacheFirstGets: 2 } }));
    await page.waitForFunction(() => document.getElementById('app')?.dataset.state === 'clean', null, { timeout: 30_000 });
    const startOff = await page.evaluate(() => document.getElementById('start').disabled);
    const reads = await page.evaluate(() => window.__fakeClaude.log.cacheGets);
    expectRow(G, 'cached status read again', startOff && reads === 2, { summary: `Start ${startOff ? 'disabled' : 'enabled'}, ${reads} cached reads before the server's` });
    await context.close();

    // Run 5: no test override on the page: a saved status that lifts the ceiling and drops the pace is refused.
    ({ context, page } = await open({ noPace: true, fake: { seed: [['status/s1-size', { ...saved, state: 'paused', phase: 'write', outcome: null, maxDocs: 9000, basePauseMs: 0, pauseMs: 0 }]] } }));
    await page.waitForFunction(() => /failed its checks/.test(document.getElementById('instructions')?.textContent ?? ''), null, { timeout: 30_000 });
    const notice = await page.textContent('#instructions');
    const blocked = await page.evaluate(() => document.getElementById('start').disabled && document.getElementById('resume').disabled);
    expectRow(G, 'saved status cannot lift the ceiling', blocked && /maxDocs/.test(notice) && /basePauseMs/.test(notice), { summary: clip(notice, 160) });
    await context.close();
  } finally {
    await server.close();
  }
}

// ---- variants: the automatic checks under faults that must not read as passes

const VARIANT_IDS = ['cdn.bootstrap-map', 'cdn.static-import', 'cdn.integrity-enforced', 'cdn.umd-fallback', 'caps.db-rules'];

async function runVariant(browser, server, { label, fake: fakeOpts, routes }) {
  server.setRoot(path.join(DIST, 'v1'));
  const context = await newContext(browser, { fake: fakeOpts });
  for (const [match, handler] of routes) await context.route(match, handler);
  const page = await context.newPage();
  watch(page, `variant ${label}`);
  try {
    await page.goto(server.url);
    await page.waitForFunction(() => !!window.__s1harness, null, { timeout: 30_000 });
    const finished = await page.evaluate(ms => Promise.race([window.__s1harness.autoDone, new Promise(r => setTimeout(() => r(false), ms))]), AUTO_WAIT_MS);
    expectRow(`variant ${label}`, 'auto checks finish', finished === true, { summary: String(finished) });
    return { context, page };
  } catch (e) {
    await context.close();
    throw e;
  }
}

async function variantsPhase(browser, server) {
  const lock = JSON.parse(fs.readFileSync(path.join(DIST, 'v1', 'lock.json'), 'utf8'));
  const badUrls = new Set([lock.badIntegrity.url, lock.badIntegrity.second.url]);
  const core = lock.umd.find(u => u.name === '@preact/signals-core').url;

  // A: the wrong-hash URLs fail at the network, signals-core answers 404, db arrives after 12 s and the
  // first three run-document writes fail.
  let G = 'variant faults';
  let { context, page } = await runVariant(browser, server, {
    label: 'faults',
    fake: { dbDelayMs: 12_000, writeFaults: { prefix: 'ops/s1-run-', count: 3, code: 'unavailable' } },
    routes: [
      [u => badUrls.has(u.href), route => route.abort('connectionreset')],
      [u => u.href.split('?')[0] === core, route => route.fulfill({ status: 404, contentType: 'text/plain', headers: { 'access-control-allow-origin': '*' }, body: 'Not found\n' })],
    ],
  });
  try {
    let live = await hdoc(page);
    judge(G, 'cdn.integrity-enforced', live.results['cdn.integrity-enforced'], 'auto', { want: ['inconclusive'], data: d => (d.bytesArrivedAndRefused === false && d.sizesExposed === true) || JSON.stringify(d.badUrlTiming) });
    judge(G, 'cdn.umd-fallback', live.results['cdn.umd-fallback'], 'auto', { want: ['inconclusive'], data: d => d.control?.outcome === 'error' || `control ${d.control?.outcome}` });
    const runPath = `ops/s1-run-${live.runId}`;
    const end = Date.now() + 40_000;
    let stored = null;
    let header = null;
    for (;;) {
      stored = await fake(page, 'get', runPath);
      header = await page.evaluate(() => ({ state: document.querySelector('.db-state')?.dataset.state, notice: document.querySelector('.notice')?.textContent ?? '' }));
      live = await hdoc(page);
      const caught = stored && Object.keys(stored.results ?? {}).length === Object.keys(live.results).length;
      if ((caught && header.state === 'connected') || Date.now() > end) break;
      await sleep(500);
    }
    const flog = await page.evaluate(() => window.__fakeClaude.log);
    expectRow(G, 'late db taken, results saved', !!stored && live.harness.log.some(l => l.includes('db arrived late')) && flog.writeFaults === 3, { summary: `stored ${stored ? Object.keys(stored.results ?? {}).length : 0} of ${Object.keys(live.results).length} results, ${flog.writeFaults} injected write faults` });
    expectRow(G, 'header recovers after failed saves', header.state === 'connected' && !header.notice.includes('Last save failed') && Object.keys(live.harness.writes.failing).length === 0, { summary: `header ${header.state}; ${clip(header.notice, 120) || 'no notice'}` });
  } finally {
    await context.close();
  }

  // B: a host import map ahead of the page's, Resource Timing sizes hidden (no Timing-Allow-Origin), and a
  // publish that did not declare the canary rule.
  G = 'variant host map';
  // Also: names withheld (the profile half of caps.user).
  const hostMap = '<script type="importmap">{"imports":{"preact":"https://cdn.jsdelivr.net/npm/preact@10.29.8/dist/preact.module.js"}}</script>';
  ({ context, page } = await runVariant(browser, server, {
    label: 'host map',
    fake: { selfPrefixes: ['data/users'], withholdNames: true },
    routes: [
      [u => u.hostname === '127.0.0.1' && (u.pathname === '/' || u.pathname === '/index.html'), async route => {
        const resp = await route.fetch();
        route.fulfill({ response: resp, body: (await resp.text()).replace('<body>', `<body>${hostMap}`) });
      }],
      [u => u.hostname === 'cdn.jsdelivr.net', route => serveNpm(route, new URL(route.request().url()), route.request(), { tao: false })],
    ],
  }));
  try {
    const live = await hdoc(page);
    const r = live.results;
    judge(G, 'cdn.bootstrap-map', r['cdn.bootstrap-map'], 'auto', { want: ['fail'], data: d => (d.mapCount === 2 && /10\.29\.8/.test(d.moduleResolvesPreact?.url ?? '')) || JSON.stringify(d.moduleResolvesPreact) });
    judge(G, 'cdn.static-import', r['cdn.static-import'], 'auto', { want: ['fail'] });
    judge(G, 'cdn.integrity-enforced', r['cdn.integrity-enforced'], 'auto', { want: ['pass'], data: d => (d.mapFound === true && d.mapCount === 2 && d.sizesExposed === false && d.second?.state === 'rejected') || 'the page did not read its own map, or sizes were exposed' });
    judge(G, 'caps.db-rules', r['caps.db-rules'], 'auto', { want: ['inconclusive'], data: d => (d.outcomes?.canaryNotMe?.set?.ok === true) || 'the canary write was not accepted' });
    judge(G, 'caps.user', r['caps.user'], 'auto', { want: ['inconclusive'], data: d => (d.id?.nonEmpty === true && d.me?.nameNonEmpty === false) || 'the names were not withheld' });
    const stray = Object.keys(r).filter(id => !VARIANT_IDS.includes(id) && !EXPECT[id]);
    if (stray.length) notes.push(`variant host map: results without an expectation: ${stray.join(', ')}`);
  } finally {
    await context.close();
  }
}

// ---- the KaTeX HTML comparison sheet

async function katexPhase(browser) {
  const G = 'screenshots';
  const r = spawnSync(process.execPath, [path.join(ROOT, 'tools', 'katex-html.mjs')], { cwd: ROOT, encoding: 'utf8' });
  expectRow(G, 'tools/katex-html.mjs', r.status === 0, { summary: (r.stdout || r.stderr).trim() });
  if (r.status !== 0) return;
  const context = await browser.newContext({ viewport: VIEWPORT, deviceScaleFactor: 2, colorScheme: 'light', locale: 'en-GB' });
  await context.route(() => true, routeRequest);
  const page = await context.newPage();
  watch(page, 'katex-html');
  try {
    await page.goto(pathToFileURL(path.join(COMPARE, 'katex-html.html')).href);
    await page.waitForFunction(() => document.documentElement.dataset.ready === '1', null, { timeout: 30_000 });
    const fonts = await page.evaluate(() => document.documentElement.dataset.fonts);
    const m = /loaded (\d+), error (\d+)/.exec(fonts ?? '');
    expectRow(G, 'KaTeX fonts load in the sheet', !!m && Number(m[1]) > 0 && Number(m[2]) === 0, { summary: fonts });
    await page.screenshot({ path: SHOTS.katex, fullPage: true });
    say(`wrote ${path.relative(ROOT, SHOTS.katex)}`);
  } finally {
    await context.close();
  }
}

// ---- report

function report() {
  const pad = (s, n) => clip(s, n).padEnd(n);
  console.log('');
  console.log(`${pad('group', 19)} ${pad('check', 41)} ${pad('kind', 9)} ${pad('status', 12)} ${pad('expected', 18)} ok   summary`);
  for (const r of rows) {
    console.log(`${pad(r.group, 19)} ${pad(r.id, 41)} ${pad(r.kind, 9)} ${pad(r.status, 12)} ${pad(r.want, 18)} ${r.ok ? 'ok  ' : 'FAIL'} ${clip(r.summary, 220)}`);
  }
  console.log('');
  const byHost = [...traffic.npm].map(([k, v]) => `${k} ${v}`).join(', ');
  console.log(`CDN from npm/: ${byHost || 'none'}; by requester ${JSON.stringify(traffic.npmByRequester)}`);
  if (traffic.npmMissing.length) console.log(`CDN paths not in npm/: ${traffic.npmMissing.slice(0, 10).join('; ')}`);
  console.log(`cdnjs requests (404): ${traffic.cdnjs.length}; Google Fonts requests: ${traffic.fonts.length}`);
  console.log(`outside requests aborted: ${traffic.outside.length ? traffic.outside.map(o => `${o.from} ${o.url}`).join('; ') : 'none'}`);
  console.log(`page errors: ${pageProblems.length ? pageProblems.map(p => `${p.label}: ${p.text}`).join('; ') : 'none'}`);
  console.log(`console errors: ${consoleErrors.length}${consoleErrors.length ? ` (first: ${consoleErrors.slice(0, 6).map(c => `${c.label}: ${c.text}`).join(' | ')})` : ''}`);
  for (const n of notes) console.log(n);
  for (const s of Object.values(SHOTS)) console.log(`screenshot: ${s}${fs.existsSync(s) ? '' : ' (not written)'}`);
  const failed = rows.filter(r => !r.ok);
  console.log(`\n${rows.length - failed.length} of ${rows.length} expectations met in ${((Date.now() - started) / 1000).toFixed(0)} s.`);
  return failed.length;
}

// ---- main

async function main() {
  say('building with tools/build.mjs --strict');
  const build = spawnSync(process.execPath, [path.join(ROOT, 'tools', 'build.mjs'), '--strict'], { cwd: ROOT, encoding: 'utf8' });
  expectRow('build', 'build --strict', build.status === 0, { summary: `${build.stdout}${build.stderr}`.trim().split('\n').slice(-4).join(' | ') });
  if (build.status !== 0) return;
  const manifest = JSON.parse(fs.readFileSync(path.join(DIST, 'manifest.json'), 'utf8'));
  const plan = manifest.publishPlan;
  const batches = plan.v2FallbackBatches;
  const nulls = batches.flatMap(b => b.nullRemovals);
  const removed = manifest.republish.removed;
  expectRow('build', 'publish plan splits the removals', plan.v2.entries === 1 + manifest.republish.added.length + manifest.republish.changed.length - 1 + removed.length
    && batches.every(b => b.entries <= 255) && nulls.length === removed.length && new Set(nulls).size === removed.length
    && batches[0].nullRemovals[0] === 'data/v1-only.json' && batches[0].nullRemovals[1] === 'bulk/b-001.json'
    && plan.v1.capabilities.db.rules.some(r => r.path === 's1canary/{self}')
    && Object.keys(plan.v1.capabilities).sort().join() === 'db,sample,user', { summary: `v2 ${plan.v2.entries} entries; batches ${batches.map(b => b.entries).join(' + ')}; first removals ${batches[0]?.nullRemovals.slice(0, 2).join(', ')}` });
  fs.mkdirSync(COMPARE, { recursive: true });

  const exe = chromiumPath();
  if (!exe) {
    expectRow('setup', 'Chromium found', false, { summary: 'Set ZQ_CHROMIUM or install a Chromium under /opt/pw-browsers.' });
    return;
  }
  const { chromium } = await import(pathToFileURL(PLAYWRIGHT).href);
  const browser = await chromium.launch({ executablePath: exe, args: ['--no-proxy-server'] });
  notes.push(`browser: ${exe}, version ${browser.version()}`);
  const server = await createServer({ root: path.join(DIST, 'v1'), allowBase: DIST, log: line => notes.push(`serve: ${line}`) });
  try {
    for (const [name, phase] of [['probe', () => probePhase(browser, server)], ['variants', () => variantsPhase(browser, server)], ['dbsize', () => dbsizePhase(browser)], ['katex', () => katexPhase(browser)]]) {
      try {
        await phase();
      } catch (e) {
        expectRow(name, `${name} phase ran to the end`, false, { summary: errText(e) });
      }
    }
    const opened = new Set(['popup', 'new page']);
    const fromProbe = traffic.outside.filter(o => !opened.has(o.from));
    const fromPopups = traffic.outside.filter(o => opened.has(o.from));
    expectRow('network', 'no outside request from a probe', fromProbe.length === 0, { summary: fromProbe.length ? fromProbe.map(o => `${o.from} ${o.url}`).join('; ') : 'none' });
    expectRow('network', 'popups only open example.org', fromPopups.every(o => o.url.startsWith('https://www.example.org/')), { summary: `${fromPopups.length} popup requests: ${[...new Set(fromPopups.map(o => o.url))].join(', ') || 'none'}` });
    expectRow('network', 'every CDN path exists in npm/', traffic.npmMissing.length === 0, { summary: traffic.npmMissing.length ? traffic.npmMissing.slice(0, 5).join('; ') : `${[...traffic.npm.values()].reduce((a, b) => a + b, 0)} requests answered` });
    expectRow('network', 'no uncaught page error', pageProblems.length === 0, { summary: pageProblems.length ? pageProblems.map(p => `${p.label}: ${p.text}`).join('; ') : 'none' });
  } finally {
    await browser.close();
    await server.close();
  }
}

try {
  await main();
} catch (e) {
  expectRow('test', 'tools/test.mjs ran', false, { summary: e?.stack ?? errText(e) });
}
process.exit(report() ? 1 : 0);
